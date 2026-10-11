// pa2_receipt_qualification.test.mjs — PA2-RC1/P2 permanent regression for the
// corrected receipt qualification validator (RUN_ID
// PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011, contract §4/§5).
//
// The predecessor full POST accepted the PA2 live receipt on verdict+matched+mode
// only — an externally measured false-PASS (Desktop M1/M2 receipts with zeroed
// MEASURED.sha256 / gateModule.sha256 passed QUALIFICATION_PASS/exit0). The
// corrected validator (tools/placement_probe/qualification/pa2_r1/validate_receipt.mjs)
// re-derives every receipt claim from trusted sources and refuses contradictions.
// These unit-level regressions exercise the SAME validator the canonical POST uses;
// the §5 full-POST matrix (CLEAN + M1..M9) is run by the bounded outer driver
// run_matrix.mjs and recorded in the run package.
//
// NOTE on the historical spy wording (PA2-RC2, contract §6): the runner's spy
// counters are an AUTHENTIC observation that THIS runner's downstream callbacks are
// never invoked (clean or refusal path) and that a refusal exits 3 — they do NOT
// establish automatic downstream enforcement for any other or future runner
// (HISTORICAL_SPY_PROVEN_ZERO_DOWNSTREAM = RETRACTED;
// PA2_DOWNSTREAM_AUTOMATIC_ENFORCEMENT = NOT_ESTABLISHED — see the run package
// SUPERSESSION.md). The unchanged historical runner string DOWNSTREAM_AUTHORIZED is
// a legacy label, not this run's authorization or renewed proof.
import test from 'node:test';
import assert from 'node:assert/strict';
import os from 'node:os';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { loadTrusted, qualifyReceipt, computeQualification, EXPECTED_OUTCOMES, RECEIPT_PROFILE, TRUSTED_GATE_MODULE, TRUSTED_RUNNER } from '../qualification/pa2_r1/validate_receipt.mjs';

const TESTS = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(TESTS, '..', '..', '..'); // worktree root (or isolated stage root)
const RUNNER = path.resolve(ROOT, 'docs', 'audits', 'PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011', 'PRE', 'verify_inputs_runner.mjs');
const sha = b => createHash('sha256').update(b).digest('hex');
const tmp = () => fs.mkdtempSync(path.join(os.tmpdir(), 'pe-t-pa2rq-'));
const trusted = await loadTrusted(ROOT);

function generateCleanReceipt(dir, name = 'receipt_clean.json') {
  // REAL_SEQUENCE invocation of the unchanged staged runner — the same live gate
  // sequence the archived CLEAN receipt came from (a context-specific requalification
  // of archived evidence, NOT proof of historical execution or authorship).
  const receipt = path.join(dir, name);
  const res = spawnSync(process.execPath, [RUNNER, '--receipt', receipt], { encoding: 'utf8', timeout: 120000 });
  assert.equal(res.status, 0, 'clean gate invocation must authorize: ' + res.stderr);
  return { receipt, obj: JSON.parse(fs.readFileSync(receipt, 'utf8')) };
}
const writeReceipt = (dir, obj, name) => { const p = path.join(dir, name); fs.writeFileSync(p, JSON.stringify(obj, null, 2) + '\n'); return p; };

test('PA2-RQ: the trusted sources verify BEFORE pin use (frozen constants; 16 distinct pins)', () => {
  assert.equal(trusted.ok, true, 'trusted source verification failed: ' + JSON.stringify(trusted.reasons));
  assert.equal(trusted.pins.length, 16);
  assert.equal(new Set(trusted.pins.map(p => p.pin)).size, 16);
  assert.equal(trusted.moduleShas.gateModule.toUpperCase(), TRUSTED_GATE_MODULE.sha256.toUpperCase());
  assert.equal(trusted.moduleShas.runner.toUpperCase(), TRUSTED_RUNNER.sha256.toUpperCase());
  assert.equal(trusted.schema, 'PE_FROZEN_INPUT_PINS_V1');
});

test('PA2-RQ: a freshly generated clean REAL_SEQUENCE receipt qualifies — all four quantities', async () => {
  const root = tmp(); try {
    const { receipt, obj } = generateCleanReceipt(root);
    const before = sha(fs.readFileSync(receipt));
    const q = await qualifyReceipt({ receiptPath: receipt, trusted });
    assert.equal(q.RECEIPT_QUALIFICATION.verdict, 'PASS', 'refusal reasons: ' + JSON.stringify(q.RECEIPT_QUALIFICATION.reasons));
    assert.equal(q.INPUT_BYTES_REMEASURED.pass, true);
    assert.equal(q.INPUT_BYTES_REMEASURED.verdict, 'PASS');
    assert.equal(q.INPUT_BYTES_REMEASURED.matched, 16);
    assert.equal(q.RECEIPT_INTERNAL_CONSISTENCY.ok, true);
    assert.equal(q.RECEIPT_INTERNAL_CONSISTENCY.recomputed.matched, 16);
    assert.equal(q.RECEIPT_INTERNAL_CONSISTENCY.recomputed.verdict, 'PASS');
    assert.equal(q.MODULE_CODE_IDENTITY.ok, true);
    assert.equal(obj.runId, RECEIPT_PROFILE.runId);
    assert.equal(obj.mode, 'REAL_SEQUENCE');
    // the live remeasurement must not overwrite, replace or repair the receipt-under-test
    assert.equal(sha(fs.readFileSync(receipt)), before, 'the receipt-under-test was modified');
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('PA2-RQ: M1 mutant (perPin[0].MEASURED.sha256 zeroed) is refused by re-derivation, not by a whole-file hash rule', async () => {
  const root = tmp(); try {
    const { obj } = generateCleanReceipt(root);
    obj.perPin[0].MEASURED.sha256 = '0'.repeat(64); // EXPECTED + compareResult left untouched
    const p = writeReceipt(root, obj, 'm1.json');
    const q = await qualifyReceipt({ receiptPath: p, trusted });
    assert.equal(q.RECEIPT_QUALIFICATION.verdict, 'FAIL');
    assert.equal(q.RECEIPT_INTERNAL_CONSISTENCY.recomputed.matched, 15);
    assert.equal(q.RECEIPT_INTERNAL_CONSISTENCY.recomputed.blockedCount, 1);
    assert.equal(q.RECEIPT_INTERNAL_CONSISTENCY.recomputed.blockedPins[0].compareResult, 'SHA_MISMATCH');
    assert.equal(q.RECEIPT_INTERNAL_CONSISTENCY.recomputed.verdict, 'BLOCKED_INPUT_IDENTITY');
    assert.ok(q.RECEIPT_QUALIFICATION.reasons.some(r => /MEASURED\.sha256 differs/.test(r)), 'the semantic reason must be recorded');
    assert.ok(q.RECEIPT_QUALIFICATION.reasons.some(r => /contradicts the independently derived/.test(r)), 'the claimed compareResult contradiction must be recorded');
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('PA2-RQ: M2/M8 mutants (gateModule/runner SHA zeroed) are refused by MODULE_CODE_IDENTITY', async () => {
  const root = tmp(); try {
    for (const [field, setter] of [
      ['moduleIdentity.gateModule.sha256', o => { o.moduleIdentity.gateModule.sha256 = '0'.repeat(64); }],
      ['moduleIdentity.runner.sha256', o => { o.moduleIdentity.runner.sha256 = '0'.repeat(64); }],
    ]) {
      const { obj } = generateCleanReceipt(root);
      setter(obj);
      const q = await qualifyReceipt({ receiptPath: writeReceipt(root, obj, 'm.json'), trusted });
      assert.equal(q.RECEIPT_QUALIFICATION.verdict, 'FAIL', field);
      assert.equal(q.MODULE_CODE_IDENTITY.ok, false, field);
      assert.ok(q.RECEIPT_QUALIFICATION.reasons.some(r => r.includes(field)), field + ' refusal reason recorded');
    }
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('PA2-RQ: M3 size+1 and M4 forged compareResult (bytes still matching) are refused', async () => {
  const root = tmp(); try {
    const { obj: m3 } = generateCleanReceipt(root);
    m3.perPin[0].MEASURED.sizeBytes += 1;
    const q3 = await qualifyReceipt({ receiptPath: writeReceipt(root, m3, 'm3.json'), trusted });
    assert.equal(q3.RECEIPT_QUALIFICATION.verdict, 'FAIL');
    assert.equal(q3.RECEIPT_INTERNAL_CONSISTENCY.recomputed.blockedPins[0].compareResult, 'SIZE_MISMATCH');
    const { obj: m4 } = generateCleanReceipt(root);
    m4.perPin[0].compareResult = 'SHA_MISMATCH'; // while the measured bytes still match the pin
    const q4 = await qualifyReceipt({ receiptPath: writeReceipt(root, m4, 'm4.json'), trusted });
    assert.equal(q4.RECEIPT_QUALIFICATION.verdict, 'FAIL');
    assert.equal(q4.RECEIPT_INTERNAL_CONSISTENCY.perPinChecks[0].derivedCompareResult, 'MATCH');
    assert.equal(q4.RECEIPT_INTERNAL_CONSISTENCY.perPinChecks[0].compareResultValid, false, 'a forged compareResult is not trusted');
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('PA2-RQ: M5/M6 pin-set mutants (one removed / one duplicated) are refused by the exact-16 profile', async () => {
  const root = tmp(); try {
    const { obj: m5 } = generateCleanReceipt(root);
    m5.perPin.pop();
    const q5 = await qualifyReceipt({ receiptPath: writeReceipt(root, m5, 'm5.json'), trusted });
    assert.equal(q5.RECEIPT_QUALIFICATION.verdict, 'FAIL');
    assert.ok(q5.RECEIPT_QUALIFICATION.reasons.some(r => /perPin count is 15/.test(r)));
    const { obj: m6 } = generateCleanReceipt(root);
    m6.perPin.push(JSON.parse(JSON.stringify(m6.perPin[0])));
    const q6 = await qualifyReceipt({ receiptPath: writeReceipt(root, m6, 'm6.json'), trusted });
    assert.equal(q6.RECEIPT_QUALIFICATION.verdict, 'FAIL');
    assert.ok(q6.RECEIPT_QUALIFICATION.reasons.some(r => /duplicate perPin entries/.test(r)));
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('PA2-RQ: M7/M9 contradictory summaries are refused (recomputed vs claimed)', async () => {
  const root = tmp(); try {
    const { obj: m7 } = generateCleanReceipt(root);
    m7.gate.matched = 15; m7.gate.blockedCount = 1; // while all perPin entries match
    const q7 = await qualifyReceipt({ receiptPath: writeReceipt(root, m7, 'm7.json'), trusted });
    assert.equal(q7.RECEIPT_QUALIFICATION.verdict, 'FAIL');
    assert.ok(q7.RECEIPT_QUALIFICATION.reasons.some(r => /gate\.matched 15 != recomputed 16/.test(r)));
    const { obj: m9 } = generateCleanReceipt(root);
    m9.perPin[0].MEASURED.exists = false; m9.perPin[0].MEASURED.sizeBytes = null; m9.perPin[0].MEASURED.sha256 = null; m9.perPin[0].compareResult = 'MISSING';
    m9.gate.matched = 15; m9.gate.blockedCount = 1;
    m9.gate.blockedPins = [{ pin: m9.perPin[0].pin, compareResult: 'MISSING', reason: 'input file not found' }];
    // verdict/EFFECTIVE_GATE_RESULT intentionally still claim PASS — the contradiction under test
    const q9 = await qualifyReceipt({ receiptPath: writeReceipt(root, m9, 'm9.json'), trusted });
    assert.equal(q9.RECEIPT_QUALIFICATION.verdict, 'FAIL');
    assert.ok(q9.RECEIPT_QUALIFICATION.reasons.some(r => /MEASURED\.exists is not true/.test(r)));
    assert.ok(q9.RECEIPT_QUALIFICATION.reasons.some(r => /gate\.verdict PASS != recomputed BLOCKED_INPUT_IDENTITY/.test(r)), 'a contradictory summary refuses qualification');
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('PA2-RQ: profile unit controls — wrong runId/stage/mode and an unreadable/truncated JSON receipt all fail closed (controlled refusal, no exception-to-PASS)', async () => {
  const root = tmp(); try {
    for (const [field, setter] of [
      ['runId', o => { o.runId = 'PE_935_SOME_OTHER_RUN_ID'; }],
      ['stage', o => { o.stage = 'PA2_SOME_OTHER_STAGE'; }],
      ['mode', o => { o.mode = 'MUTANT_TEST (private copies; expected pins frozen and unchanged)'; }],
    ]) {
      const { obj } = generateCleanReceipt(root);
      setter(obj);
      const q = await qualifyReceipt({ receiptPath: writeReceipt(root, obj, 'p.json'), trusted });
      assert.equal(q.RECEIPT_QUALIFICATION.verdict, 'FAIL', field);
      assert.ok(q.RECEIPT_QUALIFICATION.reasons.some(r => /runId\/stage\/mode do not match the frozen historical context/.test(r)), field + ' refusal must arise from the context check: ' + JSON.stringify(q.RECEIPT_QUALIFICATION.reasons));
    }
    const truncated = path.join(root, 'truncated.json');
    fs.writeFileSync(truncated, fs.readFileSync(generateCleanReceipt(root).receipt).subarray(0, 4000)); // invalid JSON
    const q4 = await qualifyReceipt({ receiptPath: truncated, trusted });
    assert.equal(q4.RECEIPT_QUALIFICATION.verdict, 'FAIL');
    assert.ok(/not valid JSON/.test(q4.RECEIPT_QUALIFICATION.refusalReason ?? ''), 'controlled parse refusal');
    // CLEAN stays unchanged after the unit controls
    const clean = generateCleanReceipt(root, 'clean_control.json');
    const qc = await qualifyReceipt({ receiptPath: clean.receipt, trusted });
    assert.equal(qc.RECEIPT_QUALIFICATION.verdict, 'PASS');
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('PA2-RQ: the ACTUAL aggregator refuses PA2 missing/FAIL/NOT_PERFORMED (only documented success statuses count)', () => {
  // uses the same imported computeQualification + EXPECTED_OUTCOMES the canonical POST uses
  const ok = Object.fromEntries(Object.entries(EXPECTED_OUTCOMES).map(([id, exp]) => [id, exp])); // all required outcomes satisfied exactly
  assert.equal(computeQualification({ ...ok }, EXPECTED_OUTCOMES).verdict, 'QUALIFICATION_PASS');
  const missing = { ...ok }; delete missing.PA2_RECEIPT_QUALIFICATION;
  const qMissing = computeQualification(missing, EXPECTED_OUTCOMES);
  assert.equal(qMissing.verdict, 'QUALIFICATION_REFUSED'); assert.ok(qMissing.exitCode !== 0); assert.ok(qMissing.missing.includes('PA2_RECEIPT_QUALIFICATION'));
  for (const bad of ['FAIL', 'ERROR', 'NOT_PERFORMED', 'PASS ', '', true, 1]) {
    const q = computeQualification({ ...ok, PA2_RECEIPT_QUALIFICATION: bad }, EXPECTED_OUTCOMES);
    assert.equal(q.verdict, 'QUALIFICATION_REFUSED', 'value ' + JSON.stringify(bad));
    assert.ok(q.exitCode !== 0 && q.failing.includes('PA2_RECEIPT_QUALIFICATION'), 'value ' + JSON.stringify(bad));
  }
});
