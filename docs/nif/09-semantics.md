# 09 — Semantics beyond parsing

## Coordinate system & units

- NIF data is **Z-up**; render conversion (Y-up): `(x, z, -y)` — position
  AND quaternion axes. CONFIRMED (museum/era math, viewer-verified).
- Units ≈ centimeters (buildings ~2,000 NIF units ≈ 21 m at 0.01 GLB scale).
- NIF local transforms (translation Vec3 + rotation Mat33 + scale f32 on
  NiNode/NiTriShape) are **model-local hierarchy transforms ONLY**.

## REJECTED — NIF local transform is NOT world placement

Tested extensively (placement census, 23 encodings × 29 anchors × 5 corpora
= 1,975 files): no tested encoding of static placement exists in client
files. Canonical status:
- DIRECT_STATIC_PLACEMENT_IN_TESTED_ENCODINGS = REJECTED
- SERVER_DELIVERED_PLACEMENT = STRONGLY_SUPPORTED (NOT CONFIRMED — origin
  trace pending)
- PLACEMENT_ORIGIN = UNRESOLVED / OPEN_FOR_FALSIFICATION
- The 29-anchor teleport table in scripts (3078) = the ONLY local
  coordinate table (Port Atlantis 6055, 8442 / PA 6055, 22278 era variants).
Never use NIF transforms as world coordinates.

## Texture binding chain (M3, CONFIRMED)

How a NIF mesh finds its textures in PE (NOT the standard Gamebryo path —
the era uses Ark blocks):

```
NiTriShape → properties → NiTexturingProperty (slot 0 = BASE, ...)
mesh → NiArkTextureExtraData entries
  entry name (e.g. "Stone04") + ref + bnt2_id (9 trailing bytes)
  bnt2_id → Textures.bnt (BNT2) payload = TGA 2.0 uncompressed 256×256×24
ArkTexture bytes[5:8] u32 LE = BNT2 texture ID (99.86% — 23,488 entries,
23,455 resolved, 33 dangling = SuperSpray particle slots, 14 unique IDs)
```
Binding edges (M3-4.5 V2, machine-validated): 20,427 static (Jaccard
1.000000 vs builder; negative control 0.0), 148 controller edges (125
NiFlipController), 1,749 effect edges (1,646 NiTextureEffect). 200/200
witnesses field-matched. **STATIC binding = CONFIRMED.**

Per-mesh binding tiers (viewer-proven, 167/167 exact on 12 multi-mesh
buildings): mesh_block data_id → geometry-name sanitizeNodeName+BB →
traversal order → bbox+vertex-count.

## Material IR (M3-5A, CONFIRMED)

16,080 material records; slots: BASE=13,928, DARK=1,785, DETAIL=199,
GLOSS=2,707, GLOW=1,531, BUMP=636, DECAL=0.
**Enum identity ≠ modern semantics**: GLOSS ≠ roughness, BUMP ≠ normalMap
(REJECTED as overclaims). Non-BASE slot semantics = M3-5B OPEN (needs
runtime/D3D8 evidence).

## Skinning & animation semantics

- LBS formula: `v' = Σ w · W_bone(t) · X_b · S · v` — CONFIRMED empirically.
- Era pattern: mesh NIF + separate ANIMATION_SKELETON NIF, paired
  cross-file **by bone NAME**; only 7 models (2003) carry in-file keyframes
  AND skinning.
- Timing: NiFlipController delta = seconds/frame (30/15 fps corpus);
  keyframe era window e.g. doors [0, 26.67] s @ 30 Hz.

## Known exporter quirks (for anyone rebuilding assets)

- v10 NiTriShape hasShader u8 sits between skinRef and shaderName —
  missing it shifts every following boundary by 1 byte.
- NiVertexColorProperty has a PE-only u32 after lightingMode.
- NiArkTexture `num_tex` is always 3 — the real entry count is packed in
  field2 bits 8..31.
- BNT/BUNT archives: every entry's packedSize spans 8 bytes into the next
  entry's zlib stream (trailing 8 = next header) — strict decompressors
  (Chromium DecompressionStream) reject the stream; Node zlib tolerates.
- ArkTexture names ↔ texture IDs are many-to-many (id ↔ name ≠ 1:1).
