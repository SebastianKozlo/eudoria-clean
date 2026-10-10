# CATALOG_METHOD.md — PE_CITY_ASSET_MAP_R1_20261010 (phase 2: METADATA_CATALOG)

Method record for the full metadata catalog of both eras + rankings (contract §2).
Everything below was executed by this executor on 2026-10-10 in the run worktree
(`D:\Eudoria_Reconstruction\12_WebGame\pe-city-asset-map-r1`, branch
`codex/pe-city-asset-map-r1-20261010`, HEAD `59641ca`; no commit made in this
phase — publication is a later, explicitly-assigned step). All original inputs
were READ_ONLY.

## 1. Era discipline (mandatory on every record)

- `CD_2003` = the 2003 CD-installer corpus (`D:\Eudoria_Reconstruction\pcg2003_install\Data\**`: Models.ark, Textures.ark, Scripts.ark, Volumes.ark).
- `PCG_9_3_5` = the PCG 9.3.5 installation (`D:\Eudoria_Reconstruction\pcg_install\Data\**`).
- The two eras are NEVER mixed: every census row, catalog row, ranking row and search result carries an explicit `era` field. Cross-era numbers appear only in the explicitly-labeled `crossEraSearch` block (exact-name matching only).
- Asset identity = `ERA + CONTAINER_SHA256 + ENTRY_NAME + PAYLOAD_SHA256`. A numeric ID alone is never globally unique.

## 2. Tools written this phase (all in `tools/pecompat/`, non-proprietary code)

| Tool | Purpose | Reuse label |
|---|---|---|
| `catalog_census.mjs` | physical-file census of one Data tree (relpath, size, ext, era, SHA256 streaming, status) | none (new, trivial) |
| `catalog_sniff.mjs` | bounded header-only payload classification (NIF/DDS/TGA/OTHER) | format facts from pe-ark-vfs / pe-bnt-tdf skills |
| `ark_index.mjs` | full CD_2003 .ark entry catalog + dual-index verification | **`src/pesource/ArkArchive.js` imported UNCHANGED** (era-validated ArkVFS reader: sequential local-header scan + EOCD cross-check; STORED-only readEntry with loud refusal of unexpected compression) |
| `bnt_index.mjs` | full PCG_9_3_5 BNT2 entry catalog | **`src/pesource/Bnt2Archive.js` imported UNCHANGED** (era-validated BNT2 footer/directory reader with exact directory-end check; raw payload readEntry with EOF bounds; used for Models.bnt entry 781 in the SceneIR run) |
| `vfs_inspect.mjs` | bounded header/structure inspection of the 3 Parameters vfs files | format facts from pe-bnt-tdf skill (ArkVFS02 16-byte serialization header) |
| `nif_batch_extent.mjs` | bounded batch decode of PCG935 NIF 10.1.0.0 models for SCENE_EXTENT/COMPLEXITY | **`src/pecompat/PecNif10Reader.js` + `src/pecompat/PecSceneIR.js` imported UNCHANGED** (the era-validated reader chain from the SceneIR run; strict 10.1.0.0 version gate; full-file closure contract; FILE_SCENE_SPACE composition) |
| `catalog_rankings.mjs` | builds the 3 rankings + coverage + primary rows + cross-era search + private artifact references | reads only this phase's own outputs |

## 3. Hash & verification policy per container

### CD_2003 Models.ark (SHA256 f660d055…, 128,742,137 B — pin from phase-1 INPUT_IDENTITIES, re-verified fail-closed at load)
- Index = sequential local-header scan (`AK\x03\x04`) via ArkArchive; EOCD totals cross-checked inside the reused reader (a mismatch would throw).
- **Dual-index verification (NEW this phase)**: the central directory (at EOCD cdOffset/cdSize) was walked with BOTH documented layouts. The pe-ark-vfs skill's speculative layout (name_len u32 @28) **failed 2,492/2,492**; the **standard-ZIP central-directory layout matched exactly (2,492/2,492 names + local-header offsets + local-header re-reads agree, 0 mismatches)**. Honest finding: for this container the central directory is standard ZIP-structured; the skill's CD layout hypothesis is wrong for this file.
- Boundaries: every payload ends before the CD (last payload end == cdOffset exactly); CD+cdSize == EOCD offset; EOCD+22 == file size exactly.
- Per entry: CRC32 stored vs computed over payload (2,492/2,492 verified, 0 mismatches), payload SHA256 (2,492/2,492 hashed), compression census (all 0 = STORED; stored==uncompressed for every entry), flags census (all 0), duplicate names (0).
- Header sniff: 2,492/2,492 NIF; version distribution (measured): 1,815 × 4.1.0.12, 440 × 4.0.0.2, 237 × 4.0.0.0.

### CD_2003 Textures.ark (SHA256 d611d125…, 289,585,581 B — re-verified)
- Same reader, same dual-index verification (standard-ZIP CD layout exact 4,833/4,833; skill layout failed 4,833/4,833), same boundary checks (all exact), CRC32 4,833/4,833 verified, all 4,833 payloads hashed, 0 duplicates, all STORED.
- Sniff: 1,359 DDS + 3,433 TGA_HEADER + **41 OTHER**. The 41 OTHER are `.tga`-named tiny files (4–96 B) with no image header — content UNKNOWN, NOT decoded in this phase (CRC-verified, kept visible). Historical "3,474 TGA" (extension-based) reconciles exactly as 3,433 header-confirmed + 41 stubs.

### PCG_9_3_5 Models.bnt (PINNED: SHA256 c950a8c2…, 395,412,868 B — pin MATCH, work authorized)
- BNT2 footer magic verified by the reused reader; full directory parsed to the exact end (reader-validated). **Count re-derived by this run: 5,596 entries** (predecessor census 5,596 = 4,838 + 757 + 1 is COMPARISON evidence; my own sniff re-measured the same distribution: 4,838 × Gamebryo 10.1.0.0, 757 × NetImmerse 4.1.0.12, 1 × NetImmerse 4.0.0.2 — MATCH, independently reproduced).
- Payloads are RAW 1:1 (all 5,596 first-bytes sniffed as direct NIF header strings — consistent with the SceneIR raw extraction of 218757.nif; the pe-bnt-tdf skill note "Models.bnt zlib-compressed entries" describes a DIFFERENT-ERA file and does NOT apply to this container).
- Boundary facts: 0 overlaps, 0 gaps, monotonic offsets, no payload crosses the directory or EOF.
- Per entry: CRC32 verified 5,596/5,596 (0 mismatches), payload SHA256 5,596/5,596, 0 duplicate names.
- **Pad-field finding**: the directory row's trailing u32 equals crc32 for only 3,435/5,596 entries (and 5,572/8,381 in Textures.bnt). Pad semantics where unequal are UNKNOWN — recorded raw, not interpreted. The skill's "CRC32 stored twice per entry" claim is therefore MEASURED_PARTIAL, not universal.
- Independent hash-pipeline verification: my catalog's payload SHA256 for entry 781 `218757.nif` equals the SceneIR run's pinned payload SHA256 (`3e8a22c2…`) exactly.

### PCG_9_3_5 Textures.bnt (SHA256 61acd13b…, 973,942,771 B — re-verified)
- **Format verified as BNT2 with the SAME reused reader — layout NOT different** (full directory parsed to exact end). **8,381 entries** — explicitly NOT the 8,095-entry EU2008-era copy described in the skill (a different-era file; never mixed with this corpus).
- Boundaries: 0 overlaps, 0 gaps, monotonic, exact end; CRC32 8,381/8,381 verified; all 8,381 payloads hashed; 0 duplicates.
- Sniff: 2,752 DDS + 5,610 TGA_HEADER + 19 OTHER (tiny stubs, UNKNOWN, kept visible).

### Parameters vfs (textures/materials/templates.vfs)
- BOUNDED header/structure inspection ONLY — no full decode attempted or claimed; record layouts NOT established in this phase.
- All three: `ArkVFS02` 8-byte signature confirmed; identity (SHA256+size) re-verified at use time — all MATCH. Header metadata bytes recorded raw (meaning UNKNOWN). materials.vfs contains HLSL shader text from offset 32 (bounded string census, 2,668 strings — consistent with the pe-bnt-tdf skill note); textures.vfs is 1,552 B mostly binary (1 string = the signature); templates.vfs is 560,788 B mostly binary (7,703 strings, layout NOT established).

## 4. Batch decode policy (SCENE_EXTENT / COMPLEXITY)

- The existing era-validated reader chain (PecNif10Reader → PecSceneIR) was used AS IS on all 4,838 NIF 10.1.0.0 candidates of PCG935 Models.bnt. **NO parser expansion** (contract §2/§task: a first systematic parser failure does NOT trigger unlimited parser repair; the 4-model deep NIF 4.x formats are phase 3's bounded scope).
- Result: 1,551 DECODED with mesh bounds; 17 DECODED without mesh geometry (extent UNKNOWN — never 0; their zero triangle/vertex counts are REAL measured values); 3,270 FAILED, all with LOUD unregistered-block-type errors (top unknown types by full-census message count: NiTextKeyExtraData 1,030, NiKeyframeController 795, NiTextureEffect 418, NiStencilProperty 328, NiSkinInstance 181, … — full histogram in CATALOG_COVERAGE.json `batchDecodeDetails.unknownTypeCensus`). Every failure is kept visible per entry.
- The 758 NIF 4.x entries (757 × 4.1.0.12 + 1 × 4.0.0.2) are outside the reader's strict version gate — never attempted, counted as unsupportedNeverAttempted.

## 5. Rankings discipline

- Three DESCENDING rankings, each with a mandatory COVERAGE line (total / measured / unsupported / failed): PAYLOAD_SIZE (both eras, FULL coverage), SCENE_EXTENT and COMPLEXITY (PCG935 measured subset only; CD2003 all UNKNOWN in this phase).
- **All tables are largest-MEASURED** — coverage is incomplete, so "largest city"-style claims are FORBIDDEN and NOT made. Big file ≠ biggest extent ≠ most complex (the tables are separate and never merged into one verdict).
- Axis frame (SCENE_EXTENT): FILE_SCENE_SPACE — the file's own serialized x/y/z labels, NO axis swap, NO unit conversion; world = parentWorld × local TRS composed from the proven root (PecSceneIR semantics). Axis semantics (e.g. which axis is up) are NOT established by the reader. **Units are ORIGINAL file units — never called meters.** footprintX/footprintZ (x,z extents) are provided alongside maxAxisExtent so a flat model can never be hidden behind one number. SOURCE_FILE_SCENE_SPACE ≠ WORLD_PLACEMENT.
- COMPLEXITY units (explicit): triangles = NiTriShapeData triangle count; vertices = vertex count; shapes = NiTriShape blocks; nodes = NiNode blocks.
- UNKNOWN is visible and sortable as UNKNOWN — never 0.

## 6. Output placement (contract §8)

- Report package (this directory): `CATALOG_COVERAGE.json` (schema, counts, coverage, bounded top-50 tables, 4 primary rows, cross-era search, private artifact references), this method file, the appended INTERVENTION_LEDGER.md. **No proprietary payload content** — only metadata (names, sizes, SHAs, counts, bounded format-identifying string samples).
- PRIVATE_OUTPUT (`D:\Eudoria_Reconstruction\99_Audits\PE_CITY_ASSET_MAP_R1_20261010\PHASE2_*`): full file censuses, full entry catalogs (CSV+JSON), full rankings, batch state (JSONL), vfs inspections — 20 artifacts, every one referenced by absolute path + SHA256 + size in CATALOG_COVERAGE.json.

## 7. Honest limitations (phase scope)

- CD_2003 NIF 4.x models: NOT decoded in this phase → SCENE_EXTENT/COMPLEXITY UNKNOWN for all 2,492 (phase 3 decodes the 4 primary models only).
- PCG935: 3,270/4,838 NIF 10.1 candidates failed on unregistered block types (the reader's supported block surface is the 218757-corpus lineage); no repair attempted.
- The 41/19 `.tga` stubs, the BNT2 pad semantics where unequal, the vfs record layouts: UNKNOWN — recorded raw, not interpreted.
- Cross-era search = exact entry-name matching of the 4 literal IDs only. Absence of the literal ID is NOT proof of absence of a counterpart (contract §3); no silhouette/geometry guessing was performed.
