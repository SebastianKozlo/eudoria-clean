// corpus_final.mjs — AV-5 CORPUS CLOSURE (era ISO_5_1_0_0, denominator = ALL
// Models.ark members). Read-only. Final counts: renderable, with-textures,
// animated (KF playable), skinned — plus STOPPED/PARSE_FAIL and the honest
// UNSUPPORTED counters. Includes the 146710/146749 texture closure-FAIL
// 8B-diff diagnosis attempt.
'use strict';
import { promises as fs } from 'node:fs';
import { dirname } from 'node:path';
import { ArkArchive } from '../../src/pesource/ArkArchive.js';
import { parseModel41 } from '../../src/pesource/NifModelReader41.js';
import { parseModel40 } from '../../src/pesource/NifModelReader40.js';
import { decodeKeyframeBlocks41 } from '../av3/kf41.mjs';
import { decodeSkinBlocks41, buildSkinBinding } from './skin41.mjs';

const MODELS = 'D:\\Eudoria_Reconstruction\\01_Original_Files\\ARK\\Models.ark';
const TEXTURES = 'D:\\Eudoria_Reconstruction\\01_Original_Files\\ARK\\Textures.ark';
const OUT = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_ISO_ASSET_VIEWER_R1_20261031\\AV5_INTEGRATION\\CORPUS_FINAL.json';

const mbuf = new Uint8Array(await fs.readFile(MODELS));
const ark = new ArkArchive(mbuf);
const tbuf = new Uint8Array(await fs.readFile(TEXTURES));
const tark = new ArkArchive(tbuf);

// ---- 146710/146749 8B-diff diagnosis ----
function diagTexture(id) {
  const entry = tark.entryById(id);
  if (!entry) return { id, status: 'NOT_IN_TEXTURES_ARK' };
  const { payload } = tark.readEntry(entry);
  const head = Array.from(payload.subarray(0, 32)).map(b => b.toString(16).padStart(2, '0')).join(' ');
  return { id, name: entry.name, size: entry.size, headHex: head };
}

const acc = {
  total: 0, byVersion: {}, renderable: 0, withTextures: 0, animated: 0, skinned: 0,
  animatedSkinned: 0, unsupported: {}, parseThrow: 0, stopped: 0, texJoinFailExamples: {},
  kfPlayable: 0, skinClosureFail: 0, skinBindOk: 0, renderable41: 0, renderable40: 0,
  animated41: 0, animated40: 0, skinnedCount: 0, maxInflHist: {},
};
const failures = [];
for (const e of ark.entries()) {
  acc.total++;
  const { payload } = ark.readEntry(e);
  const nl = payload.indexOf(0x0a);
  if (nl < 0) { acc.unsupported.NO_NIF_HEADER = (acc.unsupported.NO_NIF_HEADER ?? 0) + 1; continue; }
  const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  const ver = dv.getUint32(nl + 1, true);
  let vLabel = '0x' + ver.toString(16);
  try {
    let extraction, renderModel, parseFn;
    if (ver === 0x0401000C) { vLabel = '4.1.0.12'; parseFn = parseModel41; }
    else if (ver === 0x04000000) { vLabel = '4.0.0.0'; parseFn = parseModel40; }
    else if (ver === 0x04000002) { vLabel = '4.0.0.2'; parseFn = parseModel40; }
    else {
      acc.unsupported['UNSUPPORTED_VERSION_' + vLabel] = (acc.unsupported['UNSUPPORTED_VERSION_' + vLabel] ?? 0) + 1;
      continue;
    }
    acc.byVersion[vLabel] = (acc.byVersion[vLabel] ?? 0) + 1;
    ({ extraction, renderModel } = parseFn(payload, e.name));
    const status = extraction.parseStatus ?? 'PASS';
    if (status !== 'PASS') acc.stopped++;
    const renderable = renderModel.shapes.length > 0 && (status === 'PASS' || renderModel.shapes.length > 0);
    if (renderable) { acc.renderable++; vLabel.startsWith('4.0') ? acc.renderable40++ : acc.renderable41++; }
    // textures: NiArkTextureExtraData records resolving into Textures.ark
    let withTex = false, texJoins = 0, texOk = 0;
    for (const b of extraction.blocks) {
      if (b.type === 'NiArkTextureExtraData' && !b.fields) {
        // structural anchored records (server parity, minimal)
        const ids = extractIds(payload, b);
        texJoins += ids.length;
        for (const id of ids) if (id >= 0 && tark.entryById(id)) { texOk++; withTex = true; }
      }
    }
    if (renderable && withTex) acc.withTextures++;
    // animation: KF closure-exact controllers with resolvable target+data
    const kf = decodeKeyframeBlocks41(payload, extraction);
    let animated = false;
    if (kf.closureAll && kf.controllers.length) {
      const dataIdx = new Set(kf.data.map(d => d.blockIndex));
      const nodes = new Set(extraction.blocks.filter(b => (b.type === 'NiNode' || b.type === 'NiTriShape') && b.fields).map(b => b.index));
      for (const c of kf.controllers) {
        if (nodes.has(c.target) && dataIdx.has(c.dataRef)) { animated = true; break; }
      }
    }
    if (renderable && animated) { acc.animated++; vLabel.startsWith('4.0') ? acc.animated40++ : acc.animated41++; }
    // skinning (4.1 layout only)
    let skinned = false;
    if (vLabel === '4.1.0.12') {
      const skin = decodeSkinBlocks41(payload, extraction);
      if (!skin.closureAll) acc.skinClosureFail++;
      if (skin.instances.length && skin.closureAll) {
        for (const sh of renderModel.shapes) {
          if (sh.skinRef < 0) continue;
          const bind = buildSkinBinding(skin, sh);
          if (bind.ok) {
            skinned = true; acc.skinBindOk++;
            acc.maxInflHist[bind.stats.maxInfluencesPerVertex] = (acc.maxInflHist[bind.stats.maxInfluencesPerVertex] ?? 0) + 1;
          }
        }
      }
      if (renderable && skinned) { acc.skinned++; if (animated) acc.animatedSkinned++; }
    }
  } catch (err) {
    acc.parseThrow++;
    if (failures.length < 20) failures.push({ id: e.name, ver: vLabel, reason: String(err.message ?? err).slice(0, 140) });
  }
}

// server-parity anchored Ark texture id extraction (from decodeArkTextureRecords)
function extractIds(payload, block) {
  const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  const start = block.rttiStart, end = block.rttiStart + block.span;
  const out = [];
  const isMarker = (p) => p + 4 <= end && payload[p] === 0xff && payload[p + 1] === 0xff && payload[p + 2] === 0xff && payload[p + 3] === 0xff;
  const printable = (b) => b >= 0x20 && b < 0x7f;
  const rttiLen = dv.getInt32(start, true);
  if (rttiLen < 1 || rttiLen > 256) return out;
  let c = start + 4 + rttiLen;
  const names = [];
  while (c + 8 < end) {
    const len = dv.getInt32(c, true);
    if (len >= 4 && len <= 256 && c + 4 + len < end) {
      let ok = true;
      for (let i = 0; i < len; i++) if (!printable(payload[c + 4 + i])) { ok = false; break; }
      if (ok) {
        const nameEnd = c + 4 + len;
        let near = false;
        for (let m = nameEnd; m < nameEnd + 16 && m + 4 <= end; m++) if (isMarker(m)) { near = true; break; }
        if (near) { names.push({ namePos: c, nameEnd }); c = nameEnd + 4; continue; }
      }
    }
    c++;
  }
  for (let i = 0; i < names.length; i++) {
    const regionStart = names[i].nameEnd;
    const regionEnd = i + 1 < names.length ? names[i + 1].namePos : end;
    let lastMarker = -1;
    for (let m = regionStart; m + 8 <= regionEnd; m++) if (isMarker(m) && m + 8 <= end) lastMarker = m;
    if (lastMarker >= 0) out.push(dv.getUint32(lastMarker + 4, true));
  }
  return out;
}

const result = { era: 'ISO_5_1_0_0', denominator: acc.total, counts: acc,
  texClosureFailDiagnosis: { a: diagTexture(146710), b: diagTexture(146749) },
  parseFailures: failures };
console.log(JSON.stringify(result, null, 2));
try {
  await fs.mkdir(dirname(OUT), { recursive: true });
  await fs.writeFile(OUT, JSON.stringify(result, null, 2));
  console.log('written', OUT);
} catch (e) { console.error('SCI write failed:', e.message); }
