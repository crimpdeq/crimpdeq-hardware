#!/usr/bin/env python3
"""Generate the canonical design's PCBWay component placement list."""

import csv
import re
import subprocess
import tempfile
from pathlib import Path


EXPECTED_REFS = frozenset(
    "C1 C2 C3 C4 C5 C6 C9 C10 C11 C12 C15 C16 C17 C18 C19 "
    "D1 D2 D3 D4 D7 D8 D9 D10 J2 J5 J6 J7 J8 J9 J10 J11 J12 L1 Q2 "
    "R1 R2 R3 R7 R8 R9 R13 R14 R15 R16 R17 R18 R19 R20 R21 R22 "
    "U1 U2 U3 U5 U6".split()
)
TOP_ROTATION_OFFSETS = {"U3": 270.0, "U6": 180.0}
# J2 uses the GCT body centroid. Cable pads J5-J12 are DNP THT pads.
POSITION_OVERRIDES = {
    "J2": (147.0000, -78.5350),
}
CORRECTION_EXPECTATIONS = {
    "D4": ("LED_WS2812B_PLCC4_5.0x5.0mm_P3.2mm", "bottom"),
    "J2": ("GCT_USB4105-GF-A", "top"),
    "Q2": ("SOT-23", "bottom"),
    "U2": ("SOT-23-5", "bottom"),
    "U3": ("TSSOP-16_4.4x5mm_P0.65mm", "top"),
    "U5": ("TDFN-8-1EP_2x2mm_P0.5mm_EP0.8x1.2mm", "top"),
    "U6": ("SOT-23-5", "top"),
}
ROTATION_EXPECTATIONS = {
    "D4": 90.0,
    "Q2": 270.0,
    "U2": 270.0,
    "U5": 180.0,
    "U6": 90.0,
}


def refkey(reference):
    match = re.match(r"([A-Za-z]+)(\d+)", reference)
    return (match.group(1), int(match.group(2))) if match else (reference, 0)


version_dir = Path(__file__).resolve().parents[1]
design_name = version_dir.name
project_name = "crimpdeq"
board_path = version_dir / f"{project_name}.kicad_pcb"
bom_path = version_dir / "assembly" / f"{design_name}_bom.csv"
out = version_dir / "assembly" / f"{design_name}_cpl.csv"

if not bom_path.is_file():
    raise SystemExit(f"generate the BOM before the CPL: {bom_path}")
with bom_path.open(encoding="utf-8-sig") as source:
    bom_refs = {
        reference.strip()
        for row in csv.DictReader(source)
        for reference in row["Designator"].split(",")
        if reference.strip()
    }
if bom_refs != EXPECTED_REFS:
    raise SystemExit(
        f"BOM reference mismatch; missing={sorted(EXPECTED_REFS - bom_refs)}, "
        f"extra={sorted(bom_refs - EXPECTED_REFS)}"
    )

with tempfile.TemporaryDirectory(prefix=f"{design_name}-cpl-") as temp_dir:
    raw_path = Path(temp_dir) / "positions.csv"
    subprocess.run(
        [
            "kicad-cli",
            "pcb",
            "export",
            "pos",
            "--format",
            "csv",
            "--units",
            "mm",
            "--side",
            "both",
            "--output",
            str(raw_path),
            str(board_path),
        ],
        check=True,
    )
    with raw_path.open(encoding="utf-8-sig") as source:
        rows = list(csv.DictReader(source))

raw_refs = [row["Ref"] for row in rows]
if len(raw_refs) != len(set(raw_refs)):
    raise SystemExit("duplicate references in KiCad position export")
if set(raw_refs) != EXPECTED_REFS:
    raise SystemExit(
        f"position reference mismatch; missing={sorted(EXPECTED_REFS - set(raw_refs))}, "
        f"extra={sorted(set(raw_refs) - EXPECTED_REFS)}"
    )

rows.sort(key=lambda row: refkey(row["Ref"]))
with out.open("w", newline="") as destination:
    writer = csv.writer(destination, lineterminator="\n")
    writer.writerow(["Designator", "Mid X", "Mid Y", "Rotation", "Layer"])
    for row in rows:
        reference = row["Ref"]
        side = row["Side"].lower()
        if side not in {"top", "bottom"}:
            raise SystemExit(f"unexpected side for {reference}: {side}")
        if reference in CORRECTION_EXPECTATIONS:
            expected_package, expected_side = CORRECTION_EXPECTATIONS[reference]
            if row["Package"] != expected_package or side != expected_side:
                raise SystemExit(
                    f"correction assumptions changed for {reference}: "
                    f"package={row['Package']} side={side}, expected "
                    f"package={expected_package} side={expected_side}"
                )

        rotation = float(row["Rot"])
        if side == "bottom":
            rotation = 180.0 - rotation
        else:
            rotation += TOP_ROTATION_OFFSETS.get(reference, 0.0)
        rotation %= 360.0
        if reference in ROTATION_EXPECTATIONS:
            expected_rotation = ROTATION_EXPECTATIONS[reference]
            if abs((rotation - expected_rotation + 180.0) % 360.0 - 180.0) > 0.01:
                raise SystemExit(
                    f"{reference} assembly rotation mismatch: "
                    f"actual={rotation:.2f}, expected={expected_rotation:.2f}"
                )

        x = float(row["PosX"])
        y = float(row["PosY"])
        if reference in POSITION_OVERRIDES:
            x, y = POSITION_OVERRIDES[reference]

        writer.writerow([reference, f"{x:.4f}", f"{y:.4f}", f"{rotation:.2f}", side])

print(f"CPL written: {out} ({len(rows)} parts)")
