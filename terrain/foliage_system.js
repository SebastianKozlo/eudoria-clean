// foliage_system.js — M1 ITER 049 (ledger ITER_035, the FLOAT64 operand lock).
// THE CONFIRMED FOLIAGE CHAIN, rendered through the clean pipeline over the
// proven 9-tile region: the terrain + the GENERATED instances standing on it
// (the binary-locked node fields: position/scale per the iter035 operand
// census; heights sampled from the clean terrain chain). DETERMINISTIC: same
// inputs -> same render hash.
//
// CHAIN (the ONLY sanctioned architecture, ledger ENTRY #2/#3/#9):
//   ORIGINAL PCG_9_3_5 BYTES (terrain.bnt + VegetationClimates.bnt, SHA-pinned)
//     -> PESourceMount (BNT2_TERRAIN / BNT2 framing, era-labeled)
//     -> canonical TerrainTile + VCL climate records (provenance on every object)
//     -> PE Runtime Core (PETerrainRegion + PEFoliageCore — the CONFIRMED
//        chain with the FLOAT64 operand lock: FUN_0083a7d0 / FUN_0098fe00 /
//        FUN_00990810 / FUN_0095ac30 / FUN_0098cdf0 / FUN_0098ce30 /
//        FUN_0095b180; the constants 32767.0 / 65535.0 /
//        0.00007812499825377017 all f64 BYTE-LOCKED, the f32 rounding at the
//        binary's own six FSTP points — iter035, ledger ITER_035)
//     -> Three.js r185 WebGLRenderer
//     -> deterministic render + reproducible artifact
//
// HONEST BOUNDS (all labeled — see PEFoliageCore.FOLIAGE_PLACEHOLDERS /
// FOLIAGE_OPERAND_LOCK for the full lists with the RE evidence):
//   [P-CLIMATE] RECONSTRUCTION-ONLY: climate index 0 (0.vcl) — the
//       per-location climate input is PLAUSIBLE-UNVERIFIED (the
//       shared-selector hypothesis, iter032); the DOCUMENTED CHOICE follows
//       the established constant-byte-0 convention of the terrain material
//       page ([P1] in materials_confirmed.js); the climate's elevation band
//       union [-6, 1000] admits the region heights.
//   [P-WINDOW] RECONSTRUCTION-ONLY: the generation window = the proven region
//       mapped to the u16 record space at 2 units per world meter (u16 =
//       world x 2; windowWorld = the region box) — the historical grid
//       extents are RNG/settings-scaled and not statically pinneable, and the
//       visualizer's [0,1]-node-position -> world transform is NOT
//       decompiled (FUN_0095ae20/FUN_0095b4f0); this page's linear window
//       calibration is CURRENT_RUNTIME_CALIBRATION, NOT historical truth.
//   [P-UNITS] RECONSTRUCTION-ONLY: the GLB cache preserves the NIF centimeter
//       units (the terrain path scales m->cm x100, FUN_0082b790); the page
//       bridges cm->m (0.01) for the render. Bounding boxes recorded per model.
//   [P-MATERIALS] the render technique 'Vegetation' = FX 0x3EC (materials.vfs,
//       both eras, vertex-shaded '#include 1Ark.fx/25ArkLight.fx/10NiTexture.fx'
//       — iter032 stage 9) INFORMS this page's lighting model only; the
//       per-model materials come from the GLB cache (GENERATED_CACHE) with
//       fixed deterministic lights — an era-bounded approximation, NOT a
//       byte-faithful technique render.
//   THE NODE-SCALE RENDER BRIDGE: the BINARY node scale (node+0x68 =
//       f32(|lerp * 0.00007812499825377017|)) is carried BIT-EXACT in the
//       census/instances; the visualizer path that maps the node scale to a
//       world size is NOT decompiled (iter032 bound 5) — the render bridges it
//       with RENDER_SCALE_CALIBRATION = 2.0 / NODE_SCALE_MUL (the exact ratio
//       that preserves the previously-deployed effective tree sizes), a
//       CURRENT_RUNTIME_CALIBRATION and NOT a historical-truth claim. The
//       bit-exact node scale is the revalidation target, never the pixels.
//   WORLD CALIBRATION (CURRENT_RUNTIME_CALIBRATION, as the proven pages): 1
//   sample = 4 PE meters (TILE_WORLD = 128), heights = u16/128 m
//   (worldHeightMeters, PETerrainCore). NOT proven historical engine facts.

import * as THREE from 'three';
import { GLTFLoader } from '/node_modules/three/examples/jsm/loaders/GLTFLoader.js';
import { PESourceMount } from '../src/pesource/PESourceMount.js';
import { ERAS } from '../src/pesource/PEProvenance.js';
import { PETerrainRegion, worldHeightMeters, PE_TERRAIN_TILE_SIZE } from '../src/peworld/PETerrainCore.js';
import { generateInstances, FOLIAGE_RE, FOLIAGE_PLACEHOLDERS, FOLIAGE_OPERAND_LOCK,
         NODE_SCALE_MUL } from '../src/peworld/PEFoliageCore.js';

const HUD = document.getElementById('hud');
const LEGEND = document.getElementById('legend');
const log = (m) => { HUD.textContent = m; console.log(m); };

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
await mount.mountEra({ era: ERAS.PCG_9_3_5, container: 'Terrain/terrain.bnt',
  path: '/pcg/Data/Terrain/terrain.bnt', format: 'BNT2_TERRAIN', verifyHash: true });
await mount.mountEra({ era: ERAS.PCG_9_3_5, container: 'VegetationClimates/VegetationClimates.bnt',
  path: '/pcg/Data/VegetationClimates/VegetationClimates.bnt', format: 'BNT2', verifyHash: true });
log('mounted terrain.bnt + VegetationClimates.bnt (SHA-verified).');

// ---------- the proven 9-tile region (the P0 region, tiles 56..58 x 112..114) ----------
const ORIGIN_X = 56, ORIGIN_Y = 112, N = 3;
const TILE_WORLD = 128;   // 32 samples x 4 PE meters (page calibration)
const G = 32;
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

// ---------- the climate [P-CLIMATE] ----------
const CLIMATE_INDEX = 0;   // DOCUMENTED CHOICE — see header [P-CLIMATE]
const climate = await mount.getVegetationClimate({ era: ERAS.PCG_9_3_5, climateIndex: CLIMATE_INDEX });
log(`climate ${CLIMATE_INDEX}.vcl: ${climate.recordCount} records (12-value, FUN_0083a7d0).`);

// ---------- the generator (PEFoliageCore — the CONFIRMED chain, FLOAT64-locked) ----------
// [P-WINDOW] RECONSTRUCTION-ONLY page calibration: the u16 record space = the
// region at 2 units per world meter (u16 = world x 2); windowWorld = the
// region box. The BINARY node fields are computed inside the module
// (node01 = f32(u16/65535.0); scale = f32(|lerp * 0.00007812499825377017|)).
const U16_PER_WORLD = 2.0;  // the [P-WINDOW] page calibration (documented, NOT historical)
const LEVEL = 1;         // RE-derived default: FUN_0095b180's settings+4 = 1 -> step 2
const VIEW_BAND = 10;    // p2 (STRONGLY_SUPPORTED: the +0x2c view-band field)
const P3 = 0;            // [P-RNG-P3]
const worldX0 = ORIGIN_X * TILE_WORLD, worldY0 = ORIGIN_Y * TILE_WORLD;
const worldX1 = (ORIGIN_X + N) * TILE_WORLD, worldY1 = (ORIGIN_Y + N) * TILE_WORLD;
const windowWorld = { x0: worldX0, y0: worldY0, x1: worldX1, y1: worldY1 };
const windowU16 = {
  x0: Math.round(worldX0 * U16_PER_WORLD), y0: Math.round(worldY0 * U16_PER_WORLD),
  x1: Math.round(worldX1 * U16_PER_WORLD), y1: Math.round(worldY1 * U16_PER_WORLD),
};
const { instances, census } = generateInstances({
  records: climate.records,
  windowU16,
  windowWorld,
  level: LEVEL,
  viewBand: VIEW_BAND,
  p3: P3,
});
log(`generated ${instances.length} instances over ${census.inputs.cells} sub-cells (level ${LEVEL}, step ${census.inputs.step}).`);

// ---------- terrain height sampling (the clean chain, bilinear) ----------
// The historical attach: the NiNode carries (x, y) and the heightfield client
// supplies the ground (ArkVegetationHeightFieldSourceClient, iter032 stage 3);
// here the heights come from the SAME canonical region tiles (bilinear over
// the raw u16 sample grid -> worldHeightMeters, PETerrainCore semantics).
const SAMPLES = N * PE_TERRAIN_TILE_SIZE;   // 96 x 96 region sample grid
function rawSampleBilinear(lx, lz) {
  lx = Math.max(0, Math.min(SAMPLES - 1, lx));
  lz = Math.max(0, Math.min(SAMPLES - 1, lz));
  const x0 = Math.min(SAMPLES - 2, Math.floor(lx)), z0 = Math.min(SAMPLES - 2, Math.floor(lz));
  const fx = lx - x0, fz = lz - z0;
  const h00 = region.rawSample(x0, z0), h10 = region.rawSample(x0 + 1, z0);
  const h01 = region.rawSample(x0, z0 + 1), h11 = region.rawSample(x0 + 1, z0 + 1);
  return h00 * (1 - fx) * (1 - fz) + h10 * fx * (1 - fz) + h01 * (1 - fx) * fz + h11 * fx * fz;
}
function terrainHeightAt(wx, wz) {
  const lx = (wx - worldX0) / (TILE_WORLD / PE_TERRAIN_TILE_SIZE);
  const lz = (wz - worldY0) / (TILE_WORLD / PE_TERRAIN_TILE_SIZE);
  return worldHeightMeters(rawSampleBilinear(lx, lz));
}
for (const inst of instances) {
  inst.terrainHeightM = terrainHeightAt(inst.world.x, inst.world.y);
  // diagnostic (NO filtering — the elevation-band rule is UNVERIFIED at the
  // filter level; the census records the within-band counts honestly):
  inst.withinElevationBand = inst.terrainHeightM >= inst.elevationBand.min &&
                             inst.terrainHeightM <= inst.elevationBand.max;
}

// ---------- the model cache (GENERATED_CACHE, provenance-verified at load) ----------
const MANIFEST_URL = '/assets/foliage_glb/MANIFEST.json';
const manifest = await (await fetch(MANIFEST_URL)).json();
const manifestById = new Map(manifest.files.map((f) => [f.id, f]));

const distinctIds = [...new Set(instances.map((i) => i.modelId))];
const loadedModels = {};   // id -> {gltfScene, provenance, bbox}
const notFound = [];       // LOUD misses — no silent fallback
const loader = new GLTFLoader();
for (const id of distinctIds) {
  const rec = manifestById.get(id);
  if (!rec) {
    notFound.push({ id, reason: `model id ${id} NOT_FOUND in the foliage GLB manifest (${MANIFEST_URL}) — LOUD, instance rendering skipped` });
    continue;
  }
  const url = `/assets/foliage_glb/${rec.file}`;
  const bytes = await fetchBytes(url);
  const sha = await sha256Hex(bytes);
  if (sha !== rec.sha256.toUpperCase()) {
    throw new Error(`[foliage_system] GLB SHA256 MISMATCH for ${rec.file}: got ${sha}, manifest ${rec.sha256} — REFUSING to render (provenance gate)`);
  }
  const gltf = await new Promise((resolve, reject) =>
    loader.parse(bytes.buffer, '', resolve, reject));
  const bbox = new THREE.Box3().setFromObject(gltf.scene);
  loadedModels[id] = {
    gltfScene: gltf.scene,
    provenance: {
      class: manifest.status,
      source: manifest.source.tree,
      exporter: manifest.source.exporter,
      eraPinning: manifest.source.eraPinning,
      file: rec.file, sha256: sha, bytes: rec.bytes,
      modelIdNif: `${id}.nif (VCL col0 -> the GetModel type-0x66 id space, FUN_0094b1d0)`,
    },
    bbox: { min: bbox.min.toArray(), max: bbox.max.toArray() },
  };
}
if (notFound.length) console.warn('[foliage_system] NOT_FOUND models (LOUD):', notFound);
log(`model cache: ${Object.keys(loadedModels).length}/${distinctIds.length} distinct ids resolved${notFound.length ? `; NOT_FOUND: ${notFound.length} (LOUD)` : ''}.`);

// ---------- the scene ----------
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a12);

// The ground terrain (per-tile meshes at the grid-anchored world positions).
const ground = new THREE.Group();
for (let ty = 0; ty < N; ty++) {
  for (let tx = 0; tx < N; tx++) {
    const tile = tiles[ty][tx];
    const geo = new THREE.PlaneGeometry(TILE_WORLD, TILE_WORLD, G - 1, G - 1);
    geo.rotateX(-Math.PI / 2);
    const pos = geo.attributes.position;
    const colors = new Float32Array(pos.count * 3);
    for (let y = 0; y < G; y++) {
      for (let x = 0; x < G; x++) {
        const i = y * G + x;
        const h = worldHeightMeters(tile.heights[y * G + x]);
        pos.setY(i, h);
        const t = Math.max(0, Math.min(1, (h + 20) / 220));
        colors[i * 3] = 0.30 + 0.40 * t; colors[i * 3 + 1] = 0.30 + 0.36 * t; colors[i * 3 + 2] = 0.24 + 0.26 * t;
      }
    }
    geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geo.computeVertexNormals();
    const mesh = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ vertexColors: true }));
    mesh.position.set((ORIGIN_X + tx) * TILE_WORLD + TILE_WORLD / 2, 0,
                      (ORIGIN_Y + ty) * TILE_WORLD + TILE_WORLD / 2);
    ground.add(mesh);
  }
}
scene.add(ground);

// The instances — the BINARY node fields (bit-exact: node01 + scale) carry the
// fidelity claim; the height comes from the clean terrain chain; ROTATION =
// identity (RE-faithful: the spawn loop sets position + scale + model id only,
// iter032 bound 5).
const UNIT_BRIDGE = 0.01;   // [P-UNITS] NIF cm -> render meters
// THE NODE-SCALE RENDER BRIDGE (CURRENT_RUNTIME_CALIBRATION, NOT historical):
// the visualizer's node-scale -> world-size transform is NOT decompiled
// (iter032 bound 5); this exact ratio preserves the previously-deployed
// effective tree sizes while the census carries the BIT-EXACT binary node
// scale (see the header comment + FOLIAGE_OPERAND_LOCK).
const RENDER_SCALE_CALIBRATION = 2.0 / NODE_SCALE_MUL;
const foliage = new THREE.Group();
let renderedInstances = 0;
for (const inst of instances) {
  const model = loadedModels[inst.modelId];
  if (!model) continue;   // NOT_FOUND already recorded LOUD — never a fallback
  const node = model.gltfScene.clone(true);
  node.position.set(inst.world.x, inst.terrainHeightM, inst.world.y);
  const s = inst.scale * RENDER_SCALE_CALIBRATION * UNIT_BRIDGE;
  node.scale.set(s, s, s);
  foliage.add(node);
  inst.rendered = true;
  renderedInstances++;
}
scene.add(foliage);
// Debug/audit handles (do not affect the default render):
// - ?foliage-off hides the instance group BEFORE the single deterministic
//   render (the visibility pixel-diff audit compares fresh loads with/without
//   the instances — anti-success-theater: the "instances render" claim must
//   not rest on a hash that could be terrain-only).
// - window.__iter033_foliage exposes the group for inspection.
if (new URLSearchParams(location.search).has('foliage-off')) foliage.visible = false;
window.__iter033_foliage = foliage;

// Fixed deterministic lights + camera.
const sun = new THREE.DirectionalLight(0xffffff, 1.0);
sun.position.set(-700, 900, -1100);
scene.add(sun);
scene.add(new THREE.AmbientLight(0x404050, 1.0));
const camera = new THREE.PerspectiveCamera(52, 16 / 9, 1, 60000);
const cx = (worldX0 + worldX1) / 2, cz = (worldY0 + worldY1) / 2;
camera.position.set(cx + 120, 260, cz + 420);
camera.lookAt(cx, 40, cz);

const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setSize(1280, 720);
document.getElementById('view').appendChild(renderer.domElement);

// ---------- the deterministic render ----------
renderer.render(scene, camera);
const png1 = renderer.domElement.toDataURL('image/png');
renderer.render(scene, camera);
const png2 = renderer.domElement.toDataURL('image/png');
const deterministic = png1 === png2;
const enc = new TextEncoder();
const renderHash = await sha256Hex(enc.encode(png1));

// ---------- the result (census + provenance + hashes) ----------
const regionHeights = (() => {
  let mn = Infinity, mx = -Infinity;
  for (let ty = 0; ty < N; ty++) for (let tx = 0; tx < N; tx++) {
    for (let i = 0; i < 1024; i++) {
      const h = worldHeightMeters(tiles[ty][tx].heights[i]);
      mn = Math.min(mn, h); mx = Math.max(mx, h);
    }
  }
  return { minM: mn, maxM: mx };
})();

const result = {
  p0: 'clean foliage chain: the FLOAT64-locked iter035 algorithm -> generated instances (binary node fields bit-exact) -> deterministic render over the proven 9-tile region',
  chain: 'VegetationClimates.bnt + terrain.bnt bytes -> PESourceMount(BNT2) -> VCL climate records + TerrainTiles -> PEFoliageCore (the CONFIRMED chain with the FLOAT64 operand lock: FUN_0098fe00/00990810/0095ac30/0098cdf0/0098ce30/0095b180; 32767.0/65535.0/0.00007812499825377017 f64 byte-locked; f32 at the six FSTP points) -> r185 WebGLRenderer',
  reChain: FOLIAGE_RE,
  operandLock: FOLIAGE_OPERAND_LOCK,
  placeholders: { ...FOLIAGE_PLACEHOLDERS,
    'P-CLIMATE': `${FOLIAGE_PLACEHOLDERS['P-CLIMATE']} — PAGE CHOICE: index ${CLIMATE_INDEX} (0.vcl, ${climate.recordCount} records)`,
    'P-WINDOW': 'RECONSTRUCTION-ONLY: the generation window = the proven region mapped to the u16 record space at 2 units/world-meter (u16 = world x 2); windowWorld = the region box; the historical grid extents are settings-scaled, the visualizer [0,1]->world transform NOT decompiled — CURRENT_RUNTIME_CALIBRATION',
    'P-UNITS': 'GLB cache preserves NIF centimeters; render bridge 0.01 (m->cm x100 evidence: FUN_0082b790); the node-scale render bridge = 2.0/NODE_SCALE_MUL (CURRENT_RUNTIME_CALIBRATION — preserves the deployed effective sizes; NOT historical)',
    'P-MATERIALS': "FX technique 0x3EC ('Vegetation', vertex-shaded, materials.vfs both eras) INFORMS the lighting only; per-model materials = the GENERATED_CACHE GLBs; fixed deterministic lights — era-bounded approximation" },
  climate: {
    index: CLIMATE_INDEX,
    recordCount: climate.recordCount,
    records: climate.records,
    provenance: climate.provenance,
  },
  region: {
    originGridX: ORIGIN_X, originGridY: ORIGIN_Y, tilesX: N, tilesY: N,
    tileNames: tiles.flat().map(t => t.name),
    seamDiagnostic: region.tileSeamDiagnostic,
    heightsM: regionHeights,
    worldBox: { x0: worldX0, x1: worldX1, y0: worldY0, y1: worldY1 },
  },
  generator: {
    u16PerWorld: U16_PER_WORLD, level: LEVEL, step: census.inputs.step,
    viewBand: VIEW_BAND, p3: P3, windowU16, windowWorld,
    constants: census.inputs.constants,
    renderScaleCalibration: RENDER_SCALE_CALIBRATION,
  },
  census: {
    ...census,
    elevationBandDiagnostic: {
      rule: 'NO FILTER APPLIED — the elevation-band filter semantics are UNVERIFIED; within-band measured as a diagnostic',
      withinBand: instances.filter(i => i.withinElevationBand).length,
      outsideBand: instances.filter(i => !i.withinElevationBand).length,
    },
    renderedInstances,
    notFoundModels: notFound,
    modelProvenance: Object.fromEntries(Object.entries(loadedModels).map(([id, m]) => [id, { provenance: m.provenance, bbox: m.bbox }])),
  },
  instances,
  render: {
    deterministicInPage: deterministic,
    sha256: renderHash,
    width: 1280, height: 720,
    threeRevision: THREE.REVISION,
    foliageVisible: foliage.visible,   // false only for ?foliage-off (audit variant)
  },
};
window.__iter033_result = result;
window.__iter033_png__ = png1;

const within = result.census.elevationBandDiagnostic.withinBand;
const outside = result.census.elevationBandDiagnostic.outsideBand;
log(
`FOLIAGE SYSTEM page (ITER 049 / ledger ITER 035 — FLOAT64 operand lock) - deterministic in-page: ${deterministic}
render sha256: ${renderHash}
instances: ${instances.length} generated / ${renderedInstances} rendered (${distinctIds.length} distinct models; NOT_FOUND: ${notFound.length})
sub-cells: ${census.inputs.cells} (level ${LEVEL} -> step ${census.inputs.step}); region heights ${regionHeights.minM.toFixed(1)}..${regionHeights.maxM.toFixed(1)} m
constants LOCKED (binary f64): rand01/32767.0, node01=u16/65535.0, scale=f32(|lerp*0.00007812499825377017|); f32 at the binary's six FSTP points
elevation-band diagnostic: ${within} within / ${outside} outside (NO filter applied — rule UNVERIFIED)
models resolved from the GENERATED_CACHE manifest with per-file SHA verification (LOUD NOT_FOUND: ${notFound.length})`);

LEGEND.textContent =
`HONEST BOUNDS (labeled, never silent approximations; RECONSTRUCTION-ONLY items are NOT historical truth):
[P-CLIMATE] RECONSTRUCTION-ONLY: climate index ${CLIMATE_INDEX} (0.vcl) - the per-location climate input PLAUSIBLE-UNVERIFIED (the shared-selector hypothesis, iter032); documented choice
[P-CELLSTREAM] RECONSTRUCTION-ONLY: the per-cell record CONTENT = local deterministic stand-in (the historical cell byte-stream origin NOT closed, iter032 bound 3); the record FORMAT {u16,u16,u32} + the spawn arithmetic are the CONFIRMED parts
[P-RNG-P3] seed p3 = 0 (*(impl+0x24) UNVERIFIED); p2 = view band 10 (STRONGLY_SUPPORTED: the +0x2c 10/20/30 field pattern, FUN_0095b180)
[P-SCALE-FIELDS] the lerp min/max = the f32 fields impl+0x44/impl+0x40 (FLD DWORD, census-locked); the VCL col2/col3 mapping = the census reading (STRONGLY_SUPPORTED, NOT byte-pinned); the node-scale world-size meaning depends on the field VALUES (bounded)
[P-WINDOW] RECONSTRUCTION-ONLY: the window = the region at u16 = world x 2 + windowWorld = the region box (CURRENT_RUNTIME_CALIBRATION; the visualizer [0,1]->world transform NOT decompiled)
[P-UNITS] GLB cache preserves NIF cm; render bridges: 0.01 (cm->m) + the node-scale bridge 2.0/NODE_SCALE_MUL (CURRENT_RUNTIME_CALIBRATION, NOT historical)
[P-MATERIALS] technique 0x3EC ('Vegetation', vertex-shaded, materials.vfs both eras) INFORMS the lighting only; materials = the GENERATED_CACHE GLBs; fixed lights - era-bounded approximation
LOCKED FROM THE BINARY (iter035, ledger ITER_035, address-cited, every operand width census-locked): _DAT_00a7d7a8 = 32767.0 f64 (FDIV QWORD @0x0098CE5A; bytes 00 00 00 00 C0 FF DF 40; file 0x67D7A8); _DAT_00a8c758 = 65535.0 f64 (FLD QWORD @0x0095B2BC/0x0095B3DB; bytes 00 00 00 00 E0 FF EF 40; file 0x68C758); _DAT_00a980d0 = 0.00007812499825377017 f64 (FMUL QWORD @0x0095B347; bytes 00 00 00 40 E1 7A 14 3F; file 0x6980D0; = float32(1/12800) widened); the f32 rounding at the six FSTP points (@0x0098CE60 rand01, @0x0095ACF0 lerp, @0x0095B318/0x0095B322 node01, @0x0095B353/0x0095B365 scale); the iter032/033 f32 reads (32768.0, 2.0, 2.0f) SUPERSEDED - they were the LOW DWORDS of these QWORD doubles`;
