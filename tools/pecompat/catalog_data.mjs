// catalog_data.mjs — PE_CITY_ASSET_MAP_R1_20261010, phase 4 (W5, contract §5)
// THE CATALOG DATA MODEL shared by compat/server-catalog.mjs (the product path)
// and the tests/pecompat/* gates. REGENERATION-FIRST: at every buildCatalogData()
// call the entry catalogs are re-derived from the pinned READ_ONLY originals
// (container SHA verified fail-closed; per-entry CRC32 recomputed; payload
// SHA256 recomputed) — there is NO stale hand-edited JSON in the product path.
// The ONLY cached inputs are the phase-2/phase-3 MEASURED artifacts
// (batch extent state, PCG935 name-edge batch), attached STRICTLY BY IDENTITY
// KEY (era + container SHA + entry name + payload SHA — the phase-2 schema);
// a cache row whose identity does not match the regenerated catalog is DROPPED
// and counted (never silently used).
//
// REUSE LABELS (contract §8 discipline):
//   - src/pesource/ArkArchive.js + src/pesource/Bnt2Archive.js — the
//     era-validated container readers, imported UNCHANGED (whole-file reads,
//     exactly as in phase-2 ark_index.mjs/bnt_index.mjs).
//   - tools/pecompat/catalog_sniff.mjs sniffPayload — imported UNCHANGED
//     (phase-2 header-only heuristic classification; never a decode).
//   - tools/pecompat/nif41_deep.mjs readNif41/analyzeNif41Model — the
//     phase-3 bounded NIF-4.1 reader (four primary CD_2003 models only),
//     imported UNCHANGED plus its phase-4 ADDITIVE export of ir/worldTransforms.
//   - src/pecompat/PecSceneIR.js composition/bounds — reached through
//     analyzeNif41Model exactly as in phase 3.
//   NEW here (bounded, labeled per function): the sort/filter/search row
//   helpers, the identity-keyed cache attach, the two BOUNDED INDEX-ONLY
//   readers (readBnt2Index / readArkCentralDirectory — tail/directory reads
//   that never load payload bytes; cross-verified against the reused readers
//   in the archive-safety gates), and buildPrimaryWire.
//
// ERA DISCIPLINE: every row carries an explicit era (CD_2003 | PCG_9_3_5);
// the same entry name in both eras is TWO DISTINCT assets (identity =
// era + container SHA + entry name + payload SHA). UNKNOWN is never 0 —
// an unmeasured field is { unknown: true }.
// SOURCE_FILE_SCENE_SPACE ≠ WORLD_PLACEMENT on every measured value; ORIGINAL
// file units only (never called meters); no city/place identification anywhere.

'use strict';
import crypto from 'node:crypto';
import { promises as fsp } from 'node:fs';
import { ArkArchive } from '../../src/pesource/ArkArchive.js';
import { Bnt2Archive } from '../../src/pesource/Bnt2Archive.js';
import { sniffPayload } from './catalog_sniff.mjs';
import {
  readNif41, analyzeNif41Model, placementAnalysis, PEC_NIF41_READER_VERSION,
} from './nif41_deep.mjs';

/** Bounded positional read (the default for the index-only readers): reads
 *  EXACTLY opts.length bytes at opts.position — never the whole file. */
async function positionalRead(filePath, opts) {
  const fh = await fsp.open(filePath, 'r');
  try {
    const buf = new Uint8Array(opts.length);
    const { bytesRead } = await fh.read(buf, 0, opts.length, opts.position);
    return buf.subarray(0, bytesRead);
  } finally {
    await fh.close();
  }
}

export const CATALOG_DATA_VERSION = 'pec-catalog-data-v1-phase4';

// ---- pinned identities (INPUT_IDENTITIES.json, re-measured phase 1; fail-closed) ----
export const CATALOG_PINS = Object.freeze({
  modelsArk: {
    path: 'D:\\Eudoria_Reconstruction\\pcg2003_install\\Data\\Models\\Models.ark',
    sizeBytes: 128742137,
    sha256: 'f660d055b4b9471b3b6e16b07f5368dbd6f2208dab6b51bb9bdb9942bd73ea62',
    era: 'CD_2003',
    container: 'Models/Models.ark',
  },
  modelsBnt: {
    path: 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt',
    sizeBytes: 395412868,
    sha256: 'c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0',
    era: 'PCG_9_3_5',
    container: 'Models/Models.bnt',
    requiredPin: true, // contract §1 required pin
  },
  texturesArk: {
    path: 'D:\\Eudoria_Reconstruction\\pcg2003_install\\Data\\Textures\\Textures.ark',
    sizeBytes: 289585581,
    sha256: 'd611d1257d2e5433b6df218d671aa60d003c5c6587858757c7af3219bb739b80',
    era: 'CD_2003',
    container: 'Textures/Textures.ark',
  },
  texturesBnt: {
    path: 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Textures\\Textures.bnt',
    sizeBytes: 973942771,
    sha256: '61acd13b140e130647eee24c1e2669d3734990b76cf74897ddd3ba0f4ea61393',
    era: 'PCG_9_3_5',
    container: 'Textures/Textures.bnt',
  },
});

// ---- the four primary CD_2003 models (contract §3; payload pins from the
// phase-2 catalog + phase-3 extraction, fail-closed re-verified at every read) ----
export const PRIMARY_IDS = Object.freeze(['192374', '193207', '193313', '193684']);
export const PRIMARY_PINS = Object.freeze({
  '192374': { entryIndex: 888, sizeBytes: 66759, sha256: '08d80c67bb87caf6a1c00bf8c034e329484e25a6a588da411079bb6f682de8c1' },
  '193207': { entryIndex: 908, sizeBytes: 47167, sha256: '220f549b311563a1a6506cacefcebb8911ee4770cf72b85f2f635146c111adbb' },
  '193313': { entryIndex: 910, sizeBytes: 66726, sha256: '02fc860a840e9cdb948f04daff2691bb37baf9e0da8dbadc8f77773c517beef2' },
  '193684': { entryIndex: 913, sizeBytes: 75805, sha256: '4cc5f9203280c26fc2020bb6c432e2bcf4e5db4ec2f47be3df573e537660901f' },
});

// The Desktop name hypotheses (contract §3: NAMES/HYPOTHESES ONLY — byte-level
// reproduction evidence; NOT game classes, NOT city names; MSC/MAC not promoted).
export const PRIMARY_DESKTOP_HYPOTHESES = Object.freeze({
  '192374': 'Box01, MSC, MAC, signs',
  '193207': 'Box06, Object01',
  '193313': 'Outpost39_proxymesh, MSC, signs, build, MAC',
  '193684': 'signs, mlti, wall, signs01, mac, build, cont, forts',
});

export const SPACE_LABEL = Object.freeze({
  space: 'FILE_SCENE_SPACE',
  axisConvention: 'file-serialized x/y/z labels; NO axis swap; NO unit conversion; axis semantics (e.g. up-axis) NOT established by the reader; ORIGINAL file units everywhere — never called meters; SOURCE_FILE_SCENE_SPACE != WORLD_PLACEMENT',
});

export const SORT_RULE_LABEL =
  'Sort: MEASURED values largest->smallest; UNKNOWN rows are always LAST with an UNKNOWN badge — UNKNOWN is never treated as 0 (never invented, never silently zeroed)';

// ---------------------------------------------------------------------------
// CRC32 (the phase-2 catalog_sniff sibling helper — same table method as
// ark_index.mjs; kept here so the server and the tests share ONE definition)
// ---------------------------------------------------------------------------
const CRC_TABLE = (() => {
  const t = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = (c & 1) ? (0xedb88320 ^ (c >>> 1)) : (c >>> 1);
    t[n] = c >>> 0;
  }
  return t;
})();
export function crc32(bytes) {
  let c = 0xffffffff;
  for (let i = 0; i < bytes.length; i++) c = CRC_TABLE[(c ^ bytes[i]) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}

// ---------------------------------------------------------------------------
// BOUNDED INDEX-ONLY readers (NEW, phase 4) — directory reads that NEVER load
// payload bytes. Used by the server (Models containers are read whole via the
// REUSED readers for payload identity; these bounded readers exist for the
// big TEXTURE containers where only the name index is needed) and by the
// archive-safety gates (byte-budget + dual-index agreement vs the reused
// readers on the real Models containers).
// ---------------------------------------------------------------------------

/** BNT2 bounded index read: stat + tail(8) + directory range only.
 * Verifies: footer magic, sane count, exact directory end, entry names fit,
 * payloads fit before the directory. Returns { entries, bytesRead, fileSize }.
 * NEVER reads payload ranges. */
export async function readBnt2Index(filePath, { readFile, stat } = {}) {
  const rd = readFile ?? positionalRead;
  const st = stat ?? (async (p) => fsp.stat(p));
  const fstat = await st(filePath);
  const fileSize = fstat.size;
  if (fileSize < 8) throw new Error('[readBnt2Index] file too small');
  let bytesRead = 0;
  const tail = await rd(filePath, { length: 8, position: fileSize - 8 });
  bytesRead += tail.length;
  const magic = String.fromCharCode(...tail.subarray(4, 8));
  if (magic !== 'BNT2') throw new Error(`[readBnt2Index] bad footer magic "${magic}" (expected BNT2)`);
  const dv8 = new DataView(tail.buffer, tail.byteOffset, tail.byteLength);
  const dirOffset = dv8.getUint32(0, true);
  if (dirOffset < 4 || dirOffset > fileSize - 8) {
    throw new Error(`[readBnt2Index] implausible dirOffset ${dirOffset} for size ${fileSize}`);
  }
  const dirBytes = await rd(filePath, { length: fileSize - 8 - dirOffset, position: dirOffset });
  bytesRead += dirBytes.length;
  const dv = new DataView(dirBytes.buffer, dirBytes.byteOffset, dirBytes.byteLength);
  const count = dv.getUint32(0, true);
  if (count > 200000) throw new Error(`[readBnt2Index] implausible entry count ${count}`);
  const entries = [];
  let p = 4;
  for (let i = 0; i < count; i++) {
    const nameStart = p;
    while (p < dirBytes.length && dirBytes[p] !== 0x0a) p++;
    if (p >= dirBytes.length) throw new Error(`[readBnt2Index] entry ${i}: unterminated name`);
    if (p - nameStart > 512) throw new Error(`[readBnt2Index] entry ${i}: implausible name length ${p - nameStart}`);
    const name = String.fromCharCode(...dirBytes.subarray(nameStart, p));
    p++;
    if (p + 16 > dirBytes.length) throw new Error(`[readBnt2Index] entry ${i}: truncated directory row`);
    const size = dv.getUint32(p, true);
    const offset = dv.getUint32(p + 4, true);
    const crc = dv.getUint32(p + 8, true);
    const pad = dv.getUint32(p + 12, true);
    p += 16;
    if (offset + size > dirOffset) {
      throw new Error(`[readBnt2Index] entry ${i} "${name}" payload [${offset}, ${offset + size}) crosses the directory at ${dirOffset}`);
    }
    entries.push({ entryIndex: i, name, size, offset, crc32: crc, pad });
  }
  if (p !== dirBytes.length) {
    throw new Error(`[readBnt2Index] directory walk ended at ${p} != ${dirBytes.length} (count=${count})`);
  }
  return { entries, bytesRead, fileSize, dirOffset, count };
}

/** .ark bounded index read: stat + EOCD scan window + central-directory range
 * only (standard-ZIP CD layout — dual-index-verified on both real .ark
 * containers in phase 2; the sequential local-header scan stays with the
 * REUSED ArkArchive). NEVER reads payload ranges.
 * Returns { entries, bytesRead, fileSize, eocd: {...} }. */
export async function readArkCentralDirectory(filePath, { readFile, stat } = {}) {
  const rd = readFile ?? positionalRead;
  const st = stat ?? (async (p) => fsp.stat(p));
  const fstat = await st(filePath);
  const fileSize = fstat.size;
  if (fileSize < 46) throw new Error('[readArkCentralDirectory] file too small');
  let bytesRead = 0;
  const WINDOW = Math.min(fileSize, 22 + 65536);
  const win = await rd(filePath, { length: WINDOW, position: fileSize - WINDOW });
  bytesRead += win.length;
  let eocd = -1;
  for (let i = win.length - 22; i >= 0; i--) {
    if (win[i] === 0x41 && win[i + 1] === 0x4b && win[i + 2] === 0x05 && win[i + 3] === 0x06) { eocd = i; break; }
  }
  if (eocd < 0) throw new Error('[readArkCentralDirectory] EOCD AK\\x05\\x06 not found');
  const dvW = new DataView(win.buffer, win.byteOffset, win.byteLength);
  const cdSize = dvW.getUint32(eocd + 12, true);
  const cdOffset = dvW.getUint32(eocd + 16, true);
  const totalEntries = dvW.getUint16(eocd + 10, true);
  const eocdOffset = (fileSize - WINDOW) + eocd;
  if (cdOffset + cdSize !== eocdOffset) {
    throw new Error(`[readArkCentralDirectory] cd end ${cdOffset + cdSize} != EOCD offset ${eocdOffset}`);
  }
  const cd = await rd(filePath, { length: cdSize, position: cdOffset });
  bytesRead += cd.length;
  const dv = new DataView(cd.buffer, cd.byteOffset, cd.byteLength);
  const entries = [];
  let p = 0;
  while (p < cdSize) {
    if (!(cd[p] === 0x41 && cd[p + 1] === 0x4b && cd[p + 2] === 0x01 && cd[p + 3] === 0x02)) {
      throw new Error(`[readArkCentralDirectory] no AK\\x01\\x02 at cd pos ${p}`);
    }
    const nameLen = dv.getUint16(p + 28, true);
    const extraLen = dv.getUint16(p + 30, true);
    const commentLen = dv.getUint16(p + 32, true);
    if (nameLen > 512 || p + 46 + nameLen > cdSize) {
      throw new Error(`[readArkCentralDirectory] implausible name_len ${nameLen} at cd pos ${p}`);
    }
    const name = String.fromCharCode(...cd.subarray(p + 46, p + 46 + nameLen));
    entries.push({
      entryIndex: entries.length,
      name,
      crc32: dv.getUint32(p + 16, true) >>> 0,
      compSize: dv.getUint32(p + 20, true),
      size: dv.getUint32(p + 24, true),
      compression: dv.getUint16(p + 10, true),
      localOffset: dv.getUint32(p + 42, true),
    });
    p += 46 + nameLen + extraLen + commentLen;
  }
  if (p !== cdSize) throw new Error(`[readArkCentralDirectory] cd walk ended at ${p} != ${cdSize}`);
  if (totalEntries !== entries.length) {
    throw new Error(`[readArkCentralDirectory] EOCD total ${totalEntries} != cd walk ${entries.length}`);
  }
  return { entries, bytesRead, fileSize, eocd: { offset: eocdOffset, cdOffset, cdSize, totalEntries } };
}

// ---------------------------------------------------------------------------
// buildCatalogData — REGENERATE both Models entry catalogs from the pinned
// originals (fail-closed container identity), verify per-entry CRC32 + payload
// SHA256, attach the identity-keyed measured caches, decode the four
// primaries LIVE, and produce the browsable rows + coverage.
// ---------------------------------------------------------------------------

function decodeReasonForFailed(errorText) {
  const m = /UNKNOWN type "([^"]+)"/.exec(errorText ?? '');
  if (m) return `unregistered block type "${m[1]}" (bounded reader surface — loud failure preserved verbatim)`;
  return String(errorText ?? '').slice(0, 90);
}

function numIdOf(name) {
  const m = /^(\d+)\.nif$/i.exec(name);
  return m ? Number(m[1]) : null;
}

export async function buildCatalogData(opts = {}) {
  const io = opts.io ?? {
    readFile: async (p) => new Uint8Array(await (await import('node:fs/promises')).readFile(p)),
    sha256: (b) => crypto.createHash('sha256').update(b).digest('hex'),
  };
  const modelsArkPath = opts.modelsArkPath ?? CATALOG_PINS.modelsArk.path;
  const modelsBntPath = opts.modelsBntPath ?? CATALOG_PINS.modelsBnt.path;
  const batchStatePath = opts.batchStatePath ?? null;   // PHASE2_EXTENT/PCG935_NIF10_BATCH_STATE.jsonl (identity-keyed cache)
  const nameEdgesPath = opts.nameEdgesPath ?? null;      // PHASE3_PCG935_BATCH/PCG935_NAME_EDGES.jsonl (identity-keyed cache)
  const skipPayloadHash = opts.skipPayloadHash ?? false;  // tests may skip the 525 MB hash pass on synthetic data

  const t0 = Date.now();
  const out = {
    version: CATALOG_DATA_VERSION,
    runId: 'PE_CITY_ASSET_MAP_R1_20261010',
    eraLabels: {
      CD_2003: 'corpus of the 2003 CD installer (Models.ark/Textures.ark)',
      PCG_9_3_5: 'PCG 9.3.5 installation (Models.bnt/Textures.bnt/vfs)',
    },
    sortRule: SORT_RULE_LABEL,
    space: SPACE_LABEL,
    containers: {},
    coverage: null,
    rows: [],
    primaries: {},       // id -> { analysis, wire? } (wire built lazily by the server)
    primaryPayloads: {}, // id -> Uint8Array (pin-verified, extracted at build)
    cache: { batchState: null, nameEdges: null },
    overlap: null,       // same entry name in BOTH eras (legal; era-separated)
    elapsedMs: 0,
  };

  // ---- CD_2003 Models.ark (reused reader, whole-file, fail-closed pin) ----
  const arkBytes = await io.readFile(modelsArkPath);
  const arkSha = io.sha256(arkBytes);
  const arkPin = CATALOG_PINS.modelsArk;
  if (arkBytes.length !== arkPin.sizeBytes || arkSha !== arkPin.sha256) {
    throw new Error(`[catalog_data] CD_2003 Models.ark identity mismatch (size ${arkBytes.length}/${arkPin.sizeBytes}, sha ${arkSha}) — BLOCKED for this input`);
  }
  const ark = new ArkArchive(arkBytes);
  const arkEntries = ark.entries(); // reused reader: EOCD total == local scan
  const arkRows = [];
  let arkCrcOk = 0, arkCrcBad = 0, arkHashed = 0;
  const arkPrimaryRaw = {};
  for (const e of arkEntries) {
    const { payload } = ark.readEntry(e); // reused: STORED-only, EOF bounds
    const crcComputed = crc32(payload);
    const crcMatch = crcComputed === (e.crc32 >>> 0);
    if (crcMatch) arkCrcOk++; else arkCrcBad++;
    const sha = skipPayloadHash ? null : io.sha256(payload);
    if (sha) arkHashed++;
    const sniff = sniffPayload(payload);
    const id = numIdOf(e.name);
    const isPrimary = id != null && PRIMARY_PINS[id] != null;
    if (isPrimary) {
      const pin = PRIMARY_PINS[id];
      if (payload.length !== pin.sizeBytes || (sha && sha !== pin.sha256)) {
        throw new Error(`[catalog_data] primary ${e.name} identity mismatch (size ${payload.length}/${pin.sizeBytes}) — BLOCKED`);
      }
      arkPrimaryRaw[id] = new Uint8Array(payload); // copy — survives container release
    }
    arkRows.push({
      era: 'CD_2003', id, entryName: e.name, entryIndex: e.entryIndex,
      container: arkPin.container, containerSha256: arkPin.sha256,
      sizeBytes: e.size, storedSizeBytes: e.compSize, compression: `STORED (${e.compression})`,
      crc32Stored: e.crc32 >>> 0, crc32Match: crcMatch, payloadSha256: sha,
      sniffClass: sniff.sniffClass, nifVersion: sniff.nifVersion ?? null,
      status: 'OK',
    });
  }
  out.containers.CD_2003_Models_ark = {
    path: modelsArkPath, sizeBytes: arkBytes.length, sha256: arkSha, pin: 'MATCH',
    readerReuse: 'src/pesource/ArkArchive.js (era-validated ArkVFS reader, imported UNCHANGED)',
    entries: arkEntries.length, crc32Verified: arkCrcOk, crc32Mismatch: arkCrcBad, payloadHashed: arkHashed,
  };

  // ---- PCG_9_3_5 Models.bnt (REQUIRED PIN, fail-closed; reused reader) ----
  const bntBytes = await io.readFile(modelsBntPath);
  const bntSha = io.sha256(bntBytes);
  const bntPin = CATALOG_PINS.modelsBnt;
  if (bntBytes.length !== bntPin.sizeBytes || bntSha !== bntPin.sha256) {
    throw new Error(`[catalog_data] PCG_9_3_5 Models.bnt REQUIRED PIN MISMATCH (size ${bntBytes.length}/${bntPin.sizeBytes}, sha ${bntSha}) — BLOCKED for this input`);
  }
  const bnt = new Bnt2Archive(bntBytes);
  const bntEntries = bnt.entries(); // reused reader: exact directory end
  const bntRows = [];
  let bntCrcOk = 0, bntCrcBad = 0, bntHashed = 0;
  for (const e of bntEntries) {
    const { payload } = bnt.readEntry(e); // reused: RAW 1:1, EOF bounds
    const crcComputed = crc32(payload);
    const crcMatch = crcComputed === (e.crc32 >>> 0);
    if (crcMatch) bntCrcOk++; else bntCrcBad++;
    const sha = skipPayloadHash ? null : io.sha256(payload);
    if (sha) bntHashed++;
    const sniff = sniffPayload(payload);
    bntRows.push({
      era: 'PCG_9_3_5', id: numIdOf(e.name), entryName: e.name, entryIndex: e.entryIndex,
      container: bntPin.container, containerSha256: bntPin.sha256,
      sizeBytes: e.size, storedSizeBytes: e.size, compression: 'RAW 1:1 (no compression)',
      crc32Stored: e.crc32 >>> 0, crc32Match: crcMatch, payloadSha256: sha,
      sniffClass: sniff.sniffClass, nifVersion: sniff.nifVersion ?? null,
      status: 'OK',
    });
  }
  out.containers.PCG_9_3_5_Models_bnt = {
    path: modelsBntPath, sizeBytes: bntBytes.length, sha256: bntSha, pin: 'MATCH (REQUIRED pin verified at load)',
    readerReuse: 'src/pesource/Bnt2Archive.js (era-validated BNT2 reader, imported UNCHANGED)',
    entries: bntEntries.length, crc32Verified: bntCrcOk, crc32Mismatch: bntCrcBad, payloadHashed: bntHashed,
  };

  // ---- identity-keyed measured caches (phase-2 batch extent state) ----
  const byKeyPcg = new Map();
  for (const r of bntRows) byKeyPcg.set(`${r.entryName}|${r.payloadSha256 ?? '?'}`, r);
  let batchAttached = 0, batchDropped = 0;
  if (batchStatePath) {
    const raw = await io.readFile(batchStatePath);
    const text = new TextDecoder().decode(raw);
    for (const line of text.split('\n')) {
      if (!line.trim()) continue;
      const row = JSON.parse(line);
      const key = `${row.name}|${row.payloadSha256}`;
      const target = byKeyPcg.get(key);
      if (!target) { batchDropped++; continue; } // identity mismatch → dropped, counted
      target._batch = row;
      batchAttached++;
    }
  }
  out.cache.batchState = {
    path: batchStatePath, attached: batchAttached, droppedIdentityMismatch: batchDropped,
    policy: 'identity-keyed cache: era + container SHA + entry name + payload SHA must match the REGENERATED catalog; mismatches are DROPPED and counted (never used)',
  };

  // ---- identity-keyed measured caches (phase-3 PCG935 name edges → texture coverage) ----
  const edgesByModel = new Map();
  let edgesAttached = 0, edgesDropped = 0;
  if (nameEdgesPath) {
    const raw = await io.readFile(nameEdgesPath);
    const text = new TextDecoder().decode(raw);
    for (const line of text.split('\n')) {
      if (!line.trim()) continue;
      const e = JSON.parse(line);
      // the JSONL carries model names only; per-model identity goes through
      // the batch state rows (name + payload SHA) identity-verified below.
      const agg = edgesByModel.get(e.model) ?? { nameEdges: 0, nameFound: 0, nameBase: 0, nameNotFound: 0, matEdges: 0 };
      if (e.edge === 'SHAPE->NIMATERIALPROPERTY') agg.matEdges++;
      else {
        agg.nameEdges++;
        if (e.disposition === 'NAME_FOUND_EXACT') agg.nameFound++;
        else if (e.disposition === 'NAME_BASE_MATCH_EXTENSION_DIFF') agg.nameBase++;
        else if (e.disposition === 'NAME_NOT_FOUND') agg.nameNotFound++;
      }
      edgesByModel.set(e.model, agg);
    }
    // identity gate: only models whose batch row was identity-attached keep edges
    for (const r of bntRows) {
      if (edgesByModel.has(r.entryName) && r._batch) { r._edges = edgesByModel.get(r.entryName); edgesAttached++; }
      else if (edgesByModel.has(r.entryName)) { edgesDropped++; }
    }
  }
  out.cache.nameEdges = {
    path: nameEdgesPath, modelsAttached: edgesAttached, modelsDroppedIdentityMismatch: edgesDropped,
    policy: 'per-model aggregates attached ONLY where the model has an identity-verified phase-2 batch row (name + payload SHA) in the regenerated catalog',
  };

  // ---- the four primaries: LIVE decode (phase-3 reader, pins re-verified) ----
  for (const id of PRIMARY_IDS) {
    const payload = arkPrimaryRaw[id];
    if (!payload) throw new Error(`[catalog_data] primary ${id} not extracted — BLOCKED`);
    const pin = PRIMARY_PINS[id];
    const sha = io.sha256(payload);
    if (payload.length !== pin.sizeBytes || sha !== pin.sha256) {
      throw new Error(`[catalog_data] primary ${id} pin mismatch — BLOCKED`);
    }
    const r = readNif41(payload, { sourceName: `${id}.nif` });
    const analysis = analyzeNif41Model(r, {
      assetId: Number(id),
      era: 'CD_2003',
      build: 'CD_2003_Models_ark_primary_phase4_live_decode',
      container: arkPin.container,
      entryName: `${id}.nif`,
      payloadSha256: sha,
      sizeBytes: payload.length,
      adapterVersion: PEC_NIF41_READER_VERSION,
      physicalSource: `Models.ark entry ${pin.entryIndex} (READ_ONLY original; regenerated at server build)`,
    });
    // the phase-3 CLI step, applied on the live decode (VERTICES/TRANSFORMS/BOTH
    // classification — measured, never assumed)
    analysis.placementFinding = placementAnalysis(analysis);
    out.primaries[id] = { analysis };
    out.primaryPayloads[id] = payload;
  }

  // ---- rows (metadata only; every field honest: UNKNOWN never 0) ----
  const rows = [];
  for (const r of arkRows) {
    const prim = out.primaries[r.id];
    const row = {
      era: r.era, id: r.id, entryName: r.entryName, entryIndex: r.entryIndex,
      container: r.container, containerSha256: r.containerSha256,
      sizeBytes: r.sizeBytes, storedSizeBytes: r.storedSizeBytes, compression: r.compression,
      payloadSha256: r.payloadSha256, crc32Match: r.crc32Match,
      nifVersion: r.nifVersion,
      decodeCoverage: prim ? 'DECODED_FULL_CLOSURE' : 'CATALOG_ONLY',
      decodeReason: prim
        ? 'decoded live at server build by the phase-3 bounded NIF-4.1 reader (all blocks + TopObjects footer + EOF exact)'
        : 'no decoder authorized for this entry in this run (the bounded NIF-4.1 reader covers ONLY the four pinned primaries; NIF 4.0.x never attempted)',
      previewable: !!prim,
      sceneExtent: prim ? {
        unknown: false, ...prim.analysis.bounds,
        ...SPACE_LABEL,
      } : { unknown: true, note: 'not decoded in this run — UNKNOWN (never 0); SOURCE_FILE_SCENE_SPACE != WORLD_PLACEMENT' },
      complexity: prim ? {
        unknown: false, ...prim.analysis.complexity,
        units: 'triangles=NiTriShapeData triangle count; vertices=vertex count; shapes=NiTriShape blocks; nodes=NiNode blocks',
      } : { unknown: true, note: 'not decoded in this run' },
      textureCoverage: prim
        ? `UNTEXTURED_PROXY_MESH (0 NiTexturingProperty, 0 NiSourceTexture, ArkTexture numTex=0, 0 UV sets on every mesh; ${prim.analysis.textureEdges.length} material edges REFERENCE_CONFIRMED — explicit visual fallback, NOT a textured PASS)`
        : 'UNKNOWN (not decoded in this run)',
      roleHypothesis: prim ? PRIMARY_DESKTOP_HYPOTHESES[r.id] : null,
      roleEvidence: prim
        ? `Desktop name read REPRODUCED byte-level from the original payload as NiNode names (phase-3 reader full closure; Python dual-decode agreement). NAMES/HYPOTHESES ONLY — NOT game classes, NOT city names; MSC/MAC not promoted. Placement finding: ${prim.analysis.placementFinding.finding} (all local TRS identity — measured).`
        : null,
    };
    rows.push(row);
  }
  for (const r of bntRows) {
    const b = r._batch ?? null;
    const edges = r._edges ?? null;
    let decodeCoverage, decodeReason;
    if (b) {
      if (b.status === 'DECODED') { decodeCoverage = 'DECODED'; decodeReason = 'phase-2 batch decode through the era-validated PecNif10Reader chain (identity-keyed cache row verified)'; }
      else if (b.status === 'DECODED_NO_MESH_GEOMETRY') { decodeCoverage = 'DECODED_NO_MESH'; decodeReason = 'decoded; no mesh geometry blocks (measured zero triangle/vertex counts are REAL; scene extent UNKNOWN — never 0)'; }
      else { decodeCoverage = 'FAILED'; decodeReason = `decode attempted (phase-2 batch): ${decodeReasonForFailed(b.error)}`; }
    } else {
      decodeCoverage = 'VERSION_GATED';
      decodeReason = 'NIF 4.x outside the active reader gates (PecNif10Reader gates Gamebryo 10.1.0.0 exactly) — never attempted in this run';
    }
    const row = {
      era: r.era, id: r.id, entryName: r.entryName, entryIndex: r.entryIndex,
      container: r.container, containerSha256: r.containerSha256,
      sizeBytes: r.sizeBytes, storedSizeBytes: r.storedSizeBytes, compression: r.compression,
      payloadSha256: r.payloadSha256, crc32Match: r.crc32Match,
      nifVersion: r.nifVersion,
      decodeCoverage, decodeReason,
      previewable: false, // no safe import established for PCG_9_3_5 entries in the /catalog mode (218757's viewer is the separate SceneIR app)
      sceneExtent: (b && b.status === 'DECODED' && b.bounds)
        ? { unknown: false, ...b.bounds, ...SPACE_LABEL }
        : { unknown: true, note: 'not measured (undecoded or no mesh geometry) — UNKNOWN (never 0); SOURCE_FILE_SCENE_SPACE != WORLD_PLACEMENT' },
      complexity: b
        ? {
          unknown: false,
          triangles: b.triangles ?? null, vertices: b.vertices ?? null,
          shapes: b.shapeCount ?? null, nodes: b.nodeCount ?? null, blocks: b.blockCount ?? null,
          units: 'triangles=NiTriShapeData triangle count; vertices=vertex count; shapes=NiTriShape blocks; nodes=NiNode blocks',
        }
        : { unknown: true, note: 'not decoded in this run' },
      textureCoverage: edges
        ? `NAME_FOUND_EXACT=${edges.nameFound}; NAME_BASE_MATCH_EXTENSION_DIFF=${edges.nameBase}; NAME_NOT_FOUND=${edges.nameNotFound}; MATERIAL_REFERENCE_CONFIRMED=${edges.matEdges} (ArkTexture descriptive names vs the same-era Textures.bnt numeric-name catalog; container resolution NOT established — no IMAGE_DECODED, no MATERIAL_APPLIED)`
        : (b
          ? 'NO_RECORDED_EDGES (decoded but no shape-bound ArkTexture entries recorded in the phase-3 batch)'
          : 'UNKNOWN (not decoded in this run)'),
      roleHypothesis: null,
      roleEvidence: null,
    };
    rows.push(row);
  }
  out.rows = rows;

  // ---- coverage (mandatory, numeric, no aggregate hides a per-era count) ----
  const byDecode = {};
  for (const row of rows) byDecode[row.decodeCoverage] = (byDecode[row.decodeCoverage] ?? 0) + 1;
  const extentMeasured = rows.filter((r) => !r.sceneExtent.unknown).length;
  const complexityMeasured = rows.filter((r) => !r.complexity.unknown).length;
  out.coverage = {
    totalRows: rows.length,
    byEra: {
      CD_2003: rows.filter((r) => r.era === 'CD_2003').length,
      PCG_9_3_5: rows.filter((r) => r.era === 'PCG_9_3_5').length,
    },
    byDecodeCoverage: byDecode,
    sceneExtent: {
      measured: extentMeasured,
      unknown: rows.length - extentMeasured,
      coverageLine: `SCENE_EXTENT measured ${extentMeasured} of ${rows.length} (CD_2003: 4 of ${out.containers.CD_2003_Models_ark.entries}; PCG_9_3_5: ${bntRows.filter((r) => r._batch?.status === 'DECODED').length} of ${out.containers.PCG_9_3_5_Models_bnt.entries}) — every table is LARGEST-MEASURED, never "largest of all"`,
    },
    complexity: { measured: complexityMeasured, unknown: rows.length - complexityMeasured },
    claimDiscipline: 'ALL rankings are largest-MEASURED (coverage incomplete); "largest city"-style claims are FORBIDDEN and NOT made; big file != biggest extent != most complex (separate tables, never merged into one verdict)',
  };

  // ---- duplicate-ID-across-eras census (legal; must NOT be conflated) ----
  const cdNames = new Set(arkRows.map((r) => r.entryName));
  const overlapNames = bntRows.filter((r) => cdNames.has(r.entryName)).map((r) => r.entryName);
  out.overlap = {
    count: overlapNames.length,
    sample: overlapNames.slice(0, 8),
    policy: 'the same entry name in BOTH eras is LEGAL and stays TWO DISTINCT assets — identity = ERA + CONTAINER_SHA256 + ENTRY_NAME + PAYLOAD_SHA256 (never conflated)',
  };

  out.elapsedMs = Date.now() - t0;
  return out;
}

// ---------------------------------------------------------------------------
// pure row helpers (shared by the server routes and the UNKNOWN-handling gates)
// ---------------------------------------------------------------------------

/** DESCENDING sort by metric; UNKNOWN rows always LAST (never as 0).
 * metric: 'size' | 'extent' | 'triangles' | 'vertices' | 'shapes'. */
export function sortRows(rows, { metric = 'size', unknownLast = true } = {}) {
  const readValue = (row) => {
    switch (metric) {
      case 'size': return row.sizeBytes;
      case 'extent': return row.sceneExtent?.unknown ? null : (row.sceneExtent?.maxAxisExtent ?? null);
      case 'triangles': return row.complexity?.unknown ? null : (row.complexity?.triangles ?? null);
      case 'vertices': return row.complexity?.unknown ? null : (row.complexity?.vertices ?? null);
      case 'shapes': return row.complexity?.unknown ? null : (row.complexity?.shapes ?? null);
      default: throw new Error(`[sortRows] unknown metric "${metric}"`);
    }
  };
  const withIdx = rows.map((row, i) => ({ row, i, v: readValue(row) }));
  withIdx.sort((a, b) => {
    const aKnown = a.v != null, bKnown = b.v != null;
    if (!aKnown && !bKnown) return a.i - b.i;       // stable: UNKNOWN keeps source order
    if (!aKnown) return unknownLast ? 1 : -1;         // UNKNOWN last (never as 0)
    if (!bKnown) return unknownLast ? -1 : 1;
    if (b.v !== a.v) return b.v - a.v;               // measured: LARGEST -> smallest
    return a.i - b.i;
  });
  return withIdx.map((x) => x.row);
}

/** Filter by era / decode-coverage status / ID-or-name substring search.
 * Unknown filter values throw (server maps that to a 400). */
export function filterRows(rows, { era = 'ALL', status = 'ALL', q = '' } = {}) {
  const ERAS = ['ALL', 'CD_2003', 'PCG_9_3_5'];
  const STATUSES = ['ALL', 'DECODED_FULL_CLOSURE', 'DECODED', 'DECODED_NO_MESH', 'FAILED', 'VERSION_GATED', 'CATALOG_ONLY'];
  if (!ERAS.includes(era)) throw new Error(`[filterRows] unknown era filter "${era}"`);
  if (!STATUSES.includes(status)) throw new Error(`[filterRows] unknown status filter "${status}"`);
  const needle = String(q).trim().toLowerCase();
  return rows.filter((row) => {
    if (era !== 'ALL' && row.era !== era) return false;
    if (status !== 'ALL' && row.decodeCoverage !== status) return false;
    if (needle) {
      const inName = row.entryName.toLowerCase().includes(needle);
      const inId = row.id != null && String(row.id).includes(needle);
      if (!inName && !inId) return false;
    }
    return true;
  });
}

// ---------------------------------------------------------------------------
// buildPrimaryWire — the bounded wire payload for ONE primary's preview
// (geometry + material preview; runtime loopback-only data like the SceneIR
// wire — NEVER a committed fixture). The client re-composes transforms itself
// (three.js) and cross-checks against the shipped bounds — fail-closed.
// ---------------------------------------------------------------------------
export const CATALOG_WIRE_VERSION = 'pec-catalog-wire-v1';

export function buildPrimaryWire(primaryEntry, id) {
  const { analysis } = primaryEntry;
  const ir = analysis.ir;
  const blocks = ir.blocks.map((b) => {
    const rec = {
      index: b.index, type: b.type, name: b.name, decodeStatus: b.decodeStatus,
      byteRange: [b.byteStart, b.byteEnd],
      localTrs: b.localTrs ? {
        translate: [...b.localTrs.translate], rotate: b.localTrs.rotate.map((r) => [...r]), scale: b.localTrs.scale,
      } : null,
      children: b.children ?? null,
      propertyRefs: b.propertyRefs ?? null,
      extraDataRef: b.fields?.extraDataRef ?? null,
      dataRef: b.dataRef ?? null,
      geometry: null,
    };
    if (b.geometry) {
      const g = b.geometry;
      const posBytes = new Uint8Array(g.positions.buffer, g.positions.byteOffset, g.positions.byteLength);
      const idxBytes = new Uint8Array(g.indices.buffer, g.indices.byteOffset, g.indices.byteLength);
      rec.geometry = {
        positions: Array.from(g.positions ?? []),
        normals: g.normals ? Array.from(g.normals) : null,
        uvSets: (g.uvSets ?? []).map((s) => Array.from(s)),
        indices: Array.from(g.indices ?? []),
        numVertices: g.numVertices, numTriangles: g.numTriangles,
        // runtime fingerprints (server-computed; the client re-hashes via
        // crypto.subtle and refuses mismatches — same honest pattern as the
        // SceneIR app's verifyGeometryFingerprints)
        vertexPositionsF32leSha256: crypto.createHash('sha256').update(posBytes).digest('hex'),
        triangleIndicesU16leSha256: crypto.createHash('sha256').update(idxBytes).digest('hex'),
      };
    }
    return rec;
  });
  // materials: shape -> its verified NiMaterialProperty (REFERENCE_CONFIRMED ref)
  const byIndex = new Map(ir.blocks.map((b) => [b.index, b]));
  const materials = [];
  for (const mesh of analysis.meshRows) {
    const matBlock = (mesh.propertyRefs ?? [])[0] ?? null;
    const mat = matBlock != null ? byIndex.get(matBlock) : null;
    const f = mat?.fields ?? {};
    materials.push({
      shapeBlock: mesh.shapeBlock, shapeName: mesh.shapeName,
      materialBlock: matBlock, materialName: mat?.name ?? null,
      referenceClass: mat ? 'REFERENCE_CONFIRMED (verified block ref)' : 'NONE',
      diffuse: f.diffuse ? [...f.diffuse] : null,
      ambient: f.ambient ? [...f.ambient] : null,
      specular: f.specular ? [...f.specular] : null,
      emissive: f.emissive ? [...f.emissive] : null,
      shine: f.shine ?? null, alpha: f.alpha ?? null,
    });
  }
  const uvSetTotal = analysis.meshRows.reduce((n, m) => n + (m.uvSets ?? 0), 0);
  return {
    wireVersion: CATALOG_WIRE_VERSION,
    run: 'PE_CITY_ASSET_MAP_R1_20261010',
    phase: 'CATALOG_MODE (phase 4)',
    cacheKey: `catalog-wire-v1|${analysis.asset.era}|${analysis.asset.payloadSha256}|${PEC_NIF41_READER_VERSION}|${CATALOG_WIRE_VERSION}`,
    wireContract:
      'runtime loopback-only data regenerated from the pinned READ_ONLY Models.ark through the phase-3 bounded NIF-4.1 reader — never a committed fixture; no whole-corpus route',
    provenance: {
      era: analysis.asset.era, container: analysis.asset.container,
      containerSha256: CATALOG_PINS.modelsArk.sha256,
      entryName: analysis.asset.entryName, entryIndex: analysis.asset.entryIndex,
      payloadSha256: analysis.asset.payloadSha256, sizeBytes: analysis.asset.sizeBytes,
      readerVersion: PEC_NIF41_READER_VERSION, elapsedMs: null,
    },
    pins: {
      modelId: Number(id),
      payloadSha256: analysis.asset.payloadSha256,
      containerSha256: CATALOG_PINS.modelsArk.sha256,
    },
    asset: {
      assetId: analysis.asset.assetId, era: analysis.asset.era, build: analysis.asset.build,
      container: analysis.asset.container, entryName: analysis.asset.entryName,
      payloadSha256: analysis.asset.payloadSha256, sizeBytes: analysis.asset.sizeBytes,
      nifVersion: analysis.asset.nifVersion, numBlocks: analysis.asset.numBlocks,
      closure: analysis.asset.closure,
    },
    blockTypeCensus: analysis.blockCensus,
    decodeCensus: analysis.decodeCensus,
    roots: analysis.roots,
    hierarchyRows: analysis.hierarchyRows,
    meshRows: analysis.meshRows,
    blocks,
    materials,
    sceneBounds_FILE_SCENE_SPACE: analysis.bounds,
    placementFinding: analysis.placementFinding,
    textureDiagnostics: {
      disposition: 'UNTEXTURED_PROXY_MESH',
      numTexturingProperties: analysis.standardChainPresent.NiTexturingProperty,
      numSourceTextures: analysis.standardChainPresent.NiSourceTexture,
      arkTextureNumTex: 0, // measured on all four (ArkTexture block present, numTex=0)
      uvSets: uvSetTotal,
      perMesh: analysis.meshRows.map((m) => ({
        shapeBlock: m.shapeBlock, shapeName: m.shapeName,
        uvSets: m.uvSets, hasNormals: m.hasNormals, hasColors: m.hasColors,
      })),
      note: 'no texture bindings in the researched 4.1 scope — the preview applies ONLY the verified NiMaterialProperty diffuse colors (material preview); NO fake textures (explicit visual fallback, NOT a textured PASS)',
    },
    validation: {
      ok: analysis.validationOk, errorCount: analysis.validationErrors.length,
      warnings: analysis.validationWarnings,
    },
    policyLabels: {
      space: SPACE_LABEL.space,
      axisConvention: SPACE_LABEL.axisConvention,
      worldPlacement: 'SOURCE_FILE_SCENE_SPACE != WORLD_PLACEMENT — the preview shows FILE-scene geometry only; no historical world placement is claimed (HISTORICAL_PLACEMENT = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO)',
      hypothesis: 'node names are byte-level REPRODUCED Desktop name hypotheses — NOT game classes, NOT city names; MSC/MAC not promoted',
      wrapper: 'presentation wrapper: centering ONLY (applied exactly once at the wrapper; NO unit conversion, NO axis swap, NO double-centering) — original vertex values stay intact; an original-coordinates view mode exists beside fit-to-view',
    },
  };
}
