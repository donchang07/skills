#!/usr/bin/env node
// docs/PRD.md(정본)에서 docs/00-pm/<feature>.prd.md 파생본을 만든다. 파생본은 직접 고치지 않는다.
import fs from "node:fs";

const src = process.argv[2] || "docs/PRD.md";
const outDir = process.argv[3] || "docs/00-pm";
const text = fs.readFileSync(src, "utf8");
fs.mkdirSync(outDir, { recursive: true });

const COMMON_SCREENS = ["SCR-005", "SCR-014"];
const ids = (s, re) => [...new Set(s.match(re) || [])];
const cells = (l) => l.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((c) => c.trim());

function sectionSplit(t) {
  const parts = t.split(/^(?=## )/m);
  return { head: parts[0], secs: parts.slice(1) };
}
const { head, secs } = sectionSplit(text);
const sec = (prefix) => secs.find((s) => s.startsWith(prefix)) || "";

const featureSec = sec("## 14.");
const featureRows = featureSec.split("\n").filter((l) => /^\|\s*\d+\s*\|/.test(l)).map(cells);
const revision = (text.match(/정본 개정: (v\d+\.\d+, [\d-]+)/) || [])[1];

const s5 = sec("## 5.");
const detailStart = s5.indexOf("### 5.5 화면 상세");
const s5Head = s5.slice(0, detailStart);
const s5Detail = s5.slice(detailStart);
const blocks = {};
const bre = /^#### (SCR-\d{3}) — .*$/gm;
let m; const marks = [];
while ((m = bre.exec(s5Detail))) marks.push([m[1], m.index]);
marks.forEach(([id, i], k) => { blocks[id] = s5Detail.slice(i, k + 1 < marks.length ? marks[k + 1][1] : undefined); });

function filterRefs(line, keepScr) {
  return line.replace(/SCR-\d{3}(-EL-\d{2})?(\(v1\))?/g, (mm) => (keepScr.has(mm.slice(0, 7)) ? mm : "")).replace(/(,\s*)+/g, ", ").replace(/,\s*\|/g, " |").replace(/\|\s*,\s*/g, "| ").replace(/·\s*,/g, "·");
}

for (const row of featureRows) {
  const slug = row[1];
  const own = ids(row[2], /SCR-\d{3}/g).filter((x) => !/해당 없음/.test(row[2]) || true);
  const ownScr = /해당 없음/.test(row[2]) && !/재검증/.test(row[2]) ? [] : ids(row[2], /SCR-\d{3}/g);
  const keepScr = new Set([...ownScr, ...COMMON_SCREENS]);
  const fr = new Set(ids(row[3], /FR-\d{3}/g));
  const sc = new Set(ids(row[4], /SC-\d{3}/g));
  for (const s of keepScr) { const b = blocks[s] || ""; ids(b, /FR-\d{3}/g).forEach((x) => fr.add(x)); ids(b, /SC-\d{3}/g).forEach((x) => sc.add(x)); }
  const allRows = text.split("\n");
  const frRows2 = allRows.filter((l) => /^\| FR-\d{3} \|/.test(l) && fr.has(cells(l)[0]));
  const keepIds = (cell, set, re) => cell.replace(re, (x) => (set.has(x) ? x : "")).replace(/(,\s*)+/g, ", ").replace(/^\s*,\s*/, " ").replace(/,\s*$/, " ");
  const fixFr = (l) => { const c = l.split("|"); const keep = /해당 없음/.test(c[5]) ? c[5] : filterRefs(c[5], keepScr); c[5] = /SCR-\d{3}/.test(keep) || /해당 없음/.test(keep) ? keep : " 해당 없음 — 이 feature 밖 화면(정본 참조) "; const k7 = keepIds(c[7], sc, /SC-\d{3}/g); c[7] = /SC-\d{3}/.test(k7) ? k7 : " 해당 없음 — 이 feature 밖 SC(정본 참조) "; return c.join("|"); };
  const fixSc = (l) => { const c = l.split("|"); c[3] = keepIds(c[3], fr, /FR-\d{3}/g); let k = filterRefs(c[4], keepScr); if (!/SCR-\d{3}/.test(k)) k = " " + [...keepScr][0] + " (정본 참조) "; c[4] = k; return c.join("|"); };

  // 5장 head: inventory/menu/auth rows filtered
  const s5h = s5Head.split("\n").filter((l) => {
    if (/^\| SCR-\d{3} \|/.test(l)) return keepScr.has(cells(l)[0]);
    if (/^\| NAV-\d{3} \|/.test(l)) { const t = ids(cells(l)[4], /SCR-\d{3}/g); return t.some((x) => keepScr.has(x)); }
    return true;
  }).map((l) => (/^\| SCR-\d{3} \|/.test(l) ? l : filterRefs(l, keepScr))).join("\n");
  const detail = "### 5.5 화면 상세\n\n" + [...keepScr].sort().map((s) => blocks[s]).join("");

  const s6 = sec("## 6.");
  const s6New = s6.split("\n").filter((l) => !/^\| FR-\d{3} \|/.test(l) || fr.has(cells(l)[0])).map((l) => (/^\| FR-\d{3} \|/.test(l) ? fixFr(l) : l)).join("\n");
  const s7 = sec("## 7.");
  const s7New = s7.split("\n").filter((l) => !/^\| SC-\d{3} \|/.test(l) || sc.has(cells(l)[0])).map((l) => (/^\| SC-\d{3} \|/.test(l) ? fixSc(l) : l)).join("\n");
  const s8 = sec("## 8.");
  const s8New = s8.split("\n").filter((l) => { if (!/^\| /.test(l) || /^\| 상황/.test(l) || /^\|---/.test(l)) return true; const r = ids(cells(l)[1], /SCR-\d{3}/g); return r.length === 0 || r.some((x) => keepScr.has(x)); }).join("\n");

  const usedData = new Set();
  [detail, ...frRows2].forEach((x) => ids(x, /DATA-\d{3}/g).forEach((d) => usedData.add(d)));
  ids(row[5], /DATA-\d{3}/g).forEach((d) => usedData.add(d));
  const sA = sec("## 부록 A.");
  const aParts = sA.split(/^(?=### DATA-)/m);
  const aNew = aParts[0] + aParts.slice(1).filter((p) => usedData.has(p.slice(4, 12))).map((p) => p.split("\n").map((l) => (/^\| [a-z_·]+ \|/.test(l) ? filterRefs(l, keepScr) : l)).join("\n")).join("");

  const newHead = head
    .replace(/^# PRD — .*$/m, "# PRD — AX Assessment · " + slug)
    .replace(/^> 문서 역할: .*$/m, "> 문서 역할: feature projection")
    .replace(/^> feature: .*$/m, "> feature: " + slug)
    .replace(/^> 게이트: .*$/m, "> 게이트: docs/00-pm/" + slug + ".gate.md 참조 · 정본 게이트 docs/00-pm/_product.gate.md")
    + "> 생성: scripts/project_features.mjs가 정본 " + revision + "에서 생성. 직접 고치지 말 것. 이 feature 밖 화면 참조는 정본(docs/PRD.md)을 따른다\n\n";

  const keep = (p) => sec(p);
  const out = [newHead, keep("## 0."), keep("## 1."), keep("## 2."), keep("## 3."), keep("## 4."), s5h + detail, s6New, s7New, s8New, keep("## 9."), keep("## 10."), keep("## 11."), keep("## 12."), keep("## 13."), featureSec, keep("## 15."), aNew, keep("## 부록 B.")].join("");
  fs.writeFileSync(`${outDir}/${slug}.prd.md`, out);
  console.log(slug, "screens", [...keepScr].join(","), "FR", fr.size, "SC", sc.size, "DATA", usedData.size);
}
