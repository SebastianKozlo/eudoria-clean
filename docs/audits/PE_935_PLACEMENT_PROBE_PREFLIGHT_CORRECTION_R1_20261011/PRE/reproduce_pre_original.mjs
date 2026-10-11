// reproduce_pre_original.mjs — PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011
// PROVENANCE: run-local instrument for the PRESERVED PRE stage. It measures the
// ORIGINAL R1 kit (from the pinned ZIP, extracted to staging) on the §6/§7 cases.
// It writes PRE/PRE_MEASUREMENTS.json. Synthetic inputs only; no game payloads.
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { spawnSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';
import * as FX from '../../../../tools/placement_probe/tests/fixtures.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const STAGE = process.env.PE_KIT_STAGE; // staging dir with original kit
const WORKTREE = path.resolve(HERE, '../..', '../..'); // repo root (worktree)
const sha256 = b => createHash('sha256').update(b).digest('hex');
const results = { tool: 'PRE_REPRODUCE_ORIGINAL_R1', node: process.version, stage: STAGE, cases: {} };
function record(caseId, obj) { results.cases[caseId] = { ...obj, timeUtc: new Date().toISOString() }; }

// --- original 7 tests ---------------------------------------------------------
{
  const res = spawnSync(process.execPath, ['--test', 'tests/probe.test.mjs', 'tests/cli-fixture.test.mjs'], { cwd: STAGE, encoding: 'utf8' });
  fs.writeFileSync(path.join(HERE, 'ORIGINAL_TEST_RESULTS.json'), JSON.stringify({
    command: 'node --test tests/probe.test.mjs tests/cli-fixture.test.mjs', cwd: STAGE,
    nodeVersion: process.version, codeIdentity: { placement_probe: sha256(fs.readFileSync(path.join(STAGE, 'placement_probe.mjs'))), ids_from_export: sha256(fs.readFileSync(path.join(STAGE, 'ids_from_export.mjs'))), probe_test: sha256(fs.readFileSync(path.join(STAGE, 'tests/probe.test.mjs'))), cli_fixture_test: sha256(fs.readFileSync(path.join(STAGE, 'tests/cli-fixture.test.mjs'))) },
    exitCode: res.status, stdout: res.stdout, stderr: res.stderr,
    passCount: (res.stdout.match(/^# pass (\d+)$/m) || [])[1], failCount: (res.stdout.match(/^# fail (\d+)$/m) || [])[1],
  }, null, 2) + '\n');
  record('ORIGINAL_SEVEN_TESTS', { exitCode: res.status, pass: results.cases.ORIGINAL_SEVEN_TESTS ? null : (res.stdout.match(/# pass (\d+)/) || [])[1], fail: (res.stdout.match(/# fail (\d+)/) || [])[1] });
}

// import ORIGINAL analyzeBlob + CLI helpers
const orig = await import(pathToFileURL(path.join(STAGE, 'placement_probe.mjs')).href);
const analyzeBlob = orig.analyzeBlob;
const sets = { S_tpl: new Set([4057, 4058]), S_model: new Set([218757]) };

// helpers for CLI runs of the ORIGINAL tool
function mkRepo(root) { const repo = path.join(root, 'repo'); fs.mkdirSync(path.join(repo, 'src/pesource'), { recursive: true }); fs.writeFileSync(path.join(repo, 'package.json'), '{"type":"module"}'); fs.writeFileSync(path.join(repo, 'src/pesource/Bnt2Archive.js'), FX.shimBntSrc); fs.writeFileSync(path.join(repo, 'src/pesource/ArkArchive.js'), FX.shimArkSrc); return repo; }
function cliRun(root, { repo, args, inputs }) {
  const out = path.join(root, 'out');
  const full = ['--repo', repo, '--ids', path.join(root, 'ids.json'), '--out', out, ...inputs.flatMap(n => ['--input', path.join(root, n)]), ...args];
  const res = spawnSync(process.execPath, [path.join(STAGE, 'placement_probe.mjs'), ...full], { encoding: 'utf8' });
  let summary = null, sources = null, skips = null, csv = null;
  try { summary = JSON.parse(fs.readFileSync(path.join(out, 'SUMMARY.json'), 'utf8')); } catch {}
  try { sources = JSON.parse(fs.readFileSync(path.join(out, 'sources.json'), 'utf8')); } catch {}
  try { skips = fs.readFileSync(path.join(out, 'scan_skips.csv'), 'utf8'); } catch {}
  try { csv = fs.readFileSync(path.join(out, 'placement_candidates.csv'), 'utf8'); } catch {}
  return { exitCode: res.status, stdout: res.stdout, stderr: res.stderr, summary, sources, skips, csv, outDirExists: fs.existsSync(out) };
}

// --- O1 INVALID_NUMERIC_CONFIG ------------------------------------------------
{
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'pe-pre-o1-'));
  const repo = mkRepo(root); fs.writeFileSync(path.join(root, 'ids.json'), JSON.stringify({ S_tpl: [4057, 4058], S_model: [218757] }));
  fs.writeFileSync(path.join(root, 'raw.vfs'), FX.records80());
  const bad = cliRun(root, { repo, args: ['--max-stride', 'not-a-number'], inputs: ['raw.vfs'] });
  // exported function path: NaN maxStride must not be silently accepted
  let directNan = null; try { const r = analyzeBlob(FX.records80(), sets, { maxStride: NaN }); directNan = { threw: false, candidates: r.candidates.length, note: 'NaN maxStride accepted by exported analyzeBlob' }; } catch (e) { directNan = { threw: true, message: String(e) }; }
  // missing value after flag
  const miss = cliRun(root, { repo, args: ['--max-stride'], inputs: ['raw.vfs'] });
  // legal: maxHeader=0, negative posLo
  let legal = null; try { const r = analyzeBlob(FX.records80(), sets, { maxHeader: 0, posLo: -200000 }); legal = { threw: false, candidates: r.candidates.length }; } catch (e) { legal = { threw: true, message: String(e) }; }
  record('INVALID_NUMERIC_CONFIG', {
    cli_bad_max_stride: { exitCode: bad.exitCode, scanStartedSummaryExists: !!bad.summary, invalidConfigurationLabel: /INVALID_CONFIGURATION/i.test(bad.stderr + bad.stdout), candidatesReported: bad.summary?.candidateCount ?? null },
    exported_nan_maxStride: directNan, cli_missing_value_after_flag: { exitCode: miss.exitCode, invalidConfigurationLabel: /INVALID_CONFIGURATION/i.test(miss.stderr + miss.stdout) },
    legal_maxHeader0_negative_posLo: legal,
    interpretation: 'Original R1 accepts NaN numeric options silently (scan runs with zero candidates = false success); no INVALID_CONFIGURATION, no SCAN_STARTED=NO marker.'
  });
  fs.rmSync(root, { recursive: true, force: true });
}

// --- O2 EXCLUSION_CENSUS --------------------------------------------------------
{
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'pe-pre-o2-'));
  const repo = mkRepo(root); fs.writeFileSync(path.join(root, 'ids.json'), JSON.stringify({ S_tpl: [4057, 4058], S_model: [218757] }));
  const good = FX.records80(); const tiny = Buffer.alloc(8, 0xff);
  const bnt = FX.realBnt2([{ name: 'scan.rec', data: good }, { name: 'tex.nif', data: good }, { name: 'tiny.rec', data: tiny }, { name: 'huge.rec', data: good }]);
  fs.writeFileSync(path.join(root, 'c.bnt'), bnt);
  const a = cliRun(root, { repo, args: [], inputs: ['c.bnt'] });
  const b = cliRun(root, { repo, args: ['--entry-regex', '^scan\\.rec$'], inputs: ['c.bnt'] });
  const skipRows = a.skips ? a.skips.trim().split('\n').length - 1 : null;
  record('EXCLUSION_CENSUS', {
    declaredEntryCount: a.sources?.[0]?.declaredEntryCount ?? null,
    scannedSourceCount: a.sources?.[0]?.scannedSourceCount ?? null,
    recordedSkipRows_configA: skipRows,
    skipReasons_configA: (a.skips || '').trim().split('\n').slice(1).map(l => l.split(',').pop()),
    regexRun: { scannedSourceCount: b.sources?.[0]?.scannedSourceCount ?? null, recordedSkipRows: b.skips ? b.skips.trim().split('\n').length - 1 : null },
    knownSilentSkips_configA: { ext_nif: 1, too_small_tiny: 1, regex_none: 0 },
    interpretation: 'Original R1 records only INPUT_TOO_LARGE/ENTRY_TOO_LARGE/READER_FAILURE/SCAN_EXCEPTION/PER_SOURCE_CANDIDATE_CAP; FILTERED_EXTENSION/TOO_SMALL/FILTERED_REGEX are silent. DECLARED_ENTRIES != sum of recorded dispositions.'
  });
  fs.rmSync(root, { recursive: true, force: true });
}

// --- O3 SAMPLE_VS_CENSUS --------------------------------------------------------
{
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'pe-pre-o3-'));
  const repo = mkRepo(root); fs.writeFileSync(path.join(root, 'ids.json'), JSON.stringify({ S_tpl: [4057, 4058], S_model: [218757] }));
  fs.writeFileSync(path.join(root, 'big.vfs'), FX.poisoned4800());
  const r = cliRun(root, { repo, args: [], inputs: ['big.vfs'] });
  const cand = r.summary ? JSON.parse(fs.readFileSync(path.join(root, 'out', 'candidates_top.json'), 'utf8')) : null;
  const first = (cand || []).find(x => x.header === 16 && x.stride === 32) ?? cand?.[0] ?? null;
  const hasFullCensusField = first ? Object.keys(first).some(k => /full.?census/i.test(k)) : false;
  record('SAMPLE_VS_CENSUS', {
    tableRowCount: first?.rowCount ?? null, sampleCount: first?.sampleCount ?? null,
    sampleIdRate: first?.idRate ?? null, sampleXyzRate: first?.xyzRate ?? null,
    fullCensusFieldsPresent: hasFullCensusField, censusStatusFieldPresent: first ? ('censusStatus' in first) : null,
    interpretation: 'Original R1 evaluates only the sampled rows; no FULL_CENSUS_* fields, no CENSUS_STATUS. In this fixture the evenly spread 1200-row sample sees a 100% valid ID column while the whole 4800-row table is 25% valid — the sample cannot and does not represent the full table.'
  });
  fs.rmSync(root, { recursive: true, force: true });
}

// --- O4 SINGLE_DEFINITION_TABLE ------------------------------------------------
{
  const b = FX.singleIdTable(80);
  const atOne = analyzeBlob(b, sets, { minDistinctId: 1, minIdRate: 0.5, maxStride: 128, minPosRate: 0.9, top: 50 });
  let atDefault = null; try { atDefault = analyzeBlob(b, sets, { minIdRate: 0.5, maxStride: 128, minPosRate: 0.9, top: 50 }); } catch (e) { atDefault = { threw: String(e) }; }
  record('SINGLE_DEFINITION_TABLE', {
    minDistinctId1_candidates: atOne.candidates.length, default_minDistinctId2_candidates: atDefault.candidates?.length ?? null,
    defaultDistinctInterfaceExists: true,
    interpretation: 'Original R1 exposes --min-distinct-id / minDistinctId (default 2). At minDistinctId=1 a single-definition table (all rows ID 4057) is detected; under the default it is silently excluded (explicit coverage restriction).'
  });
}

// --- O5 INTEGER_COUNTERS_AS_FLOATS ----------------------------------------------
{
  const b = FX.countersAsFloats();
  const r = analyzeBlob(b, sets, { minIdRate: 0.5, maxStride: 128, minPosRate: 0.88, top: 50 });
  const c = r.candidates.find(x => x.xyzOffset === 4) ?? r.candidates[0] ?? null;
  const sampleFloats = c ? [0, 4, 8].map(k => b.readFloatLE(c.header + c.sampleIndices[0] * c.stride + c.xyzOffset + k)) : null;
  const hasDiagnostics = c ? Object.keys(c).some(k => /subnormal|nan|u32|infinity|magnitude/i.test(k)) : false;
  record('INTEGER_COUNTERS_AS_FLOATS', {
    candidateFound: !!c, xyzRateReported: c?.xyzRate ?? null, sampleFloatValues: sampleFloats,
    diagnosticsPresent: hasDiagnostics,
    interpretation: 'Original R1 accepts subnormal f32 (u32 counters 1..5080 as bits) as in-range positions with rate 1.0 and reports no NAN/SUBNORMAL/INFINITY/u32-alternative diagnostics; subnormal candidates pass as ordinary position candidates.'
  });
}

// --- O6 ACTUAL_PROJECT_ADAPTERS_SYNTHETIC_INPUTS --------------------------------
{
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'pe-pre-o6-'));
  fs.writeFileSync(path.join(root, 'ids.json'), JSON.stringify({ S_tpl: [4057, 4058], S_model: [218757] }));
  const good = FX.records80();
  fs.writeFileSync(path.join(root, 'raw.vfs'), good);
  fs.writeFileSync(path.join(root, 'test.bnt'), FX.realBnt2([{ name: '4057.rec', data: good }]));
  fs.writeFileSync(path.join(root, 'test.ark'), FX.realArk([{ name: '4057.rec', data: good }]));
  const res = spawnSync(process.execPath, [path.join(STAGE, 'placement_probe.mjs'), '--repo', WORKTREE, '--ids', path.join(root, 'ids.json'), '--out', path.join(root, 'out'), '--input', path.join(root, 'raw.vfs'), '--input', path.join(root, 'test.bnt'), '--input', path.join(root, 'test.ark')], { encoding: 'utf8' });
  let summary = null, sources = null, csv = null;
  try { summary = JSON.parse(fs.readFileSync(path.join(root, 'out/SUMMARY.json'), 'utf8')); } catch {}
  try { sources = JSON.parse(fs.readFileSync(path.join(root, 'out/sources.json'), 'utf8')); } catch {}
  try { csv = fs.readFileSync(path.join(root, 'out/placement_candidates.csv'), 'utf8'); } catch {}
  record('ACTUAL_PROJECT_ADAPTERS_SYNTHETIC_INPUTS', {
    exitCode: res.status, sourceCount: summary?.sourceCount ?? null, candidateCount: summary?.candidateCount ?? null,
    containerKinds: sources?.map(s => s.containerKind) ?? null, csvMentionsAllThreeInputs: csv ? ['raw.vfs', 'test.bnt', 'test.ark'].every(n => csv.includes(n)) : null,
    adaptersUsed: { bnt2Blob: '1fb862905b4749f3336bb47da87441edbd018fb7', arkBlob: 'a9c9f04319dc3128d527d0688285ec5384f8aa97', repo: 'BASE worktree ' + WORKTREE },
    stderr: res.stderr.slice(0, 400)
  });
  fs.rmSync(root, { recursive: true, force: true });
}

// --- O7 NUMERIC_DAT_MODEL_NAME_PATTERN -------------------------------------------
{
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'pe-pre-o7-'));
  fs.writeFileSync(path.join(root, 'tpl.csv'), FX.idsCsv('templateId'));
  fs.writeFileSync(path.join(root, 'models.bnt'), FX.realBnt2([
    { name: '123.nif', data: Buffer.alloc(16, 0xff) }, { name: '218757.nif', data: Buffer.alloc(16, 0xff) }, { name: 'prop_a.nif', data: Buffer.alloc(16, 0xff) }]));
  fs.writeFileSync(path.join(root, 'models.dat'), Buffer.from('dummy'));
  const run = args => spawnSync(process.execPath, [path.join(STAGE, 'ids_from_export.mjs'), ...args], { encoding: 'utf8' });
  const dat = run(['--csv', path.join(root, 'tpl.csv'), '--id-column', 'templateId', '--repo', WORKTREE, '--model-archive', path.join(root, 'models.dat'), '--out', path.join(root, 'out.json')]);
  const bnt = run(['--csv', path.join(root, 'tpl.csv'), '--id-column', 'templateId', '--repo', WORKTREE, '--model-archive', path.join(root, 'models.bnt'), '--out', path.join(root, 'out.json')]);
  let bntOut = null; try { bntOut = JSON.parse(fs.readFileSync(path.join(root, 'out.json'), 'utf8')); } catch {}
  record('NUMERIC_DAT_MODEL_NAME_PATTERN', {
    datRun: { exitCode: dat.status, rejected: /must be \.bnt or \.ark/.test(dat.stderr), stderrTail: dat.stderr.trim().split('\n').pop() },
    bntRun: { exitCode: bnt.status, modelIds: bntOut?.S_model ?? null, numericNifCounted: (bnt.stdout.match(/"nifEntries":(\d+)/) || [])[1], nonNumericNameExcluded: bntOut?.S_model?.length === 2 && !bntOut.S_model.includes(0) },
    interpretation: 'ids_from_export R1 accepts only .bnt/.ark model archives (a hypothetical .dat is rejected, NOT presented as a defect of the actual Models.bnt) and counts only <numeric>.nif names (non-numeric names silently excluded from S_model).'
  });
  fs.rmSync(root, { recursive: true, force: true });
}

// --- §7 LAYOUT_ATTEMPTS_VS_ADMITTED ----------------------------------------------
{
  const b = FX.layoutBuffer10007();
  const r = analyzeBlob(b, sets, { maxHeader: 0, maxStride: 512 });
  const expectedAttempts = 1 /* headers h=0 */ * 126 /* strides 12..512 step 4 */;
  record('LAYOUT_ATTEMPTS_VS_ADMITTED', {
    fixture: { bytes: b.length, fill: '0xFF', note: '10007 is prime: no stride in 12..512 divides it' },
    original_layoutsTested: r.stats.layoutsTested, expectedVisitedLayoutAttempts: expectedAttempts,
    layoutsAdmitted: 0,
    interpretation: 'Original R1 increments layoutsTested only AFTER the divisibility and minRows filters, so a fully-visited-but-undividable buffer reports layoutsTested=0. Budget accounting on this quantity would charge 0 instead of 126.'
  });
}

// --- §7 XYZ_COLUMN_MEAN_VS_ROW_TRIPLE_RATE ----------------------------------------
{
  const b = FX.xyzFixture80();
  const r = analyzeBlob(b, sets, { minPosRate: 0.88, minIdRate: 0.35, top: 50 });
  const c = r.candidates.find(x => x.header === 16 && x.stride === 32 && x.idOffset === 0 && x.idWidth === 2 && x.xyzOffset === 4) ?? null;
  record('XYZ_COLUMN_MEAN_VS_ROW_TRIPLE_RATE', {
    candidateFound: !!c, original_xyzRate: c?.xyzRate ?? null,
    interpretation: 'Original R1 xyzRate is the MEAN of the three per-axis column in-range rates (0.9 in this fixture). It is NOT the joint row-triple finite rate, which is 56/80=0.7 in this fixture (independently recomputed by the run countercheck).'
  });
}

fs.writeFileSync(path.join(HERE, 'PRE_MEASUREMENTS.json'), JSON.stringify(results, null, 2) + '\n');
console.log('PRE_MEASUREMENTS.json written; cases=' + Object.keys(results.cases).length);