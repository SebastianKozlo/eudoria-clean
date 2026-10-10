// QC16 — PHASE2_EXTENT batch state JSONL census (raw-row verification of the
// 1551/17/3270/758 decode distribution).
import { readFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join, resolve } from 'node:path';
const PRIV = process.argv[2];
const PKG = resolve(process.argv[3]);
const p = join(PRIV, 'PHASE2_EXTENT', 'PCG935_NIF10_BATCH_STATE.jsonl');
const bytes = readFileSync(p);
const lines = bytes.toString('utf8').split(/\r?\n/).filter(l => l.trim());
let parseFail = 0; const status = {}; const versions = {};
const seen = new Set(); let dupes = 0;
for (const l of lines) {
  try {
    const o = JSON.parse(l);
    const s = o.status ?? o.result ?? 'UNKNOWN';
    status[s] = (status[s] || 0) + 1;
    const v = o.nifVersion ?? o.version ?? 'UNKNOWN';
    versions[v] = (versions[v] || 0) + 1;
    const n = o.name ?? o.entry ?? o.id;
    if (seen.has(n)) dupes++; else seen.add(n);
  } catch { parseFail++; }
}
const out = {
  qcStep: 'QC16_BATCH_STATE_CENSUS',
  file: p, bytes: bytes.length, sha256: createHash('sha256').update(bytes).digest('hex'),
  physicalRows: lines.length, parseFail, statusHistogram: status, versionHistogram: versions,
  distinctEntries: seen.size, duplicateEntryNames: dupes,
  claimsCheck: { rows_claimed_4838: lines.length === 4838, decoded_1551: (status['DECODED'] ?? 0) === 1551, noMesh_17: (status['DECODED_NO_MESH'] ?? status['NO_MESH'] ?? 0) === 17, failed_3270: (status['FAILED'] ?? 0) === 3270 }
};
writeFileSync(join(PKG, '00_CONTROL_INTERNAL_QC', 'QC16_BATCH_STATE_CENSUS.json'), JSON.stringify(out, null, 1));
console.log(JSON.stringify(out, null, 1).slice(0, 1200));
