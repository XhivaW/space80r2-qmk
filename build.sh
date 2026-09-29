#!/bin/bash
# Space80 R2 (apollo80_r2) Vial + VialRGB firmware build script
set -e
export PATH="$HOME/opt/xpack-arm-none-eabi-gcc-13.2.1-1.1/bin:$PATH"
QMK_DIR="$HOME/Scripts/git/vial-qmk"
PROJ_DIR="$(cd "$(dirname "$0")" && pwd)"
cp -r "$PROJ_DIR/keyboards/graystudio/apollo80_r2" "$QMK_DIR/keyboards/graystudio/"
cd "$QMK_DIR"
export QMK_HOME="$QMK_DIR"
"$QMK_DIR/.venv/bin/qmk" compile -kb graystudio/apollo80_r2 -km vial
mkdir -p "$PROJ_DIR/build_output"
cp "$QMK_DIR/.build/graystudio_apollo80_r2_vial.bin" "$PROJ_DIR/build_output/"
cp "$QMK_DIR/.build/graystudio_apollo80_r2_vial.hex" "$PROJ_DIR/build_output/"
echo "Build OK: $PROJ_DIR/build_output/graystudio_apollo80_r2_vial.bin"
