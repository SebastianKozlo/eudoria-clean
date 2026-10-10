// QC1 — PE_CITY_ASSET_MAP_R1_20261010 fresh internal QC (pe-master-auditor)
// JSON validity + key-claim extraction for every report-package JSON artifact.
// READ-ONLY against originals; writes only under 00_CONTROL_INTERNAL_QC/.
import { readFileSync, readdirSync, statSync, writeFileSync } from 'node:fs';
import { join, resolve, relative } from 'node:path';
import { createHash } from 'node:crypto';

const PKG = resolve(process.argv[2]);
const OUT = join(PKG, '00_CONTROL_INTERNAL_QC');
const results = { runId: 'PE_CITY_ASSET_MAP_R1_20261010', qcStep: 'QC1_JSON_VALIDITY', files: [] };

function walk(dir) {
  const out = [];
  for (const e of readdirSync(dir)) {
    const p = join(dir, e);
    if (statSync(p).isDirectory()) { if (e !== '00_CONTROL_INTERNAL_QC') out.push(...walk(p)); }
    else out.push(p);
  }
  return out;
}

const jsonFiles = walk(PKG).filter(p => p.toLowerCase().endsWith('.json'));
for (const p of jsonFiles) {
  const rec = { file: relative(PKG, p), bytes: statSync(p).size, sha256: createHash('sha256').update(readFileSync(p)).digest('hex') };
  try {
    const obj = JSON.parse(readFileSync(p, 'utf8'));
    rec.valid = true;
    rec.topKeys = Object.keys(obj);
  } catch (e) {
    rec.valid = false;
    rec.error = String(e.message).slice(0, 200);
  }
  results.files.push(rec);
}

// CSV row counts (record-count sanity for report package CSVs)
const csvFiles = walk(PKG).filter(p => p.toLowerCase().endsWith('.csv'));
results.csvFiles = csvFiles.map(p => {
  const text = readFileSync(p, 'utf8');
  const lines = text.split(/\r?\n/);
  let lastNonEmpty = lines.length;
  while (lastNonEmpty > 0 && lines[lastNonEmpty - 1].trim() === '') lastNonEmpty--;
  return { file: relative(PKG, p), bytes: statSync(p).size, totalPhysicalLines: lines.length, lastNonEmptyLine: lastNonEmpty, header: lines[0] };
});

// Claim extraction from CATALOG_COVERAGE.json
const cov = JSON.parse(readFileSync(join(PKG, 'CATALOG_COVERAGE.json'), 'utf8'));
results.catalogCoverageClaims = {
  containerEntries: Object.fromEntries(Object.entries(cov.containerCatalogs || {}).map(([k, v]) => [k, { entries: v.entries, payloadHashed: v.payloadHashed, crc32Verified: v.crc32Verified, crc32Mismatch: v.crc32Mismatch, readFailures: v.readFailures, duplicateNames: v.duplicateNames, fullCatalogRef: v.fullCatalogRef }])),
  hasBatchDecodeDetails: !!cov.batchDecodeDetails,
  hasPrimaryModels: !!cov.primaryModels,
  hasCrossEraSearch: !!cov.crossEraSearch,
  rankings: cov.rankings ? Object.keys(cov.rankings) : null,
  coverageKeys: cov.coverage ? Object.keys(cov.coverage) : null
};
if (cov.batchDecodeDetails) results.catalogCoverageClaims.batchDecodeDetails = cov.batchDecodeDetails;
if (cov.primaryModels) results.catalogCoverageClaims.primaryModels = cov.primaryModels;
if (cov.crossEraSearch) results.catalogCoverageClaims.crossEraSearch = cov.crossEraSearch;
if (cov.coverage) results.catalogCoverageClaims.coverage = cov.coverage;
if (cov.phase3Extension) results.catalogCoverageClaims.phase3Extension = cov.phase3Extension;

// TEST_RESULTS.json claims
const tr = JSON.parse(readFileSync(join(PKG, 'TEST_RESULTS.json'), 'utf8'));
results.testResultsClaims = tr;

// PRIMARY_MODEL_ROWS.json claims
const pmr = JSON.parse(readFileSync(join(PKG, 'PRIMARY_MODEL_ROWS.json'), 'utf8'));
results.primaryModelRows = pmr;

writeFileSync(join(OUT, 'QC1_JSON_VALIDITY.json'), JSON.stringify(results, null, 1));
// console summary
const bad = results.files.filter(f => !f.valid);
console.log(`JSON files parsed: ${results.files.length}; INVALID: ${bad.length}${bad.map(b => ' ' + b.file).join('')}`);
console.log('CSV files:', JSON.stringify(results.csvFiles.map(c => ({ f: c.file, lastNonEmptyLine: c.lastNonEmptyLine })), null, 0));
