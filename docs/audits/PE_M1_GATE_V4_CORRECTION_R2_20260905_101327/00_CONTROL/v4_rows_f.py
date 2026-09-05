#!/usr/bin/env python3
# -*- coding: ascii -*-
# v4_rows_f.py - the composed V4 row data, rows 12-15 (part 6 of 7).
# ROW 12 = carry. ROW 13 = carry + the IMPLEMENTATION field composed + labeled
# (the old-matrix MD-format gap). ROW 14 = carry (five fields rendered with the
# current verdicts). ROW 15 = carry + the IMPLEMENTATION field composed + labeled.

ROWS_F = [
 {
  "row": 12, "subsystem": "WATER_SOURCE",
  "knowledge": "NO dedicated water container (0/53 containers, 0/2,217 files in the PCG Data census); the water data = (a) the TDF material tails (Water01-05 layers; exactly 5 water ids both eras, no others); (b) materials.vfs record 0x3eb = the Water technique (JUL_2003 BYTE-IDENTICAL to 9.3.5 - the technique is ERA-STABLE); (c) the client plane builders: WaterPlane01 @0xa97ce0 -> FUN_0093be20 (the no-shader path) / FUN_0093c210 (the shader path, same geometry) -> FUN_0093b4c0 plane create -> FUN_0094a250 (the ArkHeightTree leaf-corner walk; vertices z = param_7; UV = param_6 x scale) -> FUN_007c7140 NiTriShape + FUN_0082b790 scale 100.0; (d) the name-registered texture family WAVES_01/02/03 (FUN_0048be10, type 1000) + sky0/1.tga - NOT in any local container (the 178-container census); (e) MusDef 'DeepWater Theme' = AUDIO ONLY (negative); 'Geowater:0' = a second name-registered water family (FUN_006e8f70, the 0xb7dc gate UNRESOLVED - recorded lead).",
  "implementation": "terrain/water_system.html+js - the ground terrain UNDER a separate water surface over the proven water window (grid 56-59 x 107-110; 5/16 tiles carry Water02=9088; water-tile heights 7.3..120 m) - the charter Gate D architecture.",
  "validation": "iter023 exhaustive container/string census (denominators explicit); iter031 dual-era byte-extraction of the technique (SHA 857dea6e... BOTH eras); the fresh sweep hash MATCH.",
  "historical_fidelity": "all constants carried VERBATIM from the byte-faithful .fx; the non-local textures honestly bounded ([P-WAVES]/[P-SKY]).",
  "evidence_status": "CONFIRMED.",
  "era": ["JUL_2003", "PCG_9_3_5"],
  "denominator": "the 53-container / 2,217-file census + the dual-era byte-extraction (SHA-equal both eras) (the iter048-basis validation records; carried content current per the V3).",
  "limitations": "the env object's +0x14 water-wind WRITER open (open #13); the 'Geowater:0' family (open #14); the type-6 2x2 mask + 20-byte tail semantics (no consumer located).",
  "evidence": [
   {"file": "iter023_water_container_census.json", "sha256": "5F2907E7777C2E18C84ED5C3A7A0CCA2FA49AB05E95D6AF3EE1660FFDFE707E2"},
   {"file": "iter031_water_findings.json", "sha256": "2F9BEF450E74E49886AF958B573F98C6E2C465D368F203587F6FCC82269C9EB8"},
   {"file": "iter031_fx_id_0x3eb_Water.hlsl", "sha256": "857DEA6EB601CDD130B0A1FA2FF1A38B419CAD7CB94A46521377E173B6449F5F"}
  ]
 },
 {
  "row": 13, "subsystem": "WATER_REGIONS",
  "knowledge": "the 5 water materials form COHERENT lake/ocean-shaped 4-connected components (largest 3,805-tile spanning the coastal ring; Water01: 667/307/302/279-tile components); PCG 5,690 / JUL 5,523 water tiles of 51,920 (each id once per tile; Water03 era divergence +167 tiles PCG - recorded); the plane spawn = per material-driver RB-tree tile node (FUN_0093f800 third loop @0x0093ff23: obj[0]==0 -> FUN_0093d7d0 region from obj+9 tile grid coords -> plane stored INTO obj[0]); the type-6 layer = a per-tile TEXTURE-CARRIER (ALL mean-RGB ~120 neutral gray; present on 46,218 dry tiles too) - the water-plane-candidate hypothesis REJECTED-as-primary (presence does NOT discriminate water); the 12 no-type-6 tiles = era-stable high dry ground.",
  "implementation": "the water page renders the water-window region from the SAME tile data (grid 56-59 x 107-110; 5/16 tiles carry Water02=9088) - composed in V4 from the old matrix json row 13 + row 12's implementation records (the old-matrix MD-format gap).",
  "validation": "the full-corpus dual-era walk 0 failures; JUL counts == the frozen iter008b census EXACTLY (independent re-derivation); the consumer RE (FUN_00934890 -> FUN_00953340 inside the LOD ring builder).",
  "historical_fidelity": "the regions are ORIGINAL DATA (both eras); the plane model is engine-confirmed.",
  "evidence_status": "CONFIRMED (data-level coherent regions + the RE plane-per-tile-node spawn).",
  "era": ["JUL_2003", "PCG_9_3_5"],
  "denominator": "the full-corpus dual-era walk (51,920 tiles; PCG 5,690 / JUL 5,523 water tiles) + the component census (the iter048-basis validation records; carried content current per the V3).",
  "limitations": "none beyond the type-6 semantics note (the per-tile texture-carrier role; the water-plane-candidate hypothesis REJECTED-as-primary).",
  "evidence": [
   {"file": "iter023_terrain_minheight_water.json", "sha256": "314949A88AA8B8670E9555977B73F584FDDD343F6BA85F463AC54E276DDEA097"},
   {"file": "iter031_type6_census.json", "sha256": "8D62122D9A6761F9B95303C959F286A7870515C0CCE1A32473C33AD466131322"},
   {"file": "iter031_water_findings.json", "sha256": "2F9BEF450E74E49886AF958B573F98C6E2C465D368F203587F6FCC82269C9EB8"}
  ]
 },
 {
  "row": 14, "subsystem": "WATER_LEVEL",
  "knowledge": "THE WATER LEVEL = 10.0f HARDCODED (_DAT_00a7b128 = bytes 00 00 20 41): the plane vertices read z = param_7 = 10.0 (FUN_0094a250); the underwater test FUN_00853a80(x,y) < 10.0 (FUN_0048bff0); the UNIT-CONSISTENCY TRIANGLE: m->cm x100 (FUN_0093b4c0/FUN_0082b790) + the Terrain_14 WATER_LIGHT window [-5,+10] m (full light AT the water level, full dark 15 m below) - three independent code paths agreeing; the naive 'raw u16 height==0 = water marker' REFUTED at data level (the dominant zero component spans the ENTIRE map - 23,760/24,363 tiles; 82% of zero tiles carry no water; 1,362 water tiles contain no zero sample); water materials CONCENTRATE at tile-min 0 (median 0 vs global 768) - an OBSERVED CORRELATION, not semantic proof.",
  "implementation": "the water page carries the level as a demonstrative control ([P-DATUM]: engine 10.0 in the FIELD datum; the TILE-datum mapping UNPINNED; page default 0.0 = the iter023 correlation - all labeled in-page).",
  "validation": "iter023 the hypothesis test (explicit crosstab over 51,920 tiles: zero&water 4,328 / zero-only 20,035 / water-only 1,362 / neither 26,195); iter031 the RE triangle.",
  "historical_fidelity": "the 10.0 constant is engine-byte-confirmed; the tile-datum georef is the SAME open bound as [P3b] (open #5).",
  "evidence_status": "CONFIRMED (engine constant 10.0f) - the field-vs-tile georef UNPINNED ([P-DATUM] OPEN); the naive zero-marker REJECTED (a falsified hypothesis, recorded).",
  "era": ["PCG_9_3_5", "JUL_2003"],
  "denominator": "the crosstab over 51,920 tiles (4,328/20,035/1,362/26,195) + the RE triangle (the iter048-basis validation records; carried content current per the V3).",
  "limitations": "the level-in-TILE-datum remains the honest bound (open #5; needs the georef pin or a runtime capture).",
  "evidence": [
   {"file": "iter031_water_findings.json", "sha256": "2F9BEF450E74E49886AF958B573F98C6E2C465D368F203587F6FCC82269C9EB8"},
   {"file": "iter023_terrain_minheight_water.json", "sha256": "314949A88AA8B8670E9555977B73F584FDDD343F6BA85F463AC54E276DDEA097"}
  ]
 },
 {
  "row": 15, "subsystem": "WATER_TEXTURE",
  "knowledge": "the Water technique references waves01/02.tga + sky0/1.tga (4 name-referenced textures, 4 WRAP/LINEAR samplers) - the name-registered WAVES_01/02/03 family (type 1000) is NOT in any local container (the 178-container census across 3 corpora) -> the page uses synthetic normals ([P-WAVES]) + a synthetic gradient ([P-SKY]); the Water01-05 TILE-MATERIAL textures = TGA2 256x256x24, FOUR-ERA BYTE-IDENTICAL (PCG==JUL==EU==CD, 5/5; Water01 mean RGB 120.6/166.3/162.3 bright cyan-green; Water05 13.4/16.5/42.5 deep blue) - a DISTINCT layer from the plane textures (recorded distinction).",
  "implementation": "the water page uses SYNTHETIC normals ([P-WAVES]) + a SYNTHETIC gradient ([P-SKY]) for the missing plane textures (labeled, never claimed historical); the Water01-05 tile-material textures resolve + decode byte-identically across eras - composed in V4 from the old matrix json row 15 + the registry [P-WAVES]/[P-SKY] records (the old-matrix MD-format gap).",
  "validation": "the dual-era resolution + decode (iter023); the .fx decode (iter031, byte-faithful); the four-era byte-identity measured across four corpora.",
  "historical_fidelity": "the tile-material payloads are original bytes (all eras); the plane textures are honestly MISSING (no fabricated 'historical' texture).",
  "evidence_status": "CONFIRMED (payloads + technique references); the plane textures MISSING locally (era-bounded, no proxy as truth).",
  "era": ["PCG_9_3_5", "JUL_2003", "CD_JAN_2003", "EU_LATER"],
  "denominator": "the dual-era resolution + decode (Water01-05) + the four-era byte-identity (5/5) + the .fx decode (the iter048-basis validation records; carried content current per the V3).",
  "limitations": "the waves/sky acquisition path = a patched-era container or a runtime capture (post-M1 track - recorded, not attempted).",
  "evidence": [
   {"file": "iter031_water_fx_decode.json", "sha256": "3FBD46EC6078E7EA103144C6C39462FFD2A899B81607E2799250A9E513D75941"},
   {"file": "iter031_fx_id_0x3eb_Water.hlsl", "sha256": "857DEA6EB601CDD130B0A1FA2FF1A38B419CAD7CB94A46521377E173B6449F5F"},
   {"file": "iter023_water_container_census.json", "sha256": "5F2907E7777C2E18C84ED5C3A7A0CCA2FA49AB05E95D6AF3EE1660FFDFE707E2"}
  ]
 }
]
