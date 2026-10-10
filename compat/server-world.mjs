#!/usr/bin/env node
// server-world.mjs -- PE_WORLD_LAUNCHER_R1_20261010, ETAP C (contract §4 first paragraph)
// THE bounded LOOPBACK WORLD SERVER serving /launcher, /world and the
// index-derived world APIs.
//
// DESIGN (path denial BY CONSTRUCTION — EXTENDS the proven
// compat/server-catalog.mjs design, which itself extends the sceneir server;
// REUSE LABEL: same deny()/serveBytes() shape, same exact-allowlist static
// maps, same jailed three-subtree reader, same verified-free-port +
// fail-closed startup pattern, same GET/HEAD-only surface. The catalog and
// sceneir servers stay byte-identical and untouched):
//   - Binds 127.0.0.1 ONLY (loopback; the bind address is not configurable).
//   - PORT: env PEWORLD_PORT || default 8162 (contract §0). Ports 8140/8161
//     are REFUSED EXPLICITLY (the foreign standing servers own them and are
//     NEVER touched). A busy port is a LOUD failure — this server never
//     replaces another process.
//   - Static surface = EXACT ALLOWLIST MAPS (the request URL never becomes a
//     filesystem path): the launcher/world app files, the shared compat
//     stylesheet, the three client-side world modules, and the pinned three
//     package (jailed subtree).
//   - Data APIs (all index-derived, bounded; NO arbitrary filesystem reads,
//     NO whole-container downloads — the 125 MB terrain.bnt / 395 MB
//     Models.bnt / 974 MB Textures.bnt are NEVER exposed to the browser):
//       GET /api/world/status            — identity + census + stage snapshot
//       GET /api/world/overview          — per-regular-tile stats BINARY
//                                          (u16 mean/min/max + u8 status,
//                                          220x236 row-major, 7 B/tile —
//                                          partial responses allowed, PENDING
//                                          status bytes visible)
//       GET /api/world/overview/progress — census progress (measured/total…)
//       GET /api/world/tile/<gx>/<gy>   — RAW heights of ONE tile (2048 B,
//                                          uint16 LE, 32x32) + provenance
//                                          headers; grid 0..219/0..235 ONLY
//                                          (sentinel + special rows are NOT
//                                          addressable — loud refusals)
//       GET /api/world/tile/<gx>/<gy>/meta — provenance + stats of one tile
//       GET /api/world/tile/<gx>/<gy>/materials — ETAP D: the decoded material
//                                          tail of one tile (named material
//                                          records in RECORD ORDER with the
//                                          RAW 16x16 masks at record+56,
//                                          base64; per-material resolved
//                                          <id>.dat texture entry; system
//                                          records carried with UNVERIFIED
//                                          labels; sums; provenance)
//       GET /api/world/texture/<id>     — ETAP D: ONE bounded texture payload
//                                          ('<id>.dat' from the pinned PCG
//                                          Textures.bnt, LAZY single-entry
//                                          file reads — NEVER the whole
//                                          974 MB container, never an
//                                          arbitrary-path read); era gate:
//                                          ?era=PCG_9_3_5 only, every other
//                                          era label is REFUSED
//       GET /api/world/climates         — 32 .vcl profile census (honest
//                                          UNSUPPORTED rows kept UNSUPPORTED;
//                                          ETAP E: DECODED profiles carry
//                                          the per-record MODEL SUMMARY —
//                                          the REAL ids/scales)
//       GET /api/world/climate/<i>      — one decoded profile (0..31)
//       GET /api/world/model/<id>       — ETAP E: ONE bounded model NIF
//                                          payload ('<id>.nif' from the
//                                          pinned PCG Models.bnt, LAZY
//                                          single-entry file reads — NEVER
//                                          the whole 395 MB container, never
//                                          an arbitrary-path read; the
//                                          measured default-profile support
//                                          census lives in
//                                          /api/world/status .vegetation)
//       GET /api/world/gaps             — honest NOT-loaded / NOT_YET panel
//   - TERRAIN DATA PATH: PESourceMount.getTerrainTile (era PCG_9_3_5, BNT2
//     terrain framing, TDF offset-64 heights, RAW uint16 — the production
//     path, NO parallel decoder). The server-side census measures every
//     regular tile from the ORIGINAL bytes (min/max/mean/status).
//   - MATERIAL DATA PATH (ETAP D): PESourceMount.getTerrainMaterials (the
//     ACTIVE TdfMaterialTailDecoder: named material records, mask at
//     record+56 — fields 52..55 are extra4, NOT mask; stride size+4; RAW or
//     RLE (count,value) exact consumption; INDEPENDENT per-layer weights,
//     sums > 255 preserved as ORIGINAL DATA). The material->texture relation
//     is the id@+16 -> '<id>.dat' Textures.bnt entry chain (engine-RE
//     CONFIRMED: the 9.3.5 record parse reads sub@+16 as the material's
//     TEXTURE id — M1_TSFS_BINARY_FORENSICS iter015e/iter030, EU935 census
//     GROUND_TEXTURES §3 "Material-id -> texture chain CONFIRMED"; re-verified
//     on the sampled tiles of THIS run). materialId==textureId is therefore
//     NOT an assumption here — it is the carried-forward engine-RE relation,
//     re-measured per sample; an id with NO '<id>.dat' entry is an explicit
//     UNRESOLVED binding (loud diagnostic, never a fallback texture).
//   - TEXTURES CONTAINER (ETAP D): the pinned Textures.bnt is verified by
//     stream-hash at startup (fail-closed pin) and then mounted as a LAZY
//     BOUNDED reader (footer + directory parse only; per-entry single reads
//     with a size guard). It is NEVER loaded whole into memory and NEVER
//     served whole (no whole-container route exists BY CONSTRUCTION).
//   - CACHE IDENTITY (CAM-C3 discipline applies to EVERY cached payload):
//     the decoded-tile cache is keyed on the FULL identity
//     (era | container | containerSha256 | entryName) and every HIT is
//     re-verified (era, container, container SHA, entry name, payload SHA of
//     the heights bytes, decoder version) against the live mount identity;
//     a mismatch is a CONTROLLED REFUSAL of that cache entry + regeneration
//     from the original bytes, with the named reason counted and exposed.
//     THE SAME DISCIPLINE is applied to the ETAP D caches: the materials
//     cache (payload SHA recomputed over the cached TAIL bytes) and the
//     texture cache (payload SHA recomputed over the cached texture bytes).
//   - MODELS (ETAP E): the pinned Models.bnt is stream-hash verified
//     (fail-closed) and then mounted as a LAZY BOUNDED reader (footer +
//     directory parse only; per-entry single reads with a size guard). It is
//     NEVER loaded whole into memory and NEVER served whole (no
//     whole-container route exists BY CONSTRUCTION). The MEASURED
//     default-profile support census (bounded: the default profile's ~10
//     distinct models parsed with the EXISTING qualified importer + strict
//     texture decode) runs once both lazy indexes are READY and is exposed
//     in /api/world/status .vegetation.
//
// START:  npm run serve:world        (env PEWORLD_PORT, default 8162)
// STOP:   terminate the printed PID (Ctrl+C in the owning console, or
//         Stop-Process -Id <PID> / child.kill() from a harness) — this
//         terminates ONLY this process.
// The startup line is:  world server http://127.0.0.1:<PORT>/ pid=<PID> READY
//
// IMPORT-SAFE for tests: this module only starts the server when executed as
// the main script; importing { createWorldApp, buildWorldRuntime,
// verifyTileCacheIdentity, WORLD_* } has no side effects.

'use strict';
import http from 'node:http';
import net from 'node:net';
import path from 'node:path';
import fs from 'node:fs';
import { promises as fsp } from 'node:fs';
import zlib from 'node:zlib';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';

import { PESourceMount, PESOURCE_DECODER_VERSION } from '../src/pesource/PESourceMount.js';
import { ERAS } from '../src/pesource/PEProvenance.js';
import { HEIGHT_SCALE_CALIBRATION } from '../src/pesource/TerrainTile.js';
import { Bnt2TerrainArchive } from '../src/pesource/Bnt2TerrainArchive.js';
import { isSentinelName } from '../src/pesource/TdfDecoder.js';
import { parseWitnessModel } from '../src/pesource/NifModelReader.js';
import { decodeTga2, decodeTga2A32Image } from '../src/pesource/TgaDecoder.js';
import {
  VEGETATION_THREE_WAY_SEPARATION, LABSEED_WINDOW_CALIBRATION,
} from '../src/peworld/PEFoliageLabSeed.js';

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url))); // repo root
const RUN_ID = 'PE_WORLD_LAUNCHER_R1_20261010';
const SERVER_VERSION = 'world-server-r1-etap-e (loopback, allowlist statics, bounded index-derived world APIs; extends the catalog/sceneir server design; terrain through PESourceMount.getTerrainTile — raw u16, offset 64, filename-xy grid; ETAP D: per-tile material tails (mask@record+56, raw weights) + the id@+16 -> "<id>.dat" texture chain through the LAZY bounded pinned-Textures.bnt reader, CAM-C3 identity on every cache; ETAP E: /api/world/model/<id> bounded NIF payloads through the LAZY pinned-Models.bnt reader + the measured default-profile support census (parseWitnessModel + strict texture decode) + the per-profile .vcl model summaries)';

// ---- configured inputs (the ONLY filesystem paths this server may read) ----
const FOREIGN_STANDING_PORTS = [8140, 8161]; // standing sceneir + catalog servers — NEVER bound over
const PCG_DATA = 'D:\\Eudoria_Reconstruction\\pcg_install\\Data';
const CONFIG = {
  bind: '127.0.0.1',
  port: Number(process.env.PEWORLD_PORT) || 8162,
  threeRoot: process.env.PEWORLD_THREE_ROOT || process.env.PECOMPAT_THREE_ROOT ||
    'D:\\Eudoria_Reconstruction\\12_WebGame\\eudoria-clean\\node_modules\\three',
  threePinnedVersion: '0.185.0',
  terrainPath: process.env.PEWORLD_TERRAIN ?? `${PCG_DATA}\\Terrain\\terrain.bnt`,
  vclPath: process.env.PEWORLD_VCL ?? `${PCG_DATA}\\VegetationClimates\\VegetationClimates.bnt`,
  texturesPath: process.env.PEWORLD_TEXTURES ?? `${PCG_DATA}\\Textures\\Textures.bnt`,
  modelsPath: process.env.PEWORLD_MODELS ?? `${PCG_DATA}\\Models\\Models.bnt`,
  catalogUrl: process.env.PEWORLD_CATALOG_URL ?? 'http://127.0.0.1:8161/catalog',
  // pinned container SHA256 (contract §1 table; verified fail-closed)
  pins: {
    terrain: '95841761CE4EA074C97930EC1CEF3FB57AAC7F7F4F3D9B751A9EE60510299990',
    vegetation: '7B858401C3EEBDA574DF4B4517E7FB2A8149C283885F27187682AA1239C745F4',
    textures: '61ACD13B140E130647EEE24C1E2669D3734990B76CF74897DDD3BA0F4EA61393',
    models: 'C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0',
  },
  tileCacheCapacity: 4096, // decoded-tile LRU (heights 2048 B each → ≤8 MiB)
  materialsCacheCapacity: 512, // per-tile material decodes (tail + served object; ≤64 active tiles × LRU)
  modelsCacheCapacity: 64, // model NIF payloads (bounded; the active window needs ~10)
  textureCacheCapacity: 64, // texture payloads (~196 KB each → ≤12.6 MiB; the active window needs ~23)
  logRequests: process.env.WORLD_LOG_REQUESTS === '1',
};

export const WORLD_ERA = ERAS.PCG_9_3_5;
export const WORLD_TERRAIN_CONTAINER = 'Terrain/terrain.bnt';
export const WORLD_VCL_CONTAINER = 'VegetationClimates/VegetationClimates.bnt';
export const WORLD_GRID = Object.freeze({ width: 220, height: 236 }); // regular filename-xy tiles
export const WORLD_TILE_SAMPLES = 32; // 32x32 samples per tile (disjoint, no overlap)
export const WORLD_HEIGHTS_BYTES = WORLD_TILE_SAMPLES * WORLD_TILE_SAMPLES * 2; // 2048
// /api/world/overview binary layout (fixed, documented in WORLD_DATA_PROVENANCE):
//   for t = gridY * 220 + gridX (gridY 0..235, gridX 0..219):
//     [u16 LE mean][u16 LE min][u16 LE max][u8 status]
//   status: 0=PENDING 1=MEASURED 2=NODATA_MISSING_ENTRY 3=NODATA_DECODE_FAILED
export const WORLD_OVERVIEW_LAYOUT = Object.freeze({
  bytesPerTile: 7, mean: 'uint16 LE', min: 'uint16 LE', max: 'uint16 LE',
  status: 'uint8', rowMajor: true, gridWidth: WORLD_GRID.width,
  statusValues: { PENDING: 0, MEASURED: 1, NODATA_MISSING_ENTRY: 2, NODATA_DECODE_FAILED: 3 },
});
export const WORLD_CALIBRATION = Object.freeze({
  u16PerMeter: HEIGHT_SCALE_CALIBRATION.u16PerMeter, // 128
  meterPerSample: 2,
  minMax: 'identity lerp (min=0, max=65535 in u16 space) — per-tile min/max source UNRESOLVED',
  label: 'CURRENT_RUNTIME_CALIBRATION',
  evidenceStatus: HEIGHT_SCALE_CALIBRATION.evidenceStatus,
  reversibility: 'meters × 128 → raw u16 (exact for stored samples; applied EXACTLY ONCE in PETerrainCore.buildGeometry)',
});

// EXACT static allowlists (request URL -> fixed repo file; no user-derived path).
const WORLD_FILES = Object.freeze({
  'launcher.html': 'compat/launcher.html',
  'launcher.js': 'compat/launcher.js',
  'launcher.css': 'compat/launcher.css',
  'world.html': 'compat/world.html',
  'world-app.js': 'compat/world-app.js',
  'world-vegetation.js': 'compat/world-vegetation.js',
  'world.css': 'compat/world.css',
  'world-splat.js': 'compat/world-splat.js',
  'compat.css': 'compat/compat.css',
});
// Client-side world modules (served EXACT — the world app builds canonical
// TerrainTile objects in the browser from the tile API payload; the
// server-side extraction chain (Bnt2TerrainArchive internals, TdfDecoder)
// is NOT publicly routed beyond these modules). ETAP D adds the production
// TGA decoder (src/pesource/TgaDecoder.js) so the BROWSER decodes the texture
// payloads with the SAME validated decoder (no second decoder, no divergence).
// ETAP E adds: the single-witness qualified NIF reader (src/pesource/
// NifModelReader.js — the browser parses model payloads with the SAME
// production reader; NO guard widening client-side) + the byte-locked
// PEFoliageCore (the RECOVERED_RNG_ARITHMETIC module, imported untouched) +
// the documented LAB_SEED wrapper (src/peworld/PEFoliageLabSeed.js).
const CLIENT_MODULES = Object.freeze([
  'src/peworld/PETerrainCore.js',
  'src/peworld/PEFoliageCore.js',
  'src/peworld/PEFoliageLabSeed.js',
  'src/pesource/TerrainTile.js',
  'src/pesource/PEProvenance.js',
  'src/pesource/TgaDecoder.js',
  'src/pesource/NifModelReader.js',
]);

const MIME = {
  '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.html': 'text/html', '.json': 'application/json', '.css': 'text/css',
  '.map': 'application/json', '.txt': 'text/plain',
};

// ---------------------------------------------------------------------------
// request plumbing (REUSE LABEL: server-catalog.mjs deny()/serveBytes())
// ---------------------------------------------------------------------------
function deny(res, status, error, message, requestPath) {
  const body = JSON.stringify({ ok: false, error, message, requestPath: requestPath ?? null });
  res.writeHead(status, { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' });
  res.end(body);
  return body.length;
}

function serveBytes(res, status, bytes, contentType, extraHeaders = {}) {
  res.writeHead(status, {
    'Content-Type': contentType,
    'Cache-Control': 'no-store',
    'Content-Length': bytes.length,
    ...extraHeaders,
  });
  res.end(bytes);
}

async function readRepoFile(rel) {
  return fsp.readFile(path.join(ROOT, rel));
}

/** Jail-checked read inside the configured three package root (REUSE LABEL:
 * * the sceneir/catalog servers' proven readThreeSub design). Returns
 * {bytes} | {denyStatus, denyError, denyMessage} — never an escape. */
async function readThreeSub(sub) {
  if (sub.includes('..') || sub.includes('\\') || sub.includes('\0') || sub.includes('%')) {
    return { denyStatus: 403, denyError: 'PATH_TRAVERSAL_BLOCKED', denyMessage: 'three-package route refuses traversal/encoded/absolute escape attempts (allowlist-jailed subtree)' };
  }
  const abs = path.normalize(path.join(CONFIG.threeRoot, sub));
  const rootWithSep = CONFIG.threeRoot.endsWith(path.sep) ? CONFIG.threeRoot : CONFIG.threeRoot + path.sep;
  if (abs !== CONFIG.threeRoot && !abs.startsWith(rootWithSep)) {
    return { denyStatus: 403, denyError: 'PATH_TRAVERSAL_BLOCKED', denyMessage: 'resolved path escaped the configured three package root' };
  }
  try {
    const st = await fsp.stat(abs);
    if (!st.isFile()) return { denyStatus: 404, denyError: 'NOT_A_FILE', denyMessage: 'the three-package route serves files only' };
    return { bytes: await fsp.readFile(abs) };
  } catch {
    return { denyStatus: 404, denyError: 'THREE_FILE_NOT_FOUND', denyMessage: 'no such file inside the configured three package root' };
  }
}

// ---------------------------------------------------------------------------
// ETAP E — the vegetation model route + the LAZY bounded Models.bnt index
// (REUSE LABEL: the LazyTextureArchive design, applied to Models.bnt —
// footer + directory parse after the FAIL-CLOSED stream-hash pin verifies;
// per-entry single reads with a size guard; NEVER the whole 395 MB container)
// ---------------------------------------------------------------------------

export const MODEL_WIRE_VERSION = 'bnt2-model-wire-v1';
const MODEL_MAX_ENTRY_BYTES = 32 * 1024 * 1024; // bounded single-entry read guard

/** CAM-C3 cache-identity gate for ONE cached MODEL payload (exported for
 * tests): era + container + containerSha256 + entryName + payload SHA
 * (recomputed over the cached NIF bytes) + wire version. Any mismatch =
 * CONTROLLED REFUSAL with named reasons. */
export function verifyModelCacheIdentity(cacheEntry, mountIdentity, { expectedEntryName = null } = {}) {
  const reasons = [];
  if (!cacheEntry || !cacheEntry.identity || !(cacheEntry.payload instanceof Uint8Array)) {
    return { ok: false, reasons: ['CACHE_ENTRY_MALFORMED'] };
  }
  const id = cacheEntry.identity;
  if (id.era !== mountIdentity.era) reasons.push('ERA_MISMATCH');
  if (id.container !== mountIdentity.container) reasons.push('CONTAINER_MISMATCH');
  if (String(id.containerSha256 ?? '').toLowerCase() !== String(mountIdentity.containerSha256 ?? '').toLowerCase()) {
    reasons.push('CONTAINER_SHA_MISMATCH');
  }
  if (expectedEntryName !== null && id.entryName !== expectedEntryName) reasons.push('ENTRY_NAME_MISMATCH');
  if (id.wireVersion !== MODEL_WIRE_VERSION) reasons.push('WIRE_VERSION_MISMATCH');
  const actualPayloadSha = createHash('sha256')
    .update(Buffer.from(cacheEntry.payload.buffer, cacheEntry.payload.byteOffset, cacheEntry.payload.byteLength))
    .digest('hex');
  if (String(id.payloadSha256 ?? '').toLowerCase() !== actualPayloadSha.toLowerCase()) {
    reasons.push('PAYLOAD_SHA_MISMATCH');
  }
  return { ok: reasons.length === 0, reasons };
}

/** LazyModelArchive — the BOUNDED lazy reader for the pinned PCG Models.bnt
 * (395,412,868 B; BNT2 framing, payloads stored RAW — no zlib). REUSE LABEL:
 * the LazyTextureArchive design (footer + directory parse once, per-entry
 * single bounded reads). Entry names are '<modelId>.nif'. This class is the
 * ONLY code in this server that reads the Models.bnt file. */
export class LazyModelArchive {
  constructor(filePath, { containerSha256 }) {
    this.filePath = filePath;
    this.containerSha256 = containerSha256;
    this.handle = null;
    this.byName = new Map();
    this.byId = new Map();
    this.footer = null;
    this.fileSize = null;
  }
  async openAndParseIndex() {
    this.handle = await fsp.open(this.filePath, 'r');
    const st = await this.handle.stat();
    this.fileSize = st.size;
    if (this.fileSize < 16) throw new Error(`[LazyModelArchive] ${this.filePath} too small (${this.fileSize} B)`);
    const footer = Buffer.alloc(8);
    await this.handle.read(footer, 0, 8, this.fileSize - 8);
    const dirOffset = footer.readUInt32LE(0);
    const magic = footer.subarray(4, 8).toString('latin1');
    if (magic !== 'BNT2') throw new Error(`[LazyModelArchive] footer magic ${JSON.stringify(magic)} != 'BNT2' — REFUSING to serve models`);
    const dirBytes = this.fileSize - dirOffset - 8;
    if (dirBytes <= 4 || dirBytes > 16 * 1024 * 1024) {
      throw new Error(`[LazyModelArchive] implausible directory size ${dirBytes} B @ ${dirOffset}`);
    }
    const dir = Buffer.alloc(dirBytes);
    await this.handle.read(dir, 0, dirBytes, dirOffset);
    const dv = new DataView(dir.buffer, dir.byteOffset, dir.byteLength);
    const count = dv.getUint32(0, true);
    let p = 4;
    const ids = [];
    while (p < dir.length) {
      let end = p;
      while (end < dir.length && dir[end] !== 0x0a) end++;
      if (end >= dir.length) throw new Error(`[LazyModelArchive] unterminated entry name at ${p}`);
      const name = dir.toString('latin1', p, end);
      if (end + 1 + 16 > dir.length) throw new Error(`[LazyModelArchive] truncated entry header for ${name}`);
      const size = dv.getUint32(end + 1, true);
      const offset = dv.getUint32(end + 5, true);
      const crc32 = dv.getUint32(end + 9, true);
      const entry = { name, size, offset, crc32 };
      this.byName.set(name, entry);
      const m = /^(\d+)\.nif$/i.exec(name);
      if (m) { this.byId.set(parseInt(m[1], 10), entry); ids.push(parseInt(m[1], 10)); }
      p = end + 17;
    }
    if (p !== dir.length) {
      throw new Error(`[LazyModelArchive] directory consumption ${p} != ${dir.length} (count field ${count}, parsed ${this.byName.size})`);
    }
    this.footer = { magic, dirOffset, dirBytes, countField: count, parsedEntries: this.byName.size };
    return this.footer;
  }
  entryById(id) { return this.byId.get(id) ?? null; }
  entryByName(name) { return this.byName.get(name) ?? null; }
  /** ONE bounded entry read (RAW payload; size-guarded; bounds-checked). */
  async readEntry(entry) {
    if (entry.size < 0 || entry.size > MODEL_MAX_ENTRY_BYTES) {
      throw new Error(`[LazyModelArchive] entry ${entry.name} size ${entry.size} outside the bounded read guard (<= ${MODEL_MAX_ENTRY_BYTES} B) — REFUSING`);
    }
    if (entry.offset < 0 || entry.offset + entry.size > this.fileSize) {
      throw new Error(`[LazyModelArchive] entry ${entry.name} beyond EOF (offset ${entry.offset} + size ${entry.size} > ${this.fileSize})`);
    }
    const buf = Buffer.alloc(entry.size);
    const { bytesRead } = await this.handle.read(buf, 0, entry.size, entry.offset);
    if (bytesRead !== entry.size) {
      throw new Error(`[LazyModelArchive] short read for ${entry.name}: ${bytesRead} != ${entry.size}`);
    }
    return { payload: new Uint8Array(buf), entry };
  }
  stats() {
    let idMin = null, idMax = null;
    for (const id of this.byId.keys()) {
      if (idMin === null || id < idMin) idMin = id;
      if (idMax === null || id > idMax) idMax = id;
    }
    return { path: this.filePath, containerSha256: this.containerSha256, fileSize: this.fileSize, ...this.footer, numericIdCount: this.byId.size, idMin, idMax };
  }
  async close() { if (this.handle) { await this.handle.close(); this.handle = null; } }
}

/** The strict texture-decode dispatch for a MODEL texture payload (Etap E):
 * bpp 32 -> decodeTga2A32Image (IMAGE order — the model-witness UV
 * convention), bpp 24 -> decodeTga2 (the terrain-texture subset). Anything
 * else fails LOUDLY with the strict decoder's own message (the caller records
 * the honest UNRESOLVED texture chain — never a fallback texture). */
export function decodeModelTextureStrict(payload) {
  if (!(payload instanceof Uint8Array) || payload.length < 18) {
    throw new Error('[decodeModelTextureStrict] payload too small for a TGA header');
  }
  const bpp = payload[16];
  if (bpp === 32) {
    const d = decodeTga2A32Image(payload);
    return { bpp, width: d.width, height: d.height, rgba: d.rgba, decoder: 'decodeTga2A32Image (TGA2 A32 IMAGE order — the model-witness UV convention, row 0 = visual TOP)' };
  }
  if (bpp === 24) {
    const d = decodeTga2(payload);
    return { bpp, width: d.width, height: d.height, rgba: d.rgba, decoder: 'decodeTga2 (TGA2 24bpp — the terrain-texture subset)' };
  }
  throw new Error(`[decodeModelTextureStrict] bpp ${bpp} outside the strict model-texture subset {24, 32} — the payload fails LOUDLY (no fallback, no cross-era substitution)`);
}

/**
 * buildVegetationSupportCensus — the MEASURED default-profile support census
 * (contract §6.1/§6.2: the default profile must be justified by a real
 * measurement — valid profile, non-empty records, at least one supported
 * model in the same era). For the CHOSEN default profile's DISTINCT model
 * ids (bounded: ~10 lazy reads): lazy-read '<id>.nif' from the pinned PCG
 * Models.bnt, parse with the EXISTING QUALIFIED importer (NifModelReader.
 * parseWitnessModel — the single-witness reader's guards are NEVER widened),
 * and resolve each parsed shape's Ark texture binding against the parsed
 * pinned Textures.bnt index + the STRICT texture decoders. Per model:
 * SUPPORTED (parsed; textures resolved) / SUPPORTED_UNTEXTURED (parsed;
 * texture chain unresolved — honest untextured) / UNSUPPORTED (the qualified
 * importer refused — honest count, never guard removal). The ARK 9-byte tail
 * is consumed by the READER (its canon decode rule) and stays RAW-ONLY in
 * this census (never re-interpreted here).
 */
export async function buildVegetationSupportCensus({ modelArchive, textureArchive, records }) {
  const distinctIds = [...new Set(records.map((r) => r[0] | 0))];
  const models = [];
  for (const id of distinctIds) {
    const entryName = `${id}.nif`;
    const entry = modelArchive.entryByName(entryName);
    if (!entry) {
      models.push({ modelId: id, status: 'UNSUPPORTED', reason: `NO "${entryName}" entry in the pinned ${WORLD_ERA} Models.bnt index (parsed ${modelArchive.stats().parsedEntries} entries) — the qualified importer never sees a payload (honest UNSUPPORTED, no substitution)` });
      continue;
    }
    let payload;
    try {
      payload = (await modelArchive.readEntry(entry)).payload;
    } catch (e) {
      models.push({ modelId: id, status: 'UNSUPPORTED', reason: `bounded read failed: ${String(e?.message ?? e)}` });
      continue;
    }
    let extraction = null;
    try {
      extraction = parseWitnessModel(payload, entryName).extraction;
    } catch (e) {
      models.push({
        modelId: id, status: 'UNSUPPORTED', entryBytes: entry.size,
        reason: `the qualified importer (NifModelReader, single-witness guards) refused LOUDLY: ${String(e?.message ?? e).slice(0, 300)}`,
      });
      continue;
    }
    // Per-shape chains from the extraction (the reader's own parsed blocks;
    // the reader file itself is untouched). Shapes without a texprop->Ark
    // chain are the untextured collision/bounds candidates (carried, counted,
    // never rendered as visual geometry).
    const blocks = extraction.blocks;
    const arkBlocks = blocks.filter((b) => b.type === 'NiArkTextureExtraData');
    const shapes = blocks.filter((b) => b.type === 'NiTriShape');
    const shapeChains = [];
    for (const s of shapes) {
      const texprop = (s.fields.properties ?? []).map((i) => blocks[i]).find((b) => b?.type === 'NiTexturingProperty');
      if (!texprop) { shapeChains.push({ shapeIndex: s.index, shapeName: s.fields.name, status: 'NON_VISUAL_NO_TEXPROP' }); continue; }
      const arkEntry = arkBlocks.flatMap((ab) => ab.fields.entries).find((e) => e.ref === texprop.index);
      if (!arkEntry) { shapeChains.push({ shapeIndex: s.index, shapeName: s.fields.name, texpropIndex: texprop.index, status: 'NO_ARK_BINDING' }); continue; }
      shapeChains.push({ shapeIndex: s.index, shapeName: s.fields.name, texpropIndex: texprop.index, arkEntryName: arkEntry.name, textureId: arkEntry.textureId, status: 'BOUND' });
    }
    // Distinct BOUND texture ids -> resolve + STRICT decode each (bounded).
    const textures = [];
    for (const chain of shapeChains.filter((c) => c.status === 'BOUND')) {
      if (textures.some((t) => t.textureId === chain.textureId)) continue;
      const texEntryName = `${chain.textureId}.dat`;
      const texEntry = textureArchive ? textureArchive.entryByName(texEntryName) : null;
      if (!texEntry) {
        textures.push({ textureId: chain.textureId, resolved: false, reason: `NO "${texEntryName}" entry in the pinned ${WORLD_ERA} Textures.bnt index — UNRESOLVED binding (honest untextured, never a fallback texture)` });
        continue;
      }
      try {
        const texPayload = (await textureArchive.readEntry(texEntry)).payload;
        const dec = decodeModelTextureStrict(texPayload);
        textures.push({ textureId: chain.textureId, resolved: true, bytes: texEntry.size, width: dec.width, height: dec.height, bpp: dec.bpp, decoder: dec.decoder });
      } catch (e) {
        textures.push({ textureId: chain.textureId, resolved: false, reason: `STRICT decode refused: ${String(e?.message ?? e).slice(0, 220)} (honest untextured — the payload stays outside the strict subset)` });
      }
    }
    const allTexturesResolved = textures.length > 0 && textures.every((t) => t.resolved);
    const visualShapes = shapeChains.filter((c) => c.status === 'BOUND').length;
    models.push({
      modelId: id, status: allTexturesResolved ? 'SUPPORTED' : 'SUPPORTED_UNTEXTURED',
      entryBytes: entry.size, nifBlocks: extraction.blocks.length,
      nifVersion: extraction.header.versionString,
      shapesTotal: shapes.length, visualShapes, nonVisualShapes: shapes.length - visualShapes,
      textureIds: [...new Set(shapeChains.filter((c) => c.status === 'BOUND').map((c) => c.textureId))],
      textures,
      supportNote: allTexturesResolved
        ? 'parsed by the EXISTING qualified importer; every bound Ark texture resolved + strict-decoded (same-era PCG_9_3_5 chain)'
        : 'parsed by the EXISTING qualified importer; the texture chain is UNRESOLVED (strict decoder subset) — rendered honestly untextured with a diagnostic, never a fallback texture',
    });
  }
  const supported = models.filter((m) => m.status === 'SUPPORTED').length;
  const supportedUntextured = models.filter((m) => m.status === 'SUPPORTED_UNTEXTURED').length;
  const unsupported = models.filter((m) => m.status === 'UNSUPPORTED').length;
  return {
    models,
    counts: {
      distinctModels: models.length, supported, supportedUntextured, unsupported,
      atLeastOneSupportedModel: supported + supportedUntextured > 0,
    },
    importer: 'NifModelReader.parseWitnessModel (the EXISTING single-witness qualified importer; guards NEVER widened; v10.1.0.0 + the KNOWN_V10_TYPES set — anything else fails LOUDLY and counts as UNSUPPORTED)',
    importerScopeNote: 'the reader was cross-validated BIT-EXACTLY for the 457485 witness; other models parse through the SAME guards with per-model parse outcomes measured here (no new block types, no guard removal)',
    textureChain: 'NiArkTextureExtraData entry (trailing 9-byte tail decoded by the READER canon rule [0x00][0xFFFFFFFF][u32 LE textureId]; the tail itself stays RAW-ONLY — never re-interpreted) -> textureId -> "<id>.dat" in the pinned same-era Textures.bnt -> decodeModelTextureStrict (decodeTga2A32Image 32bpp / decodeTga2 24bpp)',
  };
}


export function makeNodeIo() {
  return {
    readFile: async (p) => new Uint8Array(await fsp.readFile(p)),
    inflate: async (bytes) => new Uint8Array(zlib.inflateSync(bytes)),
    sha256: async (bytes) => createHash('sha256').update(bytes).digest('hex'),
  };
}

/** CAM-C3 cache-identity gate for ONE cached tile payload (exported for
 * tests). The cache entry must carry the FULL identity envelope; every hit
 * re-verifies era + container + containerSha256 + entryName + payload SHA
 * (recomputed over the cached heights bytes) + decoder version against the
 * LIVE mount identity. Any mismatch = CONTROLLED REFUSAL with named reasons
 * (the caller re-decodes from the ORIGINAL bytes — never a silent use). */
export function verifyTileCacheIdentity(cacheEntry, mountIdentity, { expectedEntryName = null } = {}) {
  const reasons = [];
  if (!cacheEntry || !cacheEntry.identity || !cacheEntry.tile || !cacheEntry.tile.heights) {
    return { ok: false, reasons: ['CACHE_ENTRY_MALFORMED'] };
  }
  const id = cacheEntry.identity;
  const heights = cacheEntry.tile.heights;
  if (id.era !== mountIdentity.era) reasons.push('ERA_MISMATCH');
  if (id.container !== mountIdentity.container) reasons.push('CONTAINER_MISMATCH');
  if (String(id.containerSha256 ?? '').toLowerCase() !== String(mountIdentity.containerSha256 ?? '').toLowerCase()) {
    reasons.push('CONTAINER_SHA_MISMATCH');
  }
  if (expectedEntryName !== null && id.entryName !== expectedEntryName) reasons.push('ENTRY_NAME_MISMATCH');
  if (id.decoderVersion !== PESOURCE_DECODER_VERSION) reasons.push('DECODER_VERSION_MISMATCH');
  // payload SHA — recomputed over the cached bytes (the 256-bit per-payload proof)
  const actualPayloadSha = createHash('sha256')
    .update(Buffer.from(heights.buffer, heights.byteOffset, heights.byteLength))
    .digest('hex');
  if (String(id.payloadSha256 ?? '').toLowerCase() !== actualPayloadSha.toLowerCase()) {
    reasons.push('PAYLOAD_SHA_MISMATCH');
  }
  return { ok: reasons.length === 0, reasons };
}

/** Bounded LRU cache for decoded tile heights, identity-keyed + verified. */
class TileCache {
  constructor(capacity) {
    this.capacity = capacity;
    this.map = new Map(); // key -> {heights, identity, hits, lastUsed}
    this.refusals = [];  // CAM-C3 controlled refusals (bounded ring)
    this.hits = 0; this.misses = 0;
  }
  key(entryName, identity) {
    return `${identity.era}|${identity.container}|${String(identity.containerSha256).toLowerCase()}|${entryName}`;
  }
  get(entryName, identity) {
    const key = this.key(entryName, identity);
    const e = this.map.get(key);
    if (!e) { this.misses++; return null; }
    const v = verifyTileCacheIdentity(e, identity, { expectedEntryName: entryName });
    if (!v.ok) {
      this.map.delete(key);
      if (this.refusals.length > 32) this.refusals.shift();
      this.refusals.push({ key, reasons: v.reasons, at: new Date().toISOString() });
      this.misses++;
      return null; // controlled refusal — caller regenerates from original bytes
    }
    this.hits++;
    e.lastUsed = Date.now();
    // LRU refresh
    this.map.delete(key);
    this.map.set(key, e);
    return e;
  }
  set(entryName, identity, tile) {
    const key = this.key(entryName, identity);
    const heights = tile.heights;
    const payloadSha256 = createHash('sha256').update(
      Buffer.from(heights.buffer, heights.byteOffset, heights.byteLength)).digest('hex');
    const e = {
      tile, // the canonical TerrainTile (raw heights + full provenance)
      identity: {
        era: identity.era, container: identity.container,
        containerSha256: identity.containerSha256, entryName,
        payloadSha256, decoderVersion: PESOURCE_DECODER_VERSION,
      },
      hits: 0, lastUsed: Date.now(), createdAt: Date.now(),
    };
    if (this.map.has(key)) this.map.delete(key);
    this.map.set(key, e);
    while (this.map.size > this.capacity) {
      const oldest = this.map.keys().next().value;
      this.map.delete(oldest);
    }
    return e;
  }
  stats() {
    let bytes = 0;
    for (const e of this.map.values()) bytes += e.tile.heights.byteLength;
    return { size: this.map.size, capacity: this.capacity, bytes, hits: this.hits, misses: this.misses, refusals: this.refusals.length, lastRefusalReasons: this.refusals[this.refusals.length - 1]?.reasons ?? [] };
  }
}

// ---------------------------------------------------------------------------
// ETAP D — the material->texture chain server side (bounded, identity-checked)
// ---------------------------------------------------------------------------

/** The material->texture relation label carried on EVERY served texture (the
 * provenance of the binding — engine RE, NOT a materialId==textureId
 * assumption pulled from thin air; re-measured per sample by the gates). */
export const TEXTURE_CHAIN_RELATION =
  'material record id@+16 -> Textures.bnt entry "<id>.dat" (engine-RE CONFIRMED: the 9.3.5 record parse/dispatch reads sub@+16 as the material TEXTURE id — M1_TSFS_BINARY_FORENSICS_20260906 iter015e/iter015f, consolidated iter030, EU935_WORLD_DATA_CENSUS GROUND_TEXTURES §3 "Material-id -> texture chain CONFIRMED" (probe05); re-verified on THIS RUN\'s sampled tiles: every sampled material id resolves a TGA2 24bpp 256x256 payload)';
/** The ASCII-safe form of the relation for HTTP HEADERS (full text stays in
 * the JSON payloads — header values must be ASCII). */
export const TEXTURE_CHAIN_RELATION_HEADER =
  'material record id@+16 -> Textures.bnt entry "<id>.dat" (engine-RE CONFIRMED: the 9.3.5 record parse reads sub@+16 as the material TEXTURE id - M1_TSFS iter015e/f, iter030, EU935 census GROUND_TEXTURES s3; re-verified on THIS RUN sampled tiles)';

export const TEXTURE_WIRE_VERSION = 'bnt2-texture-wire-v1';
export const MATERIALS_WIRE_VERSION = PESOURCE_DECODER_VERSION + '+material-tail-v1';
const TEXTURE_MAX_ENTRY_BYTES = 8 * 1024 * 1024; // bounded single-entry read guard

/** CAM-C3 cache-identity gate for ONE cached TEXTURE payload (exported for
 * tests). The entry must carry the FULL identity envelope; every hit
 * re-verifies era + container + containerSha256 + entryName + payload SHA
 * (recomputed over the cached bytes) + wire version against the LIVE mount
 * identity. Any mismatch = CONTROLLED REFUSAL with named reasons. */
export function verifyTextureCacheIdentity(cacheEntry, mountIdentity, { expectedEntryName = null } = {}) {
  const reasons = [];
  if (!cacheEntry || !cacheEntry.identity || !(cacheEntry.payload instanceof Uint8Array)) {
    return { ok: false, reasons: ['CACHE_ENTRY_MALFORMED'] };
  }
  const id = cacheEntry.identity;
  if (id.era !== mountIdentity.era) reasons.push('ERA_MISMATCH');
  if (id.container !== mountIdentity.container) reasons.push('CONTAINER_MISMATCH');
  if (String(id.containerSha256 ?? '').toLowerCase() !== String(mountIdentity.containerSha256 ?? '').toLowerCase()) {
    reasons.push('CONTAINER_SHA_MISMATCH');
  }
  if (expectedEntryName !== null && id.entryName !== expectedEntryName) reasons.push('ENTRY_NAME_MISMATCH');
  if (id.wireVersion !== TEXTURE_WIRE_VERSION) reasons.push('WIRE_VERSION_MISMATCH');
  const actualPayloadSha = createHash('sha256')
    .update(Buffer.from(cacheEntry.payload.buffer, cacheEntry.payload.byteOffset, cacheEntry.payload.byteLength))
    .digest('hex');
  if (String(id.payloadSha256 ?? '').toLowerCase() !== actualPayloadSha.toLowerCase()) {
    reasons.push('PAYLOAD_SHA_MISMATCH');
  }
  return { ok: reasons.length === 0, reasons };
}

/** CAM-C3 cache-identity gate for ONE cached MATERIALS decode (exported for
 * tests). The payload SHA is recomputed over the cached TAIL bytes — the
 * source payload of the material decode (the raw weights survive bit-exact
 * or the SHA refuses). */
export function verifyMaterialsCacheIdentity(cacheEntry, mountIdentity, { expectedEntryName = null } = {}) {
  const reasons = [];
  if (!cacheEntry || !cacheEntry.identity || !(cacheEntry.tail instanceof Uint8Array)) {
    return { ok: false, reasons: ['CACHE_ENTRY_MALFORMED'] };
  }
  const id = cacheEntry.identity;
  if (id.era !== mountIdentity.era) reasons.push('ERA_MISMATCH');
  if (id.container !== mountIdentity.container) reasons.push('CONTAINER_MISMATCH');
  if (String(id.containerSha256 ?? '').toLowerCase() !== String(mountIdentity.containerSha256 ?? '').toLowerCase()) {
    reasons.push('CONTAINER_SHA_MISMATCH');
  }
  if (expectedEntryName !== null && id.entryName !== expectedEntryName) reasons.push('ENTRY_NAME_MISMATCH');
  if (id.wireVersion !== MATERIALS_WIRE_VERSION) reasons.push('WIRE_VERSION_MISMATCH');
  const actualTailSha = createHash('sha256')
    .update(Buffer.from(cacheEntry.tail.buffer, cacheEntry.tail.byteOffset, cacheEntry.tail.byteLength))
    .digest('hex');
  if (String(id.payloadSha256 ?? '').toLowerCase() !== actualTailSha.toLowerCase()) {
    reasons.push('PAYLOAD_SHA_MISMATCH');
  }
  return { ok: reasons.length === 0, reasons };
}

/** Bounded LRU cache with the CAM-C3 full-identity verification on every hit
 * (REUSE LABEL: the TileCache discipline, generalized; the verify function is
 * injected so each cache proves its own payload class). A HIT that fails
 * verification is a CONTROLLED REFUSAL: the entry is dropped, the refusal is
 * recorded with named reasons, and the caller regenerates from the ORIGINAL
 * bytes — a cache entry is NEVER silently used on identity mismatch. */
class IdentityCache {
  constructor(capacity, verifyFn, label, payloadBytesFn) {
    this.capacity = capacity;
    this.verifyFn = verifyFn;
    this.label = label;
    this.payloadBytesFn = payloadBytesFn ?? (() => 0);
    this.map = new Map();
    this.refusals = [];
    this.hits = 0; this.misses = 0;
  }
  key(entryName, identity) {
    return `${identity.era}|${identity.container}|${String(identity.containerSha256).toLowerCase()}|${entryName}`;
  }
  get(entryName, identity) {
    const key = this.key(entryName, identity);
    const e = this.map.get(key);
    if (!e) { this.misses++; return null; }
    const v = this.verifyFn(e, identity, { expectedEntryName: entryName });
    if (!v.ok) {
      this.map.delete(key);
      if (this.refusals.length > 32) this.refusals.shift();
      this.refusals.push({ key, reasons: v.reasons, at: new Date().toISOString() });
      this.misses++;
      return { refused: true, reasons: v.reasons }; // controlled refusal — caller regenerates
    }
    this.hits++;
    e.lastUsed = Date.now();
    this.map.delete(key);
    this.map.set(key, e);
    return e;
  }
  set(entryName, identity, entry) {
    const key = this.key(entryName, identity);
    // the ENTRY's own identity envelope (wireVersion + payloadSha256 — the
    // CAM-C3 payload proof) takes precedence; the key identity supplies
    // era|container|containerSha256 and entryName is ENFORCED (a lookup key
    // must never disagree with the stored entry name).
    const full = {
      ...entry,
      identity: { ...identity, ...(entry.identity ?? {}), entryName },
      hits: 0, lastUsed: Date.now(), createdAt: Date.now(),
    };
    if (this.map.has(key)) this.map.delete(key);
    this.map.set(key, full);
    while (this.map.size > this.capacity) {
      const oldest = this.map.keys().next().value;
      this.map.delete(oldest);
    }
    return full;
  }
  stats() {
    let bytes = 0;
    for (const e of this.map.values()) bytes += this.payloadBytesFn(e);
    return { label: this.label, size: this.map.size, capacity: this.capacity, bytes, hits: this.hits, misses: this.misses, refusals: this.refusals.length, lastRefusalReasons: this.refusals[this.refusals.length - 1]?.reasons ?? [] };
  }
}

/**
 * LazyTextureArchive — a BOUNDED file-handle reader for the pinned PCG
 * Textures.bnt (973,942,771 B). REUSE LABEL: the Bnt2Archive framing
 * knowledge (footer [u32 dir_offset]['BNT2']; directory [u32 count][count x
 * (name..0x0A, u32 size, u32 offset, u32 crc32, u32 pad)]; RAW payloads at
 * offset), implemented as LAZY single reads so the 974 MB container is NEVER
 * resident: the footer (8 B) + the directory (~225 KB) are parsed once after
 * the fail-closed stream-hash pin verification, and each read serves ONE
 * bounded entry (size-guarded). This class is the ONLY code in this server
 * that reads the Textures.bnt file.
 */
export class LazyTextureArchive {
  constructor(filePath, { containerSha256 }) {
    this.filePath = filePath;
    this.containerSha256 = containerSha256;
    this.handle = null;
    this.byName = new Map();
    this.byId = new Map();
    this.footer = null;
    this.fileSize = null;
  }
  async openAndParseIndex() {
    this.handle = await fsp.open(this.filePath, 'r');
    const st = await this.handle.stat();
    this.fileSize = st.size;
    if (this.fileSize < 16) throw new Error(`[LazyTextureArchive] ${this.filePath} too small (${this.fileSize} B)`);
    const footer = Buffer.alloc(8);
    await this.handle.read(footer, 0, 8, this.fileSize - 8);
    const dirOffset = footer.readUInt32LE(0);
    const magic = footer.subarray(4, 8).toString('latin1');
    if (magic !== 'BNT2') throw new Error(`[LazyTextureArchive] footer magic ${JSON.stringify(magic)} != 'BNT2' — REFUSING to serve textures`);
    const dirBytes = this.fileSize - dirOffset - 8;
    if (dirBytes <= 4 || dirBytes > 16 * 1024 * 1024) {
      throw new Error(`[LazyTextureArchive] implausible directory size ${dirBytes} B @ ${dirOffset}`);
    }
    const dir = Buffer.alloc(dirBytes);
    await this.handle.read(dir, 0, dirBytes, dirOffset);
    const dv = new DataView(dir.buffer, dir.byteOffset, dir.byteLength);
    const count = dv.getUint32(0, true);
    let p = 4;
    const ids = [];
    while (p < dir.length) {
      let end = p;
      while (end < dir.length && dir[end] !== 0x0a) end++;
      if (end >= dir.length) throw new Error(`[LazyTextureArchive] unterminated entry name at ${p}`);
      const name = dir.toString('latin1', p, end);
      if (end + 1 + 16 > dir.length) throw new Error(`[LazyTextureArchive] truncated entry header for ${name}`);
      const size = dv.getUint32(end + 1, true);
      const offset = dv.getUint32(end + 5, true);
      const crc32 = dv.getUint32(end + 9, true);
      const entry = { name, size, offset, crc32 };
      this.byName.set(name, entry);
      const m = /^(\d+)\.dat$/i.exec(name);
      if (m) { this.byId.set(parseInt(m[1], 10), entry); ids.push(parseInt(m[1], 10)); }
      p = end + 17;
    }
    if (p !== dir.length) {
      throw new Error(`[LazyTextureArchive] directory consumption ${p} != ${dir.length} (count field ${count}, parsed ${this.byName.size})`);
    }
    this.footer = { magic, dirOffset, dirBytes, countField: count, parsedEntries: this.byName.size };
    return this.footer;
  }
  entryById(id) { return this.byId.get(id) ?? null; }
  entryByName(name) { return this.byName.get(name) ?? null; }
  /** ONE bounded entry read (RAW payload; size-guarded; offset+size bounds-checked). */
  async readEntry(entry) {
    if (entry.size < 0 || entry.size > TEXTURE_MAX_ENTRY_BYTES) {
      throw new Error(`[LazyTextureArchive] entry ${entry.name} size ${entry.size} outside the bounded read guard (<= ${TEXTURE_MAX_ENTRY_BYTES} B) — REFUSING`);
    }
    if (entry.offset < 0 || entry.offset + entry.size > this.fileSize) {
      throw new Error(`[LazyTextureArchive] entry ${entry.name} beyond EOF (offset ${entry.offset} + size ${entry.size} > ${this.fileSize})`);
    }
    const buf = Buffer.alloc(entry.size);
    const { bytesRead } = await this.handle.read(buf, 0, entry.size, entry.offset);
    if (bytesRead !== entry.size) {
      throw new Error(`[LazyTextureArchive] short read for ${entry.name}: ${bytesRead} != ${entry.size}`);
    }
    return { payload: new Uint8Array(buf), entry };
  }
  stats() {
    let idMin = null, idMax = null;
    for (const id of this.byId.keys()) {
      if (idMin === null || id < idMin) idMin = id;
      if (idMax === null || id > idMax) idMax = id;
    }
    return { path: this.filePath, containerSha256: this.containerSha256, fileSize: this.fileSize, ...this.footer, numericIdCount: this.byId.size, idMin, idMax };
  }
  async close() { if (this.handle) { await this.handle.close(); this.handle = null; } }
}

/** Stream-hash a large container WITHOUT keeping it in memory (Models.bnt /
 * Textures.bnt are VERIFIED ONLY — not mounted, not decoded, not served). */
async function streamSha256(filePath, { chunkBytes = 8 * 1024 * 1024 } = {}) {
  const hash = createHash('sha256');
  const handle = await fsp.open(filePath, 'r');
  try {
    const buf = Buffer.alloc(chunkBytes);
    for (;;) {
      const { bytesRead } = await handle.read(buf, 0, chunkBytes, null);
      if (bytesRead === 0) break;
      hash.update(bytesRead === chunkBytes ? buf : buf.subarray(0, bytesRead));
    }
  } finally {
    await handle.close();
  }
  return hash.digest('hex').toUpperCase();
}

/**
 * buildWorldRuntime — mount the pinned containers (fail-closed), classify
 * the terrain index, and start the background census + container-verification
 * stages. Returns the shared `state` used by createWorldApp. Never throws
 * on background-stage errors (they are recorded honestly in the status).
 */
export async function buildWorldRuntime({ io = makeNodeIo(), terrainPath = CONFIG.terrainPath, vclPath = CONFIG.vclPath, texturesPath = CONFIG.texturesPath, modelsPath = CONFIG.modelsPath, startBackground = true } = {}) {
  const mount = new PESourceMount(io);
  const terrain = await mount.mountEra({
    era: WORLD_ERA, container: WORLD_TERRAIN_CONTAINER, path: terrainPath,
    format: 'BNT2_TERRAIN', // fail-closed pin from KNOWN_HASHES (§1)
  });
  const vegetation = await mount.mountEra({
    era: WORLD_ERA, container: WORLD_VCL_CONTAINER, path: vclPath, format: 'BNT2',
  });
  const terrainArchive = mount._terrainArchive(WORLD_ERA, WORLD_TERRAIN_CONTAINER);
  const entries = terrainArchive.entries();

  // index classification (measured, not assumed)
  const indexCensus = {
    totalEntries: entries.length,
    regular: 0, specialRows: 0, sentinel: 0, other: 0,
    specialRowYValues: [],
  };
  const names = new Set();
  for (const e of entries) {
    names.add(e.name);
    if (isSentinelName(e.name)) { indexCensus.sentinel++; continue; }
    const m = /^([0-9a-fA-F]{4})([0-9a-fA-F]{4})\.tdf$/.exec(e.name);
    if (!m) { indexCensus.other++; continue; }
    const gx = parseInt(m[1], 16), gy = parseInt(m[2], 16);
    if (gx < WORLD_GRID.width && gy < WORLD_GRID.height) indexCensus.regular++;
    else {
      indexCensus.specialRows++;
      if (!indexCensus.specialRowYValues.includes(gy)) indexCensus.specialRowYValues.push(gy);
    }
  }
  indexCensus.specialRowYValues.sort((a, b) => a - b);

  const identity = {
    era: WORLD_ERA,
    container: WORLD_TERRAIN_CONTAINER,
    containerSha256: terrain.actualSha256 ?? terrain.expectedSha256,
    decoderVersion: PESOURCE_DECODER_VERSION,
  };

  // per-regular-tile overview stats (u16 mean/min/max + status byte)
  const N = WORLD_GRID.width * WORLD_GRID.height;
  const stats = {
    mean: new Uint16Array(N), min: new Uint16Array(N), max: new Uint16Array(N),
    status: new Uint8Array(N), // 0 PENDING
  };
  const census = {
    total: N, measured: 0, missing: 0, failed: 0, pending: N, ready: false,
    startedAt: null, finishedAt: null, elapsedMs: null,
    globalMin: null, globalMax: null, maxMeanTile: null,
    zeroTiles: 0, nonzeroTiles: 0,
  };

  const state = {
    mount, terrainArchive, names, indexCensus, identity, stats, census,
    tileCache: new TileCache(CONFIG.tileCacheCapacity),
    terrainMount: terrain, vegetationMount: vegetation,
    // ETAP D: the material->texture chain state (bounded + identity-checked)
    textureArchive: null, // LazyTextureArchive — created ONLY after the pin VERIFIES
    textureIndexState: 'PENDING_PIN_VERIFICATION',
    materialsCache: new IdentityCache(
      CONFIG.materialsCacheCapacity, verifyMaterialsCacheIdentity, 'materials',
      (e) => (e.tail?.byteLength ?? 0)),
    textureCache: new IdentityCache(
      CONFIG.textureCacheCapacity, verifyTextureCacheIdentity, 'textures',
      (e) => (e.payload?.byteLength ?? 0)),
    materialResolve: { requests: 0, resolved: 0, unresolved: 0 },
    // ---- ETAP E: the vegetation model chain state (bounded + identity-checked) ----
    modelArchive: null, // LazyModelArchive — created ONLY after the Models.bnt pin VERIFIES
    modelIndexState: 'PENDING_PIN_VERIFICATION',
    modelCache: new IdentityCache(
      CONFIG.modelCacheCapacity, verifyModelCacheIdentity, 'models',
      (e) => (e.payload?.byteLength ?? 0)),
    vegetation: {
      mode: 'RECONSTRUCTION_PREVIEW',
      threeWaySeparation: VEGETATION_THREE_WAY_SEPARATION,
      windowCalibration: LABSEED_WINDOW_CALIBRATION,
      defaultProfile: null,        // the MEASURED default-profile justification (below)
      supportCensusState: 'PENDING',
      supportCensus: null,
      p3: 0,                       // [P-RNG-P3] — shown SEPARATELY (never the LAB_SEED)
      labSeedNote: 'LAB_SEED = the preview seed over the RECONSTRUCTION cell-stream stand-in (the documented PEFoliageLabSeed wrapper); NEVER the unestablished original p3 and NEVER a historical-seed claim',
      visibleInstanceCap: 5000,    // the HARD display limit (contract §6.7)
    },
    containerVerification: {
      terrain: { state: 'VERIFIED', sha256: terrain.actualSha256, path: terrainPath, sizeBytes: null, mounted: true },
      vegetationClimates: { state: 'VERIFIED', sha256: vegetation.actualSha256, path: vclPath, sizeBytes: null, mounted: true },
      models: { state: 'PENDING', sha256: null, path: modelsPath, sizeBytes: null, mounted: false, note: 'ETAP E: stream-hash pin verification, then a LAZY bounded index mount (footer+directory+per-entry reads only; NEVER the whole container, never a whole-container route)' },
      textures: { state: 'PENDING', sha256: null, path: texturesPath, sizeBytes: null, mounted: false, note: 'ETAP D: stream-hash pin verification, then a LAZY bounded index mount (footer+directory+per-entry reads only; NEVER the whole container, never a whole-container route)' },
    },
    climates: { total: 32, profiles: null, decoded: null, unsupported: null },
    stageLog: [],
    startedAt: new Date().toISOString(),
  };
  for (const c of [state.containerVerification.terrain, state.containerVerification.vegetationClimates]) {
    try { c.sizeBytes = fs.statSync(c.path).size; } catch { c.sizeBytes = null; }
  }
  for (const c of [state.containerVerification.models, state.containerVerification.textures]) {
    try { c.sizeBytes = fs.statSync(c.path).size; } catch { c.sizeBytes = null; }
  }

  // ---- census: decode EVERY regular tile from the ORIGINAL bytes ----
  async function runCensus() {
    census.startedAt = new Date().toISOString();
    const t0 = Date.now();
    let gMin = 0xFFFF, gMax = 0, bestMean = -1, bestIdx = -1, zeroTiles = 0, nonzeroTiles = 0;
    const BATCH = 512;
    let sinceYield = 0;
    for (let gy = 0; gy < WORLD_GRID.height; gy++) {
      for (let gx = 0; gx < WORLD_GRID.width; gx++) {
        const idx = gy * WORLD_GRID.width + gx;
        const name = gx.toString(16).padStart(4, '0') + gy.toString(16).padStart(4, '0') + '.tdf';
        try {
          if (!names.has(name)) {
            stats.status[idx] = 2; census.missing++;
          } else {
            const tile = await mount.getTerrainTile({ era: WORLD_ERA, gridX: gx, gridY: gy });
            const h = tile.heights;
            let mn = 0xFFFF, mx = 0, sum = 0;
            for (let i = 0; i < 1024; i++) {
              const v = h[i];
              sum += v;
              if (v < mn) mn = v;
              if (v > mx) mx = v;
            }
            const mean = Math.round(sum / 1024);
            stats.mean[idx] = mean; stats.min[idx] = mn; stats.max[idx] = mx;
            stats.status[idx] = 1; census.measured++;
            if (mn < gMin) gMin = mn;
            if (mx > gMax) gMax = mx;
            if (mean > bestMean) { bestMean = mean; bestIdx = idx; }
            if (mx === 0 && mn === 0) zeroTiles++; else nonzeroTiles++;
          }
        } catch (e) {
          stats.status[idx] = 3; census.failed++;
          state.stageLog.push({ at: new Date().toISOString(), kind: 'CENSUS_TILE_FAILURE', tile: name, error: String(e?.message ?? e) });
        }
        census.pending = census.total - census.measured - census.missing - census.failed;
        if (++sinceYield >= BATCH) {
          sinceYield = 0;
          await new Promise((r) => setImmediate(r)); // keep the server responsive
        }
      }
    }
    census.globalMin = gMin === 0xFFFF && census.measured > 0 ? 0 : gMin;
    census.globalMax = gMax;
    if (bestIdx >= 0) {
      census.maxMeanTile = { gridX: bestIdx % WORLD_GRID.width, gridY: Math.floor(bestIdx / WORLD_GRID.width), mean: bestMean };
    }
    census.zeroTiles = zeroTiles; census.nonzeroTiles = nonzeroTiles;
    census.ready = true;
    census.finishedAt = new Date().toISOString();
    census.elapsedMs = Date.now() - t0;
  }

  // ---- .vcl profile census (32 profiles, honest UNSUPPORTED kept) ----
  // ETAP E: DECODED profiles additionally carry the per-record MODEL SUMMARY
  // (the REAL model ids/scales read from the correctly decoded records —
  // contract §6.1; the .vcl col semantics labels follow the decoder header:
  // col1 density role PLAUSIBLE, cols 6..11 UNVERIFIED).
  async function runClimateCensus() {
    const profiles = [];
    let decoded = 0; const unsupported = [];
    for (let i = 0; i < 32; i++) {
      try {
        const c = await mount.getVegetationClimate({ era: WORLD_ERA, climateIndex: i });
        profiles.push({
          index: i, status: 'DECODED', recordCount: c.recordCount,
          models: c.records.map((r, recIndex) => ({
            recIndex, id: r[0] | 0, density: r[1], scaleMin: r[2], scaleMax: r[3],
            colSemantics: 'col0 model id (GetModel 0x66 id space); col1 density (role PLAUSIBLE, iter032); col2/col3 per-model scale min/max (census-measured); col4/col5 carried raw (UNVERIFIED — no semantics assigned)',
          })),
        });
        decoded++;
      } catch (e) {
        profiles.push({ index: i, status: 'UNSUPPORTED', recordCount: 0, error: String(e?.message ?? e).slice(0, 300) });
        unsupported.push(i);
      }
    }
    state.climates.profiles = profiles;
    state.climates.decoded = decoded;
    state.climates.unsupported = unsupported;
  }

  // ---- Models.bnt / Textures.bnt stream-hash verification (bounded memory) ----
  async function verifyContainer(which, filePath, pin) {
    const rec = state.containerVerification[which];
    try {
      const sha = await streamSha256(filePath);
      rec.sha256 = sha;
      rec.state = sha === pin ? 'VERIFIED' : `FAILED_SHA_MISMATCH (expected ${pin})`;
      if (sha !== pin) {
        state.stageLog.push({ at: new Date().toISOString(), kind: 'CONTAINER_PIN_MISMATCH', container: which, got: sha, expected: pin });
      }
    } catch (e) {
      rec.state = `FAILED_READ (${String(e?.message ?? e).slice(0, 200)})`;
    }
  }

  // ---- ETAP D: the pinned Textures.bnt LAZY bounded index mount ----
  // Runs ONLY after the fail-closed stream-hash pin VERIFIES. The texture
  // endpoints refuse everything until textureIndexState === 'READY' (a
  // FAILED/mismatched container NEVER serves a single texture byte).
  async function initTextureIndex() {
    const rec = state.containerVerification.textures;
    if (rec.state !== 'VERIFIED') {
      state.textureIndexState = `REFUSED_CONTAINER_NOT_VERIFIED (${rec.state})`;
      state.stageLog.push({ at: new Date().toISOString(), kind: 'TEXTURE_INDEX_REFUSED', reason: state.textureIndexState });
      return;
    }
    try {
      const arch = new LazyTextureArchive(texturesPath, { containerSha256: rec.sha256 });
      const footer = await arch.openAndParseIndex();
      state.textureArchive = arch;
      state.textureIndexState = 'READY';
      state.stageLog.push({ at: new Date().toISOString(), kind: 'TEXTURE_INDEX_READY', parsedEntries: footer.parsedEntries, countField: footer.countField, numericIdCount: arch.byId.size });
    } catch (e) {
      state.textureIndexState = `FAILED (${String(e?.message ?? e).slice(0, 300)})`;
      state.stageLog.push({ at: new Date().toISOString(), kind: 'TEXTURE_INDEX_FAILED', error: String(e?.message ?? e) });
    }
  }

  // ---- ETAP E: the pinned Models.bnt LAZY bounded index mount ----
  // Runs ONLY after the fail-closed stream-hash pin VERIFIES. The model
  // endpoint refuses everything until modelIndexState === 'READY'.
  async function initModelIndex() {
    const rec = state.containerVerification.models;
    if (rec.state !== 'VERIFIED') {
      state.modelIndexState = `REFUSED_CONTAINER_NOT_VERIFIED (${rec.state})`;
      state.stageLog.push({ at: new Date().toISOString(), kind: 'MODEL_INDEX_REFUSED', reason: state.modelIndexState });
      return;
    }
    try {
      const arch = new LazyModelArchive(modelsPath, { containerSha256: rec.sha256 });
      const footer = await arch.openAndParseIndex();
      state.modelArchive = arch;
      state.modelIndexState = 'READY';
      state.stageLog.push({ at: new Date().toISOString(), kind: 'MODEL_INDEX_READY', parsedEntries: footer.parsedEntries, countField: footer.countField, numericIdCount: arch.byId.size });
    } catch (e) {
      state.modelIndexState = `FAILED (${String(e?.message ?? e).slice(0, 300)})`;
      state.stageLog.push({ at: new Date().toISOString(), kind: 'MODEL_INDEX_FAILED', error: String(e?.message ?? e) });
    }
  }

  // ---- ETAP E: the MEASURED default-profile support census (contract §6.2) ----
  // The default profile choice is a MEASUREMENT, never a "historical biome"
  // claim: profile 0 (0.vcl) is DECODED with non-empty records AND contains
  // the model whose NIF is the EXISTING qualified importer's cross-validated
  // WITNESS (457485, NifModelReader scope). The census measures the profile's
  // DISTINCT models through the REAL chain (lazy reads + parseWitnessModel +
  // strict texture decode) and records per-model SUPPORTED/UNTEXTURED/
  // UNSUPPORTED counts. Runs once both lazy indexes are READY (bounded:
  // ~10 model reads + ~5 texture reads).
  const VEG_DEFAULT_PROFILE = 0;
  async function runVegetationSupportCensus() {
    const v = state.vegetation;
    try {
      const c = await state.mount.getVegetationClimate({ era: WORLD_ERA, climateIndex: VEG_DEFAULT_PROFILE });
      v.defaultProfile = {
        index: VEG_DEFAULT_PROFILE,
        status: 'DECODED',
        recordCount: c.recordCount,
        recordsNonEmpty: c.recordCount > 0,
        distinctModels: [...new Set(c.records.map((r) => r[0] | 0))].length,
        measuredJustification:
          'MEASURED CHOICE (never "the historical biome of this place"): profile 0 is DECODED by the strict VegetationClimateDecoder with 12 non-empty records, and its model set contains 457485 — the NIF whose parse chain the EXISTING qualified importer (NifModelReader) was cross-validated BIT-EXACTLY against the R61 oracle (iter037) — plus 9 further same-era PCG_9_3_5 Models.bnt models measured below through the same importer without widening any guard',
        climateProvenance: c.provenance,
      };
      if (!state.modelArchive || state.modelIndexState !== 'READY') {
        v.supportCensusState = `WAITING_MODEL_INDEX (${state.modelIndexState})`;
        return;
      }
      if (!state.textureArchive || state.textureIndexState !== 'READY') {
        v.supportCensusState = `WAITING_TEXTURE_INDEX (${state.textureIndexState})`;
        return;
      }
      v.supportCensusState = 'RUNNING';
      v.supportCensus = await buildVegetationSupportCensus({
        modelArchive: state.modelArchive,
        textureArchive: state.textureArchive,
        records: c.records,
      });
      v.supportCensusState = 'READY';
      state.stageLog.push({ at: new Date().toISOString(), kind: 'VEG_SUPPORT_CENSUS_DONE', profile: VEG_DEFAULT_PROFILE, counts: v.supportCensus.counts });
    } catch (e) {
      v.supportCensusState = `FAILED (${String(e?.message ?? e).slice(0, 300)})`;
      state.stageLog.push({ at: new Date().toISOString(), kind: 'VEG_SUPPORT_CENSUS_ERROR', error: String(e?.stack ?? e).slice(0, 500) });
    }
  }

  if (startBackground) {
    // independent bounded background stages; each records its own errors
    void runClimateCensus().then(
      () => state.stageLog.push({ at: new Date().toISOString(), kind: 'CLIMATE_CENSUS_DONE', decoded: state.climates.decoded, unsupported: state.climates.unsupported }),
      (e) => state.stageLog.push({ at: new Date().toISOString(), kind: 'CLIMATE_CENSUS_ERROR', error: String(e?.stack ?? e) }));
    void verifyContainer('models', modelsPath, CONFIG.pins.models).then(
      () => state.stageLog.push({ at: new Date().toISOString(), kind: 'MODELS_VERIFY_DONE', state: state.containerVerification.models.state }),
      (e) => state.stageLog.push({ at: new Date().toISOString(), kind: 'MODELS_VERIFY_ERROR', error: String(e?.stack ?? e) }))
      .then(initModelIndex, initModelIndex); // the model index mounts ONLY on a verified pin (or records the refusal)
    void verifyContainer('textures', texturesPath, CONFIG.pins.textures).then(
      () => state.stageLog.push({ at: new Date().toISOString(), kind: 'TEXTURES_VERIFY_DONE', state: state.containerVerification.textures.state }),
      (e) => state.stageLog.push({ at: new Date().toISOString(), kind: 'TEXTURES_VERIFY_ERROR', error: String(e?.stack ?? e) }))
      .then(initTextureIndex, initTextureIndex) // the index mounts ONLY on a verified pin (or records the refusal)
      // ETAP E: the support census runs once BOTH lazy indexes are READY
      // (bounded; polls the two states — each stage records its own errors)
      .then(async () => {
        const deadline = Date.now() + 120000;
        while (Date.now() < deadline) {
          if (state.modelIndexState === 'READY' && state.textureIndexState === 'READY') break;
          if (!String(state.modelIndexState).startsWith('PENDING') && state.modelIndexState !== 'READY') break; // refused/failed — census will record it
          if (!String(state.textureIndexState).startsWith('PENDING') && state.textureIndexState !== 'READY') break;
          await new Promise((r) => setTimeout(r, 250));
        }
        await runVegetationSupportCensus();
      });
    void runCensus().then(
      () => state.stageLog.push({ at: new Date().toISOString(), kind: 'CENSUS_DONE', measured: census.measured, missing: census.missing, failed: census.failed, elapsedMs: census.elapsedMs }),
      (e) => state.stageLog.push({ at: new Date().toISOString(), kind: 'CENSUS_ERROR', error: String(e?.stack ?? e) }));
  }

  return state;
}

function tileNameFor(gx, gy) {
  return gx.toString(16).padStart(4, '0') + gy.toString(16).padStart(4, '0') + '.tdf';
}

/** Decode one tile THROUGH THE PRODUCTION PATH with the identity-verified
 * cache: a HIT serves the cached canonical tile (identity re-verified over
 * the cached heights bytes — CAM-C3 discipline); a MISS decodes fresh from
 * the ORIGINAL bytes through PESourceMount.getTerrainTile. */
async function decodeTileWithCache(state, gx, gy) {
  const name = tileNameFor(gx, gy);
  const entry = state.tileCache.get(name, state.identity);
  const key = state.tileCache.key(name, state.identity);
  if (entry) {
    return { tile: entry.tile, cache: { state: 'HIT', key } };
  }
  const tile = await state.mount.getTerrainTile({ era: WORLD_ERA, gridX: gx, gridY: gy });
  state.tileCache.set(name, state.identity, tile);
  return { tile, cache: { state: 'MISS', key } };
}

// ---------------------------------------------------------------------------
// API payload builders
// ---------------------------------------------------------------------------
function statusPayload(state, serverInfo) {
  const c = state.census;
  const cv = state.containerVerification;
  return {
    ok: true,
    run: RUN_ID,
    serverVersion: SERVER_VERSION,
    readOnly: true,
    bind: CONFIG.bind,
    port: CONFIG.port,
    pid: process.pid,
    startedAt: state.startedAt,
    era: WORLD_ERA,
    eraNote: 'era świata tego uruchomienia = PCG_9_3_5 (installed client). CD era label in the source layer = CD_JAN_2003 (explicit mapping; never identified with JUL_2003). No cross-era mixing.',
    calibration: WORLD_CALIBRATION,
    grid: { width: WORLD_GRID.width, height: WORLD_GRID.height, samplesPerTile: WORLD_TILE_SAMPLES, meterPerSample: 2, tileMeters: WORLD_TILE_SAMPLES * 2 },
    containers: {
      terrain: { ...cv.terrain, pin: CONFIG.pins.terrain, framing: 'BNT2_TERRAIN' },
      vegetationClimates: { ...cv.vegetationClimates, pin: CONFIG.pins.vegetation, framing: 'BNT2', profiles: state.climates },
      models: { ...cv.models, pin: CONFIG.pins.models, indexState: state.modelIndexState, index: state.modelArchive ? state.modelArchive.stats() : null },
      textures: { ...cv.textures, pin: CONFIG.pins.textures, indexState: state.textureIndexState, index: state.textureArchive ? state.textureArchive.stats() : null },
    },
    vegetation: {
      mode: state.vegetation.mode,
      threeWaySeparation: state.vegetation.threeWaySeparation,
      windowCalibration: state.vegetation.windowCalibration,
      defaultProfile: state.vegetation.defaultProfile,
      supportCensusState: state.vegetation.supportCensusState,
      supportCensus: state.vegetation.supportCensus,
      p3: state.vegetation.p3,
      p3Note: '[P-RNG-P3] the p3 seed input is UNVERIFIED and stays 0 — shown SEPARATELY; it is NEVER the LAB_SEED and never claimed historical',
      labSeedNote: state.vegetation.labSeedNote,
      visibleInstanceCap: state.vegetation.visibleInstanceCap,
      caches: { models: state.modelCache.stats() },
      note: 'ETAP E: the vegetation preview is RECONSTRUCTION_PREVIEW — ORIGINAL_CLIMATE_RECORDS (strict .vcl decode) + RECOVERED_RNG_ARITHMETIC (the untouched byte-locked PEFoliageCore chain) + INSTANCE_DISTRIBUTION (the documented PEFoliageLabSeed wrapper — LAB_SEED-keyed [P-CELLSTREAM] stand-in, reconstruction-only); no historical-seed/count/biome claims anywhere',
    },
    terrainIndex: state.indexCensus,
    terrainMaterials: {
      wireVersion: MATERIALS_WIRE_VERSION,
      maskOffsetRecordRelative: 56,
      maskOffsetNote: 'named material record mask @ record+56 (fields 52..55 = extra4, NOT mask); stride = size+4; RAW or RLE (count,value) with EXACT consumption; INDEPENDENT per-layer weights — layer sums > 255 are ORIGINAL DATA and are never normalized',
      textureChainRelation: TEXTURE_CHAIN_RELATION,
      textureWireVersion: TEXTURE_WIRE_VERSION,
      textureEraGate: `?era= must be ${WORLD_ERA} — every other era label (incl. CD_JAN_2003 / CD_2003) is REFUSED before any data access (CD-era textures NEVER resolve PCG_9_3_5 references)`,
      rendererPreset: 'RENDER_RECONSTRUCTION (client): sequential lerp per layer by RAW mask/255 in record order (era-evidenced blend FORM — the 9.3.5 masks drive the LOD vertex-color bake lerp(vertexColor, materialTexture(u,v), mask/255), iter030; the ALBEDO role, UV repeat and cell sampling of this preview are reconstruction choices, labeled in the world UI)',
      caches: { materials: state.materialsCache.stats(), textures: state.textureCache.stats() },
      resolveCensus: state.materialResolve,
    },
    census: {
      total: c.total, measured: c.measured, missing: c.missing, failed: c.failed,
      pending: c.pending, ready: c.ready, startedAt: c.startedAt, finishedAt: c.finishedAt,
      elapsedMs: c.elapsedMs, globalMin: c.globalMin, globalMax: c.globalMax,
      maxMeanTile: c.maxMeanTile, zeroTiles: c.zeroTiles, nonzeroTiles: c.nonzeroTiles,
      note: 'raw u16 value 0 is DATA (not NODATA); NODATA = missing entry or decode failure',
    },
    tileCache: state.tileCache.stats(),
    overviewLayout: WORLD_OVERVIEW_LAYOUT,
    catalog: { url: CONFIG.catalogUrl, note: 'separate standing catalog server (npm run serve:catalog, port 8161) — this world server never serves /catalog' },
    gapsVersion: 'etap-d',
    three: { version: serverInfo?.threeVersion ?? null, root: CONFIG.threeRoot, pin: CONFIG.threePinnedVersion },
    stageLogTail: state.stageLog.slice(-12),
    note: 'loopback-only; static surface = fixed allowlists + the pinned three package + 4 client world modules; data APIs = index-derived only (tile heights + material tails, per-tile census stats, climate records, bounded single-texture payloads); no arbitrary filesystem path endpoint, no whole-container route BY CONSTRUCTION',
  };
}

function overviewBinary(state) {
  const n = WORLD_GRID.width * WORLD_GRID.height;
  const buf = Buffer.alloc(n * WORLD_OVERVIEW_LAYOUT.bytesPerTile);
  for (let i = 0; i < n; i++) {
    const o = i * 7;
    buf.writeUInt16LE(state.stats.mean[i], o);
    buf.writeUInt16LE(state.stats.min[i], o + 2);
    buf.writeUInt16LE(state.stats.max[i], o + 4);
    buf.writeUInt8(state.stats.status[i], o + 6);
  }
  return buf;
}

function gapsPayload(state) {
  return {
    ok: true,
    run: RUN_ID,
    catalog: { url: CONFIG.catalogUrl, note: 'model catalog viewer (192374, 193207, 193313, 193684, 218757) — separate server' },
    gaps: [
      { id: 'terrain_textures', label: 'Tekstury terenu (oryginalne)', state: 'ETAP_D_DELIVERED (z jawnym zakresem)', detail: 'The material->texture chain is LIVE: TDF named material records (mask@record+56, raw weights) -> id@+16 -> "<id>.dat" in the pinned PCG Textures.bnt -> the strict TGA2 24bpp decoder -> GPU splat in /world (texture toggle live). HONEST SCOPE: (1) the 9.3.5 engine used these masks for the LOD vertex-color tint bake + zone shadow paint (iter030, 838/838 census) — the ground ALBEDO in 9.3.5 was the climate palette pipeline whose per-location inputs (432502 climate grid, 459344 selector grids) are MISSING locally; rendering the material textures as terrain albedo is a labeled RENDER_RECONSTRUCTION preset; (2) the UV repeat of the preview is a reconstruction choice (no PE evidence for the material-texture repeat); (3) an id without a "<id>.dat" entry is an explicit UNRESOLVED binding — skipped with a diagnostic, never a random fallback texture.' },
      { id: 'vegetation', label: 'Roślinność (drzewa)', state: 'ETAP_E_DELIVERED (z jawnym zakresem)', detail: 'The vegetation preview is LIVE in /world (profile picker 0..31 with the REAL model ids/scales; LAB_SEED; preview density; the 5000 visible-instance cap with requested/rendered/limited counts). HONEST SCOPE — the THREE-WAY SEPARATION (contract §6): ORIGINAL_CLIMATE_RECORDS = the strict .vcl decode (25.vcl stays UNSUPPORTED — comma tokens never converted); RECOVERED_RNG_ARITHMETIC = the untouched byte-locked PEFoliageCore chain; INSTANCE_DISTRIBUTION = the documented PEFoliageLabSeed wrapper (LAB_SEED-keyed [P-CELLSTREAM] stand-in) — RECONSTRUCTION-ONLY: the historical cell-stream source, the climate->region mapping and the original p3 remain UNKNOWN; no historical seed/count/biome/placement claims. At least one REAL same-era model renders through the EXISTING qualified importer with its original textures where the binding resolves (unresolved texture chains render honestly untextured — never a stock pine under the same id).' },
      { id: 'water', label: 'System wody (oryginalny)', state: 'NOT_RECOVERED', detail: 'PESourceMount.getWaterResource fails LOUDLY (Gate D pending); no water rendering is claimed. Raw u16 = 0 tiles are DATA (not water claims).' },
      { id: 'special_rows', label: 'Wiersze specjalne terenu (6 530)', state: 'EXCLUDED — UNRESOLVED', detail: 'terrain.bnt index rows with gridY 0xff5a..0xffff (6,530 entries) have UNRESOLVED semantics and are EXCLUDED from regular addressing (loud out-of-range refusals), not silently rendered.' },
      { id: 'sentinel', label: 'Kafel sentinel 7ffe7ffe.tdf', state: 'NOT A REGULAR TILE', detail: 'The sentinel/overview tile is explicitly excluded from the 220x236 regular grid; requesting it through the tile API is refused loudly.' },
      { id: 'models_world_placement', label: 'Historyczne rozmieszczenie budynków', state: 'NOT_ESTABLISHED', detail: 'No building/instance placement data has been recovered in this project; the world shows terrain only. Catalog models are NOT placed into the world. HISTORICAL_BUILDING_PLACEMENT = NOT_ESTABLISHED.' },
      { id: 'historical_axes', label: 'Historyczne osie/jednostki PE', state: 'UNVERIFIED', detail: 'Adapter units (u16/128 meters, 2 units/sample, identity min/max) are CURRENT_RUNTIME_CALIBRATION — a runtime preset with provenance, NOT a proven historical engine fact. Position readouts are labeled adapter units + tile key, never "original XYZ".' },
      { id: 'historical_tree_distribution', label: 'Historyczne rozmieszczenie drzew', state: 'NOT_ESTABLISHED', detail: 'Trees are procedural from climate + terrain; instance distribution is reconstruction-only until the cell stream source is established (Etap E scope).' },
      { id: 'material_texture_atlas_dir', label: 'Textures/Terrain.bnt (12 B)', state: 'NOT A COMPLETE ATLAS — MEASURED', detail: 'The Data\\Textures\\Terrain.bnt file in the PCG install is 12 bytes (8 zero bytes + "BNT2" magic, measured this run) — it is NOT a terrain texture atlas. The REAL texture corpus is Textures.bnt (8,381 entries, pinned SHA 61ACD13B...); the terrain material chain resolves through it.' },
    ],
  };
}

// ---------------------------------------------------------------------------
// request handler (exported for tests)
// ---------------------------------------------------------------------------

/** The per-tile materials JSON served by /api/world/tile/<gx>/<gy>/materials
 * (ETAP D). The masks are the RAW 16x16 weight grids (base64 of the exact
 * decoded bytes — bit-exact, never normalized: layer sums > 255 are ORIGINAL
 * DATA). Per material, the "<id>.dat" texture entry of the pinned Textures.bnt
 * is resolved against the PARSED index — the engine-RE-confirmed id@+16
 * relation, re-measured per request; a missing entry is an explicit UNRESOLVED
 * binding (the client renders an honest diagnostic, never a fallback
 * texture). System records are carried with their UNVERIFIED labels. */
function buildMaterialsServed(state, gx, gy, name, mm) {
  const texArch = state.textureArchive;
  const resolve = state.materialResolve;
  const materials = mm.materials.map((n) => {
    const entryName = `${n.id}.dat`;
    const entry = texArch ? texArch.entryByName(entryName) : null;
    resolve.requests++;
    if (entry) {
      resolve.resolved++;
      return {
        position: n.position, id: n.id, name: n.name, dim: n.dim, bps: n.bps,
        unk: n.unk, res: n.res, size: n.size, recordOffset: n.recordOffset,
        maskEncoding: n.maskEncoding,
        maskBase64: Buffer.from(n.mask.buffer, n.mask.byteOffset, n.mask.byteLength).toString('base64'),
        texture: {
          resolved: true, entryName: entry.name, size: entry.size, offset: entry.offset,
          relation: TEXTURE_CHAIN_RELATION,
          containerSha256: state.containerVerification.textures.sha256,
        },
      };
    }
    resolve.unresolved++;
    return {
      position: n.position, id: n.id, name: n.name, dim: n.dim, bps: n.bps,
      unk: n.unk, res: n.res, size: n.size, recordOffset: n.recordOffset,
      maskEncoding: n.maskEncoding,
      maskBase64: Buffer.from(n.mask.buffer, n.mask.byteOffset, n.mask.byteLength).toString('base64'),
      texture: {
        resolved: false, entryName,
        reason: `NO "${entryName}" entry in the pinned ${WORLD_ERA} Textures.bnt index (parsed: ${texArch ? texArch.stats().parsedEntries : 'n/a'} entries) — UNRESOLVED binding: the layer is SKIPPED with an explicit diagnostic (never a fallback texture, never cross-era substitution)`,
      },
    };
  });
  return {
    ok: true,
    run: RUN_ID,
    gridX: gx, gridY: gy, name,
    wireVersion: MATERIALS_WIRE_VERSION,
    maskLayout: {
      maskOffsetRecordRelative: 56,
      extra4: 'record bytes 52..55 (NOT mask; carried by the decoder as extra4)',
      stride: 'size+4 (the size field counts all bytes after itself)',
      encodings: 'RAW u8[256] when the region length == 256, else RLE (count,value) pairs consuming the region EXACTLY; named records MUST decode (loud failure otherwise)',
      weights: 'INDEPENDENT per-layer raw u8 weights; sums > 255 are ORIGINAL DATA and are NEVER normalized',
      order: 'materials are listed in RECORD ORDER (base first: the position-0 record is the full-coverage base, e.g. Stone04)',
    },
    materials,
    systemRecords: mm.systemRecords,
    sums: mm.sums,
    textureChainRelation: TEXTURE_CHAIN_RELATION,
    rendererPreset: 'RENDER_RECONSTRUCTION (client): sequential lerp per layer by RAW mask/255 in record order — era-evidenced blend FORM (9.3.5 masks drive the LOD vertex-color bake lerp(vertexColor, materialTexture(u,v), mask/255), iter030); the ALBEDO role, the UV repeat and the 16x16 nearest cell sampling of this preview are labeled reconstruction choices (raw weights unchanged)',
    provenance: mm.provenance,
    resolveCensus: { ...resolve },
  };
}

export function createWorldApp(state, serverInfo = {}) {
  return async function handle(req, res) {
    if (CONFIG.logRequests) {
      res.on('finish', () => console.log(`[req] ${req.method} ${req.url} -> ${res.statusCode}`));
    }
    const rawUrl = req.url;
    if (req.method !== 'GET' && req.method !== 'HEAD') {
      deny(res, 405, 'METHOD_NOT_ALLOWED_READ_ONLY', `method ${req.method} refused: the server is a read-only loopback world API`, rawUrl);
      return;
    }
    let urlPath;
    try {
      urlPath = decodeURIComponent(rawUrl.split('?')[0]);
    } catch {
      deny(res, 400, 'MALFORMED_URL', 'percent-decoding failed (malformed URL refused)', rawUrl);
      return;
    }
    if (urlPath.includes('\0')) {
      deny(res, 400, 'NULL_BYTE_IN_URL', 'NUL byte in URL refused', rawUrl);
      return;
    }
    if (urlPath.includes('\\')) {
      deny(res, 400, 'BACKSLASH_IN_URL', 'backslash in URL refused (no Windows path semantics in routes)', rawUrl);
      return;
    }
    if (urlPath.split('/').some((seg) => seg === '..' || seg === '.')) {
      deny(res, 400, 'PATH_TRAVERSAL_BLOCKED', '".."/"." path segment refused (static surface = exact allowlists BY CONSTRUCTION)', rawUrl);
      return;
    }

    // ---- static allowlists (exact map lookups; no fs path from the URL) ----
    if (urlPath === '/') {
      res.writeHead(302, { Location: '/launcher', 'Cache-Control': 'no-store' });
      res.end();
      return;
    }
    if (urlPath === '/launcher' || urlPath === '/launcher/' || urlPath === '/launcher/index.html') {
      const b = await readRepoFile(WORLD_FILES['launcher.html']);
      serveBytes(res, 200, b, 'text/html');
      return;
    }
    if (urlPath === '/world' || urlPath === '/world/' || urlPath === '/world/index.html') {
      const b = await readRepoFile(WORLD_FILES['world.html']);
      serveBytes(res, 200, b, 'text/html');
      return;
    }
    if (urlPath.startsWith('/compat/')) {
      const key = urlPath.slice('/compat/'.length);
      const rel = WORLD_FILES[key];
      if (!rel) {
        deny(res, 404, 'STATIC_FILE_NOT_ALLOWEDLISTED',
          `"${key}" is not in the world app allowlist (fixed file set: ${Object.keys(WORLD_FILES).join(', ')})`, rawUrl);
        return;
      }
      const b = await readRepoFile(rel);
      serveBytes(res, 200, b, MIME[path.extname(rel)] || 'application/octet-stream');
      return;
    }
    for (const mod of CLIENT_MODULES) {
      if (urlPath === `/${mod}`) {
        const b = await readRepoFile(mod);
        serveBytes(res, 200, b, 'text/javascript');
        return;
      }
    }
    if (urlPath.startsWith('/src/peworld/') || urlPath.startsWith('/src/pesource/')) {
      const name = urlPath.split('/').slice(2).join('/');
      deny(res, 404, 'STATIC_FILE_NOT_ALLOWLISTED',
        `"${name}" is not in the client world-module allowlist (${CLIENT_MODULES.join(', ')}); the server-side extraction chain is not publicly routed`, rawUrl);
      return;
    }
    if (urlPath.startsWith('/node_modules/three/')) {
      const sub = urlPath.slice('/node_modules/three/'.length);
      const r = await readThreeSub(sub);
      if (r.bytes) {
        serveBytes(res, 200, r.bytes, MIME[path.extname(sub).toLowerCase()] || 'application/octet-stream');
      } else {
        deny(res, r.denyStatus, r.denyError, r.denyMessage, rawUrl);
      }
      return;
    }

    // ---- bounded world APIs (index-derived ONLY) ----
    // ETAP D era gate (applies to EVERY /api/world/* data route): this world
    // serves PCG_9_3_5 ONLY — the era is part of every container identity
    // and pin. An explicit ?era= label that is not PCG_9_3_5 is REFUSED
    // BEFORE ANY DATA ACCESS (era discipline: a CD-era texture reference
    // NEVER resolves a PCG_9_3_5 binding through this server; the refusal is
    // a CONTROLLED outcome, never silently substituted).
    if (urlPath.startsWith('/api/')) {
      const eraParam = new URLSearchParams(rawUrl.split('?')[1] ?? '').get('era');
      if (eraParam !== null && eraParam !== WORLD_ERA) {
        deny(res, 403, 'ERA_REFUSED_WRONG_ERA',
          `?era=${eraParam} refused: this world serves ${WORLD_ERA} ONLY (era = part of the pinned container identity; CD-era textures NEVER resolve PCG_9_3_5 references and are NEVER substituted); omit the era parameter for the default ${WORLD_ERA} data`, rawUrl);
        return;
      }
    }
    if (urlPath === '/api/world/status') {
      const body = Buffer.from(JSON.stringify(statusPayload(state, serverInfo), null, 1) + '\n');
      serveBytes(res, 200, body, 'application/json');
      return;
    }
    if (urlPath === '/api/world/overview/progress') {
      const c = state.census;
      serveBytes(res, 200, Buffer.from(JSON.stringify({
        ok: true, total: c.total, measured: c.measured, missing: c.missing,
        failed: c.failed, pending: c.pending, ready: c.ready,
        startedAt: c.startedAt, finishedAt: c.finishedAt, elapsedMs: c.elapsedMs,
      }) + '\n'), 'application/json');
      return;
    }
    if (urlPath === '/api/world/overview') {
      const buf = overviewBinary(state);
      const c = state.census;
      serveBytes(res, 200, buf, 'application/octet-stream', {
        'X-PE-Overview-Total': String(c.total),
        'X-PE-Overview-Measured': String(c.measured),
        'X-PE-Overview-Ready': String(c.ready),
        'X-PE-Overview-Layout': 'u16LE mean, u16LE min, u16LE max, u8 status; 7B/tile; row-major gridY*220+gridX',
      });
      return;
    }
    if (urlPath === '/api/world/climates') {
      const cl = state.climates;
      serveBytes(res, 200, Buffer.from(JSON.stringify({
        ok: true, total: cl.total, decoded: cl.decoded ?? null, unsupported: cl.unsupported ?? null,
        profiles: cl.profiles,
        note: 'strict decoder; 25.vcl = UNSUPPORTED (comma tokens) — controlled UNSUPPORTED, never comma-converted',
      }) + '\n'), 'application/json');
      return;
    }
    if (urlPath.startsWith('/api/world/climate/')) {
      const rest = urlPath.slice('/api/world/climate/'.length).replace(/\.json$/, '');
      if (!/^\d+$/.test(rest)) {
        deny(res, 400, 'CLIMATE_INDEX_INVALID', `the climate route serves /api/world/climate/<0..31>; got "${rest}"`, rawUrl);
        return;
      }
      const idx = parseInt(rest, 10);
      if (idx < 0 || idx > 31) {
        deny(res, 400, 'CLIMATE_INDEX_OUT_OF_RANGE', `climateIndex out of range 0..31: ${idx} (.vcl indices are 0..31)`, rawUrl);
        return;
      }
      try {
        const c = await state.mount.getVegetationClimate({ era: WORLD_ERA, climateIndex: idx });
        serveBytes(res, 200, Buffer.from(JSON.stringify({
          ok: true, climateIndex: idx, status: 'DECODED',
          recordCount: c.recordCount, records: c.records, provenance: c.provenance,
          modelSummary: c.records.map((r, recIndex) => ({
            recIndex, id: r[0] | 0, density: r[1], scaleMin: r[2], scaleMax: r[3],
            colSemantics: 'col0 model id; col1 density (role PLAUSIBLE); col2/col3 per-model scale min/max (census-measured); col4/col5 carried raw (UNVERIFIED)',
          })),
          vegetationMode: 'RECONSTRUCTION_PREVIEW (ORIGINAL_CLIMATE_RECORDS + the RECOVERED RNG chain + the LAB_SEED-keyed INSTANCE_DISTRIBUTION wrapper — contract §6)',
        }) + '\n'), 'application/json');
      } catch (e) {
        serveBytes(res, 200, Buffer.from(JSON.stringify({
          ok: false, climateIndex: idx, status: 'UNSUPPORTED',
          recordCount: 0, records: null,
          error: String(e?.message ?? e),
          provenanceNote: 'the strict VegetationClimateDecoder refuses this profile (comma tokens at record 9 col 1); controlled UNSUPPORTED — never comma-converted',
          vegetationMode: 'RECONSTRUCTION_PREVIEW',
        }) + '\n'), 'application/json');
      }
      return;
    }
    if (urlPath === '/api/world/gaps') {
      serveBytes(res, 200, Buffer.from(JSON.stringify(gapsPayload(state), null, 1) + '\n'), 'application/json');
      return;
    }
    if (urlPath.startsWith('/api/world/tile/')) {
      const rest = urlPath.slice('/api/world/tile/'.length).replace(/\.json$/, '');
      const parts = rest.split('/');
      const metaOnly = parts.length === 3 && parts[2] === 'meta';
      const materialsOnly = parts.length === 3 && parts[2] === 'materials';
      const validShape = parts.length === 2 || metaOnly || materialsOnly;
      if (!validShape) {
        deny(res, 404, 'UNKNOWN_TILE_ROUTE',
          `the tile route serves /api/world/tile/<gx>/<gy>, /api/world/tile/<gx>/<gy>/meta and /api/world/tile/<gx>/<gy>/materials only; got "${rest}"`, rawUrl);
        return;
      }
      const gxRaw = parts[0];
      const gyRaw = parts.length === 1 ? null : parts[1];
      if (!/^\d+$/.test(gxRaw) || (gyRaw !== null && !/^\d+$/.test(gyRaw))) {
        deny(res, 400, 'GRID_INVALID', `tile grid coordinates must be non-negative integers 0..219/0..235; got "${rest}"`, rawUrl);
        return;
      }
      const gx = parseInt(gxRaw, 10);
      const gy = parseInt(gyRaw, 10);
      if (gx < 0 || gx >= WORLD_GRID.width || gy < 0 || gy >= WORLD_GRID.height) {
        deny(res, 400, 'GRID_OUT_OF_RANGE',
          `tile grid out of range: gx=${gx} gy=${gy} — the regular grid is 0..${WORLD_GRID.width - 1}/0..${WORLD_GRID.height - 1} (220x236 filename-xy); sentinel 7ffe7ffe.tdf and the 6,530 special rows (gridY 0xff5a..0xffff, MEASURED range) are NOT regular tiles and are NOT addressable`, rawUrl);
        return;
      }
      const name = tileNameFor(gx, gy);
      if (isSentinelName(name)) { // defense in depth (cannot happen for 0..219/0..235)
        deny(res, 400, 'SENTINEL_NOT_A_REGULAR_TILE', 'sentinel tile requested — NOT a regular grid tile', rawUrl);
        return;
      }
      if (!state.names.has(name)) {
        deny(res, 404, 'TILE_NOT_IN_INDEX',
          `tile ${name} is not present in the terrain index (NODATA — missing entry, honestly reported, never height 0)`, rawUrl);
        return;
      }
      // ---- ETAP D: the material tail of ONE tile (contract §5) ----
      // TDF entry+record -> material identifier/name (+mask@record+56 raw
      // weights) -> the id@+16 -> "<id>.dat" texture entry relation (resolved
      // against the parsed pinned-Textures.bnt index) — the per-tile chain
      // provenance. Identity-checked cache (CAM-C3): payload SHA recomputed
      // over the cached TAIL bytes on every HIT; a mismatch = controlled
      // refusal + regeneration from the ORIGINAL bytes.
      if (materialsOnly) {
        if (!state.textureArchive || state.textureIndexState !== 'READY') {
          deny(res, 503, 'TEXTURE_CONTAINER_NOT_READY',
            `the pinned Textures.bnt index is not READY yet (state: ${state.textureIndexState}) — the materials route refuses until the fail-closed pin verification + index parse complete; retry (the client polls /api/world/status)`, rawUrl);
          return;
        }
        let served, cacheInfo;
        const hit = state.materialsCache.get(name, state.identity);
        if (hit && !hit.refused) {
          served = hit.served;
          cacheInfo = { state: 'HIT', key: state.materialsCache.key(name, state.identity) };
        } else {
          let mm;
          try {
            mm = await state.mount.getTerrainMaterials({ era: WORLD_ERA, gridX: gx, gridY: gy });
          } catch (e) {
            deny(res, 500, 'MATERIAL_TAIL_DECODE_FAILED',
              `tile ${name}: the production material-tail decode failed LOUDLY — ${String(e?.message ?? e)} (no fallback, no partial masks)`, rawUrl);
            return;
          }
          const tail = mm.tile.tail;
          const payloadSha256 = createHash('sha256')
            .update(Buffer.from(tail.buffer, tail.byteOffset, tail.byteLength)).digest('hex');
          served = buildMaterialsServed(state, gx, gy, name, mm);
          state.materialsCache.set(name, state.identity, {
            served,
            tail,
            identity: {
              era: state.identity.era, container: state.identity.container,
              containerSha256: state.identity.containerSha256,
              wireVersion: MATERIALS_WIRE_VERSION, payloadSha256,
            },
          });
          cacheInfo = hit?.refused
            ? { state: 'REFUSED_REGENERATED', reasons: hit.reasons, key: state.materialsCache.key(name, state.identity) }
            : { state: 'MISS', key: state.materialsCache.key(name, state.identity) };
        }
        serveBytes(res, 200, Buffer.from(JSON.stringify(served, null, 1) + '\n'), 'application/json', {
          'X-PE-Era': WORLD_ERA,
          'X-PE-Container': WORLD_TERRAIN_CONTAINER,
          'X-PE-Entry': name,
          'X-PE-Container-Sha256': String(state.identity.containerSha256 ?? ''),
          'X-PE-Materials-Wire-Version': MATERIALS_WIRE_VERSION,
          'X-PE-Mask-Offset-Record-Relative': '56 (fields 52..55 = extra4, NOT mask)',
          'X-PE-Texture-Chain-Relation': TEXTURE_CHAIN_RELATION_HEADER,
          'X-PE-Cache-Key': cacheInfo.key,
          'X-PE-Cache-State': cacheInfo.state,
        });
        return;
      }
      let tile, cacheInfo;
      try {
        ({ tile, cache: cacheInfo } = await decodeTileWithCache(state, gx, gy));
      } catch (e) {
        deny(res, 500, 'TILE_DECODE_FAILED',
          `tile ${name}: production decode failed loudly — ${String(e?.message ?? e)} (NODATA: decode failure is NEVER masked as height 0)`, rawUrl);
        return;
      }
      const prov = tile.provenance;
      const headers = {
        'X-PE-Era': prov.era,
        'X-PE-Container': prov.container,
        'X-PE-Entry': prov.entry,
        'X-PE-Container-Sha256': String(state.identity.containerSha256 ?? ''),
        'X-PE-Offset': String(prov.offset ?? ''),
        'X-PE-Decoder-Version': prov.decoderVersion ?? '',
        'X-PE-Evidence-Status': prov.evidenceStatus ?? '',
        'X-PE-Height-Data-Offset': '64..2111 (payload-relative; bytes 52..63 are a separate sub-header, NOT heights)',
        'X-PE-Cache-Key': state.tileCache.key(name, state.identity),
        'X-PE-Cache-State': cacheInfo.state,
      };
      if (metaOnly) {
        const h = tile.heights;
        let mn = 0xFFFF, mx = 0, sum = 0, zeros = 0;
        for (let i = 0; i < 1024; i++) {
          const v = h[i]; sum += v;
          if (v < mn) mn = v; if (v > mx) mx = v; if (v === 0) zeros++;
        }
        serveBytes(res, 200, Buffer.from(JSON.stringify({
          ok: true, gridX: gx, gridY: gy, name,
          sampleCount: h.length,
          stats: { min: mn, max: mx, mean: Math.round(sum / 1024), zeroSamples: zeros, note: 'raw uint16 values — raw 0 is DATA, not NODATA' },
          provenance: prov,
          cache: { state: cacheInfo.state, key: state.tileCache.key(name, state.identity), ...state.tileCache.stats() },
          calibration: WORLD_CALIBRATION,
        }, null, 1) + '\n'), 'application/json', headers);
        return;
      }
      // raw heights: 2048 B uint16 LE — EXPLICIT LE writes (no platform assumption)
      const buf = Buffer.alloc(WORLD_HEIGHTS_BYTES);
      for (let i = 0; i < 1024; i++) buf.writeUInt16LE(tile.heights[i], i * 2);
      serveBytes(res, 200, buf, 'application/octet-stream', headers);
      return;
    }

    // ---- ETAP D: ONE bounded texture payload (contract §5 chain step 3) ----
    // '<id>.dat' from the PINNED PCG Textures.bnt through the LAZY bounded
    // reader (single-entry reads; NEVER the whole container). The era gate
    // (?era=) has ALREADY refused wrong-era labels before this point. A
    // missing id is the explicit UNRESOLVED-binding case (404, loud). The
    // identity-checked cache (CAM-C3) recomputes the payload SHA over the
    // cached bytes on every HIT — a mismatch is a controlled refusal +
    // regeneration from the ORIGINAL file bytes.
    if (urlPath.startsWith('/api/world/texture/')) {
      const rest = urlPath.slice('/api/world/texture/'.length).replace(/\.json$/, '');
      if (!/^\d+$/.test(rest)) {
        deny(res, 400, 'TEXTURE_ID_INVALID', `the texture route serves /api/world/texture/<numeric id> (the "<id>.dat" entry space of the pinned Textures.bnt); got "${rest}"`, rawUrl);
        return;
      }
      const id = parseInt(rest, 10);
      if (id > 0xFFFFFFFF) {
        deny(res, 400, 'TEXTURE_ID_OUT_OF_RANGE', `texture id ${id} outside the u32 entry-id space of the pinned container`, rawUrl);
        return;
      }
      if (!state.textureArchive || state.textureIndexState !== 'READY') {
        deny(res, 503, 'TEXTURE_CONTAINER_NOT_READY',
          `the pinned Textures.bnt is not READY yet (pin/index state: ${state.textureIndexState}) — NO texture byte is served before the fail-closed pin verification completes; retry`, rawUrl);
        return;
      }
      const entry = state.textureArchive.entryById(id);
      const entryName = `${id}.dat`;
      if (!entry) {
        deny(res, 404, 'TEXTURE_ENTRY_NOT_FOUND',
          `texture id ${id}: NO "${entryName}" entry in the pinned ${WORLD_ERA} Textures.bnt index (parsed ${state.textureArchive.stats().parsedEntries} entries) — UNRESOLVED binding: loud NOT_FOUND, never a fallback texture, never cross-era substitution (CD-era containers are NEVER consulted)`, rawUrl);
        return;
      }
      const textureIdentity = {
        era: WORLD_ERA,
        container: 'Textures.bnt',
        containerSha256: state.containerVerification.textures.sha256,
      };
      let payload, cacheState = 'MISS', refusalReasons = [];
      const hit = state.textureCache.get(entryName, textureIdentity);
      if (hit && !hit.refused) {
        payload = hit.payload;
        cacheState = 'HIT';
      } else {
        try {
          payload = (await state.textureArchive.readEntry(entry)).payload;
        } catch (e) {
          deny(res, 500, 'TEXTURE_READ_FAILED', `texture ${entryName}: bounded read failed — ${String(e?.message ?? e)} (no fallback)`, rawUrl);
          return;
        }
        const payloadSha256 = createHash('sha256')
          .update(Buffer.from(payload.buffer, payload.byteOffset, payload.byteLength)).digest('hex');
        state.textureCache.set(entryName, textureIdentity, {
          payload,
          identity: {
            era: textureIdentity.era, container: textureIdentity.container,
            containerSha256: textureIdentity.containerSha256,
            wireVersion: TEXTURE_WIRE_VERSION, payloadSha256,
          },
        });
        if (hit?.refused) { cacheState = 'REFUSED_REGENERATED'; refusalReasons = hit.reasons; }
      }
      const actualPayloadSha = createHash('sha256')
        .update(Buffer.from(payload.buffer, payload.byteOffset, payload.byteLength)).digest('hex');
      serveBytes(res, 200, Buffer.from(payload.buffer, payload.byteOffset, payload.byteLength), 'application/octet-stream', {
        'X-PE-Era': WORLD_ERA,
        'X-PE-Container': 'Textures.bnt',
        'X-PE-Container-Sha256': String(textureIdentity.containerSha256 ?? ''),
        'X-PE-Entry': entryName,
        'X-PE-Offset': String(entry.offset),
        'X-PE-Entry-Size': String(entry.size),
        'X-PE-Payload-Sha256': actualPayloadSha,
        'X-PE-Wire-Version': TEXTURE_WIRE_VERSION,
        'X-PE-Texture-Chain-Relation': TEXTURE_CHAIN_RELATION_HEADER,
        'X-PE-Texture-Decode-Scope': 'client decodes with the PRODUCTION decodeTga2 (TGA 2.0, 24bpp, uncompressed, TRUEVISION-XFILE footer; the iter011-confirmed terrain-texture subset); a payload outside that subset fails LOUDLY in the browser (diagnostic, no fallback)',
        'X-PE-Cache-Key': state.textureCache.key(entryName, textureIdentity),
        'X-PE-Cache-State': cacheState,
      });
      return;
    }

    // ---- ETAP E: ONE bounded MODEL NIF payload (contract §6.5) ----
    // '<modelId>.nif' from the PINNED PCG Models.bnt through the LAZY bounded
    // reader (single-entry RAW reads; NEVER the whole 395 MB container; no
    // whole-container route BY CONSTRUCTION). The era gate (?era=) has ALREADY
    // refused wrong-era labels before this point. A missing id is the explicit
    // UNSUPPORTED case (404, loud — an honest UNSUPPORTED count, never a
    // substitute model). The identity-checked cache (CAM-C3) recomputes the
    // payload SHA over the cached NIF bytes on every HIT — a mismatch is a
    // controlled refusal + regeneration from the ORIGINAL file bytes.
    if (urlPath.startsWith('/api/world/model/')) {
      const rest = urlPath.slice('/api/world/model/'.length).replace(/\.json$/, '');
      if (!/^\d+$/.test(rest)) {
        deny(res, 400, 'MODEL_ID_INVALID', `the model route serves /api/world/model/<numeric id> (the "<id>.nif" entry space of the pinned Models.bnt); got "${rest}"`, rawUrl);
        return;
      }
      const id = parseInt(rest, 10);
      if (id > 0xFFFFFFFF) {
        deny(res, 400, 'MODEL_ID_OUT_OF_RANGE', `model id ${id} outside the u32 entry-id space of the pinned container`, rawUrl);
        return;
      }
      if (!state.modelArchive || state.modelIndexState !== 'READY') {
        deny(res, 503, 'MODEL_CONTAINER_NOT_READY',
          `the pinned Models.bnt index is not READY yet (pin/index state: ${state.modelIndexState}) — NO model byte is served before the fail-closed pin verification completes; retry`, rawUrl);
        return;
      }
      const entry = state.modelArchive.entryById(id);
      const entryName = `${id}.nif`;
      if (!entry) {
        deny(res, 404, 'MODEL_ENTRY_NOT_FOUND',
          `model id ${id}: NO "${entryName}" entry in the pinned ${WORLD_ERA} Models.bnt index (parsed ${state.modelArchive.stats().parsedEntries} entries) — UNSUPPORTED model id: loud NOT_FOUND (an honest UNSUPPORTED count; NEVER a substitute/stock model under the same id, never cross-era substitution)`, rawUrl);
        return;
      }
      const modelIdentity = {
        era: WORLD_ERA,
        container: 'Models.bnt',
        containerSha256: state.containerVerification.models.sha256,
      };
      let payload, cacheState = 'MISS', refusalReasons = [];
      const hit = state.modelCache.get(entryName, modelIdentity);
      if (hit && !hit.refused) {
        payload = hit.payload;
        cacheState = 'HIT';
      } else {
        try {
          payload = (await state.modelArchive.readEntry(entry)).payload;
        } catch (e) {
          deny(res, 500, 'MODEL_READ_FAILED', `model ${entryName}: bounded read failed — ${String(e?.message ?? e)} (no fallback)`, rawUrl);
          return;
        }
        const payloadSha256 = createHash('sha256')
          .update(Buffer.from(payload.buffer, payload.byteOffset, payload.byteLength)).digest('hex');
        state.modelCache.set(entryName, modelIdentity, {
          payload,
          identity: {
            era: modelIdentity.era, container: modelIdentity.container,
            containerSha256: modelIdentity.containerSha256,
            wireVersion: MODEL_WIRE_VERSION, payloadSha256,
          },
        });
        if (hit?.refused) { cacheState = 'REFUSED_REGENERATED'; refusalReasons = hit.reasons; }
      }
      const actualPayloadSha = createHash('sha256')
        .update(Buffer.from(payload.buffer, payload.byteOffset, payload.byteLength)).digest('hex');
      serveBytes(res, 200, Buffer.from(payload.buffer, payload.byteOffset, payload.byteLength), 'application/octet-stream', {
        'X-PE-Era': WORLD_ERA,
        'X-PE-Container': 'Models.bnt',
        'X-PE-Container-Sha256': String(modelIdentity.containerSha256 ?? ''),
        'X-PE-Entry': entryName,
        'X-PE-Offset': String(entry.offset),
        'X-PE-Entry-Size': String(entry.size),
        'X-PE-Payload-Sha256': actualPayloadSha,
        'X-PE-Wire-Version': MODEL_WIRE_VERSION,
        'X-PE-Model-Decode-Scope': 'the client parses with the PRODUCTION NifModelReader (single-witness qualified importer, v10.1.0.0 + KNOWN_V10_TYPES, loud failures); a payload outside that scope fails LOUDLY (honest UNSUPPORTED, never a guard removal)',
        'X-PE-Cache-Key': state.modelCache.key(entryName, modelIdentity),
        'X-PE-Cache-State': cacheState,
        ...(refusalReasons.length ? { 'X-PE-Cache-Refusal-Reasons': refusalReasons.join(',') } : {}),
      });
      return;
    }

    deny(res, 404, 'ROUTE_NOT_FOUND',
      'no route matches; this server exposes ONLY the launcher/world app allowlist, the client world modules, the pinned three package subtree, and the bounded /api/world/* index-derived APIs (status, overview, overview/progress, tile/<gx>/<gy>[+/meta+/materials], texture/<id>, model/<id>, climates, climate/<0..31>, gaps) — arbitrary filesystem paths and the original containers are not servable BY CONSTRUCTION (no whole-container route exists)', rawUrl);
  };
}

// ---------------------------------------------------------------------------
// startup (main guard — importing this module has no side effects)
// ---------------------------------------------------------------------------
async function verifyThreePin() {
  const pkgRaw = await fsp.readFile(path.join(CONFIG.threeRoot, 'package.json'), 'utf8');
  const pkg = JSON.parse(pkgRaw);
  if (pkg.version !== CONFIG.threePinnedVersion) {
    throw new Error(`three version ${pkg.version} != pinned ${CONFIG.threePinnedVersion} at ${CONFIG.threeRoot} -- REFUSING (retention pin)`);
  }
  return pkg.version;
}

function checkPortFree(port, host) {
  return new Promise((resolve, reject) => {
    const probe = net.createServer();
    probe.once('error', (err) => reject(err));
    probe.listen(port, host, () => probe.close(() => resolve(true)));
  });
}

async function main() {
  const t0 = Date.now();
  if (FOREIGN_STANDING_PORTS.includes(CONFIG.port)) {
    console.error(`[server-world] PORT ${CONFIG.port} REFUSED — that port belongs to a foreign standing server (8140 sceneir / 8161 catalog; never touched, never replaced). Set PEWORLD_PORT=<other>.`);
    process.exit(1);
  }
  const threeVersion = await verifyThreePin().catch((e) => {
    console.error(`[server-world] THREE PIN FAILURE: ${e.message} -- LOUD FAIL (refusing to start)`);
    process.exit(1);
  });

  // fail-closed mount of the pinned PCG containers (KNOWN_HASHES pins)
  let state;
  try {
    state = await buildWorldRuntime({});
  } catch (e) {
    console.error(`[server-world] WORLD RUNTIME MOUNT FAILED_FAIL_CLOSED: ${e.message}`);
    console.error('[server-world] NOTHING IS SERVED. A pinned container identity did not verify.');
    process.exit(1);
  }
  const ic = state.indexCensus;
  console.log(`[server-world] era ${WORLD_ERA} — terrain index: ${ic.totalEntries} entries = ${ic.regular} regular (220x236) + ${ic.specialRows} special rows (gridY 0x${(ic.specialRowYValues[0] ?? 0).toString(16)}..0x${(ic.specialRowYValues[ic.specialRowYValues.length - 1] ?? 0).toString(16)}) + ${ic.sentinel} sentinel + ${ic.other} other`);
  console.log(`[server-world] container pins verified (fail-closed): terrain.bnt + VegetationClimates.bnt MOUNTED; Models.bnt + Textures.bnt stream-hash verification running in background`);

  // verified-free-port binding (never replaces another process)
  try {
    await checkPortFree(CONFIG.port, CONFIG.bind);
  } catch (e) {
    console.error(`[server-world] PORT ${CONFIG.port} ON ${CONFIG.bind} IS BUSY (${e.code}) -- LOUD FAIL (this server never replaces a running process; set PEWORLD_PORT=<other free port>)`);
    process.exit(1);
  }

  const serverInfo = { threeVersion };
  const server = http.createServer(createWorldApp(state, serverInfo));
  server.on('error', (e) => {
    console.error(`[server-world] BIND ERROR on ${CONFIG.bind}:${CONFIG.port}: ${e.message} -- LOUD FAIL`);
    process.exit(1);
  });
  server.listen(CONFIG.port, CONFIG.bind, () => {
    console.log(`world server http://127.0.0.1:${CONFIG.port}/ pid=${process.pid} READY`);
    console.log(`[server-world] ready in ${Date.now() - t0} ms — routes: /launcher /world /api/world/* (bounded; ETAP E: tile/<g>/<g>/materials + texture/<id> + model/<id> + climates with per-profile model summaries); / redirects to /launcher; census of ${state.census.total} regular tiles running in background (progress on /api/world/overview/progress)`);
    console.log(`[server-world] STOP = terminate pid ${process.pid} (only this process; standing servers 8140/8161 are never touched)`);
  });
  const shutdown = () => {
    server.close(() => process.exit(0));
    setTimeout(() => process.exit(0), 3000).unref();
  };
  process.on('SIGINT', shutdown);
  process.on('SIGTERM', shutdown);
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  main().catch((e) => {
    console.error(`[server-world] UNEXPECTED STARTUP FAILURE: ${e?.stack ?? e}`);
    process.exit(1);
  });
}
