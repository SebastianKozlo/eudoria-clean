// QC15 — overlap examples for the finding correction.
import { readFileSync } from 'node:fs';
function csv(t) { const rows = []; let row = [], f = '', q = false, i = 0;
  while (i < t.length) { const c = t[i];
    if (q) { if (c === '"') { if (t[i + 1] === '"') { f += '"'; i += 2; continue; } q = false; i++; continue; } f += c; i++; continue; }
    if (c === '"') { q = true; i++; continue; }
    if (c === ',') { row.push(f); f = ''; i++; continue; }
    if (c === '\r') { i++; continue; }
    if (c === '\n') { row.push(f); rows.push(row); row = []; f = ''; i++; continue; }
    f += c; i++; }
  return rows; }
const ark = new Set(csv(readFileSync('D:/Eudoria_Reconstruction/99_Audits/PE_CITY_ASSET_MAP_R1_20261010/PHASE2_CATALOGS/CD2003_MODELS_ARK_ENTRIES.csv', 'utf8')).slice(1).map(r => r[2].toLowerCase()));
const bnt = csv(readFileSync('D:/Eudoria_Reconstruction/99_Audits/PE_CITY_ASSET_MAP_R1_20261010/PHASE2_CATALOGS/PCG935_MODELS_BNT_ENTRIES.csv', 'utf8')).slice(1).map(r => r[2].toLowerCase());
const ov = bnt.filter(n => ark.has(n));
console.log('overlap=' + ov.length);
console.log('first 12:', JSON.stringify(ov.slice(0, 12)));
console.log('has 656865? ark=' + ark.has('656865.nif') + ' bnt=' + bnt.includes('656865.nif'));
console.log('bnt names starting 6568:', JSON.stringify(bnt.filter(n => n.startsWith('6568')).slice(0, 8)));
console.log('ark names starting 6568:', JSON.stringify([...ark].filter(n => n.startsWith('6568')).slice(0, 8)));
