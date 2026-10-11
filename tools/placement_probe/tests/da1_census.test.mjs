// da1_census.test.mjs — DA-1 (R2-5 P2) semantically truthful census regression tests
// (contract PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011, section C, cases 1-5).
// All containers are synthetic bytes read through the ACTUAL project adapters
// (src/pesource/Bnt2Archive.js / ArkArchive.js from the worktree root) — no shims.
import test from 'node:test';
import assert from 'node:assert/strict';
import os from 'node:os';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { censusGate, analyzeBlob, Budget } from '../placement_probe.mjs';
import * as FX from './fixtures.mjs';

const TOOL = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'placement_probe.mjs');
const WORKTREE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..', '..');
const sets = { S_tpl: new Set([4057, 4058]), S_model: new Set([218757]) };

function mkIds(root) { fs.writeFileSync(path.join(root, 'ids.json'), JSON.stringify({ S_tpl: [4057, 4058], S_model: [218757] })); return path.join(root, 'ids.json'); }
function cli(root, inputs, args = []) {
  const out = path.join(root, 'out_' + Math.random().toString(36).slice(2, 8));
  const res = spawnSync(process.execPath, [TOOL, '--repo', WORKTREE, '--ids', path.join(root, 'ids.json'), '--out', out, ...inputs.flatMap(n => ['--input', path.join(root, n)]), ...args], { encoding: 'utf8', timeout: 120000 });
  let summary = null; try { summary = JSON.parse(fs.readFileSync(path.join(out, 'SUMMARY.json'), 'utf8')); } catch {}
  return { exitCode: res.status, stderr: res.stderr, summary };
}
const tmp = () => fs.mkdtempSync(path.join(os.tmpdir(), 'pe-t-da1-'));

test('DA1-C1: BNT2 four entries, layout limit 100 — first started/PARTIAL, whole tail OVER_BUDGET/NOT_ANALYZED, scannedPayloadCount=1', () => {
  const root = tmp(); try {
    mkIds(root);
    fs.writeFileSync(path.join(root, 'four.bnt'), FX.realBnt2([0, 1, 2, 3].map(i => ({ name: `e${i}.rec`, data: FX.records80() }))));
    const r = cli(root, ['four.bnt'], ['--budget-layout-evals', '100']);
    assert.equal(r.exitCode, 0, r.stderr);
    const c = r.summary.exclusionCensus[0];
    assert.equal(c.declaredEntryCount, 4);
    assert.equal(c.dispositionTotal, 4);
    assert.equal(c.censusOk, true);
    assert.equal(c.scannedPayloadCount, 1, 'only the payload whose analysis actually started counts as scanned');
    const d = c.dispositions;
    // whole tail controlled: every entry has exactly one disposition and a consistent state vector
    assert.equal(d[0].disposition, 'SCANNED'); assert.equal(d[0].analysisStarted, true); assert.equal(d[0].analysisStatus, 'PARTIAL');
    assert.ok(d[0].admitted === true && d[0].payloadRead === true);
    for (const e of d.slice(1)) {
      assert.equal(e.disposition, 'OVER_BUDGET', 'entry ' + e.entryIndex + ' was never analyzed');
      assert.equal(e.analysisStarted, false);
      assert.equal(e.analysisStatus, 'NOT_ANALYZED');
      assert.match(String(e.detail), /budget exhausted before analysis/);
    }
    assert.equal(c.analysisStatusCounts.PARTIAL, 1); assert.equal(c.analysisStatusCounts.NOT_ANALYZED, 3);
    assert.equal(c.admittedCount, 4); assert.equal(c.payloadReadCount, 4, 'all four were admitted+read BEFORE the exhaustion happened mid-analysis');
    assert.equal(r.summary.budgets.used.layoutAttempts, 101);
    assert.equal(r.summary.budgets.coverage, 'PARTIAL');
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('DA1-C2: ARK equivalent + >=2 declared files — unopened next files are NOT_OPENED_BUDGET with UNKNOWN_ENTRY_COUNT, no invented catalog', () => {
  const root = tmp(); try {
    mkIds(root);
    fs.writeFileSync(path.join(root, 'first.ark'), FX.realArk([{ name: 'a.rec', data: FX.records80() }, { name: 'b.rec', data: FX.records80() }, { name: 'c.rec', data: FX.records80() }, { name: 'd.rec', data: FX.records80() }]));
    fs.writeFileSync(path.join(root, 'second.ark'), FX.realArk([{ name: 'x.rec', data: FX.records80() }]));
    fs.writeFileSync(path.join(root, 'third.bnt'), FX.realBnt2([{ name: 'y.rec', data: FX.records80() }]));
    // retained cap 4: first.ark fills the global retention; second/third are never opened
    const r = cli(root, ['first.ark', 'second.ark', 'third.bnt'], ['--budget-retained-candidates', '4']);
    assert.equal(r.exitCode, 0, r.stderr);
    assert.equal(r.summary.exclusionCensus.length, 3, 'all three declared files are recorded');
    const c1 = r.summary.exclusionCensus[0];
    assert.equal(c1.parseStatus, 'OK');
    assert.equal(c1.containerKind, '.ark', 'real ArkArchive adapter path');
    assert.equal(c1.scannedPayloadCount, 4, 'all four ARK entries analyzed');
    assert.ok(c1.dispositions.every(x => x.disposition === 'SCANNED' && x.analysisStarted === true));
    const c2 = r.summary.exclusionCensus[1], c3 = r.summary.exclusionCensus[2];
    for (const c of [c2, c3]) {
      assert.equal(c.parseStatus, 'NOT_OPENED_BUDGET');
      assert.equal(c.declaredEntryCount, 'UNKNOWN_ENTRY_COUNT', 'never opened — entry count must NOT be invented');
      assert.equal(c.declaredEntryCountState, 'UNKNOWN_ENTRY_COUNT');
      assert.deepEqual(c.dispositions, [], 'no fabricated entry catalog for an unopened container');
      assert.equal(c.scannedPayloadCount, 0);
      assert.equal(c.censusOk, null, 'no entry-level census claim is made for an unopened file');
      assert.match(String(c.unopenedReason), /never opened/);
    }
    const skipCsv = fs.readdirSync(root).filter(n => n.startsWith('out_')).map(n => fs.readFileSync(path.join(root, n, 'scan_skips.csv'), 'utf8')).find(t => t.includes('NOT_OPENED_BUDGET'));
    assert.ok(skipCsv, 'the unopened files are recorded in scan_skips.csv');
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('DA1-C3: duplicate entry names are keyed by stable entryIndex identity, never by name', () => {
  const root = tmp(); try {
    mkIds(root);
    // four entries, THREE share the name dup.rec — only entryIndex tells them apart
    fs.writeFileSync(path.join(root, 'dup.bnt'), FX.realBnt2([{ name: 'dup.rec', data: FX.records80() }, { name: 'dup.rec', data: FX.records80() }, { name: 'other.rec', data: FX.records80() }, { name: 'dup.rec', data: FX.records80() }]));
    const r = cli(root, ['dup.bnt'], ['--budget-layout-evals', '100']);
    assert.equal(r.exitCode, 0, r.stderr);
    const c = r.summary.exclusionCensus[0];
    assert.equal(c.declaredEntryCount, 4);
    assert.equal(c.scannedPayloadCount, 1);
    const byIdx = new Map(c.dispositions.map(d => [d.entryIndex, d]));
    assert.deepEqual([...byIdx.keys()].sort(), [0, 1, 2, 3], 'every duplicate name keeps its own stable entryIndex');
    assert.equal(byIdx.get(0).disposition, 'SCANNED'); assert.equal(byIdx.get(0).analysisStarted, true);
    for (const i of [1, 2, 3]) {
      assert.equal(byIdx.get(i).disposition, 'OVER_BUDGET');
      assert.equal(byIdx.get(i).analysisStarted, false);
      assert.equal(byIdx.get(i).analysisStatus, 'NOT_ANALYZED');
    }
    assert.equal(c.censusOk, true, 'census reconciles with duplicate names because identity is entryIndex');
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('DA1-C4: mutant flipping a not-analyzed entry to SCANNED (keeping the sum) is REFUSED by the SAME census gate', () => {
  const root = tmp(); try {
    mkIds(root);
    fs.writeFileSync(path.join(root, 'four.bnt'), FX.realBnt2([0, 1, 2, 3].map(i => ({ name: `e${i}.rec`, data: FX.records80() }))));
    const r = cli(root, ['four.bnt'], ['--budget-layout-evals', '100']);
    const real = r.summary.exclusionCensus[0];
    // sanity: the genuine census passes the same gate that produced it
    assert.equal(censusGate(real).ok, true);
    // MUTANT: flip entry 2 (never analyzed) to SCANNED and keep the disposition sum at 4
    const mutant = JSON.parse(JSON.stringify(real));
    mutant.dispositionCounts = { SCANNED: 2, OVER_BUDGET: 2 }; // sum kept by hand, as a lying report would
    mutant.dispositions[2].disposition = 'SCANNED';
    const gate = censusGate(mutant);
    assert.equal(gate.ok, false, 'the SAME census gate must refuse a false SCANNED');
    assert.ok(gate.reasons.some(x => /claims SCANNED but analysisStarted/.test(x)), 'refusal reason is the semantic contradiction, not the sum');
    assert.ok(gate.reasons.some(x => /claims SCANNED but analysisStatus/.test(x)));
    // the sum-only check the old tool performed would have passed: 4 === declared 4
    assert.equal(mutant.dispositions.length, mutant.declaredEntryCount, 'sum still reconciles — semantic gate, not sum gate');
    // second mutant: scannedPayloadCount also forged to agree — still refused by the state vectors
    const mutant2 = JSON.parse(JSON.stringify(real));
    mutant2.dispositions[3].disposition = 'SCANNED';
    mutant2.dispositions[3].analysisStarted = true; // forged state too
    mutant2.scannedPayloadCount = 2;
    const g2 = censusGate(mutant2);
    assert.equal(g2.ok, false, 'SCANNED with analysisStatus=NOT_ANALYZED is still refused');
    assert.ok(g2.reasons.some(x => /analysisStatus/.test(x)));
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('DA1-C5: positive control — no exhaustion, with filters and an entry error; dispositions disjoint and counters/skips/coverage consistent', () => {
  const root = tmp(); try {
    mkIds(root);
    const good = FX.records80();
    fs.writeFileSync(path.join(root, 'mixed.bnt'), FX.realBnt2([
      { name: 'scan.rec', data: good },
      { name: 'tex.nif', data: good },       // FILTERED_EXTENSION
      { name: 'tiny.rec', data: Buffer.alloc(8, 0xff) }, // TOO_SMALL
      { name: 'big.rec', data: good },       // scanned (no exhaustion: default budgets)
    ]));
    const r = cli(root, ['mixed.bnt'], ['--entry-regex', '(scan|tex|tiny|big)\\.(rec|nif)']);
    assert.equal(r.exitCode, 0, r.stderr);
    const c = r.summary.exclusionCensus[0];
    assert.equal(c.censusOk, true);
    assert.equal(c.declaredEntryCount, 4);
    assert.equal(c.dispositionTotal, 4);
    assert.deepEqual(c.dispositionCounts, { SCANNED: 2, FILTERED_EXTENSION: 1, TOO_SMALL: 1 });
    assert.equal(c.scannedPayloadCount, 2);
    assert.equal(c.admittedCount, 2); assert.equal(c.payloadReadCount, 2);
    assert.equal(c.analysisStatusCounts.COMPLETED, 2); assert.equal(c.analysisStatusCounts.NOT_ANALYZED, 2);
    // disjointness: each declared entry appears exactly once with one disposition
    const idx = c.dispositions.map(d => d.entryIndex);
    assert.equal(new Set(idx).size, 4);
    for (const d of c.dispositions) {
      const states = [d.admitted, d.payloadRead, d.analysisStarted];
      assert.ok(d.disposition === 'SCANNED' ? states.every(Boolean) : d.analysisStarted === false, 'state vector consistent for ' + d.name);
    }
    assert.equal(r.summary.budgets.coverage, 'FULL');
    // filters exercised: regex case with everything filtered out
    const r2 = cli(root, ['mixed.bnt'], ['--entry-regex', '^nothing\\.rec$']);
    const c2 = r2.summary.exclusionCensus[0];
    assert.deepEqual(c2.dispositionCounts, { FILTERED_REGEX: 4 });
    assert.equal(c2.scannedPayloadCount, 0);
    assert.equal(c2.censusOk, true);
    // entry error (reader failure) is PARSE_FAILED with a refunded reservation, analysis NOT started
    const truncShim = FX.shimBntSrc.replace('readEntry(e){return {payload:this.b.subarray(e.offset,e.offset+e.size)}}', 'readEntry(e){return {payload:this.b.subarray(e.offset,Math.max(0,e.offset+e.size-4))}}');
    const badRepo = path.join(root, 'badrepo'); fs.mkdirSync(path.join(badRepo, 'src/pesource'), { recursive: true });
    fs.writeFileSync(path.join(badRepo, 'package.json'), '{"type":"module"}');
    fs.writeFileSync(path.join(badRepo, 'src/pesource/Bnt2Archive.js'), truncShim);
    fs.writeFileSync(path.join(badRepo, 'src/pesource/ArkArchive.js'), FX.shimArkSrc);
    fs.writeFileSync(path.join(root, 'one.bnt'), FX.realBnt2([{ name: 'x.rec', data: FX.recordsTwoIdSmall() }]));
    const out3 = path.join(root, 'out3');
    const res3 = spawnSync(process.execPath, [TOOL, '--repo', badRepo, '--ids', path.join(root, 'ids.json'), '--out', out3, '--input', path.join(root, 'one.bnt')], { encoding: 'utf8', timeout: 120000 });
    const s3 = JSON.parse(fs.readFileSync(path.join(out3, 'SUMMARY.json'), 'utf8'));
    const c3 = s3.exclusionCensus[0];
    assert.equal(c3.dispositionCounts.PARSE_FAILED, 1);
    const pf = c3.dispositions[0];
    assert.equal(pf.analysisStarted, false); assert.equal(pf.analysisStatus, 'NOT_ANALYZED');
    assert.equal(pf.admitted, true); assert.equal(pf.payloadRead, true);
    assert.equal(s3.budgets.used.scannedBytes, 0, 'reservation refunded');
    assert.equal(c3.censusOk, true);
    assert.equal(res3.status, 0, 'PAYLOAD_SIZE_MISMATCH keeps the published BASE exit semantics (the PARSE_FAILED disposition and the refund are the visible accounting)');
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('DA1-C-extra: exported analyzeBlob budget exhaustion mid-container does not leave false SCANNED (regression at the API level)', () => {
  // single container, four payloads, shared layout budget — the tail is accounted
  const b = FX.records80();
  const budget = new Budget({ layoutEvaluations: 100 });
  const results = [];
  for (let i = 0; i < 4; i++) results.push(analyzeBlob(b, sets, { budget, maxStride: 512, top: 10 }));
  assert.ok(results[0].stats.budgetExhausted, 'first analysis hit the limit');
  assert.equal(results[0].budget.used.layoutAttempts, 101);
  assert.equal(results[0].budget.used.layoutRefusals, 1);
  // each further call REFUSES at its first layout request: the request is counted
  // honestly as a refused request (layoutRefusals), never as a performed evaluation
  for (let i = 1; i < 4; i++) {
    assert.ok(results[i].stats.budgetExhausted, 'call ' + i + ' refuses at once');
    assert.equal(results[i].stats.layoutsAdmitted, 0, 'no layout was evaluated by call ' + i);
    assert.equal(results[i].stats.layoutAttempts, 101 + i, 'exactly one refused request per further call');
    assert.equal(results[i].stats.layoutRefusals, 1 + i);
    assert.equal(results[i].stats.coverage, 'PARTIAL');
  }
  assert.equal(budget.layoutRefusals, 4, 'four refused requests total; zero of them are performed evaluations');
});
