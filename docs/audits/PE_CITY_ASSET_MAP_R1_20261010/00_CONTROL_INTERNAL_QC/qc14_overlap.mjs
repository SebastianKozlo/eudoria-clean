// QC14 — verify the skill/coverage numeric claims: same-name-both-eras overlap (2,177),
// the dual-existence examples (65678/656865), era labels in PRIMARY_MODEL_ROWS.
import { readFileSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';

const PRIV = process.argv[2];
const PKG = resolve(process.argv[3]);
const res = { qcStep: 'QC14_OVERLAP_CENSUS' };
function parseCsv(text) { const rows = []; let row = [], f = '', q = false, i = 0;
  while (i < text.length) { const c = text[i];
    if (q) { if (c === '"') { if (text[i + 1] === '"') { f += '"'; i += 2; continue; } q = false; i++; continue; } f += c; i++; continue; }
    if (c === '"') { q = true; i++; continue; }
    if (c === ',') { row.push(f); f = ''; i++; continue; }
    if (c === '\r') { i++; continue; }
    if (c === '\n') { row.push(f); rows.push(row); row = []; f = ''; i++; continue; }
    f += c; i++; }
  if (f.length || row.length) { row.push(f); rows.push(row); }
  return rows; }
const ark = parseCsv(readFileSync(join(PRIV, 'PHASE2_CATALOGS', 'CD2003_MODELS_ARK_ENTRIES.csv'), 'utf8')).slice(1).filter(r => r.length > 1);
const bnt = parseCsv(readFileSync(join(PRIV, 'PHASE2_CATALOGS', 'PCG935_MODELS_BNT_ENTRIES.csv'), 'utf8')).slice(1).filter(r => r.length > 1);
const arkNames = new Set(ark.map(r => r[2].toLowerCase()));
const bntNames = new Set(bnt.map(r => r[2].toLowerCase()));
const overlap = [...arkNames].filter(n => bntNames.has(n));
res.overlapCount = overlap.length;
res.claimed = 2177;
res.overlapOk = overlap.length === 2177;
res.dualExistenceExamples = ['65678.nif', '656865.nif'].map(n => ({ name: n, inCD2003: arkNames.has(n), inPCG935: bntNames.has(n) }));

// era labels in PRIMARY_MODEL_ROWS.json
const pmr = JSON.parse(readFileSync(join(PKG, 'PRIMARY_MODEL_ROWS.json'), 'utf8'));
res.primaryModelRowsTopKeys = Object.keys(pmr);
const rows = pmr.rows ?? pmr.primaryModels ?? pmr.models ?? [];
res.primaryRows = Array.isArray(rows) ? rows.map(r => ({ id: r.id ?? r.modelId ?? r.model, era: r.era, hasEraLabel: !!r.era, keys: Object.keys(r).slice(0, 18) })) : 'NOT-ARRAY: ' + typeof rows;
res.pmrSample = JSON.stringify(pmr).slice(0, 900);

writeFileSync(join(PKG, '00_CONTROL_INTERNAL_QC', 'QC14_OVERLAP_CENSUS.json'), JSON.stringify(res, null, 1));
console.log(JSON.stringify({ overlapCount: res.overlapCount, overlapOk: res.overlapOk, dualExistenceExamples: res.dualExistenceExamples, pmrTop: res.primaryModelRowsTopKeys, primaryRows: res.primaryRows }, null, 1).slice(0, 2200));
