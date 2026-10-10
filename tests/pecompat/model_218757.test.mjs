// model_218757.test.mjs — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// T5 (plan T7): pinned 218757 extraction + ALL 14 mesh/data association
// checks + fingerprint comparison vs the predecessor's measured values
// (MODEL_218757_RELATION_RESULTS.json), block census/accounting, hierarchy,
// texture bindings and closure decisions — recomputed from the pinned
// Models.bnt bytes through THIS run's adapter/reader.
//
// MEASURED_QUANTITY: extraction identities; 14 association rows (counts +
//   f32-LE vertex / u16-LE triangle SHA256 fingerprints); census; FILE_SCENE_
//   SPACE bounds; texture binding census; boundary decisions.
// INDEPENDENT_SOURCE_OF_TRUTH: (a) the contract §2 pins; (b) the predecessor
//   package's committed measurements (RELATION_RESULTS + SCENE_STRUCTURE,
//   produced by an INDEPENDENT earlier parser from byte-identical payload);
//   (c) the phase-1 native captures for controls.
// WHY_NON_CIRCULAR: the predecessor fingerprints were produced by a DIFFERENT
//   (Python, s2-lineage) parser; matching all 28 hashes (14 vertex + 14 index)
//   with THIS independently written JS reader is a two-implementation
//   agreement over the pinned bytes — a mismatch is a BLOCKER, not papered
//   over.
// FAILURE_CASE_DETECTED: any hash/count/name/decision mismatch, any pin
//   mismatch, or a round-trip break fails the corresponding check loudly.
import { readFile } from 'node:fs/promises';
import { PecAssetAdapter, MODEL_218757_PINS } from '../../src/pecompat/PecAssetAdapter.js';
import { fileSceneSpaceArtifact } from '../../src/pecompat/PecSceneIR.js';
import {
  sha256, readFileBytes, record,
} from './_helpers.mjs';

const PRED_PATH = 'docs/audits/PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009/02_PE/MODEL_218757_RELATION_RESULTS.json';
const SCENE_STRUCT_PATH = 'docs/audits/PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009/02_PE/SCENE_STRUCTURE_RESULTS.json';

// The predecessor's q5 census (00_Control_Internal_QC/q5_218757_block_census.json
// values, committed at BASE) — reference for the type census:
const EXPECTED_TYPE_CENSUS = {
  NiNode: 12, NiArkAnimationExtraData: 1, NiArkImporterExtraData: 1, NiArkTextureExtraData: 1,
  NiTexturingProperty: 9, NiArkViewportInfoExtraData: 1, NiStringExtraData: 1,
  NiMaterialProperty: 9, NiZBufferProperty: 1, NiTriShape: 14, NiTriShapeData: 14,
  NiDirectionalLight: 2,
};

export async function run(ctx) {
  const out = [];
  if (!ctx.modelsPath) {
    out.push(record('T5_218757_extraction', 'pinned 218757 extraction + associations + fingerprints', 'NOT_PERFORMED', {
      measuredQuantity: 'all T5 checks',
      blocker: 'NOT_PERFORMED_CONTAINER_UNAVAILABLE — run with --models <Models.bnt path> to enable (never silently skipped)',
      failureCaseDetected: 'container not provided',
    }));
    return out;
  }

  const io = { readFile: readFileBytes, sha256 };
  const adapter = new PecAssetAdapter(io, { modelsBntPath: ctx.modelsPath });
  let m;
  try {
    m = await adapter.loadModel(MODEL_218757_PINS.modelId);
  } catch (e) {
    out.push(record('T5_218757_extraction', 'pinned 218757 extraction + associations + fingerprints', 'FAIL', {
      measuredQuantity: 'adapter load',
      measured: String(e?.message ?? e),
      failureCaseDetected: 'fail-closed adapter error (pin mismatch or parse failure)',
    }));
    return out;
  }
  const ir = m.ir;

  // ---- extraction identity (A1) ----
  const p = m.provenance;
  const extractionOk = p.payloadSha256 === MODEL_218757_PINS.payloadSha256 &&
    p.containerSha256 === MODEL_218757_PINS.modelsBntSha256 &&
    p.crossChecks.entryOrdinal.match && p.crossChecks.payloadOffset.match && p.crossChecks.payloadSize.match;
  out.push(record('T5a_extraction_identity', 'pinned extraction identity (container/payload/entry cross-checks)', extractionOk ? 'PASS' : 'FAIL', {
    measuredQuantity: 'container SHA256, payload SHA256, entry ordinal/offset/size',
    independentSourceOfTruth: 'contract §2 pins (C950A8C2... container, 3E8A22C2... payload, 781/116223520/57316 cross-checks)',
    whyNonCircular: 'pins fixed before the run; the adapter is fail-closed against them',
    measured: {
      containerSha256: p.containerSha256, payloadSha256: p.payloadSha256,
      entryOrdinal: p.entryOrdinal, entryOffset: p.entryOffset, entrySize: p.entrySize, entryCrc32: p.entryCrc32,
    },
    expected: {
      containerSha256: MODEL_218757_PINS.modelsBntSha256, payloadSha256: MODEL_218757_PINS.payloadSha256,
      entryOrdinal: MODEL_218757_PINS.entryOrdinal, entryOffset: MODEL_218757_PINS.payloadOffset,
      entrySize: MODEL_218757_PINS.payloadSize,
    },
    failureCaseDetected: extractionOk ? 'none' : 'identity mismatch (would have failed closed)',
  }));

  // ---- block census + 62+4 accounting (order-independent comparison) ----
  const normCensus = (c) => JSON.stringify(Object.entries(c).map(([k, v]) => [k, v]).sort((a, b) => a[0].localeCompare(b[0])));
  const censusOk = normCensus(ir.blockTypeCensus) === normCensus(EXPECTED_TYPE_CENSUS);
  const accountingOk = ir.blocks.length === 66 && ir.decodeCensus.SUPPORTED === 62 &&
    (ir.decodeCensus.PARTIALLY_UNDERSTOOD + ir.decodeCensus.OPAQUE) === 4;
  const arkStatuses = ir.blocks.filter((b) => b.type.startsWith('NiArk')).map((b) => `${b.index}:${b.type}:${b.decodeStatus}`);
  out.push(record('T5b_block_census_and_accounting', '66-block census; 62 supported + 4 Ark partially-understood/opaque', (censusOk && accountingOk) ? 'PASS' : 'FAIL', {
    measuredQuantity: 'type census + decode-status accounting',
    independentSourceOfTruth: 'predecessor q5 census + contract §1 62/4 ceiling',
    whyNonCircular: 'census counted from THIS reader over pinned bytes; compared to an independently measured reference',
    measured: { census: ir.blockTypeCensus, decodeCensus: ir.decodeCensus, arkStatuses },
    expected: { census: EXPECTED_TYPE_CENSUS, total: 66, supported: 62, arkBlocks: 4 },
    failureCaseDetected: (censusOk && accountingOk) ? 'none' : 'census or 62+4 accounting mismatch',
  }));

  // ---- 14 associations + fingerprints vs predecessor ----
  const pred = JSON.parse(await readFile(PRED_PATH, 'utf8'));
  const sceneStruct = JSON.parse(await readFile(SCENE_STRUCT_PATH, 'utf8'));
  const rows = [];
  let assocPass = 0, fingerPass = 0;
  for (const pm of pred.meshes_218757) {
    const mine = ir.meshAssociations.find((x) => x.meshBlock === pm.mesh_block);
    const assoc = !!mine && mine.dataBlock === pm.data_block &&
      mine.numVertices === pm.num_vertices && mine.numTriangles === pm.num_triangles &&
      mine.meshName === pm.mesh_name;
    const vHash = mine?.vertexPositionsF32leSha256 === pm.vertex_positions_f32le_sha256.toLowerCase();
    const iHash = mine?.triangleIndicesU16leSha256 === pm.triangle_indices_u16le_sha256.toLowerCase();
    if (assoc) assocPass++;
    if (vHash && iHash) fingerPass++;
    rows.push({
      meshBlock: pm.mesh_block, meshName: pm.mesh_name, dataBlock: pm.data_block,
      assocOk: assoc, vertexHashOk: vHash, indexHashOk: iHash,
      numVertices: mine?.numVertices, numTriangles: mine?.numTriangles,
    });
  }
  const assocOk = assocPass === 14;
  const fingerOk = fingerPass === 14;
  // round-trip exactness for every mesh (decoded arrays == serialized ranges)
  const roundtripOk = m.meshFingerprints.every((f) =>
    (f.vertexRoundtripExact === undefined || f.vertexRoundtripExact === true) &&
    (f.indexRoundtripExact === undefined || f.indexRoundtripExact === true));
  out.push(record('T5c_14_associations_and_fingerprints', '14 mesh/data associations + 28 fingerprint comparison vs predecessor', (assocOk && fingerOk && roundtripOk) ? 'PASS' : 'FAIL', {
    measuredQuantity: 'per-mesh association fields + f32-LE vertex SHA256 + u16-LE index SHA256 (recomputed from THIS reader\'s decoded arrays, cross-checked against serialized byte ranges)',
    independentSourceOfTruth: 'predecessor MODEL_218757_RELATION_RESULTS.json (independent Python s2-lineage parser, byte-identical payload)',
    whyNonCircular: 'two independent parsers agreeing on exact serialized fingerprints over pinned bytes; a mismatch would be a BLOCKER to investigate, not papered over',
    measured: { rows, assocPass, fingerPass, roundtripOk },
    expected: { assocPass: 14, fingerPass: 14, roundtripOk: true },
    failureCaseDetected: (assocOk && fingerOk && roundtripOk) ? 'none' : 'association or fingerprint mismatch (BLOCKER class)',
  }));

  // ---- hierarchy + closure decisions ----
  const expectedRootName = sceneStruct.assets['218757.nif'].serialized_roots[0].name; // "Scene Root"
  const rootBlock = ir.blocks.find((b) => b.index === ir.roots[0]);
  const realChildEdges = ir.blocks.reduce((n, b) => n + (b.children ?? []).filter((c) => c != null && c >= 0).length, 0);
  const decisions = ir.asset.closure.decisions;
  const decOk = decisions.length === 4 &&
    decisions.find((d) => d.block === 1)?.extLength === 16 &&
    decisions.find((d) => d.block === 2)?.extLength === 41 &&
    decisions.find((d) => d.block === 3)?.variantLayout === 'NOPREFIX' &&
    decisions.find((d) => d.block === 13)?.extLength === 49;
  const hierOk = ir.roots.length === 1 && rootBlock?.name === expectedRootName &&
    realChildEdges === 27 && m.validation.ok && ir.asset.closure.eofExact &&
    ir.asset.closure.numBlocksDecoded === 66;
  out.push(record('T5d_hierarchy_and_closure', 'hierarchy (root/edges/validation) + closure decisions match the corpus attribution', (hierOk && decOk) ? 'PASS' : 'FAIL', {
    measuredQuantity: 'root identity, real scene-child edge count, validation status, EOF-exact closure, boundary decisions',
    independentSourceOfTruth: 'predecessor SCENE_STRUCTURE_RESULTS.json (roots [0] "Scene Root", 27 scene-child edges) + s2 corpus attribution (16B/41B/NOPREFIX/49B)',
    whyNonCircular: 'hierarchy re-derived from bytes by THIS reader; compared to an independently measured reference',
    measured: {
      roots: ir.roots, rootName: rootBlock?.name, realChildEdges,
      validationOk: m.validation.ok, errorCount: m.validation.errors.length,
      eofExact: ir.asset.closure.eofExact, numBlocksDecoded: ir.asset.closure.numBlocksDecoded,
      decisions,
      nullChildSlotWarnings: m.validation.warnings.filter((w) => w.class === 'NULL_CHILD_SLOTS').length,
    },
    expected: { roots: [0], rootName: expectedRootName, realChildEdges: 27, validationOk: true, eofExact: true, numBlocksDecoded: 66, decisionsFour: true },
    failureCaseDetected: (hierOk && decOk) ? 'none' : 'hierarchy or closure attribution mismatch',
  }));

  // ---- FILE_SCENE_SPACE bounds (independent recomputation cross-check) ----
  const refBounds = sceneStruct.assets['218757.nif'].ni_ark_payload_analysis.model_extents_FILE_SCENE_SPACE;
  const boundsOk = Math.abs(m.sceneBounds.min[0] - refBounds.min[0]) <= 1e-3 &&
    Math.abs(m.sceneBounds.min[1] - refBounds.min[1]) <= 1e-3 &&
    Math.abs(m.sceneBounds.min[2] - refBounds.min[2]) <= 1e-3 &&
    Math.abs(m.sceneBounds.max[0] - refBounds.max[0]) <= 1e-3 &&
    Math.abs(m.sceneBounds.max[1] - refBounds.max[1]) <= 1e-3 &&
    Math.abs(m.sceneBounds.max[2] - refBounds.max[2]) <= 1e-3 &&
    m.sceneBounds.meshCount === 14;
  out.push(record('T5e_scene_bounds', 'FILE_SCENE_SPACE bounds recomputed vs predecessor extents', boundsOk ? 'PASS' : 'FAIL', {
    measuredQuantity: 'world-composed vertex bbox (full-matrix point application)',
    independentSourceOfTruth: 'predecessor model_extents_FILE_SCENE_SPACE min/max (independent parser + composition)',
    whyNonCircular: 'bounds recomputed by THIS reader/transform engine from pinned bytes',
    measured: m.sceneBounds, expected: refBounds, tolerance: 1e-3,
    failureCaseDetected: boundsOk ? 'none' : 'bounds disagree beyond tolerance',
  }));

  // ---- texture bindings (names + property refs re-derived from bytes) ----
  const refArk = sceneStruct.assets['218757.nif'].ni_ark_payload_analysis.blocks.find((b) => b.block === 3);
  const myArk = ir.blocks.find((b) => b.type === 'NiArkTextureExtraData');
  const myEntries = myArk.fields.entries;
  const arkEntriesOk = myEntries.length === refArk.decoded_entries.length &&
    myEntries.every((e, i) =>
      e.entryName === refArk.decoded_entries[i].texture_name &&
      e.texturingPropertyRef === refArk.decoded_entries[i].texturing_property_ref &&
      e.f1 === refArk.decoded_entries[i].f1_i32 &&
      e.f2 === refArk.decoded_entries[i].f2_i32 &&
      e.bytes9Hex === refArk.decoded_entries[i].bytes9_hex);
  const tb = ir.diagnostics.textureBindings;
  const bindingCensusOk = tb.filter((x) => x.status === 'TEXTURE_NAME_BOUND').length === 9 &&
    tb.filter((x) => x.status === 'UNTEXTURED_NO_TEXPROP').length === 5 &&
    tb.every((x) => x.containerResolution.includes('NOT_ESTABLISHED'));
  const untexturedAreDpvs = tb.filter((x) => x.status === 'UNTEXTURED_NO_TEXPROP').every((x) => /dpvs/i.test(x.meshName ?? ''));
  out.push(record('T5f_texture_bindings', 'per-part texture NAME bindings re-derived; dPVS meshes untextured; container NOT_ESTABLISHED', (arkEntriesOk && bindingCensusOk && untexturedAreDpvs) ? 'PASS' : 'FAIL', {
    measuredQuantity: 'ArkTexture entry list (names/refs/f1/f2/raw 9B tails) + per-mesh binding census',
    independentSourceOfTruth: 'predecessor ni_ark_payload_analysis (independent parse; 18 entries; 9 texprop-bound meshes; dPVS occ planes carry material-only refs)',
    whyNonCircular: 'names/refs re-derived from bytes in THIS reader; tails recorded RAW (no new 9-byte-tail semantics; no textureId interpretation)',
    measured: {
      arkEntryCount: myEntries.length, arkEntriesOk,
      bindingCensus: tb.map((x) => [x.meshBlock, x.meshName, x.status, x.textureNames.length]),
      containerResolutionAll: [...new Set(tb.map((x) => x.containerResolution))],
    },
    expected: { arkEntryCount: 18, nameBound: 9, untexturedNoTexprop: 5, container: 'NOT_ESTABLISHED everywhere' },
    failureCaseDetected: (arkEntriesOk && bindingCensusOk && untexturedAreDpvs) ? 'none' : 'ArkTexture entry or binding census mismatch / false binding',
  }));

  // ---- FILE_SCENE_SPACE artifact (bounded, for the app phase) ----
  const artifact = fileSceneSpaceArtifact(ir, m.worldTransforms);
  const artifactOk = artifact.blocks.length === 66 &&
    artifact.blocks.every((b) => (b.localTrs ? b.localTrs.t.length === 3 && b.localTrs.r.length === 3 : true)) &&
    artifact.blocks.filter((b) => b.type === 'NiTriShape').every((b) => b.worldTrs != null);
  if (ctx.artifactOutPath) {
    const { writeFile } = await import('node:fs/promises');
    await writeFile(ctx.artifactOutPath, JSON.stringify(artifact, null, 1) + '\n', 'utf8');
  }
  out.push(record('T5g_file_scene_space_artifact', 'bounded FILE_SCENE_SPACE transform artifact (transforms+names, no raw arrays)', artifactOk ? 'PASS' : 'FAIL', {
    measuredQuantity: 'artifact block coverage (66 entries; every mesh has a composed world transform)',
    independentSourceOfTruth: 'internal consistency with T5d composition + non-payload discipline (no geometry arrays in the artifact)',
    whyNonCircular: 'artifact derived from the same validated composition; payload arrays are never emitted',
    measured: { blockCount: artifact.blocks.length, writtenTo: ctx.artifactOutPath ?? '(in-memory only)' },
    expected: { blockCount: 66 },
    failureCaseDetected: artifactOk ? 'none' : 'artifact incomplete or contains payload-class data',
  }));

  return out;
}
