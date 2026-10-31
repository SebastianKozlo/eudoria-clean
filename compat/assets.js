// assets.js — AV-2 (PE_ISO_ASSET_VIEWER campaign, job AV2_VIEWER, 2026-10-31).
//
// PAGE VIEWER for ALL Models.ark members (era ISO_5_1_0_0 / NIF 4.1.0.12):
//   - index (2492 entries) via /api/assets/index, search + pagination
//   - render of the selected model from the server-side parseModel41 typed IR
//     (W09 adapter UNMODIFIED, server-side — one Rosetta path
//     source→decoder(versioned)→typedIR→consumer)
//   - textures: server-side textureJoins (structural NiSourceTexture name →
//     Textures.ark member), client fetches each joined id via
//     /api/assets/texture and decodes STRICTLY (TgaDecoder 24bpp BGR /
//     DdsDecoder DXT1/DXT5). Missing/unresolvable texture = EXPLICIT
//     'untextured' status — NO fallback, NO invented textures.
//   - animations: the ONLY controller types the 4.1 adapter implements are
//     NiUVController/NiUVData — those become THREE.AnimationClips
//     (KeyframeTrack on a proxy object; mixer drives texture.offset each
//     frame; interpolation from the data — LINEAR/CONST-as-LINEAR, NO
//     resampling, quaternion order N/A for UV float keys).
//     NiKeyframeController/NiKeyframeData/skin are OPAQUE in the R1 adapter —
//     shown VERBATIM in the census (honest UNSUPPORTED, never hidden).
//   - AV-3 additive (job AV3_ANIMATION, 2026-10-31): skeletal/rigid-part
//     keyframe animation. The server decodes NiKeyframeController/
//     NiKeyframeData/NiTextKeyExtraData closure-exact (tools/av3/kf41.mjs)
//     and ships keyframeAnim + nodeHierarchy. The client builds a rigid
//     NiNode Object3D tree (AK-3 semantics: rigid parts animated
//     hierarchically — NO skinning here, skinning is a separate job), wraps
//     it in the era axis/unit converter (raw NIF Z-up cm inside the wrapper:
//     x,z,-y @ 0.01 — same [P-AXIS]/[P-UNITS] calibration, applied ONCE at
//     the wrapper instead of per-mesh), and drives it with
//     AnimationMixer + Quaternion/Vector keyframe tracks. Quaternion order
//     comes from the data (w,x,y,z storage — physically verified against
//     bind matrices 48/48 on 206264; Three consumes x,y,z,w so the values
//     are re-ordered, NO resampling, NO inversion). LOOP policy = viewer
//     ENGINEERING choice (labeled, not a measured NIF semantic).
//   - era label ISO_5_1_0_0 visible in the badge bar (G5).
//
// [P-UNITS]/[P-AXIS] CURRENT_RUNTIME_CALIBRATION (character_preview.js
// parity): NIF cm -> m ×0.01; NIF Z-up -> Three Y-up (x, z, -y).
'use strict';
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { decodeTga2 } from '../src/pesource/TgaDecoder.js';
import { decodeDds } from '../src/pesource/DdsDecoder.js';

const ERA = 'ISO_5_1_0_0';
const PAGE = 120;
const state = {
  job: 'AV2_VIEWER', era: ERA, status: 'LOADING', errors: [],
  indexCount: null, entries: [], filtered: [], page: 0,
  currentId: null, modelStatus: null, parseStatus: null, numBlocks: null,
  opaqueCount: null, shapesCount: null, vertices: 0, triangles: 0,
  texBound: 0, texMissing: 0, texTotal: 0, texPerJoin: [],
  anim: { hasControllers: false, clips: 0, activeTracks: 0, playing: false, time: 0, duration: 0,
          kf: null },
  kfUnsupportedCount: 0,
  doneIndex: false,
};
window.__AV_STATE__ = state;
window.__AV_ERRORS__ = state.errors;

const el = (id) => document.getElementById(id);
const panel = el('panel');

function logErr(kind, text) { state.errors.push({ kind, text: String(text).slice(0, 300) }); }

// ---------- 3D viewport (REFERENCE ASSET STAGE) ----------
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
  scene.add(new THREE.AxesHelper(1.0));
  scene.add(new THREE.GridHelper(4, 8, 0x334155, 0x1e293b));
  window.addEventListener('resize', () => {
    const W = el('viewwrap').clientWidth || 640, H = el('viewwrap').clientHeight || 480;
    camera.aspect = W / H; camera.updateProjectionMatrix(); renderer.setSize(W, H);
  });
}

// ---------- animation (NiUVController/NiUVData → AnimationClip) ----------
const animCtx = { mixer: null, clips: [], proxy: null, activeTexture: null, action: null };
function buildAnimation(model, textureByShape) {
  const ctrl = model.controllers.filter(c => c.type === 'NiUVController');
  if (!ctrl.length) { state.anim.hasControllers = false; return; }
  state.anim.hasControllers = true;
  // find data blocks
  const byIdx = new Map(model.controllers.map(c => [c.blockIndex, c]));
  const clips = [];
  for (const c of ctrl) {
    const data = byIdx.get(c.dataRef);
    if (!data || data.type !== 'NiUVData') continue;
    // groups: 0=U offset, 1=V offset (NiUVData 4 groups; U/V used honestly)
    const gU = data.uvGroups[0], gV = data.uvGroups[1];
    if (!gU || gU.numKeys === 0) continue;
    const times = gU.keys.map(k => k.time);
    const values = [];
    for (let i = 0; i < gU.keys.length; i++) {
      const v = gV && gV.keys[Math.min(i, gV.keys.length - 1)] ? gV.keys[Math.min(i, gV.keys.length - 1)].value : 0;
      values.push(gU.keys[i].value, v);
    }
    const clip = new THREE.AnimationClip(`uvanim_blk${c.blockIndex}`, times[times.length - 1], [
      new THREE.VectorKeyframeTrack('.uvOffset', times, values),
    ]);
    clip.userData = { interpolation: gU.interpolation, freq: c.frequency };
    clips.push(clip);
  }
  animCtx.clips = clips;
  animCtx.proxy = new THREE.Object3D();
  animCtx.proxy.name = 'uvProxy';
  animCtx.proxy.uvOffset = new THREE.Vector2(0, 0);
  animCtx.mixer = new THREE.AnimationMixer(animCtx.proxy);
  state.anim.clips = clips.length;
  const sel = el('clip-sel');
  sel.innerHTML = '<option value="-1">— no clip —</option>' +
    clips.map((c, i) => `<option value="${i}">${c.name} (${c.duration.toFixed(2)}s, interp=${c.userData.interpolation})</option>`).join('');
}
function playClip(i) {
  if (animCtx.mixer) animCtx.mixer.stopAllAction();
  if (kfCtx.mixer) kfCtx.mixer.stopAllAction();
  state.anim.activeTracks = 0;
  if (i < 0 || !animCtx.clips[i]) { state.anim.playing = false; updateAnimBadge(); return; }
  const clip = animCtx.clips[i];
  const mixer = clip.userData && clip.userData.kind === 'kf' ? kfCtx.mixer : animCtx.mixer;
  animCtx.action = mixer.clipAction(clip);
  animCtx.action.play();
  state.anim.activeTracks = clip.tracks.length;
  state.anim.duration = clip.duration;
  state.anim.playing = true;
  updateAnimBadge();
}
window.__AV_PLAY__ = playClip; // gate hook
window.__AV_SEEK__ = (frac) => { // gate hook: seek to fraction of clip duration
  if (animCtx.action && state.anim.duration > 0) {
    animCtx.action.time = Math.max(0, Math.min(0.999, frac)) * state.anim.duration;
    state.anim.time = animCtx.action.time;
    if (animCtx.mixer) animCtx.mixer.update(0);
    el('time').textContent = `${state.anim.time.toFixed(2)}s`;
    return state.anim.time;
  }
  return -1;
};
function updateAnimBadge() {
  const a = state.anim;
  const b = el('b-anim');
  const kfTxt = a.kf ? ` + KF: ${a.kf.clips} clip(s)/${a.kf.tracks} track(s)` : '';
  b.innerHTML = `anim: <b>${a.hasControllers ? `${a.clips} clip(s), ${a.activeTracks} active track(s)` : 'no UV controller'}</b>${kfTxt} ${a.playing ? '▶' : ''}`;
  b.className = 'badge ' + (a.activeTracks > 0 ? 'ok' : '');
}

// ---------- AV-3: keyframe (skeletal/rigid-hierarchy) animation ----------
// kfCtx.root = era converter wrapper (Rx(-90°)·0.01) containing the raw-NIF
// Object3D tree; kfCtx.mixer drives it. AV-5: when a model has a decoded
// NiSkin binding (shapes[].skin.ok), the hierarchy nodes are THREE.Bone and
// skinned shapes become THREE.SkinnedMesh (boneInverses = NiSkinData
// SkinToBone = inverse bind; bind law p = SUM w_i*(W_i*STB_i)*v, physically
// verified server-side — tools/av5/skin_verify.mjs).
const kfCtx = { root: null, mixer: null, nodes: new Map(), clips: [], model: null };
function kfNodeLocalTRS(o, trs) {
  // raw NIF local TRS → Object3D props (rotation matrix rows are the stored
  // convention; composeTRS parity — same standard math as the reader's
  // engine-validated world compose)
  o.position.fromArray(trs.translation);
  const R = trs.rotation;
  const m = new THREE.Matrix4().set(
    R[0][0], R[0][1], R[0][2], 0,
    R[1][0], R[1][1], R[1][2], 0,
    R[2][0], R[2][1], R[2][2], 0,
    0, 0, 0, 1);
  o.quaternion.setFromRotationMatrix(m);
  o.scale.setScalar(trs.scale);
}
function buildKfModel(model, textureByShape) {
  const byIndex = new Map(model.nodeHierarchy.map(n => [n.index, n]));
  const shapeByNode = new Map(model.shapes.map(s => [s.shapeIndex, s]));
  const hasSkin = model.shapes.some(s => s.skin && s.skin.ok);
  const wrapper = new THREE.Group();
  wrapper.name = `kfw:${state.currentId}`;
  wrapper.matrixAutoUpdate = false;
  const wm = new THREE.Matrix4().makeRotationX(-Math.PI / 2); // Z-up → Y-up (x, z, -y)
  wm.scale(new THREE.Vector3(UNIT, UNIT, UNIT));             // cm → m (ONCE, wrapper-level)
  wrapper.matrix.copy(wm);
  const objs = new Map();
  for (const n of model.nodeHierarchy) {
    // THREE.Bone when any shape is skinned (AV-5) — same Object3D semantics,
    // Skeleton-compatible; plain Object3D otherwise (AV-3 rigid path).
    const o = hasSkin ? new THREE.Bone() : new THREE.Object3D();
    o.name = `n${n.index}`;
    kfNodeLocalTRS(o, n.localTRS);
    objs.set(n.index, o);
  }
  for (const n of model.nodeHierarchy) {
    const o = objs.get(n.index);
    const p = n.parent != null && objs.has(n.parent) ? objs.get(n.parent) : wrapper;
    p.add(o);
  }
  // shape meshes attach under their NiTriShape node (identity local mesh)
  state.skinInfo = { shapes: 0, skinned: 0, vertsOver4: 0, weightSumMismatch: 0, maxInfl: 0, bindBBox: null };
  for (const sh of model.shapes) {
    const n = byIndex.get(sh.shapeIndex);
    const isSkinned = !!(sh.skin && sh.skin.ok);
    // Skinned meshes attach at the WRAPPER (identity local): skinned
    // geometry lives in skin space and the skeleton bone world matrices
    // already carry it to world — the shape node TRS must NOT apply.
    const host = isSkinned ? wrapper : (n && objs.get(sh.shapeIndex) ? objs.get(sh.shapeIndex) : wrapper);
    const n0 = sh.numVertices;
    const positions = new Float32Array(n0 * 3);
    for (let i = 0; i < n0; i++) { // raw NIF coords — the wrapper converts
      positions[i * 3] = sh.positions[i * 3];
      positions[i * 3 + 1] = sh.positions[i * 3 + 1];
      positions[i * 3 + 2] = sh.positions[i * 3 + 2];
    }
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    if (sh.normals) geometry.setAttribute('normal', new THREE.BufferAttribute(new Float32Array(sh.normals), 3));
    const hasUV = !!(sh.uvSets && sh.uvSets[0] && sh.uvSets[0].length);
    if (hasUV) geometry.setAttribute('uv', new THREE.BufferAttribute(new Float32Array(sh.uvSets[0]), 2));
    if (sh.colors) geometry.setAttribute('color', new THREE.BufferAttribute(new Float32Array(sh.colors), 4));
    geometry.setIndex(new THREE.BufferAttribute(new Uint16Array(sh.index), 1));
    const alphaThreshold = sh.alphaProp ? sh.alphaProp.threshold : 0;
    const alphaBlendOn = sh.alphaProp ? (sh.alphaProp.flags & 1) === 1 : false;
    const material = new THREE.MeshBasicMaterial({
      vertexColors: !!sh.colors, transparent: alphaBlendOn,
      alphaTest: alphaThreshold / 255.0, side: THREE.DoubleSide,
    });
    const tex = textureByShape.get(sh.shapeIndex);
    if (tex && hasUV) { material.map = tex; material.needsUpdate = true; }
    else if (sh.material) material.color.setRGB(sh.material.diffuse[0], sh.material.diffuse[1], sh.material.diffuse[2]);
    else material.color.set(0x9aa3b0);
    let mesh;
    if (sh.skin && sh.skin.ok) {
      // ---- AV-5 THREE.SkinnedMesh ----
      // Source data has NO 4-influence limit (corpus maxInfl up to 9,
      // measured). THREE skinIndex/skinWeight attributes are vec4: the
      // ENGINEERING policy here keeps the TOP-4 influences per vertex,
      // renormalizes the kept weights, and reports the FULL per-model
      // influence stats (vertsOver4 + dropped mass) honestly — the raw
      // per-vertex influence data stays in the model payload, untruncated.
      const infl = sh.skin.influences;
      const skinIndex = new Uint16Array(n0 * 4);
      const skinWeight = new Float32Array(n0 * 4);
      let vertsOver4 = 0, droppedMass = 0, maxInfl = 0;
      for (let v = 0; v < n0; v++) {
        const list = (infl[v] || []).slice().sort((a, b) => b[1] - a[1]);
        maxInfl = Math.max(maxInfl, list.length);
        if (list.length > 4) { vertsOver4++; for (let k = 4; k < list.length; k++) droppedMass += list[k][1]; }
        const keep = list.slice(0, 4);
        const sum = keep.reduce((a, x) => a + x[1], 0) || 1;
        for (let k = 0; k < 4; k++) {
          skinIndex[v * 4 + k] = k < keep.length ? keep[k][0] : 0;
          skinWeight[v * 4 + k] = k < keep.length ? keep[k][1] / sum : 0;
        }
      }
      geometry.setAttribute('skinIndex', new THREE.BufferAttribute(skinIndex, 4));
      geometry.setAttribute('skinWeight', new THREE.BufferAttribute(skinWeight, 4));
      // bones from the live NiNode hierarchy (NiSkinInstance bone refs)
      const bones = sh.skin.bones.map(ref => {
        const b = objs.get(ref);
        if (!b) throw new Error(`skin bone ref ${ref} not in nodeHierarchy — cannot skin (honest fail)`);
        return b;
      });
      // boneInverses = NiSkinData SkinToBone (inverse bind; NiTransform
      // rotation/scale/translation → column-major Matrix4)
      const boneInverses = sh.skin.skinToBone.map(t => new THREE.Matrix4().set(
        t.rotation[0][0], t.rotation[0][1], t.rotation[0][2], t.translation[0],
        t.rotation[1][0], t.rotation[1][1], t.rotation[1][2], t.translation[1],
        t.rotation[2][0], t.rotation[2][1], t.rotation[2][2], t.translation[2],
        0, 0, 0, 1).scale(new THREE.Vector3(t.scale, t.scale, t.scale)));
      const skeleton = new THREE.Skeleton(bones, boneInverses);
      mesh = new THREE.SkinnedMesh(geometry, material);
      mesh.name = `sk${state.currentId}:${sh.shapeName ?? sh.shapeIndex}`;
      // bindMatrix = identity: the shader computes world = meshWorld *
      // (SUM w_i * (W_bone_i * boneInverse_i)) * v — with boneInverse_i =
      // SkinToBone_i this is EXACTLY the NIF bind law (skin space -> world).
      mesh.bind(skeleton, new THREE.Matrix4());
      state.skinInfo.skinned++;
      state.skinInfo.vertsOver4 += vertsOver4;
      state.skinInfo.maxInfl = Math.max(state.skinInfo.maxInfl, maxInfl);
      state.skinInfo.weightSumMismatch += sh.skin.stats.weightSumMismatch;
      if (droppedMass > 0) state.skinInfo.droppedMass = (state.skinInfo.droppedMass ?? 0) + droppedMass;
    } else {
      mesh = new THREE.Mesh(geometry, material);
      mesh.name = `k${state.currentId}:${sh.shapeName ?? sh.shapeIndex}`;
    }
    host.add(mesh);
  }
  state.skinInfo.shapes = model.shapes.length;
  kfCtx.root = wrapper;
  kfCtx.nodes = objs;
  kfCtx.model = model;
  scene.add(wrapper);
  kfCtx.mixer = new THREE.AnimationMixer(wrapper);
  return wrapper;
}
/** (documented no-op — bones live in the wrapper tree, not under the mesh) */
function rootBoneFor(skeleton, bones, wrapper) { return null; }
function buildKfClips(model) {
  const ka = model.keyframeAnim;
  if (!ka || !ka.controllers || !ka.controllers.length) return [];
  const dataByIndex = new Map(ka.data.map(d => [d.blockIndex, d]));
  const tracks = [];
  let skipped = 0, maxT = 0, minT = Infinity;
  for (const c of ka.controllers) {
    const node = kfCtx.nodes.get(c.target);
    if (!node) { skipped++; continue; }
    const d = dataByIndex.get(c.dataRef);
    if (!d) { skipped++; continue; }
    if (d.rotationKeys && d.rotationKeys.keys && d.rotationKeys.keys.length) {
      const keys = d.rotationKeys.keys;
      const times = keys.map(k => k.time);
      const values = []; // NIF stores (w,x,y,z); Three consumes (x,y,z,w) — reorder only
      for (const k of keys) values.push(k.x, k.y, k.z, k.w);
      tracks.push(new THREE.QuaternionKeyframeTrack(`n${c.target}.quaternion`, times, values));
    }
    if (d.translations && d.translations.keys && d.translations.keys.length) {
      const keys = d.translations.keys;
      const times = keys.map(k => k.time);
      const values = [];
      for (const k of keys) values.push(k.value[0], k.value[1], k.value[2]);
      tracks.push(new THREE.VectorKeyframeTrack(`n${c.target}.position`, times, values));
    }
    if (d.scales && d.scales.keys && d.scales.keys.length) {
      const keys = d.scales.keys;
      const times = keys.map(k => k.time);
      const values = [];
      for (const k of keys) values.push(k.value, k.value, k.value);
      tracks.push(new THREE.VectorKeyframeTrack(`n${c.target}.scale`, times, values));
    }
    for (const grp of [d.rotationKeys?.keys, d.translations?.keys, d.scales?.keys]) {
      if (grp && grp.length) {
        if (grp[0].time < minT) minT = grp[0].time;
        if (grp[grp.length - 1].time > maxT) maxT = grp[grp.length - 1].time;
      }
    }
  }
  if (!tracks.length) return [];
  // clip name from NiTextKeyExtraData when present, else the honest
  // KINEMATIC/EMBEDDED label (no invented names)
  const tk = (ka.textKeys || []).flatMap(t => t.keys.map(k => k.text)).filter(Boolean);
  const name = tk.length ? `kf_${tk.join('/')}` : `kf_EMBEDDED_KINEMATIC_${state.currentId}`;
  const clip = new THREE.AnimationClip(name, maxT, tracks);
  clip.userData = { kind: 'kf', textKeys: tk, timeRange: [minT === Infinity ? 0 : minT, maxT],
    loopPolicy: 'ENGINEERING_LABEL', skippedControllers: skipped };
  return [clip];
}

// ---------- model build (character_preview addShapes parity) ----------
let modelGroup = null, textureObjs = [];
const UNIT = 0.01;
function clearModel() {
  if (modelGroup) { scene.remove(modelGroup); modelGroup = null; }
  if (kfCtx.root) { scene.remove(kfCtx.root); }
  kfCtx.root = null; kfCtx.mixer = null; kfCtx.nodes = new Map(); kfCtx.clips = []; kfCtx.model = null;
  textureObjs.forEach(t => t.dispose()); textureObjs = [];
  if (animCtx.mixer) { animCtx.mixer.stopAllAction(); }
  animCtx.mixer = null; animCtx.clips = []; state.anim.activeTracks = 0; state.anim.playing = false;
  state.anim.kf = null;
  el('clip-sel').innerHTML = '<option value="-1">— no clip —</option>';
}
function addShapes(model, textureByShape) {
  const group = new THREE.Group();
  group.name = `model:${state.currentId}`;
  for (const sh of model.shapes) {
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
    geometry.setIndex(new THREE.BufferAttribute(new Uint16Array(sh.index), 1));
    const alphaThreshold = sh.alphaProp ? sh.alphaProp.threshold : 0;
    const alphaBlendOn = sh.alphaProp ? (sh.alphaProp.flags & 1) === 1 : false;
    const material = new THREE.MeshBasicMaterial({
      vertexColors: !!sh.colors, transparent: alphaBlendOn,
      alphaTest: alphaThreshold / 255.0, side: THREE.DoubleSide,
    });
    const tex = textureByShape.get(sh.shapeIndex);
    if (tex && hasUV) {
      material.map = tex; material.needsUpdate = true;
      tex.userData.shapeIndex = sh.shapeIndex;
    } else if (sh.material) {
      material.color.setRGB(sh.material.diffuse[0], sh.material.diffuse[1], sh.material.diffuse[2]);
    } else {
      material.color.set(0x9aa3b0);
    }
    const mesh = new THREE.Mesh(geometry, material);
    mesh.name = `m${state.currentId}:${sh.shapeName ?? sh.shapeIndex}`;
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
function frameOn(model) {
  const centers = model.shapes.map(sh => [sh.center[0] * UNIT, sh.center[2] * UNIT, -sh.center[1] * UNIT]);
  let cx = 0, cy = 0, cz = 0;
  for (const c of centers) { cx += c[0]; cy += c[1]; cz += c[2]; }
  if (centers.length) { cx /= centers.length; cy /= centers.length; cz /= centers.length; }
  let maxR = 0;
  for (let i = 0; i < model.shapes.length; i++) {
    const d = Math.hypot(centers[i][0] - cx, centers[i][1] - cy, centers[i][2] - cz) + model.shapes[i].radius * UNIT;
    if (d > maxR) maxR = d;
  }
  const radius = Math.max(maxR, 0.1);
  const camDist = Math.max(radius * 2.6, 0.5);
  camera.position.set(cx + camDist * 0.55, cy + camDist * 0.42, cz + camDist * 0.72);
  camera.near = Math.max(camDist / 1000, 0.001); camera.far = camDist * 50;
  camera.updateProjectionMatrix();
  controls.target.set(cx, cy, cz);
  el('viewmsg').textContent = '';
}

// ---------- texture decode (STRICT, no fallbacks) ----------
async function fetchTexture(id) {
  const r = await fetch(`/api/assets/texture?id=${id}`);
  if (!r.ok) throw new Error(`texture ${id}: HTTP ${r.status}`);
  return new Uint8Array(await r.arrayBuffer());
}
function decodeTexture(payload, name) {
  if (payload[0] === 0x44 && payload[1] === 0x44 && payload[2] === 0x53 && payload[3] === 0x20) {
    const d = decodeDds(payload); // STRICT DXT1/DXT5, loud fail otherwise
    return { rgba: d.rgba, width: d.width, height: d.height, format: `DDS ${d.fourcc}` };
  }
  const d = decodeTga2(payload); // STRICT TGA2 24bpp BGR, loud fail otherwise
  return { rgba: d.rgba, width: d.width, height: d.height, format: 'TGA2 24bpp' };
}
function makeTexture(dec) {
  const t = new THREE.DataTexture(new Uint8ClampedArray(dec.rgba), dec.width, dec.height, THREE.RGBAFormat);
  t.needsUpdate = true;
  t.flipY = false; // raw-v convention (character_preview parity)
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

// ---------- panel ----------
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
function renderPanel(model) {
  let html = `<h3>MODEL ${esc(model.name)} (id ${state.currentId}) — era ${ERA}</h3><table>
    <tr><td class="k">size</td><td>${model.size} B</td></tr>
    <tr><td class="k">sha256 (entry)</td><td style="word-break:break-all;">${model.sha256}</td></tr>
    <tr><td class="k">format</td><td>${esc(model.header.versionString)} (${esc(model.header.versionRaw)}) — server-side ${esc(model.adapter ?? 'NifModelReader41')} (version-dispatched)</td></tr>
    <tr><td class="k">parseStatus</td><td>${esc(model.parseStatus)} — blocks ${model.blockCensus ? Object.values(model.blockCensus).reduce((a, c) => a + c.count, 0) : '—'} parsed, tail ${model.tailBytes} B</td></tr>
    <tr><td class="k">shapes</td><td>${model.shapes.length} (${state.vertices} verts, ${state.triangles} tris)</td></tr>
    <tr><td class="k">textures</td><td>joins: ${state.texTotal}, bound: <span class="st">${state.texBound}</span>, missing/untextured: <span class="honest">${state.texMissing}</span></td></tr>
    <tr><td class="k">anim</td><td>${state.anim.hasControllers ? `NiUVController clips: ${state.anim.clips} (active tracks ${state.anim.activeTracks})` : 'no UV controller in this model'}</td></tr>
  </table>`;

  html += `<h3>BLOCK CENSUS (supported / OPAQUE-UNSUPPORTED)</h3><table>`;
  for (const [t, c] of Object.entries(model.blockCensus)) {
    html += `<tr><td class="k">${esc(t)}</td><td>${c.count} ${c.opaque ? `<span class="honest">(${c.opaque} OPAQUE — unsupported in R1 adapter, boundary anchored, NO invented structure)</span>` : '✓'}</td></tr>`;
  }
  html += `</table>`;
  const kf = model.blockCensus['NiKeyframeController'] || model.blockCensus['NiKeyframeData'];
  if (kf) {
    if (state.anim.kf) {
      const k = state.anim.kf;
      html += `<div class="note">AV-3 KF: ${k.controllers} controller(s) → ${k.clips} clip(s), ${k.tracks} bone/hierarchy track(s); textKeys: ${k.textKeys.length ? esc(k.textKeys.join(', ')) : 'none (KINEMATIC/EMBEDDED label)'}; closure: ${k.closureAll ? '<span class="st">EXACT</span>' : `<span class="honest">FAIL (${k.failures})</span>`}; LOOP policy: ${esc(k.loopPolicy)} (viewer ENGINEERING choice, not a measured NIF semantic); no skinning (AK-3 rigid-part semantics).</div>`;
    } else {
      html += `<div class="warnbox">HONEST GAP: NiKeyframeController/NiKeyframeData are OPAQUE in the NifModelReader41 R1 adapter — skeletal animation is <b>UNSUPPORTED</b> in this viewer. Only NiUVController/NiUVData (UV-scroll animation) is implemented. Nothing is faked.</div>`;
    }
  }
  if (model.parseStatus !== 'PASS') {
    html += `<div class="warnbox">parse stopped at block #${model.stoppedAtBlock} (${esc(model.parseStatus)}) — the geometry rendered IS the parsed IR up to that point; the stop is displayed, never hidden.</div>`;
  }

  html += `<h3>TEXTURE JOINS (per shape)</h3><table>`;
  for (const tj of model.textureJoins) {
    if (!tj.joins.length) continue;
    for (const j of tj.joins) {
      const st = j.status === 'BOUND' ? '<span class="st">BOUND</span>'
        : `<span class="honest">${esc(j.status)}</span>`;
      html += `<tr><td class="k">${esc(tj.shapeName ?? tj.shapeIndex)} slot ${j.slot}</td><td>${esc(j.arkRecordName ?? j.sourceType ?? '?')} → ${j.arkEntry ? `${esc(j.arkEntry.name)} (${j.arkEntry.size} B)` : '—'} : ${st}${j.decInfo ? ` <span class="st">[${esc(j.decInfo)}]</span>` : ''}${j.reason ? ` <span class="honest">(${esc(j.reason)})</span>` : ''}</td></tr>`;
    }
  }
  html += `</table><div class="note">NO fallback textures: a missing/unresolvable join renders the shape untextured (material diffuse color instead) with an explicit status above.</div>`;
  panel.innerHTML = html;
}
function renderUnsupportedPanel(j, id) {
  panel.innerHTML = `<h3>MODEL id ${id} — UNSUPPORTED</h3>
    <div class="warnbox">${esc(j.reason ?? 'UNSUPPORTED')}</div>
    <div class="note">era ${ERA} — shown explicitly, never hidden, never faked.</div>`;
  el('viewmsg').textContent = `UNSUPPORTED — ${String(j.reason ?? '').slice(0, 120)}`;
}

function updateBadges() {
  el('b-index').innerHTML = `index: <b>${state.indexCount ?? '—'}</b> models`;
  el('b-model').innerHTML = `model: <b>${state.currentId ?? '—'}</b>`;
  const sb = el('b-status');
  sb.innerHTML = `status: <b>${state.modelStatus ?? '—'}</b>`;
  sb.className = 'badge ' + (state.modelStatus === 'IR_READY' ? 'ok' : state.modelStatus ? 'fail' : '');
  el('b-tex').innerHTML = `textures: <b>bound ${state.texBound} / missing ${state.texMissing}</b> (joins ${state.texTotal})`;
  el('b-revision').innerHTML = `three: <b>r${THREE.REVISION}</b>`;
  updateAnimBadge();
}

// ---------- list UI ----------
function renderList() {
  const q = el('search').value.trim().toLowerCase();
  state.filtered = state.entries.filter(e => !q || e.name.toLowerCase().includes(q) || String(e.id).includes(q));
  const maxPage = Math.max(0, Math.ceil(state.filtered.length / PAGE) - 1);
  if (state.page > maxPage) state.page = maxPage;
  const slice = state.filtered.slice(state.page * PAGE, (state.page + 1) * PAGE);
  el('models').innerHTML = slice.map(e =>
    `<div class="mrow${e.id === state.currentId ? ' sel' : ''}" data-id="${e.id}">${esc(e.name)} <small>${(e.size / 1024).toFixed(0)} KB</small></div>`
  ).join('');
  el('pg-info').textContent = `${state.filtered.length} models · page ${state.page + 1}/${maxPage + 1}`;
  for (const row of el('models').querySelectorAll('.mrow')) {
    row.onclick = () => loadModel(Number(row.dataset.id));
  }
}

// ---------- model load ----------
async function loadModel(id) {
  state.currentId = id;
  state.modelStatus = 'LOADING';
  updateBadges();
  renderList();
  try {
    const r = await fetch(`/api/assets/model?id=${id}`);
    const j = await r.json();
    if (j.status === 'UNSUPPORTED' || j.status === 'NOT_FOUND' || j.status === 'ERROR') {
      state.modelStatus = `UNSUPPORTED (${j.status})`;
      renderUnsupportedPanel(j, id);
      updateBadges();
      return;
    }
    clearModel();
    state.parseStatus = j.parseStatus;
    state.numBlocks = Object.values(j.blockCensus).reduce((a, c) => a + c.count, 0);
    state.opaqueCount = j.opaqueCount;
    state.kfUnsupportedCount = (j.blockCensus['NiKeyframeController']?.count ?? 0) + (j.blockCensus['NiKeyframeData']?.count ?? 0);
    state.vertices = j.shapes.reduce((a, s) => a + s.numVertices, 0);
    state.triangles = j.shapes.reduce((a, s) => a + s.numTriangles, 0);

    // texture fetch (bounded: distinct resolved ids only)
    const textureByShape = new Map();
    const cache = new Map();
    state.texTotal = 0; state.texBound = 0; state.texMissing = 0; state.texPerJoin = [];
    for (const tj of j.textureJoins) {
      for (const jj of tj.joins) {
        state.texTotal++;
        if (!jj.resolved || jj.textureId == null) {
          jj.status = 'UNTEXTURED — ' + (jj.reason ?? 'unresolved join');
          state.texMissing++;
          state.texPerJoin.push({ shape: tj.shapeIndex, slot: jj.slot, status: jj.status });
          continue;
        }
        if (!cache.has(jj.textureId)) {
          try {
            const payload = await fetchTexture(jj.textureId);
            const dec = decodeTexture(payload, jj.arkEntry.name);
            const tex = makeTexture(dec);
            cache.set(jj.textureId, { tex, dec });
          } catch (te) {
            cache.set(jj.textureId, { err: String(te.message ?? te) });
          }
        }
        const c = cache.get(jj.textureId);
        if (c.err) {
          jj.status = `DECODE_FAIL (${c.err.slice(0, 50)})`;
          jj.reason = c.err.slice(0, 120);
          state.texMissing++;
        } else {
          jj.status = 'BOUND';
          jj.decInfo = `${c.dec.format} ${c.dec.width}×${c.dec.height}`;
          textureByShape.set(tj.shapeIndex, c.tex);
          state.texBound++;
        }
        state.texPerJoin.push({ shape: tj.shapeIndex, slot: jj.slot, status: jj.status, texId: jj.textureId });
      }
    }
    // AV-3/AV-5: models WITH decoded keyframe controllers OR a decoded skin
    // binding render through the hierarchy tree (THREE.Bone nodes when
    // skinned; KF mixer animates the tree — skinning follows the bones);
    // models WITHOUT them keep the AV-2 flattened world-TRS path unchanged.
    const hasKf = !!(j.keyframeAnim && j.keyframeAnim.controllers && j.keyframeAnim.controllers.length && j.keyframeAnim.closureAll === true);
    const hasSkin = !!(j.shapes && j.shapes.some(s => s.skin && s.skin.ok));
    modelGroup = (hasKf || hasSkin) ? buildKfModel(j, textureByShape) : addShapes(j, textureByShape);
    frameOn(j);
    buildAnimation(j, textureByShape);
    if (hasKf) {
      kfCtx.clips = buildKfClips(j);
      animCtx.clips = animCtx.clips.concat(kfCtx.clips);
      const kfc0 = j.keyframeAnim.controllers[0];
      state.anim.kf = {
        clips: kfCtx.clips.length,
        tracks: kfCtx.clips.reduce((a, c) => a + c.tracks.length, 0),
        controllers: j.keyframeAnim.controllers.length,
        textKeys: (j.keyframeAnim.textKeys || []).flatMap(t => t.keys.map(k => k.text)),
        closureAll: j.keyframeAnim.closureAll,
        failures: j.keyframeAnim.failures?.length ?? 0,
        loopPolicy: 'ENGINEERING_LABEL',
        firstController: { target: kfc0.target, startTime: kfc0.startTime, stopTime: kfc0.stopTime, frequency: kfc0.frequency, phase: kfc0.phase },
      };
      state.anim.clips = animCtx.clips.length;
      // refresh the clip selector with the merged list (UV + KF)
      el('clip-sel').innerHTML = '<option value="-1">— no clip —</option>' +
        animCtx.clips.map((c, i) => {
          const kind = c.userData?.kind === 'kf' ? 'KF' : 'UV';
          return `<option value="${i}">[${kind}] ${c.name} (${c.duration.toFixed(2)}s)</option>`;
        }).join('');
    }
    state.modelStatus = 'IR_READY';
    renderPanel(j);
  } catch (e) {
    state.modelStatus = 'LOAD_FAIL';
    logErr('model', e.message ?? e);
    panel.innerHTML = `<div class="warnbox">LOAD FAIL: ${esc(String(e.message ?? e))}</div>`;
  }
  updateBadges();
}
window.__AV_LOAD_MODEL__ = loadModel; // gate hook (returns promise implicitly)

// ---------- AV-3 gate hooks ----------
// node world position (Three space, after the era converter wrapper)
window.__AV_NODE_POS__ = (idx) => {
  const o = kfCtx.nodes.get(idx);
  if (!o) return null;
  o.updateWorldMatrix(true, false);
  const p = o.getWorldPosition(new THREE.Vector3());
  return [p.x, p.y, p.z];
};
// NaN / non-finite sweep over the live KF scene subtree
window.__AV_NAN_CHECK__ = () => {
  if (!kfCtx.root) return { naN: -1, checked: 0 };
  let naN = 0, checked = 0;
  kfCtx.root.traverse((o) => {
    o.updateWorldMatrix(true, false);
    checked++;
    for (const v of o.matrixWorld.elements) if (!Number.isFinite(v)) { naN++; break; }
    if (o.geometry && o.geometry.attributes.position) {
      for (let i = 0; i < o.geometry.attributes.position.array.length; i++) {
        if (!Number.isFinite(o.geometry.attributes.position.array[i])) { naN++; break; }
      }
    }
  });
  return { naN, checked };
};
// KF clip info (index within the merged selector)
window.__AV_KF_INFO__ = () => {
  const kfClips = animCtx.clips.filter(c => c.userData?.kind === 'kf');
  return { clips: kfClips.length, tracks: kfClips.reduce((a, c) => a + c.tracks.length, 0),
    names: kfClips.map(c => c.name), durations: kfClips.map(c => c.duration),
    kfIdx: animCtx.clips.map((c, i) => c.userData?.kind === 'kf' ? i : -1).filter(i => i >= 0),
    anim: state.anim.kf };
};
// AV-5 skin gate hook: live skinned-mesh stats (bbox stability, NaN sweep,
// weights-sum check, influence truncation accounting)
window.__AV_SKIN_INFO__ = () => {
  if (!kfCtx.root) return { skinned: 0 };
  let skinned = 0, naN = 0, checked = 0;
  const boxes = [];
  kfCtx.root.updateMatrixWorld(true);
  kfCtx.root.traverse(o => {
    if (o.isSkinnedMesh) {
      skinned++;
      o.skeleton.update();
      o.geometry.computeBoundingBox();
      const b = o.geometry.boundingBox;
      boxes.push([b.min.x, b.min.y, b.min.z, b.max.x, b.max.y, b.max.z]);
      const idx = o.geometry.getAttribute('skinIndex');
      const w = o.geometry.getAttribute('skinWeight');
      let badSum = 0;
      for (let v = 0; v < w.count; v++) {
        const s = w.getX(v) + w.getY(v) + w.getZ(v) + w.getW(v);
        if (!Number.isFinite(s) || Math.abs(s - 1) > 1e-2) badSum++;
        for (let k = 0; k < 4; k++) {
          if (idx.getComponent(v, k) >= o.skeleton.bones.length) naN++;
        }
      }
      if (badSum) naN += badSum;
      checked++;
    }
  });
  return { ...state.skinInfo, skinned, checked, naN, boxes };
};

// ---------- anim UI wiring ----------
el('btn-play').onclick = () => { if (animCtx.action) { animCtx.action.paused = false; state.anim.playing = true; updateAnimBadge(); } else playClip(el('clip-sel').value); };
el('btn-pause').onclick = () => { if (animCtx.action) { animCtx.action.paused = true; state.anim.playing = false; updateAnimBadge(); } };
el('btn-stop').onclick = () => playClip(-1);
el('clip-sel').onchange = () => playClip(Number(el('clip-sel').value));
el('seek').oninput = (ev) => {
  if (animCtx.action && state.anim.duration > 0) {
    animCtx.action.time = (Number(ev.target.value) / 1000) * state.anim.duration;
    state.anim.time = animCtx.action.time;
    el('time').textContent = `${state.anim.time.toFixed(2)}s`;
    if (animCtx.mixer) animCtx.mixer.update(0);
  }
};
el('speed').oninput = (ev) => {
  const v = Number(ev.target.value) / 10;
  el('speedval').textContent = `${v.toFixed(1)}×`;
  if (animCtx.mixer) animCtx.mixer.timeScale = v;
};
let wireOn = false;
el('btn-wire').onclick = () => {
  wireOn = !wireOn;
  if (modelGroup) modelGroup.traverse(o => { if (o.material) { o.material.wireframe = wireOn; } });
  el('btn-wire').textContent = `wireframe: ${wireOn ? 'on' : 'off'}`;
  el('btn-wire').classList.toggle('off', !wireOn);
};
el('btn-tex').onclick = () => {
  const on = el('btn-tex').textContent.endsWith('off');
  if (modelGroup) modelGroup.traverse(o => {
    if (o.material && o.material.map) { o.material.map.visible = on; o.material.needsUpdate = true; }
  });
  el('btn-tex').textContent = `textures: ${on ? 'on' : 'off'}`;
};
el('search').oninput = () => { state.page = 0; renderList(); };
el('pg-prev').onclick = () => { if (state.page > 0) { state.page--; renderList(); } };
el('pg-next').onclick = () => { state.page++; renderList(); };

// ---------- main ----------
const clock = new THREE.Clock();
(async function main() {
  initViewport();
  renderer.setAnimationLoop(() => {
    const dt = clock.getDelta();
    if (animCtx.mixer) {
      animCtx.mixer.update(dt);
      // drive the UV offset of every bound texture from the proxy track value
      const off = animCtx.proxy && animCtx.proxy.uvOffset;
      if (off) for (const t of textureObjs) { /* legacy no-op */ }
      if (off && modelGroup) modelGroup.traverse(o => {
        if (o.material && o.material.map) o.material.map.offset.set(off.x, off.y);
      });
      state.anim.time = animCtx.action ? animCtx.action.time : 0;
      el('time').textContent = `${state.anim.time.toFixed(2)}s`;
    }
    if (kfCtx.mixer) {
      kfCtx.mixer.update(dt);
      if (animCtx.action && animCtx.action.getClip().userData?.kind === 'kf') {
        state.anim.time = animCtx.action.time;
        el('time').textContent = `${state.anim.time.toFixed(2)}s`;
      }
    }
    controls.update();
    renderer.render(scene, camera);
  });
  try {
    const r = await fetch('/api/assets/index');
    const j = await r.json();
    if (j.status !== 'OK') throw new Error(j.reason ?? 'index not OK');
    state.entries = j.entries;
    state.indexCount = j.count;
    state.filtered = j.entries;
    state.status = 'INDEX_READY';
    state.doneIndex = true;
    renderList();
    updateBadges();
    // deep-link / gate entry: ?model=<id> (optional &play=1 autoplays the
    // first clip — deep-link feature, used by the headless gate runs)
    const qid = new URLSearchParams(location.search).get('model');
    if (qid) {
      await loadModel(Number(qid));
      if (new URLSearchParams(location.search).get('play') === '1') {
        const kInfo = window.__AV_KF_INFO__?.() ?? {};
        const first = kInfo.kfIdx?.length ? kInfo.kfIdx[0] : (animCtx.clips.length ? 0 : -1);
        if (first >= 0) playClip(first);
      }
    }
  } catch (e) {
    state.status = 'INDEX_FAIL';
    logErr('index', e.message ?? e);
    panel.innerHTML = `<div class="warnbox">INDEX FAIL: ${esc(String(e.message ?? e))}</div>`;
  }
  state.status = state.status === 'INDEX_READY' ? 'READY' : state.status;
  updateBadges();
})();
