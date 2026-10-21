# 작업 규모에 맞춘 협업

신규 제작, 큰 수정, 강사용 제작, 부분 재실행 때 읽는다. Claude Code에서는 `/chang-html`로 호출한다. 현재 환경에 있는 위임 도구만 쓰고, 없으면 순차로 실행하되 병렬로 했다고 보고하지 않는다.

## 모드

| target_mode | 예 | 실행 방식 |
|---|---|---|
| 작은 수정 | 문구 몇 개, 표 한 칸, 버튼 이름 | 팀 없음. 메인이 고치고 버전 +0.1, `validate.py`만 실행 |
| edit_html | 섹션 추가·이동·재구성, 내용 보강 | researcher(새 사실이 있을 때) → builder → qa |
| new_html | 새 교안 | 아래 전체 흐름 |
| instructor | 강사용 만들기·갱신 | instructor → (make_instructor.py) → qa |
| skill_update | 이 스킬 자체 개선 | 팀 없음. 지침·참조·도구·플러그인 사본의 영향 범위를 대조해 고치고 빌드 스크립트 `--check` |

판단이 애매하면 작은 수정으로 시작하고, 3개 섹션 이상의 구조 변경이 되면 팀 흐름으로 바꾼다.

## Claude Code 팀

**실행 모드:** 서브에이전트 위임 + 생성·검증. 단계 결과를 파일로 넘긴다.

| 에이전트 | 모델 | 맡는 일 | 쓰기 범위 |
|---|---|---|---|
| `chang-html-researcher` | sonnet | 주장별 근거·공식 문서 확인·기준일 | `{RUN}/01_*` |
| `chang-html-designer` | opus | 청중·목표, Part·섹션 구성, 섹션별 명세(목표·부품·narrative·출처), 실습 흐름과 과제 이름 | `{RUN}/02_*` |
| `chang-html-builder` | opus | 템플릿으로 HTML 조립·수정, 버전 관리, 번호 재정렬 | 결과 HTML, `{RUN}/03_builder_*` |
| `chang-html-instructor` | sonnet | 강사 운영 가이드·장별 노트 JSON | `{RUN}/03_instructor_*` |
| `chang-html-qa` | sonnet | 정적 검사·렌더링·명세와 사실 대조, 판정만 | `{RUN}/04_*`, `{RUN}/renders_v{N}/` |

플러그인으로 설치하면 이름 앞에 `chang-html:`이 붙는다. 사용 가능한 이름을 확인해 호출하고, 하나도 없으면 같은 역할 정의를 기본 서브에이전트에 넘겨 실행한 사실을 기록한다. 메인이 계약·통합·최종 판정과 사용자 보고를 맡는다. 같은 HTML을 두 에이전트가 동시에 쓰지 않는다. QA는 제품을 고치지 않는다.

## 작업 폴더

- `{RUN}` = 대상 프로젝트의 `_workspace/chang-html/{YYYYMMDD}_{주제}/`. 스킬 설치 폴더를 작업 폴더로 쓰지 않는다.
- `{RUN}/00_packet.md`를 먼저 쓴다: target_mode, 청중·목적·시간, 과제 이름, 원본 경로(있으면)와 버전, 결과 파일 이름, 강사용 필요 여부, 확정된 사용자 결정, 완료 기준. 모든 에이전트에 이 경로를 넘긴다.

## 흐름 (new_html)

1. 준비(메인): `00_packet.md`. 청중·목적이 없으면 합리적 가정을 적고 진행한다.
2. 조사(researcher): `01_research.md` — 주장별 근거 표(주장 · 출처 URL · 확인일 · 상태: 확인/추정/미확인).
3. 설계(designer): `02_design.md` — Part·섹션 목록, 섹션별 {번호, 제목, 부제, 목표, 쓸 부품, 핵심 표·그림 내용, narrative 두 줄, 출처 키}, 실습 Lab 구성과 프롬프트별 완료 조건, 문제 해결표 초안.
4. 제작(builder): `assets/template.html`에서 시작해 `{주제} v1.0.html`. 사용한 부품과 id 목록을 `03_builder_log.md`에.
5. 검증(qa): `validate.py`, `render.mjs`, 명세·근거 대조 → `04_qa_report_v{N}.md`.
6. 수정 반복: 실패 항목을 화면 문제는 builder, 내용 문제는 designer→builder로 보낸다. 최대 2회. 남은 실패는 통과로 바꾸지 않고 보고한다.
7. 강사용(요청 시): instructor → make_instructor.py → qa.
8. 완료(메인): 결과 파일, QA 보고서, `05_manifest.json`(결과 SHA-256, 기준 스킬 경로, 렌더 환경, 판정) → 사용자 보고.

## 부분 재실행

- 같은 교안의 `{RUN}`이 있으면 후속 요청으로 본다. 바뀐 섹션만 builder(화면) 또는 designer(내용)에 다시 맡기고 바뀐 섹션만 QA한다. 결과는 새 버전 파일로 남긴다.
- 섹션 추가·이동·삭제 뒤에는 `renumber.py`를 실행하고 본문 상호 참조(「01의 ~」)를 직접 고친다.

## 오류 처리

- 일시적 도구 오류는 원인을 확인하고 1회 재시도한다. 사용량 한도·권한 거부는 재시도하지 않고 남은 산출물을 보고한다.
- 렌더링을 못 했으면 정적 검사만으로 통과 처리하지 않고 `not_run`으로 보고한다.
