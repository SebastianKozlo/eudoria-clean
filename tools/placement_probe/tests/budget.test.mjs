// budget.test.mjs — §8 budget execution tests (contract PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011).
// Thresholds are LOWERED for short fixtures; the canonical ceilings are never raised.
// Each limit: legal boundary, exceed attempt, and (for shared per-invocation limits)
// aggregation across at least two inputs within ONE invocation.
import test from 'node:test';
import assert from 'node:assert/strict';
import os from 'node:os';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { analyzeBlob, Budget, BUDGET_CEILINGS } from '../placement_probe.mjs';
import * as FX from './fixtures.mjs';

const TOOL = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'placement_probe.mjs');
const sets = { S_tpl: new Set([4057, 4058]), S_model: new Set([218757]) };
function mkRepo(root) { const repo = path.join(root, 'repo'); fs.mkdirSync(path.join(repo, 'src/pesource'), { recursive: true }); fs.writeFileSync(path.join(repo, 'package.json'), '{"type":"module"}'); fs.writeFileSync(path.join(repo, 'src/pesource/Bnt2Archive.js'), FX.shimBntSrc); fs.writeFileSync(path.join(repo, 'src/pesource/ArkArchive.js'), FX.shimArkSrc); fs.writeFileSync(path.join(root, 'ids.json'), JSON.stringify({ S_tpl: [4057, 4058] })); return repo; }
function cli(root, repo, inputs, args) {
  const out = path.join(root, 'out');
  const res = spawnSync(process.execPath, [TOOL, '--repo', repo, '--ids', path.join(root, 'ids.json'), '--out', out, ...inputs.flatMap(n => ['--input', path.join(root, n)]), ...args], { encoding: 'utf8' });
  let summary = null; try { summary = JSON.parse(fs.readFileSync(path.join(out, 'SUMMARY.json'), 'utf8')); } catch {}
  return { exitCode: res.status, stderr: res.stderr, summary };
}
const tmp = () => fs.mkdtempSync(path.join(os.tmpdir(), 'pe-t-b-'));

test('B1: SYNTHETIC_INPUTS — legal 32 admitted; 33rd admission attempt refused before its scan; aggregation across entries', () => {
  const root = tmp(); try {
    const repo = mkRepo(root);
    // 33 entries, each a small valid record table (16+8*32=272B): 32 admitted, 33rd refused
    const entries = []; for (let i = 0; i < 33; i++) entries.push({ name: `e${i}.rec`, data: FX.recordsTwoIdSmall() });
    fs.writeFileSync(path.join(root, 'many.bnt'), FX.realBnt2(entries));
    fs.writeFileSync(path.join(root, 'one.bnt'), FX.realBnt2([{ name: 'x.rec', data: FX.recordsTwoIdSmall() }]));
    const r = cli(root, repo, ['many.bnt', 'one.bnt'], []);
    assert.equal(r.exitCode, 0, r.stderr);
    assert.equal(r.summary.budgets.used.syntheticInputs, 32, 'exactly the legal boundary admitted');
    assert.ok(r.summary.budgets.exhausted.includes('SYNTHETIC_INPUTS'));
    assert.equal(r.summary.budgets.coverage, 'PARTIAL');
    assert.equal(r.summary.status, 'BUDGET_EXHAUSTED_COVERAGE_PARTIAL', 'exhaustion is not NO_CANDIDATE');
    const c = r.summary.exclusionCensus[0];
    assert.equal(c.declaredEntryCount, 33);
    assert.equal(c.dispositionCounts.OVER_BUDGET, 1);
    assert.equal(c.dispositionCounts.SCANNED, 32);
    assert.equal(c.dispositionTotal, 33);
    assert.equal(r.summary.candidateCount > 0, true, 'the 32 scanned payloads produced candidates — work was done before the refusal');
    assert.ok(r.summary.budgets.refusals.some(x => x.kind === 'SYNTHETIC_INPUTS' && x.syntheticInputs === 32), 'refusal moment recorded');
    assert.equal(r.summary.exclusionCensus.length, 2, 'two input containers recorded');
    const c1 = r.summary.exclusionCensus[1];
    assert.equal(c1.declaredEntryCount, 1);
    assert.equal(c1.dispositions[0].disposition, 'OVER_BUDGET', 'the SECOND input aggregation is honest: its single entry is refused after the shared cap is full');
    assert.equal(c1.censusOk, true);
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('B2: SCANNED_BYTES — reservation before read; aggregation across two raw inputs', () => {
  const root = tmp(); try {
    const repo = mkRepo(root);
    fs.writeFileSync(path.join(root, 'a.vfs'), FX.records80()); // 16+80*32 = 2576 B
    fs.writeFileSync(path.join(root, 'b.vfs'), FX.records80());
    const cap = 2576 + 100; // first fits, second refused (aggregated within one invocation)
    const r = cli(root, repo, ['a.vfs', 'b.vfs'], ['--budget-scanned-bytes', String(cap)]);
    assert.equal(r.summary.budgets.used.scannedBytes, 2576, 'first payload charged');
    assert.ok(r.summary.budgets.exhausted.includes('SCANNED_BYTES'));
    assert.equal(r.summary.exclusionCensus.length, 2);
    assert.equal(r.summary.exclusionCensus[0].dispositions[0].disposition, 'SCANNED');
    assert.equal(r.summary.exclusionCensus[1].dispositions[0].disposition, 'OVER_BUDGET');
    // legal boundary: cap exactly equal to the sum admits both
    const r2 = cli(root, repo, ['a.vfs', 'b.vfs'], ['--budget-scanned-bytes', '5152']);
    assert.equal(r2.summary.budgets.used.scannedBytes, 5152);
    assert.equal(r2.summary.budgets.coverage, 'FULL');
    assert.equal(r2.summary.exclusionCensus[1].dispositions[0].disposition, 'SCANNED');
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('B3: LAYOUT_EVALUATIONS — aggregation across two inputs in one invocation; honest dispositions', () => {
  const root = tmp(); try {
    const repo = mkRepo(root);
    fs.writeFileSync(path.join(root, 'a.vfs'), FX.records80());
    fs.writeFileSync(path.join(root, 'b.vfs'), FX.records80());
    // aggregation across TWO inputs: each input uses 2142 attempts at max-stride 512;
    // cap 3000 stops the SECOND input mid-analysis (attempts 2143..3001)
    const r = cli(root, repo, ['a.vfs', 'b.vfs'], ['--budget-layout-evals', '3000', '--max-stride', '512']);
    assert.equal(r.summary.budgets.used.layoutAttempts, 3001, 'the exceeding attempt is recorded once, then the invocation stops');
    assert.ok(r.summary.budgets.exhausted.includes('LAYOUT_EVALUATIONS'));
    assert.equal(r.summary.exclusionCensus[0].dispositions[0].disposition, 'SCANNED', 'first input fully analyzed');
    assert.equal(r.summary.exclusionCensus[1].dispositions[0].disposition, 'SCANNED', 'second input was admitted and partially analyzed (mid-analysis stop) — SCANNED stands');
    const skips = fs.readFileSync(path.join(root, 'out', 'scan_skips.csv'), 'utf8');
    assert.ok(skips.includes('BUDGET_EXHAUSTED'), 'the budget stop is recorded honestly');
    // pre-exhaustion case: cap below one input's usage; the second input's payload is
    // admitted but NEVER analyzed — its disposition must be corrected to OVER_BUDGET
    const r0 = cli(root, repo, ['a.vfs', 'b.vfs'], ['--budget-layout-evals', '700', '--max-stride', '512']);
    assert.equal(r0.summary.budgets.used.layoutAttempts, 701);
    assert.equal(r0.summary.exclusionCensus[1].dispositions[0].disposition, 'OVER_BUDGET', 'admitted-but-never-analyzed payload is NOT reported as SCANNED');
    assert.equal(r0.summary.exclusionCensus[1].censusOk, true, 'disposition census still reconciles');
    // legal boundary: default ceilings do not exhaust
    const r2 = cli(root, repo, ['a.vfs', 'b.vfs'], []);
    assert.equal(r2.summary.budgets.coverage, 'FULL');
    assert.equal(r2.summary.budgets.used.layoutAttempts, 4284, 'two full inputs: 2 x 2142 aggregated attempts');
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});
test('B4: FULL_CENSUS_ROWS — finalist census charged per candidate-row unit; aggregation across two inputs', () => {
  const root = tmp(); try {
    const repo = mkRepo(root);
    fs.writeFileSync(path.join(root, 'a.vfs'), FX.records80());
    fs.writeFileSync(path.join(root, 'b.vfs'), FX.records80());
    // each invocation admits two payloads; each has multiple finalists x 80 rows.
    const r = cli(root, repo, ['a.vfs', 'b.vfs'], ['--budget-census-rows', '160', '--top', '2']);
    // 160 rows allow 2 finalist censuses of 80; any further finalist -> PARTIAL_BUDGET_EXHAUSTED
    assert.ok(r.summary.budgets.used.fullCensusRows >= 80);
    const top = JSON.parse(fs.readFileSync(path.join(root, 'out', 'candidates_top.json'), 'utf8'));
    assert.ok(top.some(c => c.censusStatus === 'PARTIAL_BUDGET_EXHAUSTED'), 'at least one finalist census is refused when the shared budget is exhausted');
    assert.ok(top.some(c => c.censusStatus === 'FULL_CENSUS'), 'earlier finalists consumed the budget first (aggregation across inputs)');
    // legal boundary: default 50000 covers everything here
    const r2 = cli(root, repo, ['a.vfs', 'b.vfs'], []);
    assert.equal(r2.summary.budgets.coverage, 'FULL');
    const top2 = JSON.parse(fs.readFileSync(path.join(root, 'out', 'candidates_top.json'), 'utf8'));
    assert.ok(top2.every(c => c.censusStatus === 'FULL_CENSUS'));
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('B5: RETAINED_CANDIDATES — peak across all structures capped; exhaustion is PARTIAL not NO_CANDIDATE', () => {
  const root = tmp(); try {
    const repo = mkRepo(root);
    fs.writeFileSync(path.join(root, 'a.vfs'), FX.records80());
    fs.writeFileSync(path.join(root, 'b.vfs'), FX.records80());
    const r = cli(root, repo, ['a.vfs'], ['--budget-retained-candidates', '4']);
    assert.ok(r.summary.budgets.used.peakRetainedCandidates <= 4, 'peak tracked and capped');
    assert.ok(r.summary.budgets.exhausted.includes('RETAINED_CANDIDATES'));
    assert.equal(r.summary.budgets.coverage, 'PARTIAL');
    assert.ok(r.summary.candidateCount > 0, 'candidates were retained before the cap — exhaustion is not NO_CANDIDATE');
    // legal boundary: cap above the natural candidate count does not exhaust
    const r2 = cli(root, repo, ['a.vfs'], ['--budget-retained-candidates', '256']);
    assert.equal(r2.summary.budgets.coverage, 'FULL');
    // aggregation across TWO inputs: the GLOBAL peak (main rows + per-call lists) stays under the cap
    const r3 = cli(root, repo, ['a.vfs', 'b.vfs'], ['--budget-retained-candidates', '4']);
    assert.ok(r3.summary.budgets.used.peakRetainedCandidates <= 4, 'global peak across all structures and both inputs is capped');
    assert.ok(r3.summary.budgets.exhausted.includes('RETAINED_CANDIDATES'));
    assert.equal(r3.summary.budgets.coverage, 'PARTIAL');
    assert.ok(r3.summary.candidateCount > 0);
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('B6: budget thresholds cannot exceed the canonical ceilings (no raised ceilings)', () => {
  assert.throws(() => analyzeBlob(FX.records80(), sets, { budgetThresholds: { layoutEvaluations: 100001 } }), /INVALID_CONFIGURATION.*ceiling/);
  assert.throws(() => analyzeBlob(FX.records80(), sets, { budgetThresholds: { syntheticInputs: 33 } }), /INVALID_CONFIGURATION/);
  const root = tmp(); try {
    const repo = mkRepo(root); fs.writeFileSync(path.join(root, 'a.vfs'), FX.records80());
    const r = cli(root, repo, ['a.vfs'], ['--budget-layout-evals', '100001']);
    assert.notEqual(r.exitCode, 0);
    assert.match(r.stderr || '', /INVALID_CONFIGURATION/);
    assert.match(r.stderr || '', /SCAN_STARTED=NO/);
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('B7: Budget class — no-reset-per-payload aggregation semantics and separate control/container byte accounting', () => {
  const b = new Budget({ scannedBytes: 500 });
  assert.equal(b.admitPayload(300, 'x'), true);
  assert.equal(b.admitPayload(300, 'y'), false, 'counters do NOT reset between payloads');
  assert.equal(b.scannedBytes, 300);
  assert.deepEqual(b.exhausted, ['SCANNED_BYTES']);
  assert.equal(b.coverage, 'PARTIAL');
  // container-read bytes and control work bytes are accounted separately from scanned payload bytes
  const b2 = new Budget();
  b2.containerReadBytes += 1234; b2.controlWorkBytes += 512;
  const s = b2.summary();
  assert.equal(s.containerReadBytes, 1234); assert.equal(s.controlWorkBytes, 512);
  assert.equal(s.used.scannedBytes, 0, 'container reads and control work are not hidden inside SCANNED_BYTES');
});