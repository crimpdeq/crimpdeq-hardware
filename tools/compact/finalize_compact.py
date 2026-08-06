#!/usr/bin/env python3
"""Add compact-board planes, rule areas, and production labels."""

import sys

import pcbnew

from common import ensure_distinct_paths, validate_frozen_design


ANTENNA_KEEPOUT = (134.80, 52.40, 148.70, 53.40)
ANALOG_VIA_KEEPOUT = (128.00, 70.80, 137.40, 77.90)


def fm(value):
    return pcbnew.FromMM(value)


def add_zone(board, net, layer, name, priority):
    edges = board.GetBoardEdgesBoundingBox()
    zone = pcbnew.ZONE(board)
    zone.SetLayer(layer)
    zone.SetNet(net)
    zone.SetZoneName(name)
    zone.SetAssignedPriority(priority)
    zone.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
    zone.SetLocalClearance(fm(0.20))
    zone.SetMinThickness(fm(0.20))
    outline = zone.Outline()
    outline.NewOutline()
    for x, y in (
        (edges.GetX(), edges.GetY()),
        (edges.GetRight(), edges.GetY()),
        (edges.GetRight(), edges.GetBottom()),
        (edges.GetX(), edges.GetBottom()),
    ):
        outline.Append(x, y)
    board.Add(zone)


def add_rule_area(board, layers, name, box, block_fill, block_tracks, block_vias):
    x0, y0, x1, y1 = box
    zone = pcbnew.ZONE(board)
    zone.SetIsRuleArea(True)
    zone.SetDoNotAllowZoneFills(block_fill)
    zone.SetDoNotAllowTracks(block_tracks)
    zone.SetDoNotAllowVias(block_vias)
    zone.SetDoNotAllowPads(False)
    zone.SetDoNotAllowFootprints(False)
    layer_set = pcbnew.LSET()
    for layer in layers:
        layer_set.AddLayer(layer)
    zone.SetLayerSet(layer_set)
    zone.SetZoneName(name)
    outline = zone.Outline()
    outline.NewOutline()
    for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
        outline.Append(fm(x), fm(y))
    board.Add(zone)


def hide_silkscreen_fields(board):
    for footprint in board.GetFootprints():
        for field in footprint.GetFields():
            if field.GetLayer() in {pcbnew.F_SilkS, pcbnew.B_SilkS}:
                field.SetVisible(False)


def move_functional_labels(board):
    placements = {
        "A-": (129.00, 76.00, 0),
        "A+": (133.00, 75.70, 0),
        "B+": (149.20, 74.90, 0),
        "SW": (149.30, 70.70, 0),
        "E+": (147.60, 54.50, 0),
        "E-": (147.60, 57.00, 0),
    }
    for footprint in board.GetFootprints():
        if footprint.GetReference() not in {"J3", "J4"}:
            continue
        for drawing in footprint.GraphicalItems():
            if not isinstance(drawing, pcbnew.PCB_TEXT):
                continue
            text = drawing.GetText()
            if text not in placements:
                continue
            x, y, rotation = placements[text]
            drawing.SetPosition(pcbnew.VECTOR2I(fm(x), fm(y)))
            drawing.SetTextAngle(pcbnew.EDA_ANGLE(rotation, pcbnew.DEGREES_T))
            drawing.SetTextSize(pcbnew.VECTOR2I(fm(0.80), fm(0.80)))


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: finalize_compact.py ROUTED_BOARD OUTPUT_BOARD")
    ensure_distinct_paths(sys.argv[1], sys.argv[2])
    board = pcbnew.LoadBoard(sys.argv[1])
    validate_frozen_design(board, "finalize input")
    for zone in list(board.Zones()):
        board.RemoveNative(zone)

    all_copper = [pcbnew.F_Cu, pcbnew.In1_Cu, pcbnew.In2_Cu, pcbnew.B_Cu]
    add_rule_area(
        board, all_copper, "antenna_keepout", ANTENNA_KEEPOUT,
        block_fill=True, block_tracks=True, block_vias=True,
    )
    add_rule_area(
        board, all_copper, "hx711_analog_via_keepout", ANALOG_VIA_KEEPOUT,
        block_fill=False, block_tracks=False, block_vias=True,
    )
    add_zone(board, board.FindNet("GND"), pcbnew.In1_Cu, "L2_GND_plane", 1)
    add_zone(board, board.FindNet("+3V3"), pcbnew.In2_Cu, "L3_3V3_power", 1)
    add_zone(board, board.FindNet("GND"), pcbnew.B_Cu, "L4_GND_flood", 0)
    add_zone(board, board.FindNet("GND"), pcbnew.F_Cu, "L1_GND_flood", 0)
    hide_silkscreen_fields(board)
    move_functional_labels(board)
    validate_frozen_design(board, "finalized board")

    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    board.BuildConnectivity()
    pcbnew.SaveBoard(sys.argv[2], board)
    print(f"saved {sys.argv[2]} with {len(list(board.Zones()))} zones/rule areas")


if __name__ == "__main__":
    main()
