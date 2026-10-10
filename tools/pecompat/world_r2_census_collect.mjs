#!/usr/bin/env node
// world_r2_census_collect.mjs — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010
// Collects WORLD_COVERAGE_AND_LOD.json + VEGETATION_CENSUS.json from the LIVE
// server (the running production instance on 8163) + the PRODUCTION
// WorldVegetation class (a headless THREE rebuild against the real routes —
// the same class the browser runs). NO synthetic payloads.
import { promises as fsp } from 'node:fs';
import path from 'node:path';

const BASE = process.env.R2_BASE ?? 'http://127.0.0.1:8163';
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).href.replace(/^file:\/\/\//, '')), '..', '..');
const OUT_COV = path.join(ROOT, 'docs/audits/PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010/WORLD_COVERAGE_AND_LOD.json');
const OUT_VEG = path.join(ROOT, 'docs/audits/PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010/VEGETATION_CENSUS.json');

const THREE = await import(pathToFileURLFullPath(path.join(ROOT, 'node_modules/three/build/three.module.js')));
const { WorldVegetation } = await import(pathToFileURLFullPath(path.join(ROOT, 'compat/world-vegetation.js')));
const { PEHeightField } = await import(pathToFileURLFullPath(path.join(ROOT, 'src/peworld/PEHeightQuery.js')));
const { PESourceMount } = await import(pathToFileURLFullPath(path.join(ROOT, 'src/pesource/PESourceMount.js')));
const zlib = await import('node:zlib');
const crypto = await import('node:crypto');

function pathToFileURLFullPath(p) { return 'file:///' + p.replace(/\\/g, '/'); }

const io = {
  readFile: async (p) => new Uint8Array(await fsp.readFile(p)),
  inflate: async (b) => new Uint8Array(zlib.inflateSync(b)),
  sha256: async (b) => crypto.createHash('sha256').update(b).digest('hex'),
};
const status = await (await fetch(`${BASE}/api/world/status`)).json();

// ---------------- the coverage census (§4: explicitly separate) ----------------
const overviewProgress = await (await fetch(`${BASE}/api/world/overview/progress`)).json();
const farHeaders = (await fetch(`${BASE}/api/world/far`));
const farOk = farHeaders.ok;
const lod8Probe = await fetch(`${BASE}/api/world/lod8/0/0`);
const coverage = {
  run: 'PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010',
  measuredAt: new Date().toISOString(),
  source: `${BASE} (the LIVE production server)`,
  denominator: {
    gridCapacity: 220 * 236,
    indexRegularTilesMeasuredFromIndex: status.denominator.indexRegularTiles,
    indexTotalEntries: status.denominator.indexTotalEntries,
    specialRows: status.denominator.specialRows,
    sentinel: status.denominator.sentinel,
    note: 'the MEASURED denominator (from the terrain.bnt index at boot — never a hardcoded 51920 gate)',
  },
  indexedTiles: {
    regular: status.denominator.indexRegularTiles,
    specialRows: status.denominator.specialRows,
    sentinel: status.denominator.sentinel,
  },
  validRawSamples: {
    measuredTiles: status.census.measured,
    missingEntryTiles: status.census.missing,
    decodeFailedTiles: status.census.failed,
    rawU16ZeroIsData: true,
  },
  coarseLod: {
    far: { ready: status.continuousWorld.farLod.ready, perTileEdge: status.continuousWorld.farLod.perTileEdge, routeOk: farOk, decimation: status.continuousWorld.farLod.decimation },
    mid: { blocksX: status.continuousWorld.midLod.blocksX, blocksY: status.continuousWorld.midLod.blocksY, perTileEdge: status.continuousWorld.midLod.perTileEdge, blocksServed: status.continuousWorld.midLod.blocksServed, decimation: status.continuousWorld.midLod.decimation },
    policy: 'renderer LOD: decimated REAL samples (never averaging; the samples keep their own positions); missing tiles = explicit holes (status bytes served with the payloads — never zero surface); the far route 503s until the census completes (no zero-filled placeholder)',
  },
  nearResident: {
    windowTiles: 8 * 8,
    haloTiles: 10 * 10,
    clientTileCacheMax: 512,
  },
  pending: { censusPendingAtCollect: overviewProgress.pending, farGatedByCensus: true },
  missing: { missingEntry: status.census.missing, decodeFailed: status.census.failed },
  seamsPolicy: 'near|mid and mid|far boundary grid lines MATCH (the same ORIGINAL samples on the cut lines — no cracks, no skirts needed); the near mesh renders 0..510 m; the halo (10x10 field) covers the generator 0..512 span for heights',
  heightQueryVersion: status.continuousWorld.heightQueryVersion,
};

// ---------------- the vegetation census (§6.5) ----------------
// a headless THREE rebuild of the PRODUCTION class against the LIVE routes
const mount = new PESourceMount(io);
await mount.mountEra({ era: 'PCG_9_3_5', container: 'Terrain/terrain.bnt', path: 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Terrain\\terrain.bnt', expectedSha256: status.containers.terrain.sha256.toUpperCase(), verifyHash: true, format: 'BNT2_TERRAIN' });
// the field for the window (50,111): window + the 1-tile REAL halo (49..58 x 110..119)
const WIN = { gx: 50, gy: 111 };
async function buildFieldFor(win) {
  const f = [];
  for (let dy = -1; dy <= 8; dy++) {
    const row = [];
    for (let dx = -1; dx <= 8; dx++) {
      const gx = win.gx + dx, gy = win.gy + dy;
      row.push(gx >= 0 && gy >= 0 && gx < 220 && gy < 236 ? await mount.getTerrainTile({ era: 'PCG_9_3_5', gridX: gx, gridY: gy }) : null);
    }
    f.push(row);
  }
  return new PEHeightField(f, { tileWorldMeters: 64 });
}
// the SHARED-query delegating handle (the app's pattern: one handle, the
// per-window PEHeightField swapped by the window rebuild)
const sharedHeightQuery = { _target: null, triangleHeightAtWorld(x, z) { return this._target ? this._target.triangleHeightAtWorld(x, z) : null; } };
sharedHeightQuery._target = await buildFieldFor(WIN);
const veg = new WorldVegetation({
  scene: new THREE.Scene(),
  fetchJson: async (url) => {
    const r = await fetch(BASE + url);
    const j = await r.json();
    if (!r.ok) throw new Error(j?.message ?? `HTTP ${r.status}`);
    return j;
  },
  fetchBinary: async (url) => {
    const r = await fetch(BASE + url);
    if (!r.ok) {
      const j = await r.json().catch(() => null);
      throw new Error(j?.message ?? `HTTP ${r.status}`);
    }
    return { payload: new Uint8Array(await r.arrayBuffer()), headers: { era: r.headers.get('x-pe-era'), entryName: r.headers.get('x-pe-entry') } };
  },
  heightField: sharedHeightQuery,
});
const censuses = {};
// the DEFAULT global profile (the launcher default) at the measured default density
await veg.setConfig({ profileMode: 'global', profile: 0, labSeed: 0, densityPercent: 50 });
censuses.globalDefault = await veg.rebuild({ gx: 50, gy: 111 }, 8);
// the regional RECONSTRUCTION_PREVIEW (OUR map)
await veg.setConfig({ profileMode: 'regional', profile: 0, labSeed: 0, densityPercent: 50 });
censuses.regionalPreview = await veg.rebuild({ gx: 50, gy: 111 }, 8);
// a regional window SPANNING a region boundary (region = tile >> 5: tiles
// 28..35 cross regionX 0 and 1 — at least two OURS-mapped profiles in one window)
sharedHeightQuery._target = await buildFieldFor({ gx: 28, gy: 111 });
censuses.regionalPreviewBoundary = await veg.rebuild({ gx: 28, gy: 111 }, 8);
const serverVeg = status.vegetation;
const vegCensus = {
  run: 'PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010',
  measuredAt: new Date().toISOString(),
  source: `${BASE} (the LIVE production server) + the PRODUCTION WorldVegetation class (headless THREE)`,
  serverSupportCensus: serverVeg?.supportCensus
    ? {
      profile: serverVeg.supportCensus.profile,
      counts: serverVeg.supportCensus.counts,
      perModel: serverVeg.supportCensus.models,
    }
    : { state: serverVeg?.supportCensusState ?? 'unknown' },
  windowRebuilds: {
    globalDefaultProfile0Seed0Density50: censuses.globalDefault,
    regionalPreviewOursSameConfig: censuses.regionalPreview,
    regionalPreviewBoundaryWindow: censuses.regionalPreviewBoundary,
  },
  censusVocabulary: {
    indexedProfileIds: censuses.globalDefault?.profiles?.used,
    records: censuses.globalDefault?.profiles?.records,
    distinctCandidateIds: censuses.globalDefault?.distinctIds?.candidates,
    distinctSelectedIds: censuses.globalDefault?.distinctIds?.selected,
    distinctGeometryRenderedIds: censuses.globalDefault?.distinctIds?.geometryRendered,
    markers: censuses.globalDefault?.distinctIds?.markers,
    statusCounts: censuses.globalDefault?.statusCounts,
    untextured: censuses.globalDefault?.models?.untextured,
    unsupportedModels: censuses.globalDefault?.models?.unsupported,
    slotDiagnostics: censuses.globalDefault?.models?.slotDiagnostics,
    sourceUntexturedControlsNote: 'the four CD proxies 192374/193207/193313/193684 are NOT part of this in-world census — they are the Asset Lab CONTROLS (source-untextured per the established catalog finding; see CAMERA_UI_AND_ASSET_LAB.md + BROWSER_INTERACTION S10)',
  },
};
veg.dispose();

await fsp.writeFile(OUT_COV, JSON.stringify(coverage, null, 1) + '\n');
await fsp.writeFile(OUT_VEG, JSON.stringify(vegCensus, null, 1) + '\n');
console.log(JSON.stringify({
  coverage: { denominator: coverage.denominator.indexRegularTilesMeasuredFromIndex, farReady: coverage.coarseLod.far.ready, missing: coverage.missing },
  vegGlobal: { requested: censuses.globalDefault?.counts?.requested, placed: censuses.globalDefault?.counts?.placed, geometryRenderedIds: censuses.globalDefault?.distinctIds?.geometryRendered?.length, markers: censuses.globalDefault?.distinctIds?.markers, statusCounts: censuses.globalDefault?.statusCounts },
  vegRegional: { requested: censuses.regionalPreview?.counts?.requested, placed: censuses.regionalPreview?.counts?.placed, profilesUsed: censuses.regionalPreview?.profiles?.used, geometryRenderedIds: censuses.regionalPreview?.distinctIds?.geometryRendered?.length },
}, null, 1));
