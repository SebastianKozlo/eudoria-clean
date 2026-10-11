// pcg935-viewer.js — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010 (Wave 7)
// Full-asset SceneIR viewer application (zero-framework ES module).
//   - every Models.bnt entry in the catalog (including parse-failed rows)
//   - REAL parse per selection (server-side, era-dispatched reader)
//   - real textures via the controlled chain (era-labelled states; checker
//     board = visible PARTIAL, never TEXTURED_EXACT)
//   - original animations: keyframe/textkey/skinning with mixer playback,
//     play/pause/stop/scrub/speed/once-repeat, drift-free looping evidence
//   - latest-wins generation identity; full disposal on asset change
//   - deep links (#asset/<id>), search/filter/sort, parts drawer, toggles.
'use strict';

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const $ = (id) => document.getElementById(id);
const canvas = $('c');

// ---------------------------------------------------------------- three setup

const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x101418);
const camera = new THREE.PerspectiveCamera(55, 1, 0.05, 100000);
camera.position.set(4, 3, 6);
const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.dampingFactor = 0.08;

const axesGroup = new THREE.Group();
const gridHelper = new THREE.GridHelper(10, 20, 0x3a4a5a, 0x232c36);
gridHelper.position.y = 0;
axesGroup.add(new THREE.AxesHelper(2));
axesGroup.add(gridHelper);
scene.add(axesGroup);
const boundsBox = new THREE.Box3Helper(new THREE.Box3(), new THREE.Color(0x4fa3d1));
boundsBox.visible = false;
scene.add(boundsBox);

{
  const hemi = new THREE.HemisphereLight(0xdfe8ef, 0x2a3038, 2.2);
  scene.add(hemi);
  const dir = new THREE.DirectionalLight(0xffffff, 1.6);
  dir.position.set(5, 9, 7);
  scene.add(dir);
}

function resize() {
  const w = canvas.clientWidth || 1;
  const h = canvas.clientHeight || 1;
  renderer.setSize(w, h, false);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
}
window.addEventListener('resize', resize);
resize();

renderer.setAnimationLoop(() => {
  controls.update();
  if (mixerState.mixer && mixerState.playing) mixerState.mixer.update(mixerState.clock.getDelta());
  renderFrameCount++;
  renderer.render(scene, camera);
});
let renderFrameCount = 0;

// ---------------------------------------------------------------- catalog ui

let catalog = null;
let filteredRows = [];
let renderedCount = 0;
const ROW_CHUNK = 200;

async function loadCatalog() {
  const res = await fetch('/api/catalog');
  if (!res.ok) throw new Error(`catalog HTTP ${res.status}`);
  catalog = await res.json();
  $('drawer-stats').textContent =
    `${catalog.stats.total} entries · ${catalog.stats.pass} parsed · ${catalog.stats.fail} failed · ` +
    `v10 ${catalog.stats.byVersion['10.1.0.0']} / v4.1 ${catalog.stats.byVersion['4.1.0.12']} / v4.0 ${catalog.stats.byVersion['4.0.0.2']}`;
  applyFilters();
}

function applyFilters() {
  if (!catalog) return;
  const q = $('search').value.trim().toLowerCase();
  const ver = $('f-version').value;
  const st = $('f-status').value;
  let rows = catalog.entries;
  if (q) rows = rows.filter((r) => String(r.id).includes(q) || String(r.name).toLowerCase().includes(q));
  if (ver) rows = rows.filter((r) => r.v === ver);
  if (st === 'PASS') rows = rows.filter((r) => r.status !== 'FAIL');
  if (st === 'FAIL') rows = rows.filter((r) => r.status === 'FAIL');
  if (st === 'animated') rows = rows.filter((r) => (r.kf || 0) > 0);
  if (st === 'skinned') rows = rows.filter((r) => (r.skin || 0) > 0);
  if (st === 'textured') rows = rows.filter((r) => (r.arkTex || 0) > 0);
  if (st === 'mesh') rows = rows.filter((r) => (r.meshes || 0) > 0);
  if (st === 'nomesh') rows = rows.filter((r) => (r.meshes || 0) === 0);

  const sortKey = $('f-sort').value;
  const cmp = {
    extent: (a, b) => {
      if (a.extent == null && b.extent == null) return a.id - b.id;
      if (a.extent == null) return 1;
      if (b.extent == null) return -1;
      if (b.extent !== a.extent) return b.extent - a.extent;
      return a.id - b.id;
    },
    bytes: (a, b) => b.size - a.size || a.id - b.id,
    tris: (a, b) => (b.tris || 0) - (a.tris || 0) || a.id - b.id,
    verts: (a, b) => (b.verts || 0) - (a.verts || 0) || a.id - b.id,
    diagonal: (a, b) => {
      const da = a.ex ? Math.hypot(a.ex[0], a.ex[1], a.ex[2]) : null;
      const db = b.ex ? Math.hypot(b.ex[0], b.ex[1], b.ex[2]) : null;
      if (da == null && db == null) return a.id - b.id;
      if (da == null) return 1;
      if (db == null) return -1;
      return db - da || a.id - b.id;
    },
    vertical: (a, b) => {
      const da = a.ex ? a.ex[2] : null;
      const db = b.ex ? b.ex[2] : null;
      if (da == null && db == null) return a.id - b.id;
      if (da == null) return 1;
      if (db == null) return -1;
      return db - da || a.id - b.id;
    },
  }[sortKey];
  filteredRows = [...rows].sort(cmp);
  renderedCount = 0;
  $('list').innerHTML = '';
  renderMore();
  $('drawer-stats').textContent = `${filteredRows.length} of ${catalog.stats.total} shown · pass ${catalog.stats.pass} / fail ${catalog.stats.fail}`;
}

function renderMore() {
  const frag = document.createDocumentFragment();
  const end = Math.min(renderedCount + ROW_CHUNK, filteredRows.length);
  for (let i = renderedCount; i < end; i++) {
    const r = filteredRows[i];
    const div = document.createElement('div');
    div.className = 'row' + (r.status === 'FAIL' ? ' fail' : '') + (r.extent == null ? ' unknown' : '');
    div.dataset.id = r.id;
    const ext = r.extent != null ? r.extent >= 100 ? Math.round(r.extent) : r.extent.toFixed(1) : 'UNK';
    div.innerHTML =
      `<span class="id">${r.id}</span>` +
      `<span class="nm">${r.name}</span>` +
      `<span class="v">${r.v}${(r.kf || 0) > 0 ? ' ·kf' : ''}${(r.skin || 0) > 0 ? ' ·sk' : ''}${(r.morph || 0) > 0 ? ' ·mp' : ''}${r.status === 'FAIL' ? ' ·FAIL' : ''}</span>` +
      `<span class="ext">${ext}</span>`;
    div.addEventListener('click', () => selectAsset(r.id, true));
    frag.appendChild(div);
  }
  renderedCount = end;
  $('list').appendChild(frag);
  $('more').hidden = renderedCount >= filteredRows.length;
}

$('more').addEventListener('click', renderMore);
$('search').addEventListener('input', debounce(applyFilters, 180));
$('f-version').addEventListener('change', applyFilters);
$('f-status').addEventListener('change', applyFilters);
$('f-sort').addEventListener('change', applyFilters);

function debounce(fn, ms) {
  let t;
  return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); };
}

// ---------------------------------------------------------------- asset lifecycle

let currentAsset = null;   // {id, group, meshes:[{mesh, name, block}], textures:[], geoms:[], mats:[], anim: {...}}
let generation = 0;

async function selectAsset(id, pushHash) {
  const gen = ++generation;
  $('gen-indicator').textContent = `gen ${gen}…`;
  $('gen-indicator').classList.add('busy');
  $('loading').classList.remove('hidden');
  if (pushHash) location.hash = `#asset/${id}`;
  document.querySelectorAll('.row.sel').forEach((el) => el.classList.remove('sel'));
  const rowEl = document.querySelector(`.row[data-id="${id}"]`);
  if (rowEl) rowEl.classList.add('sel');
  disposeAsset();
  let data;
  try {
    const res = await fetch(`/api/asset/${id}`);
    if (!res.ok) {
      const err = await res.json().catch(() => ({ message: `HTTP ${res.status}` }));
      if (gen !== generation) return; // latest-wins: a newer selection superseded this load
      showAssetError(id, res.status, err);
      return;
    }
    data = await res.json();
    if (gen !== generation) return; // latest-wins
  } catch (e) {
    if (gen !== generation) return;
    showAssetError(id, 0, { message: String(e.message || e) });
    return;
  }
  buildAsset(id, data);
  $('gen-indicator').textContent = `gen ${gen}`;
  $('gen-indicator').classList.remove('busy');
  $('loading').classList.add('hidden');
}

function showAssetError(id, status, err) {
  $('loading').classList.add('hidden');
  $('gen-indicator').textContent = `gen ${generation}`;
  $('gen-indicator').classList.remove('busy');
  const fn = $('fail-note');
  fn.classList.remove('hidden');
  fn.innerHTML = `<b>Asset ${id}</b> — HTTP ${status}<br>${escapeHtml(String(err?.message || '')).slice(0, 400)}`;
  $('asset-info').classList.add('hidden');
  currentAsset = null;
}

function disposeAsset() {
  if (!currentAsset) return;
  stopPlayback();
  scene.remove(currentAsset.group);
  currentAsset.group.traverse((o) => {
    if (o.isMesh) {
      o.geometry?.dispose();
      const m = o.material;
      (Array.isArray(m) ? m : [m]).forEach((mm) => {
        mm?.map?.dispose();
        mm?.dispose();
      });
    }
  });
  currentAsset = null;
  $('parts-list').innerHTML = '';
  $('parts-count').textContent = '';
  $('fail-note').classList.add('hidden');
}

// ------------------------------------------------------------- asset building

function b64ToType(b64, Typed) {
  const buf = Uint8Array.from(atob(b64), (c) => c.charCodeAt(0));
  return new Typed(buf.buffer, buf.byteOffset, buf.byteLength / Typed.BYTES_PER_ELEMENT);
}

const checkerTex = (() => {
  const c = document.createElement('canvas');
  c.width = c.height = 64;
  const g = c.getContext('2d');
  for (let y = 0; y < 8; y++) for (let x = 0; x < 8; x++) {
    g.fillStyle = (x + y) % 2 ? '#9aa4ad' : '#6f7a85';
    g.fillRect(x * 8, y * 8, 8, 8);
  }
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
})();

function buildAsset(id, data) {
  const group = new THREE.Group();
  group.name = `asset-${id}`;
  const asset = {
    id, data, group, meshes: [], textures: [], animData: data.animations || {},
    nodeByBlock: new Map(),
    mixers: [], actions: [], clips: [],
  };
  currentAsset = asset;

  const meshesInfo = data.meshes || [];
  const matCache = new Map();

  const makeMaterial = (meshInfo, texStateLabel) => {
    const m = meshInfo.material;
    const mat = new THREE.MeshLambertMaterial({
      color: m?.diffuse ? new THREE.Color().fromArray(m.diffuse) : new THREE.Color(0.95, 0.95, 0.95),
      emissive: m?.emissive ? new THREE.Color().fromArray(m.emissive) : new THREE.Color(0, 0, 0),
      transparent: !!(meshInfo.alphaProp && (meshInfo.alphaProp.flags & 1)),
      opacity: 1,
      side: THREE.DoubleSide,
    });
    if (m?.ambient) mat.color.multiplyScalar(0.5 + 0.5 * (m.ambient[0] ?? 1));
    mat.userData.texState = texStateLabel;
    return mat;
  };

  // First pass: create THREE.Object3D per BLOCK (nodes for the hierarchy).
  const blocks = data.blocks || [];
  for (const b of blocks) {
    const o = new THREE.Object3D();
    o.name = `b${b.i}${b.n ? ':' + b.n : ''}`;
    o.userData.blockIndex = b.i;
    asset.nodeByBlock.set(b.i, o);
  }

  // Meshes
  for (const mi of meshesInfo) {
    const geo = new THREE.BufferGeometry();
    if (mi.positions) geo.setAttribute('position', new THREE.BufferAttribute(b64ToType(mi.positions, Float32Array), 3));
    if (mi.normals) geo.setAttribute('normal', new THREE.BufferAttribute(b64ToType(mi.normals, Float32Array), 3));
    if (mi.uvs) geo.setAttribute('uv', new THREE.BufferAttribute(b64ToType(mi.uvs, Float32Array), 2));
    if (mi.indices) geo.setIndex(new THREE.BufferAttribute(b64ToType(mi.indices, Uint16Array), 1));
    if (!mi.normals) geo.computeVertexNormals();

    // texture binding: the first slot with a decodable id
    let texLabel = 'SOURCE_UNTEXTURED';
    let texId = null;
    for (const slot of mi.texSlots || []) {
      if (slot.textureId != null && slot.state === 'TEXTURED_EXACT') { texId = slot.textureId; texLabel = slot.label || slot.state; break; }
    }
    let mat;
    if (texId != null) {
      if (!matCache.has(texId)) {
        const t = new THREE.TextureLoader().load(`/api/texture/${texId}`);
        t.colorSpace = THREE.SRGBColorSpace;
        t.wrapS = t.wrapT = THREE.RepeatWrapping;
        matCache.set(texId, t);
        asset.textures.push(t);
      }
      mat = makeMaterial(mi, texLabel);
      mat.map = matCache.get(texId);
    } else if ((mi.texSlots || []).some((s) => s.hasMap)) {
      // visible PARTIAL: checkerboard for slots whose chain stayed unresolved
      mat = makeMaterial(mi, 'PARTIAL_CHECKERBOARD');
      mat.map = checkerTex;
    } else {
      mat = makeMaterial(mi, 'SOURCE_UNTEXTURED');
    }
    const mesh = new THREE.Mesh(geo, mat);
    mesh.name = `m${mi.block}:${mi.name}`;
    mesh.userData.blockIndex = mi.block;
    mesh.userData.meshName = mi.name;
    if (mi.world) {
      mesh.applyMatrix4(new THREE.Matrix4().fromArray(mi.world));
    }
    group.add(mesh);
    asset.meshes.push({ mesh, name: mi.name, block: mi.block, tris: mi.numTriangles, verts: mi.numVertices });
  }

  // Skinning: attach bones/skin where the animation data provides them
  const skels = (asset.animData.skeletons || []);
  for (const sk of skels) {
    // bones exist as blocks; bind via the skin data (inverse bind matrices)
    sk._bones = (sk.bones || []).map((b) => asset.nodeByBlock.get(b.boneBlock)).filter(Boolean);
    sk._inverses = (sk.bones || []).map((b) => {
      const m = new THREE.Matrix4();
      if (b.bindRotationQuat) m.makeRotationFromQuaternion(new THREE.Quaternion().fromArray(b.bindRotationQuat));
      if (b.bindTranslation) m.setPosition(new THREE.Vector3().fromArray(b.bindTranslation));
      return m;
    });
  }

  scene.add(group);
  group.updateMatrixWorld(true);

  // Bounds + fit (stable AABB; updateMatrixWorld already forced)
  const box = new THREE.Box3();
  let any = false;
  for (const { mesh } of asset.meshes) {
    if (!mesh.visible) continue;
    box.expandByObject(mesh);
    any = true;
  }
  if (any) {
    boundsBox.box.copy(box);
    boundsBox.visible = $('t-bounds').checked;
    fitToBox(box);
  } else {
    boundsBox.visible = false;
  }

  // UI: asset info
  const info = $('asset-info');
  info.classList.remove('hidden');
  const texState = data.textures?.state ?? 'SOURCE_UNTEXTURED';
  info.innerHTML =
    `<b>${escapeHtml(data.name)}</b> <span class="v">${data.version}</span><br>` +
    `status <span class="st ${data.status === 'OK' ? '' : 'warn'}">${data.status}</span> · ` +
    `${data.numBlocks} blocks · ${asset.meshes.length} meshes · ` +
    `${asset.meshes.reduce((a, m) => a + (m.tris || 0), 0)} tris<br>` +
    `extent <b>${data.bounds?.maxAxisExtent != null ? data.bounds.maxAxisExtent.toFixed(2) : 'UNKNOWN'}</b> · ` +
    `textures <span class="st ${texState === 'TEXTURED_EXACT' ? '' : 'warn'}">${texState}</span> (${data.textures?.exactSlots ?? 0}/${data.textures?.mapSlots ?? 0} slots)<br>` +
    `anim: kf ${(asset.animData.keyframeControllers || 0)} · textKeys ${(asset.animData.textKeys || []).length} · skins ${skels.length} · ` +
    `morph ${(asset.animData.morphs || []).length} · psys ${(asset.animData.psys || []).length}`;

  // Parts drawer
  $('parts-count').textContent = `${asset.meshes.length} parts`;
  const pl = $('parts-list');
  pl.innerHTML = '';
  for (const m of asset.meshes) {
    const div = document.createElement('div');
    div.className = 'part';
    div.innerHTML = `<input type="checkbox" checked> <span class="pn" title="${escapeHtml(m.name)}">${escapeHtml(m.name || '(unnamed)')}</span> <span class="pv">${m.tris || 0}t</span>`;
    const cb = div.querySelector('input');
    cb.addEventListener('change', () => { m.mesh.visible = cb.checked; });
    pl.appendChild(div);
  }

  buildAnimations(asset, skels);
  applyToggles();
}

// ---------------------------------------------------------------- animations

const mixerState = { mixer: null, clips: [], action: null, playing: false, clock: new THREE.Clock(), duration: 0, clipIndex: -1, loopCycles: 0, lastLoopAt: 0, startedAt: 0 };

function buildAnimations(asset, skels) {
  const anim = asset.animData;
  mixerState.mixer = null;
  mixerState.clips = [];
  mixerState.action = null;
  mixerState.playing = false;
  mixerState.duration = 0;
  mixerState.loopCycles = 0;
  const sel = $('a-clip');
  sel.innerHTML = '';
  const clips = [];

  // keyframe tracks -> AnimationClip
  const kfTracks = [];
  let maxT = 0;
  for (const c of anim.clips || []) {
    const target = asset.nodeByBlock.get(c.targetBlock);
    if (!target) continue;
    const trackName = target.name;
    if (c.quaternion && c.quaternion.times?.length) {
      const t = c.quaternion.times.map((x) => x * (c.frequency ?? 1) + (c.phase ?? 0));
      maxT = Math.max(maxT, ...t);
      kfTracks.push(new THREE.QuaternionKeyframeTrack(trackName + '.quaternion', t, c.quaternion.quats));
    }
    if (c.position && c.position.times?.length) {
      const t = c.position.times.map((x) => x * (c.frequency ?? 1) + (c.phase ?? 0));
      maxT = Math.max(maxT, ...t);
      kfTracks.push(new THREE.VectorKeyframeTrack(trackName + '.position', t, c.position.values));
    }
    if (c.scale && c.scale.times?.length) {
      const t = c.scale.times.map((x) => x * (c.frequency ?? 1) + (c.phase ?? 0));
      maxT = Math.max(maxT, ...t);
      kfTracks.push(new THREE.NumberKeyframeTrack(trackName + '.scale', t, c.scale.values));
    }
  }
  if (kfTracks.length) {
    const clip = new THREE.AnimationClip('keyframes', maxT || 1, kfTracks);
    clips.push({ clip, label: `keyframes (${kfTracks.length} tracks, ${maxT.toFixed(2)}s)` });
  }

  // text keys as marker clip entries (no simulated motion — markers only)
  for (const tk of anim.textKeys || []) {
    clips.push({ clip: null, label: `textkeys: ${tk.keys.map((k) => `${k.time.toFixed(2)} ${k.text}`).join(' | ')}` });
  }
  if ((anim.psys || []).length) {
    clips.push({ clip: null, label: `particle systems: ${(anim.psys || []).length} blocks DETECTION_UNRESOLVED` });
  }
  if ((anim.morphs || []).length) {
    clips.push({ clip: null, label: `morphs: ${(anim.morphs || []).length} regions recorded RAW (era-labelled)` });
  }

  mixerState.clips = clips;
  for (let i = 0; i < clips.length; i++) {
    const o = document.createElement('option');
    o.value = String(i);
    o.textContent = clips[i].label.slice(0, 90);
    sel.appendChild(o);
  }
  const hasPlayable = clips.length > 0 && clips[0].clip != null;
  $('anim').classList.toggle('closed', clips.length === 0);
  sel.value = hasPlayable ? '0' : '';
  if (hasPlayable) {
    mixerState.mixer = new THREE.AnimationMixer(asset.group);
    selectClip(0);
  }
  updateAnimTime();
}

function selectClip(i) {
  const c = mixerState.clips[i];
  if (!c || !c.clip) { stopPlayback(); mixerState.action = null; return; }
  if (!mixerState.mixer) mixerState.mixer = new THREE.AnimationMixer(currentAsset.group);
  if (mixerState.action) mixerState.mixer.uncacheAction(mixerState.action.getClip());
  mixerState.action = mixerState.mixer.clipAction(c.clip);
  mixerState.duration = c.clip.duration;
  mixerState.loopCycles = 0;
  mixerState.lastLoopAt = 0;
  mixerState.action.setLoop($('a-repeat').checked ? THREE.LoopRepeat : THREE.LoopOnce, $('a-repeat').checked ? Infinity : 1);
  updateAnimTime();
}

function playPlayback() {
  if (!mixerState.action) return;
  mixerState.clock.getDelta(); // reset delta accumulation
  mixerState.action.reset();
  mixerState.action.paused = false;
  mixerState.action.play();
  mixerState.playing = true;
  mixerState.startedAt = performance.now();
}
function pausePlayback() {
  if (mixerState.action) mixerState.action.paused = true;
  mixerState.playing = false;
}
function stopPlayback() {
  if (mixerState.action) { mixerState.action.stop(); mixerState.action.paused = false; }
  mixerState.playing = false;
  updateAnimTime();
}
function updateAnimTime() {
  const a = mixerState.action;
  const t = a ? a.time : 0;
  const d = mixerState.duration || 0;
  // drift evidence: completed loop cycles derived from action time (deterministic mixer time)
  if (d > 0 && t >= d) {
    const cycles = Math.floor(t / d);
    if (cycles > mixerState.loopCycles) mixerState.loopCycles = cycles;
  }
  $('a-time').textContent = `${t.toFixed(2)} / ${d.toFixed(2)}${mixerState.loopCycles > 0 ? ` · loops ${mixerState.loopCycles}` : ''}`;
  if (d > 0) $('a-scrub').value = String(Math.round((Math.min(t, d) / d) * 1000));
}

$('a-clip').addEventListener('change', (e) => selectClip(parseInt(e.target.value, 10) || 0));
$('a-play').addEventListener('click', playPlayback);
$('a-pause').addEventListener('click', pausePlayback);
$('a-stop').addEventListener('click', () => { stopPlayback(); });
$('a-repeat').addEventListener('change', (e) => {
  if (mixerState.action) mixerState.action.setLoop(e.target.checked ? THREE.LoopRepeat : THREE.LoopOnce, e.target.checked ? Infinity : 1);
});
$('a-speed').addEventListener('input', (e) => {
  if (mixerState.action) mixerState.action.timeScale = parseFloat(e.target.value) || 1;
});
$('a-scrub').addEventListener('input', (e) => {
  if (!mixerState.action || !mixerState.duration || !mixerState.mixer) return;
  mixerState.playing = false;
  const a = mixerState.action;
  a.paused = false;
  if (!a.isRunning()) a.play();
  // r185 mixer.setTime() ZEROES every action's time and a paused action never
  // re-advances (_effectiveTimeScale=0) — so the scrub seeks the ACTION time
  // directly and applies the pose with a zero-delta mixer update.
  a.time = (parseFloat(e.target.value) / 1000) * mixerState.duration;
  mixerState.mixer.update(0);
  updateAnimTime();
});

// ---------------------------------------------------------------- toggles / fit

function applyToggles() {
  const wire = $('t-wireframe').checked;
  const tex = $('t-textures').checked;
  if (currentAsset) {
    currentAsset.group.traverse((o) => {
      if (o.isMesh) {
        const m = o.material;
        (Array.isArray(m) ? m : [m]).forEach((mm) => {
          mm.wireframe = wire;
          if (mm.userData.texState === 'PARTIAL_CHECKERBOARD') mm.map = tex ? checkerTex : null;
          mm.needsUpdate = true;
        });
      }
    });
  }
  axesGroup.visible = $('t-axes').checked;
  boundsBox.visible = $('t-bounds').checked && !!currentAsset;
}
$('t-wireframe').addEventListener('change', applyToggles);
$('t-textures').addEventListener('change', applyToggles);
$('t-axes').addEventListener('change', applyToggles);
$('t-bounds').addEventListener('change', applyToggles);

function fitToBox(box) {
  const center = box.getCenter(new THREE.Vector3());
  const sphere = box.getBoundingSphere(new THREE.Sphere());
  if (!Number.isFinite(sphere.radius) || sphere.radius <= 0) return;
  const fovRad = (camera.fov * Math.PI) / 180;
  const dist = (sphere.radius / Math.sin(fovRad / 2)) * 1.15;
  const dirV = camera.position.clone().sub(controls.target).normalize();
  if (dirV.lengthSq() < 1e-8) dirV.set(0, 0.5, 1).normalize();
  controls.target.copy(center);
  camera.position.copy(center).addScaledVector(dirV, dist);
  camera.near = Math.max(0.01, sphere.radius / 500);
  camera.far = Math.max(2000, sphere.radius * 50);
  camera.updateProjectionMatrix();
  controls.update();
}
$('btn-fit').addEventListener('click', () => {
  if (!currentAsset) return;
  const box = new THREE.Box3();
  let any = false;
  for (const { mesh } of currentAsset.meshes) {
    if (!mesh.visible) continue;
    box.expandByObject(mesh);
    any = true;
  }
  if (any) fitToBox(box);
});
$('btn-drawer').addEventListener('click', () => {
  $('drawer').classList.toggle('closed');
  setTimeout(resize, 200);
});
$('btn-parts').addEventListener('click', () => $('parts').classList.toggle('closed'));

window.addEventListener('keydown', (e) => {
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT' || e.target.tagName === 'TEXTAREA') return;
  if (e.key === 'c' || e.key === 'C') $('btn-drawer').click();
  if (e.key === 'p' || e.key === 'P') $('btn-parts').click();
  if (e.key === 'f' || e.key === 'F') $('btn-fit').click();
  if (e.key === ' ') { e.preventDefault(); mixerState.playing ? pausePlayback() : playPlayback(); }
});

// ---------------------------------------------------------------- deep links

function hashAsset() {
  const m = location.hash.match(/^#asset\/(\d+)/);
  return m ? parseInt(m[1], 10) : null;
}
window.addEventListener('hashchange', () => {
  const id = hashAsset();
  if (id != null && (!currentAsset || currentAsset.id !== id)) selectAsset(id, false);
});

function escapeHtml(s) {
  return String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

// period requestAnimationFrame time updates for the anim UI
setInterval(() => { if (mixerState.playing || mixerState.action?.paused) updateAnimTime(); }, 120);

// ---------------------------------------------------------------- boot

loadCatalog().then(() => {
  const id = hashAsset();
  if (id != null) selectAsset(id, false);
  else {
    // default: the largest-extent asset (rank 1) — honest demo start
    const first = catalog.entries.find((e) => e.extent != null);
    if (first) selectAsset(first.id, true);
  }
}).catch((e) => {
  $('drawer-stats').textContent = `catalog load failed: ${e.message}`;
});
