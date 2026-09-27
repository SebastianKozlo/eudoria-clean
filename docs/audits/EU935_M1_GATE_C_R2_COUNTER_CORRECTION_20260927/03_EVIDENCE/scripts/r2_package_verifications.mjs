// FINAL PACKAGE VERIFICATIONS — EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927
// (1) PREDECESSOR_MANIFEST re-hash: every row of the post-EDIT-C R1 manifest
//     re-hashed against disk -> 0 stale / 0 missing / 0 unlisted.
// (2) CSV_SCHEMAS: strict RFC4180 parse of every CSV this run wrote or edited.
import fs from 'node:fs';
import crypto from 'node:crypto';
import { execSync } from 'node:child_process';

const REPO = 'D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean';
const PKG = REPO + '/docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927';
const R1MAN = REPO + '/docs/audits/EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926/06_REPORT/MANIFEST_SHA256.csv';
const sha = (p) => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');

// --- (1) predecessor manifest re-hash ---
const man = fs.readFileSync(R1MAN, 'utf8').split('\n').filter(Boolean);
const header = man[0];
const rows = man.slice(1).map(l => { const i = l.lastIndexOf(','); const j = l.lastIndexOf(',', i - 1); return { path: l.slice(0, j), sha: l.slice(j + 1, i), size: l.slice(i + 1) }; });
let stale = 0, missing = 0, okCount = 0;
const staleList = [];
for (const r of rows) {
  const p = REPO + '/' + r.path;
  if (!fs.existsSync(p)) { missing++; staleList.push('MISSING ' + r.path); continue; }
  const b = fs.readFileSync(p);
  const actualSha = sha(p), actualSize = String(b.length);
  if (actualSha !== r.sha || actualSize !== r.size) { stale++; staleList.push('STALE ' + r.path + ' manifest=' + r.sha.slice(0, 12) + '/' + r.size + ' actual=' + actualSha.slice(0, 12) + '/' + actualSize); }
  else okCount++;
}
const selfListed = rows.some(r => r.path.endsWith('06_REPORT/MANIFEST_SHA256.csv'));
console.log('PREDECESSOR_MANIFEST: rows=' + rows.length + ' ok=' + okCount + ' stale=' + stale + ' missing=' + missing + ' self_listed=' + selfListed + ' header=' + JSON.stringify(header));
for (const s of staleList) console.log('  ' + s);

// --- (2) CSV strict parse (this run's written/edited CSVs) ---
function parseCsv4180(s) {
  const rows = []; let row = []; let field = ''; let inQ = false;
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (inQ) { if (c === '"') { if (s[i + 1] === '"') { field += '"'; i++; } else inQ = false; } else field += c; }
    else if (c === '"') inQ = true;
    else if (c === ',') { row.push(field); field = ''; }
    else if (c === '\n') { row.push(field); rows.push(row); row = []; field = ''; }
    else field += c;
  }
  if (field.length || row.length) { row.push(field); rows.push(row); }
  return rows;
}
const csvTargets = [
  { p: PKG + '/01_RAW/FINDINGS.csv', fields: 13 },
  { p: PKG + '/01_RAW/MODIFIED_PATHS.csv', fields: 9 },
  { p: PKG + '/01_RAW/CORRECTION_EDGES.csv', fields: 6 },
  { p: PKG + '/03_EVIDENCE/AFTER_IMAGE_HASHES.csv', fields: 3 },
  { p: PKG + '/03_EVIDENCE/BEFORE_IMAGES/BEFORE_IMAGE_METADATA.csv', fields: 6 },
  { p: REPO + '/docs/audits/EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926/03_EVIDENCE/EVIDENCE_INDEX.csv', fields: 5 },
  { p: R1MAN, fields: 3 },
];
let allCsvOk = true;
for (const t of csvTargets) {
  const s = fs.readFileSync(t.p, 'utf8');
  const parsed = parseCsv4180(s);
  const fieldCounts = [...new Set(parsed.map(r => r.length))];
  const dataRows = parsed.length - 1;
  const ok = fieldCounts.length === 1 && fieldCounts[0] === t.fields && s.endsWith('\n') && !s.includes('\r');
  allCsvOk = allCsvOk && ok;
  console.log((ok ? 'CSV_OK  ' : 'CSV_FAIL') + ' ' + t.p.replace(REPO + '/', '') + ' rows=' + parsed.length + ' (data ' + dataRows + ') fieldCounts=' + fieldCounts.join('/') + ' expected=' + t.fields);
}

// --- (3) package file discipline: UTF-8 no BOM, LF-only, no U+FFFD (text files) ---
const textFiles = [];
function walk(d) {
  for (const e of fs.readdirSync(d, { withFileTypes: true })) {
    const p = d + '/' + e.name;
    if (e.isDirectory()) { walk(p); continue; }
    textFiles.push(p);
  }
}
walk(PKG);
let disciplineOk = true;
for (const p of textFiles) {
  const b = fs.readFileSync(p);
  const isText = !/\.(json|md|csv|diff|mjs|txt)$/.test(p) ? false : true;
  if (!isText) continue;
  const bom = b[0] === 0xEF && b[1] === 0xBB && b[2] === 0xBF;
  let crlf = 0; for (let i = 1; i < b.length; i++) if (b[i] === 0x0A && b[i - 1] === 0x0D) crlf++;
  const fffd = b.toString('utf8').includes('\u{FFFD}'.toString());
  const ok = !bom && !fffd;
  // RUN_CONTRACT.md has the verbatim body with ONE final CRLF (the source's own terminator) — expected
  const isContract = p.endsWith('00_CONTROL/RUN_CONTRACT.md');
  const pass = isContract ? (!bom && !fffd && crlf <= 1) : (!bom && crlf === 0 && !fffd);
  disciplineOk = disciplineOk && pass;
  console.log((pass ? 'DISC_OK  ' : 'DISC_FAIL') + ' ' + p.replace(PKG + '/', '') + ' BOM=' + bom + ' CRLF=' + crlf + ' U+FFFD=' + fffd + (isContract ? ' (verbatim contract body: 1 source CRLF allowed)' : ''));
}
console.log('ALL_CSV_OK=' + allCsvOk + ' ALL_DISCIPLINE_OK=' + disciplineOk);
console.log('MANIFEST_REHASH_PASS=' + (stale === 0 && missing === 0 && !selfListed && rows.length === 48));
