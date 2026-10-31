// tools/av3/kf41.mjs — AV-3 (PE_ISO_ASSET_VIEWER campaign, job AV3_ANIMATION,
// loop 8ee81e37, era ISO_5_1_0_0 / NIF 4.1.0.12), 2026-10-31.
//
// CLOSURE-EXACT decoder for the three NIF 4.1 animation block types that the
// W09 R1 adapter records as OPAQUE (anchored RTTI boundary, no invented
// structure):
//   NiKeyframeController, NiKeyframeData, NiTextKeyExtraData.
//
// LAYOUT BASIS (docs/nif/05-controllers-data.md, CONFIRMED C12-B/C11 lineage;
// re-verified HERE from bytes against the AV-1 anchor 206264 + closure checks):
//   NiKeyframeController = NiTimeController base
//     [nextController i32][flags u16][frequency f32][phase f32]
//     [startTime f32][stopTime f32][target i32] + [dataRef i32]
//   NiKeyframeData (rotationType != 4, quaternion path — the corpus case):
//     [numRotationKeys u32][rotationType u32]
//     per key: [time f32][quat w,x,y,z f32]  (+t,b,c f32 if TBC)
//     [translations: numKeys u32][interp u32 if numKeys>0]
//     per key: [time f32][vec3 f32] (+fwd,bwd vec3 if QUAD)(+t,b,c if TBC)
//     [scales: numKeys u32][interp u32 if numKeys>0]
//     per key: [time f32][f32] (+fwd,bwd if QUAD)(+t,b,c if TBC)
//   NiTextKeyExtraData (v4): [nextExtraData i32 (NiExtraData link, NO name —
//     name is a 10.0.1.0 addition)][unknownInt1 u32][numTextKeys u32]
//     per key: [time f32][text SizedString]
//   KeyType enum: 1=LINEAR 2=QUADRATIC 3=TBC 4=XYZ-euler 5=CONST(as LINEAR)
//   Quaternion storage order (w,x,y,z — old-NIF convention) is VERIFIED
//   physically in av3_standalone.mjs against bind rotation matrices
//   (key0 == bind pose on the corpus) — see QUAT_ORDER_MEASUREMENT in SCI.
//
// CLOSURE GATE: every decoded block must consume EXACTLY its opaque span
// (blockEnd from the anchored RTTI boundary). Any overrun/underrun is a LOUD
// per-block FAIL — recorded, never silently accepted.
'use strict';

const QUAT_OK = 1e-3; // |1 - |q|| tolerance for unit-quaternion check

function unit(n) { return n === null ? null : { value: n }; }

/** Decode one OPAQUE block span starting at rttiStart. Returns
 * { fields, consumed } where consumed = bytes eaten AFTER the RTTI sized
 * string (must equal span - rttiLen - 4). Throws loud on layout mismatch. */
export function decodeKfBlock(payload, block) {
  const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  const start = block.rttiStart;
  const end = start + block.span;
  const rttiLen = dv.getInt32(start, true);
  if (rttiLen < 1 || rttiLen > 256) throw new Error(`bad rttiLen ${rttiLen}`);
  let p = start + 4 + rttiLen;
  const need = (n) => { if (p + n > end) throw new Error(`overrun: need ${n}B at ${p}, block end ${end}`); };
  const i32 = () => { need(4); const v = dv.getInt32(p, true); p += 4; return v; };
  const u32 = () => { need(4); const v = dv.getUint32(p, true); p += 4; return v; };
  const u16 = () => { need(2); const v = dv.getUint16(p, true); p += 2; return v; };
  const f32 = () => { need(4); const v = dv.getFloat32(p, true); p += 4; return v; };
  const sizedString = () => {
    const len = i32();
    if (len < 0 || len > 65536) throw new Error(`bad string length ${len}`);
    need(len);
    let s = '';
    for (let i = 0; i < len; i++) s += String.fromCharCode(payload[p + i]);
    p += len;
    return s;
  };
  const guard = (n, what) => { if (n > 100000 || n < 0) throw new Error(`impossible ${what} ${n}`); };

  // ---- keygroup readers (mirrors of the C20 CONFIRMED KeyGroup shape) ----
  const readInterpKeys = (readValue, extraPerInterp) => {
    const numKeys = u32(); guard(numKeys, 'numKeys');
    if (numKeys === 0) return { numKeys: 0, interpolation: 0, keys: [] };
    let interp = u32();
    const interpRaw = interp;
    if (interp === 5) interp = 1; // CONST -> LINEAR (C20 canon)
    if (interp !== 1 && interp !== 2 && interp !== 3) throw new Error(`unsupported key interpolation ${interpRaw}`);
    const keys = [];
    for (let i = 0; i < numKeys; i++) {
      const time = f32();
      const value = readValue();
      const key = { time, value };
      if (interp === 2) { key.forward = extraPerInterp(); key.backward = extraPerInterp(); }
      else if (interp === 3) { key.tension = f32(); key.bias = f32(); key.continuity = f32(); }
      keys.push(key);
    }
    return { numKeys, interpolation: interpRaw, keys };
  };

  let fields;
  if (block.type === 'NiKeyframeController') {
    fields = {
      nextController: i32(), flags: u16(), frequency: f32(), phase: f32(),
      startTime: f32(), stopTime: f32(), target: i32(), dataRef: i32(),
    };
  } else if (block.type === 'NiKeyframeData') {
    const numRotationKeys = u32(); guard(numRotationKeys, 'numRotationKeys');
    let rotationType = 0, rotationKeys = null;
    if (numRotationKeys !== 0) {
      rotationType = u32();
      if (rotationType === 4) {
        // XYZ-euler path (doc C12-B: PE extra unknownFloat f32 + 3 f32 axis
        // keygroups). Rare in this corpus; treated with the same strictness.
        const unknownFloat = f32();
        const axes = [0, 1, 2].map(() => readInterpKeys(f32, f32));
        rotationKeys = { unknownFloat, axes };
      } else {
        let interp = rotationType;
        const interpRaw = interp;
        if (interp === 5) interp = 1;
        if (interp !== 1 && interp !== 2 && interp !== 3) throw new Error(`unsupported rotationType ${interpRaw}`);
        const keys = [];
        for (let i = 0; i < numRotationKeys; i++) {
          const time = f32();
          const w = f32(), x = f32(), y = f32(), z = f32();
          const key = { time, w, x, y, z };
          if (interp === 3) { key.tension = f32(); key.bias = f32(); key.continuity = f32(); }
          else if (interp === 2) { /* QUAT quadratic forced LINEAR — no tangents (doc) */ }
          const norm = Math.hypot(w, x, y, z);
          if (!Number.isFinite(norm) || Math.abs(1 - norm) > QUAT_OK * 20) {
            throw new Error(`non-unit quaternion at key ${i} (|q|=${norm}) — likely wrong layout`);
          }
          keys.push(key);
        }
        rotationKeys = { interpolation: interpRaw, keys };
      }
    }
    const translations = readInterpKeys(() => [f32(), f32(), f32()], () => [f32(), f32(), f32()]);
    const scales = readInterpKeys(f32, f32);
    fields = { numRotationKeys, rotationType, rotationKeys, translations, scales };
  } else if (block.type === 'NiTextKeyExtraData') {
    const nextExtraData = i32(); // v4 NiExtraData base: link, NO name
    const unknownInt1 = u32();   // v4-only
    const numTextKeys = u32(); guard(numTextKeys, 'numTextKeys');
    const keys = [];
    for (let i = 0; i < numTextKeys; i++) keys.push({ time: f32(), text: sizedString() });
    fields = { nextExtraData, unknownInt1, numTextKeys, keys };
  } else {
    throw new Error(`decodeKfBlock: type ${block.type} is not an AV-3 animation type`);
  }

  const consumed = p - start;
  const closure = p === end;
  return { fields, consumed, spanBytes: block.span, closureExact: closure, cursorAtEnd: p };
}

/** Decode ALL NiKeyframeController/NiKeyframeData/NiTextKeyExtraData opaque
 * blocks of an extraction. Returns per-block result + a LOUD failures list
 * (never silent). Blocks already implemented (fields != null) are skipped. */
export function decodeKeyframeBlocks41(payload, extraction) {
  const results = { controllers: [], data: [], textKeys: [], failures: [], closureAll: true };
  for (const b of extraction.blocks) {
    if (b.type !== 'NiKeyframeController' && b.type !== 'NiKeyframeData' && b.type !== 'NiTextKeyExtraData') continue;
    try {
      const dec = decodeKfBlock(payload, b);
      if (!dec.closureExact) {
        results.failures.push({ blockIndex: b.index, type: b.type, reason: `closure MISMATCH: cursor ${dec.cursorAtEnd} != blockEnd ${b.rttiStart + b.span}` });
        results.closureAll = false;
        continue;
      }
      if (b.type === 'NiKeyframeController') {
        results.controllers.push({ blockIndex: b.index, ...dec.fields });
      } else if (b.type === 'NiKeyframeData') {
        results.data.push({ blockIndex: b.index, ...dec.fields });
      } else {
        results.textKeys.push({ blockIndex: b.index, ...dec.fields });
      }
    } catch (e) {
      results.failures.push({ blockIndex: b.index, type: b.type, offset: b.rttiStart, span: b.span, reason: String(e.message ?? e) });
      results.closureAll = false;
    }
  }
  return results;
}
