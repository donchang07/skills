"""Write report.md and a self-contained report.html for a chang-diagram run.

Usage:
    python make_report.py RUN --title "AI Index Report 2026 장별 다이어그램" [--embed png|svg] [--no-review]

RUN is either one diagram folder (RUN/final/*.png) or a batch folder whose subfolders each
have final/. For each diagram the report shows the source title, the image (its headline and
takeaway are drawn inside it, so they are not repeated around it), the diagram's text in reading
order ending with the takeaway, and source pages; an appendix lists judge scores and remaining notes from
05_manifest.json unless --no-review is given.
report.md links the PNG files by relative path; report.html embeds the images so the one file
can be shared.
"""
from __future__ import annotations

import argparse
import base64
import html
import json
import re
import sys
from datetime import date
from pathlib import Path

CSS = """
:root { --navy:#1B2A4A; --body:#2C3E5A; --muted:#7F8FA9; --brand:#3A86FF; --bg:#FFFFFF; --soft:#F5F5F7;
        --focal:#B45309; --focal-bg:#FFF4E8; }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--body);
       font-family:Pretendard,'Malgun Gothic','Apple SD Gothic Neo',sans-serif; line-height:1.6; }
main { max-width:1100px; margin:0 auto; padding:48px 16px 80px; }
h1 { color:var(--navy); font-size:32px; margin:0 0 8px; }
.meta { color:var(--muted); margin:0 0 24px; }
nav ol { columns:2; padding-left:20px; margin:0 0 40px; }
nav a { color:var(--navy); text-decoration:none; }
nav a:hover { text-decoration:underline; }
section { border-top:1px solid #E3E7EE; padding:40px 0; }
h2 { color:var(--navy); font-size:26px; margin:4px 0 4px; }
h2.chapter { color:var(--brand); font-size:20px; margin:0 0 12px; }
figure { margin:0; }
figure img { width:100%; height:auto; border:1px solid #E3E7EE; border-radius:8px; background:#fff; }
.source { color:var(--muted); font-size:14px; margin:8px 0 0; }
details { margin:12px 0 0; }
summary { cursor:pointer; color:var(--navy); font-weight:700; }
details ul { margin:8px 0 0; padding-left:20px; }
details li { margin:2px 0; }
.table-wrap { overflow-x:auto; }
table { border-collapse:collapse; width:100%; min-width:560px; font-size:14px; }
th, td { border-bottom:1px solid #E3E7EE; padding:8px; text-align:left; vertical-align:top; }
th { color:var(--navy); background:var(--soft); }
@media (max-width:640px) { nav ol { columns:1; } h1 { font-size:26px; } h2 { font-size:21px; } }
@media print { section { break-inside:avoid; } nav { display:none; } }
"""


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def source_info(folder: Path) -> tuple[str, str]:
    src = folder / "00_source.md"
    if not src.exists():
        return folder.name, ""
    lines = src.read_text(encoding="utf-8").splitlines()
    head = re.sub(r"^#\s*원문:\s*", "", lines[0]).strip() if lines else folder.name
    doc, _, title = head.rpartition(" — ")
    cite = next((l for l in lines[:6] if l.startswith("출처:")), "")
    pages = re.search(r"(PDF 페이지 [\d,\s\-]+)", cite)
    origin = " · ".join(x for x in (doc, pages.group(1).strip() if pages else "") if x)
    return title or head, origin


def points(spec: dict) -> list[str]:
    """Node and annotation text in reading order, as a plain-text version of the diagram."""
    nodes = {n["id"]: n for n in spec.get("nodes", [])}
    order = [i for i in spec.get("reading_path", []) if i in nodes]
    order += [i for i in nodes if i not in order]
    flat = lambda s: " · ".join(" ".join(line.split()) for line in str(s or "").replace("\\n", "\n").splitlines() if line.strip())
    out = [" — ".join(x for x in (flat(nodes[i].get("label")), flat(nodes[i].get("sub"))) if x) for i in order]
    out += [f"주석: {flat(a.get('text'))}" for a in spec.get("annotations", [])
            if a.get("text") and not str(a["text"]).startswith("출처")]
    if spec.get("takeaway"):
        out.append(f"결론: {flat(spec['takeaway'])}")
    return [p for p in out if p]


def collect(run: Path) -> list[dict]:
    folders = [run] if (run / "final").is_dir() else sorted(p for p in run.iterdir() if (p / "final").is_dir())
    items = []
    for folder in folders:
        pngs = sorted((folder / "final").glob("*.png"))
        if not pngs:
            continue
        spec = load_json(folder / "01_spec.json")
        manifest = load_json(folder / "05_manifest.json")
        scored = [v for v in manifest.get("versions", []) if "story" in v]
        title, origin = source_info(folder)
        items.append({
            "id": folder.name, "title": title, "origin": origin,
            "headline": spec.get("headline", ""),
            "points": points(spec),
            "png": pngs[0], "svg": pngs[0].with_suffix(".svg"),
            "score": {**(scored[-1] if scored else {}), "v": (manifest.get("versions") or [{}])[-1].get("v", "-")},
            "remaining": manifest.get("remaining", []),
            "not_run": manifest.get("not_run", []),
        })
    return items


def write_md(run: Path, items: list[dict], title: str, review: bool) -> Path:
    out = [f"# {title}", "", f"{date.today():%Y-%m-%d} · 그림 {len(items)}장", ""]
    out += [f"{i}. [{it['title']}: {it['headline']}](#{it['id']})" for i, it in enumerate(items, 1)] + [""]
    for it in items:
        rel = it["png"].relative_to(run).as_posix()
        out += [f'<a id="{it["id"]}"></a>', "", f"## {it['title']}", ""]
        out += [f"![{it['headline']}]({rel})", ""]
        if it["points"]:
            out += ["그림 내용:", ""] + [f"- {p}" for p in it["points"]] + [""]
        if it["origin"]:
            out += [f"출처: {it['origin']}", ""]
    if review:
        out += ["## 부록: 심사 결과", "", "| 그림 | 최종 버전 | story | visual | 남은 지적 |", "| --- | --- | --- | --- | --- |"]
        for it in items:
            s = it["score"]
            notes = "<br>".join(it["remaining"] + [f"not_run: {x}" for x in it["not_run"]]) or "-"
            out.append(f"| {it['title']} | v{s.get('v', '-')} | {s.get('story', '-')} | {s.get('visual', '-')} | {notes} |")
        out.append("")
    path = run / "report.md"
    path.write_text("\n".join(out), encoding="utf-8")
    return path


def image_uri(it: dict, embed: str) -> str:
    if embed == "svg" and it["svg"].exists():
        return "data:image/svg+xml;base64," + base64.b64encode(it["svg"].read_bytes()).decode()
    return "data:image/png;base64," + base64.b64encode(it["png"].read_bytes()).decode()


def write_html(run: Path, items: list[dict], title: str, review: bool, embed: str) -> Path:
    e = html.escape
    parts = [f"<!doctype html><html lang='ko'><head><meta charset='utf-8'>",
             "<meta name='viewport' content='width=device-width, initial-scale=1'>",
             f"<title>{e(title)}</title><style>{CSS}</style></head><body><main>",
             f"<h1>{e(title)}</h1><p class='meta'>{date.today():%Y-%m-%d} · 그림 {len(items)}장</p>",
             "<nav><ol>" + "".join(f"<li><a href='#{e(it['id'])}'>{e(it['title'])}: {e(it['headline'])}</a></li>" for it in items) + "</ol></nav>"]
    for it in items:
        parts.append(f"<section id='{e(it['id'])}'><h2 class='chapter'>{e(it['title'])}</h2>")
        parts.append(f"<figure><img src='{image_uri(it, embed)}' alt='{e(it['headline'])}'></figure>")
        if it["points"]:
            parts.append("<details><summary>그림 내용을 글로 보기</summary><ul>"
                         + "".join(f"<li>{e(p)}</li>" for p in it["points"]) + "</ul></details>")
        if it["origin"]:
            parts.append(f"<p class='source'>출처: {e(it['origin'])}</p>")
        parts.append("</section>")
    if review:
        rows = "".join(
            f"<tr><td>{e(it['title'])}</td><td>v{e(str(it['score'].get('v', '-')))}</td>"
            f"<td>{e(str(it['score'].get('story', '-')))}</td><td>{e(str(it['score'].get('visual', '-')))}</td>"
            f"<td>{'<br>'.join(e(x) for x in it['remaining'] + [f'not_run: {y}' for y in it['not_run']]) or '-'}</td></tr>"
            for it in items)
        parts.append("<section><h2>부록: 심사 결과</h2><div class='table-wrap'><table><thead><tr><th>그림</th><th>최종 버전</th>"
                     f"<th>story</th><th>visual</th><th>남은 지적</th></tr></thead><tbody>{rows}</tbody></table></div></section>")
    parts.append("</main></body></html>")
    path = run / "report.html"
    path.write_text("".join(parts), encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run", type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--embed", choices=["png", "svg"], default="png",
                        help="png keeps the reviewed rendering on any PC; svg is smaller but needs Pretendard")
    parser.add_argument("--no-review", action="store_true", help="omit the judge-score appendix")
    args = parser.parse_args()

    items = collect(args.run)
    if not items:
        print(f"no final/*.png under {args.run}")
        return 1
    md = write_md(args.run, items, args.title, not args.no_review)
    page = write_html(args.run, items, args.title, not args.no_review, args.embed)
    print(f"{md} and {page}: {len(items)} diagrams ({page.stat().st_size // 1024} KB html)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
