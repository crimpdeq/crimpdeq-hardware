# ESP32-C3-MINI-1 ESP32-C3-MINI-1U Datasheet Version 2.2

Small-sized 2.4 GHz Wi-Fi (802.11b/g/n) and Bluetooth<sup>®</sup> 5 module Built around ESP32-C3 series of SoCs, RISC-V single-core microprocessor Up to 8 MB flash in chip package

15 GPIOs

On-board PCB antenna or external antenna connector



ESP32-C3-MINI-1



ESP32-C3-MINI-1U



www.espressif.com

1 Module Overview

## 1 Module Overview

Note:

Check the link or the QR code to make sure that you use the latest version of this document: https://www.espressif.com/documentation/esp32-c3-mini-1_datasheet_en.pdf

### 1.1 Features

#### CPU and On-Chip Memory

- ESP32-C3FH4, ESP32-C3FH4X, ESP32-C3FH8X, or ESP32-C3FH4AZ embedded, 32-bit RISC-V single-core processor, up to 160 MHz

_Note that when the chip scans in Station mode, the SoftAP channel will change along with the Station channel_

- 802.11mc FTM

#### Bluetooth<sup>®</sup>

- 384 KB ROM

- 400 KB SRAM (16 KB for cache)

   - Bluetooth LE: Bluetooth 5, Bluetooth mesh

   - Speed: 125 Kbps, 500 Kbps, 1 Mbps, 2 Mbps

- 8 KB SRAM in RTC

   - Advertising extensions

- Up to 8 MB flash in chip package

- Multiple advertisement sets

#### Wi-Fi

- IEEE 802.11 b/g/n-compliant

- Center frequency range of operating channel: 2412 ~ 2484 MHz

- Supports 20 MHz, 40 MHz bandwidth in 2.4 GHz band

- 1T1R mode with data rate up to 150 Mbps

- Wi-Fi Multimedia (WMM)

- TX/RX A-MPDU, TX/RX A-MSDU

- Immediate Block ACK

- Fragmentation and defragmentation

- Channel selection algorithm #2

- Internal co-existence mechanism between Wi-Fi and Bluetooth to share the same antenna

#### Peripherals

- Up to 15 GPIOs

   - 3 strapping GPIOs

- SPI, UART, I2C, I2S, remote control peripheral, LED PWM controller, general DMA controller, TWAI<sup>®</sup> controller (compatible with ISO 11898-1, i.e. CAN Specification 2.0), USB Serial/JTAG controller, temperature sensor, SAR ADC, general-purpose timers, watchdog timers

Note:

- Transmit opportunity (TXOP)

- Automatic Beacon monitoring (hardware TSF)

   - Please refer to _ESP32-C3 Series Datasheet_ for detailed information about the module peripherals.

- 4 × virtual Wi-Fi interfaces

- Simultaneous support for Infrastructure BSS in Station mode, SoftAP mode, Station + SoftAP mode, and promiscuous mode

#### Integrated Components on Module

- 40 MHz crystal oscillator

Espressif Systems

2

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

<u>Submit Documentation Feedback</u>

1 Module Overview

#### Antenna Options

- ESP32-C3-MINI-1: On-board PCB antenna

   - 85 °C version module: –40 ~ 85 °C

   - 105 °C version module: –40 ~ 105 °C

- ESP32-C3-MINI-1U: External antenna via a connector

#### Certification

- RF certification: See <u>certificates</u>

#### Operating Conditions

   - Green certification: RoHS/REACH

- Operating voltage/Power supply: 3.0 ~ 3.6 V

#### Test

- Operating ambient temperature:

- HTOL/HTSL/uHAST/TCT/ESD/Latch-up

### 1.2 Series Comparison

ESP32-C3-MINI-1 and ESP32-C3-MINI-1U are two general-purpose Wi-Fi and Bluetooth LE modules. The rich set of peripherals and a small size make the two modules an ideal choice for smart homes, industrial automation, health care, consumer electronics, etc.

ESP32-C3-MINI-1 comes with a PCB antenna. ESP32-C3-MINI-1U comes with an external antenna connector. A wide selection of module variants are available as shown in Table 1-1 and 1-2.

The series comparison for the two modules is as follows:

Table 1-1. ESP32-C3-MINI-1 (ANT) Series Comparison<sup>1</sup>

|<sup>5</sup>|<sup>4</sup>|Ambient Temp.<sup>2</sup>|Embedded|Size<sup>3</sup>|
|---|---|---|---|---|
|Part Number|Flash|(°C)|Chip Revision<sup>6</sup>|(mm)|
|ESP32-C3-MINI-1-N4X<br>(Recommended)|4 MB (Quad SPI)|–40_∼_85|v1.1||
|ESP32-C3-MINI-1-H4X<br>(Recommended)||–40_∼_105|v1.1|13.2 × 16.6 × 2.4|
|ESP32-C3-MINI-1-H8X|8 MB (Quad SPI)|–40_∼_105|v1.1||
|ESP32-C3-MINI-1-N4(<br>NRND)||–40_∼_85|v0.4||
|ESP32-C3-MINI-1-H4(<br>NRND)|4 MB (Quad SPI)|–40_∼_105|v0.4||
|ESP32-C3-MINI-1-H4-AZ(<br>NRND)||–40_∼_105|v0.4||



1 This table shares the same notes presented in Table 1-2 below.

Espressif Systems

3

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

<u>Submit Documentation Feedback</u>

1 Module Overview

Table 1-2. ESP32-C3-MINI-1U (CONN) Series Comparison

|Part Number<sup>5</sup>|Flash<sup>4, 7</sup>|Ambient Temp.<sup>2</sup><br>(°C)|Embedded<br>Chip Revision <sup>6</sup>|Size<sup>3</sup><br>(mm)|
|---|---|---|---|---|
|ESP32-C3-MINI-1U-N4X<br>(Recommended)||–40_∼_85|v1.1||
|ESP32-C3-MINI-1U-H4X<br>(Recommended)|4 MB (Quad SPI)|–40_∼_105|v1.1|13.2 × 12.5 × 2.4|
|ESP32-C3-MINI-1U-N4(<br>NRND)||–40_∼_85|v0.4||
|ESP32-C3-MINI-1U-H4(<br>NRND)||–40_∼_105|v0.4||



- 2 Ambient temperature specifies the recommended temperature range of the environment immediately outside the Espressif module.

- 3 For details, refer to Section 10.1 _Module Dimensions_ .

- 4 The flash is integrated in the chip’s package. For specifications, refer to Section 6.5 _Memory Specifications_ .

- 5 All modules can be pre-programmed with <u>AWS IoT ExpressLink</u> firmware. Modules with such firmware have suffix ”-A” in their part numbers, e.g. ESP32-C3-MINI-1-N4-A. Since AWS IoT ExpressLink firmware enables flash encryption and secure boot, joint download boot mode will be disabled, and it will no longer be possible to program firmware through the UART or USB port into the modules.

- 6 All chip revisions have the same SRAM size, but chip revision v1.1 has around 10 KB more available space for users than chip revision v0.4. Chip revision v1.1 depends on specific ESP-IDF versions, as detailed in <u>Compatibility Advisory for ESP32-C3 Chip Revision v1.1.</u> For how to identify chip revisions, please refer to _<u>ESP32-C3 Series SoC Errata</u>_ <u>.</u>

- 7 By default, the SPI flash on the module operates at a maximum clock frequency of 80 MHz and does not support the auto suspend feature. If you have a requirement for a higher flash clock frequency of 120 MHz or if you need the flash auto suspend feature, please <u>contact us.</u>

Both ESP32-C3-MINI-1 and ESP32-C3-MINI-1U has two operating ambient temperature options: –40 _∼_ 85 °C variants and –40 _∼_ 105 °C variants. These modules can be embedded with the following chips:

- ESP32-C3FH4: chip revision v0.4, 4 MB flash

- ESP32-C3FH4X: chip revision v1.1, 4 MB flash

- ESP32-C3FH8X: chip reivision v1.1, 8 MB

ESP32-C3-MINI-1 has one more variant: ESP32-C3-MINI-1-H4-AZ embedded with the ESP32-C3FH4AZ chip. For this chip, SPI0/SPI1 pins for flash connection are not bonded.

For more information about the differences between chips embedded, please refer to Section _Chip Series Comparison_ in _<u>ESP32-C3 Series Datasheet</u>_ <u>.</u>

### 1.3 Applications

- Smart Home

   - POS Machines

- Industrial Automation

   - Service Robot

- Health Care

   - Audio Devices

- Consumer Electronics

- Smart Agriculture

- Generic Low-power IoT Sensor Hubs

- Generic Low-power IoT Data Loggers

Espressif Systems

4 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

Contents

## Contents

|1|Module Overview|2|
|---|---|---|
|1.1|Features|2|
|1.2|Series Comparison|3|
|1.3|Applications|4|
|2|Block Diagram|9|
|3|Pin Definitions|10|
|3.1|Pin Layout|10|
|3.2|Pin Description|10|
|4|Boot Configurations|12|
|4.1|i<br>Chip Boot Mode Control|13|
|4.2|ROM Messages Printing Control|14|
|4.3|Chip Power-up and Reset|14|
|5|Peripherals|16|
|5.1|Peripheral Overview|16|
|5.2|Peripheral Description|16|
||5.2.1<br>Connectivity Interface|16|
||5.2.1.1<br>UART Controller|16|
||5.2.1.2<br>SPI Controller|16|
||5.2.1.3<br>I2C Controller|17|
||5.2.1.4<br>I2S Controller|18|
||5.2.1.5<br>USB Serial/JTAG Controller|18|
||5.2.1.6<br>Two-wire Automotive Interface|18|
||5.2.1.7<br>LED PWM Controller|19|
||5.2.1.8<br>Remote Control Peripheral|19|
||5.2.2<br>Analog Signal Processing|19|
||5.2.2.1<br>SAR ADC|20|
||5.2.2.2<br>Temperature Sensor|20|
|6|Electrical Characteristics|21|
|6.1|Absolute Maximum Ratings|21|
|6.2|Recommended Operating Conditions|21|
|6.3|DC Characteristics (3.3 V, 25 °C)|21|
|6.4|Current Consumption Characteristics|22|
||6.4.1<br>Current Consumption in Active Mode|22|
||6.4.2<br>Current Consumption in Other Modes|23|
|6.5|Memory Specifications|23|
|7|RF Characteristics|25|
|7.1|Wi-Fi Radio|25|



Espressif Systems

5 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

Contents

||7.1.1<br>Wi-Fi RF Transmitter (TX) Characteristics|25|
|---|---|---|
||7.1.2<br>Wi-Fi RF Receiver (RX) Characteristics|26|
|7.2|Bluetooth 5 (LE) Radio|27|
||7.2.1<br>Bluetooth LE RF Transmitter (TX) Characteristics|27|
||7.2.2<br>Bluetooth LE RF Receiver (RX) Characteristics|29|
|8|Module Schematics|32|
|9|Peripheral Schematics|34|
|10|Physical Dimensions|35|
|10.1|Module Dimensions|35|
|10.2|Dimensions of External Antenna Connector|36|
|11|PCB Layout Recommendations|38|
|11.1|PCB Land Pattern|38|
|11.2|Module Placement for PCB Design|39|
|12|Product Handling|40|
|12.1|Storage Conditions|40|
|12.2|Electrostatic Discharge (ESD)|40|
|12.3|Reflow Profile|40|
|12.4|Ultrasonic Vibration|41|
|Dat|asheet Versioning|42|
|Rel|ated Documentation and Resources|43|
|Re|vision History|45|



Espressif Systems

6 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

List of Tables

## List of Tables

|1-1|ESP32-C3-MINI-1 (ANT) Series Comparison<sup>1</sup>|3|
|---|---|---|
|1-2|ESP32-C3-MINI-1U (CONN) Series Comparison|4|
|3-1|Pin Definitions|11|
|4-1|Default Configuration of Strapping Pins|12|
|4-2|Description of Timing Parameters for the Strapping Pins|13|
|4-3|Chip Boot Mode Control|13|
|4-4|UART0 ROM Message Printing Control|14|
|4-5|USB Serial/JTAG ROM Message Printing Control|14|
|4-6|Description of Timing Parameters for Power-up and Reset|15|
|6-1|Absolute Maximum Ratings|21|
|6-2|Recommended Operating Conditions|21|
|6-3|DC Characteristics (3.3 V, 25 °C)|21|
|6-4|Current Consumption for Wi-Fi (2.4 GHz) in Active Mode|22|
|6-5|Current Consumption for Bluetooth LE in Active Mode|22|
|6-6|Current Consumption in Modem-sleep Mode|23|
|6-7|Current Consumption in Low-Power Modes|23|
|6-8|Flash Specifications|23|
|7-1|Wi-Fi RF Characteristics|25|
|7-2|TX Power with Spectral Mask and EVM Meeting 802.11 Standards|25|
|7-3|TX EVM Test<sup>1</sup>|25|
|7-4|RX Sensitivity|26|
|7-5|Maximum RX Level|27|
|7-6|RX Adjacent Channel Rejection|27|
|7-7|Bluetooth LE RF Characteristics|27|
|7-8|Bluetooth LE - Transmitter Characteristics - 1 Mbps|28|
|7-9|Bluetooth LE - Transmitter Characteristics - 2 Mbps|28|
|7-10|Bluetooth LE - Transmitter Characteristics - 125 Kbps|28|
|7-11|Bluetooth LE - Transmitter Characteristics - 500 Kbps|29|
|7-12|Bluetooth LE - Receiver Characteristics - 1 Mbps|29|
|7-13|Bluetooth LE - Receiver Characteristics - 2 Mbps|30|
|7-14|Bluetooth LE - Receiver Characteristics - 125 Kbps|30|
|7-15|Bluetooth LE - Receiver Characteristics - 500 Kbps|31|



Espressif Systems

7 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

List of Figures

## List of Figures

|2-1|ESP32-C3-MINI-1 Block Diagram|9|
|---|---|---|
|2-2|ESP32-C3-MINI-1U Block Diagram|9|
|3-1|Pin Layout (Top View)|10|
|4-1|Visualization of Timing Parameters for the Strapping Pins|13|
|4-2|Visualization of Timing Parameters for Power-up and Reset|15|
|8-1|ESP32-C3-MINI-1 Schematics|32|
|8-2|ESP32-C3-MINI-1U Schematics|33|
|9-1|Peripheral Schematics|34|
|10-1|ESP32-C3-MINI-1 Physical Dimensions|35|
|10-2|ESP32-C3-MINI-1U Physical Dimensions|35|
|10-3|Dimensions of External Antenna Connector|36|
|11-1|ESP32-C3-MINI-1 Recommended PCB Land Pattern|38|
|11-2|ESP32-C3-MINI-1U Recommended PCB Land Pattern|39|
|12-1|Reflow Profile|40|



Espressif Systems

8 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

2 Block Diagram

## 2 Block Diagram



<!-- Start of picture text -->
ESP32-C3-MINI-1<br>40 MHz<br>3V3 Crystal Antenna<br>RF Matching<br>ESP32-C3FH4<br>EN GPIOs<br>SPI Flash<br><!-- End of picture text -->

Figure 2-1. ESP32-C3-MINI-1 Block Diagram



<!-- Start of picture text -->
ESP32-C3-MINI-1U<br>40 MHz<br>3V3 Crystal Antenna<br>R F Matching<br>ESP32-C3FH4<br>EN GPIOs<br>SPI Flash<br><!-- End of picture text -->

Figure 2-2. ESP32-C3-MINI-1U Block Diagram

###### Note:

For the pin mapping between the chip and the in-package flash, please refer to _ESP32-C3 Series Datasheet_ > Table _Pin Mapping Between Chip and In-package Flash_ .

Espressif Systems

9 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

3 Pin Definitions

## 3 Pin Definitions

### 3.1 Pin Layout

The pin diagram below shows the approximate location of pins on the module. For the actual diagram drawn to scale, please refer to Figure 10.1 _Module Dimensions_ .



<!-- Start of picture text -->
A<br>Keepout Zone<br>Pin 53 Pin 50<br>GND GND<br>GND Pin 1 Pin 35 NC<br>GND Pin 2 Pin 34 NC<br>3V3 Pin 3 Pin 33 NC<br>GND GND GND<br>NC Pin 4 Pin 32 NC<br>IO2 Pin 5 Pin 31 TXD0<br>IO3 Pin 6 GND Pin 49GND GND Pin 30 RXD0<br>NC Pin 7 Pin 29 NC<br>EN Pin 8 Pin 28 NC<br>GND GND GND<br>NC Pin 9 Pin 27 IO19<br>NC Pin 10 Pin 26 IO18<br>GND Pin 11 Pin 25 NC<br>Pin 52 Pin 51<br>GND GND<br>GND GND GND GND GND GND GND GND GND GND GND GND GND<br>Pin 48 Pin 47 Pin 46 Pin 45 Pin 44 Pin 43 Pin 42 Pin 41 Pin 40 Pin 39 Pin 38 Pin 37 Pin 36<br>Pin 12 Pin 13 Pin 14 Pin 15 Pin 16 Pin 17 Pin 18 Pin 19 Pin 20 Pin 21 Pin 22 Pin 23 Pin 24<br>IO0 IO1 GND NC IO10 NC IO4 IO5 IO6 IO7 IO8 IO9 NC<br><!-- End of picture text -->

Figure 3-1. Pin Layout (Top View)

###### Note A:

The zone marked with dotted lines is the antenna keepout zone. The pin diagram is applicable to ESP32-C3-MINI-1 and ESP32-C3-MINI-1U, but the latter has no antenna keepout zone.

To learn more about the keepout zone for module’s antenna on the base board, please refer to _ESP32-C3 Hardware Design Guidelines_ > Section _General Principles of PCB Layout for Modules_ .

### 3.2 Pin Description

The module has 53 pins. See pin definitions in Table 3-1 _Pin Definitions_ .

For peripheral pin configurations, please refer to Section 5.2 _Peripheral Description_ .

Espressif Systems

10 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

3 Pin Definitions

Table 3-1. Pin Definitions

|Name|No.|Type<sup>1</sup>|Function|
|---|---|---|---|
|GND|1, 2, 11, 14,<br>36-53|P|Ground|
|3V3|3|P|Power supply|
|NC|4, 7, 9, 10,<br>15, 17, 24,<br>25, 28, 29,<br>32-35|—|NC|
|IO2|5|I/O/T|GPIO2, ADC1_CH2, FSPIQ|
|IO3|6|I/O/T|GPIO3, ADC1_CH3|
|EN|8|I|High: on, enables the chip.<br>Low: off, the chip powers off.<br>Note: Do not leave the EN pin floating.|
|IO0|12|I/O/T|GPIO0, ADC1_CH0, XTAL_32K_P|
|IO1|13|I/O/T|GPIO1, ADC1_CH1, XTAL_32K_N|
|IO10|16|I/O/T|GPIO10, FSPICS0|
|IO4|18|I/O/T|GPIO4, ADC1_CH4, FSPIHD, MTMS|
|IO5|19|I/O/T|GPIO5, ADC2_CH0, FSPIWP, MTDI|
|IO6|20|I/O/T|GPIO6, FSPICLK, MTCK|
|IO7|21|I/O/T|GPIO7, FSPID, MTDO|
|IO8|22|I/O/T|GPIO8|
|IO9|23|I/O/T|GPIO9|
|IO18|26|I/O/T|GPIO18, USB_D-|
|IO19|27|I/O/T|GPIO19, USB_D+|
|RXD0|30|I/O/T|GPIO20, U0RXD|
|TXD0|31|I/O/T|GPIO21, U0TXD|



1 P: power supply; I: input; O: output; T: high impedance.

Espressif Systems

11

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

<u>Submit Documentation Feedback</u>

4 Boot Configurations

## 4 Boot Configurations

Note:

The content below is excerpted from _ESP32-C3 Series Datasheet_ > Chapter _Boot Configurations_ . For the strapping pin mapping between the chip and modules, please refer to Chapter 8 _Module Schematics_ .

The chip allows for configuring the following boot parameters through strapping pins and eFuse parameters at power-up or a hardware reset, without microcontroller interaction.

- Chip boot mode

   - Strapping pins: GPIO2, GPIO8, and GPIO9

- ROM message printing

   - Strapping pin: GPIO8

   - eFuse parameters: EFUSE_UART_PRINT_CONTROL and EFUSE_USB_PRINT_CHANNEL

The default values of all the above eFuse parameters are 0, which means that they are not burnt. Given that eFuse is one-time programmable, once programmed to 1, it can never be reverted to 0. For how to program eFuse parameters, please refer to _<u>ESP32-C3 Technical Reference Manual</u>_ > Chapter _eFuse Controller_ .

The default values of the strapping pins, namely the logic levels, are determined by pins’ internal weak pull-up/pull-down resistors at reset if the pins are not connected to any circuit, or connected to an external high-impedance circuit.

Table 4-1. Default Configuration of Strapping Pins

|StrappingPin|Default Configuration|Bit Value|
|---|---|---|
|GPIO2|Floating|–|
|GPIO8|Floating|–|
|GPIO9|Weak pull-up|1|



To change the bit values, the strapping pins should be connected to external pull-down/pull-up resistances. If the ESP32-C3 is used as a device by a host MCU, the strapping pin voltage levels can also be controlled by the host MCU.

All strapping pins have latches. At Chip Reset, the latches sample the bit values of their respective strapping pins and store them until the chip is powered down or shut down. The states of latches cannot be changed in any other way. It makes the strapping pin values available during the entire chip operation, and the pins are freed up to be used as regular IO pins after reset. For details on Chip Reset, see _<u>ESP32-C3 Technical Reference Manual</u>_ > Chapter _Reset and Clock_ .

The timing of signals connected to the strapping pins should adhere to the _setup time_ and _hold time_ specifications in Table 4-2 and Figure 4-1.

Espressif Systems

12

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

<u>Submit Documentation Feedback</u>

4 Boot Configurations

Table 4-2. Description of Timing Parameters for the Strapping Pins

|Parameter|Description|Min (ms)|
|---|---|---|
|t_SU_|_Setup time_is the time reserved for the power rails to stabilize be-<br>fore the CHIP_EN pin is pulled high to activate the chip.|0|
||_Hold time_ is the time reserved for the chip to read the strapping||
|t_H_|pin values after CHIP_EN is already high and before these pins|3|
||start operatingas regular IO pins.||





<!-- Start of picture text -->
t SU t H<br>V IH_nRST<br>CHIP_EN<br>V IH<br>Strapping pin<br><!-- End of picture text -->

Figure 4-1. Visualization of Timing Parameters for the Strapping Pins

### 4.1 Chip Boot Mode Control

GPIO2, GPIO8, and GPIO9 control the boot mode after the reset is released. See Table 4-3 _Chip Boot Mode Control_ .

Table 4-3. Chip Boot Mode Control

|Boot Mode|GPIO2 <sup>2</sup>|GPIO8|GPIO9|
|---|---|---|---|
|SPI boot mode|1|Any value|1|
|Joint download boot mode<sup>3</sup>|1|1|0|



- 1 Bold marks the default value and configuration.

- 2 GPIO2 actually does not determine SPI Boot and Joint Download Boot mode, but it is recommended to pull this pin up due to glitches.

- 3 Joint Download Boot mode supports the following download methods:

   - USB-Serial-JTAG Download Boot

   - UART Download Boot

In SPI Boot mode, the ROM bootloader loads and executes the program from SPI flash to boot the system.

Espressif Systems

13 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

4 Boot Configurations

In Joint Download Boot mode, users can download binary files into flash using UART0 or USB interface. It is also possible to download binary files into SRAM and execute it from SRAM.

In addition to SPI Boot and Joint Download Boot modes, ESP32-C3 also supports SPI Download Boot mode. For details, please see _<u>ESP32-C3 Technical Reference Manual</u>_ > Chapter _Chip Boot Control_ .

### 4.2 ROM Messages Printing Control

During the boot process, the messages by the ROM code can be printed to:

- (Default) UART0 and USB Serial/JTAG controller

- UART0

- USB Serial/JTAG controller

EFUSE_UART_PRINT_CONTROL and GPIO8 control ROM messages printing to UART0 as shown in Table 4-4 _UART0 ROM Message Printing Control_ .

Table 4-4. UART0 ROM Message Printing Control

|UART0 ROM Code Printing|EFUSE_UART_PRINT_CONTROL|GPIO8|
|---|---|---|
||0|Ignored|
|Enabled|1|0|
||2|1|
||1|1|
|Disabled|2|0|
||3|Ignored|



- 1 Bold marks the default value and configuration.

EFUSE_USB_PRINT_CHANNEL controls the printing to USB Serial/JTAG controller as shown in Table 4-5 _USB Serial/JTAG ROM Message Printing Control_ .

Table 4-5. USB Serial/JTAG ROM Message Printing Control

|USB Serial/JTAG<br>ROM Code Printing|EFUSE_DIS_USB_SERIAL_JTAG <sup>2</sup>|EFUSE_USB_PRINT_CHANNEL|
|---|---|---|
|Enabled|0|0|
|Disabled|0|1|
||1|Ignored|



- 1 Bold marks the default value and configuration.

- 2 EFUSE_DIS_USB_SERIAL_JTAG controls whether to disable USB Serial/JTAG.

### 4.3 Chip Power-up and Reset

Once the power is supplied to the chip, its power rails need a short time to stabilize. After that, CHIP_EN – the pin used for power-up and reset – is pulled high to activate the chip. For information on CHIP_EN as well as power-up and reset timing, see Figure 4-2 and Table 4-6.

Espressif Systems

14 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

4 Boot Configurations



<!-- Start of picture text -->
t ST BL t RST<br>2.8 V<br>VDDA,<br>VDD3P3,<br>VDD3P3_RTC,<br>VDD3P3_CPU<br>V IL_nRST<br>CHIP_EN<br><!-- End of picture text -->

Figure 4-2. Visualization of Timing Parameters for Power-up and Reset

Table 4-6. Description of Timing Parameters for Power-up and Reset

|Parameter|Description|Min (_µ_s)|
|---|---|---|
||Time<br>reserved<br>for<br>the<br>power<br>rails<br>of<br>VDDA,<br>VDD3P3,||
|t_ST BL_|VDD3P3_RTC, and VDD3P3_CPU to stabilize before the CHIP_EN|50|
||pin is pulled high to activate the chip||
|t_RST_|Time reserved for CHIP_EN to stay below V_IL_nRST_ to reset the<br>chip (see Table6-3)|50|



Espressif Systems

15

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

<u>Submit Documentation Feedback</u>

5 Peripherals

## 5 Peripherals

### 5.1 Peripheral Overview

ESP32-C3FH4 integrates a rich set of peripherals including SPI, UART, I2C, I2S, remote control peripheral, LED PWM controller, TWAI<sup>®</sup> controller, USB Serial/JTAG controller, temperature sensor, SAR ADC.

To learn more about on-chip components, please refer to _<u>ESP32-C3 Series Datasheet</u>_ > Section _Functional Description_ .

Note:

The content below is sourced from _ESP32-C3 Series Datasheet_ > Section _Peripherals_ . Some information may not be applicable to ESP32-C3-MINI-1 and ESP32-C3-MINI-1U as not all the IO signals are exposed on the module. To learn more about peripheral signals, please refer to _ESP32-C3 Technical Reference Manual_ > Section _Peripheral Signal List_ .

### 5.2 Peripheral Description

This section describes the chip’s peripheral capabilities, covering connectivity interfaces and on-chip sensors that extend its functionality.

#### 5.2.1 Connectivity Interface

This subsection describes the connectivity interfaces on the chip that enable communication and interaction with external devices and networks.

#### 5.2.1.1 UART Controller

ESP32-C3 has two UART interfaces, i.e. UART0 and UART1, which support IrDA and asynchronous communication (RS232 and RS485) at a speed of up to 5 Mbps. The UART controller provides hardware flow control (CTS and RTS signals) and software flow control (XON and XOFF). Both UART interfaces connect to GDMA via UHCI0, and can be accessed by the GDMA controller or directly by the CPU.

For details, see _<u>ESP32-C3 Technical Reference Manual</u>_ > Chapter _UART Controller (UART, LP_UART)_ .

##### Pin Assignment

For details, see _<u>ESP32-C3 Series Datasheet</u>_ > Section _Peripheral Pin Assignment_ .

#### 5.2.1.2 SPI Controller

ESP32-C3 has the following SPI interfaces:

- SPI0 used by ESP32-C3’s GDMA controller and cache to access in-package or off-package flash

- SPI1 used by the CPU to access in-package or off-package flash

- SPI2 is a general purpose SPI controller with access to a DMA channel allocated by the GDMA controller

Espressif Systems

16 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

5 Peripherals

#### Features of SPI0 and SPI1

- Supports Single SPI, Dual SPI, and Quad SPI, QPI modes

- Configurable clock frequency with a maximum of 120 MHz in Single Transfer Rate (STR) mode

- Data transmission is in bytes

#### Features of SPI2

- Supports operation as a master or slave

- Connects to a DMA channel allocated by the GDMA controller

- Supports Single SPI, Dual SPI, and Quad SPI, QPI

- Configurable clock polarity (CPOL) and phase (CPHA)

- Configurable clock frequency

- Data transmission is in bytes

- Configurable read and write data bit order: most-significant bit (MSB) first, or least-significant bit (LSB) first

- As a master

   - Supports 2-line full-duplex communication with clock frequency up to 80 MHz

   - Supports 1-, 2-, 4-line half-duplex communication with clock frequency up to 80 MHz

   - Provides six SPI_CS pins for connection with six independent SPI slaves

   - Configurable CS setup time and hold time

- As a slave

   - Supports 2-line full-duplex communication with clock frequency up to 60 MHz

   - Supports 1-, 2-, 4-line half-duplex communication with clock frequency up to 60 MHz

For details, see _<u>ESP32-C3 Technical Reference Manual</u>_ > Chapter _SPI Controller (SPI)_ .

##### Pin Assignment

For details, see _<u>ESP32-C3 Series Datasheet</u>_ > Section _Peripheral Pin Assignment_ .

#### 5.2.1.3 I2C Controller

ESP32-C3 has an I2C bus interface which is used for I2C master mode or slave mode, depending on your configuration. The I2C interface supports:

- Standard mode (100 Kbit/s)

- Fast mode (400 Kbit/s)

- Up to 800 Kbit/s (constrained by SCL and SDA pull-up strength)

- 7-bit and 10-bit addressing mode

- Double addressing mode

Espressif Systems

17

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

<u>Submit Documentation Feedback</u>

5 Peripherals

- 7-bit broadcast address

For details, see _<u>ESP32-C3 Technical Reference Manual</u>_ > Chapter _I2C Controller (I2C)_ .

##### Pin Assignment

For details, see _<u>ESP32-C3 Series Datasheet</u>_ > Section _Peripheral Pin Assignment_ .

#### 5.2.1.4 I2S Controller

ESP32-C3 includes a standard I2S interface. This interface can operate as a master or a slave in full-duplex mode or half-duplex mode, and can be configured for 8-bit, 16-bit, 24-bit, or 32-bit serial communication. BCK clock frequency, from 10 kHz up to 40 MHz, is supported.

The I2S interface connects to the GDMA controller. The interface supports TDM PCM, TDM MSB alignment, TDM standard, and PDM standard.

For details, see _<u>ESP32-C3 Technical Reference Manual</u>_ > Chapter _I2S Controller (I2S)_ .

##### Pin Assignment

For details, see _<u>ESP32-C3 Series Datasheet</u>_ > Section _Peripheral Pin Assignment_ .

#### 5.2.1.5 USB Serial/JTAG Controller

ESP32-C3 integrates a USB Serial/JTAG controller. This controller has the following features:

- CDC-ACM virtual serial port and JTAG adapter functionality

- USB 2.0 full speed compliant, capable of up to 12 Mbit/s transfer speed (Note that this controller does not support the faster 480 Mbit/s high-speed transfer mode)

- Programming in-package/off-package flash

- CPU debugging with compact JTAG instructions

- A full-speed USB PHY integrated in the chip

For details, see _<u>ESP32-C3 Technical Reference Manual</u>_ > Chapter _USB Serial/JTAG Controller (USB_SERIAL_JTAG)_ .

##### Pin Assignment

For details, see _<u>ESP32-C3 Series Datasheet</u>_ > Section _Peripheral Pin Assignment_ .

#### 5.2.1.6 Two-wire Automotive Interface

ESP32-C3 has a TWAI<sup>®</sup> controller with the following features:

- Compatible with ISO 11898-1 protocol (CAN Specification 2.0)

- Standard frame format (11-bit ID) and extended frame format (29-bit ID)

- Bit rates from 1 Kbit/s to 1 Mbit/s

- Multiple modes of operation: Normal, Listen Only, and Self-Test (no acknowledgment required)

Espressif Systems

18 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

5 Peripherals

- 64-byte receive FIFO

- Acceptance filter (single and dual filter modes)

- Error detection and handling: error counters, configurable error interrupt threshold, error code capture, arbitration lost capture

For details, see _<u>ESP32-C3 Technical Reference Manual</u>_ > Chapter _Two-wire Automotive Interface_ .

##### Pin Assignment

For details, see _<u>ESP32-C3 Series Datasheet</u>_ > Section _Peripheral Pin Assignment_ .

#### 5.2.1.7 LED PWM Controller

The LED PWM controller can generate independent digital waveform on six channels. The LED PWM controller:

- Can generate digital waveform with configurable periods and duty cycle. The resolution of duty cycle can be up to 14 bits.

- Has multiple clock sources, including APB clock and external main crystal clock.

- Can operate when the CPU is in Light-sleep mode.

- Supports gradual increase or decrease of duty cycle, which is useful for the LED RGB color-gradient generator.

For details, see _<u>ESP32-C3 Technical Reference Manual</u>_ > Chapter _LED PWM Controller_ .

##### Pin Assignment

For details, see _<u>ESP32-C3 Series Datasheet</u>_ > Section _Peripheral Pin Assignment_ .

#### 5.2.1.8 Remote Control Peripheral

The Remote Control Peripheral (RMT) supports two channels of infrared remote transmission and two channels of infrared remote reception. By controlling pulse waveform through software, it supports various infrared and other single wire protocols. All four channels share a 192 × 32-bit memory block to store transmit or receive waveform.

For more details, see _<u>ESP32-C3 Technical Reference Manual</u>_ > Chapter _Remote Control Peripheral (RMT)_ .

##### Pin Assignment

For details, see _<u>ESP32-C3 Series Datasheet</u>_ > Section _Peripheral Pin Assignment_ .

#### 5.2.2 Analog Signal Processing

This subsection describes components on the chip that sense and process real-world data.

Espressif Systems

19 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

5 Peripherals

#### 5.2.2.1 SAR ADC

ESP32-C3 integrates two 12-bit SAR ADCs.

- ADC1 supports measurements on 5 channels, and is factory-calibrated.

- ADC2 supports measurements on 1 channel, and is not factory-calibrated.

Note:

ADC2 of some chip revisions is not operable. For details, please refer to ESP32-C3 Series SoC Errata.

For more details, see _<u>ESP32-C3 Technical Reference Manual</u>_ > Chapter _On-Chip Sensors and Analog Signal Processing_ .

##### Pin Assignment

For details, see _<u>ESP32-C3 Series Datasheet</u>_ > Section _Peripheral Pin Assignment_ .

#### 5.2.2.2 Temperature Sensor

The temperature sensor generates a voltage that varies with temperature. The voltage is internally converted via an ADC into a digital value.

The temperature sensor has a range of –40 °C to 125 °C. It is designed primarily to sense the temperature changes inside the chip. The temperature value depends on factors like microcontroller clock frequency or I/O load. Generally, the chip’s internal temperature is higher than the operating ambient temperature.

For more details, see _<u>ESP32-C3 Technical Reference Manual</u>_ > Chapter _On-Chip Sensors and Analog Signal Processing_ .

Espressif Systems

20 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

6 Electrical Characteristics

## 6 Electrical Characteristics

### 6.1 Absolute Maximum Ratings

Stresses above those listed in Table 6-1 _Absolute Maximum Ratings_ may cause permanent damage to the device. These are stress ratings only and functional operation of the device at these or any other conditions beyond those indicated under Table 6-2 _Recommended Operating Conditions_ is not implied. Exposure to absolute-maximum-rated conditions for extended periods may affect device reliability.

Table 6-1. Absolute Maximum Ratings

|Symbol|Parameter|Min|Max|Unit|
|---|---|---|---|---|
|VDD33|Power supply voltage|–0.3|3.6|V|



### 6.2 Recommended Operating Conditions

Table 6-2. Recommended Operating Conditions

|Symbol|Parameter||Min|Typ|Max|Unit|
|---|---|---|---|---|---|---|
|VDD33|Power supply voltage||3.0|3.3|3.6|V|
|I_V DD_|Current delivered by external po|wer supply|0.5|—|—|A|
|T_A_|Operating ambient temperature|85 °C version<br>105 °C version|–40|—|85<br>105|°C|



### 6.3 DC Characteristics (3.3 V, 25 °C)

Table 6-3. DC Characteristics (3.3 V, 25 °C)

|Parameter|Description|Min|Typ|Max|Unit|
|---|---|---|---|---|---|
|C_IN_|Pin capacitance|—|2|—|pF|
|V_IH_|High-level input voltage|0.75 × VDD<sup>1</sup>|—|VDD<sup>1 </sup>+ 0.3|V|
|V_IL_|Low-level input voltage|–0.3|—|0.25 × VDD<sup>1</sup>|V|
|I_IH_|High-level input current|—|—|50|nA|
|I_IL_|Low-level input current|—|—|50|nA|
|V_OH_ <sup>2</sup>|High-level output voltage|0.8 × VDD<sup>1</sup>|—|—|V|
|V_OL_ <sup>2</sup>|Low-level output voltage|—|—|0.1 × VDD<sup>1</sup>|V|
|I_OH_|High-level source current (VDD<sup>1 </sup>= 3.3 V,<br>V_OH_ >= 2.64 V, PAD_DRIVER = 3)|—|40|—|mA|
|I_OL_|Low-level sink current (VDD<sup>1 </sup>= 3.3 V, V_OL_ =<br>0.495 V, PAD_DRIVER = 3)|—|28|—|mA|
|R_P U_|Internal weak pull-up resistor|—|45|—|kΩ|
|R_P D_|Internal weak pull-down resistor|—|45|—|kΩ|
|V_IH_nRST_|Chip reset release voltage (CHIP_EN voltage<br>is within the specified range)|0.75 × VDD<sup>1</sup>|—|VDD<sup>1 </sup>+ 0.3|V|



Cont’d on next page

Espressif Systems

21 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

6 Electrical Characteristics

Table 6-3 – cont’d from previous page

|Parameter|Description|Min|Typ|Max|Unit|
|---|---|---|---|---|---|
|V_IL_nRST_|Chip reset voltage (CHIP_EN voltage is within<br>the specified range)|–0.3|—|0.25 × VDD<sup>1</sup>|V|



- 1 VDD – voltage from a power pin of a respective power domain.

- 2 V _OH_ and V _OL_ are measured using high-impedance load.

### 6.4 Current Consumption Characteristics

#### 6.4.1 Current Consumption in Active Mode

The current consumption measurements are taken with a 3.3 V supply at 25 °C ambient temperature.

TX current consumption is rated at a 100% duty cycle.

RX current consumption is rated when the peripherals are disabled and the CPU idle.

Table 6-4. Current Consumption for Wi-Fi (2.4 GHz) in Active Mode

|Work mode|Des|cription|Peak (mA)|
|---|---|---|---|
|||802.11b, 1 Mbps, @20.5 dBm|350|
||TX|802.11g, 54 Mbps, @18 dBm|295|
|||802.11n, HT20, MCS7, @17.5 dBm|290|
|Active (RF working)||802.11n, HT40, MCS7, @17 dBm|290|
||RX|802.11b/g/n, HT20|82|
|||802.11n, HT40|84|



Table 6-5. Current Consumption for Bluetooth LE in Active Mode

|Work Mode|RF Condition|Description|Peak (mA)|
|---|---|---|---|
|||Bluetooth LE @ 20.0 dBm|340|
||TX|Bluetooth LE @ 9.0 dBm|190|
|Active (RF working)||Bluetooth LE @ 0 dBm|170|
|||Bluetooth LE @ –15.0 dBm|100|
||RX|Bluetooth LE|86|



Espressif Systems

22

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

<u>Submit Documentation Feedback</u>

6 Electrical Characteristics

Note:

The content below is excerpted from _Section Power Consumption in Other Modes_ in _ESP32-C3 Series Datasheet_ .

#### 6.4.2 Current Consumption in Other Modes

Table 6-6. Current Consumption in Modem-sleep Mode

|Mode|CPU Frequency<br>(MHz)|Description|Ty<br>All Peripherals Clocks<br>Disabled (mA)|p<br>All Peripherals Clocks<br>Enabled (mA) <sup>1</sup>|
|---|---|---|---|---|
||160|CPU is running|23|28|
|Mdl<sup>2,3</sup>||CPU is idle|16|21|
|oem-seep|80|CPU is running|17|22|
|||CPU is idle|13|18|



- 1 In practice, the current consumption might be different depending on which peripherals are enabled. 2 In Modem-sleep mode, Wi-Fi is clock gated.

- 3 In Modem-sleep mode, the consumption might be higher when accessing flash. For a flash rated at 80 Mbit/s, in SPI 2-line mode the consumption is 10 mA.

Table 6-7. Current Consumption in Low-Power Modes

|Mode|Description|Typ (_µ_A)|
|---|---|---|
|Light-sleep|VDD_SPI and Wi-Fi are powered down, and all GPIOs are high-impedance|130|
|Deep-sleep|RTC timer + RTC memory|5|
|Power off|CHIP_EN is set to low level, the chip is powered off|1|



### 6.5 Memory Specifications

The data below is sourced from the memory vendor datasheet. These values are guaranteed through design and/or characterization but are not fully tested in production. Devices are shipped with the memory erased.

Table 6-8. Flash Specifications

|Parameter|Description|Min|Typ|Max|Unit|
|---|---|---|---|---|---|
|VCC|Power supply voltage (1.8 V)|1.65|1.80|2.00|V|
||Power supply voltage (3.3 V)|2.7|3.3|3.6|V|
|F_C_|Maximum clock frequency|80|—|—|MHz|
|—|Program/erase cycles|100,000|—|—|cycles|
|T_RET_|Data retention time|20|—|—|years|
|T_P P_|Page program time|—|0.8|5|ms|
|T_SE_|Sector erase time (4 KB)|—|70|500|ms|
|T_BE_1|Block erase time (32 KB)|—|0.2|2|s|
|T_BE_2|Block erase time (64 KB)|—|0.3|3|s|



Cont’d on next page

Espressif Systems

23 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

6 Electrical Characteristics

Table 6-8 – cont’d from previous page

|Parameter|Description|Min|Typ|Max|Unit|
|---|---|---|---|---|---|
||Chip erase time (16 Mb)|—|7|20|s|
||Chip erase time (32 Mb)|—|20|60|s|
|T_CE_|Chip erase time (64 Mb)|—|25|100|s|
||Chip erase time (128 Mb)|—|60|200|s|
||Chip erase time (256 Mb)|—|70|300|s|



Espressif Systems

24

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

<u>Submit Documentation Feedback</u>

7 RF Characteristics

## 7 RF Characteristics

This section contains tables with RF characteristics of the Espressif product.

The RF data is measured at the antenna port, where RF cable is connected, including the front-end loss. The external antennas used for the tests on the modules with external antenna connectors have an impedance of 50 Ω.

Devices should operate in the center frequency range allocated by regional regulatory authorities. The target center frequency range and the target transmit power are configurable by software. See <u>ESP RF Test Tool and Test Guide</u> for instructions.

Unless otherwise stated, the RF tests are conducted with a 3.3 V (±5%) supply at 25 ºC ambient temperature.

### 7.1 Wi-Fi Radio

Table 7-1. Wi-Fi RF Characteristics

|Name|Description|
|---|---|
|Center frequency range of operatingchannel|2412~2484 MHz|
|Wi-Fi wireless standard|IEEE 802.11b/g/n|



#### 7.1.1 Wi-Fi RF Transmitter (TX) Characteristics

Table 7-2. TX Power with Spectral Mask and EVM Meeting 802.11 Standards

|Rt|Min|Typ|Max|
|---|---|---|---|
|ae|(dBm)|(dBm)|(dBm)|
|802.11b, 1 Mbps|—|20.5|—|
|802.11b, 11 Mbps|—|20.5|—|
|802.11g, 6 Mbps|—|20.0|—|
|802.11g, 54 Mbps|—|18.0|—|
|802.11n, HT20, MCS0|—|19.0|—|
|802.11n, HT20, MCS7|—|17.5|—|
|802.11n, HT40, MCS0|—|18.5|—|
|802.11n, HT40, MCS7|—|17.0|—|



Table 7-3. TX EVM Test<sup>1</sup>

|Rate|Min|Typ|Limit|
|---|---|---|---|
||(dB)|(dB)|(dB)|
|802.11b, 1 Mbps, @20.5 dBm|—|–24.5|–10|
|802.11b, 11 Mbps, @20.5 dBm|—|–25.0|–10|
|802.11g, 6 Mbps, @20 dBm|—|–23.0|–5|
|802.11g, 54 Mbps, @18 dBm|—|–28.0|–25|



Cont’d on next page

Espressif Systems

25 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

7 RF Characteristics

Table 7-3 – cont’d from previous page

|Rate|Min<br>(dB)|Typ<br>(dB)|Limit<br>(dB)|
|---|---|---|---|
|802.11n, HT20, MCS0, @19 dBm|—|–23.5|–5|
|802.11n, HT20, MCS7, @17.5 dBm|—|–30.5|–27|
|802.11n, HT40, MCS0, @18.5 dBm|—|–26.5|–5|
|802.11n, HT40, MCS7, @17 dBm|—|–30.5|–27|



- 1 EVM is measured at the corresponding typical TX power provided in Table 7-2 _TX Power with Spectral Mask and EVM Meeting 802.11 Standards_ above.

#### 7.1.2 Wi-Fi RF Receiver (RX) Characteristics

For RX tests, the PER (packet error rate) limit is 8% for 802.11b, and 10% for 802.11g/n.

Table 7-4. RX Sensitivity

|Rate|Min<br>(dBm)|Typ<br>(dBm)|Max<br>(dBm)|
|---|---|---|---|
|802.11b, 1 Mbps|—|–98.0|—|
|802.11b, 2 Mbps|—|–96.0|—|
|802.11b, 5.5 Mbps|—|–93.0|—|
|802.11b, 11 Mbps|—|–88.6|—|
|802.11g, 6 Mbps|—|–92.8|—|
|802.11g, 9 Mbps|—|–91.8|—|
|802.11g, 12 Mbps|—|–90.8|—|
|802.11g, 18 Mbps|—|–88.4|—|
|802.11g, 24 Mbps|—|–85.4|—|
|802.11g, 36 Mbps|—|–82.0|—|
|802.11g, 48 Mbps|—|–77.8|—|
|802.11g, 54 Mbps|—|–76.2|—|
|802.11n, HT20, MCS0|—|–92.6|—|
|802.11n, HT20, MCS1|—|–90.6|—|
|802.11n, HT20, MCS2|—|–88.0|—|
|802.11n, HT20, MCS3|—|–84.8|—|
|802.11n, HT20, MCS4|—|–81.6|—|
|802.11n, HT20, MCS5|—|–77.4|—|
|802.11n, HT20, MCS6|—|–75.6|—|
|802.11n, HT20, MCS7|—|–74.4|—|
|802.11n, HT40, MCS0|—|–90.0|—|
|802.11n, HT40, MCS1|—|–87.6|—|
|802.11n, HT40, MCS2|—|–84.8|—|
|802.11n, HT40, MCS3|—|–81.8|—|
|802.11n, HT40, MCS4|—|–78.4|—|
|802.11n, HT40, MCS5|—|–74.2|—|



Cont’d on next page

Espressif Systems

26 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

7 RF Characteristics

Table 7-4 – cont’d from previous page

|Rate|Min<br>(dBm)|Typ<br>(dBm)|Max<br>(dBm)|
|---|---|---|---|
|802.11n, HT40, MCS6|—|–72.6|—|
|802.11n, HT40, MCS7|—|–71.2|—|



Table 7-5. Maximum RX Level

|Rt|Min|Typ|Max|
|---|---|---|---|
|ae|(dBm)|(dBm)|(dBm)|
|802.11b, 1 Mbps|—|5|—|
|802.11b, 11 Mbps|—|5|—|
|802.11g, 6 Mbps|—|5|—|
|802.11g, 54 Mbps|—|0|—|
|802.11n, HT20, MCS0|—|5|—|
|802.11n, HT20, MCS7|—|0|—|
|802.11n, HT40, MCS0|—|5|—|
|802.11n, HT40, MCS7|—|0|—|



Table 7-6. RX Adjacent Channel Rejection

|Rate|Min<br>(dB)|Typ<br>(dB)|Max<br>(dB)|
|---|---|---|---|
|802.11b, 1 Mbps|—|35|—|
|802.11b, 11 Mbps|—|35|—|
|802.11g, 6 Mbps|—|31|—|
|802.11g, 54 Mbps|—|14|—|
|802.11n, HT20, MCS0|—|31|—|
|802.11n, HT20, MCS7|—|13|—|
|802.11n, HT40, MCS0|—|19|—|
|802.11n, HT40, MCS7|—|8|—|



### 7.2 Bluetooth 5 (LE) Radio

#### 7.2.1 Bluetooth LE RF Transmitter (TX) Characteristics

Table 7-7. Bluetooth LE RF Characteristics

|Name|Description|
|---|---|
|Center frequency range of operatingchannel|2402~2480 MHz|
|RF transmit power range|–24.0~20.0 dBm|



Espressif Systems

27 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

7 RF Characteristics

Table 7-8. Bluetooth LE - Transmitter Characteristics - 1 Mbps

|Parameter|Description|Min|Typ|Max|Unit|
|---|---|---|---|---|---|
||F = F0 ± 2 MHz|—|–37.62|—|dBm|
|In-band emissions|F = F0 ± 3 MHz|—|–41.95|—|dBm|
||F = F0 ± > 3 MHz|—|–44.48|—|dBm|
||∆_f_1avg|—|245.00|—|kHz|
|Modulation characteristics|∆_f_2max|—|208.00|—|kHz|
||∆_f_2avg/∆_f_1avg|—|0.93|—|—|
|Carrier frequency offset|—|—|–9.00|—|kHz|
||_|f_0 _−fn|n_=2_,_ 3_,_ 4_, ..k_|—|1.17|—|kHz|
|Carrier frequency drift|_|f_1 _−f_0_|_|—|0.30|—|kHz|
||_|fn −fn−_5_|n_=6_,_ 7_,_ 8_, ..k_|—|4.90|—|kHz|



Table 7-9. Bluetooth LE - Transmitter Characteristics - 2 Mbps

|Parameter|Description|Min|Typ|Max|Unit|
|---|---|---|---|---|---|
||F = F0 ± 4 MHz|—|–43.55|—|dBm|
|In-band emissions|F = F0 ± 5 MHz|—|–45.26|—|dBm|
||F = F0 ± > 5 MHz|—|–47.00|—|dBm|
||∆_f_1avg|—|497.00|—|kHz|
|Modulation characteristics|∆_f_2max|—|398.00|—|kHz|
||∆_f_2avg/∆_f_1avg|—|0.95|—|—|
|Carrier frequency offset|—|—|–9.00|—|kHz|
||_|f_0 _−fn|n_=2_,_ 3_,_ 4_, ..k_|—|0.46|—|kHz|
|Carrier frequency drift|_|f_1 _−f_0_|_|—|0.70|—|kHz|
||_|fn −fn−_5_|n_=6_,_ 7_,_ 8_, ..k_|—|6.80|—|kHz|



Table 7-10. Bluetooth LE - Transmitter Characteristics - 125 Kbps

|Parameter|Description|Min|Typ|Max|Unit|
|---|---|---|---|---|---|
||F = F0 ± 2 MHz|—|–37.90|—|dBm|
|In-band emissions|F = F0 ± 3 MHz|—|–41.00|—|dBm|
||F = F0 ± > 3 MHz|—|–42.50|—|dBm|
|Modulation characteristics|∆_f_1avg|—|252.00|—|kHz|
||∆_f_1max|—|200.00|—|kHz|
|Carrier frequency offset|—|—|–13.70|—|kHz|
||_|f_0 _−fn|n_=1_,_ 2_,_ 3_, ..k_|—|1.52|—|kHz|
|Carrier frequency drift|_|f_0 _−f_3_|_|—|0.65|—|kHz|
||_|fn −fn−_3_|n_=7_,_ 8_,_ 9_, ..k_|—|0.70|—|kHz|



Espressif Systems

28 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

7 RF Characteristics

Table 7-11. Bluetooth LE - Transmitter Characteristics - 500 Kbps

|Parameter|Description|Min|Typ|Max|Unit|
|---|---|---|---|---|---|
||F = F0 ± 2 MHz|—|–37.90|—|dBm|
|In-band emissions|F = F0 ± 3 MHz|—|–41.30|—|dBm|
||F = F0 ± > 3 MHz|—|–42.80|—|dBm|
|Modulation characteristics|∆_f_2avg|—|220.00|—|kHz|
||∆_f_2max|—|205.00|—|kHz|
|Carrier frequency offset|—|—|–11.90|—|kHz|
||_|f_0 _−fn|n_=1_,_ 2_,_ 3_, ..k_|—|1.37|—|kHz|
|Carrier frequency drift|_|f_0 _−f_3_|_|—|1.09|—|kHz|
||_|fn −fn−_3_|n_=7_,_ 8_,_ 9_, ..k_|—|0.51|—|kHz|



#### 7.2.2 Bluetooth LE RF Receiver (RX) Characteristics

Table 7-12. Bluetooth LE - Receiver Characteristics - 1 Mbps

|Parameter|Description|Min|Typ|Max|Unit|
|---|---|---|---|---|---|
|Sensitivity @30.8% PER|—|—|–96|—|dBm|
|Maximum received signal @30.8% PER|—|—|10|—|dBm|
|Co-channel C/I|—|—|8|—|dB|
||F = F0 + 1 MHz|—|–4|—|dB|
||F = F0 – 1 MHz|—|–3|—|dB|
|Adt hl ltiit C/I|F = F0 + 2 MHz|—|–32|—|dB|
|jacen canne seecvy|F = F0 – 2 MHz|—|–36|—|dB|
||F_≥_F0 + 3 MHz<sup>(1)</sup>|—|—|—|dB|
||F_≤_F0 – 3 MHz|—|–39|—|dB|
|Image frequency|—|—|–29|—|dB|
|hl|F = F_image_ + 1 MHz|—|–38|—|dB|
|Adjacent canne to image frequency|F = F_image_ – 1 MHz|—|–34|—|dB|
||30 MHz~2000 MHz|—|–9|—|dBm|
||2003 MHz~2399 MHz|—|–18|—|dBm|
|Out-of-band blocking performance|2484 MHz~2997 MHz|—|–16|—|dBm|
||3000 MHz~12.75 GHz|—|–6|—|dBm|
|Intermodulation|—|—|–44|—|dBm|



1 Refer to the value of Adjacent channel to image frequency when F = F _image_ – 1 MHz.

Espressif Systems

29

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

<u>Submit Documentation Feedback</u>

7 RF Characteristics

Table 7-13. Bluetooth LE - Receiver Characteristics - 2 Mbps

|Parameter|Description|Min|Typ|Max|Unit|
|---|---|---|---|---|---|
|Sensitivity @30.8% PER|—|—|–93|—|dBm|
|Maximum received signal @30.8% PER|—|—|0|—|dBm|
|Co-channel C/I|—|—|10|—|dB|
||F = F0 + 2 MHz|—|–7|—|dB|
||F = F0 – 2 MHz|—|–7|—|dB|
|Adt hl ltiit C/I|F = F0 + 4 MHz<sup>(1)</sup>|—|—|—|dB|
|jacen canne seecvy|F = F0 – 4 MHz|—|–34|—|dB|
||F_≥_F0 + 6 MHz|—|–39|—|dB|
||F_≤_F0 – 6 MHz|—|–39|—|dB|
|Image frequency|—|—|–27|—|dB|
|Ad hl  i f|F = F_image_ + 2 MHz|—|–39|—|dB|
|jacent canne to mage requency|F = F_image_ – 2 MHz<sup>(2)</sup>|—|—|—|dB|
||30 MHz~2000 MHz|—|–17|—|dBm|
||2003 MHz~2399 MHz|—|–19|—|dBm|
|Out-of-band blocking performance|2484 MHz~2997 MHz|—|–16|—|dBm|
||3000 MHz~12.75 GHz|—|–22|—|dBm|
|Intermodulation|—|—|–40|—|dBm|



1 Refer to the value of Image frequency.

2 Refer to the value of Adjacent channel selectivity C/I when F = F0 + 2 MHz.

Table 7-14. Bluetooth LE - Receiver Characteristics - 125 Kbps

|Parameter|Description|Min|Typ|Max|Unit|
|---|---|---|---|---|---|
|Sensitivity @30.8% PER|—|—|–104|—|dBm|
|Maximum received signal @30.8% PER|—|—|10|—|dBm|
|Co-channel C/I|—|—|2|—|dB|
||F = F0 + 1 MHz|—|–6|—|dB|
||F = F0 – 1 MHz|—|–5|—|dB|
|Ad hl lii C/I|F = F0 + 2 MHz|—|–40|—|dB|
|jacent canne seectvty|F = F0 – 2 MHz|—|–42|—|dB|
||F_≥_F0 + 3 MHz<sup>(1)</sup>|—|—|—|dB|
||F_≤_F0 – 3 MHz|—|–46|—|dB|
|Image frequency|—|—|–34|—|dB|
|Ad hl  i f|F = F_image_ + 1 MHz|—|–44|—|dB|
|jacent canne to mage requency|F = F_image_ – 1 MHz|—|–37|—|dB|



1 Refer to the value of Adjacent channel to image frequency when F = F _image_ – 1 MHz.

Espressif Systems

30 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

7 RF Characteristics

Table 7-15. Bluetooth LE - Receiver Characteristics - 500 Kbps

|Parameter|Description|Min|Typ|Max|Unit|
|---|---|---|---|---|---|
|Sensitivity @30.8% PER|—|—|–99|—|dBm|
|Maximum received signal @30.8% PER|—|—|10|—|dBm|
|Co-channel C/I|—|—|3|—|dB|
||F = F0 + 1 MHz|—|–5|—|dB|
||F = F0 – 1 MHz|—|–7|—|dB|
|Adnt hnnl ltiit C/I|F = F0 + 2 MHz|—|–39|—|dB|
|jace cae seecvy|F = F0 – 2 MHz|—|–40|—|dB|
||F_≥_F0 + 3 MHz<sup>(1)</sup>|—|—|—|dB|
||F_≤_F0 – 3 MHz|—|–40|—|dB|
|Image frequency|—|—|–34|—|dB|
|Adnt hnnl t im fn|F = F_image_ + 1 MHz|—|–43|—|dB|
|jace cae o age requecy|F = F_image_ – 1 MHz|—|–38|—|dB|



1 Refer to the value of Adjacent channel to image frequency when F = F _image_ – 1 MHz.

Espressif Systems

31

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

<u>Submit Documentation Feedback</u>

## 8 Module Schematics

Thi ~~s is the reference design of the module.~~



<!-- Start of picture text -->
GND<br>GND GND<br>U1<br>The values of C1 and C2 vary with C1 C2<br>the selection of the crystal. TBD TBD<br>The value of R1 varies with the<br>actual PCB board. R1 could be a<br>resistor or inductor, the initial<br>VDD33 value is suggested to be 24 nH.<br>GND<br>40MHz(±10ppm)<br>C3 C4 R2 499 U0TXD GND<br>U0RXD<br>1uF 10nF GPIO19<br>VDD33 GND GND GND GPIO18<br>L1 2.0nH<br>C5 C6 C7<br>10uF 0.1uF 0.1uF 53 50<br>GND GND<br>GND GND GND VDD33 1 35<br>2 GND NC 34<br>ANT1 50 ohm Impedance Control 3 GND NC 33<br>1 RF_ANT L2 TBD LNA_IN 1 24 4 3V3 NC 32<br>2 2 LNA_IN SPIQ 23 VDD_SPI VDD33 GPIO2 5 NC NC 31 U0TXD<br>PCB_ANT C8TBD TBDC9 GPIO0GPIO1 345 VDD3P3VDD3P3XTAL_32K_P SPICLKSPICS0SPID 222120 SPICS0 R8 10K(NC) GPIO3CHIP_EN 678 IO2IO3NC ESP32-C3-MINI-1 RXD0TXD0NC 302928 U0RXD<br>GPIO2 6 XTAL_32K_N SPIWP 19 D1 9 EN NC 27 GPIO19<br>GND GND GND CHIPGPIO3_EN 78 GPIO2CHIP_EN VDD_SPISPIHD 1817 ESD 1011 NCNC IO19IO18 2625 GPIO18<br>GPIO3 VDD3P3_CPU GND NC<br>The values of C8, L2 and C9vary with the actual PCB board. C100.1uF 1uFC11 VDD33 GND 52 GND GND 51<br>NC: No component.<br>GND GND<br>U2 ESP32-C3FH4<br>VDD33<br>GPIO4<br>GPIO5 GND<br>GPIO6 C12<br>GPIO7<br>GPIO8GPIO9 0.1uF ESP32-C3-MINI-1(pin-out)<br>GPIO10<br>GND<br>4 3<br>GND XOUT<br>XIN GND<br>1 2<br>0<br>R1<br>33 32 31 30 29 28 27 26 25 49 48 47 46 45 44 43 42 41 40 39 38 37 36<br>GND VDDA VDDA XTAL_P XTAL_N U0TXD U0RXD GPIO19 GPIO18 EPAD GND GND GND GND GND GND GND GND GND GND GND GND GND<br>32<br>Submit Documentation Feedback<br>IO0 IO1 GND NC IO10 NC IO4 IO5 IO6 IO7 IO8 IO9 NC<br>12 13 14 15 16 17 18 19 20 21 22 23 24<br>MTMS MTDI VDD3P3_RTC MTCK MTDO GPIO8 GPIO9 GPIO10<br>9 10 11 12 13 14 15 16<br>GPIO0 GPIO1 GPIO10 GPIO4 GPIO5 GPIO6 GPIO7 GPIO8 GPIO9<br>ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2<br><!-- End of picture text -->

Figure 8-1. ESP32-C3-MINI-1 Schematics



<!-- Start of picture text -->
GND<br>GND GND<br>U1<br>The values of C1 and C2 vary with C1 C2<br>the selection of the crystal. TBD TBD<br>The value of R1 varies with the<br>actual PCB board. R1 could be a<br>resistor or inductor, the initial<br>VDD33 value is suggested to be 24 nH.<br>GND<br>40MHz(±10ppm)<br>C3 C4 R2 499 U0TXD GND<br>U0RXD<br>1uF 10nF GPIO19<br>VDD33 GND GND GND GPIO18<br>L1 2.0nH<br>C5 C6 C7<br>10uF 0.1uF 0.1uF 53 50<br>GND GND<br>GND GND GND VDD33 1 35<br>2 GND NC 34<br>50 ohm Impedance Control 3 GND NC 33<br>1 RF_ANT L2 TBD LNA_IN 1 24 4 3V3 NC 32<br>2 LNA_IN SPIQ 23 VDD_SPI VDD33 GPIO2 5 NC NC 31 U0TXD<br>ANT1CONN C8TBD TBDC9 GPIO0GPIO1 345 VDD3P3VDD3P3XTAL_32K_P SPICLKSPICS0SPID 222120 SPICS0 R8 10K(NC) GPIO3CHIP_EN 678 IO2IO3NC ESP32-C3-MINI-1U RXD0TXD0NC 302928 U0RXD<br>GPIO2 6 XTAL_32K_N SPIWP 19 D1 9 EN NC 27 GPIO19<br>GND GND GND CHIPGPIO3_EN 78 GPIO2CHIP_EN VDD_SPISPIHD 1817 ESD 1011 NCNC IO19IO18 2625 GPIO18<br>GPIO3 VDD3P3_CPU GND NC<br>The values of C8, L2 and C9vary with the actual PCB board. C100.1uF 1uFC11 VDD33 GND 52 GND GND 51<br>NC: No component.<br>GND GND<br>U2 ESP32-C3FH4<br>VDD33<br>GPIO4<br>GPIO5 GND<br>GPIO6 C12<br>GPIO7<br>GPIO8GPIO9 0.1uF ESP32-C3-MINI-1U(pin-out)<br>GPIO10<br>GND<br>4 3<br>GND XOUT<br>XIN GND<br>1 2<br>0<br>R1<br>33 32 31 30 29 28 27 26 25 49 48 47 46 45 44 43 42 41 40 39 38 37 36<br>GND VDDA VDDA XTAL_P XTAL_N U0TXD U0RXD GPIO19 GPIO18 EPAD GND GND GND GND GND GND GND GND GND GND GND GND GND<br>4 3 2<br>IO0 IO1 GND NC IO10 NC IO4 IO5 IO6 IO7 IO8 IO9 NC<br>12 13 14 15 16 17 18 19 20 21 22 23 24<br>MTMS MTDI VDD3P3_RTC MTCK MTDO GPIO8 GPIO9 GPIO10<br>9 10 11 12 13 14 15 16<br>GPIO0 GPIO1 GPIO10 GPIO4 GPIO5 GPIO6 GPIO7 GPIO8 GPIO9<br><!-- End of picture text -->

Figure 8-2. ESP32-C3-MINI-1U Schematics

~~9 Peripheral Schematics~~

## 9 Peripheral Schematics

This is the typical application circuit of the module connected with peripheral components (for example, power supply, antenna, reset button, JTAG interface, and UART interface).



<!-- Start of picture text -->
GND<br>53 50 VDD33<br>VDD33 GND GND JP4<br>1 35 1<br>R9 10K 2 GND NC 34 2 1<br>3 GND NC 33 3 2<br>4 3V3 NC 32 4 3<br>C1 C2 R1 IO2 5 NC NC 31 TXD0 4<br>IO3 6 IO2 ESP32-C3-MINI-1 TXD0 30 RXD0 UART<br>10uF 0.1uF TBD 7 IO3 ESP32-C3-MINI-1U RXD0 29 GND<br>EN 8 NC NC 28 JP3<br>9 EN NC 27 IO19 R4 0 USB_D+ 1<br>10 NC IO19 26 IO18 R6 0 USB_D- 2 1<br>C3 11 NC IO18 25 2<br>GND NC<br>C5 C6 USB<br>TBD 52 51<br>GND GND TBD TBD<br>GND GND<br>U1<br>GND GND GND<br>GND C7 12pF(NC) VDD33<br>X1 R5 0(NC) R8 10K<br>32.768kHz(NC) R6 0(NC) SW1<br>JP2 R2 0 EN<br>1 TMS 1<br>GND C8 12pF(NC) JP1 1 2 TDI 2 1 C4 0.1uF<br>JTAG 2 3 TCK 2<br>NC: No component. 3 4 TDO Boot Option<br>4<br>GND GND<br>49 48 47 46 45 44 43 42 41 40 39 38 37 36<br>EPAD GND GND GND GND GND GND GND GND GND GND GND GND GND<br>IO0 IO1 GND NC IO10 NC IO4 IO5 IO6 IO7 IO8 IO9 NC<br>12 13 14 15 16 17 18 19 20 21 22 23 24<br>IO0 IO1 IO10 IO4 IO5 IO6 IO7 IO8 IO9<br>1 R7<br>2 NC<br><!-- End of picture text -->

Figure 9-1. Peripheral Schematics

- Soldering the EPAD to the ground of the base board is not a must, however, it can optimize thermal performance. If you choose to solder it, please apply the correct amount of soldering paste. Too much soldering paste may increase the gap between the module and the baseboard. As a result, the adhesion between other pins and the baseboard may be poor.

- To ensure that the power supply to the ESP32-C3 chip is stable during power-up, it is advised to add an RC delay circuit at the EN pin. The recommended setting for the RC delay circuit is usually R = 10 kΩ and C = 1 _µ_ F. However, specific parameters should be adjusted based on the power-up timing of the module and the power-up and reset sequence timing of the chip. For ESP32-C3’s power-up and reset sequence timing diagram, please refer Section 4.3 _Chip Power-up and Reset_ .

- UART0 is used to download firmware and log output. When using the AT firmware, note that the UART GPIO is already configured. It is recommended to use the default configuration. Please refer to _~~<u>ESP-AT User Guide for ESP32-C3</u>~~_ ~~> Section~~ _~~Hardware Connection~~_ ~~.~~

Espressif Systems

34 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

10 Physical Dimensions

## 10 Physical Dimensions

### 10.1 Module Dimensions



<!-- Start of picture text -->
Unit: mm<br>13.2±0.15 0.8<br>1.45 0.6<br>11.95<br>5.4<br>0.62 2.4±0.15 8.4<br>9.2<br>10<br>11<br>11.2<br>12.6<br>Top view Side view Bottom view<br>Ø0.5<br>16.6±0.15 9.95 10.6 9.2 9 8.4 7.6 6.8 5.4 1.45 0.6 11.2<br>0.62<br><!-- End of picture text -->

Figure 10-1. ESP32-C3-MINI-1 Physical Dimensions



<!-- Start of picture text -->
Unit: mm<br>13.2±0.15 0.8<br>1.7 0.85<br>9.18<br>1.45 0.6<br>12.25<br>5.4<br>8.4<br>0.47 2.4±0.15<br>9.2<br>10<br>11<br>11.2<br>12.6<br>Top view Side view Bottom view<br>1.55<br>12.5±0.15 8.7 11.55 10.6 9.2 9 8.4 7.6 6.8 5.4 1.45 0.6<br>0.48 5.6<br><!-- End of picture text -->

Figure 10-2. ESP32-C3-MINI-1U Physical Dimensions

Note:

For information about tape, reel, and product marking, please refer to _ESP32-C3 Module Packaging Information_ .

Espressif Systems

35 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

10 Physical Dimensions

### 10.2 Dimensions of External Antenna Connector

ESP32-C3-MINI-1U uses the third generation external antenna connector as shown in Figure 10-3 _Dimensions of External Antenna Connector_ . This connector is compatible with the following connectors:

- W.FL Series connector from Hirose

- MHF III connector from I-PEX

- AMC connector from Amphenol



<!-- Start of picture text -->
CONTACT<br>A<br>A<br>GROUND CONTACT<br>1.7 2.05<br>1.7 2 .0<br><!-- End of picture text -->



<!-- Start of picture text -->
0.10<br>0.57<br>0.85<br><!-- End of picture text -->



<!-- Start of picture text -->
CONTACT<br>HOUSING<br>SHELL<br>SECTION: A- A<br>SCALE: 1 : 1<br>1 . 40<br><!-- End of picture text -->

Figure 10-3. Dimensions of External Antenna Connector

The external antenna used for ESP32-C3-MINI-1U during certification testing is the third generation monopole antenna, with material code TFPD08H10060011.

The module does not include an external antenna upon shipment. If needed, select a suitable external

Espressif Systems

36 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

10 Physical Dimensions

antenna based on the product’s usage environment and performance requirements.

It is recommended to select an antenna that meets the following requirements:

- 2.4 GHz band

- 50 Ω impedance

- The maximum gain does not exceed 2.33 dBi, the gain of the antenna used for certification

- The connector matches the specifications shown in Figure 10-3 _Dimensions of External Antenna Connector_

###### Note:

If you use an external antenna of a different type or gain, additional testing, such as EMC, may be required beyond the existing antenna test reports for Espressif modules. Specific requirements depend on the certification type.

Espressif Systems

37

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

<u>Submit Documentation Feedback</u>

11 PCB Layout Recommendations

## 11 PCB Layout Recommendations

### 11.1 PCB Land Pattern

This section provides the following resources for your reference:

- Figures for recommended PCB land patterns with all the dimensions needed for PCB design. See Figure 11-1 _ESP32-C3-MINI-1 Recommended PCB Land Pattern_ and Figure 11-2 _ESP32-C3-MINI-1U Recommended PCB Land Pattern_ .

- Source files of recommended PCB land patterns to measure dimensions not covered in Figure 11-1 and Figure 11-2. You can view the source files for <u>ESP32-C3-MINI-1</u> and <u>ESP32-C3-MINI-1U</u> with <u>Autodesk Viewer.</u>

- 3D models of <u>ESP32-C3-MINI-1</u> and <u>ESP32-C3-MINI-1U. Please make sure that you download the 3D</u> model file in .STEP format. Beware that some browsers might add .txt.



<!-- Start of picture text -->
Unit: mm<br>Via for thermal pad<br>Pad<br>13.2<br>Pin 1<br>Antenna Area<br>48 x 0.4 4 x 0.7<br>0.6 1.45<br>5.4<br>1.6<br>11.8<br>11.9<br>9.9 9.8 1.6 5.4 0.6 4 x 0.7 11.2 16.6<br>48 x 0.8 1.45<br>0.8<br><!-- End of picture text -->

Figure 11-1. ESP32-C3-MINI-1 Recommended PCB Land Pattern

Espressif Systems

38 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

11 PCB Layout Recommendations



<!-- Start of picture text -->
Unit: mm<br>Via for thermal pad<br>Pad<br>13.2<br>Pin 1<br>48 x 0.4 4 x 0.7<br>0.6 1.45<br>5.4<br>1.6<br>11.8<br>11.9<br>9.9 9.8 1.6 5.4 0.6 4 x 0.7 12.5<br>48 x 0.8 1.45<br>0.8 5.6<br><!-- End of picture text -->

Figure 11-2. ESP32-C3-MINI-1U Recommended PCB Land Pattern

### 11.2 Module Placement for PCB Design

If module-on-board design is adopted, attention should be paid while positioning the module on the base board. The interference of the base board on the module’s antenna performance should be minimized.

For details about module placement for PCB design, please refer to _<u>ESP32-C3 Hardware Design Guidelines</u>_ > Section _General Principles of PCB Layout for Modules_ .

Espressif Systems

39 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

12 Product Handling

## 12 Product Handling

### 12.1 Storage Conditions

The products sealed in moisture barrier bags (MBB) should be stored in a non-condensing atmospheric environment of < 40 °C and 90%RH. The module is rated at the moisture sensitivity level (MSL) of 3.

After unpacking, the module must be soldered within 168 hours with the factory conditions 25±5 °C and 60%RH. If the above conditions are not met, the module needs to be baked.

### 12.2 Electrostatic Discharge (ESD)

- Human body model (HBM): ±2000 V

- Charged-device model (CDM): ±500 V

### 12.3 Reflow Profile

Solder the module in a single reflow.



<!-- Start of picture text -->
Peak temperature: 235 – 250 °C<br>Peak time: 30 – 70 s<br>Temperature (°C)<br>Soldering time: ＞ 30 s<br>Solder: Sn-Ag-Cu (SAC305) lead-free solder<br>250<br>230<br>217<br>200<br>180<br>150<br>100<br>50<br>Ramp-up Preheating Soldering Cooling<br>25 – 150 °C 150 – 200 °C ＞ 217 °C ＜ 180 °C<br>25 60 – 90 s 60 – 120 s 60 – 90 s –5 ~ –1 °C/s<br>1 – 3 °C/s<br>Time (s)<br>0<br>50 100 150 200 250<br><!-- End of picture text -->

Figure 12-1. Reflow Profile

Espressif Systems

40 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

12 Product Handling

### 12.4 Ultrasonic Vibration

Avoid exposing Espressif modules to vibration from ultrasonic equipment, such as ultrasonic welders or ultrasonic cleaners. This vibration may induce resonance in the in-module crystal and lead to its malfunction or even failure. As a consequence, the module may stop working or its performance may deteriorate.

Espressif Systems

41 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

_Datasheet Versioning_

## Datasheet Versioning

|Datasheet<br>Version|Status|Watermark|Definition|
|---|---|---|---|
|v0.1 ~ v0.5<br>(excluding v0.5)|Draft|Confidential|This datasheet is under development for products<br>in the design stage. Specifications may change<br>without prior notice.|
|v0.5 ~ v1.0<br>(excluding v1.0)|Preliminary<br>release|Preliminary|This datasheet is actively updated for products in<br>the verification stage. Specifications may change<br>before mass production, and the changes will be<br>documentation in the datasheet’s Revision History.|
|v1.0 and higher|Official release|—|This datasheet is publicly released for products in<br>mass production. Specifications are finalized, and<br>major changes will be communicated via<br>Product<br>Change<br>Notifications<br>(PCN).|
|Any version|—|Not<br>Recommended<br>for New Design<br>(NRND)<sup>1</sup>|This datasheet is updated less frequently for<br>products not recommended for new designs.|
|Any version|—|End of Life<br>(EOL)<sup>2</sup>|This datasheet is no longer mtained for products<br>that have reached end of life.|



> 1 Watermark will be added to the datasheet title page only when all the product variants covered by this datasheet are not recommended for new designs.

> 2 Watermark will be added to the datasheet title page only when all the product variants covered by this datasheet have reached end of life.

Espressif Systems

42 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

_Related Documentation and Resources_

## Related Documentation and Resources

### Related Documentation

- _<u>ESP32-C3 Series Datasheet</u>_ - Specifications of the ESP32-C3 hardware.

- _<u>ESP32-C3 Technical Reference Manual</u>_ – Detailed information on how to use the ESP32-C3 memory and peripherals.

- _<u>ESP32-C3 Hardware Design Guidelines</u>_ – Guidelines on how to integrate the ESP32-C3 into your hardware product.

- _<u>ESP32-C3 Series SoC Errata</u>_ – Descriptions of known errors in ESP32-C3 series of SoCs.

- _Certificates_

<u>https://espressif.com/en/support/documents/certifcatesi</u>

- _ESP32-C3 Product/Process Change Notifications (PCN)_

<u>https://espressif.com/en/support/documents/pcns?keys=ESP32-C3</u>

- _ESP32-C3 Advisories_ – Information on security, bugs, compatibility, component reliability. <u>https://espressif.com/en/support/documents/advisories?keys=ESP32-C3</u>

- _Documentation Updates and Update Notification Subscription_ <u>https://espressif.com/en/support/download/documents</u>

### Developer Zone

- <u>ESP-IDF Programming Guide for ESP32-C3</u> – Extensive documentation for the ESP-IDF development framework.

- _ESP-IDF_ and other development frameworks on GitHub. <u>https://github.com/espressif</u>

- _ESP32 BBS Forum_ – Engineer-to-Engineer (E2E) Community for Espressif products where you can post questions, share knowledge, explore ideas, and help solve problems with fellow engineers.

- <u>https://esp32.com/</u>

- _ESP-FAQ_ – A summary document of frequently asked questions released by Espressif. <u>https://espressif.com/projects/esp-faq/en/latest/index.html</u>

- _The ESP Journal_ – Best Practices, Articles, and Notes from Espressif folks. <u>https://blog.espressif.com/</u>

- See the tabs _SDKs and Demos_ , _Apps_ , _Tools_ , _AT Firmware_ .

<u>https://espressif.com/en/support/download/sdks-demos</u>

### Products

- _ESP32-C3 Series SoCs_ – Browse through all ESP32-C3 SoCs. <u>https://espressif.com/en/products/socs?id=ESP32-C3</u>

- _ESP32-C3 Series Modules_ – Browse through all ESP32-C3-based modules. <u>https://espressif.com/en/products/modules?id=ESP32-C3</u>

- _ESP32-C3 Series DevKits_ – Browse through all ESP32-C3-based devkits.

- <u>https://espressif.com/en/products/devkits?id=ESP32-C3</u>

- _ESP Product Selector_ – Find an Espressif hardware product suitable for your needs by comparing or applying filters. <u>https://products.espressif.com/#/product-selector?language=en</u>

Espressif Systems

43 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

_Related Documentation and Resources_

### Contact Us

- See the tabs _Sales Questions_ , _Technical Enquiries_ , _Circuit Schematic & PCB Design Review_ , _Get Samples_ (Online stores), _Become Our Supplier_ , _Comments & Suggestions_ . <u>https://espressif.com/en/contact-us/sales-questions</u>

Espressif Systems

44

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

<u>Submit Documentation Feedback</u>

_Revision History_

## Revision History

|Date<br>2026-05-06|Version<br>v2.2|Release notes<br>_•_ Added ESP32-C3-MINI-1-H8X<br>_•_ Table 1-1 _ESP32-C3-MINI-1 (ANT) Series Comparison_<sup>1 </sup>and Table 1-<br>2 _ESP32-C3-MINI-1U (CONN) Series Comparison_: Updated ”Ordering<br>Code” to ”Part Number”|
|---|---|---|
|2025-07-14|v2.1|_•_ Added Section4.3_Chip Power-up and Reset_<br>_•_ Added Section6.5_Memory Specifications_<br>_•_ Section9_Peripheral Schematics_: Added a note about AT communication<br>using UART0<br>_•_ Section10.2_Dimensions of External Antenna Connector_: Added the ex-<br>ternal antenna information for certification<br>_•_ AddedDatasheet Versioning|
|2025-04-14|v2.0|According to updates in<br>Compatibility<br>Advisory<br>for<br>ESP32-C3<br>Chip<br>Revision<br>v1.1,<br>updated SRAM space in note 6 for Table _ESP32-C3-MINI-1U (CONN) Series_<br>_Comparison_|
|2025-01-24|v1.9|Updated chip in ESP32-C3-MINI-1-N4 and ESP32-C3-MINI-1U-N4 from ESP32-<br>C3FN4 to ESP32-C3FH4|
|2024-11-20|v1.8|_•_ Table1-1_ESP32-C3-MINI-1 (ANT) Series Comparison_<sup>1 </sup>and1-2_ESP32-C3-_<br>_MINI-1U (CONN) Series Comparison_:<br>– Added the ESP32-C3-MINI-1-N4X, ESP32-C3-MINI-1U-N4X, and<br>ESP32-C3-MINI-1U-H4X variants<br>– Marked the ESP32-C3-MINI-1U-N4 and ESP32-C3-MINI-1U-H4 vari-<br>ants as Not Recommended for New Designs (NRND)<br>_•_ Added Table6-5_Current Consumption for Bluetooth LE in Active Mode_|
|2024-09-19|v1.7|_•_ Table 1-2 _ESP32-C3-MINI-1U (CONN) Series Comparison_: Updated flash<br>program/erase cycles, data retention time (note 4) and maximum clock<br>frequency (note 7)<br>_•_ Improved the wording and structure of following sections:<br>– Updated Section ”Strapping Pins” and renamed to4_Boot Configu-_<br>_rations_<br>– Added Chapter5_Peripherals_<br>– Updated Table ”Wi-Fi RF Standards” and renamed to ”Wi-Fi RF Char-<br>acteristics”<br>– Added Section11.2_Module Placement for PCB Design_<br>– Optimized Figure12-1_Reflow Profile_|



Cont’d on next page

Espressif Systems

45

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

<u>Submit Documentation Feedback</u>

_Revision History_

Cont’d from previous page

|Date|Version|Release notes|
|---|---|---|
|2024-07-29|v1.6|Added<br>Compatibility<br>Advisory<br>for<br>ESP32-C3<br>Chip<br>Revision<br>v1.1 to the notes of<br>Table_ESP32-C3-MINI-1U (CONN) Series Comparison_|
|2024-06-05|v1.5|_•_ Added new variant ESP32-C3-MINI-1-H4X<br>_•_ Marked the ESP32-C3-MINI-1-N4, ESP32-C3-MINI-1-H4, and ESP32-C3-<br>MINI-1-H4-AZ variants as Not Recommended for New Designs (NRND)|
|2024-05-15|v1.4|_•_ Updated note 5 of Table_ESP32-C3-MINI-1 (ANT) Series Comparison_<sup>1 </sup>and<br>Table_ESP32-C3-MINI-1U (CONN) Series Comparison_<br>_•_ Updated the formatting of Section4_Boot Configurations_<br>_•_ Updated the maximum value of ”RF power control range” to 20 dBm in<br>Table_Bluetooth LE RF Characteristics_<br>_•_ Updated the note about solder paste in Section9_Peripheral Schematics_<br>_•_ Updated the markings of dimensions and thermal pad vias in Section11.1<br>_PCB Land Pattern_|
|2022-11-08|v1.3|_•_ Added a new variant ESP32-C3-MINI-1-H4-AZ<br>_•_ Changed Table_Ordering Information_to Table_ESP32-C3-MINI-1 (ANT) Se-_<br>_ries Comparison_<sup>1 </sup>and Table_ESP32-C3-MINI-1U (CONN) Series Compari-_<br>_son_<br>_•_ Updated test condition descriptions and data in Section6.4_Current Con-_<br>_sumption Characteristics_<br>_•_ Updated ”RF power control range” in Table_Bluetooth LE RF Characteris-_<br>_tics_<br>_•_ Added descriptions in Section11.1_PCB Land Pattern_|
|2022-06-30|v1.2|Added Section12.4_Ultrasonic Vibration_|
|2022-05-16|v1.1|_•_ Added a note under Table_Ordering Information_<br>_•_ Updated Chapter8_Module Schematics_|
|2021-06-21|v1.0|_•_ Updated module description on the title page<br>_•_ Deleted Section ”About This Document”<br>_•_ Restructured Section1.1_Features_<br>_•_ Added ordering code in Table_Ordering Information_<br>_•_ Added descriptions in Section10.2_Dimensions of External Antenna Con-_<br>_nector_<br>_•_ Updated Section ”Learning Resources” and renamed to Related Docu-<br>mentation and Resources<br>_•_ Replaced ”chip family” with ”chip series” following Espressif’s taxonomy|
|2021-04-16|v0.7|Added information about ESP32-C3-MINI-1U module|



Cont’d on next page

Espressif Systems

46 <u>Submit Documentation Feedback</u>

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

_Revision History_

##### Cont’d from previous page

|Date|Version|Release notes|
|---|---|---|
|2021-02-22|v0.6|Updated the value of C7 to 0.1_µ_F in Chapter8_Module Schematics_|
|2021-02-05|v0.5|Preliminary release|



Espressif Systems

47

ESP32-C3-MINI-1 & MINI-1U Datasheet v2.2

<u>Submit Documentation Feedback</u>



#### Disclaimer and Copyright Notice

Information in this document, including URL references, is subject to change without notice.

ALL THIRD PARTY’S INFORMATION IN THIS DOCUMENT IS PROVIDED AS IS WITH NO WARRANTIES TO ITS AUTHENTICITY AND ACCURACY.

NO WARRANTY IS PROVIDED TO THIS DOCUMENT FOR ITS MERCHANTABILITY, NON-INFRINGEMENT, FITNESS FOR ANY PARTICULAR PURPOSE, NOR DOES ANY WARRANTY OTHERWISE ARISING OUT OF ANY PROPOSAL, SPECIFICATION OR SAMPLE. All liability, including liability for infringement of any proprietary rights, relating to use of information in this document is disclaimed. No licenses express or implied, by estoppel or otherwise, to any intellectual property rights are granted herein. The Wi-Fi Alliance Member logo is a trademark of the Wi-Fi Alliance. The Bluetooth logo is a registered trademark of Bluetooth SIG. All trade names, trademarks and registered trademarks mentioned in this document are property of their respective owners, and are hereby acknowledged.

Copyright © 2026 Espressif Systems (Shanghai) Co., Ltd. All rights reserved. <u>w.espressif.comww</u>
