# USB signal integrity actions

Keep the USB pair parallel and matched over a continuous reference, with short transitions and nearby return vias. The saved board has no dielectric stackup, so geometry alone cannot prove 90 Ω differential impedance.

Obtain four-layer dielectric and copper thicknesses, Dk/Df, tolerances, stackup-based width/spacing calculations, and coupon or impedance-test terms. Review connector transitions, via barrels, spacing changes, and ESD branches against the calculated target.

Earlier planar endpoint skews were 0.6494 mm and 2.6746 mm; via barrels were excluded, and these values are not qualification limits. Test both plug orientations, enumeration/reconnect, sustained traffic, cable sensitivity, waveform quality, and intended ESD behavior.

Reference: [Espressif ESP32-C3 PCB guidance](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c3/pcb-layout-design.html).
