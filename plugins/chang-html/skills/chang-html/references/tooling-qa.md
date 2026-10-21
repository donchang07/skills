# 도구와 QA 절차

## 도구

| 도구 | 하는 일 | 실행 |
|---|---|---|
| `scripts/validate.py` | 태그 짝, 복사 버튼 id, 탭, 금지어, 섹션 번호, 남은 자리표시, 팔레트 밖 색 | `python scripts/validate.py <교안.html> [--baseline <이전 버전>] [--json <보고서>]` |
| `scripts/renumber.py` | 섹션 배지 번호 재정렬, 상호 참조 후보 출력 | `python scripts/renumber.py <입력> <새 버전 출력>` |
| `scripts/make_instructor.py` | 강사용 파일 생성 | `python scripts/make_instructor.py <참가자용> <notes.json>` |
| `scripts/render.mjs` | 브라우저 렌더링, 섹션별 PNG, 콘솔 오류, 탭·노트 버튼, 모바일 가로 넘침 | `node scripts/render.mjs <교안.html> <폴더>` (Playwright 필요, 경로가 다르면 `CHROMIUM_PATH`) |

- 이전 형식 교안은 원래부터 태그 불일치가 있을 수 있다. `--baseline`으로 이전 버전보다 늘지 않았는지만 본다.
- 파일 이름에 공백이 있으므로 경로를 따옴표로 감싼다.

## 결과 QA 점검표

1. `validate.py` 전 항목 PASS(colors는 경고만). 실패는 그대로 보고한다.
2. `render.mjs` 콘솔 오류 0건, 탭 전환·강사 노트 접기 true, 모바일 가로 넘침 없음.
3. 섹션 PNG를 한 장씩 열어 확인: 제목 가운데·네이비, 직각 상자, 표 머리 네이비, narrative 두 줄 가운데, 출처 줄 위치, 그림 화살표 방향과 라벨, 글자 겹침·잘림, 코드 줄바꿈.
4. 명세 대조: `02_design.md`의 섹션별 제목·목표·narrative·출처가 화면과 같은지, 명세에 없는 수치·출처가 들어갔는지.
5. 사실 대조: 본문의 제품 이름·명령·요금제·버전이 `01_research.md`에서 「확인」 상태인지. 「추정」은 본문에 추정이라고 적혔는지.
6. 문체: style-guide.md 금지어·호칭·과제 이름 통일·강사 3인칭 여부.
7. 버전: 툴바·제목·footer·data-file이 모두 같은 버전인지, 이전 버전 파일이 남아 있는지.

## 보고서

`{RUN}/04_qa_report_v{N}.md`: 렌더 환경(브라우저·글꼴), 실제로 연 섹션 목록, 표(섹션 | 판정 통과/실패/not_run | 문제 | 근거 | 수정 대상 builder/designer), 🔴 필수 / 🟡 권장 / 🟢 문제없음 요약. 열어 보지 않은 섹션은 not_run이다.
