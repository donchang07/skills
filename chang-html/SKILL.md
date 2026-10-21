---
name: chang-html
description: "장동인 교수의 HTML 실습 교안(참가자용·강사용)을 chang-ppt 브랜드 색과 구조로 새로 만들거나 고칩니다. 공식 문서 근거·기준일, 복사 버튼 프롬프트와 완료 조건, 버전 관리, 강사 노트, 검증까지 조사·설계·제작·강사노트·QA 에이전트 팀으로 진행합니다. 교안 수정·섹션 추가·강사용 만들기와 이 스킬 자체 개선에도 사용합니다."
---

# Chang HTML 교안

## 통합 작업 모드와 정본

- 새 교안 제작, 기존 교안 수정(섹션 추가·이동·보강), 강사용 만들기, 스킬 자체 개선을 이 스킬에서 처리한다. 요청에 맞는 모드를 고르고 입력·결과 파일·수정 범위를 기록한다. 교안 수정 요청으로 스킬 파일을 고치지 않는다.
- 이 폴더의 SKILL.md·references·assets/template.html·scripts를 한 묶음의 기준으로 쓴다. 저장소 `chang-html/`이 정본이고 개인 설치본·플러그인은 배포 사본이다.
- 신규 제작·큰 수정·강사용·부분 재실행은 [협업 절차](references/orchestration.md)를 먼저 읽고 그 흐름을 따른다. Claude Code에서는 `chang-html-researcher`(근거), `chang-html-designer`(구성·명세), `chang-html-builder`(제작), `chang-html-instructor`(강사 노트), `chang-html-qa`(독립 검증)에 맡긴다. 문구 몇 개 같은 작은 수정은 팀 없이 직접 고치고 검사만 한다.

## 적용 순서

1. 사용자의 명시적 요청을 우선한다. 자료가 없으면 수치·출처를 만들지 않는다.
2. 문장·용어·사실성·버전은 [style-guide.md](references/style-guide.md)를 따른다.
3. 색과 화면 구조는 [brand-structure.md](references/brand-structure.md)를 따른다. 색은 chang-ppt `color-system.md`와 같고 새 색을 만들지 않는다.
4. 화면은 [components.md](references/components.md)의 부품을 `assets/template.html`에서 복제해 만든다.
5. 강사용은 [instructor-mode.md](references/instructor-mode.md)를 따른다.
6. 검증은 [tooling-qa.md](references/tooling-qa.md)의 점검표를 따른다.

## 작업 흐름 요약

- 청중(대부분 CEO·임원), 목적, 강의 시간, 실습 과제 이름, 실습 환경, 강사용 필요 여부를 확인한다. 없으면 합리적 가정을 적고 진행한다.
- 교안 전체를 하나의 질문과 결론으로 묶고 Part·섹션 순서를 정한다. 섹션마다 목표·핵심 표나 그림·실습·narrative 두 줄·출처를 명세한다.
- 구조가 있는 내용(실행 위치, 설정 파일 관계, 선택 기준)은 문장 대신 그림·표·단계 전개로 보여 준다. 참가자가 붙여 넣을 지시는 모두 복사 버튼과 완료 조건을 단다.
- 결과는 `{주제} v{버전}.html`. 고칠 때마다 0.1씩 올리고 이전 파일을 남긴다.
- 섹션을 추가·이동·삭제하면 `scripts/renumber.py`로 번호를 다시 매기고 본문 상호 참조를 고친다.
- `scripts/validate.py`와 `scripts/render.mjs`로 확인한 결과만 통과라고 보고한다. 렌더링하지 못한 부분은 not_run으로 보고한다.

## 함께 쓰는 스킬

- 같은 교안으로 발표 슬라이드가 필요하면 chang-ppt를 쓴다. 교안의 Part·섹션 구성과 narrative를 슬라이드 명세의 입력으로 넘기고, 발표자 노트와 강사 노트의 핵심 메시지·시간을 맞춘다.

## 최종 점검

- 금지어(참가자 영역): 학생·구멍·회차 0건. 과제 이름 통일. 강사 3인칭 없음.
- 모든 섹션: 가운데 제목, 직각 상자, narrative 두 줄, 출처 줄(근거가 있는 섹션).
- 모든 복사 버튼이 대상 id를 가리키고 id가 중복되지 않음. 탭 전환 작동.
- 툴바·제목·footer·다운로드 이름의 버전이 같음. 이전 버전 파일이 남아 있음.
- 강사용: 운영 가이드, 장별 노트, 버튼 3개 작동. 참가자용 파일은 바뀌지 않음.
