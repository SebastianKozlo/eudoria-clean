# HANDOFF — PE_935_CAND4_CHILD_ROOT_NC2_NC3_DECODER_CORRECTION_R1_20261008

Contract §6 terminal fields (persistence/publication phase), filled with the actual measured
values. RESULTING_SHA and REMOTE_SHA are governed by the one-commit + manifest-LAST
constraints: their post-push values are recorded at the terminal handoff returned by the
persistence worker to PE-MASTER (the contract forbids embedding the resulting SHA in a file
that is part of the same commit). No second commit exists or is permitted for this run.

## TERMINAL FIELDS BLOCK

```text
RUN_ID =
PE_935_CAND4_CHILD_ROOT_NC2_NC3_DECODER_CORRECTION_R1_20261008

EXPECTED_BASE_SHA =
91598a9868037c4954e22e16c535d6a5a671771e

RESULTING_SHA =
recorded at the terminal handoff (the contract forbids embedding the resulting SHA in a file
of the same commit)

REMOTE_SHA =
recorded at the terminal handoff (the contract forbids embedding the resulting SHA in a file
of the same commit)

REMOTE_VERIFICATION =
LOCAL_HEAD == origin/master == actual remote master == RESULTING_SHA, measured live after the
push (live ls-remote); recorded at the terminal handoff

NC1_PRESERVED =
YES (fail-closed SIB guard in every memory-ModRM branch of both successors, before any
displacement/length computation — production guard call sites @lines 245/287/299/328; 9-case
SIB battery rejected 9/9 by BOTH decoders; 144-form sweep rejected 144/144 by BOTH decoders;
NC1 = CLOSED_FOR_AUDITED_STATE for 91598a98 — unchanged historical status)

NC2_DISPOSITION =
CORRECTED_AND_REVALIDATED_IN_TEST_SCOPE (production: the sibfixed 0x84 memory length table
REMOVED; every memory TEST form mod!=11 rejected fail-closed BEFORE any length computation —
raise @289 precedes size @291; register TEST 84 C0 kept; NC2 buffer now FAIL on both checkers;
historical production false-pass reproduced PRE as PASS)

NC3_FF_DISPOSITION =
CORRECTED_AND_REVALIDATED_IN_TEST_SCOPE (QC: erroneous FF /3 acceptance REMOVED; FF /2 mod=11
only, incl. the FF D2 endpoint; FF D8 rejected — no FF /6 or extra forms added; NC3 FF D8 buffer
FAIL on both checkers; historical QC false-pass reproduced PRE as PASS)

NC3_LEA_DISPOSITION =
CORRECTED_AND_REVALIDATED_IN_TEST_SCOPE (both decoders: LEA mod=11 rejected explicitly BEFORE
operand formatting — production raise @247 precedes LEA formatting @282 — controlled
(False, diagnostic) verdict, never TypeError; historical production ERROR:TypeError and
historical QC PASS reproduced PRE)

PRE_REPRODUCTION =
16/16 rows on the REAL historical functions (safe AST extraction of exact definitions +
needed constants; top level NEVER executed — top_level_executed: false for both sources);
NC2: production PASS (false pass) / QC FAIL; NC3 FF D8: production FAIL / QC PASS;
NC3 LEA: production ERROR (TypeError captured as ERROR, never FAIL) / QC PASS; the five
NC1-era cases: clean PASS/PASS, clobber/esi/nop/NC1 FAIL/FAIL; PRE_REPRODUCED=YES per-case
flags. Kept separate from SOURCE_DESKTOP_MEASUREMENT (Desktop residual_tests transcribed
VERBATIM with citation, 3/3 deep-equal) — no prior verdict copied as a new measurement.

POST_MATRIX_16_ROWS =
16/16 match the contract-mandated results on the ACTUAL corrected functions (clean PASS;
clobber/esi/nop/NC1 SIB/NC2 TEST/NC3 FF D8/NC3 LEA all FAIL on both checkers; zero unexpected
exceptions; every rejection the controlled (False, diagnostic) verdict; production executed
via importlib; QC re-execution equals POST 8/8; PE-MASTER counter-check 8/8)

CLEAN_BOUNDARY_REGRESSION =
PASS (22-instruction VA/size map identical to the published record; total 0x42 = 66 B;
P1 8B F8 @0x0050A3B7, P3 57 @0x0050A3F6, P4 FF D2 @0x0050A3F7 all exact; production, QC and
PE-MASTER executions agree; the corrections altered NO clean boundary)

SIB_9_CASE_REGRESSION =
PASS (nine historical SIB negative cases re-derived safely via ast.parse + ast.literal_eval
from the READ-ONLY historical QC script — zero code execution; 9/9 rejected at DECODER level by
BOTH decoders)

SIB_144_FORM_SWEEP =
PASS (6 opcode branches x 3 memory mod x 8 reg, always rm=4 — 144 synthetic forms, 288
decoder calls, ALL rejected AT THE DECODER LEVEL by BOTH decoders 144/144 + 144/144; tested at
decoder level, never presented as an accidental whole-checker P1 FAIL)

PRODUCTION_AUTHENTICITY =
PASS (03_SCRIPTS/ctrl4_exact_endpoint_nc23fixed.py SHA256
68BEC1AEFDF6A0F32A3ED12F3AED9B72255F8A89AA2F5BA4EFD11C709C4D9F13 == pin == POST declared;
the ACTUAL function executed via importlib — no imitation, no hardcoded results; QC re-executed
it 8/8 row-equal; PE-MASTER independently re-executed it 8/8 on PE-MASTER-derived buffers)

QC_ORIGIN =
FRESH_INDEPENDENT_INTERNAL_QC_BY_PE_MASTER_AUDITOR (fresh-context, under direct PE-MASTER
dispatch; own successor implementation lineage of the historical internal-QC engine; only
stdlib imports; production executed separately via importlib for comparison only; NOT a
Desktop post-audit; NOT independent of PE-MASTER — recorded; one targeted repair round on the
QC's own static structure control, followed by a FULL QC re-run)

QC_VERDICT =
PASS (executable terminal gate G1..G6, every condition recorded individually in
00_CONTROL_INTERNAL_QC/QC_RESULTS.json)

QC_GATE_PREDICATES =
QC_PASS = G1(16/16 matrix rows) AND G2(production authenticity: SHA match + POST row equality
by own re-execution + structural guard verification on CODE lines) AND G3(clean map 22/0x42)
AND G4(9/9 SIB cases rejected by both decoders) AND G5(144/144 decoder-level rejections by
both decoders) AND G6(explicit NC2/NC3 rejection mechanisms + zero unexpected exceptions).
Measured: G1..G6 ALL PASS.

SOURCE_PACKAGES_UNCHANGED =
YES (the three historical packages READ-ONLY: `git diff 91598a98 -- <each path>` EMPTY for
all three; physical census unchanged: NC1 package 14 files, PRIOR_SCIENCE 38 files,
PRIOR_CORRECTION 27 files; zero tracked changes repo-wide at persistence; pinned repo inputs
re-measured byte-identical)

PACKAGE_PHYSICAL_FILE_COUNT =
14 (13 package files + MANIFEST_SHA256.csv; measured physical census at manifest generation)

MANIFEST_ROWS =
14 (13 package rows — every physical file under OUTPUT_REPO_PATH except the manifest itself —
+ 1 AUDIT_ENTRYPOINT.md row, repo-relative)

MANIFEST_BIJECTION =
PASS (missing=0, extra=0, duplicate=0, size mismatch=0, SHA256 mismatch=0; generator
self-check + independent persistence-phase full re-hash of every row)

CHANGED_PATH_CENSUS =
exactly 15 paths, all inside the WRITE_ALLOWLIST
(OUTPUT_REPO_PATH/** = 14 package files + AUDIT_ENTRYPOINT.md);
staged census clean — zero foreign, zero historical-package files, zero .pyc/__pycache__;
pre-existing foreign untracked paths untouched (5x PE_935_* packages + experiments/)

OPEN_FINDINGS =
NONE material.
Disclosed (process items, no evidence affected):
1. One targeted QC repair round (1 of 1 allowed) on the QC's own static structure control
   (docstring exclusion + branch anchoring; falsifiability preserved; full QC re-run, no stale
   PASS copied).
2. Two prior QC dispatch sessions returned empty with zero files written (child session
   failures, not gate failures); the third fresh-context dispatch completed the QC; per
   contract, an unperformed QC would have forbidden a positive QC_VERDICT.
3. Executor in-scope process fixes disclosed (AST census allowlist for exception constructors;
   a placeholder hash replaced with the measured value before handoff).
4. Executor matrix run 1 aborted at its own AST static call census guard (RuntimeError; no
   evidence accepted from that run); runs 2-3 measured identical results.
5. Historical records wording backlog documented by the prior NC1 package (not reopened).

NEW_CORRECTION_DESKTOP_POST_AUDIT =
NOT_PERFORMED (the fresh internal QC of this run is NOT the future Desktop post-audit of the
newly published correction SHA; the published exact SHA is returned for that audit)

WORLD_XYZ_RECOVERED = NO

CANONICAL_GATE_EFFECT = NONE

NEXT_EXPERIMENT_AUTHORIZED = NO

HARD_STOP = YES
```

## Notes

- NC2/NC3 changes VALIDATION MACHINERY ONLY: no historical placement data created or retracted;
  all science statuses of contract §5 preserved verbatim (see FINAL_REPORT.md §11).
- Publication is NOT acceptance: the PE-MASTER verdict is advisory (ADVISORY_PRE_QUALIFICATION;
  Q1 absent, PROVISIONAL_UNTIL_QUALIFIED; CANONICAL_GATE_EFFECT=NONE); the independent Desktop
  post-audit of the NEW published correction SHA remains pending.
- Persistence: exactly ONE normal commit at BASE 91598a98 (no amend, no force push, no history
  rewrite), normal fast-forward push; MANIFEST_SHA256.csv generated LAST; live remote verify
  after push. Any write after the manifest requires regeneration + full re-verification.
- Status naming: NC2/NC3 = CORRECTED_AND_REVALIDATED_IN_TEST_SCOPE (test scope = the 8-case
  matrix + the 9-case SIB battery + the 144-form sweep). NOT GENERAL_X86_DECODER_PROVEN.
