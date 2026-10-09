# EVIDENCE_INDEX — PE_935_CMO_ARG1_BR_C1_ARTIFACT_VALIDATION_CORRECTION_R1_20261009

All evidence paths are PACKAGE-relative (this package). SCRATCH paths are
local-only (OUTPUT_ROOT\SCRATCH) and NEVER published. Physical sizes/SHA256
of every published file are in MANIFEST_SHA256.csv (generated LAST, after
all other writes).

## A. Contract / authorization

| Item | Path | Identity |
|---|---|---|
| Authorizing contract | `C:\Users\User\Documents\ChatGPT\PE\PE_CMO_BR_C1_CORRECTION_PROMPT_REVIEW_20261009\OPENCODE_BR_C1_ARTIFACT_VALIDATION_CORRECTION_R1_20261009.md` (external, read-only) | 18566 B, SHA256 B30E807BFA24BC37A8FFC015D37B42EC96F72F47D8B6956AFA9512D09CDC1CE3 |
| Predecessor contract (methodological input) | external (I2 in INPUT_IDENTITIES.md) | 23187 B, 773C1310… |
| Desktop post-audit REPORT.md / AUDIT_COUNTERCHECKS.json / SECOND_PASS_VERIFICATION.json | external (I3; defect MAP, never a gate oracle) | FA6D8C43… / 60DE66C2… / 7259B582… |

## B. Pre-registration (written before the correction work)

| Item | Path | Notes |
|---|---|---|
| Preregistration | PREREGISTRATION.md | P1 defect, P2 expected PRE, P3 planned POST, P4 planned controls, P5 planned regression, P6 preserved science, P7 supersession plan, P8 publication-safety order, P9 honest scope; never rewritten |

## C. Inputs

| Item | Path | Identity |
|---|---|---|
| Predecessor BRIDGE_PROVENANCE.json (byte-identical copy, explicitly a PREDECESSOR INPUT) | 01_INPUTS/BRIDGE_PROVENANCE.json | 32219 B, ADBA8BF873A4BA41755DA7D5CFCF2AC80F2E5B6131E54BA1CB7BF44868947D9F |
| Predecessor package (read-only source) | docs/audits/PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009/ at BASE 2ac7cfa1 | 35/35 files blob-verified; before/after hash inventory identical |
| EXE (read-only) | D:\Eudoria_Reconstruction\pcg_install\Entropia.exe | 8015872 B, E7785430…; unchanged every phase |

## D. PRE (defect reproduction, ACTUAL predecessor gates)

| Item | Path | Key content |
|---|---|---|
| PRE results | PRE_ARTIFACT_RESULTS.json | 7 fixed cases x 2 gates; predecessor module hashes (0DB331D8…/EC9F3FBE…); CLEAN PASS 21/21 both; AC1/AC2 REJECTED; BR1–BR4 PASS both = 8 false-PASS; pre_reproduction.defect_reproduced = true; full check lists per case |
| PRE mutated copies | SCRATCH/prov/pre_*.json (local only) | deep copies via the gates' normal provenance override |

## E. POST (corrected gates)

| Item | Path | Key content |
|---|---|---|
| Corrected production gate | 03_SCRIPTS/run_frame_bridge.py | SHA256 1b11b3a152696c0090c51f3c4507dc575ef87cd6eb0caf7bd99e6b461772b6b3 |
| Corrected QC gate | 03_SCRIPTS/qc_frame_bridge.py | SHA256 1d6e168cb290923a855f2f9f41cc30ab40c01464ba128dbd50fd24b594b8be73 |
| Test driver | 03_SCRIPTS/run_br_c1_controls.py | SHA256 55f952a576724bfafcef0833b88badce57d052355839579cafb3fd26187cc8cb; imports gates as modules, normal provenance override, all writes to OUTPUT_ROOT |
| Code diff | CODE_DIFF.patch | predecessor vs corrected, repo-relative labels; hunks confined to the gate sections |
| POST results | POST_ARTIFACT_RESULTS.json | fixed_matrix 14/14; per-case verdicts, failing check names, expected predicates, hash-side failures (all empty), named diagnostics; additional_matrix 43 cases / 86 outcomes, 86/86; clean_final_validation 50/50 checks per gate |
| Coverage table | FIELD_CHECK_COVERAGE.csv | 34 rows; PERSISTED_FIELD_PATH / ACTUAL_PERSISTED_VALUE / DERIVED_EXPECTED_VALUE / EVIDENCE_SOURCE / WHY_NON_CIRCULAR / check names / single-field FAILURE_CASE_DETECTED / GATE_VERDICT |

## F. Regression (unchanged byte matrices)

| Item | Path | Key content |
|---|---|---|
| Regression results | REGRESSION_RESULTS.json | production 12/12 + QC 12/12 CONTROL_PASS = 24/24; per-case fixtures SHAs, objdump commands/rc; M5/M7 arg1-unchanged + other-channel-changed (production + QC); unchanged-helper preservation proofs (EXPECTED/MUTATIONS/CASE_ORDER/EXP/MUT identical); EXE unchanged |
| Regression scratch | SCRATCH/reg_prod_out/, SCRATCH/reg_prod_work/, SCRATCH/qc_work/reg/ (local only) | 12 production raw objdump texts, 24 fixtures — never published |

## G. QC (self-review, honest scope)

| Item | Path | Key content |
|---|---|---|
| QC results | QC_RESULTS.json | EXECUTOR_SELF_REVIEW; fresh-context QC = NOT_PERFORMED (separate later agent); 43 mechanical checks, 43/43 PASS; independence dimensions + honest limitations |
| QC report | QC_REPORT.md | method, findings F-QC-1/2/3 (driver CSV-writer shadowing defect caught+fixed+full re-execution; CSV display artifact; predecessor EXEC_CLAIMS residual) |
| Self-review script | SCRATCH/self_review.py (local only) | the 43-check mechanical re-inspection |

## H. Standing / governance

| Item | Path | Key content |
|---|---|---|
| Supersession record | SUPERSESSION_AND_STANDING.md | supersedes ONLY the predecessor's overbroad artifact-gate adequacy claim; preserves controls/science/failed-history; standing science verbatim; scope fences |
| PE-MASTER review provenance | PE_MASTER_REVIEW.md | actual internal origin: NOT_PERFORMED_IN_THIS_RUN; self-review is the only in-run review; guidance for later reviewers |
| Final report | FINAL_REPORT.md | full narrative + all measured matrices |
| Input identities | INPUT_IDENTITIES.md | I1–I9 (contract, inputs, EXE, tools, environment, post-work re-verification) |

## I. Driver run summary

| Item | Path | Key content |
|---|---|---|
| Driver run summary | DRIVER_RUN_SUMMARY.json | per-phase exe hashes, source-package before/after inventory comparison, timestamps |

## J. Persistence artifacts (canonical repo)

| Item | Path | Notes |
|---|---|---|
| Published package | docs/audits/PE_935_CMO_ARG1_BR_C1_ARTIFACT_VALIDATION_CORRECTION_R1_20261009/ (repo) | byte-copy of PACKAGE minus SCRATCH |
| AUDIT_ENTRYPOINT.md | docs/audits/AUDIT_ENTRYPOINT.md (repo root of audits) | ONE new truthful row |
| MANIFEST_SHA256.csv | MANIFEST_SHA256.csv (this package) | generated LAST; covers the published package physical files minus itself plus the changed AUDIT_ENTRYPOINT.md; verified bijection |

## Evidence-chain notes

- The two corrected gates share GNU objdump 2.44 with the predecessor run
  (the same objdump is NOT two independent disassemblers — honest).
- The QC gate independently derives its expected facts (own parse/walk/
  opcode bytes); it does not import or delegate to the production verdict;
  the driver records both outcomes without mixing derivations.
- Every rejection in the fixed/additional matrices was verified to have
  zero hash/identity-side failures and the expected named BR-C1
  predicate(s) failing — rejections caused by hash/manifest failure,
  missing fixture, crash or unrelated predicate failure would NOT count.
