// av4_census.mjs — AV-4 gates + readiness matrix (read-only over Models.ark).
// GATE (a): parse ALL 677 NIF 4.0.x members (4.0.0.0 + 4.0.0.2) — superset of
//   the required >=50 sample; per-block PASS/partial/fail counters + reasons.
// GATE (b): negatives — truncated payload, byte-swapped (endian) payload, and
//   a 4.1 file fed to the 40 adapter (version-width control) MUST ALL FAIL.
// GATE (c): 2 files decoded by an INDEPENDENT naive scanner (separate code
//   path, raw-byte anchored RTTI walk) — geometry counts must agree.
// OUTPUT: SCI AV4_NIF40/READINESS_MATRIX_40.json + GATES_40.json.
'use strict';
import { promises as fs } from 'node:fs';
import { ArkArchive } from '../../src/pesource/ArkArchive.js';
import { parseModel40 } from '../../src/pesource/NifModelReader40.js';

const MODELS = 'D:\\Eudoria_Reconstruction\\01_Original_Files\\ARK\\Models.ark';
const SCI = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_ISO_ASSET_VIEWER_R1_20261031\\AV4_NIF40';

const mbuf = new Uint8Array(await fs.readFile(MODELS));
const ark = new ArkArchive(mbuf);

// ---- collect 4.0.x members ----
const v400 = [], v402 = [], v41sample = [];
for (const e of ark.entries()) {
  const { payload } = ark.readEntry(e);
  const nl = payload.indexOf(0x0a);
  if (nl < 0) continue;
  const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  const ver = dv.getUint32(nl + 1, true);
  if (ver === 0x04000000) v400.push({ e, payload });
  else if (ver === 0x04000002) v402.push({ e, payload });
  else if (ver === 0x0401000C && v41sample.length < 1) v41sample.push({ e, payload });
}
console.log('v400', v400.length, 'v402', v402.length);

function versionKey(ver) { return ver === 0x04000000 ? '4.0.0.0' : '4.0.0.2'; }

function newAcc() {
  return { total: 0, parsePass: 0, parsePartial: 0, parseFail: 0,
    withGeometry: 0, withTextures: 0, withMaterial: 0, withKf: 0, withUVData: 0,
    renderable: 0, closureViolations: 0, topObjectTailOk: 0, topObjectTailBad: 0,
    shapes: 0, vertices: 0, triangles: 0, texJoins: 0, blockTypeCounts: {},
    failReasons: {}, partialReasons: {}, opaqueTypeCounts: {} };
}

function bump(map, k) { map[k] = (map[k] ?? 0) + 1; }

function parseOne(rec, acc) {
  acc.total++;
  try {
    const { extraction, renderModel } = parseModel40(rec.payload, rec.e.name);
    for (const b of extraction.blocks) {
      bump(acc.blockTypeCounts, b.type + (b.opaque ? ' [opaque]' : ''));
      if (b.opaque) bump(acc.opaqueTypeCounts, b.type);
      if (b.type === 'NiKeyframeController') acc.withKf += 0; // per-file below
    }
    const hasKf = extraction.blocks.some(b => b.type.startsWith('NiKeyframe') || b.type === 'NiKeyframeData');
    const status = extraction.parseStatus ?? 'PASS';
    if (status === 'PASS') {
      const ok = extraction.opaqueBlocks.length === 0 && extraction.closureViolations === 0
        && extraction.topLevelObjects !== null && extraction.fileTailBytesLen === 0;
      if (ok) { acc.parsePass++; bump(acc.failReasons, '__never__'); }
      else {
        acc.parsePartial++;
        if (extraction.opaqueBlocks.length > 0) bump(acc.partialReasons, 'opaque_blocks=' + extraction.opaqueBlocks.length);
        if (extraction.closureViolations > 0) bump(acc.partialReasons, 'closure_violations=' + extraction.closureViolations);
        if (extraction.topLevelObjects === null) bump(acc.partialReasons, 'no_top_level_tail');
        else if (extraction.fileTailBytesLen > 0) bump(acc.partialReasons, 'leftover_tail_bytes=' + extraction.fileTailBytesLen);
      }
      acc.closureViolations += extraction.closureViolations;
      if (extraction.topLevelObjects !== null) acc.topObjectTailOk++;
      else acc.topObjectTailBad++;
      if (renderModel.shapes.length > 0) {
        acc.withGeometry++;
        acc.renderable++;
        let verts = 0, tris = 0;
        for (const sh of renderModel.shapes) { verts += sh.numVertices; tris += sh.numTriangles; }
        acc.vertices += verts; acc.triangles += tris;
      }
      let joins = 0, hasMat = false;
      for (const sh of renderModel.shapes) {
        if (sh.material) hasMat = true;
        if (sh.textureProp) {
          for (const slot of sh.textureProp.textures) if (slot && slot.has === 1) { joins++; }
        }
      }
      acc.texJoins += joins;
      if (joins > 0) acc.withTextures++;
      if (hasMat) acc.withMaterial++;
      if (hasKf) acc.withKf++;
      if (extraction.blocks.some(b => b.type === 'NiUVController' || b.type === 'NiUVData')) acc.withUVData++;
      acc.shapes += renderModel.shapes.length;
      return { name: rec.e.name, status, shapes: renderModel.shapes.length, opaque: extraction.opaqueBlocks.length, joins };
    }
    // STOPPED_* on an otherwise-declared-complete file
    acc.parseFail++;
    bump(acc.failReasons, status);
    return { name: rec.e.name, status, shapes: 0, opaque: extraction.opaqueBlocks.length, joins: 0 };
  } catch (err) {
    acc.parseFail++;
    const reason = String(err.message ?? err).replace(rec.e.name, '<file>').slice(0, 100);
    bump(acc.failReasons, reason);
    return { name: rec.e.name, status: 'PARSE_FAIL: ' + reason, shapes: 0, opaque: 0, joins: 0 };
  }
}

const accs = { '4.0.0.0': newAcc(), '4.0.0.2': newAcc() };
const perFile = [];
for (const rec of v400) perFile.push({ version: '4.0.0.0', ...parseOne(rec, accs['4.0.0.0']) });
for (const rec of v402) perFile.push({ version: '4.0.0.2', ...parseOne(rec, accs['4.0.0.2']) });

// ---- GATE (b): negatives MUST FAIL ----
const negatives = {};
function negativeGuard(name, fn) {
  // A negative MUST NOT yield a full PASS (status PASS + clean tail). Any
  // throw OR any non-PASS/unclean status counts as the expected FAIL.
  try {
    const { extraction } = fn();
    const clean = (extraction.parseStatus === 'PASS') &&
      extraction.opaqueBlocks.length === 0 &&
      extraction.closureViolations === 0 &&
      extraction.fileTailBytesLen === 0 &&
      extraction.topLevelObjects !== null;
    negatives[name] = clean ? 'FAIL_EXPECTED__BUT_PASSED' : 'FAIL (non-PASS status: ' + extraction.parseStatus + ')';
  } catch (err) { negatives[name] = 'FAIL: ' + String(err.message).slice(0, 80); }
}
{
  const rec = v400[0];
  const cut = Math.floor(rec.payload.length * 0.6);
  negativeGuard('truncated60pct', () => parseModel40(rec.payload.subarray(0, cut), 'truncated.nif'));
  const swapped = Uint8Array.from(rec.payload);
  const nl = swapped.indexOf(0x0a);
  const tmp = swapped[nl + 1]; swapped[nl + 1] = swapped[nl + 4]; swapped[nl + 4] = tmp;
  const t2 = swapped[nl + 2]; swapped[nl + 2] = swapped[nl + 3]; swapped[nl + 3] = t2;
  negativeGuard('endianSwapped', () => parseModel40(swapped, 'endian.nif'));
  negativeGuard('v41Into40', () => parseModel40(v41sample[0].payload, 'v41.nif'));
  const rec2 = v402[0];
  const cut2 = Math.floor(rec2.payload.length * 0.4);
  negativeGuard('truncated40pct', () => parseModel40(rec2.payload.subarray(0, cut2), 'truncated2.nif'));
}

// ---- GATE (c): independent naive scanner (separate code path) ----
// Walks raw bytes: finds "NiTriShapeData" RTTI anchors, then reads the 4.0
// header fields at hypothesized offsets with INDEPENDENT arithmetic and
// computes the block span; compares against the reader's per-block numbers.
function independentScan(payload) {
  const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  const needle = 'NiTriShapeData';
  const nb = new Uint8Array(needle.length);
  for (let i = 0; i < needle.length; i++) nb[i] = needle.charCodeAt(i);
  const results = [];
  const rtti = (pos) => {
    const len = dv.getInt32(pos, true);
    if (len < 1 || len > 256) return null;
    let s = '';
    for (let i = 0; i < len; i++) s += String.fromCharCode(payload[pos + 4 + i]);
    return { len, name: s };
  };
  let pos = 0;
  while (pos + 4 < payload.length) {
    const r = rtti(pos);
    if (r && r.name === needle) {
      let p = pos + 4 + r.len;
      const numVertices = dv.getUint16(p, true); p += 2;
      const vp = dv.getUint32(p, true); p += 4;
      if (vp !== 0) p += numVertices * 12;
      const np = dv.getUint32(p, true); p += 4;
      if (np !== 0) p += numVertices * 12;
      p += 16; // center vec3 + radius
      const cp = dv.getUint32(p, true); p += 4;
      if (cp !== 0) p += numVertices * 16;
      const numTextureSets = dv.getInt16(p, true); p += 2;
      const uvp = dv.getUint32(p, true); p += 4;
      if (numTextureSets > 0 && uvp !== 0) p += numTextureSets * numVertices * 8;
      const numTriangles = dv.getUint16(p, true); p += 2;
      const tp = dv.getUint32(p, true); p += 4;
      p += numTriangles * 6;
      const numMatchGroups = dv.getUint16(p, true); p += 2;
      for (let g = 0; g < numMatchGroups; g++) {
        const c = dv.getUint16(p, true); p += 2 + c * 2;
      }
      results.push({ rttiStart: pos, numVertices, numTextureSets, numTriangles, blockEnd: p });
      pos = p;
    } else pos++;
  }
  return results;
}

const crosscheck = [];
for (const rec of [v400.find(r => r.e.size > 40000) ?? v400[0], v402.find(r => r.e.size > 40000) ?? v402[0]]) {
  const { extraction, renderModel } = parseModel40(rec.payload, rec.e.name);
  const readerShapes = extraction.blocks.filter(b => b.type === 'NiTriShapeData' && !b.opaque).map(b => ({
    rttiStart: b.rttiStart, numVertices: b.fields.numVertices, numTextureSets: b.fields.numTextureSets,
    numTriangles: b.fields.numTriangles, blockEnd: b.blockEnd,
  }));
  const indep = independentScan(rec.payload);
  const match = readerShapes.length === indep.length && readerShapes.every((r, i) =>
    r.rttiStart === indep[i].rttiStart && r.numVertices === indep[i].numVertices &&
    r.numTextureSets === indep[i].numTextureSets && r.numTriangles === indep[i].numTriangles &&
    r.blockEnd === indep[i].blockEnd);
  crosscheck.push({ file: rec.e.name, version: versionKey(dv0(rec.payload)), readerShapeDataBlocks: readerShapes.length,
    independentShapeDataBlocks: indep.length, spanExactMatch: match,
    reader: readerShapes.slice(0, 3), independent: indep.slice(0, 3) });
}
function dv0(p) { const dv = new DataView(p.buffer, p.byteOffset, p.byteLength); const nl = p.indexOf(0x0a); return dv.getUint32(nl + 1, true); }

const readiness = {
  job: 'AV-4 NIF40 reader + readiness matrix',
  era: 'ISO_5_1_0_0 (single era label; per-file NIF format versions explicit)',
  source: { file: MODELS, sha256_pin: 'F660D055B4B9471B3B6E16B07F5368DBD6F2208DAB6B51BB9BDB9942BD73EA62' },
  corpus: { totalNif40x: v400.length + v402.length, v400: v400.length, v402: v402.length },
  perVersion: accs,
  negatives,
  crosscheck,
  generated: new Date().toISOString(),
};

await fs.mkdir(SCI, { recursive: true });
await fs.writeFile(SCI + '\\READINESS_MATRIX_40.json', JSON.stringify(readiness, null, 1));
await fs.writeFile(SCI + '\\GATES_40_PERFILE.json', JSON.stringify(perFile, null, 1));
console.log(JSON.stringify({ corpus: readiness.corpus, perVersion: {
  '4.0.0.0': { pass: accs['4.0.0.0'].parsePass, partial: accs['4.0.0.0'].parsePartial, fail: accs['4.0.0.0'].parseFail, geom: accs['4.0.0.0'].withGeometry, tex: accs['4.0.0.0'].withTextures },
  '4.0.0.2': { pass: accs['4.0.0.2'].parsePass, partial: accs['4.0.0.2'].parsePartial, fail: accs['4.0.0.2'].parseFail, geom: accs['4.0.0.2'].withGeometry, tex: accs['4.0.0.2'].withTextures },
}, negatives, crosscheck: crosscheck.map(c => ({ file: c.file, match: c.spanExactMatch })) }, null, 2));
