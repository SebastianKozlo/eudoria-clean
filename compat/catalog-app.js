// catalog-app.js — PE_CITY_ASSET_MAP_R1_20261010, phase 4 (contract §5)
// THE /catalog browser app: the era-separated catalog table (full index
// catalogs of BOTH eras, paged through /api/catalog/rows), sorting per metric
// (measured largest->smallest; UNKNOWN always LAST — never 0), era/status
// filters, ID/name search across both eras, and the bounded PREVIEW for the
// four pinned CD_2003 primaries (the only entries with an established safe
// import — everything else shows its honest CATALOG_ONLY / VERSION_GATED /
// FAILED / DECODED state; no fake previews).
//
// REUSE LABEL: the boot/diagnostics/observable patterns follow the SceneIR
// app (compat/app.js) — one WebGLRenderer, one render loop, OrbitControls,
// the fail-closed load discipline, window.__pecApp-style observable surface
// (here: window.__pecCatalog). The preview itself is compat/catalog-preview.js.
//
// HONESTY: the app NEVER downloads the containers — the only data paths are
// the bounded /api/catalog/* endpoints. Client-side pin check: the preview
// wire must match the pinned four-primary identity (era+container+entry+
// payload SHA) — a mismatch refuses the render loudly.

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import {
  mountCatalogPreview, verifyWireClientSide, PREVIEW_VIEW_MODES,
} from './catalog-preview.js';
import {
  rowsTableHtml, coverageBoxHtml, escapeHtml, UNKNOWN_BADGE,
} from './catalog-table.js';

const $ = (id) => document.getElementById(id);
const RUN_ID = 'PE_CITY_ASSET_MAP_R1_20261010';
const PHASE = 'CATALOG_MODE (phase 4, contract §5)';

// the four pinned primaries (fail-closed client-side pins — same discipline
// as compat/api.js CLIENT_PIN; the pins travel in the app source, not the wire)
export const CATALOG_CLIENT_PINS = Object.freeze({
  containerSha256: 'f660d055b4b9471b3b6e16b07f5368dbd6f2208dab6b51bb9bdb9942bd73ea62',
  models: {
    '192374': '08d80c67bb87caf6a1c00bf8c034e329484e25a6a588da411079bb6f682de8c1',
    '193207': '220f549b311563a1a6506cacefcebb8911ee4770cf72b85f2f635146c111adbb',
    '193313': '02fc860a840e9cdb948f04daff2691bb37baf9e0da8dbadc8f77773c517beef2',
    '193684': '4cc5f9203280c26fc2020bb6c432e2bcf4e5db4ec2f47be3df573e537660901f',
  },
});

window.__pecCatalog = {
  runId: RUN_ID,
  boot: 'pending',
  loadStatus: 'PENDING',
  rowsLoaded: 0,
  coverage: null,
  sortMetric: 'size',
  era: 'ALL',
  status: 'ALL',
  q: '',
  page: 1,
  pageCount: 1,
  selectedModel: null,
  previewState: null,
  fingerprintCheck: null,
  errors: [],
};

const diagRoot = $('diagnostics');
function setLoadStatus(status) {
  window.__pecCatalog.loadStatus = status;
  diagRoot.dataset.loadStatus = status;
}
function recordError(msg) {
  window.__pecCatalog.errors.push(String(msg).slice(0, 300));
  const b = $('error-banner');
  b.hidden = false;
  b.textContent = String(msg).slice(0, 500);
}
function hud(text) { $('hud-line').textContent = text; }

// ---------------------------------------------------------------------------
// boot
// ---------------------------------------------------------------------------
async function boot() {
  const canvas = $('view-canvas');
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  } catch (e) {
    setLoadStatus('ERROR_WEBGL_RENDERER_UNAVAILABLE');
    recordError(`WebGLRenderer creation failed: ${e.message} — geometry preview is impossible in this context; the catalog table + diagnostics remain honest.`);
    hud('ERROR: WebGL renderer unavailable (see the diagnostics panel).');
    window.__pecCatalog.boot = 'webgl-error';
    await loadCatalogDataOnly();
    return;
  }
  renderer.setPixelRatio(window.devicePixelRatio || 1);
  renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);
  renderer.setClearColor(0x0c1018);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(55, canvas.clientWidth / canvas.clientHeight, 0.1, 500000);
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

  const appGeometryCache = new Map();
  let activePreview = null;

  const ui = {
    diagCatalog: $('diag-catalog'),
    diagPreviewIdentity: $('diag-preview-identity'),
    diagBounds: $('diag-bounds'),
    diagTexture: $('diag-texture'),
    diagMaterials: $('diag-materials'),
    diagWrapper: $('diag-wrapper'),
    diagLayout: $('diag-layout'),
    diagTiming: $('diag-timing'),
    hierarchyTree: $('hierarchy-tree'),
    btnFit: $('btn-fit'), btnReset: $('btn-reset'),
    btnOrigcoords: $('btn-origcoords'), btnWire: $('btn-wire'),
  };

  function renderLayoutDiagnostics() {
    // honest measured layout + camera state (also the debugging record for the
    // pixel-render verification: proves WHAT the canvas actually sees)
    const rect = canvas.getBoundingClientRect();
    ui.diagLayout.innerHTML =
      `<div>canvas css ${canvas.clientWidth}x${canvas.clientHeight} px @(${Math.round(rect.left)},${Math.round(rect.top)}); buffer ${renderer.domElement.width}x${renderer.domElement.height}</div>` +
      `<div>camera pos (${camera.position.toArray().map((v) => v.toFixed(1)).join(', ')}) target (${controls.target.toArray().map((v) => v.toFixed(1)).join(', ')}) fov ${camera.fov} near ${camera.near} far ${camera.far}</div>` +
      `<div>viewport ${window.innerWidth}x${window.innerHeight}px; document scrollH ${document.documentElement.scrollHeight}</div>` +
      (activePreview
        ? `<div>preview meshes ${activePreview.meshObjects.length}, visible ${activePreview.meshObjects.filter((m) => m.visible).length}; view mode ${activePreview.state.viewMode}; wrapper offset [${activePreview.state.wrapperOffset.map((v) => v.toFixed(1)).join(', ')}]</div>`
        : '');
  }

  function resetCamera() {
    controls.target.set(0, 0, 0);
    camera.position.set(0, 30, 70);
    controls.update();
    hud('camera reset (lab default pose)');
  }

  async function closePreview() {
    if (activePreview) { activePreview.dispose(); activePreview = null; }
    $('preview-title').textContent = 'no model selected — click a PREVIEWABLE row (the four CD_2003 primaries) to open the preview';
    window.__pecCatalog.selectedModel = null;
    window.__pecCatalog.previewState = null;
  }

  async function openPreview(id) {
    const t0 = Date.now();
    setLoadStatus('LOADING');
    $('preview-title').textContent = `loading preview CD_2003 ${id}.nif …`;
    let res;
    try {
      res = await fetch(`/api/catalog/model/CD_2003/${id}`);
    } catch (e) {
      setLoadStatus('ERROR_PREVIEW_FETCH');
      recordError(`preview fetch failed: ${e.message}`);
      return;
    }
    if (!res.ok) {
      setLoadStatus('ERROR_PREVIEW_FETCH');
      let body = '';
      try { body = JSON.stringify(await res.json()).slice(0, 400); } catch { /* non-JSON */ }
      recordError(`preview refused for ${id}: HTTP ${res.status} ${body}`);
      $('preview-title').textContent = `preview refused for CD_2003 ${id}.nif — honest state (see the error banner; CATALOG_ONLY/VERSION_GATED are never faked)`;
      return;
    }
    const wire = await res.json();
    // ---- fail-closed client-side pin check ----
    const pinSha = CATALOG_CLIENT_PINS.models[id];
    if (!pinSha || wire.provenance.payloadSha256 !== pinSha ||
        wire.provenance.containerSha256 !== CATALOG_CLIENT_PINS.containerSha256 ||
        wire.pins.modelId !== Number(id)) {
      setLoadStatus('ERROR_PIN_MISMATCH');
      recordError(`PREVIEW PIN MISMATCH for ${id} — served wire identity does not match the pinned four-primary identity; refusing to render (fail-closed).`);
      return;
    }
    // ---- client-side wire verification (composition cross-check + fingerprints) ----
    const verification = await verifyWireClientSide(wire);
    window.__pecCatalog.fingerprintCheck = {
      status: verification.fingerprintCheck.status,
      verified: verification.fingerprintCheck.verified,
    };
    if (!verification.ok) {
      setLoadStatus('ERROR_WIRE_VERIFICATION');
      recordError(`preview wire verification FAILED: ${verification.problems.join(' | ')}`);
      return;
    }
    await closePreview();
    activePreview = mountCatalogPreview({
      THREE, scene, canvas, controls, camera, wire,
      geometryCache: appGeometryCache,
      ui: { btnOrigcoords: ui.btnOrigcoords, diagWrapper: ui.diagWrapper },
      hud, observable: window.__pecCatalog, pickHandler,
    });    window.__pecCatalog.selectedModel = Number(id);
    window.__pecCatalog.previewState = activePreview.state;
    const sb = wire.sceneBounds_FILE_SCENE_SPACE;
    $('preview-title').innerHTML =
      `preview: <b>CD_2003 ${id}.nif</b> — DECODED_FULL_CLOSURE; UNTEXTURED_PROXY_MESH (material preview only; no fake textures)` +
      ` | ${wire.meshRows.length} meshes | ${activePreview.materialApplications.length} materials applied`;
    // diagnostics: identity
    ui.diagPreviewIdentity.innerHTML =
      `<div>era ${wire.provenance.era} | container ${wire.provenance.container} | entry ${wire.provenance.entryName}</div>` +
      `<div class="mono">payload SHA256 ${wire.provenance.payloadSha256}</div>` +
      `<div class="mono">container SHA256 ${wire.provenance.containerSha256}</div>` +
      `<div>NIF ${wire.asset.nifVersion} | blocks ${wire.asset.numBlocks} (${wire.decodeCensus.SUPPORTED} SUPPORTED + ${wire.decodeCensus.PARTIALLY_UNDERSTOOD} PARTIALLY_UNDERSTOOD + ${wire.decodeCensus.OPAQUE} OPAQUE) | pin verified: YES (fail-closed client check)</div>` +
      `<div>client wire verification: ${verification.ok ? 'PASS' : 'FAIL'} (world-transform composition cross-check + bounds cross-check; geometry fingerprints ${verification.fingerprintCheck.status}: ${verification.fingerprintCheck.verified}/${wire.meshRows.length} verified)</div>`;
    // diagnostics: bounds/origin (FILE_SCENE_SPACE, original units)
    const fx = (v) => v.toLocaleString('en-US', { maximumFractionDigits: 2 });
    ui.diagBounds.innerHTML =
      `<div>min [${sb.min.map(fx).join(', ')}] max [${sb.max.map(fx).join(', ')}]</div>` +
      `<div>extents [${sb.extents.map(fx).join(', ')}] | maxAxisExtent ${fx(sb.maxAxisExtent)} | footprintX ${fx(sb.footprintX)} footprintZ ${fx(sb.footprintZ)}</div>` +
      `<div>space FILE_SCENE_SPACE | units ORIGINAL file units (unit semantics NOT established — never meters)</div>` +
      `<div class="policy">SOURCE_FILE_SCENE_SPACE ≠ WORLD_PLACEMENT (HISTORICAL_PLACEMENT = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO)</div>` +
      `<div>placement finding: ${wire.placementFinding.finding} (layout stored in vertex coordinates; every local TRS identity — measured)</div>`;
    // diagnostics: UV/texture
    const td = wire.textureDiagnostics;
    ui.diagTexture.innerHTML =
      `<div><b>${td.disposition}</b> — ${td.numTexturingProperties} NiTexturingProperty, ${td.numSourceTextures} NiSourceTexture, ArkTexture numTex=${td.arkTextureNumTex}, ${td.uvSets} UV sets total (per mesh: ${td.perMesh.map((m) => `${m.shapeName}:0`).join(', ')})</div>` +
      `<div>${escapeHtml(td.note)}</div>`;
    // diagnostics: materials (measured applications)
    ui.diagMaterials.innerHTML = activePreview.materialApplications.map((m) =>
      `<div class="mono">[${m.shapeBlock}] ${escapeHtml(m.shapeName)} -> NiMaterialProperty#${m.materialBlock} (${escapeHtml(m.materialName ?? 'unnamed')}) diffuse [${m.diffuse.map((v) => v.toFixed(3)).join(', ')}] ${m.referenceClass} — APPLIED (material preview)</div>`).join('\n');
    // hierarchy tree with per-shape visibility (part isolation)
    const tree = ['<div>Scene Root (block ' + wire.roots[0] + ') — original hierarchy</div>'];
    for (const h of wire.hierarchyRows) {
      if (h.block === wire.roots[0]) continue;
      const isShape = h.type === 'NiTriShape';
      const cls = isShape ? 'tree-shape' : 'tree-node';
      const toggle = isShape
        ? ` <label><input type="checkbox" data-shape="${h.block}" checked> visible</label>`
        : '';
      tree.push(`<div class="${cls}">[${h.block}] ${escapeHtml(h.type)} "${escapeHtml(h.name ?? '')}"${toggle}</div>`);
    }
    ui.hierarchyTree.innerHTML = tree.join('\n');
    for (const cb of ui.hierarchyTree.querySelectorAll('input[data-shape]')) {
      cb.addEventListener('change', () => {
        activePreview.setPartVisible(Number(cb.dataset.shape), cb.checked);
        hud(`part isolation: shape block ${cb.dataset.shape} ${cb.checked ? 'VISIBLE' : 'HIDDEN'}`);
      });
    }
    ui.diagTiming.innerHTML = `preview wire fetch ${Date.now() - t0} ms | ${wire.blocks.length} blocks | cacheKey ${wire.cacheKey.slice(0, 60)}…`;
    activePreview.renderWrapperDiagnostics();
    activePreview.fitToBounds();
    renderLayoutDiagnostics();
    setLoadStatus('READY');
    hud(`PREVIEW — CD_2003 ${id}.nif (DECODED_FULL_CLOSURE; UNTEXTURED_PROXY_MESH). [LMB] orbit | [RMB] pan | [wheel] zoom | [F] fit | [C] original-coords view | [W] wireframe`);
  }

  // ---- table wiring ----
  const state = { era: 'ALL', status: 'ALL', sort: 'size', q: '', page: 1, pageSize: 100 };
  async function loadRows() {
    const t0 = Date.now();
    const params = new URLSearchParams({
      era: state.era, status: state.status, sort: state.sort, q: state.q,
      page: String(state.page), pageSize: String(state.pageSize),
    });
    let data;
    try {
      const res = await fetch(`/api/catalog/rows?${params.toString()}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      data = await res.json();
    } catch (e) {
      recordError(`catalog rows load failed: ${e.message}`);
      setLoadStatus('ERROR_ROWS_LOAD');
      return;
    }
    window.__pecCatalog.rowsLoaded = data.rows.length;
    window.__pecCatalog.coverage = data.coverage;
    window.__pecCatalog.page = data.page;
    window.__pecCatalog.pageCount = data.pageCount;
    $('catalog-tbody').innerHTML = rowsTableHtml(data.rows, {
      selectedId: window.__pecCatalog.selectedModel,
    });
    $('ctl-page').textContent = `page ${data.page} / ${data.pageCount} (${data.total} rows match)`;
    const cov = data.coverage;
    $('catalog-coverage').innerHTML = coverageBoxHtml(cov, {
      overlapCount: window.__pecCatalog.statusInfo?.overlapSameNameBothEras?.count ?? null,
    });
    $('catalog-sort-rule').innerHTML = `<span class="unknown-badge">${UNKNOWN_BADGE}</span> ${escapeHtml(data.sortRule)}`;
    for (const tr of $('catalog-tbody').querySelectorAll('tr')) {
      tr.addEventListener('click', () => {
        const id = tr.dataset.id;
        const era = tr.dataset.era;
        if (era === 'CD_2003' && id && CATALOG_CLIENT_PINS.models[id]) {
          history.replaceState(null, '', `#model=${id}`);
          openPreview(id);
        } else {
          hud(`CD_2003/PCG_9_3_5 ${tr.dataset.entry}: CATALOG row — no safe import established for a preview in this run (honest state; nothing faked)`);
        }
      });
    }
    const elapsed = Date.now() - t0;
    ui.diagCatalog.innerHTML =
      `<div>rows API: ${data.rows.length} rendered of ${data.total} matching (page ${data.page}/${data.pageCount}, ${elapsed} ms)</div>` +
      `<div>filters: era=${state.era} status=${state.status} sort=${state.sort} q="${escapeHtml(state.q)}"</div>`;
  }

  async function loadCatalogDataOnly() {
    try { await loadRows(); } catch (e) { recordError(String(e)); }
    setLoadStatus('READY'); // table READY even without WebGL (preview impossible, honestly labeled)
    window.__pecCatalog.boot = 'ready-no-webgl';
  }

  // status fetch + table load + READY
  try {
    const st = await (await fetch('/api/catalog/status')).json();
    window.__pecCatalog.statusInfo = st;
    $('catalog-coverage').innerHTML = 'coverage: loaded from /api/catalog/status — see table header box';
  } catch (e) {
    recordError(`catalog status fetch failed: ${e.message}`);
  }
  await loadRows();
  setLoadStatus('READY');
  window.__pecCatalog.boot = 'ready';

  // ---- controls ----
  $('ctl-era').addEventListener('change', (ev) => { state.era = ev.target.value; state.page = 1; loadRows(); });
  $('ctl-status').addEventListener('change', (ev) => { state.status = ev.target.value; state.page = 1; loadRows(); });
  $('ctl-sort').addEventListener('change', (ev) => { state.sort = ev.target.value; state.page = 1; loadRows(); });
  let qTimer = null;
  $('ctl-q').addEventListener('input', (ev) => {
    clearTimeout(qTimer);
    qTimer = setTimeout(() => { state.q = ev.target.value; state.page = 1; loadRows(); }, 250);
  });
  $('ctl-prev').addEventListener('click', () => { if (state.page > 1) { state.page--; loadRows(); } });
  $('ctl-next').addEventListener('click', () => { if (state.page < window.__pecCatalog.pageCount) { state.page++; loadRows(); } });

  $('btn-fit').addEventListener('click', () => { activePreview?.fitToBounds(); hud('camera fit to current visible bounds'); });
  $('btn-reset').addEventListener('click', resetCamera);
  ui.btnOrigcoords.addEventListener('click', () => {
    if (!activePreview) return;
    activePreview.setViewMode(activePreview.state.viewMode === PREVIEW_VIEW_MODES.CENTERED
      ? PREVIEW_VIEW_MODES.ORIGINAL : PREVIEW_VIEW_MODES.CENTERED);
    hud(activePreview.state.viewMode === PREVIEW_VIEW_MODES.ORIGINAL
      ? 'view: ORIGINAL file coordinates (wrapper identity — camera moved instead; centering NOT applied)'
      : 'view: fit-to-view (centering applied EXACTLY ONCE at the presentation wrapper)');
  });
  ui.btnWire.addEventListener('click', () => {
    if (!activePreview) return;
    activePreview.setWireframe(!activePreview.state.wireframe);
    hud(`wireframe ${activePreview.state.wireframe ? 'ON' : 'OFF'}`);
  });
  window.addEventListener('keydown', (ev) => {
    if (ev.target && /INPUT|TEXTAREA|SELECT/.test(ev.target.tagName)) return;
    if (ev.key === 'f' || ev.key === 'F') activePreview?.fitToBounds();
    if (ev.key === 'r' || ev.key === 'R') resetCamera();
    if (ev.key === 'w' || ev.key === 'W') ui.btnWire.click();
    if (ev.key === 'c' || ev.key === 'C') ui.btnOrigcoords.click();
  });

  // deep link: /catalog#model=193313
  const m = /^#model=(\d+)$/.exec(location.hash);
  if (m && CATALOG_CLIENT_PINS.models[m[1]]) {
    await openPreview(m[1]);
  } else if (m) {
    hud(`#model=${m[1]}: no safe import established for this id — the preview is only for the four pinned primaries`);
  }

  // ---- the single render loop ----
  const clock = new THREE.Clock();
  (function loop() {
    requestAnimationFrame(loop);
    void clock.getDelta();
    controls.update();
    renderer.render(scene, camera);
  })();

  if (!window.__pecCatalog.selectedModel) {
    hud('CATALOG — both eras, era-separated. Sort: measured largest->smallest, UNKNOWN last. Click a PREVIEWABLE row for the four-primary preview.');
  }
}

boot().catch((e) => {
  setLoadStatus(`ERROR_BOOT: ${String(e?.message ?? e).slice(0, 160)}`);
  recordError(`BOOT FAILED: ${e?.stack ?? e}`);
  hud('ERROR: boot failed (see the error banner + diagnostics).');
  window.__pecCatalog.boot = 'error';
});
