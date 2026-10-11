// da3_budget.test.mjs — DA-3 P2: the effective Budget used by the exported
// analyzeBlob is validated (contract PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011,
// section E). The construction+call is covered as ONE operation: a constructor
// refusal means the analysis never starts. No test performs 100001 analyses —
// these are CONFIGURATION refusals, not scan executions.
import test from 'node:test';
import assert from 'node:assert/strict';
import os from 'node:os';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { analyzeBlob, Budget, BUDGET_CEILINGS, budgetLimitErrors } from '../placement_probe.mjs';
import * as FX from './fixtures.mjs';

const TOOL = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'placement_probe.mjs');
const WORKTREE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..', '..');
const sets = { S_tpl: new Set([4057, 4058]), S_model: new Set([218757]) };
const refusalsOf = (label, fn) => {
  let threw = false, message = null, result = null;
  try { result = fn(); } catch (e) { threw = true; message = String(e?.message || e); }
  assert.equal(threw, true, label + ' must be REFUSED with INVALID_CONFIGURATION (got result: ' + JSON.stringify(result).slice(0, 120) + ')');
  assert.match(message, /INVALID_CONFIGURATION/, label + ' refusal must be the controlled INVALID_CONFIGURATION status');
  return { label, message };
};

test('DA3: Budget constructor validates all five limits (finite safe integers in [1, ceiling])', () => {
  // layoutEvaluations: 100001 / NaN / Infinity / -1 / 1.5
  refusalsOf('Budget{layoutEvaluations:100001}', () => new Budget({ layoutEvaluations: 100001 }));
  refusalsOf('Budget{layoutEvaluations:NaN}', () => new Budget({ layoutEvaluations: NaN }));
  refusalsOf('Budget{layoutEvaluations:Infinity}', () => new Budget({ layoutEvaluations: Infinity }));
  refusalsOf('Budget{layoutEvaluations:-1}', () => new Budget({ layoutEvaluations: -1 }));
  refusalsOf('Budget{layoutEvaluations:1.5}', () => new Budget({ layoutEvaluations: 1.5 }));
  refusalsOf('Budget{retainedCandidates:512}', () => new Budget({ retainedCandidates: 512 }));
  // the other three limits: ceiling+1 and NaN
  refusalsOf('Budget{syntheticInputs:33}', () => new Budget({ syntheticInputs: 33 }));
  refusalsOf('Budget{syntheticInputs:NaN}', () => new Budget({ syntheticInputs: NaN }));
  refusalsOf('Budget{scannedBytes:67108865}', () => new Budget({ scannedBytes: 67108865 }));
  refusalsOf('Budget{scannedBytes:NaN}', () => new Budget({ scannedBytes: NaN }));
  refusalsOf('Budget{fullCensusRows:50001}', () => new Budget({ fullCensusRows: 50001 }));
  refusalsOf('Budget{fullCensusRows:NaN}', () => new Budget({ fullCensusRows: NaN }));
  refusalsOf('Budget{retainedCandidates:NaN}', () => new Budget({ retainedCandidates: NaN }));
});

test('DA3: exported analyzeBlob refuses an injected invalid Budget — construction+call as ONE operation, INVALID_CONFIGURATION before any analysis', () => {
  // the fixture is 10007B of 0xFF; an ACCEPTED call would burn 126 layout attempts —
  // the refusals below must happen BEFORE any of that work
  const buf = FX.layoutBuffer10007();
  for (const bad of [{ layoutEvaluations: 100001 }, { layoutEvaluations: NaN }, { retainedCandidates: 512 }, { syntheticInputs: 33 }, { scannedBytes: 67108865 }, { fullCensusRows: 50001 }]) {
    const r = refusalsOf('analyzeBlob with Budget' + JSON.stringify(bad), () => analyzeBlob(buf, sets, { maxHeader: 0, budget: new Budget(bad) }));
    assert.ok(r.message.includes('budget.'), 'the refusal names the offending limit: ' + r.message);
  }
  // the ordinary option path stays refused as well (control from the previous correction)
  refusalsOf('budgetThresholds{layoutEvaluations:100001}', () => analyzeBlob(buf, sets, { maxHeader: 0, budgetThresholds: { layoutEvaluations: 100001 } }));
  // a NaN limit is NEVER serialized as a valid null limit: the call throws instead of producing a result
  let leaked = null;
  try { leaked = analyzeBlob(buf, sets, { maxHeader: 0, budget: new Budget({ layoutEvaluations: NaN }) }); } catch {}
  assert.equal(leaked, null, 'no fake NO_CANDIDATE result object escapes an invalid configuration');
});

test('DA3: a valid Budget with contradictory budgetThresholds is refused fail-closed', () => {
  const b = new Budget({ layoutEvaluations: 500 });
  const r = refusalsOf('valid Budget(500) + budgetThresholds{layoutEvaluations:100}', () => analyzeBlob(FX.records80(), sets, { maxHeader: 16, maxStride: 32, budget: b, budgetThresholds: { layoutEvaluations: 100 } }));
  assert.match(r.message, /contradictory/, 'the contradiction is named, not silently resolved');
  // identical limits are NOT contradictory (pass-through positive)
  const ok = analyzeBlob(FX.records80(), sets, { maxHeader: 16, maxStride: 32, budget: new Budget({ layoutEvaluations: 500 }), budgetThresholds: { layoutEvaluations: 500 } });
  assert.ok(ok.candidates.length > 0, 'a supplied Budget with agreeing budgetThresholds works');
  // an INVALID budgetThresholds next to a valid Budget is also refused (nothing invalid enters)
  refusalsOf('valid Budget + invalid budgetThresholds', () => analyzeBlob(FX.records80(), sets, { maxHeader: 16, maxStride: 32, budget: new Budget(), budgetThresholds: { layoutEvaluations: 100001 } }));
});

test('DA3: a masquerading non-Budget object cannot supply effective limits; a MUTATED instance is caught at use time', () => {
  const fake = { limits: { ...BUDGET_CEILINGS, layoutEvaluations: 999999, retainedCandidates: 999999 }, layoutAttempts: 0 };
  // not instanceof Budget -> the fake is IGNORED entirely; the canonical ceilings apply
  const r = analyzeBlob(FX.records80(), sets, { maxHeader: 16, maxStride: 32, budget: fake });
  assert.equal(r.budget.limits.layoutEvaluations, BUDGET_CEILINGS.layoutEvaluations, 'the masquerade supplied nothing');
  assert.equal(r.budget.limits.retainedCandidates, BUDGET_CEILINGS.retainedCandidates);
  assert.ok(r.candidates.length > 0, 'the ordinary analysis still works with the fake ignored');
  // a real instance whose limits property was REPLACED after construction is refused at use time
  const m = new Budget(); m.limits = { ...BUDGET_CEILINGS, layoutEvaluations: 999999 };
  refusalsOf('mutated instance limits at use time', () => analyzeBlob(FX.records80(), sets, { maxHeader: 16, maxStride: 32, budget: m }));
  assert.equal(m.layoutAttempts, 0, 'the refusal happened BEFORE any analysis start');
  // budgetLimitErrors is exported for independent recomputation
  assert.ok(budgetLimitErrors({ ...BUDGET_CEILINGS }).length === 0);
  assert.ok(budgetLimitErrors({ ...BUDGET_CEILINGS, layoutEvaluations: NaN }).length === 1);
});

test('DA3: positive controls — defaults, legal minimum, exact ceiling, lowered limit, shared Budget across >=2 inputs without reset', () => {
  // no own options at all
  const d = new Budget();
  assert.deepEqual({ ...d.limits }, { ...BUDGET_CEILINGS });
  // legal minimum 1
  const min = new Budget({ layoutEvaluations: 1 });
  assert.equal(min.limits.layoutEvaluations, 1);
  // exact ceilings are legal
  const ceil = new Budget({ syntheticInputs: 32, scannedBytes: 67108864, layoutEvaluations: 100000, fullCensusRows: 50000, retainedCandidates: 256 });
  assert.deepEqual({ ...ceil.limits }, { ...BUDGET_CEILINGS });
  // lowered limit works and exhausts honestly
  const r = analyzeBlob(FX.layoutBuffer10007(), sets, { maxHeader: 0, maxStride: 512, budgetThresholds: { layoutEvaluations: 60 } });
  assert.equal(r.stats.layoutAttempts, 61); // REQUESTS: 60 evaluated + 1 refused
  assert.equal(r.stats.layoutRefusals, 1);
  assert.equal(r.stats.layoutsAdmitted, 0);
  assert.equal(r.stats.layoutRequests, 61);
  assert.equal(r.budget.used.layoutRefusals, 1);
  assert.ok(r.budget.refusals[r.budget.refusals.length - 1].detail.includes('executed evaluations: 60'), 'the refusal names the executed count — 61 is never claimed as 61 performed evaluations');
  // shared Budget across >=2 inputs WITHOUT reset: counters aggregate on the same instance
  const shared = new Budget();
  const r1 = analyzeBlob(FX.records80(), sets, { maxHeader: 0, maxStride: 512, budget: shared, top: 10 });
  const r2 = analyzeBlob(FX.records80(), sets, { maxHeader: 0, maxStride: 512, budget: shared, top: 10 });
  assert.equal(shared.layoutAttempts, 252, 'the SAME tracker instance accumulated both inputs');
  assert.equal(r1.stats.layoutAttempts, 126, 'first input: its own 126 requests');
  assert.equal(r2.stats.layoutAttempts, 252, 'second input: the shared counters continue — no reset between payloads/inputs');
  assert.equal(r2.stats.layoutAttempts, 2 * r1.stats.layoutAttempts, 'aggregation across two inputs on one instance');
  assert.equal(shared.layoutRefusals, 0);
});

test('DA3: CLI refuses raised/NaN budget flags fail-closed (exit!=0, SCAN_STARTED=NO)', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'pe-t-da3-'));
  try {
    fs.writeFileSync(path.join(root, 'ids.json'), JSON.stringify({ S_tpl: [4057, 4058] }));
    fs.writeFileSync(path.join(root, 'a.vfs'), FX.records80());
    for (const args of [['--budget-layout-evals', '100001'], ['--budget-layout-evals', 'nan'], ['--budget-retained-candidates', '512'], ['--budget-max-inputs', '33'], ['--budget-census-rows', '50001'], ['--budget-scanned-bytes', '67108865']]) {
      const out = path.join(root, 'out');
      const res = spawnSync(process.execPath, [TOOL, '--repo', WORKTREE, '--ids', path.join(root, 'ids.json'), '--out', out, '--input', path.join(root, 'a.vfs'), ...args], { encoding: 'utf8', timeout: 60000 });
      assert.notEqual(res.status, 0, 'CLI must fail for ' + args.join(' '));
      assert.match(res.stderr, /INVALID_CONFIGURATION/);
      assert.match(res.stderr, /SCAN_STARTED=NO/);
      assert.equal(fs.existsSync(out), false, 'no output dir for ' + args.join(' '));
    }
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});
