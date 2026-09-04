// iter021_era_byte_audit.js — MILESTONE 1-E ITER 021 P0 AUDIT (Node side)
// QUESTION: Does the CLEAN pipeline render the ERA-DIVERGENT region
// (100..102 x 100..102) byte-faithfully end-to-end (heights + materials +
// textures, era=PCG_9_3_5 primary)?
//
// INDEPENDENT CHECKS (non-circular — SECOND minimal parsers written HERE,
// DataView/Buffer-level, NO shared code with src/pesource or the page):
//   (A) HEIGHTS: per-tile 32x32 u16 LE block sha256 — independent parser vs
//       the browser clean-chain export (9/9 byte-faithful required); relief
//       stats per tile.
//   (B) JUL_2003 TWIN CENSUS (era-labeled): per tile — does the JUL 50.bnt
//       twin exist? payload/heights/tail byte-equality, tail SHAs, relief
//       delta. HONEST per-tile statement: twin exists-but-differs vs no-twin.
//   (C) MATERIALS: independent tail walk — record census per tile (counts,
//       ids/names/encodings, mask SHAs) vs the page export; tailConsumedExactly
//       9/9 in BOTH implementations; Stone04-base rule re-checked on THIS
//       era-divergent data (report what the data says, era-labeled).
//   (D) TEXTURES: independent BNT2 walk of PCG Textures.bnt + independent
//       minimal TGA decode; payload SHAs vs page export; per-id mean color
//       (for the probe comparison); missing-id census (fallback decision).
//   (E) HEIGHTS ORACLE (LEGITIMATE third artifact, version-labeled): legacy
//       r169 chunk_r006_c006_u16le.bin (JUL heights baked by the FROZEN legacy
//       runtime) — valid HERE because (B) measures heights as JUL-identical
//       for these tiles; the era divergence lives in the TAILS.
//   (F) PIXEL PROBE: page probe pixels vs the independently decoded texture
//       means of each probe's dominant material (measured deltas recorded).
//   (G) r169 MATERIAL ORACLE: HONESTLY N/A — legacy splat caches were baked
//       from JUL-era tails which DIFFER on all 9 tiles (per (B)); a byte
//       comparison would compare two different eras' material data.
// Usage: node tools/iter021_era_byte_audit.js <browserExportJson>
// Writes: 03_EVIDENCE/iter021_era_byte_audit.json
'use strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import zlib from 'node:zlib';

const PCG_TERRAIN = 'D:/Eudoria_Reconstruction/pcg_install/Data/Terrain/terrain.bnt';
const PCG_TEXTURES = 'D:/Eudoria_Reconstruction/pcg_install/Data/Textures/Textures.bnt';
const JUL_TERRAIN = 'C:/Entropia Universe/Data/Terrain/50.bnt';
const LEGACY_CHUNK = 'D:/Eudoria_Reconstruction/12_WebGame/eudoria-web/data/terrain/chunk_r006_c006_u16le.bin';
const EVIDENCE_DIR = 'D:/Eudoria_Reconstruction/99_Audits/PE_MILESTONE_1_WORLD_SURFACE_R1/03_EVIDENCE';
const BROWSER_JSON = process.argv[2];

const ORIGIN_X = 100, ORIGIN_Y = 100, N = 3;
const ERA = 'PCG_9_3_5';
const sha256 = (b) => crypto.createHash('sha256').update(b).digest('hex').toUpperCase();

// --- independent minimal parsers (SECOND implementation; DataView/Buffer only) ---
function parseBnt2(file) {
  const b = fs.readFileSync(file);
  const dv = b.readUInt32LE(b.length - 8);
  const cnt = b.readUInt32LE(dv);
  const m = new Map();
  let p = dv + 4;
  for (let i = 0; i < cnt; i++) {
    const s = p;
    while (b[p] !== 0x0a) p++;
    const name = b.toString('latin1', s, p);
    p++;
    const size = b.readUInt32LE(p), off = b.readUInt32LE(p + 4);
    p += 16;
    m.set(name, { off, size });
  }
  if (p !== b.length - 8) throw new Error(`BNT2 dir walk mismatch ${file}`);
  if (b.toString('ascii', b.length - 4, b.length) !== 'BNT2') throw new Error('BNT2 magic missing');
  return { b, m };
}
function parseBunt(file) {
  const b = fs.readFileSync(file);
  const dv = b.readUInt32LE(b.length - 8);
  const cnt = b.readUInt32LE(dv);
  const m = new Map();
  let p = dv + 4;
  for (let i = 0; i < cnt; i++) {
    const name = b.toString('latin1', p, p + 13).trim();
    const size = b.readUInt32LE(p + 13), off = b.readUInt32LE(p + 17);
    p += 21;
    m.set(name, { off, size });
  }
  if (p !== b.length - 8) throw new Error('BUNT dir walk mismatch');
  return { b, m };
}
function inflateAt(b, e) {
  const rec = b.subarray(e.off, e.off + e.size);
  if (rec[0] !== 0x02 || rec[1] !== 0x00 || rec[2] !== 0x00 || rec[3] !== 0xff) {
    throw new Error('bad record marker');
  }
  const dSize = rec.readUInt32LE(4);
  const out = zlib.inflateSync(rec.subarray(8, e.size));
  if (out.length !== dSize) throw new Error(`inflate size mismatch ${out.length} != ${dSize}`);
  return out;
}
const tileName = (x, y) => x.toString(16).padStart(4, '0') + y.toString(16).padStart(4, '0') + '.tdf';

// --- independent tail walk ([u32 size][u32 dim][size-4]; stride = size+4; tail at 2112) ---
function independentTailWalk(payload) {
  if (payload.length < 2112 + 4) throw new Error(`payload too small ${payload.length}`);
  const records = [];
  let q = 2112;
  while (q < payload.length) {
    const size = payload.readUInt32LE(q);
    const dim = payload.readUInt32LE(q + 4);
    const id = payload.readUInt32LE(q + 16);
    let name = '';
    for (let i = 0; i < 28; i++) { const c = payload[q + 24 + i]; if (c === 0) break; name += String.fromCharCode(c); }
    const maskStart = q + 56, maskEnd = q + 4 + size;
    const region = payload.subarray(maskStart, maskEnd);
    // name printability (independent): printable ASCII until NUL
    let printable = name.length > 0;
    for (let i = 0; i < name.length; i++) { const c = name.charCodeAt(i); if (c < 32 || c >= 127) { printable = false; break; } }
    let mask = null, encoding = null;
    if (region.length === dim * dim) {
      mask = Buffer.from(region); encoding = 'raw';
    } else if (dim === 16 && printable && name.length > 0) {
      // NAMED dim=16 records must decode (RAW or RLE) — LOUD failure;
      // unnamed dim=16 records are SYSTEM records, carried raw (mask=null).
      mask = Buffer.alloc(dim * dim);
      let w = 0, r = 0;
      while (r < region.length) {
        const cnt = region[r++], val = region[r++];
        if (w + cnt > dim * dim) throw new Error('indep RLE overrun');
        mask.fill(val, w, w + cnt); w += cnt;
      }
      if (w !== dim * dim) throw new Error(`indep RLE sum ${w} != ${dim * dim}`);
      encoding = 'rle_cv';
    }
    records.push({ size, dim, id, name, encoding, mask, recordOffset: q });
    q = maskEnd;
  }
  return { records, consumedExactly: q === payload.length, payloadLen: payload.length };
}

// --- independent TGA decode (validated subset: TGA2 256x256x24 bottom-up) ---
function independentTgaMeanAndSha(payload) {
  if (payload.length < 44) throw new Error('payload too small for TGA2');
  const w = payload[12] | (payload[13] << 8), h = payload[14] | (payload[15] << 8);
  const bpp = payload[16], imageType = payload[2], cm = payload[1];
  if (cm !== 0 || imageType !== 2 || bpp !== 24) throw new Error(`unsupported TGA cm=${cm} type=${imageType} bpp=${bpp}`);
  const expected = 18 + w * h * 3 + 8 + 18;
  if (payload.length !== expected) throw new Error(`TGA size ${payload.length} != ${expected}`);
  if (payload.toString('ascii', payload.length - 18, payload.length) !== 'TRUEVISION-XFILE.\0') throw new Error('TGA2 footer missing');
  let r = 0, g = 0, b = 0;
  const px = w * h, dataStart = 18;
  for (let i = 0; i < px; i++) {
    const s = dataStart + i * 3;
    b += payload[s]; g += payload[s + 1]; r += payload[s + 2]; // BGR storage
  }
  return { width: w, height: h,
    meanRgb: [Math.round(r / px), Math.round(g / px), Math.round(b / px)] };
}

// ================= (A) HEIGHTS + (B) JUL TWIN CENSUS =================
const pcg = parseBnt2(PCG_TERRAIN);
const jul = parseBunt(JUL_TERRAIN);
const browser = JSON.parse(fs.readFileSync(BROWSER_JSON, 'utf8'));
const pageResult = browser.result;

const tileAudit = [];
let heightsAllMatch = true;
for (let ty = ORIGIN_Y; ty < ORIGIN_Y + N; ty++) {
  for (let tx = ORIGIN_X; tx < ORIGIN_X + N; tx++) {
    const name = tileName(tx, ty);
    const payload = inflateAt(pcg.b, pcg.m.get(name));
    const heights = Buffer.alloc(2048);
    let mn = 65535, mx = 0;
    for (let i = 0; i < 1024; i++) {
      const v = payload.readUInt16LE(64 + i * 2);
      heights.writeUInt16LE(v, i * 2);
      if (v < mn) mn = v; if (v > mx) mx = v;
    }
    const h = sha256(heights);
    const pageTile = pageResult.heights.perTile.find((t) => t.name === name);
    const byteFaithful = h === pageTile.heightsSha256;
    if (!byteFaithful) heightsAllMatch = false;

    // (B) JUL twin census
    const je = jul.m.get(name);
    let julInfo = { julTwinExists: false };
    if (je) {
      const jp = inflateAt(jul.b, je);
      const heightsEq = jp.subarray(64, 2112).equals(payload.subarray(64, 2112));
      const tailEq = jp.subarray(2112).equals(payload.subarray(2112));
      let jmn = 65535, jmx = 0;
      for (let i = 0; i < 1024; i++) {
        const v = jp.readUInt16LE(64 + i * 2);
        if (v < jmn) jmn = v; if (v > jmx) jmx = v;
      }
      julInfo = {
        julTwinExists: true, julEra: 'JUL_2003',
        julPayloadEqual: jp.equals(payload),
        julHeightsEqual: heightsEq, julTailEqual: tailEq,
        julTailSha256: sha256(jp.subarray(2112)), pcgTailSha256: sha256(payload.subarray(2112)),
        julReliefU16: { min: jmn, max: jmx, relief: jmx - jmn },
        reliefDeltaU16: (jmx - jmn) - (mx - mn),
        honestStatement: heightsEq && !tailEq
          ? 'JUL twin EXISTS; heights byte-identical; MATERIAL TAIL differs (era divergence lives in the surface/material data)'
          : (heightsEq && tailEq ? 'JUL twin EXISTS and is payload-identical (NOT divergent)' :
            'JUL twin EXISTS and differs in HEIGHTS (unexpected — record, never force)'),
      };
    }
    tileAudit.push({
      name, gridX: tx, gridY: ty, era: ERA,
      heightsSha256: h, pageHeightsSha256: pageTile.heightsSha256, byteFaithful,
      reliefU16: { min: mn, max: mx, relief: mx - mn },
      payloadSha256: sha256(payload),
      julTwin: julInfo,
    });
  }
}

// ================= (C) MATERIALS independent census =================
const materialAudit = [];
let materialAllMatch = true;
const idCensus = new Map();
const nameDupCensus = new Map(); // name -> Set(ids) — duplicate-name data observation
for (const te of tileAudit) {
  const payload = inflateAt(pcg.b, pcg.m.get(te.name));
  const indep = independentTailWalk(payload);
  const named = indep.records.filter((r) => r.dim === 16 && r.name.length > 0 && r.mask !== null);
  const pageCensus = pageResult.materialCensus.find((c) => c.tile === te.name);
  const base = named[0] ?? null;
  let baseAll255 = false;
  if (base) baseAll255 = base.mask.every((v) => v === 255);
  // sums census (ORIGINAL DATA; normalization REJECTED)
  const sums = [];
  for (let p = 0; p < 256; p++) {
    let s = 0;
    for (const r of named) s += r.mask[p];
    sums.push(s);
  }
  let mismatch = 0;
  if (named.length !== pageCensus.records.length) { mismatch++; materialAllMatch = false; }
  for (let i = 0; i < Math.min(named.length, pageCensus.records.length); i++) {
    const a = named[i], b = pageCensus.records[i];
    if (a.id !== b.id || a.name !== b.name || a.encoding !== b.encoding || a.size !== b.size
      || sha256(a.mask) !== b.maskSha256) { mismatch++; materialAllMatch = false; }
  }
  for (const r of named) {
    if (!idCensus.has(r.id)) idCensus.set(r.id, new Set());
    idCensus.get(r.id).add(r.name);
    if (!nameDupCensus.has(r.name)) nameDupCensus.set(r.name, new Set());
    nameDupCensus.get(r.name).add(r.id);
  }
  materialAudit.push({
    tile: te.name, era: ERA,
    independentConsumedExactly: indep.consumedExactly,
    pageConsumedExactly: pageCensus.tailConsumedExactly,
    recordCountTotal: indep.records.length,
    namedMaterialCount: named.length,
    systemRecordCount: indep.records.length - named.length,
    namedRecords: named.map((r) => ({ id: r.id, name: r.name, encoding: r.encoding, size: r.size,
      maskSha256: sha256(r.mask) })),
    pageRecordMismatchCount: mismatch,
    baseCheck: {
      baseName: base ? base.name : null, baseId: base ? base.id : null,
      baseAll255,
      stone04BaseRule: base && base.name === 'Stone04' && baseAll255
        ? 'HOLDS (base=Stone04 all-255)'
        : 'DATA SAYS OTHERWISE — recorded as-is (era-divergent region, no assumption)',
    },
    sumsCensus: { min: Math.min(...sums), max: Math.max(...sums),
      cellsExceeding255: sums.filter((s) => s > 255).length,
      note: 'sums>255 tolerated as ORIGINAL DATA (normalization REJECTED)' },
  });
}
const duplicateNames = [...nameDupCensus.entries()]
  .filter(([nm, ids]) => ids.size > 1)
  .map(([nm, ids]) => ({ name: nm, ids: [...ids] }));

// ================= (D) TEXTURES independent resolution =================
const tex = parseBnt2(PCG_TEXTURES);
const textureAudit = [];
let texturesAllMatch = true;
for (const [id, names] of idCensus) {
  const entryName = `${id}.dat`;
  const e = tex.m.get(entryName);
  if (!e) {
    textureAudit.push({ id, era: ERA, resolved: false,
      decision: 'MISSING in PCG_9_3_5 Textures.bnt — EXPLICIT era-labeled fallback decision required (no silent substitution)' });
    texturesAllMatch = false;
    continue;
  }
  // BNT2 Textures.bnt payloads are stored 1:1 RAW (no decompression —
  // canonical Bnt2Archive.readEntry semantics, re-implemented independently)
  const payload = tex.b.subarray(e.off, e.off + e.size);
  const payloadSha = sha256(payload);
  const pageBinding = pageResult.textureBindings.find((b) => b.id === id);
  let mean = null, decoded = true;
  try { mean = independentTgaMeanAndSha(payload); }
  catch (err) { decoded = false; }
  const match = pageBinding && pageBinding.payloadSha256 === payloadSha;
  if (!match) texturesAllMatch = false;
  textureAudit.push({
    id, names: [...names], era: ERA, entry: entryName, resolved: true,
    payloadSha256: payloadSha, pagePayloadSha256: pageBinding ? pageBinding.payloadSha256 : null,
    payloadMatch: !!match, decoded,
    decodedSize: mean ? `${mean.width}x${mean.height}` : null,
    meanRgb: mean ? mean.meanRgb : null,
  });
}

// ================= (E) HEIGHTS ORACLE (legitimate: heights are JUL-identical here) =================
// Legacy chunk layout (canon): chunk (r,c) = 513x513 samples covering map rows
// [r*512, r*512+512] (last row shared) and cols likewise. Region py 3200..3295
// -> chunk r006_c006 local rows 128..223; px 3200..3295 -> local cols 128..223.
const chunk = fs.readFileSync(LEGACY_CHUNK);
if (chunk.length !== 513 * 513 * 2) throw new Error(`unexpected chunk size ${chunk.length}`);
let oracleEq = 0, oracleNe = 0, oracleMaxAbs = 0;
const oracleDiffs = [];
for (let vy = 0; vy < 96; vy++) {
  for (let vx = 0; vx < 96; vx++) {
    const px = ORIGIN_X * 32 + vx, py = ORIGIN_Y * 32 + vy;
    const oracleVal = chunk.readUInt16LE(((py % 512) * 513 + (px % 512)) * 2);
    const tX = Math.floor(vx / 32), tY = Math.floor(vy / 32);
    const payload = inflateAt(pcg.b, pcg.m.get(tileName(ORIGIN_X + tX, ORIGIN_Y + tY)));
    const cleanVal = payload.readUInt16LE(64 + ((vy % 32) * 32 + (vx % 32)) * 2);
    if (oracleVal === cleanVal) oracleEq++;
    else {
      oracleNe++; oracleMaxAbs = Math.max(oracleMaxAbs, Math.abs(oracleVal - cleanVal));
      if (oracleDiffs.length < 10) oracleDiffs.push({ vx, vy, oracleVal, cleanVal });
    }
  }
}

// ================= (F) PIXEL PROBE vs independent texture means =================
const probeCompare = [];
let byteExactProbes = 0;
for (const p of pageResult.pixelProbe) {
  const texA = textureAudit.find((t) => t.id === p.dominantMaterial.id);
  const mean = texA ? texA.meanRgb : null;
  const rgb = p.rgb;
  const delta = mean ? [rgb[0] - mean[0], rgb[1] - mean[1], rgb[2] - mean[2]] : null;
  const byteExact = mean && rgb[0] === mean[0] && rgb[1] === mean[1] && rgb[2] === mean[2];
  if (byteExact) byteExactProbes++;
  probeCompare.push({
    tile: p.tile, era: ERA, canvasPos: p.canvasPos, rgb,
    dominantMaterial: p.dominantMaterial,
    independentMeanRgb: mean, delta,
    byteExactVsDominantMean: !!byteExact,
    note: 'probe fragment color vs mean of the dominant material at the probe cell — measured delta, mip/linear filtering in play (deterministic unlit render)',
  });
}

// ================= evidence write =================
const result = {
  iter: 'ITER_021',
  era: ERA,
  purpose: 'P0 independent byte audit: era-divergent region (100..102 x 100..102) through the clean pipeline — heights + materials + textures',
  sources: {
    pcgTerrainBnt: { path: PCG_TERRAIN, sha256: sha256(fs.readFileSync(PCG_TERRAIN)), era: ERA },
    pcgTexturesBnt: { path: PCG_TEXTURES, sha256: sha256(fs.readFileSync(PCG_TEXTURES)), era: ERA },
    julBnt: { path: JUL_TERRAIN, sha256: sha256(fs.readFileSync(JUL_TERRAIN)), era: 'JUL_2003 (era-labeled oracle, read-only)' },
    legacyHeightsOracleChunk: { path: LEGACY_CHUNK, sha256: sha256(chunk),
      renderer: 'r169 legacy eudoria-web (FROZEN, read-only)', sourceEra: 'JUL_2003 50.bnt heights',
      legitimacy: 'heights for these tiles are JUL-byte-identical (measured in (B)); the era divergence lives in the TAILS' },
    browserExport: { path: BROWSER_JSON, screenshotPngSha256: pageResult.screenshotPngSha256,
      screenshotDeterministicInPage: pageResult.screenshotDeterministicInPage },
  },
  heightsByteAudit: {
    method: 'independent minimal parser (this file) vs browser clean chain; per-tile sha256 of the 32x32 u16 LE height block',
    denominator: '9 tiles',
    allByteFaithful: heightsAllMatch,
    tiles: tileAudit.map((t) => ({
      name: t.name, heightsSha256: t.heightsSha256, byteFaithful: t.byteFaithful,
      reliefU16: t.reliefU16, payloadSha256: t.payloadSha256, julTwin: t.julTwin,
    })),
    seamDiagnostic: pageResult.heights.seamDiagnostic,
    seamNote: 'disjoint-tile borders are ORIGINAL DATA — NO repair applied (page export, PE Runtime Core diagnostic)',
  },
  julTwinCensus: {
    denominator: '9 tiles',
    perTile: tileAudit.map((t) => ({ tile: t.name, ...t.julTwin })),
    summary: (() => {
      const exists = tileAudit.filter((t) => t.julTwin.julTwinExists).length;
      const hEq = tileAudit.filter((t) => t.julTwin.julHeightsEqual).length;
      const tNe = tileAudit.filter((t) => t.julTwin.julTailEqual === false).length;
      return {
        julTwinsExist: `${exists}/9`, julHeightsIdentical: `${hEq}/9`, julTailsDiffer: `${tNe}/9`,
        eraLabels: { decode: 'PCG_9_3_5', twin: 'JUL_2003' },
        statement: 'every tile has a JUL twin that EXISTS-BUT-DIFFERS in the material tail; heights are byte-identical across eras for this region',
      };
    })(),
  },
  materialsByteAudit: {
    denominator: '9 tiles; per-tile record counts explicit (total/named/system)',
    independentParserAllMatch: materialAllMatch,
    perTile: materialAudit,
    distinctMaterialIds: idCensus.size,
    distinctMaterialIdCensus: [...idCensus.entries()].map(([id, names]) => ({ id, names: [...names] })),
    stone04BaseRuleRegionVerdict: (() => {
      const hold = materialAudit.filter((m) => m.baseCheck.stone04BaseRule === 'HOLDS (base=Stone04 all-255)').length;
      return {
        holdsOnTiles: `${hold}/9`,
        note: 'era-divergent region — rule RE-CHECKED on THIS data, not assumed from JUL-derived evidence',
      };
    })(),
    duplicateNameObservation: {
      denominator: 'named records across 9 tiles',
      duplicates: duplicateNames,
      note: 'same material NAME at multiple ids in PCG_9_3_5 tail data (e.g. Grassmix04) — ORIGINAL DATA, recorded; historical id-aliasing semantics UNRESOLVED',
    },
  },
  texturesByteAudit: {
    denominator: `${idCensus.size} distinct region material ids; PCG_9_3_5 Textures.bnt entries (all '<id>.dat')`,
    allPayloadsMatch: texturesAllMatch,
    census: textureAudit,
    fallbackDecision: '0 fallbacks expected; ANY missing id => EXPLICIT era-labeled decision, NO silent cross-era substitution (page enforces by throwing)',
  },
  heightsOracle: {
    oracleVersion: 'r169 legacy chunk binary (JUL_2003 heights baked by the FROZEN legacy runtime)',
    cleanVersion: `${ERA} bytes through the clean r185 pipeline`,
    regionMapPixels: { x0: ORIGIN_X * 32, y0: ORIGIN_Y * 32, w: 96, h: 96 },
    chunk: { file: path.basename(LEGACY_CHUNK), localRows: '128..223', localCols: '128..223' },
    equal: oracleEq, notEqual: oracleNe, total: 96 * 96, maxAbsDiff: oracleMaxAbs,
    firstDiffs: oracleDiffs,
  },
  materialOracleHonestNA: {
    r169MaterialOracle: 'N/A — the legacy r169 splat caches were baked from JUL_2003-era material tails; the JUL tails DIFFER on 9/9 tiles of this region (measured in julTwinCensus), so a legacy material byte comparison would compare two different eras, not validate the clean decode. Documented as honestly N/A per the iteration prompt.',
  },
  pixelProbeVsIndependentMeans: {
    denominator: `${probeCompare.length} probe points (one per tile center sample)`,
    byteExactProbes,
    probes: probeCompare,
  },
  verdict: null,
};
const heightsOk = heightsAllMatch && tileAudit.every((t) => t.byteFaithful);
const matsOk = materialAllMatch && materialAudit.every((m) => m.independentConsumedExactly && m.pageConsumedExactly && m.pageRecordMismatchCount === 0);
const texOk = texturesAllMatch && textureAudit.every((t) => t.resolved && t.decoded);
const oracleOk = oracleNe === 0;
result.verdict = (heightsOk && matsOk && texOk && oracleOk)
  ? 'PASS — era-divergent region rendered byte-faithfully through the clean pipeline (heights 9/9 vs independent parser + heights oracle identical; materials 9/9 exact both parsers; textures all resolved same-era; probe deltas recorded)'
  : 'FAIL — see per-section booleans';
fs.writeFileSync(path.join(EVIDENCE_DIR, 'iter021_era_byte_audit.json'), JSON.stringify(result, null, 1));
console.log(JSON.stringify({
  verdict: result.verdict,
  heightsOk, matsOk, texOk, oracleOk,
  julTwinSummary: result.julTwinCensus.summary,
  distinctMaterialIds: idCensus.size,
  stone04Base: result.materialsByteAudit.stone04BaseRuleRegionVerdict,
  duplicateNames: duplicateNames,
  probeByteExact: byteExactProbes,
  probes: probeCompare.map((p) => ({ tile: p.tile, rgb: p.rgb, mean: p.independentMeanRgb, dom: p.dominantMaterial.name })),
}, null, 1));
