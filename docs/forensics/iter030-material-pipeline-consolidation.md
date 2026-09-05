# ITER-30 — The 9.3.5 Terrain Material Pipeline: Consolidated Specification

**Binary:** `Entropia.exe` 9.3.5.6746, SHA256 `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31`
(all addresses VA, image base 0x00400000; evidence prefix `iter030_*`)

This document consolidates the CONFIRMED end-to-end terrain material
pipeline of the 9.3.5 client (Gate B, M1) — including the residual role of
the TDF material masks, resolved this iteration — into one auditable spec.
Every stage cites the function addresses and the evidence pointers.

---

## 1. Input inventory (LOCAL vs PATCHER-delivered)

| input | resource id | container | status (local corpora) |
|---|---|---|---|
| Global 257×257 height field (24bpp TGA; heights = (t−128)×5 m; origin −65536, 512-unit texels) | 429259 (0x68CCB) | `Textures\Textures.bnt` entry 71 (PCG) / 2785 (EU2008), byte-identical | **LOCAL** |
| 65×65 climate byte grid (R = palette climate byte, G = detail id, B = third) | 432502 (0x698F6) | nowhere in 178 scanned containers | **MISSING (patcher-delivered)** |
| 129×129 detail-texture-id selectors (R/G/B → tables C/D/E) | 459344 (0x70060) | nowhere in 178 scanned containers | **MISSING (patcher-delivered)** |
| 17 climate palettes 64×256×32bpp RGBA + 79 detail textures 256×256×24 | hardcoded ids in the manager ctor tables A/C/D/E | `Textures.bnt` (96/96 verified) | **LOCAL** |
| Per-tile TDF payloads (heights + typed layers) | type-0x6e resources | `Data\Terrain\terrain.bnt` (BNT2, 51,920 tiles + sentinel) | **LOCAL** |
| `Textures\Terrain.bnt` | — | 12-byte empty BNT2 stub (install-time orphan, no code path writes or mounts it) | **ABSENT (orphan)** |

The fetch chain: `FUN_00416390` builds the id array → `FUN_0044d590` →
`FUN_0044d360` → `FUN_00938f50` (3× `FUN_006ba110` type-100 fetch; dims
validated 257/65/129) → the 9-buffer grid bank (`FUN_0094a9e0`; splits
`FUN_0094aac0/ab50/ab90`). A total miss inserts the id into the
ArkResourceManager known-missing RB-tree (`FUN_008237d0`) and **halts client
init** (`FUN_004172a0`). The type-100 provider set is exactly
`UI\ui.bnt` + `Textures\textures.bnt` (`FUN_005b3fc0`).

---

## 2. The TDF tile payload = a serialized MaTerrainMapPatch (NEW, this iteration)

The terrain.bnt per-tile record framing
`[02 00 00 FF][u32 decompressed_size][zlib]` is **the client's own patch
serialization format**, byte-proven from the writer side:

- **Serializer** (patch vtable `0xa97c2c` slot 2): `FUN_00934bd0` →
  `FUN_00934970`. It walks the patch's intrusive slist of typed layers
  (layer flag `+0x34 == 1` = serialized), serializes each layer via
  `FUN_009383f0`, optionally zlib-compresses (`FUN_0095f390`, level 8) and
  emits `[u32 0xFF000002][u32 size][zlib]` — or `[u32 0xFF000001][raw]`
  when compression does not shrink. This is byte-exactly the terrain.bnt
  record framing (era-validated on the PCG corpus, iter019/020).
- **Layer record format** (the `[size][dim]` records of the material tail):
  `[u32 size][u32 dim][u32 bps][u32 type][u32 sub][u32 param5][32-byte
  name-block][FUN_00938040 sub-block][data]` — the 52-byte pre-mask header
  = dim/bps/type/sub/param5 + the 32-byte name block. This reconciles the
  two historical offset spaces: the "52-byte TDF header + 12-byte
  sub-header" = `[u32 count][u32 patch_field][u32 size][52-byte type-0
  layer header]` and the heights at payload 64..2112 are the type-0 layer
  data (dim 32, bps 2, type 0).
- **Typed layer census** (record `type` field, decoded from the data +
  binary): `0` = u16 heights (dim 32, bps 2), `2` = per-material masks
  (dim 16 coarse / 256 fine, bps 1, sub = the material's texture id —
  e.g. Stone04 = 13382), `3` = dim-32 mask layers, `6` = sub-id'd special
  planes (water-path lead; consumed via `FUN_00934890` →
  `FUN_00953340` plane geometry in the LOD ring), `7` = u16 normals
  (computed, not stored), `9` = dim-4, `0xa` = dim-8 system layers.
- **Parse/mount chain**: `FUN_0041dae0` opens `Data\Terrain\terrain.bnt`
  (string refs 0xa7a7e4/0xa7a8ac) from the client init gate
  `FUN_004172a0`; the patch lookup `FUN_00935870` triggers the tile fetch
  `FUN_00934670` (type-0x6e resource via the provider walk
  `FUN_00823c10`) and the post-load hook `FUN_009354f0`. The post-load
  hook processes layer types {0, 2, 3}: for each, `FUN_009348c0` resamples
  the same-(type,sub) layer of the east/south neighbor patches
  (`FUN_00935200` fetches the 3 neighbors) into the layer's edge buffers
  +8/+0xC (`FUN_00937ac0`/`FUN_009377c0` — the LOD up/downsamplers) for
  seamless tile-border blending; then `FUN_009362d0` computes the type-7
  normals from the type-0 heights (+ neighbor edges).
- The exact deserialization loop inside the mount/provider remains an
  honest bound (the mount function is a multi-KB timeout case); the format
  is proven from the writer side + the full field semantics from the
  consumers + the data side.

---

## 3. The CONFIRMED material assembly (the climate pipeline)

Per tile (128×128 world units; the material objects are keyed by the tile
grid — `FUN_00950810` ctor, slots [9]=x [10]=y; driver `FUN_0093f800`:

1. **Fetch-or-bake gate** `FUN_0093f1d0`: fetch the per-tile base texture
   resource `{type 0x82, key=tilekey}` and the factor
   `{0x82, tilekey|0x80000000}` (`FUN_006b9e80/006b9eb0`). Validity: base
   square ≤256, factor square ≤64. On miss/invalid → **the CPU bake**
   `FUN_0093eb50` → both are registered in-memory (`FUN_00826880`); no
   persistence path exists (the TerrainImageCache VFS record-writer
   negative, iter026; the caches are empty in every shipped state).
2. **The CPU bake** `FUN_0093eb50`: S = max(256, (x2−x1)×2); creates the
   BASE NiPixelData S×S RGBA (memset 0) + the FACTOR (S/4)² RGBA; 3 RNG
   seeds; the (S/4)² float accumulator; 4 corner-tile flags; then
   `FUN_0093d9a0(mgr, pos, mode 0)` — the data walk:
   - 4-corner climate sampling `FUN_00939a30` (the 65×65 byte grid at
     *(mgr+0xC)+0xC, 1024-unit cells, origin −32768) → up to 4 palettes
     via table A (mgr+0x40, 256 entries, 17 distinct ids [0..16],
     default 0x66DC7) → fetch `FUN_00938e30` → cache mgr+0x440;
     bilinear per-RGBA-byte corner blend `FUN_00938900`.
   - The ArkHeightTree quadtree walk over the tile bbox
     (`FUN_00938d00` overlap): each leaf accumulates
     `clamp(FUN_00991880(leaf),0,1)×edge_falloff` into the quarter-res
     accumulator. The leaf heights = the GLOBAL field (bank[0])
     bilinear (`FUN_00947a40`, stride 0x101) + position-keyed noise
     (`FUN_004059c0`, a Java-LCG draw — `FUN_004058a0/00405920`) +
     slope (`FUN_00947b20`), clamped [−20, +512]
     (constants 0xa97dc8 f32 / 0xa97c88 f64).
   - The base paint `FUN_00939c40` (×4 corner calls + the factor marker
     call): **row = clamp(ftol(255×(1 − ((slot[c]+slot[4])/2 − 2)/512 −
     noise2[cursor])), 0, 254)** — the altitude axis (constants 0xa7d748
     255.0, 0xa7af9c 2.0, 0xa7b0b8 512.0); **col = clamp(ftol(63×
     (noise1[cursor] + accumulatorSample)), 0, 62)** (0xa97cb0);
     base texel = palette[(row×64 + col)×4], RGB written with A=255
     (`FUN_00938870`).
   - The FACTOR write (the marker path): blended palette **ALPHA** →
     one-hot channel: **α ≥ 73 → R=255; 53 ≤ α < 73 → G=255; α < 53 →
     B=255; A=255 always** (thresholds _DAT_00a97c90=73.0 /
     _DAT_00a97c98=53.0). NO normalization exists or is needed (one-hot
     ∈ {0,1} per pixel; the shader's unrenormalized weighted sum can
     never saturate).
3. **Detail slots** `FUN_00939900` (called per material, sole caller the
   driver at 0x0093ff46's loop): position query `FUN_009510a0` (the
   center tile key = mgr+0x24/+0x28 + 0x40) → `FUN_00938da0` samples the
   **129×129 selector grid** ((pos+0x8000)>>9, index gx×0x81+gy) →
   tables **C/D/E** (mgr+0xC40/+0x1040/+0x1440) → 3 texture ids →
   `FUN_006ba110` fetches → the material's 3 detail slots. The tables are
   hardcoded in the manager ctor `FUN_0093cbf0` (defaults C=0x7003D,
   D=0, E=0x70028 + per-index overrides; e.g. selector byte 0 →
   C[0]=0x70027, D[0]=0x70027, E[0]=0x70028).
4. **The shader** — Terrain_14 (materials.vfs record 0x3EA, byte-extract
   SHA 5AE4AF81…): `D = d0×w0 + d1×w1 + d2×w2` (w = factor RGB/255,
   unrenormalized) → per-channel overlay onto the base keyed on D
   (D≥0.5: 1−2(1−b)(1−D) else 2bD) → **shadow = `mul r0, r0, r0.a` (the
   BASE TEXTURE ALPHA is a shadow/darkening field!)** → light → fog.
   Vertex stage: one patch-local texcoord; details repeat 32/32/16;
   sampler states: base+factor CLAMP/LINEAR/LINEAR/POINT-mip, details
   WRAP/LINEAR/LINEAR/LINEAR with MipMapLodBias −0.5. The 5-slot binding
   `FUN_00950bf0` (mode 2) maps slots 0..4 = base/factor/detail1..3
   1:1 to the samplers. Ark11 (0x3ED) is the mode-1 fallback
   (`FUN_009518e0`: 3EA→+0x1B4, 3EB→+0x1B8 water, 3ED fallback).

**The BASE texture per cell is the CPU-baked palette paint** — not a TDF
material, not a per-tile file id. The `{0x82,key}` pair is the bake's own
in-memory cache.

---

## 4. The residual role of the TDF material masks (P0 ANSWER)

The per-material mask layers (type 2: the dim-16 named records with the
material's texture id at record+16, plus the dim-256 fine-mask variants;
region A tiles carry ~7, region B ~11, PCG census iter030) are **parsed,
edge-extended, and consumed by the LOD mesh vertex-color bake** — NOT by
the climate material assembly:

1. **The LOD ring builder** `FUN_00941f90` (distance-sorted per-tile LOD
   densities 256/128/64/32; the tess-init `FUN_00944bf0` pre-creates
   per-tile slots + NiTriShape + NiVertexColorProperty + the Ark11
   default) calls **`FUN_00941710`** per tile: it walks the patch's
   type-2 layers in record order, fetches each layer's own texture by the
   sub-id (`FUN_006ba150(sub)` — the material's 256×256 TGA), and:
   - the FIRST layer: `FUN_00940b50` — initialize the mesh vertex-color
     buffer by resampling the texture to the mesh density;
   - subsequent layers: `FUN_00940de0` — per vertex, resample the mask
     (16×16/256×256 → the mesh LOD density, using the layer's own edge
     buffers +8/+0xC filled at load for seamless tile borders) and
     **blend: vertexColor = lerp(vertexColor, materialTexture(u,v),
     mask/255)** (`(tex−dst)×mask>>8 + dst`);
   - the type-3 layer (`FUN_009402b0`, when flagged) — the same
     mask-weighted blend from the dim-32 layer;
   - the flag path (`FUN_00940230`) halves the RGB of a bottom band
     (an edge-darkening band).
   The result feeds the per-tile **vertex colors** — the ambient/light
   tint consumed by the Terrain_14 vertex stage
   (`ArkLight(W, F.Color0, …)` → `F.Color0 *= heightFactor`), i.e. the
   masks drive the per-tile LIGHTING COLOR of the mesh, while the
   base/factor/detail TEXELS come from the climate system.
2. **The zone system** (the 0x00958xxx cluster, the
   TerrainEditZones/.tez consumers): zone objects {mode@+0xC,
   gridX@+0x10, gridY@+0x14} apply via `FUN_00958930`:
   - mode 0 → `FUN_00943000`: rasterize the zone's source mask
     (descriptor {x,y,stride,count,scale,data,end}) into the patches'
     type-2 **sub-0 scratch layers** (created empty on miss,
     `FUN_009376f0(0x100,1,2,0,0,0)`), value = (255−mask)×0.8+0.5
     (constants 0xa7af78/0xa79a08), max-blend (`FUN_00942cf0`), then
     dirty-flag the patches (`FUN_0094b7f0` → the LOD refresh queue
     `FUN_00941ea0`); cleared via `FUN_009589d0` → `FUN_009429c0`.
   - mode 1 → `FUN_0093e3b0`: paint the zone mask directly into the
     material object's **BASE NiPixelData** — RGB modulation
     (tex×mask/255) in Ark11 mode, **ALPHA modulation** (α×mask/255) in
     Terrain_14 mode with edge falloff (8.0, 1/256) and noise — i.e.
     the zones paint the SHADOW field (`mul r0, r0, r0.a`).
3. **What the masks do NOT feed** (exhaustive census, 838/838 functions
   of the terrain range decompiled): the base texture (climate palettes),
   the factor texture (palette-alpha one-hot), the detail selection
   (129×129 global selectors via tables C/D/E). No other type-2 reader
   exists; the slist walkers are fully enumerated
   (`FUN_009347e0` typed-get users, `FUN_00934890` type-6,
   `FUN_009354f0` post-load, `FUN_00941710` the LOD mask reader,
   `FUN_00934970` the serializer, `FUN_00934d40` the dtor).

**Verdict:** the TDF material masks are NOT legacy-unused and NOT the
base/factor/detail source. Their residual 9.3.5 role = the per-tile
**vertex-color (lighting tint) bake** of the LOD meshes + the zone
shadow-paint carrier; the VISUAL texel material moved to the global
climate pipeline (which the missing 65×65/129×129 grids drive).

---

## 5. Era-honest MISSING list (the clean-runtime inputs)

MISSING locally (patcher-delivered; NO local container carries them —
the 178-container negative, iter029):

- the 65×65 **climate byte grid** (id 432502 R channel) → the palette
  selection per location cannot be computed from the local corpus;
- the 129×129 **detail selector grids** (id 459344 R/G/B) → the per-cell
  detail selection cannot be computed locally.

Everything else is local: the global height field (429259), the 17
palettes + 79 detail textures (hardcoded table ids, all in Textures.bnt),
the TDF tiles (heights + masks + per-material texture ids), the Terrain_14
shader byte-extract, and the full mechanism chain.

The clean runtime implements the mechanism with EXPLICIT era-bounded
placeholders for the two missing grids (see
`terrain/materials_confirmed.js`): a constant climate byte → table A[0] =
palette 0x66DC6, and a constant selector byte → C[0]/D[0]/E[0] =
0x70027/0x70027/0x70028 — every placeholder labeled, no historical-truth
claim.

## 6. Evidence

`99_Audits/PE_MILESTONE_1_WORLD_SURFACE_R1/03_EVIDENCE/iter030_*.json`
(census, constants, decompile corpus index, the PCG tile census) +
`04_SESSIONs/ITER044_TDFROLE_RUN/logs/` (60+ fresh decompiles, raw Ghidra
logs, script hashes). Prior-iteration evidence cross-referenced inline
(iter024–029).
