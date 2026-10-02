# PE_MASTER_COVERAGE_ERRATUM_R1 — PE-MASTER REVIEW COVERAGE SUPERSESSION / ERRATUM

- Target of supersession: the historical 06_REPORT\PE_MASTER_REVIEW.md AS COMMITTED at
  2b381b32b39d0939b0637ab0cf52419ca2eb4fa8 (the DESKTOP_CORRECTION_R1 review). That file is
  PRESERVED byte-unchanged as historical evidence; this erratum is the supersession record.
- Issued by: PE-MASTER (advisory; ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT = NONE).
- Correction run: PE_935_20002_PAYLOAD30_QC_R4_FAIL_CLOSED_CORRECTION_R1_20261002
  (human order 2026-10-02: TARGET_SHA 2b381b32...; DESKTOP_POST_AUDIT_VERDICT =
  REQUIRE_CORRECTIONS; scope = QC VALIDATOR REPAIR + REVIEW COVERAGE ERRATUM ONLY).
- Cause: the independent ChatGPT Desktop post-audit of 2b381b32 — finding F2 (PE-MASTER
  coverage erratum) together with F1 (the QC-R3 Q1 pin-verification validator's fail-open
  defect, repaired in 04_QC\QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM\).

## 1. SUPERSEDED AS WORDED (exactly two coverage claims)

S-1. The historical review's COVERAGE closing claim — "NO load-bearing generator, validator,
     gate predicate, current-state pointer or physical source remains NOT_CHECKED." —
     SUPERSEDED_AS_WORDED. At the time of that review the QC-R3 tool sources had NOT been
     reviewed line-by-line by PE-MASTER; the review's own preceding bullet recorded this
     honestly. The QC-R3 pin validator qc3_q1_pinverify.py (SHA256
     C354E559B99411DB3AD926577B4C6C8DF5A287B3D19C47B2832BCBC104089F0F) IS a load-bearing
     validator (its 185/185 census is cited by the review), and its source was
     NOT_CHECKED_PERSONALLY at the historical review. The universal-negative claim was an
     overclaim that contradicted the review's own disclosure in the same section. The same
     overclaim pattern also appears in the preserved pre-correction review copy
     (00_CONTROL\DESKTOP_CORRECTION_R1\BEFORE\06_REPORT\PE_MASTER_REVIEW.md, its COVERAGE
     closing bullet) and is superseded there by the same logic; the BEFORE copy itself stays
     byte-unchanged as historical evidence.
S-2. The historical review's CLAIM_MATRIX header — "load-bearing rows of the CORRECTION;
     every row triple-verified — executor pins + QC-R3 independent re-verification +
     PE-MASTER own byte reads" — SUPERSEDED_AS_WORDED. "Triple-verified" is accurate only
     where all three lineages are complete for that row. The honest per-row lineages are
     restated in section 6 below. Rows 1/2/4/5/8 have three complete lineages; rows 3/6/7
     have executor + QC-R3 complete with PE-MASTER at spot-match level only; row 9 rests on
     the bounded 202-site census that QC-R3 explicitly did not re-execute and of which
     PE-MASTER personally examined only 2 of 202 call-site contexts.

## 2. WHAT REMAINS SUPPORTED (not retracted by this erratum)

Every MEASURED claim of the historical review: the byte pins, the branch-selection proof,
the cursor and destination proofs, the QC-R3 machine results under the valid inputs actually
present (185/185 pins; 51/51 semantic assertions), the starting/final manifest bijection
verifications, the gate dispositions, the retraction records, and the SUPERSESSION NOTICE
regarding the pre-correction selected-reader claim. The F1 fail-open defect (fixed in QC-R4)
was LATENT under those valid inputs: it does not invalidate the historical 185/185 result;
it invalidates the implicit fail-closedness assumption for malformed/unmapped pins (Desktop
counterexample reproduced and REJECTED by the repaired validator in QC-R4 Regression B).

## 3. WHAT BECOMES UNKNOWN (retraction-opposite firewall; no auto-promotion of the opposite)

The fail-closedness of the OTHER six historical QC-R3 tool sources (qc3_pe32_x86.py,
qc3_q0_identity.py, qc3_q2_branch_model.py, qc3_q3_vfs_walk.py, qc3_q4_before_copies.py,
qc3_q5_wording_sweep.py) is NOT re-audited by this correction: their sources remain
NOT_CHECKED_PERSONALLY beyond what is recorded in section 7 (LATER_PERSONAL_SOURCE_REVIEW).
No claim is made that they are defect-free; no claim is made that they are defective.
(Retracting the "no load-bearing validator NOT_CHECKED" claim does NOT confirm that any
validator is defective — only qc3_q1_pinverify.py has a CONFIRMED, repaired defect.)

## 4. THE HISTORICAL COVERAGE, RE-CLASSIFIED (five honest lists; nothing here upgrades what was done)

### A. PERSONAL_FULL_READ (by the historical PE-MASTER session, per its own coverage record)
1. 00_CONTROL\DESKTOP_CORRECTION_R1\CORRECTION_RUN_CONTRACT.md (308 lines; 21,076 B;
   SHA256 1E592EBC056FD4110EB8151C92872DDBEF744755FF3AAB50C1A87CAFFABFE557).
2. 00_CONTROL\DESKTOP_CORRECTION_R1\PRE_CORRECTION_STATE.md (SHA256
   8602EDB628D5D34206B4B34250BB22CE9E96E82FA212C5D1684C40DDEE0C1B7B).
3. ALL 10 corrected documents post-correction: 02_ANALYSIS\FIELD_TO_DESTINATION_TRACE.md;
   CONSUMER_TRACE.md; SEMANTIC_ASSESSMENT.md; NEGATIVE_CONTROLS.md; BLAST_RADIUS.md;
   VFS_TO_PARSER_TRACE.md; DESTINATION_CONSUMER_CENSUS.json; 06_REPORT\REPORT.md;
   EVIDENCE_INDEX.md; HANDOFF.md.
4. 06_REPORT\AMEND_LOG_DESKTOP_CORRECTION_R1.md (the executor-close state as it stood at the
   review; the persistence-phase section 11 append postdates the review's read).
5. The two load-bearing correction generators, in full source:
   03_SCRIPTS\desktop_correction_r1\pe_parse.py; 03_SCRIPTS\desktop_correction_r1\s2_branch_pins.py.

### B. PERSONAL_PHYSICAL_RECOMPUTATION (own byte reads / own measurements by the historical session)
1. Own PE-header/section reads of the pinned Entropia.exe.
2. READ bytes 8B 04 10 at file offset 0x577807 (VA 0x00977807); STORE bytes 89 02 at file
   offset 0x577810 (VA 0x00977810).
3. The FUN_009777F0 cursor-reader window (flag check [cursor+0x11]; bounds offset+4<=limit;
   base load; read; dest arg; advance-4 CALL FUN_0040de60).
4. The FUN_0075F660 dispatch structure — the full byte sequence 8B C1 8B 08 85 C9 53 56 8B
   74 24 0C B3 01 74 17 8B 54 24 10 8B 01 8B 40 14 52 56 FF D0.
5. The registration window 0x7616F0-0x761727 (CALL FUN_00977a50; PUSH EAX arg5; PUSH 0;
   PUSH 0xC0; PUSH 1; PUSH 0x11; MOV ECX,ESI; CALL FUN_0070cbc0).
6. The factory FUN_00977a50 (lazy-init singleton: TEST byte [0xBA9380]; MOV dword
   [0xBA937C],0x00A9C670; MOV EAX,0x00BA937C; RET — non-NULL on both paths).
7. The vtable 0x00A9C670 slot dump (slot +0x14 = dword 0x009777F0 at file offset 0x69C684).
8. The RTTI pointer [vtable-4] = 0x00AB8360.
9. The fallback reader window at file offset 0x12540 (read 8B 04 10 @0x12553, store 89 02
   @0x1255A) — BYTE-CORRECT; reachability condition descriptor+0==NULL.
10. The static object image at 0x7A937C (zeroed in the file image — BSS-tail; the vtable is a
    RUNTIME store, reasoned from the pinned factory bytes).
11. The starting-manifest bijection re-hash: 388/388 file rows size+SHA identical; 0 missing;
    0 extra; disk == 388 covered + the manifest itself; the manifest NOTE row identified.

### C. PERSONAL_SPOT_CHECK (QC-R3 outputs spot-matched by the historical session; NOT personally re-executed)
1. QC-R3's 185/185 pin census (own PE32/x86 toolchain) — spot-matched.
2. The A/B/C discriminating branch-selection detector (NULL->FALLBACK; non-NULL->VIRTUAL;
   synthetic slot->changed target; all 3 mutant models DETECTED) — spot-matched.
3. The independent VFS walk (1366 records; 16+1366*128 == 174,864 exact EOF; cursor +0x30 at
   tag ID 17 in 1366/1366; record 0 = BB 2E 00 00 = 11963; record 1014 = 0; zeros exactly
   [1014, 1015]) — spot-matched.
4. The BEFORE-copy verification 10/10 == the starting manifest rows — spot-matched.
5. The wording sweep (148 high-risk hits reviewed; the 2 flagged P2 clauses fixed in
   disposition) — spot-matched.
6. The REPORT §18 key census 46/46 — spot-matched.

### D. DELEGATED_INDEPENDENT_QC (executed by the fresh QC-R3 pe-master-auditor session; NOT by PE-MASTER personally)
1. Q0 identity + the 388-row bijection re-hash + protected-file census.
2. Q1 the 185-pin census + 51 semantic assertions + 19 decode windows (tools:
   qc3_q1_pinverify.py + qc3_pe32_x86.py — the F1 defect carrier, repaired in QC-R4).
3. Q2 the A/B/C branch-selection detector + 3 mutants (tool: qc3_q2_branch_model.py).
4. Q3 the independent VFS framing walk + 2 negative controls + destination derivation
   (tool: qc3_q3_vfs_walk.py).
5. Q4 the BEFORE-copy + AMEND_LOG verification (tool: qc3_q4_before_copies.py).
6. Q5 the wording sweep (tool: qc3_q5_wording_sweep.py).
7. Q6 the persistence-phase file untouched checks.
   QC-R3 toolchain identities (byte-unchanged at erratum issue): qc3_pe32_x86.py
   FE0C2F2BEC51504C6A332DCE6C0C54B872A9F32D05D7242D897F5B4E4C819DD6; qc3_q0_identity.py
   FB1588821B0A13AA947896AC6D141D4CA7E37978101E913CEDCC312D90B80A17; qc3_q1_pinverify.py
   C354E559B99411DB3AD926577B4C6C8DF5A287B3D19C47B2832BCBC104089F0F; qc3_q2_branch_model.py
   66B175156FCB6D34B45B026C4AFF7C5CCE131121A61146301D5BED8E2917C1B1; qc3_q3_vfs_walk.py
   E6C68C45267398FE080C253D9638C80E7E60F78DA547E62339B217BD0D86D2BE; qc3_q4_before_copies.py
   531142AFABC6CF2D133F69AD432E16E5AB285892C8DE4A21E1DB7F9218CB0381; qc3_q5_wording_sweep.py
   B0FE268C427A91B9CC135EB0755035D88E39E50B7017E219945D0758B92DDFC2.

### E. NOT_CHECKED_PERSONALLY (at the historical review)
1. The QC-R3 tool sources, line-by-line — ALL SEVEN (identities in list D), including
   qc3_q1_pinverify.py, the load-bearing pin validator and F1 defect carrier (verification
   exceptions appended to errors[] without a pin result row; denominator = len(pins);
   overall_ok not requiring errors==0 nor comparing against the input-pin count).
2. PARTIAL reads recorded as partial, NOT full: 01_RAW\DESKTOP_CORRECTION_R1\
   BRANCH_SELECTION_TRACE.json (head + structure + section table only); the QC-R3 report
   (verdict/gates/coverage sections + machine-result summaries only).
3. The ~180 PASS15 call-site contexts beyond the 2 examined candidates (of the 202-site
   consumer census; original-run evidence; its denominator reproduced in the ORIGINAL
   audit's QC rounds, not personally re-walked).
4. Re-execution of the executor's 11 correction scripts (reproducibility, not independence;
   outputs verified against physical bytes by QC-R3 + PE-MASTER spot reads).
5. A personal full VFS byte-level walk (the VFS numbers are QC-R3-covered + spot-matched —
   list C — not personally re-walked).
6. Runtime behavior (STATIC-ONLY; the client was never launched by any party).
7. The historical QC round 1/2 tool sources (original-run historical artifacts, outside the
   R1-correction review's declared scope; recorded here for completeness of the honest
   coverage state).

## 5. COVERAGE-CLAIM RULE (henceforth)

Do not state "every row triple-verified" unless every row genuinely has all three complete
lineages; do not state "no load-bearing validator remains NOT_CHECKED" while any
load-bearing validator source is NOT_CHECKED_PERSONALLY.

## 6. PER-ROW LINEAGE CORRECTION (supersedes the "every row triple-verified" header)

| Row | Claim | Executor | QC-R3 independent | PE-MASTER personal | Verdict on "triple" |
|---|---|---|---|---|---|
| 1 | tag-ID-17 registration window | BRANCH_SELECTION_TRACE §A pins | own decode | OWN BYTE READS (B5) | THREE COMPLETE LINEAGES |
| 2 | factory FUN_00977a50 non-NULL return | pins | own decode | OWN BYTE READS (B6) | THREE COMPLETE |
| 3 | descriptor+0 dataflow (FUN_0070cbc0 -> FUN_0075f5c0 @0x75F5CA -> table insert) | pins | own decode (Q1 chain items 3-5) | SPOT-MATCH ONLY | TWO COMPLETE + SPOT-MATCH |
| 4 | FUN_0075F660 branch selection (TEST/JZ; virtual slot) | pins | own decode | OWN BYTE READS (B4) | THREE COMPLETE |
| 5 | vtable dword @0xA9C684 = 0x009777F0; RTTI .?AUArkRTTraitsInt@@ | pins | own read | OWN BYTE READS (B7/B8) | THREE COMPLETE |
| 6 | cursor == payload+0x30 (record 0 = 11963; record 1014 = 0; 1366/1366) | CURSOR_PROOF walk | independent VFS walk | SPOT-MATCH ONLY (C3) | TWO COMPLETE + SPOT-MATCH |
| 7 | destination value-array slot 21 (+0x54) | DESTINATION_PROOF 23/23 | Q3 derivation | SPOT-MATCH ONLY | TWO COMPLETE + SPOT-MATCH |
| 8 | fallback classification (FUN_00412540 @0x12553/0x1255A non-selected) | FALLBACK_PATH_RECORD 25/25 | own decode | OWN BYTE READS (B9) | THREE COMPLETE |
| 9 | DOWNSTREAM_CONSUMER_IDENTIFIED = NO (bounded 202-site census) | original-run census | NOT re-executed by QC-R3 (its own NOT_CHECKED disclosure) | 2 of 202 contexts personally (~180 not) | ONE FULL EXECUTION + HISTORICAL QC REPRODUCTION + PARTIAL PERSONAL |

## 7. LATER_PERSONAL_SOURCE_REVIEW (performed NOW; NOT retroactively attributable to the historical review)

The checks in this section are performed NOW, in this correction run
(PE_935_20002_PAYLOAD30_QC_R4_FAIL_CLOSED_CORRECTION_R1_20261002), and CANNOT be
retroactively attributed to the historical audit at 2b381b32.

LATER_PERSONAL_SOURCE_REVIEW = YES for the items actually completed, recorded below with
scope, reviewer and timestamp. [FINALIZED IN THE PERSISTENCE PHASE FROM THE PE-MASTER
VERBATIM RECORD. If an item was NOT completed, its honest NOT_CHECKED status is preserved
and unrestricted review closure is NOT claimed.]

- 04_QC\QC_R3_DESKTOP_CORRECTION\qc_tools\qc3_q1_pinverify.py (the ORIGINAL validator source,
  SHA256 C354E559B99411DB3AD926577B4C6C8DF5A287B3D19C47B2832BCBC104089F0F, 308 lines) — read
  through EOF by PE-MASTER at this correction's baseline (2026-10-02) to confirm the F1
  defect directly in the source: exception path without a pin result row; denominator =
  len(res["pins"]); overall_ok without errors==0 and without the ORIGINAL_INPUT_PIN_COUNT
  comparison; no exit-code logic. This is a LATER check, not a historical one.
- 04_QC\QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM\qc_tools\qc4_q1_pinverify.py (the REPAIRED validator;
  SHA256 345D69FA6CEC60590F79B97FFE73F29538BEAF6704C5A5B9F7D14192DB8157A8; 30,772 B; 548 lines)
  — read through EOF by PE-MASTER in this correction run's master audit (2026-10-02):
  requirements R1-R12 verified line-by-line against the frozen contract (R1 L196; R2/R3
  L198-248; R4 L487-498; R5 L544; R8 L121-136 + L252-257; R9 L60-88; R10 L148-195; R11
  verification semantics identical to the original; R12 L37-38). LATER CHECK — not
  attributable to the historical review.
- 04_QC\QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM\qc_tools\qc4_pe32_x86.py (the PE helper copy;
  SHA256 FE0C2F2BEC51504C6A332DCE6C0C54B872A9F32D05D7242D897F5B4E4C819DD6; 20,432 B;
  520 lines — verified BYTE-IDENTICAL to the historical qc3_pe32_x86.py by PE-MASTER's own
  hash comparison, so this read-through-EOF is a full read of the historical helper's
  bytes) — read through EOF by PE-MASTER in this correction run (2026-10-02). LATER CHECK —
  the historical helper source was NOT personally reviewed at the historical review; this
  later read is recorded as what it is and does not retroactively close the historical gap.
- 04_QC\QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM\qc_tools\qc4_regression_runner.py (the regression
  harness; SHA256 E8B01077AE5AD31259FA16CAC27B00A6723F02A99D8EB4C0896E9E531E33DCE5; 27,271 B;
  536 lines) — read through EOF by PE-MASTER in this correction run (2026-10-02): the fixture
  build (pre-mutation hash verification, exactly-one selector, length-preserving single-field
  splice, byte-level + recursive-JSON machine-checked diff), the subprocess execution with
  captured exit codes, the per-field expected-value verification and the independent PASS
  predicates verified line-by-line. LATER CHECK.
- PE-MASTER OWN EXECUTION COUNTER-CHECK (AUDITOR_COUNTERCHECK; outputs under
  C:\Users\User\AppData\Local\Temp\opencode\pe_master_qc4_countercheck\ — OUTSIDE the project
  tree, NOT project evidence): BOTH regressions independently re-executed by PE-MASTER with
  own output paths (POSITIVE: exit 0, 185/185 verified, 0 errors/mismatches, denominator 185,
  bijection OK, 51/51 semantic assertions, overall_ok true; INVALID_VA: exit 1, 185
  input/184 verified/1 FAILED row retained in denominator 185, overall_ok false, the FAILED
  row's pin_id/source/original VA string/error retained); own recursive JSON diff of the
  fixture = exactly one changed leaf (pins[74].va "0x00977807" -> "0xFFFFFFFF"); own fixture
  pin census = 185. LATER CHECK (2026-10-02).

## 8. P3 — PROCEDURAL DEVIATION RECORD (terminal order; nonblocking historical fact)

The original DESKTOP_CORRECTION_R1 persistence sequence REGENERATED THE PACKAGE MANIFEST
BEFORE the applicable AUDIT_ENTRYPOINT.md edit — inverting the correction contract's step
order (contract §10: step 9 entrypoint update BEFORE step 10 final manifest regeneration).
This did NOT invalidate the package manifest bijection, because AUDIT_ENTRYPOINT.md is a
repo-root tracked file OUTSIDE the package-manifest scope (every MANIFEST_SHA256.csv row is
a package-relative path; the manifest does not and cannot cover the entrypoint). Recorded
here as P3 / PROCEDURAL_DEVIATION. Literal original compliance with contract step 9 ->
step 10 is NOT claimed. The historical records (AMEND_LOG §11, HANDOFF FINALIZED STATE)
stand byte-unchanged as the historical presentation of that sequence; this erratum is the
corrective record. The QC_R4_FAIL_CLOSED_CORRECTION persistence sequence applies the
corrected order literally: entrypoint pointer update BEFORE the final manifest regeneration.

## 9. WHAT THIS ERRATUM DOES NOT CHANGE

SCIENCE_STATUS = UNCHANGED. CORRECTED_SELECTED_READER = CONFIRMED_STATIC (FUN_009777F0;
READ VA 0x00977807 / FO 0x00577807 / 8B 04 10; STORE VA 0x00977810 / 89 02; cursor
payload+0x30 in 1366/1366; destination ArkParameterArmor value-array slot 21 / +0x54).
DOWNSTREAM_CONSUMER_IDENTIFIED = NO. FINAL_SEMANTIC_STATUS = UNVERIFIED.
WORLD_INSTANCE_TO_MODEL_EDGE = NOT_TESTED. PLACEMENT_XYZ_RECOVERED = NO.
CANONICAL_GATE_EFFECT = NONE. Q1_STATUS_CHANGED = NO. M1/M2/M3_CHANGED = NO.
The historical verdict string, the status algebra, the retraction records and the QC-R3
machine results under valid inputs stand as historical evidence with the coverage
corrections above.
