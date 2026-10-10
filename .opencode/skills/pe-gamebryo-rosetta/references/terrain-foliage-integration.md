# Terrain / materials / foliage integration index — PE_WORLD_LAUNCHER_R1 (2026-10)

Status: MEASURED in PE_WORLD_LAUNCHER_R1_20261010 Etap B (mechanism research +
module API verification; the launcher itself is the NEXT phase). Every claim
carries source+scope; SDK knowledge is NEVER PE knowledge; no "engine 100%
known". SDK sources/docs/binaries are read-only and never copied into the repo.
Run package: docs/audits/PE_WORLD_LAUNCHER_R1_20261010/ (GAMEBRYO_MECHANISM_MAP.md
= the five mechanisms; IMPLEMENTATION_MAP.md = the reuse/miss map).

## 1. Verified source locations (Etap B, own SHA256 measurements)

- Gb12 (Gamebryo 1.x, GAMEBRYO_MAJOR_VERSION=1 in CoreLibs\NiSystem\NiVersion.h):
  `D:\gamebyroengine\extracted\Gb12_Source\CoreLibs\NiMain\`
  - NiStream.cpp (38,458 B, e955c36e…): LoadHeader/LoadRTTI/RTTIError/LoadStream
    (the stock registry chain; "cannot find create function." text lives at
    RTTIError L387-400).
  - Win32\NiAVObject_Win32.cpp (999 B, 75e45268…) + Win32\NiTransform.inl
    (1,067 B, 92e8acf6…): world = parentWorld × local; point → (R·p)·s + t.
  - NiAVObject.inl (10,672 B, 09e1a5a5…): setters write m_kLocal ONLY (lazy
    world recompute). NiNode.cpp (33,897 B, 38c7a1de…): AttachChild =
    no local compensation.
  - NiTexturingProperty.cpp (32,194 B, 2bc36c08…) / NiSourceTexture.cpp
    (14,704 B, b5d0bb02…) / NiGeometry.cpp (14,679 B, fde29a81…): the stock
    texture chain (Map = texture + clamp + filter + TEXCOORD INDEX; UV sets live
    on NiGeometryData; SetModelData = shared smart-pointer mesh; CopyMembers
    SHARES geometry across clones).
- Samples (other apps' examples — NEVER PE format proof): BackgroundLoad.cpp
  (5,746 B, 8287a6ae…) + CallbackStream.cpp (3,740 B, 6c4a2998…): async load
  with read%/link% progress + renderer prep in the loading thread; MOUT
  TerrainManager.cpp (7,148 B, cdad77ba…) + WorldManager.cpp (27,057 B,
  e9eb4f45…): whole-world NIF + NiPick ground raycast, NO tile streaming.
- Gb26 (Emergent 2.6 — later-generation comparison ONLY):
  NiExternalAssetNIFHandler.cpp (12,796 B, 38e13c8a…): pristine-root vs clone-set
  separation, refcount-based unused-asset unload.
- Docs: Gb112_docs_html (Gamebryo 1.1 help) — NiTexturingProperty_Map.htm
  (8,749 B, e1ae44e2…) consulted for Map semantics.

## 2. Reuse-first module map (real APIs verified this run; see IMPLEMENTATION_MAP.md)

- `src/pesource/PESourceMount.js`: getTerrainTile / getTerrainMaterials /
  resolveTexture / getVegetationClimate / getModelResource (era-disciplined,
  fail-closed). io = { readFile, inflate, sha256? } — BrowserSourceAdapter /
  NodeSourceAdapter DO NOT EXIST (comment-only); 10-line adapters are the
  established pattern (terrain/p0.js browser; tools/iter020_material_audit.js
  Node). getSentinelInfo is 50.bnt-bound (JUL) — PCG sentinel handling is an
  explicit launcher decision.
- `src/pesource/TdfMaterialTailDecoder.js` (ACTIVE): record = [u32 size][u32
  dim][body], stride size+4; named mask @ record+56; 52..55 = extra4 (NOT mask);
  RAW or RLE, exact consumption; sums>255 = ORIGINAL DATA. The
  TdfDecoder.TDF_MATERIAL_RECORD_LAYOUT.MASK16 (record+52) constant is STALE —
  never take mask offsets from it.
- `src/peworld/PETerrainCore.js`: PETerrainRegion LIVES HERE (NxN tile block,
  disjoint 32×32 tiles, seam differences = ORIGINAL_DATA, no repair);
  buildGeometry = positions+indices only (no UV/normals). PE_TERRAIN_METER_PER_
  SAMPLE=2, HEIGHT_SCALE_CALIBRATION u16/128.
- `src/peworld/PEFoliageCore.js`: generateInstances (byte-locked f64
  constants + f32 rounding points; placement 1:1 NOT claimed). NO LAB_SEED
  input exists — a documented wrapper must inject LAB_SEED into the
  [P-CELLSTREAM] stand-in, never into the locked RNG arithmetic.
- `src/pesource/TgaDecoder.js`: decodeTga2 (24bpp terrain texture subset),
  decodeTga2A32 (file-row, climate palettes), decodeTga2A32Image (image-order,
  model textures). `VegetationClimateDecoder`: strict TSV→12-value records;
  25.vcl = UNSUPPORTED_BY_CURRENT_DECODER (comma tokens — controlled, never
  comma-converted).

## 3. Executed controls (prior runs; era-labeled)

- TDF calibration facts are CURRENT_RUNTIME_CALIBRATION — u16/128 heightScale,
  2 spatial units/sample, identity min/max lerp (per-tile min/max source
  UNRESOLVED — sub-header reads zero on samples). NEVER historical meters/axes.
- Composition law verified vs NATIVE stock-printer controls (218757 lineage);
  stock GB 1.2.2 rejects NIF-10.1 NiArk content (RTTIError registry gap — the
  exact text is in NiStream.cpp); 4,838/4,838 PCG NIF-10.1 entries declare
  NiArk* → stock-only readers corpus-proven unusable.
- TGA subsets qualified (iter011/027/030); material tail corpus-proven (JUL
  51,920/51,920; PCG 448,384 records/0 failures, mask@56 convention).
- Launcher-phase controls are PLANNED (Etap C/D/E per contract §8) and were
  NOT executed in Etap B — no launcher code exists yet.

## 4. Explicit UNKNOWNs (do not silently resolve)

- [P-CELLSTREAM] historical per-cell record stream source: NOT closed (the
  record FORMAT {u16,u16,u32} + spawn arithmetic are the confirmed parts;
  instance distribution = reconstruction-only).
- [P-CLIMATE] climate→region mapping: PLAUSIBLE-UNVERIFIED (shared-selector
  hypothesis); the caller passes an explicit index; a chosen default profile is
  NEVER a "historical biome of the place".
- [P-RNG-P3] seed input p3 = *(impl+0x24): UNVERIFIED → 0; show separately from
  LAB_SEED; LAB_SEED ≠ the original p3.
- materialId == textureId: NOT established (terrain texture binding needs a
  provenance-backed mapping table or an explicit unresolved-binding diagnostic;
  name agreement alone is a candidate, never proof).
- PCG terrain special rows (y=0xff5a..0xffff, 6,530 entries): semantics
  UNRESOLVED — excluded loudly from regular addressing.
- PE terrain streaming design: NOT established (MOUT/BackgroundLoad are other
  apps' examples); the ≤64-tile streaming plan is an ADAPTER design.
- VCL columns 6..11: UNVERIFIED (carried raw); per-column int/float types
  UNVERIFIED.

## 5. Commands

- Existing: npm run serve:sceneir (8140), serve:catalog (8161), test:pecompat*.
- PLANNED (Etap C): npm run serve:world — bounded loopback server on port 8162
  (server-side PESourceMount; /launcher + /world routes; explicit PID/READY/stop;
  no whole-container browser downloads), + launcher and world apps. It does NOT
  exist yet as of Etap B.

## 6. Era discipline (binding for launcher work)

- World profile era: PCG_9_3_5 (terrain.bnt / Textures.bnt / Models.bnt /
  VegetationClimates.bnt, all SHA-pinned in PEProvenance.KNOWN_HASHES).
  CD_2003 (label CD_JAN_2003 in pesource) = catalog/comparison ONLY; JUL_2003
  = historical reference pipeline; EU_LATER = RE evidence only. No silent
  cross-era substitution; asset identity = era + container SHA + entry name +
  payload SHA; same entry name in two eras = TWO DISTINCT assets.
- Historical 2003-era terrain rules in the pe-reconstruction skill (50.bnt
  BUNT, r169 runtime) are THAT pipeline's reference — not defaults for
  PCG_9_3_5 launcher terrain.
