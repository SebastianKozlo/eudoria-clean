// run_post.mjs — POST evidence harness (v2, after fresh-QC ROUND 2 corrections).
// PROVENANCE: run-local instrument; measures the CORRECTED tool in tools/placement_probe.
// Every case records command, exit code, code identity, fixture identity and measured
// values; the case OUTCOME is computed by an explicit predicate over the measured
// values (never a hand-typed label). Counters are generated from outcomes.
import fs from 'node:fs'; import path from 'node:path'; import os from 'node:os';
import { spawnSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const WT = path.resolve(HERE, '..', '..', '..', '..');
const TOOL = path.join(WT, 'tools/placement_probe/placement_probe.mjs');
const HELPER = path.join(WT, 'tools/placement_probe/ids_from_export.mjs');
const TESTS = path.join(WT, 'tools/placement_probe/tests');
const sha = b => createHash('sha256').update(b).digest('hex');
const shaF = p => sha(fs.readFileSync(p));
const FX = await import(pathToFileURL(path.join(TESTS, 'fixtures.mjs')).href);
const { analyzeBlob, Budget } = await import(pathToFileURL(TOOL).href);
const sets = { S_tpl: new Set([4057, 4058]), S_model: new Set([218757]) };
const codeIdentity = { placement_probe: shaF(TOOL), ids_from_export: shaF(HELPER), fixtures: shaF(path.join(TESTS, 'fixtures.mjs')), node: process.version };
const fixtureIdentity = { records80: sha(FX.records80()), xyzFixture80: sha(FX.xyzFixture80()), layoutBuffer10007: sha(FX.layoutBuffer10007()), poisoned4800: sha(FX.poisoned4800()), countersAsFloats: sha(FX.countersAsFloats()), singleIdTable80: sha(FX.singleIdTable(80)), recordsTwoIdSmall: sha(FX.recordsTwoIdSmall()), records80Headerless: sha(FX.records80Headerless()) };
const out = { tool: 'POST_MEASUREMENTS_CORRECTED_R1', harnessRevision: 'v2_after_fresh_qc_round_2', codeIdentity, fixtureIdentity, node: process.version, cases: {}, generated: { pass: 0, controlPass: 0, fail: 0 } };
const PASSED = 'PASS';
function rec(id, v) { out.cases[id] = { ...v, timeUtc: new Date().toISOString() }; }
function mkRepo(root, bntSrc) { const repo = path.join(root, 'repo'); fs.mkdirSync(path.join(repo, 'src/pesource'), { recursive: true }); fs.writeFileSync(path.join(repo, 'package.json'), '{"type":"module"}'); fs.writeFileSync(path.join(repo, 'src/pesource/Bnt2Archive.js'), bntSrc || FX.shimBntSrc); fs.writeFileSync(path.join(repo, 'src/pesource/ArkArchive.js'), FX.shimArkSrc); fs.writeFileSync(path.join(root, 'ids.json'), JSON.stringify({ S_tpl: [4057, 4058], S_model: [218757] })); return repo; }
function cli(root, repo, inputs, args, tool = TOOL) {
  const outDir = path.join(root, 'out');
  const res = spawnSync(process.execPath, [tool, '--repo', repo, '--ids', path.join(root, 'ids.json'), '--out', outDir, ...inputs.flatMap(n => ['--input', path.join(root, n)]), ...args], { encoding: 'utf8' });
  let summary = null; try { summary = JSON.parse(fs.readFileSync(path.join(outDir, 'SUMMARY.json'), 'utf8')); } catch {}
  return { exitCode: res.status, stderr: res.stderr, stdout: res.stdout, summary, outDirExists: fs.existsSync(outDir) };
}
const tmp = () => fs.mkdtempSync(path.join(os.tmpdir(), 'pe-post-'));

// ===== full test suite (5 files) =====
{
  const files = ['probe.test.mjs', 'cli-fixture.test.mjs', 'correction_matrix.test.mjs', 'budget.test.mjs', 'census_extra.test.mjs'].map(f => path.join(TESTS, f));
  const res = spawnSync(process.execPath, ['--test', ...files], { encoding: 'utf8' });
  const ORIGINAL_SEVEN = ['CLI probes RAW, BNT2, Ark payload via locally imported compatible readers', 'discovers known synthetic record layout without treating it as historical placement', 'wrong IDs do not manufacture a template relation', 'no file/geometry source is inferred from a matching ID alone', 'missing template set is a hard error', 'truncated buffers and zero-row cases do not fabricate a pass', 'independent aligned anchors enable a joint label-position permutation control'];
  const originalSevenPass = ORIGINAL_SEVEN.every(n => new RegExp('^ok \\d+ - ' + n.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '$', 'm').test(res.stdout));
  fs.writeFileSync(path.join(HERE, 'POST_TEST_RESULTS.json'), JSON.stringify({
    command: 'node --test probe.test.mjs cli-fixture.test.mjs correction_matrix.test.mjs budget.test.mjs census_extra.test.mjs', cwd: TESTS, nodeVersion: process.version, codeIdentity, exitCode: res.status, stdout: res.stdout, stderr: res.stderr,
    testsCount: Number((res.stdout.match(/# tests (\d+)/) || [])[1]), passCount: Number((res.stdout.match(/# pass (\d+)/) || [])[1]), failCount: Number((res.stdout.match(/# fail (\d+)/) || [])[1]),
    originalSevenPass, originalSevenNames: ORIGINAL_SEVEN,
  }, null, 2) + '\n');
  rec('TEST_SUITE', { command: 'node --test (5 files)', exitCode: res.status, tests: Number((res.stdout.match(/# tests (\d+)/) || [])[1]), pass: Number((res.stdout.match(/# pass (\d+)/) || [])[1]), fail: Number((res.stdout.match(/# fail (\d+)/) || [])[1]), originalSevenPass, outcome: (Number((res.stdout.match(/# fail (\d+)/) || [])[1]) === 0 && originalSevenPass) ? PASSED : 'FAIL' });
}

// ===== O1 =====
{
  const root = tmp(); try {
    const repo = mkRepo(root); fs.writeFileSync(path.join(root, 'raw.vfs'), FX.records80());
    const bad = cli(root, repo, ['raw.vfs'], ['--max-stride', 'not-a-number']);
    const miss = cli(root, repo, ['raw.vfs'], ['--max-stride']);
    let exportedNan = null; try { analyzeBlob(FX.records80(), sets, { maxStride: NaN }); exportedNan = { threw: false }; } catch (e) { exportedNan = { threw: true, message: String(e.message).slice(0, 120) }; }
    let rateEx = null; try { analyzeBlob(FX.records80(), sets, { minIdRate: 1.5 }); rateEx = { threw: false }; } catch (e) { rateEx = { threw: true, message: String(e.message).slice(0, 120) }; }
    let legalHeaderless = null; try { const r = analyzeBlob(FX.records80Headerless(), sets, { maxHeader: 0, posLo: -200000, minPosRate: 0.9, minIdRate: 0.5, top: 50 }); legalHeaderless = { threw: false, candidates: r.candidates.length }; } catch (e) { legalHeaderless = { threw: true, message: String(e) }; }
    const m = { command: 'CLI --max-stride not-a-number / --max-stride (missing); exported analyzeBlob(maxStride=NaN, minIdRate=1.5); legal boundary maxHeader=0',
      cli_bad_exit: bad.exitCode, cli_bad_invalidLabel: /INVALID_CONFIGURATION/.test(bad.stderr), cli_bad_scanStartedNo: /SCAN_STARTED=NO/.test(bad.stderr), cli_bad_noOutDir: !bad.outDirExists,
      cli_missing_exit: miss.exitCode, cli_missing_scanStartedNo: /SCAN_STARTED=NO/.test(miss.stderr),
      exported_nan_throws: exportedNan.threw, exported_rate_throws: rateEx.threw,
      legal_boundary_headerless_candidates: legalHeaderless.candidates };
    rec('O1_INVALID_NUMERIC_CONFIG', { ...m, outcome: (bad.exitCode !== 0 && m.cli_bad_invalidLabel && m.cli_bad_scanStartedNo && m.cli_bad_noOutDir && miss.exitCode !== 0 && m.cli_missing_scanStartedNo && exportedNan.threw && rateEx.threw && legalHeaderless.candidates > 0) ? PASSED : 'FAIL' });
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
}

// ===== O2 =====
{
  const root = tmp(); try {
    const repo = mkRepo(root); const good = FX.records80();
    fs.writeFileSync(path.join(root, 'c.bnt'), FX.realBnt2([{ name: 'scan.rec', data: good }, { name: 'tex.nif', data: good }, { name: 'tiny.rec', data: Buffer.alloc(8, 0xff) }, { name: 'huge.rec', data: good }]));
    const a = cli(root, repo, ['c.bnt'], []);
    const c = a.summary.exclusionCensus[0];
    const b = cli(root, repo, ['c.bnt'], ['--entry-regex', '^scan\\.rec$']);
    const c2 = b.summary.exclusionCensus[0];
    const m = { command: 'CLI single c.bnt (4 declared entries), default and --entry-regex',
      exitCode: a.exitCode, declared: c.declaredEntryCount, dispositionTotal: c.dispositionTotal, censusOk: c.censusOk,
      counts: c.dispositionCounts, units: { containers: a.summary.sourceCount, scannedPayloads: c.scannedPayloadCount },
      regexCounts: c2.dispositionCounts, regexCensusOk: c2.censusOk };
    rec('O2_EXCLUSION_CENSUS', { ...m, outcome: (a.exitCode === 0 && c.censusOk === true && c.dispositionTotal === c.declaredEntryCount && c.dispositionCounts.SCANNED === 2 && c.dispositionCounts.FILTERED_EXTENSION === 1 && c.dispositionCounts.TOO_SMALL === 1 && c2.censusOk === true && c2.dispositionCounts.FILTERED_REGEX === 3 && c2.dispositionCounts.SCANNED === 1) ? PASSED : 'FAIL' });
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
}

// ===== O3 =====
{
  const root = tmp(); try {
    const repo = mkRepo(root); fs.writeFileSync(path.join(root, 'big.vfs'), FX.poisoned4800());
    const r = cli(root, repo, ['big.vfs'], ['--max-stride', '64']);
    const top = JSON.parse(fs.readFileSync(path.join(root, 'out', 'candidates_top.json'), 'utf8'));
    const c = top.find(x => x.header === 16 && x.stride === 32 && x.idOffset === 0);
    const m = { command: 'CLI single big.vfs (4800 rows, valid IDs only at i%4===2), --max-stride 64',
      exitCode: r.exitCode, tableRowCount: c.tableRowCount, sampledRowCount: c.sampledRowCount,
      sampleIdRate: c.idRate, sampleXyzFiniteRate: c.sampleXyzFiniteRate,
      censusStatus: c.censusStatus, fullCensusRowCount: c.fullCensusRowCount, fullCensusIdRate: c.fullCensusIdRate, fullCensusXyzFiniteRate: c.fullCensusXyzFiniteRate };
    rec('O3_SAMPLE_VS_CENSUS', { ...m, note: 'sample rate 1.0 is NOT presented as table quality; the FULL_CENSUS reproduces the known 0.25 quality', outcome: (r.exitCode === 0 && c.tableRowCount === 4800 && c.sampledRowCount === 1200 && c.idRate === 1 && c.censusStatus === 'FULL_CENSUS' && c.fullCensusIdRate === 0.25) ? PASSED : 'FAIL' });
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
}

// ===== O4 =====
{
  const b = FX.singleIdTable(80);
  const atOne = analyzeBlob(b, sets, { minDistinctId: 1, minIdRate: 0.5, maxStride: 128, minPosRate: 0.9, top: 50 });
  const atDefault = analyzeBlob(b, sets, { minIdRate: 0.5, maxStride: 128, minPosRate: 0.9, top: 50 });
  const m = { command: 'exported analyzeBlob on singleIdTable(80), minDistinctId=1 vs default 2',
    minDistinctId1_candidates: atOne.candidates.length, allIdDistinct1: atOne.candidates.every(x => x.idDistinct === 1), default_candidates: atDefault.candidates.length };
  rec('O4_SINGLE_DEFINITION_TABLE', { ...m, outcome: (atOne.candidates.length > 0 && m.allIdDistinct1 && atDefault.candidates.length === 0) ? PASSED : 'FAIL' });
}

// ===== O5 =====
{
  const b = FX.countersAsFloats();
  const r = analyzeBlob(b, sets, { minIdRate: 0.5, maxStride: 128, minPosRate: 0.88, top: 50 });
  const c = r.candidates.find(x => x.xyzOffset === 4);
  const cen = c.fullCensus;
  const m = { command: 'exported analyzeBlob on countersAsFloats() (u32 counters 1..5079 as f32 subnormals)',
    candidateFound: !!c, censusStatus: c.censusStatus, perAxis: cen.perAxis.map(a => ({ finiteRate: a.finiteRate, nanCount: a.nanCount, infinityCount: a.infinityCount, subnormalCount: a.subnormalCount, zeroCount: a.zeroCount, u32: a.alternativeU32Interpretation })),
    placementClaimPresent: /PLACEMENT_CONFIRMED|HISTORICAL_PLACEMENT/.test(JSON.stringify(c)) };
  rec('O5_INTEGER_COUNTERS_AS_FLOATS', { ...m, outcome: (!!c && c.censusStatus === 'FULL_CENSUS' && cen.perAxis.every(a => a.subnormalCount > 0 && a.finiteRate > 0 && typeof a.alternativeU32Interpretation.min === 'number') && !m.placementClaimPresent) ? PASSED : 'FAIL' });
}

// ===== O6 =====
{
  const root = tmp(); try {
    fs.writeFileSync(path.join(root, 'ids.json'), JSON.stringify({ S_tpl: [4057, 4058], S_model: [218757] }));
    const good = FX.records80();
    fs.writeFileSync(path.join(root, 'raw.vfs'), good);
    fs.writeFileSync(path.join(root, 'test.bnt'), FX.realBnt2([{ name: '4057.rec', data: good }]));
    fs.writeFileSync(path.join(root, 'test.ark'), FX.realArk([{ name: '4057.rec', data: good }]));
    const res = spawnSync(process.execPath, [TOOL, '--repo', WT, '--ids', path.join(root, 'ids.json'), '--out', path.join(root, 'out'), '--input', path.join(root, 'raw.vfs'), '--input', path.join(root, 'test.bnt'), '--input', path.join(root, 'test.ark')], { encoding: 'utf8' });
    const summary = JSON.parse(fs.readFileSync(path.join(root, 'out', 'SUMMARY.json'), 'utf8'));
    const m = { command: 'CLI RAW+BNT2+ARK with the real BASE adapters (repo = BASE worktree)', exitCode: res.status, sourceCount: summary.sourceCount, candidateCount: summary.candidateCount, adaptersGitBlobs: { Bnt2Archive: '1fb862905b4749f3336bb47da87441edbd018fb7', ArkArchive: 'a9c9f04319dc3128d527d0688285ec5384f8aa97' } };
    rec('O6_ACTUAL_PROJECT_ADAPTERS', { ...m, outcome: (res.status === 0 && summary.sourceCount === 3 && summary.candidateCount >= 3) ? PASSED : 'FAIL' });
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
}

// ===== O7 =====
{
  const root = tmp(); try {
    fs.writeFileSync(path.join(root, 'tpl.csv'), FX.idsCsv('templateId'));
    fs.writeFileSync(path.join(root, 'models.bnt'), FX.realBnt2([
      { name: '123.nif', data: Buffer.alloc(16, 0xff) }, { name: '218757.nif', data: Buffer.alloc(16, 0xff) }, { name: 'prop_a.nif', data: Buffer.alloc(16, 0xff) }]));
    fs.writeFileSync(path.join(root, 'models.dat'), Buffer.from('dummy'));
    const run = args => spawnSync(process.execPath, [HELPER, ...args], { encoding: 'utf8' });
    const dat = run(['--csv', path.join(root, 'tpl.csv'), '--id-column', 'templateId', '--repo', WT, '--model-archive', path.join(root, 'models.dat'), '--out', path.join(root, 'out.json')]);
    const bnt = run(['--csv', path.join(root, 'tpl.csv'), '--id-column', 'templateId', '--repo', WT, '--model-archive', path.join(root, 'models.bnt'), '--out', path.join(root, 'out.json')]);
    const consoleJson = JSON.parse(bnt.stdout);
    const m = { command: 'ids_from_export with models.dat (rejected) and models.bnt (numeric + non-numeric names)',
      datExit: dat.status, datRejected: /must be \.bnt or \.ark/.test(dat.stderr),
      bntExit: bnt.status, modelIds: consoleJson.modelIds, nifEntries: consoleJson.modelArchives[0].nifEntries, nonNumericNamesExcluded: consoleJson.modelArchives[0].nonNumericNamesExcluded };
    rec('O7_NUMERIC_DAT_MODEL_NAME_PATTERN', { ...m, note: 'hypothetical .dat is a helper limitation, NOT presented as a defect of the actual Models.bnt', outcome: (dat.status !== 0 && m.datRejected && bnt.status === 0 && consoleJson.modelIds === 2 && m.nifEntries === 2 && m.nonNumericNamesExcluded === 1) ? PASSED : 'FAIL' });
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
}

// ===== S7a =====
{
  const b = FX.layoutBuffer10007();
  const r = analyzeBlob(b, sets, { maxHeader: 0, maxStride: 512 });
  const r2 = analyzeBlob(b, sets, { maxHeader: 0, maxStride: 512, budgetThresholds: { layoutEvaluations: 60 } });
  const m = { command: 'exported analyzeBlob on 10007B 0xFF buffer, maxHeader=0, strides 12..512; lowered limit 60',
    layoutAttempts: r.stats.layoutAttempts, layoutsAdmitted: r.stats.layoutsAdmitted, legacyLayoutsTested: r.stats.layoutsTested, coverage: r.stats.coverage,
    loweredLimit: { threshold: 60, layoutAttempts: r2.stats.layoutAttempts, budgetExhausted: r2.stats.budgetExhausted, coverage: r2.stats.coverage, refusal: r2.budget.refusals[0] },
    budgetChargedQuantity: 'LAYOUT_ATTEMPTS (first magnitude), not LAYOUTS_ADMITTED' };
  rec('S7a_LAYOUT_ATTEMPTS_VS_ADMITTED', { ...m, outcome: (r.stats.layoutAttempts === 126 && r.stats.layoutsAdmitted === 0 && r.stats.layoutsTested === 0 && r2.stats.layoutAttempts === 61 && r2.stats.budgetExhausted === true && r2.stats.coverage === 'PARTIAL' && r2.budget.refusals[0].kind === 'LAYOUT_EVALUATIONS') ? PASSED : 'FAIL' });
}

// ===== S7b =====
{
  const b = FX.xyzFixture80();
  const r = analyzeBlob(b, sets, { minPosRate: 0.88, minIdRate: 0.35, top: 50 });
  const c = r.candidates.find(x => x.header === 16 && x.stride === 32 && x.idOffset === 0 && x.idWidth === 2 && x.xyzOffset === 4);
  const m = { command: 'exported analyzeBlob on xyzFixture80() (8 NaN per axis in rows 0..7/8..15/16..23)',
    legacyXyzRateColumnMean: c.xyzRate, sampleXyzFiniteRate: c.sampleStats.xyzFiniteRate, completeFiniteTriples: c.sampleStats.completeFiniteTriples, sampleDenominator: c.sampleStats.denominator,
    perAxisFiniteRates: c.sampleStats.perAxis.map(a => a.finiteRate), perAxisNanCounts: c.sampleStats.perAxis.map(a => a.nanCount),
    censusStatus: c.censusStatus, fullCensusXyzFiniteRate: c.fullCensusXyzFiniteRate, fullCensusRowCount: c.fullCensusRowCount };
  rec('S7b_XYZ_TRIPLE_RATE', { ...m, expectedFromCountercheck: { columnMean: 0.9, tripleRate: 0.7, triples: '56/80' }, note: '0.9 stays labeled as the legacy per-axis column mean; the joint XYZ_FINITE_RATE is 56/80=0.7 and is the quantity reported as the common rate', outcome: (c.xyzRate === 0.9 && c.sampleStats.xyzFiniteRate === 0.7 && c.sampleStats.completeFiniteTriples === 56 && c.sampleStats.denominator === 80 && c.censusStatus === 'FULL_CENSUS' && c.fullCensusXyzFiniteRate === 0.7 && c.fullCensusRowCount === 80 && c.sampleStats.perAxis.every(a => a.finiteRate === 0.9 && a.nanCount === 8)) ? PASSED : 'FAIL' });
}
// ===== budget battery B1..B7 (v2: 2-input aggregation scenarios) =====
{
  const results = {};
  // B1 — SYNTHETIC_INPUTS: 32 of 33 entries of file 1 admitted; file 2 entry refused (2-input aggregation)
  {
    const root = tmp(); try {
      const repo = mkRepo(root);
      const entries = []; for (let i = 0; i < 33; i++) entries.push({ name: `e${i}.rec`, data: FX.recordsTwoIdSmall() });
      fs.writeFileSync(path.join(root, 'many.bnt'), FX.realBnt2(entries));
      fs.writeFileSync(path.join(root, 'one.bnt'), FX.realBnt2([{ name: 'x.rec', data: FX.recordsTwoIdSmall() }]));
      const r = cli(root, repo, ['many.bnt', 'one.bnt'], []);
      const c = r.summary.exclusionCensus[0];
      const c1 = r.summary.exclusionCensus[1];
      const m = { limit: 'SYNTHETIC_INPUTS', ceiling: 32, legalBoundaryAdmitted: r.summary.budgets.used.syntheticInputs, refusals: r.summary.budgets.refusals.filter(x => x.kind === 'SYNTHETIC_INPUTS'), exhausted: r.summary.budgets.exhausted, coverage: r.summary.budgets.coverage, firstContainer: { overBudget: c.dispositionCounts.OVER_BUDGET, scanned: c.dispositionCounts.SCANNED, censusOk: c.censusOk }, secondContainer: { declared: c1.declaredEntryCount, disposition: c1.dispositions[0].disposition, censusOk: c1.censusOk }, candidates: r.summary.candidateCount };
      m.outcome = (m.legalBoundaryAdmitted === 32 && m.exhausted.includes('SYNTHETIC_INPUTS') && m.coverage === 'PARTIAL' && m.firstContainer.scanned === 32 && m.firstContainer.overBudget === 1 && m.firstContainer.censusOk === true && m.secondContainer.declared === 1 && m.secondContainer.disposition === 'OVER_BUDGET' && m.secondContainer.censusOk === true && m.candidates > 0) ? PASSED : 'FAIL';
      results.B1 = m;
    } finally { fs.rmSync(root, { recursive: true, force: true }); }
  }
  // B2 — SCANNED_BYTES: reservation before read; aggregation across two raw inputs; refund of refused-before-read
  {
    const root = tmp(); try {
      const repo = mkRepo(root); fs.writeFileSync(path.join(root, 'a.vfs'), FX.records80()); fs.writeFileSync(path.join(root, 'b.vfs'), FX.records80());
      const r = cli(root, repo, ['a.vfs', 'b.vfs'], ['--budget-scanned-bytes', '2676']);
      const r2 = cli(root, repo, ['a.vfs', 'b.vfs'], ['--budget-scanned-bytes', '5152']);
      const m = { limit: 'SCANNED_BYTES', ceiling: 67108864, exceedCase: { scannedBytes: r.summary.budgets.used.scannedBytes, exhausted: r.summary.budgets.exhausted, secondInputDisposition: r.summary.exclusionCensus[1].dispositions[0].disposition }, legalBoundary: { scannedBytes: r2.summary.budgets.used.scannedBytes, coverage: r2.summary.budgets.coverage, bothScanned: r2.summary.exclusionCensus.every(x => x.dispositions[0].disposition === 'SCANNED') } };
      m.outcome = (m.exceedCase.scannedBytes === 2576 && m.exceedCase.exhausted.includes('SCANNED_BYTES') && m.exceedCase.secondInputDisposition === 'OVER_BUDGET' && m.legalBoundary.scannedBytes === 5152 && m.legalBoundary.coverage === 'FULL' && m.legalBoundary.bothScanned) ? PASSED : 'FAIL';
      results.B2 = m;
    } finally { fs.rmSync(root, { recursive: true, force: true }); }
  }
  // B3 — LAYOUT_EVALUATIONS: aggregation across two inputs (cap 3000) + pre-exhaustion disposition honesty (cap 700)
  {
    const root = tmp(); try {
      const repo = mkRepo(root); fs.writeFileSync(path.join(root, 'a.vfs'), FX.records80()); fs.writeFileSync(path.join(root, 'b.vfs'), FX.records80());
      const r = cli(root, repo, ['a.vfs', 'b.vfs'], ['--budget-layout-evals', '3000', '--max-stride', '512']);
      const skips = fs.readFileSync(path.join(root, 'out', 'scan_skips.csv'), 'utf8');
      const r0 = cli(root, repo, ['a.vfs', 'b.vfs'], ['--budget-layout-evals', '700', '--max-stride', '512']);
      const r2 = cli(root, repo, ['a.vfs', 'b.vfs'], []);
      const m = { limit: 'LAYOUT_EVALUATIONS', ceiling: 100000, aggregatedAttempts: r.summary.budgets.used.layoutAttempts, exhausted: r.summary.budgets.exhausted, refusal: r.summary.budgets.refusals[r.summary.budgets.refusals.length - 1], secondInputDisposition: r.summary.exclusionCensus[1].dispositions[0].disposition, budgetStopRecorded: skips.includes('BUDGET_EXHAUSTED'), preExhaustionCase: { attempts: r0.summary.budgets.used.layoutAttempts, secondInputDisposition: r0.summary.exclusionCensus[1].dispositions[0].disposition, censusOk: r0.summary.exclusionCensus[1].censusOk }, defaultCeilingCase: { layoutAttempts: r2.summary.budgets.used.layoutAttempts, coverage: r2.summary.budgets.coverage } };
      m.outcome = (m.aggregatedAttempts === 3001 && m.exhausted.includes('LAYOUT_EVALUATIONS') && m.secondInputDisposition === 'SCANNED' && m.budgetStopRecorded && m.preExhaustionCase.attempts === 701 && m.preExhaustionCase.secondInputDisposition === 'OVER_BUDGET' && m.preExhaustionCase.censusOk === true && m.defaultCeilingCase.coverage === 'FULL' && m.defaultCeilingCase.layoutAttempts === 4284) ? PASSED : 'FAIL';
      results.B3 = m;
    } finally { fs.rmSync(root, { recursive: true, force: true }); }
  }
  // B4 — FULL_CENSUS_ROWS
  {
    const root = tmp(); try {
      const repo = mkRepo(root); fs.writeFileSync(path.join(root, 'a.vfs'), FX.records80()); fs.writeFileSync(path.join(root, 'b.vfs'), FX.records80());
      const r = cli(root, repo, ['a.vfs', 'b.vfs'], ['--budget-census-rows', '160', '--top', '2']);
      const top = JSON.parse(fs.readFileSync(path.join(root, 'out', 'candidates_top.json'), 'utf8'));
      const r2 = cli(root, repo, ['a.vfs', 'b.vfs'], []);
      const top2 = JSON.parse(fs.readFileSync(path.join(root, 'out', 'candidates_top.json'), 'utf8'));
      const m = { limit: 'FULL_CENSUS_ROWS', ceiling: 50000, exceedCase: { censusRowsUsed: r.summary.budgets.used.fullCensusRows, statuses: [...new Set(top.map(c => c.censusStatus))], refusals: r.summary.budgets.refusals.filter(x => x.kind === 'FULL_CENSUS_ROWS') }, legalBoundary: { statuses: [...new Set(top2.map(c => c.censusStatus))], coverage: r2.summary.budgets.coverage } };
      m.outcome = (m.exceedCase.statuses.includes('PARTIAL_BUDGET_EXHAUSTED') && m.exceedCase.statuses.includes('FULL_CENSUS') && m.exceedCase.refusals.length >= 1 && m.legalBoundary.statuses.every(s => s === 'FULL_CENSUS') && m.legalBoundary.coverage === 'FULL') ? PASSED : 'FAIL';
      results.B4 = m;
    } finally { fs.rmSync(root, { recursive: true, force: true }); }
  }
  // B5 — RETAINED_CANDIDATES: global peak across structures, 2-input aggregation
  {
    const root = tmp(); try {
      const repo = mkRepo(root); fs.writeFileSync(path.join(root, 'a.vfs'), FX.records80()); fs.writeFileSync(path.join(root, 'b.vfs'), FX.records80());
      const r = cli(root, repo, ['a.vfs'], ['--budget-retained-candidates', '4']);
      const r3 = cli(root, repo, ['a.vfs', 'b.vfs'], ['--budget-retained-candidates', '4']);
      const r2 = cli(root, repo, ['a.vfs'], ['--budget-retained-candidates', '256']);
      const m = { limit: 'RETAINED_CANDIDATES', ceiling: 256, exceedCase: { peakRetained: r.summary.budgets.used.peakRetainedCandidates, exhausted: r.summary.budgets.exhausted, candidates: r.summary.candidateCount, coverage: r.summary.budgets.coverage }, twoInputAggregation: { peakRetained: r3.summary.budgets.used.peakRetainedCandidates, exhausted: r3.summary.budgets.exhausted.includes('RETAINED_CANDIDATES'), coverage: r3.summary.budgets.coverage, candidates: r3.summary.candidateCount }, legalBoundary: { peakRetained: r2.summary.budgets.used.peakRetainedCandidates, coverage: r2.summary.budgets.coverage } };
      m.outcome = (m.exceedCase.peakRetained <= 4 && m.exceedCase.exhausted.includes('RETAINED_CANDIDATES') && m.exceedCase.coverage === 'PARTIAL' && m.exceedCase.candidates > 0 && m.twoInputAggregation.peakRetained <= 4 && m.twoInputAggregation.exhausted === true && m.twoInputAggregation.coverage === 'PARTIAL' && m.twoInputAggregation.candidates > 0 && m.legalBoundary.coverage === 'FULL') ? PASSED : 'FAIL';
      results.B5 = m;
    } finally { fs.rmSync(root, { recursive: true, force: true }); }
  }
  // B6 — ceilings can never be raised (full error messages kept)
  {
    let raisedEx = null; try { analyzeBlob(FX.records80(), sets, { budgetThresholds: { layoutEvaluations: 100001 } }); raisedEx = { threw: false }; } catch (e) { raisedEx = { threw: true, message: String(e.message) }; }
    const root = tmp(); try { const repo = mkRepo(root); fs.writeFileSync(path.join(root, 'a.vfs'), FX.records80()); const r = cli(root, repo, ['a.vfs'], ['--budget-layout-evals', '100001']); const m = { rule: 'threshold may not exceed canonical ceiling', exportedRaised: raisedEx, cliRaised: { exitCode: r.exitCode, invalidLabel: /INVALID_CONFIGURATION/.test(r.stderr), scanStartedNo: /SCAN_STARTED=NO/.test(r.stderr), stderr: r.stderr.trim() } }; m.outcome = (raisedEx.threw === true && /ceiling/.test(raisedEx.message) && r.exitCode !== 0 && m.cliRaised.invalidLabel && m.cliRaised.scanStartedNo) ? PASSED : 'FAIL'; results.B6 = m; } finally { fs.rmSync(root, { recursive: true, force: true }); }
  }
  // B7 — Budget class semantics
  {
    const b = new Budget({ scannedBytes: 500 });
    const a1 = b.admitPayload(300, 'x'), a2 = b.admitPayload(300, 'y');
    b.refundPayload(300);
    const after = b.scannedBytes;
    const b3 = new Budget(); b3.admitPayload(100, 'p'); b3.refundPayload(100);
    const b2 = new Budget(); b2.containerReadBytes += 1234; b2.controlWorkBytes += 512; const s = b2.summary();
    const m = { rule: 'no-reset-per-payload aggregation; reservation refund; separate container/control byte accounting', firstAdmitted: a1, secondRefused: !a2, scannedBytesAfterFirst: 300, refundWorks: (after === 0 && b.syntheticInputs === 0), refundZeroesInputs: (b3.syntheticInputs === 0 && b3.scannedBytes === 0), exhausted: b.exhausted, coverage: b.coverage, separate: { containerReadBytes: s.containerReadBytes, controlWorkBytes: s.controlWorkBytes, scannedBytes: s.used.scannedBytes } };
    m.outcome = (a1 === true && !a2 === true && after === 0 && m.refundWorks && m.refundZeroesInputs && b.coverage === 'PARTIAL' && s.containerReadBytes === 1234 && s.controlWorkBytes === 512 && s.used.scannedBytes === 0) ? PASSED : 'FAIL';
    results.B7 = m;
  }
  // CX1..CX4 — census extra categories (fresh-QC F10)
  {
    const root = tmp(); try {
      const repo = mkRepo(root);
      fs.writeFileSync(path.join(root, 'c.bnt'), FX.realBnt2([{ name: 'small.rec', data: FX.small16 ? FX.small16() : FX.recordsTwoIdSmall() }, { name: 'big.rec', data: FX.records80() }]));
      const r = cli(root, repo, ['c.bnt'], ['--max-payload-mib', '0.001']);
      const c = r.summary.exclusionCensus[0];
      const m = { case: 'ENTRY_TOO_LARGE', counts: c.dispositionCounts, censusOk: c.censusOk };
      m.outcome = (r.exitCode === 0 && c.dispositionCounts.SCANNED === 1 && c.dispositionCounts.ENTRY_TOO_LARGE === 1 && c.censusOk === true) ? PASSED : 'FAIL';
      results.CX1 = m;
    } finally { fs.rmSync(root, { recursive: true, force: true }); }
  }
  {
    const root = tmp(); try {
      const repo = mkRepo(root); fs.writeFileSync(path.join(root, 'a.vfs'), FX.records80());
      const r = cli(root, repo, ['a.vfs'], ['--max-input-mib', '0.001']);
      const c = r.summary.exclusionCensus[0];
      const m = { case: 'INPUT_TOO_LARGE', parseStatus: c.parseStatus, declaredEntryCount: c.declaredEntryCount, candidateCount: r.summary.candidateCount, scannedBytes: r.summary.budgets.used.scannedBytes };
      m.outcome = (c.parseStatus === 'INPUT_TOO_LARGE' && c.declaredEntryCount === null && r.summary.candidateCount === 0 && r.summary.budgets.used.scannedBytes === 0) ? PASSED : 'FAIL';
      results.CX2 = m;
    } finally { fs.rmSync(root, { recursive: true, force: true }); }
  }
  {
    const root = tmp(); try {
      const repo = mkRepo(root);
      const bogus = Buffer.alloc(64, 0x41); bogus.write('XXXX', 60, 'ascii');
      fs.writeFileSync(path.join(root, 'bad.bnt'), bogus);
      const r = cli(root, repo, ['bad.bnt'], []);
      const c = r.summary.exclusionCensus[0];
      const skips = fs.readFileSync(path.join(root, 'out', 'scan_skips.csv'), 'utf8');
      const m = { case: 'UNSUPPORTED', exitCode: r.exitCode, parseStatus: c.parseStatus, declaredEntryCount: c.declaredEntryCount, skipRecorded: skips.includes('CONTAINER_PARSE_FAILED') };
      m.outcome = (r.exitCode === 2 && c.parseStatus === 'UNSUPPORTED' && c.declaredEntryCount === null && m.skipRecorded) ? PASSED : 'FAIL';
      results.CX3 = m;
    } finally { fs.rmSync(root, { recursive: true, force: true }); }
  }
  {
    const root = tmp(); try {
      const truncShim = FX.shimBntSrc.replace('readEntry(e){return {payload:this.b.subarray(e.offset,e.offset+e.size)}}', 'readEntry(e){return {payload:this.b.subarray(e.offset,Math.max(0,e.offset+e.size-4))}}');
      const repo = mkRepo(root, truncShim);
      fs.writeFileSync(path.join(root, 'c.bnt'), FX.realBnt2([{ name: 'x.rec', data: FX.recordsTwoIdSmall() }]));
      const r = cli(root, repo, ['c.bnt'], []);
      const c = r.summary.exclusionCensus[0];
      const skips = fs.readFileSync(path.join(root, 'out', 'scan_skips.csv'), 'utf8');
      const m = { case: 'PAYLOAD_SIZE_MISMATCH', shimActuallyTruncated: truncShim !== FX.shimBntSrc, parseFailed: c.dispositionCounts.PARSE_FAILED, censusOk: c.censusOk, scannedBytesAfterRefund: r.summary.budgets.used.scannedBytes, syntheticInputsAfterRefund: r.summary.budgets.used.syntheticInputs, skipRecorded: skips.includes('PAYLOAD_SIZE_MISMATCH') };
      m.outcome = (m.shimActuallyTruncated && m.parseFailed === 1 && m.censusOk === true && m.scannedBytesAfterRefund === 0 && m.syntheticInputsAfterRefund === 0 && m.skipRecorded) ? PASSED : 'FAIL';
      results.CX4 = m;
    } finally { fs.rmSync(root, { recursive: true, force: true }); }
  }
  rec('BUDGET_BATTERY', { command: 'CLI + exported budget scenarios B1..B7 + census extra categories CX1..CX4 (thresholds LOWERED, ceilings never raised)', ...results });
  const budgetAccounting = {
    run: 'PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011',
    limits: { MAX_FIX_ROUNDS: 2, MAX_SYNTHETIC_INPUTS_PER_INVOCATION: 32, MAX_SCANNED_BYTES_PER_INVOCATION: 67108864, MAX_LAYOUT_EVALUATIONS_PER_INVOCATION: 100000, MAX_FULL_CENSUS_ROWS_PER_INVOCATION: 50000, MAX_RETAINED_CANDIDATES: 256 },
    perLimit: results,
    fixRoundsUsed: 2,
    notes: 'Thresholds lowered only for short fixtures; ceilings never raised. LAYOUT_ATTEMPTS is charged (not LAYOUTS_ADMITTED). Reservation happens BEFORE the payload read using the verified size (declared directory size / on-disk stat size) and is refunded when the payload fails to decode (read failure, size mismatch); an admitted payload skipped due to earlier budget exhaustion stays charged (admission-time accounting). Container-read and control-work bytes are reported separately from SCANNED_BYTES. RETAINED_CANDIDATES applies to the GLOBAL peak across all structures (main rows + per-call lists). Exhaustion => BUDGET_EXHAUSTED + COVERAGE=PARTIAL, never NO_CANDIDATE. Aggregation across >= 2 inputs is exercised for SYNTHETIC_INPUTS (B1), SCANNED_BYTES (B2), LAYOUT_EVALUATIONS (B3), FULL_CENSUS_ROWS (B4), RETAINED_CANDIDATES (B5).',
  };
  fs.writeFileSync(path.join(HERE, '..', 'BUDGET_ACCOUNTING.json'), JSON.stringify(budgetAccounting, null, 2) + '\n');
}

// counters generated from computed outcomes
for (const [id, c] of Object.entries(out.cases)) {
  if (id === 'TEST_SUITE') { out.generated.pass += c.pass; out.generated.fail += c.fail; continue; }
  if (id === 'BUDGET_BATTERY') { for (const [k, v] of Object.entries(c)) if (/^[BC]X?\d/.test(k)) { if (v.outcome === 'PASS') out.generated.pass++; else out.generated.fail++; } continue; }
  if (c.outcome === 'PASS') out.generated.pass++;
  else out.generated.fail++;
}
fs.writeFileSync(path.join(HERE, 'POST_MEASUREMENTS.json'), JSON.stringify(out, null, 2) + '\n');
console.log('POST_MEASUREMENTS.json written; cases=' + Object.keys(out.cases).length + ' pass=' + out.generated.pass + ' fail=' + out.generated.fail);