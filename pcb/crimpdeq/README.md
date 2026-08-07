# Crimpdeq — 30 x 30 mm Four-Layer Design

This is the repository's single canonical PCB design and current production candidate. It
includes corrected ESP32 module grounding, improved power/analog placement, and sufficient
routing and return-path clearance.

- Board/project/rules/schematic: `crimpdeq.{kicad_pcb,kicad_pro,kicad_dru,kicad_sch}`
- Outline: 30.00 x 30.00 mm (30.05 x 30.05 mm including edge stroke)
- Components: 51 total, 29 front / 22 back
- U1 antenna and D4 LED: back; J2 USB-C and U3 HX711: front
- U1 pins 37–53, including EPAD 49, are connected to GND as required by Espressif.
- R20/R21/R22 provide 10 kΩ pull-ups for SDA, SCL, and the MAX17048 alert output.
- The buck input, switch, output, and feedback components form a compact front-side cluster.
  The switch node is 1.83 mm and feedback is 4.91 mm with no feedback vias.
- Twelve dedicated GND stitching vias tie the outer floods to the solid L2 plane around the
  ESP32, buck, charger, ADC, USB/power, and fuel-gauge sections.
- C9, C11, C15, C17, C18, C5, and C6 were moved close to the IC pins they bypass.
- All four load-cell pads (`E-`, `A-`, `A+`, `E+`) are together on the bottom edge near U3 and
  away from the antenna. `B+` and `SW` are on the right edge.
- The ESP32 antenna body overhangs the top edge; its all-layer copper keepout is retained.
- The USB-C housing overhangs the bottom edge by 1.00 mm; connector copper remains in-board.
- L2 is a signal-free GND plane. L3 carries the 3V3 pour and low-speed signals.
- 203 named pads / 216 physical pads; 48 routing vias, including 12 GND stitching vias.
- KiCad error-level DRC: zero violations and zero unconnected items.
- Schematic ERC and PCB/schematic parity: zero errors.

Production files:

- Gerbers: `gerbers/crimpdeq.zip`
- Assembly package: `assembly/`
- Front/back renders: `renders/`

Manufacturer DFM review and physical validation of power integrity, USB, HX711 noise, antenna
performance, and connector fit remain required before production.
