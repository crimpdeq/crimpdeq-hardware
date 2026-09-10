# Manufacturing and assembly actions

## Fabrication

The three 0.50/0.30 mm vias are structurally identical to the successfully manufactured [PR #23](https://github.com/crimpdeq/crimpdeq-pcb/pull/23), including J2 drill and slot geometry. The previous fabrication conflict is therefore closed for this revision. Retain the order-specific review of finished-hole interpretation, plating, cable holes, shell slots, NPTH locators, copper clearance, and edge clearance before release.

## Component approval

Confirm manufacturer MPN, package, polarity, temperature suitability, and availability for U3, U5, D4, J2, and any USB-C alternate. Reconcile schematic placeholders, generator overrides, and supplier codes.

## Assembly process

Obtain assembler acceptance for double-sided reflow, bottom-side support, U1/D4 hidden joints, J2 SMT contacts and plated shell tabs, overhang, panel clearance, and inspection. J5–J12 remain bare cable pads and Do Not Place. Confirm cable gauge, soldering, strain relief, polarity, and the 47-placement centroid/rotation preview.

## D4

D4 remains unchanged. Its WS2812B specification, footprint, +3V3 supply, and four-pad mapping match published v2.0.0, which has reported successful operation. The exact purchased LED suffix is still not encoded; qualify the selected variant on assembled prototypes.
