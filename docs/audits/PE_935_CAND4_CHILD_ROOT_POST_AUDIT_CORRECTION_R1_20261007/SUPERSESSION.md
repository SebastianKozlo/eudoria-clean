# SUPERSESSION — PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007

Explicit supersessions issued by this correction package (contract §7). The superseded
package is the SOURCE run PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007 at
AUDITED_SHA 790e83735b439e2d76a250868a47a599c2c10184 (READ-ONLY; its records are NOT
edited — this file + the corrected records of THIS package are the supersession
authority). Superseding scope: the source run's Census/ACCOUNTING/QC-MACHINERY claims
and the wrapper-depth semantic claim, per the Desktop post-audit C4-C1/C4-C2 verdict
REQUIRE_CORRECTIONS.

## S-1. "ACCOUNTED_EDGE_COUNT = 24" as the COMPLETE total — SUPERSEDED

Where (source package): EDGE_ACCOUNTING_LEDGER.csv header ("ACCOUNTED_EDGE_COUNT (ANALYZED_NEW rows below) = 24"); FINAL_REPORT.md §4 ("ANALYZED 24"); HANDOFF.md
(NEW_INTERPROCEDURAL_EDGES_SEMANTICALLY_ANALYZED = 24); PE_MASTER_REVIEW.md census line.

Superseded by: CORRECTED_EDGE_ACCOUNTING_LEDGER.csv. 24 is the count of ledger-labeled
ANALYZED_NEW rows only — NOT the complete total of semantically analyzed callsite units.
The corrected conservative PROVEN floor is MINIMUM_NEW_ANALYZED_EDGE_COUNT >= 32
(24 + the 8 content-proven additional units RV-01..RV-07 + NEIGH-09); the exact complete
total is UNRESOLVED (9 candidate rows not adjudicated + 11 repin exemptions not
re-verified).

## S-2. "INDEPENDENT_RECONSTRUCTED_EDGE_COUNT = 24 (== ACCOUNTED_EDGE_COUNT)" as a complete-census proof — SUPERSEDED

Where (source package): QC_REPORT.md §2 (S6); qc_ind_census.py QC-I9/QC-I10;
HANDOFF.md ("INDEPENDENT_RECONSTRUCTED_EDGE_COUNT = 24 (== ACCOUNTED_EDGE_COUNT)"); PE_MASTER_REVIEW.md ("INDEPENDENT_RECONSTRUCTED_EDGE_COUNT 24 == … (exceedance exactly 24, not more…)").

Superseded by: the corrected accounting + this package's QC. The historical
"reconstruction" re-derived the LEDGER CLASSIFICATION itself (QC-I9 subtracts
ledger-classified RV/NEIGH rows per class), and QC-I5 checked only the emptiness of the
NEW_INTERPRETATION column — the interpretation content recorded in NOT_COUNTED_REASON
was ignored. A re-enumeration that trusts the same ledger's class column is not an
independent reconstruction of the true analyzed set. The corrected classification is
content-based (CORRECTED_EDGE_ACCOUNTING_LEDGER.csv; QC check C1–C6 re-derives it from
row content).

## S-3. "exceedance exactly 24 units / exactly +16 past the stop line" — SUPERSEDED

Where (source package): EDGE_ACCOUNTING_LEDGER.csv header ("the run analyzed 24 callsite units, 16 past the stop line"); FINAL_REPORT.md §4 ("EXCEEDED by 16"); qc_ind_census.py
QC-I10 ("EXCEEDED by exactly 16"); HANDOFF.md ("16 past the stop line").

Superseded by: EDGE_ACCOUNTING_STATUS = BUDGET_EXCEEDED with the proven floor >= 32
units — at least +24 past MAX 8; the exact exceedance is UNRESOLVED (not "exactly"
anything). ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL stands (historical).

## S-4. "zero semantic analysis hidden under RAW_VISIBLE" as an ACHIEVED state — SUPERSEDED

Where (source package): EDGE_ACCOUNTING_LEDGER.csv header lesson-J2 line ("analysis is never hidden behind a RAW_VISIBLE label"); CLAIM_MATRIX.csv CL-14 evidence cell ("no analysis is hidden behind RAW labels"); PE_MASTER_REVIEW.md ("zero semantic analysis hidden under RAW_VISIBLE").

Citation repaired 2026-10-07 (PE-MASTER-ordered records-repair; independent internal QC
finding F-IND-1): the pre-repair text attributed the "no analysis is hidden behind RAW
labels" phrase to FINAL_REPORT.md §4, where it does NOT exist (git grep at BASE); the
superseded claim is real in exactly the three loci above (EDGE_ACCOUNTING_LEDGER.csv
header line 8; PE_MASTER_REVIEW.md line 23; CLAIM_MATRIX.csv CL-14). S-4 substance
(superseded claim + supersession) unchanged.

Superseded by: the corrected classification. Eight rows (RV-01..RV-07, NEIGH-09) carry
recorded interpretations in their NOT_COUNTED_REASON while classified not-counted —
analysis WAS present under the not-counted labels. What remains TRUE and is NOT
superseded: the J2 row-per-callsite census discipline itself (every callsite touched by
the run's records has a ledger row — 69 rows retained verbatim; the corrected ledger
keeps every original column).

## S-5. "NEW_FUNCTION_BODIES_OPENED = 6/6 within, NOT exceeded" — SUPERSEDED

Where (source package): FINAL_REPORT.md §2 ("budgeted bodies 6/6") + §4 ("used 6/6 … NOT exceeded"); HANDOFF.md ("NEW_FUNCTION_BODIES_OPENED = 6/6"); CLAIM_MATRIX.csv CL-15;
PREREGISTRATION.md §3 plan (MAX 6).

Superseded by: FUNCTION_BODY_ACCOUNTING.csv. The historical CTRL_3 performed a REAL
8-byte EXE probe of FUN_006C0EE0 (8B 81 20 01 00 00 C3 CC) and interpreted it as the
manager+0x120 getter of the same class family — an undeclared real-body probe (Desktop
C4-C1 second counterexample; absent from both declared prior packages). Per the
source-run contract §2 rule (partial opening/probing consumes the budget):
MINIMUM_NEW_FUNCTION_BODIES_OPENED >= 7; ORIGINAL_FUNCTION_BODY_BUDGET_COMPLIANCE =
FAIL (supersedes "6/6 within"); EXACT_NEW_FUNCTION_BODIES_OPENED = UNRESOLVED; the exact
total is not provable from existing records). The six declared bodies' own measured
facts (extents, writer roles, the getter/producer-chain byte facts) are BYTE
MEASUREMENTS and are NOT superseded.

## S-6. The stronger claim that the OLD CTRL_4 correctly checks the EXACT FINAL CHILD ARGUMENT — SUPERSEDED (with the historical test results PRESERVED)

Where (source package): CONTROL_RESULTS.json CTRL_4 (checker description "§7 chain intactness: head move + no EDI-writing instruction + push edi"); verdict PASS with the
final-argument framing); FINAL_REPORT.md §3 ("CTRL_4 (child identity break) = PASS");
HANDOFF.md ("CTRL_4_RESULT = PASS (child identity break: an EDI clobber between the head move and push edi breaks the return->final-child relation — same checker, same window)").

Superseded by: 03_SCRIPTS/ctrl4_exact_endpoint.py + CONTROL_RESULTS.json
(CTRL_4_EXACT_ENDPOINT_REBUILT). The old predicate (qc_controls.py:150-199) sets
push_edi=True at ANY `push edi` in the window — the window contains an earlier
push edi @0x0050A3D7 — so it did NOT bind the predicate to the exact final-argument site
0x0050A3F6, did not require the join call endpoint CALL edx @0x0050A3F7 (FF D2, no
shift), and FALSE-PASSES the two Desktop mutants (0x0050A3F6: 57->56 push esi;
57->90 nop). The rebuilt checker requires simultaneously: exact head mov edi,eax
@0x0050A3B7 (8B F8); no caller-side EDI write in the required range; exact final child
argument push edi @0x0050A3F6 (57); exact join call endpoint call edx @0x0050A3F7
(FF D2) — verified at exact addresses on correct decode boundaries.

PRESERVED (NOT rewritten — authentic historical measurements of the OLD checker, and
they remain valid AS MEASUREMENTS): the historical REAL CLEAN case PASS and the
historical EDI-clobber mutant FAIL genuinely occurred and are kept as historical test
results. ADDED by this correction (not present in the source package): the two Desktop
false-PASS mutant results (both reproduced by the old-logic reproduction over in-memory
buffers) and the new exact-endpoint implementation with the full 4-case matrix (clean
PASS; clobber FAIL; esi FAIL; nop FAIL — matching the Desktop's
own_exact_endpoint_predicate). The corrected CTRL_4 still checks ONLY the caller-side
exact final-argument predicate — CHILD_TO_JOIN_IDENTITY is NOT promoted to CONFIRMED
(the four intervening callee bodies remain unopened).

## S-7. "WRAPPER_DEPTH = 2" as a SEMANTIC wrapper-layer proof — SUPERSEDED (the historical budget charge PRESERVED)

Where (source package): FINAL_REPORT.md §1 answer 2 ("WRAPPER_DEPTH = 2 (manager -> instance [+0x6C]; instance -> [+4]; the further moves to the join are SAME_OBJECT)");
HANDOFF.md; PE_MASTER_REVIEW.md ("WRAPPER_DEPTH = 2").

Superseded by: CORRECTED_LINEAGE_STATUS.md. WRAPPER_DEPTH = UNRESOLVED — semantics is
NOT budget consumption. H-1 (manager stores/contains the created instance at [+0x6C]) is
a measured containment; H-2's relation (whether [instance+4] is the instance's contained
model root, a handle, or a refcount slot of a wrapper class) is NOT physically
established, so the number of semantic wrapper layers is UNRESOLVED, and the two charged
units do NOT establish two model-wrapper layers. PRESERVED per correction contract §4:
the historical budget consumption NEW_WRAPPER_HOPS = 2 (charged analysis units H-1/H-2
under MAX_NEW_WRAPPER_HOPS = 3, unchanged) — the unresolved H-2 relation still consumed
the budget; the charge is NOT zeroed or reduced. POINTER_LINEAGE_TRANSITIONS_OBSERVED =
2 is the description of the two examined transitions (H-1/H-2), not a global census.

## S-8. "SCOPE_COMPLIANCE = PARTIAL_WITH_EXCEEDED_EDGE_BUDGET" — SUPERSEDED

Where (source package): EDGE_ACCOUNTING_LEDGER.csv header; FINAL_REPORT.md §4; HANDOFF.md.

Superseded by: ORIGINAL_SCOPE_COMPLIANCE = FAIL — the historical state of the audited
run, never to become PASS (the edge budget exceedance is now a floor-exceedance >= 32
vs MAX 8, and the function-body budget is also exceeded at >= 7 vs MAX 6). This is a
historical process fact; the byte evidence and the component findings of the source run
are NOT falsified by it.

## S-9. The source package's "MASTER_ACCEPTED (advisory)" / internal-QC "zero P1/P2" completeness framing — SUPERSEDED as to completeness

Where (source package): PE_MASTER_REVIEW.md ("RUN_VERDICT = MASTER_ACCEPTED (advisory)"
with "zero P1/P2" in the internal-QC line); QC_REPORT.md §7 (QC_PASS 23/23 framing).

Superseded by: the authoritative Desktop post-audit verdict REQUIRE_CORRECTIONS (2 x P2:
C4-C1, C4-C2) — the internal QC's check SET was incomplete for census-completeness
purposes (the QC-I5/QC-I9 defects; SUPERSESSION S-2) and the CTRL_4 predicate had a
reproducible false PASS (S-6). NOT superseded: the individual historical check RESULTS
as executed (23/23 checks passed as specified — the check specifications were the
defect), the advisory authority statuses (ADVISOry_PRE_QUALIFICATION; Q1 absent), and
the PE-MASTER review's own verified byte re-pins. Publication was never acceptance; the
historical FAILs stand.

## NOT superseded (explicit preservation list — byte measurements and standings)

- All byte measurements of the source run: the getter body (8B 41 68 C3 —
  DIRECT_FIELD_GETTER [manager+0x68], extent proven); the base-ctor NULL-init of +0x68
  (89 5E 68 @0x006C8FD3); the measured store [manager+0x68] = [instance+4] (89 7E 68
  @0x006C67E2 with the read 8B 78 04 @0x006C67BE and the refcount swap protocol); the
  lazy producer chain byte/dataflow facts (FUN_006C8B20 trigger, FUN_006C6F60 producer,
  FUN_0072FCE0 validity, empty-string-key lookups, getter A = FUN_007CE1E0, the pump
  FUN_006C9700 -> [+0x6C] store 89 46 6C @0x006C7008, the installer FUN_006C6780); the
  join-window bytes (8B F8 @0x0050A3B7; 57 @0x0050A3F6; FF D2 @0x0050A3F7); all 56 byte
  pins + 23 rel32 recomputes; the RTTI names (.?AVArkModelManagerMain@@ /
  .?AVArkModelManager@@ / .?AVArkModelResourceInstanceRef@@); the string constants
  ('ArkTexture' 0x00A859F8; 'ArkAnimation' 0x00A8547C; the empty-string key 0x00A7957B).
- EXACT_PARENT = CONFIRMED_EXACT_SCENEFEEDER_PLUS_30 (carried, scoped to the examined
  ACLD+0x18 SF instance) and JOIN_OPERATION = STRONGLY_SUPPORTED (the ceiling).
- The component ceilings/standings (NOT promoted by this correction):
  CHILD_RESOURCE_PROVENANCE = STRONGLY_SUPPORTED_MODEL_DERIVED (NOT CONFIRMED_MODEL_
  DERIVED — GAP-1 [instance+4] identity and GAP-2 FUN_006C8BB0 stand);
  MODEL_ROOT_RELATION = UNKNOWN; CHILD_VISUAL_ROLE = UNRESOLVED;
  CHILD_TO_JOIN_IDENTITY = STRONGLY_SUPPORTED (NOT CONFIRMED — the four intervening
  callee bodies remain unopened); CAND4_CHILD_ROOT_CLOSURE = NOT_ESTABLISHED_WITHIN_BOUND.
- The J1–J3 supersessions of the earlier correction run (historical qualification gate
  not a positive qualifier; the source run's minimum-22 pair convention; the transform
  relation NOT_QUALIFIED_BY_ORIGINAL_SCOPE) — carried, unchanged.
- Governance statuses: WORLD_XYZ_RECOVERED = NO; HISTORICAL_INSTANCE_DATA_RECOVERED = NO;
  STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED; RUNTIME_JOIN_OBSERVED = NO;
  CANONICAL_GATE_EFFECT = NONE; REAL_SCIENCE_AUTO_QUALIFICATION = DISABLED;
  NEXT_EXPERIMENT_AUTHORIZED = NO.
