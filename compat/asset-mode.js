// asset-mode.js -- PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// ASSET MODE (contract ?7 item 1): model 218757 loaded from the pinned
// container through the asset API; orbit camera; fit-bounds action;
// solid/wireframe toggle; axes helper; hierarchy inspector (block tree with
// names, supported/opaque status, per-block ORIGINAL SERIALIZED TRS vs
// COMPUTED FILE_SCENE_SPACE transform).
//
// dPVS POLICY (contract ?7): meshes whose NAMES resemble dPVS/occluder are
// HINTS, not proven runtime roles. They stay ADDRESSABLE (selectable +
// inspectable at all times); the visibility toggle is a clearly-labeled
// HEURISTIC that may hide them, and the visible ledger reports total
// imported vs currently visible with exclusion reasons -- the app never
// claims more rendered than visible.
//
// Node-testable exports (THREE injected where needed): isDpvsHeuristicHint,
// computeVisibilityLedger, buildInspectorRows, buildAssetRenderModel.

import { buildRenderModel } from '../src/pecompat/PecRenderConvert.js';

export const DPVS_HEURISTIC_LABEL =
  'dPVS_NAME_HEURISTIC_HINT -- name-based hint only; runtime occluder role NOT proven; meshes remain addressable (selectable/inspectable)';

export function isDpvsHeuristicHint(name) {
  return /dpvs|occ/i.test(name ?? '');
}

/** The honest visible-mesh ledger: imported vs visible with exclusion
 *  reasons. Pure -- tested in T8. */
export function computeVisibilityLedger(meshObjects, dpvsHidden) {
  const exclusions = [];
  let visible = 0;
  for (const mesh of meshObjects) {
    const hidden = dpvsHidden && mesh.userData.dpvsHint === true;
    if (hidden) {
      exclusions.push({
        meshBlock: mesh.userData.meshBlock,
        meshName: mesh.userData.meshName,
        reason: 'HIDDEN_BY_USER_DPVS_HEURISTIC_TOGGLE',
        detail: DPVS_HEURISTIC_LABEL,
      });
    } else {
      visible++;
    }
  }
  return {
    imported: meshObjects.length,
    visible,
    exclusions,
    accounting: `imported ${meshObjects.length} / currently visible ${visible}` +
      (exclusions.length ? ` / excluded ${exclusions.length} (heuristic user toggle; reason per mesh in exclusions)` : ' / none excluded'),
  };
}

/** Inspector rows: one per block -- names, supported/opaque status, original
 *  serialized local TRS vs computed FILE_SCENE_SPACE world TRS. Pure. */
export function buildInspectorRows(ir, worldTransforms) {
  return ir.blocks.map((b) => {
    const w = worldTransforms.get(b.index) ?? null;
    return {
      index: b.index,
      type: b.type,
      name: b.name,
      decodeStatus: b.decodeStatus,
      statusLabel: b.decodeStatus === 'SUPPORTED'
        ? 'supported'
        : `${b.decodeStatus} (Ark block; semantics not fully decoded -- kept addressable, never silently interpreted)`,
      isMesh: b.type === 'NiTriShape',
      dpvsHint: b.type === 'NiTriShape' ? isDpvsHeuristicHint(b.name) : false,
      originalSerializedLocalTrs: b.localTrs
        ? { translate: [...b.localTrs.translate], rotate: b.localTrs.rotate.map((r) => [...r]), scale: b.localTrs.scale }
        : null,
      computedFileSceneSpaceTrs: w
        ? { translate: [...w.translate], rotate: w.rotate.map((r) => [...r]), scale: w.scale }
        : null,
      sceneMember: worldTransforms.has(b.index),
    };
  });
}

/** Build the asset render model (no instance wrapper). THREE injected. */
export function buildAssetRenderModel(THREE, asset, opts = {}) {
  const model = buildRenderModel(THREE, asset, opts);
  for (const mesh of model.meshObjects) {
    mesh.userData.dpvsHint = isDpvsHeuristicHint(mesh.userData.meshName);
  }
  return model;
}

// ---------------------------------------------------------------------------
// browser mount (all DOM/THREE wiring lives below -- Node imports never run it)
// ---------------------------------------------------------------------------
function trsText(trs) {
  if (!trs) return '(none)';
  const t = trs.translate.map((v) => v.toFixed(3)).join(', ');
  const s = typeof trs.scale === 'number' ? trs.scale.toFixed(3) : '';
  return `t(${t}) s(${s})`;
}

export function mountAssetMode(ctx) {
  const { THREE, scene, asset, ui, diagnostics, hud, observable } = ctx;
  // the app-level shared resource cache: the SAME BufferGeometry objects the
  // authored scene mode uses for its two instances (one asset = one resource).
  const model = buildAssetRenderModel(THREE, asset, { geometryCache: ctx.geometryCache });
  scene.add(model.root);

  const state = {
    wireframe: false,
    dpvsHidden: false,
    selectedBlock: null,
    model,
  };

  // axes helper (authored lab helper -- not original asset data)
  const axes = new THREE.AxesHelper(2.0);
  axes.name = 'lab-axes-helper (AUTHORED)';
  scene.add(axes);

  const rows = buildInspectorRows(asset.ir, asset.worldTransforms);
  const byBlock = new Map(model.meshObjects.map((m) => [m.userData.meshBlock, m]));

  function renderInspector() {
    const html = ['<table class="insp"><tr><th>idx</th><th>type:name</th><th>status</th><th>serialized local TRS</th><th>FILE_SCENE world TRS</th></tr>'];
    for (const r of rows) {
      const sel = state.selectedBlock === r.index ? ' class="sel"' : '';
      const dpvs = r.dpvsHint ? ` <span class="dpvs" title="${DPVS_HEURISTIC_LABEL}">[dPVS-name-hint]</span>` : '';
      html.push(
        `<tr data-block="${r.index}"${sel}><td>${r.index}</td>` +
        `<td>${r.type}:${r.name ?? ''}${dpvs}</td>` +
        `<td>${r.statusLabel}</td>` +
        `<td class="mono">${trsText(r.originalSerializedLocalTrs)}</td>` +
        `<td class="mono">${trsText(r.computedFileSceneSpaceTrs)}</td></tr>`);
    }
    html.push('</table>');
    ui.inspector.innerHTML = html.join('\n');
    for (const trEl of ui.inspector.querySelectorAll('tr[data-block]')) {
      trEl.addEventListener('click', () => selectBlock(Number(trEl.dataset.block)));
    }
  }

  function selectBlock(index) {
    state.selectedBlock = index;
    const r = rows.find((x) => x.index === index);
    if (r) {
      ui.selection.innerHTML =
        `<div><b>selected block</b> [${r.index}] ${r.type}:${r.name ?? ''}</div>` +
        `<div>status: ${r.statusLabel}</div>` +
        `<div class="mono">serialized local TRS: ${trsText(r.originalSerializedLocalTrs)}</div>` +
        `<div class="mono">FILE_SCENE_SPACE world TRS: ${trsText(r.computedFileSceneSpaceTrs)}</div>` +
        (r.isMesh
          ? `<div>mesh: ${r.dpvsHint ? DPVS_HEURISTIC_LABEL : 'mesh block (addressable)'}</div>`
          : `<div>scene member: ${r.sceneMember ? 'yes' : 'no (resource/property block)'}</div>`);
    }
    renderInspector();
    if (observable) observable.selectedBlock = index;
  }

  function applyVisibility() {
    for (const mesh of model.meshObjects) {
      const hidden = state.dpvsHidden && mesh.userData.dpvsHint === true;
      mesh.visible = !hidden;
      const wire = mesh.children.find((c) => c.name.startsWith('wire['));
      if (wire) wire.visible = state.wireframe && !hidden;
    }
    const ledger = computeVisibilityLedger(model.meshObjects, state.dpvsHidden);
    ui.ledger.innerHTML =
      `<div><b>visible ledger</b> ${ledger.accounting}</div>` +
      (ledger.exclusions.length
        ? `<div class="mono">${ledger.exclusions.map((x) => `#${x.meshBlock} ${x.meshName}: ${x.reason}`).join('<br>')}</div>`
        : '');
    if (diagnostics) diagnostics.updateVisibleLedger(ledger);
    if (observable) {
      observable.visibleLedger = { imported: ledger.imported, visible: ledger.visible, exclusions: ledger.exclusions.length };
    }
  }

  function applyWireframe() {
    for (const mesh of model.meshObjects) {
      const wire = mesh.children.find((c) => c.name.startsWith('wire['));
      if (wire) wire.visible = state.wireframe && mesh.visible;
    }
    if (observable) observable.wireframe = state.wireframe;
  }

  ui.btnWire.addEventListener('click', () => {
    state.wireframe = !state.wireframe;
    applyWireframe();
    hud(`wireframe ${state.wireframe ? 'ON' : 'OFF'}`);
  });
  ui.btnDpvs.addEventListener('click', () => {
    state.dpvsHidden = !state.dpvsHidden;
    applyVisibility();
    hud(`dPVS-name-hint meshes ${state.dpvsHidden ? 'HIDDEN (heuristic toggle -- they remain selectable in the inspector)' : 'VISIBLE'}`);
  });

  // click-pick a mesh -> select its block (addressability proof)
  ctx.canvas.addEventListener('pointerdown', (ev) => ctx.pickHandler(ev, model.meshObjects, (mesh) => {
    selectBlock(mesh.userData.meshBlock);
  }));

  renderInspector();
  applyVisibility();
  applyWireframe();
  selectBlock(asset.ir.roots[0]);
  hud(`ASSET MODE -- 218757 imported ${model.meshObjects.length} meshes (14 associations preserved incl. helper candidates); click rows or meshes to inspect`);

  return {
    kind: 'asset',
    model,
    state,
    rows,
    fitBounds() { return ctx.fitToObjects(model.meshObjects); },
    selectBlock,
    dispose() {
      scene.remove(model.root);
      scene.remove(axes);
      // geometries are ASSET resources (shared with the scene mode) -- disposed
      // only by the app's final teardown, not per-mode.
    },
  };
}
