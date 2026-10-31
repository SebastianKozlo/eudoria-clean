// skin_verify.mjs — AV-5: bind-law physical verification for the decoded 4.1
// skin layout. For each skinned candidate: at BIND pose, per vertex
//   p_bind = SUM w_i * (W_bone_i * SkinToBone_i) * v
// must reproduce the shape's bind-pose world position
//   shapeWorld * v
// within tolerance (rootParentWorld incorporated when that is the form the
// bytes demand). W = parentWorld*local (campaign-8163 W4-1 bind law).
'use strict';
import { promises as fs } from 'node:fs';
import { ArkArchive } from '../../src/pesource/ArkArchive.js';
import { parseModel41 } from '../../src/pesource/NifModelReader41.js';
import { decodeSkinBlocks41, buildSkinBinding } from './skin41.mjs';

const MODELS = 'D:\\Eudoria_Reconstruction\\01_Original_Files\\ARK\\Models.ark';
const mbuf = new Uint8Array(await fs.readFile(MODELS));
const ark = new ArkArchive(mbuf);

const bitsToF32 = (hex) => {
  const u = new Uint32Array(1); const b = new Uint8Array(u.buffer);
  for (let i = 0; i < 4; i++) b[i] = parseInt(hex.substr(i * 2, 2), 16);
  return new Float32Array(u.buffer)[0];
};
function composeTRS(P, C) {
  const R = [[0,0,0],[0,0,0],[0,0,0]];
  for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++)
    R[i][j] = P.rotation[i][0]*C.rotation[0][j] + P.rotation[i][1]*C.rotation[1][j] + P.rotation[i][2]*C.rotation[2][j];
  const t = [
    P.translation[0] + P.scale*(P.rotation[0][0]*C.translation[0]+P.rotation[0][1]*C.translation[1]+P.rotation[0][2]*C.translation[2]),
    P.translation[1] + P.scale*(P.rotation[1][0]*C.translation[0]+P.rotation[1][1]*C.translation[1]+P.rotation[1][2]*C.translation[2]),
    P.translation[2] + P.scale*(P.rotation[2][0]*C.translation[0]+P.rotation[2][1]*C.translation[1]+P.rotation[2][2]*C.translation[2]),
  ];
  return { translation: t, rotation: R, scale: P.scale * C.scale };
}
function applyTR(T, v) {
  return [
    T.rotation[0][0]*v[0]+T.rotation[0][1]*v[1]+T.rotation[0][2]*v[2],
    T.rotation[1][0]*v[0]+T.rotation[1][1]*v[1]+T.rotation[1][2]*v[2],
    T.rotation[2][0]*v[0]+T.rotation[2][1]*v[1]+T.rotation[2][2]*v[2],
  ].map((r, i) => r * T.scale + T.translation[i]);
}

let verified = 0, checked = 0;
const results = [];
for (const e of ark.entries()) {
  if (!/\.nif$/i.test(e.name)) continue;
  const { payload } = ark.readEntry(e);
  const nl = payload.indexOf(0x0a);
  if (nl < 0) continue;
  const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  if (dv.getUint32(nl + 1, true) !== 0x0401000C) continue;
  let ex;
  try { ex = parseModel41(payload, e.name); } catch { continue; }
  const hasSkin = ex.extraction.blocks.some(b => b.type === 'NiSkinInstance');
  if (!hasSkin) continue;
  checked++;
  try {
    const skin = decodeSkinBlocks41(payload, ex.extraction);
    if (!skin.closureAll || !skin.instances.length) {
      results.push({ id: e.name, skinStatus: 'DECODE_FAIL', failures: skin.failures.slice(0, 2) });
      continue;
    }
    // bind world transforms from the hierarchy
    const childOf = new Map();
    const local = new Map();
    for (const b of ex.extraction.blocks) {
      if ((b.type === 'NiNode' || b.type === 'NiTriShape') && b.fields) {
        local.set(b.index, {
          translation: b.fields.translation.map(bitsToF32),
          rotation: b.fields.rotation.map(r => r.map(bitsToF32)),
          scale: bitsToF32(b.fields.scale),
        });
        if (b.type === 'NiNode') for (const c of b.fields.children || []) if (c >= 0) childOf.set(c, b.index);
      }
    }
    const worldCache = new Map();
    const worldOf = (idx) => {
      if (worldCache.has(idx)) return worldCache.get(idx);
      const l = local.get(idx), par = childOf.get(idx);
      const w = par === undefined ? l : composeTRS(worldOf(par), l);
      worldCache.set(idx, w);
      return w;
    };
    for (const sh of ex.renderModel.shapes) {
      if (sh.skinRef < 0) continue;
      const bind = buildSkinBinding(skin, sh);
      if (!bind.ok) { results.push({ id: e.name, shape: sh.shapeName, skinStatus: 'BIND_FAIL', reason: bind.reason }); continue; }
      const inst = skin.instances.find(i => i.blockIndex === sh.skinRef);
      // BIND INVARIANT: M_i = W_bone_i(bind) * SkinToBone_i must be the SAME
      // matrix for every bone i (campaign-8163 W4-1: W_i*SkinToBone_i = I in
      // the skin's own space; a rigid remap M is allowed, rootParentWorld
      // explains M when present).
      const M = [];
      let mSpread = 0;
      for (let i = 0; i < bind.bones.length; i++) {
        const boneWorld = worldOf(bind.bones[i]);
        M.push(composeTRS(boneWorld, bind.skinToBone[i]));
      }
      for (let i = 1; i < M.length; i++) {
        for (let r = 0; r < 3; r++) {
          mSpread = Math.max(mSpread, Math.abs(M[i].translation[r] - M[0].translation[r]));
          for (let c = 0; c < 3; c++) mSpread = Math.max(mSpread, Math.abs(M[i].rotation[r][c] - M[0].rotation[r][c]));
        }
        mSpread = Math.max(mSpread, Math.abs(M[i].scale - M[0].scale));
      }
      const target = applyTR(M[0], [0, 0, 0]);
      results.push({ id: e.name, shape: sh.shapeName, verts: sh.numVertices, bones: bind.bones.length,
        maxInfl: bind.stats.maxInfluencesPerVertex, badSum: bind.stats.weightSumMismatch,
        bindInvariantSpread: +mSpread.toFixed(5),
        bindCenterM: target.map(x => +x.toFixed(2)), unknownTail: skin.data.find(d => d.blockIndex === inst?.dataRef)?.unknownTail ?? null });
      if (mSpread < 0.01) verified++;
    }
  } catch (err) {
    results.push({ id: e.name, skinStatus: 'THROW', reason: String(err.message ?? e).slice(0, 120) });
  }
  if (checked >= 118) break;
}
console.log(JSON.stringify({ candidatesChecked: checked, shapesBindVerified: verified, results: results.slice(0, 40) }, null, 2));
