# SUPERSESSION_AND_STANDING — PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009

Documentary standing record per contract §2/§8. This run SUPERSEDES no prior
package, rewrites no historical file and restores no superseded conclusion; it
adds ONE bounded upstream-delivery qualification for the already recorded
callsite pair, with strict scope fences. All historical packages and
supersessions remain immutable.

## 1. Prior standing preserved VERBATIM (carried, not re-derived, not reinterpreted)

```text
S = ESP at 0x00528E76, not function-entry ESP
0x00528E84: EDI := DWORD [S+0x3C]
0x00528E8A: PUSH EDI
0x00528E8D: CALL 0x0085B1B0
ARG1_DIRECT_SOURCE = CONFIRMED_STATIC_CONDITIONAL
UPSTREAM_PROVENANCE = UNRESOLVED_UPSTREAM (prior bounded result)
CMO_C1 = CLOSED_FOR_AUDITED_STATE
CORE_RECEIVER_VALUE_CHAIN = PRESERVED_CONFIRMED_STATIC_CONDITIONAL
```

J3 preserved verbatim:

```text
PHYSICAL_TRANSFORM_MEASUREMENTS = PRESERVED
NEW_TRANSFORM_TRACE = MEASURED_INCIDENTAL_OUTSIDE_PERMITTED_PROMOTION
SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN = NOT_QUALIFIED_BY_ORIGINAL_SCOPE
```

No transfer of object identity between ACLD+0x18 SF and CMO+0xC0 SF. R/P/T,
PLUS4 and CMO-C1 correction loops remain closed in their audited scopes.
Historical labels such as record/position are not type evidence.

## 2. This run's relation to the standing

- CONSISTENT, NOT SUPERSEDING: the prior result ARG1_DIRECT_SOURCE (arg1 of
  FUN_0085B1B0 at CALL 0x00528E8D = the value loaded from [S+0x3C] at
  0x00528E84, delivered by PUSH EDI at 0x00528E8A) is re-derived independently
  this run from the extended window A (now including the entry frame):
  S = E-0x38 (E = symbolic ESP at entry 0x00528E50), [S+0x3C] = [E+4], arg1
  slot = [S-0xC]. All values match the prior pinned result; nothing in it is
  reopened or contradicted.
- ONE NEW QUALIFIED BOUNDARY: for the SINGLE caller path through window B
  (CALL 0x004C47C1, qualified only on the EAX!=0 branch under the recorded
  normal ABI-compatible opaque-return condition of 0x0095D3C4), the upstream
  delivery is now qualified one step: the entry first stack argument slot of
  FUN_00528E50 ([E+4] == [T-0x10], where E = T-0x14) is prepared by
  PUSH ECX at 0x004C47BE with ADDRESS(T+8) — the address computed by
  LEA ECX,[ESP+0x14] at 0x004C47BA — and that SAME pointer value travels
  through the load at 0x00528E84 into EDI and out at PUSH EDI 0x00528E8A as
  arg1 of FUN_0085B1B0. Status:
  CROSS_CALL_IDENTITY = POINTER_VALUE_IDENTITY_ESTABLISHED_CONDITIONAL
  (conditions: AS1/AS2 x86 stack semantics; AS3 opaque normal return; the
  EAX!=0 qualified branch; AS4 FS/TIB disjointness; straight-line window-A
  path; no claim of uniqueness across unexamined callers/entries/paths).
- UPSTREAM_PROVENANCE is therefore PARTIALLY resolved for this callsite path
  only: the FIRST upstream boundary (who supplies [E+4] and with what value)
  is qualified as above. Everything BEYOND remains UNRESOLVED_UPSTREAM:
  the contents of the pointed-to area at [T+8] (the pointee), its producer
  before the examined frames, its type, its lifetime and its history are NOT
  traced (UPSTREAM_BEYOND_WINDOW_B = 0 in this run).

## 3. Scope fences and status fields (required by the contract)

```text
FIELD_SEMANTICS = UNVERIFIED
POINTEE_CONTENTS_PROVENANCE = UNRESOLVED_UPSTREAM
WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED
HISTORICAL_PLACEMENT = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
```

The qualified relation is a POINTER_VALUE_IDENTITY across two delivery
boundaries (ARGUMENT_DELIVERY at the FUN_00528E50 entry via CALL 0x004C47C1;
ARGUMENT_DELIVERY at the FUN_0085B1B0 entry via CALL 0x00528E8D). It does NOT
prove any value inside [T+8], any type/lifetime beyond the examined calls, the
caller's global frame layout, or the history of that stack area. No full
signature is inferred from visible pushes. No position, NiPoint3, world
instance, building, network packet, model or XYZ is assumed. No OpenMW or
Gamebryo engine was researched or loaded in this run.

## 4. Not reopened / not restored (list)

- The [arg1+8] -> MovableObject+0x44 store and its callee: NOT reinterpreted;
  callee 0x0085B1B0 NOT re-opened (its pinned consumption facts were carried
  unchanged from the prior package; not re-derived here).
- Callee 0x0095D3C4: treated strictly opaque (no body, no heap-origin claim,
  no allocator-wide semantics; the normal ABI-compatible return condition is
  recorded as assumption AS3, never verified by opening it).
- CMO_C1 = CLOSED_FOR_AUDITED_STATE — unchanged.
- CORE_RECEIVER_VALUE_CHAIN = PRESERVED_CONFIRMED_STATIC_CONDITIONAL —
  unchanged (the receiver ECX channel is separate from the arg1 channel in
  both windows of this run as well).
- J3 supersession records (S-1..S-4 of the 20261007 correction package) —
  unchanged; ORIGINAL_J3_EDGE_BUDGET_COMPLIANCE = FAIL stands as recorded.

## 5. Open findings / remaining uncertainty (carried to the parent)

1. AS3: the normal ABI-compatible return condition of opaque callee
   0x0095D3C4 is an explicit assumption (callee unopened). If unsupported at
   any future audit, the Phase-B and bridge results stay CONDITIONAL and must
   not be silently promoted.
2. AS4: the FS segment base (TIB) disjointness from the live argument stack
   region is an explicit assumption; the runtime FS base is not statically
   resolvable in this bounded static run.
3. The EAX==0 branch of window B exits the window at 0x004C47C8 and is NOT
   interpreted; nothing is asserted about allocation success or the
   out-of-window branch.
4. ESI at window-B entry (the T-point value pushed as the third argument) has
   an UNKNOWN producer (outside window B; not traced).
5. Fresh internal QC: NOT_PERFORMED_BY_THIS_WORKER (separate fresh-QC worker
   per dispatch); the QC side of the 24-outcome matrix (12 QC_FRESH rows of
   CLAIM_MATRIX.csv) is pending that session.
6. Session continuity: this package originates from TWO executor sessions
   (crashed first session wrote PREREGISTRATION.md + the two window objdump
   files; the fresh retry session verified them and produced everything else).
   See PREREGISTRATION.md P10 and INPUT_IDENTITIES.md I2.

## 6. Phase boundaries of THIS record (delegation)

This production executor phase wrote only, under OUTPUT_ROOT:
PREREGISTRATION.md (P10 extension), INPUT_IDENTITIES.md,
WINDOW_IDENTITIES.json, 01_RAW/WINDOW_{A,B}_OBJDUMP_RETRY.txt,
01_RAW/CONTROLS/<CASE>_OBJDUMP.txt (12 files), ENTRY_FRAME_LEDGER.csv,
CALLER_STACK_LEDGER.csv, BRIDGE_PROVENANCE.json, CLAIM_MATRIX.csv,
CONTROL_RESULTS.json, ARTIFACT_CONTROL_RESULTS.json,
SUPERSESSION_AND_STANDING.md (this file) and
03_SCRIPTS/run_frame_bridge.py. The two window objdump raw files are the
verified crash-session files (kept unchanged). NOT this phase:
qc_frame_bridge.py/QC_RESULTS.json/QC_REPORT.md (fresh-QC worker);
FINAL_REPORT.md/PE_MASTER_REVIEW.md/EVIDENCE_INDEX.md/HANDOFF.md/MANIFEST/
AUDIT_ENTRYPOINT.md row/any stage/commit/push (parent phases). No commit, no
push, no entrypoint write was performed by this phase.
