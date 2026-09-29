# Space80 R2 (apollo80_r2) Custom Firmware

[中文说明](README.zh-CN.md)

QMK / Vial firmware for the Graystudio **Space80 R2 "Apollo's Cyber Armor"**, with per-LED control (VialRGB) and a standard Windows default keymap.

## Overview

Built on open-source [vial-qmk](https://github.com/vial-kb/vial-qmk).

- Lighting: RGB Matrix engine, 9 hand-picked animations
- Per-LED control: **VialRGB** (protocol + GUI Direct Control)
- Default keymap: **standard Windows (104/TKL order)**
- Caps Lock indicator: badge strip (LEDs 0-5) in white

Verified working on hardware: all keys, Vial recognition, VialRGB (87 LEDs), Caps Lock badge indicator.

## Effects

`breathing`, `hue_breathing`, `hue_pendulum`, `hue_wave`, `gradient_up_down`, `gradient_left_right`, `cycle_all`, `cycle_left_right`, `cycle_up_down`, plus `Disable`, `Solid Color`, and `Direct Control`.

## Default keymap (standard Windows)

Layer 0 is the standard Windows 104/TKL order — `Ctrl Win Alt ... Alt Win Fn Ctrl`, `PrtSc ScrLk Pause` top-right, `Ins Home PgUp / Del End PgDn` column, arrows bottom-right.
Layer 1 (Fn, right of Right-Alt): lighting controls (`UG_*` / `RM_*`), NKRO toggle, **QK_BOOT**, media keys (`VOLD/MUTE/VOLU` top-right), numpad.

## Repository layout

```
space80r2-qmk/
├── keyboards/graystudio/apollo80_r2/    # keyboard definition (drop into a vial-qmk tree)
│   ├── keyboard.json                    # MCU / matrix / LED driver / animations
│   ├── apollo80_r2.c                    # g_led_config (LED map) + Caps Lock hook
│   └── keymaps/vial/                    # keymap.c, config.h, rules.mk, vial.json
├── tools/
│   ├── led_index_test.py                # light a single LED / scan / restore
│   └── led_spot_test.py                 # animated sliding-spot demo (VialRGB streaming)
├── docs/led_map.txt                     # per-LED map notes
├── build.sh                             # one-shot build
├── dfu_commands.sh                      # backup / flash via dfu-util
├── README.md                            # this file (English)
└── README.zh-CN.md                      # Chinese readme
```

## Dependencies (NOT included in this repo)

**This repository ships only the keyboard definition, helper scripts and docs.** It contains no
QMK/vial-qmk sources, no `qmk` CLI, no ARM toolchain and no dfu-util — install them separately:

| Dependency | Notes |
|---|---|
| [vial-qmk](https://github.com/vial-kb/vial-qmk) (vial branch) | QMK/Vial source tree; `build.sh` expects it at `~/Scripts/git/vial-qmk` (edit to taste) |
| [qmk CLI](https://github.com/qmk/qmk_cli) | run inside vial-qmk's `.venv`, or `pip install qmk` |
| [xPack ARM GCC](https://github.com/xpack-dev-tools/arm-none-eabi-gcc-xpack/releases) ≥ 13.x | Homebrew's `arm-none-eabi-gcc` lacks newlib and will fail |
| [dfu-util](https://dfu-util.sourceforge.net/) | flashing (`brew install dfu-util`) |
| Python 3 + [hid](https://pypi.org/project/hid/) | only for `tools/*.py` (`pip install hid`) |

## Build

```bash
./build.sh
# output: build_output/graystudio_apollo80_r2_vial.bin (~41 KB / 128 KB flash)
```
