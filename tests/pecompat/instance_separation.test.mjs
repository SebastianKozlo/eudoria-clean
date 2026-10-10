// instance_separation.test.mjs — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// T3 (plan T4): two instances of ONE asset — shared resource geometry with
// INDEPENDENT transforms; changing one instance's authored transform must NOT
// move the other; the shared asset IR must stay unmutated.
//
// MEASURED_QUANTITY: geometry object identity + per-instance world transforms
//   (exact values) before/after a mutation of ONE instance.
// INDEPENDENT_SOURCE_OF_TRUTH: literal analytic world transforms written in
//   this test; THREE object identity (===) for geometry sharing.
// WHY_NON_CIRCULAR: expectations are hand-computed; the separation property
//   is asserted by EXACT before/after comparison of the untouched instance.
// FAILURE_CASE_DETECTED: if mutating instance A changes instance B's world
//   (aliasing/coupling bug), or if the two instances do not share the same
//   BufferGeometry/arrays, the test FAILS with the measured values.
import {
  makeSyntheticIR, composeWorldTransforms,
} from '../../src/pecompat/PecSceneIR.js';
import { PecInstanceRegistry, VIEWER_INSTANCE_WRAPPER_POLICY } from '../../src/pecompat/PecInstanceBuilder.js';
import { buildRenderModel } from '../../src/pecompat/PecRenderConvert.js';
import { trsDeepEqual, cloneTrs } from '../../src/pecompat/PecTransform.js';
import { loadThree, record, trs } from './_helpers.mjs';

export async function run(ctx) {
  const out = [];
  const { THREE } = await loadThree();

  // ONE shared synthetic asset (two meshes under a rotated parent):
  const assetIr = makeSyntheticIR({
    assetId: 'SYN_T3_SHARED_ASSET',
    blocks: [
      { index: 0, type: 'NiNode', name: 'assetRoot', localTrs: trs([1, 0, 0]), children: [1, 2] },
      { index: 1, type: 'NiTriShape', name: 'meshA', localTrs: trs([0, 0, 0]), dataRef: 3 },
      { index: 2, type: 'NiTriShape', name: 'meshB', localTrs: trs([10, 0, 0]), dataRef: 3 },
      { index: 3, type: 'NiTriShapeData', name: 'sharedData', geometry: { positions: [0, 0, 0, 1, 0, 0, 0, 1, 0], indices: [0, 1, 2] } },
    ],
  });
  const worldTransforms = composeWorldTransforms(assetIr);
  const asset = { ir: assetIr, worldTransforms };

  // snapshot of the serialized asset state (for the unmutated proof):
  const snapshotTrs = assetIr.blocks.map((b) => (b.localTrs ? cloneTrs(b.localTrs) : null));

  const registry = new PecInstanceRegistry(asset);
  const instA = registry.createInstance({ instanceId: 'inst-A', authoredTrs: trs([100, 0, 0]) });
  const instB = registry.createInstance({ instanceId: 'inst-B', authoredTrs: trs([0, 200, 0]) });

  // Independent scene transforms (hand-computed: authored only; asset root
  // composed per node by sceneWorldOfNode):
  const sceneA = registry.instanceSceneTransform('inst-A');
  const sceneB = registry.instanceSceneTransform('inst-B');
  const okScene = trsDeepEqual(sceneA, trs([100, 0, 0])) && trsDeepEqual(sceneB, trs([0, 200, 0]));

  // Node world INSIDE each instance: scene * worldInAsset. meshA worldInAsset
  // = assetRoot(1,0,0) * (0,0,0) = (1,0,0); so A: (101,0,0), B: (1,200,0).
  const nodeWorldA = registry.sceneWorldOfNode('inst-A', 1);
  const nodeWorldB = registry.sceneWorldOfNode('inst-B', 1);
  const expA = [101, 0, 0];
  const expB = [1, 200, 0];
  const okWorld = nodeWorldA.translate.every((v, i) => Math.abs(v - expA[i]) <= 1e-9) &&
    nodeWorldB.translate.every((v, i) => Math.abs(v - expB[i]) <= 1e-9);

  // RENDER sharing: one geometry cache across both instances -> the SAME
  // THREE.BufferGeometry objects; independent object transforms.
  const geometryCache = new Map();
  const rmA = buildRenderModel(THREE, asset, { instance: { instanceId: 'inst-A', sceneTrs: sceneA }, geometryCache });
  const rmB = buildRenderModel(THREE, asset, { instance: { instanceId: 'inst-B', sceneTrs: sceneB }, geometryCache });
  const geoA = rmA.meshObjects.map((m) => m.geometry);
  const geoB = rmB.meshObjects.map((m) => m.geometry);
  const sharedGeometry = geoA.length === geoB.length && geoA.length > 0 &&
    geoA.every((g, i) => g === geoB[i]);
  const sharedArrays = rmA.meshObjects.every((m, i) =>
    m.geometry.getAttribute('position').array === rmB.meshObjects[i].geometry.getAttribute('position').array);

  // instance wrapper separation in the render tree:
  const wrapperSeparate = rmA.instanceWrapper !== rmB.instanceWrapper &&
    rmA.instanceWrapper.matrix.elements.some((v, i) => v !== rmB.instanceWrapper.matrix.elements[i]);

  // MUTATION: change instance A's authored transform ONLY.
  const bWorldBefore = cloneTrs(nodeWorldB);
  registry.setInstanceTransform('inst-A', trs([500, 0, 0]));
  const nodeWorldA2 = registry.sceneWorldOfNode('inst-A', 1);
  const nodeWorldB2 = registry.sceneWorldOfNode('inst-B', 1);
  const aChanged = !trsDeepEqual(nodeWorldA2, nodeWorldA);
  const bUnchanged = trsDeepEqual(nodeWorldB2, bWorldBefore);
  const expA2 = [501, 0, 0];
  const okA2 = nodeWorldA2.translate.every((v, i) => Math.abs(v - expA2[i]) <= 1e-9);

  // the ASSET IR is unmutated by all instance operations:
  const assetIntact = assetIr.blocks.every((b, i) => {
    const snap = snapshotTrs[i];
    if (snap == null) return b.localTrs == null;
    return trsDeepEqual(b.localTrs, snap);
  });

  const ok = okScene && okWorld && sharedGeometry && sharedArrays && wrapperSeparate &&
    aChanged && bUnchanged && okA2 && assetIntact;

  out.push(record('T3_instance_separation', 'two instances: shared geometry, independent transforms', ok ? 'PASS' : 'FAIL', {
    measuredQuantity: 'geometry identity (===) + per-instance composed world transforms before/after mutating one instance + asset IR intactness',
    independentSourceOfTruth: 'literal analytic transforms: A=(100,0,0)->meshA world (101,0,0); B=(0,200,0)->(1,200,0); after A->(500,0,0): A=(501,0,0), B UNCHANGED',
    whyNonCircular: 'hand-computed expectations; separation asserted by exact before/after comparison of the untouched instance and by object identity for shared geometry',
    measured: {
      instanceSceneTransforms: { A: sceneA.translate, B: sceneB.translate },
      meshAWorldInA: nodeWorldA.translate,
      meshAWorldInB: nodeWorldB.translate,
      sharedGeometry, sharedArrays, wrapperSeparate,
      afterMutation: { A: nodeWorldA2.translate, B: nodeWorldB2.translate, aChanged, bUnchanged },
      assetIntact,
      uniqueInstanceIds: instA.instanceId !== instB.instanceId,
      viewerWrapperPolicy: VIEWER_INSTANCE_WRAPPER_POLICY,
    },
    expected: {
      meshAWorldInA: expA, meshAWorldInB: expB,
      sharedGeometry: true, sharedArrays: true, wrapperSeparate: true,
      afterMutation: { A: expA2, B: expB, aChanged: true, bUnchanged: true },
      assetIntact: true, uniqueInstanceIds: true,
    },
    failureCaseDetected: ok ? 'none' : 'instances coupled (mutation leaked), geometry not shared, or asset IR mutated',
  }));

  return out;
}
