# ITER-024 (Gate B / iter038): Terrain Material Blend-Op Consumer RE — Entropia.exe 9.3.5

Era: PCG_9_3_5. Static Ghidra RE (fresh project, sandbox copy SHA E7785430... verified) + original
data-file forensics. Evidence: `99_Audits/PE_MILESTONE_1_WORLD_SURFACE_R1/03_EVIDENCE/iter024_*`
(audit tree, outside this repo).

## Headline

The 9.3.5 terrain material blend is a **ps.1.4 pixel shader** (technique `Terrain_14`) stored as
HLSL source in `Data\Parameters\materials.vfs` (ArkVFS02 container, original install file,
record id 0x3ea). It is a **weighted-sum splat of up to 3 DETAIL textures by the RGB channels
of a FACTOR texture, overlay-blended onto a 4th (BASE) texture** — NOT a sequential alpha
overlay. The clean runtime's "sequential overlay mix" calibration is falsified as the
real-engine op.

## The blend op (verbatim semantics)

```
texld r1, t1   // FACTOR texture: material weights in RGB (TDF u8 masks /255, unrenormalized)
texld r2..r4   // detail textures d0,d1,d2
mul  r2, r2, r1.r          // d0*w0
mad  r2, r3, r1.g, r2      // + d1*w1
mad  r1, r4, r1.b, r2      // D = d0*w0 + d1*w1 + d2*w2
phase
texld r0, t0               // BASE texture
mul_x2_sat r3.rgb, r0, r1            // 2*base*D
mul_x2_sat r2.rgb, 1-r0, 1-r1        // 2*(1-base)*(1-D)
cnd  r4.rgb, r1, 1-r2, r3            // overlay keyed on D: D>=0.5 -> 1-2(1-b)(1-D), else 2bD
// then (Material + L1*LIGHT_ADD_X_2) * (L0 + L1), * shadow, fog lerp
```

Vertex stage: height light factor `clamp((z/100 - (-5)) / (10 - (-5)), 0, 1)`; detail UV
repeats 32.0 / 32.0 / 16.0.

## Layer cap

3 weighted detail layers + 1 base = **4 material textures per cell per ps.1.4 pass** (factor
texture is the 5th sampler). This source-anchors the legacy 4-materials-per-pixel structural
cap (iter020). How TDF tiles with >4 named records are reduced (top-4 pre-bake vs multipass)
remains UNRESOLVED.

## Texture-stage / filtering states (era 9.3.5, CONFIRMED)

- base + factor: AddressUVW=CLAMP, MIN=LINEAR, MAG=LINEAR, MIP=POINT
- details: WRAP, MIN=LINEAR, MAG=LINEAR, MIP=LINEAR, MipMapLodBias=-0.5
- pass: AlphaBlend=false, AlphaTest=false, ZWrite=true, ZEnable=true, CullMode=2, FogEnable=false

## Era divergence vs PE2 (2003 oracle)

9.3.5 is **D3D9 + programmable shaders** (D3DX9_30.DLL imports: D3DXCompileShader,
D3DXCreateEffect; NiDX9Renderer strings; zero d3d8). PE2's fixed-function STSS facts
(FUN_004c3670 clamp, FUN_004297e0 UV sets, state cache) are era-invalid for 9.3.5: replaced by
sampler_state blocks and vertex-shader texcoord writes. PE2 FUN_0047fb20 height form has a
sibling at FUN_00989e70 (u16-grid scale clamp-to-65535); the full lerp form is UNRESOLVED.

## Exe-side chain (decompiled, R2 split)

- FUN_0041dae0 — VFS/data mount init (terrain.bnt, textures.bnt, TerrainImageCache1/2.vfs,
  .tdf extension table)
- FUN_006ec760 — ArkFXCompiler reading `Parameters\Materials.vfs` + 0x30-stride
  (material name, shader) binding table
- FUN_00935200 — "MaTerrainMapPatch" name-based factory registration (x3)

## Documented negatives

Material-name strings (Water01-05/Stone04/Grassmix04) = 0 hits in the whole exe (names live in
data files, not the binary). RTTI COL→vtable chain = 0 pointer refs (name-based factories).
Immediate 0x834 (2100) sites = stack offsets only. inv255 float constant = 0 hits. The exe
function baking TDF tail masks into the factor texture was NOT located (leading residual:
TerrainImageCache writer path, next iteration).

## Worked example

factor (255,128,64) → w=(1.0,0.502,0.251); d0=(0.20,0.25,0.15), d1=(0.60,0.55,0.40),
d2=(0.80,0.75,0.60); base=(0.50,0.45,0.35) → D=(0.702,0.714,0.501) → overlay
O=(0.702,0.686,0.352) → lit (L1=0.1, L0=1.0, shadow=1, fog=0) → final (0.992,0.974,0.607).
Full numbers: `iter024_blend_op_findings.json`.

## Opportunistic leads (recorded)

WaterPlane01 consumer FUN_0093be20; ARK_WATER_WIND binder FUN_009512a0; Geowater consumer
FUN_006e8f70; Water.fx (materials.vfs record 0x3eb) and Vegetation.fx (0x3ec) extracted;
TerrainImageCache1/2.vfs are runtime-generated caches (absent from fresh install).
