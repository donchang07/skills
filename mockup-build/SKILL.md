---
name: mockup-build
description: docs/mockups/plan.md와 docs/mockups/screens.md에 정의된 특정 화면 하나를 선택해 프론트엔드 목업으로 구현하고, 관련 화면 흐름 연결, 검증, 완료 마킹, 커밋까지 수행합니다. 사용자가 mockup-plan 이후 특정 Screen ID 또는 화면명을 만들라고 하거나, 화면 단위로 목업을 구현/수정/완료하려고 할 때 사용합니다. UI 구현 단계에서는 frontend-ui-engineering 스킬을 함께 사용해야 합니다.
---

# 개요

이 스킬은 `mockup-plan`으로 설계된 화면 중 하나를 선택해 프론트엔드 목업으로 구현한다.

목표는 화면 하나를 완결성 있게 만들고, `docs/mockups/plan.md`에 정의된 다른 화면과의 흐름도 끊기지 않게 연결한 뒤, 검증과 커밋까지 끝내는 것이다.

# 요구사항 요약

- 사용자는 이번에 작업할 screen을 반드시 지정해야 한다.
- screen이 지정되지 않았으면 `docs/mockups/plan.md`에서 미완료 screen 목록을 보여주고 선택을 요청한다.
- `docs/mockups/plan.md`와 `docs/mockups/screens.md`가 반드시 있어야 한다.
- 선택한 screen의 상세 설계는 `docs/mockups/screens.md`에서 읽는다.
- UI 구현에는 반드시 `frontend-ui-engineering` 스킬을 함께 사용한다.
- 선택한 screen은 독립적으로 리뷰 가능한 수준으로 완성한다.
- `plan.md`에 정의된 screen 간 관계가 있으면 해당 흐름도 연결한다.
- 완료 후 검증하고, 해당 screen을 완료 마킹한 뒤 커밋한다.

# 입력

사용자는 screen을 명시해야 한다.

허용 예시:

- `/mockup-build S001`
- `/mockup-build 홈 화면`
- `S003 결과 화면 만들어줘`
- `mockup-plan의 Onboarding screen 구현해줘`

screen이 명시되지 않았으면 구현하지 않는다. 대신 `docs/mockups/plan.md`를 읽고 완료되지 않은 screen 목록을 보여준 뒤, 어떤 screen을 만들지 물어본다. 질문과 함께 이번 단계에서 만들면 좋을 screen을 가장 먼저 추천한다.

미완료 screen 인식 기준:

```markdown
## [ ] Screen S001 - 화면 이름
```

완료 screen 인식 기준:

```markdown
## [x] Screen S001 - 화면 이름
## [X] Screen S001 - 화면 이름
```

# 필수 파일

작업 전에 반드시 다음 파일이 있는지 확인하고 읽는다.

1. `docs/mockups/plan.md`
2. `docs/mockups/screens.md`

둘 중 하나가 없거나 비어 있으면 구현하지 말고, 먼저 `mockup-plan`을 실행해야 한다고 보고한다.

UI 구현 단계에 들어가기 전에는 `frontend-ui-engineering` 스킬을 함께 사용한다고 알리고, 해당 스킬 지침을 적용한다.

필요하면 다음 문서도 읽는다.

1. `docs/DESIGN.md`
2. `docs/PRD.md`
3. `docs/userflows.md`
4. `docs/idea.md`

# 실행 전 점검

1. `git status --short`를 확인한다.
2. 기존 변경사항이 있으면 이번 작업과 관련 있는지 구분한다.
3. unrelated local change는 건드리거나 커밋하지 않는다.
4. 사용자가 지정한 screen이 `plan.md`와 `screens.md`에 모두 존재하는지 확인한다.
5. 지정한 screen이 이미 `[x]`이면 다시 작업할지 사용자에게 확인한다.

# 작업 절차

## 1. Screen 선택

사용자가 screen을 지정했으면 다음 기준으로 매칭한다.

- Screen ID: `S001`, `S002` 등
- Screen 이름
- 화면 목적이나 별칭이 명확히 일치하는 경우

매칭이 애매하면 후보를 2-5개로 좁혀 사용자에게 선택을 요청한다.

## 2. Screen 상세 이해

`docs/mockups/screens.md`에서 선택한 screen 섹션을 읽고 다음을 추출한다.

- Purpose
- Entry Points
- Exit Points
- Primary User Action
- Secondary Actions
- Layout ASCII
- Key UI Regions
- Content / Copy Notes
- Data / Placeholder Needs
- States
- Responsive Notes
- Review Questions
- Acceptance Criteria

`docs/mockups/plan.md`에서는 다음을 확인한다.

- Screen Flow
- Screen Relationship Map
- 선택 screen의 Leads To
- 선택 screen의 Review Focus
- 선택 screen의 Done When

## 3. 관련 코드 읽기

코드를 쓰기 전에 기존 프론트엔드 구조를 읽는다.

- 라우팅 방식
- 페이지/컴포넌트 위치
- 기존 UI 컴포넌트
- 디자인 토큰
- 더미 데이터 패턴
- 테스트/빌드 명령

새 구조를 임의로 만들지 말고 기존 프로젝트 패턴을 우선한다.

## 4. 구현

`frontend-ui-engineering` 스킬 기준을 적용해 선택 screen을 구현한다.

구현 원칙:

- 화면 하나가 독립적으로 렌더링되고 리뷰 가능해야 한다.
- 실제 백엔드, DB, 인증, 외부 API를 붙이지 않는다.
- 필요한 데이터는 더미 데이터 또는 로컬 상태로 처리한다.
- `screens.md`에 정의된 기본/빈/로딩/오류/선택 상태를 가능한 범위에서 표현한다.
- 실제 서비스 문맥에 맞는 한국어 문구를 사용한다.
- 기존 디자인 토큰과 컴포넌트를 먼저 재사용한다.
- 반응형 기준을 지킨다.

## 5. Screen 간 연결

`docs/mockups/plan.md`에 선택 screen과 다른 screen의 관계가 있으면 흐름을 연결한다.

연결 원칙:

- 이미 구현된 관련 screen이 있으면 실제 라우트나 UI 흐름으로 연결한다.
- 아직 구현되지 않은 screen으로 이어지는 경우에도 CTA, 링크, 버튼, disabled/placeholder 상태 등으로 다음 흐름이 이해되게 만든다.
- 선택 screen 구현을 위해 관련 screen 전체를 과도하게 구현하지 않는다.
- 연결을 위해 작은 route placeholder가 꼭 필요하면 최소 범위로 만들고, 커밋 메시지와 완료 요약에 명시한다.

## 6. 검증

가능한 가장 강한 검증을 실행한다.

우선순위:

1. 해당 화면 테스트 또는 컴포넌트 렌더링 테스트
2. 전체 테스트
3. 타입 체크
4. lint
5. build
6. 수동 검증

검증 실패 시 원인을 고치고 다시 검증한다. 실패 상태로 완료 마킹하거나 커밋하지 않는다.

수동 검증에는 최소한 다음을 포함한다.

- 화면이 콘솔 에러 없이 렌더링된다.
- 주요 CTA와 이동 흐름이 동작하거나 의도된 placeholder로 표현된다.
- 320px, 768px, 1024px, 1440px 기준에서 레이아웃이 크게 깨지지 않는다.
- `screens.md`의 Acceptance Criteria를 충족한다.

## 7. 완료 마킹

검증이 통과하면 `docs/mockups/plan.md`에서 해당 screen 제목의 `[ ]`를 `[x]`로 바꾼다.

예:

```markdown
## [x] Screen S001 - 홈 화면
```

사용자 확인이나 UX 결정이 남아 있어 완료라고 보기 어렵다면 `[x]`로 바꾸지 말고 중단 사유를 보고한다.

## 8. Commit

검증과 완료 마킹 후 커밋한다.

커밋 원칙:

- 한 screen = 한 커밋을 기본으로 한다.
- `git add -A`를 쓰지 않는다.
- 이번 screen 구현에 필요한 파일과 `docs/mockups/plan.md` 완료 마킹만 stage한다.
- unrelated local change는 포함하지 않는다.

권장 커밋 메시지:

```text
feat(mockup): build S001 home screen
```

수정이나 polish 중심이면 `fix`, `chore`, `docs` 중 맞는 타입을 사용한다.

# 중단 조건

다음 상황에서는 구현을 멈추고 사용자에게 보고한다.

- `docs/mockups/plan.md` 또는 `docs/mockups/screens.md`가 없음
- 사용자가 screen을 지정하지 않았고 선택이 필요함
- 지정 screen을 찾을 수 없음
- 지정 screen이 이미 완료되어 재작업 확인이 필요함
- screen 상세 설계가 모순되거나 구현에 필요한 결정이 빠짐
- unrelated local change와 충돌해 안전하게 커밋할 수 없음
- 실제 백엔드/API/DB/인증 구현이 필요해지는 경우
- 테스트나 빌드 실패를 합리적으로 해결할 수 없음

# 최종 응답

작업을 마치면 다음을 간단히 보고한다.

- 구현한 screen ID와 이름
- 주요 변경 파일
- 실행한 검증 명령
- 생성한 커밋 SHA
- 완료 마킹 여부
- 남은 리뷰 포인트가 있다면 그 내용
