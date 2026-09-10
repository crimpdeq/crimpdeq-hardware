# Crimpdeq — 30 x 30 mm Four-Layer Design

This is the repository's single canonical PCB design and current production candidate. It
includes corrected ESP32 module grounding, an ADS1220 load-cell front-end, and compact
power/USB routing.

- Board/project/rules/schematic: `crimpdeq.{kicad_pcb,kicad_pro,kicad_dru,kicad_sch}`
- Outline: 30.00 x 30.00 mm (30.05 x 30.05 mm including edge stroke)
- Components: 55 total, 36 front / 19 back
- U1 antenna and D4 LED: back; J2 USB-C and U3 ADS1220: front
- U1 pins 37–53, including EPAD 49, are connected to GND as required by Espressif.
- R20/R21/R22 provide 10 kΩ pull-ups for SDA, SCL, and the MAX17048 alert output.
- U3 ADS1220 (TSSOP-16, LCSC C48263) uses ratiometric +3V3 excitation (E+/REFP0) with
  E-/REFN0 on GND. AVDD/DVDD decoupling is C11 + C19. R7/R8/C12 filter into AIN0/AIN1.
- SPI map: GPIO5 SCK, GPIO4 MOSI, GPIO3 CS, GPIO1 MISO (DOUT/~DRDY). CLK is grounded.
- The buck input, switch, output, and feedback components form a compact front-side cluster.
- Twelve dedicated GND stitching vias tie the outer floods to the solid L2 plane.
- All four load-cell pads (`E-`, `A-`, `A+`, `E+`) are together on the bottom edge near U3 and
  away from the antenna. `B+` and `SW` are on the right edge.
- The ESP32 antenna body overhangs the top edge; its all-layer copper keepout is retained.
- The USB-C housing overhangs the bottom edge by 1.00 mm; connector copper remains in-board.
- L2 is a signal-free GND plane. L3 carries the 3V3 pour and low-speed signals.
- KiCad error-level DRC: zero violations and zero unconnected items.
- Schematic ERC and PCB/schematic parity: zero errors.

Production files:

- Gerbers: `gerbers/crimpdeq.zip`
- Assembly package: `assembly/`

Manufacturer DFM review and physical validation of power integrity, USB, ADS1220 noise, antenna
performance, and connector fit remain required before production.
