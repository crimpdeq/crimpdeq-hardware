# Crimpdeq PCB Agent Handoff

This is a KiCad 10 hardware project. The single canonical KiCad project lives at
`pcb/crimpdeq/`. Shared footprints are under `libraries/` and datasheets are under
`pcb/datasheets/`.

Do not create versioned design directories. Update the canonical project only when the user
explicitly requests a design change.

## Konnect workflow

Prefer Konnect for KiCad operations, including its supported file-based edits. When no suitable
Konnect tool exists or a tool cannot safely complete the requested operation, the agent may edit
`.kicad_pcb`, `.kicad_sch`, `.kicad_pro`, `.kicad_sym`, `.kicad_mod`, `fp-lib-table`, and
`sym-lib-table` directly using KiCad APIs, format-aware scripts, or precise text edits.

For direct file edits:

- Explain the tool limitation and intended fallback before writing. Stay within the user's
  requested design change; this permission does not authorize unrelated repairs.
- Save and close every affected KiCad editor first. Never overwrite a file whose live editor
  may hold unsaved changes. Confirm any lock is stale before removing it.
- Back up the affected files outside the canonical project directory before editing, and check
  that the source files have not changed since inspection before replacing them.
- Prefer KiCad APIs or format-aware editing. Preserve UUIDs, schematic identities, pad-to-net
  connectivity, routing, placement, and unrelated content unless explicitly changing them.
- For net renames, update all affected pads, tracks, vias, zones, labels, rules, and verification
  expectations consistently; prove connectivity is unchanged apart from the requested rename.
- Reopen the design in KiCad, run applicable ERC/DRC and `verify.py`, and inspect the result.
  Resolve new violations without suppressing checks. Report any remaining verification limits.

### MCP configuration

Keep the shared `.mcp.json` committed. Each checkout used with Pi must also have an ignored,
machine-local `.pi/mcp.json` whose `command` points to the installed Konnect executable by
absolute path. For this macOS installation:

```json
{
  "mcpServers": {
    "konnect": {
      "command": "/Users/sergio/Documents/KiCad/10.0/3rdparty/plugins/com_github_mixelpixx_konnect/bin/konnect"
    }
  }
}
```

Update the absolute path when Konnect is installed elsewhere. Do not commit `.pi/mcp.json` because
it is machine-specific.

Cursor should use the same absolute Konnect path in `~/.cursor/mcp.json` (and optional
project `.cursor/mcp.json`). Do not pass `--config` unless that file exists. Committed
`.mcp.json` keeps `command: "konnect"` for Pi; that name is not on PATH in this checkout,
so Cursor must not rely on it.

At the start of PCB work:

1. Call `list_toolboxes` to discover the tools available in the current Konnect installation.
2. Confirm the project with `get_project_info` on `pcb/crimpdeq/crimpdeq.kicad_pro`, then check
   KiCad IPC with `open_project` (pass the same project path). If `open_project` itself is
   unavailable, report that explicitly before continuing. File-based schematic work can proceed
   when IPC is down; live PCB edits require KiCad running with this board open.
3. Load user and project configuration with `load_user_config` and `load_project_config`, then use
   `get_effective_config` for design decisions.
4. Confirm the intended project and board paths. For live operations, verify that the correct
   board is open; for direct file edits, verify that the affected editors are closed. Do not
   assume a board currently open in KiCad belongs to this working tree.
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
- Keep changes focused and use the smallest appropriate Konnect operation or the controlled
  direct-file fallback described above.

After a meaningful layout change:

1. Re-inspect the affected area and resulting board state.
2. Run DRC.
3. Resolve errors caused by the change.
4. Do not suppress or waive DRC violations without explaining the specific reason.
5. Save through KiCad/Konnect for live edits. For direct edits, reopen the saved files in KiCad
   and confirm the project loads normally.

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
- Avoid dumping full board or schematic diffs into context. For direct edits, inspect a focused
  diff or structured before/after comparison alongside DRC, ERC, and `verify.py` output.
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
- All 55 footprints have unique schematic symbol paths matching the saved schematic. C11,
  C19, J11, J12, and U3 were relinked without changing placement, routing, or pad nets.
  `verify.py` rejects missing or duplicate symbol paths. This does not resolve the separate
  routed-net naming mismatches (`Buck_Coil` vs `/Buck_Coil`, and U3's AIN0 name).
- U1 antenna and D4 LED are on the back; J2 USB-C and U3 ADS1220 are on the front.
- U1 ground pins 37–53 are connected to GND.
- MAX17048 U5 TDFN pad 7 is SCL (`IO6_SCL`) and pad 8 is SDA (`IO7_SDA`).
  Wiring: GPIO6 → U5.7 SCL; GPIO7 → U5.8 SDA. Firmware in
  `../crimpdeq-firmware/src/main.rs` uses GPIO7=SDA and GPIO6=SCL.
  Coordinate any future pin-map change with that firmware. The I²C names
  were corrected as metadata only (copper and GPIO numbers unchanged).
  Post-rename ERC, error-severity DRC with schematic parity, and
  `verify.py` are green.
- R20/R21/R22 are 10 kΩ pull-ups for SCL, SDA, and MAX17048 ALERT, respectively.
  `verify.py` preserves these pad-to-net assignments.
- L2 is a signal-free solid GND plane. L3 carries the 3V3 pour and low-speed signals.
- At least twelve dedicated GND stitching vias connect the outer floods to L2.
- No via drill overlaps an SMD solder-paste aperture; `verify.py` enforces this to prevent
  accidental via-in-pad solder wicking.
- The buck switch node is 6.84 mm and feedback is 4.85 mm with no feedback vias.
- U2, Q2, and D4 use datasheet top-view pad order on the back; U5 uses the standard KiCad
  TDFN top-side geometry. `verify.py` enforces component-side pad order, side, and rotation.
- U3 is ADS1220 (TSSOP-16) with ratiometric bridge excitation from +3V3 (E+/REFP0) and
  E-/REFN0 on GND. Local AVDD/DVDD decoupling is C11 + C19.
- SPI to U3: GPIO5 `IO5_SCK`→SCLK, GPIO4 `IO4_MOSI`→DIN, GPIO3 `IO3_CS`→~CS,
  GPIO1 `IO1_MISO`→DOUT/~DRDY. CLK is grounded; dedicated ~DRDY is unused.
- Analog filter cluster: C12 `(137.200, 74.100)` rot 180; R7
  `(137.975, 75.800)` / R8 `(136.425, 75.800)` rot −90; AIN0/AIN1 both 7.338 mm,
  0 vias, F.Cu; +3V3 stitch via `(137.400, 71.750)`.
- USB D+/D−: 41.49875 / 41.49829 mm, Δ 0.000459 mm; 3 vias each on
  B.Cu/F.Cu/In2.Cu. J2 vias `(146.965, 77.0322)` / `(147.65, 77.85)`; U1 vias
  `(136.802, 61.026)` / `(134.245, 62.331)`. Canonical SHA `96043150…`; pre-USB
  analog backup `ae89cc72…`. Not a 90 Ω stackup claim.
- Schematic R7/R8 `Value` is `100R 1%` but instance LCSC is `C25741` (the 100 kΩ
  BOM line). Assembly CSV uses `C25076`. Do not edit unless asked.
- Load-cell pads are grouped on the bottom edge near U3; battery/switch pads are on the right.
- The ESP32 antenna and USB body retain their intentional board-edge overhangs.

## Package contents

- KiCad source and rules: `pcb/crimpdeq/crimpdeq.{kicad_pcb,kicad_pro,kicad_dru,kicad_sch}`
- Gerber ZIP: `pcb/crimpdeq/gerbers/crimpdeq.zip`
- Assembly BOM/CPL: `pcb/crimpdeq/assembly/crimpdeq_{bom,cpl}.csv`
- DFM report: `pcb/crimpdeq/reports/crimpdeq_pcbway_tht_to_smd.md`
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

On this Linux checkout, `kicad-cli` is `/usr/bin/kicad-cli` and KiCad Python is
`/usr/bin/python3` with `pcbnew.py` at `/usr/lib/python3.14/site-packages/pcbnew.py`.

Prefer the corresponding Konnect ERC and DRC tools when available. Use these CLI checks only when
Konnect does not provide the required operation. Run the assembly BOM/CPL generators only when the
user explicitly requests updated manufacturing outputs. Use a Python environment compatible with
this KiCad installation for verification, assembly scripts, and KiCad API edits. Direct source
edits must follow the safeguards in the Konnect workflow above.

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
- J5–J12 are bare cable pads and must be marked Do Not Place.
- J2 includes plated through-hole shell tabs; assembly may require THT/manual soldering.
- Re-check package, polarity, side, rotation, and manufacturer DFM before ordering.
- Physical validation of power integrity, USB, ADS1220 noise, antenna performance, and connector
  fit is still required.
