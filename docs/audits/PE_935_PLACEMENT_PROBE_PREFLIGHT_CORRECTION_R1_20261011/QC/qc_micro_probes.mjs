// qc_micro_probes.mjs — two micro-measurements for the QC gate table:
// (1) full INVALID_CONFIGURATION message for a raised budget threshold (POST B6 stores a
//     slice(0,80) truncation; compare full vs stored text);
// (2) layout attempts consumed by ONE records80 input at --max-stride 512 (default
//     maxHeader=64): 17 headers x 126 strides = 2142 — proving the B3 cap-700 stop occurs
//     during input 1, not across inputs.
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const WT = String.raw`D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011\workspace\eudoria-clean`;
const TOOL = path.join(WT, 'tools/placement_probe/placement_probe.mjs');
const FX = await import(pathToFileURL(path.join(WT, 'tools/placement_probe/tests/fixtures.mjs')).href);
const { analyzeBlob } = await import(pathToFileURL(TOOL).href);
const sets = { S_tpl: new Set([4057, 4058]), S_model: new Set([218757]) };

let fullMessage = null;
try { analyzeBlob(FX.records80(), sets, { budgetThresholds: { layoutEvaluations: 100001 } }); } catch (e) { fullMessage = e.message; }
const slice80 = fullMessage.slice(0, 80);
console.log(JSON.stringify({
  B6_fullMessage: fullMessage,
  B6_slice80_as_stored_by_run_post: slice80,
  slice80_equals_POST_stored: slice80 === 'INVALID_CONFIGURATION: budgetThresholds.layoutEvaluations out of range [1, 10000',
  S7_oneInput_layoutAttempts: analyzeBlob(FX.records80(), sets, { maxStride: 512 }).stats.layoutAttempts,
  headers: 17, strides: 126, product: 17 * 126,
}, null, 2));
