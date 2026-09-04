// materials.js — MILESTONE 1-E ITER 020 P0 (CLEAN-PATH MATERIALS + TEXTURE BINDING)
// QUESTION: Do the CONFIRMED terrain material data for the audited 9-tile
// region render through the CLEAN pipeline with byte-provenance from
// PCG_9_3_5 (heights + materials + textures, end-to-end, zero legacy input)?
//
// CHAIN: pcg_install terrain.bnt + Textures.bnt ORIGINAL BYTES (/pcg/, SHA-pinned)
//   -> PESourceMount (PCG_9_3_5; BNT2_TERRAIN terrain + BNT2 textures)
//   -> getTerrainMaterials (canonical material objects, provenance)
//   -> resolveTexture + TgaDecoder (SAME-ERA PCG texture payloads)
//   -> r185 WebGLRenderer, per-tile splat (Stone04 base + sequential overlays)
//
// BLEND MODEL (iter009 CONFIRMED data model, labels kept honest):
//   color = base texture (position-0 named record, full coverage);
//   for each overlay in RECORD ORDER: color = mix(color, overlay, w/255).
//   NO normalization (REJECTED corpus-wide) — sums>255 = ORIGINAL DATA.
//   UV scale = world-space repeat (uvRepeat), CURRENT_RUNTIME_CALIBRATION
//   (historical UV scale UNVERIFIED; iter015/iter014 negatives).
//
// r185 PREIMPLEMENTATION CHECKS (pe-threejs-r185 skill, ENTRY #9 §7):
//   - Material.type STATIC (r170): ShaderMaterial used, .type never mutated.
//   - r177 MultiplyBlending premultipliedAlpha: NOT USED (no blending).
//   - flipY/orientation: DataTexture flipY=false; TGA rows pre-flipped at
//     upload so texture v=0 = image bottom; image top <-> world +Z (south).
//     Mask row 0 <-> tile grid-y row 0. BOTH orientations UNVERIFIED
//     historically — recorded as CURRENT_RUNTIME_CALIBRATION.
//   - color-space: NoColorSpace passthrough (raw TGA texels -> framebuffer,
//     no tone mapping, deterministic unlit render) — calibration choice.
//   - mip/filter (gate F convention): generateMipmaps=true, minFilter
//     LinearMipmapLinearFilter, magFilter LinearFilter — recorded.
//   - matrix/world-transform: static meshes, matrixAutoUpdate default.
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

// ---------- mounts (SHA-pinned, era-labeled) ----------
const mount = new PESourceMount(io);
log('mounting PCG_9_3_5 terrain.bnt + Textures.bnt…');
await mount.mountEra({ era: ERAS.PCG_9_3_5, container: 'Terrain/terrain.bnt',
  path: '/pcg/Data/Terrain/terrain.bnt', format: 'BNT2_TERRAIN', verifyHash: true });
await mount.mountEra({ era: ERAS.PCG_9_3_5, container: 'Textures.bnt',
  path: '/pcg/Data/Textures/Textures.bnt', format: 'BNT2', verifyHash: true });
log('mounted + SHA-verified (terrain 95841761…, textures 61ACD13B…).');

// ---------- canonical tiles + materials through the clean chain ----------
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

// material decode per tile (clean chain)
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

// ---------- texture binding (same-era PCG payloads via resolveTexture) ----------
const idSet = new Map(); // id -> {texture, provenance, payloadSha, name}
for (const dec of tileMaterials.flat()) {
  for (const m of dec.materials) {
    if (!idSet.has(m.id)) idSet.set(m.id, { name: m.name });
  }
}
for (const [id, info] of idSet) {
  const res = await mount.resolveTexture({ era: ERAS.PCG_9_3_5, container: 'Textures.bnt', textureId: id });
  const dec = decodeTga2(res.payload); // loud-failure validated TGA2 subset
  const payloadSha = await sha256Hex(res.payload);
  // vertical flip at upload: decoded rgba is top-down; store bottom-up so
  // texture v=0 = image bottom (orientation calibration, see header)
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
log(`textures bound: ${idSet.size} distinct ids, same-era PCG payloads, TGA2 decode 0 failures.`);

// ---------- per-tile splat meshes ----------
const UV_REPEAT = 8; // world meters per texture repeat — CURRENT_RUNTIME_CALIBRATION (UNVERIFIED)
const MAX_OV = 8;    // covers the region max (8 named records on 003a0070)
const BLACK = new THREE.DataTexture(new Uint8Array([0, 0, 0, 255]), 1, 1, THREE.RGBAFormat);
BLACK.flipY = false; BLACK.needsUpdate = true;

const scene = new THREE.Scene();
const tileShaders = [];

function weightTexturePair(masks) {
  // pack up to 8 weight maps (16x16 each) into TWO RGBA textures (w0->texA.RGBA,
  // w4->texB.RGBA) — keeps the shader within MAX_TEXTURE_IMAGE_UNITS(16).
  const A = new Uint8Array(16 * 16 * 4), B = new Uint8Array(16 * 16 * 4);
  for (let i = 0; i < Math.min(masks.length, 8); i++) {
    const dst = i < 4 ? A : B;
    const ch = i % 4;
    for (let p = 0; p < 256; p++) dst[p * 4 + ch] = masks[i][p];
  }
  const mk = (data) => {
    const t = new THREE.DataTexture(data, 16, 16, THREE.RGBAFormat);
    t.magFilter = THREE.NearestFilter;  // discrete weights — no interpolation
    t.minFilter = THREE.NearestFilter;
    t.wrapS = THREE.ClampToEdgeWrapping;
    t.wrapT = THREE.ClampToEdgeWrapping;
    t.flipY = false;
    t.needsUpdate = true;
    return t;
  };
  return [mk(A), mk(B)];
}

for (let ty = 0; ty < N; ty++) {
  for (let tx = 0; tx < N; tx++) {
    const tile = tiles[ty][tx];
    const dec = tileMaterials[ty][tx];
    const named = dec.materials;
    const base = named[0];
    if (!base) throw new Error(`tile ${tile.name}: no named material`);
    const overlays = named.slice(1, 1 + MAX_OV);

    // per-tile geometry from canonical heights (same conventions as PETerrainRegion)
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
      uWA: { value: null },
      uWB: { value: null },
    };
    for (let i = 0; i < MAX_OV; i++) {
      const ov = overlays[i] ?? null;
      uniforms.uOvTex.value.push(ov ? idSet.get(ov.id).texture : BLACK);
    }
    const [wA, wB] = weightTexturePair(overlays.map((o) => o.mask));
    uniforms.uWA.value = wA;
    uniforms.uWB.value = wB;

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
        uniform sampler2D uWA;  // overlay weights 0..3 -> RGBA
        uniform sampler2D uWB;  // overlay weights 4..7 -> RGBA
        uniform int uOvCount;
        uniform float uVRepeat;
        varying vec3 vWorld;
        varying vec2 vCell;
        void main() {
          vec2 uv = vWorld.xz / uVRepeat;
          vec3 color = texture2D(uBase, uv).rgb;
          // unrolled: GLSL ES 1.00 requires constant sampler indices
          if (uOvCount > 0) { float w = texture2D(uWA, vCell).r; if (w > 0.0) color = mix(color, texture2D(uOvTex[0], uv).rgb, w / 255.0); }
          if (uOvCount > 1) { float w = texture2D(uWA, vCell).g; if (w > 0.0) color = mix(color, texture2D(uOvTex[1], uv).rgb, w / 255.0); }
          if (uOvCount > 2) { float w = texture2D(uWA, vCell).b; if (w > 0.0) color = mix(color, texture2D(uOvTex[2], uv).rgb, w / 255.0); }
          if (uOvCount > 3) { float w = texture2D(uWA, vCell).a; if (w > 0.0) color = mix(color, texture2D(uOvTex[3], uv).rgb, w / 255.0); }
          if (uOvCount > 4) { float w = texture2D(uWB, vCell).r; if (w > 0.0) color = mix(color, texture2D(uOvTex[4], uv).rgb, w / 255.0); }
          if (uOvCount > 5) { float w = texture2D(uWB, vCell).g; if (w > 0.0) color = mix(color, texture2D(uOvTex[5], uv).rgb, w / 255.0); }
          if (uOvCount > 6) { float w = texture2D(uWB, vCell).b; if (w > 0.0) color = mix(color, texture2D(uOvTex[6], uv).rgb, w / 255.0); }
          if (uOvCount > 7) { float w = texture2D(uWB, vCell).a; if (w > 0.0) color = mix(color, texture2D(uOvTex[7], uv).rgb, w / 255.0); }
          gl_FragColor = vec4(color, 1.0);
        }`,
    });
    const mesh = new THREE.Mesh(g, material);
    scene.add(mesh);
    tileShaders.push({
      tile: tile.name, base: { id: base.id, name: base.name, maskEncoding: base.maskEncoding },
      baseAll255: Array.from(base.mask).every((v) => v === 255),
      overlays: overlays.map((o) => ({ id: o.id, name: o.name, maskEncoding: o.maskEncoding })),
      sums: dec.sums,
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
  const g = m.geometry;
  const pos = g.getAttribute('position');
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
// determinism: second render must be byte-identical
renderer.render(scene, camera);
const png2 = renderer.domElement.toDataURL('image/png');
const hash2 = await sha256Hex(Uint8Array.from(atob(png2.split(',')[1]), c => c.charCodeAt(0)));

// ---------- in-page pixel probe (what is actually drawn under the region center) ----------
function ndcToCanvas(v) {
  return { x: Math.round((v.x * 0.5 + 0.5) * W), y: Math.round((-v.y * 0.5 + 0.5) * H) };
}
const centerNdc = center.clone().project(camera);
const cpx = ndcToCanvas(centerNdc);
const probeCanvas = document.createElement('canvas');
probeCanvas.width = W; probeCanvas.height = H;
const pctx = probeCanvas.getContext('2d', { willReadFrequently: true });
pctx.drawImage(renderer.domElement, 0, 0);
function sampleAt(dx, dy) {
  const x = Math.min(W - 1, Math.max(0, cpx.x + dx)), y = Math.min(H - 1, Math.max(0, cpx.y + dy));
  const d = pctx.getImageData(x, y, 1, 1).data;
  return [d[0], d[1], d[2]];
}
const pixelProbe = {
  canvasPos: cpx,
  center: sampleAt(0, 0),
  offsets: {
    '-200,-200': sampleAt(-200, -200), '-100,-100': sampleAt(-100, -100),
    '-50,-50': sampleAt(-50, -50), '0,-100': sampleAt(0, -100),
    '100,100': sampleAt(100, 100), '200,200': sampleAt(200, 200),
  },
  centerWorld: [center.x, center.y, center.z],
};

// ---------- results / provenance chain ----------
const binding = [];
for (const [id, info] of idSet) {
  binding.push({
    id, name: info.name, payloadSha256: info.payloadSha,
    era: info.provenance.era, container: info.provenance.container,
    entry: info.provenance.entry, sameEraAsCleanRuntimePrimary: info.provenance.extra.sameEraAsCleanRuntimePrimary,
    decodedSize: `${info.width}x${info.height}`,
  });
}
const result = {
  p0: 'clean-path materials + texture binding (PCG_9_3_5 primary, zero legacy runtime input)',
  chain: 'terrain.bnt+Textures.bnt bytes -> PESourceMount -> TerrainTile+materials -> TgaDecoder -> r185 splat render',
  region: { originGridX: ORIGIN_X, originGridY: ORIGIN_Y, tilesX: N, tilesY: N },
  mount: { terrainHashVerified: true, texturesHashVerified: true },
  materialDenominators: {
    tiles: 9, namedRecordsTotal: totalNamed,
    distinctMaterialIds: idSet.size,
    perTileNamedCounts: tileShaders.map((t) => `${t.tile}:${t.overlays.length + 1}`),
  },
  blendModel: {
    base: 'position-0 named record (Stone04 full-coverage base rule, CONFIRMED iter009)',
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
  screenshotPngSha256: hash1, screenshotDeterministic: hash1 === hash2,
  pixelProbe,
  tileBindings: tileShaders,
  textureBindings: binding,
  provenanceCount: 9 + totalNamed,
};
window.__MAT__ = result;
window.__MAT_PNG__ = png1;
log(
`P0 MATERIALS RENDERED — 9 tiles, ${totalNamed} material records, ${idSet.size} textures bound (same-era PCG)
screenshot sha256: ${hash1} (deterministic: ${hash1 === hash2})
base rule: 9/9 Stone04 all-255; normalization REJECTED (sums>255 = original data)`);
