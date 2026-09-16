#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const requested = process.argv.slice(2);
const files = requested.length > 0
  ? requested
  : (fs.existsSync("docs/PRD.md") ? ["docs/PRD.md"] : []);

if (files.length === 0) {
  console.error("Usage: node scripts/validate_prd.mjs <PRD file> [additional PRD files...]");
  process.exit(2);
}

const requiredHeadings = [
  "## 0. Executive Summary",
  "## 1. 개요",
  "## 2. 배경 & 근거",
  "## 3. 목표 (Goals)",
  "## 4. User Scenarios",
  "## 5. Functional Requirements",
  "## 6. Success Criteria",
  "## 7. Edge Cases",
  "## 8. 화면 · 정보 구조 (Page UI Checklist)",
  "## 9. 브랜드 & 디자인",
  "## 10. 범위 / 비범위 & 우선순위 · 납기",
  "## 11. Assumptions",
  "## 12. 오픈 이슈 / 리스크 [구현자]",
  "## 13. 작성자 결정 요청 [작성자]",
  "## 14. feature 분해표",
  "## 15. bkit 실행 명세",
  "## 부록 A. 데이터 계약",
  "## 부록 B. 외부 사실 확인"
];

let totalErrors = 0;
let totalWarnings = 0;

function escapeRegExp(value) {
  return value.replace(/[.*+?^$()|[\]\\]/g, "\\$&");
}

function section(text, startHeading, endHeading) {
  const start = text.search(new RegExp("^" + escapeRegExp(startHeading) + "\\s*$", "m"));
  if (start < 0) return "";
  const bodyStart = start + text.slice(start).indexOf("\n") + 1;
  if (!endHeading) return text.slice(bodyStart);
  const tail = text.slice(bodyStart);
  const end = tail.search(new RegExp("^" + escapeRegExp(endHeading) + "\\s*$", "m"));
  return end < 0 ? tail : tail.slice(0, end);
}

function tableIds(text, prefix) {
  const pattern = new RegExp("^\\|\\s*(" + prefix + "-\\d{3,})\\s*\\|", "gm");
  return Array.from(text.matchAll(pattern), function (match) { return match[1]; });
}

function duplicates(values) {
  const seen = new Set();
  const duplicate = new Set();
  for (const value of values) {
    if (seen.has(value)) duplicate.add(value);
    seen.add(value);
  }
  return Array.from(duplicate);
}

function inspect(file) {
  const errors = [];
  const warnings = [];
  const resolved = path.resolve(file);
  let text;

  try {
    text = fs.readFileSync(resolved, "utf8");
  } catch (error) {
    errors.push("파일을 읽을 수 없음: " + error.message);
    return { file: resolved, errors, warnings };
  }

  if (!/^# PRD — .+/m.test(text)) {
    errors.push("문서 제목 '# PRD — ...'가 없음");
  }

  if (!/^> 상태: (final|draft|superseded)\s*$/m.test(text)) {
    errors.push("상단 메타의 상태가 final, draft, superseded 중 하나가 아님");
  }

  for (const heading of requiredHeadings) {
    if (!text.includes(heading)) errors.push("필수 장 누락: " + heading);
  }

  const placeholderMatches = text.match(/\{[^{}\n]{1,120}\}|<(?:placeholder|feature|product|name|date|YYYY-MM-DD|[^<>\n]*(?:입력|작성|결정|항목|이름|값)[^<>\n]*)>/gi) || [];
  if (placeholderMatches.length > 0) {
    errors.push("미해결 placeholder " + placeholderMatches.length + "개: " + placeholderMatches.slice(0, 5).join(", "));
  }

  const contract = section(text, "## 4. User Scenarios", "## 9. 브랜드 & 디자인");
  const unresolved = contract.match(/\b(?:TBD|TODO)\b|미정|택일|검토\s*중|결정\s*필요/gi) || [];
  if (unresolved.length > 0) {
    errors.push("4~8장에 unresolved 표현 " + unresolved.length + "개: " + Array.from(new Set(unresolved)).join(", "));
  }

  const frIds = tableIds(text, "FR");
  const scIds = tableIds(text, "SC");
  if (frIds.length === 0) errors.push("정의된 FR 행이 없음");
  if (scIds.length === 0) errors.push("정의된 SC 행이 없음");

  const duplicateFr = duplicates(frIds);
  const duplicateSc = duplicates(scIds);
  if (duplicateFr.length > 0) errors.push("중복 FR 정의: " + duplicateFr.join(", "));
  if (duplicateSc.length > 0) errors.push("중복 SC 정의: " + duplicateSc.join(", "));

  const featureMap = section(text, "## 14. feature 분해표", "## 15. bkit 실행 명세");
  for (const frId of frIds) {
    if (!featureMap.includes(frId)) errors.push("14장 feature 분해표에 없는 FR: " + frId);
  }
  for (const scId of scIds) {
    if (!featureMap.includes(scId)) errors.push("14장 feature 분해표에 없는 SC: " + scId);
  }

  const assumptions = section(text, "### 11.2 시스템 가정 10칸", "### 11.3 제품 가정");
  for (let index = 1; index <= 10; index += 1) {
    const rowPattern = new RegExp("^\\|\\s*" + index + "\\s*\\|(.+)$", "m");
    const match = assumptions.match(rowPattern);
    if (!match) {
      errors.push("11.2 시스템 가정 행 누락: " + index);
      continue;
    }
    if (!/\[(?:확정|기본값|해당 없음|결정 필요)\]/.test(match[1])) {
      errors.push("11.2 시스템 가정 " + index + "번의 상태 라벨 누락");
    }
  }

  const screens = section(text, "## 8. 화면 · 정보 구조 (Page UI Checklist)", "## 9. 브랜드 & 디자인");
  for (const state of ["로딩", "빈", "오류", "성공"]) {
    if (!screens.includes(state)) warnings.push("8장 전체에서 화면 상태를 찾지 못함: " + state);
  }

  const success = section(text, "## 6. Success Criteria", "## 7. Edge Cases");
  if (!success.includes("현재 PRD 데이터로 검증 가능")) {
    errors.push("6장에 현재 PRD 데이터 검증 가능 여부 열이 없음");
  }

  const edge = section(text, "## 7. Edge Cases", "## 8. 화면 · 정보 구조 (Page UI Checklist)");
  for (const column of ["상황", "사용자 표시 문구", "이후 동작", "로그"]) {
    if (!edge.includes(column)) errors.push("7장 오류 처리 표 열 누락: " + column);
  }

  if (resolved.includes(path.join("docs", "00-pm")) && !text.includes("> 정본: docs/PRD.md")) {
    errors.push("feature 파생본에 정본 경로·개정 메타가 없음");
  }

  if (!text.includes("matchRateThreshold") || !text.includes("maxIterations")) {
    errors.push("15장에 bkit gate 설정이 없음");
  }

  return { file: resolved, errors, warnings };
}

for (const file of files) {
  const result = inspect(file);
  console.log("\n" + result.file);
  for (const message of result.errors) console.log("ERROR " + message);
  for (const message of result.warnings) console.log("WARN  " + message);
  if (result.errors.length === 0 && result.warnings.length === 0) console.log("PASS  기계 검사 통과");
  totalErrors += result.errors.length;
  totalWarnings += result.warnings.length;
}

console.log("\nSummary: ERROR " + totalErrors + ", WARN " + totalWarnings + ", FILES " + files.length);
if (totalErrors > 0) process.exitCode = 1;
