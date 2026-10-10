// app_integration.test.mjs — T8 (APP_SERVER_TESTS phase) — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// Node-side app-integration checks through THE APP'S OWN BUILDER PATH
// (dispatch T8): two instances built from the shared asset with independent
// transforms; instance selection/transform-change leaves the other UNCHANGED
// (reusing the phase-2 instance semantics through the app's own
// createAuthoredScene / buildInstanceRenderModels / setAuthoredTrsFromInputs);
// diagnostics fields present and honest (buildDiagnosticsModel,
// computeVisibilityLedger, buildInspectorRows, wireToAsset).
// NEGATIVE CONTROLS: tampered wire (pin mismatch + transform corruption) must
// fail CLOSED; a hidden dPVS-hint mesh must produce an honest exclusion, never
// a silent pass.
import { writeFile, mkdir } from 'node:fs/promises';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { loadThree, sha256 } from './_helpers.mjs';
import { PecAssetAdapter, MODEL_218757_PINS } from '../../src/pecompat/PecAssetAdapter.js';
import { buildWireSceneIR } from '../../compat/server-sceneir.mjs';
import { wireToAsset, verifyGeometryFingerprints, buildDiagnosticsModel, CLIENT_PIN } from '../../compat/api.js';
import { createAuthoredScene, buildInstanceRenderModels, setAuthoredTrsFromInputs, AUTHORING } from '../../compat/scene-mode.js';
import { buildAssetRenderModel, computeVisibilityLedger, buildInspectorRows } from '../../compat/asset-mode.js';
import { trsDeepEqual } from '../../src/pecompat/PecTransform.js';

function rec(id, name, status, extra = {}) {
  return { id, name, status, ...extra };
}
const ok = (b) => (b ? 'PASS' : 'FAIL');

export async function run(ctx) {
  const rawDir = ctx.rawDir;
  await mkdir(rawDir, { recursive: true });
  const records = [];

  // -- inputs: the pinned container (LOUD not-performed without it) + three --
  if (!ctx.modelsPath) {
    return [rec('T8_CONTAINER_UNAVAILABLE', 'app-integration against the real pinned container', 'NOT_PERFORMED', {
      measuredQuantity: 'container availability',
      measured: 'no --models path supplied',
      failureCaseDetected: 'T8 requires the pinned Models.bnt (the app path loads the REAL regenerated asset)',
    })];
  }
  let THREE;
  try {
    ({ THREE } = await loadThree());
  } catch (e) {
    return [rec('T8_THREE_UNAVAILABLE', 'three 0.185.0 module load for the render-level checks', 'NOT_PERFORMED', {
      measuredQuantity: 'three module resolution',
      measured: String(e?.message ?? e),
      failureCaseDetected: 'pinned three module not resolvable — render-level instance checks not executed',
    })];
  }

  // -- 1. the real asset, regenerated from the pinned container (server path) --
  let loaded;
  try {
    const adapter = new PecAssetAdapter({
      readFile: async (p) => new Uint8Array(await readFile(p)),
      sha256,
    }, { modelsBntPath: ctx.modelsPath });
    loaded = await adapter.loadModel(MODEL_218757_PINS.modelId);
  } catch (e) {
    return [rec('T8_ASSET_LOAD', 'pinned asset load through PecAssetAdapter (fail-closed)', 'FAIL', {
      measuredQuantity: 'container/payload SHA verification + reader + IR build',
      measured: String(e?.message ?? e).slice(0, 2000),
      failureCaseDetected: 'the pinned container load failed — the app path cannot be exercised',
    })];
  }
  records.push(rec('T8_ASSET_LOAD', 'pinned asset load through PecAssetAdapter (fail-closed SHA verified)', 'PASS', {
    measuredQuantity: 'payloadSha256 vs pin + block/mesh accounting',
    measured: {
      payloadSha256: loaded.provenance.payloadSha256,
      blocks: loaded.ir.blocks.length,
      meshes: loaded.ir.meshAssociations.length,
      elapsedMs: loaded.provenance.elapsedMs,
    },
    independentSourceOfTruth: 'the pinned SHA256 identities (contract §2)',
    whyNonCircular: 'the load is refused by the adapter itself on any pin mismatch',
    failureCaseDetected: 'none',
  }));

  // -- 2. the wire round-trip: exactly what the server serves and the app rebuilds --
  const wireServer = buildWireSceneIR(loaded);
  const wire = JSON.parse(JSON.stringify(wireServer)); // the HTTP wire round-trip
  let asset;
  try {
    asset = wireToAsset(wire);
  } catch (e) {
    return [rec('T8_WIRE_TO_ASSET', 'the app client path rebuilds the asset from the served wire (pin + cross-checks)', 'FAIL', {
      measuredQuantity: 'wireToAsset fail-closed rebuild',
      measured: String(e?.message ?? e).slice(0, 2000),
      failureCaseDetected: 'the app client path refused the served wire — app cannot render',
    })];
  }
  const rebuildOk = asset.ir.blocks.length === 66 && asset.ir.meshAssociations.length === 14 &&
    asset.worldTransforms.size > 0 && asset.ir.diagnostics.textureBindings.length === 14;
  records.push(rec('T8_WIRE_TO_ASSET', 'the app client path rebuilds the asset from the served wire (pin + composition cross-checks)', ok(rebuildOk), {
    measuredQuantity: 'rebuilt IR accounting + client-composed world transforms vs the shipped FILE_SCENE_SPACE artifact',
    measured: { blocks: asset.ir.blocks.length, meshes: asset.ir.meshAssociations.length, composed: asset.worldTransforms.size },
    independentSourceOfTruth: 'the wire payload built by the server module + the phase-2 measured accounting',
    whyNonCircular: 'the client recomposes transforms itself and cross-checks against the server-shipped artifact — two independent computations must agree',
    failureCaseDetected: 'wire corruption, pin mismatch, composition mismatch',
  }));

  // -- 3. NEGATIVE CONTROLS on the client fail-closed path --
  {
    // 3a. tampered pin
    const tamperedPin = JSON.parse(JSON.stringify(wire));
    tamperedPin.provenance.payloadSha256 = 'f'.repeat(64);
    let pinRefused = false;
    let pinMsg = '';
    try { wireToAsset(tamperedPin); } catch (e) { pinRefused = true; pinMsg = e.message; }
    // 3b. corrupted transform in the wire (composition cross-check must catch it)
    const tamperedTrs = JSON.parse(JSON.stringify(wire));
    const rootIdx = tamperedTrs.fileSceneSpaceTransforms.findIndex((r) => r.worldTrs);
    tamperedTrs.blocks[rootIdx].localTrs.translate[0] += 1.25;
    let trsRefused = false;
    let trsMsg = '';
    try { wireToAsset(tamperedTrs); } catch (e) { trsRefused = true; trsMsg = e.message; }
    const both = pinRefused && trsRefused;
    records.push(rec('T8_CLIENT_FAIL_CLOSED_NEGATIVES', 'tampered wire (wrong pin / corrupted transform) is REFUSED by the app client path', ok(both), {
      measuredQuantity: 'exception raised by wireToAsset on each tampered input',
      measured: { pinRefused, pinMsg: pinMsg.slice(0, 160), trsRefused, trsMsg: trsMsg.slice(0, 160) },
      independentSourceOfTruth: 'the fail-closed checks in compat/api.js (pin + FILE_SCENE cross-check)',
      whyNonCircular: 'deliberately corrupted inputs must NOT render — the negative control proves the gate is real',
      failureCaseDetected: both ? 'none (both tampered inputs refused)' : 'A TAMPERED WIRE WAS ACCEPTED — fail-closed breach',
    }));
  }

  // -- 4. client-side geometry fingerprint re-hash (the app's verify path) --
  {
    const fp = await verifyGeometryFingerprints(asset);
    const fpOk = fp.status === 'OK' && fp.verified === 14;
    records.push(rec('T8_CLIENT_FINGERPRINTS', 'client-side re-hash of all 14 mesh vertex+index arrays vs the recomputed fingerprints', ok(fpOk), {
      measuredQuantity: 'crypto.subtle SHA256 of the rebuilt typed arrays vs meshAssociations fingerprints',
      measured: { status: fp.status, verified: fp.verified, elapsedMs: fp.elapsedMs },
      independentSourceOfTruth: 'the predecessor-measured per-mesh fingerprints (phase-2 T7 pins)',
      whyNonCircular: 'the client recomputes hashes from the arrays it would render and compares them to pinned values',
      failureCaseDetected: fp.status !== 'OK' ? 'fingerprint mismatch — wire arrays differ from the pinned geometry' : 'none',
    }));
  }

  // -- 5. TWO INSTANCES through the app's own builder path --
  {
    const authored = createAuthoredScene(asset);
    const [idA, idB] = authored.instances.map((i) => i.instanceId);
    const BAuthoredBefore = authored.registry.instances.get(idB).authoredTrs;
    const BSceneBefore = authored.registry.instanceSceneTransform(idB);

    // change A's authored transform through the app's input path
    const applied = setAuthoredTrsFromInputs(authored.registry, idA, { tx: 55.5, ty: 0, tz: 0, scale: 1.25, rzDeg: 90 });
    const AScene = authored.registry.instanceSceneTransform(idA);
    const BAuthoredAfter = authored.registry.instances.get(idB).authoredTrs;
    const BSceneAfter = authored.registry.instanceSceneTransform(idB);
    const bUnchangedAuthored = trsDeepEqual(BAuthoredBefore, BAuthoredAfter);
    const bUnchangedScene = trsDeepEqual(BSceneBefore, BSceneAfter);
    const aMoved = !trsDeepEqual(applied.updatedTrs, AUTHORING.instances.find((s) => s.instanceId === idA).authoredTrs) ||
      AScene.translate[0] === 55.5;

    // render-level: shared geometry, independent wrapper transforms
    const authored2 = createAuthoredScene(asset); // fresh registry at authored defaults (as the app mounts it)
    const ids = authored2.instances.map((i) => i.instanceId);
    const { models, geometryCache } = buildInstanceRenderModels(THREE, asset, authored2.registry, ids);
    const meshesA = models.get(ids[0]).meshObjects;
    const meshesB = models.get(ids[1]).meshObjects;
    const geometryShared = meshesA.length === meshesB.length && meshesA.every((m, i) => m.geometry === meshesB[i].geometry);
    const wrappersIndependent = models.get(ids[0]).instanceWrapper.matrix.equals(models.get(ids[1]).instanceWrapper.matrix) === false ||
      JSON.stringify([...models.get(ids[0]).instanceWrapper.matrix.elements]) !== JSON.stringify([...models.get(ids[1]).instanceWrapper.matrix.elements]);
    const conversionsOnce = [...models.values()].every((m) => m.conversion.appliedOnce === true && m.conversion.applications === 1);
    const rootIdx = asset.ir.roots[0];
    const distinctWorlds = authored2.registry.sceneWorldOfNode(ids[0], rootIdx)
      .translate.join(',') !== authored2.registry.sceneWorldOfNode(ids[1], rootIdx).translate.join(',');
    const cacheSize = geometryCache.size;

    const twoInstancesOk = bUnchangedAuthored && bUnchangedScene && aMoved && geometryShared &&
      wrappersIndependent && conversionsOnce && distinctWorlds && meshesA.length === 14 && cacheSize === 14;
    records.push(rec('T8_TWO_INSTANCES_INDEPENDENT', 'two instances from the shared asset: change A leaves B bit-identical; geometry SHARED; wrappers/conversions independent', ok(twoInstancesOk), {
      measuredQuantity: 'authored+composed TRS deep-equality before/after; BufferGeometry object identity across instances; conversion-application count',
      measured: {
        bUnchangedAuthored, bUnchangedScene, aMoved, geometryShared, wrappersIndependent, conversionsOnce, distinctWorlds,
        meshesPerInstance: meshesA.length, sharedGeometryCacheEntries: cacheSize,
        aAppliedTranslate: applied.updatedTrs.translate,
      },
      independentSourceOfTruth: 'trsDeepEqual (exact TRS comparison) + THREE object identity (===) of the geometry cache',
      whyNonCircular: 'the app builder path is executed as the app uses it; the independence predicate compares B against its own pre-change snapshot',
      failureCaseDetected: twoInstancesOk ? 'none' : 'instance separation or resource-sharing semantics broken',
    }));
  }

  // -- 6. diagnostics model honest + visibility ledger + inspector rows --
  {
    const diag = buildDiagnosticsModel(asset, {});
    const model = buildAssetRenderModel(THREE, asset);
    const ledgerAllVisible = computeVisibilityLedger(model.meshObjects, false);
    const ledgerDpvsHidden = computeVisibilityLedger(model.meshObjects, true);
    const rows = buildInspectorRows(asset.ir, asset.worldTransforms);
    const dpvsRows = rows.filter((r) => r.dpvsHint);
    const diagOk =
      diag.assetIdentity.pinVerified === true &&
      diag.blockAccounting.total === 66 && diag.blockAccounting.supported === 62 &&
      diag.blockAccounting.partiallyUnderstood === 2 && diag.blockAccounting.opaque === 2 &&
      diag.meshes.imported === 14 && diag.textureStatus.nameBound === 9 &&
      diag.textureStatus.untexturedLabeled === 5 && diag.textureStatus.perMesh.length === 14 &&
      typeof diag.meshes.renderedClaim === 'string' && diag.meshes.visibleLedger === null && // not claimed before render
      ledgerAllVisible.visible === 14 && ledgerAllVisible.exclusions.length === 0 &&
      ledgerDpvsHidden.visible === 9 && ledgerDpvsHidden.exclusions.length === 5 &&
      ledgerDpvsHidden.exclusions.every((x) => /dPVS|occ/i.test(x.meshName)) &&
      rows.length === 66 && dpvsRows.length === 5 &&
      rows.every((r) => typeof r.decodeStatus === 'string' && ('originalSerializedLocalTrs' in r) && ('computedFileSceneSpaceTrs' in r));
    records.push(rec('T8_DIAGNOSTICS_AND_LEDGER_HONEST', 'diagnostics fields present and honest; dPVS heuristic ledger reports imported vs visible with reasons (9/5 preserved)', ok(diagOk), {
      measuredQuantity: 'buildDiagnosticsModel + computeVisibilityLedger + buildInspectorRows outputs vs the measured IR accounting',
      measured: {
        pinVerified: diag.assetIdentity.pinVerified,
        blocks: `${diag.blockAccounting.supported}+${diag.blockAccounting.partiallyUnderstood + diag.blockAccounting.opaque}=${diag.blockAccounting.total}`,
        meshes: diag.meshes.imported,
        textureStatus: `${diag.textureStatus.nameBound}+${diag.textureStatus.untexturedLabeled}`,
        ledgerAllVisible: `${ledgerAllVisible.imported}/${ledgerAllVisible.visible}`,
        ledgerDpvsHidden: `${ledgerDpvsHidden.imported}/${ledgerDpvsHidden.visible} (excluded ${ledgerDpvsHidden.exclusions.length})`,
        inspectorRows: rows.length, dpvsHintRows: dpvsRows.length,
      },
      independentSourceOfTruth: 'the phase-2 measured accounting (62+4=66, 14 meshes, 9 TEXTURE_NAME_BOUND + 5 UNTEXTURED, 5 dPVS-named meshes)',
      whyNonCircular: 'the diagnostics/ledger builders are fed the SAME asset and their outputs are compared against independently pinned counts — a hidden mesh MUST appear as an exclusion, never as a silent pass',
      failureCaseDetected: diagOk ? 'none' : 'diagnostics dishonest or incomplete (missing field / wrong count / silent exclusion)',
    }));
  }

  await writeFile(path.join(rawDir, 'APP_INTEGRATION_MEASURED.json'), JSON.stringify({
    run: 'PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009',
    suite: 'tests/pecompat/app_integration.test.mjs (T8)',
    threeModule: '0.185.0 (pinned; see loadThree in tests/pecompat/_helpers.mjs)',
    records: records.map(({ id, status, measured }) => ({ id, status, measured: measured ?? null })),
  }, null, 1) + '\n', 'utf8');

  return records;
}
