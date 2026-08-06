# 4-Layer Reorg Tooling

Scripts used to move the `crimpdeq-v2` electrical baseline (antenna + LED on the back, USB on
the front) from its original 2-layer stackup to 4 layers, preserving the exact BOM and
connectivity. `crimpdeq-v2-nano` (`pcb/designs/crimpdeq-v2-nano/`) is built on top of this
4-layer reorg; the compact-specific placement/finishing scripts are in `../compact/`.

They are a scripted place -> rip -> autoroute -> import -> pour -> verify pipeline, kept as a
record of the process and reusable for future re-layouts of the same electrical baseline.

## Prerequisites

- KiCad Python (has `pcbnew`, incl. `ExportSpecctraDSN` / `ImportSpecctraSES`); see
  `../compact/README.md` for OS-specific interpreter paths.
- A JDK 21+ for FreeRouting: `/opt/homebrew/opt/openjdk@26/bin/java` (macOS example; any JDK
  21+ on your platform works)
- FreeRouting jar (download outside the repo; do NOT commit it):
  `curl -L -o /tmp/freerouting-2.2.4.jar https://github.com/freerouting/freerouting/releases/download/v2.2.4/freerouting-2.2.4.jar`
- A scratch dir: `mkdir -p /tmp/pcbwork`

Run everything from the repo root.

## Files

- `moves_B.json` — the exact footprint moves (ref, target layer, x, y, rot) that flip
  U1/ESP32 + place D4/LED on the back and relocate the buck cluster to the front.
  U1 uses `rot:180` after a left-right flip so the antenna faces the top board edge.
- `place_4l.py <in.pcb> <moves.json> <out_noroute.pcb> <out.dsn> [clearance_mm]` —
  loads the baseline, sets 4 copper layers, applies the moves, checks footprint overlaps,
  full-rips tracks, saves the unrouted board, exports the DSN.
- `prep_dsn_B.sh` — runs `place_4l.py` then reserves `In1.Cu` as a plane
  (`(type signal)` -> `(type power)`) and injects the antenna keepout (all layers) +
  a tight via-keepout under the HX711 INA+/INA- inputs into the DSN.
- `import_ses.py <noroute.pcb> <in.ses> <out.pcb>` — imports the routed SES.
- `add_planes.py <routed.pcb> <out.pcb>` — adds the antenna rule-area keepout and the
  copper pours: L2 (In1) solid GND, L3 (In2) +3V3, L4 (B) + L1 (F) GND floods
  (solid pad connection), then fills zones.
- `verify.py <board.pcb>` — pad/net comparison vs
  `pcb/designs/crimpdeq-v2/crimpdeq.kicad_pcb`
  (expects 197/197 pads, 0 changed nets).
- `compare_connectivity.py <A.pcb> <B.pcb> [labelA labelB]` — robust electrical
  equivalence: same pad set, net-name match, and identical net partition (ignores
  net renaming). Use vs the upstream `crimpdeq/crimpdeq-pcb` `v2.0.0` board.

## Pipeline

```sh
PY=python3  # KiCad-bundled interpreter; see ../compact/README.md for OS-specific paths
JAVA=/opt/homebrew/opt/openjdk@26/bin/java
FR=/tmp/freerouting-2.2.4.jar
mkdir -p /tmp/pcbwork
cp pcb/designs/crimpdeq-v2/crimpdeq.kicad_pcb /tmp/v8.kicad_pcb

# 1. place + reserve In1 + inject keepouts, export DSN
bash tools/4layer/prep_dsn_B.sh /tmp/v8.kicad_pcb

# 2. autoroute  (HEADLESS is required, else FreeRouting hangs on a GUI email dialog)
"$JAVA" -Djava.awt.headless=true -jar "$FR" \
  -de /tmp/pcbwork/optB4.dsn -do /tmp/pcbwork/optB4.ses -mp 100

# 3. import routed session
$PY tools/4layer/import_ses.py /tmp/pcbwork/optB4_noroute.kicad_pcb \
  /tmp/pcbwork/optB4.ses /tmp/pcbwork/optB4_routed.kicad_pcb

# 4. add GND/power planes + antenna keepout, fill zones
$PY tools/4layer/add_planes.py /tmp/pcbwork/optB4_routed.kicad_pcb \
  /tmp/pcbwork/optB4_planes.kicad_pcb
cp pcb/designs/crimpdeq-v2-nano/crimpdeq.kicad_dru \
  /tmp/pcbwork/optB4_planes.kicad_dru   # J2 pad-to-NPTH hole-clearance exception

# 5. verify
kicad-cli pcb drc --refill-zones --severity-error --format report \
  --output /tmp/pcbwork/drc.txt /tmp/pcbwork/optB4_planes.kicad_pcb
$PY tools/4layer/verify.py /tmp/pcbwork/optB4_planes.kicad_pcb
$PY tools/4layer/compare_connectivity.py \
  pcb/designs/crimpdeq-v2/crimpdeq.kicad_pcb \
  /tmp/pcbwork/optB4_planes.kicad_pcb upstream_v2 new_4L
```

Notes:
- FreeRouting leaves ~1 net unrouted from scratch on this board; the solid GND pour in
  step 4 absorbs the remaining GND connection, giving 0 unconnected after pours.
- `prep_dsn_B.sh` and the pipeline use `/tmp/pcbwork` scratch paths and the FreeRouting
  jar in `/tmp` — adjust if your paths differ.
