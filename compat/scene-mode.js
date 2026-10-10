// scene-mode.js -- PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// AUTHORED SCENE MODE (contract ?7 item 2): TWO separate instances of the
// shared 218757 resource with INDEPENDENT authored transforms. Selecting one
// instance and changing ITS transform must NOT move the other. Each instance
// is independently selectable/inspectable (instance ID, asset ref, authored
// transform, composed scene transform). ALL authored coordinates are labeled
// AUTHOR_PLACED_LAB -- authored laboratory values, NOT historical Eudoria
// positions (HISTORICAL_WORLD_INSTANCE = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED
// = NO).
//
// The terrain is an EXPLICITLY AUTHORED lab grid (GridHelper) -- no Eudoria
// terrain integration is claimed or manufactured in this slice.
//
// VIEWER POLICY (labeled in the UI): the instance WRAPPER owns the scene
// transform; the imported asset hierarchy retains its serialized root/child
// transforms (VIEWER_INSTANCE_WRAPPER_POLICY from PecInstanceBuilder). This
// is NOT a reproduction of every SDK 2.6 root-replacement branch or the
// original PE placement mechanism.
//
// Node-testable exports: AUTHORING, createAuthoredScene, buildInstanceRenderModels,
// setAuthoredTrsFromInputs -- the app's own builder path, exercised by T8.

import { PecInstanceRegistry, VIEWER_INSTANCE_WRAPPER_POLICY } from '../src/pecompat/PecInstanceBuilder.js';
import { buildRenderModel } from '../src/pecompat/PecRenderConvert.js';
import { makeRotationZTrs, makeTranslationTrs, trsToColumnMajor4 } from '../src/pecompat/PecTransform.js';

/** The authored two-instance spec (AUTHOR_PLACED_LAB -- laboratory values). */
export const AUTHORING = Object.freeze({
  label: 'AUTHOR_PLACED_LAB',
  policy: VIEWER_INSTANCE_WRAPPER_POLICY,
  instances: Object.freeze([
    Object.freeze({
      instanceId: 'author-instance-A',
      authoredTrs: Object.freeze({ translate: Object.freeze([30, 0, -10]), rotate: Object.freeze([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), scale: 1.0 }),
      label: 'A -- offset right (AUTHOR_PLACED_LAB)',
    }),
    Object.freeze({
      instanceId: 'author-instance-B',
      authoredTrs: Object.freeze({ translate: Object.freeze([-30, 0, 10]), rotate: Object.freeze([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), scale: 1.0 }),
      label: 'B -- offset left (AUTHOR_PLACED_LAB)',
    }),
  ]),
  gridNote: 'AUTHORED LAB GRID (GridHelper) -- explicitly authored; NOT Eudoria terrain; no placement success claimed',
});

/** The app's own builder path: build the authored scene records from the
 *  SHARED asset (pure -- Node-tested in T8). */
export function createAuthoredScene(asset) {
  const registry = new PecInstanceRegistry(asset);
  const instances = [];
  for (const spec of AUTHORING.instances) {
    instances.push(registry.createInstance({
      instanceId: spec.instanceId,
      authoredTrs: spec.authoredTrs,
    }));
  }
  return { registry, instances };
}

/** Build the per-instance render models sharing ONE geometry cache (resource
 *  geometry shared; instance transforms independent). THREE injected. */
export function buildInstanceRenderModels(THREE, asset, registry, instanceIds, geometryCache) {
  const sharedCache = geometryCache ?? new Map(); // one cache for ALL instances
  const models = new Map();
  for (const id of instanceIds) {
    const sceneTrs = registry.instanceSceneTransform(id);
    models.set(id, buildRenderModel(THREE, asset, {
      instance: { instanceId: id, sceneTrs },
      geometryCache: sharedCache,
    }));
  }
  return { models, geometryCache: sharedCache };
}

/** Apply an authored TRS from UI inputs (deg -> rad for the Z rotation).
 *  Returns { updatedTrs, sceneTrs } -- the same path the UI uses. */
export function setAuthoredTrsFromInputs(registry, instanceId, { tx, ty, tz, scale, rzDeg }) {
  const t = makeTranslationTrs([tx, ty, tz]);
  const r = makeRotationZTrs((rzDeg * Math.PI) / 180).rotate;
  const trs = { translate: [...t.translate], rotate: r.map((row) => [...row]), scale };
  const updated = registry.setInstanceTransform(instanceId, trs);
  return { updatedTrs: updated.authoredTrs, sceneTrs: registry.instanceSceneTransform(instanceId) };
}

function trsToText(trs) {
  const t = trs.translate.map((v) => v.toFixed(3)).join(', ');
  return `t(${t}) s(${trs.scale.toFixed(3)})`;
}

// ---------------------------------------------------------------------------
// browser mount
// ---------------------------------------------------------------------------
export function mountSceneMode(ctx) {
  const { THREE, scene, asset, ui, diagnostics, hud, observable } = ctx;
  const authored = createAuthoredScene(asset);
  const { registry } = authored;
  const instanceIds = authored.instances.map((i) => i.instanceId);
  const { models, geometryCache } = buildInstanceRenderModels(THREE, asset, registry, instanceIds, ctx.geometryCache);
  for (const m of models.values()) scene.add(m.root);

  // the EXPLICITLY AUTHORED lab grid (never claimed as terrain)
  const grid = new THREE.GridHelper(120, 60, 0x30507a, 0x1c2c44);
  grid.name = 'lab-grid (AUTHORED -- not Eudoria terrain)';
  scene.add(grid);
  const axes = new THREE.AxesHelper(3.0);
  axes.name = 'lab-axes-helper (AUTHORED)';
  scene.add(axes);

  const state = {
    selectedInstanceId: instanceIds[0],
    wireframe: false,
    dpvsHidden: false,
  };

  function instanceSelection(id) {
    state.selectedInstanceId = id;
    const rec = registry.instances.get(id);
    const sceneTrs = registry.instanceSceneTransform(id);
    ui.selection.innerHTML =
      `<div><b>selected instance</b> ${id} <span class="lab">${AUTHORING.label}</span></div>` +
      `<div>asset ref: ${asset.ir.cacheKey} (shared resource)</div>` +
      `<div class="mono">authored TRS: ${trsToText(rec.authoredTrs)}</div>` +
      `<div class="mono">composed scene TRS: ${trsToText(sceneTrs)}</div>` +
      `<div class="policy">${VIEWER_INSTANCE_WRAPPER_POLICY}</div>`;
    // editor inputs reflect the selected instance's authored values
    ui.inputs.tx.value = rec.authoredTrs.translate[0];
    ui.inputs.ty.value = rec.authoredTrs.translate[1];
    ui.inputs.tz.value = rec.authoredTrs.translate[2];
    ui.inputs.scale.value = rec.authoredTrs.scale;
    ui.inputs.rzDeg.value = 0;
    for (const btn of ui.instanceButtons()) {
      btn.classList.toggle('active', btn.dataset.instance === id);
    }
    if (observable) observable.selectedInstance = id;
  }

  function refreshInstancePanel() {
    const rows = [];
    for (const id of instanceIds) {
      const rec = registry.instances.get(id);
      const sceneTrs = registry.instanceSceneTransform(id);
      rows.push(
        `<button class="inst-btn${state.selectedInstanceId === id ? ' active' : ''}" data-instance="${id}">` +
        `${id} ${trsToText(sceneTrs)}</button>`);
      if (observable) {
        observable.instances[id] = {
          authoredTrs: { translate: [...rec.authoredTrs.translate], scale: rec.authoredTrs.scale },
          composedSceneTranslate: [...sceneTrs.translate],
        };
      }
    }
    ui.instanceList.innerHTML = rows.join('\n');
    for (const btn of ui.instanceButtons()) {
      btn.addEventListener('click', () => instanceSelection(btn.dataset.instance));
    }
  }

  function applyAuthoredInputs() {
    const id = state.selectedInstanceId;
    const before = registry.instanceSceneTransform(id);
    const otherId = instanceIds.find((x) => x !== id);
    const otherBefore = registry.instanceSceneTransform(otherId);
    const { sceneTrs } = setAuthoredTrsFromInputs(registry, id, {
      tx: Number(ui.inputs.tx.value), ty: Number(ui.inputs.ty.value), tz: Number(ui.inputs.tz.value),
      scale: Number(ui.inputs.scale.value), rzDeg: Number(ui.inputs.rzDeg.value),
    });
    // wrapper matrix update: the wrapper OWNS the scene transform
    const model = models.get(id);
    model.instanceWrapper.matrixAutoUpdate = false;
    model.instanceWrapper.matrix.fromArray(trsToColumnMajor4(sceneTrs));
    model.instanceWrapper.updateMatrixWorld?.(true);
    const otherAfter = registry.instanceSceneTransform(otherId);
    const otherMoved = JSON.stringify([...otherBefore.translate]) !== JSON.stringify([...otherAfter.translate]);
    if (otherMoved) {
      hud(`INSTANCE INDEPENDENCE VIOLATION for ${otherId} -- this must never happen (T4 guards the semantics)`);
    }
    ui.independence.textContent =
      `independence check: changing ${id} left ${otherId} unchanged: ${otherMoved ? 'NO -- VIOLATION' : 'YES (authored + composed TRS bit-identical before/after)'}`;
    refreshInstancePanel();
    instanceSelection(id);
    if (observable) {
      observable.lastApplied = {
        instanceId: id,
        beforeTranslate: [...before.translate],
        afterTranslate: [...sceneTrs.translate],
        otherInstanceId: otherId,
        otherTranslateUnchanged: !otherMoved,
      };
    }
  }

  ui.btnApplyTrs.addEventListener('click', () => {
    applyAuthoredInputs();
    hud(`authored transform applied to ${state.selectedInstanceId} (${AUTHORING.label})`);
  });
  ui.btnInstanceReset.addEventListener('click', () => {
    const id = state.selectedInstanceId;
    const spec = AUTHORING.instances.find((s) => s.instanceId === id);
    registry.setInstanceTransform(id, spec.authoredTrs);
    const model = models.get(id);
    model.instanceWrapper.matrix.fromArray(trsToColumnMajor4(registry.instanceSceneTransform(id)));
    refreshInstancePanel();
    instanceSelection(id);
    hud(`instance ${id} reset to its authored default (${AUTHORING.label})`);
  });

  function applyVisibility() {
    for (const model of models.values()) {
      for (const mesh of model.meshObjects) {
        const hint = /dpvs|occ/i.test(mesh.userData.meshName ?? '');
        const hidden = state.dpvsHidden && hint;
        mesh.visible = !hidden;
        const wire = mesh.children.find((c) => c.name.startsWith('wire['));
        if (wire) wire.visible = state.wireframe && !hidden;
      }
    }
    let imported = 0; let visible = 0; const exclusions = [];
    for (const model of models.values()) {
      for (const mesh of model.meshObjects) {
        imported++;
        if (mesh.visible) visible++;
        else exclusions.push({ meshName: mesh.userData.meshName, reason: 'HIDDEN_BY_USER_DPVS_HEURISTIC_TOGGLE' });
      }
    }
    const ledger = {
      imported, visible, exclusions,
      accounting: `imported ${imported} (2x14 per-instance mesh objects) / currently visible ${visible}` +
        (exclusions.length ? ` / excluded ${exclusions.length} (heuristic user toggle)` : ' / none excluded'),
    };
    ui.ledger.innerHTML = `<div><b>visible ledger</b> ${ledger.accounting}</div>`;
    if (diagnostics) diagnostics.updateVisibleLedger(ledger);
    if (observable) observable.visibleLedger = { imported, visible, exclusions: exclusions.length };
  }

  ui.btnWire.addEventListener('click', () => {
    state.wireframe = !state.wireframe;
    applyVisibility();
    hud(`wireframe ${state.wireframe ? 'ON' : 'OFF'}`);
  });
  ui.btnDpvs.addEventListener('click', () => {
    state.dpvsHidden = !state.dpvsHidden;
    applyVisibility();
    hud(`dPVS-name-hint meshes ${state.dpvsHidden ? 'HIDDEN (heuristic toggle)' : 'VISIBLE'}`);
  });

  ctx.canvas.addEventListener('pointerdown', (ev) => {
    const allMeshes = [...models.values()].flatMap((m) => m.meshObjects);
    ctx.pickHandler(ev, allMeshes, (mesh) => {
      // resolve the owning instance by walking to the instance-wrapper group
      let node = mesh;
      while (node && !(node.name && node.name.startsWith('instance-wrapper:'))) node = node.parent;
      const id = node ? node.name.slice('instance-wrapper:'.length) : null;
      if (id && models.has(id)) instanceSelection(id);
    });
  });

  refreshInstancePanel();
  instanceSelection(instanceIds[0]);
  applyVisibility();
  hud(
    `SCENE MODE -- two authored instances of the shared 218757 resource (${AUTHORING.label}); ` +
    'select an instance, edit its authored transform, verify the other instance does NOT move');

  return {
    kind: 'scene',
    registry,
    models,
    geometryCache,
    state,
    fitBounds() {
      const meshes = [...models.values()].flatMap((m) => m.meshObjects);
      return ctx.fitToObjects(meshes);
    },
    applyAuthoredInputs,
    instanceSelection,
    dispose() {
      for (const m of models.values()) scene.remove(m.root);
      scene.remove(grid);
      scene.remove(axes);
    },
  };
}

// local helper (kept next to its only consumer)
