# 05 — Controllers and animation data blocks

## NiTimeController base (all controllers) — CONFIRMED

```
NextController Ref (-1 = none) | Flags u16 | Frequency f32 | Phase f32 |
StartTime f32 | StopTime f32 | Target Ref            <- 30 bytes
```
NOT NiObjectNET — no name/extra/controller fields.

## Controller registry (own fields after the base)

| Controller | Own fields (PE v4+v10) |
|---|---|
| NiKeyframeController | Data Ref (→ NiKeyframeData) |
| NiUVController | unknownShort u16 + Data Ref |
| NiTextureTransformController | unknown2 u8 + textureSlot u32 + operation u32 + Data Ref |
| NiFlipController | textureSlot u32 + unknownInt2 u32 + delta f32 + numSources u32 + sources Ref[] |
| NiVisController | Data Ref |
| NiAlphaController | Data Ref |
| NiMaterialColorController / NiLightColorController | [v10: targetColor u16] + Data Ref (NiPoint3Interp chain, interpolator NOT read < 0x0A020000) |
| NiPSysEmitterCtlr | modifierName SizedString + emitterLink (v ≤ 0x0A010000) |
| NiPSysUpdateCtlr / NiPSysResetOnLoopCtlr | none |
| NiPSysModifierActiveCtlr | modifierName + unknownLink u32 (v ≤ 0x0A010000) |
| NiLookAtController | [v10: unknown1 u16] + lookAtNode Ref |

## NiFlipController — CONFIRMED semantics (iteration 24 canon)

69 flip models in the 2003 corpus. `delta` = seconds per frame
(byte-verified 114/114: 30 fps × 49, 15 fps × 35; e.g. 0.0333 s; the smoke
model 28939 = 8 textures @30fps). sources[] = texture refs cycled by time.

## NiKeyframeData — CONFIRMED (C12-B; 72,552 in 9.3.5)

Interpolation KeyType enum: 1=LINEAR, 2=QUADRATIC, 3=TBC, 4=XYZ euler,
5=CONST (treated as LINEAR).

```
numRotationKeys u32
if != 0: rotationType u32
if rotationType != 4 (quaternion path):
  per key: time f32 + quat (w,x,y,z × f32)
  [QUADRATIC quaternions forced LINEAR — no tangents]
  [TBC: + tension, bias, continuity f32]
if rotationType == 4 (XYZ euler):
  [v ≤ 0x0A010000: unknownFloat f32]     <- PE-specific extra!
  3 axis groups: numKeys u32 [+ interpolation u32]
    per key: time f32 + value f32
    [QUAD: + forward, backward] [TBC: + t,b,c]
translations: numKeys u32 [+ interp u32]
  per key: time f32 + Vec3 [+ QUAD: 2×Vec3] [+ TBC: 3×f32]
scales: numKeys u32 [+ interp u32]
  per key: time f32 + value f32 [+ QUAD: 2×f32] [+ TBC: 3×f32]
```

Corpus stats (2003): 62,984 LINEAR quats / 6,401 TBC / 112 QUAD /
1,021 XYZ-euler key groups. Both doors 496215/496216 use XYZ-euler QUAD
rotation + 801/501-key LINEAR translation at 30 Hz (era window [0, 26.67] s).

## NiTextKeyExtraData — CONFIRMED (C11)

```
v4:  ExtraData base (link) + unknownInt1 u32
v10: ExtraData base (name) — NO unknownInt1
numTextKeys u32
per key: time f32 + text SizedString     <- LINEAR, never TBC
```
Text keys = animation clip markers ("idle", "walk", door open/close...).
1,039 instances in 9.3.5.

## Key data blocks — CONFIRMED

- **NiFloatData** = KeyGroup\<f32\>
- **NiPosData** = KeyGroup\<Vec3\>
- **NiColorData** = KeyGroup\<Color4\>
- **NiUVData** = 4 × KeyGroup\<f32\> (U offset, V offset, U tiling, V tiling)
- **NiVisData** = u32 count + (time f32 + value u8) per key (LINEAR only)

KeyGroup\<T\> shape:
```
numKeys u32
if != 0: interpolation u32
per key: time f32 + value T
  [QUAD: + forward T, backward T]  [TBC: + tension, bias, continuity f32]
```

## NiArkAnimationExtraData

See [08 — Ark proprietary blocks](08-ark-proprietary.md) — this is MindArk's
own animation metadata carrier (one per file: 5,596 in 9.3.5), with the
TEXT_CRLF grammar carrying per-node animation data.
