// run_post.mjs — CANONICAL POST for PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011
// (QUALIFICATION_CODE_ROOT tools/placement_probe/qualification/pa2_r1; contract §4/§5).
//
// SUPERSESSION (recorded in the run package SUPERSESSION.md): this canonical POST is
// adapted from the predecessor full POST
//   docs/audits/PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011/POST/run_post.mjs
//   (BASE 28e91eb, SHA256 3BBDC404E40B0ED2135BA74D5C978E5DB810AAD0A962C45D23FBE04D4B25C3BB)
// and preserves its required cases and source mapping (ORIGINAL_SEVEN, FULL_SUITE,
// DA1_CENSUS, DA1_NOT_OPENED, DA2_CAP4, DA2_CAP256, DA2_MUTANT_COPY, DA2_SMALL_FIXTURE,
// DA3_REFUSALS, DA3_POSITIVES, PA1_REGRESSION, AGGREGATOR_CONTROL). Changes:
//   1. CLI adds --receipt <receipt-under-test.json> and --out <private-output-dir>;
//      all outputs are written to --out, never alongside historical scripts.
//   2. The predecessor PA2_LIVE_GATE acceptance condition
//        liveOk = verdict==='PASS' && matched===16 && mode==='REAL_SEQUENCE'
//      (the externally measured false-PASS defect: M1/M2 receipts with zeroed
//      MEASURED.sha256 / gateModule.sha256 passed the full POST) is SUPERSEDED by
//      PA2_RECEIPT_QUALIFICATION: the receipt is validated by the shared corrected
//      validator (validate_receipt.mjs — trusted-pin verification, strict legacy
//      profile, per-pin re-derivation, summary recomputation, module-identity
//      check, live input remeasurement, fail-closed) and is a REQUIRED CONJUNCT:
//      a refused receipt makes the whole aggregator QUALIFICATION_REFUSED/exit!=0.
//   3. New required cases: BASE_53_REPLAY (exact BASE 53-test replay, separate from
//      the new suite), DA2_TWO_SOURCE (DA2-COV cap32 29+3 two-contributing-source
//      regression through the actual scan).
//   4. The aggregator is the SAME computeQualification (imported from the shared
//      qualification module) the predecessor used — expectations frozen in
//      EXPECTED_OUTCOMES (PA2 result required; missing/FAIL/ERROR/NOT_PERFORMED =>
//      overall REFUSED, conjunctive).
// The scanner, frozen gate module (verify_inputs.mjs), adapters and historical
// packages are UNCHANGED. This harness is the executor's own harness — replaying it
// is not a second implementation. All executions happen in an ISOLATED STAGE of
// byte-identical copies (SHA-recorded); the pinned BASE adapters are imported from
// the stage. No game payload is scanned; fixtures are synthetic.
import fs from 'node:fs'; import path from 'node:path'; import os from 'node:os';
import { spawnSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';
import { qualifyReceipt, loadTrusted, computeQualification, EXPECTED_OUTCOMES, TRUSTED_GATE_MODULE, TRUSTED_RUNNER, RECEIPT_PROFILE } from './validate_receipt.mjs';
import { measureTwoSource, TWO_SOURCE_TARGETS } from './two_source.mjs';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const arg = (k, d) => { const i = process.argv.indexOf(k); return i >= 0 ? process.argv[i + 1] : d; };
const WORKTREE = path.resolve(arg('--worktree', null));
const RUNROOT = path.resolve(arg('--runroot', null));
const KITDIR = path.resolve(arg('--kitdir', null));
const RECEIPT = path.resolve(arg('--receipt', null));
const OUT = path.resolve(arg('--out', null));
if (!WORKTREE || !RUNROOT || !KITDIR || !RECEIPT || !OUT) { console.error('INVALID_CONFIGURATION: required --worktree --runroot --kitdir --receipt --out'); process.exitCode = 3; process.exit(process.exitCode ?? 3); }
const sha = b => createHash('sha256').update(b).digest('hex');
const shaF = p => sha(fs.readFileSync(p));
const node = process.version;
const time = () => new Date().toISOString();
const sets = { S_tpl: new Set([4057, 4058]), S_model: new Set([218757]) };
const EXECUTED_COMMAND = 'node ' + process.argv.slice(1).map(a => '"' + a + '"').join(' ');

// ---------- isolated stage (byte-identical copies, SHA-recorded) ----------
const STAGE = path.join(RUNROOT, 'staging', 'stage_post'); fs.rmSync(STAGE, { recursive: true, force: true }); fs.mkdirSync(STAGE, { recursive: true });
const stageCopies = [];
const STAGE_FILES = ['tools/placement_probe/placement_probe.mjs', 'tools/placement_probe/ids_from_export.mjs', 'tools/placement_probe/verify_inputs.mjs', 'tools/placement_probe/README.md',
  'tools/placement_probe/tests/fixtures.mjs', 'tools/placement_probe/tests/probe.test.mjs', 'tools/placement_probe/tests/cli-fixture.test.mjs', 'tools/placement_probe/tests/budget.test.mjs', 'tools/placement_probe/tests/census_extra.test.mjs', 'tools/placement_probe/tests/correction_matrix.test.mjs', 'tools/placement_probe/tests/da1_census.test.mjs', 'tools/placement_probe/tests/da2_retained.test.mjs', 'tools/placement_probe/tests/da3_budget.test.mjs', 'tools/placement_probe/tests/pa1_regression.test.mjs', 'tools/placement_probe/tests/pa2_identity_gate.test.mjs',
  'tools/placement_probe/tests/pa2_receipt_qualification.test.mjs', 'tools/placement_probe/tests/da2_two_source.test.mjs',
  'tools/placement_probe/qualification/pa2_r1/validate_receipt.mjs', 'tools/placement_probe/qualification/pa2_r1/two_source.mjs',
  'src/pesource/Bnt2Archive.js', 'src/pesource/ArkArchive.js', 'docs/audits/PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011/PRE/verify_inputs_runner.mjs'];
for (const f of STAGE_FILES) {
  const src = path.join(WORKTREE, f), dst = path.join(STAGE, f);
  fs.mkdirSync(path.dirname(dst), { recursive: true }); fs.copyFileSync(src, dst);
  const a = shaF(src), b = shaF(dst);
  if (a !== b) throw Error('stage copy mismatch: ' + f);
  stageCopies.push({ path: f, sha256: a, byteIdentical: true });
}
fs.writeFileSync(path.join(STAGE, 'package.json'), '{"type":"module"}');
const codeIdentity = { placement_probe: shaF(path.join(STAGE, 'tools/placement_probe/placement_probe.mjs')), verify_inputs: shaF(path.join(STAGE, 'tools/placement_probe/verify_inputs.mjs')), fixtures: shaF(path.join(STAGE, 'tools/placement_probe/tests/fixtures.mjs')), runner: shaF(path.join(STAGE, 'docs/audits/PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011/PRE/verify_inputs_runner.mjs')), receiptValidator: shaF(path.join(STAGE, 'tools/placement_probe/qualification/pa2_r1/validate_receipt.mjs')), twoSourceHelper: shaF(path.join(STAGE, 'tools/placement_probe/qualification/pa2_r1/two_source.mjs')), adapters: { Bnt2Archive: shaF(path.join(STAGE, 'src/pesource/Bnt2Archive.js')), ArkArchive: shaF(path.join(STAGE, 'src/pesource/ArkArchive.js')) }, node };
const STAGE_TOOL = path.join(STAGE, 'tools/placement_probe/placement_probe.mjs');
const STAGE_TESTS = path.join(STAGE, 'tools/placement_probe/tests');
const STAGE_RUNNER = path.join(STAGE, 'docs/audits/PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011/PRE/verify_inputs_runner.mjs');
fs.mkdirSync(OUT, { recursive: true });
const { analyzeBlob, Budget, censusGate, BUDGET_CEILINGS } = await import(pathToFileURL(STAGE_TOOL).href);
const FX = await import(pathToFileURL(path.join(STAGE_TESTS, 'fixtures.mjs')).href);

function cli(tag, inputs, args = [], tool = STAGE_TOOL) {
  const dir = path.join(RUNROOT, 'staging', 'post_cli', tag); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  const ids = path.join(dir, 'ids.json'); fs.writeFileSync(ids, JSON.stringify({ S_tpl: [4057, 4058], S_model: [218757] }));
  const res = spawnSync(process.execPath, [tool, '--repo', STAGE, '--ids', ids, '--out', path.join(dir, 'out'), ...inputs.flatMap(n => ['--input', n]), ...args], { encoding: 'utf8', timeout: 180000 });
  let summary = null; try { summary = JSON.parse(fs.readFileSync(path.join(dir, 'out', 'SUMMARY.json'), 'utf8')); } catch {}
  return { exitCode: res.status, stderr: res.stderr, stdout: res.stdout, summary, dir, out: path.join(dir, 'out') };
}
function runTests(cwd, files) {
  const res = spawnSync(process.execPath, ['--test', ...files], { encoding: 'utf8', cwd, timeout: 1800000 });
  const m = re => Number((res.stdout.match(re) || [])[1]);
  return { exitCode: res.status, stdout: res.stdout, stderr: res.stderr, tests: m(/# tests (\d+)/), pass: m(/# pass (\d+)/), fail: m(/# fail (\d+)/) };
}
const cases = {};
const fieldCase = (id, v) => { cases[id] = { CASE_ID: id, timeUtc: time(), ...v }; };

// ---------- 1. ORIGINAL_SEVEN (pinned ZIP kit, isolated stage) ----------
{
  const KIT = path.join(RUNROOT, 'staging', 'stage_post_kit'); fs.rmSync(KIT, { recursive: true, force: true });
  for (const f of ['placement_probe.mjs', 'ids_from_export.mjs', 'tests/probe.test.mjs', 'tests/cli-fixture.test.mjs']) { fs.mkdirSync(path.dirname(path.join(KIT, f)), { recursive: true }); fs.copyFileSync(path.join(KITDIR, f), path.join(KIT, f)); }
  fs.writeFileSync(path.join(KIT, 'package.json'), '{"type":"module"}');
  const hashes = JSON.parse(fs.readFileSync(path.join(KITDIR, 'FILE_HASHES.json'), 'utf8'));
  const membersOk = hashes.every(m => { const b = fs.readFileSync(path.join(KITDIR, m.path)); return b.length === m.sizeBytes && sha(b) === m.sha256; });
  const r = runTests(KIT, ['tests/probe.test.mjs', 'tests/cli-fixture.test.mjs']);
  const names = ['CLI probes RAW, BNT2, Ark payload via locally imported compatible readers', 'discovers known synthetic record layout without treating it as historical placement', 'wrong IDs do not manufacture a template relation', 'no file/geometry source is inferred from a matching ID alone', 'missing template set is a hard error', 'truncated buffers and zero-row cases do not fabricate a pass', 'independent aligned anchors enable a joint label-position permutation control'];
  const sevenPass = names.every(n => new RegExp('^ok \\d+ - ' + n.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '$', 'm').test(r.stdout));
  fieldCase('ORIGINAL_SEVEN', {
    CODE_IDENTITY: { kitPlacementProbe: shaF(path.join(KIT, 'placement_probe.mjs')), zipMembersVerified: membersOk },
    FIXTURE_IDENTITY: 'pinned PE935_Placement_Probe_Kit_R1.zip (7 FILE_HASHES.json members verified)',
    MEASURED_QUANTITY: 'TAP pass/fail counts + the exact seven named tests', EXPECTED: { tests: 7, pass: 7, fail: 0, exitCode: 0, sevenPass: true },
    ACTUAL: { tests: r.tests, pass: r.pass, fail: r.fail, exitCode: r.exitCode, sevenPass },
    DENOMINATOR: 7, UNIT: 'tests', SOURCE_OF_TRUTH: 'node:test TAP output over the byte-pinned original kit',
    WHY_NON_CIRCULAR: 'the seven kit tests are replayed from the externally pinned ZIP whose members are re-verified by size+SHA before execution — the kit is independent of this correction',
    NEGATIVE_CONTROL: 'names must match EXACTLY — a renamed or dropped test fails sevenPass',
    FAILURE_CASE_DETECTED: 'original kit regression', TEST_RESULT: (r.exitCode === 0 && r.pass === 7 && r.fail === 0 && sevenPass && membersOk) ? 'PASS' : 'FAIL',
  });
}

// ---------- 2. BASE_53_REPLAY (exact BASE 53-test replay, separate from the new suite) ----------
let base53;
{
  const files = ['probe.test.mjs', 'cli-fixture.test.mjs', 'correction_matrix.test.mjs', 'budget.test.mjs', 'census_extra.test.mjs', 'da1_census.test.mjs', 'da2_retained.test.mjs', 'da3_budget.test.mjs', 'pa1_regression.test.mjs', 'pa2_identity_gate.test.mjs'];
  const r = runTests(STAGE_TESTS, files);
  base53 = r;
  fieldCase('BASE_53_REPLAY', {
    CODE_IDENTITY: codeIdentity, FIXTURE_IDENTITY: { stageCopies: stageCopies.length, allByteIdentical: stageCopies.every(c => c.byteIdentical), files: files.length },
    MEASURED_QUANTITY: 'TAP tests/pass/fail of the exact BASE 10 test files replayed separately from the new test set',
    EXPECTED: { tests: 53, pass: 53, fail: 0, exitCode: 0 },
    ACTUAL: { tests: r.tests, pass: r.pass, fail: r.fail, exitCode: r.exitCode },
    DENOMINATOR: 53, UNIT: 'tests', SOURCE_OF_TRUTH: 'node:test TAP output over the isolated byte-identical stage of the unchanged BASE tests',
    WHY_NON_CIRCULAR: 'the BASE test files are staged byte-identical (SHA per file) and run exactly as at BASE — this replay is a preservation check, not the new suite',
    NEGATIVE_CONTROL: 'any BASE test failing/flipping makes this case FAIL the whole qualification',
    FAILURE_CASE_DETECTED: 'a correction that damaged the preserved BASE coverage', TEST_RESULT: (r.exitCode === 0 && r.tests === 53 && r.pass === 53 && r.fail === 0) ? 'PASS' : 'FAIL',
  });
}

// ---------- 3. FULL_SUITE (isolated stage: BASE tests + new regressions) ----------
let suiteInfo;
{
  const files = ['probe.test.mjs', 'cli-fixture.test.mjs', 'correction_matrix.test.mjs', 'budget.test.mjs', 'census_extra.test.mjs', 'da1_census.test.mjs', 'da2_retained.test.mjs', 'da3_budget.test.mjs', 'pa1_regression.test.mjs', 'pa2_identity_gate.test.mjs', 'pa2_receipt_qualification.test.mjs', 'da2_two_source.test.mjs'];
  const r = runTests(STAGE_TESTS, files);
  const required = ['B1:', 'B2:', 'B3:', 'B4:', 'B5:', 'B6:', 'B7:', 'CX1:', 'CX2:', 'CX3:', 'CX4:', 'O1:', 'O2:', 'O3:', 'O4:', 'O5:', 'O6:', 'O7:', 'S7a:', 'S7b:', 'DA1-C1', 'DA1-C2', 'DA1-C3', 'DA1-C4', 'DA1-C5', 'DA3:', 'DA2:', 'PA1:', 'PA2:', 'PA2-RQ:', 'DA2-COV:'];
  const present = Object.fromEntries(required.map(k => [k.trim(), new RegExp('^ok \\d+ - ' + k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'm').test(r.stdout)]));
  const allPresent = Object.values(present).every(Boolean);
  suiteInfo = { r, present, allPresent, stdout: r.stdout };
  fieldCase('FULL_SUITE', {
    CODE_IDENTITY: codeIdentity, FIXTURE_IDENTITY: { stageCopies: stageCopies.length, allByteIdentical: stageCopies.every(c => c.byteIdentical), files: files.length },
    MEASURED_QUANTITY: 'TAP tests/pass/fail + presence of every required named coverage test (per-limit B1..B7, CX1..CX4, O1..O7, S7a/S7b, DA/PA tests, the new PA2-RQ receipt-qualification and DA2-COV two-source regressions)',
    EXPECTED: { fail: 0, exitCode: 0, allRequiredPresent: true },
    ACTUAL: { tests: r.tests, pass: r.pass, fail: r.fail, exitCode: r.exitCode, allRequiredPresent: allPresent, requiredPresent: present },
    DENOMINATOR: r.tests, UNIT: 'tests', SOURCE_OF_TRUTH: 'node:test TAP output over the isolated stage',
    WHY_NON_CIRCULAR: 'the required-name presence check is an independent prefix probe over TAP output — a dropped or renamed regression cannot hide behind the total count',
    NEGATIVE_CONTROL: 'a missing or failing required test flips allRequiredPresent/fail and must refuse qualification',
    FAILURE_CASE_DETECTED: 'regression in any required coverage area', TEST_RESULT: (r.exitCode === 0 && r.fail === 0 && allPresent) ? 'PASS' : 'FAIL',
  });
}

// ---------- 4. DA1_CENSUS ----------
{
  const dir = path.join(RUNROOT, 'staging', 'post_fixtures', 'da1_census'); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'four.bnt'), FX.realBnt2([0, 1, 2, 3].map(i => ({ name: `e${i}.rec`, data: FX.records80() }))));
  const r = cli('da1_census', [path.join(dir, 'four.bnt')], ['--budget-layout-evals', '100']);
  const c = r.summary.exclusionCensus[0];
  const d = c.dispositions;
  const expected = { e0: 'SCANNED/PARTIAL', tail: 'OVER_BUDGET/NOT_ANALYZED', scannedPayloadCount: 1, censusOk: true };
  const actual = {
    dispositions: d.map(x => ({ i: x.entryIndex, disp: x.disposition, admitted: x.admitted, payloadRead: x.payloadRead, started: x.analysisStarted, status: x.analysisStatus, detail: x.detail ?? null })),
    scannedPayloadCount: c.scannedPayloadCount, admittedCount: c.admittedCount, payloadReadCount: c.payloadReadCount,
    analysisStatusCounts: c.analysisStatusCounts, censusOk: c.censusOk, coverage: r.summary.budgets.coverage, layoutAttempts: r.summary.budgets.used.layoutAttempts, layoutRefusals: r.summary.budgets.used.layoutRefusals,
  };
  const semanticsOk = d[0].disposition === 'SCANNED' && d[0].analysisStarted === true && d[0].analysisStatus === 'PARTIAL' &&
    d.slice(1).every(x => x.disposition === 'OVER_BUDGET' && x.analysisStarted === false && x.analysisStatus === 'NOT_ANALYZED');
  // NEGATIVE CONTROL: mutate the measured census — flip entry 2 to SCANNED keeping the sum
  const mutant = JSON.parse(JSON.stringify(c));
  mutant.dispositions[2].disposition = 'SCANNED';
  const gate = censusGate(mutant);
  fieldCase('DA1_CENSUS', {
    CODE_IDENTITY: codeIdentity, FIXTURE_IDENTITY: { fourEntriesBnt: shaF(path.join(dir, 'four.bnt')), adapter: 'src/pesource/Bnt2Archive.js BASE git blob 1fb862905b4749f3336bb47da87441edbd018fb7 (real adapter, synthetic bytes)' },
    MEASURED_QUANTITY: 'per-entry disposition + state vector; scannedPayloadCount; census gate verdict on a mutated census',
    EXPECTED: expected, ACTUAL: actual,
    DENOMINATOR: 4, UNIT: 'declared entries', SOURCE_OF_TRUTH: 'scan execution state + the exported censusGate re-derivation',
    WHY_NON_CIRCULAR: 'the census is re-derived through the SAME exported censusGate the publication uses — a sum-keeping mutant is refused by the function whose opinion the summary carries',
    NEGATIVE_CONTROL: { mutant: 'entry 2 flipped to SCANNED, disposition sum kept', gateVerdict: gate.ok, gateReasons: gate.reasons, refused: gate.ok === false },
    FAILURE_CASE_DETECTED: 'false SCANNED for entries whose analysis never started (R2-5 P2)',
    TEST_RESULT: (r.exitCode === 0 && semanticsOk && c.scannedPayloadCount === 1 && c.censusOk === true && gate.ok === false) ? 'PASS' : 'FAIL',
  });
}

// ---------- 5. DA1_NOT_OPENED ----------
{
  const dir = path.join(RUNROOT, 'staging', 'post_fixtures', 'da1_not_opened'); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'first.ark'), FX.realArk([{ name: 'a.rec', data: FX.records80() }, { name: 'b.rec', data: FX.records80() }, { name: 'c.rec', data: FX.records80() }, { name: 'd.rec', data: FX.records80() }]));
  fs.writeFileSync(path.join(dir, 'second.ark'), FX.realArk([{ name: 'x.rec', data: FX.records80() }]));
  fs.writeFileSync(path.join(dir, 'third.bnt'), FX.realBnt2([{ name: 'y.rec', data: FX.records80() }]));
  const r = cli('da1_not_opened', [path.join(dir, 'first.ark'), path.join(dir, 'second.ark'), path.join(dir, 'third.bnt')], ['--budget-retained-candidates', '4']);
  const cs = r.summary.exclusionCensus;
  const first = cs[0], unopened = cs.slice(1);
  const unopenedOk = unopened.every(x => x.parseStatus === 'NOT_OPENED_BUDGET' && x.declaredEntryCount === 'UNKNOWN_ENTRY_COUNT' && Array.isArray(x.dispositions) && x.dispositions.length === 0 && x.scannedPayloadCount === 0 && x.censusOk === null);
  const firstOk = first.parseStatus === 'OK' && first.scannedPayloadCount === 4 && first.censusOk === true && first.containerKind === '.ark';
  fieldCase('DA1_NOT_OPENED', {
    CODE_IDENTITY: codeIdentity, FIXTURE_IDENTITY: { firstArk: shaF(path.join(dir, 'first.ark')), adapter: 'real BASE ArkArchive + Bnt2Archive (synthetic bytes)' },
    MEASURED_QUANTITY: 'census records of never-opened declared files',
    EXPECTED: { unopened: 'NOT_OPENED_BUDGET + UNKNOWN_ENTRY_COUNT + empty dispositions + censusOk null', first: 'fully accounted (4 SCANNED/COMPLETED)' },
    ACTUAL: { unopened: unopened.map(x => ({ input: path.basename(x.input), parseStatus: x.parseStatus, declared: x.declaredEntryCount, dispositions: x.dispositions.length, censusOk: x.censusOk, reason: x.unopenedReason })), first: { parseStatus: first.parseStatus, scanned: first.scannedPayloadCount, censusOk: first.censusOk, kind: first.containerKind } },
    DENOMINATOR: 3, UNIT: 'declared files', SOURCE_OF_TRUTH: 'scan execution (no catalog invented for unopened files)',
    WHY_NON_CIRCULAR: 'never-opened files are recorded from actual refusal state at the budget stop — no entry count is invented from file names',
    NEGATIVE_CONTROL: 'the first container must remain fully accounted — partial accounting of the opened container would fail firstOk',
    FAILURE_CASE_DETECTED: 'unaccounted declared files at a budget stop', TEST_RESULT: (r.exitCode === 0 && unopenedOk && firstOk) ? 'PASS' : 'FAIL',
  });
}

// ---------- 6-9. DA2 (identity observer over every phase) ----------
const MARK_CREATION = '  budget.trackTotalHeld(found.length);';
const MARK_FORWARD = '        allRows.push(c);';
const MARK_SERIALIZATION = "  writeCsvRows(path.join(root, 'placement_candidates.csv'), rows, cols, csvRowCells);";
const INJ_CREATION = `\n  { const obs = { stage: 'creation', distinctFound: new Set(found).size, externalRows: (globalThis.__auditRows ?? new Set()).size, combinedLiveDistinct: new Set([...found, ...(globalThis.__auditRows ?? [])]).size, trackedPeak: budget.peakRetained, limit: budget.limits.retainedCandidates }; (globalThis.__auditPhases ??= []).push(obs); }`;
const INJ_FORWARD = `\n        { (globalThis.__auditRows ??= new Set()).add(c); const obs = { stage: 'forward', rankObjects: new Set(data.candidates).size, allRowsObjects: new Set(allRows).size, combinedLiveDistinct: new Set([...data.candidates, ...allRows]).size, trackedPeak: budget.peakRetained, limit: budget.limits.retainedCandidates }; (globalThis.__auditPhases ??= []).push(obs); }`;
const INJ_SERIALIZATION = `  { const __cells = r => { (globalThis.__auditSer ??= new Set()).add(r); return csvRowCells(r); }; writeCsvRows(path.join(root, 'placement_candidates.csv'), rows, cols, __cells); const obs = { stage: 'serialization', liveRows: new Set(rows).size, serializedIdentities: (globalThis.__auditSer ?? new Set()).size, combinedLiveDistinct: new Set([...rows, ...(globalThis.__auditSer ?? [])]).size, allSerializedAreLiveRows: [...(globalThis.__auditSer ?? [])].every(o => new Set(rows).has(o)), trackedPeak: budget.peakRetained, limit: budget.limits.retainedCandidates }; (globalThis.__auditPhases ??= []).push(obs); fs.writeFileSync(path.join(root, 'AUDIT_OBJECT_COPIES.json'), JSON.stringify({ phases: globalThis.__auditPhases ?? [] }, null, 2) + '\\n'); }`;
function buildObserved(mutate = false) {
  const original = fs.readFileSync(STAGE_TOOL, 'utf8');
  let src = original;
  if (mutate) {
    const mutantLine = '        allRows.push({ ...c });';
    if (src.split(MARK_FORWARD).length !== 2) throw Error('forward marker not unique');
    src = src.replace(MARK_FORWARD, mutantLine);
    if (src.split(mutantLine).length !== 2) throw Error('mutant marker not unique');
    src = src.replace(mutantLine, mutantLine + INJ_FORWARD);
  } else {
    if (src.split(MARK_FORWARD).length !== 2) throw Error('forward marker not unique');
    src = src.replace(MARK_FORWARD, MARK_FORWARD + INJ_FORWARD);
  }
  if (src.split(MARK_CREATION).length !== 2) throw Error('creation marker not unique');
  src = src.replace(MARK_CREATION, MARK_CREATION + INJ_CREATION);
  if (src.split(MARK_SERIALIZATION).length !== 2) throw Error('serialization marker not unique');
  src = src.replace(MARK_SERIALIZATION, INJ_SERIALIZATION);
  return { originalSha256: sha(Buffer.from(original)), observedSha256: sha(Buffer.from(src)), source: src, mutation: mutate ? 'forced extra copy at forward (allRows.push({...c}))' : 'none (read-only hooks)' };
}
function observedCli(tag, nInputs, args, mutate = false) {
  const obs = buildObserved(mutate);
  const obsTool = path.join(RUNROOT, 'staging', 'post_cli', tag, 'observed_tool.mjs');
  fs.mkdirSync(path.dirname(obsTool), { recursive: true }); fs.writeFileSync(obsTool, obs.source);
  const dir = path.join(RUNROOT, 'staging', 'post_cli', tag); fs.mkdirSync(dir, { recursive: true });
  const raws = []; for (let i = 0; i < nInputs; i++) { const f = path.join(dir, `raw_${i}.vfs`); fs.writeFileSync(f, FX.records80()); raws.push(f); }
  const un = cli(tag + '_un', raws, args);
  const ob = cli(tag + '_ob', raws, args, obsTool);
  const four = ['placement_candidates.csv', 'candidates_top.json', 'sources.json', 'scan_skips.csv'];
  const byteIdentical = Object.fromEntries(four.map(f => [f, fs.readFileSync(path.join(un.out, f)).equals(fs.readFileSync(path.join(ob.out, f)))]));
  const phases = JSON.parse(fs.readFileSync(path.join(ob.out, 'AUDIT_OBJECT_COPIES.json'), 'utf8')).phases;
  return { obs, un, ob, byteIdentical, phases };
}
{
  // DA2_CAP4
  const { obs, un, ob, byteIdentical, phases } = observedCli('da2_cap4', 2, ['--budget-retained-candidates', '4']);
  const cap = 4;
  const perPhaseMax = Object.fromEntries(['creation', 'forward', 'serialization'].map(st => [st, Math.max(...phases.filter(p => p.stage === st).map(p => p.combinedLiveDistinct))]));
  const allWithinCap = phases.every(p => p.combinedLiveDistinct <= cap);
  const ser = phases.filter(p => p.stage === 'serialization')[0];
  fieldCase('DA2_CAP4', {
    CODE_IDENTITY: { toolSha256: obs.originalSha256, observedToolSha256: obs.observedSha256, mutation: obs.mutation },
    FIXTURE_IDENTITY: { inputs: 2, fixture: 'records80 x2 (synthetic)', threshold: 4 },
    MEASURED_QUANTITY: 'distinct live candidate-record OBJECTS per phase (Set identity over the actual holding collections)',
    EXPECTED: { perPhaseDistinct: '<= 4', serializationIdentitiesAreLiveRows: true, outputsByteIdentical: true, budgetsIdentical: true, honestExhaustion: 'PARTIAL coverage with candidates retained' },
    ACTUAL: { perPhaseMax, allWithinCap, phasesCount: phases.length, serialization: ser, byteIdentical, budgetsIdentical: JSON.stringify(un.summary.budgets) === JSON.stringify(ob.summary.budgets), coverage: un.summary.budgets.coverage, candidates: un.summary.candidateCount, trackedPeak: un.summary.budgets.used.peakRetainedCandidates },
    PRE_REFERENCE_ON_BASE: { tracker: 4, forwardDistinct: 8, serializationDistinct: 8 },
    DENOMINATOR: cap, UNIT: 'distinct live records vs cap', SOURCE_OF_TRUTH: 'Set-of-identities observer over found/data.candidates+allRows/rows+serialized identities (the production tracker is recorded, not used as oracle)',
    WHY_NON_CIRCULAR: 'the independent Set-identity observer measures the actual holding collections — not the production tracker it audits',
    NEGATIVE_CONTROL: 'the same observer detects the forced-copy mutant (DA2_MUTANT_COPY) and counts aliasing once',
    FAILURE_CASE_DETECTED: 'distinct-record cap bypass (R2-2 P2)', TEST_RESULT: (allWithinCap && ser.allSerializedAreLiveRows && Object.values(byteIdentical).every(Boolean) && JSON.stringify(un.summary.budgets) === JSON.stringify(ob.summary.budgets) && un.summary.budgets.coverage === 'PARTIAL' && un.summary.candidateCount > 0) ? 'PASS' : 'FAIL',
  });
  // DA2_CAP256
  const r256 = observedCli('da2_cap256', 9, []);
  const cap256 = 256;
  const within256 = r256.phases.every(p => p.combinedLiveDistinct <= cap256);
  const ser256 = r256.phases.filter(p => p.stage === 'serialization')[0];
  fieldCase('DA2_CAP256', {
    CODE_IDENTITY: { toolSha256: r256.obs.originalSha256, observedToolSha256: r256.obs.observedSha256, mutation: r256.obs.mutation },
    FIXTURE_IDENTITY: { inputs: 9, fixture: 'records80 x9 (synthetic)', threshold: 256 },
    MEASURED_QUANTITY: 'distinct live candidate-record OBJECTS per phase at the canonical ceiling',
    EXPECTED: { perPhaseDistinct: '<= 256', serializationIdentitiesAreLiveRows: true, outputsByteIdentical: true },
    ACTUAL: { perPhaseMax: Object.fromEntries(['creation', 'forward', 'serialization'].map(st => [st, Math.max(...r256.phases.filter(p => p.stage === st).map(p => p.combinedLiveDistinct))])), allWithinCap: within256, serialization: ser256, byteIdentical: r256.byteIdentical, candidates: r256.un.summary.candidateCount },
    PRE_REFERENCE_ON_BASE: { tracker: 256, forwardDistinct: 280, serializationDistinct: 512 },
    DENOMINATOR: cap256, UNIT: 'distinct live records vs cap', SOURCE_OF_TRUTH: 'same Set-identity observer',
    WHY_NON_CIRCULAR: 'the observer is injected read-only into a byte-verified staged copy and its outputs are byte-compared against the unmodified CLI at the same configuration',
    NEGATIVE_CONTROL: 'aliasing positive: the same object in data.candidates and allRows counts once (forward distinct == live rows, not 2x)',
    FAILURE_CASE_DETECTED: 'cap bypass at the canonical ceiling', TEST_RESULT: (within256 && ser256.allSerializedAreLiveRows && Object.values(r256.byteIdentical).every(Boolean)) ? 'PASS' : 'FAIL',
  });
  // DA2_MUTANT_COPY (negative control)
  const rm = observedCli('da2_mutant', 2, ['--budget-retained-candidates', '4'], true);
  const fwds = rm.phases.filter(p => p.stage === 'forward');
  const maxMutantFwd = Math.max(...fwds.map(p => p.combinedLiveDistinct));
  fieldCase('DA2_MUTANT_COPY', {
    CODE_IDENTITY: { toolSha256: rm.obs.originalSha256, mutantToolSha256: rm.obs.observedSha256, mutation: rm.obs.mutation },
    FIXTURE_IDENTITY: { inputs: 2, fixture: 'records80 x2 (synthetic)', threshold: 4 },
    MEASURED_QUANTITY: 'forward distinct live records on the forced-copy mutant',
    EXPECTED: { forwardDistinct: '> 4 (DETECTED)', trackedPeakWouldStaySmall: true },
    ACTUAL: { maxForwardDistinct: maxMutantFwd, detected: maxMutantFwd > 4, trackedPeaks: fwds.map(p => p.trackedPeak) },
    DENOMINATOR: 4, UNIT: 'distinct live records vs cap', SOURCE_OF_TRUTH: 'Set-identity observer (independent of the production tracker, which stays <=4 and would hide the mutant)',
    WHY_NON_CIRCULAR: 'the mutant is a forced {...c} copy — only an identity-based observer can distinguish an alias from a copy; counts alone cannot',
    NEGATIVE_CONTROL: 'this case IS the negative control; expected result CONTROL_PASS means the observer detects the forced copy',
    FAILURE_CASE_DETECTED: 'a reintroduced copy regression is detected', TEST_RESULT: (maxMutantFwd > 4) ? 'CONTROL_PASS' : 'FAIL',
  });
  // DA2_SMALL_FIXTURE
  const dir = path.join(RUNROOT, 'staging', 'post_fixtures', 'da2_small'); fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'small.vfs'), FX.recordsTwoIdSmall());
  const rs = cli('da2_small', [path.join(dir, 'small.vfs')], []);
  fieldCase('DA2_SMALL_FIXTURE', {
    CODE_IDENTITY: codeIdentity, FIXTURE_IDENTITY: { smallVfs: shaF(path.join(dir, 'small.vfs')), size: 272 },
    MEASURED_QUANTITY: 'candidateCount and coverage of a normal small valid fixture',
    EXPECTED: { candidateCount: '> 0', coverage: 'FULL' }, ACTUAL: { candidateCount: rs.summary.candidateCount, coverage: rs.summary.budgets.coverage },
    DENOMINATOR: 'NOT_APPLICABLE', UNIT: 'candidates', SOURCE_OF_TRUTH: 'SUMMARY.json',
    WHY_NON_CIRCULAR: 'the small fixture is generated by the pinned fixture builder and its result is read from the scanner\u2019s own summary',
    NEGATIVE_CONTROL: 'an empty-result regression would show candidateCount=0',
    FAILURE_CASE_DETECTED: 'over-aggressive cap enforcement deleting valid results', TEST_RESULT: (rs.exitCode === 0 && rs.summary.candidateCount > 0 && rs.summary.budgets.coverage === 'FULL') ? 'PASS' : 'FAIL',
  });
  // DA2_TWO_SOURCE (DA2-COV/P3: cap32 29+3 two-contributing-source regression through the actual scan)
  const ts = measureTwoSource({ toolPath: STAGE_TOOL, worktreeRoot: STAGE, dir: path.join(RUNROOT, 'staging', 'post_fixtures', 'da2_two_source') });
  const [c1, c2] = ts.perSource.contributions;
  const peaksWithinCap = ts.peaks.creation <= TWO_SOURCE_TARGETS.PEAK_DISTINCT_CREATION_MAX && ts.peaks.forward <= TWO_SOURCE_TARGETS.PEAK_DISTINCT_FORWARD_MAX && ts.peaks.serialization <= TWO_SOURCE_TARGETS.PEAK_DISTINCT_SERIALIZATION_MAX;
  const totalsOk = ts.totals.candidateCount === TWO_SOURCE_TARGETS.TOTAL_CANDIDATE_ROWS && ts.totals.trackedPeak === TWO_SOURCE_TARGETS.RETAINED_CAP;
  const contributionsOk = c1?.rows === TWO_SOURCE_TARGETS.SOURCE_1_CONTRIBUTION && c2?.rows === TWO_SOURCE_TARGETS.SOURCE_2_CONTRIBUTION;
  const provenanceOk = ts.totals.bothInputsOpened && ts.totals.twoSourcesContributing
    && Object.values(ts.totals.forwardContributionsPerInput).length === 2
    && Object.entries(ts.totals.forwardContributionsPerInput).every(([, n]) => n > 0)
    && ts.totals.forwardContributionsPerInput[c1?.path] === TWO_SOURCE_TARGETS.SOURCE_1_CONTRIBUTION
    && ts.totals.forwardContributionsPerInput[c2?.path] === TWO_SOURCE_TARGETS.SOURCE_2_CONTRIBUTION
    && ts.totals.serialization?.allSerializedAreLiveRows === true;
  fieldCase('DA2_TWO_SOURCE', {
    CODE_IDENTITY: { ordinaryToolSha256: ts.tool.ordinaryToolSha256, observedToolSha256: ts.tool.observedToolSha256, helperIdentity: ts.tool.helperIdentity, mutation: ts.tool.mutation },
    FIXTURE_IDENTITY: { inputs: 2, fixture: 'records80 x2 (synthetic)', threshold: 32, externallyMeasuredCase: 'Desktop post-audit cap32 control: 32/32/32 with contributions 29+3' },
    MEASURED_QUANTITY: 'per-source candidate contributions, total retained rows, per-phase distinct-live peaks (WeakMap scalar-identity observer), byte-identity of ordinary vs instrumented outputs, both inputs opened and contributing',
    EXPECTED: { RETAINED_CAP: 32, SOURCE_1_CONTRIBUTION: 29, SOURCE_2_CONTRIBUTION: 3, TOTAL_CANDIDATE_ROWS: 32, peaks: '<= 32 per phase', bothInputsOpened: true, outputsByteIdentical: true, budgetsIdentical: true },
    ACTUAL: { contributions: ts.perSource.contributions, sourcesParseStatus: ts.perSource.sourcesParseStatus, totalCandidateRows: ts.totals.candidateCount, trackedPeak: ts.totals.trackedPeak, coverage: ts.totals.coverage, exhausted: ts.totals.exhausted, peaks: ts.peaks, serialization: ts.totals.serialization, forwardContributionsPerInput: ts.totals.forwardContributionsPerInput, byteIdentical: ts.byteIdentical, budgetsIdentical: ts.budgetsIdentical, bothInputsOpened: ts.totals.bothInputsOpened },
    DENOMINATOR: 32, UNIT: 'retained candidate rows vs cap', SOURCE_OF_TRUTH: 'actual scan outputs (placement_candidates.csv per-input rows, sources.json parse status) + the WeakMap scalar-identity observer over creation/forward/serialization',
    WHY_NON_CIRCULAR: 'the 29+3 split is generated by the scanner\u2019s own retention loop over two real synthetic inputs — never fabricated; the observer stores only scalar ids (WeakMap) and the production tracker is recorded, not the oracle',
    NEGATIVE_CONTROL: 'negative protection against a missing second contribution: source 2 must contribute exactly 3 rows (a never-opened or zero-contribution second input FAILS); a forced-copy regression would exceed the peak cap',
    FAILURE_CASE_DETECTED: 'aggregation control that never opens/consumes the second declared input (DA2-COV P3)', TEST_RESULT: (contributionsOk && totalsOk && provenanceOk && peaksWithinCap && Object.values(ts.byteIdentical).every(Boolean) && ts.budgetsIdentical) ? 'PASS' : 'FAIL',
  });
  // write the full phase observations for the evidence package
  fs.writeFileSync(path.join(OUT, 'OBJECT_IDENTITY_OBSERVATIONS.json'), JSON.stringify({
    runId: 'PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011', timeUtc: time(), node,
    method: 'Set-of-object-identities over the actual holding collections (cap4/cap256/mutant: BASE observer pattern) + WeakMap scalar-identity observer for DA2_TWO_SOURCE (no candidate objects retained as audit roots); same object in two arrays counts once; new objects with equal fields count separately; no GC-based proof',
    instrumentation: { markers: { creation: MARK_CREATION, forward: MARK_FORWARD, serialization: MARK_SERIALIZATION }, injectionsReadOnly: true, predicatesChanged: false },
    cap4: { phases: phases, perPhaseMax: Object.fromEntries(['creation', 'forward', 'serialization'].map(st => [st, Math.max(...phases.filter(p => p.stage === st).map(p => p.combinedLiveDistinct))])), outputsByteIdentical: byteIdentical },
    cap256: { phases: r256.phases, perPhaseMax: Object.fromEntries(['creation', 'forward', 'serialization'].map(st => [st, Math.max(...r256.phases.filter(p => p.stage === st).map(p => p.combinedLiveDistinct))])), outputsByteIdentical: r256.byteIdentical },
    forcedCopyMutant: { phases: rm.phases, maxForwardDistinct: maxMutantFwd, detected: maxMutantFwd > 4 },
    twoSource: { phases: ts.phases, contributions: ts.perSource.contributions, peaks: ts.peaks, observerIdentity: ts.tool },
    preReferenceOnBASE: { cap4: { tracker: 4, forwardDistinct: 8, serializationDistinct: 8 }, cap256: { tracker: 256, forwardDistinct: 280, serializationDistinct: 512 } },
  }, null, 2) + '\n');
}

// ---------- 10-11. DA3 ----------
{
  const refusals = [];
  const attempt = (label, fn) => { let threw = false, message = null; try { fn(); } catch (e) { threw = true; message = String(e?.message || e).slice(0, 160); } refusals.push({ label, refused: threw, invalidLabel: /INVALID_CONFIGURATION/.test(message ?? ''), message }); return threw; };
  const buf = FX.layoutBuffer10007();
  attempt('Budget{layoutEvaluations:100001}', () => new Budget({ layoutEvaluations: 100001 }));
  attempt('Budget{layoutEvaluations:NaN}', () => new Budget({ layoutEvaluations: NaN }));
  attempt('Budget{layoutEvaluations:Infinity}', () => new Budget({ layoutEvaluations: Infinity }));
  attempt('Budget{layoutEvaluations:-1}', () => new Budget({ layoutEvaluations: -1 }));
  attempt('Budget{layoutEvaluations:1.5}', () => new Budget({ layoutEvaluations: 1.5 }));
  attempt('Budget{retainedCandidates:512}', () => new Budget({ retainedCandidates: 512 }));
  attempt('Budget{syntheticInputs:33}', () => new Budget({ syntheticInputs: 33 }));
  attempt('Budget{syntheticInputs:NaN}', () => new Budget({ syntheticInputs: NaN }));
  attempt('Budget{scannedBytes:67108865}', () => new Budget({ scannedBytes: 67108865 }));
  attempt('Budget{scannedBytes:NaN}', () => new Budget({ scannedBytes: NaN }));
  attempt('Budget{fullCensusRows:50001}', () => new Budget({ fullCensusRows: 50001 }));
  attempt('Budget{fullCensusRows:NaN}', () => new Budget({ fullCensusRows: NaN }));
  attempt('analyzeBlob+Budget{layoutEvaluations:100001}', () => analyzeBlob(buf, sets, { maxHeader: 0, budget: new Budget({ layoutEvaluations: 100001 }) }));
  attempt('analyzeBlob+Budget{layoutEvaluations:NaN}', () => analyzeBlob(buf, sets, { maxHeader: 0, budget: new Budget({ layoutEvaluations: NaN }) }));
  attempt('analyzeBlob+Budget{retainedCandidates:512}', () => analyzeBlob(buf, sets, { maxHeader: 0, budget: new Budget({ retainedCandidates: 512 }) }));
  attempt('contradictory valid Budget(500)+thresholds{100}', () => analyzeBlob(FX.records80(), sets, { maxHeader: 16, maxStride: 32, budget: new Budget({ layoutEvaluations: 500 }), budgetThresholds: { layoutEvaluations: 100 } }));
  const mutated = new Budget(); mutated.limits = { ...BUDGET_CEILINGS, layoutEvaluations: 999999 };
  attempt('mutated instance limits at use time', () => analyzeBlob(FX.records80(), sets, { maxHeader: 16, maxStride: 32, budget: mutated }));
  const masqueradeAccepted = analyzeBlob(FX.records80(), sets, { maxHeader: 16, maxStride: 32, budget: { limits: { ...BUDGET_CEILINGS, layoutEvaluations: 999999 }, layoutAttempts: 0 } });
  const masqueradeIgnored = masqueradeAccepted.budget.limits.layoutEvaluations === BUDGET_CEILINGS.layoutEvaluations && masqueradeAccepted.candidates.length > 0;
  const cliRefusals = [];
  const cliDir = path.join(RUNROOT, 'staging', 'post_cli', 'da3'); fs.mkdirSync(cliDir, { recursive: true });
  fs.writeFileSync(path.join(cliDir, 'a.vfs'), FX.records80());
  for (const args of [['--budget-layout-evals', '100001'], ['--budget-layout-evals', 'nan'], ['--budget-retained-candidates', '512'], ['--budget-max-inputs', '33'], ['--budget-census-rows', '50001'], ['--budget-scanned-bytes', '67108865']]) {
    const out = path.join(cliDir, 'out_' + args[1]);
    const res = spawnSync(process.execPath, [STAGE_TOOL, '--repo', STAGE, '--ids', path.join(cliDir, 'ids.json'), '--out', out, '--input', path.join(cliDir, 'a.vfs'), ...args], { encoding: 'utf8', timeout: 60000 });
    cliRefusals.push({ args, exitCode: res.status, invalidLabel: /INVALID_CONFIGURATION/.test(res.stderr), scanStartedNo: /SCAN_STARTED=NO/.test(res.stderr), noOutDir: !fs.existsSync(out) });
  }
  const allRefused = refusals.every(r => r.refused && r.invalidLabel) && cliRefusals.every(r => r.exitCode !== 0 && r.invalidLabel && r.scanStartedNo && r.noOutDir);
  const attemptsAfterRefusal = mutated.layoutAttempts === 0;
  fieldCase('DA3_REFUSALS', {
    CODE_IDENTITY: codeIdentity, FIXTURE_IDENTITY: { layoutBuffer10007: sha(buf), records80: shaF(path.join(cliDir, 'a.vfs')) },
    MEASURED_QUANTITY: 'refusal of every invalid effective-budget configuration (constructor, injected instance, mutated instance, contradictory thresholds, CLI flags)',
    EXPECTED: { allRefused: true, invalidBeforeAnalysisStart: true, cli: 'exit!=0 + SCAN_STARTED=NO + no output dir', noNullLimitLeak: 'NaN throws; no result with limits.layoutEvaluations=null', masqueradeSuppliesNothing: true },
    ACTUAL: { refusals, cliRefusals, attemptsAfterRefusal, masqueradeIgnored },
    DENOMINATOR: refusals.length + cliRefusals.length, UNIT: 'refusal attempts', SOURCE_OF_TRUTH: 'Budget constructor + effective-tracker validation in analyzeBlob + CLI flag validation',
    WHY_NON_CIRCULAR: 'refusals are attempted through the exported analyzeBlob/Budget surfaces the production CLI itself uses — not a re-implementation of the checks',
    NEGATIVE_CONTROL: 'legal minimum/exact ceilings/defaults/lowered limits are ACCEPTED (see DA3_POSITIVES)',
    FAILURE_CASE_DETECTED: 'configuration bypass via an injected Budget instance (the DA-3 P2)',
    TEST_RESULT: (allRefused && attemptsAfterRefusal && masqueradeIgnored) ? 'PASS' : 'FAIL',
  });
  // DA3_POSITIVES
  const def = new Budget();
  const min = new Budget({ layoutEvaluations: 1 });
  const ceil = new Budget({ syntheticInputs: 32, scannedBytes: 67108864, layoutEvaluations: 100000, fullCensusRows: 50000, retainedCandidates: 256 });
  const lower = analyzeBlob(buf, sets, { maxHeader: 0, maxStride: 512, budgetThresholds: { layoutEvaluations: 60 } });
  const shared = new Budget();
  const s1 = analyzeBlob(FX.records80(), sets, { maxHeader: 0, maxStride: 512, budget: shared, top: 10 });
  const s2 = analyzeBlob(FX.records80(), sets, { maxHeader: 0, maxStride: 512, budget: shared, top: 10 });
  const counter61 = { limit: 60, layoutAttempts: lower.stats.layoutAttempts, layoutRefusals: lower.stats.layoutRefusals, executedEvaluations: lower.stats.layoutAttempts - lower.stats.layoutRefusals, admitted: lower.stats.layoutsAdmitted, refusalDetail: lower.budget.refusals[lower.budget.refusals.length - 1]?.detail };
  const sharedOk = shared.layoutAttempts === s2.stats.layoutAttempts && s2.stats.layoutAttempts === 2 * s1.stats.layoutAttempts && s1.stats.layoutAttempts === 126;
  fieldCase('DA3_POSITIVES', {
    CODE_IDENTITY: codeIdentity, FIXTURE_IDENTITY: { layoutBuffer10007: sha(buf), records80: sha(FX.records80()) },
    MEASURED_QUANTITY: 'acceptance of legal configurations; request/refusal counter semantics; shared-instance aggregation',
    EXPECTED: { defaults: '== canonical ceilings', minimum1: true, exactCeilings: true, limit60: 'attempts 61 = 60 executed + 1 refused (never described as 61 performed evaluations)', sharedBudgetTwoInputsNoReset: true },
    ACTUAL: { defaults: def.limits, minimum1: min.limits.layoutEvaluations === 1, exactCeilings: JSON.stringify({ ...ceil.limits }) === JSON.stringify({ ...BUDGET_CEILINGS }), limit60: counter61, shared: { firstAttempts: s1.stats.layoutAttempts, secondAttempts: s2.stats.layoutAttempts, sharedInstanceAttempts: shared.layoutAttempts, sameInstanceAggregated: sharedOk } },
    DENOMINATOR: 'NOT_APPLICABLE', UNIT: 'configurations', SOURCE_OF_TRUTH: 'Budget counters',
    WHY_NON_CIRCULAR: 'the 61-request record is cross-checked against layoutRefusals and the refusal detail naming the 60 executed evaluations — the counter cannot be re-described post hoc',
    NEGATIVE_CONTROL: 'the refusal record must name the executed evaluations count (60), proving the 61 is not 61 performed layouts',
    FAILURE_CASE_DETECTED: 'over-rejection of legal budgets or misdescribed counters', TEST_RESULT: (JSON.stringify({ ...def.limits }) === JSON.stringify({ ...BUDGET_CEILINGS }) && min.limits.layoutEvaluations === 1 && JSON.stringify({ ...ceil.limits }) === JSON.stringify({ ...BUDGET_CEILINGS }) && counter61.layoutAttempts === 61 && counter61.layoutRefusals === 1 && counter61.executedEvaluations === 60 && sharedOk) ? 'PASS' : 'FAIL',
  });
}

// ---------- 12. PA1 ----------
{
  const pins = FX.PA1_PINS;
  const results = {};
  const sampled = new Set(); for (let j = 0; j < 1200; j++) sampled.add(Math.floor((j + 0.5) * 4800 / 1200));
  function truth(b) {
    let finiteTriples = 0, idHits = 0, sampleFinite = 0;
    for (let i = 0; i < 4800; i++) {
      const fin = [4, 8, 12].every(o => Number.isFinite(b.readFloatLE(16 + i * 32 + o)));
      if (fin) finiteTriples++;
      if (sampled.has(i) && fin) sampleFinite++;
      const id = b.readUInt16LE(16 + i * 32);
      if (id === 4057 || id === 4058) idHits++;
    }
    return { FULL_XYZ_FINITE_RATE: finiteTriples / 4800, SAMPLE_XYZ_FINITE_RATE: sampleFinite / 1200, FULL_ID_HIT_RATE: idHits / 4800 };
  }
  const bufA = FX.pa1A(), bufB = FX.pa1B(), bufC = FX.pa1C();
  const prod = {};
  for (const [k, b] of [['A', bufA], ['B', bufB], ['C', bufC]]) {
    const bytes = { sizeBytes: b.length, sha256: sha(b).toUpperCase() };
    const t = truth(b);
    const r = analyzeBlob(b, sets, { maxStride: 32, maxHeader: 16, top: 10, budgetThresholds: { fullCensusRows: 4800 } });
    const c = r.candidates.find(x => x.header === 16 && x.stride === 32 && x.idOffset === 0 && x.idWidth === 2 && x.xyzOffset === 4);
    prod[k] = {
      bytes, pinMatch: bytes.sizeBytes === pins[k].sizeBytes && bytes.sha256 === pins[k].sha256,
      independentTruth: t, production: c ? { targetFound: true, sampleRows: c.sampleCount, sampleXyzFiniteRate: c.sampleXyzFiniteRate, censusStatus: c.censusStatus, fullRows: c.fullCensusRowCount, fullXyzFiniteRate: c.fullCensusXyzFiniteRate, fullIdRate: c.fullCensusIdRate } : { targetFound: false },
      equalsTruth: c ? (c.fullCensusXyzFiniteRate === t.FULL_XYZ_FINITE_RATE && c.fullCensusIdRate === t.FULL_ID_HIT_RATE && c.sampleXyzFiniteRate === t.SAMPLE_XYZ_FINITE_RATE) : false,
    };
  }
  const noBudget = analyzeBlob(bufA, sets, { maxStride: 32, maxHeader: 16, top: 10, budgetThresholds: { fullCensusRows: 100 } });
  const nc = noBudget.candidates.find(x => x.header === 16 && x.stride === 32 && x.xyzOffset === 4);
  // harness mutant gate (field names as measured on the production record)
  const gate = (name, obs) => { const p = pins[name]; return obs.sampleXyzFiniteRate === p.SAMPLE_XYZ_FINITE_RATE && obs.fullXyzFiniteRate === p.FULL_XYZ_FINITE_RATE && obs.fullIdRate === p.FULL_ID_HIT_RATE; };
  const mutantRejected = !gate('A', { sampleXyzFiniteRate: 1.0, fullXyzFiniteRate: 1.0, fullIdRate: 0.25 }) && !gate('B', { sampleXyzFiniteRate: 1.0, fullXyzFiniteRate: 1.0, fullIdRate: 1.0 });
  const genuineAccepted = prod.A.production.targetFound && gate('A', prod.A.production) && gate('B', prod.B.production) && gate('C', prod.C.production);
  const deltaOk = prod.A.production.fullIdRate === 0.25 && prod.B.production.fullIdRate === 1.0 && prod.A.production.fullXyzFiniteRate === prod.B.production.fullXyzFiniteRate && prod.B.production.fullXyzFiniteRate === 0.25 && prod.C.production.fullXyzFiniteRate === 1.0 && prod.B.production.fullIdRate === prod.C.production.fullIdRate;
  results.fixtures = prod;
  fieldCase('PA1_REGRESSION', {
    CODE_IDENTITY: codeIdentity, FIXTURE_IDENTITY: { A: pins.A, B: pins.B, C: pins.C, measured: { A: prod.A.bytes, B: prod.B.bytes, C: prod.C.bytes } },
    MEASURED_QUANTITY: 'sample/full XYZ and ID rates vs independently computed ground truth; censusStatus under the legal 4800 budget and under a no-budget control; harness mutant gate verdicts',
    EXPECTED: { A: 'sample 1.0, full XYZ 0.25, full ID 0.25, FULL_CENSUS 4800', B: 'sample 1.0, full XYZ 0.25, full ID 1.0', C: 'sample 1.0, full XYZ 1.0, full ID 1.0', deltaDiscipline: true, noBudgetControl: 'PARTIAL_BUDGET_EXHAUSTED', mutantRejectedForAB: true },
    ACTUAL: { prod, noBudgetControl: { censusStatus: nc.censusStatus, fullRows: nc.fullCensusRowCount }, mutantGate: { mutantRejected, genuineAccepted }, deltaOk },
    DENOMINATOR: 4800, UNIT: 'table rows', SOURCE_OF_TRUTH: 'ground truth computed by this harness directly from the synthetic bytes (independent of the production reader/sampler); external reference: the pinned Desktop recheck on unchanged BASE',
    WHY_NON_CIRCULAR: 'the ground truth is computed byte-wise by the harness — the production sampler\u2019s rates are compared against it, never against another sampler output',
    NEGATIVE_CONTROL: 'a forged FULL_XYZ=1.0 for A/B (sample kept 1.0) is REJECTED by the harness gate',
    FAILURE_CASE_DETECTED: 'a future regression extrapolating the sample onto the whole table',
    TEST_RESULT: (prod.A.pinMatch && prod.B.pinMatch && prod.C.pinMatch && genuineAccepted && deltaOk && mutantRejected && nc.censusStatus === 'PARTIAL_BUDGET_EXHAUSTED') ? 'PASS' : 'FAIL',
  });
}

// ---------- 13. PA2_RECEIPT_QUALIFICATION (the corrected acceptance condition) ----------
{
  const receiptBytesBefore = fs.readFileSync(RECEIPT);
  const receiptShaBefore = sha(receiptBytesBefore);
  // predicate 1: trusted sources verified BEFORE pin use (BASE gate module + predecessor runner)
  const trusted = await loadTrusted(WORKTREE);
  // predicates 1-7: the corrected validator over the receipt-under-test
  const q = await qualifyReceipt({ receiptPath: RECEIPT, trusted });
  const live = q.INPUT_BYTES_REMEASURED;
  const cons = q.RECEIPT_INTERNAL_CONSISTENCY;
  const modId = q.MODULE_CODE_IDENTITY;
  const qual = q.RECEIPT_QUALIFICATION;
  const receiptShaAfter = sha(fs.readFileSync(RECEIPT));
  // preserved historical counterchecks: the staged runner refuses bad inputs with ZERO downstream calls
  const mutantRuns = [];
  const mDir = path.join(RUNROOT, 'staging', 'post_cli', 'pa2'); fs.mkdirSync(mDir, { recursive: true });
  const mod = trusted.module;
  const overridesSameSize = {}, overridesMissing = {};
  for (const pin of trusted.pins) {
    const bytes = fs.readFileSync(pin.path); bytes[bytes.length - 1] ^= 0x01;
    const f = path.join(mDir, pin.pin + '.bin'); fs.writeFileSync(f, bytes); overridesSameSize[pin.pin] = f;
    overridesMissing[pin.pin] = path.join(mDir, 'missing_' + pin.pin);
  }
  const ovSS = path.join(mDir, 'ov_samesize.json'); fs.writeFileSync(ovSS, JSON.stringify(overridesSameSize));
  const ovMiss = path.join(mDir, 'ov_missing.json'); fs.writeFileSync(ovMiss, JSON.stringify(overridesMissing));
  const bytes0 = fs.readFileSync(trusted.pins[0].path);
  const grown = path.join(mDir, 'grown.bin'); fs.writeFileSync(grown, Buffer.concat([bytes0, Buffer.from([0])]));
  const ovSize = path.join(mDir, 'ov_size.json'); fs.writeFileSync(ovSize, JSON.stringify({ [trusted.pins[0].pin]: grown }));
  const runRunner = (ovFile, tag) => {
    const receipt = path.join(mDir, tag + '_receipt.json');
    const args = ovFile ? ['--overrides-json', ovFile, '--receipt', receipt] : ['--receipt', receipt];
    const res = spawnSync(process.execPath, [STAGE_RUNNER, ...args], { encoding: 'utf8', timeout: 180000 });
    let rc = null; try { rc = JSON.parse(fs.readFileSync(receipt, 'utf8')); } catch {}
    return { exitCode: res.status, receipt: rc, stderr: res.stderr, stdout: res.stdout };
  };
  const ss = runRunner(ovSS, 'samesize');
  const miss = runRunner(ovMiss, 'missing');
  const size = runRunner(ovSize, 'wrongsize');
  mutantRuns.push({ mutant: 'all pins -> same-size-wrong-sha private copies', exitCode: ss.exitCode, verdict: ss.receipt?.gate?.verdict, blockedCount: ss.receipt?.gate?.blockedCount, downstreamCalls: ss.receipt?.downstreamCallsAfterGate, expectedPinsUnchanged: true, realGithubWrite: false },
    { mutant: 'all pins -> missing private paths', exitCode: miss.exitCode, verdict: miss.receipt?.gate?.verdict, blockedCount: miss.receipt?.gate?.blockedCount, downstreamCalls: miss.receipt?.downstreamCallsAfterGate, expectedPinsUnchanged: true, realGithubWrite: false },
    { mutant: 'one pin -> wrong-size private copy', exitCode: size.exitCode, verdict: size.receipt?.gate?.verdict, blockedCount: size.receipt?.gate?.blockedCount, blockedCompare: size.receipt?.gate?.blockedPins?.map(b => b.compareResult), downstreamCalls: size.receipt?.downstreamCallsAfterGate, expectedPinsUnchanged: true, realGithubWrite: false });
  const mutantsOk = mutantRuns.every(m => m.exitCode === 3 && m.verdict === 'BLOCKED_INPUT_IDENTITY' && Object.values(m.downstreamCalls).every(v => v === 0));
  const fourQuantitiesOk = (live?.pass === true) && (cons?.ok === true) && (modId?.ok === true) && (qual?.verdict === 'PASS');
  fieldCase('PA2_RECEIPT_QUALIFICATION', {
    CODE_IDENTITY: { validator: codeIdentity.receiptValidator, gateModule: { path: TRUSTED_GATE_MODULE.path, trustedSha256: TRUSTED_GATE_MODULE.sha256, measuredSha256: trusted.moduleShas?.gateModule }, runner: { path: TRUSTED_RUNNER.path, trustedSha256: TRUSTED_RUNNER.sha256, measuredSha256: trusted.moduleShas?.runner }, stagedRunner: shaF(STAGE_RUNNER) },
    FIXTURE_IDENTITY: { receiptUnderTest: RECEIPT, receiptIdentity: qual?.receiptIdentity ?? { sizeBytes: receiptBytesBefore.length, sha256: receiptShaBefore }, pins: trusted.pins?.length ?? null, schema: trusted.schema ?? null, historicalContext: RECEIPT_PROFILE },
    MEASURED_QUANTITY: 'FOUR SEPARATE QUANTITIES: INPUT_BYTES_REMEASURED (live 16-pin remeasurement), RECEIPT_INTERNAL_CONSISTENCY (per-pin re-derivation + summary recomputation), MODULE_CODE_IDENTITY (paths+SHAs vs trusted sources), RECEIPT_QUALIFICATION (conjunction verdict)',
    EXPECTED: { trustedSourcesVerified: true, profile: 'exact historical runId/stage/mode, 16 distinct pins, strict legacy shape', consistency: 'all receipt claims re-derived and consistent', moduleIdentity: 'paths+SHAs match trusted sources', liveRemeasurement: 'PASS 16/16', receiptQualification: 'PASS', runnerMutants: 'BLOCKED_INPUT_IDENTITY exit 3 with ZERO downstream calls', receiptUntouched: true },
    ACTUAL: {
      trusted: { ok: trusted.ok, reasons: trusted.reasons ?? [], moduleShas: trusted.moduleShas, pinCount: trusted.pins?.length ?? null, schema: trusted.schema ?? null },
      INPUT_BYTES_REMEASURED: live ?? { performed: false },
      RECEIPT_INTERNAL_CONSISTENCY: cons ? { ok: cons.ok, recomputed: cons.recomputed, claimed: cons.claimed, perPinReasons: cons.perPinReasons, summaryMismatches: cons.summaryMismatches, perPinChecks: cons.perPinChecks } : { performed: false },
      MODULE_CODE_IDENTITY: modId ?? { performed: false },
      RECEIPT_QUALIFICATION: qual,
      mutantRuns,
    },
    DENOMINATOR: 16, UNIT: 'pinned inputs / receipt claims', SOURCE_OF_TRUTH: 'frozen trusted pins from the SHA-verified gate module + independently re-derived comparisons + live verifyAllInputs remeasurement',
    WHY_NON_CIRCULAR: 'expected values NEVER come from the tested receipt: pins are frozen in the SHA-verified gate module, module SHAs are frozen constants, compareResult/summary/verdict are recomputed from trusted pins, and the live remeasurement reads the physical evidence files — a receipt-declared value confers nothing',
    NEGATIVE_CONTROL: 'the three staged-runner mutants refuse with exit 3 and zero downstream calls; a contradictory receipt (zeroed measured SHA, zeroed module SHA, forged compareResult, forged summary, missing/duplicate/removed pins) must refuse the WHOLE qualification — proven by the §5 full-POST matrix in the run package',
    FAILURE_CASE_DETECTED: 'the externally measured PA2 false-PASS defect (Desktop M1/M2: a full POST accepting a receipt whose MEASURED.sha256/gateModule.sha256 was zeroed)',
    TEST_RESULT: (trusted.ok === true && fourQuantitiesOk && mutantsOk && receiptShaBefore === receiptShaAfter) ? 'PASS' : 'FAIL',
  });
  fs.writeFileSync(path.join(OUT, 'IDENTITY_GATE_COUNTERCHECKS.json'), JSON.stringify({
    runId: 'PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011', timeUtc: time(), node,
    receiptUnderTest: { path: RECEIPT, identity: qual?.receiptIdentity ?? { sizeBytes: receiptBytesBefore.length, sha256: receiptShaBefore }, untouchedByThisRun: receiptShaBefore === receiptShaAfter },
    qualificationQuantities: q,
    mutantCounterchecks: mutantRuns,
    method: 'validate_receipt.mjs (SHA-recorded): trusted pin verification BEFORE use; strict legacy receipt profile; per-pin re-derivation from trusted pins; summary recomputation; module identity vs trusted source files; live verifyAllInputs remeasurement required to PASS; fail-closed; the PA2 result is a required conjunct of the aggregator',
    supersession: 'the predecessor PA2_LIVE_GATE accepted verdict+matched+mode only — superseded by this corrected acceptance condition (see SUPERSESSION.md)',
  }, null, 2) + '\n');
}

// ---------- 14. AGGREGATOR + qualification ----------
{
  const outcomes = Object.fromEntries(Object.entries(cases).map(([id, c]) => [id, c.TEST_RESULT]));
  const expectations = { ...EXPECTED_OUTCOMES };
  const full = computeQualification(outcomes, expectations);
  // NEGATIVE CONTROL: remove one required result at a time — the aggregator must refuse with exit != 0
  const removals = {};
  for (const id of Object.keys(expectations)) {
    const partial = { ...outcomes }; delete partial[id];
    removals[id] = computeQualification(partial, expectations);
  }
  const removalsRefuse = Object.values(removals).every(q => !q.ok && q.exitCode !== 0);
  fieldCase('AGGREGATOR_CONTROL', {
    CODE_IDENTITY: codeIdentity, FIXTURE_IDENTITY: 'NOT_APPLICABLE', MEASURED_QUANTITY: 'aggregator verdict + exit code over the full result set and over each single-removal set',
    EXPECTED: { fullSet: 'QUALIFICATION_PASS/exit 0 (CLEAN receipt) or QUALIFICATION_REFUSED/exit != 0 (mutant receipts)', eachSingleRemoval: 'QUALIFICATION_REFUSED/exit != 0' },
    ACTUAL: { full, removals, removalsRefuse },
    DENOMINATOR: Object.keys(expectations).length, UNIT: 'required results', SOURCE_OF_TRUTH: 'computeQualification (the ACTUAL shared aggregator) over the measured named outcomes',
    WHY_NON_CIRCULAR: 'the aggregator is the same imported function that computes the final qualification — its refusal behavior is exercised over every single-removal subset of the actual measured outcomes',
    NEGATIVE_CONTROL: 'this case IS the collector self-test; a collector that always exits 0 would fail removalsRefuse',
    FAILURE_CASE_DETECTED: 'a collector that reports PASS with missing required results (the PA2 result is one of the required conjuncts)', TEST_RESULT: (removalsRefuse) ? 'PASS' : 'FAIL',
  });
  const finalQualification = computeQualification({ ...outcomes, AGGREGATOR_CONTROL: cases.AGGREGATOR_CONTROL.TEST_RESULT }, { ...expectations, AGGREGATOR_CONTROL: 'PASS' });
  fs.writeFileSync(path.join(OUT, 'POST_TEST_RESULTS.json'), JSON.stringify({
    runId: 'PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011', stage: 'POST', timeUtc: time(), node,
    executedCommand: EXECUTED_COMMAND,
    supersession: 'canonical POST adapted from docs/audits/PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011/POST/run_post.mjs (SHA 3BBDC404...) — the PA2_LIVE_GATE acceptance condition is superseded by PA2_RECEIPT_QUALIFICATION (see SUPERSESSION.md in the run package)',
    stageInfo: { stageRoot: STAGE, copies: stageCopies, allByteIdentical: true },
    suite: { exitCode: suiteInfo.r.exitCode, tests: suiteInfo.r.tests, pass: suiteInfo.r.pass, fail: suiteInfo.r.fail, requiredPresent: suiteInfo.present, allRequiredPresent: suiteInfo.allPresent },
    base53Replay: { tests: base53.tests, pass: base53.pass, fail: base53.fail, exitCode: base53.exitCode },
    cases, namedOutcomeCount: Object.keys(cases).length,
    counters: { pass: Object.values(cases).filter(c => c.TEST_RESULT === 'PASS').length, controlPass: Object.values(cases).filter(c => c.TEST_RESULT === 'CONTROL_PASS').length, fail: Object.values(cases).filter(c => c.TEST_RESULT === 'FAIL').length },
    finalQualification,
    limitations: ['run_post.mjs is the executor\u2019s own harness; replaying it is not a second implementation of the checks', 'independent anchors: the pinned external Desktop post-audit measurements, the frozen byte pins, the exported censusGate, the identity observers, the PA-1 harness ground truth, and the fresh-context internal QC', 'no game payload was scanned; all inputs are synthetic fixtures', 'hash consistency is not proof of historical execution, authorship, or a signature'],
  }, null, 2) + '\n');
  fs.writeFileSync(path.join(OUT, 'POST_MEASUREMENTS.json'), JSON.stringify({
    runId: 'PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011', tool: 'POST_MEASUREMENTS_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1', timeUtc: time(), node,
    codeIdentity, stageCopies, cases,
    generated: { pass: Object.values(cases).filter(c => c.TEST_RESULT === 'PASS').length, controlPass: Object.values(cases).filter(c => c.TEST_RESULT === 'CONTROL_PASS').length, fail: Object.values(cases).filter(c => c.TEST_RESULT === 'FAIL').length },
    suiteCounts: { tests: suiteInfo.r.tests, pass: suiteInfo.r.pass, fail: suiteInfo.r.fail },
    finalQualification,
  }, null, 2) + '\n');
  console.log(JSON.stringify({ named: Object.keys(cases).length, pass: Object.values(cases).filter(c => c.TEST_RESULT === 'PASS').length, controlPass: Object.values(cases).filter(c => c.TEST_RESULT === 'CONTROL_PASS').length, fail: Object.values(cases).filter(c => c.TEST_RESULT === 'FAIL').length, PA2: cases.PA2_RECEIPT_QUALIFICATION.TEST_RESULT, qualification: finalQualification.verdict }));
  process.exitCode = finalQualification.exitCode;
}
