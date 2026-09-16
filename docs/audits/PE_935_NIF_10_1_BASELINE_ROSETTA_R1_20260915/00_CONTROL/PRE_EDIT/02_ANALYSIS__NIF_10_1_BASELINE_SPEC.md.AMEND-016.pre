# NIF 10.1.0.0 Normalized Baseline Spec — PE_935_NIF_10_1_BASELINE_ROSETTA_R1

Scope: NIF VERSION = 10.1.0.0 (0x0A010000) ONLY. Derived EXCLUSIVELY from
pinned external oracles (SOURCE_REGISTRY.md): SRC-02 nifxml historical
0.7.1.1 (primary, era-closest), SRC-01 nifxml modern 0.10.0.0 (cross-check),
SRC-06 Gamebryo 1.2 engine source (framing truth), SRC-08/09 SDK + EE2
samples (cross-publisher physical controls). Machine-readable form:
`01_RAW/BASELINE_TYPE_TABLE.csv` (10,890 field rows; both oracles emitted;
conflicts in `01_RAW/BASELINE_CONFLICT_RAW.csv` + curated
`02_ANALYSIS/BASELINE_CONFLICT_MATRIX.csv`).

## File framing (engine-confirmed; applies to EVERY 10.1.0.0 file)

```
HeaderString      line, 0x0A-terminated ("Gamebryo File Format, Version 10.1.0.0")
Version           u32 = 0x0A010000
User Version      u32                      [>= 10.0.1.8; PE: 0 in 4838/4838]
Num Blocks        u32
Num Block Types   u16                      [>= 5.0.0.1]
Block Types       SizedString[num_block_types]   (u32 len + chars)
Block Type Index  u16[num_blocks]         (per-block type index)
Num Groups        u32                      [>= 5.0.0.6; PE: 0 in 4838/4838]
Group Sizes       u32[num_groups]
BLOCKS: num_blocks x { GroupID u32 [5.0.0.6 <= v < 10.1.0.114; PE: 0] + class payload }
TopObjects        u32 count + u32 refs[count]   (engine LoadTopLevelObjects)
EOF-exact
```

Engine sources (Gamebryo 1.2, NiStream.cpp / NiObject.cpp): LoadHeader →
LoadRTTI → LoadObjectGroups → per-block NiObject::LoadBinary (GroupID) →
LoadTopLevelObjects. THE PER-BLOCK GroupID IS THE FRAMING FACT THAT ALL
PUBLIC SCHEMAS MISS FOR 10.1.0.0 (conflict C-01: modern schema mis-versions
it as since=10.1.0.114; historical omits it; NiflySharp implements the
per-block u32 CORRECTLY for 10.1.0.0 — NiflySharp\NiObject.cs L61-62:
`if (stream.Version.FileVersion >= NiFileVersion.V10_0_0_0 &&
stream.Version.FileVersion < NiFileVersion.V10_1_0_114)
stream.Sync(ref groupId);` — no misalignment on real 10.1.0.0 files
[F-16/AMEND-010 corrects the former "header read would misalign" wording;
residual: NiflySharp's per-block range starts at 10.0.0.0 vs the engine's
5.0.0.6 — a 5.x–9.x-only difference, out of this run's 10.1 scope]).

## Primitives (10.1)

bool=1B (4-byte only for v <= 4.0.0.2), u8/i8=1, u16/i16=2, u32/i32=4,
f32=4, Vec3=12, Mat33=36, Color3=12, Color4=16, TexCoord=8,
SizedString/FilePath=u32+chars, Ref/Ptr=i32 (-1=NULL).

## Type table for the world slice (validated classes — closure-proven)

Effective field order = inheritance chain (parent first). APPLIES_TO_10_1
per type in BASELINE_TYPE_TABLE.csv. Key chains (all closure-validated on
Entropia bytes this run; see HOLDOUT_RESULTS.csv):

- NiObjectNET: Name; Num Extra Data List u32; Extra Data List Ref[];
  Controller Ref.
- NiAVObject = NET + Flags u16; Translation Vec3; Rotation Mat33; Scale f32;
  Num Properties u32; Properties Ref[]; Collision Object Ref (>=10.0.1.0).
  (Velocity/HasBoundingBox only <= 4.2.2.0.)
- NiNode = NiAVObject + Num Children; Children Ref[]; Num Effects; Effects Ref[].
- NiGeometry = NiAVObject + Data Ref; Skin Instance Ref (>=3.3.0.13);
  Has Shader u8 (10.0.1.0..20.1.0.3) [+ Shader Name SizedString + Unknown Int
  i32 if set]; (20.x material arrays absent).
- NiTriShape = NiGeometry (no own fields).
- NiGeometryData: Num Vertices u16; Keep Flags u8 (>=10.1.0.0); Compress Flags
  u8 (>=10.1.0.0); Has Vertices + Vertices[]; Num UV Sets u8 (>=10.0.1.0) +
  Extra Vectors Flags u8 (>=10.0.1.0); Has Normals + Normals[]; [Tangents/
  Bitangents if (ExtraVectorsFlags & 16) and Has Normals, >=10.1.0.0];
  Center; Radius; Has Vertex Colors + Colors[]; UV Sets [(NumUVSets&63) x
  NumVertices]; Consistency Flags u16 (>=10.0.1.0).
- NiTriBasedGeomData = NiGeometryData + Num Triangles u16.
- NiTriShapeData = NiTriBasedGeomData + Num Triangle Points u32; Has Triangles
  u8 (>=10.1.0.0); Triangles [3xu16] x NumTriangles; Num Match Groups u16;
  Match Groups (u16 count + u16 indices).
- NiProperty = NiObjectNET (no own fields).
- NiMaterialProperty = NiProperty + Ambient/Diffuse/Specular/Emissive Color3 +
  Glossiness f32 + Alpha f32 (Flags ONLY <=10.0.1.2 — absent in PE v10).
- NiTexturingProperty = NiProperty + Apply Mode u32 (<=20.0.0.5) + Texture
  Count u32 + per-slot Has+TexDesc (0..N-1) + Bump Luma Scale/Offset + Bump
  Map Matrix (cond slot5) + Num Shader Textures u32 (>=10.0.1.0; PE: 0) +
  ShaderTexDesc[]. TexDesc = Source Ref; Clamp u32; Filter u32; UV Set u32;
  PS2 L i16; PS2 K i16; Has Texture Transform u8 (>=10.1.0.0) + [Translation
  TexCoord; Tiling TexCoord; W Rotation f32; Transform Type u32; Center
  Offset TexCoord] (= the 32-byte "raw transform payload").
- NiZBufferProperty = NiProperty + Flags u16 + Function u32 (>=4.1.0.12).
- NiAlphaProperty = NiProperty + Flags u16 + Threshold u8.
- NiStencilProperty = NiProperty + Stencil Enabled u8 + Stencil Function u32 +
  Stencil Ref u32 + Stencil Mask u32 + Fail/ZFail/Pass Action u32 + Draw Mode
  u32 (Flags only <=10.0.1.2 — absent).
- NiVertexColorProperty = NiProperty + Flags u16 + Vertex Mode (u32 enum) +
  Lighting Mode (u32 enum). NOTE width-identical alternative split
  (u16+u16+u32) documented (conflict C-05) — same 10 bytes.
- NiExtraData (v10 base): Name only (Next Extra Data only <=4.2.2.0).
- NiStringExtraData = NiExtraData + String Data.
- NiIntegerExtraData = NiExtraData + Integer Data u32.
- NiBooleanExtraData = NiExtraData + Boolean Data u8.
- NiTimeController = NiObject + Next Controller Ref; Flags u16; Frequency/
  Phase/Start/Stop f32; Target Ref (30 bytes).
- NiDynamicEffect = NiAVObject + Num Affected Nodes u32 + Affected Nodes Ref[]
  (>=10.1.0.0).
- NiLight = NiDynamicEffect + Dimmer f32 + Ambient/Diffuse/Specular Color3.
- NiPointLight = NiLight + Constant/Linear/Quadratic Attenuation f32.
- NiSpotLight = NiPointLight + Cutoff Angle f32 + Exponent f32.
- NiDirectionalLight = NiLight. NiAmbientLight = NiLight.
- NiTextureEffect = NiDynamicEffect + Model Projection Matrix Mat33 + Model
  Projection Transform Vec3 + Texture Filtering u32 + Texture Clamping u32 +
  Texture Type u32 + Coordinate Generation Type u32 + Source Texture Ref +
  Clipping Plane u8 + Unknown Vector Vec3 + Unknown Float f32 + PS2 L i16 +
  PS2 K i16.
- NiBillboardNode = NiNode + Billboard Mode u16 (>=10.1.0.0).
- NiCollisionData = NiCollisionObject(target Ref) + Propagation Mode u32 +
  Collision Mode u32 (>=10.1.0.0) + Use ABV u8 + [Bounding Volume].
- NiSortAdjustNode = NiNode + Sorting Mode u32 + Unknown Int 2 i32 (<=10.2.0.0).
- NiSourceTexture = NiTexture + Use External u8 + [File Name + Unknown Link Ref]
  / [File Name + Pixel Data Ref] + Pixel Layout u32 + Use Mipmaps u32 +
  Alpha Format u32 + Is Static u8. (NOT closure-validated this run — deferred.)
- NiPixelData = ATextureRenderData + Num Pixels u32 + Pixel Data bytes. (NOT
  closure-validated this run — deferred.)

## Non-validated-in-this-run classes

All other observed types (controllers, skinning, particles, keyframe data,
morph, text keys — 45 of 76) are schema-defined (BASELINE_TYPE_TABLE.csv)
but NOT byte-validated here (explicit deferral with denominators in
NIF_10_1_STANDARD_COVERAGE.csv). Their classification is UNKNOWN for layout
in THIS run's evidence hierarchy (prior R61 closure exists as prior claim).

## Baseline conflicts

See 02_ANALYSIS/BASELINE_CONFLICT_MATRIX.csv (C-01..C-11). The load-bearing
conflicts C-01 (GroupID), C-07 (importer tail 41B), C-08 (ArkTexture
count — (field2>>8)&0xFFFFFF, 100% in-slice after the F-14 retraction;
corpus-wide outside the slice OPEN) are physically adjudicated from
Entropia + EE2/SDK bytes.
