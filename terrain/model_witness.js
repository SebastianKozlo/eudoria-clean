// model_witness.js — M1 ITER 051 (ledger ITER_037): THE ORIGINAL-DIRECT
// SINGLE-MODEL WITNESS (architect decision #3's chain, demonstrated for ONE
// model before ANY scaling — the witness rule; NO corpus, NO witness matrix).
//
// THE CHAIN (every step byte-anchored, era-labeled, provenance on the result):
//   ORIGINAL PCG_9_3_5 Models.bnt bytes (SHA-verified at mount, C950A8C2...)
//     -> PESourceMount.getModelResource(457485)   [BNT2 framing, entry + offset + size]
//     -> NifModelReader.parseWitnessModel        [clean v10.1.0.0 NIF reader; loud failures]
//     -> NiTriShape chain -> NiTriShapeData      [16 vertices / 8 triangles / 2 UV sets, bit-exact]
//     -> NiTexturingProperty BASE slot           [clamp=3, filter=2, uv_set=0, source=-1]
//     -> NiArkTextureExtraData entry              [the ERA binding: texture id in the trailing 9 bytes]
//     -> PESourceMount.resolveTexture(457490)     [era-explicit, PCG_9_3_5:Textures.bnt, SHA-verified]
//     -> TgaDecoder.decodeTga2A32Image            [TGA 2.0, 32bpp BGRA, image order]
//     -> THREE.DataTexture (flipY=false) + MeshBasicMaterial (vertex-shaded era technique)
//     -> deterministic render + reproducible hash
//
// THE WITNESS MODEL CHOICE (documented): 457485 — one of the 10 foliage
// climate-0 (0.vcl) col0 model ids ALREADY rendered on the foliage page (the
// most frequent rendered model, x20 in the ITER_033/035 census); the SMALLEST
// NIF of the 10 candidates (2,547 bytes, 16 blocks, ONE NiTriShape + ONE
// ArkTexture BASE entry — iter037_witness_select.json); its texture id
// 457490 resolves in the SAME-ERA Textures.bnt (457490.dat, TGA2 A32). This
// directly serves the foliage page's future switch to original-direct assets.
//
// HONEST BOUNDS (labeled — never silent approximations):
//   [P-UNITS] the NIF is in centimeters (the era m->cm x100 evidence,
//       FUN_0082b790); the render bridges cm->m x0.01 (as the foliage page).
//   [P-AXIS] NIF Z-up -> Three Y-up via (x, z, -y) — the SAME mapping the
//       deployed legacy GLB exporter documented (nif_glb_exporter_uvc_v1
//       "Coordinate system: NIF Z-up -> glTF Y-up (X, Z, -Y)"); the engine's
//       own NIF->world transform for vegetation models is NOT decompiled
//       (iter032 bound 5) — CURRENT_RUNTIME_CALIBRATION, not historical truth.
//   [P-UV] NIF uv used RAW (no V flip); texture rows top-first (image order);
//       DataTexture flipY=false -> v=0 samples the image TOP. Evidence: the
//       legacy UVConv v1 byte-probe (runtime_flipY_probe.json, the r169
//       runtime) + the witness model's own structure (card top v≈0.104,
//       card bottom v≈0.940; the dark ground-shadow vertex colors at z=0;
//       the texture's alpha structure: top-half mean 27.2, bottom-half 66.8).
//       A D3D8 runtime capture can falsify this — documented choice.
//   [P-MATERIAL] the model's NiArkShaderExtraData config ("effectfile
//       Vegetation, CullMethod 2, AlphaTreshold 111, EnableAnimation 1.0,
//       ModelAmpPlanar 5.0, ModelAmpHeight 5.0, ModelFreqScale 2.86") is the
//       era material/technique evidence (the 'Vegetation' technique = FX
//       0x3EC, vertex-shaded — iter032 stage 9). The render uses a FIXED
//       MeshBasicMaterial (vertex-shaded: texture x vertex colors, NO
//       dynamic lighting — deterministic); DoubleSide (CullMethod 2's exact
//       D3D8 cull mapping UNVERIFIED); no wind animation (the era's
//       EnableAnimation is a runtime effect, not a static render input) —
//       CURRENT_RUNTIME_CALIBRATION, not historical truth.
//   [P-MIPS] filter=2 (trilinear in the niflib enum) with DataTexture mip
//       generation OFF + LinearFilter (a deterministic subset choice; the
//       era's mip chain generation is not reproduced) — CURRENT_RUNTIME
//       CALIBRATION.
//   THE FILE TAIL: 8 bytes after the last NIF block (01 00 00 00 00 00 00 00)
//       — recorded raw, semantics UNKNOWN (labeled, not interpreted).

import * as THREE from 'three';
import { PESourceMount } from '../src/pesource/PESourceMount.js';
import { ERAS } from '../src/pesource/PEProvenance.js';
import { parseWitnessModel } from '../src/pesource/NifModelReader.js';
import { decodeTga2A32Image } from '../src/pesource/TgaDecoder.js';

const HUD = document.getElementById('hud');
const log = (m) => { HUD.textContent = m; console.log(m); };

async function fetchBytes(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`fetch ${url}: HTTP ${res.status}`);
  return new Uint8Array(await res.arrayBuffer());
}
async function sha256Hex(bytes) {
  const d = await crypto.subtle.digest('SHA-256', bytes);
  return [...new Uint8Array(d)].map(b => b.toString(16).padStart(2, '0')).join('').toUpperCase();
}
const io = { readFile: fetchBytes, inflate: async (b) => { throw new Error('not needed (BNT2 raw)'); }, sha256: sha256Hex };

// ---------- the witness model (documented choice — see header) ----------
const WITNESS_MODEL_ID = 457485;

// ---------- mounts (SHA-pinned, era-labeled) ----------
const mount = new PESourceMount(io);
await mount.mountEra({ era: ERAS.PCG_9_3_5, container: 'Models/Models.bnt',
  path: '/pcg/Data/Models/Models.bnt', format: 'BNT2', verifyHash: true });
await mount.mountEra({ era: ERAS.PCG_9_3_5, container: 'Textures.bnt',
  path: '/pcg/Data/Textures/Textures.bnt', format: 'BNT2', verifyHash: true });
log('mounted Models.bnt + Textures.bnt (SHA-verified, era PCG_9_3_5).');

// ---------- the model resource (ORIGINAL bytes + provenance) ----------
const modelRes = await mount.getModelResource({ era: ERAS.PCG_9_3_5, modelId: WITNESS_MODEL_ID });
log(`model entry ${WITNESS_MODEL_ID}.nif: ${modelRes.entry.size} bytes @${modelRes.entry.offset} (crc32 0x${modelRes.entry.crc32.toString(16)}).`);

// ---------- the clean NIF read (the witness reader — loud failures) ----------
const { extraction, renderModel } = parseWitnessModel(modelRes.payload, `${WITNESS_MODEL_ID}.nif`);
const payloadSha = await sha256Hex(modelRes.payload);
log(`NIF parsed: v${extraction.header.versionString}, ${extraction.blocks.length} blocks; payload sha256 ${payloadSha.slice(0, 16)}…`);

// ---------- the texture (the ERA Ark binding -> era-explicit resolveTexture) ----------
const textureId = renderModel.textureBinding.textureId;
const texRes = await mount.resolveTexture({ era: ERAS.PCG_9_3_5, container: 'Textures.bnt', textureId });
const texPayloadSha = await sha256Hex(texRes.payload);
const tex = decodeTga2A32Image(texRes.payload);
const texRgbaSha = await sha256Hex(tex.rgba);
log(`texture ${textureId}.dat (${tex.width}x${tex.height}x32 TGA2): entry ${texRes.entry.size} bytes @${texRes.entry.offset}; rgba sha256 ${texRgbaSha.slice(0, 16)}…`);

// ---------- the scene / mesh (decision #3: geometry -> material -> texture/UV -> render) ----------
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x14141c);

// [P-AXIS] NIF Z-up -> Three Y-up: (x, y, z) -> (x, z, -y); [P-UNITS] cm -> m.
const UNIT_BRIDGE = 0.01;
const n = renderModel.numVertices;
const positions = new Float32Array(n * 3);
for (let i = 0; i < n; i++) {
  positions[i * 3] = renderModel.positions[i * 3] * UNIT_BRIDGE;
  positions[i * 3 + 1] = renderModel.positions[i * 3 + 2] * UNIT_BRIDGE;   // NIF z -> up
  positions[i * 3 + 2] = -renderModel.positions[i * 3 + 1] * UNIT_BRIDGE;  // NIF y -> -z
}
const geometry = new THREE.BufferGeometry();
geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
if (renderModel.normals) {
  const normals = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) {
    normals[i * 3] = renderModel.normals[i * 3];
    normals[i * 3 + 1] = renderModel.normals[i * 3 + 2];
    normals[i * 3 + 2] = -renderModel.normals[i * 3 + 1];
  }
  geometry.setAttribute('normal', new THREE.BufferAttribute(normals, 3));
}
// [P-UV] RAW NIF uv set 0 (the BASE slot's uv_set=0), NO V flip.
geometry.setAttribute('uv', new THREE.BufferAttribute(new Float32Array(renderModel.uvSets[0]), 2));
if (renderModel.colors) {
  geometry.setAttribute('color', new THREE.BufferAttribute(new Float32Array(renderModel.colors), 4));
}
geometry.setIndex(new THREE.BufferAttribute(renderModel.index, 1));

// The era texture as a DataTexture (top-first image rows; flipY=false -> v=0 = image top).
// colorSpace = NoColorSpace passthrough — the established page convention
// (materials_confirmed.js makeTexture; the r185 calibration record).
const texture = new THREE.DataTexture(tex.rgba, tex.width, tex.height, THREE.RGBAFormat);
texture.colorSpace = THREE.NoColorSpace;
texture.flipY = false;
texture.wrapS = THREE.RepeatWrapping;   // clamp=3 -> WRAP_S_WRAP_T (niflib TexClampMode)
texture.wrapT = THREE.RepeatWrapping;
texture.minFilter = THREE.LinearFilter; // [P-MIPS] documented deterministic subset
texture.magFilter = THREE.LinearFilter;
texture.needsUpdate = true;

// [P-MATERIAL]: fixed vertex-shaded material (texture x vertex colors, deterministic).
const alphaThreshold = renderModel.alpha ? renderModel.alpha.threshold : 0;
const alphaBlendOn = renderModel.alpha ? (renderModel.alpha.flags & 1) === 1 : false;
const material = new THREE.MeshBasicMaterial({
  map: texture,
  vertexColors: !!renderModel.colors,
  transparent: alphaBlendOn,
  alphaTest: alphaThreshold / 255.0,
  side: THREE.DoubleSide,
});
const mesh = new THREE.Mesh(geometry, material);
scene.add(mesh);

// Fixed deterministic camera, derived from the PARSED geometry (center/radius
// from the NIF bytes — deterministic; no user input).
const centerM = renderModel.center.map(v => v * UNIT_BRIDGE);
const camDist = renderModel.radius * UNIT_BRIDGE * 2.6;
const camera = new THREE.PerspectiveCamera(50, 16 / 9, 0.01, 100);
camera.position.set(centerM[0] + camDist * 0.55, centerM[1] + camDist * 0.42, centerM[2] + camDist * 0.72);
camera.lookAt(centerM[0], centerM[1], centerM[2]);

const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setSize(1280, 720);
document.getElementById('view').appendChild(renderer.domElement);

// ---------- the deterministic render ----------
// ?model-off hides the mesh BEFORE the single deterministic render (the
// visibility pixel-diff audit — anti-success-theater: the "the model renders"
// claim must not rest on a hash that could be background-only).
if (new URLSearchParams(location.search).has('model-off')) mesh.visible = false;

renderer.render(scene, camera);
const png1 = renderer.domElement.toDataURL('image/png');
renderer.render(scene, camera);
const png2 = renderer.domElement.toDataURL('image/png');
const deterministic = png1 === png2;
const enc = new TextEncoder();
const renderHash = await sha256Hex(enc.encode(png1));

// ---------- the result (the full provenance chain + the canonical extraction) ----------
const result = {
  p0: 'ORIGINAL-DIRECT single-model witness (decision #3): one model parsed from the era Models.bnt NIF bytes through the clean reader, textured with the era Textures.bnt payload, rendered deterministically',
  chain: 'Models.bnt (SHA-verified) -> getModelResource(457485) -> NifModelReader (v10.1.0.0, loud) -> NiTriShape/NiTriShapeData -> NiTexturingProperty BASE slot -> NiArkTextureExtraData id -> resolveTexture(457490, PCG_9_3_5:Textures.bnt) -> decodeTga2A32Image -> DataTexture(flipY=false) -> MeshBasicMaterial(vertex-shaded) -> deterministic render',
  witnessChoice: {
    modelId: WITNESS_MODEL_ID,
    justification: 'one of the 10 foliage climate-0 (0.vcl) col0 ids ALREADY rendered on the foliage page (x20 in the ITER_033/035 census — the most frequent); the SMALLEST NIF of the 10 candidates (2,547 bytes, 16 blocks, ONE NiTriShape + ONE ArkTexture BASE entry, iter037_witness_select.json); serves the foliage page\'s future original-direct switch',
  },
  provenance: {
    era: 'PCG_9_3_5',
    modelContainer: { container: 'Models/Models.bnt', sha256Verified: true,
      path: 'D:/Eudoria_Reconstruction/pcg_install/Data/Models/Models.bnt' },
    modelEntry: modelRes.provenance,
    modelPayloadSha256: payloadSha,
    nifVersion: extraction.header.versionString,
    blockCount: extraction.blocks.length,
    textureContainer: { container: 'Textures.bnt', sha256Verified: true,
      path: 'D:/Eudoria_Reconstruction/pcg_install/Data/Textures/Textures.bnt' },
    textureEntry: texRes.provenance,
    texturePayloadSha256: texPayloadSha,
    textureRgbaImageOrderSha256: texRgbaSha,
  },
  nifExtraction: extraction,
  renderModel: {
    shapeName: renderModel.shapeName,
    numVertices: renderModel.numVertices,
    numTriangles: renderModel.numTriangles,
    uvSetCount: renderModel.uvSets.length,
    textureBinding: renderModel.textureBinding,
    material: renderModel.material,
    alpha: renderModel.alpha,
    centerCm: renderModel.center,
    radiusCm: renderModel.radius,
  },
  texture: {
    tgaHeader: tex.header,
    rowOrder: tex.rowOrder,
    width: tex.width, height: tex.height,
    rgbaImageOrderSha256: texRgbaSha,
  },
  placeholders: {
    'P-UNITS': 'NIF cm -> render m x0.01 (the era m->cm x100 evidence FUN_0082b790)',
    'P-AXIS': 'NIF Z-up -> Three Y-up (x, z, -y) — the legacy-exporter-documented mapping; the engine transform not decompiled (iter032 bound 5) — CURRENT_RUNTIME_CALIBRATION',
    'P-UV': 'RAW NIF v (no flip) + top-first image rows + DataTexture flipY=false -> v=0 = image TOP (legacy UVConv v1 byte-probe + the witness card structure: top v≈0.104, bottom v≈0.940) — documented choice, falsifiable by a D3D8 capture',
    'P-MATERIAL': 'fixed MeshBasicMaterial (vertex-shaded: texture x vertex colors; the era technique = FX 0x3EC "Vegetation", vertex-shaded); DoubleSide (CullMethod 2 exact mapping UNVERIFIED); no wind animation — CURRENT_RUNTIME_CALIBRATION',
    'P-MIPS': 'filter=2 (trilinear enum) rendered as LinearFilter + mip generation OFF (deterministic subset) — CURRENT_RUNTIME_CALIBRATION',
    'FILE-TAIL': `${extraction.fileTailBytesLen} bytes after the last block: ${extraction.fileTailBytesHex} — semantics UNKNOWN (recorded raw)`,
  },
  render: {
    deterministicInPage: deterministic,
    sha256: renderHash,
    width: 1280, height: 720,
    threeRevision: THREE.REVISION,
    modelVisible: mesh.visible,
  },
};
window.__iter037_result = result;
window.__iter037_png__ = png1;

log(
`ORIGINAL-DIRECT MODEL WITNESS (ITER 051 / ledger ITER_037) — model ${WITNESS_MODEL_ID} rendered from the era NIF bytes
render sha256: ${renderHash}   deterministic in-page: ${deterministic}
chain: Models.bnt -> 457485.nif (${modelRes.entry.size} B @${modelRes.entry.offset}) -> NIF v${extraction.header.versionString} (${extraction.blocks.length} blocks)
      -> NiTriShape "default624:0" -> NiTriShapeData (${n} verts / ${renderModel.numTriangles} tris / ${renderModel.uvSets.length} UV sets)
      -> NiTexturingProperty BASE (clamp ${renderModel.textureBinding.baseSlot.clamp}, filter ${renderModel.textureBinding.baseSlot.filter}, uv_set ${renderModel.textureBinding.baseSlot.uvSet}, source ${renderModel.textureBinding.baseSlot.source})
      -> NiArkTextureExtraData "${renderModel.textureBinding.arkEntryName}" -> texture id ${textureId}
      -> Textures.bnt 457490.dat (${texRes.entry.size} B @${texRes.entry.offset}) -> TGA2 A32 ${tex.width}x${tex.height} -> DataTexture(flipY=false)
model payload sha256: ${payloadSha}
texture payload sha256: ${texPayloadSha}   rgba(image-order) sha256: ${texRgbaSha}
era: PCG_9_3_5 — both containers SHA-verified at mount (Models.bnt C950A8C2…, Textures.bnt 61ACD13B…)
honest bounds: P-UNITS cm->m 0.01 | P-AXIS (x,z,-y) | P-UV raw v + top-first rows (v=0 = image top) | P-MATERIAL vertex-shaded fixed | P-MIPS linear no-mips`);
