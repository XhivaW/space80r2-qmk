# Space80 R2 (apollo80_r2) 自定义固件

[English](README.md)

Graystudio **Space80 R2 "Apollo's Cyber Armor"** 的 QMK / Vial 固件：支持逐颗灯珠控制（VialRGB），默认键位为标准 Windows 布局。

> 仅在 macOS 下使用过，未验证其他平台。

## 概述

基于开源 [vial-qmk](https://github.com/vial-kb/vial-qmk) 构建。

- 灯效：RGB Matrix 引擎，精选 9 个动画
- 逐颗灯珠控制：**VialRGB**（协议 + GUI Direct Control）
- 默认键位：**标准 Windows（104/TKL 顺序）**
- CapsLock 指示：铭牌排白光（LED 0-5）

已实机验证：全部按键、Vial 识别、VialRGB（87 颗）、CapsLock 铭牌指示。

## 灯效

`breathing`、`hue_breathing`、`hue_pendulum`、`hue_wave`、`gradient_up_down`、`gradient_left_right`、`cycle_all`、`cycle_left_right`、`cycle_up_down`，外加 `Disable`、`Solid Color`、`Direct Control`。

## 默认键位（标准 Windows）

层 0 为标准 Windows 104/TKL 顺序——`Ctrl Win Alt ... Alt Win Fn Ctrl`，右上三键 `PrtSc ScrLk Pause`，右侧编辑区 `Ins Home PgUp / Del End PgDn`，右下方向键。
层 1（Fn，位于右 Alt 右侧）：灯效控制（`UG_*` / `RM_*`）、NKRO 切换、**QK_BOOT**、媒体键（右上 `VOLD/MUTE/VOLU`）、小键盘。

## 目录结构

```
space80r2-qmk/
├── keyboards/graystudio/apollo80_r2/    # 键盘定义（拷入 vial-qmk 树即可）
│   ├── keyboard.json                    # MCU / 矩阵 / 灯驱动 / 动画开关
│   ├── apollo80_r2.c                    # g_led_config（灯珠映射）+ CapsLock 钩子
│   └── keymaps/vial/                    # keymap.c, config.h, rules.mk, vial.json
├── tools/
│   ├── led_index_test.py                # 单颗点亮 / 扫描 / 恢复
│   └── led_spot_test.py                 # 滑动光斑演示（VialRGB 推流）
├── docs/led_map.txt                     # 灯珠编号记录
├── build.sh                             # 一键构建
├── dfu_commands.sh                      # dfu-util 备份 / 刷入
├── README.md                            # 英文说明
└── README.zh-CN.md                      # 本文件
```

## 依赖（本仓库不包含）

**本仓库只提供键盘定义、辅助脚本与文档**，不包含 QMK/vial-qmk 源码、`qmk` CLI、ARM 工具链和 dfu-util，需自行安装：

| 依赖 | 说明 |
|---|---|
| [vial-qmk](https://github.com/vial-kb/vial-qmk)（vial 分支） | QMK/Vial 源码树；`build.sh` 默认找 `~/Scripts/git/vial-qmk`（可改） |
| [qmk CLI](https://github.com/qmk/qmk_cli) | 在 vial-qmk 的 `.venv` 内，或 `pip install qmk` |
| [xPack ARM GCC](https://github.com/xpack-dev-tools/arm-none-eabi-gcc-xpack/releases) ≥ 13.x | Homebrew 的 `arm-none-eabi-gcc` 缺 newlib，编译会失败 |
| [dfu-util](https://dfu-util.sourceforge.net/) | 刷机（`brew install dfu-util`） |
| Python 3 + [hid](https://pypi.org/project/hid/) | 仅 `tools/*.py` 需要（`pip install hid`） |

## 构建

```bash
./build.sh
# 产物：build_output/graystudio_apollo80_r2_vial.bin（约 41KB / 128KB flash）
```
