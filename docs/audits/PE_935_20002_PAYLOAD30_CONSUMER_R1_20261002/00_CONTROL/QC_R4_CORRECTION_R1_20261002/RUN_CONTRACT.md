# RUN_CONTRACT — PE_935_20002_PAYLOAD30_QC_R4_FAIL_CLOSED_CORRECTION_R1_20261002

Contract class: ONE bounded QC/review correction of the existing run package PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002, per the human order 2026-10-02 (TARGET_SHA 2b381b32b39d0939b0637ab0cf52419ca2eb4fa8; DESKTOP_POST_AUDIT_VERDICT = REQUIRE_CORRECTIONS; SCOPE = QC VALIDATOR REPAIR + REVIEW COVERAGE ERRATUM ONLY). NO new RE. NO Ghidra. NO new EXE/VFS science. NO runtime. NO downstream-consumer search. NO placement experiment. NO Q1/gate/milestone advancement. NO history rewrite. ONE normal new commit at the end (persistence phase only).

Table of roles/fields:

| Field | Value |
|---|---|
| RUN_ID | PE_935_20002_PAYLOAD30_QC_R4_FAIL_CLOSED_CORRECTION_R1_20261002 (RUN_CLASS LOAD_BEARING; RUN_TYPE QC_VALIDATOR_FAIL_CLOSED_REPAIR + REVIEW_COVERAGE_ERRATUM — a bounded non-science correction) |
| DISPATCHED_BY | PE-MASTER direct; NO_NESTED_TASKS |
| EXECUTOR | pe-reconstruction (repairs the validator copy, builds fixtures, runs both regressions, writes the QC-R4 revision artifacts) |
| FRESH QC | a separate fresh-context pe-master-auditor session (audits the repair + regressions + erratum draft; writes ONLY inside 04_QC\QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM\INTERNAL_QC\) |
| PERSISTENCE | pe-master-auditor (finalizes erratum/review, entrypoint row, manifest LAST, commit, push, receipts) |
| MODE | STATIC-ONLY (the client never launches; the pinned EXE is read as a static file solely for existing pin verification) |
| BASE_SHA (authorized base) | 2b381b32b39d0939b0637ab0cf52419ca2eb4fa8 (== HEAD == live remote master at start) |
| Baseline pins | (the B4-B8 values from PREFLIGHT_QC_R4.md; the manifest SHA 4967DAC7C22666962B2EFD39D70FE37711CCAD089D670A93CBD3C6EAE7E87DD5; the original validator SHA C354E559B99411DB3AD926577B4C6C8DF5A287B3D19C47B2832BCBC104089F0F) |

## §1 F1 — THE CONFIRMED DEFECT (fail-open pin validator; P2)

Affected source (IMMUTABLE — do not edit): 04_QC\QC_R3_DESKTOP_CORRECTION\qc_tools\qc3_q1_pinverify.py (SHA256 C354E559...).

Confirmed defects:

- verification exceptions are appended to res["errors"];
- the failed pin is NOT retained in res["pins"];
- the denominator is later calculated as len(res["pins"]);
- overall_ok does not require errors == 0 and does not compare against the original input-pin count;
- therefore a malformed/unmapped pin can disappear from the denominator (fail-open).

Desktop executed counterexample: mutating only the selected READ pin VA 0x00977807 -> 0xFFFFFFFF (input still 185 pins) produced: errors = 1, claimed denominator = 184, verified_ok = 184, overall_ok = true, exit code = 0.

## §2 F1 — REQUIRED REPAIR (the repaired copy; requirements are NORMATIVE, each is a gate)

The new revision root: NEW_QC_RELATIVE_ROOT = 04_QC\QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM\ (inside the package). Keep the existing QC-R3 tool sources AND outputs byte-unchanged. Copy the validator and its PE helper into the new revision (qc_tools\qc4_q1_pinverify.py + qc_tools\qc4_pe32_x86.py) and repair the new copy only. Record the old/new source identities and the actual change (SOURCE_IDENTITY_AND_CHANGES.md: old SHA C354E559... -> new SHA; a line-referenced change list).

Repair requirements (ALL mandatory):

R1. Capture ORIGINAL_INPUT_PIN_COUNT before verification.
R2. Every input pin MUST remain represented in the result (no pin may vanish).
R3. On verification exception: create an explicit FAILED pin result row; retain source/VA/error; do not remove it from the denominator.
R4. overall_ok MUST require simultaneously: processed_count == ORIGINAL_INPUT_PIN_COUNT AND verified_ok == ORIGINAL_INPUT_PIN_COUNT AND mismatch_count == 0 AND error_count == 0 AND all semantic assertions PASS AND all required extra checks PASS.
R5. Process exit code MUST be nonzero when overall_ok == false (and zero when true).
R6. Preserve historical QC-R3 outputs unchanged (no writes anywhere under 04_QC\QC_R3_DESKTOP_CORRECTION\).
R7. Repaired-validator results are NEW QC revision artifacts (distinct POSITIVE and INVALID_VA result files inside the new revision).
R8. Give each input pin a stable source/JSON-location identity (pin_id = "<artifact-name>::<array_path>[<index>]" covering pins[] / entry_pins[] / width_sources.<key>.width_pins[]), preserved even when the VA is malformed; verify a BIJECTION between all original input pins and result rows (including failed rows) by identity sets — counters alone must not permit a dropped or duplicated result row.

Additional normative implementation requirements:

R9. The repaired validator takes EXPLICIT input and output paths (CLI arguments): --inputs (a directory containing exactly the four canonical artifact names, or the four explicit file paths) and --output (the result JSON path). It must NOT inherit or contain the old script's hard-coded QC-R3 output path. This parameterization also allows independent counter-check re-execution WITHOUT overwriting project evidence.
R10. Fail-closed at every level: missing input file, unparsable JSON, unparsable/missing pin fields (a pin without a parseable "va" is a FAILED row with the error retained — never skipped), EXE identity mismatch (the validator MUST hash the pinned EXE at start and compare to E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31; on mismatch: overall_ok=false + nonzero exit).
R11. Keep the original verification semantics otherwise IDENTICAL: same four-artifact pin loading (pins[] + entry_pins fallback + width_sources width_pins), same extra checks, same semantic windows, same semantic assertions (the POSITIVE regression must re-verify the same 185 pins + 51 semantic assertions). The ONLY behavioral changes are the fail-closed coverage repair, the pin identities, the bijection, the explicit paths, the EXE identity check, and the exit codes.
R12. Bytecode disabled: sys.dont_write_bytecode = True as the first statements of EVERY qc4 script; the regression runner also sets PYTHONDONTWRITEBYTECODE=1 for subprocesses; after all runs, verify NO __pycache__ exists anywhere under the package.

## §3 REVISION LAYOUT (exact; all paths inside the package)

```text
04_QC\QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM\
  qc_tools\qc4_pe32_x86.py          (copy of qc3_pe32_x86.py; if byte-identical, record that; any change must be justified in SOURCE_IDENTITY_AND_CHANGES.md)
  qc_tools\qc4_q1_pinverify.py      (the repaired validator)
  qc_tools\qc4_regression_runner.py (the harness: builds the fixture, verifies pre-mutation hashes, runs both regressions as subprocesses capturing exit codes, verifies the fixture diff and the bijections, aggregates QC_R4_REGRESSIONS_SUMMARY.json)
  FIXTURE_INVALID_VA\BRANCH_SELECTION_TRACE.json          (mutated fixture copy)
  FIXTURE_INVALID_VA\FALLBACK_PATH_RECORD.json            (byte-identical fixture copy)
  FIXTURE_INVALID_VA\DESTINATION_PROOF_CORRECTION_R1.json (byte-identical fixture copy)
  FIXTURE_INVALID_VA\CURSOR_PROOF_CORRECTION_R1.json      (byte-identical fixture copy)
  FIXTURE_INVALID_VA\FIXTURE_DIFF.json                    (machine-checked single-field diff record)
  POSITIVE\QC_R4_PINVERIFY_POSITIVE_RESULT.json
  INVALID_VA\QC_R4_PINVERIFY_INVALID_VA_RESULT.json
  QC_R4_REGRESSIONS_SUMMARY.json
  SOURCE_IDENTITY_AND_CHANGES.md
  QC_R4_REPORT.md
  INTERNAL_QC\ (created by the separate fresh-QC session only; the executor does not write here)
```

Fixtures and results may contain derived audit evidence ONLY. Read the pinned physical EXE solely for existing pin verification; do NOT copy any original EXE/VFS payload into the fixture or the repository. No new EXE/VFS science, no VFS reparsing.

## §4 MANDATORY REGRESSION A — POSITIVE (uses unchanged canonical artifacts, read in place at 01_RAW\DESKTOP_CORRECTION_R1\)

Expected (the run FAILS if any value differs):

```text
INPUT_PIN_COUNT = 185; processed = 185; verified_ok = 185; errors = 0; mismatches = 0; denominator = 185; result rows = 185; bijection input<->rows = OK; semantic assertions 51/51 PASS; extra checks PASS; overall_ok = true; process exit code = 0.
```

POSITIVE_REGRESSION_PASS definition: the unchanged positive control matches EVERY expected count/predicate above AND exit code 0.

## §5 MANDATORY REGRESSION B — DESKTOP INVALID-VA REPRODUCTION (separate fixture only; canonical EXE and committed evidence untouched)

Fixture build (machine-checked, all steps mandatory):

a. Copy all four positive inputs byte-for-byte into FIXTURE_INVALID_VA\.
b. BEFORE mutation, verify the four copies hash-match the positive-input hashes (§0 pins B7). Record the pre-mutation hashes.
c. Selector: in the fixture BRANCH_SELECTION_TRACE.json, select pins with va == "0x00977807" — the selector MUST identify EXACTLY ONE pin (PE-MASTER's own baseline census: exactly 1, pins[74]). If the selector matches more or fewer, the run FAILS before mutation.
d. Mutate exactly that one field: va "0x00977807" -> "0xFFFFFFFF". No other change.
e. Machine-check the difference: a recursive JSON diff between the canonical BRANCH_SELECTION_TRACE.json and the fixture copy MUST show EXACTLY ONE changed leaf (pins[74].va: "0x00977807" -> "0xFFFFFFFF"); every other pin field/value and the other three input files remain identical (hash-equal). Persist this as FIXTURE_DIFF.json.
f. Keep 185 input pin identities in the fixture (the mutation changes a value, not the structure).

Expected (the run FAILS if any value differs):

```text
INPUT_PIN_COUNT = 185; processed = 185; verified_ok = 184; failed = 1; errors = 1; mismatches = 0; denominator = 185; result rows = 185; bijection input<->rows = OK (including the FAILED row); semantic assertions 51/51 PASS; extra checks PASS; overall_ok = FALSE; process exit code != 0.
```

INVALID_VA_REGRESSION_PASS definition: the negative fixture is REJECTED with denominator 185, exactly one FAILED/error row (pin_id preserved, source + original VA string + error retained), overall_ok = false, and a nonzero exit code. The validator's failure here is a SUCCESSFUL negative regression — it must NOT label the whole correction cycle FAIL, and no process exit may be ignored.

F1 may be CLOSED only if BOTH regressions pass AND the result-row/input bijection is verified in both runs.

## §6 F2 — PE-MASTER COVERAGE ERRATUM (the erratum is PE-MASTER-authored content; normative source = 00_CONTROL\QC_R4_CORRECTION_R1_20261002\ERRATUM_CONTENT_FROZEN.md)

- The historical 06_REPORT\PE_MASTER_REVIEW.md at 2b381b32 is PRESERVED byte-unchanged as historical evidence. Do NOT rewrite it. Do NOT state "every row triple-verified" or "no load-bearing validator remains NOT_CHECKED" as current truth anywhere.
- The persistence phase materializes 06_REPORT\PE_MASTER_COVERAGE_ERRATUM_R1.md VERBATIM from ERRATUM_CONTENT_FROZEN.md, finalizing ONLY its section 7 (LATER_PERSONAL_SOURCE_REVIEW) rows from the PE-MASTER verbatim record (files, SHAs, scope read-through-EOF, timestamp). If PE-MASTER's later review is incomplete for an item, that item keeps its honest NOT_CHECKED status and unrestricted review closure is NOT claimed. The later checks are NOT retroactively attributable to the historical audit.
- This correction's PE-MASTER run verdict is persisted as 06_REPORT\PE_MASTER_REVIEW_QC_R4_R1.md (persistence phase, verbatim from the PE-MASTER final order; the historical PE_MASTER_REVIEW.md is untouched).

## §7 P3 — TERMINAL ORDER (procedural deviation record; nonblocking)

Preserve the known nonblocking historical fact: the original DESKTOP_CORRECTION_R1 persistence sequence regenerated the package manifest BEFORE the applicable AUDIT_ENTRYPOINT.md edit (inverting the contract's step 9 -> step 10 order). This did NOT invalidate package bijection because AUDIT_ENTRYPOINT.md is a repo-root tracked file OUTSIDE the package-manifest scope. Record it as P3 / procedural deviation in the erratum (section 8 of the frozen content) and in QC_R4_REPORT.md. Do NOT claim literal original compliance with step 9 -> step 10. THIS correction's persistence applies the corrected order literally: entrypoint pointer update BEFORE the final manifest regeneration.

## §8 CONTRADICTION / CURRENT-STATE SWEEP (executor; bounded, package + repo-root current-state docs)

Sweep the package and AUDIT_ENTRYPOINT.md for CURRENT-STATE claims that would contradict the QC-R4 state, specifically:

- any claim that the QC-R3 pinverify validator is fail-closed (expected hits: none in current-state docs; the QC-R3 report's own fail-closed statements about its DECODER (x86 fail-closed on unknown opcodes) are about the decoder, not the pin-coverage logic — do not touch the immutable QC-R3 report);
- any "every row triple-verified" / "no load-bearing ... NOT_CHECKED" claims OUTSIDE the preserved historical review files and BEFORE copies (those are superseded by the erratum, not edited);
- file-count/current-state claims that would become stale after the QC-R4 additions (REPORT.md's counts are dated executor-close measurements and already state that later phases add artifacts — they stand as dated records; do NOT edit REPORT.md/HANDOFF.md unless the sweep finds a LIVE contradiction introduced by this correction; if found, record it in QC_R4_REPORT.md and fix minimally with a BEFORE copy).

Expected sweep outcome: no current-state file contradicts the QC-R4 state; the overclaims live only in preserved historical records superseded by the erratum.

## §9 FRESH INTERNAL QC (separate pe-master-auditor session; writes ONLY 04_QC\QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM\INTERNAL_QC\)

Duties: re-measure the baseline pins; full-read the repaired validator + helper + harness sources; independently re-derive the 185-pin census from the four canonical artifacts with its OWN parser; re-execute BOTH regressions by running the repaired validator with ITS OWN output paths under INTERNAL_QC\ (never overwriting the executor results); verify the fixture pre-mutation hashes and the single-field diff with its own differ; verify both bijections by identity sets; audit QC_R4_REPORT.md claims vs artifacts; audit the frozen erratum content against the historical review (lists A-E must re-classify only facts the historical record supports); check every gate predicate in §11 against the artifacts. Verdict PASS | PASS_WITH_FINDINGS | FAIL with P0/P1/P2/P3 findings. No edits to executor evidence; no writes outside INTERNAL_QC\; no git operations; bytecode disabled.

## §10 PERSISTENCE SEQUENCE (persistence phase only, after the PE-MASTER final audit; the human order steps, in this literal order)

1. Complete contradiction/current-state sweep (§8 disposition).
2. Update the factual AUDIT_ENTRYPOINT.md pointer (ONLY the existing package row's purpose/verdict cells gain the QC-R4 correction facts: the Desktop post-audit REQUIRE_CORRECTIONS verdict on 2b381b32; the QC-R4 fail-closed validator repair with both regressions' results; the PE-MASTER coverage erratum; the P3 record; NEXT_ACTION = FOCUSED_CHATGPT_DESKTOP_POST_AUDIT of the new SHA. NO governance cell changes; NO row disappears (ENTRYPOINT_ROW_SURVIVAL); no Desktop-PASS claim).
3. Generate the FINAL package MANIFEST LAST (self-excluded; quoted NOTE row; every data line parses as exactly 5 CSV fields).
4. Verify every manifest file row against disk size + SHA256.
5. Verify package disk census == manifest file rows + manifest self-exclusion.
6. Stage ONLY this bounded correction's additions (00_CONTROL\QC_R4_CORRECTION_R1_20261002\ + 04_QC\QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM\ + 06_REPORT\PE_MASTER_COVERAGE_ERRATUM_R1.md + 06_REPORT\PE_MASTER_REVIEW_QC_R4_R1.md + the applicable AUDIT_ENTRYPOINT.md update). Verify the staged/Git-tree package bytes match the verified manifest before commit.
7. Scan for proprietary original payloads/secrets (no Entropia.exe/20002.vfs/installers/original .bnt/.ark/.vfs payloads; no credentials).
8. Create ONE NORMAL NEW COMMIT (no amend/squash/force-push/reset/history-rewrite; message identifies RUN_ID, the QC-R4 fail-open validator repair + regressions, the coverage erratum, and confirms original proprietary payloads are excluded).
9. Push origin/master. On failure/divergence: preserve local state, report PERSISTENCE_BLOCKED, stop without force.
10. Verify: git ls-remote --exit-code origin refs/heads/master; record command, UTC timestamp, exit status, returned SHA; require LOCAL_HEAD == LIVE_REMOTE_MASTER_SHA.
11. No package edits after the final manifest verification. Store post-commit/push receipts OUTSIDE the finalized package or return them in the final response (no receipt files inside the finalized package).
12. HARD_STOP = YES; NEXT_EXPERIMENT_AUTHORIZED = NO; NEXT_ACTION = FOCUSED_CHATGPT_DESKTOP_POST_AUDIT OF THE NEW EXACT SHA.

## §11 GATES (executable; fail-closed; a gate weaker than its label is a finding)

- R4-G0_BASELINE: every B1-B10 pin matches (re-measured by formalizer, executor, internal QC, and PE-MASTER independently). FAIL => BLOCKED_BASELINE; HARD_STOP before any package edit; no reset/overwrite/force-push/substitute base.
- R4-G1_REPAIR: the repaired validator implements R1-R12 exactly (verified by full source read: internal QC + PE-MASTER; any requirement weakened or missing = a finding; the gate predicate IS the requirement list).
- R4-G2_POSITIVE_REGRESSION: §4 expected values, all of them, AND exit 0.
- R4-G3_INVALID_VA_REGRESSION: §5 expected values, all of them, AND exit != 0 AND exactly one FAILED row AND the reproduced fail-open case is rejected.
- R4-G4_BIJECTION: identity-set bijection input<->result rows in BOTH runs (185/185, no duplicates, no drops).
- R4-G5_ISOLATION_AND_HYGIENE: no writes outside {00_CONTROL\QC_R4_CORRECTION_R1_20261002\, 04_QC\QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM\, the persistence-phase files named in §6/§10-2}; QC-R3 sources/outputs + all historical artifacts byte-unchanged (re-hash sweep vs the B-pins); the 5 untracked groups untouched; no __pycache__; no EXE/VFS payload bytes in the fixture/repo (scan); bytecode disabled in all runs.
- R4-G6_ERRATUM: the erratum document separates the A-E lists, corrects exactly the two overclaims (S-1, S-2), records P3, carries LATER_PERSONAL_SOURCE_REVIEW only for items actually read NOW, and preserves the honest NOT_CHECKED status wherever the later review is incomplete.
- R4-G7_PERSISTENCE: §10 steps 1-12 executed in order; staged census exact; manifest bijection exact; live remote == LOCAL_HEAD; receipts outside the package.

Non-pass classes: BLOCKED_BASELINE; REPAIR_DEFECT; REGRESSION_FAIL (either regression's own PASS predicate failed); ERRATUM_DEFECT; PERSISTENCE_BLOCKED. The negative validator failure in Regression B is EXPECTED and is a successful negative regression — not a REGRESSION_FAIL.

HARD_STOP: after the verified push (or on any BLOCKED class). Publish the honest state even if a regression fails or a finding remains open (record the failure; no claim promotion; no automatic new correction/science cycle).

## §12 FORBIDDEN

launching/instrumenting the client; any runtime execution; Ghidra; new RE questions; downstream-consumer search; placement experiments; VFS reparsing or new EXE/VFS science; Q1/gate/milestone advancement; editing any historical artifact (incl. 04_QC\QC_R3_DESKTOP_CORRECTION\ — sources AND outputs; the QC rounds 1/2 reports/tools; 00_CONTROL historical files; 06_REPORT\PE_MASTER_REVIEW.md; BEFORE copies; 01_RAW canonical evidence incl. the four positive inputs); copying original EXE/VFS payloads into the fixture/repo; writing outside the authorized paths; git operations by the executor/QC (persistence only, after the PE-MASTER verdict); staging unrelated working-tree groups; proprietary payloads/secrets in git; force-push; history rewrite; recording the commit's own SHA inside files in that same commit; nested task dispatch.

## §13 DELIVERY FIELDS (machine-recorded in QC_R4_REGRESSIONS_SUMMARY.json + QC_R4_REPORT.md; assembled by the persistence worker's terminal response)

BASE_SHA; NEW_COMMIT_SHA; LIVE_REMOTE_MASTER_SHA; REMOTE_QUERY/UTC_TIMESTAMP/EXIT_STATUS/RETURNED_SHA_OR_ERROR; CHANGED_PATH_CENSUS; PACKAGE_PATH; FINAL_MANIFEST_SHA256; MANIFEST_FILE_ROW_COUNT/NOTE_ROW_COUNT/PHYSICAL_PACKAGE_FILE_COUNT; STAGED_GIT_TREE_IDENTITY_RESULT; PROPRIETARY_PAYLOAD_AND_SECRET_SCAN_RESULT; FINAL_CORRECTION_VERDICT; PUBLICATION_STATUS/PUBLICATION_BLOCKER; F1_STATUS; POSITIVE_REGRESSION_RESULT; INVALID_VA_REGRESSION_RESULT; POSITIVE_{INPUT_PIN_COUNT,PROCESSED_COUNT,VERIFIED_OK,FAILED_COUNT,ERROR_COUNT,MISMATCH_COUNT,DENOMINATOR,OVERALL_OK,PROCESS_EXIT_CODE,REGRESSION_PASS}; INVALID_VA_{same fields}; INPUT_RESULT_BIJECTION; FIXTURE_DIFF_PATH; NEW_VALIDATOR_SOURCE_SHA256; NEW_QC_REVISION_PATH; F2_STATUS; PERSONAL_FULL_READ list; PERSONAL_PHYSICAL_RECOMPUTATION list; PERSONAL_SPOT_CHECK list; DELEGATED_QC list; NOT_CHECKED_PERSONALLY list; LATER_PERSONAL_SOURCE_REVIEW list; SCIENCE_STATUS = UNCHANGED; CORRECTED_SELECTED_READER = CONFIRMED_STATIC; DOWNSTREAM_CONSUMER_IDENTIFIED = NO; FINAL_SEMANTIC_STATUS = UNVERIFIED; CANONICAL_GATE_EFFECT = NONE; Q1_STATUS_CHANGED = NO; M1/M2/M3_CHANGED = NO; HARD_STOP = YES; NEXT_EXPERIMENT_AUTHORIZED = NO; NEXT_ACTION = FOCUSED_CHATGPT_DESKTOP_POST_AUDIT OF THE NEW EXACT SHA.
