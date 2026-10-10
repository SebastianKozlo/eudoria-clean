// qc_independent_recheck.mjs — PE_WORLD_LAUNCHER_R1_20261010 — FRESH INTERNAL QC (pe-master-auditor)
// MY OWN independent byte-level re-verification. This file is QC code, NOT product code.
// INDEPENDENCE STATEMENT: the terrain/material/texture/vcl byte reads below are
// freshly written for this QC (own footer/dir walkers, own inflate use, own RLE
// expansion, own TSV tokenization) — they import ZERO production modules.
// The ONLY production import is src/peworld/PEFoliageLabSeed.js for the
// determinism/cap checks (the dispatch REQUIRES running the production
// generateTileInstances; that is the code under test, not the reader).
// All HTTP checks go against the STANDING run server 127.0.0.1:8162 (final code).
import { open } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import zlib from 'node:zlib';
import { generateTileInstances } from '../../../../src/peworld/PEFoliageLabSeed.js';

const OUT = [];
function log(s) { OUT.push(s); console.log(s); }
const sha256 = (b) => createHash('sha256').update(b).digest('hex');
const BASE = 'http://127.0.0.1:8162';
const result = { qcOrigin: 'FRESH_INTERNAL_REVIEW', sections: {} };

async function httpGet(pathname) {
  const res = await fetch(BASE + pathname);
  const ab = await res.arrayBuffer();
  return { status: res.status, headers: Object.fromEntries(res.headers), bytes: new Uint8Array(ab) };
}

// ---------- my own bounded BNT2 index reader (generic BNT2: RAW payloads) ----------
async function bnt2Index(filePath) {
  const fh = await open(filePath, 'r');
  const stat = await fh.stat();
  const tail = Buffer.alloc(8);
  await fh.read(tail, 0, 8, stat.size - 8);
  const magic = tail.toString('latin1', 4, 8);
  if (magic !== 'BNT2') throw new Error(`footer magic ${magic} != BNT2 (${filePath})`);
  const dirOffset = tail.readUInt32LE(0);
  const dirLen = stat.size - 8 - dirOffset;
  const dir = Buffer.alloc(dirLen);
  await fh.read(dir, 0, dirLen, dirOffset);
  const count = dir.readUInt32LE(0);
  const entries = new Map();
  let p = 4;
  for (let i = 0; i < count; i++) {
    const nul = dir.indexOf(0x0a, p);
    if (nul < 0) throw new Error(`entry ${i} unterminated`);
    const name = dir.toString('latin1', p, nul);
    p = nul + 1;
    const size = dir.readUInt32LE(p);
    const offset = dir.readUInt32LE(p + 4);
    p += 16;
    entries.set(name, { size, offset });
  }
  if (p !== dirLen) throw new Error(`dir walk end ${p} != ${dirLen}`);
  return { fh, size: stat.size, count, entries };
}
async function readRawAt(fh, offset, size) {
  const buf = Buffer.alloc(size);
  await fh.read(buf, 0, size, offset);
  return new Uint8Array(buf);
}

// ---------- my own terrain record reader (BNT2_TERRAIN: 8B header + zlib) ----------
async function readTerrainPayload(tFh, ent) {
  const head = await readRawAt(tFh, ent.offset, 8);
  if (!(head[0] === 0x02 && head[1] === 0x00 && head[2] === 0x00 && head[3] === 0xff)) {
    throw new Error(`bad record marker at ${ent.offset}`);
  }
  const decSize = head[4] | (head[5] << 8) | (head[6] << 16) | (head[7] << 24);
  const stream = await readRawAt(tFh, ent.offset + 8, ent.size - 8);
  const payload = new Uint8Array(zlib.inflateSync(Buffer.from(stream)));
  if (payload.byteLength !== decSize) throw new Error(`inflate ${payload.byteLength} != header ${decSize}`);
  return payload;
}
const u16 = (p, o) => p[o] | (p[o + 1] << 8);

async function sectionTerrain() {
  const T = 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Terrain\\terrain.bnt';
  const idx = await bnt2Index(T);
  log(`[T] my dir walk: count=${idx.count} (expected 58451)`);
  const names = [...idx.entries.keys()];
  const regular = names.filter((n) => /^([0-9a-f]{8})\.tdf$/.test(n));
  log(`[T] regular-named entries: ${regular.length} (expected 51920)`);
  // pick: spawn tile + a middle tile + the far corner tile
  const picks = ['00350072.tdf', regular[30000], '00db00eb.tdf'];
  const per = [];
  for (const name of picks) {
    const ent = idx.entries.get(name);
    const payload = await readTerrainPayload(idx.fh, ent);
    const heights = [];
    for (let i = 0; i < 1024; i++) heights.push(u16(payload, 64 + i * 2));
    const sub52 = [];
    for (let i = 0; i < 6; i++) sub52.push(u16(payload, 52 + i * 2));
    const gx = parseInt(name.slice(0, 4), 16), gy = parseInt(name.slice(4, 8), 16);
    const wire = await httpGet(`/api/world/tile/${gx}/${gy}`);
    const wireHeights = [];
    const wb = wire.bytes;
    for (let i = 0; i < 1024; i++) wireHeights.push(wb[i * 2] | (wb[i * 2 + 1] << 8));
    const bitExact = wire.status === 200 && wire.bytes.byteLength === 2048
      && heights.every((v, i) => v === wireHeights[i]);
    const min = Math.min(...heights), max = Math.max(...heights);
    let mean = 0; for (const v of heights) mean += v; mean = Math.round(mean / 1024);
    per.push({
      name, gx, gy, payloadBytes: payload.byteLength,
      dataSize: payload[8] | (payload[9] << 8) | (payload[10] << 16) | (payload[11] << 24),
      tileDim: payload[12] | (payload[13] << 8) | (payload[14] << 16) | (payload[15] << 24),
      myMin: min, myMax: max, myMean: mean,
      wireStatus: wire.status, wireBitExactVsMyRead: bitExact,
      offset52First6: sub52, offset64First6: heights.slice(0, 6),
      offset52Discriminates: sub52.some((v, i) => v !== heights[i]),
      heightsSha256: sha256(new Uint8Array(new Uint16Array(heights).buffer ? new Uint8Array(new Uint16Array(heights).buffer) : new Uint8Array(0))),
    });
    log(`[T] ${name} (${gx},${gy}): wire=${wire.status} bitExact=${bitExact} min=${min} max=${max} mean=${mean} 52discrim=${per[per.length - 1].offset52Discriminates}`);
  }
  result.sections.terrain = { dirCount: idx.count, regularCount: regular.length, tiles: per };
  await idx.fh.close();
}

// ---------- my own material tail walker ----------
function myRleExpand(region, dim) {
  const target = dim * dim;
  const mask = new Uint8Array(target);
  let wp = 0, rp = 0;
  while (rp + 1 < region.length) {
    const c = region[rp], v = region[rp + 1]; rp += 2;
    if (wp + c > target) return null;
    mask.fill(v, wp, wp + c); wp += c;
  }
  return wp === target ? mask : null;
}
function myTailWalk(tail) {
  const recs = [];
  const rd = (o) => tail[o] | (tail[o + 1] << 8) | (tail[o + 2] << 16) | (tail[o + 3] << 24);
  let p = 0;
  while (p + 4 <= tail.byteLength) {
    const size = rd(p);
    if (size < 8 || p + 4 + size > tail.byteLength) throw new Error(`implausible size ${size} at tail+${p}`);
    const dim = rd(p + 4);
    const id = rd(p + 16);
    let name = '';
    for (let i = 0; i < 28 && tail[p + 24 + i] !== 0; i++) name += String.fromCharCode(tail[p + 24 + i]);
    const maskStart = p + 56, maskEnd = p + 4 + size;
    const region = tail.subarray(maskStart, maskEnd);
    let mask = null, enc = null;
    if (region.length === dim * dim) { mask = new Uint8Array(region); enc = 'raw'; }
    else { mask = myRleExpand(region, dim); enc = mask ? 'rle' : null; }
    const named = dim === 16 && name.length > 0 && /^[\x20-\x7e]+$/.test(name);
    if (named && mask === null) throw new Error(`named record ${name} region not RAW/RLE (len ${region.length})`);
    recs.push({
      tailOffset: p, size, dim, id, name, named,
      enc: named ? enc : `system_${dim}`,
      mask, extra4: Array.from(tail.subarray(p + 52, p + 56)),
      wrong52RegionLen: (p + 4 + size) - (p + 52),
    });
    p = maskEnd;
  }
  if (p !== tail.byteLength) throw new Error(`tail not exactly consumed: ${p} != ${tail.byteLength}`);
  return recs;
}

async function sectionMaterials() {
  const T = 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Terrain\\terrain.bnt';
  const idx = await bnt2Index(T);
  const per = [];
  for (const [gx, gy] of [[53, 114], [50, 111]]) {
    const name = `${gx.toString(16).padStart(4, '0')}${gy.toString(16).padStart(4, '0')}.tdf`;
    const payload = await readTerrainPayload(idx.fh, idx.entries.get(name));
    const tail = payload.subarray(2112);
    const recs = myTailWalk(tail);
    const named = recs.filter((r) => r.named);
    // server materials JSON
    const res = await fetch(`${BASE}/api/world/tile/${gx}/${gy}/materials`);
    const mat = await res.json();
    const served = mat.tile?.materials ?? mat.materials ?? [];
    let allBitExact = true;
    const cmp = [];
    for (const m of served) {
      const mine = named.find((r) => r.id === m.id && r.name === m.name);
      const servedMask = m.maskBase64 ? new Uint8Array(Buffer.from(m.maskBase64, 'base64'))
        : (m.mask ? new Uint8Array(m.mask) : null);
      let bitExact = false;
      if (mine && servedMask && servedMask.length === mine.mask.length) {
        bitExact = Array.from(servedMask).every((v, i) => v === mine.mask[i]);
      }
      if (mine && !bitExact) allBitExact = false;
      if (mine) cmp.push({ id: m.id, name: m.name, myEnc: mine.enc, servedEnc: m.maskEncoding, bitExact, extra4: mine.extra4, wrong52RegionLen: mine.wrong52RegionLen });
    }
    const rawRecords = cmp.filter((c) => c.myEnc === 'raw');
    const rle52Degenerate = cmp.filter((c) => c.myEnc === 'rle' && c.extra4.every((v) => v === 0)).length;
    per.push({
      tile: name, myNamedCount: named.length, servedNamedCount: served.length,
      allServedBitExactVsMyWalk: allBitExact,
      perRecord: cmp,
      rawRecordsWrong52RegionLen260: rawRecords.filter((c) => c.wrong52RegionLen === 260).length,
      rawRecords: rawRecords.length,
      rleRecordsWithZeroExtra4: rle52Degenerate,
    });
    log(`[M] ${name}: myNamed=${named.length} served=${served.length} bitExact=${allBitExact} raw=${rawRecords.length} (wrong52 region len 260 on ${per[per.length - 1].rawRecordsWrong52RegionLen260})`);
  }
  result.sections.materials = { tiles: per };
  await idx.fh.close();
}

// ---------- texture chain: my own lazy Textures.bnt reads ----------
async function sectionTextureChain() {
  const X = 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Textures\\Textures.bnt';
  const idx = await bnt2Index(X);
  log(`[X] my Textures.bnt dir walk: count=${idx.count} (expected 8381)`);
  const per = [];
  for (const id of [13382, 457490]) {
    const ent = idx.entries.get(`${id}.dat`);
    if (!ent) throw new Error(`${id}.dat not in my index`);
    const myBytes = await readRawAt(idx.fh, ent.offset, ent.size);
    const wire = await httpGet(`/api/world/texture/${id}`);
    const bitExact = wire.status === 200 && wire.bytes.byteLength === myBytes.byteLength
      && Array.from(wire.bytes).every((v, i) => v === myBytes[i]);
    const tgaBpp = myBytes[16];
    per.push({
      id, entryName: `${id}.dat`, mySize: ent.size, wireStatus: wire.status,
      wireBytes: wire.bytes.byteLength, bitExact,
      mySha256: sha256(myBytes), tgaHeaderBpp: tgaBpp,
    });
    log(`[X] ${id}.dat: my=${ent.size}B wire=${wire.status}/${wire.bytes.byteLength}B bitExact=${bitExact} sha=${sha256(myBytes).slice(0, 16)}…`);
  }
  // wrong-era refusals through the REAL route
  const eras = {};
  for (const era of ['CD_2003', 'CD_JAN_2003', 'JUL_2003']) {
    const r = await httpGet(`/api/world/texture/13382?era=${era}`);
    eras[era] = { status: r.status, error: r.bytes.byteLength < 400 ? Buffer.from(r.bytes).toString('utf8').slice(0, 120) : null };
  }
  const mEra = await fetch(`${BASE}/api/world/tile/53/114/materials?era=CD_2003`);
  eras.materialsRouteCD2003 = { status: mEra.status };
  result.sections.textureChain = { indexCount: idx.count, entries: per, eraRefusals: eras };
  await idx.fh.close();
}

// ---------- vegetation: my own .vcl reads + production determinism ----------
async function sectionVegetation() {
  const V = 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\VegetationClimates\\VegetationClimates.bnt';
  const idx = await bnt2Index(V);
  log(`[V] my VegetationClimates.bnt dir walk: count=${idx.count}`);
  const v25 = await readRawAt(idx.fh, idx.entries.get('25.vcl').offset, idx.entries.get('25.vcl').size);
  const text25 = Buffer.from(v25).toString('latin1');
  const tokens25 = text25.split(/\s+/).filter((t) => t.length > 0);
  const badIdx = [];
  tokens25.forEach((t, i) => { if (!Number.isFinite(Number(t))) badIdx.push({ tokenIndex: i, token: t, record: Math.floor(i / 12), col: i % 12 }); });
  log(`[V] 25.vcl: ${tokens25.length} whitespace tokens; non-numeric: ${badIdx.length}; first=${JSON.stringify(badIdx[0])}`);

  // profile 0 + 1 payloads (my own decode)
  const decodeMyVcl = async (name) => {
    const e = idx.entries.get(name);
    const payload = await readRawAt(idx.fh, e.offset, e.size);
    const text = Buffer.from(payload).toString('latin1');
    const toks = text.split(/\s+/).filter((t) => t.length > 0);
    if (toks.length % 12 !== 0) throw new Error(`${name}: ${toks.length} tokens not multiple of 12`);
    const recs = [];
    for (let i = 0; i < toks.length; i += 12) recs.push(toks.slice(i, i + 12).map(Number));
    return { recs, tokens: toks.length };
  };
  const p0 = await decodeMyVcl('0.vcl');
  const p1 = await decodeMyVcl('1.vcl');
  log(`[V] 0.vcl: ${p0.recs.length} records (my decode); 1.vcl: ${p1.recs.length} records`);

  // cross-check with the API
  const api0 = await (await fetch(`${BASE}/api/world/climate/0`)).json();
  const api25 = await (await fetch(`${BASE}/api/world/climate/25`)).json();
  const apiRecordsMatch = api0.records && p0.recs.length === api0.records.length
    && api0.records.every((r, i) => r.every((v, c) => v === p0.recs[i][c]));
  log(`[V] API climate/0 records == my decode: ${apiRecordsMatch} (apiRecordCount=${api0.records?.length}); witness 457485 in profile 0: ${p0.recs.some((r) => r[0] === 457485)}`);
  log(`[V] API climate/25: status=${api25.status} records=${api25.records} error=${JSON.stringify((api25.error ?? '').slice(0, 60))}`);

  // determinism — MY OWN canonical serialization + the PRODUCTION generator
  // (fields per the REAL instance shape: key/modelId/u16/world/scale)
  const f32bits = (v) => {
    const b = new ArrayBuffer(4); new DataView(b).setFloat32(0, v);
    return new DataView(b).getUint32(0).toString(16).padStart(8, '0');
  };
  const canon = (insts) => {
    const lines = insts.map((i) => `${i.key}|${i.modelId}|${i.u16.x},${i.u16.y}|${i.world.x},${i.world.y}|${f32bits(i.scale)}|${f32bits(i.samplerValue)}|${i.rngState0}`);
    lines.sort();
    return lines.join('\n');
  };
  let sample = null;
  const gen = (records, labSeed, gx, gy, densityPercent) => {
    const out = generateTileInstances({
      records, labSeed, gx, gy, level: 1, viewBand: 10, p3: 0,
      densityPercent, tileWorldMeters: 64, u16PerWorldMeter: 2.0,
    });
    return out;
  };
  const first = gen(p0.recs, 0, 53, 114, 50);
  sample = first.instances.slice(0, 2);
  const again = gen(p0.recs, 0, 53, 114, 50);
  const diffSeed = gen(p0.recs, 1, 53, 114, 50);
  const h1 = sha256(Buffer.from(canon(first.instances), 'utf8'));
  const h2 = sha256(Buffer.from(canon(again.instances), 'utf8'));
  const h3 = sha256(Buffer.from(canon(diffSeed.instances), 'utf8'));
  const positionsDiffer = first.instances.some((i, ix) => {
    const j = diffSeed.instances[ix];
    return !j || i.u16.x !== j.u16.x || i.u16.y !== j.u16.y;
  });
  log(`[V] determinism: sameSeed repeat identical=${h1 === h2} (${h1.slice(0, 16)}…); diffSeed different=${h1 !== h3} (${h3.slice(0, 16)}…); positionsDiffer=${positionsDiffer}; count=${first.instances.length}`);

  // cap case: profile 1 @100% over the 8x8 window at origin 50,111
  let requested = 0;
  const perTile = [];
  for (let gx = 50; gx <= 57; gx++) for (let gy = 111; gy <= 118; gy++) {
    const t = gen(p1.recs, 0, gx, gy, 100);
    requested += t.instances.length;
    perTile.push(t.instances.length);
  }
  const rendered = Math.min(requested, 5000);
  const limited = requested - rendered;
  const all96 = perTile.every((c) => c === 96) ? 'ALL_96' : 'MIXED';
  log(`[V] cap case (profile 1 @100%, window 50..57 x 111..118): requested=${requested} rendered=${rendered} limited=${limited} perTile=${all96}`);

  // model chain: 457485 wire vs MY physical read
  const M = 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt';
  const midx = await bnt2Index(M);
  log(`[V] my Models.bnt dir walk: count=${midx.count} (expected 5596)`);
  const ent = midx.entries.get('457485.nif');
  const myBytes = await readRawAt(midx.fh, ent.offset, ent.size);
  const wire = await httpGet('/api/world/model/457485');
  const bitExact = wire.status === 200 && wire.bytes.byteLength === myBytes.byteLength
    && Array.from(wire.bytes).every((v, i) => v === myBytes[i]);
  log(`[V] model 457485: my=${myBytes.byteLength}B wire=${wire.status}/${wire.bytes.byteLength}B bitExact=${bitExact} sha=${sha256(myBytes)}`);
  const missing = await fetch(`${BASE}/api/world/model/999999`);
  log(`[V] model 999999: status=${missing.status} (expect 404)`);

  // status vegetation section
  const st = await (await fetch(`${BASE}/api/world/status`)).json();
  const veg = st.vegetation ?? {};
  result.sections.vegetation = {
    vcl25: {
      tokenCount: tokens25.length, nonNumericTokens: badIdx.slice(0, 8),
      firstBad: badIdx[0] ?? null,
      apiStatus: api25.status, apiRecordsNull: api25.records === null,
    },
    profile0: { myRecordCount: p0.recs.length, apiRecordsMatch, witness457485Present: p0.recs.some((r) => r[0] === 457485) },
    determinism: {
      sameSeedRepeatIdentical: h1 === h2, hashSameSeed: h1,
      diffSeedDifferent: h1 !== h3, hashDiffSeed: h3, positionsDiffer,
      instanceCount: first.instances.length, sampleInstance: sample,
    },
    cap: { requested, rendered, limited, cap: 5000, perTilePattern: all96 },
    modelChain: {
      wireBitExactVsMyRead: bitExact, servedBytes: wire.bytes.byteLength,
      myBytes: myBytes.byteLength, sha256: sha256(myBytes),
      missing999999: missing.status,
    },
    statusSection: {
      mode: veg.mode, defaultProfile: veg.defaultProfileIndex,
      supportCounts: veg.supportCounts, p3: veg.p3, cap: veg.cap,
    },
  };
  await idx.fh.close(); await midx.fh.close();
}

await sectionTerrain();
await sectionMaterials();
await sectionTextureChain();
await sectionVegetation();
const { writeFile, mkdir } = await import('node:fs/promises');
await mkdir(new URL('.', import.meta.url), { recursive: true });
await writeFile(new URL('./raw/QC_INDEPENDENT_RECHECK.json', import.meta.url), JSON.stringify(result, null, 1), 'utf8');
log('[QC] done — raw/QC_INDEPENDENT_RECHECK.json written');
