#!/opt/homebrew/bin/python
"""Space80 R2 单颗灯珠测试工具

用法:
    /opt/homebrew/bin/python led_index_test.py <index>     # 点亮指定灯珠（白光），其余全黑
    /opt/homebrew/bin/python led_index_test.py restore     # 恢复正常效果（cycle_left_right）

index 范围 0-86；超出范围会报错。使用 VialRGB direct 模式逐颗控制。
"""
import sys, time

try:
    import hid
except ImportError:
    print("错误: 需要 hid 模块。请使用 /opt/homebrew/bin/python 运行")
    sys.exit(2)

VID, PID = 0x4753, 0x3080
LED_COUNT = 87
RAW_USAGE_PAGE, RAW_USAGE = 0xFF60, 0x61


def open_space80():
    for d in hid.enumerate(VID, PID):
        if d.get("usage_page") == RAW_USAGE_PAGE and d.get("usage") == RAW_USAGE:
            for _ in range(30):
                try:
                    h = hid.device()
                    h.open_path(d["path"])
                    h.set_nonblocking(0)
                    return h
                except OSError:
                    time.sleep(0.3)
    raise SystemExit("错误: 未找到 Space80 R2（0x4753:0x3080）的 raw HID 接口")


def xfer(h, payload, timeout=400):
    pkt = bytes([0]) + bytes(payload) + bytes(32 - len(payload))
    h.write(pkt[:33])
    time.sleep(0.02)
    r = h.read(32, timeout)
    return list(r) if r else None


def fastset(h, first, hsv_list):
    args = [first & 0xFF, (first >> 8) & 0xFF, len(hsv_list)]
    for (hh, ss, vv) in hsv_list:
        args += [hh, ss, vv]
    xfer(h, [0x07, 0x42] + args)


def set_direct_mode(h):
    xfer(h, [0x07, 0x41, 0x01, 0x00, 0x00, 0x00, 0x00, 0xFF])


def set_effect(h, vialrgb_id, speed=128, hue=0, sat=255, val=200):
    xfer(h, [0x07, 0x41, vialrgb_id & 0xFF, (vialrgb_id >> 8) & 0xFF, speed, hue, sat, val])


def clear_all(h):
    i = 0
    while i < LED_COUNT:
        n = min(9, LED_COUNT - i)
        fastset(h, i, [(0, 0, 0)] * n)
        i += n


def main():
    if len(sys.argv) != 2:
        print("用法: /opt/homebrew/bin/python led_index_test.py <index 0-%d>" % (LED_COUNT - 1))
        print("      /opt/homebrew/bin/python led_index_test.py scan     # 逐颗循环扫描（0→86 循环，1 秒/颗）")
        print("      /opt/homebrew/bin/python led_index_test.py restore")
        sys.exit(2)

    arg = sys.argv[1]
    h = open_space80()

    if arg == "restore":
        # VIALRGB_EFFECT_CYCLE_LEFT_RIGHT = 14
        set_effect(h, 14, speed=128, hue=0, sat=255, val=200)
        print("已恢复正常效果 (cycle_left_right)")
        h.close()
        return

    if arg == "scan":
        set_direct_mode(h)
        time.sleep(0.1)
        clear_all(h)
        print("逐颗循环扫描中（1 秒/颗，白光亮 0.85s 灭 0.15s，Ctrl+C 停止）...")
        try:
            while True:
                for idx in range(LED_COUNT):
                    print("LED %d" % idx, flush=True)
                    fastset(h, idx, [(0, 0, 255)])
                    time.sleep(0.85)
                    fastset(h, idx, [(0, 0, 0)])
                    time.sleep(0.15)
        except KeyboardInterrupt:
            print("\n已停止。灯光保持在最后状态；可运行 restore 恢复动画。")
        h.close()
        return

    try:
        idx = int(arg)
    except ValueError:
        print("错误: index 需要是整数（0-%d）或 restore" % (LED_COUNT - 1))
        h.close()
        sys.exit(2)

    if not (0 <= idx < LED_COUNT):
        print("错误: index 超出范围，有效范围 0-%d" % (LED_COUNT - 1))
        h.close()
        sys.exit(2)

    set_direct_mode(h)
    time.sleep(0.1)
    clear_all(h)
    fastset(h, idx, [(0, 0, 255)])
    print("LED %d 已点亮（白光），其余全黑。测试下一颗请再次运行。" % idx)
    h.close()


if __name__ == "__main__":
    main()
