// PHASE 2 BEFORE-IMAGE PRESERVATION — EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927
// Binary-copies (fs.copyFileSync, byte-for-byte) the three EDIT TARGETS into
// 03_EVIDENCE/BEFORE_IMAGES/ BEFORE any edit, and proves BYTE_IDENTITY by
// size + SHA256 + full byte-compare. Any failure -> the run STOPS (no edits).
import fs from 'node:fs';
import crypto from 'node:crypto';

const REPO = 'D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean';
const PKG = REPO + '/docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927';
const TARGETS = [
  { repo: 'docs/audits/EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926/02_ANALYSIS/F03_TERRAIN_TEXTURE_SCOPE.md', copy: 'BEFORE_F03_TERRAIN_TEXTURE_SCOPE.md' },
  { repo: 'docs/audits/EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926/03_EVIDENCE/EVIDENCE_INDEX.csv', copy: 'BEFORE_EVIDENCE_INDEX.csv' },
  { repo: 'docs/audits/EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926/06_REPORT/MANIFEST_SHA256.csv', copy: 'BEFORE_MANIFEST_SHA256.csv' },
];
const sha = (b) => crypto.createHash('sha256').update(b).digest('hex').toUpperCase();

const rows = [];
for (const t of TARGETS) {
  const src = REPO + '/' + t.repo;
  const dst = PKG + '/03_EVIDENCE/BEFORE_IMAGES/' + t.copy;
  const orig = fs.readFileSync(src);
  fs.copyFileSync(src, dst); // byte-for-byte binary copy
  const copy = fs.readFileSync(dst);
  const byteIdentical = (orig.length === copy.length && Buffer.compare(orig, copy) === 0);
  rows.push({
    ORIGINAL_REPOSITORY_PATH: t.repo,
    PRESERVED_COPY_PATH: 'docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/03_EVIDENCE/BEFORE_IMAGES/' + t.copy,
    ORIGINAL_SIZE: orig.length,
    ORIGINAL_SHA256: sha(orig),
    PRESERVED_COPY_SHA256: sha(copy),
    BYTE_IDENTITY: byteIdentical ? 'YES' : 'NO',
  });
  console.log(t.copy + ': ' + orig.length + ' B | ' + sha(orig).slice(0, 16) + '... | BYTE_IDENTITY=' + (byteIdentical ? 'YES' : 'NO'));
  if (!byteIdentical) { console.log('BYTE-IDENTITY FAILURE — HARD STOP, NO EDITS'); process.exit(2); }
}

const csv = 'ORIGINAL_REPOSITORY_PATH,PRESERVED_COPY_PATH,ORIGINAL_SIZE,ORIGINAL_SHA256,PRESERVED_COPY_SHA256,BYTE_IDENTITY\n' +
  rows.map(r => [r.ORIGINAL_REPOSITORY_PATH, r.PRESERVED_COPY_PATH, r.ORIGINAL_SIZE, r.ORIGINAL_SHA256, r.PRESERVED_COPY_SHA256, r.BYTE_IDENTITY].join(',')).join('\n') + '\n';
fs.writeFileSync(PKG + '/03_EVIDENCE/BEFORE_IMAGES/BEFORE_IMAGE_METADATA.csv', csv);
console.log('BEFORE_IMAGE_METADATA.csv written; ALL THREE BYTE_IDENTITY = YES — edits authorized to proceed');
