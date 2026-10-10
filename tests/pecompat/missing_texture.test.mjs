// missing_texture.test.mjs — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// T4 part 2 (plan T6): missing/unknown texture -> labeled UNTEXTURED material
// status + diagnostic, WITHOUT false binding. No cross-era substitutions, no
// guessed IDs, no fabricated container resolution.
//
// MEASURED_QUANTITY: per-mesh binding status + diagnostic records + the
//   material labels produced by the render layer.
// INDEPENDENT_SOURCE_OF_TRUTH: the authored synthetic IR content (which
//   meshes deliberately carry NO texprop / a texprop with NO ArkTexture
//   entries / a valid name binding) — the test knows the truth because it
//   authored it.
// WHY_NON_CIRCULAR: the expected statuses are part of the controlled input
//   design; any binding that was NOT authored (false binding) fails.
// FAILURE_CASE_DETECTED: a falsely-bound mesh, a missing diagnostic, or a
//   claimed container resolution would all be detected.
import {
  makeSyntheticIR, composeWorldTransforms,
} from '../../src/pecompat/PecSceneIR.js';
import { resolveTextureBindings } from '../../src/pecompat/PecAssetAdapter.js';
import { buildRenderModel } from '../../src/pecompat/PecRenderConvert.js';
import { record, trs, loadThree } from './_helpers.mjs';

export async function run(ctx) {
  const out = [];
  const { THREE } = await loadThree();

  // Authored synthetic asset with THREE deliberate binding cases:
  //   mesh 1 "bound"   -> texprop 10 which HAS ArkTexture entries (name bound)
  //   mesh 2 "noentry" -> texprop 11 which has NO ArkTexture entry
  //   mesh 3 "noprop"  -> NO texproperty ref at all
  //   mesh 4 "wrongref"-> property refs point ONLY at a material property
  //                       (must NOT be misread as a texture binding)
  const TRI = { positions: [0, 0, 0, 1, 0, 0, 0, 1, 0], indices: [0, 1, 2] };
  const ir = makeSyntheticIR({
    assetId: 'SYN_T4B_TEXTURE_CASES',
    blocks: [
      { index: 0, type: 'NiNode', name: 'root', children: [1, 2, 3, 4] },
      { index: 1, type: 'NiTriShape', name: 'bound', dataRef: 20, propertyRefs: [10] },
      { index: 2, type: 'NiTriShape', name: 'noentry', dataRef: 21, propertyRefs: [11] },
      { index: 3, type: 'NiTriShape', name: 'noprop', dataRef: 22 },
      { index: 4, type: 'NiTriShape', name: 'wrongref', dataRef: 23, propertyRefs: [12] },
      { index: 10, type: 'NiTexturingProperty', name: 'tex10', fields: { slots: [] } },
      { index: 11, type: 'NiTexturingProperty', name: 'tex11', fields: { slots: [] } },
      { index: 12, type: 'NiMaterialProperty', name: 'matOnly' },
      { index: 5, type: 'NiArkTextureExtraData', name: 'ark', fields: {
        entryCount: 1,
        entries: [
          { entryName: 'SYN_part_0_BASE', f1: 0, f2: -1, texturingPropertyRef: 10, bytes9Hex: '00ffffffff00000000' },
        ],
      } },
      { index: 20, type: 'NiTriShapeData', name: 'd1', geometry: TRI },
      { index: 21, type: 'NiTriShapeData', name: 'd2', geometry: TRI },
      { index: 22, type: 'NiTriShapeData', name: 'd3', geometry: TRI },
      { index: 23, type: 'NiTriShapeData', name: 'd4', geometry: TRI },
    ],
  });
  const bindings = resolveTextureBindings(ir);
  const byMesh = new Map(bindings.map((b) => [b.meshName, b]));
  const bound = byMesh.get('bound');
  const noentry = byMesh.get('noentry');
  const noprop = byMesh.get('noprop');
  const wrongref = byMesh.get('wrongref');

  const checks = {
    boundStatus: bound?.status === 'TEXTURE_NAME_BOUND',
    boundNames: JSON.stringify(bound?.textureNames) === JSON.stringify(['SYN_part_0_BASE']),
    boundContainerUnresolved: bound?.containerResolution?.includes('NOT_ESTABLISHED'),
    noentryStatus: noentry?.status === 'UNTEXTURED_NO_ARK_ENTRY',
    noentryNoFalseBinding: (noentry?.textureNames?.length ?? 0) === 0,
    nopropStatus: noprop?.status === 'UNTEXTURED_NO_TEXPROP',
    wrongrefNotBound: wrongref?.status === 'UNTEXTURED_NO_TEXPROP' && (wrongref?.textureNames?.length ?? 0) === 0,
    diagnosticsRecorded: (ir.diagnostics.unresolvedBindings ?? []).filter((u) => u.class === 'UNTEXTURED_MESH').length === 3,
  };
  const allBoundChecks = Object.values(checks).every(Boolean);

  // render-layer labels: untextured meshes stay viewable with a LABELED plain material
  const rm = buildRenderModel(THREE, { ir, worldTransforms: composeWorldTransforms(ir) }, {});
  // (scene composition not otherwise needed for the material-label check)
  const matLabels = new Map(rm.meshObjects.map((m) => [m.userData.meshName, m.material.userData]));
  const labeledOk = matLabels.get('noprop')?.materialClass?.startsWith('UNTEXTURED_LABELED') &&
    matLabels.get('bound')?.materialClass?.startsWith('PLAIN_LABELED');

  const ok = allBoundChecks && labeledOk;
  out.push(record('T4b_missing_texture_diagnostic', 'missing/unknown texture -> labeled untextured + diagnostic, no false binding', ok ? 'PASS' : 'FAIL', {
    measuredQuantity: 'per-mesh texture binding status + diagnostics + render material labels',
    independentSourceOfTruth: 'the authored synthetic binding design (only mesh "bound" carries an ArkTexture name entry; texprop 11 has none; mesh "wrongref" only references a MATERIAL property)',
    whyNonCircular: 'any status other than the authored truth (including a false binding of "wrongref" to the material block) fails',
    measured: {
      statuses: { bound: bound?.status, noentry: noentry?.status, noprop: noprop?.status, wrongref: wrongref?.status },
      boundNames: bound?.textureNames,
      boundContainerResolution: bound?.containerResolution,
      untexturedDiagnostics: (ir.diagnostics.unresolvedBindings ?? []).filter((u) => u.class === 'UNTEXTURED_MESH'),
      materialLabels: Object.fromEntries([...matLabels.entries()].map(([k, v]) => [k, {
        textureBindingStatus: v.textureBindingStatus, materialClass: v.materialClass,
      }])),
      checks,
    },
    expected: {
      bound: 'TEXTURE_NAME_BOUND (names only; container NOT_ESTABLISHED)',
      noentry: 'UNTEXTURED_NO_ARK_ENTRY',
      noprop: 'UNTEXTURED_NO_TEXPROP',
      wrongref: 'UNTEXTURED_NO_TEXPROP (material property NOT misread as texture)',
      diagnosticsRecorded: 3,
      geometryStillViewable: true,
    },
    failureCaseDetected: ok ? 'none' : 'false binding, missing diagnostic, or claimed container resolution',
  }));

  return out;
}
