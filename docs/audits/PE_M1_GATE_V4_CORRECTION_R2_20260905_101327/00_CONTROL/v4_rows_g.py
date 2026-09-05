#!/usr/bin/env python3
# -*- coding: ascii -*-
# v4_rows_g.py - the composed V4 row data, rows 16-19 (part 7 of 7).
# ROW 16/17 = carry + the IMPLEMENTATION fields composed + labeled (the
# old-matrix MD-format gaps). ROW 18 = carry. ROW 19 = NO-COPY SET: composed
# from the current evidence (the V3 delta + the correction-series hash
# supersessions + the offline re-checks) - NOT carried from ITER_048; the
# old-matrix merged KNOWLEDGE/IMPLEMENTATION gap is SPLIT here.

ROWS_G = [
 {
  "row": 16, "subsystem": "WATER_MATERIAL",
  "knowledge": "the full Water technique material set decoded: 22 uniform defaults; WaterColor (0.1,0.2,0.25); the alpha band [0.6,0.9]; the reflection [0.4,0.9]; the states: SrcAlpha/InvSrcAlpha alpha-blend (ArkAlphaBlendRenderState_Default from 25ArkLight.fx), ZWrite ON, CullMode 1, alpha-test off; 4 WRAP/LINEAR samplers; vs_1_1 + ps_2_0; the wind/scroll/4-phase ops; the manager slots +0x1b4 (terrain shader) / +0x1b8 (water) / +0x1bc (mode); JUL_2003 record 0x3eb BYTE-IDENTICAL to 9.3.5 (same offset/size/SHA - era-stable).",
  "implementation": "the technique constants carried VERBATIM into the water page constants - composed in V4 from the old matrix json row 16 + the row's validation records (the old-matrix MD-format gap).",
  "validation": "the byte-faithful extraction from BOTH eras (SHA 857dea6e... each; the frozen iter024 artifact's CRLF translation documented as the only delta).",
  "historical_fidelity": "verbatim original technique constants (era-stable, byte-proven both eras).",
  "evidence_status": "CONFIRMED.",
  "era": ["JUL_2003", "PCG_9_3_5"],
  "denominator": "the byte-faithful extraction from BOTH eras (SHA 857dea6e... each) + the JUL-vs-9.3.5 record comparison (the iter048-basis validation records; carried content current per the V3).",
  "limitations": "none beyond the technique-level notes.",
  "evidence": [
   {"file": "iter031_fx_id_0x3eb_Water.hlsl", "sha256": "857DEA6EB601CDD130B0A1FA2FF1A38B419CAD7CB94A46521377E173B6449F5F"},
   {"file": "iter031_jul_fx_id_0x3eb_Water.hlsl", "sha256": "857DEA6EB601CDD130B0A1FA2FF1A38B419CAD7CB94A46521377E173B6449F5F"},
   {"file": "iter031_jul_materials_compare.json", "sha256": "4C4B8D7363A1B1B3D360C66EEAC5928803185960537B7D249A9329DE91549028"}
  ]
 },
 {
  "row": 17, "subsystem": "WATER_ANIMATION",
  "knowledge": "g_Time mod 1800 (the .fx 4-phase wind/scroll ops - the page uses the deterministic frame g_Time=300); g_WaterWind = the ARK_WATER_WIND semantic (ArkFXPShared<float> @mgr+0x15c, value @mgr+0x184, disasm-pinned FUN_009512a0 <- FUN_009516f0 PER FRAME: value = 0.5 + clamp(env+0x14, 0, 1) x 1.5 -> RANGE [0.5, 2.0]; ARK_WIND = env+0x10) -> the vtable bind slots -> the .fx g_WaterWind; the auction-UI +0x184 write = a FALSE POSITIVE (honestly dispositioned).",
  "implementation": "the page implements the verbatim wind/scroll/4-phase ops at the deterministic frame 300 (labeled; a live per-frame animation would break the deterministic-hash discipline - the trade-off documented) - composed in V4 from the old matrix json row 17 (the old-matrix MD-format gap).",
  "validation": "the RE chain (fresh project, disasm-pinned stores); the .fx semantic + the state macro from the original 1Ark.fx/25ArkLight.fx includes (the include-id rule verified over all referenced numbers).",
  "historical_fidelity": "the ops are verbatim; the frame choice = the reconstruction determinism discipline (labeled, not a historical claim).",
  "evidence_status": "CONFIRMED (mechanism chain; the env writer open).",
  "era": ["PCG_9_3_5"],
  "denominator": "the RE chain (disasm-pinned stores) + the .fx decode + the include-id rule verified over all referenced numbers (the iter048-basis validation records; carried content current per the V3).",
  "limitations": "the env object's +0x14 water-wind WRITER (EnvironmentZones/ArkScript/server - the last wind link) = open #13.",
  "evidence": [
   {"file": "iter031_water_findings.json", "sha256": "2F9BEF450E74E49886AF958B573F98C6E2C465D368F203587F6FCC82269C9EB8"},
   {"file": "iter031_water_fx_decode.json", "sha256": "3FBD46EC6078E7EA103144C6C39462FFD2A899B81607E2799250A9E513D75941"},
   {"file": "iter031_materials_vfs_rec0025_25ArkLight.fx", "sha256": "061C1E43FF5DAA65B9A9BE1E56591F1D3C5145B606792484403F70986F36D7E3"}
  ]
 },
 {
  "row": 18, "subsystem": "PESOURCE_MOUNT",
  "knowledge": "the era-aware source/compatibility layer: mountEra (formats BUNT | BNT2 | BNT2_TERRAIN | ARKVFS; KNOWN_HASHES SHA-enforced at mount); enumerate/openResource/getTerrainTile/resolveTexture/getTerrainMaterials/getVegetationClimate; provenance on EVERY resource (era, container, entry, offset, SHA, decoderVersion, evidenceStatus); BUNT_TRAILING_BYTES=8 (the format-layer fix for the trailing-8 zlib junk - 51,921/51,921 corpus-proven); era-validation per ledger ENTRY #3 (Bnt2TerrainArchive VERSIONED for PCG terrain.bnt - the legacy BuntArchive never fed terrain.bnt); NO silent cross-era (era-explicit fallbacks logged + provenance-recorded; NOT_FOUND LOUD); the 9.3.5 type-100 provider set CLOSED (ui.bnt + textures.bnt ONLY; the 12-byte Textures\\Terrain.bnt stub = the BNT2 writer's zero-entry output, an install-time ORPHAN - the second-provider hypothesis REJECTED); the BNT2/BUNT reader continuity documented (FUN_00967680 parses both footers).",
  "implementation": "src/pesource/* in eudoria-clean (BuntArchive, Bnt2Archive, Bnt2TerrainArchive, ArkArchive, TdfDecoder, TdfMaterialTailDecoder, TgaDecoder, VegetationClimateDecoder, TerrainMaterialSet, PESourceMount, PEProvenance) - the Rosetta layer with NO renderer semantics.",
  "validation": "iter005 the full-map SHA reproduction (3DC16D52... == iter002) + 210/210 chunk byte-equality; iter019 era-validation (58,451 entries, 0 failures, 448,384 tail records); iter010 oracle agreement 175/175 (M3-2-R1 independent pipeline); iter033 the VCL mount (SHA-pinned 7B858401...); the fresh sweep: every page mount re-verified (hashVerified true at runtime).",
  "historical_fidelity": "the mount reads ORIGINAL era bytes only; every era divergence recorded (heights 773 tiles; Water03 +167; region-B tail divergence), never silently substituted.",
  "evidence_status": "CONFIRMED.",
  "era": ["all four - era-explicit per mount"],
  "denominator": "the full-map SHA reproduction + 210/210 chunks + the 58,451-entry era-validation (0 failures, 448,384 tail records) + the 175/175 oracle agreement + the fresh page-mount re-verification (the iter048-basis validation records; carried content current per the V3).",
  "limitations": "the JUL-era water/foliage RUNTIME layers carry the loader-absence/era-stability notes per rows 7/12 (no runtime bridging claims).",
  "evidence": [
   {"file": "iter019_era_validation_terrain_bnt.json", "sha256": "D2D13D84558E337D8A3B8CA14DAFA8240A8B4A4B4B97AFA470F707141183F1DD"},
   {"file": "iter010_id_resolution.json", "sha256": "ECA9B3588D99D1FF44CCC880B1EE82A245113DE1EB86357ED715C1F4AAF10D2A"},
   {"file": "iter033_manifest.json", "sha256": "DD59815206F35E795B6A9E6BE6A89C053DF17B9DF696CAB9658D0026179BBFAA"}
  ]
 },
 {
  "row": 19, "subsystem": "RUNTIME_INTEGRATION",
  "knowledge": "composed in V4 from the current evidence (the V3 delta + the old matrix json row 19, the merged-field gap split; NOT carried as a merged field). the clean chain = ORIGINAL PCG_9_3_5/JUL bytes -> PESourceMount -> canonical semantic objects (TerrainTile, TerrainMaterialSet, VegetationClimate records, PEFoliageCore, PETerrainCore) -> r185 WebGLRenderer pages: heights (p0), materials, materials_wsum (the labeled comparison model), materials_confirmed (the CONFIRMED architecture), era_divergent, water_system, foliage_system - ZERO legacy runtime input; eudoria-web FROZEN oracle; THREE_R185_PROJECT_BASELINE CALIBRATED.",
  "implementation": "composed in V4 from the current evidence: 7 deterministic clean pages (the generated GLB/PNG/JSON = CACHE/DEBUG/PREVIEW/REGRESSION only; the foliage GLBs = GENERATED_CACHE labeled) + the witness page (iter037) integrating the original-direct chain for the single model; the CURRENT deterministic hashes after the correction series: materials_confirmed EA4411B5... (supersedes 3C785581...; delta root-caused = the draw-construction correction shifts every table entry), foliage 8770AAA0... (supersedes A79CB65C...; delta root-caused = the /32767 rand01 shift + the f32 roundings; the ?foliage-off control A3339D4A... UNCHANGED - the terrain path contributed ZERO delta), heights 50BD7F9E... / materials 5F4677E6... / water D7C13F1F... UNCHANGED; the witness page 381A80C4... + the ?model-off control 2084DB5A... DIFFERS.",
  "validation": "composed in V4 from the current evidence: THE REGRESSION SWEEP (iter034): ALL 5 clean pages reproduce their recorded deterministic hashes EXACTLY on fresh headless-Chromium loads (5/5 MATCH) - behavioral stats reproduced (whitePct 43.36 vs 0.0; waterTileCount 5, 7.3..120.0 m; foliage 76/76, 0 NOT_FOUND, visible); processes killed + liveness-verified; the correction-run re-render re-validated the pages deterministically (materials_confirmed EA4411B5 3/3 loads; foliage 8770AAA0 3/3 loads - the iter035 records); THIS V4-correction run did NOT re-render (offline re-checks only, per the mandate) - the 76/2048/16 recorded results RE-VERIFIED bit-exact with the repaired method (offline_rechecks.json): foliage 76/76 rng-state/scale bit-exact (constants byte-derived from the EXE), noise 2048/2048 bit-exact, witness 16/16 strict.",
  "historical_fidelity": "composed in V4 from the current evidence: every rendered resource traceable to original bytes (the provenance chain); the regression is vs OUR OWN recorded runtime - the ORIGINAL-CLIENT visual parity NOT claimed (a server/original-client comparison is post-M1, human-gated).",
  "evidence_status": "CONFIRMED for the audited scope (the clean chain + the deterministic regression vs OUR OWN recorded runtime) - the ORIGINAL-CLIENT visual parity NOT claimed.",
  "era": ["PCG_9_3_5", "JUL_2003"],
  "denominator": "the recorded regression hashes (5 pages) + the offline re-checks (76/2048/16) (the V3 denominator, current).",
  "limitations": "REGIONAL runtime (the proven 9-tile regions + the water window) - NO full-map claim; NO model/animation/avatar systems beyond the single-model witness (the witness-matrix rule gates them, ledger ENTRY #3/#4); the era-bounded inputs never claimed historical (see the registry); the ORIGINAL-CLIENT parity + the WITNESS MATRIX stay OPEN.",
  "evidence": [
   {"file": "iter034_regression_sweep.json", "sha256": "SEE 03_EVIDENCE (written at the iter034 session; recorded in the frozen matrix PART 2)"},
   {"file": "iter019_p0_browser_result.json", "sha256": "20CFC413E530E3F7C67760E884977F23970EEA6167E75E6159FEFE5CA8EC3FC9"},
   {"file": "iter020_browser_result.json", "sha256": "43AC2739BBBBC9282874B782D3AF79CF88761CB61E032E3549812C8A0D60370D"},
   {"file": "iter030_page_result.json", "sha256": "9B62AD3399F8D1D4E295862D5B065D580D5AB66E7DBA6655DD03FF3F20F8E39B"},
   {"file": "iter031_water_findings.json", "sha256": "2F9BEF450E74E49886AF958B573F98C6E2C465D368F203587F6FCC82269C9EB8"},
   {"file": "iter033_render_hashes.json", "sha256": "37E0713EBBEC2C7DB61B0F3C01F674EB0CA751CB7A595E927F80B528C536D3BD"},
   {"file": "offline_rechecks.json (repair run 01_RAW)", "sha256": "C80E65D62147E8DED2DE9C3D8EE028DE14BF619CB80C69BE71D30C8F0DEB4E32"}
  ]
 }
]
