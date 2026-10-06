#!/usr/bin/env node
// 편집 원본 to-prd/에서 설치 패키지를 생성한다. 배포본을 직접 편집하지 않는다.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = path.join(root, 'to-prd');
const target = path.join(root, 'plugins/to-prd/skills/to-prd');
const checkOnly = process.argv.includes('--check');
function inventory(directory, prefix='') {
  return fs.readdirSync(directory, { withFileTypes:true }).flatMap(entry => {
    const rel = path.join(prefix, entry.name);
    assert(!entry.isSymbolicLink(), '패키지에는 심볼릭 링크를 넣지 않는다: ' + rel);
    return entry.isDirectory() ? inventory(path.join(directory, entry.name), rel) : [rel];
  }).sort();
}
const files = inventory(source);
if (!checkOnly) {
  for (const rel of files) {
    const destination = path.join(target, rel);
    fs.mkdirSync(path.dirname(destination), { recursive:true });
    fs.copyFileSync(path.join(source, rel), destination);
  }
}
assert.deepEqual(inventory(target), files, '원본과 배포본 파일 목록 불일치. 제거된 파일은 배포본에서도 제거해야 한다.');
for (const rel of files) assert(fs.readFileSync(path.join(source, rel)).equals(fs.readFileSync(path.join(target, rel))), '배포본 내용 불일치: ' + rel);
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'plugins/to-prd/plugin.json'), 'utf8'));
const legacy = JSON.parse(fs.readFileSync(path.join(root, 'plugins/to-prd/.codex-plugin/plugin.json'), 'utf8'));
assert.equal(manifest.name, legacy.name);
assert.equal(manifest.version, legacy.version);
const brief = fs.readFileSync(path.join(source, 'references/brief-mapping.md'), 'utf8').match(/브리프 버전: v(\d+\.\d+)/)[1];
assert(manifest.version.startsWith(brief + '.'), '플러그인 버전과 브리프 버전 불일치');
console.log(`PASS to-prd ${manifest.version}: ${files.length}개 파일의 원본·배포본 일치`);
