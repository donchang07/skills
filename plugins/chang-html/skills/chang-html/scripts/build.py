#!/usr/bin/env python3
"""원본 HTML(src) 하나와 강사 노트(notes.json)로 참가자용·강사용 교안 두 파일을 만든다.

사용: python build.py <src.html> <notes.json> [--out 폴더] [--name 파일이름]

- 파일 이름은 원본 <body data-file="..."> 값을 쓴다. data-file이 없을 때만 --name을 쓴다.
- 참가자용 <이름>.html: 표식(<!--GUIDE-->, <!--NOTE:NN-->, /*INSTRUCTOR-CSS*/, /*INSTRUCTOR-JS*/)을 지운다.
- 강사용 <이름> 강사용.html: <!--GUIDE--> 자리에 강사 운영 가이드, <!--NOTE:NN--> 자리에 장별 노트,
  표식 자리에 강사용 CSS·JS를 넣고 <title>·data-file·#file-label·footer의 이름 뒤에 「 강사용」을 붙인다.
- 원본 파일은 바꾸지 않는다. 표준 라이브러리만 쓴다.

notes.json 형식 (assets/notes.example.json 참고, 시간 정보는 넣지 않는다)
{
  "prep": ["강의 전날 준비 항목", ...],
  "principles": ["진행 원칙", ...],
  "sections": {
    "01": {"mode": "강의", "key": "핵심 메시지", "flow": ["진행 1", ...],
           "qa": [["질문", "답"]], "caution": "주의"}
  }
}
mode 값은 진행 형식(강의·시연·실습·점검)만 적는다.
"""
import argparse
import html
import json
import os
import re
import sys

E = html.escape
TIME_KEYS = {"time", "total", "runsheet"}


def fail(msg):
    sys.exit(f"빌드 중단: {msg}")


def mode_label(m):
    # 「A · B」 메타 문자열을 피하려고 가운뎃점 앞뒤 공백을 없앤다(내용은 같음)
    return m.replace(" · ", "·")


def note(num, d):
    flow = "".join(f"<li>{E(x)}</li>" for x in d.get("flow", []))
    qa = ""
    if d.get("qa"):
        items = "".join(f'<div class="in-qa"><p class="q">Q. {E(q)}</p><p class="a">A. {E(a)}</p></div>' for q, a in d["qa"])
        qa = f'<div class="in-block"><p class="in-h">예상 질문과 답</p>{items}</div>'
    cau = f'<p class="in-caution"><b>주의.</b> {E(d["caution"])}</p>' if d.get("caution") else ""
    mode = f'<span class="in-mode">{E(mode_label(d["mode"]))}</span>' if d.get("mode") else ""
    return f'''
    <details open class="instructor-note">
      <summary><span class="in-tag">강사 노트 {num}</span>{mode}</summary>
      <div class="in-body">
        <p class="in-key"><b>핵심 메시지</b>{E(d.get("key", ""))}</p>
        <div class="in-block"><p class="in-h">진행 순서</p><ol>{flow}</ol></div>{qa}{cau}
      </div>
    </details>'''


def guide(data):
    prep = "".join(f'<li><label><input type="checkbox"><span>{E(x)}</span></label></li>' for x in data.get("prep", []))
    prin = "".join(f"<li>{E(x)}</li>" for x in data.get("principles", []))
    return f'''
  <section id="instructor-guide">
    <h2 class="ch">강사 운영 가이드</h2>
    <p class="lead">참가자용 본문은 같고, 각 장 제목 아래에 강사 노트를 더했습니다. 참가자에게는 참가자용 파일만 배포합니다.</p>
    <div class="in-actions no-print">
      <button type="button" onclick="toggleNotes(true)">노트 모두 펼치기</button>
      <button type="button" onclick="toggleNotes(false)">노트 모두 접기</button>
      <button type="button" class="primary" onclick="hideNotes()">화면 공유용: 노트 숨기기</button>
    </div>
    <div class="in-guide">
      <div><p class="in-h">강의 전날 준비</p><ul class="in-prep">{prep}</ul></div>
      <div><p class="in-h">진행 원칙</p><ul class="in-prin">{prin}</ul></div>
    </div>
  </section>'''


CSS = """
/* 강사용 */
.instructor-note{max-width:var(--measure);margin:4px 0 28px;background:#FFF1F5;border:1.5px solid #FF5C8A;border-radius:12px;padding:0;color:var(--text);font-size:15px}
section.dark .instructor-note{color:var(--text)}
.instructor-note > summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:10px;padding:12px 16px}
.instructor-note > summary::-webkit-details-marker{display:none}
.instructor-note > summary::after{content:"접기";margin-left:auto;font-size:13px;color:var(--muted)}
.instructor-note:not([open]) > summary::after{content:"펼치기"}
.in-tag{font-weight:700;color:#B0124A}
.in-mode{font-size:13px;font-weight:500;background:#FFFFFF;border:1px solid #FFB3C8;border-radius:999px;padding:2px 10px}
.in-body{padding:0 16px 16px;display:grid;gap:12px}
.in-body p{margin:0}
.in-key{background:#FFFFFF;border-radius:8px;padding:10px 12px}
.in-key b{margin-right:8px}
.in-h{font-weight:700;font-size:14px;color:#B0124A;margin:0 0 6px}
.in-block ol{margin:0;padding-left:20px;display:grid;gap:4px}
.in-qa{border-left:2px solid #FF5C8A;padding:4px 0 4px 12px;margin-top:8px}
.in-qa .q{font-weight:700}
.in-caution{border-top:1px dashed #FFB3C8;padding-top:10px}
#instructor-guide{background:#FFF1F5;border:1.5px solid #FF5C8A;border-radius:18px;padding:40px 32px;margin-top:56px}
#instructor-guide + section{border-top:0}
.in-actions{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:24px}
.in-actions button{font:500 14px/1 var(--sans);border:1px solid #FF5C8A;background:#FFFFFF;color:var(--text);border-radius:999px;padding:10px 16px;cursor:pointer}
.in-actions button.primary{background:#FF5C8A;color:var(--ink);font-weight:700}
.in-guide{display:grid;grid-template-columns:1fr;gap:20px}
@media(min-width:900px){.in-guide{grid-template-columns:1fr 1fr}}
.in-guide > div{background:#FFFFFF;border-radius:12px;padding:18px 20px;font-size:15px}
.in-prep{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.in-prep label{display:grid;grid-template-columns:20px 1fr;gap:8px;cursor:pointer}
.in-prep input{margin-top:5px;accent-color:#FF5C8A}
.in-prin{margin:0;padding-left:18px;display:grid;gap:8px}
@media(max-width:640px){#instructor-guide{padding:28px 18px}}
"""
JS = ("function toggleNotes(o){document.querySelectorAll('details.instructor-note').forEach(function(d){d.style.display='';d.open=o;});}\n"
      "function hideNotes(){document.querySelectorAll('details.instructor-note').forEach(function(d){d.style.display=d.style.display==='none'?'':'none';});}")


def add_suffix_once(s, pattern, name, label):
    """pattern 안의 첫 name 뒤에 「 강사용」을 붙인다. pattern은 (앞부분)(name) 두 그룹을 가진다."""
    rx = re.compile(pattern.replace("NAME", re.escape(name)))
    s2, n = rx.subn(lambda m: m.group(1) + name + " 강사용", s, count=1)
    if not n:
        fail(f"강사용 이름을 붙일 {label}을(를) 찾지 못했습니다. 원본의 {label}에 「{name}」이 있어야 합니다.")
    return s2


def main():
    ap = argparse.ArgumentParser(description="참가자용·강사용 교안 빌드")
    ap.add_argument("src"); ap.add_argument("notes")
    ap.add_argument("--out", help="출력 폴더(기본: 원본과 같은 폴더)")
    ap.add_argument("--name", help="원본에 data-file이 없을 때 쓸 파일 이름")
    a = ap.parse_args()

    src = open(a.src, encoding="utf-8").read()
    m = re.search(r'<body[^>]*\sdata-file="([^"]+)"', src)
    if m and a.name and a.name != m.group(1):
        fail(f'--name 「{a.name}」과 원본 data-file 「{m.group(1)}」이 다릅니다. 원본 data-file을 고치십시오.')
    P = m.group(1) if m else a.name
    if not P:
        fail("파일 이름을 알 수 없습니다. <body data-file=\"...\">를 넣거나 --name을 주십시오.")

    # 표식 검사
    for mark in ["<!--GUIDE-->", "/*INSTRUCTOR-CSS*/", "/*INSTRUCTOR-JS*/"]:
        if src.count(mark) != 1:
            fail(f"표식 {mark}이(가) {src.count(mark)}개입니다. 정확히 1개여야 합니다.")
    marks = re.findall(r"<!--NOTE:(\d\d)-->", src)
    dup = sorted({x for x in marks if marks.count(x) > 1})
    if dup:
        fail("NOTE 표식이 중복됩니다: " + ", ".join(dup))

    data = json.load(open(a.notes, encoding="utf-8"))
    bad = sorted(TIME_KEYS & set(data))
    if bad:
        fail("notes.json에 시간 항목이 있습니다(" + ", ".join(bad) + "). 시간 정보는 넣지 않습니다.")
    S = data.get("sections", {})
    for k, d in S.items():
        if TIME_KEYS & set(d):
            fail(f"노트 {k}에 시간 항목이 있습니다. 시간 정보는 넣지 않습니다.")
        if not d.get("key"):
            fail(f"노트 {k}에 핵심 메시지(key)가 없습니다.")
    no_note = sorted(set(marks) - set(S))
    no_mark = sorted(set(S) - set(marks))
    if no_note or no_mark:
        msg = []
        if no_note: msg.append("노트가 없는 NOTE 표식: " + ", ".join(no_note))
        if no_mark: msg.append("원본에 NOTE 표식이 없는 노트: " + ", ".join(no_mark))
        fail(" / ".join(msg))

    out_dir = a.out or os.path.dirname(os.path.abspath(a.src))
    os.makedirs(out_dir, exist_ok=True)
    p_path = os.path.join(out_dir, f"{P}.html")
    i_path = os.path.join(out_dir, f"{P} 강사용.html")
    src_abs = os.path.abspath(a.src)
    for p in (p_path, i_path):
        if os.path.abspath(p) == src_abs:
            fail(f"출력 파일이 원본과 같습니다: {p}. 원본 파일 이름을 src_... 처럼 다르게 두십시오.")

    # ---------- 참가자용 ----------
    part = re.sub(r"<!--(GUIDE|NOTE:\d\d)-->", "", src)
    for mark in ["/*INSTRUCTOR-CSS*/", "/*INSTRUCTOR-JS*/"]:
        part = part.replace(mark + "\n", "", 1) if mark + "\n" in part else part.replace(mark, "", 1)

    # ---------- 강사용 ----------
    ins = src
    for k in marks:
        ins = ins.replace(f"<!--NOTE:{k}-->", note(k, S[k]), 1)
    ins = ins.replace("<!--GUIDE-->", guide(data), 1)
    ins = ins.replace("/*INSTRUCTOR-CSS*/", CSS.strip(), 1)
    ins = ins.replace("/*INSTRUCTOR-JS*/", JS, 1)

    # 레일 맨 앞에 강사 가이드 링크
    nav = re.search(r'<nav[^>]*class="[^"]*\brail\b[\s\S]*?</nav>', ins)
    if nav:
        block = nav.group(0)
        new, n = re.subn(r'(\n[ \t]*)(<li><a href="#s01">)',
                         lambda mm: mm.group(1) + '<li><a href="#instructor-guide"><span>00</span>강사 가이드</a></li>' + mm.group(1) + mm.group(2),
                         block, count=1)
        if not n:
            new = block.replace("<ol>", '<ol><li><a href="#instructor-guide"><span>00</span>강사 가이드</a></li>', 1)
        ins = ins[:nav.start()] + new + ins[nav.end():]

    # 이름 표기
    ins = add_suffix_once(ins, r"(<title>[^<]*?)NAME", P, "<title>")
    ins = add_suffix_once(ins, r'(<body[^>]*\sdata-file=")NAME(?=")', P, "data-file")
    ins = add_suffix_once(ins, r'(<span id="file-label">[^<]*?)NAME', P, "#file-label")
    ins = add_suffix_once(ins, r"(<footer[^>]*>[\s\S]*?)NAME", P, "footer")

    for s, label in ((part, "참가자용"), (ins, "강사용")):
        left = re.findall(r"<!--NOTE:\d\d-->|<!--GUIDE-->|/\*INSTRUCTOR-(?:CSS|JS)\*/", s)
        if left:
            fail(f"{label}에 표식이 남았습니다: {sorted(set(left))}")

    open(p_path, "w", encoding="utf-8").write(part)
    open(i_path, "w", encoding="utf-8").write(ins)
    print("참가자용:", p_path)
    print("강사용:  ", i_path)
    print(f"강사 노트 {len(marks)}개: {', '.join(marks)}")


if __name__ == "__main__":
    main()
