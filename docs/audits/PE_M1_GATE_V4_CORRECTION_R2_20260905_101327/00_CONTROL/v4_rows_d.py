#!/usr/bin/env python3
# -*- coding: ascii -*-
# v4_rows_d.py - the composed V4 row data, rows 8-9 (part 4 of 5).
# ROW 8 = NO-COPY SET: composed per W6 - the SINGLE ORIGINAL-DIRECT WITNESS
# separated from the STILL-OPEN full clean-NIF path + witness matrix +
# scrambled-texture falsification. ROW 9 = carry row.

ROWS_D = [
 {
  "row": 8, "subsystem": "FOLIAGE_MODEL_BINDING",
  "knowledge": "composed in V4 from the current evidence (the iter037 witness records + the iter032 mechanism; NOT carried from the ITER_048 matrix). the instance's node+0x19 u32 id -> GetModel (type-0x66 fetch: FUN_006c9700/00415670/00823c10 -> the 0x14 ArkVegetationModelClient); VCL col0 = the model id source; the model-space ids = the Models container ids (the mechanism CONFIRMED at code level, iter032); THE ERA TEXTURE BINDING = THE ARK SYSTEM: NiArkTextureExtraData (0/10 climate-0 candidate models contain NiSourceTexture - a TEN-CANDIDATE census fact, iter037), NOT an era-wide claim.",
  "implementation": "composed in V4 from the current evidence (W6 - the witness separated from the still-open full path). THE SINGLE ORIGINAL-DIRECT WITNESS (iter037): Models.bnt entry 457485 (payload offset 315186289, payload SHA 72479A7F...) -> NIF v10.1.0.0 -> NiTriShape -> NiArkTextureExtraData 457490 (texture entry offset 389949379, payloadSize 262188, payload SHA 8D76027C...) -> TGA2 -> deterministic render - the chain PROVEN ORIGINAL-DIRECT for ONE model + ONE texture. The foliage PAGE still binds the 10 climate-0 col0 ids to the DEPLOYED legacy GLB corpus (assets/foliage_glb/ + MANIFEST.json, GENERATED_CACHE class, per-file SHA256 verified at load, NOT_FOUND LOUD, 0 misses). The FULL clean pesource NIF path (the GENERATED_CACHE replacement beyond the witness), the WITNESS MATRIX, and the scrambled-texture FALSIFICATION are the STILL-OPEN closers - recorded as OPEN, no unbounded wording.",
  "validation": "composed in V4 from the current evidence: the witness re-checked STRICTLY under the repaired gates: 16/16 blocks (the index compared AS A FIELD), payloadSize 262188 present == own BNT2 read == the oracle, payload SHAs equal - 0 mismatches (offline_rechecks.json witness_16 + fail_closed_gates witness_clean PASS with 5/5 mutations FAIL); 10/10 col0 ids resolved in the GLB cache; the fresh sweep reproduced 76/76 rendered, 0 NOT_FOUND; the witness page cross-validated vs the frozen R61 python parser (575 leaves / 0 mismatches - the iter037 record).",
  "historical_fidelity": "composed in V4 from the current evidence: the BINDING MECHANISM is engine-confirmed; the witness chain = ORIGINAL bytes (Models.bnt SHA C950A8C2..., Textures.bnt SHA 61ACD13B... pinned) - ONE model + ONE texture only; the RENDERED FOLIAGE MESHES beyond the witness remain GENERATED_CACHE (the export source corpus UNVERIFIED at file level) - labeled, never claimed byte-faithful.",
  "evidence_status": "CONFIRMED (mechanism) + the ORIGINAL-DIRECT single witness delivered (iter037); GENERATED_CACHE labels superseded ONLY where the witness chain applies (the non-witness models keep the honest GENERATED_CACHE label).",
  "era": ["PCG_9_3_5", "legacy export corpus (labeled)"],
  "denominator": "1 witness model + 1 texture + the 10-candidate census (the V4-composed denominator; the witness record denominators: 16/16 blocks strict, 575 parser leaves, 5/5 mutation controls).",
  "limitations": "single-witness scope: the original-direct proof covers ONE model (457485) + ONE texture (457490) + the 10-candidate census - NOT era-wide; the FULL clean-NIF path, the WITNESS MATRIX (known-good + mildly wrong + severely scrambled + v4 + v10 + character/clothing - ledger ENTRY #4 R4), and the scrambled-texture FALSIFICATION (ledger ENTRY #3) stay OPEN; [P-MATERIALS] the per-model materials of the non-witness models = GENERATED_CACHE GLBs (the era-bounded approximation, never claimed byte-faithful).",
  "evidence": [
   {"file": "iter032_re_dec_0094b1d0_getmodel.c", "sha256": "A0C2C9566EB40FFBE2EC0FD018E65F509FA643CAFD2AF6B4F0A7623C41168278"},
   {"file": "iter033_foliage_generator_census.json", "sha256": "3AAFBF4874046395C63EA095B69FC172C4A908E22D0980448BD852416FA80E24"},
   {"file": "iter033_manifest.json", "sha256": "DD59815206F35E795B6A9E6BE6A89C053DF17B9DF696CAB9658D0026179BBFAA"},
   {"file": "assets/foliage_glb/MANIFEST.json", "sha256": "F299C6222917DA8859351D9BE4D2DF0D40F9C6BB7767378DFB22B18C4FFAD46C"},
   {"file": "offline_rechecks.json (repair run 01_RAW)", "sha256": "C80E65D62147E8DED2DE9C3D8EE028DE14BF619CB80C69BE71D30C8F0DEB4E32"}
  ]
 },
 {
  "row": 9, "subsystem": "FOLIAGE_BIOME_RULES",
  "knowledge": "the 12-column VCL records carried canonically: col1 density 0..330 (median 0.6), col2/col3 scale pair (corr 0.449), col4/col5 elevation bands (corr 0.296), col7 ~maxElev (corr 0.382), col10/col11 probability pair (corr 0.370); ADJACENT CLIMATE INDICES SHARE MODEL SETS (0<->9 Jaccard 0.583, 16<->17 0.500, 30<->31 0.500, 23<->24 0.375); the VCL ids 0..31 vs the palette ids 0x66dc6..0x85527 = DISJOINT value spaces (TWO climate resource families with ONE shared init FUN_0044d590); the .tez = LOCAL terrain edit zones (widths q50 56u, the z field a target height; alignment near-random vs the 1024u climate cells - NO climate carrier; the d>0 20xxx family = west-clustered, era-stable, byte-proven disjoint from templates/hierarchy id spaces except one crossing d=20070==B(template 1969), role UNVERIFIED).",
  "implementation": "the records decoded canonically into the generator; the climate choice = DOCUMENTED constant index 0 [P-CLIMATE] (the constant-byte-0 convention, like materials P1) - no historical-truth claim.",
  "validation": "iter032_vcl_columns (census + correlations); iter032_climate_id_space (disjointness measured from both id sets); iter032_tez_zoning_v3 (geometry census, both eras 1015/1020 records); iter022 (the id-space joins, raw + structured, both eras).",
  "historical_fidelity": "the DATA is original (both eras byte-identical); the SELECTION SEMANTICS (which .vcl applies where) are PLAUSIBLE-UNVERIFIED (the shared-selector hypothesis).",
  "evidence_status": "PARTIALLY CONFIRMED (record structure CONFIRMED; the per-location selection UNVERIFIED -> [P-CLIMATE]).",
  "era": ["JUL_2003", "PCG_9_3_5"],
  "denominator": "the 12-column census (492 rows) + the correlation measurements + the disjointness measurement + the .tez geometry census (1015/1020 records both eras) (the iter048-basis validation records; carried content current per the V3).",
  "limitations": "cols 6-11 semantics UNVERIFIED (open #17); the climate->region binding NOT FOUND in .tez (measured negative); the 2xxxx cross-container resource-space hypothesis PLAUSIBLE (open #26).",
  "evidence": [
   {"file": "iter032_vcl_columns.json", "sha256": "A62D9473D6D6D82C97595CEECCBCB915490F95A2B0F14750DBC03075A6526789"},
   {"file": "iter032_climate_id_space.json", "sha256": "D7541E1D4F5F76FB6BC331FAD2E82FE10C8A64AF63019E6E85897C1614D01F51"},
   {"file": "iter032_tez_zoning_v3.json", "sha256": "4892B189C6DE2F0783331AC305BDAAB4CAF4EA200BBF353141173DCA59806278"}
  ]
 }
]
