#!/opt/homebrew/bin/python
"""Space80 R2 光斑滑动测试（VialRGB direct 逐颗推流）

效果：
  - 铭牌 0-5：固定颜色呼吸
  - 环 6-86：宽度 N 颗的光斑沿环逆时针（索引递增方向）滑动

用法:
    /opt/homebrew/bin/python led_spot_test.py
    /opt/homebrew/bin/python led_spot_test.py --hue 43 --width 4 --ring-seconds 1.5
    /opt/homebrew/bin/python led_spot_test.py --skip-bottom    # 光斑跳过 36-53
    Ctrl+C 停止；之后可用 led_index_test.py restore 恢复正常效果。

色相参考（0-255）：0 红 / 43 黄 / 85 绿 / 128 青 / 170 蓝 / 213 品红。
"""
import argparse
import math
import sys
import time

try:
    import hid
except ImportError:
    print("错误: 需要 hid 模块。请使用 /opt/homebrew/bin/python 运行", file=sys.stderr)
    sys.exit(2)

VID, PID = 0x4753, 0x3080
LED_COUNT = 87
BADGE_N = 6  # LEDs 0-5
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


def xfer(h, payload, timeout=5):
    pkt = bytes([0]) + bytes(payload) + bytes(32 - len(payload))
    h.write(pkt[:33])
    return h.read(32, timeout)


def set_direct(h, speed=0):
    # VIALRGB_EFFECT_DIRECT = 1
    xfer(h, [0x07, 0x41, 0x01, 0x00, speed, 0, 0, 0xFF])


def fastset(h, first, hsv_list):
    args = [first & 0xFF, (first >> 8) & 0xFF, len(hsv_list)]
    for (hh, ss, vv) in hsv_list:
        args += [hh, ss, vv]
    xfer(h, [0x07, 0x42] + args)


def send_colors(h, colors):
    i = 0
    while i < LED_COUNT:
        n = min(9, LED_COUNT - i)
        fastset(h, i, colors[i:i + n])
        i += n


def main():
    ap = argparse.ArgumentParser(description="Space80 R2 光斑滑动测试")
    ap.add_argument("--hue", type=int, default=43, help="色相 0-255（默认 43 黄）")
    ap.add_argument("--sat", type=int, default=255, help="饱和度 0-255")
    ap.add_argument("--width", type=int, default=4, help="光斑宽度（颗，默认 4）")
    ap.add_argument("--ring-seconds", type=float, default=1.5, help="光斑绕环一圈的秒数")
    ap.add_argument("--spot-val", type=int, default=200, help="光斑亮度 0-255")
    ap.add_argument("--skip-bottom", action="store_true",
                    help="光斑只在 6-35 与 54-86 上滑，跳过 36-53")
    ap.add_argument("--badge-period", type=float, default=2.0, help="铭牌呼吸周期（秒）")
    ap.add_argument("--badge-min", type=int, default=20, help="铭牌最暗亮度")
    ap.add_argument("--badge-max", type=int, default=200, help="铭牌最亮亮度")
    ap.add_argument("--fps", type=float, default=60, help="目标帧率")
    ap.add_argument("--seconds", type=float, default=0, help="运行秒数，0=不限")
    args = ap.parse_args()

    order = list(range(6, 87))
    if args.skip_bottom:
        order = list(range(6, 36)) + list(range(54, 87))
    n = len(order)

    h = open_space80()
    set_direct(h)
    time.sleep(0.05)

    period = 1.0 / args.fps
    t0 = time.time()
    frames = 0
    try:
        while True:
            frame_start = time.time()
            t = frame_start - t0
            colors = [(0, 0, 0)] * LED_COUNT

            ph = (math.sin(2 * math.pi * t / args.badge_period - math.pi / 2) + 1) / 2
            bv = int(round(args.badge_min + (args.badge_max - args.badge_min) * ph))
            for i in range(BADGE_N):
                colors[i] = (args.hue, args.sat, bv)

            head = (t / args.ring_seconds * n) % n
            for k in range(n):
                if (k - head) % n < args.width:
                    colors[order[k]] = (args.hue, args.sat, args.spot_val)

            send_colors(h, colors)
            frames += 1

            if args.seconds and t >= args.seconds:
                break
            dt = time.time() - frame_start
            if dt < period:
                time.sleep(period - dt)
    except KeyboardInterrupt:
        print()
    finally:
        elapsed = time.time() - t0
        if elapsed > 0:
            print("frames=%d  %.1fs  avg=%.1f fps" % (frames, elapsed, frames / elapsed))
        h.close()
        print("已停止。可用 led_index_test.py restore 恢复正常效果。")


if __name__ == "__main__":
    main()
