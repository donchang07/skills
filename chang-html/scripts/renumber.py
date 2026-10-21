#!/usr/bin/env python3
"""섹션을 추가·삭제·이동한 뒤 .sec-badge 번호를 문서 순서대로 01, 02, ... 로 다시 매긴다.

사용: python renumber.py <입력.html> <출력.html>
출력은 새 버전 파일이어야 한다. 입력을 덮어쓰지 않는다.
본문 속 "01장", "02의" 같은 상호 참조는 자동으로 바꾸지 않고 목록으로 알려 준다.
"""
import re, sys

src, dst = sys.argv[1], sys.argv[2]
if src == dst:
    sys.exit("입력과 출력이 같습니다. 새 버전 파일 이름을 주십시오.")
s = open(src, encoding="utf-8").read()
n = 0
mapping = []
def rep(m):
    global n
    n += 1
    mapping.append((m.group(2), f"{n:02d}"))
    return f"{m.group(1)}{n:02d}<"
s2 = re.sub(r'(class="sec-badge"[^>]*>)(\d+)<', rep, s)
open(dst, "w", encoding="utf-8").write(s2)
changed = [(a, b) for a, b in mapping if a != b]
print(f"섹션 {n}개, 번호 변경 {len(changed)}개: " + ", ".join(f"{a}→{b}" for a, b in changed))
if changed:
    refs = sorted(set(re.findall(r"(?<![\d#])(\d\d)(?:장|의|번|-\d)", re.sub(r"<[^>]+>", " ", s2))))
    print("본문 상호 참조 후보(직접 확인 필요):", ", ".join(refs))
