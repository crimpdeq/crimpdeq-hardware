# Crimpdeq JLCPCB DFM Status

The canonical design uses a 30 x 30 mm outline and the current cable-pad/USB placement.

Local checks completed:

- KiCad error-level DRC: 0 violations, 0 unconnected items.
- All cable pads have 1.50 mm copper with 0.80 mm drills and remain inside the board outline.
- Functional labels are on front silkscreen beside `E-`, `A-`, `A+`, `E+`, `SW`, and `B+`.
- Routing vias use 0.60 mm copper / 0.30 mm drills and are tented on both faces.
- USB shell slots retain the board-specific 0.15 mm NPTH clearance exception.

A fresh manufacturer web-DFM upload is still required before ordering. Record any accepted
manufacturer-specific advisories here rather than copying the v2-nano pair list.
