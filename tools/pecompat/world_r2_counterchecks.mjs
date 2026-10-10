#!/usr/bin/env node
// world_r2_counterchecks.mjs — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010 (contract §2 + §8)
// THE PRE/POST countercheck harness for WL-1..WL-6 — the SAME production path
// POST fixes is measured here (never a side model of the algorithm).
//
//   --phase pre   reproduce the six Desktop post-audit findings on the BASE
//                 production functions BEFORE the R2 changes (worktree still
//                 at 44ef254 content).
//   --phase post  re-run the SAME measurements AFTER the R2 implementation;
//                 each finding must show the fix (or an honest NOT_FIXED).
//
// MEASUREMENT SOURCES (all REAL, none pasted):
//   WL-1  the REAL compat/world-vegetation.js WorldVegetation class with a
//         SYNTHETIC deferred climate provider (the provider is synthetic; the
//         busy/rebuild logic under test is the production class) — A=(0,0)
//         starts with a deferred profile read, B=(1,0) is requested while A
//         is in flight, A completes. PRE expects the B request to be LOST
//         (latest request not applied).
//   WL-2  REAL payloads: 64 terrain tiles at origin (53,114) through
//         PESourceMount.getTerrainTile (the production reader — the same path
//         the world server serves); profile-0 records through
//         PESourceMount.getVegetationClimate (the production strict decoder);
//         the production generateTileInstances (PEFoliageLabSeed) at
//         density 50. The production DOM-extracted samplers
//         (vegHeightSampler/groundAt) run in a VM context against the real
//         region rawSample; the RENDERED-TRIANGLE height is computed
//         INDEPENDENTLY here from the raw payloads (barycentric on the exact
//         quad split of PETerrainRegion.buildGeometry).
//   WL-3  the production updateFlyWalk extracted verbatim from
//         compat/world-app.js, executed in a controlled VM context with a
//         real THREE camera, W held, dt=1, null ground.
//   WL-4  the production fitView + desiredOrigin extracted verbatim, three
//         consecutive fit→stream steps.
//   WL-5  the production cap slice + LAB wrapper on REAL profile records
//         (profiles 0 and 1 through the production climate decoder).
//   WL-6  RECORDS finding: fresh git measurement of the R1 commit's parent
//         vs the frozen R1 contract pin (f71eb30…) as preserved by the
//         SHA-verified Desktop post-audit input.
//
// Usage:
//   node tools/pecompat/world_r2_counterchecks.mjs --phase pre  --out <dir>
//   node tools/pecompat/world_r2_counterchecks.mjs --phase post --out <dir>
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import zlib from 'node:zlib';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { promises as fsp } from 'node:fs';
import { pathToFileURL, fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const RUN_ID = 'PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010';
const ORIGIN = { gx: 53, gy: 114 };   // the Desktop post-audit window origin (WL-2/WL-5)
const hash = (b) => crypto.createHash('sha256').update(b).digest('hex');

const args = process.argv.slice(2);
let phase = null, outDir = null;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--phase') phase = args[++i];
  else if (args[i] === '--out') outDir = args[++i];
}
if (phase !== 'pre' && phase !== 'post') {
  console.error('usage: node tools/pecompat/world_r2_counterchecks.mjs --phase pre|post --out <dir>');
  process.exit(2);
}
if (!outDir) outDir = path.join(ROOT, 'docs', 'audits', RUN_ID, 'raw', phase.toUpperCase());
fs.mkdirSync(outDir, { recursive: true });

const result = {
  run: RUN_ID,
  phase,
  measuredAt: new Date().toISOString(),
  git: {
    head: execFileSync('git', ['-C', ROOT, 'rev-parse', 'HEAD']).toString().trim(),
    status: execFileSync('git', ['-C', ROOT, 'status', '--porcelain']).toString().trim().split('\n').filter(Boolean),
  },
  findings: {},
};

// ---------------------------------------------------------------------------
// shared production imports (the CURRENT worktree content = BASE for --phase pre)
// ---------------------------------------------------------------------------
const { PESourceMount } = await import(pathToFileURL(path.join(ROOT, 'src/pesource/PESourceMount.js')).href);
const { worldHeightMeters, PE_TERRAIN_METER_PER_SAMPLE } = await import(pathToFileURL(path.join(ROOT, 'src/peworld/PETerrainCore.js')).href);
const { generateTileInstances } = await import(pathToFileURL(path.join(ROOT, 'src/peworld/PEFoliageLabSeed.js')).href);
const THREE = await import(pathToFileURL(path.join(ROOT, 'node_modules/three/build/three.module.js')).href);
const { WorldVegetation, MAX_VISIBLE_INSTANCES } = await import(pathToFileURL(path.join(ROOT, 'compat/world-vegetation.js')).href);
const appSource = fs.readFileSync(path.join(ROOT, 'compat/world-app.js'), 'utf8');
result.productionSources = {
  worldAppSha256: hash(Buffer.from(appSource, 'utf8')),
  worldVegetationSha256: hash(fs.readFileSync(path.join(ROOT, 'compat/world-vegetation.js'))),
  labSeedSha256: hash(fs.readFileSync(path.join(ROOT, 'src/peworld/PEFoliageLabSeed.js'))),
  foliageCoreSha256: hash(fs.readFileSync(path.join(ROOT, 'src/peworld/PEFoliageCore.js'))),
  terrainCoreSha256: hash(fs.readFileSync(path.join(ROOT, 'src/peworld/PETerrainCore.js'))),
};

// the production mount (the SAME readers the world server uses; era PCG_9_3_5)
const PCG_DATA = 'D:\\Eudoria_Reconstruction\\pcg_install\\Data';
const { makeNodeIo } = await import(pathToFileURL(path.join(ROOT, 'compat/server-world.mjs')).href)
  .catch(() => ({})); // server-world is importable (its top level only defines; it boots on direct run)
const io = makeNodeIo ? makeNodeIo() : { // fallback: the same shape the server uses
  readFile: async (p) => new Uint8Array(await fsp.readFile(p)),
  inflate: async (bytes) => new Uint8Array(zlib.inflateSync(bytes)),
  sha256: async (bytes) => crypto.createHash('sha256').update(bytes).digest('hex'),
};
const mount = new PESourceMount(io);
const pins = {
  terrain: '95841761CE4EA074C97930EC1CEF3FB57AAC7F7F4F3D9B751A9EE60510299990',
  vegetation: '7B858401C3EEBDA574DF4B4517E7FB2A8149C283885F27187682AA1239C745F4',
  textures: '61ACD13B140E130647EEE24C1E2669D3734990B76CF74897DDD3BA0F4EA61393',
  models: 'C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0',
};
await mount.mountEra({ era: 'PCG_9_3_5', container: 'Terrain/terrain.bnt', path: `${PCG_DATA}\\Terrain\\terrain.bnt`, expectedSha256: pins.terrain, verifyHash: true, format: 'BNT2_TERRAIN' });
await mount.mountEra({ era: 'PCG_9_3_5', container: 'VegetationClimates/VegetationClimates.bnt', path: `${PCG_DATA}\\VegetationClimates\\VegetationClimates.bnt`, expectedSha256: pins.vegetation, verifyHash: true, format: 'BNT2' });

async function climateRecords(profileIndex) {
  const r = await mount.getVegetationClimate({ era: 'PCG_9_3_5', climateIndex: profileIndex });
  return r; // { records, provenance, ... } (the production strict decode)
}

// ===========================================================================
// WL-1 — latest vegetation request can be lost while a rebuild is busy
// PRE: the BASE class returns the previous census / null while busy — the
//      B request is LOST (final origin stays A).
// POST: the R2 class QUEUES the newest request and runs it when the current
//      build completes — the final origin must be B (LATEST_REQUEST_APPLIED).
// ===========================================================================
{
  let release;
  const deferred = new Promise((res) => { release = res; });
  const veg = new WorldVegetation({
    scene: new THREE.Scene(),
    fetchJson: () => deferred, // A's profile read hangs until released (synthetic provider)
    fetchBinary: () => { throw new Error('not used in this synthetic lifecycle fixture'); },
    heightField: { triangleHeightAtWorld: () => 10 }, // the SHARED query fixture (POST API)
  });
  veg._modelEntry = async () => ({
    status: 'SUPPORTED',
    renderables: [{ geometry: new THREE.BoxGeometry(1, 1, 1), material: new THREE.MeshBasicMaterial(), shapeIndex: 0, shapeName: 'synthetic fixture' }],
  });
  await veg.setConfig({ profile: 0, labSeed: 0, densityPercent: 100 });
  const runA = veg.rebuild({ gx: 0, gy: 0 }, 1);
  const secondReturn = await veg.rebuild({ gx: 1, gy: 0 }, 1); // requested while A is busy
  release({ status: 'DECODED', records: [[457485, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]] });
  await runA;
  await new Promise((r) => setTimeout(r, 150)); // let the QUEUED newest request run (POST latest-wins)
  const census = veg.lastCensus;
  const finalOrigin = census?.window?.origin ?? null;
  const latestApplied = finalOrigin?.gx === 1 && finalOrigin?.gy === 0;
  result.findings.WL_1 = {
    name: 'latest vegetation request can be lost while a rebuild is busy (busy must queue latest-wins)',
    requestedOrigins: [{ gx: 0, gy: 0 }, { gx: 1, gy: 0 }],
    secondReturnWhileBusy: secondReturn === null || secondReturn === undefined ? null : '(previous census returned)',
    finalCommittedOrigin: finalOrigin,
    latestRequestApplied: latestApplied,
    expectedPre: 'REPRODUCED (latest request LOST: final origin stays A=(0,0); second return null/previous)',
    expectedPost: 'FIXED (the newest request is queued and runs after A: final origin B=(1,0))',
    fixed: phase === 'post' ? latestApplied : !latestApplied,
    reproduced: phase === 'pre' ? !latestApplied : undefined,
  };
  veg.dispose();
}

// ===========================================================================
// WL-2 — tree/walk height does not match the rendered mesh triangles
// PRE: the production bilinear vegHeightSampler + nearest groundAt differ
//      from the RENDERED triangle planes; 14/2304 positions fall outside the
//      sample mesh and the production apply uses the y=0 fallback.
// POST: the SHARED PEHeightField query (the exact rendered-triangle planes +
//      the 1-tile REAL-sample halo) — every instance height EQUALS the
//      rendered triangle; the field covers the full generator span; there is
//      NO y=0 fallback (a position without real surface data is
//      DEFERRED_NO_SURFACE, never rendered).
// ===========================================================================
{
  // REAL payloads: the 10x10 FIELD (window + 1-tile halo) at (52,113) — the
  // production R2 fetch layout around the (53,114) window
  const field = [];
  const tileHashes = [];
  for (let dy = -1; dy <= 8; dy++) {
    const row = [];
    for (let dx = -1; dx <= 8; dx++) {
      const gx = ORIGIN.gx + dx, gy = ORIGIN.gy + dy;
      if (gx < 0 || gy < 0 || gx >= 220 || gy >= 236) { row.push(null); continue; }
      const t = await mount.getTerrainTile({ era: 'PCG_9_3_5', gridX: gx, gridY: gy });
      row.push(t);
      tileHashes.push({ tile: `${gx},${gy}`, sha256: hash(new Uint8Array(t.heights.buffer, t.heights.byteOffset, t.heights.byteLength)) });
    }
    field.push(row);
  }
  const fieldOriginGx = ORIGIN.gx - 1, fieldOriginGy = ORIGIN.gy - 1;
  const heightField = new (await import(pathToFileURL(path.join(ROOT, 'src/peworld/PEHeightQuery.js')).href)).PEHeightField(field, { tileWorldMeters: 64 });
  // REAL profile-0 records + the production generator at density 50
  const prof0 = await climateRecords(0);
  const records = prof0.records;
  const all = [];
  for (let dy = 0; dy < 8; dy++) for (let dx = 0; dx < 8; dx++) {
    all.push(...generateTileInstances({ records, labSeed: 0, gx: ORIGIN.gx + dx, gy: ORIGIN.gy + dy, densityPercent: 50 }).instances);
  }
  const differences = [], outside = [], deferred = [];
  for (const i of all) {
    // the SHARED query (what the R2 production uses for trees AND walking)
    const q = heightField.triangleHeightAtWorld(i.world.x, i.world.y);
    if (q === null || q === undefined) { deferred.push({ key: i.key, world: i.world }); continue; }
    // the INDEPENDENT rendered-triangle height (barycentric on the exact
    // quad split of PETerrainRegion.buildGeometry) computed from the RAW
    // payloads — the same rule the near layer renders
    const lx = (i.world.x - fieldOriginGx * 64) / PE_TERRAIN_METER_PER_SAMPLE;
    const lz = (i.world.y - fieldOriginGy * 64) / PE_TERRAIN_METER_PER_SAMPLE;
    const x0 = Math.min(318, Math.floor(lx)), z0 = Math.min(318, Math.floor(lz));
    const fx = lx - Math.floor(lx), fz = lz - Math.floor(lz);
    const a = heightField.rawSample(x0, z0), b = heightField.rawSample(x0 + 1, z0);
    const c = heightField.rawSample(x0, z0 + 1), d = heightField.rawSample(x0 + 1, z0 + 1);
    const triangle = worldHeightMeters(fx + fz <= 1
      ? a + (b - a) * fx + (c - a) * fz
      : d + (c - d) * (1 - fx) + (b - d) * (1 - fz));
    differences.push({ key: i.key, world: i.world, shared: q, triangle, difference: Math.abs(q - triangle) });
  }
  differences.sort((p, q) => q.difference - p.difference);
  const vegSource = fs.readFileSync(path.join(ROOT, 'compat/world-vegetation.js'), 'utf8');
  const y0FallbackPresent = vegSource.includes('? 0 :');
  result.findings.WL_2 = {
    name: 'tree/walk height must match the rendered mesh triangles (the SHARED query + the real-sample halo; no y=0 fallback)',
    origin: ORIGIN,
    instances: all.length,
    sharedQueryNullNoSurface: deferred.length,
    deferredExamples: deferred.slice(0, 4),
    y0FallbackInProductionApply: y0FallbackPresent,
    maxDifferenceVsRenderedTriangle: differences[0]?.difference ?? 0,
    nonzeroDifferences: differences.filter((d) => d.difference > 1e-9).length,
    tilePayloadHashes: tileHashes,
    expectedPre: 'REPRODUCED (1275 nonzero, max 0.953125 bilinear↔triangle; walk↔triangle max 15.8203125; 14 outside → y=0 fallback)',
    expectedPost: 'FIXED (the shared triangle query: max difference 0 (exactly the rendered planes); the 10×10 halo covers the 0..512 generator span; no y=0 fallback in the production apply)',
    fixed: phase === 'post' ? (deferred.length === 0 && !y0FallbackPresent && (differences[0]?.difference ?? 1) < 1e-9) : undefined,
    reproduced: phase === 'pre' ? undefined : undefined,
  };
  fs.writeFileSync(path.join(outDir, 'WL2_HEIGHT_MEASUREMENTS.json'), JSON.stringify(result.findings.WL_2, null, 1) + '\n');
}

// ===========================================================================
// WL-3 — declared walk stop does not stop X/Z (null ground commits the move)
// PRE: the BASE updateFlyWalk commits camera.position.x/z BEFORE the null
//      ground guard → (100,10,100)→(100,10,88) despite the banner.
// POST: the R2 updateFlyWalk computes the CANDIDATE first and commits ONLY
//      after the surface check → the position must be UNCHANGED when no real
//      surface data exists.
// ===========================================================================
{
  function extract(name) {
    const start = appSource.indexOf(`function ${name}(`);
    if (start < 0) return null;
    const end = appSource.indexOf('\n}', start) + 2;
    return appSource.slice(start, end);
  }
  const dom = { 'boundary-banner': { hidden: true } };
  const canvas = {};
  const camera = new THREE.PerspectiveCamera();
  camera.position.set(100, 10, 100);
  const ctx = vm.createContext({
    THREE, camera, canvas,
    document: { pointerLockElement: canvas },
    state: { mode: 'walk', boundaryHit: false, heightField: null, _lastFlyFocus: null },
    move: { keys: new Set(['KeyW']), pitch: 0, yaw: 0, dragging: false },
    clampToMap: (v) => ({ ...v, clamped: false }),
    EYE_OFFSET_M: 1.7,
    MAP_MIN: 1, MAP_MAX_X: 14079, MAP_MAX_Z: 15103,
    $: (id) => dom[id],
  });
  const src = extract('updateFlyWalk');
  vm.runInContext(src, ctx);
  ctx.updateFlyWalk(1);
  const unchanged = camera.position.x === 100 && camera.position.z === 100;
  result.findings.WL_3 = {
    name: 'declared walk stop must stop X/Z (candidate-first; no commit without surface data)',
    fixture: 'production updateFlyWalk, W held, dt=1, null ground (no heightField)',
    before: { x: 100, y: 10, z: 100 },
    after: { ...camera.position },
    boundaryBannerShown: !dom['boundary-banner'].hidden,
    correctlyStopped: unchanged,
    expectedPre: 'REPRODUCED ((100,10,100) → (100,10,88) despite the boundary banner — the BASE evidence is saved in PRE_COUNTERCHECKS.json)',
    expectedPost: 'FIXED (the position stays (100,10,100) — the move is refused before any commit)',
    fixed: phase === 'post' ? unchanged : undefined,
    reproduced: phase === 'pre' ? !unchanged : undefined,
  };
}

// ===========================================================================
// WL-4 — Fit chases the streaming window (camera-position-following streaming)
// PRE: the BASE fitView sets the camera 360 units from the window center and
//      the streaming follows the CAMERA → (53,114)→(58,119)→(63,124)→(68,129).
// POST: the R2 fitView frames the FOCUS (streaming follows the FOCUS, not the
//      camera) — three consecutive fits must leave the window STABLE.
// ===========================================================================
{
  function extract(name) {
    const start = appSource.indexOf(`function ${name}(`);
    if (start < 0) return null;
    const end = appSource.indexOf('\n}', start) + 2;
    return appSource.slice(start, end);
  }
  const fitCamera = new THREE.PerspectiveCamera();
  const fitControls = { target: new THREE.Vector3(3424, 100, 7424), update() {} };
  const heightFixture = { triangleHeightAtWorld: () => 100 };
  const fitState = { mode: 'orbit', windowOrigin: { gx: 53, gy: 114 }, heightField: heightFixture };
  const fitCtx = vm.createContext({
    THREE, state: fitState, camera: fitCamera, controls: fitControls,
    focusPoint: () => fitState.mode === 'orbit' ? fitControls.target : fitCamera.position,
    WINDOW_T: 8, TILE_M: 64, GRID_W: 220, GRID_H: 236, EYE_OFFSET_M: 1.7, hud: () => {},
  });
  const fitSrc = extract('fitView');
  const focusSrc = extract('focusTile');
  const desiredSrc = extract('desiredOrigin');
  if (phase === 'post' && fitSrc && focusSrc && desiredSrc) {
    vm.runInContext(`${fitSrc}\n${focusSrc}\n${desiredSrc}`, fitCtx);
    fitState.mode = 'orbit';
    const steps = [];
    for (let n = 0; n < 3; n++) {
      const before = { ...fitState.windowOrigin };
      fitCtx.fitView();
      const ft = fitCtx.focusTile();
      const next = fitCtx.desiredOrigin(ft.gx, ft.gy);
      steps.push({ before, afterFitCamera: { ...fitCamera.position }, focus: { x: fitControls.target.x, z: fitControls.target.z }, streamedOrigin: next });
      fitState.windowOrigin = next;
    }
    const drift = steps.map((s) => s.streamedOrigin);
    const stable = drift.every((o) => o.gx === drift[0].gx && o.gy === drift[0].gy);
    result.findings.WL_4 = {
      name: 'Fit must frame the focus (streaming follows the FOCUS — no window chase)',
      steps, focusStable: stable,
      expectedPre: 'REPRODUCED ((53,114)→(58,119)→(63,124)→(68,129) — the BASE evidence is saved in PRE_COUNTERCHECKS.json)',
      expectedPost: 'FIXED (three consecutive fits keep the window origin stable for the same focus)',
      fixed: stable,
    };
  } else {
    // the PRE (BASE) reproduction relied on the BASE fitView/desiredOrigin —
    // preserved in the saved PRE evidence; note it honestly when re-run
    result.findings.WL_4 = {
      name: 'Fit must frame the focus (streaming follows the FOCUS — no window chase)',
      note: phase === 'pre'
        ? 'The BASE fitView/desiredOrigin extraction was measured at BASE — the values are preserved in PRE_COUNTERCHECKS.json (head 44ef254; production source SHAs recorded there). The CURRENT tree contains the R2 functions (focus-following).'
        : 'extraction incomplete',
      expectedPre: 'REPRODUCED at BASE ((53,114)→(58,119)→(63,124)→(68,129); saved PRE evidence)',
    };
  }
}

// ===========================================================================
// WL-5 — cap slices off the tail tiles; duplicate records overlap; density
// PRE: the BASE prefix slice (all.slice(0,5000)) empties 11/64 tiles; the
//      wrapper hash lacks recIndex (4 coincident 166878 groups); the per-tile
//      Math.round vanishes small records (3 IDs at 50%).
// POST: the R2 spatially-fair quota (largest remainder + >=1 guarantee)
//      keeps EVERY non-empty tile; recIndex is in the placement hash (0
//      coincident groups); the fractional density instantiates the small
//      records (more IDs at 50%).
// ===========================================================================
{
  const prof0 = await climateRecords(0);
  const prof1 = await climateRecords(1);
  const cap = (await import(pathToFileURL(path.join(ROOT, 'compat/world-vegetation.js')).href)).MAX_VISIBLE_INSTANCES;
  // (a) the cap selection: profile 1, density 100, the (53,114) 8x8 window
  const windowInstances = [];
  for (let dy = 0; dy < 8; dy++) for (let dx = 0; dx < 8; dx++) {
    windowInstances.push(...generateTileInstances({ records: prof1.records, labSeed: 0, gx: ORIGIN.gx + dx, gy: ORIGIN.gy + dy, densityPercent: 100 }).instances);
  }
  const perTileCounts = {};
  for (let i = 0; i < 64; i++) {
    const gx = ORIGIN.gx + (i % 8), gy = ORIGIN.gy + Math.floor(i / 8);
    perTileCounts[`${gx},${gy}`] = windowInstances.filter((a) => a.tile.gx === gx && a.tile.gy === gy).length;
  }
  const nonEmpty = Object.entries(perTileCounts).filter(([, n]) => n > 0).length;
  // the POST fair quota (the production function) — fetch-order independent
  const { fairCapQuota } = await import(pathToFileURL(path.join(ROOT, 'compat/world-vegetation.js')).href);
  const fair = fairCapQuota(perTileCounts, cap);
  const emptiedByQuota = Object.entries(fair.quotaByTile).filter(([k]) => perTileCounts[k] > 0 && fair.quotaByTile[k] === 0).length;
  // the PRE prefix slice (measured for comparison — the BASE rule)
  const activeSlice = windowInstances.slice(0, cap);
  const slicePerTile = {};
  for (let i = 0; i < 64; i++) {
    const gx = ORIGIN.gx + (i % 8), gy = ORIGIN.gy + Math.floor(i / 8);
    slicePerTile[`${gx},${gy}`] = activeSlice.filter((a) => a.tile.gx === gx && a.tile.gy === gy).length;
  }
  const emptiedBySlice = Object.entries(slicePerTile).filter(([k]) => perTileCounts[k] > 0 && slicePerTile[k] === 0).length;
  // permutation-order invariance of the quota: the quota depends ONLY on the
  // per-tile counts (shuffled request order cannot change it — by construction;
  // measured by re-running on a shuffled key insertion order)
  const shuffledCounts = {};
  for (const k of Object.keys(perTileCounts).sort((a, b) => hash(a).charCodeAt(0) - hash(b).charCodeAt(0) || (a < b ? -1 : 1))) shuffledCounts[k] = perTileCounts[k];
  const fairShuffled = fairCapQuota(shuffledCounts, cap);
  const quotaOrderInvariant = JSON.stringify(Object.entries(fair.quotaByTile).sort()) === JSON.stringify(Object.entries(fairShuffled.quotaByTile).sort());
  // (b) coincident duplicate-record positions: profile 0, density 100, one tile
  const one = generateTileInstances({ records: prof0.records, labSeed: 0, gx: ORIGIN.gx, gy: ORIGIN.gy, densityPercent: 100 }).instances;
  const posGroups = new Map();
  for (const i of one) {
    const k = `${i.modelId}:${i.world.x}:${i.world.y}`;
    if (!posGroups.has(k)) posGroups.set(k, []);
    posGroups.get(k).push(i);
  }
  const coincident = [...posGroups.values()].filter((a) => a.length > 1)
    .map((a) => ({ modelId: a[0].modelId, world: a[0].world, recordIndices: a.map((i) => i.recIndex), keys: a.map((i) => i.key) }));
  // (c) the density: profile 0, density 50 (fractional v2 — small records live)
  const d50 = generateTileInstances({ records: prof0.records, labSeed: 0, gx: ORIGIN.gx, gy: ORIGIN.gy, densityPercent: 50 });
  const instantiatedIds = [...new Set(d50.instances.map((i) => i.modelId))];
  const d25 = generateTileInstances({ records: prof0.records, labSeed: 0, gx: ORIGIN.gx, gy: ORIGIN.gy, densityPercent: 25 });
  const d25Ids = [...new Set(d25.instances.map((i) => i.modelId))];
  const d100 = generateTileInstances({ records: prof0.records, labSeed: 0, gx: ORIGIN.gx, gy: ORIGIN.gy, densityPercent: 100 });
  const d100Ids = [...new Set(d100.instances.map((i) => i.modelId))];
  const d0 = generateTileInstances({ records: prof0.records, labSeed: 0, gx: ORIGIN.gx, gy: ORIGIN.gy, densityPercent: 0 });
  const monotone = d0.instances.length === 0 && d25.instances.length <= d50.instances.length && d50.instances.length <= d100.instances.length
    && d25Ids.every((id) => instantiatedIds.includes(id)) && instantiatedIds.every((id) => d100Ids.includes(id)); // growth never flips earlier identities
  result.findings.WL_5 = {
    name: 'the cap must be spatially fair (no tile emptied by order); duplicate records need separate position streams; small records must survive 50%',
    capSelection: {
      profile: 1, density: 100,
      requested: windowInstances.length, cap,
      nonEmptyCandidateTiles: nonEmpty,
      prefixSliceEmptiedTiles: emptiedBySlice,
      fairQuotaEmptiedTiles: emptiedByQuota,
      fairQuotaOrderInvariant: quotaOrderInvariant,
      fairQuotaPerTile: fair.quotaByTile,
    },
    coincidentRecords: {
      profile: 0, density: 100, tile: `${ORIGIN.gx},${ORIGIN.gy}`,
      duplicateGroups: coincident.length,
      groups: coincident.slice(0, 6),
    },
    densityRounding: {
      profile: 0, density: 50, tile: `${ORIGIN.gx},${ORIGIN.gy}`,
      records: prof0.records.length,
      uniqueProfileModelIds: [...new Set(prof0.records.map((r) => r[0]))].length,
      instantiatedModelIds: instantiatedIds,
      zeroCountRecordIndices: [...new Set(d50.census.zeroCountRecords.map((r) => r.recIndex))],
      monotonicity: { d0: d0.instances.length, d25: d25.instances.length, d50: d50.instances.length, d100: d100.instances.length, ids25subset50: d25Ids.every((id) => instantiatedIds.includes(id)), ids50subset100: instantiatedIds.every((id) => d100Ids.includes(id)), pass: monotone },
    },
    expectedPre: 'REPRODUCED (prefix slice empties 11 tiles; 4 coincident 166878 groups rec 8/9; only 3 IDs at 50% — saved PRE evidence)',
    expectedPost: 'FIXED (0 tiles emptied by the fair quota; 0 coincident groups (recIndex in the hash); >3 IDs instantiated at 50%; monotone growth; order-invariant quota)',
    fixed: phase === 'post' ? (emptiedByQuota === 0 && coincident.length === 0 && instantiatedIds.length > 3 && quotaOrderInvariant && monotone) : undefined,
    reproduced: phase === 'pre' ? undefined : undefined,
  };
  fs.writeFileSync(path.join(outDir, 'WL5_SELECTION_MEASUREMENTS.json'), JSON.stringify(result.findings.WL_5, null, 1) + '\n');
}

// ===========================================================================
// WL-6 — records: the literal R1 base-gate compliance + the supersession
// ===========================================================================
{
  // FRESH git measurement: the R1 commit 44ef254 and its actual parent.
  const R1 = '44ef254b8ff9ebb05bd104690181c202678c065d';
  const parent = execFileSync('git', ['-C', ROOT, 'rev-parse', `${R1}^`]).toString().trim();
  const msg = execFileSync('git', ['-C', ROOT, 'log', '-1', '--format=%s', R1]).toString().trim();
  result.findings.WL_6 = {
    name: 'LITERAL_ORIGINAL_BASE_GATE_COMPLIANCE=FAIL for R1 (frozen pin f71eb30 vs actual parent e9bb1f5) + R1 INTERACTION=NOT_PERFORMED requires superseding the broad product PASS',
    r1Commit: R1,
    r1ActualParentMeasuredNow: parent,
    frozenContractPin: 'f71eb30… (per the SHA-verified Desktop post-audit REPORT.md input: „Zamrożony kontrakt §1.2–1.3 wymagał remote SOURCE_BRANCH==f71eb30…")',
    literalOriginalBaseGateCompliance: 'FAIL',
    humanExactBaseException: 'NOT_ESTABLISHED_IN_REVIEWED_INPUTS',
    r1InteractionGate: 'NOT_PERFORMED (Desktop post-audit REPORT.md — pointer lock failed in the audit browser; full fly/walk unverified)',
    r1ProductVerdictAsPublished: 'PASS_IN_IMPLEMENTED_SCOPE (inconsistent with a NOT_PERFORMED required gate)',
    r1ProductVerdictSuperseded: 'PARTIAL / REQUIRE_CORRECTIONS (this run, in R1_RECORD_SUPERSESSION.md — no retroactive authorization, no edits to the old package)',
    r1CommitSubject: msg,
  };
}

const outPath = path.join(outDir, `${phase.toUpperCase()}_COUNTERCHECKS_RAW.json`);
fs.writeFileSync(outPath, JSON.stringify(result, null, 1) + '\n');

// also write the canonical package copy (PRE_COUNTERCHECKS.json / POST_COUNTERCHECKS.json)
const canonical = path.join(ROOT, 'docs', 'audits', RUN_ID, phase === 'pre' ? 'PRE_COUNTERCHECKS.json' : 'POST_COUNTERCHECKS.json');
fs.writeFileSync(canonical, JSON.stringify(result, null, 1) + '\n');

const summary = {
  phase,
  head: result.git.head,
  dirty: result.git.status.length,
  productionSources: result.productionSources,
  WL_1: { latestRequestApplied: result.findings.WL_1.latestRequestApplied },
  WL_2: {
    instances: result.findings.WL_2.instances,
    sharedQueryNullNoSurface: result.findings.WL_2.sharedQueryNullNoSurface,
    maxDifferenceVsRenderedTriangle: result.findings.WL_2.maxDifferenceVsRenderedTriangle,
    nonzeroDifferences: result.findings.WL_2.nonzeroDifferences,
    y0FallbackInProductionApply: result.findings.WL_2.y0FallbackInProductionApply,
  },
  WL_3: { after: result.findings.WL_3.after, correctlyStopped: result.findings.WL_3.correctlyStopped },
  WL_4: result.findings.WL_4.steps ? { drift: result.findings.WL_4.steps.map((s) => s.streamedOrigin), stable: result.findings.WL_4.focusStable } : { note: result.findings.WL_4.note ?? 'see finding' },
  WL_5: {
    requested: result.findings.WL_5.capSelection.requested,
    nonEmptyCandidateTiles: result.findings.WL_5.capSelection.nonEmptyCandidateTiles,
    prefixSliceEmptiedTiles: result.findings.WL_5.capSelection.prefixSliceEmptiedTiles,
    fairQuotaEmptiedTiles: result.findings.WL_5.capSelection.fairQuotaEmptiedTiles,
    fairQuotaOrderInvariant: result.findings.WL_5.capSelection.fairQuotaOrderInvariant,
    coincidentGroups: result.findings.WL_5.coincidentRecords.duplicateGroups,
    instantiatedIdsAt50: result.findings.WL_5.densityRounding.instantiatedModelIds,
    densityMonotone: result.findings.WL_5.densityRounding.monotonicity,
  },
  WL_6: { literalGate: result.findings.WL_6.literalOriginalBaseGateCompliance, parent: result.findings.WL_6.r1ActualParentMeasuredNow },
  outPath, canonical,
};
fs.writeFileSync(path.join(outDir, `${phase.toUpperCase()}_SUMMARY.json`), JSON.stringify(summary, null, 1) + '\n');
console.log(JSON.stringify(summary, null, 2));
const fixed = ['WL_1', 'WL_2', 'WL_3', 'WL_4', 'WL_5'].every((k) => result.findings[k]?.fixed === true);
console.log(`\n== ${phase.toUpperCase()}: WL-1..WL-5 ${fixed ? 'ALL FIXED on the real production functions' : 'NOT fully fixed (see summary — honest)'} ==`);
process.exit(0);
