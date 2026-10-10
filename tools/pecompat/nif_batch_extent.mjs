// nif_batch_extent.mjs — PE_CITY_ASSET_MAP_R1_20261010, phase 2 (W2, contract §2)
// Bounded BATCH decode of the PCG_9_3_5 Models.bnt NIF 10.1.0.0 entries for
// the SCENE_EXTENT and COMPLEXITY rankings. NO parser expansion happens here:
// the existing era-validated reader chain is used AS IS, failures are
// recorded per entry and the batch continues (contract §2: the first
// systematic parser error does NOT trigger unlimited parser repair).
//
// REUSE LABELS (documented parser lineage — imported unchanged):
//   - src/pesource/Bnt2Archive.js — BNT2 framing (Models.bnt, pin verified).
//   - src/pecompat/PecNif10Reader.js — the era-validated NIF 10.1.0.0 reader
//     (strict version gate, full-file closure contract, LOUD failures).
//   - src/pecompat/PecSceneIR.js — buildAssetIR / validateSceneGraph /
//     composeWorldTransforms / computeSceneBounds (FILE_SCENE_SPACE AABB:
//     world = parentWorld * local from serialized TRS; NO axis swap, NO unit
//     conversion; NOT a PE world position).
//
// MEASURED per entry: composed-hierarchy AABB (min/max/extents in the file's
// own axis labels x/y/z — axis SEMANTICS like up-axis are NOT established;
// units are ORIGINAL file units, never called meters), max-axis extent,
// footprint (x,z extents), meshCount, triangles/vertices/shapes/nodes counts,
// elapsed ms. Models without mesh geometry get extents UNKNOWN (never 0).
//
// RESUME/BOUNDS: state is a JSONL file appended per completed entry;
// --start/--limit allow chunked bounded runs; a killed chunk resumes cleanly.
//
// OUTPUT: JSONL state + summary JSON → PRIVATE_OUTPUT only. Full ranking
// tables are built from the state by catalog_rankings.mjs.

import fs from 'node:fs';
import crypto from 'node:crypto';
import { Bnt2Archive } from '../../src/pesource/Bnt2Archive.js';
import { readNif10, PEC_NIF10_READER_VERSION } from '../../src/pecompat/PecNif10Reader.js';
import { buildAssetIR, composeWorldTransforms, computeSceneBounds, PEC_SCENEIR_SCHEMA_VERSION } from '../../src/pecompat/PecSceneIR.js';
import { sniffPayload } from './catalog_sniff.mjs';

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) args[key] = true;
      else { args[key] = next; i++; }
    }
  }
  return args;
}

function classifyError(msg) {
  const m = String(msg);
  if (m.includes('UNKNOWN type') || m.includes('no parser registered')) return 'UNKNOWN_BLOCK_TYPE_NO_PARSER';
  if (m.includes('CLOSURE_FAIL')) return 'CLOSURE_FAIL';
  if (m.includes('read(') || m.includes('exceeds size')) return 'STREAM_OVERRUN';
  if (m.includes('scene graph invalid') || m.includes('DANGLING_') || m.includes('CYCLE')) return 'SCENE_GRAPH_INVALID';
  if (m.includes('VERSION')) return 'VERSION_GATE';
  if (m.includes('did not reach')) return 'UNREACHABLE_BLOCKS';
  return 'OTHER';
}

async function main() {
  const args = parseArgs(process.argv);
  const bntPath = args.models;
  const statePath = args.state;
  const summaryPath = args.summary;
  const expectSha = args['expect-sha'];
  const expectSize = args['expect-size'] ? parseInt(args['expect-size'], 10) : null;
  const start = args.start ? parseInt(args.start, 10) : 0;
  const limit = args.limit ? parseInt(args.limit, 10) : Infinity;
  if (!bntPath || !statePath || !summaryPath) throw new Error('--models <Models.bnt> --state <jsonl> --summary <json> required');

  const t0 = Date.now();
  const buf = fs.readFileSync(bntPath);
  const bytes = new Uint8Array(buf);
  const containerSha = crypto.createHash('sha256').update(bytes).digest('hex');
  if (expectSize != null && bytes.length !== expectSize) {
    throw new Error(`[nif_batch_extent] container size ${bytes.length} != expected ${expectSize} — BLOCKED`);
  }
  if (expectSha && containerSha !== expectSha.toLowerCase()) {
    throw new Error(`[nif_batch_extent] container SHA256 ${containerSha} != expected — BLOCKED`);
  }
  const arch = new Bnt2Archive(bytes);
  const entries = arch.entries();

  // candidates: NIF 10.1.0.0 by header sniff (the reader's strict version gate
  // re-verifies per file — the sniff is only the candidate selector)
  const candidates = [];
  for (const e of entries) {
    const { payload } = arch.readEntry(e);
    const s = sniffPayload(payload);
    if (s.sniffClass === 'NIF' && s.nifVersion === '10.1.0.0') candidates.push(e);
  }

  // resume: which ordinals already in state?
  const doneOrdinals = new Set();
  if (fs.existsSync(statePath)) {
    for (const line of fs.readFileSync(statePath, 'utf8').split('\n')) {
      if (!line.trim()) continue;
      try { doneOrdinals.add(JSON.parse(line).entryIndex); } catch { /* torn tail line from a kill — ignored, the entry reruns */ }
    }
  }

  const todo = candidates.filter((e) => !doneOrdinals.has(e.entryIndex)).slice(start, start + limit);
  let decoded = 0, failed = 0, noMesh = 0;
  const errorClasses = new Map();
  const errorSamples = new Map();
  let maxFileMs = 0, sumFileMs = 0;

  for (const e of todo) {
    const ft0 = Date.now();
    const { payload } = arch.readEntry(e);
    const payloadSha256 = crypto.createHash('sha256').update(payload).digest('hex');
    const row = {
      era: 'PCG_9_3_5',
      entryIndex: e.entryIndex,
      name: e.name,
      entryOffset: e.offset,
      sizeBytes: e.size,
      payloadSha256,
      readerVersion: PEC_NIF10_READER_VERSION,
      schemaVersion: PEC_SCENEIR_SCHEMA_VERSION,
      status: null, error: null, errorClass: null,
      elapsedMs: null,
      space: 'FILE_SCENE_SPACE',
      axisConvention: 'file-serialized x/y/z labels, NO axis swap, NO unit conversion (axis semantics e.g. up-axis NOT established; units are original file units, never meters)',
    };
    try {
      const r = readNif10(payload, { sourceName: e.name });
      const ir = buildAssetIR(r, {
        assetId: parseInt(e.name.replace(/\.nif$/i, ''), 10) || e.name,
        era: 'PCG_9_3_5',
        build: 'PCG_9_3_5_Models_bnt_entry_batch',
        container: 'Models/Models.bnt',
        entryName: e.name,
        payloadSha256,
        sizeBytes: e.size,
        adapterVersion: 'nif_batch_extent-phase2',
      });
      const worldTransforms = composeWorldTransforms(ir);
      const bounds = computeSceneBounds(ir, worldTransforms);
      let triangles = 0, vertices = 0, shapes = 0, nodes = 0;
      for (const b of ir.blocks) {
        if (b.type === 'NiTriShape') shapes++;
        if (b.type === 'NiNode') nodes++;
        if (b.type === 'NiTriShapeData' && b.geometry) {
          triangles += b.geometry.numTriangles ?? 0;
          vertices += b.geometry.numVertices ?? 0;
        }
      }
      const hasMeshGeometry = bounds.meshCount > 0 && Number.isFinite(bounds.min[0]);
      row.status = hasMeshGeometry ? 'DECODED' : 'DECODED_NO_MESH_GEOMETRY';
      row.triangles = triangles;
      row.vertices = vertices;
      row.shapeCount = shapes;
      row.nodeCount = nodes;
      row.blockCount = ir.blocks.length;
      row.rootCount = ir.roots.length;
      row.meshCount = bounds.meshCount;
      if (hasMeshGeometry) {
        row.bounds = {
          min: bounds.min, max: bounds.max,
          extents: bounds.extents,
          maxAxisExtent: Math.max(bounds.extents[0], bounds.extents[1], bounds.extents[2]),
          footprintX: bounds.extents[0],
          footprintZ: bounds.extents[2],
        };
      } else {
        row.bounds = { extents: null, maxAxisExtent: null, note: 'UNKNOWN — no mesh geometry in composed scene (never reported as 0)' };
      }
      decoded++;
      if (!hasMeshGeometry) noMesh++;
    } catch (err) {
      row.status = 'FAILED';
      row.error = String(err?.message ?? err).slice(0, 400);
      row.errorClass = classifyError(row.error);
      failed++;
      errorClasses.set(row.errorClass, (errorClasses.get(row.errorClass) ?? 0) + 1);
      if (!errorSamples.has(row.errorClass)) errorSamples.set(row.errorClass, row.error);
    }
    row.elapsedMs = Date.now() - ft0;
    if (row.elapsedMs > maxFileMs) maxFileMs = row.elapsedMs;
    sumFileMs += row.elapsedMs;
    fs.appendFileSync(statePath, JSON.stringify(row) + '\n', 'utf8');
  }

  const summary = {
    artifact: 'NIF10_BATCH_EXTENT_SUMMARY',
    runId: 'PE_CITY_ASSET_MAP_R1_20261010',
    phase: 'METADATA_CATALOG',
    era: 'PCG_9_3_5',
    container: { path: bntPath, sizeBytes: bytes.length, sha256: containerSha },
    totalEntriesInContainer: entries.length,
    nif101Candidates: candidates.length,
    alreadyDoneBeforeThisRun: doneOrdinals.size,
    thisRunProcessed: todo.length,
    thisRunDecoded: decoded,
    thisRunDecodedNoMeshGeometry: noMesh,
    thisRunFailed: failed,
    errorClassHistogram: Object.fromEntries([...errorClasses.entries()].sort((a, b) => b[1] - a[1])),
    errorSamples: Object.fromEntries([...errorSamples.entries()]),
    maxFileMs, sumFileMs,
    statePath, summaryPath,
    elapsedMs: Date.now() - t0,
  };
  process.stdout.write(JSON.stringify(summary, null, 1) + '\n');
}

main().catch((err) => {
  console.error('[nif_batch_extent] FATAL:', err?.stack ?? err);
  process.exitCode = 1;
});
