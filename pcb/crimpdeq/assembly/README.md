# PCBWay Assembly Package

Assembly files for `../crimpdeq.kicad_pcb`.

- `crimpdeq_bom.csv`: PCBWay BOM (`Item`, `Quantity`, `Designator`, `Value`,
  `Footprint`, `MPN`, `Type`, `Notes`). `MPN` currently holds reviewed LCSC
  catalog numbers for sourcing.
- `crimpdeq_cpl.csv`: 47 fitted placements, 28 top / 19 bottom; J5–J12 are omitted as DNP.
- `J5`–`J12` are bare cable pads and must be marked Do Not Place.
- R20/R21/R22 are 10 kΩ 0402 pull-ups using the same validated part as R1/R2/R14.
- `_gen_cpl.py` converts KiCad positions to the PCBWay convention, applies
  the USB4105-GF-A body-centroid correction, and validates critical package rotations.

The schematic contains known LCSC placeholder reuse. `_gen_bom.py` maps those codes into
the PCBWay `MPN` column, applies the reviewed overrides, marks `J5`–`J12` as Do Not Place,
and validates the three hardware pull-ups. Confirm package, polarity, stock, side, and
rotation in the assembler preview. J2 has plated through-hole shell tabs; ensure the PCBA
order includes the required THT/manual soldering operation.

```sh
DESIGN=pcb/crimpdeq
# Use KiCad's bundled Python interpreter because the scripts import pcbnew.
PY=python3

$PY "$DESIGN/assembly/_gen_bom.py"
$PY "$DESIGN/assembly/_gen_cpl.py"
```
