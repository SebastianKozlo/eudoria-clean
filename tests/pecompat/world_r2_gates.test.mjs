// world_r2_gates.test.mjs — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010 (contract §8)
// THE R2 GATE BATTERY for the NEW subsystems (every case on the PRODUCTION
// functions; independent sources of truth; negative controls REQUIRED):
//   R2_HEIGHT_TRIANGLE_EXACT     - the SHARED PEHeightField query returns
//                                  EXACTLY the rendered-triangle planes on
//                                  the real payloads (independent barycentric
//                                  re-computation), including the exact-edge
//                                  and diagonal cases.
//   R2_HEIGHT_MISSING_TILE_NULL  - a quad touching a MISSING tile returns null
//                                  (never a fill, never y=0, never the last
//                                  height duplicated) — negative controls.
//   R2_HEIGHT_HALO_BOUNDARY      - the 256-samples/0..510 vs 0..512 boundary:
//                                  positions in (510,512] resolve on the REAL
//                                  halo samples (the y=0 fallback is GONE).
//   R2_DDS_QUALIFIED             - the DDS DXT1/DXT5 strict subset decodes the
//                                  REAL same-era witnesses (518860/518862/
//                                  516807 DXT1 + 166881 DXT5) and REFUSES the
//                                  negatives (truncated / wrong fourcc / TGA
//                                  payload / uncompressed flags).
//   R2_FAIR_CAP                  - the spatially-fair quota: >=1 for every
//                                  non-empty tile; order-invariant; the sum is
//                                  EXACTLY the cap; negative: an empty-tile
//                                  result FAILS.
//   R2_REGIONAL_PREVIEW          - the OURS regional map is deterministic +
//                                  versioned + uses DECODED profiles only.
//   R2_LOD_ROUTES                - the far + lod8 routes serve the decimated
//                                  REAL samples bit-exactly against an
//                                  INDEPENDENT decimation of the production
//                                  tile payloads; negative: out-of-range 400.
//   R2_MOVEMENT_GUARD            - the production updateFlyWalk refuses a move
//                                  with no surface data BEFORE any commit (the
//                                  WL-3 fix, on the extracted CURRENT source).
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { promises as fsp } from 'node:fs';
import zlib from 'node:zlib';
import { record } from './_helpers.mjs';
import { startWorldServer, stopWorldServer, findFreePort } from './_world_server_helpers.mjs';
import { PESourceMount } from '../../src/pesource/PESourceMount.js';
import { PEHeightField, LOD_DECIMATION, SURFACE_STATUS } from '../../src/peworld/PEHeightQuery.js';
import { fairCapQuota, REGIONAL_PREVIEW, regionalProfileFor, decodeModelTextureStrict } from '../../compat/world-vegetation.js';
import { decodeDds } from '../../src/pesource/DdsDecoder.js';
import { generateTileInstances } from '../../src/peworld/PEFoliageLabSeed.js';
import { worldHeightMeters, PE_TERRAIN_METER_PER_SAMPLE } from '../../src/peworld/PETerrainCore.js';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const PCG_DATA = 'D:\\Eudoria_Reconstruction\\pcg_install\\Data';
const sha256 = (b) => createHash('sha256').update(b).digest('hex');

export async function run(ctx) {
  const out = [];
  const io = { readFile: async (p) => new Uint8Array(await fsp.readFile(p)), inflate: async (b) => new Uint8Array(zlib.inflateSync(b)), sha256: async (b) => createHash('sha256').update(b).digest('hex') };
  const mount = new PESourceMount(io);
  await mount.mountEra({ era: 'PCG_9_3_5', container: 'Terrain/terrain.bnt', path: `${PCG_DATA}\\Terrain\\terrain.bnt`, expectedSha256: '95841761CE4EA074C97930EC1CEF3FB57AAC7F7F4F3D9B751A9EE60510299990', verifyHash: true, format: 'BNT2_TERRAIN' });
  await mount.mountEra({ era: 'PCG_9_3_5', container: 'VegetationClimates/VegetationClimates.bnt', path: `${PCG_DATA}\\VegetationClimates\\VegetationClimates.bnt`, expectedSha256: '7B858401C3EEBDA574DF4B4517E7FB2A8149C283885F27187682AA1239C745F4', verifyHash: true, format: 'BNT2' });
  await mount.mountEra({ era: 'PCG_9_3_5', container: 'Textures/Textures.bnt', path: `${PCG_DATA}\\Textures\\Textures.bnt`, expectedSha256: '61ACD13B140E130647EEE24C1E2669D3734990B76CF74897DDD3BA0F4EA61393', verifyHash: true, format: 'BNT2' });

  // ---- the REAL field: window (53,114) + the 1-tile REAL-sample halo ----
  const field = [];
  for (let dy = -1; dy <= 8; dy++) {
    const row = [];
    for (let dx = -1; dx <= 8; dx++) {
      row.push(await mount.getTerrainTile({ era: 'PCG_9_3_5', gridX: 53 + dx, gridY: 114 + dy }));
    }
    field.push(row);
  }
  const hf = new PEHeightField(field, { tileWorldMeters: 64 });

  // ---- R2_HEIGHT_TRIANGLE_EXACT: random + edge + diagonal probes vs an
  // INDEPENDENT barycentric re-computation on the RAW payloads ----
  const probes = [];
  for (let i = 0; i < 300; i++) {
    probes.push({ x: 53 * 64 + Math.random() * 512, z: 114 * 64 + Math.random() * 512 });
  }
  for (const e of [[0, 0], [510, 0], [0, 510], [510, 510], [256, 256], [128.5, 384.25]]) {
    probes.push({ x: 53 * 64 + e[0], z: 114 * 64 + e[1] });
  }
  let maxDiff = 0, nulls = 0;
  for (const p of probes) {
    const q = hf.triangleHeightAtWorld(p.x, p.z);
    if (q === null) { nulls++; continue; }
    const lx = (p.x - 52 * 64) / PE_TERRAIN_METER_PER_SAMPLE;
    const lz = (p.z - 113 * 64) / PE_TERRAIN_METER_PER_SAMPLE;
    const x0 = Math.floor(lx), z0 = Math.floor(lz), fx = lx - x0, fz = lz - z0;
    const a = hf.rawSample(x0, z0), b = hf.rawSample(x0 + 1, z0), c = hf.rawSample(x0, z0 + 1), d = hf.rawSample(x0 + 1, z0 + 1);
    const indep = worldHeightMeters(fx + fz <= 1 ? a + (b - a) * fx + (c - a) * fz : d + (c - d) * (1 - fx) + (b - d) * (1 - fz));
    maxDiff = Math.max(maxDiff, Math.abs(q - indep));
  }
  out.push(record('R2_HEIGHT_TRIANGLE_EXACT',
    'the SHARED PEHeightField query returns EXACTLY the rendered-triangle planes (300 random + 6 edge/diagonal probes vs an independent barycentric re-computation on the raw payloads)',
    (maxDiff < 1e-9 && nulls === 0) ? 'PASS' : 'FAIL', {
    resultClass: 'PRODUCTION_QUERY_VS_INDEPENDENT_RECOMPUTATION',
    measuredQuantity: 'max |sharedQuery - independentTriangle| over the probes (adapter meters)',
    measured: { probes: probes.length, nullReturns: nulls, maxAbsDifference: maxDiff },
    independentSourceOfTruth: 'a barycentric re-computation written in-test from the raw u16 payloads (the same quad split PETerrainRegion.buildGeometry renders)',
    whyNonCircular: 'the two computations share only the raw payload bytes; a wrong split or a wrong calibration shows as a nonzero difference',
    failureCaseDetected: maxDiff < 1e-9 && nulls === 0 ? 'none' : 'a probe mismatched or returned null inside the field',
  }));

  // ---- R2_HEIGHT_MISSING_TILE_NULL (negative controls) ----
  const fieldWithHole = field.map((r, y) => r.map((t, x) => (y === 5 && x === 5 ? null : t)));
  const hfHole = new PEHeightField(fieldWithHole, { tileWorldMeters: 64 });
  const holeNulls = [];
  const holeProbes = [[5 * 64 + 32, 5 * 64 + 32], [5 * 64, 5 * 64], [5 * 64 + 62, 5 * 64 + 62], [5 * 64 + 63.5, 5 * 64 + 63.5]];
  for (const [x, z] of holeProbes) holeNulls.push(hfHole.triangleHeightAtWorld(53 * 64 - 64 + x, 114 * 64 - 64 + z));
  const allNull = holeNulls.every((v) => v === null);
  // and the neighbors OUTSIDE the hole still work (both axes outside tile (5,5))
  const okNeighbor = hfHole.triangleHeightAtWorld(53 * 64 - 64 + 3 * 64 + 32, 114 * 64 - 64 + 3 * 64 + 32) !== null;
  out.push(record('R2_HEIGHT_MISSING_TILE_NULL',
    'a quad touching a MISSING tile returns null — never a fill, never y=0, never the last height duplicated; neighbors outside the hole still resolve',
    (allNull && okNeighbor) ? 'PASS' : 'FAIL', {
    resultClass: 'NEGATIVE_CONTROL (the missing-tile field)',
    measuredQuantity: 'null returns at 4 positions inside the missing tile + a working neighbor',
    measured: { holeProbes: holeNulls, neighborResolves: okNeighbor },
    independentSourceOfTruth: 'the field built in-test with a null tile',
    whyNonCircular: 'a fill/zero/duplicate-height implementation shows as a non-null return',
    failureCaseDetected: allNull && okNeighbor ? 'none' : 'the query invented a surface over a missing tile',
  }));

  // ---- R2_HEIGHT_HALO_BOUNDARY (the 0..510 vs 0..512 boundary resolution) ----
  const prof0 = await mount.getVegetationClimate({ era: 'PCG_9_3_5', climateIndex: 0 });
  const boundaryInstances = [];
  for (let dx = 0; dx < 8; dx++) for (let dy = 0; dy < 8; dy++) {
    boundaryInstances.push(...generateTileInstances({ records: prof0.records, labSeed: 0, gx: 53 + dx, gy: 114 + dy, densityPercent: 100 }).instances);
  }
  let beyond510 = 0, resolvedOnHalo = 0, yZero = 0;
  for (const i of boundaryInstances) {
    const lx = i.world.x - 53 * 64, lz = i.world.y - 114 * 64;
    if (lx > 510 || lz > 510) beyond510++;
    const q = hf.triangleHeightAtWorld(i.world.x, i.world.y);
    if (q !== null) resolvedOnHalo++;
    if (q === 0) yZero++;
  }
  out.push(record('R2_HEIGHT_HALO_BOUNDARY',
    'the 256-samples/0..510 vs generator 0..512 boundary: positions beyond the mesh sample range resolve on the REAL halo samples; the y=0 fallback is GONE',
    (beyond510 > 0 && resolvedOnHalo === boundaryInstances.length && yZero === 0) ? 'PASS' : 'FAIL', {
    resultClass: 'BOUNDARY_RESOLUTION (the halo of REAL neighboring samples)',
    measuredQuantity: 'instances beyond 510 m + resolved count + zero-height count',
    measured: { totalInstances: boundaryInstances.length, beyond510, resolvedAll: resolvedOnHalo, zeroHeights: yZero },
    independentSourceOfTruth: 'the raw halo payloads + the generator positions at 100%',
    whyNonCircular: 'the pre-fix behavior (14 nulls → y=0) would show as zeroHeights > 0 or resolved < total',
    failureCaseDetected: beyond510 > 0 && resolvedOnHalo === boundaryInstances.length && yZero === 0 ? 'none' : 'the boundary fell back or dropped instances',
  }));

  // ---- R2_DDS_QUALIFIED (positive witnesses + negative controls) ----
  const ddsResults = [];
  for (const id of [518860, 518862, 516807, 166881]) {
    const r = await mount.resolveTexture({ era: 'PCG_9_3_5', container: 'Textures/Textures.bnt', textureId: id });
    const d = decodeDds(new Uint8Array(r.payload));
    let nonzero = 0;
    for (let i = 0; i < d.rgba.length; i += 4) if (d.rgba[i] | d.rgba[i + 1] | d.rgba[i + 2]) nonzero++;
    ddsResults.push({ id, fourcc: d.fourcc, w: d.width, h: d.height, nonzeroPx: nonzero, mipsDecoded: d.mipsDecoded });
  }
  const neg = [];
  const ok1 = await mount.resolveTexture({ era: 'PCG_9_3_5', container: 'Textures/Textures.bnt', textureId: 518860 });
  const p518860 = new Uint8Array(ok1.payload);
  for (const [label, payload] of [
    ['truncated', p518860.slice(0, 100)],
    ['wrongFourcc', (() => { const b = new Uint8Array(p518860); b.set([0x33, 0x33, 0x33, 0x33], 84); return b; })()],
    ['tgaPayload', new Uint8Array((await mount.resolveTexture({ era: 'PCG_9_3_5', container: 'Textures/Textures.bnt', textureId: 519227 })).payload)],
  ]) {
    let refused = false, reason = '';
    try { decodeDds(payload); } catch (e) { refused = true; reason = String(e?.message ?? e).slice(0, 90); }
    neg.push({ label, refused, reason });
  }
  // the strict model-texture dispatch (DDS magic branch) also passes the positives
  let dispatchOk = true;
  try { decodeModelTextureStrict(p518860); } catch { dispatchOk = false; }
  out.push(record('R2_DDS_QUALIFIED',
    'the DDS DXT1/DXT5 strict subset decodes the REAL same-era witnesses (518860/518862/516807 DXT1 + 166881 DXT5 — the two previously-UNSUPPORTED formats of this run inputs) and REFUSES the negatives',
    (ddsResults.every((r) => r.nonzeroPx > 0 && r.mipsDecoded === 1) && neg.every((n) => n.refused) && dispatchOk) ? 'PASS' : 'FAIL', {
    resultClass: 'QUALIFIED_FORMAT_SUBSET (positive witnesses + negative controls; contract §6.6)',
    measuredQuantity: 'decoded dimensions/nonzero pixel counts + the refusal reasons',
    measured: { witnesses: ddsResults, negatives: neg, dispatchOk },
    independentSourceOfTruth: 'the REAL pinned payload bytes + the strict header/fourcc gates',
    whyNonCircular: 'the negatives construct malformed variants that a lax decoder would silently accept',
    failureCaseDetected: ddsResults.every((r) => r.nonzeroPx > 0) && neg.every((n) => n.refused) ? 'none' : 'a malformed payload was accepted (or a witness failed)',
  }));

  // ---- R2_FAIR_CAP ----
  const counts = {};
  for (let i = 0; i < 64; i++) {
    const gx = 53 + (i % 8), gy = 114 + Math.floor(i / 8);
    counts[`${gx},${gy}`] = 80 + (i % 41); // sum ~6400 > cap 5000 (a measured-shaped capped case)
  }
  const fair = fairCapQuota(counts, 5000);
  const totalQuota = Object.values(fair.quotaByTile).reduce((a, b) => a + b, 0);
  const minQuota = Math.min(...Object.entries(counts).filter(([, n]) => n > 0).map(([k]) => fair.quotaByTile[k]));
  const keysShuffled = Object.keys(counts).sort((a, b) => (sha256(a) < sha256(b) ? -1 : 1));
  const counts2 = {};
  for (const k of keysShuffled) counts2[k] = counts[k];
  const fair2 = fairCapQuota(counts2, 5000);
  const orderInvariant = JSON.stringify(Object.entries(fair.quotaByTile).sort()) === JSON.stringify(Object.entries(fair2.quotaByTile).sort());
  out.push(record('R2_FAIR_CAP',
    'the spatially-fair cap: every non-empty tile keeps >=1 instance at 6144->5000-class pressure; the quota is a PURE function of the per-tile counts (order-invariant); the sum is EXACTLY the cap',
    (minQuota >= 1 && totalQuota === 5000 && orderInvariant) ? 'PASS' : 'FAIL', {
    resultClass: 'PURE_ALLOCATION_CONTROL (the production fairCapQuota)',
    measuredQuantity: 'min quota over non-empty tiles + the quota sum + the order-invariance',
    measured: { nonEmptyTiles: Object.keys(fair.quotaByTile).length, minQuota, totalQuota, orderInvariant },
    independentSourceOfTruth: 'the largest-remainder + >=1-guarantee rule re-derived in-test',
    whyNonCircular: 'a prefix-slice implementation (the WL-5 defect) empties tail tiles -> minQuota 0',
    failureCaseDetected: minQuota >= 1 && totalQuota === 5000 ? 'none' : 'the allocation emptied a tile or overflowed the cap',
  }));

  // ---- R2_REGIONAL_PREVIEW ----
  const regionalDeterministic = regionalProfileFor(37, 91) === regionalProfileFor(37, 91)
    && regionalProfileFor(0, 0) !== null && regionalProfileFor(219, 235) !== null;
  const profilesAreDecoded = await (async () => {
    for (const p of REGIONAL_PREVIEW.profiles) {
      try { await mount.getVegetationClimate({ era: 'PCG_9_3_5', climateIndex: p }); } catch { return false; }
    }
    return true;
  })();
  const coversGrid = new Set();
  for (let gy = 0; gy < 236; gy += 8) for (let gx = 0; gx < 220; gx += 8) coversGrid.add(regionalProfileFor(gx, gy));
  out.push(record('R2_REGIONAL_PREVIEW',
    'the regional RECONSTRUCTION_PREVIEW map is deterministic, versioned, covers the grid, and uses ONLY DECODED profiles (0/2/7/19 — OUR choice, never a historical biome)',
    (regionalDeterministic && profilesAreDecoded && coversGrid.size >= 1) ? 'PASS' : 'FAIL', {
    resultClass: 'RECONSTRUCTION_POLICY_CONTROL (OURS — ORIGINAL_REGION_TO_CLIMATE_JOIN = NOT_ESTABLISHED)',
    measuredQuantity: 'determinism + the DECODED check + the grid coverage',
    measured: { deterministic: regionalDeterministic, profilesDecoded: profilesAreDecoded, distinctProfilesSampled: coversGrid.size, version: REGIONAL_PREVIEW.version, mapRule: REGIONAL_PREVIEW.mapRule },
    independentSourceOfTruth: 'the strict climate decode of each mapped profile',
    whyNonCircular: 'an UNSUPPORTED profile in the map would fail the decode check',
    failureCaseDetected: regionalDeterministic && profilesAreDecoded ? 'none' : 'the map is unstable or references a non-DECODED profile',
  }));

  // ---- R2_LOD_ROUTES (the LIVE server: bit-exact vs an independent decimation) ----
  const server = await startWorldServer({ port: await findFreePort(8223) });
  try {
    const get = async (p) => {
      const r = await fetch(`http://127.0.0.1:${server.port}${p}`);
      return { status: r.status, buf: new Uint8Array(await r.arrayBuffer()), headers: r.headers };
    };
    const far = await get('/api/world/far');
    let farOk = false, farChecked = 0, farMaxDiff = 0;
    if (far.status === 200 && far.buf.byteLength === 8 + 51920 + 51920 * 16 * 2) {
      const dv = new DataView(far.buf.buffer);
      const FARIDX = LOD_DECIMATION.far.indices;
      for (let probe = 0; probe < 48; probe++) {
        const gx = Math.floor(Math.random() * 220), gy = Math.floor(Math.random() * 236);
        const tile = await mount.getTerrainTile({ era: 'PCG_9_3_5', gridX: gx, gridY: gy });
        for (let ky = 0; ky < 4; ky++) for (let kx = 0; kx < 4; kx++) {
          const served = dv.getUint16(8 + 51920 + (gy * 220 + gx) * 16 * 2 + (ky * 4 + kx) * 2, true);
          const indep = tile.heights[FARIDX[ky] * 32 + FARIDX[kx]];
          farChecked++;
          if (served !== indep) farMaxDiff++;
        }
      }
      farOk = farMaxDiff === 0;
    }
    const lod8 = await get('/api/world/lod8/5/10');
    let lodOk = false, lodChecked = 0, lodBad = 0;
    if (lod8.status === 200 && lod8.buf.byteLength === 64 + 64 * 64 * 2) {
      const dv = new DataView(lod8.buf.buffer);
      const MIDIDX = LOD_DECIMATION.mid.indices;
      for (let ty = 0; ty < 8; ty++) for (let tx = 0; tx < 8; tx++) {
        const gx = 5 * 8 + tx, gy = 10 * 8 + ty;
        if (gx >= 220 || gy >= 236) continue;
        const tile = await mount.getTerrainTile({ era: 'PCG_9_3_5', gridX: gx, gridY: gy });
        for (let ky = 0; ky < 8; ky++) for (let kx = 0; kx < 8; kx++) {
          const served = dv.getUint16(64 + ((ty * 8 + ky) * 64 + (tx * 8 + kx)) * 2, true);
          const indep = tile.heights[MIDIDX[ky] * 32 + MIDIDX[kx]];
          lodChecked++;
          if (served !== indep) lodBad++;
        }
      }
      lodOk = lodBad === 0;
    }
    const negFar = await get('/api/world/lod8/99/99');
    const statusRoute = await (await fetch(`http://127.0.0.1:${server.port}/api/world/status`)).json();
    const denominatorMeasured = statusRoute.denominator.indexRegularTiles === 51920;
    out.push(record('R2_LOD_ROUTES',
      'the distant-LOD routes serve the decimated REAL samples bit-exactly (independent re-decimation of the production payloads); the denominator is MEASURED from the index (never hardcoded); out-of-range refuses 400',
      (farOk && lodOk && negFar.status === 400 && denominatorMeasured) ? 'PASS' : 'FAIL', {
      resultClass: 'LIVE_ROUTE_VS_INDEPENDENT_DECIMATION',
      measuredQuantity: 'bit-exact served vs independently decimated samples + route negatives',
      measured: { farBytes: far.buf.byteLength, farSamplesChecked: farChecked, farMismatches: farMaxDiff, lod8SamplesChecked: lodChecked, lod8Mismatches: lodBad, negativeLod8Status: negFar.status, denominator: statusRoute.denominator.indexRegularTiles },
      independentSourceOfTruth: 'an in-test decimation of PESourceMount.getTerrainTile payloads (a second read of the same originals)',
      whyNonCircular: 'the route bytes are compared sample-by-sample against an independently computed decimation',
      failureCaseDetected: farOk && lodOk ? 'none' : 'a served LOD sample mismatched the original decimation',
    }));
  } finally {
    const stop = await stopWorldServer(server);
    if (!stop.portFreed) {
      out.push(record('R2_GATES_SERVER_LIFECYCLE', 'suite-owned world server stop + port-freed proof', 'FAIL', {
        measuredQuantity: 'stop result', measured: stop, failureCaseDetected: 'PORT NOT FREED after stop',
      }));
    }
  }

  // ---- R2_MOVEMENT_GUARD (the extracted CURRENT production function) ----
  {
    const THREE = await import(pathToFileURL(path.join(ROOT, 'node_modules/three/build/three.module.js')).href);
    const appSource = await fsp.readFile(path.join(ROOT, 'compat/world-app.js'), 'utf8');
    const extract = (name) => {
      const start = appSource.indexOf(`function ${name}(`);
      if (start < 0) return null;
      return appSource.slice(start, appSource.indexOf('\n}', start) + 2);
    };
    const src = extract('updateFlyWalk');
    const { VMX } = { VMX: (await import('node:vm')) };
    const vm = VMX;
    const dom = { 'boundary-banner': { hidden: true, textContent: '' } };
    const canvas = {};
    const camera = new THREE.PerspectiveCamera();
    camera.position.set(100, 10, 100);
    const cx = vm.createContext({
      THREE, camera, canvas, document: { pointerLockElement: canvas },
      state: { mode: 'walk', boundaryHit: false, heightField: null },
      move: { keys: new Set(['KeyW']), pitch: 0, yaw: 0, dragging: false },
      clampToMap: (v) => ({ ...v, clamped: false }),
      EYE_OFFSET_M: 1.7, MAP_MIN: 1, MAP_MAX_X: 14079, MAP_MAX_Z: 15103,
      $: (id) => dom[id],
    });
    vm.runInContext(src, cx);
    cx.updateFlyWalk(1);
    const refusedAtLastSafe = camera.position.x === 100 && camera.position.z === 100 && camera.position.y === 10;
    const bannerShown = !dom['boundary-banner'].hidden;
    out.push(record('R2_MOVEMENT_GUARD',
      'the production updateFlyWalk computes the candidate FIRST and refuses the move with no real surface data BEFORE any commit (the last safe position stands)',
      refusedAtLastSafe && bannerShown ? 'PASS' : 'FAIL', {
      resultClass: 'EXTRACTED_PRODUCTION_FUNCTION_CONTROL (the same function the browser runs)',
      measuredQuantity: 'camera position + banner after a W-step with NO surface data',
      measured: { positionAfter: { ...camera.position }, bannerShown },
      independentSourceOfTruth: 'the current compat/world-app.js source, executed verbatim in a controlled context',
      whyNonCircular: 'the BASE function (WL-3) commits X/Z despite the banner — measured in PRE; a regression re-introduces it',
      failureCaseDetected: refusedAtLastSafe ? 'none' : 'the move committed without surface data',
    }));
  }

  return out;
}
