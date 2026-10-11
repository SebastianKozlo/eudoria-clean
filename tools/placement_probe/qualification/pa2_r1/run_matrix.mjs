// run_matrix.mjs — outer bounded full-POST matrix driver (contract §5)
// (RUN_ID PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011)
//
// This driver is OUTSIDE the canonical POST recursion: the canonical POST
// (run_post.mjs) never invokes this driver, and this driver invokes the canonical
// POST through its documented CLI once per case. It runs the fixed integration
// matrix: CLEAN + M1..M9 (each mutant from a FRESH EXACT CLEAN copy with ONLY the
// listed field changed), the four validator profile unit controls (wrong runId /
// wrong stage / wrong mode / unreadable-truncated JSON receipt; separately counted
// from the ten full-POST cases), and the three ACTUAL aggregator controls (PA2
// result missing / FAIL / NOT_PERFORMED; separate from receipt cases and test
// counts). POST code/pins are frozen for the batch (SHA-recorded before and after);
// any repair invalidates the batch and requires a full rerun.
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { fileURLToPath, pathToFileURL } from 'node:url';
const sha = b => createHash('sha256').update(b).digest('hex');
const shaF = p => sha(fs.readFileSync(p));
const HERE = path.dirname(fileURLToPath(import.meta.url));
const RUN_ROOT = 'D:/Eudoria_Reconstruction/99_Audits/PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011';
const WT = path.join(RUN_ROOT, 'workspace/eudoria-clean');
const KITDIR = path.join(RUN_ROOT, 'stage_kit');
const POSTS = path.join(RUN_ROOT, 'posts'); fs.mkdirSync(POSTS, { recursive: true });
const RECEIPTS = path.join(RUN_ROOT, 'matrix', 'receipts'); fs.mkdirSync(RECEIPTS, { recursive: true });
const CANONICAL_POST = path.join(WT, 'tools/placement_probe/qualification/pa2_r1/run_post.mjs');
const VALIDATOR = path.join(WT, 'tools/placement_probe/qualification/pa2_r1/validate_receipt.mjs');
const CLEAN_RECEIPT = path.join(WT, 'docs/audits/PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011/POST/IDENTITY_GATE_LIVE_RECEIPT.json');
const CLEAN_RECEIPT_FROZEN_SHA = '837030ab901d7e2d3ca72c89d555f0c75d06b4cc04e0a71b1793841d52a1da88';

// ---- freeze the batch: POST code + validator identity (verified again at the end) ----
const frozenCode = {
  run_post_sha256: shaF(CANONICAL_POST),
  validate_receipt_sha256: shaF(VALIDATOR),
  two_source_sha256: shaF(path.join(WT, 'tools/placement_probe/qualification/pa2_r1/two_source.mjs')),
  run_matrix_sha256: shaF(path.join(HERE, 'run_matrix.mjs')),
  gate_module_sha256: shaF(path.join(WT, 'tools/placement_probe/verify_inputs.mjs')),
  clean_receipt_source_sha256: shaF(CLEAN_RECEIPT),
};
if (frozenCode.clean_receipt_source_sha256 !== CLEAN_RECEIPT_FROZEN_SHA) throw Error('CLEAN receipt source does not match the frozen baseline fixture identity');
console.log('frozen batch code identity:', JSON.stringify(frozenCode));

// ---- the fixed matrix cases (contract §5 table) ----
function buildMutant(caseId) {
  const receipt = JSON.parse(fs.readFileSync(CLEAN_RECEIPT, 'utf8')); // fresh exact CLEAN copy each time
  const diff = [];
  switch (caseId) {
    case 'CLEAN': break;
    case 'M1': diff.push({ field: 'perPin[0].MEASURED.sha256', before: receipt.perPin[0].MEASURED.sha256, after: (receipt.perPin[0].MEASURED.sha256 = '0'.repeat(64)) }); break;
    case 'M2': diff.push({ field: 'moduleIdentity.gateModule.sha256', before: receipt.moduleIdentity.gateModule.sha256, after: (receipt.moduleIdentity.gateModule.sha256 = '0'.repeat(64)) }); break;
    case 'M3': diff.push({ field: 'perPin[0].MEASURED.sizeBytes', before: receipt.perPin[0].MEASURED.sizeBytes, after: (receipt.perPin[0].MEASURED.sizeBytes += 1) }); break;
    case 'M4': diff.push({ field: 'perPin[0].compareResult', before: receipt.perPin[0].compareResult, after: (receipt.perPin[0].compareResult = 'SHA_MISMATCH') }); break; // measured bytes still match
    case 'M5': diff.push({ field: 'perPin[last] removed', before: receipt.perPin[receipt.perPin.length - 1].pin, after: 'REMOVED' }); receipt.perPin.pop(); break;
    case 'M6': diff.push({ field: 'perPin duplicate appended', before: receipt.perPin[0].pin + ' x1', after: (receipt.perPin.push(JSON.parse(JSON.stringify(receipt.perPin[0]))), receipt.perPin[0].pin + ' x2') }); break;
    case 'M7': diff.push({ field: 'gate.matched', before: receipt.gate.matched, after: (receipt.gate.matched = 15) }, { field: 'gate.blockedCount', before: receipt.gate.blockedCount, after: (receipt.gate.blockedCount = 1) }); break; // all perPin entries still match
    case 'M8': diff.push({ field: 'moduleIdentity.runner.sha256', before: receipt.moduleIdentity.runner.sha256, after: (receipt.moduleIdentity.runner.sha256 = '0'.repeat(64)) }); break;
    case 'M9': {
      receipt.perPin[0].MEASURED.exists = false; receipt.perPin[0].MEASURED.sizeBytes = null; receipt.perPin[0].MEASURED.sha256 = null; receipt.perPin[0].compareResult = 'MISSING';
      receipt.gate.matched = 15; receipt.gate.blockedCount = 1;
      receipt.gate.blockedPins = [{ pin: receipt.perPin[0].pin, compareResult: 'MISSING', reason: 'input file not found' }];
      // verdict / EFFECTIVE_GATE_RESULT intentionally still claim PASS — the contradiction under test
      diff.push({ field: 'perPin[0].MEASURED.{exists,sizeBytes,sha256}+compareResult', before: 'true/11361/3d1a9ea1.../MATCH', after: 'false/null/null/MISSING' },
        { field: 'gate.{matched,blockedCount,blockedPins}', before: '16/0/[]', after: '15/1/[' + receipt.perPin[0].pin + ']' },
        { field: 'gate.{verdict,EFFECTIVE_GATE_RESULT}', before: receipt.gate.verdict + '/' + receipt.gate.EFFECTIVE_GATE_RESULT, after: 'STILL PASS / STILL GATE_PASS__DOWNSTREAM_AUTHORIZED (contradiction under test)' });
      break;
    }
    default: throw Error('unknown case ' + caseId);
  }
  return { receipt, diff };
}
const MATRIX = [
  { case: 'CLEAN', requiredPA2: 'PASS', requiredOverall: 'QUALIFICATION_PASS', requiredExit: 0 },
  { case: 'M1', requiredPA2: 'FAIL', requiredOverall: 'QUALIFICATION_REFUSED', requiredExit: 'nonzero' },
  { case: 'M2', requiredPA2: 'FAIL', requiredOverall: 'QUALIFICATION_REFUSED', requiredExit: 'nonzero' },
  { case: 'M3', requiredPA2: 'FAIL', requiredOverall: 'QUALIFICATION_REFUSED', requiredExit: 'nonzero' },
  { case: 'M4', requiredPA2: 'FAIL', requiredOverall: 'QUALIFICATION_REFUSED', requiredExit: 'nonzero' },
  { case: 'M5', requiredPA2: 'FAIL', requiredOverall: 'QUALIFICATION_REFUSED', requiredExit: 'nonzero' },
  { case: 'M6', requiredPA2: 'FAIL', requiredOverall: 'QUALIFICATION_REFUSED', requiredExit: 'nonzero' },
  { case: 'M7', requiredPA2: 'FAIL', requiredOverall: 'QUALIFICATION_REFUSED', requiredExit: 'nonzero' },
  { case: 'M8', requiredPA2: 'FAIL', requiredOverall: 'QUALIFICATION_REFUSED', requiredExit: 'nonzero' },
  { case: 'M9', requiredPA2: 'FAIL', requiredOverall: 'QUALIFICATION_REFUSED', requiredExit: 'nonzero' },
];
const fullPostResults = [];
for (const spec of MATRIX) {
  const { receipt, diff } = buildMutant(spec.case);
  const receiptPath = path.join(RECEIPTS, spec.case + '.json');
  fs.writeFileSync(receiptPath, JSON.stringify(receipt, null, 2) + '\n');
  const receiptShaBefore = shaF(receiptPath);
  const caseRoot = path.join(RUN_ROOT, 'matrix', 'case_' + spec.case);
  const outDir = path.join(caseRoot, 'out'); const runroot = path.join(caseRoot, 'runroot');
  const cmd = [process.execPath, CANONICAL_POST, '--worktree', WT, '--runroot', runroot, '--kitdir', KITDIR, '--receipt', receiptPath, '--out', outDir];
  const t0 = Date.now();
  const res = spawnSync(process.execPath, [CANONICAL_POST, '--worktree', WT, '--runroot', runroot, '--kitdir', KITDIR, '--receipt', receiptPath, '--out', outDir], { encoding: 'utf8', timeout: 3600000, maxBuffer: 1 << 28 });
  const wallMs = Date.now() - t0;
  fs.writeFileSync(path.join(caseRoot, 'stdout.txt'), res.stdout ?? '');
  fs.writeFileSync(path.join(caseRoot, 'stderr.txt'), res.stderr ?? '');
  const receiptShaAfter = shaF(receiptPath);
  let post = null; try { post = JSON.parse(fs.readFileSync(path.join(outDir, 'POST_TEST_RESULTS.json'), 'utf8')); } catch (e) { }
  const pa2 = post?.cases?.PA2_RECEIPT_QUALIFICATION ?? null;
  const otherResults = post ? Object.fromEntries(Object.entries(post.cases).filter(([id]) => id !== 'PA2_RECEIPT_QUALIFICATION').map(([id, c]) => [id, c.TEST_RESULT])) : null;
  const expectedOthers = { ORIGINAL_SEVEN: 'PASS', BASE_53_REPLAY: 'PASS', FULL_SUITE: 'PASS', DA1_CENSUS: 'PASS', DA1_NOT_OPENED: 'PASS', DA2_CAP4: 'PASS', DA2_CAP256: 'PASS', DA2_MUTANT_COPY: 'CONTROL_PASS', DA2_SMALL_FIXTURE: 'PASS', DA2_TWO_SOURCE: 'PASS', DA3_REFUSALS: 'PASS', DA3_POSITIVES: 'PASS', PA1_REGRESSION: 'PASS', AGGREGATOR_CONTROL: 'PASS' };
  const othersOk = otherResults && Object.keys(expectedOthers).every(id => otherResults[id] === expectedOthers[id]);
  const exitOk = spec.requiredExit === 0 ? res.status === 0 : (res.status !== 0 && res.status !== null);
  const pa2Ok = pa2?.TEST_RESULT === spec.requiredPA2;
  const overall = post?.finalQualification?.verdict ?? null;
  const overallOk = overall === spec.requiredOverall;
  const record = {
    case: spec.case, mutations: diff, receiptUnderTest: { path: receiptPath, sha256: receiptShaBefore, untouchedByRun: receiptShaBefore === receiptShaAfter },
    command: cmd.map(a => '"' + a + '"').join(' '), wallMs,
    PA2: {
      required: spec.requiredPA2, actual: pa2?.TEST_RESULT ?? null,
      refusalReason: pa2?.ACTUAL?.RECEIPT_QUALIFICATION?.refusalReason ?? null,
      refusalReasons: pa2?.ACTUAL?.RECEIPT_QUALIFICATION?.reasons ?? null,
      recomputedSummary: pa2?.ACTUAL?.RECEIPT_INTERNAL_CONSISTENCY?.recomputed ?? null,
      claimedSummary: pa2?.ACTUAL?.RECEIPT_INTERNAL_CONSISTENCY?.claimed ?? null,
      moduleIdentityCheck: pa2?.ACTUAL?.MODULE_CODE_IDENTITY ? { ok: pa2.ACTUAL.MODULE_CODE_IDENTITY.ok ?? null, gateShaOk: pa2.ACTUAL.MODULE_CODE_IDENTITY.gateModule?.shaOk ?? null, runnerShaOk: pa2.ACTUAL.MODULE_CODE_IDENTITY.runner?.shaOk ?? null } : null,
      liveRemeasurement: pa2?.ACTUAL?.INPUT_BYTES_REMEASURED ? { verdict: pa2.ACTUAL.INPUT_BYTES_REMEASURED.verdict, matched: pa2.ACTUAL.INPUT_BYTES_REMEASURED.matched, blockedCount: pa2.ACTUAL.INPUT_BYTES_REMEASURED.blockedCount } : null,
      perPinDerived: pa2?.ACTUAL?.RECEIPT_INTERNAL_CONSISTENCY?.perPinChecks?.map(c => ({ pin: c.pin, derived: c.derivedCompareResult, claimed: c.claimedCompareResult, valid: c.compareResultValid })) ?? null,
    },
    overall: { required: spec.requiredOverall, actual: overall, missing: post?.finalQualification?.missing ?? null, failing: post?.finalQualification?.failing ?? null },
    exitCode: { required: spec.requiredExit, actual: res.status },
    suite: post ? { tests: post.suite.tests, pass: post.suite.pass, fail: post.suite.fail, exitCode: post.suite.exitCode } : null,
    otherRequiredCasesStillPassed: othersOk, otherCaseResults: otherResults,
    receiptUntouched: receiptShaBefore === receiptShaAfter,
    VERDICT: (pa2Ok && overallOk && exitOk && othersOk && (post ? post.suite.fail === 0 : false) && (spec.case === 'CLEAN' ? true : receiptShaBefore !== shaF(CLEAN_RECEIPT) || diff.length === 0)) ? 'CONTROL_SUCCESS' : 'CONTROL_FAILURE',
  };
  fullPostResults.push(record);
  console.log(spec.case, 'PA2=' + record.PA2.actual, 'overall=' + overall, 'exit=' + res.status, 'othersOk=' + othersOk, record.VERDICT);
}

// ---- four validator profile unit controls (separately counted; direct validator calls) ----
const { loadTrusted, qualifyReceipt, computeQualification, EXPECTED_OUTCOMES } = await import(pathToFileURL(VALIDATOR).href);
const trusted = await loadTrusted(WT);
const profileControls = [];
{
  const mk = caseId => {
    const receipt = JSON.parse(fs.readFileSync(CLEAN_RECEIPT, 'utf8'));
    if (caseId === 'wrong_runId') receipt.runId = 'PE_935_SOME_OTHER_RUN_ID';
    if (caseId === 'wrong_stage') receipt.stage = 'PA2_SOME_OTHER_STAGE';
    if (caseId === 'wrong_mode') receipt.mode = 'MUTANT_TEST (private copies; expected pins frozen and unchanged)';
    const p = path.join(RECEIPTS, caseId + '.json');
    fs.writeFileSync(p, JSON.stringify(receipt, null, 2) + '\n');
    return p;
  };
  for (const caseId of ['wrong_runId', 'wrong_stage', 'wrong_mode']) {
    const q = await qualifyReceipt({ receiptPath: mk(caseId), trusted });
    profileControls.push({
      control: caseId, kind: 'unit profile control (direct validator call, not a full POST case)',
      receiptPath: path.join(RECEIPTS, caseId + '.json'),
      required: 'controlled refusal (RECEIPT_QUALIFICATION FAIL with a profile/context reason)',
      actualVerdict: q.RECEIPT_QUALIFICATION?.verdict, actualReason: q.RECEIPT_QUALIFICATION?.refusalReason,
      context: q.RECEIPT_PROFILE?.context,
      VERDICT: q.RECEIPT_QUALIFICATION?.verdict === 'FAIL' ? 'CONTROL_SUCCESS' : 'CONTROL_FAILURE',
    });
    console.log('unit control', caseId, q.RECEIPT_QUALIFICATION?.verdict, q.RECEIPT_QUALIFICATION?.refusalReason);
  }
  // unreadable / truncated JSON receipt
  const truncatedPath = path.join(RECEIPTS, 'truncated.json');
  fs.writeFileSync(truncatedPath, fs.readFileSync(CLEAN_RECEIPT).subarray(0, 4000)); // half a JSON document — must fail to parse
  const q4 = await qualifyReceipt({ receiptPath: truncatedPath, trusted });
  profileControls.push({
    control: 'unreadable_truncated_json', kind: 'unit profile control (direct validator call, not a full POST case)',
    receiptPath: truncatedPath, required: 'controlled refusal (fail-closed parse failure, never an exception-to-PASS)',
    actualVerdict: q4.RECEIPT_QUALIFICATION?.verdict, actualReason: q4.RECEIPT_QUALIFICATION?.refusalReason,
    VERDICT: q4.RECEIPT_QUALIFICATION?.verdict === 'FAIL' && /not valid JSON/.test(q4.RECEIPT_QUALIFICATION?.refusalReason ?? '') ? 'CONTROL_SUCCESS' : 'CONTROL_FAILURE',
  });
  console.log('unit control truncated_json', q4.RECEIPT_QUALIFICATION?.verdict, q4.RECEIPT_QUALIFICATION?.refusalReason);
  // CLEAN stays unchanged: the same direct validator call must still PASS the CLEAN receipt
  const cleanCopy = path.join(RECEIPTS, 'CLEAN_control.json');
  fs.copyFileSync(CLEAN_RECEIPT, cleanCopy);
  const qc = await qualifyReceipt({ receiptPath: cleanCopy, trusted });
  profileControls.push({
    control: 'CLEAN_unchanged_control', kind: 'unit profile control (direct validator call)',
    receiptPath: cleanCopy, required: 'PASS (the unmodified archived receipt still qualifies; the unit controls did not modify the validator or the CLEAN source)',
    actualVerdict: qc.RECEIPT_QUALIFICATION?.verdict,
    VERDICT: qc.RECEIPT_QUALIFICATION?.verdict === 'PASS' ? 'CONTROL_SUCCESS' : 'CONTROL_FAILURE',
  });
  console.log('unit control CLEAN_unchanged', qc.RECEIPT_QUALIFICATION?.verdict);
}

// ---- three ACTUAL aggregator controls (the shared computeQualification over the REAL CLEAN outcomes) ----
const aggregatorControls = [];
{
  const cleanPost = JSON.parse(fs.readFileSync(path.join(RUN_ROOT, 'matrix/case_CLEAN/out/POST_TEST_RESULTS.json'), 'utf8'));
  const realOutcomes = Object.fromEntries(Object.entries(cleanPost.cases).map(([id, c]) => [id, c.TEST_RESULT]));
  const expectations = { ...EXPECTED_OUTCOMES, AGGREGATOR_CONTROL: 'PASS' };
  const mutations = [
    { control: 'PA2_result_missing', mutate: o => { const p = { ...o }; delete p.PA2_RECEIPT_QUALIFICATION; return p; }, affectedGate: 'PA2_RECEIPT_QUALIFICATION', codePath: 'computeQualification missing-result branch' },
    { control: 'PA2_result_FAIL', mutate: o => ({ ...o, PA2_RECEIPT_QUALIFICATION: 'FAIL' }), affectedGate: 'PA2_RECEIPT_QUALIFICATION', codePath: 'computeQualification failing-result branch' },
    { control: 'PA2_result_NOT_PERFORMED', mutate: o => ({ ...o, PA2_RECEIPT_QUALIFICATION: 'NOT_PERFORMED' }), affectedGate: 'PA2_RECEIPT_QUALIFICATION', codePath: 'computeQualification failing-result branch (explicitly documented statuses only)' },
  ];
  for (const m of mutations) {
    const q = computeQualification(m.mutate(realOutcomes), expectations);
    aggregatorControls.push({
      control: m.control, kind: 'ACTUAL aggregator control (the shared computeQualification imported by the canonical POST, over the REAL measured CLEAN outcomes)',
      affectedGate: m.affectedGate, codePath: m.codePath,
      required: 'QUALIFICATION_REFUSED with a nonzero exit code',
      actual: q,
      VERDICT: (q.ok === false && q.verdict === 'QUALIFICATION_REFUSED' && q.exitCode !== 0 && (q.missing.includes('PA2_RECEIPT_QUALIFICATION') || q.failing.includes('PA2_RECEIPT_QUALIFICATION'))) ? 'CONTROL_SUCCESS' : 'CONTROL_FAILURE',
    });
    console.log('aggregator control', m.control, q.verdict, 'exit', q.exitCode, 'missing', q.missing.join(','), 'failing', q.failing.join(','));
  }
}

// ---- two-source aggregation raw record (extracted from the CLEAN full POST) ----
const cleanPost2 = JSON.parse(fs.readFileSync(path.join(RUN_ROOT, 'matrix/case_CLEAN/out/POST_TEST_RESULTS.json'), 'utf8'));
const tsCase = cleanPost2.cases.DA2_TWO_SOURCE;
const twoSourceRaw = {
  source: 'the CLEAN canonical full POST case DA2_TWO_SOURCE (actual scan through the UNCHANGED staged scanner; per contract §7 the values are generated by the scan, not fabricated)',
  caseRecord: tsCase,
  observerPhases: JSON.parse(fs.readFileSync(path.join(RUN_ROOT, 'matrix/case_CLEAN/out/OBJECT_IDENTITY_OBSERVATIONS.json'), 'utf8')).twoSource,
};
fs.writeFileSync(path.join(POSTS, 'two_source_raw.json'), JSON.stringify(twoSourceRaw, null, 2) + '\n');

// ---- verify the batch freeze (POST code unchanged during the whole matrix) ----
const freezeOk = frozenCode.run_post_sha256 === shaF(CANONICAL_POST) && frozenCode.validate_receipt_sha256 === shaF(VALIDATOR) && frozenCode.gate_module_sha256 === shaF(path.join(WT, 'tools/placement_probe/verify_inputs.mjs')) && frozenCode.clean_receipt_source_sha256 === shaF(CLEAN_RECEIPT);

fs.writeFileSync(path.join(POSTS, 'matrix_receipt_mutations.json'), JSON.stringify({
  frozenCode, freezeOk,
  matrix: fullPostResults,
  expectedTable: MATRIX,
  summary: {
    fullPostCases: fullPostResults.length,
    cleanPass: fullPostResults[0]?.VERDICT === 'CONTROL_SUCCESS',
    mutantsRefused: fullPostResults.slice(1).filter(r => r.PA2.actual === 'FAIL' && r.overall.actual === 'QUALIFICATION_REFUSED' && r.exitCode.actual !== 0 && r.otherRequiredCasesStillPassed).length,
    allControlsSuccess: fullPostResults.every(r => r.VERDICT === 'CONTROL_SUCCESS'),
  },
}, null, 2) + '\n');
fs.writeFileSync(path.join(POSTS, 'full_post_results.json'), JSON.stringify({
  frozenCode, freezeOk,
  cases: fullPostResults.map(r => ({ case: r.case, PA2: r.PA2.actual, refusalReason: r.PA2.refusalReason, overall: r.overall.actual, exit: r.exitCode.actual, otherRequiredCasesStillPassed: r.otherRequiredCasesStillPassed, suite: r.suite, receiptUntouched: r.receiptUntouched, VERDICT: r.VERDICT })),
}, null, 2) + '\n');
fs.writeFileSync(path.join(POSTS, 'validator_profile_controls.json'), JSON.stringify({ controls: profileControls, count: profileControls.length, note: 'four unit controls (wrong runId, wrong stage, wrong mode, unreadable/truncated JSON) + the CLEAN-unchanged control; separately counted from the ten full-POST cases' }, null, 2) + '\n');
fs.writeFileSync(path.join(POSTS, 'aggregator_controls.json'), JSON.stringify({ controls: aggregatorControls, count: aggregatorControls.length, note: 'three ACTUAL aggregator controls over the real measured CLEAN outcomes; separate from receipt cases and from test counts' }, null, 2) + '\n');
console.log('MATRIX COMPLETE: fullPost=' + fullPostResults.length + ' profile=' + profileControls.length + ' aggregator=' + aggregatorControls.length + ' freezeOk=' + freezeOk);
