# HANDOFF — PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007

Executor: pe-reconstruction (PE-MASTER direct dispatch, NO_NESTED_TASKS).
Phase of THIS dispatch = RECORDS_AND_QC_MACHINERY_CORRECTION (correction contract §1–§7)
+ rebuilt CTRL_3/CTRL_4 machinery (synthetic fixtures; in-memory mutants) + fresh
internal QC (SELF-REVIEW) + PACKAGE. Persistence (AUDIT_ENTRYPOINT row, manifest
regeneration with the entrypoint row, one path-limited commit, push, live remote
verification) belongs to PE-MASTER after its own audit of this package. This executor
does NOT edit AUDIT_ENTRYPOINT.md (proposed newest-first row below) and does NOT
commit/push (RESULTING_SHA = NONE this phase).

## TERMINAL BLOCK (correction contract §Zwrot — actual measured)

```text
RUN_ID = PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007
EXPECTED_BASE_SHA = 790e83735b439e2d76a250868a47a599c2c10184
RESULTING_SHA = NONE (this phase; no commit/push by this executor)
REMOTE_SHA = 790e83735b439e2d76a250868a47a599c2c10184 (remote master verified UNCHANGED
  at preflight 2026-10-07T18:37Z: actual remote master == origin/master == LOCAL_HEAD ==
  EXPECTED_BASE_SHA; re-verified at package close; no write to the remote occurred in
  this phase)
C4_C1_DISPOSITION = CORRECTED (records: edge re-adjudication 32-counted floor + body
  accounting >= 7; historical compliance FAILs stand; EXACT counts UNRESOLVED)
C4_C2_DISPOSITION = CORRECTED (machinery: ctrl4_preservation rebuilt as the exact-
  endpoint checker; required 4-case matrix verified; caller-side scope unchanged)
MINIMUM_NEW_ANALYZED_EDGE_COUNT = 32 (>= 32; proven floor = 24 historical + 8
  content-proven additional units RV-01..RV-07 + NEIGH-09)
EXACT_NEW_ANALYZED_EDGE_COUNT = UNRESOLVED (9 candidate rows + 11 repin exemptions not
  adjudicated; not provable from existing records)
MINIMUM_NEW_FUNCTION_BODIES_OPENED = 7 (>= 7; the 6 declared + the undeclared
  historical CTRL_3 probe FUN_006C0EE0)
EXACT_NEW_FUNCTION_BODIES_OPENED = UNRESOLVED
ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL (historical; stands permanently; exceedance
  >= +24 vs MAX 8, not exact)
ORIGINAL_FUNCTION_BODY_BUDGET_COMPLIANCE = FAIL (historical; supersedes "6/6 within")
ORIGINAL_SCOPE_COMPLIANCE = FAIL (historical state; never becomes PASS)
RETROACTIVE_PRIOR_AUTHORIZATION = NO
WRAPPER_DEPTH = UNRESOLVED (semantics != budget consumption)
HISTORICAL_LINEAGE_BUDGET_CHARGE = NEW_WRAPPER_HOPS = 2 of MAX_NEW_WRAPPER_HOPS = 3
  (unchanged limit; the unresolved H-2 relation still consumed the budget — preserved,
  not zeroed; the 2 charged units do NOT establish 2 model-wrapper layers)
CTRL3_SYNTHETIC_OR_PRIOR_PIN_STATUS = SYNTHETIC_FIXTURES_AND_PERSISTED_PRIOR_PINS_ONLY
  (clean = the persisted getter pin 8B 41 68 C3 CC CC CC CC; mutated = the recorded
  historical probe constant 8B 81 20 01 00 00 C3 CC; ZERO EXE access; no new real
  accessor discovery; the historical probe itself is ACCOUNTED as the 7th body)
CTRL4_CLEAN = PASS (rebuilt exact-endpoint checker; P1 head 8B F8 @0x0050A3B7 + P2 no
  EDI write in range + P3 push edi 57 @0x0050A3F6 + P4 call edx FF D2 @0x0050A3F7 — all
  at exact addresses on verified decode boundaries)
HISTORICAL_EDI_CLOBBER = FAIL (P2: mov edi,[0xB9D8D0] @0x0050A3DD in the required range)
FINAL_PUSH_ESI = FAIL (P3: 57 -> 56 @0x0050A3F6 = push esi, not push edi)
FINAL_PUSH_NOP = FAIL (P3: 57 -> 90 @0x0050A3F6 = nop, not push edi)
  (all three mutants SYNTHETIC/IN-MEMORY ONLY; the old checker's logic reproduction
  FALSE-PASSES the ESI and NOP mutants — the two Desktop false PASS, reproduced)
QC_ORIGIN = SELF-REVIEW (fresh internal QC by the same pe-reconstruction executor
  session that produced this package; NOT an independent external Desktop post-audit;
  NOT a PE-MASTER qualification; the independent Desktop post-audit of THIS correction's
  SHA remains NOT_PERFORMED)
CORRECTION_RECORDS_QC = PASS (QC_PASS 21/21; one QC-tooling defect round disclosed and
  fixed in the QC script only — QC_REPORT.md §6)
ORIGINAL_SCOPE_COMPLIANCE = FAIL (separated from CORRECTION_RECORDS_QC; historical)
MANIFEST_ROWS = 18 (physical package files minus the manifest itself)
PHYSICAL_FILE_COUNT = 19 (18 package files + MANIFEST_SHA256.csv)
MANIFEST_BIJECTION = VERIFIED (generator self-check: zero missing/extra/duplicate; all
  sizes+SHA256 re-read at generation; independent post-generation re-hash by a separate
  implementation — .NET SHA-256 via PowerShell — reported in the terminal response; any
  write after the manifest requires regeneration + re-verification)
SOURCE_PACKAGE_UNCHANGED = YES (38/38 BASE git-blob identity verified BEFORE and AFTER
  the work; zero mismatches, zero missing; zero writes into any historical package)
CHANGED_PATH_CENSUS = exclusively docs/audits/PE_935_CAND4_CHILD_ROOT_POST_AUDIT_
  CORRECTION_R1_20261007/** (created by this run; 19 physical files incl. the manifest);
  ZERO tracked modifications; AUDIT_ENTRYPOINT.md NOT edited; the 6 foreign untracked
  roots untouched
OPEN_FINDINGS =
  1. EXACT_NEW_ANALYZED_EDGE_COUNT = UNRESOLVED (the 9 candidate NEIGH annotations and
     the 11 repin exemptions were NOT adjudicated; adjudication belongs to a human/
     PE-MASTER decision, not this records correction).
  2. EXACT_NEW_FUNCTION_BODIES_OPENED = UNRESOLVED (the bounded-window neighbor-body
     raw display question — FUNCTION_BODY_ACCOUNTING.csv candidate row C1).
  3. The historical scope FAILs (edges >= 32 vs MAX 8; bodies >= 7 vs MAX 6) are
     permanent process facts; no retroactive authorization.
  4. GAP-1 ([instance+4] identity; FUN_006C9700 unopened) and GAP-2 (FUN_006C8BB0
     unopened) remain the recorded next-input candidates of the SOURCE run — recorded
     only; NOT opened, NOT authorized by this correction.
NOT_CHECKED (explicit) = FUN_006C9700; FUN_006C8BB0; the four §7 intervening callee
  bodies (FUN_006C0F90/FUN_006C10B0/FUN_0050A1E0/FUN_005246E0); FUN_007B6C30;
  FUN_007BF900/FUN_007BF630; FUN_007BF470 (forbidden — join ceiling); all NEIGH bodies;
  the FUN_006C6780 continuation; runtime anything (STATIC-ONLY lineage); payloads; the
  EXE (ZERO access of any kind by this correction); the independent PE-MASTER audit of
  THIS package (pending)
CAND4_CHILD_ROOT_CLOSURE = NOT_ESTABLISHED_WITHIN_BOUND (unchanged; this correction
  promotes nothing)
WORLD_XYZ_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES (after package + manifest LAST + bijection verification; no entrypoint
  edit, no commit/push by this executor)
```

## Manifest verification (per the every-write-after-the-manifest rule)

MANIFEST_SHA256.csv is generated LAST (03_SCRIPTS/make_manifest.py; every package file
was already on disk at generation time; scope = the physical OUTPUT_ROOT files minus the
manifest itself; AUDIT_ENTRYPOINT.md EXCLUDED pending persistence — noted in the
manifest header; the persistence phase regenerates the manifest over the final physical
package together with the entrypoint row). Bijection: the generator's self-check (zero
missing/extra/duplicate; sizes+SHA256 re-read at generation) + an INDEPENDENT
post-generation re-hash by a separate implementation (.NET SHA-256 via PowerShell),
reported in this session's terminal response (not persisted as a package file — any
write after the manifest requires regeneration + re-verification; the persistence phase
repeats the re-hash over the final physical package). Encoding: every package file
UTF-8 no-BOM, LF-only (QC check C20 at QC time; manifest regenerated after — same
writer discipline).

## PROPOSED AUDIT_ENTRYPOINT.md newest-first row (NOT applied by this executor)

The persistence phase should add this row at the TOP of AUDIT_ENTRYPOINT.md
(newest-first), adapted to the entrypoint's current column format:

| RUN_ID | PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007 |
|---|---|
| DATE | 2026-10-07 |
| PACKAGE | docs/audits/PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007/ |
| BASE_SHA | 790e83735b439e2d76a250868a47a599c2c10184 |
| RESULT | C4-C1/C4-C2 POST-AUDIT CORRECTION (records/QC-machinery only; executor phase: corrections + rebuilt CTRL_3/CTRL_4 + internal QC SELF-REVIEW QC_PASS 21/21 + package; no commit/push this phase — RESULTING_SHA = NONE). C4-C1 EDGE ACCOUNTING CORRECTED: the source run's "ACCOUNTED_EDGE_COUNT = 24 complete total" / "INDEPENDENT_RECONSTRUCTED = 24" / "exceedance +16" / "zero analysis hidden under RAW" RETRACTED; content-based re-adjudication of all 69 rows (original columns verbatim) counts 32 proven units (24 + RV-01..RV-07 + NEIGH-09) => MINIMUM_NEW_ANALYZED_EDGE_COUNT >= 32, EXACT = UNRESOLVED (9 candidates + 11 repin exemptions unadjudicated). C4-C1 BODY ACCOUNTING CORRECTED: the historical CTRL_3 8-byte probe of FUN_006C0EE0 (manager+0x120 getter) is the undeclared 7th real-body opening => MINIMUM_NEW_FUNCTION_BODIES_OPENED >= 7, EXACT = UNRESOLVED; ORIGINAL_FUNCTION_BODY_BUDGET_COMPLIANCE = FAIL (supersedes 6/6). C4-C2 CTRL_4 REBUILT as the exact-endpoint checker (P1 head 8B F8 @0x0050A3B7; P2 no EDI write in range; P3 push edi 57 @0x0050A3F6; P4 call edx FF D2 @0x0050A3F7 — exact addresses, verified decode boundaries): clean PASS / EDI-clobber FAIL / ESI-mutant FAIL / NOP-mutant FAIL (all synthetic in-memory; the old predicate's two Desktop false PASS reproduced by a logic-only reproduction; the historical clean PASS / clobber FAIL results preserved as authentic). CTRL_3 rebuilt on synthetic fixtures/persisted prior pins (zero EXE access). WRAPPER_DEPTH = UNRESOLVED (semantics != budget consumption); historical lineage budget charge preserved (NEW_WRAPPER_HOPS = 2/3; H-2 relation UNRESOLVED still consumed). PRESERVED (not superseded): all byte measurements (getter DIRECT_FIELD_GETTER [manager+0x68]; NULL-init +0x68; measured store [manager+0x68]=[instance+4]; producer chain; join window bytes; 56 pins; 23 rel32; RTTI; string constants) and standings (CHILD_RESOURCE_PROVENANCE = STRONGLY_SUPPORTED_MODEL_DERIVED; MODEL_ROOT_RELATION = UNKNOWN; CHILD_VISUAL_ROLE = UNRESOLVED; CHILD_TO_JOIN_IDENTITY = STRONGLY_SUPPORTED NOT CONFIRMED; EXACT_PARENT = CONFIRMED_EXACT_SCENEFEEDER_PLUS_30 ACLD-scoped; JOIN_OPERATION = STRONGLY_SUPPORTED ceiling; CAND4_CHILD_ROOT_CLOSURE = NOT_ESTABLISHED_WITHIN_BOUND). ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL; ORIGINAL_SCOPE_COMPLIANCE = FAIL (historical, permanent); RETROACTIVE_PRIOR_AUTHORIZATION = NO. CORRECTION_RECORDS_QC = PASS (self-review) separated from ORIGINAL_SCOPE_COMPLIANCE = FAIL. SOURCE_PACKAGE_UNCHANGED (38/38). NEXT_EXPERIMENT_AUTHORIZED = NO. |
| SUPERSESSIONS | This correction supersedes (SUPERSESSION.md S-1..S-9): the source run's complete-edge-count 24 / exact exceedance +16 / zero-analysis-under-RAW census claims (content-based re-adjudication, floor 32, exact UNRESOLVED); the independent-24 reconstruction as a completeness proof (QC-I5/QC-I9 defect); body count 6/6 (floor 7, exact UNRESOLVED); the old CTRL_4 exact-final-argument correctness claim (rebuilt; two Desktop false PASS documented; historical clean PASS / clobber FAIL preserved); WRAPPER_DEPTH = 2 as a semantic proof (budget charge 2 preserved); SCOPE_COMPLIANCE = PARTIAL_WITH_EXCEEDED_EDGE_BUDGET (now FAIL); the MASTER_ACCEPTED/zero-P1-P2 completeness framing (Desktop post-audit verdict REQUIRE_CORRECTIONS stands). NOT superseded: all byte measurements, EXACT_PARENT, JOIN_OPERATION ceiling, component ceilings/standings, J1–J3. |
| STATUS | CORRECTION_EXECUTED_PENDING_PE_MASTER_AUDIT (executor phase complete: corrected records + rebuilt machinery + internal QC SELF-REVIEW QC_PASS 21/21 + package + manifest LAST + bijection verified; entrypoint update/commit/push = the PE-MASTER persistence phase after its own audit; publication != acceptance; the independent Desktop post-audit of the new SHA remains NOT_PERFORMED) |

## Key artifact paths

- CORRECTED_EDGE_ACCOUNTING_LEDGER.csv — the C4-C1 edge re-adjudication (69 rows;
  verbatim originals + corrected adjudication; 32/11/17/9 census).
- FUNCTION_BODY_ACCOUNTING.csv — the C4-C1 body accounting (7 counted + candidates).
- CORRECTED_LINEAGE_STATUS.md — the wrapper/lineage terminology correction.
- CONTROL_RESULTS.json — the rebuilt CTRL_3 + CTRL_4 results (4-case matrix + the
  old-logic false-PASS reproduction).
- 03_SCRIPTS/ctrl3_rebuilt.py / ctrl4_exact_endpoint.py — the rebuilt checkers
  (synthetic fixtures; in-memory mutants; zero EXE access).
- 03_SCRIPTS/build_corrected_ledger.py — the corrected-ledger builder (verbatim copy).
- 03_SCRIPTS/qc_correction.py + QC_CORRECTION_RESULTS.json — the fresh internal QC.
- 03_SCRIPTS/FIXTURES.md — the byte-fixture provenance (incl. the window map).
- 03_SCRIPTS/make_manifest.py — the manifest generator (LAST).
- QC_REPORT.md / SUPERSESSION.md / FINAL_REPORT.md / PE_MASTER_REVIEW.md (placeholder —
  NOT_PERFORMED-do-persistence) / GOVERNANCE_DECISION.md / INPUT_IDENTITIES.md.
- MANIFEST_SHA256.csv — generated LAST (entrypoint excluded pending persistence).

## HARD STOP

After the package + manifest LAST + bijection verification: HARD STOP. No next RE, no
FUN_006C9700/FUN_006C8BB0 decoding, no §7 preservation bodies, no visual-role RE, no
candidate-row adjudication, no runtime, no entrypoint edit, no commit/push by this
executor. NEXT_EXPERIMENT_AUTHORIZED = NO. Any write after the manifest requires
manifest regeneration + re-verification (the every-write-after-the-manifest rule).
