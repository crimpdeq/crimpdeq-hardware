# Crimpdeq PCB Agent Handoff

This is a KiCad 10 hardware project. The single canonical KiCad project lives at
`pcb/crimpdeq/`. Shared footprints are under `libraries/` and datasheets are under
`pcb/datasheets/`.

Do not create versioned design directories. Update the canonical project only when the user
explicitly requests a design change.

## Konnect workflow

Use Konnect for every KiCad operation for which an appropriate Konnect tool exists. Never edit
`.kicad_pcb`, `.kicad_sch`, `.kicad_pro`, `.kicad_sym`, `.kicad_mod`, `fp-lib-table`, or
`sym-lib-table` files with text editors, shell scripts, or generic file-writing tools. When
Konnect requires a file-based operation, invoke the Konnect tool and let it perform the write. If
the required tool is unavailable, stop and report the limitation rather than editing the source
directly.

At the start of PCB work:

1. Call `list_toolboxes` to discover the tools available in the current Konnect installation.
2. Verify the KiCad installation and connection with `get_installation_info` and `open_project`.
   If either tool is unavailable, report that explicitly before continuing.
3. Load user and project configuration with `load_user_config` and `load_project_config`, then use
   `get_effective_config` for design decisions.
4. Confirm that the intended project and board are open. Do not assume the board currently open in
   KiCad belongs to this working tree.
5. Inspect the board before making changes.
6. Load only the toolsets required for the current task. Unload toolsets when switching to a
   different phase of work.

Before modifying the PCB:

- Inspect the current board and the affected components, pads, nets, rules, and geometry.
- Run placement and design-rule checks where applicable.
- Briefly explain the intended changes before applying them.
- Preserve unrelated local changes and existing design intent.

During layout:

- Prefer live KiCad IPC operations.
- Preserve locked items unless the user explicitly asks to alter them.
- Do not change the schematic, board outline, or component footprints unless explicitly requested.
- Keep changes focused and use the smallest appropriate Konnect operation.

After a meaningful layout change:

1. Re-inspect the affected area and resulting board state.
2. Run DRC.
3. Resolve errors caused by the change.
4. Do not suppress or waive DRC violations without explaining the specific reason.
5. Save through KiCad/Konnect and confirm the project still opens normally.

Never generate manufacturing outputs or apply a large autorouter result unless explicitly
requested. Keep the project in a state that can be opened normally by KiCad.

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
- No via drill overlaps an SMD solder-paste aperture; `verify.py` enforces this to prevent
  accidental via-in-pad solder wicking.
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
```

Prefer the corresponding Konnect ERC and DRC tools when available. Use these CLI checks only when
Konnect does not provide the required operation. Run the assembly BOM/CPL generators only when the
user explicitly requests updated manufacturing outputs. Use the bundled KiCad Python only for the
existing verification and assembly scripts; never use it to edit KiCad source files directly.

## Autorouting (optional)

Do not run an autorouter or apply a large autorouter result unless explicitly requested. When
requested, prefer Konnect `autoroute` / `check_freerouting`. Do not commit JREs or Freerouting
jars. If a local run is required, download into gitignored `.tools/` and delete it when finished.

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
