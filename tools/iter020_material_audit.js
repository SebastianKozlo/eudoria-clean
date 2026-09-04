// iter020_material_audit.js — MILESTONE 1-E ITER 020 P0 AUDIT (Node side)
// QUESTION: Do the CONFIRMED terrain material data for the audited 9-tile
// region decode through the CLEAN pipeline with byte-provenance from
// PCG_9_3_5 (heights + materials + textures, end-to-end, zero legacy input)?
//
// CHAIN: pcg_install terrain.bnt + Textures.bnt ORIGINAL BYTES
//   -> PESourceMount (PCG_9_3_5, BNT2_TERRAIN / BNT2, SHA-pinned mounts)
//   -> getTerrainMaterials (TdfMaterialTailDecoder, CONFIRMED tail format)
//   -> canonical material objects (provenance on every object)
//   -> resolveTexture + TgaDecoder (same-era PCG texture payloads)
//
// INDEPENDENT CHECKS (non-circular):
//   (1) SECOND minimal parser in this script (no shared code with the
//       format layer) re-walks every tail and compares per-record bytes.
//   (2) JUL_2003 oracle: frozen iter008b tile material lists (independent
//       earlier evidence, different corpus copy) vs the PCG decode.
//   (3) EU/CD era oracle: frozen iter010_id_resolution.csv payload SHA256s
//       vs the PCG texture payload SHA256s (byte-identity census).
'use strict';
import { promises as fs } from 'node:fs';
import { createHash } from 'node:crypto';
import { inflateSync } from 'node:zlib';
import { PESourceMount } from '../src/pesource/PESourceMount.js';
import { ERAS } from '../src/pesource/PEProvenance.js';
import { decodeTga2 } from '../src/pesource/TgaDecoder.js';

const TERRAIN_PATH = 'D:/Eudoria_Reconstruction/pcg_install/Data/Terrain/terrain.bnt';
const TEXTURES_PATH = 'D:/Eudoria_Reconstruction/pcg_install/Data/Textures/Textures.bnt';
const JUL_CSV = 'D:/Eudoria_Reconstruction/99_Audits/PE_MILESTONE_1_WORLD_SURFACE_R1/03_EVIDENCE/iter008b_tile_material_lists.csv';
const ERA_CSV = 'D:/Eudoria_Reconstruction/99_Audits/PE_MILESTONE_1_WORLD_SURFACE_R1/03_EVIDENCE/iter010_id_resolution.csv';
const EVIDENCE_DIR = 'D:/Eudoria_Reconstruction/99_Audits/PE_MILESTONE_1_WORLD_SURFACE_R1/03_EVIDENCE';

const sha256 = (bytes) => createHash('sha256').update(bytes).digest('hex').toUpperCase();
const b64 = (bytes) => Buffer.from(bytes).toString('base64');

// ---------- clean-chain I/O adapter (Node) ----------
const io = {
  readFile: async (p) => new Uint8Array(await fs.readFile(p)),
  inflate: async (zlibBytes) => new Uint8Array(inflateSync(zlibBytes)),
  sha256: async (bytes) => sha256(bytes),
};

const ORIGIN_X = 56, ORIGIN_Y = 112, N = 3;
const tiles = [];
for (let y = ORIGIN_Y; y < ORIGIN_Y + N; y++) for (let x = ORIGIN_X; x < ORIGIN_X + N; x++) tiles.push({ x, y });

// ---------- (A) CLEAN-PATH MATERIAL DECODE ----------
const mount = new PESourceMount(io);
const terrainMount = await mount.mountEra({
  era: ERAS.PCG_9_3_5, container: 'Terrain/terrain.bnt', path: TERRAIN_PATH,
  format: 'BNT2_TERRAIN', verifyHash: true,
});
const texturesMount = await mount.mountEra({
  era: ERAS.PCG_9_3_5, container: 'Textures.bnt', path: TEXTURES_PATH,
  format: 'BNT2', verifyHash: true,
});

const perTile = [];
const idCensus = new Map(); // id -> {names:Set, tiles:Set, maskCellsActive}
for (const t of tiles) {
  const dec = await mount.getTerrainMaterials({ era: ERAS.PCG_9_3_5, gridX: t.x, gridY: t.y });
  const base = dec.materials[0] ?? null;
  const baseAll255 = base ? Array.from(base.mask).every((v) => v === 255) : false;
  const tileEntry = {
    gridX: t.x, gridY: t.y, name: dec.tile.name,
    tailLength: dec.tile.tail.byteLength,
    recordCount: dec.provenance.extra.recordCount,
    namedMaterialCount: dec.provenance.extra.namedMaterialCount,
    systemRecordCount: dec.provenance.extra.systemRecordCount,
    tailConsumedExactly: dec.provenance.extra.tailConsumedExactly,
    heightsSha256: sha256(Buffer.from(dec.tile.heights.buffer.slice(0, 2048))),
    namedMaterials: dec.materials.map((m) => ({
      position: m.position, id: m.id, name: m.name, bps: m.bps, unk: m.unk, res: m.res,
      encoding: m.maskEncoding, size: m.size, recordOffset: m.recordOffset,
      maskSha256: sha256(m.mask),
      maskMin: Math.min(...m.mask), maskMax: Math.max(...m.mask),
      activeCells: Array.from(m.mask).filter((v) => v > 0).length,
    })),
    baseCheck: {
      baseName: base ? base.name : null, baseId: base ? base.id : null,
      baseIsStone04: base ? base.name === 'Stone04' : false,
      baseAll255, baseRule: 'Stone04 full-coverage base (CONFIRMED iter009); normalization REJECTED',
    },
    sums: dec.sums, // min/max/constantSum/cellsExceeding255 — sums>255 = ORIGINAL DATA
    provenance: dec.provenance,
    // full masks exported for the independent-language (Python) oracle compare
    masksB64: dec.materials.map((m) => ({ id: m.id, name: m.name, maskB64: b64(m.mask) })),
    systemRecords: dec.systemRecords,
  };
  perTile.push(tileEntry);
  for (const m of dec.materials) {
    if (!idCensus.has(m.id)) idCensus.set(m.id, { names: new Set(), tiles: new Set() });
    const c = idCensus.get(m.id);
    c.names.add(m.name); c.tiles.add(`${t.x},${t.y}`);
  }
}

// ---------- (B) INDEPENDENT SECOND PARSER (no shared code) ----------
// Minimal direct walk: BNT2 footer -> entry by name -> inflate -> tail ->
// [size][dim] records -> per-record field extraction. Written deliberately
// low-level (DataView only) to be structurally different from the decoder.
function independentTailWalk(terrainBytes, tileName) {
  const whole = Buffer.from(terrainBytes);
  const dv = new DataView(whole.buffer, whole.byteOffset, whole.byteLength);
  const dirOff = dv.getUint32(whole.length - 8, true);
  if (whole.toString('ascii', whole.length - 4, whole.length) !== 'BNT2') throw new Error('bad magic');
  const count = dv.getUint32(dirOff, true);
  let p = dirOff + 4;
  let entry = null;
  for (let i = 0; i < count; i++) {
    const s = p;
    while (whole[p] !== 0x0a) p++;
    const nm = whole.toString('ascii', s, p);
    p++;
    const size = dv.getUint32(p, true); const offset = dv.getUint32(p + 4, true);
    p += 16;
    if (nm === tileName) { entry = { size, offset, name: nm }; break; }
  }
  if (!entry) throw new Error(`entry ${tileName} not found`);
  const comp = whole.subarray(entry.offset + 8, entry.offset + 8 + entry.size - 8);
  const payload = new Uint8Array(inflateSync(comp));
  if (payload.length < 2112 + 4) throw new Error(`payload too small ${payload.length}`);
  const pdv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  const out = [];
  let q = 2112;
  while (q < payload.length) {
    const size = pdv.getUint32(q, true);
    const dim = pdv.getUint32(q + 4, true);
    const id = pdv.getUint32(q + 16, true);
    let name = '';
    for (let i = 0; i < 28; i++) { const c = pdv.getUint8(q + 24 + i); if (c === 0) break; name += String.fromCharCode(c); }
    const maskStart = q + 56, maskEnd = q + 4 + size;
    const region = payload.subarray(maskStart, maskEnd);
    let mask = null;
    if (region.length === dim * dim) {
      mask = Buffer.from(region); // RAW
    } else if (dim === 16) {
      // named-material class: strict independent RLE decode (count,value) pairs
      mask = Buffer.alloc(dim * dim);
      let w = 0, r = 0;
      while (r < region.length) {
        const cnt = region[r++], val = region[r++];
        if (w + cnt > dim * dim) throw new Error(`indep RLE overrun tile ${tileName}`);
        mask.fill(val, w, w + cnt); w += cnt;
      }
      if (w !== dim * dim) throw new Error(`indep RLE sum ${w} != ${dim * dim} tile ${tileName}`);
    } // other dims: raw region carried, no mask comparison (system records)
    out.push({ size, dim, id, name, mask });
    q = maskEnd;
  }
  return { records: out, consumedExactly: q === payload.length, payloadLen: payload.length };
}

const terrainBytes = terrainMount.bytes;
let independentMismatch = 0, independentCompared = 0, independentConsumedOk = 0;
for (const te of perTile) {
  const indep = independentTailWalk(terrainBytes, te.name);
  if (indep.consumedExactly) independentConsumedOk++;
  const cleanNamed = te.namedMaterials;
  const indepNamed = indep.records.filter((r) => r.dim === 16 && r.name.length > 0 && r.mask !== null);
  if (indepNamed.length !== cleanNamed.length) independentMismatch++;
  for (let i = 0; i < Math.min(indepNamed.length, cleanNamed.length); i++) {
    independentCompared++;
    const a = cleanNamed[i], b = indepNamed[i];
    if (a.id !== b.id || a.name !== b.name || a.size !== b.size) independentMismatch++;
    else if (!b64ToBytes(te.masksB64[i].maskB64).equals(b.mask)) independentMismatch++;
  }
}
function b64ToBytes(s) { return Buffer.from(s, 'base64'); }

// ---------- (C) JUL ORACLE (frozen iter008b evidence, read-only) ----------
const julCsv = await fs.readFile(JUL_CSV, 'utf8');
const julRows = new Map();
for (const line of julCsv.split('\n').slice(1)) {
  const m = line.match(/^(00[0-9a-f]{6})\.tdf,(\d+),(\d+),(\d+),exact,(\d+),"(.*)"\s*$/);
  if (m) julRows.set(m[1], { gx: +m[2], gy: +m[3], list: m[6] });
}
let julCompared = 0, julSequenceMatch = 0;
const julComparison = [];
for (const te of perTile) {
  const julName = `${te.gridX.toString(16).padStart(4, '0')}${te.gridY.toString(16).padStart(4, '0')}`;
  const jul = julRows.get(julName);
  if (!jul) { julComparison.push({ tile: te.name, julFound: false }); continue; }
  // parse JUL list "1:Stone04(16,rle_cv)|2:Grass01(...)|..." — named records only
  const julSeq = [...jul.list.matchAll(/(?:^|\|)\d+:([^|(]+)\(16,/g)].map((mm) => mm[1]);
  const pcgSeq = te.namedMaterials.map((m) => m.name);
  julCompared++;
  const match = julSeq.length === pcgSeq.length && julSeq.every((nm, i) => nm === pcgSeq[i]);
  if (match) julSequenceMatch++;
  julComparison.push({ tile: te.name, julFound: true, julSequence: julSeq, pcgSequence: pcgSeq, match });
}

// ---------- (D) TEXTURE RESOLUTION (same-era PCG container) + era oracle ----------
const eraCsv = await fs.readFile(ERA_CSV, 'utf8');
const eraRows = new Map();
for (const line of eraCsv.split('\n').slice(1)) {
  const c = line.split(',');
  if (c.length >= 12 && c[0].match(/^\d+$/)) {
    eraRows.set(parseInt(c[0], 10), { names: c[1], euSha: c[6], cdSha: c[10], sameBoth: c[11] });
  }
}
const textureCensus = [];
for (const [id, c] of idCensus) {
  const res = await mount.resolveTexture({ era: ERAS.PCG_9_3_5, container: 'Textures.bnt', textureId: id });
  const payloadSha = sha256(res.payload);
  const dec = decodeTga2(res.payload);
  const rgbaSha = sha256(dec.rgba);
  const era = eraRows.get(id) ?? null;
  let r = 0, g = 0, b = 0;
  for (let i = 0; i < dec.rgba.length; i += 4) { r += dec.rgba[i]; g += dec.rgba[i + 1]; b += dec.rgba[i + 2]; }
  const px = dec.width * dec.height;
  textureCensus.push({
    id, names: [...c.names], tilesUsed: [...c.tiles],
    pcgEntry: res.entry.name, pcgPayloadSize: res.payload.byteLength,
    pcgPayloadSha256: payloadSha, decodedSize: `${dec.width}x${dec.height}`,
    rgbaSha256: rgbaSha,
    meanColor: [Math.round(r / px), Math.round(g / px), Math.round(b / px)],
    euPayloadSha256: era ? era.euSha : null,
    cdPayloadSha256: era ? era.cdSha : null,
    pcgEqualsEu: era ? payloadSha.toLowerCase() === era.euSha : null,
    pcgEqualsCd: era ? payloadSha.toLowerCase() === era.cdSha : null,
    eraFallback: null, // PCG resolution expected same-era; fallbacks would be EXPLICIT here
    provenance: res.provenance,
  });
}

// PCG container census (what the container holds)
const { Bnt2Archive } = await import('../src/pesource/Bnt2Archive.js');
const texArch = new Bnt2Archive(texturesMount.bytes);
const texEntries = texArch.entries();
const texNameKinds = new Map();
for (const e of texEntries) {
  const kind = e.name.replace(/\d+/, 'N');
  texNameKinds.set(kind, (texNameKinds.get(kind) ?? 0) + 1);
}
const sizeHisto = new Map();
for (const e of texEntries) sizeHisto.set(e.size, (sizeHisto.get(e.size) ?? 0) + 1);

// ---------- evidence write ----------
const evidence = {
  iteration: 'ITER_020',
  p0: 'clean-path materials + texture binding audit (9-tile region, PCG_9_3_5 primary)',
  region: { originGridX: ORIGIN_X, originGridY: ORIGIN_Y, tilesX: N, tilesY: N, tileCount: 9 },
  mounts: {
    terrain: { path: TERRAIN_PATH, sha256: terrainMount.actualSha256, hashVerified: terrainMount.hashVerified },
    textures: { path: TEXTURES_PATH, sha256: texturesMount.actualSha256, hashVerified: texturesMount.hashVerified },
  },
  cleanDecode: {
    denominator: '9 tiles (region 56..58 x 112..114)',
    tilesAllTailConsumedExactly: perTile.every((t) => t.tailConsumedExactly),
    perTile: perTile.map((t) => ({
      name: t.name, gridX: t.gridX, gridY: t.gridY,
      recordCount: t.recordCount, namedMaterialCount: t.namedMaterialCount,
      systemRecordCount: t.systemRecordCount, tailConsumedExactly: t.tailConsumedExactly,
      namedMaterials: t.namedMaterials, baseCheck: t.baseCheck, sums: t.sums,
    })),
    materialIdCensus: [...idCensus.entries()].map(([id, c]) => ({
      id, names: [...c.names], tileCount: c.tiles.size, tiles: [...c.tiles],
    })),
    distinctMaterialIds: idCensus.size,
    stone04BaseRule: {
      allTilesBaseStone04: perTile.every((t) => t.baseCheck.baseIsStone04),
      allTilesBaseAll255: perTile.every((t) => t.baseCheck.baseAll255),
      normalization: 'REJECTED (iter009 corpus-wide); sums>255 tolerated as ORIGINAL DATA',
    },
  },
  independentSecondParser: {
    comparedRecords: independentCompared,
    mismatches: independentMismatch,
    tilesConsumedExactly: `${independentConsumedOk}/9`,
  },
  julOracle: {
    source: JUL_CSV, compared: julCompared, sequenceMatches: julSequenceMatch,
    eraLabels: { decode: 'PCG_9_3_5', oracle: 'JUL_2003 (frozen iter008b evidence)' },
    comparison: julComparison,
  },
  textures: {
    denominator: `${textureCensus.length} distinct region material ids`,
    eraLabel: 'PCG_9_3_5 (SAME-ERA primary); EU_LATER/CD_JAN_2003 = frozen iter010 oracles (read-only)',
    census: textureCensus,
  },
  pcgTextureContainerCensus: {
    entryCount: texEntries.length,
    nameKinds: [...texNameKinds.entries()],
    sizeHistogramTop: [...sizeHisto.entries()].sort((a, b) => b[1] - a[1]).slice(0, 10),
  },
};

await fs.mkdir(EVIDENCE_DIR, { recursive: true });
await fs.writeFile(`${EVIDENCE_DIR}/iter020_material_decode_audit.json`, JSON.stringify(evidence, null, 2));
// region decode export for the independent-language (Python) r169-oracle compare
await fs.writeFile(`${EVIDENCE_DIR}/iter020_region_masks_export.json`, JSON.stringify({
  region: { originGridX: ORIGIN_X, originGridY: ORIGIN_Y, tilesX: N, tilesY: N },
  tiles: perTile.map((t) => ({
    name: t.name, gridX: t.gridX, gridY: t.gridY,
    materials: t.masksB64.map((m, i) => ({
      id: m.id, name: m.name, maskB64: m.maskB64,
      encoding: t.namedMaterials[i].encoding,
    })),
  })),
}, null, 2));

// console summary
console.log('=== ITER 020 material audit ===');
console.log('tiles:', perTile.length, 'all tail consumed exactly:', evidence.cleanDecode.tilesAllTailConsumedExactly);
console.log('distinct material ids:', idCensus.size);
console.log('independent parser: compared', independentCompared, 'mismatches', independentMismatch, 'consumed', `${independentConsumedOk}/9`);
console.log('JUL oracle sequence matches:', `${julSequenceMatch}/${julCompared}`);
console.log('textures resolved (PCG same-era):', textureCensus.length,
  'pcgEqualsEu:', textureCensus.filter((t) => t.pcgEqualsEu).length,
  'pcgEqualsCd:', textureCensus.filter((t) => t.pcgEqualsCd).length);
console.log('PCG texture container entries:', texEntries.length);
console.log('evidence written to 03_EVIDENCE/iter020_material_decode_audit.json');
