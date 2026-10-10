// QC6 — census byte sums + native run-record provenance fields.
import { readFileSync } from 'node:fs';
function csv(t) { const rows = []; let row = [], f = '', q = false, i = 0;
  while (i < t.length) { const c = t[i];
    if (q) { if (c === '"') { if (t[i + 1] === '"') { f += '"'; i += 2; continue; } q = false; i++; continue; } f += c; i++; continue; }
    if (c === '"') { q = true; i++; continue; }
    if (c === ',') { row.push(f); f = ''; i++; continue; }
    if (c === '\r') { i++; continue; }
    if (c === '\n') { row.push(f); rows.push(row); row = []; f = ''; i++; continue; }
    f += c; i++; }
  if (f.length || row.length) { row.push(f); rows.push(row); }
  return rows; }
const P = 'D:/Eudoria_Reconstruction/99_Audits/PE_CITY_ASSET_MAP_R1_20261010/PHASE2_CENSUS/';
const cd = csv(readFileSync(P + 'CD_2003_FILE_CENSUS.csv', 'utf8')).slice(1).filter(r => r.length > 1);
const pcg = csv(readFileSync(P + 'PCG_9_3_5_FILE_CENSUS.csv', 'utf8')).slice(1).filter(r => r.length > 1);
console.log('CD rows=' + cd.length + ' totalBytes=' + cd.reduce((a, r) => a + (+r[3]), 0) + ' (claimed 424407359)');
console.log('PCG rows=' + pcg.length + ' totalBytes=' + pcg.reduce((a, r) => a + (+r[3]), 0) + ' (claimed 2384417861)');
const rr = JSON.parse(readFileSync('D:/Eudoria_Reconstruction/99_Audits/PE_CITY_ASSET_MAP_R1_20261010/PHASE3_NativeControl/run_records.json', 'utf8').replace(/^\uFEFF/, ''));
console.log('RUN RECORD[0]:', JSON.stringify(rr[0], null, 1));
