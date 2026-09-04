# 02 — Block registry

Status: layout CONFIRMED for every listed type (R61 parses all 5596 + 5426
files with zero failures). Counts: 9.3.5 corpus census (2026-09-04, fully
machine-readable); 2003 counts canonical where marked.

## Inheritance bases (read order = serialization order)

**NiObjectNET** (per version):
```
v4:  Name(SizedString) + ExtraData(Ref) + Controller(Ref)
v10: Name(SizedString) + NumExtraData(u32) + ExtraData(Ref[]) + Controller(Ref)
```

**NiAVObject** = NET +
```
v4:  Flags(u16) Translation(Vec3) Rotation(Mat33) Scale(f32)
     Velocity(Vec3) NumProperties(u32) Properties(Ref[])
     HasBoundingBox(bool→4B in 4.0.0.2) [+ BoundingBox: unk u32, trans Vec3,
     rot Mat33, radius f32]
v10: Flags(u16) Translation(Vec3) Rotation(Mat33) Scale(f32)
     NumProperties(u32) Properties(Ref[]) CollisionObject(Ref)
```

**NiProperty** = NET + (per-type fields)
**NiTimeController** (NOT NiObjectNET!): NextController(Ref) Flags(u16)
Frequency(f32) Phase(f32) StartTime(f32) StopTime(f32) Target(Ref) = 30 B
**NiExtraData base**:
```
v4:  nextExtraData(Ref) only — NO Name
v10: Name(SizedString) only — NO link
```
**NiGeometry** = AVObject + Data(Ref) + Skin(Ref) [+ v10 hasShader u8,
shaderName SizedString + u32 if set]

## Full registry (77 types observed in 9.3.5; counts = 9.3.5 / 2003 where known)

| Type | Count 9.3.5 | Parser notes |
|---|---|---|
| NiNode | 120,956 | NET+AV+Children(Ref[])+Effects(Ref[]) |
| NiKeyframeController | 72,552 | TimeController + Data(Ref) |
| NiKeyframeData | 72,552 | see 05 |
| NiTriShape | 21,914 / 21,190 | see 03 |
| NiTriShapeData | 21,830 / 21,106 | see 03 |
| NiTexturingProperty | 14,817 | see 04 |
| NiMaterialProperty | 11,563 / ~11,185 | see 04 |
| NiArkAnimationExtraData | 5,596 | see 08 |
| NiArkImporterExtraData | 5,596 | see 08 |
| NiArkTextureExtraData | 5,596 | see 08 |
| NiAlphaProperty | 5,527 | NET + Flags(u16) + Threshold(u8) |
| NiZBufferProperty | 5,245 | NET + Flags(u16) + Function(u32, v≥0x0401000C) |
| NiStringExtraData | 4,781 | ExtraData base + Data(SizedString) |
| NiVertexColorProperty | 4,313 | NET + flags u16 + vertexMode u16 + lightingMode u16 + **PE ext u32 (always consumed; values 0/1)** |
| NiArkViewportInfoExtraData | 4,095 / ~3,917 | see 08 |
| NiArkShaderExtraData | 2,084 | see 08 |
| NiTextureEffect | 1,694 / 1,646 | see 06 |
| NiTextKeyExtraData | 1,039 | see 05 |
| NiPointLight | 846 | see 06 |
| NiFloatData | 778 | KeyGroup<float> |
| NiTextureTransformController | 744 | TimeController + unk u8 + textureSlot u32 + operation u32 + Data(Ref) |
| NiSkinInstance | 720 | see 07 |
| NiSkinData | 720 | see 07 |
| NiStencilProperty | 532 | see 04 |
| NiBillboardNode | 384 | NiNode + mode(u16, v10 only) |
| NiVertexMorphExtraData | 354 / 79 | see 08 |
| NiArkBillboardNode | 293 | = NiNode (+mode u16 in v10) — proven alias |
| NiPSysEmitterCtlr / UpdateCtlr / EmitterCtlrData / AgeDeath / Spawn / Position / BoundUpdate modifiers | 259 each | see 06 |
| NiPosData | 258 | KeyGroup<Vec3> |
| NiParticleSystem | 256 | see 06 |
| NiPSysData | 256 | see 06 |
| NiMaterialColorController | 247 | TimeController + targetColor(u16, v10) + Data(Ref) |
| NiPSysGrowFadeModifier | 227 | modifier + growTime f32 + growGen u16 + fadeTime f32 + fadeGen u16 |
| NiPSysBoxEmitter | 223 | volume emitter + width/height/depth f32 |
| NiPSysColorModifier | 221 | modifier + Data(Ref) |
| NiColorData | 221 | KeyGroup<Color4> |
| NiUVController | 180 | TimeController + unk u16 + Data(Ref); NiUVData = 4× KeyGroup<float> |
| NiUVData | 180 | |
| NiDirectionalLight | 130 | light, no own fields |
| NiFlipController | 126 / 125 | see 05 |
| NiSkinPartition | 116 | see 07 |
| NiAmbientLight | 76 | light, no own fields |
| NiPSysGravityModifier | 54 | see 06 |
| NiSpotLight | 47 | point light + cutoffAngle f32 + exponent f32 |
| NiSourceTexture | 45 | see 04 |
| NiAlphaController | 34 | TimeController + Data(Ref) |
| NiVisData | 27 | u32 count + keys(time f32 + u8) |
| NiIntegerExtraData | 25 | base + u32 |
| NiBooleanExtraData | 25 | base + u8 |
| NiVisController | 24 | TimeController + Data(Ref) |
| NiPSysMeshEmitter | 24 | see 06 |
| NiSpecularProperty | 21 | NET + Flags(u16) |
| NiCollisionData | 12 | see 06 |
| + particle colliders/managers, lights extras, NiCamera, NiSortAdjustNode, NiFogProperty, NiDitherProperty, NiShadeProperty, NiPixelData, NiPSys* remainder | | see 06 / 04 |

Every type above = boundary EXACT (stream ends exactly at block end after
parse). Types marked `_partial` in the parser keep their raw payload +
SHA256 for future semantic work: NiArkAnimation variants, NiArkTexture
entries (9 trailing bytes = anim_flag u8 + frame_index u32 + bnt2_id u32 —
iteration-24 canon), NiArkImporter trailing 38 B, viewport extensions,
vertex morph payloads.

## FAIL_CLOSED types (known unsupported)

- `NiTriStripsData` — stub only (**0 occurrences** in both PE corpora — PE
  uses NiTriShape triangles exclusively)
- CD-2003 corpus: 17 block types unsupported by R61 (CD dialect) — see
  README corpus note; separate work package if ever needed.
