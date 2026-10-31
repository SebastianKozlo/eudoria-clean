// character_preview.js — JOB W18_CHARACTER_PREVIEW (attempt W18_a1, 2026-10-30/31).
//
// Local character preview: the REAL 2003 avatar candidate (Models.ark member
// 208861 — VREG REPORT §5 example-evidence member of the 207222–208861 family,
// full Bip01_face_cd_* morph-bone signature + 'Bip01 Ponytail1' hair bone)
// rendered from the W09 dedicated NIF 4.1.0.12 adapter IR (era dispatch: the
// SAME minimal header sniff as inspector.js — 0x0401000C -> parseModel41;
// anything else LOUD-FAILs, no second parser), plus the RECOVERED hair
// mapping (6052.obj Hair::GetMeshId/GetTexture registry, 34 meshes = 2
// gender arrays × 17; mesh↔texture pairing per CHAR_G
// PALETTE_MAPS_HAIR_V7.csv item_index 0 of BOTH arrays — V7 CORRECTED
// GENDER: W18/CHAR_F paired male mesh 32498 with tex@636 (FEMALE table)
// and female mesh 32509 with tex@800 (MALE table) — the textures were
// SWAPPED. Byte-proven 6052 dispatch (CHAR_G): GetMeshId [this+0]==1 ->
// mesh CODE+96 (MALE), ==2 -> CODE+248 (FEMALE); GetTexture ==2 -> tex
// CODE+636 (FEMALE), ==1 -> tex CODE+800 (MALE). W25 re-pair (this job):
// male = mesh 32498 + texture 216257; female = mesh 32509 + texture 216302.
//
// HONESTY CONTRACT (every unsupported item is listed, nothing is faked):
//   - NO fictional sliders: the 21 recovered creator controls are LISTED
//     with CHAR_F V6 statuses (RANGE_RECOVERED_CHAR_F / ENGINE_DEPENDENT)
//     — strings only; no morph-target runtime proof exists yet (R1).
//   - Hair meshes render SEPARATELY (side-by-side + toggle) — NOT attached
//     to the avatar: there is NO proof of the head-attachment position in R1
//     (skin/morph semantics pending; NiKeyframeController/NiKeyframeData/
//     NiSkinInstance/NiSkinData/NiArk* are OPAQUE in the adapter).
//   - Avatar 208861 parses with 549 blocks; 143 OPAQUE (NiKeyframeController
//     70, NiKeyframeData 70, NiArk* 3) — census shown verbatim.
//   - Hair meshes parse to geometry+UV then STOP (STOPPED_OPAQUE_NO_BOUNDARY
//     at NiSkinInstance/NiSkinData) — the geometry rendered IS the parsed IR,
//     the stop is displayed, never hidden.
//   - Texture: era TGA (24bpp BGR 64×128, Textures.ark member, TGA 2.0
//     footer) decoded by the STRICT TgaDecoder (W05 pattern) and applied to
//     the hair mesh ONLY where UVs are parsed; if not -> 'untextured (UV
//     pending)'.
//   - Source labels: payloads = STRICT_ISO extracted (SHA-pinned corpus
//     members, derived copies served read-only via server EXACT_ROUTES);
//     presentation = REFERENCE stage (diagnostic axes/grid, NOT the PE
//     environment).
//
// [P-UNITS]/[P-AXIS] CURRENT_RUNTIME_CALIBRATION (model_witness.js /
// inspector.js parity): NIF cm -> m ×0.01; NIF Z-up -> Three Y-up (x, z, -y).

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { parseModel41 } from '../src/pesource/NifModelReader41.js';
import { decodeTga2 } from '../src/pesource/TgaDecoder.js';

// ---------- payload registry (this run's extraction, EXTRACT_MANIFEST.json) ----------
const AVATAR = {
  id: '208861', url: '/assets/avatar/208861.nif', size: 205459,
  sha256: '0C37505EAFD9C1E14D9D834D8D30321AA9FA115D7767293A9A2ED50A7D4DAECF',
  era: 'PE2003_CD_JAN2003 (Models.ark member, STRICT_ISO-extracted)',
  family: '207222–208861 (VREG REPORT §5 primary avatar family; 208860/208861 = likely gender pair — WHICH gender is UNPROVEN)',
};
// W25 V7 re-pair: texture ids/shas SWAPPED vs W18 (mesh↔texture now both
// from the SAME gender array per PALETTE_MAPS_HAIR_V7.csv — W18 had male
// mesh + female texture and vice versa). Meshes unchanged (they were
// already correctly gendered by GetMeshId).
const HAIR = [
  {
    key: 'A', id: '32498', url: '/assets/hair/32498.nif', size: 19776,
    sha256: '9EFD4051172ABE4E5D725DBC4D5F488FD1522EE3853F235EBD5CEE6A6B7EA9BC',
    gender: 'MALE (gender_array 1)',
    texId: '216257', texUrl: '/assets/hair/216257.tga',
    texSha256: '367536D833BED0EA81901BDDBDEE2FB1E489A55B91D35ED4DFFAD756401FAFAE',
    array: 'gender_array 1 = MALE (6052 Hair::GetMeshId [this+0]==1 -> mesh CODE+96; Hair::GetTexture ==1 -> texture CODE+800 — CHAR_G byte-proven, PALETTE_MAPS_HAIR_V7)',
  },
  {
    key: 'B', id: '32509', url: '/assets/hair/32509.nif', size: 20420,
    sha256: '9D3CF3B8D0BC96A223324DBA388DA98DD4EDD8F38B5918579505C935CBA08A88',
    gender: 'FEMALE (gender_array 2)',
    texId: '216302', texUrl: '/assets/hair/216302.tga',
    texSha256: '5FB155FEAC694EF5FE24AED4F9948F4F6EF19D87A83AC7B652DDBEA1F6FAD863',
    array: 'gender_array 2 = FEMALE (6052 Hair::GetMeshId [this+0]==2 -> mesh CODE+248; Hair::GetTexture ==2 -> texture CODE+636 — CHAR_G byte-proven, PALETTE_MAPS_HAIR_V7)',
  },
];

// W27 (ADDITIVE SECTION, attempt W27_a1, 2026-10-31): the 20 head-appearance
// candidate TGAs — 6051 MESH_TABLE head ids physically resolved by W26 to
// Textures.ark members (128x128, uncompressed truecolor imageType 2, 24bpp
// BGR, TGA 2.0 footer, constant 49196 B). Extracted STRICT_ISO this run
// (corpus SHA-pinned D611D125…); payloads served read-only via server
// EXACT_ROUTES (/assets/head/<id>.tga). SEMANTICS: HYPOTHESIS ONLY —
// appearance-map role (face / skin / mask / hair-color) is UNVERIFIED;
// see W27_TGA_STATS.json for the raw byte statistics behind the hypotheses.
// `preview: true` = the 6 rendered as canvas previews; ALL 20 are
// fetched + SHA-verified + listed in the stats table.
// sha256 = the run's REAL payload SHAs (W27_TGA_STATS.json, extraction of
// 2026-10-31) — verified again in main() against the served bytes.
const HEAD_APPEARANCE = [
  { id: '27697',  preview: true,  sha256: '6BFC6E96F54FF23C5E3FB05E7F70AAFEB69AA1B64EE493957263D50349CA2EF0' },
  { id: '19704',  preview: true,  sha256: 'DF3811D95AD3A7D36005410769F3C572B0EFC2A1B16BD80AF7B4FC6D0EDCB369' },
  { id: '19705',  preview: false, sha256: 'AC551D01F898A516D76385BE65ABC8652F9D1842A4CFB2F47A40205DF309C7D7' },
  { id: '19706',  preview: false, sha256: '8930B89B18370D47923FB68CDD251930A8E498D6DBEA69EB1665D6F2A52A2683' },
  { id: '19707',  preview: false, sha256: '0ED80FD074C16441041DE001296CB27DEB6DCC39FB26D3435E508421EAF7AC2C' },
  { id: '19708',  preview: false, sha256: '7B3F5FFECDE4420B77725EDE066ABA6DDDF53697FBA517419F6170BF7D4B1894' },
  { id: '4336',   preview: true,  sha256: '8466C099C95CF7C050AFAE2BB16B4D7D6BAD89BAD2A3B131D13B4FA669F3CBAC' },
  { id: '5691',   preview: true,  sha256: '751ADAE93A6CF757B38217D2B691E55B04828479FEE7168F222542DCB9E0E356' },
  { id: '5989',   preview: false, sha256: '88BF02E6723AFABF81EB2B1A4C2CAB2CF22AF3552CA0DF99763B3A0636554FA6' },
  { id: '5990',   preview: false, sha256: '60A195BFAEC0CA538107DA95A5AAD280E5BE1FB16B78ECACB044DA50F61C7F90' },
  { id: '5991',   preview: false, sha256: 'BBBEF307C75BCF598239BE818BDC610C5C019A43B717E77A59C5C753C401EC7B' },
  { id: '5997',   preview: false, sha256: '70D46B7F708708B56CCBB6B4233ECB4C34EF8531E9B8F653562E764531D814A7' },
  { id: '6081',   preview: false, sha256: 'CC1D8BFB9418D998EA618C842581F6AEC731468EDC67D3451754E728DCBECEA0' },
  { id: '6082',   preview: false, sha256: '7A7E9CCECE46287CAC619514A97FD53260D5745395601624380A04E505A6B488' },
  { id: '187058', preview: true,  sha256: '851DD209052BB4D2C494A2C4C82850CEB9BE027D05F03CAB95F0888607C8BCD4' },
  { id: '187059', preview: false, sha256: '19ED06260B2DF6ADF5FFE487AFD90C46BAA82BBA6B42D1727AC6F1F95366987B' },
  { id: '187060', preview: false, sha256: '651C5A5202E88844B706A9C2DD35713B78CCB6795160BBE5D2DD837D3C027A51' },
  { id: '187061', preview: false, sha256: 'DD27703E8ED557F53CF96FE33D53D626655BAE20E5895DD75CD974BA0EFF1655' },
  { id: '216925', preview: true,  sha256: '8CEC5E5F5B58FDB9E396FFD586F39FE8A6F25C0B8D87F3BFB24DCC65B9B54823' },
  { id: '216926', preview: false, sha256: '654F7BB4E2C97AA81DCEA20ECC109F14E5C979DC12741136B31154341ACB97E5' },
];

// 21 recovered creator controls (CHAR_A/CHAR_C labels; CHAR_F §6 V6 statuses).
// Strings ONLY — no working sliders (no morph-target runtime proof in R1).
const CONTROLS_21 = [
  { label: 'Skin color',  status: 'ENGINE_DEPENDENT', note: 'palette host-side; skin registry scripts 5509/5504 unclassified (CHAR_G pending)' },
  { label: 'Hair color',  status: 'ENGINE_DEPENDENT', note: 'hair palette → texture ids RECOVERED (6052); color palette host-side' },
  { label: 'Eye color',    status: 'ENGINE_DEPENDENT', note: 'palette host-side' },
  { label: 'Hair type',    status: 'RANGE_RECOVERED_CHAR_F', note: '17 items × 2 gender arrays (6052 cross-script); item strings NOT in 1883' },
  { label: 'Face type',    status: 'ENGINE_DEPENDENT', note: 'bounds not in 1883' },
  { label: 'Hair volume',  status: 'ENGINE_DEPENDENT', note: 'bounds not in 1883' },
  { label: 'Constitution', status: 'ENGINE_DEPENDENT', note: 'bounds not in 1888/1883' },
  { label: 'Length and Proportions', status: 'ENGINE_DEPENDENT', note: 'bounds not in 1883' },
  { label: 'Chest size',   status: 'ENGINE_DEPENDENT', note: 'bounds not in 1883' },
  { label: 'Eyes1',        status: 'ENGINE_DEPENDENT', note: 'bounds not in 1883' },
  { label: 'Eyes2',        status: 'ENGINE_DEPENDENT', note: 'bounds not in 1883' },
  { label: 'Ear position', status: 'ENGINE_DEPENDENT', note: 'bounds not in 1883' },
  { label: 'Ear angle/size', status: 'ENGINE_DEPENDENT', note: 'bounds not in 1883' },
  { label: 'Cheeks',       status: 'ENGINE_DEPENDENT', note: 'bounds not in 1883' },
  { label: 'Cheekbones',  status: 'ENGINE_DEPENDENT', note: 'bounds not in 1883' },
  { label: 'Chin',         status: 'ENGINE_DEPENDENT', note: 'bounds not in 1883' },
  { label: 'Forehead',     status: 'ENGINE_DEPENDENT', note: 'bounds not in 1883' },
  { label: 'Size',         status: 'RANGE_RECOVERED_CHAR_F', note: '0..299 (creator 211689: RANDOM(299) default — COMPUTED_RUNTIME)' },
  { label: 'Nose1',        status: 'ENGINE_DEPENDENT', note: 'bounds not in 1883' },
  { label: 'Nose2',        status: 'ENGINE_DEPENDENT', note: 'bounds not in 1883' },
  { label: 'Mouth',        status: 'ENGINE_DEPENDENT', note: 'bounds not in 1883' },
];

// Attachment slots — 635.obj (CharDef) MESH-SECTION names for CharDef::250323
// (set mesh) — CHAR_F §4: inline strings in 635; NO runtime attachment proof.
const SLOTS_635 = ['head', 'hair', 'face', 'hand', 'forearm', 'torso', 'upperarm', 'leg', 'calf', 'foot'];

const state = {
  job: 'W18_CHARACTER_PREVIEW', attempt: 'W18_a1',
  status: 'LOADING', avatarStatus: '—',
  revision: null, errors: [],
  avatarShaVerified: false, hairShaVerified: {}, hairTexShaVerified: {},
  numBlocks: null, typeCounts: {}, opaqueTypes: {}, parseStatus: null,
  shapes: null, vertices: null, triangles: null,
  hairVisible: { A: true, B: true },
  hairStatus: {}, hairTexStatus: {},
  // W27 additive fields (head appearance candidates)
  headVisible: true, headStatus: {}, headTexShaVerified: {},
  headDecodedCount: 0, headStatusLine: 'LOADING',
  done: false,
};
window.__W18_STATE__ = state;
window.__W18_ERRORS__ = state.errors;
// W27 mirror state (independent namespace — additive, consumed by gates)
window.__W27_STATE__ = {
  job: 'W27_HEAD_APPEARANCE_DECODE', attempt: 'W27_a1',
  headIds: HEAD_APPEARANCE.map(h => h.id),
  headVisible: state.headVisible, headDecodedCount: 0,
  headTexShaVerified: {}, headStatus: 'LOADING', errors: [],
};

const el = (id) => document.getElementById(id);
const panel = el('panel');

async function fetchBuf(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`fetch ${url} -> HTTP ${r.status}`);
  return new Uint8Array(await r.arrayBuffer());
}
async function sha256hex(buf) {
  const h = await crypto.subtle.digest('SHA-256', buf);
  return [...new Uint8Array(h)].map(b => b.toString(16).padStart(2, '0')).join('').toUpperCase();
}

// ---------- era dispatch (inspector.js parity: minimal header sniff) ----------
function parseAvatarEra(payload, name) {
  const nl = payload.indexOf(0x0a);
  if (nl < 0) throw new Error('no newline in header — LOUD FAIL');
  const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  const version = dv.getUint32(nl + 1, true);
  if (version === 0x0401000C) return parseModel41(payload, name);
  throw new Error(`[W18 era dispatch] NIF version 0x${version.toString(16)} — NOT the 4.1.0.12 avatar era; LOUD FAIL (no second parser)`);
}

// ---------- 3D viewport (REFERENCE ASSET STAGE — Three r187) ----------
let renderer, scene, camera, controls;
function initViewport() {
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x14141c);
  const w = el('viewwrap').clientWidth || 640, h = el('viewwrap').clientHeight || 480;
  camera = new THREE.PerspectiveCamera(50, w / h, 0.01, 1000);
  renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  renderer.setSize(w, h);
  el('view').appendChild(renderer.domElement);
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  const axes = new THREE.AxesHelper(1.0);
  scene.add(axes);
  const grid = new THREE.GridHelper(4, 8, 0x334155, 0x1e293b);
  scene.add(grid);
  window.addEventListener('resize', () => {
    const W = el('viewwrap').clientWidth || 640, H = el('viewwrap').clientHeight || 480;
    camera.aspect = W / H; camera.updateProjectionMatrix(); renderer.setSize(W, H);
  });
  renderer.setAnimationLoop(() => { controls.update(); renderer.render(scene, camera); });
}

/** [P-UNITS] cm->m ×0.01; [P-AXIS] Z-up->Y-up (x, z, -y). Per-shape WORLD TRS
 * (NiTransform compose parity, rotation transposed for column-vector THREE)
 * — inspector.js addRenderModel41 parity. Returns the meshes added. */
function addShapes(renderModel, opts = {}) {
  const UNIT = 0.01;
  const group = new THREE.Group();
  group.name = opts.groupName || 'nif41';
  for (const sh of renderModel.shapes) {
    const n = sh.numVertices;
    const positions = new Float32Array(n * 3);
    for (let i = 0; i < n; i++) {
      positions[i * 3] = sh.positions[i * 3] * UNIT;
      positions[i * 3 + 1] = sh.positions[i * 3 + 2] * UNIT;
      positions[i * 3 + 2] = -sh.positions[i * 3 + 1] * UNIT;
    }
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    if (sh.normals) {
      const normals = new Float32Array(n * 3);
      for (let i = 0; i < n; i++) {
        normals[i * 3] = sh.normals[i * 3];
        normals[i * 3 + 1] = sh.normals[i * 3 + 2];
        normals[i * 3 + 2] = -sh.normals[i * 3 + 1];
      }
      geometry.setAttribute('normal', new THREE.BufferAttribute(normals, 3));
    }
    const hasUV = !!(sh.uvSets && sh.uvSets[0] && sh.uvSets[0].length);
    if (hasUV) geometry.setAttribute('uv', new THREE.BufferAttribute(new Float32Array(sh.uvSets[0]), 2));
    if (sh.colors) geometry.setAttribute('color', new THREE.BufferAttribute(new Float32Array(sh.colors), 4));
    geometry.setIndex(new THREE.BufferAttribute(sh.index, 1));
    const alphaThreshold = sh.alphaProp ? sh.alphaProp.threshold : 0;
    const alphaBlendOn = sh.alphaProp ? (sh.alphaProp.flags & 1) === 1 : false;
    const material = new THREE.MeshBasicMaterial({
      vertexColors: !!sh.colors, transparent: alphaBlendOn,
      alphaTest: alphaThreshold / 255.0, side: THREE.DoubleSide,
    });
    if (opts.texture && hasUV) {
      material.map = opts.texture;
      material.needsUpdate = true;
    } else if (sh.material) {
      material.color.setRGB(sh.material.diffuse[0], sh.material.diffuse[1], sh.material.diffuse[2]);
    } else {
      material.color.set(opts.flatColor ?? 0x9aa3b0);
    }
    const mesh = new THREE.Mesh(geometry, material);
    mesh.name = `${group.name}:${sh.shapeName}`;
    const w = sh.worldTRS;
    const m = new THREE.Matrix4();
    m.set(
      w.rotation[0][0], w.rotation[1][0], w.rotation[2][0], w.translation[0] * UNIT,
      w.rotation[0][2], w.rotation[1][2], w.rotation[2][2], w.translation[2] * UNIT,
      -w.rotation[0][1], -w.rotation[1][1], -w.rotation[2][1], -w.translation[1] * UNIT,
      0, 0, 0, w.scale,
    );
    mesh.matrixAutoUpdate = false;
    mesh.matrix.copy(m);
    group.add(mesh);
  }
  scene.add(group);
  return group;
}

function frameOn(center, radius) {
  const camDist = Math.max(radius * 2.6, 0.5);
  camera.position.set(center[0] + camDist * 0.55, center[1] + camDist * 0.42, center[2] + camDist * 0.72);
  camera.near = Math.max(camDist / 1000, 0.001);
  camera.far = camDist * 50;
  camera.updateProjectionMatrix();
  controls.target.set(center[0], center[1], center[2]);
  el('viewmsg').textContent = '';
}

// overall bounds (meters, Y-up bridged) from per-shape center/radius
function boundsOf(renderModel) {
  const UNIT = 0.01;
  const centers = renderModel.shapes.map(sh => [sh.center[0] * UNIT, sh.center[2] * UNIT, -sh.center[1] * UNIT]);
  let cx = 0, cy = 0, cz = 0;
  for (const c of centers) { cx += c[0]; cy += c[1]; cz += c[2]; }
  if (centers.length) { cx /= centers.length; cy /= centers.length; cz /= centers.length; }
  let maxR = 0;
  for (let i = 0; i < renderModel.shapes.length; i++) {
    const d = Math.hypot(centers[i][0] - cx, centers[i][1] - cy, centers[i][2] - cz) + renderModel.shapes[i].radius * UNIT;
    if (d > maxR) maxR = d;
  }
  return { center: [cx, cy, cz], radius: Math.max(maxR, 0.1) };
}

// ---------- hair toggle ----------
const hairGroups = {};
function toggleHair(key) {
  state.hairVisible[key] = !state.hairVisible[key];
  const g = hairGroups[key];
  if (g) g.visible = state.hairVisible[key];
  const btn = el(`btn-hair-${key}`);
  if (btn) {
    btn.classList.toggle('off', !state.hairVisible[key]);
    btn.textContent = `hair ${key} (mesh ${HAIR.find(x => x.key === key).id}, ${HAIR.find(x => x.key === key).gender.split(' (')[0]}): ${state.hairVisible[key] ? 'VISIBLE' : 'hidden'}`;
  }
  updateBadges();
}
window.__W18_TOGGLE_HAIR__ = toggleHair;

// ---------- W27 head appearance candidates (ADDITIVE — toggle + canvases) ----------
const headDecoded = {}; // id -> { width, height, rgba } (decodeTga2 output)
function toggleHeadAppearances() {
  state.headVisible = !state.headVisible;
  window.__W27_STATE__.headVisible = state.headVisible;
  const sec = el('head-appear-section');
  if (sec) sec.style.display = state.headVisible ? '' : 'none';
  const btn = el('btn-head-appearance');
  if (btn) {
    btn.classList.toggle('off', !state.headVisible);
    btn.textContent = `head appearance candidates (${HEAD_APPEARANCE.length} TGA): ${state.headVisible ? 'VISIBLE' : 'hidden'}`;
  }
}
window.__W27_TOGGLE_HEAD__ = toggleHeadAppearances;

function drawHeadCanvases() {
  for (const h of HEAD_APPEARANCE) {
    if (!h.preview) continue;
    const cv = el(`head-canvas-${h.id}`);
    const d = headDecoded[h.id];
    if (!cv || !d) continue;
    cv.width = d.width; cv.height = d.height;
    const ctx = cv.getContext('2d');
    ctx.putImageData(new ImageData(new Uint8ClampedArray(d.rgba), d.width, d.height), 0, 0);
    cv.dataset.drawn = 'Y';
  }
}

function renderHeadSectionHtml() {
  const previews = HEAD_APPEARANCE.filter(h => h.preview);
  let html = `<h3>HEAD APPEARANCE CANDIDATES (W27 — ${HEAD_APPEARANCE.length} TGA, semantics HYPOTHESIS)</h3>
  <div class="warnbox">HYPOTHESIS — semantics UNVERIFIED: whether these are faces / skin tone maps / masks / hair-color maps is NOT proven. What IS proven: 6051 MESH_TABLE head ids resolve to these Textures.ark members (W26), 128×128, uncompressed truecolor (imageType 2), 24bpp BGR, TGA 2.0 footer, constant 49,196 B, NO alpha channel. Source: STRICT_ISO members, era ISO_5_1_0_0 (PC Gamer Nov2003 install corpus, Textures.ark SHA-pinned D611D125…). Byte statistics + hypotheses: W27_TGA_STATS.json.</div>
  <div id="head-appear-section">
  <div class="note">canvas previews (${previews.length} of ${HEAD_APPEARANCE.length}; ALL 20 fetched + SHA-verified):</div>
  <div style="display:flex;flex-wrap:wrap;gap:8px;margin:4px 0 8px 0;">`;
  for (const h of previews) {
    const ok = state.headTexShaVerified[h.id];
    html += `<div style="border:1px solid #444;padding:4px;text-align:center;">
      <canvas id="head-canvas-${h.id}" class="head-tga-canvas" data-head-id="${h.id}" data-head-sha="${h.sha256}" data-head-sha-verified="${ok ? 'Y' : 'N'}" style="width:112px;height:112px;image-rendering:pixelated;border:1px solid #222;background:#000;"></canvas>
      <div style="margin-top:3px;"><b>${h.id}.tga</b> <span class="${ok ? 'st' : 'honest'}" style="font-family:monospace;">SHA ${h.sha256.slice(0, 10)}… v=${ok ? 'Y' : 'N'}</span></div>
      <div class="badge warn" style="display:inline-block;margin-top:2px;">HYPOTHESIS</div>
      <div class="note" style="font-size:10px;">STRICT_ISO member · era ISO_5_1_0_0</div>
    </div>`;
  }
  html += `</div><table>`;
  for (const h of HEAD_APPEARANCE) {
    const ok = state.headTexShaVerified[h.id];
    const st = state.headStatus[h.id] ?? (ok ? 'DECODED' : '—');
    html += `<tr><td class="k">${h.id}.tga</td><td>${st} · SHA ${h.sha256.slice(0, 16)}… <span class="${ok ? 'st' : 'honest'}">verified=${ok ? 'Y' : 'N'}</span></td></tr>`;
  }
  html += `</table><div class="note">head section total: ${state.headDecodedCount}/${HEAD_APPEARANCE.length} decoded — <span class="honest">${state.headStatusLine}</span></div>
  <button id="btn-head-appearance">head appearance candidates (${HEAD_APPEARANCE.length} TGA): ${state.headVisible ? 'VISIBLE' : 'hidden'}</button>
  <div class="note">toggle = visibility of this section only (hair/avatar above are unaffected). Raw statistics recorded in W27_TGA_STATS.json; hypotheses are labeled HYPOTHESIS and are NOT facts.</div>
  </div>`;
  return html;
}

function updateBadges() {
  const setB = (id, html, cls) => { const b = el(id); b.innerHTML = html; if (cls !== undefined) b.className = cls; };
  setB('b-era', `era: <b>${AVATAR.era}</b>`, 'badge ref');
  setB('b-format', `format: <b>${state.formatVersion ?? '—'}</b>`);
  setB('b-revision', `three: <b>r${THREE.REVISION}</b>`);
  setB('b-sha', `avatar sha256: <b>${AVATAR.sha256.slice(0, 12)}…</b> verified=${state.avatarShaVerified ? 'Y' : 'N'}`);
  const stCls = state.avatarStatus === 'IR_READY' ? 'ok' : 'fail';
  setB('b-status', `avatar status: <b>${state.avatarStatus}</b> (${state.parseStatus ?? '—'})`, `badge ${stCls}`);
  setB('b-blocks', `blocks: <b>${state.numBlocks ?? '—'}</b> shapes: <b>${state.shapes ?? '—'}</b> opaque: <b>${state.opaqueCount ?? '—'}</b>`);
  const hs = HAIR.map(x => `${x.key}=${state.hairVisible[x.key] ? 'ON' : 'off'}`).join(' ');
  setB('b-hair', `hair: <b>${hs}</b> (side-by-side, NOT attached)`);
}

// ---------- panel ----------
function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
function renderPanel(avatarIR, hairIRs) {
  const e = avatarIR.extraction, rm = avatarIR.renderModel;
  const counts = {};
  for (const b of e.blocks) counts[b.type] = (counts[b.type] || 0) + 1;
  const supported = {};
  const opaque = {};
  for (const [t, n] of Object.entries(counts)) {
    if (e.blocks.find(b => b.type === t && b.opaque)) opaque[t] = n; else supported[t] = n;
  }
  let html = '';

  html += `<h3>AVATAR IDENTITY (STRICT_ISO extracted)</h3><table>
    <tr><td class="k">member id</td><td>208861.nif (Models.ark member; family ${esc(AVATAR.family)})</td></tr>
    <tr><td class="k">size</td><td>${AVATAR.size} B</td></tr>
    <tr><td class="k">sha256</td><td>${AVATAR.sha256} <span class="${state.avatarShaVerified ? '' : 'honest'}">verified=${state.avatarShaVerified ? 'Y' : 'N'}</span></td></tr>
    <tr><td class="k">era</td><td>${esc(AVATAR.era)} — corpus Models.ark SHA F660D055… (VREG pin, re-verified this run)</td></tr>
    <tr><td class="k">chosen vs 208860</td><td>208861 = the VREG REPORT §5 example-evidence member (full Bip01_face_cd_* morph signature + Ponytail1 hair bone, 180 Bip01 strings); 208860 (pair sibling, SHA F140B056…) censused in W18_AVATAR_CENSUS.json. <span class="honest">WHICH member is which gender: UNPROVEN (VREG: 'likely gender pair' — no opcode/registry binding yet).</span></td></tr>
    <tr><td class="k">source</td><td>STRICT_ISO extracted (derived payload — NOT in the git repo; served read-only via server EXACT_ROUTES)</td></tr>
    <tr><td class="k">format</td><td>${e.header.versionString} (${e.header.versionRaw}) — era dispatch → NifModelReader41.parseModel41 (W09 adapter, UNMODIFIED)</td></tr>
    <tr><td class="k">parseStatus</td><td>${e.parseStatus ?? 'PASS'} (${e.blocks.length}/${e.header.numBlocks} blocks parsed; tail ${e.fileTailBytesLen} B — raw, semantics UNVERIFIED)</td></tr>
  </table>`;

  html += `<h3>BLOCK CENSUS (supported: ${Object.values(supported).reduce((a, b) => a + b, 0)} / opaque: ${Object.values(opaque).reduce((a, b) => a + b, 0)})</h3>
  <table>${Object.entries(supported).map(([t, n]) => `<tr><td class="k">${esc(t)}</td><td>${n} ✓ supported</td></tr>`).join('')}
  ${Object.entries(opaque).map(([t, n]) => `<tr><td class="k">${esc(t)}</td><td>${n} <span class="honest">OPAQUE — unsupported in R1 adapter — skeleton/morph semantic pending (known-RTTI-anchored boundary, span recorded)</span></td></tr>`).join('')}</table>
  <div class="note">geometry: ${rm.shapes.length} shapes, ${state.vertices} vertices, ${state.triangles} triangles; roots ${rm.roots.length}; shapes carry NO skinRef on the avatar (rigid per-bone chunks under the Bip01 NiNode hierarchy — the avatar NIF contains NO NiSkinInstance; skin/morph behavior is carried by the OPAQUE NiKeyframeController/NiKeyframeData/NiArk* blocks listed above).</div>`;

  html += `<h3>UNSUPPORTED / OPAQUE (honest list)</h3>
  <div class="refbox">${Object.entries(opaque).map(([t, n]) => `${esc(t)} ×${n}`).join('<br>')}<br><span class="honest">skin/morph → 'unsupported in R1 adapter — skeleton/morph semantic pending'.</span> No boundary was invented: every opaque block is recorded with offset+span via the known-RTTI-anchored method (W09 policy).</div>`;

  html += `<h3>ATTACHMENT SLOTS (635 CharDef mesh sections)</h3><table>
    <tr><td class="k">slots</td><td>${SLOTS_635.join(', ')}</td></tr>
    <tr><td class="k">source</td><td>635.obj (CharDef) inline strings — MESH-SECTION names for CharDef::250323 (set mesh), CHAR_F §4; also VREG §3.1 registry classes (1464 Facemaskplate/head, 2284 Glovesplate/hand, 5493 Helmetplate head+hair, 5500 Boots foot+calf, 3577/3581 torso, 3703 calf, 4288 Shoes…)</td></tr>
    <tr><td class="k">status</td><td><span class="honest">NO runtime attachment proof in R1 — slot names are script-recovered strings; positions/engine binding NOT recovered (engine-side).</span></td></tr>
  </table>`;

  html += `<h3>HAIR CANDIDATES (recovered mapping — VREG/CHAR_F)</h3>`;
  for (const h of HAIR) {
    const ir = hairIRs[h.key];
    const parseOk = !!ir;
    const st = state.hairStatus[h.key] ?? '—';
    html += `<table>
      <tr><td class="k">hair ${h.key}</td><td>mesh ${h.id}.nif (${h.gender}) (${h.size} B, SHA ${h.sha256.slice(0, 16)}… verified=${state.hairShaVerified[h.key] ? 'Y' : 'N'})</td></tr>
      <tr><td class="k">mapping source</td><td>6052.obj Hair::GetMeshId/GetTexture registry — ${esc(h.array)}; item_index 0 pairing per CHAR_G PALETTE_MAPS_HAIR_V7.csv (W25 re-pair: W18 had the two textures crossed between the gender arrays)</td></tr>
      <tr><td class="k">texture</td><td>${h.texId}.tga (${state.hairTexStatus[h.key] ?? '—'}; SHA ${h.texSha256.slice(0, 16)}… verified=${state.hairTexShaVerified[h.key] ? 'Y' : 'N'})</td></tr>
      <tr><td class="k">parse</td><td>${parseOk ? `${ir.extraction.parseStatus} — ${ir.renderModel.shapes.length} shape, ${ir.renderModel.shapes[0].numVertices} verts, UV sets: ${ir.renderModel.shapes[0].uvSets.length}; stopped at NiSkinInstance/NiSkinData (skin semantic pending)` : st}</td></tr>
      <tr><td class="k">gender note</td><td>gender-array binding BYTE-PROVEN (CHAR_G, 2026-10-31): GetSex slot 45 via 635 -> 1 = MALE (classtypes {926,4195}), 2 = FEMALE ({1014,4063}); 6052 GetMeshId [this+0]==1 -> mesh@96 (MALE), ==2 -> mesh@248 (FEMALE); GetTexture ==2 -> tex@636 (FEMALE), ==1 -> tex@800 (MALE). mesh 32498 = MALE + tex 216257; mesh 32509 = FEMALE + tex 216302 (V7).</td></tr>
      <tr><td class="k">texture state</td><td>${state.hairTexStatus[h.key] === 'APPLIED (TGA decoded, UV parsed)' ? 'APPLIED — era TGA 24bpp BGR 64×128, TGA 2.0 footer, STRICT TgaDecoder (W05 pattern); raw-v convention' : esc(st)}</td></tr>
    </table>`;
  }
  html += `<div class="note">hair meshes render SEPARATELY (side-by-side + toggle) — <span class="honest">NOT attached to the avatar: no proof of the head-attachment position in R1</span> (the avatar's own Ponytail bone transforms are shown in the avatar render only as the IR places them).</div>`;

  html += `<h3>RECOVERED CONTROLS (21 — strings ONLY, NO working sliders)</h3>
  <div class="warnbox">No morph-target runtime proof exists yet (R1): these are RECOVERED LABELS + RANGE STATUSES, not functional controls. No fictional sliders are drawn.</div>`;
  html += `<table>${CONTROLS_21.map(c => `<tr><td class="k">${esc(c.label)}</td><td><span class="ctrl"><span class="${c.status.startsWith('RANGE') ? 'st' : 'eng'}">${c.status}</span> — ${esc(c.note)}</span></td></tr>`).join('')}</table>`;

  html += `<h3>SOURCE LABELS</h3><table>
    <tr><td class="k">payloads</td><td>STRICT_ISO extracted — Models.ark/Textures.ark members of the SHA-pinned 2003 corpus (derived copies; NOT committed to the repo; read-only server routes)</td></tr>
    <tr><td class="k">presentation</td><td>REFERENCE stage — diagnostic axes/grid; cm→m ×0.01, Z-up→Y-up (x,z,-y) CURRENT_RUNTIME_CALIBRATION (W09 convention); NOT world instance positions; NOT the original PE environment</td></tr>
  </table>`;

  html += `<h3>HAIR TOGGLE</h3><div>
    <button id="btn-hair-A">hair A (mesh 32498, MALE): VISIBLE</button>
    <button id="btn-hair-B">hair B (mesh 32509, FEMALE): VISIBLE</button>
  </div><div class="note">toggle = visibility of the side-by-side hair groups (state published in __W18_STATE__.hairVisible). Gender labels per CHAR_G PALETTE_MAPS_HAIR_V7 (W25).</div>`;

  // W27 ADDITIVE SECTION (head appearance candidates) — appended at the end,
  // no existing section modified.
  html += renderHeadSectionHtml();

  panel.innerHTML = html;
  el('btn-hair-A').onclick = () => toggleHair('A');
  el('btn-hair-B').onclick = () => toggleHair('B');
  const btnHead = el('btn-head-appearance');
  if (btnHead) btnHead.onclick = () => toggleHeadAppearances();
  drawHeadCanvases();
}

// ---------- main ----------
(async function main() {
  initViewport();
  state.revision = THREE.REVISION;
  try {
    // ---- avatar ----
    const avBuf = await fetchBuf(AVATAR.url);
    state.avatarShaVerified = (await sha256hex(avBuf)) === AVATAR.sha256;
    if (!state.avatarShaVerified) throw new Error(`avatar SHA256 mismatch: expected ${AVATAR.sha256}`);
    let avatarIR;
    try {
      avatarIR = parseAvatarEra(avBuf, '208861.nif');
      state.avatarStatus = 'IR_READY';
    } catch (e) {
      state.avatarStatus = 'ERA_GATE_LOUD_FAIL';
      throw e;
    }
    const e = avatarIR.extraction, rm = avatarIR.renderModel;
    state.formatVersion = e.header.versionString;
    state.numBlocks = e.blocks.length;
    state.parseStatus = e.parseStatus ?? 'PASS';
    const counts = {};
    for (const b of e.blocks) counts[b.type] = (counts[b.type] || 0) + 1;
    state.typeCounts = counts;
    state.opaqueTypes = {};
    for (const b of e.blocks) if (b.opaque) state.opaqueTypes[b.type] = (state.opaqueTypes[b.type] || 0) + 1;
    state.opaqueCount = e.opaqueBlocks.length;
    state.shapes = rm.shapes.length;
    state.vertices = rm.shapes.reduce((a, s) => a + s.numVertices, 0);
    state.triangles = rm.shapes.reduce((a, s) => a + s.numTriangles, 0);

    addShapes(rm, { groupName: 'avatar:208861', flatColor: 0x9aa3b0 });
    const avBounds = boundsOf(rm);

    // ---- hair (side-by-side; NOT attached) ----
    const hairIRs = {};
    for (const h of HAIR) {
      try {
        const buf = await fetchBuf(h.url);
        state.hairShaVerified[h.key] = (await sha256hex(buf)) === h.sha256;
        if (!state.hairShaVerified[h.key]) throw new Error(`hair ${h.id} SHA mismatch`);
        const ir = parseModel41(buf, `${h.id}.nif`);
        hairIRs[h.key] = ir;
        state.hairStatus[h.key] = ir.extraction.parseStatus;
        // era texture (decoded STRICTLY; applied only if UV parsed)
        let texture = null;
        try {
          const tbuf = await fetchBuf(h.texUrl);
          state.hairTexShaVerified[h.key] = (await sha256hex(tbuf)) === h.texSha256;
          const decoded = decodeTga2(tbuf);
          texture = new THREE.DataTexture(decoded.rgba, decoded.width, decoded.height, THREE.RGBAFormat);
          texture.needsUpdate = true;
          const hasUV = !!(ir.renderModel.shapes[0] && ir.renderModel.shapes[0].uvSets.length);
          state.hairTexStatus[h.key] = hasUV
            ? 'APPLIED (TGA decoded, UV parsed)'
            : 'untextured (UV pending)';
        } catch (te) {
          state.hairTexStatus[h.key] = `untextured (texture decode out of adapter scope: ${String(te.message ?? te).slice(0, 60)})`;
          state.errors.push({ kind: 'texture', hair: h.key, text: String(te.message ?? te) });
        }
        const sideX = h.key === 'A' ? -1 : 1;
        const g = addShapes(ir.renderModel, {
          groupName: `hair${h.key}:${h.id}`, texture, flatColor: 0x9aa3b0,
        });
        const hb = boundsOf(ir.renderModel);
        // side-by-side placement: to the left/right of the avatar, grounded on
        // the stage grid — an EXPLICIT non-attachment offset (not a head bind)
        g.position.set(
          avBounds.center[0] + sideX * (avBounds.radius + hb.radius + 0.6),
          0 - hb.center[1], // ground the hair base near y=0 (reference placement)
          avBounds.center[2],
        );
        g.userData.referenceOffset = g.position.toArray();
        hairGroups[h.key] = g;
      } catch (e2) {
        state.hairStatus[h.key] = `LOAD_FAIL: ${String(e2.message ?? e2)}`;
        state.errors.push({ kind: 'hair', hair: h.key, text: String(e2.message ?? e2) });
      }
    }

    frameOn(avBounds.center, avBounds.radius + 1.2);

    // ---- W27 head appearance candidates (ADDITIVE — fetch + verify + decode) ----
    for (const h of HEAD_APPEARANCE) {
      try {
        const buf = await fetchBuf(`/assets/head/${h.id}.tga`);
        const ok = (await sha256hex(buf)) === h.sha256;
        state.headTexShaVerified[h.id] = ok;
        window.__W27_STATE__.headTexShaVerified[h.id] = ok;
        if (!ok) throw new Error(`head tga ${h.id} SHA mismatch (expected ${h.sha256})`);
        const decoded = decodeTga2(buf); // STRICT decoder: 24bpp BGR + TGA2 footer, loud fail otherwise
        headDecoded[h.id] = decoded;
        state.headStatus[h.id] = `DECODED (128×128 24bpp BGR, TGA2 footer, ${buf.length} B)`;
        state.headDecodedCount++;
        window.__W27_STATE__.headDecodedCount = state.headDecodedCount;
      } catch (e3) {
        state.headStatus[h.id] = `FAIL: ${String(e3.message ?? e3).slice(0, 100)}`;
        window.__W27_STATE__.errors.push({ id: h.id, text: String(e3.message ?? e3) });
        state.errors.push({ kind: 'head-tga', id: h.id, text: String(e3.message ?? e3) });
      }
    }
    state.headStatusLine = state.headDecodedCount === HEAD_APPEARANCE.length
      ? `ALL ${HEAD_APPEARANCE.length}/20 decoded + SHA-verified (STRICT decodeTga2)`
      : `PARTIAL: ${state.headDecodedCount}/${HEAD_APPEARANCE.length} decoded — see per-id rows`;
    window.__W27_STATE__.headStatus = state.headStatusLine;

    renderPanel(avatarIR, hairIRs);
    state.status = 'READY';
  } catch (e) {
    state.status = 'ERROR';
    state.errors.push({ kind: 'fatal', text: String(e.message ?? e) });
    panel.innerHTML = `<div class="refbox">FATAL: ${esc(String(e.message ?? e))}</div>`;
    el('viewmsg').textContent = `NO RENDER — ${String(e.message ?? e).slice(0, 120)}`;
  }
  updateBadges();
  state.done = true;
  state.doneAt = new Date().toISOString();
})();
