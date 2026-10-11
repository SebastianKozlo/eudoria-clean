---
run_id: PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010
card: animation-decoder
status: MEASURED_ON_CORPUS
sources:
  - module: src/pecompat/PecAnimDecoder.js (pec-anim-decoder-pcg935-r1)
corpus_scope: catalog — kf 1844 assets, skin 373, morph 116, psys 256 blocks, textkeys 1038 blocks
classification: INTERNAL_QC_ONLY_PENDING_DESKTOP
created: 2026-10-11
---

# Animation decoder — original-clip emission + honest labels

## Emitted (REAL playback)

- **NiKeyframeController -> NiKeyframeData**: per-node tracks — quaternion
  keys (LINEAR; TBC tangents consumed per type), translation (vec3) and scale
  key groups; euler-XYZ type 4 kept as axis groups (era PE extra float
  preserved). Duration measured from the ORIGINAL key times (never invented).
- **NiTextKeyExtraData**: clip markers preserved as time+text pairs
  (witness 462325: "0.00 morph:left", "0.67 morph:right").
- **Skinning**: NiSkinInstance + NiSkinData -> per-bone bindTranslation /
  bindRotationQuat (converted from the stored mat33) / bindScale +
  per-vertex weights. The NIF bone transform IS the inverse bind — emitted
  directly for THREE.Skeleton boneInverses; the skeleton root is the block's
  skeletonRootRef (NO double root application).
- **NiUVController/NiUVData, NiVisController/NiVisData, NiFlipController,
  NiMaterialColorController(+NiColorData), NiAlphaController(+NiFloatData)**:
  emitted with their original key groups (era coverage; viewer applies
  keyframe clips; the property controllers are inventoried and emitted —
  see PERFORMANCE_AND_LIMITS for the applied subset).

## Honest labels (no simulated clips anywhere)

- **PSys** (256 blocks): `DETECTION_UNRESOLVED` — opaque runtime metadata.
- **Morphs** (NiVertexMorphExtraData, 116 assets): region recorded RAW by
  the reader; label `MORPH_REGION_RECORDED_RAW`.
- Empty controllers (0 keys in every group) are counted as a separate
  category, never promoted to playable.

## Verified witnesses

- 462325.nif (v10): 50 controllers -> 50 tracks/clips, 3.33 s, 1 textKey
  block; browser playback: play/pause/stop/scrub(3.00/5.00 on 360268)/
  speed/once-repeat; >2-duration repeat wraps cleanly (1.44/3.33 after
  2×+1.5 s) — deterministic LoopRepeat, no drift.
- 360268.nif (v4): 6 keyframe controllers (5.00 s) + 7-bone skin + 9 meshes
  + 2 TEXTURED_EXACT slots — the v4 animated+skinned+textured witness.
- 508326.nif (v10): skin (2 bones, 11 weights) + 6 PSys blocks labeled
  DETECTION_UNRESOLVED.
