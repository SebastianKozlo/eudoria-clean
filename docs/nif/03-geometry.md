# 03 — Geometry blocks

Status: CONFIRMED (byte traces C9-A/C18-A + full-corpus regression + niflib
agreement; v10 layout corrected after the hasShader 1-byte fix — C9-A traces
made BEFORE that fix were wrong, superseded).

## NiTriShape (container)

```
NiObjectNET   (name, extraData, controller — version-shaped)
NiAVObject    (flags, translation, rotation, scale, properties [+v4 velocity/bbox | v10 collision])
Data(Ref)     — i32 → NiTriShapeData block
Skin(Ref)     — i32 → NiSkinInstance block (-1 if none)
[v10] hasShader(u8); if != 0: shaderName(SizedString) + unknown u32
```

## NiTriShapeData v4 (4.1.0.12) — read order

```
numVertices u16
hasVertices bool
  vertices Vec3 × numVertices
hasNormals bool
  normals Vec3 × numVertices
center Vec3
radius f32
hasVertexColors bool
  vertexColors Color4 × numVertices
numUvSets u16                 <- LATE (after vertex colors)
[hasUv bool — ONLY v4.0.0.2]  <- 4-byte bool
uvSets TexCoord × (numUvSets & 63) × numVertices
numTriangles u16
numTrianglePoints u32         <- should be numTriangles × 3
triangles (u16,u16,u16) × numTriangles   <- UNCONDITIONAL (no flag)
numMatchGroups u16
matchGroups: count u16 + indices u16[] each
```

## NiTriShapeData v10 (10.1.0.0) — DIFFERENT read order!

```
numVertices u16
keepFlags u8                  <- v10 only
compressFlags u8              <- v10 only
hasVertices bool
  vertices Vec3 × numVertices
numUvSets u16                 <- EARLY (before normals!)
hasNormals bool
  normals Vec3 × numVertices
  [if numUvSets & 0xF000: tangents + bitangents Vec3 × numVertices each]
center Vec3
radius f32
hasVertexColors bool
  vertexColors Color4 × numVertices
uvSets TexCoord × (numUvSets & 63) × numVertices
consistencyFlags u16          <- v10 only
numTriangles u16
numTrianglePoints u32
hasTriangles bool             <- v10 only
  triangles (u16,u16,u16) × numTriangles
numMatchGroups u16
matchgroups (as v4)
```

Critical facts:
- `numUvSets & 63` = number of UV sets actually present (lower 6 bits).
- `numUvSets & 0xF000` = tangent/bitangent presence flag (only 1 corpus
  outlier ever set it: 417906.nif).
- v4 has `hasUv` ONLY in 4.0.0.2 (4-byte bool). Missing this single field
  was the R60 fix that restored 52555.nif.
- niflib accepts `hasX=true + numVertices=0` (reads zero arrays) — do NOT
  hard-fail on that combination (M1D-16).
- `numTrianglePoints` is a byte-size guard (numTriangles × 3), sanity cap
  200,000 in parser.

## What the geometry means (semantics)

- Coordinates are in **NIF local space**, Z-up. Units ≈ centimeters
  (buildings ~2000 units ≈ 21 m at 0.01 scale — museum convention).
- Local transforms live on the PARENT NiNode/NiTriShape (translation Vec3,
  rotation Mat33, scale f32) — NOT baked into vertices.
- UV convention: v-flip needed for OpenGL-style rendering (`v' = 1 - v`) —
  the exporter convention drift caused the historical V-mirror bug
  (nif_glb_exporter_uvc_v1 is the corrected converter, 124/124 regression).
