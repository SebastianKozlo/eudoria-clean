// qc_retained_gap_probe.mjs — fresh internal QC probe: does the RETAINED_CANDIDATES
// ceiling (256) strictly bound the peak of simultaneously stored candidate records
// (allRows + per-blob found) in a multi-input invocation? Each records80 input yields
// 29 candidates (measured); 9 inputs => 261 > 256 expected BEFORE the post-file check.
import fs from 'node:fs'; import path from 'node:path'; import os from 'node:os';
import { spawnSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
const WT = String.raw`D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011\workspace\eudoria-clean`;
const TOOL = path.join(WT, 'tools/placement_probe/placement_probe.mjs');
const FX = await import(pathToFileURL(path.join(WT, 'tools/placement_probe/tests/fixtures.mjs')).href);
const root = fs.mkdtempSync(path.join(os.tmpdir(), 'pe-qc-ret9-'));
try {
  fs.writeFileSync(path.join(root, 'ids.json'), JSON.stringify({ S_tpl: [4057, 4058] }));
  const inputs = [];
  for (let i = 0; i < 9; i++) { const n = `f${i}.vfs`; fs.writeFileSync(path.join(root, n), FX.records80()); inputs.push('--input', path.join(root, n)); }
  const res = spawnSync(process.execPath, [TOOL, '--repo', WT, '--ids', path.join(root, 'ids.json'), '--out', path.join(root, 'out'), ...inputs], { encoding: 'utf8' });
  const s = JSON.parse(fs.readFileSync(path.join(root, 'out', 'SUMMARY.json'), 'utf8'));
  console.log(JSON.stringify({
    exitCode: res.status, inputs: 9, candidateCount: s.candidateCount,
    peakRetainedCandidates: s.budgets.used.peakRetainedCandidates,
    ceiling: s.budgets.limits.retainedCandidates,
    exhausted: s.budgets.exhausted, coverage: s.budgets.coverage, status: s.status,
    refusals: s.budgets.refusals,
  }, null, 2));
} finally { fs.rmSync(root, { recursive: true, force: true }); }
