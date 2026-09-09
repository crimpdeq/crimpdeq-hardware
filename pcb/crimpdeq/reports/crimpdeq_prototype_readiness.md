# Crimpdeq prototype readiness review

## 1. Ver: NEEDS ATTENTION

**The two CRITICAL blockers C1/C2 are resolved.** This is a prototype assessment, not a production qualification or approval of the existing fabrication package.

**Canonical saved-fill DRC, ERC, explicit error-level schematic parity, and `verify.py` pass.** C12/R7/R8 CPL positions now match the live board; the board was refilled and saved through Konnect IPC. Only cached zone-fill polygons changed in the PCB; routing, placement, pad nets and other design content are unchanged.

**Next action:** resolve or explicitly disposition W1–W8, particularly assembly metadata and analog/USB layout concerns, then prepare and check one synchronized manufacturing package under separate authorization. The blocker-fix request was applied only to C1/C2: three existing CPL rows were corrected; no BOM or Gerbers were generated or changed.

### Reviewed identity and scope

- Review date: 2026-09-08; KiCad CLI/Python 10.0.6.
- Working tree: `/home/sergio/Documents/Crimpdeq/crimpdeq-pcb`.
- Canonical project: `pcb/crimpdeq/crimpdeq.kicad_pro`.
- Branch: `feat/ads1220`; HEAD: `554dbfe7dfcd972b2a8799a22fa54f7b5a465613`.
- Trusted manufactured baseline: `v2.0.0`, commit `4976be254f64bac70d162865ef47e0bbe7e2f28b`.
- Konnect confirmed the canonical board is the single board open over IPC. Its component listing agrees with the inspected placements. This report certifies the saved working-tree revision, not arbitrary unsaved editor changes.
- HEAD and v2.0.0 were exported into `/tmp/crimpdeq-review-refjLB/{current,baseline}`. The working tree had no tracked modifications when exported. No live PCB/schematic git diff was used.
- Original review: the user authorized temporary-copy CLI/API validation to fill Konnect capability gaps. Refills then occurred only on the temporary board; canonical source hashes remained unchanged.
- Subsequent blocker-fix authorization: canonical zones were refilled and saved through Konnect IPC, three existing CPL rows were corrected, and this report was updated. No schematic, project rules, libraries, BOM or Gerbers were changed. Backups and verification evidence are under `/tmp/crimpdeq-blockers-cgLHpp`. The pre-existing staged report was preserved in the index; follow-up edits were not staged.

## 2. Coverage

The original Konnect refill/parity coverage gap is resolved by the authorized isolated CLI workflow. All eight requested check categories were exercised. Konnect's consolidated review reported complete coverage, with no unresolved symbols or audit failures; its heuristic findings were investigated rather than accepted as a final verdict.

| Check / tool | Result and interpretation |
|---|---|
| `list_toolboxes`, `get_project_info`, `open_project` | PASS: correct canonical project and live board confirmed |
| User/project/effective configuration | PCBWay, four layers; preferred 0.15 mm trace/clearance, 0.30 mm drill; no project overrides |
| `find_orphan_items` | PASS: zero orphans |
| `find_shorted_nets` | PASS: zero shorts |
| `find_single_pin_nets` | Three heuristic hits: Buck_Coil, ENABLE, CHIP_PU; actual connected pad counts are 2, 2, 3, respectively. Not single-pin electrical nets |
| Konnect `run_erc`, errors only | PASS: zero errors |
| CLI DRC, refill + save temporary board + schematic parity + errors only | PASS: exit 0, zero violations, zero unconnected items, zero error-severity parity findings |
| Additional CLI all-severity DRC + parity | 84 board warnings and 10 schematic-parity warnings; no errors or unconnected items |
| `tools/crimpdeq/verify.py` on refilled copy | PASS: 55 components, 172 connected named pads, 12 GND stitching vias; golden pin nets, unique symbol paths, component-side package geometry, outline, no L2 tracks, no via drill/paste overlap and route limits pass |
| Konnect `run_design_review` | Complete: one sheet, 112/112 symbols resolved, 55 footprints, 213 physical pads. Automated verdict NOT READY from two duplicate J2 decoupling heuristics; see adjudication below |
| Konnect `validate_for_manufacturing(fab_house='pcbway')` | Automated READY, zero issues, four layers. Does not certify existing CPL, part selection or analog performance |
| Konnect `audit_manufacturing`, `get_design_rules` | Completed; double-sided assembly and three cross-side proximity heuristics investigated |
| Konnect netlist export, isolated CLI XML netlists + read-only KiCad APIs | Compared all 43 shared schematic references and their PCB pad assignments, side, rotation and side-normalized pad geometry; details in §3 |
| Current schematic-to-board endpoint-set comparison | PASS: all 32 multi-pad electrical net endpoint sets match exactly, independent of names. This resolves the electrical meaning of the reported net-name conflicts, not their metadata inconsistency |
| Layout/DFM inspection | Four copper-layer Konnect SVG plots inspected; API checks of zones, analog reference coverage, digital crossings, dimensions, drills, rings, DNP and package pads completed |
| Existing BOM/CPL and DFM notes | Original review found obsolete analog CPL positions; follow-up corrected only C12/R7/R8. BOM and DFM notes unchanged. Existing Gerber ZIP not certified or regenerated |
| Blocker-fix validation | Canonical saved-fill Konnect DRC: zero errors/unconnected items without another refill; ERC zero errors; canonical `verify.py` PASS. Explicit all-severity parity on a copy of the newly saved board: unchanged 84 board warnings + 10 parity warnings, zero errors |
| Change-scope verification | Parsed before/after board structures match when cached `filled_polygon` nodes and serialization ordering are excluded. CPL retains all 55 rows and changes exactly C12/R7/R8; coordinates/angles agree with post-save live Konnect queries |

### Reproducible isolated checks

With `T` pointing to the isolated review directory:

```sh
B="$T/current/pcb/crimpdeq/crimpdeq.kicad_pcb"
kicad-cli pcb drc --refill-zones --save-board --schematic-parity \
  --severity-error --exit-code-violations --format json \
  --output "$T/drc-errors.json" "$B"
/usr/bin/python3 tools/crimpdeq/verify.py "$B"
kicad-cli pcb drc --schematic-parity --severity-all --format json \
  --output "$T/drc-all.json" "$B"
```

ERC and first netlists were obtained through Konnect. XML netlists were subsequently exported with `kicad-cli sch export netlist --format kicadxml` because the Konnect interface did not expose that comparison format. Netlists and plots were inspection artifacts under `/tmp`, not manufacturing deliverables.

**Important limitations:** error-only parity hides warning-severity net conflicts. Existing project settings also ignore `missing_courtyard`, `track_not_centered_on_via`, `tuning_profile_track_geometries`, `footprint_filters_mismatch`, and `footprint_type_mismatch`; this review changed no severities or exclusions. In particular, a DRC pass does not validate USB tuning geometry. `verify.py` does not itself prove antenna clearance or absence of digital routing beneath analog inputs; the supplementary geometry/plot checks address those topics. These checks are not electromagnetic simulation or PCBWay process approval.

### Automated audit adjudication

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

A format-aware before/after comparison confirms that only cached filled polygons changed in the PCB, aside from serialization ordering. No tracks, vias, pads, footprints, zone definitions, net assignments or rules were changed. The existing Gerber ZIP remains unchanged and **is not certified as representing these new saved fills**; preparing and checking a synchronized fabrication package remains a separate release action.

### WARNING — resolve or explicitly disposition before ordering

**W1. R7/R8 part selection and J5–J12 DNP intent disagree across sources.** R7/R8 schematic Value is `100R 1%`, but LCSC is `C25741`, also used by the 100 kΩ R9/R15 line. Their AssemblyNote explicitly prohibits 100 kΩ. Existing BOM correctly uses `C25076` for 100 Ω, so this is a source-of-truth conflict, not a claim that the existing BOM specifies the wrong value. J5–J12 have PCB DNP=false and attributes=0, and remain in the CPL; the existing BOM explicitly says Do Not Place. **Fix:** make source metadata and eventual assembly files agree; PCBWay must treat those eight entries as bare cable pads, not buy/place connectors. Do not regenerate BOM blindly from current fields.

**W2. Digital routing enters the projected ADS1220 input region.** No digital tracks enter the lower filter/cable region x=128–140, y=74–81.9 mm. However, near U3, USB_D+/USB_D− on L3 and IO3_CS on B.Cu cross beneath AIN traces: AIN0 at x=138.28 intersects their projections near y=70.40, 70.85 and 70.9141 mm; AIN1 is also crossed. L2 GND separates these layers and is intact under the analog copper, reducing coupling, but the stated “digital nets kept off the analog region” constraint is not fully satisfied. **Fix:** move those digital paths outside the projected analog corridor in an authorized layout pass, or obtain an explicit prototype-only design-constraint exception with radio/USB/ADC noise tests. No exception is granted by this report.

**W3. USB aggregate length equality is not proof of a well-routed matched pair.** Both nets use 0.20 mm tracks and three vias, with total segment lengths approximately 41.499 mm each. However, USB_D+ on In2.Cu contains overlapping collinear segments `(148.550,73.400)→(146.965,73.400)` and `(146.965,73.400)→(148.548,73.400)`, overlapping for **1.583 mm**. Summing both counts the same copper twice; the near-joined vertical runs at x=148.550/148.548 also bypass that out-and-back excursion electrically. TVS branches further complicate delay comparison. Plots show separated routing and rectangular detours, not uniform pair coupling. **Fix:** inspect/remove the redundant excursion and route/check actual U1-to-J2 paths as a pair, preserving ESD branches; obtain PCBWay's stackup before claiming 90 Ω. Full-speed USB may tolerate this, but a numeric total-length match is not a validation.

**W4. New ADC bypass and interface implementation carry noise/startup risk.** C19's supply pad is about 2.96 mm straight-line from DVDD; C11's is about 4.14 mm from AVDD. Actual current-loop lengths can be longer; 100 nF connectivity alone does not establish optimal bypassing. There are no TI-recommended 47 Ω SPI series resistors. C12 dielectric is unspecified and its simple RC pole is relatively high. **Fix:** confirm actual AVDD/DVDD return paths, selected MLCC dielectric and supply ramp; consider closer bypassing and damping/filter footprints in a separately authorized revision. Test at intended gain/rate with USB and radio activity. TI requires monotonic supply ramp slower than 1 V per 50 µs and approximately 50 µs settling before communication; that is not proven by static checks.

**W5. Ten warning-level parity findings remain.** Five pad-net name conflicts are limited to L1.1/U6.3 (`Buck_Coil` versus `/Buck_Coil`) and C12.1/R7.1/U3.11 (`Net-(U3-AIN0)` versus the schematic AIN0/REFP1 auto-name). Three footprint-ID warnings concern C11/C19/U3; two datasheet-field differences concern Q2/U5. All 32 multi-pad endpoint sets match, so no extra electrical connection is inferred from these warnings. **Fix:** synchronize metadata carefully without moving copper or changing pad endpoints; rerun all-severity parity. An error-only pass is not metadata parity.

**W6. Silkscreen and dangling copper need cleanup/disposition.** The 84 board warnings comprise 24 mirrored/nonmirrored texts, five silk overlaps, five silk-on-copper, 39 footprint-library mismatches, two unavailable library aliases, seven dangling tracks and two dangling vias. Front `B−` overlaps D9 pads and R21/R22 text overlaps neighboring pull-up pads; these can be clipped by fabrication. Dangling traces include a roughly 2.04 mm IO5_SCK stub, plus +3V3/VSYS remnants; the dangling vias are on D4 DIN. **Fix:** preserve unambiguous battery/load-cell labels, remove unnecessary copper stubs where authorized, and inspect affected text layers before order. The two library aliases are Rust_Board/J2 and PCM_Espressif/U1; embedded pads are present and match baseline, so this is not evidence of missing physical pads. Avoid a blind library refresh.

**W7. Fab constraints and old DFM notes need reconciliation.** Current minimum via is 0.50/0.30 mm, giving a **0.10 mm nominal annular ring**; default netclass vias are 0.60/0.30 mm. Cable drills are **0.70 mm**, not the 0.80 mm stated in the older DFM note. Default net clearance is 0.20 mm, although the global minimum clearance field is 0.00 mm. **Fix:** confirm PCBWay's actual quoted ring/drill/clearance capability for this stackup and use current geometry, not the old report's blanket dimensions. A validator's READY is not a manufacturer acceptance.

**W8. Inherited D4 voltage margin is not guaranteed by its generic datasheet.** D4 remains on +3V3 with the same pin polarity as v2.0.0; the local WS2812B document does not establish 3.3 V operation. **Fix:** retain the actually validated LED variant or obtain a supplier datasheet guaranteeing the intended voltage, then test brightness/data behavior across supply and temperature. Baseline success reduces prototype risk but does not qualify arbitrary WS2812B substitutions.

### SUGGESTIONS

- Put exact orderable package/variant requirements for U3, U5, D4 and the USB-C alternate into the eventual procurement approval. Do not infer interchangeability from generic names or supplier codes.
- Remove misleading mirrored reference artwork and obsolete `hx711` naming only in an authorized cleanup session; they do not by themselves change connectivity.
- Validate I2C rise time at the selected clock rate with the new 10 kΩ pull-ups, and scope ADC supply startup. Match the firmware reference/gain/rate settings to the actual bridge.

## 5. Prototype manufacturing notes

### Geometry and constraints verified

- Closed 30.00 × 30.00 mm outline: four connected edges, x=127.45–157.45 and y=52.40–82.40 mm. Error-level outline, drill and configured clearance checks pass after refill.
- 55 footprints: **36 front / 19 back**. Excluding eight cable-pad entries leaves 47 component placements; J2 is hybrid SMT/THT, not a purely SMT assembly.
- L2/In1.Cu has **zero tracks**, one contiguous filled GND outline and normal antipads; it is not a solid copper sheet at non-GND vias/holes. Sampling AIN0/AIN1 centerlines and trace edges every ≤0.05 mm found no loss of L2 GND beneath either net; layer plot inspection agrees.
- AIN0 and AIN1 are each **7.338 mm, zero vias, F.Cu**. C12 bridges the inputs, R7/R8 are symmetric; lower cable-pad/filter area contains no digital routing. The upper-region digital crossings remain W2.
- Twelve dedicated GND vias; no via drill overlaps an SMD paste aperture. No physical proof of solder quality is implied.
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
3. **ADS1220:** register readback, correct SPI mode/reference/gain, bridge common-mode/headroom, calibration/polarity, settling, effective resolution/drift and noise with Wi-Fi/BLE, USB and LED activity. HX711-era electrical validation does not prove this subsystem.
4. **Antenna:** link range and RF performance with the final battery, enclosure and user grip; a keepout check is not an RF qualification.
5. **Mechanical/assembly:** USB fit/retention, plated-slot soldering, cable insertion/strain relief, bottom-side clearances and visual/X-ray inspection as appropriate for U1/U5 hidden joints.

C1/C2 are closed. A small prototype run is reasonable after the remaining warning dispositions and final synchronized manufacturing-package checks are complete. **NEEDS ATTENTION: this is not yet approval to submit the existing ZIP/BOM/CPL package.**
