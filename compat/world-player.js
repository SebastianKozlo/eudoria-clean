// world-player.js â€” PE_WORLD_8163 W4-1: THE GAME CHARACTER REF pawn in /world
// (staging 8171 ONLY; never production 8163).
//
// SOURCE (all game data, zero synthetic motion):
//   PCG_9_3_5 Models.bnt (C950A8C2...B3D3BEE0) member 546608 â€” skinned biped
//   (Mesh:0, 11161 verts, 38 skin bones, NiSkinData weights â€” max 3 influences,
//   NO truncation) + texture chain ArkTexture BASE=bnt2Id 546609 (Textures.bnt).
//   Clip members 546617 (idle KINEMATIC_CLASSIFICATION) + 546613 (walk
//   KINEMATIC_CLASSIFICATION) â€” LINEAR keys (OBSERVED), source keytimes kept.
// IDENTITY: GAME_CHARACTER_REF â€” MOB-family humanoid biped (Tail/cannon/drill/
//   flash bones), NOT the creator avatar (which is 567279/576976, no KF clips).
// BIND LAW (verified numerically W4-1): world = parentWorld*local,
//   p' = (R*p)*s + t (GB contract, PecTransform.js law); W_i * SkinToBone_i = I.
// QUATS: clip key0 quat == rig node rotation 33/33 (standard formula) ->
//   THREE.Quaternion(x,y,z,w) directly; translations are node-local (37/37).
// ENGINEERING labels (runtime policies, NOT source claims): LoopRepeat loop
//   policy, 0.25s crossfade, 2.0 m height calibration, third-person camera,
//   4 m/s walk speed, input-driven idle<->walk switching.
'use strict';

import * as THREE from 'three';
// NOTE: world-vegetation.js is NOT imported (module wiring side effects); the
// texture payload is decoded with the SAME production decoders exposed as
// client modules (/src/pesource/TgaDecoder.js + /src/pesource/DdsDecoder.js).

const CFG = {
  crossfadeSec: 0.25,       // ENGINEERING
  walkSpeed: 4.0,           // ENGINEERING (m/s)
  targetHeightM: 2.0,       // RUNTIME_CALIBRATION target (honest label)
  switchSpeedThreshold: 0.2,// ENGINEERING
};

const dbg = window.__peR2Debug;
let scene, camera, renderer;
let root = null, yawGroup = null, skinnedMesh = null, mixer = null;
let actions = null, activeName = 'idle', clipSwitchCount = 0;
let keys = new Set();
let charYaw = 0;
let camFramed = false;
let rigByName = null, rigRootBone = null;
let feetShiftY = 0;
const charPos = new THREE.Vector3();
let paused = false, speedScale = 1.0;
let ready = false;
let bindReport = null;
let texInfo = null;

function log(...a) { console.log('[world-player]', ...a); }

async function fetchBinary(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`fetch ${url} -> ${res.status}`);
  const buf = await res.arrayBuffer();
  const headers = {};
  res.headers.forEach((v, k) => { headers[k] = v; });
  return { payload: new Uint8Array(buf), headers };
}

async function fetchJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`fetch ${url} -> ${res.status}`);
  return res.json();
}

// ---- build the node hierarchy (bind pose from NIF TRS) ----
function buildRig(asset) {
  const byBlock = new Map();
  const byName = new Map();
  const objs = [];
  for (const nd of asset.nodes) {
    const b = new THREE.Bone();
    b.name = nd.name;
    // local matrix from GB law: p' = (R*p)*s + t  -> rows scaled, standard set()
    const s = nd.s;
    const m = new THREE.Matrix4().set(
      nd.r[0] * s, nd.r[1] * s, nd.r[2] * s, 0,
      nd.r[3] * s, nd.r[4] * s, nd.r[5] * s, 0,
      nd.r[6] * s, nd.r[7] * s, nd.r[8] * s, 0,
      nd.t[0], nd.t[1], nd.t[2], 1,
    );
    m.decompose(b.position, b.quaternion, b.scale);
    byBlock.set(nd.blockIndex, b);
    if (!byName.has(nd.name)) byName.set(nd.name, b);
    objs.push({ node: nd, obj: b });
  }
  let rootBone = null;
  for (const { node, obj } of objs) {
    if (node.parent == null) { rootBone = obj; continue; }
    const p = byBlock.get(node.parent);
    if (p) p.add(obj); else rootBone = obj;
  }
  rigByName = byName; rigRootBone = rootBone;
  return { rootBone, byBlock, byName };
}

function buildClips(asset) {
  const clips = {};
  for (const [label, clip] of Object.entries(asset.clips)) {
    const tracks = [];
    for (const t of clip.tracks) {
      if (t.rot.length >= 2) {
        const times = t.rot.map((k) => k[0]);
        const vals = [];
        for (const k of t.rot) vals.push(k[2], k[3], k[4], k[1]); // x,y,z,w
        tracks.push(new THREE.QuaternionKeyframeTrack(`${t.bone}.quaternion`, times, vals));
      }
      if (t.trans.length >= 2) {
        const times = t.trans.map((k) => k[0]);
        const vals = [];
        for (const k of t.trans) vals.push(k[1], k[2], k[3]);
        tracks.push(new THREE.VectorKeyframeTrack(`${t.bone}.position`, times, vals));
      }
    }
    const ac = new THREE.AnimationClip(`clip_${label}_${clip.duration}s`, clip.duration, tracks);
    clips[label] = ac;
  }
  return clips;
}

async function loadTexture(asset) {
  const id = asset.identity.texture.BASE.bnt2Id;
  try {
    const { payload } = await fetchBinary(`/api/world/texture/${id}?era=PCG_9_3_5`);
    // decode with the SAME production decoders, dispatch mirroring
    // world-vegetation.js decodeModelTextureStrict (the strict subset):
    const { decodeTga2, decodeTga2A32Image } = await import('/src/pesource/TgaDecoder.js');
    const { decodeDds } = await import('/src/pesource/DdsDecoder.js');
    let dec = null;
    if (payload[0] === 0x44 && payload[1] === 0x44 && payload[2] === 0x53 && payload[3] === 0x20) {
      const d = decodeDds(payload);
      dec = { width: d.width, height: d.height, rgba: d.rgba, decoder: `decodeDds (${d.fourcc})` };
    } else if (payload.length >= 18 && payload[16] === 32) {
      const d = decodeTga2A32Image(payload);
      dec = { width: d.width, height: d.height, rgba: d.rgba, decoder: 'decodeTga2A32Image' };
    } else if (payload.length >= 18 && payload[16] === 24) {
      const d = decodeTga2(payload);
      dec = { width: d.width, height: d.height, rgba: d.rgba, decoder: 'decodeTga2' };
    }
    if (!dec || !dec.rgba) throw new Error('no production decoder accepted the BASE texture payload (strict subset)');
    const texture = new THREE.DataTexture(dec.rgba, dec.width, dec.height, THREE.RGBAFormat);
    texture.colorSpace = THREE.NoColorSpace;
    texture.flipY = false;
    texture.wrapS = THREE.RepeatWrapping;
    texture.wrapT = THREE.RepeatWrapping;
    texture.minFilter = THREE.LinearFilter;
    texture.magFilter = THREE.LinearFilter;
    texture.needsUpdate = true;
    texInfo = { textureId: id, decoder: dec.decoder, width: dec.width, height: dec.height, resolved: true };
    return texture;
  } catch (e) {
    texInfo = { textureId: id, resolved: false, reason: String(e?.message ?? e).slice(0, 200) };
    return null;
  }
}

// GB-law world position of a named node, computed from the asset tree
// (world = parentWorld * local, p' = (R*p)*s + t — PecTransform.js law,
// numerically verified against SkinToBone in W4-1).
function upAxisFromAsset(asset) {
  const byNameA = new Map();
  const parentOf = new Map();
  for (const nd of asset.nodes) {
    if (!byNameA.has(nd.name)) byNameA.set(nd.name, nd);
    if (nd.parent != null) parentOf.set(nd.blockIndex, nd.parent);
  }
  const mvB = (m, v) => [
    m[0] * v[0] + m[1] * v[1] + m[2] * v[2],
    m[3] * v[0] + m[4] * v[1] + m[5] * v[2],
    m[6] * v[0] + m[7] * v[1] + m[8] * v[2],
  ];
  const mul = (a, b) => {
    const out = [0, 0, 0, 0, 0, 0, 0, 0, 0];
    for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) {
      out[i * 3 + j] = a[i * 3] * b[j] + a[i * 3 + 1] * b[3 + j] + a[i * 3 + 2] * b[6 + j];
    }
    return out;
  };
  const worldPos = (name) => {
    const nd = byNameA.get(name);
    if (!nd) return [0, 0, 0];
    let chain = [];
    let cur = nd.blockIndex;
    const seen = new Set();
    while (cur != null && !seen.has(cur)) { seen.add(cur); chain.push(cur); cur = parentOf.get(cur); }
    // start at the leaf (chain[0] == the node itself)
    const leaf = byNameA.get(asset.nodes.find((x) => x.blockIndex === chain[0])?.name);
    let m = [...leaf.r], t = [...leaf.t];
    for (let k = 1; k < chain.length; k++) {
      const n = asset.nodes.find((x) => x.blockIndex === chain[k]);
      if (!n) continue;
      t = [mvB(n.r, t)[0] + n.t[0], mvB(n.r, t)[1] + n.t[1], mvB(n.r, t)[2] + n.t[2]];
      m = mul(n.r, m);
    }
    return t;
  };
  const h = worldPos('Bip01 Head');
  const p = worldPos('Bip01 Pelvis');
  return { x: h[0] - p[0], y: h[1] - p[1], z: h[2] - p[2] };
}

async function boot() {
  if (!dbg || !window.__peWorldScene) { setTimeout(boot, 250); return; }
  scene = window.__peWorldScene.scene;
  camera = window.__peWorldScene.camera;
  renderer = window.__peWorldScene.renderer;
  const asset = await fetchJson('/compat/player-character-ref.json');

  const { rootBone, byBlock, byName } = buildRig(asset);
  // skinned mesh = the single hasSkin mesh (Mesh:0)
  const skinMeshDef = asset.meshes.find((m) => m.hasSkin);
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(skinMeshDef.positions, 3));
  if (skinMeshDef.normals) g.setAttribute('normal', new THREE.Float32BufferAttribute(skinMeshDef.normals, 3));
  if (skinMeshDef.uvs) g.setAttribute('uv', new THREE.Float32BufferAttribute(skinMeshDef.uvs, 2));
  g.setIndex(skinMeshDef.indices);
  const skin = asset.skin;
  g.setAttribute('skinIndex', new THREE.Uint16BufferAttribute(skin.skinIndex, 4));
  g.setAttribute('skinWeight', new THREE.Float32BufferAttribute(skin.skinWeight, 4));

  const bones = skin.bones.map((blk) => byBlock.get(blk));
  const boneInverses = skin.boneInverses.map((m12) =>
    new THREE.Matrix4().set(
      m12[0], m12[1], m12[2], 0,
      m12[3], m12[4], m12[5], 0,
      m12[6], m12[7], m12[8], 0,
      m12[9], m12[10], m12[11], 1,
    ));
  const skeleton = new THREE.Skeleton(bones, boneInverses);

  skinnedMesh = new THREE.SkinnedMesh(g, new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.DoubleSide }));
  const tex = await loadTexture(asset);
  if (tex) skinnedMesh.material.map = tex;
  skinnedMesh.material.needsUpdate = true;
  skinnedMesh.add(rootBone); // skeleton root lives under the mesh (bind space)
  skinnedMesh.bind(skeleton);

  root = new THREE.Group();
  root.name = 'GAME_CHARACTER_REF_546608';
  yawGroup = new THREE.Group();
  root.add(yawGroup);
  yawGroup.add(skinnedMesh);
  scene.add(root);

  // ---- clips + mixer FIRST (clip t0 == bind pose, VERIFIED W4-1: 37/37
  // translations, 33/33 quats equal the rig node TRS) ----
  const clips = buildClips(asset);
  mixer = new THREE.AnimationMixer(root);
  actions = {};
  for (const [label, clip] of Object.entries(clips)) {
    const a = mixer.clipAction(clip);
    a.loop = THREE.LoopRepeat;   // ENGINEERING loop policy
    a.play();
    a.fadeOut(0);                // start faded out except idle
    actions[label] = a;
  }
  actions.idle.fadeIn(CFG.crossfadeSec);
  activeName = 'idle';
  mixer.update(0);               // pose the rig at clip t0 (= bind pose)

  // ---- orientation/scale calibration (deterministic: the GB-law chain math
  // straight from the asset node tree — the same law verified numerically
  // against SkinToBone in W4-1; matrixWorld proved unreliable pre-render) ----
  const up = upAxisFromAsset(asset);   // head-pelvis world delta (GB law)
  const ax = Math.abs(up.x) > Math.abs(up.y) && Math.abs(up.x) > Math.abs(up.z) ? 'x'
    : (Math.abs(up.y) >= Math.abs(up.z) ? 'y' : 'z');
  const sign = up.x !== 0 || up.y !== 0 || up.z !== 0 ? Math.sign(ax === 'x' ? up.x : ax === 'y' ? up.y : up.z) : 1;
  // bind bbox in root-local space (scale 1, rotation 0): skinned geometry
  const box = new THREE.Box3();
  const tmp = new THREE.Vector3();
  const pos = g.getAttribute('position');
  for (let i = 0; i < pos.count; i += 7) {
    tmp.fromBufferAttribute(pos, i);
    skinnedMesh.applyBoneTransform(i, tmp);
    box.expandByPoint(tmp);
  }
  const size = box.getSize(new THREE.Vector3());
  bindReport = {
    bindBboxSize: { x: +size.x.toFixed(2), y: +size.y.toFixed(2), z: +size.z.toFixed(2) },
    bindBboxMin: { x: +box.min.x.toFixed(1), y: +box.min.y.toFixed(1), z: +box.min.z.toFixed(1) },
    bindBboxMax: { x: +box.max.x.toFixed(1), y: +box.max.y.toFixed(1), z: +box.max.z.toFixed(1) },
    upAxisMeasured: ax,
    upSign: sign,
    headPelvisVec: { x: +up.x.toFixed(1), y: +up.y.toFixed(1), z: +up.z.toFixed(1) },
    sourceHeight: +(ax === 'x' ? size.x : ax === 'y' ? size.y : size.z).toFixed(2),
  };
  const scale = CFG.targetHeightM / bindReport.sourceHeight;
  // orient the NIF up-axis (measured, incl. sign) to world +Y
  // (RENDER space, RUNTIME_CALIBRATION — evidence recorded in bindReport)
  if (ax === 'y' && sign < 0) root.rotation.z = Math.PI;        // up = -Y -> flip
  else if (ax === 'y') { /* up = +Y already */ }
  else if (ax === 'z') root.rotation.x = sign > 0 ? -Math.PI / 2 : Math.PI / 2;
  else if (ax === 'x') root.rotation.z = sign > 0 ? Math.PI / 2 : -Math.PI / 2;
  root.scale.setScalar(scale);

  // feet calibration: shift so the posed geometry bottom sits at root origin
  root.updateMatrixWorld(true);
  const worldBox = new THREE.Box3().setFromObject(root);
  feetShiftY = worldBox.min.y - root.position.y; // <= 0 typically
  bindReport.feetShiftY = +feetShiftY.toFixed(3);
  bindReport.worldBbox = {
    min: { x: +worldBox.min.x.toFixed(2), y: +worldBox.min.y.toFixed(2), z: +worldBox.min.z.toFixed(2) },
    max: { x: +worldBox.max.x.toFixed(2), y: +worldBox.max.y.toFixed(2), z: +worldBox.max.z.toFixed(2) },
  };
  bindReport.scaleApplied = +scale.toFixed(6);

  // ---- spawn: wait for the shared height query (the terrain window builds
  // asynchronously); then feet on the REAL surface at the viewed focus ----
  const ctl = window.__peWorldScene.controls;
  const focus = () => (ctl ? [ctl.target.x, ctl.target.z] : [dbg.camera.x, dbg.camera.z]);
  let [x, z] = focus();
  let y = dbg.queryHeightAt(x, z);
  for (let tries = 0; y == null && tries < 120; tries++) {   // up to ~30 s
    await new Promise((r) => setTimeout(r, 250));
    [x, z] = focus();          // the viewed focus may settle after init
    y = dbg.queryHeightAt(x, z);
  }
  if (y == null) { x = 0; z = 0; y = dbg.queryHeightAt(0, 0) ?? 0; }
  charPos.set(x, y, z);
  ready = true;
  log('ready', { bindReport, texInfo, spawn: { x, y, z }, scale: +scale.toFixed(5) });
  requestAnimationFrame(tick);
}

// ---- input (non-capturing; WASD/arrows) ----
window.addEventListener('keydown', (ev) => {
  if (!ready) return;
  const k = ev.key.toLowerCase();
  if (['w', 'a', 's', 'd', 'arrowup', 'arrowdown', 'arrowleft', 'arrowright'].includes(k)) keys.add(k);
});
window.addEventListener('keyup', (ev) => keys.delete(ev.key.toLowerCase()));
window.addEventListener('blur', () => keys.clear());

let lastT = performance.now();
function tick() {
  requestAnimationFrame(tick);
  const now = performance.now();
  const dt = Math.min(0.1, (now - lastT) / 1000) * speedScale;
  lastT = now;

  // move in camera-yaw space
  let mx = 0, mz = 0;
  if (keys.has('w') || keys.has('arrowup')) mz += 1;
  if (keys.has('s') || keys.has('arrowdown')) mz -= 1;
  if (keys.has('a') || keys.has('arrowleft')) mx -= 1;
  if (keys.has('d') || keys.has('arrowright')) mx += 1;
  const moving = (mx !== 0 || mz !== 0);
  const speed = moving ? CFG.walkSpeed : 0;

  if (moving) {
    const camDir = new THREE.Vector3();
    camera.getWorldDirection(camDir); camDir.y = 0; camDir.normalize();
    const camRight = new THREE.Vector3().crossVectors(camDir, new THREE.Vector3(0, 1, 0)).normalize();
    const dir = new THREE.Vector3().addScaledVector(camDir, mz).addScaledVector(camRight, mx).normalize();
    const nx = charPos.x + dir.x * CFG.walkSpeed * dt;
    const nz = charPos.z + dir.z * CFG.walkSpeed * dt;
    const h = dbg.queryHeightAt(nx, nz);
    if (h != null) { charPos.x = nx; charPos.z = nz; charPos.y = h; } // feet on ground
    charYaw = Math.atan2(dir.x, dir.z);
  } else {
    const h = dbg.queryHeightAt(charPos.x, charPos.z);
    if (h != null) charPos.y = h;
  }

  // idle<->walk switching (input speed > threshold)
  const want = speed > CFG.switchSpeedThreshold ? 'walk' : 'idle';
  if (want !== activeName && actions) {
    actions[activeName].fadeOut(CFG.crossfadeSec);
    actions[want].fadeIn(CFG.crossfadeSec);
    actions[want].reset();
    activeName = want;
    clipSwitchCount++;
  }

  if (root && yawGroup) {
    root.position.set(charPos.x, charPos.y, charPos.z);
    yawGroup.rotation.y = charYaw; // yaw in the character's own (up-oriented) frame
  }
  if (mixer && !paused) mixer.update(dt);

  // third-person camera (ENGINEERING): COOPERATE with the app's OrbitControls
  // (its animate() calls controls.update() AFTER our tick would move the
  // camera — fighting it loses). We set the controls TARGET to the character
  // each frame and reposition the camera ONCE; OrbitControls then keeps the
  // camera at a constant offset while following the character (and the user
  // can still orbit-drag around it — a free 3rd-person orbit).
  if (root && window.__peWorldScene.controls) {
    const controls = window.__peWorldScene.controls;
    if (!camFramed) {
      camera.position.set(charPos.x, charPos.y + 2.4, charPos.z + 6.0);
      camFramed = true;
    }
    controls.target.set(charPos.x, charPos.y + 1.2, charPos.z);
  }
}

// ---- G5 + QC debug handle ----
window.__pePlayer = {
  get ready() { return ready; },
  get bootError() { return bootError; },
  get activeClip() { return activeName; },
  get clipSwitchCount() { return clipSwitchCount; },
  get position() { return ready ? { x: +charPos.x.toFixed(2), y: +charPos.y.toFixed(2), z: +charPos.z.toFixed(2) } : null; },
  get identity() { return 'GAME_CHARACTER_REF (Models.bnt 546608 + clips 546617/546613, PCG_9_3_5)'; },
  get bindReport() { return bindReport; },
  get texture() { return texInfo; },
  nanCheck() {
    if (!root || !skinnedMesh) return null;
    let nan = 0;
    root.traverse((o) => {
      if (!Number.isFinite(o.position?.x ?? 0) || !Number.isFinite(o.quaternion?.x ?? 0)) nan++;
      if (o.matrixWorld && [...o.matrixWorld.elements].some((v) => !Number.isFinite(v))) nan++;
    });
    const box = new THREE.Box3().setFromObject(root);
    const size = box.getSize(new THREE.Vector3());
    return {
      nanObjects: nan,
      bbox: { x: +size.x.toFixed(3), y: +size.y.toFixed(3), z: +size.z.toFixed(3) },
      bboxFinite: Number.isFinite(size.x) && Number.isFinite(size.y) && Number.isFinite(size.z),
    };
  },
  setPaused(p) { paused = !!p; return paused; },
  seek(clip, t) { if (actions?.[clip]) { actions[clip].time = t; } return actions?.[clip]?.time ?? null; },
  setSpeed(s) { speedScale = +s; return speedScale; },
  projectToScreen() {
    if (!ready || !camera) return null;
    const v = new THREE.Vector3(charPos.x, charPos.y + 1.0, charPos.z).project(camera);
    return { sx: Math.round((v.x + 1) / 2 * (renderer.domElement.clientWidth || 1280)), sy: Math.round((1 - (v.y + 1) / 2) * (renderer.domElement.clientHeight || 720)) };
  },
  debugBones() {
    const byName2 = rigByName;
    let viaTraverse = null;
    root.traverse((o) => { if (o.name === 'Bip01 Head' && !viaTraverse) viaTraverse = o; });
    const h1 = byName2.get('Bip01 Head');
    return {
      byNameHeadLocal: h1 ? h1.position.toArray() : null,
      byNameHeadIsTraverseHead: h1 === viaTraverse,
      traverseHeadLocal: viaTraverse ? viaTraverse.position.toArray() : null,
      skinnedMeshChildren: skinnedMesh.children.map((c) => c.name),
      rootBoneName: rigRootBone?.name ?? null,
      rootBoneInTree: rigRootBone ? rigRootBone.parent?.name ?? '(no parent)' : null,
    };
  },
};

let bootError = null;
const bootSafe = async () => { try { await boot(); } catch (e) { bootError = String(e?.stack ?? e).slice(0, 800); console.error('[world-player] BOOT FAILED', e); } };
bootSafe();
