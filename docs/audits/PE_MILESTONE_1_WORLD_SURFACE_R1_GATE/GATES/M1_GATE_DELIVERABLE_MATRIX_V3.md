# M1 GATE DELIVERABLE MATRIX V3 (consolidated)

- CREATED BY: PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439 (2026-09-05) - the
  audit-repair package directed by the external V2 audit verdict DIRECT.
- CONSOLIDATES: iter035 (foliage operand lock + rows 10/11 re-judgment) + iter036
  (constlock sweep + noise correction) + iter037 (the original-direct witness) + THIS run
  (the validator repair, real-domain coverage, fail-closed gates, the section-derived
  address map, the offline re-checks).
- SUPERSESSION: the OLD matrix (02_ANALYSIS\M1_GATE_DELIVERABLE_MATRIX.md/.json, the
  ITER_048/b7d38ad snapshot, SHA256 F0C7D0F29EEE32F1... / F373E60ABF87BF04...) stays FROZEN HISTORY - this V3 is a NEW
  physical file, NOT an in-place amendment. The iter035 sidecar corrections are now
  physically consolidated here.
- SCOPE: PASS of this package = validator errors removed + coverage correct. It does NOT
  close M1, does NOT unlock M2, does NOT change charter section 13.
- TAXONOMY: CONFIRMED / STRONGLY_SUPPORTED / PLAUSIBLE / UNVERIFIED / REJECTED.

## THE 19 ROWS (charter section 13) - V3 statuses with scope/era/denominator + evidence

### ROW 1 - TERRAIN_HEIGHT
- **V3 VERDICT: CONFIRMED (structure/bytes); engine height-form: identity+operation CONFIRMED, final role STRONGLY_SUPPORTED**
- V3: carried unchanged from the ITER_048 basis (no new evidence this run)
- V3 DENOMINATOR: carried (see the iter048 row evidence)
- ERA: ['JUL_2003', 'PCG_9_3_5']

### ROW 2 - TERRAIN_GRID
- **V3 VERDICT: CONFIRMED**
- V3: carried unchanged from the ITER_048 basis (no new evidence this run)
- V3 DENOMINATOR: carried (see the iter048 row evidence)
- ERA: ['JUL_2003', 'PCG_9_3_5']

### ROW 3 - TERRAIN_WORLD_TRANSFORM
- **V3 VERDICT: STRONGLY_SUPPORTED (engine facts CONFIRMED; global georef intentionally NOT claimed)**
- V3: carried unchanged from the ITER_048 basis (no new evidence this run)
- V3 DENOMINATOR: carried (see the iter048 row evidence)
- ERA: ['PCG_9_3_5', 'JUL_2003']

### ROW 4 - TERRAIN_MATERIAL_RECORDS
- **V3 VERDICT: CONFIRMED (structure both eras; consumer role CONFIRMED 9.3.5)**
- V3: carried unchanged from the ITER_048 basis (no new evidence this run)
- V3 DENOMINATOR: carried (see the iter048 row evidence)
- ERA: ['JUL_2003', 'PCG_9_3_5']

### ROW 5 - TERRAIN_TEXTURE_RESOLUTION
- **V3 VERDICT: CONFIRMED (resolution layer, oracle-verified); world-data grids MISSING/ERA-BOUNDED (patcher-delivered)**
- V3: carried unchanged from the ITER_048 basis (no new evidence this run)
- V3 DENOMINATOR: carried (see the iter048 row evidence)
- ERA: ['JUL_2003', 'PCG_9_3_5', 'CD_JAN_2003', 'EU_LATER']

### ROW 6 - TERRAIN_BLEND_SEMANTICS
- **V3 VERDICT: CONFIRMED (era 9.3.5) - the noise-table validator REPAIRED this run**
- V3 DELTA: iter036 correction APPLIED and physically consolidated. THIS run: the noise tables re-checked 2048/2048 bit-exact with the NEW method (constants byte-derived from the EXE through the section-derived map; per-step 80-bit exactness ENFORCED, 0 violations; the P8/P9 division double-rounding 0 on the actual quotients). The OLD validator's gates were VULNERABLE (zip comparison, no length check: empty/prefix tables PASS) + its f32 rounder had the subnormal sign bug (-2^-149 -> +2^-149) - BOTH defects repaired and the repaired gates proven fail-closed on 13 negative controls; both defects measured LATENT on the actual data (no recorded result changes).
- V3 DENOMINATOR: 2048 recorded table entries at the FIXED seed 0x30303030 ([P4]; the per-session engine seed stays era-bounded)
- ERA: ['PCG_9_3_5']

### ROW 7 - FOLIAGE_SOURCE
- **V3 VERDICT: CONFIRMED (9.3.5 loader positive + source graph address-cited)**
- V3 DELTA: carried unchanged from the ITER_048 basis (no new evidence this run)
- V3 DENOMINATOR: carried (see the iter048 row evidence)
- ERA: ['JUL_2003', 'PCG_9_3_5']

### ROW 8 - FOLIAGE_MODEL_BINDING
- **V3 VERDICT: CONFIRMED (mechanism) + the ORIGINAL-DIRECT witness delivered (iter037); GENERATED_CACHE labels superseded where the witness chain applies**
- V3 DELTA: iter037 APPLIED: the single-model witness chain (Models.bnt bytes -> NIF v10.1.0.0 -> NiTriShape -> NiArkTextureExtraData 457490 -> TGA2 -> render) proven original-direct; the era binding = NiArkTextureExtraData (0/10 candidates contain NiSourceTexture - a TEN-CANDIDATE census fact, NOT an era-wide claim). THIS run re-checked the witness STRICTLY under the new gates: 16/16 blocks (index compared AS A FIELD), payloadSize 262188 present == my own BNT2 read == the oracle, payload SHAs equal - 0 mismatches. The witness MATRIX + the scrambled-texture FALSIFICATION (ENTRY #3) stay OPEN.
- V3 DENOMINATOR: 1 witness model + 1 texture + the 10-candidate census
- ERA: ['PCG_9_3_5', 'legacy export corpus (labeled)']

### ROW 9 - FOLIAGE_BIOME_RULES
- **V3 VERDICT: PARTIALLY CONFIRMED (record structure CONFIRMED; per-location selection UNVERIFIED -> [P-CLIMATE])**
- V3: carried unchanged from the ITER_048 basis (no new evidence this run)
- V3 DENOMINATOR: carried (see the iter048 row evidence)
- ERA: ['JUL_2003', 'PCG_9_3_5']

### ROW 10 - FOLIAGE_DISTRIBUTION
- **V3 VERDICT: CONFIRMED (mechanism + byte-locked arithmetic) / CELL CONTENT RECONSTRUCTION-ONLY**
- V3 DELTA: iter035 re-judgment APPLIED (the rows-10/11 corrections physically consolidated here, no longer sidecar-only). THIS run: the exhaustive lerp/scale proof now actually covers the REAL VCL domain - all 7 original 0.vcl (col2,col3) pairs x all 32768 r values (229,376 + 229,376 checks) with the REPAIRED oracle - engine(80-bit) vs JS(f64): 0 mismatches; the old oracle's bug frequency on the recorded domains measured 0 (its conclusions were accidentally correct). The [P-CELLSTREAM] stand-in + [P-CLIMATE] + cell-content origin stay OPEN.
- V3 DENOMINATOR: 7 real VCL climate-0 pairs x 32768 r (the union with the labeled synthetic 38-pair sensitivity domain: 43 pairs; total exactness comparisons this run 3,047,424, generated from results)
- ERA: ['PCG_9_3_5']

### ROW 11 - FOLIAGE_SEED/RNG
- **V3 VERDICT: CONFIRMED (identity + byte-locked FLOAT64 operands + f32 rounding) - CONDITIONAL on the x87 model (RC=nearest-even; PC dimension measured)**
- V3 DELTA: iter035 re-judgment APPLIED. The OLD proof's oracle was BROKEN (carry bug: to_f32(1-2^-25) returned 0.25; the auditor's counterexample) - THIS run repaired the oracle (platform cross-validated, 463k+ samples, 0 mismatches) and REPROVED the conclusion: all 32768 rand01 + 65536 positions + the real-pair lerp/scale domains agree engine-vs-JS with 0 mismatches. NEW CONDITIONAL EVIDENCE: PC=24 would differ on 14,104/229,376 lerp values - the engine-parity claim is CONDITIONAL on PC in {53,64} + RC=nearest-even (the documented Win32 default CW 0x027F; the actual client CW is UNMEASURED - a runtime capture remains the falsifier). The 'fully procedural' demotion stands; the cell-content origin stays OPEN.
- V3 DENOMINATOR: 32768 rand01 values + 65536 u16 positions + 7x32768 real-pair lerp/scale
- ERA: ['PCG_9_3_5']

### ROW 12 - WATER_SOURCE
- **V3 VERDICT: CONFIRMED**
- V3: carried unchanged from the ITER_048 basis (no new evidence this run)
- V3 DENOMINATOR: carried (see the iter048 row evidence)
- ERA: ['JUL_2003', 'PCG_9_3_5']

### ROW 13 - WATER_REGIONS
- **V3 VERDICT: CONFIRMED (data-level coherent regions + the RE plane-per-tile-node spawn)**
- V3: carried unchanged from the ITER_048 basis (no new evidence this run)
- V3 DENOMINATOR: carried (see the iter048 row evidence)
- ERA: ['JUL_2003', 'PCG_9_3_5']

### ROW 14 - WATER_LEVEL
- **V3 VERDICT: CONFIRMED (engine constant 10.0f) - the field-vs-tile georef UNPINNED ([P-DATUM] OPEN)**
- V3 DELTA: carried unchanged; [P-DATUM] explicitly OPEN (the georef pin was NOT attempted in this run - out of scope per the prompt's open-items rule)
- V3 DENOMINATOR: the engine-confirmed constant + the measured contradiction (carried)
- ERA: ['PCG_9_3_5', 'JUL_2003']

### ROW 15 - WATER_TEXTURE
- **V3 VERDICT: CONFIRMED (payloads + technique references); plane textures MISSING locally (era-bounded, no proxy as truth)**
- V3: carried unchanged from the ITER_048 basis (no new evidence this run)
- V3 DENOMINATOR: carried (see the iter048 row evidence)
- ERA: ['PCG_9_3_5', 'JUL_2003', 'CD_JAN_2003', 'EU_LATER']

### ROW 16 - WATER_MATERIAL
- **V3 VERDICT: CONFIRMED**
- V3: carried unchanged from the ITER_048 basis (no new evidence this run)
- V3 DENOMINATOR: carried (see the iter048 row evidence)
- ERA: ['JUL_2003', 'PCG_9_3_5']

### ROW 17 - WATER_ANIMATION
- **V3 VERDICT: CONFIRMED (mechanism chain; the env writer open)**
- V3: carried unchanged from the ITER_048 basis (no new evidence this run)
- V3 DENOMINATOR: carried (see the iter048 row evidence)
- ERA: ['PCG_9_3_5']

### ROW 18 - PESOURCE_MOUNT
- **V3 VERDICT: CONFIRMED**
- V3: carried unchanged from the ITER_048 basis (no new evidence this run)
- V3 DENOMINATOR: carried (see the iter048 row evidence)
- ERA: ['all four - era-explicit per mount']

### ROW 19 - RUNTIME_INTEGRATION
- **V3 VERDICT: CONFIRMED for the audited scope (the clean chain + deterministic regression vs OUR OWN recorded runtime) - the ORIGINAL-CLIENT visual parity NOT claimed**
- V3 DELTA: iter037 APPLIED (the original-direct witness integrated; the regression sweep 5/5 vs the recorded runtime). THIS run did NOT re-render (offline re-checks only) - the 76/2048/16 recorded results RE-VERIFIED bit-exact with the repaired method. The original-client comparison + the witness matrix stay OPEN.
- V3 DENOMINATOR: the recorded regression hashes (5 pages) + the offline re-checks
- ERA: ['PCG_9_3_5', 'JUL_2003']

## THE ERA-BOUNDED REGISTRY - V3 statuses

- **P1 (materials_confirmed)** - carried (open/era-bounded as in the ITER_048 basis)
- **P2 (materials_confirmed)** - carried (open/era-bounded as in the ITER_048 basis)
- **P3a (materials_confirmed)** - carried (open/era-bounded as in the ITER_048 basis)
- **P3b (materials_confirmed)** - carried (open/era-bounded as in the ITER_048 basis)
- **P4 (materials_confirmed)** - carried (open/era-bounded as in the ITER_048 basis)
- **P5 (materials_confirmed)** - carried (open/era-bounded as in the ITER_048 basis)
- **P-WAVES (water_system)** - carried (open/era-bounded as in the ITER_048 basis)
- **P-SKY (water_system)** - carried (open/era-bounded as in the ITER_048 basis)
- **P-DATUM (water_system)** - OPEN (not attempted in this run - the georef pin remains future work)
- **P-CLIMATE (foliage_system)** - OPEN (the cell-content origin remains open; the real-domain re-proof this run covers the sampler arithmetic only)
- **P-CELLSTREAM (foliage_system)** - OPEN (the cell-content origin remains open; the real-domain re-proof this run covers the sampler arithmetic only)
- **P-RNG-DIV (foliage_system)** - SUPERSEDED-LOCKED: _DAT_00a7d7a8 = 32767.0 f64 byte-locked (iter035; re-locked this run via the section map)
- **P-RNG-P3 (foliage_system)** - carried (open/era-bounded as in the ITER_048 basis)
- **P-POS-SCALE (foliage_system)** - SUPERSEDED-LOCKED: _DAT_00a8c758 = 65535.0 f64 byte-locked (iter035; re-locked this run)
- **P-SCALE-FIELDS (foliage_system)** - carried (open/era-bounded as in the ITER_048 basis)
- **P-WINDOW (foliage_system)** - carried (open/era-bounded as in the ITER_048 basis)
- **P-UNITS (foliage_system + water)** - carried (open/era-bounded as in the ITER_048 basis)
- **P-MATERIALS (foliage_system)** - carried (open/era-bounded as in the ITER_048 basis)
- **ROTATION (foliage - RE-faithful absence, not a placeholder)** - carried (open/era-bounded as in the ITER_048 basis)

## EXPLICITLY OPEN (kept open by this package - none solved here)

- the scrambled-texture FALSIFICATION (ledger ENTRY #3 - the witness must be used to falsify the U1 SEVERE cases) -- OPEN - explicitly NOT solved in this package
- the WITNESS MATRIX (known-good + mildly wrong + severely scrambled + v4 + v10 + character/clothing - ledger ENTRY #4 R4) -- OPEN - not started
- the georef pin / [P-DATUM] (field-vs-tile datum) -- OPEN
- the patcher-delivered world-data grids (65x65 climate / 129x129 details; [P1]/[P2]) -- OPEN - era-bounded placeholders stand
- the cell-content origin (the historical cell byte stream; [P-CELLSTREAM]) -- OPEN - the placement stand-in stays RECONSTRUCTION-ONLY
- the ORIGINAL-CLIENT visual parity (the regression sweep is vs OUR OWN recorded runtime; a server/original-client comparison is post-M1, human-gated) -- OPEN - milestone-scope limit, stated
- the actual x87 control word at chain-execution time (the PC/RC conditional model this run is measurement-free; a runtime capture is the falsifier) -- OPEN - added by THIS run (conditional-model honesty)

## THIS RUN'S EVIDENCE (all SHA-pinned in the run's 01_RAW/03_STATIC)

- oracle_battery: D:\Eudoria_Reconstruction\99_Audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439\01_RAW\oracle_battery.json (verdict PASS)
- domain_reproof: D:\Eudoria_Reconstruction\99_Audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439\01_RAW\domain_reproof.json (verdict PASS)
- fail_closed_gates: D:\Eudoria_Reconstruction\99_Audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439\01_RAW\fail_closed_gates.json (verdict PASS)
- pe_section_map: D:\Eudoria_Reconstruction\99_Audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439\03_STATIC\PE_SECTION_MAP.json (verdict -)
- constant_address_lock: D:\Eudoria_Reconstruction\99_Audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439\03_STATIC\CONSTANT_ADDRESS_LOCK.json (verdict PASS)
- offline_rechecks: D:\Eudoria_Reconstruction\99_Audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439\01_RAW\offline_rechecks.json (verdict PASS)

## HONEST LIMITS (binding)

- Self-regression + agreement of saved samples is NOT historical client fidelity.
- The engine-parity arithmetic claims are CONDITIONAL on the x87 model: RC=nearest-even
  (the documented Win32 default; NOT a measurement of the original client) and PC in
  {53,64} - PC=24 measured DIFFERENT on 14,104/229,376 lerp values (this run), so the
  condition is load-bearing; the actual control word is UNMEASURED (a runtime capture
  remains the falsifier - explicitly not performed, no runtime experiments).
- The noise-table seed is the FIXED reconstruction seed 0x30303030 ([P4] reduced to the
  seed only); per-session engine seeding is runtime state, unknowable statically.
- '71/71 on the given list' is NOT completeness of all constants - the claim coverage
  matrix states every searched-set boundary explicitly.
- The witness result covers ONE model + ONE texture (the 10-candidate census), NOT the era.
