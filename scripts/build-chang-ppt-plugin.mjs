#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = path.join(root, 'chang-ppt');
const target = path.join(root, 'plugins/chang-ppt/skills/chang-ppt');
const check = process.argv.includes('--check');
function inventory(dir, prefix = '') {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, {withFileTypes:true}).flatMap(e => {
    if (e.name === '__pycache__' || e.name.endsWith('.pyc')) return [];
    assert(!e.isSymbolicLink(), `Unexpected symlink: ${path.join(dir,e.name)}`);
    const rel = path.join(prefix,e.name);
    return e.isDirectory() ? inventory(path.join(dir,e.name),rel) : [rel];
  }).sort();
}
const files = inventory(source);
function sync(destination) {
  for (const rel of files) {
    const out = path.join(destination,rel);
    fs.mkdirSync(path.dirname(out),{recursive:true});
    fs.copyFileSync(path.join(source,rel),out);
  }
}
function verify(destination) {
  assert.deepEqual(inventory(destination),files,'File list differs; review obsolete files manually.');
  for (const rel of files) assert(fs.readFileSync(path.join(source,rel)).equals(fs.readFileSync(path.join(destination,rel))),`Content differs: ${rel}`);
}
if (!check) sync(target);
verify(target);
const manifest = JSON.parse(fs.readFileSync(path.join(root,'plugins/chang-ppt/.claude-plugin/plugin.json'),'utf8'));
const market = JSON.parse(fs.readFileSync(path.join(root,'.claude-plugin/marketplace.json'),'utf8'));
const entry = market.plugins.find(p=>p.name==='chang-ppt');
assert.equal(entry?.version,manifest.version);
assert.equal(entry?.source,'./plugins/chang-ppt');
if (process.argv.includes('--install-claude')) {
  assert(!check,'--check and --install-claude cannot be combined');
  const personal = path.join(os.homedir(),'.claude/skills/chang-ppt');
  sync(personal); verify(personal);
  console.log(`Installed: ${personal}`);
}
console.log(`PASS chang-ppt ${manifest.version}: ${files.length} source/package files match`);
