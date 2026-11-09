#!/usr/bin/env python3
"""给公众号封面图加品牌水印:底部半透明条 + 公众号名 + 搜一搜引导。

依赖: Pillow (pip install pillow), macOS 中文字体。

用法:
  python3 watermark.py <src> <dst> \
      [--name "作业不慌记"] \
      [--sub "微信搜一搜 · 看更多陪学日常"]

批量(只处理全尺寸封面,跳过 thumbs):
  for f in covers/*.png; do
    [ -f "$f" ] || continue
    case "$f" in covers/thumbs/*) continue;; esac
    python3 watermark.py "$f" "$f"
  done
"""
import argparse
from PIL import Image, ImageDraw, ImageFont

FONT = "/System/Library/Fonts/STHeiti Medium.ttc"


def add_watermark(src, dst, name, sub):
    img = Image.open(src).convert("RGBA")
    w, h = img.size
    draw = ImageDraw.Draw(img, "RGBA")

    bar_h = max(40, int(h * 0.16))
    draw.rectangle([0, h - bar_h, w, h], fill=(0, 0, 0, 120))

    name_font = ImageFont.truetype(FONT, int(bar_h * 0.52))
    sub_font = ImageFont.truetype(FONT, int(bar_h * 0.34))
    pad = int(bar_h * 0.18)

    draw.text((pad, h - bar_h + pad), name, font=name_font, fill=(255, 255, 255, 235))
    sub_w = draw.textlength(sub, font=sub_font)
    draw.text(
        (w - sub_w - pad, h - bar_h + int(bar_h * 0.30)),
        sub,
        font=sub_font,
        fill=(255, 255, 255, 190),
    )

    img.convert("RGB").save(dst, "PNG")
    print(f"watermarked {src} -> {dst} ({w}x{h})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--name", default="作业不慌记")
    ap.add_argument("--sub", default="微信搜一搜 · 看更多陪学日常")
    args = ap.parse_args()
    add_watermark(args.src, args.dst, args.name, args.sub)


if __name__ == "__main__":
    main()
