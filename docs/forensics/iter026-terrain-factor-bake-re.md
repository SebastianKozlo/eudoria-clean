# ITER-026 (Gate B / iter040): The Bake - TDF-Mask -> Factor-Texture Reduction + Normalization RE (Entropia.exe 9.3.5)

Era: PCG_9_3_5. Static Ghidra RE (fresh project ITER040_BAKE, sandbox copy SHA E7785430...
verified before import) + data-side worked example on original terrain.bnt/50.bnt bytes
(read-only). Evidence: `99_Audits/PE_MILESTONE_1_WORLD_SURFACE_R1/03_EVIDENCE/iter026_*`
(audit tree, outside this repo; 28 files, SHA256 manifest included).

## Headline

The FACTOR-TEXTURE CONSUMER chain of the 9.3.5 terrain material pipeline is now
CONFIRMED end-to-end at decompilation level: the engine loads technique
**Terrain_14 (0x3ea) as the PRIMARY terrain shader** (mode flag 2), keeps **Ark11 (0x3ed)
as a 2-texture FALLBACK** (mode 1, no factor texture at all), and binds **exactly the 5
sampler slots of Terrain_14** (base, factor, 3 details) per material object. The exact
arithmetic that bakes TDF masks into the factor texture was NOT located in the bounded
pass (honest bound; precise resume point recorded). A worked example on real tile data
falsifies BOTH the raw and the clamp255 factor-content candidates, leaving **per-cell
renormalization** as the only surviving normalization candidate of the three tested.

## Key findings (address-anchored)

### 1. The iter024 RTTI negative was INVALID

The iter024 RTTI scan used file offsets as VAs; its "0 COL refs" negative is falsified.
With correct VAs the MSVC RTTI chain resolves for 14 terrain classes, e.g.:

- `MaTerrainMapPatch` vtable 0xa97c2c, ctor FUN_00934d00 (0x2c-byte object with a typed
  slist of refcounted sub-objects), dtor FUN_00934d40, factory create FUN_009343e0.
- `MaTerrainMapManagerClient` vtable 0xa97d3c, ctor FUN_00942a20 (writes the 0x7fff7fff
  sentinel at +0x60 = current patch coords; the patch-streaming anchor).
- `NiTexturingProperty` vtable 0xa8d084; vt[9] = FUN_007b9b50 = the "MultiTexture X Map"
  debug serializer (slots 0=Base 1=Dark 2=Detail 3=Gloss 4=Glow 5=Bump 6+=Decal +
  Shader Maps carrying m_uiID; per-map +4 texture / +8 clamp / +0xC filter / +0x10
  texcoord / +0x18 transform).

### 2. The terrain shader selector (FUN_009518e0; sole caller = renderer init FUN_0094e890)

```
Water(0x3eb)      -> renderer+0x1b8
Terrain_14(0x3ea) -> renderer+0x1b4          ; mode +0x1bc = 2
on 0x3ea failure: Ark11(0x3ed) -> +0x1b4     ; mode +0x1bc = (ok != 0) = 1
getters: FUN_00951260 (shader), FUN_00951270 (mode)
```

Record 0x3ed was extracted this session: a generic 2-texture `base * detail * 2`
ps.1.1 modulate - structurally incapable of the factor model. Terrain_14 is thus
CONFIRMED as the loaded primary terrain technique (not just an extracted file).

### 3. The 5-slot factor consumer (FUN_00950bf0, called per material by the RB-tree driver FUN_0093f800)

When mode == 2 (Terrain_14):

- slot 0 = base texture from material[1] (refcounted get FUN_00950b80)
- slot 1 = FACTOR texture from material[2]
- slots 2/3/4 = the 3 detail textures from material[3..5], each bound as a
  `NiTexturingProperty::ShaderMap`
- then the terrain shader (Terrain_14 or Ark11) is attached at mesh+0xe4.

When mode != 2 (Ark11): only 2 x 0x1C descriptors (base + detail) - NO factor.

**The binding order 0,1,2,3,4 matches Terrain_14.hlsl `Sampler[0..4]` one-to-one.**

Material object layout: `{vptr, [1] base map, [2] FACTOR map, [3..5] detail maps}`
with map+0x10 = the refcounted texture; assembled via the 0x1C descriptor family
(ctor FUN_007b88d0, slot setters FUN_006b23c0/FUN_00444a80). Per-frame entry:
FUN_0044cda0 (camera -> FUN_0093f800).

### 4. TDF material data objects are TYPED (FUN_009347e0 getter)

- type 0 = u16 heights (12 call sites; +4 data, +0x18 dim)
- **type 2 = fine-grain material masks, DEFAULT DIM 0x100 = 256** (creator
  FUN_009376f0(0x100, count, 2, ...); consumers FUN_00943000/FUN_009429c0; per-point
  mask evaluation FUN_00942cf0) - the exe-side anchor for the data-side dim=256 TDF
  records; leading candidate as the factor CONTENT source at 256x256 resolution
- type 6 -> FUN_00953340 -> 0x100x0x100 plane geometry (water-plane candidate)
- type 7 = second u16 grid in the tile-load path; type 0xa -> FUN_009367f0

### 5. Tile streaming pipeline (CONFIRMED)

FUN_00942c50 (client update) -> FUN_00946ae0 (queue consumer) -> FUN_009458f0 (tile
load + LOD tessellation) -> FUN_00944b10 (NiNode world-position); queues via
FUN_009460a0/FUN_00941ea0; LOD ring builder FUN_00941f90 assigns tessellation
densities **256 / 128 / 64 / 32** by distance (4 closest tiles at 0x100); tesselator
init FUN_00944bf0 pre-creates per-tile slots with the 0x7fff7fff coords sentinel,
NiTriShape + NiVertexColorProperty + an Ark11 default attach.

### 6. VFS persistence negative CLOSED

The VFS subsystem has NO record-append writer (FUN_00972ad0 called only by
FUN_00972df0; FUN_00971680 only from open/close; FUN_00971d20 only from
FUN_00828770; KERNEL32 imports are by-ordinal with zero direct refs). Combined
with iter025's byte census (TerrainImageCache1/2.vfs are 16-byte headers in every
extant install): **the factor bake is PER-SESSION IN-MEMORY; no persistence path
exists in the observable code.**

### 7. Worked example on REAL tile data (m1_iter026_worked_example.py)

Under the CONFIRMED overlay op (iter024) with documented synthetic detail/base texels:

| Tile | top-3 by total weight (C1) | cells sum>255 | raw | per-cell renorm | clamp255 |
|---|---|---|---|---|---|
| 00380070.tdf (region A, 7 named) | Grass01 65280 / Rock03 65280 / Grass27 52751 | 256/256 | 84.0% white-sat | 0.0% | 84.0% |
| 00650064.tdf (region B, 9 named) | Grass06 / Grassmix04 / Grassmix14 | 206/256 | 2.7% | 0.0% | 2.7% |

clamp255 is ALWAYS identical to raw for u8 masks (no single mask can exceed 255),
so it is falsified by the same measurement. RAW and CLAMP255 are rejected as the
engine factor-content; **per-cell renormalization is the only surviving candidate of
the three tested** (the exact engine formula remains UNVERIFIED; the raw/renorm
candidates already exist side-by-side in the clean runtime's materials_wsum page
from iter025, correctly labeled as candidates).

## Honest bound / resume point

The exact factor-byte arithmetic (selection + normalization code) was NOT located.
The bounded remaining lead: the material-object creator that inserts 5-slot objects
into FUN_0093f800's RB-trees, and the type-2 256-dim fine masks as the factor
content source (converging hints: LOD densities 0x100 + the 0x100 type-2 default
dim). Next vectors (separate authorization per bounded-iteration rules): the RB-tree
INSERT callers walk; the 256x256 factor-resolution hypothesis test; x32dbg
breakpoint on FUN_00950bf0's material[2] texture on a live client; a ProcMon
file-size watch on TerrainImageCache during a live run.
