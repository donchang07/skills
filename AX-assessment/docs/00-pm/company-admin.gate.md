# 착수 게이트 — docs/00-pm/company-admin.prd.md

- 대상: docs/00-pm/company-admin.prd.md (feature projection)
- 정본 개정: v1.0, 2026-10-01 · 생성: scripts/project_features.mjs
- 검사 시각: 2026-10-01

## Hard Gate

HG-01~HG-13은 정본 게이트(docs/00-pm/_product.gate.md)와 같다. 파생본 고유 항목 HG-07(정본 개정·포함 계약 일치): 통과 — 정본 v1.0에서 자동 생성, 이 feature의 화면·공통 인증 화면(SCR-005, SCR-014)·관련 FR·SC·DATA 포함.

## 점수·판정

정본 판정을 따른다: **착수 가능 · Blocker 0**. 이 feature 고유 결함은 아래 기계 검사 WARN뿐이다(Minor).

## 기계 검사

- 명령: `node ../to-prd/scripts/validate_prd.mjs docs/00-pm/company-admin.prd.md`
- WARN  화면 요소나 FR에서 참조하지 않는 데이터: DATA-009
- Summary: ERROR 0, WARN 1, FILES 1

## 시작 명령

`/pdca plan company-admin`
