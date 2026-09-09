# Crimpdeq Verification Tooling

`verify.py` compares every connected named pad against the corrected golden netlist, including
U1 ground pins 37–53 and R20/R21/R22. It also checks the component set, outline, L2 plane
usage, GND stitching, critical-route limits, and cable-pad placement. Digital tracks and vias
on every layer must stay outside the AIN and cable-signal copper envelopes, each guarded by
0.20 mm. This geometry check does not qualify ADC noise or prove ground-plane coverage.

Run it from the repository root with KiCad's bundled Python:

```sh
PY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
$PY tools/crimpdeq/verify.py pcb/crimpdeq/crimpdeq.kicad_pcb
```
