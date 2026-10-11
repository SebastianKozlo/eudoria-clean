// correction_matrix.test.mjs — the seven §6 observations + the two §7 cases of
// contract PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011, as POST regression
// tests against the corrected tool. All inputs are synthetic fixtures (fixtures.mjs).
import test from 'node:test';
import assert from 'node:assert/strict';
import os from 'node:os';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { analyzeBlob, Budget } from '../placement_probe.mjs';
import * as FX from './fixtures.mjs';

const TOOL = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'placement_probe.mjs');
const HELPER = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'ids_from_export.mjs');
const WORKTREE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..', '..');
const sets = { S_tpl: new Set([4057, 4058]), S_model: new Set([218757]) };

function mkRepo(root) { const repo = path.join(root, 'repo'); fs.mkdirSync(path.join(repo, 'src/pesource'), { recursive: true }); fs.writeFileSync(path.join(repo, 'package.json'), '{"type":"module"}'); fs.writeFileSync(path.join(repo, 'src/pesource/Bnt2Archive.js'), FX.shimBntSrc); fs.writeFileSync(path.join(repo, 'src/pesource/ArkArchive.js'), FX.shimArkSrc); return repo; }
function cliRun(root, { repo, args, inputs }) {
  const out = path.join(root, 'out');
  const full = ['--repo', repo, '--ids', path.join(root, 'ids.json'), '--out', out, ...inputs.flatMap(n => ['--input', path.join(root, n)]), ...args];
  const res = spawnSync(process.execPath, [TOOL, ...full], { encoding: 'utf8' });
  let summary = null, sources = null;
  try { summary = JSON.parse(fs.readFileSync(path.join(out, 'SUMMARY.json'), 'utf8')); } catch {}
  try { sources = JSON.parse(fs.readFileSync(path.join(out, 'sources.json'), 'utf8')); } catch {}
  return { exitCode: res.status, stdout: res.stdout, stderr: res.stderr, summary, sources, outDirExists: fs.existsSync(out) };
}

// ---- O1 INVALID_NUMERIC_CONFIG ------------------------------------------------
test('O1: invalid numeric config fails closed (INVALID_CONFIGURATION, nonzero exit, SCAN_STARTED=NO)', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'pe-t-o1-'));
  try {
    const repo = mkRepo(root); fs.writeFileSync(path.join(root, 'ids.json'), JSON.stringify({ S_tpl: [4057, 4058] }));
    fs.writeFileSync(path.join(root, 'raw.vfs'), FX.records80());
    const bad = cliRun(root, { repo, args: ['--max-stride', 'not-a-number'], inputs: ['raw.vfs'] });
    assert.notEqual(bad.exitCode, 0, 'exit must be nonzero');
    assert.match(bad.stderr, /INVALID_CONFIGURATION/);
    assert.match(bad.stderr, /SCAN_STARTED=NO/);
    assert.equal(bad.outDirExists, false, 'no output dir may be created');
    const miss = cliRun(root, { repo, args: ['--max-stride'], inputs: ['raw.vfs'] });
    assert.notEqual(miss.exitCode, 0); assert.match(miss.stderr, /SCAN_STARTED=NO/);
    const nanExport = { ...{}, ...{ maxStride: NaN } };
    assert.throws(() => analyzeBlob(FX.records80(), sets, nanExport), /INVALID_CONFIGURATION/);
    // legal boundary values must NOT be rejected (false-rejection control)
    const okCfg = { maxHeader: 0, posLo: -200000, posHi: 200000, minPosRate: 0.9, minIdRate: 0.5, minDistinctId: 2, top: 50 };
    const r = analyzeBlob(FX.records80Headerless(), sets, okCfg);
    assert.ok(r.candidates.length > 0, 'legal maxHeader=0 + negative posLo config must still find the headerless synthetic candidate');
    const okCfg2 = { maxHeader: 64, posLo: -200000, posHi: 200000, minPosRate: 0.88, minIdRate: 0.35, minDistinctId: 2, top: 50 };
    const r2 = analyzeBlob(FX.records80(), sets, okCfg2);
    assert.ok(r2.candidates.length > 0, 'default-legal config finds the 16-byte-header synthetic candidate');
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

// ---- O2 EXCLUSION_CENSUS -----------------------------------------------------
test('O2: every declared entry has exactly one disposition and DECLARED_ENTRIES reconciles', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'pe-t-o2-'));
  try {
    const repo = mkRepo(root); fs.writeFileSync(path.join(root, 'ids.json'), JSON.stringify({ S_tpl: [4057, 4058] }));
    const good = FX.records80(); const tiny = Buffer.alloc(8, 0xff);
    fs.writeFileSync(path.join(root, 'c.bnt'), FX.realBnt2([{ name: 'scan.rec', data: good }, { name: 'tex.nif', data: good }, { name: 'tiny.rec', data: tiny }, { name: 'huge.rec', data: good }]));
    const a = cliRun(root, { repo, args: [], inputs: ['c.bnt'] });
    assert.equal(a.exitCode, 0, a.stderr);
    const c = a.summary.exclusionCensus[0];
    assert.equal(c.parseStatus, 'OK');
    assert.equal(c.declaredEntryCount, 4);
    assert.equal(c.dispositionTotal, 4, 'disposition sum must equal declared entries');
    assert.equal(c.censusOk, true);
    assert.equal(c.dispositionCounts.SCANNED, 2);
    assert.equal(c.dispositionCounts.FILTERED_EXTENSION, 1);
    assert.equal(c.dispositionCounts.TOO_SMALL, 1);
    const b = cliRun(root, { repo, args: ['--entry-regex', '^scan\\.rec$'], inputs: ['c.bnt'] });
    const c2 = b.summary.exclusionCensus[0];
    assert.equal(c2.dispositionCounts.FILTERED_REGEX, 3);
    assert.equal(c2.dispositionCounts.SCANNED, 1);
    assert.equal(c2.dispositionTotal, 4);
    // unit separation: container vs entries vs payloads vs candidate tables
    assert.equal(a.summary.sourceCount, 1, 'one container');
    assert.equal(c.scannedPayloadCount, 2, 'two scanned payloads — a container is not a payload');
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

// ---- O3 SAMPLE_VS_CENSUS ------------------------------------------------------
test('O3: sample does not impersonate a full evaluation; full census reproduces known table quality', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'pe-t-o3-'));
  try {
    const repo = mkRepo(root); fs.writeFileSync(path.join(root, 'ids.json'), JSON.stringify({ S_tpl: [4057, 4058] }));
    fs.writeFileSync(path.join(root, 'big.vfs'), FX.poisoned4800());
    const r = cliRun(root, { repo, args: [], inputs: ['big.vfs'] });
    assert.equal(r.exitCode, 0, r.stderr);
    const top = JSON.parse(fs.readFileSync(path.join(root, 'out', 'candidates_top.json'), 'utf8'));
    const c = top.find(x => x.header === 16 && x.stride === 32 && x.idOffset === 0);
    assert.ok(c, 'the stride-32 candidate must be found');
    assert.equal(c.tableRowCount, 4800);
    assert.equal(c.sampledRowCount, 1200);
    assert.equal(c.idRate, 1, 'sample sees a 100% valid ID column');
    assert.equal(c.censusStatus, 'FULL_CENSUS', 'all 4800 rows fit the census budget');
    assert.equal(c.fullCensusRowCount, 4800);
    assert.equal(c.fullCensusIdRate, 0.25, 'full census reproduces the known table quality (25%)');
    assert.ok(Math.abs(c.sampleXyzFiniteRate - 1) < 1e-12);
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

// ---- O4 SINGLE_DEFINITION_TABLE ----------------------------------------------
test('O4: --min-distinct-id 1 detects a single-definition table; default filter restriction is explicit', () => {
  const b = FX.singleIdTable(80);
  const atOne = analyzeBlob(b, sets, { minDistinctId: 1, minIdRate: 0.5, maxStride: 128, minPosRate: 0.9, top: 50 });
  assert.ok(atOne.candidates.length > 0, 'minDistinctId=1 must detect the all-4057 table');
  assert.ok(atOne.candidates.every(x => x.idDistinct === 1));
  const atDefault = analyzeBlob(b, sets, { minIdRate: 0.5, maxStride: 128, minPosRate: 0.9, top: 50 });
  assert.equal(atDefault.candidates.length, 0, 'default minDistinctId=2 excludes it — explicit coverage restriction, single interface only');
});

// ---- O5 INTEGER_COUNTERS_AS_FLOATS -------------------------------------------
test('O5: u32 counters read as subnormal f32 are visible candidates with full diagnostics, never placement', () => {
  const b = FX.countersAsFloats();
  const r = analyzeBlob(b, sets, { minIdRate: 0.5, maxStride: 128, minPosRate: 0.88, top: 50 });
  const c = r.candidates.find(x => x.xyzOffset === 4);
  assert.ok(c, 'candidate is allowed');
  assert.ok(!/PLACEMENT_CONFIRMED|HISTORICAL_PLACEMENT/.test(JSON.stringify(c)), 'candidate carries no placement claim');
  const census = c.fullCensus ?? c.sampleStats;
  assert.ok(census.perAxis.every(a => a.subnormalCount > 0), 'subnormal f32 counts must be visible');
  assert.ok(census.perAxis.every(a => a.finiteRate > 0));
  assert.ok(census.perAxis.every(a => typeof a.alternativeU32Interpretation.min === 'number' && a.alternativeU32Interpretation.max > 0), 'ALTERNATIVE_U32_INTERPRETATION of the same bytes must be reported');
  assert.ok(census.perAxis[0].alternativeU32Interpretation.min >= 1 && census.perAxis[2].alternativeU32Interpretation.max <= 5079, 'the competing u32 reading is the counter sequence');
  // no promotion: the candidate carries no placement claim anywhere
  assert.equal(c.censusStatus, 'FULL_CENSUS');
});

// ---- O6 ACTUAL_PROJECT_ADAPTERS ----------------------------------------------
test('O6: positive RAW/BNT2/ARK smoke with the actual BASE adapters on synthetic bytes', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'pe-t-o6-'));
  try {
    fs.writeFileSync(path.join(root, 'ids.json'), JSON.stringify({ S_tpl: [4057, 4058] }));
    const good = FX.records80();
    fs.writeFileSync(path.join(root, 'raw.vfs'), good);
    fs.writeFileSync(path.join(root, 'test.bnt'), FX.realBnt2([{ name: '4057.rec', data: good }]));
    fs.writeFileSync(path.join(root, 'test.ark'), FX.realArk([{ name: '4057.rec', data: good }]));
    const res = spawnSync(process.execPath, [TOOL, '--repo', WORKTREE, '--ids', path.join(root, 'ids.json'), '--out', path.join(root, 'out'), '--input', path.join(root, 'raw.vfs'), '--input', path.join(root, 'test.bnt'), '--input', path.join(root, 'test.ark')], { encoding: 'utf8' });
    assert.equal(res.status, 0, res.stderr);
    const summary = JSON.parse(fs.readFileSync(path.join(root, 'out', 'SUMMARY.json'), 'utf8'));
    assert.equal(summary.sourceCount, 3);
    assert.ok(summary.candidateCount >= 3);
    const csv = fs.readFileSync(path.join(root, 'out', 'placement_candidates.csv'), 'utf8');
    for (const n of ['raw.vfs', 'test.bnt', 'test.ark']) assert.match(csv, new RegExp(n.replace('.', '\\.')));
    assert.match(csv, /CANDIDATE_ONLY_NOT_PLACEMENT_PROOF/);
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

// ---- O7 NUMERIC_DAT_MODEL_NAME_PATTERN -----------------------------------------
test('O7: .dat model archive rejection is explicit; non-numeric .nif names are counted, not silent', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'pe-t-o7-'));
  try {
    fs.writeFileSync(path.join(root, 'tpl.csv'), FX.idsCsv('templateId'));
    fs.writeFileSync(path.join(root, 'models.bnt'), FX.realBnt2([
      { name: '123.nif', data: Buffer.alloc(16, 0xff) }, { name: '218757.nif', data: Buffer.alloc(16, 0xff) }, { name: 'prop_a.nif', data: Buffer.alloc(16, 0xff) }]));
    fs.writeFileSync(path.join(root, 'models.dat'), Buffer.from('dummy'));
    const run = args => spawnSync(process.execPath, [HELPER, ...args], { encoding: 'utf8' });
    const dat = run(['--csv', path.join(root, 'tpl.csv'), '--id-column', 'templateId', '--repo', WORKTREE, '--model-archive', path.join(root, 'models.dat'), '--out', path.join(root, 'out.json')]);
    assert.notEqual(dat.status, 0);
    assert.match(dat.stderr, /must be \.bnt or \.ark/);
    const bnt = run(['--csv', path.join(root, 'tpl.csv'), '--id-column', 'templateId', '--repo', WORKTREE, '--model-archive', path.join(root, 'models.bnt'), '--out', path.join(root, 'out.json')]);
    assert.equal(bnt.status, 0, bnt.stderr);
    const console_ = JSON.parse(bnt.stdout);
    assert.equal(console_.modelIds, 2);
    assert.equal(console_.modelArchives[0].nifEntries, 2);
    assert.equal(console_.modelArchives[0].nonNumericNamesExcluded, 1, 'the non-numeric name is excluded AND counted');
    const out = JSON.parse(fs.readFileSync(path.join(root, 'out.json'), 'utf8'));
    assert.deepEqual(out.S_model, [123, 218757]);
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

// ---- §7 LAYOUT_ATTEMPTS_VS_ADMITTED --------------------------------------------
test('S7a: LAYOUT_ATTEMPTS=126 counted before filters; LAYOUTS_ADMITTED=0; lowered limit stops early', () => {
  const b = FX.layoutBuffer10007();
  const r = analyzeBlob(b, sets, { maxHeader: 0, maxStride: 512 });
  assert.equal(r.stats.layoutAttempts, 126, 'every visited (source,header,stride) before divisibility/minRows');
  assert.equal(r.stats.layoutsAdmitted, 0);
  assert.equal(r.stats.layoutsTested, 0, 'legacy post-filter field stays 0');
  assert.equal(r.stats.budgetExhausted, false);
  // lowered limit (threshold LOWERED, ceiling untouched): stops before 126
  const r2 = analyzeBlob(b, sets, { maxHeader: 0, maxStride: 512, budgetThresholds: { layoutEvaluations: 60 } });
  assert.equal(r2.stats.layoutAttempts, 61, 'the attempt that exceeds the lowered limit is recorded, then the scan stops');
  assert.equal(r2.stats.budgetExhausted, true);
  assert.equal(r2.stats.coverage, 'PARTIAL');
  assert.ok(r2.budget.exhausted.includes('LAYOUT_EVALUATIONS'));
  assert.ok(r2.budget.refusals.length >= 1);
  const refusal = r2.budget.refusals[r2.budget.refusals.length - 1];
  assert.equal(refusal.kind, 'LAYOUT_EVALUATIONS');
  assert.equal(refusal.layoutAttempts, 61, 'refusal moment recorded with actual counters');
});

// ---- §7 XYZ_COLUMN_MEAN_VS_ROW_TRIPLE_RATE -------------------------------------
test('S7b: joint XYZ_FINITE_RATE=56/80 distinct from the 0.9 legacy column mean', () => {
  const b = FX.xyzFixture80();
  const r = analyzeBlob(b, sets, { minPosRate: 0.88, minIdRate: 0.35, top: 50 });
  const c = r.candidates.find(x => x.header === 16 && x.stride === 32 && x.idOffset === 0 && x.idWidth === 2 && x.xyzOffset === 4);
  assert.ok(c, 'candidate found');
  assert.equal(c.xyzRate, 0.9, 'legacy xyzRate stays the historical column-mean measurement');
  assert.equal(c.sampleStats.xyzFiniteRate, 0.7, 'joint triple rate on the sample (all 80 rows sampled)');
  assert.equal(c.sampleStats.completeFiniteTriples, 56);
  assert.equal(c.sampleStats.denominator, 80);
  assert.ok(Math.abs(c.sampleStats.perAxis[0].finiteRate - 0.9) < 1e-12);
  assert.equal(c.sampleStats.perAxis[0].nanCount, 8);
  assert.equal(c.censusStatus, 'FULL_CENSUS');
  assert.equal(c.fullCensusXyzFiniteRate, 0.7);
  assert.equal(c.fullCensusRowCount, 80);
});