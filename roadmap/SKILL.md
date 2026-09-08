---
name: roadmap
description: 기존 코드베이스의 현재 구현 상태를 확인하고 docs/PRD.md와 비교해, 아직 충족되지 않은 Functional Requirements를 구현하기 위한 마일스톤 로드맵을 작성합니다. PRD 대비 구현 갭을 파악하고 남은 작업을 여러 마일스톤과 버티컬 슬라이스로 나누고 싶을 때 사용합니다.
---

# Overview

이 스킬은 기존 코드베이스의 현재 구현 상태를 확인하고 `docs/PRD.md`와 비교해, PRD의 Functional Requirements 중 아직 충족되지 않은 항목을 구현하기 위한 단계별 로드맵을 작성한다.

로드맵의 핵심 목적은 이미 구현된 범위를 중복 계획하지 않고, 남은 요구사항을 사용자 가치 흐름 기준의 버티컬 슬라이스로 나누는 것이다.

최종 산출물은 `docs/ROADMAP.md`다. 문서는 한국어로 작성한다. 필요한 경우 섹션 제목은 영어를 사용할 수 있지만, 본문 설명은 한국어로 작성한다.

# Inputs

반드시 다음 파일을 읽는다.

1. `docs/PRD.md`

선택적으로, 있으면 읽는다.

1. `docs/userflow.md`
2. `docs/idea.md`

`docs/PRD.md`가 없거나 비어 있으면 로드맵을 작성하지 말고, 먼저 PRD가 필요하다고 보고한다.

기존 코드베이스를 반드시 확인한다. 프로젝트 구조에 맞게 다음 항목을 조사한다.

- 패키지와 기술 스택: `package.json`, lockfile, 설정 파일
- 앱 구조: 라우트, 페이지, 레이아웃, 컴포넌트, 상태 관리
- 데이터와 서버 로직: API route, server action, backend module, database schema, migration, Supabase 설정
- 테스트와 품질 장치: test files, lint/typecheck 설정, CI 설정
- 문서화된 현재 구현 상태가 있으면 관련 문서

# Output

`docs/ROADMAP.md`를 작성한다.

로드맵에는 반드시 다음 내용을 포함한다.

1. 현재 구현 상태 요약
2. PRD Functional Requirements별 충족 여부
3. 미충족 또는 부분 충족 Functional Requirements 목록
4. 확인된 기술 스택
5. 마일스톤 목록
6. 각 마일스톤의 목표
7. 각 마일스톤이 충족하는 Functional Requirements
8. 각 마일스톤의 범위와 제외 범위
9. 각 마일스톤의 완료 기준
10. 마일스톤 간 의존성

이 스킬은 태스크 파일을 만들지 않는다. 각 마일스톤은 이후 별도의 계획/태스크 분리 스킬에서 태스크 덩어리로 쪼갤 수 있을 만큼 명확하게 정의한다.

# Tech Stack Rules

기술 스택은 기존 코드베이스와 프로젝트 문서에서 확인된 내용만 기록한다.

사용자가 명시적으로 기술 스택 변경을 요구하지 않았다면 새로운 프레임워크, UI 라이브러리, 백엔드, 데이터베이스를 임의로 추가하지 않는다.

코드베이스에서 기술 스택이 명확히 확인되지 않으면 기본값을 가정하지 말고, `Notes`에 확인이 필요한 사항으로 적는다.

# Milestone Rules

모든 마일스톤은 PRD와 현재 코드베이스의 차이를 바탕으로 정의한다. 이미 충족된 Functional Requirement를 다시 구현 대상으로 잡지 않는다.

마일스톤은 가능한 한 버티컬 슬라이스로 정의한다. 각 마일스톤은 사용자가 실제로 완료할 수 있는 하나의 가치 흐름을 끝까지 포함해야 한다.

좋은 버티컬 슬라이스:

- 하나의 사용자 목표를 end-to-end로 완성한다.
- 필요한 UI, 상태, 데이터, API/백엔드, 검증, 테스트 범위를 함께 포함한다.
- 완료되면 독립적으로 데모하거나 검증할 수 있다.
- PRD의 Functional Requirements 일부를 명확히 충족한다.
- 다른 마일스톤에 비해 의존성이 낮거나, 의존성이 있으면 명확히 적는다.

나쁜 슬라이스:

- “DB 전체 만들기”, “API 전체 만들기”, “UI 전체 만들기”처럼 레이어별로만 나눈다.
- 사용자가 체감할 수 있는 완성 흐름 없이 내부 구조만 만든다.
- 여러 사용자 목표를 한 마일스톤에 과하게 묶는다.
- 완료 기준이 “구현 완료”, “잘 동작”처럼 검증 불가능하다.
- 특정 파일이나 코드 작업 목록 수준으로 너무 잘게 쪼개져 있다.

기존 코드베이스의 구조와 패턴을 우선한다. 필요한 경우 UI, 상태, 데이터, API/백엔드, 검증, 테스트 범위를 한 마일스톤 안에 함께 포함한다.

# Process

1. `docs/PRD.md`에서 Functional Requirements, User Scenarios, Success Criteria, Edge Cases, Assumptions를 파악한다.
2. 기존 코드베이스의 구조, 기술 스택, 주요 구현 흐름을 조사한다.
3. 각 Functional Requirement별로 현재 구현 여부를 판단한다.
4. Functional Requirement 상태를 `충족됨`, `부분 충족`, `미충족`, `확인 필요` 중 하나로 분류한다.
5. 이미 충족된 Functional Requirement는 로드맵 구현 범위에서 제외한다.
6. 부분 충족 또는 미충족 Functional Requirement를 사용자 가치 흐름 기준으로 묶어 마일스톤을 정의한다.
7. 각 마일스톤마다 포함 범위, 제외 범위, 완료 기준, 관련 Functional Requirements, 의존성을 적는다.
8. 어떤 Functional Requirement가 현재 어떤 상태이며 어느 마일스톤에서 충족되는지 추적 가능한 표를 작성한다.
9. `docs/ROADMAP.md`에 최종 로드맵을 작성한다.

# Roadmap Structure

`docs/ROADMAP.md`는 아래 구조를 따른다.

```markdown
# Roadmap

## Tech Stack

## Current Implementation Snapshot

## Requirement Gap Analysis

## Milestone Overview

## Milestone 1 - [Implementation Slice Name]

### Goal
### User Value
### Scope
### Out of Scope
### Functional Requirements Covered
### Completion Criteria
### Dependencies

## Milestone 2 - [Implementation Slice Name]

...

## Requirement Coverage

## Notes
```

마일스톤 수는 PRD와 현재 구현 갭의 크기에 맞게 정한다.

# Writing Rules

- 로드맵 본문은 한국어로 작성한다.
- 로드맵은 태스크 목록이 아니라 마일스톤 수준의 구현 전략이다.
- 각 마일스톤은 나중에 태스크로 쪼갤 수 있을 만큼 충분히 구체적이어야 한다.
- 프론트엔드만 따로, 백엔드만 따로, DB만 따로 나누지 않는다. 사용자 가치가 완결되는 버티컬 슬라이스로 나눈다.
- 미충족 또는 부분 충족 Functional Requirements는 최소 하나의 마일스톤에 매핑되어야 한다.
- 이미 충족된 Functional Requirements는 구현 대상 마일스톤에 포함하지 않는다.
- 한 마일스톤이 너무 커지면 사용자 가치 기준으로 더 작게 나눈다.
- 한 마일스톤이 너무 작아 독립 검증이 어렵다면 인접 흐름과 합친다.
- 구현 세부 파일 목록이나 세부 태스크는 쓰지 않는다. 그것은 다음 단계의 planning/task 스킬에서 다룬다.
- PRD와 현재 코드베이스에 근거가 없는 기능을 임의로 추가하지 않는다. 필요한 추론은 `Notes`에 가정으로 분리한다.
- 코드베이스 조사만으로 구현 여부를 확정하기 어려운 Functional Requirement는 `확인 필요`로 표시하고, 무리하게 충족 또는 미충족으로 단정하지 않는다.

# Final Response

작업을 마치면 작성한 파일을 커밋한 다음 `docs/ROADMAP.md`를 작성했다고 간단히 보고하고, 아래 내용을 이어서 간단히 보고한다.

- 확인한 현재 구현 범위
- 미충족 또는 부분 충족 Functional Requirements 수
- 마일스톤 개수와 구성 요약
