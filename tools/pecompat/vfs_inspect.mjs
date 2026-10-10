// vfs_inspect.mjs — PE_CITY_ASSET_MAP_R1_20261010, phase 2 (W2, contract §2)
// BOUNDED header/structure inspection of the 3 PCG_9_3_5 Parameters vfs
// files (textures.vfs / materials.vfs / templates.vfs). These are small
// (1,552 / 80,400 / 560,788 B). This is a HEADER/STRUCTURE inspection ONLY —
// NO forced full decode (contract §2); nothing here claims format
// understanding beyond what is directly measured.
//
// Measured, honestly labeled:
//   - size + SHA256 (identity re-verification at use time)
//   - first bytes hex/ASCII + the 8-byte signature ('ArkVFS02' expected per
//     pe-bnt-tdf skill: 16-byte serialization header, NOT a file container)
//   - the 8 metadata bytes after the signature (recorded raw, UNKNOWN meaning)
//   - (size - 16) divisibility by candidate record strides 4/8/16/32/64/128/
//     256/512/1024 (a FACT about possible fixed-size records — not proof)
//   - bounded printable-string census: total count, total bytes, first 100
//     strings with offsets (strings are METADATA-grade identifiers; never a
//     payload decode)
//
// Era label on every record (PCG_9_3_5). OUTPUT: one JSON per file to
// PRIVATE_OUTPUT; stdout = combined bounded summary.

import fs from 'node:fs';
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

function extractStrings(bytes, minLen = 4, maxCount = 100) {
  const strings = [];
  let start = -1;
  let total = 0, totalBytes = 0, offset = 0;
  for (let i = 0; i <= bytes.length; i++) {
    const c = i < bytes.length ? bytes[i] : 0x00;
    const printable = (c >= 0x20 && c <= 0x7e);
    if (printable) {
      if (start < 0) start = i;
    } else {
      if (start >= 0) {
        const len = i - start;
        if (len >= minLen) {
          total++; totalBytes += len;
          if (strings.length < maxCount) {
            strings.push({ offset: start, length: len, text: String.fromCharCode(...bytes.subarray(start, i)).slice(0, 120) });
          }
        }
        start = -1;
      }
    }
  }
  return { strings, totalStringCount: total, totalStringBytes: totalBytes };
}

function inspectFile(filePath, expectSha, expectSize) {
  const buf = fs.readFileSync(filePath);
  const bytes = new Uint8Array(buf);
  const sha = crypto.createHash('sha256').update(bytes).digest('hex');
  const name = filePath.split(/[\\/]/).pop();
  const dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  const signature = String.fromCharCode(...bytes.subarray(0, Math.min(8, bytes.length)));
  const meta8 = bytes.length >= 16 ? Array.from(bytes.subarray(8, 16)) : null;
  const strides = [4, 8, 16, 32, 64, 128, 256, 512, 1024];
  const divisibility = {};
  for (const s of strides) {
    const rem = (bytes.length - 16) % s;
    if (bytes.length >= 16) divisibility[`${s}`] = { exact: rem === 0, remainder: rem };
  }
  // candidate count if a fixed-stride record area followed the 16-byte header
  const candidates = {};
  for (const s of [128, 256, 512, 1024]) {
    if (bytes.length > 16 && (bytes.length - 16) % s === 0) candidates[`stride_${s}`] = (bytes.length - 16) / s;
  }
  const stringCensus = extractStrings(bytes, 4, 100);
  const rec = {
    artifact: 'VFS_BOUNDED_INSPECTION',
    runId: 'PE_CITY_ASSET_MAP_R1_20261010',
    phase: 'METADATA_CATALOG',
    era: 'PCG_9_3_5',
    path: filePath,
    fileName: name,
    sizeBytes: bytes.length,
    sha256: sha,
    identityCheck: {
      expectSha256: expectSha ?? null,
      expectSizeBytes: expectSize ?? null,
      match: (expectSha ? sha === expectSha.toLowerCase() : null),
      sizeMatch: (expectSize ? bytes.length === expectSize : null),
    },
    signature: { first8: signature, isArkVFS02: signature === 'ArkVFS02', first32Hex: Buffer.from(bytes.subarray(0, Math.min(32, bytes.length))).toString('hex') },
    headerMetaBytes8to16: meta8,
    headerMetaMeaning: 'UNKNOWN — recorded raw, not interpreted (skill: 16-byte serialization header; NOT a file container)',
    strideDivisibilityAfter16ByteHeader: divisibility,
    fixedStrideRecordCandidates: candidates,
    boundedStringCensus: {
      minLen: 4,
      totalStringCount: stringCensus.totalStringCount,
      totalStringBytes: stringCensus.totalStringBytes,
      first100: stringCensus.strings,
    },
    formatVerdict: 'BOUNDED_HEADER_INSPECTION_ONLY — no full decode attempted or claimed (contract §2); record layouts NOT established in this phase',
  };
  return rec;
}

function main() {
  const args = parseArgs(process.argv);
  const outDir = args['out-dir'];
  const inputs = [
    { p: 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Parameters\\textures.vfs', sha: 'ad8208a42184f49364b740e035673aa4d541706d11f3e2df7cdfb192d4cbd3b7', size: 1552 },
    { p: 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Parameters\\materials.vfs', sha: 'fd386e0d238da845c24da2f58f14f441ac4c7ab29fde76baca12b9db9de29650', size: 80400 },
    { p: 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Parameters\\templates.vfs', sha: 'be57818c7516f8c6c8a68df427591567dd0e5a421934ac24ada57e8261f65b77', size: 560788 },
  ];
  if (!outDir) throw new Error('--out-dir required');
  const results = [];
  for (const inp of inputs) {
    const rec = inspectFile(inp.p, inp.sha, inp.size);
    const safeName = inp.p.split(/[\\/]/).pop().replace(/\./g, '_');
    const stem = `${outDir}/PCG935_${safeName.toUpperCase()}_INSPECT`;
    fs.writeFileSync(stem + '.json', JSON.stringify(rec, null, 1), 'utf8');
    results.push({
      file: rec.fileName, sizeBytes: rec.sizeBytes, sha256: rec.sha256,
      identityMatch: rec.identityCheck.match && rec.identityCheck.sizeMatch,
      isArkVFS02: rec.signature.isArkVFS02,
      stringCount: rec.boundedStringCensus.totalStringCount,
      fixedStrideCandidates: rec.fixedStrideRecordCandidates,
      outputPath: stem + '.json',
    });
  }
  process.stdout.write(JSON.stringify({ artifact: 'VFS_INSPECTION_SUMMARY', runId: 'PE_CITY_ASSET_MAP_R1_20261010', era: 'PCG_9_3_5', results }, null, 1) + '\n');
}

main();
