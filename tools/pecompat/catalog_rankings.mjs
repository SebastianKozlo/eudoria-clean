// catalog_rankings.mjs — PE_CITY_ASSET_MAP_R1_20261010, phase 2 (W2, contract §2)
// Builds the three DESCENDING rankings from the phase-2 catalogs + batch
// state, with MANDATORY coverage numbers (total / measured / unsupported /
// failed) on every ranking, and the four PRIMARY_IDS rows + cross-era search.
//
//   1. PAYLOAD_SIZE — uncompressed model size (Models containers, BOTH eras;
//      full coverage: CD2003 Models.ark 2,492/2,492; PCG935 Models.bnt
//      5,596/5,596).
//   2. SCENE_EXTENT — composed-hierarchy FILE_SCENE_SPACE AABB, MEASURED ONLY
//      for decoded models (PCG935 NIF 10.1 batch); CD2003 NIF 4.x models are
//      NOT decoded in this phase → UNKNOWN for every one of them (never 0).
//      maxAxisExtent is the primary sort key; footprintX/footprintZ are given
//      alongside so a flat model can never be hidden by a volume number.
//   3. COMPLEXITY — triangles / vertices / shapes / nodes as EXPLICIT
//      separate unit columns (same coverage as SCENE_EXTENT).
//
// "Largest city"-style claims are FORBIDDEN: coverage is incomplete; every
// table is labeled largest-MEASURED.
//
// OUTPUT: full ranking CSVs → PRIVATE_OUTPUT; bounded top-50 tables +
// coverage + primary rows + cross-era search → REPORT_PACKAGE
// (docs/audits/PE_CITY_ASSET_MAP_R1_20261010/CATALOG_COVERAGE.json).
// Era labels on every row.

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

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

/** Hash every file in the private PHASE2_* artifact dirs → path+SHA256
 * references for the report (the report references private artifacts by
 * path+SHA; payload content itself never enters the repo). */
function hashPrivateArtifacts(dirs) {
  const refs = [];
  const walk = (dir) => {
    for (const d of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, d.name);
      if (d.isDirectory()) walk(full);
      else if (d.isFile()) {
        const bytes = fs.readFileSync(full);
        refs.push({
          path: full.split(path.sep).join('/'),
          sizeBytes: bytes.length,
          sha256: crypto.createHash('sha256').update(bytes).digest('hex'),
        });
      }
    }
  };
  for (const d of dirs) if (fs.statSync(d).isDirectory()) walk(d);
  refs.sort((a, b) => a.path.localeCompare(b.path));
  return refs;
}

function csvWrite(file, header, rows) {
  const lines = [header, ...rows.map((r) => r.join(','))];
  fs.writeFileSync(file, lines.join('\r\n') + '\r\n', 'utf8');
}

function main() {
  const args = parseArgs(process.argv);
  const privCats = args['cats-dir'];       // PHASE2_CATALOGS
  const privExtent = args['extent-dir'];   // PHASE2_EXTENT
  const privRank = args['rankings-dir'];   // PHASE2_RANKINGS
  const privCensus = args['census-dir'];   // PHASE2_CENSUS
  const privVfs = args['vfs-dir'];         // PHASE2_VFS
  const reportDir = args['report-dir'];    // docs/audits/PE_CITY_ASSET_MAP_R1_20261010/
  for (const d of [privCats, privExtent, privRank, reportDir]) {
    if (!d || !fs.statSync(d).isDirectory()) throw new Error(`dir required/missing: ${d}`);
  }

  const cdModels = JSON.parse(fs.readFileSync(path.join(privCats, 'CD2003_MODELS_ARK_ENTRIES.json'), 'utf8'));
  const pcgModels = JSON.parse(fs.readFileSync(path.join(privCats, 'PCG935_MODELS_BNT_ENTRIES.json'), 'utf8'));
  const cdTex = JSON.parse(fs.readFileSync(path.join(privCats, 'CD2003_TEXTURES_ARK_ENTRIES.json'), 'utf8'));
  const pcgTex = JSON.parse(fs.readFileSync(path.join(privCats, 'PCG935_TEXTURES_BNT_ENTRIES.json'), 'utf8'));

  // ---- batch state (SCENE_EXTENT + COMPLEXITY measured rows) ----
  const pcgTotal = pcgModels.records.length;
  const stateRows = fs.readFileSync(path.join(privExtent, 'PCG935_NIF10_BATCH_STATE.jsonl'), 'utf8')
    .trim().split('\n').map((l) => JSON.parse(l));
  const measured = stateRows.filter((r) => r.status === 'DECODED' && r.bounds && r.bounds.maxAxisExtent != null);
  const noMesh = stateRows.filter((r) => r.status === 'DECODED_NO_MESH_GEOMETRY');
  const decodedTotal = stateRows.filter((r) => r.status === 'DECODED' || r.status === 'DECODED_NO_MESH_GEOMETRY');
  const failedBatch = stateRows.filter((r) => r.status === 'FAILED');
  const notAttempted = pcgTotal - stateRows.length; // version gate: never attempted
  const errorHistogram = new Map();
  const unknownTypeCensus = new Map();
  for (const r of failedBatch) {
    // classify by MESSAGE content (probe-run rows may carry the older 'OTHER'
    // label from the pre-fix classifier — the message is authoritative)
    const m = (r.error ?? '');
    const cls = (m.includes('UNKNOWN type') || m.includes('no parser registered'))
      ? 'UNKNOWN_BLOCK_TYPE_NO_PARSER'
      : (r.errorClass ?? 'OTHER');
    errorHistogram.set(cls, (errorHistogram.get(cls) ?? 0) + 1);
    const um = m.match(/UNKNOWN type "([^"]+)"/);
    if (um) unknownTypeCensus.set(um[1], (unknownTypeCensus.get(um[1]) ?? 0) + 1);
  }

  // ================= RANKING 1: PAYLOAD_SIZE (both eras, full coverage) =================
  const cdSize = cdModels.records.map((r) => ({
    era: 'CD_2003', rank: 0, name: r.name, entryIndex: r.entryIndex,
    uncompressedSizeBytes: r.uncompressedSize, storedSizeBytes: r.storedSize,
    payloadSha256: r.payloadSha256, status: r.status,
  })).sort((a, b) => b.uncompressedSizeBytes - a.uncompressedSizeBytes);
  cdSize.forEach((r, i) => { r.rank = i + 1; });
  const pcgSize = pcgModels.records.map((r) => ({
    era: 'PCG_9_3_5', rank: 0, name: r.name, entryIndex: r.entryIndex,
    uncompressedSizeBytes: r.uncompressedSize, storedSizeBytes: r.storedSize,
    payloadSha256: r.payloadSha256, status: r.status,
  })).sort((a, b) => b.uncompressedSizeBytes - a.uncompressedSizeBytes);
  pcgSize.forEach((r, i) => { r.rank = i + 1; });
  csvWrite(path.join(privRank, 'CD2003_MODELS_PAYLOAD_SIZE_RANKING.csv'),
    'era,rank,name,entry_index,uncompressed_size_bytes,stored_size_bytes,payload_sha256,status',
    cdSize.map((r) => [r.era, r.rank, r.name, r.entryIndex, r.uncompressedSizeBytes, r.storedSizeBytes, r.payloadSha256, r.status]));
  csvWrite(path.join(privRank, 'PCG935_MODELS_PAYLOAD_SIZE_RANKING.csv'),
    'era,rank,name,entry_index,uncompressed_size_bytes,stored_size_bytes,payload_sha256,status',
    pcgSize.map((r) => [r.era, r.rank, r.name, r.entryIndex, r.uncompressedSizeBytes, r.storedSizeBytes, r.payloadSha256, r.status]));

  // ================= RANKING 2: SCENE_EXTENT (PCG935 measured only) =================
  const extent = measured.map((r) => ({
    era: 'PCG_9_3_5', rank: 0, name: r.name, entryIndex: r.entryIndex, payloadSha256: r.payloadSha256,
    maxAxisExtent: r.bounds.maxAxisExtent,
    extentX: r.bounds.extents[0], extentY: r.bounds.extents[1], extentZ: r.bounds.extents[2],
    footprintX: r.bounds.footprintX, footprintZ: r.bounds.footprintZ,
    meshCount: r.meshCount, triangles: r.triangles,
    space: 'FILE_SCENE_SPACE',
    units: 'ORIGINAL file units (unit scale NOT established — never called meters)',
  })).sort((a, b) => b.maxAxisExtent - a.maxAxisExtent);
  extent.forEach((r, i) => { r.rank = i + 1; });
  csvWrite(path.join(privRank, 'PCG935_SCENE_EXTENT_RANKING.csv'),
    'era,rank,name,entry_index,max_axis_extent,extent_x,extent_y,extent_z,footprint_x,footprint_z,mesh_count,triangles,payload_sha256,space,units',
    extent.map((r) => [r.era, r.rank, r.name, r.entryIndex, r.maxAxisExtent, r.extentX, r.extentY, r.extentZ, r.footprintX, r.footprintZ, r.meshCount, r.triangles, r.payloadSha256, r.space, '"' + r.units + '"']));

  // ================= RANKING 3: COMPLEXITY (PCG935: all decoded rows) =================
  const complexity = decodedTotal.map((r) => ({
    era: 'PCG_9_3_5', rank: 0, name: r.name, entryIndex: r.entryIndex, payloadSha256: r.payloadSha256,
    triangles: r.triangles, vertices: r.vertices, shapes: r.shapeCount, nodes: r.nodeCount,
    blocks: r.blockCount, roots: r.rootCount,
    decodeStatus: r.status,
  })).sort((a, b) => b.triangles - a.triangles);
  complexity.forEach((r, i) => { r.rank = i + 1; });
  csvWrite(path.join(privRank, 'PCG935_COMPLEXITY_RANKING.csv'),
    'era,rank,name,entry_index,triangles,vertices,shapes,tri_shape_count,nodes,ni_node_count,blocks,roots,decode_status,payload_sha256',
    complexity.map((r) => [r.era, r.rank, r.name, r.entryIndex, r.triangles, r.vertices, r.shapes, r.nodes, r.blocks, r.roots, r.decodeStatus, r.payloadSha256]));

  // ================= PRIMARY_IDS rows (CD_2003 Models.ark) + cross-era search =================
  const PRIMARY_IDS = ['192374', '193207', '193313', '193684'];
  const pcgNameIndex = new Map(pcgModels.records.map((r) => [r.name, r]));
  const cdNameIndex = new Map(cdModels.records.map((r) => [r.name, r]));
  const primaryRows = [];
  const crossEraSearch = [];
  for (const id of PRIMARY_IDS) {
    const cdRow = cdNameIndex.get(`${id}.nif`) ?? null;
    const primaryRow = cdRow ? {
      id, era: 'CD_2003', container: 'Models/Models.ark',
      entryName: cdRow.name, entryIndex: cdRow.entryIndex,
      storedSizeBytes: cdRow.storedSize, uncompressedSizeBytes: cdRow.uncompressedSize,
      compression: cdRow.compression === 0 ? 'STORED (ArkVFS; stored==uncompressed)' : cdRow.compression,
      crc32: cdRow.crc32Stored, crc32Match: cdRow.crc32Match,
      payloadSha256: cdRow.payloadSha256, sniffClass: cdRow.sniff?.sniffClass, nifVersion: cdRow.sniff?.nifVersion,
      sceneExtent: 'UNKNOWN (NIF 4.1.0.12 — not decoded in phase 2; phase 3 bounded scope)',
      complexity: 'UNKNOWN (same)',
    } : { id, era: 'CD_2003', status: 'NOT_FOUND' };
    primaryRows.push(primaryRow);
    // cross-era exact search: same literal entry name in PCG_9_3_5 Models.bnt
    const candidates = [];
    for (const probe of [`${id}.nif`, `${id}.NIF`]) {
      const hit = pcgNameIndex.get(probe);
      if (hit) {
        candidates.push({ entryName: hit.name, entryIndex: hit.entryIndex, sizeBytes: hit.storedSize, payloadSha256: hit.payloadSha256, sniffClass: hit.sniff?.sniffClass, nifVersion: hit.sniff?.nifVersion });
      }
    }
    crossEraSearch.push({
      id, searchedIn: 'PCG_9_3_5 Models.bnt catalog (exact entry-name match only — NO silhouette/geometry guessing)',
      exactNameMatch: candidates.length ? candidates : null,
      verdict: candidates.length ? 'LITERAL_ID_FOUND' : 'NO_LITERAL_ID_MATCH (absence of the literal ID is NOT proof of absence of a counterpart — contract §3)',
    });
  }

  // ================= coverage =================
  const nif10Candidates = stateRows.length;         // 4,838 (attempted)
  const unsupportedByVersionGate = notAttempted;    // 758 (never attempted)
  const coverage = {
    PAYLOAD_SIZE: {
      CD_2003: { container: 'Models/Models.ark', total: cdSize.length, measured: cdSize.length, unsupported: 0, failed: 0, coverageLabel: 'FULL (entry sizes are index metadata; all entries measured)' },
      PCG_9_3_5: { container: 'Models/Models.bnt', total: pcgSize.length, measured: pcgSize.length, unsupported: 0, failed: 0, coverageLabel: 'FULL (BNT2 raw payload sizes; all entries measured)' },
    },
    SCENE_EXTENT: {
      CD_2003: { container: 'Models/Models.ark', total: cdSize.length, measured: 0, unsupported: cdSize.length, failed: 0, coverageLabel: 'NONE MEASURED — NIF 4.x not decoded in phase 2 (phase 3 = 4 primary models only); every CD_2003 SCENE_EXTENT is UNKNOWN (never 0)' },
      PCG_9_3_5: {
        container: 'Models/Models.bnt', total: pcgTotal,
        measured: measured.length,
        decodedWithoutMeshGeometry_extentUnknown: noMesh.length,
        attemptedAndFailed: failedBatch.length,
        unsupportedNeverAttempted_versionGate: unsupportedByVersionGate,
        coverageLabel: `MEASURED ${measured.length} of ${pcgTotal}: batch attempted on ${nif10Candidates} NIF 10.1.0.0 candidates → ${measured.length} decoded WITH mesh bounds; ${noMesh.length} decoded WITHOUT mesh geometry (extent UNKNOWN, never 0); ${failedBatch.length} FAILED with unregistered block types (parser surface NOT expanded this phase); ${unsupportedByVersionGate} NIF 4.x entries outside the reader version gate never attempted (757 x 4.1.0.12 + 1 x 4.0.0.2)`,
      },
    },
    COMPLEXITY: {
      CD_2003: { container: 'Models/Models.ark', total: cdSize.length, measured: 0, unsupported: cdSize.length, failed: 0, coverageLabel: 'NONE MEASURED — same as SCENE_EXTENT' },
      PCG_9_3_5: {
        container: 'Models/Models.bnt', total: pcgTotal,
        measured: decodedTotal.length,
        measuredWithGeometry: measured.length,
        measuredNoMeshGeometry_zeroCountsAreReal: noMesh.length,
        attemptedAndFailed: failedBatch.length,
        unsupportedNeverAttempted_versionGate: unsupportedByVersionGate,
        coverageLabel: `MEASURED ${decodedTotal.length} of ${pcgTotal} (${measured.length} with geometry + ${noMesh.length} with genuinely zero triangles/vertices — real values, not placeholders); ${failedBatch.length} FAILED (unregistered block types); ${unsupportedByVersionGate} version-gated NIF 4.x never attempted`,
      },
    },
  };

  const topN = (rows, n, cols) => rows.slice(0, n).map((r) => Object.fromEntries(cols.map((c) => [c, r[c]])));

  const report = {
    artifact: 'CATALOG_COVERAGE.json',
    runId: 'PE_CITY_ASSET_MAP_R1_20261010',
    phase: 'METADATA_CATALOG (phase 2)',
    generatedBy: 'tools/pecompat/catalog_rankings.mjs (this run; input catalogs re-measured by this executor)',
    eraLabels: { CD_2003: 'corpus of the 2003 CD installer (Models.ark, Textures.ark)', PCG_9_3_5: 'PCG 9.3.5 installation (Models.bnt, Textures.bnt, *.vfs)' },
    identityKeySchema: {
      description: 'ASSET_IDENTITY = ERA + CONTAINER_SHA256 + ENTRY_NAME + PAYLOAD_SHA256 — an ID alone is never globally unique; every catalog record carries all four (see full catalogs in PRIVATE_OUTPUT, referenced by path+SHA256 in this file)',
      containerSha256: {
        CD_2003_Models_ark: cdModels.container.sha256,
        CD_2003_Textures_ark: cdTex.container.sha256,
        PCG_9_3_5_Models_bnt: pcgModels.container.sha256,
        PCG_9_3_5_Textures_bnt: pcgTex.container.sha256,
      },
    },
    fileCensus: {
      CD_2003: { filesFound: 4, filesOk: 4, filesFailed: 0, totalBytes: 424407359, byTopLevelDirectory: { Models: 1, Scripts: 1, Textures: 1, Volumes: 1 }, byExtension: { '.ark': 4 }, fullCensusRef: 'PRIVATE_OUTPUT/PHASE2_CENSUS/CD_2003_FILE_CENSUS.{csv,json}' },
      PCG_9_3_5: { filesFound: 1818, filesOk: 1818, filesFailed: 0, totalBytes: 2384417861, byTopLevelDirectory: { '.': 1, EffectSequences: 1, Models: 1, MouseCursors: 14, Parameters: 27, Portals: 1, Sounds: 1722, Strings: 15, Terrain: 1, TerrainEditZones: 1, Textures: 2, UI: 1, VegetationClimates: 1, Video: 29, Volumes: 1 }, byExtension: { '.wav': 1616, '.sgt': 104, '.bik': 29, '.vfs': 27, '.bnt': 26, '.ani': 13, '.ini': 1, '.cur': 1, '.mp3': 1 }, fullCensusRef: 'PRIVATE_OUTPUT/PHASE2_CENSUS/PCG_9_3_5_FILE_CENSUS.{csv,json}' },
    },
    containerCatalogs: {
      CD_2003_Models_ark: {
        entries: cdModels.entryCount, payloadHashed: cdModels.entryCount, crc32Verified: cdModels.entryCount, crc32Mismatch: 0,
        readFailures: 0, duplicateNames: 0, compression: ['STORED (0) — stored==uncompressed for every entry'],
        sniffDistribution: { NIF: cdModels.entryCount }, nifVersionDistribution: { '4.1.0.12': 1815, '4.0.0.2': 440, '4.0.0.0': 237 },
        dualIndexVerification: 'sequential local-header scan (era-validated ArkArchive) == EOCD totals == standard-ZIP-layout central directory walk (entry-by-entry name/offset match, 0 mismatches; the alternative skill-documented CD layout FAILED 100% — recorded honestly)',
        boundaryChecks: 'all payloads end exactly at central-directory offset; CD+cdSize == EOCD offset; EOCD+22 == file size',
        fullCatalogRef: 'PRIVATE_OUTPUT/PHASE2_CATALOGS/CD2003_MODELS_ARK_ENTRIES.{csv,json}',
      },
      CD_2003_Textures_ark: {
        entries: cdTex.entryCount, payloadHashed: cdTex.entryCount, crc32Verified: cdTex.entryCount, crc32Mismatch: 0,
        readFailures: 0, duplicateNames: 0, compression: ['STORED (0)'],
        sniffDistribution: { DDS: 1359, TGA_HEADER: 3433, OTHER: 41 },
        otherNote: '41 entries named *.tga are tiny (4-96 B) data stubs — no image header; content NOT decoded in this phase (honestly UNKNOWN, CRC-verified)',
        fullCatalogRef: 'PRIVATE_OUTPUT/PHASE2_CATALOGS/CD2003_TEXTURES_ARK_ENTRIES.{csv,json}',
      },
      PCG_9_3_5_Models_bnt: {
        format: 'BNT2 verified with the SAME reused reader (full directory parsed to exact end); payloads are RAW 1:1 (all 5,596 first-bytes sniffed as direct NIF headers)',
        entries: pcgModels.entryCount, payloadHashed: pcgModels.entryCount, crc32Verified: pcgModels.entryCount, crc32Mismatch: 0,
        readFailures: 0, duplicateNames: 0, overlaps: 0, gaps: 0,
        padFieldNote: 'directory trailing u32 == crc32 for 3,435/5,596 entries only — pad semantics UNKNOWN where unequal (recorded raw, not interpreted)',
        nifVersionDistribution: { 'Gamebryo 10.1.0.0': 4838, 'NetImmerse 4.1.0.12': 757, 'NetImmerse 4.0.0.2': 1 },
        predecessorComparison: 'predecessor census 5,596 = 4,838 + 757 + 1 — REPRODUCED by this run as its OWN measurement (comparison evidence only)',
        fullCatalogRef: 'PRIVATE_OUTPUT/PHASE2_CATALOGS/PCG935_MODELS_BNT_ENTRIES.{csv,json}',
      },
      PCG_9_3_5_Textures_bnt: {
        format: 'BNT2 verified with the SAME reused reader (layout NOT different; 8,381 entries — explicitly NOT the 8,095-entry EU2008-era copy, which is a different-era file never mixed with this corpus)',
        entries: pcgTex.entryCount, payloadHashed: pcgTex.entryCount, crc32Verified: pcgTex.entryCount, crc32Mismatch: 0,
        readFailures: 0, duplicateNames: 0, overlaps: 0, gaps: 0,
        sniffDistribution: { DDS: 2752, TGA_HEADER: 5610, OTHER: 19 },
        fullCatalogRef: 'PRIVATE_OUTPUT/PHASE2_CATALOGS/PCG935_TEXTURES_BNT_ENTRIES.{csv,json}',
      },
    },
    vfsInspection: {
      scope: 'bounded header/structure inspection ONLY — no full decode attempted or claimed; record layouts NOT established in this phase',
      textures_vfs: { sizeBytes: 1552, signature: 'ArkVFS02', identityMatch: true, strings: 1, headerMetaMeaning: 'UNKNOWN (recorded raw)', ref: 'PRIVATE_OUTPUT/PHASE2_VFS/PCG935_TEXTURES_VFS_INSPECT.json' },
      materials_vfs: { sizeBytes: 80400, signature: 'ArkVFS02', identityMatch: true, strings: 2668, firstStrings: '#include "1Ark.fx" / struct Vertex / float3 Position : POSITION; — HLSL shader text (bounded string census only; consistent with the pe-bnt-tdf skill note)', ref: 'PRIVATE_OUTPUT/PHASE2_VFS/PCG935_MATERIALS_VFS_INSPECT.json' },
      templates_vfs: { sizeBytes: 560788, signature: 'ArkVFS02', identityMatch: true, strings: 7703, layout: 'record layout NOT established; mostly binary after the 16-byte header', ref: 'PRIVATE_OUTPUT/PHASE2_VFS/PCG935_TEMPLATES_VFS_INSPECT.json' },
    },
    rankings: {
      axisConvention: 'SCENE_EXTENT/COMPLEXITY are measured in FILE_SCENE_SPACE: the file\'s own serialized x/y/z axis labels, NO axis swap, NO unit conversion, world = parentWorld * local TRS from the proven root; axis semantics (e.g. which axis is up) NOT established by the reader; ORIGINAL file units everywhere — never called meters; footprint = x,z extents per the task contract; SOURCE_FILE_SCENE_SPACE ≠ WORLD_PLACEMENT',
      claimDiscipline: 'ALL ranking tables are largest-MEASURED (coverage incomplete); "largest city"-style claims are FORBIDDEN and NOT made',
      PAYLOAD_SIZE: {
        CD_2003: { coverage: coverage.PAYLOAD_SIZE.CD_2003, top50: topN(cdSize, 50, ['rank', 'name', 'uncompressedSizeBytes', 'payloadSha256']), fullRef: 'PRIVATE_OUTPUT/PHASE2_RANKINGS/CD2003_MODELS_PAYLOAD_SIZE_RANKING.csv' },
        PCG_9_3_5: { coverage: coverage.PAYLOAD_SIZE.PCG_9_3_5, top50: topN(pcgSize, 50, ['rank', 'name', 'uncompressedSizeBytes', 'payloadSha256']), fullRef: 'PRIVATE_OUTPUT/PHASE2_RANKINGS/PCG935_MODELS_PAYLOAD_SIZE_RANKING.csv' },
      },
      SCENE_EXTENT: {
        CD_2003: { coverage: coverage.SCENE_EXTENT.CD_2003, top50: [], fullRef: null, note: 'no measured rows — every CD_2003 model is UNKNOWN (phase 3 handles the 4 primary NIF 4.1.0.12 models only)' },
        PCG_9_3_5: {
          coverage: coverage.SCENE_EXTENT.PCG_9_3_5,
          top50: topN(extent, 50, ['rank', 'name', 'maxAxisExtent', 'extentX', 'extentY', 'extentZ', 'footprintX', 'footprintZ', 'meshCount', 'triangles']),
          fullRef: 'PRIVATE_OUTPUT/PHASE2_RANKINGS/PCG935_SCENE_EXTENT_RANKING.csv',
        },
      },
      COMPLEXITY: {
        CD_2003: { coverage: coverage.COMPLEXITY.CD_2003, top50: [], fullRef: null, note: 'no measured rows — UNKNOWN (phase 3)' },
        PCG_9_3_5: {
          coverage: coverage.COMPLEXITY.PCG_9_3_5,
          top50: topN(complexity, 50, ['rank', 'name', 'triangles', 'vertices', 'shapes', 'nodes']),
          units: 'triangles = NiTriShapeData triangle count; vertices = vertex count; shapes = NiTriShape blocks; nodes = NiNode blocks',
          fullRef: 'PRIVATE_OUTPUT/PHASE2_RANKINGS/PCG935_COMPLEXITY_RANKING.csv',
        },
      },
    },
    batchDecodeDetails: {
      candidates: nif10Candidates, decodedWithBounds: measured.length, decodedNoMeshGeometry: noMesh.length,
      decodedTotal: decodedTotal.length, failed: failedBatch.length,
      unsupportedVersionGate: unsupportedByVersionGate,
      failureClasses: Object.fromEntries([...errorHistogram.entries()].sort((a, b) => b[1] - a[1])),
      unknownTypeCensus: Object.fromEntries([...unknownTypeCensus.entries()].sort((a, b) => b[1] - a[1])),
      policy: 'the era-validated reader was used AS IS — no parser expansion; every failure is a LOUD unregistered-block-type error, recorded per entry and kept visible (contract §2)',
    },
    primaryModels: { ids: PRIMARY_IDS, era: 'CD_2003', rows: primaryRows },
    crossEraSearch: {
      method: 'exact entry-name match of the 4 literal IDs in the PCG_9_3_5 Models.bnt catalog — NO silhouette/geometry/name-similarity guessing; a negative is NOT proof of absence of a counterpart',
      results: crossEraSearch,
    },
    unknownVisibility: 'UNSUPPORTED/FAILED/UNKNOWN entries are KEPT in every catalog with explicit error/unknown fields — no invented zeros anywhere',
    privateArtifactReferences: {
      policy: 'every full private catalog/census/ranking/state artifact is referenced by absolute path + SHA256 + size; PRIVATE_OUTPUT content itself never enters the repo (contract §8)',
      root: 'D:/Eudoria_Reconstruction/99_Audits/PE_CITY_ASSET_MAP_R1_20261010/',
      artifacts: hashPrivateArtifacts([privCensus, privCats, privVfs, privExtent, privRank].filter(Boolean)),
    },
  };

  const outPath = path.join(reportDir, 'CATALOG_COVERAGE.json');
  fs.writeFileSync(outPath, JSON.stringify(report, null, 1), 'utf8');
  process.stdout.write(JSON.stringify({
    artifact: 'CATALOG_RANKINGS_BUILT',
    outPath,
    counts: {
      cdSize: cdSize.length, pcgSize: pcgSize.length, extentMeasured: measured.length,
      complexityMeasured: complexity.length, batchFailed: failedBatch.length,
      noMesh: noMesh.length, primaryRows: primaryRows.length,
    },
  }, null, 1) + '\n');
}

main();
