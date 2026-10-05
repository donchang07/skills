#!/usr/bin/env node
// 템플릿(Word)·핸드북(Word)·to-prd 스킬이 같은 버전과 같은 규칙을 가리키는지 검사한다.
// 사용: node scripts/check_sync.mjs   (스킬 폴더에서 실행, unzip 필요)

import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const read = (rel) => fs.readFileSync(path.join(root, rel), "utf8");
const results = [];
const check = (id, ok, detail) => results.push({ id, ok: Boolean(ok), detail });

function docx(rel) {
  const file = path.join(root, rel);
  const part = (name) => {
    try { return execFileSync("unzip", ["-p", file, name], { encoding: "utf8", maxBuffer: 64 << 20, stdio: ["ignore", "pipe", "ignore"] }); }
    catch { return ""; }
  };
  const text = (xml) => xml
    .replace(/<w:tab\/>/g, " ")
    .replace(/<\/w:p>/g, "\n")
    .replace(/<[^>]+>/g, "")
    .replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">");
  const xml = part("word/document.xml");
  const headings = [];
  for (const p of xml.match(/<w:p[ >][\s\S]*?<\/w:p>/g) || []) {
    if (/w:pStyle w:val="Heading1"/.test(p)) headings.push(text(p).trim());
  }
  return {
    body: text(xml),
    footer: text(part("word/footer1.xml")),
    title: (part("docProps/core.xml").match(/<dc:title>([^<]*)/) || [])[1] || "",
    headings
  };
}

const skill = read("SKILL.md");
const mapping = read("references/brief-mapping.md");
const prdTemplate = read("assets/prd-template.md");
const gate = read("references/gate-checklist.md");
const bkit = read("references/bkit-contract.md");
const validator = read("scripts/validate_prd.mjs");

// 1. 버전
const version = (mapping.match(/브리프 버전: (v\d+\.\d+)/) || [])[1];
check("V-01 매핑 문서에 브리프 버전 선언", version, version || "없음");
const tplRel = `assets/brief/PRD템플릿_${version}.docx`;
const hbRel = `assets/brief/PRD작성핸드북_${version}.docx`;
check("V-02 템플릿 파일 존재", fs.existsSync(path.join(root, tplRel)), tplRel);
check("V-03 핸드북 파일 존재", fs.existsSync(path.join(root, hbRel)), hbRel);
const others = fs.readdirSync(path.join(root, "assets/brief")).filter((f) => f.endsWith(".docx") && !f.includes(`_${version}.`));
check("V-04 다른 버전 docx가 남아 있지 않음", others.length === 0, others.join(", ") || "없음");
if (!fs.existsSync(path.join(root, tplRel)) || !fs.existsSync(path.join(root, hbRel))) report();

const tpl = docx(tplRel);
const hb = docx(hbRel);
check("V-05 템플릿 바닥글 없음", tpl.footer.trim() === "", tpl.footer.trim() || "없음");
check("V-06 템플릿 파일 속성 제목 버전", tpl.title.includes(version), tpl.title);
check("V-07 핸드북 바닥글 없음", hb.footer.trim() === "", hb.footer.trim() || "없음");
check("V-08 핸드북 파일 속성 제목 버전", hb.title.includes(version), hb.title);
const hbTplVersions = [...new Set((hb.body.match(/PRD템플릿[ _](v\d+\.\d+)/g) || []).map((m) => m.slice(-4)))];
check("V-09 핸드북이 가리키는 템플릿 버전", hbTplVersions.length === 1 && hbTplVersions[0] === version, hbTplVersions.join(", "));
check("V-10 SKILL.md가 두 파일을 같은 버전으로 참조",
  skill.includes(`PRD템플릿_${version}.docx`) && skill.includes(`PRD작성핸드북_${version}.docx`), version);

// 2. 스키마·bkit
const schema = (mapping.match(/PRD 스키마: (screen-first-v\d+)/) || [])[1];
check("S-01 스키마: 매핑 = PRD 템플릿 = 핸드북 = 검증기",
  schema && prdTemplate.includes(`PRD 스키마: ${schema}`) && hb.body.includes(schema) && validator.includes(schema), schema);
const hbBkit = (hb.body.match(/bkit 검증 기준 (v\d+\.\d+\.\d+)/) || [])[1];
check("S-02 핸드북 bkit 버전이 bkit-contract에 있음", hbBkit && bkit.includes(hbBkit), hbBkit || "없음");

// 3. 템플릿 구조 ↔ 매핑
const mapped = new Set([...mapping.matchAll(/^\| ([^|]+?) \|/gm)].map((m) => m[1].trim()));
const missingMap = tpl.headings.filter((h) => !mapped.has(h));
check("T-01 템플릿 장이 모두 대응표에 있음", missingMap.length === 0, missingMap.join(", ") || `${tpl.headings.length}개 장`);
const extraMap = [...mapped].filter((h) => /^(기본 정보|\d+ )/.test(h) && !tpl.headings.includes(h));
check("T-02 대응표에 템플릿에 없는 장이 없음", extraMap.length === 0, extraMap.join(", ") || "없음");
const required = (tpl.body.match(/필수 항목\s+(.+?)은 반드시 작성하십시오/) || [])[1];
check("T-03 필수 항목 목록이 템플릿과 매핑에서 같음", required && mapping.includes(`**${required}**`), required || "템플릿에서 찾지 못함");
const states = ["처리 중", "데이터 없음", "입력 오류", "시스템 오류", "권한 없음", "오프라인", "취소 반려 이탈"];
const stateMiss = states.filter((s) => !tpl.body.includes(s) || !mapping.includes(`| ${s} |`));
check("T-04 템플릿 화면 상태가 모두 매핑됨", stateMiss.length === 0, stateMiss.join(", ") || "7개");
for (const label of ["이번에 만들지 않을 것", "나중에 추가할 것", "사용할 AI 기능", "평소와 다른 흐름", "참고할 화면이나 디자인"]) {
  check(`T-05 템플릿 항목 '${label}' ↔ 매핑`, tpl.body.includes(label) && mapping.includes(label), label);
}

// 4. 규칙 일치
const ids = [...new Set((prdTemplate.match(/\b(SCR|NAV|DATA|FR|SC|REF|NG)-\d{3}/g) || []).map((m) => m.split("-")[0]))].concat(["EL"]);
const hbIdTable = hb.body.slice(hb.body.indexOf("ID의 의미"), hb.body.indexOf("FR SC와 화면 중심 계약"));
const idMiss = ids.filter((id) => !new RegExp(`(^|\\n)${id}\\n`).test(hbIdTable));
check("R-01 PRD ID 체계가 핸드북 ID 표에 모두 있음", idMiss.length === 0, idMiss.join(", ") || ids.join(" "));
check("R-02 게이트 기준 90점·70점 일치",
  /90점 이상/.test(hb.body) && /70점 이상/.test(hb.body) && /Blocker 0, 90점 이상/.test(gate) && /70~89점/.test(gate), "90 / 70");
check("R-03 비목표 Blocker 규칙: 핸드북 ↔ 게이트 HG-14",
  hb.body.includes("이번에 만들지 않을 것을 구현하는 FR이나 화면이 있어도 Blocker") && gate.includes("| HG-14 |"), "HG-14");
check("R-04 AI 결과·사람 확정값 분리: 템플릿 ↔ 핸드북 ↔ 스킬",
  tpl.body.includes("AI 결과와 사람이 확정한 값은 따로 저장") && hb.body.includes("AI 결과와 사람 확정값을 나눠 저장") &&
  skill.includes("AI 판정 계약") && prdTemplate.includes("### 11.4 AI 판정 계약"), "11.4");
check("R-05 모름 처리: 템플릿 ↔ 핸드북 ↔ 매핑",
  tpl.body.includes("필수 항목을 모름으로 두면 to-prd가 객관식으로 다시 묻고") &&
  hb.body.includes("객관식으로 최대 4문항") && mapping.includes("최대 4문항") && skill.includes("최대 4문항"), "최대 4문항");
check("R-06 다시 검토할 시점: 템플릿 ↔ PRD 템플릿",
  tpl.body.includes("다시 검토할 시점") && prdTemplate.includes("다시 검토할 시점"), "NG 열");
for (const term of ["/pdca plan", "Pretendard", "Playwright", "data-testid", "match rate", "docs/PRD.html", "_decisions.md", "CLAUDE.md", "screen-first-v2"]) {
  check(`R-07 공통 용어 '${term}' (핸드북·스킬)`, hb.body.includes(term) && (skill.includes(term) || validator.includes(term)), term);
}
const hbOutputs = (hb.body.match(/docs\/[\w./-]+|CLAUDE\.md/g) || []).filter((p) => /\.(md|html)$/.test(p));
const outMiss = [...new Set(hbOutputs)].filter((p) => !skill.includes(p.replace("feature.", "{feature}.").replace("00-pm/feature", "00-pm/{feature}")));
check("R-08 핸드북 산출물 경로가 SKILL.md에 있음", outMiss.length === 0, outMiss.join(", ") || `${new Set(hbOutputs).size}개`);
check("R-09 실행 문구의 템플릿 파일명 버전", hb.body.includes(`PRD템플릿_${version}.docx`), `PRD템플릿_${version}.docx`);
const ask = "필수 항목이 비었으면 객관식으로 묻고, 작성자 결정이 필요한 항목은 D 번호로 정리해줘.";
const askCount = (t) => t.split(ask).length - 1;
check("R-10 실행 문구의 질문·결정 처리 (템플릿 2개 = 핸드북 2개)", askCount(tpl.body) === 2 && askCount(hb.body) === 2, `템플릿 ${askCount(tpl.body)} · 핸드북 ${askCount(hb.body)}`);
check("R-11 _interview.md: 핸드북 산출물 ↔ 스킬 ↔ 매핑", hb.body.includes("_interview.md") && skill.includes("_interview.md") && mapping.includes("_interview.md"), "_interview.md");
check("R-12 NG가 HTML 링크 대상", read("scripts/render_prd_html.mjs").includes("NG-\\d{3,}"), "render_prd_html.mjs");

report();

function report() {
  let fail = 0;
  for (const r of results) {
    if (!r.ok) fail += 1;
    console.log(`${r.ok ? "PASS" : "FAIL"}  ${r.id} — ${r.detail}`);
  }
  console.log(`\nSummary: PASS ${results.length - fail}, FAIL ${fail}`);
  process.exit(fail > 0 ? 1 : 0);
}
