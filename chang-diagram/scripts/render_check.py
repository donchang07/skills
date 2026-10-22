"""Render a chang-diagram SVG to PNG and run geometric checks.

Usage:
    python render_check.py diagram.svg --png diagram.png --report check.json [--spec 01_spec.json] [--density normal|dense]

Exit code 0 when no errors, 1 when errors remain, 2 when rendering is unavailable.
"""
from __future__ import annotations

import argparse
import itertools
import json
import re
import sys
from pathlib import Path

PALETTE = {
    "#1b2a4a", "#2c3e5a", "#7f8fa9", "#3a86ff", "#ffffff", "#f5f5f7",
    "#b45309", "#fff4e8", "#0f766e", "#eaf6f3", "#2563eb", "#edf3ff",
    "#355c7d", "#eef2f6", "#7c3aed",
    "#0f1b33", "#172744", "#3a4e73", "#e6ecf5", "#a9b6cc", "#2dd4bf",
    "#f59e0b", "#a78bfa", "#000000",
}
ENDPOINT_TOLERANCE = 12
MIN_FONT_AT_1600 = 14
MAX_LINES = {"normal": 4, "dense": 6}
BREAK_END = re.compile(r"(→|←|↔|\(|약)$")
BREAK_START = re.compile(r"^(%p?|\)|→|(배|건|명|개|억|만|조)(?![가-힣])|billion|million|trillion|GW|TB|미만|이상|이하|초과)")
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿⭐⭕️]")

COLLECT_JS = r"""
() => {
  const svg = document.querySelector('svg');
  const vb = svg.viewBox.baseVal;
  const W = vb && vb.width ? vb.width : svg.width.baseVal.value;
  const H = vb && vb.height ? vb.height : svg.height.baseVal.value;
  const sr = svg.getBoundingClientRect();
  const k = W / sr.width;
  const box = el => { const r = el.getBoundingClientRect();
    return [(r.left - sr.left) * k, (r.top - sr.top) * k, (r.right - sr.left) * k, (r.bottom - sr.top) * k]; };
  const pt = (el, x, y) => { const p = svg.createSVGPoint(); p.x = x; p.y = y;
    const q = p.matrixTransform(el.getScreenCTM()); return [(q.x - sr.left) * k, (q.y - sr.top) * k]; };
  const owner = (el, attr) => { const g = el.closest('[' + attr + ']'); return g ? g.getAttribute(attr) : null; };
  const texts = [...svg.querySelectorAll('text')].filter(t => t.textContent.trim()).map(t => {
    const cs = getComputedStyle(t);
    return { text: t.textContent.trim().slice(0, 40), rect: box(t), size: parseFloat(cs.fontSize),
      family: cs.fontFamily, fill: cs.fill, node: owner(t, 'data-node'), edge: owner(t, 'data-edge'),
      segs: (() => { const leaves = [...t.querySelectorAll('tspan')].filter(s => !s.querySelector('tspan') && s.textContent.trim());
        return (leaves.length ? leaves : [t]).map(s => { const r = box(s); return { left: r[0], top: r[1], bottom: r[3], text: s.textContent }; }); })() };
  });
  const nodes = [...svg.querySelectorAll('[data-node]')].map(g => {
    const b = g.querySelector('[data-box]');
    return { id: g.getAttribute('data-node'), hasBox: !!b, rect: b ? box(b) : box(g),
      fill: b ? getComputedStyle(b).fill : null };
  });
  const sample = el => {
    const tag = el.tagName.toLowerCase();
    if (tag === 'line') { const a = el.x1.baseVal.value, b = el.y1.baseVal.value, c = el.x2.baseVal.value, d = el.y2.baseVal.value;
      const n = Math.max(2, Math.ceil(Math.hypot(c - a, d - b) / 4));
      return [...Array(n + 1).keys()].map(i => pt(el, a + (c - a) * i / n, b + (d - b) * i / n)); }
    if (tag === 'polyline') { const ps = [...el.points].map(p => [p.x, p.y]); const out = [];
      for (let i = 0; i < ps.length - 1; i++) { const [a, b] = ps[i], [c, d] = ps[i + 1];
        const n = Math.max(1, Math.ceil(Math.hypot(c - a, d - b) / 4));
        for (let j = 0; j < n; j++) out.push(pt(el, a + (c - a) * j / n, b + (d - b) * j / n)); }
      const [a, b] = ps[ps.length - 1]; out.push(pt(el, a, b)); return out; }
    const L = el.getTotalLength(); const n = Math.max(2, Math.ceil(L / 4));
    return [...Array(n + 1).keys()].map(i => { const p = el.getPointAtLength(L * i / n); return pt(el, p.x, p.y); });
  };
  const edges = [...svg.querySelectorAll('[data-edge]')].map(g => {
    const line = g.querySelector('path, line, polyline');
    return { id: g.getAttribute('data-edge'), points: line ? sample(line) : [],
      undirected: g.getAttribute('data-undirected') === 'true',
      marker: line ? (line.getAttribute('marker-end') || line.getAttribute('marker-start') || '') : '' };
  });
  const colors = new Set();
  svg.querySelectorAll('*').forEach(el => { for (const a of ['fill', 'stroke']) {
    const v = el.getAttribute(a); if (v) colors.add(v.trim().toLowerCase()); } });
  const outer = [...svg.querySelectorAll('text, [data-box], [data-role="icon"]')].map(el => box(el));
  return { W, H, texts, nodes, edges, colors: [...colors], outer,
    pretendard: (() => { const c = document.createElement('canvas').getContext('2d');
      const w = f => { c.font = '40px ' + f; return c.measureText('가나다 ABC 123').width; };
      return w('Pretendard, monospace') !== w('monospace') || w('Pretendard, serif') !== w('serif'); })(),
    external: svg.querySelectorAll('image[href^="http"], script, foreignObject').length };
}
"""


def parse_rgb(value: str | None) -> tuple[float, float, float] | None:
    if not value:
        return None
    m = re.match(r"rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)", value)
    if not m or (m.group(4) is not None and float(m.group(4)) == 0):
        return None
    return float(m.group(1)), float(m.group(2)), float(m.group(3))


def luminance(rgb: tuple[float, float, float]) -> float:
    def channel(c: float) -> float:
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def overlap(a: list[float], b: list[float], pad: float = 0) -> float:
    w = min(a[2], b[2]) - max(a[0], b[0]) - pad
    h = min(a[3], b[3]) - max(a[1], b[1]) - pad
    return w * h if w > 0 and h > 0 else 0


def inside(p: list[float], r: list[float], shrink: float = 0) -> bool:
    return r[0] + shrink < p[0] < r[2] - shrink and r[1] + shrink < p[1] < r[3] - shrink


def edge_gap(p: list[float], r: list[float]) -> float:
    dx = max(r[0] - p[0], 0, p[0] - r[2])
    dy = max(r[1] - p[1], 0, p[1] - r[3])
    if dx or dy:
        return (dx * dx + dy * dy) ** 0.5
    return min(p[0] - r[0], r[2] - p[0], p[1] - r[1], r[3] - p[1])


def check(data: dict, spec: dict | None, max_lines: int) -> list[dict]:
    issues: list[dict] = []

    def add(severity: str, check_name: str, ids: list[str], detail: str) -> None:
        issues.append({"severity": severity, "check": check_name, "ids": ids, "detail": detail})

    W, H = data["W"], data["H"]
    nodes = {n["id"]: n for n in data["nodes"]}

    for r in data["outer"]:
        if r[0] < -1 or r[1] < -1 or r[2] > W + 1 or r[3] > H + 1:
            add("error", "out_of_canvas", [], f"element at {[round(v) for v in r]} exceeds {W}x{H}")
        elif min(r[0], r[1], W - r[2], H - r[3]) < 24:
            add("warning", "tight_margin", [], f"element at {[round(v) for v in r]} is within 24px of edge")

    for n in data["nodes"]:
        if not n["hasBox"]:
            add("error", "missing_box", [n["id"]], "node has no [data-box] shape")

    min_font = max(12, MIN_FONT_AT_1600 * W / 1600)
    for t in data["texts"]:
        if t["size"] < min_font - 0.01:
            add("warning", "small_font", [t["node"] or t["edge"] or ""], f"'{t['text']}' {t['size']}px < {min_font:.0f}px")
        if t["node"] and t["node"] in nodes:
            n = nodes[t["node"]]
            if overlap(t["rect"], n["rect"]) < (t["rect"][2] - t["rect"][0]) * (t["rect"][3] - t["rect"][1]) - 1 or \
                    t["rect"][0] < n["rect"][0] + 4 or t["rect"][2] > n["rect"][2] - 4 or \
                    t["rect"][1] < n["rect"][1] + 2 or t["rect"][3] > n["rect"][3] - 2:
                add("error", "text_overflow", [t["node"]], f"'{t['text']}' exceeds its node box")
            fg, bg = parse_rgb(t["fill"]), parse_rgb(n["fill"])
            if fg and bg and contrast(fg, bg) < 4.5:
                add("error", "low_contrast", [t["node"]], f"'{t['text']}' contrast {contrast(fg, bg):.1f}:1")
        if EMOJI.search(t["text"]):
            add("warning", "emoji", [t["node"] or t["edge"] or ""], f"'{t['text']}' contains emoji; use words or a palette shape")
        if "pretendard" not in t["family"].lower() and not re.search(r"consolas|d2coding|mono", t["family"], re.I):
            add("warning", "font_family", [t["node"] or ""], f"'{t['text']}' uses {t['family']}")

    for nid, n in nodes.items():
        segs = sorted((s for t in data["texts"] if t["node"] == nid for s in t["segs"]), key=lambda s: s["top"])
        if not segs:
            continue
        lines: list[list[dict]] = []
        for s in segs:
            if lines and abs(s["top"] - lines[-1][0]["top"]) < 4:
                lines[-1].append(s)
            else:
                lines.append([s])
        if len(lines) > max_lines:
            add("warning", "too_many_lines", [nid], f"{len(lines)} rendered lines in node (max {max_lines})")
        line_texts = ["".join(s["text"] for s in sorted(line, key=lambda s: s["left"])).strip() for line in lines]
        for a, b in zip(line_texts, line_texts[1:]):
            if BREAK_END.search(a) or BREAK_START.match(b):
                add("warning", "number_break", [nid], f"line break splits a figure: '{a[-12:]}' / '{b[:12]}'")
        box_h = n["rect"][3] - n["rect"][1]
        text_h = max(s["bottom"] for s in segs) - min(s["top"] for s in segs)
        if box_h > 0 and text_h / box_h < 0.5:
            add("warning", "card_whitespace", [nid], f"text fills {text_h / box_h:.0%} of the box height")

    for a, b in itertools.combinations(data["texts"], 2):
        if overlap(a["rect"], b["rect"], pad=1) > 4:
            add("error", "text_overlap", [a["node"] or a["edge"] or "", b["node"] or b["edge"] or ""],
                f"'{a['text']}' overlaps '{b['text']}'")

    for a, b in itertools.combinations(data["nodes"], 2):
        if overlap(a["rect"], b["rect"], pad=1) > 0:
            add("error", "node_overlap", [a["id"], b["id"]], "node boxes overlap")

    for e in data["edges"]:
        src, _, dst = e["id"].partition("->")
        if not e["points"]:
            add("error", "edge_no_line", [e["id"]], "edge group has no path/line/polyline")
            continue
        if e["undirected"] and "url(" in e["marker"]:
            add("warning", "undirected_has_arrow", [e["id"]], "edge marked data-undirected has an arrowhead")
        elif not e["undirected"] and "url(" not in e["marker"]:
            add("warning", "edge_no_arrow", [e["id"]], "edge line has no marker; add data-undirected=\"true\" if intended")
        for end, nid, label in ((e["points"][0], src, "start"), (e["points"][-1], dst, "end")):
            if nid not in nodes:
                add("error", "edge_unknown_node", [e["id"]], f"{label} node '{nid}' not found")
            elif abs(edge_gap(end, nodes[nid]["rect"])) > ENDPOINT_TOLERANCE:
                add("error", "edge_endpoint", [e["id"]],
                    f"{label} point {[round(v) for v in end]} is {edge_gap(end, nodes[nid]['rect']):.0f}px from '{nid}' border")
        crossed = {n["id"] for n in data["nodes"] if n["id"] not in (src, dst)
                   and any(inside(p, n["rect"], 2) for p in e["points"])}
        for nid in sorted(crossed):
            add("error", "edge_through_node", [e["id"], nid], f"edge passes through node '{nid}'")
        hits = {t["text"] for t in data["texts"] if t["edge"] != e["id"] and t["node"] not in (src, dst)
                and any(inside(p, t["rect"], 1) for p in e["points"])}
        for text in sorted(hits):
            add("error", "edge_through_text", [e["id"]], f"edge crosses text '{text}'")

    for c in data["colors"]:
        if c.startswith("#") and len(c) == 4:
            c = "#" + "".join(ch * 2 for ch in c[1:])
        if c.startswith("#") and c not in PALETTE:
            add("warning", "off_palette", [], f"color {c} is outside the approved palette")

    if not data["pretendard"]:
        add("warning", "font_missing", [], "Pretendard is not available to the renderer; PNG uses a fallback font")
    if data["external"]:
        add("error", "external_content", [], "svg contains script, foreignObject or remote image")
    if len(data["nodes"]) > 14:
        add("warning", "density", [], f"{len(data['nodes'])} nodes; consider grouping or splitting")

    if spec:
        spec_nodes = {n["id"] for n in spec.get("nodes", [])}
        spec_edges = {f"{e['from']}->{e['to']}" for e in spec.get("edges", [])}
        svg_edges = {e["id"] for e in data["edges"]}
        for nid in sorted(spec_nodes - nodes.keys()):
            add("error", "spec_node_missing", [nid], "node in spec but not in svg")
        for nid in sorted(nodes.keys() - spec_nodes):
            add("warning", "spec_node_extra", [nid], "node in svg but not in spec")
        for eid in sorted(spec_edges - svg_edges):
            reverse = "->".join(reversed(eid.split("->")))
            add("error", "spec_edge_reversed" if reverse in svg_edges else "spec_edge_missing", [eid],
                "edge drawn in reverse direction" if reverse in svg_edges else "edge in spec but not in svg")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("svg", type=Path)
    parser.add_argument("--png", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--spec", type=Path)
    parser.add_argument("--scale", type=float, default=2)
    parser.add_argument("--density", choices=MAX_LINES, default="normal",
                        help="00_packet.md density: normal = label+3 body lines, dense = label+5 body lines")
    args = parser.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        args.report.write_text(json.dumps({"renderer": None, "status": "not_run",
                                           "reason": "playwright is not installed"}, ensure_ascii=False, indent=2), encoding="utf-8")
        print("not_run: playwright is not installed")
        return 2

    svg_text = args.svg.read_text(encoding="utf-8")
    spec = json.loads(args.spec.read_text(encoding="utf-8")) if args.spec else None
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(device_scale_factor=args.scale, viewport={"width": 4000, "height": 4000})
        page.set_content(f"<html><body style='margin:0;background:#fff'>{svg_text}</body></html>")
        page.evaluate("document.fonts.ready")
        data = page.evaluate(COLLECT_JS)
        page.set_viewport_size({"width": int(data["W"]), "height": int(data["H"])})
        page.locator("svg").first.screenshot(path=str(args.png))
        version = browser.version
        browser.close()

    issues = check(data, spec, MAX_LINES[args.density])
    errors = sum(i["severity"] == "error" for i in issues)
    report = {
        "renderer": f"playwright chromium {version}",
        "status": "run",
        "canvas": [data["W"], data["H"]],
        "density": args.density,
        "pretendard_available": data["pretendard"],
        "counts": {"nodes": len(data["nodes"]), "edges": len(data["edges"]), "texts": len(data["texts"])},
        "summary": {"errors": errors, "warnings": len(issues) - errors},
        "issues": issues,
    }
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{'PASS' if not errors else 'FAIL'} errors={errors} warnings={len(issues) - errors} png={args.png}")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
