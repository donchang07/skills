# dns-part-prd 플러그인

고객 부품 도면을 가공 PRD로 만드는 스킬입니다. 도면의 모든 요구를 요구 추적표(REQ)로 옮기고, 공정·기계·시뮬레이션 합격 기준(SC)·검사(INSP)·일정·승인에 하나씩 연결합니다. 요청하면 공정표에서 NC 코드를 만들고 시연용 대역 검사기로 검사합니다.

## 설치 (Claude Code)

```
/plugin marketplace add donchang07/skills
/plugin install dns-part-prd@donchang-skills
```

## 포함 파일

- `skills/dns-part-prd/scripts/`: NC 빠른 검사기(nc_check.mjs), 형상·고정구 검사기(sim_check.py), 합성 기계 사양(machine.json)
- `skills/dns-part-prd/examples/SYN-BRK-0101/`: 합성 도면과 가공 PRD, NC 예시

검사기는 DN Virtual Simulator가 아닌 시연용 대역이며, 예제의 도면·사양은 모두 합성 데이터입니다.

## 유지보수

편집 원본은 저장소 루트의 `dns-part-prd/`입니다. 이 폴더의 `skills/dns-part-prd/`는 같은 내용의 배포본이며, 원본을 고친 뒤 그대로 복사합니다.
