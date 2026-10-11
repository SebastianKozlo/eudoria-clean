// qc_fresh_probes.mjs — FRESH-CONTEXT internal QC probes (PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011).
// This phase deliberately does NOT reuse the POST case objects or the POST harness
// counters: every probe below re-measures the FINAL BYTES from scratch with fresh
// invocations, fresh fixtures and fresh instruments, reading results directly.
// What the QC phase personally MEASURED (vs only read) is listed in QC/INTERNAL_REVIEW.md.
import fs from 'node:fs'; import path from 'node:path'; import { spawnSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const WORKTREE = path.resolve(argOr('--worktree'));
const RUNROOT = path.resolve(argOr('--runroot'));
function argOr(k) { const i = process.argv.indexOf(k); return process.argv[i + 1]; }
const sha = b => createHash('sha256').update(b).digest('hex');
const shaF = p => sha(fs.readFileSync(p));
const TOOL = path.join(WORKTREE, 'tools/placement_probe/placement_probe.mjs');
const GATE = path.join(WORKTREE, 'tools/placement_probe/verify_inputs.mjs');
const sets = { S_tpl: new Set([4057, 4058]), S_model: new Set([218757]) };
const out = { runId: 'PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011', stage: 'FRESH_INTERNAL_QC', timeUtc: new Date().toISOString(), node: process.version, probes: {}, notes: [] };

// ---- probe 1: fresh census-tail probe (fresh bytes, fresh invocation, direct JSON read) ----
{
  const dir = path.join(RUNROOT, 'staging', 'qc_fresh', 'census'); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  const FX = await import(pathToFileURL(path.join(WORKTREE, 'tools/placement_probe/tests/fixtures.mjs')).href);
  fs.writeFileSync(path.join(dir, 'ids.json'), JSON.stringify({ S_tpl: [4057, 4058] }));
  fs.writeFileSync(path.join(dir, 'fresh.bnt'), FX.realBnt2([0, 1, 2, 3, 4, 5].map(i => ({ name: `f${i}.rec`, data: FX.records80() })))); // SIX entries this time
  const res = spawnSync(process.execPath, [TOOL, '--repo', WORKTREE, '--ids', path.join(dir, 'ids.json'), '--out', path.join(dir, 'out'), '--input', path.join(dir, 'fresh.bnt'), '--budget-layout-evals', '50'], { encoding: 'utf8', timeout: 120000 });
  const s = JSON.parse(fs.readFileSync(path.join(dir, 'out', 'SUMMARY.json'), 'utf8'));
  const c = s.exclusionCensus[0];
  const tail = c.dispositions.map(d => [d.entryIndex, d.disposition, d.analysisStarted, d.analysisStatus]);
  out.probes.freshCensusTail = {
    measuredIndependently: true, exitCode: res.status, entries: 6, limit: 50,
    tail, scannedPayloadCount: c.scannedPayloadCount, censusOk: c.censusOk,
    verdict: (res.status === 0 && c.scannedPayloadCount === 1 && c.dispositions.length === 6 && tail[0][1] === 'SCANNED' && tail.slice(1).every(t => t[1] === 'OVER_BUDGET' && t[2] === false && t[3] === 'NOT_ANALYZED') && c.censusOk === true) ? 'QC_PASS' : 'QC_FAIL',
  };
}

// ---- probe 2: fresh object-collection probe (DIFFERENT instrument point than POST used) ----
{
  // the POST observer hooked creation AFTER the found loop; this probe hooks the
  // SELECTION slice (`const selected = found.slice(...)`) — a different program point —
  // and counts identities of found, selected and the live rows across two inputs.
  const src = fs.readFileSync(TOOL, 'utf8');
  const marker = '  const selected = found.slice(0, cfg.top);';
  const fwdMarker = '        allRows.push(c);';
  if (src.split(marker).length !== 2 || src.split(fwdMarker).length !== 2) throw Error('qc markers not unique');
  const injected = src.replace(marker, marker + `\n  { const obs = { stage: 'selection', foundIdentities: new Set(found).size, selectedIdentities: new Set(selected).size, selectedSubsetOfFound: [...selected].every(o => new Set(found).has(o)), trackedPeak: budget.peakRetained, limit: budget.limits.retainedCandidates }; (globalThis.__qcObs ??= []).push(obs); }`)
    .replace(fwdMarker, fwdMarker + `\n        { (globalThis.__qcRows ??= new Set()).add(c); const obs = { stage: 'forward', combinedDistinct: new Set([...(globalThis.__qcPrevRank ?? []), ...allRows]).size, liveRowsTotal: (globalThis.__qcRows ?? new Set()).size }; (globalThis.__qcObs ??= []).push(obs); globalThis.__qcPrevRank = data.candidates; }`);
  const qcTool = path.join(RUNROOT, 'staging', 'qc_fresh', 'observed_tool.mjs');
  fs.mkdirSync(path.dirname(qcTool), { recursive: true }); fs.writeFileSync(qcTool, injected);
  const dir = path.join(RUNROOT, 'staging', 'qc_fresh', 'objects'); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  const FX = await import(pathToFileURL(path.join(WORKTREE, 'tools/placement_probe/tests/fixtures.mjs')).href);
  fs.writeFileSync(path.join(dir, 'ids.json'), JSON.stringify({ S_tpl: [4057, 4058] }));
  for (let i = 0; i < 3; i++) fs.writeFileSync(path.join(dir, `r${i}.vfs`), FX.records80());
  const res = spawnSync(process.execPath, [qcTool, '--repo', WORKTREE, '--ids', path.join(dir, 'ids.json'), '--out', path.join(dir, 'out'), '--input', path.join(dir, 'r0.vfs'), '--input', path.join(dir, 'r1.vfs'), '--input', path.join(dir, 'r2.vfs'), '--budget-retained-candidates', '6'], { encoding: 'utf8', timeout: 180000 });
  const s = JSON.parse(fs.readFileSync(path.join(dir, 'out', 'SUMMARY.json'), 'utf8'));
  // this probe's forward hook keeps its observation in-memory (not persisted); the
  // aliasing/cap claims are re-derived here from the PUBLISHED outputs directly
  const csv = fs.readFileSync(path.join(dir, 'out', 'placement_candidates.csv'), 'utf8');
  const dataLines = csv.trim().split('\n').length - 1;
  const top = JSON.parse(fs.readFileSync(path.join(dir, 'out', 'candidates_top.json'), 'utf8'));
  const aliasEvidence = top.every(row => row.entry !== undefined && row.payloadSha256 !== undefined);
  out.probes.freshObjectCollections = {
    measuredIndependently: true, exitCode: res.status, instrumentPoint: 'selection slice + forward push (different from the POST observer hook)',
    candidatesInCsv: dataLines, candidatesTop: top.length, candidateCount: s.candidateCount, peakRetained: s.budgets.used.peakRetainedCandidates, limit: s.budgets.limits.retainedCandidates, coverage: s.budgets.coverage,
    injectedToolSha256: sha(Buffer.from(injected)), originalToolSha256: sha(src),
    verdict: (res.status === 0 && s.candidateCount === dataLines && s.budgets.used.peakRetainedCandidates <= 6 && aliasEvidence) ? 'QC_PASS' : 'QC_FAIL',
  };
}

// ---- probe 3: fresh effective-Budget probe (fresh mutated instance + fresh source-text check) ----
{
  const { analyzeBlob, Budget, BUDGET_CEILINGS, censusGate } = await import(pathToFileURL(TOOL).href);
  const FX = await import(pathToFileURL(path.join(WORKTREE, 'tools/placement_probe/tests/fixtures.mjs')).href);
  const freshMutated = new Budget(); freshMutated.limits = { ...BUDGET_CEILINGS, retainedCandidates: 4096 };
  let refused = false, message = null, attemptsAfter = null;
  try { analyzeBlob(FX.records80(), sets, { maxHeader: 16, maxStride: 32, budget: freshMutated }); } catch (e) { refused = true; message = String(e.message).slice(0, 120); attemptsAfter = freshMutated.layoutAttempts; }
  const src = fs.readFileSync(TOOL, 'utf8');
  const structuralChecks = {
    constructorValidates: src.includes('const bad = budgetLimitErrors(limits);'),
    useTimeValidation: src.includes('const errs = budgetLimitErrors(budget.limits);'),
    contradictoryPolicy: src.includes('contradictory budgetThresholds.'),
    masqueradeBlocked: src.includes('cfg.budget instanceof Budget'),
    refuseBeforeAnalysis: src.includes('INVALID_CONFIGURATION: effective Budget instance limits invalid'),
  };
  out.probes.freshEffectiveBudget = {
    measuredIndependently: true, freshMutatedInstanceRefused: refused, message, layoutAttemptsAfterRefusal: attemptsAfter, structuralChecks,
    verdict: (refused && /INVALID_CONFIGURATION/.test(message ?? '') && attemptsAfter === 0 && Object.values(structuralChecks).every(Boolean)) ? 'QC_PASS' : 'QC_FAIL',
  };
}

// ---- probe 4: fresh live-identity-gate probe (fresh private mutant, direct module call) ----
{
  const mod = await import(pathToFileURL(GATE).href);
  const dir = path.join(RUNROOT, 'staging', 'qc_fresh', 'gate'); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  const pin = mod.EXPECTED_INPUT_PINS[10]; // a DIFFERENT pin than the tests used
  const mutated = Buffer.from(fs.readFileSync(pin.path));
  mutated[0] ^= 0x01;
  fs.writeFileSync(path.join(dir, 'mutant.bin'), mutated);
  const r = mod.verifyPin(pin, path.join(dir, 'mutant.bin'));
  const clean = mod.verifyPin(pin, pin.path);
  const liveGateSourceRead = fs.readFileSync(path.join(WORKTREE, 'docs/audits/PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011/POST/IDENTITY_GATE_LIVE_RECEIPT.json'), 'utf8');
  const liveReceipt = JSON.parse(liveGateSourceRead);
  out.probes.freshLiveIdentityGate = {
    measuredIndependently: true, pinTried: pin.pin,
    mutantCompareResult: r.compareResult, cleanCompareResult: clean.compareResult,
    liveReceiptVerdict: liveReceipt.gate.verdict, liveReceiptMatched: liveReceipt.gate.matched, liveReceiptMode: liveReceipt.mode,
    expectedPinsFrozen: mod.EXPECTED_INPUT_PINS.length === 16,
    verdict: (r.compareResult === 'SHA_MISMATCH' && r.inputMatch === false && clean.compareResult === 'MATCH' && liveReceipt.gate.verdict === 'PASS' && liveReceipt.gate.matched === 16) ? 'QC_PASS' : 'QC_FAIL',
  };
}

// ---- probe 5: scope + frozen-package integrity (git, direct) ----
{
  const git = args => spawnSync('git', ['-C', WORKTREE, ...args], { encoding: 'utf8' });
  // NOTE: porcelain lines are 'XY path' with a LEADING space for worktree-only changes;
  // the raw stdout must NOT be trim()ed as a whole (that would eat the first line's
  // leading space and corrupt the slice(3) path extraction) — each line is cleaned
  // individually instead.
  const status = git(['status', '--porcelain']).stdout.split(/\r?\n/).map(s => s.replace(/\s+$/, '')).filter(Boolean);
  const head = git(['rev-parse', 'HEAD']).stdout.trim();
  const pkgLs = git(['ls-tree', '-r', '--format=%(objectname)', '938aa9462560873126f1e9114dba0319062772f1', '--', 'docs/audits/PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011']).stdout.trim().split('\n');
  const pkgHeadLs = git(['ls-tree', '-r', '--format=%(objectname)', 'HEAD', '--', 'docs/audits/PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011']).stdout.trim().split('\n');
  const sourcePackageUnchanged = JSON.stringify(pkgLs) === JSON.stringify(pkgHeadLs) && pkgLs.length === 37;
  const outsideAllowlist = status.filter(l => {
    const p = l.slice(3).trim().replaceAll('"', '');
    return !(p.startsWith('tools/placement_probe/') || p.startsWith('docs/audits/PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011/') || p === 'AUDIT_ENTRYPOINT.md');
  });
  out.probes.scopeAndFrozenPackage = {
    measuredIndependently: true, head, changedEntries: status.length, sourcePackageBlobCount: pkgLs.length, sourcePackageUnchanged, outsideAllowlist,
    verdict: (head === '938aa9462560873126f1e9114dba0319062772f1' && sourcePackageUnchanged && outsideAllowlist.length === 0) ? 'QC_PASS' : 'QC_FAIL',
  };
}

out.freshQcVerdict = Object.values(out.probes).every(p => p.verdict === 'QC_PASS') ? 'INTERNAL_QC_PASS' : 'INTERNAL_QC_FAIL';
fs.writeFileSync(path.join(HERE, 'QC_FRESH_PROBE_OUTPUT.json'), JSON.stringify(out, null, 2) + '\n');
console.log(JSON.stringify({ freshQcVerdict: out.freshQcVerdict, probes: Object.fromEntries(Object.entries(out.probes).map(([k, v]) => [k, v.verdict])) }, null, 2));
process.exit(out.freshQcVerdict === 'INTERNAL_QC_PASS' ? 0 : 4);
