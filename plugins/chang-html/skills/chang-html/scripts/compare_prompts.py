#!/usr/bin/env python3
"""교안의 프롬프트(<pre id="...">) 본문을 이전 버전이나 정본 원고와 글자 단위로 대조한다.

사용: python compare_prompts.py <교안.html> (--baseline <이전.html> | --canon <원고.md>) [--ids a,b]

- 교안: <pre id="X"> 안의 글자(태그 제거, HTML 엔티티 복원)를 비교한다.
- --canon: 원고에서 「(id: X)」가 있는 줄 다음에 오는 첫 ``` 코드 블록을 정본으로 본다.
  정본에 있는 id만 비교한다.
- 줄마다 끝 공백과 앞뒤 빈 줄은 무시한다.
- 결과: id마다 OK / DIFF / MISSING(교안에 없음) / EXTRA(이전 버전에 없던 새 id). DIFF·MISSING이 있으면 종료 코드 1.
표준 라이브러리만 쓴다.
"""
import argparse, difflib, html, re, sys


def norm(t):
    lines = [l.rstrip() for l in t.replace("\r\n", "\n").split("\n")]
    while lines and not lines[0]: lines.pop(0)
    while lines and not lines[-1]: lines.pop()
    return "\n".join(lines)


def pres(path):
    s = open(path, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"<pre\b([^>]*)>([\s\S]*?)</pre>", s):
        idm = re.search(r'\sid="([^"]+)"', " " + m.group(1))
        if idm:
            out[idm.group(1)] = norm(html.unescape(re.sub(r"<[^>]+>", "", m.group(2))))
    return out


def canon(path):
    lines = open(path, encoding="utf-8").read().replace("\r\n", "\n").split("\n")
    out, i = {}, 0
    while i < len(lines):
        m = re.search(r"\(id:\s*([^)\s]+)\s*\)", lines[i])
        if m:
            j = i + 1
            while j < len(lines) and not lines[j].lstrip().startswith("```"):
                if re.search(r"\(id:\s*[^)\s]+\s*\)", lines[j]): break
                j += 1
            if j < len(lines) and lines[j].lstrip().startswith("```"):
                fence = lines[j].lstrip()[:3]
                k = j + 1
                while k < len(lines) and not lines[k].lstrip().startswith(fence): k += 1
                out[m.group(1)] = norm("\n".join(lines[j + 1:k]))
                i = k
        i += 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--baseline"); g.add_argument("--canon")
    ap.add_argument("--ids", help="비교할 id 목록(쉼표 구분)")
    a = ap.parse_args()

    cur = pres(a.html)
    ref = pres(a.baseline) if a.baseline else canon(a.canon)
    if a.canon and not ref:
        sys.exit("원고에서 「(id: X)」 다음의 코드 블록을 찾지 못했습니다.")
    ids = [x.strip() for x in a.ids.split(",") if x.strip()] if a.ids else None
    keys = ids if ids else list(ref) + ([k for k in cur if k not in ref] if a.baseline else [])

    bad = 0
    count = {"OK": 0, "DIFF": 0, "MISSING": 0, "EXTRA": 0}
    for k in keys:
        if k not in ref and k in cur:
            st = "EXTRA" if a.baseline else "MISSING"
            if st == "MISSING":
                print(f"MISSING {k}: 기준에 없습니다"); bad += 1
            else:
                print(f"EXTRA   {k}: 이전 버전에 없던 프롬프트")
            count[st] += 1; continue
        if k not in cur:
            print(f"MISSING {k}: 교안에 없습니다" if k in ref else f"MISSING {k}: 양쪽에 없습니다")
            count["MISSING"] += 1; bad += 1; continue
        if cur[k] == ref[k]:
            print(f"OK      {k}"); count["OK"] += 1
        else:
            print(f"DIFF    {k}")
            d = list(difflib.unified_diff(ref[k].split("\n"), cur[k].split("\n"), "기준", "교안", lineterm="", n=1))
            for line in d[:24]: print("        " + line)
            if len(d) > 24: print(f"        … {len(d) - 24}줄 더")
            count["DIFF"] += 1; bad += 1
    skipped = len([k for k in cur if k not in keys])
    print("RESULT", " ".join(f"{k}={v}" for k, v in count.items()) + (f" 비교제외={skipped}" if skipped else ""))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
