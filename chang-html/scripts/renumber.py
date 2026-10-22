#!/usr/bin/env python3
"""장을 추가·삭제·이동한 뒤 main > section의 id(sNN)를 문서 순서대로 s01, s02, ... 로 다시 매긴다.

사용: python renumber.py <입력.html> <출력.html>

함께 고치는 것
  - section id="sNN"과 문서 안의 모든 #sNN 참조(href, CSS 선택자, 스크립트)
  - 레일 링크 안의 번호 <a href="#sNN"><span>NN</span>
  - <!--NOTE:NN--> 표식: 그 표식이 들어 있는 장의 새 번호로 바꾼다(notes.json 키도 같은 표대로 고치십시오)
#instructor-guide는 번호를 매기지 않는다. 입력을 덮어쓰지 않는다.
본문 속 「09장」 같은 상호 참조는 자동으로 바꾸지 않고 확인할 후보로 알려 준다. 표준 라이브러리만 쓴다.
"""
import os, re, sys


def main():
    if len(sys.argv) != 3:
        sys.exit("사용: python renumber.py <입력.html> <출력.html>")
    src, dst = sys.argv[1], sys.argv[2]
    if os.path.abspath(src) == os.path.abspath(dst):
        sys.exit("입력과 출력이 같습니다. 새 버전 파일 이름을 주십시오.")
    s = open(src, encoding="utf-8").read()

    mm = re.search(r"<main\b[^>]*>([\s\S]*)</main>", s)
    if not mm:
        sys.exit("<main>을 찾지 못했습니다.")
    m_start, m_end = mm.start(1), mm.end(1)
    body = mm.group(1)

    # main 바로 아래 section을 깊이로 구분해 순서대로 찾는다
    secs, depth = [], 0
    for t in re.finditer(r"<(/?)section\b([^>]*)>", body):
        if t.group(1):
            depth -= 1; continue
        if depth == 0:
            idm = re.search(r'\sid="([^"]*)"', t.group(2))
            secs.append((t.start() + m_start, idm.group(1) if idm else ""))
        depth += 1
    secs = [(pos, i) for pos, i in secs if i != "instructor-guide"]
    if not secs:
        sys.exit("main 아래 section이 없습니다.")

    mapping, n = {}, 0
    for pos, old in secs:
        n += 1
        new = f"s{n:02d}"
        if not re.fullmatch(r"s\d\d", old or ""):
            print(f"주의: id가 sNN 형식이 아닌 장({old or 'id 없음'})은 {new}로 바꾸려면 직접 고치십시오.")
            continue
        mapping[old] = new
    if len(set(mapping)) != len([1 for _, o in secs if re.fullmatch(r"s\d\d", o or "")]):
        sys.exit("같은 sNN id가 여러 장에 있습니다. 먼저 중복을 없애십시오.")

    # NOTE 표식: 들어 있는 장의 새 번호
    bounds = [p for p, _ in secs] + [m_end]
    note_map = []
    def note_rep(m):
        pos = m.start()
        for idx in range(len(secs)):
            if bounds[idx] <= pos < bounds[idx + 1]:
                new = f"{idx + 1:02d}"
                note_map.append((m.group(1), new))
                return f"<!--NOTE:{new}-->"
        note_map.append((m.group(1), m.group(1)))
        return m.group(0)
    s2 = re.sub(r"<!--NOTE:(\d\d)-->", note_rep, s)

    # 레일: 번호 span을 새 번호로 바꾸고(href는 아래에서 한 번에 바꾼다), 항목을 새 번호 순서로 정렬한다
    def rail_rep(m):
        old = m.group(2)
        new = mapping.get(old, old)
        return f'{m.group(1)}{old}{m.group(3)}{new[1:]}{m.group(4)}'
    nav = re.search(r'<nav[^>]*class="[^"]*\brail\b[\s\S]*?</nav>', s2)
    if nav:
        block = re.sub(r'(<a\b[^>]*href="#)(s\d\d)("[^>]*>\s*<span>)\d+(</span>)', rail_rep, nav.group(0))
        items = list(re.finditer(r'<li>(?:(?!</li>)[\s\S])*?href="#(s\d\d)"[\s\S]*?</li>', block))
        if items:
            order = sorted(items, key=lambda it: mapping.get(it.group(1), it.group(1)))
            out, pos = [], 0
            for slot, it in zip(items, order):
                out += [block[pos:slot.start()], it.group(0)]; pos = slot.end()
            block = "".join(out) + block[pos:]
        s2 = s2[:nav.start()] + block + s2[nav.end():]

    # id와 #참조를 한 번에 바꾼다
    s2 = re.sub(r'(\sid=")(s\d\d)(")', lambda m: m.group(1) + mapping.get(m.group(2), m.group(2)) + m.group(3), s2)
    s2 = re.sub(r"(#)(s\d\d)\b", lambda m: m.group(1) + mapping.get(m.group(2), m.group(2)), s2)

    open(dst, "w", encoding="utf-8").write(s2)
    changed = [(a, b) for a, b in mapping.items() if a != b]
    nchanged = [(a, b) for a, b in note_map if a != b]
    print(f"장 {len(secs)}개, id 변경 {len(changed)}개" + (": " + ", ".join(f"{a}→{b}" for a, b in changed) if changed else ""))
    print(f"NOTE 표식 {len(note_map)}개, 변경 {len(nchanged)}개" + (": " + ", ".join(f"{a}→{b}" for a, b in nchanged) + " (notes.json 키도 같이 고치십시오)" if nchanged else ""))
    print("변경 없음" if s2 == s else f"저장: {dst}")

    text = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", " ", s2)
    text = re.sub(r"<[^>]+>", " ", text)
    refs = []
    for m in re.finditer(r"(?<![\d#])(\d{1,2})장", text):
        ctx = re.sub(r"\s+", " ", text[max(0, m.start() - 12):m.end() + 8]).strip()
        refs.append(f"{m.group(1)}장 …{ctx}…")
    if refs:
        print(f"본문 상호 참조 후보 {len(refs)}개(직접 확인 필요):")
        for r in refs: print("  " + r)


if __name__ == "__main__":
    main()
