# HANDOFF — PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007

Executor: pe-reconstruction (PE-MASTER direct dispatch, NO_NESTED_TASKS).
Phase of THIS dispatch = SCIENCE (bounded static RE §4–§7) + the four §9
controls + fresh-context internal QC (SELF_CHECK) + PACKAGE. Persistence
(AUDIT_ENTRYPOINT row, manifest regeneration with the entrypoint row, one
commit, push, remote verification) belongs to PE-MASTER after its own audit of
this package. This executor does NOT edit AUDIT_ENTRYPOINT.md (proposed
newest-first row below) and does NOT commit/push (RESULTING_SHA = NONE this
phase).

## TERMINAL BLOCK (contract §12 / dispatch handoff — actual measured)

```text
RUN_ID = PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007
BASE_SHA = d65fa12e5bae4e9aab291c3cc7815b1822e41cff
RESULTING_SHA = NONE (this phase; no commit/push by this executor)
REMOTE_SHA = d65fa12e5bae4e9aab291c3cc7815b1822e41cff (remote verified UNCHANGED
  at preflight 2026-10-07T10:54:17Z: actual remote master == origin/master ==
  LOCAL_HEAD == BASE_SHA; no write to the remote occurred in this phase)
GETTER_OPERATION = DIRECT_FIELD_GETTER (FUN_006C66D0 = 4-byte body:
  mov eax,[ecx+0x68]; ret; extent 0x006C66D0..0x006C66D4 RESOLVED by terminal
  ret + 12x int3 padding + aligned next entry 0x006C66E0)
ARKMODELMANAGER_CHILD_FIELD_OFFSET = 0x68 (measured; the ArkModelManagerMain
  BASE-class region; RTTI .?AVArkModelManagerMain@@ / .?AVArkModelManager@@
  measured from the vtable COL chains)
CHILD_RESOURCE_PROVENANCE = STRONGLY_SUPPORTED_MODEL_DERIVED (the producer
  chain is byte-proven: base-ctor NULL write @0x006C8FD3 -> lazy trigger
  FUN_006C8B20 -> producer FUN_006C6F60 [validity FUN_0072FCE0; empty-string-key
  lookups; getter A = FUN_007CE1E0; instance = FUN_006C9700 pump -> [+0x6C]]
  -> writer FUN_006C6780: [manager+0x68] = [instance+4] @0x006C67E2 with the
  refcounted smart-pointer protocol; NOT CONFIRMED_MODEL_DERIVED — [instance+4]
  identity UNRESOLVED (GAP-1) and the alternative on-path producer FUN_006C8BB0
  NOT_CHECKED (GAP-2))
MODEL_ROOT_RELATION = UNKNOWN (physical facts recorded: refcounted object,
  refcount@+4, named-lookup root for the measured constants 'ArkTexture'
  (0x00A859F8) and 'ArkAnimation' (0x00A8547C), attached to the SF+0x30 NiNode;
  raw-vs-wrapper vs actor-family identity unresolved at the [instance+4]
  boundary; no clone operation observed on the path; the OpenMW/GB2.6 oracles
  are NOT on local disk — NOT_USED)
WRAPPER_DEPTH = 2 (manager -> created instance [+0x6C]; instance -> [instance+4]
  -> [+0x68]; the moves to the join are SAME_OBJECT, not hops)
CHILD_VISUAL_ROLE = UNRESOLVED (no positive §6 principal-visual proof; the
  measured positive evidence — model-instance-family production, NiObject-
  family refcount protocol, named texture/animation component lookups, the
  attach into the SF's visual root — is not sufficient per contract §6; VFX/
  helper alternatives not excluded; FUN_007BF900/FUN_007BF630 undecoded)
CHILD_TO_JOIN_IDENTITY = STRONGLY_SUPPORTED (NOT CONFIRMED: the caller window
  is measured clean of EDI writes between mov edi,eax @0x0050A3B7 and push edi
  @0x0050A3F6 — free re-pin of the source run's QC S4 — but the FOUR
  intervening callee bodies (FUN_006C0F90/FUN_006C10B0/FUN_0050A1E0/
  FUN_005246E0) were NOT opened; the MSVC callee-saved ABI is support, not
  proof — the honest §7 fallback)
EXACT_PARENT = CONFIRMED_EXACT_SCENEFEEDER_PLUS_30 (carried, scoped to the
  examined ACLD+0x18 SF instance; window re-pinned byte-identical; NO
  identity/transform transfer from the CMO+0xC0 holder)
JOIN_OPERATION = STRONGLY_SUPPORTED (carried; the ceiling of this run;
  FUN_007BF470 NOT opened)
CAND4_CHILD_ROOT_CLOSURE = NOT_ESTABLISHED_WITHIN_BOUND (CHILD_EVIDENCE_COMPLETE
  = FALSE: provenance != CONFIRMED_MODEL_DERIVED, visual role UNRESOLVED,
  identity != CONFIRMED; §8 algebra literal — the chain does not advance past
  its weakest required edge)
NEW_FUNCTION_BODIES_OPENED = 6/6 (FUN_006C66D0; FUN_006C0D50; FUN_006C8F80;
  FUN_006C8B20; FUN_006C6F60; FUN_006C6780 PARTIAL with extent UNRESOLVED past
  0x006C6848 — the load-bearing facts are inside the seen window)
NEW_INTERPROCEDURAL_EDGES_SEMANTICALLY_ANALYZED = 24 (vs MAX 8 — EXCEEDED;
  disclosed honestly by this run itself in EDGE_ACCOUNTING_LEDGER.csv)
NEW_MANAGER_FIELD_WRITERS_TRACED = 2/6 (W1 NULL reset @0x006C8FD3; W2 value
  producer @0x006C67E2) + 3 declared gaps (GAP-1 creation-chain internals;
  GAP-2 FUN_006C8BB0; GAP-3 off-path writers out of scope by governance)
NEW_CHILD_PROVENANCE_CANDIDATES = 3/3 (ctor reset; producer chain; FUN_006C8BB0
  alternative — the limit reached exactly)
INDEPENDENT_RECONSTRUCTED_EDGE_COUNT = 24 (== ACCOUNTED_EDGE_COUNT; the QC
  additionally re-enumerated all 26 CALL instructions in the 6 analyzed
  extents — 100% ledger coverage, zero missing)
EDGE_ACCOUNTING_STATUS = BUDGET_EXCEEDED (24 > MAX 8; 16 past the stop line;
  ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL; RETROACTIVE_PRIOR_AUTHORIZATION = NO;
  the historical minimum-22 pair convention of the source run is unchanged;
  the byte evidence is not falsified by the exceedance — full census per the
  J2 lesson: every uncounted row carries an explicit reason)
SCOPE_COMPLIANCE = PARTIAL_WITH_EXCEEDED_EDGE_BUDGET (bodies 6/6 within; edges
  exceeded; writers within; hops 2/3 within; candidates 3/3 at limit)
CTRL_1_RESULT = PASS (animation false positive: the pinned NiControllerSequence
  does not qualify as main visual through model-adjacency — same checker clean
  PASS -> adjacency-only FAIL; the REAL child input is classified POLICY_ONLY)
CTRL_2_RESULT = PASS (wrapper relation break: the containment/field-store
  predicate does not survive the broken relation — same checker, same range)
CTRL_3_RESULT = PASS (wrong manager field: correct bytes of a foreign manager
  field do not qualify as provenance of THIS getter — same checker, same shape)
CTRL_4_RESULT = PASS (child identity break: an EDI clobber between the head move
  and push edi breaks the return->final-child relation — same checker, same
  window)
QC_VERDICT = SELF_CHECK QC_PASS 23/23 (fresh-context internal QC, origin =
  the executor per contract §9 — NOT independent Desktop post-audit; NOT
  PE-MASTER qualification; two QC-tooling defect rounds found and fixed in the
  QC scripts only, disclosed in QC_REPORT.md §6; no executor evidence modified)
MANIFEST_ROWS = 27 (physical package files minus the manifest itself;
  AUDIT_ENTRYPOINT.md EXCLUDED pending persistence — noted in the manifest
  header; the persistence phase regenerates the manifest over the final
  physical package together with the entrypoint row)
PHYSICAL_PACKAGE_FILE_COUNT = 28 (27 package files + MANIFEST_SHA256.csv)
MANIFEST_BIJECTION = VERIFIED (generator self-check + INDEPENDENT post-
  generation re-hash by a separate implementation — zero missing/extra/
  duplicate/size/SHA mismatch; see §Manifest verification below)
OPEN_FINDINGS =
  1. The identity of [instance+4] (GAP-1) — the single highest-value next
     input: decode FUN_006C9700/the creation chain and reconcile with the
     prior-canon ArkModelResourceInstanceRef field map (refcount@+4/item@+8
     CONTRADICTS pointer use if the pump returns that wrapper).
  2. FUN_006C8BB0 (GAP-2) — an alternative on-path producer of [+0x68] cannot
     be excluded.
  3. The §7 preservation bodies (FUN_006C0F90/FUN_006C10B0/FUN_0050A1E0/
     FUN_005246E0) — CHILD_TO_JOIN_IDENTITY can rise toward CONFIRMED only
     with their bodies.
  4. The child's class/role evidence: FUN_007B6C30, FUN_007BF900/
     FUN_007BF630, the manager slot-2/slot-3 targets (0x006C0FD0/0x006C19B0).
  5. The positive §6 visual-role proof — the missing required leg for any
     future closure.
  6. The FUN_006C6780 unseen continuation (extent UNRESOLVED past 0x006C6848).
NOT_CHECKED (explicit) = FUN_006C8BB0; FUN_006C9700 and the whole creation
  chain; FUN_005670A0; FUN_0043A330; FUN_006C7740; FUN_006C7B40;
  FUN_006C0FD0; FUN_006C19B0; FUN_006C66E0; FUN_006C6CE0; FUN_007B6C30;
  FUN_006D3570; FUN_006C0F90; FUN_006C10B0; FUN_0050A1E0; FUN_005246E0;
  FUN_007BF470 (forbidden — join ceiling); FUN_007BF900; FUN_007BF630;
  FUN_006C0EC0/ED0/EE0/EF0/F80/FA0/FB0/FC0 and every other neighbor body
  (NEIGH rows); the FUN_006C6780 continuation; the import targets [0xA75A38/
  0xA75A44/0xA75A48/0xA75A5C/0xA75A40]; runtime anything (STATIC-ONLY);
  payloads; the independent PE-MASTER audit of this package (pending)
CHANGED_PATH_CENSUS = exclusively docs/audits/PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007/**
  (27 physical files incl. the manifest; created by this run). ZERO tracked
  modifications; the 6 foreign untracked roots untouched; AUDIT_ENTRYPOINT.md
  NOT edited; the two prior evidence packages re-verified read-only
  (49/49 + 27/27 BASE blob identity before AND after work)
REAL_SCIENCE_AUTO_QUALIFICATION = DISABLED
RUNTIME_JOIN_OBSERVED = NO
WORLD_XYZ_RECOVERED = NO
STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED
HISTORICAL_INSTANCE_DATA_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES (after package + manifest + bijection; no commit/push by this
  executor)
```

## Manifest verification (per the every-write-after-the-manifest rule)

MANIFEST_SHA256.csv is generated LAST (at package time this HANDOFF and every
other package file were already on disk; the F-QC-A..F-QC-E records-repair
regenerated it LAST again after its edits — record-repair log: QC_REPORT.md
§8); scope = the physical OUTPUT_ROOT files minus the manifest itself (the
00_CONTROL_INTERNAL_QC/ records of the internal QC stay OUT pending the
persistence-phase regeneration over the final physical package); entrypoint
EXCLUDED pending persistence (noted in the manifest header). Bijection: the
generator's self-check (zero missing/extra/duplicate/size/SHA mismatch),
re-run at the regeneration. INDEPENDENT re-hash of the manifest: the
executor-phase manifest was independently re-hashed by the internal QC
(00_CONTROL_INTERNAL_QC/QC_IND_RESULTS.json — 27/27 size+SHA256 MATCH, zero
mismatch); the records-repair regeneration is independently re-hashed by a
separate implementation with the result reported in the records-repair
session's terminal response (not persisted as a package file, to keep the
manifest LAST); the persistence phase repeats the re-hash over the final
physical package. The executor-phase QC_REPORT.md checks (§1-§7, written
before the manifest generation) contain no re-hash record. Any write after
the manifest requires regeneration + re-verification.

## PROPOSED AUDIT_ENTRYPOINT.md newest-first row (NOT applied by this executor)

The persistence phase should add this row at the TOP of AUDIT_ENTRYPOINT.md
(newest-first), adapted to the entrypoint's current column format:

| RUN_ID | PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007 |
|---|---|
| DATE | 2026-10-07 |
| PACKAGE | docs/audits/PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007/ |
| BASE_SHA | d65fa12e5bae4e9aab291c3cc7815b1822e41cff |
| RESULT | CAND4_CHILD_MODEL_ROOT_PROVENANCE (bounded static RE; executor phase: science + §9 controls + internal QC SELF_CHECK 23/23 + package; no commit/push this phase — RESULTING_SHA = NONE). THE CHILD GETTER DECODED: FUN_006C66D0 = 4-byte DIRECT FIELD GETTER (mov eax,[ecx+0x68]; ret; extent resolved); ARKMODELMANAGER_CHILD_FIELD_OFFSET = 0x68. PRODUCER CHAIN BYTE-PROVEN on the examined ACLD path: base ctor NULL write (@0x006C8FD3) -> FUN_006C8B20 lazy trigger -> FUN_006C6F60 producer (FUN_0072FCE0 validity; empty-string-key lookups; getter A = FUN_007CE1E0; instance-creator pump FUN_006C9700 -> [manager+0x6C]) -> WRITER FUN_006C6780: [manager+0x68] = [instance+4] @0x006C67E2 (refcounted smart-pointer set; NiObject-family protocol) + conditional named lookups 'ArkTexture'/'ArkAnimation' ON the child. STATUSES: CHILD_RESOURCE_PROVENANCE = STRONGLY_SUPPORTED_MODEL_DERIVED (NOT CONFIRMED: [instance+4] identity GAP-1; FUN_006C8BB0 GAP-2); MODEL_ROOT_RELATION = UNKNOWN; CHILD_VISUAL_ROLE = UNRESOLVED (no positive §6 proof); CHILD_TO_JOIN_IDENTITY = STRONGLY_SUPPORTED (4 intervening bodies unopened; ABI = support not proof); EXACT_PARENT = CONFIRMED_EXACT_SCENEFEEDER_PLUS_30 (carried); JOIN_OPERATION = STRONGLY_SUPPORTED (ceiling); CAND4_CHILD_ROOT_CLOSURE = NOT_ESTABLISHED_WITHIN_BOUND (§8 algebra literal). BUDGET: bodies 6/6; writers 2/6 (+3 gaps); hops 2/3; candidates 3/3; EDGES EXCEEDED — 24 analyzed callsite units vs MAX 8 (EDGE_ACCOUNTING_STATUS = BUDGET_EXCEEDED; ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL; RETROACTIVE_PRIOR_AUTHORIZATION = NO; full census disclosed per the J2 lesson; byte evidence not falsified). CONTROLS: CTRL_1..4 all PASS (machinery falsifiability; CTRL_1 real input = POLICY_ONLY). RTTI measured: .?AVArkModelManagerMain@@ / .?AVArkModelManager@@ / .?AVArkModelResourceInstanceRef@@. NEXT_EXPERIMENT_AUTHORIZED = NO. |
| SUPERSESSIONS | none (this run adds new science records; the J1–J3 supersessions of the prior correction run remain in force; the historical qualification gate remains NOT a positive qualifier; the source run's minimum-22 pair convention unchanged) |
| STATUS | SCIENCE_EXECUTED_PENDING_PE_MASTER_AUDIT (executor phase complete: package + manifest LAST + bijection verified; entrypoint update/commit/push = the PE-MASTER persistence phase after its own audit; publication != acceptance) |

## Key artifact paths

- GETTER_DECODE.md — the §4 deliverable (getter + operation class + offset + producer trace).
- 01_RAW/FUN_006C66D0_GETTER_FULL.txt … 01_RAW/FUN_006C6780_INSTALLER_PARTIAL.txt — the six body decodes (raw bytes + instructions + extent provenance).
- 01_RAW/PINS_AND_REL32.txt — 56 byte pins + 23 rel32 recomputes (+ prior-record cross-checks).
- 01_RAW/VTABLE_RTTI_STRINGS.txt — the measured RTTI names and string constants.
- 01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt — the §7 chain re-pin + honest STRONGLY_SUPPORTED basis.
- EDGE_ACCOUNTING_LEDGER.csv — the full 24-unit census + 45 non-counted rows with explicit reasons.
- FIELD_PRODUCER_LEDGER.csv / POINTER_LINEAGE.csv / CLAIM_MATRIX.csv — the writer census, the typed lineage, the claims.
- 03_SCRIPTS/qc_controls.py + CONTROL_RESULTS.json — the four §9 controls (all PASS).
- 03_SCRIPTS/qc_internal.py + QC_INTERNAL_RESULTS.json + QC_REPORT.md — the internal QC (QC_PASS 23/23; two QC-tooling defect rounds disclosed, fixed in the QC scripts only).
- FINAL_REPORT.md — the full answer with statuses, budget accounting, open items.
- PE_MASTER_REVIEW.md — placeholder (NOT_PERFORMED-do-persistence).
- MANIFEST_SHA256.csv — generated LAST (entrypoint excluded pending persistence).
- GOVERNANCE_DECISION.md / INPUT_IDENTITIES.md / PREREGISTRATION.md — the authorization, identities, preregistration.

## HARD STOP

After the package + manifest + bijection verification: HARD STOP. No next RE,
no FUN_006C9700/FUN_006C8BB0 decoding, no §7 preservation bodies, no
visual-role RE, no runtime, no commit/push by this executor.
NEXT_EXPERIMENT_AUTHORIZED = NO. Any write after the manifest requires manifest
regeneration + re-verification (the every-write-after-the-manifest rule of the
verbatim human instruction of 2026-10-07).
