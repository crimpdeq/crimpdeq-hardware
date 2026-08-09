# Crimpdeq PCB Agent Handoff

The single canonical KiCad project lives at `pcb/crimpdeq/`. Shared footprints are under
`libraries/` and datasheets are under `pcb/datasheets/`.

Do not create versioned design directories. Update the canonical project only when the user
explicitly requests a design change, and use Konnect MCP tools for all KiCad source changes.

## Session efficiency

Keep token use low on long PCB work:

- Split work across chats: schematic, then PCB/route, then verify/docs. Start a fresh session
  once ERC, DRC, and `verify.py` are green.
- Prefer Konnect MCP queries (components, nets, clearances, DRC summaries) over reading or
  dumping whole `.kicad_pcb` / `.kicad_sch` / netlist files into context.
- Consult the searchable Markdown datasheets in `pcb/datasheets/` for component-specific
  electrical, layout, package, and application guidance before relying on external sources.
- Do not `git diff` the board or schematic in-session; trust DRC, ERC, and `verify.py` output.
- Keep Freerouting/Java downloads in gitignored `.tools/` only; delete when done. Do not open
  autorouter logs in the IDE during the chat.
- Prefer Konnect `autoroute` when available; bound local autoroute retries (stop after a few
  failures and report blockers instead of looping on JRE/jar downloads).
- Plan first when the change is ambiguous; execute only the locked scope. Say so explicitly if
  the user already constrained the task.
- Update this handoff when board facts change so later sessions do not rediscover SPI maps,
  keepouts, or check commands.
- Do not leave one-shot helper scripts in `tools/`; only keep reusable checkers such as
  `verify.py`.

## Current board

- Project: `pcb/crimpdeq/crimpdeq.kicad_pro`
- Four copper layers; 30.00 x 30.00 mm nominal outline.
- 55 components: 36 front / 19 back.
- U1 antenna and D4 LED are on the back; J2 USB-C and U3 ADS1220 are on the front.
- U1 ground pins 37–53 are connected to GND.
- R20/R21/R22 are 10 kΩ pull-ups for SDA, SCL, and MAX17048 ALERT.
- L2 is a signal-free solid GND plane. L3 carries the 3V3 pour and low-speed signals.
- At least twelve dedicated GND stitching vias connect the outer floods to L2.
- The buck switch node is 1.83 mm and feedback is 4.91 mm with no feedback vias.
- U3 is ADS1220 (TSSOP-16) with ratiometric bridge excitation from +3V3 (E+/REFP0) and
  E-/REFN0 on GND. Local AVDD/DVDD decoupling is C11 + C19.
- SPI to U3: GPIO5 `IO5_SCK`→SCLK, GPIO4 `IO4_MOSI`→DIN, GPIO3 `IO3_CS`→~CS,
  GPIO1 `IO1_MISO`→DOUT/~DRDY. CLK is grounded; dedicated ~DRDY is unused.
- Load-cell pads are grouped on the bottom edge near U3; battery/switch pads are on the right.
- The ESP32 antenna and USB body retain their intentional board-edge overhangs.

## Package contents

- KiCad source and rules: `pcb/crimpdeq/crimpdeq.{kicad_pcb,kicad_pro,kicad_dru,kicad_sch}`
- Gerber ZIP: `pcb/crimpdeq/gerbers/crimpdeq.zip`
- Assembly BOM/CPL: `pcb/crimpdeq/assembly/crimpdeq_{bom,cpl}.csv`
- DFM report: `pcb/crimpdeq/reports/crimpdeq_jlc_tht_to_smd.md`
- Component datasheets: `pcb/datasheets/*.md`
- Invariant checker: `tools/crimpdeq/verify.py`

## Design constraints

- Do not introduce electrical changes without an explicit request.
- Keep the ESP32-C3-MINI-1 module antenna at the board edge with an all-layer copper keepout.
- Keep L2 free of signal routing and unbroken under the antenna and ADS1220 analog inputs.
- Keep the ADS1220 AIN0/AIN1 pair short, symmetric, on one signal layer, and over solid GND.
- Keep digital nets away from the ADS1220 analog input region.
- Keep power paths low impedance and the SY8088 buck loop compact.
- Route USB D+/D- as a matched pair and keep protection/CC parts near J2.
- Refill zones after PCB changes.

## Preview renders

Generate previews on demand with Konnect; do not commit generated render files:

- Schematic: call `konnect_get_schematic_view` with
  `schematic: pcb/crimpdeq/crimpdeq.kicad_sch`.
- PCB: call `konnect_get_board_2d_view` with `board: pcb/crimpdeq/crimpdeq.kicad_pcb` and the
  desired `width` and `height`. This produces a top-down 3D board render, not a layer plot.

If a preview must be saved as a file, keep it under `/tmp` and delete it after use.

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

## Autorouting (optional)

Do not commit JREs or Freerouting jars. Prefer Konnect `autoroute` / `check_freerouting` when
those tools are loaded. If you need a local run, download into gitignored `.tools/` and delete
when finished.

```sh
# From the repository root (Apple Silicon macOS example)
mkdir -p .tools && cd .tools

# Temurin 17 JRE (Freerouting 1.9)
curl -L --fail -o jre17.tar.gz \
  "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.14%2B7/OpenJDK17U-jre_aarch64_mac_hotspot_17.0.14_7.tar.gz"
mkdir -p jre17 && tar -xzf jre17.tar.gz -C jre17
JAVA="$(find jre17 -type f -name java | head -1)"

# Freerouting 1.9 (built for Java 17). Newer Freerouting 2.x needs Java 21+.
curl -L --fail -o freerouting.jar \
  "https://github.com/freerouting/freerouting/releases/download/v1.9.0/freerouting-1.9.0.jar"

# Export Specctra DSN from KiCad, route, then import the .ses session back.
# "$JAVA" -jar freerouting.jar -de /path/to/board.dsn -do /path/to/board.ses -mp 100
```

On Intel Mac use the Temurin `x64` JRE asset; on Linux/Windows use the matching platform
package or a system JDK 17+. After import: refill zones, run DRC + `tools/crimpdeq/verify.py`,
and keep L2 signal-free. Do not autoroute across the ADS1220 AIN region or the antenna keepout.

## Manufacturing notes

- Track only `pcb/crimpdeq/gerbers/crimpdeq.zip`, not loose Gerber files.
- J3/J4 are bare cable pads and must be marked Do Not Place.
- J2 includes plated through-hole shell tabs; assembly may require THT/manual soldering.
- Re-check package, polarity, side, rotation, and manufacturer DFM before ordering.
- Physical validation of power integrity, USB, ADS1220 noise, antenna performance, and connector
  fit is still required.
