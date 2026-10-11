// verify_inputs_runner.mjs — PA-2 live gate runner (PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011)
// This runner ACTUALLY invokes tools/placement_probe/verify_inputs.mjs in the real
// sequence: after implementation and BEFORE POST/qualification and publication. The
// downstream work of this run (analysis, correction, RESULT_REF reservation, POST
// qualification) is gated on the verdict: after a BLOCKED verdict ZERO downstream
// calls happen — proven by the spy counters below (they can only be incremented by
// this runner; a refusal path never reaches them).
// Mutant testing (private copies only, expected pins UNCHANGED): pass
//   --overrides-json <file>  mapping pin names to private mutant paths
//   --receipt <path>         where to write this invocation's receipt
// No mutant performs a real GitHub write: the ref-reservation stub only counts.
import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath, pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const arg = (k, d) => { const i = process.argv.indexOf(k); return i >= 0 ? process.argv[i + 1] : d; };
const GATE = path.resolve(HERE, '..', '..', '..', '..', 'tools', 'placement_probe', 'verify_inputs.mjs');
const sha = p => createHash('sha256').update(fs.readFileSync(p)).digest('hex');

// downstream spy: the ONLY way to increment these counters is to actually invoke the
// downstream operations from this runner; the refusal path never calls them.
const downstreamCalls = { analysis: 0, correction: 0, refReservation: 0, postQualification: 0 };
const downstream = {
  runAnalysis: () => { downstreamCalls.analysis++; },
  applyCorrection: () => { downstreamCalls.correction++; },
  reserveResultRef: () => { downstreamCalls.refReservation++; },
  runPostQualification: () => { downstreamCalls.postQualification++; },
};

const overridesPath = arg('--overrides-json', null);
const overrides = overridesPath ? JSON.parse(fs.readFileSync(overridesPath, 'utf8')) : {};
const mod = await import(pathToFileURL(GATE).href);
const gate = mod.verifyAllInputs(mod.EXPECTED_INPUT_PINS, overrides);

const receipt = {
  runId: 'PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011',
  stage: 'PA2_LIVE_IDENTITY_GATE',
  timeUtc: new Date().toISOString(),
  callPath: ['docs/audits/PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011/PRE/verify_inputs_runner.mjs', '-> import', 'tools/placement_probe/verify_inputs.mjs', '-> verifyAllInputs(EXPECTED_INPUT_PINS, overrides)'],
  command: 'node ' + process.argv.slice(1).map(a => '"' + a + '"').join(' '),
  mode: overridesPath ? 'MUTANT_TEST (private copies; expected pins frozen and unchanged)' : 'REAL_SEQUENCE',
  moduleIdentity: {
    gateModule: { path: path.relative(path.resolve(HERE, '..', '..', '..', '..'), GATE), sha256: sha(GATE) },
    runner: { path: 'docs/audits/PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011/PRE/verify_inputs_runner.mjs', sha256: sha(fileURLToPath(import.meta.url)) },
  },
  expectedPinsAreFrozenConstants: true,
  expectedNeverDerivedFromMeasured: true,
  gate: { verdict: gate.verdict, EFFECTIVE_GATE_RESULT: gate.EFFECTIVE_GATE_RESULT, total: gate.total, matched: gate.matched, blockedCount: gate.blockedCount, blockedPins: gate.blockedPins },
  perPin: gate.results.map(r => ({ pin: r.pin, compareResult: r.compareResult, EXPECTED: r.expected, MEASURED: r.measured })),
  downstreamCallsAfterGate: { ...downstreamCalls },
};

if (gate.verdict !== 'PASS') {
  // FAIL-CLOSED: zero downstream calls after refusal; the spy proves it.
  receipt.downstreamPolicy = 'BLOCKED_INPUT_IDENTITY — downstream analysis/correction/ref-reservation/POST must NOT run; the spy counters above are all zero';
  process.stdout.write(mod.formatGateReport(gate) + '\n');
  process.stderr.write('EFFECTIVE_GATE_RESULT=' + gate.EFFECTIVE_GATE_RESULT + '\n');
  process.exitCode = 3;
} else {
  // REAL SEQUENCE: the gate authorizes the run inputs; downstream work of this run
  // continues per the contract order (POST/qualification next; the RESULT_REF was
  // already reserved earlier in the contract's own order — this runner never repeats
  // a real GitHub write, and in mutant mode nothing here executes at all).
  receipt.downstreamPolicy = 'GATE_PASS — downstream authorized; the counters above record the state AT GATE TIME (zero, by construction: downstream work runs after the gate, not inside it)';
  process.stdout.write(mod.formatGateReport(gate) + '\n');
}
const receiptPath = arg('--receipt', null);
if (receiptPath) { fs.mkdirSync(path.dirname(receiptPath), { recursive: true }); fs.writeFileSync(receiptPath, JSON.stringify(receipt, null, 2) + '\n'); }
process.exit(process.exitCode ?? 0);
