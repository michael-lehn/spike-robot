# SPIKE Robot (Pybricks) — Quickstart Repo

Minimal setup to program LEGO Education SPIKE Prime with **Pybricks** from the
**terminal** (vim + Makefile).

## Prereqs (macOS)
```bash
brew install python pipx dfu-util
pipx ensurepath
pipx install pybricksdev
```

## Flash Pybricks Firmware
Put the Pybricks firmware ZIP in the repo (default:
`pybricks-primehub-v3.6.1.zip`) or fetch it:
```bash
make fetch-firmware
```
Put the hub into **DFU mode** (turn off → hold center button while plugging USB
→ orange blinking). Then:
```bash
make flash
```
This names the hub after your `$USER` by default.

> To restore the official LEGO firmware later, run `make lego` and use **Tools
> → Restore official LEGO firmware** in the opened page.

## Run Your Program
```bash
make run            # runs main.py
make run FILE=foo.py
```

The BLE connection is handled by `pybricksdev run ble`. Any `print()` in your
program is streamed back to your terminal.

## main.py
- Straight driving by distance
- Right-angle turns
- Circular arcs with chosen radius (center-following)
- Simple demo sequence at the bottom

Tune the geometry constants to your robot: wheel diameter and axle track.

## Repo Layout
```
.
├── Makefile
├── README.md
├── main.py
└── pybricks-primehub-v3.6.1.zip   # (or download with make fetch-firmware)
```
