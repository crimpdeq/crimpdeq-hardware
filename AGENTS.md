# Crimpdeq PCB Agent Handoff

KiCad 10 hardware project. Canonical project: `pcb/crimpdeq/`. Shared footprints under
`libraries/`, searchable Markdown datasheets under `pcb/datasheets/`.

Do not create versioned design directories. Update the canonical project only when the user
explicitly requests a design change.

## Konnect workflow

Prefer Konnect for KiCad operations, including its supported file-based edits. When no suitable
Konnect tool exists or a tool cannot safely complete the requested operation, edit
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
- For net renames, update all affected pads, tracks, vias, zones, labels, rules, and
  verification expectations consistently; prove connectivity is unchanged apart from the
  requested rename.
- Reopen the design in KiCad, run applicable ERC/DRC and `verify.py`, and inspect the result.
  Resolve new violations without suppressing checks. Report any remaining verification limits.

## Session start (once per session)

Run this sequence ONCE, before the first board operation of a session. Do not repeat it for
later user messages in the same session unless a call fails or KiCad/Konnect restarts:

1. Call `list_toolboxes` to discover the tools in the current Konnect installation.
2. Confirm the project with `get_project_info` on `pcb/crimpdeq/crimpdeq.kicad_pro`, then check
   KiCad IPC with `open_project` (same path). If `open_project` is unavailable, report that
   explicitly: file-based schematic work can proceed; live PCB edits require KiCad running with
   this board open.
3. Load configuration with `load_user_config` and `load_project_config`, then use
   `get_effective_config` for design decisions.
4. Confirm the intended project and board paths. For live operations, verify the correct board
   is open; for direct file edits, verify the affected editors are closed. Do not assume a
   board open in KiCad belongs to this working tree.
5. Inspect the board before making changes.
6. In the first tool call, before any other substantial reads or work, load every toolset
   you expect to need for the session's phase, then keep the tool list stable. Avoid
   unload/reload cycles: each tool-list change invalidates the prompt cache for the whole
   conversation that follows it.

Before modifying the PCB: inspect the affected components, pads, nets, rules, and geometry;
run placement and design-rule checks where applicable; briefly explain the intended changes;
preserve unrelated local changes and existing design intent.

During layout: prefer live KiCad IPC operations; preserve locked items unless the user
explicitly asks to alter them; do not change the schematic, board outline, or footprints unless
explicitly requested; keep changes focused.

After a meaningful layout change: re-inspect the affected area, run DRC, resolve errors caused
by the change, and never suppress or waive violations without explaining why. Save through
KiCad/Konnect for live edits; for direct edits, reopen the saved files and confirm the project
loads normally. Never generate manufacturing outputs or apply a large autorouter result unless
explicitly requested.

## Session efficiency

- Split work across chats: schematic, then PCB/route, then verify/docs. Start a fresh session
  once ERC, DRC, and `verify.py` are green.
- Prefer Konnect MCP queries over reading or dumping whole `.kicad_pcb` / `.kicad_sch` /
  netlist files into context.
- Batch repeated queries (component pads, nets, traces) into a single `mcpScript` call that
  loops and filters, returning only a summary, instead of many individual tool calls. Each
  individual call costs a full model turn over the whole conversation.
- Search files with `rg` and read only the matching section or line range. Do not load an
  entire report, README, checker, or generated file into context unless the whole file is
  required.
- When iterating on a local script (router driver, checker, generator), run the edit-run-fix
  cycle inside a single shell command where safe: retry internally until checks pass or a
  real blocker appears, then return only the final diff, validation output, and any blocker.
  Do not spend one model turn per attempt. Design-file edits still follow the Konnect
  workflow safeguards above.
- If KiCad IPC is unavailable, attempt recovery once, then switch to the file-based workflow
  or ask the user to start KiCad with IPC enabled. Do not spend multiple turns on IPC
  recovery.
- Read each relevant datasheet section in `pcb/datasheets/` once, then reference it. Do not
  re-read the same section later in the session.
- Avoid dumping full board or schematic diffs into context; inspect a focused diff or
  structured before/after comparison alongside DRC, ERC, and `verify.py` output.
- Keep Freerouting/Java downloads in gitignored `.tools/`; delete when done.
- Plan first when the change is ambiguous; execute only the locked scope.
- Do not leave one-shot helper scripts in `tools/`; only keep reusable checkers such as
  `verify.py`.

## Design constraints

- Do not introduce electrical changes without an explicit request.
- Keep the ESP32-C3-MINI-1 module antenna at the board edge with an all-layer copper keepout.
- Keep L2 free of signal routing and unbroken under the antenna and ADS1220 analog inputs.
- Keep the ADS1220 AIN0/AIN1 pair short, symmetric, on one signal layer, and over solid GND.
- Keep digital nets away from the ADS1220 analog input region.
- Keep power paths low impedance and the SY8088 buck loop compact.
- Route USB D+/D- as a matched pair and keep protection/CC parts near J2.
- Refill zones after PCB changes.

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

On the Linux checkout, `kicad-cli` is `/usr/bin/kicad-cli` and KiCad Python is
`/usr/bin/python3` with `pcbnew.py` at `/usr/lib/python3.14/site-packages/pcbnew.py`.

Prefer the corresponding Konnect ERC and DRC tools when available; use these CLI checks only
when Konnect does not provide the operation. Run assembly BOM/CPL generators only when the user
explicitly requests updated manufacturing outputs.

## Preview renders

Generate previews on demand with Konnect; do not commit generated render files:

- Schematic: `konnect_get_schematic_view` with `schematic: pcb/crimpdeq/crimpdeq.kicad_sch`.
- PCB: `konnect_get_board_2d_view` with `board: pcb/crimpdeq/crimpdeq.kicad_pcb` and the
  desired `width`/`height` (top-down 3D render, not a layer plot).
- Request cropped, downscaled renders (around 800 px wide) sized to the question being
  answered, and do not reread an identical render that is already in context.

If a preview must be saved, keep it under `/tmp` and delete it after use.

## Manufacturing notes

- Track only `pcb/crimpdeq/gerbers/crimpdeq.zip`, not loose Gerber files.
- J5-J12 are bare cable pads and must be marked Do Not Place.
- J2 includes plated through-hole shell tabs; assembly may require THT/manual soldering.
- Re-check package, polarity, side, rotation, and manufacturer DFM before ordering.
- Physical validation of power integrity, USB, ADS1220 noise, antenna performance, and
  connector fit is still required.
