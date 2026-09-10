# Release verification and prototype actions

After any approved source edit, reopen the canonical project, refill zones, inspect affected copper and artwork, and run all-severity ERC, DRC with schematic parity, and `tools/crimpdeq/verify.py`. Record ignored checks, effective clearances, warnings, source hashes, and output hashes in a dated release manifest.

The remaining D4 DIN track and historical dangling-track findings require an explicit connectivity disposition before release. Do not recursively remove newly exposed objects.

Define numerical limits before calling tests pass: rail droop/ripple, settling, ADC input-referred noise and drift, USB reliability, LED behavior, temperature, and transient/injection limits. Record firmware revision, fixture, settings, and captures.

Test power startup/back-power, USB orientations and reconnects, LED envelope/timing, physical cable and connector fit, hidden joints, enclosure clearance, and antenna performance with the final battery and enclosure. Reconcile stale DFM dimensions, placement counts, GND-via counts, and obsolete HX711 wording at release.
