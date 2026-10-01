#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const input = process.argv[2] || "docs/PRD.md";
const output = process.argv[3] || input.replace(/\.md$/i, ".html");

if (!fs.existsSync(input)) {
  console.error("Usage: node scripts/render_prd_html.mjs <PRD.md> [PRD.html]");
  process.exit(2);
}

const source = fs.readFileSync(input, "utf8").replace(/\r\n/g, "\n");
const lines = source.split("\n");

const ID_PATTERN = /\b(SCR-\d{3,}(?:-EL-\d{2,})?|FR-\d{3,}|SC-\d{3,}|DATA-\d{3,}|NAV-\d{3,}|REF-\d{3,}|D-\d{3,}|I-\d{3,})((?:\.[A-Za-z_][\w]*)?)/g;
const TEST_LABEL = /\[(E2E|통합|단위|수동)\]/g;
const STATUS_LABEL = /\[(확정·출처|확정|조사·기준일|추정|가설|기본값|해당 없음|결정 필요|구현자|작성자)\]/g;

function escapeHtml(value) {
  return value.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function anchorOf(id) {
  return id.toLowerCase();
}

function cells(line) {
  return line.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map(function (cell) { return cell.trim(); });
}

function isSeparator(line) {
  const parts = cells(line);
  return parts.length > 0 && parts.every(function (cell) { return /^:?-{3,}:?$/.test(cell); });
}

function headingAnchor(text) {
  const id = text.match(/^(SCR-\d{3,}|DATA-\d{3,})\b/);
  if (id) return anchorOf(id[1]);
  const scenario = text.match(/^Scenario\s+(S\d+)/);
  if (scenario) return "scenario-" + scenario[1].toLowerCase();
  const numbered = text.match(/^(\d+(?:\.\d+)*|부록 [A-Z])\.?\s/);
  if (numbered) return "s-" + numbered[1].replace(/\./g, "-").replace(/\s/g, "").toLowerCase();
  return "h-" + Buffer.from(text).toString("hex").slice(0, 16);
}

const anchors = new Set();
for (const line of lines) {
  const heading = line.match(/^#{2,6}\s+(.*)$/);
  if (heading) anchors.add(headingAnchor(heading[1].trim()));
  const row = line.match(/^\|\s*((?:SCR-\d{3,}-EL-\d{2,})|FR-\d{3,}|SC-\d{3,}|NAV-\d{3,}|REF-\d{3,}|D-\d{3,}|I-\d{3,})\s*\|/);
  if (row) anchors.add(anchorOf(row[1]));
}

function inline(text) {
  const parts = text.split(/(`[^`]*`)/);
  return parts.map(function (part) {
    if (/^`[^`]*`$/.test(part)) return "<code>" + escapeHtml(part.slice(1, -1)) + "</code>";
    let html = escapeHtml(part);
    html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    html = html.replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
    html = html.replace(/(^|[\s(])(https?:\/\/[^\s<)]+)/g, '$1<a href="$2" target="_blank" rel="noopener">$2</a>');
    html = html.replace(TEST_LABEL, function (_, label) { return '<span class="pill test test-' + ({ "E2E": "e2e", "통합": "int", "단위": "unit", "수동": "manual" })[label] + '">' + label + "</span>"; });
    html = html.replace(STATUS_LABEL, function (_, label) {
      const tone = /확정/.test(label) ? "ok" : /결정 필요|가설|추정/.test(label) ? "warn" : "neutral";
      return '<span class="pill status ' + tone + '">' + label + "</span>";
    });
    html = html.replace(/\bP([012])(\s*\((?:High|Medium|Low)\))?/g, function (_, level) { return '<span class="pill prio p' + level + '">P' + level + "</span>"; });
    html = html.replace(ID_PATTERN, function (match, id, field) {
      const kind = id.split("-")[0].toLowerCase();
      const target = anchorOf(id);
      const label = '<span class="idk">' + id + "</span>" + (field ? "<wbr>" + field : "");
      if (anchors.has(target)) return '<a class="id id-' + kind + '" href="#' + target + '">' + label + "</a>";
      const parent = id.match(/^(SCR-\d{3,})-EL/);
      if (parent && anchors.has(anchorOf(parent[1]))) return '<a class="id id-scr" href="#' + anchorOf(parent[1]) + '">' + label + "</a>";
      return '<span class="id id-' + kind + '">' + label + "</span>";
    });
    return html;
  }).join("");
}

const meta = [];
let title = "PRD";
let index = 0;
while (index < lines.length && !/^## /.test(lines[index])) {
  const line = lines[index];
  const heading = line.match(/^# (.*)$/);
  if (heading) title = heading[1].trim();
  const quote = line.match(/^>\s*([^:]+):\s*(.*)$/);
  if (quote) meta.push([quote[1].trim(), quote[2].trim()]);
  index += 1;
}
const metaMap = Object.fromEntries(meta);

function renderTable(rows) {
  const header = cells(rows[0]);
  const body = rows.slice(2).map(cells);
  const head = "<thead><tr>" + header.map(function (cell) { return "<th>" + inline(cell) + "</th>"; }).join("") + "</tr></thead>";
  const tbody = body.map(function (row) {
    const first = row[0] || "";
    const idMatch = first.match(/^((?:SCR-\d{3,}-EL-\d{2,})|FR-\d{3,}|SC-\d{3,}|NAV-\d{3,}|REF-\d{3,}|D-\d{3,}|I-\d{3,})$/);
    const rowId = idMatch ? ' id="' + anchorOf(idMatch[1]) + '"' : "";
    return "<tr" + rowId + ">" + row.map(function (cell, column) { return '<td data-label="' + escapeHtml((header[column] || "").replace(/\*\*/g, "")) + '">' + inline(cell) + "</td>"; }).join("") + "</tr>";
  }).join("");
  const wide = header.length >= 7 ? " wide" : "";
  return '<div class="table-wrap' + wide + '"><table>' + head + "<tbody>" + tbody + "</tbody></table></div>";
}

function renderCards(rows, small) {
  return '<div class="cards' + (small ? " small" : "") + '">' + rows.slice(2).map(cells).map(function (row) {
    return '<div class="card"><div class="card-key">' + inline(row[0].replace(/\*\*/g, "")) + '</div><div class="card-value">' + inline(row[1] || "") + "</div></div>";
  }).join("") + "</div>";
}

const out = [];
const toc = [];
let open = { section: false, article: false };
let currentH2 = "";
let currentH3 = "";
let paragraph = [];

function flushParagraph() {
  if (paragraph.length > 0) {
    out.push("<p>" + inline(paragraph.join(" ")) + "</p>");
    paragraph = [];
  }
}

function closeArticle() {
  if (open.article) { out.push("</article>"); open.article = false; }
}

function closeSection() {
  closeArticle();
  if (open.section) { out.push("</section>"); open.section = false; }
}

for (; index < lines.length; index += 1) {
  const line = lines[index];

  if (/^```/.test(line)) {
    flushParagraph();
    const code = [];
    index += 1;
    while (index < lines.length && !/^```/.test(lines[index])) { code.push(lines[index]); index += 1; }
    out.push("<pre><code>" + escapeHtml(code.join("\n")) + "</code></pre>");
    continue;
  }

  const heading = line.match(/^(#{2,6})\s+(.*)$/);
  if (heading) {
    flushParagraph();
    const level = heading[1].length;
    const text = heading[2].trim();
    const anchor = headingAnchor(text);
    if (level === 2) {
      closeSection();
      currentH2 = text;
      out.push('<section class="chapter" id="' + anchor + '">');
      open.section = true;
      out.push('<h2>' + inline(text) + "</h2>");
      toc.push({ level: 2, text, anchor });
      continue;
    }
    if (level === 3) {
      closeArticle();
      currentH3 = text;
      const isData = /^DATA-\d/.test(text);
      if (isData) { out.push('<article class="block data" id="' + anchor + '">'); open.article = true; }
      out.push("<h3" + (isData ? "" : ' id="' + anchor + '"') + ">" + inline(text) + "</h3>");
      if (/^5\.5|^DATA-\d/.test(text) || /^5\.\d/.test(text)) toc.push({ level: 3, text, anchor });
      continue;
    }
    if (level === 4 && /^SCR-\d/.test(text)) {
      closeArticle();
      out.push('<article class="block screen" id="' + anchor + '">');
      open.article = true;
      out.push('<h4 class="screen-title">' + inline(text) + "</h4>");
      toc.push({ level: 4, text, anchor });
      continue;
    }
    out.push("<h" + Math.min(level, 6) + ">" + inline(text) + "</h" + Math.min(level, 6) + ">");
    continue;
  }

  if (/^\|/.test(line) && index + 1 < lines.length && isSeparator(lines[index + 1])) {
    flushParagraph();
    const rows = [];
    while (index < lines.length && /^\|/.test(lines[index])) { rows.push(lines[index]); index += 1; }
    index -= 1;
    if (/^0\./.test(currentH2) && currentH3 === "" && cells(rows[0])[0] === "Perspective") out.push(renderCards(rows, false));
    else if (/^Context Anchor/.test(currentH3) && cells(rows[0])[0] === "Key") out.push(renderCards(rows, true));
    else out.push(renderTable(rows));
    continue;
  }

  const bullet = line.match(/^(\s*)([-*]|\d+\.)\s+(.*)$/);
  if (bullet) {
    flushParagraph();
    const ordered = /\d+\./.test(bullet[2]);
    const items = [];
    while (index < lines.length) {
      const item = lines[index].match(/^(\s*)([-*]|\d+\.)\s+(.*)$/);
      if (!item) break;
      items.push({ depth: Math.min(Math.floor(item[1].length / 2), 3), text: item[3] });
      index += 1;
    }
    index -= 1;
    const pairs = items.map(function (item) { return item.text.match(/^\*\*([^*]+?):\*\*\s*(.*)$/); });
    if (!ordered && pairs.every(Boolean)) {
      out.push('<dl class="kv">' + pairs.map(function (pair) { return "<dt>" + inline(pair[1]) + "</dt><dd>" + inline(pair[2]) + "</dd>"; }).join("") + "</dl>");
    } else {
      out.push((ordered ? "<ol>" : "<ul>") + items.map(function (item) { return '<li class="indent-' + item.depth + '">' + inline(item.text) + "</li>"; }).join("") + (ordered ? "</ol>" : "</ul>"));
    }
    continue;
  }

  const quote = line.match(/^>\s?(.*)$/);
  if (quote) {
    flushParagraph();
    out.push('<div class="callout">' + inline(quote[1]) + "</div>");
    continue;
  }

  if (line.trim() === "") { flushParagraph(); continue; }
  paragraph.push(line.trim());
}
flushParagraph();
closeSection();

function count(pattern) {
  return new Set(Array.from(source.matchAll(pattern), function (match) { return match[1]; })).size;
}

const screenCount = count(/^####\s+(SCR-\d{3,})\s+—/gm);
const frRows = source.split("\n").filter(function (line) { return /^\|\s*FR-\d{3,}\s*\|/.test(line); });
const p0Count = frRows.filter(function (line) { return /\|\s*P0\b/.test(line); }).length;
const scCount = count(/^\|\s*(SC-\d{3,})\s*\|/gm);
const dataCount = count(/^###\s+(DATA-\d{3,})\s+—/gm);
const featureSection = (source.split(/^## 14\./m)[1] || "").split(/^## /m)[0];
const featureCount = featureSection.split("\n").filter(function (line) { return /^\|\s*\d+\s*\|/.test(line); }).length;

const gate = metaMap["게이트"] || "";
const gateVerdict = (gate.match(/착수 가능|조건부 착수|착수 불가/) || [""])[0];
const gateScore = (gate.match(/(\d+)\s*점/) || [])[1] || "";
const gateCounts = ["Blocker", "Major", "Minor"].map(function (key) {
  return [key, (gate.match(new RegExp(key + "\\s*(\\d+)")) || [])[1] || "0"];
});
const gateTone = gateVerdict === "착수 가능" ? "ok" : gateVerdict === "조건부 착수" ? "warn" : "bad";
const status = metaMap["상태"] || "";
const revision = ((metaMap["정본"] || "").match(/정본 개정:\s*([^,]+)/) || [])[1] || "";

const metaRows = meta.filter(function (pair) { return !["상태", "게이트"].includes(pair[0]); }).map(function (pair) {
  return "<div><dt>" + escapeHtml(pair[0]) + "</dt><dd>" + inline(pair[1]) + "</dd></div>";
}).join("");

const tocHtml = toc.map(function (item) {
  return '<a class="toc-' + item.level + '" href="#' + item.anchor + '">' + escapeHtml(item.text.replace(/\s*\(.*\)$/, "")) + "</a>";
}).join("");

const productName = title.replace(/^PRD\s*—\s*/, "");
const html = `<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${escapeHtml(productName)} PRD</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<style>
:root{--primary:#0066cc;--primary-focus:#0071e3;--ink:#1d1d1f;--muted:#7a7a7a;--muted-80:#333333;--hairline:#e0e0e0;--divider:#f0f0f0;--canvas:#ffffff;--parchment:#f5f5f7;--pearl:#fafafc;--tile:#272729;--ok:#1d8a3a;--warn:#b25000;--bad:#c4161c;--r-sm:8px;--r-md:11px;--r-lg:18px}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:24px}
body{margin:0;background:var(--parchment);color:var(--ink);font-family:"Pretendard Variable",Pretendard,-apple-system,BlinkMacSystemFont,system-ui,sans-serif;font-size:17px;line-height:1.47;letter-spacing:-0.374px;-webkit-font-smoothing:antialiased;word-break:keep-all;overflow-wrap:break-word}
a{color:var(--primary);text-decoration:none}
a:hover{text-decoration:underline}
.hero{background:#000;color:#fff;padding:72px 24px 56px}
.hero-inner{max-width:1440px;margin:0 auto}
.eyebrow{font-size:14px;color:#a1a1a6;letter-spacing:-0.224px;margin:0 0 8px}
.hero h1{font-size:56px;line-height:1.07;font-weight:600;letter-spacing:-0.28px;margin:0 0 20px}
.badges{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:32px}
.badge{display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border-radius:9999px;font-size:14px;background:#1d1d1f;color:#f5f5f7;border:1px solid #333}
.badge.ok{background:#0f3d1c;border-color:#1d8a3a}.badge.warn{background:#3d2600;border-color:#b25000}.badge.bad{background:#3d0a0c;border-color:#c4161c}
.stats{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px}
.stat{background:var(--tile);border-radius:var(--r-lg);padding:18px 20px}
.stat b{display:block;font-size:34px;font-weight:600;letter-spacing:-0.374px;line-height:1.1}
.stat span{font-size:14px;color:#a1a1a6}
.layout{max-width:1440px;margin:0 auto;padding:32px 24px 96px;display:grid;grid-template-columns:220px minmax(0,1fr);gap:32px}
nav.toc{position:sticky;top:24px;align-self:start;max-height:calc(100vh - 48px);overflow:auto;font-size:14px;padding-right:8px}
nav.toc a{display:block;color:var(--muted-80);padding:5px 10px;border-radius:var(--r-sm);line-height:1.35}
nav.toc a:hover{background:#e8e8ed;text-decoration:none}
nav.toc a.active{background:#fff;color:var(--primary);font-weight:600}
nav.toc .toc-3{padding-left:22px;color:var(--muted)}nav.toc .toc-4{padding-left:34px;color:var(--muted);font-size:13px}
main{min-width:0}
.meta{background:var(--canvas);border-radius:var(--r-lg);padding:24px 28px;margin-bottom:24px}
.meta dl{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 32px;margin:0}
.meta dt{font-size:12px;color:var(--muted);letter-spacing:-0.12px}.meta dd{margin:2px 0 0;font-size:14px;letter-spacing:-0.224px}
section.chapter{background:var(--canvas);border-radius:var(--r-lg);padding:40px 44px;margin-bottom:24px}
h2{font-size:34px;line-height:1.2;font-weight:600;margin:0 0 24px;letter-spacing:-0.374px}
h3{font-size:24px;font-weight:600;margin:40px 0 16px;letter-spacing:-0.2px}
h4,h5,h6{font-size:17px;font-weight:600;margin:28px 0 10px}
h5{font-size:15px;color:var(--muted-80);text-transform:none;margin-top:24px}
p,ul,ol{margin:0 0 14px}
li{margin:4px 0}
.kv{display:grid;grid-template-columns:minmax(120px,180px) minmax(0,1fr);gap:10px 24px;margin:0 0 20px;font-size:15px}
.kv dt{color:var(--muted);font-weight:600;font-size:14px;padding-top:1px}
.kv dd{margin:0}li.indent-1{margin-left:20px}li.indent-2{margin-left:40px}
code{font-family:"SF Mono",ui-monospace,Menlo,Consolas,monospace;font-size:13px;background:var(--parchment);border-radius:5px;padding:2px 6px;letter-spacing:0}
pre{background:var(--parchment);border-radius:var(--r-md);padding:16px;overflow:auto}
pre code{background:none;padding:0}
.callout{background:var(--pearl);border-left:3px solid var(--primary);border-radius:var(--r-sm);padding:12px 16px;margin:0 0 14px;font-size:15px}
.table-wrap{overflow-x:auto;margin:0 0 20px;border:1px solid var(--hairline);border-radius:var(--r-md)}
table{border-collapse:collapse;width:100%;font-size:14px;letter-spacing:-0.224px;line-height:1.43}
.table-wrap.wide table{font-size:13px;line-height:1.4}
.table-wrap.wide th,.table-wrap.wide td{padding:8px 9px}
td{min-width:56px}
td code,td a{white-space:normal;overflow-wrap:anywhere}
.idk{white-space:nowrap}
.table-wrap{background:linear-gradient(to right,#fff 30%,rgba(255,255,255,0)) left/40px 100% no-repeat local,linear-gradient(to left,#fff 30%,rgba(255,255,255,0)) right/40px 100% no-repeat local,radial-gradient(farthest-side at 0 50%,rgba(0,0,0,.12),transparent) left/12px 100% no-repeat scroll,radial-gradient(farthest-side at 100% 50%,rgba(0,0,0,.12),transparent) right/12px 100% no-repeat scroll}
th{position:sticky;top:0;background:var(--parchment);text-align:left;font-weight:600;color:var(--muted-80);padding:10px 12px;border-bottom:1px solid var(--hairline)}
td{padding:10px 12px;border-bottom:1px solid var(--divider);vertical-align:top}
tr:last-child td{border-bottom:none}
tbody tr:hover{background:var(--pearl)}
tr:target{background:#e8f1fb}
.cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin:0 0 20px}
.cards.small{grid-template-columns:repeat(5,minmax(0,1fr))}
.card{background:var(--parchment);border-radius:var(--r-md);padding:18px 20px}
.card-key{font-size:12px;font-weight:600;color:var(--primary);text-transform:uppercase;letter-spacing:0.4px;margin-bottom:6px}
.card-value{font-size:15px;line-height:1.5}
.cards.small .card-value{font-size:14px}
article.block{border:1px solid var(--hairline);border-radius:var(--r-lg);padding:28px 32px;margin:24px 0;background:var(--canvas)}
article.block:target{border-color:var(--primary);box-shadow:0 0 0 3px rgba(0,102,204,.15)}
.screen-title{font-size:24px;margin:0 0 16px}
article.block h5{border-top:1px solid var(--divider);padding-top:20px}
.id{display:inline-block;max-width:100%;overflow-wrap:anywhere;font-family:"SF Mono",ui-monospace,Menlo,Consolas,monospace;font-size:12px;letter-spacing:0;padding:1px 7px;border-radius:9999px;background:#e8f1fb;color:var(--primary);margin:1px 0}
a.id:hover{background:var(--primary);color:#fff;text-decoration:none}
.id-fr{background:#eef6ee;color:#1d6b33}.id-sc{background:#fff4e5;color:#995200}.id-data{background:#f3eefc;color:#6a3fb5}.id-nav,.id-ref{background:#eeeef2;color:#4a4a50}.id-d,.id-i{background:#fdeceb;color:#a3201b}
a.id-fr:hover{background:#1d6b33}a.id-sc:hover{background:#995200}a.id-data:hover{background:#6a3fb5}
.pill{display:inline-block;font-size:12px;font-weight:600;letter-spacing:0;padding:1px 8px;border-radius:9999px;white-space:nowrap}
.test-e2e{background:#0066cc;color:#fff}.test-int{background:#5e5ce6;color:#fff}.test-unit{background:#30a46c;color:#fff}.test-manual{background:#8e8e93;color:#fff}
.status.ok{background:#e3f4e8;color:var(--ok)}.status.warn{background:#fff1e0;color:var(--warn)}.status.neutral{background:#eeeef2;color:#4a4a50}
.prio.p0{background:#1d1d1f;color:#fff}.prio.p1{background:#d2d2d7;color:#1d1d1f}.prio.p2{background:#eeeef2;color:#7a7a7a}
footer{max-width:1440px;margin:0 auto;padding:0 24px 48px;font-size:12px;color:var(--muted)}
@media (max-width:1200px){.layout{grid-template-columns:1fr;gap:16px}nav.toc{position:static;max-height:none;background:var(--canvas);border-radius:var(--r-lg);padding:12px}nav.toc .toc-3,nav.toc .toc-4{display:none}.stats{grid-template-columns:repeat(3,minmax(0,1fr))}.cards.small{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:900px){.table-wrap.wide{background:none}.table-wrap.wide table,.table-wrap.wide tbody,.table-wrap.wide tr,.table-wrap.wide td{display:block}.table-wrap.wide thead{display:none}.table-wrap.wide tr{padding:12px 14px;border-bottom:1px solid var(--hairline)}.table-wrap.wide tr:last-child{border-bottom:none}.table-wrap.wide td{display:grid;justify-items:start;grid-template-columns:104px minmax(0,1fr);gap:10px;padding:3px 0;border:none;min-width:0}.table-wrap.wide td::before{content:attr(data-label);color:var(--muted);font-weight:600;font-size:12px;padding-top:2px}}
@media (max-width:640px){.table-wrap{background:none}.table-wrap table,.table-wrap tbody,.table-wrap tr,.table-wrap td{display:block}.table-wrap thead{display:none}.table-wrap tr{padding:12px 14px;border-bottom:1px solid var(--hairline)}.table-wrap tr:last-child{border-bottom:none}.table-wrap td{display:grid;justify-items:start;grid-template-columns:96px minmax(0,1fr);gap:10px;padding:3px 0;border:none;min-width:0}.table-wrap td::before{content:attr(data-label);color:var(--muted);font-weight:600;font-size:12px;padding-top:2px}.hero{padding:48px 16px 36px}.hero h1{font-size:34px}.layout{padding:16px 16px 64px}section.chapter{padding:24px 20px}article.block{padding:20px}h2{font-size:28px}.stats{grid-template-columns:repeat(2,minmax(0,1fr))}.cards{grid-template-columns:1fr}.meta dl{grid-template-columns:1fr}.kv{grid-template-columns:1fr;gap:2px}.kv dd{margin-bottom:10px}}
@media print{body{background:#fff}.hero{background:#fff;color:#000;padding:0 0 24px}.stat{background:#f5f5f7}.stat span,.eyebrow{color:#555}nav.toc{display:none}.layout{display:block;padding:0}section.chapter{padding:0;break-inside:auto}article.block{break-inside:avoid}}
</style>
</head>
<body>
<header class="hero">
  <div class="hero-inner">
    <p class="eyebrow">Product Requirements · ${escapeHtml(revision)}</p>
    <h1>${escapeHtml(productName)}</h1>
    <div class="badges">
      <span class="badge">상태 ${escapeHtml(status)}</span>
      ${gateVerdict ? `<span class="badge ${gateTone}">게이트 ${escapeHtml(gateVerdict)}${gateScore ? " · " + gateScore + "점" : ""}</span>` : ""}
      ${gateCounts.map(function (pair) { return `<span class="badge">${pair[0]} ${pair[1]}</span>`; }).join("")}
    </div>
    <div class="stats">
      <div class="stat"><b>${screenCount}</b><span>화면</span></div>
      <div class="stat"><b>${frRows.length}</b><span>기능 요구사항 · P0 ${p0Count}</span></div>
      <div class="stat"><b>${scCount}</b><span>성공 기준</span></div>
      <div class="stat"><b>${dataCount}</b><span>데이터 엔티티</span></div>
      <div class="stat"><b>${featureCount}</b><span>feature</span></div>
    </div>
  </div>
</header>
<div class="layout">
  <nav class="toc" aria-label="목차">${tocHtml}</nav>
  <main>
    <div class="meta"><dl>${metaRows}</dl></div>
    ${out.join("\n")}
  </main>
</div>
<footer>${escapeHtml(path.basename(input))}에서 생성됨 · 정본은 PRD.md이며 이 파일은 읽기용입니다.</footer>
<script>
(function(){var links=[].slice.call(document.querySelectorAll('nav.toc a'));var map={};links.forEach(function(a){map[a.getAttribute('href').slice(1)]=a});
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting&&map[e.target.id]){links.forEach(function(l){l.classList.remove('active')});map[e.target.id].classList.add('active')}})},{rootMargin:'0px 0px -70% 0px'});
document.querySelectorAll('section.chapter,article.block.screen').forEach(function(s){io.observe(s)})})();
</script>
</body>
</html>
`;

fs.writeFileSync(output, html, "utf8");
console.log("PRD HTML: " + output);
