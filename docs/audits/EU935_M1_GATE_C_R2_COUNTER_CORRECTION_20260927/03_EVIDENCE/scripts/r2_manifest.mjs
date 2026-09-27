// R2 MANIFEST (computed LAST) + full re-hash verification.
import fs from 'node:fs';
import crypto from 'node:crypto';

const REPO = 'D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean';
const PKG_REL = 'docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927';
const PKG = REPO + '/' + PKG_REL;
const MANIFEST = PKG + '/06_REPORT/MANIFEST_SHA256.csv';
const sha = (p) => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');

function walk(d) {
  const out = [];
  for (const e of fs.readdirSync(d, { withFileTypes: true })) {
    const p = d + '/' + e.name;
    if (e.isDirectory()) out.push(...walk(p)); else out.push(p);
  }
  return out;
}
const files = walk(PKG).sort();
const rows = [];
for (const f of files) {
  const rel = f.replace(REPO + '/', '').replace(/\\/g, '/');
  if (rel === PKG_REL + '/06_REPORT/MANIFEST_SHA256.csv') continue; // self-excluded
  rows.push([rel, sha(f), fs.statSync(f).size]);
}
const csv = 'path,sha256,size_bytes\n' + rows.map(r => r.join(',')).join('\n') + '\n';
fs.writeFileSync(MANIFEST, csv);
console.log('R2 manifest written: ' + rows.length + ' rows (package files = ' + files.length + '; self-excluded = 1)');

// --- full re-hash verification on the final file set ---
const man = fs.readFileSync(MANIFEST, 'utf8').split('\n').filter(Boolean);
const dataRows = man.slice(1);
let stale = 0, missing = 0, ok = 0;
for (const l of dataRows) {
  const i = l.lastIndexOf(','); const j = l.lastIndexOf(',', i - 1);
  const p = l.slice(0, j), h = l.slice(j + 1, i), s = l.slice(i + 1);
  const full = REPO + '/' + p;
  if (!fs.existsSync(full)) { missing++; console.log('MISSING ' + p); continue; }
  const b = fs.readFileSync(full);
  if (sha(full) !== h || String(b.length) !== s) { stale++; console.log('STALE ' + p); } else ok++;
}
const unlisted = files.filter(f => {
  const rel = f.replace(REPO + '/', '');
  return rel !== PKG_REL + '/06_REPORT/MANIFEST_SHA256.csv' && !dataRows.some(l => l.startsWith(rel + ','));
});
console.log('RE-HASH: ok=' + ok + ' stale=' + stale + ' missing=' + missing + ' unlisted=' + unlisted.length);
console.log('MANIFEST_CENSUS_PASS=' + (rows.length === files.length - 1 && stale === 0 && missing === 0 && unlisted.length === 0));
