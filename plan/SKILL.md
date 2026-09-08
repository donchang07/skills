---
name: plan
description: docs/PRD.md와 docs/ROADMAP.md를 읽고 특정 마일스톤의 구현 계획과 태스크 목록을 docs/milestones/M*/ 아래에 작성합니다.
---

# 개요

이 스킬은 `docs/PRD.md`와 `docs/ROADMAP.md`를 읽고, 로드맵에 정의된 특정 마일스톤을 실제 구현 직전 단계까지 구체화한다.

코드를 작성하지 않는다. 산출물은 마일스톤별 보존 문서인 `plan.md`와 `tasks.md`다.

# 입력

반드시 다음 파일을 읽는다.

1. `docs/PRD.md`
2. `docs/ROADMAP.md`

선택적으로, 마일스톤 이해에 필요하면 다음 파일도 읽는다.

1. `docs/DESIGN.md`
2. `docs/userflow.md`
3. `docs/idea.md`

사용자가 마일스톤 번호를 명시하면 해당 마일스톤을 대상으로 한다. 예: `M1`, `Milestone 2`, `두 번째 마일스톤`.

사용자가 마일스톤을 명시하지 않았으면 바로 작성하지 말고, 어떤 마일스톤을 계획할지 물어본다.

# 산출물

마일스톤 번호에 맞춰 아래 파일을 작성한다.

```text
docs/milestones/M<N>/plan.md
docs/milestones/M<N>/tasks.md
```

예시:

```text
docs/milestones/M1/plan.md
docs/milestones/M1/tasks.md
```

산출물은 임시 파일이 아니다. 마일스톤 구현 계약서와 체크리스트로 보존한다.

# 계획 원칙

## 1. 읽기 전용 계획 모드

계획을 세우기 전에는 코드를 작성하지 않는다.

먼저 PRD와 ROADMAP에서 다음을 파악한다.

- 해당 마일스톤의 목표
- 충족해야 하는 Functional Requirements
- 관련 User Scenarios와 Success Criteria
- 마일스톤 범위와 제외 범위
- 이전 마일스톤에 대한 의존성
- 리스크와 미정 사항

## 2. 의존성 그래프 우선

구현 순서를 정하기 전에 무엇이 무엇에 의존하는지 먼저 정리한다.

예시:

```text
디자인 토큰
  └─ 공통 UI 컴포넌트
      └─ 화면 레이아웃
          └─ 상태별 목업
              └─ 수동 검증 시나리오
```

실제 기능 마일스톤에서는 다음처럼 end-to-end 의존성을 고려한다.

```text
데이터 모델
  └─ 서버/DB 로직
      └─ 클라이언트 상태/호출
          └─ UI 흐름
              └─ 검증/테스트
```

## 3. 마일스톤 유형별 계획 방식

### M1: Frontend Mockup

`M1`은 프론트엔드 목업 품질을 높이는 마일스톤이다.

계획에는 다음을 우선 반영한다.

- `docs/DESIGN.md` 기반의 화면 구성
- 디자인 토큰 정리
- 재사용 가능한 UI 컴포넌트 후보
- 핵심 사용자 흐름을 보여주는 hi-fidelity working prototype
- 더미 데이터와 정적 상태
- 기본/빈/로딩/오류/선택/활성 상태
- 반응형 기준
- 수동 시각 검증 기준

M1의 태스크는 실제 Supabase 연동, 실제 인증, 실제 DB 저장, 운영 백엔드 구현을 포함하지 않는다.

### M2+

`M2`부터는 실제 기능 구현 마일스톤이다.

태스크는 horizontal layer가 아니라 vertical slice 기준으로 나눈다.

좋은 vertical slice:

- 하나의 사용자 목표를 끝까지 완성한다.
- 필요한 UI, 상태, 데이터, 서버/DB 로직, 검증을 함께 포함한다.
- 완료되면 독립적으로 데모하거나 테스트할 수 있다.
- PRD의 Functional Requirements 일부를 명확히 충족한다.

나쁜 분해:

- DB 전체 만들기
- API 전체 만들기
- UI 전체 만들기
- 테스트 전부 나중에 몰아서 작성하기
- 사용자가 체감할 수 없는 내부 구조 작업만 따로 떼기

# plan.md 작성 방식

`plan.md`는 해당 마일스톤을 어떻게 구현할지 설명하는 문서다.

아래 구조를 사용한다.

```markdown
# Plan: M<N> - [마일스톤 이름]

## Overview
[마일스톤 목표와 사용자 가치 요약]

## Source Context
- PRD: [관련 섹션/요구사항 요약]
- Roadmap: [해당 마일스톤 정의 요약]
- Additional Context: [필요 시 DESIGN/userflow/idea에서 확인한 내용]

## Scope
[이번 마일스톤에 포함되는 범위]

## Out of Scope
[이번 마일스톤에서 하지 않는 일]

## Functional Requirements Covered
[FR ID 또는 요구사항 문장과 충족 방식]

## Architecture / Implementation Approach
[구현 접근. 기술 선택, 데이터 흐름, UI 구조, 상태 처리 방향]

## Dependency Graph
[ASCII 다이어그램 또는 단계별 의존성]

## Verification Strategy
[테스트, 빌드, 수동 검증 기준]

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|

## Open Questions
[구현 전 확인이 필요한 질문. 없으면 "없음"]
```

계획은 구현자가 설계 결정을 다시 크게 하지 않아도 될 만큼 구체적이어야 한다. 하지만 세부 코드나 긴 코드 스니펫은 넣지 않는다.

# tasks.md 작성 방식

`tasks.md`는 실제 구현 직전에 사용할 실행 가능한 태스크 목록이다.

각 태스크는 한 번의 집중 세션에서 끝낼 수 있을 만큼 작아야 한다. 권장 크기는 1-5개 파일 변경이다. 5개 파일을 넘기거나 독립된 하위 목표가 섞이면 더 작은 태스크로 나눈다.

각 태스크는 반드시 다음 정보를 포함한다.

- 설명
- Acceptance Criteria
- Verification
- Dependencies
- Likely Files
- Estimated Scope

태스크 형식:

```markdown
## [ ] Task T001 - [짧은 제목]

**Description:** [이 태스크가 달성하는 것]

**Acceptance Criteria:**
- [ ] [구체적이고 테스트 가능한 완료 조건]
- [ ] [구체적이고 테스트 가능한 완료 조건]

**Verification:**
- [ ] [실행할 테스트/빌드/수동 확인]

**Dependencies:** [없음 또는 T000]

**Likely Files:**
- `path/to/file`

**Estimated Scope:** [XS/S/M/L]
```

크기 기준:

| Size | 기준 |
|------|------|
| XS | 단일 설정, 문서, 작은 함수 수준 |
| S | 1-2개 파일의 작은 변경 |
| M | 3-5개 파일의 하나의 완결 흐름 |
| L | 5개 초과 또는 여러 하위 목표 포함. 가능하면 분리 |

# 태스크 배열 원칙

1. 의존성 순서대로 배열한다.
2. 각 태스크 후에도 프로젝트가 가능한 한 동작 가능한 상태를 유지해야 한다.
3. 2-3개 태스크마다 Checkpoint를 둔다.
4. 리스크가 큰 태스크는 너무 뒤로 미루지 않는다.
5. 테스트나 검증 태스크를 마지막에 몰지 않는다.
6. M2+에서는 사용자 가치 흐름이 완성되는 vertical slice 단위로 묶는다.

Checkpoint 형식:

```markdown
## Checkpoint - [이름]

- [ ] 관련 태스크 완료
- [ ] 빌드 성공
- [ ] 핵심 흐름 검증 완료
- [ ] 다음 단계 진행 전 사용자 검토 가능 상태
```

# 검증 기준

작성이 끝나기 전에 다음을 확인한다.

- [ ] `plan.md`가 해당 마일스톤의 목표, 범위, 제외 범위, 의존성, 검증 전략을 포함한다.
- [ ] `tasks.md`의 모든 태스크가 Acceptance Criteria를 가진다.
- [ ] `tasks.md`의 모든 태스크가 Verification을 가진다.
- [ ] 태스크 의존성이 명확하다.
- [ ] 태스크가 너무 큰 경우 분리되어 있다.
- [ ] Checkpoint가 포함되어 있다.
- [ ] PRD의 관련 Functional Requirements가 누락되지 않았다.
- [ ] M1은 프론트엔드 목업 중심이고 실제 백엔드/DB 구현을 포함하지 않는다.
- [ ] M2+는 vertical slice 기준으로 나뉘어 있다.

# 최종 응답

작업을 마치면 두 파일을 커밋한 다음, 작성한 두 파일 경로를 보고하고, 태스크 개수와 주요 checkpoint를 간단히 요약한다.
