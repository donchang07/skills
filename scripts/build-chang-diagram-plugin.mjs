#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = path.join(root, 'chang-diagram');
const target = path.join(root, 'plugins/chang-diagram/skills/chang-diagram');
const agents = path.join(root, 'plugins/chang-diagram/agents');
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
function sync(from, list, destination) {
  for (const rel of list) {
    const out = path.join(destination,rel);
    fs.mkdirSync(path.dirname(out),{recursive:true});
    fs.copyFileSync(path.join(from,rel),out);
  }
}
function verify(from, list, destination, exact = true) {
  if (exact) assert.deepEqual(inventory(destination),list,'File list differs; review obsolete files manually.');
  for (const rel of list) assert(fs.readFileSync(path.join(from,rel)).equals(fs.readFileSync(path.join(destination,rel))),`Content differs: ${rel}`);
}
if (!check) sync(source, files, target);
verify(source, files, target);
const manifest = JSON.parse(fs.readFileSync(path.join(root,'plugins/chang-diagram/.claude-plugin/plugin.json'),'utf8'));
const market = JSON.parse(fs.readFileSync(path.join(root,'.claude-plugin/marketplace.json'),'utf8'));
const entry = market.plugins.find(p=>p.name==='chang-diagram');
assert.equal(entry?.version,manifest.version);
assert.equal(entry?.source,'./plugins/chang-diagram');
const agentFiles = inventory(agents);
if (process.argv.includes('--install-claude')) {
  assert(!check,'--check and --install-claude cannot be combined');
  const personal = path.join(os.homedir(),'.claude/skills/chang-diagram');
  const personalAgents = path.join(os.homedir(),'.claude/agents');
  sync(source, files, personal); verify(source, files, personal);
  sync(agents, agentFiles, personalAgents); verify(agents, agentFiles, personalAgents, false);
  console.log(`Installed: ${personal} and ${agentFiles.length} agents in ${personalAgents}`);
}
console.log(`PASS chang-diagram ${manifest.version}: ${files.length} source/package files match, ${agentFiles.length} agents`);
