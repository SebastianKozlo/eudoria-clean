# CORRECTED_LINEAGE_STATUS — PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007

Wrapper / pointer-lineage record correction (correction contract §4). This file
supersedes the SOURCE run's WRAPPER/lineage CLAIMS (see SUPERSESSION.md) while
preserving every measured dataflow fact and the historical budget consumption.
Basis: the correction contract §4 + the SOURCE package's POINTER_LINEAGE.csv
(H-1..H-4, READ-ONLY) + FINAL_REPORT.md/HANDOFF.md of the audited run.

## 1. Corrected statuses (authoritative for this correction package)

```text
WRAPPER_DEPTH = UNRESOLVED
MODEL_ROOT_RELATION = UNKNOWN
POINTER_LINEAGE_TRANSITIONS_OBSERVED = 2
H-2 RELATION_TYPE = UNRESOLVED
NEW_WRAPPER_HOPS (historical budget consumption, PRESERVED) = 2
MAX_NEW_WRAPPER_HOPS (unchanged source-run limit) = 3
```

- WRAPPER_DEPTH = UNRESOLVED — SEMANTICS != BUDGET CONSUMPTION. The number of charged
  analysis units is NOT the number of proven wrapper layers. What is physically
  established: H-1 is a measured containment (the manager stores/contains the created
  instance at [+0x6C] — a separate object with its own lifetime; RELATION_TYPE
  WRAPPER_CONTAINS per POINTER_LINEAGE.csv). H-2's relation — whether [instance+4] is the
  instance's contained model root, a handle, or a reference-count slot of a wrapper class
  (the prior-canon ArkModelResourceInstanceRef map: refcount@+4/item@+8 CONTRADICTS
  pointer use if the pump returns that wrapper) — is NOT physically established (would
  require opening FUN_006C9700, which is not authorized). Therefore the semantic wrapper
  depth between the manager and the CAND-4 child is UNRESOLVED. The SOURCE run's
  "WRAPPER_DEPTH = 2 (manager -> instance [+0x6C]; instance -> [+4]; the further moves to
  the join are SAME_OBJECT)" (FINAL_REPORT §1 answer 2; HANDOFF; PE_MASTER_REVIEW
  CLAIM MATRIX line) is SUPERSEDED as a semantic-proof claim.

- MODEL_ROOT_RELATION = UNKNOWN — standing, unchanged (the §5 enum is not resolved; no
  clone operation observed on the path; raw-vs-wrapper vs actor-family identity
  unresolved at the [instance+4] boundary).

- POINTER_LINEAGE_TRANSITIONS_OBSERVED = 2 — this is a DESCRIPTION of the two examined
  lineage transitions (H-1, H-2 below), NOT a global census and NOT a claim that the
  pointer lineage of the child contains exactly two transitions everywhere:

  | hop | transition | recorded physical basis | relation status |
  |---|---|---|---|
  | H-1 | ArkModelManagerMain instance -> [manager+0x6C] (the created resource instance handle) | store `mov [esi+0x6C], eax` @0x006C7008 (89 46 6C) inside FUN_006C6F60 | WRAPPER_CONTAINS (measured store; the instance object's class NOT established) — CONFIRMED as a physical containment fact |
  | H-2 | the created instance -> [manager+0x68] via [instance+4] | load `mov edi,[eax+4]` @0x006C67BE (8B 78 04); store `mov [esi+0x68],edi` @0x006C67E2 (89 7E 68); incref [edi+4] @0x006C67E7; old-value decref + zero-destroy via vtable slot 1 @0x006C67D4/0x006C67DE | PHYSICAL DATAFLOW CONFIRMED (the store is measured); RELATION_TYPE = UNRESOLVED |

  H-3 and H-4 of POINTER_LINEAGE.csv are SAME_OBJECT register moves (EDI = EAX
  @0x0050A3B7; the EDI value crossing the four intervening calls to the two child
  arguments @0x0050A3D7/@0x0050A3F6) — NOT lineage transitions; the four intervening
  callee bodies remain UNOPENED (ABI support, not proof).

- H-2 RELATION_TYPE = UNRESOLVED — unchanged from POINTER_LINEAGE.csv; the physical
  dataflow (load/store/refcount protocol bytes) is a measured fact and is NOT superseded.

## 2. Historical budget consumption (PRESERVED — not zeroed, not reduced)

```text
NEW_WRAPPER_HOPS = 2  (charged analysis units of the original run: H-1 and H-2)
MAX_NEW_WRAPPER_HOPS = 3  (the preregistered source-run limit, unchanged)
```

- The source-run contract §3 (MAX_NEW_WRAPPER_HOPS) covered ALL new typed lineage hops
  (clone, containment, selected subtree, target) that were EXAMINED — not only proven
  semantic wrappers. H-1 and H-2 were both examined; both charged. The budget
  consumption of the UNRESOLVED H-2 stands: an unresolved relation still consumes the
  budget (a hop was spent examining it; its semantic resolution was not achieved within
  the bound). This correction does NOT zero, refund or reduce the historical charge —
  and does not claim the two charged units establish two layers of model wrappers
  (§1: WRAPPER_DEPTH = UNRESOLVED).
- Budget arithmetic of the lineage component (historical, unchanged): 2 of 3 used —
  WITHIN the wrapper-hop limit. This is a budget-compliance fact only; it is NOT a
  semantic wrapper-depth result and NOT a scope-compliance exoneration of the audited
  run (ORIGINAL_SCOPE_COMPLIANCE = FAIL stands on the edge and body budgets — see
  CORRECTED_EDGE_ACCOUNTING_LEDGER.csv and FUNCTION_BODY_ACCOUNTING.csv).

## 3. What is NOT changed by this correction

- Every byte/dataflow measurement cited in §1 (the H-1 store bytes; the H-2 load/store/
  refcount protocol bytes; the join-window register facts) is a measured fact of the
  audited run and is preserved (science preservation — correction contract §5).
- POINTER_LINEAGE.csv of the SOURCE package is a historical record and is NOT edited;
  this file is the corrected lineage-status record of THIS package.
- No promotion of MODEL_ROOT_RELATION, CHILD_VISUAL_ROLE, CHILD_TO_JOIN_IDENTITY or
  CAND4_CHILD_ROOT_CLOSURE occurs here (standing statuses: UNKNOWN / UNRESOLVED /
  STRONGLY_SUPPORTED (NOT CONFIRMED) / NOT_ESTABLISHED_WITHIN_BOUND).
