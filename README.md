# Crimpdeq Hardware

The Crimpdeq hardware is actively evolving. Several people have already built a prototype. Instructions for building your own prototype are available in the [Crimpdeq book](crimpdeq.github.io/book/). In parallel, I'm designing a PCB that is nearly finished but not yet manufactured, so it remains untested.

## Prototype

Here is the prototype:

![Prototype](assets/prototype.png)

The [Making Your Own Crimpdeq](https://crimpdeq.github.io/book/assembly.html) chapter explains the required materials and steps to build your own Crimpdeq.

## PCB

The PCB design is located under `hardware/crimpdeq/` and was created using KiCad. It is a two-layer board based on the [Rust ESP Board](https://github.com/esp-rs/esp-rust-board). This design removes unused sensors from the original board and adds the necessary components for this project.