# Crimpdeq prototype readiness review

**Last updated:** 2026-09-10, W6 follow-up on `fix/adc-bypass-cleanup`, HEAD `901718df6b036220c08ba32bd71c96748747bdcb` (uncommitted follow-up changes).

**Current round:** **NEEDS ATTENTION.** Prior remediation was committed as `901718d` at Sergio's request, without pushing. The four subsequently queued W6 objects are now removed; two further dangling track segments are exposed and retained outside that four-item scope. Final checks: **0 DRC errors, 0 unconnected, 43 board warnings, 0 parity findings, ERC 0 errors; `verify.py` PASS.** C1/C2/W2/W5 and W1 source metadata remain resolved; W3/W4/W7/W8, the two-track W6 decision and W1 assembly-release handling remain open. Historical rounds and the updated decision queue follow.

## 1. Ver: NEEDS ATTENTION

**The two CRITICAL blockers C1/C2 and the W2 digital/analog corridor violation are resolved.** This is a prototype assessment, not a production qualification or approval of the existing fabrication package.

**Current isolated refill DRC and errors-only ERC pass; explicit all-severity schematic parity is now zero and `verify.py` passes.** The 43 remaining board warnings are itemized in the latest W6 follow-up round. All-severity ERC was not rerun; its earlier warnings remain historical coverage. C11/C19 bypass placement and routing were improved, an unused IO5_SCK stub was removed, R7/R8 supplier metadata was corrected, and the affected C11/C19/C12/R7/R8 CPL positions match the saved board. No BOM or Gerbers were generated or changed.

**Historical W2/W3 follow-up (counts below precede this remediation):** USB_D± now pass north of the AIN fanout on L3. CS goes around the north/west of U3, replacing its intermediate via without increasing its three-via count. The redundant USB_D+ inner-layer overlap was subsequently removed, and `verify.py` now rejects same-net collinear overlaps on the USB routes. Only the affected routing and cached fills changed in the PCB; all footprints, pad assignments, analog routing, outline and rules are unchanged. No assembly or manufacturing files changed. The corridor and USB-geometry checks pass. Saved-board DRC/parity retains 81 board warnings and 10 parity warnings, with zero errors or unconnected items; ERC and `verify.py` pass. L2 GND remains contiguous and covers 4,976 sampled AIN trace-envelope points. USB impedance/path matching and physical ADC noise testing remain pending.

**Next action:** Sergio/manufacturer must close the decision queue, including the two newly exposed W6 dangling track segments. Separately authorize and check a synchronized manufacturing package, with J5–J12 explicitly excluded from component placement. Current tool PASS is not ADC noise qualification, manufacturer acceptance, or certification of the existing Gerber/BOM/CPL package.

### Reviewed identity and scope — prior review-only round

The bullets below preserve the earlier review identity. This remediation started with the report already modified and `.pi/` untracked; it changed only the two authorized design files and this report, without changing branch or HEAD. No commits, pushes, remote/PR changes, library refresh, rules/severity changes, vendor contact, ordering, or manufacturing regeneration occurred.

- Original review date: 2026-09-08; current validation: 2026-09-09; KiCad CLI/Python 10.0.6.
- Working tree: `/home/sergio/Documents/Crimpdeq/crimpdeq-pcb`.
- Canonical project: `pcb/crimpdeq/crimpdeq.kicad_pro`.
- Current branch: `fix/adc-bypass-cleanup`; reviewed HEAD: `4f3ed260a4c4dd86b32ec6d32ba566a6044ef294`. Initial `git status --short`: only `?? .pi/`; no tracked uncommitted changes. HEAD differs from `9de34eb` only in this report, not in design files. Prior bypass checkpoint: `87dc660`; W2 follows report commit `95f1986`; W3 geometry follows `9de34eb`.
- This round modified only this report. Canonical PCB/schematic/project/rules hashes were checked unchanged after worker execution. No design edits, fabrication regeneration, commits, pushes, remote changes, ordering or vendor interaction were authorized or performed.
- Trusted manufactured baseline: `v2.0.0`, commit `4976be254f64bac70d162865ef47e0bbe7e2f28b`.
- The original review confirmed the canonical board over IPC. For W2, Konnect could not reach the PCB editor, so the editors were closed, the source was backed up outside the project, and KiCad API routing edits were tested/refilled on an isolated copy before revision-checked replacement. Konnect DRC/ERC were available; CLI supplied explicit refill/save and schematic-parity checks not exposed by those tools. This report assesses saved files, not arbitrary unsaved editor state.
- The original `feat/ads1220` revision and v2.0.0 were exported into `/tmp/crimpdeq-review-refjLB/{current,baseline}` for the baseline comparison in §3. Later fixes were inspected separately against their pre-change sources.
- Canonical zones were refilled and saved during the blocker fix. Subsequent changes improved C11/C19 bypass placement/routing, removed the IO5_SCK stub, synchronized R7/R8 metadata, corrected C11/C19 CPL rows, and cleaned the affected silkscreen and obsolete via. No project rules, libraries, BOM or Gerbers were changed.

## 2. Coverage

The original Konnect refill/parity coverage gap was resolved by the historical isolated CLI workflow. The table below preserves accumulated prior evidence; **its Konnect results were not rerun at HEAD**. The current round's actual coverage and NOT RUN items follow the table. Historical complete-coverage claims do not imply complete coverage in this session.

| Check / tool | Result and interpretation |
|---|---|
| `list_toolboxes`, `get_project_info`, `open_project` | PASS: correct canonical project and live board confirmed |
| User/project/effective configuration | PCBWay, four layers; preferred 0.15 mm trace/clearance, 0.30 mm drill; no project overrides |
| `find_orphan_items` | PASS: zero orphans |
| `find_shorted_nets` | PASS: zero shorts |
| `find_single_pin_nets` | Three heuristic hits: Buck_Coil, ENABLE, CHIP_PU; actual connected pad counts are 2, 2, 3, respectively. Not single-pin electrical nets |
| Current CLI ERC, errors only | PASS: zero errors. The earlier Konnect ERC result was also zero errors |
| CLI DRC, refill + save temporary board + schematic parity + errors only | PASS: exit 0, zero violations, zero unconnected items, zero error-severity parity findings |
| Current isolated CLI all-severity DRC + parity | 81 board warnings and 10 schematic-parity warnings; no errors or unconnected items |
| `tools/crimpdeq/verify.py` on current canonical board | PASS: 55 components, 172 connected named pads, 13 GND stitching vias; golden pin nets, unique symbol paths, component-side package geometry, outline, no L2 tracks, no via drill/paste overlap and route limits pass |
| Konnect `run_design_review` | Complete: one sheet, 112/112 symbols resolved, 55 footprints, 213 physical pads. Automated verdict NOT READY from two duplicate J2 decoupling heuristics; see adjudication below |
| Konnect `validate_for_manufacturing(fab_house='pcbway')` | Automated READY, zero issues, four layers. Does not certify existing CPL, part selection or analog performance |
| Konnect `audit_manufacturing`, `get_design_rules` | Completed; double-sided assembly and three cross-side proximity heuristics investigated |
| Konnect netlist export, isolated CLI XML netlists + read-only KiCad APIs | Compared all 43 shared schematic references and their PCB pad assignments, side, rotation and side-normalized pad geometry; details in §3 |
| Current schematic-to-board endpoint-set comparison | PASS: all 32 multi-pad electrical net endpoint sets match exactly, independent of names. This resolves the electrical meaning of the reported net-name conflicts, not their metadata inconsistency |
| Layout/DFM inspection | Four copper-layer Konnect SVG plots inspected; API checks of zones, analog reference coverage, digital crossings, dimensions, drills, rings, DNP and package pads completed |
| Existing BOM/CPL and DFM notes | CPL positions for C12/R7/R8 and later C11/C19 were corrected from saved-board placement. BOM and DFM notes are unchanged. Existing Gerber ZIP was not certified or regenerated |
| Current validation | Saved canonical board and isolated refill copy: zero errors/unconnected items; ERC zero errors; canonical `verify.py` PASS. Explicit all-severity parity: 81 board warnings + 10 parity warnings, zero errors |
| Change-scope verification | Earlier blocker fix changed C12/R7/R8 CPL rows and cached fills. The bypass follow-up moved/rerouted C11/C19, added one GND via, removed the IO5_SCK stub and an obsolete +3V3 via, synchronized two supplier fields, moved C11 text, and changed only C11/C19 in the CPL. Pad endpoint connectivity and AIN routing are unchanged |

### 2026-09-10 W6 follow-up — latest evidence

Sergio authorized committing the prior changes and proceeding with queued work. Commit `901718df6b036220c08ba32bd71c96748747bdcb` contains the prior schematic/PCB remediation and report; `.pi/` was left untracked and no push occurred. The next bounded task removed only the four W6 objects listed in the prior decision queue: three tracks (`7fadb04f`, `66885830`, `d76388cd`) and one via (`ea989365`). The schematic, text, pad geometry/net assignments, footprint placement, libraries, rules, zones and cached fills were not changed.

| Check | Before → after follow-up |
|---|---|
| Isolated refill/save DRC | Errors **0 → 0**, unconnected **0 → 0**, board warnings **45 → 43** |
| All-severity schematic parity | **0 → 0** |
| Errors-only ERC | **0 → 0**; all-severity ERC not rerun |
| Canonical `verify.py` | **PASS → PASS**; 55 components, 172 connected named pads, 13 GND vias; AIN0/AIN1 7.338 mm each, F.Cu, zero vias; corridor guards pass |
| Scope/invariants | Full parent diff review: exactly four specified S-expressions removed; all other source bytes preserved apart from deletion-site whitespace. Tracked-file hashes: only PCB changed before this report update; no manufacturing outputs or other tracked files changed |

**Remaining warnings:** 39 footprint-library mismatches + two library aliases + **two `track_dangling`** findings. Each remaining track was exposed by removal of its terminal segment; neither was included in the four-item follow-up scope. They remain unsuppressed and are named in §7. The written no-refresh library disposition still applies.

The first follow-up worker failed at provider usage limit before edits. Sergio requested the same worker methodology; the fresh native background-worker retry succeeded, with a parent decision gate retaining the two newly exposed segments. Editors/locks were checked, backups made and canonical source hash guarded before applying an **unrefilled** candidate. Only temporary copies received `--save-board`. The parent independently reran the complete documented isolated block: all three command exit codes zero. Evidence: `/tmp/crimpdeq-w6-parent-final-3AYLx6/{drc.json,erc.json,verify.log}`; baseline hashes/report snapshot `/tmp/crimpdeq-w6-parent-uc0Q08/`. Validated canonical PCB SHA-256: `8aea5696f7fd23f1cc8b70366b968c350abbf4065f5645b38a8e1f56eec875e1`.

**Follow-up visual review completed:** a fresh read-only worker rendered and inspected side-by-side F.Cu/B.Cu crops at all four edited regions (`/tmp/crimpdeq-w6-visual-975435/r{1,2,3,4}-{F_Cu,B_Cu}.png`). Each requested local feature disappeared, with adjacent pads/vias/copper visually intact; no collateral visual change was observed. A focused parser independently confirmed 607→603 segment/via records, exactly the four approved UUIDs absent and all remaining records byte-identical. AIN/L2 continuity is an unchanged-source invariant here, not a fresh full-board visual qualification. Canonical render-input hashes remained unchanged. GUI reload/save and physical qualification were **NOT RUN**. Disposable PNG/SVG previews were deleted after inspection; validation evidence and backups remain under `/tmp`.

### 2026-09-09 bounded remediation round — before W6 follow-up

This round accepts the supplied revalidation baseline rather than repeating the historical baseline comparison. Fresh-context native background workers performed research, geometry measurement, sequential schematic/PCB edits and visual review. The parent reviewed each design diff before the next edit phase and independently reran the documented isolated check block.

| Check | Supplied baseline → final result |
|---|---|
| All-severity DRC on an isolated refilled/saved copy | Errors **0 → 0**; unconnected **0 → 0**; board warnings **81 → 45** |
| Explicit schematic parity | Original W5 findings **10 → 0**; final total **0**. F1 temporarily introduced eight DNP mismatches until F2 aligned board attributes |
| Errors-only ERC | **0 → 0**; all-severity ERC **NOT RERUN** |
| Canonical `verify.py` | **PASS → PASS**: 55 components, 172 connected named pads, 13 GND vias; AIN0/AIN1 each 7.338 mm, F.Cu, zero vias; corridor/USB-overlap guards pass |
| F1 electrical/identity invariants | Before/after XML netlists: all **57 net endpoint sets identical**; every pre-existing UUID retained, one label UUID added |
| F2 copper/geometry invariants | Exactly four segments and two vias removed; no copper added. Remaining 539 segments, 68 vias, 213 pads and all six zone objects, including keepout/fill content, byte-identical |
| F2 text/DNP changes | 24 fabrication-reference mirror flags corrected, six front-silk text positions moved (U3, R21, R22, B−, E−, E+); no text deleted/reworded/resized; J5–J12 board DNP set |
| Regression/scope guard | Parent tracked-file hashes confirmed only the two design files changed before this report update. BOM/CPL/Gerbers, project/rules, libraries and all other tracked files unchanged; existing report edits preserved |

**Remaining board warnings:** 39 `lib_footprint_mismatch`, two `lib_footprint_issues`, three `track_dangling`, one `via_dangling`. All 24 mirror warnings, five silk overlaps and five silk-on-copper warnings are gone. Removing only the six expressly authorized objects exposed four parent-branch objects; their removal is not authorized by a request to remove exactly the original six. They remain unsuppressed and are listed in §7.

**W5 implementation detail:** schematic global net labels now match board `Buck_Coil` and `Net-(U3-AIN0)` without endpoint changes. C11/C19/U3 schematic footprint IDs match the existing unqualified embedded board IDs; no library was refreshed. Q2's datasheet field matches the board's `DMG2301L.pdf` URL; U5's schematic datasheet field matches the currently empty board field. This is parity synchronization, not improved library resolution or new part qualification. All eight J5–J12 schematic DNP flags and board `attr dnp` flags are now set; the existing CPL still contains their eight rows and has not been regenerated.

**Tool/safety record:** the first F1 attempt stopped without writes while KiCad/locks were present. Sergio saved and closed KiCad; process/lock and unchanged-hash checks preceded the retry. Builtin worker tool allowlists did not expose Konnect, so the explained fallback used backed-up, hash-checked, format-aware replacements, not broad KiCad serialization. Canonical zones were not refilled or rewritten; only isolated copies received `--refill-zones --save-board`. An early F2 scratch test used `board.kicad_pcb` without matching project/rule files and incorrectly reported four J2 hole errors; that result was rejected. The corrected same-stem isolated block and the independent parent run both give zero errors. No rules or severities were changed to obtain that result. The retry workflow subsequently ended with `Request was aborted` after F2's parent-approved edit/validation checkpoint, before launching visual review. The parent confirmed both design files still matched the reviewed candidate, captured the partial diff, and retried only the read-only visual stage as a fresh native background child; no external/foreground execution fallback was used.

Parent final evidence: `/tmp/crimpdeq-parent-final-3Bk2mG/{drc.json,erc.json,verify.log}`. F1 netlists: `/tmp/f1-{before,after}.xml`. F2 backup/evidence: `/tmp/crimpdeq-f2-backup-29lkhN/`, `/tmp/crimpdeq-remediation-f2-FcwgmK/`. Original report/diff/hash snapshot: `/tmp/crimpdeq-orchestrator-vk6KeL/`. These are disposable inspection artifacts, not release outputs.

**Visual review completed:** the fresh background worker generated and actually inspected isolated CLI plots of front/bottom silk with mask/pad context, all six moved-text regions, fabrication-reference montages and before/after copper-deletion regions. Moved silk and bottom-facing labels are upright/readable and visibly off same-side pads; 24/24 fabrication-reference mirror states are correct. All six requested copper objects are absent visually and by UUID; the four out-of-scope dangling items remain. J5–J12 pads, net mapping and DNP attributes were confirmed. The worker cited `ain-In2-Cu.png` in its L2 discussion; the parent separately inspected the correct **L2/In1.Cu** crop, `ain-In1-Cu.png`, showing a continuous plane with normal antipads. Byte-identical surviving copper/zones and `verify.py`, rather than the image alone, support the unchanged-corridor claim.

Inspected disposable visual artifacts were `/tmp/crimpdeq-visual-retry-657379/after/svg/{after-silk-mask-square,after-bottom-facing-silk-mask-square}.png`, `after/crops/` (moved-text, fabrication-reference and AIN layer crops), and `{before,after}/copper-crops/*-removed-objects-montage.png`. Generated PNG/SVG previews were deleted after inspection; validation logs and source backups were retained under `/tmp`. **GUI reopen was NOT RUN**; saved designs loaded through KiCad CLI/Python and isolated plots, not a reopened live editor. Very small unchanged fabrication text has no fabrication-scale readability guarantee. Hardware/impedance/noise/RF/physical checks remain unperformed.

### 2026-09-09 HEAD revalidation round — historical, before remediation

Four independent fresh-context background workers checked CLI results, baseline connectivity, available review/render operations, and metadata. The orchestrator reconciled conflicting claims against current JSON, source files and Git ancestry.

| Check at `4f3ed260` | Current result | Delta versus `9de34eb` round |
|---|---|---|
| KiCad CLI | 10.0.6 | Same version |
| Isolated refill/save DRC, all severities + parity | 0 errors; 0 unconnected; 81 board warnings; 10 parity warnings | 0 / 0 / 0 / 0 |
| Separate saved-state copy, before refill | Same 0 / 0 / 81 / 10 | C2 still resolved; not masked by refill |
| ERC, requested errors-only scope | 0 errors | 0 |
| `verify.py`, canonical saved board | PASS; 55 components, 172 connected named pads, 13 GND stitching vias | PASS unchanged |
| Current schematic ↔ PCB multi-pad endpoint sets | 32/32 match exactly | No endpoint drift |
| Trusted baseline XML export and requested pin-map comparison | U1, all 16 U3 pins, R7/R8/C12, J5–J12 and U5 agree with §3 | No drift from documented changes |
| Adjacent firmware pin-map inspection | Matches; firmware HEAD `3f664b6783c3b0cc61338b17435c94a48ff22913`, untracked `photos/` | Pin map only; no build/test |
| CLI copper/silkscreen plots, actually inspected by render worker | F.Cu/In1.Cu/In2.Cu/B.Cu and both silk layers inspected; AIN corridor free of digital tracks, L2 visually continuous beneath AIN, USB north of fanout, antenna notch visible | Supports W2/W3 geometry history; not impedance/noise/RF qualification |

**Additional ERC scope:** the render worker's all-severity ERC reports **27 warnings**: 21 `lib_symbol_mismatch`, four `lib_symbol_issues`, two `footprint_link_issues`; zero errors. The errors-only output has no violations. Thus “zero ERC warnings” is not established by the requested errors-only check. No all-severity ERC baseline was recorded for a numeric delta; these are newly recorded coverage, not a demonstrated regression.

**NOT RUN:** Konnect discovery/config loading, project/IPC confirmation, consolidated `run_design_review`, PCBWay `validate_for_manufacturing`, `audit_manufacturing`, Konnect netlist export and Konnect rendering: ambient Konnect tools were unavailable to the background worker. CLI temp-copy checks, XML export and layer plots substituted where equivalent operations exist; no equivalent consolidated/manufacturing verdict was obtained. Historical NOT READY/READY heuristics below remain prior evidence, not refreshed tool results. No claim is made about current live editor state.

**NOT RUN:** hardware noise/startup/USB/LED/RF/fit tests (no physical test setup exercised); firmware build/test (pin-map inspection only); electrical path tuning/impedance qualification; PCBWay stackup/process acceptance; BOM/CPL/Gerber regeneration or package certification (outside review scope). Existing Gerber ZIP remains unverified.

Temporary evidence: `/tmp/crimpdeq-review-sjUKwQ/` (DRC/ERC/verify and pre-refill copy), `/tmp/crimpdeq-review-DObl8V/{current,baseline}/netlist.xml` (baseline exports), `/tmp/crimpdeq-review-850ePi/` (fallback JSON, netlist and inspected PNG/SVG plots). These are disposable inspection artifacts, not fabrication deliverables. A direct parent pcbnew track-iterator query failed because Python 3.14 SWIG lacks `next`; actual via sizes were instead checked from PCB text, and cable drills through read-only pad APIs. No canonical file was saved.

### Reproducible isolated checks

From the repository root, with `T` as a fresh temporary directory:

```sh
DESIGN=pcb/crimpdeq
T="$(mktemp -d /tmp/crimpdeq-review-XXXXXX)"
cp "$DESIGN"/crimpdeq.kicad_{pcb,sch,pro,dru} "$T/"

kicad-cli pcb drc --refill-zones --save-board --schematic-parity \
  --severity-all --format json --output "$T/drc.json" \
  "$T/crimpdeq.kicad_pcb"
kicad-cli sch erc --severity-error --format json \
  --output "$T/erc.json" "$T/crimpdeq.kicad_sch"
/usr/bin/python3 tools/crimpdeq/verify.py "$DESIGN/crimpdeq.kicad_pcb"
```

In the prior 2026-09-09 refresh, the MCP gateway did not rediscover the previously loaded Konnect DRC/ERC operations, so that refresh used this documented CLI fallback. In the current round, ambient Konnect tools were unavailable to the background worker; the CLI fallback was used again. The original review's netlists were first obtained through Konnect; XML netlists were subsequently exported with `kicad-cli sch export netlist --format kicadxml` because Konnect did not expose that comparison format. Netlists and plots were inspection artifacts under `/tmp`, not manufacturing deliverables.

**Important limitations:** error-only parity hides warning-severity net conflicts. Existing project settings also ignore `missing_courtyard`, `track_not_centered_on_via`, `tuning_profile_track_geometries`, `footprint_filters_mismatch`, and `footprint_type_mismatch`; this review changed no severities or exclusions. In particular, a DRC pass does not validate USB tuning geometry. `verify.py` now rejects IO/USB/reset/LED-data tracks and vias on every layer within the projected AIN and cable-signal copper envelopes plus 0.20 mm. It does not itself prove antenna clearance or ground-plane coverage; supplementary geometry/plot checks address those topics. These checks are not electromagnetic simulation or PCBWay process approval.

### Automated audit adjudication

The following Konnect findings and adjudications are retained from prior rounds. The unavailable consolidated/manufacturing tools mean their complete finding set was **not independently refreshed** this round. Current CLI library warnings do not alone prove that every footprint mismatch is harmless; retained baseline geometry evidence supports the scoped interpretation, not a blanket waiver.

- **J2 decoupling, two reported errors:** both concern the connector's raw USB supply pins on `Net-(D8-A)`. C5 is 4.7 µF on VBUS downstream of D8, not directly on the connector net. This topology and all surviving supply-path pin assignments match trusted v2.0.0. A generic connector decoupling heuristic is not evidence of a new fatal defect; no blanket extra 100 nF/10 µF addition is prescribed. Confirm USB inrush and protection behavior on hardware.
- **+BATT/VBUS bulk-cap warnings:** C6/C5 are each 4.7 µF, matching v2.0.0 and the MCP73831 typical application. The tool's blanket ≥10 µF threshold is not a mandatory charger requirement.
- **C18–Q2, C9–R2, C15–C5 proximity warnings:** each pair is on opposite sides. Their 0.40/0.00/0.71 mm origin separations are not same-side component collisions. They instead require a supported double-sided assembly process and fixture review.
- **Missing MPN U3/U5:** U5's Value already identifies MAX17048G+T10; U3's Value is only ADS1220. Existing BOM uses supplier codes C48263/C2682616. Confirm exact manufacturer/orderable package codes with PCBWay; an LCSC code is not itself an MPN.

## 3. Delta vs v2.0.0

### Comparison method

Compared exported schematic pin-number → net mappings, including unconnected pins, and independently compared PCB pad nets and side-normalized pad geometry. Net endpoint sets distinguish renames from rewiring. Repeated physical U1 pad 49 instances were compared as multisets, not collapsed to a single pad. Layout displacement by itself was not treated as an electrical defect.

Baseline has 47 schematic components; current has 55. **43 references are shared**, four removed (`Q1 R5 R6 U4`) and twelve added (`C19 J5 J6 J7 J8 J9 J10 J11 J12 R20 R21 R22`). U3 is a shared designator but an entirely different IC and is not baseline-proven.

### Unchanged-and-matching

These **35 shared references have unchanged schematic pin-to-net names**:

`C1 C2 C3 C4 C5 C6 C9 C15 C16 C17 C18 D1 D2 D3 D4 D7 D8 D9 D10 J2 L1 Q2 R1 R2 R3 R9 R13 R14 R15 R16 R17 R18 R19 U2 U6`.

This includes charger U2, battery MOSFET Q2, buck U6/L1/divider, USB-C J2/CC/ESD, LED polarity and reset circuitry. Added/removed consumers on shared supply nets are accounted for separately below. Q2's schematic datasheet URL changed, not its pin nets. Board-only `/Buck_Coil` → `Buck_Coil` is a name change on L1.1/U6.3, not a changed connection.

All **42 retained non-U3 footprints preserve their component-side pad numbers, positions and sizes** relative to v2.0.0, including polarized devices and the multi-pad U1 ground array. Changes of board side/rotation below do not introduce a mirrored pin-order reversal.

### Changed-and-risky / new-and-unproven connectivity

| Refdes | Exhaustive changed pin mappings / interpretation |
|---|---|
| C10 | Pin 1: E+ → +3V3; pin 2 remains GND. Former HX711 excitation reservoir is now on the 3V3 rail |
| C11 | Pin 1: GND → +3V3; pin 2: HX711 VBG → GND. Repurposed nonpolar 100 nF bypass, not the old function |
| C12 | Pin 1: HX711 INA+ → ADS1220 AIN0; pin 2: INA− → AIN1. Still differential 100 nF |
| R7 | Pin 1: HX711 INA+ → ADS1220 AIN0; pin 2 remains A+ |
| R8 | Pin 1: HX711 INA− → ADS1220 AIN1; pin 2 remains A− |
| U1 | Pin 6/GPIO3: NC → CS; pin 13/GPIO1: NC → MISO; pin 18/GPIO4: IO4_DATA → IO4_MOSI, with ADC endpoint U3.12 → U3.16. Pin 19/GPIO5 retains IO5_SCK but its endpoint changes U3.11 → U3.1. Pins 20/21: IO6_SDA/IO7_SCL → IO6_SCL/IO7_SDA; the same GPIO6→U5.7 and GPIO7→U5.8 connections are retained. Pins 37–53: formerly absent/unassigned GND pad nets → explicit GND. Other U1 pin mappings unchanged |
| U5 | Pin 7: IO6_SDA → IO6_SCL; pin 8: IO7_SCL → IO7_SDA. Metadata corrected to TDFN datasheet pin 7=SCL, pin 8=SDA; not crossed physical wiring. Other pins unchanged |
| U3 | HX711 SOP-16 → ADS1220 TSSOP-16. Every pin's role reviewed afresh; complete new mapping below |

New R20/R21/R22 are 10 kΩ pull-ups to +3V3 on GPIO6/SCL, GPIO7/SDA and GPIO10/ALRT, respectively. ALERT still joins U1.16 to U5.5. The adjacent firmware `src/main.rs` currently selects GPIO7=SDA, GPIO6=SCL, GPIO5=SCLK, GPIO4=MOSI, GPIO3=CS, GPIO1=MISO and SPI mode 1; this is a pin-map check, not a firmware validation.

Removed Q1/R5/R6 and old HX711 feedback/reference functions are not assumed preserved. Former U4 terminal nets map to the new cable pads as follows: U4.11 +BATT → J6/J7, U4.10 SW_BATT → J8, U4.12 A+ → J9, U4.13 A− → J10, U4.14 GND/E− → J12. Old U4.15 E+ is replaced by J11 on **+3V3**, not the former regulated HX711 E+ rail. J5 additionally exposes battery negative/GND. Verify the new cable legend instead of transferring the old connector's pin order or SW+ naming blindly.

### All footprint-side and rotation deltas

All 19 side changes are **front → back**:

`C1 C2 C3 C5 C6 C10 D1 D2 D4 Q2 R1 R2 R3 R13 R17 R18 R19 U1 U2`.

Every other common reference remains front-side. The following are all changed board rotations, in KiCad degrees; references not listed retain their old angle:

| References | Old → current |
|---|---|
| C2, R16, U3 | 90 → 0; 90 → −90; 90 → 0, respectively |
| C3, C6, C16, C18, D1, D8 | −90 → 90 |
| C5, R2, U6 | 0 → 90; 0 → −90; 0 → −90, respectively |
| C9, R15 | 180 → 90 |
| C11, R1, R9 | −90 → 0 |
| C12 | 90 → 180 |
| C15 | 180 → −90 |
| D2 | 180 → 90 |
| D4 | 0 → 90 |
| D7, D9, D10, R17 | 90 → 0 |
| L1, R3, R14 | 180 → 0 |
| R7 | 90 → −90 |
| R8 | 0 → −90 |
| R18, R19 | −90 → 0 |
| U1, U5 | 0 → 180 |
| U2 | 90 → −90 |

Current board library IDs for C11/C19/U3 lack the schematic's library prefix; actual pad geometry is present. U3 is the only shared reference whose physical pad geometry changed, as required by the IC/package replacement.

### ADS1220 datasheet review

Reviewed `pcb/datasheets/ads1220.md`, Table 5-1 and §§8.3.2.1, 8.3.4, 9.1, 9.3, 9.4. Other supporting references: local MAX17048 pin table, MCP73831 typical application, SY8088 pinout/layout, WS2812B pin table and ESP32 module antenna/pin diagrams.

| U3 TSSOP pin | Connection | Assessment |
|---|---|---|
| 1 SCLK | U1.19/GPIO5 | Correct SPI clock; no series damping |
| 2 CS | U1.6/GPIO3 | Correct active-low select; no series damping |
| 3 CLK | GND | Correct for internal clock |
| 4 DGND, 5 AVSS | GND | Common ground, backed by L2 |
| 6 AIN3/REFN1, 7 AIN2 | Explicitly unused | Not floating digital inputs; unused analog channels |
| 8 REFN0 | GND/J12 E− | Correct ratiometric negative reference |
| 9 REFP0 | +3V3/J11 E+ | Correct excitation/reference source |
| 10 AIN1 | C12.2/R8.1, through R8 to J10 A− | Correct negative input |
| 11 AIN0/REFP1 | C12.1/R7.1, through R7 to J9 A+ | Correct positive input |
| 12 AVDD, 13 DVDD | +3V3; C11/C19 each 100 nF to GND | Correct electrical bypass topology; placement caveat below |
| 14 DRDY | Explicit NC | Datasheet permits unused output; use DOUT/DRDY or polling |
| 15 DOUT/DRDY | U1.13/GPIO1 | Correct MISO; no series damping |
| 16 DIN | U1.18/GPIO4 | Correct MOSI; no series damping |

U3 is front, rotation 0°, pin 1 upper-left and pin 16 upper-right in component top view; 0.65 mm pitch TSSOP-16 geometry matches PW, not VQFN. U2 back −90°, Q2 back −90°, D4 back +90°, U5 front 180° also pass component-side geometry checks. Their retained pin nets and polarity agree with baseline; U5's TDFN pin numbering separately agrees with its datasheet.

A symmetrical bridge excited at 3.3 V nominally places its common mode near 1.65 V, suitable in principle for the PGA; actual bridge sensitivity, offset and selected gain must meet the common-mode and ±VREF/gain limits. Firmware must select REFP0/REFN0 rather than assume the default internal 2.048 V reference. For two 100 Ω inputs and C12=100 nF, the simple differential RC pole is approximately **7.96 kHz**, ignoring bridge source impedance. This is not proof of low-noise performance or adequate rejection for every sample rate. TI recommends a high-quality differential capacitor, preferably C0G, and 47 Ω series resistors on used digital signals; neither C12 dielectric nor those series resistors is established by this schematic.

## 4. Findings

### Latest disposition — working-tree follow-up at `901718d`

| Finding | Latest status and evidence |
|---|---|
| C1 | **STILL RESOLVED.** Corrected CPL evidence retained; BOM/CPL byte-identical to session start. No assembly package certification implied. |
| C2 | **STILL RESOLVED.** Saved canonical fill content unchanged; final isolated refill check has zero errors/unconnected. |
| W1 | **SOURCE METADATA FIXED; RELEASE HANDLING OPEN.** J5–J12 DNP=true in schematic and PCB, matching BOM Do Not Place intent. Existing CPL still lists all eight; its correction/assembler handling awaits a separately authorized release step. |
| W2 | **STILL RESOLVED.** Parent `verify.py` corridor and USB-overlap guards PASS; surviving copper and zones unchanged. |
| W3 | **OPEN; MEASURED, NOT TUNED.** U1→J2 A-side D−/D+ planar difference 3.6374 mm; B-side 0.3134 mm. Branch-separated paths and limitations in §7; no USB copper changed. PCBWay stackup/90 Ω assessment and tuning decision pending. |
| W4 | **OPEN; PROPOSAL ONLY.** Both 100 nF bypass capacitors share a 0.8786 mm routed return segment; current-loop impedance remains unqualified. Four 47 Ω SPI resistors and specified C12 C0G dielectric are proposed in §7, not applied. |
| W5 | **FIXED.** Original ten parity findings resolved; final all-severity parity zero. All 57 schematic net endpoint sets and existing UUIDs preserved. Library/procurement quality is not inferred from metadata parity. |
| W6 | **PARTIALLY FIXED.** Text warning categories remain zero. Original six dangling objects and the subsequent four queued objects are removed. **43 warnings** remain: 39 library mismatches + 2 aliases + 2 newly exposed dangling tracks retained outside follow-up removal scope. Written dispositions below and §7. |
| W7 | **OPEN; PUBLISHED CAPABILITY CONFLICT.** PCBWay's published 0.15 mm annular-ring minimum exceeds the board's 0.10 mm minimum; order-specific acceptance/redesign decision required. Published drills/spacing/slots do not constitute acceptance. |
| W8 | **OPEN; ACTUAL V6 EVIDENCE FOUND.** Supplier-linked WS2812B-V6 datasheet explicitly says 3.3 V is supported, but guaranteed operating-range and VIH characterization at 3.3 V were not found. Keep/substitute qualification decision remains with Sergio. |

**Library disposition (W6):** retain all 39 embedded-footprint mismatch warnings and the two aliases (Rust_Board/J2 and PCM_Espressif/U1), without refresh, suppression or waiver. Embedded pads remain intact; prior geometry evidence is retained but is not a blanket determination that every library difference is harmless. A later explicit library audit must compare each embedded footprint against the intended manufacturer package before any selective refresh. The unavailable aliases do not mean the present board lacks physical pads. These unresolved library checks remain part of release review.

### Prior disposition at `4f3ed260` — historical evidence retained below

| Finding | Revalidated status and evidence |
|---|---|
| C1 | **STILL RESOLVED.** C12/R7/R8 CPL coordinates, sides and rotations match the board; C11/C19 rows also agree. This is a narrow placement check, not package certification. |
| C2 | **STILL RESOLVED.** Separate pre-refill saved-copy DRC has zero errors/unconnected, identical to the isolated refill result. |
| W1 | **STILL OPEN.** J5–J12 board attributes remain 0/not DNP; all eight BOM entries say Do Not Place and all eight remain in CPL. |
| W2 | **STILL RESOLVED.** Canonical `verify.py` corridor checks pass; inspected CLI layer plots agree with north-routed USB and clear AIN corridor/L2 coverage. The historical 4,976-point ground sampling was not rerun; visual continuity is not full return-path qualification. |
| W3 | **STILL OPEN; geometry fix retained.** USB overlap/corridor checks pass; coupled endpoint-path matching and stackup impedance remain unvalidated. No copper changed since the prior round. |
| W4 | **STILL OPEN.** C11/C19/C12 remain 100 nF; no established C12 dielectric or SPI 47 Ω damping. TI's series-resistor, differential-cap quality and monotonic-ramp guidance still applies. Bypass improvement is retained; startup/current-loop/noise performance is untested. |
| W5 | **STILL OPEN.** Current DRC JSON confirms all ten identities: net conflicts L1.1/U6.3 and C12.1/R7.1/U3.11; footprint IDs C11/C19/U3; datasheet fields Q2/U5. Current endpoint sets independently match 32/32. |
| W6 | **STILL OPEN.** Current 81-warning count: 12 mirrored + 12 nonmirrored text, five silk overlaps, five silk/copper overlaps, 39 footprint-library mismatches, two unavailable aliases, four dangling tracks, two dangling vias. Silk defects are visible in current plots. No cleanup performed. |
| W7 | **STILL OPEN.** Direct source inspection confirms actual vias 0.50/0.30 and 0.60/0.30 mm, all eight cable drills 0.70 mm, Default clearance 0.20 mm and global minimum field 0.00 mm. Minimum nominal via ring remains 0.10 mm; no manufacturer acceptance obtained. |
| W8 | **STILL OPEN; variant evidence clarified.** BOM says WS2812B, 5050 footprint, supplier `C52917433`; `_gen_bom.py` comments identify WS2812B-V6/SMD5050-4P, not WS2812B-2020. The local generic datasheet labels VDD +3.5–+5.3 V under absolute maxima and characterizes at 4.5–5.5 V; neither establishes guaranteed 3.3 V operation of the selected V6 part. Supplier-code/comment identity is not voltage qualification. |

**Exact readiness gates:** reconcile W1 DNP/source/assembly handling; resolve or explicitly disposition W3 path matching/impedance and W4 analog/startup risk; disposition W5 metadata and W6 silk/dangling/library warnings without blanket suppression; reconcile W7 actual process constraints and W8 guaranteed LED variant/margin. Separately authorize preparation and checking of a synchronized fabrication/assembly package. Until then **NEEDS ATTENTION**; tool PASS is neither analog noise qualification nor PCBWay acceptance nor certification of the existing files.

### CRITICAL — C1/C2 resolved

**C1. Obsolete C12/R7/R8 CPL entries — FIXED.**

`pcb/crimpdeq/assembly/crimpdeq_cpl.csv` now contains the following live-board-derived entries (CSV Y is negative board Y; −90° is represented as 270°):

| Ref | Previous CPL X, Y | Corrected CPL X, Y | Corrected rotation / side |
|---|---|---|---|
| C12 | 131.2500, −74.5000 | 137.2000, −74.1000 | 180° / top |
| R7 | 135.8000, −74.5000 | 137.9750, −75.8000 | 270° / top |
| R8 | 128.8000, −73.5000 | 136.4250, −75.8000 | 270° / top |

Exactly these three rows changed; the other 52 entries, including existing J2 centroid and IC rotation conventions, were preserved. Post-save Konnect placement queries confirm all three coordinates and angles. These are nonpolar two-terminal passives; the corrected angles follow the existing top-side passive convention. This narrow correction does not certify assembler-specific U3/U6/U1 rotations or the entire release package; those still require assembly preview approval.

**C2. Stale canonical zone fills — FIXED.**

Before the fix, saved canonical copper still produced **54 DRC errors**: 43 clearance, five hole-clearance and six solder-mask-bridge findings. `refill_zones` and `save_project` were applied to the confirmed canonical live board through IPC. DRC of the saved board, without another refill, now reports **zero errors and zero unconnected items**. ERC and `verify.py` pass; explicit all-severity schematic parity has no errors and retains the previously documented ten warnings.

For the C2 refill operation specifically, a format-aware before/after comparison confirmed that only cached filled polygons changed in the PCB, aside from serialization ordering. Later authorized bypass-layout cleanup changed the focused items listed in the coverage table; it did not change pad endpoints or the AIN routes. The existing Gerber ZIP remains unchanged and **is not certified as representing the current board**; preparing and checking a synchronized fabrication package remains a separate release action.

### WARNING — historical findings before bounded remediation

These detailed descriptions preserve the prior state. The latest status table and §7 supersede their open/fixed wording where this round changed the evidence.

**W1. J5–J12 DNP intent still disagrees across sources; R7/R8 metadata is fixed.** R7/R8 schematic and PCB LCSC fields now use `C25076` for 100 Ω, matching their Value, AssemblyNote and existing BOM. J5–J12 still have PCB DNP=false and attributes=0 and remain in the CPL, while the existing BOM explicitly says Do Not Place. **Fix:** make source metadata and eventual assembly files agree; PCBWay must treat those eight entries as bare cable pads, not buy/place connectors. Do not regenerate BOM blindly from current fields.

**W2. Digital routing beneath the ADS1220 inputs — FIXED.** The former USB_D+/USB_D− L3 and IO3_CS B.Cu crossings are removed. USB passes north of the AIN fanout at y=67.95/68.35 mm, with the D− turn south occurring east of the corridor. CS instead runs north/west of U3 on L3, with a short F.Cu transition near the MCU. Its old via at (142.462,69.750) is replaced by a 0.60/0.30 mm via at (145.050,57.700); all three affected nets retain three vias. No digital copper enters the lower filter/cable guard x=128–140, y=74–81.9 mm. AIN0/AIN1 remain 7.338 mm each, zero vias, F.Cu. L2 remains track-free with one contiguous GND fill; 4,976 trace-envelope samples at ≤0.05 mm steps retain GND beneath AIN copper. A new geometry-derived `verify.py` corridor guard rejects the original crossings and passes the fixed board. No design-constraint exception or suppression was used. Radio/USB/ADC noise tests remain required; geometry is not a noise qualification.

**W3. USB pair geometry — redundant excursion FIXED; matching remains unvalidated.** Both nets use 0.20 mm tracks and three vias. The redundant USB_D+ In2.Cu loop and its two short vertical legs were removed and replaced by one direct `(148.548,72.800)→(148.548,74.200)` segment. The previous **1.583 mm** collinear overlap is gone; `verify.py` now rejects same-net collinear overlaps on the USB inner-layer routes. Aggregate copper is now 37.745 mm for D+ and 40.210 mm for D−. These totals include branches and are not electrical path lengths. TVS branches, layer transitions and the remaining 2.465 mm aggregate difference mean the actual U1-to-J2 pair is still not tuned or impedance-qualified. **Remaining fix:** inspect the complete pair as a coupled route, preserve ESD branches, obtain PCBWay's stackup before claiming 90 Ω, and use field/length tuning only after defining the actual endpoint path. Full-speed USB may tolerate this, but no numeric matching claim is made.

**W4. ADC bypass placement improved, but interface/filtering and startup risk remain.** C11/AVDD and C19/DVDD supply-pad distances are now approximately 2.98 mm and 2.53 mm, respectively, with direct F.Cu supply routing and a dedicated nearby GND via. This is better than the reviewed 4.14/2.96 mm placement, but actual current-loop inductance and return quality are not proven by distance alone. There are no TI-recommended 47 Ω SPI series resistors. C12 dielectric is unspecified and its simple RC pole is relatively high. **Fix:** confirm the AVDD/DVDD return paths, selected MLCC dielectric and supply ramp; consider damping/filter footprints in a separately authorized revision. Test at intended gain/rate with USB and radio activity. TI requires a monotonic supply ramp slower than 1 V per 50 µs and approximately 50 µs settling before communication; static checks do not prove either.

**W5. Ten warning-level parity findings remain.** Five pad-net name conflicts are limited to L1.1/U6.3 (`Buck_Coil` versus `/Buck_Coil`) and C12.1/R7.1/U3.11 (`Net-(U3-AIN0)` versus the schematic AIN0/REFP1 auto-name). Three footprint-ID warnings concern C11/C19/U3; two datasheet-field differences concern Q2/U5. All 32 multi-pad endpoint sets match, so no extra electrical connection is inferred from these warnings. **Fix:** synchronize metadata carefully without moving copper or changing pad endpoints; rerun all-severity parity. An error-only pass is not metadata parity.

**W6. Silkscreen and dangling copper still need cleanup/disposition.** The current 81 board warnings comprise 24 mirrored/nonmirrored texts, five silk overlaps, five silk-on-copper, 39 footprint-library mismatches, two unavailable library aliases, four dangling tracks and two dangling vias. The C11/C19 text conflict and approximately 2.04 mm IO5_SCK stub are fixed. Remaining dangling tracks are three +3V3 remnants (0.568/0.889/0.885 mm) and one 0.732 mm VSYS remnant; the two dangling vias remain on D4 DIN. Front `B−` overlaps D9 pads and R21/R22 text overlaps neighboring pull-up pads; these can be clipped by fabrication. **Fix:** preserve unambiguous battery/load-cell labels, remove unnecessary copper stubs where authorized, and inspect affected text layers before order. The two library aliases are Rust_Board/J2 and PCM_Espressif/U1; embedded pads are present and match baseline, so this is not evidence of missing physical pads. Avoid a blind library refresh.

**W7. Fab constraints and old DFM notes need reconciliation.** Current minimum via is 0.50/0.30 mm, giving a **0.10 mm nominal annular ring**; default netclass vias are 0.60/0.30 mm. Cable drills are **0.70 mm**, not the 0.80 mm stated in the older DFM note. Default net clearance is 0.20 mm, although the global minimum clearance field is 0.00 mm. **Fix:** confirm PCBWay's actual quoted ring/drill/clearance capability for this stackup and use current geometry, not the old report's blanket dimensions. A validator's READY is not a manufacturer acceptance.

**W8. Inherited D4 voltage margin is not guaranteed by its generic datasheet.** D4 remains on +3V3 with the same pin polarity as v2.0.0; the local WS2812B document does not establish 3.3 V operation. **Fix:** retain the actually validated LED variant or obtain a supplier datasheet guaranteeing the intended voltage, then test brightness/data behavior across supply and temperature. Baseline success reduces prototype risk but does not qualify arbitrary WS2812B substitutions.

### SUGGESTIONS — historical review

- Put exact orderable package/variant requirements for U3, U5, D4 and the USB-C alternate into the eventual procurement approval. Do not infer interchangeability from generic names or supplier codes.
- Remove misleading mirrored reference artwork and obsolete `hx711` naming only in an authorized cleanup session; they do not by themselves change connectivity.
- Validate I2C rise time at the selected clock rate with the new 10 kΩ pull-ups, and scope ADC supply startup. Match the firmware reference/gain/rate settings to the actual bridge.

## 5. Prototype manufacturing notes

The artifact provenance and physical-design notes below are retained from the prior review. For current DNP flags, web research and manufacturer questions, use the latest disposition above and §7; historical statements that no fresh web research occurred no longer describe this remediation. No existing manufacturing output was changed or certified.

### Existing artifact provenance — current round

All three existing deliverables predate the last board-changing commit `9de34ebd815f8ec416ca3a7e743051afaf6b82ae`. Direct `git merge-base --is-ancestor` checks confirm each commit is an ancestor of both that board commit and reviewed HEAD; a worker's “divergent/not ancestor” claim was rejected.

| Existing artifact | Last Git-modified commit | Current treatment |
|---|---|---|
| `assembly/crimpdeq_bom.csv` | `a38028fbe77354ca930afe389d3d99cf16f99bfe` | Older than board; W1 and variant/package checks remain |
| `assembly/crimpdeq_cpl.csv` | `8c437a20cc4d5289e4baedc3211f046afe8683d6` | Older than board; narrow corrected rows match, full release not certified |
| `gerbers/crimpdeq.zip` | `97fa941a1fcd6b17cb636897969170cffcffdb7f` | Older than board; unverified until an authorized regeneration/comparison check |

`assembly/` also contains `_gen_bom.py`, `_gen_cpl.py`, `README.md` and a local `__pycache__/` directory. No outputs were regenerated. Age alone does not prove a BOM/CPL mismatch, but does not establish synchronized release provenance either.

### Geometry and constraints verified

- Closed 30.00 × 30.00 mm outline: four connected edges, x=127.45–157.45 and y=52.40–82.40 mm. Error-level outline, drill and configured clearance checks pass after refill.
- 55 footprints: **36 front / 19 back**. Excluding eight cable-pad entries leaves 47 component placements; J2 is hybrid SMT/THT, not a purely SMT assembly.
- L2/In1.Cu has **zero tracks**, one contiguous filled GND outline and normal antipads; it is not a solid copper sheet at non-GND vias/holes. Sampling AIN0/AIN1 centerlines and trace edges every ≤0.05 mm found no loss of L2 GND beneath either net; layer plot inspection agrees.
- AIN0 and AIN1 are each **7.338 mm, zero vias, F.Cu**. C12 bridges the inputs, R7/R8 are symmetric; lower cable-pad/filter area contains no digital routing. The former upper-region digital crossings are removed; W2 is closed.
- Thirteen dedicated GND vias; no via drill overlaps an SMD paste aperture. No physical proof of solder quality is implied.
- Buck switch node: **6.838 mm, zero vias, F.Cu**; feedback **4.847 mm, zero vias, F.Cu**. U6/L1/C15/C17 and R15/R16/C16 form a compact upper-board cluster. Divider 100 kΩ/22.1 kΩ and 22 pF feed-forward capacitor agree with the SY8088 3.3 V example. Efficiency, switching noise and transient response remain hardware tests.
- Antenna footprint keepout bounds are approximately x=135.2–148.4, y=47.2–52.6 mm, with the antenna extending beyond the board's y=52.4 edge. No tracks/vias/pads intersect the actual antenna region. The board-level four-copper-layer keepout x=134.8–148.7, y=52.4–53.4 blocks tracks/vias/fill; interior fill sampling and plots show the corresponding notch on inner layers. This larger guard strip permits pads and includes module GND pads outside the actual antenna region; do not misclassify them as antenna copper violations. Keep metal/enclosure/battery away from the antenna in the product.

### Assembly and narrow intentional-item dispositions

- **Antenna overhang — accepted mechanical intent:** places the radiating section beyond the host-board edge; RF clearance and enclosure performance still require hardware validation.
- **USB body overhang — accepted mechanical intent:** connector mating mouth must remain accessible at the board edge; confirm enclosure and panel fixture clearance.
- **J2 internal pad-to-NPTH clearance — accepted only within the existing scoped rule:** 0.15 mm is applied only when both items belong to J2, following the intended manufacturer footprint; other holes retain the board's 0.25 mm rule. This does not waive unrelated copper/drill conflicts.
- **Cable-pad non-placement — accepted assembly intent, not a claim that DNP flags pass:** J5–J12 are bare wire terminals and the existing BOM explicitly says Do Not Place; W1 must reconcile source/CPL handling before order.

J2 has four **plated shell slots**: S1/S4 drill 0.65 × 1.70 mm in 1.05 × 2.10 mm pads; S2/S3 drill 0.65 × 1.40 mm in 1.00 × 2.00 mm pads. These are separate from the two **0.65 mm NPTH locating holes**. PCBWay must quote plated slots and shell-tab soldering; do not turn shell tabs into NPTH features. Cable pads have 1.50 mm copper / 0.70 mm plated drills. Confirm wire gauge, strain relief and whether cable attachment is included in the assembly service.

Final cable mapping: **J5 B−=GND; J7 B+=+BATT; J6 SW+=+BATT; J8 SW−=SW_BATT; J9 A+; J10 A−; J11 E+=+3V3; J12 E−=GND.** No signal polarity reversal was found, but connector form and excitation source differ from baseline.

PCBWay must confirm double-sided reflow/handling, bottom U1 and D4 support, hybrid J2 soldering, minimum annular ring, and any panel rails/support needed by the overhangs. No fresh manufacturer web-DFM, stackup impedance certification, component stock check, or validation of the existing Gerber ZIP was performed. Those are order-stage requirements, not implied passes.

## 6. Residual risk that only hardware can prove

With C1/C2 fixed, this still remains a prototype:

1. **Power:** USB/battery startup and switchover, no backfeed, charger termination/current, 3V3 monotonic ramp and load transients, buck thermal margin and supply noise.
2. **USB:** both plug orientations, enumeration/reconnect, sustained traffic, ESD behavior, cable sensitivity and waveform quality; equal stored segment totals are insufficient.
3. **ADS1220:** physical validation was not run in this session because no assembled board, bridge/load-cell fixture, capture instrument or configured firmware test setup was available. The required test remains register readback, correct SPI mode/reference/gain, bridge common-mode/headroom, calibration/polarity, settling, effective resolution/drift and noise with Wi-Fi/BLE, USB and LED activity. HX711-era electrical validation does not prove this subsystem.
4. **Antenna:** link range and RF performance with the final battery, enclosure and user grip; a keepout check is not an RF qualification.
5. **Mechanical/assembly:** USB fit/retention, plated-slot soldering, cable insertion/strain relief, bottom-side clearances and visual/X-ray inspection as appropriate for U1/U5 hidden joints.

C1/C2, W2 and now W5 are closed; W1 source metadata is aligned. A small prototype run remains conditional on closing the decision queue and separately completing synchronized manufacturing-package checks. **NEEDS ATTENTION: this is not approval to submit the existing ZIP/BOM/CPL package.**

## 7. Decision queue — prepared, not applied or sent

### W3 — Sergio tuning decision + PCBWay stackup/impedance response

R2 measured unique routed centerline paths from U1 pad centers to each tied USB-C data pad. Lengths below are planar millimetres; via barrel lengths are excluded because an accepted stackup was not available. J2 A6/B6 are tied D+ endpoints and A7/B7 are tied D− endpoints, so there is not one orientation-independent endpoint difference.

| Net / endpoint | B.Cu | In2.Cu | F.Cu | Total |
|---|---:|---:|---:|---:|
| D+ U1.27 → J2.A6 | 1.2108 | 32.6514 | 1.3020 | 35.1643 |
| D+ U1.27 → J2.B6 | 1.2108 | 32.6514 | 1.8720 | 35.7343 |
| D− U1.26 → J2.A7 | 2.0406 | 30.6233 | 6.1378 | 38.8017 |
| D− U1.26 → J2.B7 | 2.0406 | 30.6233 | 3.3838 | 36.0477 |

D− minus D+: **A-side 3.6374 mm; B-side 0.3134 mm** (totals rounded independently). Through-route layer transitions: D+ B.Cu→In2.Cu at (136.8020,61.0260), In2.Cu→F.Cu at (146.9650,77.0322); D− at (134.2450,62.3310) and (147.6500,77.8500), respectively. Additional via taps lead to TVS branches: D+ (146.1940,72.6247)→D10.1 (146.3000,73.5000), **0.9189 mm F.Cu**; D− (141.9120,73.4517)→D7.1 (143.3000,73.5000), **1.4079 mm F.Cu**. Aggregate copper totals 37.7452/40.2096 mm include branches and must not be presented as paired endpoint paths. These measurements do not prove coupling, skew tolerance or impedance.

**Question to PCBWay (not sent):** “For this four-layer Crimpdeq board with USB_D± routed on F.Cu, In2.Cu and B.Cu using 0.20 mm traces, please supply the exact proposed production stackup: total thickness/tolerance, each core/prepreg thickness and material Dk/Df, finished copper thickness per layer, reference planes and soldermask assumptions. Please assess the actual pair spacing, transitions and TVS/USB-C branches against 90 Ω differential impedance on each routed layer; state your impedance tolerance, required width/spacing adjustments and coupon/test method. Do not assume a nominal stackup or modify routing without approval.”

**Sergio decision:** after that response, choose an explicit full-speed USB impedance/skew acceptance target and whether to authorize coupled-route tuning, preserving ESD branches and the W2 analog corridor. No tuning applied.

### W4 — Sergio approval of component substitutions/additions and qualification plan

Measured supply geometry: C11.1→U3.12 **2.9752 mm straight / 3.4699 mm routed F.Cu**; C19.1→U3.13 **2.5287 / 2.7007 mm**. C11.2→GND via (142.3500,68.8500) **0.8143 mm straight / 0.8786 mm routed**. C19.2 uses the same via: **1.7855 mm straight / 2.5857 mm routed via C11.2**. C19.2→C11.2 is 1.7071 mm; the shared C11.2→(142.1000,69.1000)→via segment is 0.8786 mm. U3 ground pads connect through filled planes rather than an explicit trace-only return to that via, so a complete loop impedance/length is not established by this measurement.

**Proposal, NOT APPLIED:** add four **47 Ω series resistors**, one each on SCK/U3.1, MOSI/U3.16, MISO/U3.15 and CS/U3.2, near U3; verify SPI timing with actual bus capacitance and edge rates. Leave unused DRDY/U3.14 NC. Specify **C12 = 100 nF, C0G/NP0, ±5%, ≥16 V**, retaining the existing 0603 footprint only if an exact qualified orderable part can meet it. Package availability is unverified; any larger footprint or capacitance change needs explicit approval, not a silent substitution. C11/C19 remain 100 nF bypass capacitors. No schematic, PCB or BOM component change was made for this proposal.

Source: TI ADS1220 datasheet §§9.1, 9.3 and 9.4 (`pcb/datasheets/ads1220.md`; https://www.ti.com/lit/ds/symlink/ads1220.pdf): 47 Ω used-digital-line guidance, high-quality differential capacitor with C0G preferred, monotonic supply ramp slower than 1 V/50 µs and approximately 50 µs wait after supplies stabilize. **Sergio approval required:** component/footprint procurement plan and separately authorized implementation. Startup scope captures and ADC noise tests at intended gain/rate, with USB/radio/LED activity, remain physical tests; geometry and DRC are insufficient.

### W7 — PCBWay process acceptance or Sergio-authorized redesign

Published research, retrieved 2026-09-09: https://www.pcbway.com/capabilities.html covers 1–14 layers and states **0.15 mm minimum annular ring**, **0.10 mm minimum spacing**, CNC/finished holes **0.15–6.0 mm**, and **PTH ±0.08 mm** tolerance; sub-0.20 mm holes incur extra charges. These are general capabilities, not a four-layer order acceptance. https://www.pcbway.com/pcb_prototype/Plated_through_slots.html explicitly supports plated slots with **0.50 mm minimum width** (NPTH slots 0.80 mm).

**Exact question to PCBWay (not sent):** “Please confirm acceptance for the quoted four-layer stackup of 0.50/0.30 mm and 0.60/0.30 mm copper/drill vias, including the **0.10 mm minimum nominal annular ring**. Your published minimum is 0.15 mm: is an explicitly approved process available, or must we redesign? Please clarify whether the 0.30 mm Excellon tool callouts are interpreted as finished plated holes and how drill compensation, registration and annular-ring tolerances are applied. Also confirm **1.50 mm copper / 0.70 mm plated cable holes**, **0.20 mm default copper clearance**, and J2 plated shell slots: S1/S4 **0.65×1.70 mm in 1.05×2.10 mm pads**, S2/S3 **0.65×1.40 mm in 1.00×2.00 mm pads**, plus two separate **0.65 mm NPTH locating holes**. Quote plated-slot fabrication and shell-tab soldering; do not convert shell slots to NPTH. State finished-hole/slot tolerances and any required geometry changes before we authorize release.”

The global minimum-clearance field remains 0.00 mm; no rules were changed. Published drill/spacing/slot capability does not override the annular-ring conflict or certify this geometry. **Sergio decision:** obtain explicit acceptance or authorize redesign; neither occurred.

### W8 — Sergio keep-or-substitute decision for D4

Actual supplier listing: https://www.lcsc.com/product-detail/LED-Indication-Discrete_Worldsemi-WS2812B-V6_C52917433.html identifies **Worldsemi WS2812B-V6, C52917433, SMD5050-4P**. Its linked eight-page datasheet was retrieved on 2026-09-09: https://datasheet.lcsc.com/datasheet/pdf/0689d8fd6dabfc7959e82552d4ffad8b.pdf?productCode=C52917433 .

The V6 feature text states **“3.3 V power supply is supported.”** This corrects the earlier absence-of-variant-evidence claim. However, its **Absolute Maximum Ratings** table gives VDD **+3.3–+5.3 V** at TA=25°C; that heading is not a guaranteed recommended operating range. Its Electrical Characteristics table is conditioned at **TA=25°C, VDD=5 V, VSS=0 V**, with VIH minimum **0.55×VDD** and maximum **VDD+0.7 V**. A guaranteed operating range and VIH test/specification at **VDD=3.3 V were NOT FOUND**; extrapolating the VIH coefficient to 3.3 V is not qualification.

**Research verdict:** positive manufacturer evidence of 3.3 V support exists for the actual V6, but full supply/temperature/data-margin guarantees remain incomplete. **Sergio decision:** keep only this exact variant with explicit prototype-risk acceptance plus supplier/manufacturer clarification and hardware tests over actual 3V3 tolerance/temperature, or authorize a substitute whose datasheet guarantees that envelope and verify package/polarity/protocol compatibility. No variant, supply or routing change applied; no supplier contacted.

### W6 — additional bounded cleanup authorization needed

The original six deletions were completed in the prior remediation. The following **four subsequently queued parent-branch items were removed in the 2026-09-10 follow-up**; this table preserves their identities rather than implying they remain on the board:

| Object / UUID | Net/layer | Geometry (mm) |
|---|---|---|
| Track `7fadb04f-5e14-45a1-b68c-e0d4993ac03f` | +3V3 / F.Cu | (143.2600,65.2556)→(140.9460,65.2556), 2.3140 mm |
| Via `ea989365-0abb-45d4-84a5-039c80940880` | +3V3 / F.Cu–B.Cu | (132.3070,72.3100) |
| Track `66885830-2dfd-4215-bd50-e0bb37166b1c` | VSYS / B.Cu | (156.6000,68.0310)→(156.3020,68.3298), 0.4220 mm |
| Track `d76388cd-6241-4c6f-af23-d25cc3d40694` | D4 DIN / B.Cu | (144.3980,64.1454)→(144.7110,63.8327), 0.4424 mm |

That four-item removal exposed **two further track segments**, both still present:

| Object / UUID | Net/layer | Geometry (mm) |
|---|---|---|
| Track `05c0f8db-81c9-46db-8811-81c49e629dc4` | +3V3 / F.Cu | (145.8860,67.8825)→(143.2600,65.2556), 3.7144 mm; starts at a surviving route junction |
| Track `a88de2d6-3049-4fa2-aba5-665c74d45e23` | D4 DIN / B.Cu | (144.7110,63.8327)→(146.8430,63.8327), 2.1320 mm; ends at a surviving via |

**Sergio decision:** authorize a bounded inspection/removal of these two remaining spur segments and explicitly define whether any further exposed terminal objects may be included, or disposition them as retained. Confirm complete branch endpoints/connectivity before any further removal rather than silently expanding the four-item scope. These two tracks were not removed or suppressed here. The 39 footprint mismatches and two aliases retain the written no-refresh disposition in §4 and require deliberate release review, not blind library updates.

**Release boundary:** no questions above have been sent. BOM/CPL/Gerber regeneration and review remain a separate authorized release step, including removing/explicitly excluding all eight bare cable-pad placements. Until the decision queue closes, the verdict stays **NEEDS ATTENTION**. Tool PASS is not analog noise qualification, manufacturer acceptance, certification of existing deliverables, or permission to order.
