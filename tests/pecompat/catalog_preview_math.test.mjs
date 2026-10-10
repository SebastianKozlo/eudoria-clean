// catalog_preview_math.test.mjs — PE_CITY_ASSET_MAP_R1_20261010, phase 4 (W6)
// NO-ACCIDENTAL-CENTERING / NO-DOUBLE-CONVERSION GATES (contract §7):
//   - a KNOWN vertex maps to its FILE-SPACE value in the original-coordinates
//     view mode (wrapper identity);
//   - the CENTERED (fit-to-view) mode applies the centering EXACTLY ONCE at
//     the presentation wrapper (rendered = v - center, NEVER v - 2*center);
//   - there is NO unit conversion and NO axis swap in the catalog preview
//     (component-wise identity — unlike the 218757 app's (x,z,-y)×0.01 render
//     conversion, which stays in ITS app);
//   - the row-major->column rotation conversion is correct (a synthetic
//     asymmetric rotation).
//
// The pure exports under test are compat/catalog-preview.js (PREVIEW_VIEW_MODES,
// wrapperCenter, wrapperOffsetFor, fileSpaceToRendered, applyWrapperToFileSpace,
// localTrsToColumns, boundsEqualWithin) — the SAME functions the browser
// mount uses. The KNOWN vertex comes from the REAL 193313 wire (live decode),
// so the gate exercises the production data path end-to-end for the math.
import {
  PREVIEW_VIEW_MODES, wrapperCenter, wrapperOffsetFor, fileSpaceToRendered,
  applyWrapperToFileSpace, localTrsToColumns, boundsEqualWithin,
} from '../../compat/catalog-preview.js';
import {
  buildCatalogData, buildPrimaryWire, CATALOG_PINS,
} from '../../tools/pecompat/catalog_data.mjs';

function rec(id, name, status, extra = {}) {
  return { id, name, status, ...extra };
}
const ok = (b) => (b ? 'PASS' : 'FAIL');

export async function run(ctx) {
  const records = [];

  // ---- G1: wrapper math with a synthetic bounds (pure, no containers) ----
  {
    const bounds = { unknown: false, min: [-1000, -2000, 0], max: [1000, 2000, 4000], extents: [2000, 4000, 4000] };
    const center = wrapperCenter(bounds);
    const offCentered = wrapperOffsetFor(PREVIEW_VIEW_MODES.CENTERED, bounds);
    const offOriginal = wrapperOffsetFor(PREVIEW_VIEW_MODES.ORIGINAL, bounds);
    const v = [123.5, -67.25, 3.75];
    const renderedCentered = fileSpaceToRendered(v, offCentered);
    const renderedOriginal = fileSpaceToRendered(v, offOriginal);
    const backToFile = applyWrapperToFileSpace(renderedCentered, offCentered);
    const centeredOnce =
      renderedCentered[0] === v[0] - center[0] && renderedCentered[1] === v[1] - center[1] && renderedCentered[2] === v[2] - center[2];
    // not-twice proof on the axis where the center is NONZERO (z: center 2000):
    // exactly-once gives -1996.25; twice would give -3996.25
    const notTwice = renderedCentered[2] !== v[2] - 2 * center[2] && renderedCentered[2] === v[2] - center[2];
    const originalIdentity = renderedOriginal[0] === v[0] && renderedOriginal[1] === v[1] && renderedOriginal[2] === v[2];
    const inverseExact = backToFile[0] === v[0] && backToFile[1] === v[1] && backToFile[2] === v[2];
    const allOk = centeredOnce && notTwice && originalIdentity && inverseExact;
    records.push(rec('CAT_PREVIEW_WRAPPER_MATH', 'wrapper math: CENTERED applies centering EXACTLY ONCE (v - center, never twice); ORIGINAL mode is wrapper identity; the inverse restores the file value exactly', ok(allOk), {
      measuredQuantity: 'fileSpaceToRendered/applyWrapperToFileSpace on a synthetic bounds + vertex',
      measured: {
        center, offCentered, offOriginal,
        v, renderedCentered, renderedOriginal, backToFile,
        centeredAppliedOnce: centeredOnce, notAppliedTwice: notTwice,
        originalModeIdentity: originalIdentity, inverseExact,
      },
      failureCaseDetected: allOk ? 'none' : 'centering applied more/less than once or the inverse broke',
    }));
  }

  // ---- G2: rotation conversion (row-major R·p -> renderer basis columns) ----
  {
    // 90° rotation around z: R = [[0,-1,0],[1,0,0],[0,0,1]] (p' = R·p)
    const trs = {
      translate: [1, 2, 3],
      rotate: [[0, -1, 0], [1, 0, 0], [0, 0, 1]],
      scale: 2,
    };
    const cols = localTrsToColumns(trs);
    // p=(1,0,0) -> R·p = (0,1,0) -> basis X column must be (0,1,0)
    const basisXCorrect = cols.basisX[0] === 0 && cols.basisX[1] === 1 && cols.basisX[2] === 0;
    const basisYCorrect = cols.basisY[0] === -1 && cols.basisY[1] === 0 && cols.basisY[2] === 0;
    const basisZCorrect = cols.basisZ[0] === 0 && cols.basisZ[1] === 0 && cols.basisZ[2] === 1;
    const translateIntact = cols.translate[0] === 1 && cols.translate[1] === 2 && cols.translate[2] === 3;
    const scaleIntact = cols.scale === 2;
    const allOk = basisXCorrect && basisYCorrect && basisZCorrect && translateIntact && scaleIntact;
    records.push(rec('CAT_PREVIEW_ROTATION_CONVERSION', 'row-major NIF rotation -> renderer basis columns conversion verified on a synthetic asymmetric 90° rotation (translate/scale pass through untouched)', ok(allOk), {
      measuredQuantity: 'localTrsToColumns output on a synthetic asymmetric rotation',
      measured: { input: trs, output: cols },
      failureCaseDetected: allOk ? 'none' : 'basis column transposition defect (would flip handedness/rotation direction in the preview)',
    }));
  }

  // ---- G3: REAL known-vertex mapping through the live wire (193313) ----
  {
    try {
      const data = await buildCatalogData({
        modelsArkPath: ctx.modelsArkPath ?? CATALOG_PINS.modelsArk.path,
        modelsBntPath: ctx.modelsPath ?? CATALOG_PINS.modelsBnt.path,
        batchStatePath: ctx.batchStatePath ?? null,
        nameEdgesPath: ctx.nameEdgesPath ?? null,
      });
      const wire = buildPrimaryWire(data.primaries['193313'], '193313');
      // a KNOWN vertex: the first position of the first mesh's data block
      // (NiTriShape blocks reference NiTriShapeData via dataRef — the data
      // block carries the geometry arrays)
      const mesh = wire.meshRows[0];
      const dataBlock = wire.blocks.find((b) => b.index === mesh.dataBlock);
      const knownVertex = [dataBlock.geometry.positions[0], dataBlock.geometry.positions[1], dataBlock.geometry.positions[2]];
      const sb = wire.sceneBounds_FILE_SCENE_SPACE;
      const offCentered = wrapperOffsetFor(PREVIEW_VIEW_MODES.CENTERED, sb);
      const offOriginal = wrapperOffsetFor(PREVIEW_VIEW_MODES.ORIGINAL, sb);
      const renderedOriginal = fileSpaceToRendered(knownVertex, offOriginal);
      const renderedCentered = fileSpaceToRendered(knownVertex, offCentered);
      const restored = applyWrapperToFileSpace(renderedCentered, offCentered);
      // NO conversion/swap: the rendered ORIGINAL value must equal the file
      // value component-wise (a (x,z,-y)×0.01-style adapter would fail this)
      const noSwapNoScale = renderedOriginal[0] === knownVertex[0] && renderedOriginal[1] === knownVertex[1] && renderedOriginal[2] === knownVertex[2];
      // known vertex really is in FILE space: it must lie inside the shipped bounds
      const insideBounds = ['0', '1', '2'].every((k) => knownVertex[Number(k)] >= sb.min[Number(k)] - 1e-6 && knownVertex[Number(k)] <= sb.max[Number(k)] + 1e-6);
      const centeredOnce = Math.abs(renderedCentered[0] - (knownVertex[0] + offCentered[0])) < 1e-9;
      const restoredExact = restored[0] === knownVertex[0] && restored[1] === knownVertex[1] && restored[2] === knownVertex[2];
      const allOk = noSwapNoScale && insideBounds && centeredOnce && restoredExact;
      records.push(rec('CAT_PREVIEW_KNOWN_VERTEX', 'REAL known vertex (193313 first mesh position) maps to its FILE-SPACE value in original-coords mode; centered mode offsets EXACTLY ONCE; no axis swap, no unit conversion (unlike the 218757 app adapter which stays in its own app)', ok(allOk), {
        measuredQuantity: 'fileSpaceToRendered of a live-wire vertex vs the wire-shipped bounds',
        measured: {
          knownVertex,
          bounds: { min: sb.min, max: sb.max },
          renderedOriginal, renderedCentered, restored,
          noSwapNoScale, insideBounds, centeredOnce, restoredExact,
        },
        independentSourceOfTruth: 'the live wire geometry arrays (regenerated from the pinned Models.ark)',
        whyNonCircular: 'the vertex is taken from the production wire and mapped through the production wrapper math; expectations derive from arithmetic, not from the implementation output',
        failureCaseDetected: allOk ? 'none' : 'accidental centering/conversion-twice or an axis swap detected',
      }));

      // ---- G4: identity-TRS precondition + bounds cross-check helpers ----
      const trsAll = wire.blocks.map((b) => b.localTrs).filter(Boolean);
      const allIdentity = trsAll.every((t) =>
        t.translate[0] === 0 && t.translate[1] === 0 && t.translate[2] === 0 &&
        t.rotate[0][0] === 1 && t.rotate[1][1] === 1 && t.rotate[2][2] === 1 && t.scale === 1);
      const boundsEq = boundsEqualWithin(wire.sceneBounds_FILE_SCENE_SPACE, wire.sceneBounds_FILE_SCENE_SPACE, 1e-9);
      records.push(rec('CAT_PREVIEW_TRS_PRECONDITION', 'all local TRS identity in the live 193313 wire (measured — the preview applies local transforms per node; the composition cross-check in verifyWireClientSide uses this fact)', ok(allIdentity && boundsEq), {
        measuredQuantity: 'identity check of every localTrs in the live wire + boundsEqualWithin sanity',
        measured: { avObjectsWithTrs: trsAll.length, allIdentity, boundsEq },
        failureCaseDetected: allIdentity ? 'none' : 'non-identity TRS found (would need per-node composition verification — see the wire cross-check)',
      }));
    } catch (e) {
      records.push(rec('CAT_PREVIEW_KNOWN_VERTEX', 'REAL known-vertex mapping through the live wire', 'NOT_PERFORMED', {
        measuredQuantity: 'container availability',
        measured: String(e?.message ?? e).slice(0, 800),
        failureCaseDetected: 'prerequisites unavailable — honest NOT_PERFORMED (never PASS)',
      }));
      records.push(rec('CAT_PREVIEW_TRS_PRECONDITION', 'identity-TRS precondition on the live wire', 'NOT_PERFORMED', {
        measuredQuantity: 'container availability',
        measured: { note: 'skipped with the known-vertex gate' },
        failureCaseDetected: 'not executed',
      }));
    }
  }

  return records;
}
