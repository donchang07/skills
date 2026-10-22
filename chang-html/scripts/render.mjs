#!/usr/bin/env node
// 교안을 실제 브라우저로 열어 화면을 캡처하고 글꼴·인쇄·앵커·버튼 동작을 확인한다.
// 사용: node render.mjs <교안.html> <출력폴더> [--width 1280]
// Playwright가 필요하다. 브라우저 경로가 다르면 CHROMIUM_PATH 환경변수로 지정한다.
//
// 만드는 파일: first.png(첫 화면), mobile-first.png(390 첫 화면), sec-NN.png(장별), top.png, mobile-top.png, render_report.json
// 검사: fonts, print_readable, anchors_clear, tab_switch, notes_collapse, mobile_no_hscroll
// 콘솔 오류가 있거나 검사 하나라도 실패하면 종료 코드 1.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); } catch { ({ chromium } = require(path.join(require('child_process').execSync('npm root -g').toString().trim(), 'playwright'))); }

const [file, outDir] = process.argv.slice(2);
if (!file || !outDir) { console.error('사용: node render.mjs <교안.html> <출력폴더> [--width 1280]'); process.exit(2); }
const width = Number((process.argv.find((a, i, all) => all[i - 1] === '--width')) || 1280);
fs.mkdirSync(outDir, { recursive: true });
const url = 'file://' + path.resolve(file);
const launch = process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {};
const browser = await chromium.launch(launch);
const errors = [];
const watch = p => {
  p.on('pageerror', e => errors.push(e.message));
  p.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
};
const settle = async p => {
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(1200);
};

const report = { file, width, sections: 0, errors, checks: {}, details: {} };
const page = await browser.newPage({ viewport: { width, height: 900 } });
watch(page);
await page.goto(url, { waitUntil: 'networkidle' });
await settle(page);

// 1) 첫 화면 (다른 조작 전에)
await page.screenshot({ path: path.join(outDir, 'first.png') });

// 2) 글꼴: 화면 전체를 한 번 훑어 글꼴을 불러온 뒤 상태를 본다
await page.evaluate(async () => {
  for (let y = 0; y < document.body.scrollHeight; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 25)); }
  window.scrollTo(0, 0);
});
await page.waitForLoadState('networkidle');
await settle(page);
const fonts = await page.evaluate(async () => {
  const sheets = [...document.querySelectorAll('link[rel="stylesheet"]')].map(l => l.href).join(' ');
  const css = [...document.querySelectorAll('style')].map(s => s.textContent).join(' ');
  const declared = { pretendard: /pretendard/i.test(sheets), d2coding: /d2coding/i.test(sheets) };
  // 선언했지만 화면에 쓰이지 않아 아직 안 불러온 경우를 위해 한 번 직접 불러 본다
  try { if (declared.pretendard) await document.fonts.load('16px "Pretendard Variable"', '가a'); } catch (e) {}
  try { if (declared.d2coding) await document.fonts.load('14px "D2Coding"', '가a{'); } catch (e) {}
  await document.fonts.ready;
  const list = [...document.fonts].map(f => ({ family: f.family.replace(/["']/g, ''), weight: f.weight, status: f.status }));
  const has = re => list.some(f => re.test(f.family) && f.status === 'loaded');
  return {
    declared,
    loaded: { pretendard: has(/pretendard/i), d2coding: has(/^d2coding$/i), d2coding_fill: has(/d2coding fill/i) },
    error: list.filter(f => f.status === 'error').map(f => f.family + ' ' + f.weight),
    families: [...new Set(list.map(f => f.family + ':' + f.status))].slice(0, 30),
    google: /fonts\.googleapis|fonts\.gstatic/.test(sheets + css),
  };
});
report.details.fonts = fonts;
report.checks.fonts = fonts.error.length === 0 && !fonts.google
  && (!fonts.declared.pretendard || fonts.loaded.pretendard)
  && (!fonts.declared.d2coding || fonts.loaded.d2coding);

// 3) 앵커: 고정 툴바가 있는 상태에서 각 문서 안 링크 대상이 툴바에 가리지 않는지
await page.addStyleTag({ content: 'html{scroll-behavior:auto!important}' });
const anchors = await page.evaluate(async () => {
  const bar = document.querySelector('.toolbar');
  const targets = [...new Set([...document.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href').slice(1)).filter(Boolean))];
  const bad = [], checked = [];
  for (const id of targets) {
    const el = document.getElementById(id);
    if (!el) { bad.push({ id, reason: '대상 없음' }); continue; }
    const r0 = el.getBoundingClientRect();
    if (!r0.width && !r0.height) continue; // 숨은 탭 안의 대상은 건너뛴다
    history.replaceState(null, '', '#');
    location.hash = '#' + id;
    await new Promise(r => setTimeout(r, 60));
    const barBottom = bar && getComputedStyle(bar).position === 'sticky' ? bar.getBoundingClientRect().bottom : 0;
    const top = el.getBoundingClientRect().top;
    checked.push(id);
    if (top < barBottom - 1) bad.push({ id, top: Math.round(top), toolbar_bottom: Math.round(barBottom) });
  }
  history.replaceState(null, '', location.pathname);
  window.scrollTo(0, 0);
  return { checked: checked.length, failures: bad };
});
report.details.anchors = anchors;
report.checks.anchors_clear = anchors.failures.length === 0;

// 4) 인쇄: 코드 상자 글자와 실제 배경의 대비 4.5 이상
await page.emulateMedia({ media: 'print' });
await page.waitForTimeout(300);
const print = await page.evaluate(() => {
  const rgb = s => { const m = s.match(/[\d.]+/g) || [0, 0, 0, 0]; return { r: +m[0], g: +m[1], b: +m[2], a: m[3] === undefined ? 1 : +m[3] }; };
  const lum = c => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }; return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
  const bgOf = el => {
    for (let e = el; e; e = e.parentElement) { const c = rgb(getComputedStyle(e).backgroundColor); if (c.a > 0.5) return c; }
    return { r: 255, g: 255, b: 255, a: 1 };
  };
  const bad = []; let n = 0;
  document.querySelectorAll('pre, .code').forEach(el => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    const fg = rgb(cs.color), bg = bgOf(el);
    const L1 = lum(fg), L2 = lum(bg);
    const ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
    n += 1;
    if (ratio < 4.5) bad.push({ el: el.tagName.toLowerCase() + (el.id ? '#' + el.id : '.' + el.className), ratio: Math.round(ratio * 100) / 100, color: cs.color });
  });
  return { checked: n, failures: bad.slice(0, 20) };
});
await page.emulateMedia({ media: 'screen' });
report.details.print = print;
report.checks.print_readable = print.failures.length === 0;

// 5) 장별 캡처: 고정 툴바가 겹치지 않게 한다
await page.addStyleTag({ content: '.sticky{position:static!important}' });
const sections = await page.$$('main > section');
let i = 0;
for (const s of sections) { i += 1; await s.screenshot({ path: path.join(outDir, `sec-${String(i).padStart(2, '0')}.png`) }); }
report.sections = i;
await page.evaluate(() => window.scrollTo(0, 0));
await page.screenshot({ path: path.join(outDir, 'top.png') });

// 6) 버튼 동작: 둘째 탭 전환, 강사 노트 접기
const tabs = await page.$$eval('[id^="btn-"]', b => b.map(x => x.id.slice(4)));
if (tabs.length > 1) {
  await page.evaluate(id => window.switchTab(id), tabs[1]);
  report.checks.tab_switch = await page.$eval('#' + tabs[1], e => !e.classList.contains('hidden'));
  await page.evaluate(id => window.switchTab(id), tabs[0]);
}
if (await page.$('details.instructor-note')) {
  await page.evaluate(() => window.toggleNotes(false));
  report.checks.notes_collapse = (await page.$$eval('details.instructor-note', d => d.filter(x => x.open).length)) === 0;
  await page.evaluate(() => window.toggleNotes(true));
}
await page.close();

// 7) 휴대폰 폭: 새 창에서 첫 화면과 가로 넘침
const mob = await browser.newPage({ viewport: { width: 390, height: 844 } });
watch(mob);
await mob.goto(url, { waitUntil: 'networkidle' });
await settle(mob);
await mob.screenshot({ path: path.join(outDir, 'mobile-first.png') });
report.checks.mobile_no_hscroll = await mob.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1);
await mob.screenshot({ path: path.join(outDir, 'mobile-top.png') });
await mob.close();
await browser.close();

const failed = Object.entries(report.checks).filter(([, v]) => v === false).map(([k]) => k);
report.result = errors.length || failed.length ? 'FAIL' : 'PASS';
report.failed = failed;
fs.writeFileSync(path.join(outDir, 'render_report.json'), JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
process.exit(errors.length || failed.length ? 1 : 0);
