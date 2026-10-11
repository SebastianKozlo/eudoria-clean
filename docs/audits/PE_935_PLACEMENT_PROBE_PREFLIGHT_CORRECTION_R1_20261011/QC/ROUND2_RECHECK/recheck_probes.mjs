// recheck_probes.mjs — ROUND 2 re-QC probes (fresh measurements by the re-QC worker).
// Read-only on the worktree: all scan outputs go to OS temp dirs; this script writes
// nothing outside its own stdout (the re-QC worker captures it into ROUND2_RECHECK).
// Probes:
//  P1  F1 original scenario: 9 raw records80 inputs, DEFAULT ceilings -> tracked peak vs 256
//  P1b F1 stress: 20 raw inputs, DEFAULT ceilings -> tracked peak vs 256
//  P2  F1 adversarial: 2 raw inputs, --budget-retained-candidates 4
//  P3  F1 adversarial: 5 raw inputs, cap 10
//  P4  F1 adversarial mixed: 3 raw + 1 container (4 entries), cap 12
//  P5  F2/F3: B3 pre-exhaustion (cap 700, two raw inputs): budgets + dispositions + skips
//  P6  F3 residual gap probe: container with 4 entries, cap 100 (exhaustion inside e0)
//  P7  F2 accounting probe: refused raw input vs containerReadBytes (line-350 charge)
//  P8  F5: live INVALID_CONFIGURATION message byte-identity vs POST B6 stored string
import fs from 'node:fs'; import path from 'node:path'; import os from 'node:os';
import { spawnSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
const WT = String.raw`D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011\workspace\eudoria-clean`;
const TOOL = path.join(WT, 'tools/placement_probe/placement_probe.mjs');
const FX = await import(pathToFileURL(path.join(WT, 'tools/placement_probe/tests/fixtures.mjs')).href);
const { analyzeBlob } = await import(pathToFileURL(TOOL).href);
const sets = { S_tpl: new Set([4057, 4058]), S_model: new Set([218757]) };
const tmp = () => fs.mkdtempSync(path.join(os.tmpdir(), 'pe-r2-'));
function mkRepo(root) {
  const repo = path.join(root, 'repo');
  fs.mkdirSync(path.join(repo, 'src/pesource'), { recursive: true });
  fs.writeFileSync(path.join(repo, 'package.json'), '{"type":"module"}');
  fs.writeFileSync(path.join(repo, 'src/pesource/Bnt2Archive.js'), FX.shimBntSrc);
  fs.writeFileSync(path.join(repo, 'src/pesource/ArkArchive.js'), FX.shimArkSrc);
  fs.writeFileSync(path.join(root, 'ids.json'), JSON.stringify({ S_tpl: [4057, 4058] }));
  return repo;
}
function cli(root, repo, inputs, args) {
  const out = path.join(root, 'out');
  const res = spawnSync(process.execPath, [TOOL, '--repo', repo, '--ids', path.join(root, 'ids.json'), '--out', out, ...inputs.flatMap(n => ['--input', path.join(root, n)]), ...args], { encoding: 'utf8' });
  let summary = null; try { summary = JSON.parse(fs.readFileSync(path.join(out, 'SUMMARY.json'), 'utf8')); } catch {}
  let skips = null; try { skips = fs.readFileSync(path.join(out, 'scan_skips.csv'), 'utf8'); } catch {}
  return { exitCode: res.status, stderr: res.stderr, summary, skips };
}
function rawInputs(root, n) { const names = []; for (let i = 0; i < n; i++) { const nm = `f${i}.vfs`; fs.writeFileSync(path.join(root, nm), FX.records80()); names.push(nm); } return names; }
const peakOf = s => ({ peak: s.budgets.used.peakRetainedCandidates, cap: s.budgets.limits.retainedCandidates, candidateCount: s.candidateCount, exhausted: s.budgets.exhausted, coverage: s.budgets.coverage, scannedBytes: s.budgets.used.scannedBytes, syntheticInputs: s.budgets.used.syntheticInputs });
const out = {};

// P1 / P1b: F1 original + stress, default ceilings
for (const n of [9, 20]) {
  const root = tmp(); try {
    const repo = mkRepo(root); const names = rawInputs(root, n);
    const r = cli(root, repo, names, []);
    out[`P1_${n}inputs_defaultCeilings`] = { ...peakOf(r.summary), exitCode: r.exitCode, peakWithinCap: r.summary.budgets.used.peakRetainedCandidates <= r.summary.budgets.limits.retainedCandidates };
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
}
// P2/P3: adversarial lowered caps, multi raw inputs
for (const [n, cap] of [[2, 4], [5, 10]]) {
  const root = tmp(); try {
    const repo = mkRepo(root); const names = rawInputs(root, n);
    const r = cli(root, repo, names, ['--budget-retained-candidates', String(cap)]);
    const disp = r.summary.exclusionCensus.map(c => c.dispositions.map(d => d.disposition));
    out[`P${n === 2 ? 2 : 3}_${n}inputs_cap${cap}`] = { ...peakOf(r.summary), dispositions: disp, peakWithinCap: r.summary.budgets.used.peakRetainedCandidates <= cap };
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
}
// P4: adversarial mixed raw + container, cap 12
{
  const root = tmp(); try {
    const repo = mkRepo(root);
    const names = rawInputs(root, 3);
    fs.writeFileSync(path.join(root, 'c.bnt'), FX.realBnt2([0, 1, 2, 3].map(i => ({ name: `e${i}.rec`, data: FX.records80() }))));
    names.push('c.bnt');
    const r = cli(root, repo, names, ['--budget-retained-candidates', '12']);
    out.P4_mixed_cap12 = { ...peakOf(r.summary), dispositions: r.summary.exclusionCensus.map(c => ({ kind: c.containerKind, declared: c.declaredEntryCount, disps: c.dispositions.map(d => d.disposition), censusOk: c.censusOk })), peakWithinCap: r.summary.budgets.used.peakRetainedCandidates <= 12 };
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
}
// P5: B3 pre-exhaustion case (cap 700) — budget charges + dispositions + skips
{
  const root = tmp(); try {
    const repo = mkRepo(root); const names = rawInputs(root, 2);
    const r = cli(root, repo, names, ['--budget-layout-evals', '700', '--max-stride', '512']);
    out.P5_preExhaustion_cap700 = {
      layoutAttempts: r.summary.budgets.used.layoutAttempts,
      scannedBytes: r.summary.budgets.used.scannedBytes,
      syntheticInputs: r.summary.budgets.used.syntheticInputs,
      predictionIfRefundImplemented: { scannedBytes: 2576, syntheticInputs: 1 },
      predictionIfChargeStands: { scannedBytes: 5152, syntheticInputs: 2 },
      dispositions: r.summary.exclusionCensus.map(c => c.dispositions.map(d => ({ d: d.disposition, detail: d.detail ?? '' }))),
      skipRows: r.skips.trim().split(/\r?\n/).filter(l => l && !l.startsWith('file,')),
      exhausted: r.summary.budgets.exhausted,
    };
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
}
// P6: F3 residual-gap probe — container with 4 entries, layout cap 100 (exhaustion inside e0)
{
  const root = tmp(); try {
    const repo = mkRepo(root);
    fs.writeFileSync(path.join(root, 'c.bnt'), FX.realBnt2([0, 1, 2, 3].map(i => ({ name: `e${i}.rec`, data: FX.records80() }))));
    const r = cli(root, repo, ['c.bnt'], ['--budget-layout-evals', '100']);
    const c = r.summary.exclusionCensus[0];
    out.P6_multientry_cap100 = {
      layoutAttempts: r.summary.budgets.used.layoutAttempts,
      declaredEntryCount: c.declaredEntryCount,
      censusOk: c.censusOk,
      dispositions: c.dispositions.map(d => ({ name: d.name, disposition: d.disposition, detail: d.detail ?? '' })),
      skipRows: r.skips.trim().split(/\r?\n/).filter(l => l && !l.startsWith('file,')),
      interpretation: 'e0 partially analyzed; e1 corrected to OVER_BUDGET; e2/e3 admitted but never analyzed — check their disposition labels',
    };
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
}
// P7: refused raw input vs containerReadBytes charge
{
  const root = tmp(); try {
    const repo = mkRepo(root); const names = rawInputs(root, 2);
    const r = cli(root, repo, names, ['--budget-scanned-bytes', '2676']); // first admitted+read, second refused BEFORE read
    out.P7_refusedRaw_containerReadBytes = {
      scannedBytes: r.summary.budgets.used.scannedBytes,
      containerReadBytes: r.summary.budgets.containerReadBytes,
      inputFileSize: 2576,
      note: 'if containerReadBytes == 5152, the refused (never-read) second input was charged to containerReadBytes at scanInput line 350',
      dispositions: r.summary.exclusionCensus.map(c => c.dispositions.map(d => d.disposition)),
    };
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
}
// P8: B6 live message byte-identity
{
  let msg = null; try { analyzeBlob(FX.records80(), sets, { budgetThresholds: { layoutEvaluations: 100001 } }); msg = 'NO_THROW'; } catch (e) { msg = e.message; }
  const stored = 'INVALID_CONFIGURATION: budgetThresholds.layoutEvaluations out of range [1, 100000] (ceiling 100000): 100001';
  out.P8_B6_message = { live: msg, byteIdenticalToPOSTstored: msg === stored, endsWithOffendingValue: msg.endsWith(': 100001'), length: msg.length };
}
console.log(JSON.stringify(out, null, 2));
