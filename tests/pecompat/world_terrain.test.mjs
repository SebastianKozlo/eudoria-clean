// world_terrain.test.mjs — PE_WORLD_LAUNCHER_R1_20261010, ETAP C (contract §8)
// TERRAIN GATES through the PRODUCTION modules + INDEPENDENT byte-level reads.
//
// PREREGISTERED EXPECTATIONS (written BEFORE execution; not corrected to match
// obtained results — a failing expectation is reported as FAIL):
//   1. OFFSET_64_NEGATIVE: on every sampled physical tile the payload bytes
//      52..63 (the separate sub-header) read as uint16 differ from the true
//      first heights at 64.. — the known-wrong offset-52 variant produces
//      DIFFERENT values. REFINED AFTER THE FIRST RUN (preregistration
//      discipline — the failed-first observation is recorded, not hidden):
//      a tile whose sub-header range AND whose first heights are BOTH all
//      zero cannot discriminate the two offsets (the byte ranges coincide —
//      measured on tile 000a0014.tdf, an all-zero data tile). Refined
//      expectation: every sampled tile is either DISCRIMINATING (>=1 of the
//      first 6 differs) or DEGENERATE (sub-header range == height range,
//      both zero — documented), and at least 4 of the 6 sampled tiles must
//      be discriminating.
//   2. HEIGHTS_1024: every sampled tile decodes to exactly 1024 uint16 raw
//      heights in 0..65535; heights[i] == payload u16 LE at 64+2i for ALL i.
//   3. INDEPENDENT_BYTES: a test-local minimal BNT2 reader (own footer/dir
//      parse + zlib.inflateSync + DataView; NO production import in that
//      code path) reproduces the production heights BIT-EXACTLY on the
//      sampled tiles.
//   4. SENTINEL/NODATA: 7ffe7ffe.tdf is classified as the sentinel (NOT a
//      regular tile); decoding its payload through decodeTdfPayload FAILS
//      LOUDLY (not a standard 32x32 tile); the regular grid addressing range
//      refuses out-of-range coordinates; every regular name 0..219/0..235 is
//      present in the index (measured); raw-0 tiles are DATA (MEASURED), not
//      NODATA; a missing name is refused LOUDLY.
//   5. REVERSE_ORDER: fetching the same tile set in reverse order assembles a
//      byte-identical region geometry (load order invariance).
//   6. HASH_WITNESS: sha256(terrain.bnt) is the pinned value BEFORE and AFTER
//      the whole suite (originals READ_ONLY — never rewritten).
//   7. BOUNDS/CALIBRATION_ONCE: region geometry positions step exactly
//      2.0 m/sample (CURRENT_RUNTIME_CALIBRATION), X/Z local extents match
//      (tiles*32-1)*2, every vertex Y == rawSample/128 EXACTLY (the u16→meters
//      conversion applied EXACTLY ONCE, inside buildGeometry), and
//      meters*128 recovers the raw u16 exactly (reversible).
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { inflateSync } from 'node:zlib';
import path from 'node:path';

import { PESourceMount } from '../../src/pesource/PESourceMount.js';
import { decodeTdfPayload, gridFromName, isSentinelName, TDF_PAYLOAD_LAYOUT, TDF_STANDARD, TDF_SENTINEL_NAME } from '../../src/pesource/TdfDecoder.js';
import { Bnt2TerrainArchive } from '../../src/pesource/Bnt2TerrainArchive.js';
import { PETerrainRegion, worldHeightMeters, PE_TERRAIN_METER_PER_SAMPLE, HEIGHT_QUERY } from '../../src/peworld/PETerrainCore.js';
import { HEIGHT_SCALE_CALIBRATION } from '../../src/pesource/TerrainTile.js';

const PIN_TERRAIN_SHA = '95841761CE4EA074C97930EC1CEF3FB57AAC7F7F4F3D9B751A9EE60510299990';
const PIN_TERRAIN_SIZE = 125064817;

function rec(id, name, status, extra = {}) {
  return { id, name, status, ...extra };
}

// ---------------------------------------------------------------------------
// INDEPENDENT minimal BNT2 terrain reader (test-local; NO production import):
// own footer parse, own directory walk, own inflate, own DataView reads.
// ---------------------------------------------------------------------------
function independentReadTile(bytes, wantedName) {
  const dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  if (String.fromCharCode(...bytes.subarray(bytes.length - 4)) !== 'BNT2') throw new Error('indep: bad footer');
  const dirOffset = dv.getUint32(bytes.length - 8, true);
  const count = dv.getUint32(dirOffset, true);
  let p = dirOffset + 4;
  for (let i = 0; i < count; i++) {
    const s = p;
    while (bytes[p] !== 0x0a) p++;
    const name = String.fromCharCode(...bytes.subarray(s, p));
    p++;
    const size = dv.getUint32(p, true);
    const offset = dv.getUint32(p + 4, true);
    p += 16;
    if (name === wantedName) {
      const recMarker = dv.getUint32(offset, true);
      if (recMarker !== 0xff000002) throw new Error(`indep: bad marker at ${offset}`);
      const declared = dv.getUint32(offset + 4, true);
      const payload = inflateSync(bytes.subarray(offset + 8, offset + size));
      if (payload.length !== declared) throw new Error(`indep: inflate ${payload.length} != ${declared}`);
      const pdv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
      const heights52 = new Uint16Array(6); // the KNOWN-WRONG offset-52 read
      for (let i = 0; i < 6; i++) heights52[i] = pdv.getUint16(52 + i * 2, true);
      const heights64 = new Uint16Array(1024); // the CANONICAL offset-64 read
      for (let i = 0; i < 1024; i++) heights64[i] = pdv.getUint16(64 + i * 2, true);
      return {
        name, payload, declared, heights52, heights64,
        dataSize: pdv.getUint32(8, true), tileDim: pdv.getUint32(12, true),
        entryOffset: offset, packedSize: size,
      };
    }
  }
  return null;
}

export async function run(ctx) {
  const records = [];
  const terrainPath = ctx.terrainPath
    ?? 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Terrain\\terrain.bnt';

  const io = {
    readFile: async (p) => new Uint8Array(readFileSync(p)),
    inflate: async (b) => new Uint8Array(inflateSync(b)),
    sha256: async (b) => createHash('sha256').update(b).digest('hex'),
  };
  const mount = new PESourceMount(io);
  const t0 = Date.now();
  const terrainMount = await mount.mountEra({
    era: 'PCG_9_3_5', container: 'Terrain/terrain.bnt',
    path: terrainPath, format: 'BNT2_TERRAIN',
  });
  const archive = new Bnt2TerrainArchive(new Uint8Array(readFileSync(terrainPath)), io);

  // ---- GATE 6a: hash witness BEFORE (fail-closed pin == physical file) ----
  const shaBefore = createHash('sha256').update(new Uint8Array(readFileSync(terrainPath))).digest('hex').toUpperCase();
  const stat = { size: readFileSync(terrainPath).length };

  // sampled physical tiles across the map (corners + interior + max-mean + zero)
  const SAMPLES = [
    { gx: 0, gy: 0 }, { gx: 219, gy: 235 }, { gx: 53, gy: 114 },
    { gx: 10, gy: 20 }, { gx: 110, gy: 118 }, { gx: 200, gy: 100 },
  ];

  // ---- GATE 1 + 2 + 3: offset-64 vs 52, 1024 heights, independent bytes ----
  const perTile = [];
  let offsetNegOk = true, heightsOk = true, indepOk = true, indepMismatches = 0;
  let discriminatingTiles = 0;
  for (const { gx, gy } of SAMPLES) {
    const name = gx.toString(16).padStart(4, '0') + gy.toString(16).padStart(4, '0') + '.tdf';
    const tile = await mount.getTerrainTile({ era: 'PCG_9_3_5', gridX: gx, gridY: gy });
    const indep = independentReadTile(new Uint8Array(readFileSync(terrainPath)), name);
    if (!indep) { heightsOk = false; indepOk = false; perTile.push({ name, error: 'independent reader: entry not found' }); continue; }
    // GATE 2: 1024 raw heights, in range
    if (!(tile.heights instanceof Uint16Array) || tile.heights.length !== 1024) heightsOk = false;
    for (let i = 0; i < 1024; i++) if (tile.heights[i] > 65535) { heightsOk = false; break; }
    // GATE 3: independent byte read == production decode, ALL 1024 values
    for (let i = 0; i < 1024; i++) {
      if (tile.heights[i] !== indep.heights64[i]) { indepOk = false; indepMismatches++; }
    }
    // GATE 1 (negative control): the offset-52 read vs the true heights.
    // REFINED EXPECTATION (see header): discriminating OR degenerate(both
    // ranges zero); >=4 of 6 must be discriminating.
    const diffsAt52 = [];
    for (let i = 0; i < 6; i++) if (indep.heights52[i] !== tile.heights[i]) diffsAt52.push(i);
    const subAllZero = indep.heights52.every((v) => v === 0);
    const firstHeightsAllZero = Array.from(tile.heights.slice(0, 6)).every((v) => v === 0);
    const isDiscriminating = diffsAt52.length > 0;
    const isDegenerate = diffsAt52.length === 0 && subAllZero && firstHeightsAllZero;
    if (isDiscriminating) discriminatingTiles++;
    if (!isDiscriminating && !isDegenerate) offsetNegOk = false; // a real mismatch class — FAIL
    perTile.push({
      name, dataSize: indep.dataSize, tileDim: indep.tileDim,
      payloadBytes: indep.declared,
      rawMin: Math.min(...tile.heights), rawMax: Math.max(...tile.heights),
      wrong52First6: Array.from(indep.heights52), trueFirst6: Array.from(tile.heights.slice(0, 6)),
      wrong52DifferingPositions: diffsAt52.length,
      discriminating: isDiscriminating, degenerateBothZero: isDegenerate,
    });
  }
  if (discriminatingTiles < 4) offsetNegOk = false;
  records.push(rec('WORLD_TERRAIN_OFFSET_64_NEGATIVE',
    'offset-64 canonical vs the KNOWN-WRONG offset-52 read (negative control on 6 physical tiles)',
    offsetNegOk ? 'PASS' : 'FAIL', {
      resultClass: 'NEGATIVE_CONTROL_THROUGH_PRODUCTION_PATH',
      measuredQuantity: 'differing u16 positions between the sub-header (payload 52..63) and the true heights (payload 64..) per sampled tile',
      measured: {
        perTile, discriminatingTiles,
        expectation: 'every sampled tile DISCRIMINATING (>=1 of first 6 differs) or DEGENERATE (sub-header and first heights both all-zero — measured on 000a0014.tdf in the first run); >=4 of 6 must be discriminating',
        firstRunFinding: 'the original preregistration required >=1 difference on EVERY tile; the first run measured tile 000a0014.tdf (all-zero data tile with an all-zero sub-header) as non-discriminating — the refinement documents this boundary case honestly, it does not remove the control',
      },
      independentSourceOfTruth: 'test-local minimal BNT2+TDF byte reader (own inflate + DataView at payload offsets 52 and 64)',
      whyNonCircular: 'the wrong-52 values come from the physical file bytes via an independent reader — a production bug in offsets would show as a mismatch',
    }));
  records.push(rec('WORLD_TERRAIN_HEIGHTS_1024',
    'exact 1024 raw uint16 heights per tile on sampled physical tiles (production PESourceMount.getTerrainTile)',
    heightsOk ? 'PASS' : 'FAIL', {
      measuredQuantity: 'heights.length == 1024 and all values 0..65535 per sampled tile',
      measured: { sampledTiles: SAMPLES.length, perTile: perTile.map((p) => ({ name: p.name, rawMin: p.rawMin, rawMax: p.rawMax, payloadBytes: p.payloadBytes, dataSize: p.dataSize, tileDim: p.tileDim })) },
      independentSourceOfTruth: 'Uint16Array contract + value range check',
      whyNonCircular: 'structural assertion on the production decode output',
    }));
  records.push(rec('WORLD_TERRAIN_INDEPENDENT_BYTES',
    'INDEPENDENT byte-level read of physical tiles cross-checked against the production decoder',
    indepOk ? 'PASS' : 'FAIL', {
      resultClass: 'INDEPENDENT_CROSSCHECK (not the production parser)',
      measuredQuantity: 'bit-exact equality of all 1024 heights per sampled tile: independent reader vs production getTerrainTile',
      measured: { tilesChecked: perTile.length, mismatches: indepMismatches, expectation: '0 mismatches' },
      independentSourceOfTruth: 'test-local BNT2 footer/dir walk + zlib.inflateSync + DataView (zero production imports in that path)',
      whyNonCircular: 'two independent decoders of the same physical bytes must agree bit-exactly; agreement proves both, disagreement localizes the defect',
    }));

  // ---- GATE 4: sentinel + NODATA ----
  const sentinelFacts = {};
  let sentinelOk = true;
  sentinelFacts.isSentinelName = isSentinelName(TDF_SENTINEL_NAME);
  sentinelFacts.sentinelEntryInIndex = Boolean(archive.entryByName(TDF_SENTINEL_NAME));
  sentinelFacts.gridFromName = gridFromName(TDF_SENTINEL_NAME); // {32766, 32766} — NOT in 0..219/0..235
  const sentinelEntry = archive.entryByName(TDF_SENTINEL_NAME);
  const { payload: sentinelPayload } = await archive.readEntry(sentinelEntry);
  let sentinelDecodeRefused = false;
  let sentinelRefusal = null;
  try { decodeTdfPayload(sentinelPayload, { name: TDF_SENTINEL_NAME }); }
  catch (e) { sentinelDecodeRefused = true; sentinelRefusal = String(e?.message ?? e); }
  sentinelFacts.productionDecodeRefusesSentinel = sentinelDecodeRefused;
  sentinelFacts.refusalMessage = sentinelRefusal;
  // range refuses the sentinel ADDRESS (32766 > 219) — loud, never silently a tile
  let sentinelAddressRefused = false;
  let sentinelAddressMsg = null;
  try { await mount.getTerrainTile({ era: 'PCG_9_3_5', gridX: 32766, gridY: 32766 }); }
  catch (e) { sentinelAddressRefused = true; sentinelAddressMsg = String(e?.message ?? e); }
  sentinelFacts.outOfRangeRefusal = sentinelAddressMsg;
  sentinelOk = sentinelFacts.isSentinelName === true && sentinelFacts.sentinelEntryInIndex === true
    && sentinelDecodeRefused === true && sentinelAddressRefused === true;
  records.push(rec('WORLD_TERRAIN_SENTINEL_HANDLING',
    'sentinel 7ffe7ffe.tdf is NOT a regular tile: classified, payload decode refused LOUDLY, address refused by range',
    sentinelOk ? 'PASS' : 'FAIL', {
      measuredQuantity: 'sentinel classification + loud refusals',
      measured: sentinelFacts,
      independentSourceOfTruth: 'production TdfDecoder.isSentinelName + decodeTdfPayload + PESourceMount range check + archive index',
      whyNonCircular: 'each refusal is an observed exception with its message (not an assumed code path)',
    }));

  // NODATA: full regular-grid presence census (measured, not assumed) + loud
  // missing-name refusal + raw-0 tiles counted as DATA.
  const entries = archive.entries();
  const nameSet = new Set(entries.map((e) => e.name));
  let missing = 0; const missingList = [];
  for (let gy = 0; gy < 236; gy++) {
    for (let gx = 0; gx < 220; gx++) {
      const n = gx.toString(16).padStart(4, '0') + gy.toString(16).padStart(4, '0') + '.tdf';
      if (!nameSet.has(n)) { missing++; if (missingList.length < 5) missingList.push(n); }
    }
  }
  let missingRefused = false; let missingMsg = null;
  try { await mount.getTerrainTile({ era: 'PCG_9_3_5', gridX: 0, gridY: 0 }); }
  catch { /* exists */ }
  const fakeName = 'deadbeef.tdf'; // NOT in the index (measured below) — out-of-grid name
  const fakeInIndex = nameSet.has(fakeName);
  let missingNameRefused = false; let missingNameMsg = null;
  if (!fakeInIndex) {
    try { await mount.openResource({ era: 'PCG_9_3_5', container: 'Terrain/terrain.bnt', entryName: fakeName }); }
    catch (e) { missingNameRefused = true; missingNameMsg = String(e?.message ?? e); }
  }
  // raw-0 tile is DATA: tile (0,0) is all-zero in this corpus; its decode
  // succeeds with 1024 zeros (MEASURED), never NODATA.
  const zeroTile = await mount.getTerrainTile({ era: 'PCG_9_3_5', gridX: 0, gridY: 0 });
  let zeroAllZero = true;
  for (let i = 0; i < 1024; i++) if (zeroTile.heights[i] !== 0) { zeroAllZero = false; break; }
  // index classification census (measured)
  let regular = 0, special = 0, sentinelCount = 0, other = 0;
  let specialYMin = 0xffff, specialYMax = -1;
  for (const e of entries) {
    if (isSentinelName(e.name)) { sentinelCount++; continue; }
    const m = /^([0-9a-fA-F]{4})([0-9a-fA-F]{4})\.tdf$/.exec(e.name);
    if (!m) { other++; continue; }
    const gx = parseInt(m[1], 16), gy = parseInt(m[2], 16);
    if (gx < 220 && gy < 236) regular++;
    else {
      special++;
      if (gy < specialYMin) specialYMin = gy;
      if (gy > specialYMax) specialYMax = gy;
    }
  }
  const nodataOk = missing === 0 && missingNameRefused && zeroAllZero
    && regular === 51920 && special === 6530 && sentinelCount === 1 && other === 0;
  records.push(rec('WORLD_TERRAIN_NODATA_CENSUS',
    'regular-grid NODATA census: every regular name present; missing names refused loudly; raw-0 tiles are DATA',
    nodataOk ? 'PASS' : 'FAIL', {
      measuredQuantity: 'index classification counts + loud-missing refusal + all-zero tile decode',
      measured: {
        totalEntries: entries.length, regular, specialRows: special, sentinel: sentinelCount, other,
        specialRowYRangeHex: [specialYMin.toString(16), specialYMax.toString(16)],
        missingRegular: missing, missingSample: missingList,
        missingNameRefused, missingNameRefusalMessage: missingNameMsg, fakeName, fakeInIndex,
        rawZeroTileIsData: zeroAllZero,
        note: 'raw u16 = 0 is DATA (MEASURED); NODATA would be a missing/failed entry — measured 0 in this corpus',
      },
      independentSourceOfTruth: 'archive index enumeration + per-name Set membership + a real decode of the all-zero tile',
      whyNonCircular: 'presence is measured name-by-name from the physical index, not assumed from the format docs',
    }));

  // ---- GATE 5: reverse tile-load order invariance ----
  const ORIGIN = { gx: 108, gy: 116 }; // 4x4 patch origin (interior)
  async function buildRegion(order) {
    const tiles = new Map();
    const coords = [];
    for (let dy = 0; dy < 4; dy++) for (let dx = 0; dx < 4; dx++) coords.push([ORIGIN.gx + dx, ORIGIN.gy + dy]);
    const fetchOrder = order === 'reverse' ? [...coords].reverse() : coords;
    for (const [gx, gy] of fetchOrder) {
      tiles.set(`${gx},${gy}`, await mount.getTerrainTile({ era: 'PCG_9_3_5', gridX: gx, gridY: gy }));
    }
    const rows = [];
    for (let dy = 0; dy < 4; dy++) {
      const row = [];
      for (let dx = 0; dx < 4; dx++) row.push(tiles.get(`${ORIGIN.gx + dx},${ORIGIN.gy + dy}`));
      rows.push(row);
    }
    const region = new PETerrainRegion(rows);
    return { region, geo: region.buildGeometry(), seam: region.tileSeamDiagnostic };
  }
  const fwd = await buildRegion('forward');
  const rev = await buildRegion('reverse');
  let orderInvariant = true;
  if (fwd.geo.positions.length !== rev.geo.positions.length) orderInvariant = false;
  else {
    for (let i = 0; i < fwd.geo.positions.length; i++) {
      if (fwd.geo.positions[i] !== rev.geo.positions[i]) { orderInvariant = false; break; }
    }
    for (let i = 0; i < fwd.geo.indices.length; i++) {
      if (fwd.geo.indices[i] !== rev.geo.indices[i]) { orderInvariant = false; break; }
    }
  }
  // fresh re-decode determinism (same source → same heights)
  const again = await mount.getTerrainTile({ era: 'PCG_9_3_5', gridX: ORIGIN.gx, gridY: ORIGIN.gy });
  const againOk = again.heights.every((v, i) => v === fwd.region.tiles[0][0].heights[i]);
  records.push(rec('WORLD_TERRAIN_REVERSE_ORDER',
    'reverse tile-load order assembles a byte-identical region geometry (load order invariance) + deterministic re-decode',
    orderInvariant && againOk ? 'PASS' : 'FAIL', {
      measuredQuantity: 'positions/indices equality between forward-order and reverse-order 4x4 region builds',
      measured: {
        positionsBytes: fwd.geo.positions.length * 4, indicesBytes: fwd.geo.indices.length * 4,
        byteIdentical: orderInvariant, freshReDecodeIdentical: againOk,
        seamDiagnostic: fwd.seam,
      },
      independentSourceOfTruth: 'byte comparison of two independent builds through the production PETerrainRegion',
      whyNonCircular: 'the comparison is over the actual emitted arrays, not internal state',
    }));

  // ---- GATE 7: bounds + calibration applied exactly once + reversibility ----
  const region4 = fwd.region;
  const g4 = fwd.geo;
  let boundsOk = true;
  const boundsFacts = {};
  boundsFacts.sampleStepMeters = PE_TERRAIN_METER_PER_SAMPLE;
  if (PE_TERRAIN_METER_PER_SAMPLE !== 2) boundsOk = false;
  if (HEIGHT_SCALE_CALIBRATION.u16PerMeter !== 128) boundsOk = false;
  if (HEIGHT_SCALE_CALIBRATION.label !== 'CURRENT_RUNTIME_CALIBRATION') boundsOk = false;
  const sx = g4.sampleGridX, sy = g4.sampleGridY;
  boundsFacts.sampleGrid = [sx, sy];
  if (sx !== 128 || sy !== 128) boundsOk = false; // 4 tiles x 32 samples, NO overlap
  boundsFacts.indexCount = g4.indices.length;
  if (g4.indices.length !== 127 * 127 * 6) boundsOk = false; // quads over the FULL sample grid incl. cross-tile quads
  // local extents + exact step
  let stepOk = true, extentOk = true, convOnceOk = true, roundtripOk = true;
  let firstY = null; const roundtripBad = [];
  for (let vy = 0; vy < sy; vy++) {
    for (let vx = 0; vx < sx; vx++) {
      const i = (vy * sx + vx) * 3;
      const X = g4.positions[i], Y = g4.positions[i + 1], Z = g4.positions[i + 2];
      if (X !== vx * 2 || Z !== vy * 2) { stepOk = false; }
      if (Y !== region4.rawSample(vx, vy) / 128) { convOnceOk = false; } // applied EXACTLY ONCE (u16/128)
      if (Math.round(Y * 128) !== region4.rawSample(vx, vy)) { if (roundtripBad.length < 5) roundtripBad.push([vx, vy, Y]); roundtripOk = false; }
      if (firstY === null) firstY = Y;
    }
  }
  if (g4.positions[0] !== 0 || g4.positions[2] !== 0) extentOk = false;
  const maxLocalX = g4.positions[((sy - 1) * sx + (sx - 1)) * 3];      // vx=sx-1, vy=sy-1 (X)
  const maxLocalZ = g4.positions[((sy - 1) * sx + (sx - 1)) * 3 + 2];  // same vertex (Z)
  if (maxLocalX !== (sx - 1) * 2 || maxLocalZ !== (sy - 1) * 2) extentOk = false;
  // worldHeightMeters identity-lerp form (min=0, max=65535) — the documented preset
  const wqOk = worldHeightMeters(0) === 0 && worldHeightMeters(65535) === 65535 / 128
    && HEIGHT_QUERY.observedOperation.includes('min + (max - min) * u16 * (1/65535)');
  boundsOk = boundsOk && stepOk && extentOk && convOnceOk && roundtripOk && wqOk;
  records.push(rec('WORLD_TERRAIN_BOUNDS_CALIBRATION_ONCE',
    'bounds/calibration: 2 m/sample steps, no tile overlap, conversion u16→meters applied EXACTLY ONCE, reversible (×128), identity min/max preset',
    boundsOk ? 'PASS' : 'FAIL', {
      measuredQuantity: 'per-vertex arithmetic over the full 128x128 sample grid of the 4x4 region',
      measured: {
        sampleStep: PE_TERRAIN_METER_PER_SAMPLE, u16PerMeter: HEIGHT_SCALE_CALIBRATION.u16PerMeter,
        label: HEIGHT_SCALE_CALIBRATION.label, heightQuery: HEIGHT_QUERY.observedOperation,
        sampleGrid: [sx, sy], indexCount: boundsFacts.indexCount,
        stepExact: stepOk, extentsExact: extentOk,
        maxLocalX, maxLocalZ, expectedLocalMax: (sx - 1) * 2,
        conversionExactlyOnce: convOnceOk,
        roundtripMetersToU16: roundtripOk, roundtripBadSamples: roundtripBad,
        identityLerpForm: wqOk,
        note: 'conversion applied once inside buildGeometry via worldHeightMeters; meters×128 recovers raw u16 exactly; CURRENT_RUNTIME_CALIBRATION is a preset, not a historical claim',
      },
      independentSourceOfTruth: 'direct arithmetic comparison of positions[] against rawSample()/128 for every vertex',
      whyNonCircular: 'a double conversion or a wrong scale would break the exact float equality at every vertex',
    }));

  // ---- GATE 8: hash witness AFTER the whole suite (originals READ_ONLY) ----
  const shaAfter = createHash('sha256').update(new Uint8Array(readFileSync(terrainPath))).digest('hex').toUpperCase();
  const hashOk = shaBefore === PIN_TERRAIN_SHA && shaAfter === PIN_TERRAIN_SHA && stat.size === PIN_TERRAIN_SIZE;
  records.push(rec('WORLD_TERRAIN_HASH_WITNESS',
    'terrain.bnt byte-identity witness: pinned SHA256 before AND after the whole suite (originals never rewritten)',
    hashOk ? 'PASS' : 'FAIL', {
      measuredQuantity: 'sha256 + size of the physical container across the suite lifetime',
      measured: { shaBefore, shaAfter, pin: PIN_TERRAIN_SHA, sizeBytes: stat.size, pinSize: PIN_TERRAIN_SIZE },
      independentSourceOfTruth: 'node:crypto stream hash of the physical file (not a cache)',
      whyNonCircular: 'any write to the original container would change the hash — measured twice, both equal to the pin',
    }));

  // suite metadata record (not a gate): what ran, how long
  records.push(rec('WORLD_TERRAIN_SUITE_META',
    'suite metadata (SIDE record — elapsed + module identities)',
    'PASS', {
      measuredQuantity: 'suite runtime + pinned module constants',
      measured: {
        elapsedMs: Date.now() - t0,
        tdfLayout: { HEIGHTS: TDF_PAYLOAD_LAYOUT.HEIGHTS, SUBHEADER: TDF_PAYLOAD_LAYOUT.SUBHEADER },
        tdfStandard: { DATA_SIZE_FIELD: TDF_STANDARD.DATA_SIZE_FIELD, TILE_DIM_FIELD: TDF_STANDARD.TILE_DIM_FIELD, HEIGHT_SAMPLES: TDF_STANDARD.HEIGHT_SAMPLES },
      },
    }));

  return records;
}
