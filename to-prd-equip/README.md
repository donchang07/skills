# to-prd-equip (초안 v0.1)

반도체·검사 장비 소프트웨어용 `to-prd` 변형판입니다. 고객 변경 요청서를 읽어 bkit(PDCA)이 바로 쓸 **변경 영역 중심 PRD**를 만듭니다.

`to-prd`는 화면 중심이라 장비 업그레이드의 대부분인 검사 판정·불량 분류·호스트(SECS/GEM)·물류 변경을 계약으로 다루지 못합니다. 이 변형판은 운영 방식(정본, ID 보존, 비목표, 착수 게이트, `CLAUDE.md` 실행 규칙)은 그대로 두고 다음을 바꿉니다.

| 바뀐 점 | 내용 |
|---|---|
| 화면 계약 → 변경 영역 계약 | `RCP`·`INS`·`DEF`·`HOST`·`LOG`·`UI` 항목마다 현재 값·목표 값·근거·허용 경로 |
| 동결 영역 `FRZ-*` 추가 | 3D 측정·광학 보정·영상 취득·모션·통신 엔진처럼 AI가 고치면 안 되는 곳 |
| 시험 라벨 | `[골든]` 이미지 재생 · `[가상호스트]` · `[HIL]` · `[단위]` · `[현장]` |
| 완료 관문 셋 | match rate · 시험 통과 · 범위 감시(허용 경로 밖 변경 0건) |
| 2층 정본 | 제품 `docs/PRD.md` + 고객 `docs/customers/{customer}/PRD.md` |
| 입력 양식 | 고객 변경 요청서 `assets/change-request-template.md` |

## 구성

| 파일 | 역할 |
|---|---|
| `SKILL.md` | 절차와 운영 불변식 |
| `references/change-area-contract.md` | 변경 영역·동결 영역·장비 상태·시험 도출 규칙 |
| `references/request-mapping.md` | 요청서 → PRD 대응, 필수 항목 질문 |
| `references/gate-checklist.md` | Hard Gate HG-E01~E14 |
| `references/bkit-contract.md` | `to-prd`에서 복사한 bkit 계약 + 장비용 보충 |
| `assets/prd-template.md` | PRD 구조(change-area-v1) |
| `assets/change-request-template.md` | 고객대응 엔지니어용 입력 양식 |
| `scripts/validate_prd.mjs` | 기계 검사 |
| `examples/sample-customer-prd.md` | 가상 고객 예시(실제 고객·장비 아님) |

## 검사

```bash
node to-prd-equip/scripts/validate_prd.mjs to-prd-equip/examples/sample-customer-prd.md
```

## 아직 하지 않은 것

- 실제 고객 변경 요청서 2~3건으로 시험(장비 업체 소스와 요청서 필요)
- Word 양식과 작성 핸드북, `check_sync.mjs`
- 플러그인 배포본(`plugins/to-prd-equip/`)과 빌드 스크립트
- 소스 역생성은 짝 스킬 `code-prd-equip`이 맡습니다. 이 스킬은 그 결과를 `[역추출]` 라벨로 받기만 합니다
- `[골든]`·`[가상호스트]` 실행 명령은 가상 팹이 있어야 동작합니다. 예시의 `vfab` 명령은 가상의 이름입니다
