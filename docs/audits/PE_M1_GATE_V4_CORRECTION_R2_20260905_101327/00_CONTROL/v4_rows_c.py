#!/usr/bin/env python3
# -*- coding: ascii -*-
# v4_rows_c.py - the composed V4 row data, rows 6-7 (part 3 of 5).
# ROW 6 = NO-COPY SET: composed from CURRENT evidence only (the iter036 closure
# + the repair-run re-checks + the byte-extracted .fx evidence) - NEVER carried
# from ITER_048. ROW 7 = carry row (current content, current verdicts rendered).

ROWS_C = [
 {
  "row": 6, "subsystem": "TERRAIN_BLEND_SEMANTICS",
  "knowledge": "composed in V4 from the current evidence (the iter036 closure + the repair-run re-checks + the byte-extracted .fx evidence; NOT carried from the ITER_048 matrix). TERRAIN_14 (materials.vfs 0x3ea, ps.1.4 + vs_1_1, byte-extracted iter024): D = d0*w0 + d1*w1 + d2*w2 (the factor texture RGB u8/255, UNRENORMALIZED in-shader) -> per-channel OVERLAY onto the base keyed on D vs 0.5 (D>=0.5 -> 1-2(1-b)(1-D), else 2bD) -> light/shadow/fog (the shadow term = the base alpha: mul r0, r0, r0.a); THE FACTOR CONTENT = ONE-HOT band selection by the palette-ALPHA 3-band partition (alpha>=73->R, 53..73->G, <53->B, A=255) + noise + accumulated weight - NO normalization needed or performed (the renorm candidate REFINED into the one-hot model; RAW + CLAMP255 falsified by measurement); the BASE = the palette bake (row = altitude 255*(1-(h-2)/512-noise2), col = 63*(noise1+roughness)); LAYER CAP 3 details + 1 base per ps.1.4 pass; FILTERING states verbatim (base/factor CLAMP + LINEAR/LINEAR/POINT-mip; details WRAP + LINEAR/LINEAR/LINEAR-mip, LOD bias -0.5, repeats 32/32/16); Terrain_14 = the LOADED primary (mode-2; Ark11 fallback mode-1); the TDF masks feed the VERTEX COLORS (row 4), NOT the factor. THE NOISE-TABLE OPERANDS ARE NOW BINARY-LOCKED (iter036): the constants are the BINARY f64 slots (4 corrected-at-code: the float32(0.01)/float32(0.005)/float32(0.4)/float32(0.2)-widened slots at 0x00A7B360/0x00A81D18/0x00A7B308/0x00A7B2D0; NOISE_OPERAND_LOCK exported); the RNG DRAW is the engine's EXACT construction (FUN_00405920: draw = (state & 0xFFFFFFFFFFFF)/2^48, EXACT by Sterbenz) SUPERSEDING the documented variant; the 9 f32 rounding points replicated (FUN_0093cbf0 FSTP sites P1-P9).",
  "implementation": "composed in V4 from the current evidence: terrain/materials_confirmed.html+js renders the CONFIRMED architecture with the BINARY f64 noise slots, the EXACT engine draw construction, and the 9 f32 rounding points (P1-P9) replicated; terrain/materials_wsum.html kept as the labeled comparison model; the naive 'sequential overlay mix' CURRENT_RUNTIME_CALIBRATION was FALSIFIED for the real engine (iter024) - superseded, not deleted.",
  "validation": "composed in V4 from the current evidence: the noise tables re-checked 2048/2048 BIT-EXACT with the REPAIRED method (constants byte-derived from the EXE through the section-derived map: C04=0.4000000059604645, C02=0.20000000298023224, C001=0.009999999776482582, C0005=0.004999999888241291, DIV20=20.0; per-step 80-bit exactness ENFORCED, 0 violations; the P8/P9 division double-rounding 0 on the actual quotients - offline_rechecks.json); the repaired gates proven FAIL-CLOSED on 13 negative controls (fail_closed_gates.json: 8/8 noise mutations + 5/5 witness mutations FAIL, clean copies PASS); the OLD validator's two defects (the zip-gate with no length check; the f32 subnormal sign bug) measured LATENT on the actual data (0 recorded result changes); the 18-tile worked-example gate 0.0% white saturation (vs naive 84.0%); the page probe naive 43.36% vs confirmed 0.0% (reproduced in the fresh sweep).",
  "historical_fidelity": "composed in V4 from the current evidence: the blend semantics are era-9.3.5-CONFIRMED from the shipped .fx + binary (the HLSL byte-extracted; the producer FUN_00939c40 decompiled + disasm-pinned; the 53/73 thresholds byte-match the ORIGINAL palette alpha values {45,62,85} - the double data-side confirmation); the PE2-2003 fixed-function blend is era-divergent RECORDED (never auto-propagated; open #22).",
  "evidence_status": "CONFIRMED (era 9.3.5; the noise-table validator repaired + the tables re-proven 2048/2048 bit-exact).",
  "era": ["PCG_9_3_5"],
  "denominator": "2048 recorded table entries at the FIXED seed 0x30303030 ([P4]; the per-session engine seed stays era-bounded) + the 13 fail-closed negative controls.",
  "limitations": ">4-material reduction mechanism UNRESOLVED (open #25); quadtree construction not RE'd (iter027 bound 1); LOD bias -0.5 not expressible in r185 (documented renderer deviation); [P4] reduced to the SEED only.",
  "evidence": [
   {"file": "iter024_fx_id_0x3ea_Terrain_14.hlsl", "sha256": "5AE4AF81B54A71E66E1F63A9718A984314D8FCB0763FDFFF19AE0C7EDF8516F1"},
   {"file": "iter024_blend_op_findings.json", "sha256": "BA08FFD6F92B741AA76E095AA0EEE7066C51AB73CC5CFD8FB39134C4CC204126"},
   {"file": "iter030_findings.json", "sha256": "1104F3186116A98856438741D7F7439E25E6DEF578EAD6D2AA666812B3951207"},
   {"file": "iter030_page_result.json", "sha256": "9B62AD3399F8D1D4E295862D5B065D580D5AB66E7DBA6655DD03FF3F20F8E39B"},
   {"file": "AMENDMENT_ITER036_CLOSURE.json", "sha256": "CBBEEEB9DF345FA804FE79011AF23D0F685E2CE51582B472BB3709BB3D590AE1"},
   {"file": "offline_rechecks.json (repair run 01_RAW)", "sha256": "C80E65D62147E8DED2DE9C3D8EE028DE14BF619CB80C69BE71D30C8F0DEB4E32"},
   {"file": "fail_closed_gates.json (repair run 01_RAW)", "sha256": "645C9FC472FA4E93445C539FB375EDADB4DF5890D59B03715F9E914E50C52775"}
  ]
 },
 {
  "row": 7, "subsystem": "FOLIAGE_SOURCE",
  "knowledge": "the 9.3.5 client LOADS the foliage system: FUN_0041dae0 registers '.vcl' extension + the VegetationClimates dir + VegetationClimates.bnt container, and CREATES ArkVegetationClimateFactory INSIDE it @0x00420007; 45 ArkVegetation* classes RTTI-proven (TD->COL->vftable chain, file-side deterministic); the client created at init FUN_0044cb70 <- FUN_0044d590 (the SAME init as the palette manager); VegetationClimates.bnt = BNT2, 32 .vcl entries, TAB-SEPARATED TEXT, 492 data rows, 12 numeric columns, 256 DISTINCT model ids; 255/256 resolve in Models.bnt (1 unresolved: 10136 - recorded); both corpus copies BYTE-IDENTICAL JUL==PCG (SHA 7B858401...); THE 2003 PE2 BINARY HAS NONE OF THIS (0 loader strings) - the data pre-dates the loader (era-labeled).",
  "implementation": "VegetationClimateDecoder.js (FUN_0083a7d0 semantics: the FLAT 12-value token stream -> 0x30 records; reproduces the audited 491-line + 9.vcl continuation census exactly) + PESourceMount.getVegetationClimate (BNT2 framing era-validated, SHA-pinned; provenance with the JUL byte-identity + loader-absence note).",
  "validation": "the string census + the mount decompile + the RTTI chain (fresh Ghidra project, sandbox SHA-pinned, ~250 functions decompiled); the VCL census re-derived (492/256/32 denominators - the '493' lead corrected to 492, off-by-one recorded).",
  "historical_fidelity": "for 9.3.5 the foliage is LOCALLY reproducible down to the RNG; for JUL_2003 the VCL data remains the historical reference WITH THE LOADER ABSENT - the era difference is recorded, never silently bridged.",
  "evidence_status": "CONFIRMED (9.3.5 loader positive + source graph address-cited).",
  "era": ["JUL_2003", "PCG_9_3_5"],
  "denominator": "the 32 .vcl / 492 rows / 256 ids census + the ~250-function RE sample + the RTTI chain (45 classes) (the iter048-basis validation records; carried content current per the V3).",
  "limitations": ".vcl fetch id source + type-id constant UNVERIFIED (open #3); cell byte-stream origin NOT closed (open #18); the JUL-era foliage RUNTIME semantics = absent-loader era fact.",
  "evidence": [
   {"file": "iter032_findings.json", "sha256": "AF8B900A3864612356A9575EE740F821BCEC1B7EB0FF65194E24A36E89B16866"},
   {"file": "iter032_rtti_chain.json", "sha256": "176BCCC010F606C4808DF07024E5216AD6AE6DA3D8EBBE669E4ACA6B6F4F8F8A"},
   {"file": "iter032_re_dec_0083a7d0_vcl_parser.c", "sha256": "F7E887DE9F27F0BD4E294C1CC7C5519018823A534E01DBD43F461B00D85D8A99"},
   {"file": "iter033_manifest.json", "sha256": "DD59815206F35E795B6A9E6BE6A89C053DF17B9DF696CAB9658D0026179BBFAA"}
  ]
 }
]
