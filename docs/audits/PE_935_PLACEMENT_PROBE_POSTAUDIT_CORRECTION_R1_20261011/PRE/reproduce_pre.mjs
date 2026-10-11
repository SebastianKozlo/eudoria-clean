// reproduce_pre.mjs — PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011 (PRESERVED PRE harness)
// Factual PRE of every DA/PA defect on the UNCHANGED BASE 938aa946, measured only in
// isolated stage copies under the run's own LOCAL_RUN_ROOT/staging (never in the source
// package, never in the original kit directories).
// Adapted from the pinned Desktop post-audit reproducer adversarial_checks.mjs
// (SHA256 1548C777988C40FA4E958D8A034BB490DAC8401B9C9D81A4D5679DB6C134A28196). DOCUMENTED
// DIFF vs that file: paths point at this run's worktree/staging instead of the Desktop
// snapshot; the original kit is staged from the already-verified private ZIP extraction;
// the old SOURCE_PACKAGE POST harness is replayed from a byte-identical private copy;
// no predicates, fixtures, limits or expectations were changed.
// Outputs: PRE/BASE_TEST_RESULTS.json, PRE/BASE_POST_REPLAY.json, PRE/PRE_MEASUREMENTS.json.
import fs from 'node:fs'; import path from 'node:path'; import os from 'node:os';
import { spawnSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const arg = (k, d) => { const i = process.argv.indexOf(k); return i >= 0 ? process.argv[i + 1] : d; };
const WORKTREE = path.resolve(arg('--worktree'));
const RUNROOT = path.resolve(arg('--runroot'));
const KITDIR = path.resolve(arg('--kitdir')); // verified private ZIP extraction (7 members hash-checked below)
const STAGE = path.join(RUNROOT, 'staging'); fs.mkdirSync(STAGE, { recursive: true });
const sha = b => createHash('sha256').update(b).digest('hex');
const shaF = p => sha(fs.readFileSync(p));
const sets = { S_tpl: new Set([4057, 4058]), S_model: new Set([218757]) };
const node = process.version;
const time = () => new Date().toISOString();

// ---------- staging helpers: byte-identical copies with recorded SHA ----------
function stageTree(stageRoot, items, label) {
  const records = [];
  for (const it of items) {
    const src = path.join(WORKTREE, it), dst = path.join(stageRoot, it);
    fs.mkdirSync(path.dirname(dst), { recursive: true });
    fs.copyFileSync(src, dst);
    const a = shaF(src), b = shaF(dst);
    if (a !== b) throw Error('stage copy mismatch: ' + it);
    records.push({ path: it, sha256: a, byteIdentical: true });
  }
  return { stageRoot, label, copies: records };
}

// ---------- 1. original R1 kit from the verified private ZIP extraction ----------
const kitFiles = ['placement_probe.mjs', 'ids_from_export.mjs', 'tests/probe.test.mjs', 'tests/cli-fixture.test.mjs'];
const fileHashes = JSON.parse(fs.readFileSync(path.join(KITDIR, 'FILE_HASHES.json'), 'utf8'));
for (const m of fileHashes) {
  const p = path.join(KITDIR, m.path); const b = fs.readFileSync(p);
  const ok = b.length === m.sizeBytes && sha(b) === m.sha256;
  if (!ok) throw Error('ZIP member hash mismatch: ' + m.path);
}
const STAGE_KIT = path.join(STAGE, 'kit_r1');
for (const f of kitFiles) { fs.mkdirSync(path.dirname(path.join(STAGE_KIT, f)), { recursive: true }); fs.copyFileSync(path.join(KITDIR, f), path.join(STAGE_KIT, f)); }
fs.writeFileSync(path.join(STAGE_KIT, 'package.json'), '{"type":"module"}');
const kitStageId = { stageRoot: STAGE_KIT, source: 'PE935_Placement_Probe_Kit_R1.zip (pinned, privately extracted; 7 members verified against FILE_HASHES.json)', copies: kitFiles.map(f => ({ path: f, sha256: shaF(path.join(STAGE_KIT, f)) })) };

// ---------- 2. BASE code stage (27-suite + old POST replay) ----------
const baseToolFiles = ['tools/placement_probe/placement_probe.mjs', 'tools/placement_probe/ids_from_export.mjs', 'tools/placement_probe/tests/fixtures.mjs', 'tools/placement_probe/tests/probe.test.mjs', 'tools/placement_probe/tests/cli-fixture.test.mjs', 'tools/placement_probe/tests/budget.test.mjs', 'tools/placement_probe/tests/census_extra.test.mjs', 'tools/placement_probe/tests/correction_matrix.test.mjs', 'src/pesource/Bnt2Archive.js', 'src/pesource/ArkArchive.js'];
const STAGE_BASE = path.join(STAGE, 'stage_base');
const baseStageId = stageTree(STAGE_BASE, baseToolFiles, 'BASE_938aa946_byte_identical_copies');
const STAGE_OLDPOST = path.join(STAGE, 'stage_old_post');
const oldPostId = stageTree(STAGE_OLDPOST, baseToolFiles, 'BASE_938aa946_byte_identical_copies');
const OLD_POST_REL = 'docs/audits/PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011/POST/run_post.mjs';
fs.mkdirSync(path.join(STAGE_OLDPOST, path.dirname(OLD_POST_REL)), { recursive: true });
fs.copyFileSync(path.join(WORKTREE, OLD_POST_REL), path.join(STAGE_OLDPOST, OLD_POST_REL));
const oldPostScript = { path: OLD_POST_REL, sha256: shaF(path.join(STAGE_OLDPOST, OLD_POST_REL)), originalSha256: shaF(path.join(WORKTREE, OLD_POST_REL)), byteIdentical: shaF(path.join(STAGE_OLDPOST, OLD_POST_REL)) === shaF(path.join(WORKTREE, OLD_POST_REL)), note: 'frozen historical POST harness replayed from a private byte-identical copy; the SOURCE_PACKAGE original is READ_ONLY and untouched' };

// ---------- run node --test in a directory ----------
function runTests(cwd, files) {
  const res = spawnSync(process.execPath, ['--test', ...files], { encoding: 'utf8', cwd, timeout: 300000 });
  const m = re => Number((res.stdout.match(re) || [])[1]);
  return { exitCode: res.status, stdout: res.stdout, stderr: res.stderr, tests: m(/# tests (\d+)/), pass: m(/# pass (\d+)/), fail: m(/# fail (\d+)/) };
}

// ---------- 3. original seven (ZIP R1 kit) ----------
const ORIGINAL_SEVEN = ['CLI probes RAW, BNT2, Ark payload via locally imported compatible readers', 'discovers known synthetic record layout without treating it as historical placement', 'wrong IDs do not manufacture a template relation', 'no file/geometry source is inferred from a matching ID alone', 'missing template set is a hard error', 'truncated buffers and zero-row cases do not fabricate a pass', 'independent aligned anchors enable a joint label-position permutation control'];
const origSeven = runTests(STAGE_KIT, ['tests/probe.test.mjs', 'tests/cli-fixture.test.mjs']);
const origSevenPass = ORIGINAL_SEVEN.every(n => new RegExp('^ok \\d+ - ' + n.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '$', 'm').test(origSeven.stdout));

// ---------- 4. current 27 suite on UNCHANGED BASE ----------
const suite27 = runTests(path.join(STAGE_BASE, 'tools/placement_probe/tests'), ['probe.test.mjs', 'cli-fixture.test.mjs', 'correction_matrix.test.mjs', 'budget.test.mjs', 'census_extra.test.mjs']);

const baseTestResults = {
  runId: 'PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011', stage: 'PRESERVED_PRE', timeUtc: time(), node,
  purpose: 'factual PRE: the original kit regression and the current BASE suite status BEFORE any correction; no expectation was changed to obtain any result',
  originalKit: { stage: kitStageId, command: 'node --test tests/probe.test.mjs tests/cli-fixture.test.mjs', nodeVersion: node, codeIdentity: { kitPlacementProbe: shaF(path.join(STAGE_KIT, 'placement_probe.mjs')), probe_test: shaF(path.join(STAGE_KIT, 'tests/probe.test.mjs')), cli_fixture_test: shaF(path.join(STAGE_KIT, 'tests/cli-fixture.test.mjs')) }, exitCode: origSeven.exitCode, tests: origSeven.tests, pass: origSeven.pass, fail: origSeven.fail, originalSevenPass: origSevenPass, originalSevenNames: ORIGINAL_SEVEN, stdout: origSeven.stdout },
  baseSuite27: { stage: baseStageId, command: 'node --test probe.test.mjs cli-fixture.test.mjs correction_matrix.test.mjs budget.test.mjs census_extra.test.mjs', cwd: 'stage_base/tools/placement_probe/tests', codeIdentity: { placement_probe: shaF(path.join(STAGE_BASE, 'tools/placement_probe/placement_probe.mjs')), fixtures: shaF(path.join(STAGE_BASE, 'tools/placement_probe/tests/fixtures.mjs')) }, exitCode: suite27.exitCode, tests: suite27.tests, pass: suite27.pass, fail: suite27.fail, stdout: suite27.stdout },
};
fs.writeFileSync(path.join(HERE, 'BASE_TEST_RESULTS.json'), JSON.stringify(baseTestResults, null, 2) + '\n');

// ---------- 5. replay the historical POST battery (47 outcomes) from BASE ----------
const oldPostRun = spawnSync(process.execPath, [path.join(STAGE_OLDPOST, OLD_POST_REL)], { encoding: 'utf8', timeout: 600000 });
const oldPostMeasurements = JSON.parse(fs.readFileSync(path.join(STAGE_OLDPOST, path.dirname(OLD_POST_REL), 'POST_MEASUREMENTS.json'), 'utf8'));
const oldPostTestResults = JSON.parse(fs.readFileSync(path.join(STAGE_OLDPOST, path.dirname(OLD_POST_REL), 'POST_TEST_RESULTS.json'), 'utf8'));
const namedOutcomes = {};
for (const [id, c] of Object.entries(oldPostMeasurements.cases)) {
  if (id === 'TEST_SUITE') continue;
  if (id === 'BUDGET_BATTERY') { for (const [k, v] of Object.entries(c)) if (/^[BC]X?\d/.test(k)) namedOutcomes[k] = v.outcome; continue; }
  namedOutcomes[id] = c.outcome;
}
const basePostReplay = {
  runId: 'PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011', stage: 'PRESERVED_PRE_BASE_POST_REPLAY', timeUtc: time(), node,
  purpose: 'replay of the historical POST battery published at BASE 938aa946 (47 PASS / 0 FAIL) from a private byte-identical copy of the frozen harness against the UNCHANGED BASE code, before this run changes anything',
  stageInfo: { stage: oldPostId, postScript: oldPostScript, cwd: path.join(STAGE_OLDPOST, path.dirname(OLD_POST_REL)) },
  replay: { command: 'node run_post.mjs (private stage copy)', exitCode: oldPostRun.status, stdoutTail: String(oldPostRun.stdout).split('\n').slice(-3).join('\n'), stderr: oldPostRun.stderr },
  historicalCounters: { pass: oldPostMeasurements.generated.pass, fail: oldPostMeasurements.generated.fail, suiteTests: oldPostTestResults.testsCount, suitePass: oldPostTestResults.passCount, suiteFail: oldPostTestResults.failCount, originalSevenPass: oldPostTestResults.originalSevenPass },
  namedOutcomes, namedOutcomeCount: Object.keys(namedOutcomes).length,
  interpretation: 'The historical 47-outcome aggregate is reproducible on unchanged BASE (27 suite + 20 named battery outcomes). It is the status quo this correction run must preserve while fixing DA-1/DA-2/DA-3 and closing PA-1/PA-2.',
};
fs.writeFileSync(path.join(HERE, 'BASE_POST_REPLAY.json'), JSON.stringify(basePostReplay, null, 2) + '\n');

// ---------- 6. DA-1 PRE: false SCANNED for unvisited entries (R2-5) ----------
const TOOL_BASE = path.join(STAGE_BASE, 'tools/placement_probe/placement_probe.mjs');
const FXB = await import(pathToFileURL(path.join(STAGE_BASE, 'tools/placement_probe/tests/fixtures.mjs')).href);
const { analyzeBlob: analyzeBase, Budget: BudgetBase } = await import(pathToFileURL(TOOL_BASE).href);
const work = path.join(STAGE, 'pre_reproducers'); fs.mkdirSync(work, { recursive: true });
const idsJson = path.join(work, 'ids.json');
fs.writeFileSync(idsJson, JSON.stringify({ S_tpl: [4057, 4058], S_model: [218757] }));
function cli(tag, files, args = [], tool = TOOL_BASE, repo = WORKTREE) {
  const dir = path.join(work, tag); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  const res = spawnSync(process.execPath, [tool, '--repo', repo, '--ids', idsJson, '--out', dir, ...files.flatMap(x => ['--input', x]), ...args], { encoding: 'utf8', timeout: 120000 });
  const summary = fs.existsSync(path.join(dir, 'SUMMARY.json')) ? JSON.parse(fs.readFileSync(path.join(dir, 'SUMMARY.json'), 'utf8')) : null;
  return { exit: res.status, stdout: res.stdout, stderr: res.stderr, summary, dir };
}
const bnt4 = path.join(work, 'four_entries.bnt');
fs.writeFileSync(bnt4, FXB.realBnt2([0, 1, 2, 3].map(i => ({ name: `e${i}.rec`, data: FXB.records80() }))));
const r25 = cli('da1_r2_5', [bnt4], ['--budget-layout-evals', '100']);
const da1Census = r25.summary.exclusionCensus[0];
const DA1 = {
  case: 'DA-1 / R2-5 — SCANNED for entries whose analysis never started (external post-audit P2, confirmed here on unchanged BASE with the pinned real BASE Bnt2Archive adapter, synthetic bytes)',
  command: 'CLI --input four_entries.bnt --budget-layout-evals 100 (4 x records80; adapter src/pesource/Bnt2Archive.js from LOCAL_WORKTREE at BASE)',
  inputSha256: shaF(bnt4), adapterGitBlob: '1fb862905b4749f3336bb47da87441edbd018fb7',
  exit: r25.exit, dispositions: da1Census.dispositions, dispositionCounts: da1Census.dispositionCounts, declaredEntryCount: da1Census.declaredEntryCount,
  scannedPayloadCount: da1Census.scannedPayloadCount, censusOk: da1Census.censusOk, coverage: r25.summary.budgets.coverage,
  used: r25.summary.budgets.used, exhausted: r25.summary.budgets.exhausted,
  falseScannedForUnvisitedEntries: da1Census.dispositions.slice(2).every(x => x.disposition === 'SCANNED'),
  semanticGap: 'e0 (analysis started, cut at attempt 101), e1 (never analyzed, corrected to OVER_BUDGET by the BASE loop), e2 and e3 (never analyzed, still reported SCANNED). scannedPayloadCount=4 counts admissions+reads, not analyses; the sum reconciles (4=4) while the per-entry meaning is false.',
};

// ---------- 7. DA-3 PRE: injected Budget bypasses validation ----------
function tryAnalyze(label, fn) { let err = null, result = null; try { result = fn(); } catch (e) { err = String(e); } return { label, rejected: err !== null, error: err, effectiveLimits: result?.budget?.limits ?? null, attempts: result?.stats?.layoutAttempts ?? null }; }
const da3Cases = [
  tryAnalyze('Budget{layoutEvaluations:100001}', () => analyzeBase(FXB.layoutBuffer10007(), sets, { maxHeader: 0, budget: new BudgetBase({ layoutEvaluations: 100001 }) })),
  tryAnalyze('Budget{layoutEvaluations:NaN}', () => analyzeBase(FXB.layoutBuffer10007(), sets, { maxHeader: 0, budget: new BudgetBase({ layoutEvaluations: NaN }) })),
  tryAnalyze('Budget{retainedCandidates:512}', () => analyzeBase(FXB.layoutBuffer10007(), sets, { maxHeader: 0, budget: new BudgetBase({ retainedCandidates: 512 }) })),
  tryAnalyze('control budgetThresholds{layoutEvaluations:100001}', () => analyzeBase(FXB.layoutBuffer10007(), sets, { maxHeader: 0, budgetThresholds: { layoutEvaluations: 100001 } })),
];
const DA3 = { case: 'DA-3 — a Budget instance passed to exported analyzeBlob supplies effective limits that were never validated (external post-audit P2, confirmed on unchanged BASE)', command: 'exported analyzeBlob(..., { budget: new Budget(...) }) on the 10007B 0xFF layout fixture; only 126 attempts executed, no large scan', cases: da3Cases, control: 'the same raised value via budgetThresholds IS refused (INVALID_CONFIGURATION) — the ordinary CLI flag path works; the exported Budget path does not' };

// ---------- 8. DA-2 PRE: candidate record copies (Desktop reproducer, adapted paths) ----------
const original = fs.readFileSync(TOOL_BASE, 'utf8');
const marker1 = '        allRows.push({ ...meta, ...normalizeCandidate(c), sampleRows: coords, scanStats: data.stats });';
const marker2 = "  writeCsv(path.join(root, 'placement_candidates.csv'), csvRows, cols);";
if (original.split(marker1).length !== 2 || original.split(marker2).length !== 2) throw Error('instrumentation markers must be unique in BASE');
const injected1 = marker1 + `\n        { const obs={stage:'forwarded_copy', rank:rank.length, allRows:allRows.length, distinctObjects:new Set([...rank,...allRows]).size, trackedPeak:budget.peakRetained, limit:budget.limits.retainedCandidates}; (globalThis.__auditCopies ??= []).push(obs); }`;
const injected2 = `  fs.writeFileSync(path.join(root,'AUDIT_OBJECT_COPIES.json'),JSON.stringify({stages:globalThis.__auditCopies ?? [],serialization:{rows:rows.length,csvRows:csvRows.length,distinctObjects:new Set([...rows,...csvRows]).size,eachCopyDistinct:rows.every((r,i)=>r!==csvRows[i]),trackedPeak:budget.peakRetained,limit:budget.limits.retainedCandidates}},null,2));\n` + marker2;
const observedSource = original.replace(marker1, injected1).replace(marker2, injected2);
const observedTool = path.join(work, 'observed_placement_probe.mjs');
fs.writeFileSync(observedTool, observedSource);
const instrumentation = { adaptedFrom: 'adversarial_checks.mjs (pinned Desktop post-audit, SHA256 1548C777988C40FA4E958D8A034BB490DAC8401B9C9D81A4D5679DB6C134A28196)', documentedDiff: 'paths only (stage/worktree locations of this run); hooks, markers and predicates identical', originalSha256: sha(Buffer.from(original)), observedSha256: sha(Buffer.from(observedSource)), marker1, marker2, hookReadsCollections: 'forward: Set([...rank,...allRows]); serialization: Set([...rows,...csvRows]) — object identity via Set, not reference counting' };
const raws = []; for (let i = 0; i < 9; i++) { const f = path.join(work, `raw_${i}.vfs`); fs.writeFileSync(f, FXB.records80()); raws.push(f); }
function da2Pair(tag, files, args) {
  const un = cli(tag + '_unmodified', files, args);
  const ob = cli(tag + '_observed', files, args, observedTool);
  const details = JSON.parse(fs.readFileSync(path.join(work, tag + '_observed', 'AUDIT_OBJECT_COPIES.json'), 'utf8'));
  const compared = ['placement_candidates.csv', 'candidates_top.json', 'sources.json', 'scan_skips.csv'];
  const outputByteIdentical = Object.fromEntries(compared.map(f => [f, fs.readFileSync(path.join(work, tag + '_unmodified', f)).equals(fs.readFileSync(path.join(work, tag + '_observed', f)))]));
  return {
    exitUnmodified: un.exit, exitObserved: ob.exit,
    byteIdenticalOutputs: outputByteIdentical,
    summaryBudgetIdentical: JSON.stringify(un.summary.budgets) === JSON.stringify(ob.summary.budgets),
    stages: details.stages, serialization: details.serialization,
    trackedPeak: un.summary.budgets.used.peakRetainedCandidates, limit: un.summary.budgets.limits.retainedCandidates,
    maxForwardedDistinctObjects: Math.max(...details.stages.map(s => s.distinctObjects)),
    serializationDistinctObjects: details.serialization.distinctObjects,
    actualObjectCapExceeded: details.serialization.distinctObjects > details.serialization.limit || Math.max(...details.stages.map(s => s.distinctObjects)) > details.serialization.limit,
  };
}
const cap4 = da2Pair('cap4', raws.slice(0, 2), ['--budget-retained-candidates', '4']);
const cap256 = da2Pair('cap256', raws, []);
const DA2 = {
  case: 'DA-2 / R2-2 — MAX_RETAINED_CANDIDATES=256 does not bound simultaneously live DISTINCT candidate records (external post-audit P2, reconfirmed here on unchanged BASE with the same observer discipline)',
  instrumentation,
  cap4_twoInputs: { inputs: 2, retainedCandidatesThreshold: 4, ...cap4, expectedFromDesktopPostAudit: { tracker: 4, forwardDistinct: 8, serializationDistinct: 8 } },
  cap256_nineInputs: { inputs: 9, retainedCandidatesThreshold: 256, ...cap256, expectedFromDesktopPostAudit: { tracker: 256, forwardDistinctMax: 280, serializationDistinct: 512 } },
  semantics: 'same object in two arrays counts once; new object with same fields counts separately; CSV/JSON text, indexes, config and per-axis stats are not candidate records',
};

// ---------- 9. layout 60/61 counter semantics (BASE) ----------
const lower = analyzeBase(FXB.layoutBuffer10007(), sets, { maxHeader: 0, budgetThresholds: { layoutEvaluations: 60 } });
const LAYOUT61 = { limit: 60, layoutAttempts: lower.stats.layoutAttempts, layoutsAdmitted: lower.stats.layoutsAdmitted, exhausted: lower.stats.exhaustedKinds, note: 'BASE layoutAttempts counts the refused 61st request too; it must not be described as 61 performed layout evaluations — 60 were evaluated, 1 was refused' };

// ---------- 10. independent XYZ arithmetic (no detector helper) ----------
const bytes80 = FXB.xyzFixture80();
let perAxis = [0, 0, 0], triple = 0;
for (let i = 0; i < 80; i++) { const xyz = [0, 1, 2].map(a => bytes80.readFloatLE(16 + i * 32 + 4 + 4 * a)); xyz.forEach((x, a) => { if (Number.isFinite(x)) perAxis[a]++; }); if (xyz.every(Number.isFinite)) triple++; }
const INDEP_XYZ = { denominator: 80, perAxisFinite: perAxis, completeFiniteTriples: triple, jointRate: triple / 80, columnMean: perAxis.reduce((a, b) => a + b) / 240, fixtureSha256: sha(bytes80) };

// ---------- 11. PA-1 PRE: pinned fixture builders + production baseline on unchanged BASE ----------
function pa1A() { const b = Buffer.alloc(16 + 4800 * 32, 0xff); for (let j = 0; j < 1200; j++) { const i = Math.floor((j + 0.5) * 4800 / 1200); const p = 16 + i * 32; b.writeUInt16LE(j % 2 ? 4058 : 4057, p); [4, 8, 12].forEach((o, k) => b.writeFloatLE(j * 2 + k * 100, p + o)); } return b; }
function pa1B() { const b = pa1A(); for (let i = 0; i < 4800; i++) { if (i % 4 !== 2) b.writeUInt16LE(i % 2 ? 4058 : 4057, 16 + i * 32); } return b; }
function pa1C() { const b = pa1B(); for (let i = 0; i < 4800; i++) { if (i % 4 !== 2) [4, 8, 12].forEach((o, k) => b.writeFloatLE(i * 2 + k * 100, 16 + i * 32 + o)); } return b; }
const PINS = {
  A: { sizeBytes: 153616, sha256: '9AB2D32A1DE4DB50E0496F5364C1EE694A08D3D2B3B82A7E65B460EBB52681C7', sampleXyzFiniteRate: 1.0, fullXyzFiniteRate: 0.25, fullIdHitRate: 0.25 },
  B: { sizeBytes: 153616, sha256: '2E8520FF73690D5ED44026A568C9438CA4625ED85DA9A433169B1143B5153622', sampleXyzFiniteRate: 1.0, fullXyzFiniteRate: 0.25, fullIdHitRate: 1.0 },
  C: { sizeBytes: 153616, sha256: '20258A0CD3D93B2FD2C496AAC32F1655E7A45768450177A3F6E764B2D7EA926B', sampleXyzFiniteRate: 1.0, fullXyzFiniteRate: 1.0, fullIdHitRate: 1.0 },
};
function pa1Independent(buf, sampledSet) { // ground truth independent of the production reader/sampler
  let finiteTriples = 0, idHits = 0, sampleFinite = 0;
  for (let i = 0; i < 4800; i++) {
    const fin = [4, 8, 12].every(o => Number.isFinite(buf.readFloatLE(16 + i * 32 + o)));
    if (fin) finiteTriples++;
    if (sampledSet.has(i) && fin) sampleFinite++;
    if (buf.readUInt16LE(16 + i * 32) === 4057 || buf.readUInt16LE(16 + i * 32) === 4058) idHits++;
  }
  return { rows: 4800, finiteTriples, finiteTripleRate: finiteTriples / 4800, idHits, idRate: idHits / 4800, sampleRows: sampledSet.size, sampleFiniteTriples: sampleFinite, sampleXyzFiniteRate: sampleFinite / sampledSet.size };
}
const sampledSet = new Set(); for (let j = 0; j < 1200; j++) sampledSet.add(Math.floor((j + 0.5) * 4800 / 1200));
const PA1 = { purpose: 'regression coverage gap PA-1: the original XYZ 1200/4800 counterexample was not a named regression fixture. The three pinned fixtures are built byte-exactly here and measured on UNCHANGED BASE (they PASS on BASE — this is a coverage gap, not a demonstrated computation error; the algorithm must NOT be rewritten without a new counterexample).', builderProvenance: 'PA1-A is the exact original builder from the pinned review_counterchecks.mjs (SHA256 3BF07497F33270791999235C78A70408105E02DF2BAD4C58EFDA38CB17823D35), lines 54-60; B and C follow the contract section F byte-exact recipes', fixtures: {} };
for (const [k, fn] of [['A', pa1A], ['B', pa1B], ['C', pa1C]]) {
  const b = fn(); const id = { sizeBytes: b.length, sha256: sha(b) };
  const pinOk = id.sizeBytes === PINS[k].sizeBytes && id.sha256.toUpperCase() === PINS[k].sha256.toUpperCase();
  const ind = pa1Independent(b, sampledSet);
  const prod = analyzeBase(b, sets, { maxStride: 32, maxHeader: 16, top: 10, budgetThresholds: { fullCensusRows: 4800 } });
  const t = prod.candidates.find(c => c.header === 16 && c.stride === 32 && c.idOffset === 0 && c.idWidth === 2 && c.xyzOffset === 4);
  PA1.fixtures[k] = {
    bytes: id, pinned: PINS[k], pinMatch: pinOk, independentTruth: ind,
    production: t ? { targetFound: true, sampleRows: t.sampleCount, sampleXyzFiniteRate: t.sampleXyzFiniteRate, censusStatus: t.censusStatus, fullRows: t.fullCensusRowCount, fullXyzFiniteRate: t.fullCensusXyzFiniteRate, fullIdRate: t.fullCensusIdRate } : { targetFound: false },
    desktopRecheckReference: 'ADDITIONAL_CLAIMS_RECHECK.json (pinned input, SHA256 45024942C2D9EE77CD89F6F278B99348764BAAD12E600EC856E58FCA204B1D1C) — unchanged BASE already reproduces A/B/C',
  };
}

// ---------- 12. PA-2 PRE: the historical literal-PASS identity generator ----------
const frozenGenPath = path.join(WORKTREE, 'docs/audits/PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011/PRE/gen_pre_identity.mjs');
const frozenGen = fs.readFileSync(frozenGenPath, 'utf8');
const frozenInputId = fs.readFileSync(path.join(WORKTREE, 'docs/audits/PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011/PRE/INPUT_IDENTITIES.json'), 'utf8');
const PA2 = {
  purpose: 'PA-2: the historical PRE identity gate was NOT an effective gate',
  frozenGeneratorGitBlob: '9c57e2bc9c75e596d76cea9d8200cb31808c2719', frozenGeneratorSha256: sha(frozenGen), frozenGeneratorReadonly: true,
  literalVerdictLines: frozenGen.split('\n').map((l, i) => ({ line: i + 1, text: l.trim() })).filter(l => /verdict:\s*'PASS'/.test(l.text)),
  interpretation: "gen_pre_identity.mjs writes verdict:'PASS' as a string LITERAL at object construction — expected and measured are recorded but the verdict is never computed from a comparison; a mutated input would still be recorded with verdict PASS. The historical extra manual check is UNVERIFIED (no evidence either way about which file was historically measured); the historical measured identities in INPUT_IDENTITIES.json do match the pins, but a literal PASS proves no effective gate existed.",
  desktopMutantReference: 'ADDITIONAL_CLAIMS_RECHECK.json PA2 block — same-size-wrong-sha and wrong-size private mutants were recorded as verdict PASS by a byte-identical copy of the historical generator; the missing-file case crashed with ENOENT instead of a controlled BLOCKED verdict',
  historicalInputIdentitiesVerdictLiterals: frozenInputId.split('\n').filter(l => /"verdict"/.test(l.trim())).map(l => l.trim()),
};

const preMeasurements = {
  runId: 'PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011', tool: 'PRE_MEASUREMENTS_POSTAUDIT_CORRECTION_R1', stage: 'PRESERVED_PRE', timeUtc: time(), node,
  codeIdentity: { placement_probe_BASE: shaF(path.join(WORKTREE, 'tools/placement_probe/placement_probe.mjs')), fixtures_BASE: shaF(path.join(WORKTREE, 'tools/placement_probe/tests/fixtures.mjs')) },
  DA1_R2_5: DA1, DA2_R2_2: DA2, DA3_BUDGET_BYPASS: DA3, LAYOUT_COUNTER_SEMANTICS: LAYOUT61, INDEPENDENT_XYZ: INDEP_XYZ, PA1_REGRESSION_GAP: PA1, PA2_LITERAL_PASS_GATE: PA2,
};
fs.writeFileSync(path.join(HERE, 'PRE_MEASUREMENTS.json'), JSON.stringify(preMeasurements, null, 2) + '\n');
console.log(JSON.stringify({
  originalSeven: { exit: origSeven.exitCode, pass: origSeven.pass, fail: origSeven.fail, namesPass: origSevenPass },
  suite27: { exit: suite27.exitCode, tests: suite27.tests, pass: suite27.pass, fail: suite27.fail },
  oldPostReplay: { pass: basePostReplay.historicalCounters.pass, fail: basePostReplay.historicalCounters.fail, named: basePostReplay.namedOutcomeCount },
  da1_falseScanned: DA1.falseScannedForUnvisitedEntries, da1_scannedPayloadCount: DA1.scannedPayloadCount,
  da2_cap4: { tracker: cap4.trackedPeak, forwardDistinct: cap4.maxForwardedDistinctObjects, serializationDistinct: cap4.serializationDistinctObjects, byteIdentical: Object.values(cap4.byteIdenticalOutputs).every(Boolean) },
  da2_cap256: { tracker: cap256.trackedPeak, forwardDistinct: cap256.maxForwardedDistinctObjects, serializationDistinct: cap256.serializationDistinctObjects, byteIdentical: Object.values(cap256.byteIdenticalOutputs).every(Boolean) },
  da3_rejected: da3Cases.slice(0, 3).map(c => c.rejected), da3_controlRejected: da3Cases[3].rejected,
  pa1_pins: { A: PA1.fixtures.A.pinMatch, B: PA1.fixtures.B.pinMatch, C: PA1.fixtures.C.pinMatch },
  pa2_literalVerdictLines: PA2.literalVerdictLines.length,
}, null, 2));
