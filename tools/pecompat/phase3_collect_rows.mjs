// phase3_collect_rows.mjs — PE_CITY_ASSET_MAP_R1_20261010, phase 3
// Builds PRIMARY_MODEL_ROWS.json (report package) from the four private block
// dumps + the native-control run records. Machine-readable per-model rows:
// measured SCENE_EXTENT/COMPLEXITY, hierarchy summary, names, TRS coverage,
// placement finding, texture-edge summary, native control outcome.

import fs from 'node:fs';

const PRIV = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_CITY_ASSET_MAP_R1_20261010';
const DUMPS = `${PRIV}\\PHASE3_BlockDumps`;
const NATIVE = `${PRIV}\\PHASE3_NativeControl\\run_records.json`;

const MODELS = ['192374', '193207', '193313', '193684'];

const rows = [];
// strip a possible UTF-8 BOM (the native run_records.json was written by PowerShell)
const nativeRecords = JSON.parse(fs.readFileSync(NATIVE, 'utf8').replace(/^\uFEFF/, ''));

for (const m of MODELS) {
  const d = JSON.parse(fs.readFileSync(`${DUMPS}\\${m}_blocks.json`, 'utf8'));
  const native = nativeRecords.find((r) => r.model === `${m}.nif`);
  const shapeRows = d.meshRows.map((r) => ({
    shapeBlock: r.shapeBlock, shapeName: r.shapeName, dataBlock: r.dataBlock,
    pairingVerifiedBy: 'REAL dataRef (never order)',
    numVertices: r.numVertices, numTriangles: r.numTriangles,
    uvSets: r.uvSets, hasNormals: r.hasNormals,
    materialBlock: (r.propertyRefs ?? [])[0] ?? null,
  }));
  const nodeNames = d.nodeNames.map((n) => ({ index: n.index, type: n.type, name: n.name }));
  rows.push({
    era: 'CD_2003',
    model: `${m}.nif`,
    payloadSha256: d.payloadSha256,
    sizeBytes: 0, // filled below from the extraction record
    container: 'Models/Models.ark (CD_2003; READ_ONLY original)',
    nifVersion: '4.1.0.12 (0x0401000C)',
    statusClass: 'DECODED_FULL_CLOSURE (all blocks + TopObjects footer + EOF exact)',
    readerVersion: d.readerVersion,
    blockCensus: d.blockCensus,
    decodeCensus: d.decodeCensus,
    blockCount: d.header.numBlocks,
    roots: d.roots,
    rootName: d.blocks?.[0]?.name ?? null,
    hierarchySummary: {
      maxDepth: d.hierarchyRows.reduce((a, r) => Math.max(a, r.depth), 0),
      nodes: d.blockCensus.NiNode ?? 0,
      shapes: d.blockCensus.NiTriShape ?? 0,
      sceneBlocks: d.hierarchyRows.length,
    },
    nodeNames, // byte-level names — NOT game classes/city names
    desktopNameHypothesis: {
      reproduced: true,
      note: 'Desktop name hypotheses reproduced from the ORIGINAL payloads as byte-level node names; NOT confirmed collision/dPVS/LOD roles, NOT city names',
    },
    trsCoverage: d.trsCoverage,
    trsFinding: 'ALL local TRS identity on every AVObject in all four models (0 non-identity) — transforms carry NO placement',
    sceneExtent: {
      space: 'FILE_SCENE_SPACE',
      units: 'ORIGINAL file units (unit semantics NOT established — never called meters)',
      axisConvention: 'file-serialized x/y/z; NO axis swap; axis semantics (up-axis) NOT established; SOURCE_FILE_SCENE_SPACE ≠ WORLD_PLACEMENT',
      min: d.bounds.min, max: d.bounds.max, extents: d.bounds.extents,
      maxAxisExtent: d.bounds.maxAxisExtent,
      footprintX: d.bounds.footprintX, footprintZ: d.bounds.footprintZ,
      meshCount: d.bounds.meshCount,
    },
    complexity: d.complexity,
    placementFinding: d.placementFinding.finding,
    placementEvidence: d.placementFinding.evidence,
    connectedComponents: d.connectedComponents,
    textureEdges: {
      summary: 'ZERO texture bindings in the researched 4.1 scope: 0 NiTexturingProperty, 0 NiSourceTexture, NiArkTextureExtraData present with numTex=0, 0 UV sets on every mesh. UNTEXTURED_PROXY_MESH — explicit visual-fallback label, NOT a textured PASS.',
      standardPropertyChainPresent: false,
      arkTextureEntries: 0,
      arkTailNote: 'the PCG935-era 9-byte-tail interpretation does NOT transfer (no entries at all exist here — vacuously verified)',
      materialEdges: shapeRows.map((s) => ({
        shapeBlock: s.shapeBlock, shapeName: s.shapeName,
        edge: 'SHAPE->NIMATERIALPROPERTY',
        disposition: 'REFERENCE_CONFIRMED (verified block ref; material colors recorded in the private dump)',
        materialApplied: 'NOT_YET (no render in this phase)',
        browserObserved: 0,
      })),
      nameFound: 0, referenceConfirmed: shapeRows.length,
      containerEntryResolved: 0, imageDecoded: 0,
      materialApplied: 0, browserObserved: 0,
    },
    nativeControl: native ? {
      layer: 'ORIGINAL_NATIVE_EXECUTION vs OUR_READER',
      tool: 'stock Gamebryo 1.2 SceneGraphPrinter.exe',
      exeSha256: native.exe_sha256,
      argv: native.argv,
      dllExposureClass: 'CHILD_PROCESS_PATH_DLL_EXPOSURE (sandbox-local MSVCP71/MSVCR71 via child PATH)',
      outcome: native.outcome, exit: native.exit,
      stdoutBytes: native.stdout_bytes,
      stderrFirstLine: native.stderr_first_line,
      verdict: 'NATIVE_LOAD_REJECTED (measured) — the stock printer refuses these files; the cross-check layer for these four is therefore the PYTHON DUAL-DECODE (nif_parser_v2.py), which agrees on every standard block, name, ref, and geometry count',
    } : null,
    dualDecode: {
      layer: 'INDEPENDENT_SECOND_DECODER (OUR_READER vs PYTHON historical parser)',
      result: 'AGREEMENT: block-type census, all node/shape names, shape→data pairing, all vertex/triangle counts, UV/normals flags identical on all four files; the Python parser lacks NiVertexColorProperty (unknown-type for it) and does not parse the TopObjects footer (its last-block -8B "misalign" IS the footer my reader closes exactly)',
      arkNote: 'both readers consume identical Ark byte totals (57/65/21B); the SDK-conformant split (nextRef+uiSize base) is adopted here — see nif41_deep.mjs READER_VALIDATION NOTE',
    },
    shapes: shapeRows,
    privateArtifacts: {
      blockDump: `PRIVATE_OUTPUT/PHASE3_BlockDumps/${m}_blocks.json`,
      partsCsv: `PRIVATE_OUTPUT/PHASE3_BlockDumps/${m}_parts.csv`,
      nifCopy: `PRIVATE_OUTPUT/PHASE3_MODELS/${m}.nif`,
      renders: [
        `PRIVATE_OUTPUT/PHASE3_Renders/${m}_topdown_xz_filled.png`,
        `PRIVATE_OUTPUT/PHASE3_Renders/${m}_topdown_xz_wireframe.png`,
        `PRIVATE_OUTPUT/PHASE3_Renders/${m}_iso3d_wireframe.png`,
      ],
    },
  });
}

// fill exact sizes from the extraction identities
const sizes = { '192374.nif': 66759, '193207.nif': 47167, '193313.nif': 66726, '193684.nif': 75805 };
for (const r of rows) r.sizeBytes = sizes[r.model];

const out = {
  artifact: 'PRIMARY_MODEL_ROWS.json',
  runId: 'PE_CITY_ASSET_MAP_R1_20261010',
  phase: 'FOUR_MODELS_DEEP_ANALYSIS (phase 3)',
  coverageDelta: 'phase-2 rankings stay as they are; coverage measured NOW extends them: 4 CD_2003 models measured (SCENE_EXTENT/COMPLEXITY coverage 0 → 4 of 2,492; every other CD_2003 model remains UNKNOWN — never 0)',
  axisConvention: 'FILE_SCENE_SPACE everywhere: file-serialized x/y/z labels, NO axis swap, NO unit conversion; axis semantics (up-axis) NOT established; ORIGINAL file units (never meters); SOURCE_FILE_SCENE_SPACE ≠ WORLD_PLACEMENT',
  rows,
};
const outPath = process.argv[2];
if (outPath) {
  fs.writeFileSync(outPath, JSON.stringify(out, null, 1) + '\n', 'utf8');
  process.stdout.write(JSON.stringify({ artifact: 'PRIMARY_MODEL_ROWS', written: outPath, rows: out.rows.length }, null, 1) + '\n');
} else {
  process.stdout.write(JSON.stringify(out, null, 1) + '\n');
}
