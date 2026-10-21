#!/usr/bin/env node
// to-prd 실행 뒤 산출물 묶음이 서로 맞는지 검사한다. PRD 한 파일의 형식은 validate_prd.mjs가 본다.
// 사용: node scripts/check_output.mjs <프로젝트 루트>

import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const skillRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const project = path.resolve(process.argv[2] || ".");
const docs = path.join(project, "docs");
const pm = path.join(docs, "00-pm");
const results = [];
const check = (name, ok, detail = "") => results.push({ name, ok: Boolean(ok), detail });
const exists = (p) => fs.existsSync(p);
const read = (p) => (exists(p) ? fs.readFileSync(p, "utf8") : "");

const finalPath = path.join(docs, "PRD.md");
const draftPath = path.join(docs, "PRD.draft.md");
const isFinal = exists(finalPath);
const prdPath = isFinal ? finalPath : draftPath;
check("정본 또는 draft 존재", exists(prdPath), path.relative(project, prdPath));
if (!exists(prdPath)) finish();

const prd = read(prdPath);
const revision = (prd.match(/^> 정본: docs\/PRD\.md · 정본 개정: (v\d+\.\d+)/m) || [])[1];
const mode = (prd.match(/^> 작성 모드: (Full|Lean|변경 노트)/m) || [])[1];
check("정본 개정 메타", revision, revision || "없음");
check("작성 모드 메타", mode, mode || "없음");

function section(text, start, end) {
  const i = text.indexOf(start);
  if (i < 0) return "";
  const j = end ? text.indexOf(end, i + start.length) : -1;
  return j < 0 ? text.slice(i) : text.slice(i, j);
}

let validateOk = false;
let validateOut = "";
try {
  validateOut = execFileSync(process.execPath, [path.join(skillRoot, "scripts/validate_prd.mjs"), prdPath], { encoding: "utf8" });
  validateOk = true;
} catch (error) {
  validateOut = String(error.stdout || error.message);
}
const summary = (validateOut.match(/Summary: [^\n]+/) || [""])[0];
check("정본 기계 검사 ERROR 0", isFinal ? validateOk : true, isFinal ? summary : "draft라 생략");

const htmlPath = path.join(docs, isFinal ? "PRD.html" : "PRD.draft.html");
check("읽기용 HTML", exists(htmlPath), path.relative(project, htmlPath));

const featureTable = section(prd, "## 14. feature 분해표", "## 15. bkit 실행 명세");
const slugs = [...featureTable.matchAll(/^\|\s*\d+\s*\|\s*([a-z0-9]+(?:-[a-z0-9]+)*)\s*\|/gm)].map((m) => m[1]);
check("14장 feature 슬러그", slugs.length > 0, slugs.join(", ") || "없음");
for (const slug of slugs) {
  const candidates = isFinal
    ? [path.join(pm, slug + ".prd.md"), path.join(pm, "features", slug + ".prd.md")]
    : [path.join(pm, slug + ".prd.draft.md")];
  const featurePath = candidates.find(exists);
  check(`feature 파생본: ${slug}`, featurePath, featurePath ? path.relative(project, featurePath) : candidates.map((c) => path.relative(project, c)).join(" 또는 "));
  if (featurePath) {
    const feature = read(featurePath);
    const featureRevision = (feature.match(/정본 개정: (v\d+\.\d+)/) || [])[1];
    check(`파생본 개정 일치: ${slug}`, featureRevision === revision, `${featureRevision || "없음"} / 정본 ${revision}`);
    check(`파생본 비목표 포함: ${slug}`, feature.includes("### 비목표 (Non-goals)"));
  }
  const gate = path.join(pm, slug + (isFinal ? ".gate.md" : ".gate.draft.md"));
  check(`feature gate: ${slug}`, exists(gate), path.relative(project, gate));
}

const productGatePath = path.join(pm, isFinal ? "_product.gate.md" : "_product.gate.draft.md");
const productGate = read(productGatePath);
check("제품 gate", productGate, path.relative(project, productGatePath));
check("gate에 검토 방식 기록", /검토 방식/.test(productGate));
check("gate에 HG-15까지 결과", /HG-15/.test(productGate));
check("_decisions.md", exists(path.join(pm, "_decisions.md")));

const workspace = path.join(pm, "_workspace");
check("작업 메모 01_mapping.md", exists(path.join(workspace, "01_mapping.md")));
check("기계 검사 기록 02_validate.txt", exists(path.join(workspace, "02_validate.txt")));
const reviews = exists(workspace) ? fs.readdirSync(workspace).filter((f) => /^03_review_.+\.md$/.test(f)) : [];
const singleSession = /단일 세션 역할 전환/.test(productGate);
const minReviews = mode === "Full" ? 4 : mode === "Lean" ? 2 : 1;
check("검토자별 결과 03_review_*", singleSession || reviews.length >= minReviews, `${reviews.length}개 (모드 ${mode} 최소 ${minReviews}${singleSession ? ", 단일 세션" : ""})`);

const claude = read(path.join(project, "CLAUDE.md"));
const block = (claude.match(/<!-- to-prd:begin[\s\S]*?<!-- to-prd:end -->/) || [""])[0];
if (isFinal) {
  check("CLAUDE.md to-prd 블록", block);
  check("블록 개정 = 정본 개정", revision && block.includes(revision), revision);
  const testLine = (section(prd, "### 11.1 레벨·스택", "### 11.2").match(/\*\*테스트:\*\*[^\n]*/) || [""])[0];
  const commands = [...testLine.matchAll(/`([^`]+)`/g)].map((m) => m[1]);
  check("블록에 11.1 테스트 명령", commands.length > 0 && commands.every((c) => block.includes(c)), commands.join(" · ") || "11.1 명령 없음");
  const ai = section(prd, "### 11.4 AI 판정 계약", "### 11.5");
  const aiUsed = /^\|\s*(?!AI 기능|-)[^|\s][^|]*\|/m.test(ai) && !/해당 없음\s*—\s*브리프/.test(ai.split("\n").slice(1, 4).join(" "));
  if (aiUsed) {
    const evalLine = (section(prd, "### 11.1 레벨·스택", "### 11.2").match(/\*\*AI 평가:\*\*[^\n]*/) || [""])[0];
    const evalCommands = [...evalLine.matchAll(/`([^`]+)`/g)].map((m) => m[1]).filter((c) => !c.includes("/"));
    check("블록에 AI 평가 명령과 세 번째 관문", evalCommands.some((c) => block.includes(c)) && /세 번째 관문|금지 행동 0건/.test(block), evalCommands.join(" · ") || "11.1 평가 명령 없음");
  }
} else {
  check("draft일 때 CLAUDE.md 블록이 draft를 가리키지 않음", !/PRD\.draft/.test(block));
}

const changeLog = section(prd, "## 부록 C. 변경 이력과 영향");
check("부록 C에 이번 개정 행", revision && new RegExp("^\\|\\s*" + revision.replace(".", "\\.") + "\\b", "m").test(changeLog), revision);

finish();

function finish() {
  let fail = 0;
  for (const r of results) {
    if (!r.ok) fail += 1;
    console.log(`${r.ok ? "PASS" : "FAIL"} ${r.name}${r.detail ? " — " + r.detail : ""}`);
  }
  console.log(`Summary: PASS ${results.length - fail}, FAIL ${fail}`);
  process.exit(fail ? 1 : 0);
}
