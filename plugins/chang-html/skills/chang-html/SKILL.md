---
name: chang-html
description: "장동인 교수의 HTML 실습 교안(참가자용·강사용)을 새로 만들거나 고칩니다. 교안마다 디자인 브리프를 정하고(기본: 잉크·페이퍼 디자인, Pretendard·D2Coding), 메인이 쓴 내용 원고를 제작 담당이 원본 HTML로 옮기며, 읽기 전용 검수 담당이 독립 판정합니다. 복사 버튼 프롬프트(만드는 프롬프트·질문 스크립트·완료 조건), 근거·기준일, 강사 노트, 빌드·검사 도구, Drive 배포까지 다룹니다. 교안 수정·장 추가·디자인 개편·강사용 만들기와 이 스킬 자체 개선에도 사용합니다."
---

# Chang HTML 교안

## 작업 모드와 정본

- 새 교안 제작, 기존 교안 수정(장 추가·이동·보강), 디자인 개편, 강사용 만들기, 스킬 자체 개선을 이 스킬에서 처리한다. 교안 수정 요청으로 스킬 파일을 고치지 않는다.
- 이 폴더의 SKILL.md·references·assets·scripts가 한 묶음의 기준이다. 저장소 `chang-html/`이 정본이고 개인 설치본·플러그인은 배포 사본이다.
- 문구 몇 개 같은 작은 수정은 메인이 직접 고치고 검사 도구만 돌린다. 그 밖의 작업은 [협업 절차](references/orchestration.md)를 먼저 읽는다. 구조는 메인(원고·통합·배포), 제작 담당 `chang-html-builder`, 읽기 전용 검수 담당 `chang-html-reviewer` 셋이다.

## 적용 순서

1. 사용자의 명시적 요청과 사용자가 저장한 선호를 우선한다. 자료가 없으면 수치·출처를 만들지 않는다.
2. 문장·용어·금지 사항·사실성·버전: [style-guide.md](references/style-guide.md)
3. 디자인: 교안마다 `{RUN}/_workspace/02_design_brief.md`를 쓴다. 기본값은 [design-system.md](references/design-system.md)이고, 사용자가 chang-ppt 브랜드를 요청하면 [chang-ppt-brand.md](references/chang-ppt-brand.md)를 쓴다.
4. 화면 부품: [components.md](references/components.md), 시작 파일은 `assets/template.html`
5. 실습 프롬프트: [lab-prompts.md](references/lab-prompts.md)
6. 강사용: [instructor-mode.md](references/instructor-mode.md)
7. 검사와 검수: [tooling-qa.md](references/tooling-qa.md)
8. 배포: [deploy.md](references/deploy.md)

## 작업 흐름 요약

- 청중(대부분 CEO·임원), 목적, 실습 과제 이름, 실습 환경(로그인만인지, API 키가 있는지), 강사용 필요 여부, 배포 위치를 확인한다. 없으면 합리적 가정을 `00_packet.md`에 적고 진행한다. 강의 길이는 구성 판단에만 쓰고 화면에 적지 않는다.
- 메인이 내용 원고(`{RUN}/_workspace/05_content_*.md`)에 장 구성, 표 값, 프롬프트 전문(`(id: …)` 표기)을 쓴다. 제작 담당은 원고를 글자 그대로 옮기고, 검수 담당은 `compare_prompts.py`로 대조한다.
- 원본 한 개(`src_v{N}.html`, 표식 포함)와 강사 노트 JSON으로 `scripts/build.py`가 참가자용·강사용을 동시에 만든다.
- 결과는 `{주제} v{N}.html`과 `{주제} v{N} 강사용.html`. 고칠 때마다 0.1씩 올리고 이전 파일을 남긴다.
- 장을 추가·이동·삭제하면 `scripts/renumber.py`로 장 id·목차·노트 표식을 다시 매기고 본문 상호 참조를 고친다.
- 검수 담당이 PASS로 판정한 결과만 배포한다. 렌더링하지 못한 항목은 not_run으로 보고한다.

## 함께 쓰는 스킬

- 같은 교안으로 발표 슬라이드가 필요하면 chang-ppt를 쓴다. 교안의 장 구성과 핵심 메시지를 슬라이드 명세의 입력으로 넘기고, 발표자 노트와 강사 노트의 핵심 메시지를 맞춘다.
- 디자인 판단에는 frontend-design 원칙(대담함은 한 곳, 템플릿 티 나는 기본값 피하기)을 함께 적용한다.

## 최종 점검

- 금지: 학생·수강생·구멍·회차, 강의 시간·분량·진행 시간표 표기, 강사 3인칭. 과제 이름 통일.
- 모든 장은 `main > section#sNN`, 제목 뒤 `<!--NOTE:NN-->`(원본), 레일 목차 링크가 모두 이어짐.
- 모든 복사 버튼이 대상 id를 가리키고 id가 중복되지 않음. 탭 전환 작동. 프롬프트는 원고와 글자 단위로 같음.
- 한국어 줄바꿈(keep-all), 휴대폰 폭 가로 넘침 없음, 인쇄 시 밝은 바탕, 글꼴 로드 성공.
- 툴바·제목·footer·data-file의 버전이 같고 이전 버전 파일이 남아 있음.
- 강사용: 운영 가이드, 장별 노트, 버튼 3개 작동, 정답은 강사용에만.
