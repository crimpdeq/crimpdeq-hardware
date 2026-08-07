# Crimpdeq PCB Agent Handoff

The single canonical KiCad project lives at `pcb/crimpdeq/`. Shared footprints are under
`libraries/` and datasheets are under `pcb/datasheets/`.

Do not create versioned design directories. Update the canonical project only when the user
explicitly requests a design change, and use Konnect MCP tools for all KiCad source changes.

## Current board

- Project: `pcb/crimpdeq/crimpdeq.kicad_pro`
- Four copper layers; 30.00 x 30.00 mm nominal outline.
- 51 components: 29 front / 22 back; 203 named / 216 physical pads.
- U1 antenna and D4 LED are on the back; J2 USB-C and U3 HX711 are on the front.
- U1 ground pins 37–53 are connected to GND.
- R20/R21/R22 are 10 kΩ pull-ups for SDA, SCL, and MAX17048 ALERT.
- L2 is a signal-free solid GND plane. L3 carries the 3V3 pour and low-speed signals.
- Twelve dedicated GND stitching vias connect the outer floods to L2.
- The buck switch node is 1.83 mm and feedback route is 4.91 mm with no feedback vias.
- HX711 VBG is 2.32 mm with no vias.
- Load-cell pads are grouped on the bottom edge near U3; battery/switch pads are on the right.
- The ESP32 antenna and USB body retain their intentional board-edge overhangs.

## Package contents

- KiCad source and rules: `pcb/crimpdeq/crimpdeq.{kicad_pcb,kicad_pro,kicad_dru,kicad_sch}`
- Gerber ZIP: `pcb/crimpdeq/gerbers/crimpdeq.zip`
- Assembly BOM/CPL: `pcb/crimpdeq/assembly/crimpdeq_{bom,cpl}.csv`
- Renders: `pcb/crimpdeq/renders/crimpdeq_{front,back}.png`
- DFM report: `pcb/crimpdeq/reports/crimpdeq_jlc_tht_to_smd.md`
- Invariant checker: `tools/crimpdeq/verify.py`

## Design constraints

- Do not introduce electrical changes without an explicit request.
- Keep the ESP32-C3-MINI-1 module antenna at the board edge with an all-layer copper keepout.
- Keep L2 free of signal routing and unbroken under the antenna and HX711 analog inputs.
- Keep the HX711 input pair short, symmetric, on one signal layer, and over solid GND.
- Keep digital nets away from the HX711 analog input region.
- Keep power paths low impedance and the SY8088 buck loop compact.
- Route USB D+/D- as a matched pair and keep protection/CC parts near J2.
- Refill zones after PCB changes.

## Verification

Run from the repository root:

```sh
DESIGN=pcb/crimpdeq
BOARD="$DESIGN/crimpdeq.kicad_pcb"
PY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3

kicad-cli sch erc --severity-error --output /tmp/crimpdeq_erc.txt \
  "$DESIGN/crimpdeq.kicad_sch"
kicad-cli pcb drc --refill-zones --severity-error --schematic-parity \
  --output /tmp/crimpdeq_drc.txt "$BOARD"
"$PY" tools/crimpdeq/verify.py "$BOARD"
"$PY" "$DESIGN/assembly/_gen_bom.py"
"$PY" "$DESIGN/assembly/_gen_cpl.py"
```

Use `kicad-cli` for exports and checks. Use the bundled KiCad Python only for the existing
verification and assembly scripts; do not directly edit KiCad source files with text tools.

## Manufacturing notes

- Track only `pcb/crimpdeq/gerbers/crimpdeq.zip`, not loose Gerber files.
- J3/J4 are bare cable pads and must be marked Do Not Place.
- J2 includes plated through-hole shell tabs; assembly may require THT/manual soldering.
- Re-check package, polarity, side, rotation, and manufacturer DFM before ordering.
- Physical validation of power integrity, USB, HX711 noise, antenna performance, and connector
  fit is still required.
