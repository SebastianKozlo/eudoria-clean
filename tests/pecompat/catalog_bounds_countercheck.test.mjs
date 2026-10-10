// catalog_bounds_countercheck.test.mjs — PE_CITY_ASSET_MAP_R1_20261010, phase 4 (W6)
// HIERARCHY->BOUNDS INDEPENDENT COUNTERCHECK (contract §7: "nie tylko ten sam
// parser dwa razy" / NOT the same parser twice).
//
// INDEPENDENT PATH (this suite's OWN code — it imports NEITHER nif41_deep
// NOR PecSceneIR for the bounds computation): a minimal raw-byte scan of each
// primary payload that locates the length-prefixed "NiTriShapeData" block-type
// strings directly in the file bytes, validates each candidate structurally
// (length prefix == string length; sane numVertices; hasVertices flag byte;
// the vertex array fits the file), reads the vertex arrays as raw f32 LE and
// unions their AABB. Because the composed FILE_SCENE_SPACE bounds equal the
// raw vertex union EXACTLY WHEN the local TRS are identity, the suite ALSO
// verifies from the LIVE WIRE (server path) that every AVObject local TRS is
// identity — making the raw-vertex union a valid independent composition.
//
// COMPARISON TARGETS (three-way):
//   (a) the LIVE viewer-path bounds (catalog_data.buildCatalogData ->
//       buildPrimaryWire — the phase-3 reader + PecSceneIR composition used by
//       the actual /catalog product);
//   (b) the FROZEN phase-3 measured values (docs/audits/.../CATALOG_COVERAGE.json
//       primaryModels rows — the checkpoint PE-MASTER verified);
//   (c) the PHASE-3 PYTHON DUAL-DECODE agreement (recorded evidence —
//       nif_parser_v2.py agreed on all standard blocks/names/refs/geometry;
//       noted here as recorded, not re-run).
//
// TOLERANCES (stated): the independent scan reads the same f32 bytes, so
// agreement is expected EXACT; the gate uses absTol = 0.01 ORIGINAL file units
// (float32 magnitude ~3e4 -> ~4e-3 ulp-scale) and reports the max measured
// delta. maxAxisExtent and footprintX/footprintZ agreement are asserted too.
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import { ArkArchive } from '../../src/pesource/ArkArchive.js';
import {
  buildCatalogData, buildPrimaryWire, PRIMARY_PINS, PRIMARY_IDS, CATALOG_PINS,
} from '../../tools/pecompat/catalog_data.mjs';

const RUN_ID = 'PE_CITY_ASSET_MAP_R1_20261010';
const PKG = path.resolve(path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1')), '..', '..', 'docs', 'audits', RUN_ID);

function rec(id, name, status, extra = {}) {
  return { id, name, status, ...extra };
}
const ok = (b) => (b ? 'PASS' : 'FAIL');

// ---------------------------------------------------------------------------
// the INDEPENDENT minimal scanner (own stream math; NO product imports)
// ---------------------------------------------------------------------------
/** Scan a raw NIF 4.1 payload for length-prefixed "NiTriShapeData" type
 * strings and read the vertex arrays at their file offsets. Returns per-candidate
 * vertex arrays + a union AABB. Validates each candidate structurally — a
 * false-positive string match cannot survive the checks. */
export function independentVertexScan(payload) {
  const TYPE = 'NiTriShapeData';
  const typeBytes = new TextEncoder().encode(TYPE);
  const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  const found = [];
  for (let i = 0; i + 4 + typeBytes.length <= payload.length; i++) {
    if (dv.getInt32(i, true) !== typeBytes.length) continue;
    let match = true;
    for (let k = 0; k < typeBytes.length; k++) {
      if (payload[i + 4 + k] !== typeBytes[k]) { match = false; break; }
    }
    if (!match) continue;
    // candidate block: type string at i; data starts after it
    let p = i + 4 + typeBytes.length;
    if (p + 3 > payload.length) continue;
    const numVertices = dv.getUint16(p, true);
    const hasVertices = payload[p + 2];
    if (numVertices === 0 || numVertices > 65535) continue; // implausible/empty
    if (hasVertices !== 1) continue;                          // NiBool: must be true
    p += 3;
    if (p + numVertices * 12 > payload.length) continue;      // array must fit the file
    const min = [Infinity, Infinity, Infinity];
    const max = [-Infinity, -Infinity, -Infinity];
    for (let v = 0; v < numVertices; v++) {
      for (let k = 0; k < 3; k++) {
        const x = dv.getFloat32(p + (v * 12) + k * 4, true);
        if (x < min[k]) min[k] = x;
        if (x > max[k]) max[k] = x;
      }
    }
    found.push({ typeStringAt: i, dataAt: i + 4 + typeBytes.length, numVertices, min, max });
  }
  if (found.length === 0) return null;
  const min = [Infinity, Infinity, Infinity];
  const max = [-Infinity, -Infinity, -Infinity];
  for (const f of found) {
    for (let k = 0; k < 3; k++) {
      if (f.min[k] < min[k]) min[k] = f.min[k];
      if (f.max[k] > max[k]) max[k] = f.max[k];
    }
  }
  return {
    dataBlocks: found,
    union: {
      min, max,
      extents: [max[0] - min[0], max[1] - min[1], max[2] - min[2]],
      maxAxisExtent: Math.max(max[0] - min[0], max[1] - min[1], max[2] - min[2]),
      footprintX: max[0] - min[0],
      footprintZ: max[2] - min[2],
    },
  };
}

export async function run(ctx) {
  const records = [];
  const modelsArkPath = ctx.modelsArkPath ?? CATALOG_PINS.modelsArk.path;
  let data = null;
  try {
    data = await buildCatalogData({
      modelsArkPath,
      modelsBntPath: ctx.modelsPath ?? CATALOG_PINS.modelsBnt.path,
      batchStatePath: ctx.batchStatePath ?? null,
      nameEdgesPath: ctx.nameEdgesPath ?? null,
    });
  } catch (e) {
    records.push(rec('CAT_BOUNDS_PRECHECK', 'catalog data build (prerequisites for the countercheck)', 'FAIL', {
      measuredQuantity: 'buildCatalogData on the pinned originals',
      measured: String(e?.message ?? e).slice(0, 1500),
      failureCaseDetected: 'the pinned containers did not verify or the build failed — countercheck prerequisites unavailable',
    }));
    return records;
  }

  // the frozen phase-3 values (PE-MASTER-verified checkpoint) as a third source
  let frozen = null;
  try {
    const pkgPath = ctx.coveragePath ?? path.join(PKG, 'CATALOG_COVERAGE.json');
    const raw = JSON.parse(await readFile(pkgPath, 'utf8'));
    frozen = new Map(raw.primaryModels.rows.map((r) => [String(r.id), r.sceneExtent]));
  } catch { /* optional third source; recorded when absent */ }

  const results = [];
  let allOk = true;
  const TOL = 0.01; // ORIGINAL file units; exact same f32 bytes are expected
  for (const id of PRIMARY_IDS) {
    // 1. extract the payload INDEPENDENTLY from the pinned original
    const whole = new Uint8Array(await readFile(modelsArkPath));
    const containerSha = crypto.createHash('sha256').update(whole).digest('hex');
    if (containerSha !== CATALOG_PINS.modelsArk.sha256) {
      results.push({ id, independent: null, error: 'container SHA mismatch' });
      allOk = false;
      continue;
    }
    const arch = new ArkArchive(whole);
    const entry = arch.entries().find((e) => e.name === `${id}.nif`);
    const { payload } = arch.readEntry(entry);
    const sha = crypto.createHash('sha256').update(payload).digest('hex');
    if (sha !== PRIMARY_PINS[id].sha256) {
      results.push({ id, independent: null, error: `payload pin mismatch (${sha})` });
      allOk = false;
      continue;
    }
    // 2. INDEPENDENT scan (own code — no product imports for the bounds)
    const scan = independentVertexScan(payload);
    // 3. the LIVE viewer-path wire (the product path the browser uses)
    const wire = buildPrimaryWire(data.primaries[id], id);
    const live = wire.sceneBounds_FILE_SCENE_SPACE;
    // 4. identity-TRS precondition measured FROM THE WIRE (composition must
    //    be a pass-through for the raw-vertex union to equal the composed bounds)
    const trs = wire.blocks.map((b) => b.localTrs).filter(Boolean);
    const allIdentity = trs.every((t) =>
      t.translate[0] === 0 && t.translate[1] === 0 && t.translate[2] === 0 &&
      t.rotate[0][0] === 1 && t.rotate[1][1] === 1 && t.rotate[2][2] === 1 &&
      t.rotate[0][1] === 0 && t.rotate[0][2] === 0 && t.rotate[1][0] === 0 &&
      t.rotate[1][2] === 0 && t.rotate[2][0] === 0 && t.rotate[2][1] === 0 &&
      t.scale === 1);
    const delta = {
      min: [0, 1, 2].map((k) => Math.abs(scan.union.min[k] - live.min[k])),
      max: [0, 1, 2].map((k) => Math.abs(scan.union.max[k] - live.max[k])),
      maxAxisExtent: Math.abs(scan.union.maxAxisExtent - live.maxAxisExtent),
      footprintX: Math.abs(scan.union.footprintX - live.footprintX),
      footprintZ: Math.abs(scan.union.footprintZ - live.footprintZ),
    };
    const agreeLive = delta.min.every((d) => d <= TOL) && delta.max.every((d) => d <= TOL) &&
      delta.maxAxisExtent <= TOL && delta.footprintX <= TOL && delta.footprintZ <= TOL;
    // 5. frozen phase-3 values agreement (third source)
    let frozenDelta = null;
    let agreeFrozen = null;
    if (frozen?.has(id)) {
      const f = frozen.get(id);
      frozenDelta = Math.max(...[0, 1, 2].map((k) =>
        Math.max(Math.abs(scan.union.min[k] - f.min[k]), Math.abs(scan.union.max[k] - f.max[k]))));
      agreeFrozen = frozenDelta <= TOL && Math.abs(scan.union.maxAxisExtent - f.maxAxisExtent) <= TOL;
    }
    const entryOk = allIdentity && agreeLive && (frozen ? agreeFrozen === true : true) && scan.dataBlocks.length === wire.meshRows.length;
    if (!entryOk) allOk = false;
    results.push({
      id,
      dataBlocksScanned: scan.dataBlocks.length,
      meshesInWire: wire.meshRows.length,
      allLocalTrsIdentity: allIdentity,
      independent: scan.union,
      liveViewerBounds: live,
      frozenPhase3Bounds: frozen?.get(id) ?? null,
      delta,
      frozenDeltaMax: frozenDelta,
      agreeLive, agreeFrozen, entryOk,
    });
  }

  records.push(rec('CAT_BOUNDS_COUNTERCHECK', 'hierarchy->bounds INDEPENDENT countercheck: raw-byte vertex scan (own minimal code) vs the LIVE viewer-path composed bounds vs the FROZEN phase-3 values, for all four primaries', ok(allOk), {
    measuredQuantity: 'per-primary AABB agreement (min/max/maxAxisExtent/footprints) across three sources',
    measured: {
      tolerance: 'absTol 0.01 ORIGINAL file units (the independent scan reads the same f32 bytes; exact equality expected, tolerance stated)',
      identityPrecondition: 'all local TRS identity measured FROM THE WIRE for every AVObject (the raw-vertex union equals the composed FILE_SCENE_SPACE bounds exactly when TRS are identity — verified, not assumed)',
      independentPath: 'minimal length-prefixed "NiTriShapeData" scan + raw f32 vertex reads (this suite OWN code; imports neither nif41_deep nor PecSceneIR for the bounds)',
      recordedThirdLayer: 'phase-3 PYTHON DUAL-DECODE agreement (nif_parser_v2.py) is recorded evidence in DEEP_ANALYSIS.md §1.4 — not re-run here',
      results,
    },
    independentSourceOfTruth: 'raw payload bytes scanned by this suite own minimal scanner vs the product reader+composer vs the frozen checkpoint values',
    whyNonCircular: 'the scanner shares no code with the reader/composer; the wire is read only as the comparison target',
    failureCaseDetected: allOk ? 'none — all four agree within the stated tolerance on min/max/maxAxisExtent/footprintX/footprintZ' : 'bounds disagreement beyond tolerance (see results)',
  }));
  return records;
}
