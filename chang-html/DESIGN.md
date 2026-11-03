# DESIGN.md — chang-html 디자인 기준

모든 chang-html 교안에 **항상** 적용하는 디자인 기준이다. 「문서 질의응답 AI 방식 v2.5」(기준일 2026-10-28, `G:\내 드라이브\CEO_AI_Coding\CEO_18기\8.RAG\`)에서 뽑았다.

## 적용 규칙

- 새 교안, 장 추가, 수정, 강사용 모두 이 문서를 따른다. 제작 담당은 시작 전에 읽고, 검수 담당은 이 문서를 판정 근거로 쓴다.
- 이 문서를 덮어쓸 수 있는 것은 사용자의 명시적 요청뿐이다. 「chang-ppt 브랜드」를 요청하면 [references/chang-ppt-brand.md](references/chang-ppt-brand.md)로 색과 구조만 바꾸고, 글꼴·품질 바닥·부품 규칙은 이 문서를 그대로 쓴다.
- 디자인 브리프(`{RUN}/_workspace/02_design_brief.md`)는 이 문서 안에서 교안마다 정할 것만 적는다(아래 「디자인 브리프」). 토큰·글꼴·간격을 브리프에서 바꾸지 않는다.
- `assets/template.html`은 v1.9 기준이라 v2.5 부품(실습 단계 목록·카드, 위치 배지, PowerShell 입력 상자, 예상 요약, 한계 상자, 방식 장 색 테마)이 없다. 필요하면 아래 「v2.5 부품 CSS」를 그대로 옮겨 쓴다.

## 원칙

1. **ink와 paper 두 면.** 첫 화면·프롬프트 상자·표 머리·체크리스트는 진한 남색(ink), 본문은 밝은 회청색(paper). 그 밖의 바탕은 흰색 카드다.
2. **의미색은 비교 대상에만.** 교안이 비교하는 방식·구분(최대 4개)에 색을 하나씩 주고, 그 뜻 밖에서는 쓰지 않는다. 위치 배지·판정 배지·강조처럼 의미가 다른 것은 중립색과 모양(실선·점선·굵기)으로 구분한다.
3. **대담함은 한 곳.** 첫 화면 오른쪽의 직접 조작 데모(같은 문서를 방식별로 다르게 읽는 장면)에만 움직임과 색을 몰아 쓴다. 본문은 조용하게.
4. **같은 뼈대, 다른 색.** 같은 성격의 장(방식별 장)은 구조를 똑같이 두고 색 테마 변수만 바꾼다.

## 색 토큰

```css
:root{
  --ink:#0E1A3B; --ink-2:#18264D; --paper:#F5F6FA; --text:#172036; --muted:#5A6480; --line:#D9DEEA;
  --long:#14B8A6; --rag:#6C5CFF; --wiki:#FFC93C; --tree:#F2643D;
  --long-ink:#0F766E; --rag-ink:#5243D9; --wiki-ink:#8A6100; --wiki-line:#E0A800; --tree-ink:#B93E1C;
  --on-ink:#F5F6FA; --on-ink-muted:#B4BDD6; --ink-line:#2B3A66;
}
```

| 토큰 | 쓰임 |
|---|---|
| ink / ink-2 / ink-line | 어두운 면 / 어두운 면 위 카드·분할 버튼 바탕 / 어두운 면의 구분선 |
| paper / text / muted / line | 본문 바탕 / 본문 글자 / 보조 글자(흰 바탕 대비 약 6:1) / 구분선·표 선 |
| on-ink / on-ink-muted | 어두운 면 위 글자 / 보조 글자. 첫 화면 리드는 `#D3D9EA`, 체크리스트 설명은 `#C9D0E4` |
| 의미색 4개 (`--long --rag --wiki --tree`) | 비교 대상 1~4. 이름은 교안 주제에 맞게 바꿔도 값은 유지한다 |
| `*-ink` | 의미색을 **글자**로 쓸 때(흰 바탕 대비 확보). 노랑 선은 `--wiki-line` |
| 옅은 바탕 | 의미색 rgba: 보라 .07, 청록 .09, 노랑 .17, 주황 .08 |
| 강사 노트 | `#FF5C8A` 테두리 / `#FFF1F5` 바탕. 강사용에만 |
| 기타 회색 | 인라인 코드·웹 배지 `#E8EBF3`, 강조 행 `#F0F2F8`, 답 상자 `#FAFBFD` |

- 의미색 위 글자: 보라 위는 흰색, 청록·노랑·주황 위는 ink.
- 장식용 그라데이션 금지. 첫 화면 바탕에만 의미색을 옅게 겹친 radial 빛(불투명도 .16~.38)을 허용한다.
- 교안의 비교 대상이 3개 이하이면 앞에서부터 쓰고 남는 색은 쓰지 않는다.

## 글꼴과 글자 크기

| 용도 | 글꼴 |
|---|---|
| 제목·본문·그림 글자 | Pretendard Variable — `https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css` |
| 프롬프트·명령·코드·폴더 구조·단계 번호 | D2Coding — `https://cdn.jsdelivr.net/npm/d2coding@1.3.2/d2coding-subset.css` |

- 대체 순서: `--sans:'Pretendard Variable',Pretendard,-apple-system,BlinkMacSystemFont,system-ui,'Apple SD Gothic Neo','Malgun Gothic',sans-serif`, `--mono:'D2Coding','D2Coding Fill',Consolas,'Courier New',monospace`.
- 템플릿에 내장된 `D2Coding Fill`(경량판에 없는 공백·`{` `}`만 담은 약 1KB)은 지우지 않는다.
- 고정폭에서 한글은 2칸으로 세어 열을 맞춘다. Google Fonts·Tailwind CDN은 쓰지 않는다.

| 요소 | 크기 / 굵기 / 자간 |
|---|---|
| 본문 | 16px, 줄 간격 1.7, 자간 -.005em |
| 첫 화면 h1 | clamp(2.6rem, 5.4vw, 4.4rem) / 860 / -.03em, 부제 .52em·650 |
| 장 제목 `h2.ch` | 30px(휴대폰 26px) / 780 / -.025em, 최대 24em |
| 소제목 h3 | 22px / 720 / -.02em, 실습 카드 제목 19px |
| 리드 `.lead`, 첫 화면 리드 | 18px, 줄 간격 1.75 |
| 표 | 15px, 머리 14px·700 |
| 보조(출처·캡션·배지) | 13~14px |
| 큰 번호(체크리스트) | 22px / 900 |

## 배치와 간격

```
[툴바(sticky, ink 96%): 파일 이름·기준일 | 교안 다운로드 · PDF로 인쇄]
[첫 화면(ink): 왼쪽 byline·h1·리드·실습 소재 줄·의미색 범례 | 오른쪽 데모(분할 버튼 + 흰 문서 시트)]
[레일 목차 200px(1280px 이상, sticky)] [main 최대 1000px: 장 01~NN]
[footer]
```

- 폭: 바깥 1320px, 본문 줄 길이 `--measure:680px`. 표·그림은 더 넓게.
- 장 간격: 위 60px + 장 사이 구분선과 60px(휴대폰 44px). `scroll-margin-top` 60~72px.
- 둥글기: 패널·그림·데모 시트 18px, 프롬프트 상자·카드 12px, 흐름 상자 10px, 데모 줄 8px, 위치 배지 6px, 칩·버튼 알약(999px), 표는 각진 모서리.
- 장 번호는 레일에만 둔다. 장 제목 위 대문자 라벨 금지. 방식 장은 제목 위에 48×6px 의미색 막대만.
- 휴대폰 첫 화면 순서: byline → h1 → 데모 → 리드 → 범례(데모를 위로 올린다).

## 부품

| 부품 | 규칙 |
|---|---|
| 툴바 | 버튼은 투명 알약 + `#3A4A78` 테두리. 휴대폰에서는 고정 해제, 기준일 숨김 |
| 범례 `.legend` | 의미색 점 12px + 이름 + 설명, 위아래 ink-line 구분선 |
| 데모 | 분할 버튼 `.seg`(눌림=paper 바탕), 흰 시트에 줄 번호·형광펜 표시. 방식마다 다른 시각 문법: 전체 강조 / 조각만 남기고 흐림 / 흐림+정리 카드 / 범위 막대 |
| 리드·본문 | `.lead`(라벨 14px muted), `.prose`, 출처 `.src` 13px, 주의 `.caution`(왼쪽 3px text 막대), 다음 장 안내 `.next-ch` |
| 표 `.tbl` | 흰 바탕+line 테두리, 머리 ink 바탕. 첫 열 굵게·nowrap, 핵심 행 `tr.key`(왼쪽 4px text 막대), 의미색 열은 머리 위 5px 막대와 아주 옅은 열 바탕 |
| 그림 `.fig` | 흰 패널 18px, SVG 최소 680px. 820px 이하에서 오른쪽 흐림 + 「옆으로 밀어 끝까지 볼 수 있습니다」 |
| 실습 단계 목록 `.lab-toc` | 장 앞에 단계 번호(mono)·위치 배지·단계 이름 3열 목록 |
| 실습 단계 카드 `.sc` | 왼쪽 3px 의미색 막대. 머리(번호·위치 배지·제목) 아래 「할 일 / 확인(체크 표시) / 막히면(점선 위 구분)」 행 |
| 위치 배지 `.loc` | 의미색 금지, 모양으로 구분: PowerShell = ink 바탕 + `PS>`, Claude Code = 흰 바탕 text 테두리, 브라우저 = 회색 바탕 점선 |
| 프롬프트 상자 `.code` | ink 바탕, 머리에 제목 + paper 알약 「복사」 버튼 |
| PowerShell 입력 상자 `.code-ps` | 흰 바탕 + 왼쪽 4px ink 막대, 머리 `#F0F2F8`, 복사 버튼은 ink. 예시(입력 안 함)는 막대를 점선 `.code-ex` |
| 예상 요약 `.expect` | 의미색 옅은 바탕, 항목명 10.5em + 내용 2열, 한계 행은 진한 구분선 |
| 한계 상자 `.limit` | 흰 바탕 + 왼쪽 4px 의미색, 제목은 `*-ink` 글자 |
| 해결 칩 `.solves` | 의미색 테두리 알약, 앞에 코드 배지 |
| 판정 배지 `.v` | 충족 = text 바탕 흰 글자, 부분 = 흰 바탕 점선. 의미색 쓰지 않음 |
| 체크리스트 `section.dark` | ink 바탕 18px, 2열, 큰 번호 22px·900 |
| 선택 표시 `.opt` | 「필요할 때만」 같은 회색 테두리 알약 |
| 토스트 | 오른쪽 아래 text 바탕 알약, 복사 완료 알림 |

## v2.5 부품 CSS

템플릿에 없을 때 그대로 옮긴다(원본 교안과 같은 값).

```css
section.m-rag{--m:var(--rag);--m-on:#FFFFFF;--m-soft:rgba(108,92,255,.07);--m-ink:var(--rag-ink)}
section.m-long{--m:var(--long);--m-on:var(--ink);--m-soft:rgba(20,184,166,.09);--m-ink:var(--long-ink)}
section.m-wiki{--m:var(--wiki);--m-on:var(--ink);--m-soft:rgba(255,201,60,.17);--m-ink:var(--wiki-ink)}
section.m-tree{--m:var(--tree);--m-on:var(--ink);--m-soft:rgba(242,100,61,.08);--m-ink:var(--tree-ink)}
section.sol h2.ch::before{content:"";display:block;width:48px;height:6px;border-radius:3px;background:var(--m);margin:0 0 18px}
.limit{max-width:var(--measure);margin:20px 0 0;padding:14px 18px 15px;background:#FFFFFF;border:1px solid var(--line);border-left:4px solid var(--m);border-radius:0 12px 12px 0}
.limit strong{display:block;font-size:14px;color:var(--m-ink);margin-bottom:2px}
.expect{margin-top:18px;max-width:var(--measure);background:var(--m-soft);border-radius:12px;padding:14px 18px 12px}
.expect li{display:grid;grid-template-columns:minmax(0,10.5em) minmax(0,1fr);gap:12px;font-size:14.5px;line-height:1.5;padding:6px 0;border-top:1px solid rgba(14,26,59,.09)}
.loc{display:inline-flex;align-items:center;gap:5px;font:700 12px/1 var(--sans);padding:4px 8px;border-radius:6px;white-space:nowrap;border:1.5px solid transparent}
.loc i{font:700 11.5px/1 var(--mono);font-style:normal}
.loc-ps{background:var(--ink);border-color:var(--ink);color:var(--on-ink)} .loc-ps i{color:#AEB9D9}
.loc-cc{background:#FFFFFF;border-color:var(--text);color:var(--text)}
.loc-web{background:#E8EBF3;border:1.5px dashed var(--muted);color:var(--text)}
.lab-toc{max-width:var(--measure);margin:36px 0 0;background:#FFFFFF;border:1px solid var(--line);border-radius:12px;padding:12px 18px 6px}
.lab-toc a{display:grid;grid-template-columns:2.6em 9.4em minmax(0,1fr);align-items:center;column-gap:10px;padding:7px 0;text-decoration:none;color:var(--text);font-size:15px}
.lab-toc .sn{font:700 14px/1 var(--mono);color:var(--m-ink,var(--text))}
.sc{margin-top:14px;background:#FFFFFF;border:1px solid var(--line);border-left:3px solid var(--m,var(--text));border-radius:0 12px 12px 0;padding:16px 20px 18px;scroll-margin-top:72px}
.sc-head{display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px}
.sc-num{font:800 17px/1 var(--mono);color:var(--m-ink,var(--text));min-width:2.4em}
.sc h3{margin:0;font-size:19px;line-height:1.4;font-weight:720;letter-spacing:-.015em;flex:1 1 14em;min-width:0}
.sc-row{display:grid;grid-template-columns:62px minmax(0,1fr);column-gap:14px;margin:12px 0 0;font-size:15.5px;line-height:1.65}
.sc-lab{font-size:13px;font-weight:700;color:var(--muted);padding-top:3px;white-space:nowrap}
.sc-row.stuck{padding-top:12px;border-top:1px dashed var(--line)}
.sc > .code,.sc > .expect{margin:12px 0 0 76px}
.code.code-ps{background:#FFFFFF;color:var(--text);border:1px solid var(--line);border-left:4px solid var(--ink)}
.code-ps .code-head{background:#F0F2F8;border-bottom:1px solid var(--line);padding:6px 8px 6px 14px}
.code-ps pre{color:var(--text);padding:10px 16px 12px}
.code-ps .copy{background:var(--ink);color:var(--on-ink);padding:7px 14px}
.code-ex{border-left-style:dashed}
@media(max-width:640px){
  .sc{padding:14px 14px 16px} .sc h3{font-size:17.5px;flex-basis:100%}
  .sc-row{grid-template-columns:minmax(0,1fr);row-gap:2px;font-size:15px}
  .sc > .code,.sc > .expect{margin-left:0}
  .expect li{grid-template-columns:minmax(0,1fr);gap:2px}
  .lab-toc a{grid-template-columns:2.6em minmax(0,1fr);row-gap:4px}
}
@media print{
  .code.code-ps,.code-ps .code-head{background:#FFFFFF}
  .loc-ps{background:#FFFFFF;color:var(--text);border-color:var(--text)} .loc-ps i{color:var(--text)}
  .sc,.expect{break-inside:avoid}
}
```

실습 단계 카드 마크업:

```html
<div class="sc" id="st-1-2">
  <div class="sc-head"><b class="sc-num">1-2</b><span class="locs"><span class="loc loc-ps"><i>PS&gt;</i>PowerShell</span></span><h3>단계 이름</h3></div>
  <div class="sc-row"><span class="sc-lab">할 일</span><div class="sc-tx">…</div></div>
  <div class="code code-ps"><div class="code-head"><h4><small>PS&gt;</small>PowerShell에 입력</h4><button type="button" class="copy no-print" onclick="copyPrompt('ps-1-2')" aria-label="1-2 … 복사">복사</button></div><pre id="ps-1-2">…</pre></div>
  <div class="sc-row ok"><span class="sc-lab">확인</span><div class="sc-tx">…</div></div>
  <div class="sc-row stuck"><span class="sc-lab">막히면</span><div class="sc-tx">…</div></div>
</div>
```

## 반응형

| 폭 | 바뀌는 것 |
|---|---|
| 1280px 이상 | 레일 목차 표시, 본문 2열 그리드 |
| 1024px 이상 | 첫 화면 2열 |
| 760px 이상 | 대비 카드·체크리스트 2열 |
| 900px / 820px 이하 | 표 / 그림 오른쪽 흐림과 밀기 안내 |
| 640px 이하 | 장 제목 26px, 툴바 고정 해제, 분할 버튼 2×2, 카드 1열, 들여쓴 상자 왼쪽 정렬 |

## 인쇄

- 툴바·레일·분할 버튼·밀기 안내 숨김, 레이아웃 1열, 모든 탭과 `details` 펼침.
- 어두운 바탕(첫 화면, 프롬프트 상자, 체크리스트, 흐름 상자, 해결표 첫 열, PS 배지, 창 막대)은 모두 흰 바탕 + text 글자로. 인쇄 규칙이 더 구체적인 선택자에 밀리기 쉬우니 상자 종류마다 따로 둔다.
- 카드·예상 요약·그림은 `break-inside:avoid`.

## 품질 바닥 (지우지 않는다)

- 한국어: `word-break:keep-all`, `overflow-wrap:break-word`, 제목 `text-wrap:balance`, 본문 `text-wrap:pretty`. 단어 중간 줄바꿈은 결함이다.
- 코드 값(품번·날짜·`25/월`·하이픈 값)과 짧은 고유명사 묶음은 `.nw`(`white-space:nowrap`)로 감싼다. 스크립트가 textContent로 넣는 값처럼 span을 쓸 수 없으면 화면 글자에서만 하이픈을 U+2011(줄바꿈 없는 하이픈)로 바꾸고 슬래시 뒤에 U+2060을 넣는다. 복사 대상(`pre`, 복사 버튼이 가리키는 id)에는 넣지 않는다. 복사한 명령이 달라지기 때문이다.
- 휴대폰 360~390px에서 페이지 가로 넘침 없음. 넘치는 표·그림·폴더 구조는 상자 안에서만 밀린다.
- 그림 글자는 실제 표시 크기 13px 이상(1280px 화면 기준).
- 키보드 포커스 `:focus-visible{outline:3px solid currentColor}`, `prefers-reduced-motion`에서 전환·애니메이션 끔, 본문 대비 4.5:1 이상.
- 복사 버튼마다 `aria-label`에 단계 번호와 대상을 적는다. 시각 숨김 텍스트는 `.vh`.

## 금지 패턴

- 장마다 반복되는 등장 애니메이션, 모든 카드에 같은 hover 효과
- 대문자 라벨, 가운뎃점으로 이은 메타 문자열(「A · B · C」), 버튼 끝 「→」
- 의미색을 위치·판정·장식에 재사용
- 크림 바탕+테라코타, 검정+형광 녹색, 모든 장이 같은 카드 모양

## 디자인 브리프

교안마다 `02_design_brief.md`에 이것만 적는다.

- 주제와 청중, 화면을 띄우고 강의하는지, 참가자가 프롬프트를 복사하는지
- 비교 대상(최대 4개)과 각각에 줄 의미색, 그 뜻
- 첫 화면 데모 장면 하나: 비교 대상의 차이를 직접 조작해 보는 장면
- 장별 표현 형식(그림·표·흐름도·카드·실습 단계)과 방식 장 색 테마(`m-*`) 배정
- 이 문서에서 벗어나는 점이 있으면 그 이유와 사용자 요청 근거
