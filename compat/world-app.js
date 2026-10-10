// world-app.js — PE_WORLD_LAUNCHER_R1_20261010, ETAP C (contract §4 + §7) + ETAP D (§5)
// THE /world view: terrain region rendering from ORIGINAL u16 samples.
//
// DATA PATH (production modules, no parallel decoder):
//   /api/world/tile/<gx>/<gy> (2048 B uint16 LE, raw heights offset 64..2111,
//   provenance headers) → canonical TerrainTile (client-side, provenance via
//   makeProvenance) → PETerrainRegion (NxN contiguous block, disjoint 32x32
//   sample blocks, NO seam repair) → buildGeometry() (positions + indices;
//   the u16→meters conversion is applied EXACTLY ONCE here, inside
//   worldHeightMeters, CURRENT_RUNTIME_CALIBRATION u16/128) → THREE
//   BufferGeometry (normals + preview palette are renderer-side
//   reconstruction aids — never source-data claims).
//
// ETAP D — ORIGINAL TERRAIN TEXTURES (contract §5, the proven chain):
//   per window tile: /api/world/tile/<gx>/<gy>/materials (named material
//   records in RECORD ORDER, RAW 16x16 masks at record+56 — base64, bit-exact,
//   NEVER normalized; per-material resolved "<id>.dat" texture entry per the
//   engine-RE-CONFIRMED id@+16 relation) → buildRegionSplatData (pure module,
//   compat/world-splat.js: per-cell layer slots in record order, EXACT-
//   duplicate dedupe, unresolved bindings SKIPPED with an explicit
//   diagnostic — never a fallback texture) → /api/world/texture/<id> (the
//   ORIGINAL bounded payload, provenance headers) → decodeTga2 (the SAME
//   PRODUCTION decoder as the server gates — strict TGA2 24bpp subset, LOUD
//   failure) → RGBA → THREE.DataArrayTexture + per-cell idx/weight
//   DataTextures (NearestFilter; RAW u8 weights bit-exact) → the splat
//   shader (sequential lerp per layer by RAW mask/255 in RECORD ORDER — the
//   era-evidenced blend FORM; the albedo role, the 32 m UV repeat and the
//   nearest-cell sampling are the labeled RENDER_RECONSTRUCTION preset) →
//   the visible terrain. The texture toggle ACTUALLY swaps the terrain
//   material (measured by the PIXEL on/off gates).
//
// INTER-TILE TOPOLOGY (documented choice, contract §4):
//   the active window is ONE 8x8-tile PETerrainRegion; buildGeometry emits
//   quads across tile borders derived from the ADJACENT ORIGINAL samples of
//   the two neighboring tiles (no shared/overlapping vertices, no height
//   changes for jump masking — tile-border differences are ORIGINAL DATA).
//   One region mesh per window → no inter-region cracks inside the active
//   set; the window edge is the visible streaming boundary.
//
// STREAMING: window = 8x8 tiles = AT MOST 64 ACTIVE TILES, clamped at the
//   map edges; rebuild when the camera tile leaves the current window's
//   interior. Missing data (NODATA / fetch error) never builds a mesh over
//   void: movement is stopped at the boundary and the honest banner shows.
//   TEXTURES (ETAP D): the window's splat resources are rebuilt per window
//   and DISPOSED on window move (bounded client memory: the raw-height LRU +
//   the decoded-texture LRU keep only what the active window needs).
'use strict';

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { PETerrainRegion, worldHeightMeters, PE_TERRAIN_METER_PER_SAMPLE } from '/src/peworld/PETerrainCore.js';
import { TerrainTile } from '/src/pesource/TerrainTile.js';
import { makeProvenance } from '/src/pesource/PEProvenance.js';
import { decodeTga2 } from '/src/pesource/TgaDecoder.js';
import {
  buildRegionSplatData, RENDER_RECONSTRUCTION_PRESET, REGION_CELLS,
  WORLD_SPLAT_SCHEMA_VERSION, MAX_LAYERS_PER_CELL,
} from '/compat/world-splat.js';
import {
  WorldVegetation, MAX_VISIBLE_INSTANCES, MODEL_CACHE_MAX, VEGETATION_SCHEMA_VERSION,
} from '/compat/world-vegetation.js';

const $ = (id) => document.getElementById(id);
const GRID_W = 220, GRID_H = 236;          // regular filename-xy tile grid
const TILE_M = 64;                          // 32 samples × 2 m (CURRENT_RUNTIME_CALIBRATION)
const WINDOW_T = 8;                          // 8×8 tiles = 64 active tiles max
const CLIENT_CACHE_MAX = 512;                // bounded LRU of raw tile payloads
const TEXTURE_CACHE_MAX = 64;                // bounded LRU of decoded texture RGBA (active window needs ~23)
const EYE_OFFSET_M = 1.7;                    // walk-mode viewer eye offset (VIEWER SETTING, not PE data)
const UV_REPEAT_M = 32;                      // RENDER_RECONSTRUCTION: world meters per texture repeat (see world-splat.js)
const MATERIAL_CELL_M = 4;                   // 2×2 samples per 16x16 material cell = 4 m

const params = parseHash();
const state = {
  status: null,
  anchor: null,                 // selected 4x4 patch anchor {gx,gy}
  spawn: null,                  // {x, z} world meters
  windowOrigin: null,           // {gx,gy} current 8x8 window origin
  region: null, mesh: null, boundsLines: null,
  cache: new Map(),             // "gx,gy" -> {heights, identity, tile}
  cacheOrder: [],
  fetchCount: 0, fetchErrors: 0, lastError: null,
  rebuildBusy: false, pendingOrigin: null, rebuilds: 0,
  mode: 'orbit',
  firstFrameDone: false,
  boundaryHit: false,
  diag: [],
  // ---- ETAP D: the material->texture chain state ----
  texturesOn: params.textures !== '0',     // default ON (#textures=0 forces the palette preview)
  splat: null,          // { material, arrayTexture, idxTex[], wTex[], data, origin } — the CURRENT window's GPU resources
  materialsByOrigin: new Map(), // "gx,gy" -> the materials grid JSON (bounded: the current window only)
  textureRgbaCache: new Map(),  // id -> {rgba,width,height,identity} (bounded LRU)
  textureRgbaOrder: [],
  mat: {
    materialsFetches: 0, materialsErrors: 0,
    textureFetches: 0, textureErrors: 0,
    lastDiag: null,
    busy: false,
  },
  // ---- ETAP E: the vegetation subsystem state ----
  vegOn: params.veg !== '0',           // default ON (#veg=0 forces the no-vegetation view)
  veg: null,                           // the WorldVegetation instance (created in boot)
  vegCensus: null,                     // the last census (rendered by updateHud)
  vegBusy: false,
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
    textures: h.get('textures'), // undefined = default ON; '0' = palette preview; '1' = textures
    veg: h.get('veg'),           // undefined = default ON; '0' = vegetation OFF; '1' = ON (ETAP E)
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
  const id = state.status.identityOf; // live mount identity from /api/world/status
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

// ---- ETAP D: the material->texture chain (client side, contract §5) ----

/** Bounded LRU of DECODED texture RGBA (identity-checked — CAM-C3 discipline:
 * the entry carries era|container|containerSha256|id from the response
 * headers; a hit against a different container identity is REFUSED and
 * re-fetched from the ORIGINAL payloads). */
function textureRgbaGet(id, identity) {
  const e = state.textureRgbaCache.get(id);
  if (!e) return null;
  if (e.identity.era !== identity.era || e.identity.container !== identity.container ||
      String(e.identity.containerSha256) !== String(identity.containerSha256)) {
    state.textureRgbaCache.delete(id); // controlled refusal — refetch
    return null;
  }
  // LRU refresh
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
    state.textureRgbaCache.delete(old); // bounded: unload what the window no longer needs
  }
}

/** The materials grid of ONE 8x8 window (bounded parallel fetch; the served
 * objects carry the RAW masks + the per-material resolved texture entries). */
async function fetchMaterialsGrid(origin) {
  const grid = [];
  let done = 0;
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
    done += chunk.length;
    setLoading(`materiały okna 8×8: ${done}/64 kafli…`);
  }
  return grid;
}

/** Fetch + decode ONE original texture payload through the PRODUCTION
 * decoder (decodeTga2 — strict TGA2 24bpp subset; LOUD failure). The
 * response identity headers are verified against the live status identity
 * (era + container + containerSha256) BEFORE the bytes enter the cache. */
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
    throw new Error(`tekstura ${id}.dat: tożsamość kontenera z odpowiedzi nie zgadza się z live statusem (era/kontener/SHA) — kontrolowana odmowa`);
  }
  const buf = new Uint8Array(await r.arrayBuffer());
  const decoded = decodeTga2(buf); // LOUD on anything outside the confirmed subset
  if (decoded.width !== 256 || decoded.height !== 256) {
    throw new Error(`tekstura ${id}.dat: ${decoded.width}x${decoded.height} != 256x256 (spoza zbioru tekstur terenu — warstwa pominięta, jawnie)`);
  }
  const entry = { rgba: decoded.rgba, width: decoded.width, height: decoded.height, identity: { ...liveIdentity }, payloadSha256: hdr.payloadSha256 };
  textureRgbaPut(id, liveIdentity, decoded);
  return entry;
}

// The splat shader — the RENDER_RECONSTRUCTION preset (world-splat.js is the
// single source of truth for the preset text). Sequential lerp per layer by
// RAW mask/255 in SLOT ORDER (= record order per cell); idx=255 marks an
// empty slot; the material textures are sampled at GLOBAL world uv.
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
  // U-19 FIX (a) — the LAYER COORDINATE (QC P2-1, confirmed at code level):
  // the idx DataTextures are RGBA8 (UnsignedByteType), so texelFetch returns
  // the slot bytes NORMALIZED (byte/255 in [0,1]) — NOT the layer number.
  // The sampler2DArray layer coordinate must be the LAYER NUMBER: array layer
  // k is the window's texture slot k (buildRegionSplatData writes layer.slot
  // into the idx bytes and the DataArrayTexture is filled in the SAME
  // textureIds order). EXACT decode floor(b*255.0+0.5): byte k -> layer k, no
  // off-by-one (byte 255 = the EMPTY slot marker). The empty-slot guard
  // (< 254.5) now runs on the DECODED value — pre-fix it compared the
  // normalized byte against 254.5 and was always-true (harmless only because
  // empty slots also carry w=0).
  // U-19 FIX (b) — THE BLEND FACTOR (found in the correction round; the
  // DOMINANT cause of the near-black headless render): texelFetch on the RGBA8
  // weight texture ALREADY returns the RAW mask NORMALIZED (mask/255 — the
  // preset's documented lerp factor). The pre-fix shader divided by 255 AGAIN
  // (w0.x / 255.0 = mask/255/255 — a factor 1/255x too small), so every
  // blend collapsed to ~tex*0.004 ≈ black. The factor below is the normalized
  // weight AS FETCHED (w0.x = mask/255 — bit-exact the RAW served byte).
  vec4 s0 = floor(i0 * 255.0 + 0.5); vec4 s1 = floor(i1 * 255.0 + 0.5);
  vec4 s2 = floor(i2 * 255.0 + 0.5); vec4 s3 = floor(i3 * 255.0 + 0.5);
  vec3 col = vec3(0.0);
  bool any = false;
  // slot k: idx from i(k/4)[k%4], weight from w(k/4)[k%4]; RAW mask/255 lerp
  // (sequential mix in SLOT ORDER = the tile's RECORD ORDER)
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
  if (!any) { gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0); return; } // no active layers in this cell (counted client-side; honest void, NOT a fallback color)
  gl_FragColor = vec4(col, 1.0); // SRGB_PASSTHROUGH — no output colorspace chunk (documented preset)
}
`;

/** Dispose the current window's splat GPU resources (bounded memory — called
 * on EVERY window move and on toggle-off). The decoded-texture RGBA LRU
 * survives (bounded) so a window move reuses payloads without re-fetching. */
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

/** Build + apply the textured terrain material for the CURRENT window (the
 * proven chain end-to-end). Returns the honest diagnostic object. On ANY
 * fetch/decode failure the affected layers are SKIPPED with explicit
 * diagnostics (never a fallback texture); if the window cannot be textured
 * at all, the terrain KEEPS the height-palette preview and the banner
 * explains why (loud, honest). */
async function applyTexturesForWindow(origin) {
  if (!state.texturesOn) return null;
  state.mat.busy = true;
  try {
    const t0 = performance.now();
    let grid = state.materialsByOrigin.get(`${origin.gx},${origin.gy}`);
    if (!grid) {
      grid = await fetchMaterialsGrid(origin);
      state.materialsByOrigin.set(`${origin.gx},${origin.gy}`, grid);
      // bounded: keep only the current window's materials grid
      while (state.materialsByOrigin.size > 2) {
        const first = state.materialsByOrigin.keys().next().value;
        if (first === `${origin.gx},${origin.gy}`) break;
        state.materialsByOrigin.delete(first);
      }
    }
    // a null tile row (materials fetch failed) is LOUD: no silent texturing
    const failedTiles = [];
    for (let dy = 0; dy < WINDOW_T; dy++) for (let dx = 0; dx < WINDOW_T; dx++) {
      if (!grid[dy][dx]) failedTiles.push(tileName(origin.gx + dx, origin.gy + dy));
    }
    if (failedTiles.length === WINDOW_T * WINDOW_T) {
      throw new Error(`pobranie materiałów nie udało się dla CAŁEGO okna (${failedTiles.length} kafli) — teren zostaje z paletą wysokości (uczciwie; bez fałszywych tekstur)`);
    }
    // fill failed tiles with EMPTY materials payloads (their layers are
    // skipped + counted — the diagnostic shows which tiles failed)
    const safeGrid = grid.map((row, dy) => row.map((m, dx) => m ?? {
      ok: false, materials: [], fetchFailedTile: tileName(origin.gx + dx, origin.gy + dy),
      _failed: true,
    }));
    const data = buildRegionSplatData(safeGrid);
    // fetch + decode every distinct texture of the window (bounded parallel 4)
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
    // textures that failed fetch/decode: their layers become unresolved —
    // REBUILD the splat data with those ids marked unresolved (explicit
    // diagnostic, layers SKIPPED, never a fallback)
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
    // GPU build (only if at least one texture decoded)
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
      t.magFilter = THREE.NearestFilter; // DISCRETE cells (idx) + RAW per-cell weights (documented choice)
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
    disposeSplat();
    state.splat = { material, arrayTexture, idxTex, wTex, data: splatData, origin, textureIds: usable, decodeFailures, failedTiles };
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
    if (state.texturesOn) {
      banner(`TEKSTURY TERENU: BŁĄD — ${e.message}. Teren renderowany paletą wysokości (bez fałszywych tekstur).`);
    }
    return state.mat.lastDiag;
  } finally {
    state.mat.busy = false;
  }
}

/** Swap the terrain mesh material between the ORIGINAL-TEXTURE splat (toggle
 * ON) and the height-palette preview (toggle OFF) — the REAL toggle (the
 * PIXEL on/off gates measure the difference). */
function applyTerrainMaterial() {
  if (!state.mesh) return;
  const wantSplat = state.texturesOn && state.splat && state.splat.origin.gx === state.windowOrigin?.gx && state.splat.origin.gy === state.windowOrigin?.gy;
  const target = wantSplat ? state.splat.material : state.paletteMaterial;
  if (state.mesh.material !== target) {
    state.mesh.material = target;
    state.mesh.material.wireframe = $('tog-wireframe').checked;
  }
}

// ---- ETAP E: the vegetation subsystem (contract §6 — RECONSTRUCTION_PREVIEW) ----
// The three-way separation labels live in world-vegetation.js /
// PEFoliageLabSeed.js (the single sources of truth, surfaced in the panels).

/** Identity-checked binary fetch for the vegetation chains (CAM-C3 client
 * discipline): the response must carry the expected container identity
 * (era + container + containerSha256 from the LIVE server status) — a
 * mismatch is a controlled refusal (never silently used). */
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
    throw new Error(`${url}: tożsamość kontenera z odpowiedzi nie zgadza się z live statusem (era/kontener/SHA) — kontrolowana odmowa`);
  }
  const payload = new Uint8Array(await r.arrayBuffer());
  return { payload, headers: hdr };
}

/** The vegetation terrain-height sampler (RECONSTRUCTION placement — the
 * deployed foliage-page rule): BILINEAR over the raw u16 samples of the
 * SAME active window region the terrain renders, -> adapter meters
 * (worldHeightMeters — the SAME conversion as the terrain mesh). null
 * outside the active data window (the census shows it; never a fake
 * height). */
function vegHeightSampler(worldX, worldZ) {
  if (!state.region || !state.windowOrigin) return null;
  const lx = (worldX - state.windowOrigin.gx * TILE_M) / PE_TERRAIN_METER_PER_SAMPLE;
  const lz = (worldZ - state.windowOrigin.gy * TILE_M) / PE_TERRAIN_METER_PER_SAMPLE;
  const S = WINDOW_T * 32;
  if (lx < 0 || lz < 0 || lx > S - 1 || lz > S - 1) return null;
  const x0 = Math.min(S - 2, Math.floor(lx)), z0 = Math.min(S - 2, Math.floor(lz));
  const fx = lx - x0, fz = lz - z0;
  const h00 = state.region.rawSample(x0, z0), h10 = state.region.rawSample(x0 + 1, z0);
  const h01 = state.region.rawSample(x0, z0 + 1), h11 = state.region.rawSample(x0 + 1, z0 + 1);
  const raw = h00 * (1 - fx) * (1 - fz) + h10 * fx * (1 - fz) + h01 * (1 - fx) * fz + h11 * fx * fz;
  return worldHeightMeters(raw);
}

/** Build + apply the vegetation for the CURRENT window (async; the initial
 * boot awaits it so READY means the vegetation census is real or honestly
 * diagnosed; window moves rebuild without blocking the terrain). */
async function rebuildVegetation(origin, { awaited = false } = {}) {
  if (!state.vegOn || !state.veg) { state.vegCensus = state.veg ? state.veg.lastCensus : null; return null; }
  if (state.vegBusy) return null;
  state.vegBusy = true;
  try {
    const c = await state.veg.rebuild(origin, WINDOW_T);
    state.vegCensus = c;
    if (c && !c.ok) {
      banner(`ROŚLINNOŚĆ: ${c.error ?? 'błąd łańcucha'} — podgląd roślinności wyłączony uczciwie dla tego profilu (teren działa); wybierz profil zdekodowany.`);
    }
    // NOTE: a successful vegetation build NEVER clears the banner — a terrain
    // error must stay visible (a component success cannot mask another error).
    updateVegPanel();
    updateEvidencePanel();
    return c;
  } finally {
    state.vegBusy = false;
    if (awaited) { /* the caller completes the boot */ }
  }
}

// ---- window management (streaming; ≤64 active tiles) ----
function desiredOrigin(camGx, camGy) {
  return {
    gx: Math.min(Math.max(camGx - (WINDOW_T >> 1), 0), GRID_W - WINDOW_T),
    gy: Math.min(Math.max(camGy - (WINDOW_T >> 1), 0), GRID_H - WINDOW_T),
  };
}
function cameraTile() {
  return {
    gx: Math.min(Math.max(Math.floor(camera.position.x / TILE_M), 0), GRID_W - 1),
    gy: Math.min(Math.max(Math.floor(camera.position.z / TILE_M), 0), GRID_H - 1),
  };
}

function setLoading(msg) { $('world-loading').textContent = msg; }

async function rebuildWindow(origin, { isInitial = false } = {}) {
  state.rebuildBusy = true;
  try {
    const wanted = [];
    for (let dy = 0; dy < WINDOW_T; dy++) {
      for (let dx = 0; dx < WINDOW_T; dx++) wanted.push([origin.gx + dx, origin.gy + dy]);
    }
    // fetch with bounded concurrency (chunks of 8)
    const tiles = [];
    let done = 0, failed = 0;
    for (let i = 0; i < wanted.length; i += 8) {
      const chunk = wanted.slice(i, i + 8);
      const results = await Promise.all(chunk.map(async ([gx, gy]) => {
        try { return { tile: await fetchTile(gx, gy) }; }
        catch (e) { state.fetchErrors++; state.lastError = String(e.message); return { err: e, gx, gy }; }
      }));
      for (const r of results) {
        if (r.err) { failed++; tiles.push(null); }
        else tiles.push(r.tile);
      }
      done += chunk.length;
      if (isInitial || failed > 0) {
        setLoading(`okno 8×8 kafli: ${done}/${wanted.length} pobranych${failed ? `, BŁĘDY: ${failed} (NODATA/odmowa — UJCIWIE)` : ''}`);
      }
    }
    if (failed > 0) {
      // MISSING DATA NEVER BUILDS A MESH OVER VOID: keep the previous mesh (or
      // none on initial), stop movement at the boundary, show the banner.
      state.boundaryHit = true;
      $('boundary-banner').hidden = false;
      if (isInitial) {
        setLoadStatus(`ERROR_TERRAIN_LOAD: ${failed} kafli okna niedostępne — ${state.lastError}`);
        banner(`BŁĄD ŁADOWANIA TERENU: ${state.lastError}`);
      }
      return;
    }
    // assemble rows[gy][gx] (PETerrainRegion contract: rows=y, cols=x)
    const rows = [];
    for (let dy = 0; dy < WINDOW_T; dy++) {
      const row = [];
      for (let dx = 0; dx < WINDOW_T; dx++) row.push(tiles[dy * WINDOW_T + dx]);
      rows.push(row);
    }
    const region = new PETerrainRegion(rows);
    const geo = region.buildGeometry();
    state.lastGeo = geo; // for the tile-bounds toggle rebuild
    // renderer-side (RECONSTRUCTION_PREVIEW): normals + height palette colors
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
    // ETAP D: the material now reflects the texture toggle (the REAL swap —
    // palette preview when OFF, the original-texture splat when ON and this
    // window's splat is applied; until the new window's splat is built the
    // palette shows, honestly, for the moving window)
    applyTerrainMaterial();
    state.mesh.material.wireframe = $('tog-wireframe').checked;
    buildTileBounds(region, geo, origin);
    state.region = region;
    state.windowOrigin = origin;
    state.rebuilds++;
    state.boundaryHit = false;
    $('boundary-banner').hidden = true;
    setLoading(`teren: okno 8×8 (64 kafle aktywne) przy origin ${origin.gx},${origin.gy} — z SUROWYCH próbek u16; przebudowań: ${state.rebuilds}`);
    if (isInitial && !state.firstFrameDone) {
      hud(`teren gotowy — ${geo.positions.length / 3} wierzchołków z surowych u16; tryb: ORBITA (klawisze 1/2/3 zmieniają tryb)`);
    }
    // ETAP D: rebuild THIS window's texture resources (async on window moves;
    // the initial boot awaits the first application so READY means textured
    // or honestly diagnosed)
    if (state.texturesOn && !isInitial) void applyTexturesForWindow(origin);
    // ETAP E: rebuild the vegetation instances for the NEW window (async on
    // moves; per-tile determinism makes the order irrelevant — the census is
    // refreshed when done; the initial build is awaited in boot)
    if (!isInitial) void rebuildVegetation(origin);
  } finally {
    state.rebuildBusy = false;
    if (state.pendingOrigin) {
      const next = state.pendingOrigin;
      state.pendingOrigin = null;
      if (next.gx !== state.windowOrigin?.gx || next.gy !== state.windowOrigin?.gy) {
        void rebuildWindow(next);
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

// tile-bound lines ON THE SURFACE (sample-grid lines at tile borders) — toggle
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

// ---- three.js core ----
const canvas = $('view-canvas');
let renderer, scene, camera, controls;
try {
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
} catch (e) {
  setLoadStatus(`ERROR_WEBGL: ${e.message}`);
  banner(`WebGL niedostępny: ${e.message}`);
  throw e;
}
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
scene = new THREE.Scene();
scene.background = new THREE.Color(0x0c1018);
camera = new THREE.PerspectiveCamera(60, 1, 0.5, 30000);
camera.position.set(0, 200, 0);
const sun = new THREE.DirectionalLight(0xffffff, 1.25);
sun.position.set(0.35, 1.0, 0.2);
scene.add(sun);
scene.add(new THREE.AmbientLight(0x707890, 1.1));
controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.maxDistance = 12000;
// the height-palette preview material (toggle OFF; RECONSTRUCTION_PREVIEW aid —
// the ORIGINAL u16 heights drive it; shared across window rebuilds)
state.paletteMaterial = new THREE.MeshLambertMaterial({ vertexColors: true, side: THREE.DoubleSide });

function syncCanvasSize() {
  const w = canvas.clientWidth || 1, h = canvas.clientHeight || 1;
  renderer.setSize(w, h, false);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
}
window.addEventListener('resize', syncCanvasSize);

// ---- exploration modes (contract §7) ----
const move = { keys: new Set(), yaw: 0, pitch: 0 };
function setMode(mode) {
  state.mode = mode;
  for (const [id, m] of [['btn-mode-orbit', 'orbit'], ['btn-mode-fly', 'fly'], ['btn-mode-walk', 'walk']]) {
    $(id).classList.toggle('active', m === mode);
  }
  controls.enabled = mode === 'orbit';
  if (mode === 'orbit') {
    if (document.pointerLockElement === canvas) document.exitPointerLock();
    if (state.region) {
      const t = camera.position;
      controls.target.set(t.x, groundAt(t.x, t.z) ?? t.y - 50, t.z);
    }
    $('lock-hint').style.display = 'none';
  } else {
    const e = new THREE.Euler().setFromQuaternion(camera.quaternion, 'YXZ');
    move.yaw = e.y; move.pitch = e.x;
    if (mode === 'walk') {
      const g = groundAt(camera.position.x, camera.position.z);
      if (g !== null) camera.position.y = g + EYE_OFFSET_M; // snap to terrain on mode entry
    }
    $('lock-hint').style.display = 'block';
    hud(`${mode === 'walk' ? 'SPACER' : 'LOT'}: kliknij canvas, aby przechwycić mysz (ESC uwalnia); WASD ${mode === 'walk' ? 'po terenie' : '+ Q/E'}; Shift ×3`);
  }
}
canvas.addEventListener('click', () => {
  if (state.mode !== 'orbit' && document.pointerLockElement !== canvas) {
    canvas.requestPointerLock(); // pointer lock ONLY after a conscious click
  }
});
document.addEventListener('pointerlockchange', () => {
  const locked = document.pointerLockElement === canvas;
  hud(locked ? `mysz przechwycona (${state.mode}) — ESC uwalnia kursor` : 'kursor uwolniony');
});
document.addEventListener('mousemove', (ev) => {
  if (document.pointerLockElement !== canvas) return;
  move.yaw -= ev.movementX * 0.0022;
  move.pitch = Math.min(Math.max(move.pitch - ev.movementY * 0.0022, -1.5), 1.5);
});
window.addEventListener('keydown', (ev) => {
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

function groundAt(x, z) {
  if (!state.region || !state.windowOrigin) return null;
  const vx = Math.floor((x - state.windowOrigin.gx * TILE_M) / PE_TERRAIN_METER_PER_SAMPLE);
  const vy = Math.floor((z - state.windowOrigin.gy * TILE_M) / PE_TERRAIN_METER_PER_SAMPLE);
  const sx = WINDOW_T * 32, sy = WINDOW_T * 32;
  if (vx < 0 || vy < 0 || vx >= sx || vy >= sy) return null; // outside the ACTIVE DATA window
  return worldHeightMeters(state.region.rawSample(vx, vy)); // the SAME terrain data
}

const MAP_MIN = 1, MAP_MAX_X = GRID_W * TILE_M - 1, MAP_MAX_Z = GRID_H * TILE_M - 1;
function clampToMap(v) {
  const out = { x: v.x, z: v.z, clamped: false };
  if (out.x < MAP_MIN) { out.x = MAP_MIN; out.clamped = true; }
  if (out.z < MAP_MIN) { out.z = MAP_MIN; out.clamped = true; }
  if (out.x > MAP_MAX_X) { out.x = MAP_MAX_X; out.clamped = true; }
  if (out.z > MAP_MAX_Z) { out.z = MAP_MAX_Z; out.clamped = true; }
  return out;
}

function updateFlyWalk(dt) {
  if (state.mode === 'orbit' || document.pointerLockElement !== canvas) return;
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
  const next = { x: camera.position.x + step.x, z: camera.position.z + step.z };
  const c = clampToMap(next);
  camera.position.x = c.x;
  camera.position.z = c.z;
  if (state.mode === 'walk') {
    const g = groundAt(c.x, c.z);
    if (g === null) {
      // outside the ACTIVE DATA window: STOP the move (never drop into void)
      state.boundaryHit = true;
      $('boundary-banner').hidden = false;
      return;
    }
    camera.position.y = g + EYE_OFFSET_M;
  } else {
    camera.position.y = Math.min(Math.max(camera.position.y + up * speed * dt, 2), 8000);
  }
  camera.quaternion.setFromEuler(new THREE.Euler(move.pitch, move.yaw, 0, 'YXZ'));
  if (c.clamped) { state.boundaryHit = true; $('boundary-banner').hidden = false; }
  else if (state.boundaryHit && !$('boundary-banner').hidden) { state.boundaryHit = false; $('boundary-banner').hidden = true; }
}

function fitView() {
  if (!state.windowOrigin) return;
  const o = state.windowOrigin;
  const cx = (o.gx + WINDOW_T / 2) * TILE_M, cz = (o.gy + WINDOW_T / 2) * TILE_M;
  const g = groundAt(cx, cz) ?? 0;
  if (state.mode === 'orbit') {
    controls.target.set(cx, g, cz);
    camera.position.set(cx + 360, g + 420, cz + 360);
    controls.update();
  } else {
    camera.position.set(cx, g + 240, cz + 240);
  }
  hud('widok dopasowany do okna danych (F)');
}
function resetView() {
  if (!state.spawn) return;
  const s = state.spawn;
  const g = groundAt(s.x, s.z) ?? 0;
  if (state.mode === 'orbit') {
    controls.target.set(s.x, g, s.z);
    camera.position.set(s.x + 180, g + 220, s.z + 180);
    controls.update();
  } else {
    camera.position.set(s.x, (state.mode === 'walk' ? g + EYE_OFFSET_M : g + 120), s.z);
  }
  hud('reset kamery na spawn (R)');
}

// ---- HUD + census panels ----
let censusTimer = 0;
function updateHud(now) {
  const p = camera.position;
  const gx = Math.min(Math.max(Math.floor(p.x / TILE_M), 0), GRID_W - 1);
  const gy = Math.min(Math.max(Math.floor(p.z / TILE_M), 0), GRID_H - 1);
  const lx = Math.min(Math.max(Math.floor((p.x - gx * TILE_M) / PE_TERRAIN_METER_PER_SAMPLE), 0), 31);
  const ly = Math.min(Math.max(Math.floor((p.z - gy * TILE_M) / PE_TERRAIN_METER_PER_SAMPLE), 0), 31);
  let raw = '—';
  if (state.region && state.windowOrigin) {
    const vx = Math.floor((p.x - state.windowOrigin.gx * TILE_M) / PE_TERRAIN_METER_PER_SAMPLE);
    const vy = Math.floor((p.z - state.windowOrigin.gy * TILE_M) / PE_TERRAIN_METER_PER_SAMPLE);
    if (vx >= 0 && vy >= 0 && vx < WINDOW_T * 32 && vy < WINDOW_T * 32) raw = String(state.region.rawSample(vx, vy));
  }
  $('pos-hud').textContent =
    `pozycja (jednostki adaptera — NIE „oryginalne XYZ”): X=${p.x.toFixed(1)} Y=${p.y.toFixed(1)} Z=${p.z.toFixed(1)} m ` +
    `| kafel ${gx}:${gy} (${tileName(gx, gy)}) | próbka (x=${lx}, y=${ly}) | surowe u16=${raw} | tryb: ${{ orbit: 'ORBITA', fly: 'LOT', walk: 'SPACER' }[state.mode]}`;
  if (now - censusTimer > 400) {
    censusTimer = now;
    let cacheBytes = 0; for (const e of state.cache.values()) cacheBytes += e.tile.heights.byteLength;
    let texBytes = 0; for (const e of state.textureRgbaCache.values()) texBytes += e.rgba.byteLength;
    const verts = state.mesh ? state.mesh.geometry.getAttribute('position').count : 0;
    const idx = state.mesh ? state.mesh.geometry.getIndex().count / 3 : 0;
    const d = state.mat.lastDiag;
    const splatLine = !state.texturesOn
      ? 'tekstury terenu: WYŁĄCZONE (paleta wysokości — przełącz włączony, zmienia renderowanie)'
      : state.splat
        ? `tekstury terenu: WŁĄCZONE — materiały resolved ${d?.resolvedLayers ?? 0}/${d?.layersTotal ?? 0} warstw, zdekodowane tekstury ${d?.decoded ?? 0}, zastosowane warstwy ${d?.appliedLayers ?? 0}${d?.unresolvedBindings?.length ? `, DIAGNOSTIC: ${d.unresolvedBindings.length} niepowiązanych (pominięte jawnie)` : ''}${d?.decodeFailures?.length ? `, błędy dekodowania: ${d.decodeFailures.length}` : ''}${d?.cappedCells ? `, komórki z przyciętymi warstwami: ${d.cappedCells}` : ''}`
        : 'tekstury terenu: WŁĄCZONE — buduję łańcuch materiałów/tekstur okna…';
    const vc = state.vegCensus;
    const vegLine = !state.vegOn
      ? 'roślinność: WYŁĄCZONA (przełącz #veg=0; współdzielony cache modeli zachowany)'
      : vc && vc.ok
        ? `roślinność: żądane ${vc.counts.requested} / wyrenderowane ${vc.counts.rendered} / ograniczone ${vc.counts.limited} (twardy limit widocznych ${MAX_VISIBLE_INSTANCES}) | modele: ${vc.models.withInstances} z instancjami (wsparte ${vc.models.supported.length}, bez tekstur ${vc.models.untextured.length}, UNSUPPORTED ${vc.models.unsupported.length})`
        : vc && vc.unsupportedProfile
          ? `roślinność: profil UNSUPPORTED (strict decoder) — ZERO instancji (uczciwie; bez konwersji przecinków)`
          : `roślinność: błąd łańcucha (${state.veg?.lastError ?? '…'}) — uczciwie pokazany`;
    $('world-census').textContent =
      `kafle aktywne (okno 8×8): ${state.region ? WINDOW_T * WINDOW_T : 0} / limit 64\n` +
      `cache klienta: ${state.cache.size} kafli (${(cacheBytes / 1024).toFixed(0)} KiB; limit ${CLIENT_CACHE_MAX})\n` +
      `pobrania: ${state.fetchCount} | błędy: ${state.fetchErrors}${state.lastError ? `\nostatni błąd: ${state.lastError}` : ''}\n` +
      `geometria: ${verts} wierzchołków, ${idx} trójkątów (1 mesh regionu) | przebudowań okna: ${state.rebuilds}\n` +
      `${splatLine}\n` +
      `${vegLine}\n` +
      `cache tekstur RGBA: ${state.textureRgbaCache.size} (${(texBytes / 1024 / 1024).toFixed(1)} MiB; limit ${TEXTURE_CACHE_MAX}) | fetch materiałów: ${state.mat.materialsFetches} (błędy ${state.mat.materialsErrors}) | fetch tekstur: ${state.mat.textureFetches} (błędy ${state.mat.textureErrors})\n` +
      `cache modeli roślinności: ${state.veg ? state.veg.modelCache.size : 0} (współdzielony; limit ${MODEL_CACHE_MAX}) | fetch modeli: ${state.veg ? state.veg.fetchCounters.modelPayloads : 0} | fetch tekstur modeli: ${state.veg ? state.veg.fetchCounters.texturePayloads : 0}\n` +
      `origin okna: ${state.windowOrigin ? `${state.windowOrigin.gx},${state.windowOrigin.gy}` : '—'}`;
    // stream check (window follow) — every census tick is enough (~400 ms)
    const ct = cameraTile();
    const want = desiredOrigin(ct.gx, ct.gy);
    if (state.windowOrigin && (want.gx !== state.windowOrigin.gx || want.gy !== state.windowOrigin.gy)) {
      if (state.rebuildBusy) state.pendingOrigin = want;
      else void rebuildWindow(want);
    }
  }
}

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
    setLoadStatus('READY');
  }
  updateHud(now);
}

// ---- toggles / buttons ----
$('tog-wireframe').addEventListener('change', (ev) => { if (state.mesh) state.mesh.material.wireframe = ev.target.checked; });
$('tog-tilebounds').addEventListener('change', () => {
  if (state.region && state.lastGeo && state.windowOrigin) buildTileBounds(state.region, state.lastGeo, state.windowOrigin);
});
// ETAP D — the REAL terrain-texture toggle: ON builds+applies the window's
// original-texture splat (if not applied yet) and swaps the mesh material;
// OFF swaps back to the height-palette preview. The swap is measured by the
// PIXEL on/off gates — a toggle that changes nothing would FAIL them.
$('tog-textures').addEventListener('change', async (ev) => {
  state.texturesOn = ev.target.checked;
  if (state.texturesOn && state.windowOrigin && !state.splat) {
    hud('buduję tekstury terenu (łańcuch materiał→tekstura)…');
    await applyTexturesForWindow(state.windowOrigin);
  }
  applyTerrainMaterial();
  hud(state.texturesOn ? 'tekstury terenu WŁĄCZONE (oryginalne, z łańcucha id@+16 → <id>.dat; preset RENDER_RECONSTRUCTION)' : 'tekstury terenu WYŁĄCZONE (paleta wysokości)');
});
// ETAP E — the REAL vegetation toggle: ON builds+applies the deterministic
// reconstruction-preview instances (per-tile generation through the
// PEFoliageLabSeed wrapper; the model cache is shared — re-enabling reuses
// it without re-fetching); OFF hides + disposes the per-window instance
// meshes (the shared model cache survives). The swap is measured by the
// PIXEL on/off gates — a toggle that changes nothing would FAIL them.
$('tog-vegetation').addEventListener('change', async (ev) => {
  state.vegOn = ev.target.checked;
  if (state.veg) state.veg.setEnabled(state.vegOn);
  if (state.vegOn && state.veg && state.windowOrigin) {
    hud('buduję podgląd roślinności (deterministyczny wrapper LAB_SEED + oryginalne modele z Models.bnt)…');
    await rebuildVegetation(state.windowOrigin);
  }
  hud(state.vegOn
    ? 'roślinność WŁĄCZONA (RECONSTRUCTION_PREVIEW: profile .vcl + byte-locked RNG + wrapper LAB_SEED; modele ORYGINALNE z łańcucha Models.bnt → NIF → Tekstury)'
    : 'roślinność WYŁĄCZONA (instancje okna zwolnione; współdzielony cache modeli zachowany)');
});
$('btn-mode-orbit').addEventListener('click', () => setMode('orbit'));
$('btn-mode-fly').addEventListener('click', () => setMode('fly'));
$('btn-mode-walk').addEventListener('click', () => setMode('walk'));
$('btn-fit').addEventListener('click', fitView);
$('btn-reset').addEventListener('click', resetView);
$('btn-launcher').addEventListener('click', () => { location.href = '/launcher'; });

// ---- boot ----
async function boot() {
  setLoadStatus('LOADING');
  syncCanvasSize();
  hud('łączę z serwerem świata…');
  state.status = await fetchJson('/api/world/status');
  state.status.identityOf = {
    era: state.status.era,
    container: 'Terrain/terrain.bnt', // the mounted terrain container identity
    containerSha256: state.status.containers.terrain.sha256,
  };
  // anchor: explicit selection or the measured default (data-derived; no city names)
  const anchor = params.anchor ?? (state.status.census.maxMeanTile
    ? { gx: Math.min(state.status.census.maxMeanTile.gridX, GRID_W - 4), gy: Math.min(state.status.census.maxMeanTile.gridY, GRID_H - 4) }
    : { gx: 108, gy: 116 });
  state.anchor = anchor;
  state.spawn = { x: anchor.gx * TILE_M + 128, z: anchor.gy * TILE_M + 128 }; // center of the 4x4 patch
  // ---- ETAP E: the vegetation subsystem (contract §6) ----
  // ORIGINAL_CLIMATE_RECORDS (strict .vcl decode via the API) + the
  // RECOVERED byte-locked RNG chain + the DOCUMENTED LAB_SEED wrapper —
  // VEGETATION_MODE = RECONSTRUCTION_PREVIEW (no historical claims).
  state.veg = new WorldVegetation({
    scene,
    fetchJson,
    fetchBinary: async (url) => {
      if (url.startsWith('/api/world/model/')) {
        return fetchVegBinary(url, { container: 'Models.bnt', containerSha256: state.status?.containers?.models?.sha256 });
      }
      return fetchVegBinary(url, { container: 'Textures.bnt', containerSha256: state.status?.containers?.textures?.sha256 });
    },
    heightSampler: vegHeightSampler,
  });
  await state.veg.setConfig({ profile: params.profile, labSeed: params.seed, densityPercent: params.density });
  updateVegPanel(); // the honest profile/seed panel (rendered from the server + census state)
  updateEvidencePanel();
  setLoading('pobieram okno terenu 8×8 (64 kafle) wokół zaznaczenia…');
  // initial window centered on the anchor's patch
  const origin = desiredOrigin(state.anchor.gx + 1, state.anchor.gy + 1);
  await rebuildWindow(origin, { isInitial: true });
  if (!state.mesh) {
    if (!$('diagnostics').getAttribute('data-load-status').startsWith('ERROR')) {
      setLoadStatus('ERROR_TERRAIN_LOAD: brak mesha po początkowym ładowaniu (uczciwy błąd)');
    }
    return;
  }
  // ---- ETAP D: the original-texture chain for the initial window ----
  // The toggle default state comes from the URL (#textures=0|1; default ON).
  $('tog-textures').checked = state.texturesOn;
  if (state.texturesOn) {
    // the pinned Textures.bnt index becomes READY right after the fail-closed
    // pin verification (~seconds after server boot) — poll BOUNDED (honest
    // timeout: never an infinite READY wait)
    setLoading('czekam na indeks tekstur (weryfikacja pinu Textures.bnt)…');
    const waitT0 = performance.now();
    for (;;) {
      state.status = await fetchJson('/api/world/status');
      const stx = state.status?.containers?.textures;
      if (stx?.indexState === 'READY') break;
      if (performance.now() - waitT0 > 20000) {
        banner(`TEKSTURY TERENU: indeks Textures.bnt niegotowy po 20 s (state: ${stx?.indexState ?? 'nieznany'}) — teren działa z paletą wysokości; tekstury włącz ręcznie po powodzeniu weryfikacji.`);
        state.texturesOn = false;
        $('tog-textures').checked = false;
        break;
      }
      await new Promise((r) => setTimeout(r, 500));
    }
    if (state.texturesOn) {
      setLoading('buduję łańcuch materiały→tekstury okna (maski@record+56 → id@+16 → <id>.dat → TGA2 → RGBA → GPU)…');
      await applyTexturesForWindow(origin);
    }
  }
  // ---- ETAP E: the initial vegetation build (awaited — READY means the
  // vegetation census is REAL or honestly diagnosed; a component failure
  // never disables the terrain but is always shown) ----
  $('tog-vegetation').checked = state.vegOn;
  if (state.vegOn) {
    setLoading('czekam na indeks modeli (weryfikacja pinu Models.bnt)…');
    const waitT0 = performance.now();
    for (;;) {
      state.status = await fetchJson('/api/world/status');
      const stm = state.status?.containers?.models;
      if (stm?.indexState === 'READY') break;
      if (performance.now() - waitT0 > 20000) {
        banner(`ROŚLINNOŚĆ: indeks Models.bnt niegotowy po 20 s (state: ${stm?.indexState ?? 'nieznany'}) — teren działa; roślinność włącz ręcznie po powodzeniu weryfikacji.`);
        state.vegOn = false;
        $('tog-vegetation').checked = false;
        break;
      }
      await new Promise((r) => setTimeout(r, 500));
    }
    if (state.vegOn) {
      setLoading('buduję podgląd roślinności (profil .vcl → wrapper LAB_SEED → instancje → oryginalne modele z Models.bnt + tekstury)…');
      await rebuildVegetation(origin, { awaited: true });
    }
  }
  updateVegPanel();
  updateEvidencePanel(); // with the measured chain census (resolved/decoded/applied)
  resetView();
  animate();
}

/** The vegetation profile/seed panel (ETAP E — „Profil roślinności” +
 * „Seed podglądu”; the THREE-WAY SEPARATION surfaced verbatim; the census
 * from the server's MEASURED default-profile support + this view's own
 * per-model render states). */
function updateVegPanel() {
  const cfg = state.veg?.config;
  const vc = state.vegCensus;
  const sv = state.status?.vegetation;
  const lines = [];
  lines.push(`Profil roślinności: ${cfg?.profile ?? params.profile} | Seed podglądu (LAB_SEED): ${cfg?.labSeed ?? params.seed} | gęstość podglądu: ${cfg?.densityPercent ?? params.density}% | p3 = 0 [P-RNG-P3] (pokazane OSOBNO — nigdy LAB_SEED)`);
  if (sv) {
    lines.push(`VEGETATION_MODE = ${sv.mode} — ${sv.threeWaySeparation.INSTANCE_DISTRIBUTION}`);
    if (sv.defaultProfile) {
      lines.push(`domyślny profil serwera: ${sv.defaultProfile.index} (pomiarowe uzasadnienie: ${sv.defaultProfile.measuredJustification})`);
    }
    if (sv.supportCensusState === 'READY' && sv.supportCensus) {
      const c = sv.supportCensus.counts;
      lines.push(`census wsparcia profilu ${sv.defaultProfile.index}: modele ${c.distinctModels} (wsparte z teksturami ${c.supported}, geometryjnie-bez-tekstur ${c.supportedUntextured}, UNSUPPORTED ${c.unsupported})`);
    }
  }
  if (vc && vc.ok) {
    lines.push(`instancje okna: żądane ${vc.counts.requested} / wyrenderowane ${vc.counts.rendered} / ograniczone ${vc.counts.limited} (twardy limit ${vc.counts.cap})`);
    if (vc.models.untextured.length) {
      lines.push(`modele bez oryginalnych tekstur (uczciwie, bez zamienników): ${vc.models.untextured.map((m) => m.id).join(', ')}`);
    }
    if (vc.models.unsupported.length) {
      lines.push(`modele UNSUPPORTED (znacznik diagnostyczny — NIE oryginalny model): ${vc.models.unsupported.map((m) => m.id).join(', ')}`);
    }
    lines.push(`umiejscowienie: wysokość terenu z TEGO SAMEGO okna (próbkowanie dwuliniowe po surowych u16) — REKONSTRUKCJA (nigdy historyczny placement)`);
  } else if (vc && vc.unsupportedProfile) {
    lines.push(`PROFIL UNSUPPORTED (strict decoder): ${vc.error ?? '—'} — zero instancji; wybierz profil zdekodowany (25.vcl pozostaje UNSUPPORTED — bez konwersji przecinków)`);
  } else if (state.vegOn && !vc) {
    lines.push('łańcuch roślinności: budowanie…');
  } else if (!state.vegOn) {
    lines.push('roślinność WYŁĄCZONA (#veg=0)');
  }
  lines.push(`rozdział (kontrakt §6): ORIGINAL_CLIMATE_RECORDS = dane z przypiętych .vcl (strict); RECOVERED_RNG_ARITHMETIC = nietknięty łańcuch byte-locked PEFoliageCore; INSTANCE_DISTRIBUTION = wrapper PEFoliageLabSeed (LAB_SEED) — rekonstrukcja`);
  $('world-veg').textContent = lines.join('\n');
}

/** The evidence panel (separate from viewer fit/centering — source identity
 * facts + the Etap D chain provenance, refreshed after the chain runs). */
function updateEvidencePanel() {
  const s = state.status;
  const d = state.mat.lastDiag;
  $('world-evidence').textContent = [
    `era: ${s.era} | terrain.bnt SHA256: ${s.containers.terrain.sha256} (pin zweryfikowany fail-closed)`,
    `kalibracja (CURRENT_RUNTIME_CALIBRATION — preset z provenance, NIE fakt historyczny):`,
    `  u16PerMeter=${s.calibration.u16PerMeter}; meterPerSample=${s.calibration.meterPerSample}; min/max=${s.calibration.minMax}`,
    `  konwersja u16→metry zastosowana DOKŁADNIE RAZ w PETerrainRegion.buildGeometry (worldHeightMeters); odwracalna: ×${s.calibration.u16PerMeter}`,
    `topologia inter-tile (wybór renderera, udokumentowany): quady przez granice kafli z SASIEDNICH ORYGINALNYCH próbek;`,
    `  kafle = rozłączne bloki 32×32 (bez nakładania, bez napraw szwów — różnice na granicach to DANE ORYGINALNE);`,
    `  brak zmian wysokości dla maskowania skoku.`,
    `---- ETAP D: łańcuch tekstur terenu (oryginalne) ----`,
    `materiały: rekordy nazwane TDF, maska@record+56 (pola 52..55 = extra4, NIE maska); wagi RAW u8 — sumy >255 to DANE ORYGINALNE (bez normalizacji)`,
    `relacja: id@+16 → "<id>.dat" w Textures.bnt (era PCG_9_3_5; potwierdzona silnikowo — 9.3.5 czyta sub@+16 jako id TEKSTURY materiału; ponownie zweryfikowana na próbkach tego uruchomienia)`,
    `kontener tekstur: Textures.bnt SHA256 ${s.containers.textures.sha256} (pin fail-closed; LAZY indeks ${s.containers.textures.index?.parsedEntries ?? '—'} wpisów; pojedyncze odczyty plików, bez ładowania całego kontenera)`,
    `dekoder: decodeTga2 (TGA 2.0, 24bpp, 256×256, stopka TRUEVISION-XFILE) — TEN SAM moduł produkcyjny po stronie serwera i przeglądarki`,
    d ? `okno: warstwy resolved ${d.resolvedLayers ?? d.resolved ?? 0}/${d.layersTotal ?? 0} | tekstury zdekodowane ${d.decoded ?? 0} | warstwy zastosowane ${d.appliedLayers ?? d.applied ?? 0}${d.unresolvedBindings?.length ? ` | DIAGNOSTIC: ${d.unresolvedBindings.length} niepowiązanych (pominięte jawnie, bez tekstur zastępczych)` : ''}` : `okno: łańcuch tekstur jeszcze niezbudowany`,
    `preset renderowania: RENDER_RECONSTRUCTION — ${RENDER_RECONSTRUCTION_PRESET.blendForm};`,
    `  UV: ${RENDER_RECONSTRUCTION_PRESET.uv}`,
    `  kolejność wierszy: ${RENDER_RECONSTRUCTION_PRESET.rowOrder}`,
    `  próbki komórek: ${RENDER_RECONSTRUCTION_PRESET.cellSampling}`,
    `  przestrzeń barw: ${RENDER_RECONSTRUCTION_PRESET.colorSpace}`,
    `  limity: ${RENDER_RECONSTRUCTION_PRESET.caps}`,
    `normale + paleta kolorów (tryb OFF) = RECONSTRUCTION_PREVIEW (renderer); bajty źródłowe i transformacje sceny (mesh.position = origin×64 m)`,
    `  są oddzielne od dopasowania kamery (fit/centering tylko w kontrolerze kamery).`,
    `---- ETAP E: podgląd roślinności (RECONSTRUCTION_PREVIEW) ----`,
    `trójstopniowy rozdział (kontrakt §6):`,
    `  ORIGINAL_CLIMATE_RECORDS = dane z przypniętych .vcl (strict VegetationClimateDecoder; ${state.status.containers.vegetationClimates.sha256?.slice(0, 16)}…); 25.vcl = UNSUPPORTED (bez konwersji)`,
    `  RECOVERED_RNG_ARITHMETIC = PEFoliageCore (byte-locked; seed FUN_0098cdf0, LCG FUN_0098ce30, lerp FUN_0095ac30, node01=/65535.0 f32; operand lock iter035) — NIETKNIĘTY`,
    `  INSTANCE_DISTRIBUTION = wrapper PEFoliageLabSeed (LAB_SEED-keyed [P-CELLSTREAM] stand-in) — rekonstrukcja (źródło cell stream NIEUSTALENE)`,
    `LAB_SEED = ${state.veg?.config?.labSeed ?? params.seed} (wpływa TYLKO na rekonstrukcyjny cell stream; NIE oryginalny p3; NIE historyczny seed) | p3 = 0 [P-RNG-P3] | viewBand = 10 (STRONGLY_SUPPORTED)`,
    `modele: <id>.nif z przypiętego PCG_9_3_5 Models.bnt (${state.status.containers.models.sha256?.slice(0, 16)}…) → parseWitnessModel (ISTNIEJĄCY kwalifikowany importer; głośne odmowy = uczciwe UNSUPPORTED) → NiTriShape → NiTexturingProperty → NiArkTextureExtraData id → <id>.dat z Textures.bnt → decodeModelTextureStrict (A32 32bpp IMAGE order / TGA2 24bpp) → GPU`,
    `  granice uczciwe: [P-UNITS] cm→m ×0.01 RAZ; [P-AXIS] (x,z,-y); [P-UV] surowe v + flipY=false; [P-SCALE] mostek 2.0/NODE_SCALE_MUL×0.01 (CURRENT_RUNTIME_CALIBRATION — rozmiar NIE historyczny);`,
    `  kształty bez łańcucha texprop→Ark ( Bip01/Box ) = NIE-wizualne (kandydaci kolizji — rola UNVERIFIED; liczone, nie renderowane);`,
    `  łańcuch tekstury nierozwiązywalny (np. DDS poza strict subset) → model renderowany uczciwie BEZ tekstur (diagnostyka; nigdy tekstura zastępcza)`,
    `limit: ${MAX_VISIBLE_INSTANCES} widocznych instancji (twardy) — census żądane/wyrenderowane/ograniczone; determinizm: (era+profil+LAB_SEED+gęstość+kalibracja+tileKey) → TEN SAM zestaw niezależnie od kolejności ładowania`,
    `spawn: kafel ${state.anchor.gx},${state.anchor.gy} (środek zaznaczenia 4×4 z launchera; domyślnie = najwyższa zmierzona średnia — wybór z DANYCH, bez zgadywania nazw miast).`,
    `census terenu: ${s.census.measured}/${s.census.total} zwykłych kafli zmierzonych; NODATA: ${s.census.missing}+${s.census.failed}; sentinel/wiersze specjalne wykluczone.`,
  ].join('\n');
}

boot().catch((e) => {
  setLoadStatus(`ERROR_BOOT: ${e?.message ?? e}`);
  banner(`KRYTYCZNY BŁĄD: ${e?.stack?.split('\n')[0] ?? e}`);
});
