#!/usr/bin/env node
// 편집 원본 to-prd-equip/, code-prd-equip/에서 설치 패키지를 생성한다. 배포본을 직접 편집하지 않는다.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const plugin = path.join(root, 'plugins/to-prd-equip');
const skills = ['to-prd-equip', 'code-prd-equip'];
const checkOnly = process.argv.includes('--check');
function inventory(directory, prefix='') {
  return fs.readdirSync(directory, { withFileTypes:true }).flatMap(entry => {
    const rel = path.join(prefix, entry.name);
    assert(!entry.isSymbolicLink(), '패키지에는 심볼릭 링크를 넣지 않는다: ' + rel);
    return entry.isDirectory() ? inventory(path.join(directory, entry.name), rel) : [rel];
  }).sort();
}
let total = 0;
for (const name of skills) {
  const source = path.join(root, name);
  const target = path.join(plugin, 'skills', name);
  const files = inventory(source);
  if (!checkOnly) {
    fs.rmSync(target, { recursive:true, force:true });
    for (const rel of files) {
      const destination = path.join(target, rel);
      fs.mkdirSync(path.dirname(destination), { recursive:true });
      fs.copyFileSync(path.join(source, rel), destination);
    }
  }
  assert(fs.existsSync(target), '배포본 없음: ' + name);
  assert.deepEqual(inventory(target), files, name + ' 원본과 배포본 파일 목록 불일치');
  for (const rel of files) assert(fs.readFileSync(path.join(source, rel)).equals(fs.readFileSync(path.join(target, rel))), name + ' 배포본 내용 불일치: ' + rel);
  total += files.length;
}
assert.deepEqual(fs.readdirSync(path.join(plugin, 'skills')).sort(), skills.slice().sort(), 'skills/에 예상하지 않은 폴더가 있음');
const read = (p) => JSON.parse(fs.readFileSync(path.join(plugin, p), 'utf8'));
const manifests = [read('plugin.json'), read('.claude-plugin/plugin.json'), read('.codex-plugin/plugin.json')];
for (const m of manifests) {
  assert.equal(m.name, 'to-prd-equip');
  assert.equal(m.version, manifests[0].version, 'manifest 버전 불일치');
}
const marketplace = JSON.parse(fs.readFileSync(path.join(root, '.claude-plugin/marketplace.json'), 'utf8'));
const entry = marketplace.plugins.find(p => p.name === 'to-prd-equip');
assert(entry, '.claude-plugin/marketplace.json에 to-prd-equip 항목이 없음');
assert.equal(entry.version, manifests[0].version, 'marketplace 버전 불일치');
const form = fs.readFileSync(path.join(root, 'to-prd-equip/references/request-mapping.md'), 'utf8').match(/요청서 버전: v(\d+\.\d+)/)[1];
assert(manifests[0].version.startsWith(form + '.'), '플러그인 버전과 요청서 양식 버전 불일치');
console.log(`PASS to-prd-equip ${manifests[0].version}: 스킬 ${skills.length}개, ${total}개 파일의 원본·배포본 일치`);
