// transform_composition.test.mjs — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// T1 (native Control B comparison) + T2 (authored synthetic transform tests:
// nonidentity asset root, parent rotation + uniform scale, translation,
// reparenting without compensation, conversion applied exactly once).
//
// MEASURED_QUANTITY: composed world transforms (full vectors/matrices).
// INDEPENDENT_SOURCE_OF_TRUTH: T1 — the native GB 1.2 SceneGraphPrinter
//   ground truth captured in phase 1 (CONTROLS_B.json, verbatim
//   "C <96,202,306>, R 0" / "C <58,221,363>, R 0"); T2 — analytic literal
//   arithmetic written directly in this test (hand-computed), not calls into
//   the code under test.
// WHY_NON_CIRCULAR: the IR composition (PecTransform/PecSceneIR) and the
//   THREE.Matrix4 composition are two independent math engines fed the same
//   parsed serialized TRS; both are compared against values neither produced.
// FAILURE_CASE_DETECTED: any component beyond tolerance = FAIL with the
//   measured values; double-conversion and compensated-reparent negatives
//   are asserted to be DETECTED (i.e. the wrong behaviors differ from the
//   measured correct one).
import { readNif10 } from '../../src/pecompat/PecNif10Reader.js';
import {
  buildAssetIR, composeWorldTransforms, makeSyntheticIR, validateSceneGraph,
} from '../../src/pecompat/PecSceneIR.js';
import {
  composeTrs, applyTrsPoint, trsToColumnMajor4, cloneTrs, trsDeepEqual,
  makeRotationZTrs,
} from '../../src/pecompat/PecTransform.js';
import {
  convertPointSceneToRender, buildRenderModel, RENDER_ADAPTER_CHOICE,
} from '../../src/pecompat/PecRenderConvert.js';
import {
  CONTROL_B_FIXTURES, loadThree, readFileBytes, sha256, record, trs, RZ90,
} from './_helpers.mjs';

const RAD90 = Math.PI / 2;

export async function run(ctx) {
  const out = [];
  const tol = ctx.tol ?? 1e-4;

  // ---------------- T1: native Control B fixtures ----------------
  const { THREE, modulePath, packageVersion } = await loadThree();

  for (const [fixtureName, fx] of Object.entries(CONTROL_B_FIXTURES)) {
    const bytes = await readFileBytes(fx.path);
    const fixtureSha = sha256(bytes);
    if (fixtureSha !== fx.sha256 || bytes.byteLength !== fx.sizeBytes) {
      out.push(record(`T1_${fixtureName}`, `native control comparison (${fixtureName})`, 'FAIL', {
        measured: { fixtureSha256: fixtureSha, size: bytes.byteLength },
        expected: { fixtureSha256: fx.sha256, size: fx.sizeBytes },
        failureCaseDetected: 'fixture identity mismatch — refusing to compare',
      }));
      continue;
    }
    const r = readNif10(bytes, { sourceName: `${fixtureName}.nif` });
    const ir = buildAssetIR(r, {
      assetId: fixtureName, era: 'SYNTHETIC_CONTROL', build: 'GB_1_2_SOURCE_QUALIFIED_FIXTURE',
      container: 'synthetic-controlB', entryName: fx.path, payloadSha256: fixtureSha,
      sizeBytes: bytes.byteLength, adapterVersion: 'pec-test',
    });
    // (a) IR composition (PecTransform law):
    const world = composeWorldTransforms(ir);
    const cam = r.blocks.find((b) => b.type === 'NiCamera');
    const irW = world.get(cam.index);
    // (b) independent THREE.Matrix4 composition from the same parsed TRS:
    const threeWorld = new THREE.Matrix4();
    const chain = [];
    {
      const byIndex = new Map(r.blocks.map((b) => [b.index, b]));
      let cur = cam.index;
      const parentOf = new Map();
      for (const b of r.blocks) for (const c of b.children ?? []) if (c != null && c >= 0) parentOf.set(c, b.index);
      while (cur != null) { chain.unshift(cur); cur = parentOf.get(cur); }
      for (const idx of chain) {
        const b = byIndex.get(idx);
        const local = b.localTrs;
        const m = new THREE.Matrix4();
        m.fromArray(trsToColumnMajor4(local));
        threeWorld.multiply(m);
      }
    }
    const threePos = new THREE.Vector3().setFromMatrixPosition(threeWorld);
    const threeT = [threePos.x, threePos.y, threePos.z];
    const diffIr = irW.translate.map((v, i) => Math.abs(v - fx.expectedWorldTranslate[i]));
    const diffThree = threeT.map((v, i) => Math.abs(v - fx.expectedWorldTranslate[i]));
    const ok = Math.max(...diffIr) <= tol && Math.max(...diffThree) <= tol;
    out.push(record(`T1_${fixtureName}`, `native control comparison (${fixtureName})`, ok ? 'PASS' : 'FAIL', {
      measuredQuantity: 'composed camera world translate (FILE_SCENE_SPACE; parentWorld*local to file root)',
      independentSourceOfTruth: `native GB 1.2 SceneGraphPrinter probe world bound center (phase-1 CONTROLS_B.json): (${fx.expectedWorldTranslate.join(',')})`,
      whyNonCircular: 'IR math (PecTransform) and THREE.Matrix4 math are independent engines; both are compared to a NATIVE-captured value neither produced',
      measured: { irCompose: irW.translate, threeCompose: threeT, fixtureSha256: fixtureSha, cameraBlock: cam.index },
      expected: fx.expectedWorldTranslate,
      perComponentDiff: { ir: diffIr, three: diffThree },
      tolerance: tol,
      failureCaseDetected: ok ? 'none' : 'composed world translate beyond tolerance vs native ground truth',
      threeModule: { modulePath, packageVersion },
    }));
  }

  // ---------------- T2: authored synthetic transform tests ----------------
  // T2a: NON-IDENTITY asset root + child translation.
  // root: T=(10,0,0), R=Rz90, s=3; child mesh: T=(1,2,3), R=I, s=1.
  // Analytic expectation (literal arithmetic in-test):
  //   Rz90*(1,2,3) = (-2,1,3); *3 = (-6,3,9); +(10,0,0) = (4,3,9)
  const rootTrs = trs([10, 0, 0], RZ90, 3);
  const childTrs = trs([1, 2, 3]);
  const irA = makeSyntheticIR({
    assetId: 'SYN_T2A_NONIDENTITY_ROOT',
    blocks: [
      { index: 0, type: 'NiNode', name: 'root', localTrs: rootTrs, children: [1] },
      { index: 1, type: 'NiTriShape', name: 'mesh', localTrs: childTrs, dataRef: 2 },
      { index: 2, type: 'NiTriShapeData', name: 'data', geometry: { positions: [0, 0, 0, 1, 0, 0, 0, 1, 0], indices: [0, 1, 2] } },
    ],
  });
  const worldA = composeWorldTransforms(irA);
  const meshWorldT = worldA.get(1).translate;
  const expectedA = [4, 3, 9]; // hand-computed (see comment above)
  const diffA = meshWorldT.map((v, i) => Math.abs(v - expectedA[i]));
  out.push(record('T2a_nonidentity_root', 'non-identity asset root composition', Math.max(...diffA) <= 1e-9 ? 'PASS' : 'FAIL', {
    measuredQuantity: 'child world translate under a non-identity root (rotation+scale+translation)',
    independentSourceOfTruth: 'literal in-test arithmetic: rootT + rootS*(Rz90*childT) = (10,0,0)+3*(-2,1,3) = (4,3,9)',
    whyNonCircular: 'expected value computed by hand from the composition law, never by calling composeTrs',
    measured: meshWorldT, expected: expectedA, perComponentDiff: diffA, tolerance: 1e-9,
    failureCaseDetected: Math.max(...diffA) <= 1e-9 ? 'none' : 'composition deviates from the analytic law',
  }));

  // T2b: parent rotation + uniform scale + translation (Control-B-mirroring
  // case on authored synthetic data): parent (100,200,300) Rz90 s=2, child
  // (1,2,3) -> world (100,200,300)+2*(-2,1,3) = (96,202,306).
  {
    const irB = makeSyntheticIR({
      assetId: 'SYN_T2B_ROTATED_SCALED_PARENT',
      blocks: [
        { index: 0, type: 'NiNode', name: 'root', localTrs: trs([100, 200, 300], RZ90, 2), children: [1] },
        { index: 1, type: 'NiTriShape', name: 'mesh', localTrs: trs([1, 2, 3]), dataRef: 2 },
        { index: 2, type: 'NiTriShapeData', name: 'data', geometry: { positions: [0, 0, 0, 1, 0, 0, 0, 1, 0], indices: [0, 1, 2] } },
      ],
    });
    const wB = composeWorldTransforms(irB).get(1).translate;
    const expB = [96, 202, 306];
    const diffB = wB.map((v, i) => Math.abs(v - expB[i]));
    out.push(record('T2b_parent_rotate_scale_translate', 'parent rotation + uniform scale + translation', Math.max(...diffB) <= 1e-9 ? 'PASS' : 'FAIL', {
      measuredQuantity: 'child world translate (parent rotate + uniform scale + translation)',
      independentSourceOfTruth: 'literal in-test arithmetic: (100,200,300)+2*(Rz90*(1,2,3))=(96,202,306)',
      whyNonCircular: 'hand-computed expectation; also mirrors the native Control B value for an independent cross-anchor',
      measured: wB, expected: expB, perComponentDiff: diffB, tolerance: 1e-9,
      failureCaseDetected: Math.max(...diffB) <= 1e-9 ? 'none' : 'composition deviates',
    }));
  }

  // T2c: REPARENTING under constant local transform (SetAt semantics: NO
  // local compensation). child (1,2,3): under parentA
  // (100,200,300,Rz90,2) -> (96,202,306); reparent to parentB (0,200,0,I,1)
  // -> (1,202,3). The child's LOCAL TRS must be UNCHANGED by the reparent.
  {
    const irC = makeSyntheticIR({
      assetId: 'SYN_T2C_REPARENT',
      blocks: [
        { index: 0, type: 'NiNode', name: 'root', localTrs: trs([0, 0, 0]), children: [1, 2] },
        { index: 1, type: 'NiNode', name: 'parentA', localTrs: trs([100, 200, 300], RZ90, 2), children: [3] },
        { index: 2, type: 'NiNode', name: 'parentB', localTrs: trs([0, 200, 0]) },
        { index: 3, type: 'NiTriShape', name: 'mesh', localTrs: trs([1, 2, 3]), dataRef: 4 },
        { index: 4, type: 'NiTriShapeData', name: 'data', geometry: { positions: [0, 0, 0, 1, 0, 0, 0, 1, 0], indices: [0, 1, 2] } },
      ],
    });
    const before = composeWorldTransforms(irC).get(3).translate;
    const expBefore = [96, 202, 306];
    // reparent (SetAt: parent rebind only, no local compensation):
    const meshBlock = irC.blocks.find((b) => b.index === 3);
    const localBefore = cloneTrs(meshBlock.localTrs);
    irC.blocks.find((b) => b.index === 1).children = [];
    irC.blocks.find((b) => b.index === 2).children = [3];
    irC.roots = [0];
    const after = composeWorldTransforms(irC).get(3).translate;
    const expAfter = [1, 202, 3];
    const localUnchanged = trsDeepEqual(meshBlock.localTrs, localBefore);
    const okC = before.every((v, i) => Math.abs(v - expBefore[i]) <= 1e-9) &&
      after.every((v, i) => Math.abs(v - expAfter[i]) <= 1e-9) && localUnchanged;
    out.push(record('T2c_reparent_no_compensation', 'reparenting changes world by composition, local TRS unchanged', okC ? 'PASS' : 'FAIL', {
      measuredQuantity: 'child world translate before/after reparent + local TRS identity',
      independentSourceOfTruth: 'literal arithmetic: under A (100,200,300)+2*(Rz90*(1,2,3))=(96,202,306); under B (0,200,0)+(1,2,3)=(1,202,3); GB SetAt performs NO local compensation',
      whyNonCircular: 'expectations hand-computed; the no-compensation behavior is asserted directly (a compensating engine would fail the after-value check)',
      measured: { before, after, localUnchanged },
      expected: { before: expBefore, after: expAfter, localUnchanged: true },
      tolerance: 1e-9,
      failureCaseDetected: okC ? 'none' : 'reparent compensation or wrong composition detected',
    }));
  }

  // T2d: RENDER CONVERSION APPLIED EXACTLY ONCE.
  {
    const pScene = [96, 202, 306];
    const pRender = convertPointSceneToRender(pScene);
    // analytic: (x,z,-y)*0.01 = (0.96, 3.06, -2.02)
    const expRender = [0.96, 3.06, -2.02];
    const doubleConv = convertPointSceneToRender(pRender);
    const diffD = pRender.map((v, i) => Math.abs(v - expRender[i]));
    // structural once-ness: build a render tree and count conversion applications
    let convCount = 0;
    const rm = buildRenderModel(THREE, { ir: irA, worldTransforms: worldA }, {
      conversionCountHook: (n) => { convCount = n; },
    });
    // IR must be UNCHANGED by the render build:
    const irIntact = trsDeepEqual(irA.blocks[0].localTrs, rootTrs) &&
      trsDeepEqual(irA.blocks[1].localTrs, childTrs);
    // full-matrix agreement: THREE world == IR world for the mesh:
    const meshObj = rm.meshObjects[0];
    meshObj.updateWorldMatrix(true, false);
    const wp = new THREE.Vector3().setFromMatrixPosition(meshObj.matrixWorld);
    const irPos = applyTrsPoint(worldA.get(1), [0, 0, 0]);
    const sceneToRender = convertPointSceneToRender(irPos);
    const matrixAgree = Math.abs(wp.x - sceneToRender[0]) < 1e-9 &&
      Math.abs(wp.y - sceneToRender[1]) < 1e-9 &&
      Math.abs(wp.z - sceneToRender[2]) < 1e-9;
    const okD = diffD.every((d) => d <= 1e-12) && convCount === 1 && rm.conversion.appliedOnce &&
      !arraysEqual(pRender, doubleConv) && irIntact && matrixAgree;
    out.push(record('T2d_conversion_once', 'render-axis/unit conversion applied exactly once, originals intact', okD ? 'PASS' : 'FAIL', {
      measuredQuantity: 'converted point + conversion application count + IR intactness + THREE/IR world agreement',
      independentSourceOfTruth: 'analytic conversion (x,z,-y)*0.01; double conversion must differ; the serialized TRS must be unchanged by the render build',
      whyNonCircular: 'the once-ness is asserted structurally (a counter hook counts actual applications) and by negative control (double conversion differs)',
      measured: {
        converted: pRender, doubleConversion: doubleConv, conversionApplications: convCount,
        appliedOnce: rm.conversion.appliedOnce, irIntact,
        threeWorldPos: [wp.x, wp.y, wp.z], irSceneThenConverted: sceneToRender,
        choice: { axisMap: RENDER_ADAPTER_CHOICE.axisMap, unitScale: RENDER_ADAPTER_CHOICE.unitScale, labels: RENDER_ADAPTER_CHOICE.labels },
      },
      expected: { converted: expRender, conversionApplications: 1, appliedOnce: true, irIntact: true, doubleConversionDiffers: true },
      tolerance: 1e-12,
      failureCaseDetected: okD ? 'none' : 'conversion applied zero/multiple times, values mutated, or engines disagree',
    }));
  }

  return out;
}

function arraysEqual(a, b) {
  return a.length === b.length && a.every((v, i) => Math.abs(v - b[i]) < 1e-12);
}
