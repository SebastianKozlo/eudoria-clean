// era_divergent.js — MILESTONE 1-E ITER 021 P0 (ERA-DIVERGENT REGION, r185)
// QUESTION: Does the CLEAN pipeline render an ERA-DIVERGENT region — data with
// NO byte-identical historical twin (PCG_9_3_5 material tails differ from the
// JUL_2003 counterparts on every tile of this region) — end-to-end
// byte-faithfully (heights + materials + textures)?
//
// REGION: tiles (100..102 x 100..102), era=PCG_9_3_5. Per the ITER_019
// discovery this region's tiles are NOT payload-identical to JUL 50.bnt
// (the material TAIL differs on every tile; the height blocks happen to be
// identical — recorded per tile by the Node audit, never assumed here).
// The r169 legacy material oracle is therefore HONESTLY N/A for this region
// (legacy splat caches were baked from JUL-era tails; the tails DIFFER here).
//
// CHAIN: pcg_install terrain.bnt + Textures.bnt ORIGINAL BYTES (/pcg/, SHA-pinned)
//   -> PESourceMount (PCG_9_3_5; BNT2_TERRAIN terrain + BNT2 textures)
//   -> getTerrainTile + getTerrainMaterials (canonical, provenance)
//   -> resolveTexture + TgaDecoder (SAME-ERA PCG texture payloads)
//   -> r185 WebGLRenderer, per-tile splat (Stone04-position-0 base + overlays)
//
// BLEND MODEL (iter009 CONFIRMED data model, labels kept honest):
//   color = base texture (position-0 named record);
//   for each overlay in RECORD ORDER: color = mix(color, overlay, w/255).
//   NO normalization (REJECTED corpus-wide) — sums>255 = ORIGINAL DATA.
//   UV scale = world-space repeat (uvRepeat), CURRENT_RUNTIME_CALIBRATION
//   (historical UV scale UNVERIFIED; iter014/iter015 negatives).
//
// r185 PREIMPLEMENTATION CHECKS (pe-threejs-r185 skill, ENTRY #9 §7):
//   - Material.type STATIC (r170): ShaderMaterial used, .type never mutated.
//   - r177 MultiplyBlending premultipliedAlpha: NOT USED (no blending).
//   - flipY/orientation: DataTexture flipY=false; TGA rows pre-flipped at
//     upload (v=0 = image bottom). Mask row 0 <-> tile grid-y row 0. Both
//     orientations UNVERIFIED historically — CURRENT_RUNTIME_CALIBRATION.
//   - color-space: NoColorSpace passthrough (raw texels, no tone mapping).
//   - mip/filter (gate F convention): generateMipmaps=true,
//     minFilter=LinearMipmapLinearFilter, magFilter=LinearFilter — recorded.
//   - matrix/world-transform: static meshes, matrixAutoUpdate default.
//
// REGION DATA (measured in-session before render; era=PCG_9_3_5):
//   max named records per tile = 13 (tile 00650066) -> MAX_OV = 12 overlays,
//   weights packed into 3 RGBA 16x16 textures; sampler budget per material:
//   1 base + 12 overlays + 3 weight = 16 = MAX_TEXTURE_IMAGE_UNITS (measured
//   16 in the ITER 020 failure; 16 <= 16 passes, loud failure if not).
import * as THREE from 'three';
import { PESourceMount } from '../src/pesource/PESourceMount.js';
import { ERAS } from '../src/pesource/PEProvenance.js';
import { PETerrainRegion } from '../src/peworld/PETerrainCore.js';
import { decodeTga2 } from '../src/pesource/TgaDecoder.js';
import { worldHeightMeters, PE_TERRAIN_METER_PER_SAMPLE } from '../src/peworld/PETerrainCore.js';

const HUD = document.getElementById('hud');
const log = (m) => { HUD.textContent = m; console.log(m); };

// ---------- browser I/O adapter ----------
async function fetchBytes(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`fetch ${url}: HTTP ${res.status}`);
  return new Uint8Array(await res.arrayBuffer());
}
async function strictInflate(zlibBytes) {
  const ds = new DecompressionStream('deflate');
  const stream = new Blob([zlibBytes]).stream().pipeThrough(ds);
  return new Uint8Array(await new Response(stream).arrayBuffer());
}
async function sha256Hex(bytes) {
  const d = await crypto.subtle.digest('SHA-256', bytes);
  return [...new Uint8Array(d)].map(b => b.toString(16).padStart(2, '0')).join('').toUpperCase();
}
const io = { readFile: fetchBytes, inflate: strictInflate, sha256: sha256Hex };

// ---------- mounts (SHA-pinned, era-labeled) ----------
const ERA = ERAS.PCG_9_3_5; // era label carried on EVERY artifact below
const mount = new PESourceMount(io);
log('mounting PCG_9_3_5 terrain.bnt + Textures.bnt…');
await mount.mountEra({ era: ERA, container: 'Terrain/terrain.bnt',
  path: '/pcg/Data/Terrain/terrain.bnt', format: 'BNT2_TERRAIN', verifyHash: true });
await mount.mountEra({ era: ERA, container: 'Textures.bnt',
  path: '/pcg/Data/Textures/Textures.bnt', format: 'BNT2', verifyHash: true });
log('mounted + SHA-verified (terrain 95841761…, textures 61ACD13B…).');

// ---------- canonical tiles + materials through the clean chain ----------
const ORIGIN_X = 100, ORIGIN_Y = 100, N = 3;
const tiles = [];
for (let ty = ORIGIN_Y; ty < ORIGIN_Y + N; ty++) {
  const row = [];
  for (let tx = ORIGIN_X; tx < ORIGIN_X + N; tx++) {
    row.push(await mount.getTerrainTile({ era: ERA, gridX: tx, gridY: ty }));
  }
  tiles.push(row);
}
log(`decoded 9 canonical tiles (${tiles[0][0].name} .. ${tiles[2][2].name}), era=${ERA}.`);

// seam diagnostic + provenance via the PE Runtime Core (disjoint tiles =
// ORIGINAL DATA, NO repair — recorded, never fixed)
const regionCore = new PETerrainRegion(tiles);

// per-tile heights sha256 (u16le of the 32x32 block) + relief stats
const u16le = (h) => { const b = new Uint8Array(2048); const dv = new DataView(b.buffer);
  for (let i = 0; i < 1024; i++) dv.setUint16(i * 2, h[i], true); return b; };
const tileHeights = [];
for (let ty = 0; ty < N; ty++) for (let tx = 0; tx < N; tx++) {
  const t = tiles[ty][tx];
  let mn = 65535, mx = 0;
  for (const v of t.heights) { if (v < mn) mn = v; if (v > mx) mx = v; }
  tileHeights.push({
    name: t.name, era: ERA,
    heightsSha256: await sha256Hex(u16le(t.heights)),
    reliefU16: { min: mn, max: mx, relief: mx - mn },
  });
}

// material decode per tile (clean chain) — explicit denominators
const tileMaterials = [];
for (let ty = 0; ty < N; ty++) {
  const row = [];
  for (let tx = 0; tx < N; tx++) {
    const dec = await mount.getTerrainMaterials({ era: ERA, gridX: ORIGIN_X + tx, gridY: ORIGIN_Y + ty });
    if (!dec.provenance.extra.tailConsumedExactly) throw new Error('tail not consumed exactly');
    row.push(dec);
  }
  tileMaterials.push(row);
}
const totalNamed = tileMaterials.flat().reduce((s, d) => s + d.materials.length, 0);
log(`material tails decoded: 9/9 exact; ${totalNamed} named material records (era=${ERA}).`);

// per-tile material census (era-labeled, explicit denominators)
const materialCensus = [];
for (let ty = 0; ty < N; ty++) for (let tx = 0; tx < N; tx++) {
  const dec = tileMaterials[ty][tx];
  const base = dec.materials[0];
  materialCensus.push({
    tile: tiles[ty][tx].name, era: ERA,
    tailConsumedExactly: dec.provenance.extra.tailConsumedExactly,
    recordCountTotal: dec.provenance.extra.recordCount,
    namedMaterialCount: dec.provenance.extra.namedMaterialCount,
    systemRecordCount: dec.provenance.extra.systemRecordCount,
    base: { id: base.id, name: base.name, encoding: base.maskEncoding,
      baseAll255: Array.from(base.mask).every((v) => v === 255) },
    records: [],
    sums: dec.sums, // sums>255 tolerated as ORIGINAL DATA (normalization REJECTED)
  });
  for (const m of dec.materials) {
    materialCensus[materialCensus.length - 1].records.push({
      position: m.position, id: m.id, name: m.name, encoding: m.maskEncoding,
      size: m.size, maskSha256: await sha256Hex(m.mask),
    });
  }
}

// ---------- texture binding (same-era PCG payloads via resolveTexture) ----------
const idSet = new Map(); // id -> {texture, provenance, payloadSha, name, width, height, maskWeightsForProbe}
for (const dec of tileMaterials.flat()) {
  for (const m of dec.materials) {
    if (!idSet.has(m.id)) idSet.set(m.id, { name: m.name });
  }
}
let fallbacks = 0;
const fallbackCensus = [];
for (const [id, info] of idSet) {
  let res;
  try {
    res = await mount.resolveTexture({ era: ERA, container: 'Textures.bnt', textureId: id });
  } catch (e) {
    // EXPLICIT era-labeled fallback decision (no silent substitution)
    fallbacks++;
    fallbackCensus.push({ id, reason: String(e.message ?? e), decision:
      'NO_SUBSTITUTION — missing same-era texture would be recorded and rendered absent' });
    throw new Error(`texture id ${id} unresolved in PCG_9_3_5 Textures.bnt — no silent fallback`);
  }
  let dec;
  try {
    dec = decodeTga2(res.payload); // loud-failure validated TGA2 subset
  } catch (e) {
    fallbacks++;
    fallbackCensus.push({ id, reason: `TGA decode: ${String(e.message ?? e)}`, decision:
      'NO_SUBSTITUTION — decode failure recorded, no cross-era fallback' });
    throw new Error(`texture id ${id} TGA decode failed — no silent fallback`);
  }
  const payloadSha = await sha256Hex(res.payload);
  const { width, height, rgba } = dec;
  const flipped = new Uint8Array(rgba.length);
  for (let y = 0; y < height; y++) {
    flipped.set(rgba.subarray((height - 1 - y) * width * 4, (height - y) * width * 4), y * width * 4);
  }
  const tex = new THREE.DataTexture(flipped, width, height, THREE.RGBAFormat);
  tex.colorSpace = THREE.NoColorSpace; // passthrough calibration (see header)
  tex.generateMipmaps = true;
  tex.minFilter = THREE.LinearMipmapLinearFilter;
  tex.magFilter = THREE.LinearFilter;
  tex.wrapS = THREE.RepeatWrapping;
  tex.wrapT = THREE.RepeatWrapping;
  tex.flipY = false;
  tex.needsUpdate = true;
  Object.assign(info, { texture: tex, provenance: res.provenance, payloadSha, width, height });
}
log(`textures bound: ${idSet.size} distinct ids, same-era PCG payloads, TGA2 decode 0 failures, 0 fallbacks.`);

// ---------- per-tile splat meshes (MAX_OV = 12, 3 packed weight textures) ----------
const UV_REPEAT = 8;  // world meters per texture repeat — CURRENT_RUNTIME_CALIBRATION (UNVERIFIED)
const MAX_OV = 12;    // region max named = 13 (tile 00650066) -> 12 overlays
const BLACK = new THREE.DataTexture(new Uint8Array([0, 0, 0, 255]), 1, 1, THREE.RGBAFormat);
BLACK.flipY = false; BLACK.needsUpdate = true;

const scene = new THREE.Scene();

function weightTextures(masks) {
  // pack up to 12 weight maps (16x16) into THREE RGBA textures (4 overlays each)
  const packs = [new Uint8Array(16 * 16 * 4), new Uint8Array(16 * 16 * 4), new Uint8Array(16 * 16 * 4)];
  for (let i = 0; i < Math.min(masks.length, MAX_OV); i++) {
    const dst = packs[i >> 2], ch = i & 3;
    for (let p = 0; p < 256; p++) dst[p * 4 + ch] = masks[i][p];
  }
  return packs.map((data) => {
    const t = new THREE.DataTexture(data, 16, 16, THREE.RGBAFormat);
    t.magFilter = THREE.NearestFilter;  // discrete weights — no interpolation
    t.minFilter = THREE.NearestFilter;
    t.wrapS = THREE.ClampToEdgeWrapping;
    t.wrapT = THREE.ClampToEdgeWrapping;
    t.flipY = false;
    t.needsUpdate = true;
    return t;
  });
}

const tileShaderInfo = [];
for (let ty = 0; ty < N; ty++) {
  for (let tx = 0; tx < N; tx++) {
    const tile = tiles[ty][tx];
    const dec = tileMaterials[ty][tx];
    const named = dec.materials;
    const base = named[0];
    if (!base) throw new Error(`tile ${tile.name}: no named material`);
    const overlays = named.slice(1, 1 + MAX_OV);
    if (named.length - 1 > MAX_OV) throw new Error(`tile ${tile.name}: ${named.length - 1} overlays > MAX_OV`);

    const S = 32;
    const positions = new Float32Array(S * S * 3);
    for (let y = 0; y < S; y++) {
      for (let x = 0; x < S; x++) {
        const i = (y * S + x) * 3;
        positions[i] = (ORIGIN_X + tx) * S * PE_TERRAIN_METER_PER_SAMPLE + x * PE_TERRAIN_METER_PER_SAMPLE;
        positions[i + 1] = worldHeightMeters(tile.heights[y * S + x]);
        positions[i + 2] = (ORIGIN_Y + ty) * S * PE_TERRAIN_METER_PER_SAMPLE + y * PE_TERRAIN_METER_PER_SAMPLE;
      }
    }
    const indices = new Uint32Array((S - 1) * (S - 1) * 6);
    let q = 0;
    for (let y = 0; y < S - 1; y++) {
      for (let x = 0; x < S - 1; x++) {
        const a = y * S + x, b = a + 1, c = a + S, d = c + 1;
        indices[q++] = a; indices[q++] = c; indices[q++] = b;
        indices[q++] = b; indices[q++] = c; indices[q++] = d;
      }
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    g.setIndex(new THREE.BufferAttribute(indices, 1));
    g.computeVertexNormals();

    const uniforms = {
      uBase: { value: idSet.get(base.id).texture },
      uOvCount: { value: overlays.length },
      uVRepeat: { value: UV_REPEAT },
      uOvTex: { value: [] },
      uW: { value: [] },
    };
    for (let i = 0; i < MAX_OV; i++) {
      const ov = overlays[i] ?? null;
      uniforms.uOvTex.value.push(ov ? idSet.get(ov.id).texture : BLACK);
    }
    uniforms.uW.value = weightTextures(overlays.map((o) => o.mask));

    const material = new THREE.ShaderMaterial({
      uniforms,
      vertexShader: `
        varying vec3 vWorld;
        varying vec2 vCell;
        void main() {
          vWorld = position.xyz;
          vec2 tileOrigin = vec2(${(ORIGIN_X + tx) * 64}.0, ${(ORIGIN_Y + ty) * 64}.0);
          vCell = (position.xz - tileOrigin) / 64.0;
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }`,
      fragmentShader: `
        precision highp float;
        uniform sampler2D uBase;
        uniform sampler2D uOvTex[${MAX_OV}];
        uniform sampler2D uW[3];
        uniform int uOvCount;
        uniform float uVRepeat;
        varying vec3 vWorld;
        varying vec2 vCell;
        void main() {
          vec2 uv = vWorld.xz / uVRepeat;
          vec3 color = texture2D(uBase, uv).rgb;
          // unrolled: GLSL ES 1.00 requires constant sampler indices
          if (uOvCount > 0)  { float w = texture2D(uW[0], vCell).r; if (w > 0.0) color = mix(color, texture2D(uOvTex[0], uv).rgb, w / 255.0); }
          if (uOvCount > 1)  { float w = texture2D(uW[0], vCell).g; if (w > 0.0) color = mix(color, texture2D(uOvTex[1], uv).rgb, w / 255.0); }
          if (uOvCount > 2)  { float w = texture2D(uW[0], vCell).b; if (w > 0.0) color = mix(color, texture2D(uOvTex[2], uv).rgb, w / 255.0); }
          if (uOvCount > 3)  { float w = texture2D(uW[0], vCell).a; if (w > 0.0) color = mix(color, texture2D(uOvTex[3], uv).rgb, w / 255.0); }
          if (uOvCount > 4)  { float w = texture2D(uW[1], vCell).r; if (w > 0.0) color = mix(color, texture2D(uOvTex[4], uv).rgb, w / 255.0); }
          if (uOvCount > 5)  { float w = texture2D(uW[1], vCell).g; if (w > 0.0) color = mix(color, texture2D(uOvTex[5], uv).rgb, w / 255.0); }
          if (uOvCount > 6)  { float w = texture2D(uW[1], vCell).b; if (w > 0.0) color = mix(color, texture2D(uOvTex[6], uv).rgb, w / 255.0); }
          if (uOvCount > 7)  { float w = texture2D(uW[1], vCell).a; if (w > 0.0) color = mix(color, texture2D(uOvTex[7], uv).rgb, w / 255.0); }
          if (uOvCount > 8)  { float w = texture2D(uW[2], vCell).r; if (w > 0.0) color = mix(color, texture2D(uOvTex[8], uv).rgb, w / 255.0); }
          if (uOvCount > 9)  { float w = texture2D(uW[2], vCell).g; if (w > 0.0) color = mix(color, texture2D(uOvTex[9], uv).rgb, w / 255.0); }
          if (uOvCount > 10) { float w = texture2D(uW[2], vCell).b; if (w > 0.0) color = mix(color, texture2D(uOvTex[10], uv).rgb, w / 255.0); }
          if (uOvCount > 11) { float w = texture2D(uW[2], vCell).a; if (w > 0.0) color = mix(color, texture2D(uOvTex[11], uv).rgb, w / 255.0); }
          gl_FragColor = vec4(color, 1.0);
        }`,
    });
    const mesh = new THREE.Mesh(g, material);
    scene.add(mesh);
    tileShaderInfo.push({
      tile: tile.name, era: ERA,
      base: { id: base.id, name: base.name, encoding: base.maskEncoding },
      baseAll255: Array.from(base.mask).every((v) => v === 255),
      overlayCount: overlays.length,
      overlays: overlays.map((o) => ({ id: o.id, name: o.name, encoding: o.maskEncoding })),
    });
  }
}

// ---------- r185 render (deterministic, unlit) ----------
const W = 1024, H = 768;
const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1);
renderer.setSize(W, H);
renderer.setClearColor(0x0a0a12, 1);
document.getElementById('view').appendChild(renderer.domElement);

const box = new THREE.Box3();
for (const m of scene.children) {
  const pos = m.geometry.getAttribute('position');
  for (let i = 0; i < pos.count; i++) box.expandByPoint(new THREE.Vector3().fromBufferAttribute(pos, i));
}
const center = box.getCenter(new THREE.Vector3());
const size = box.getSize(new THREE.Vector3());
const camera = new THREE.PerspectiveCamera(55, W / H, 1, 50000);
camera.up.set(0, 1, 0);
camera.position.set(center.x + size.x * 0.9, box.max.y + size.z * 0.75, center.z + size.z * 1.15);
camera.lookAt(center.x, center.y, center.z);

renderer.render(scene, camera);
const png1 = renderer.domElement.toDataURL('image/png');
const hash1 = await sha256Hex(Uint8Array.from(atob(png1.split(',')[1]), c => c.charCodeAt(0)));
renderer.render(scene, camera);
const png2 = renderer.domElement.toDataURL('image/png');
const hash2 = await sha256Hex(Uint8Array.from(atob(png2.split(',')[1]), c => c.charCodeAt(0)));

// ---------- per-tile probe points (tile center sample; known cell + dominant material) ----------
const probeCanvas = document.createElement('canvas');
probeCanvas.width = W; probeCanvas.height = H;
const pctx = probeCanvas.getContext('2d', { willReadFrequently: true });
pctx.drawImage(renderer.domElement, 0, 0);
function sampleCanvas(x, y) {
  const d = pctx.getImageData(Math.min(W - 1, Math.max(0, x)), Math.min(H - 1, Math.max(0, y)), 1, 1).data;
  return [d[0], d[1], d[2]];
}
const pixelProbe = [];
for (let ty = 0; ty < N; ty++) {
  for (let tx = 0; tx < N; tx++) {
    const S = 32, MPS = PE_TERRAIN_METER_PER_SAMPLE;
    const sx = 16, sy = 16; // tile-center sample
    const world = new THREE.Vector3(
      (ORIGIN_X + tx) * S * MPS + sx * MPS,
      worldHeightMeters(tiles[ty][tx].heights[sy * S + sx]),
      (ORIGIN_Y + ty) * S * MPS + sy * MPS);
    const ndc = world.clone().project(camera);
    const cx = Math.round((ndc.x * 0.5 + 0.5) * W), cy = Math.round((-ndc.y * 0.5 + 0.5) * H);
    // dominant material at the containing mask cell (16x16 mask; sample 16 -> cell 8)
    const cellX = sx >> 1, cellY = sy >> 1, ci = cellY * 16 + cellX;
    const dec = tileMaterials[ty][tx];
    let dom = null;
    for (const m of dec.materials) {
      const w = m.mask[ci];
      if (!dom || w > dom.weight) dom = { id: m.id, name: m.name, weight: w };
    }
    pixelProbe.push({
      tile: tiles[ty][tx].name, era: ERA,
      world: [world.x, world.y, world.z], canvasPos: [cx, cy],
      maskCell: [cellX, cellY],
      dominantMaterial: dom,
      rgb: sampleCanvas(cx, cy),
    });
  }
}

// ---------- results / provenance chain (era-labeled throughout) ----------
const binding = [];
for (const [id, info] of idSet) {
  binding.push({
    id, name: info.name, era: ERA,
    container: info.provenance.container, entry: info.provenance.entry,
    payloadSha256: info.payloadSha,
    sameEraAsCleanRuntimePrimary: info.provenance.extra.sameEraAsCleanRuntimePrimary,
    decodedSize: `${info.width}x${info.height}`,
  });
}
const result = {
  iter: 'ITER_021',
  era: ERA,
  p0: 'era-divergent region through the clean pipeline (heights + materials + textures, PCG_9_3_5 primary, zero legacy runtime input)',
  chain: 'terrain.bnt+Textures.bnt bytes -> PESourceMount -> TerrainTile+materials -> TgaDecoder -> r185 splat render',
  region: { originGridX: ORIGIN_X, originGridY: ORIGIN_Y, tilesX: N, tilesY: N, era: ERA,
    eraDivergenceNote: 'per-tile JUL_2003 twin census (payload/heights/tail equality) is measured by the Node audit tools/iter021_era_byte_audit.js; the r169 material oracle is HONESTLY N/A for this region (legacy splat caches were baked from JUL-era tails which differ here)' },
  mount: { era: ERA, terrainHashVerified: true, texturesHashVerified: true },
  heights: {
    era: ERA, tiles: 9,
    perTile: tileHeights,
    seamDiagnostic: regionCore.tileSeamDiagnostic,
  },
  materialDenominators: {
    era: ERA, tiles: 9, namedRecordsTotal: totalNamed,
    distinctMaterialIds: idSet.size,
    perTileNamedCounts: tileShaderInfo.map((t) => `${t.tile}:${t.overlayCount + 1}`),
    encodings: ['raw', 'rle_cv'],
  },
  blendModel: {
    base: 'position-0 named record (whatever the data says — Stone04-base rule RE-CHECKED per tile on this era-divergent region)',
    overlays: 'sequential mix by w/255 in RECORD ORDER',
    normalization: 'REJECTED (sums>255 tolerated as ORIGINAL DATA)',
    uvRepeat: UV_REPEAT, uvScaleStatus: 'CURRENT_RUNTIME_CALIBRATION (historical UNVERIFIED)',
  },
  renderer: {
    threeRevision: THREE.REVISION, backend: 'WebGLRenderer', width: W, height: H,
    colorSpace: 'NoColorSpace passthrough (raw texels, no tone mapping)',
    mipmapConfig: 'generateMipmaps=true, min=LinearMipmapLinear, mag=Linear',
    weightFilter: 'Nearest (discrete 16x16 data, no interpolation)',
  },
  screenshotPngSha256: hash1, screenshotDeterministicInPage: hash1 === hash2,
  pixelProbe,
  tileBindings: tileShaderInfo,
  materialCensus,
  textureBindings: binding,
  textureFallbackCensus: { fallbacks, census: fallbackCensus, decision: 'ANY missing id => era-labeled EXPLICIT decision, NO silent cross-era substitution' },
  provenanceCount: 9 + totalNamed + idSet.size,
};
window.__ERA__ = result;
window.__ERA_PNG__ = png1;
log(
`P0 ERA-DIVERGENT REGION RENDERED — 9 tiles, ${totalNamed} material records, ${idSet.size} textures bound (same-era PCG)
screenshot sha256: ${hash1} (deterministic in-page: ${hash1 === hash2})
base rule per tile: see materialCensus; normalization REJECTED (sums>255 = original data)`);
