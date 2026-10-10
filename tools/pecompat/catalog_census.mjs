// catalog_census.mjs — PE_CITY_ASSET_MAP_R1_20261010, phase 2 (W2, contract §2)
// Physical-file census of ONE era's Data tree: for every file — relative path,
// size, extension, era, SHA256 (streaming read — no whole-file loads), status.
// This is an INVENTORY, not a claim of format understanding (contract §2).
//
// OUTPUT POLICY: full per-file census (CSV + JSON) goes to PRIVATE_OUTPUT only
// (never the repo); stdout gets the bounded summary (counts per directory /
// extension + failures). Era label is mandatory on every record.
//
// READ_ONLY: the source tree is never written to. Failures are recorded
// honestly as FAILED with the error string — never skipped silently.

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) args[key] = true;
      else { args[key] = next; i++; }
    }
  }
  return args;
}

function sha256FileStreaming(filePath) {
  return new Promise((resolve, reject) => {
    const hash = crypto.createHash('sha256');
    const stream = fs.createReadStream(filePath, { highWaterMark: 4 * 1024 * 1024 });
    stream.on('error', reject);
    stream.on('data', (chunk) => hash.update(chunk));
    stream.on('end', () => resolve(hash.digest('hex')));
  });
}

async function walk(root, out) {
  const dirents = fs.readdirSync(root, { withFileTypes: true });
  for (const d of dirents) {
    const full = path.join(root, d.name);
    if (d.isDirectory()) await walk(full, out);
    else if (d.isFile()) out.push(full);
    // symlinks/other types: recorded as such, not followed (bounded, honest)
    else out.push(full + ' [NOT_A_REGULAR_FILE]');
  }
}

async function main() {
  const args = parseArgs(process.argv);
  const era = args.era;
  const root = args.root;
  const outDir = args['out-dir'];
  const expectedSha = args['expect-sha'] ?? null;
  if (!era || (era !== 'CD_2003' && era !== 'PCG_9_3_5')) {
    throw new Error('--era CD_2003|PCG_9_3_5 required (era labels are mandatory)');
  }
  if (!root || !fs.statSync(root).isDirectory()) throw new Error('--root <Data dir> required');
  if (!outDir || !fs.statSync(outDir).isDirectory()) throw new Error('--out-dir required');

  const t0 = Date.now();
  const files = [];
  await walk(root, files);
  files.sort();

  const records = [];
  const failures = [];
  const byTopDir = new Map();
  const byExt = new Map();
  let totalBytes = 0;
  for (let i = 0; i < files.length; i++) {
    const full = files[i];
    const rel = path.relative(root, full).split(path.sep).join('/');
    const topDir = rel.includes('/') ? rel.split('/')[0] : '.';
    const ext = path.extname(full).toLowerCase() || '(none)';
    const rec = { era, ordinal: i, relativePath: rel, sizeBytes: null, extension: ext, sha256: null, status: null, error: null };
    try {
      const st = fs.statSync(full);
      if (!st.isFile()) throw new Error('NOT_A_REGULAR_FILE');
      rec.sizeBytes = st.size;
      rec.sha256 = await sha256FileStreaming(full);
      rec.status = 'OK';
      totalBytes += st.size;
    } catch (err) {
      rec.status = 'FAILED';
      rec.error = String(err?.message ?? err).slice(0, 300);
      failures.push({ era, relativePath: rel, error: rec.error });
    }
    records.push(rec);
    byTopDir.set(topDir, (byTopDir.get(topDir) ?? 0) + 1);
    byExt.set(ext, (byExt.get(ext) ?? 0) + 1);
    // pinned single-input comparison (contract §1: mismatch blocks work on that
    // INPUT only — recorded here as a per-file finding, not a global abort)
    if (expectedSha && rec.sha256 && rec.sha256 === expectedSha.toLowerCase()) {
      rec.pinnedInputMatch = true;
    }
  }

  // full census → PRIVATE_OUTPUT only
  const stem = path.join(outDir, `${era}_FILE_CENSUS`);
  const csvLines = ['era,ordinal,relative_path,size_bytes,extension,sha256,status,error'];
  for (const r of records) {
    const err = r.error ? `"${r.error.replace(/"/g, '""')}"` : '';
    csvLines.push(`${r.era},${r.ordinal},${r.relativePath},${r.sizeBytes ?? 'UNKNOWN'},${r.extension},${r.sha256 ?? 'UNKNOWN'},${r.status},${err}`);
  }
  fs.writeFileSync(stem + '.csv', csvLines.join('\r\n') + '\r\n', 'utf8');
  fs.writeFileSync(stem + '.json', JSON.stringify({
    artifact: `${era}_FILE_CENSUS`,
    runId: 'PE_CITY_ASSET_MAP_R1_20261010',
    phase: 'METADATA_CATALOG',
    era,
    root,
    fileCount: records.length,
    totalBytes,
    records,
  }, null, 1), 'utf8');

  const summary = {
    artifact: 'FILE_CENSUS_SUMMARY',
    runId: 'PE_CITY_ASSET_MAP_R1_20261010',
    era,
    root,
    filesFound: files.length,
    filesOk: records.filter((r) => r.status === 'OK').length,
    filesFailed: failures.length,
    totalBytesOk: totalBytes,
    byTopLevelDirectory: Object.fromEntries([...byTopDir.entries()].sort()),
    byExtension: Object.fromEntries([...byExt.entries()].sort((a, b) => b[1] - a[1])),
    failures: failures.slice(0, 50),
    fullCensusPaths: { csv: stem + '.csv', json: stem + '.json' },
    elapsedMs: Date.now() - t0,
  };
  process.stdout.write(JSON.stringify(summary, null, 1) + '\n');
}

main().catch((err) => {
  console.error('[catalog_census] FATAL:', err?.stack ?? err);
  process.exitCode = 1;
});
