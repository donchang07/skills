#!/usr/bin/env python3
"""chang-html 교안 정적 검사. 표준 라이브러리만 사용한다.

사용: python validate.py <교안.html> [--baseline <이전버전.html>] [--json <보고서.json>] [--source]

검사 항목
  structure   태그 짝(이전 버전보다 불일치가 늘면 실패)
  copy-ids    copyPrompt('id')의 대상이 있는지, id가 중복되지 않는지
  tabs        switchTab('id')의 대상과 btn-id가 있는지
  terms       금지어(참가자 영역): 학생, 수강생, 구멍, 회차
  time        참가자 화면 글(pre·code 밖)의 시간 표기: 숫자+분(「N분의 M」 제외), 숫자+시간, hh:mm, 「강의 시간」
  sections    main > section id가 s01부터 빈칸 없이 이어지는지, 레일 링크(#...) 대상이 있는지
  markers     빌드 결과에 표식(<!--NOTE:NN-->, <!--GUIDE-->, /*INSTRUCTOR-...*/)이 남았는지
              --source를 주면 반대로 원본 표식이 하나씩 있는지 확인한다(src_*.html 검사용)
  badges      .sec-badge 번호가 01부터 이어지는지(없으면 해당 없음)
  leftovers   {{자리표시}}, TODO, lorem 이 남았는지
  colors      :root에 선언한 HEX와 #FFFFFF·#000000 밖의 색(경고만)
강사 노트(.instructor-note)와 강사 운영 가이드(#instructor-guide) 안은 terms·time·leftovers에서 검사하지 않는다.
"""
import argparse, json, re, sys
from html.parser import HTMLParser

BANNED = ["학생", "수강생", "구멍", "회차"]
VOID = {"br", "img", "input", "meta", "link", "hr", "source", "area", "base", "col", "embed", "param", "track", "wbr"}
SVG_LEAF = {"path", "rect", "circle", "line", "polygon", "ellipse", "polyline", "use", "stop"}
TIME_PATTERNS = [
    (r"\d+\s*분(?!\s*의\s*\d)", "숫자+분"),
    (r"\d+\s*시간", "숫자+시간"),
    (r"(?<![\d:])\d{1,2}:\d{2}(?![\d:])", "hh:mm"),
    (r"강의\s*시간", "강의 시간"),
]


class Balance(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack = []; self.mismatch = 0
    def handle_starttag(self, t, a):
        if t not in VOID and t not in SVG_LEAF: self.stack.append(t)
    def handle_startendtag(self, t, a): pass
    def handle_endtag(self, t):
        if t in SVG_LEAF or t in VOID: return
        if self.stack and self.stack[-1] == t: self.stack.pop()
        else: self.mismatch += 1


class MainSections(HTMLParser):
    """main의 바로 아래 section id를 문서 순서대로 모은다."""
    def __init__(self):
        super().__init__(); self.stack = []; self.ids = []
    def handle_starttag(self, t, a):
        if t in VOID or t in SVG_LEAF: return
        if t == "section" and self.stack and self.stack[-1] == "main":
            self.ids.append(dict(a).get("id") or "")
        self.stack.append(t)
    def handle_endtag(self, t):
        if t in VOID or t in SVG_LEAF: return
        if t in self.stack:
            while self.stack and self.stack.pop() != t: pass


def balance(text):
    p = Balance(); p.feed(text); return len(p.stack), p.mismatch


def strip_instructor(text):
    text = re.sub(r'<details[^>]*class="[^"]*instructor-note[\s\S]*?</details>', "", text)
    text = re.sub(r'<section[^>]*id="instructor-guide"[\s\S]*?</section>', "", text)
    return text


def visible_text(text):
    text = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", " ", text)
    text = re.sub(r"<!--[\s\S]*?-->", " ", text)
    return re.sub(r"<[^>]+>", " ", text)


def prose_text(text):
    """pre·code·title 밖의 참가자 화면 글."""
    text = re.sub(r"<(pre|code|title)\b[\s\S]*?</\1>", " ", text)
    return visible_text(text)


def expand_hex(h):
    h = h.lower()
    return "".join(c * 2 for c in h) if len(h) == 3 else h


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html"); ap.add_argument("--baseline"); ap.add_argument("--json")
    ap.add_argument("--source", action="store_true", help="빌드 전 원본(src_*.html)을 검사한다")
    a = ap.parse_args()
    s = open(a.html, encoding="utf-8").read()
    res = {}

    unclosed, mism = balance(s)
    ok = unclosed == 0
    if a.baseline:
        bu, bm = balance(open(a.baseline, encoding="utf-8").read())
        ok = ok and mism <= bm
        res["structure"] = dict(ok=ok, unclosed=unclosed, mismatch=mism, baseline_mismatch=bm)
    else:
        ok = ok and mism == 0
        res["structure"] = dict(ok=ok, unclosed=unclosed, mismatch=mism)

    code = re.sub(r"<!--[\s\S]*?-->", "", s)  # 주석 속 예시는 검사하지 않는다
    ids = re.findall(r'\sid="([^"]+)"', code)
    dup = sorted({i for i in ids if ids.count(i) > 1})
    copy = re.findall(r"copyPrompt\('([^']+)'\)", code)
    missing = sorted({c for c in copy if c not in ids})
    res["copy-ids"] = dict(ok=not dup and not missing, buttons=len(copy), duplicate_ids=dup, missing_targets=missing)

    tabs = re.findall(r"switchTab\('([^']+)'\)", code)
    tmiss = sorted({t for t in tabs if t not in ids or ("btn-" + t) not in ids})
    res["tabs"] = dict(ok=not tmiss, missing=tmiss)

    part = strip_instructor(s)
    vt = visible_text(part)
    hits = {w: vt.count(w) for w in BANNED if w in vt}
    res["terms"] = dict(ok=not hits, hits=hits)

    pt = prose_text(part)
    th = []
    for rx, label in TIME_PATTERNS:
        for m in re.finditer(rx, pt):
            ctx = re.sub(r"\s+", " ", pt[max(0, m.start() - 15):m.end() + 10]).strip()
            th.append(f"{label}: …{ctx}…")
    res["time"] = dict(ok=not th, found=th[:20])

    ms = MainSections(); ms.feed(s)
    secs = [i for i in ms.ids if i != "instructor-guide"]
    want = [f"s{n:02d}" for n in range(1, len(secs) + 1)]
    nav = re.search(r'<nav[^>]*class="[^"]*\brail\b[\s\S]*?</nav>', s)
    rail = re.findall(r'href="#([^"]+)"', nav.group(0)) if nav else []
    rail_missing = sorted({r for r in rail if r not in ids})
    unlinked = [x for x in secs if nav and x not in rail]
    res["sections"] = dict(ok=bool(secs) and secs == want and not rail_missing, found=secs,
                           rail_missing=rail_missing, not_in_rail=unlinked)

    mk = re.findall(r"<!--NOTE:\d\d-->|<!--GUIDE-->|/\*INSTRUCTOR-(?:CSS|JS)\*/", s)
    if a.source:
        cnt = {m: mk.count(m) for m in ["<!--GUIDE-->", "/*INSTRUCTOR-CSS*/", "/*INSTRUCTOR-JS*/"]}
        notes = [m for m in mk if m.startswith("<!--NOTE:")]
        ndup = sorted({n for n in notes if notes.count(n) > 1})
        res["markers"] = dict(ok=all(v == 1 for v in cnt.values()) and not ndup, mode="source",
                              counts=cnt, notes=len(notes), duplicate_notes=ndup)
    else:
        res["markers"] = dict(ok=not mk, left=sorted(set(mk)))

    badges = re.findall(r'class="sec-badge"[^>]*>(\d+)<', s)
    if badges:
        seq = [int(b) for b in badges]
        res["badges"] = dict(ok=seq == list(range(1, len(seq) + 1)), found=badges)
    else:
        res["badges"] = dict(ok=True, found="해당 없음")

    left = re.findall(r"\{\{[A-Z0-9_]+\}\}|TODO|lorem", part)
    res["leftovers"] = dict(ok=not left, count=len(left), found=sorted(set(left))[:20])

    root = re.search(r":root\s*\{([^}]*)\}", s)
    palette = {expand_hex(h) for h in re.findall(r"#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b", root.group(1))} if root else set()
    palette |= {"ffffff", "000000"}
    no_script = re.sub(r"<script[\s\S]*?</script>", "", s)
    hexes = {expand_hex(h) for h in re.findall(r"#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b", no_script)}
    off = sorted(hexes - palette)
    res["colors"] = dict(ok=True, palette_from_root=len(palette) - 2, warning_off_palette=off[:30])

    fail = [k for k, v in res.items() if not v["ok"]]
    for k, v in res.items():
        print(f"{'PASS' if v['ok'] else 'FAIL'} {k}: " + json.dumps({x: y for x, y in v.items() if x != 'ok'}, ensure_ascii=False))
    if a.json:
        json.dump(res, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("RESULT", "PASS" if not fail else "FAIL " + ",".join(fail))
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
