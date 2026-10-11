---
run_id: PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010
card: nif-4.0.0.2-gates
status: MEASURED_SINGLE_FILE
sources:
  - entry: Models.bnt/52555.nif (38115 B, entryIndex 799)
  - module: src/pecompat/PecNif41Reader.js (version gates on NIF_V4_0_0_2)
corpus_scope: 1/1 NIF 4.0.0.2 entry closed EOF-exact (37 blocks)
classification: INTERNAL_QC_ONLY_PENDING_DESKTOP
created: 2026-10-11
---

# NIF 4.0.0.2 gates (the single 52555.nif)

## Version gates (vs 4.1.0.12)

1. **Booleans are 4-byte i32** (01/00), NOT the 1-byte NiBool of 4.1.0.12.
   Applies to: NiAVObject HasABV, NiTriShapeData hasVertices/hasNormals/
   hasColors.
2. **NiTriShapeData hasUv**: an EXTRA 4-byte boolean between numTextureSets
   (i16) and the uvSets — ONLY in 4.0.0.2 (missing this single field breaks
   the block chain; the historical R60 fix, re-verified here).
3. **NiZBufferProperty has NO u32 z-function** (z-function exists only
   >= 4.1.0.5): the property ends after the base + flags.
4. **NiLight 4.0.0.2 form (measured byte-exact on all 3 lights of 52555)**:
   `NET + AV + numAffectedNodeListPointers u32 + RAW ptr u32[] + ambient(12)
   + diffuse(12) + specular(12) + trailing f32`. The ptr values are raw heap
   addresses (0x0a91c9d8 × 3 — a real saved pointer list, post-load
   meaningless). The trailing f32 measured 1.0, 1.0, 0.0 — semantics
   UNRESOLVED (dimmer-like values); recorded as measured, NOT interpreted.

## 4.1.0.12 contrast (do not merge these forms!)

The 4.1.0.12 NiLight has NO ptr-list layer and NO trailing f32: it is
`NET + AV + dimmer(f32) + colors`, and the 8 bytes at EOF are the footer
`[ntop][ref]`. Merging the two forms broke 25 v4.1 files (fixed this run);
both forms are now version-gated in the reader.

## Verified block census (52555.nif)

NiNode:8, NiArkAnimationExtraData:1, NiArkTextureExtraData:1,
NiArkImporterExtraData:1, NiZBufferProperty:1, NiVertexColorProperty:1,
NiTriShape:7, NiMaterialProperty:7, NiTriShapeData:7, NiDirectionalLight:2,
NiAmbientLight:1 — 37 blocks, footer [1][0], EOF exact.
