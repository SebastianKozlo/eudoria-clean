// bnt_index.mjs — PE_CITY_ASSET_MAP_R1_20261010, phase 2 (W2, contract §2)
// FULL entry catalog of ONE PCG_9_3_5 BNT2 container (Models.bnt / Textures.bnt).
//
// REUSE LABEL: the BNT2 footer/directory reader is src/pesource/Bnt2Archive.js
// — the base repo's era-validated reader (BNT2 footer magic + [u32 count][name
// LF-terminated][size][offset][crc32][pad] entries + exact directory-end
// check; used for Models.bnt entry 781 '218757.nif' in the SceneIR run and
// canon-validated for Textures.bnt payloads 1:1 in M3-2-R1). IMPORTED and used
// UNCHANGED. Any layout deviation of Textures.bnt would surface as a reader
// error — recorded honestly (contract: "if its layout differs, record the
// difference").
//
// NEW in this tool (bounded verification on top of the reused reader):
//   1. Per-entry CRC32 verification (computed vs stored; the directory's
//      trailing pad field is recorded and checked against the skill claim
//      "CRC32 stored twice" — pad==crc32 per entry is measured, not assumed).
//   2. Per-entry payload SHA256 (full extract-and-hash — catalog integrity).
//   3. Payload-region boundary checks: every [offset, offset+size) inside
//      [0, dirOffset); offsets monotonic? overlaps/gaps measured as FACTS
//      (never assumed contiguous).
//   4. Duplicate names counted (loud finding).
//   5. Bounded header sniff (catalog_sniff.mjs) — NIF/DDS/TGA classification;
//      for Models.bnt the NIF version distribution is RE-DERIVED here (the
//      predecessor's 5,596 = 4,838 + 757 + 1 census is COMPARISON evidence
//      only — this run's numbers are measured by this executor).
//
// Container identity fail-closed per input (--expect-sha/--expect-size).
//
// OUTPUT POLICY: full per-entry catalog (CSV + JSON) → PRIVATE_OUTPUT only;
// stdout = bounded summary. Era label on every record (PCG_9_3_5).

import fs from 'node:fs';
import crypto from 'node:crypto';
import { Bnt2Archive } from '../../src/pesource/Bnt2Archive.js';
import { sniffPayload } from './catalog_sniff.mjs';

const CRC_TABLE = (() => {
  const t = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = (c & 1) ? (0xedb88320 ^ (c >>> 1)) : (c >>> 1);
    t[n] = c >>> 0;
  }
  return t;
})();
function crc32(bytes) {
  let c = 0xffffffff;
  for (let i = 0; i < bytes.length; i++) c = CRC_TABLE[(c ^ bytes[i]) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}

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

async function main() {
  const args = parseArgs(process.argv);
  const bntPath = args.bnt;
  const outDir = args['out-dir'];
  const expectSha = args['expect-sha'] ?? null;
  const expectSize = args['expect-size'] ? parseInt(args['expect-size'], 10) : null;
  const skipPayloadHash = !!args['skip-payload-hash'];
  if (!bntPath || !outDir) throw new Error('--bnt <path> --out-dir <dir> required');

  const t0 = Date.now();
  const buf = fs.readFileSync(bntPath);
  const bytes = new Uint8Array(buf);
  const containerSha = crypto.createHash('sha256').update(bytes).digest('hex');
  if (expectSize != null && bytes.length !== expectSize) {
    throw new Error(`[bnt_index] container size ${bytes.length} != expected ${expectSize} — BLOCKED for this input`);
  }
  if (expectSha && containerSha !== expectSha.toLowerCase()) {
    throw new Error(`[bnt_index] container SHA256 ${containerSha} != expected ${expectSha} — BLOCKED for this input`);
  }

  const dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  const arch = new Bnt2Archive(bytes); // reuse: footer magic + dirOffset + count
  const entries = arch.entries();      // reuse: full dir parse + exact end check

  // per-entry pad field (the directory row is [size][offset][crc32][pad]) —
  // recorded to test the "CRC32 stored twice" skill claim as a MEASURED fact.
  const padValues = [];
  let p = arch.dirOffset + 4;
  const nameRows = [];
  for (let i = 0; i < arch.count; i++) {
    let q = p;
    while (bytes[q] !== 0x0a) q++;
    const nameLen = q - p;
    const crcOff = p + nameLen + 1 + 8; // name + 0x0A + size(4) + offset(4) → crc32
    const pad = dv.getUint32(crcOff + 4, true);
    padValues.push(pad);
    nameRows.push({ nameLen, pad });
    p = q + 1 + 16;
  }
  const padEqualsCrcCount = entries.filter((e, i) => (padValues[i] >>> 0) === (e.crc32 >>> 0)).length;

  // payload-region boundary analysis (facts, not assumptions)
  const sorted = [...entries].sort((a, b) => a.offset - b.offset);
  let overlaps = 0, gaps = 0, monotonic = true;
  let prevEnd = 0;
  const overlapSamples = [];
  for (const e of sorted) {
    if (e.offset < prevEnd) { overlaps++; if (overlapSamples.length < 5) overlapSamples.push({ name: e.name, offset: e.offset, prevEnd }); }
    else if (e.offset > prevEnd) gaps++;
    prevEnd = Math.max(prevEnd, e.offset + e.size);
  }
  for (let i = 1; i < entries.length; i++) if (entries[i].offset < entries[i - 1].offset) { monotonic = false; break; }
  const beyondDir = entries.filter((e) => e.offset + e.size > arch.dirOffset);
  const beyondEof = entries.filter((e) => e.offset + e.size > bytes.length - 8);

  // per-entry catalog
  const records = [];
  let hashed = 0, crcVerified = 0, crcMismatched = 0, readFailures = 0;
  const dupNames = new Map();
  for (let i = 0; i < entries.length; i++) {
    const e = entries[i];
    const nameCount = dupNames.get(e.name) ?? 0;
    dupNames.set(e.name, nameCount + 1);
    const rec = {
      era: 'PCG_9_3_5',
      entryIndex: e.entryIndex,
      name: e.name,
      offset: e.offset,
      storedSize: e.size,
      uncompressedSize: e.size, // BNT2 payloads are RAW 1:1 (reader-validated lineage); no decompression step exists
      compression: 'NONE_RAW',
      crc32Stored: e.crc32,
      crc32PadField: padValues[i],
      padEqualsCrc: (padValues[i] >>> 0) === (e.crc32 >>> 0),
      crc32Computed: null,
      crc32Match: null,
      payloadSha256: null,
      sniff: null,
      status: 'OK',
      error: null,
    };
    try {
      const { payload } = arch.readEntry(e); // reuse: EOF bounds enforced
      rec.crc32Computed = crc32(payload);
      rec.crc32Match = rec.crc32Computed === (e.crc32 >>> 0);
      if (rec.crc32Match) crcVerified++; else crcMismatched++;
      if (!skipPayloadHash) {
        rec.payloadSha256 = crypto.createHash('sha256').update(payload).digest('hex');
        hashed++;
      }
      rec.sniff = sniffPayload(payload);
    } catch (err) {
      rec.status = 'FAILED';
      rec.error = String(err?.message ?? err).slice(0, 300);
      readFailures++;
    }
    records.push(rec);
  }
  const duplicateNames = [...dupNames.entries()].filter(([, n]) => n > 1)
    .map(([name, n]) => ({ name, count: n }));

  const base = (args.label ?? bntPath.split(/[\\/]/).pop()).replace(/\.bnt$/i, '');
  const stem = `${outDir}/PCG935_${base.toUpperCase()}_ENTRIES`;
  const csvLines = ['era,entry_index,name,offset,size_bytes,compression,crc32_stored,crc32_pad,crc32_pad_equals_crc,crc32_computed,crc32_match,payload_sha256,sniff_class,nif_engine,nif_version,tga_width,tga_height,tga_bpp,first8_hex,status,error'];
  for (const r of records) {
    const s = r.sniff ?? {};
    csvLines.push([
      r.era, r.entryIndex, r.name, r.offset, r.storedSize, r.compression,
      r.crc32Stored, r.crc32PadField, r.padEqualsCrc, r.crc32Computed ?? 'UNKNOWN', r.crc32Match ?? 'UNKNOWN',
      r.payloadSha256 ?? 'UNKNOWN', s.sniffClass ?? 'UNKNOWN', s.nifEngine ?? '', s.nifVersion ?? '',
      s.tgaWidth ?? '', s.tgaHeight ?? '', s.tgaBpp ?? '', s.first8Hex ?? '', r.status,
      (r.error ?? '').replace(/"/g, '""') ? `"${(r.error ?? '').replace(/"/g, '""')}"` : '',
    ].join(','));
  }
  fs.writeFileSync(stem + '.csv', csvLines.join('\r\n') + '\r\n', 'utf8');
  fs.writeFileSync(stem + '.json', JSON.stringify({
    artifact: `PCG935_${base.toUpperCase()}_ENTRIES`,
    runId: 'PE_CITY_ASSET_MAP_R1_20261010',
    phase: 'METADATA_CATALOG',
    era: 'PCG_9_3_5',
    container: { path: bntPath, sizeBytes: bytes.length, sha256: containerSha },
    readerReuse: 'src/pesource/Bnt2Archive.js (era-validated BNT2 reader, imported unchanged)',
    entryCount: entries.length,
    records,
  }, null, 1), 'utf8');

  const sniffDist = new Map();
  const nifVerDist = new Map();
  const tgaDimDist = new Map();
  const extDist = new Map();
  for (const r of records) {
    const s = r.sniff ?? { sniffClass: 'NO_SNIFF' };
    sniffDist.set(s.sniffClass, (sniffDist.get(s.sniffClass) ?? 0) + 1);
    if (s.nifVersion) nifVerDist.set(`${s.nifEngine} ${s.nifVersion}`, (nifVerDist.get(`${s.nifEngine} ${s.nifVersion}`) ?? 0) + 1);
    if (s.sniffClass === 'TGA_HEADER') {
      const k = `${s.tgaWidth}x${s.tgaHeight}@${s.tgaBpp}`;
      tgaDimDist.set(k, (tgaDimDist.get(k) ?? 0) + 1);
    }
    const dot = r.name.lastIndexOf('.');
    extDist.set(dot >= 0 ? r.name.slice(dot).toLowerCase() : '(none)', (extDist.get(dot >= 0 ? r.name.slice(dot).toLowerCase() : '(none)') ?? 0) + 1);
  }

  const summary = {
    artifact: 'BNT2_ENTRY_CATALOG_SUMMARY',
    runId: 'PE_CITY_ASSET_MAP_R1_20261010',
    phase: 'METADATA_CATALOG',
    era: 'PCG_9_3_5',
    container: { path: bntPath, sizeBytes: bytes.length, sha256: containerSha },
    formatVerdict: 'BNT2 footer magic verified by the reused reader; full directory parsed to exact end (reader would throw otherwise)',
    entryCount: entries.length,
    dirOffset: arch.dirOffset,
    padEqualsCrc32: { padEqualsCrcCount, total: entries.length, claim: 'skill: CRC32 stored twice per entry', verdict: padEqualsCrcCount === entries.length ? 'MEASURED_CONFIRMED' : `MEASURED_PARTIAL (${padEqualsCrcCount}/${entries.length})` },
    payloadRegion: {
      overlaps, gaps, monotonicOffsets: monotonic,
      entriesBeyondDirectory: beyondDir.length,
      entriesBeyondEof: beyondEof.length,
      overlapSamples,
    },
    payloadHashedCount: hashed,
    crcVerifiedCount: crcVerified,
    crcMismatchCount: crcMismatched,
    readFailures,
    duplicateNames,
    entryNameExtensionDistribution: Object.fromEntries([...extDist.entries()].sort((a, b) => b[1] - a[1])),
    sniffClassDistribution: Object.fromEntries([...sniffDist.entries()].sort()),
    nifVersionDistribution: Object.fromEntries([...nifVerDist.entries()].sort((a, b) => b[1] - a[1])),
    tgaDimensionDistribution: Object.fromEntries([...tgaDimDist.entries()].sort((a, b) => b[1] - a[1]).slice(0, 20)),
    fullCatalogPaths: { csv: stem + '.csv', json: stem + '.json' },
    elapsedMs: Date.now() - t0,
  };
  process.stdout.write(JSON.stringify(summary, null, 1) + '\n');
}

main().catch((err) => {
  console.error('[bnt_index] FATAL:', err?.stack ?? err);
  process.exitCode = 1;
});
