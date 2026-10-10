// catalog_cam_fixes.test.mjs — PE_WORLD_LAUNCHER_R1_20261010, Etap A
// FOCUSED QC A (contract §2 + §8; Desktop post-audit §3/§4/§5 CAM-C1/C2/C3).
// The three catalog corrections verified through the REAL production paths:
//
//   CAM_C1 — the GLB comparison tool is EXECUTED fresh (child process, pinned
//            inputs, fail-closed pins) and its measured output is gated.
//   CAM-C2 — the corrected shared status model: FAILED is not a measurement.
//            Coverage recomputed from records through isComplexityMeasured;
//            the 1572 baseline (PCG 1568 + CD 4) is a CONTROL, not a hardcode
//            (the production code contains no 1572 anywhere).
//   CAM-C3 — full cache identity through the REAL production buildCatalogData:
//            three in-memory mutants (wrong batch era, wrong batch
//            containerSha256, wrong edges era — metadata ONLY; the physical
//            caches are proven unchanged by hash) must be REFUSED with named
//            reasons; the clean cache must pass the SAME gate. Plus the
//            fail-closed default: cache paths without a declared envelope are
//            REFUSED whole (catalog still builds; complexity coverage falls
//            back to the four live-decoded CD primaries).
//
// EXPLICIT LIMIT: the CAM-C3 mutants are SYNTHETIC negative controls. They are
// NOT proof of historical contamination of the f71eb30 published run (the
// Desktop audit proved only that the declared fail-closed gate was false).
import { spawn } from 'node:child_process';
import { promises as fsp } from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  buildCatalogData, productionCacheIdentity, complexityFromBatchRow, isComplexityMeasured,
  CATALOG_PINS,
} from '../../tools/pecompat/catalog_data.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(HERE, '..', '..');
const RUN_ID = 'PE_WORLD_LAUNCHER_R1_20261010';
const PRIV_CAM = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_CITY_ASSET_MAP_R1_20261010';
const BATCH_PATH = `${PRIV_CAM}\\PHASE2_EXTENT\\PCG935_NIF10_BATCH_STATE.jsonl`;
const EDGES_PATH = `${PRIV_CAM}\\PHASE3_PCG935_BATCH\\PCG935_NAME_EDGES.jsonl`;
const SUBJECT = '508854.nif'; // the same subject the Desktop post-audit used (DECODED with edge rows)
// Baseline CONTROL values (Desktop post-audit RUNTIME_CHECKS.json on UNCHANGED inputs) —
// used ONLY as test controls; the production code recomputes everything from records.
const CONTROL = Object.freeze({
  rowsTotal: 8088,
  complexityMeasuredBaseline: 1572, // PCG 1568 (1551 DECODED + 17 DECODED_NO_MESH) + CD 4
  complexityUnknownBaseline: 6516,
  failedRows: 3270,
  batchAttached: 4838,
  edgesAttached: 1545,
  byDecodeCoverage: { CATALOG_ONLY: 2488, DECODED_FULL_CLOSURE: 4, FAILED: 3270, DECODED: 1551, VERSION_GATED: 758, DECODED_NO_MESH: 17 },
});

function rec(id, name, status, extra = {}) {
  return { id, name, status, ...extra };
}
const ok = (b) => (b ? 'PASS' : 'FAIL');
const sha256 = (b) => crypto.createHash('sha256').update(b).digest('hex');

/** Run the CAM-C1 comparison tool as a bounded child process (real fresh
 *  execution against the pinned READ_ONLY inputs). */
function runCamC1Tool(tmpDir) {
  return new Promise((resolve, reject) => {
    const jsonOut = path.join(tmpDir, 'CAM_C1_GLB_COMPARE.testrun.json');
    const child = spawn(process.execPath, [
      path.join(REPO_ROOT, 'tools', 'pecompat', 'cam_c1_glb_compare.mjs'), '--json-out', jsonOut,
    ], { cwd: REPO_ROOT, stdio: ['ignore', 'ignore', 'pipe'], windowsHide: true });
    let stderr = '';
    child.stderr.setEncoding('utf8');
    child.stderr.on('data', (d) => { stderr += d; });
    child.on('error', reject);
    child.on('exit', (code) => resolve({ code, stderr, jsonOut }));
  });
}

/** The REAL production buildCatalogData with in-memory cache-metadata mutation
 *  ONLY (mirrors the Desktop control method): the container bytes and SHA
 *  verification remain fully active (memoized byte-identical CONTAINER reads —
 *  the fail-closed pin checks still run on the same bytes in every build).
 *  The CACHE files are never memoized: each build reads them fresh and applies
 *  the requested mutation (a memoized cache copy would silently defeat the
 *  mutant — caught by the first battery run and fixed; recorded in the
 *  intervention ledger). */
async function buildWithMutatedCaches({ batchMut, edgesMut, cacheIdentity, memo }) {
  const readFile = async (p) => {
    const norm = String(p).replaceAll('/', '\\');
    if (norm === BATCH_PATH) {
      let bytes = new Uint8Array(await fsp.readFile(p));
      if (batchMut) {
        const rows = new TextDecoder().decode(bytes).trim().split('\n').map(JSON.parse);
        batchMut(rows);
        bytes = new TextEncoder().encode(rows.map((r) => JSON.stringify(r)).join('\n') + '\n');
      }
      return bytes;
    }
    if (norm === EDGES_PATH) {
      let bytes = new Uint8Array(await fsp.readFile(p));
      if (edgesMut) {
        const rows = new TextDecoder().decode(bytes).trim().split('\n').map(JSON.parse);
        edgesMut(rows);
        bytes = new TextEncoder().encode(rows.map((r) => JSON.stringify(r)).join('\n') + '\n');
      }
      return bytes;
    }
    if (memo.has(norm)) return memo.get(norm);
    const bytes = new Uint8Array(await fsp.readFile(p));
    memo.set(norm, bytes);
    return bytes;
  };
  return buildCatalogData({
    modelsArkPath: CATALOG_PINS.modelsArk.path,
    modelsBntPath: CATALOG_PINS.modelsBnt.path,
    batchStatePath: BATCH_PATH,
    nameEdgesPath: EDGES_PATH,
    cacheIdentity: cacheIdentity === undefined ? productionCacheIdentity() : cacheIdentity,
    io: { readFile, sha256 },
  });
}

export async function run(ctx) {
  const records = [];
  const os = await import('node:os');
  const tmp = await fsp.mkdtemp(path.join(os.tmpdir(), 'opencode', 'pec-camfix-'));
  const memo = new Map(); // byte-identical container memo (the pin checks still run per build)

  // physical cache integrity witness: hash before/after everything
  const batchBefore = sha256(await fsp.readFile(BATCH_PATH));
  const edgesBefore = sha256(await fsp.readFile(EDGES_PATH));

  try {
    // ===================== CAM-C1 (fresh real execution) =====================
    {
      const run = await runCamC1Tool(tmp);
      let parsed = null;
      try { parsed = JSON.parse(await fsp.readFile(run.jsonOut, 'utf8')); } catch { /* gate below */ }
      const models = parsed?.models ?? [];
      const all4 = models.length === 4 && models.every((m) =>
        m.glb.pin.contractPin === 'MATCH' && m.nif.payloadPin.contractPin === 'MATCH');
      const posExact = models.filter((m) => m.comparison.positionsMultisetExact).length;
      const triExact = models.filter((m) => m.comparison.trianglesUnorientedMultisetExact).length;
      const countOk = models.every((m) => m.comparison.vertexCountAgreement && m.comparison.triangleCountAgreement);
      const uvZero = models.every((m) => m.nif.uvSetsTotal === 0);
      const imagesZero = models.every((m) => m.glb.images === 0);
      records.push(rec('CAM_C1_GLB_COMPARISON', 'CAM-C1: the four GLB comparison inputs exist (RETRACTION of NO_GLB_PRESENT_FOR_THESE_IDS) — the comparison tool executes fresh on the pinned inputs; 4/4 bit-exact position multisets + unoriented triangle multisets after the EXPLICIT (x,z,-y) conversion; UNTEXTURED_PROXY limits recorded', ok(
        run.code === 0 && all4 && posExact === 4 && triExact === 4 && countOk && uvZero && imagesZero,
      ), {
        measuredQuantity: 'fresh tool execution: per-model converted-position multiset + unoriented-triangle multiset equality (bit-exact float32), counts, UV/images census',
        measured: {
          toolExit: run.code,
          models: models.length,
          positionsExact: posExact,
          trianglesUnorientedExact: triExact,
          countsAgree: countOk,
          originalUvSetsTotal: parsed?.summary?.originalUvSetsTotal ?? null,
          glbImagesTotal: parsed?.summary?.glbImagesTotal ?? null,
          perModel: models.map((m) => ({ id: m.id, verdict: m.verdict, nif: { geoms: m.nif.geometries, verts: m.nif.vertices, tris: m.nif.triangles }, glb: { prims: m.glb.primitives, verts: m.glb.vertices, tris: m.glb.triangles } })),
        },
        independentSourceOfTruth: 'my own re-decode from the pinned Models.ark payloads (phase-3 production reader) vs an independent bounded GLB binary parse — two independent readers of the same assets',
        whyNonCircular: 'the GLB parser shares no code with the NIF reader; agreement cannot come from a shared implementation',
        failureCaseDetected: (run.code !== 0 || posExact !== 4 || triExact !== 4) ? 'the geometry comparison did not reproduce (finding — reported, never massaged)' : 'none',
        limits: [
          'Unoriented triangle agreement does NOT confirm winding, materials, or the converter execution lineage.',
          'The _textured.glb filename is NOT proof of textures; the ORIGINAL NIFs have 0 UV sets; the four models remain UNTEXTURED_PROXY.',
          'GLB TEXCOORD_0/NORMAL are exporter-side artifacts; GLB images total 0 (measured).',
        ],
      }));
    }

    // =============== CAM-C2: shared status model (unit-level) ===============
    {
      const failedRow = { status: 'FAILED', error: '[PecNif10Reader] block 8: UNKNOWN type "NiTextureEffect" — LOUD FAIL' };
      const cFailed = complexityFromBatchRow(failedRow);
      const decodedIncomplete = { status: 'DECODED', triangles: 10, vertices: null, shapeCount: 2, nodeCount: 1, blockCount: 9 };
      const cIncomplete = complexityFromBatchRow(decodedIncomplete);
      const noMesh = { status: 'DECODED_NO_MESH_GEOMETRY', triangles: 0, vertices: 0, shapeCount: 0, nodeCount: 1, blockCount: 5 };
      const cNoMesh = complexityFromBatchRow(noMesh);
      const decoded = { status: 'DECODED', triangles: 120, vertices: 240, shapeCount: 2, nodeCount: 3, blockCount: 12 };
      const cDecoded = complexityFromBatchRow(decoded);
      const cGated = complexityFromBatchRow(null);
      const allOk =
        cFailed.unknown === true && !isComplexityMeasured(cFailed) && /decode FAILED/.test(cFailed.note ?? '') &&
        cIncomplete.unknown === true && !isComplexityMeasured(cIncomplete) &&
        cNoMesh.unknown === false && isComplexityMeasured(cNoMesh) && cNoMesh.triangles === 0 && cNoMesh.vertices === 0 &&
        cDecoded.unknown === false && isComplexityMeasured(cDecoded) && cDecoded.triangles === 120 &&
        cGated.unknown === true && !isComplexityMeasured(cGated);
      records.push(rec('CAM_C2_SHARED_STATUS_MODEL', 'CAM-C2 unit: complexityFromBatchRow/isComplexityMeasured — FAILED → UNKNOWN with reason; incomplete numerics → UNKNOWN (no promotion); DECODED_NO_MESH real zeros → measured; DECODED complete → measured; no row → UNKNOWN', ok(allOk), {
        measuredQuantity: 'complexityFromBatchRow outputs on synthetic cache rows + isComplexityMeasured verdicts',
        measured: { cFailed, cIncomplete, cNoMesh, cDecoded, cGated },
        failureCaseDetected: allOk ? 'none' : 'the shared status model promoted a non-measurement (defect)',
      }));
    }

    // =============== CAM-C2 + CAM-C3 clean: the REAL production build ===============
    let clean = null;
    {
      clean = await buildWithMutatedCaches({ memo });
      const cov = clean.coverage;
      const batch = clean.cache.batchState;
      const edges = clean.cache.nameEdges;
      const failedRows = clean.rows.filter((r) => r.decodeCoverage === 'FAILED');
      const failedUnknownComplexity = failedRows.every((r) => r.complexity.unknown === true && r.complexity.triangles == null && r.complexity.vertices == null);
      const failedTextureHonest = failedRows.every((r) => /^UNKNOWN \(decode FAILED/.test(r.textureCoverage));
      const noDecodedButWording = failedRows.every((r) => !/decoded but/.test(r.textureCoverage));
      const subjectRow = clean.rows.find((r) => r.entryName === SUBJECT);
      const cleanOk =
        cov.totalRows === CONTROL.rowsTotal &&
        cov.complexity.measured === CONTROL.complexityMeasuredBaseline &&
        cov.complexity.unknown === CONTROL.complexityUnknownBaseline &&
        cov.byDecodeCoverage.FAILED === CONTROL.failedRows &&
        cov.complexity.measuredByStatus.DECODED_FULL_CLOSURE === 4 &&
        cov.complexity.measuredByStatus.DECODED === 1551 &&
        cov.complexity.measuredByStatus.DECODED_NO_MESH === 17 &&
        batch.envelope.state === 'VERIFIED' && batch.attached === CONTROL.batchAttached && batch.droppedIdentityMismatch === 0 &&
        edges.envelope.state === 'VERIFIED' && edges.modelsAttached === CONTROL.edgesAttached && edges.modelsDroppedIdentityMismatch === 0 &&
        failedRows.length === CONTROL.failedRows && failedUnknownComplexity && failedTextureHonest && noDecodedButWording &&
        subjectRow.decodeCoverage === 'DECODED' && !subjectRow.sceneExtent.unknown && isComplexityMeasured(subjectRow.complexity) &&
        /MATERIAL_REFERENCE_CONFIRMED=/.test(subjectRow.textureCoverage);
      records.push(rec('CAM_C2_C3_CLEAN_BASELINE', 'CAM-C2/CAM-C3 clean gate: the REAL production build with the declared envelope — measured complexity 1572 (BASELINE CONTROL: PCG 1568 + CD 4; recomputed from records via the shared predicate, NOT hardcoded in production code); FAILED 3270 rows are UNKNOWN-complexity with honest texture wording; caches attach with the known-good counts and zero identity drops', ok(cleanOk), {
        measuredQuantity: 'coverage counts + cache attach counters + FAILED row schema on the unchanged pinned inputs',
        measured: {
          totalRows: cov.totalRows,
          complexityMeasured: cov.complexity.measured,
          complexityUnknown: cov.complexity.unknown,
          complexityByStatus: cov.complexity.measuredByStatus,
          baselineControl: { measured: CONTROL.complexityMeasuredBaseline, pCG: 1568, cD: 4 },
          byDecodeCoverage: cov.byDecodeCoverage,
          batchState: { state: batch.envelope.state, attached: batch.attached, dropped: batch.droppedIdentityMismatch },
          nameEdges: { state: edges.envelope.state, attached: edges.modelsAttached, dropped: edges.modelsDroppedIdentityMismatch },
          failedRows: failedRows.length,
          failedUnknownComplexity,
          failedTextureCoverageSample: failedRows[0]?.textureCoverage,
          subject: { name: SUBJECT, decodeCoverage: subjectRow.decodeCoverage, extentUnknown: subjectRow.sceneExtent.unknown, complexityMeasured: isComplexityMeasured(subjectRow.complexity) },
        },
        independentSourceOfTruth: 'the Desktop post-audit RUNTIME_CHECKS.json baseline numbers (4842→1572, 3270 FAILED) as a CONTROL',
        whyNonCircular: 'the baseline is an independent prior measurement; my build recomputes the counts from the records without reading the Desktop numbers',
        failureCaseDetected: cleanOk ? 'none' : 'the corrected coverage/cache numbers disagree with the registered baseline control (finding — reported as measured)',
      }));
    }

    // =============== CAM-C3 M1: wrong batch era (through the REAL gate) ===============
    {
      const data = await buildWithMutatedCaches({
        memo,
        batchMut: (rows) => { const r = rows.find((x) => x.name === SUBJECT); r.era = 'CD_2003'; },
      });
      const batch = data.cache.batchState;
      const subjectRow = data.rows.find((r) => r.entryName === SUBJECT);
      const dropReasons = Object.keys(batch.droppedByReason ?? {});
      const refusedOk =
        batch.attached === CONTROL.batchAttached - 1 &&
        batch.droppedIdentityMismatch === 1 &&
        dropReasons.some((r) => r.startsWith('ROW_ERA_MISMATCH')) &&
        subjectRow.decodeCoverage === 'VERSION_GATED' &&
        subjectRow.sceneExtent.unknown === true &&
        !isComplexityMeasured(subjectRow.complexity) &&
        data.coverage.complexity.measured === CONTROL.complexityMeasuredBaseline - 1; // the subject's measured metrics refused
      records.push(rec('CAM_C3_M1_WRONG_BATCH_ERA', 'CAM-C3 mutant 1: subject batch row era → CD_2003 — REFUSED by the production gate (named drop, counted; the subject falls back to VERSION_GATED/UNKNOWN; no crash)', ok(refusedOk), {
        measuredQuantity: 'per-row identity drop reason + affected row state + counters',
        measured: {
          attached: batch.attached, dropped: batch.droppedIdentityMismatch, droppedByReason: batch.droppedByReason,
          subjectAfter: { decodeCoverage: subjectRow.decodeCoverage, extentUnknown: subjectRow.sceneExtent.unknown, complexityUnknown: subjectRow.complexity.unknown },
          complexityMeasured: data.coverage.complexity.measured,
        },
        failureCaseDetected: refusedOk ? 'none — the gate refused the mutant row' : 'the wrong-era row was ACCEPTED (CAM-C3 defect — the f71eb30 behavior)',
      }));
    }

    // =============== CAM-C3 M2: wrong batch containerSha256 (through the REAL gate) ===============
    {
      const data = await buildWithMutatedCaches({
        memo,
        batchMut: (rows) => { const r = rows.find((x) => x.name === SUBJECT); r.containerSha256 = '0'.repeat(64); },
      });
      const batch = data.cache.batchState;
      const subjectRow = data.rows.find((r) => r.entryName === SUBJECT);
      const dropReasons = Object.keys(batch.droppedByReason ?? {});
      const refusedOk =
        batch.attached === CONTROL.batchAttached - 1 &&
        batch.droppedIdentityMismatch === 1 &&
        dropReasons.some((r) => r.startsWith('ROW_CONTAINER_SHA_MISMATCH')) &&
        subjectRow.decodeCoverage === 'VERSION_GATED' && subjectRow.sceneExtent.unknown === true;
      records.push(rec('CAM_C3_M2_WRONG_BATCH_CONTAINER_SHA', 'CAM-C3 mutant 2: subject batch row containerSha256 → 64 zeros — REFUSED by the production gate (named drop, counted)', ok(refusedOk), {
        measuredQuantity: 'per-row identity drop reason + affected row state + counters',
        measured: {
          attached: batch.attached, dropped: batch.droppedIdentityMismatch, droppedByReason: batch.droppedByReason,
          subjectAfter: { decodeCoverage: subjectRow.decodeCoverage, extentUnknown: subjectRow.sceneExtent.unknown },
        },
        failureCaseDetected: refusedOk ? 'none — the gate refused the mutant row' : 'the wrong-container row was ACCEPTED (CAM-C3 defect)',
      }));
    }

    // =============== CAM-C3 M3: wrong edges era (through the REAL gate) ===============
    {
      const data = await buildWithMutatedCaches({
        memo,
        edgesMut: (rows) => { for (const e of rows) if (e.model === SUBJECT) e.era = 'CD_2003'; },
      });
      const edges = data.cache.nameEdges;
      const batch = data.cache.batchState;
      const subjectRow = data.rows.find((r) => r.entryName === SUBJECT);
      const dropReasons = Object.keys(edges.droppedByReason ?? {});
      const refusedOk =
        edges.modelsAttached === CONTROL.edgesAttached - 1 &&
        edges.modelsDroppedIdentityMismatch === 1 &&
        dropReasons.some((r) => r.startsWith('EDGE_ERA_MISMATCH')) &&
        /EDGE_AGGREGATE_REFUSED/.test(subjectRow.textureCoverage) &&
        // the DECODE itself is unaffected — only the edge aggregate is refused
        batch.attached === CONTROL.batchAttached &&
        subjectRow.decodeCoverage === 'DECODED' && !subjectRow.sceneExtent.unknown && isComplexityMeasured(subjectRow.complexity) &&
        data.coverage.complexity.measured === CONTROL.complexityMeasuredBaseline;
      records.push(rec('CAM_C3_M3_WRONG_EDGES_ERA', 'CAM-C3 mutant 3: all texture edges of the subject → CD_2003 — the per-model aggregate is REFUSED (all-or-nothing; the model reads EDGE_AGGREGATE_REFUSED, never a name-edge census; the DECODED extent/complexity stay attached — only the contaminated aggregate is refused)', ok(refusedOk), {
        measuredQuantity: 'per-model edge-aggregate refusal + row texture coverage + unaffected batch state',
        measured: {
          modelsAttached: edges.modelsAttached, modelsDropped: edges.modelsDroppedIdentityMismatch, droppedByReason: edges.droppedByReason,
          subjectTextureCoverage: subjectRow.textureCoverage,
          subjectDecodeUnaffected: { decodeCoverage: subjectRow.decodeCoverage, extentUnknown: subjectRow.sceneExtent.unknown, complexityMeasured: isComplexityMeasured(subjectRow.complexity) },
          batchAttachedUnaffected: batch.attached,
        },
        failureCaseDetected: refusedOk ? 'none — the gate refused the contaminated aggregate' : 'the wrong-era edge aggregate was ACCEPTED (CAM-C3 defect)',
      }));
    }

    // =============== CAM-C3 fail-closed default: no declared envelope ===============
    {
      const data = await buildWithMutatedCaches({ cacheIdentity: null, memo });
      const batch = data.cache.batchState;
      const edges = data.cache.nameEdges;
      const refusedOk =
        /REFUSED: CACHE_IDENTITY_ENVELOPE_MISSING/.test(batch.envelope.state) &&
        /REFUSED: CACHE_IDENTITY_ENVELOPE_MISSING/.test(edges.envelope.state) &&
        batch.attached === 0 && edges.modelsAttached === 0 &&
        data.coverage.totalRows === CONTROL.rowsTotal && // the catalog itself still builds from the pinned originals
        data.coverage.complexity.measured === 4; // only the four live-decoded CD primaries remain measured
      records.push(rec('CAM_C3_NO_ENVELOPE_REFUSED', 'CAM-C3 fail-closed default: cache paths WITHOUT a declared identity envelope are REFUSED whole (named reason, disclosed in the status; the catalog still regenerates from the pinned originals — complexity coverage falls to the four live-decoded primaries; never a crash, never a silent attach)', ok(refusedOk), {
        measuredQuantity: 'cache refusal states + fallback coverage',
        measured: {
          batchState: batch.envelope.state, nameEdgesState: edges.envelope.state,
          batchAttached: batch.attached, edgesAttached: edges.modelsAttached,
          complexityMeasuredFallback: data.coverage.complexity.measured,
        },
        failureCaseDetected: refusedOk ? 'none — the undeclared cache was refused loudly' : 'an undeclared cache was attached or the build crashed (defect)',
      }));
    }

    // =============== physical caches unchanged (witness) ===============
    {
      const batchAfter = sha256(await fsp.readFile(BATCH_PATH));
      const edgesAfter = sha256(await fsp.readFile(EDGES_PATH));
      const unchanged = batchAfter === batchBefore && edgesAfter === edgesBefore;
      records.push(rec('CAM_C3_PHYSICAL_CACHES_UNCHANGED', 'CAM-C3 mutants are IN-MEMORY metadata mutations ONLY — the physical cache files are byte-identical before/after (hash witness). These synthetic counterexamples are NOT proof of historical contamination of the f71eb30 run.', ok(unchanged), {
        measuredQuantity: 'SHA256 of both physical cache files before/after the whole suite',
        measured: { batchBefore, batchAfter, edgesBefore, edgesAfter },
        failureCaseDetected: unchanged ? 'none' : 'a physical cache file changed (VIOLATION)',
      }));
    }
  } finally {
    await fsp.rm(tmp, { recursive: true, force: true }).catch(() => {});
  }
  return records;
}
