#!/bin/bash
# Space80 R2 DFU 操作脚本（自动等待版）
#
# 用法：先在键盘正常模式下执行命令，脚本会等待 DFU 设备出现；
# 提示"等待 DFU 设备"时再做物理动作：拔线 -> 按住 ESC 不放 -> 插线 -> 松手。
# 全程无需在 DFU 期间使用键盘。
#
#   ./dfu_commands.sh list      # 等待并列出 DFU 设备信息
#   ./dfu_commands.sh backup    # 等待 DFU -> 全量备份 flash（128KB）
#   ./dfu_commands.sh flash     # 等待 DFU -> 刷入新固件

PROJ="$(cd "$(dirname "$0")" && pwd)"

wait_dfu() {
    if dfu-util -l 2>/dev/null | grep -q "0483:df11"; then
        echo "== 已在 DFU 模式 =="
        return 0
    fi
    echo "== 等待 DFU 设备 =="
    echo "请操作：拔掉数据线 -> 按住 ESC 不放 -> 插上数据线 -> 等 1 秒松手"
    for _ in $(seq 1 600); do
        if dfu-util -l 2>/dev/null | grep -q "0483:df11"; then
            echo "== 检测到 DFU 设备 =="
            return 0
        fi
        sleep 1
    done
    echo "!! 超时（600 秒）未检测到 DFU 设备，退出"
    exit 1
}

case "$1" in
  list)
    wait_dfu
    dfu-util -l
    ;;
  backup)
    wait_dfu
    dfu-util -d 0483:df11 -a 0 -s 0x08000000:131072 -U "$PROJ/build_output/full_flash_backup.bin" \
      && echo "== 备份完成: $PROJ/build_output/full_flash_backup.bin ==" \
      && echo "== 现在是 DFU 模式，可拔线结束 =="
    ;;
  flash)
    wait_dfu
    dfu-util -d 0483:df11 -a 0 -s 0x08000000:leave -D "$PROJ/build_output/graystudio_apollo80_r2_vial.bin" \
      && echo "== 刷入完成，键盘将自动复位 ==" \
      && echo "== 拔线 -> 重新插线（正常启动）=="
    ;;
  *)
    echo "用法: $0 {list|backup|flash}"
    echo "  list     等待 DFU 并列出设备信息"
    echo "  backup   等待 DFU -> 全量备份当前 flash -> build_output/full_flash_backup.bin"
    echo "  flash    等待 DFU -> 刷入新固件 build_output/graystudio_apollo80_r2_vial.bin"
    ;;
esac
