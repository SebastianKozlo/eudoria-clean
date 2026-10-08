# SUPERSESSION — PE_935_CAND4_CHILD_ROOT_NC1_SIB_DECODER_POST_AUDIT_CORRECTION_R1_20261007

Explicit supersessions issued by this NC1 correction package (frozen contract §15). The
superseded package is the SOURCE run PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007
published at 57ecf3506481e73ca27548ea02e4864904d9883a (READ-ONLY; its records are NOT edited —
this file + the corrected records of THIS package are the supersession authority).
Superseding scope: the CTRL_4 boundary-safety interpretation of that published state and the
open NC1 defect state recorded by the independent Desktop post-audit
(PE_935_CAND4_CORRECTION_DESKTOP_POST_AUDIT_57ECF350_20261007: verdict REQUIRE_CORRECTIONS,
C4_C1_RECORDS = ACCEPTED_IN_EXAMINED_RECORDS_SCOPE,
C4_C2_REQUIRED_ENDPOINT_MUTATIONS = PASS_REPRODUCED,
CTRL4_GENERAL_BOUNDARY_SAFETY = REJECTED_BY_COUNTEREXAMPLE,
NC1_SHARED_SIB_FALSE_PASS = OPEN_P2, FULL_CORRECTION_POST_AUDIT = REQUIRE_CORRECTIONS).

This supersession is NARROW: it reaches exactly two claims and their status transitions.
Nothing else of the audited 57ecf350 state is reopened.

## SN-1. CTRL4_GENERAL_BOUNDARY_SAFETY as claimed at 57ecf350 — SUPERSEDED (bounded)

Where (source package, at 57ecf350): 03_SCRIPTS/ctrl4_exact_endpoint.py line 13 ("at EXACT
addresses on CORRECT decode boundaries (boundary-safe linear decode of the …)" and the
"Boundary-safe linear decode of the whole buffer" docstring at line 128);
00_CONTROL_INTERNAL_QC/qc_ind_ctrl_own.py line 245 ("PASS: P1+P2+P3+P4 all hold at exact
addresses on verified decode boundaries"); CONTROL_RESULTS.json CTRL_4 checker description
("exact-address instruction lookup on verified decode boundaries; ONE code path for all
cases"); FINAL_REPORT.md (§ "instruction AT THE EXACT ADDRESS on correct decode boundaries
(boundary-safe linear …)"); HANDOFF.md ("at exact addresses on verified decode boundaries");
00_CONTROL_INTERNAL_QC/QC_IND_REPORT.md ("out of a boundary-safe linear decode of the whole …").

Superseded by: the authoritative NC1 synthetic counterexample (contract §4: replacement bytes
`8B 8C 24 8C 00 00 E8 BF AA BB CC 90` over 0x0050A3DD..0x0050A3E8) — BOTH published CTRL_4
decoders omit the SIB byte for memory ModRM forms with `mod != 0b11 and rm == 0b100`, compute
displacement/instruction length as though no SIB exists, and FALSE-PASS that buffer
(Desktop measurement: EXPECTED=FAIL, PRODUCTION_CHECKER=PASS, INTERNAL_QC_CHECKER=PASS,
REFERENCE_EDI_WRITE=0x0050A3E4, FALSE_PASS_REPRODUCED=YES; independently reproduced by this
run's EXECUTOR_REPRODUCTION in CONTROL_RESULTS_PRE.json). The generalized boundary-safety
interpretation of those checkers is therefore REJECTED_BY_COUNTEREXAMPLE: agreement of the
two implementations missed the same encoding error.

The corrected, now-authoritative boundary claim is BOUNDED to exactly:

```text
CTRL4_BOUNDARY_VALIDATION =
SUPPORTED_WITHIN_RECORDED_CLEAN_WINDOW_AND_REGISTERED_FALSIFIERS
```

established by the corrected successors (03_SCRIPTS/ctrl4_exact_endpoint_sibfixed.py and
00_CONTROL_INTERNAL_QC/qc_ind_ctrl_sib_own.py): the fail-closed SIB guard (reject
`mod != 0b11 and rm == 0b100` BEFORE any displacement/length computation, in every
memory-ModRM branch) plus the five-case matrix revalidation and the 9-form synthetic SIB
negative battery. NOT GENERAL_X86_DECODER_PROVEN.

PRESERVED under the bound (NOT superseded): the real clean recorded bytes and their
published decode map (22 instructions, contiguous boundaries, total 0x42 — unchanged by the
guard, proven by the boundary regression); the exact-endpoint P1-P4 predicate design;
and the historical endpoint test outcomes (SN-2 note below).

## SN-2. NC1_SHARED_SIB_FALSE_PASS = OPEN_P2 — SUPERSEDED (status transition to CORRECTED_AND_REVALIDATED)

Where: the open-defect state recorded by the Desktop post-audit of 57ecf350 (§4/§6 of
PE_935_CAND4_CORRECTION_DESKTOP_POST_AUDIT_57ECF350_20261007/REPORT.md and
CONTROL_COUNTERCHECKS.json case sib_hidden_edi_write; carried as NC1_SHARED_SIB_FALSE_PASS =
OPEN_P2 by the frozen correction contract §3).

Superseded by: the correction performed and revalidated by THIS package (contract §5-§8):

```text
NC1_SHARED_SIB_FALSE_PASS = CORRECTED_AND_REVALIDATED
```

- Both successors corrected with the fail-closed SIB guard, BEFORE any displacement/length
  computation, in every memory-ModRM branch (production 0x8B/0x89/0x8D, 0x84, 0x83, 0xFF via
  `_reject_sib`; independent QC via its own `mem_dlen` guard + register-only non-11 raises).
  Full SIB decoding NOT implemented (NOT required by the contract; fail-closed rejection is
  the preferred minimum-blast-radius solution).
- Five-case production matrix revalidated on the ACTUAL corrected function
  (CONTROL_RESULTS_POST.json; script SHA256
  44155437F20FA6DA9D6847A236F708C7F2A40F26BABE71424B21C325B4FB4405):
  REAL_RECORDED_CLEAN=PASS; HISTORICAL_EDI_CLOBBER=FAIL (P2 EDI write @0x0050A3DD);
  FINAL_PUSH_ESI=FAIL (P3); FINAL_PUSH_NOP=FAIL (P3); NC1_SIB_HIDDEN_EDI_WRITE=FAIL
  (rejected before any displacement/length computation).
- Fresh independent internal QC (00_CONTROL_INTERNAL_QC/): identical results on all five
  cases; 9-form synthetic SIB negative battery — both decoders fail-closed on every form;
  true-boundary diagnostic: 7-byte MOV+SIB @0x0050A3DD, `mov edi,0x90CCBBAA` @0x0050A3E4
  inside the prohibited P2 interval; QC_VERDICT = PASS.
- The NC1 counterexample is a SYNTHETIC boundary-validator counterexample: it does NOT
  establish an EDI clobber in the real clean PCG window.

The false-pass defect itself is NOT retracted as a finding: it was real, is preserved
authentically in CONTROL_RESULTS_PRE.json (provenance-separated), and stands as the
historical reason for this correction.

## NOT superseded (explicit preservation list)

- **C4_C1_RECORDS acceptance** stands: C4_C1_RECORDS = ACCEPTED_IN_EXAMINED_RECORDS_SCOPE
  (Desktop post-audit of 57ecf350, §2/§6). The corrected ledger, its content-based
  re-adjudication and its 69-row round-trip are untouched by NC1.
- **The minimum floors**: MINIMUM_NEW_ANALYZED_EDGE_COUNT >= 32 and
  MINIMUM_NEW_FUNCTION_BODIES_OPENED >= 7 (EXACT counts UNRESOLVED) — unchanged.
- **The historical budget FAILs (permanent historical facts, never becoming PASS)**:
  ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL;
  ORIGINAL_FUNCTION_BODY_BUDGET_COMPLIANCE = FAIL;
  ORIGINAL_SCOPE_COMPLIANCE = FAIL;
  RETROACTIVE_PRIOR_AUTHORIZATION = NO.
- **The real clean recorded bytes**: the 0x42-byte published clean window
  0x0050A3B7..0x0050A3F8 and its per-instruction record
  (PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007/01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt) —
  byte measurements, NOT superseded by any interpretation change.
- **The historical endpoint test outcomes** of the OLD checkers (clean PASS; historical
  clobber FAIL; push-esi FAIL; push-nop FAIL as measured at 57ecf350) — preserved as
  authentic historical results; NC1 adds the SIB falsifier, it does not rewrite them.
- **The getter/store byte evidence**: FUN_006C66D0 direct field getter [manager+0x68]
  (8B 41 68 C3) = CONFIRMED byte/operation fact; measured store manager+0x68 <-
  [returned_object+4] = CONFIRMED physical dataflow fact; the lazy producer chain, the
  join-window bytes (8B F8 @0x0050A3B7; 57 @0x0050A3F6; FF D2 @0x0050A3F7), all 56 byte
  pins + 23 rel32 recomputes, the RTTI names and string constants — all preserved.
- **All science ceilings and statuses (contract §10, verbatim)**:

```text
FUN_006C66D0 direct field getter [manager+0x68] =
CONFIRMED byte/operation fact

measured store manager+0x68 <- [returned_object+4] =
CONFIRMED physical dataflow fact

CHILD_RESOURCE_PROVENANCE =
STRONGLY_SUPPORTED_MODEL_DERIVED

MODEL_ROOT_RELATION =
UNKNOWN

WRAPPER_DEPTH =
UNRESOLVED

CHILD_VISUAL_ROLE =
UNRESOLVED

CHILD_TO_JOIN_IDENTITY =
STRONGLY_SUPPORTED

EXACT_PARENT =
CONFIRMED_EXACT_SCENEFEEDER_PLUS_30
scoped to examined ACLD path

JOIN_OPERATION =
STRONGLY_SUPPORTED

CAND4_CHILD_ROOT_CLOSURE =
NOT_ESTABLISHED_WITHIN_BOUND

WORLD_XYZ_RECOVERED =
NO

STATIC_BUILDING_CHANNEL =
NOT_ESTABLISHED

HISTORICAL_INSTANCE_DATA_RECOVERED =
NO
```

- The bounded evidence wording (contract §10) remains the ONLY permitted summary of the
  existing science — the established:
  `model/resource -> instance -> [instance+4] -> child`
  summary is NOT adopted by this correction:

```text
recorded producer path
    -> returned object (semantic identity unresolved)
    -> measured read [object+4]
    -> measured store manager+0x68
    -> candidate join argument
       (STRONGLY_SUPPORTED in current caller-side scope)

WORLD_INSTANCE = NOT_ESTABLISHED
MODEL_ROOT = NOT_ESTABLISHED
MAIN_VISUAL_CHILD = NOT_ESTABLISHED
```

## Governance preservation (contract §11, verbatim — permanent)

```text
MINIMUM_NEW_ANALYZED_EDGE_COUNT >= 32
EXACT_NEW_ANALYZED_EDGE_COUNT = UNRESOLVED

MINIMUM_NEW_FUNCTION_BODIES_OPENED >= 7
EXACT_NEW_FUNCTION_BODIES_OPENED = UNRESOLVED

ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL
ORIGINAL_FUNCTION_BODY_BUDGET_COMPLIANCE = FAIL
ORIGINAL_SCOPE_COMPLIANCE = FAIL

RETROACTIVE_PRIOR_AUTHORIZATION = NO

WRAPPER_DEPTH = UNRESOLVED

HISTORICAL_LINEAGE_BUDGET_CHARGE =
NEW_WRAPPER_HOPS = 2
MAX_NEW_WRAPPER_HOPS = 3
```

No remaining edge candidate is re-adjudicated and no exemption is re-pinned by this run
(that would exceed the records/QC correction scope).

## Effect statement

NC1 changes validation machinery only. It does NOT create or retract historical placement
data. No science branch, promotion, retraction or ceiling change is issued by this package;
CANONICAL_GATE_EFFECT = NONE. The remaining edge candidates, the CMO/ACLD questions and all
FORBIDDEN-SCOPE items of contract §12 stay closed to this run; the next science anchor is a
separate HUMAN decision after the independent Desktop post-audit of the NEW published
correction SHA (NEXT_EXPERIMENT_AUTHORIZED = NO).
