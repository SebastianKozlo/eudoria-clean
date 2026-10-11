// da2_retained.test.mjs — DA-2 (R2-2 P2) global limit of DISTINCT live candidate records
// (contract PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011, section D).
// The observer counts OBJECT IDENTITIES in the actual holding collections at
// creation (found), forward (data.candidates + allRows) and serialization (live rows
// + serialized identities) using Set identity — the production peakRetained tracker is
// recorded for comparison but is NEVER the oracle. No GC-based proof is used: the
// counted sets are exactly the collections that hold the records.
// The instrumented copy changes no predicate/limit/expectation; its outputs are
// byte-compared against the unmodified CLI at the same configuration.
import test from 'node:test';
import assert from 'node:assert/strict';
import os from 'node:os';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import * as FX from './fixtures.mjs';

const TESTS = path.dirname(fileURLToPath(import.meta.url));
const TOOL = path.join(TESTS, '..', 'placement_probe.mjs');
const WORKTREE = path.resolve(TESTS, '..', '..', '..');
const sha = b => createHash('sha256').update(b).digest('hex');
const tmp = () => fs.mkdtempSync(path.join(os.tmpdir(), 'pe-t-da2-'));

// ---- observer: read-only hooks injected at unique markers of the CORRECTED source ----
const MARK_CREATION = '  budget.trackTotalHeld(found.length);';
const MARK_FORWARD = '        allRows.push(c);';
const MARK_SERIALIZATION = '  writeCsvRows(path.join(root, \'placement_candidates.csv\'), rows, cols, csvRowCells);';
const INJ_CREATION = `\n  { const obs = { stage: 'creation', distinctFound: new Set(found).size, externalRows: (globalThis.__auditRows ?? new Set()).size, combinedLiveDistinct: new Set([...found, ...(globalThis.__auditRows ?? [])]).size, trackedPeak: budget.peakRetained, limit: budget.limits.retainedCandidates }; (globalThis.__auditPhases ??= []).push(obs); }`;
const INJ_FORWARD = `\n        { (globalThis.__auditRows ??= new Set()).add(c); const obs = { stage: 'forward', rankObjects: new Set(data.candidates).size, allRowsObjects: new Set(allRows).size, combinedLiveDistinct: new Set([...data.candidates, ...allRows]).size, trackedPeak: budget.peakRetained, limit: budget.limits.retainedCandidates }; (globalThis.__auditPhases ??= []).push(obs); }`;
const INJ_SERIALIZATION = `  { const __cells = r => { (globalThis.__auditSer ??= new Set()).add(r); return csvRowCells(r); }; writeCsvRows(path.join(root, 'placement_candidates.csv'), rows, cols, __cells); const obs = { stage: 'serialization', liveRows: new Set(rows).size, serializedIdentities: (globalThis.__auditSer ?? new Set()).size, combinedLiveDistinct: new Set([...rows, ...(globalThis.__auditSer ?? [])]).size, allSerializedAreLiveRows: [...(globalThis.__auditSer ?? [])].every(o => new Set(rows).has(o)), trackedPeak: budget.peakRetained, limit: budget.limits.retainedCandidates }; (globalThis.__auditPhases ??= []).push(obs); fs.writeFileSync(path.join(root, 'AUDIT_OBJECT_COPIES.json'), JSON.stringify({ phases: globalThis.__auditPhases ?? [] }, null, 2) + '\\n'); }`;

function buildObservedTool(mutate = false) {
  const original = fs.readFileSync(TOOL, 'utf8');
  let src = original;
  if (mutate) {
    const mutantMarker = '        allRows.push({ ...c });'; // DA-2 regression: a forced extra copy at forward
    if (src.split(MARK_FORWARD).length !== 2) throw Error('forward marker not unique');
    src = src.replace(MARK_FORWARD, mutantMarker);
    const injF = `\n        { (globalThis.__auditRows ??= new Set()).add(c); const obs = { stage: 'forward', rankObjects: new Set(data.candidates).size, allRowsObjects: new Set(allRows).size, combinedLiveDistinct: new Set([...data.candidates, ...allRows]).size, trackedPeak: budget.peakRetained, limit: budget.limits.retainedCandidates }; (globalThis.__auditPhases ??= []).push(obs); }`;
    if (src.split(mutantMarker).length !== 2) throw Error('mutant marker not unique');
    src = src.replace(mutantMarker, mutantMarker + injF);
  } else {
    if (src.split(MARK_FORWARD).length !== 2) throw Error('forward marker not unique');
    src = src.replace(MARK_FORWARD, MARK_FORWARD + INJ_FORWARD);
  }
  if (src.split(MARK_CREATION).length !== 2) throw Error('creation marker not unique');
  src = src.replace(MARK_CREATION, MARK_CREATION + INJ_CREATION);
  if (src.split(MARK_SERIALIZATION).length !== 2) throw Error('serialization marker not unique');
  src = src.replace(MARK_SERIALIZATION, INJ_SERIALIZATION);
  return { originalSha256: sha(Buffer.from(original)), observedSha256: sha(Buffer.from(src)), source: src };
}

function cliRun(tool, root, ids, inputs, args, tag) {
  const out = path.join(root, tag); fs.mkdirSync(out, { recursive: true });
  const res = spawnSync(process.execPath, [tool, '--repo', WORKTREE, '--ids', ids, '--out', out, ...inputs.flatMap(n => ['--input', n]), ...args], { encoding: 'utf8', timeout: 180000 });
  let summary = null; try { summary = JSON.parse(fs.readFileSync(path.join(out, 'SUMMARY.json'), 'utf8')); } catch {}
  let phases = null; try { phases = JSON.parse(fs.readFileSync(path.join(out, 'AUDIT_OBJECT_COPIES.json'), 'utf8')).phases; } catch {}
  return { exitCode: res.status, stderr: res.stderr, summary, phases, out };
}
function fourOutputs(out) {
  return Object.fromEntries(['placement_candidates.csv', 'candidates_top.json', 'sources.json', 'scan_skips.csv'].map(f => [f, fs.readFileSync(path.join(out, f))]));
}

test('DA2: aliasing counts the same instance once (identity oracle, not the production tracker)', () => {
  const a = { id: 1 }, b = { id: 2 };
  const rows = [a, b], sameRefAgain = [a, b]; // the same objects in two arrays
  assert.equal(new Set([...rows, ...sameRefAgain]).size, 2, 'same object in two arrays counts ONCE');
  assert.equal(new Set([...rows, { ...a }, { ...b }]).size, 4, 'new objects with the same fields count SEPARATELY');
});

test('DA2: cap4 (2 inputs) — independently measured peak <= cap in EVERY phase; aliasing, not copying', () => {
  const root = tmp(); try {
    const ids = path.join(root, 'ids.json');
    fs.writeFileSync(ids, JSON.stringify({ S_tpl: [4057, 4058], S_model: [218757] }));
    for (let i = 0; i < 2; i++) fs.writeFileSync(path.join(root, `raw_${i}.vfs`), FX.records80());
    const obs = buildObservedTool(false);
    const obsTool = path.join(root, 'observed_placement_probe.mjs');
    fs.writeFileSync(obsTool, obs.source);
    const un = cliRun(TOOL, root, ids, [path.join(root, 'raw_0.vfs'), path.join(root, 'raw_1.vfs')], ['--budget-retained-candidates', '4'], 'un');
    const ob = cliRun(obsTool, root, ids, [path.join(root, 'raw_0.vfs'), path.join(root, 'raw_1.vfs')], ['--budget-retained-candidates', '4'], 'ob');
    // instrumented vs ordinary at the SAME configuration: byte-identical outputs + identical budgets
    const unB = fourOutputs(path.join(root, 'un')), obB = fourOutputs(path.join(root, 'ob'));
    for (const f of Object.keys(unB)) assert.ok(unB[f].equals(obB[f]), 'byte-identical output: ' + f);
    assert.deepEqual(un.summary.budgets, ob.summary.budgets);
    assert.equal(un.exitCode, 0, un.stderr);
    // honest exhaustion is kept: PARTIAL coverage with candidates retained
    assert.equal(un.summary.budgets.coverage, 'PARTIAL');
    assert.ok(un.summary.budgets.exhausted.includes('RETAINED_CANDIDATES'));
    assert.ok(un.summary.candidateCount > 0);
    // EVERY phase: independently measured distinct live records <= cap
    const phases = ob.phases;
    assert.ok(phases.length > 0, 'observations recorded');
    const cap = 4;
    for (const p of phases) {
      assert.ok(p.combinedLiveDistinct <= cap, p.stage + ' distinct ' + p.combinedLiveDistinct + ' exceeds cap ' + cap);
    }
    const fwds = phases.filter(p => p.stage === 'forward');
    const sers = phases.filter(p => p.stage === 'serialization');
    assert.ok(fwds.length > 0 && sers.length === 1, 'forward and serialization phases observed');
    assert.ok(fwds.every(p => p.combinedLiveDistinct === p.rankObjects + 0 || p.combinedLiveDistinct <= cap));
    // serialization: the serialized identities ARE the live rows (no second array of copies)
    assert.equal(sers[0].allSerializedAreLiveRows, true);
    assert.equal(sers[0].serializedIdentities, sers[0].liveRows);
    assert.equal(sers[0].combinedLiveDistinct, sers[0].liveRows);
    assert.ok(sers[0].liveRows <= cap);
    // PRE reference (Desktop post-audit on BASE): tracker 4 while distinct records were 8 — the corrected peak is 4
    assert.equal(ob.summary.budgets.used.peakRetainedCandidates, 4);
    const maxFwd = Math.max(...fwds.map(p => p.combinedLiveDistinct));
    assert.ok(maxFwd <= 4, 'forward distinct peak ' + maxFwd + ' (PRE on BASE: 8)');
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('DA2: canonical cap256 (9 inputs) — every phase <= 256; PRE forward was 280 and CSV serialization 512', () => {
  const root = tmp(); try {
    const ids = path.join(root, 'ids.json');
    fs.writeFileSync(ids, JSON.stringify({ S_tpl: [4057, 4058], S_model: [218757] }));
    const raws = []; for (let i = 0; i < 9; i++) { const f = path.join(root, `raw_${i}.vfs`); fs.writeFileSync(f, FX.records80()); raws.push(f); }
    const obs = buildObservedTool(false);
    const obsTool = path.join(root, 'observed_placement_probe.mjs');
    fs.writeFileSync(obsTool, obs.source);
    const un = cliRun(TOOL, root, ids, raws, [], 'un');
    const ob = cliRun(obsTool, root, ids, raws, [], 'ob');
    const unB = fourOutputs(path.join(root, 'un')), obB = fourOutputs(path.join(root, 'ob'));
    for (const f of Object.keys(unB)) assert.ok(unB[f].equals(obB[f]), 'byte-identical output: ' + f);
    assert.deepEqual(un.summary.budgets, ob.summary.budgets);
    assert.equal(un.exitCode, 0, un.stderr);
    const phases = ob.phases; const cap = 256;
    for (const p of phases) assert.ok(p.combinedLiveDistinct <= cap, p.stage + ' distinct ' + p.combinedLiveDistinct + ' exceeds ' + cap);
    const sers = phases.filter(p => p.stage === 'serialization');
    assert.equal(sers.length, 1);
    assert.equal(sers[0].allSerializedAreLiveRows, true, 'the CSV is serialized over the live rows — no second array of copies (PRE: 512 distinct at serialization)');
    assert.ok(Math.max(...phases.filter(p => p.stage === 'forward').map(p => p.combinedLiveDistinct)) <= cap, 'PRE forward peak on BASE was 280');
    assert.ok(ob.summary.candidateCount > 0);
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('DA2: a deliberately forced extra copy IS detected by the identity observer (mutant control)', () => {
  const root = tmp(); try {
    const ids = path.join(root, 'ids.json');
    fs.writeFileSync(ids, JSON.stringify({ S_tpl: [4057, 4058], S_model: [218757] }));
    for (let i = 0; i < 2; i++) fs.writeFileSync(path.join(root, `raw_${i}.vfs`), FX.records80());
    const obs = buildObservedTool(true); // mutant: allRows.push({ ...c }) — forced extra copy
    const obsTool = path.join(root, 'mutant_observed.mjs');
    fs.writeFileSync(obsTool, obs.source);
    const mu = cliRun(obsTool, root, ids, [path.join(root, 'raw_0.vfs'), path.join(root, 'raw_1.vfs')], ['--budget-retained-candidates', '4'], 'mu');
    assert.equal(mu.exitCode, 0, mu.stderr);
    const fwds = mu.phases.filter(p => p.stage === 'forward');
    assert.ok(fwds.length > 0);
    const maxFwd = Math.max(...fwds.map(p => p.combinedLiveDistinct));
    assert.ok(maxFwd > 4, 'the observer DETECTS the forced extra copy: forward distinct ' + maxFwd + ' > cap 4 (identity measurement, not the production tracker)');
    // the mutant's outputs are byte-identical to a correct run — output equality alone is NOT the cap proof
    assert.equal(fwds.some(p => p.trackedPeak <= 4), true, 'the production tracker alone would still look satisfied — it is not the oracle');
    const sers = mu.phases.filter(p => p.stage === 'serialization');
    if (sers.length) assert.equal(sers[0].allSerializedAreLiveRows, true, 'the CSV still walks the (copied) live rows; the defect is the extra forward copy population');
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('DA2: a normal small valid fixture still emits candidates', () => {
  const root = tmp(); try {
    const ids = path.join(root, 'ids.json');
    fs.writeFileSync(ids, JSON.stringify({ S_tpl: [4057, 4058], S_model: [218757] }));
    fs.writeFileSync(path.join(root, 'small.vfs'), FX.recordsTwoIdSmall());
    const r = cliRun(TOOL, root, ids, [path.join(root, 'small.vfs')], [], 'out');
    assert.equal(r.exitCode, 0, r.stderr);
    assert.ok(r.summary.candidateCount > 0, 'the copy-free forwarding does not remove candidates from a small valid fixture');
    assert.equal(r.summary.budgets.coverage, 'FULL');
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});
