---
run_id: PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010
card: nif-4.1.0.12-corpus-reader
status: MEASURED_ON_CORPUS
sources:
  - path: D:/Eudoria_Reconstruction/pcg_install/Data/Models/Models.bnt
    sha256: c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0
  - module: src/pecompat/PecNif41Reader.js
    version: pec-nif41-corpus-reader-v1
corpus_scope: 757/757 NIF 4.1.0.12 entries closed EOF-exact (100%)
classification: INTERNAL_QC_ONLY_PENDING_DESKTOP
created: 2026-10-11
---

# NIF 4.1.0.12 corpus reader — closure mechanism

## Mechanism (implemented, measured)

- Header: `NetImmerse File Format, Version 4.1.0.12\n` + version u32
  `0x0401000C` + numBlocks u32; NO preamble table — blocks carry INLINE RTTI
  SizedStrings (4-byte length + chars).
- Closure = all numBlocks blocks + TopObjects footer `[ntop u32][refs i32×ntop]`
  + EOF EXACT. Fail-closed otherwise (CLOSURE_FAIL loud).
- Boundary search for `NiArkAnimationExtraData` / `NiArkViewportInfoExtraData`:
  documented ext sizes seeded FIRST (FIXED_A 37 B when `u3==-1 && u2<4`),
  then v4-RTTI-shaped candidates (a u32 length 5..50 + printable string that is
  a KNOWN type name), then footer-shape candidates. Unknown-RTTI and RTTI
  read errors are BACKTRACKABLE (return null) — the RTTI is data-derived, so a
  garbage type means the candidate is wrong, not the file.
- Memoization of failed `(blockIndex, pos)` pairs converts the candidate
  product from exponential to linear.

## Measured layout corrections (this run's lessons)

1. **NiProperty double-flags**: the NiProperty base ALREADY reads the u16
   property flags; per-property parsers must NOT read flags again. The double
   read shifted every property block by +2 bytes and broke 757/757 files at
   the Z-buffer boundary (fixed; 757/757 closed).
2. **ArkTexture v4 entry count**: `base(link) + 2×i32 + u8 + i32 + numTex`
   — the unnamed i32 BETWEEN the u8 and numTex was missing (4-byte shift).
   Byte-verified on 223534.nif: link=3, i32a=0, i32b=3, u8=1, i32=0,
   numTex=1, entry `Scene_Root_0_BASE` + f1 + f2(-1) + texPropRef(4) + 9-byte tail.
3. **v4 lights have NO dynamic-effect layer**: v4.1.0.12 NiLight =
   `NET + AV + Dimmer(f32) + ambient + diffuse + specular` (verified on
   353832.nif NiAmbientLight @58065; the [1][0] at EOF is the FOOTER, not a
   ptr list). See the 4.0.0.2 card for the DIFFERENT ptr-list form.

## v4 block-type census (757 entries, this run)

NiTriShape 4891, NiTriShapeData 4872, NiNode 4806, NiTexturingProperty 3640,
NiMaterialProperty 3417, NiZBufferProperty 1069, NiAlphaProperty 1049,
NiArkAnimationExtraData 757, NiArkTextureExtraData 757, NiArkImporterExtraData 757,
NiStringExtraData 556, NiVertexColorProperty 436, NiArkBillboardNode 253,
NiUVController 155, NiUVData 155, NiTextureEffect 108, NiKeyframeController 69,
NiKeyframeData 69, NiArkViewportInfoExtraData 33, NiSkinInstance 26, NiSkinData 26,
NiAmbientLight 22, NiFlipController 14, NiVisController 13, NiVisData 13,
NiDirectionalLight 10, NiSpecularProperty 7, NiAlphaController 3,
NiMaterialColorController 3, NiPosData 3, NiFloatData 3, NiDitherProperty 3,
NiTextKeyExtraData 1.
