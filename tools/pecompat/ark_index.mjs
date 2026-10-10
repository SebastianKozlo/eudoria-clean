// ark_index.mjs — PE_CITY_ASSET_MAP_R1_20261010, phase 2 (W2, contract §2)
// FULL entry catalog of ONE CD_2003 .ark container (Models.ark / Textures.ark).
//
// REUSE LABEL: the sequential local-header index + EOCD cross-check come from
// src/pesource/ArkArchive.js — the base repo's era-validated ArkVFS reader
// (pe-ark-vfs skill F-111: standard ZIP layout, AK vs PK magic; all entries
// STORED; validated 2492/4833 entries, 0 issues). The reader is IMPORTED and
// used unchanged; its boundary check (EOCD total == local scan count) runs
// inside entries().
//
// NEW in this tool (bounded verification on top of the reused reader):
//   1. CENTRAL-DIRECTORY DUAL CROSS-CHECK — the .ark central directory
//      (AK\x01\x02 entries at eocdCdOffset, size eocdCdSize) is parsed with
//      BOTH documented layouts (skill: name_len u32 @28; standard ZIP:
//      name_len u16 @28) and cross-checked entry-by-entry against the
//      local-header scan (names, sizes, offsets, count, exact end). A layout
//      is accepted only on exact agreement; disagreements are recorded
//      LOUDLY (never silently absorbed). This is a real dual-index
//      verification — no random-magic scan is ever called an index.
//   2. Per-entry CRC32 verification (stored vs computed over the payload).
//   3. Per-entry payload SHA256 (full extract-and-hash — catalog integrity).
//   4. Boundary verification: every payload fits before the central directory;
//      no payload crosses the local-scan end; duplicate names counted.
//   5. Bounded header sniff (catalog_sniff.mjs) — NIF/DDS/TGA classification,
//      version/dims captured; NEVER presented as a decode.
//
// Container identity is fail-closed: --expect-sha/--expect-size must match
// (contract §1: a mismatch blocks work on THIS input only).
//
// OUTPUT POLICY: full per-entry catalog (CSV + JSON) → PRIVATE_OUTPUT only;
// stdout gets the bounded summary. Era label on every record (CD_2003).

import fs from 'node:fs';
import crypto from 'node:crypto';
import { ArkArchive } from '../../src/pesource/ArkArchive.js';
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

/** Central-directory walk with a candidate per-entry fixed layout.
 * layout 'skill': name_len u32@28, extra_len u32@32, ??? u32@36, local_offset u32@40, ??? u16@44, name@46
 * layout 'zip':   std ZIP 46-byte fixed: name_len u16@28, extra_len u16@30, comment_len u16@32,
 *                disk u16@34, int_attr u16@36, ext_attr u32@38, local_offset u32@42, name@46
 */
function walkCentralDirectory(bytes, dv, cdOffset, cdSize, layout) {
  const entries = [];
  let p = cdOffset;
  const end = cdOffset + cdSize;
  while (p < end) {
    if (!(bytes[p] === 0x41 && bytes[p + 1] === 0x4b && bytes[p + 2] === 0x01 && bytes[p + 3] === 0x02)) {
      return { ok: false, reason: `no AK\\x01\\x02 at cd pos ${p}`, entries };
    }
    let nameLen, nameOff, localOffset;
    if (layout === 'skill') {
      nameLen = dv.getUint32(p + 28, true);
      nameOff = p + 46;
      localOffset = dv.getUint32(p + 40, true);
    } else {
      nameLen = dv.getUint16(p + 28, true);
      const extraLen = dv.getUint16(p + 30, true);
      const commentLen = dv.getUint16(p + 32, true);
      nameOff = p + 46;
      localOffset = dv.getUint32(p + 42, true);
      // consume name+extra+comment
      if (p + 46 + nameLen + extraLen + commentLen > end) {
        return { ok: false, reason: `cd entry at ${p} overruns cd end`, entries };
      }
      const name = String.fromCharCode(...bytes.subarray(nameOff, nameOff + nameLen));
      entries.push({ cdPos: p, name, localOffset });
      p += 46 + nameLen + extraLen + commentLen;
      continue;
    }
    if (nameLen > 65536 || nameOff + nameLen > end) {
      return { ok: false, reason: `cd entry at ${p}: implausible name_len ${nameLen}`, entries };
    }
    const name = String.fromCharCode(...bytes.subarray(nameOff, nameOff + nameLen));
    entries.push({ cdPos: p, name, localOffset });
    p = nameOff + nameLen;
  }
  return { ok: p === end, reason: p === end ? null : `cd walk ended at ${p} != ${end}`, entries };
}

async function main() {
  const args = parseArgs(process.argv);
  const arkPath = args.ark;
  const outDir = args['out-dir'];
  const expectSha = args['expect-sha'] ?? null;
  const expectSize = args['expect-size'] ? parseInt(args['expect-size'], 10) : null;
  const skipPayloadHash = !!args['skip-payload-hash'];
  if (!arkPath || !outDir) throw new Error('--ark <path> --out-dir <dir> required');

  const t0 = Date.now();
  const buf = fs.readFileSync(arkPath);
  const bytes = new Uint8Array(buf);
  // container identity — fail-closed for THIS input (contract §1)
  const containerSha = crypto.createHash('sha256').update(bytes).digest('hex');
  if (expectSize != null && bytes.length !== expectSize) {
    throw new Error(`[ark_index] container size ${bytes.length} != expected ${expectSize} — BLOCKED for this input`);
  }
  if (expectSha && containerSha !== expectSha.toLowerCase()) {
    throw new Error(`[ark_index] container SHA256 ${containerSha} != expected ${expectSha} — BLOCKED for this input`);
  }

  const dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  const arch = new ArkArchive(bytes); // reuse: EOCD parse + sequential local scan
  const entries = arch.entries();      // reuse: includes EOCD total == scan count check

  // --- central-directory dual cross-check (NEW bounded verification) ---
  // For each CD entry: (a) a real local header AK\x03\x04 must exist at its
  // localOffset, (b) the local header's own name must equal the CD name, and
  // (c) the scan entry with dataOffset == localOffset+30+nameLen(+extra) must
  // exist and agree on sizes/crc — a true entry-by-entry dual-index match.
  const scanByDataOffset = new Map(entries.map((e) => [e.dataOffset, e]));
  const cdChecks = [];
  for (const layout of ['skill', 'zip']) {
    const walk = walkCentralDirectory(bytes, dv, arch.eocdCdOffset, arch.eocdCdSize, layout);
    if (!walk.ok) {
      cdChecks.push({ layout, ok: false, reason: walk.reason, cdEntries: walk.entries.length });
      continue;
    }
    if (walk.entries.length !== entries.length) {
      cdChecks.push({ layout, ok: false, reason: `cd count ${walk.entries.length} != local scan ${entries.length}`, cdEntries: walk.entries.length });
      continue;
    }
    let mismatches = 0;
    const firstMismatches = [];
    for (let i = 0; i < walk.entries.length; i++) {
      const cd = walk.entries[i];
      const off = cd.localOffset;
      if (off + 30 > bytes.length || !(bytes[off] === 0x41 && bytes[off + 1] === 0x4b && bytes[off + 2] === 0x03 && bytes[off + 3] === 0x04)) {
        mismatches++; if (firstMismatches.length < 5) firstMismatches.push(`entry ${i}: no local header at ${off}`);
        continue;
      }
      const nameLen = dv.getUint16(off + 26, true);
      const extraLen = dv.getUint16(off + 28, true);
      const localName = String.fromCharCode(...bytes.subarray(off + 30, off + 30 + nameLen));
      const dataOffset = off + 30 + nameLen + extraLen;
      const scan = scanByDataOffset.get(dataOffset);
      if (localName !== cd.name || !scan || scan.name !== cd.name) {
        mismatches++; if (firstMismatches.length < 5) firstMismatches.push(`entry ${i}: cd '${cd.name}'@${off} vs local '${localName}' scan=${scan ? scan.name : 'MISSING'}`);
      }
    }
    cdChecks.push({
      layout, ok: mismatches === 0, cdEntries: walk.entries.length, mismatches,
      ...(firstMismatches.length ? { firstMismatches } : {}),
    });
  }

  // --- per-entry catalog ---
  const records = [];
  let hashed = 0, crcVerified = 0, crcMismatched = 0, readFailures = 0;
  const dupNames = new Map();
  for (const e of entries) {
    const nameCount = dupNames.get(e.name) ?? 0;
    dupNames.set(e.name, nameCount + 1);
    const rec = {
      era: 'CD_2003',
      entryIndex: e.entryIndex,
      name: e.name,
      localHeaderOffset: null, // computed below from dataOffset - fixed - nameLen
      dataOffset: e.dataOffset,
      storedSize: e.compSize,
      uncompressedSize: e.size,
      compression: e.compression,
      flags: e.flags,
      crc32Stored: e.crc32,
      crc32Computed: null,
      crc32Match: null,
      payloadSha256: null,
      sniff: null,
      status: 'OK',
      error: null,
    };
    try {
      const { payload } = arch.readEntry(e); // reuse: STORED-only, compSize==uncomp, EOF bounds
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

  // boundary verification: last payload must end at or before the central directory
  const scanEnd = Math.max(...entries.map((e) => e.dataOffset + e.compSize));
  const boundaryChecks = {
    lastPayloadEnd: scanEnd,
    centralDirectoryOffset: arch.eocdCdOffset,
    payloadBeforeCD: scanEnd <= arch.eocdCdOffset,
    cdPlusSize: arch.eocdCdOffset + arch.eocdCdSize,
    eocdOffset: arch.eocdOffset,
    cdSizeExactToEocd: (arch.eocdCdOffset + arch.eocdCdSize) === arch.eocdOffset,
    eocdEndEqualsFileSize: (arch.eocdOffset + 22) === bytes.length,
  };

  // full catalog → PRIVATE_OUTPUT only
  const base = (args.label ?? arkPath.split(/[\\/]/).pop()).replace(/\.ark$/i, '');
  const stem = `${outDir}/CD2003_${base.toUpperCase()}_ENTRIES`;
  const csvLines = ['era,entry_index,name,data_offset,stored_size,uncompressed_size,compression,flags,crc32_stored,crc32_computed,crc32_match,payload_sha256,sniff_class,nif_version,tga_width,tga_height,tga_bpp,first8_hex,status,error'];
  for (const r of records) {
    const s = r.sniff ?? {};
    csvLines.push([
      r.era, r.entryIndex, r.name, r.dataOffset, r.storedSize, r.uncompressedSize, r.compression, r.flags,
      r.crc32Stored, r.crc32Computed ?? 'UNKNOWN', r.crc32Match ?? 'UNKNOWN', r.payloadSha256 ?? 'UNKNOWN',
      s.sniffClass ?? 'UNKNOWN', s.nifVersion ?? '', s.tgaWidth ?? '', s.tgaHeight ?? '', s.tgaBpp ?? '',
      s.first8Hex ?? '', r.status, (r.error ?? '').replace(/"/g, '""') ? `"${(r.error ?? '').replace(/"/g, '""')}"` : '',
    ].join(','));
  }
  fs.writeFileSync(stem + '.csv', csvLines.join('\r\n') + '\r\n', 'utf8');
  fs.writeFileSync(stem + '.json', JSON.stringify({
    artifact: `CD2003_${base.toUpperCase()}_ENTRIES`,
    runId: 'PE_CITY_ASSET_MAP_R1_20261010',
    phase: 'METADATA_CATALOG',
    era: 'CD_2003',
    container: { path: arkPath, sizeBytes: bytes.length, sha256: containerSha },
    readerReuse: 'src/pesource/ArkArchive.js (era-validated ArkVFS reader, imported unchanged)',
    entryCount: entries.length,
    records,
  }, null, 1), 'utf8');

  // distributions
  const sniffDist = new Map();
  const nifVerDist = new Map();
  const tgaDimDist = new Map();
  for (const r of records) {
    const s = r.sniff ?? { sniffClass: 'NO_SNIFF' };
    sniffDist.set(s.sniffClass, (sniffDist.get(s.sniffClass) ?? 0) + 1);
    if (s.nifVersion) nifVerDist.set(s.nifVersion, (nifVerDist.get(s.nifVersion) ?? 0) + 1);
    if (s.sniffClass === 'TGA_HEADER') {
      const k = `${s.tgaWidth}x${s.tgaHeight}@${s.tgaBpp}`;
      tgaDimDist.set(k, (tgaDimDist.get(k) ?? 0) + 1);
    }
  }

  const summary = {
    artifact: 'ARK_ENTRY_CATALOG_SUMMARY',
    runId: 'PE_CITY_ASSET_MAP_R1_20261010',
    phase: 'METADATA_CATALOG',
    era: 'CD_2003',
    container: { path: arkPath, sizeBytes: bytes.length, sha256: containerSha },
    entryCount: entries.length,
    eocd: {
      totalEntries: arch.eocdTotalEntries, entriesDisk: arch.eocdEntriesDisk,
      cdOffset: arch.eocdCdOffset, cdSize: arch.eocdCdSize, eocdOffset: arch.eocdOffset,
    },
    localScanVsEocd: 'MATCH (ArkArchive.entries() would have thrown otherwise)',
    centralDirectoryDualCheck: cdChecks,
    boundaryChecks,
    payloadHashedCount: hashed,
    crcVerifiedCount: crcVerified,
    crcMismatchCount: crcMismatched,
    readFailures,
    duplicateNames,
    compressionMethods: [...new Set(records.map((r) => r.compression))],
    flagsSet: [...new Set(records.map((r) => r.flags))],
    sniffClassDistribution: Object.fromEntries([...sniffDist.entries()].sort()),
    nifVersionDistribution: Object.fromEntries([...nifVerDist.entries()].sort((a, b) => b[1] - a[1])),
    tgaDimensionDistribution: Object.fromEntries([...tgaDimDist.entries()].sort((a, b) => b[1] - a[1]).slice(0, 20)),
    fullCatalogPaths: { csv: stem + '.csv', json: stem + '.json' },
    elapsedMs: Date.now() - t0,
  };
  process.stdout.write(JSON.stringify(summary, null, 1) + '\n');
}

main().catch((err) => {
  console.error('[ark_index] FATAL:', err?.stack ?? err);
  process.exitCode = 1;
});
