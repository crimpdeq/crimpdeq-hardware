# Crimpdeq PCB Agent Handoff

All complete PCB packages live under `pcb/designs/`. Shared resources remain in
`pcb/libraries/` and `pcb/datasheets/`.

Directory roles:

- `pcb/designs/crimpdeq-v2-nano/`: HX711 production reference (current design).
- `pcb/designs/crimpdeq-v2/`: original two-layer v2 source and frozen electrical reference.

A significant board change MUST create a new, complete folder under `pcb/designs/`; never
overwrite or remove an older design. Significant changes include outline, stackup, major
placement/routing, connector-edge, or other fabrication/fit changes.

## Current board (read first)

**`pcb/designs/crimpdeq-v2-nano/crimpdeq.kicad_pcb`
is the current canonical design.**

- 4 copper layers, `25.00 x 26.00 mm` outline (bbox `25.05 x 26.05 mm` incl. edge stroke).
- **Antenna (`U1` ESP32-C3-MINI-1) + LED (`D4` WS2812B) both on the BACK**; USB (`J2`) and
  HX711 (`U3`) on the FRONT. This meets the product goal: antenna + LED on the same side.
- Components: 48 total, 28 front / 20 back.
- The antenna body overhangs the top edge while its castellated pads remain supported.
- The USB-C housing overhangs the bottom edge by `1.00 mm`; all connector copper is in-board.
- Cable pads are edge-accessible and labelled `A-`, `A+`, `B+`, `SW`, `E+`, and `E-`.
- Electrically identical to the `crimpdeq-v2` release (197 pads, 0 changed nets). KiCad DRC:
  `0` violations, `0` unconnected.

Package files (all under the current design directory):

- Board / project / rules / schematic: `crimpdeq.{kicad_pcb,kicad_pro,kicad_dru,kicad_sch}`
- Gerber ZIP: `gerbers/crimpdeq-v2-nano.zip`
- JLC DFM mapping: `reports/crimpdeq-v2-nano_jlc_tht_to_smd.md` (DRC itself is checked by CI on
  every push/PR, not committed as a static report)
- Renders: `renders/crimpdeq-v2-nano_front.png` / `..._back.png`
- Assembly package: `assembly/`

Electrical reference (not the current fabrication target):

- `pcb/designs/crimpdeq-v2/crimpdeq.kicad_pcb`, original `23 x 63.8 mm` layout + schematic.
  Used only as the golden reference for netlist verification.

Stackup:

- `F.Cu` (L1): signal + short/critical/analog on top + top GND flood.
- `In1.Cu` (L2): **solid GND plane** (signal-free; unbroken under the antenna and HX711 analog inputs).
- `In2.Cu` (L3): `+3V3` power pour + low-speed signal hybrid.
- `B.Cu` (L4): non-critical / LED data / switching signals + secondary GND flood.
- Antenna copper keep-out on ALL 4 layers; via keep-out under the HX711 analog inputs keeps L2 solid there.

Placement: `U1`/ESP32 antenna at the top edge on the back; `D4`/LED on the back; `J2`/USB-C at
the bottom edge on the front; `U3`/HX711 and the analog cable pads remain away from the RF end.
All wired pads are on the bottom or right edge with adjacent functional labels.

Provenance: the current design was re-placed and re-routed from the original two-layer
`crimpdeq-v2` design into a 4-layer, `25 x 26 mm` layout while preserving the exact BOM and
connectivity. The general 4-layer reorg pipeline (place -> rip -> headless FreeRoute -> import
-> pour -> verify) lives in `tools/4layer/`; compact-specific placement and DFM-finishing
scripts live in `tools/compact/`.

## Session Log — 2026-07-16

- Added `crimpdeq-v2-nano` as a new design under `pcb/designs/`. Nominal board
  area is `650.00 mm2`, about 56% smaller than the `crimpdeq-v2` reference (`1467.40 mm2`).
- Kept U1 and D4 on the back, J2 and U3 on the front, and the exact 48-component / 197-pad
  electrical design. Moved every cable pad to an edge and placed functional silk beside it.
- Allowed the ESP32 antenna body to extend beyond the top edge, preserving the all-layer copper
  keepout. Positioned J2 for a 1.00 mm body overhang with every USB pad and shell mount in-board.
- Moved the original v2 reference into `pcb/designs/crimpdeq-v2/`. Each design now owns its
  source and production package.
- Removed the former `latest/` folder. `pcb/designs/README.md` defines the versioning policy.
- Updated local schematic references, automation, CI paths, and assembly generators for the new
  hierarchy. Verified the compact board with KiCad DRC and connectivity comparison.
- Reviewed the compact Gerbers in JLCPCB's web DFM checker. Corrected all functional-label
  silk-to-pad/hole findings, moved R13 0.80 mm to clear two avoidable `E-` findings, and added
  `tools/compact/check_dfm.py`. The remaining `tht to smd` notices are accepted conservative
  advisories for the 1.50 mm cable PTH pads; all real clearances pass the board rules.
- Eliminated every remaining red `tht to smd` entry. Locally moved R1/C18, R7/R8/C12, and
  D2/Q2; shifted J2 0.25 mm left without changing its 1.00 mm overhang or USB data lengths;
  and moved J4.4 down 0.10 mm. JLCDFM now reports warnings only. The pair mapping and
  before/after gaps are in the design's `reports/*_jlc_tht_to_smd.md`; `check_dfm.py` enforces
  a nominal 2.03 mm KiCad-shape boundary for the mapped pairs.

## Session Log — 2026-07-14

- Reorganized the board so the antenna and LED sit on the same side (both back), USB on the
  front, without growing the outline. 2-layer was infeasible at the existing density, so moved
  to 4 layers via a scripted place -> rip -> **headless** FreeRoute -> import -> pour -> verify
  pipeline (`tools/4layer/`). Added the solid L2 GND plane, L3 +3V3 pour, L1/L4 GND floods,
  antenna keep-out (all layers) and HX711 analog via keep-out.
- Verified identical connectivity to the `crimpdeq-v2` reference; DRC clean.
- Generated a complete JLCPCB **assembly package**: `crimpdeq_4layer_bom.csv` (46/48 LCSC codes
  filled; `J3`/`J4` are bare `External_Cable_Pads` = Do Not Place), `crimpdeq_4layer_cpl.csv`
  (placement, absolute origin matching the gerbers), and `_gen_bom.py`/`_gen_cpl.py`.
  **Gotcha:** the upstream schematic's resistor `LCSC` fields are corrupt (placeholder reuse —
  `C25741`=100k was reused on R5/R6/R7/R8; `C25744` shared between 10k and 0R). Corrected with
  verified Uni-Royal 0402 parts; details in that design's `assembly/README.md`. Removed `*.csv`
  from `.gitignore` so BOM/CPL are tracked.

**Key decisions (do not re-litigate without asking):**

- Keep the ESP32-C3-MINI-1 **module** (integrated antenna). No external RF feedline, so
  50-ohm-CPWG-feedline rules are N/A; RF reduces to antenna-at-edge + all-layer keep-out.
- **Preserve the exact netlist** — do not add/remove/re-value components (e.g. no added LED
  decoupling cap), even where good practice would suggest one. See "Design Invariants".

**Open items / possible next steps:**

- LED data (`Net-(D4-DIN)`) runs mostly on `In2` rather than `B.Cu` (the module blocks the
  back-top on `B.Cu`); it is shielded between GND references and clear of the analog area, but
  moving it to `B.Cu` where possible is a GUI-finish nicety.
- HX711 input pair (`Net-(U3-INA+)` / `Net-(U3-INA-)`) is over solid GND but not length-matched
  (non-critical for a load cell).
- Physical prototype validation is still required for antenna performance and connector fit.

**Tooling note:** the FreeRouting 2.2.4 jar + a JDK live in `/tmp` (NOT committed). Re-download
the jar as shown in `tools/4layer/README.md` if `/tmp` was cleared.

**Verification method (reuse for any future design):** electrical equivalence is confirmed
against the local `pcb/designs/crimpdeq-v2/crimpdeq.kicad_pcb` using
`tools/4layer/compare_connectivity.py` — checks identical pad set, net-name match, and identical
net partition (robust to net renaming).

## HX711 Electrical Preservation

The frozen invariants below apply to the HX711 production reference and its layout derivatives.
Keep the exact same schematic connectivity unless explicitly requested.

Verification of the current board against the original PCB:

- Original pads: `197` / current pads: `197`
- Missing pads: `0`; extra pads: `0`; changed pad nets: `0`
- KiCad DRC error-level violations: `0`; unconnected pads/items: `0`

## HX711 Design Invariants — Components And Routing (DO NOT MODIFY)

This is the frozen definition of the design. **Any layout change (reorg, reroute, layer
change, new variant) MUST preserve everything in this section.** Changes may move, rotate,
flip, and reroute parts; they may NOT add/remove/re-value components or alter which pads are
electrically joined. This matches the `crimpdeq-v2` reference design.

Enforce after every change:

- `tools/4layer/verify.py <board>` -> expect `197/197` pads, `0` changed nets vs
  `pcb/designs/crimpdeq-v2/crimpdeq.kicad_pcb`.
- `tools/4layer/compare_connectivity.py <crimpdeq-v2 board> <board>` -> partition IDENTICAL.
- `kicad-cli pcb drc --refill-zones --severity-error ...` -> `0` violations, `0` unconnected.

### Component list (BOM) — INVARIANT: do not add, remove, or re-value

| Ref | Value | Footprint | Function |
|-----|-------|-----------|----------|
| C1 | 1uF 16V | C_0402_1005Metric | Capacitor 1uF 16V |
| C2 | 100nF 10V | C_0402_1005Metric | Capacitor 100nF 10V |
| C3 | 1uF 16V | C_0402_1005Metric | Capacitor 1uF 16V |
| C4 | 10nF 10V | C_0402_1005Metric | Capacitor 10nF 10V |
| C5 | 4.7uF 16V | C_0603_1608Metric | Capacitor 4.7uF 16V |
| C6 | 4.7uF 16V | C_0603_1608Metric | Capacitor 4.7uF 16V |
| C9 | 10uF | C_0603_1608Metric | Capacitor 10uF |
| C10 | 10uF | C_0603_1608Metric | Capacitor 10uF |
| C11 | 0.1uF | C_0603_1608Metric | Capacitor 0.1uF |
| C12 | 0.1uF | C_0603_1608Metric | Capacitor 0.1uF |
| C15 | 10uF 16V | C_0805_2012Metric | Capacitor 10uF 16V |
| C16 | 22pF 50V | C_0603_1608Metric | Capacitor 22pF 50V |
| C17 | 10uF 16V | C_0805_2012Metric | Capacitor 10uF 16V |
| C18 | 100nF 10V | C_0402_1005Metric | Capacitor 100nF 10V |
| D1 | LED | LED_0603_1608Metric | Charge-status LED |
| D2 | B5819W | D_SOD-123 | B5819W Schottky diode (power path) |
| D3 | LESD8D3.3CAT5G | D_SOD-882 | LESD8D3.3CAT5G TVS/ESD (USB/load-cell protection) |
| D4 | WS2812B | LED_WS2812B_PLCC4_5.0x5.0mm_P3.2mm | WS2812B addressable RGB LED (user indicator) |
| D7 | LESD5D5.0CT1G | D_SOD-523 | LESD5D5.0CT1G TVS/ESD |
| D8 | B5819W | D_SOD-123 | B5819W Schottky diode (power path) |
| D9 | LESD5D5.0CT1G | D_SOD-523 | LESD5D5.0CT1G TVS/ESD |
| D10 | LESD5D5.0CT1G | D_SOD-523 | LESD5D5.0CT1G TVS/ESD |
| J2 | USB4105-GF-A | GCT_USB4105-GF-A | USB4105-GF-A USB-C receptacle (power + data) |
| J3 | Loadcell_Pads | External_Cable_Pads_Left | Load-cell pad header |
| J4 | Power_Sense_Pads | External_Cable_Pads_Right | Power/sense pad header (battery / switch) |
| L1 | SPH4018H2R2MT (2.2uH 2.2A) | L_Bourns-SRN4018 | SPH4018 2.2uH power inductor (buck) |
| Q1 | SS8550 | SOT-23 | SS8550 PNP BJT |
| Q2 | DMG3415U | SOT-23 | DMG3415U P-channel MOSFET (load switch) |
| R1 | 10kR 1% | R_0402_1005Metric | Resistor 10kR 1% |
| R2 | 10kR 1% | R_0402_1005Metric | Resistor 10kR 1% |
| R3 | 1kR 1% | R_0402_1005Metric | Resistor 1kR 1% |
| R5 | 12kR 1% | R_0402_1005Metric | Resistor 12kR 1% |
| R6 | 8k2R 1% | R_0402_1005Metric | Resistor 8k2R 1% |
| R7 | 100R 1% | R_0402_1005Metric | Resistor 100R 1% (HX711 INA+ filter) |
| R8 | 100R 1% | R_0402_1005Metric | Resistor 100R 1% (HX711 INA- filter) |
| R9 | 100kR 1% | R_0402_1005Metric | Resistor 100kR 1% |
| R13 | 0R 1% | R_0402_1005Metric | Resistor 0R (LED data series) |
| R14 | 10kR 1% | R_0402_1005Metric | Resistor 10kR 1% |
| R15 | 100kR 1% | R_0402_1005Metric | Resistor 100kR 1% |
| R16 | 22k1R 1% | R_0402_1005Metric | Resistor 22k1R 1% |
| R17 | 0R 1% | R_0402_1005Metric | Resistor 0R (USB shell/GND) |
| R18 | 5k1R 1% | R_0402_1005Metric | Resistor 5k1R 1% (USB CC2) |
| R19 | 5k1R 1% | R_0402_1005Metric | Resistor 5k1R 1% (USB CC1) |
| U1 | ESP32-C3-MINI-1 | ESP32-C3-MINI-1 | ESP32-C3-MINI-1 module (MCU + Wi-Fi/BLE, integrated antenna) |
| U2 | MCP73831T-2ACI/OT | SOT-23-5 | MCP73831 Li-ion/LiPo battery charger |
| U3 | HX711 | SOP-16_3.9x9.9mm_P1.27mm | HX711 24-bit load-cell ADC (analog front end) |
| U5 | MAX17048G+T10 | TDFN-8-1EP_2x2mm_P0.5mm_EP0.8x1.2mm | MAX17048 battery fuel gauge (I2C) |
| U6 | SY8088 | SOT-23-5 | SY8088 step-down (buck) regulator -> +3V3 |

48 components total (197 named pads / 210 physical pads).

### Netlist (connectivity) — INVARIANT: 34 named nets

Each net lists the pads that MUST remain electrically joined. No pad may change nets.

| Net | Pads |
|-----|------|
| `+3V3` | C1.1, C2.1, C4.1, C9.1, C16.1, C17.1, D3.1, D4.1, L1.2, Q1.2, R1.1, R15.1, U1.3, U3.1, U3.15, U3.16 |
| `+BATT` | C6.1, C18.1, J4.3, U2.3, U5.2, U5.3 |
| `/Buck_Coil` | L1.1, U6.3 |
| `A+` | J4.2, R7.2 |
| `A-` | J4.1, R8.2 |
| `CHIP_PU` | C3.1, R1.2, U1.8 |
| `E+` | C10.1, J3.1, Q1.3, R5.1, U3.3 |
| `ENABLE` | R14.2, U6.1 |
| `GND` | C1.2, C2.2, C3.2, C4.2, C5.1, C6.2, C9.2, C10.2, C11.1, C15.2, C17.2, C18.2, D3.2, D4.3, D7.2, D9.2, D10.2, J2.A1_B12, J2.B1_A12, J3.2, R2.1, R6.2, R9.2, R16.2, R17.2, R18.2, R19.2, U1.1, U1.11, U1.14, U1.2, U1.36, U2.2, U3.10, U3.14, U3.5, U3.9, U5.1, U5.4, U5.6, U5.9, U6.2 |
| `IO10_ALRT` | U1.16, U5.5 |
| `IO2_LED` | R13.1, U1.5 |
| `IO4_DATA` | U1.18, U3.12 |
| `IO5_SCK` | U1.19, U3.11 |
| `IO6_SDA` | U1.20, U5.7 |
| `IO7_SCL` | U1.21, U5.8 |
| `Net-(D1-K)` | D1.1, R3.2 |
| `Net-(D4-DIN)` | D4.4, R13.2 |
| `Net-(D8-A)` | D8.2, D9.1, J2.A4_B9, J2.B4_A9 |
| `Net-(J2-CC1)` | J2.A5, R19.1 |
| `Net-(J2-CC2)` | J2.B5, R18.1 |
| `Net-(J2-SHELL_GND-PadS1)` | J2.S1, J2.S2, J2.S3, J2.S4, R17.1 |
| `Net-(Q1-B)` | Q1.1, U3.2 |
| `Net-(U2-PROG)` | R2.2, U2.5 |
| `Net-(U2-STAT)` | R3.1, U2.1 |
| `Net-(U3-INA+)` | C12.1, R7.1, U3.8 |
| `Net-(U3-INA-)` | C12.2, R8.1, U3.7 |
| `Net-(U3-VBG)` | C11.2, U3.6 |
| `Net-(U3-VFB)` | R5.2, R6.1, U3.4 |
| `Net-(U6-FB)` | C16.2, R15.2, R16.1, U6.5 |
| `SW_BATT` | J4.4, Q2.3 |
| `USB_D+` | D10.1, J2.A6, J2.B6, U1.27 |
| `USB_D-` | D7.1, J2.A7, J2.B7, U1.26 |
| `VBUS` | C5.2, D1.2, D2.2, D8.1, Q2.1, R9.1, U2.4 |
| `VSYS` | C15.1, D2.1, Q2.2, R14.1, U6.4 |

(Pads not listed above are intentionally no-connect / unconnected in the original design and
must stay unconnected: e.g. `D4.2` WS2812B DOUT, unused `U1` GPIO/NC pads, `U3.13` XO.)

### Routing rules — how components should be routed (preserve in all changes)

General
- Preserve the netlist and BOM above exactly. Do not change pad nets, add, or remove parts.
- Do not grow the current board outline (`25 x 26 mm`) without explicit request. Create a new
  design directory for any significant outline or layout change.

Stackup (4-layer)
- L1 `F.Cu`: components + short/critical + analog on top; top GND flood.
- L2 `In1.Cu`: **solid GND plane, no signal routing**; unbroken under the antenna and under the HX711 analog inputs.
- L3 `In2.Cu`: `+3V3` power pour + low-speed signal hybrid. There is a single 3V3 rail (HX711 AVDD shares `+3V3`), so there is **no** separate analog supply to split.
- L4 `B.Cu`: non-critical / LED data / switching signals + secondary GND flood.

RF / antenna (`U1`, ESP32-C3-MINI-1)
- It is a **module with an integrated antenna** — there is no external 50-ohm feedline to route.
- Keep the antenna at a board edge; keep a 100% copper keep-out under the antenna footprint on ALL layers.

HX711 analog (`U3`)
- Keep `U3` and the load-cell header (`J3`/`J4` A+/A-/E+) at the opposite end from the ESP32/RF section.
- Route `Net-(U3-INA+)` (U3.8) and `Net-(U3-INA-)` (U3.7) as a tight, symmetric, short pair on one signal layer over solid GND; keep the input filter (`R7`,`R8`,`C11`,`C12`) close to U3.
- Keep the L2 GND reference under the analog inputs solid — no vias or plane splits there.
- Do not run digital nets (LED data, `IO4_DATA`/`IO5_SCK`, USB) under the analog input region.

LED (`D4`, WS2812B)
- Route the data chain `IO2_LED` -> `R13` -> `Net-(D4-DIN)` -> `D4` on a signal layer, away from the HX711 analog inputs. `D4.2` (DOUT) stays unconnected.
- There is no LED-local decoupling cap and none may be added (netlist frozen); rely on the nearby `+3V3` bulk caps.

Power / vias
- Keep power nets (`+3V3`, `VBUS`, `+BATT`, `VSYS`, buck `/Buck_Coil`) low-impedance: wide traces (>= ~0.4 mm) or copper pours; use the L3 `+3V3` pour.
- Keep the SY8088 buck loop (`U6`, `L1`, `C15`, `C17`, `/Buck_Coil`, `Net-(U6-FB)`) compact.
- Drop GND vias to the L2 plane at IC / decoupling-cap GND pads (except inside the HX711 analog keep-out). Minimize vias on the analog input nets.

USB / protection (`J2`)
- Route `USB_D+`/`USB_D-` as a matched pair; keep the ESD/TVS parts (`D7`,`D9`,`D10`,`D3`) near the connector / entry point. Keep CC resistors (`R18`,`R19`) at the connector.

## DFM Notes (baked into the current design)

These fixes/observations came from the manufacturer web checker on the 2-layer predecessor's
gerbers and are carried into the current board via the `.kicad_dru` and footprint geometry.
Re-run the manufacturer upload for the 4-layer gerbers before production.

DFM fixes present in the design:

- USB-C shell slot drill widened `0.60 mm` -> `0.65 mm` (silences the slot-width danger).
- Production silkscreen reduced to functional labels only: `A-`, `A+`, `B+`, `SW`, `E+`, `E-`.
  Labels are 0.80 mm high and have at least 0.20 mm clearance from top copper and drilled holes.
- Moved bottom-side R13 0.80 mm away from `E-`, eliminating both of that cable pad's bottom-layer
  `tht to smd` danger entries without changing connectivity.
- `J4` pads 3/4 (`+BATT`/`SW_BATT`) shifted for clearance from bottom-side `Q2`.
- `VSYS` dogleg near `Q2` pad 2 replaced with a direct segment to avoid a soldermask opening over a trace.
- `J2` pad-to-NPTH hole clearance relaxed to `0.15 mm` via a scoped rule in the `.kicad_dru`
  (USB-C manufacturer footprint geometry). This rule ships next to each board file.

Observed website DFM tolerances (Danger/Warning/Good):

- Annular ring: `0.15 mm` vias shown as orange warning; treat `>0.15 mm` as green target. Current vias are `0.60 mm` dia / `0.30 mm` drill = `0.15 mm` ring (kept — larger vias caused KiCad clearance errors).
- `tht to smd` / via-to-pad: red `<2.03 mm`, orange `2.03-3.05 mm`, green `>=3.05 mm` (very
  conservative for this compact board). The website reports the six 1.50 mm cable PTH pads as
  `r59.0551` "vias". The accepted local finish clears every red entry without moving the cable
  pads off their edges or degrading USB/analog routing. Remaining entries are warnings at or
  above 2.03 mm. `check_dfm.py` enforces this boundary for the exact mapped pairs, including
  USB shell slot J2.S4 on both outer layers.
- Soldermask opening exposing trace: `0.05 mm` red, `0.20 mm` green.
- Silkscreen to pad/hole: red `<0.13 mm`, orange `0.13-0.18 mm`, green `>=0.18 mm`. Current
  functional text is 0.80 mm high and has at least 0.20 mm designed clearance.
- Slot width: red `<0.61 mm`, orange `0.61-0.81 mm`, green `>=0.81 mm`.

## Verification Commands

Run from the repository root.

```sh
DESIGN=pcb/designs/crimpdeq-v2-nano
BOARD="$DESIGN/crimpdeq.kicad_pcb"

# DRC (expect 0 violations / 0 unconnected); CI runs this on every push/PR,
# no static report is committed to the design directory
kicad-cli pcb drc --refill-zones --severity-error --format report \
  --output /tmp/crimpdeq-v2-nano_drc.txt "$BOARD"

# Netlist preservation vs the original (expect 197/197, 0 changed)
PY=python3  # KiCad-bundled interpreter; see assembly/README.md for OS-specific paths
$PY tools/4layer/verify.py "$BOARD"

# Full connectivity equivalence vs the crimpdeq-v2 reference
$PY tools/4layer/compare_connectivity.py \
  pcb/designs/crimpdeq-v2/crimpdeq.kicad_pcb "$BOARD"

# Compact DFM geometry (labels, cable PTH clearances, and via tenting)
$PY tools/compact/check_dfm.py "$BOARD"
```

## Local Tooling

Use the installed local tools instead of guessing alternate PCB/CAD utilities.

### KiCad

- KiCad CLI in PATH as `kicad-cli` (observed version `10.0.4`).
- KiCad bundled Python (has `pcbnew`, incl. `ExportSpecctraDSN` / `ImportSpecctraSES`); path
  varies by OS/install, e.g. macOS
  `/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3`,
  Windows `C:\Program Files\KiCad\<version>\bin\python.exe`.

```sh
# open the board in the GUI
open -a KiCad \
  pcb/designs/crimpdeq-v2-nano/crimpdeq.kicad_pro
```

Use KiCad Python for repeatable geometry checks (board-outline size, footprint side counts,
pad/net comparisons, scripted pad/track edits). After any scripted edit, rerun DRC and compare
pad nets against `pcb/designs/crimpdeq-v2/crimpdeq.kicad_pcb`.

Export production gerbers + drill for the 4-layer board (note the inner layers):

```sh
DESIGN=pcb/designs/crimpdeq-v2-nano
PROJECT=crimpdeq
PACKAGE=crimpdeq-v2-nano
BOARD="$DESIGN/$PROJECT.kicad_pcb"
OUT=/tmp/$PACKAGE-gerbers
mkdir -p "$OUT"
kicad-cli pcb export gerbers --output "$OUT" \
  --layers F.Cu,In1.Cu,In2.Cu,B.Cu,F.Paste,B.Paste,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,Edge.Cuts \
  --subtract-soldermask --precision 6 "$BOARD"
kicad-cli pcb export drill --output "$OUT" --format excellon --drill-origin absolute \
  --excellon-units mm --excellon-zeros-format decimal --excellon-separate-th \
  --generate-map --map-format gerberx2 --generate-report --report-path "$OUT/drill_report.txt" "$BOARD"
(cd "$OUT" && zip -q -r "$OLDPWD/$DESIGN/gerbers/$PACKAGE.zip" .)
```

### FreeRouting

- No FreeRouting app or jar is kept in this repository. Do not commit FreeRouting binaries or
  large tool downloads — keep them outside the repo (e.g. `/tmp`).
- Use FreeRouting only as a routing assist. It must not change the board outline, footprint
  placement, pad identities, or net assignments.

**IMPORTANT — always run FreeRouting HEADLESS:**

```sh
JAVA=/opt/homebrew/opt/openjdk@26/bin/java   # any JDK 21+ works
FR=/tmp/freerouting-2.2.4.jar                # download outside the repo
"$JAVA" -Djava.awt.headless=true -jar "$FR" -de input.dsn -do output.ses -mp 100
```

- The `-Djava.awt.headless=true` flag is **required**. Without it FreeRouting v2.x opens a GUI
  window and **blocks/hangs on an email/profile dialog** (looks like the CLI is stuck). Headless
  forces pure CLI and prints `session completed ... (N unrouted)`.
- CLI mode needs BOTH `-de` (input `.dsn`) and `-do` (output `.ses`). `--help` is not valid.
- It typically leaves a few nets unrouted on this dense board; more `-mp` passes help but it can
  oscillate on the last 1-2 nets. Finish stragglers by hand, or let the GND/power pours absorb
  the remaining GND/power connections.
- To reserve an inner layer as a plane, edit its `(type signal)` -> `(type power)` in the `.dsn`
  before routing. Add antenna / analog via keepouts by injecting `(keepout ...)` /
  `(via_keepout ...)` polygons into the `.dsn` (coords are in um, Y negative).

The 4-layer reorg pipeline lives in `tools/4layer/`; compact-board placement and finishing
scripts live in `tools/compact/`. Both use headless FreeRouting for the routing step.
`kicad-cli` cannot export/import Specctra, but the bundled `pcbnew` Python can, so the whole
loop is scriptable with no GUI.

## Git Workflow

- This folder is a local git repository. Keep useful repo updates committed.
- When updating tracked files or adding a new canonical PCB/Gerber package, create a git commit
  before handing work back. Use focused commits with clear messages.
- Track one Gerber **.zip** in each design's `gerbers/` directory, not loose Gerber files.
  `.kicad_prl` is gitignored; `.kicad_pro`, `.kicad_sch`, and `.kicad_dru` are tracked.
- Do not commit scratch experiments or tool downloads.
- NOTE: this repo may be worked on by multiple agents concurrently. Re-check `git status` /
  `git log` before large edits, and leave unrelated untracked files alone unless asked.
