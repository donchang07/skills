#!/usr/bin/env node
// 루트의 편집 원본 스킬 폴더에서 plugins/<name>/ 설치 패키지를 생성한다. 배포본을 직접 편집하지 않는다.
// to-prd는 버전 검증이 따로 있어 scripts/build-to-prd-plugin.mjs가 담당한다.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const skills = ['chang-ppt', 'chang-book', 'github-pages-handbook', 'vercel-rag'];
const checkOnly = process.argv.includes('--check');
const ignored = new Set(['__pycache__', '.DS_Store']);
function inventory(directory, prefix='') {
  return fs.readdirSync(directory, { withFileTypes:true }).filter(entry => !ignored.has(entry.name)).flatMap(entry => {
    const rel = path.join(prefix, entry.name);
    assert(!entry.isSymbolicLink(), '패키지에는 심볼릭 링크를 넣지 않는다: ' + rel);
    return entry.isDirectory() ? inventory(path.join(directory, entry.name), rel) : [rel];
  }).sort();
}
const marketplace = JSON.parse(fs.readFileSync(path.join(root, '.claude-plugin/marketplace.json'), 'utf8'));
for (const name of skills) {
  const source = path.join(root, name);
  const target = path.join(root, 'plugins', name, 'skills', name);
  const files = inventory(source);
  if (!checkOnly) {
    fs.rmSync(target, { recursive:true, force:true });
    for (const rel of files) {
      const destination = path.join(target, rel);
      fs.mkdirSync(path.dirname(destination), { recursive:true });
      fs.copyFileSync(path.join(source, rel), destination);
    }
  }
  assert.deepEqual(inventory(target), files, `${name}: 원본과 배포본 파일 목록 불일치`);
  for (const rel of files) assert(fs.readFileSync(path.join(source, rel)).equals(fs.readFileSync(path.join(target, rel))), `${name}: 배포본 내용 불일치: ` + rel);
  const manifests = ['plugin.json', '.claude-plugin/plugin.json', '.codex-plugin/plugin.json'].map(file => JSON.parse(fs.readFileSync(path.join(root, 'plugins', name, file), 'utf8')));
  const entry = marketplace.plugins.find(plugin => plugin.name === name);
  assert(entry, `${name}: .claude-plugin/marketplace.json에 항목이 없다`);
  for (const manifest of manifests) {
    assert.equal(manifest.name, name);
    assert.equal(manifest.version, entry.version, `${name}: 매니페스트와 마켓플레이스 버전 불일치`);
  }
  console.log(`PASS ${name} ${entry.version}: ${files.length}개 파일의 원본·배포본 일치`);
}
