// assetlab.js — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010 (contract §7)
// THE ASSET LAB: model inspection with the EXISTING chains (no new loader
// families — the world server serves the PCG witness payload through the
// SAME bounded /api/world/model/<id> route; the CD proxy controls through the
// pinned Models.ark route; the BROWSER parses with the SAME production
// readers: parseWitnessModel (v10.1.0.0) and the bounded phase-3 nif41 reader
// (4.1.0.12, the four CD primaries ONLY).
//
// HONEST STATUS PER WITNESS (§7: "check the actual payload/status; an earlier
// DECODED is not a render proof"):
//   PCG 519316 → parseWitnessModel → per-shape renderables (buildShapeRenderables
//   REUSED from compat/world-vegetation.js) → per-shape texture slots tried IN
//   ORDER through decodeModelTextureStrict (TGA 24/32 + the QUALIFIED DDS
//   DXT1/DXT5 subset) → the FIRST resolvable slot binds (RENDER_RECONSTRUCTION
//   slot choice, labeled); unresolved slots are explicit diagnostics.
//   CD proxies (192374/193207/193313/193684) → readNif41 → geometry in
//   FILE_SCENE space (NO unit conversion, NO axis swap — the catalog-preview
//   convention) with the optional reversible CENTERED display wrapper;
//   SOURCE-UNTEXTURED (established: no UV/texture bindings) → neutral material
//   + the explicit label — NEVER invented bindings, never a random texture.
'use strict';

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { parseWitnessModel } from '/src/pesource/NifModelReader.js';
import {
  buildShapeRenderables, decodeModelTextureStrict,
} from '/compat/world-vegetation.js';

const $ = (id) => document.getElementById(id);
const RUN_ID = 'PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010';

const WITNESSES = [
  { id: 519316, era: 'PCG_9_3_5', label: '519316 — witness PCG (bridge_02)', kind: 'pcg' },
  { id: 192374, era: 'CD_JAN_2003', label: '192374 — proxy CD (kontrola)', kind: 'cd' },
  { id: 193207, era: 'CD_JAN_2003', label: '193207 — proxy CD (kontrola)', kind: 'cd' },
  { id: 193313, era: 'CD_JAN_2003', label: '193313 — proxy CD (kontrola)', kind: 'cd' },
  { id: 193684, era: 'CD_JAN_2003', label: '193684 — proxy CD (kontrola)', kind: 'cd' },
];

const canvas = $('view-canvas');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, logarithmicDepthBuffer: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
renderer.setClearColor(0x1a1a2e); // the 9350 reference background (VIEWER SETTING)
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x1a1a2e);
// the 9350 reference lights (VIEWER SETTINGS — presentation, not a PE claim)
scene.add(new THREE.HemisphereLight(0xb0d0ff, 0x806040, 0.8));
const dir = new THREE.DirectionalLight(0xffffff, 1.2);
dir.position.set(0.35, 1.0, 0.2);
scene.add(dir);
const camera = new THREE.PerspectiveCamera(45, 1, 0.5, 200000); // the live-9350 reference preset
camera.position.set(1, 1, 1);
const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 10;
controls.maxDistance = 50000;

function syncCanvasSize() {
  const w = canvas.clientWidth || 1, h = canvas.clientHeight || 1;
  renderer.setSize(w, h, false);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
}
window.addEventListener('resize', syncCanvasSize);

const state = {
  status: null,
  model: null,          // { group, meshObjects[], kind, era, provenance, slotDiag, displayOffset }
  displayMode: 'FILE_SCENE', // FILE_SCENE (identity) — no unit/axis ops for the CD controls
  witness: null,
  textures: new Map(),  // textureId -> {texture, decoder} (per-lab, disposed on witness change)
  lastChain: null,
};

async function fetchJson(url) {
  const r = await fetch(url, { cache: 'no-store' });
  const t = await r.text();
  let j = null; try { j = JSON.parse(t); } catch { /* none */ }
  if (!r.ok) throw new Error((j && (j.error || j.message)) || `HTTP ${r.status} ${url}`);
  return j;
}

async function fetchBinaryChecked(url, { era, container, containerSha256 }) {
  const r = await fetch(url, { cache: 'no-store' });
  if (!r.ok) {
    const t = await r.text();
    let msg = `HTTP ${r.status}`;
    try { msg = JSON.parse(t).message || msg; } catch { /* raw */ }
    throw new Error(`${url}: ${msg}`);
  }
  const hdr = {
    era: r.headers.get('X-PE-Era'),
    container: r.headers.get('X-PE-Container'),
    containerSha256: r.headers.get('X-PE-Container-Sha256'),
    entryName: r.headers.get('X-PE-Entry'),
    payloadSha256: r.headers.get('X-PE-Payload-Sha256'),
    offset: r.headers.get('X-PE-Offset'),
  };
  if (hdr.era !== era || hdr.container !== container ||
      String(hdr.containerSha256 ?? '').toUpperCase() !== String(containerSha256 ?? '').toUpperCase()) {
    throw new Error(`${url}: tożsamość kontenera nie zgadza się z żądaniem (era/kontener/SHA) — kontrolowana odmowa`);
  }
  const payload = new Uint8Array(await r.arrayBuffer());
  return { payload, headers: hdr };
}

function disposeWitness() {
  if (!state.model) return;
  for (const m of state.model.meshObjects) {
    m.geometry.dispose();
    if (m.material) m.material.dispose();
  }
  scene.remove(state.model.group);
  for (const [, t] of state.textures) t.texture.dispose();
  state.textures.clear();
  state.model = null;
}

/** The PCG witness chain — REUSED from the world-vegetation production
 *  modules (no second importer; per-slot honest diagnostics). */
async function loadPcgWitness(id) {
  const s = state.status;
  const { payload, headers } = await fetchBinaryChecked(`/api/world/model/${id}`, {
    era: 'PCG_9_3_5', container: 'Models.bnt',
    containerSha256: s?.containers?.models?.sha256 ?? '',
  });
  const { extraction } = parseWitnessModel(payload, headers.entryName ?? `${id}.nif`);
  const { renderables, nonVisual } = buildShapeRenderables(extraction, id);
  const group = new THREE.Group();
  const meshObjects = [];
  const slotDiag = [];
  let texturedShapes = 0, untexturedShapes = 0;
  for (const r of renderables) {
    let chosen = null;
    for (const slot of r.textureSlots) {
      let cached = state.textures.get(slot.textureId);
      if (!cached) {
        try {
          const texRes = await fetchBinaryChecked(`/api/world/texture/${slot.textureId}`, {
            era: 'PCG_9_3_5', container: 'Textures.bnt',
            containerSha256: s?.containers?.textures?.sha256 ?? '',
          });
          const dec = decodeModelTextureStrict(texRes.payload);
          const texture = new THREE.DataTexture(dec.rgba, dec.width, dec.height, THREE.RGBAFormat);
          texture.colorSpace = THREE.NoColorSpace;
          texture.flipY = false;
          texture.wrapS = THREE.RepeatWrapping;
          texture.wrapT = THREE.RepeatWrapping;
          texture.minFilter = THREE.LinearFilter;
          texture.magFilter = THREE.LinearFilter;
          texture.needsUpdate = true;
          cached = { texture, decoder: dec.decoder, bpp: dec.bpp };
          state.textures.set(slot.textureId, cached);
        } catch (e) {
          slotDiag.push({ textureId: slot.textureId, slotName: slot.name, reason: String(e?.message ?? e).slice(0, 220) });
          continue;
        }
      }
      chosen = { slot, cached };
      break; // the FIRST resolvable slot binds (RENDER_RECONSTRUCTION slot choice — labeled)
    }
    const material = new THREE.MeshBasicMaterial({
      map: chosen ? chosen.cached.texture : null,
      vertexColors: r.hasVertexColors,
      transparent: r.alpha ? (r.alpha.flags & 1) === 1 : false,
      alphaTest: r.alpha ? r.alpha.threshold / 255.0 : 0,
      side: THREE.DoubleSide,
      color: chosen ? 0xffffff : 0x8a8f96, // untextured: neutral gray + the diagnostic (never a fake texture)
    });
    const mesh = new THREE.Mesh(r.geometry, material);
    mesh.userData = { shapeName: r.shapeName, textureId: chosen?.slot.textureId ?? null, slotName: chosen?.slot.name ?? null, decoder: chosen?.cached.decoder ?? null };
    group.add(mesh);
    meshObjects.push(mesh);
    if (chosen) texturedShapes++; else untexturedShapes++;
  }
  scene.add(group);
  state.model = {
    group, meshObjects, kind: 'pcg', era: 'PCG_9_3_5',
    provenance: {
      era: 'PCG_9_3_5',
      container: 'Models.bnt', containerSha256: s?.containers?.models?.sha256,
      entry: headers.entryName ?? `${id}.nif`, payloadSha256: headers.payloadSha256,
      decoder: 'parseWitnessModel (NifModelReader v10.1.0.0 — the production qualified importer)',
    },
    slotDiag, texturedShapes, untexturedShapes, nonVisual,
    nifVersion: extraction.header.versionString,
    displayOffset: null, // the PCG chain bakes [P-UNITS]/[P-AXIS] in geometry (documented bridges)
  };
  state.lastChain = {
    steps: [
      `1. GET /api/world/model/${id} — bounded ORIGINAL payload from the pinned PCG_9_3_5 Models.bnt (entry ${headers.entryName ?? id + '.nif'}; payload SHA ${headers.payloadSha256?.slice(0, 16)}…)`,
      `2. parseWitnessModel — NifModelReader v10.1.0.0 (production; ${extraction.blocks.length} blocks; LOUD refusals)`,
      `3. per-shape: NiTriShape → NiTexturingProperty (properties refs) → NiArkTextureExtraData entries → texture slots IN ORDER`,
      `4. per-slot: GET /api/world/texture/<id> (pinned PCG_9_3_5 Textures.bnt) → decodeModelTextureStrict (TGA2 24bpp / A32 32bpp / DDS DXT1+DXT5 — the QUALIFIED same-era subset)`,
      `5. GPU: DataTexture + MeshBasicMaterial (DoubleSide; alpha from NiAlphaProperty; [P-UNITS] cm→m ×0.01 ONCE; [P-AXIS] (x,z,-y); [P-UV] raw v, flipY=false)`,
    ],
  };
}

/** The CD proxy controls — the SERVER-parsed WIRE (the catalog pattern: the
 *  bounded nif41 reader runs server-side; the browser renders the wire) in
 *  FILE_SCENE geometry, SOURCE-UNTEXTURED (established; no invented
 *  bindings). */
async function loadCdProxy(id) {
  const s = state.status;
  const wire = await (async () => {
    const r = await fetch(`/api/world/asset/cd/${id}/wire`, { cache: 'no-store' });
    if (!r.ok) {
      const t = await r.text();
      let msg = `HTTP ${r.status}`;
      try { msg = JSON.parse(t).message || msg; } catch { /* raw */ }
      throw new Error(msg);
    }
    return r.json();
  })();
  if (!wire?.ok || !Array.isArray(wire.shapes)) throw new Error('the served CD wire is not ok');
  const group = new THREE.Group();
  const meshObjects = [];
  const bounds = new THREE.Box3();
  for (const sh of wire.shapes) {
    if (!sh.positions?.length || !sh.indices?.length) continue;
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(new Float32Array(sh.positions), 3)); // FILE_SCENE — NO unit/axis ops
    if (sh.normals?.length) geometry.setAttribute('normal', new THREE.BufferAttribute(new Float32Array(sh.normals), 3));
    if (sh.uv0?.length) geometry.setAttribute('uv', new THREE.BufferAttribute(new Float32Array(sh.uv0), 2));
    geometry.setIndex(new THREE.BufferAttribute(new Uint16Array(sh.indices), 1));
    if (!sh.normals?.length) geometry.computeVertexNormals();
    geometry.computeBoundingBox();
    bounds.union(geometry.boundingBox);
    // SOURCE-UNTEXTURED (established for these proxies): the explicit neutral
    // material — never invented bindings, never a random texture
    const material = new THREE.MeshBasicMaterial({ color: 0x9aa3ad, side: THREE.DoubleSide });
    const mesh = new THREE.Mesh(geometry, material);
    mesh.userData = { shapeName: sh.shapeName, sourceUntextured: true };
    group.add(mesh);
    meshObjects.push(mesh);
  }
  // the CENTERED display wrapper (reversible, shown): the camera convenience ONLY
  let displayOffset = new THREE.Vector3();
  if (!bounds.isEmpty()) {
    const center = new THREE.Vector3();
    bounds.getCenter(center);
    displayOffset = center.clone().negate();
    group.position.copy(displayOffset); // display wrapper; file-space mapping: file = display - offset (reversible)
  }
  scene.add(group);
  state.model = {
    group, meshObjects, kind: 'cd', era: 'CD_JAN_2003',
    provenance: {
      era: 'CD_JAN_2003',
      container: 'Models.ark', containerSha256: wire.provenance?.containerSha256,
      entry: wire.provenance?.entry ?? `${id}.nif`, payloadSha256: wire.provenance?.payloadSha256,
      decoder: `${wire.readerVersion} (bounded NIF 4.1.0.12 — the four CD primaries ONLY; SERVER-side parse — the catalog wire pattern)`,
    },
    slotDiag: [], texturedShapes: 0, untexturedShapes: meshObjects.length, nonVisual: [],
    nifVersion: wire.nifVersion,
    wireCensus: { shapes: wire.shapes.length, triangles: wire.triangles, vertices: wire.vertices, blockCensus: wire.blockCensus, closure: wire.closure },
    displayOffset: bounds.isEmpty() ? null : { x: displayOffset.x, y: displayOffset.y, z: displayOffset.z },
  };
  state.lastChain = {
    steps: [
      `1. GET /api/world/asset/cd/${id}/wire — the SERVER-parsed wire of the PINNED CD_JAN_2003 Models.ark payload (entry ${wire.provenance?.entry}; payload SHA ${String(wire.provenance?.payloadSha256 ?? '').slice(0, 16)}…)`,
      `2. ${wire.readerVersion} — bounded 4.1.0.12, closure EXACT (blocks ${JSON.stringify(wire.blockCensus)}); the parse runs SERVER-SIDE (the reader imports node:fs — never a client module)`,
      `3. per-shape geometry in FILE_SCENE space (NO unit conversion, NO axis swap — the catalog-preview convention)`,
      `4. material: the EXPLICIT neutral MeshBasicMaterial — SOURCE-UNTEXTURED (established: no UV/texture bindings in the examined payloads; NEVER invented bindings)`,
      `5. display wrapper: CENTERED offset ${JSON.stringify(state.model.displayOffset)} (reversible: file = display − offset; original vertices untouched)`,
    ],
  };
}

/** The 9350-reference fit: AABB center, distance = maxDim × 1.8, direction
 *  (0.7, 0.6, 0.7) — the same corrected orbit model as the world view. */
function fitView() {
  if (!state.model) return;
  const box = new THREE.Box3();
  for (const m of state.model.meshObjects) {
    m.geometry.computeBoundingBox();
    const b = m.geometry.boundingBox.clone().applyMatrix4(m.matrixWorld);
    box.union(b);
  }
  if (box.isEmpty()) return;
  const center = new THREE.Vector3();
  const size = new THREE.Vector3();
  box.getCenter(center);
  box.getSize(size);
  const maxDim = Math.max(size.x, size.y, size.z) || 1;
  const dist = maxDim * 1.8;
  const dirV = new THREE.Vector3(0.7, 0.6, 0.7).normalize();
  controls.target.set(center.x, center.y, center.z);
  camera.position.set(center.x + dirV.x * dist, center.y + dirV.y * dist, center.z + dirV.z * dist);
  controls.update();
}

async function selectWitness(w) {
  disposeWitness();
  state.witness = w;
  $('witness-status').textContent = `ładowanie ${w.label}…`;
  try {
    if (w.kind === 'pcg') await loadPcgWitness(w.id);
    else await loadCdProxy(w.id);
    fitView();
    const m = state.model;
    const status = m.kind === 'pcg'
      ? `WITNESS PCG ${w.id}: NIF ${m.nifVersion}; kształty wizualne ${m.meshObjects.length} (teksturowane ${m.texturedShapes}, bez tekstur ${m.untexturedShapes}); nie-wizualne ${m.nonVisual.length}\n` +
        `era ${m.provenance.era} | kontener ${m.provenance.container} SHA ${String(m.provenance.containerSha256 ?? '').slice(0, 16)}… | wpis ${m.provenance.entry} | payload SHA ${String(m.provenance.payloadSha256 ?? '').slice(0, 16)}…\n` +
        `sloty pominięte (jawne): ${m.slotDiag.length}`
      : `PROXY CD ${w.id} (KONTROLA): NIF ${m.nifVersion}; kształty ${m.meshObjects.length}; SOURCE-UNTEXTURED (ustalone: brak UV/texture bindings w zbadanych payloadach) — neutralny materiał, NIGDY wymyślone bindingi\n` +
        `era ${m.provenance.era} (ODRĘBNA od PCG_9_3_5) | kontener ${m.provenance.container} SHA ${String(m.provenance.containerSha256 ?? '').slice(0, 16)}… | wpis ${m.provenance.entry} | payload SHA ${String(m.provenance.payloadSha256 ?? '').slice(0, 16)}…`;
    $('witness-status').textContent = status;
    $('witness-chain').textContent = state.lastChain.steps.join('\n');
    $('slot-diag').textContent = m.slotDiag.length
      ? m.slotDiag.map((d) => `slot ${d.slotName} → tekstura ${d.textureId}: ${d.reason}`).join('\n')
      : (m.kind === 'pcg' ? '— (wszystkie sloty rozwiązane przez strict decoder)' : '— (proxy CD: source-untextured — brak bindingów w źródle, nic nie pominięto po cichu)');
    $('cam-note').textContent = m.kind === 'cd'
      ? `wyświetlanie: FILE_SCENE (bez konwersji jednostek i osi) + odwracalny CENTERED offset ${JSON.stringify(m.displayOffset)} — oryginalne wierzchołki nietknięte; kamera FOV 45, damping 0.08, min 10, max 50000, far 200000 (referencja 9350)`
      : `wyświetlanie: mostki udokumentowane łańcucha roślinności ([P-UNITS] ×0.01 RAZ; [P-AXIS] (x,z,-y); [P-UV] raw v); kamera FOV 45, damping 0.08, min 10, max 50000, far 200000 (referencja 9350)`;
    $('hud-line').textContent = `Asset Lab: ${w.label} — ${m.meshObjects.length} kształtów; F dopasuj; orbita LMB/RMB/MMB`;
  } catch (e) {
    $('witness-status').textContent = `BŁĄD (uczciwie): ${e?.message ?? e}\n— żaden model nie jest pokazany dla tego witnessa; wybierz inny witness.`;
    $('error-banner').hidden = false;
    $('error-banner').textContent = `Asset Lab: ${w.label}: ${e?.message ?? e}`;
  }
}

function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
  if (state.model && !animate._shown) {
    animate._shown = true;
  }
}

async function boot() {
  $('error-banner').hidden = true;
  syncCanvasSize();
  const sel = $('witness-select');
  for (const w of WITNESSES) {
    const opt = document.createElement('option');
    opt.value = String(w.id);
    opt.textContent = w.label;
    sel.appendChild(opt);
  }
  sel.addEventListener('change', () => {
    const w = WITNESSES.find((x) => String(x.id) === sel.value);
    if (w) void selectWitness(w);
  });
  $('btn-fit').addEventListener('click', fitView);
  $('btn-launcher').addEventListener('click', () => { location.href = '/launcher'; });
  $('btn-world').addEventListener('click', () => { location.href = '/compat/world.html'; });
  $('btn-drawer').addEventListener('click', () => {
    const el = $('world-side');
    const open = el.getAttribute('data-open') === 'true';
    el.setAttribute('data-open', open ? 'false' : 'true');
    syncCanvasSize();
  });
  $('btn-drawer-close').addEventListener('click', () => {
    $('world-side').setAttribute('data-open', 'false');
    syncCanvasSize();
  });
  $('world-side').setAttribute('data-open', 'true'); // the lab starts with the details visible
  window.addEventListener('keydown', (ev) => {
    const t = ev.target;
    if (t instanceof HTMLElement && (t.tagName === 'INPUT' || t.tagName === 'SELECT' || t.tagName === 'TEXTAREA')) return;
    if (ev.code === 'KeyF') fitView();
  });
  try {
    state.status = await fetchJson('/api/world/status');
  } catch (e) {
    $('hud-line').textContent = `brak statusu serwera: ${e?.message ?? e}`;
  }
  // the pinned default: the PCG witness 519316 (contract: start from 519316)
  await selectWitness(WITNESSES[0]);
  animate();
}

boot().catch((e) => {
  $('error-banner').hidden = false;
  $('error-banner').textContent = `Asset Lab boot: ${e?.message ?? e}`;
});
