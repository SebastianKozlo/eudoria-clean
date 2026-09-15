# HANDOFF — PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915 (executor -> PE-MASTER)
#
# AMEND (correction run PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915, executed in-place on this package):
# the origin-mutability content of this handoff was CORRECTED (the original "immutable zero-vector singleton /
# out = W*0.01 / 100:1" unconditional claims are retracted; writer site 0x00458E27 exists; the corrected status
# algebra is 02_ANALYSIS/ORIGIN_STATUS_CORRECTION.md). Corrected prose is amended inline with AMEND markers below;
# the correction's own handoff block is appended at the end of this file.

- AUDIT_OUTPUT_ROOT: D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915\
- FINAL_REPORT_PATH: 06_REPORT/REPORT.md
- PRIMARY_EVIDENCE_PATHS:
    01_RAW/FUN_0050A050_DOWNSTREAM_DISASM.txt        (Phase A: 36/36 pin MATCH — count amended per QC P2-2 — + stack/arg mapping + def-use NO answer)
    01_RAW/FUN_00437F70_DISASM.txt                   (Phase C: singleton getter; args ignored; SEH; census; 10 questions — S-lifetime prose amended by the origin-mutability correction)
    01_RAW/FUN_0082B5A0_DISASM.txt                   (Phase D: scaled-subtract converter; bit-exact constants; x87 trace; 7 questions — zero-origin simplification conditionalized)
    01_RAW/SOURCE_VECTOR_LAYOUT_RAW.txt              (Phase B: +0x90 = m_kWorld translate; world vs local; vtable matrix)
    01_RAW/END_TO_END_VALUE_FLOW_RAW.txt              (Phase E: per-component formulas + the triple write-census — AMENDED: the
                                                      "S={0,0,0} never-written => immutable" inference is retracted; the
                                                      census survives as a triple-ADDRESS measurement; the singleton-pointer
                                                      write-through is measured by the correction census
                                                      01_RAW/ORIGIN_SINGLETON_WRITE_THROUGH_CENSUS.csv)
    01_RAW/NEGATIVE_CONTROL_RAW.txt                   (4 executed controls; FAILURE_CASE_DETECTED=YES — Control 4 SUPERSEDED:
                                                      FALSIFIED_BY_COUNTEREXAMPLE 0x458E27; Controls 1-3 stand)
    01_RAW/FALLBACK_PRIMARY_COMPARISON.txt            (five contract questions answered — origin-condition wording amended)
    01_RAW/HELPER437F70_CALLER_CENSUS.csv / HELPER82B5A0_CALLER_CENSUS.csv  (99 / 36 sites, classified)
- RUN_STATUS: COMPLETE
- HARD_STOP_REASON: NONE

## Measured gate table (G0..G14 one-liners; full: 06_REPORT/STAGE_ACCEPTANCE_GATES.csv)
G0 PASS — S0 re-verified at run start (size+SHA256+PE layout MATCH).
G1 PASS — HEAD==BASE_SHA==origin/master==ls-remote 3068f31a...; untracked = 2 pre-existing + run dir; zero mutations.
G2 PASS — 36/36 pin MATCH (count amended per QC P2-2); both-helper arg mapping derived; FUN_0050A050 writes NO primary-path XYZ itself.
G3 PASS — m_kWorld translate +0x90/+0x94/+0x98 CONFIRMED; m_kLocal +0x5C distinguished.
G4 PASS — 437F70 = origin-singleton getter (S initial value {0,0,0} measured; AMENDED by the origin-mutability
    correction: "S={0,0,0} proven immutable" retracted — mutation channel exists, writer 0x458E27); plain ret;
    99-caller census; 10 questions answered; evidence file regenerated clean (G4_EVIDENCE_CONSISTENCY recheck PASS).
G5 PASS — 82B5A0 = out[i]=f32(f32(src[i]*K)-S[i]), K=(double)(float)0.01; exact x87 trace; 7 questions answered
    (arithmetic decode untouched by the correction; K bits re-verified BITMATCH).
G6 PASS — per-component dataflow recovered (basis corrected: the confirmed relation is out = scale(W) - S; the
    zero-origin reduction is a conditional special case); UNKNOWNs localized (space label; fallback stored-value scale).
G7 PASS — out float3 +0/+4/+8; return == ARG1.
G8 PASS — five fallback-vs-primary questions answered (conversion present ONLY in primary).
G9 PASS — 5 independent context classes; no single-caller promotion.
G10 PASS — 4 executed negative controls; FAILURE_CASE_DETECTED=YES; NC-4 SUPERSEDED (FALSIFIED_BY_COUNTEREXAMPLE
    0x458E27; Controls 1-3 stand).
G11 STRONGLY_SUPPORTED — scale-by-0.01 + base subtraction proven (K bit-proven); 100:1 magnitude relation
    CONDITIONAL on S=={0,0,0}; absolute space label UNVERIFIED.
G12 PASS — identity permutation proven; axis labels UNVERIFIED statically.
G13 PASS — bit-exact 0.01 scale proven (re-verified by the correction probe); cm->m reading = PLAUSIBLE interpretation.
G14 STRONGLY_SUPPORTED — position role corroborated by >=2 independent consumers; runtime trace not permitted;
    no unconditional scale relation asserted (correction wording).
G15/G16/G17 PASS — governance (fresh QC chain; adjudication; persistence by pe-master-auditor; G16 supersession
    chain pointer added by the origin-mutability correction).

## PRIMARY QUESTION — one-line answer at the highest status the bytes support (AMENDED by the origin-mutability
## correction: the ORIGINAL one-liner said "immutable zero-vector origin singleton" and "out[i] = f32(... - 0)
## = f32(W[i]*0.01f) — a 100:1 conversion" unconditionally — RETRACTED)
CONFIRMED: the primary path of SF slot3 does NOT copy the world translation — FUN_0050A050 writes nothing itself;
FUN_00437F70 fetches the origin singleton S (initial value {0,0,0} measured; NOT proven immutable — a mutation
channel exists: writer site 0x00458E27; runtime mutability/value UNVERIFIED), and FUN_0082B5A0
writes the caller's out float3 as the bit-exact per-component conversion
out[i] = f32( f32( m_kWorld.m_Translate[i] * (double)(float)0.01 ) - S[i] ) — an engine->internal-space position
conversion (identity axis order; IF S == {0,0,0} — the measured initial value — this reduces bit-exactly to
f32(W[i]*0.01f) and a 100:1 magnitude relation), paired with a measured inverse family
((src+S)*100.0) and contrasted by an unscaled raw-copy fallback of the stored placement value.

## SCIENCE_STATUS_DELTA (all 11 dimensions; full CSV: 02_ANALYSIS/SCIENCE_STATUS_DELTA.csv)
SOURCE_OBJECT_IDENTITY=CONFIRMED; SOURCE_FIELD_IDENTITY=CONFIRMED; SOURCE_VECTOR_LAYOUT=CONFIRMED;
HELPER_437F70_OPERATION=CONFIRMED; HELPER_82B5A0_OPERATION=CONFIRMED; OUTPUT_BUFFER_LAYOUT=CONFIRMED;
OUTPUT_VALUE_RELATION=CONFIRMED; COORDINATE_SPACE=STRONGLY_SUPPORTED; AXIS_MAPPING=CONFIRMED(identity
permutation; labels UNVERIFIED); UNIT_SCALE=CONFIRMED(bit-exact; cm->m reading PLAUSIBLE);
FINAL_POSITION_SEMANTIC_ROLE=STRONGLY_SUPPORTED.

## Findings contradicting standing knowledge labels (loud)
1. FUN_00437F70 is NOT a value-transfer helper (H2 REJECTED by bytes) — it is an origin-singleton getter that
   ignores both stack args; the entire output computation lives in FUN_0082B5A0.
2. FUN_0082B5A0 is NOT a copy — the SF slot3 primary output is scale(W) - S (IF S == {0,0,0}, the measured
   initial value, it is a 100:1-scaled position — engine translate x 0.01; AMENDED by the origin-mutability
   correction: the unconditional "off by 100x" reading is retracted), so any consumer treating slot3 output as
   engine-units is off by the scale relation only under the zero-origin condition; the fallback output is a
   DIFFERENT derivation (raw stored placement value, no conversion) sharing only the float3 interface.
3. FUN_0082B790's apparent [ecx] writes are a loop over a FRESH array — ECX (singleton) is clobbered at 0x82B79B
   before use; naive write-scans would misclassify it as a singleton setter (trap-library candidate).
4. All package-A/B pins re-measured MATCH (extent, ABI, slot17, +0x90) — no contradiction to prior canon; the
   contradiction targets only the UNMEASURED helper semantics that prior runs explicitly left as "do NOT inherit".

## Notes for QC
- ZERO git mutations performed; untracked set at run end = 2 pre-existing + this run dir (AT_RUN_END_GIT_OBSERVATION.md).
- AMEND_LOG_R1.md DOES exist and is part of the package: it contains the 2 pre-execution-completion entries
  (AMEND-1 evidence-index self-hash fix; AMEND-2 UTF-8 normalization of the raw files) PLUS the correction-pass
  entries added after the fresh QC (AMEND-3.. per the QC findings; see 00_CONTROL/AMEND_LOG_R1.md and
  00_CONTROL/PRE_EDIT/ for the byte-exact pre-edit copies). (AMEND NOTE, QC P2-3: this note originally claimed
  "No AMEND_LOG_R1.md — no correction was needed after any run artifact was written", which was wrong about the
  package state; the ImageBase-offset event it refers to remains disclosed in AT_RUN_START SECTION 2.)
- Raw files carry measured provenance headers (python 3.12.7 / capstone 5.0.7 / script SHA256 / source SHA256).
- MANIFEST_SHA256.csv follows L12 self-exclusion. Static analysis only; the client was never executed.

## CORRECTION RUN PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915 (executor handoff amendment; in-place)

- CORRECTION RUN_ID: PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915 (SCIENCE_CORRECTION_REVALIDATION; STATIC-ONLY;
  zero git mutations; no new package root)
- WHAT WAS CORRECTED: the origin-singleton mutability claims of this package. The original run claimed
  "no caller writes through the returned pointer within 8 instructions (measured over all 99 sites)" and
  "S == {0,0,0} permanently / immutable after construction" — BOTH RETRACTED: the write-through measurement never
  existed (fabricated measurement claim; the original census instrument looked at 2 instructions and keyed on the
  first instruction's pattern, recording instruction_after_next='mov dword ptr [eax], edx' for the very site it
  needed to interpret), and the immutability inference from the (valid) triple-address write census was invalid.
- COUNTEREXAMPLE (measured by the correction's own instruments, reproduced BEFORE any canonical edit):
  site 0x00458E27 (call 0x437F70) inside FUN_00458D90..0x458E43; EAX = getter return (proven); writes
  0x458E30 mov [eax],edx / 0x458E36 mov [eax+4],ecx / 0x458E3D mov [eax+8],edx (offsets 0/4/8);
  operation S[i] := f32(f80(-(int32_in[i]))); input ECX = 12-byte int32 triple; statically reachable from the
  message loop (FUN_00402910 --0x40296F--> FUN_00417030 tick --guarded--> 0x4171BA --> FUN_00458E50
  --delta-condition 0x458EE2--> 0x458EF2 --> FUN_00458D90). RUNTIME execution/value: UNVERIFIED (STATIC-ONLY).
- CORRECTED STATUS ALGEBRA (full: 02_ANALYSIS/ORIGIN_STATUS_CORRECTION.md):
  ORIGIN_INITIAL_ZERO=CONFIRMED; ORIGIN_MUTATION_CHANNEL_EXISTS=CONFIRMED; ORIGIN_MUTATED_AT_RUNTIME=UNVERIFIED;
  ORIGIN_PERMANENT_ZERO=REJECTED; ORIGIN_RUNTIME_VALUE=UNVERIFIED;
  OUTPUT_GENERAL_FORMULA=CONFIRMED (out[i]=f32(f32(W[i]*K)-S[i]); K=0x3F847AE140000000 BITMATCH; ret 8);
  OUTPUT_ZERO_ORIGIN_SPECIAL_CASE=CONFIRMED CONDITIONALLY (IF S=={0,0,0}; sign-of-zero caveat);
  OUTPUT_ALWAYS_W_TIMES_0_01=REJECTED (as unconditional); PRIMARY_ALWAYS_100X_SMALLER=REJECTED (as unconditional);
  NUMERIC_SCALE_FACTOR=CONFIRMED; CM_TO_M=PLAUSIBLE (not upgraded);
  NEGATIVE_CONTROL_4=FALSIFIED_BY_COUNTEREXAMPLE (Controls 1-3 stand).
- NEW EVIDENCE (correction run): 01_RAW/ORIGIN_SETTER_458D90_DISASM.txt; 01_RAW/ORIGIN_SINGLETON_WRITE_THROUGH_CENSUS.csv;
  01_RAW/ORIGIN_SINGLETON_WRITE_THROUGH_RAW.txt; 01_RAW/ORIGIN_SETTER_CALLER_CENSUS.csv;
  01_RAW/ORIGIN_SETTER_REACHABILITY_RAW.txt; 01_RAW/OUTPUT_FORMULA_REVALIDATION_RAW.txt;
  01_RAW/CORRECTION_RUN_GIT_OBSERVATION.md; 02_ANALYSIS/ORIGIN_STATUS_CORRECTION.md;
  new scripts: sprov.py, probe_origin_setter.py, census_write_through.py, census_setter_reach.py,
  probe_output_formula.py (all S0 fail-closed, read-only on the EXE; recorded in SCRIPT_SHA256.csv).
- CENSUS NUMBERS (pre-registered N=16 + N=8 views; denominator 99 re-measured, all boundary-verified):
  N=16: WRITE_S_PLUS_0+4+8=1 (0x458E27); S_PTR_ESCAPED_READ_ONLY=43; S_PTR_ESCAPED_UNRESOLVED=12;
  INSUFFICIENT_PROOF=6; CONTROL_FLOW_ESCAPE=1; NO_WRITE_WITHIN_BOUND=17; S_PROVENANCE_LOST=19 (sum 99 OK).
  N=8 (historical view): 41/8/14/17/18/1 — at N=8, 17 sites are bound-exhausted-live: the original
  "measured within 8 instructions" claim could not have resolved those sites even if it had been measured.
- EXTERNAL-AUDIT BRANCH CORRECTIONS (measured): Branch A (0x514EF0 vtable 0xA7D764 slot 5; RTTI
  .?AVArkClientPlayerImpl@@) has real edges (0x5159E5->0x417880->0x417972->0x416FD0) but NEVER reaches the setter;
  the auditor's "0x458E50 <- 0x416FD0" attribution is FALSE (0x4171BA is inside FUN_00417030; 0x416FD0's own
  callees exclude 0x458E50); 0xA7A240.. is a data descriptor, not a vtable. Branch B subtree re-derived (AMEND-23/24 per QC_R3 F1): NOT self-recursive and NOT statically dead — the
  E8 sites 0x4B1EEB (call 0x417A40) and 0x4B1F2C (call 0x4B1B70) both lie inside FUN_004B1C70 (FUN_004B1B70
  extent ends ret @0x4B1C6E + int3 0x4B1C6F); FUN_004B1C70 has external caller E8@0x4B2984 inside FUN_004B2950
  (Execute, case-0xB2 dispatch) => the subtree Execute --0xB2--> FUN_004B1C70 -> {0x417A40 -> 0x417880 ->
  0x416FD0; 0x4B1B70} is STATICALLY REACHABLE within the measured channels and STILL NEVER REACHES the origin
  setter (immaterial to origin mutability; the setter's sole static in-tree remains the message-loop chain).
  [AMEND-28 (QC_R3 F1 residual copy, PE-MASTER-verified; logged in AMEND_LOG_R1.md): this sentence originally
  read "Branch B (0x4B1B70: sole self-recursive E8 0x4B1F2C, zero imm32/vtable) is statically dead within
  measured channels AND immaterial (does not reach the setter)" — RETRACTED per AMEND-23/24; the corrected
  disposition is canonical in 02_ANALYSIS/ORIGIN_STATUS_CORRECTION.md, the CG4 gate basis and
  01_RAW/ORIGIN_SETTER_REACHABILITY_RAW.txt [R.6].] ANCHOR DISCREPANCY (loud): PE-MASTER's anchor note said "ret 0xc @0x0041702D"; measured ret @0x0041702C
  (0x41702D is mid-instruction; boundary conclusion unchanged).
- GENERATOR REPAIR: gen_raw_evidence.py / census_triple_writes.py no longer emit hardcoded science conclusions
  (GENERATORS EMIT MEASUREMENTS; CONCLUSIONS LIVE IN THE ANALYSIS LAYER); gen_manifest.py role map neutralized +
  extended; QC-pass inline amendments moved INTO the generators so regeneration preserves them; regenerated files
  verified: measurement content byte-stable vs 00_CONTROL/PRE_EDIT_R2 (diffs = corrected prose + disclosed
  GENERATED_UTC/GENERATOR_SHA256 headers only); HELPER437F70/HELPER82B5A0 census CSVs byte-IDENTICAL.
- STANDING LESSONS (recorded in AMEND_LOG_R1.md AMEND-14+):
  LESSON 1: CLAIM_OF_MEASUREMENT_REQUIRES_MEASUREMENT_ARTIFACT.
  LESSON 2: ROW_INTEGRITY_DOES_NOT_VALIDATE_INFERENCE.
- SNAPSHOTS: every AMEND-14+ edited file has 00_CONTROL/PRE_EDIT_R2/<mirrored path>.pre (SNAPSHOT_MECHANISM =
  PRE_EDIT_R2); 00_CONTROL/PRE_EDIT/** verified byte-identical (hash census before/after).
- PENDING (NOT this executor's work): fresh QC of the corrected package (QC_AUDIT_R3 by a later session);
  the superseding PE-MASTER review (CURRENT scientific adjudication for the corrected claims);
  persistence (path-limited commit/push happens only after fresh QC + adjudication, as a separate ordered pass).
