// world-app.js — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010 (contract §3–§7)
// THE /world view: the WHOLE AVAILABLE MAP as a continuous world.
//
// THE R2 DESIGN (binding — each item cites the contract):
//   §3.1 LATEST-REQUEST SCENE IDENTITY: one explicit requested-scene identity
//     (era + container identities + focus/region + profile mode + seed/
//     density + adapter versions); terrain/textures/vegetation rebuilds carry
//     a generation/request id; a STALE result never replaces the newer scene
//     or the READY state (abort before apply + dispose); busy never loses the
//     newest request (latest-wins queues: terrain pendingOrigin, vegetation
//     pendingRequest, texture generation gate). The previous coherent scene
//     stays until the new one is ready (honest LOADING/PARTIAL — never
//     terrain A with trees B as READY; the coherence line shows all three
//     window origins).
//   §3.2 ONE SHARED HEIGHT QUERY: PEHeightField (triangle-exact on EXACTLY
//     the near layer's rendered triangles; raw u16 preserved; the decode
//     offset/calibration applied EXACTLY ONCE; NO smoothing) serves the
//     render layer, the trees and the walker. The 256-samples/0..510 vs
//     0..512 boundary is resolved with a 1-tile HALO of REAL neighboring
//     samples (10x10 fetch for an 8x8 window); positions without real
//     surface data return null (never the last height duplicated, never
//     interpolation through an unknown tile, never y=0). Movement computes
//     the candidate position FIRST, checks the surface, and only then
//     commits X/Y/Z; no data = stop at the last safe position + prefetch
//     (the streaming window follows); LOADING is distinguished from the
//     actual corpus boundary in the banner.
//   §4 CONTINUOUS WORLD: near 8x8 window (RAW payloads, PETerrainRegion) +
//     WorldLod mid ring (8x8-decimated REAL samples) + far whole-world mesh
//     (4x4-decimated REAL samples, census-gated) — decimation of ORIGINAL
//     SAMPLES (renderer LOD policy with explicit coverage/seams; missing
//     tiles are NAMED holes, never zero surface; no skirts needed — the
//     boundary grid lines MATCH across levels). The regular-tile
//     denominator comes from the server's MEASURED index census (never a
//     hardcoded 51920).
//   §5 CAMERA/UI: reference preset FOV 45, damping 0.08, minDistance 10,
//     maxDistance 50000, far 200000 (near 0.5 + logarithmicDepthBuffer —
//     the justified world-scale choice; never a claimed historical unit);
//     streaming follows the VIEWED FOCUS (controls.target in orbit), not an
//     arbitrary camera position; F/Reset frame the same focus stably (3x);
//     canvas >=85%/80% of the viewport with the collapsible „Szczegóły”
//     drawer; drawer preferences remembered; inputs never capture movement
//     keys; resize updates the drawing buffer/aspect WITHOUT a camera reset.
//   §6 VEGETATION: WorldVegetation r2 (recIndex identity + fractional
//     density + spatially-fair cap + explicit instance statuses + optional
//     regional RECONSTRUCTION_PREVIEW) — see compat/world-vegetation.js.
//   §7 ROSETTA DEBUG POINT: click terrain/model -> era + container SHA +
//     entry/payload SHA -> decoder/schema -> scene object/material ->
//     applied display/LOD/reconstruction policy (the drawer shows it).
//
// DATA PATH (production modules, no parallel decoder — unchanged from R1):
//   /api/world/tile/<gx>/<gy> (2048 B uint16 LE, raw heights offset 64..2111,
//   provenance headers) -> canonical TerrainTile -> PETerrainRegion (8x8
//   render window) + PEHeightField (10x10 halo sampling field) -> Three.js.
'use strict';

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { PETerrainRegion, worldHeightMeters, PE_TERRAIN_METER_PER_SAMPLE } from '/src/peworld/PETerrainCore.js';
import { PEHeightField, SURFACE_STATUS } from '/src/peworld/PEHeightQuery.js';
import { TerrainTile } from '/src/pesource/TerrainTile.js';
import { makeProvenance } from '/src/pesource/PEProvenance.js';
import { decodeTga2 } from '/src/pesource/TgaDecoder.js';
import {
  buildRegionSplatData, RENDER_RECONSTRUCTION_PRESET, REGION_CELLS,
  WORLD_SPLAT_SCHEMA_VERSION, MAX_LAYERS_PER_CELL,
} from '/compat/world-splat.js';
import {
  WorldVegetation, MAX_VISIBLE_INSTANCES, MODEL_CACHE_MAX, VEGETATION_SCHEMA_VERSION,
  REGIONAL_PREVIEW, regionalProfileFor,
} from '/compat/world-vegetation.js';
import { WorldLod, WORLD_LOD_VERSION } from '/compat/world-lod.js';

const $ = (id) => document.getElementById(id);
const RUN_ID = 'PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010';
const GRID_W = 220, GRID_H = 236;          // regular filename-xy tile grid (capacity)
const TILE_M = 64;                          // 32 samples × 2 m (CURRENT_RUNTIME_CALIBRATION)
const WINDOW_T = 8;                         // 8×8 near window (64 active tiles)
const HALO_T = 1;                           // the 1-tile REAL-sample halo ring (§3.2)
const FIELD_T = WINDOW_T + HALO_T * 2;      // the height sampling field: 10×10 tiles
const CLIENT_CACHE_MAX = 512;               // bounded LRU of raw tile payloads
const TEXTURE_CACHE_MAX = 64;               // bounded LRU of decoded texture RGBA
const EYE_OFFSET_M = 1.7;                   // walk-mode viewer eye offset (VIEWER SETTING, not PE data)
const UV_REPEAT_M = 32;                     // RENDER_RECONSTRUCTION: world meters per texture repeat
const MATERIAL_CELL_M = 4;                  // 2×2 samples per 16x16 material cell = 4 m

const params = parseHash();
const state = {
  status: null,
  anchor: null,                 // selected patch anchor {gx,gy}
  spawn: null,                  // {x, z} world meters
  windowOrigin: null,           // {gx,gy} current 8x8 near window origin
  region: null, mesh: null, boundsLines: null, lastGeo: null,
  heightField: null,            // THE SHARED height query (PEHeightField over the 10×10 field)
  cache: new Map(),             // "gx,gy" -> {heights, identity, tile}
  cacheOrder: [],
  fetchCount: 0, fetchErrors: 0, lastError: null,
  rebuildBusy: false, pendingOrigin: null, rebuilds: 0,
  mode: 'orbit',
  firstFrameDone: false,
  boundaryHit: false,
  boundaryReason: null,         // 'LOADING' | 'CORPUS_EDGE' | null (the honest distinction)
  diag: [],
  // ---- §3.1: the scene request identity + coherence ----
  sceneSeq: 0,
  sceneRequest: null,           // { id, origin, era, containers, profileMode, profile, labSeed, density, calibration, versions }
  coherence: { terrain: null, splat: null, veg: null },
  readyShown: false,
  // ---- ETAP D: the material->texture chain state ----
  texturesOn: params.textures !== '0',
  splat: null,
  materialsByOrigin: new Map(),
  textureRgbaCache: new Map(),
  textureRgbaOrder: [],
  mat: {
    materialsFetches: 0, materialsErrors: 0,
    textureFetches: 0, textureErrors: 0,
    lastDiag: null,
    busy: false,
  },
  // ---- vegetation ----
  vegOn: params.veg !== '0',
  veg: null,
  vegCensus: null,
  vegBusy: false,
  vegPending: null, // P1-2 fix: the WRAPPER-level latest-wins slot (a newer request while busy is STORED, never dropped)
  vegTrace: [],     // P1-2 diagnostics: a bounded ring of wrapper request/store/drain/commit events (read-only via __peR2Debug)
  vegConfig: { profileMode: params.region === '1' ? 'regional' : 'global', profile: params.profile, labSeed: params.seed, densityPercent: params.density },
  // ---- the distant LOD ----
  lod: null,
  lodFarReadyShown: false,
  // ---- §7 debug point ----
  debugPoint: null,
  teleportCount: 0,
};

function parseHash() {
  const h = new URLSearchParams(location.hash.replace(/^#/, ''));
  const tile = (h.get('tile') ?? '').split(',');
  let anchor = null;
  if (tile.length === 2 && Number.isInteger(+tile[0]) && Number.isInteger(+tile[1])) {
    anchor = { gx: Math.min(Math.max(+tile[0], 0), GRID_W - 4), gy: Math.min(Math.max(+tile[1], 0), GRID_H - 4) };
  }
  return {
    anchor,
    profile: Math.min(Math.max(parseInt(h.get('profile') ?? '0', 10) || 0, 0), 31),
    seed: Math.max(0, Math.floor(Number(h.get('seed') ?? '0') || 0)),
    density: Math.min(Math.max(parseInt(h.get('density') ?? '50', 10) || 0, 0), 100),
    textures: h.get('textures'),
    veg: h.get('veg'),
    region: h.get('region'),
  };
}

function hud(msg) { $('hud-line').textContent = msg; }
function banner(msg) { const b = $('error-banner'); if (msg) { b.textContent = msg; b.hidden = false; } else b.hidden = true; }
function setLoadStatus(s) {
  $('diagnostics').setAttribute('data-load-status', s);
  state.diag.push(`${new Date().toISOString()} data-load-status = ${s}`);
  $('world-diag').textContent = state.diag.slice(-14).join('\n');
}

async function fetchJson(url) {
  const r = await fetch(url, { cache: 'no-store' });
  const t = await r.text();
  let j = null; try { j = JSON.parse(t); } catch { /* none */ }
  if (!r.ok) throw new Error((j && (j.error || j.message)) || `HTTP ${r.status} ${url}`);
  return j;
}

function tileName(gx, gy) { return gx.toString(16).padStart(4, '0') + gy.toString(16).padStart(4, '0') + '.tdf'; }

// ---- client tile cache (bounded LRU; CAM-C3 identity discipline) ----
function cachePut(tile, identity) {
  const key = `${tile.gridX},${tile.gridY}`;
  if (state.cache.has(key)) state.cache.delete(key);
  state.cache.set(key, { tile, identity: { era: identity.era, container: identity.container, containerSha256: identity.containerSha256, entryName: tile.name } });
  state.cacheOrder.push(key);
  while (state.cacheOrder.length > CLIENT_CACHE_MAX) {
    const old = state.cacheOrder.shift();
    state.cache.delete(old);
  }
}
function cacheGet(gx, gy) {
  const key = `${gx},${gy}`;
  const e = state.cache.get(key);
  if (!e) return null;
  const id = state.status.identityOf;
  if (!id || e.identity.era !== id.era || e.identity.container !== id.container ||
      String(e.identity.containerSha256) !== String(id.containerSha256) || e.identity.entryName !== tileName(gx, gy)) {
    state.cache.delete(key); // controlled refusal — refetch from the original bytes
    return null;
  }
  return e.tile;
}

async function fetchTile(gx, gy) {
  const cached = cacheGet(gx, gy);
  if (cached) return cached;
  state.fetchCount++;
  const r = await fetch(`/api/world/tile/${gx}/${gy}`, { cache: 'no-store' });
  if (!r.ok) {
    const t = await r.text();
    let msg = `HTTP ${r.status}`;
    try { msg = JSON.parse(t).message || msg; } catch { /* raw */ }
    throw new Error(`${tileName(gx, gy)}: ${msg}`);
  }
  const buf = await r.arrayBuffer();
  if (buf.byteLength !== 2048) throw new Error(`${tileName(gx, gy)}: ${buf.byteLength} B != 2048 B`);
  const heights = new Uint16Array(buf);
  const prov = makeProvenance({
    era: r.headers.get('X-PE-Era') ?? 'PCG_9_3_5',
    container: r.headers.get('X-PE-Container') ?? 'Terrain/terrain.bnt',
    entry: r.headers.get('X-PE-Entry') ?? tileName(gx, gy),
    physicalSource: r.url,
    offset: Number(r.headers.get('X-PE-Offset') ?? '0'),
    decoderVersion: r.headers.get('X-PE-Decoder-Version') ?? '',
    evidenceStatus: r.headers.get('X-PE-Evidence-Status') ?? 'CONFIRMED',
    extra: {
      containerSha256: r.headers.get('X-PE-Container-Sha256') ?? '',
      cacheState: r.headers.get('X-PE-Cache-State') ?? '',
      heightDataOffsetPayloadRelative: 64, rawUInt16NoNormalization: true,
    },
  });
  const tile = new TerrainTile({ gridX: gx, gridY: gy, name: tileName(gx, gy), heights, provenance: prov });
  cachePut(tile, {
    era: prov.era, container: prov.container,
    containerSha256: r.headers.get('X-PE-Container-Sha256') ?? '',
  });
  return tile;
}

// ---- ETAP D: the material->texture chain (client side; gen-gated §3.1) ----

function textureRgbaGet(id, identity) {
  const e = state.textureRgbaCache.get(id);
  if (!e) return null;
  if (e.identity.era !== identity.era || e.identity.container !== identity.container ||
      String(e.identity.containerSha256) !== String(identity.containerSha256)) {
    state.textureRgbaCache.delete(id);
    return null;
  }
  state.textureRgbaCache.delete(id);
  state.textureRgbaCache.set(id, e);
  return e;
}
function textureRgbaPut(id, identity, decoded) {
  if (state.textureRgbaCache.has(id)) state.textureRgbaCache.delete(id);
  state.textureRgbaCache.set(id, { rgba: decoded.rgba, width: decoded.width, height: decoded.height, identity });
  state.textureRgbaOrder.push(id);
  while (state.textureRgbaOrder.length > TEXTURE_CACHE_MAX) {
    const old = state.textureRgbaOrder.shift();
    state.textureRgbaCache.delete(old);
  }
}

async function fetchMaterialsGrid(origin) {
  const grid = [];
  for (let dy = 0; dy < WINDOW_T; dy++) {
    const row = [];
    for (let dx = 0; dx < WINDOW_T; dx++) row.push(null);
    grid.push(row);
  }
  const wanted = [];
  for (let dy = 0; dy < WINDOW_T; dy++) for (let dx = 0; dx < WINDOW_T; dx++) wanted.push([origin.gx + dx, origin.gy + dy]);
  for (let i = 0; i < wanted.length; i += 8) {
    const chunk = wanted.slice(i, i + 8);
    const results = await Promise.all(chunk.map(async ([gx, gy]) => {
      try {
        state.mat.materialsFetches++;
        return { tile: await fetchJson(`/api/world/tile/${gx}/${gy}/materials`) };
      } catch (e) {
        state.mat.materialsErrors++;
        state.lastError = String(e.message);
        return { err: e };
      }
    }));
    for (let k = 0; k < chunk.length; k++) {
      const [gx, gy] = chunk[k];
      const r = results[k];
      grid[gy - origin.gy][gx - origin.gx] = r.err ? null : r.tile;
    }
  }
  return grid;
}

async function fetchTextureDecoded(id) {
  const liveIdentity = {
    era: 'PCG_9_3_5',
    container: 'Textures.bnt',
    containerSha256: state.status?.containers?.textures?.sha256 ?? '',
  };
  const cached = textureRgbaGet(id, liveIdentity);
  if (cached) return cached;
  state.mat.textureFetches++;
  const r = await fetch(`/api/world/texture/${id}`, { cache: 'no-store' });
  if (!r.ok) {
    const t = await r.text();
    let msg = `HTTP ${r.status}`;
    try { msg = JSON.parse(t).message || msg; } catch { /* raw */ }
    throw new Error(`tekstura ${id}.dat: ${msg}`);
  }
  const hdr = {
    era: r.headers.get('X-PE-Era'),
    container: r.headers.get('X-PE-Container'),
    containerSha256: r.headers.get('X-PE-Container-Sha256'),
    payloadSha256: r.headers.get('X-PE-Payload-Sha256'),
  };
  if (hdr.era !== liveIdentity.era || hdr.container !== liveIdentity.container ||
      String(hdr.containerSha256 ?? '').toUpperCase() !== String(liveIdentity.containerSha256 ?? '').toUpperCase()) {
    throw new Error(`tekstura ${id}.dat: tożsamość kontenera z odpowiedzi nie zgadza się z live statusem — kontrolowana odmowa`);
  }
  const buf = new Uint8Array(await r.arrayBuffer());
  const decoded = decodeTga2(buf); // LOUD on anything outside the confirmed terrain subset
  if (decoded.width !== 256 || decoded.height !== 256) {
    throw new Error(`tekstura ${id}.dat: ${decoded.width}x${decoded.height} != 256x256 (spoza zbioru tekstur terenu — warstwa pominięta, jawnie)`);
  }
  const entry = { rgba: decoded.rgba, width: decoded.width, height: decoded.height, identity: { ...liveIdentity }, payloadSha256: hdr.payloadSha256 };
  textureRgbaPut(id, liveIdentity, decoded);
  return entry;
}

const SPLAT_VERT = /* glsl */`
varying vec3 vWorldPos;
void main() {
  vec4 wp = modelMatrix * vec4(position, 1.0);
  vWorldPos = wp.xyz;
  gl_Position = projectionMatrix * viewMatrix * wp;
}
`;
const SPLAT_FRAG = /* glsl */`
precision highp float;
precision highp sampler2DArray;
uniform sampler2DArray uMats;
uniform sampler2D uIdx0; uniform sampler2D uIdx1; uniform sampler2D uIdx2; uniform sampler2D uIdx3;
uniform sampler2D uW0;   uniform sampler2D uW1;   uniform sampler2D uW2;   uniform sampler2D uW3;
uniform float uUVRepeatM;
uniform vec2 uRegionOriginM;
varying vec3 vWorldPos;
void main() {
  vec2 cellF = (vWorldPos.xz - uRegionOriginM) / ${MATERIAL_CELL_M.toFixed(1)};
  ivec2 cell = ivec2(clamp(int(cellF.x), 0, ${REGION_CELLS - 1}), clamp(int(cellF.y), 0, ${REGION_CELLS - 1}));
  vec2 uv = vWorldPos.xz / uUVRepeatM; // GLOBAL world uv (no per-tile reset)
  vec4 i0 = texelFetch(uIdx0, cell, 0); vec4 i1 = texelFetch(uIdx1, cell, 0);
  vec4 i2 = texelFetch(uIdx2, cell, 0); vec4 i3 = texelFetch(uIdx3, cell, 0);
  vec4 w0 = texelFetch(uW0, cell, 0);   vec4 w1 = texelFetch(uW1, cell, 0);
  vec4 w2 = texelFetch(uW2, cell, 0);   vec4 w3 = texelFetch(uW3, cell, 0);
  vec4 s0 = floor(i0 * 255.0 + 0.5); vec4 s1 = floor(i1 * 255.0 + 0.5);
  vec4 s2 = floor(i2 * 255.0 + 0.5); vec4 s3 = floor(i3 * 255.0 + 0.5);
  vec3 col = vec3(0.0);
  bool any = false;
  if (w0.x > 0.0 && s0.x < 254.5) { col = mix(col, texture(uMats, vec3(uv, s0.x)).rgb, w0.x); any = true; }
  if (w0.y > 0.0 && s0.y < 254.5) { col = mix(col, texture(uMats, vec3(uv, s0.y)).rgb, w0.y); any = true; }
  if (w0.z > 0.0 && s0.z < 254.5) { col = mix(col, texture(uMats, vec3(uv, s0.z)).rgb, w0.z); any = true; }
  if (w0.w > 0.0 && s0.w < 254.5) { col = mix(col, texture(uMats, vec3(uv, s0.w)).rgb, w0.w); any = true; }
  if (w1.x > 0.0 && s1.x < 254.5) { col = mix(col, texture(uMats, vec3(uv, s1.x)).rgb, w1.x); any = true; }
  if (w1.y > 0.0 && s1.y < 254.5) { col = mix(col, texture(uMats, vec3(uv, s1.y)).rgb, w1.y); any = true; }
  if (w1.z > 0.0 && s1.z < 254.5) { col = mix(col, texture(uMats, vec3(uv, s1.z)).rgb, w1.z); any = true; }
  if (w1.w > 0.0 && s1.w < 254.5) { col = mix(col, texture(uMats, vec3(uv, s1.w)).rgb, w1.w); any = true; }
  if (w2.x > 0.0 && s2.x < 254.5) { col = mix(col, texture(uMats, vec3(uv, s2.x)).rgb, w2.x); any = true; }
  if (w2.y > 0.0 && s2.y < 254.5) { col = mix(col, texture(uMats, vec3(uv, s2.y)).rgb, w2.y); any = true; }
  if (w2.z > 0.0 && s2.z < 254.5) { col = mix(col, texture(uMats, vec3(uv, s2.z)).rgb, w2.z); any = true; }
  if (w2.w > 0.0 && s2.w < 254.5) { col = mix(col, texture(uMats, vec3(uv, s2.w)).rgb, w2.w); any = true; }
  if (w3.x > 0.0 && s3.x < 254.5) { col = mix(col, texture(uMats, vec3(uv, s3.x)).rgb, w3.x); any = true; }
  if (w3.y > 0.0 && s3.y < 254.5) { col = mix(col, texture(uMats, vec3(uv, s3.y)).rgb, w3.y); any = true; }
  if (w3.z > 0.0 && s3.z < 254.5) { col = mix(col, texture(uMats, vec3(uv, s3.z)).rgb, w3.z); any = true; }
  if (w3.w > 0.0 && s3.w < 254.5) { col = mix(col, texture(uMats, vec3(uv, s3.w)).rgb, w3.w); any = true; }
  if (!any) { gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0); return; } // no active layers in this cell (counted; honest void, NOT a fallback color)
  gl_FragColor = vec4(col, 1.0); // SRGB_PASSTHROUGH — no output colorspace chunk (documented preset)
}
`;

function disposeSplat() {
  if (!state.splat) return;
  try {
    state.splat.material.dispose();
    state.splat.arrayTexture.dispose();
    for (const t of state.splat.idxTex) t.dispose();
    for (const t of state.splat.wTex) t.dispose();
  } catch { /* disposal best-effort; resources are dropped from state below */ }
  state.splat = null;
}

/** Build + apply the textured terrain material for the window (§3.1: the
 *  generation gate — a STALE result never applies; the fetched-but-unapplied
 *  GPU resources of an aborted build are disposed, never leaked into the
 *  newer scene). */
async function applyTexturesForWindow(origin, requestId) {
  if (!state.texturesOn) return null;
  state.mat.busy = true;
  let builtSplat = null; // owned here until committed
  try {
    const stale = () => state.sceneRequest?.id !== requestId;
    const t0 = performance.now();
    let grid = state.materialsByOrigin.get(`${origin.gx},${origin.gy}`);
    if (!grid) {
      grid = await fetchMaterialsGrid(origin);
      if (stale()) return { aborted: true };
      state.materialsByOrigin.set(`${origin.gx},${origin.gy}`, grid);
      while (state.materialsByOrigin.size > 2) {
        const first = state.materialsByOrigin.keys().next().value;
        if (first === `${origin.gx},${origin.gy}`) break;
        state.materialsByOrigin.delete(first);
      }
    }
    const failedTiles = [];
    for (let dy = 0; dy < WINDOW_T; dy++) for (let dx = 0; dx < WINDOW_T; dx++) {
      if (!grid[dy][dx]) failedTiles.push(tileName(origin.gx + dx, origin.gy + dy));
    }
    if (failedTiles.length === WINDOW_T * WINDOW_T) {
      throw new Error(`pobranie materiałów nie udało się dla CAŁEGO okna (${failedTiles.length} kafli) — teren zostaje z paletą wysokości (uczciwie; bez fałszywych tekstur)`);
    }
    const safeGrid = grid.map((row, dy) => row.map((m, dx) => m ?? {
      ok: false, materials: [], fetchFailedTile: tileName(origin.gx + dx, origin.gy + dy),
      _failed: true,
    }));
    const data = buildRegionSplatData(safeGrid);
    const texRgba = new Array(data.textureIds.length);
    const decodeFailures = [];
    for (let i = 0; i < data.textureIds.length; i += 4) {
      const ids = data.textureIds.slice(i, i + 4);
      const res = await Promise.all(ids.map(async (id) => {
        try { return await fetchTextureDecoded(id); }
        catch (e) { state.mat.textureErrors++; decodeFailures.push({ id, error: String(e.message) }); return null; }
      }));
      for (let k = 0; k < ids.length; k++) texRgba[i + k] = res[k];
    }
    if (stale()) return { aborted: true };
    const failedIdSet = new Set(decodeFailures.map((f) => f.id));
    let splatData = data;
    if (failedIdSet.size > 0) {
      const markedGrid = safeGrid.map((row) => row.map((tilePayload) => ({
        ...tilePayload,
        materials: (tilePayload.materials ?? []).map((m) => (
          failedIdSet.has(m.id) ? { ...m, texture: { resolved: false, reason: `DECODE/FETCH FAILED for ${m.id}.dat — layer skipped (diagnostic; no fallback)` } } : m
        )),
      })));
      splatData = buildRegionSplatData(markedGrid);
    }
    const usable = splatData.textureIds.filter((id) => !failedIdSet.has(id));
    if (usable.length === 0) {
      throw new Error(`ŻADNA tekstura okna nie zdekodowała się (${decodeFailures.length} błędów) — teren zostaje z paletą wysokości (uczciwie; bez fałszywych tekstur)`);
    }
    const rgbaById = new Map();
    data.textureIds.forEach((id, i) => rgbaById.set(id, texRgba[i]));
    const depth = usable.length;
    const arrayData = new Uint8Array(256 * 256 * 4 * depth);
    let o = 0;
    for (const id of usable) {
      const rgba = rgbaById.get(id).rgba;
      arrayData.set(rgba, o); o += rgba.byteLength;
    }
    const arrayTexture = new THREE.DataArrayTexture(arrayData, 256, 256, depth);
    arrayTexture.format = THREE.RGBAFormat;
    arrayTexture.type = THREE.UnsignedByteType;
    arrayTexture.magFilter = THREE.LinearFilter;
    arrayTexture.minFilter = THREE.LinearFilter;
    arrayTexture.wrapS = THREE.RepeatWrapping;
    arrayTexture.wrapT = THREE.RepeatWrapping;
    arrayTexture.colorSpace = THREE.NoColorSpace; // SRGB_PASSTHROUGH preset (documented)
    arrayTexture.needsUpdate = true;
    const mkCell = (arr) => {
      const t = new THREE.DataTexture(arr, REGION_CELLS, REGION_CELLS, THREE.RGBAFormat, THREE.UnsignedByteType);
      t.magFilter = THREE.NearestFilter;
      t.minFilter = THREE.NearestFilter;
      t.generateMipmaps = false;
      t.colorSpace = THREE.NoColorSpace;
      t.needsUpdate = true;
      return t;
    };
    const idxTex = splatData.idxTextures.map(mkCell);
    const wTex = splatData.wTextures.map(mkCell);
    const material = new THREE.ShaderMaterial({
      uniforms: {
        uMats: { value: arrayTexture },
        uIdx0: { value: idxTex[0] }, uIdx1: { value: idxTex[1] }, uIdx2: { value: idxTex[2] }, uIdx3: { value: idxTex[3] },
        uW0: { value: wTex[0] }, uW1: { value: wTex[1] }, uW2: { value: wTex[2] }, uW3: { value: wTex[3] },
        uUVRepeatM: { value: UV_REPEAT_M },
        uRegionOriginM: { value: new THREE.Vector2(origin.gx * TILE_M, origin.gy * TILE_M) },
      },
      vertexShader: SPLAT_VERT,
      fragmentShader: SPLAT_FRAG,
      side: THREE.DoubleSide,
    });
    material.wireframe = $('tog-wireframe').checked;
    builtSplat = { material, arrayTexture, idxTex, wTex, data: splatData, origin, textureIds: usable, decodeFailures, failedTiles };
    if (stale()) {
      // ABORT: dispose the fetched-but-unapplied GPU resources (never leak into the newer scene)
      material.dispose(); arrayTexture.dispose();
      for (const t of idxTex) t.dispose();
      for (const t of wTex) t.dispose();
      return { aborted: true };
    }
    disposeSplat(); // the previous window's resources (owned by the state, disposed HERE — not by a stale instance)
    state.splat = builtSplat;
    state.coherence.splat = origin; // §3.1: the texture chain now matches THIS request's window
    applyTerrainMaterial();
    state.mat.lastDiag = {
      ok: splatData.diagnostic.mode === 'NONE' && failedTiles.length === 0,
      elapsedMs: Math.round(performance.now() - t0),
      textureCount: usable.length,
      layersTotal: splatData.layersTotal,
      resolvedLayers: splatData.resolvedLayers,
      appliedLayers: splatData.appliedLayers,
      resolved: splatData.resolvedLayers,
      decoded: usable.length,
      applied: splatData.appliedLayers,
      unresolvedBindings: splatData.unresolved,
      decodeFailures,
      failedMaterialsTiles: failedTiles,
      duplicates: splatData.duplicates,
      cappedCells: splatData.cappedCells,
      cellsWithNoActiveLayers: splatData.cellsWithNoActiveLayers,
      activeLayersHist: splatData.activeLayersHist,
      schemaVersion: WORLD_SPLAT_SCHEMA_VERSION,
      preset: RENDER_RECONSTRUCTION_PRESET,
    };
    return state.mat.lastDiag;
  } catch (e) {
    state.mat.lastDiag = { ok: false, error: String(e?.message ?? e), unresolvedBindings: [], decodeFailures: [] };
    if (state.texturesOn && state.sceneRequest?.id === requestId) {
      banner(`TEKSTURY TERENU: BŁĄD — ${e.message}. Teren renderowany paletą wysokości (bez fałszywych tekstur).`);
    }
    return state.mat.lastDiag;
  } finally {
    state.mat.busy = false;
  }
}

function applyTerrainMaterial() {
  if (!state.mesh) return;
  const wantSplat = state.texturesOn && state.splat && state.splat.origin.gx === state.windowOrigin?.gx && state.splat.origin.gy === state.windowOrigin?.gy;
  const target = wantSplat ? state.splat.material : state.paletteMaterial;
  if (state.mesh.material !== target) {
    state.mesh.material = target;
    state.mesh.material.wireframe = $('tog-wireframe').checked;
  }
}

// ---- the vegetation subsystem (contract §6) ----

async function fetchVegBinary(url, { container, containerSha256 }) {
  const r = await fetch(url, { cache: 'no-store' });
  if (!r.ok) {
    const t = await r.text();
    let msg = `HTTP ${r.status}`;
    try { msg = JSON.parse(t).message || msg; } catch { /* raw */ }
    throw new Error(`${url}: ${msg}`);
  }
  const hdr = {
    era: r.headers.get('X-PE-Era'),
    container: r.headers.get('X-PE-Container'),
    containerSha256: r.headers.get('X-PE-Container-Sha256'),
    entryName: r.headers.get('X-PE-Entry'),
    payloadSha256: r.headers.get('X-PE-Payload-Sha256'),
  };
  if (hdr.era !== state.status.era || hdr.container !== container ||
      String(hdr.containerSha256 ?? '').toUpperCase() !== String(containerSha256 ?? '').toUpperCase()) {
    throw new Error(`${url}: tożsamość kontenera z odpowiedzi nie zgadza się z live statusem — kontrolowana odmowa`);
  }
  const payload = new Uint8Array(await r.arrayBuffer());
  return { payload, headers: hdr };
}

async function rebuildVegetation(origin, requestId, { awaited = false } = {}) {
  // P1-2 diagnostics: a bounded read-only event ring (never a behavior input;
  // defensive in non-browser harness contexts — a missing vegTrace is fine)
  const trace = (event, extra = {}) => {
    if (!Array.isArray(state.vegTrace)) return;
    const t = (typeof performance !== 'undefined' && performance.now) ? Math.round(performance.now()) : Date.now();
    state.vegTrace.push({ t, event, origin: { gx: origin.gx, gy: origin.gy }, requestId, ...extra });
    if (state.vegTrace.length > 48) state.vegTrace.splice(0, state.vegTrace.length - 48);
  };
  if (!state.vegOn || !state.veg) { state.vegCensus = state.veg ? state.veg.lastCensus : null; return null; }
  // P1-2 FIX (production wiring; correction round 2026-10-10): a newer request
  // arriving while a veg rebuild is BUSY is STORED at the WRAPPER level
  // (latest-wins — the slot is overwritten by newer requests) and DELIVERED
  // to the WorldVegetation class by the drain loop below. The busy path no
  // longer drops the newest request, and the WINNING census is committed back
  // to state.vegCensus/state.coherence.veg gen-gated vs requestId. The
  // class-internal pendingRequest queue (WL-1) remains as a second safety
  // layer for direct rebuild() callers; in the production path the wrapper
  // delivers requests SERIALLY, so the class queue is not engaged.
  trace(state.vegBusy ? 'request-stored-pending (busy)' : 'request-take (idle)');
  state.vegPending = { origin, requestId };
  if (state.vegBusy) return null; // the running drain loop delivers the newest pending when the current build finishes
  state.vegBusy = true;
  let lastCensus = null;
  let lastReq = null;
  try {
    for (;;) {
      const req = state.vegPending;
      state.vegPending = null;
      if (!req) break; // no newer request — the wrapper queue is drained
      // DEDUPE (the requestScene analogue): a repeat of the request JUST run
      // (same origin + same request id = the same scene identity incl. the
      // veg config — config changes bump the id via forceNew) is already
      // served by that build; re-running it is pointless.
      if (lastReq && req.origin.gx === lastReq.origin.gx && req.origin.gy === lastReq.origin.gy && req.requestId === lastReq.requestId) {
        trace('drain-deduped-repeat', { pendingOrigin: req.origin, pendingRequestId: req.requestId });
        break;
      }
      trace('drain-run', { runOrigin: req.origin, runRequestId: req.requestId });
      const c = await state.veg.rebuild(req.origin, WINDOW_T);
      lastReq = req;
      lastCensus = c;
      trace('class-rebuild-returned', { runOrigin: req.origin, runRequestId: req.requestId, censusOrigin: c?.window?.origin ?? null, aborted: !!(c && c.aborted) });
      if (c && !c.aborted && state.sceneRequest?.id === req.requestId) {
        state.vegCensus = c; // the WINNING census propagates (gen-gated vs requestId)
        state.coherence.veg = c.ok ? c.window.origin : null;
        trace('census-committed (current scene)', { runOrigin: req.origin, runRequestId: req.requestId, censusOrigin: c.window.origin });
        if (!c.ok && !c.unsupportedProfile) {
          banner(`ROŚLINNOŚĆ: ${c.error ?? 'błąd łańcucha'} — podgląd roślinności niedostępny dla tej konfiguracji (teren działa); wybierz profil zdekodowany.`);
        }
        updateVegPanel();
        updateEvidencePanel();
      } else {
        trace('census-not-committed (stale or aborted)', { runOrigin: req.origin, runRequestId: req.requestId, censusOrigin: c?.window?.origin ?? null, sceneIdNow: state.sceneRequest?.id ?? null });
      }
      // a STALE census (sceneRequest moved on) is NOT committed — the newer
      // scene's own veg request (queued or arriving) owns the commit
    }
  } finally {
    state.vegBusy = false;
    trace('drain-done (wrapper idle)');
  }
  return lastCensus;
}

// ---- window management (streaming; the FOCUS-following near window) ----

/** §5/WL-4: streaming follows the VIEWED FOCUS (orbit: controls.target;
 *  fly/walk: the camera position) with the near window kept centered on it. */
function focusPoint() {
  return state.mode === 'orbit' && controls ? controls.target : camera.position;
}
function desiredOrigin(focusGx, focusGy) {
  return {
    gx: Math.min(Math.max(focusGx - (WINDOW_T >> 1), 0), GRID_W - WINDOW_T),
    gy: Math.min(Math.max(focusGy - (WINDOW_T >> 1), 0), GRID_H - WINDOW_T),
  };
}
function focusTile() {
  const p = focusPoint();
  return {
    gx: Math.min(Math.max(Math.floor(p.x / TILE_M), 0), GRID_W - 1),
    gy: Math.min(Math.max(Math.floor(p.z / TILE_M), 0), GRID_H - 1),
  };
}

function setLoading(msg) { $('world-loading').textContent = msg; }

/** §3.1: the explicit scene request identity + the latest-wins terrain queue.
 *  DEDUPE: while a rebuild is RUNNING (or queued) for the SAME origin, a
 *  repeated identical request does NOT invalidate it (the streaming tick fires
 *  every ~400 ms; without this the in-flight rebuild would be perpetually
 *  superseded — measured in this run's own browser probe). A request for a
 *  DIFFERENT origin, or an explicit forceNew (a CONFIG change: profile/seed/
 *  density are part of the scene identity), bumps the sequence — the stale
 *  build aborts before applying and the newest runs. */
function requestScene(origin, { forceNew = false } = {}) {
  const runningSame = state.rebuildBusy && state.runningOrigin &&
    state.runningOrigin.gx === origin.gx && state.runningOrigin.gy === origin.gy;
  const pendingSame = state.pendingOrigin &&
    state.pendingOrigin.gx === origin.gx && state.pendingOrigin.gy === origin.gy;
  if ((runningSame || pendingSame) && !forceNew) {
    return state.sceneRequest?.id ?? state.sceneSeq; // already building/queued for THIS origin
  }
  const id = ++state.sceneSeq;
  state.sceneRequest = {
    id,
    origin,
    era: state.status?.era ?? 'PCG_9_3_5',
    containers: state.status?.containers ?? null,
    profileMode: state.vegConfig.profileMode,
    profile: state.vegConfig.profile,
    labSeed: state.vegConfig.labSeed,
    density: state.vegConfig.densityPercent,
    calibration: state.status?.calibration ?? null,
    versions: {
      heightQuery: 'peheight-query-triangle-v1', vegetation: VEGETATION_SCHEMA_VERSION,
      splat: WORLD_SPLAT_SCHEMA_VERSION, lod: WORLD_LOD_VERSION,
    },
  };
  state.readyShown = false;
  if (state.rebuildBusy) {
    state.pendingOrigin = origin; // latest wins (the slot is overwritten by newer requests)
  } else {
    void rebuildWindow(origin, id);
  }
  return id;
}

/** Fetch the window tiles + the 1-tile REAL-sample halo (§3.2) with bounded
 *  concurrency. Returns { field (10x10, nulls on failure), windowFailed } . */
async function fetchFieldTiles(origin) {
  const field = [];
  const wanted = [];
  for (let dy = 0; dy < FIELD_T; dy++) {
    const row = [];
    for (let dx = 0; dx < FIELD_T; dx++) row.push(null);
    field.push(row);
    for (let dx = 0; dx < FIELD_T; dx++) {
      const gx = origin.gx - HALO_T + dx, gy = origin.gy - HALO_T + dy;
      if (gx >= 0 && gy >= 0 && gx < GRID_W && gy < GRID_H) wanted.push([gx, gy, dx, dy]);
    }
  }
  let done = 0, failed = 0;
  for (let i = 0; i < wanted.length; i += 8) {
    const chunk = wanted.slice(i, i + 8);
    const results = await Promise.all(chunk.map(async ([gx, gy]) => {
      try { return { tile: await fetchTile(gx, gy) }; }
      catch (e) { state.fetchErrors++; state.lastError = String(e.message); return { err: e, gx, gy }; }
    }));
    for (let k = 0; k < chunk.length; k++) {
      const [gx, gy, dx, dy] = chunk[k];
      const r = results[k];
      if (r.err) { failed++; }
      else field[dy][dx] = r.tile;
      done++;
    }
    if (failed > 0) setLoading(`okno + halo: ${done}/${wanted.length} pobranych, BŁĘDY: ${failed} (NODATA/odmowa — UCZCIWIE)`);
  }
  return { field, failed };
}

async function rebuildWindow(origin, requestId, { isInitial = false } = {}) {
  state.rebuildBusy = true;
  state.runningOrigin = origin; // the requestScene dedupe key (this build's target)
  try {
    const stale = () => state.sceneRequest?.id !== requestId;
    const { field, failed } = await fetchFieldTiles(origin);
    if (stale()) return; // the newer request owns the scene now — nothing applied
    // the inner 8x8 render window must be fully present (missing inner tile = no mesh over void)
    const innerMissing = [];
    for (let dy = HALO_T; dy < HALO_T + WINDOW_T; dy++) {
      for (let dx = HALO_T; dx < HALO_T + WINDOW_T; dx++) {
        if (!field[dy][dx]) innerMissing.push(tileName(origin.gx + (dx - HALO_T), origin.gy + (dy - HALO_T)));
      }
    }
    if (innerMissing.length > 0) {
      state.boundaryHit = true;
      state.boundaryReason = 'LOADING';
      $('boundary-banner').hidden = false;
      if (isInitial) {
        setLoadStatus(`ERROR_TERRAIN_LOAD: ${innerMissing.length} kafli okna niedostępne — ${state.lastError}`);
        banner(`BŁĄD ŁADOWANIA TERENU: ${state.lastError}`);
      }
      return; // keep the previous coherent scene (never a mesh over void)
    }
    // THE SHARED HEIGHT FIELD (10x10 with the real-sample halo; missing halo
    // tiles are explicit nulls — the query refuses to cross them)
    const heightField = new PEHeightField(field, { tileWorldMeters: TILE_M });
    // the RENDER window (8x8 — the production PETerrainRegion path)
    const rows = [];
    for (let dy = 0; dy < WINDOW_T; dy++) {
      const row = [];
      for (let dx = 0; dx < WINDOW_T; dx++) row.push(field[dy + HALO_T][dx + HALO_T]);
      rows.push(row);
    }
    const region = new PETerrainRegion(rows);
    const geo = region.buildGeometry();
    state.lastGeo = geo;
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(geo.positions, 3));
    g.setAttribute('color', new THREE.BufferAttribute(paletteColors(geo.positions), 3));
    g.setIndex(new THREE.BufferAttribute(geo.indices, 1));
    g.computeVertexNormals();
    if (state.mesh) {
      state.mesh.geometry.dispose();
      state.mesh.geometry = g;
      state.mesh.position.set(origin.gx * TILE_M, 0, origin.gy * TILE_M);
    } else {
      state.mesh = new THREE.Mesh(g, state.paletteMaterial);
      state.mesh.position.set(origin.gx * TILE_M, 0, origin.gy * TILE_M);
      scene.add(state.mesh);
    }
    applyTerrainMaterial();
    state.mesh.material.wireframe = $('tog-wireframe').checked;
    buildTileBounds(region, geo, origin);
    state.region = region;
    state.heightField = heightField;
    state.windowOrigin = origin;
    state.coherence.terrain = origin;
    state.rebuilds++;
    state.boundaryHit = false;
    state.boundaryReason = null;
    $('boundary-banner').hidden = true;
    setLoading(`teren: okno 8×8 (64 kafle) + halo 10×10 przy origin ${origin.gx},${origin.gy} — z SUROWYCH próbek u16; przebudowań: ${state.rebuilds}`);
    if (isInitial && !state.firstFrameDone) {
      hud(`teren gotowy — ${geo.positions.length / 3} wierzchołków z surowych u16; tryb: ORBITA (1/2/3 zmienia tryb); F dopasuj, R reset`);
    }
    // the distant LOD follows (mid ring + far hole; NOT gen-critical — the LOD
    // is window-derived and idempotent; a late mid rebuild is harmless)
    void state.lod?.rebuildMid(origin).then(() => { updateCensusPanel(); });
    // textures + vegetation for THIS request (gen-gated; latest wins)
    if (state.texturesOn) void applyTexturesForWindow(origin, requestId);
    if (!isInitial) void rebuildVegetation(origin, requestId);
    updateCensusPanel();
  } finally {
    state.rebuildBusy = false;
    state.runningOrigin = null;
    if (state.pendingOrigin) {
      const next = state.pendingOrigin;
      state.pendingOrigin = null;
      if (next.gx !== state.windowOrigin?.gx || next.gy !== state.windowOrigin?.gy) {
        const id = state.sceneRequest?.id; // the request id is already the newest (requestScene bumped it)
        void rebuildWindow(next, id);
      }
    }
  }
}

// height-preview palette (RECONSTRUCTION_PREVIEW visualization; raw heights untouched)
const STOPS = [[0.00, 14, 34, 56], [0.35, 30, 95, 79], [0.55, 107, 122, 69], [0.75, 138, 122, 95], [1.00, 232, 228, 216]];
function paletteColors(positions) {
  const n = positions.length / 3;
  const colors = new Float32Array(n * 3);
  let mn = Infinity, mx = -Infinity;
  for (let i = 0; i < n; i++) { const y = positions[i * 3 + 1]; if (y < mn) mn = y; if (y > mx) mx = y; }
  const span = (mx > mn) ? (mx - mn) : 1;
  for (let i = 0; i < n; i++) {
    const t = (positions[i * 3 + 1] - mn) / span;
    let r = 0, g = 0, b = 0;
    for (let s = 1; s < STOPS.length; s++) {
      if (t <= STOPS[s][0] || s === STOPS.length - 1) {
        const [t0, r0, g0, b0] = STOPS[s - 1];
        const [t1, r1, g1, b1] = STOPS[s];
        const f = Math.min(1, Math.max(0, (t - t0) / (t1 - t0)));
        r = (r0 + f * (r1 - r0)) / 255; g = (g0 + f * (g1 - g0)) / 255; b = (b0 + f * (b1 - b0)) / 255;
        break;
      }
    }
    colors[i * 3] = r; colors[i * 3 + 1] = g; colors[i * 3 + 2] = b;
  }
  return colors;
}

function buildTileBounds(region, geo, origin) {
  if (state.boundsLines) {
    state.boundsLines.geometry.dispose();
    scene.remove(state.boundsLines);
    state.boundsLines = null;
  }
  if (!$('tog-tilebounds').checked) return;
  const sx = geo.sampleGridX, sy = geo.sampleGridY, P = geo.positions;
  const verts = [];
  const push = (i) => verts.push(P[i * 3], P[i * 3 + 1], P[i * 3 + 2]);
  for (let vy = 0; vy < sy; vy++) {
    for (let vx = 0; vx < sx; vx++) {
      const i = vy * sx + vx;
      if (vx % 32 === 0 && vx + 1 < sx) { push(i); push(i + 1); }
      if (vy % 32 === 0 && vy + 1 < sy) { push(i); push(i + sx); }
    }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(verts), 3));
  state.boundsLines = new THREE.LineSegments(g, new THREE.LineBasicMaterial({ color: 0xff9a2e, transparent: true, opacity: 0.55 }));
  state.boundsLines.position.set(origin.gx * TILE_M, 0, origin.gy * TILE_M);
  scene.add(state.boundsLines);
}

// ---- three.js core (§5: the reference camera preset) ----
const canvas = $('view-canvas');
let renderer, scene, camera, controls, pointerLockFailed = false;
try {
  // §5: near 0.5 + logarithmicDepthBuffer with far 200000 — the justified
  // world-scale depth choice (close-up trees AND 14 km distant LOD in one
  // frustum without z-collapse; a renderer choice, never a PE unit claim)
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true, logarithmicDepthBuffer: true });
} catch (e) {
  setLoadStatus(`ERROR_WEBGL: ${e.message}`);
  banner(`WebGL niedostępny: ${e.message}`);
  throw e;
}
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
scene = new THREE.Scene();
scene.background = new THREE.Color(0x0c1018);
camera = new THREE.PerspectiveCamera(45, 1, 0.5, 200000); // §5 the live 9350 reference preset (FOV 45, far 200000)
camera.position.set(0, 200, 0);
const sun = new THREE.DirectionalLight(0xffffff, 1.25);
sun.position.set(0.35, 1.0, 0.2);
scene.add(sun);
scene.add(new THREE.AmbientLight(0x707890, 1.1));
controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.dampingFactor = 0.08;   // §5 the reference damping
controls.minDistance = 10;       // §5 the reference limit
controls.maxDistance = 50000;    // §5 the reference limit
state.paletteMaterial = new THREE.MeshLambertMaterial({ vertexColors: true, side: THREE.DoubleSide });

function syncCanvasSize() {
  const w = canvas.clientWidth || 1, h = canvas.clientHeight || 1;
  renderer.setSize(w, h, false);
  camera.aspect = w / h;
  camera.updateProjectionMatrix(); // resize updates the drawing buffer/aspect — the camera POSITION is never reset
}
window.addEventListener('resize', syncCanvasSize);

// ---- exploration modes (§3.2: the movement guard; §5: no key capture from inputs) ----
const move = { keys: new Set(), yaw: 0, pitch: 0, dragging: false, lastX: 0, lastY: 0 };

function isTypingTarget(ev) {
  const t = ev.target;
  return t instanceof HTMLElement && (t.tagName === 'INPUT' || t.tagName === 'SELECT' || t.tagName === 'TEXTAREA' || t.isContentEditable);
}

function clearHeldKeys() { move.keys.clear(); } // §3.2: blur / lock loss / mode change
window.addEventListener('blur', clearHeldKeys);

function setMode(mode) {
  if (state.mode === mode) return;
  state.mode = mode;
  clearHeldKeys();
  for (const [id, m] of [['btn-mode-orbit', 'orbit'], ['btn-mode-fly', 'fly'], ['btn-mode-walk', 'walk']]) {
    $(id).classList.toggle('active', m === mode);
  }
  controls.enabled = mode === 'orbit';
  if (mode === 'orbit') {
    if (document.pointerLockElement === canvas) document.exitPointerLock();
    // keep the CURRENT focus: orbit pivots on the place you were looking at (no jump)
    const t = state._lastFlyFocus ?? { x: camera.position.x, z: camera.position.z };
    const g = state.heightField?.triangleHeightAtWorld(t.x, t.z);
    controls.target.set(t.x, g ?? Math.max(camera.position.y - 50, 0), t.z);
    $('lock-hint').hidden = true;
  } else {
    const e = new THREE.Euler().setFromQuaternion(camera.quaternion, 'YXZ');
    move.yaw = e.y; move.pitch = e.x;
    state._lastFlyFocus = { x: camera.position.x, z: camera.position.z };
    if (mode === 'walk') {
      const g = state.heightField?.triangleHeightAtWorld(camera.position.x, camera.position.z);
      if (g !== null && g !== undefined) camera.position.y = g + EYE_OFFSET_M; // snap to the shared surface on mode entry
    }
    $('lock-hint').hidden = false;
    tryPointerLock();
  }
}
function tryPointerLock() {
  try {
    const p = canvas.requestPointerLock();
    if (p && typeof p.catch === 'function') {
      p.catch(() => {
        pointerLockFailed = true;
        $('lock-hint').hidden = false;
        $('lock-hint').textContent = 'przechwycenie myszy odrzucone przez przeglądarkę — działa tryb przeciągania: trzymaj LPM na canvasie i ruszaj myszą (WASD bez zmian)';
      });
    }
  } catch {
    pointerLockFailed = true;
  }
}
canvas.addEventListener('click', () => {
  if (state.mode !== 'orbit' && document.pointerLockElement !== canvas && !pointerLockFailed) {
    tryPointerLock();
  } else if (state.mode !== 'orbit' && pointerLockFailed) {
    tryPointerLock(); // retry on the conscious click (the fallback drag-look stays available regardless)
  }
});
document.addEventListener('pointerlockchange', () => {
  const locked = document.pointerLockElement === canvas;
  if (!locked) clearHeldKeys(); // §3.2: lock loss clears held keys
  if (!locked && state.mode !== 'orbit' && !pointerLockFailed) {
    $('lock-hint').hidden = false;
    $('lock-hint').textContent = 'kursor uwolniony — kliknij canvas, aby ponownie przechwycić mysz; WASD wznowione po kliknięciu';
  }
});
// the drag-look fallback (works with OR without pointer lock; §3.2)
canvas.addEventListener('mousedown', (ev) => {
  if (state.mode === 'orbit') return;
  move.dragging = true; move.lastX = ev.clientX; move.lastY = ev.clientY;
});
window.addEventListener('mouseup', () => { move.dragging = false; });
document.addEventListener('mousemove', (ev) => {
  if (document.pointerLockElement === canvas) {
    move.yaw -= ev.movementX * 0.0022;
    move.pitch = Math.min(Math.max(move.pitch - ev.movementY * 0.0022, -1.5), 1.5);
    return;
  }
  if (move.dragging && state.mode !== 'orbit') { // the drag-look fallback path
    move.yaw -= (ev.clientX - move.lastX) * 0.0044;
    move.pitch = Math.min(Math.max(move.pitch - (ev.clientY - move.lastY) * 0.0044, -1.5), 1.5);
    move.lastX = ev.clientX; move.lastY = ev.clientY;
  }
});
window.addEventListener('keydown', (ev) => {
  if (isTypingTarget(ev)) return; // §5: the drawer inputs never capture movement keys
  if (ev.code === 'Digit1') setMode('orbit');
  else if (ev.code === 'Digit2') setMode('fly');
  else if (ev.code === 'Digit3') setMode('walk');
  else if (ev.code === 'KeyF') fitView();
  else if (ev.code === 'KeyR') resetView();
  else if (ev.code === 'Escape') { /* pointer lock exits automatically */ }
  else move.keys.add(ev.code);
  if (['KeyW', 'KeyA', 'KeyS', 'KeyD', 'KeyQ', 'KeyE', 'ShiftLeft', 'ShiftRight'].includes(ev.code)) ev.preventDefault?.();
});
window.addEventListener('keyup', (ev) => move.keys.delete(ev.code));

const MAP_MIN = 1, MAP_MAX_X = GRID_W * TILE_M - 1, MAP_MAX_Z = GRID_H * TILE_M - 1;
function clampToMap(v) {
  const out = { x: v.x, z: v.z, clamped: false };
  if (out.x < MAP_MIN) { out.x = MAP_MIN; out.clamped = true; }
  if (out.z < MAP_MIN) { out.z = MAP_MIN; out.clamped = true; }
  if (out.x > MAP_MAX_X) { out.x = MAP_MAX_X; out.clamped = true; }
  if (out.z > MAP_MAX_Z) { out.z = MAP_MAX_Z; out.clamped = true; }
  return out;
}

/** §3.2/WL-3 FIX: the candidate position is computed FIRST, the surface is
 *  checked, and ONLY THEN is X/Y/Z committed. No surface data = the move is
 *  REFUSED (the last safe position stands; never a void drop, never y=0). */
function updateFlyWalk(dt) {
  if (state.mode === 'orbit' || (document.pointerLockElement !== canvas && !move.dragging)) {
    if (state.mode !== 'orbit' && move.keys.size > 0 && document.pointerLockElement !== canvas && !move.dragging) {
      // no pointer lock AND no drag: WASD still works (the honest fallback input)
    }
  }
  if (state.mode === 'orbit') return;
  if (move.keys.size === 0 && !move.dragging) return;
  const speedBase = state.mode === 'walk' ? 12 : 60;
  const speed = speedBase * (move.keys.has('ShiftLeft') || move.keys.has('ShiftRight') ? 3 : 1);
  const dir = new THREE.Vector3();
  if (move.keys.has('KeyW')) dir.z -= 1;
  if (move.keys.has('KeyS')) dir.z += 1;
  if (move.keys.has('KeyA')) dir.x -= 1;
  if (move.keys.has('KeyD')) dir.x += 1;
  let up = 0;
  if (state.mode === 'fly') {
    if (move.keys.has('KeyE')) up += 1;
    if (move.keys.has('KeyQ')) up -= 1;
  }
  if (dir.lengthSq() === 0 && up === 0) return;
  const rot = new THREE.Euler(move.pitch, move.yaw, 0, 'YXZ');
  const step = dir.normalize().applyEuler(rot).multiplyScalar(speed * dt);
  // ---- the CANDIDATE position (nothing committed yet) ----
  const candidate = { x: camera.position.x + step.x, z: camera.position.z + step.z, y: camera.position.y };
  const c = clampToMap(candidate);
  if (state.mode === 'walk') {
    const g = state.heightField ? state.heightField.triangleHeightAtWorld(c.x, c.z) : null;
    if (g === null || g === undefined) {
      // NO REAL SURFACE DATA: the move is refused at the last safe position
      // (distinguish LOADING from the corpus edge honestly)
      state.boundaryHit = true;
      const atEdge = c.x <= MAP_MIN || c.z <= MAP_MIN || c.x >= MAP_MAX_X || c.z >= MAP_MAX_Z;
      state.boundaryReason = atEdge ? 'CORPUS_EDGE' : 'LOADING';
      $('boundary-banner').textContent = state.boundaryReason === 'CORPUS_EDGE'
        ? 'osiągnięto krawędź dostępnej mapy (regularnej siatki kafli) — ruch wstrzymany (to realna granica korpusu, nie błąd ładowania)'
        : 'dane powierzchni jeszcze się ładują (okno/halo w przebudowie) — ruch wstrzymany na ostatniej bezpiecznej pozycji; prefetch (streaming) już działa';
      $('boundary-banner').hidden = false;
      return; // NOTHING committed
    }
    candidate.y = g + EYE_OFFSET_M;
  } else {
    candidate.y = Math.min(Math.max(camera.position.y + up * speed * dt, 2), 8000);
  }
  // ---- the surface was checked: commit ----
  camera.position.set(c.x, candidate.y, c.z);
  camera.quaternion.setFromEuler(new THREE.Euler(move.pitch, move.yaw, 0, 'YXZ'));
  state._lastFlyFocus = { x: c.x, z: c.z };
  if (c.clamped) { state.boundaryHit = true; state.boundaryReason = 'CORPUS_EDGE'; $('boundary-banner').hidden = false; }
  else if (state.boundaryHit) { state.boundaryHit = false; state.boundaryReason = null; $('boundary-banner').hidden = true; }
}

/** §5/WL-4 FIX: fit frames the CURRENT FOCUS (the streaming follows the
 * focus — the window NEVER chases the fit). Stable across repetitions. */
function fitView() {
  const focus = focusPoint();
  const g = state.heightField?.triangleHeightAtWorld(focus.x, focus.z) ?? Math.max(focus.y - 50, 0);
  // frame the near window AROUND the focus (the reference autoFit direction 0.7/0.6/0.7; distance = extent*1.8)
  const extent = WINDOW_T * TILE_M; // the window around the focus
  const dist = extent * 1.8;
  const dirV = new THREE.Vector3(0.7, 0.6, 0.7).normalize();
  if (state.mode === 'orbit') {
    controls.target.set(focus.x, g, focus.z); // the focus is PRESERVED (no window move)
    camera.position.set(focus.x + dirV.x * dist, g + dirV.y * dist, focus.z + dirV.z * dist);
    controls.update();
  } else {
    const back = new THREE.Vector3(-dirV.x, 0, -dirV.z).normalize();
    camera.position.set(focus.x + back.x * 60, g + 160, focus.z + back.z * 60);
  }
  hud('widok dopasowany do fokusu (F) — okno streamingu podąża za fokusem, nie za kamerą (stabilne przy powtórzeniach)');
}
function resetView() {
  if (!state.spawn) return;
  const s = state.spawn;
  // the teleport rule (§3.2): ensure the DESTINATION data first — the window
  // request happens; the camera settles once the surface is available
  const g = state.heightField?.triangleHeightAtWorld(s.x, s.z);
  if (state.mode === 'orbit') {
    controls.target.set(s.x, g ?? Math.max(120, s.x * 0), s.z); // focus at spawn; height from the shared query (no y=0 fallback)
    const extent = WINDOW_T * TILE_M;
    const dist = extent * 1.8;
    const dirV = new THREE.Vector3(0.7, 0.6, 0.7).normalize();
    camera.position.set(s.x + dirV.x * dist, (g ?? 200) + dirV.y * dist, s.z + dirV.z * dist);
    controls.update();
  } else {
    camera.position.set(s.x, state.mode === 'walk' ? (g ?? 200) + EYE_OFFSET_M : (g ?? 200) + 120, s.z + 120);
  }
  hud('reset kamery na spawn (R) — focus na spawn; streaming podąża za fokusem');
}

// ---- teleport (§8 QC: distant regions + return) ----
function teleportTo(gx, gy) {
  const cx = gx * TILE_M + TILE_M / 2, cz = gy * TILE_M + TILE_M / 2;
  state.teleportCount++;
  // the window request FIRST (the destination data), then the camera settle
  const want = desiredOrigin(gx, gy);
  requestScene(want);
  if (state.mode === 'orbit') {
    controls.target.set(cx, 200, cz);
    camera.position.set(cx + 400, 620, cz + 400);
    controls.update();
  } else {
    camera.position.set(cx, 400, cz);
    state._lastFlyFocus = { x: cx, z: cz };
  }
  // settle the focus height once the surface is in (honest: no y=0)
  const settle = () => {
    const g = state.heightField?.triangleHeightAtWorld(cx, cz);
    if (g !== null && g !== undefined) {
      if (state.mode === 'orbit') { controls.target.y = g; controls.update(); }
      else if (state.mode === 'walk') camera.position.y = g + EYE_OFFSET_M;
    } else {
      setTimeout(settle, 250); // still loading — the focus stays where it is until real data
    }
  };
  settle();
  hud(`teleport → kafel ${gx},${gy} (najpierw dane miejsca docelowego; brak ground ≠ wysokość zero)`);
}

// ---- §7: the Rosetta debug point (click) ----
const raycaster = new THREE.Raycaster();
function debugPointFromClick(ev) {
  if (state.mode !== 'orbit') return; // selection in orbit only (movement owns fly/walk input)
  const rect = canvas.getBoundingClientRect();
  const ndc = new THREE.Vector2(((ev.clientX - rect.left) / rect.width) * 2 - 1, -((ev.clientY - rect.top) / rect.height) * 2 + 1);
  raycaster.setFromCamera(ndc, camera);
  const targets = [];
  if (state.mesh) targets.push(state.mesh);
  if (state.veg) targets.push(...state.veg.meshes, ...state.veg.markerMeshes);
  const hits = raycaster.intersectObjects(targets, false);
  if (!hits.length) return;
  const hit = hits[0];
  const s = state.status;
  let out;
  if (hit.object === state.mesh) {
    const gx = Math.min(Math.max(Math.floor(hit.point.x / TILE_M), 0), GRID_W - 1);
    const gy = Math.min(Math.max(Math.floor(hit.point.z / TILE_M), 0), GRID_H - 1);
    const key = `${gx},${gy}`;
    const cached = state.cache.get(key);
    const h = state.heightField ? state.heightField.triangleHeightAtWorld(hit.point.x, hit.point.z) : null;
    out = {
      kind: 'TERRAIN',
      era: cached?.identity?.era ?? s?.era,
      container: cached?.identity?.container ?? 'Terrain/terrain.bnt',
      containerSha256: cached?.identity?.containerSha256 ?? s?.containers?.terrain?.sha256,
      entry: cached?.identity?.entryName ?? tileName(gx, gy),
      decoder: 'PESourceMount.getTerrainTile (BNT2 terrain framing; TDF offset-64 heights, RAW uint16) → TerrainTile → PETerrainRegion/PEHeightField',
      sceneObject: 'the near-layer render mesh (PETerrainRegion.buildGeometry quads)',
      appliedPolicy: `LOD=near (8×8 window); calibration=CURRENT_RUNTIME_CALIBRATION applied EXACTLY ONCE; clickedSurface=${h === null ? 'BRAK DANYCH (null)' : `${h.toFixed(3)} adapter-m (the EXACT rendered-triangle plane)`}`,
      note: 'entry/payload SHA available per-tile through /api/world/tile/<gx>/<gy>/meta (bounded); the click identity here is the cache-verified tile entry + container pin',
    };
  } else if (hit.object.userData?.vegetation) {
    const v = hit.object.userData.vegetation;
    const entry = state.veg.modelCache.get(v.modelId);
    out = {
      kind: 'VEGETATION_INSTANCE_MESH',
      era: s?.era,
      container: 'Models.bnt',
      containerSha256: s?.containers?.models?.sha256,
      entry: `${v.modelId}.nif`,
      payloadSha256: entry?.payloadSha256 ?? '(fetch /api/world/model/<id> headers)',
      decoder: 'parseWitnessModel (NifModelReader, v10.1.0.0 qualified importer — LOUD failures) → NiTriShape → NiTexturingProperty → NiArkTextureExtraData → <id>.dat → decodeModelTextureStrict (TGA 24/32 + DDS DXT1/DXT5 qualified)',
      sceneObject: `InstancedMesh (shared geometry+material; shape ${v.shapeName ?? v.shapeIndex})`,
      appliedPolicy: `RECONSTRUCTION_PREVIEW: [P-UNITS] cm→m ×0.01 RAZ; [P-AXIS] (x,z,-y); [P-UV] raw v; [P-SCALE] node×${2.0.toFixed(1)}/NODE_SCALE_MUL; placement = the SHARED triangle query surface; textureId=${v.textureId ?? '(untextured)'}`,
      note: 'INSTANCE_DISTRIBUTION = the documented PEFoliageLabSeed wrapper (LAB_SEED-keyed) — reconstruction, NEVER a historical placement claim',
    };
  } else if (hit.object.userData?.marker === true || hit.object.material === state.veg._markerMaterial) {
    out = { kind: 'UNSUPPORTED_MODEL_MARKER', note: 'the diagnostic marker — explicitly NOT an original tree model (UNSUPPORTED import chain; counted, never substituted)' };
  }
  if (out) {
    state.debugPoint = out;
    $('debug-point').textContent = JSON.stringify(out, null, 1).slice(0, 4000);
    if ($('world-side').getAttribute('data-open') !== 'true') { /* the drawer stays as-is; the value waits there */ }
  }
}
canvas.addEventListener('click', debugPointFromClick);
canvas.addEventListener('pointerdown', (ev) => { /* orbit click-select kept distinct from mode clicks: see click above */ });

// ---- HUD + census panels ----
let censusTimer = 0;
function updateHud(now) {
  const p = camera.position;
  const gx = Math.min(Math.max(Math.floor(p.x / TILE_M), 0), GRID_W - 1);
  const gy = Math.min(Math.max(Math.floor(p.z / TILE_M), 0), GRID_H - 1);
  const lx = Math.min(Math.max(Math.floor((p.x - gx * TILE_M) / PE_TERRAIN_METER_PER_SAMPLE), 0), 31);
  const ly = Math.min(Math.max(Math.floor((p.z - gy * TILE_M) / PE_TERRAIN_METER_PER_SAMPLE), 0), 31);
  let raw = '—';
  if (state.heightField) {
    const r = state.heightField.rawSample(
      Math.floor((p.x - (state.windowOrigin.gx - 1) * TILE_M) / PE_TERRAIN_METER_PER_SAMPLE),
      Math.floor((p.z - (state.windowOrigin.gy - 1) * TILE_M) / PE_TERRAIN_METER_PER_SAMPLE));
    if (r !== null && r !== undefined) raw = String(r);
  }
  $('pos-hud').textContent =
    `pozycja (jednostki adaptera — NIE „oryginalne XYZ”): X=${p.x.toFixed(1)} Y=${p.y.toFixed(1)} Z=${p.z.toFixed(1)} m ` +
    `| kafel ${gx}:${gy} (${tileName(gx, gy)}) | próbka (x=${lx}, y=${ly}) | surowe u16=${raw} | tryb: ${{ orbit: 'ORBITA', fly: 'LOT', walk: 'SPACER' }[state.mode]}`;
  if (now - censusTimer > 400) {
    censusTimer = now;
    updateCensusPanel();
    // stream check — the WINDOW FOLLOWS THE FOCUS (§5/WL-4), every census tick
    const ft = focusTile();
    const want = desiredOrigin(ft.gx, ft.gy);
    if (state.windowOrigin && (want.gx !== state.windowOrigin.gx || want.gy !== state.windowOrigin.gy)) {
      requestScene(want);
    }
  }
}

/** §3.1: the honest scene-coherence line (never terrain A with trees B as READY). */
function updateCoherencePanel() {
  const req = state.sceneRequest;
  if (!req) { $('scene-coherence').textContent = 'scena: — (brak żądania)'; return; }
  const same = (a) => a && a.gx === req.origin.gx && a.gy === req.origin.gy;
  const terrainOk = same(state.coherence.terrain);
  const splatOk = !state.texturesOn || same(state.coherence.splat);
  const vegOk = !state.vegOn || same(state.coherence.veg);
  const all = terrainOk && splatOk && vegOk;
  const o = (a) => a ? `${a.gx},${a.gy}` : '—';
  $('scene-coherence').textContent =
    `scena #${req.id}: żądane okno ${req.origin.gx},${req.origin.gy} | teren ${o(state.coherence.terrain)} | tekstury ${state.texturesOn ? o(state.coherence.splat) : 'wył.'} | roślinność ${state.vegOn ? o(state.coherence.veg) : 'wył.'}\n` +
    `status spójności: ${all ? 'GOTOWA (wszystkie komponenty tego samego żądania)' : `${!terrainOk ? 'teren ładowany; ' : ''}${!splatOk ? 'tekstury budowane; ' : ''}${!vegOk ? 'roślinność budowana; ' : ''}(PARTIAL — poprzednia spójna scena pozostaje widoczna)`}\n` +
    `tożsamość: era ${req.era} | profil ${req.profileMode}${req.profileMode === 'global' ? `:${req.profile}` : ' (mapa NASZA)'} | LAB_SEED ${req.labSeed} | gęstość ${req.density}% | wersje: heightQuery=${req.versions.heightQuery} veg=${req.versions.vegetation} lod=${req.versions.lod}`;
  if (all && !state.readyShown) {
    state.readyShown = true;
    setLoadStatus('READY');
    hud(`scena GOTOWA — okno ${req.origin.gx},${req.origin.gy} (teren+tekstury+roślinność tego samego żądania); F dopasuj, R reset`);
  }
}

function updateCensusPanel() {
  let cacheBytes = 0; for (const e of state.cache.values()) cacheBytes += e.tile.heights.byteLength;
  let texBytes = 0; for (const e of state.textureRgbaCache.values()) texBytes += e.rgba.byteLength;
  const verts = state.mesh ? state.mesh.geometry.getAttribute('position').count : 0;
  const idx = state.mesh ? state.mesh.geometry.getIndex().count / 3 : 0;
  const d = state.mat.lastDiag;
  const splatLine = !state.texturesOn
    ? 'tekstury terenu: WYŁĄCZONE (paleta wysokości)'
    : state.splat
      ? `tekstury terenu: WŁĄCZONE — resolved ${d?.resolvedLayers ?? 0}/${d?.layersTotal ?? 0} warstw, zdekodowane ${d?.decoded ?? 0}, zastosowane ${d?.appliedLayers ?? 0}${d?.decodeFailures?.length ? `, błędy dekodowania: ${d.decodeFailures.length}` : ''}`
      : 'tekstury terenu: WŁĄCZONE — buduję łańcuch materiałów/tekstur okna…';
  const vc = state.vegCensus;
  const vegLine = !state.vegOn
    ? 'roślinność: WYŁĄCZONA (#veg=0; współdzielony cache modeli zachowany)'
    : vc && vc.ok
      ? `roślinność: żądane ${vc.counts.requested} / wybrane ${vc.counts.selected} / umieszczone ${vc.counts.placed} / ograniczone ${vc.counts.limited} (limit ${vc.counts.cap}; sprawiedliwy dobór per kafel)\n` +
        `  statusy: PLACED ${vc.statusCounts.PLACED_ON_AVAILABLE_SURFACE} | DEFERRED_NO_SURFACE ${vc.statusCounts.DEFERRED_NO_SURFACE} | UNSUPPORTED_MODEL ${vc.statusCounts.UNSUPPORTED_MODEL} | LOD_LIMITED ${vc.statusCounts.LOD_LIMITED}\n` +
        `  modele: kandydaci ${vc.distinctIds.candidates} → wybrane ${vc.distinctIds.selected} → geometry renderowane ${vc.distinctIds.geometryRendered} (wsparte ${vc.models.supported.length}, bez tekstur ${vc.models.untextured.length}, UNSUPPORTED ${vc.models.unsupported.length}, markery ${vc.distinctIds.markers})`
      : vc && vc.unsupportedProfile
        ? 'roślinność: profil UNSUPPORTED (strict decoder) — ZERO instancji (uczciwie)'
        : `roślinność: ${state.vegBusy ? 'budowanie…' : (vc?.error ?? '…')}`;
  const lod = state.lod;
  const lodLine = lod
    ? `daleki LOD: far ${lod.far.status === 'READY' ? `GOTOWY (${lod.far.tris} trójk., reprezentuje ${lod.coverage.farTilesRepresented} kafli, braki ${lod.coverage.farTilesMissing})` : lod.farProgressNote()} | mid ${lod.mid.status === 'READY' ? `GOTOWY (${lod.mid.tris} trójk. przy ${JSON.stringify(lod.mid.origin)}, bloków w cache ${lod.mid.blocksCache.size})` : 'budowanie…'}`
    : 'daleki LOD: nie uruchomiony';
  $('world-census').textContent =
    `kafle aktywne (okno 8×8): ${state.region ? WINDOW_T * WINDOW_T : 0} / limit 64 | halo 10×10 (rzeczywiste próbki) dla wysokości drzew/spaceru\n` +
    `cache klienta: ${state.cache.size} kafli (${(cacheBytes / 1024).toFixed(0)} KiB; limit ${CLIENT_CACHE_MAX})\n` +
    `pobrania: ${state.fetchCount} | błędy: ${state.fetchErrors}${state.lastError ? `\nostatni błąd: ${state.lastError}` : ''}\n` +
    `geometria bliska: ${verts} wierzchołków, ${idx} trójkątów (1 mesh regionu) | przebudowań okna: ${state.rebuilds} | teleporty: ${state.teleportCount}\n` +
    `${splatLine}\n` +
    `${vegLine}\n` +
    `${lodLine}\n` +
    `cache tekstur RGBA: ${state.textureRgbaCache.size} (${(texBytes / 1024 / 1024).toFixed(1)} MiB; limit ${TEXTURE_CACHE_MAX}) | fetch materiałów: ${state.mat.materialsFetches} (błędy ${state.mat.materialsErrors}) | fetch tekstur: ${state.mat.textureFetches} (błędy ${state.mat.textureErrors})\n` +
    `cache modeli roślinności: ${state.veg ? state.veg.modelCache.size : 0} (limit ${MODEL_CACHE_MAX}) | fetch modeli: ${state.veg ? state.veg.fetchCounters.modelPayloads : 0} | fetch tekstur modeli: ${state.veg ? state.veg.fetchCounters.texturePayloads : 0}\n` +
    `renderer: draw calls ${renderer.info.render.calls}, trójkąty ${renderer.info.render.triangles}, tekstury ${renderer.info.memory.textures}, geometrie ${renderer.info.memory.geometries}\n` +
    `origin okna: ${state.windowOrigin ? `${state.windowOrigin.gx},${state.windowOrigin.gy}` : '—'}`;
  updateCoherencePanel();
  const vs = $('veg-status-line');
  vs.hidden = !state.vegOn || !vc?.ok;
  if (state.vegOn && vc?.ok) {
    vs.textContent = `roślinność: ${vc.counts.placed} instancji na powierzchni · ${vc.distinctIds.geometryRendered} typów modeli z geometrią · profil ${vc.profiles.mode}`;
  }
}

// ---- §7/§8 QC: a minimal READ-ONLY debug handle (introspection for the
// browser QC harnesses; no behavior is changed through it — the debug POINT
// in the drawer remains the human-facing provenance view) ----
window.__peR2Debug = {
  get mode() { return state.mode; },
  get keys() { return [...move.keys]; },
  get yawPitch() { return { yaw: move.yaw, pitch: move.pitch }; },
  get camera() { return { x: camera.position.x, y: camera.position.y, z: camera.position.z }; },
  get windowOrigin() { return state.windowOrigin ? { ...state.windowOrigin } : null; },
  get fieldSpan() {
    const f = state.heightField;
    if (!f) return null;
    return { originGx: f.originGridX, originGy: f.originGridY, tilesX: f.tilesX, tilesY: f.tilesY, ...f.census() };
  },
  get running() { return { busy: state.rebuildBusy, runningOrigin: state.runningOrigin ? { ...state.runningOrigin } : null, pending: state.pendingOrigin ? { ...state.pendingOrigin } : null, sceneId: state.sceneRequest?.id ?? null, vegBusy: state.vegBusy, vegPending: state.vegPending ? { origin: { ...state.vegPending.origin }, requestId: state.vegPending.requestId } : null, vegTrace: state.vegTrace.slice(-24) }; },
  queryHeightAt(x, z) { return state.heightField ? state.heightField.triangleHeightAtWorld(x, z) : null; },
};

// ---- animate ----
let lastT = performance.now();
function animate() {
  requestAnimationFrame(animate);
  const now = performance.now();
  const dt = Math.min(0.1, (now - lastT) / 1000);
  lastT = now;
  updateFlyWalk(dt);
  if (state.mode === 'orbit') controls.update();
  renderer.render(scene, camera);
  if (!state.firstFrameDone && state.mesh) {
    state.firstFrameDone = true;
    if (!state.readyShown) setLoadStatus('LOADING');
  }
  updateHud(now);
}

// ---- toggles / buttons ----
$('tog-wireframe').addEventListener('change', (ev) => { if (state.mesh) state.mesh.material.wireframe = ev.target.checked; });
$('tog-tilebounds').addEventListener('change', () => {
  if (state.region && state.lastGeo && state.windowOrigin) buildTileBounds(state.region, state.lastGeo, state.windowOrigin);
});
$('tog-textures').addEventListener('change', async (ev) => {
  state.texturesOn = ev.target.checked;
  if (state.texturesOn && state.windowOrigin && !state.splat) {
    hud('buduję tekstury terenu (łańcuch materiał→tekstura)…');
    await applyTexturesForWindow(state.windowOrigin, state.sceneRequest?.id);
  }
  if (state.splat) state.coherence.splat = state.splat.origin;
  applyTerrainMaterial();
  hud(state.texturesOn ? 'tekstury terenu WŁĄCZONE (oryginalne z łańcucha id@+16 → <id>.dat; preset RENDER_RECONSTRUCTION)' : 'tekstury terenu WYŁĄCZONE (paleta wysokości)');
});
$('tog-vegetation').addEventListener('change', async (ev) => {
  state.vegOn = ev.target.checked;
  if (state.veg) state.veg.setEnabled(state.vegOn);
  if (state.vegOn && state.veg && state.windowOrigin) {
    hud('buduję podgląd roślinności (deterministyczny wrapper LAB_SEED + oryginalne modele z Models.bnt)…');
    await rebuildVegetation(state.windowOrigin, state.sceneRequest?.id);
  }
  hud(state.vegOn
    ? 'roślinność WŁĄCZONA (RECONSTRUCTION_PREVIEW: profile .vcl + byte-locked RNG + wrapper LAB_SEED; modele ORYGINALNE)'
    : 'roślinność WYŁĄCZONA (instancje okna zwolnione; współdzielony cache modeli zachowany)');
});
$('btn-mode-orbit').addEventListener('click', () => setMode('orbit'));
$('btn-mode-fly').addEventListener('click', () => setMode('fly'));
$('btn-mode-walk').addEventListener('click', () => setMode('walk'));
$('btn-fit').addEventListener('click', fitView);
$('btn-reset').addEventListener('click', resetView);
$('btn-launcher').addEventListener('click', () => { location.href = '/launcher'; });
$('btn-assetlab').addEventListener('click', () => { location.href = '/compat/assetlab.html'; });
$('tp-go').addEventListener('click', () => {
  const gx = parseInt($('tp-gx').value, 10), gy = parseInt($('tp-gy').value, 10);
  if (Number.isInteger(gx) && Number.isInteger(gy) && gx >= 0 && gy >= 0 && gx < GRID_W && gy < GRID_H) teleportTo(gx, gy);
  else banner('teleport: podaj poprawny kafel gx (0..219), gy (0..235)');
});

// ---- the „Szczegóły” drawer (§5) ----
function applyDrawerState() {
  const open = localStorage.getItem('pe-world-drawer') === '1';
  $('world-side').setAttribute('data-open', open ? 'true' : 'false');
}
$('btn-drawer').addEventListener('click', () => {
  const cur = $('world-side').getAttribute('data-open') === 'true';
  $('world-side').setAttribute('data-open', cur ? 'false' : 'true');
  localStorage.setItem('pe-world-drawer', cur ? '0' : '1');
  syncCanvasSize();
});
$('btn-drawer-close').addEventListener('click', () => {
  $('world-side').setAttribute('data-open', 'false');
  localStorage.setItem('pe-world-drawer', '0');
  syncCanvasSize();
});

// ---- the vegetation config controls (drawer inputs; apply = a NEW scene request) ----
function fillVegProfileSelect(climates) {
  const sel = $('veg-profile');
  sel.innerHTML = '';
  for (const p of climates.profiles ?? []) {
    const opt = document.createElement('option');
    opt.value = String(p.index);
    opt.textContent = `${p.index} — ${p.status === 'DECODED' ? 'DECODED' : `UNSUPPORTED (${p.error ?? 'strict decoder'})`}${p.modelSummary ? ` (${p.modelSummary.distinctModels ?? '?'} modeli)` : ''}`;
    sel.appendChild(opt);
  }
  sel.value = String(state.vegConfig.profile);
}
$('veg-mode').addEventListener('change', (ev) => { state.vegConfig.profileMode = ev.target.value; });
$('veg-profile').addEventListener('change', (ev) => { state.vegConfig.profile = parseInt(ev.target.value, 10) || 0; });
$('veg-seed').addEventListener('change', (ev) => { state.vegConfig.labSeed = Math.max(0, Math.floor(Number(ev.target.value) || 0)); });
$('veg-density').addEventListener('input', (ev) => {
  state.vegConfig.densityPercent = parseInt(ev.target.value, 10) || 0;
  $('veg-density-value').textContent = `${ev.target.value}%`;
});
$('veg-apply').addEventListener('click', async () => {
  if (!state.veg) return;
  await state.veg.setConfig(state.vegConfig);
  if (state.windowOrigin) {
    // the CONFIG is part of the scene identity: a config change REQUIRES a new
    // request id even for the same origin (forceNew — §3.1)
    const id = requestScene(state.windowOrigin, { forceNew: true });
    void rebuildVegetation(state.windowOrigin, id);
  }
  hud(`roślinność: profil ${state.vegConfig.profileMode}${state.vegConfig.profileMode === 'global' ? `:${state.vegConfig.profile}` : ''} | LAB_SEED ${state.vegConfig.labSeed} | gęstość ${state.vegConfig.densityPercent}% — przebudowa`);
});

// ---- boot ----
async function boot() {
  setLoadStatus('LOADING');
  applyDrawerState();
  syncCanvasSize();
  hud('łączę z serwerem świata…');
  state.status = await fetchJson('/api/world/status');
  state.status.identityOf = {
    era: state.status.era,
    container: 'Terrain/terrain.bnt',
    containerSha256: state.status.containers.terrain.sha256,
  };
  // anchor: explicit selection or the measured default (data-derived; no city names)
  const anchor = params.anchor ?? (state.status.census.maxMeanTile
    ? { gx: Math.min(state.status.census.maxMeanTile.gridX, GRID_W - 4), gy: Math.min(state.status.census.maxMeanTile.gridY, GRID_H - 4) }
    : { gx: 108, gy: 116 });
  state.anchor = anchor;
  state.spawn = { x: anchor.gx * TILE_M + 128, z: anchor.gy * TILE_M + 128 };
  // the distant LOD subsystem (§4) — mid + far from decimated REAL samples
  state.lod = new WorldLod({
    scene,
    fetchJson,
    fetchBinary: async (url) => {
      const r = await fetch(url, { cache: 'no-store' });
      if (!r.ok) {
        const t = await r.text();
        let msg = `HTTP ${r.status}`;
        try { msg = JSON.parse(t).message || msg; } catch { /* raw */ }
        throw new Error(`${url}: ${msg}`);
      }
      return { payload: new Uint8Array(await r.arrayBuffer()), headers: {} };
    },
  });
  state.lod.setGrid(GRID_W, GRID_H); // the far payload header carries the MEASURED grid (verified in ensureFar)
  // vegetation subsystem (§6) — the SHARED height query (§3.2): one stable
  // delegating handle over the per-window PEHeightField (rendering, trees and
  // walking all read the SAME triangle-exact field)
  const sharedHeightQuery = {
    version: 'peheight-query-triangle-v1',
    triangleHeightAtWorld: (x, z) => (state.heightField ? state.heightField.triangleHeightAtWorld(x, z) : null),
    _delegatesTo: () => state.heightField,
  };
  state.veg = new WorldVegetation({
    scene,
    fetchJson,
    fetchBinary: async (url) => {
      if (url.startsWith('/api/world/model/')) {
        return fetchVegBinary(url, { container: 'Models.bnt', containerSha256: state.status?.containers?.models?.sha256 });
      }
      return fetchVegBinary(url, { container: 'Textures.bnt', containerSha256: state.status?.containers?.textures?.sha256 });
    },
    heightField: sharedHeightQuery,
  });
  await state.veg.setConfig(state.vegConfig);
  // the climate census for the profile picker (drawer)
  try {
    const climates = await fetchJson('/api/world/climates');
    fillVegProfileSelect(climates);
  } catch { /* the select stays empty; the config still applies */ }
  $('veg-mode').value = state.vegConfig.profileMode;
  $('veg-seed').value = String(state.vegConfig.labSeed);
  $('veg-density').value = String(state.vegConfig.densityPercent);
  $('veg-density-value').textContent = `${state.vegConfig.densityPercent}%`;
  updateVegPanel();
  updateEvidencePanel();
  // initial window centered on the anchor + the first scene request
  const origin = desiredOrigin(state.anchor.gx + 1, state.anchor.gy + 1);
  const id = requestScene(origin);
  await new Promise((resolve) => {
    const wait = () => { if (state.coherence.terrain) resolve(); else setTimeout(wait, 120); };
    wait();
  });
  if (!state.mesh) {
    if (!$('diagnostics').getAttribute('data-load-status').startsWith('ERROR')) {
      setLoadStatus('ERROR_TERRAIN_LOAD: brak mesha po początkowym ładowaniu (uczciwy błąd)');
    }
    return;
  }
  // the texture chain for the initial window (toggle default from the URL)
  $('tog-textures').checked = state.texturesOn;
  if (state.texturesOn) {
    setLoading('czekam na indeks tekstur (weryfikacja pinu Textures.bnt)…');
    const waitT0 = performance.now();
    for (;;) {
      state.status = await fetchJson('/api/world/status');
      const stx = state.status?.containers?.textures;
      if (stx?.indexState === 'READY') break;
      if (performance.now() - waitT0 > 20000) {
        banner(`TEKSTURY TERENU: indeks Textures.bnt niegotowy po 20 s — teren działa z paletą; tekstury włącz ręcznie po powodzeniu weryfikacji.`);
        state.texturesOn = false;
        $('tog-textures').checked = false;
        break;
      }
      await new Promise((r) => setTimeout(r, 500));
    }
    if (state.texturesOn) {
      setLoading('buduję łańcuch materiały→tekstury okna…');
      const td = await applyTexturesForWindow(origin, id);
      if (td && !td.aborted) state.coherence.splat = state.splat?.origin ?? null;
    }
  }
  // the initial vegetation build (awaited — the scene is READY only when the
  // census is real or honestly diagnosed)
  $('tog-vegetation').checked = state.vegOn;
  if (state.vegOn) {
    setLoading('czekam na indeks modeli (weryfikacja pinu Models.bnt)…');
    const waitT0 = performance.now();
    for (;;) {
      state.status = await fetchJson('/api/world/status');
      const stm = state.status?.containers?.models;
      if (stm?.indexState === 'READY') break;
      if (performance.now() - waitT0 > 20000) {
        banner(`ROŚLINNOŚĆ: indeks Models.bnt niegotowy po 20 s — teren działa; roślinność włącz ręcznie.`);
        state.vegOn = false;
        $('tog-vegetation').checked = false;
        break;
      }
      await new Promise((r) => setTimeout(r, 500));
    }
    if (state.vegOn) {
      setLoading('buduję podgląd roślinności (profil .vcl → wrapper LAB_SEED → instancje → oryginalne modele)…');
      await rebuildVegetation(origin, id, { awaited: true });
    }
  }
  // the far LOD: poll the census progress honestly (no zero placeholder)
  void (async () => {
    setLoading('daleki LOD: czekam na census regularnych kafli (rzeczywiste próbki, decymowane)…');
    for (;;) {
      try {
        const p = await fetchJson('/api/world/overview/progress');
        if (state.lod.far.status === 'READY') break;
        const ok = await state.lod.ensureFar();
        if (ok) {
          state.lod.rebuildFarIndex(state.lod.mid.origin ?? origin);
          break;
        }
        if (!state.lodFarReadyShown) {
          state.lodFarReadyShown = true;
        }
        await new Promise((r) => setTimeout(r, 1000));
      } catch {
        await new Promise((r) => setTimeout(r, 1500));
      }
      if (state.lod.far.status === 'READY' || state.lod.far.status === 'FAILED') break;
    }
    updateCensusPanel();
    if (state.lod.far.status === 'FAILED') {
      banner(`DALEKI LOD: ${state.lod.far.error?.slice(0, 160) ?? 'błąd'} — świat działa z warstwą bliską + mid; brak nie jest maskowany.`);
    }
  })();
  updateVegPanel();
  updateEvidencePanel();
  resetView();
  animate();
}

function updateVegPanel() {
  const cfg = state.vegConfig;
  const vc = state.vegCensus;
  const sv = state.status?.vegetation;
  const lines = [];
  lines.push(`Tryb profilu: ${cfg.profileMode === 'regional' ? 'REGIONALNY RECONSTRUCTION_PREVIEW (mapa NASZA — nie historyczny biom)' : 'GLOBALNY (oryginalnie odczytany profil)'} | profil ${cfg.profile} | LAB_SEED ${cfg.labSeed} | gęstość ${cfg.densityPercent}% | p3 = 0 [P-RNG-P3] (OSOBNO — nigdy LAB_SEED)`);
  if (cfg.profileMode === 'regional') {
    lines.push(`mapa regionów (NASZA rekonstrukcja): ${REGIONAL_PREVIEW.mapRule}; region = ${REGIONAL_PREVIEW.regionTiles} kafli; profile ${JSON.stringify(REGIONAL_PREVIEW.profiles)} — ${REGIONAL_PREVIEW.note}`);
  }
  if (sv) {
    lines.push(`VEGETATION_MODE = ${sv.mode} — ${sv.threeWaySeparation.INSTANCE_DISTRIBUTION}`);
    if (sv.defaultProfile) lines.push(`domyślny profil serwera: ${sv.defaultProfile.index} (${sv.defaultProfile.measuredJustification})`);
  }
  if (vc && vc.ok) {
    lines.push(`instancje okna: żądane ${vc.counts.requested} / wybrane ${vc.counts.selected} / umieszczone ${vc.counts.placed} / ograniczone ${vc.counts.limited} (limit ${vc.counts.cap})`);
    lines.push(`statusy (jawne): PLACED_ON_AVAILABLE_SURFACE ${vc.statusCounts.PLACED_ON_AVAILABLE_SURFACE} | DEFERRED_NO_SURFACE ${vc.statusCounts.DEFERRED_NO_SURFACE} | UNSUPPORTED_MODEL ${vc.statusCounts.UNSUPPORTED_MODEL} | LOD_LIMITED ${vc.statusCounts.LOD_LIMITED}`);
    lines.push(`profile w oknie: ${vc.profiles.mode} → ${JSON.stringify(vc.profiles.used)} | rekordy ${vc.profiles.records}`);
    if (vc.models.untextured.length) lines.push(`modele bez oryginalnych tekstur (uczciwie): ${vc.models.untextured.map((m) => m.id).join(', ')}`);
    if (vc.models.unsupported.length) lines.push(`modele UNSUPPORTED (znacznik diagnostyczny): ${vc.models.unsupported.map((m) => m.id).join(', ')}`);
    if (vc.models.slotDiagnostics?.length) lines.push(`pominięte sloty tekstur (jawne): ${vc.models.slotDiagnostics.length}`);
    lines.push(`umiejscowienie: WSPÓLNE zapytanie trójkątowe (dokładnie renderowane płaszczyzny + halo rzeczywistych próbek) — REKONSTRUKCJA (nigdy historyczny placement)`);
  } else if (vc && vc.unsupportedProfile) {
    lines.push(`PROFIL UNSUPPORTED (strict decoder): ${vc.error ?? '—'} — zero instancji (25.vcl pozostaje UNSUPPORTED — bez konwersji przecinków)`);
  } else if (state.vegOn && !vc) {
    lines.push('łańcuch roślinności: budowanie…');
  } else if (!state.vegOn) {
    lines.push('roślinność WYŁĄCZONA (#veg=0)');
  }
  lines.push(`rozdział (kontrakt §6): ORIGINAL_CLIMATE_RECORDS = przypięte .vcl (strict); RECOVERED_RNG_ARITHMETIC = byte-locked PEFoliageCore NIETKNIĘTY; INSTANCE_DISTRIBUTION = wrapper PEFoliageLabSeed v2 (recIndex w kluczu, gęstość frakcyjna — wersjonowane)`);
  $('world-veg').textContent = lines.join('\n');
}

function updateEvidencePanel() {
  const s = state.status;
  const d = state.mat.lastDiag;
  const den = s?.denominator;
  $('world-evidence').textContent = [
    `era: ${s.era} | terrain.bnt SHA256: ${s.containers.terrain.sha256} (pin zweryfikowany fail-closed)`,
    `mianownik (ZMIERZONY z indeksu — nie hardcode): zwykłe kafle w indeksie ${den?.indexRegularTiles ?? '—'} (pojemność siatki ${den?.gridCapacity ?? '—'}); wpisy razem ${den?.indexTotalEntries ?? '—'}; wiersze specjalne ${den?.specialRows ?? '—'}; sentinel ${den?.sentinel ?? '—'}`,
    `kalibracja (CURRENT_RUNTIME_CALIBRATION — preset z provenance, NIE fakt historyczny): u16PerMeter=${s.calibration.u16PerMeter}; meterPerSample=${s.calibration.meterPerSample}; min/max=${s.calibration.minMax}`,
    `konwersja u16→metry zastosowana DOKŁADNIE RAZ (wspólne PEHeightField/PETerrainRegion — worldHeightMeters); odwracalna: ×${s.calibration.u16PerMeter}; bez wygładzania źródła`,
    `---- wysokość: jedno wspólne zapytanie (kontrakt §3.2) ----`,
    `rendering + drzewa + spacer = PEHeightField.triangleHeightAtWorld (DOKŁADNIE renderowane trójkąty warstwy bliskiej;`
    + ` ten sam podział quada co PETerrainRegion.buildGeometry); halo = 1 kafel RZECZYWISTYCH sąsiednich próbek (rozwiązanie granicy 256/0..510 vs generator 0..512);`
    + ` brak danych = null (nigdy y=0, nigdy duplikat ostatniej wysokości); statusy instancji: PLACED/DEFERRED_NO_SURFACE/UNSUPPORTED_MODEL/LOD_LIMITED`,
    `---- ciągły świat (kontrakt §4) ----`,
    `near = okno 8×8 (RAW u16, PETerrainRegion); mid = 40×40 kafli, 8×8 decymowanych RZECZYWISTYCH próbek/kafel (bloki /api/world/lod8);`
    + ` far = cały świat 4×4 decymowane (census-gated); granice poziomów = te same oryginalne próbki na liniach cięcia (bez szwów, bez skirtów);`
    + ` brakujące kafle = jawne dziury (status, nie zero); polityka = RENDERERA (nie format źródłowy, nie odzyskany paging PE)`,
    `---- tekstury terenu (oryginalne) ----`,
    `materiały: rekordy nazwane TDF, maska@record+56; wagi RAW u8 — sumy >255 to DANE ORYGINALNE (bez normalizacji)`,
    `relacja: id@+16 → "<id>.dat" w Textures.bnt (era PCG_9_3_5; potwierdzona silnikowo)`,
    d ? `okno: resolved ${d.resolvedLayers ?? 0}/${d.layersTotal ?? 0} | zdekodowane ${d.decoded ?? 0} | zastosowane ${d.appliedLayers ?? 0}${d.decodeFailures?.length ? ` | błędy: ${d.decodeFailures.length}` : ''}` : `okno: łańcuch tekstur jeszcze niezbudowany`,
    `preset renderowania: RENDER_RECONSTRUCTION — ${RENDER_RECONSTRUCTION_PRESET.blendForm}; UV ${RENDER_RECONSTRUCTION_PRESET.uv}; próbki komórek ${RENDER_RECONSTRUCTION_PRESET.cellSampling}`,
    `---- roślinność (RECONSTRUCTION_PREVIEW) ----`,
    `trójstopniowy rozdział: ORIGINAL_CLIMATE_RECORDS (.vcl strict; 25 UNSUPPORTED) | RECOVERED_RNG_ARITHMETIC (PEFoliageCore byte-locked — NIETKNIĘTY) | INSTANCE_DISTRIBUTION (wrapper PEFoliageLabSeed v2 — LAB_SEED; recIndex w kluczu pozycji; gęstość frakcyjna ${'labseed-density-v2-fractional'}; rekonstrukcja)`,
    `modele: <id>.nif z PCG_9_3_5 Models.bnt → parseWitnessModel → NiTriShape → NiTexturingProperty → NiArkTextureExtraData → <id>.dat z Textures.bnt → decodeModelTextureStrict (TGA2 24bpp / A32 32bpp / DDS DXT1+DXT5 — kwalifikowane na RZECZYWISTYCH payloadach tego runu: 518860/518862/516807 DXT1, 166881 DXT5; kontrole negatywne: truncated/fourcc/magic) → GPU`,
    `granic uczciwe: [P-UNITS] cm→m ×0.01 RAZ; [P-AXIS] (x,z,-y); [P-UV] surowe v; [P-SCALE] 2.0/NODE_SCALE_MUL×0.01 (CURRENT_RUNTIME_CALIBRATION); brak łańcucha texprop→Ark = NIE-wizualne; UNSUPPORTED → znacznik diagnostyczny, nigdy zamiennik`,
    `spawn: kafel ${state.anchor.gx},${state.anchor.gy} (zaznaczenie z launchera / domyślnie najwyższa zmierzona średnia — wybór z DANYCH)`,
    `census terenu: ${s.census.measured}/${s.census.total} zwykłych kafli zmierzonych; NODATA: ${s.census.missing}+${s.census.failed}; sentinel/wiersze specjalne wykluczone.`,
    `HISTORICAL_TREE_DISTRIBUTION = NOT_ESTABLISHED | ORIGINAL_REGION_TO_CLIMATE_JOIN = NOT_ESTABLISHED | WORLD_XYZ_RECOVERED = NO`,
  ].join('\n');
}

boot().catch((e) => {
  setLoadStatus(`ERROR_BOOT: ${e?.message ?? e}`);
  banner(`KRYTYCZNY BŁĄD: ${e?.stack?.split('\n')[0] ?? e}`);
});
