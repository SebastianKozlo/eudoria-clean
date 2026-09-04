// materials_wsum.js â€” M1 ITER 039 / ledger ITER_025 BOUNDED SECONDARY v2
// (CLEAN RUNTIME FIDELITY REWORK â€” TERRAIN_14 REAL BLEND SEMANTICS, DUAL FACTOR CANDIDATES)
//
// QUESTION: Can the proven 9-tile region render through the CLEAN pipeline with
// the REAL 9.3.5 terrain blend (TERRAIN_14: weighted-sum splat + OVERLAY),
// replacing the FALSIFIED sequential-mix calibration of terrain/materials.js?
//
// SOURCE ANCHORS (era PCG_9_3_5, evidence iter024_fx_id_0x3ea_Terrain_14.hlsl):
//   - technique Terrain_14 (ps.1.4 + vs_1_1) extracted byte-faithfully from the
//     ORIGINAL materials.vfs (SHA 5AE4AF81...): blend D = d0*w0 + d1*w1 + d2*w2
//     with w = factor-texture RGB (u8/255, NO in-shader renormalization), then
//     per-channel OVERLAY onto the base keyed on D (D>=0.5: 1-2(1-b)(1-D),
//     else 2*b*D), then light/shadow/fog (NOT implemented here â€” UNLIT
//     deterministic calibration, labeled).
//   - texture states CONFIRMED verbatim: base+factor CLAMP/LINEAR/LINEAR/POINT-mip;
//     details WRAP/LINEAR/LINEAR/LINEAR with MipMapLodBias=-0.5 (LOD bias is NOT
//     EXPRESSIBLE in r185 â€” recorded, not faked).
//   - vertex stage: ONE patch-local texcoord for all 5 samplers; details repeat
//     32/32/16 within the patch.
//
// DUAL FACTOR-CONTENT CANDIDATES (v2 â€” honest, because the >4-material factor
// BAKE is UNRESOLVED; see iter025_census.json + iter025_reduction_analysis.json):
//   ROW "raw"  (C1-raw):  factor RGB = the raw TDF mask u8 weights of the top-3
//          overlays (unrenormalized). RESULT: where overlays overlap with large
//          weights (sums > 255 in 253/256 cells of some region-B tiles; several
//          region-A tiles carry TWO all-255 full-coverage overlays), D exceeds
//          1.0 and the historical overlay op SATURATES TO WHITE. This is the
//          shader's own behavior with unrenormalized inputs â€” the finding WEAKENS
//          the raw-mask factor-content model as the engine's bake.
//   ROW "norm" (C1n):     factor RGB = per-cell RENORMALIZED top-3 weights
//          (w_k' = round(w_k*255/sum) when sum > 255; raw otherwise). A
//          bake-side normalization candidate (the shader itself never divides).
//   NEITHER candidate is claimed as the engine's mechanism (UNVERIFIED).
//
// HONEST LABELS (anti-success-theater):
//   - REDUCTION = TOP3_TOTAL_WEIGHT: the >4-material reduction mechanism of the
//     real engine is UNRESOLVED (iter025: TerrainImageCache1/2.vfs are
//     runtime-created EMPTY ArkVFS02 caches, 0 records; the exe-side bake
//     function was not located). CURRENT_RUNTIME_CALIBRATION.
//   - FACTOR SOURCE: TerrainImageCache factor textures DO NOT EXIST in any
//     shipped/install state (16-byte empty headers), so the factor textures here
//     are DERIVED from the CONFIRMED TDF masks (dim=16 RAW/RLE, iter008b).
//   - Vertex UV mapping (patch-local 0..1 per TDF tile) = CURRENT_RUNTIME_CALIBRATION
//     (the 9.3.5 mesh UV generation is UNVERIFIED; PE2 facts era-invalid here).
//   - NO claim of matching r169 legacy visuals (oracle = comparison only).
//
// r185 PREIMPLEMENTATION CHECKS (pe-threejs-r185 skill, ENTRY #9 Â§7):
//   - Material.type STATIC (r170): ShaderMaterial, .type never mutated.
//   - r177 MultiplyBlending premultipliedAlpha: NOT USED.
//   - DataTexture flipY=false everywhere; color-space NoColorSpace passthrough;
//     matrix/world-transform: static meshes, matrixAutoUpdate default.
import * as THREE from 'three';
import { PESourceMount } from '../src/pesource/PESourceMount.js';
import { ERAS } from '../src/pesource/PEProvenance.js';
import { PETerrainRegion, PE_TERRAIN_METER_PER_SAMPLE } from '../src/peworld/PETerrainCore.js';
import { decodeTga2 } from '../src/pesource/TgaDecoder.js';
import { worldHeightMeters } from '../src/peworld/PETerrainCore.js';

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

// ---------- mounts (SHA-pinned, era-labeled; same chain as iter020) ----------
const mount = new PESourceMount(io);
log('mounting PCG_9_3_5 terrain.bnt + Textures.bntâ€¦');
await mount.mountEra({ era: ERAS.PCG_9_3_5, container: 'Terrain/terrain.bnt',
  path: '/pcg/Data/Terrain/terrain.bnt', format: 'BNT2_TERRAIN', verifyHash: true });
await mount.mountEra({ era: ERAS.PCG_9_3_5, container: 'Textures.bnt',
  path: '/pcg/Data/Textures/Textures.bnt', format: 'BNT2', verifyHash: true });
log('mounted + SHA-verified (terrain 95841761â€¦, textures 61ACD13Bâ€¦).');

// ---------- canonical tiles + materials (proven 9-tile region) ----------
const ORIGIN_X = 56, ORIGIN_Y = 112, N = 3;
const tiles = [];
for (let ty = ORIGIN_Y; ty < ORIGIN_Y + N; ty++) {
  const row = [];
  for (let tx = ORIGIN_X; tx < ORIGIN_X + N; tx++) {
    row.push(await mount.getTerrainTile({ era: ERAS.PCG_9_3_5, gridX: tx, gridY: ty }));
  }
  tiles.push(row);
}
const region = new PETerrainRegion(tiles);
log(`decoded 9 canonical tiles (${tiles[0][0].name} .. ${tiles[2][2].name}).`);

const tileMaterials = [];
for (let ty = 0; ty < N; ty++) {
  const row = [];
  for (let tx = 0; tx < N; tx++) {
    const dec = await mount.getTerrainMaterials({
      era: ERAS.PCG_9_3_5, gridX: ORIGIN_X + tx, gridY: ORIGIN_Y + ty });
    if (!dec.provenance.extra.tailConsumedExactly) throw new Error('tail not consumed exactly');
    row.push(dec);
  }
  tileMaterials.push(row);
}
const totalNamed = tileMaterials.flat().reduce((s, d) => s + d.materials.length, 0);
log(`material tails decoded: 9/9 exact; ${totalNamed} named material records.`);

// ---------- texture binding (CONFIRMED TERRAIN_14 sampler states) ----------
// TERRAIN_14 states (iter024 verbatim): base+factor CLAMP/LINEAR/LINEAR/POINT-mip;
// details WRAP/LINEAR/LINEAR/LINEAR, LOD bias -0.5 (not expressible in r185).
function makeTexture(rgba, width, height, { wrap, mipmap }) {
  const tex = new THREE.DataTexture(rgba, width, height, THREE.RGBAFormat);
  tex.colorSpace = THREE.NoColorSpace;
  tex.generateMipmaps = true;
  tex.magFilter = THREE.LinearFilter;
  tex.minFilter = mipmap === 'point' ? THREE.LinearMipmapNearestFilter : THREE.LinearMipmapLinearFilter;
  tex.wrapS = wrap;
  tex.wrapT = wrap;
  tex.flipY = false;
  tex.needsUpdate = true;
  return tex;
}
function flipVertical(rgba, width, height) {
  const flipped = new Uint8Array(rgba.length);
  for (let y = 0; y < height; y++) {
    flipped.set(rgba.subarray((height - 1 - y) * width * 4, (height - y) * width * 4), y * width * 4);
  }
  return flipped;
}

const idSet = new Map();
for (const dec of tileMaterials.flat()) {
  for (const m of dec.materials) {
    if (!idSet.has(m.id)) idSet.set(m.id, { name: m.name });
  }
}
for (const [id, info] of idSet) {
  const res = await mount.resolveTexture({ era: ERAS.PCG_9_3_5, container: 'Textures.bnt', textureId: id });
  const dec = decodeTga2(res.payload);
  const payloadSha = await sha256Hex(res.payload);
  const flipped = flipVertical(dec.rgba, dec.width, dec.height);
  const tex = makeTexture(flipped, dec.width, dec.height, { wrap: THREE.RepeatWrapping, mipmap: 'linear' });
  Object.assign(info, { texture: tex, provenance: res.provenance, payloadSha, width: dec.width, height: dec.height });
}
log(`textures bound: ${idSet.size} distinct ids, same-era PCG payloads, TGA2 decode 0 failures.`);

// per-tile CLAMPED base texture views (base sampled once per patch, CLAMP state)
const baseTexById = new Map();
for (const [id, info] of idSet) {
  const res = await mount.resolveTexture({ era: ERAS.PCG_9_3_5, container: 'Textures.bnt', textureId: id });
  const dec = decodeTga2(res.payload);
  const flipped = flipVertical(dec.rgba, dec.width, dec.height);
  baseTexById.set(id, makeTexture(flipped, dec.width, dec.height, { wrap: THREE.ClampToEdgeWrapping, mipmap: 'point' }));
}

// ---------- dual-row meshes with TERRAIN_14 blend ----------
const scene = new THREE.Scene();
const S = 32;
const DETAIL_REPEAT = [32.0, 32.0, 16.0]; // CONFIRMED vertex-stage repeats (iter024)
const COLUMN_X_OFFSET = 200;               // world meters between the two candidate columns (side by side in X)
const tileResults = [];

function selectTop3(overlays) {
  // REDUCTION CANDIDATE C1 (TOP3_TOTAL_WEIGHT) â€” deterministic, UNVERIFIED.
  const idx = overlays.map((o, i) => ({ i, total: o.mask.reduce((s, v) => s + v, 0) }));
  idx.sort((a, b) => (b.total - a.total) || (a.i - b.i));
  return idx.slice(0, 3).map((e) => e.i);
}

function factorTexture(sel, overlays, normalized) {
  // factor 16x16 RGB = 3 selected per-cell weights (u8). C1-raw: raw masks.
  // C1n: per-cell renormalized (w_k'=round(w_k*255/sum)) ONLY where sum>255.
  const data = new Uint8Array(16 * 16 * 4);
  let renormCells = 0;
  for (let p = 0; p < 256; p++) {
    const w = [0, 1, 2].map((k) => (overlays[sel[k]] ? overlays[sel[k]].mask[p] : 0));
    if (normalized) {
      const s = w[0] + w[1] + w[2];
      if (s > 255) {
        for (let k = 0; k < 3; k++) w[k] = Math.round((w[k] * 255) / s);
        renormCells++;
      }
    }
    data[p * 4] = w[0]; data[p * 4 + 1] = w[1]; data[p * 4 + 2] = w[2]; data[p * 4 + 3] = 255;
  }
  return { texture: makeTexture(data, 16, 16, { wrap: THREE.ClampToEdgeWrapping, mipmap: 'point' }),
           renormCells };
}

function buildTileMesh(tx, ty, variant, xOff) {
  const tile = tiles[ty][tx];
  const dec = tileMaterials[ty][tx];
  const named = dec.materials;
  const base = named[0];
  const overlaysAll = named.slice(1);
  const sel = selectTop3(overlaysAll);
  const selOverlays = sel.map((i) => overlaysAll[i]);
  const dropped = overlaysAll.filter((_, i) => !sel.includes(i));
  const fac = factorTexture(sel, overlaysAll, variant === 'norm');

  const positions = new Float32Array(S * S * 3);
  const uvs = new Float32Array(S * S * 2);
  for (let y = 0; y < S; y++) {
    for (let x = 0; x < S; x++) {
      const i = (y * S + x) * 3;
      positions[i] = (ORIGIN_X + tx) * S * PE_TERRAIN_METER_PER_SAMPLE + x * PE_TERRAIN_METER_PER_SAMPLE + xOff;
      positions[i + 1] = worldHeightMeters(tile.heights[y * S + x]);
      positions[i + 2] = (ORIGIN_Y + ty) * S * PE_TERRAIN_METER_PER_SAMPLE + y * PE_TERRAIN_METER_PER_SAMPLE;
      const u = (y * S + x) * 2;
      uvs[u] = x / (S - 1);
      uvs[u + 1] = y / (S - 1);
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
  g.setAttribute('uv', new THREE.BufferAttribute(uvs, 2));
  g.setIndex(new THREE.BufferAttribute(indices, 1));
  g.computeVertexNormals();

  const material = new THREE.ShaderMaterial({
    uniforms: {
      uBase: { value: baseTexById.get(base.id) },
      uFactor: { value: fac.texture },
      uD0: { value: idSet.get(selOverlays[0]?.id ?? base.id).texture },
      uD1: { value: idSet.get(selOverlays[1]?.id ?? base.id).texture },
      uD2: { value: idSet.get(selOverlays[2]?.id ?? base.id).texture },
    },
    vertexShader: `
      varying vec2 vUv;
      void main() {
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }`,
    fragmentShader: `
      precision highp float;
      // TERRAIN_14 blend (era 9.3.5, ops CONFIRMED from the original ps.1.4):
      //   D = d0*w0 + d1*w1 + d2*w2 ; w = factor RGB, u8/255, NO renormalization
      //   overlay keyed per channel on D: D>=0.5 -> 1-2(1-b)(1-D) else 2*b*D
      // UNLIT calibration: original light/shadow/fog NOT implemented here.
      uniform sampler2D uBase;
      uniform sampler2D uFactor;
      uniform sampler2D uD0;
      uniform sampler2D uD1;
      uniform sampler2D uD2;
      varying vec2 vUv;
      void main() {
        vec3 w = texture2D(uFactor, vUv).rgb;
        vec3 d0 = texture2D(uD0, vUv * ${DETAIL_REPEAT[0].toFixed(1)}).rgb;
        vec3 d1 = texture2D(uD1, vUv * ${DETAIL_REPEAT[1].toFixed(1)}).rgb;
        vec3 d2 = texture2D(uD2, vUv * ${DETAIL_REPEAT[2].toFixed(1)}).rgb;
        vec3 D = d0 * w.r + d1 * w.g + d2 * w.b;
        vec3 b = texture2D(uBase, vUv).rgb;
        vec3 lo = clamp(b * D * 2.0, 0.0, 1.0);
        vec3 hi = 1.0 - clamp((1.0 - b) * (1.0 - D) * 2.0, 0.0, 1.0);
        vec3 o = mix(lo, hi, step(vec3(0.5), D));
        gl_FragColor = vec4(o, 1.0);
      }`,
  });
  scene.add(new THREE.Mesh(g, material));
  return { tile: tile.name, variant, factorRenormCells: fac.renormCells, base,
           selOverlays, dropped, dec, facTexture: fac.texture };
}

const rowInfo = { raw: [], norm: [] };
for (let ty = 0; ty < N; ty++) {
  for (let tx = 0; tx < N; tx++) {
    rowInfo.raw.push(buildTileMesh(tx, ty, 'raw', 0));
    rowInfo.norm.push(buildTileMesh(tx, ty, 'norm', COLUMN_X_OFFSET));
  }
}
log('built 2x9 meshes: row[raw] (C1-raw factor) + row[norm] (C1n per-cell renormalized).');

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
// look along -Z so the two side-by-side X-offset candidate columns map to
// screen LEFT/RIGHT (v4 lesson: looking along -X made them overlap in depth).
camera.position.set(center.x, box.max.y + size.x * 0.5, center.z + size.x * 1.05);
camera.lookAt(center.x, center.y, center.z);

renderer.render(scene, camera);
const png1 = renderer.domElement.toDataURL('image/png');
const hash1 = await sha256Hex(Uint8Array.from(atob(png1.split(',')[1]), c => c.charCodeAt(0)));
renderer.render(scene, camera);
const png2 = renderer.domElement.toDataURL('image/png');
const hash2 = await sha256Hex(Uint8Array.from(atob(png2.split(',')[1]), c => c.charCodeAt(0)));

// ---------- in-page render-quality measures (robust, no projection guessing) ----------
// canvas histogram + per-row center probes (row centers projected â€” the proven
// iter020 approach: project a known world point, sample fixed pixel offsets).
const probeCanvas = document.createElement('canvas');
probeCanvas.width = W; probeCanvas.height = H;
const pctx = probeCanvas.getContext('2d', { willReadFrequently: true });
pctx.drawImage(renderer.domElement, 0, 0);
const img = pctx.getImageData(0, 0, W, H).data;
let clearPx = 0, whitePx = 0, otherPx = 0;
for (let p = 0; p < W * H; p++) {
  const r = img[p * 4], g = img[p * 4 + 1], b = img[p * 4 + 2];
  if (r === 10 && g === 10 && b === 18) clearPx++;
  else if (r >= 250 && g >= 250 && b >= 250) whitePx++;
  else otherPx++;
}
const histogram = {
  totalPx: W * H,
  clearColorPx: clearPx, clearColorPct: (100 * clearPx) / (W * H),
  whitePx, whitePct: (100 * whitePx) / (W * H),
  otherPx, otherPct: (100 * otherPx) / (W * H),
};

// per-variant analysis (EXACT, not heuristic): the camera sits at center.x
// looking along -Z (right vector = +X), so world x = center.x maps EXACTLY to
// canvas x = W/2 — the two candidate columns split perfectly at the screen
// center. Per variant: pixel count, bbox, mean RGB, white fraction.
function variantStats() {
  const SPLIT = W / 2; // exact: canvas x < SPLIT = raw column (world x < center.x)
  const out = { raw: null, norm: null, splitCanvasX: SPLIT };
  for (const [key, lo, hi] of [['raw', 0, SPLIT - 1], ['norm', SPLIT, W - 1]]) {
    let n = 0, sr = 0, sg = 0, sb = 0, nw = 0;
    let minY = H, maxY = 0, minX = W, maxX = 0;
    for (let y = 0; y < H; y++) {
      for (let x = lo; x <= hi; x++) {
        const p = (y * W + x) * 4;
        if (img[p] === 10 && img[p + 1] === 10 && img[p + 2] === 18) continue;
        n++; sr += img[p]; sg += img[p + 1]; sb += img[p + 2];
        if (img[p] >= 250 && img[p + 1] >= 250 && img[p + 2] >= 250) nw++;
        if (y < minY) minY = y; if (y > maxY) maxY = y;
        if (x < minX) minX = x; if (x > maxX) maxX = x;
      }
    }
    if (n === 0) continue;
    out[key] = { pixels: n, xRange: [minX, maxX], yRange: [minY, maxY],
                 meanRgb: [Math.round(sr / n), Math.round(sg / n), Math.round(sb / n)],
                 whitePct: (100 * nw) / n };
  }
  return out;
}
const bands = variantStats();

function colCenterProbe(xOff) {
  // project the CENTER TILE's actual surface point (sample 16,16 of tile (1,1))
  // at its TRUE terrain height — the v1 lesson: probing at bbox-center height
  // projected ~150m above the surface and landed in the background.
  const wx = ((ORIGIN_X + 1) * S + 16) * PE_TERRAIN_METER_PER_SAMPLE + xOff;
  const wz = ((ORIGIN_Y + 1) * S + 16) * PE_TERRAIN_METER_PER_SAMPLE;
  const h = worldHeightMeters(tiles[1][1].heights[16 * S + 16]);
  const v = new THREE.Vector3(wx, h, wz).project(camera);
  const cx = Math.round((v.x * 0.5 + 0.5) * W), cy = Math.round((-v.y * 0.5 + 0.5) * H);
  const samples = [];
  for (const [dx, dy] of [[0, 0], [8, 0], [-8, 0], [0, 8], [0, -8], [16, 8], [-16, -8]]) {
    const x = Math.min(W - 1, Math.max(0, cx + dx)), y = Math.min(H - 1, Math.max(0, cy + dy));
    const p = (y * W + x) * 4;
    samples.push([img[p], img[p + 1], img[p + 2]]);
  }
  return { canvasPos: [cx, cy], surfaceHeightM: h, samples };
}

// ---------- results / provenance ----------
function tilePayload(r) {
  const tot = (m) => m.reduce((s, v) => s + v, 0);
  const selMass = r.selOverlays.reduce((s, o) => s + tot(o.mask), 0);
  const allMass = selMass + r.dropped.reduce((s, o) => s + tot(o.mask), 0);
  return {
    tile: r.tile, variant: r.variant,
    base: { id: r.base.id, name: r.base.name, maskEncoding: r.base.maskEncoding,
            baseAll255: Array.from(r.base.mask).every((v) => v === 255) },
    selectedTop3: r.selOverlays.map((o) => ({ id: o.id, name: o.name, total: tot(o.mask) })),
    droppedOverlays: r.dropped.map((o) => ({ id: o.id, name: o.name, total: tot(o.mask) })),
    weightMassCapture: allMass ? selMass / allMass : null,
    factorRenormCells: r.factorRenormCells,
    namedCount: r.dec.materials.length,
  };
}
const binding = [];
for (const [id, info] of idSet) {
  binding.push({
    id, name: info.name, payloadSha256: info.payloadSha,
    era: info.provenance.era, container: info.provenance.container,
    entry: info.provenance.entry,
    sameEraAsCleanRuntimePrimary: info.provenance.extra.sameEraAsCleanRuntimePrimary,
    decodedSize: `${info.width}x${info.height}`,
  });
}
const result = {
  page: 'terrain/materials_wsum.js v2 â€” TERRAIN_14 REAL BLEND, dual factor-content candidates',
  version: 'M1_ITER_039_secondary (ledger ITER_025)',
  chain: 'terrain.bnt+Textures.bnt bytes -> PESourceMount -> tiles+materials -> TgaDecoder -> r185 TERRAIN_14-style render',
  region: { originGridX: ORIGIN_X, originGridY: ORIGIN_Y, tilesX: N, tilesY: N },
  rows: {
    raw: { xOffset: 0, factorContent: 'C1-raw: raw TDF mask u8 weights (unrenormalized)',
           expectation: 'overlapping heavy weights => D>1 => overlay saturates white (shader behavior)' },
    norm: { xOffset: COLUMN_X_OFFSET, factorContent: 'C1n: per-cell renormalized (round(w*255/sum) where sum>255)',
            expectation: 'no saturation; bake-side normalization candidate' },
  },
  blendModel: {
    op: 'D = d0*w0 + d1*w1 + d2*w2; overlay on base keyed per channel on D',
    opStatus: 'CONFIRMED era 9.3.5 (iter024 extracted Terrain_14 ps.1.4, byte-faithful SHA 5AE4AF81â€¦)',
    lighting: 'UNLIT deterministic calibration (original light/shadow/fog NOT implemented)',
    normalization: 'NONE in-shader (factor u8/255 unrenormalized â€” CONFIRMED)',
  },
  reduction: {
    mechanism: 'TOP3_TOTAL_WEIGHT',
    status: 'UNVERIFIED_REDUCTION_CANDIDATE (engine mechanism UNRESOLVED; TerrainImageCache1/2.vfs EMPTY â€” iter025)',
    dataReference: 'iter025_reduction_analysis.json (C1 UB-capture 0.934-0.999 region A / 0.770-0.951 region B)',
  },
  factorTexture: {
    source: 'DERIVED from TDF dim=16 named masks (RAW/RLE, iter008b semantics)',
    resolution: '16x16 per tile',
    originalCacheStatus: 'TerrainImageCache1/2.vfs = runtime-created EMPTY ArkVFS02 (0 records) â€” factor data NOT shipped',
  },
  samplerStates: {
    base: 'CLAMP, MIN=LINEAR, MAG=LINEAR, MIP=POINT -> ClampToEdge + LinearMipmapNearest',
    factor: 'CLAMP, MIN=LINEAR, MAG=LINEAR, MIP=POINT -> ClampToEdge + LinearMipmapNearest',
    details: 'WRAP, MIN=LINEAR, MAG=LINEAR, MIP=LINEAR -> Repeat + LinearMipmapLinear',
    detailLodBias: '-0.5 (CONFIRMED historical) NOT EXPRESSIBLE in r185 â€” documented deviation',
    detailRepeats: [32, 32, 16],
  },
  calibrations: {
    vertexUv: 'patch-local 0..1 per TDF tile (CURRENT_RUNTIME_CALIBRATION; 9.3.5 mesh UV UNVERIFIED)',
    factorResolution: '16x16 (mask-derived; original factor resolution UNKNOWN â€” dim=256 fine-grain masks open lead)',
  },
  renderer: {
    threeRevision: THREE.REVISION, backend: 'WebGLRenderer', width: W, height: H,
    colorSpace: 'NoColorSpace passthrough (raw texels, no tone mapping)',
  },
  renderQuality: { histogram, bands },
  rowProbes: { raw: colCenterProbe(0), norm: colCenterProbe(COLUMN_X_OFFSET) },
  screenshotPngSha256: hash1, screenshotDeterministic: hash1 === hash2,
  tileBindings: [...rowInfo.raw.map(tilePayload), ...rowInfo.norm.map(tilePayload)],
  textureBindings: binding,
};
window.__WSUM__ = result;
window.__WSUM_PNG__ = png1;
log(
`SECONDARY v2 RENDERED (TERRAIN_14 ops; dual factor candidates) â€” 2 rows x 9 tiles
render canvas: clear ${histogram.clearColorPct.toFixed(1)}% / white ${histogram.whitePct.toFixed(1)}% / terrain-other ${histogram.otherPct.toFixed(1)}%
screenshot sha256: ${hash1} (deterministic: ${hash1 === hash2})
row[raw]=C1-raw factor; row[norm]=C1n renormalized â€” NEITHER claimed as the engine's bake`);
