#!/usr/bin/env python3
# -*- coding: ascii -*-
# v4_rows_b.py - the composed V4 row data, rows 4-5 (part 2 of 5).
# CARRY rows (current content, rendered with the current verdicts).

ROWS_B = [
 {
  "row": 4, "subsystem": "TERRAIN_MATERIAL_RECORDS",
  "knowledge": "JUL_2003: TDF tail = single size-tagged record sequence [u32 size][u32 dim][size-4 bytes], stride size+4, EXACT consumption 51,920/51,920; 175 distinct material ids (id<->name many-to-many recorded); masks RAW + RLE-(count,value) exact; record order base-first (Stone04 51,521 tiles position-0). PCG_9_3_5: the payload RECONCILED as the serialized MaTerrainMapPatch (the patch serializer FUN_00934970 byte-matches the container framing; the 52/64 offset-space confusion unified); layer TYPE census {0: u16 heights, 2: per-material masks (sub@+16 = the material's TEXTURE id; Stone04=13382), 3: dim-32 masks, 6: sub-id'd per-tile texture-carrier planes (1/tile, dim 2, 18093=87%), 7: u16 normals (computed FUN_009362d0), 9/0xa: system}; THE MASKS DRIVE THE LOD MESH VERTEX-COLOR BAKE + THE ZONE SHADOW PAINT (FUN_00941710/FUN_00940de0/FUN_009402b0) - NOT the base/factor/detail texel source (the exhaustive 838/838 terrain-range consumer census; NO other reader exists).",
  "implementation": "TdfMaterialTailDecoder.js (format layer: named dim=16 records decoded RAW/RLE; system records dim=2/4/8/32/256 carried RAW with UNVERIFIED labels, no interpretation); PESourceMount.getTerrainMaterials (provenance on every object + tailConsumedExactly).",
  "validation": "iter008b corpus exact-consumption; iter020 64/64 records vs an INDEPENDENT DataView-level parser; iter021 era-divergent region 95 records both parsers exact; JUL oracle iter008b tile lists 9/9 sequence match; >4-material tiles rendered AS-IS (the legacy 4-cap = a structural difference recorded, not 'fixed').",
  "historical_fidelity": "record grammar CONFIRMED on original bytes both eras; consumer semantics CONFIRMED at code level for 9.3.5; JUL-era runtime consumer = the Ark11 fallback family + vertex-color bake (era drift is CONTENT never GRAMMAR - iter030).",
  "evidence_status": "CONFIRMED (structure both eras; consumer role CONFIRMED 9.3.5).",
  "era": ["JUL_2003", "PCG_9_3_5"],
  "denominator": "the full-corpus walk (51,920/51,920 exact consumption) + 64/64 records vs the independent parser + the 95-record era-divergent region + the 838/838 consumer census (the iter048-basis validation records; carried content current per the V3).",
  "limitations": "dim=2/dim=4 record SEMANTICS UNRESOLVED (open #7/#8); the type-2/sub-0 zone scratch reader NOT located (open #11); Grassmix04 duplicate-id + unnamed dim=16 512-byte system records recorded (open #24).",
  "evidence": [
   {"file": "iter008b_winning_walk.json", "sha256": "AAFD1A4EB0E459C27C597E5AEF96EEEA4B187F8F40EBA9D7AFA274AADFF80E11"},
   {"file": "iter020_material_decode_audit.json", "sha256": "51898ABC09B15F6711634955928B8DF56FD35B4E2B2E17BDCAEB7543F223F458"},
   {"file": "iter030_findings.json", "sha256": "1104F3186116A98856438741D7F7439E25E6DEF578EAD6D2AA666812B3951207"},
   {"file": "iter030_pcg_tile_census.json", "sha256": "C3EB3C28CBEF2926E2A706F51D437D07C793C10D6A2CA74017FBD49F30E7F071"}
  ]
 },
 {
  "row": 5, "subsystem": "TERRAIN_TEXTURE_RESOLUTION",
  "knowledge": "material record id@+16 -> texture resource: BNT2 entry '<id>.dat' (EU_LATER 175/175; PCG_9_3_5: 8,381 entries, region ids 10/10 + 20/20 same-era, 0 fallbacks); CD_JAN_2003 '<id>.tga' 171/175 (Cabbage_01-03 + Rock02e later-era additions - the era gap REAL, handled explicitly); payload = TGA 2.0 uniform 256x256x24 uncompressed bottom-up (175/175 + 171/171); the 9.3.5 climate system textures: 17 palettes 64x256x32bpp + 79 details 256x256x24 (96/96 manager ids EXIST in PCG Textures.bnt - iter027); the global world-data set: 429259 (257x257 heights, LOCAL both 9.x eras, absent 2003), 432502 (65x65 climate grid, MISSING locally), 459344 (129x129 detail selectors via tables C/D/E, MISSING locally) - the missing two are PATCHER-delivered (ClientLoader = WinInet FTP; the client fetch is LOCAL-ONLY and a miss HALTS init - iter029).",
  "implementation": "PESourceMount.resolveTexture (era-explicit, LOUD NOT_FOUND, provenance era/container/entry/offset/SHA/crossEra) + TgaDecoder (validated TGA2 subset, loud failures); the pages fetch palettes/field/details LIVE with SHA provenance (materials_confirmed bindings: 458791 C551707C..., 458792 A2608374...).",
  "validation": "frozen M3-2-R1 provenance manifest agreement 175/175 (INDEPENDENT pipeline); M3-4 witness-set intersection 0 (disjoint id space - non-circular); iter011 cross-run hash drift 0; four-era byte-identity for the 5 water textures.",
  "historical_fidelity": "every resolved payload is ORIGINAL era bytes, era-labeled; NO silent cross-era (the CD-only 4-id gap recorded, never papered over).",
  "evidence_status": "CONFIRMED (resolution layer, oracle-verified); the world-data grids MISSING/ERA-BOUNDED (patcher-delivered - honest; [P1]/[P2] placeholders; open #4).",
  "era": ["JUL_2003", "PCG_9_3_5", "CD_JAN_2003", "EU_LATER"],
  "denominator": "175/175 manifest agreement + 171/175 CD + 8,381 PCG entries + 96/96 climate textures + the four-era byte-identity (5/5 water textures) (the iter048-basis validation records; carried content current per the V3).",
  "limitations": "the era-correct JUL_2003 texture container DOES NOT EXIST (auditor-verified; both usable corpora CROSS-ERA by construction - tagged per resolution); 110/175 ids era-stable, 61 divergent (which version matches JUL_2003 undecidable from bytes - open #23).",
  "evidence": [
   {"file": "iter010_id_resolution.json", "sha256": "ECA9B3588D99D1FF44CCC880B1EE82A245113DE1EB86357ED715C1F4AAF10D2A"},
   {"file": "iter011_payload_classification.json", "sha256": "86271B9F08BF2057B846C3D21F10E1B0E385E9266575A5B47B4E91BA3BB0C2CE"},
   {"file": "iter030_page_result.json", "sha256": "9B62AD3399F8D1D4E295862D5B065D580D5AB66E7DBA6655DD03FF3F20F8E39B"}
  ]
 }
]
