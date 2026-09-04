#!/usr/bin/env python3
"""Verify the canonical Crimpdeq electrical and layout invariants."""

import math
import sys

import pcbnew


EXPECTED_REFS = frozenset(
    "C1 C2 C3 C4 C5 C6 C9 C10 C11 C12 C15 C16 C17 C18 C19 "
    "D1 D2 D3 D4 D7 D8 D9 D10 J2 J5 J6 J7 J8 J9 J10 J11 J12 L1 Q2 "
    "R1 R2 R3 R7 R8 R9 R13 R14 R15 R16 R17 R18 R19 R20 R21 R22 "
    "U1 U2 U3 U5 U6".split()
)

COMPONENT_GEOMETRY = {
    # Pad coordinates are normalized to the component side, so bottom-side
    # packages can be compared directly with their datasheet top views.
    "D4": (pcbnew.B_Cu, 90.0, ":LED_WS2812B_PLCC4_5.0x5.0mm_P3.2mm", {
        "1": (-2.45, -1.65), "2": (-2.45, 1.65),
        "3": (2.45, 1.65), "4": (2.45, -1.65),
    }),
    "Q2": (pcbnew.B_Cu, -90.0, ":SOT-23", {
        "1": (-0.9375, -0.95), "2": (-0.9375, 0.95), "3": (0.9375, 0.0),
    }),
    "U2": (pcbnew.B_Cu, -90.0, ":SOT-23-5", {
        "1": (-1.1375, -0.95), "2": (-1.1375, 0.0), "3": (-1.1375, 0.95),
        "4": (1.1375, 0.95), "5": (1.1375, -0.95),
    }),
    "U5": (pcbnew.F_Cu, 180.0, ":TDFN-8-1EP_2x2mm_P0.5mm_EP0.8x1.2mm", {
        "1": (-0.9875, -0.75), "2": (-0.9875, -0.25),
        "3": (-0.9875, 0.25), "4": (-0.9875, 0.75),
        "5": (0.9875, 0.75), "6": (0.9875, 0.25),
        "7": (0.9875, -0.25), "8": (0.9875, -0.75), "9": (0.0, 0.0),
    }),
    "U6": (pcbnew.F_Cu, -90.0, ":SOT-23-5", {
        "1": (-1.1375, -0.95), "2": (-1.1375, 0.0), "3": (-1.1375, 0.95),
        "4": (1.1375, 0.95), "5": (1.1375, -0.95),
    }),
}

GOLDEN_NETS = {
    "+3V3": (
        "C1.1 C2.1 C4.1 C9.1 C10.1 C11.1 C16.1 C17.1 C19.1 D3.1 D4.1 "
        "J11.1 L1.2 R1.1 R15.1 R20.2 R21.2 R22.2 U1.3 U3.9 U3.12 U3.13"
    ),
    "+BATT": "C6.1 C18.1 J6.1 J7.1 U2.3 U5.2 U5.3",
    "Buck_Coil": "L1.1 U6.3",
    "A+": "J9.1 R7.2",
    "A-": "J10.1 R8.2",
    "CHIP_PU": "C3.1 R1.2 U1.8",
    "ENABLE": "R14.2 U6.1",
    "GND": (
        "C1.2 C2.2 C3.2 C4.2 C5.1 C6.2 C9.2 C10.2 C11.2 C15.2 C17.2 "
        "C18.2 C19.2 D3.2 D4.3 D7.2 D9.2 D10.2 J2.A1_B12 J2.B1_A12 J5.1 J12.1 R2.1 "
        "R9.2 R16.2 R17.2 R18.2 R19.2 U1.1 U1.2 U1.11 U1.14 U1.36 "
        "U1.37 U1.38 U1.39 U1.40 U1.41 U1.42 U1.43 U1.44 U1.45 U1.46 "
        "U1.47 U1.48 U1.49 U1.50 U1.51 U1.52 U1.53 U2.2 U3.3 U3.4 U3.5 "
        "U3.8 U5.1 U5.4 U5.6 U5.9 U6.2"
    ),
    "IO10_ALRT": "R22.1 U1.16 U5.5",
    "IO1_MISO": "U1.13 U3.15",
    "IO2_LED": "R13.1 U1.5",
    "IO3_CS": "U1.6 U3.2",
    "IO4_MOSI": "U1.18 U3.16",
    "IO5_SCK": "U1.19 U3.1",
    "IO6_SDA": "R20.1 U1.20 U5.7",
    "IO7_SCL": "R21.1 U1.21 U5.8",
    "Net-(D1-K)": "D1.1 R3.2",
    "Net-(D4-DIN)": "D4.4 R13.2",
    "Net-(D8-A)": "D8.2 D9.1 J2.A4_B9 J2.B4_A9",
    "Net-(J2-CC1)": "J2.A5 R19.1",
    "Net-(J2-CC2)": "J2.B5 R18.1",
    "Net-(J2-SHELL_GND-PadS1)": "J2.S1 J2.S2 J2.S3 J2.S4 R17.1",
    "Net-(U2-PROG)": "R2.2 U2.5",
    "Net-(U2-STAT)": "R3.1 U2.1",
    "Net-(U3-AIN0)": "C12.1 R7.1 U3.11",
    "Net-(U3-AIN1)": "C12.2 R8.1 U3.10",
    "Net-(U6-FB)": "C16.2 R15.2 R16.1 U6.5",
    "SW_BATT": "J8.1 Q2.3",
    "USB_D+": "D10.1 J2.A6 J2.B6 U1.27",
    "USB_D-": "D7.1 J2.A7 J2.B7 U1.26",
    "VBUS": "C5.2 D1.2 D2.2 D8.1 Q2.1 R9.1 U2.4",
    "VSYS": "C15.1 D2.1 Q2.2 R14.1 U6.4",
}


def mm(value):
    return pcbnew.ToMM(value)


def board_tracks(board):
    """Return tracks without relying on the broken Python 3.14 SWIG iterator."""
    items = board.Tracks()
    return [items[index] for index in range(items.size())]


def net_metrics(board, net_name):
    length = 0.0
    vias = 0
    layers = set()
    for item in board_tracks(board):
        if item.GetNetname() != net_name:
            continue
        if item.Type() == pcbnew.PCB_VIA_T:
            vias += 1
        else:
            start, end = item.GetStart(), item.GetEnd()
            length += math.hypot(mm(start.x - end.x), mm(start.y - end.y))
            layers.add(pcbnew.LayerName(item.GetLayer()))
    return length, vias, layers


def pad(footprint, number):
    matches = [item for item in footprint.Pads() if item.GetPadName() == number]
    if not matches:
        raise ValueError(f"{footprint.GetReference()}.{number} not found")
    return matches[0]


def via_in_paste(board):
    overlaps = []
    for item in board_tracks(board):
        if item.Type() != pcbnew.PCB_VIA_T:
            continue
        via = pcbnew.Cast_to_PCB_VIA(item)
        radius = via.GetDrillValue() // 2
        for footprint in board.GetFootprints():
            for layer in (pcbnew.F_Paste, pcbnew.B_Paste):
                if footprint.GetLayer() not in (pcbnew.F_Cu, pcbnew.B_Cu):
                    continue
                for pad_item in footprint.Pads():
                    if pad_item.GetEffectiveShape(layer).Collide(via.GetPosition(), radius):
                        overlaps.append(
                            f"{footprint.GetReference()}.{pad_item.GetPadName()}@"
                            f"({mm(via.GetPosition().x):.3f},{mm(via.GetPosition().y):.3f})"
                        )
    return overlaps


def verify_golden_netlist(footprints):
    expected = {}
    for net_name, pad_names in GOLDEN_NETS.items():
        for pad_name in pad_names.split():
            if pad_name in expected:
                raise SystemExit(f"duplicate golden pad: {pad_name}")
            expected[pad_name] = net_name

    actual = {}
    for reference, footprint in footprints.items():
        for item in footprint.Pads():
            number = item.GetPadName()
            net_name = item.GetNetname()
            if not number or not net_name or net_name.startswith("unconnected-"):
                continue
            pad_name = f"{reference}.{number}"
            if pad_name in actual and actual[pad_name] != net_name:
                raise SystemExit(
                    f"physical pads named {pad_name} disagree: "
                    f"{actual[pad_name]} vs {net_name}"
                )
            actual[pad_name] = net_name

    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    changed = sorted(
        (pad_name, expected[pad_name], actual[pad_name])
        for pad_name in set(expected) & set(actual)
        if expected[pad_name] != actual[pad_name]
    )
    if missing or extra or changed:
        raise SystemExit(
            "golden netlist mismatch: "
            f"missing={missing}, extra={extra}, changed={changed}"
        )
    return len(actual)


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify.py BOARD")
    board = pcbnew.LoadBoard(sys.argv[1])
    footprints = {item.GetReference(): item for item in board.GetFootprints()}
    if set(footprints) != EXPECTED_REFS:
        raise SystemExit(
            f"reference mismatch: missing={sorted(EXPECTED_REFS - set(footprints))}, "
            f"extra={sorted(set(footprints) - EXPECTED_REFS)}"
        )

    connected_pads = verify_golden_netlist(footprints)

    bounds = board.GetBoardEdgesBoundingBox()
    if not (abs(mm(bounds.GetWidth()) - 30.05) < 0.01 and abs(mm(bounds.GetHeight()) - 30.05) < 0.01):
        raise SystemExit(f"unexpected outline bbox: {mm(bounds.GetWidth()):.3f} x {mm(bounds.GetHeight()):.3f} mm")

    u1 = footprints["U1"]
    bad_u1_ground = [
        number for number in map(str, range(37, 54))
        if pad(u1, number).GetNetname() != "GND"
    ]
    if bad_u1_ground:
        raise SystemExit(f"U1 ground pads not connected to GND: {bad_u1_ground}")

    expected_pullups = {"R20": "IO6_SDA", "R21": "IO7_SCL", "R22": "IO10_ALRT"}
    for reference, signal in expected_pullups.items():
        footprint = footprints[reference]
        actual = (footprint.GetValue(), pad(footprint, "1").GetNetname(), pad(footprint, "2").GetNetname())
        expected = ("10kR 1%", signal, "+3V3")
        if actual != expected:
            raise SystemExit(f"{reference} mismatch: actual={actual}, expected={expected}")

    u3 = footprints["U3"]
    if u3.GetValue() != "ADS1220":
        raise SystemExit(f"U3 value mismatch: {u3.GetValue()}")
    if "TSSOP-16" not in u3.GetFPIDAsString():
        raise SystemExit(f"U3 footprint mismatch: {u3.GetFPIDAsString()}")

    u6 = footprints["U6"]
    if u6.GetValue() != "SY8088" or not u6.GetFPIDAsString().endswith(":SOT-23-5"):
        raise SystemExit(
            f"U6 identity mismatch: value={u6.GetValue()}, "
            f"footprint={u6.GetFPIDAsString()}"
        )
    for reference, (expected_layer, expected_angle, footprint_suffix, expected_pads) in COMPONENT_GEOMETRY.items():
        footprint = footprints[reference]
        if footprint.GetLayer() != expected_layer:
            raise SystemExit(
                f"{reference} side mismatch: {pcbnew.LayerName(footprint.GetLayer())}"
            )
        angle_error = (footprint.GetOrientationDegrees() - expected_angle + 180.0) % 360.0 - 180.0
        if abs(angle_error) > 0.01:
            raise SystemExit(
                f"{reference} orientation mismatch: "
                f"{footprint.GetOrientationDegrees():.2f} degrees"
            )
        if not footprint.GetFPIDAsString().endswith(footprint_suffix):
            raise SystemExit(
                f"{reference} footprint mismatch: {footprint.GetFPIDAsString()}"
            )

        actual_pads = {}
        for number in expected_pads:
            position = pad(footprint, number).GetFPRelativePosition()
            x, y = mm(position.x), mm(position.y)
            actual_pads[number] = (x, -y if expected_layer == pcbnew.B_Cu else y)
        bad_pads = {
            number: actual_pads[number]
            for number, expected_position in expected_pads.items()
            if math.dist(actual_pads[number], expected_position) > 0.001
        }
        if bad_pads:
            raise SystemExit(
                f"{reference} component-side pad geometry mismatch: {bad_pads}"
            )

    inner_ground_tracks = [
        item for item in board_tracks(board)
        if item.Type() != pcbnew.PCB_VIA_T and item.GetLayer() == pcbnew.In1_Cu
    ]
    if inner_ground_tracks:
        raise SystemExit(f"L2 must be signal-free; found {len(inner_ground_tracks)} tracks")

    ground_vias = sum(
        item.Type() == pcbnew.PCB_VIA_T and item.GetNetname() == "GND"
        for item in board_tracks(board)
    )
    if ground_vias < 12:
        raise SystemExit(f"expected at least 12 GND stitching vias, found {ground_vias}")

    paste_overlaps = via_in_paste(board)
    if paste_overlaps:
        raise SystemExit(f"via drill overlaps solder-paste aperture: {paste_overlaps}")

    limits = {
        # Correct pin 3 is on U6's far side; this route goes around the
        # package and its local GND fanout without changing layers.
        "Buck_Coil": (7.0, 0),
        "Net-(U6-FB)": (8.0, 0),
        "Net-(U3-AIN0)": (16.0, 0),
        "Net-(U3-AIN1)": (16.0, 0),
    }
    for net_name, (max_length, max_vias) in limits.items():
        length, vias, _ = net_metrics(board, net_name)
        if length > max_length or vias > max_vias:
            raise SystemExit(
                f"{net_name} exceeds limit: {length:.3f} mm/{vias} vias; "
                f"limit={max_length:.3f} mm/{max_vias} vias"
            )

    loadcell_pads = (
        pad(footprints["J12"], "1"),
        pad(footprints["J10"], "1"),
        pad(footprints["J9"], "1"),
        pad(footprints["J11"], "1"),
    )
    positions = [(mm(item.GetPosition().x), mm(item.GetPosition().y)) for item in loadcell_pads]
    if any(abs(y - 81.10) > 0.01 or x >= 140.0 for x, y in positions):
        raise SystemExit(f"load-cell pads are not grouped on the bottom analog edge: {positions}")

    battery_pads = (
        pad(footprints["J5"], "1"),
        pad(footprints["J7"], "1"),
        pad(footprints["J6"], "1"),
        pad(footprints["J8"], "1"),
    )
    battery_positions = [(mm(item.GetPosition().x), mm(item.GetPosition().y)) for item in battery_pads]
    if any(abs(x - 156.20) > 0.05 for x, _ in battery_positions):
        raise SystemExit(f"battery/switch pads are not on the right edge column: {battery_positions}")

    print(
        f"Crimpdeq verification passed: {len(footprints)} components, "
        f"{connected_pads} connected named pads, {ground_vias} GND vias"
    )
    for net_name in limits:
        length, vias, layers = net_metrics(board, net_name)
        print(f"  {net_name}: {length:.3f} mm, {vias} vias, {sorted(layers)}")


if __name__ == "__main__":
    main()
