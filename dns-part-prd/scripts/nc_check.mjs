#!/usr/bin/env node
// NC 코드 빠른 검사기 v2 — DN Virtual Simulator의 「빠른 검사」를 흉내 낸 시연용 대역입니다.
// 실제 시뮬레이터가 아닙니다. 형상 비교와 고정구 충돌은 sim_check.py가 맡습니다.
// 지원: G0 G1 G2 G3(I·J), G81 G82 G83 G84 G85 고정 사이클, G80, G98·G99, 주석 (OPERATION ..) (STOCK TOP Z..)
// 사용법: node nc_check.mjs <파일.nc> [--json]
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const args = process.argv.slice(2);
const file = args.find((a) => !a.startsWith("--"));
if (!file) { console.error("사용법: node nc_check.mjs <파일.nc> [--json]"); process.exit(2); }
const asJson = args.includes("--json");
const here = path.dirname(fileURLToPath(import.meta.url));
const machine = JSON.parse(fs.readFileSync(path.join(here, "machine.json"), "utf8"));

const lines = fs.readFileSync(file, "utf8").split(/\r?\n/);
const pos = { X: 0, Y: 0, Z: 100 };
let mode = null, feed = null, op = null, stockTop = 0, cycle = null, retract = "G98", initZ = 100;
let tools = 0;
let cycleR = null, cycleZ = null;
const alarms = [], suggestions = [];
let cutSec = 0, rapidSec = 0;
const WORD = /^[A-Z][+-]?(\d+\.?\d*|\.\d+)$/;
const alarm = (line, code, msg) => alarms.push({ line, code, msg });
const opLim = (k) => op && machine.operations[op] ? machine.operations[op][k] : null;

function checkLimits(ln, p) {
  for (const a of Object.keys(machine.limits_mm_deg)) {
    const [lo, hi] = machine.limits_mm_deg[a];
    if (p[a] < lo || p[a] > hi) { alarm(ln, "TRAVEL", `${a}축 이동 한계(${lo}~${hi}) 초과: ${p[a]}`); return; }
  }
}
function rapid(ln, t) {
  const xy = t.X !== pos.X || t.Y !== pos.Y;
  if (xy && Math.min(pos.Z, t.Z) < stockTop) alarm(ln, "COLLISION", `충돌 위험: 소재 윗면 Z${stockTop} 아래(Z${Math.min(pos.Z, t.Z)})에서 빠른 이송으로 XY 이동`);
  checkLimits(ln, t);
  rapidSec += Math.hypot(t.X - pos.X, t.Y - pos.Y, t.Z - pos.Z) / machine.rapid_mm_per_min * 60;
  Object.assign(pos, t);
}
function cut(ln, t, len) {
  if (feed == null) { alarm(ln, "NOFEED", "절삭 이송에 이송 속도(F)가 없습니다"); Object.assign(pos, t); return; }
  const lim = opLim("feed_max_mm_per_min");
  if (lim && feed > lim) alarm(ln, "FEED", `이송 ${feed}mm/min이 ${op} 상한 ${lim}을 넘습니다`);
  checkLimits(ln, t);
  cutSec += len / feed * 60;
  const airborne = pos.Z > stockTop + 1 && t.Z > stockTop + 1;
  if (airborne && len > 20) suggestions.push({ line: ln, msg: `소재 위 공중 이동 ${len.toFixed(0)}mm를 절삭 이송으로 합니다 — G0로 바꿀 수 있습니다` });
  Object.assign(pos, t);
}

lines.forEach((raw, i) => {
  const ln = i + 1;
  let t = raw.trim();
  const m1 = t.match(/\(OPERATION\s+(\w+)\)/i); if (m1) op = m1[1].toUpperCase();
  const m2 = t.match(/\(STOCK TOP Z([-\d.]+)\)/i); if (m2) stockTop = parseFloat(m2[1]);
  t = t.replace(/\(.*?\)/g, "").trim();
  if (!t || t === "%") return;
  const w = {}; const gs = [];
  for (const word of t.split(/\s+/)) {
    if (!WORD.test(word)) { alarm(ln, "FORMAT", `형식 오류: 「${word}」를 읽을 수 없습니다`); continue; }
    const L = word[0], v = parseFloat(word.slice(1));
    if (L === "G") gs.push(v); else w[L] = v;
  }
  for (const g of gs) {
    if ([0, 1, 2, 3].includes(g)) { mode = g; cycle = null; }
    else if ([81, 82, 83, 84, 85].includes(g)) { if (cycle !== g) { initZ = pos.Z; cycleR = null; cycleZ = null; } cycle = g; }
    else if (g === 80) cycle = null;
    else if (g === 98) retract = "G98"; else if (g === 99) retract = "G99";
  }
  if (gs.includes(91) || gs.includes(28)) return; // G91 G28 원점 복귀 줄은 이동 계산에서 제외
  if (w.F !== undefined) feed = w.F;
  if (w.S !== undefined) { const lim = opLim("spindle_max_rpm"); if (lim && w.S > lim) alarm(ln, "SPINDLE", `주축 ${w.S}rpm이 ${op} 상한 ${lim}을 넘습니다`); }
  if (w.M === 6) tools++;
  const has = ["X", "Y", "Z"].some((a) => w[a] !== undefined);
  if (!has) return;
  const tgt = { X: w.X ?? pos.X, Y: w.Y ?? pos.Y, Z: w.Z ?? pos.Z };
  if (cycle) {
    // 고정 사이클: XY 빠른 이송 → R까지 빠른 이송 → Z까지 절삭 → 복귀
    if (w.R !== undefined) cycleR = w.R;
    const Rz = w.R ?? cycleR; const Zd = w.Z ?? cycleZ; if (w.Z !== undefined) cycleZ = w.Z;
    if (Rz == null || Zd == null) { alarm(ln, "CYCLE", "고정 사이클에 R 또는 Z가 없습니다"); return; }
    if (Rz < stockTop) alarm(ln, "CYCLE", `R점 Z${Rz}가 소재 윗면 Z${stockTop}보다 낮습니다`);
    rapid(ln, { X: tgt.X, Y: tgt.Y, Z: pos.Z });
    rapid(ln, { X: tgt.X, Y: tgt.Y, Z: Rz });
    cut(ln, { X: tgt.X, Y: tgt.Y, Z: Zd }, Rz - Zd);
    if (cycle === 84 || cycle === 85) cut(ln, { X: tgt.X, Y: tgt.Y, Z: Rz }, Rz - Zd);
    rapid(ln, { X: tgt.X, Y: tgt.Y, Z: retract === "G98" ? initZ : Rz });
    return;
  }
  if (mode === 0) rapid(ln, tgt);
  else if (mode === 1) cut(ln, tgt, Math.hypot(tgt.X - pos.X, tgt.Y - pos.Y, tgt.Z - pos.Z));
  else if (mode === 2 || mode === 3) {
    if (w.I === undefined && w.J === undefined) { alarm(ln, "ARC", "원호에 I·J가 없습니다"); return; }
    const cx = pos.X + (w.I ?? 0), cy = pos.Y + (w.J ?? 0);
    const r0 = Math.hypot(pos.X - cx, pos.Y - cy), r1 = Math.hypot(tgt.X - cx, tgt.Y - cy);
    if (Math.abs(r0 - r1) > 0.005) alarm(ln, "ARC", `원호 시작·끝 반지름이 다릅니다(${r0.toFixed(3)} / ${r1.toFixed(3)})`);
    let a0 = Math.atan2(pos.Y - cy, pos.X - cx), a1 = Math.atan2(tgt.Y - cy, tgt.X - cx);
    let d = mode === 3 ? a1 - a0 : a0 - a1; while (d <= 0) d += 2 * Math.PI;
    cut(ln, tgt, Math.hypot(r0 * d, tgt.Z - pos.Z));
  }
});

const toolSec = tools * machine.tool_change_sec;
const total = cutSec + rapidSec + toolSec;
const fmt = (s) => `${Math.floor(s / 60)}분 ${(s % 60).toFixed(1)}초`;
const result = {
  file: path.basename(file), blocks: lines.length, alarm_count: alarms.length, alarms,
  cycle_time_sec: +total.toFixed(1), cutting_sec: +cutSec.toFixed(1), rapid_sec: +rapidSec.toFixed(1), tool_change_sec: toolSec, tool_changes: tools,
  suggestions, note: "시연용 대역 검사기 결과입니다. 실제 DN Virtual Simulator 결과가 아닙니다.",
};
if (asJson) console.log(JSON.stringify(result, null, 2));
else {
  console.log(`파일 ${result.file} · 블록 ${result.blocks}`);
  console.log(`사이클타임 ${fmt(total)} (절삭 ${fmt(cutSec)}, 빠른 이송 ${fmt(rapidSec)}, 공구 교환 ${tools}회 ${toolSec}초)`);
  console.log(`알람 ${alarms.length}건`);
  for (const a of alarms) console.log(`  ${String(a.line).padStart(4)}행 [${a.code}] ${a.msg}`);
  if (suggestions.length) { console.log(`개선 후보 ${suggestions.length}건`); for (const s of suggestions) console.log(`  ${String(s.line).padStart(4)}행 ${s.msg}`); }
  console.log(result.note);
}
process.exit(alarms.length ? 1 : 0);
