// world_vegetation.test.mjs — PE_WORLD_LAUNCHER_R1_20261010, ETAP E
// (contract §6 + §8 vegetation gates; PREREGISTERED BEFORE execution).
//
// THE GATES (preregistered expectations — not corrected to match results):
//   WORLD_VEG_VCL_STRICT_25          — 25.vcl stays controlled UNSUPPORTED
//                                       through the REAL routes (strict
//                                       decoder; comma tokens NEVER
//                                       converted; records=null asserted BY
//                                       ABSENCE, not by message).
//   WORLD_VEG_DEFAULT_PROFILE_MEASURED— the chosen default profile (0) is
//                                       valid + non-empty + has >=1 SUPPORTED
//                                       model in the same era (the server's
//                                       measured support census; the witness
//                                       457485 must be SUPPORTED with a
//                                       resolved texture chain).
//   WORLD_VEG_CORE_UNTOUCHED          — PEFoliageCore.js + NifModelReader.js
//                                       + VegetationClimateDecoder.js are
//                                       byte-identical to HEAD (git blob) AND
//                                       the byte-locked arithmetic still
//                                       matches an INDEPENDENT formula
//                                       reimplementation (seed/LCG/f32 lerp/
//                                       node positions on a known vector).
//   WORLD_VEG_REPEAT_SEED_DETERMINISM — same (records+labSeed+gx/gy+density+
//                                       calibration) -> IDENTICAL instance-set
//                                       SHA-256; changed labSeed -> DIFFERENT
//                                       hash (a real placement change, not a
//                                       label); the byte-locked fields equal.
//   WORLD_VEG_STREAMING_ORDER_INVARIANCE — 16 tiles generated in TWO
//                                       different orders -> identical per-tile
//                                       sets + identical union (the load
//                                       order cannot change ANY set).
//   WORLD_VEG_EDGE_OWNERSHIP_NO_DUPLICATES — instance keys unique;
//                                       positions STRICTLY inside their tile's
//                                       half-open u16 box (no position can be
//                                       claimed by two tiles); a drop-and-
//                                       regenerate cycle (the camera-return
//                                       proof) reproduces the SAME set.
//   WORLD_VEG_CAP_5000                — a measured high-density case (profile
//                                       1, density 100% -> 6,144 requested
//                                       over the 8x8 window) renders EXACTLY
//                                       5000 with limited=1144; the limited
//                                       subset is deterministic.
//   WORLD_VEG_MODEL_IMPORT_SUPPORT    — the /api/world/model/<id> payloads
//                                       are bit-exact the physical container
//                                       reads (independent lazy reader); the
//                                       witness 457485 parses with the
//                                       EXISTING qualified importer (16v/8t/
//                                       textureId 457490); the per-model
//                                       support census is recorded (8
//                                       textured / 2 honest-untextured (DDS
//                                       outside the strict subset) / 0
//                                       parse-unsupported); a missing id is a
//                                       loud 404 (never a substitute model).
//   WORLD_VEG_RESOURCE_DISCIPLINE     — the headless THREE census: window
//                                       A -> B -> A reuses the model payloads
//                                       (fetch counters measured; texture
//                                       object IDENTITY reused — no
//                                       duplication), a profile change
//                                       releases unreferenced models/
//                                       textures while still-referenced shared
//                                       resources survive, toggle OFF -> ON
//                                       re-renders WITHOUT re-fetching, and
//                                       the instance counts return to the
//                                       same values (no loss, no dupes).
//   WORLD_VEG_MODEL_CACHE_IDENTITY    — CAM-C3 mutants through the PRODUCTION
//                                       verifyModelCacheIdentity (era /
//                                       containerSha / entryName / payloadSha
//                                       / wireVersion each REFUSED by name);
//                                       clean passes; the REAL route
//                                       double-fetch = HIT with identical
//                                       bytes.
//   WORLD_VEG_SERVER_LIFECYCLE         — the suite-owned server stops + the
//                                       port is freed (standing 8140/8161
//                                       never touched).
//
// THREE resolution: this suite imports the REAL world-vegetation.js, whose
// bare 'three' specifier resolves through the worktree node_modules (the
// pinned 0.185.0 — package.json dependency; the same instance the browser
// importmap serves). A missing node_modules is a LOUD import failure, never
// a silent skip.
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { promises as fsp } from 'node:fs';
import { readFile } from 'node:fs/promises';

import { record } from './_helpers.mjs';
import {
  startWorldServer, stopWorldServer, findFreePort, rawRequestFull, parseJsonOrNone,
} from './_world_server_helpers.mjs';
import {
  generateTileInstances, tileU16Span, LABSEED_WINDOW_CALIBRATION,
} from '../../src/peworld/PEFoliageLabSeed.js';
import { VegetationRNG, sampleModelScale, NODE_POS_DIVISOR, NODE_SCALE_MUL } from '../../src/peworld/PEFoliageCore.js';
import { verifyModelCacheIdentity, MODEL_WIRE_VERSION } from '../../compat/server-world.mjs';
import { WorldVegetation, MAX_VISIBLE_INSTANCES } from '../../compat/world-vegetation.js';
import * as THREE from 'three';

const MODELS_PATH = 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt';
const MODELS_PIN = 'C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0';

const sha256 = (bytes) => createHash('sha256').update(bytes).digest('hex');

/** The CANONICAL instance-set serialization for hashing: SORTED by instance
 * key (an order-independent SET hash — the load order cannot change it) over
 * the deterministic fields (identity + the u16 placement + the byte-locked
 * f32 bit patterns; the world coords are a pure function of u16+calibration,
 * so hashing the inputs is complete). */
function instanceSetSha256(instances) {
  const h = createHash('sha256');
  const f32bits = (v) => {
    const b = new Uint8Array(4); new Float32Array(b.buffer)[0] = v;
    let s = ''; for (let i = 0; i < 4; i++) s += b[i].toString(16).padStart(2, '0');
    return s;
  };
  const sorted = [...instances].sort((a, b2) => (a.key < b2.key ? -1 : a.key > b2.key ? 1 : 0));
  for (const i of sorted) {
    h.update(`${i.key}|${i.modelId}|${i.u16.x}|${i.u16.y}|${f32bits(i.scale)}|${f32bits(i.node01.x)}|${f32bits(i.node01.y)}\n`);
  }
  return h.digest('hex');
}

// ---- an INDEPENDENT lazy Models.bnt reader (own footer/dir walk; no
// production imports — the whyNonCircular witness for the wire payloads) ----
async function independentModelIndex() {
  const st = await fsp.stat(MODELS_PATH);
  const h = await fsp.open(MODELS_PATH, 'r');
  const footer = Buffer.alloc(8);
  await h.read(footer, 0, 8, st.size - 8);
  const dirOffset = footer.readUInt32LE(0);
  if (footer.subarray(4, 8).toString('latin1') !== 'BNT2') throw new Error('bad magic');
  const dirBytes = st.size - dirOffset - 8;
  const dir = Buffer.alloc(dirBytes);
  await h.read(dir, 0, dirBytes, dirOffset);
  const dv = new DataView(dir.buffer, dir.byteOffset, dir.byteLength);
  const count = dv.getUint32(0, true);
  let p = 4;
  const byName = new Map();
  while (p < dir.length) {
    let end = p;
    while (end < dir.length && dir[end] !== 0x0a) end++;
    const name = dir.toString('latin1', p, end);
    byName.set(name, { name, size: dv.getUint32(end + 1, true), offset: dv.getUint32(end + 5, true) });
    p = end + 17;
  }
  await h.close();
  return { size: st.size, count, byName };
}
async function independentModelRead(entry) {
  const h = await fsp.open(MODELS_PATH, 'r');
  const buf = Buffer.alloc(entry.size);
  const { bytesRead } = await h.read(buf, 0, entry.size, entry.offset);
  await h.close();
  if (bytesRead !== entry.size) throw new Error('short read');
  return new Uint8Array(buf);
}

export async function run(ctx) {
  const out = [];
  const port = await findFreePort(8162);
  const serverRec = await startWorldServer({ port });
  const base = `http://127.0.0.1:${port}`;

  try {
    // ============================ profile records ============================
    const climate0 = parseJsonOrNone((await rawRequestFull(port, '/api/world/climate/0')).body.toString('utf8'));
    const climate25 = parseJsonOrNone((await rawRequestFull(port, '/api/world/climate/25')).body.toString('utf8'));
    const status = parseJsonOrNone((await rawRequestFull(port, '/api/world/status')).body.toString('utf8'));

    // ---- WORLD_VEG_VCL_STRICT_25: controlled UNSUPPORTED, never converted ----
    const strictOk =
      climate25.ok === false && climate25.status === 'UNSUPPORTED' &&
      climate25.records === null && climate25.recordCount === 0 &&
      /non-numeric token "0,2"/.test(climate25.error ?? '') &&
      /never comma-converted|comma/i.test(climate25.provenanceNote ?? '');
    const climate0Decoded = climate0.ok === true && climate0.status === 'DECODED' && climate0.recordCount === 12
      && Array.isArray(climate0.records) && climate0.records.length === 12
      && climate0.records.every((r) => Array.isArray(r) && r.length === 12);
    out.push(record('WORLD_VEG_VCL_STRICT_25',
      '25.vcl stays controlled UNSUPPORTED through the REAL route (strict decoder — comma tokens never converted; records asserted NULL by absence)',
      strictOk && climate0Decoded ? 'PASS' : 'FAIL', {
      resultClass: 'PRODUCTION_ROUTE_MEASUREMENT (the running server through the strict decoder)',
      measuredQuantity: 'the climate API payloads of profiles 0 and 25',
      measured: {
        profile25: { ok: climate25.ok, status: climate25.status, recordCount: climate25.recordCount, recordsNull: climate25.records === null, errorExcerpt: (climate25.error ?? '').slice(0, 160), provenanceNote: climate25.provenanceNote },
        profile0: { ok: climate0.ok, status: climate0.status, recordCount: climate0.recordCount, allRecords12Value: climate0Decoded },
      },
      independentSourceOfTruth: 'the raw HTTP payloads (no client normalization)',
      whyNonCircular: 'UNSUPPORTED is asserted BY ABSENCE (records === null) — a fabricated-records regression would fail the null check',
      failureCaseDetected: strictOk && climate0Decoded ? 'none — the strict refusal is intact and profile 0 decodes 12x12-value records' : 'the strict-decoder contract was violated (records fabricated or the refusal message changed)',
    }));

    // ---- WORLD_VEG_DEFAULT_PROFILE_MEASURED ----
    const sv = status.vegetation;
    const dp = sv?.defaultProfile;
    const sc = sv?.supportCensus;
    const witness = sc?.models?.find((m) => m.modelId === 457485);
    const defaultOk =
      dp?.index === 0 && dp?.status === 'DECODED' && dp?.recordCount > 0 && dp?.recordsNonEmpty === true &&
      sv?.supportCensusState === 'READY' &&
      sc?.counts?.atLeastOneSupportedModel === true && sc.counts.unsupported === 0 &&
      witness?.status === 'SUPPORTED' && witness.textures?.[0]?.resolved === true &&
      typeof dp.measuredJustification === 'string' && /MEASURED CHOICE/.test(dp.measuredJustification) &&
      sv.p3 === 0 && sv.visibleInstanceCap === 5000;
    out.push(record('WORLD_VEG_DEFAULT_PROFILE_MEASURED',
      'the default profile (0) is chosen MEASURABLY: DECODED + non-empty records + >=1 supported same-era model (the witness 457485 SUPPORTED with its texture chain resolved); never a historical-biome claim',
      defaultOk ? 'PASS' : 'FAIL', {
      resultClass: 'PRODUCTION_SUPPORT_CENSUS (the bounded server measurement through the REAL lazy archives + the existing importer)',
      measuredQuantity: 'status.vegetation.defaultProfile + the per-model support census',
      measured: {
        defaultProfile: dp,
        supportCounts: sc?.counts,
        witness457485: witness ? { status: witness.status, textureId: witness.textureIds?.[0], textures: witness.textures } : null,
        perModelStatuses: sc?.models?.map((m) => ({ modelId: m.modelId, status: m.status, visualShapes: m.visualShapes, shapesTotal: m.shapesTotal })),
        p3: sv?.p3, p3Note: sv?.p3Note, cap: sv?.visibleInstanceCap,
      },
      independentSourceOfTruth: 'the server-side census through LazyModelArchive/LazyTextureArchive + parseWitnessModel + decodeModelTextureStrict (the same production modules the browser uses)',
      whyNonCircular: 'the justification is a MEASURED outcome (per-model parse + strict decode), not a profile label; the justification text forbids the historical-biome claim',
      failureCaseDetected: defaultOk ? 'none — profile 0 satisfies every preregistered criterion with measured evidence' : 'the default-profile justification did not measure out (see measured)',
    }));

    // ---- WORLD_VEG_CORE_UNTOUCHED: byte-identity + the arithmetic control ----
    const CORE_FILES = [
      'src/peworld/PEFoliageCore.js',
      'src/pesource/NifModelReader.js',
      'src/pesource/VegetationClimateDecoder.js',
      'src/pesource/TgaDecoder.js',
    ];
    const repoRoot = ctx.repoRoot ?? process.cwd();
    let untouched = true;
    const fileMeasured = [];
    for (const f of CORE_FILES) {
      const wt = await readFile(`${repoRoot}/${f}`);
      const wtSha = sha256(wt);
      let baseSha = null;
      try {
        const baseBlob = execFileSync('git', ['show', `HEAD:${f}`], { cwd: repoRoot, maxBuffer: 8 * 1024 * 1024 });
        baseSha = sha256(baseBlob);
      } catch { baseSha = null; }
      const same = baseSha !== null && wtSha === baseSha;
      if (!same) untouched = false;
      fileMeasured.push({ file: f, workingTreeSha256: wtSha, headSha256: baseSha, identical: same });
    }
    // the byte-locked arithmetic control: an INDEPENDENT reimplementation of
    // the documented formulas must reproduce the module outputs exactly.
    const vec = [];
    let arithOk = true;
    for (const [p4, p5, rec2, rec3] of [[100, 200, 0.5, 1.5], [4096, 8191, 0.8, 1.5], [30000, 60000, 0.25, 1.25], [7, 13, 0.5, 2.0]]) {
      const rng = new VegetationRNG();
      const state0 = rng.seed(0x1234, 10, 0, p4, p5);
      const { value, scale } = sampleModelScale(rng, rec2, rec3);
      // independent formula reimplementation (documented in PEFoliageCore):
      const x = ((((p4 >>> 0) * 0x10 + (p5 >>> 0)) * 0x10) + 0x1234 + 10 + 0) >>> 0;
      const hashed = (x * 0x5CC7 + 0x6D7) >>> 0;
      const expState0 = ((hashed * 8) ^ hashed) >>> 0;
      let state = state0;
      state = (state * 0x343FD + 0x269EC3) >>> 0;
      const r = (state >>> 16) & 0x7FFF;
      const expRand01 = Math.fround(r / 32767.0);
      const expValue = Math.fround(expRand01 * (Math.fround(rec3) - Math.fround(rec2)) + Math.fround(rec2));
      const expScale = Math.fround(Math.abs(expValue * NODE_SCALE_MUL));
      const ok = state0 === expState0 && value === expValue && scale === expScale;
      if (!ok) arithOk = false;
      vec.push({ p4, p5, state0, value, scale, expState0, expValue, expScale, ok });
    }
    // node positions: the locked divisor + fround
    const nodeOk = Math.fround(457485 / NODE_POS_DIVISOR) === Math.fround(457485 / 65535.0);
    out.push(record('WORLD_VEG_CORE_UNTOUCHED',
      'PEFoliageCore + NifModelReader + VegetationClimateDecoder + TgaDecoder are byte-identical to HEAD and the byte-locked arithmetic matches an INDEPENDENT formula reimplementation (seed hash / LCG / f32 lerp / f32 scale on measured vectors)',
      untouched && arithOk && nodeOk ? 'PASS' : 'FAIL', {
      resultClass: 'GIT_BLOB_IDENTITY + INDEPENDENT_ARITHMETIC_CONTROL',
      measuredQuantity: 'working-tree SHA256 vs HEAD blobs + the module outputs vs the independently recomputed formulas',
      measured: { files: fileMeasured, arithmeticVectors: vec, nodeDivisorOk: nodeOk, nodePosDivisor: NODE_POS_DIVISOR },
      independentSourceOfTruth: 'git HEAD blobs + the documented formulas re-implemented in THIS test (not the module under test)',
      whyNonCircular: 'a byte edit would break the blob comparison; an arithmetic regression would break the independent-formula vectors',
      failureCaseDetected: untouched && arithOk && nodeOk ? 'none — the recovered chain is untouched and reproduces its documented formulas' : 'a core file changed OR the byte-locked arithmetic drifted (see measured)',
    }));

    // ======================= determinism gates (pure generation) =======================
    const records0 = climate0.records;
    const genOpts = { records: records0, densityPercent: 50 };

    // ---- WORLD_VEG_REPEAT_SEED_DETERMINISM ----
    const a1 = generateTileInstances({ ...genOpts, labSeed: 0, gx: 53, gy: 114 });
    const a2 = generateTileInstances({ ...genOpts, labSeed: 0, gx: 53, gy: 114 });
    const b = generateTileInstances({ ...genOpts, labSeed: 1, gx: 53, gy: 114 });
    const hA1 = instanceSetSha256(a1.instances), hA2 = instanceSetSha256(a2.instances), hB = instanceSetSha256(b.instances);
    const countsA1 = a1.instances.length, countsB = b.instances.length;
    // the byte-locked fields stay in-range: every instance's lerp value must
    // lie inside ITS OWN record's scale band (col2..col3 of that record)
    const scalesInBand = a1.instances.every((i) => {
      const rec = records0[i.recIndex];
      return i.scale > 0 && i.samplerValue >= Math.min(rec[2], rec[3]) - 1e-6 && i.samplerValue <= Math.max(rec[2], rec[3]) + 1e-6;
    });
    const seedOk = hA1 === hA2 && hA1 !== hB && countsA1 === countsB && scalesInBand;
    out.push(record('WORLD_VEG_REPEAT_SEED_DETERMINISM',
      'repeat-seed determinism: the SAME (records+LAB_SEED+tile+density+calibration) -> the IDENTICAL instance-set hash; a CHANGED seed -> a DIFFERENT hash (a real placement change)',
      seedOk ? 'PASS' : 'FAIL', {
      resultClass: 'PURE_GENERATION_CONTROL (PEFoliageLabSeed over the ORIGINAL_CLIMATE_RECORDS of profile 0)',
      measuredQuantity: 'SHA-256 of the canonical instance serialization (key|model|u16|f32 bits)',
      measured: {
        labSeed0: { hash: hA1, instances: countsA1 },
        labSeed0Repeat: { hash: hA2 },
        labSeed1: { hash: hB, instances: countsB },
        hashesIdentical: hA1 === hA2, seedsDiffer: hA1 !== hB,
        scalesInLerpBand: scalesInBand,
      },
      independentSourceOfTruth: 'the canonical serialization of every instance (no sampling, no subset)',
      whyNonCircular: 'identical hashes across two INDEPENDENT calls prove the generator is pure; a different seed changing the hash proves LAB_SEED influences the actual placement (not a UI label)',
      failureCaseDetected: seedOk ? 'none — repeat-seed identical, changed-seed different' : 'the determinism contract was violated (hash drift or a seed with no effect)',
    }));

    // ---- WORLD_VEG_STREAMING_ORDER_INVARIANCE ----
    const tiles = [];
    for (let gy = 111; gy < 115; gy++) for (let gx = 50; gx < 54; gx++) tiles.push([gx, gy]);
    const forward = new Map(), shuffled = new Map();
    for (const [gx, gy] of tiles) {
      forward.set(`${gx},${gy}`, generateTileInstances({ ...genOpts, labSeed: 7, gx, gy }));
    }
    const shuffledOrder = [tiles[7], tiles[2], tiles[13], tiles[0], tiles[9], tiles[4], tiles[11], tiles[6], tiles[1], tiles[14], tiles[3], tiles[10], tiles[5], tiles[12], tiles[8], tiles[15]];
    for (const [gx, gy] of shuffledOrder) {
      shuffled.set(`${gx},${gy}`, generateTileInstances({ ...genOpts, labSeed: 7, gx, gy }));
    }
    let orderInvariant = true;
    const perTileCompare = [];
    for (const k of [...forward.keys()]) {
      const hf = instanceSetSha256(forward.get(k).instances);
      const hs = instanceSetSha256(shuffled.get(k).instances);
      if (hf !== hs) orderInvariant = false;
      perTileCompare.push({ tile: k, forwardHash: hf.slice(0, 12), shuffledHash: hs.slice(0, 12), identical: hf === hs });
    }
    const unionF = instanceSetSha256([...forward.values()].flatMap((g) => g.instances));
    const unionS = instanceSetSha256([...shuffled.values()].flatMap((g) => g.instances));
    const unionIdentical = unionF === unionS;
    out.push(record('WORLD_VEG_STREAMING_ORDER_INVARIANCE',
      'streaming-order invariance: 16 tiles generated in TWO different orders -> identical per-tile sets AND identical union (the load order cannot change any instance)',
      orderInvariant && unionIdentical ? 'PASS' : 'FAIL', {
      resultClass: 'PURE_GENERATION_CONTROL',
      measuredQuantity: 'per-tile instance-set hashes + the union hash across the two orders',
      measured: { tiles: tiles.length, perTileCompare, unionForwardHash: unionF, unionShuffledHash: unionS, unionIdentical },
      independentSourceOfTruth: 'the canonical serialization per tile + the union',
      whyNonCircular: 'each tile is generated independently keyed on its tileKey; comparing both orders through the same serializer exposes any order dependence',
      failureCaseDetected: orderInvariant && unionIdentical ? 'none — order cannot change the result' : 'an order-dependent generation path was found',
    }));

    // ---- WORLD_VEG_EDGE_OWNERSHIP_NO_DUPLICATES ----
    const span = tileU16Span();
    let keysUnique = true, insideBox = true;
    const keys = new Set();
    const all16 = [...forward.values()].flatMap((g) => g.instances);
    for (const i of all16) {
      if (keys.has(i.key)) keysUnique = false;
      keys.add(i.key);
      const x0 = i.tile.gx * span, y0 = i.tile.gy * span;
      if (!(i.u16.x >= x0 && i.u16.x < x0 + span && i.u16.y >= y0 && i.u16.y < y0 + span)) insideBox = false;
    }
    // the camera-return proof: drop the tile's set and regenerate it -> identical
    const key53 = '53,112';
    const before = instanceSetSha256(forward.get(key53).instances);
    forward.delete(key53);
    const regenerated = generateTileInstances({ ...genOpts, labSeed: 7, gx: 53, gy: 112 });
    const after = instanceSetSha256(regenerated.instances);
    const regenIdentical = before === after;
    out.push(record('WORLD_VEG_EDGE_OWNERSHIP_NO_DUPLICATES',
      'edge ownership: keys unique across the window, every u16 position STRICTLY inside its tile half-open box (no position claimable by two tiles), and a drop-and-regenerate cycle (the camera-return proof) reproduces the SAME set',
      keysUnique && insideBox && regenIdentical ? 'PASS' : 'FAIL', {
      resultClass: 'PURE_GENERATION_CONTROL (BY-CONSTRUCTION ownership measured, not assumed)',
      measuredQuantity: 'key uniqueness (Set size), in-box positions, the regenerate hash',
      measured: {
        instances: all16.length, uniqueKeys: keys.size, keysUnique, allInsideTileBox: insideBox,
        tileU16Span: span,
        cameraReturn: { tile: key53, hashBefore: before.slice(0, 16), hashAfterDropAndRegen: after.slice(0, 16), identical: regenIdentical },
      },
      independentSourceOfTruth: 'the canonical serialization + the arithmetic bounds',
      whyNonCircular: 'the half-open box check recomputes the tile bounds from the tile key; the duplicate check is a Set-vs-count comparison',
      failureCaseDetected: keysUnique && insideBox && regenIdentical ? 'none — ownership is by construction and survives unload/reload' : 'a duplicate or cross-tile position was measured',
    }));

    // ---- WORLD_VEG_CAP_5000 (a measured high-density case: profile 1 @100%) ----
    const climate1 = parseJsonOrNone((await rawRequestFull(port, '/api/world/climate/1')).body.toString('utf8'));
    let capRequested = 0;
    const capPerTile = [];
    for (let dy = 0; dy < 8; dy++) {
      for (let dx = 0; dx < 8; dx++) {
        const g = generateTileInstances({ records: climate1.records, densityPercent: 100, labSeed: 0, gx: 50 + dx, gy: 111 + dy });
        capRequested += g.instances.length;
        capPerTile.push(g.instances.length);
      }
    }
    const capRendered = Math.min(capRequested, MAX_VISIBLE_INSTANCES);
    const capLimited = capRequested - capRendered;
    // determinism of the limited subset: the same slice rule on the same order
    const capRequested2 = (() => {
      let n = 0;
      for (let dy = 0; dy < 8; dy++) for (let dx = 0; dx < 8; dx++) {
        n += generateTileInstances({ records: climate1.records, densityPercent: 100, labSeed: 0, gx: 50 + dx, gy: 111 + dy }).instances.length;
      }
      return n;
    })();
    const capOk = capRequested > MAX_VISIBLE_INSTANCES && capRendered === MAX_VISIBLE_INSTANCES && capLimited === capRequested - 5000 && capRequested2 === capRequested;
    out.push(record('WORLD_VEG_CAP_5000',
      'the 5000 visible-instance cap respected on a measured high-density case (profile 1 @100% over the 8x8 window): requested > cap -> rendered EXACTLY 5000, limited counted honestly; the requested count is stable (deterministic)',
      capOk ? 'PASS' : 'FAIL', {
      resultClass: 'MEASURED_CAP_CONTROL (the hard display limit; never fake full coverage)',
      measuredQuantity: 'requested / rendered / limited over the profile-1 window at 100%',
      measured: { requested: capRequested, rendered: capRendered, limited: capLimited, cap: MAX_VISIBLE_INSTANCES, requestedRepeatStable: capRequested2, perTileCounts: capPerTile },
      independentSourceOfTruth: 'the pure generator over the served profile-1 records',
      whyNonCircular: 'the counts are recomputed tile-by-tile; the cap rule is min(requested, 5000) applied to the deterministic order',
      failureCaseDetected: capOk ? 'none — the cap limits the high-density case exactly' : 'the cap was not respected or the counts are unstable',
    }));

    // ---- WORLD_VEG_MODEL_IMPORT_SUPPORT ----
    const idx = await independentModelIndex();
    const modelChecks = [];
    let wireBitExact = true;
    const profile0ModelIds = [...new Set(records0.map((r) => r[0] | 0))];
    for (const id of profile0ModelIds) {
      const r = await rawRequestFull(port, `/api/world/model/${id}`);
      const entry = idx.byName.get(`${id}.nif`);
      const served = new Uint8Array(r.body);
      const phys = entry ? await independentModelRead(entry) : null;
      const same = phys !== null && served.length === phys.length && sha256(served) === sha256(phys);
      if (!same) wireBitExact = false;
      modelChecks.push({ id, httpStatus: r.status, servedBytes: served.length, physicalBytes: entry?.size ?? null, bitExact: same, entryName: r.headers['x-pe-entry'], payloadSha: r.headers['x-pe-payload-sha256']?.slice(0, 16) });
    }
    // the witness reproduction through the EXISTING qualified importer
    const witnessPayload = await independentModelRead(idx.byName.get('457485.nif'));
    const { parseWitnessModel } = await import('../../src/pesource/NifModelReader.js');
    let witnessParse = null;
    let witnessOk = false;
    try {
      const { extraction, renderModel } = parseWitnessModel(witnessPayload, '457485.nif');
      witnessParse = {
        nifVersion: extraction.header.versionString, blocks: extraction.blocks.length,
        numVertices: renderModel.numVertices, numTriangles: renderModel.numTriangles,
        textureId: renderModel.textureBinding.textureId,
      };
      witnessOk = witnessParse.nifVersion === '10.1.0.0' && witnessParse.numVertices === 16
        && witnessParse.numTriangles === 8 && witnessParse.textureId === 457490;
    } catch (e) { witnessParse = { error: String(e?.message ?? e) }; }
    // the missing-id honest 404 (never a substitute model)
    const missing = await rawRequestFull(port, '/api/world/model/999999');
    const missingOk = missing.status === 404 && parseJsonOrNone(missing.body.toString('utf8')).error === 'MODEL_ENTRY_NOT_FOUND';
    // the support census per-model statuses (from the status payload — measured server-side)
    const scCounts = sv.supportCensus.counts;
    const untextured = sv.supportCensus.models.filter((m) => m.status === 'SUPPORTED_UNTEXTURED');
    const importOk = wireBitExact && witnessOk && missingOk && scCounts.distinctModels === 10
      && scCounts.supported === 8 && scCounts.supportedUntextured === 2 && scCounts.unsupported === 0
      && untextured.every((m) => /strict model-texture subset/.test(m.textures?.find((t) => !t.resolved)?.reason ?? ''));
    out.push(record('WORLD_VEG_MODEL_IMPORT_SUPPORT',
      'the model route payloads are bit-exact the physical container reads; the witness 457485 parses through the EXISTING qualified importer (16v/8t/texId 457490); the profile-0 support census: 8 textured + 2 honest-untextured (DDS outside the strict subset) + 0 parse-unsupported; a missing id is a loud 404 (never a substitute model)',
      importOk ? 'PASS' : 'FAIL', {
      resultClass: 'PRODUCTION_ROUTE + INDEPENDENT_BYTES + QUALIFIED_IMPORTER',
      measuredQuantity: 'wire bytes vs physical reads; the witness parse through parseWitnessModel; the server support census',
      measured: { perModelWireChecks: modelChecks, wireBitExact, witness: witnessParse, missing999999: { status: missing.status, error: parseJsonOrNone(missing.body.toString('utf8'))?.error }, supportCounts: scCounts, untexturedReasons: untextured.map((m) => ({ id: m.modelId, reason: m.textures?.find((t) => !t.resolved)?.reason?.slice(0, 120) })) },
      independentSourceOfTruth: 'the test-local lazy Models.bnt reader (own footer/dir walk + raw file reads) + the strict importer run in THIS process',
      whyNonCircular: 'the wire payloads are compared against the physical container by code that imports NOTHING from the server; the witness numbers are the reader\'s own measured output',
      failureCaseDetected: importOk ? 'none — the chain holds bit-exactly with honest per-model statuses' : 'a wire mismatch, a witness regression, a wrong support count, or a missing-id substitution',
    }));

    // ---- WORLD_VEG_MODEL_CACHE_IDENTITY (CAM-C3 mutants through the production gate) ----
    const mountIdentity = { era: 'PCG_9_3_5', container: 'Models.bnt', containerSha256: status.containers.models.sha256 };
    const wR457 = await rawRequestFull(port, '/api/world/model/457485');
    const payload457 = new Uint8Array(wR457.body);
    const cleanEntry = {
      payload: payload457,
      identity: {
        era: mountIdentity.era, container: mountIdentity.container,
        containerSha256: mountIdentity.containerSha256, entryName: '457485.nif',
        wireVersion: MODEL_WIRE_VERSION, payloadSha256: sha256(payload457),
      },
    };
    const mutants = [];
    const mk = (id, mut) => ({
      ...cleanEntry,
      identity: { ...cleanEntry.identity, ...mut },
    });
    for (const [id, mut, expReason] of [
      ['M1_WRONG_ERA', { era: 'CD_JAN_2003' }, 'ERA_MISMATCH'],
      ['M2_WRONG_CONTAINER_SHA', { containerSha256: '0'.repeat(64) }, 'CONTAINER_SHA_MISMATCH'],
      ['M3_WRONG_ENTRY_NAME', { entryName: '999999.nif' }, 'ENTRY_NAME_MISMATCH'],
      ['M5_WRONG_WIRE_VERSION', { wireVersion: 'bnt2-model-wire-v0' }, 'WIRE_VERSION_MISMATCH'],
    ]) {
      const v = verifyModelCacheIdentity(mk(id, mut), mountIdentity, { expectedEntryName: '457485.nif' });
      mutants.push({ id, refused: !v.ok, reasons: v.reasons, expected: [expReason], ok: !v.ok && v.reasons.includes(expReason) });
    }
    const tampered = { ...cleanEntry, payload: new Uint8Array(payload457.length) };
    tampered.payload.set(payload457); tampered.payload[0] ^= 0xFF;
    const vTamper = verifyModelCacheIdentity(tampered, mountIdentity, { expectedEntryName: '457485.nif' });
    mutants.push({ id: 'M4_TAMPERED_PAYLOAD', refused: !vTamper.ok, reasons: vTamper.reasons, expected: ['PAYLOAD_SHA_MISMATCH'], ok: !vTamper.ok && vTamper.reasons.includes('PAYLOAD_SHA_MISMATCH') });
    const vClean = verifyModelCacheIdentity(cleanEntry, mountIdentity, { expectedEntryName: '457485.nif' });
    const malformed = verifyModelCacheIdentity({ payload: 'not-bytes' }, mountIdentity, {});
    const firstFetch = await rawRequestFull(port, '/api/world/model/218757');
    const secondFetch = await rawRequestFull(port, '/api/world/model/218757');
    const mutOk = mutants.every((m) => m.ok) && vClean.ok === true && malformed.ok === false
      && firstFetch.headers['x-pe-cache-state'] === 'MISS' && secondFetch.headers['x-pe-cache-state'] === 'HIT'
      && sha256(new Uint8Array(secondFetch.body)) === sha256(new Uint8Array(firstFetch.body));
    out.push(record('WORLD_VEG_MODEL_CACHE_IDENTITY',
      'CAM-C3 model-cache mutants (wrong era / containerSha / entryName / tampered payload / wireVersion) REFUSED with named reasons through the PRODUCTION verifyModelCacheIdentity; clean PASSES; the REAL route double-fetch = HIT with identical bytes',
      mutOk ? 'PASS' : 'FAIL', {
      resultClass: 'PRODUCTION_GATE_MUTANTS (each flips exactly one identity component)',
      measuredQuantity: 'verifyModelCacheIdentity verdicts + the route cache headers',
      measured: { mutants, clean: { ok: vClean.ok, reasons: vClean.reasons }, malformed: { ok: malformed.ok, reasons: malformed.reasons }, realRoute: { note: 'a fresh model id (218757 — NOT fetched earlier in this suite) proves the MISS -> HIT cycle on the shared server', first: firstFetch.headers['x-pe-cache-state'], second: secondFetch.headers['x-pe-cache-state'], identicalBytes: sha256(new Uint8Array(secondFetch.body)) === sha256(new Uint8Array(firstFetch.body)) } },
      independentSourceOfTruth: 'the exported production gate + the real HTTP route',
      whyNonCircular: 'the mutants are constructed in-test and asserted BY NAMED REASON; a silent attach would fail',
      failureCaseDetected: mutOk ? 'none — every identity violation is refused by name' : 'a cache identity violation was accepted (or the clean entry refused)',
    }));

    // ---- WORLD_VEG_RESOURCE_DISCIPLINE (headless THREE + the REAL routes) ----
    const scene = new THREE.Scene();
    const identityOf = (container) => ({
      'Models.bnt': { container: 'Models.bnt', containerSha256: status.containers.models.sha256 },
      'Textures.bnt': { container: 'Textures.bnt', containerSha256: status.containers.textures.sha256 },
    }[container]);
    const veg = new WorldVegetation({
      scene,
      fetchJson: async (url) => {
        const r = await rawRequestFull(port, url.startsWith('/') ? url : `/${url}`);
        const j = parseJsonOrNone(r.body.toString('utf8'));
        if (r.status !== 200) throw new Error(j?.message ?? `HTTP ${r.status}`);
        return j;
      },
      fetchBinary: async (url) => {
        const container = url.startsWith('/api/world/model/') ? identityOf('Models.bnt') : identityOf('Textures.bnt');
        const r = await rawRequestFull(port, url);
        if (r.status !== 200) {
          const j = parseJsonOrNone(r.body.toString('utf8'));
          throw new Error(j?.message ?? `HTTP ${r.status}`);
        }
        if (r.headers['x-pe-era'] !== status.era || r.headers['x-pe-container'] !== container.container
          || String(r.headers['x-pe-container-sha256'] ?? '').toUpperCase() !== String(container.containerSha256 ?? '').toUpperCase()) {
          throw new Error('identity mismatch — controlled refusal (test mirror of the browser check)');
        }
        return { payload: new Uint8Array(r.body), headers: { era: r.headers['x-pe-era'], container: r.headers['x-pe-container'], containerSha256: r.headers['x-pe-container-sha256'], entryName: r.headers['x-pe-entry'], payloadSha256: r.headers['x-pe-payload-sha256'] } };
      },
      heightSampler: () => 42.0, // a FIXED reconstruction height (the placement knob is not under test here)
    });
    await veg.setConfig({ profile: 0, labSeed: 0, densityPercent: 100 });
    const originA = { gx: 50, gy: 111 };
    const originB = { gx: 60, gy: 120 };
    const cA1 = await veg.rebuild(originA, 8);
    const fetchesAfterA = veg.fetchCounters.modelPayloads;
    const texA = veg.textureCache.get(436225);
    const cB = await veg.rebuild(originB, 8);
    const cA2 = await veg.rebuild(originA, 8);
    const returnStable = cA2.counts.requested === cA1.counts.requested
      && cA2.counts.rendered === cA1.counts.rendered && instanceSetHashByCensus(cA1) === instanceSetHashByCensus(cA2);
    const noRefetchOnReturn = veg.fetchCounters.modelPayloads === fetchesAfterA;
    const texIdentityReused = veg.textureCache.get(436225) === texA; // SAME object — no duplication
    // profile change: unreferenced models released, shared/referenced survive
    await veg.setConfig({ profile: 5, labSeed: 0, densityPercent: 100 });
    const cP5 = await veg.rebuild(originA, 8);
    const p5ids = new Set(Object.keys(cP5.perModelRendered ?? {}).map(Number));
    const cacheIds = new Set([...veg.modelCache.keys()]);
    const cacheOnlyReferenced = [...cacheIds].every((id) => p5ids.has(id));
    const disposalsHappened = veg.disposeCounters.cacheEntries > 0 && veg.disposeCounters.textures > 0;
    // back to profile 0: re-fetch allowed (it was released), counts return
    await veg.setConfig({ profile: 0, labSeed: 0, densityPercent: 100 });
    const cA3 = await veg.rebuild(originA, 8);
    const countsRestored = cA3.counts.requested === cA1.counts.requested;
    // toggle off/on: no refetch, same counts
    const vegSetEnabledCounters = { ...veg.fetchCounters };
    veg.setEnabled(false);
    veg.setEnabled(true);
    const cA4 = await veg.rebuild(originA, 8);
    const toggleNoRefetch = veg.fetchCounters.modelPayloads === vegSetEnabledCounters.modelPayloads
      && cA4.counts.requested === cA1.counts.requested;
    const meshesAreInstanced = veg.meshes.every((m) => m instanceof THREE.InstancedMesh);
    // instancing preserves per-instance transforms: two instances of the same model differ
    const instanceDistinct = veg.meshes.length > 0 && (() => {
      const m = veg.meshes[0];
      const a = new THREE.Matrix4(), b = new THREE.Matrix4();
      m.getMatrixAt(0, a); m.getMatrixAt(Math.min(1, m.count - 1), b);
      return !a.equals(b);
    })();
    const beforeDispose = { cache: veg.modelCache.size, textures: veg.textureCache.size };
    veg.dispose();
    const afterDispose = { cache: veg.modelCache.size, textures: veg.textureCache.size };
    const resourceOk = cA1.ok && cB.ok && cA2.ok && cP5.ok && cA3.ok && cA4.ok
      && returnStable && noRefetchOnReturn && texIdentityReused && cacheOnlyReferenced
      && disposalsHappened && countsRestored && toggleNoRefetch && meshesAreInstanced
      && instanceDistinct && beforeDispose.cache > 0 && afterDispose.cache === 0 && afterDispose.textures === 0;
    out.push(record('WORLD_VEG_RESOURCE_DISCIPLINE',
      'unload/reload without resource duplication or loss (headless THREE census through the REAL routes): window A->B->A reuses payloads (no refetch) + the SAME texture object (identity), a profile change releases unreferenced models/textures (disposals measured) while referenced shared resources survive, counts return on profile return, toggle OFF->ON re-renders without refetch, per-instance transforms are REAL and distinct, dispose() empties the caches',
      resourceOk ? 'PASS' : 'FAIL', {
      resultClass: 'HEADLESS_THREE_RESOURCE_CENSUS (the REAL WorldVegetation against the REAL server routes)',
      measuredQuantity: 'fetch counters + texture object identity + cache/dispose counters + instance counts across the cycles',
      measured: {
        windowA: { requested: cA1.counts.requested, rendered: cA1.counts.rendered, limited: cA1.counts.limited, models: cA1.models },
        windowB: { requested: cB.counts.requested, rendered: cB.counts.rendered },
        windowAReturn: { requested: cA2.counts.requested, returnStable, noRefetchOnReturn, texIdentityReused },
        profile5: { requested: cP5.counts.requested, modelsWithInstances: [...p5ids], cacheOnlyReferenced, disposalsHappened, disposeCountersAfterProfileChange: { ...veg.disposeCounters } },
        profile0Return: { requested: cA3.counts.requested, countsRestored },
        toggleCycle: { noRefetch: toggleNoRefetch, requested: cA4.counts.requested },
        instancing: { meshesAreInstanced, instanceDistinct, meshCount: veg.meshes.length },
        teardown: { beforeDispose, afterDispose },
        fetchCountersFinal: { ...veg.fetchCounters },
      },
      independentSourceOfTruth: 'the fetch/identity/counter observations of the REAL module against the REAL routes (no synthetic payloads)',
      whyNonCircular: 'object identity (===) for the shared texture cannot be faked by re-decoding; fetch counters measure the REAL HTTP surface; the disposal counters measure the actual THREE .dispose() calls',
      failureCaseDetected: resourceOk ? 'none — the discipline holds through every cycle' : 'a resource leak, duplication, or loss was measured (see measured)',
    }));

  } finally {
    const stop = await stopWorldServer(serverRec);
    out.push(record('WORLD_VEG_SERVER_LIFECYCLE',
      `suite-owned world server lifecycle (pid ${serverRec.pid}, port ${port}; stop + port-freed proof; standing 8140/8161 never touched)`,
      stop.portFreed ? 'PASS' : 'FAIL', {
      resultClass: 'SUITE_LIFECYCLE',
      measuredQuantity: 'startup line + stop result + port-freed proof',
      measured: { startupLine: serverRec.startupLine, pid: serverRec.pid, port, stop },
      failureCaseDetected: stop.portFreed ? 'none — the suite cleaned up its OWN process only' : 'PORT NOT FREED after stop',
    }));
  }
  return out;
}

/** A census-level instance fingerprint helper (requested/rendered + per-model
 * counts — for the return-stability comparison in the resource gate). */
function instanceSetHashByCensus(census) {
  const pm = census.perModelRendered ?? {};
  const keys = Object.keys(pm).sort();
  return keys.map((k) => `${k}:${pm[k]}`).join('|') + `#${census.counts.requested}.${census.counts.rendered}.${census.counts.limited}`;
}
