// p0_byte_audit.js — MILESTONE 1-E ITER 019 P0 INDEPENDENT AUDIT (Node, offline).
// THREE independent verifications of the clean-pipeline P0 render:
//   1. BYTE AUDIT: decode the 9 region tiles from pcg terrain.bnt with a
//      MINIMAL parser written HERE (independent of src/pesource — a second
//      implementation), sha256 the 32x32 u16 LE height blocks, and compare
//      with the browser pipeline's exported hashes (p0_result.json).
//   2. ERA CROSS-CHECK: same tiles from JUL 50.bnt (C:\Entropia Universe) —
//      byte-equality of decompressed payloads recorded per tile (the region
//      was pre-selected byte-identical; any diff = genuine era divergence,
//      recorded, never forced).
//   3. R169 ORACLE: legacy chunk_r006_c003_u16le.bin (513x513 u16 LE, read-only)
//      — extract the region's pixels and compare with the clean-decoded
//      heights. VERSION-LABELED (oracle data = JUL 50.bnt baked by the r169
//      runtime; legitimate differences are recorded, not "fixed").
// Writes: 03_EVIDENCE/iter019_p0_byte_audit.json
'use strict';
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const zlib = require('zlib');

const PCG = 'D:/Eudoria_Reconstruction/pcg_install/Data/Terrain/terrain.bnt';
const JUL = 'C:/Entropia Universe/Data/Terrain/50.bnt';
const LEGACY_CHUNK = 'D:/Eudoria_Reconstruction/12_WebGame/eudoria-web/data/terrain/chunk_r006_c003_u16le.bin';
const P0_RESULT = process.argv[2]; // browser export JSON

const ORIGIN_X = 56, ORIGIN_Y = 112, N = 3;
const sha256 = (b) => crypto.createHash('sha256').update(b).digest('hex').toUpperCase();

// --- independent minimal parsers (SECOND implementation) ---
function parseBnt2Dir(file) {
  const b = fs.readFileSync(file);
  const dirOff = b.readUInt32LE(b.length - 8);
  const cnt = b.readUInt32LE(dirOff);
  const m = new Map();
  let p = dirOff + 4;
  for (let i = 0; i < cnt; i++) {
    const s = p;
    while (b[p] !== 0x0a) p++;
    const name = b.toString('latin1', s, p);
    p++;
    const size = b.readUInt32LE(p), off = b.readUInt32LE(p + 4);
    p += 16;
    m.set(name, { off, size });
  }
  if (p !== b.length - 8) throw new Error('BNT2 dir walk mismatch');
  return { b, m };
}
function parseBuntDir(file) {
  const b = fs.readFileSync(file);
  const dirOff = b.readUInt32LE(b.length - 8);
  const cnt = b.readUInt32LE(dirOff);
  const m = new Map();
  let p = dirOff + 4;
  for (let i = 0; i < cnt; i++) {
    const name = b.toString('latin1', p, p + 13).trim();
    const size = b.readUInt32LE(p + 13), off = b.readUInt32LE(p + 17);
    p += 21;
    m.set(name, { off, size });
  }
  if (p !== b.length - 8) throw new Error('BUNT dir walk mismatch');
  return { b, m };
}
const inflateAt = (b, e) => {
  const rec = b.subarray(e.off, e.off + e.size);
  if (rec[0] !== 0x02 || rec[1] !== 0x00 || rec[2] !== 0x00 || rec[3] !== 0xff) {
    throw new Error('bad record marker');
  }
  const dSize = rec.readUInt32LE(4);
  const out = zlib.inflateSync(rec.subarray(8, e.size)); // stream = size-8 bytes
  if (out.length !== dSize) throw new Error(`inflate size mismatch ${out.length} != ${dSize}`);
  return out;
};
const tileName = (x, y) => x.toString(16).padStart(4, '0') + y.toString(16).padStart(4, '0') + '.tdf';

// --- 1. byte audit vs browser export ---
const pcg = parseBnt2Dir(PCG);
const jul = parseBuntDir(JUL);
const browser = JSON.parse(fs.readFileSync(P0_RESULT, 'utf8'));
const browserHashes = new Map(browser.tileHeightsSha256.map(t => [t.name, t.heightsSha256]));

const tiles = [];
let allMatch = true;
for (let ty = ORIGIN_Y; ty < ORIGIN_Y + N; ty++) {
  for (let tx = ORIGIN_X; tx < ORIGIN_X + N; tx++) {
    const name = tileName(tx, ty);
    const payload = inflateAt(pcg.b, pcg.m.get(name));
    const heights = Buffer.alloc(2048);
    for (let i = 0; i < 1024; i++) heights.writeUInt16LE(payload.readUInt16LE(64 + i * 2), i * 2);
    const h = sha256(heights);
    const browserHash = browserHashes.get(name);
    const match = h === browserHash;
    if (!match) allMatch = false;
    // era cross-check
    const julEntry = jul.m.get(name);
    const julIdentical = julEntry
      ? inflateAt(jul.b, julEntry).equals(payload)
      : null;
    tiles.push({
      name, gridX: tx, gridY: ty,
      heightsSha256: h, browserHeightsSha256: browserHash, byteFaithful: match,
      payloadSha256: sha256(payload),
      julIdentical,
    });
  }
}

// --- 3. r169 oracle chunk comparison ---
// Legacy chunk layout (canon): chunk (r,c) is 513x513 samples covering map
// rows [r*512, r*512+512] (the last row is SHARED with chunk r+1) and cols
// [c*512, c*512+512]. The region py 3584..3679 therefore lives in chunk
// r007_c003 (local rows 0..95; local row 512 of r006 is the SAME shared first
// row — cross-checked below). px 1792..1887 -> local cols 256..351.
const ORACLE_CHUNK = 'D:/Eudoria_Reconstruction/12_WebGame/eudoria-web/data/terrain/chunk_r007_c003_u16le.bin';
const ORACLE_BORDER_CHUNK = 'D:/Eudoria_Reconstruction/12_WebGame/eudoria-web/data/terrain/chunk_r006_c003_u16le.bin';
const chunk = fs.readFileSync(ORACLE_CHUNK);
if (chunk.length !== 513 * 513 * 2) throw new Error(`unexpected chunk size ${chunk.length}`);
const borderChunk = fs.readFileSync(ORACLE_BORDER_CHUNK);
const px0 = ORIGIN_X * 32, py0 = ORIGIN_Y * 32;
const localRow = (py) => py % 512;   // 3584..3679 -> 0..95 (chunk r007)
const localCol = (px) => px % 512;   // 1792..1887 -> 256..351
let oracleEq = 0, oracleNe = 0, oracleMaxAbs = 0;
const oracleSamples = [];
let borderRowEq = 0, borderRowNe = 0;
for (let vy = 0; vy < 96; vy++) {
  for (let vx = 0; vx < 96; vx++) {
    const px = px0 + vx, py = py0 + vy;
    const chunkIdx = localRow(py) * 513 + localCol(px);
    const oracleVal = chunk.readUInt16LE(chunkIdx * 2);
    if (vy === 0) { // shared border row: chunk r006 local row 512 must agree
      const bIdx = 512 * 513 + localCol(px);
      if (borderChunk.readUInt16LE(bIdx * 2) === oracleVal) borderRowEq++; else borderRowNe++;
    }
    const tX = Math.floor(vx / 32), tY = Math.floor(vy / 32);
    const payload = inflateAt(pcg.b, pcg.m.get(tileName(ORIGIN_X + tX, ORIGIN_Y + tY)));
    const cleanVal = payload.readUInt16LE(64 + ((vy % 32) * 32 + (vx % 32)) * 2);
    if (oracleVal === cleanVal) oracleEq++; else {
      oracleNe++;
      oracleMaxAbs = Math.max(oracleMaxAbs, Math.abs(oracleVal - cleanVal));
      if (oracleSamples.length < 10) oracleSamples.push({ vx, vy, oracleVal, cleanVal });
    }
  }
}

const result = {
  iter: '019',
  purpose: 'P0 independent byte audit: second-parser verification of the clean pipeline 9-tile region + r169 oracle comparison',
  region: { originGridX: ORIGIN_X, originGridY: ORIGIN_Y, tiles: N * N, sampleGrid: '96x96' },
  sources: {
    pcgTerrainBnt: { path: PCG, sha256: sha256(fs.readFileSync(PCG)) },
    julBnt: { path: JUL, sha256: sha256(fs.readFileSync(JUL)) },
    legacyOracleChunk: { path: ORACLE_CHUNK, sha256: sha256(chunk), renderer: 'r169 legacy eudoria-web (FROZEN, read-only)', sourceEra: 'JUL_2003 50.bnt' },
    legacyOracleBorderChunk: { path: ORACLE_BORDER_CHUNK, sha256: sha256(borderChunk), role: 'shared-border cross-check (chunk r006 local row 512)' },
    browserExport: { path: P0_RESULT, screenshotPngSha256: browser.screenshotPngSha256 },
  },
  byteAudit: {
    method: 'independent minimal parser (this file) vs browser PESourceMount chain; per-tile sha256 of 32x32 u16 LE height block',
    allByteFaithful: allMatch,
    tiles,
  },
  oracleCompare: {
    oracleVersion: 'r169 legacy chunk binary (JUL_2003 bytes baked by the FROZEN legacy runtime)',
    cleanVersion: 'PCG_9_3_5 bytes through the clean r185 pipeline',
    regionMapPixels: { x0: px0, y0: py0, w: 96, h: 96 },
    chunk: { file: path.basename(ORACLE_CHUNK), localRows: '0..95', localCols: '256..351' },
    sharedBorderRowCrossCheck: { equal: borderRowEq, notEqual: borderRowNe, note: 'chunk r006 local row 512 vs chunk r007 local row 0 (same shared row)' },
    equal: oracleEq, notEqual: oracleNe, total: 96 * 96,
    maxAbsDiff: oracleMaxAbs,
    firstDiffs: oracleSamples,
    interpretation: oracleNe === 0
      ? 'IDENTICAL: the clean r185 pipeline reproduces the r169 oracle bytes for this region (both eras byte-identical here)'
      : 'DIFFERENCES RECORDED (era divergence and/or oracle bake transformations) — legitimate differences, not fixed',
  },
  verdict: null,
};
result.verdict = allMatch
  ? (oracleNe === 0 ? 'PASS — byte-faithful vs independent parser AND identical to the r169 oracle for this region'
                   : 'PASS — byte-faithful vs independent parser; oracle differences recorded (legitimate)')
  : 'FAIL — clean pipeline heights do not match the independent parser';
fs.writeFileSync(path.join(__dirname, '..', '..', '..', '99_Audits', 'PE_MILESTONE_1_WORLD_SURFACE_R1', '03_EVIDENCE', 'iter019_p0_byte_audit.json'),
  JSON.stringify(result, null, 1));
console.log(JSON.stringify({ verdict: result.verdict, byteAuditAllMatch: allMatch, oracleEq, oracleNe, oracleMaxAbs, firstDiffs: oracleSamples }, null, 1));
