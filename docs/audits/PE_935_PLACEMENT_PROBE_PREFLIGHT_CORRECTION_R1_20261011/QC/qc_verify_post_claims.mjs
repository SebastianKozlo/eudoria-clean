// qc_verify_post_claims.mjs — fresh internal QC: re-executes the corrected tool on the
// key POST cases and compares MEASURED behavior against POST_MEASUREMENTS.json claims.
// (Q1b: POST measurements must match what the corrected code actually computes.)
// Writes only to a temp directory; reads the worktree tool read-only.
import fs from 'node:fs'; import path from 'node:path'; import os from 'node:os';
import { spawnSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
const WT = String.raw`D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011\workspace\eudoria-clean`;
const TOOL = path.join(WT, 'tools/placement_probe/placement_probe.mjs');
const FX = await import(pathToFileURL(path.join(WT, 'tools/placement_probe/tests/fixtures.mjs')).href);
const { analyzeBlob } = await import(pathToFileURL(TOOL).href);
const sets = { S_tpl: new Set([4057, 4058]), S_model: new Set([218757]) };
const R = {};

// S7a per POST: layoutAttempts=126, layoutsAdmitted=0, legacy layoutsTested=0, coverage FULL; lowered 60 -> 61 attempts, exhausted, PARTIAL
{
  const b = FX.layoutBuffer10007();
  const r = analyzeBlob(b, sets, { maxHeader: 0, maxStride: 512 });
  const r2 = analyzeBlob(b, sets, { maxHeader: 0, maxStride: 512, budgetThresholds: { layoutEvaluations: 60 } });
  R.S7a = { layoutAttempts: r.stats.layoutAttempts, layoutsAdmitted: r.stats.layoutsAdmitted, legacyLayoutsTested: r.stats.layoutsTested, coverage: r.stats.coverage,
    lowered: { layoutAttempts: r2.stats.layoutAttempts, budgetExhausted: r2.stats.budgetExhausted, coverage: r2.stats.coverage, refusal: r2.budget.refusals[0]?.kind, refusalDetail: r2.budget.refusals[0]?.detail } };
}
// S7b per POST: xyzRate 0.9 legacy; sampleStats.xyzFiniteRate 0.7; triples 56; denominator 80; perAxis 0.9/8 NaN; FULL_CENSUS 0.7/80
{
  const r = analyzeBlob(FX.xyzFixture80(), sets, { minPosRate: 0.88, minIdRate: 0.35, top: 50 });
  const c = r.candidates.find(x => x.header === 16 && x.stride === 32 && x.idOffset === 0 && x.idWidth === 2 && x.xyzOffset === 4);
  R.S7b = { found: !!c, xyzRate: c.xyzRate, sampleXyzFiniteRate: c.sampleStats.xyzFiniteRate, completeFiniteTriples: c.sampleStats.completeFiniteTriples,
    denominator: c.sampleStats.denominator, perAxisFiniteRates: c.sampleStats.perAxis.map(a => a.finiteRate), perAxisNanCounts: c.sampleStats.perAxis.map(a => a.nanCount),
    censusStatus: c.censusStatus, fullCensusXyzFiniteRate: c.fullCensusXyzFiniteRate, fullCensusRowCount: c.fullCensusRowCount, idRate: c.idRate };
}
// O1 per POST: legal maxHeader=0 headerless positive control -> 26 candidates
{
  const r = analyzeBlob(FX.records80Headerless(), sets, { maxHeader: 0, posLo: -200000, minPosRate: 0.9, minIdRate: 0.5, top: 50 });
  R.O1_legal_headerless = { candidates: r.candidates.length };
}
// O4 per POST: minDistinctId=1 -> 22 candidates all idDistinct=1; default -> 0
{
  const atOne = analyzeBlob(FX.singleIdTable(80), sets, { minDistinctId: 1, minIdRate: 0.5, maxStride: 128, minPosRate: 0.9, top: 50 });
  const atDefault = analyzeBlob(FX.singleIdTable(80), sets, { minIdRate: 0.5, maxStride: 128, minPosRate: 0.9, top: 50 });
  R.O4 = { minDistinctId1_candidates: atOne.candidates.length, allIdDistinct1: atOne.candidates.every(x => x.idDistinct === 1), default_candidates: atDefault.candidates.length };
}
// O2 census via CLI with the REAL BASE adapters (repo=WT): 4 declared, dispositions SCANNED 2 / FILTERED_EXTENSION 1 / TOO_SMALL 1
{
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'pe-qc-o2-'));
  try {
    fs.writeFileSync(path.join(root, 'ids.json'), JSON.stringify({ S_tpl: [4057, 4058] }));
    fs.writeFileSync(path.join(root, 'c.bnt'), FX.realBnt2([{ name: 'scan.rec', data: FX.records80() }, { name: 'tex.nif', data: FX.records80() }, { name: 'tiny.rec', data: Buffer.alloc(8, 0xff) }, { name: 'huge.rec', data: FX.records80() }]));
    const res = spawnSync(process.execPath, [TOOL, '--repo', WT, '--ids', path.join(root, 'ids.json'), '--out', path.join(root, 'out'), '--input', path.join(root, 'c.bnt')], { encoding: 'utf8' });
    const s = JSON.parse(fs.readFileSync(path.join(root, 'out', 'SUMMARY.json'), 'utf8'));
    const c = s.exclusionCensus[0];
    R.O2_real_adapters = { exitCode: res.status, status: s.status, declared: c.declaredEntryCount, dispositionTotal: c.dispositionTotal, censusOk: c.censusOk,
      counts: c.dispositionCounts, containers: s.sourceCount, scannedPayloads: c.scannedPayloadCount, containerReadBytes: s.budgets.containerReadBytes, controlWorkBytes: s.budgets.controlWorkBytes };
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
}
// O3 per POST (CLI, max-stride 64): sample idRate 1.0 vs fullCensusIdRate 0.25, FULL_CENSUS 4800
{
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'pe-qc-o3-'));
  try {
    fs.writeFileSync(path.join(root, 'ids.json'), JSON.stringify({ S_tpl: [4057, 4058] }));
    fs.writeFileSync(path.join(root, 'big.vfs'), FX.poisoned4800());
    const res = spawnSync(process.execPath, [TOOL, '--repo', WT, '--ids', path.join(root, 'ids.json'), '--out', path.join(root, 'out'), '--input', path.join(root, 'big.vfs'), '--max-stride', '64'], { encoding: 'utf8' });
    const top = JSON.parse(fs.readFileSync(path.join(root, 'out', 'candidates_top.json'), 'utf8'));
    const c = top.find(x => x.header === 16 && x.stride === 32 && x.idOffset === 0);
    R.O3 = { exitCode: res.status, tableRowCount: c.tableRowCount, sampledRowCount: c.sampledRowCount, sampleIdRate: c.idRate, sampleXyzFiniteRate: c.sampleXyzFiniteRate,
      censusStatus: c.censusStatus, fullCensusRowCount: c.fullCensusRowCount, fullCensusIdRate: c.fullCensusIdRate, fullCensusXyzFiniteRate: c.fullCensusXyzFiniteRate };
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
}
// RETAINED_CANDIDATES cross-input gap probe: 3 raw inputs x records80 with default top=100,
// ceiling 256 — does the tool bound the GLOBAL rows peak at 256, or can allRows exceed it?
{
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'pe-qc-ret-'));
  try {
    fs.writeFileSync(path.join(root, 'ids.json'), JSON.stringify({ S_tpl: [4057, 4058] }));
    for (const n of ['a.vfs', 'b.vfs', 'c.vfs', 'd.vfs']) fs.writeFileSync(path.join(root, n), FX.records80());
    const res = spawnSync(process.execPath, [TOOL, '--repo', WT, '--ids', path.join(root, 'ids.json'), '--out', path.join(root, 'out'),
      '--input', path.join(root, 'a.vfs'), '--input', path.join(root, 'b.vfs'), '--input', path.join(root, 'c.vfs'), '--input', path.join(root, 'd.vfs')], { encoding: 'utf8' });
    const s = JSON.parse(fs.readFileSync(path.join(root, 'out', 'SUMMARY.json'), 'utf8'));
    R.RETAINED_GAP_PROBE = { exitCode: res.status, inputs: 4, perFileRows: s.exclusionCensus.map(c => ({ input: path.basename(c.input), dispositions: c.dispositionCounts })),
      candidateCount: s.candidateCount, peakRetainedCandidates: s.budgets.used.peakRetainedCandidates, exhausted: s.budgets.exhausted, coverage: s.budgets.coverage, status: s.status };
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
}
console.log(JSON.stringify(R, null, 2));
