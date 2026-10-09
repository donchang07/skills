# code-prd-equip (초안 v0.1)

이미 고객사에 설치된 장비 소프트웨어의 **소스에서 현재 상태를 추출**하는 스킬입니다. 결과는 PRD가 아니라 `to-prd-equip`이 읽는 현재 상태 문서입니다.

```text
현장 소스(기준 버전) ──code-prd-equip──▶ _as-is/{customer}.md  ([역추출], 근거·신뢰도)
                                              │  핵심 개발자 확인
고객 변경 요청서 ─────────────────────────────┴──to-prd-equip──▶ 고객 정본 PRD ──▶ bkit
```

## 왜 to-prd-equip과 나눴나

역생성은 틀릴 수 있는 일이고, PRD는 틀리면 안 되는 계약입니다. 한 스킬에 두면 추정이 계약에 섞입니다. 이 스킬의 값은 모두 `[역추출]`로 나가며, 핵심 개발자가 확인한 항목만 `to-prd-equip`에서 사실로 쓰입니다(to-prd-equip HG-E09).

## 하는 일

- 저장소를 영역(`RCP`·`INS`·`DEF`·`HOST`·`LOG`·`UI`)과 동결 후보(`FRZ`)로 나눈 코드 지도
- 변경 영역 항목의 현재 값을 `파일:줄` 근거, 신뢰도(높음·중간·낮음), 대조 결과와 함께 추출
- 동결 영역은 내용 없이 경로와 경계 인터페이스 후보만
- 핵심 개발자 확인표와 정확도 지표(담긴 비율·틀린 비율·모름 비율) — 제안서 "실험 1 · 역생성 정확도"의 측정값

## 하지 않는 일

목표 값, FR, 시험 기준, 개선 제안, 소스 붙여넣기.

## 구성

| 파일 | 역할 |
|---|---|
| `SKILL.md` | 절차와 운영 불변식 |
| `references/extraction-rules.md` | 영역별 찾는 곳, 근거·신뢰도·대조 규칙 |
| `assets/as-is-template.md` | 산출물 구조(as-is-v1) |
| `scripts/validate_asis.mjs` | 근거·라벨·신뢰도·코드 붙여넣기 검사 |
| `examples/sample-as-is.md` | 가상 고객 예시. 다음 단계는 `to-prd-equip/examples/sample-customer-prd.md` |

```bash
node code-prd-equip/scripts/validate_asis.mjs code-prd-equip/examples/sample-as-is.md
```

## 아직 하지 않은 것

- 실제 인텍 고객 소스로 시험(과거 업그레이드 재현 시험과 함께)
- 언어별(C++·C#) 탐색 힌트 보강
- 플러그인 배포본
