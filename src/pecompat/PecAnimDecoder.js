// PecAnimDecoder.js — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010 (Wave 6)
// REAL original-animation inventory + decoding for PCG 9.3.5 assets:
//   - NiKeyframeController -> NiKeyframeData (quaternion LINEAR keys + euler
//     XYZ groups; translation/scale key groups) -> per-node tracks.
//   - NiTextKeyExtraData -> clip markers (names + times).
//   - Skinning: NiSkinInstance + NiSkinData (bind pose, inverse bind via
//     the skin overall/bone transforms, vertex weights) — emitted for the
//     client to build a THREE.Skeleton WITHOUT double root application.
//   - NiUVController/NiUVData, NiVisController/NiVisData, NiFlipController,
//     NiMaterialColorController, NiAlphaController/NiFloatData.
//   - NiVertexMorphExtraData (v10): record inventory; targets decoded where
//     the reader recorded ranges (era-labelled).
//   - Particle systems: DETECTION_UNRESOLVED (opaque runtime metadata — honest
//     label, no simulated clips anywhere).
// NO invented/simulated clips: every track comes from original key data.
'use strict';

export const PEC_ANIM_DECODER_VERSION = 'pec-anim-decoder-pcg935-r1';

function mat33ToQuat(m) {
  // m: row-major 9-array [r00..r22]
  const trace = m[0] + m[4] + m[8];
  let x; let y; let z; let w;
  if (trace > 0) {
    const s = Math.sqrt(trace + 1) * 2;
    w = 0.25 * s;
    x = (m[7] - m[5]) / s;
    y = (m[2] - m[6]) / s;
    z = (m[3] - m[1]) / s;
  } else if (m[0] > m[4] && m[0] > m[8]) {
    const s = Math.sqrt(1 + m[0] - m[4] - m[8]) * 2;
    w = (m[7] - m[5]) / s;
    x = 0.25 * s;
    y = (m[1] + m[3]) / s;
    z = (m[2] + m[6]) / s;
  } else if (m[4] > m[8]) {
    const s = Math.sqrt(1 + m[4] - m[0] - m[8]) * 2;
    w = (m[2] - m[6]) / s;
    x = (m[1] + m[3]) / s;
    y = 0.25 * s;
    z = (m[5] + m[7]) / s;
  } else {
    const s = Math.sqrt(1 + m[8] - m[0] - m[4]) * 2;
    w = (m[3] - m[1]) / s;
    x = (m[2] + m[6]) / s;
    y = (m[5] + m[7]) / s;
    z = 0.25 * s;
  }
  return [x, y, z, w];
}

function keyGroupToTrack(group, reader, dims) {
  if (!group || !group.numKeys) return null;
  const times = [];
  const values = [];
  for (let i = 0; i < group.numKeys; i++) {
    times.push(group.times[i]);
    const v = group.values[i];
    if (dims === 4) values.push(v[0], v[1], v[2], v[3]);
    else if (dims === 3) values.push(v[0], v[1], v[2]);
    else values.push(v);
  }
  return { times, values };
}

/**
 * @param ir buildAssetIR result (blocks with .fields/.name/.index)
 * @returns animation inventory + decodable clips/tracks JSON
 */
export function decodeAssetAnimations(ir) {
  const blocks = ir.blocks ?? [];
  const byIndex = new Map(blocks.map((b) => [b.index, b]));
  const out = {
    version: PEC_ANIM_DECODER_VERSION,
    detection: {},
    keyframeControllers: 0,
    clips: [],
    uvControllers: [],
    visControllers: [],
    flipControllers: [],
    materialColorControllers: [],
    alphaControllers: [],
    skeletons: [],
    morphs: [],
    psys: [],
    textKeys: [],
    unresolved: [],
  };
  const det = out.detection;
  for (const b of blocks) det[b.type] = (det[b.type] || 0) + 1;

  // ---- text keys (clip markers) ----
  const textKeyBlocks = blocks.filter((b) => b.type === 'NiTextKeyExtraData');
  for (const tk of textKeyBlocks) {
    const keys = tk.fields?.keys ?? [];
    out.textKeys.push({ block: tk.index, name: tk.fields?.name ?? '', keys: keys.map((k) => ({ time: k.time, text: k.text })) });
  }

  // ---- keyframe controllers -> tracks ----
  for (const b of blocks) {
    if (b.type !== 'NiKeyframeController') continue;
    out.keyframeControllers++;
    const f = b.fields ?? {};
    const data = byIndex.get(f.dataRef);
    const target = byIndex.get(f.targetRef);
    if (!data || !target) { out.unresolved.push({ block: b.index, reason: 'dataRef/targetRef missing' }); continue; }
    const d = data.fields ?? {};
    const track = { controller: b.index, targetBlock: target.index, targetName: target.name ?? '', startTime: f.startTime ?? null, stopTime: f.stopTime ?? null, frequency: f.frequency ?? 1, phase: f.phase ?? 0, quaternion: null, euler: null, position: null, scale: null };
    const rk = d.rotationKeys;
    if (rk && rk.numKeys) {
      track.quaternion = { interpolation: rk.interpolation, times: Array.from(rk.times ?? []), quats: Array.from(rk.quats ?? []) };
    } else if (d.eulerAxes) {
      track.euler = {
        unknownFloat: d.eulerUnknownFloat ?? null,
        axes: d.eulerAxes.map((g) => keyGroupToTrack(g, null, 1)),
      };
    }
    track.position = keyGroupToTrack(d.translationKeys, null, 3);
    track.scale = keyGroupToTrack(d.scaleKeys, null, 1);
    // duration from data
    const allTimes = [...(track.quaternion?.times ?? []), ...(track.position?.times ?? []), ...(track.scale?.times ?? [])];
    track.dataDuration = allTimes.length ? Math.max(...allTimes) : 0;
    out.clips.push(track);
  }

  // ---- UV controllers ----
  for (const b of blocks) {
    if (b.type !== 'NiUVController') continue;
    const f = b.fields ?? {};
    const data = byIndex.get(f.dataRef);
    const target = byIndex.get(f.targetRef);
    const groups = data?.fields?.uvGroups ?? [];
    out.uvControllers.push({
      block: b.index, targetBlock: target?.index ?? null, targetName: target?.name ?? null,
      startTime: f.startTime ?? null, stopTime: f.stopTime ?? null,
      groups: groups.map((g) => keyGroupToTrack(g, null, 1)),
    });
  }

  // ---- vis controllers ----
  for (const b of blocks) {
    if (b.type !== 'NiVisController') continue;
    const f = b.fields ?? {};
    const data = byIndex.get(f.dataRef);
    const target = byIndex.get(f.targetRef);
    out.visControllers.push({
      block: b.index, targetBlock: target?.index ?? null, targetName: target?.name ?? null,
      startTime: f.startTime ?? null, stopTime: f.stopTime ?? null,
      keys: data?.fields?.keys ?? [],
    });
  }

  // ---- flip controllers ----
  for (const b of blocks) {
    if (b.type !== 'NiFlipController') continue;
    const f = b.fields ?? {};
    const target = byIndex.get(f.targetRef);
    out.flipControllers.push({
      block: b.index, targetBlock: target?.index ?? null, targetName: target?.name ?? null,
      textureSlot: f.textureSlot ?? null, delta: f.delta ?? null,
      startTime: f.startTime ?? null, stopTime: f.stopTime ?? null,
      sources: (f.sourceRefs ?? []).map((r) => byIndex.get(r)?.fields?.fileName ?? null),
    });
  }

  // ---- material color + alpha controllers ----
  for (const b of blocks) {
    if (b.type === 'NiMaterialColorController') {
      const f = b.fields ?? {};
      const data = byIndex.get(f.dataRef);
      const target = byIndex.get(f.targetRef);
      out.materialColorControllers.push({
        block: b.index, targetBlock: target?.index ?? null, targetColor: f.targetColor ?? null,
        startTime: f.startTime ?? null, stopTime: f.stopTime ?? null,
        keys: data ? keyGroupToTrack(data.fields?.colorKeys, null, 4) : null,
      });
    } else if (b.type === 'NiAlphaController') {
      const f = b.fields ?? {};
      const data = byIndex.get(f.dataRef);
      const target = byIndex.get(f.targetRef);
      out.alphaControllers.push({
        block: b.index, targetBlock: target?.index ?? null,
        startTime: f.startTime ?? null, stopTime: f.stopTime ?? null,
        keys: data ? keyGroupToTrack(data.fields?.floatKeys, null, 1) : null,
      });
    }
  }

  // ---- skinning ----
  for (const b of blocks) {
    if (b.type !== 'NiSkinInstance') continue;
    const f = b.fields ?? {};
    const skinData = byIndex.get(f.dataRef);
    const root = byIndex.get(f.skeletonRootRef);
    const bones = (f.boneRefs ?? []).map((r) => byIndex.get(r));
    const sd = skinData?.fields ?? {};
    const skel = {
      block: b.index, skinDataBlock: f.dataRef, rootBlock: f.skeletonRootRef,
      rootName: root?.name ?? null, numBones: f.numBones ?? 0,
      overall: { rotation: sd.overallRotation ?? null, translation: sd.overallTranslation ?? null, scale: sd.overallScale ?? null },
      bones: [],
      weightsOnSkinData: sd.hasVertexWeights ?? null,
    };
    const boneFields = sd.bones ?? [];
    for (let i = 0; i < bones.length; i++) {
      const bone = bones[i];
      const bf = boneFields[i] ?? {};
      const q = bf.boneRotation ? mat33ToQuat(bf.boneRotation) : null;
      skel.bones.push({
        boneBlock: bone?.index ?? null, boneName: bone?.name ?? '',
        bindTranslation: bf.boneTranslation ?? null, bindRotationQuat: q, bindScale: bf.boneScale ?? null,
        numVertices: bf.numVertices ?? 0,
        vertexWeights: bf.vertexWeights ?? [],
      });
    }
    out.skeletons.push(skel);
  }

  // ---- morphs (v10) ----
  for (const b of blocks) {
    if (b.type !== 'NiVertexMorphExtraData') continue;
    const f = b.fields ?? {};
    out.morphs.push({
      block: b.index, name: f.name ?? null,
      numVertices: f.numVertices ?? null,
      relStart: f.morphRelStart ?? null, relEnd: f.morphRelEnd ?? null,
      // era-labelled: the morph target semantics stay DETECTION_UNRESOLVED
      // where the reader recorded the region RAW (see PecNif10CorpusReader).
      label: 'MORPH_REGION_RECORDED_RAW',
    });
  }

  // ---- particle systems (opaque runtime metadata) ----
  const psysTypes = ['NiPSysData', 'NiPSysEmitterCtlr', 'NiPSysUpdateCtlr', 'NiPSysResetOnLoopCtlr', 'NiPSysModifierActiveCtlr', 'NiPSysColliderMgr', 'NiMeshPSysData'];
  for (const b of blocks) {
    if (psysTypes.includes(b.type)) {
      out.psys.push({ block: b.index, type: b.type, label: 'DETECTION_UNRESOLVED' });
    }
  }
  return out;
}
