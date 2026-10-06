# to-prd

bkit(PDCA)가 `/pdca plan`부터 바로 소비할 수 있는 **화면 중심 실행 계약형 PRD**를 만드는 Claude Code·Codex 스킬입니다. 역할·화면·메뉴·로그인·UI 요소와 디자인 기준을 먼저 정의하고, 화면의 행동과 데이터에서 Functional Requirements, 데이터 계약, 화면 테스트 기준을 도출합니다. 화면 디자인과 화면 테스트를 중간에 별도 단계로 두지 않고 PRD 안에서 완결합니다.

기획 문서 또는 브리프를 다음 구조로 변환합니다.

- 제품 전체의 단일 정본 `docs/PRD.md`
- bkit이 읽는 feature별 `docs/00-pm/{feature}.prd.md`
- 작성자 결정 목록
- 통합/feature별 착수 gate

일반 이해관계자용 PRD나 범용 제품 전략 문서를 만드는 스킬이 아닙니다.

## 설치

Codex 플러그인으로 설치:

```bash
codex plugin marketplace add donchang07/skills --ref main
codex plugin add to-prd@donchang-skills
```

앱을 재시작하고 새 채팅에서 사용합니다. 업데이트는 `codex plugin marketplace upgrade donchang-skills`로 받습니다. 플러그인 배포본은 `plugins/to-prd/`에 있으며 편집 원본은 이 폴더입니다.

기존 폴더 복사 방식으로도 설치할 수 있습니다.

```bash
git clone https://github.com/donchang07/skills.git
```

Claude Code:

```bash
cp -r skills/to-prd ~/.claude/skills/to-prd
```

Codex:

```bash
cp -r skills/to-prd ~/.codex/skills/to-prd
```

재시작하면 Claude Code에서는 `/to-prd`, Codex에서는 `$to-prd`로 호출할 수 있습니다. 두 환경은 같은 SKILL.md와 산출물 구조를 사용합니다. bkit 개발 명령(`/pdca ...`)은 Claude Code에서 실행합니다.

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
| `docs/DESIGN.md` | 시각 시스템·컴포넌트. 없으면 Apple 기본값(`assets/apple-DESIGN.md`)을 복사 |
| `docs/PRD.md` | 기존 정본·ID·결정·개정 이력 |
| 브리프(PRD템플릿 Word 포함)·현재 대화·코드 | 최신 결정, 참고 사이트, 테스트 계정, 실제 시스템 제약 |

## 산출물과 단일 정본

`docs/PRD.md`가 유일한 정본입니다.

```text
docs/PRD.md                         제품 통합 정본
    │
    ├─ docs/PRD.html                읽기용 HTML (Apple 스타일)
    ├─ docs/DESIGN.md               없을 때만 Apple 기본값 복사
    ├─ docs/00-pm/{feature}.prd.md  bkit feature projection
    ├─ docs/00-pm/_decisions.md     미결 결정 projection
    ├─ docs/00-pm/_product.gate.md  제품 gate
    ├─ docs/00-pm/{feature}.gate.md feature gate
    └─ CLAUDE.md의 to-prd 블록       bkit 실행 규칙
```

feature PRD를 직접 수정하지 않습니다. 업데이트는 정본을 먼저 바꾸고 영향받는 파생본을 다시 만듭니다. 파생본에만 존재하는 사람의 편집은 덮어쓰기 전에 정본으로 옮깁니다.

현재 스키마는 `screen-first-v2`입니다. `screen-first-v1` PRD는 ID를 보존한 채 디자인 기준·컴포넌트·상태별 검증 SC·테스트 계정·테스트 식별자를 보강해 v2로 올립니다. 스키마 표기가 없으면 FR/SC ID를 보존한 채 화면 계약으로 마이그레이션합니다. 역할·화면·메뉴·인증·요소·데이터 연결이 완성되기 전에는 기존 최종본을 덮어쓰지 않습니다.

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
        ├─ 역할 + 화면 인벤토리 + 메뉴/인증
        ├─ 화면별 UI 요소 + 행동 + 데이터
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
5.  Screen Contract
    - 역할·접근 매트릭스
    - 화면 인벤토리
    - 데스크톱/모바일 메뉴
    - 로그인·권한·세션 흐름
    - 화면별 디자인 참고·레이아웃·UI 요소(컴포넌트)·행동·데이터·8개 상태(검증 SC)
6.  Functional Requirements + NFR (실행 검증·테스트 식별자·상태 유도)
7.  Success Criteria
8.  Edge Cases
9.  브랜드 & 디자인 (DESIGN.md·Pretendard·토큰·컴포넌트·참고 레퍼런스)
10. 범위 / 비범위 / 우선순위 / 납기
11. 레벨·스택·테스트 계정 + 시스템 가정 10칸
12. 구현자 오픈 이슈
13. 작성자 결정 요청
14. feature 분해표
15. bkit 실행 명세
부록 A. 데이터 계약
부록 B. 외부 사실 확인
```

화면은 `SCR-*`, 화면 요소는 `SCR-*-EL-*`, 데이터 엔티티는 `DATA-*` ID를 사용합니다. FR은 화면의 사용자 행동과 시스템 반응에서 도출되며 시나리오·화면 요소·SC·데이터·feature와 연결됩니다. 이 연결이 끊기면 gate가 결함으로 판정합니다.

## 화면 계약

화면 정의는 UI 목록이 아니라 구현 계약입니다.

- `비로그인 / 일반 사용자 / 관리자`의 열람·행동 차이
- 모든 화면의 Route·진입 조건·종료·뒤로 가기
- 메뉴 위치·순서·라벨·노출 역할·대상 화면
- 데스크톱·모바일 내비게이션 차이
- 관리자 기능이 있을 때 독립된 로그인/인증 화면
- 화면 안의 영역과 실제 UI 요소
- 요소별 표시값·입력 규칙·권한·조건·데이터·행동 결과
- 초기·로딩·빈·성공·검증 오류·시스템 오류·권한 없음·오프라인 상태
- 반응형·접근성 기준
- 화면별 디자인 참고와 요소별 컴포넌트

관리자 기능이나 보호 데이터가 있는데 로그인 화면이 없거나, 화면 요소가 `DATA-*`와 `FR-*`에 연결되지 않으면 착수 Blocker입니다.

## 디자인 기준

- 프로젝트에 `docs/DESIGN.md`가 있으면 그대로 사용합니다.
- 없으면 `assets/apple-DESIGN.md`(Apple 디자인 시스템, Pretendard)를 `docs/DESIGN.md`로 복사합니다. 기존 파일은 덮어쓰지 않습니다.
- 폰트는 항상 Pretendard입니다.
- PRD 9장에 토큰 요약, 컴포넌트 목록, 브리프의 참고 사이트(`REF-*`)를 기록하고, UI 요소의 컴포넌트 열은 이 목록의 이름만 사용합니다.

## 화면 테스트

화면 테스트는 별도로 설계하지 않고 화면 계약에서 도출합니다.

- P0 화면의 주요 전이·적용 상태·역할별 차이·인증과 세션은 각각 `[E2E]` SC가 됩니다.
- 반응형은 NFR 뷰포트로, 접근성은 자동 접근성 검사로 판정합니다.
- 요소 ID를 `data-testid`로 쓰고, 역할별 테스트 계정·시드와 상태 유도 방법을 PRD에 둡니다.
- 스크린샷 비교 테스트는 완료 조건에 넣지 않습니다.

## 읽기용 PRD.html

`docs/PRD.md`를 저장할 때마다 `scripts/render_prd_html.mjs`로 `docs/PRD.html`을 다시 만듭니다. 외부 의존성 없이 Node만 사용합니다.

- Apple 디자인 토큰과 Pretendard, 상단 요약(게이트 판정, 화면·FR·SC·데이터·feature 수)
- 고정 목차와 화면별 카드, 표 가로 스크롤
- `SCR`·`FR`·`SC`·`DATA`·`NAV`·`REF`·`D` ID를 정의 위치로 연결하는 링크
- `[E2E]`·`[통합]`·`[단위]`·`[수동]`, 상태 라벨, P0~P2를 색 배지로 표시
- 모바일·인쇄 레이아웃

```bash
node scripts/render_prd_html.mjs docs/PRD.md docs/PRD.html
```

HTML은 읽기용입니다. 수정은 항상 `docs/PRD.md`에서 합니다. 착수 불가일 때는 `docs/PRD.draft.html`을 만들고 기존 `docs/PRD.html`은 덮어쓰지 않습니다.

## CLAUDE.md 동기화

게이트를 통과하면 프로젝트 루트 `CLAUDE.md`에 `<!-- to-prd:begin -->`~`<!-- to-prd:end -->` 블록을 만들거나 다시 생성합니다. bkit이 매 세션 읽는 규칙이어서 PRD와 구현·검증이 같은 기준을 씁니다.

- UI는 `docs/DESIGN.md`, 폰트는 Pretendard, 컴포넌트는 PRD 9장 목록
- 모든 UI 요소에 PRD 요소 ID를 `data-testid`로 부여
- `/pdca analyze` 단계에서 PRD 11.1의 단위 테스트·Playwright 명령을 실제로 실행
- 완료는 match rate 기준과 테스트 전체 통과의 두 관문

마커 밖의 내용은 수정하지 않으며, 착수 불가(draft)일 때는 블록을 갱신하지 않습니다.

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
- `SCR/화면 요소/DATA/FR/SC` 정의·중복·참조 무결성
- 역할·화면 인벤토리·메뉴·인증 계약
- 화면별 메타·디자인 참고·레이아웃·UI 요소·컴포넌트·전이·8개 상태·반응형·접근성
- 9장 DESIGN.md·Pretendard·토큰·컴포넌트 목록·참고 레퍼런스
- P0 화면 상태별 검증 SC
- NFR 테스트 식별자·상태 유도, 11.1 테스트 계정·시드
- 관리자 기능과 로그인/인증 화면의 일치
- UI 요소의 데이터 바인딩과 FR의 화면·데이터 연결
- feature 분해표의 화면·FR·SC·데이터 누락
- unresolved placeholder
- 계약 섹션의 미결 표현
- 시스템 가정 10개와 상태 라벨
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
│   ├── apple-DESIGN.md
│   ├── prd-template.md
│   └── brief/
│       ├── PRD템플릿_v1.3.docx        # 현업 입력 양식
│       └── PRD작성핸드북_v1.3.docx    # 현업 사용 안내
├── references/
│   ├── bkit-contract.md
│   ├── brief-mapping.md            # 브리프 → PRD 대응, 브리프 버전 선언
│   ├── gate-checklist.md
│   └── screen-definition-contract.md
└── scripts/
    ├── check_sync.mjs              # 템플릿·핸드북·스킬 동기화 검사
    ├── render_prd_html.mjs
    └── validate_prd.mjs
```

## 템플릿·핸드북과의 동기화

템플릿·핸드북·스킬은 한 묶음입니다. 하나를 고치면 `references/brief-mapping.md`의 브리프 버전과 두 Word 파일의 파일명·파일 속성 제목을 함께 올리고 다음을 실행합니다.

```bash
node scripts/check_sync.mjs
```

## 기존 버전과의 차이

| 기존 | 현재 |
|---|---|
| 범용 Vibe UX PRD | bkit 전용 실행 계약 |
| `docs/PRD.md` 하나 | 정본 + feature projection + decisions + gate |
| 기획 문서 4개 중심 | 일부 문서 또는 브리프도 가능 |
| roadmap에 구현 분해 위임 | feature를 bkit PDCA 단위로 분해 |
| 단순 화면 표 | 역할·화면·메뉴·인증·레이아웃·요소·행동·데이터·8개 상태 계약 |
| 서술형 Edge Cases | 문구·동작·로그 계약 |
| 정성 검토 | Hard Gate + 점수 + Node 검사 |
| 미결 항목 한 종류 | 구현자 이슈와 작성자 결정 분리 |
| 경로·명령이 본문에 섞임 | versioned bkit contract reference로 분리 |

## 원칙

- bkit 전용 범위를 유지합니다.
- 정본은 하나이며 파생본은 정본에서 재생성합니다.
- 화면 계약을 먼저 작성하고 FR과 데이터를 화면에서 도출합니다.
- `SCR/화면 요소/DATA/FR/SC` ID와 개정 이력을 보존합니다.
- 기본값·추정·가설·출처를 구분합니다.
- 메뉴·일반/관리자 차이·로그인·화면 요소가 필요한데 빠진 PRD를 통과시키지 않습니다.
- 화면·요소·데이터 연결이 없는 P0 UI FR과 측정할 수 없는 SC를 통과시키지 않습니다.
- 일반 단어를 금지어로 검색하지 않고 실제 미결 의미를 검사합니다.
- Hard Gate가 점수보다 우선합니다.
