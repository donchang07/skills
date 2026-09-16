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
  "## 5. 화면 정의 & 정보 구조 (Screen Contract)",
  "## 6. Functional Requirements",
  "## 7. Success Criteria",
  "## 8. Edge Cases",
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

const screenSubheadings = [
  "### 5.1 역할·접근 매트릭스",
  "### 5.2 화면 인벤토리",
  "### 5.3 메뉴·내비게이션",
  "### 5.4 인증·권한 흐름",
  "### 5.5 화면 상세"
];

const screenMetadata = [
  "화면 유형",
  "Route",
  "대상 사용자·권한",
  "목적",
  "진입 조건",
  "종료·전이",
  "관련 시나리오",
  "관련 FR·SC",
  "관련 데이터"
];

const screenDetailHeadings = [
  "##### 레이아웃·영역",
  "##### UI 요소 계약",
  "##### 상호작용·전이",
  "##### 화면 상태",
  "##### 반응형·접근성"
];

const screenStates = [
  "초기",
  "로딩",
  "빈",
  "성공",
  "검증 오류",
  "시스템 오류",
  "권한 없음",
  "오프라인"
];

let totalErrors = 0;
let totalWarnings = 0;

function escapeRegExp(value) {
  return value.replace(/[.*+?^$()|[\]\\]/g, "\\$&");
}

function section(text, startHeading, endHeading) {
  const start = text.search(new RegExp("^" + escapeRegExp(startHeading) + "\\s*$", "m"));
  if (start < 0) return "";
  const newline = text.indexOf("\n", start);
  const bodyStart = newline < 0 ? text.length : newline + 1;
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

function unique(values) {
  return Array.from(new Set(values));
}

function references(text, pattern) {
  return unique(Array.from(text.matchAll(pattern), function (match) { return match[0]; }));
}

function markdownCells(line) {
  const trimmed = line.trim();
  if (!trimmed.startsWith("|")) return [];
  return trimmed.replace(/^\|/, "").replace(/\|$/, "").split("|").map(function (cell) {
    return cell.trim();
  });
}

function hasTableDataRow(text, headerFirstCell) {
  for (const line of text.split(/\r?\n/)) {
    const cells = markdownCells(line);
    if (cells.length === 0) continue;
    if (cells[0] === headerFirstCell) continue;
    if (cells.every(function (cell) { return /^:?-{3,}:?$/.test(cell); })) continue;
    return true;
  }
  return false;
}

function blocksByHeading(text, pattern) {
  const matches = Array.from(text.matchAll(pattern));
  return matches.map(function (match, index) {
    const start = match.index + match[0].length;
    const end = index + 1 < matches.length ? matches[index + 1].index : text.length;
    return { id: match[1], name: match[2].trim(), body: text.slice(start, end) };
  });
}

function missingFrom(reference, actual) {
  const actualSet = new Set(actual);
  return unique(reference).filter(function (value) { return !actualSet.has(value); });
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

  if (!/^> PRD 스키마: screen-first-v1\s*$/m.test(text)) {
    errors.push("상단 메타에 'PRD 스키마: screen-first-v1'이 없음");
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
    errors.push("4~8장에 unresolved 표현 " + unresolved.length + "개: " + unique(unresolved).join(", "));
  }

  const screens = section(text, "## 5. 화면 정의 & 정보 구조 (Screen Contract)", "## 6. Functional Requirements");
  for (const heading of screenSubheadings) {
    if (!screens.includes(heading)) errors.push("5장 화면 계약 필수 절 누락: " + heading);
  }

  const roles = section(screens, "### 5.1 역할·접근 매트릭스", "### 5.2 화면 인벤토리");
  for (const column of ["기능·영역", "비로그인", "일반 사용자", "관리자", "차이·제약"]) {
    if (!roles.includes(column)) errors.push("5.1 역할·접근 표 열 누락: " + column);
  }
  if (!hasTableDataRow(roles, "기능·영역")) errors.push("5.1 역할·접근 매트릭스에 정의 행이 없음");

  const inventory = section(screens, "### 5.2 화면 인벤토리", "### 5.3 메뉴·내비게이션");
  for (const column of ["화면 ID", "화면명", "Route·진입 방식", "화면 유형", "대상 역할", "진입점", "핵심 목적", "관련 시나리오", "우선순위"]) {
    if (!inventory.includes(column)) errors.push("5.2 화면 인벤토리 열 누락: " + column);
  }
  const inventoryIds = tableIds(inventory, "SCR");
  if (inventoryIds.length === 0) errors.push("5.2 화면 인벤토리에 SCR 행이 없음");
  const duplicateInventory = duplicates(inventoryIds);
  if (duplicateInventory.length > 0) errors.push("화면 인벤토리 중복 ID: " + duplicateInventory.join(", "));

  const menu = section(screens, "### 5.3 메뉴·내비게이션", "### 5.4 인증·권한 흐름");
  for (const column of ["메뉴 ID", "위치·순서", "라벨", "노출 역할", "대상 화면", "데스크톱", "모바일", "활성·선택 규칙"]) {
    if (!menu.includes(column)) errors.push("5.3 메뉴·내비게이션 표 열 누락: " + column);
  }
  if (!/^\|\s*NAV-\d{3,}\s*\|/m.test(menu)) errors.push("5.3 메뉴·내비게이션에 NAV 행이 없음");
  if (!menu.includes("사이트맵")) errors.push("5.3에 사이트맵이 없음");
  if (!menu.includes("공통 복귀 규칙")) errors.push("5.3에 공통 복귀 규칙이 없음");

  const auth = section(screens, "### 5.4 인증·권한 흐름", "### 5.5 화면 상세");
  const authMatch = auth.match(/\*\*인증 사용:\*\*\s*(예|아니오\s*—[^\n]+)/);
  if (!authMatch) errors.push("5.4 인증 사용 여부가 '예' 또는 '아니오 — 이유'로 정의되지 않음");
  for (const column of ["상황", "화면 ID", "진입 조건", "성공 결과·복귀", "실패·만료·권한 없음"]) {
    if (!auth.includes(column)) errors.push("5.4 인증·권한 표 열 누락: " + column);
  }

  const detailArea = section(screens, "### 5.5 화면 상세");
  const screenBlocks = blocksByHeading(detailArea, /^####\s+(SCR-\d{3,})\s+—\s+(.+)$/gm);
  const detailIds = screenBlocks.map(function (block) { return block.id; });
  if (detailIds.length === 0) errors.push("5.5에 '#### SCR-001 — 화면명' 형식의 화면 상세가 없음");
  const duplicateDetails = duplicates(detailIds);
  if (duplicateDetails.length > 0) errors.push("화면 상세 중복 ID: " + duplicateDetails.join(", "));

  const missingDetails = missingFrom(inventoryIds, detailIds);
  const missingInventory = missingFrom(detailIds, inventoryIds);
  if (missingDetails.length > 0) errors.push("인벤토리에 있지만 상세가 없는 화면: " + missingDetails.join(", "));
  if (missingInventory.length > 0) errors.push("상세는 있지만 인벤토리에 없는 화면: " + missingInventory.join(", "));

  const menuScreenRefs = references(menu, /SCR-\d{3,}/g);
  const authScreenRefs = references(auth, /SCR-\d{3,}/g);
  for (const screenId of unique(menuScreenRefs.concat(authScreenRefs))) {
    if (!detailIds.includes(screenId)) errors.push("메뉴·인증 흐름이 정의되지 않은 화면을 참조: " + screenId);
  }

  const allElementIds = [];
  const elementDataRefs = [];
  let hasAdminCapability = false;

  for (const block of screenBlocks) {
    for (const label of screenMetadata) {
      if (!block.body.includes("**" + label + ":**")) {
        errors.push(block.id + " 메타데이터 누락: " + label);
      }
    }

    for (const heading of screenDetailHeadings) {
      if (!block.body.includes(heading)) errors.push(block.id + " 상세 절 누락: " + heading);
    }

    if (!/^\- \*\*화면 유형:\*\*[ \t]*(공개|일반|관리자|인증|공통)[ \t]*$/m.test(block.body)) {
      errors.push(block.id + " 화면 유형이 공개·일반·관리자·인증·공통 중 하나가 아님");
    }
    if (/^\- \*\*화면 유형:\*\*[ \t]*관리자[ \t]*$/m.test(block.body)) hasAdminCapability = true;

    const layout = section(block.body, "##### 레이아웃·영역", "##### UI 요소 계약");
    for (const column of ["순서·영역", "구성 요소 ID", "일반 사용자", "관리자", "모바일·반응형"]) {
      if (!layout.includes(column)) errors.push(block.id + " 레이아웃 표 열 누락: " + column);
    }
    if (!hasTableDataRow(layout, "순서·영역")) errors.push(block.id + " 레이아웃·영역 정의 행이 없음");

    const elements = section(block.body, "##### UI 요소 계약", "##### 상호작용·전이");
    for (const column of ["요소 ID", "종류", "표시 내용·라벨", "사용자·권한", "표시·활성 조건", "데이터 바인딩", "입력·검증", "행동·결과"]) {
      if (!elements.includes(column)) errors.push(block.id + " UI 요소 표 열 누락: " + column);
    }

    const elementMatches = Array.from(elements.matchAll(/^\|\s*(SCR-\d{3,}-EL-\d{2,})\s*\|(.+)$/gm));
    if (elementMatches.length === 0) errors.push(block.id + "에 정의된 UI 요소 행이 없음");
    for (const match of elementMatches) {
      const elementId = match[1];
      const cells = markdownCells(match[0]);
      allElementIds.push(elementId);
      if (!elementId.startsWith(block.id + "-EL-")) {
        errors.push(block.id + " 블록에 다른 화면의 요소 ID가 있음: " + elementId);
      }
      if (cells.length < 8) {
        errors.push(elementId + " UI 요소 행의 열이 부족함");
        continue;
      }
      const permission = cells[3];
      const dataBinding = cells[5];
      const validation = cells[6];
      const action = cells[7];
      if (permission.includes("관리자")) hasAdminCapability = true;
      if (!/(?:DATA-\d{3,}|정적|해당 없음\s*—)/.test(dataBinding)) {
        errors.push(elementId + " 데이터 바인딩이 DATA ID·정적·해당 없음 중 하나가 아님");
      }
      elementDataRefs.push(...references(dataBinding, /DATA-\d{3,}/g));
      if (!validation || validation === "—") errors.push(elementId + " 입력·검증 계약이 비어 있음");
      if (!action || action === "—") errors.push(elementId + " 행동·결과 계약이 비어 있음");
    }

    const interactions = section(block.body, "##### 상호작용·전이", "##### 화면 상태");
    for (const column of ["트리거", "선행 조건", "처리·데이터 변화", "성공 결과·다음 화면", "실패 결과", "관련 FR·SC"]) {
      if (!interactions.includes(column)) errors.push(block.id + " 상호작용 표 열 누락: " + column);
    }
    if (!hasTableDataRow(interactions, "트리거")) errors.push(block.id + " 상호작용·전이 정의 행이 없음");

    const states = section(block.body, "##### 화면 상태", "##### 반응형·접근성");
    for (const state of screenStates) {
      if (!new RegExp("^\\|\\s*" + escapeRegExp(state) + "\\s*\\|", "m").test(states)) {
        errors.push(block.id + " 화면 상태 누락: " + state);
      }
    }

    const responsive = section(block.body, "##### 반응형·접근성");
    if (!responsive.includes("**반응형:**")) errors.push(block.id + " 반응형 계약 누락");
    if (!responsive.includes("**접근성:**")) errors.push(block.id + " 접근성 계약 누락");
  }

  const duplicateElements = duplicates(allElementIds);
  if (duplicateElements.length > 0) errors.push("중복 UI 요소 ID: " + duplicateElements.join(", "));

  const authEnabled = authMatch && authMatch[1] === "예";
  const hasAuthScreen = screenBlocks.some(function (block) {
    return /^\- \*\*화면 유형:\*\*[ \t]*인증[ \t]*$/m.test(block.body);
  });
  if (hasAdminCapability && !authEnabled) {
    errors.push("관리자 기능·요소가 있지만 5.4 인증 사용이 '예'가 아님");
  }
  if (authEnabled && !hasAuthScreen) {
    errors.push("인증을 사용하지만 독립된 '화면 유형: 인증' 화면 상세가 없음");
  }

  const frIds = tableIds(text, "FR");
  const scIds = tableIds(text, "SC");
  if (frIds.length === 0) errors.push("정의된 FR 행이 없음");
  if (scIds.length === 0) errors.push("정의된 SC 행이 없음");

  const duplicateFr = duplicates(frIds);
  const duplicateSc = duplicates(scIds);
  if (duplicateFr.length > 0) errors.push("중복 FR 정의: " + duplicateFr.join(", "));
  if (duplicateSc.length > 0) errors.push("중복 SC 정의: " + duplicateSc.join(", "));

  const frSection = section(text, "## 6. Functional Requirements", "## 7. Success Criteria");
  for (const column of ["ID", "판정 가능한 요구사항", "우선순위", "시나리오", "화면·요소", "데이터", "관련 SC", "검증 방법"]) {
    if (!frSection.includes(column)) errors.push("6장 FR 표 열 누락: " + column);
  }
  const frRows = text.split(/\r?\n/).filter(function (line) { return /^\|\s*FR-\d{3,}\s*\|/.test(line); });
  const frDataRefs = [];
  for (const row of frRows) {
    const cells = markdownCells(row);
    if (cells.length < 8) {
      errors.push("FR 행의 열이 부족함: " + cells[0]);
      continue;
    }
    const frId = cells[0];
    const screenCell = cells[4];
    const dataCell = cells[5];
    const scCell = cells[6];
    const noScreen = /해당 없음\s*—/.test(screenCell);
    if (!noScreen && !/SCR-\d{3,}/.test(screenCell)) errors.push(frId + "에 SCR 화면 참조가 없음");
    if (!noScreen && !/SCR-\d{3,}-EL-\d{2,}/.test(screenCell)) errors.push(frId + "에 UI 요소 참조가 없음");
    if (!/(?:DATA-\d{3,}|해당 없음\s*—)/.test(dataCell)) errors.push(frId + " 데이터 열에 DATA ID 또는 해당 없음 이유가 없음");
    if (!/(?:SC-\d{3,}|해당 없음\s*—)/.test(scCell)) errors.push(frId + " 관련 SC가 없음");

    for (const screenId of references(screenCell, /SCR-\d{3,}/g)) {
      if (!detailIds.includes(screenId)) errors.push(frId + "가 정의되지 않은 화면을 참조: " + screenId);
    }
    for (const elementId of references(screenCell, /SCR-\d{3,}-EL-\d{2,}/g)) {
      if (!allElementIds.includes(elementId)) errors.push(frId + "가 정의되지 않은 UI 요소를 참조: " + elementId);
    }
    for (const scId of references(scCell, /SC-\d{3,}/g)) {
      if (!scIds.includes(scId)) errors.push(frId + "가 정의되지 않은 SC를 참조: " + scId);
    }
    frDataRefs.push(...references(dataCell, /DATA-\d{3,}/g));
  }

  const success = section(text, "## 7. Success Criteria", "## 8. Edge Cases");
  for (const column of ["ID", "소프트웨어가 보장할 기준", "관련 FR", "관련 화면", "측정 방법", "현재 PRD 데이터로 검증 가능", "라벨"]) {
    if (!success.includes(column)) errors.push("7장 SC 표 열 누락: " + column);
  }
  const scRows = text.split(/\r?\n/).filter(function (line) { return /^\|\s*SC-\d{3,}\s*\|/.test(line); });
  for (const row of scRows) {
    const cells = markdownCells(row);
    if (cells.length < 7) {
      errors.push("SC 행의 열이 부족함: " + cells[0]);
      continue;
    }
    const scId = cells[0];
    for (const frId of references(cells[2], /FR-\d{3,}/g)) {
      if (!frIds.includes(frId)) errors.push(scId + "가 정의되지 않은 FR을 참조: " + frId);
    }
    const relatedScreens = references(cells[3], /SCR-\d{3,}/g);
    if (relatedScreens.length === 0) errors.push(scId + "에 관련 화면이 없음");
    for (const screenId of relatedScreens) {
      if (!detailIds.includes(screenId)) errors.push(scId + "가 정의되지 않은 화면을 참조: " + screenId);
    }
  }

  for (const block of screenBlocks) {
    const referencedFr = references(block.body, /FR-\d{3,}/g);
    const referencedSc = references(block.body, /SC-\d{3,}/g);
    if (referencedFr.length === 0) errors.push(block.id + "에 관련 FR이 없음");
    if (referencedSc.length === 0) errors.push(block.id + "에 관련 SC가 없음");
    for (const frId of referencedFr) {
      if (!frIds.includes(frId)) errors.push(block.id + "가 정의되지 않은 FR을 참조: " + frId);
    }
    for (const scId of referencedSc) {
      if (!scIds.includes(scId)) errors.push(block.id + "가 정의되지 않은 SC를 참조: " + scId);
    }
  }

  const dataSection = section(text, "## 부록 A. 데이터 계약", "## 부록 B. 외부 사실 확인");
  const dataBlocks = blocksByHeading(dataSection, /^###\s+(DATA-\d{3,})\s+—\s+(.+)$/gm);
  const dataIds = dataBlocks.map(function (block) { return block.id; });
  const duplicateData = duplicates(dataIds);
  if (duplicateData.length > 0) errors.push("중복 DATA 정의: " + duplicateData.join(", "));

  for (const block of dataBlocks) {
    if (!block.body.includes("**저장 위치·수명:**")) errors.push(block.id + " 저장 위치·수명 누락");
    if (!block.body.includes("**접근 권한:**")) errors.push(block.id + " 접근 권한 누락");
    for (const column of ["필드", "타입", "필수", "기본값", "검증·제약", "읽기 화면·요소", "쓰기 화면·요소", "값·출처·라벨"]) {
      if (!block.body.includes(column)) errors.push(block.id + " 데이터 표 열 누락: " + column);
    }
    if (!hasTableDataRow(block.body, "필드")) errors.push(block.id + "에 데이터 필드 행이 없음");
  }

  for (const dataId of unique(elementDataRefs.concat(frDataRefs))) {
    if (!dataIds.includes(dataId)) errors.push("화면·FR이 정의되지 않은 데이터를 참조: " + dataId);
  }
  for (const dataId of dataIds) {
    if (!elementDataRefs.includes(dataId) && !frDataRefs.includes(dataId)) {
      warnings.push("화면 요소나 FR에서 참조하지 않는 데이터: " + dataId);
    }
  }

  const featureMap = section(text, "## 14. feature 분해표", "## 15. bkit 실행 명세");
  for (const column of ["feature 슬러그", "포함 화면", "포함 FR", "관련 SC", "관련 데이터", "의존", "규모", "검증 가능한 완료점"]) {
    if (!featureMap.includes(column)) errors.push("14장 feature 분해표 열 누락: " + column);
  }
  for (const screenId of detailIds) {
    if (!featureMap.includes(screenId)) errors.push("14장 feature 분해표에 없는 화면: " + screenId);
  }
  for (const frId of frIds) {
    if (!featureMap.includes(frId)) errors.push("14장 feature 분해표에 없는 FR: " + frId);
  }
  for (const scId of scIds) {
    if (!featureMap.includes(scId)) errors.push("14장 feature 분해표에 없는 SC: " + scId);
  }
  for (const dataId of dataIds) {
    if (!featureMap.includes(dataId)) errors.push("14장 feature 분해표에 없는 데이터: " + dataId);
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

  const edge = section(text, "## 8. Edge Cases", "## 9. 브랜드 & 디자인");
  for (const column of ["상황", "발생 화면·요소", "사용자 표시 문구", "이후 동작", "데이터·로그"]) {
    if (!edge.includes(column)) errors.push("8장 오류 처리 표 열 누락: " + column);
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
