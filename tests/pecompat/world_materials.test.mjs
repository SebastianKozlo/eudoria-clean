// world_materials.test.mjs — PE_WORLD_LAUNCHER_R1_20261010, ETAP D (contract §5 + §8)
// THE MATERIALS GATE BATTERY: the proven chain TDF material record → material
// id/name → <id>.dat texture entry (the engine-RE-confirmed id@+16 relation,
// re-measured per sample) → PCG Textures.bnt payload → the strict decoder →
// RGBA → the GPU splat data — through the PRODUCTION modules AND the REAL
// HTTP routes, with INDEPENDENT test-local byte readers for every bit-exact
// claim.
//
// PREREGISTERED EXPECTATIONS (written BEFORE execution — not corrected to
// match obtained results; a failing prediction is reported as a failure with
// its measured value):
//   1. MASK56_NEGATIVE: for every named material record of the sampled tiles
//      the mask region at record+56 decodes (RAW u8[256] or RLE (count,value)
//      with EXACT consumption). The KNOWN-WRONG offset 52 is the negative
//      control: for RAW-encoded records (size=308) the region at 52 is 260 B
//      → decodeMaskRegion REFUSES (not 256; the RLE attempt fails on raw
//      content) — EXPECTED DISCRIMINATING. For RLE-encoded records with
//      extra4 == [0,0,0,0] (measured on samples) the region at 52 = region56
//      + 4 leading zero-count pairs → the expanded mask EQUALS the mask56
//      (DEGENERATE for value; the structural region LENGTHS still differ) —
//      EXPECTED measured-degenerate, recorded honestly (the same pattern as
//      the phase-3 offset-64 all-zero tile). Structural proof: a 256-B mask
//      ending at p+4+size can only start at p+56 — at 52 the record would
//      not consume exactly.
//   2. WIRE_BITEXACT: the served base64 masks are BIT-EXACT the physical tail
//      region bytes (RAW) / the independent RLE expansion (RLE) — 256/256 per
//      record; per-cell layer sums are served UNNORMALIZED (sums > 255 are
//      original data; measured min/max recorded).
//   3. MALFORMED_CONTROLLED: synthetic malformed tails (RLE overrun, odd
//      region, implausible size, residual bytes) and malformed TGA payloads
//      (32bpp, missing TRUEVISION footer, truncated) all FAIL LOUDLY through
//      the production decoders — no mask, no rgba, no fallback.
//   4. CHAIN_RESOLVE: every named material id of the sampled tiles resolves
//      "<id>.dat" in the pinned Textures.bnt; the server's entry metadata
//      equals the INDEPENDENT index parse; the texture wire bytes equal the
//      independent file reads BIT-EXACT; every sampled payload decodes with
//      the production decodeTga2 (TGA2 24bpp 256x256, TRUEVISION footer).
//      A missing id (999999999) is a loud 404. Double-fetch = HIT.
//   5. ERA_REFUSAL: ?era=CD_JAN_2003 and ?era=CD_2003 are REFUSED (403
//      ERA_REFUSED_WRONG_ERA) through the REAL routes; no era param serves
//      the default PCG_9_3_5 data. The CAM-C3 cache-identity mutants (wrong
//      era / containerSha / entryName / tampered payload / wrong wire
//      version) are REFUSED with named reasons through the PRODUCTION
//      verify functions; clean PASSES the same gate.
//   6. UNRESOLVED_BINDING: a synthetic unresolved relation through the pure
//      production splat builder: the layer is SKIPPED + listed (explicit
//      diagnostic), NO texture slot assigned, resolved layers still applied;
//      an all-resolved grid has diagnostic.mode NONE.
//   7. UV_FLIP_CONTROL: a synthetic PATTERN texture (TGA2 24bpp, distinct
//      per-row colors) + a REAL texture: decodeTga2 returns IMAGE order
//      (row 0 = the LAST stored row = visual TOP) — distinguished from the
//      A32 FILE-row convention (decodeTga2A32: row 0 = the FIRST stored row)
//      on the SAME synthetic payload shape; the documented GPU sampling
//      convention (sampleTexelImageOrder, flipY=false) is consistent with
//      the decoder output on BOTH the pattern and the real payload.
//   8. SPLAT_RAW_WEIGHTS: the REAL spawn-window materials (64 tiles via the
//      HTTP route) through buildRegionSplatData: an independent re-walk
//      proves the wTextures bytes are the RAW served mask weights (bit-exact,
//      slot order = record order per cell), slot indices reference only
//      resolved textures, and the active-layers histogram matches an
//      independent count.
import { readFileSync } from 'node:fs';
import { openSync, readSync, closeSync, statSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { inflateSync } from 'node:zlib';

import { PESourceMount } from '../../src/pesource/PESourceMount.js';
import { decodeMaskRegion, decodeMaterialTail, MATERIAL_TAIL_START } from '../../src/pesource/TdfMaterialTailDecoder.js';
import { decodeTga2, decodeTga2A32 } from '../../src/pesource/TgaDecoder.js';
import {
  verifyTextureCacheIdentity, verifyMaterialsCacheIdentity,
  TEXTURE_WIRE_VERSION, MATERIALS_WIRE_VERSION,
} from '../../compat/server-world.mjs';
import {
  buildRegionSplatData, sampleTexelImageOrder, worldUV,
  RENDER_RECONSTRUCTION_PRESET, REGION_CELLS,
} from '../../compat/world-splat.js';
import {
  startWorldServer, stopWorldServer, findFreePort, rawRequestFull, parseJsonOrNone,
} from './_world_server_helpers.mjs';

const PIN_TERRAIN_SHA = '95841761CE4EA074C97930EC1CEF3FB57AAC7F7F4F3D9B751A9EE60510299990';
const PIN_TEXTURES_SHA = '61ACD13B140E130647EEE24C1E2669D3734990B76CF74897DDD3BA0F4EA61393';
const TERRAIN_PATH_DEFAULT = 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Terrain\\terrain.bnt';
const TEXTURES_PATH_DEFAULT = 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Textures\\Textures.bnt';
const WIN_ORIGIN = { gx: 50, gy: 111 }; // the default world window (max-mean tile 53,114 → origin 50,111)

function rec(id, name, status, extra = {}) {
  return { id, name, status, ...extra };
}
function tileName(gx, gy) { return gx.toString(16).padStart(4, '0') + gy.toString(16).padStart(4, '0') + '.tdf'; }
const sha256Hex = (u8) => createHash('sha256').update(Buffer.from(u8.buffer ?? u8)).digest('hex');

// ---------------------------------------------------------------------------
// INDEPENDENT test-local readers (NO production import in these functions)
// ---------------------------------------------------------------------------
/** Minimal BNT2-terrain entry read: own footer/dir walk + inflate (mirrors
 * the world_terrain.test.mjs independent reader). Returns the FULL payload. */
function independentReadTerrainPayload(bytes, wantedName) {
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
      if (dv.getUint32(offset, true) !== 0xff000002) throw new Error(`indep: bad marker at ${offset}`);
      const declared = dv.getUint32(offset + 4, true);
      const payload = inflateSync(bytes.subarray(offset + 8, offset + size));
      if (payload.length !== declared) throw new Error(`indep: inflate ${payload.length} != ${declared}`);
      return new Uint8Array(payload);
    }
  }
  return null;
}

/** Independent named-material-record walk of one tail (stride size+4; the
 * mask region at record+56; the WRONG region at record+52 for the negative
 * control; INDEPENDENT RLE expansion). */
function independentWalkTail(tail) {
  const dv = new DataView(tail.buffer, tail.byteOffset, tail.byteLength);
  const out = [];
  let p = 0;
  while (p < tail.byteLength) {
    const size = dv.getUint32(p, true);
    const dim = dv.getUint32(p + 4, true);
    if (size < 8 || size > tail.byteLength - p) throw new Error(`indep: implausible size ${size} at ${p}`);
    const end = p + 4 + size;
    const nameBytes = tail.subarray(p + 24, p + 52);
    let endNul = nameBytes.indexOf(0); if (endNul === -1) endNul = nameBytes.length;
    let nm = ''; let printable = true;
    for (let i = 0; i < endNul; i++) { const c = nameBytes[i]; if (c >= 0x20 && c < 0x7f) nm += String.fromCharCode(c); else printable = false; }
    const id = dv.getUint32(p + 16, true);
    const region56 = tail.subarray(p + 56, end);
    const region52 = tail.subarray(p + 52, end);
    const extra4 = Array.from(tail.subarray(p + 52, p + 56));
    const isNamed = dim === 16 && printable && nm.length > 0;
    let mask56 = null, enc56 = null, mask52Expanded = null, enc52 = null, mask52Equal = null;
    if (isNamed) {
      if (region56.length === 256) { mask56 = new Uint8Array(region56); enc56 = 'raw'; }
      else if (region56.length % 2 === 0) {
        const m = new Uint8Array(256); let wp = 0, rp = 0, ok = true;
        while (rp < region56.length) { const c = region56[rp++], v = region56[rp++]; if (wp + c > 256) { ok = false; break; } m.fill(v, wp, wp + c); wp += c; }
        if (ok && wp === 256) { mask56 = m; enc56 = 'rle'; }
      }
      // the WRONG offset: same expansion attempt at 52 (the negative control)
      if (region52.length === 256) { mask52Expanded = new Uint8Array(region52); enc52 = 'raw_len256'; }
      else if (region52.length % 2 === 0) {
        const m = new Uint8Array(256); let wp = 0, rp = 0, ok = true;
        while (rp < region52.length) { const c = region52[rp++], v = region52[rp++]; if (wp + c > 256) { ok = false; break; } m.fill(v, wp, wp + c); wp += c; }
        if (ok && wp === 256) { mask52Expanded = m; enc52 = 'rle'; }
        else enc52 = `refused_region_${region52.length}B`;
      } else enc52 = `refused_region_${region52.length}B`;
      if (mask56 && mask52Expanded) {
        mask52Equal = mask56.every((b, i) => b === mask52Expanded[i]);
      }
    }
    out.push({ p, size, dim, id, name: nm, isNamed, mask56, enc56, mask52Expanded, enc52, mask52Equal, extra4, region56Len: region56.length, region52Len: region52.length, end });
    p = end;
  }
  if (p !== tail.byteLength) throw new Error(`indep: tail not consumed exactly (${p} != ${tail.byteLength})`);
  return out;
}

/** Independent LAZY parse of the pinned Textures.bnt index (own footer read +
 * directory walk via fs reads — independent of the server's
 * LazyTextureArchive). Returns { byId, footer } with byId = Map(id → entry). */
function independentTextureIndex(filePath) {
  const fd = openSync(filePath, 'r');
  try {
    const fsize = statSync(filePath).size;
    const footer = Buffer.alloc(8);
    readSync(fd, footer, 0, 8, fsize - 8);
    const dirOffset = footer.readUInt32LE(0);
    const magic = footer.subarray(4, 8).toString('latin1');
    if (magic !== 'BNT2') throw new Error(`indep: bad texture footer magic ${magic}`);
    const dirBytes = fsize - dirOffset - 8;
    const dir = Buffer.alloc(dirBytes);
    readSync(fd, dir, 0, dirBytes, dirOffset);
    const dv = new DataView(dir.buffer, dir.byteOffset, dir.byteLength);
    const count = dv.getUint32(0, true);
    let p = 4;
    const byId = new Map();
    while (p < dir.length) {
      let end = p; while (end < dir.length && dir[end] !== 0x0a) end++;
      const name = dir.toString('latin1', p, end);
      const size = dv.getUint32(end + 1, true);
      const offset = dv.getUint32(end + 5, true);
      const m = /^(\d+)\.dat$/i.exec(name);
      if (m) byId.set(parseInt(m[1], 10), { name, size, offset });
      p = end + 17;
    }
    if (p !== dir.length) throw new Error(`indep: texture dir not consumed exactly (${p} != ${dir.length})`);
    return { byId, footer: { magic, dirOffset, dirBytes, countField: count, parsedEntries: byId.size } };
  } finally { closeSync(fd); }
}

/** Independent raw payload read at [offset, offset+size). */
function independentReadTexturePayload(filePath, entry) {
  const fd = openSync(filePath, 'r');
  try {
    const buf = Buffer.alloc(entry.size);
    const n = readSync(fd, buf, 0, entry.size, entry.offset);
    if (n !== entry.size) throw new Error(`indep: short read ${n} != ${entry.size}`);
    return new Uint8Array(buf);
  } finally { closeSync(fd); }
}

/** A synthetic TGA2 payload per the CONFIRMED subset (24bpp bottom-up,
 * TRUEVISION-XFILE footer) with DISTINCT per-row colors — the UV/flip
 * pattern control. Stored row r (file order) gets color (r*40+10, 250-r*30, 90+r*20). */
function syntheticPatternTga2({ width = 4, height = 4, bpp = 24 } = {}) {
  const idLength = 0;
  const bytesPerPixel = bpp / 8;
  const total = 18 + idLength + width * height * bytesPerPixel + 8 + 18;
  const buf = Buffer.alloc(total);
  buf[0] = idLength; buf[1] = 0; buf[2] = 2; // colorMapType=0, imageType=2 (uncompressed true-color)
  buf.writeUInt16LE(width, 12); buf.writeUInt16LE(height, 14);
  buf[16] = bpp; buf[17] = 0; // descriptor: bottom-up (top-down bit = 0)
  for (let r = 0; r < height; r++) {
    for (let c = 0; c < width; c++) {
      const i = 18 + (r * width + c) * bytesPerPixel;
      const storedRow = r; // file row r
      if (bpp === 24) {
        buf[i] = (storedRow * 40 + 10) & 0xff; // B slot (stored BGR)
        buf[i + 1] = (250 - storedRow * 30) & 0xff; // G
        buf[i + 2] = (90 + storedRow * 20) & 0xff; // R
      } else {
        buf[i] = (storedRow * 40 + 10) & 0xff; // B (BGRA)
        buf[i + 1] = (250 - storedRow * 30) & 0xff;
        buf[i + 2] = (90 + storedRow * 20) & 0xff;
        buf[i + 3] = 255;
      }
    }
  }
  buf.write('TRUEVISION-XFILE.\0', total - 18, 'latin1');
  return new Uint8Array(buf);
}

export async function run(ctx) {
  const records = [];
  const terrainPath = ctx.terrainPath ?? TERRAIN_PATH_DEFAULT;
  const texturesPath = ctx.texturesPath ?? TEXTURES_PATH_DEFAULT;
  const SAMPLED = [[53, 114], [50, 111], [57, 118], [110, 118], [0, 0], [219, 235]];

  // in-process production mount (fail-closed pin) for the pure-module gates
  const io = {
    readFile: async (p) => new Uint8Array(readFileSync(p)),
    inflate: async (b) => new Uint8Array(inflateSync(b)),
    sha256: async (b) => createHash('sha256').update(b).digest('hex'),
  };
  const mount = new PESourceMount(io);
  await mount.mountEra({ era: 'PCG_9_3_5', container: 'Terrain/terrain.bnt', path: terrainPath, format: 'BNT2_TERRAIN' });
  const terrainBytes = new Uint8Array(readFileSync(terrainPath));

  // ============================ GATE 1: mask@56 vs wrong 52 ============================
  {
    const perTile = [];
    let allDecode56 = true, rawDiscriminating = 0, rawTotal = 0, rleTotal = 0, rleDegenerate = 0, rleDiscriminating = 0;
    for (const [gx, gy] of SAMPLED) {
      const name = tileName(gx, gy);
      const payload = independentReadTerrainPayload(terrainBytes, name);
      const tail = payload.subarray(MATERIAL_TAIL_START);
      const walk = independentWalkTail(tail);
      const named = walk.filter((r) => r.isNamed);
      // the PRODUCTION decoder must agree on the same tail (exact consumption + masks)
      const prod = decodeMaterialTail(tail);
      let prodOk = prod.consumed === tail.byteLength && prod.namedMaterials.length === named.length;
      for (let i = 0; i < named.length && prodOk; i++) {
        const pn = prod.namedMaterials[i];
        if (pn.id !== named[i].id || pn.name !== named[i].name) { prodOk = false; break; }
        if (!named[i].mask56 || !pn.mask) { if (!(!named[i].mask56 && !pn.mask)) { prodOk = false; break; } continue; }
        for (let c = 0; c < 256; c++) if (pn.mask[c] !== named[i].mask56[c]) { prodOk = false; break; }
      }
      if (!prodOk) allDecode56 = false;
      for (const r of named) {
        if (!r.mask56) { allDecode56 = false; continue; }
        if (r.enc56 === 'raw') {
          rawTotal++;
          // EXPECTED: the 260-byte region at 52 is REFUSED by the production decoder
          const d52 = decodeMaskRegion(tail.subarray(r.p + 52, r.end), 16);
          if (d52.mask === null) rawDiscriminating++;
        } else {
          rleTotal++;
          if (r.mask52Equal === true) rleDegenerate++;
          else if (r.mask52Equal === false) rleDiscriminating++;
        }
      }
      perTile.push({
        name, namedRecords: named.length,
        masks: named.map((r) => ({ id: r.id, name: r.name, enc: r.enc56, extra4: r.extra4, mask52Equal: r.mask52Equal })),
        prodAgrees: prodOk,
      });
    }
    const gateOk = allDecode56 && rawTotal > 0 && rawDiscriminating === rawTotal;
    records.push(rec('WORLD_MAT_MASK56_NEGATIVE',
      'named material record mask@record+56 verified on physical samples (production + independent walk); the wrong offset 52 as the negative control',
      gateOk ? 'PASS' : 'FAIL', {
        measuredQuantity: 'per-record mask decode at 56 (RAW/RLE exact) vs the wrong-52 region; extra4 census',
        measured: {
          sampledTiles: SAMPLED.length,
          rawRecords: { total: rawTotal, refusedAtWrong52: rawDiscriminating },
          rleRecords: { total: rleTotal, maskEqualsWrong52WithZeroExtra4: rleDegenerate, differing: rleDiscriminating },
          productionIndependentAgreement: allDecode56,
          note: 'RAW records: region@52 = 260B -> production decodeMaskRegion REFUSES (not 256; RLE fails on raw content) — DISCRIMINATING. RLE records with extra4=[0,0,0,0] (measured): region@52 = region56+4 leading zero-count pairs -> the expanded mask equals mask56 (degenerate for VALUE; the region LENGTHS differ: measured). Structure: a 256-B mask ending at p+4+size can only start at p+56 (exact consumption fails at 52).',
          perTile,
        },
        independentSourceOfTruth: 'test-local minimal tail walker (own DataView, own RLE expansion, own stride walk)',
        whyNonCircular: 'the masks and refusals are recomputed from the physical file bytes by code that does not import the production decoder',
        failureCaseDetected: gateOk ? 'none' : 'a named record failed to decode at 56, or the wrong-52 control stopped discriminating on RAW records',
      }));
  }

  // ============================ GATE 2: raw weights bit-exact through the wire ============================
  {
    const port = ctx.worldPort ?? (await findFreePort(8162));
    const serverRec = await startWorldServer({ port });
    try {
      let bitexact = true, recordsChecked = 0, weightBytesChecked = 0, sumMin = 0xffffffff, sumMax = 0, cellsAbove255 = 0, totalCells = 0;
      const perTile = [];
      for (const [gx, gy] of SAMPLED) {
        const name = tileName(gx, gy);
        const r = await rawRequestFull(port, `/api/world/tile/${gx}/${gy}/materials`);
        const j = parseJsonOrNone(r.body.toString('utf8'));
        const payload = independentReadTerrainPayload(terrainBytes, name);
        const tail = payload.subarray(MATERIAL_TAIL_START);
        const walk = independentWalkTail(tail).filter((x) => x.isNamed);
        let tileOk = r.status === 200 && j && j.ok === true && Array.isArray(j.materials) && j.materials.length === walk.length;
        for (let i = 0; i < walk.length && tileOk; i++) {
          const servedB64 = j.materials[i].maskBase64;
          const servedMask = Buffer.from(servedB64, 'base64');
          const indepMask = walk[i].mask56;
          recordsChecked++;
          if (servedMask.length !== 256 || !indepMask) { tileOk = false; break; }
          for (let c = 0; c < 256; c++) {
            if (servedMask[c] !== indepMask[c]) { tileOk = false; break; }
            weightBytesChecked++;
          }
        }
        // per-cell layer sums of the SERVED masks (no normalization anywhere)
        for (let c = 0; c < 256; c++) {
          totalCells++;
          let sum = 0;
          for (const m of (j?.materials ?? [])) sum += Buffer.from(m.maskBase64, 'base64')[c];
          if (sum < sumMin) sumMin = sum;
          if (sum > sumMax) sumMax = sum;
          if (sum > 255) cellsAbove255++;
        }
        if (!tileOk) bitexact = false;
        perTile.push({ name, servedMaterials: j?.materials?.length ?? 0, independentNamed: walk.length, tileOk });
      }
      records.push(rec('WORLD_MAT_WIRE_BITEXACT',
        'the served RAW 16x16 masks are bit-exact the physical tail bytes (independent reader); sums > 255 preserved UNNORMALIZED',
        bitexact && recordsChecked > 0 ? 'PASS' : 'FAIL', {
          measuredQuantity: 'bit-exact mask bytes vs independent tail reads + per-cell layer-sum range',
          measured: {
            sampledTiles: SAMPLED.length, recordsChecked, weightBytesChecked,
            perCellLayerSums: { min: sumMin === 0xffffffff ? null : sumMin, max: sumMax, cellsAbove255, totalCells },
            note: 'layer sums > 255 are ORIGINAL DATA (never normalized — measured, not asserted)',
            perTile,
          },
          independentSourceOfTruth: 'test-local minimal reader + own RLE expansion',
          whyNonCircular: 'the wire payload is compared to the physical container bytes read by independent code',
          failureCaseDetected: bitexact ? 'none' : 'a served mask differed from the independent byte read (pipeline modified raw weights)',
        }));
      ctx.materialsPort = port; // reuse THIS server for the remaining HTTP gates
      ctx.materialsServer = serverRec;
      try {
        // ============================ GATE 4: chain resolve + texture wire ============================
        {
          const indepIndex = independentTextureIndex(texturesPath);
          let allResolved = true, chainSamples = [], wireOk = true, decodeOk = true, missingRefused = false, hitOk = false;
          const idsToCheck = new Set();
          for (const [gx, gy] of SAMPLED) {
            const r = await rawRequestFull(port, `/api/world/tile/${gx}/${gy}/materials`);
            const j = parseJsonOrNone(r.body.toString('utf8'));
            for (const m of (j?.materials ?? [])) {
              idsToCheck.add(m.id);
              if (m.texture?.resolved !== true) allResolved = false;
              else {
                const indepEntry = indepIndex.byId.get(m.id);
                if (!indepEntry || indepEntry.size !== m.texture.size || indepEntry.offset !== m.texture.offset) allResolved = false;
              }
            }
          }
          for (const id of idsToCheck) {
            const r = await rawRequestFull(port, `/api/world/texture/${id}`);
            const indepEntry = indepIndex.byId.get(id);
            const indepPayload = indepEntry ? independentReadTexturePayload(texturesPath, indepEntry) : null;
            let thisOk = r.status === 200 && indepPayload
              && r.body.byteLength === indepPayload.byteLength
              && Buffer.from(r.body).equals(Buffer.from(indepPayload));
            if (!thisOk) wireOk = false;
            const headerSha = r.headers['x-pe-payload-sha256'];
            if (String(headerSha ?? '').toLowerCase() !== sha256Hex(new Uint8Array(r.body)).toLowerCase()) wireOk = false;
            let dec = null;
            try { dec = decodeTga2(new Uint8Array(r.body)); } catch { dec = null; }
            if (!dec || dec.width !== 256 || dec.height !== 256 || dec.header.bpp !== 24 || dec.footerOk !== true) decodeOk = false;
            chainSamples.push({ id, bytes: r.body.byteLength, wireBitExact: thisOk, decode: dec ? 'OK 256x256x24' : 'FAILED' });
          }
          // the SYNTHETIC missing relation: a id with NO entry — loud 404
          const miss = await rawRequestFull(port, '/api/world/texture/999999999');
          missingRefused = miss.status === 404;
          // cache HIT: double-fetch = identical bytes + HIT state
          const first = await rawRequestFull(port, '/api/world/texture/13382');
          const second = await rawRequestFull(port, '/api/world/texture/13382');
          hitOk = first.status === 200 && second.status === 200
            && second.headers['x-pe-cache-state'] === 'HIT'
            && Buffer.from(first.body).equals(Buffer.from(second.body));
          const gateOk = allResolved && idsToCheck.size > 0 && wireOk && decodeOk && missingRefused && hitOk;
          records.push(rec('WORLD_MAT_CHAIN_RESOLVE',
            'every sampled material id resolves "<id>.dat" (server == independent index parse); texture wire bytes bit-exact the independent file reads; strict decodeTga2 subset holds; missing id = loud 404; double-fetch = HIT',
            gateOk ? 'PASS' : 'FAIL', {
              measuredQuantity: 'resolved ids / wire bytes / decode subset / refusal / cache state',
              measured: {
                distinctMaterialIds: idsToCheck.size, allResolved, wireBitExact: wireOk, decodeSubsetOk: decodeOk,
                missingIdRefused404: missingRefused, doubleFetchCacheHit: hitOk,
                independentIndex: { parsedEntries: indepIndex.footer.parsedEntries, countField: indepIndex.footer.countField },
                chainSamples,
                relationEvidence: 'id@+16 -> "<id>.dat" (engine RE: 9.3.5 record parse reads sub@+16 as the material TEXTURE id — M1_TSFS iter015e/f, iter030, EU935 census GROUND_TEXTURES §3 CONFIRMED; re-measured per sample HERE)',
              },
              independentSourceOfTruth: 'test-local lazy Textures.bnt index parse + raw file reads',
              whyNonCircular: 'the wire payloads/metadata are compared to the physical container read by independent code',
              failureCaseDetected: gateOk ? 'none' : 'a chain step failed (unresolved id, wire mismatch, decode failure, missing-id not refused, or cache identity broken)',
            }));
        }

        // ============================ GATE 5: era refusal + CAM-C3 mutants ============================
        {
          const eraChecks = [];
          for (const era of ['CD_JAN_2003', 'CD_2003', 'JUL_2003']) {
            const rt = await rawRequestFull(port, `/api/world/texture/13382?era=${era}`);
            const rm = await rawRequestFull(port, `/api/world/tile/53/114/materials?era=${era}`);
            eraChecks.push({
              era, textureStatus: rt.status, textureError: parseJsonOrNone(rt.body.toString('utf8'))?.error,
              materialsStatus: rm.status, materialsError: parseJsonOrNone(rm.body.toString('utf8'))?.error,
            });
          }
          const noEra = await rawRequestFull(port, '/api/world/texture/13382');
          const eraGateOk = eraChecks.every((c) => c.textureStatus === 403 && c.textureError === 'ERA_REFUSED_WRONG_ERA'
            && c.materialsStatus === 403 && c.materialsError === 'ERA_REFUSED_WRONG_ERA')
            && noEra.status === 200;
          // CAM-C3 mutants through the PRODUCTION verify functions
          const texIdentity = { era: 'PCG_9_3_5', container: 'Textures.bnt', containerSha256: PIN_TEXTURES_SHA.toLowerCase() };
          const goodPayload = new Uint8Array(197);
          const texEntry = (over) => ({
            payload: over.payload ?? goodPayload,
            identity: {
              era: over.era ?? texIdentity.era,
              container: over.container ?? texIdentity.container,
              containerSha256: over.containerSha256 ?? texIdentity.containerSha256,
              entryName: over.entryName ?? '13382.dat',
              wireVersion: over.wireVersion ?? TEXTURE_WIRE_VERSION,
              payloadSha256: over.payloadSha256 ?? sha256Hex(goodPayload),
            },
          });
          const vtex = (e) => verifyTextureCacheIdentity(e, texIdentity, { expectedEntryName: '13382.dat' });
          const matIdentity = { era: 'PCG_9_3_5', container: 'Terrain/terrain.bnt', containerSha256: PIN_TERRAIN_SHA.toLowerCase() };
          const goodTail = new Uint8Array(64);
          const matEntry = (over) => ({
            tail: over.tail ?? goodTail,
            identity: {
              era: over.era ?? matIdentity.era,
              container: over.container ?? matIdentity.container,
              containerSha256: over.containerSha256 ?? matIdentity.containerSha256,
              entryName: over.entryName ?? '00350072.tdf',
              wireVersion: over.wireVersion ?? MATERIALS_WIRE_VERSION,
              payloadSha256: over.payloadSha256 ?? sha256Hex(goodTail),
            },
          });
          const vmat = (e) => verifyMaterialsCacheIdentity(e, matIdentity, { expectedEntryName: '00350072.tdf' });
          const mutants = {
            texWrongEra: vtex(texEntry({ era: 'CD_JAN_2003' })),
            texWrongContainerSha: vtex(texEntry({ containerSha256: '0'.repeat(64) })),
            texWrongEntryName: vtex(texEntry({ entryName: '20281.dat' })),
            texTamperedPayload: vtex(texEntry({ payload: new Uint8Array(197).fill(1) })),
            texWrongWireVersion: vtex(texEntry({ wireVersion: 'bogus-v9' })),
            texClean: vtex(texEntry({})),
            matWrongEra: vmat(matEntry({ era: 'CD_JAN_2003' })),
            matWrongContainerSha: vmat(matEntry({ containerSha256: '0'.repeat(64) })),
            matWrongEntryName: vmat(matEntry({ entryName: '00000000.tdf' })),
            matTamperedTail: vmat(matEntry({ tail: new Uint8Array(64).fill(7) })),
            matWrongWireVersion: vmat(matEntry({ wireVersion: 'bogus-v9' })),
            matClean: vmat(matEntry({})),
          };
          const mutantOk =
            mutants.texWrongEra.ok === false && mutants.texWrongEra.reasons.includes('ERA_MISMATCH')
            && mutants.texWrongContainerSha.ok === false && mutants.texWrongContainerSha.reasons.includes('CONTAINER_SHA_MISMATCH')
            && mutants.texWrongEntryName.ok === false && mutants.texWrongEntryName.reasons.includes('ENTRY_NAME_MISMATCH')
            && mutants.texTamperedPayload.ok === false && mutants.texTamperedPayload.reasons.includes('PAYLOAD_SHA_MISMATCH')
            && mutants.texWrongWireVersion.ok === false && mutants.texWrongWireVersion.reasons.includes('WIRE_VERSION_MISMATCH')
            && mutants.texClean.ok === true
            && mutants.matWrongEra.ok === false && mutants.matWrongEra.reasons.includes('ERA_MISMATCH')
            && mutants.matWrongContainerSha.ok === false && mutants.matWrongContainerSha.reasons.includes('CONTAINER_SHA_MISMATCH')
            && mutants.matWrongEntryName.ok === false && mutants.matWrongEntryName.reasons.includes('ENTRY_NAME_MISMATCH')
            && mutants.matTamperedTail.ok === false && mutants.matTamperedTail.reasons.includes('PAYLOAD_SHA_MISMATCH')
            && mutants.matWrongWireVersion.ok === false && mutants.matWrongWireVersion.reasons.includes('WIRE_VERSION_MISMATCH')
            && mutants.matClean.ok === true;
          records.push(rec('WORLD_MAT_ERA_REFUSAL',
            'wrong-era labels REFUSED through the REAL routes (CD_JAN_2003/CD_2003/JUL_2003 -> 403); CAM-C3 identity mutants REFUSED through the PRODUCTION verify functions; clean passes the same gate',
            eraGateOk && mutantOk ? 'PASS' : 'FAIL', {
              measuredQuantity: 'HTTP refusals + verifyTextureCacheIdentity/verifyMaterialsCacheIdentity verdicts',
              measured: { eraChecks, noEraDefaultStatus: noEra.status, mutants },
              independentSourceOfTruth: 'raw sockets against the running server + the exported production verify functions',
              whyNonCircular: 'the mutants are constructed in-test and the refusal reasons are asserted by name',
              failureCaseDetected: eraGateOk && mutantOk ? 'none' : 'an era label was served, or an identity mutant passed the cache gate',
            }));
        }

        // ============================ GATE 8: the REAL window through the pure splat builder ============================
        {
          const grid = [];
          for (let dy = 0; dy < 8; dy++) {
            const row = [];
            for (let dx = 0; dx < 8; dx++) row.push(null);
            grid.push(row);
          }
          let fetchOk = true;
          for (let dy = 0; dy < 8; dy++) {
            for (let dx = 0; dx < 8; dx++) {
              const r = await rawRequestFull(port, `/api/world/tile/${WIN_ORIGIN.gx + dx}/${WIN_ORIGIN.gy + dy}/materials`);
              const j = parseJsonOrNone(r.body.toString('utf8'));
              if (r.status !== 200 || !j?.ok) { fetchOk = false; continue; }
              grid[dy][dx] = j;
            }
          }
          const atobFn = (s) => Buffer.from(s, 'base64').toString('binary');
          const data = buildRegionSplatData(grid, { atobFn });
          // INDEPENDENT re-walk: per tile/cell the active layers in RECORD ORDER
          // must appear in the w/idx textures with the RAW served weights
          let weightsOk = true, slotsOk = true, histOk = true, checkedCells = 0, checkedWeights = 0;
          const hist = new Map();
          for (let ty = 0; ty < 8 && weightsOk; ty++) {
            for (let tx = 0; tx < 8 && weightsOk; tx++) {
              const tile = grid[ty][tx];
              const mats = [...tile.materials].sort((a, b) => a.position - b.position);
              const masks = mats.map((m) => Buffer.from(m.maskBase64, 'base64'));
              const resolved = mats.map((m) => m.texture?.resolved === true);
              for (let cy = 0; cy < 16; cy++) {
                for (let cx = 0; cx < 16; cx++) {
                  const cellCol = tx * 16 + cx, cellRow = ty * 16 + cy;
                  const texel = (cellRow * REGION_CELLS + cellCol) * 4;
                  // expected: active layers (resolved only) in record order
                  const expected = [];
                  for (let i = 0; i < mats.length; i++) {
                    if (!resolved[i]) continue;
                    const w = masks[i][cy * 16 + cx];
                    if (w > 0) expected.push({ id: mats[i].id, w });
                  }
                  hist.set(expected.length, (hist.get(expected.length) ?? 0) + 1);
                  checkedCells++;
                  let slot = 0;
                  for (const e of expected) {
                    if (slot >= 16) break;
                    const idx = data.idxTextures[slot >> 2][texel + (slot & 3)];
                    const w = data.wTextures[slot >> 2][texel + (slot & 3)];
                    if (w !== e.w) weightsOk = false;
                    if (data.textureIds[idx] !== e.id) slotsOk = false;
                    checkedWeights++;
                    slot++;
                  }
                  // slots beyond the active count must be EMPTY (idx=255, w=0)
                  for (; slot < 16; slot++) {
                    const idx = data.idxTextures[slot >> 2][texel + (slot & 3)];
                    const w = data.wTextures[slot >> 2][texel + (slot & 3)];
                    if (idx !== 255 || w !== 0) { weightsOk = false; break; }
                  }
                }
              }
            }
          }
          const histExpected = Object.fromEntries([...hist.entries()].sort((a, b) => a[0] - b[0]).map(([k, v]) => [String(k), v]));
          const histGot = Object.fromEntries(Object.entries(data.activeLayersHist).map(([k, v]) => [String(k), v]));
          for (const [k, v] of Object.entries(histExpected)) if (histGot[k] !== v) histOk = false;
          for (const [k, v] of Object.entries(histGot)) if (histExpected[k] !== v) histOk = false;
          const gateOk = fetchOk && weightsOk && slotsOk && histOk && data.unresolved.length === 0 && checkedWeights > 0;
          records.push(rec('WORLD_MAT_SPLAT_RAW_WEIGHTS',
            'the REAL spawn-window materials through the pure splat builder: RAW served weights bit-exact in the GPU-bound textures (slot order = record order per cell), slots reference resolved textures only, active-layer histogram agrees with an independent count',
            gateOk ? 'PASS' : 'FAIL', {
              measuredQuantity: 'per-cell slot weights vs the served masks (independent re-walk) + histogram',
              measured: {
                windowOrigin: WIN_ORIGIN, tilesFetched: fetchOk ? 64 : 'FAILED',
                cellsChecked: checkedCells, weightSlotsChecked: checkedWeights,
                weightsBitExact: weightsOk, slotsConsistent: slotsOk, histogramAgrees: histOk,
                builderCensus: {
                  layersTotal: data.layersTotal, resolvedLayers: data.resolvedLayers, appliedLayers: data.appliedLayers,
                  distinctTextures: data.textureIds.length, unresolved: data.unresolved.length,
                  duplicates: data.duplicates, cappedCells: data.cappedCells,
                  cellsWithNoActiveLayers: data.cellsWithNoActiveLayers,
                  activeLayersHist: data.activeLayersHist,
                },
                preset: RENDER_RECONSTRUCTION_PRESET,
              },
              independentSourceOfTruth: 'test-local grid walk over the SERVED masks (the same wire payload the browser consumes)',
              whyNonCircular: 'the re-walk recomputes the expected slot weights from the wire JSON, independently of the builder',
              failureCaseDetected: gateOk ? 'none' : 'the GPU-bound weights diverged from the served raw masks (normalization leak) or the slot order broke',
            }));
        }
      } finally {
        // stop the suite-owned server (unless the outer ctx wants to keep it — it does not)
        const stop = await stopWorldServer(serverRec);
        records.push(rec('WORLD_MAT_SERVER_LIFECYCLE',
          `suite-owned world server lifecycle (pid ${serverRec.pid}, port ${port}; stop + port-freed proof)`,
          stop.portFreed ? 'PASS' : 'FAIL', {
            measuredQuantity: 'startup line + stop result + port-freed proof',
            measured: { startupLine: serverRec.startupLine, pid: serverRec.pid, port, stop },
            failureCaseDetected: stop.portFreed ? 'none — the suite cleaned up its OWN process only' : 'PORT NOT FREED after stop',
          }));
      }
    } catch (e) {
      // the server failed to start: record the honest failure and stop
      records.push(rec('WORLD_MAT_HTTP_GATES', 'the HTTP material gates (wire/chain/era/splat)', 'FAIL', {
        measuredQuantity: 'suite-owned server availability',
        measured: { error: String(e?.stack ?? e).slice(0, 2000) },
        failureCaseDetected: 'the suite-owned world server failed to start/verify — the HTTP gates could not run',
      }));
    }
  }

  // ============================ GATE 3: malformed input -> controlled failure ============================
  {
    const mkNamedRecord = ({ region }) => {
      // minimal named material record: [size][dim=16][unk=1][bps=2][id][res]
      // [name] (56 B pre-mask, size at offset 0) + mask region; the record
      // consumes [0, 4+size) with size = 52 + region.length (stride size+4)
      const size = 52 + region.length;
      const buf = Buffer.alloc(4 + size);
      const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
      dv.setUint32(0, size, true);
      dv.setUint32(4, 16, true);   // dim
      dv.setUint32(8, 1, true);   // unk
      dv.setUint32(12, 2, true);  // bps
      dv.setUint32(16, 12345, true); // id
      dv.setUint32(20, 0, true);  // res
      buf.write('Stone04\0', 24, 'latin1');
      region.copy(buf, 56);
      return new Uint8Array(buf);
    };
    const goodRaw = Buffer.alloc(256, 137); // RAW 256B — decodes
    const rleOverrun = Buffer.from([255, 5, 2, 3, 1, 1]); // counts sum > 256 (dim=16)
    const oddRegion = Buffer.from([3, 7, 5]);
    const cases = [];
    // (a) named record with an RLE-overrun region -> LOUD failure
    let threw = null;
    try { decodeMaterialTail(mkNamedRecord({ region: rleOverrun })); } catch (e) { threw = String(e.message); }
    cases.push({ case: 'rle_overrun_named_record', threw: threw !== null, message: threw });
    // (b) named record with an odd-length region -> LOUD failure
    threw = null;
    try { decodeMaterialTail(mkNamedRecord({ region: oddRegion })); } catch (e) { threw = String(e.message); }
    cases.push({ case: 'odd_region_named_record', threw: threw !== null, message: threw });
    // (c) implausible size field -> LOUD failure
    threw = null;
    const bogus = Buffer.alloc(64); bogus.writeUInt32LE(0xfffffff0, 0); bogus.writeUInt32LE(16, 4);
    try { decodeMaterialTail(new Uint8Array(bogus)); } catch (e) { threw = String(e.message); }
    cases.push({ case: 'implausible_size', threw: threw !== null, message: threw });
    // (d) residual bytes (< 4) at the tail end -> LOUD failure
    threw = null;
    try { decodeMaterialTail(new Uint8Array([1, 2, 3])); } catch (e) { threw = String(e.message); }
    cases.push({ case: 'residual_bytes', threw: threw !== null, message: threw });
    // (e) the CLEAN control: the same builder with a good RAW region decodes
    let cleanOk = false;
    try {
      const t = decodeMaterialTail(mkNamedRecord({ region: goodRaw }));
      cleanOk = t.namedMaterials.length === 1 && t.namedMaterials[0].maskEncoding === 'raw'
        && t.namedMaterials[0].mask[0] === 137;
    } catch { cleanOk = false; }
    // TGA malformed negatives (the strict subset — loud, no fallback)
    const tgaCases = [];
    const pattern = syntheticPatternTga2();
    let tgaClean = null; try { tgaClean = decodeTga2(pattern); } catch { tgaClean = null; }
    const bpp32 = syntheticPatternTga2({ bpp: 32 });
    threw = null; try { decodeTga2(bpp32); } catch (e) { threw = String(e.message); }
    tgaCases.push({ case: 'tga_32bpp_out_of_subset', threw: threw !== null, message: threw });
    const noFooter = Buffer.from(pattern); noFooter.fill(0, noFooter.length - 18, noFooter.length - 4);
    threw = null; try { decodeTga2(new Uint8Array(noFooter)); } catch (e) { threw = String(e.message); }
    tgaCases.push({ case: 'tga_footer_missing', threw: threw !== null, message: threw });
    threw = null; try { decodeTga2(pattern.subarray(0, 40)); } catch (e) { threw = String(e.message); }
    tgaCases.push({ case: 'tga_truncated', threw: threw !== null, message: threw });
    const malformedOk = cases.every((c) => c.threw) && cleanOk && tgaCases.every((c) => c.threw) && tgaClean !== null;
    records.push(rec('WORLD_MAT_MALFORMED_CONTROLLED',
      'malformed material tails and out-of-subset TGA payloads FAIL LOUDLY through the production decoders (no mask, no rgba, no fallback)',
      malformedOk ? 'PASS' : 'FAIL', {
        measuredQuantity: 'thrown vs decoded on synthetic malformed inputs + the clean controls',
        measured: { tailCases: cases, cleanNamedRecordDecodes: cleanOk, tgaCases, cleanPatternDecodes: tgaClean !== null },
        resultClass: 'SYNTHETIC_MALFORMED_NEGATIVE_CONTROL (through the production decoders)',
        failureCaseDetected: malformedOk ? 'none — every malformed case threw, every clean case decoded' : 'a malformed input was accepted or a clean input failed',
      }));
  }

  // ============================ GATE 6: unresolved-binding diagnostic (synthetic) ============================
  {
    const atobFn = (s) => Buffer.from(s, 'base64').toString('binary');
    const mkTile = (mats) => ({ ok: true, materials: mats });
    const mkMat = (id, name, resolved, weight) => ({
      position: 0, id, name, dim: 16, bps: 2, maskEncoding: 'raw',
      maskBase64: Buffer.from(new Uint8Array(256).fill(weight)).toString('base64'),
      texture: resolved
        ? { resolved: true, entryName: `${id}.dat`, size: 196652, offset: 1 }
        : { resolved: false, entryName: `${id}.dat`, reason: 'SYNTHETIC missing relation (no <id>.dat entry) — diagnostic' },
    });
    const good = Array.from({ length: 8 }, () => Array.from({ length: 8 }, () => mkTile([mkMat(13382, 'Stone04', true, 255), mkMat(20281, 'Grass01', true, 128)])));
    const oneUnresolved = good.map((row, y) => row.map((tile, x) => (y === 0 && x === 0
      ? mkTile([mkMat(13382, 'Stone04', true, 255), mkMat(999999, 'GhostMat', false, 200), mkMat(20281, 'Grass01', true, 128)])
      : tile)));
    const dGood = buildRegionSplatData(good, { atobFn });
    const dBad = buildRegionSplatData(oneUnresolved, { atobFn });
    const unresolvedListed = dBad.unresolved.some((u) => u.id === 999999);
    const noSlotForUnresolved = !dBad.slotById.has(999999) && !dBad.textureIds.includes(999999);
    const resolvedStillApplied = dBad.appliedLayers > 0 && dBad.textureIds.includes(13382) && dBad.textureIds.includes(20281);
    const diagMode = dBad.diagnostic.mode !== 'NONE' && dBad.diagnostic.unresolvedCount >= 1;
    const goodOk = dGood.ok === true && dGood.diagnostic.mode === 'NONE' && dGood.unresolved.length === 0;
    // the DECODE-FAILURE variant: a texture that resolves in the index but
    // fails the strict decode subset in the browser — the app marks those ids
    // unresolved and rebuilds; the SAME pure path proves the skip:
    const decodeFailed = good.map((row, y) => row.map((tile, x) => (y === 4 && x === 4
      ? mkTile([mkMat(13382, 'Stone04', true, 255), mkMat(424242, 'BadTga', false, 240)])
      : tile)));
    const dDecode = buildRegionSplatData(decodeFailed, { atobFn });
    const decodeFailSkipped = !dDecode.slotById.has(424242) && dDecode.unresolved.some((u) => u.id === 424242);
    const gateOk = unresolvedListed && noSlotForUnresolved && resolvedStillApplied && diagMode && goodOk && decodeFailSkipped;
    records.push(rec('WORLD_MAT_UNRESOLVED_BINDING',
      'synthetic unresolved material->texture bindings: layers SKIPPED + listed (explicit diagnostic), no texture slot, resolved layers still applied; all-resolved grid has NO diagnostic',
      gateOk ? 'PASS' : 'FAIL', {
        measuredQuantity: 'builder diagnostics on synthetic grids (pure production module)',
        measured: {
          unresolvedListed, noSlotForUnresolved, resolvedStillApplied, diagMode,
          allResolvedGridClean: goodOk, decodeFailureSkipped: decodeFailSkipped,
          unresolvedSample: dBad.unresolved, badGridCensus: {
            layersTotal: dBad.layersTotal, resolvedLayers: dBad.resolvedLayers, appliedLayers: dBad.appliedLayers,
          },
        },
        resultClass: 'SYNTHETIC_MISSING_RELATION_CONTROL (through the REAL pure builder — never a random green texture)',
        failureCaseDetected: gateOk ? 'none' : 'an unresolved binding leaked into a texture slot, or a resolved layer was dropped',
      }));
  }

  // ============================ GATE 7: UV/flip control (pattern + real) ============================
  {
    const pattern = syntheticPatternTga2({ width: 4, height: 4, bpp: 24 });
    const decoded = decodeTga2(pattern); // IMAGE order: row 0 = visual TOP = the LAST stored row
    // stored row r has B=r*40+10 (B slot) => in RGBA, R = 90+r*20 (stored BGR -> R slot = stored R = 90+r*20)
    const rowOf = (rgba, y) => [rgba[(y * 4) * 4], rgba[(y * 4) * 4 + 1], rgba[(y * 4) * 4 + 2]];
    const imageRow0 = rowOf(decoded.rgba, 0);
    const expectedImageRow0 = [90 + 3 * 20, 250 - 3 * 30, 3 * 40 + 10].map((v) => v & 0xff); // LAST stored row (r=3)
    const imageOrderOk = imageRow0[0] === expectedImageRow0[0] && imageRow0[1] === expectedImageRow0[1] && imageRow0[2] === expectedImageRow0[2];
    // the A32 FILE-ORDER sibling on a 32bpp pattern: row 0 = the FIRST stored row (DIFFERENT convention)
    const pattern32 = syntheticPatternTga2({ width: 4, height: 4, bpp: 32 });
    const decoded32File = decodeTga2A32(pattern32);
    const fileRow0 = rowOf(decoded32File.rgba, 0);
    const expectedFileRow0 = [90 + 0 * 20, 250 - 0 * 30, 0 * 40 + 10].map((v) => v & 0xff); // FIRST stored row (r=0)
    const fileOrderOk = fileRow0[0] === expectedFileRow0[0] && fileRow0[1] === expectedFileRow0[1] && fileRow0[2] === expectedFileRow0[2];
    const conventionsDistinguished = imageOrderOk && fileOrderOk && (imageRow0[0] !== fileRow0[0] || imageRow0[2] !== fileRow0[2]);
    // the documented GPU sampling convention on the pattern
    const uv00 = sampleTexelImageOrder(decoded.rgba, 4, 4, 0, 0);
    const uv11 = sampleTexelImageOrder(decoded.rgba, 4, 4, 0.999, 0.999);
    const uvConsistent = uv00[0] === imageRow0[0] && uv11[0] === rowOf(decoded.rgba, 3)[0];
    // the REAL texture: Stone04 payload through the same convention
    const indepIndex = independentTextureIndex(texturesPath);
    const stoneEntry = indepIndex.byId.get(13382);
    const stonePayload = independentReadTexturePayload(texturesPath, stoneEntry);
    const stoneDec = decodeTga2(stonePayload);
    const s00 = sampleTexelImageOrder(stoneDec.rgba, 256, 256, 0, 0);
    const sTL = [stoneDec.rgba[0], stoneDec.rgba[1], stoneDec.rgba[2]];
    const sBR = sampleTexelImageOrder(stoneDec.rgba, 256, 256, 0.999, 0.999);
    const sBRExpected = [stoneDec.rgba[255 * 256 * 4 + 255 * 4], stoneDec.rgba[255 * 256 * 4 + 255 * 4 + 1], stoneDec.rgba[255 * 256 * 4 + 255 * 4 + 2]];
    const realOk = s00[0] === sTL[0] && s00[1] === sTL[1] && s00[2] === sTL[2]
      && sBR[0] === sBRExpected[0] && sBR[1] === sBRExpected[1] && sBR[2] === sBRExpected[2];
    // the world-uv formula (u along +X, v along +Z/south; global, repeat in meters)
    const [u, v] = worldUV(64, 128, 32);
    const worldUvOk = Math.abs(u - 2) < 1e-12 && Math.abs(v - 4) < 1e-12;
    const gateOk = imageOrderOk && fileOrderOk && conventionsDistinguished && uvConsistent && realOk && worldUvOk;
    records.push(rec('WORLD_MAT_UV_FLIP_CONTROL',
      'UV/flip controlled with a PATTERN and a REAL texture: decodeTga2 IMAGE order (row 0 = visual top) distinguished from the A32 FILE-row convention; the documented GPU sampling (flipY=false, v=0 -> top) consistent on both; the world-uv formula recorded',
      gateOk ? 'PASS' : 'FAIL', {
        measuredQuantity: 'texel values through the decoder + the documented sampling convention',
        measured: {
          patternImageRow0: imageRow0, patternFileRow0A32: fileRow0,
          conventionsDistinguished, gpuSamplingConsistent: uvConsistent,
          realTexture: { id: 13382, topLeft: s00, bottomRight: sBR, expected: { tl: sTL, br: sBRExpected }, consistent: realOk },
          worldUv: { input: [64, 128, 32], output: [u, v], ok: worldUvOk },
          preset: { rowOrder: RENDER_RECONSTRUCTION_PRESET.rowOrder, uv: RENDER_RECONSTRUCTION_PRESET.uv, colorSpace: RENDER_RECONSTRUCTION_PRESET.colorSpace },
        },
        independentSourceOfTruth: 'the synthetic pattern payload (distinct per-row colors, built in-test) + the real Stone04 payload read independently',
        whyNonCircular: 'the expected row/texel values come from the constructed storage order, not from the decoder output',
        failureCaseDetected: gateOk ? 'none' : 'the row-order/sampling convention did not behave as documented',
      }));
  }

  return records;
}
