// app.js -- PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// THE browser shell (PLAN ?2): one WebGLRenderer, one render loop, two modes
// (ASSET MODE / AUTHORED SCENE MODE), free camera (OrbitControls: orbit /
// pan / zoom), discoverable reset/fit actions (buttons + keys F/R), the
// fail-closed asset load via compat/api.js, the honest diagnostics panel and
// the automation-observable surface window.__pecApp (for the smoke checks).
//
// HONESTY LABELS rendered by this app (never removed):
//   - AUTHOR_PLACED_LAB -- authored laboratory coordinates, NOT historical
//     Eudoria positions (HISTORICAL_WORLD_INSTANCE = NOT_ESTABLISHED;
//     WORLD_XYZ_RECOVERED = NO);
//   - RENDER_ADAPTER_CHOICE / PE_UNITS_NOT_CONFIRMED -- the (x,z,-y) x0.01
//     render conversion applied EXACTLY ONCE at the render-space root;
//   - VIEWER_INSTANCE_WRAPPER_POLICY -- the instance wrapper owns the scene
//     transform; NOT a reproduction of every SDK 2.6 root-replacement branch
//     or the original PE placement mechanism;
//   - the 62+4=66 block accounting and the 9+5 texture binding statuses.

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { SceneIRApi, buildDiagnosticsModel } from './api.js';
import { mountAssetMode } from './asset-mode.js';
import { mountSceneMode, AUTHORING } from './scene-mode.js';
import { RENDER_ADAPTER_CHOICE } from '../src/pecompat/PecRenderConvert.js';

const $ = (id) => document.getElementById(id);
const RUN_ID = 'PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009';

// the QC-observable surface (window.__pecApp) -- the smoke checklist reads it
window.__pecApp = {
  runId: RUN_ID,
  boot: 'pending',
  loadStatus: 'PENDING',
  mode: null,
  modeSwitches: 0,
  selectedBlock: null,
  selectedInstance: null,
  visibleLedger: null,
  wireframe: false,
  instances: {},
  lastApplied: null,
  diagnostics: null,
  fingerprintCheck: null,
  errors: [],
};

const diagRoot = $('diagnostics');
function setLoadStatus(status) {
  window.__pecApp.loadStatus = status;
  diagRoot.dataset.loadStatus = status;
}
function recordError(msg) {
  window.__pecApp.errors.push(String(msg).slice(0, 300));
  $('error-banner').hidden = false;
  $('error-banner').textContent = String(msg).slice(0, 500);
}

function hud(text) { $('hud-line').textContent = text; }

// ---- diagnostics panel (the honest, field-complete record) -------------
function makeDiagnostics(assetBundle, loadTimings, fingerprintCheck) {
  const extras = { loadTimings, fingerprintCheck, errors: [] };
  const model = buildDiagnosticsModel(assetBundle.asset, extras);
  const api = {
    model,
    updateVisibleLedger(ledger) {
      model.meshes.visibleLedger = ledger;
      renderLedgerLine(ledger);
    },
  };
  function renderLedgerLine(ledger) {
    const el = $('diag-meshes');
    el.innerHTML =
      `imported ${model.meshes.imported} / currently visible ${ledger ? ledger.visible : model.meshes.imported}` +
      (ledger && ledger.exclusions?.length ? ` -- excluded ${ledger.exclusions.length} (${ledger.exclusions[0].reason}; full ledger in the panel)` : ' -- none excluded');
  }
  function render() {
    const m = model;
    $('diag-identity').innerHTML =
      `<div>era ${m.assetIdentity.era} | container ${m.assetIdentity.container} | entry ${m.assetIdentity.entryName}</div>` +
      `<div class="mono">payload SHA256 ${m.assetIdentity.payloadSha256}</div>` +
      `<div class="mono">cache key ${m.assetIdentity.cacheKey}</div>` +
      `<div>NIF ${m.assetIdentity.nifVersion} | pin verified: ${m.assetIdentity.pinVerified ? 'YES (fail-closed client check)' : 'NO -- MUST NEVER RENDER'}</div>`;
    $('diag-blocks').innerHTML =
      `blocks ${m.blockAccounting.total} = ${m.blockAccounting.supported} supported + ${m.blockAccounting.partiallyUnderstood} PARTIALLY_UNDERSTOOD + ${m.blockAccounting.opaque} OPAQUE -- ${m.blockAccounting.note}`;
    $('diag-textures').innerHTML =
      `meshes with bound texture NAMES ${m.textureStatus.nameBound} + UNTEXTURED_LABELED ${m.textureStatus.untexturedLabeled} of ${model.meshes.imported} ` +
      `(${m.textureStatus.containerResolution})`;
    const perMesh = m.textureStatus.perMesh.map((p) =>
      `<div class="mono${p.status.startsWith('UNTEXTURED') ? ' untextured' : ''}">[${p.meshBlock}] ${p.meshName}: ${p.status}${p.textureNames.length ? ' -> ' + p.textureNames.join(', ') : ''}</div>`).join('');
    $('diag-textures-per-mesh').innerHTML = perMesh;
    $('diag-transforms').innerHTML =
      `<div>${m.transforms.spaces}</div>` +
      `<div>render conversion: ${RENDER_ADAPTER_CHOICE.axisMap} x${RENDER_ADAPTER_CHOICE.unitScale} -- ${RENDER_ADAPTER_CHOICE.labels.join(' / ')} (applied exactly once at the render-space root)</div>` +
      `<div class="policy">${m.transforms.policyLabels.viewerInstanceWrapper}</div>` +
      `<div class="policy">${m.transforms.policyLabels.authorPlacedLab}</div>`;
    $('diag-timing').innerHTML =
      loadTimings
        ? `server adapter load ${loadTimings.adapterLoadElapsedMs} ms (fail-closed SHA verified) | wire fetch ${loadTimings.fetchBytes} B | client rebuild ${loadTimings.wireBuildMs} ms`
        : '(load timings unavailable)';
    $('diag-fingerprints').innerHTML = fingerprintCheck
      ? `client-side geometry fingerprint re-hash: ${fingerprintCheck.status} -- ${fingerprintCheck.verified}/${model.meshes.imported} mesh vertex+index SHA256 pairs re-verified${fingerprintCheck.elapsedMs != null ? ` in ${fingerprintCheck.elapsedMs} ms` : ''}`
      : '(fingerprint check not run)';
    renderLedgerLine(model.meshes.visibleLedger);
  }
  return { api, model, render };
}

// ---- boot ----------------------------------------------------------------
async function boot() {
  const canvas = $('view-canvas');
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  } catch (e) {
    setLoadStatus('ERROR_WEBGL_RENDERER_UNAVAILABLE');
    recordError(`WebGLRenderer creation failed: ${e.message} -- geometry viewing is impossible in this context; diagnostics remain honest.`);
    hud('ERROR: WebGL renderer unavailable (see the diagnostics panel).');
    window.__pecApp.boot = 'webgl-error';
    return;
  }
  renderer.setPixelRatio(window.devicePixelRatio || 1);
  renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);
  renderer.setClearColor(0x0c1018);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(55, canvas.clientWidth / canvas.clientHeight, 0.1, 2000);
  camera.position.set(0, 30, 70);
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;

  const hemi = new THREE.HemisphereLight(0xbfd4ff, 0x22303f, 1.1);
  const dir = new THREE.DirectionalLight(0xffffff, 0.9);
  dir.position.set(40, 80, 30);
  scene.add(hemi, dir);

  window.addEventListener('resize', () => {
    renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);
    camera.aspect = canvas.clientWidth / canvas.clientHeight;
    camera.updateProjectionMatrix();
  });

  // ---- fail-closed asset load (pin + wire cross-check + fingerprints) ----
  const api = new SceneIRApi();
  let assetBundle;
  try {
    assetBundle = await api.loadAssetIR();
  } catch (e) {
    setLoadStatus(`ERROR_ASSET_LOAD: ${String(e.message).slice(0, 160)}`);
    recordError(`ASSET LOAD FAILED (fail-closed): ${e.message}`);
    $('diag-identity').textContent = 'asset NOT loaded -- pin/wire verification refused the payload';
    hud('ERROR: asset load failed (see diagnostics).');
    window.__pecApp.boot = 'asset-load-error';
    return;
  }
  const { fingerprintCheck, timings } = assetBundle;
  window.__pecApp.fingerprintCheck = { status: fingerprintCheck.status, verified: fingerprintCheck.verified };
  const diagnostics = makeDiagnostics(assetBundle, timings, fingerprintCheck);
  diagnostics.render();
  window.__pecApp.diagnostics = {
    importedMeshes: diagnostics.model.meshes.imported,
    blocks: diagnostics.model.blockAccounting.total,
    supported: diagnostics.model.blockAccounting.supported,
    opaque: diagnostics.model.blockAccounting.partiallyUnderstood + diagnostics.model.blockAccounting.opaque,
    nameBound: diagnostics.model.textureStatus.nameBound,
    untextured: diagnostics.model.textureStatus.untexturedLabeled,
  };
  setLoadStatus('READY');
  window.__pecApp.boot = 'ready';

  // ---- picking (shared by both modes) ------------------------------------
  const raycaster = new THREE.Raycaster();
  const pointer = new THREE.Vector2();
  function pickHandler(ev, meshes, onPick) {
    const rect = renderer.domElement.getBoundingClientRect();
    pointer.x = ((ev.clientX - rect.left) / rect.width) * 2 - 1;
    pointer.y = -((ev.clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(pointer, camera);
    const hits = raycaster.intersectObjects(meshes.filter((m) => m.visible), false);
    if (hits.length > 0) onPick(hits[0].object);
  }

  function fitToObjects(meshes) {
    const box = new THREE.Box3();
    const tmp = new THREE.Box3();
    let any = false;
    for (const mesh of meshes) {
      if (!mesh.visible) continue;
      tmp.setFromObject(mesh);
      box.union(tmp);
      any = true;
    }
    if (!any) return;
    const center = box.getCenter(new THREE.Vector3());
    const sphere = box.getBoundingSphere(new THREE.Sphere());
    const fovRad = (camera.fov * Math.PI) / 180;
    const dist = (sphere.radius / Math.sin(fovRad / 2)) * 1.15;
    const dirV = camera.position.clone().sub(controls.target).normalize();
    if (dirV.lengthSq() < 1e-8) dirV.set(0, 0.5, 1).normalize();
    controls.target.copy(center);
    camera.position.copy(center).addScaledVector(dirV, dist);
    controls.update();
  }
  function resetCamera() {
    controls.target.set(0, 0, 0);
    camera.position.set(0, 30, 70);
    controls.update();
    hud('camera reset (lab default pose)');
  }

  // ---- modes --------------------------------------------------------------
  let activeMode = null;
  // ONE app-level resource cache: the asset's BufferGeometry objects are the
  // SHARED resource (per data block) -- reused across modes and between the two
  // authored instances (resource geometry shared; transforms independent).
  const appGeometryCache = new Map();
  const modeCtx = () => ({
    THREE, scene, canvas, controls, camera,
    asset: assetBundle.asset,
    geometryCache: appGeometryCache,
    ui: {
      inspector: $('inspector-body'), selection: $('selection-body'), ledger: $('ledger-body'),
      instanceList: $('instance-list'),
      instanceButtons: () => document.querySelectorAll('#instance-list .inst-btn'),
      independence: $('independence'),
      inputs: { tx: $('in-tx'), ty: $('in-ty'), tz: $('in-tz'), scale: $('in-scale'), rzDeg: $('in-rz') },
      btnWire: $('btn-wire'), btnDpvs: $('btn-dpvs'),
      btnApplyTrs: $('btn-apply-trs'), btnInstanceReset: $('btn-instance-reset'),
    },
    diagnostics: diagnostics.api,
    hud,
    observable: window.__pecApp,
    pickHandler,
    fitToObjects,
  });

  function switchMode(name) {
    if (activeMode) {
      activeMode.dispose();
      activeMode = null;
    }
    $('inspector-body').innerHTML = '';
    $('selection-body').innerHTML = '';
    $('ledger-body').innerHTML = '';
    const ctx = modeCtx();
    if (name === 'asset') {
      activeMode = mountAssetMode(ctx);
      window.__pecApp.mode = 'asset';
      $('scene-panel').hidden = true;
    } else {
      activeMode = mountSceneMode(ctx);
      window.__pecApp.mode = 'scene';
      $('scene-panel').hidden = false;
    }
    window.__pecApp.modeSwitches++;
    for (const btn of document.querySelectorAll('.mode-btn')) {
      btn.classList.toggle('active', btn.dataset.mode === name);
    }
  }

  $('btn-asset').addEventListener('click', () => switchMode('asset'));
  $('btn-scene').addEventListener('click', () => switchMode('scene'));
  $('btn-fit').addEventListener('click', () => { activeMode?.fitBounds(); hud('camera fit to current visible bounds'); });
  $('btn-reset').addEventListener('click', resetCamera);
  window.addEventListener('keydown', (ev) => {
    if (ev.target && /INPUT|TEXTAREA/.test(ev.target.tagName)) return;
    if (ev.key === 'f' || ev.key === 'F') activeMode?.fitBounds();
    if (ev.key === 'r' || ev.key === 'R') resetCamera();
    if (ev.key === 'w' || ev.key === 'W') $('btn-wire').click();
  });

  // initial mode: asset by default; #scene deep-links the authored scene mode
  // (also used by the headless scene-mount verification + SMOKE_CHECKLIST)
  switchMode(location.hash === '#scene' ? 'scene' : 'asset');

  // ---- the single render loop --------------------------------------------
  const clock = new THREE.Clock();
  (function loop() {
    requestAnimationFrame(loop);
    const dt = clock.getDelta();
    void dt;
    controls.update();
    renderer.render(scene, camera);
  })();

  hud(
    'ASSET MODE -- model 218757 (fail-closed pinned load). [LMB drag] orbit | [RMB drag] pan | [wheel] zoom | [F] fit | [R] reset camera | [W] wireframe');
}

boot().catch((e) => {
  setLoadStatus(`ERROR_BOOT: ${String(e?.message ?? e).slice(0, 160)}`);
  recordError(`BOOT FAILED: ${e?.stack ?? e}`);
  hud('ERROR: boot failed (see the error banner + diagnostics).');
  window.__pecApp.boot = 'error';
});
