"""Render lecture slides (PDF) to images and pull out each page's text.

    uv run --with pymupdf python slides.py materials/L01.pdf --id L01 --out site/slides
    uv run --with pymupdf python slides.py materials/L01.pdf --id L01 --out site/slides --pages 3,7-9 --dpi 150
    uv run --with pymupdf python slides.py materials/L01.pdf --id L01 --out site/slides --crop 7:0.05,0.2,0.95,0.8

Writes
    <out>/<id>-p007.png         one image per page (or per --crop, named <id>-p007-crop.png)
    <out>/<id>-slides.json      [{"page": 7, "text": "...", "image": "<id>-p007.png"}, ...]

--crop PAGE:x0,y0,x1,y1 cuts a region given as fractions of the page width and height,
for when only one figure on a busy slide matters.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_pages(spec: str | None, n: int) -> list[int]:
    if not spec:
        return list(range(1, n + 1))
    pages: list[int] = []
    for part in spec.split(","):
        a, _, b = part.partition("-")
        pages += range(int(a), int(b or a) + 1)
    return [p for p in pages if 1 <= p <= n]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--id", required=True, help="short lecture id used in file names, e.g. L01")
    ap.add_argument("--out", required=True)
    ap.add_argument("--pages", help="e.g. 1,3,5-9 (default: all)")
    ap.add_argument("--dpi", type=int, default=110, help="110 keeps a 16:9 slide near 1460px wide")
    ap.add_argument("--crop", action="append", default=[], help="PAGE:x0,y0,x1,y1 as fractions")
    args = ap.parse_args()

    try:
        import pymupdf as fitz
    except ImportError:  # PyMuPDF older than 1.24
        import fitz

    doc = fitz.open(args.pdf)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    zoom = fitz.Matrix(args.dpi / 72, args.dpi / 72)

    index = []
    for p in parse_pages(args.pages, doc.page_count):
        page = doc[p - 1]
        name = f"{args.id}-p{p:03d}.png"
        page.get_pixmap(matrix=zoom).save(out / name)
        index.append({"page": p, "text": " ".join(page.get_text().split()), "image": name})

    for spec in args.crop:
        p_str, _, box = spec.partition(":")
        p = int(p_str)
        x0, y0, x1, y1 = (float(v) for v in box.split(","))
        page = doc[p - 1]
        r = page.rect
        clip = fitz.Rect(r.x0 + x0 * r.width, r.y0 + y0 * r.height, r.x0 + x1 * r.width, r.y0 + y1 * r.height)
        name = f"{args.id}-p{p:03d}-crop.png"
        page.get_pixmap(matrix=zoom, clip=clip).save(out / name)
        print("cropped", name)

    (out / f"{args.id}-slides.json").write_text(json.dumps(index, ensure_ascii=False, indent=1))
    total = sum((out / i["image"]).stat().st_size for i in index)
    print(f"{len(index)} pages → {out} ({total / 1e6:.1f} MB), text in {args.id}-slides.json")


if __name__ == "__main__":
    main()
