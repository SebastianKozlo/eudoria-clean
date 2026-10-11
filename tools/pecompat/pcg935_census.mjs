#!/usr/bin/env node
// pcg935_census.mjs — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010 (Wave 1, contract §2)
// FULL-CORPUS CENSUS of the pinned PCG_9_3_5 Models.bnt: enumerate EVERY entry
// from the PHYSICAL BNT2 index, extract each payload, recompute CRC32+SHA256
// per entry, and identify the ACTUAL NIF header version of every entry from
// its bytes. Denominators are RE-MEASURED here — never taken from the frozen
// manifest CSV (which stays untouched derived documentation).
//
// FAIL-CLOSED INPUT IDENTITY: container size + SHA256 verified against the run
// pins before anything else; mismatch = loud exit, no output.
//
// CLOSURE CONTROLS (contract gate 1):
//   - payload ranges: 0 overlaps, 0 gaps vs the payload span [minOffset, dirEnd)
//     — every entry's [offset, offset+size) must fit in the file; adjacent
//     overlap/gap census reported (slack regions are recorded, not interpreted);
//   - directory walk ends EXACTLY at footer-8 (Bnt2Archive enforces this too);
//   - measured payload CRC32 == directory CRC32 for every entry (both recorded);
//   - duplicate entry-name census (expected 0; loud if any);
//   - NIF header version measured per entry (text line + u32 version gate).
//
// RESUMABLE: checkpoints under PRIVATE_OUTPUT_ROOT/pcg935_census/checkpoint.json
// keyed to container SHA256 + tool SHA256; a mismatched checkpoint is refused.
//
// OUTPUT (PRIVATE): census/full_census.json + census/census_summary.json.
'use strict';

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import zlib from 'node:zlib';
import { fileURLToPath } from 'node:url';

import { Bnt2Archive } from '../../src/pesource/Bnt2Archive.js';

export const PCG935_CENSUS_TOOL_VERSION = 'pcg935-census-v1';

export const MODELS_BNT_PINS = Object.freeze({
  path: 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt',
  sizeBytes: 395412868,
  sha256: 'c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0',
  era: 'PCG_9_3_5',
  container: 'Models/Models.bnt',
});

const PRIVATE_ROOT = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010';
const OUT_DIR = path.join(PRIVATE_ROOT, 'census');
const CHECKPOINT = path.join(OUT_DIR, 'checkpoint.json');

const sha256 = (b) => crypto.createHash('sha256').update(b).digest('hex');

/** NIF header sniff (bounded bytes; the version is read from the payload
 * itself, never from an external manifest). */
function sniffNifHeader(payload, entryName) {
  const nl = payload.indexOf(0x0a);
  if (nl < 0) return { headerText: null, versionRaw: null, versionString: 'NO_NEWLINE_NOT_NIF' };
  let headerText = '';
  for (let i = 0; i < nl; i++) headerText += String.fromCharCode(payload[i]);
  if (nl + 8 > payload.length) {
    return { headerText, versionRaw: null, versionString: 'TRUNCATED_VERSION' };
  }
  const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  const versionRaw = dv.getUint32(nl + 1, true);
  const userVersion = dv.getUint32(nl + 5, true);
  let versionString;
  switch (versionRaw) {
    case 0x0A010000: versionString = '10.1.0.0'; break;
    case 0x0401000C: versionString = '4.1.0.12'; break;
    case 0x04000002: versionString = '4.0.0.2'; break;
    default: versionString = `UNKNOWN_0x${versionRaw.toString(16).padStart(8, '0').toUpperCase()}`;
  }
  void entryName;
  return { headerText, versionRaw: `0x${versionRaw.toString(16).padStart(8, '0').toUpperCase()}`, versionString, userVersion };
}

export async function runCensus({ modelsBntPath = MODELS_BNT_PINS.path, outDir = OUT_DIR } = {}) {
  const t0 = Date.now();
  fs.mkdirSync(outDir, { recursive: true });
  // ---- fail-closed container identity ----
  const bytes = new Uint8Array(await fs.promises.readFile(modelsBntPath));
  if (bytes.byteLength !== MODELS_BNT_PINS.sizeBytes) {
    throw new Error(`[census] container size ${bytes.byteLength} != pinned ${MODELS_BNT_PINS.sizeBytes} — REFUSING`);
  }
  const containerSha = sha256(bytes);
  if (containerSha !== MODELS_BNT_PINS.sha256) {
    throw new Error(`[census] container SHA256 ${containerSha} != pinned ${MODELS_BNT_PINS.sha256} — REFUSING`);
  }
  const archive = new Bnt2Archive(bytes);
  const entries = archive.entries();
  console.log(`[census] container OK (${bytes.byteLength} B, ${containerSha.slice(0, 12)}…); entries=${entries.length}`);

  // ---- range controls ----
  let overlaps = 0; let gaps = 0; let beyondEof = 0;
  const dirEnd = archive.dirOffset;
  const sorted = [...entries].sort((a, b) => a.offset - b.offset);
  for (let i = 0; i < sorted.length; i++) {
    const e = sorted[i];
    if (e.offset + e.size > bytes.length) beyondEof++;
    if (i > 0) {
      const prev = sorted[i - 1];
      const prevEnd = prev.offset + prev.size;
      if (e.offset < prevEnd) overlaps++;
      else if (e.offset > prevEnd) gaps++;
    }
  }
  const names = new Set(); let dupNames = 0;
  for (const e of entries) { if (names.has(e.name)) dupNames++; names.add(e.name); }

  // ---- resume checkpoint (provenance-keyed) ----
  const toolSha = sha256(new Uint8Array(await fs.promises.readFile(fileURLToPath(import.meta.url))));
  let done = 0;
  let rows = [];
  let resumeCheckpoint = null;
  if (fs.existsSync(CHECKPOINT)) {
    try {
      const cp = JSON.parse(fs.readFileSync(CHECKPOINT, 'utf8'));
      if (cp.containerSha256 === containerSha && cp.toolSha256 === toolSha && cp.entriesCount === entries.length) {
        resumeCheckpoint = cp;
        rows = cp.rows;
        done = cp.nextIndex;
        console.log(`[census] RESUMING from checkpoint at index ${done}`);
      } else {
        console.log('[census] checkpoint provenance mismatch — restarting from 0 (old checkpoint preserved as checkpoint.stale.json)');
        fs.renameSync(CHECKPOINT, CHECKPOINT + '.stale.json');
      }
    } catch (e) {
      console.log(`[census] checkpoint unreadable (${e.message}) — restarting from 0`);
    }
  }

  // ---- per-entry extraction + hash + version sniff ----
  const crcMismatches = [];
  for (let i = done; i < entries.length; i++) {
    const e = entries[i];
    const payload = bytes.subarray(e.offset, e.offset + e.size);
    const payloadSha = sha256(payload);
    const crc = zlib.crc32(payload) >>> 0;
    const crcMatch = (crc >>> 0) === (e.crc32 >>> 0);
    if (!crcMatch) crcMismatches.push({ name: e.name, dirCrc32: (e.crc32 >>> 0), measured: (crc >>> 0) });
    const hdr = sniffNifHeader(payload, e.name);
    rows.push({
      entryIndex: e.entryIndex,
      name: e.name,
      offset: e.offset,
      sizeBytes: e.size,
      dirCrc32: (e.crc32 >>> 0),
      measuredCrc32: (crc >>> 0),
      crcMatch,
      payloadSha256: payloadSha,
      headerText: hdr.headerText,
      versionRaw: hdr.versionRaw,
      versionString: hdr.versionString,
      userVersion: hdr.userVersion ?? null,
    });
    if ((i + 1) % 500 === 0 || i === entries.length - 1) {
      fs.writeFileSync(CHECKPOINT, JSON.stringify({
        containerSha256: containerSha, toolSha256: toolSha, entriesCount: entries.length,
        nextIndex: i + 1, rows,
      }));
      console.log(`[census] ${i + 1}/${entries.length} (${Math.round((i + 1) / entries.length * 100)}%)`);
    }
  }

  // ---- version census (re-measured; never hardcoded) ----
  const versionCensus = {};
  for (const r of rows) {
    versionCensus[r.versionString] = (versionCensus[r.versionString] ?? 0) + 1;
  }

  const summary = {
    run: 'PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010',
    toolVersion: PCG935_CENSUS_TOOL_VERSION,
    toolSha256: toolSha,
    container: {
      path: modelsBntPath,
      era: MODELS_BNT_PINS.era,
      container: MODELS_BNT_PINS.container,
      sizeBytes: bytes.byteLength,
      sha256: containerSha,
    },
    entriesCount: entries.length,
    rangeControls: { overlaps, gaps, beyondEof, dirEndCheck: 'Bnt2Archive dir-end==footer-8 enforced' },
    duplicateNames: dupNames,
    crcMismatches: crcMismatches.length,
    crcMismatchList: crcMismatches.slice(0, 50),
    versionCensus,
    elapsedMs: Date.now() - t0,
    resumedFrom: resumeCheckpoint ? resumeCheckpoint.nextIndex : 0,
  };
  fs.writeFileSync(path.join(outDir, 'census_summary.json'), JSON.stringify(summary, null, 2));
  fs.writeFileSync(path.join(outDir, 'full_census.json'), JSON.stringify({ summary, entries: rows }, null, 1));
  try { fs.unlinkSync(CHECKPOINT); } catch { /* fine */ }
  console.log(`[census] DONE entries=${entries.length} versions=${JSON.stringify(versionCensus)} crcMismatch=${crcMismatches.length} overlaps=${overlaps} gaps=${gaps} elapsed=${summary.elapsedMs}ms`);
  return { summary, entries: rows };
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  runCensus().catch((e) => {
    console.error(`[census] FATAL: ${e?.stack ?? e}`);
    process.exit(1);
  });
}
