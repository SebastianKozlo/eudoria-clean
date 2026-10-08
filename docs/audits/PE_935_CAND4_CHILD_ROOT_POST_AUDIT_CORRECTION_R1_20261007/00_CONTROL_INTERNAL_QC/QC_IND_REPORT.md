# QC_IND_REPORT — PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_INTERNAL_QC_R1_20261007

ASSIGNMENT_MODE = INTERNAL_QC (independent, fresh-context; PE-MASTER direct dispatch; NO_NESTED_TASKS)
AUDITED PACKAGE = PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007 (executor: pe-reconstruction;
its own QC = the honestly-labeled SELF-REVIEW — this QC is the INDEPENDENT verification the dispatch ordered)
REPO = D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean · BASE = HEAD = 790e83735b439e2d76a250868a47a599c2c10184
(package untracked; AUDIT_ENTRYPOINT.md NOT edited; zero commit/push by this QC; SOURCE_PACKAGE + historical
packages READ-ONLY, verified). RECORDS/QC-MACHINERY ONLY — zero EXE access of any kind; zero new RE;
replicas only on published byte buffers and synthetic in-memory copies.

Machine record: QC_IND_RESULTS.json (17 records-checks + 7 controls-checks, all PASS; 2 findings, both P3;
QC_VERDICT = QC_PASS_WITH_FINDINGS). Engines: qc_ind_reverify.py, qc_ind_ctrl_own.py, qc_ind_finalize.py.

---

## 1. FULL_READ (dispatch item 1) — DONE

All 19 package files read IN FULL to EOF (11 root + 7×03_SCRIPTS + manifest; FULL_READ_LOG.md).
The corrected ledger's all 69 rows × 13 fields read row-by-row; the source ledger read in full;
the old qc_controls.py read in full (both defect loci verified at source). Identities: contract
364D5C82…F348 (11,851 B) MATCH; Desktop REPORT/CONTROL_COUNTERCHECKS/EDGE_AND_SCOPE (BDE7B9EB… /
32DC3FEE… / E275035B…) MATCH — all re-measured by this QC.

## 2. CORRECTED_EDGE_ACCOUNTING_LEDGER — MY OWN re-adjudication of all 69 rows (dispatch item 2)

Method: per-row content adjudication by THIS QC (explicit per-row map in qc_ind_reverify.py,
written after reading every row's NEW_INTERPRETATION + NOT_COUNTED_REASON), under the literal
source-run contract §2 rule (PREREGISTRATION.md lines 65–71: a NEW interpretation of receiver /
callee identity / argument-result flow / path role / semantic role of a callsite = a counted unit;
partial probing consumes the body budget; "not load-bearing" is not an exemption).

- E-01..E-24: all have genuine recorded callsite interpretations → COUNTED (24). ✓
- RV-01..RV-07 + NEIGH-09: interpretation content lives in NOT_COUNTED_REASON (argument
  construction; temp init ×2; cleanup ×4; receiver esi + result→FUN_006C9F30 argument) → COUNTED (8). ✓
- RP-01..RP-11: interpretation text present but explicitly prior-recorded re-pins → exemption
  retained. MY SPOT-VERIFICATION (I11) converts the ledger's conservative UNREVERIFIED label into
  spot-verified-GENUINE for all 11 rows: X01/X03/X05/X31/X08 are real rows of the J2 correction's
  EDGE_BUDGET_RECONSTRUCTION.csv; E5/E6 are real rows of the 20261006 join-run EDGE_LEDGER.csv
  (E6 = THE JOIN SITE); QC S4 exists; the prior FUN_0050A310_DECODE.txt window contains the four
  intervening calls + the [SF+0x2C] writes. ✓
- NEIGH-01/02/05/08/10/12/13/14/17/18/19/20/22/23/25/26/27 (17): topology/window facts only → CLEAN. ✓
- NEIGH-03/04/06/07/11/15/16/21/24 (9): annotations that MAY constitute §3 interpretations
  (body-identity/body-role/receiver/allocation-argument/topology/path-role notes) → honestly left
  UNADJUDICATED. This is the honest UNRESOLVED treatment, NOT arbitrary adjudication: the
  authoritative Desktop itself did not adjudicate them ("pozostałych neighbor annotations i wszystkich
  REPIN exemptions nie adjudykowano wyczerpująco"), adjudicating them would create new interpretive
  science (forbidden in a records correction), and counting them could only RAISE the floor. ✓

**MY classification vs the corrected ledger: ZERO differences** (I6 PASS; all 69 rows agree on
COUNTED + class). My stricter reading (NEIGH-04 'new(0x68)', NEIGH-15 'receiver [esp+0x40]' arguably
countable) would only raise the floor above 32 — no disposition changes. **Census: 32 COUNTED +
11 PRIOR_REPIN_EXEMPTION_UNREVERIFIED + 17 NOT_COUNTED_CLEAN + 9 CANDIDATE_UNADJUDICATED = 69 —
matches the declared 32/11/17/9 exactly** (I7). Minimum >= 32 is defensive (24 + the 8
contract-mandated rows) and matches the Desktop's conservative floor. EXACT = UNRESOLVED is CORRECT:
9 candidates unadjudicated + the full re-verification of every exemption's prior scope is beyond a
records correction; the exact total is not provable from existing records. ORIGINAL_EDGE_BUDGET_
COMPLIANCE = FAIL stands (>= 32 > MAX 8; exceedance >= +24, not exact); RETROACTIVE_PRIOR_
AUTHORIZATION = NO; ORIGINAL_SCOPE_COMPLIANCE = FAIL (supersedes PARTIAL_WITH_EXCEEDED_EDGE_BUDGET). ✓
Verbatim round-trip: all 69 rows × 9 original fields byte-identical to the BASE source ledger (I5). ✓

## 3. FUNCTION_BODY_ACCOUNTING (dispatch item 3)

- FUN_006C0EE0 historically counted as the 7th body: **VERIFIED AT SOURCE** (I9) — the old
  qc_controls.py line 131 `ok_mut3, det_mut3 = ctrl3_provenance(0x006C0EE0)` through
  `disasm(getter_va, 8)` = `PE_OBJ.read(va, 8)` — a REAL 8-byte EXE probe, interpreted as the
  [+0x120] getter; recorded in the source CONTROL_RESULTS.json CTRL_3 mutated_case. ✓
- The probe is NOT a prior pin: `git grep -i 6c0ee0` over ALL FOUR prior audit packages at BASE =
  ZERO hits (I10) — the Desktop's "absent from both declared prior packages" independently
  CONFIRMED and extended. ✓
- MINIMUM_NEW_FUNCTION_BODIES_OPENED >= 7 ✓ (6 declared + the proven 7th);
  EXACT_NEW_FUNCTION_BODIES_OPENED = UNRESOLVED ✓ (the C1 window-spill question honestly
  unadjudicated; the recorded-scripts probe scan found no other undeclared probe — the
  unrecorded execution history is not provable from records); ORIGINAL_FUNCTION_BODY_BUDGET_
  COMPLIANCE = FAIL ✓ (supersedes 6/6). No new body opened by the correction: zero affirmative
  EXE-access occurrences in the package scripts (I16; the only pe_reader/capstone mentions are
  explicit negations); the rebuilt CTRL_3 is synthetic/persisted-prior-pin only. ✓

## 4. CTRL_4 REBUILT — code read + MY OWN executions (dispatch item 4)

Code (03_SCRIPTS/ctrl4_exact_endpoint.py, read to EOF): the checker requires SIMULTANEOUSLY
P1 exact head `mov edi,eax` @0x0050A3B7 (bytes 8B F8) · P2 no caller-side EDI write in
(0x0050A3B7, 0x0050A3F6) · P3 exact final child argument `push edi` @0x0050A3F6 (byte 57) ·
P4 exact join call endpoint `call edx` @0x0050A3F7 (bytes FF D2) — each looked up as the
instruction STARTING at the exact address out of a boundary-safe linear decode of the whole
window (fail-closed on any uncovered form). A CALL mnemonic anywhere else never satisfies P4;
the earlier push edi @0x0050A3D7 never satisfies P3. ✓

MY OWN decoder + MY OWN checker (structurally independent; qc_ind_ctrl_own.py):

| case | MY checker | executor's checker | old logic | expected |
|---|---|---|---|---|
| REAL CLEAN (window re-derived by me from the published record: 22 instr, 0x42 B, contiguous, byte-identical to the fixture) | PASS | PASS | PASS | PASS |
| historical EDI-clobber @0x0050A3DD (8B 3D D0 D8 B9 00) | FAIL (P2) | FAIL (P2) | FAIL | FAIL |
| 0x0050A3F6: 57→56 push esi | FAIL (P3) | FAIL (P3) | **PASS (false)** | FAIL |
| 0x0050A3F6: 57→90 nop | FAIL (P3) | FAIL (P3) | **PASS (false)** | FAIL |

Matrix == the Desktop own_exact_endpoint_predicate (clean=true; recorded_mutant=false;
ESI=false; NOP=false) and == the persisted CONTROL_RESULTS.json (C4). The old-logic
reproduction reproduces the two Desktop false PASS exactly (C5) while the historical clean
PASS / clobber FAIL remain preserved as authentic measurements. ✓

**MY adversarial mutants (all 9 FAIL BOTH checkers — zero false PASS; C6):**

| mutant | expected leg | mine | executor's | old logic |
|---|---|---|---|---|
| A1a head displaced (nop @B7; chain otherwise intact) | P1 | FAIL | FAIL | FAIL |
| A1b head alternative byte form 89 C7 (mov edi,eax, non-canonical) | P1 | FAIL | FAIL | **PASS** |
| A2 real push edi @F4/F5 but NOT at the exact site F6 | P3 | FAIL | FAIL | **PASS** |
| A3a join call shifted to 0x0050A3F8 (push edi @F7) | P3+P4 | FAIL | FAIL | **PASS** |
| A3b call truncated at the window end (FF @F8, no modrm) | fail-closed | FAIL | FAIL | FAIL |
| A4a pop edi injected @0x0050A3E3 | P2 | FAIL | FAIL | FAIL |
| A4b pop edi injected @0x0050A3D6 | P2 | FAIL | FAIL | FAIL |
| A5 push edi 2-byte form FF F7 @0x0050A3F6 | P3 exact bytes | FAIL (fail-closed) | FAIL (fail-closed) | FAIL |
| A6 final push removed, earlier push edi @0x0050A3D7 survives | P3 | FAIL | FAIL | **PASS** |

Conclusion: **no obvious hole found** — exact addresses (A2/A3a/A6), exact byte forms (A1b/A5),
P2 write-detection breadth incl. pop forms (A4a/b), fail-closed decode (A3b/A5) all hold; the
earlier-push hole of the old checker is closed (A6). BONUS OBSERVATION: A1b additionally revealed
that the OLD checker also accepted the non-canonical head encoding (89 C7) — a further old-checker
weakness the rebuilt exact-byte requirement closes. All mutants SYNTHETIC/IN-MEMORY ONLY; the
executor's run_and_write() was never invoked by this QC (no package file rewritten; manifest
re-verified zero-mismatch after all executions).

## 5. CTRL_3 REBUILT (dispatch item 5)

Clean = the persisted getter pin `8B 41 68 C3 CC CC CC CC` — provenance verified against the
source 01_RAW/FUN_006C66D0_GETTER_FULL.txt RAW BYTES line — = PASS; mutated = the recorded
historical probe constant `8B 81 20 01 00 00 C3 CC` (reads [ecx+0x120]) = FAIL — on BOTH my own
checker and the executor's (C7). MY adversarial fixtures: [ecx+0x69] FAIL (offset specificity);
[esi+0x68] FAIL (base-register specificity); disp32 form `8B 81 68 00 00 00` of the SAME field
PASS (semantically identical encoding correctly NOT false-failed). ZERO EXE access in the script
(I16). CTRL3_SYNTHETIC_OR_PRIOR_PIN_STATUS = SYNTHETIC_FIXTURES_AND_PERSISTED_PRIOR_PINS_ONLY ✓.

## 6. CORRECTED_LINEAGE_STATUS (dispatch item 6)

All elements verified mechanically + by full read: WRAPPER_DEPTH = UNRESOLVED ✓;
MODEL_ROOT_RELATION = UNKNOWN ✓; POINTER_LINEAGE_TRANSITIONS_OBSERVED = 2 as the DESCRIPTION of
the examined H-1/H-2 (explicitly NOT a global census) ✓; H-2 RELATION_TYPE = UNRESOLVED ✓;
NEW_WRAPPER_HOPS = 2 (charged analysis units) / MAX_NEW_WRAPPER_HOPS = 3 (unchanged) PRESERVED ✓;
the unresolved H-2 relation still consumes the budget (not zeroed/reduced) ✓; NO claim that the
two charged units establish two model-wrapper layers ✓; the budget-compliance fact (2 of 3) is
explicitly NOT presented as a semantic result or a scope exoneration ✓. Basis matches the source
POINTER_LINEAGE.csv (H-1 WRAPPER_CONTAINS measured store; H-2 physical dataflow CONFIRMED /
RELATION_TYPE UNRESOLVED; H-3/H-4 SAME_OBJECT register moves, NOT lineage transitions). ✓

## 7. SUPERSESSION S-1..S-9 (dispatch item 7)

Every S-quote verified in the cited SOURCE package file at BASE (whitespace/comment-wrap
normalized for the ~78-col hard wraps; I12): complete-24 (ledger header, FINAL_REPORT §4, HANDOFF,
PE_MASTER_REVIEW census line) ✓; independent-24-as-proof (source QC_REPORT §2 S6, qc_ind_census
QC-I9/QC-I10, HANDOFF, PE_MASTER_REVIEW) ✓; exact +16 (ledger header, FINAL_REPORT, QC-I10,
HANDOFF) ✓; zero-under-RAW (ledger header line 8, PE_MASTER_REVIEW, CLAIM_MATRIX CL-14) ✓; body
6/6 (FINAL_REPORT §2/§4, HANDOFF, CLAIM_MATRIX CL-15, PREREGISTRATION §2/§3) ✓; the stronger
old-CTRL_4 claim (source CONTROL_RESULTS CTRL_4 checker description + PASS verdict, FINAL_REPORT
§3, HANDOFF) — with the historical clean PASS / EDI-clobber FAIL preserved as authentic
measurements and the two Desktop false PASS ADDED (my C5 reproduces them) ✓; WRAPPER_DEPTH=2 as
semantic proof (FINAL_REPORT §1, HANDOFF, PE_MASTER_REVIEW) with the budget charge 2 preserved ✓;
SCOPE_COMPLIANCE = PARTIAL… → FAIL (S-8) ✓; MASTER_ACCEPTED/zero-P1-P2 completeness framing (S-9) ✓.
NOT superseded (verified present): the getter bytes 8B 41 68 C3 (DIRECT_FIELD_GETTER [manager+0x68]);
the store pair 89 7E 68 @0x006C67E2 / 8B 78 04 @0x006C67BE ([manager+0x68]=[instance+4]); the
producer-chain facts; the join-window bytes 8B F8 / 57 / FF D2; EXACT_PARENT; the RTTI/string
constants. ✓ **FINDING F-IND-1 (below): one citation's file attribution is wrong.**

## 8. Science preservation (dispatch item 8)

Standing statuses present and NOT promoted (mechanical sweep + my per-occurrence context
adjudication of all 16 token occurrences): MODEL_ROOT_RELATION = UNKNOWN; CHILD_VISUAL_ROLE =
UNRESOLVED; CHILD_TO_JOIN_IDENTITY = STRONGLY_SUPPORTED (NOT CONFIRMED); CAND4_CHILD_ROOT_CLOSURE
= NOT_ESTABLISHED_WITHIN_BOUND; CHILD_RESOURCE_PROVENANCE = STRONGLY_SUPPORTED_MODEL_DERIVED
(ceiling; GAP-1/GAP-2 stand); provenance ceiling unchanged; EXACT_PARENT carried scoped. ZERO
active promotions; ZERO new science branches anywhere in the package (the 8 additionally counted
units quote only recorded source content — verified verbatim per row); NO SCIENCE_PASS (every
occurrence is a negation/policy context). ✓

## 9. GOVERNANCE_DECISION (dispatch item 9)

The verbatim human instruction (§1) contains exactly: the contract path + RUN_ID + CONTRACT_SIZE
11851 + SHA 364D5C82…F348 + EXPECTED_BASE_SHA 790e837… + the authorization sentence + "Zachowaj
historyczny budget FAIL i potwierdzone byte measurements" + "Nie rozpoczynaj FUN_006C9700 ani
żadnego nowego RE" + RESULTING_SHA/REMOTE_SHA return requirement + NEXT_EXPERIMENT_AUTHORIZED = NO
+ HARD_STOP = YES — all consistent with the contract and the PE-MASTER dispatch chain (I14). The
phase split (no entrypoint edit, no commit/push in the executor phase; RESULTING_SHA = NONE) is
recorded as ORCHESTRATOR_PHASE_SPLIT from the dispatch text — the established methodology — and
matches the observed repo state (package untracked, HEAD == BASE, AUDIT_ENTRYPOINT.md unmodified).
✓

## 10. SOURCE_PACKAGE_UNCHANGED + manifest (dispatch item 10)

- My own full re-verification: 38/38 working-tree == BASE git blobs, zero mismatches, zero
  missing (I3) — SOURCE_PACKAGE_UNCHANGED at my QC time; the Desktop COMMITTED_INPUT ledger copy
  hashes identically to the BASE blob (I13) — same evidence basis. ✓
- Manifest: 18 rows vs 19 physical files (self-excluded ✓; entrypoint excluded pending
  persistence — noted in the manifest header ✓; HANDOFF documents the persistence-phase
  regeneration). My full re-hash: every row's size+SHA256 re-measured — ZERO mismatch (I1);
  UTF-8 no-BOM / LF-only / strict-decodable for all 19 files (I2). ✓
- Expected consequence, disclosed here: THIS QC's own 00_CONTROL_INTERNAL_QC/ additions enlarge
  the physical package beyond the executor's 18-row manifest scope; per the established pattern
  (the source package did the same) the PERSISTENCE PHASE regenerates the manifest over the final
  physical package (including these QC records + the entrypoint row) before commit/push.

## 11. Separation algebra (dispatch item 11)

No file anywhere claims ORIGINAL_SCOPE_COMPLIANCE = PASS (mechanical scan over all record files);
CORRECTION_RECORDS_QC = PASS is always reported as a SEPARATE algebra object from the historical
ORIGINAL_SCOPE_COMPLIANCE = FAIL (FINAL_REPORT §3, QC_REPORT §7, HANDOFF terminal block, QC_
CORRECTION_RESULTS.json) — never conflated, never merged (I15). ✓

---

## FINDINGS (bold title; exact source; effect; correction; revalidation)

**F-IND-1 (P3) — SUPERSESSION.md S-4: cytat przypisany do złego pliku.**
Source: docs/audits/PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007/SUPERSESSION.md, §S-4
"Where (source package)" line: "FINAL_REPORT.md §4 ('no analysis is hidden behind RAW labels')".
Counter-evidence: the phrase does NOT exist in the source FINAL_REPORT.md (git grep at BASE); it
exists in CLAIM_MATRIX.csv CL-14 (evidence cell: "…no analysis is hidden behind RAW labels").
Effect: citation-level imprecision only — the superseded CLAIM is real in three genuine loci
(EDGE_ACCOUNTING_LEDGER.csv header line 8; PE_MASTER_REVIEW.md line 23; CLAIM_MATRIX.csv CL-14),
so supersession S-4 stands in full; a reader following the FINAL_REPORT citation would not find
the phrase. Correction: re-attribute that citation to CLAIM_MATRIX.csv CL-14 (or quote FINAL_REPORT
§4's actual wording: "every uncounted row carries an explicit reason — the J2 discipline").
Secondary (same file, trivial): S-3's QC-I10 quote "exceeded by exactly 16" vs the source's
"EXCEEDED by exactly 16" (capitalization); several S-quotes span the source's hard line wraps /
drop backticks (S-1 ledger header; S-6 FINAL_REPORT §3; S-7 FINAL_REPORT §1) — substance identical.
Revalidation: grep the corrected citation strings against the named source files at BASE.

**F-IND-2 (P3) — QC_REPORT.md §1: deklaracja niezależności "LEDGER_CLASS not trusted" jest
nadmiarowa względem faktycznej implementacji C2.**
Source: package QC_REPORT.md §1 ("LEDGER_CLASS was NOT trusted as a truth source (the historical
QC-I9 defect)…") + FINAL_REPORT.md §3 ("the corrected ledger classification was FULLY re-derived
from the SOURCE ledger's recorded content") vs 03_SCRIPTS/qc_correction.py check C2
(`if r["LEDGER_CLASS"] == "ANALYZED_NEW": derived[eid] = bool(...)` — LEDGER_CLASS jest selektorem
gałęzi dla 24 wierszy E, a wszystkie wiersze poza ANALYZED_NEW/poza 8 markerami są derivationowo
przypisane na False bez badania ich treści, w tym RP-01..11 z nietrywialnym tekstem interpretacji).
Effect: samoopis QC executora obiecował więcej niezależności, niż C2 dostarcza — C2 nie wyłapałby
samodzielnie błędnie sklasyfikowanego wiersza RP; zgodność C4 jest dla wierszy poza E/markerami
strukturalnie gwarantowana. MATERIALITY LOW: treść 24 wierszy E JEST zweryfikowana (niepustość),
treść 8 wierszy obowiązkowych JEST zweryfikowana (markery), a TEN QC dostarcza genuinely
niezależną adjudykację per-wiersz (I6: zero różnic) — więc klasyfikacja ledgera stoi. To jest
defekt samoopisu QC (records-precision), nie defekt skorygowanego ledgera. Correction: przeformułować
zdanie w QC_REPORT.md §1 tak, aby opisywało rzeczywistą strukturę C2 (class-gated content check dla
wierszy E + marker check dla 8; pozostałe porównane tylko przez wspólną strukturę adjudykacji).
Revalidation: zdanie zgodne z kodem C2; moja niezależna adjudykacja pozostaje rozstrzygająca.

No P1/P2 findings. No hidden promotions, no result-fitted classification (the counted set is
exactly the Desktop-proven floor; my stricter reading only raises it), no CTRL_4 predicate hole
found (9 adversarial mutants, zero false PASS), no unresolved-candidate silently counted.

## COVERAGE

- Package: 19/19 files FULL_READ; corrected ledger 69/69 rows adjudicated by me; manifest 18/18
  rows re-hashed; source ledger 69/69 rows byte-compared; supersession quotes: all S-1..S-9
  loci + all 4 NOT-superserved classes verified; controls: 4 mandatory + 9 adversarial CTRL_4
  cases and 5 CTRL_3 fixtures executed on BOTH my engine and the executor's; science token
  sweep 16/16 occurrences adjudicated; lineage 9/9 mechanical elements; governance 10/10 elements;
  separation scan over all record files; EXE-access scan over all package scripts.
- Algebra: 69 = 32 counted + 11 exemptions + 17 clean + 9 candidates (matches 32/11/17/9);
  bodies 7 counted + 1 candidate + 1 prior-scope non-counted; lineage 2/3 hops preserved.

## NOT_CHECKED

See FULL_READ_LOG.md §6. Highlights: the EXE (zero access — records-only QC); the four intervening
callee bodies, FUN_006C9700, FUN_006C8BB0, FUN_007B6C30, FUN_007BF900/630, FUN_007BF470, all NEIGH
bodies, the FUN_006C6780 continuation (forbidden); the unrecorded execution history of the
audited run (EXACT counts stay UNRESOLVED by design); no re-execution of the executor's
qc_correction.py (it writes into the package — post-manifest write forbidden to this QC; my own
engine independently covers its load-bearing paths); live remote state (persistence-phase duty);
the PE-MASTER audit of this package; the independent Desktop post-audit of the future SHA
(NOT_PERFORMED, pending persistence/publication).

## VERDICT

```text
QC_VERDICT = QC_PASS_WITH_FINDINGS (2 x P3; zero P1/P2; 17/17 records-checks + 7/7 controls-checks PASS)
CORRECTION_RECORDS_QC = the executor's correction records/machinery are VERIFIED by this independent QC
  (C4-C1 ledger re-adjudication + body accounting; C4-C2 rebuilt CTRL_4 + CTRL_3) — with the two P3
  records-precision findings above, neither overturning a disposition
ORIGINAL_SCOPE_COMPLIANCE = FAIL (historical state of the audited run; never becomes PASS; separated)
CAND4_CHILD_ROOT_CLOSURE = NOT_ESTABLISHED_WITHIN_BOUND (unchanged; this QC promotes nothing)
NEXT_EXPERIMENT_AUTHORIZED = NO · HARD_STOP = YES (this QC adds no authorization)
Publication != acceptance; the independent Desktop post-audit of the new SHA remains NOT_PERFORMED.
```

NEXT_PARENT_ACTION (for PE-MASTER): adjudicate the two P3 findings (records-repair in the
correction package: SUPERSESSION S-4 citation re-attribution + QC_REPORT §1 wording — both are
allowlist-path edits inside OUTPUT_ROOT, each requiring the manifest LAST regeneration rule to be
re-applied by the persistence phase anyway); then, if accepted, run the persistence phase
(entrypoint newest-first row from HANDOFF.md, manifest regeneration over the final physical package
including 00_CONTROL_INTERNAL_QC/, bijection re-verification, one path-limited commit, push, live
remote verification, HARD STOP), and record the pending independent Desktop post-audit of the new SHA.
