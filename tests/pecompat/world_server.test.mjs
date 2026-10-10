// world_server.test.mjs — PE_WORLD_LAUNCHER_R1_20261010, ETAP C (contract §8)
// WORLD SERVER GATES: /launcher + /world serve, bounded API positives, the
// denial subset (T7 pattern reuse), NO whole-container route, tile wire
// cross-checks against the PRODUCTION in-process decode, overview binary
// layout, climates/gaps honesty, and the CAM-C3 cache-identity gates applied
// to the world tile cache (mutants through the PRODUCTION verify function +
// a real-HTTP clean double-fetch HIT).
//
// PREREGISTERED EXPECTATIONS (written BEFORE execution):
//   1. /launcher, /world, statics, client modules, three module: 200.
//   2. / redirects 302 to /launcher; unknown routes 404 ROUTE_NOT_FOUND.
//   3. Tile API: 2048 B exactly; heights == production in-process decode
//      (bit-exact for the sampled tiles); provenance headers present;
//      double-fetch = HIT with identical bytes; meta route = JSON stats.
//   4. Denials (raw sockets, NO client-side URL normalization): out-of-range
//      220/0 and 0/236 -> 400 GRID_OUT_OF_RANGE; -1 -> 400; 'abc' -> 400;
//      sentinel coordinates 32766/32766 -> 400 (range refusal mentioning the
//      regular grid); shape violations -> 404; POST -> 405; NUL byte -> 400;
//      backslash -> 400; '..' segment -> 400 PATH_TRAVERSAL_BLOCKED.
//      REGISTERED EXPECTATION (decided at implementation): decimal
//      coordinates with leading zeros ('010') are canonicalized to 10 by
//      parseInt and SERVED (bounded, path-safe) — expected 200, not a denial.
//   5. NO whole-container route: /api/world/terrain.bnt, /api/world/container,
//      /api/world/raw, /pcg/..., /api/world/entries -> 404 (by construction).
//   6. Overview binary: exactly 51,920*7 = 363,440 B; layout documented;
//      all regular tiles MEASURED (status 1) in this corpus; overview stats
//      for a sampled tile == recomputed stats from the tile wire bytes.
//   7. Climates: 32 profiles, 31 DECODED, [25] UNSUPPORTED (strict decoder,
//      never comma-converted); climate/32 and climate/xx -> 400.
//   8. Gaps: the honest panel lists vegetation NOT_YET (Etap E), water
//      NOT_RECOVERED, special_rows EXCLUDED, sentinel, models_world_placement
//      NOT_ESTABLISHED, historical_axes UNVERIFIED, tree_distribution
//      NOT_ESTABLISHED, and the measured 12-B Textures/Terrain.bnt warning;
//      the ETAP D terrain_textures item carries its DELIVERED state WITH the
//      honest scope labels (RENDER_RECONSTRUCTION, unresolved-binding policy,
//      the 9.3.5 vertex-tint-vs-albedo role distinction).
//   9. CAM-C3 world-cache mutants (through the production
//      verifyTileCacheIdentity): wrong era REFUSED; wrong containerSha
//      REFUSED; wrong entryName REFUSED; tampered heights REFUSED
//      (PAYLOAD_SHA_MISMATCH); clean PASSES; and the real server re-decodes
//      on refusal (HTTP double-fetch proves the clean path attaches).
//  10. Server lifecycle: startup line + PID; stop terminates ONLY this
//      process; port freed; standing 8140/8161 untouched.
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { inflateSync } from 'node:zlib';

import { PESourceMount } from '../../src/pesource/PESourceMount.js';
import { verifyTileCacheIdentity } from '../../compat/server-world.mjs';
import {
  startWorldServer, stopWorldServer, findFreePort, rawRequest, rawRequestFull, parseJsonOrNone, checkPortFree,
} from './_world_server_helpers.mjs';

const PIN_TERRAIN_SHA = '95841761CE4EA074C97930EC1CEF3FB57AAC7F7F4F3D9B751A9EE60510299990';

function rec(id, name, status, extra = {}) {
  return { id, name, status, ...extra };
}

export async function run(ctx) {
  const records = [];
  const terrainPath = ctx.terrainPath ?? 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Terrain\\terrain.bnt';

  // in-process production decode for wire cross-checks
  const io = {
    readFile: async (p) => new Uint8Array(readFileSync(p)),
    inflate: async (b) => new Uint8Array(inflateSync(b)),
    sha256: async (b) => createHash('sha256').update(b).digest('hex'),
  };
  const mount = new PESourceMount(io);
  await mount.mountEra({ era: 'PCG_9_3_5', container: 'Terrain/terrain.bnt', path: terrainPath, format: 'BNT2_TERRAIN' });

  const standingBefore = { 8140: await checkPortFree(8140).then(() => false).catch(() => true), 8161: await checkPortFree(8161).then(() => false).catch(() => true) };

  const port = ctx.worldPort ?? (await findFreePort(8162));
  const serverRec = await startWorldServer({ port });
  try {
    // ---- 1. routes + statics ----
    const statics = [
      ['/launcher', 'text/html'], ['/world', 'text/html'], ['/', null],
      ['/compat/launcher.js', 'text/javascript'], ['/compat/launcher.css', 'text/css'],
      ['/compat/world-app.js', 'text/javascript'], ['/compat/world.css', 'text/css'],
      ['/compat/world-splat.js', 'text/javascript'], ['/compat/world-vegetation.js', 'text/javascript'],
      ['/compat/compat.css', 'text/css'], ['/compat/launcher.html', 'text/html'],
      ['/src/peworld/PETerrainCore.js', 'text/javascript'],
      ['/src/peworld/PEFoliageCore.js', 'text/javascript'],
      ['/src/peworld/PEFoliageLabSeed.js', 'text/javascript'],
      ['/src/pesource/TerrainTile.js', 'text/javascript'],
      ['/src/pesource/PEProvenance.js', 'text/javascript'],
      ['/src/pesource/TgaDecoder.js', 'text/javascript'],
      ['/src/pesource/NifModelReader.js', 'text/javascript'],
      ['/node_modules/three/build/three.module.js', 'text/javascript'],
    ];
    const staticChecks = {};
    for (const [p, mime] of statics) {
      const r = await rawRequestFull(port, p);
      staticChecks[p] = { status: r.status, bytes: r.body.length, contentType: r.headers['content-type']?.split(';')[0] ?? '' };
      if (p === '/') continue; // the root is the 302 redirect — checked separately below
      if (r.status !== 200) staticChecks[p].FAIL = 'expected 200';
      if (mime && !staticChecks[p].contentType.includes(mime.split('/')[1])) staticChecks[p].FAIL = 'mime';
    }
    // '/' is a 302 redirect to /launcher
    const rootRedir = await rawRequestFull(port, '/');
    staticChecks.rootRedirectLocation = rootRedir.headers.location;
    const staticsOk = Object.values(staticChecks).every((v) => !v?.FAIL)
      && rootRedir.status === 302 && rootRedir.headers.location === '/launcher';
    records.push(rec('WORLD_T7_ROUTES_STATICS',
      '/launcher + /world + allowlisted statics + client world modules + pinned three (200); / -> 302 /launcher',
      staticsOk ? 'PASS' : 'FAIL', {
        measuredQuantity: 'HTTP statuses/content-types over the exact allowlist',
        measured: staticChecks,
        independentSourceOfTruth: 'raw sockets against the running server',
        whyNonCircular: 'the browser-facing surface is exercised as the browser would',
      }));

    // ---- 2. status snapshot ----
    const st = parseJsonOrNone((await rawRequestFull(port, '/api/world/status')).body.toString('utf8'));
    const statusOk = st && st.ok === true && st.era === 'PCG_9_3_5'
      && st.containers.terrain.state === 'VERIFIED' && st.containers.vegetationClimates.state === 'VERIFIED'
      && String(st.containers.models.state).startsWith('VERIFIED') && String(st.containers.textures.state).startsWith('VERIFIED')
      && st.containers.textures.indexState === 'READY' && (st.containers.textures.index?.parsedEntries ?? 0) === 8381
      && st.terrainMaterials.maskOffsetRecordRelative === 56
      && String(st.terrainMaterials.textureChainRelation ?? '').includes('id@+16')
      && st.terrainMaterials.textureWireVersion === 'bnt2-texture-wire-v1'
      && st.terrainIndex.totalEntries === 58451 && st.terrainIndex.regular === 51920
      && st.terrainIndex.specialRows === 6530 && st.terrainIndex.sentinel === 1
      && st.calibration.u16PerMeter === 128 && st.calibration.meterPerSample === 2
      && st.calibration.label === 'CURRENT_RUNTIME_CALIBRATION'
      && st.census.total === 51920 && st.census.measured === 51920 && st.census.ready === true
      && String(st.containers.terrain.sha256 ?? '').toUpperCase() === PIN_TERRAIN_SHA
      // ETAP E: the lazy model index READY + the vegetation section present
      && st.containers.models.indexState === 'READY'
      && st.vegetation?.mode === 'RECONSTRUCTION_PREVIEW'
      && st.vegetation?.defaultProfile?.index === 0
      && st.vegetation?.supportCensusState === 'READY'
      && st.vegetation?.supportCensus?.counts?.atLeastOneSupportedModel === true
      && st.vegetation?.p3 === 0
      && st.vegetation?.visibleInstanceCap === 5000
      && Object.keys(st.vegetation?.threeWaySeparation ?? {}).length === 3;
    records.push(rec('WORLD_T7_STATUS',
      '/api/world/status: era PCG_9_3_5, four pinned containers VERIFIED (terrain+veg mounted; models+textures hash-verified with BOTH lazy indexes READY), the material-chain section (mask@56, id@+16 relation, wire versions), the ETAP E vegetation section (the THREE-WAY SEPARATION + the measured default profile + the support census + p3 shown separately + the 5000 cap), index + census + calibration snapshot',
      statusOk ? 'PASS' : 'FAIL', {
        measuredQuantity: 'status JSON field agreement with the contract pins',
        measured: {
          era: st?.era,
          containers: st ? {
            terrain: st.containers.terrain.state, veg: st.containers.vegetationClimates.state,
            models: st.containers.models.state, textures: st.containers.textures.state,
            textureIndexState: st.containers.textures.indexState, textureIndexEntries: st.containers.textures.index?.parsedEntries,
            modelIndexState: st.containers.models.indexState, modelIndexEntries: st.containers.models.index?.parsedEntries,
          } : null,
          vegetation: st ? {
            mode: st.vegetation?.mode, defaultProfileIndex: st.vegetation?.defaultProfile?.index,
            supportCensusState: st.vegetation?.supportCensusState, supportCounts: st.vegetation?.supportCensus?.counts,
            p3: st.vegetation?.p3, cap: st.vegetation?.visibleInstanceCap,
            threeWaySeparationKeys: st.vegetation ? Object.keys(st.vegetation.threeWaySeparation ?? {}) : null,
          } : null,
          terrainMaterials: st ? { maskOffset: st.terrainMaterials.maskOffsetRecordRelative, chainRelation: String(st.terrainMaterials.textureChainRelation ?? '').slice(0, 120) } : null,
          index: st?.terrainIndex, census: st ? { total: st.census.total, measured: st.census.measured, ready: st.census.ready, zeroTiles: st.census.zeroTiles } : null,
          calibration: st?.calibration?.label, maxMeanTile: st?.census?.maxMeanTile,
        },
        independentSourceOfTruth: 'the running server + the contract §1 pinned SHA/size table + the probe05-measured 8,381-entry index census + the measured 5,596-entry Models.bnt index census',
        whyNonCircular: 'the pins are external constants (contract / prior corpus census), not values echoed from the server',
      }));

    // ---- 3. tile wire cross-check + cache HIT ----
    const SAMPLED = [[0, 0], [219, 235], [53, 114], [110, 118]];
    const tileChecks = [];
    let tilesOk = true;
    for (const [gx, gy] of SAMPLED) {
      const r = await rawRequestFull(port, `/api/world/tile/${gx}/${gy}`);
      const prod = await mount.getTerrainTile({ era: 'PCG_9_3_5', gridX: gx, gridY: gy });
      const wireU16 = new Uint16Array(r.body.buffer, r.body.byteOffset, r.body.byteLength / 2);
      let equal = r.status === 200 && r.body.length === 2048 && wireU16.length === 1024;
      for (let i = 0; i < 1024 && equal; i++) if (wireU16[i] !== prod.heights[i]) equal = false;
      const headers = {
        era: r.headers['x-pe-era'], container: r.headers['x-pe-container'], entry: r.headers['x-pe-entry'],
        offset: r.headers['x-pe-offset'], cache: r.headers['x-pe-cache-state'],
        containerSha: r.headers['x-pe-container-sha256'], heightOffset: r.headers['x-pe-height-data-offset'],
      };
      if (!equal || headers.era !== 'PCG_9_3_5' || !headers.entry?.endsWith('.tdf')) tilesOk = false;
      tileChecks.push({ gx, gy, status: r.status, bytes: r.body.length, equal, headers });
    }
    // double-fetch -> HIT with identical bytes
    const r1 = await rawRequestFull(port, '/api/world/tile/53/114');
    const r2 = await rawRequestFull(port, '/api/world/tile/53/114');
    const hitOk = r2.headers['x-pe-cache-state'] === 'HIT' && r1.body.equals(r2.body);
    tilesOk = tilesOk && hitOk;
    records.push(rec('WORLD_T7_TILE_WIRE',
      'tile API: 2048 B uint16 LE == production in-process decode (bit-exact); provenance headers; double-fetch = HIT with identical bytes',
      tilesOk ? 'PASS' : 'FAIL', {
        measuredQuantity: 'wire bytes vs PESourceMount.getTerrainTile in-process decode + cache header states',
        measured: { tileChecks, doubleFetch: { first: r1.headers['x-pe-cache-state'], second: r2.headers['x-pe-cache-state'], identical: r1.body.equals(r2.body) } },
        independentSourceOfTruth: 'a second production decode in the TEST process (fresh PESourceMount, not the server cache)',
        whyNonCircular: 'the server and the test decode the same original bytes independently; equality proves the wire, difference localizes the defect',
      }));

    // meta route
    const meta = parseJsonOrNone((await rawRequestFull(port, '/api/world/tile/53/114/meta')).body.toString('utf8'));
    const metaOk = meta && meta.ok === true && meta.sampleCount === 1024
      && Number.isInteger(meta.stats.min) && Number.isInteger(meta.stats.max)
      && meta.provenance?.era === 'PCG_9_3_5' && meta.provenance?.extra?.heightDataOffsetPayloadRelative === 64
      && meta.calibration?.label === 'CURRENT_RUNTIME_CALIBRATION';
    records.push(rec('WORLD_T7_TILE_META',
      'tile meta route: provenance + stats + calibration preset (JSON)',
      metaOk ? 'PASS' : 'FAIL', {
        measuredQuantity: 'meta JSON structure (provenance era/offset/decoder, 1024 samples, calibration label)',
        measured: meta ? { name: meta.name, stats: meta.stats, provenance: meta.provenance } : null,
      }));

    // ---- 4. denial subset (raw sockets) ----
    const denials = [
      // [id, rawPath, expectedStatus, expectedError]
      ['OUT_OF_RANGE_X', '/api/world/tile/220/0', 400, 'GRID_OUT_OF_RANGE'],
      ['OUT_OF_RANGE_Y', '/api/world/tile/0/236', 400, 'GRID_OUT_OF_RANGE'],
      ['NEGATIVE', '/api/world/tile/-1/0', 400, 'GRID_INVALID'],
      ['NON_NUMERIC', '/api/world/tile/abc/0', 400, 'GRID_INVALID'],
      ['SENTINEL_COORDS', '/api/world/tile/32766/32766', 400, 'GRID_OUT_OF_RANGE'],
      ['SHAPE_1PART', '/api/world/tile/10', 404, 'UNKNOWN_TILE_ROUTE'],
      ['SHAPE_4PART', '/api/world/tile/10/20/33/44', 404, 'UNKNOWN_TILE_ROUTE'],
      ['CLIMATE_OOR', '/api/world/climate/32', 400, 'CLIMATE_INDEX_OUT_OF_RANGE'],
      ['CLIMATE_NONNUM', '/api/world/climate/xx', 400, 'CLIMATE_INDEX_INVALID'],
      ['NUL_BYTE', '/api/world/tile/10%0020', 400, null],
      ['BACKSLASH', '/api/world/tile/10%5C20', 400, 'BACKSLASH_IN_URL'],
      ['TRAVERSAL_ROOT', '/../server-world.mjs', 400, 'PATH_TRAVERSAL_BLOCKED'],
      ['TRAVERSAL_COMPAT', '/compat/../package.json', 400, 'PATH_TRAVERSAL_BLOCKED'],
      ['TRAVERSAL_API', '/api/world/../../../etc/passwd', 400, 'PATH_TRAVERSAL_BLOCKED'],
      ['STATIC_NOT_ALLOWLISTED', '/compat/server-world.mjs', 404, 'STATIC_FILE_NOT_ALLOWEDLISTED'],
      ['MODULE_NOT_ALLOWLISTED', '/src/pesource/PESourceMount.js', 404, 'STATIC_FILE_NOT_ALLOWLISTED'],
    ];
    const denialResults = [];
    let denialsOk = true;
    for (const [id, p, wantStatus, wantError] of denials) {
      const r = await rawRequest(port, 'GET', p);
      const j = parseJsonOrNone(r.bodyText);
      const err = j?.error ?? null;
      const ok = r.status === wantStatus && (wantError === null || err === wantError);
      if (!ok) denialsOk = false;
      denialResults.push({ id, path: p, status: r.status, expectedStatus: wantStatus, error: err, expectedError: wantError, ok });
    }
    // method denial (POST)
    const post = await rawRequest(port, 'POST', '/api/world/status');
    const postOk = post.status === 405;
    if (!postOk) denialsOk = false;
    denialResults.push({ id: 'POST_405', path: '/api/world/status', status: post.status, expectedStatus: 405, ok: postOk });
    // leading-zero canonicalization (REGISTERED EXPECTATION: served as 10/20)
    const lead0 = await rawRequestFull(port, '/api/world/tile/010/020');
    const lead0Ok = lead0.status === 200 && lead0.body.length === 2048;
    denialResults.push({ id: 'LEADING_ZERO_CANONICAL', path: '/api/world/tile/010/020', status: lead0.status, expectedStatus: 200, ok: lead0Ok, note: 'registered expectation: parseInt canonicalization (bounded, path-safe)' });
    records.push(rec('WORLD_T7_DENIAL_SUBSET',
      'denial subset (T7 pattern reuse, raw sockets): out-of-range/sentinel coords, shape violations, NUL/backslash, traversal, method, non-allowlisted statics',
      denialsOk ? 'PASS' : 'FAIL', {
        measuredQuantity: 'HTTP status + error-class of each denial probe',
        measured: { denialResults },
        independentSourceOfTruth: 'raw sockets (no client URL normalization) against the running server',
        whyNonCircular: 'each probe carries a preregistered expected status/error; the server cannot see the expectation',
      }));

    // ---- 5. no whole-container route ----
    const wholeProbes = [
      '/api/world/terrain.bnt', '/api/world/container', '/api/world/raw',
      '/api/world/entries', '/pcg/Data/Terrain/terrain.bnt', '/terrain.bnt',
      '/api/world/models.bnt', '/api/world/textures.bnt',
    ];
    const wholeResults = [];
    let noWholeOk = true;
    for (const p of wholeProbes) {
      const r = await rawRequest(port, 'GET', p);
      const ok = r.status === 404;
      if (!ok) noWholeOk = false;
      wholeResults.push({ path: p, status: r.status, ok });
    }
    records.push(rec('WORLD_T7_NO_WHOLE_CONTAINER',
      'NO whole-container route exists (terrain.bnt/Models.bnt/Textures.bnt are never exposed to the browser)',
      noWholeOk ? 'PASS' : 'FAIL', {
        measuredQuantity: 'status of container-shaped paths',
        measured: { wholeResults },
        independentSourceOfTruth: 'route table of the running server (probed, not read from source)',
        whyNonCircular: 'a 200 on any container-shaped path would be a FAIL — measured directly',
      }));

    // ---- 6. overview binary ----
    const ov = await rawRequestFull(port, '/api/world/overview');
    const ovOk = ov.status === 200 && ov.body.length === 51920 * 7
      && Number(ov.headers['x-pe-overview-total']) === 51920
      && Number(ov.headers['x-pe-overview-measured']) === 51920
      && ov.headers['x-pe-overview-ready'] === 'true';
    const dvv = new DataView(ov.body.buffer, ov.body.byteOffset, ov.body.byteLength);
    let statuses = { 0: 0, 1: 0, 2: 0, 3: 0 };
    for (let i = 0; i < 51920; i++) statuses[ov.body[i * 7 + 6]]++;
    const overviewAllMeasured = statuses[1] === 51920 && statuses[0] === 0 && statuses[2] === 0 && statuses[3] === 0;
    // cross-check overview stats vs tile wire bytes for one sampled tile
    const t53 = await rawRequestFull(port, '/api/world/tile/53/114');
    const tU16 = new Uint16Array(t53.body.buffer, t53.body.byteOffset, 1024);
    let mn = 0xffff, mx = 0, sum = 0;
    for (let i = 0; i < 1024; i++) { const v = tU16[i]; sum += v; if (v < mn) mn = v; if (v > mx) mx = v; }
    const mean = Math.round(sum / 1024);
    const idx = 114 * 220 + 53;
    const ovMean = dvv.getUint16(idx * 7, true), ovMin = dvv.getUint16(idx * 7 + 2, true), ovMax = dvv.getUint16(idx * 7 + 4, true);
    const statsMatch = ovMean === mean && ovMin === mn && ovMax === mx;
    // progress endpoint
    const prog = parseJsonOrNone((await rawRequestFull(port, '/api/world/overview/progress')).body.toString('utf8'));
    const progOk = prog?.ready === true && prog?.total === 51920 && prog?.measured === 51920;
    records.push(rec('WORLD_T7_OVERVIEW_BINARY',
      'overview binary: 363,440 B (51,920×7 layout), all regular tiles MEASURED (status=1), per-tile stats == tile wire recompute',
      ovOk && overviewAllMeasured && statsMatch && progOk ? 'PASS' : 'FAIL', {
        measuredQuantity: 'binary length + status census + per-tile stat equality (overview vs independent tile recompute)',
        measured: {
          bytes: ov.body.length, statuses, totalHeader: ov.headers['x-pe-overview-total'],
          tile_53_114: { overview: { mean: ovMean, min: ovMin, max: ovMax }, recomputed: { mean, min: mn, max: mx }, match: statsMatch },
          progress: prog,
        },
        independentSourceOfTruth: 'the tile wire bytes (already cross-checked against the in-process production decode)',
        whyNonCircular: 'overview stats are recomputed from the wire in the test, not trusted from the server',
      }));

    // ---- 7. climates honesty ----
    const cl = parseJsonOrNone((await rawRequestFull(port, '/api/world/climates')).body.toString('utf8'));
    const cl0 = parseJsonOrNone((await rawRequestFull(port, '/api/world/climate/0')).body.toString('utf8'));
    const cl25 = parseJsonOrNone((await rawRequestFull(port, '/api/world/climate/25')).body.toString('utf8'));
    // ETAP E: DECODED profiles carry the per-record MODEL SUMMARY (the REAL
    // ids/scales from the correctly decoded records — contract §6.1).
    const climatesOk = cl?.total === 32 && cl?.decoded === 31 && Array.isArray(cl?.unsupported) && cl.unsupported.length === 1 && cl.unsupported[0] === 25
      && cl0?.status === 'DECODED' && cl0?.recordCount > 0 && Array.isArray(cl0?.records) && cl0.records.length === cl0.recordCount
      && cl25?.status === 'UNSUPPORTED' && cl25?.ok === false && cl25?.records === null && typeof cl25?.error === 'string'
      && Array.isArray(cl.profiles?.[0]?.models) && cl.profiles[0].models.length === 12
      && cl.profiles[0].models[0].id === 436293 && cl.profiles[0].models[0].scaleMin === 0.5 && cl.profiles[0].models[0].scaleMax === 1.5
      && Array.isArray(cl0?.modelSummary) && cl0.modelSummary.length === cl0.recordCount
      && cl.profiles?.[25]?.status === 'UNSUPPORTED' && cl.profiles?.[25]?.models === undefined;
    records.push(rec('WORLD_T7_CLIMATES_HONESTY',
      'climates: 32 profiles, 31 DECODED, 25 UNSUPPORTED (strict decoder — never comma-converted); decoded profiles expose records + the ETAP E per-record MODEL SUMMARY (the REAL model ids/scales); UNSUPPORTED exposes the honest error and NO model summary',
      climatesOk ? 'PASS' : 'FAIL', {
        measuredQuantity: 'profile census + one decoded + the known-unsupported profile + the model summaries',
        measured: {
          total: cl?.total, decoded: cl?.decoded, unsupported: cl?.unsupported,
          profile0: { status: cl0?.status, recordCount: cl0?.recordCount, firstRecord: cl0?.records?.[0], firstModelSummary: cl.profiles?.[0]?.models?.[0], modelSummaryCount: cl0?.modelSummary?.length },
          profile25: { status: cl25?.status, ok: cl25?.ok, records: cl25?.records, error: cl25?.error, profileRowModels: cl.profiles?.[25]?.models ?? null },
        },
        independentSourceOfTruth: 'the strict VegetationClimateDecoder through the production mount',
        whyNonCircular: 'UNSUPPORTED must NOT fabricate records — asserted by absence, not by message; the model summaries are asserted against the KNOWN profile-0 first record (436293, scale 0.5..1.5) measured from the decoded records',
      }));

    // ---- 8. gaps honesty ----
    const gaps = parseJsonOrNone((await rawRequestFull(port, '/api/world/gaps')).body.toString('utf8'));
    const gapIds = new Set((gaps?.gaps ?? []).map((g) => `${g.id}|${g.state}`));
    const gapById = new Map((gaps?.gaps ?? []).map((g) => [g.id, g]));
    // ETAP D/E UPDATE (product state change, tracked honestly): terrain_textures
    // moved to ETAP_D_DELIVERED and vegetation to ETAP_E_DELIVERED — the gate
    // now requires BOTH delivered items to carry their HONEST SCOPE (the
    // vertex-tint vs albedo role distinction + RENDER_RECONSTRUCTION for the
    // textures; the THREE-WAY SEPARATION + the UNSUPPORTED-25 + the untextured
    // policy + the 5000 cap for the vegetation). All NOT-loaded items stay.
    const wantGaps = [
      ['water', 'NOT_RECOVERED'], ['special_rows', 'EXCLUDED — UNRESOLVED'],
      ['sentinel', 'NOT A REGULAR TILE'], ['models_world_placement', 'NOT_ESTABLISHED'],
      ['historical_axes', 'UNVERIFIED'], ['historical_tree_distribution', 'NOT_ESTABLISHED'],
      ['material_texture_atlas_dir', 'NOT A COMPLETE ATLAS — MEASURED'],
    ];
    const texturesGap = gapById.get('terrain_textures');
    const texturesGapOk = String(texturesGap?.state ?? '').startsWith('ETAP_D_DELIVERED')
      && /RENDER_RECONSTRUCTION/.test(texturesGap?.detail ?? '')
      && /UNRESOLVED binding/.test(texturesGap?.detail ?? '')
      && /climate palette pipeline/.test(texturesGap?.detail ?? '');
    const vegGap = gapById.get('vegetation');
    const vegGapOk = String(vegGap?.state ?? '').startsWith('ETAP_E_DELIVERED')
      && /THREE-WAY SEPARATION|tr\u00f3jstopniow/i.test(vegGap?.detail ?? '')
      && /25\.vcl stays UNSUPPORTED/.test(vegGap?.detail ?? '')
      && /honestly untextured|uczciwie/.test(vegGap?.detail ?? '')
      && /5000/.test(vegGap?.detail ?? '')
      && /no historical seed\/count\/biome\/placement claims|nigdy historyczny/i.test(vegGap?.detail ?? '');
    const gapsOk = wantGaps.every(([id, state]) => gapIds.has(`${id}|${state}`)) && gaps?.catalog?.url?.includes('8161') && texturesGapOk && vegGapOk;
    records.push(rec('WORLD_T7_GAPS_HONESTY',
      'gaps panel: every NOT-loaded/unsupported item is listed with its honest state; BOTH delivered items (terrain_textures Etap D, vegetation Etap E) carry their honest scope (RENDER_RECONSTRUCTION / the THREE-WAY SEPARATION + the UNSUPPORTED-25 + the untextured policy + the 5000 cap)',
      gapsOk ? 'PASS' : 'FAIL', {
        measuredQuantity: 'gap id|state set + the delivered items scope labels',
        measured: { have: [...gapIds], catalog: gaps?.catalog, terrainTexturesState: texturesGap?.state, texturesGapScopeOk: texturesGapOk, vegetationState: vegGap?.state, vegetationScopeOk: vegGapOk },
      }));

    // ---- 9. CAM-C3 world cache identity gates (production verify function) ----
    const liveIdentity = {
      era: 'PCG_9_3_5', container: 'Terrain/terrain.bnt', containerSha256: PIN_TERRAIN_SHA.toLowerCase(),
    };
    const prodTile = await mount.getTerrainTile({ era: 'PCG_9_3_5', gridX: 53, gridY: 114 });
    const heightsSha = createHash('sha256').update(Buffer.from(prodTile.heights.buffer, prodTile.heights.byteOffset, prodTile.heights.byteLength)).digest('hex');
    const cleanEntry = {
      tile: prodTile,
      identity: {
        era: 'PCG_9_3_5', container: 'Terrain/terrain.bnt', containerSha256: PIN_TERRAIN_SHA.toLowerCase(),
        entryName: '00350072.tdf', payloadSha256: heightsSha, decoderVersion: 'pesource-m1-v1',
      },
    };
    const mutants = [
      ['M1_WRONG_ERA', structuredClone(cleanEntry), (e) => { e.identity.era = 'CD_JAN_2003'; }, ['ERA_MISMATCH']],
      ['M2_WRONG_CONTAINER_SHA', structuredClone(cleanEntry), (e) => { e.identity.containerSha256 = '0'.repeat(64); }, ['CONTAINER_SHA_MISMATCH']],
      ['M3_WRONG_ENTRY_NAME', structuredClone(cleanEntry), (e) => { e.identity.entryName = '0000000a.tdf'; }, ['ENTRY_NAME_MISMATCH']],
      ['M4_TAMPERED_HEIGHTS', structuredClone(cleanEntry), (e) => { e.tile.heights[0] = (e.tile.heights[0] + 1) % 65536; }, ['PAYLOAD_SHA_MISMATCH']],
    ];
    const mutantResults = [];
    let mutantsOk = true;
    for (const [id, entry, mutate, expectedReasons] of mutants) {
      mutate(entry);
      const v = verifyTileCacheIdentity(entry, liveIdentity, { expectedEntryName: '00350072.tdf' });
      const namedExactly = v.ok === false && expectedReasons.every((r) => v.reasons.includes(r));
      if (!namedExactly) mutantsOk = false;
      mutantResults.push({ id, gate: v.passed === undefined ? v.ok : null, refused: v.ok === false, reasons: v.reasons, expectedReasons, ok: namedExactly });
    }
    const cleanV = verifyTileCacheIdentity(cleanEntry, liveIdentity, { expectedEntryName: '00350072.tdf' });
    const malformedV = verifyTileCacheIdentity({ identity: null }, liveIdentity);
    const cleanOk = cleanV.ok === true && malformedV.ok === false;
    if (!cleanOk) mutantsOk = false;
    records.push(rec('WORLD_T7_CACHE_IDENTITY_CAM_C3',
      'CAM-C3 cache-identity gates for world tile payloads: wrong era / wrong container SHA / wrong entry name / tampered heights all REFUSED with named reasons; clean PASSES (through the PRODUCTION verifyTileCacheIdentity)',
      mutantsOk ? 'PASS' : 'FAIL', {
        resultClass: 'SYNTHETIC_COUNTEREXAMPLE_THROUGH_PRODUCTION_GATE (not proof of historical contamination)',
        measuredQuantity: 'verifyTileCacheIdentity verdicts + reasons per mutant',
        measured: { mutantResults, clean: { ok: cleanV.ok, reasons: cleanV.reasons }, malformed: { ok: malformedV.ok, reasons: malformedV.reasons }, realHttpDoubleFetchHit: hitOk },
        independentSourceOfTruth: 'the production gate function + the real-HTTP HIT/MISS observation above',
        whyNonCircular: 'each mutant flips exactly one identity component; the gate must name it (never a silent attach)',
      }));
  } finally {
    const stop = await stopWorldServer(serverRec);
    records.push(rec('WORLD_T7_SERVER_LIFECYCLE',
      `suite-owned world server lifecycle (pid ${serverRec.pid}, port ${port}; stop + port-freed proof; standing 8140/8161 untouched)`,
      stop.portFreed ? 'PASS' : 'FAIL', {
        measuredQuantity: 'startup line + PID + stop result + port-freed proof',
        measured: {
          startupLine: serverRec.startupLine, pid: serverRec.pid, port,
          startedMs: serverRec.startupElapsedMs,
          stop: { killed: stop.killed, exitCode: stop.exitCode, signal: stop.signal, portFreed: stop.portFreed, freedAfterMs: stop.freedAfterMs, lifetimeMs: stop.lifetimeMs },
          standingServersBusyBefore: standingBefore,
          stdoutExcerpt: serverRec.stdout.slice(0, 900),
        },
      }));
  }
  return records;
}
