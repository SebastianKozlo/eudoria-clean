# 07 — Skinning

Status: layouts CONFIRMED (C20/C21 + 4-model byte-exact boundary proof);
formula CONFIRMED empirically (iteration 27: v' = Σ w · W_bone(t) · X_b ·
S · v; 204828 dev 1.7e-4 across 40 bones; 20/20 viewer trace EXACT).

Corpus: 720 NiSkinInstance+NiSkinData in 9.3.5 (2003: 316 carriers / 623
pairs — categories: creatures 152, avatar 85, armor 68, weapon 11).
Only 7 models (2003) have skinning AND in-file keyframes — **the era's
pattern is cross-file**: mesh-NIF + separate ANIMATION_SKELETON NIF paired
by bone NAME (not by ID).

## NiSkinInstance — CONFIRMED

```
data Ref (→ NiSkinData)
skinPartition Ref          <- v ≥ 0x0A020000 only — NOT in PE... but see NiSkinData note
skeletonRoot Ref (→ NiNode)
numBones u32
bones Ref[] (→ NiNode per bone)
```

## NiSkinData — CONFIRMED

```
overall skin transform: rotation Mat33 + translation Vec3 + scale f32
numBones u32
[skinPartition link u32 — for 0x04000002 ≤ v ≤ 0x0A010000: BOTH PE versions read it]
[hasVertexWeights u8 — only v ≥ 0x04020100: PE v10 YES, PE v4 NO]
per bone:
  boneTransform: rotation Mat33 + translation Vec3 + scale f32
  boundingSphereOffset Vec3 + boundingSphereRadius f32
  numVertices u16
  vertexWeights: (index u16 + weight f32) × numVertices
    v4 (≤ 0x04020100): ALWAYS read
    v10: read only if hasVertexWeights
```
PE-specific deviations from the oracle (byte-documented, iteration 27):
bind offset C ≠ identity in PE data; file pose ≠ bind pose; root named
"Scene Root"; partition links are -1 in some files.

## NiSkinPartition — CONFIRMED (C21)

```
numPartitions u32
per partition:
  numVertices u16, numTriangles u16, numBones u16, numStrips u16,
  numWeightsPerVertex u16
  bones u16[numBones]
  v4 (≤ 0x0A000102):  vertexMap u16[] unconditional; vertexWeights f32[][] unconditional
  v10 (≥ 0x0A010000): hasVertexMap bool → optional vertexMap; hasVertexWeights
                      bool → optional weights; hasFaces bool → strips/triangles
  stripLengths u16[numStrips]
  faces: v4 by numStrips; v10 additionally gated by hasFaces
  hasBoneIndices bool → boneIndices u8[vertices][weightsPerVertex]
```
116 instances in 9.3.5 (v4 layout: 0 occurrences — PE v4 files use the
unconditional path).

## Runtime math (for implementers)

- Bone hierarchy: walk NiNode parents from skeletonRoot using local
  transforms (Mat33 rotation, Vec3 translation, scale).
- W_bone(t) = animated world matrix of the bone at time t; X_b = inverse
  bind (from NiSkinData bone transform); S = overall skin transform.
- Evaluate in NIF (Z-up) space, then apply the Z-up→Y-up flip once at
  render boundary: `(x, z, -y)`.
- Animation clips pair CROSS-FILE by bone name; era files store clips with
  NiTextKeyExtraData markers.
