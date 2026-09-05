# ITER-32 — Gate C: The Foliage Source Graph (loader + instance derivation)

- **Session**: M1 ITER_046 (ledger ITER_032), 2026-09-04
- **Binary**: `Entropia.exe 9.3.5.6746`, sandbox copy, SHA256 `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` (verified before import; fresh Ghidra project `ITER046_GATEC`, never TMF1_12H)
- **Evidence**: `99_Audits/PE_MILESTONE_1_WORLD_SURFACE_R1/03_EVIDENCE/iter032_*` (25 files, SHA-pinned in `iter032_manifest.json`)
- **Scope**: static RE + data cross-checks only. No foliage render wiring, no full-map, no runtime tracing, no network.

## P0 verdict: the loader EXISTS — CONFIRMED (positive chain)

The 9.3.5 client ships and mounts a **complete local foliage system**:

| Element | Address | Evidence |
|---|---|---|
| `.vcl` extension string | `0x00a7a724` | PUSH-imm ref from `FUN_0041dae0` @ `0x0041f668` |
| `VegetationClimates.bnt` container string | `0x00a7a7a8` | PUSH-imm ref from `FUN_0041dae0` @ `0x0041f09a` |
| `VegetationClimates\` directory string | `0x00a7a880` | PUSH-imm ref from `FUN_0041dae0` @ `0x0041ea04` |
| `ArkVegetationClimateFactory` ctor `FUN_0083a630` | called from inside `FUN_0041dae0` @ `0x00420007` | the factory is *part of the resource registry* |
| `ArkVegetationClient` ctor `FUN_0094ac50` (44 B) | created at init `FUN_0044cb70`, called from `FUN_0044d590` | the same init that calls `FUN_0044d360` (the terrain palette manager) |
| The class family | 45 `ArkVegetation*` classes | MSVC RTTI chain (type descriptors → COLs → vftables → methods), file-side deterministic (`iter032_rtti_chain.json`) |

The 2003 PE2 binary has **no** vegetation strings (iter017 negative) — the loader is later-generation; for the 9.3.5 era it is **fully local**. (The `plant` substring hits were honestly rejected: they are `ArkImplantToolUI` — implant-tool UI, not flora.)

## The source graph (9 stages, address-cited)

1. **Registration** (`FUN_0041dae0`, sole caller `FUN_004172a0`): extensions via `FUN_008286e0` (`.nif .dat .jpg .tga .wav .mp3 .amu .tdf .bvi .prt .vcl .tez .esq .bik .str`), directories via `FUN_00827960`, containers incl. `VegetationClimates.bnt`, and the **ArkVegetationClimateFactory** (boost `sp_counted_impl` vtable `0x00a7a4f0`).
2. **Climate data**: factory create `FUN_0083aa40` (vtable `0x00a91a94`) builds a 0x1C `ArkVegetationClimate` (ctor `FUN_0083acb0`) **from the .vcl payload text** via a stringstream (`FUN_004072d0`) and **`FUN_0083a7d0` = the TSV parser**: a stream loop reading **12 values per record**, appending **0x30 (48-byte)** records to the climate's row vector. The 12 columns match the VCL census exactly (`iter032_vcl_columns.json`): **492 engine records** (491 line-records + 1 continuation from the 9.vcl multi-model line).
3. **Client**: `ArkVegetationClient` (ctor `FUN_0094ac50`) creates the MapManager (`FUN_0098bee0`) + Visualizer (`FUN_00943b90`); defaults measured (1.0f, 300.0, 100.0, 0.1, 500.0, 0.01, 128.0, 0x1e, 0x19, 0x1400000, 10000); registered via `FUN_0094adf0`.
4. **Record query**: `FUN_0098cf90` → `FUN_0098f3a0` (position pair `*(obj+8)` split `>>16` / `&0xFFFF`) → **`FUN_0098fe00` the procedural grid**: subdivision switch on settings+4 (0/1/2/3/4 → step **1/2/4/8/16**, getter `FUN_0098ead0`), RNG-scaled extents, a **24-byte-per-cell** array, `density = *(cell+8) >> 3` → **`FUN_00990810` the cell-record parser**: **8-byte triples `{u16 x, u16 y, u32 model_id}`** from a compact per-cell byte stream.
5. **Instance spawn** (`FUN_0095b180`, the loop): per record with density>0, per instance `{u16 A, u16 B, u32 id}`: **NiNode** (ctor `FUN_007b6000`, 0x118 B), `node[0x17] = A / K` (**position X**), `node[0x18] = B / K` (**position Y**), `node[0x19] = id` (**model binding**), `node[0x1a] = |rand × 2.0|` (**scale**, `_DAT_00a980d0 = 2.0f`), registered via vtable[41].
6. **The RNG** (fully recovered): seed hash `FUN_0098cdf0`: `x = ((p4*16 + p5)*16 + p1+p2+p3) * 0x5CC7 + 0x6D7; state = x*8 ^ x`, with p4/p5 = the two 16-bit position components; next value `FUN_0098ce30`: `state = state * 0x343FD + 0x269EC3; rand01 = ((state>>16) & 0x7FFF) / divisor` — **the classic MSVC rand() LCG** (214013 / 2531011). Sampler `FUN_0095ac30` lerps `[min,max]` = `impl+0x44`/`impl+0x40`. **The same u16 position values are both the position and the seed inputs → position-keyed determinism.**
7. **Model resolution**: `ArkVegetationClient::GetModel` (`FUN_0094b1d0`, vtable `0x00a97de0[1]`, assert strings at `0x00a97df4`/`0x00a97e14`): gated on client+0x24, fetches a **type-0x66** resource by id via `FUN_006c9700` (key built by `FUN_00415670`, provider walk `FUN_00823c10`), wraps in a 0x14 `ArkVegetationModelClient` (`FUN_00958bb0`). The id space = VCL col0 (10136..546547; 255/256 resolve as `<id>.nif|.dat` in Models.bnt, iter017b).
8. **Explicit patch path** (`FUN_0098caf0`): builds 0x28 `ArkVegetationExplicitPatchComponent`s per layer item, **sorts into three view bands 10 / 20 / 30** (layer field +0x2C), attaches the 0x10 Spawner `{settings, embedded RNG}` (`FUN_0098eb20`).
9. **Render technique**: `FUN_006ae840` maps the name **"Vegetation" → 0x3EC (1004) = the FX technique id** — materials.vfs record **0x3EC exists in both eras** (`#include 1Ark.fx/25ArkLight.fx/10NiTexture.fx`, vertex-shaded; sibling 0x3EB = Water, iter031). The 13 `PUSH 0x3EC` sites are technique bind sites. This is *not* a resource type id (corrected in-session from the initial hypothesis).

## Data cross-checks (independent of RE)

- **VCL census** (`iter032_vcl_columns.json`, `VegetationClimates.bnt` SHA `7B858401...`, byte-identical in all 3 corpus copies): col0 model ids 256 distinct; col1 "density" 0..330 (82 distinct, median 0.6); col2/col3 = scale 0.2..4 / 0.5..6 (corr 0.449); col4/col5 = elevation bands 0..1000 (corr 0.296); col7 correlates with max-elevation (0.382); col10/col11 = a probability pair (corr 0.370); cols 6–11 semantics remain UNVERIFIED. **Adjacent climate indices share model sets**: top Jaccard pairs 0↔9 (0.583), 16↔17 (0.500), 30↔31 (0.500), 23↔24 (0.375). Per-file density sums 2.7 (5.vcl) … 84.9 (11.vcl).
- **.tez zoning** (`iter032_tez_zoning_v3.json`): the 171 .tez zone **local terrain edits, not climates**: rect widths q50 56 u (max 800), heights q50 52 (max 832), z field = a target height (−35.5…645.1 m), alignment near-random vs both the 1024-unit climate cells (5.5% zero-frac) and the 128-unit tiles (10.7%), coverage = only 174 unique 1024-cells, quadrant census SW 868 / NW 93 / SE 52 / NE 2; the d>0 (20xxx) family = larger rects (q50 180) clustered in the west (x −29556…−9416), 233 records era-stable. iter036's "no climate carrier" confirmed with geometry.
- **Climate id spaces** (`iter032_climate_id_space.json`): the VCL resource ids (0..31) and the terrain palette ids (`0x66dc6..0x85527` = 420,806..546,471, table A, iter028) are **disjoint value spaces** (0 overlaps; the 256 VCL model ids are also disjoint). The terrain palettes release under the name **"TerrainClimates"** (`FUN_0093bbd0`, the 256-slot `mgr+0x440` cache of the same 0x38A8 palette manager) — **two separate climate resource families, one shared init** (`FUN_0044d590` calls both the palette manager init and the vegetation client init). The shared-selector hypothesis (climate byte *c* → table A[*c*] AND `.vcl` *c*) is **PLAUSIBLE but NOT CONFIRMED** — the .vcl fetch id source is not closed (bound below).

## Honest bounds

1. The `.vcl` resource **type-id constant** and the fetch id source (is the id = the climate byte?) — UNVERIFIED; the provider chain (factory created inside the registry) is proven.
2. The runtime-initialized divisors `_DAT_00a7d7a8` (RNG normalizer) and `_DAT_00a8c758` (position scale) read **0.0 from the file** — referenced only as FDIV/FLOAD operands; no static writer found; runtime values not statically recoverable.
3. The **cell byte-stream origin** (the Layer/patch provider: local file vs server content) — the DataSource/PatchSourceClient abstraction proven, the buffer source not closed.
4. cols 6–11 semantics UNVERIFIED; the per-column parser types (`FUN_0083a5b0`) not decompiled.
5. **Rotation/variant derivation NOT FOUND** in the spawn loop (position + scale + model id only); candidates: `FUN_0095ae20`/`FUN_0095b4f0` (the other RNG sampler users, not read this session) — UNVERIFIED.

## Impact

`FOLIAGE_SOURCE`, `FOLIAGE_DISTRIBUTION`, `FOLIAGE_SEED/RNG` = **CONFIRMED** (local, deterministic, position-keyed); `FOLIAGE_MODEL_BINDING` = CONFIRMED (type-0x66 fetch, VCL col0 ids); `FOLIAGE_BIOME_RULES` = ADVANCED (12-column rules measured; climate selection input bounded). `PESourceMount.getVegetationClimate()` now has a proven backend for era 9.3.5. The seed-20030130 scatter remains `VISUAL_RECONSTRUCTION_LEGACY` until the climate-selection input closes and the clean wiring iteration executes.

**Next**: (1) the .vcl fetch id source (the Gate B–C convergence closer); (2) the cell byte-stream provider; (3) `FUN_0095ae20`/`FUN_0095b4f0` (rotation/variant); (4) the clean-runtime foliage wiring (a later iteration).
