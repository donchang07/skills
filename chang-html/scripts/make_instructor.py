#!/usr/bin/env python3
"""참가자용 교안에 강사 운영 가이드와 장별 강사 노트를 넣어 강사용 파일을 만든다.

사용: python make_instructor.py <참가자용.html> <notes.json> [<출력.html>]
출력 기본값: 입력 이름 뒤에 " 강사용" (예: "주제 v2.0 강사용.html"). 참가자용 파일은 바꾸지 않는다.

notes.json 형식 (references/instructor-mode.md 참고)
{
  "total": "3시간 20분",
  "runsheet": [["0:00", "도입", "머리말"], ...],
  "prep": ["강의 전날 준비 항목", ...],
  "principles": ["진행 원칙", ...],
  "sections": {
    "01": {"time": "강의 12분", "mode": "강의 · 시연", "key": "핵심 메시지",
           "flow": ["진행 1", "진행 2"], "qa": [["질문", "답"]], "caution": "주의"}
  }
}
"""
import html, json, os, re, sys

E = html.escape
src, notes_path = sys.argv[1], sys.argv[2]
dst = sys.argv[3] if len(sys.argv) > 3 else re.sub(r"\.html$", " 강사용.html", src)
s = open(src, encoding="utf-8").read()
N = json.load(open(notes_path, encoding="utf-8"))
SEC = N.get("sections", {})


def note(num, d):
    flow = "".join(f"<li>{E(x)}</li>" for x in d.get("flow", []))
    qa = "".join(f'<div style="border-left:2px solid var(--key);padding-left:.75rem"><div class="font-bold c-navy">Q. {E(q)}</div><div>A. {E(a)}</div></div>' for q, a in d.get("qa", []))
    qa = f'<div><div class="font-bold mb-2" style="color:var(--key)">예상 질문과 답</div><div class="space-y-2">{qa}</div></div>' if qa else ""
    cau = f'<div class="sem sem-risk"><span class="lbl">주의</span>{E(d["caution"])}</div>' if d.get("caution") else ""
    return f'''
      <details open class="instructor-note">
        <summary>강사 노트 {num} · {E(d.get("mode", ""))} · {E(d.get("time", ""))}</summary>
        <div class="mt-4 space-y-4">
          <div class="box p-3"><span class="font-bold c-navy">핵심 메시지</span> {E(d.get("key", ""))}</div>
          <div><div class="font-bold mb-1" style="color:var(--key)">진행 순서</div><ol class="list-decimal pl-5 space-y-1">{flow}</ol></div>
          {qa}{cau}
        </div>
      </details>
'''

# 1) 섹션마다 머리(.sec-head) 바로 뒤에 노트 삽입
done = []
def ins(m):
    num = m.group(2)
    if num in SEC:
        done.append(num)
        return m.group(0) + note(num, SEC[num])
    return m.group(0)
s = re.sub(r'(<div class="sec-head">[\s\S]*?class="sec-badge"[^>]*>(\d+)<[\s\S]*?</div>\s*</div>)', ins, s)
# 이전 형식(sec-head가 없는 교안) 호환: 섹션 첫 h2 다음 </div>
if not done:
    out, pos = [], 0
    for m in re.finditer(r"<section[^>]*>", s):
        b = re.search(r">(\d\d)</span>", s[m.end():m.end() + 900])
        if not b or b.group(1) not in SEC: continue
        end = s.find("</div>", s.find("</h2>", m.end())) + len("</div>")
        out += [s[pos:end], note(b.group(1), SEC[b.group(1)])]; pos = end; done.append(b.group(1))
    s = "".join(out) + s[pos:]

# 2) 맨 앞 강사 운영 가이드
rows = "".join(f"<tr><td class='font-mono text-xs'>{E(a)}</td><td>{E(b)}</td><td class='c-sub'>{E(c)}</td></tr>" for a, b, c in N.get("runsheet", []))
prep = "".join(f'<li class="flex gap-2"><input type="checkbox" class="mt-1"><span>{E(x)}</span></li>' for x in N.get("prep", []))
prin = "".join(f"<div>• {E(x)}</div>" for x in N.get("principles", []))
guide = f'''
    <section id="instructor-guide" class="p-8" style="border:2px solid var(--key);background:var(--key-bg)">
      <div class="sec-head"><div class="sec-title">강사 운영 가이드</div><div class="sec-sub">참가자용 본문은 같고, 각 장 머리에 강사 노트를 더했습니다</div></div>
      <div class="flex flex-wrap gap-2 justify-center mb-6 no-print">
        <button onclick="toggleNotes(true)" class="btn">노트 모두 펼치기</button>
        <button onclick="toggleNotes(false)" class="btn">노트 모두 접기</button>
        <button onclick="hideNotes()" class="btn btn-brand">화면 공유용: 노트 숨기기</button>
      </div>
      <div class="grid lg:grid-cols-2 gap-6">
        <div><div class="mid-title mb-2">진행 시간표 ({E(N.get("total", ""))})</div>
          <table class="brand"><thead><tr><th>시각</th><th>내용</th><th>교안</th></tr></thead><tbody>{rows}</tbody></table></div>
        <div><div class="mid-title mb-2">강의 전날 준비</div><ul class="box p-4 space-y-2 text-sm">{prep}</ul></div>
      </div>
      <div class="box p-4 mt-6 text-sm space-y-1"><div class="font-bold c-navy">진행 원칙</div>{prin}</div>
    </section>
'''
s = re.sub(r'(<main[^>]*>)', r"\1" + guide.replace("\\", "\\\\"), s, count=1)

# 3) 이름표와 스크립트
s = re.sub(r"(<title>)([^|<]+?)(\s*\|)", r"\1\2 강사용\3", s, count=1)
s = s.replace('data-file="', 'data-file="__TMP__', 1)
s = re.sub(r'data-file="__TMP__([^"]*)"', lambda m: f'data-file="{m.group(1)} 강사용"', s, count=1)
s = re.sub(r'(<span id="file-label">)([^<]*)(</span>)', r"\1\2 · 강사용\3", s, count=1)
JS = """function toggleNotes(o){document.querySelectorAll('details.instructor-note').forEach(d=>{d.style.display='';d.open=o;});}
    function hideNotes(){document.querySelectorAll('details.instructor-note').forEach(d=>{d.style.display=d.style.display==='none'?'':'none';});}"""
if "/* INSTRUCTOR-JS */" in s:
    s = s.replace("/* INSTRUCTOR-JS */", JS, 1)
else:
    s = s.replace("</script>\n</body>", JS + "\n  </script>\n</body>", 1)

missing = sorted(set(SEC) - set(done))
open(dst, "w", encoding="utf-8").write(s)
print(f"강사용 생성: {dst}\n노트 삽입 {len(done)}개: {', '.join(done)}")
if missing:
    print("교안에서 찾지 못한 섹션 번호:", ", ".join(missing)); sys.exit(1)
