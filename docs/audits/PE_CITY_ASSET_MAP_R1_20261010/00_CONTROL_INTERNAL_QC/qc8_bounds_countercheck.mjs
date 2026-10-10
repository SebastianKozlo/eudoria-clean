// QC8 — INDEPENDENT bounds countercheck (pe-master-auditor fresh internal QC).
// My OWN minimal raw-byte NIF 4.1.0.12 parser written from the documented SDK
// layouts (NiObjectNET/NiAVObject/NiNode/NiGeometry/NiGeometryData/NiTriShapeData/
// NiProperty-family/NiExtraData base + the documented Ark lineage splits).
// Imports NOTHING from the executor (no nif41_deep, no PecSceneIR, no PecTransform).
// Purpose: independent per-axis vertex bounds for the four primaries, compared
// against the published extents (tolerance 0.01 = float-print rounding budget).
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve, join } from 'node:path';

const PRIV = process.argv[2];
const PKG = resolve(process.argv[3]);

class MyReader {
  constructor(bytes) { this.b = bytes; this.dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength); this.p = 0; }
  get size() { return this.b.length; }
  u8() { return this.b[this.p++]; }
  u16() { const v = this.dv.getUint16(this.p, true); this.p += 2; return v; }
  i16() { const v = this.dv.getInt16(this.p, true); this.p += 2; return v; }
  u32() { const v = this.dv.getUint32(this.p, true); this.p += 4; return v; }
  i32() { const v = this.dv.getInt32(this.p, true); this.p += 4; return v; }
  f32() { const v = this.dv.getFloat32(this.p, true); this.p += 4; return v; }
  sstr() { const n = this.i32(); if (n < 0 || n > 1e6) throw new Error('bad sstr len ' + n); let s = ''; for (let i = 0; i < n; i++) s += String.fromCharCode(this.b[this.p + i]); this.p += n; return s; }
  ref() { return this.i32(); }
  refs() { const n = this.u32(); if (n > 65536) throw new Error('bad refs count ' + n); const a = []; for (let i = 0; i < n; i++) a.push(this.ref()); return a; }
  raw(n) { const h = this.b.subarray(this.p, this.p + n).toString('hex'); this.p += n; return h; }
}

function parseModel(bytes, name) {
  const s = new MyReader(bytes);
  const nl = bytes.indexOf(0x0a);
  const headerText = bytes.subarray(0, nl).toString('latin1');
  s.p = nl + 1;
  const version = s.u32();
  if (version !== 0x0401000C) throw new Error(`${name}: version 0x${version.toString(16)} not 4.1.0.12`);
  const numBlocks = s.u32();
  const blocks = [];
  const trsRows = [];
  const meshBounds = [];
  let triTotal = 0, vertTotal = 0;
  for (let i = 0; i < numBlocks; i++) {
    const type = s.sstr();
    if (type === 'NiNode' || type === 'NiTriShape') {
      // NiObjectNET: name SS, extraData ref, controller ref
      const nm = s.sstr(); s.ref(); s.ref();
      // NiAVObject: flags u16, translation vec3, rotation mat33, scale f32, velocity vec3, propertyRefs, hasABV u8
      s.u16();
      const t = [s.f32(), s.f32(), s.f32()];
      const rot = [];
      for (let r = 0; r < 3; r++) rot.push([s.f32(), s.f32(), s.f32()]);
      const sc = s.f32();
      s.f32(); s.f32(); s.f32(); // velocity
      s.refs();
      if (s.u8() !== 0) throw new Error(`${name}: block ${i} hasABV=true (not expected)`);
      trsRows.push({ block: i, type, name: nm, t, rot, sc });
      if (type === 'NiNode') { s.refs(); s.refs(); } // children + effects
      else { s.ref(); s.ref(); } // NiGeometry: dataRef + skinRef
      blocks.push({ i, type, name: nm });
    } else if (type === 'NiTriShapeData') {
      const nv = s.u16();
      const hasV = s.u8() !== 0;
      if (!hasV) throw new Error(`${name}: NiTriShapeData without vertices — layout assumption broken`);
      const verts = new Float32Array(nv * 3);
      let mn = [Infinity, Infinity, Infinity], mx = [-Infinity, -Infinity, -Infinity];
      for (let k = 0; k < nv * 3; k++) {
        const v = s.f32(); verts[k] = v;
        const ax = k % 3;
        if (v < mn[ax]) mn[ax] = v;
        if (v > mx[ax]) mx[ax] = v;
      }
      const hasN = s.u8() !== 0;
      if (hasN) { for (let k = 0; k < nv * 3; k++) s.f32(); } // normals (unit vectors; skipped in bounds)
      s.f32(); s.f32(); s.f32(); // center
      s.f32(); // radius
      const hasC = s.u8() !== 0;
      if (hasC) { for (let k = 0; k < nv * 4; k++) s.f32(); } // colors
      const nts = s.i16(); const uvSets = nts & 0x3F;
      for (let u = 0; u < uvSets; u++) { for (let k = 0; k < nv * 2; k++) s.f32(); }
      const nt = s.u16(); const tll = s.u32();
      if (tll !== nt * 3) throw new Error(`${name}: triListLength ${tll} != numTriangles*3 ${nt * 3}`);
      for (let k = 0; k < tll; k++) { const idx = s.u16(); if (idx >= nv) throw new Error(`${name}: index ${idx} >= numVertices ${nv}`); }
      const mg = s.u16(); for (let g = 0; g < mg; g++) { const c = s.u16(); for (let k = 0; k < c; k++) s.u16(); }
      meshBounds.push({ block: i, nv, nt, min: mn, max: mx, uvSets });
      triTotal += nt; vertTotal += nv;
      blocks.push({ i, type });
    } else if (type === 'NiMaterialProperty') {
      s.sstr(); s.ref(); s.ref(); s.u16();
      for (let k = 0; k < 12; k++) s.f32(); // ambient/diffuse/specular/emissive
      s.f32(); s.f32(); // glossiness + alpha
      blocks.push({ i, type });
    } else if (type === 'NiZBufferProperty' || type === 'NiVertexColorProperty') {
      s.sstr(); s.ref(); s.ref(); s.u16();
      if (type === 'NiZBufferProperty') s.u32();
      else { s.u32(); s.u32(); }
      blocks.push({ i, type });
    } else if (type === 'NiArkTextureExtraData') {
      s.ref(); s.u32(); // NiExtraData base: nextRef + uiSize
      s.i32(); s.i32(); s.u8(); // ui1a, ui1b, ub
      const numTex = s.i32();
      if (numTex < 0 || numTex > 4096) throw new Error(`${name}: numTex ${numTex} implausible`);
      for (let e = 0; e < numTex; e++) { s.sstr(); s.i32(); s.i32(); s.ref(); s.raw(9); }
      blocks.push({ i, type, numTex });
    } else if (type === 'NiArkAnimationExtraData') {
      s.ref(); s.u32();
      s.i32(); s.i32(); s.i32(); s.i32();
      s.raw(33);
      blocks.push({ i, type });
    } else if (type === 'NiArkImporterExtraData') {
      s.ref(); s.u32();
      s.i32(); const nm = s.sstr(); s.raw(13);
      for (let k = 0; k < 7; k++) s.f32();
      blocks.push({ i, type, name: nm });
    } else {
      throw new Error(`${name}: block ${i} unknown type "${type}" — my independent reader refuses (loud)`);
    }
  }
  const numTop = s.u32();
  const tops = [];
  for (let i = 0; i < numTop; i++) tops.push(s.ref());
  const closure = s.p === s.size;
  // file-wide vertex bounds (per axis)
  const fileMin = [Infinity, Infinity, Infinity], fileMax = [-Infinity, -Infinity, -Infinity];
  for (const m of meshBounds) for (let a = 0; a < 3; a++) { if (m.min[a] < fileMin[a]) fileMin[a] = m.min[a]; if (m.max[a] > fileMax[a]) fileMax[a] = m.max[a]; }
  const extents = [fileMax[0] - fileMin[0], fileMax[1] - fileMin[1], fileMax[2] - fileMin[2]];
  // TRS identity check (my own)
  const nonIdentity = trsRows.filter(r => !(r.t[0] === 0 && r.t[1] === 0 && r.t[2] === 0 && r.sc === 1 && r.rot[0][0] === 1 && r.rot[1][1] === 1 && r.rot[2][2] === 1 && r.rot[0][1] === 0 && r.rot[0][2] === 0 && r.rot[1][0] === 0 && r.rot[1][2] === 0 && r.rot[2][0] === 0 && r.rot[2][1] === 0));
  return {
    model: name, headerText, numBlocks, blockTypes: blocks.map(b => b.type),
    closureEofExact: closure, numTopObjects: numTop, topObjects: tops,
    meshCount: meshBounds.length, meshBounds, vertexTotal: vertTotal, triangleTotal: triTotal,
    fileVertexMin: fileMin, fileVertexMax: fileMax, extents, maxAxisExtent: Math.max(...extents),
    nonIdentityTrsCount: nonIdentity.length, avObjectCount: trsRows.length,
    names: trsRows.map(r => r.name)
  };
}

const published = {
  '192374': { min: [-10230.58, -9733.57, 0], max: [22558.57, 16306.27, 5952.57], extents: [32789.15, 26039.84, 5952.57], maxAxis: 32789.15, tri: 1200, vert: 2400, meshes: 4 },
  '193207': { min: [-8620.09, -9269.01, 0], max: [18320.81, 7643.05, 1570.07], extents: [26940.91, 16912.07, 1570.07], maxAxis: 26940.91, tri: 864, vert: 1698, meshes: 2 },
  '193313': { min: [-12508.28, -11570.41, 0], max: [19257.57, 16369.40, 5308.88], extents: [31765.85, 27939.80, 5308.88], maxAxis: 31765.85, tri: 1192, vert: 2384, meshes: 5 },
  '193684': { min: [-12830.90, -15486.04, -74.67], max: [19238.37, 18253.16, 3687.61], extents: [32069.27, 33739.21, 3762.27], maxAxis: 33739.21, tri: 1340, vert: 2680, meshes: 8 },
};
const TOL = 0.01;
const results = { qcStep: 'QC8_INDEPENDENT_BOUNDS_COUNTERCHECK', method: 'own minimal raw-byte NIF 4.1.0.12 vertex reader; zero executor imports; tolerance 0.01 on published (2-dp-rounded) values', models: {} };
let allOk = true;
for (const id of ['192374', '193207', '193313', '193684']) {
  const bytes = readFileSync(join(PRIV, 'PHASE3_MODELS', `${id}.nif`));
  const mine = parseModel(new Uint8Array(bytes), id);
  const pub = published[id];
  const cmp = {
    closureEofExact: mine.closureEofExact,
    numBlocks: mine.numBlocks,
    meshes: mine.meshCount, meshes_ok: mine.meshCount === pub.meshes,
    vertexTotal: mine.vertexTotal, vertexTotal_ok: mine.vertexTotal === pub.vert,
    triangleTotal: mine.triangleTotal, triangleTotal_ok: mine.triangleTotal === pub.tri,
    myVertexMin: mine.fileVertexMin, publishedMin: pub.min,
    myVertexMax: mine.fileVertexMax, publishedMax: pub.max,
    min_ok: mine.fileVertexMin.every((v, a) => Math.abs(v - pub.min[a]) <= TOL),
    max_ok: mine.fileVertexMax.every((v, a) => Math.abs(v - pub.max[a]) <= TOL),
    myExtents: mine.extents, publishedExtents: pub.extents,
    extents_ok: mine.extents.every((v, a) => Math.abs(v - pub.extents[a]) <= TOL),
    myMaxAxis: mine.maxAxisExtent, publishedMaxAxis: pub.maxAxis,
    maxAxis_ok: Math.abs(mine.maxAxisExtent - pub.maxAxis) <= TOL,
    nonIdentityTrsCount: mine.nonIdentityTrsCount, identityTrs_confirmed: mine.nonIdentityTrsCount === 0,
    names: mine.names
  };
  const ok = cmp.closureEofExact && cmp.meshes_ok && cmp.vertexTotal_ok && cmp.triangleTotal_ok && cmp.min_ok && cmp.max_ok && cmp.extents_ok && cmp.maxAxis_ok && cmp.identityTrs_confirmed;
  allOk = allOk && ok;
  results.models[id] = { ok, ...cmp, raw: mine };
  console.log(`${id}: closure=${cmp.closureEofExact} blocks=${mine.numBlocks} meshes=${cmp.meshes_ok} vert=${cmp.vertexTotal_ok} tri=${cmp.triangleTotal_ok} min=${cmp.min_ok} max=${cmp.max_ok} extents=${cmp.extents_ok} maxAxis=${cmp.maxAxis_ok} (mine=${mine.maxAxisExtent}) identityTRS=${cmp.identityTrs_confirmed} => ${ok ? 'COUNTERCHECK_PASS' : 'COUNTERCHECK_FAIL'}`);
}
results.allOk = allOk;
results.toleranceStatement = 'published values are rounded to 2 decimal places; tolerance 0.01 covers the print rounding; raw float32 values compared directly where available';
writeFileSync(join(PKG, '00_CONTROL_INTERNAL_QC', 'QC8_BOUNDS_COUNTERCHECK.json'), JSON.stringify(results, null, 1));
console.log('ALL_OK=' + allOk);
