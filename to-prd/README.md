# to-prd

Vibe UX 기획 산출물을 하나의 **PRD(제품 요구사항 정의서)** 로 통합하고, 이후에도 갱신·관리하는 Claude Code 스킬입니다.

PRD는 단순 요약이 아니라 다음 단계인 **vibe-build의 roadmap·plan·build**가 그대로 따라가는 기준 문서입니다. 사람이 읽는 맥락(개요·배경·브랜드)과 기계가 파싱하는 **계약 섹션**(Functional Requirements·User Scenarios·Success Criteria·Edge Cases·Assumptions)을 함께 담습니다.

## 설치

```bash
git clone https://github.com/donchang07/skills.git
cp -r skills/to-prd ~/.claude/skills/to-prd
```

Claude Code를 재시작하면 `/to-prd`로 호출할 수 있습니다.

## 언제 쓰나

아래처럼 말하면 자동으로 활성화됩니다.

- "이제 PRD로 묶어줘", "기획 끝났으니 정리해줘", "제품 요구사항 정의서 만들어줘"
- "PRD 업데이트", "이 기능 PRD에 추가", "범위 바꿨으니 PRD 고쳐줘", "이거 결정됐으니 반영"

## 입력과 산출물

작업 폴더의 `docs/` 아래 파일을 읽습니다.

| 파일 | 만드는 스킬 | 담는 것 | 필수 |
|------|------------|---------|:---:|
| `docs/idea.md` | brainstorming-idea | 컨셉·문제·타깃·핵심 기능·플랫폼 | ✅ |
| `docs/benchmark.md` | benchmark-research | 경쟁 비교·차별 프레이밍 | ✅ |
| `docs/userflow.md` | userflow-generator | 온보딩·핵심 해피패스·화면 | ✅ |
| `docs/brandvoice.md` | brand-voice | 확정 이름·보이스·톤 | ✅ |
| `docs/DESIGN.md` | design-brandfit | 시각 디자인 시스템 | 있으면 |

산출물은 항상 `docs/PRD.md` 파일입니다. 채팅에만 보여주고 끝내지 않고 바로 저장합니다.

필수 파일이 빠져 있으면 어떤 스킬로 만들지 안내하고, 그대로 진행할 경우 해당 섹션을 `⚠️ (파일 없음 — 추후 보완)`으로 표시합니다. 추측으로 채우지 않습니다.

## 두 가지 모드

### 새로 만들기

`docs/PRD.md`가 없을 때. 입력 4개(+DESIGN.md)를 읽고 서로 연결하여 PRD를 처음부터 작성합니다.

### 업데이트

`docs/PRD.md`가 이미 있을 때. 덮어쓰지 않고 변경분만 반영합니다.

- **FR/SC ID 보존.** 기존 ID는 재배정하지 않습니다. 새 요구사항은 다음 번호로 추가하고, 제거된 항목은 `~~FR-004~~ (제거됨: 사유)`로 남깁니다.
- **수동 편집 보존.** 입력 문서에 없지만 PRD에 직접 추가한 내용은 그대로 둡니다.
- **개정 이력 누적.** 상단에 `vN 변경 요약 날짜` 한 줄을 추가합니다.

FR ID가 안정적이어야 roadmap의 요구사항 추적이 깨지지 않습니다.

## 작동 순서

1. **모드 판단** — `docs/PRD.md` 존재 여부로 새로 만들기 / 업데이트 결정
2. **입력 점검** — 필수 파일 확인, 빠진 파일 안내
3. **Functional Requirements 정리** — `FR-001`… ID, 테스트 가능한 문장, P0/P1/P2 우선순위, 관련 시나리오 연결
4. **계약 섹션 도출** — User Scenarios(완료 조건 포함), Success Criteria(`SC-001`…), Edge Cases, Assumptions
5. **범위/비범위** — v1 범위, Out of scope, 제품 관점 우선순위 묶음
6. **`docs/PRD.md` 저장**
7. **보고** — FR 개수·P0 개수·시나리오 수·오픈 이슈, 다음 단계(roadmap) 안내

## PRD 구조

```
1. 개요                       ← idea
2. 배경 & 근거                 ← benchmark
3. 목표 (Goals)
4. User Scenarios             ← userflow        [계약]
5. Functional Requirements    ← idea + userflow [계약]
6. Success Criteria                             [계약]
7. Edge Cases                                   [계약]
8. 화면 · 정보 구조            ← userflow
9. 브랜드 & 디자인             ← brandvoice + DESIGN
10. 범위 / 비범위 & 우선순위
11. Assumptions                                 [계약]
12. 오픈 이슈 / 리스크
```

`[계약]` 섹션 5개는 roadmap이 영어 라벨로 파싱하므로 제목을 영어 그대로 유지합니다.

## 우선순위 기준

| 등급 | 의미 |
|------|------|
| **P0** | MVP. 없으면 서비스가 성립하지 않는 핵심 가치(aha) 기능 |
| **P1** | 중요. 핵심 경험을 좋게 만들지만 첫 버전에 없어도 가치는 성립 |
| **P2** | 이후. 확장 아이디어, nice-to-have |

MVP는 작을수록 빨리 만들어지므로, 모든 것을 P0로 넣지 않도록 사용자에게 확인합니다.

## 원칙

- **추측으로 메우지 않는다.** 입력에 없는 내용은 묻거나 Assumptions / 오픈 이슈로 남긴다.
- **MVP를 작게.**
- **계약 섹션을 빠뜨리지 않는다.** 영어 제목과 FR/SC ID를 유지한다.
- **로드맵은 roadmap에 위임.** PRD는 "무엇을·왜·우선순위"까지만. 구현 마일스톤은 `docs/ROADMAP.md`의 몫이다.
- **PRD는 살아있는 문서.** 덮어쓰지 않고 업데이트한다.

## 스킬 체인

```
brainstorming-idea → benchmark-research → userflow-generator → brand-voice → design-brandfit
                                                                                   ↓
                                                                    to-prd (docs/PRD.md)
                                                                                   ↓
                                                              vibe-build/roadmap (docs/ROADMAP.md)
```

`DESIGN.md`가 없으면 roadmap 전에 **design-brandfit**을 먼저 실행해야 합니다.

## 파일

- `SKILL.md` — 스킬 본문 (Claude Code가 읽는 지시문)
- `README.md` — 이 문서
