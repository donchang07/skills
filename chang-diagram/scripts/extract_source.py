"""Copy PDF pages verbatim into a numbered 00_source.md for chang-diagram.

Usage:
    python extract_source.py report.pdf --pages 15-16 --out RUN/00_source.md --title "1장 Research and Development"
    python extract_source.py report.pdf --pages 4,10-12 --out RUN/00_source.md --title "개요"

Each text block becomes one paragraph "[T#] (p.N) ..." so distiller and judges can cite it.
Blocks shorter than --min-chars (page numbers, chart ticks) and blocks repeated on two or more
extracted pages (running headers) are dropped. Use --skip for a header on a single page.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def parse_pages(spec: str) -> list[int]:
    pages: list[int] = []
    for part in spec.split(","):
        start, _, end = part.strip().partition("-")
        pages.extend(range(int(start), int(end or start) + 1))
    return pages


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--pages", required=True, help="1-based PDF page numbers, e.g. 15-16 or 4,10-12")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--min-chars", type=int, default=40)
    parser.add_argument("--skip", action="append", default=[], help="regex for blocks to drop (repeatable)")
    args = parser.parse_args()

    try:
        import fitz
    except ImportError:
        print("PyMuPDF (fitz) is required: pip install pymupdf")
        return 2

    doc = fitz.open(args.pdf)
    pages = parse_pages(args.pages)
    skip = [re.compile(p) for p in args.skip]
    raw: list[tuple[int, str]] = []
    for page in pages:
        for block in doc[page - 1].get_text("blocks"):
            text = " ".join(block[4].split())
            if len(text) < args.min_chars or re.fullmatch(r"[\d\s%.,]+", text) or any(p.search(text) for p in skip):
                continue
            raw.append((page, text))
    shape = lambda t: re.sub(r"\d+", "#", t)
    seen_on = {}
    for page, text in raw:
        seen_on.setdefault(shape(text), set()).add(page)
    running = {k for k, v in seen_on.items() if len(v) > 1}
    paras = [(page, text) for page, text in raw if shape(text) not in running]

    lines = [f"# 원문: {args.title}", "",
             f"출처: {args.pdf.name}, PDF 페이지 {args.pages} (원문을 그대로 옮김, 단락마다 번호)", ""]
    for i, (page, text) in enumerate(paras, 1):
        lines += [f"[T{i}] (p.{page}) {text}", ""]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines), encoding="utf-8")
    print(f"{args.out}: {len(paras)} paragraphs from pages {args.pages}")
    return 0 if paras else 1


if __name__ == "__main__":
    sys.exit(main())
