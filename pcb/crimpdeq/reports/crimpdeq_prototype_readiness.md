# Crimpdeq prototype manufacturing readiness

Review date: 2026-09-08 (fresh checks; supersedes the previous local report).

- Target: **PCBWay, four-layer, double-sided SMT plus limited THT**, small prototype, not production release.
- Reviewed source: `feat/ads1220`, starting commit `a38028fbe77354ca930afe389d3d99cf16f99bfe`, canonical `pcb/crimpdeq/`. During review HEAD advanced to documentation-only commit `1bdaca77dd544c6466c9de82212947f6dd0084a7`; protected design-file hashes remained unchanged.
- Trusted connectivity baseline: [v2.0.0](https://github.com/crimpdeq/crimpdeq-pcb/releases/tag/v2.0.0), commit `66f672d2e5675e2a716527d34c7a7d6b512641fe`. Its manufactured/electrically working status is supplied by the owner.
- Scope: inspection and report only. No KiCad source, libraries, rules, Gerbers, BOM/CPL, or other manufacturing outputs changed/generated. Temporary netlists and SVG inspection plots were used; no live schematic/PCB Git diff was taken.

## 1. Verdict

**INCOMPLETE — review could not evaluate the full design.**

**Do not treat this report as approval to send the board to fabrication.** Error-level ERC, refilled DRC with schematic parity, and the repository verifier pass. No confirmed critical electrical regression was found in the completed checks. Nevertheless:

1. The required **complete baseline footprint-side/pad-geometry comparison remains unfinished**. Konnect `get_component_list` rejected the baseline board because it was not open in the PCB editor. `launch_kicad_ui` reported launch success but subsequent `open_project` still listed only the current board. Baseline fabrication-layer SVGs cover 37 of 43 shared references; six have no identifying fabrication-layer text. This gap must not be converted into a pass.
2. The current AIN routing is not symmetric, digital routing enters its region, and USB is not a consistently coupled pair. These are design-constraint warnings, not automatically waived because the older design worked.
3. The assembler must accept the actual drill/annular-ring geometry, assembly sides, package orientations, DNP instructions and connector exceptions.

**Next action:** open the v2.0.0 board in KiCad's PCB editor for Konnect inspection, complete the physical baseline comparison, and disposition the warnings below. Preserve the current board without saving any inspection-induced changes. A later manufacturing-package preparation/check is a separate task. The baseline inspection worktree is at `/tmp/crimpdeq-prototype-review-docs/pcb/crimpdeq/crimpdeq.kicad_pcb`.

## 2. Coverage

### Checks run

| Check | Result | Evidence / scope |
|---|---|---|
| `list_toolboxes` | Available | 217 tools advertised. `get_installation_info` is not a required tool; earlier stops on that name were mistaken. |
| `get_project_info`, `open_project` | Confirmed | Exact open board: `/Users/sergio/Documents/Crimpdeq/crimpdeq-pcb/pcb/crimpdeq/crimpdeq.kicad_pcb`; IPC responsive. |
| User/project/effective configuration | Read | Defaults still say JLCPCB/two layers. This review explicitly used **pcbway** and the actual four-layer board, without changing configuration. |
| `get_board_info`, `get_component_list`, pad queries | Completed for current board | Revision 3.0; 55 footprints, 36 front / 19 back; 57 named board nets including no-connect nets. |
| `find_orphan_items` | Pass | 0 orphans. |
| `find_shorted_nets` | Pass | 0 shorts. |
| `find_single_pin_nets` | Three heuristic reports, resolved | `ENABLE` = R14.2/U6.1; `Buck_Coil` = L1.1/U6.3; `CHIP_PU` = C3.1/R1.2/U1.8. Each has multiple connected pins; single label count is not single-pin connectivity. |
| Konnect `run_erc(severity="error")` | Pass | 0 errors. |
| Konnect `run_drc(severity="error")` | Pass | 0 errors, 0 unconnected items, 0 schematic-parity findings. 84 warning-level findings remain. |
| Explicit refilled/parity DRC | Pass | Repository CLI command below: 0 violations, 0 unconnected items, 0 schematic-parity issues. |
| `tools/crimpdeq/verify.py` | Pass | 55 components; 172 connected named pads; 12 GND vias; no via-drill/paste overlap; checked package geometry and route limits pass. |
| `run_design_review` | Tool coverage complete, canned verdict NOT READY | One sheet, 112/112 resolved symbol instances; 55 footprints/213 pads; diagnostics empty. Two error-severity J2 decoupling heuristics are assessed below rather than silently suppressed. |
| `validate_for_manufacturing(fab_house="pcbway")` | Tool verdict READY | 0 reported issues; 55 footprints, four copper layers, 598 track/via items. This limited tool verdict does not close the baseline or SI/analog-layout gaps. |
| `audit_manufacturing(fab_house="pcbway")` | Completed | Double-sided assembly information and three opposite-side XY proximity warnings. |
| Both schematic netlists via `generate_netlist` | Compared | All 43 common references; 181 pin positions in their combined pin sets, including added U1 grounds and explicit no-connects. |
| Current `query_traces` and four copper-layer SVGs | Inspected | L2 has no track segments; saved L2 pour appears continuous through the analog region, apart from normal hole/via clearances. Analog, digital and USB routes assessed below. |
| Outline / drills / silk | Inspected | Four Edge.Cuts lines, 30.00 × 30.00 mm nominal outline; actual-size SVG pad/hole geometry and DRC warning records reviewed. |
| DNP / assembly data | Existing files read only | Existing BOM marks J5–J12 Do Not Place and J2 Hybrid/THT. No existing package is certified current by this review. |
| v2.0.0 placed-footprint inspection | **Incomplete** | Baseline board not accessible through live IPC; exact physical pad/polarity/rotation comparison not completed. |

The Konnect DRC interface exposes no explicit refill/parity switches. To remove ambiguity without altering the saved design, the expressly permitted repository CLI check was also run:

```sh
kicad-cli pcb drc --refill-zones --severity-error --schematic-parity \
  --output /tmp/crimpdeq-prototype-review-evidence/drc-refilled.txt \
  pcb/crimpdeq/crimpdeq.kicad_pcb

/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 \
  tools/crimpdeq/verify.py pcb/crimpdeq/crimpdeq.kicad_pcb
```

The verifier printed a wx initialization diagnostic but completed successfully. KiCad CLI identified itself as 10.0.6. SHA-256 checks confirmed the protected design files remained unchanged after checks.

### Important limits of the checks

- The consolidated Konnect audit's `complete` status means its built-in audits completed, **not** that every additional owner-requested comparison has completed.
- `verify.py` does **not** inspect antenna keepout polygons, GND-pour net/continuity, differential symmetry, digital/analog separation, USB impedance/matching, or DNP flags. It counts GND vias, not whether every one is dedicated stitching. It checks U3 value/footprint family and nets, but **not** U3's detailed package coordinates/rotation. U3 was therefore checked separately through IPC against the datasheet.
- Copper plots provide visual evidence of the current antenna copper exclusion and analog reference plane; they do not independently prove all keepout-object flags or exact RF clearance compliance. Do not add GND under the antenna to satisfy an ambiguous “unbroken plane” instruction: the antenna area must remain copper-free.
- Six shared refs lack confirmed baseline-side identification: **D2, D3, D7, D9, D10, J2**. The other 37 have identifying text on the baseline F.Fab export. B.Fab contained no identifying refdes text; absence of text alone does not prove side.
- PCBWay web DFM, stackup/impedance agreement, component availability and assembler preview were not performed. There was no electrical, RF, fit or hardware test in this review.
- A read-only firmware spot-check used `crimpdeq-firmware` commit `fd330fde885ccdfcae6120a7fc986ab918ec04f3`; it was not a full firmware review or build.

### Layout constraints and buck measurements

- **U6/L1 switch node:** `Buck_Coil` = 6.838 mm, F.Cu, zero vias (verifier ceiling 7 mm).
- **U6/R15/R16/C16 feedback:** `Net-(U6-FB)` = 4.847 mm, F.Cu, zero vias (ceiling 8 mm).
- U6, C15, L1 and C17 form the front-side supply cluster; no new buck connectivity discrepancy was found. These route-length checks do not measure switching-loop inductance or qualify stability under load.
- **AIN0/AIN1:** F.Cu, zero vias, but asymmetric; W1 remains open.
- **L2:** zero track segments and visually continuous saved ground pour through the analog region; normal via antipads remain. Exact all-layer antenna keepout flags and proof that all 12 GND vias are dedicated stitching remain coverage limits.
- **Digital separation / USB pair:** not satisfied by the inspected routing; see W2/W3.

### DRC warnings: all 84 accounted for

| Rule | Count | Disposition |
|---|---:|---|
| `lib_footprint_mismatch` | 39 | Placed/library copies differ; do not assume every difference is cosmetic. No refresh applied. |
| `lib_footprint_issues` | 2 | Missing configured libraries `Rust_Board` (J2) and `PCM_Espressif` (U1). |
| `track_dangling` | 7 | Five +3V3 ends, one VSYS end, one IO5_SCK end. No unrouted required connection reported, but stubs deserve cleanup/review. |
| `via_dangling` | 2 | `Net-(D4-DIN)` at (144.398, 64.1454) and (130.103, 55.2355) mm. |
| `silk_overlap` | 5 | R20/R21/R22, E+/E− markings, U3. |
| `silk_over_copper` | 5 | R21/R22 reference text and B− marking over D9 pads. |
| Mirrored front / nonmirrored back text | 12 + 12 | Assembly/fabrication text orientation needs preview review; not a demonstrated copper fault. |

## 3. Delta vs v2.0.0

### Method and unchanged-and-matching references

Konnect exported both schematic netlists; a temporary parser compared every shared reference's numbered pin assignments, no-connect state, value and schematic footprint ID. Leading sheet-path `/` on local net names and generated names of explicitly unconnected pins were normalized. Identical net names do not imply identical routing or unchanged loading.

Baseline: **46 components**. Current: **55**. Common: **43**. The following **36 references / 102 pin assignments** match, including pin-specific power/ground and diode/MOSFET polarity assignments:

| Group | Every matching reference |
|---|---|
| Capacitors | C1, C2, C3, C4, C5, C6, C9, C15, C16, C17, C18 |
| Diodes / LED | D1, D2, D3, D4, D7, D8, D9, D10 |
| Connector / inductor / MOSFET | J2, L1, Q2 |
| Resistors | R1, R2, R3, R9, R13, R14, R15, R16, R17, R18, R19 |
| ICs | U2, U5, U6 |

Their schematic values and footprint IDs also match. This preserves the trusted connectivity reference, **not** proof of current placed-pad geometry, revised layout performance, or a supplier substitution.

### Changed-and-risky references: all seven

| Reference / pin | v2.0.0 → current | Assessment |
|---|---|---|
| C10.1 | `E+` → `+3V3` | Excitation rail changed to direct 3.3 V; C10.2 stays GND. |
| C11.1 / C11.2 | GND / `Net-(U3-VBG)` → +3V3 / GND | Repurposed as supply bypass; nonpolar capacitor, not a reversed polarized part. |
| C12.1 / R7.1 | `Net-(U3-INA+)` → ADS1220 AIN0/REFP1 node | New ADC input function. R7.2 stays A+. |
| C12.2 / R8.1 | `Net-(U3-INA-)` → `Net-(U3-AIN1)` | New ADC input function. R8.2 stays A−. |
| U1.6, GPIO3 | Explicit NC → `IO3_CS` | New chip select. |
| U1.13, GPIO1 | Explicit NC → `IO1_MISO` | New ADC output input. |
| U1.18, GPIO4 | `IO4_DATA` → `IO4_MOSI` | Former HX711 output connection becomes ADS1220 DIN; direction/function changed. |
| U1.37–53 | Absent from baseline schematic netlist → GND | Newly represented grounds. Espressif Table 3-1 specifies GND for pins 36–53. Do not call these baseline-proven schematic connections. |
| U3 | HX711 SOP-16 → ADS1220 TSSOP-16 | Entire device and pin-function mapping replaced; table below covers all 16 pins. |

U1's remaining pin assignments/no-connect states match. In particular GPIO5/U1.19 retains `IO5_SCK`, but its endpoint changes from HX711 U3.11 to ADS1220 U3.1. GPIO6/U1.20, GPIO7/U1.21 and GPIO10/U1.16 retain the gauge nets; GPIO18/U1.26 and GPIO19/U1.27 retain USB D− and D+. I2C and ALERT loading changes because R20–R22 were added.

Schematic AIN0's generated name is `Net-(U3-AIN0{slash}REFP1)`; the board uses `Net-(U3-AIN0)`. Endpoint identity and schematic parity agree; this spelling difference is not a short or missing connection.

### U3: complete pin comparison and datasheet check

Current TSSOP pin functions agree with `pcb/datasheets/ads1220.md`, Table 5-1. IPC shows a front-side, 0° TSSOP with 0.65 mm pitch: pin 1 at (131.3375, 66.225), pin 8 at (131.3375, 70.775), pin 9 at (137.0625, 70.775), pin 16 at (137.0625, 66.225) mm. This is the expected top-view numbering sequence.

| Pin | Old HX711 net | Current ADS1220 function → net |
|---:|---|---|
| 1 | +3V3 | SCLK → IO5_SCK |
| 2 | `Net-(Q1-B)` | /CS → IO3_CS |
| 3 | E+ | CLK → GND; internal oscillator selected physically |
| 4 | `Net-(U3-VFB)` | DGND → GND |
| 5 | GND | AVSS → GND |
| 6 | `Net-(U3-VBG)` | AIN3/REFN1 → explicit NC |
| 7 | HX711 INA− | AIN2 → explicit NC |
| 8 | HX711 INA+ | REFN0 → GND |
| 9 | GND | REFP0 → +3V3 |
| 10 | GND | AIN1 → R8.1/C12.2 |
| 11 | IO5_SCK | AIN0/REFP1 → R7.1/C12.1 |
| 12 | IO4_DATA | AVDD → +3V3 |
| 13 | Explicit NC | DVDD → +3V3 |
| 14 | GND | Dedicated /DRDY → explicit NC |
| 15 | +3V3 | DOUT//DRDY → IO1_MISO |
| 16 | +3V3 | DIN → IO4_MOSI |

Unused AIN2/AIN3 and /DRDY treatment follows datasheet §9.1.5; grounded CLK is correct. AVDD/DVDD at 3.3 V meet the 2.3–5.5 V supply range. C11 and C19 each provide nominal 100 nF to GND. Supply-pad straight-line distances are approximately 4.14 mm (U3.12–C11.1) and 2.96 mm (U3.13–C19.1), not measured loop inductances.

REFP0/+3V3 and REFN0/GND use the same nets as E+/E−: electrically ratiometric per §9.1.3/§9.2.3, but not Kelvin-sensed at a remote four-wire bridge. R7/R8 are 100 Ω and C12 is 100 nF differentially, giving approximately 7.96 kHz RC cutoff before accounting for bridge/source impedance. Common-mode RF filtering is not provided by that differential capacitor.

Firmware must select AIN0/AIN1, external REFP0/REFN0 and SPI mode 1; the SPI spot-check uses GPIO5/4/1, GPIO3 CS initially high, mode 1 at 2 MHz. This does not prove the complete register/readiness sequence. At 3.3 V and gain 128, the PGA-limited differential range is approximately ±22.66 mV, not the entire ±25.78 mV reference-derived range. Check the actual bridge sensitivity, overload and common-mode voltage before selecting gain.

### New-and-unproven parts and external wiring

Added: **C19, R20, R21, R22, J5–J12**. Removed: **Q1, R5, R6**. R20/R21/R22 are 10 kΩ pull-ups to +3V3 on IO6_SDA/IO7_SCL/IO10_ALRT respectively. Their connections pass the golden-net check; rise time and powered-off behavior remain hardware concerns.

| Bare cable pad | Current net / intended connection |
|---|---|
| J5 B− | GND |
| J6 SW+ | +BATT |
| J7 B+ | +BATT |
| J8 SW− | SW_BATT, Q2 drain |
| J9 A+ | R7.2, then U3 AIN0 |
| J10 A− | R8.2, then U3 AIN1 |
| J11 E+ | +3V3, also REFP0 |
| J12 E− | GND, also REFN0 |

J5–J12 have no same-ref schematic baseline counterpart. In particular **SW− is not GND**: the switch joins J6 to J8; battery negative goes to J5. No load-cell cable colour convention is assumed.

### Footprint-side and polarity delta

Baseline F.Fab and current IPC establish **18 front-to-back moves**: C1, C2, C3, C5, C6, C10, D1, D4, Q2, R1, R2, R3, R13, R17, R18, R19, U1, U2. These are intentional layout changes, but require a new assembly-side/orientation review, not reuse of old placement data.

The following **19 remain front** by the same evidence: C4, C9, C11, C12, C15, C16, C17, C18, D8, L1, R7, R8, R9, R14, R15, R16, U3, U5, U6. The other six baseline sides remain unconfirmed as listed in §2.

Current critical package checks:

| Ref | Current side / rotation | Current numbered-pad electrical check |
|---|---|---|
| U2 | Back / −90° | 1 STAT, 2 GND, 3 +BATT, 4 VBUS, 5 PROG; MCP73831 SOT-23-5 table agrees. |
| Q2 | Back / −90° | 1 gate=VBUS, 2 source=VSYS, 3 drain=SW_BATT; baseline pin mapping and repository geometry invariant retained. |
| D4 | Back / +90° | 1 +3V3, 2 DOUT NC, 3 GND, 4 DIN; local WS2812B pin table agrees. |
| U5 | Front / 180° | 1/4/6/9 GND, 2/3 +BATT, 5 ALERT, 7 GPIO6, 8 GPIO7; **actual I2C functions differ from schematic labels**, see W4. |
| U3 | Front / 0° | Independently checked against the TSSOP datasheet table above, not inherited from HX711. |

U2/Q2/D4/U5 current component-side geometry passes `verify.py`; that is not an exact physical delta against the original placed footprints. No confirmed netlist-level polarity reversal was found among retained polarized parts.

## 4. Findings and concrete actions

### CRITICAL

**No confirmed critical fault in completed checks.** This is not a zero-risk certification: baseline physical coverage remains incomplete. No clearance/parity violation was waived or suppressed.

### WARNING

**W1 — U3/R7/R8/C12: asymmetric analog routing.** AIN0 has 15.566 mm of total trace versus AIN1 10.978 mm, both F.Cu and zero vias. AIN0 detours east of the ADC; AIN1 runs beneath it and west toward R8. These are sums including capacitor branches, not point-to-point propagation skew. The two input paths are visibly not symmetric despite passing the 16 mm verifier ceilings. **Action:** bring the matched R7/R8/C12 network close to pins 10/11 and shorten/rebalance routing over L2 GND. Do not add serpentine solely to equalize millimetres. No prototype waiver is assumed; explicitly accept the noise risk if deferring layout work.

**W2 — IO3_CS and USB_D± enter the analog region.** CS reaches F.Cu at approximately (133.965, 69.399) mm and routes under U3; its B.Cu route crosses the analog-region projection. Both USB nets cross that region on L3. L2 between F.Cu and L3 mitigates direct coupling, but does not establish the requested digital/analog separation. **Action:** keep control routing on the digital side of U3 and move USB away from the analog input/filter region. Scope analog noise while toggling SPI/USB/BLE if accepting a prototype exception.

**W3 — J2/U1 USB_D±: uncoupled routing and unverified impedance.** Total routed copper is 28.799 mm for D+ and 31.693 mm for D−, including connector/protection branches. Both use F.Cu, B.Cu and In2.Cu; the L3 paths take different routes rather than maintaining pair spacing. Their 2.893 mm total-length difference is not a calculated receiver skew. Unchanged pin connectivity and v2.0.0 USB operation do not prove this layout. **Action:** route a consistent pair with controlled reference transitions and obtain a PCBWay stackup/90 Ω differential calculation; otherwise explicitly accept and test the prototype USB risk. No impedance certification was performed.

**W4 — U5 pin 7/8 signal names are reversed relative to the real IC.** The MAX17048 TDFN datasheet states pin 7=SCL and pin 8=SDA. Both schematic revisions instead label U5.7 `IO6_SDA` and U5.8 `IO7_SCL`. Current firmware `src/main.rs:178–190` explicitly compensates with **GPIO7=SDA, GPIO6=SCL**. This resolves the apparent fault and preserves the working baseline; it is not a reason to swap copper blindly. **Action:** retain the compensated firmware for bring-up; later correct symbol/net naming and documentation together without changing physical connectivity unintentionally. R20 actually pulls up SCL and R21 SDA. The firmware comment claiming no external ALERT pull-up is also stale now that R22 exists.

**W5 — Three vias have 0.10 mm nominal annular rings.** Actual-size Konnect SVG geometry shows 66 round vias at 0.60/0.30 mm and three at **0.50/0.30 mm**, not uniformly 0.60/0.30 as the existing DFM note claims. Smaller vias are at (138.350, 66.875), (146.200, 61.700), and (132.750, 64.250) mm; the first two terminate IO1_MISO traces. **Action:** have PCBWay approve 0.10 mm nominal rings with its drill/plating tolerances, or enlarge these pads in a separately authorized layout change. Passing the configured DRC is not manufacturer acceptance.

**W6 — R21/R22 and B− silk is clipped by solder mask.** The B− text is over D9's pads, not directly on the J5 cable pad; blindly following the marking could mislead manual wiring. R21/R22 identifiers also overlap adjacent resistor pads. **Action:** move the conflicting silk in a later authorized change, or require assembler mask clipping and use the explicit J5–J12 wiring table for this prototype. Do not print ink on exposed solder pads. E+/E− and U3 silk-to-silk warnings are readability issues, not copper shorts.

**W7 — Footprint provenance/side comparison remains open.** There are 39 placed/library mismatch warnings and missing U1/J2 library registrations; U3/C11/C19 also appear in the board list without a library nickname. A correct netlist does not rule out altered physical pad numbering. **Action:** finish the baseline placed-pad/side comparison through Konnect, especially flipped polarized packages, and approve the current assembler orientation preview. Do not bulk-refresh footprints as a way to silence warnings. The existing CPL generator deliberately adds +270° for U3 and +180° for U6 on the front, and transforms back-side rotations as `180° − board rotation`; J2 also has a body-centroid offset. The existing CPL reflects these conventions, but their acceptance by PCBWay was not verified. Explicitly approve pin-1 orientation in its preview rather than treating the generator's hard-coded expectations as independent proof.

**W8 — Procurement identifiers and D4 operating variant require confirmation.** `check_bom_health` reports missing schematic MPNs for U3/U5. The existing PCBWay BOM uses LCSC catalogue IDs (`C48263`, `C2682616`, etc.) in its MPN column, not actual manufacturer order codes. The local generic WS2812B datasheet specifies 3.5–5.3 V whereas D4 is on +3V3, unchanged from the working baseline; the selected lot/variant is not established by that earlier success. **Action:** obtain actual manufacturer ordering codes/packages and confirm PCBWay can source those exact parts, including a D4 variant suitable for 3.3 V. No stock or substitution approval is implied.

### Heuristic findings assessed, not silently waived

- **J2 VBUS decoupling (two audit “errors”):** both raw connector VBUS pads join `Net-(D8-A)`, then D8 feeds the downstream VBUS rail with C5=4.7 µF and U2.4. This numbered-pin topology matches v2.0.0. MCP73831 §3.1 specifies 4.7 µF input bypass; a heuristic requiring 100 nF on every connector pin named VBUS is not an established design fault. No critical finding assigned solely from those duplicate reports; hot-plug/inrush remains a hardware check.
- **+BATT/VBUS “no ≥10 µF” warnings:** C6/C5 each provide nominal 4.7 µF, matching MCP73831's specified bypass value and the baseline. Blanket addition of 10 µF is not justified by that heuristic; effective capacitance under bias remains relevant.
- **C18/Q2, C9/R2, C15/C5 spacing:** each is an opposite-side pair, not a same-side component-body collision. Their XY distances of 0.40/0.00/0.71 mm alone do not establish an assembly fault. Double-sided reflow, heat and rework access still need assembler approval.

### SUGGESTION

1. **Verifier coverage:** later add reusable checks for actual antenna keepout coverage, L2 net/fill continuity, analog-region digital intrusion, U3 pad geometry and DNP metadata. Do not describe these as already tested by the current verifier.
2. **SPI/analog robustness:** ADS1220 §9.1.1 recommends 47 Ω series resistors on digital I/O; none are present on the direct SPI connections. Consider them if edge ringing is measured. §9.4.1 recommends high-quality differential capacitors such as C0G; confirm C12 dielectric/microphonics rather than assuming the existing sourcing code is optimal.
3. **Routing remnants:** inspect/remove unused IO5_SCK/+3V3/VSYS stubs and the two D4-DIN dangling vias in a separate change, then refill/recheck. Do not confuse these warnings with unconnected required pins.
4. **Debug access:** designate safe probe points for +3V3, VBUS, battery and ADC signals before bring-up. Cable pads offer some access but are not a complete test strategy.

## 5. Prototype manufacturing notes

- **Layer/assembly count:** four copper layers; L2 GND has zero routed segments, L3 carries supply copper and signals. 55 footprints = 36 front / 19 back. After excluding eight bare cable pads, there are **47 component placements: 28 front / 19 back**, with J2 requiring both SMT and shell soldering.
- **DNP waiver — J5–J12:** intentional bare plated cable pads, not components; the existing assembly BOM explicitly says Do Not Place. Keep them out of placement purchasing/assembly despite their presence in the existing CPL. Native KiCad DNP metadata was not independently established by the queried tools.
- **Cable holes:** actual-size SVG shows all eight with 1.50 mm copper / **0.70 mm drill**, giving 0.40 mm nominal annular rings. This disagrees with the existing DFM Markdown's 0.80 mm drill claim. Use the actual board geometry for wire-gauge/fit approval and correct that note in a separate documentation change.
- **J2 THT:** four plated shell anchors S1–S4 connect through R17 to GND; they require THT/manual or an explicitly qualified through-hole-reflow operation. Two unnumbered mechanical holes have no assigned net. Do not order SMT-only assembly without addressing the anchors.
- **J2 clearance waiver — conditional on fab acceptance:** the existing custom rule allows 0.15 mm pad-to-hole clearance only between J2 footprint members, for the connector's mechanical geometry. This is a specific existing connector exception, not permission to reduce board-wide clearances. Obtain PCBWay acceptance.
- **U1 antenna overhang waiver:** intentional board-edge antenna placement avoids base-board copper beneath the antenna; preserve that exclusion on all four layers and keep panel rails/metal/cabling clear. Quantitative RF keepout-object verification remains limited as noted above.
- **J2 housing overhang waiver:** the documented intentional 1.00 mm housing overhang permits cable mating; do not shift the connector merely to fit its body inside Edge.Cuts. Verify the mechanical drawing, panel edge and enclosure clearance with PCBWay.
- **Rules:** retrieved board minima are 0.20 mm trace, 0.30 mm via drill, 0.50 mm via pad and 0.25 mm hole-to-hole. Default netclass clearance is 0.20 mm; the board absolute minimum clearance is 0.00 mm. This does not mean routing was assessed against zero spacing alone, but it is not a verified PCBWay capability profile either.
- **Paste:** the repository verifier reports no via drill intersecting an SMD paste aperture. This does not qualify stencil thickness, U1/U5 paste volume or double-sided reflow.
- **Ordering hold:** obtain PCBWay's four-layer stackup, annular-ring/hole tolerances, panelization/fiducial plan, dual-side SMT and limited-THT agreement, DNP confirmation, and per-part orientation preview. Do not reuse the v2.0.0 placement file.
- **Outputs:** no Gerbers, BOM/CPL or fabrication package generated. Existing archives/assembly files were not checked for complete synchronization with this reviewed commit and are not approved for submission by this report.

## 6. Residual risk that only hardware can prove

1. **Power and battery:** first power-up under current limit; check polarity, 3.3 V startup/overshoot/ripple, brownouts under radio/LED/bridge load, buck stability/temperature, charger termination and battery/USB switchover. ADS1220 §9.3.2 calls for a monotonic ramp slower than 1 V per 50 µs; actual startup was not measured. Confirm battery protection and safe wiring separately.
2. **USB:** enumeration/data integrity in both Type-C orientations, across representative cables/hosts, hot-plug behavior and ESD. Earlier USB connectivity success does not validate these new paths.
3. **ADS1220:** register readback, reset/data-ready handling, external-reference selection, gain/common-mode headroom, bridge excitation drop, input polarity, saturation, zero/load calibration and drift. Measure noise with USB, SPI, BLE and D4 activity both on and off, and with realistic cable strain/motion.
4. **Gauge:** use GPIO7=SDA/GPIO6=SCL firmware; verify ACK/readings/ALERT, rise times with the 10 kΩ pull-ups, and behavior when the 3.3 V rail is off but the battery remains connected.
5. **Antenna:** BLE range and repeatability with the real enclosure, battery, load cell, nearby metal and user's hand. Visual keepout checks do not establish RF performance.
6. **Fit and assembly:** connector mating/retention, U1/J2 overhangs, cable fit in 0.70 mm holes, solder-joint quality, strain relief, and double-sided assembly/rework yield.

The manufactured v2.0.0 is trusted for matching retained connectivity. It does **not** prove the ADS1220, the new SPI/analog/bridge implementation, added pull-ups, revised placed-pad geometry or this layout's analog/RF/USB performance.
