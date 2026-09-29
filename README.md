# Space80 R2 (apollo80_r2) Custom Firmware / 自定义固件

QMK / Vial firmware rebuild for the Graystudio **Space80 R2 "Apollo's Cyber Armor"**, with per-LED control (VialRGB), a true-to-harness LED coordinate map, and a standard Windows default keymap.

Graystudio **Space80 R2 "Apollo's Cyber Armor"** 的 QMK / Vial 固件重建：支持逐颗灯珠控制（VialRGB）、按实际走线标定的灯珠坐标映射，默认键位为标准 Windows 布局。

> English below / 中文说明见下半部分。

---

## English

### Overview

Built on open-source [vial-qmk](https://github.com/vial-kb/vial-qmk), based on reverse engineering, live protocol reads, and per-LED physical calibration.

- Lighting: RGB Matrix engine, 9 hand-picked animations
- Per-LED control: **VialRGB** (protocol + GUI Direct Control)
- Default keymap: **standard Windows (104/TKL order)**
- Caps Lock indicator: badge strip (LEDs 0-5) in white

Verified working on hardware: all keys, Vial recognition, VialRGB (87 LEDs), Caps Lock badge indicator.

### Hardware (reverse-engineered, verified)

| Item | Value |
|---|---|
| MCU | STM32F072 (128 KB flash / 16 KB RAM) |
| Bootloader | ST ROM DFU (`0483:DF11`); hold **ESC** while plugging in (bootmagic), or short **BOOT0** to 3.3 V |
| USB | VID `0x4753` / PID `0x3080` |
| Matrix | 6 x 17, **COL2ROW**; rows `B5 B4 B3 B1 A2 A1`; cols `B12 B13 B14 B15 A8 B11 B10 B2 B0 A7 A6 A5 A4 A3 B8 B7 B6` |
| LEDs | 87 x WS2812 (GRB) on **B9**, bitbang |
| Vial UID | `{0xD0, 0x75, 0x79, 0xBF, 0x01, 0x05, 0xAC, 0xD2}` |
| Vial unlock combo | **ESC + `` ` ``** (plug in while held) |

### LED mapping (87 LEDs, per-LED calibrated)

| Index | Count | Physical location |
|---|---|---|
| 0–5 | 6 | badge strip (top of keyboard), 0 = leftmost |
| 6–35 | 30 | rear-center → CCW via left side → left-front corner |
| 36–53 | 18 | bottom (front/under) edge, left to right |
| 54–86 | 33 | right-front corner → CCW via right side → rear-center |

86 is physically adjacent to 6 (seam). Raw calibration notes: `docs/led_map_calibration.txt`.

`apollo80_r2.c` uses a hybrid coordinate map, so stock effects behave correctly out of the box:

- `x` = physical horizontal position → `*_left_right` effects sweep left/right, seamless across the 6/86 seam
- `y` = ring arc-length from the seam → `*_up_down` effects start at the seam (86/6) symmetrically and merge at the bottom center (LED 46, middle of 36-53), with an equal hue step per LED

### Effects

9 animations compiled in (keeps flash/RAM lean and the Vial list clean):
`breathing`, `hue_breathing`, `hue_pendulum`, `hue_wave`, `gradient_up_down`, `gradient_left_right`, `cycle_all`, `cycle_left_right`, `cycle_up_down` — plus the always-present `Disable`, `Solid Color`, and `Direct Control`.

Note: `pixel_flow` / `starlight` / `starlight_smooth` are not in the VialRGB protocol enum, so they can never show in the Vial GUI even if compiled in.

### Default keymap (standard Windows)

Layer 0 is the standard Windows 104/TKL order — `Ctrl Win Alt ... Alt Win Fn Ctrl`, `PrtSc ScrLk Pause` top-right, `Ins Home PgUp / Del End PgDn` column, arrows bottom-right.
Layer 1 (Fn, right of Right-Alt): lighting controls (`UG_*` / `RM_*`), NKRO toggle, **QK_BOOT**, media keys (`VOLD/MUTE/VOLU` top-right), numpad.
Layer 2/3: reserved, transparent.

Keymaps live in EEPROM: flashing does not reset your keys. `keymap.c` only provides the default values (reset via Vial, or VIA command `0x06`).

### Repository layout

```
space80r2-qmk/
├── keyboards/graystudio/apollo80_r2/    # keyboard definition (drop into a vial-qmk tree)
│   ├── keyboard.json                    # MCU / matrix / LED driver / animations
│   ├── apollo80_r2.c                    # g_led_config (LED map) + Caps Lock hook
│   └── keymaps/vial/                    # keymap.c, config.h, rules.mk, vial.json
├── tools/
│   ├── led_index_test.py                # light a single LED / scan / restore
│   └── led_spot_test.py                 # animated sliding-spot demo (VialRGB streaming)
├── docs/led_map_calibration.txt         # raw per-LED calibration notes
├── build.sh                             # one-shot build
├── dfu_commands.sh                      # backup / flash via dfu-util
└── README.md
```

### Dependencies (NOT included in this repo)

**This repository ships only the keyboard definition, helper scripts and docs.** It contains no
QMK/vial-qmk sources, no `qmk` CLI, no ARM toolchain and no dfu-util — install them separately:

| Dependency | Notes |
|---|---|
| [vial-qmk](https://github.com/vial-kb/vial-qmk) (vial branch) | QMK/Vial source tree; `build.sh` expects it at `~/Scripts/git/vial-qmk` (edit to taste) |
| [qmk CLI](https://github.com/qmk/qmk_cli) | run inside vial-qmk's `.venv`, or `pip install qmk` |
| [xPack ARM GCC](https://github.com/xpack-dev-tools/arm-none-eabi-gcc-xpack/releases) ≥ 13.x | Homebrew's `arm-none-eabi-gcc` lacks newlib and will fail |
| [dfu-util](https://dfu-util.sourceforge.net/) | flashing (`brew install dfu-util`) |
| Python 3 + [hid](https://pypi.org/project/hid/) | only for `tools/*.py` (`pip install hid`) |

### Build

```bash
./build.sh
# output: build_output/graystudio_apollo80_r2_vial.bin (~41 KB / 128 KB flash)
```

### Flash

```bash
./dfu_commands.sh list      # wait for DFU device
./dfu_commands.sh backup    # full 128 KB flash backup
./dfu_commands.sh flash     # flash build_output/graystudio_apollo80_r2_vial.bin
```

Enter DFU: unplug → hold **ESC** → plug in. If ESC is unavailable (dead matrix), short **BOOT0** to 3.3 V while plugging in. On macOS, plug directly into a built-in USB port; hubs/docks can cause `LIBUSB_ERROR_PIPE`.

### Tools

```bash
/opt/homebrew/bin/python tools/led_index_test.py <0-86>   # single LED on (white)
/opt/homebrew/bin/python tools/led_index_test.py scan     # sweep all LEDs
/opt/homebrew/bin/python tools/led_index_test.py restore  # back to cycle_left_right

/opt/homebrew/bin/python tools/led_spot_test.py           # sliding spot demo
/opt/homebrew/bin/python tools/led_spot_test.py --skip-bottom --width 4
```

Both use the VialRGB raw-HID protocol (usage page `0xFF60`, usage `0x61`, 32-byte reports):

- get info `[0x08,0x40]`, get mode `[0x08,0x41]`, LED count `[0x08,0x43]`
- set mode `[0x07,0x41, id_lo,id_hi, speed, h,s,v]` (DIRECT = 1)
- per-LED fastset `[0x07,0x42, idx_lo,idx_hi, n, (h,s,v)*n]` (max 9 LEDs/packet)

### Gotchas (learned the hard way)

1. **Matrix direction must be COL2ROW.** ROW2COL yields a fully dead matrix while USB/lighting still work.
2. **Vial unlock deadlock:** after `unlock_start (0xFE 0x06)` without completing the ESC+`` ` `` combo, only 6 whitelisted commands are served (including `vial_lock`, which does *not* clear the state) — only a power cycle recovers. Don't probe it casually.
3. Keymaps are EEPROM-resident; flashing never clears them. After keymap experiments, reset via VIA `0x06`.
4. Directional effects use `g_led_config` coordinates; flow/random effects use LED indices — the seam behaves differently between the two families.
5. RAM is the tight resource (~13.3 KB / 16 KB incl. stacks): trimming animations saves flash, not RAM.
6. VialRGB cannot address custom effects — they would be invisible/unselectable in the GUI (protocol enum is fixed upstream).

---

## 中文

### 概述

基于开源 [vial-qmk](https://github.com/vial-kb/vial-qmk) 重建：参数来自静态逆向、VIA/Vial 在线协议读取，以及逐颗灯珠的物理标定。

- 灯效：RGB Matrix 引擎，精选 9 个动画
- 逐颗灯珠控制：**VialRGB**（协议 + GUI Direct Control）
- 默认键位：**标准 Windows（104/TKL 顺序）**
- CapsLock 指示：铭牌排白光（LED 0-5）

已实机验证：全部按键、Vial 识别、VialRGB（87 颗）、CapsLock 铭牌指示。

### 硬件参数（逆向 + 实测）

| 项目 | 值 |
|---|---|
| MCU | STM32F072（128KB Flash / 16KB RAM） |
| 引导 | ST ROM DFU（`0483:DF11`）；**按住 ESC 插线**（bootmagic），或 **BOOT0 短接 3.3V** |
| USB | VID `0x4753` / PID `0x3080` |
| 矩阵 | 6×17，**COL2ROW**；行 `B5 B4 B3 B1 A2 A1`；列 `B12 B13 B14 B15 A8 B11 B10 B2 B0 A7 A6 A5 A4 A3 B8 B7 B6` |
| 灯珠 | 87 颗 WS2812（GRB），数据线 **B9**，bitbang |
| Vial UID | `{0xD0, 0x75, 0x79, 0xBF, 0x01, 0x05, 0xAC, 0xD2}` |
| Vial 解锁组合 | **ESC + `` ` ``**（按住插线） |

### 灯珠映射（87 颗，逐颗标定）

| 索引 | 数量 | 物理位置 |
|---|---|---|
| 0–5 | 6 | 铭牌排（键盘顶部），0 = 最左 |
| 6–35 | 30 | 后侧中央 → 逆时针经左面 → 左前角 |
| 36–53 | 18 | 底面（前/下沿）一排，从左到右 |
| 54–86 | 33 | 右前角 → 逆时针经右面 → 后侧中央 |

86 与 6 物理相邻（接缝）。原始标定记录见 `docs/led_map_calibration.txt`。

`apollo80_r2.c` 使用混合坐标映射，标准灯效开箱即符合直觉：

- `x` = 物理水平位置 → `*_left_right` 系列按左右扫动，在 6/86 接缝处连续无跳变
- `y` = 距接缝的环弧长 → `*_up_down` 系列从接缝（86/6）向两侧对称展开、在底中（LED 46，即 36-53 中间）汇合，且每颗灯珠色差恒定

### 灯效

固件内编译 9 个动画（控制体积、保持 Vial 列表干净）：
`breathing`、`hue_breathing`、`hue_pendulum`、`hue_wave`、`gradient_up_down`、`gradient_left_right`、`cycle_all`、`cycle_left_right`、`cycle_up_down`，外加恒存的 `Disable`、`Solid Color`、`Direct Control`。

注意：`pixel_flow` / `starlight` / `starlight_smooth` 不在 VialRGB 协议枚举内，即使编译进去也不会出现在 Vial GUI。

### 默认键位（标准 Windows）

层 0 为标准 Windows 104/TKL 顺序——`Ctrl Win Alt ... Alt Win Fn Ctrl`，右上三键 `PrtSc ScrLk Pause`，右侧编辑区 `Ins Home PgUp / Del End PgDn`，右下方向键。
层 1（Fn，位于右 Alt 右侧）：灯效控制（`UG_*` / `RM_*`）、NKRO 切换、**QK_BOOT**、媒体键（右上 `VOLD/MUTE/VOLU`）、小键盘。
层 2/3：保留，透明。

键位存储在 EEPROM：刷固件不会清键位。`keymap.c` 只是出厂默认值（可用 Vial 重置，或 VIA 命令 `0x06`）。

### 目录结构

```
space80r2-qmk/
├── keyboards/graystudio/apollo80_r2/    # 键盘定义（拷入 vial-qmk 树即可）
│   ├── keyboard.json                    # MCU / 矩阵 / 灯驱动 / 动画开关
│   ├── apollo80_r2.c                    # g_led_config（灯珠映射）+ CapsLock 钩子
│   └── keymaps/vial/                    # keymap.c, config.h, rules.mk, vial.json
├── tools/
│   ├── led_index_test.py                # 单颗点亮 / 扫描 / 恢复
│   └── led_spot_test.py                 # 滑动光斑演示（VialRGB 推流）
├── docs/led_map_calibration.txt         # 逐颗灯珠标定原始记录
├── build.sh                             # 一键构建
├── dfu_commands.sh                      # dfu-util 备份 / 刷入
└── README.md
```

### 依赖（本仓库不包含）

**本仓库只提供键盘定义、辅助脚本与文档**，不包含 QMK/vial-qmk 源码、`qmk` CLI、ARM 工具链和 dfu-util，需自行安装：

| 依赖 | 说明 |
|---|---|
| [vial-qmk](https://github.com/vial-kb/vial-qmk)（vial 分支） | QMK/Vial 源码树；`build.sh` 默认找 `~/Scripts/git/vial-qmk`（可改） |
| [qmk CLI](https://github.com/qmk/qmk_cli) | 在 vial-qmk 的 `.venv` 内，或 `pip install qmk` |
| [xPack ARM GCC](https://github.com/xpack-dev-tools/arm-none-eabi-gcc-xpack/releases) ≥ 13.x | Homebrew 的 `arm-none-eabi-gcc` 缺 newlib，编译会失败 |
| [dfu-util](https://dfu-util.sourceforge.net/) | 刷机（`brew install dfu-util`） |
| Python 3 + [hid](https://pypi.org/project/hid/) | 仅 `tools/*.py` 需要（`pip install hid`） |

### 构建

```bash
./build.sh
# 产物：build_output/graystudio_apollo80_r2_vial.bin（约 41KB / 128KB flash）
```

### 刷机

```bash
./dfu_commands.sh list      # 等待 DFU 设备出现
./dfu_commands.sh backup    # 全片 128KB 备份
./dfu_commands.sh flash     # 刷入 build_output/graystudio_apollo80_r2_vial.bin
```

进入 DFU：拔线 → 按住 **ESC** → 插线。ESC 不可用（矩阵故障）时，插线同时将 **BOOT0** 短接 3.3V。macOS 下请直插机身 USB 口，经扩展坞/Hub 可能报 `LIBUSB_ERROR_PIPE`。

### 工具

```bash
/opt/homebrew/bin/python tools/led_index_test.py <0-86>   # 单颗点亮（白）
/opt/homebrew/bin/python tools/led_index_test.py scan     # 逐颗扫描
/opt/homebrew/bin/python tools/led_index_test.py restore  # 恢复 cycle_left_right

/opt/homebrew/bin/python tools/led_spot_test.py           # 滑动光斑演示
/opt/homebrew/bin/python tools/led_spot_test.py --skip-bottom --width 4
```

两者均走 VialRGB raw HID 协议（usage page `0xFF60`、usage `0x61`、32 字节报文）：

- get info `[0x08,0x40]`、get mode `[0x08,0x41]`、灯数 `[0x08,0x43]`
- set mode `[0x07,0x41, id_lo,id_hi, speed, h,s,v]`（DIRECT = 1）
- 逐颗 fastset `[0x07,0x42, idx_lo,idx_hi, n, (h,s,v)*n]`（每包最多 9 颗）

### 踩坑记录

1. **矩阵方向必须是 COL2ROW。** 配成 ROW2COL 会导致全部按键失效，而 USB/灯效仍正常。
2. **Vial 解锁死锁：** 发出 `unlock_start (0xFE 0x06)` 后未完成 ESC+`` ` `` 组合，固件只放行 6 个白名单命令（`vial_lock` 也不在白名单且不清状态）——只能断电恢复。不要随手探测。
3. 键位在 EEPROM：刷机不清除。改键实验后用 VIA `0x06` 重置。
4. 方向性灯效用 `g_led_config` 坐标，流/随机类用 LED 索引——接缝在两类效果中的表现不同。
5. RAM 才是紧张资源（约 13.3KB / 16KB，含栈）：裁剪动画省 flash 不省 RAM。
6. VialRGB 无法定位自定义效果——自定义灯效在 GUI 中不可见/不可选（上游协议枚举固定）。
