// p0.js — MILESTONE 1-E ITER 019 P0 (CLEAN_RUNTIME_FOUNDATION)
// QUESTION: Does the CLEAN pipeline (r185, PCG_9_3_5 primary, ZERO legacy
// runtime input) render one terrain chunk region byte-faithfully end-to-end?
//
// CHAIN (the ONLY sanctioned architecture, ledger ENTRY #2/#3/#9):
//   pcg_install Data/Terrain/terrain.bnt ORIGINAL BYTES (read-only, SHA-pinned)
//     -> PESourceMount (era PCG_9_3_5, BNT2_TERRAIN framing)
//     -> canonical TerrainTile objects (provenance on every object)
//     -> PE Runtime Core (PETerrainRegion — FUN_0047fb20 height semantics)
//     -> Three.js r185 WebGLRenderer
//     -> render + reproducible artifact
//
// REGION: tiles (56..58, 112..114) — 3x3 = 9 tiles, all byte-identical to the
// JUL 50.bnt counterparts (verified pre-selection), fully inside legacy chunk
// r006_c003 (r169 ORACLE comparison is therefore legitimate for the same bytes).
import * as THREE from 'three';
import { PESourceMount } from '../src/pesource/PESourceMount.js';
import { ERAS } from '../src/pesource/PEProvenance.js';
import { PETerrainRegion, HEIGHT_QUERY } from '../src/peworld/PETerrainCore.js';

const HUD = document.getElementById('hud');
const log = (m) => { HUD.textContent = m; console.log(m); };

// ---------- browser I/O adapter (injected into PESourceMount) ----------
async function fetchBytes(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`fetch ${url}: HTTP ${res.status}`);
  return new Uint8Array(await res.arrayBuffer());
}
async function strictInflate(zlibBytes) {
  // DecompressionStream('deflate') = zlib (RFC1950) wrapper; STRICT about
  // trailing bytes (the exact property the era-validation relied on).
  const ds = new DecompressionStream('deflate');
  const stream = new Blob([zlibBytes]).stream().pipeThrough(ds);
  const buf = await new Response(stream).arrayBuffer();
  return new Uint8Array(buf);
}
async function sha256Hex(bytes) {
  const d = await crypto.subtle.digest('SHA-256', bytes);
  return [...new Uint8Array(d)].map(b => b.toString(16).padStart(2, '0')).join('').toUpperCase();
}
const io = { readFile: fetchBytes, inflate: strictInflate, sha256: sha256Hex };

// ---------- mount the ORIGINAL container (hash-pinned, era-labeled) ----------
const TERRAIN_URL = '/pcg/Data/Terrain/terrain.bnt';
const mount = new PESourceMount(io);
log('mounting PCG_9_3_5 terrain.bnt (125,064,817 bytes)…');
await mount.mountEra({
  era: ERAS.PCG_9_3_5,
  container: 'Terrain/terrain.bnt',
  path: TERRAIN_URL,
  format: 'BNT2_TERRAIN',
  verifyHash: true, // SHA256 enforced against KNOWN_HASHES (95841761…)
});
log('mounted + SHA-verified.');

// ---------- canonical tiles through PESourceMount ----------
const ORIGIN_X = 56, ORIGIN_Y = 112, N = 3;
const tiles = [];
for (let ty = ORIGIN_Y; ty < ORIGIN_Y + N; ty++) {
  const row = [];
  for (let tx = ORIGIN_X; tx < ORIGIN_X + N; tx++) {
    const t = await mount.getTerrainTile({ era: ERAS.PCG_9_3_5, gridX: tx, gridY: ty });
    row.push(t);
  }
  tiles.push(row);
}
log(`decoded 9 canonical tiles (${tiles[0][0].name} .. ${tiles[2][2].name}).`);

// ---------- PE Runtime Core: canonical region + geometry ----------
const region = new PETerrainRegion(tiles);
const geom = region.buildGeometry();

// per-tile heights sha256 (byte-faithfulness export — compared against the
// independent Node audit and the r169 oracle chunk binary)
const u16le = (h) => { const b = new Uint8Array(2048); const dv = new DataView(b.buffer);
  for (let i = 0; i < 1024; i++) dv.setUint16(i * 2, h[i], true); return b; };
const tileHashes = [];
for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
  tileHashes.push({ name: region.tiles[y][x].name, heightsSha256: await sha256Hex(u16le(region.tiles[y][x].heights)) });
}

// ---------- r185 render (calibrated baseline conventions) ----------
const W = 1024, H = 768;
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(1);
renderer.setSize(W, H);
renderer.setClearColor(0x0a0a12, 1);
document.getElementById('view').appendChild(renderer.domElement);

const scene = new THREE.Scene();
// World space: +X = grid x (meters), +Y = height (meters), +Z = grid y (meters).
const g = new THREE.BufferGeometry();
g.setAttribute('position', new THREE.BufferAttribute(geom.positions, 3));
g.setIndex(new THREE.BufferAttribute(geom.indices, 1));
g.computeVertexNormals();
const material = new THREE.MeshBasicMaterial({ color: 0x9a8f7a, wireframe: false });
const mesh = new THREE.Mesh(g, material);
scene.add(mesh);

const box = new THREE.Box3().setFromBufferAttribute(g.getAttribute('position'));
const center = box.getCenter(new THREE.Vector3());
const size = box.getSize(new THREE.Vector3());
const camera = new THREE.PerspectiveCamera(55, W / H, 1, 50000);
camera.up.set(0, 1, 0);
camera.position.set(center.x + size.x * 0.9, box.max.y + size.z * 0.55, center.z + size.z * 1.15);
camera.lookAt(center.x, center.y, center.z);
scene.add(new THREE.AxesHelper(200));

renderer.render(scene, camera);

// deterministic lights-free MeshBasicMaterial render: reproducible screenshot
const pngDataUrl = renderer.domElement.toDataURL('image/png');
const pngHash = await sha256Hex(Uint8Array.from(atob(pngDataUrl.split(',')[1]), c => c.charCodeAt(0)));

// ---------- results / provenance chain ----------
const provenance = region.provenanceList();
const result = {
  p0: 'clean pipeline 9-tile region render (PCG_9_3_5 primary, zero legacy runtime input)',
  chain: 'terrain.bnt bytes -> PESourceMount(BNT2_TERRAIN) -> TerrainTile -> PETerrainRegion -> r185 WebGLRenderer',
  mount: {
    era: ERAS.PCG_9_3_5, path: TERRAIN_URL, format: 'BNT2_TERRAIN',
    hashVerified: provenance[0].extra.hashVerified,
  },
  region: {
    originGridX: ORIGIN_X, originGridY: ORIGIN_Y, tilesX: N, tilesY: N,
    tileNames: tiles.flat().map(t => t.name),
    sampleGridX: geom.sampleGridX, sampleGridY: geom.sampleGridY,
    seamDiagnostic: region.tileSeamDiagnostic,
  },
  heightQuery: HEIGHT_QUERY,
  tileHeightsSha256: tileHashes,
  renderer: { threeRevision: THREE.REVISION, backend: 'WebGLRenderer', width: W, height: H },
  screenshotPngSha256: pngHash,
  provenanceSample: provenance[0],
  provenanceCount: provenance.length,
};
window.__P0__ = result;
window.__P0_PNG__ = pngDataUrl;
log(
`P0 RENDERED — ${geom.sampleGridX}x${geom.sampleGridY} samples, height ${box.min.y.toFixed(1)}..${box.max.y.toFixed(1)} m
screenshot sha256: ${pngHash}
tiles: ${result.region.tileNames.join(' ')}
provenance objects: ${provenance.length}/9 (era=${provenance[0].era}, hashVerified=${provenance[0].extra.hashVerified})`);
