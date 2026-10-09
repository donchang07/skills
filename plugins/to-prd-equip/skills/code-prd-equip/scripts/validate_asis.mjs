#!/usr/bin/env node
// code-prd-equip 현재 상태 문서(as-is-v1) 기계 검사.

import fs from "node:fs";
import path from "node:path";

const files = process.argv.slice(2);
if (files.length === 0) {
  console.error("Usage: node scripts/validate_asis.mjs <as-is file> [more files...]");
  process.exit(2);
}

const EVIDENCE = /[\w./-]+\.\w+:\d+(-\d+)?/;
const LABEL = /^\[역추출(·확인: \S+ \d{4}-\d{2}-\d{2}|·정정: \S+ \d{4}-\d{2}-\d{2})?\]/;
const CONF = new Set(["높음", "중간", "낮음"]);
const CHECK = new Set(["일치", "불일치", "대조 자료 없음"]);

function cells(line) {
  return line.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((c) => c.trim());
}

function section(text, start, endPattern) {
  const at = text.indexOf(start);
  if (at < 0) return "";
  const rest = text.slice(at + start.length);
  const end = rest.search(endPattern);
  return end < 0 ? rest : rest.slice(0, end);
}

function inspect(file) {
  const resolved = path.resolve(file);
  const text = fs.readFileSync(resolved, "utf8");
  const errors = [], warnings = [];

  if (!/^> 산출물 스키마: as-is-v1\s*$/m.test(text)) errors.push("상단 메타에 '산출물 스키마: as-is-v1'이 없음");
  for (const key of ["고객", "기준 버전", "실행 환경", "보안 등급"]) {
    const m = text.match(new RegExp("^> " + key + ": (.*)$", "m"));
    if (!m || !m[1].trim() || /\{/.test(m[1])) errors.push("메타 '" + key + "'가 비어 있음");
  }
  for (const h of ["## 2. 코드 지도", "## 3. 동결 영역 후보", "## 4. 변경 영역 항목", "## 5. 모름 목록"]) {
    if (!text.includes(h)) errors.push("필수 제목 누락: " + h);
  }
  if (/```/.test(text)) errors.push("코드 블록이 있음 — 소스를 문서로 옮기지 않는다");
  const ph = text.match(/\{[^}\n]{1,40}\}/g);
  if (ph) errors.push("placeholder가 남아 있음: " + [...new Set(ph)].slice(0, 5).join(", "));

  const ids = [];
  const frz = section(text, "## 3. 동결 영역 후보", /^## 4\. /m);
  for (const line of frz.split(/\r?\n/)) {
    const c = cells(line);
    if (!/^AS-FRZ-\d{3,}$/.test(c[0] || "")) continue;
    ids.push(c[0]);
    if (!c[2]) errors.push(c[0] + "에 경로가 없음");
    if (!EVIDENCE.test(c[4] || "")) errors.push(c[0] + "에 경로:줄 근거가 없음");
  }

  const items = section(text, "## 4. 변경 영역 항목", /^## 5\. /m);
  let header = null, count = 0, unconfirmed = 0;
  for (const line of items.split(/\r?\n/)) {
    if (!line.trim().startsWith("|")) { header = null; continue; }
    const c = cells(line);
    if (c.every((x) => /^:?-{3,}:?$/.test(x))) continue;
    if (!header) { header = c; continue; }
    const col = (n) => c[header.findIndex((h) => h === n)] || "";
    const id = c[0];
    if (!/^AS-(RCP|INS|DEF|HOST|LOG|UI)-\d{3,}$/.test(id)) { errors.push("항목 ID 형식 오류: " + id); continue; }
    ids.push(id); count++;
    const value = col("현재 값"), ev = col("근거");
    if (value === "모름") {
      if (!/^찾아본 곳:/.test(ev)) errors.push(id + " 값이 모름인데 '찾아본 곳:'이 없음");
    } else if (!EVIDENCE.test(ev)) errors.push(id + "에 경로:줄 근거가 없음");
    if (!CONF.has(col("신뢰도"))) errors.push(id + " 신뢰도가 높음·중간·낮음이 아님");
    if (!CHECK.has(col("대조"))) errors.push(id + " 대조 값이 일치·불일치·대조 자료 없음이 아님");
    if (col("대조") === "불일치" && col("신뢰도") !== "낮음") errors.push(id + " 대조 불일치인데 신뢰도가 낮음이 아님");
    if (/^\[역추출\]/.test(col("라벨")) && value !== "모름") unconfirmed++;
    if (!LABEL.test(col("라벨"))) errors.push(id + " 라벨이 [역추출] 형식이 아님");
    if (/^\[역추출·정정/.test(col("라벨")) && !/\]\s*\S/.test(col("라벨"))) errors.push(id + " 정정 라벨에 정정 값이 없음");
    if ((value.match(/;/g) || []).length > 1 || /[{}]/.test(value)) warnings.push(id + " 현재 값이 코드처럼 보임 — 한 줄 요약으로");
  }
  if (count === 0) errors.push("4장에 변경 영역 항목이 없음");

  const seen = new Set();
  for (const id of ids) { if (seen.has(id)) errors.push("ID 중복: " + id); seen.add(id); }

  if (/^> 상태: reviewed/m.test(text) && unconfirmed > 0) {
    warnings.push("상태가 reviewed인데 값이 있는 미확인 [역추출] 항목이 " + unconfirmed + "건 남아 있음");
  }
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
