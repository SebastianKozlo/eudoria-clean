# IMPLEMENTATION_MAP — PE_WORLD_LAUNCHER_R1_20261010 (DRAFT)

RUN_ID = PE_WORLD_LAUNCHER_R1_20261010
PHASE = ETAP_B_MECHANISM_RESEARCH — this map is the DRAFT architecture prepared from
mechanism research + verified module APIs. **NO launcher implementation was started in
this phase** (contract §3 hard constraint: research in service of implementation).
Status of every API below = VERIFIED BY READING THE REAL MODULES (this phase), not by
comments or memory. File names marked NEW are PLANS; they may change at implementation.

## 1. Verified module APIs to REUSE (no parallel code)

### 1.1 src/pesource/PESourceMount.js (22,225 B, measured this phase)

- `new PESourceMount(io)` — io = `{ readFile(path)→Promise<Uint8Array>, inflate(bytes)→Promise<Uint8Array>, sha256?(bytes)→Promise<string> }`. **BrowserSourceAdapter/NodeSourceAdapter DO NOT EXIST** (grep-verified: only a header comment mentions them); the io adapters are 10-line objects (see §3).
- `mountEra({ era, container, path, expectedSha256?, verifyHash?, format })` — format ∈ BUNT|BNT2|ARKVFS|BNT2_TERRAIN; hash-pin fail-closed; era part of identity.
- `enumerate({era, container})`, `openResource({era, container, entryName})`.
- `getTerrainTile({era, gridX, gridY})` — FILENAME-XY addressing 0..219/0..235; sentinel name rejected LOUDLY; PCG_9_3_5→Bnt2TerrainArchive, JUL_2003→BuntArchive; returns canonical `TerrainTile` (provenance + explicit offset-space notes).
- `getTerrainMaterials({era, gridX, gridY})` → `{tile, materials[{position,id,name,dim,bps,unk,res,maskEncoding,mask(16×16),recordOffset,size}], systemRecords, sums, provenance}` — the contract §5 entry point ("Use PESourceMount.getTerrainMaterials() and the active TdfMaterialTailDecoder").
- `resolveTexture({era, container, textureId})` → `{payload, entry, provenance}` — LOUD NOT_FOUND, era-disciplined.
- `getVegetationClimate({era, climateIndex 0..31})` → `{climateIndex, records(12-value), recordCount, text, provenance}`.
- `getModelResource({era, modelId})` → `{payload, entry, provenance}` — `'<modelId>.nif'` in PCG Models.bnt.
- `getWaterResource()` — throws NOT_RECOVERED (explicit stub; Gate D pending).
- `get heightScaleCalibration` — HEIGHT_SCALE_CALIBRATION.
- **Finding (launcher-relevant)**: `getSentinelInfo` hardcodes container `Terrain/50.bnt` (JUL_2003 path) — it does NOT serve the PCG sentinel. Per contract §4, the launcher must NOT assume the sentinel helper handles PCG; PCG sentinel/special-row handling = an explicit launcher-side decision in Etap C (Bnt2TerrainArchive has 58,451 entries incl. 7ffe7ffe.tdf + 6,530 special rows y=0xff1a..0xffff, semantics UNRESOLVED, excluded from regular addressing).

### 1.2 Format layer (all verified this phase)

- `Bnt2TerrainArchive(bytes, io)` — PCG terrain.bnt (BNT2 footer; variable 0x0A-terminated dir; `readEntry` ASYNC inflate, strict size check). `entries()/entryByName()`.
- `Bnt2Archive(bytes)` — `entries()/entryByName()/entryById(id)/readEntry()` (SYNC readEntry — payloads RAW in PCG containers).
- `ArkArchive`, `BuntArchive` (JUL path) — same interface family.
- `TdfDecoder` — `decodeTdfPayload` (payload layout: HEADER 0..52, SUBHEADER 52..64 (NOT heights), HEIGHTS 64..2112 = 32×32 u16 LE, TAIL 2112..; standard tile data_size=2100, dim=32), `gridFromName`, `isSentinelName`. **WARNING (measured): `TDF_MATERIAL_RECORD_LAYOUT.MASK16` (record+52) is a STALE layout constant — contradicts the ACTIVE decoder below. The launcher must NEVER take mask offsets from it.**
- `TdfMaterialTailDecoder` (ACTIVE, contract-pinned convention) — record = [u32 size][u32 dim][body]; stride = size+4; id@16, res@20, name@24..51 (28 B NUL-terminated), **extra4@52..55 (NOT mask), mask@56..size+3**; RAW or RLE (count,value) with EXACT consumption; `decodeMaterialTail(tail)`, `decodeMaskRegion`, `maskSumStats`. Corpus-proven (JUL 51,920/51,920; PCG 448,384 records/0 failures).
- `TerrainTile` — raw u16 Uint16Array(1024), `heightAt(x,y)` (no interpolation), provenance required; `HEIGHT_SCALE_CALIBRATION = { u16PerMeter: 128, label: CURRENT_RUNTIME_CALIBRATION }`.
- `TgaDecoder` — `decodeTga2` (24bpp BGR TGA2 TRUEVISION-XFILE subset, bottom-up, 196,652 B constant; the terrain material texture subset); `decodeTga2A32` (32bpp, FILE-ROW order — climate palettes); `decodeTga2A32Image` (32bpp IMAGE order — model textures, v=0=top convention). All strict, loud failures.
- `VegetationClimateDecoder` — `decodeVclPayload` (TSV → 12-value records, whitespace-stream semantics per FUN_0083a7d0); **25.vcl = UNSUPPORTED_BY_CURRENT_DECODER** (comma tokens at record 9 col 1 — controlled UNSUPPORTED, NEVER comma-converted).
- `PEProvenance` — ERAS {CD_JAN_2003, JUL_2003, PCG_9_3_5, EU_LATER}, KNOWN_HASHES (incl. the run's pinned containers), makeProvenance.

### 1.3 src/peworld

- `PETerrainCore.js` — **PETerrainRegion LIVES HERE** (contract §4's "PETerrainRegion" = `export class PETerrainRegion` inside PETerrainCore.js — VERIFIED, answering the contract question). API: `new PETerrainRegion(tiles[rows][cols])` (validates NxN block + grid contiguity), `rawSample(vx,vy)`, `buildGeometry()` → `{positions Float32Array, indices Uint32Array, sampleGridX, sampleGridY}` (+X grid-x meters, +Y height meters, +Z grid-y south; 2 m/sample = CURRENT_RUNTIME_CALIBRATION), `provenanceList()`, `tileSeamDiagnostic` (seam differences = ORIGINAL_DATA, NO repair). **Launcher note: buildGeometry emits positions+indices ONLY — no UVs/normals; Etap D derives world-space UVs in the renderer (labeled RENDER_RECONSTRUCTION) or extends this module.** `worldHeightMeters(u16)`, `HEIGHT_QUERY` (FUN_0047fb20 form, identity min/max — min/max source UNRESOLVED).
- `PEFoliageCore.js` — `generateInstances({records, windowU16, windowWorld, level, viewBand, p3=0})` → `{instances, census}`; `VegetationRNG {seed(p1,p2,p3,p4,p5), next01()}`; `sampleModelScale(rng,min,max)`; `subdivisionStep(level)`; `packedQueryPosition`; FOLIAGE_OPERAND_LOCK (byte-locked f64 constants + f32 rounding points, CONDITIONAL exactness status); FOLIAGE_PLACEHOLDERS ([P-CLIMATE], [P-CELLSTREAM], [P-RNG-P3], [P-SCALE-FIELDS], [P-WINDOW]). **Launcher findings: (a) NO LAB_SEED parameter exists — the reconstruction stand-in `placementHash` is seedless; the Etap E wrapper must add a DOCUMENTED LAB_SEED input into [P-CELLSTREAM] content generation (never into the locked RNG arithmetic). (b) p3 default 0 = [P-RNG-P3] UNVERIFIED, shown separately. (c) instance count per sub-cell = max(0, round(col1)) per record — the 5000-visible-instance cap is a RENDERER-side limit, reported as requested/rendered/limited.**

### 1.4 src/pecompat (models, Etap E)

- `PecNif10Reader → PecSceneIR → PecAssetAdapter → PecInstanceBuilder → PecRenderConvert` — version gate NIF 10.1.0.0 exact; resource/instance separation; (x,z,-y)×0.01 render conversion applied exactly ONCE, labeled RENDER_ADAPTER_CHOICE / PE_UNITS_NOT_CONFIRMED. Reuse for supported vegetation models.
- `src/pesource/NifModelReader.js` — SINGLE-WITNESS (457485) reader; never widened without its witness regression. Not used as a general importer.

## 2. What is MISSING for the launcher (measured gaps → minimal new work)

1. **io adapters** — BrowserSourceAdapter/NodeSourceAdapter do NOT exist (comment-only). Minimal adapters are established patterns in-tree:
   - Node (server side): `{ readFile: fs→Uint8Array, inflate: zlib.inflateSync, sha256: crypto }` — exactly `tools/iter020_material_audit.js` L36-41.
   - Browser: `{ readFile: fetch→Uint8Array, inflate: DecompressionStream('deflate'), sha256: crypto.subtle }` — exactly `terrain/p0.js` L24-42.
2. **Bounded world server** (NEW, `compat/server-world.mjs` style extending server-catalog.mjs's design): port **8162** (verified free by phase 1; standing servers 8140/8161 untouched), routes `/launcher`, `/world`, `/` → launcher redirect; explicit PID, READY status, own-process stop only; **server-side PESourceMount** with bounded JSON/binary API (tile heights, material masks, texture RGBA, climate records, catalog gaps panel) — **NO arbitrary path reads and NO whole-container downloads to the browser** (contract §4; the old terrain/p0.js prototypes fetched whole terrain.bnt via `/pcg/` — NOT the launcher pattern).
3. **Tile streaming component** (NEW, `src/peworld/`): ≤64 active tiles around the camera, camera-distance ring order, NODATA = stop/boundary (never void-drop), async with progress (SDK BackgroundLoad pattern — mechanism 5), controlled memory + unload.
4. **Terrain texture chain module** (NEW, Etap D): TDF entry+record → material identifier/name → **texture entry relation (materialId==textureId NOT established — mapping-table provenance or explicit unresolved-binding diagnostic)** → PCG Textures.bnt payload → `decodeTga2` → GPU sampler; blend = Stone04-base + independent alpha overlays, RENDER_RECONSTRUCTION label; texture toggle actually re-renders.
5. **Foliage wrapper** (NEW, Etap E): LAB_SEED → [P-CELLSTREAM] stand-in content (documented wrapper; locked RNG untouched); same source+era+profile+seed+calibration+tile-key → identical instance set; instance keys + edge ownership; profile picker from `getVegetationClimate` (0..31; default = measurably justified, never "historical biome"); VEGETATION_MODE = RECONSTRUCTION_PREVIEW.
6. **Launcher UI** (NEW, `compat/launcher*`): connection status/era/loading stages; height overview from the REAL terrain.bnt index (downsampled to screen, NODATA ≠ 0, raw u16 on hover, async refresh with progress + percentage/denominator coverage); region/tile pick; vegetation profile + LAB_SEED + density preview; "Uruchom podgląd świata" entry; model-catalog link + gaps panel; original-data vs reconstruction-settings separation (hashes/offsets in a collapsible evidence panel).
7. **World viewer app** (NEW, `compat/world*`): Three.js 0.185.0 (pinned; no dependency changes), r185 stack; orbit/fly + walk (WASD, mouse after click, ESC); height sampling from the SAME terrain data; fit/reset; back to launcher; toggles (textures, vegetation, wireframe, tile bounds); loading/errors + profile/seed + memory/instance census; position in adapter units + tile key (no "original XYZ" labels).
8. **`npm run serve:world`** (NEW script in package.json).

## 3. Phase breakdown following this map (per contract §4-§8)

- **ETAP C (next)** — server 8162 + launcher + terrain from real tiles: start from a working 4×4-tile patch, then ≤64-tile streaming; terrain invariants (offset 64, raw u16, sentinel/NODATA, calibration labels, conversion once); §8 terrain controls incl. the 64-vs-52 negative control and independent byte re-reads.
- **ETAP D** — original terrain textures: the §2.4 chain on ≥1 real tile + same path for all supported layers of the patch; §8 materials controls (mask@56 on used samples, malformed/RLE fail, raw weights unchanged, unresolved binding explicit, wrong-era refusal, UV/flip control with a real texture).
- **ETAP E** — trees/climate/seed: the §2.5 wrapper + ≥1 real same-era vegetation model with original textures if binding resolves; unsupported IDs = explicit counts + optional diagnostic marker (never a stock pine under the same ID); unload frees unused instances/materials without destroying shared resources.
- **EXPLORATION (§7)** — orbit/fly/walk + toggles + census panel; browser smoke launcher→map→enter→terrain→texture toggle→profile/seed change→move→return→re-enter with console/network evidence; DATA_VALIDATED/APP_LOAD/PIXEL_RENDER/INTERACTION_VERIFIED separated (INTERACTION honest NOT_PERFORMED while the 9222 daemon is down).

## 4. Reuse rules (standing)

- Reuse the modules above BEFORE writing parallel code; the catalog data model (`tools/pecompat/catalog_data.mjs`, CAM-fixed this run) feeds the launcher's gaps panel through the same era/identity discipline (asset identity = era + container SHA + entry name + payload SHA).
- Historical r169 runtime knowledge (EudoriaWorldTransform etc.) is REFERENCE for THAT pipeline — the launcher world profile is PCG_9_3_5 with CURRENT_RUNTIME_CALIBRATION labels (u16/128, 2 units/sample, identity min/max), never historical meters/axes claims.
- This map is a DRAFT: file names may change at implementation; every module listed was verified against its real source this phase (identities in INPUT_IDENTITIES.json).
