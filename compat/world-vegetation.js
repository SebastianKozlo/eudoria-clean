// world-vegetation.js — PE_WORLD_LAUNCHER_R1_20261010, ETAP E (contract §6)
// THE /world vegetation subsystem: deterministic RECONSTRUCTION_PREVIEW
// instances standing on the terrain, rendered from ORIGINAL same-era model
// NIF payloads + their original textures where the binding resolves.
//
// THE THREE-WAY SEPARATION (contract §6 — binding, surfaced in the UI):
//   ORIGINAL_CLIMATE_RECORDS = the .vcl records served by /api/world/climate
//       (strict decode; 25.vcl stays UNSUPPORTED — this module renders NOTHING
//       for an UNSUPPORTED profile and shows the honest banner).
//   RECOVERED_RNG_ARITHMETIC = src/peworld/PEFoliageCore.js — imported
//       UNTOUCHED (the byte-locked seed/RNG/float chain runs inside the
//       generation wrapper).
//   INSTANCE_DISTRIBUTION = src/peworld/PEFoliageLabSeed.js — the DOCUMENTED
//       LAB_SEED wrapper ([P-CELLSTREAM] stand-in, LAB_SEED-keyed,
//       reconstruction-only; never the historical distribution).
//
// THE MODEL CHAIN (contract §6.5/§6.6 — the PROVEN witness pattern of
// terrain/model_witness.js, applied per shape):
//   model id -> /api/world/model/<id> (bounded ORIGINAL '<id>.nif' payload
//   from the pinned same-era PCG_9_3_5 Models.bnt) -> parseWitnessModel (the
//   EXISTING QUALIFIED single-witness importer — guards NEVER widened; a
//   refusal is an honest UNSUPPORTED count, never a substitute model) ->
//   per-shape renderables from the extraction (shape -> NiTexturingProperty
//   via the shape's properties refs -> the NiArkTextureExtraData entry
//   referencing that texprop -> textureId; the ARK 9-byte tail is consumed
//   by the READER canon rule and stays RAW-ONLY here) -> textureId ->
//   /api/world/texture/<id> -> decodeModelTextureStrict (32bpp A32 IMAGE
//   order / 24bpp TGA2; a payload outside the strict subset — e.g. a DDS —
//   renders the model honestly untextured with a diagnostic, NEVER a
//   fallback texture, never a stock pine under the same id) -> THREE
//   InstancedMeshes (shared geometry + shared material per (model, shape) +
//   REAL per-instance transforms — geometry sharing is NOT instance sharing).
//
// HONEST BOUNDS (labeled — the same placeholders as the proven pages):
//   [P-UNITS] the model NIF is in centimeters (FUN_0082b790 m->cm x100
//       evidence); the render bridges cm->m x0.01 EXACTLY ONCE (reversible
//       x100) — the model/terrain conversion is consistent with the adapter
//       meters of the terrain view (never an uncontrolled .01 transfer).
//   [P-AXIS] NIF Z-up -> Three Y-up via (x, z, -y) (the SAME documented
//       mapping as the deployed legacy GLB exporter + model_witness.js; the
//       engine's own transform is NOT decompiled — iter032 bound 5).
//   [P-UV] NIF uv set 0 used RAW (no V flip); texture rows top-first
//       (decodeTga2A32Image IMAGE order); DataTexture flipY=false -> v=0
//       samples the image TOP (the model-witness convention).
//   [P-MATERIAL] fixed MeshBasicMaterial (vertex-shaded: texture x vertex
//       colors — the era technique 'Vegetation' = FX 0x3EC is vertex-shaded,
//       iter032 stage 9); DoubleSide; alpha from the shape's own
//       NiAlphaProperty (fallback: the model's first alpha block — the
//       buildRenderModel rule); no wind animation.
//   [P-SCALE] THE NODE-SCALE RENDER BRIDGE = 2.0 / NODE_SCALE_MUL — the
//       EXACT ratio of the deployed foliage page (terrain/foliage_system.js:
//       "preserves the previously-deployed effective tree sizes"); the
//       instance scale = the binary node scale x this ratio = lerpValue x 2.0
//       (CURRENT_RUNTIME_CALIBRATION, NOT historical truth — the visualizer's
//       node-scale -> world-size transform is NOT decompiled, iter032 bound
//       5). The cm->m unit bridge (x0.01) is applied EXACTLY ONCE — in the
//       per-shape geometry (buildShapeRenderables); the INSTANCE matrix
//       applies NO further unit conversion (the conversion-once invariant,
//       contract §4: a double 0.01 would render the trees at 1/50 size —
//       caught by the ETAP_E pixel toggle gate). The bit-exact binary node
//       scale is carried on every instance.
//   [P-PLACE] instances stand on the terrain height sampled from the SAME
//       window region (bilinear over the raw u16 samples -> adapter meters —
//       the deployed foliage-page rule); placement + the preview-density
//       filter are RECONSTRUCTION choices (never historical placement).
//   COLLISION BOXES: shapes WITHOUT a texprop->Ark chain (the untextured
//       Bip01/Box 24v/12t candidates) are NOT rendered as visual geometry —
//       they are carried + counted as NON_VISUAL (role UNVERIFIED — the BVI
//       = local-collision corpus finding; never silently rendered).
//
// THE 5000-VISIBLE-INSTANCE CAP (contract §6.7 — a HARD display limit):
//   requested = every generated instance of the active window; rendered =
//   min(requested, 5000) taken in DETERMINISTIC generation order (window
//   tiles row-major, then record index, then j — the same inputs always give
//   the same limited subset); limited = requested - rendered. The census
//   displays requested/rendered/limited — never a fake full coverage.
//
// RESOURCE DISCIPLINE (contract §6.8): per-window InstancedMeshes are
//   disposed on EVERY rebuild; the per-model cache (geometry + material +
//   texture) is SHARED and survives window moves (no re-fetch, no
//   duplication — measured); entries NOT referenced by the current profile +
//   window instance set are pruned (disposed + dropped) so a profile/seed
//   change releases unused resources WITHOUT destroying still-shared ones.
'use strict';

import * as THREE from 'three';
import { parseWitnessModel } from '../src/pesource/NifModelReader.js';
import { decodeTga2, decodeTga2A32Image } from '../src/pesource/TgaDecoder.js';
import {
  generateTileInstances, VEGETATION_THREE_WAY_SEPARATION, LABSEED_WINDOW_CALIBRATION,
  LABSEED_WRAPPER_VERSION,
} from '../src/peworld/PEFoliageLabSeed.js';
import { NODE_SCALE_MUL } from '../src/peworld/PEFoliageCore.js';

export const VEGETATION_SCHEMA_VERSION = 'world-vegetation-v1';
export const MAX_VISIBLE_INSTANCES = 5000;   // the HARD display cap (contract §6.7)
export const MODEL_CACHE_MAX = 16;           // bounded per-model cache
export const NODE_SCALE_RENDER_BRIDGE = 2.0 / NODE_SCALE_MUL; // [P-SCALE] (the deployed-page ratio; lerpValue x 2.0)
export const UNIT_BRIDGE_CM_TO_M = 0.01;     // [P-UNITS] applied EXACTLY ONCE (in the per-shape geometry)
export const VEGETATION_MODE_LABEL = 'VEGETATION_MODE = RECONSTRUCTION_PREVIEW';

/** The per-shape renderable built from the extraction (my code — the reader
 * file stays untouched; every rule below is the reader's own canon):
 * shape -> dataRef -> NiTriShapeData; texprop via the shape's properties
 * refs; the Ark entry referencing that texprop -> textureId; alpha via the
 * shape's own NiAlphaProperty ref (fallback: the first alpha block). */
function buildShapeRenderables(extraction, modelId) {
  const blocks = extraction.blocks;
  const bitsToF32 = (hex) => {
    const u = new Uint32Array(1);
    const b = new Uint8Array(u.buffer);
    for (let i = 0; i < 4; i++) b[i] = parseInt(hex.substr(i * 2, 2), 16);
    return new Float32Array(u.buffer)[0];
  };
  const arkEntries = blocks.filter((b) => b.type === 'NiArkTextureExtraData')
    .flatMap((ab) => ab.fields.entries.map((e) => ({ ...e, texprop: e.ref })));
  const renderables = [];
  const nonVisual = [];
  for (const s of blocks.filter((b) => b.type === 'NiTriShape')) {
    const dataBlk = blocks[s.fields.dataRef];
    if (!dataBlk || dataBlk.type !== 'NiTriShapeData') {
      nonVisual.push({ shapeIndex: s.index, shapeName: s.fields.name, reason: 'NO_DATA_BLOCK' });
      continue;
    }
    const texprop = (s.fields.properties ?? [])
      .map((i) => blocks[i]).find((b) => b?.type === 'NiTexturingProperty');
    const arkEntry = texprop ? arkEntries.find((e) => e.texprop === texprop.index) : null;
    if (!texprop || !arkEntry) {
      nonVisual.push({ shapeIndex: s.index, shapeName: s.fields.name, reason: 'NON_VISUAL_NO_TEXPROP_ARK_CHAIN (untextured Bip01/Box candidate — collision/bounds role UNVERIFIED; carried + counted, NOT rendered)' });
      continue;
    }
    const alphaBlk = (s.fields.properties ?? [])
      .map((i) => blocks[i]).find((b) => b?.type === 'NiAlphaProperty')
      ?? blocks.find((b) => b.type === 'NiAlphaProperty'); // the buildRenderModel fallback rule
    const d = dataBlk.fields;
    const n = d.numVertices;
    // [P-AXIS] (x, z, -y) + [P-UNITS] x0.01, with the SHAPE'S OWN transform
    // composed first (measured: only 457523's Geo_Rock shape carries one —
    // all parent NiNodes of the shape chains are identity in this corpus).
    const st = s.fields;
    const T = st.translation.map(bitsToF32);
    const R = st.rotation.map((r) => r.map(bitsToF32));
    const S = bitsToF32(st.scale);
    const positions = new Float32Array(n * 3);
    for (let i = 0; i < n; i++) {
      // the shape-local vertex, transformed by the shape's own TRS
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
      geometry, textureId: arkEntry.textureId, arkEntryName: arkEntry.name,
      numVertices: n, numTriangles: d.numTriangles,
      hasVertexColors: d.hasVertexColors, hasUv: d.uvCount > 0,
      alpha: alphaBlk ? { flags: alphaBlk.fields.alphaFlags, threshold: alphaBlk.fields.alphaThreshold } : null,
    });
  }
  return { renderables, nonVisual };
}

/** The strict texture decode dispatch (the server's decodeModelTextureStrict,
 * mirrored client-side with the SAME production decoders — bpp 32 -> A32
 * IMAGE order, bpp 24 -> TGA2; anything else fails LOUDLY (honest
 * untextured, never a fallback). */
export function decodeModelTextureStrict(payload) {
  if (!(payload instanceof Uint8Array) || payload.length < 18) {
    throw new Error('[world-vegetation] payload too small for a TGA header');
  }
  const bpp = payload[16];
  if (bpp === 32) {
    const d = decodeTga2A32Image(payload);
    return { bpp, width: d.width, height: d.height, rgba: d.rgba, decoder: 'decodeTga2A32Image (TGA2 A32 IMAGE order — row 0 = visual TOP)' };
  }
  if (bpp === 24) {
    const d = decodeTga2(payload);
    return { bpp, width: d.width, height: d.height, rgba: d.rgba, decoder: 'decodeTga2 (TGA2 24bpp terrain-texture subset)' };
  }
  throw new Error(`[world-vegetation] bpp ${bpp} outside the strict model-texture subset {24, 32} — the payload fails LOUDLY (honest untextured; never a fallback texture)`);
}

/**
 * WorldVegetation — the vegetation subsystem manager.
 * @param {object} deps
 *   scene            a THREE.Scene (the meshes are added/removed)
 *   fetchJson(url)   async JSON fetch (the world-app fetchJson)
 *   fetchBinary(url) async -> {arrayBuffer, headers} (identity-checked by the caller)
 *   heightSampler(worldX, worldZ) -> meters|null  (the terrain height at a
 *                    world point — the SAME window region the terrain view
 *                    renders; null = outside the active data window)
 *   onDiag(diag)     optional callback for diagnostics
 */
export class WorldVegetation {
  constructor({ scene, fetchJson, fetchBinary, heightSampler, onDiag = () => {} }) {
    if (!scene || typeof fetchJson !== 'function' || typeof fetchBinary !== 'function' || typeof heightSampler !== 'function') {
      throw new Error('[WorldVegetation] scene, fetchJson, fetchBinary and heightSampler are required');
    }
    this.scene = scene;
    this.fetchJson = fetchJson;
    this.fetchBinary = fetchBinary;
    this.heightSampler = heightSampler;
    this.onDiag = onDiag;
    this.config = null;          // { profile, labSeed, densityPercent }
    this.enabled = true;
    this.windowOrigin = null;
    this.recordsByProfile = new Map();  // profile -> records | {unsupported}
    this.modelCache = new Map();        // modelId -> entry (bounded LRU below)
    this.modelCacheOrder = [];
    this.textureCache = new Map();      // textureId -> {texture,...} SHARED across model entries
    this.textureCacheOrder = [];
    this.meshes = [];              // the per-window InstancedMeshes
    this.markerMeshes = [];        // the per-window diagnostic marker meshes
    this.group = new THREE.Group();
    this.group.name = 'vegetation-reconstruction-preview';
    this.group.visible = true;
    scene.add(this.group);
    this.fetchCounters = { modelPayloads: 0, texturePayloads: 0, climate: 0 };
    this.disposeCounters = { meshes: 0, geometries: 0, materials: 0, textures: 0, cacheEntries: 0 };
    this.lastCensus = null;
    this.lastError = null;
    this.buildBusy = false;
    this._markerGeometry = null;   // shared diagnostic marker geometry (lazily built)
    this._markerMaterial = null;   // shared diagnostic marker material
  }

  /** The shared diagnostic marker geometry (a small wireframe box — a MARKER,
   * explicitly NOT an original tree model; built once, shared, disposed with
   * the subsystem). */
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
      profile: Math.min(Math.max(config.profile | 0, 0), 31),
      labSeed: Math.max(0, Math.floor(Number(config.labSeed) || 0)) >>> 0,
      densityPercent: Math.min(Math.max(Math.round(Number(config.densityPercent) || 0), 0), 100),
    };
  }

  setEnabled(on) {
    this.enabled = !!on;
    this.group.visible = this.enabled;
  }

  /** Fetch + cache the climate records of a profile (25.vcl -> the honest
   * UNSUPPORTED state — never comma-converted). */
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
    // bounded: keep at most 4 profiles of records (~60 KB each)
    while (this.recordsByProfile.size > 4) {
      const first = this.recordsByProfile.keys().next().value;
      this.recordsByProfile.delete(first);
    }
    return rec;
  }

  /** The SHARED texture entry for one textureId (fetched + strict-decoded
   * ONCE, reused by every model entry that binds it — contract §6.8: shared
   * resources are never duplicated per model). A failed strict decode caches
   * the honest unresolved reason (the model renders untextured — never a
   * fallback). */
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

  /** Fetch + parse ONE model through the EXISTING qualified importer.
   * Returns a cache entry {modelId, status, renderables, nonVisual, textures,
   * reason?} — status SUPPORTED / SUPPORTED_UNTEXTURED / UNSUPPORTED. The
   * entry is BOUNDED (LRU) and SHARED across windows. */
  async _modelEntry(modelId) {
    const hit = this.modelCache.get(modelId);
    if (hit) {
      // LRU refresh
      this.modelCache.delete(modelId);
      this.modelCache.set(modelId, hit);
      return hit;
    }
    const entry = { modelId, status: 'UNSUPPORTED', renderables: [], nonVisual: [], textures: [], reason: null };
    // 1. the ORIGINAL bounded payload
    let payload, headers;
    try {
      this.fetchCounters.modelPayloads++;
      ({ payload, headers } = await this.fetchBinary(`/api/world/model/${modelId}`));
    } catch (e) {
      entry.reason = `model payload fetch failed: ${String(e?.message ?? e)}`;
      this._cachePut(modelId, entry);
      return entry;
    }
    // 2. the EXISTING qualified importer (LOUD failures — honest UNSUPPORTED)
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
    // 3. per-shape renderables (texprop -> Ark -> textureId; non-visual counted)
    const { renderables, nonVisual } = buildShapeRenderables(extraction, modelId);
    entry.renderables = renderables;
    entry.nonVisual = nonVisual;
    if (renderables.length === 0) {
      entry.status = 'UNSUPPORTED';
      entry.reason = 'no visual (texprop->Ark) shape chain in the model — nothing renderable through the qualified importer (honest UNSUPPORTED count; never a substitute model)';
      this._cachePut(modelId, entry);
      return entry;
    }
    // 4. per-textureId shared entries (the SHARED texture cache — one fetch +
    // strict decode per textureId across ALL model entries)
    entry.status = 'SUPPORTED';
    for (const r of renderables) {
      const texInfo = await this._textureEntry(r.textureId);
      if (!texInfo.resolved) entry.status = 'SUPPORTED_UNTEXTURED';
    }
    entry.textureIds = [...new Set(renderables.map((r) => r.textureId))];
    // 5. one shared material per shape (bound to the shape's texture chain)
    for (const r of renderables) {
      const texInfo = this.textureCache.get(r.textureId);
      const alphaBlendOn = r.alpha ? (r.alpha.flags & 1) === 1 : false;
      const alphaThreshold = r.alpha ? r.alpha.threshold : 0;
      r.material = new THREE.MeshBasicMaterial({
        map: texInfo?.resolved ? texInfo.texture : null,
        vertexColors: r.hasVertexColors,
        transparent: alphaBlendOn,
        alphaTest: alphaThreshold / 255.0,
        side: THREE.DoubleSide,   // [P-MATERIAL] CullMethod 2 exact mapping UNVERIFIED
        color: texInfo?.resolved ? 0xffffff : 0x8a8f96, // untextured: neutral gray + the diagnostic label (never a fake texture)
      });
    }
    this._cachePut(modelId, entry);
    return entry;
  }

  _cachePut(modelId, entry) {
    if (this.modelCache.has(modelId)) this.modelCache.delete(modelId);
    this.modelCache.set(modelId, entry);
    this.modelCacheOrder.push(modelId);
    let evictedIds = [];
    while (this.modelCacheOrder.length > MODEL_CACHE_MAX) {
      const old = this.modelCacheOrder.shift();
      const e = this.modelCache.get(old);
      if (e) { this._disposeModelEntry(e); this.modelCache.delete(old); evictedIds.push(old); }
    }
    if (evictedIds.length) this._pruneTextureCache(); // evicted models may have been the last referents
  }

  _disposeModelEntry(entry) {
    for (const r of entry.renderables ?? []) {
      r.geometry?.dispose(); this.disposeCounters.geometries++;
      r.material?.dispose(); this.disposeCounters.materials++;
    }
    // NOTE: textures are OWNED by the shared texture cache (never disposed
    // per model entry — a texture shared by several models survives them).
    this.disposeCounters.cacheEntries++;
  }

  /** The set of texture ids referenced by the CURRENT model cache entries. */
  _referencedTextureIds() {
    const ref = new Set();
    for (const [, e] of this.modelCache) for (const t of e.textureIds ?? []) ref.add(t);
    return ref;
  }

  /** Prune the SHARED texture cache to the referenced set (a texture whose
   * last referent is gone is disposed + dropped — unused resources are
   * released; still-referenced shared textures are NEVER destroyed). */
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

  /** Prune the model cache to the REFERENCED set (profile/seed change + region
   * unload release UNUSED instances/materials/textures WITHOUT destroying
   * shared resources — contract §6.8), then prune the shared textures. */
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

  /** Dispose the per-window meshes (the shared model cache SURVIVES — window
   * moves reuse geometry/material/texture without re-fetching). */
  _disposeWindowMeshes() {
    for (const m of this.meshes) {
      m.dispose();  // the InstancedMesh instance buffers
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
   * rebuild — regenerate the vegetation for ONE window origin. DETERMINISTIC:
   * the same (records + labSeed + densityPercent + window origin + calibration)
   * always produces the SAME instance set regardless of load order (each
   * tile is generated independently keyed on its tileKey — streaming-order
   * invariance by construction, measured by the gates).
   * @param {{gx, gy}} origin the window origin (top-left tile)
   * @param {number} windowTiles the window size (8 -> an 8x8 tile window)
   */
  async rebuild(origin, windowTiles = 8) {
    if (!this.config) throw new Error('[WorldVegetation] setConfig() first');
    if (this.buildBusy) return this.lastCensus;  // a rebuild in flight: the caller re-triggers
    this.buildBusy = true;
    try {
      const cfg = this.config;
      const recInfo = await this._recordsForProfile(cfg.profile);
      if (!recInfo.records) {
        // the honest UNSUPPORTED-profile state: NOTHING renders, the census
        // carries the reason (never comma-converted, never a fallback profile)
        this._disposeWindowMeshes();
        this.lastError = `profile ${cfg.profile}: UNSUPPORTED by the strict decoder — ${recInfo.error ?? 'no records'} (the vegetation preview renders NOTHING for this profile; select a DECODED profile)`;
        this.lastCensus = {
          schemaVersion: VEGETATION_SCHEMA_VERSION,
          ok: false, profile: cfg.profile, unsupportedProfile: true,
          error: this.lastError,
          requested: 0, rendered: 0, limited: 0,
          mode: VEGETATION_MODE_LABEL,
        };
        return this.lastCensus;
      }
      // 1. generate the instances per tile (DETERMINISTIC; fixed tile order —
      // per-tile keyed, so the ORDER of this loop cannot change any set)
      const all = [];
      let perTileCensus = null;
      const t0 = performance?.now?.() ?? Date.now();
      for (let dy = 0; dy < windowTiles; dy++) {
        for (let dx = 0; dx < windowTiles; dx++) {
          const gx = origin.gx + dx, gy = origin.gy + dy;
          const { instances, census } = generateTileInstances({
            records: recInfo.records,
            labSeed: cfg.labSeed,
            gx, gy,
            densityPercent: cfg.densityPercent,
          });
          all.push(...instances);
          perTileCensus = census; // the inputs are identical per tile (window-independent)
        }
      }
      const requested = all.length;
      // 2. the 5000-cap in DETERMINISTIC generation order (tiles row-major —
      // the SAME order this loop built them in, so the limited subset is a
      // pure function of the inputs)
      const limited = Math.max(0, requested - MAX_VISIBLE_INSTANCES);
      const rendered = requested - limited;
      const active = all.slice(0, MAX_VISIBLE_INSTANCES);

      // 3. ensure the model cache covers every model with instances
      const idsWithInstances = [...new Set(active.map((i) => i.modelId))];
      const entries = new Map();
      for (const id of idsWithInstances) {
        entries.set(id, await this._modelEntry(id));
      }

      // 4. dispose the previous window's meshes; build the new InstancedMeshes
      this._disposeWindowMeshes();
      const instanceGroups = new Map(); // modelId -> instances[]
      for (const inst of active) {
        if (!instanceGroups.has(inst.modelId)) instanceGroups.set(inst.modelId, []);
        instanceGroups.get(inst.modelId).push(inst);
      }
      const perModelRendered = {};
      let renderedInstances = 0, markerInstances = 0;
      for (const [modelId, insts] of instanceGroups) {
        perModelRendered[modelId] = insts.length;
        const entry = entries.get(modelId);
        if (!entry || entry.status === 'UNSUPPORTED' || entry.renderables.length === 0) {
          // honest diagnostic MARKER (explicitly NOT an original tree model)
          const { geometry, material } = this._ensureMarkerResources();
          const marker = new THREE.InstancedMesh(geometry, material, insts.length);
          this._applyInstanceMatrices(marker, insts, 1.0);
          this.markerMeshes.push(marker);
          this.group.add(marker);
          markerInstances += insts.length;
          continue;
        }
        for (const r of entry.renderables) {
          const mesh = new THREE.InstancedMesh(r.geometry, r.material, insts.length);
          this._applyInstanceMatrices(mesh, insts, 1.0);
          mesh.userData.vegetation = { modelId, shapeIndex: r.shapeIndex, shapeName: r.shapeName };
          this.meshes.push(mesh);
          this.group.add(mesh);
        }
        renderedInstances += insts.length;
      }

      // 5. prune the cache to the referenced set (unused released; shared kept)
      this._pruneModelCache(new Set([...instanceGroups.keys()]));

      const supportedModels = [], untexturedModels = [], unsupportedModels = [];
      for (const [id, e] of entries) {
        if (e.status === 'SUPPORTED') supportedModels.push(id);
        else if (e.status === 'SUPPORTED_UNTEXTURED') {
          const reasons = (e.textureIds ?? [])
            .map((tid) => this.textureCache.get(tid))
            .filter((t) => t && !t.resolved)
            .map((t) => t.reason);
          untexturedModels.push({ id, reason: reasons.join(' | ') || 'texture chain unresolved' });
        }
        else unsupportedModels.push({ id, reason: e.reason });
      }
      this.lastError = null;
      this.lastCensus = {
        schemaVersion: VEGETATION_SCHEMA_VERSION,
        ok: true,
        mode: VEGETATION_MODE_LABEL,
        threeWaySeparation: VEGETATION_THREE_WAY_SEPARATION,
        wrapperVersion: LABSEED_WRAPPER_VERSION,
        windowCalibration: LABSEED_WINDOW_CALIBRATION,
        config: { ...cfg, p3: 0, p3Note: '[P-RNG-P3] p3 = 0 (UNVERIFIED input) — shown SEPARATELY; NEVER the LAB_SEED' },
        window: { origin, windowTiles },
        counts: { requested, rendered, limited, cap: MAX_VISIBLE_INSTANCES, limitedApplied: limited > 0 },
        models: {
          withInstances: idsWithInstances.length,
          supported: supportedModels, untextured: untexturedModels, unsupported: unsupportedModels,
          nonVisualShapes: [...entries.values()].reduce((a, e) => a + (e.nonVisual?.length ?? 0), 0),
        },
        perModelRendered,
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
    } catch (e) {
      this.lastError = String(e?.message ?? e);
      this.lastCensus = { schemaVersion: VEGETATION_SCHEMA_VERSION, ok: false, error: this.lastError, mode: VEGETATION_MODE_LABEL };
      return this.lastCensus;
    } finally {
      this.buildBusy = false;
    }
  }

  /** Apply the REAL per-instance transforms (position on terrain height +
   * the [P-SCALE] bridge; rotation IDENTITY — RE-faithful: the spawn loop
   * sets position + scale + model id only). The cm->m unit bridge is
   * already applied EXACTLY ONCE inside the geometry — the instance scale
   * carries ONLY the node-scale bridge (NO second unit conversion). */
  _applyInstanceMatrices(mesh, insts, _unusedScale = 1.0) {
    const m = new THREE.Matrix4();
    let n = 0;
    for (const inst of insts) {
      const h = this.heightSampler(inst.world.x, inst.world.y);
      const y = h === null || h === undefined ? 0 : h; // outside the active data window: height 0 + the census note (never a fake sample)
      const s = inst.scale * NODE_SCALE_RENDER_BRIDGE;
      m.makeScale(s, s, s);
      m.setPosition(inst.world.x, y, inst.world.y);
      mesh.setMatrixAt(n++, m);
    }
    mesh.instanceMatrix.needsUpdate = true;
    mesh.frustumCulled = true;
  }

  /** Full dispose (the subsystem goes away): window meshes + the shared
   * model cache + the SHARED texture cache + the marker resources. Used only
   * on teardown. */
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
