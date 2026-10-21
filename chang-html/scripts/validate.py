#!/usr/bin/env python3
"""chang-html 교안 정적 검사. 표준 라이브러리만 사용한다.

사용: python validate.py <교안.html> [--baseline <이전버전.html>] [--json <보고서.json>]

검사 항목
  structure   태그 짝(이전 버전보다 불일치가 늘면 실패)
  copy-ids    copyPrompt('id')의 대상이 있는지, id가 중복되지 않는지
  tabs        switchTab('id')의 대상과 btn-id가 있는지
  terms       금지어(참가자 영역): 학생, 구멍, 회차
  badges      .sec-badge 번호가 01부터 빈칸 없이 이어지는지
  leftovers   {{자리표시}}, TODO, lorem 이 남았는지
  colors      팔레트 밖 HEX 색(경고)
강사 노트(.instructor-note)와 강사 운영 가이드(#instructor-guide) 안의 금지어는 검사하지 않는다.
"""
import argparse, json, re, sys
from html.parser import HTMLParser

BANNED = ["학생", "구멍", "회차"]
PALETTE = {c.lower() for c in """1B2A4A 2C3E5A 7F8FA9 3A86FF FFFFFF F5F5F7 B45309 FFF4E8 0F766E EAF6F3
2563EB EDF3FF 355C7D EEF2F6 7C3AED F3EEFE 0F172A E2E8F0 F8FAFC CBD5E1 93C5FD 000000 FFF FFFFFF""".split()}
VOID = {"br", "img", "input", "meta", "link", "hr", "source", "area", "base", "col", "embed", "param", "track", "wbr"}
SVG_LEAF = {"path", "rect", "circle", "line", "polygon", "ellipse", "polyline", "use", "stop"}


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


def balance(text):
    p = Balance(); p.feed(text); return len(p.stack), p.mismatch


def strip_instructor(text):
    text = re.sub(r'<details[^>]*class="[^"]*instructor-note[\s\S]*?</details>', "", text)
    text = re.sub(r'<section[^>]*id="instructor-guide"[\s\S]*?</section>', "", text)
    return text


def visible_text(text):
    text = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", " ", text)
    return re.sub(r"<[^>]+>", " ", text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html"); ap.add_argument("--baseline"); ap.add_argument("--json")
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

    ids = re.findall(r'\sid="([^"]+)"', s)
    dup = sorted({i for i in ids if ids.count(i) > 1})
    copy = re.findall(r"copyPrompt\('([^']+)'\)", s)
    missing = sorted({c for c in copy if c not in ids})
    res["copy-ids"] = dict(ok=not dup and not missing, buttons=len(copy), duplicate_ids=dup, missing_targets=missing)

    tabs = re.findall(r"switchTab\('([^']+)'\)", s)
    tmiss = sorted({t for t in tabs if t not in ids or ("btn-" + t) not in ids})
    res["tabs"] = dict(ok=not tmiss, missing=tmiss)

    vt = visible_text(strip_instructor(s))
    hits = {w: vt.count(w) for w in BANNED if w in vt}
    res["terms"] = dict(ok=not hits, hits=hits)

    badges = re.findall(r'class="sec-badge"[^>]*>(\d+)<', s)
    if not badges:  # 이전 형식(v2.0 이하) 호환: 섹션 머리의 두 자리 번호
        badges = []
        for m in re.finditer(r"<section[^>]*>", s):
            b = re.search(r">(\d\d)</span>", s[m.end():m.end() + 900])
            if b: badges.append(b.group(1))
    seq = [int(b) for b in badges]
    res["badges"] = dict(ok=seq == list(range(1, len(seq) + 1)), found=badges)

    left = re.findall(r"\{\{[A-Z0-9_]+\}\}|TODO|lorem", strip_instructor(s))
    res["leftovers"] = dict(ok=not left, found=sorted(set(left))[:20])

    hexes = {h.lower() for h in re.findall(r"#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b", re.sub(r"<script[\s\S]*?</script>", "", s))}
    off = sorted(hexes - PALETTE)
    res["colors"] = dict(ok=True, warning_off_palette=off[:30])

    fail = [k for k, v in res.items() if not v["ok"]]
    for k, v in res.items():
        print(f"{'PASS' if v['ok'] else 'FAIL'} {k}: " + json.dumps({x: y for x, y in v.items() if x != 'ok'}, ensure_ascii=False))
    if a.json:
        json.dump(res, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("RESULT", "PASS" if not fail else "FAIL " + ",".join(fail))
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
