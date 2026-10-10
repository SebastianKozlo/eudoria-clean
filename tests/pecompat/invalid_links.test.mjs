// invalid_links.test.mjs — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// T4 part 1 (plan T5): invalid/missing link CONTROLLED failures — cycle;
// dangling required child link; dangling model-data ref; missing master
// (instance layer); dangling scene parent; multi-parent REPORTED, never
// silently selected. Every case must be REJECTED/DIAGNOSED LOUDLY — a silent
// identity transform would be a FAIL.
//
// MEASURED_QUANTITY: thrown error classes / validation report contents.
// INDEPENDENT_SOURCE_OF_TRUTH: the contract §6 rule set (cycles/dangling
//   REQUIRED links REJECTED; multiple parents REPORTED) — asserted by
//   observing WHICH classes are reported, and that NO composition happens.
// WHY_NON_CIRCULAR: each case is a controlled invalid input; success is
//   defined as the CORRECT rejection, not as any output of the code.
// FAILURE_CASE_DETECTED: the invalid inputs themselves ARE the failure cases —
//   a missing rejection (or a silently-resolved multi-parent) fails the test.
import {
  makeSyntheticIR, validateSceneGraph, composeWorldTransforms,
} from '../../src/pecompat/PecSceneIR.js';
import { PecInstanceRegistry } from '../../src/pecompat/PecInstanceBuilder.js';
import { record, trs } from './_helpers.mjs';

const TRI = { positions: [0, 0, 0, 1, 0, 0, 0, 1, 0], indices: [0, 1, 2] };

function expectThrow(fn, classNeedle, id, name, extra = {}) {
  try {
    fn();
    return record(id, name, 'FAIL', {
      measuredQuantity: 'rejection',
      measured: 'NO ERROR THROWN — invalid input was ACCEPTED (silent failure class)',
      expected: `loud rejection mentioning "${classNeedle}"`,
      failureCaseDetected: 'invalid link accepted silently',
      ...extra,
    });
  } catch (e) {
    const msg = String(e?.message ?? e);
    const ok = msg.includes(classNeedle);
    return record(id, name, ok ? 'PASS' : 'FAIL', {
      measuredQuantity: 'rejection error class',
      measured: msg,
      expected: `loud rejection mentioning "${classNeedle}"`,
      failureCaseDetected: ok ? 'none (invalid input correctly rejected)' : 'wrong rejection class',
      ...extra,
    });
  }
}

export async function run(ctx) {
  const out = [];

  // ---- cycle in the scene-child graph ----
  const irCycle = makeSyntheticIR({
    assetId: 'SYN_T4_CYCLE',
    blocks: [
      { index: 0, type: 'NiNode', name: 'a', localTrs: trs([1, 0, 0]), children: [1] },
      { index: 1, type: 'NiNode', name: 'b', localTrs: trs([0, 1, 0]), children: [0] },
    ],
  });
  // give the cycle a reachable root so the cycle itself is the reported error:
  const vCycle = validateSceneGraph(irCycle);
  const cycleReported = vCycle.errors.some((e) => e.class === 'SCENE_GRAPH_CYCLE');
  let cycleComposed = false;
  try { composeWorldTransforms(irCycle); cycleComposed = true; } catch { cycleComposed = false; }
  out.push(record('T4a_cycle_rejected', 'scene-child cycle rejected loudly', (cycleReported && !cycleComposed) ? 'PASS' : 'FAIL', {
    measuredQuantity: 'validation error classes + composition refusal',
    measured: { cycleReported, composedAnyway: cycleComposed, errorClasses: vCycle.errors.map((e) => e.class) },
    expected: { cycleReported: true, composedAnyway: false },
    failureCaseDetected: cycleReported && !cycleComposed ? 'none (cycle correctly rejected)' : 'cycle accepted or composed',
    whyNonCircular: 'a deliberately cyclic authored graph; success = correct rejection behavior',
  }));

  // ---- dangling REQUIRED child link ----
  const irDangling = makeSyntheticIR({
    assetId: 'SYN_T4_DANGLING_CHILD',
    blocks: [
      { index: 0, type: 'NiNode', name: 'root', children: [99] },
    ],
  });
  const vDang = validateSceneGraph(irDangling);
  const dangReported = vDang.errors.some((e) => e.class === 'DANGLING_CHILD_REF');
  let dangComposed = false;
  try { composeWorldTransforms(irDangling); dangComposed = true; } catch { dangComposed = false; }
  out.push(record('T4b_dangling_child_rejected', 'dangling required child link rejected', (dangReported && !dangComposed) ? 'PASS' : 'FAIL', {
    measuredQuantity: 'validation error classes + composition refusal',
    measured: { dangReported, composedAnyway: dangComposed, errorClasses: vDang.errors.map((e) => e.class) },
    expected: { dangReported: true, composedAnyway: false },
    failureCaseDetected: dangReported && !dangComposed ? 'none (dangling child correctly rejected)' : 'dangling child accepted',
    whyNonCircular: 'a deliberately dangling authored link; success = correct rejection',
  }));

  // ---- dangling model-data (geometry) ref on a mesh ----
  const irData = makeSyntheticIR({
    assetId: 'SYN_T4_DANGLING_DATA',
    blocks: [
      { index: 0, type: 'NiNode', name: 'root', children: [1] },
      { index: 1, type: 'NiTriShape', name: 'mesh', dataRef: 42 },
    ],
  });
  const vData = validateSceneGraph(irData);
  const dataReported = vData.errors.some((e) => e.class === 'DANGLING_MODEL_DATA_REF');
  out.push(record('T4c_dangling_data_ref', 'dangling model-data ref diagnosed', dataReported ? 'PASS' : 'FAIL', {
    measuredQuantity: 'validation error classes',
    measured: { dataReported, errorClasses: vData.errors.map((e) => e.class) },
    expected: { dataReported: true },
    failureCaseDetected: dataReported ? 'none' : 'dangling data ref not diagnosed',
    whyNonCircular: 'controlled invalid resource link; success = correct diagnosis',
  }));

  // ---- multi-parent: REPORTED, never silently selected ----
  const irMulti = makeSyntheticIR({
    assetId: 'SYN_T4_MULTI_PARENT',
    blocks: [
      { index: 0, type: 'NiNode', name: 'root', children: [1, 2] },
      { index: 1, type: 'NiNode', name: 'p1', localTrs: trs([10, 0, 0]), children: [3] },
      { index: 2, type: 'NiNode', name: 'p2', localTrs: trs([0, 20, 0]), children: [3] },
      { index: 3, type: 'NiTriShape', name: 'mesh', dataRef: 4 },
      { index: 4, type: 'NiTriShapeData', name: 'data', geometry: TRI },
    ],
  });
  const vMulti = validateSceneGraph(irMulti);
  const multiReport = vMulti.errors.find((e) => e.class === 'MULTI_PARENT_REPORT');
  const multiReportedWithBothParents = !!multiReport &&
    multiReport.multiParent.length === 1 &&
    multiReport.multiParent[0].child === 3 &&
    multiReport.multiParent[0].parents.length === 2 &&
    multiReport.multiParent[0].parents.includes(1) &&
    multiReport.multiParent[0].parents.includes(2);
  let multiComposed = false;
  try { composeWorldTransforms(irMulti); multiComposed = true; } catch { multiComposed = false; }
  out.push(record('T4d_multi_parent_reported', 'multiple parents reported (never silently selected)', (multiReportedWithBothParents && !multiComposed) ? 'PASS' : 'FAIL', {
    measuredQuantity: 'multi-parent report contents + composition refusal',
    measured: { multiReportedWithBothParents, composedAnyway: multiComposed, report: multiReport ?? null },
    expected: { multiReportedWithBothParents: true, composedAnyway: false },
    failureCaseDetected: multiReportedWithBothParents && !multiComposed
      ? 'none (both parents reported; no arbitrary selection)'
      : 'multi-parent silently resolved or composition proceeded',
    whyNonCircular: 'a deliberately conflicting authored graph; success = full report + refusal',
  }));

  // ---- instance layer: missing master (attachment source) ----
  const irOk = makeSyntheticIR({
    assetId: 'SYN_T4_INSTANCE_ASSET',
    blocks: [
      { index: 0, type: 'NiNode', name: 'root', children: [1] },
      { index: 1, type: 'NiTriShape', name: 'mesh', dataRef: 2 },
      { index: 2, type: 'NiTriShapeData', name: 'data', geometry: TRI },
    ],
  });
  const registry = new PecInstanceRegistry({ ir: irOk, worldTransforms: composeWorldTransforms(irOk) });
  out.push(expectThrow(
    () => registry.createInstance({ instanceId: 'i1', attachment: { sourceInstanceId: 'ghost-master', attachmentPointName: 'top' } }),
    'MISSING_MASTER', 'T4e_missing_master', 'missing master (attachment source) rejected',
    {
      measuredQuantity: 'instance-layer rejection class',
      whyNonCircular: 'a deliberately missing master reference; success = loud rejection (no silent identity instance)',
    },
  ));

  // ---- instance layer: dangling scene parent ----
  out.push(expectThrow(
    () => registry.createInstance({ instanceId: 'i2', sceneParentId: 'ghost-parent' }),
    'DANGLING_SCENE_PARENT', 'T4f_dangling_scene_parent', 'dangling scene parent rejected',
    {
      measuredQuantity: 'instance-layer rejection class',
      whyNonCircular: 'a deliberately missing parent; success = loud rejection',
    },
  ));

  // ---- instance layer: duplicate instanceId ----
  registry.createInstance({ instanceId: 'dup' });
  out.push(expectThrow(
    () => registry.createInstance({ instanceId: 'dup' }),
    'duplicate instanceId', 'T4g_duplicate_instance_id', 'duplicate instanceId rejected',
    {
      measuredQuantity: 'instance identity uniqueness',
      whyNonCircular: 'instance identity must stay unique (contract §6)',
    },
  ));

  // ---- instance layer: scene-parent cycle ----
  const reg2 = new PecInstanceRegistry({ ir: irOk, worldTransforms: composeWorldTransforms(irOk) });
  const c1 = reg2.createInstance({ instanceId: 'c1', authoredTrs: trs([1, 0, 0]) });
  reg2.createInstance({ instanceId: 'c2', sceneParentId: 'c1', authoredTrs: trs([0, 1, 0]) });
  // force a cycle (bypass attachChild guard by direct record edit — the
  // registry must still detect it at validation):
  reg2.instances.get('c1').sceneParentId = 'c2';
  const vInst = reg2.validate();
  let instComposed = false;
  try { reg2.instanceSceneTransform('c2'); instComposed = true; } catch { instComposed = false; }
  const instCycleOk = !vInst.ok && vInst.errors.some((e) => e.class === 'INSTANCE_SCENE_CYCLE') && !instComposed;
  out.push(record('T4h_instance_scene_cycle', 'instance scene-parent cycle rejected', instCycleOk ? 'PASS' : 'FAIL', {
    measuredQuantity: 'instance validation + composition refusal',
    measured: { errors: vInst.errors, composedAnyway: instComposed },
    expected: { cycleDetected: true, composedAnyway: false },
    failureCaseDetected: instCycleOk ? 'none (cycle detected and refused)' : 'instance cycle accepted',
    whyNonCircular: 'a deliberately cyclic instance chain; success = detection + refusal',
  }));

  return out;
}
