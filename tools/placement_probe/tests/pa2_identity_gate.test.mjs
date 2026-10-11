// pa2_identity_gate.test.mjs — PA-2 P2: a LIVE input identity gate with frozen
// expected pins, separately measured values and a CONDITIONAL verdict
// (contract PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011, section G).
// The historical gen_pre_identity.mjs wrote verdict:'PASS' as a string literal — its
// PASS proved no effective gate (superseded READ_ONLY; see SUPERSESSION.md). Here
// the gate is exercised on PRIVATE MUTANT COPIES with UNCHANGED expected pins, and
// the runner's spy counters record that ZERO downstream analysis/correction/
// ref-reservation callbacks are invoked by THIS runner after a refusal — an
// authentic zero observation about this runner's own callbacks (never reached on
// clean runs either); it does NOT by itself establish automatic downstream
// enforcement for any other or future runner (HISTORICAL_SPY_PROVEN_ZERO_DOWNSTREAM
// = RETRACTED; PA2_DOWNSTREAM_AUTOMATIC_ENFORCEMENT = NOT_ESTABLISHED; see
// docs/audits/PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011/
// SUPERSESSION.md). No mutant performs a real GitHub write. (Wording corrected by
// PA2-RC2 records-only supersession, 2026-10-11; the assertions are unchanged.)
import test from 'node:test';
import assert from 'node:assert/strict';
import os from 'node:os';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { EXPECTED_INPUT_PINS, verifyPin, verifyAllInputs, measureInput } from '../verify_inputs.mjs';

const TESTS = path.dirname(fileURLToPath(import.meta.url));
const RUNNER = path.resolve(TESTS, '..', '..', '..', 'docs', 'audits', 'PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011', 'PRE', 'verify_inputs_runner.mjs');
const tmp = () => fs.mkdtempSync(path.join(os.tmpdir(), 'pe-t-pa2-'));

test('PA2: the gate module carries the 16 frozen pins as constants (expected never derived from measured)', () => {
  assert.equal(EXPECTED_INPUT_PINS.length, 16);
  for (const pin of EXPECTED_INPUT_PINS) {
    assert.ok(Number.isSafeInteger(pin.sizeBytes) && pin.sizeBytes > 0);
    assert.match(pin.sha256, /^[0-9a-fA-F]{64}$/);
  }
  // a separate measurement of a clean pinned input matches
  const m = measureInput(EXPECTED_INPUT_PINS[0].path);
  assert.equal(m.exists, true);
  assert.equal(m.sizeBytes, EXPECTED_INPUT_PINS[0].sizeBytes);
  assert.equal(m.sha256.toUpperCase(), EXPECTED_INPUT_PINS[0].sha256.toUpperCase());
});

test('PA2: unit mutants on PRIVATE copies with UNCHANGED expected — clean MATCH, wrong-sha/size/missing all BLOCKED', () => {
  const root = tmp(); try {
    const pin = EXPECTED_INPUT_PINS[8]; // the pinned ZIP member
    // clean private copy -> MATCH
    const clean = path.join(root, 'clean.zip');
    fs.copyFileSync(pin.path, clean);
    const rClean = verifyPin(pin, clean);
    assert.equal(rClean.compareResult, 'MATCH'); assert.equal(rClean.inputMatch, true);
    // changed SHA at the SAME size -> SHA_MISMATCH
    const sameSize = path.join(root, 'same_size.zip');
    const bytes = fs.readFileSync(pin.path);
    bytes[bytes.length - 1] ^= 0x01; // one flipped byte: same size, different SHA256
    fs.writeFileSync(sameSize, bytes);
    assert.equal(bytes.length, pin.sizeBytes, 'mutant keeps the pinned size');
    const rSha = verifyPin(pin, sameSize);
    assert.equal(rSha.compareResult, 'SHA_MISMATCH'); assert.equal(rSha.inputMatch, false);
    // changed size -> SIZE_MISMATCH
    const otherSize = path.join(root, 'other_size.zip');
    fs.writeFileSync(otherSize, Buffer.concat([fs.readFileSync(pin.path), Buffer.from([0x00])]));
    const rSize = verifyPin(pin, otherSize);
    assert.equal(rSize.compareResult, 'SIZE_MISMATCH'); assert.equal(rSize.inputMatch, false);
    // missing -> MISSING
    const rMiss = verifyPin(pin, path.join(root, 'does_not_exist.zip'));
    assert.equal(rMiss.compareResult, 'MISSING'); assert.equal(rMiss.inputMatch, false);
    // the gate over ALL pins with every input overridden to the same-size-wrong-sha mutant
    const overrides = Object.fromEntries(EXPECTED_INPUT_PINS.map(p => [p.pin, sameSize]));
    const g = verifyAllInputs(EXPECTED_INPUT_PINS, overrides);
    assert.equal(g.verdict, 'BLOCKED_INPUT_IDENTITY');
    assert.equal(g.blockedCount, 16);
    assert.equal(g.EFFECTIVE_GATE_RESULT, 'GATE_BLOCKED__DOWNSTREAM_REFUSED_ZERO_CALLS');
    // one clean override of a WRONG pin is still blocked (the others are real and clean) — pin-level precision
    const g2 = verifyAllInputs(EXPECTED_INPUT_PINS, { [EXPECTED_INPUT_PINS[0].pin]: sameSize });
    assert.equal(g2.verdict, 'BLOCKED_INPUT_IDENTITY');
    assert.deepEqual(g2.blockedPins.map(b => b.pin), [EXPECTED_INPUT_PINS[0].pin]);
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('PA2: the live runner is actually invoked — clean inputs authorize (exit 0), mutants refuse (exit 3) with ZERO downstream calls', () => {
  // REAL-SEQUENCE-style invocation: no overrides — all 16 pins measured at their true paths
  const receiptClean = path.join(tmp(), 'receipt_clean.json');
  const clean = spawnSync(process.execPath, [RUNNER, '--receipt', receiptClean], { encoding: 'utf8', timeout: 120000 });
  assert.equal(clean.status, 0, 'clean gate: ' + clean.stderr);
  const rc = JSON.parse(fs.readFileSync(receiptClean, 'utf8'));
  assert.equal(rc.mode, 'REAL_SEQUENCE');
  assert.equal(rc.gate.verdict, 'PASS');
  assert.equal(rc.gate.matched, 16);
  assert.equal(rc.gate.EFFECTIVE_GATE_RESULT, 'GATE_PASS__DOWNSTREAM_AUTHORIZED');
  assert.match(rc.command, /verify_inputs_runner\.mjs/, 'the receipt records the actual command');
  assert.ok(rc.callPath.includes('tools/placement_probe/verify_inputs.mjs'), 'the receipt records the call path through the gate module');
  assert.equal(typeof rc.moduleIdentity.gateModule.sha256, 'string');

  // MUTANT: same-size-wrong-sha private copies for every pin; expected pins UNCHANGED
  const root = tmp(); try {
    const mutantDir = path.join(root, 'mutants'); fs.mkdirSync(mutantDir, { recursive: true });
    const overrides = {};
    for (const pin of EXPECTED_INPUT_PINS) {
      const bytes = fs.readFileSync(pin.path);
      bytes[bytes.length - 1] ^= 0x01;
      const f = path.join(mutantDir, pin.pin + '.bin');
      fs.writeFileSync(f, bytes);
      overrides[pin.pin] = f;
    }
    const ovPath = path.join(root, 'overrides.json');
    fs.writeFileSync(ovPath, JSON.stringify(overrides));
    const receiptMut = path.join(root, 'receipt_mutant.json');
    const mut = spawnSync(process.execPath, [RUNNER, '--overrides-json', ovPath, '--receipt', receiptMut], { encoding: 'utf8', timeout: 120000 });
    assert.equal(mut.status, 3, 'mutant gate must exit nonzero');
    assert.match(mut.stderr, /GATE_BLOCKED__DOWNSTREAM_REFUSED_ZERO_CALLS/);
    const rm = JSON.parse(fs.readFileSync(receiptMut, 'utf8'));
    assert.equal(rm.mode, 'MUTANT_TEST (private copies; expected pins frozen and unchanged)');
    assert.equal(rm.gate.verdict, 'BLOCKED_INPUT_IDENTITY');
    assert.equal(rm.gate.blockedCount, 16);
    assert.deepEqual(rm.downstreamCallsAfterGate, { analysis: 0, correction: 0, refReservation: 0, postQualification: 0 }, 'spy counters record ZERO downstream calls by THIS runner after the refusal (authentic zero observation; NOT proof of downstream automatic enforcement — see SUPERSESSION.md of PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011)');
    assert.match(rm.downstreamPolicy, /must NOT run/);
    // missing-file mutant: every pin overridden to a nonexistent path
    const overridesMissing = Object.fromEntries(EXPECTED_INPUT_PINS.map(p => [p.pin, path.join(root, 'missing', p.pin)]));
    const ovMiss = path.join(root, 'overrides_missing.json');
    fs.writeFileSync(ovMiss, JSON.stringify(overridesMissing));
    const miss = spawnSync(process.execPath, [RUNNER, '--overrides-json', ovMiss, '--receipt', path.join(root, 'receipt_missing.json')], { encoding: 'utf8', timeout: 120000 });
    assert.equal(miss.status, 3, 'missing-input gate must exit nonzero (controlled BLOCKED, not an ENOENT crash)');
    const rmis = JSON.parse(fs.readFileSync(path.join(root, 'receipt_missing.json'), 'utf8'));
    assert.equal(rmis.gate.verdict, 'BLOCKED_INPUT_IDENTITY');
    assert.equal(rmis.gate.blockedPins.every(b => b.compareResult === 'MISSING'), true);
    assert.deepEqual(rmis.downstreamCallsAfterGate, { analysis: 0, correction: 0, refReservation: 0, postQualification: 0 });
    // wrong-size mutant for one pin only: still blocked, at that pin
    const bytes = fs.readFileSync(EXPECTED_INPUT_PINS[0].path);
    const grown = path.join(root, 'grown.bin'); fs.writeFileSync(grown, Buffer.concat([bytes, Buffer.from([0])]));
    const ovSize = path.join(root, 'overrides_size.json');
    fs.writeFileSync(ovSize, JSON.stringify({ [EXPECTED_INPUT_PINS[0].pin]: grown }));
    const size = spawnSync(process.execPath, [RUNNER, '--overrides-json', ovSize, '--receipt', path.join(root, 'receipt_size.json')], { encoding: 'utf8', timeout: 120000 });
    assert.equal(size.status, 3);
    const rsize = JSON.parse(fs.readFileSync(path.join(root, 'receipt_size.json'), 'utf8'));
    assert.deepEqual(rsize.gate.blockedPins.map(b => b.compareResult), ['SIZE_MISMATCH']);
    assert.deepEqual(rsize.downstreamCallsAfterGate, { analysis: 0, correction: 0, refReservation: 0, postQualification: 0 });
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});
