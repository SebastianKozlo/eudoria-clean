// pa1_regression.test.mjs — PA-1: the original XYZ 1200/4800 counterexample as named
// regression fixtures (contract PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011,
// section F). This closes a REGRESSION COVERAGE GAP: the unchanged BASE already
// computes the right rates on these bytes (verified in PRESERVED PRE and by the
// pinned Desktop recheck); the algorithm is NOT rewritten and no new counterexample
// is claimed. The ground truth below is computed by this harness directly from the
// synthetic bytes — independently of the production reader/sampler.
import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { analyzeBlob } from '../placement_probe.mjs';
import * as FX from './fixtures.mjs';

const sets = { S_tpl: new Set([4057, 4058]), S_model: new Set([218757]) };
const sha = b => createHash('sha256').update(b).digest('hex');
const isTarget = c => c.header === 16 && c.stride === 32 && c.idOffset === 0 && c.idWidth === 2 && c.xyzOffset === 4;

// independent truth: which rows the 1200-of-4800 sampler covers is computed here by
// the analytic form of the fixture construction (i = floor((j+0.5)*4800/1200) = 4j+2),
// and the triple/ID truths are read straight from the synthetic bytes — no production
// sampler, no production candidate reader.
function groundTruth(buf) {
  const sampled = new Set();
  for (let j = 0; j < 1200; j++) sampled.add(Math.floor((j + 0.5) * 4800 / 1200));
  let finiteTriples = 0, idHits = 0, sampleFiniteTriples = 0;
  for (let i = 0; i < 4800; i++) {
    const fin = [4, 8, 12].every(o => Number.isFinite(buf.readFloatLE(16 + i * 32 + o)));
    if (fin) finiteTriples++;
    if (sampled.has(i) && fin) sampleFiniteTriples++;
    const id = buf.readUInt16LE(16 + i * 32);
    if (id === 4057 || id === 4058) idHits++;
  }
  return {
    rows: 4800, sampledRows: sampled.size,
    FULL_XYZ_FINITE_RATE: finiteTriples / 4800,
    SAMPLE_XYZ_FINITE_RATE: sampleFiniteTriples / sampled.size,
    FULL_ID_HIT_RATE: idHits / 4800,
  };
}
function productionOn(buf, extra = {}) {
  const r = analyzeBlob(buf, sets, { maxStride: 32, maxHeader: 16, top: 10, budgetThresholds: { fullCensusRows: 4800 }, ...extra });
  const t = r.candidates.find(isTarget);
  return { r, t };
}

test('PA1-A: the exact original builder — sample 1.0 vs full 0.25 (XYZ) and 0.25 (ID); FULL_CENSUS 4800 under the legal budget 4800', () => {
  const b = FX.pa1A();
  assert.equal(b.length, 153616);
  assert.equal(sha(b).toUpperCase(), FX.PA1_PINS.A.sha256, 'PA1-A bytes are byte-exactly the pinned original counterexample');
  const truth = groundTruth(b);
  assert.equal(truth.rows, 4800); assert.equal(truth.sampledRows, 1200);
  assert.equal(truth.SAMPLE_XYZ_FINITE_RATE, 1.0);
  assert.equal(truth.FULL_XYZ_FINITE_RATE, 0.25);
  assert.equal(truth.FULL_ID_HIT_RATE, 0.25, 'the ORIGINAL fixture does NOT have valid IDs everywhere');
  const { r, t } = productionOn(b);
  assert.ok(t, 'the target header16/stride32/idOffset0/idWidth2/xyzOffset4 must be found');
  assert.equal(t.sampleCount, 1200);
  assert.equal(t.sampleXyzFiniteRate, 1.0);
  assert.equal(t.censusStatus, 'FULL_CENSUS', 'the mandatory target gets a legal budget of exactly 4800 census rows');
  assert.equal(t.fullCensusRowCount, 4800);
  assert.equal(t.fullCensusXyzFiniteRate, 0.25);
  assert.equal(t.fullCensusIdRate, 0.25);
  // the production result must equal the independent truth, not merely a self-consistent value
  assert.equal(t.fullCensusXyzFiniteRate, truth.FULL_XYZ_FINITE_RATE);
  assert.equal(t.fullCensusIdRate, truth.FULL_ID_HIT_RATE);
});

test('PA1-B: isolating XYZ — only the unsampled IDs change; sample 1.0 and full XYZ 0.25 unchanged, full ID becomes 1.0', () => {
  const a = FX.pa1A(), b = FX.pa1B();
  assert.equal(sha(b).toUpperCase(), FX.PA1_PINS.B.sha256, 'PA1-B bytes match the pinned pin');
  // A -> B changes ONLY unsampled bytes (IDs of rows i%4!==2): the sampled rows are untouched
  for (let j = 0; j < 1200; j++) {
    const i = Math.floor((j + 0.5) * 4800 / 1200), p = 16 + i * 32;
    assert.equal(b.readUInt16LE(p), a.readUInt16LE(p), 'sampled row ' + i + ' is unchanged');
    for (let o = 4; o < 32; o += 1) if (o !== 0) assert.equal(b[p + o], a[p + o], 'sampled row ' + i + ' byte +' + o + ' is unchanged');
  }
  const truth = groundTruth(b);
  assert.equal(truth.SAMPLE_XYZ_FINITE_RATE, 1.0);
  assert.equal(truth.FULL_XYZ_FINITE_RATE, 0.25, 'XYZ truth unchanged — only IDs were touched');
  assert.equal(truth.FULL_ID_HIT_RATE, 1.0);
  const { t } = productionOn(b);
  assert.ok(t);
  assert.equal(t.censusStatus, 'FULL_CENSUS');
  assert.equal(t.sampleXyzFiniteRate, 1.0);
  assert.equal(t.fullCensusXyzFiniteRate, 0.25);
  assert.equal(t.fullCensusIdRate, 1.0);
});

test('PA1-C: only the unsampled XYZ changes — sample 1.0, full XYZ 1.0, full ID 1.0', () => {
  const b = FX.pa1C(), bb = FX.pa1B();
  assert.equal(sha(b).toUpperCase(), FX.PA1_PINS.C.sha256, 'PA1-C bytes match the pinned pin');
  // B -> C changes ONLY the unsampled f32 xyz: IDs and sampled rows are untouched
  for (let i = 0; i < 4800; i++) {
    const p = 16 + i * 32;
    assert.equal(b.readUInt16LE(p), bb.readUInt16LE(p), 'ID of row ' + i + ' unchanged');
    if (i % 4 === 2) for (let o = 0; o < 32; o++) assert.equal(b[p + o], bb[p + o], 'sampled row ' + i + ' unchanged');
  }
  const truth = groundTruth(b);
  assert.equal(truth.SAMPLE_XYZ_FINITE_RATE, 1.0);
  assert.equal(truth.FULL_XYZ_FINITE_RATE, 1.0, 'changing ONLY unsampled bytes changed the FULL result');
  assert.equal(truth.FULL_ID_HIT_RATE, 1.0);
  const { t } = productionOn(b);
  assert.ok(t);
  assert.equal(t.censusStatus, 'FULL_CENSUS');
  assert.equal(t.sampleXyzFiniteRate, 1.0, 'the sample is saturated in all three variants — the sample alone never proves the table');
  assert.equal(t.fullCensusXyzFiniteRate, 1.0);
  assert.equal(t.fullCensusIdRate, 1.0);
});

test('PA1: the full result changes ONLY after changing unsampled bytes (A->B->C delta discipline)', () => {
  const prodA = productionOn(FX.pa1A()).t, prodB = productionOn(FX.pa1B()).t, prodC = productionOn(FX.pa1C()).t;
  // A -> B: unsampled IDs changed -> ONLY the full ID rate changes
  assert.equal(prodA.fullCensusIdRate, 0.25); assert.equal(prodB.fullCensusIdRate, 1.0);
  assert.equal(prodA.fullCensusXyzFiniteRate, prodB.fullCensusXyzFiniteRate, 'full XYZ unchanged by an ID-only change');
  assert.equal(prodA.sampleXyzFiniteRate, prodB.sampleXyzFiniteRate, 'sample unchanged by an unsampled change');
  // B -> C: unsampled XYZ changed -> ONLY the full XYZ rate changes
  assert.equal(prodB.fullCensusXyzFiniteRate, 0.25); assert.equal(prodC.fullCensusXyzFiniteRate, 1.0);
  assert.equal(prodB.fullCensusIdRate, prodC.fullCensusIdRate, 'full ID unchanged by an XYZ-only change');
  assert.equal(prodB.sampleXyzFiniteRate, prodC.sampleXyzFiniteRate);
});

// harness gate: rejects a forged FULL_XYZ=1.0 for A/B while the sample stays 1.0
function pa1HarnessGate(fixtureName, observed) {
  const pin = FX.PA1_PINS[fixtureName];
  const reasons = [];
  if (observed.sampleXyzFiniteRate !== pin.SAMPLE_XYZ_FINITE_RATE) reasons.push('sample XYZ ' + observed.sampleXyzFiniteRate + ' != pinned ' + pin.SAMPLE_XYZ_FINITE_RATE);
  if (observed.fullCensusXyzFiniteRate !== pin.FULL_XYZ_FINITE_RATE) reasons.push('full XYZ ' + observed.fullCensusXyzFiniteRate + ' != pinned ' + pin.FULL_XYZ_FINITE_RATE);
  if (observed.fullCensusIdRate !== pin.FULL_ID_HIT_RATE) reasons.push('full ID ' + observed.fullCensusIdRate + ' != pinned ' + pin.FULL_ID_HIT_RATE);
  return { accepted: reasons.length === 0, reasons };
}

test('PA1: harness control REJECTS a mutant FULL_XYZ=1.0 for A/B while keeping sample 1.0', () => {
  for (const name of ['A', 'B']) {
    // genuine production values pass
    const genuine = productionOn(name === 'A' ? FX.pa1A() : FX.pa1B()).t;
    assert.equal(pa1HarnessGate(name, genuine).accepted, true);
    // MUTANT: claims full XYZ 1.0 (the C-like value) while keeping the sample at 1.0
    const mutant = { sampleXyzFiniteRate: 1.0, fullCensusXyzFiniteRate: 1.0, fullCensusIdRate: FX.PA1_PINS[name].FULL_ID_HIT_RATE };
    const g = pa1HarnessGate(name, mutant);
    assert.equal(g.accepted, false, 'mutant FULL_XYZ=1.0 for ' + name + ' must be rejected');
    assert.ok(g.reasons.some(x => /full XYZ/.test(x)), 'the rejection names the full-XYZ contradiction: ' + g.reasons.join('; '));
    // and the positive alias: the gate accepts the TRUE A/B rates (0.25) — sample alone is not proof
    const truthLike = { sampleXyzFiniteRate: 1.0, fullCensusXyzFiniteRate: 0.25, fullCensusIdRate: FX.PA1_PINS[name].FULL_ID_HIT_RATE };
    assert.equal(pa1HarnessGate(name, truthLike).accepted, true);
  }
  // C is the only variant whose pinned full XYZ is 1.0
  assert.equal(FX.PA1_PINS.C.FULL_XYZ_FINITE_RATE, 1.0);
  assert.equal(pa1HarnessGate('C', productionOn(FX.pa1C()).t).accepted, true);
});

test('PA1: without the census budget the target stays honestly PARTIAL (no fabricated full census)', () => {
  const { r, t } = productionOn(FX.pa1A(), { budgetThresholds: { fullCensusRows: 100 } });
  assert.ok(t, 'the target is still found without a full census');
  assert.equal(t.censusStatus, 'PARTIAL_BUDGET_EXHAUSTED', 'the missing budget stays an honest PARTIAL');
  assert.equal(t.fullCensusRowCount, null);
  assert.equal(t.fullCensusXyzFiniteRate, null);
  assert.equal(t.fullCensusIdRate, null);
  // the SAMPLE quantities are still reported and still do not claim table quality
  assert.equal(t.sampleXyzFiniteRate, 1.0);
  assert.ok(r.stats.budgetExhausted || r.budget.exhausted.includes('FULL_CENSUS_ROWS'), 'the census budget stop is visible');
});
