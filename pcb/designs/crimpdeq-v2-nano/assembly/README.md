# JLCPCB Assembly Package

Assembly files for `../crimpdeq.kicad_pcb`.

- `crimpdeq-v2-nano_bom.csv`: grouped BOM with LCSC part numbers.
- `crimpdeq-v2-nano_cpl.csv`: 48 placements, 28 top / 20 bottom.
- `J3` and `J4` are bare cable pads and must be marked Do Not Place.
- `_gen_cpl.py` converts KiCad positions to the JLC/Fabrication Toolkit convention and applies
  the USB4105-GF-A centroid correction.
- The tracked CPL reflects the accepted JLCDFM placement finish, including the 0.25 mm J2
  shift; local moves of R1, C18, R7, R8, C12, D2, and Q2; and the R1/C12 rotations. Moving
  only J4.4 down 0.10 mm changes the distributed J4 CPL centroid by 0.025 mm.

The schematic's resistor LCSC fields contain known placeholder reuse. `_gen_bom.py` applies
the reviewed overrides; confirm package, polarity, stock, and all rotations in JLC's preview.

```sh
DESIGN=pcb/designs/crimpdeq-v2-nano
# PY must be the KiCad-bundled Python interpreter (has the `pcbnew` module), e.g.:
#   macOS:   /Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
#   Linux:   /usr/lib/kicad/bin/python3 (or whatever `kicad-cli version --format json` reports)
#   Windows: "C:\Program Files\KiCad\<version>\bin\python.exe"
PY=python3

$PY "$DESIGN/assembly/_gen_bom.py"
$PY "$DESIGN/assembly/_gen_cpl.py"
```
