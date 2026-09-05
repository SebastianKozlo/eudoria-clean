# M1 GATE DELIVERABLE MATRIX — PE_WORLD_SURFACE_FIDELITY_R1
# Milestone-gate preparation deliverable (charter §13 FINAL MATRIX + fresh regression sweep + era-bounded registry + known-open list)

- SESSION: M1 ITER_048 (ledger ITER_034), 2026-09-04 15:30 physical
- CHARTER: PE_MILESTONE_1_WORLD_SURFACE_R1 (SHA256 7A10CD2BE286499540C6668C90E63897781BF6B472541FF0CCB75ADA84562ECA — verified in-session, read IN FULL)
- GOVERNING LEDGER ENTRIES: #2 (clean runtime strategy), #3 (foundation gate refinement), #7 (backup-first + M1-E start), #8 (English repo + GitHub remote), #9 (Three.js r185 target)
- CLEAN RUNTIME: eudoria-clean @ git b7d38ad (master, origin in sync; three@0.185.0; THREE_R185_PROJECT_BASELINE = CALIBRATED)
- LEGACY ORACLE: eudoria-web r169 FROZEN (LEGACY_REFERENCE / DEBUG / REGRESSION_ORACLE — ledger ENTRY #2/#9)
- ERA LABELS: **JUL_2003** (charter primary target; 01_Original_Files\BNT\50.bnt SHA A6E59EE0...), **PCG_9_3_5** (pcg_install; the clean-runtime primary era per ENTRY #2/#6; Entropia.exe 9.3.5.6746 SHA E7785430...), **CD_JAN_2003** (Textures.ark SHA D611D125...), **EU_LATER** (Textures.bnt SHA 2EAE1159...)
- SWEEP EVIDENCE: 03_EVIDENCE\iter034_regression_sweep.json (per-page fresh results)
- THIS FILE IS THE INPUT TO THE MASTER AUDITOR'S FULL_MILESTONE_AUDIT.

TAXONOMY: CONFIRMED / STRONGLY_SUPPORTED / PLAUSIBLE / UNVERIFIED / REJECTED.
Every evidence SHA below was re-hashed on disk THIS session (see iter034_regression_sweep.json.evidenceShaVerification — 0 failures). No row is filled from memory.

---

## PART 1 — THE 19-ROW FINAL MATRIX (charter §13)

Row format: verdict | KNOWLEDGE | IMPLEMENTATION | VALIDATION | HISTORICAL_FIDELITY | EVIDENCE_STATUS | evidence (file + SHA) | era | honest bounds

### ROW 1 — TERRAIN_HEIGHT
- **VERDICT (structure/bytes): CONFIRMED** | engine height-form: identity+operation CONFIRMED, final semantic role STRONGLY_SUPPORTED
- KNOWLEDGE: JUL_2003: TDF payload heights = 32×32 uint16 LE at payload offset 64 (52-byte header + 12-byte sub-header; the two offset spaces NEVER collapsed); PCG_9_3_5: PE2003 client decode FUN_0047fb20 = min + (max-min)*u16/65535 (per-tile min/max lerp — identity + observed operation CONFIRMED at VA; the 9.3.5 sibling FUN_00989e70 = square-u16-grid scale-by-float CLAMP-to-65535).
- IMPLEMENTATION: clean chain = terrain.bnt/50.bnt bytes → PESourceMount (BNT2_TERRAIN/BUNT, BUNT_TRAILING_BYTES=8) → TerrainTile (provenance per tile) → PETerrainCore (height = u16 × 1/128 m, CURRENT_RUNTIME_CALIBRATION; disjoint-tile borders kept AS ORIGINAL DATA, no repair).
- VALIDATION: 9/9 region tiles byte-faithful vs an INDEPENDENT second parser (tools/p0_byte_audit.js); 9216/9216 samples IDENTICAL vs the frozen r169 oracle chunk (built from JUL-identical source tiles); JUL full-map rebuild SHA 3DC16D52... == audit-accepted iter002 (ledger ITER_005); sentinel 7ffe7ffe.tdf EXPLICIT_NOT_ASSEMBLED.
- HISTORICAL_FIDELITY: heights byte-exact from ORIGINAL bytes (both eras; 773/51,920 PCG-vs-JUL tiles differ in heights — era divergence recorded, never mixed).
- EVIDENCE_STATUS: CONFIRMED (byte-level); heightScale 128 u16/m = STRONGLY_SUPPORTED (runtime calibration, not an engine-extracted constant).
- EVIDENCE: iter019_p0_browser_result.json (SHA 20CFC413E530E3F7C67760E884977F23970EEA6167E75E6159FEFE5CA8EC3FC9); iter019_p0_byte_audit.json (4C29D22071E3E9CACD4744329B985EA534CFF1558C93F761AD1A8E89B2EF7A6B); iter019_era_validation_terrain_bnt.json (D2D13D84558E337D8A3B8CA14DAFA8240A8B4A4B4B97AFA470F707141183F1DD).
- ERA: JUL_2003 + PCG_9_3_5.
- HONEST BOUNDS: the per-tile min/max SOURCE is UNRESOLVED (sub-header reads zero on 386/400 sampled tiles, iter020 P1; identity lerp used); the full-lerp form in 9.3.5 itself is UNRESOLVED (see KNOWN-OPEN #9).

### ROW 2 — TERRAIN_GRID
- **VERDICT: CONFIRMED**
- KNOWLEDGE: JUL_2003: BUNT footer filename-xy grid 220×236 = 51,920 regular + 1 sentinel (7ffe7ffe.tdf); PCG_9_3_5: BNT2 footer, 58,451 entries = 51,920 regular (SAME filename-xy convention) + 6,530 special-row (y=0xff1a..0xffff) + sentinel; tile world size = 128 units (from the >>7 math, engine-confirmed iter030).
- IMPLEMENTATION: PESourceMount era-validated decoders (BuntArchive JUL / Bnt2TerrainArchive PCG — versioned per ENTRY #3, never one interpretation forced across eras); sentinel handled explicitly.
- VALIDATION: iter019 era-validation 0 walk failures (58,451 entries); iter008b full-corpus walk exact consumption 51,920/51,920; denominator checks 7040×7552 in-browser (ledger ITER_005 r2).
- EVIDENCE_STATUS: CONFIRMED.
- EVIDENCE: iter008b_winning_walk.json (AAFD1A4EB0E459C27C597E5AEF96EEEA4B187F8F40EBA9D7AFA274AADFF80E11); iter019_era_validation_terrain_bnt.json (D2D13D84...); iter030_findings.json (1104F3186116A98856438741D7F7439E25E6DEF578EAD6D2AA666812B3951207).
- ERA: JUL_2003 + PCG_9_3_5.
- HONEST BOUNDS: the 6,530 special-row tiles = structure-censused (2,386 B dominant payload, ds=2100 dim=32; LOD-skirt candidate) but semantics UNRESOLVED (KNOWN-OPEN #6).

### ROW 3 — TERRAIN_WORLD_TRANSFORM
- **VERDICT: STRONGLY_SUPPORTED (engine facts CONFIRMED; the clean pages' global georef intentionally NOT claimed)**
- KNOWLEDGE: engine world = 131,072 units (ArkHeightTree root size key 65,536 half — iter028, vtable-proven); tile = 128 world units (>>7 math — iter030); m→cm ×100 (FUN_0082b790 — iter031); the height field covers the FULL world at 512-unit texels origin -65,536 (FUN_009478e0 — iter029); climate/detail grids cover the CENTER 65,536-unit region (origin -32,768).
- IMPLEMENTATION: clean pages render REGIONS: per-tile meshes at TILE_WORLD=128 on a local grid; no global-world placement claim made; cm→m bridge 0.01 labeled [P-UNITS] (foliage page).
- VALIDATION: deterministic renders + the heights oracle (rows 1-2); the engine constants address-cited (iter028/029/030/031 decompiles).
- HISTORICAL_FIDELITY: the tile/world sizes are ENGINE-CONFIRMED; the runtime's regional placement is explicitly a reconstruction window ([P-WINDOW]), not a claimed historical world positioning.
- EVIDENCE_STATUS: STRONGLY_SUPPORTED; the cross-era FIELD-vs-TILE georeferencing UNPINNED (r 0.527 saturation — iter028; the measured contradiction: field at engine addressing −130..−125 m vs tiles +16..+487 m — iter030 paletteProbe).
- EVIDENCE: iter030_findings.json (1104F318...); iter031_water_findings.json (2f9bef450e74e49886af958b573f98c6e2c465d368f203587f6fcc82269c9eb8); iter030_page_result.json (9B62AD3399F8D1D4E295862D5B065D580D5AB66E7DBA6655DD03FF3F20F8E39B — the [P3b] measured contradiction).
- ERA: PCG_9_3_5 (engine facts); JUL_2003 (tile data).
- HONEST BOUNDS: [P3b] — the row-input substitution on the materials_confirmed page is backed by a MEASURED contradiction, not a silent choice; the georef pin is a KNOWN-OPEN (#5) that needs the 2010-era local terrain or runtime tracing.

### ROW 4 — TERRAIN_MATERIAL_RECORDS
- **VERDICT: CONFIRMED (structure, both eras; consumer role CONFIRMED 9.3.5)**
- KNOWLEDGE: JUL_2003: TDF tail = single size-tagged record sequence [u32 size][u32 dim][size-4 bytes], stride size+4, EXACT consumption 51,920/51,920; 175 distinct material ids (id↔name many-to-many recorded); masks RAW + RLE-(count,value) exact; record order base-first (Stone04 51,521 tiles position-0). PCG_9_3_5: the payload RECONCILED as the serialized MaTerrainMapPatch (the patch serializer FUN_00934970 byte-matches the container framing; the 52/64 offset-space confusion unified); layer TYPE census {0: u16 heights, 2: per-material masks (sub@+16 = the material's TEXTURE id; Stone04=13382), 3: dim-32 masks, 6: sub-id'd per-tile texture-carrier planes (1/tile, dim 2, 18093=87%), 7: u16 normals (computed FUN_009362d0), 9/0xa: system}; THE MASKS DRIVE THE LOD MESH VERTEX-COLOR BAKE + THE ZONE SHADOW PAINT (FUN_00941710/FUN_00940de0/FUN_009402b0; the zone mode-1 alpha-modulation writer) — NOT the base/factor/detail texel source (the exhaustive 838/838 terrain-range consumer census; NO other reader exists).
- IMPLEMENTATION: TdfMaterialTailDecoder.js (format layer: named dim=16 records decoded RAW/RLE; system records dim=2/4/8/32/256 carried RAW with UNVERIFIED labels, no interpretation); PESourceMount.getTerrainMaterials (provenance on every object + tailConsumedExactly).
- VALIDATION: iter008b corpus exact-consumption; iter020 64/64 records vs INDEPENDENT DataView-level parser; iter021 era-divergent region 95 records both parsers exact; JUL oracle iter008b tile lists 9/9 sequence match; >4-material tiles rendered AS-IS (the legacy 4-cap = a structural difference recorded, not "fixed").
- HISTORICAL_FIDELITY: record grammar CONFIRMED on original bytes both eras; consumer semantics CONFIRMED at code level for 9.3.5; JUL-era runtime consumer = the Ark11 fallback family + vertex-color bake (era drift is CONTENT never GRAMMAR — iter030).
- EVIDENCE_STATUS: CONFIRMED.
- EVIDENCE: iter008b_winning_walk.json (AAFD1A4E...); iter020_material_decode_audit.json (51898ABC09B15F6711634955928B8DF56FD35B4E2B2E17BDCAEB7543F223F458); iter030_findings.json (1104F318...); iter030_pcg_tile_census.json (C3EB3C28CBEF2926E2A706F51D437D07C793C10D6A2CA74017FBD49F30E7F071).
- ERA: JUL_2003 + PCG_9_3_5.
- HONEST BOUNDS: dim=2/dim=4 record SEMANTICS UNRESOLVED (KNOWN-OPEN #7/#8); the type-2/sub-0 zone scratch reader NOT located (KNOWN-OPEN #11); Grassmix04 duplicate-id + unnamed dim=16 512-byte system records recorded (iter021, KNOWN-OPEN #24).

### ROW 5 — TERRAIN_TEXTURE_RESOLUTION
- **VERDICT: CONFIRMED (resolution layer, oracle-verified); the world-data grids MISSING/ERA-BOUNDED (patcher-delivered — honest)**
- KNOWLEDGE: material record id@+16 → texture resource: BNT2 entry '<id>.dat' (EU_LATER 175/175; PCG_9_3_5: 8,381 entries, region ids 10/10 + 20/20 same-era, 0 fallbacks); CD_JAN_2003 '<id>.tga' 171/175 (Cabbage_01-03 + Rock02e later-era additions — the era gap REAL, handled explicitly); payload = TGA 2.0 uniform 256×256×24 uncompressed bottom-up (175/175 + 171/171); the 9.3.5 climate system textures: 17 palettes 64×256×32bpp + 79 details 256×256×24 (96/96 manager ids EXIST in PCG Textures.bnt — iter027); the global world-data set: 429259 (257×257 heights, LOCAL both 9.x eras, absent 2003), 432502 (65×65 climate grid, MISSING locally), 459344 (129×129 detail selectors via tables C/D/E, MISSING locally) — the missing two are PATCHER-delivered (ClientLoader = WinInet FTP; the client fetch is LOCAL-ONLY and a miss HALTS init — iter029).
- IMPLEMENTATION: PESourceMount.resolveTexture (era-explicit, LOUD NOT_FOUND, provenance era/container/entry/offset/SHA/crossEra) + TgaDecoder (validated TGA2 subset, loud failures); the pages fetch palettes/field/details LIVE with SHA provenance (materials_confirmed bindings: 458791 C551707C..., 458792 A2608374...).
- VALIDATION: frozen M3-2-R1 provenance manifest agreement 175/175 (INDEPENDENT pipeline); M3-4 witness-set intersection 0 (disjoint id space — non-circular); iter011 cross-run hash drift 0; four-era byte-identity for the 5 water textures.
- HISTORICAL_FIDELITY: every resolved payload is ORIGINAL era bytes, era-labeled; NO silent cross-era (the CD-only 4-id gap recorded, never papered over).
- EVIDENCE_STATUS: CONFIRMED (resolution); MISSING-locally items honestly bounded ([P1]/[P2] placeholders; KNOWN-OPEN #4).
- EVIDENCE: iter010_id_resolution.json (ECA9B3588D99D1FF44CCC880B1EE82A245113DE1EB86357ED715C1F4AAF10D2A); iter011_payload_classification.json (86271B9F08BF2057B846C3D21F10E1B0E385E9266575A5B47B4E91BA3BB0C2CE); iter030_page_result.json (9B62AD33... — the detail bindings).
- ERA: JUL_2003 (terrain ids) / PCG_9_3_5 (primary resolution era) / CD_JAN_2003 + EU_LATER (cross-era texture containers, every resolution tagged).
- HONEST BOUNDS: the era-correct JUL_2003 texture container DOES NOT EXIST (auditor-verified; both usable corpora CROSS-ERA by construction — tagged per resolution); 110/175 ids era-stable, 61 divergent (which version matches JUL_2003 undecidable from bytes — PLAUSIBLE: CD closest in time; UNVERIFIED).

### ROW 6 — TERRAIN_BLEND_SEMANTICS
- **VERDICT: CONFIRMED (era 9.3.5: shader op + factor content + filtering; code + data + gate)**
- KNOWLEDGE: TERRAIN_14 technique (materials.vfs 0x3ea, ps.1.4 + vs_1_1, byte-extracted): D = d0*w0 + d1*w1 + d2*w2 (weights = the FACTOR texture RGB channels u8/255, UNRENORMALIZED in-shader) → per-channel OVERLAY onto the base keyed on D vs 0.5 (D>=0.5 → 1−2(1−b)(1−D), else 2bD) → light/shadow/fog (the shadow term = the base alpha: 'mul r0, r0, r0.a'); THE FACTOR CONTENT = ONE-HOT band selection by the palette-ALPHA 3-band partition (alpha≥73→R, 53..73→G, <53→B, A=255) + noise + accumulated weight — NO normalization needed or performed (the iter025/026 'per-cell renormalization' candidate REFINED into the one-hot model; RAW + CLAMP255 falsified by measurement); the BASE = the palette bake (row = altitude 255*(1−(h−2)/512−noise2), col = 63*(noise1+roughness)); LAYER CAP = 3 details + 1 base per ps.1.4 pass; FILTERING states verbatim (base/factor: CLAMP + LINEAR/LINEAR/POINT-mip; details: WRAP + LINEAR/LINEAR/LINEAR-mip, LOD bias −0.5, repeats 32/32/16); Terrain_14 CONFIRMED as the LOADED primary (mode-2; Ark11 fallback mode-1 — iter026 selector FUN_009518e0); the TDF masks feed the VERTEX COLORS (row 4), NOT the factor.
- IMPLEMENTATION: terrain/materials_confirmed.html+js renders the CONFIRMED architecture (palette bake + one-hot factor + tables C[0]/D[0]/E[0] details + the full Terrain_14 ops incl. the shadow term); terrain/materials_wsum.html kept as the labeled comparison model; the naive 'sequential overlay mix' CURRENT_RUNTIME_CALIBRATION was FALSIFIED for the real engine (iter024) — superseded, not deleted.
- VALIDATION: the HLSL extracted byte-faithfully from the ORIGINAL materials.vfs (both eras for Water/Vegetation; Terrain_14 = PCG era); the producer FUN_00939c40 decompiled + disasm-pinned; the 53/73 thresholds byte-match the ORIGINAL palette alpha values ({45,62,85} partition — the double data-side confirmation); the 18-tile worked-example gate 0.0% white saturation (vs naive 84.0%/43.4%); the page's own renderQuality probe reproduces the signature (fresh sweep: naive 43.36% vs confirmed 0.0%).
- HISTORICAL_FIDELITY: the blend semantics are era-9.3.5-CONFIRMED from the shipped .fx + binary; the PE2-2003 fixed-function blend is era-divergent RECORDED (never auto-propagated).
- EVIDENCE_STATUS: CONFIRMED (era 9.3.5); JUL_2003 runtime blend = era-divergent (KNOWN-OPEN #22).
- EVIDENCE: iter024_fx_id_0x3ea_Terrain_14.hlsl (5AE4AF81B54A71E66E1F63A9718A984314D8FCB0763FDFFF19AE0C7EDF8516F1); iter024_blend_op_findings.json (BA08FFD6F92B741AA76E095AA0EEE7066C51AB73CC5CFD8FB39134C4CC204126); iter030_findings.json (1104F318...); iter030_page_result.json (9B62AD33...).
- ERA: PCG_9_3_5 (engine evidence era).
- HONEST BOUNDS: the >4-material reduction (top-4 pre-bake vs multipass) UNRESOLVED (the 3+1 cap is source-anchored; the reduction mechanism open); the quadtree CONSTRUCTION (leaf fields' origin) not RE'd (iter027 bound 1); the LOD bias −0.5 NOT EXPRESSIBLE in r185 (documented renderer deviation).

### ROW 7 — FOLIAGE_SOURCE
- **VERDICT: CONFIRMED (9.3.5 loader positive + the source graph address-cited)**
- KNOWLEDGE: the 9.3.5 client LOADS the foliage system: FUN_0041dae0 registers '.vcl' extension + 'VegetationClimates\' dir + VegetationClimates.bnt container, and CREATES ArkVegetationClimateFactory INSIDE it @0x00420007; 45 ArkVegetation* classes RTTI-proven (TD→COL→vftable chain, file-side deterministic); the client created at init FUN_0044cb70 ← FUN_0044d590 (the SAME init as the palette manager); VegetationClimates.bnt = BNT2, 32 .vcl entries, TAB-SEPARATED TEXT, 492 data rows, 12 numeric columns, 256 DISTINCT model ids; 255/256 resolve in Models.bnt (1 unresolved: 10136 — recorded); both corpus copies BYTE-IDENTICAL JUL==PCG (SHA 7B858401...); **the 2003 PE2 binary has NONE of this (0 loader strings)** — the data pre-dates the loader (era-labeled).
- IMPLEMENTATION: VegetationClimateDecoder.js (FUN_0083a7d0 semantics: the FLAT 12-value token stream → 0x30 records; reproduces the audited 491-line + 9.vcl continuation census exactly) + PESourceMount.getVegetationClimate (BNT2 framing era-validated, SHA-pinned; provenance with the JUL byte-identity + loader-absence note).
- VALIDATION: the string census + the mount decompile + the RTTI chain (fresh Ghidra project, sandbox SHA-pinned, ~250 functions decompiled); the VCL census re-derived (492/256/32 denominators — the '493' lead corrected to 492, off-by-one recorded).
- HISTORICAL_FIDELITY: for 9.3.5 the foliage is LOCALLY reproducible down to the RNG; for JUL_2003 the VCL data remains the historical reference WITH THE LOADER ABSENT — the era difference is recorded, never silently bridged.
- EVIDENCE_STATUS: CONFIRMED.
- EVIDENCE: iter032_findings.json (af8b900a3864612356a9575ee740f821bcec1b7eb0ff65194e24a36e89b16866); iter032_rtti_chain.json (176bccc010f606c4808df07024e5216ad6ae6da3d8ebbe669e4aca6b6f4f8f8a); iter032_re_dec_0083a7d0_vcl_parser.c (f7e887de9f27f0bd4e294c1cc7c5519018823a534e01dbd43f461b00d85d8a99); iter033_manifest.json (F299C6222917DA8859351D9BE4D2DF0D40F9C6BB7767378DFB22B18C4FFAD46C).
- ERA: JUL_2003 (data) + PCG_9_3_5 (loader/engine).
- HONEST BOUNDS: the .vcl fetch id source + type-id constant UNVERIFIED (KNOWN-OPEN #3); the cell byte-stream origin NOT closed (KNOWN-OPEN #18); the JUL-era foliage RUNTIME semantics = absent-loader era fact.

### ROW 8 — FOLIAGE_MODEL_BINDING
- **VERDICT: CONFIRMED (mechanism) + IMPLEMENTED via GENERATED_CACHE (honestly labeled)**
- KNOWLEDGE: the instance's node+0x19 u32 id → GetModel (type-0x66 fetch: FUN_006c9700/00415670/00823c10 → the 0x14 ArkVegetationModelClient); VCL col0 = the model id source; the model-space ids = the Models container ids.
- IMPLEMENTATION: the clean page binds the 10 distinct climate-0 col0 ids to the DEPLOYED legacy GLB corpus (glb/vegetation/<id>_complete_textured.glb, 'PE NIF10 pyffi' export, 255 files) COPIED READ-ONLY into assets/foliage_glb/ + MANIFEST.json (GENERATED_CACHE class, per-file SHA256); the page VERIFIES every loaded GLB against the manifest SHA at load and records NOT_FOUND LOUDLY (0 misses; fresh sweep reproduced 0 notFoundModels).
- VALIDATION: 10/10 ids resolved in the GLB cache; the manifest SHAs pinned in iter033_manifest.json; the fresh sweep reproduced the binding (76/76 rendered, 0 NOT_FOUND).
- HISTORICAL_FIDELITY: the BINDING MECHANISM is engine-confirmed; the RENDERED MESHES are a GENERATED_CACHE (the export source corpus UNVERIFIED at the file level; the original era Models.bnt NIFs remain the semantic truth) — labeled, not claimed as byte-faithful.
- EVIDENCE_STATUS: CONFIRMED (mechanism) / GENERATED_CACHE (assets, labeled).
- EVIDENCE: iter032_re_dec_0094b1d0_getmodel.c (a0c2c9566eb40ffbe2ec0fd018e65f509fa643cafd2af6b4f0a7623c41168278); iter033_foliage_generator_census.json (3AAFBF4874046395C63EA095B69FC172C4A908E22D0980448BD852416FA80E24); iter033_manifest.json (F299C622...).
- ERA: PCG_9_3_5 (mechanism) / legacy export corpus (assets — labeled).
- HONEST BOUNDS: [P-MATERIALS] the per-model materials = the GENERATED_CACHE GLBs; the clean pesource NIF path = the queued closer (KNOWN-OPEN #21's positive path).

### ROW 9 — FOLIAGE_BIOME_RULES
- **VERDICT: PARTIALLY CONFIRMED (record structure CONFIRMED; the per-location selection UNVERIFIED → [P-CLIMATE])**
- KNOWLEDGE: the 12-column VCL records carried canonically: col1 density 0..330 (median 0.6), col2/col3 scale pair (corr 0.449), col4/col5 elevation bands (corr 0.296), col7 ~maxElev (corr 0.382), col10/col11 probability pair (corr 0.370); ADJACENT CLIMATE INDICES SHARE MODEL SETS (0↔9 Jaccard 0.583, 16↔17 0.500, 30↔31 0.500, 23↔24 0.375); the VCL ids 0..31 vs the palette ids 0x66dc6..0x85527 = DISJOINT value spaces (TWO climate resource families — 'VegetationClimates' vs 'TerrainClimates' — with ONE shared init FUN_0044d590); the .tez = LOCAL terrain edit zones (widths q50 56u, the z field a target height; alignment near-random vs the 1024u climate cells — NO climate carrier; the d>0 20xxx family = west-clustered, era-stable, byte-proven disjoint from templates/hierarchy id spaces except one crossing d=20070==B(template 1969), role UNVERIFIED).
- IMPLEMENTATION: the records decoded canonically into the generator; the climate choice = DOCUMENTED constant index 0 [P-CLIMATE] (the constant-byte-0 convention, like materials P1) — no historical-truth claim.
- VALIDATION: iter032_vcl_columns (census + correlations); iter032_climate_id_space (disjointness measured from both id sets); iter032_tez_zoning_v3 (geometry census, both eras 1015/1020 records); iter022 (the id-space joins, raw + structured, both eras).
- HISTORICAL_FIDELITY: the DATA is original (both eras byte-identical); the SELECTION SEMANTICS (which .vcl applies where) are PLAUSIBLE-UNVERIFIED (the shared-selector hypothesis).
- EVIDENCE_STATUS: structure CONFIRMED; selection UNVERIFIED (honestly bounded).
- EVIDENCE: iter032_vcl_columns.json (a62d9473d6d6d82c97595ceeccbcb915490f95a2b0f14750dbc03075a6526789); iter032_climate_id_space.json (d7541e1d4f5f76fb6bc331fad2e82fe10c8a64af63019e6e85897c1614d01f51); iter032_tez_zoning_v3.json (4892b189c6de2f0783331ac305bdaab4caf4ea200bbf353141173dca59806278).
- ERA: JUL_2003 + PCG_9_3_5 (data era-invariant).
- HONEST BOUNDS: cols 6-11 semantics UNVERIFIED (KNOWN-OPEN #17); the climate→region binding NOT FOUND in .tez (measured negative); the 2xxxx cross-container resource-space hypothesis PLAUSIBLE (no semantics claimed).

### ROW 10 — FOLIAGE_DISTRIBUTION
- **VERDICT: CONFIRMED (mechanism) + IMPLEMENTED with era-bounded [P-CELLSTREAM] stand-in**
- KNOWLEDGE: FUN_0098fe00 = the procedural grid generation (subdivision levels 0..4 → cell steps 1/2/4/8/16; 24-byte cells; density = *(cell+8)>>3); FUN_00990810 = the stored cell records ({u16 x, u16 y, u32 id} triples); FUN_0095b180 = the instance spawn loop (position = u16/K; scale = |rand*2.0| — the MEASURED 2.0f; model id bind; rotation = IDENTITY = the RE-faithful absence, iter032 bound 5); the spawn-loop default subdivision level 1 (settings+4 = 1).
- IMPLEMENTATION: PEFoliageCore.js — the generator with every stage address-cited (the subdivision switch, the triple layout, the spawn fields); the historical cell byte-stream = the LOCAL DETERMINISTIC STAND-IN ([P-CELLSTREAM]: count mapping round(col1) + the placement hash are RECONSTRUCTION-ONLY, recorded).
- VALIDATION: iter033 census over the proven 9-tile region: 76 instances / 4 sub-cells / 4 distinct models (436293 x8, 457485 x20, 457579 x40, 166878 x8) with per-instance seedInputs/rngState0/samplerValue/scale; 28 record-per-cell zero-counts recorded honestly; the elevation-band diagnostic MEASURED without filtering (62 within / 14 outside — the filter rule UNVERIFIED, so the census measures instead of assuming); the fresh sweep reproduced 76/76 exactly.
- HISTORICAL_FIDELITY: the MECHANISM is engine-confirmed; the CELL CONTENT is an era-bounded stand-in (labeled — no historical-truth claim).
- EVIDENCE_STATUS: CONFIRMED (mechanism) / [P-CELLSTREAM]+[P-WINDOW] bounded (content).
- EVIDENCE: iter033_foliage_generator_census.json (3AAFBF48...); iter032_re_dec_0098fe00_grid_gen.c (d02fc56af76c1b1cda2cc85b15736d683bd3d13b945d93d8bdffa27245e2bd9e); iter032_re_dec_00990810_cell_records.c (45339fe1862b967c093da1823c1785a6c5967114bf1d9290a3182682249ebdd7).
- ERA: PCG_9_3_5 (engine).
- HONEST BOUNDS: KNOWN-OPEN #18 (cell byte-stream origin), #19 (rotation/variant candidates FUN_0095ae20/FUN_0095b4f0 unread), #20 (elevation-band filter).

### ROW 11 — FOLIAGE_SEED/RNG
- **VERDICT: CONFIRMED (position-keyed determinism, decompiled + cross-checked 76/76)**
- KNOWLEDGE: the RNG FULLY RECOVERED: position-hash seed = ((p4*16+p5)*16+p1+p2+p3)*0x5CC7 + 0x6D7 (uint32), state = x*8^x; then the MSVC rand() LCG state*0x343FD + 0x269EC3 >> 16 & 0x7FFF; the seed inputs: p1 = the packed 32-bit query position, p2 = the VIEW BAND (10/20/30), p4/p5 = the record u16 pair (POSITION-KEYED); NO global seed, NO server RNG in the local path; the seed-20030130 legacy scatter = VISUAL_RECONSTRUCTION_LEGACY (different BY CONSTRUCTION — documented, no match claimed or tested).
- IMPLEMENTATION: VegetationRNG class in PEFoliageCore.js (the formulas VERBATIM, address-cited); the divisor + lerp per FUN_0098ce30/FUN_0095ac30.
- VALIDATION: the INDEPENDENT python implementation (m1_iter033_rng_reference.py, SHA 43E31935..., written from the Ghidra decompiles NOT from the JS) recomputed ALL 76 instances: state0/samplerValue/scale EXACT agreement, 0 mismatches, PASS + reference sequences; the MSVC constants = an EXTERNAL public LCG matched by the binary's own bytes (non-circular identification).
- HISTORICAL_FIDELITY: the RNG is engine-byte-confirmed for 9.3.5.
- EVIDENCE_STATUS: CONFIRMED.
- EVIDENCE: iter033_rng_crosscheck.json (F8056CD5EC3F7051DAF7799D7B3BAC92A7C9087A012CCD891BE61E70E6337F42); iter032_re_dec_0098cdf0_rng_seed.c (d416a42236a26759c6e2f3dd7c8a8a426880d949fdb80ac1536de477bc5f1221); iter032_re_dec_0098ce30_rng_next.c (0a4af5879de70c1250bb3bd8d80a6cbc5d75e7dcc6e069eb406a7e4244ceb8f5).
- ERA: PCG_9_3_5.
- HONEST BOUNDS: [P-RNG-DIV] the 32768.0 divisor candidate (_DAT_00a7d7a8 runtime-initialized, reads 0.0 statically); [P-RNG-P3] p3 = 0 (*(impl+0x24) UNVERIFIED); p2 = view band 10 STRONGLY_SUPPORTED (not byte-pinned).

### ROW 12 — WATER_SOURCE
- **VERDICT: CONFIRMED**
- KNOWLEDGE: NO dedicated water container (0/53 containers, 0/2,217 files in the PCG Data census); the water data = (a) the TDF material tails (Water01-05 layers; exactly 5 water ids both eras, no others); (b) materials.vfs record 0x3eb = the Water technique (JUL_2003 BYTE-IDENTICAL to 9.3.5 — the technique is ERA-STABLE); (c) the client plane builders: WaterPlane01 @0xa97ce0 → FUN_0093be20 (the no-shader path) / FUN_0093c210 (the shader path, same geometry) → FUN_0093b4c0 plane create → FUN_0094a250 (the ArkHeightTree leaf-corner walk; vertices z = param_7; UV = param_6 x scale) → FUN_007c7140 NiTriShape + FUN_0082b790 scale 100.0; (d) the name-registered texture family WAVES_01/02/03 (FUN_0048be10, type 1000) + sky0/1.tga — NOT in any local container (the 178-container census); (e) MusDef 'DeepWater Theme' = AUDIO ONLY (negative); 'Geowater:0' = a second name-registered water family (FUN_006e8f70, the 0xb7dc gate UNRESOLVED — recorded lead).
- IMPLEMENTATION: terrain/water_system.html+js — the ground terrain UNDER a separate water surface over the proven water window (grid 56-59 x 107-110; 5/16 tiles carry Water02=9088; water-tile heights 7.3..120 m) — the charter Gate D architecture.
- VALIDATION: iter023 exhaustive container/string census (denominators explicit); iter031 dual-era byte-extraction of the technique (SHA 857dea6e... BOTH eras); the fresh sweep hash MATCH.
- HISTORICAL_FIDELITY: all constants carried VERBATIM from the byte-faithful .fx; the non-local textures honestly bounded ([P-WAVES]/[P-SKY]).
- EVIDENCE_STATUS: CONFIRMED.
- EVIDENCE: iter023_water_container_census.json (5F2907E7777C2E18C84ED5C3A7A0CCA2FA49AB05E95D6AF3EE1660FFDFE707E2); iter031_water_findings.json (2f9bef45...); iter031_fx_id_0x3eb_Water.hlsl (857dea6eb601cdd130b0a1fa2ff1a38b419cad7cb94a46521377e173b6449f5f — == the JUL copy).
- ERA: JUL_2003 + PCG_9_3_5 (technique era-stable, byte-proven).
- HONEST BOUNDS: the env object's +0x14 water-wind WRITER open (KNOWN-OPEN #13); 'Geowater:0' family (KNOWN-OPEN #14); the type-6 2x2 mask + 20-byte tail semantics (no consumer in the located path — iter031).

### ROW 13 — WATER_REGIONS
- **VERDICT: CONFIRMED (data-level coherent regions + the RE plane-per-tile-node spawn)**
- KNOWLEDGE: the 5 water materials form COHERENT lake/ocean-shaped 4-connected components (largest 3,805-tile spanning the coastal ring; Water01: 667/307/302/279-tile components); PCG 5,690 / JUL 5,523 water tiles of 51,920 (each id once per tile; Water03 era divergence +167 tiles PCG — recorded); the plane spawn = per material-driver RB-tree tile node (FUN_0093f800 third loop @0x0093ff23: obj[0]==0 → FUN_0093d7d0 region from obj+9 tile grid coords → plane stored INTO obj[0]); the type-6 layer = a per-tile TEXTURE-CARRIER (ALL mean-RGB ~120 neutral gray; present on 46,218 dry tiles too) — the water-plane-candidate hypothesis REJECTED-as-primary (presence does NOT discriminate water); the 12 no-type-6 tiles = era-stable high dry ground.
- VALIDATION: the full-corpus dual-era walk 0 failures; JUL counts == the frozen iter008b census EXACTLY (independent re-derivation); the consumer RE (FUN_00934890 → FUN_00953340 inside the LOD ring builder).
- HISTORICAL_FIDELITY: the regions are ORIGINAL DATA (both eras); the plane model is engine-confirmed.
- EVIDENCE_STATUS: CONFIRMED.
- EVIDENCE: iter023_terrain_minheight_water.json (314949A88AA8B8670E9555977B73F584FDDD343F6BA85F463AC54E276DDEA097); iter031_type6_census.json (8d62122d9a6761f9b95303c959f286a7870515c0cce1a32473c33ad466131322); iter031_water_findings.json (2f9bef45...).
- ERA: JUL_2003 + PCG_9_3_5 (Water03 divergence era-recorded).
- HONEST BOUNDS: none beyond the type-6 semantics note (recorded above).

### ROW 14 — WATER_LEVEL
- **VERDICT: CONFIRMED (engine level constant; the tile-datum mapping bounded [P-DATUM])**
- KNOWLEDGE: THE WATER LEVEL = 10.0f HARDCODED (_DAT_00a7b128 = bytes 00 00 20 41): the plane vertices read z = param_7 = 10.0 (FUN_0094a250); the underwater test FUN_00853a80(x,y) < 10.0 (FUN_0048bff0); the UNIT-CONSISTENCY TRIANGLE: m→cm ×100 (FUN_0093b4c0/FUN_0082b790) + the Terrain_14 WATER_LIGHT window [-5,+10] m (full light AT the water level, full dark 15 m below) — three independent code paths agreeing; the naive 'raw u16 height==0 = water marker' REFUTED at data level (the dominant zero component spans the ENTIRE map — 23,760/24,363 tiles; 82% of zero tiles carry no water; 1,362 water tiles contain no zero sample); water materials CONCENTRATE at tile-min 0 (median 0 vs global 768) — an OBSERVED CORRELATION, not semantic proof.
- IMPLEMENTATION: the water page carries the level as a demonstrative control ([P-DATUM]: engine 10.0 in the FIELD datum; the TILE-datum mapping UNPINNED; page default 0.0 = the iter023 correlation — all labeled in-page).
- VALIDATION: iter023 the hypothesis test (explicit crosstab over 51,920 tiles: zero&water 4,328 / zero-only 20,035 / water-only 1,362 / neither 26,195); iter031 the RE triangle.
- HISTORICAL_FIDELITY: the 10.0 constant is engine-byte-confirmed; the tile-datum georef is the SAME open bound as [P3b] (KNOWN-OPEN #5).
- EVIDENCE_STATUS: CONFIRMED (constant) / the naive marker REJECTED (a falsified hypothesis, recorded).
- EVIDENCE: iter031_water_findings.json (2f9bef45...); iter023_terrain_minheight_water.json (314949A8...).
- ERA: PCG_9_3_5 (engine); JUL_2003 (correlation data — counts match iter008b exactly).
- HONEST BOUNDS: the level-in-TILE-datum remains the honest bound (needs the georef pin or runtime capture).

### ROW 15 — WATER_TEXTURE
- **VERDICT: CONFIRMED (payloads + technique references); the plane textures MISSING locally (era-bounded, no proxy as truth)**
- KNOWLEDGE: the Water technique references waves01/02.tga + sky0/1.tga (4 name-referenced textures, 4 WRAP/LINEAR samplers) — the name-registered WAVES_01/02/03 family (type 1000) is NOT in any local container (the 178-container census across 3 corpora) → the page uses synthetic normals ([P-WAVES]) + a synthetic gradient ([P-SKY]); the Water01-05 TILE-MATERIAL textures = TGA2 256×256×24, FOUR-ERA BYTE-IDENTICAL (PCG==JUL==EU==CD, 5/5; Water01 mean RGB 120.6/166.3/162.3 bright cyan-green; Water05 13.4/16.5/42.5 deep blue) — a DISTINCT layer from the plane textures (recorded distinction).
- VALIDATION: the dual-era resolution + decode (iter023); the .fx decode (iter031, byte-faithful); the era byte-identity measured across four corpora.
- HISTORICAL_FIDELITY: the tile-material payloads are original bytes (all eras); the plane textures are honestly MISSING (no fabricated "historical" texture).
- EVIDENCE_STATUS: CONFIRMED (what exists) / MISSING-locally (what does not — labeled).
- EVIDENCE: iter031_water_fx_decode.json (3fbd46ec6078e7ea103144c6c39462ffd2a899b81607e2799250a9e513d75941); iter031_fx_id_0x3eb_Water.hlsl (857dea6e...); iter023_water_container_census.json (5F2907E7...).
- ERA: PCG_9_3_5 + JUL_2003 (+ CD/EU for the byte-identity proof).
- HONEST BOUNDS: the acquisition path for waves/sky textures = a patched-era container or a runtime capture (post-M1 track — recorded, not attempted).

### ROW 16 — WATER_MATERIAL
- **VERDICT: CONFIRMED**
- KNOWLEDGE: the full Water technique material set decoded: 22 uniform defaults; WaterColor (0.1,0.2,0.25); the alpha band [0.6,0.9]; the reflection [0.4,0.9]; the states: SrcAlpha/InvSrcAlpha alpha-blend (ArkAlphaBlendRenderState_Default from 25ArkLight.fx), ZWrite ON, CullMode 1, alpha-test off; 4 WRAP/LINEAR samplers; vs_1_1 + ps_2_0; the wind/scroll/4-phase ops; the manager slots +0x1b4 (terrain shader) / +0x1b8 (water) / +0x1bc (mode); JUL_2003 record 0x3eb BYTE-IDENTICAL to 9.3.5 (same offset/size/SHA — era-stable).
- VALIDATION: the byte-faithful extraction from BOTH eras (SHA 857dea6e... each; the CRLF line-ending translation of the frozen iter024 artifact documented as the only delta).
- HISTORICAL_FIDELITY: carried verbatim into the page constants.
- EVIDENCE_STATUS: CONFIRMED.
- EVIDENCE: iter031_fx_id_0x3eb_Water.hlsl (857dea6e...) + iter031_jul_fx_id_0x3eb_Water.hlsl (857dea6e... — byte-identical); iter031_jul_materials_compare.json (4c4b8d7363a1b1b3d360c66eeac5928803185960537b7d249a9329de91549028).
- ERA: JUL_2003 + PCG_9_3_5 (era-stable, byte-proven).

### ROW 17 — WATER_ANIMATION
- **VERDICT: CONFIRMED (mechanism chain; the env writer open)**
- KNOWLEDGE: g_Time mod 1800 (the .fx 4-phase wind/scroll ops — the page uses the deterministic frame g_Time=300); g_WaterWind = the ARK_WATER_WIND semantic (ArkFXPShared<float> @mgr+0x15c, value @mgr+0x184, disasm-pinned FUN_009512a0 ← FUN_009516f0 PER FRAME: value = 0.5 + clamp(env+0x14, 0, 1) × 1.5 → RANGE [0.5, 2.0]; ARK_WIND = env+0x10) → the vtable bind slots → the .fx g_WaterWind; the auction-UI +0x184 write = a FALSE POSITIVE (honestly dispositioned).
- VALIDATION: the RE chain (fresh project, disasm-pinned stores); the .fx decode (the semantic + the state macro from the original 1Ark.fx/25ArkLight.fx includes — the include-id rule verified over all referenced numbers).
- HISTORICAL_FIDELITY: the page implements the verbatim ops at a deterministic frame (labeled; a live per-frame animation would break the deterministic-hash discipline — the trade-off documented).
- EVIDENCE_STATUS: CONFIRMED.
- EVIDENCE: iter031_water_findings.json (2f9bef45...); iter031_water_fx_decode.json (3fbd46ec...); iter031_materials_vfs_rec0025_25ArkLight.fx (061c1e43ff5daa65b9a9be1e56591f1d3c5145b606792484403f70986f36d7e3).
- ERA: PCG_9_3_5.
- HONEST BOUNDS: the env object's +0x14 water-wind WRITER (EnvironmentZones/ArkScript/server — the last wind link) = KNOWN-OPEN #13.

### ROW 18 — PESOURCE_MOUNT
- **VERDICT: CONFIRMED**
- KNOWLEDGE: the era-aware source/compatibility layer: mountEra (formats BUNT | BNT2 | BNT2_TERRAIN | ARKVFS; KNOWN_HASHES SHA-enforced at mount); enumerate/openResource/getTerrainTile/resolveTexture/getTerrainMaterials/getVegetationClimate; provenance on EVERY resource (era, container, entry, offset, SHA, decoderVersion, evidenceStatus); BUNT_TRAILING_BYTES=8 (the format-layer fix for the trailing-8 zlib junk — 51,921/51,921 corpus-proven); era-validation per ENTRY #3 (Bnt2TerrainArchive VERSIONED for PCG terrain.bnt — the legacy BuntArchive never fed terrain.bnt); NO silent cross-era (era-explicit fallbacks logged + provenance-recorded; NOT_FOUND LOUD); the 9.3.5 type-100 provider set CLOSED (ui.bnt + textures.bnt ONLY; the 12-byte Textures\Terrain.bnt stub = the BNT2 writer's zero-entry output, an install-time ORPHAN — the second-provider hypothesis REJECTED); the BNT2/BUNT reader continuity documented (FUN_00967680 parses both footers).
- IMPLEMENTATION: src/pesource/* in eudoria-clean (BuntArchive, Bnt2Archive, Bnt2TerrainArchive, ArkArchive, TdfDecoder, TdfMaterialTailDecoder, TgaDecoder, VegetationClimateDecoder, TerrainMaterialSet, PESourceMount, PEProvenance) — the Rosetta layer with NO renderer semantics.
- VALIDATION: iter005 the full-map SHA reproduction (3DC16D52... == iter002) + 210/210 chunk byte-equality; iter019 era-validation (58,451 entries, 0 failures, 448,384 tail records); iter010 oracle agreement 175/175 (M3-2-R1 independent pipeline); iter033 the VCL mount (SHA-pinned 7B858401...); the fresh sweep: every page mount re-verified (hashVerified true at runtime).
- HISTORICAL_FIDELITY: the mount reads ORIGINAL era bytes only; every era divergence recorded (heights 773 tiles; Water03 +167; region-B tail divergence), never silently substituted.
- EVIDENCE_STATUS: CONFIRMED.
- EVIDENCE: iter019_era_validation_terrain_bnt.json (D2D13D84...); iter010_id_resolution.json (ECA9B358...); iter033_manifest.json (F299C622... — the runtime file SHAs of the pesource layer).
- ERA: all four (era-explicit per mount).
- HONEST BOUNDS: the JUL-era water/foliage RUNTIME layers carry the loader-absence/era-stability notes per row 7/12 (no runtime bridging claims).

### ROW 19 — RUNTIME_INTEGRATION
- **VERDICT: CONFIRMED (M1-E clean chain proven + FRESH regression sweep 5/5 PASS)**
- KNOWLEDGE/IMPLEMENTATION: the clean chain = ORIGINAL PCG_9_3_5/JUL bytes → PESourceMount → canonical semantic objects (TerrainTile, TerrainMaterialSet, VegetationClimate records, PEFoliageCore, PETerrainCore) → r185 WebGLRenderer pages: heights (p0), materials, materials_wsum (the labeled comparison model), materials_confirmed (the CONFIRMED architecture), era_divergent, water_system, foliage_system — ZERO legacy runtime input (ENTRY #2/#3 satisfied); eudoria-web untouched (FROZEN oracle); THREE_R185_PROJECT_BASELINE = CALIBRATED (gate A-J with per-item artifacts, ledger ITER_019; rules per ENTRY #9: WebGPURenderer excluded, r169 = oracle only).
- VALIDATION: **THE FRESH REGRESSION SWEEP (this session, 03_EVIDENCE\iter034_regression_sweep.json): ALL 5 clean pages reproduce their recorded deterministic hashes EXACTLY on fresh headless-Chromium loads at b7d38ad** — heights 50BD7F9E... MATCH; materials 5F4677E6... MATCH; materials_confirmed 3C785581... MATCH; water_system D7C13F1F... MATCH; foliage A79CB65C... MATCH (76/76 instances, 0 NOT_FOUND, foliageVisible true); every page's in-page double-render determinism true; processes killed + liveness-verified (server PID 10584, chrome PIDs 12264/10252/14656/14248/6024; port 8132 closed; 0 orphans).
- HISTORICAL_FIDELITY: every rendered resource traceable to original bytes (provenance chain); generated GLB/PNG/JSON = CACHE/DEBUG/PREVIEW/REGRESSION only (the foliage GLBs = GENERATED_CACHE, labeled).
- EVIDENCE_STATUS: CONFIRMED (deterministic + reproducible + provenance-complete); the era-bounded placeholders ALL labeled in-page (see PART 3).
- EVIDENCE: iter034_regression_sweep.json (this session) + the five per-page result JSONs in 04_SESSIONs\ITER048_GATEPREP_RUN\logs\iter034_*.json; the frozen page records: iter019_p0_browser_result.json (20CFC413...), iter020_browser_result.json (43AC2739...), iter030_page_result.json (9B62AD33...), iter031_water_findings.json (2f9bef45...), iter033_render_hashes.json (37E0713E...).
- ERA: PCG_9_3_5 (runtime primary) + JUL_2003 (oracle/region byte-identity).
- HONEST BOUNDS: the runtime is REGIONAL (the proven 9-tile regions + the water window) — NO full-map claim; NO model/animation/avatar systems (the single-model witness rule gates those, ENTRY #3/#4); the milestone does NOT pretend the era-bounded inputs are historical (PART 3).

---

## PART 2 — THE FRESH REGRESSION SWEEP (this session; full detail in 03_EVIDENCE\iter034_regression_sweep.json)

| # | Page | Recorded hash (evidence, SHA re-verified) | Fresh hash (this session) | Verdict |
|---|------|-------------------------------------------|---------------------------|---------|
| 1 | heights (terrain/p0.html) | 50BD7F9E4B715DB4972C65B068585696E8FEBC0E360FDABE4E941C6A6EBE33BC (iter019_p0_browser_result.json) | 50BD7F9E4B715DB4972C65B068585696E8FEBC0E360FDABE4E941C6A6EBE33BC | **MATCH** |
| 2 | materials (terrain/materials.html) | 5F4677E6D7EB2EF2DABBAD7D52400A7412C7309E423C6059BFCDB01A22D336EC (iter020_browser_result.json) | 5F4677E6D7EB2EF2DABBAD7D52400A7412C7309E423C6059BFCDB01A22D336EC | **MATCH** |
| 3 | materials_confirmed (terrain/materials_confirmed.html) | 3C7855818B658B03E12132B31E4084A63194AC1F83C6F0568EB92EA886B8318F (iter030_page_result.json) | 3C7855818B658B03E12132B31E4084A63194AC1F83C6F0568EB92EA886B8318F | **MATCH** |
| 4 | water_system (terrain/water_system.html) | D7C13F1F128EEA1C096C6CEC00854D4D77DCD915F0FB219A554278FEBDFE3F44 (iter031_water_findings.json) | D7C13F1F128EEA1C096C6CEC00854D4D77DCD915F0FB219A554278FEBDFE3F44 | **MATCH** |
| 5 | foliage (terrain/foliage_system.html) | A79CB65C1852E8893E1346905D2F29BCBAC0C076D3EA6491AC1E2A7BDD92929F (iter033_render_hashes.json; 5-load determinism + the ?foliage-off visibility proof A3339D4A...) | A79CB65C1852E8893E1346905D2F29BCBAC0C076D3EA6491AC1E2A7BDD92929F | **MATCH** |

- SWEEP VERDICT: **PASS — 5/5 pages, ZERO deltas, ZERO root-cause investigations needed.** The recorded behavioral stats also reproduced: materials_confirmed naive-vs-confirmed whitePct 43.36 vs 0.0; water stats waterTileCount 5, heights 7.3..120.0 m; foliage 76 instances / 4 models / 0 NOT_FOUND / foliageVisible true.
- PROCESS DISCIPLINE: server node.exe PID 10584 (port 8132) spawned + killed + liveness-verified dead; port 8132 closed; five headless-Chromium instances (PIDs 12264, 10252, 14656, 14248, 6024) each killed by the probe + liveness-verified dead after each run; pre-existing node/chrome processes from other sessions NOT touched (identity not provably this session's).
- EXECUTED SCRIPT HASHES (unchanged tools, recorded before execution): server.mjs 43404C17FEEF6BB3E529BFC8917A11B6F09AEA6FD0DFCA7A46E4C653D280B629; tools/cdp_probe.js 7052AE4167442F2EC3D943BEE36505CAD5A6775AC1060015F2DB22FCCE112195; page scripts: p0.js BD019D56..., materials.js A42CE835..., materials_confirmed.js 6CBEAF4F..., water_system.js 92681C80..., foliage_system.js 011473ED... (== the iter033 manifest — tree unchanged).

---

## PART 3 — THE ERA-BOUNDED REGISTRY (consolidated; every placeholder across the pages)

Format: placeholder | what is missing | why (evidence) | what would close it (resume path) | era-honest statement

| Placeholder | Missing | Why (evidence) | Resume path | Era-honest statement |
|---|---|---|---|---|
| **[P1]** (materials_confirmed) | the 65×65 climate byte grid (texture id 432502) | NOT in ANY local container (178-container census across 3 corpora); the client fetch is LOCAL-ONLY and a miss halts init; delivered by the ClientLoader FTP patcher (iter029) | a patcher-updated Textures.bnt of the era, or a runtime capture | the page uses constant byte 0 → palette A[0]=0x66DC6 (a DOCUMENTED choice; the engine default for unmapped bytes is 0x66DC7); NO historical climate-truth claim |
| **[P2]** (materials_confirmed) | the 129×129 detail-selector grids (texture id 459344) | same delivery-channel verdict as P1 (patcher-delivered; tables C/D/E are engine-side but the byte input is not local) | same as P1 | constant byte 0 → the engine tables C[0]=D[0]=458791, E[0]=458792 (the ACTUAL engine table entries for byte 0 — table mechanics CONFIRMED, input bounded) |
| **[P3a]** (materials_confirmed) | the ArkHeightTree leaf recursion | the tree CONSTRUCTION was not RE'd (iter027 bound 1; the leaves carry global-field height samples, no tile linkage — iter028) | the quadtree construction RE | the page preserves the leaf data chain IN FORM (the direct height sample + clamp); the recursion itself is an approximation, labeled |
| **[P3b]** (materials_confirmed) | the cross-era georeferencing (field vs tiles) | UNPINNED: r=0.527 saturation (iter028); the MEASURED contradiction: the field at the engine addressing = −130..−125 m vs the tiles +16..+487 m (iter030 paletteProbe) | the 2010-era local terrain, or runtime tracing | the ROW INPUT uses the TILES' OWN heights (the substitution is backed by the measured contradiction — an honest choice, NOT a historical claim) |
| **[P4]** (materials_confirmed) | the per-session noise-table seeds | the engine seeds the manager RNG per-session (FUN_004058a0/00405920 Java-LCG decompiled, iter030) | runtime RNG capture | FIXED-seed Java-LCG tables — deterministic reconstruction only, not a session-faithful seed |
| **[P5]** (materials_confirmed) | the accumulated leaf roughness at the historical scale | the CONFIRMED 12-slot formula (FUN_00991880 decompiled) evaluated on the tile height grid at the 4-unit sample scale; the historical leaf size/depth rule not pinned | the quadtree RE (same as P3a) | formula CONFIRMED, scale DOCUMENTED — labeled |
| **[P-WAVES]** (water_system) | waves01/02.tga (the plane's wave textures) | name-registered (WAVES_01/02/03, FUN_0048be10, type 1000) NOT in any local container (178-container census) | a patched-era container or runtime capture | SYNTHETIC normals on the page — never claimed historical |
| **[P-SKY]** (water_system) | sky0/1.tga (the reflection textures) | same census negative | same as P-WAVES | SYNTHETIC gradient — never claimed historical |
| **[P-DATUM]** (water_system) | the water level in the TILE datum | the 10.0f constant is in the GLOBAL-FIELD datum (engine-confirmed); the field-vs-tile georef is UNPINNED (same as P3b) | the georef pin (P3b's closer) | the page elevation = a demonstrative control (engine 10.0 field-datum; tile-datum UNPINNED; default 0.0 = the iter023 correlation) — labeled |
| **[P-CLIMATE]** (foliage_system) | the per-location climate selection (which .vcl applies where) | the shared-selector hypothesis PLAUSIBLE-NOT-CONFIRMED (the VCL ids 0..31 vs palette ids DISJOINT; the .vcl fetch id source + type-id constant UNVERIFIED — iter032 bound 1) | the .vcl fetch-id RE + the cell-stream provider RE | DOCUMENTED choice: climate index 0 (0.vcl) — the reconstruction demonstrates the MECHANISM, not the historical placement |
| **[P-CELLSTREAM]** (foliage_system) | the historical cell byte-stream content (the stored {u16,u16,u32} records per cell) | the DataSource/PatchSourceClient abstraction proven but the data origin NOT closed (iter032 bound 3) | the cell-stream provider RE | the local deterministic stand-in (round(col1) count + the placement hash) is RECONSTRUCTION-ONLY — labeled |
| **[P-RNG-DIV]** (foliage_system) | the exact RNG normalization divisor | _DAT_00a7d7a8 reads 0.0 statically (runtime-initialized; FDIV/FLOAD operands only) | runtime tracing (needs separate authorization) | the 32768.0 divisor CANDIDATE — the RNG identity is confirmed, the divisor labeled |
| **[P-RNG-P3]** (foliage_system) | p3 = *(impl+0x24) of the seed | UNVERIFIED (iter033); p2 = the view band 10 STRONGLY_SUPPORTED not byte-pinned | the impl-object RE | p3 = 0 in the reconstruction — labeled |
| **[P-POS-SCALE]** (foliage_system) | the u16→world position divisor | _DAT_00a8c758 reads 0.0 statically (runtime-initialized — iter032 bound 2) | runtime tracing | the 2.0 divisor CANDIDATE — labeled |
| **[P-SCALE-FIELDS]** (foliage_system) | the col2/col3 → scale min/max field mapping | the census reading + the impl+0x40/+0x44 direction STRONGLY_SUPPORTED (not byte-pinned) | the impl-object RE | the mapping is a documented reading of the records — labeled |
| **[P-WINDOW]** (foliage_system) | the historical generation window (grid extents) | the extents are settings-scaled, not statically pinneable (iter032) | the settings-source RE | the window = the proven region — a demonstration window, labeled |
| **[P-UNITS]** (foliage_system + water) | the NIF cm→render-m bridge | the NIF corpus is centimeter-native; the m→cm ×100 engine scale is CONFIRMED (FUN_0082b790) but the GLB cache bridge is a reconstruction convention | the clean pesource NIF path | the 0.01 bridge — labeled CURRENT_RUNTIME_CALIBRATION |
| **[P-MATERIALS]** (foliage_system) | the per-model materials | the per-model materials come from the GENERATED_CACHE GLBs (the export source corpus UNVERIFIED at file level); the 0x3EC technique informs the lighting only | the clean pesource NIF parser (a JS NIF reader over era Models.bnt) | the foliage render = GENERATED_CACHE assets + fixed deterministic lights — an era-bounded approximation, NEVER claimed byte-faithful |
| ROTATION (foliage, not a placeholder — RE-faithful ABSENCE) | the rotation/variant derivation | NOT FOUND in the spawn loop (iter032 bound 5; candidates FUN_0095ae20/FUN_0095b4f0 unread) | the candidate-function RE | identity rotation = the RE-faithful absence, recorded as such |

Era-bounded REGISTRY VERDICT: every placeholder is LABELED IN-PAGE, DOCUMENTED with evidence, and carries NO historical-truth claim — the charter's NO SILENT ERA FALLBACK rule is satisfied end-to-end.

---

## PART 4 — THE KNOWN-OPEN LIST (every UNRESOLVED / PLAUSIBLE-UNVERIFIED item left open, with evidence pointers)

1. **TDF sub-header (52..63) min/max source** — UNRESOLVED. 386/400 sampled tiles read all-zero, 14 nonzero; NO probed encoding carries the per-tile min/max (iter020 P1). Resume: the FUN_0047fb20 min/max RE path.
2. **TDF payload header-xy mismatch** — 0/400 header-xy == filename-xy (consistent; values small ints); semantics UNRESOLVED (iter020 P2; the 65×65 climate-cell candidate was REJECTED — values vary within single cells).
3. **The shared climate selector** (.vcl fetch id source + type-id constant) — UNVERIFIED (iter032 bound 1). The [P-CLIMATE] closer.
4. **The 65×65 climate grid (432502) + 129×129 detail selectors (459344)** — MISSING locally (patcher-delivered; the 178-container census + the local-only fetch + the init-halt gate — iter029). Acquisition = a patcher-updated era container or a runtime capture. [P1]/[P2].
5. **The cross-era georeferencing [P3b]** — UNPINNED (r=0.527 saturation, iter028; the measured −130..−125 m vs +16..+487 m contradiction, iter030). Needs the 2010-era local terrain or runtime tracing.
6. **Special-row tiles (6,530 PCG, y=0xff1a..0xffff)** — structure-censused (dominant 2,386 B payload, ds=2100 dim=32; LOD-skirt candidate) but semantics UNRESOLVED (iter019/020 P3, iter028 specialtiles).
7. **dim=2 record semantics** — TEMPLATE/PARAMETER role CONFIRMED (75.72% the identical (256,227,376,227) template, id=18093; 21 deviant ids); semantics UNRESOLVED (iter009/016; the stale-pointer note in iter031 closes the '227 constant' question).
8. **dim=4 record semantics** — U16-PER-PIXEL structure CONFIRMED (size 84, region 32 B = 16 px × 2 B, id=6 constant); semantic role UNVERIFIED (iter016; type-system records per iter030).
9. **The height-form full-lerp in 9.3.5** — FUN_00989e70 = the clamp-to-65535 sibling; the full lerp form + the min/max source in 9.3.5 itself UNRESOLVED (iter024f). PE2003 FUN_0047fb20 identity+operation CONFIRMED (R2-split per ENTRY #4).
10. **Cross-file skeleton pairing** — OUT OF M1 SCOPE (charter §11); recorded as an M2 lead (the single-model witness + witness-matrix rules gate any model work — ENTRY #3/#4).
11. **The type-2/sub-0 zone scratch reader** — written + cleared + dirty-flagged, NO reader located in the 838-function census (iter030). Resume: the zone-apply vtable owner.
12. **The zone-apply vtable owner** — the ptr scans hit Jython API failures; the object family identified from the mode/grid fields (iter030 honest bound).
13. **The env object's +0x14 water-wind WRITER** — the last wind link (EnvironmentZones/ArkScript/server candidates — iter031 NEXT 1).
14. **'Geowater:0' family consumer + the 0xb7dc gate** — a second name-registered water family, UNRESOLVED (iter031).
15. **The bank[1]/bank[2]/bank[5] consumers** — the 257 G/B float fields + the 65×65 B selector of the world-data bank (candidates: water/min-height) — UNRESOLVED (iter029).
16. **The runtime world-id singleton (id[0])** — per-planet set-swap question UNRESOLVED (iter029).
17. **VCL cols 6-11 semantics** — UNVERIFIED (iter032 bound 4; candidacy only).
18. **The cell byte-stream origin** — the DataSource/PatchSourceClient abstraction proven; the provider NOT closed (iter032 bound 3). The [P-CELLSTREAM] closer.
19. **The rotation/variant derivation** — candidates FUN_0095ae20/FUN_0095b4f0 unread (iter032 bound 5); identity rotation = the RE-faithful absence.
20. **The elevation-band filter rule** — UNVERIFIED; the foliage census MEASURES the bands instead of assuming (62 within / 14 outside — iter033).
21. **The clean pesource NIF path** — the GENERATED_CACHE GLB dependency's replacement (a JS NIF parser over era Models.bnt) — queued future work (iter033 NEXT 2).
22. **The JUL_2003-era terrain material RUNTIME semantics** — the PE2 2003 client = D3D8 fixed-function (era-divergent from the 9.3.5 HLSL Terrain_14); the TMF canon stands as the PE2 reference; the 2003-era blend was NOT re-RE'd (iter024f era table; the era drift = CONTENT never GRAMMAR per iter030).
23. **The JUL-era texture version choice** — 110/175 ids era-stable; for the 61 divergent ids, which version matches JUL_2003 is UNDECIDABLE from bytes (PLAUSIBLE: CD closest in time; UNVERIFIED — iter010/011).
24. **Region-B observations** — Grassmix04 duplicate id (108727 AND 88103, aliasing semantics UNRESOLVED); UNNAMED dim=16 records with 512-byte non-RAW/non-RLE regions (system records, 6/9 tiles — recorded, carried raw by the decoder) — iter021.
25. **The >4-material reduction mechanism** (top-4 pre-bake vs multipass) — UNRESOLVED (iter024/025; C1 top-3 capture measured 93-99%/77-95% vs UB; C2 record-order unreliable) — the 3+1 per-pass cap is source-anchored.
26. **The 2xxxx cross-container resource-id space hypothesis** — PLAUSIBLE, no semantics claimed (iter022: .tez d 20068-20641 + template B-space runs + ArkScript chat slots + 20001..20043.vfs share the numeric family; the d↔B crossing = d 20070 == B(template 1969), 1/7, role UNVERIFIED).
27. **Era divergence census (recorded, not open per se)** — PCG-vs-JUL: heights differ on 773/51,920 tiles; Water03 +167 tiles; region-B tails diverge in the UNNAMED system records (named records era-identical on the sample — iter025); ALL recorded with era provenance, never mixed.

OPEN-LIST VERDICT: NO open item blocks the milestone gate definition (charter §13): PASS does not require pretending unknown historical facts are known; every essential subsystem has a non-arbitrary implementation (the arbitrary-seed scatter is GONE from the clean runtime; the water level is engine-confirmed; the material model is engine-confirmed) — the genuinely-unavailable inputs are era-bounded with explicit labels + resume paths, per the charter's MILESTONE_BLOCKED_WITH_EXHAUSTIVE_NEGATIVE alternative NOT being triggered (all four gates have CONFIRMED local evidence + wired deterministic pages).

---

## PART 5 — EVIDENCE SHA VERIFICATION SUMMARY (build-time, this session)

All evidence files cited in PART 1 were re-hashed on disk this session (the full list: 03_EVIDENCE\iter034_regression_sweep.json .evidenceShaVerification). **ZERO mismatches** vs ledger/manifest-recorded values:
- Ledger-recorded (12 files): iter008b_winning_walk, iter009_mask_semantics, iter010_id_resolution, iter011_payload_classification, iter020_browser_result, iter020_material_decode_audit, iter020_r169_oracle_compare, iter021_browser_load1, iter021_era_byte_audit, iter023_water_container_census, iter023_terrain_minheight_water, iter024_fx_id_0x3ea_Terrain_14.hlsl — ALL MATCH.
- Manifest-recorded: iter030_manifest 5/5, iter031_manifest spot-check 6/6, iter032_manifest spot-check 5/5, iter033_manifest 4/4 evidence + 7/7 repo runtime files — ALL MATCH (the repo tree is UNCHANGED since commit b7d38ad).
- Fresh-recorded (no prior ledger SHA to compare — recorded here as the new pinned values): iter019_p0_browser_result.json 20CFC413..., iter019_p0_byte_audit.json 4C29D220..., iter019_era_validation_terrain_bnt.json D2D13D84..., iter024_blend_op_findings.json BA08FFD6...
- FAILURES: none. (Any SHA that fails re-verification would have been listed here per the gate-prep rules; there were none.)

## PART 6 — SCOPE DISCIPLINE STATEMENT

This iteration was CONSOLIDATION + VERIFICATION ONLY (per the NEXT_PROMPT P0): NO new forensics/RE, NO runtime code changes (eudoria-web + originals READ-ONLY; eudoria-clean tree verified byte-identical to b7d38ad), no new parsers. The one matrix gap that would demand new RE (the [P-CLIMATE]/[P-CELLSTREAM]/georef closers) is documented as KNOWN-OPEN items with resume paths instead of expanding scope.
