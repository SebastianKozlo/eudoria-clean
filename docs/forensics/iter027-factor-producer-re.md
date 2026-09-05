# ITER-27: Terrain factor producer RE — material[2] writer + the bake arithmetic (Entropia.exe 9.3.5)

## Summary

Static RE (Ghidra 11.2.1, fresh project, sandbox copy SHA-verified `E7785430...`)
located the complete producer chain for the terrain FACTOR texture
(`material[2]`, sampler slot 1 of the Terrain_14 technique) and extracted the
exact reduction and normalization arithmetic. The factor content model is
rewritten from the previous "per-cell renormalized top-3 weights" hypothesis
to the engine's actual mechanism: **one-hot channel selection by a palette
alpha 3-band partition**. The code thresholds are byte-matched by the original
palette texture data.

## The producer chain

```
FUN_0093f800 (driver, RB-trees of 0x30 material objects)
  └─ FUN_00950810 ctor: [0]=mesh [1]=base map [2]=FACTOR map [3..5]=details
                         [9]/[10]=grid x/y
  └─ for mesh==0 and in range (FUN_0093d7d0):
       FUN_0093f1d0 (the material[2] WRITER)
         ├─ mat[1] = resource {type 0x82, key = tilekey}            (base)
         ├─ mat[2] = resource {type 0x82, key = tilekey|0x80000000} (FACTOR)
         ├─ validity: base square <= 256 px; FACTOR square <= 64 px
         ├─ on missing/invalid -> FUN_0093eb50 (CPU bake)
         ├─ register both via FUN_00826880 (in-memory resource registry)
         └─ FUN_00939900: mat[3..5] = 3 detail textures from the
                          per-tile material list (FUN_006ba110)
```

## The CPU bake (FUN_0093eb50 -> FUN_0093d9a0 -> FUN_00939c40)

- `S = max(256, span*2)`; BASE = NiPixelData S x S RGBA; **FACTOR = NiPixelData
  (S/4) x (S/4) RGBA, memset 0**. `FUN_007c3090` is the NiPixelData ctor
  (vtable write byte-proven) — the from-pixels path; no D3DX involved.
- 3 seeds drawn as random ints in [0, 1024) from the manager RNG; a
  `(S/4)^2` float accumulator grid is created and zeroed.
- FUN_0093d9a0 walks a bbox-overlap quadtree (children at +0/+4/+8/+0xC,
  half-size key `*(u32*)(node+0x44)>>5 & 0x7fffff`), accumulating
  `acc[cell] += clamp(noisy_ratio, 0, 1) * edge_falloff`, and samples the
  climate system per tile corner:
  - 65x65 byte climate grid, 1024-unit cells (world 64k x 64k), stride 0x41.
  - climate byte -> identity remap table (mgr+0x840, 255 -> -1) ->
    FUN_00938e30: texture by id from the manager's table A (mgr+0x40),
    cached at mgr+0x440, requires 32 bpp RGBA.

## The reduction rule (FUN_00939c40, factor path)

Per factor pixel (the S/4 x S/4 buffer):

```
blended_alpha = bilinear(palette_alpha, corner weights)   # 4 climate corners
if   blended_alpha >= 73.0: R = 0xFF   # _DAT_00a97c90 (double)
elif blended_alpha >= 53.0: G = 0xFF   # _DAT_00a97c98 (double)
else:                      B = 0xFF
A = 0xFF always
```

plus tile-edge channel switches driven by the 4 "corner tile present" flags for
climate-cell transitions. The palette COLUMN is
`63.0 * (noise_table[cursor++ & 0x3FF] + accumulated_weight)`: the per-cell
accumulated material weight plus noise picks where in the 64-column material
gradient the pixel falls, and the palette's alpha at that column selects
exactly one of the 3 detail channels.

## The normalization

**None is needed or performed.** The one-hot factor yields per-channel weights
in {0.0, 1.0} with at most one active channel per pixel, so the shader's
unrenormalized weighted sum `D = d0*w0 + d1*w1 + d2*w2` (Terrain_14,
iter-24-confirmed) can never exceed a single detail value — explaining the
0.0% white-saturation signature measured in iter-25/26. The earlier
"per-cell renormalization" hypothesis shared that signature but is not the
engine's arithmetic.

## Data-side confirmation (original PCG_9_3_5 Textures.bnt, read-only)

- All 96 hardcoded manager texture ids exist: **17 climate palettes
  (64x256, 32 bpp RGBA) + 79 detail textures (256x256, 24 bpp)** — 96/96.
- The palettes' per-column median alpha values: `{62, 85}` (15 palettes:
  24 G-columns + 40 R-columns); `0x6a427 = {45, 85}` (51 B-columns);
  `0x6a436 = {50, 51, 52, 53, 62, 82}` (full 3-band gradient, transitions at
  columns 4/28/32). **The code thresholds 53/73 byte-exactly partition the
  original alpha values** (62 -> G, 85 -> R, 45..52 -> B).

## Worked-example gate (18 proven-region tiles)

The extracted one-hot factor content under the confirmed Terrain_14 overlay
operation: **0.0% white saturation on all 18 tiles** (raw: 84.0% / 23.1% /
80.9% ... per tile, consistent with prior measurements). Top-3-by-weight
per-cell capture vs upper bound: region A 0.934–0.999, region B 0.770–0.940
(measured expectations 0.934–0.999 / 0.770–0.951) — consistent.

## Honest bounds

1. The quadtree leaf fields' (+0x1c..+0x44) provenance from the TDF 16x16
   masks is not traced (the quadtree construction is the remaining RE link).
2. The exact world-space anchoring of the palette's 256-row dimension is
   plausible but not byte-pinned (x87 stack ambiguity); the palette indexing
   itself (row stride 0x40, texel offsets) is disasm-proven.
3. The sources of bake-flag bits 2/3 (noise modulation, constant-RGB
   fallback `RGB(50,70,85) x noise`) are unresolved; FUN_0093f1d0 sets only
   bits 0/1.
4. The 65x65 climate grid's file source is untraced (TerrainClimates
   candidate).
5. The edge-marker channel-switch rule is decompiled but not reduced to
   closed form.

## Evidence

Session: `99_Audits/PE_MILESTONE_1_WORLD_SURFACE_R1/04_Sessions/ITER041_FACTOR_RUN/`
(logs: dec_*.c decompiles, iter027*.json, ghidra_a.log). Consolidated:
`03_EVIDENCE/iter027_findings.json`, `iter027_texture_ids.json`,
`iter027_worked_example.json`, `iter027_manifest.json` (148 entries, SHA256).
Binary: Entropia.exe 9.3.5 sandbox copy, SHA256
`E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31`.
