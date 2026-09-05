#!/usr/bin/env python3
# -*- coding: ascii -*-
# v4_rows_e.py - the composed V4 row data, rows 10-11 (part 5 of 5).
# ROW 10 + ROW 11 = NO-COPY SET, composed per W4/W5 from the iter035 amendment
# + the CONSTANT_ADDRESS_LOCK + the repair-run evidence + THIS RUN's
# pc24_synthetic_measurement.json (the run-side double measurement of the
# synthetic-domain PC24 sensitivity: 103,073/1,245,184 CONFIRMED).
# The "@COMPUTE_ME@" sha placeholder is replaced by the builder with the actual
# SHA256 of 01_RAW\pc24_synthetic_measurement.json.

ROWS_E = [
 {
  "row": 10, "subsystem": "FOLIAGE_DISTRIBUTION",
  "knowledge": "composed in V4 per W4 from the iter035 amendment (the ONLY iter035 arithmetic; NOT carried from the ITER_048 matrix). FUN_0098fe00 procedural grid (subdivision 0..4 -> steps 1/2/4/8/16; INTEGER-ONLY per the iter035 census; 24B cells; density = *(cell+8)>>3); FUN_00990810 stored cell records {u16 x, u16 y, u32 id}; FUN_0095b180 spawn loop: nodeX/Y = f32(u16 / 65535.0 f64) = node-local fractions [0,1] (the _DAT_00a8c758 QWORD; node+0x5C/0x60); nodeScale = f32(|value * 0.00007812499825377017|) = float32(1/12800)-widened = 10737418/2^37 (the _DAT_00a980d0 QWORD; node+0x68); the u32 model bind at node+0x64; rotation IDENTITY = the RE-faithful absence; the spawn default level 1; Math.fround at the six binary FSTP-DWORD points; 76/76 bit-exact; CELL CONTENT RECONSTRUCTION-ONLY.",
  "implementation": "PEFoliageCore.js - the generator with every stage address-cited (the subdivision switch, the {u16,u16,u32} triple layout, the spawn fields; the arithmetic VERBATIM with the f32 roundings at the six binary FSTP-DWORD points); the historical cell byte-stream = the LOCAL DETERMINISTIC STAND-IN ([P-CELLSTREAM]: the placement hash + counts = max(0, round(col1 density)) are RECONSTRUCTION-ONLY, recorded; the [0,1]-node->world mapping lives in the visualizer path, NOT decompiled - the page's window calibration is a labeled CURRENT_RUNTIME_CALIBRATION).",
  "validation": "the ANTI-CIRCULAR revalidation (iter035): 76/76 instances BIT-EXACT (every f32 field, every u32 state, every position) vs the reference deriving its constants FROM the binary extraction and its records FROM the ORIGINAL VegetationClimates.bnt; the OLD shared-assumption reference FAILS 76/76 (the demonstrative negative); the exhaustive lerp/scale proof covers the REAL VCL domain - all 7 original 0.vcl (col2,col3) pairs x all 32768 r values (229,376 + 229,376 checks) with the REPAIRED oracle: engine(80-bit) vs JS(f64) 0 mismatches, per-step 80-bit exactness ENFORCED (0 violations), the old oracle's bug frequency on the recorded domains measured 0; 28 record-per-cell zero-counts recorded honestly; the elevation-band diagnostic MEASURED without filtering (62 within / 14 outside); the fresh sweep reproduced 76/76 exactly.",
  "historical_fidelity": "MECHANISM engine-confirmed + the arithmetic BYTE-LOCKED (iter035: the three QWORD operands + the six FSTP f32 points byte-locked; the bit-exactness proven exhaustively over the complete input domains); CELL CONTENT = the labeled RECONSTRUCTION stand-in (open, never claimed historical).",
  "evidence_status": "CONFIRMED (mechanism + byte-locked arithmetic) / CELL CONTENT RECONSTRUCTION-ONLY.",
  "era": ["PCG_9_3_5"],
  "denominator": "7 real VCL climate-0 pairs x 32768 r (the union with the labeled synthetic 38-pair sensitivity domain: 43 pairs; total exactness comparisons 3,047,424, generated from results).",
  "limitations": "cell byte-stream origin OPEN (open #18; [P-CELLSTREAM] the stand-in is RECONSTRUCTION-ONLY); rotation/variant candidates unread (open #19); the elevation-band filter rule UNVERIFIED (open #20); [P-CLIMATE] + [P-WINDOW] RECONSTRUCTION-ONLY (content/selection/window).",
  "evidence": [
   {"file": "iter033_foliage_generator_census.json", "sha256": "3AAFBF4874046395C63EA095B69FC172C4A908E22D0980448BD852416FA80E24"},
   {"file": "iter032_re_dec_0098fe00_grid_gen.c", "sha256": "D02FC56AF76C1B1CDA2CC85B15736D683BD3D13B945D93D8BDFFA27245E2BD9E"},
   {"file": "iter032_re_dec_00990810_cell_records.c", "sha256": "45339FE1862B967C093DA1823C1785A6C5967114BF1D9290A3182682249EBDD7"},
   {"file": "AMENDMENT_ITER035_ROWS10_11.json", "sha256": "2B1FF548D1323BA46D1A8B533BF8BA943B5A508390637C632817D90B58254385"},
   {"file": "offline_rechecks.json (repair run 01_RAW)", "sha256": "C80E65D62147E8DED2DE9C3D8EE028DE14BF619CB80C69BE71D30C8F0DEB4E32"}
  ]
 },
 {
  "row": 11, "subsystem": "FOLIAGE_SEED/RNG",
  "knowledge": "composed in V4 per W5 from the iter035 amendment + the CONSTANT_ADDRESS_LOCK (NOT carried from the ITER_048 matrix). seed = ((p4*16+p5)*16+p1+p2+p3)*0x5CC7 + 0x6D7 (uint32), state = x*8^x; then the MSVC rand() LCG state*0x343FD + 0x269EC3 >> 16 & 0x7FFF (r in [0, 32767], always >= 0 - the 2^32f FADD idiom in FUN_0098ce30 is DEAD CODE); rand01 = f32(r / 32767.0) -> [0, 1] INCLUSIVE (the FSTP DWORD @0x0098CE60 = the f32 rounding BEFORE return); the sampler value = f32(rand01*(max-min)+min) (the min/max are f32 fields; FUN_0095ac30 FSTP DWORD @0x0095ACF0); the seed inputs: p1 = the packed 32-bit query position, p2 = the VIEW BAND (10/20/30), p4/p5 = the record u16 pair (POSITION-KEYED); NO global seed, NO server RNG in the LOCAL spawn loop; the seed-20030130 legacy scatter = VISUAL_RECONSTRUCTION_LEGACY (different BY CONSTRUCTION).",
  "implementation": "VegetationRNG class in PEFoliageCore.js (the formulas VERBATIM, address-cited); the byte-locked operands: rand01 = f32(r / 32767.0 f64) [_DAT_00a7d7a8, FDIV QWORD @0x0098CE5A]; the node position fractions = f32(u16 / 65535.0 f64) [_DAT_00a8c758, FLD QWORD @0x0095B2BC]; the node scale = f32(|value * 0.00007812499825377017|) [_DAT_00a980d0, FMUL QWORD @0x0095B347]; the lerp f32 rounding at the FUN_0095ac30 FSTP DWORD.",
  "validation": "the INDEPENDENT python reference (m1_iter035_rng_reference.py - written from the Ghidra decompiles NOT the JS; its constants FROM the binary bytes, its records FROM the ORIGINAL VegetationClimates.bnt) recomputed ALL 76 instances: state0/samplerValue/scale EXACT, 0 mismatches, PASS; the human's byte-proven vector (RNG 9719: /32767 = 0.2966093935972167...) is a BUILT-IN test - verified BIT-EXACT as instance 0's RNG draw; the repaired oracle platform-cross-validated (443,141 platform samples + 20,000 f80-exactness sweep = 463,141 TOTAL, 0 mismatches); the exhaustive re-proof: 32768 rand01 + 65536 u16 positions + the 7x32768 real-pair lerp/scale - engine-vs-JS 0 mismatches with per-step 80-bit exactness ENFORCED (0 violations); the PC=24 sensitivity measured: REAL domain 14,104/229,376 (frozen + independently confirmed), SYNTHETIC domain 103,073/1,245,184 (CONFIRMED by THIS run's double measurement - pc24_synthetic_measurement.json).",
  "historical_fidelity": "engine-byte-confirmed for 9.3.5 (the three QWORD operands + the six FSTP f32 points byte-locked; the bit-exactness proven exhaustively over the complete input domains).",
  "evidence_status": "CONFIRMED (identity + byte-locked FLOAT64 operands + f32 rounding) - CONDITIONAL on the x87 model (RC=nearest-even; the PC dimension measured).",
  "era": ["PCG_9_3_5"],
  "denominator": "32768 rand01 values + 65536 u16 positions + 7x32768 real-pair lerp/scale (the frozen denominators; the synthetic PC24 sensitivity domain 38x32768 = 1,245,184 re-measured this run).",
  "limitations": "[P-RNG-DIV] SUPERSEDED-LOCKED: _DAT_00a7d7a8 = 32767.0 f64 (bytes 00 00 00 00 C0 FF DF 40, FDIV QWORD @0x0098CE5A) - the normalization uses the byte-locked operand, no candidate wording stands; [P-POS-SCALE] SUPERSEDED-LOCKED: _DAT_00a8c758 = 65535.0 f64 (bytes 00 00 00 00 E0 FF EF 40, FLD QWORD @0x0095B2BC) - the position normalization uses the byte-locked operand, no candidate wording stands. KEEP OPEN: [P-RNG-P3] p3 = *(impl+0x24) UNVERIFIED (p3 = 0 in the reconstruction - labeled); the view-band p2 provenance (10/20/30) STRONGLY_SUPPORTED not byte-pinned; the actual-x87-CW conditionality: PC=24 breaks 14,104/229,376 = 6.15% of the REAL lerp domain AND 103,073/1,245,184 of the labeled synthetic domain (CONFIRMED by the run-side re-measurement) - the engine-parity claim is CONDITIONAL on PC in {53,64} + RC=nearest-even (the documented Win32 default CW 0x027F; the ACTUAL client CW is UNMEASURED - the falsifier = a runtime capture, NOT authorized in this run); 'FOLIAGE_FULLY_PROCEDURAL_ZERO_SERVER_RNG' STAYS DEMOTED (the local spawn-loop chain is decoded; the cell-content origin remains open); the seed-20030130 legacy = VISUAL_RECONSTRUCTION_LEGACY.",
  "evidence": [
   {"file": "iter033_rng_crosscheck.json", "sha256": "F8056CD5EC3F7051DAF7799D7B3BAC92A7C9087A012CCD891BE61E70E6337F42"},
   {"file": "iter032_re_dec_0098cdf0_rng_seed.c", "sha256": "D416A42236A26759C6E2F3DD7C8A8A426880D949FDB80AC1536DE477BC5F1221"},
   {"file": "iter032_re_dec_0098ce30_rng_next.c", "sha256": "0A4AF5879DE70C1250BB3BD8D80A6CBC5D75E7DCC6E069EB406A7E4244CEB8F5"},
   {"file": "AMENDMENT_ITER035_ROWS10_11.json", "sha256": "2B1FF548D1323BA46D1A8B533BF8BA943B5A508390637C632817D90B58254385"},
   {"file": "CONSTANT_ADDRESS_LOCK.json (repair run 03_STATIC)", "sha256": "6F4A9A6ED2E26F18C59AEB88F571374B73647C80FE19F65D5F0B6466A8D80304"},
   {"file": "pc24_synthetic_measurement.json (THIS run 01_RAW)", "sha256": "@COMPUTE_ME@"}
  ]
 }
]
