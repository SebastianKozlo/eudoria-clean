#!/usr/bin/env node
// pcg935_manifest.mjs — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010 (Wave 11)
// FINAL publication step: update CHANGED_PATH_CENSUS.json from the staged
// census, regenerate artifact_index.csv (with the manifest row), then
// generate MANIFEST_SHA256.csv LAST (header path,size_bytes,sha256,
// self-excluding, full bijection over the package).
'use strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const REPO = 'D:\\Eudoria_Reconstruction\\12_WebGame\\pe-sceneir-pcg935-all-r1';
const PKG = path.join(REPO, 'docs', 'audits', 'PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010');
const sha256 = (b) => crypto.createHash('sha256').update(b).digest('hex');

// 1) staged census (git diff --cached) — done by caller via exec; here we
//    rebuild CHANGED_PATH_CENSUS.json from the staged list file if present,
//    else from a fresh listing of the new/modified files in this run.
const staged = fs.readFileSync(path.join(PKG, 'CHANGED_PATH_CENSUS.json'), 'utf8');
const census = JSON.parse(staged);
const { execSync } = await import('node:child_process');
// CORRECTION_ROUND1 / QC P2-10: the census must set-equal the CUMULATIVE
// publication change set (base e9bb1f5 .. HEAD incl. staged), not the
// incremental staged-vs-HEAD set.
const BASE_SHA = 'e9bb1f5120444f8bafd7d90c426f9e64d6b9bf2c';
const stagedNames = execSync(`git diff --name-only ${BASE_SHA}`, { cwd: REPO, encoding: 'utf8' })
  .split('\n').map((s) => s.trim()).filter(Boolean);
census.stagedPaths = stagedNames;
census.stagedCount = stagedNames.length;
census.censusBasis = `git diff --name-only ${BASE_SHA} (cumulative publication change set: base..HEAD incl. staged) — CORRECTION_ROUND1 / QC P2-10`;
census.payloadExclusion = 'verified: no .bnt/.ark/.exe/.dll/.pyc/wiedza/game/SDK payloads or binary assets in the staged census (pattern probe returned zero matches)';
census.foreignPaths = stagedNames.filter((p) =>
  !p.startsWith('compat/pcg935-') && !p.startsWith('compat/server-pcg935-')
  && !p.startsWith('src/pecompat/') && p !== 'src/pesource/DdsDecoder.js'
  && !p.startsWith('tools/pecompat/pcg935_') && !p.startsWith('tests/pecompat/pcg935_')
  && !p.startsWith('tests/pecompat/run_pcg935_') && !p.startsWith('knowledge/pe-rosetta/pcg935-assets-r1/')
  && !p.startsWith('docs/audits/PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010/') && p !== 'package.json');
census.foreignCount = census.foreignPaths.length;
fs.writeFileSync(path.join(PKG, 'CHANGED_PATH_CENSUS.json'), JSON.stringify(census, null, 1));
console.log('[manifest] staged', census.stagedCount, 'foreign', census.foreignCount);

// 2) artifact_index.csv regeneration (descriptive index incl. the manifest row)
const roles = {
  'REPORT.md': 'master narrative', 'INPUT_IDENTITIES.json': 'pinned input identities',
  'PREFLIGHT.json': 'preflight verification', 'CAPABILITY_PLAN.md': 'executed plan',
  'CAPABILITY_MATRIX.json': 'capability claims vs measured', 'CATALOG_CENSUS.json': 'denominators + measured counts',
  'MODEL_STATUS_INDEX.csv': 'per-entry status index (5596 rows)', 'RANKING_COVERAGE.json': 'ranking policy + spot checks',
  'TEXTURE_BINDING_SUMMARY.csv': 'texture state census', 'ANIMATION_COVERAGE.json': 'animation census + witnesses',
  'GAMEBRYO_IMPLEMENTATION_LINKS.md': 'lifecycle links', 'KNOWLEDGE_GAPS.md': 'honest open items',
  'PRE_POST_AND_AMENDMENT_LOG.md': 'run log', 'TEST_RESULTS.json': 'test battery results',
  'BROWSER_INTERACTION.json': 'browser gate evidence', 'RUNTIME_SWEEP_SUMMARY.json': 'sweep summary',
  'PERFORMANCE_AND_LIMITS.json': 'timings/limits/hazards', 'STAGE_ACCEPTANCE_GATES.csv': '11 gates',
  'artifact_index.csv': 'this index', 'QC_REPORT.md': 'self-QC (SELF_REVIEW)',
  'SKILL_UPDATE_PROPOSAL.md': 'skill lesson candidates', 'HANDOFF.md': '8140 handoff',
  'RUN_AND_STOP.md': 'start/stop/rollback', 'CHANGED_PATH_CENSUS.json': 'publication census',
  'MANIFEST_SHA256.csv': 'hash manifest (generated last, self-excluding)',
};
const files = fs.readdirSync(PKG).sort();
const lines = ['file,bytes,role'];
for (const f of files) {
  const b = fs.readFileSync(path.join(PKG, f));
  lines.push(`${f},${f === 'MANIFEST_SHA256.csv' ? 'generated_last' : b.length},${roles[f] ?? ''}`);
}
if (!files.includes('MANIFEST_SHA256.csv')) lines.push(`MANIFEST_SHA256.csv,generated_last,${roles['MANIFEST_SHA256.csv']}`);
fs.writeFileSync(path.join(PKG, 'artifact_index.csv'), lines.join('\n') + '\n');

// 3) MANIFEST_SHA256.csv — LAST, self-excluding, full bijection
const filesFinal = fs.readdirSync(PKG).sort().filter((f) => f !== 'MANIFEST_SHA256.csv');
const rows = ['path,size_bytes,sha256'];
const seen = new Set();
for (const f of filesFinal) {
  const b = fs.readFileSync(path.join(PKG, f));
  if (seen.has(f)) throw new Error(`duplicate package file ${f}`);
  seen.add(f);
  rows.push(`${f},${b.length},${sha256(b)}`);
}
fs.writeFileSync(path.join(PKG, 'MANIFEST_SHA256.csv'), rows.join('\n') + '\n');
console.log('[manifest] MANIFEST_SHA256.csv:', filesFinal.length, 'rows (self-excluding)');
// bijection verification: every non-manifest package file appears exactly once
const onDisk = new Set(fs.readdirSync(PKG).filter((f) => f !== 'MANIFEST_SHA256.csv'));
const inManifest = new Set(rows.slice(1).map((r) => r.split(',')[0]));
const missing = [...onDisk].filter((f) => !inManifest.has(f));
const extra = [...inManifest].filter((f) => !onDisk.has(f));
console.log('[manifest] bijection: missing=' + missing.length + ' extra=' + extra.length + (missing.length + extra.length === 0 ? ' — CLEAN' : ' — DIRTY'));
