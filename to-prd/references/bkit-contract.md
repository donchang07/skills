# bkit 계약 기준

이 파일은 bkit처럼 자주 바뀌는 외부 계약을 SKILL.md에서 분리한다. PRD를 만들 때 프로젝트의 **로컬 설치본과 `bkit.config.json`을 먼저 확인**하고, 이 문서는 확인할 수 없을 때 사용하는 검증 기준으로 삼는다.

## 검증 기준

- 저장소: https://github.com/ww-w-ai/bkit-claude-code
- 확인일: 2026-09-16
- 확인 버전: v2.1.38
- 런타임: Claude Code 전용
- 근거:
  - `bkit.config.json`의 `pdca.docPaths.pm`, `matchRateThreshold`, `autoIterate`, `maxIterations`
  - 공식 README/README-FULL의 PDCA 및 Sprint 명령 설명
  - 공식 bkit System Architecture 문서의 최신 maintenance release 표기

## 우선순위

계약이 다르면 다음 순서로 적용한다.

1. 현재 프로젝트의 `bkit.config.json`
2. 현재 설치된 bkit의 skill·template·README
3. 이 reference의 검증 기준

차이가 있으면 PRD 15장에 실제 사용한 값과 출처를 쓰고 부록 B에 재확인 항목을 남긴다. 확인 없이 새로운 경로나 명령을 추측하지 않는다.

## PRD 탐색 경로

v2.1.38 기본 설정은 PM 문서를 다음 순서로 찾는다.

1. `docs/00-pm/features/{feature}.prd.md`
2. `docs/00-pm/{feature}.prd.md`

이 스킬의 기본 출력은 기존 Vibe UX 호환성을 위해 두 번째 경로인 `docs/00-pm/{feature}.prd.md`다. 프로젝트 설정이 첫 번째 경로만 허용하도록 바뀌었다면 로컬 설정을 따라 출력 경로를 바꾼다.

`docs/PRD.md`는 이 스킬의 제품 통합 정본이며 bkit feature 실행 파일을 대체하지 않는다.

## PDCA 설정 기본값

v2.1.38의 `bkit.config.json` 기본값:

```json
{
  "pdca": {
    "matchRateThreshold": 90,
    "autoIterate": true,
    "maxIterations": 5,
    "requireDesignDoc": true,
    "automationLevel": "semi-auto"
  }
}
```

Sprint 설정에는 별도의 목표·최소 허용값이 있을 수 있으므로 Sprint 실행에서는 `sprint` 섹션을 함께 읽는다. PRD에 값을 복사할 때 프로젝트 설정을 우선한다.

## 실행 흐름

feature 단위 기본 흐름:

```text
/pdca plan {feature}
→ /pdca design {feature}
→ /pdca do {feature}
→ /pdca analyze {feature}
→ 기준 미달이면 autoIterate가 자동으로 Check/Act 반복
→ /pdca report {feature}
```

`/pdca iterate`는 v2.1.38의 일반 사용자 수동 버튼으로 안내하지 않는다. `autoIterate`가 켜져 있으면 gap-detector가 기준 미달을 감지해 자동 실행하며, 반복 한도에 도달하면 중단·상향 보고한다.

여러 feature를 묶을 때:

```text
/sprint master-plan {release} --features feature-a,feature-b
```

실제 Sprint 명령과 옵션은 로컬 설치본을 다시 확인한다.

## 이 스킬과 `/pdca pm`의 관계

bkit의 `/pdca pm <feature>`는 자체 PM 팀을 실행해 `docs/00-pm/<feature>.prd.md`를 만든다. 이 스킬은 Vibe UX 기획 산출물이나 사용자 브리프를 같은 계약 수준의 PRD로 변환하므로 다음처럼 처리한다.

- 이 스킬이 새 PRD를 만들었다면 `/pdca pm`을 건너뛰고 `/pdca plan`부터 시작한다.
- 기존 `/pdca pm` 산출물이 있으면 폐기하지 말고 입력으로 읽어 정본에 병합한다.
- 프로젝트가 PM Gate에서 별도 메타데이터를 요구하면 로컬 template에 맞춰 추가한다.

## PRD가 제공해야 하는 bkit 입력

### Plan

- Executive Summary와 Context Anchor
- FR과 NFR
- Success Criteria
- 범위·비범위·우선순위

### Design

- 데이터 계약
- Page UI Checklist와 화면 상태
- 오류·경계 처리
- 레벨·스택·권한·배포 가정

### Check/Act

- FR과 SC의 검증 방법
- 오류 처리의 기대 동작
- 로딩·빈·오류·성공 상태
- match rate 기준과 반복 한도

## 업데이트 조건

다음 중 하나가 바뀌면 이 파일을 다시 검증한다.

- bkit 버전
- `bkit.config.json`의 `pdca.docPaths` 또는 gate 값
- PDCA/Sprint 명령 이름이나 자동화 방식
- Plan·Design template의 필수 섹션
- gap-detector의 평가 축 또는 가중치
