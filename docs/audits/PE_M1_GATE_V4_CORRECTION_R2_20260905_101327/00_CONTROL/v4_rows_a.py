#!/usr/bin/env python3
# -*- coding: ascii -*-
# v4_rows_a.py - the composed V4 row data, rows 1-3 (part 1 of 5).
# Composition sources (all pinned + read-only): the V3 matrix (current verdicts,
# deltas, denominators, honest bounds), the frozen old matrix (carry rows only),
# the amendment records, the repair-run evidence JSONs, this run's
# pc24_synthetic_measurement.json. Rows 1-3 are CARRY rows (current content,
# rendered with the current verdicts).

ROWS_A = [
 {
  "row": 1, "subsystem": "TERRAIN_HEIGHT",
  "knowledge": "JUL_2003: TDF payload heights = 32x32 uint16 LE at payload offset 64 (52-byte header + 12-byte sub-header; the two offset spaces NEVER collapsed); PCG_9_3_5: PE2003 client decode FUN_0047fb20 = min + (max-min)*u16/65535 (per-tile min/max lerp - identity + observed operation CONFIRMED at VA; the 9.3.5 sibling FUN_00989e70 = square-u16-grid scale-by-float CLAMP-to-65535).",
  "implementation": "clean chain = terrain.bnt/50.bnt bytes -> PESourceMount (BNT2_TERRAIN/BUNT, BUNT_TRAILING_BYTES=8) -> TerrainTile (provenance per tile) -> PETerrainCore (height = u16 x 1/128 m, CURRENT_RUNTIME_CALIBRATION; disjoint-tile borders kept AS ORIGINAL DATA, no repair).",
  "validation": "9/9 region tiles byte-faithful vs an INDEPENDENT second parser (tools/p0_byte_audit.js); 9216/9216 samples IDENTICAL vs the frozen r169 oracle chunk (built from JUL-identical source tiles); JUL full-map rebuild SHA 3DC16D52... == audit-accepted iter002 (ledger ITER_005); sentinel 7ffe7ffe.tdf EXPLICIT_NOT_ASSEMBLED.",
  "historical_fidelity": "heights byte-exact from ORIGINAL bytes (both eras; 773/51,920 PCG-vs-JUL tiles differ in heights - era divergence recorded, never mixed).",
  "evidence_status": "CONFIRMED (structure/bytes); engine height-form: identity+operation CONFIRMED, final role STRONGLY_SUPPORTED (heightScale 128 u16/m = STRONGLY_SUPPORTED runtime calibration, not an engine-extracted constant).",
  "era": ["JUL_2003", "PCG_9_3_5"],
  "denominator": "9/9 region tiles + 9216/9216 samples + the full-map SHA reproduction (the iter048-basis validation records; carried content current per the V3).",
  "limitations": "per-tile min/max SOURCE UNRESOLVED (sub-header zero on 386/400 sampled; identity lerp used); full-lerp form in 9.3.5 itself UNRESOLVED (open #9).",
  "evidence": [
   {"file": "iter019_p0_browser_result.json", "sha256": "20CFC413E530E3F7C67760E884977F23970EEA6167E75E6159FEFE5CA8EC3FC9"},
   {"file": "iter019_p0_byte_audit.json", "sha256": "4C29D22071E3E9CACD4744329B985EA534CFF1558C93F761AD1A8E89B2EF7A6B"},
   {"file": "iter019_era_validation_terrain_bnt.json", "sha256": "D2D13D84558E337D8A3B8CA14DAFA8240A8B4A4B4B97AFA470F707141183F1DD"}
  ]
 },
 {
  "row": 2, "subsystem": "TERRAIN_GRID",
  "knowledge": "JUL_2003: BUNT footer filename-xy grid 220x236 = 51,920 regular + 1 sentinel (7ffe7ffe.tdf); PCG_9_3_5: BNT2 footer, 58,451 entries = 51,920 regular (SAME filename-xy convention) + 6,530 special-row (y=0xff1a..0xffff) + sentinel; tile world size = 128 units (from the >>7 math, engine-confirmed iter030).",
  "implementation": "PESourceMount era-validated VERSIONED decoders (BuntArchive JUL / Bnt2TerrainArchive PCG - never one interpretation forced across eras); the sentinel handled explicitly.",
  "validation": "iter019 era-validation 0 walk failures (58,451 entries); iter008b full-corpus walk exact consumption 51,920/51,920; denominator checks 7040x7552 in-browser (ledger ITER_005 r2).",
  "historical_fidelity": "the grid is decoded from ORIGINAL container bytes both eras (BUNT JUL / BNT2 PCG, the same filename-xy convention); the 6,530 PCG special-row tiles are carried as RECORDED STRUCTURE ONLY (structure-censused; no semantics claimed) - composed in V4 from the old matrix json row 2 + the row's era records (the old-matrix MD-format gap).",
  "evidence_status": "CONFIRMED.",
  "era": ["JUL_2003", "PCG_9_3_5"],
  "denominator": "51,920/51,920 exact-consumption walk + the 58,451-entry era-validation (0 failures) + the 7040x7552 denominator checks (the iter048-basis validation records; carried content current per the V3).",
  "limitations": "6,530 special-row tiles structure-censused only; semantics UNRESOLVED (open #6).",
  "evidence": [
   {"file": "iter008b_winning_walk.json", "sha256": "AAFD1A4EB0E459C27C597E5AEF96EEEA4B187F8F40EBA9D7AFA274AADFF80E11"},
   {"file": "iter019_era_validation_terrain_bnt.json", "sha256": "D2D13D84558E337D8A3B8CA14DAFA8240A8B4A4B4B97AFA470F707141183F1DD"},
   {"file": "iter030_findings.json", "sha256": "1104F3186116A98856438741D7F7439E25E6DEF578EAD6D2AA666812B3951207"}
  ]
 },
 {
  "row": 3, "subsystem": "TERRAIN_WORLD_TRANSFORM",
  "knowledge": "engine world = 131,072 units (ArkHeightTree root size key 65,536 half - iter028, vtable-proven); tile = 128 world units (>>7 math - iter030); m->cm x100 (FUN_0082b790 - iter031); the height field covers the FULL world at 512-unit texels origin -65,536 (FUN_009478e0 - iter029); climate/detail grids cover the CENTER 65,536-unit region (origin -32,768).",
  "implementation": "clean pages render REGIONS: per-tile meshes at TILE_WORLD=128 on a local grid; no global-world placement claim made; cm->m bridge 0.01 labeled [P-UNITS] (the foliage page).",
  "validation": "deterministic renders + the heights oracle (rows 1-2); the engine constants address-cited (iter028/029/030/031 decompiles).",
  "historical_fidelity": "the tile/world sizes are ENGINE-CONFIRMED; the runtime's regional placement is explicitly a reconstruction window ([P-WINDOW]), not a claimed historical world positioning.",
  "evidence_status": "STRONGLY_SUPPORTED (engine facts CONFIRMED; the clean pages' global georef intentionally NOT claimed); the cross-era FIELD-vs-TILE georeferencing UNPINNED (r 0.527 saturation - iter028; the measured contradiction: field at engine addressing -130..-125 m vs tiles +16..+487 m - iter030).",
  "era": ["PCG_9_3_5", "JUL_2003"],
  "denominator": "the deterministic renders + the heights oracle (rows 1-2) + the address-cited engine constants (the iter028/029/030/031 decompiles; carried content current per the V3).",
  "limitations": "[P3b] the row-input substitution on the materials_confirmed page is backed by a MEASURED contradiction, not a silent choice; the georef pin is a KNOWN-OPEN (#5) that needs the 2010-era local terrain or runtime tracing.",
  "evidence": [
   {"file": "iter030_findings.json", "sha256": "1104F3186116A98856438741D7F7439E25E6DEF578EAD6D2AA666812B3951207"},
   {"file": "iter031_water_findings.json", "sha256": "2F9BEF450E74E49886AF958B573F98C6E2C465D368F203587F6FCC82269C9EB8"},
   {"file": "iter030_page_result.json", "sha256": "9B62AD3399F8D1D4E295862D5B065D580D5AB66E7DBA6655DD03FF3F20F8E39B"}
  ]
 }
]
