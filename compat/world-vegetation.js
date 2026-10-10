// world-vegetation.js — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010 (contract §3.1 + §6)
// THE /world vegetation subsystem: deterministic RECONSTRUCTION_PREVIEW
// instances standing on the terrain, rendered from ORIGINAL same-era model
// NIF payloads + their original textures where the binding resolves.
//
// THE THREE-WAY SEPARATION (contract §6, BINDING — unchanged from R1):
//   ORIGINAL_CLIMATE_RECORDS = the .vcl records served by /api/world/climate
//       (strict decode; 25.vcl stays UNSUPPORTED — comma tokens are never
//       converted; nothing renders for an UNSUPPORTED profile, honestly).
//   RECOVERED_RNG_ARITHMETIC = src/peworld/PEFoliageCore.js — imported
//       UNTOUCHED (byte-locked seed/RNG/float chain; verified byte-identical
//       by the WORLD_VEG_CORE_UNTOUCHED gate every run).
//   INSTANCE_DISTRIBUTION = src/peworld/PEFoliageLabSeed.js — the DOCUMENTED
//       LAB_SEED wrapper (v2: recIndex identity + fractional density).
//
// THE R2 CHANGES in this module (all labeled; the census carries versions):
//   WL-1 FIX (contract §3.1): rebuild is LATEST-REQUEST-WINS — a busy rebuild
//     stores the newest pending request and re-runs it when the current one
//     completes; a request that was superseded mid-flight ABORTS before
//     applying anything (no stale census/mesh replaces the newer request).
//   WL-2 FIX (contract §3.2): instances stand on the SHARED height query
//     (PEHeightField.triangleHeightAtWorld — the EXACT rendered-triangle
//     planes, with the halo of REAL neighboring samples); NO y=0 fallback —
//     a position without real surface data gets the explicit status
//     DEFERRED_NO_SURFACE and is NOT rendered (counted honestly).
//   WL-5 FIX (contract §6.2): the visible cap is a SPATIALLY FAIR per-tile
//     quota (largest-remainder over the candidate tiles with a ≥1 guarantee
//     for every non-empty tile) — a pure function of the per-tile candidate
//     counts, never of the fetch/generation order; at 6144→5000 NO non-empty
//     candidate tile becomes empty. Per-tile + per-model cap counters, and
//     geometry vs markers counted SEPARATELY.
//   STATUS VOCABULARY (contract §3.2): every generated candidate instance
//     ends PLACED_ON_AVAILABLE_SURFACE / DEFERRED_NO_SURFACE /
//     UNSUPPORTED_MODEL / LOD_LIMITED (the census counts each).
//   REGIONAL PREVIEW (contract §6.4): profileMode 'regional' maps tiles to
//     DECODED profiles through OUR documented reconstruction region map —
//     the map and seed are EXPLICITLY ours (ORIGINAL_REGION_TO_CLIMATE_JOIN
//     = NOT_ESTABLISHED; never a historical biome claim).
'use strict';

import * as THREE from 'three';
import { parseWitnessModel } from '../src/pesource/NifModelReader.js';
import { decodeTga2, decodeTga2A32Image } from '../src/pesource/TgaDecoder.js';
import { decodeDds, DDS_DECODER_VERSION } from '../src/pesource/DdsDecoder.js';
import {
  generateTileInstances, VEGETATION_THREE_WAY_SEPARATION, LABSEED_WINDOW_CALIBRATION,
  LABSEED_WRAPPER_VERSION, LAB_DENSITY_POLICY,
} from '../src/peworld/PEFoliageLabSeed.js';
import { NODE_SCALE_MUL } from '../src/peworld/PEFoliageCore.js';
import { SURFACE_STATUS } from '../src/peworld/PEHeightQuery.js';

export const VEGETATION_SCHEMA_VERSION = 'world-vegetation-r2';
export const MAX_VISIBLE_INSTANCES = 5000;   // the HARD display cap (contract §6.7)
export const MODEL_CACHE_MAX = 16;           // bounded per-model cache
export const NODE_SCALE_RENDER_BRIDGE = 2.0 / NODE_SCALE_MUL; // [P-SCALE] (the deployed-page ratio; lerpValue x 2.0)
export const UNIT_BRIDGE_CM_TO_M = 0.01;     // [P-UNITS] applied EXACTLY ONCE (in the per-shape geometry)
export const VEGETATION_MODE_LABEL = 'VEGETATION_MODE = RECONSTRUCTION_PREVIEW';

/** The REGIONAL PREVIEW region map (contract §6.4) — OUR reconstruction
 * policy, deterministic, versioned. REGION_TILES = 32 tiles (2048 adapter m)
 * per region cell; the profile of a region cell = REGION_PROFILES[(x*31 + y*17)
 * % REGION_PROFILES.length] — a fixed, documented choice of DECODED profiles
 * (0/2/7/19: all actually handled this run; their UNSUPPORTED models render
 * honest markers, never substitutes). The historical region→climate join is
 * NOT_ESTABLISHED — this map is NEVER a historical biome. */
export const REGIONAL_PREVIEW = Object.freeze({
  version: 'regional-preview-v1',
  regionTiles: 32,
  profiles: [0, 2, 7, 19],
  mapRule: 'profile = REGION_PROFILES[(regionX*31 + regionY*17) % 4]; region = tile >> 5',
  note: 'RECONSTRUCTION_PREVIEW only — the map, region size and choice of profiles are OURS; ORIGINAL_REGION_TO_CLIMATE_JOIN = NOT_ESTABLISHED; not a historical biome',
});
export function regionalProfileFor(gx, gy) {
  const rx = Math.floor(gx / REGIONAL_PREVIEW.regionTiles), ry = Math.floor(gy / REGIONAL_PREVIEW.regionTiles);
  const p = REGIONAL_PREVIEW.profiles[(rx * 31 + ry * 17) % REGIONAL_PREVIEW.profiles.length];
  return p;
}

/** The spatially-fair cap allocation (contract §6.2 — WL-5 FIX): largest
 *  remainder over the candidate tiles, with a ≥1 guarantee for every
 *  non-empty tile (when cap >= the number of non-empty tiles). PURE + tested:
 *  the quota is a pure function of the per-tile counts (fetch-order
 *  independent by construction). Returns { quotaByTile, perTileQuota } . */
export function fairCapQuota(perTileCounts, cap) {
  const entries = Object.entries(perTileCounts).filter(([, n]) => n > 0);
  const nonEmpty = entries.length;
  const total = entries.reduce((a, [, n]) => a + n, 0);
  const quota = {};
  if (total <= cap) {
    for (const [k, n] of entries) quota[k] = n;
    return { quotaByTile: quota, perTileQuota: quota, capped: false, nonEmpty, total };
  }
  // (a) the >=1 guarantee: every non-empty tile keeps at least one instance
  for (const [k] of entries) quota[k] = nonEmpty <= cap ? 1 : 0;
  // (b) proportional largest-remainder distribution of the rest
  const rest = cap - Object.values(quota).reduce((a, b) => a + b, 0);
  const scaled = entries.map(([k, n]) => ({ k, q: (n / total) * rest, r: ((n / total) * rest) % 1 }));
  scaled.sort((a, b) => b.r - a.r || (a.k < b.k ? -1 : a.k > b.k ? 1 : 0)); // deterministic tie-break by tile key
  for (let i = 0; i < scaled.length && rest > 0; i++) {
    if (quota[scaled[i].k] === undefined) continue;
    quota[scaled[i].k] += Math.floor(scaled[i].q);
  }
  // (c) the fractional leftovers (largest remainder), never exceeding the cap
  let assigned = Object.values(quota).reduce((a, b) => a + b, 0);
  for (let i = 0; i < scaled.length && assigned < cap; i++) {
    quota[scaled[i].k] += 1; assigned += 1;
  }
  return { quotaByTile: quota, perTileQuota: quota, capped: true, nonEmpty, total };
}

/** The strict texture decode dispatch (server-parity; R2 adds the QUALIFIED
 *  DDS DXT1/DXT5 subset — the two real same-era formats measured on the
 *  inputs of this run; anything else fails LOUDLY → honest untextured,
 *  never a fallback). */
export function decodeModelTextureStrict(payload) {
  if (!(payload instanceof Uint8Array) || payload.length < 4) {
    throw new Error('[world-vegetation] payload too small for a texture header');
  }
  if (payload[0] === 0x44 && payload[1] === 0x44 && payload[2] === 0x53 && payload[3] === 0x20) {
    const d = decodeDds(payload);
    return { bpp: d.fourcc, width: d.width, height: d.height, rgba: d.rgba, decoder: `decodeDds (${DDS_DECODER_VERSION}; ${d.fourcc}; TOP-LEVEL mip only — the mip chain stays unread, documented)` };
  }
  if (payload.length < 18) throw new Error('[world-vegetation] payload too small for a TGA header');
  const bpp = payload[16];
  if (bpp === 32) {
    const d = decodeTga2A32Image(payload);
    return { bpp, width: d.width, height: d.height, rgba: d.rgba, decoder: 'decodeTga2A32Image (TGA2 A32 IMAGE order — row 0 = visual TOP)' };
  }
  if (bpp === 24) {
    const d = decodeTga2(payload);
    return { bpp, width: d.width, height: d.height, rgba: d.rgba, decoder: 'decodeTga2 (TGA2 24bpp terrain-texture subset)' };
  }
  throw new Error(`[world-vegetation] bpp ${bpp} outside the strict model-texture subset {24, 32, DDS-DXT1, DDS-DXT5} — the payload fails LOUDLY (honest untextured; never a fallback texture)`);
}

/** Per-shape renderables from the extraction (the reader file stays
 * untouched; every rule below is the reader's own canon). R2: a texprop with
 * MULTIPLE Ark texture entries tries them IN ENTRY ORDER and uses the FIRST
 * entry whose payload strict-decodes (the era slot order is the evidence —
 * BASE first; a skipped slot is carried as an explicit per-slot diagnostic,
 * never a fabricated material: RENDER_RECONSTRUCTION slot choice, labeled).
 * EXPORTED for the Asset Lab (contract §7: the witness chain is REUSED — no
 * second importer). */
export function buildShapeRenderables(extraction, modelId) {
  const blocks = extraction.blocks;
  const bitsToF32 = (hex) => {
    const u = new Uint32Array(1);
    const b = new Uint8Array(u.buffer);
    for (let i = 0; i < 4; i++) b[i] = parseInt(hex.substr(i * 2, 2), 16);
    return new Float32Array(u.buffer)[0];
  };
  const arkBlocks = blocks.filter((b) => b.type === 'NiArkTextureExtraData');
  const renderables = [];
  const nonVisual = [];
  const slotDiagnostics = [];
  for (const s of blocks.filter((b) => b.type === 'NiTriShape')) {
    const dataBlk = blocks[s.fields.dataRef];
    if (!dataBlk || dataBlk.type !== 'NiTriShapeData') {
      nonVisual.push({ shapeIndex: s.index, shapeName: s.fields.name, reason: 'NO_DATA_BLOCK' });
      continue;
    }
    const texprop = (s.fields.properties ?? [])
      .map((i) => blocks[i]).find((b) => b?.type === 'NiTexturingProperty');
    if (!texprop) {
      nonVisual.push({ shapeIndex: s.index, shapeName: s.fields.name, reason: 'NON_VISUAL_NO_TEXPROP_ARK_CHAIN (untextured Bip01/Box candidate — collision/bounds role UNVERIFIED; carried + counted, NOT rendered)' });
      continue;
    }
    // ALL Ark entries referencing THIS texprop, in ENTRY ORDER
    const entriesForTexprop = arkBlocks
      .flatMap((ab) => ab.fields.entries.map((e) => ({ ...e, texprop: e.ref })))
      .filter((e) => e.texprop === texprop.index);
    if (entriesForTexprop.length === 0) {
      nonVisual.push({ shapeIndex: s.index, shapeName: s.fields.name, reason: 'NON_VISUAL_NO_TEXPROP_ARK_CHAIN (no Ark entry references the texprop)' });
      continue;
    }
    const alphaBlk = (s.fields.properties ?? [])
      .map((i) => blocks[i]).find((b) => b?.type === 'NiAlphaProperty')
      ?? blocks.find((b) => b.type === 'NiAlphaProperty'); // the buildRenderModel fallback rule
    const d = dataBlk.fields;
    const n = d.numVertices;
    const st = s.fields;
    const T = st.translation.map(bitsToF32);
    const R = st.rotation.map((r) => r.map(bitsToF32));
    const S = bitsToF32(st.scale);
    const positions = new Float32Array(n * 3);
    for (let i = 0; i < n; i++) {
      let x = bitsToF32(d.verticesBits[i * 3]);
      let y = bitsToF32(d.verticesBits[i * 3 + 1]);
      let z = bitsToF32(d.verticesBits[i * 3 + 2]);
      let tx = (R[0][0] * x + R[0][1] * y + R[0][2] * z) * S + T[0];
      let ty = (R[1][0] * x + R[1][1] * y + R[1][2] * z) * S + T[1];
      let tz = (R[2][0] * x + R[2][1] * y + R[2][2] * z) * S + T[2];
      // NIF Z-up -> Three Y-up: (x, z, -y); cm -> m x0.01 (applied ONCE)
      positions[i * 3] = tx * UNIT_BRIDGE_CM_TO_M;
      positions[i * 3 + 1] = tz * UNIT_BRIDGE_CM_TO_M;
      positions[i * 3 + 2] = -ty * UNIT_BRIDGE_CM_TO_M;
    }
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    if (d.hasNormals) {
      const normals = new Float32Array(n * 3);
      for (let i = 0; i < n; i++) {
        const nx = bitsToF32(d.normalsBits[i * 3]);
        const ny = bitsToF32(d.normalsBits[i * 3 + 1]);
        const nz = bitsToF32(d.normalsBits[i * 3 + 2]);
        normals[i * 3] = nx; normals[i * 3 + 1] = nz; normals[i * 3 + 2] = -ny;
      }
      geometry.setAttribute('normal', new THREE.BufferAttribute(normals, 3));
    }
    if (d.uvCount > 0) {
      // [P-UV] NIF uv set 0 RAW (no V flip)
      geometry.setAttribute('uv', new THREE.BufferAttribute(new Float32Array(d.uvSetsBits[0].map(bitsToF32)), 2));
    }
    if (d.hasVertexColors) {
      const colors = new Float32Array(n * 4);
      for (let i = 0; i < n * 4; i++) colors[i] = bitsToF32(d.vertexColorsBits[i]);
      geometry.setAttribute('color', new THREE.BufferAttribute(colors, 4));
    }
    const index = new Uint16Array(d.triangles.length * 3);
    d.triangles.forEach((t, i) => { index[i * 3] = t[0]; index[i * 3 + 1] = t[1]; index[i * 3 + 2] = t[2]; });
    geometry.setIndex(new THREE.BufferAttribute(index, 1));
    if (!d.hasNormals) geometry.computeVertexNormals();
    renderables.push({
      modelId, shapeIndex: s.index, shapeName: s.fields.name,
      geometry, textureSlots: entriesForTexprop.map((e) => ({ textureId: e.textureId, name: e.name })),
      arkEntryName: entriesForTexprop[0].name,
      numVertices: n, numTriangles: d.numTriangles,
      hasVertexColors: d.hasVertexColors, hasUv: d.uvCount > 0,
      alpha: alphaBlk ? { flags: alphaBlk.fields.alphaFlags, threshold: alphaBlk.fields.alphaThreshold } : null,
    });
  }
  return { renderables, nonVisual, slotDiagnostics };
}

/**
 * WorldVegetation — the vegetation subsystem manager (R2: latest-request-wins
 * + the shared height query + the fair cap + statuses).
 * @param {object} deps
 *   scene            a THREE.Scene
 *   fetchJson(url)   async JSON fetch
 *   fetchBinary(url) async -> {payload, headers} (identity-checked by the caller)
 *   heightField      the SHARED PEHeightField (contract §3.2: the exact
 *                    rendered-triangle query + the real-sample halo)
 */
export class WorldVegetation {
  constructor({ scene, fetchJson, fetchBinary, heightField, onDiag = () => {} }) {
    if (!scene || typeof fetchJson !== 'function' || typeof fetchBinary !== 'function' || !heightField) {
      throw new Error('[WorldVegetation] scene, fetchJson, fetchBinary and heightField (the SHARED query) are required');
    }
    this.scene = scene;
    this.fetchJson = fetchJson;
    this.fetchBinary = fetchBinary;
    this.heightField = heightField;
    this.onDiag = onDiag;
    this.config = null;          // { profileMode, profile, labSeed, densityPercent }
    this.enabled = true;
    this.windowOrigin = null;
    this.requestSeq = 0;         // the LATEST-request wins (WL-1 fix)
    this.pendingRequest = null;  // the newest request made while a build ran
    this.buildBusy = false;
    this.recordsByProfile = new Map();  // profile -> records | {unsupported}
    this.modelCache = new Map();        // modelId -> entry (bounded LRU)
    this.modelCacheOrder = [];
    this.textureCache = new Map();      // textureId -> {texture,...} SHARED across model entries
    this.textureCacheOrder = [];
    this.meshes = [];              // the per-window InstancedMeshes (GEOMETRY)
    this.markerMeshes = [];        // the per-window diagnostic marker meshes
    this.group = new THREE.Group();
    this.group.name = 'vegetation-reconstruction-preview';
    this.group.visible = true;
    scene.add(this.group);
    this.fetchCounters = { modelPayloads: 0, texturePayloads: 0, climate: 0 };
    this.disposeCounters = { meshes: 0, geometries: 0, materials: 0, textures: 0, cacheEntries: 0 };
    this.lastCensus = null;
    this.lastError = null;
    this._markerGeometry = null;
    this._markerMaterial = null;
  }

  _ensureMarkerResources() {
    if (!this._markerGeometry) {
      this._markerGeometry = new THREE.BoxGeometry(1.2, 2.4, 1.2);
      this._markerGeometry.translate(0, 1.2, 0);
    }
    if (!this._markerMaterial) {
      this._markerMaterial = new THREE.MeshBasicMaterial({ color: 0xff3355, wireframe: true, transparent: true, opacity: 0.85 });
    }
    return { geometry: this._markerGeometry, material: this._markerMaterial };
  }

  async setConfig(config) {
    this.config = {
      profileMode: config.profileMode === 'regional' ? 'regional' : 'global',
      profile: Math.min(Math.max(config.profile | 0, 0), 31),
      labSeed: Math.max(0, Math.floor(Number(config.labSeed) || 0)) >>> 0,
      densityPercent: Math.min(Math.max(Math.round(Number(config.densityPercent) || 0), 0), 100),
    };
  }

  setEnabled(on) {
    this.enabled = !!on;
    this.group.visible = this.enabled;
  }

  /** The profile INDEX used for one tile (global mode: one profile; regional
   *  mode: OUR documented reconstruction map — never a historical biome). */
  profileForTile(gx, gy) {
    if (!this.config) throw new Error('[WorldVegetation] setConfig() first');
    if (this.config.profileMode === 'regional') return regionalProfileFor(gx, gy);
    return this.config.profile;
  }

  async _recordsForProfile(profile) {
    if (this.recordsByProfile.has(profile)) return this.recordsByProfile.get(profile);
    this.fetchCounters.climate++;
    let payload;
    try {
      payload = await this.fetchJson(`/api/world/climate/${profile}`);
    } catch (e) {
      payload = { ok: false, status: 'FETCH_ERROR', error: String(e?.message ?? e) };
    }
    const rec = payload?.status === 'DECODED' && Array.isArray(payload?.records) && payload.records.length > 0
      ? { records: payload.records, provenance: payload.provenance }
      : { records: null, unsupported: true, error: payload?.error ?? `profile ${profile} is not DECODED (strict decoder)` };
    this.recordsByProfile.set(profile, rec);
    while (this.recordsByProfile.size > 8) { // bounded: the regional mode uses ~4 profiles
      const first = this.recordsByProfile.keys().next().value;
      this.recordsByProfile.delete(first);
    }
    return rec;
  }

  /** The SHARED texture entry for one textureId (fetched + strict-decoded ONCE,
   *  reused by every model entry; a failed strict decode caches the honest
   *  unresolved reason — the model renders untextured, never a fallback). */
  async _textureEntry(textureId) {
    const hit = this.textureCache.get(textureId);
    if (hit) {
      this.textureCache.delete(textureId);
      this.textureCache.set(textureId, hit); // LRU refresh
      return hit;
    }
    let info;
    try {
      this.fetchCounters.texturePayloads++;
      const res = await this.fetchBinary(`/api/world/texture/${textureId}`);
      const dec = decodeModelTextureStrict(new Uint8Array(res.payload));
      const texture = new THREE.DataTexture(dec.rgba, dec.width, dec.height, THREE.RGBAFormat);
      texture.colorSpace = THREE.NoColorSpace; // SRGB passthrough (the established convention)
      texture.flipY = false;                    // [P-UV] v=0 = image TOP
      texture.wrapS = THREE.RepeatWrapping;     // clamp=3 -> WRAP (niflib TexClampMode)
      texture.wrapT = THREE.RepeatWrapping;
      texture.minFilter = THREE.LinearFilter;   // [P-MIPS] deterministic subset
      texture.magFilter = THREE.LinearFilter;
      texture.needsUpdate = true;
      info = { textureId, resolved: true, texture, width: dec.width, height: dec.height, bpp: dec.bpp, decoder: dec.decoder };
    } catch (e) {
      info = { textureId, resolved: false, reason: String(e?.message ?? e).slice(0, 260) };
    }
    this.textureCache.set(textureId, info);
    this.textureCacheOrder.push(textureId);
    return info;
  }

  /** Fetch + parse ONE model through the EXISTING qualified importer. */
  async _modelEntry(modelId) {
    const hit = this.modelCache.get(modelId);
    if (hit) {
      this.modelCache.delete(modelId);
      this.modelCache.set(modelId, hit);
      return hit;
    }
    const entry = { modelId, status: 'UNSUPPORTED', renderables: [], nonVisual: [], textures: [], reason: null };
    let payload, headers;
    try {
      this.fetchCounters.modelPayloads++;
      ({ payload, headers } = await this.fetchBinary(`/api/world/model/${modelId}`));
    } catch (e) {
      entry.reason = `model payload fetch failed: ${String(e?.message ?? e)}`;
      this._cachePut(modelId, entry);
      return entry;
    }
    let extraction;
    try {
      ({ extraction } = parseWitnessModel(payload, headers?.entryName ?? `${modelId}.nif`));
    } catch (e) {
      entry.reason = `the qualified importer refused LOUDLY: ${String(e?.message ?? e).slice(0, 300)}`;
      this._cachePut(modelId, entry);
      return entry;
    }
    entry.extractionBlocks = extraction.blocks.length;
    entry.nifVersion = extraction.header.versionString;
    const { renderables, nonVisual } = buildShapeRenderables(extraction, modelId);
    entry.renderables = renderables;
    entry.nonVisual = nonVisual;
    if (renderables.length === 0) {
      entry.status = 'UNSUPPORTED';
      entry.reason = 'no visual (texprop->Ark) shape chain in the model — nothing renderable through the qualified importer (honest UNSUPPORTED count; never a substitute model)';
      this._cachePut(modelId, entry);
      return entry;
    }
    // per-shape: try the texprop's Ark slots IN ORDER; use the FIRST that
    // strict-decodes; skipped slots are explicit diagnostics
    entry.status = 'SUPPORTED';
    entry.slotDiagnostics = [];
    for (const r of renderables) {
      let chosen = null;
      for (const slot of r.textureSlots) {
        const texInfo = await this._textureEntry(slot.textureId);
        if (texInfo.resolved) { chosen = { slot, texInfo }; break; }
        entry.slotDiagnostics.push({ modelId, shapeIndex: r.shapeIndex, textureId: slot.textureId, slotName: slot.name, reason: texInfo.reason });
      }
      if (!chosen) {
        entry.status = 'SUPPORTED_UNTEXTURED';
        r.textureId = r.textureSlots[0]?.textureId ?? null;
        continue;
      }
      r.textureId = chosen.slot.textureId;
      r.textureSlotName = chosen.slot.name;
      const alphaBlendOn = r.alpha ? (r.alpha.flags & 1) === 1 : false;
      const alphaThreshold = r.alpha ? r.alpha.threshold : 0;
      r.material = new THREE.MeshBasicMaterial({
        map: chosen.texInfo.texture,
        vertexColors: r.hasVertexColors,
        transparent: alphaBlendOn,
        alphaTest: alphaThreshold / 255.0,
        side: THREE.DoubleSide,   // [P-MATERIAL] CullMethod 2 exact mapping UNVERIFIED
        color: 0xffffff,
      });
    }
    entry.textureIds = [...new Set(renderables.map((r) => r.textureId).filter(Boolean))];
    // untextured shapes (no resolvable slot): the honest neutral material
    for (const r of renderables) {
      if (!r.material) {
        r.material = new THREE.MeshBasicMaterial({
          map: null, vertexColors: r.hasVertexColors, side: THREE.DoubleSide,
          color: 0x8a8f96, // untextured: neutral gray + the diagnostic label (never a fake texture)
        });
      }
    }
    this._cachePut(modelId, entry);
    return entry;
  }

  _cachePut(modelId, entry) {
    if (this.modelCache.has(modelId)) this.modelCache.delete(modelId);
    this.modelCache.set(modelId, entry);
    this.modelCacheOrder.push(modelId);
    const evictedIds = [];
    while (this.modelCacheOrder.length > MODEL_CACHE_MAX) {
      const old = this.modelCacheOrder.shift();
      const e = this.modelCache.get(old);
      if (e) { this._disposeModelEntry(e); this.modelCache.delete(old); evictedIds.push(old); }
    }
    if (evictedIds.length) this._pruneTextureCache();
  }

  _disposeModelEntry(entry) {
    for (const r of entry.renderables ?? []) {
      r.geometry?.dispose(); this.disposeCounters.geometries++;
      r.material?.dispose(); this.disposeCounters.materials++;
    }
    this.disposeCounters.cacheEntries++;
  }

  _referencedTextureIds() {
    const ref = new Set();
    for (const [, e] of this.modelCache) for (const t of e.textureIds ?? []) ref.add(t);
    return ref;
  }

  _pruneTextureCache() {
    const ref = this._referencedTextureIds();
    for (const [id, info] of [...this.textureCache]) {
      if (!ref.has(id)) {
        if (info.texture) { info.texture.dispose(); this.disposeCounters.textures++; }
        this.textureCache.delete(id);
        const k = this.textureCacheOrder.indexOf(id);
        if (k >= 0) this.textureCacheOrder.splice(k, 1);
      }
    }
  }

  _pruneModelCache(referencedIds) {
    for (const [id, entry] of [...this.modelCache]) {
      if (!referencedIds.has(id)) {
        this._disposeModelEntry(entry);
        this.modelCache.delete(id);
        const k = this.modelCacheOrder.indexOf(id);
        if (k >= 0) this.modelCacheOrder.splice(k, 1);
      }
    }
    this._pruneTextureCache();
  }

  _disposeWindowMeshes() {
    for (const m of this.meshes) {
      m.dispose();
      this.group.remove(m);
      this.disposeCounters.meshes++;
    }
    this.meshes = [];
    for (const m of this.markerMeshes) {
      m.dispose();
      this.group.remove(m);
      this.disposeCounters.meshes++;
    }
    this.markerMeshes = [];
  }

  /**
   * rebuild — regenerate the vegetation for ONE window origin. LATEST REQUEST
   * WINS (WL-1 fix): every rebuild carries a request id; a rebuild whose id
   * is no longer the latest ABORTS before applying anything, and the newest
   * request made while a build was busy is re-run when the current one
   * completes. DETERMINISTIC per tile (the same inputs give the same instance
   * set regardless of load order — measured by the gates).
   */
  async rebuild(origin, windowTiles = 8) {
    if (!this.config) throw new Error('[WorldVegetation] setConfig() first');
    const requestId = ++this.requestSeq;
    if (this.buildBusy) {
      // WL-1 FIX: the busy path stores THE NEWEST request (never loses it)
      this.pendingRequest = { origin, windowTiles, requestId };
      return null;
    }
    this.buildBusy = true;
    try {
      return await this._rebuildInner(origin, windowTiles, requestId);
    } finally {
      this.buildBusy = false;
      const next = this.pendingRequest;
      this.pendingRequest = null;
      if (next && next.requestId !== requestId) {
        void this.rebuild(next.origin, next.windowTiles); // the newest request runs
      }
    }
  }

  async _rebuildInner(origin, windowTiles, requestId) {
    const stale = () => this.requestSeq !== requestId;
    const cfg = this.config;
    // 1. the per-tile profiles (global: one; regional: OUR map)
    const tileProfiles = [];
    for (let dy = 0; dy < windowTiles; dy++) {
      const row = [];
      for (let dx = 0; dx < windowTiles; dx++) row.push(this.profileForTile(origin.gx + dx, origin.gy + dy));
      tileProfiles.push(row);
    }
    const usedProfiles = [...new Set(tileProfiles.flat())].sort((a, b) => a - b);
    const recordsByProfileHere = new Map();
    for (const p of usedProfiles) {
      const recInfo = await this._recordsForProfile(p);
      if (stale()) return { aborted: true, reason: 'superseded by a newer request (latest-wins; nothing applied)' };
      recordsByProfileHere.set(p, recInfo);
    }
    // an UNSUPPORTED profile (in the used set) = the honest zero-render state
    const unsupportedProfiles = usedProfiles.filter((p) => !recordsByProfileHere.get(p)?.records);
    if (unsupportedProfiles.length > 0 && unsupportedProfiles.length === usedProfiles.length) {
      this._disposeWindowMeshes();
      this.lastError = `profile(s) ${unsupportedProfiles.join(',')}: UNSUPPORTED by the strict decoder — the vegetation preview renders NOTHING for them (select a DECODED profile)`;
      this.lastCensus = {
        schemaVersion: VEGETATION_SCHEMA_VERSION,
        ok: false, profile: cfg.profile, profileMode: cfg.profileMode, unsupportedProfile: true,
        error: this.lastError,
        requested: 0, rendered: 0, limited: 0,
        mode: VEGETATION_MODE_LABEL,
      };
      return this.lastCensus;
    }
    // 2. generate the candidates per tile (DETERMINISTIC, per-tileKey; per
    //    tile its OWN profile's records)
    const candidates = [];
    let perTileCensus = null;
    const t0 = performance?.now?.() ?? Date.now();
    const perTileCounts = {};
    for (let dy = 0; dy < windowTiles; dy++) {
      for (let dx = 0; dx < windowTiles; dx++) {
        const gx = origin.gx + dx, gy = origin.gy + dy;
        const p = tileProfiles[dy][dx];
        const recInfo = recordsByProfileHere.get(p);
        if (!recInfo?.records) continue; // UNSUPPORTED tile profile: no candidates (honest)
        const { instances, census } = generateTileInstances({
          records: recInfo.records,
          labSeed: cfg.labSeed,
          gx, gy,
          densityPercent: cfg.densityPercent,
        });
        for (const inst of instances) inst.profile = p;
        candidates.push(...instances);
        perTileCounts[`${gx},${gy}`] = instances.length;
        perTileCensus = census;
      }
    }
    const requested = candidates.length;
    // 3. the SPATIALLY FAIR CAP (WL-5 fix): per-tile quota, largest remainder,
    //    >=1 for every non-empty tile — a PURE function of the per-tile counts
    const fair = fairCapQuota(perTileCounts, MAX_VISIBLE_INSTANCES);
    const active = [];
    let lodLimited = 0;
    const perTileCapPrice = {};
    for (let dy = 0; dy < windowTiles; dy++) {
      for (let dx = 0; dx < windowTiles; dx++) {
        const gx = origin.gx + dx, gy = origin.gy + dy;
        const key = `${gx},${gy}`;
        const tileCands = candidates.filter((c) => c.tile.gx === gx && c.tile.gy === gy);
        const quota = fair.quotaByTile[key] ?? 0;
        // deterministic within-tile order: generation order (record then j)
        for (let i = 0; i < tileCands.length; i++) {
          const inst = tileCands[i];
          if (i < quota) { inst.status = null; active.push(inst); }
          else { inst.status = SURFACE_STATUS.LOD_LIMITED; lodLimited++; }
        }
        perTileCapPrice[key] = { candidates: tileCands.length, selected: Math.min(quota, tileCands.length), limited: Math.max(0, tileCands.length - quota) };
      }
    }
    // 4. the per-model entries (bounded; SHARED cache)
    const idsWithInstances = [...new Set(active.map((i) => i.modelId))];
    const entries = new Map();
    for (const id of idsWithInstances) {
      const e = await this._modelEntry(id);
      if (stale()) return { aborted: true, reason: 'superseded by a newer request (latest-wins; nothing applied)' };
      entries.set(id, e);
    }
    // 5. SURFACE + status (WL-2 fix): the SHARED triangle query; no y=0.
    //    Status precedence (one status per instance): no real surface →
    //    DEFERRED_NO_SURFACE (never rendered, markers included); real surface
    //    + unsupported model → UNSUPPORTED_MODEL (diagnostic marker ON the
    //    real surface); real surface + supported model → PLACED.
    const unsupportedModel = [];
    const deferredNoSurface = [];
    const placed = [];
    for (const inst of active) {
      const entry = entries.get(inst.modelId);
      const unsupported = !entry || entry.status === 'UNSUPPORTED' || entry.renderables.length === 0;
      const h = this.heightField.triangleHeightAtWorld(inst.world.x, inst.world.y);
      if (h === null || h === undefined) {
        inst.status = SURFACE_STATUS.DEFERRED_NO_SURFACE; // honest: NOT rendered, counted
        inst.surfaceY = null;
        deferredNoSurface.push(inst);
        continue;
      }
      inst.surfaceY = h;
      if (unsupported) {
        inst.status = SURFACE_STATUS.UNSUPPORTED_MODEL;
        unsupportedModel.push(inst);
      } else {
        inst.status = SURFACE_STATUS.PLACED_ON_AVAILABLE_SURFACE;
        placed.push(inst);
      }
    }
    // 6. dispose the previous meshes; build the new InstancedMeshes
    if (stale()) return { aborted: true, reason: 'superseded by a newer request (latest-wins; nothing applied)' };
    this._disposeWindowMeshes();
    const instanceGroups = new Map();
    for (const inst of placed) {
      if (!instanceGroups.has(inst.modelId)) instanceGroups.set(inst.modelId, []);
      instanceGroups.get(inst.modelId).push(inst);
    }
    const markerGroups = new Map(); // UNSUPPORTED_MODEL diagnostic markers — on real surface data
    for (const inst of unsupportedModel) {
      if (!markerGroups.has(inst.modelId)) markerGroups.set(inst.modelId, []);
      markerGroups.get(inst.modelId).push(inst);
    }
    const perModelRendered = {};
    const perModelMarkers = {};
    let renderedInstances = 0, markerInstances = 0;
    for (const [modelId, insts] of instanceGroups) {
      perModelRendered[modelId] = insts.length;
      const entry = entries.get(modelId);
      for (const r of entry.renderables) {
        const mesh = new THREE.InstancedMesh(r.geometry, r.material, insts.length);
        this._applyInstanceMatrices(mesh, insts);
        mesh.userData.vegetation = { modelId, shapeIndex: r.shapeIndex, shapeName: r.shapeName, textureId: r.textureId };
        this.meshes.push(mesh);
        this.group.add(mesh);
      }
      renderedInstances += insts.length;
    }
    for (const [modelId, insts] of markerGroups) {
      perModelMarkers[modelId] = insts.length;
      const { geometry, material } = this._ensureMarkerResources();
      const marker = new THREE.InstancedMesh(geometry, material, insts.length);
      this._applyInstanceMatrices(marker, insts);
      this.markerMeshes.push(marker);
      this.group.add(marker);
      markerInstances += insts.length;
    }
    // 7. prune the caches to the referenced set
    this._pruneModelCache(new Set([...instanceGroups.keys(), ...markerGroups.keys()]));

    // 8. the honest census (per contract §6.5: indexed profile IDs, records,
    //    distinct candidate/selected/geometry-rendered IDs, markers, and the
    //    per-status counts; geometry vs markers SEPARATE)
    const recordsTotal = usedProfiles.reduce((a, p) => a + (recordsByProfileHere.get(p)?.records?.length ?? 0), 0);
    const distinctCandidateIds = [...new Set(candidates.map((i) => i.modelId))];
    const distinctSelectedIds = [...new Set(active.map((i) => i.modelId))];
    const distinctGeometryRenderedIds = [...new Set(placed.map((i) => i.modelId))];
    const supportedModels = [], untexturedModels = [], unsupportedModels = [];
    for (const [id, e] of entries) {
      if (e.status === 'SUPPORTED') supportedModels.push(id);
      else if (e.status === 'SUPPORTED_UNTEXTURED') {
        const reasons = (e.textureIds ?? []).map((tid) => this.textureCache.get(tid)).filter((t) => t && !t.resolved).map((t) => t.reason);
        untexturedModels.push({ id, reason: reasons.join(' | ') || 'texture chain unresolved' });
      } else unsupportedModels.push({ id, reason: e.reason });
    }
    this.lastError = null;
    this.windowOrigin = origin;
    this.lastCensus = {
      schemaVersion: VEGETATION_SCHEMA_VERSION,
      ok: true,
      mode: VEGETATION_MODE_LABEL,
      threeWaySeparation: VEGETATION_THREE_WAY_SEPARATION,
      wrapperVersion: LABSEED_WRAPPER_VERSION,
      densityPolicy: LAB_DENSITY_POLICY,
      regionalPreview: REGIONAL_PREVIEW,
      windowCalibration: LABSEED_WINDOW_CALIBRATION,
      config: { ...cfg, p3: 0, p3Note: '[P-RNG-P3] p3 = 0 (UNVERIFIED input) — shown SEPARATELY; NEVER the LAB_SEED' },
      window: { origin, windowTiles },
      profiles: {
        mode: cfg.profileMode,
        used: usedProfiles,
        unsupported: unsupportedProfiles,
        records: recordsTotal,
        regionalMap: cfg.profileMode === 'regional' ? REGIONAL_PREVIEW.mapRule : null,
      },
      counts: {
        requested, selected: active.length, limited: lodLimited, cap: MAX_VISIBLE_INSTANCES,
        placed: placed.length, deferredNoSurface: deferredNoSurface.length,
        unsupportedModel: unsupportedModel.length,
      },
      statusCounts: {
        [SURFACE_STATUS.PLACED_ON_AVAILABLE_SURFACE]: placed.length,
        [SURFACE_STATUS.DEFERRED_NO_SURFACE]: deferredNoSurface.length,
        [SURFACE_STATUS.UNSUPPORTED_MODEL]: unsupportedModel.length,
        [SURFACE_STATUS.LOD_LIMITED]: lodLimited,
      },
      distinctIds: {
        candidates: distinctCandidateIds.length, candidateIds: distinctCandidateIds,
        selected: distinctSelectedIds.length, selectedIds: distinctSelectedIds,
        geometryRendered: distinctGeometryRenderedIds.length, geometryRenderedIds: distinctGeometryRenderedIds,
        markers: markerGroups.size,
      },
      models: {
        withInstances: idsWithInstances.length,
        supported: supportedModels,
        untextured: untexturedModels,
        unsupported: unsupportedModels,
        nonVisualShapes: [...entries.values()].reduce((a, e) => a + (e.nonVisual?.length ?? 0), 0),
        slotDiagnostics: [...entries.values()].flatMap((e) => e.slotDiagnostics ?? []),
      },
      perModelRendered,
      perModelMarkers,
      perTileCapPrice,
      perTileCensusInputs: perTileCensus ? perTileCensus.inputs : null,
      perModelGenerator: perTileCensus ? perTileCensus.perModel : null,
      cache: {
        modelEntries: this.modelCache.size, max: MODEL_CACHE_MAX,
        sharedTextures: this.textureCache.size,
        sharedTexturesResolved: [...this.textureCache.values()].filter((t) => t.resolved).length,
      },
      fetchCounters: { ...this.fetchCounters },
      disposeCounters: { ...this.disposeCounters },
      elapsedMs: Math.round((performance?.now?.() ?? Date.now()) - t0),
      renderedInstances, markerInstances,
    };
    return this.lastCensus;
  }

  /** Apply the REAL per-instance transforms (position on the SHARED triangle
   *  query surface + the [P-SCALE] bridge; rotation IDENTITY). The cm->m unit
   *  bridge is applied EXACTLY ONCE inside the geometry — the instance scale
   *  carries ONLY the node-scale bridge. The height was resolved by the
   *  caller (status PLACED…/UNSUPPORTED_MODEL markers stand on real surface
   *  data too — never an invented y). */
  _applyInstanceMatrices(mesh, insts) {
    const m = new THREE.Matrix4();
    let n = 0;
    for (const inst of insts) {
      const s = inst.scale * NODE_SCALE_RENDER_BRIDGE;
      m.makeScale(s, s, s);
      m.setPosition(inst.world.x, inst.surfaceY, inst.world.y);
      mesh.setMatrixAt(n++, m);
    }
    mesh.instanceMatrix.needsUpdate = true;
    mesh.frustumCulled = true;
  }

  dispose() {
    this._disposeWindowMeshes();
    for (const [, entry] of this.modelCache) this._disposeModelEntry(entry);
    this.modelCache.clear();
    this.modelCacheOrder = [];
    for (const [, info] of this.textureCache) {
      if (info.texture) { info.texture.dispose(); this.disposeCounters.textures++; }
    }
    this.textureCache.clear();
    this.textureCacheOrder = [];
    if (this._markerGeometry) { this._markerGeometry.dispose(); this._markerGeometry = null; this.disposeCounters.geometries++; }
    if (this._markerMaterial) { this._markerMaterial.dispose(); this._markerMaterial = null; this.disposeCounters.materials++; }
    this.scene.remove(this.group);
  }
}
