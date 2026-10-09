#!/usr/bin/env node
// to-prd-equip PRD(change-area-v1) 기계 검사. 판정은 gate-checklist.md의 Hard Gate가 정한다.

import fs from "node:fs";
import path from "node:path";

const files = process.argv.slice(2);
if (files.length === 0) {
  console.error("Usage: node scripts/validate_prd.mjs <PRD file> [additional PRD files...]");
  process.exit(2);
}

const requiredHeadings = [
  "## 0. Executive Summary",
  "## 3. 목표 (Goals)",
  "## 4. 운영 시나리오",
  "## 5. 변경 영역 계약 (Change-Area Contract)",
  "### 5.1 동결 영역",
  "### 5.2 변경 영역 인벤토리",
  "### 5.8 장비 상태 매트릭스",
  "### 5.10 증분 계약",
  "## 6. Functional Requirements",
  "## 7. Success Criteria",
  "## 9. 시험 데이터·회귀 기준",
  "## 11. Assumptions",
  "### 11.1 장비·시험 체계",
  "### 11.2 시스템 가정 10칸",
  "## 13. 작성자 결정 요청 [작성자]",
  "## 14. feature 분해표",
  "## 15. bkit 실행 명세"
];

const AREA = ["RCP", "INS", "DEF", "HOST", "LOG", "UI"];
const AREA_ID = new RegExp("\\b(?:" + AREA.join("|") + ")-\\d{3,}\\b", "g");
const LABEL = /^\[(골든|가상호스트|HIL|단위|현장|수동)\]/;

function section(text, start, endPattern) {
  const at = text.indexOf(start);
  if (at < 0) return "";
  const rest = text.slice(at + start.length);
  const end = rest.search(endPattern);
  return end < 0 ? rest : rest.slice(0, end);
}

function cells(line) {
  return line.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((c) => c.trim());
}

// 첫 표의 머리글과 데이터 행을 돌려준다. 구분선 행은 건너뛴다.
function tables(text) {
  const out = [];
  let current = null;
  for (const line of text.split(/\r?\n/)) {
    if (!line.trim().startsWith("|")) { current = null; continue; }
    const row = cells(line);
    if (row.every((c) => /^:?-{3,}:?$/.test(c))) continue;
    if (!current) { current = { header: row, rows: [] }; out.push(current); continue; }
    current.rows.push(row);
  }
  return out;
}

function col(table, name) {
  return table.header.findIndex((h) => h.includes(name));
}

function dup(values) {
  const seen = new Set(), d = new Set();
  for (const v of values) (seen.has(v) ? d : seen).add(v);
  return [...d];
}

function prefix(glob) {
  return glob.replace(/`/g, "").replace(/\*\*.*$/, "").replace(/\*.*$/, "").replace(/\/+$/, "").trim();
}

function paths(cell) {
  return cell.split(/[,·;]|<br>/).map(prefix).filter((p) => p && !/^해당 없음/.test(p));
}

function overlaps(a, b) {
  return a === b || a.startsWith(b + "/") || b.startsWith(a + "/");
}

function inspect(file) {
  const resolved = path.resolve(file);
  const text = fs.readFileSync(resolved, "utf8");
  const errors = [], warnings = [];

  if (!/^> PRD 스키마: change-area-v1\s*$/m.test(text)) errors.push("상단 메타에 'PRD 스키마: change-area-v1'이 없음");
  for (const h of requiredHeadings) if (!text.includes(h)) errors.push("필수 제목 누락: " + h);

  // 계약 섹션(4~10장)의 placeholder
  const contract = section(text, "## 4. 운영 시나리오", /^## 11\. /m);
  const ph = contract.match(/\{[^}\n]{1,40}\}/g);
  if (ph) errors.push("4~10장에 placeholder가 남아 있음: " + [...new Set(ph)].slice(0, 5).join(", "));

  // 5.1 동결 영역
  const frzTable = tables(section(text, "### 5.1 동결 영역", /^### 5\.2 /m))[0];
  const frzPaths = [];
  if (!frzTable || frzTable.rows.length === 0) {
    errors.push("5.1 동결 영역 표가 비어 있음 (HG-E02)");
  } else {
    const pi = col(frzTable, "모듈·경로");
    for (const r of frzTable.rows) {
      if (!/^FRZ-\d{3,}$/.test(r[0])) continue;
      if (r.slice(1).some((c) => !c)) errors.push(r[0] + " 동결 영역 행에 빈 칸이 있음 (HG-E02)");
      if (pi >= 0) frzPaths.push(...paths(r[pi]).map((p) => ({ id: r[0], p })));
    }
    const ids = frzTable.rows.map((r) => r[0]).filter((v) => /^FRZ-/.test(v));
    const d = dup(ids); if (d.length) errors.push("FRZ ID 중복: " + d.join(", "));
  }

  // 5.2 인벤토리와 5.3~5.7 상세
  const invTable = tables(section(text, "### 5.2 변경 영역 인벤토리", /^### 5\.3 /m))[0];
  const inventory = invTable ? invTable.rows.map((r) => r[0]).filter((v) => v.match(AREA_ID)) : [];
  if (inventory.length === 0) errors.push("5.2 변경 영역 인벤토리에 항목이 없음 (HG-E03)");
  const di = dup(inventory); if (di.length) errors.push("인벤토리 ID 중복: " + di.join(", "));
  const p0Items = invTable ? invTable.rows.filter((r) => /P0/.test(r[col(invTable, "우선순위")] || "")).map((r) => r[0]) : [];

  const detailText = section(text, "### 5.3 ", /^### 5\.8 /m);
  const details = new Map();
  for (const t of tables(detailText)) {
    for (const r of t.rows) {
      if (!r[0].match(AREA_ID)) continue;
      if (details.has(r[0])) errors.push("상세 표 ID 중복: " + r[0]);
      details.set(r[0], { row: r, t });
    }
  }
  for (const id of inventory) if (!details.has(id)) errors.push(id + " 인벤토리에 있으나 5.3~5.7 상세 행이 없음 (HG-E03)");
  for (const id of details.keys()) if (!inventory.includes(id)) errors.push(id + " 상세에 있으나 5.2 인벤토리에 없음 (HG-E01)");
  const changed = new Set(), extracted = [];
  for (const [id, { row, t }] of details) {
    for (const name of ["근거", "허용 경로"]) {
      const i = col(t, name);
      if (i < 0 || !row[i]) errors.push(id + " 상세에 '" + name + "' 값이 없음 (HG-E03)");
    }
    const cur = col(t, "현재"), tgt = col(t, "목표");
    if (cur >= 0 && tgt >= 0 && row[cur] !== row[tgt]) changed.add(id);
    if (cur >= 0 && /\[역추출\]/.test(row[cur] || "")) extracted.push(id);
  }

  // 6장 FR
  const frTable = tables(section(text, "## 6. Functional Requirements", /^### 6\.x |^## 7\. /m))[0];
  const frIds = [], frItems = new Map();
  if (!frTable) errors.push("6장 FR 표가 없음");
  else {
    const iItem = col(frTable, "영역 항목"), iPath = col(frTable, "허용 경로"), iSc = col(frTable, "관련 SC"), iVer = col(frTable, "검증 방법"), iPri = col(frTable, "우선순위");
    for (const r of frTable.rows) {
      if (!/^FR-\d{3,}$/.test(r[0])) continue;
      const id = r[0]; frIds.push(id);
      const items = (r[iItem] || "").match(AREA_ID) || [];
      frItems.set(id, items);
      const p0 = /P0/.test(r[iPri] || "");
      if (items.length === 0 && !/^공통\s*—/.test(r[iItem] || "")) (p0 ? errors : warnings).push(id + "에 영역 항목이 없음 (HG-E06)");
      for (const it of items) if (!inventory.includes(it)) errors.push(id + "가 없는 항목 " + it + "를 참조 (HG-E01)");
      if (!r[iPath]) (p0 ? errors : warnings).push(id + "에 허용 경로가 없음 (HG-E06)");
      for (const p of paths(r[iPath] || "")) for (const f of frzPaths) if (overlaps(p, f.p)) errors.push(id + " 허용 경로 " + p + "가 " + f.id + " 동결 경로와 겹침 (HG-E04)");
      if (!/SC-\d{3,}/.test(r[iSc] || "")) (p0 ? errors : warnings).push(id + "에 관련 SC가 없음 (HG-E06)");
      if (!LABEL.test(r[iVer] || "")) errors.push(id + " 검증 방법이 시험 수단 라벨로 시작하지 않음");
    }
    const d = dup(frIds); if (d.length) errors.push("FR ID 중복: " + d.join(", "));
  }
  const frCovered = new Set([...frItems.values()].flat());
  for (const id of changed) if (!frCovered.has(id)) errors.push(id + "는 현재 값과 목표 값이 다르지만 FR이 없음");
  for (const id of p0Items) if (!frCovered.has(id)) errors.push("P0 항목 " + id + "에 FR이 없음 (HG-E06)");
  for (const id of extracted) (frCovered.has(id) ? errors : warnings).push(id + " 현재 값이 확인되지 않은 [역추출] (HG-E09)");

  // 7장 SC와 시험 수단 규칙
  const scTable = tables(section(text, "## 7. Success Criteria", /^## 8\. /m))[0];
  const scIds = [], byItem = new Map();
  if (!scTable) errors.push("7장 SC 표가 없음");
  else {
    const iItem = col(scTable, "관련 항목"), iM = col(scTable, "측정 방법");
    for (const r of scTable.rows) {
      if (!/^SC-\d{3,}$/.test(r[0])) continue;
      scIds.push(r[0]);
      const label = (r[iM] || "").match(LABEL);
      if (!label) { errors.push(r[0] + " 측정 방법이 시험 수단 라벨로 시작하지 않음"); continue; }
      if (label[1] === "현장" && !/이유|재현 불가|재현할 수 없/.test(r[iM])) errors.push(r[0] + " [현장]인데 사무실 재현 불가 이유가 없음 (HG-E10)");
      for (const it of (r[iItem] || "").match(AREA_ID) || []) {
        if (!byItem.has(it)) byItem.set(it, new Set());
        byItem.get(it).add(label[1]);
      }
    }
    const d = dup(scIds); if (d.length) errors.push("SC ID 중복: " + d.join(", "));
  }
  for (const id of frCovered) {
    const labels = byItem.get(id) || new Set();
    if (/^(RCP|INS|DEF)-/.test(id) && !labels.has("골든")) errors.push(id + " 판정 영향 항목에 [골든] SC가 없음 (HG-E07)");
    if (/^(HOST|LOG)-/.test(id) && !labels.has("가상호스트")) errors.push(id + " 호스트·물류 항목에 [가상호스트] SC가 없음 (HG-E08)");
  }
  for (const r of frTable ? frTable.rows : []) {
    for (const sc of (r.join(" ").match(/SC-\d{3,}/g) || [])) if (!scIds.includes(sc)) errors.push(r[0] + "가 없는 " + sc + "를 참조 (HG-E01)");
  }

  // 5.10 증분 계약
  const inc = section(text, "### 5.10 증분 계약", /^## 6\. /m);
  for (const k of ["기준 버전", "허용 경로", "동결 경로", "롤백"]) {
    const t = tables(inc)[0];
    const row = t && t.rows.find((r) => r[0] === k);
    if (!row || !row[1]) errors.push("5.10 증분 계약에 '" + k + "'이 없음 (HG-E13)");
  }

  // 11.1·11.2
  const a111 = section(text, "### 11.1 장비·시험 체계", /^### 11\.2 /m);
  for (const l of ["[단위]", "[골든]", "[가상호스트]"]) if (!a111.includes(l)) errors.push("11.1 시험 체계에 " + l + " 명령이 없음 (HG-E11)");
  const a112 = tables(section(text, "### 11.2 시스템 가정 10칸", /^### 11\.3 /m))[0];
  const nums = a112 ? a112.rows.map((r) => r[0]) : [];
  for (let n = 1; n <= 10; n++) if (!nums.includes(String(n))) errors.push("11.2 시스템 가정 " + n + "번 행 누락 (HG-E11)");
  const baseRow = a112 && a112.rows.find((r) => r[0] === "1");
  if (/고객 정본/.test(text.match(/^> 문서 역할:.*$/m)?.[0] || "") && baseRow && !/\[확정/.test(baseRow[3] || "")) errors.push("고객 정본인데 11.2 #1 기준 버전이 [확정]이 아님 (HG-E05)");

  // 14장 feature 분해
  const feat = section(text, "## 14. feature 분해표", /^## 15\. /m);
  for (const id of frIds) if (!feat.includes(id)) errors.push(id + "가 14장 feature 분해표에 없음 (HG-E01)");

  // 15장 세 관문
  const b15 = section(text, "## 15. bkit 실행 명세", /^## 부록/m);
  const done = (b15.match(/^- \*\*완료:\*\*.*$/m) || [""])[0];
  if (!done) errors.push("15장에 '- **완료:**' 줄이 없음 (HG-E12)");
  if (!/match rate/i.test(done)) errors.push("15장 완료 조건에 match rate 관문이 없음 (HG-E12)");
  if (!/11\.1 시험/.test(done)) errors.push("15장 완료 조건에 11.1 시험 통과 관문이 없음 (HG-E12)");
  if (!/범위 감시/.test(done)) errors.push("15장 완료 조건에 범위 감시 관문이 없음 (HG-E12)");
  if (!b15.includes("matchRateThreshold")) errors.push("15장에 matchRateThreshold 설정이 없음");

  // 3장 비목표
  const ng = section(text, "### 비목표 (Non-goals)", /^## 4\. /m);
  const ngIds = (ng.match(/^\|\s*NG-\d{3,}/gm) || []).map((s) => s.replace(/^\|\s*/, ""));
  if (ngIds.length === 0) warnings.push("3장 비목표 NG-* 표가 없음");
  const dn = dup(ngIds); if (dn.length) errors.push("NG ID 중복: " + dn.join(", "));

  if (resolved.includes(path.join("docs", "00-pm")) && !/^> 제품 정본: docs\/PRD\.md/m.test(text)) errors.push("feature 파생본에 제품 정본 경로·개정 메타가 없음");

  return { file: resolved, errors, warnings };
}

let totalErrors = 0, totalWarnings = 0;
for (const file of files) {
  const r = inspect(file);
  console.log("\n" + r.file);
  for (const m of r.errors) console.log("ERROR " + m);
  for (const m of r.warnings) console.log("WARN  " + m);
  if (r.errors.length === 0 && r.warnings.length === 0) console.log("PASS  기계 검사 통과");
  totalErrors += r.errors.length;
  totalWarnings += r.warnings.length;
}
console.log("\nSummary: ERROR " + totalErrors + ", WARN " + totalWarnings + ", FILES " + files.length);
if (totalErrors > 0) process.exitCode = 1;
