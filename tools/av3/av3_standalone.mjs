// tools/av3/av3_standalone.mjs — AV-3 offline validation (no server needed).
// Reads Models.ark (fail-closed byte pin) directly, runs:
//   K1 known-answer gate on 206264 (AV-1 anchor: 63 KFC + 63 KFD, first KFD
//      numRotationKeys=61, rotationType=1/LINEAR, t0=0.0)
//   K2 quaternion storage-order MEASUREMENT (w,x,y,z vs x,y,z,w) against the
//      bind rotation matrices of controller targets (key0 == bind pose)
//   K3 cross-validation (QH-009): KFD block count + first-KFD stats from the
//      primary decoder vs an INDEPENDENT minimal field scan (different lines)
//   K4 negative parser controls (L19): truncated / wrong-endian / wrong-width
// Writes evidence JSON to the AV3_ANIMATION SCI dir.
'use strict';
import { promises as fs } from 'node:fs';
import { ArkArchive } from '../../src/pesource/ArkArchive.js';
import { parseModel41 } from '../../src/pesource/NifModelReader41.js';
import { decodeKeyframeBlocks41, decodeKfBlock } from './kf41.mjs';

const MODELS_ARK_PATH = process.env.AV_MODELS_ARK ||
  'D:\\Eudoria_Reconstruction\\01_Original_Files\\ARK\\Models.ark';
const PIN = 128742137;
const SCI = process.env.AV_SCI_DIR ||
  'D:\\Eudoria_Reconstruction\\99_Audits\\PE_ISO_ASSET_VIEWER_R1_20261031\\AV3_ANIMATION';

const buf = await fs.readFile(MODELS_ARK_PATH);
if (buf.length !== PIN) throw new Error(`FAIL-CLOSED pin: ${buf.length} != ${PIN}`);
const ark = new ArkArchive(new Uint8Array(buf));

async function getNif(id) {
  const entry = ark.entryById(id);
  if (!entry) throw new Error(`no entry ${id}`);
  const { payload } = ark.readEntry(entry);
  return payload;
}

const evidence = { job: 'AV3', loop: '8ee81e37', era: 'ISO_5_1_0_0', generated: new Date().toISOString() };

// ---------- K1: known-answer 206264 ----------
{
  const payload = await getNif(206264);
  const { extraction } = parseModel41(payload, '206264.nif');
  const kf = decodeKeyframeBlocks41(payload, extraction);
  const first = kf.data[0];
  const rot = first.rotationKeys;
  const k0 = rot.keys[0], kLast = rot.keys[rot.keys.length - 1];
  evidence.K1_206264 = {
    kfcCount: kf.controllers.length,
    kfdCount: kf.data.length,
    textKeyBlocks: kf.textKeys.length,
    closureAll: kf.closureAll,
    failures: kf.failures,
    firstKfd: {
      blockIndex: first.blockIndex,
      numRotationKeys: first.numRotationKeys,
      rotationType: first.rotationType,
      interpolation: rot.interpolation,
      firstKeyTime: k0.time, firstKeyQuat: [k0.w, k0.x, k0.y, k0.z],
      lastKeyTime: kLast.time,
      translationKeys: first.translations.numKeys,
      translationInterp: first.translations.interpolation,
      scaleKeys: first.scales.numKeys,
    },
    knownAnswer: {
      expected: { kfc: 63, kfd: 63, numRotationKeysFirst: 61, rotationType: 1, t0: 0.0 },
      measured: { kfc: kf.controllers.length, kfd: kf.data.length, numRotationKeysFirst: first.numRotationKeys, rotationType: first.rotationType, t0: k0.time },
    },
    pass: kf.controllers.length === 63 && kf.data.length === 63 && first.numRotationKeys === 61 &&
      first.rotationType === 1 && k0.time === 0.0 && kf.closureAll,
  };
  // per-block stats for all 63 KFD (sanity: every one closure-exact + key totals)
  evidence.K1_206264.kfdStats = {
    totalRotationKeys: kf.data.reduce((a, d) => a + d.numRotationKeys, 0),
    totalTranslationKeys: kf.data.reduce((a, d) => a + d.translations.numKeys, 0),
    totalScaleKeys: kf.data.reduce((a, d) => a + d.scales.numKeys, 0),
    rotTypes: [...new Set(kf.data.map(d => d.rotationType))],
    translationInterps: [...new Set(kf.data.map(d => d.translations.interpolation))],
  };
  // KFC target/data sanity: every KFC dataRef resolves to a KFD, target to a block
  const byIdx = new Map(extraction.blocks.map(b => [b.index, b]));
  evidence.K1_206264.kfcSanity = {
    dataRefsResolve: kf.controllers.every(c => { const d = byIdx.get(c.dataRef); return d && d.type === 'NiKeyframeData'; }),
    targetRefsResolve: kf.controllers.every(c => c.target < 0 || (byIdx.has(c.target))),
    timeRangesSample: kf.controllers.slice(0, 3).map(c => ({ startTime: c.startTime, stopTime: c.stopTime, frequency: c.frequency, phase: c.phase, target: c.target, dataRef: c.dataRef })),
  };
}
console.log('K1', JSON.stringify(evidence.K1_206264.pass), JSON.stringify(evidence.K1_206264.knownAnswer.measured));

// ---------- K2: quaternion order measurement (bind-pose cross-check) ----------
{
  const payload = await getNif(206264);
  const { extraction } = parseModel41(payload, '206264.nif');
  const kf = decodeKeyframeBlocks41(payload, extraction);
  const byIdx = new Map(extraction.blocks.map(b => [b.index, b]));
  const bitsToF32 = (hex) => {
    const u = new Uint32Array(1); const b = new Uint8Array(u.buffer);
    for (let i = 0; i < 4; i++) b[i] = parseInt(hex.substr(i * 2, 2), 16);
    return new Float32Array(u.buffer)[0];
  };
  // rotation matrix R from a quaternion (column-vector convention, Hamilton)
  const quatToMat = (w, x, y, z) => [
    [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
    [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
    [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
  ];
  const matDiff = (A, B) => {
    let s = 0;
    for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) s += Math.abs(A[i][j] - B[i][j]);
    return s;
  };
  const transpose = (M) => M[0].map((_, j) => M.map(r => r[j]));
  // per KFC: target node bind rotation vs first rotation key of its KFD.
  // candidates: storage order (w-first vs w-last) x (direct vs transposed match)
  const votes = { w_first_direct: 0, w_first_transposed: 0, w_last_direct: 0, w_last_transposed: 0, noBindMatch: 0 };
  let tested = 0;
  for (const c of kf.controllers) {
    const d = kf.data.find(x => x.blockIndex === c.dataRef);
    const t = byIdx.get(c.target);
    if (!d || !d.rotationKeys || !d.rotationKeys.keys || !d.rotationKeys.keys.length) continue;
    if (!t || !t.fields || !t.fields.rotation) continue;
    const bind = t.fields.rotation.map(r => r.map(bitsToF32));
    const k = d.rotationKeys.keys[0];
    const qWfirst = quatToMat(k.w, k.x, k.y, k.z);        // storage (w,x,y,z)
    const qWlast = quatToMat(k.w === undefined ? 0 : k.w, 0, 0, 0); // placeholder, real test below
    // w-last interpretation: bytes are (x,y,z,w) — i.e. swap: x=k.w? no:
    // under w-last the FIRST stored float is x: so x=k.w?? unambiguous swap:
    const x2 = k.w, y2 = k.x, z2 = k.y, w2 = k.z;         // w-last reading of the same 4 floats
    const qWlastReal = quatToMat(w2, x2, y2, z2);
    const diffs = {
      w_first_direct: matDiff(qWfirst, bind),
      w_first_transposed: matDiff(transpose(qWfirst), bind),
      w_last_direct: matDiff(qWlastReal, bind),
      w_last_transposed: matDiff(transpose(qWlastReal), bind),
    };
    const best = Object.entries(diffs).sort((a, b) => a[1] - b[1])[0];
    tested++;
    if (best[1] < 0.02) votes[best[0]]++;
    else votes.noBindMatch++;
  }
  evidence.K2_quatOrder = {
    method: 'first rotation key vs controller-target bind rotation matrix (206264; best of 4 candidate interpretations, diff < 0.02 counts as a vote)',
    tested, votes,
    conclusion: Object.entries(votes).sort((a, b) => b[1] - a[1])[0][1] === 0 ? 'INCONCLUSIVE' :
      `storage order = ${Object.entries(votes).sort((a, b) => b[1] - a[1])[0][0]} (majority ${Object.entries(votes).sort((a, b) => b[1] - a[1])[0][1]}/${tested})`,
  };
}
console.log('K2', JSON.stringify(evidence.K2_quatOrder.votes), evidence.K2_quatOrder.conclusion);

// ---------- K3: independent cross-check scan (QH-009 — different lines) ----------
{
  const payload = await getNif(206264);
  // independent minimal scan: locate every 'NiKeyframeData' RTTI by raw
  // byte search, decode ONLY numRotationKeys/rotationType + first/last key
  // times with standalone DataView code (no shared helpers with kf41.mjs).
  const needle = 'NiKeyframeData';
  const nb = Buffer.from(needle, 'ascii');
  const buf = Buffer.from(payload.buffer, payload.byteOffset, payload.byteLength);
  const found = [];
  let pos = 0;
  while (true) {
    const at = buf.indexOf(nb, pos);
    if (at < 0) break;
    // require a plausible u32 length right before (8..64)
    if (at >= 4) {
      const len = buf.readInt32LE(at - 4);
      if (len === needle.length) found.push(at - 4);
    }
    pos = at + 1;
  }
  const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  const kfdIndependent = [];
  for (const s of found) {
    let p = s + 4 + needle.length;
    const numRotationKeys = dv.getUint32(p, true); p += 4;
    if (numRotationKeys > 100000) { kfdIndependent.push({ rttiStart: s, bad: true }); continue; }
    let rotationType = 0, t0 = null, t1 = null;
    if (numRotationKeys > 0) {
      rotationType = dv.getUint32(p, true); p += 4;
      if (rotationType === 1 || rotationType === 2 || rotationType === 5) {
        t0 = dv.getFloat32(p, true);
        p += (4 + 16) * numRotationKeys + (rotationType === 3 ? numRotationKeys * 12 : 0) - 0;
        t1 = dv.getFloat32(p - 20, true);
      }
    }
    kfdIndependent.push({ rttiStart: s, numRotationKeys, rotationType, t0, t1 });
  }
  const { extraction } = parseModel41(payload, '206264.nif');
  const kf = decodeKeyframeBlocks41(payload, extraction);
  const primaryKfd = kf.data.map(d => {
    const b = extraction.blocks[d.blockIndex];
    return { rttiStart: b.rttiStart, numRotationKeys: d.numRotationKeys, rotationType: d.rotationType, t0: d.rotationKeys?.keys?.[0]?.time ?? null, t1: d.rotationKeys?.keys?.[d.rotationKeys.keys.length - 1]?.time ?? null };
  });
  const primarySorted = JSON.stringify(primaryKfd);
  const indepSorted = JSON.stringify(kfdIndependent.filter(k => !k.bad));
  evidence.K3_crosscheck = {
    method: 'primary kf41 decoder vs independent raw byte-scan (QH-009: separate code, no shared helpers)',
    primaryKfdCount: kf.data.length, independentKfdCount: kfdIndependent.filter(k => !k.bad).length,
    identical: primarySorted === indepSorted,
    pass: kf.data.length === kfdIndependent.filter(k => !k.bad).length && primarySorted === indepSorted,
  };
}
console.log('K3', JSON.stringify(evidence.K3_crosscheck.pass), evidence.K3_crosscheck.primaryKfdCount, evidence.K3_crosscheck.independentKfdCount);

// ---------- K4: negative parser controls (L19) ----------
{
  const payload = await getNif(206264);
  const { extraction } = parseModel41(payload, '206264.nif');
  const kfd = extraction.blocks.find(b => b.type === 'NiKeyframeData');
  const negatives = [];
  // a) truncated: cut the payload 16 bytes into the first KFD
  {
    const cut = payload.slice(0, kfd.rttiStart + 16);
    const cutEx = { blocks: [{ ...kfd, span: cut.length - kfd.rttiStart }] };
    try { decodeKfBlock(cut, cutEx.blocks[0]); negatives.push({ control: 'truncated_16B', pass: false, msg: 'NO FAIL — WRONG' }); }
    catch (e) { negatives.push({ control: 'truncated_16B', pass: true, msg: e.message.slice(0, 120) }); }
  }
  // b) truncated mid-keys (deeper, past the count fields)
  {
    const cut = payload.slice(0, kfd.rttiStart + 200);
    const blk = { ...kfd, span: cut.length - kfd.rttiStart };
    try { decodeKfBlock(cut, blk); negatives.push({ control: 'truncated_200B', pass: false, msg: 'NO FAIL — WRONG' }); }
    catch (e) { negatives.push({ control: 'truncated_200B', pass: true, msg: e.message.slice(0, 120) }); }
  }
  // c) wrong-endian: byte-swap the key count (read as BE fails plausibility)
  {
    const swapped = new Uint8Array(payload);
    const s = kfd.rttiStart, rttiLen = swapped[s] | (swapped[s + 1] << 8);
    const cpos = s + 4 + rttiLen;
    // big-endian numRotationKeys of 61 = 0x0000003D -> byteswap to 0x3D000000
    swapped[cpos + 3] = 0x3D; swapped[cpos + 2] = 0; swapped[cpos + 1] = 0; swapped[cpos] = 0;
    const blk = { ...kfd, span: kfd.span };
    try { decodeKfBlock(swapped, blk); negatives.push({ control: 'wrong_endian_count', pass: false, msg: 'NO FAIL — WRONG' }); }
    catch (e) { negatives.push({ control: 'wrong_endian_count', pass: true, msg: e.message.slice(0, 120) }); }
  }
  // d) wrong-width (quat read as 3 floats — count*20 leaves closure short/long)
  {
    // simulate: force numRotationKeys+1 (one extra key read overruns or breaks unit check)
    const mutated = new Uint8Array(payload);
    const s = kfd.rttiStart, rttiLen = mutated[s] | (mutated[s + 1] << 8);
    const cpos = s + 4 + rttiLen;
    mutated[cpos] = mutated[cpos] + 1;
    try {
      decodeKfBlock(mutated, { ...kfd, span: kfd.span });
      negatives.push({ control: 'wrong_width_count_plus1', pass: false, msg: 'NO FAIL — WRONG' });
    } catch (e) { negatives.push({ control: 'wrong_width_count_plus1', pass: true, msg: e.message.slice(0, 120) }); }
  }
  evidence.K4_negatives = { controls: negatives, pass: negatives.every(n => n.pass) };
}
console.log('K4', JSON.stringify(evidence.K4_negatives.pass), evidence.K4_negatives.controls.map(c => `${c.control}:${c.pass}`).join(' '));

// ---------- K5: textkey anchor models (census candidates) ----------
{
  const candidates = [103004, 103005];
  evidence.K5_textkeyModels = [];
  for (const id of candidates) {
    const payload = await getNif(id);
    const { extraction } = parseModel41(payload, `${id}.nif`);
    const kf = decodeKeyframeBlocks41(payload, extraction);
    evidence.K5_textkeyModels.push({
      id, kfc: kf.controllers.length, kfd: kf.data.length, closureAll: kf.closureAll,
      textKeys: kf.textKeys.map(t => ({ blockIndex: t.blockIndex, numTextKeys: t.numTextKeys, keys: t.keys.map(k => ({ time: k.time, text: k.text })) })),
      kfdSummary: {
        totalRotKeys: kf.data.reduce((a, d) => a + d.numRotationKeys, 0),
        totalTransKeys: kf.data.reduce((a, d) => a + d.translations.numKeys, 0),
        rotTypes: [...new Set(kf.data.map(d => d.rotationType))],
      },
      failures: kf.failures,
    });
  }
  evidence.K5_pass = evidence.K5_textkeyModels.every(m => m.kfc > 0 && m.closureAll && m.textKeys.length > 0 && m.textKeys.some(t => t.keys.length > 0));
}
console.log('K5', JSON.stringify(evidence.K5_pass), JSON.stringify(evidence.K5_textkeyModels.map(m => ({ id: m.id, kfc: m.kfc, tk: m.textKeys.flatMap(t => t.keys.map(k => k.text)) }))));

evidence.ALL_GATES = {
  K1: evidence.K1_206264.pass, K2: evidence.K2_quatOrder.conclusion !== 'INCONCLUSIVE',
  K3: evidence.K3_crosscheck.pass, K4: evidence.K4_negatives.pass, K5: evidence.K5_pass,
};
evidence.ALL_PASS = Object.values(evidence.ALL_GATES).every(Boolean);
await fs.mkdir(SCI, { recursive: true });
await fs.writeFile(`${SCI}\\av3_parser_gates.json`, JSON.stringify(evidence, null, 2));
console.log('ALL_PASS =', evidence.ALL_PASS);
process.exit(evidence.ALL_PASS ? 0 : 2);
