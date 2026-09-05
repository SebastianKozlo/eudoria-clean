# 00_FINAL_REPORT - PE_M1_GATE_V4_CORRECTION_R2_20260905_101327

- RUN: PE_M1_GATE_V4_CORRECTION_R2_20260905_101327 (the corrected re-launch of the R1 mandate;
  R1 = PE_M1_GATE_V4_CORRECTION_R1_20260905_100405 HARD-STOPPED correctly on a single-nibble pin
  transcription error in its own section 2; the R1 blocked-run evidence is preserved and was
  never touched by this run).
- EXECUTED BY: pe-reconstruction, per NEXT_PROMPT.md (SHA256
  0ACE8F637DB6A75F7BDE095B3FC09BF1DC8016D54DE0E8C46CAE728EE81AA7D9, launcher-verified BEFORE any
  work) - the PE-MASTER-refined 12-point correction mandate.
- MODE: OFFLINE. NO runtime, NO Ghidra, NO x87 CW capture, NO witness matrix, NO georef, NO patcher
  hunt, NO M2, NO edits to any frozen/completed file (including the blocked R1 dir), the
  repair-run evidence, shared tools, src/, AUDIT_ENTRYPOINT.md. INTERVENTION_LEDGER = EMPTY.

## 1. The launcher protocol + PRE_RUN_LOCKS (fail-closed)

- PROMPT SHA256 computed BEFORE any work: MATCH (0ACE8F63...).
- AUDIT_OUTPUT_ROOT verified FREE (the dir did not exist; created fresh with 00_CONTROL / 01_RAW /
  05_ANALYSIS / 06_REPORT).
- BASE_SHA recorded FIRST: faf215b4b5da80d30b895997c58f0a292d33fd08 (== the expected faf215b).
- PRE_RUN_LOCKS: ALL 21 pinned inputs re-hashed (python hashlib, streamed 1 MiB) - 21/21 MATCH,
  including the R1-corrected fail_closed_gates.json pin (...D59B0371... - the exact nibble R1's
  prompt mistyped). Evidence: 01_RAW\pre_run_locks_verification.json.
- Git status inspected FIRST: one PREEXISTING_UNCOMMITTED_WORK item recorded - `M AUDIT_ENTRYPOINT.md`
  (pe-master-auditor's file; OUT OF SCOPE per the mandate; never staged, never committed).

## 2. W10 - the PC24 SYNTHETIC RE-MEASUREMENT (executed FIRST; its result feeds the V4 content)

- Method (verbatim from the pinned records): the 38 synthetic pairs READ from the FROZEN
  domain_reproof.json (SHA-verified E654D2EF...; mismatch would have been an infeasible HARD STOP);
  the PC-mode method from oracle_battery.json (PC=24 -> f32(x) directly; PC=53 -> f32(f64(x)); the
  engine = the 80-bit x87 chain with per-step exactness ENFORCED); the lerp semantics EXACTLY
  repair_02_domain.py's lerp_engine/lerp_pc24/lerp_js (measure_pc24=True semantics), the IEEE
  rounders VERBATIM from repair_lib_ieee.py (SHA-locked); an int fast path guarded by a 1,998-sample
  equivalence assertion vs the verbatim Fraction path (0 divergences).
- Measured: **103,073 / 1,245,184** (38 pairs x 32,768 r; per-pair counts recorded).
- The negative controls (all PASS): NC1 the REAL-domain anchor re-measured = **14,104 EXACT**
  (the frozen + PE-MASTER-confirmed value); NC2 rand01 0/32,768 + positions 0/65,536 engine-vs-PC24
  (the frozen zeros); NC3 engine-vs-js 0 on all domains (the frozen zeros); NC4 the two pairs shared
  by the real + synthetic sets produce IDENTICAL per-pair counts (0=0 and 1491=1491); NC5 zero
  80-bit exactness violations on both domains.
- **DISPOSITION: CONFIRMED** - the 103,073 citation is promoted to CONFIRMED (double measurement:
  PE-MASTER auditor-side + THIS run-side, independent implementations, exact agreement).
- The frozen domain_reproof.json lerp_scale_synthetic.lerp_pc24_mismatches=0 stays UNTOUCHED (HYGI-1:
  it is a DEFAULT COUNTER - repair_02_domain.py ran the synthetic domain with measure_pc24=False;
  the reading "measured 0" was already retracted by CORRECTION_NOTES.md; this run's
  01_RAW\pc24_synthetic_measurement.json is the run-side artifact).
- Evidence: 01_RAW\pc24_synthetic_measurement.json (method, per-pair counts, total, input SHAs,
  script SHA, the five negative controls, the disposition).

## 3. W1/W2 - the V4 matrix (the new LIVE gate deliverable)

Built: `GATES\M1_GATE_DELIVERABLE_MATRIX_V4.md` + `GATES\M1_GATE_DELIVERABLE_MATRIX_V4.json`
(NEW physical files; generated from one composed dataset by 00_CONTROL\build_matrix_v4.py, so
MD/JSON field parity is structural and was re-verified post-write).

- ALL 19 rows physically carry 9 FIELDS in BOTH formats: KNOWLEDGE / IMPLEMENTATION / VALIDATION /
  HISTORICAL_FIDELITY / EVIDENCE_STATUS / ERA / DENOMINATOR / LIMITATIONS / EVIDENCE.
- The MD RENDERS the five charter section-13 labels per row (the V3 MD's verdict-only rendering -
  defect F1 - is not repeated).
- The six old-matrix field gaps COMPOSED + LABELED ("composed in V4 from <source>"): ROW2
  historical_fidelity; ROW13/15/16/17 implementation; ROW19 knowledge/implementation (the merged
  field split).
- The NO-COPY SET honored (rows 6, 8, 10, 11, 19 + the registry era_statements for P-RNG-DIV and
  P-POS-SCALE - the fourth stale carrier): composed from CURRENT evidence (the amendment records,
  the repair-run evidence, the V3 deltas, this run's PC24 measurement) - NEVER carried from
  ITER_048.
- W4 (ROW10): the knowledge field = ONLY the iter035 arithmetic - nodeX/Y = f32(u16/65535.0 f64)
  node-local fractions [0,1]; nodeScale = f32(|value * 0.00007812499825377017|) =
  float32(1/12800)-widened = 10737418/2^37; Math.fround at the six binary FSTP-DWORD points; 76/76
  bit-exact; CELL CONTENT RECONSTRUCTION-ONLY. The retracted arithmetic wordings ("pos = u16/K",
  "scale = |rand*2.0| MEASURED") are NOT carried.
- W5 (ROW11): the 32768.0 candidate REMOVED; [P-RNG-DIV] SUPERSEDED-LOCKED: _DAT_00a7d7a8 =
  32767.0 f64 (bytes 00 00 00 00 C0 FF DF 40, FDIV QWORD @0x0098CE5A); [P-POS-SCALE]
  SUPERSEDED-LOCKED: _DAT_00a8c758 = 65535.0 f64 (bytes 00 00 00 00 E0 FF EF 40, FLD QWORD
  @0x0095B2BC). The OPEN items KEPT: [P-RNG-P3] (*(impl+0x24) UNVERIFIED); the view-band p2
  provenance (10/20/30 STRONGLY_SUPPORTED, not byte-pinned); the actual-x87-CW conditionality
  (PC=24 breaks 14,104/229,376 = 6.15% of the REAL lerp domain AND 103,073/1,245,184 of the
  synthetic domain - the latter now double-confirmed; the CW itself UNMEASURED - the falsifier = a
  runtime capture, NOT authorized in this run).
- W6 (ROW8): the SINGLE ORIGINAL-DIRECT WITNESS (iter037: Models.bnt 457485 -> NIF v10.1.0.0 ->
  NiTriShape -> NiArkTextureExtraData 457490 -> TGA2; 16/16 strict; ONE model + ONE texture + the
  10-candidate census - NOT era-wide) SEPARATED from the STILL-OPEN full clean-NIF path + the
  witness matrix + the scrambled-texture falsification. The unbounded "queued" phrase is absent
  from all live fields.
- The HYG-5 citation-label defect NOT carried: iter033_manifest.json cites its own SHA
  (DD598152...); F299C622... is attached to assets/foliage_glb/MANIFEST.json.
- SHAs: V4.json 11FB16B0A175CE183F5C46E734737921DBA0BA72CD975C447CF197C2046F9C58;
  V4.md 5B90D2C43B3B0D9E5D9CBB05A387557862A61647D1A29F437F6F18416A744ACD.

## 4. W7 - EVIDENCE_MANIFEST_V4.json (built FROM THE V4 FIELDS)

- 19 claims, each carrying the V4's 9 fields + the full provenance chain (source / generator /
  SHA / denominator / independent truth / why_non_circular / failure case / dependencies /
  limitations) - NEVER the old matrix's carried fields.
- Every cited evidence file RE-HASHED from the physical file at build time: 72/72 MATCH
  (fail-loud: the build caught and fixed two transcription typos in carried SHA citations before
  anything was written to the repo - rows 9/13; the bounded-retry rule honored).
- The local-only originals identity table re-hashed: 5/5 MATCH (50.bnt, Entropia.exe,
  VegetationClimates.bnt, Models.bnt, Textures.bnt) - identity metadata ONLY, zero payload bytes.
- The old EVIDENCE_MANIFEST.json SUPERSEDED (the append-only index mark; the file untouched).
- SHA: A1E0F5B9C9B342645D9EFAF74319CD9839096B25EC6414C9B7CE165816AB69F8.

## 5. W8 - the semantic gate (run-local; report in 01_RAW)

- Scans ALL live fields of the V4 JSON (9 fields x 19 rows; registry v4_status + era_statement +
  missing/why/resume_path; known_open) + the V4 MD + the V4 manifest.
- FORBIDDEN phrases: "32768.0 divisor", "divisor candidate", "u16/K", "rand*2.0",
  "2.0 divisor CANDIDATE", "463141+20000", "4,912,912" - permitted ONLY in records explicitly
  typed as retraction/supersession.
- Clean scan: **PASS** - 0 hits, 0 problems; the single permitted typed carrier observed (the
  retired counter phrasing inside the manifest's typed supersession record).
- The negative fixtures (fail-closed proof, ALL behaving as required):
  - N1 (rows 8/10/11 from the V3 carried fields): **FAIL** - 4 hits ("u16/k" + "rand*2.0" in the
    row-10 carried knowledge; "32768.0 divisor" + "divisor candidate" in the row-11 carried bounds);
  - N2 (one section-13 field removed): **FAIL** - 1 problem (row 5 historical_fidelity vacuous);
  - N3 (the stale era_statement fixture "the 32768.0 divisor CANDIDATE"): **FAIL** - 3 hits;
  - N4 (the ROW10 required phrase removed): **FAIL** - 1 problem;
  - N5 (the clean V4 copy): **PASS**.
- REQUIRED phrases verified in BOTH formats: ROW10 "65535.0" + "float32(1/12800)"; ROW11 "32767.0" +
  "SUPERSEDED-LOCKED"; ROW8 LIMITATIONS "single-witness" + "457485"; the registry P-RNG-DIV /
  P-POS-SCALE v4_status "SUPERSEDED-LOCKED"; the five section-13 fields non-vacuous x 19 rows.
- Evidence: 01_RAW\semantic_gate_report.json.

## 6. W9 - the oracle counter split corrected

- The V4 package carries: **443,141 platform cross-validation samples (200,000 m2e f32 + 43,141
  subnormal-band f32 + 100,000 f64 + 100,000 arbitrary-rationals f32) + 20,000 f80-exactness sweep
  = 463,141 TOTAL** (consistent with oracle_battery.json platform_cross_validation - re-derived
  from the JSON's own sub-counts by the consistency check).
- The supersession note for the retired "463141+20000" phrasing at the repair-run
  STAGE_ACCEPTANCE_GATES.csv line 4 lives in EVIDENCE_MANIFEST_V4.json as a record EXPLICITLY
  TYPED as supersession. THE FROZEN CSV WAS NOT EDITED (re-hashed unchanged: 3277E5C7...).

## 7. The append-only V3-frozen/superseded marks (W1)

- The .pre copies saved as append-only prefix proofs: 01_RAW\GATE_INDEX.md.pre (B8FD886B... == the
  pinned pre-append value) + 01_RAW\AMENDMENTS.md.pre (5403B196... == the pin).
- APPENDED (never rewritten; byte-prefix-proven): the V4 correction record to GATE_INDEX.md
  (B8FD886B... -> FD68060A6318...) and the V4 consolidation note to GATES\AMENDMENTS.md
  (5403B196... -> C8FF0ABE475E...). The appended GATE_INDEX section records the actual V4/manifest
  SHAs (verified by the consistency check).
- The V3 files + the old matrix copies + the old manifest + the frozen package files re-hashed
  UNCHANGED post-run (the consistency check).

## 8. The consistency check (fail-closed; 01_RAW\consistency_report_v4.json)

30/30 checks PASS: 18 frozen pinned inputs unchanged (V3 md/json, the old matrix copies, the
amendment record, the old manifest, HANDOFF/RETRACTIONS/UNRESOLVED, the charter, the repair-run
evidence set, Entropia.exe); the R1 blocked-run dir preserved (untouched); the .pre pins + the
byte-prefix append-only proofs; the V4 structure re-verified independently (19x9 both formats, the
five labels per MD row); 72/72 cited evidence SHAs + 5/5 local-only originals re-hashed; the counter
split consistency; the PC24 measurement consistency (103,073 CONFIRMED, controls PASS); the
GATE_INDEX append SHA records; the payload scan (27 to-be-committed files, 0 binary-magic hits -
identity metadata only, zero proprietary payloads).

## 9. Bounded retries used (per the mandate's max-2 rule; all within element bounds)

1. Two SHA transcription typos in the composed carried citations (rows 9/13) - caught by the
   manifest builder's fail-loud re-hash, fixed from the pinned V3 citations (1 retry each).
2. The semantic gate's MD label regex + the manifest field name (v4_evidence_status ->
   evidence_status) - caught by the gate's own clean scan (1 retry); the manifest rebuild + the
   .pre-restore/re-append sequence used the .pre copies exactly as designed (the append re-verified
   the pinned pre-append SHAs before re-appending).
3. The PC24 script's negative-exponent product path (d=2.0 canonical e=-1) - caught by the run
   itself mid-domain (the real-domain anchor had already passed 14,104 EXACT before the crash;
   1 retry; the equivalence assertion + the controls cover the fix).

NO new stale-content class was discovered beyond the cataloged set during the V3/old-matrix/manifest
census (the census confirmed the cataloged carriers and nothing else) - no improvisation was
needed.

## 10. W11 - the commit scope (explicitly granted by the ORDERED_WORK)

- Committed ONLY: docs\audits\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE\** (the V4 matrix md/json, the
  EVIDENCE_MANIFEST_V4.json, the appended GATE_INDEX.md + GATES\AMENDMENTS.md) +
  docs\audits\PE_M1_GATE_V4_CORRECTION_R2_20260905_101327\** (the run mirror: REPORT.md, HANDOFF.md,
  the gates csv, artifact_index.csv, 00_CONTROL scripts, 01_RAW outputs incl. the .pre proofs).
- AUDIT_ENTRYPOINT.md NOT committed (out of scope; pe-master-auditor's file).
- BASE_SHA faf215b4b5da80d30b895997c58f0a292d33fd08 (recorded FIRST at run start; == the expected
  faf215b). OBSERVATION (no intervention): mid-run a PARALLEL SESSION committed d20e15d
  ("PE_NIF_R3_PERSISTENCE_AND_TARGETMAP_R1", governance-only) - verified via `git show --stat` to
  touch ONLY AUDIT_ENTRYPOINT.md + its own separate audit dir (13 files, zero overlap with THIS
  run's commit scope; it also explains the run-start PREEXISTING_UNCOMMITTED_WORK item
  `M AUDIT_ENTRYPOINT.md`, which the parallel session resolved). THIS run's commit sits on top of
  d20e15d; the working tree was otherwise clean.
- HEAD_SHA + PUSH_STATUS recorded below (post-push; a commit cannot embed its own hash - the
  committed mirror says "recorded run-locally").

## 11. W12 - the final status (binding)

**M1_PARTIAL + M2_HARD_STOP - UNCHANGED.** This run closes NOTHING beyond its own package; the
open items live in UNRESOLVED.md + the V4 known-open set; nothing here authorizes M2, the x87 CW
capture, the witness matrix, the georef pin, the patcher hunt, or any original-client execution.

## 12. FINAL HANDOFF BLOCK

```text
AUDIT_OUTPUT_ROOT      = D:\Eudoria_Reconstruction\99_Audits\PE_M1_GATE_V4_CORRECTION_R2_20260905_101327
FINAL_REPORT_PATH      = D:\Eudoria_Reconstruction\99_Audits\PE_M1_GATE_V4_CORRECTION_R2_20260905_101327\06_REPORT\00_FINAL_REPORT.md
PRIMARY_EVIDENCE_PATHS = 01_RAW\pc24_synthetic_measurement.json + 01_RAW\semantic_gate_report.json
                          + 01_RAW\consistency_report_v4.json + 01_RAW\pre_run_locks_verification.json
                          + 01_RAW\GATE_INDEX.md.pre + 01_RAW\AMENDMENTS.md.pre
                          + the repo V4 matrix (GATES\M1_GATE_DELIVERABLE_MATRIX_V4.md/.json)
                          + EVIDENCE_MANIFEST_V4.json + the appended GATE_INDEX.md / GATES\AMENDMENTS.md
BASE_SHA / HEAD_SHA    = faf215b4b5da80d30b895997c58f0a292d33fd08 / recorded RUN-LOCALLY after the push
                          (a commit cannot embed its own hash - see 99_Audits\PE_M1_GATE_V4_CORRECTION_R2_20260905_101327\06_REPORT\00_FINAL_REPORT.md)
PUSH_STATUS            = recorded RUN-LOCALLY after the push
RUN_STATUS             = V4_CORRECTION_COMPLETE
HARD_STOP_REASON       = NONE
INTERVENTION_LEDGER    = EMPTY (run offline)
```
