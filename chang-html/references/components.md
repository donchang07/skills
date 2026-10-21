# 부품 목록

모든 부품의 정본 코드는 `assets/template.html` 안의 `<!-- COMPONENT: 이름 -->` 주석 아래에 있다. 새 교안은 템플릿을 복사해 `{{자리표시}}`를 채우고, 필요한 부품만 복제해 쓴다. 쓰지 않는 예시 부품은 지운다. 검사기는 남은 `{{...}}`를 실패로 본다.

| 부품 | 쓰는 곳 | 규칙 |
|---|---|---|
| toolbar | 맨 위 고정 | `id="file-label"`과 `body data-file`에 `{파일 이름} {버전}`. 다운로드 이름은 data-file에서 만든다 |
| cover | 표지 | 과정 이름·제목·부제·강사 표기. 날짜는 툴바에만 |
| toc | 오늘의 순서 | Part 카드는 `href="#part-N"`으로 연결 |
| part-divider | Part 시작 | `id="part-N"`. 설명 한 줄 |
| section | 내용 단위 | `.sec-head > .sec-badge + .sec-title (+ .sec-sub)`. 배지 번호는 `scripts/renumber.py`로 관리 |
| goal | 섹션 첫 상자 | `sem-warn` + 「이 장의 목표」 |
| table | 비교·설정·요금 | `table.brand`. 강조 셀만 `td.hl` |
| semantic-boxes | 결론·권고·확인·중단 | `sem-key / sem-good / sem-warn / sem-risk` + 라벨 |
| flow | 순서가 있는 절차 | 번호 + 직각 상자 + 화살표. 4단계 이하 권장 |
| copy-prompt | 참가자가 붙여 넣을 지시문 | `<pre id="p-{섹션}-{n}" class="prompt">` + `copyPrompt('같은 id')`. 끝에 「완료 조건」 번호 목록 |
| code | 명령·설정 파일 | `<pre id="c-{섹션}-{n}" class="code">`. 주석으로 설명, 비밀값 금지 |
| diagram | 아키텍처·위치 관계 | 인라인 SVG. marker id는 섹션마다 다르게(`arr-01`) |
| tabs | 실습 Lab 묶음 | `switchTab('tabN')` + `id="btn-tabN"`. 한 문서에 탭 묶음이 둘이면 id 접두어를 달리 |
| screenshot | 실제 화면 | base64 `data:` URI, `figcaption` 필수 |
| narrative + source | 섹션 끝 | brand-structure.md 규칙 |
| troubleshooting | 현장 대응 | 증상·원인·조치 3열 |
| checklist | 마무리 | 번호 카드 + 마무리 narrative |
| sources | 마지막 | 실제로 연 페이지만. 「무엇을 뒷받침하는지」 함께 |

## id 규칙

- 프롬프트 `p-{섹션번호}-{순번}`, 코드 `c-{섹션번호}-{순번}`, 탭 `tab{n}`·`btn-tab{n}`, SVG marker `arr-{섹션번호}-{색}`.
- 섹션 번호가 바뀌어도 id는 바꾸지 않아도 된다. 중복만 없으면 된다(검사기가 확인).

## 이전 형식 교안

claude-remote-control v2.0 이하 교안은 Tailwind 색과 둥근 상자를 쓰는 이전 형식이다. 이전 형식 교안을 고칠 때는 사용자가 브랜드 전환을 요청하지 않는 한 그 형식을 유지한다. 새 교안은 이 템플릿으로 만든다.
