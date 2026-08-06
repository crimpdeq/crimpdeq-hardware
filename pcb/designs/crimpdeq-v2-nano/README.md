# Crimpdeq v2 Nano — 25 x 26 mm Four-Layer Design

Current compact production design.

- Board/project/rules: `crimpdeq.{kicad_pcb,kicad_pro,kicad_dru}`
- Local schematic copy: `crimpdeq.kicad_sch`
- Outline: 25.00 x 26.00 mm (25.05 x 26.05 mm including edge stroke)
- Components: 48 total, 28 front / 20 back
- U1 antenna and D4 LED: back; J2 USB-C and U3 HX711: front
- U1 antenna body overhangs the top edge while its castellated pads remain supported.
- J2 housing overhangs the bottom edge by 1.00 mm; all connector copper remains in-board.
- Cable pads are edge-accessible and labelled `A-`, `A+`, `B+`, `SW`, `E+`, and `E-`.
- Functional labels use 0.80 mm text and have at least 0.20 mm clearance from copper and holes.
- All 44 routing vias are tented on both faces. JLCPCB's `tht to smd` check identifies the
  six 1.50 mm cable PTH pads as vias; its 2.03/3.05 mm thresholds are conservative assembly
  heuristics rather than fabrication clearances.
- The mapped JLC danger pairs were cleared by local moves of R1, C18, R7, R8, C12, D2, Q2,
  J2, and J4.4. J2 moved 0.25 mm left but retains its 1.00 mm bottom-edge overhang; USB data
  route lengths are unchanged. The final JLCDFM upload reports warnings only and no dangers.
- `reports/crimpdeq-v2-nano_jlc_tht_to_smd.md` records every original danger pair and its
  before/after clearance. `tools/compact/check_dfm.py` enforces a nominal 2.03 mm KiCad-shape
  boundary for those mapped pairs; release Gerbers still require JLCDFM.
- R13 remains 0.80 mm away from its original position near `E-`; its closest final gaps are
  2.035 mm and 2.086 mm.
- Gerbers: `gerbers/crimpdeq-v2-nano.zip`
- Assembly package: `assembly/`

Validated against `../crimpdeq-v2/crimpdeq.kicad_pcb`: 197/197 named pads, zero changed
pad nets, zero error-level DRC violations, and zero unconnected items. DRC is checked on
every push/PR by CI (`.github/workflows/pcb_ci.yml`); no static report is committed here.

The manufacturer web DFM checker and physical prototype validation remain required before a
production order, particularly for antenna performance and USB connector mechanics.
