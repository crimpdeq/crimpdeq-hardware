#!/usr/bin/env python3
"""Generate the design-local JLCPCB BOM from its board and schematic."""

import csv
import re
import subprocess
import tempfile
from pathlib import Path

import pcbnew


EXPECTED_REFS = frozenset(
    "C1 C2 C3 C4 C5 C6 C9 C10 C11 C12 C15 C16 C17 C18 "
    "D1 D2 D3 D4 D7 D8 D9 D10 J2 J3 J4 L1 Q1 Q2 "
    "R1 R2 R3 R5 R6 R7 R8 R9 R13 R14 R15 R16 R17 R18 R19 "
    "U1 U2 U3 U5 U6".split()
)
DNP_REFS = frozenset({"J3", "J4"})

# Overrides for blank, corrupt, or unsuitable fields in the frozen upstream schematic.
OVERRIDES = {
    "D4": "C52917433",  # WS2812B-V6, Worldsemi, SMD5050-4P
    "U3": "C43656",  # HX711 SOP-16, Avia Semicon
    "U5": "C2682616",  # MAX17048G+T10 DFN-8-EP 2x2, Maxim
    "Q1": "C266595",  # SS8550 SOT-23 PNP
    "C9": "C19702",
    "C10": "C19702",  # 10uF 10V X5R 0603
    "C11": "C14663",
    "C12": "C14663",  # 100nF 50V X7R 0603
    "C18": "C1525",  # 100nF 10V X7R 0402
    "R5": "C25752",  # 12kR 0402 1%
    "R6": "C136971",  # 8k2R 0402 1%
    "R7": "C25076",
    "R8": "C25076",  # 100R 0402 1%
    "R13": "C17168",  # 0R 0402
    "R1": "C60490",
    "R2": "C60490",
    "R14": "C60490",  # 10kR 0402 1%
    "D7": "C2982332",
    "D9": "C2982332",
    "D10": "C2982332",  # SOD-523 bidirectional 5V ESD
}


def refkey(reference):
    match = re.match(r"([A-Za-z]+)(\d+)", reference)
    return (match.group(1), int(match.group(2))) if match else (reference, 0)


version_dir = Path(__file__).resolve().parents[1]
design_name = version_dir.name
project_name = "crimpdeq"
board_path = version_dir / f"{project_name}.kicad_pcb"
schematic_path = version_dir / f"{project_name}.kicad_sch"
out = version_dir / "assembly" / f"{design_name}_bom.csv"

with tempfile.TemporaryDirectory(prefix=f"{design_name}-bom-") as temp_dir:
    schematic_bom = Path(temp_dir) / "schematic.csv"
    subprocess.run(
        [
            "kicad-cli",
            "sch",
            "export",
            "bom",
            "--fields",
            "Reference,Value,Footprint,LCSC",
            "--group-by",
            "",
            "--ref-range-delimiter",
            "",
            "--output",
            str(schematic_bom),
            str(schematic_path),
        ],
        check=True,
    )
    with schematic_bom.open(encoding="utf-8-sig") as source:
        lcsc = {
            row["Reference"].strip(): row["LCSC"].strip()
            for row in csv.DictReader(source)
        }

board = pcbnew.LoadBoard(str(board_path))
footprints = {footprint.GetReference(): footprint for footprint in board.GetFootprints()}
if set(footprints) != EXPECTED_REFS:
    missing = sorted(EXPECTED_REFS - set(footprints))
    extra = sorted(set(footprints) - EXPECTED_REFS)
    raise SystemExit(f"unexpected board references; missing={missing}, extra={extra}")

missing_schematic_refs = sorted(set(footprints) - set(lcsc) - DNP_REFS)
if missing_schematic_refs:
    raise SystemExit(f"board references missing from schematic: {missing_schematic_refs}")

reference_path = version_dir.parent / "crimpdeq-v2" / "crimpdeq.kicad_pcb"
reference_board = pcbnew.LoadBoard(str(reference_path))
reference_parts = {
    footprint.GetReference(): (
        footprint.GetValue(),
        footprint.GetFPID().GetLibItemName().wx_str(),
    )
    for footprint in reference_board.GetFootprints()
}
actual_parts = {
    reference: (
        footprint.GetValue(),
        footprint.GetFPID().GetLibItemName().wx_str(),
    )
    for reference, footprint in footprints.items()
}
if actual_parts != reference_parts:
    changed = sorted(
        (reference, reference_parts.get(reference), actual_parts.get(reference))
        for reference in set(reference_parts) | set(actual_parts)
        if reference_parts.get(reference) != actual_parts.get(reference)
    )
    raise SystemExit(f"BOM value/footprint mismatch vs frozen reference: {changed}")

lcsc.update(OVERRIDES)

parts = []
blank_non_dnp_refs = []
for reference in sorted(footprints, key=refkey):
    footprint = footprints[reference]
    value = footprint.GetValue()
    footprint_name = footprint.GetFPID().GetLibItemName().wx_str()
    code = lcsc.get(reference, "")
    if not code and reference not in DNP_REFS:
        blank_non_dnp_refs.append(reference)
    parts.append((reference, value, footprint_name, code))

if blank_non_dnp_refs:
    raise SystemExit(f"BOM validation failed; blank non-DNP refs={blank_non_dnp_refs}")

groups = {}
for reference, value, footprint_name, code in parts:
    groups.setdefault((value, footprint_name, code), []).append(reference)

rows = []
for (value, footprint_name, code), references in groups.items():
    designators = ",".join(sorted(references, key=refkey))
    rows.append((value, designators, footprint_name, code))
rows.sort(key=lambda row: refkey(row[1].split(",")[0]))

with out.open("w", newline="") as destination:
    writer = csv.writer(destination, lineterminator="\n")
    writer.writerow(["Comment", "Designator", "Footprint", "LCSC Part #"])
    writer.writerows(rows)

filled = sum(1 for reference, _, _, code in parts if code)
print(f"BOM written: {out}")
print(f"  grouped lines: {len(rows)}   placements: {len(parts)}   with LCSC: {filled}/{len(parts)}")
print(f"  DNP cable pads: {', '.join(sorted(DNP_REFS))}")
