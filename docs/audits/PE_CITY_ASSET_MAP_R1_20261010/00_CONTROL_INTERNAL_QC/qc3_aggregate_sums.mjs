// QC3 — corrected aggregation of TEXTURE_LINK_DISPOSITIONS.csv (handles the 8-field
// comma-split rows) + verification of the private PCG935_NAME_EDGES.jsonl batch artifact.
// READ-ONLY; writes under 00_CONTROL_INTERNAL_QC/.
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { createHash } from 'node:crypto';

const PKG = resolve(process.argv[2]);
const PRIV = process.argv[3];
const out = { runId: 'PE_CITY_ASSET_MAP_R1_20261010', qcStep: 'QC3_AGGREGATE_SUMS' };

const text = readFileSync(join(PKG, 'TEXTURE_LINK_DISPOSITIONS.csv'), 'utf8');
function parseCsv(t) {
  const rows = []; let row = [], f = '', q = false, i = 0;
  while (i < t.length) { const c = t[i];
    if (q) { if (c === '"') { if (t[i+1] === '"') { f += '"'; i += 2; continue; } q = false; i++; continue; } f += c; i++; continue; }
    if (c === '"') { q = true; i++; continue; }
    if (c === ',') { row.push(f); f = ''; i++; continue; }
    if (c === '\r') { i++; continue; }
    if (c === '\n') { row.push(f); rows.push(row); row = []; f = ''; i++; continue; }
    f += c; i++; }
  if (f.length || row.length) { row.push(f); rows.push(row); }
  return rows;
}
const rows = parseCsv(text);
const data = rows.slice(1).filter(r => r.length > 1 || r[0] !== '');
let nameNotFound = 0, matRef = 0, nameFoundExact = 0, nameBaseMatch = 0, pcgAgg = 0, distinctPcg = new Set();
let splitContainerRows = 0, containerFieldSamples = new Set();
for (const r of data) {
  if (r[1] !== 'PCG_9_3_5' || !r[2].includes('aggregated')) continue;
  pcgAgg++;
  if (r.length === 8) { splitContainerRows++; containerFieldSamples.add(r[5] + '|' + r[6]); const disp = r[7]; distinctPcg.add(r[0]);
    const m1 = disp.match(/NAME_NOT_FOUND=(\d+)/); if (m1) nameNotFound += +m1[1];
    const m2 = disp.match(/MATERIAL_REFERENCE_CONFIRMED=(\d+)/); if (m2) matRef += +m2[1];
    const m3 = disp.match(/NAME_FOUND_EXACT=(\d+)/); if (m3) nameFoundExact += +m3[1];
    const m4 = disp.match(/NAME_BASE_MATCH_EXTENSION_DIFF=(\d+)/); if (m4) nameBaseMatch += +m4[1];
  }
}
out.csvAggregateSums = { pcgAggRows: pcgAgg, split8FieldRows: splitContainerRows, containerFieldVariants: [...containerFieldSamples], distinctPcgModels: distinctPcg.size, nameNotFoundSum: nameNotFound, materialRefSum: matRef, nameFoundExactSum: nameFoundExact, nameBaseMatchSum: nameBaseMatch };
out.claimsCheck = {
  claim_1551_processed: null, claim_3357_NAME_NOT_FOUND: nameNotFound === 3357,
  claim_794_material_refs: matRef === 794, claim_4151_edges: nameNotFound + matRef === 4151,
  claim_1545_models_with_edges: distinctPcg.size === 1545
};

// PCG935_NAME_EDGES.jsonl (private): re-count from raw rows
const jsonlPath = join(PRIV, 'PHASE3_PCG935_BATCH', 'PCG935_NAME_EDGES.jsonl');
if (existsSync(jsonlPath)) {
  const jl = readFileSync(jsonlPath, 'utf8').split(/\r?\n/).filter(l => l.trim());
  let parseFail = 0; const kind = {}; const models = new Set(); let textureName = 0, material = 0;
  for (const l of jl) { try { const o = JSON.parse(l); kind[o.kind || o.edgeKind || o.class || 'UNKNOWN'] = (kind[o.kind || o.edgeKind || o.class || 'UNKNOWN'] || 0) + 1; models.add(String(o.modelId ?? o.model_id ?? o.id)); if (/material/i.test(String(o.kind ?? o.edgeKind ?? o.class ?? ''))) material++; else textureName++; } catch { parseFail++; } }
  out.jsonl = { path: jsonlPath, bytes: readFileSync(jsonlPath).length, sha256: createHash('sha256').update(readFileSync(jsonlPath)).digest('hex'), physicalRows: jl.length, parseFail, kindHistogram: kind, distinctModels: models.size, textureNameRows: textureName, materialRows: material };
  // expected: 4151 rows = 3357 + 794
}
// batch summary artifact
const sumPath = join(PRIV, 'PHASE3_PCG935_BATCH', 'PCG935_NAME_BATCH_SUMMARY.json');
if (existsSync(sumPath)) out.batchSummary = JSON.parse(readFileSync(sumPath, 'utf8'));

writeFileSync(join(PKG, '00_CONTROL_INTERNAL_QC', 'QC3_AGGREGATE_SUMS.json'), JSON.stringify(out, null, 1));
console.log(JSON.stringify(out, null, 1));
