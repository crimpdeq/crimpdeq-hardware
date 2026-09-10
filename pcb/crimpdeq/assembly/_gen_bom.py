#!/usr/bin/env python3
"""Generate the design-local PCBWay BOM from its board and schematic."""

import csv
import re
import subprocess
import tempfile
from pathlib import Path

import pcbnew


EXPECTED_REFS = frozenset(
    "C1 C2 C3 C4 C5 C6 C9 C10 C11 C12 C15 C16 C17 C18 C19 "
    "D1 D2 D3 D4 D7 D8 D9 D10 J2 J5 J6 J7 J8 J9 J10 J11 J12 L1 Q2 "
    "R1 R2 R3 R7 R8 R9 R13 R14 R15 R16 R17 R18 R19 R20 R21 R22 "
    "U1 U2 U3 U5 U6".split()
)
DNP_REFS = frozenset({"J5", "J6", "J7", "J8", "J9", "J10", "J11", "J12"})
EXPECTED_PART_GROUPS = (
    ("C1 C3", "1uF 16V", "C_0402_1005Metric"),
    ("C2 C18", "100nF 10V", "C_0402_1005Metric"),
    ("C4", "10nF 10V", "C_0402_1005Metric"),
    ("C5 C6", "4.7uF 16V", "C_0603_1608Metric"),
    ("C9 C10", "10uF", "C_0603_1608Metric"),
    ("C11 C12 C19", "0.1uF", "C_0603_1608Metric"),
    ("C15 C17", "10uF 16V", "C_0805_2012Metric"),
    ("C16", "22pF 50V", "C_0603_1608Metric"),
    ("D1", "LED", "LED_0603_1608Metric"),
    ("D2 D8", "B5819W", "D_SOD-123"),
    ("D3", "LESD8D3.3CAT5G", "D_SOD-882"),
    ("D4", "WS2812B", "LED_WS2812B_PLCC4_5.0x5.0mm_P3.2mm"),
    ("D7 D9 D10", "LESD5D5.0CT1G", "D_SOD-523"),
    ("J2", "USB4105-GF-A", "GCT_USB4105-GF-A"),
    ("J5", "B-_Cable_Pad", "TestPoint_THTPad_D1.5mm_Drill0.7mm"),
    ("J6", "SW+_Cable_Pad", "TestPoint_THTPad_D1.5mm_Drill0.7mm"),
    ("J7", "B+_Cable_Pad", "TestPoint_THTPad_D1.5mm_Drill0.7mm"),
    ("J8", "SW-_Cable_Pad", "TestPoint_THTPad_D1.5mm_Drill0.7mm"),
    ("J9", "A+_Cable_Pad", "TestPoint_THTPad_D1.5mm_Drill0.7mm"),
    ("J10", "A-_Cable_Pad", "TestPoint_THTPad_D1.5mm_Drill0.7mm"),
    ("J11", "E+_Cable_Pad", "TestPoint_THTPad_D1.5mm_Drill0.7mm"),
    ("J12", "E-_Cable_Pad", "TestPoint_THTPad_D1.5mm_Drill0.7mm"),
    ("L1", "SPH4018H2R2MT (2.2uH 2.2A)", "L_Bourns-SRN4018"),
    ("Q2", "DMG3415U", "SOT-23"),
    ("R1 R2 R14 R20 R21 R22", "10kR 1%", "R_0402_1005Metric"),
    ("R3", "1kR 1%", "R_0402_1005Metric"),
    ("R7 R8", "100R 1%", "R_0402_1005Metric"),
    ("R9 R15", "100kR 1%", "R_0402_1005Metric"),
    ("R13 R17", "0R 1%", "R_0402_1005Metric"),
    ("R16", "22k1R 1%", "R_0402_1005Metric"),
    ("R18 R19", "5k1R 1%", "R_0402_1005Metric"),
    ("U1", "ESP32-C3-MINI-1", "ESP32-C3-MINI-1"),
    ("U2", "MCP73831T-2ACI/OT", "SOT-23-5"),
    ("U3", "ADS1220", "TSSOP-16_4.4x5mm_P0.65mm"),
    ("U5", "MAX17048G+T10", "TDFN-8-1EP_2x2mm_P0.5mm_EP0.8x1.2mm"),
    ("U6", "SY8088", "SOT-23-5"),
)
EXPECTED_PARTS = {
    reference: (value, footprint)
    for references, value, footprint in EXPECTED_PART_GROUPS
    for reference in references.split()
}

# Overrides for blank, corrupt, or unsuitable schematic fields.
OVERRIDES = {
    "D4": "C52917433",  # WS2812B-V6, Worldsemi, SMD5050-4P
    "U3": "C48263",  # ADS1220IPWR TSSOP-16, Texas Instruments
    "U5": "C2682616",  # MAX17048G+T10 DFN-8-EP 2x2, Maxim
    "C9": "C19702",
    "C10": "C19702",  # 10uF 10V X5R 0603
    "C11": "C14663",
    "C12": "C14663",  # 100nF 50V X7R 0603
    "C19": "C14663",
    "C18": "C1525",  # 100nF 10V X7R 0402
    "R7": "C25076",
    "R8": "C25076",  # 100R 0402 1%
    "R13": "C17168",  # 0R 0402
    "R1": "C60490",
    "R2": "C60490",
    "R14": "C60490",
    "R20": "C60490",
    "R21": "C60490",
    "R22": "C60490",  # 10kR 0402 1%
    "D7": "C2982332",
    "D9": "C2982332",
    "D10": "C2982332",  # SOD-523 bidirectional 5V ESD
}


def refkey(reference):
    match = re.match(r"([A-Za-z]+)(\d+)", reference)
    return (match.group(1), int(match.group(2))) if match else (reference, 0)


def mount_type(footprint):
    reference = footprint.GetReference()
    if reference == "J2":
        return "Hybrid"
    attrs = footprint.GetAttributes()
    smd = bool(attrs & pcbnew.FP_SMD)
    tht = bool(attrs & pcbnew.FP_THROUGH_HOLE)
    if smd and tht:
        return "Hybrid"
    if tht:
        return "THT"
    if smd:
        return "SMD"
    name = footprint.GetFPID().GetLibItemName().wx_str()
    if "THT" in name:
        return "THT"
    return "SMD"


def part_notes(reference):
    if reference in DNP_REFS:
        return "Do Not Place"
    if reference == "J2":
        return "PTH shell tabs; THT/manual soldering"
    return ""


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

actual_parts = {
    reference: (
        footprint.GetValue(),
        footprint.GetFPID().GetLibItemName().wx_str(),
    )
    for reference, footprint in footprints.items()
}
if actual_parts != EXPECTED_PARTS:
    changed = sorted(
        (reference, EXPECTED_PARTS.get(reference), actual_parts.get(reference))
        for reference in set(EXPECTED_PARTS) | set(actual_parts)
        if EXPECTED_PARTS.get(reference) != actual_parts.get(reference)
    )
    raise SystemExit(f"BOM value/footprint mismatch: {changed}")

expected_pullups = {
    reference: ("10kR 1%", "R_0402_1005Metric")
    for reference in ("R20", "R21", "R22")
}
actual_pullups = {reference: actual_parts[reference] for reference in expected_pullups}
if actual_pullups != expected_pullups:
    raise SystemExit(
        f"hardware pull-up mismatch: actual={actual_pullups}, expected={expected_pullups}"
    )

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
    parts.append(
        (
            reference,
            value,
            footprint_name,
            code,
            mount_type(footprint),
            part_notes(reference),
        )
    )

if blank_non_dnp_refs:
    raise SystemExit(f"BOM validation failed; blank non-DNP refs={blank_non_dnp_refs}")

groups = {}
for reference, value, footprint_name, code, kind, notes in parts:
    groups.setdefault((value, footprint_name, code, kind, notes), []).append(reference)

rows = []
for (value, footprint_name, code, kind, notes), references in groups.items():
    ordered = sorted(references, key=refkey)
    rows.append((value, ",".join(ordered), len(ordered), footprint_name, code, kind, notes))
rows.sort(key=lambda row: refkey(row[1].split(",")[0]))

with out.open("w", newline="") as destination:
    writer = csv.writer(destination, lineterminator="\n")
    writer.writerow(
        ["Item", "Quantity", "Designator", "Value", "Footprint", "MPN", "Type", "Notes"]
    )
    for item, (value, designators, quantity, footprint_name, code, kind, notes) in enumerate(
        rows, start=1
    ):
        writer.writerow(
            [item, quantity, designators, value, footprint_name, code, kind, notes]
        )

filled = sum(1 for reference, _, _, code, _, _ in parts if code)
print(f"BOM written: {out}")
print(f"  grouped lines: {len(rows)}   placements: {len(parts)}   with MPN: {filled}/{len(parts)}")
print(f"  DNP cable pads: {', '.join(sorted(DNP_REFS))}")
