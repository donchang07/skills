# dns-to-prd 플러그인

DN솔루션즈 업무 설명을 bkit용 PRD로 만드는 스킬입니다. to-prd의 절차·검사 스크립트를 그대로 쓰고, DN 도메인 팩(역할·통화·거점·기밀 등급·합성 데이터 원칙), 계산 모델 계약(CM-*), DN 점검 기준(DN-1~12)을 더합니다.

## 설치 (Claude Code)

to-prd가 먼저 설치돼 있어야 합니다.

```
/plugin marketplace add donchang07/skills
/plugin install to-prd@donchang-skills
/plugin install dns-to-prd@donchang-skills
```

## 유지보수

편집 원본은 저장소 루트의 `dns-to-prd/SKILL.md`입니다. 이 폴더의 `skills/dns-to-prd/SKILL.md`는 같은 내용의 배포본이며, 원본을 고친 뒤 그대로 복사합니다.
