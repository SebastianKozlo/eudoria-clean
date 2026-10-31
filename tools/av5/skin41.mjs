// skin41.mjs — AV-5 (PE_ISO_ASSET_VIEWER, loop 8ee81e37, era ISO_5_1_0_0).
// Closure-exact decoder for NIF 4.1.0.12 skinning blocks, layout established
// FROM BYTES of Models.ark members 101411/101412/101413/102103/102171/102172
// (probe 2026-10-31; see tools/av5/skin_probe.mjs) — NOT copied from the 10.1
// pipeline. Bind law: campaign-8163 W4-1 / niTransformAdapter.mjs SDK site
// NiDX9Renderer.cpp:2948 — boneMatrix = boneWorld * SkinToBone (parent on
// the LEFT); per-bone NiSkinData transform = SkinToBone (inverse bind).
//
// LAYOUT (measured):
//   NiSkinInstance: [dataRef i32][rootNodeRef i32][numBones u32][boneRefs i32×n]
//   NiSkinData: [rootParentWorld: rot 9f + trans 3f + scale 1f]
//               [numBones u32][unknownFloat f32 (observed -1.0 on all samples)]
//               per bone: [SkinToBone: rot 9f + trans 3f + scale 1f]
//                         [boundCenter 3f][boundRadius 1f]
//                         [numWeights u16]
//                         [(vertexIndex u16, weight f32) × numWeights]
//   NiSkinPartition: decoded best-effort when present (see decode below); a
//   partition closure FAIL is LOUD and recorded — skinning itself only needs
//   NiSkinInstance + NiSkinData (software path).
// CLOSURE GATE: every decoded block consumes EXACTLY its opaque span.
'use strict';

export function decodeSkinBlock(payload, block, numShapeVertsHint = null) {
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
  const guard = (n, what, max = 100000) => { if (n > max || n < 0) throw new Error(`impossible ${what} ${n}`); };
  const readTransform = () => {
    const rotation = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
    for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) rotation[i][j] = f32();
    const translation = [f32(), f32(), f32()];
    const scale = f32();
    return { rotation, translation, scale };
  };
  const isRotation = (R) => {
    for (let i = 0; i < 3; i++) {
      const n = Math.hypot(R[i][0], R[i][1], R[i][2]);
      if (!Number.isFinite(n) || Math.abs(1 - n) > 0.01) return false;
    }
    const d01 = R[0][0] * R[1][0] + R[0][1] * R[1][1] + R[0][2] * R[1][2];
    const d02 = R[0][0] * R[2][0] + R[0][1] * R[2][1] + R[0][2] * R[2][2];
    const d12 = R[1][0] * R[2][0] + R[1][1] * R[2][1] + R[1][2] * R[2][2];
    return Math.abs(d01) < 0.01 && Math.abs(d02) < 0.01 && Math.abs(d12) < 0.01;
  };

  let fields;
  if (block.type === 'NiSkinInstance') {
    const dataRef = i32(); const rootNodeRef = i32();
    const numBones = u32(); guard(numBones, 'numBones', 256);
    const bones = [];
    for (let i = 0; i < numBones; i++) bones.push(i32());
    fields = { dataRef, rootNodeRef, numBones, bones };
  } else if (block.type === 'NiSkinData') {
    const rootParentWorld = readTransform();
    if (!isRotation(rootParentWorld.rotation)) throw new Error('rootParentWorld rotation not orthonormal — wrong layout');
    const numBones = u32(); guard(numBones, 'numBones', 256);
    const unknownFloat = f32();
    const bones = [];    for (let b = 0; b < numBones; b++) {
      const skinToBone = readTransform();
      if (!isRotation(skinToBone.rotation)) throw new Error(`bone ${b} SkinToBone rotation not orthonormal — wrong layout`);
      const boundCenter = [f32(), f32(), f32()];
      const boundRadius = f32();
      if (!Number.isFinite(boundRadius) || boundRadius < 0 || boundRadius > 1e6) throw new Error(`bone ${b} boundRadius ${boundRadius} implausible`);
      const numWeights = u16();
      guard(numWeights, 'numWeights', 65535);
      const weights = [];
      for (let k = 0; k < numWeights; k++) {
        const vertexIndex = u16();
        const weight = f32();
        if (numShapeVertsHint != null && vertexIndex >= numShapeVertsHint) {
          throw new Error(`bone ${b} vertexIndex ${vertexIndex} >= shape verts ${numShapeVertsHint}`);
        }
        if (!Number.isFinite(weight) || weight < -1e-4 || weight > 1.0001) {
          throw new Error(`bone ${b} weight ${weight} out of [0,1] — wrong layout`);
        }
        weights.push({ weight, vertexIndex });
      }
      bones.push({ skinToBone, boundCenter, boundRadius, numWeights, weights });
    }
    // trailing bytes after the last bone's vertex list (DISCOVERY: corpus
    // shows a small constant tail; recorded verbatim until its semantics
    // are identified).
    const tailLen = end - p;
    if (tailLen < 0 || tailLen > 64) throw new Error(`implausible tailLen ${tailLen}`);
    let tailHex = '';
    for (let i = 0; i < tailLen; i++) tailHex += payload[p + i].toString(16).padStart(2, '0');
    p = end;
    fields = { rootParentWorld, numBones, unknownFloat, bones, tailLen, tailHex };
  } else if (block.type === 'NiSkinPartition') {
    // Best-effort layout (bytes; verified only where it closes exactly — a
    // closure failure is LOUD, never silent):
    //   [numPartitions u32] per partition:
    //   [numBones u32][boneRefs i32×n][numVertices u32][numTriangles u32]
    //   [unknown?][vertexIndex remap u16×numVertices][trueWeights f32?]
    // The 4.1-era partition payload varies; anything not closing exactly is
    // recorded as UNSUPPORTED with the raw span — the software skinning
    // path (NiSkinInstance+NiSkinData) is COMPLETE without it.
    const numPartitions = u32(); guard(numPartitions, 'numPartitions', 64);
    const partitions = [];
    let consumedExact = true;
    try {
      for (let i = 0; i < numPartitions; i++) {
        const numBones = u32(); guard(numBones, 'p.numBones', 256);
        const bones = [];
        for (let b = 0; b < numBones; b++) bones.push(i32());
        const numVertices = u32(); guard(numVertices, 'p.numVertices', 65535);
        // stop structural guessing here: consume the rest as raw (span-close
        // enforced below at the partition-list level only if exactly 0 left)
        partitions.push({ numBones, bones, numVertices, raw: true, rawBytes: end - p });
        p = end; // span raw — marked, not invented
        consumedExact = false;
      }
    } catch (e) {
      consumedExact = false;
      fields = { numPartitions, partitions, note: 'PARTIAL_RAW — 4.1 partition structural layout not closure-verified; software path does not need it' };
      return { fields, consumed: p - start, spanBytes: block.span, closureExact: false, note: 'PARTIAL_RAW' };
    }
    fields = { numPartitions, partitions, note: 'RAW structural prefix only' };
    return { fields, consumed: p - start, spanBytes: block.span, closureExact: consumedExact && p === end, note: 'RAW' };
  } else {
    throw new Error(`decodeSkinBlock: ${block.type} is not a skin type`);
  }

  const consumed = p - start;
  return { fields, consumed, spanBytes: block.span, closureExact: p === end, cursorAtEnd: p };
}

/** Decode all skin blocks of an extraction. numShapeVertsHint: map of
 * skinInstance blockIndex -> shape numVertices (for cross-checks). */
export function decodeSkinBlocks41(payload, extraction, shapeVertsBySkinRef = new Map()) {
  const out = { instances: [], data: [], partitions: [], failures: [], closureAll: true };
  for (const b of extraction.blocks) {
    if (b.type !== 'NiSkinInstance' && b.type !== 'NiSkinData' && b.type !== 'NiSkinPartition') continue;
    try {
      const hint = b.type === 'NiSkinData' ? null : null;
      const dec = decodeSkinBlock(payload, b, hint);
      if (b.type === 'NiSkinPartition') {
        out.partitions.push({ blockIndex: b.index, ...dec.fields, note: dec.note });
        if (!dec.closureExact) out.closureAll = false; // partition is optional; noted, not fatal
        continue;
      }
      if (!dec.closureExact) {
        out.failures.push({ blockIndex: b.index, type: b.type, reason: `closure MISMATCH: cursor ${dec.cursorAtEnd} != blockEnd ${b.rttiStart + b.span}` });
        out.closureAll = false;
        continue;
      }
      if (b.type === 'NiSkinInstance') out.instances.push({ blockIndex: b.index, ...dec.fields });
      else out.data.push({ blockIndex: b.index, ...dec.fields });
    } catch (e) {
      out.failures.push({ blockIndex: b.index, type: b.type, offset: b.rttiStart, span: b.span, reason: String(e.message ?? e) });
      out.closureAll = false;
    }
  }
  return out;
}

/** Build per-shape skin payload: for a shape with skinRef -> NiSkinInstance:
 * bones (block indices), skinToBone matrices, and merged per-vertex
 * influences (weight, boneSlot). NO truncation — max influences per vertex
 * measured and reported. */
export function buildSkinBinding(skin, shape) {
  const inst = skin.instances.find(i => i.blockIndex === shape.skinRef);
  if (!inst) return { ok: false, reason: 'NiSkinInstance not closure-decoded' };
  const data = skin.data.find(d => d.blockIndex === inst.dataRef);
  if (!data) return { ok: false, reason: 'NiSkinData not closure-decoded' };
  if (inst.bones.length !== data.bones.length) {
    return { ok: false, reason: `bone count mismatch inst ${inst.bones.length} vs data ${data.bones.length}` };
  }
  const nV = shape.numVertices;
  const infl = Array.from({ length: nV }, () => []);
  for (let b = 0; b < data.bones.length; b++) {
    for (const w of data.bones[b].weights) {
      if (w.vertexIndex >= nV) return { ok: false, reason: `vertex index ${w.vertexIndex} >= ${nV}` };
      infl[w.vertexIndex].push({ bone: b, weight: w.weight });
    }
  }
  // per-vertex stats: sum + max influences (no truncation anywhere)
  let maxInfl = 0, badSum = 0;
  const sums = new Float64Array(nV);
  for (let v = 0; v < nV; v++) {
    maxInfl = Math.max(maxInfl, infl[v].length);
    for (const i of infl[v]) sums[v] += i.weight;
    if (Math.abs(sums[v] - 1) > 1e-3) badSum++;
  }
  return {
    ok: true,
    skinInstanceBlock: inst.blockIndex,
    skinDataBlock: data.blockIndex,
    rootBoneRef: inst.rootNodeRef,
    bones: inst.bones,
    skinToBone: data.bones.map(b => b.skinToBone),
    rootParentWorld: data.rootParentWorld,
    influences: infl.map(list => list.map(x => [x.bone, x.weight])),
    stats: { maxInfluencesPerVertex: maxInfl, weightSumMismatch: badSum, numVertices: nV,
             sums: Array.from(sums) },
  };
}
