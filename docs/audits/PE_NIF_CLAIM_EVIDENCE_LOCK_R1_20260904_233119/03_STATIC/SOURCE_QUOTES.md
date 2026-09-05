# 03_STATIC — verified source quotes (file, lines, SHA256)
# PE-NIF-CLAIM-EVIDENCE-LOCK-R1 — every quote below was read this session from the
# exact file at the given SHA. Line numbers are 1-based in the on-disk file.

## S1 — R32 REPORT.md (SHA256 b985f6fda047ebf05de50dd9bec1fa2cb63b9492cbf40961cd05ba9de397d7ec)
Path: D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MATERIAL_CENSUS_R32_20260904_160538\REPORT.md

- L12 (S1): "a **40-slot** vocabulary (8 major slots + ANIM0–31 + DECAL0) with a
  **perfect f1↔slot enum mapping** (f1 IS the slot-type code: BASE=0, DARK=1,
  DETAIL=2, GLOSS=3, GLOW=4, BUMP=5, DECAL0=6, ENVIRONMENT=9, ANIM=11 in
  985/1,157 ANIM entries — late v4 frames carry 0/4)"
- L108 (S4.3 table, ANIM0–ANIM31 row): "**11** in 985/1,157 (all 985 f1=11
  entries corpus-wide are ANIM); the 172 others use f1=0 ×142 / f1=4 ×30
  (mostly v4 late frames)"
- L110 (S4.3): "f1 = slot-type enum — CONFIRMED as a per-slot constant with zero
  exceptions for BASE/DARK/DETAIL/GLOSS/GLOW/BUMP/DECAL0/ENVIRONMENT (and 11 for
  985/1,157 ANIM entries; the 45 late ANIM16–31 entries are mostly v4 with
  f1=0/4 — 10 of 45 carry 11)."
  [THIS-RUN NOTE: raw evidence gives 9 of 45, not 10 — see S2.]
- L138 (S7 CONFIRMED list): "f1↔slot enum for 8 named slots (zero
  counterexamples; ANIM=11 in 985/1,157)"

## S2 — R32 ANIM_FRAME_CHECK.json (SHA256 b293d84401150e0465f835487ff82be0381d7a3b64b891a6690fba8b461af8ae)
Path: D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MATERIAL_CENSUS_R32_20260904_160538\02_results\ANIM_FRAME_CHECK.json

- L2-6: anim_entries_total 1157 / frame_index_equals_slot_number 1157 /
  regular_00ffffffff_prefix 0 / mismatches [] / verdict CONFIRMED
- L184-199 (ANIM16): count 7, f1 {4:1, 11:3, 0:3}; ANIM17 identical;
  L206-227 (ANIM18/19): {4:1, 0:2, 11:1}; L228-238 (ANIM20): {4:1, 0:1, 11:1};
  L239-328 (ANIM21-29): {4:1, 0:1} each; L329-346 (ANIM30/31): {0:1} each.
  Sum ANIM16-31: 45 entries, f1=11 in 9 (3+3+1+1+1), f1=0 in 22, f1=4 in 14.

## S3 — R34 morph_quant_r34.py driver (SHA256 8d788a9a37c4ab2b1d9f76f3d0fb1e3cab9b2a9bda0432089f694f41598d490e)
Path: D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_QUANT_R34_20260904_164538\01_source\morph_quant_r34.py

- L77-79: "WP_TOL = 1e-4  # weight-pair tolerance (ITER-4 basis)" /
  "VAR_MAX_K = 8  # variable-k parse max weights" / "VAR_NDELTA = 9"
- L810-811: "Parse dp[u:] as records [u16 idx][k weights sum~1][9 deltas],
  k = smallest matching 1..VAR_MAX_K."
- L824-840 (core loop): `found = False; for k in range(1, VAR_MAX_K + 1): ...
  if abs(sum(fls[:k]) - 1.0) <= WP_TOL: found = True; k_hist[k] += 1; ...
  p += need; break` — FIRST (smallest) match wins; no enumeration of
  alternative k, no uniqueness proof.
- L17 (REAL definition): "REAL = entry with (id != 0) AND (id < N) AND all-4
  floats clean" (+ pos%4==0 per L334 comment).

## S4 — R34 REAL_SPARSE_GRAMMAR.json (SHA256 2c26ba86db44ad7a58322c136112fec36e23efab1db1fafea1c976311eba007e)
Path: D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_QUANT_R34_20260904_164538\02_results\REAL_SPARSE_GRAMMAR.json

- meta.fit_spans_tested = 6167; meta.real_record_spans = 2427;
  meta.real_record_spans_def = "has_real(>=1 REAL entry) AND n_wp_inrange>0"
- VARIABLE_K.spans_exact = 3186; .files_exact = 84;
  .spans_exact_of_real_record = 2093
- G1 = 132; G2 = 1547; M_SCAN.spans_with_any_valid_m = 3705;
  m_histogram contains [1,126] and [3,124]
- VARIABLE_K.exact_examples_cap50 contains:
  ["574845.nif",69,14,14,{"1":14}] and ["574845.nif",69,27,5,{"1":5}]
  (plus 25 more 574845.nif bi=69 spans, predominantly k=1)

## S5 — R35 GRAMMAR_VALIDATION.json (SHA256 2f15df0d14dd03e1ee49d6f3d69cc4f7249ed7067800ffccc5174b8bdfa62d80)
- morph_real_sparse_and_quant["2003"].grammar.k_histogram =
  {"1":1884,"2":3135,"3":829,"4":215,"5":108}
- shader_directives["2003"]: blocks 1741; directive_vocabulary_size 16;
  version_line_census {"0":1741}; declared_vs_actual_anomalies 0
- texture_slots["2003"]: anim_frame_check.anim_entries_total 1149;
  anim_entries_with_f1_11 977 (84.9%)
- G3B_record_grammar["2003"]: population_all_g3b 1653;
  population_binary_family_u4_mode2 1650; exact_fit 1650

## S6 — R35 FORMAT_EVOLUTION.json (SHA256 bfd2a3e0bb8f2cc25c8c554c649300c7ef134d0989a47181beb477049101def9)
- 21 claim objects C-G3B-1..C-IMP-4; verdict_counts {ERA-STABLE:19, EVOLVED:2}
- C-SHAD-2: "16-name vocabulary; shared with 9.3.5: 16; 9.3.5-only:
  ['BaseTexture']; 2003-only: []"

## S7 — R36 FIELD_D_TESTS.json (SHA256 2af4cd39d36db96a2013a6de75983469aa6e2e7856a40061de6c86c6d54ee043)
- populations: shared_names 5422 / identical 5208 / changed_same_version 211 /
  changed_version_flip 3 / old_only_2003 [13563, 261922, 38579, 524174] /
  new_only_953_count 174
- T1_d_stability: n 5208; d_stable 5205; d_unstable_sample_first20 =
  ["524071.nif","524077.nif","524083.nif"]
- T4 census name_derived_candidate_matches (both eras): d==crc32(payload)[==c]
  3435 / 3299; d==adler32(payload) 0; d==crc32(name) 0; d==crc32(name+0x0A) 0;
  d==adler32(name) 0; d==crc32(name+u32size_le) 0; d==crc32(u32size_le+name) 0;
  d==fnv1a(name) 0; d==size 0; d==offset 0

## S8 — R36 REPORT.md (SHA256 c878b3a85bf3636ac72fe7a839f2240a42c8b1457161400e64bec7025147d14a)
- L53-55 (verdict): "Overall semantics: **STRONGLY_SUPPORTED** (packer
  write-path semantics inferred from value patterns, not from packer code; 3 T1
  exceptions + 21 intermediate-CRC files rely on unobserved historical
  versions)."

## S9 — R29 PATTERNS.json (SHA256 d6d42801818205754ab84af2d2a0bc97d72cd6b491295b6d777df17cc121cd88)
- census.distinct_exact_headers 14; distinct_masked_headers 10
- era_matrix_nifver_x_exporter: 10.1.0.0 x Gamebryo_1_1 = 4004;
  10.1.0.0 x 4.1.0.12 = 507; 10.1.0.0 x 4.0.0.2 = 212; 10.1.0.0 x 4.0.0.0 = 115
  (sum of v10-with-4.x = 834)

## S10 — R37 CLASS_SEQUENCES.json (SHA256 2e1826fd9cf2e85c62e5ae4ed6f8cf255eff22731d29e15fe45ce90a6067d29c)
- a2_position.scene_root_target: bucket_census {TAIL: 347,
  HEAD_TAIL_ONLY: 1}; relpos {n:347, mean:1, median:1, min:1, max:1}
- class_histogram {1:17, 2:15150, 3:718}

## S11 — R38 MODE_ANALYSIS.json (SHA256 cc77c608c089bc131fd9d8c503a581edb6b82dbb6a65ef0374e8afd25d1e281d)
- M1_cross_tables.mode_census: {activeIdle:996, single:253, active:20,
  Single:4, "activeIdle/single":1}
- M3_mode_vs_mode.identical_param_pairs_diff_mode: two 41076.nif records for
  Bip01_rotator_1, one mode "activeIdle", one mode "single", both noted "all
  non-mode fields byte-identical to its twin record"
- verdicts.mode_is_state_binding_orthogonal_to_params = STRONGLY_SUPPORTED;
  verdicts.single_implies_count1_one_shot = PLAUSIBLE

## S12 — wiki README.md @ 077b8a4 == HEAD (SHA256 4f9765814e82b91762d4d1bc4ec608dbe75c020665c7f564b5f147983bc6400e)
Path: D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\nif\README.md
- L3-5: "This is the complete, evidence-based documentation of the NIF binary
  format as used by Project Entropia"
- L80 (state table): "NiArkAnimationExtraData — ... SEMANTICS decoded (TEXT
  behavior records ITER-5/16; Controllers attachment ITER-24; viewport suite
  ITER-25; modes ITER-38; event registry ITER-7/30); G3D class 01/02/03 engine
  roles UNVERIFIED (ITER-37)"
- L82: "NiArkTextureExtraData | CONFIRMED — 40-slot vocabulary, f1 = slot enum,
  packed field2 formula 4,838/4,838 (ITER-32)"
- L94-97: G3D entry preserving the UNVERIFIED caution (correctly scoped)

## S13 — wiki 09-semantics.md @ 077b8a4 == HEAD (SHA256 bb22d51823e10c92e132db6f4c388b50c6dd10b0de9accccd3b973b561a83606)
- L55: "The slot VOCABULARY itself is now closed — 40 slots with a perfect f1
  enum (ITER-32, next section)"
- L70-73: "encoded twice — in the entry-name suffix AND in entry f1 (a perfect
  1:1 enum): BASE=0, DARK=1, DETAIL=2, GLOSS=3, GLOW=4, BUMP=5, DECAL0=6,
  ENVIRONMENT=9, ANIM=11."
- L84-86: "ANIM0–31 — flipbook frames: each entry's trailing frame index EQUALS
  its slot number (1,157/1,157 auxiliary-verified)" [no f1 exception mention]
- L146+: "Mode = a STATE-BINDING label, orthogonal to the parameters
  (ITER-38)" [ungraded presentation of R38's graded verdicts]
- L180-181: "Uniform blocks = per-vertex morph records: [u16 tag][k × f32
  blend weights summing to 1.0][9 × f32 position deltas]"
- L190-194: "with k per-record ∈ {2,3,4} — byte-exact on 86.2% of real-record
  spans (ITER-34)"
- L204-218: field_c/field_d section; L208: "**d==c ⟺ the file has not changed
  since registration**"
- L219-228: "The importer exporter-string = the ORIGINAL toolchain version
  (ITER-29)" [ungraded]

## S14 — wiki 10-containers-corpus.md (SHA256 0b197ed46a5461ab4224b521f7c8351f0350ceb7ecc4c5fca657aa76ab5da094)
- L18-23: "field_d ... a CARRIED-FORWARD REGISTRATION CRC ... d==c ⟺ unchanged
  since registration.**"
- L38-40: "Status: STRONGLY_SUPPORTED (registration-event mechanism inferred
  from correlations; the archive tool that wrote d is not directly observed)."
- L121-125: "**Conclusion (CONFIRMED): the NIF extension formats are era-stable
  at the byte level — across a half-decade corpus gap every byte-exact grammar
  reproduces at 100% ... The era drift is CONTENT ..., never GRAMMAR.**"

## S15 — wiki 11-open-problems.md (SHA256 5fd138f2a71a77a1652b800df13efe15c2d44b5d2b6bad1f879612e868f1421c)
- L24: "BNT2 index field_d | **RESOLVED (ITER-36, STRONGLY_SUPPORTED)**:
  carried-forward REGISTRATION CRC ...; d==c ⇔ unchanged since registration"
- L74-81: "The honest 100% statement" (PARSE closure = 100%; BYTE coverage ≈
  100%; SEMANTIC closure = PARTIAL) closing with "nothing outside that list is
  open."

## S16 — PE_AUTO_LOOP.json (SHA256 df86731f358dd11ba162f39ad042a01cda4113b4043080ddfd843ba390d0996e; READ-ONLY)
- L298 (last_completed): "ITER-40 (pe-reconstruction): README
  state-of-documentation + 09-semantics enrichment - 9 proposals applied
  byte-safe (+236 lines): field_d bu..."

## S17 — R40 REPORT.md (SHA256 3b453ede4b807edbdff53c92d68f9d182e7e9cbbfadc89c7ba0d3872c2f7d4cc)
- L106-107 (S4): "Simulated apply: README 4,573 → 9,182 bytes; 09-semantics
  3,705 → 13,214 bytes (length deltas machine-matched in G7)."
  [THIS-RUN NOTE: true applied byte sizes are 9,213 and 13,326 — the report
  adds CHAR deltas to BYTE pre-sizes.]
- L118-119 (S5 G7): "simulate-apply invariant (README delta 4609/4609, SEM
  delta 9509/9509; new_texts exactly-once; CR-free)"

## S18 — R40 SEMANTICS_PROPOSALS.json (SHA256 82fde5918b6084c3340b4c816752cec0b2b9ca64b4a90c51192144da71f69e18)
- R40-SP2 proposal new_text contains "in entry f1 (a perfect 1:1 enum): ...
  ANIM=11" — the exception-omitting wording ORIGINATES in the worker proposal
  (the master applied it byte-exact; see C-R40-01).

## S19 — containers (read-only, both parsed directly by control_r1.cjs)
- D:\Eudoria_Reconstruction\01_Original_Files\BNT_Models\Models.bnt
  SHA256 1322adf2919b1b24a8b4fda9618347e00c5a2b35dbb54516e353f1cefd3524a6,
  5,426 entries, index exact
- D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt
  SHA256 c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0,
  5,596 entries, index exact
