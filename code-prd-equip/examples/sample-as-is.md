# 현재 상태 — CUST-A FC-BGA 범프 검사 장비

> 상태: reviewed
> 산출물 스키마: as-is-v1
> 고객: CUST-A
> 장비: FC-BGA 범프 검사 장비(가상)
> 저장소: equip-sw (가상)
> 기준 버전: cust-a-3.4.2 · 9f3c1e2
> 공통 코어 비교 기준: core-3.4.0
> 실행 환경: 사내 망분리 서버 · 사내 승인 모델
> 보안 등급: B
> 변경 지도: 제품 정본 v1.2
> 작성일: 2026-10-06 · 확인 반영일: 2026-10-07
> 라벨: [역추출] 미확인 · [역추출·확인: 이름 날짜] · [역추출·정정: 이름 날짜]

**이 문서는 code-prd-equip 사용법을 보여 주는 가상 예시입니다. 고객·장비·경로·수치는 실제가 아닙니다. 다음 단계 예시는 `to-prd-equip/examples/sample-customer-prd.md`입니다.**

## 1. 요약

| 영역 | 항목 수 | 높음 | 중간 | 낮음 | 모름 | 확인됨 |
|---|---:|---:|---:|---:|---:|---:|
| INS | 2 | 1 | 1 | 0 | 0 | 2 |
| DEF | 2 | 2 | 0 | 0 | 0 | 2 |
| HOST | 3 | 2 | 0 | 0 | 1 | 2 |

## 2. 코드 지도

| 모듈·경로 | 분류 | 분류 근거 |
|---|---|---|
| src/inspection/rules/ | INS | 판정 함수, Pass/Fail 열거형 |
| src/defect/classes/ | DEF | DefectClass 열거형, 호스트 코드 표 |
| src/host/reports/ | HOST | S6F11 보고 구성, CEID 표 |
| src/gem/engine/ | FRZ | HSMS 연결, SECS-II 인코딩 |
| src/measure3d/ | FRZ | 높이 측정 알고리즘 |
| src/optics/ | FRZ | 캘리브레이션 |
| src/acquire/ | FRZ | 카메라 트리거, 스티칭 |
| src/motion/ | FRZ | 축 제어, 인터록 |
| tools/legacy_export/ | 미분류 | 사용처 확인 안 됨 |

## 3. 동결 영역 후보

| ID | 영역 | 경로 | 경계 인터페이스 후보 | 근거 |
|---|---|---|---|---|
| AS-FRZ-001 | 3D 측정 엔진 | src/measure3d/** | MeasureResult 구조체 | src/measure3d/result.h:12 |
| AS-FRZ-002 | 광학 보정 | src/optics/** | CalibStore::get | src/optics/calib_store.h:20 |
| AS-FRZ-003 | 영상 취득·스티칭 | src/acquire/** | FrameBuffer 읽기 | src/acquire/frame_buffer.h:31 |
| AS-FRZ-004 | 모션·안전 | src/motion/** | 없음 | src/motion/axis.h:1 |
| AS-FRZ-005 | SECS/GEM 통신 엔진 | src/gem/engine/** | ReportRegistry::define | src/gem/engine/report_registry.h:44 |

## 4. 변경 영역 항목

### 4.1 RCP 레시피·검사 조건

해당 없음 — 이번 추출 범위(변경 지도 우선 영역) 밖

### 4.2 INS 검사 판정 기준

| ID | 항목 | 현재 값 | 근거 | 신뢰도 | 대조 | 고객 특이 | 라벨 | 비고 |
|---|---|---|---|---|---|---|---|---|
| AS-INS-001 | 범프 연결 판정 | bridge_width >= 15µm → 이물(FM) | src/inspection/rules/foreign_material.cpp:88 | 높음 | 일치 | 아니오 | [역추출·확인: 김OO 2026-10-07] | 경계값 포함 |
| AS-INS-002 | 이물 최소 면적 | area >= 120µm² → 이물 | src/inspection/rules/foreign_material.cpp:64; recipe/cust-a/default.xml:210 | 중간 | 대조 자료 없음 | 예 | [역추출·정정: 김OO 2026-10-07] 150µm² | 레시피로 덮어씀 |

### 4.3 DEF 불량 분류

| ID | 항목 | 현재 값 | 근거 | 신뢰도 | 대조 | 고객 특이 | 라벨 | 비고 |
|---|---|---|---|---|---|---|---|---|
| AS-DEF-001 | 이물 클래스 | FM · 호스트 코드 12 | src/defect/classes/defect_class.h:30 | 높음 | 일치 | 아니오 | [역추출·확인: 김OO 2026-10-07] | |
| AS-DEF-002 | 클래스 코드 사용 범위 | 1~26 사용, 27 이후 비어 있음 | src/defect/classes/host_code_map.cpp:15-48 | 높음 | 대조 자료 없음 | 아니오 | [역추출·확인: 김OO 2026-10-07] | 신규 클래스 코드 후보 |

### 4.4 HOST 호스트 연동

| ID | 항목 | 현재 값 | 근거 | 신뢰도 | 대조 | 고객 특이 | 라벨 | 비고 |
|---|---|---|---|---|---|---|---|---|
| AS-HOST-001 | 로트 종료 이벤트 | S6F11 · CEID 3010 · RPTID 310 | src/host/reports/lot_end.cpp:22 | 높음 | 일치 | 예 | [역추출·확인: 박OO 2026-10-07] | 고객 사양서 rev.7과 일치 |
| AS-HOST-002 | RPTID 310 변수 | SVID 4101 로트 ID, 4120 총 불량 수 | src/host/reports/lot_end.cpp:30-41 | 높음 | 일치 | 예 | [역추출·확인: 박OO 2026-10-07] | |
| AS-HOST-003 | 통신 끊김 시 스풀 크기 | 모름 | 찾아본 곳: src/host/reports/, src/gem/engine/spool.cpp | 낮음 | 대조 자료 없음 | 비교 기준 없음 | [역추출] | 엔진 설정 파일 위치 확인 필요 |

### 4.5 LOG 물류·캐리어

해당 없음 — 이번 추출 범위 밖

### 4.6 UI 장비 HMI

해당 없음 — 이번 추출 범위 밖

## 5. 모름 목록

| ID | 무엇을 모르는가 | 찾아본 곳 | 누가 알 것 같은가 |
|---|---|---|---|
| AS-HOST-003 | 스풀 최대 크기와 초과 시 동작 | src/gem/engine/spool.cpp | 통신팀 |

## 6. 발견 사항

- tools/legacy_export/는 빌드 대상에 없음(사용처 확인 필요)

## 7. PRD 이관 대응

| AS ID | PRD ID | 정본 |
|---|---|---|
| AS-INS-001 | INS-001 (현재 조건) | docs/customers/cust-a/PRD.md |
| AS-DEF-002 | DEF-001 (코드 27 선택 근거) | docs/customers/cust-a/PRD.md |
| AS-HOST-001 | HOST-001 | docs/customers/cust-a/PRD.md |
| AS-HOST-002 | HOST-001 | docs/customers/cust-a/PRD.md |
| AS-FRZ-001~005 | FRZ-001~005 | docs/PRD.md |
