# 04 — Property blocks (materials, texturing, render states)

## NiMaterialProperty — CONFIRMED

```
NiObjectNET
[Flags u16 — ONLY v ≤ 10.0.1.2 (PE v10 does NOT have it)]
ambient  Color3
diffuse  Color3
specular Color3
emissive Color3
glossiness f32
alpha    f32
```
11,563 instances in 9.3.5. Classic Phong-era parameters — NOT PBR
(glossiness ≠ roughness).

## NiTexturingProperty v4 (4.1.0.12) — CONFIRMED (G1, 693/693)

```
NiObjectNET (v4 shape)
Flags u16
ApplyMode u32
TextureCount u32
per slot 0..TextureCount-1:
  Has u8
  if Has == 1:
    Source i32 (Ref → NiSourceTexture or effect block)
    Clamp u32
    Filter u32
    UVSet u32
    PS2_L i16, PS2_K i16, unknown1 u16      <- 22-byte TexDesc
```

## NiTexturingProperty v10 (10.1.0.0) — CONFIRMED (G3+B24, 2049/2049)

```
NiObjectNET (v10 shape)
field_A u16, field_B u16          <- replaces the u16 Flags
TexCount u32
per slot:
  Has u8
  if 1:
    Source i32, Clamp u32, Filter u32, UVSet u32
    tail_A i16, tail_B i16
    transform_present u8
      if 1: 32-byte transform payload (raw)
      if 0: nothing; other values = parse error
after slot 5: if slot5.Has == 1 → 24-byte bump payload (raw)
trailing u32 (always 0)
```

Slot indices (standard Gamebryo): 0=BASE, 1=DARK, 2=DETAIL, 3=GLOSS,
4=GLOW, 5=BUMP, 6=DECAL. **Slot identity ≠ proven modern render semantics**
(M3-5A: enum identity preserved; GLOSS≠roughness, BUMP≠normalMap — REJECTED
as overclaims; see 09-semantics.md).

## NiZBufferProperty — CONFIRMED

```
NiObjectNET
Flags u16
[Function u32 — ONLY v ≥ 0x0401000C]   <- v4.0.0.2 lacks it (R58 fix)
```

## NiStencilProperty — CONFIRMED (the 23-byte trap)

```
NiObjectNET
[Flags u16 — only v ≤ 0x0A000102 (PE v4 YES, v10 NO)]
[if v ≤ 0x14000005 (both PE versions):  stencilEnabled u8, stencilFunction u32,
  stencilRef u32, stencilMask u32, failAction u32, zFailAction u32,
  passAction u32, drawMode u32]   <- 29 bytes
```
The old 6-byte parse caused a 23-byte deficit corrupting every later
boundary (M1D-02).

## NiAlphaProperty — CONFIRMED
`NET + Flags u16 + Threshold u8`

## NiVertexColorProperty — CONFIRMED (PE extension!)
```
NET + flags u16 + vertexMode u16 + lightingMode u16
+ unknown_pe_field u32   <- PE-SPECIFIC; ALWAYS consumed; values 0/1 in corpus
```
(M1D-32: seeking back when the field ≠ 1 created a phantom preamble —
never conditionally seek back.)

## NiSourceTexture — CONFIRMED (M1D-34/38/39)

```
NiObjectNET
useExternal u8
if 1: fileName SizedString [+ v10: unknownLink u32]
else: [v10: fileName SizedString] [v4: unknown u8] + pixelDataRef u32
pixelLayout u32, useMipmaps u32, alphaFormat u32, isStatic u8
[v10 && internal: extra u32 (value 0)]
```
45 instances in 9.3.5 (embedded textures are rare; the normal path is
ArkTexture → BNT2 external — see 09-semantics).

## NiPixelData v10 (embedded pixels) — CONFIRMED (M1D-38/40)

```
pixelFormat u32, r/g/b/a masks ×4 u32, bitsPerPixel u8,
unknown3 B, unknown8 B,
palette u32 (Ref), numMipmaps u32, bytesPerPixel u32,
mipmaps: width u32 + height u32 + offset u32 each,
numPixels u32   <- TOTAL BYTE SIZE, not pixel count (262143 = 87381 px × 3 B!)
[skip numPixels bytes]
```

## One-flag properties — CONFIRMED
`NiSpecularProperty / NiDitherProperty / NiShadeProperty` = NET + Flags u16.
`NiFogProperty` = NET + flags u16 + fogDepth f32 + fogColor Color3.
