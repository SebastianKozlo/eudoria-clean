# QC_R4_REPORT — fail-closed pin-validator repair + coverage-erratum correction report

- RUN_ID: PE_935_20002_PAYLOAD30_QC_R4_FAIL_CLOSED_CORRECTION_R1_20261002
- Executor: pe-reconstruction (PE-MASTER direct dispatch; NO_NESTED_TASKS; STATIC-ONLY —
  the pinned EXE was read as a static file solely for pin verification and identity hashing;
  it was NEVER launched; no Ghidra, no runtime, no new EXE/VFS science, no VFS reparsing,
  no downstream-consumer search, no placement experiment, no Q1/gate/milestone advancement).
- Contract: 00_CONTROL\QC_R4_CORRECTION_R1_20261002\RUN_CONTRACT.md (21,236 B, SHA256
  72EE288AC979BCCD8F65DECB6FD8E0BD1D07F4A0E6433E53870042C7E4A7BB14 — verified before work;
  companion CONTRACT_FREEZE.json SHA256 10221FC36CA9F3F43995EC45B254EAC02FD7F04DCC2C61E0F123DE953B745649 — verified).
- Base: 2b381b32b39d0939b0637ab0cf52419ca2eb4fa8 (== HEAD at start and at executor close;
  NO git operation was performed by this executor — no stage, no commit, no push).

## 1. F1 defect and repair summary

**The confirmed defect** (RUN_CONTRACT §1; source 04_QC\QC_R3_DESKTOP_CORRECTION\qc_tools\qc3_q1_pinverify.py,
SHA256 C354E559B99411DB3AD926577B4C6C8DF5A287B3D19C47B2832BCBC104089F0F, 18,199 B, 308 lines —
IMMUTABLE, byte-unchanged, not executed by this run): a per-pin verification exception was
appended to res["errors"] WITHOUT creating a pin result row (old lines 60-64), so the failed pin
VANISHED from res["pins"]; the denominator was computed as len(res["pins"]) (old line 66), and
overall_ok (old line 298) required neither errors == 0 nor comparison against the original
input-pin count. Fail-open consequence (Desktop counterexample): 185 input pins with one
malformed VA produced claimed denominator 184, verified_ok 184, overall_ok = true, exit 0.

**The repair** (04_QC\QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM\qc_tools\qc4_q1_pinverify.py, 30,772 B,
548 lines, SHA256 345D69FA6CEC60590F79B97FFE73F29538BEAF6704C5A5B9F7D14192DB8157A8 — the repaired
copy): R1 ORIGINAL_INPUT_PIN_COUNT captured before verification; R2 every input pin gets a
result row; R3 an exception produces an explicit FAILED row (pin_id + source + original VA
string + error retained) that STAYS in the denominator; R4 overall_ok requires processed ==
input count AND verified_ok == input count AND mismatch_count == 0 AND error_count == 0 AND all
51 semantic assertions PASS AND all required extra checks PASS (plus the R8 bijection and R10
identity/run-error conditions); R5 exit 0 iff overall_ok else 1; R8 stable pin_id
"<artifact-name>::<array_path>[<index>]" with identity-set bijection; R9 explicit
--inputs/--output CLI (no inherited QC-R3 path); R10 pinned-EXE SHA256 identity check at start
(expected E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31) + fail-closed
artifact loading and per-pin handling; R12 sys.dont_write_bytecode = True first statements.
Verification semantics otherwise IDENTICAL (R11): same four-artifact loading (pins[] with
entry_pins fallback + width_sources width_pins), same verify_pin comparisons, same extra checks
(incl. the BSS-tail factory note), same 19 semantic windows, same 51 semantic assertions.
The helper qc4_pe32_x86.py is a BYTE-IDENTICAL copy of qc3_pe32_x86.py
(FE0C2F2BEC51504C6A332DCE6C0C54B872A9F32D05D7242D897F5B4E4C819DD6, 20,432 B, 520 lines).
Full line-referenced change list: SOURCE_IDENTITY_AND_CHANGES.md.

## 2. Regression A — POSITIVE (canonical artifacts read in place)

Inputs: the four canonical artifacts at 01_RAW\DESKTOP_CORRECTION_R1\ (unchanged; hashes ==
CONTRACT_FREEZE positive_input_sha256 for all four). Subprocess PID 12816.

| Field (RUN_CONTRACT §4) | Expected | Measured | Result |
|---|---|---|---|
| INPUT_PIN_COUNT | 185 | 185 | OK |
| PROCESSED_COUNT | 185 | 185 | OK |
| VERIFIED_OK | 185 | 185 | OK |
| FAILED_COUNT | 0 | 0 | OK |
| ERROR_COUNT | 0 | 0 | OK |
| MISMATCH_COUNT | 0 | 0 | OK |
| DENOMINATOR | 185 | 185 | OK |
| RESULT_ROW_COUNT | 185 | 185 | OK |
| input<->row bijection (identity sets) | OK | OK (validator self-check + harness independent re-derivation; 185==185, no dups, no drops) | OK |
| semantic assertions | 51/51 PASS | 51/51 PASS | OK |
| extra checks | PASS | all_required_ok = true (6/6 required) | OK |
| overall_ok | true | true | OK |
| process exit code | 0 | 0 | OK |

Per-artifact: BRANCH_SELECTION_TRACE.json 96/96 ok; FALLBACK_PATH_RECORD.json 25/25 ok;
DESTINATION_PROOF_CORRECTION_R1.json 23/23 ok; CURSOR_PROOF_CORRECTION_R1.json 41/41 ok
(30 entry_pins + 11 width_pins). Every row status VERIFIED_OK.
Result: POSITIVE\QC_R4_PINVERIFY_POSITIVE_RESULT.json (203,571 B, SHA256
4FD61642D268C236BEBA4EB43F062DB2D00F2305FD4E5579430EE33CE2D05207).
**POSITIVE_REGRESSION_PASS = TRUE.**

## 3. Regression B — INVALID_VA (Desktop counterexample reproduction)

Fixture (machine-checked build; FIXTURE_INVALID_VA\FIXTURE_DIFF.json):
- the four canonical artifacts copied byte-for-byte; pre-mutation hashes == the
  CONTRACT_FREEZE positive-input hashes (4/4 MATCH);
- selector: fixture BRANCH_SELECTION_TRACE.json pins with va == "0x00977807" — EXACTLY ONE,
  index 74 (== PE-MASTER baseline census);
- mutation: exactly the one field va "0x00977807" -> "0xFFFFFFFF" — a length-preserving
  surgical byte splice; byte-level diff: same length, changed positions exactly
  32009..32016 (8 bytes = the differing characters of the two 10-char strings; the "0x"
  prefix is shared), everything else byte-identical;
- recursive JSON diff canonical-vs-fixture: EXACTLY ONE changed leaf —
  pins[74].va: "0x00977807" -> "0xFFFFFFFF";
- the other three fixture files hash-equal to the canonical ones;
- the fixture keeps all 185 input pin identities (per-artifact 96/25/23/41; pin_ids identical
  to canonical) — a value change, not a structure change;
- no EXE/VFS payload bytes anywhere in the fixture (derived audit evidence only).
Post-mutation fixture BRANCH_SELECTION_TRACE.json SHA256
F40AAA249A7D8C20B24F3E70839C3064AF16C3E7C6840A7917FAF5A5BA9F3B25. Subprocess PID 13996.

| Field (RUN_CONTRACT §5) | Expected | Measured | Result |
|---|---|---|---|
| INPUT_PIN_COUNT | 185 | 185 | OK |
| PROCESSED_COUNT | 185 | 185 | OK |
| VERIFIED_OK | 184 | 184 | OK |
| FAILED_COUNT | 1 | 1 | OK |
| ERROR_COUNT | 1 | 1 | OK |
| MISMATCH_COUNT | 0 | 0 | OK |
| DENOMINATOR | 185 | 185 | OK (the FAILED row STAYS in the denominator) |
| RESULT_ROW_COUNT | 185 | 185 | OK |
| input<->row bijection (identity sets) | OK incl. the FAILED row | OK (validator self-check + harness independent re-derivation) | OK |
| semantic assertions | 51/51 PASS | 51/51 PASS | OK |
| extra checks | PASS | all_required_ok = true (6/6 required) | OK |
| overall_ok | FALSE | FALSE | OK |
| process exit code | != 0 | 1 (nonzero) | OK |

The single FAILED row (retained, full identity): pin_id
"BRANCH_SELECTION_TRACE.json::pins[74]", source "BRANCH_SELECTION_TRACE.json", original VA
string "0xFFFFFFFF" (as present in the fixture input), error
"DecodeError: VA 0xffffffff not mapped to file", ok = false. The reproduced fail-open case is
REJECTED: the repaired validator reports denominator 185, exactly one FAILED/error row,
overall_ok = false, nonzero exit. **INVALID_VA_REGRESSION_PASS = TRUE** (a SUCCESSFUL negative
regression; the validator's nonzero exit is the expected rejection, not a run failure).

Result: INVALID_VA\QC_R4_PINVERIFY_INVALID_VA_RESULT.json (203,359 B, SHA256
060C5BEA3A52B0AF593236B122078F38D0770A336AA4104562C9DF68C419D547).
Machine summary of both runs: QC_R4_REGRESSIONS_SUMMARY.json (all §13 F1 machine fields;
OVERALL_REGRESSIONS_PASS = true; harness failures 0).

## 4. Additional R10 fail-closed SELF_CHECKS (executor self-checks; executed entirely in
   C:\Users\User\AppData\Local\Temp\opencode — NOTHING written inside the package)

- NC-1 missing-artifact input (empty --inputs directory): one input_resolution run error
  listing all four missing canonical artifacts, overall_ok = false, exit 1. Fail-closed. PASS.
- NC-2 unparsable JSON (corrupted BRANCH copy; other three valid): one artifact_load
  JSONDecodeError run error; the 89 loadable pins (25+23+41) were still enumerated and
  verified 89/89, but overall_ok = false and exit 1 (run-level error is never absorbed by
  pin counts). Fail-closed with partial evidence retained. PASS.
- NC-3 pin without a parseable va (va string "not-a-hex-va" at pins[74] in a temp copy):
  185/185 enumerated/processed, denominator 185, verified_ok 184, exactly one FAILED row with
  pin_id preserved, the original VA string retained and the ValueError retained; overall_ok
  = false, exit 1. Never skipped. PASS.
The EXE-identity-mismatch branch was NOT live-tested (the pinned EXE is present and correct;
falsifying it would require modifying the physical source, which is forbidden). Its code path
was verified by source read: hash mismatch -> run error + overall_ok = false + nonzero exit +
no PE32 construction + every enumerated pin reported as a FAILED row.

## 5. §8 contradiction / current-state sweep (executed; package + AUDIT_ENTRYPOINT.md)

Patterns swept: "fail-closed" claims about the QC-R3 pinverify; "every row triple-verified";
"no load-bearing ... NOT_CHECKED"; file-count/current-count staleness. Method: literal
pattern search over every .md file in the package (incl. BEFORE copies, the historical QC
reports, 00_CONTROL historical and current files) + the repo-root AUDIT_ENTRYPOINT.md,
followed by per-hit reading.

**Sweep outcome: NO LIVE current-state contradiction.** Per-hit dispositions:

- "fail-closed" hits: (a) 04_QC\QC_R3_DESKTOP_CORRECTION\QC_R3_REPORT.md L153 — about the
  x86 DECODER ("fail-closed on unknown opcodes"), not the pin-coverage logic; the immutable
  QC-R3 report is NOT touched per RUN_CONTRACT §8. (b) 06_REPORT\PE_MASTER_REVIEW.md L33
  ("expected-bytes pins fail-closed") — inside the preserved historical review superseded by
  the erratum. (c) 04_QC\QC_REPORT.md L212/L216/L250 and 04_QC\QC_R2_TARGETED_REPORT.md L30 —
  S0 input-identity fail-closedness and the audited CODE's error path ("the error path stores
  0, i.e. fail-closed"), not the pin validator. (d) 00_CONTROL\PREFLIGHT.md L39,
  PREFLIGHT_EXPECTED.md L37, RUN_CONTRACT.md L180, DESKTOP_CORRECTION_R1 control files —
  input-identity/gate fail-closedness of other phases (historical control docs).
  (e) 00_CONTROL\QC_R4_CORRECTION_R1_20261002\* — the current contract and the frozen erratum,
  which correctly describe the defect and the repair. NO current-state document claims the
  QC-R3 pin-coverage logic was fail-closed.
- "every row triple-verified" / "remains NOT_CHECKED" hits: ONLY in preserved historical
  records — 06_REPORT\PE_MASTER_REVIEW.md L20-L21 (the COVERAGE closing claim) and L32 (the
  CLAIM_MATRIX header), the BEFORE copy 00_CONTROL\DESKTOP_CORRECTION_R1\BEFORE\06_REPORT\
  PE_MASTER_REVIEW.md L18, the historical 06_REPORT\AMEND_LOG_R1.md L178 (a different,
  original-run QC lineage claim), and AUDIT_ENTRYPOINT.md L58 (a historical LATEST RUNS row
  about the 296445 NIF bbox recompute — a different package/claim). All are historical
  records; the first three are exactly the overclaims superseded by
  00_CONTROL\QC_R4_CORRECTION_R1_20261002\ERRATUM_CONTENT_FROZEN.md (S-1, S-2, section 5
  rule, section 6 per-row lineages). NO current-state file restates them as current truth;
  per the contract, NO historical file was edited.
- File-count staleness: 06_REPORT\REPORT.md L111-L116 ("Package counts ... freshly measured
  at the DESKTOP_CORRECTION_R1 executor close", with the explicit POST-CLOSE GROWTH note that
  the QC-R3 round added artifacts and later phases add more) and 06_REPORT\HANDOFF.md L74/L86/L205
  (dated delivery-census counts) — dated records that already disclose later-phase growth;
  the QC-R4 additions are exactly such a later phase; NO LIVE contradiction introduced by
  this correction; REPORT.md/HANDOFF.md NOT edited.

## 6. P3 — procedural deviation record (RUN_CONTRACT §7, transcribed)

The original DESKTOP_CORRECTION_R1 persistence sequence REGENERATED THE PACKAGE MANIFEST
BEFORE the applicable AUDIT_ENTRYPOINT.md edit — inverting the correction contract's step
order (contract §10: step 9 entrypoint update BEFORE step 10 final manifest regeneration).
This did NOT invalidate the package manifest bijection, because AUDIT_ENTRYPOINT.md is a
repo-root tracked file OUTSIDE the package-manifest scope (every MANIFEST_SHA256.csv row is a
package-relative path; the manifest does not and cannot cover the entrypoint). Recorded as
P3 / PROCEDURAL_DEVIATION, nonblocking. Literal original compliance with contract step 9 ->
step 10 is NOT claimed. The historical records (AMEND_LOG §11, HANDOFF FINALIZED STATE) stand
byte-unchanged as the historical presentation of that sequence; the erratum (frozen content
section 8) is the corrective record. THIS correction's persistence sequence (persistence
phase, not executed by this executor) applies the corrected order literally: entrypoint
pointer update BEFORE the final manifest regeneration.

## 7. Persistence-phase artifacts NOT written by this executor (honest scope statement)

The following are PERSISTENCE-PHASE artifacts per RUN_CONTRACT §6/§10 and were NOT written by
this executor: 06_REPORT\PE_MASTER_COVERAGE_ERRATUM_R1.md (materialized VERBATIM from
00_CONTROL\QC_R4_CORRECTION_R1_20261002\ERRATUM_CONTENT_FROZEN.md, with ONLY its section 7
LATER_PERSONAL_SOURCE_REVIEW rows finalized from the PE-MASTER verbatim record);
06_REPORT\PE_MASTER_REVIEW_QC_R4_R1.md; the AUDIT_ENTRYPOINT.md package-row update; the FINAL
package manifest regeneration; the commit/push. The frozen erratum content itself
(15,766 B, SHA256 7B4CF13EC65BF5A2853B07A6AD1190F2185E81D2FB56A337F1F2FA87C8BF3CE8 per the
formalizer's record) was PE-MASTER-authored and formalizer-persisted BEFORE this executor
session; this executor verified its existence and handled the §8 sweep against it but wrote
neither it nor any of the persistence artifacts.

## 8. Status fields (unchanged by this correction)

- SCIENCE_STATUS = UNCHANGED (this run is a bounded non-science correction: QC validator
  repair + regressions + review-coverage erratum only).
- RUN_STATUS = CONSUMER_UNREACHED (unchanged).
- DOWNSTREAM_CONSUMER_IDENTIFIED = NO (unchanged; no consumer search performed).
- FINAL_SEMANTIC_STATUS = UNVERIFIED (unchanged; STATIC-ONLY).
- CORRECTED_SELECTED_READER = CONFIRMED_STATIC (unchanged; the historical 185/185 pin
  result under valid inputs stands — the repaired defect was LATENT under those inputs).
- CANONICAL_GATE_EFFECT = NONE; Q1_STATUS_CHANGED = NO; M1/M2/M3_CHANGED = NO.
- F1_STATUS = REPAIR_EXECUTED_AND_BOTH_REGRESSIONS_PASS (closure of F1 requires the fresh
  internal QC + PE-MASTER final audit per the run contract; not claimed closed by the executor).

## 9. Hygiene (executor close)

- __pycache__: 0 directories anywhere under the package (walk verified after ALL runs);
  bytecode disabled in every script (sys.dont_write_bytecode first statements) and
  PYTHONDONTWRITEBYTECODE=1 in every subprocess environment and every shell invocation.
- Write scope: this executor wrote ONLY inside 04_QC\QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM\
  (13 files: 3 qc_tools sources, 4 fixture artifact copies + FIXTURE_DIFF.json, 2 regression
  results, QC_R4_REGRESSIONS_SUMMARY.json, SOURCE_IDENTITY_AND_CHANGES.md, this report).
  Disk-vs-manifest census: 436/436 manifest rows match disk size+SHA; 17 files on disk
  beyond the manifest = the 4 formalizer control files (00_CONTROL\QC_R4_CORRECTION_R1_20261002\,
  pre-existing before this session) + these 13 revision files; 0 files outside the two
  authorized new dirs. TEMP self-checks wrote only under
  C:\Users\User\AppData\Local\Temp\opencode (outside the repo).
- Historical artifacts byte-unchanged (re-hash sweep at executor close): qc3_q1_pinverify.py
  == C354E559B99411DB3AD926577B4C6C8DF5A287B3D19C47B2832BCBC104089F0F (18,199 B);
  qc3_pe32_x86.py == FE0C2F2BEC51504C6A332DCE6C0C54B872A9F32D05D7242D897F5B4E4C819DD6
  (20,432 B); the four canonical inputs == their CONTRACT_FREEZE hashes (D488D534... 39,607 B /
  67956FD1... 12,753 B / AF0E2657... 10,889 B / 2E0BEA3D... 23,482 B);
  06_REPORT\PE_MASTER_REVIEW.md == 5EF8B22729F4076D6036A0AB51698239B012C025C0D7AAC0FE1912AFCDD882EB
  (20,795 B); 06_REPORT\MANIFEST_SHA256.csv ==
  4967DAC7C22666962B2EFD39D70FE37711CCAD089D670A93CBD3C6EAE7E87DD5 (61,150 B; 439 raw lines =
  1 header + 436 data + 1 blank + 1 NOTE; every data row parses as exactly 5 CSV fields);
  PLUS the full 436/436 manifest-row bijection re-hash above (covers ALL QC-R3 sources and
  outputs and every other package file).
- The 5 pre-existing untracked groups untouched (never written; root mtimes predate this
  session): PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001, PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914,
  PE_935_P1_CLOSURE_EXTERNAL_QC_20260930, PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928,
  experiments\.
- Git state at executor close: HEAD == 2b381b32b39d0939b0637ab0cf52419ca2eb4fa8; tracked
  modifications 0; staged 0; untracked = exactly the 5 pre-existing groups + the two new
  QC-R4 dirs. NO git operation performed (read-only status/diff/rev-parse only).
- The pinned EXE D:\Eudoria_Reconstruction\pcg_install\Entropia.exe was read as a static
  file only (8,015,872 B, SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
  — re-measured by the validator at the start of BOTH regressions; MATCH). Never launched.

## 10. Executor SELF_CHECK against the gates (RUN_CONTRACT §11) — SELF_CHECK, NOT the
    independent internal-QC/PE-MASTER audit

- **R4-G0_BASELINE: PASS.** Every baseline pin re-measured by this executor before any
  package edit (STEP 0): HEAD 2b381b32... MATCH; git working tree = the 5 pre-existing
  untracked groups + the new 00_CONTROL\QC_R4_CORRECTION_R1_20261002\ dir MATCH; manifest
  SHA 4967DAC7... MATCH; original validator C354E559... MATCH; the four positive-input
  hashes MATCH (== CONTRACT_FREEZE); EXE E7785430.../8,015,872 B MATCH; QC-R4 revision root
  did NOT exist (fresh-run rule) MATCH.
- **R4-G1_REPAIR: PASS (executor self-assessment; independent full-source verification
  assigned to the fresh internal QC + PE-MASTER).** The repaired validator implements
  R1-R12 exactly as specified (line-referenced mapping in SOURCE_IDENTITY_AND_CHANGES.md §3;
  the ONLY behavioral changes are the enumerated R-items; no requirement weakened or
  dropped). Deviation notes recorded honestly (§4 of that file) — none weakens a requirement.
- **R4-G2_POSITIVE_REGRESSION: PASS.** Every §4 expected value reproduced exactly AND
  exit code 0 (table in §2 above).
- **R4-G3_INVALID_VA_REGRESSION: PASS.** Every §5 expected value reproduced exactly AND
  exit code 1 (nonzero) AND exactly one FAILED row AND the reproduced fail-open case
  REJECTED (table in §3 above).
- **R4-G4_BIJECTION: PASS.** Identity-set bijection input<->result rows verified in BOTH
  runs by TWO independent checks (the validator's self-check and the harness's own
  re-derivation from the input dirs): 185/185, no duplicates, no drops, FAILED row included.
- **R4-G5_ISOLATION_AND_HYGIENE: PASS.** No writes outside the authorized paths (census in
  §9); QC-R3 sources/outputs and all historical artifacts byte-unchanged (full 436/436
  manifest re-hash + the named re-hashes); the 5 untracked groups untouched; no __pycache__
  anywhere under the package; no EXE/VFS payload bytes in the fixture (derived audit
  evidence only); bytecode disabled in all runs.
- **R4-G6_ERRATUM: NOT_EXECUTED_BY_THIS_EXECUTOR (persistence-phase gate).** The erratum
  DOCUMENT (06_REPORT\PE_MASTER_COVERAGE_ERRATUM_R1.md) is materialized in the persistence
  phase from the frozen PE-MASTER content; the executor verified the frozen content exists
  (it separates lists A-E, corrects exactly the two overclaims S-1/S-2, records P3, and
  carries LATER_PERSONAL_SOURCE_REVIEW only as persistence-phase-finalized rows) and swept
  the package against it (§5 above), but does NOT claim this gate closed.
- **R4-G7_PERSISTENCE: NOT_EXECUTED_BY_THIS_EXECUTOR (persistence-phase gate; assigned to
  pe-master-auditor after the PE-MASTER final audit).**

## 11. Honest deviations and in-run corrections (nothing hidden)

1. First harness execution: both regressions produced all expected values, but MY harness
   byte-level self-check predicate was wrong (it required 10 changed bytes; "0x00977807" ->
   "0xFFFFFFFF" share the "0x" prefix, so exactly 8 bytes change). Harness predicate fixed;
   fixture + BOTH regressions + summary regenerated wholesale. The validator was not touched.
2. After the second execution, self-review found the repaired validator never incremented
   the new per-artifact "processed" counter (showed 0 while claimed/verified_ok/error were
   correct). Validator fixed (+3 lines); fixture + BOTH regressions + summary regenerated
   wholesale again. The final identities and the tables above are the post-fix state.
3. My NC-1 self-check script initially expected four per-artifact missing-file errors; the
   actual (correct) fail-closed behavior catches the directory form earlier, in
   resolve_inputs, with ONE input_resolution error listing all four missing artifacts. The
   self-check expectation was corrected; the validator was not changed. All three NC
   self-checks pass.
4. No deviation from RUN_CONTRACT §3 layout: all 13 revision files exist as specified;
   INTERNAL_QC\ was NOT created (it belongs to the separate fresh-QC session).

END OF REPORT.

## 12. PERSISTENCE-PHASE DISPOSITION RECORD (appended by pe-master-auditor under the PE-MASTER final order, before the final manifest regeneration)

- Fresh internal QC (04_QC\QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM\INTERNAL_QC\QC_R4_INTERNAL_QC_REPORT.md): verdict PASS_WITH_FINDINGS — 4xP3 notational findings; every gate R4-G0..R4-G6 PASS; the F1 repair verified end-to-end by its independent re-execution (byte-identical results: POSITIVE 4FD61642..., INVALID_VA 060C5BEA...).
- PE-MASTER adjudication of the 4xP3: P3-1 (this report §11.4 miscount "all 12 revision files"; 13 exist) ACCEPTED + FIXED by the disposition edit of this phase (that one clause corrected to 13; no other change to the executor-time content of this report; the pre-edit identity: 21,628 B / SHA256 4A32231F80E7F440BA236D3379BB152AB027039ECFBA432D26424FCB776C03A7; the post-edit identity is carried by the final manifest and the PE-MASTER terminal delivery — a file cannot contain its own post-edit hash). P3-2 (SOURCE_IDENTITY_AND_CHANGES.md §3 change-map line ranges drift by up to ~4 lines; the mapped CONTENT machine-verified correct by the internal QC's Q1_R11_MACHINE_COMPARISON_RESULT.json) RECORDED, no package edit — the internal QC's machine comparison is the precise mapping record. P3-3 (qc4_q1_pinverify.py: the enumerate_artifact_pins call sits outside the artifact_load try/except — a non-object JSON root would crash the process; the OUTCOME remains fail-closed: nonzero exit, no result file, no false PASS; unreachable for the four canonical dict-root artifacts) RECORDED, no edit — changing the audited validator now would invalidate the triple re-execution evidence (executor + internal QC byte-identical + PE-MASTER own counter-check). P3-4 (dead assignment qc4_regression_runner.py L430, immediately overwritten by the L453 predicate) RECORDED, no edit (zero behavioral effect; same regeneration rationale).
- PE-MASTER final verdict for this correction: MASTER_ACCEPTED (advisory; ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT = NONE) — persisted verbatim in 06_REPORT\PE_MASTER_REVIEW_QC_R4_R1.md.
- Persistence sequence (this phase, in the CORRECTED order per the P3 record): the erratum 06_REPORT\PE_MASTER_COVERAGE_ERRATUM_R1.md materialized VERBATIM from 00_CONTROL\QC_R4_CORRECTION_R1_20261002\ERRATUM_CONTENT_FROZEN.md with ONLY its section 7 (LATER_PERSONAL_SOURCE_REVIEW) placeholder rows replaced by the PE-MASTER verbatim record; the review 06_REPORT\PE_MASTER_REVIEW_QC_R4_R1.md written verbatim per the PE-MASTER final order; the factual AUDIT_ENTRYPOINT.md package-row update applied BEFORE the final manifest regeneration (the corrected order — the original DESKTOP_CORRECTION_R1 persistence had inverted it; see the P3 record in the erratum §8 and this report §6); the FINAL package MANIFEST regenerated LAST (self-excluded; quoted NOTE row; every data line exactly 5 CSV fields); bijection verified; staged census verified against the manifest; proprietary-payload/secret scan run; ONE normal new commit; push; live remote equality verified. The commit SHA and the push/remote receipts are reported in the PE-MASTER terminal delivery (outside the finalized package; a file cannot carry its own commit's SHA).
