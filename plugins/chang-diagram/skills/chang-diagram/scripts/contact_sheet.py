"""Tile every PNG in a folder into one preview sheet with file-name captions.

Usage:
    python contact_sheet.py RUN/ALL --out RUN/ALL/_contact_sheet.png [--cols 2] [--width 800]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

FONTS = ["C:/Windows/Fonts/malgunbd.ttf", "/System/Library/Fonts/AppleSDGothicNeo.ttc",
         "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--cols", type=int, default=2)
    parser.add_argument("--width", type=int, default=800)
    args = parser.parse_args()

    from PIL import Image, ImageDraw, ImageFont

    files = sorted(f for f in args.folder.glob("*.png") if f.resolve() != args.out.resolve() and not f.name.startswith("_"))
    if not files:
        print(f"no PNG files in {args.folder}")
        return 1
    tiles = []
    for f in files:
        im = Image.open(f).convert("RGB")
        tiles.append((f.stem, im.resize((args.width, int(im.height * args.width / im.width)), Image.LANCZOS)))

    pad, cap = 24, 36
    rows = [tiles[i:i + args.cols] for i in range(0, len(tiles), args.cols)]
    height = sum(max(t[1].height for t in r) + cap + pad for r in rows) + pad
    sheet = Image.new("RGB", (args.cols * args.width + (args.cols + 1) * pad, height), "#F5F5F7")
    draw = ImageDraw.Draw(sheet)
    font = next((ImageFont.truetype(p, 22) for p in FONTS if Path(p).exists()), ImageFont.load_default())
    y = pad
    for row in rows:
        x = pad
        for name, im in row:
            draw.text((x, y), name, fill="#1B2A4A", font=font)
            sheet.paste(im, (x, y + cap))
            x += args.width + pad
        y += max(t[1].height for t in row) + cap + pad
    sheet.save(args.out)
    print(f"{args.out}: {len(files)} diagrams, {sheet.size[0]}x{sheet.size[1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
