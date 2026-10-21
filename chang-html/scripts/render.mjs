#!/usr/bin/env node
// 교안을 실제 브라우저로 열어 화면을 캡처하고 콘솔 오류·버튼 동작을 확인한다.
// 사용: node render.mjs <교안.html> <출력폴더> [--width 1280]
// Playwright가 필요하다. 브라우저 경로가 다르면 CHROMIUM_PATH 환경변수로 지정한다.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); } catch { ({ chromium } = require(path.join(require('child_process').execSync('npm root -g').toString().trim(), 'playwright'))); }

const [file, outDir] = process.argv.slice(2);
if (!file || !outDir) { console.error('사용: node render.mjs <교안.html> <출력폴더>'); process.exit(2); }
const width = Number((process.argv.find((a, i, all) => all[i - 1] === '--width')) || 1280);
fs.mkdirSync(outDir, { recursive: true });
const launch = process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {};
const browser = await chromium.launch(launch);
const page = await browser.newPage({ viewport: { width, height: 900 } });
const errors = [];
page.on('pageerror', e => errors.push(e.message));
page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
await page.goto('file://' + path.resolve(file));
await page.waitForTimeout(2500);
// 섹션 캡처에 고정 툴바가 겹치지 않게 한다
await page.addStyleTag({ content: '.sticky{position:static!important}' });

// 섹션별 캡처
const sections = await page.$$('main > section');
let i = 0;
for (const s of sections) { i += 1; await s.screenshot({ path: path.join(outDir, `sec-${String(i).padStart(2, '0')}.png`) }); }
await page.screenshot({ path: path.join(outDir, 'top.png') });

// 버튼 동작: 첫 탭 전환, 강사 노트 접기
const report = { file, sections: i, errors, checks: {} };
const tabs = await page.$$eval('[id^="btn-"]', b => b.map(x => x.id.slice(4)));
if (tabs.length > 1) {
  await page.evaluate(id => window.switchTab(id), tabs[1]);
  report.checks.tab_switch = await page.$eval('#' + tabs[1], e => !e.classList.contains('hidden'));
}
if (await page.$('details.instructor-note')) {
  await page.evaluate(() => window.toggleNotes(false));
  report.checks.notes_collapse = (await page.$$eval('details.instructor-note', d => d.filter(x => x.open).length)) === 0;
}
// 가로 넘침: 휴대폰 폭에서 페이지 가로 스크롤 여부
await page.setViewportSize({ width: 390, height: 844 });
report.checks.mobile_no_hscroll = await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1);
await page.screenshot({ path: path.join(outDir, 'mobile-top.png') });
await browser.close();
fs.writeFileSync(path.join(outDir, 'render_report.json'), JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
process.exit(errors.length ? 1 : 0);
