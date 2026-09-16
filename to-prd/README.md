# to-prd

bkit(PDCA)가 `/pdca plan`부터 바로 소비할 수 있는 **실행 계약형 PRD**를 만드는 Claude Code 스킬입니다.

기획 문서 또는 브리프를 다음 구조로 변환합니다.

- 제품 전체의 단일 정본 `docs/PRD.md`
- bkit이 읽는 feature별 `docs/00-pm/{feature}.prd.md`
- 작성자 결정 목록
- 통합/feature별 착수 gate

일반 이해관계자용 PRD나 범용 제품 전략 문서를 만드는 스킬이 아닙니다.

## 설치

```bash
git clone https://github.com/donchang07/skills.git
cp -r skills/to-prd ~/.claude/skills/to-prd
```

Claude Code를 재시작하면 `/to-prd`로 호출할 수 있습니다.

## 언제 쓰나

- “bkit에 넣을 PRD 만들어줘”
- “기획 문서를 bkit PRD로 묶어줘”
- “PRD 업데이트하고 feature 파일도 동기화해줘”
- “이 기능을 PRD에 추가하고 /pdca plan 준비해줘”
- bkit 프로젝트에서 PRD 없이 바로 구현 또는 `/pdca plan`을 시작하려 할 때

## 입력

있는 파일만 읽습니다. 파일이 부족해도 브리프나 현재 대화로 시작할 수 있습니다.

| 파일 | 정보 |
|---|---|
| `docs/idea.md` | 문제·타깃·핵심 기능 |
| `docs/benchmark.md` | 경쟁 맥락·차별화·외부 사실 |
| `docs/userflow.md` | 사용자 흐름·화면 |
| `docs/brandvoice.md` | 서비스 이름·보이스 |
| `docs/DESIGN.md` | 시각 시스템 |
| `docs/PRD.md` | 기존 정본·ID·결정·개정 이력 |
| 브리프·현재 대화·코드 | 최신 결정과 실제 시스템 제약 |

## 산출물과 단일 정본

`docs/PRD.md`가 유일한 정본입니다.

```text
docs/PRD.md                         제품 통합 정본
    │
    ├─ docs/00-pm/{feature}.prd.md  bkit feature projection
    ├─ docs/00-pm/_decisions.md     미결 결정 projection
    ├─ docs/00-pm/_product.gate.md  제품 gate
    └─ docs/00-pm/{feature}.gate.md feature gate
```

feature PRD를 직접 수정하지 않습니다. 업데이트는 정본을 먼저 바꾸고 영향받는 파생본을 다시 만듭니다. 파생본에만 존재하는 사람의 편집은 덮어쓰기 전에 정본으로 옮깁니다.

## Blocker가 있을 때

기존 최종본을 덮어쓰지 않습니다.

| 대상 | draft 경로 |
|---|---|
| 제품 정본 | `docs/PRD.draft.md` |
| feature PRD | `docs/00-pm/{feature}.prd.draft.md` |
| 제품 gate | `docs/00-pm/_product.gate.draft.md` |
| feature gate | `docs/00-pm/{feature}.gate.draft.md` |

Blocker가 해소된 뒤 최종본을 생성해도 draft를 자동 삭제하지 않고 `superseded` 상태와 대체 파일을 기록합니다.

## bkit 흐름

```text
기획 산출물·브리프
        ↓
to-prd
        ├─ docs/PRD.md
        ├─ docs/00-pm/{feature}.prd.md
        └─ gate + decisions
        ↓
/pdca plan {feature}
→ /pdca design {feature}
→ /pdca do {feature}
→ /pdca analyze {feature}
→ 기준 미달 시 autoIterate 자동 반복
→ /pdca report {feature}
```

이 스킬이 PRD를 새로 만들었다면 bkit `/pdca pm`을 건너뜁니다. 기존 `/pdca pm` 산출물이 있다면 입력으로 병합합니다.

## PRD 계약

```text
0.  Executive Summary + Context Anchor
1.  개요
2.  배경 & 근거
3.  목표 + 비목표
4.  User Scenarios
5.  Functional Requirements + NFR
6.  Success Criteria
7.  Edge Cases
8.  Page UI Checklist + 화면 4상태
9.  브랜드 & 디자인
10. 범위 / 비범위 / 우선순위 / 납기
11. 레벨·스택 + 시스템 가정 10칸
12. 구현자 오픈 이슈
13. 작성자 결정 요청
14. feature 분해표
15. bkit 실행 명세
부록 A. 데이터 계약
부록 B. 외부 사실 확인
```

FR은 시나리오·화면·SC·데이터·feature와 연결됩니다. 이 연결이 끊기면 gate가 결함으로 판정합니다.

## 시스템 가정

10개 행을 무조건 두되, 제품에 맞는 상태를 사용합니다.

| 상태 | 의미 |
|---|---|
| `[확정]` | 사용자나 기존 문서가 결정 |
| `[기본값]` | 안전한 권장값으로 진행 |
| `[해당 없음]` | 적용되지 않는 이유가 있음 |
| `[결정 필요]` | 범위·아키텍처·비용·보안이 달라짐 |

모든 `[결정 필요]`가 Blocker는 아닙니다. P0 설계를 바꾸고 안전한 fallback이 없는 결정만 Blocker입니다.

## 착수 gate

먼저 Hard Gate를 확인하고, 그다음 보조 점수를 계산합니다.

- 착수 가능: Blocker 0, 90점 이상
- 조건부 착수: Blocker 0, 70~89점
- 착수 불가: Blocker 1 이상 또는 70점 미만

점수는 Blocker를 상쇄할 수 없습니다.

기계 검사는 다음처럼 실행합니다.

```bash
node scripts/validate_prd.mjs docs/PRD.md docs/00-pm/example.prd.md
```

검사 항목:

- 필수 장
- FR/SC 정의와 중복
- feature 분해표의 FR 누락
- unresolved placeholder
- 계약 섹션의 미결 표현
- 시스템 가정 10개와 상태 라벨
- 화면 4상태
- bkit gate 설정

## bkit 검증 기준

변동 가능한 bkit 사양은 `references/bkit-contract.md`에서만 관리합니다.

2026-09-16 확인 기준:

- 공식 저장소: [ww-w-ai/bkit-claude-code](https://github.com/ww-w-ai/bkit-claude-code)
- 최신 maintenance release: v2.1.38
- PM 문서 탐색: `docs/00-pm/features/{feature}.prd.md`, `docs/00-pm/{feature}.prd.md`
- 기본 `matchRateThreshold`: 90
- 기본 `maxIterations`: 5
- `autoIterate`: true

프로젝트의 로컬 `bkit.config.json`이 항상 이 reference보다 우선합니다.

## 스킬 파일

```text
to-prd/
├── SKILL.md
├── README.md
├── assets/
│   └── prd-template.md
├── references/
│   ├── bkit-contract.md
│   └── gate-checklist.md
└── scripts/
    └── validate_prd.mjs
```

## 기존 버전과의 차이

| 기존 | 현재 |
|---|---|
| 범용 Vibe UX PRD | bkit 전용 실행 계약 |
| `docs/PRD.md` 하나 | 정본 + feature projection + decisions + gate |
| 기획 문서 4개 중심 | 일부 문서 또는 브리프도 가능 |
| roadmap에 구현 분해 위임 | feature를 bkit PDCA 단위로 분해 |
| 단순 화면 표 | 요소 체크리스트 + 로딩·빈·오류·성공 |
| 서술형 Edge Cases | 문구·동작·로그 계약 |
| 정성 검토 | Hard Gate + 점수 + Node 검사 |
| 미결 항목 한 종류 | 구현자 이슈와 작성자 결정 분리 |
| 경로·명령이 본문에 섞임 | versioned bkit contract reference로 분리 |

## 원칙

- bkit 전용 범위를 유지합니다.
- 정본은 하나이며 파생본은 정본에서 재생성합니다.
- FR/SC ID와 개정 이력을 보존합니다.
- 기본값·추정·가설·출처를 구분합니다.
- 데이터 없는 P0 FR과 측정할 수 없는 SC를 통과시키지 않습니다.
- 일반 단어를 금지어로 검색하지 않고 실제 미결 의미를 검사합니다.
- Hard Gate가 점수보다 우선합니다.
