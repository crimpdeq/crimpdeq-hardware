# ADC, SPI, and component actions

## C12

Selected: Murata **GRM31C5C2A104JA01L**, LCSC **C405303** — 100 nF, C0G, ±5%, 100 V, 1206. Evidence: [Murata reference sheet](https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM31C5C2A104JA01-01A.pdf) and [C405303 listing](https://www.lcsc.com/product-detail/C405303.html). Preserve the 100 nF value and R7/R8 network; split C12 from the C11/C19 bypass-cap group if implemented.

## SPI damping

Proposed: four 47 Ω, 1%, 0402 resistors, UNI-ROYAL **0402WGF470JTCE**, LCSC **C25118**: R23 SCLK, R24 MOSI, and R25 CS near U1, with R26 MISO near U3.15. Evidence: [C25118 listing](https://www.lcsc.com/product-detail/C25118.html) and [TI ADS1220 datasheet](https://www.ti.com/lit/ds/symlink/ads1220.pdf). Expected benefit is lower digital edge ringing and interference; ADC resolution improvement requires measurement. Dedicated DRDY remains NC.

Measure shorted-input and bridge-simulator noise, drift, settling, and input excursions across USB, radio TX, LED, charging, and load states. Verify SPI mode 1, reset/register readback, external reference, gain/rate, headroom, calibration, polarity, and settling.
