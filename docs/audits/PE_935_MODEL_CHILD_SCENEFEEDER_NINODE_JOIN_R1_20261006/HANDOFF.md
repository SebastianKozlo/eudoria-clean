# HANDOFF — PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006

Executor: pe-reconstruction (PE-MASTER direct dispatch, NO_NESTED_TASKS).
Phase of THIS dispatch = nauka + targeted QC + pakiet (SCIENCE + TARGETED INTERNAL QC
+ PACKAGE). Persistence (AUDIT_ENTRYPOINT row, final manifest regeneration with the
entrypoint row, commit, push, remote verification) belongs to PE-MASTER after its own
audit and fresh internal QC.

## TERMINAL BLOCK (contract §7 — actual measured)

```text
RUN_ID = PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006
BASE_SHA = 24f45e0108b922c26ff584fee9ef7749de0390b6
RESULTING_SHA / REMOTE_SHA = NONE / NOT_VERIFIED (no commit/push in this phase; PERSISTENCE_STATUS = PREPARED_NOT_PERSISTED)
SCIENCE OUTCOME = PARENT_FOUND_CHILD_UNRESOLVED
QC_VERDICT = QC_PASS (SELF_CHECK — targeted/fresh-context INTERNAL QC; NOT independent Desktop post-audit; NOT PE-MASTER qualification)
UNRESOLVED FINDINGS =
  1. CAND-4 child provenance: the child = FUN_006C66D0(ArkModelManagerMain) result — the getter body and the manager's model/resource provenance are NOT decoded/traced (function budget boundary 8/8). Proof A = UNRESOLVED.
  2. CAND-4 child visual role: no physical visual-role proof (FUN_007BF900/FUN_007BF630 on the child noted, undecoded). Proof D = UNRESOLVED.
  3. JOIN_OPERATION C = STRONGLY_SUPPORTED, not CONFIRMED: the PCG engine generation is not era-exact with the Gb12 oracle; the AttachParent-shaped inner call FUN_007BF470 is undecoded.
  4. PARENT SCOPE: the join's parent is the examined ACLD-path SF instance's +0x30 NiNode — the SAME SF class/creation chain as the contract's SF island but a DIFFERENT holder instance (ArkClientLocalDynamic+0x18, NOT the CMO+0xC0 instance). For the SF-island CMO instance, no model-child join was found in the examined chain.
  5. The resource-island completion chain past the scheduler entry FUN_006C3640 was NOT followed; FUN_008BD720 (the pinned "callback" VA) proved to be a 4-byte accessor lea eax,[ecx+0x18]; ret — the completion-handler lead is redirected through the scheduler entry.
  6. FUN_0050A310's other callers (if any) were not censused — whether the CMO installs a manager/visual through a different path is open.
BUDGET USED = functions 8/8, edges 6/6, join candidates 4/4, wrapper levels 2/2, oracle mechanisms 1/1 (NiNode::AttachChild + its AttachParent step)
CANDIDATES EXAMINED = 4 (CAND-1 CMO-path FUN_007BF500 call — REJECTED no-child/no-children-array; CAND-2 CMO-path transform write — REJECTED transform≠child; CAND-3 SF-ctor ExtraData registration — NON_MODEL metadata; CAND-4 ACLD-path slot-41 join site — EXAMINED_UNRESOLVED)
BEST CANDIDATE = CAND-4-ACLD-PATH-SLOT41-ATTACH (join site VA 0x0050A3F7)
A-STATUS (CHILD_PROVENANCE) = UNRESOLVED
B-STATUS (EXACT_PARENT) = CONFIRMED_EXACT_SCENEFEEDER_PLUS_30 (scoped: the examined ACLD-path SF instance)
C-STATUS (JOIN_OPERATION) = STRONGLY_SUPPORTED (AttachChild counterpart; F1/F2/F4/F5 byte-proven, F3 direct-call body undecoded)
D-STATUS (VISUAL_ROLE) = UNRESOLVED
WRAPPER DEPTH = 2 (FUN_006A3930 -> FUN_0050A310 -> the slot-41 join edge; the child's next wrapper FUN_006C66D0 NOT traversed)
INSTANCE_MODEL_NODE_JOIN = NOT_ESTABLISHED
RUNTIME_JOIN_OBSERVED = NO
SAME_INSTANCE_TRANSFORM_RELATION = CONFIRMED_STATIC (separate status; the CMO-path FUN_00509850 applies the SF pos/rot/scale to the same-instance SF+0x30 NiNode m_kLocal; path-conditional; NO join promotion)
CTRL-A/B/C (baseline origin) = all three causal falsifiers executed on COPIES of the SYNTHETIC_GATE_TEST_ONLY baseline fixture (qualification_gate.py): CTRL-A parent->other-node FAIL by the PARENT predicate (+ a legitimate operation-parent consistency cascade); CTRL-B child-provenance-removed FAIL by the CHILD predicate; CTRL-C identity-edge(+0x30->+0x34) FAIL by the PARENT-IDENTITY predicate; the REAL CAND-4 chain FAILS the gate (no rubber-stamping); the baseline PASS proves the gate is not checker-always-FAIL. The synthetic fixture is NOT recorded as PCG finding/evidence and does NOT promote any claim.
RESOURCE SIDE STATUS = request pair {0x66,A} emission + scheduler entry re-pinned MATCH (CH1); FUN_008BD720 = accessor (NEW finding); completion chain NOT followed (budget boundary); A<->296445.nif data join = inherited prior canon, not re-run
SF SIDE STATUS = PA1-PA4 re-pinned MATCH; NEW: FUN_00509510/FUN_00509070 setters, FUN_00509850 update (transform application + model-manager calls), FUN_0050A310 visual install (the join site), FUN_007BF500 (not an attach)
MANIFEST_ROWS (without entrypoint) = see MANIFEST_SHA256.csv (generated LAST over the package's physical files minus itself; the AUDIT_ENTRYPOINT.md row is EXPLICITLY OUT of this phase's manifest scope — the persistence phase regenerates the manifest together with the entrypoint row)
PHYSICAL_PACKAGE_FILE_COUNT = manifest rows + 1 (the manifest itself)
BIJECTION = verified at generation: zero missing / extra / duplicate / size-mismatch / SHA-mismatch (see 03_SCRIPTS/make_manifest.py output below and the bijection record)
CHANGED PATHS (this phase) = OUTPUT_ROOT/** only (docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/); AUDIT_ENTRYPOINT.md NOT edited; no commit; no push; foreign untracked untouched
FINAL_EXTRADATA_STORAGE = NOT_CHECKED (FUN_007B68B0 remained DEFERRED_LEAD; the declared dependency was never triggered — PRE_REGISTERED_ANCHORS.md §DEFERRED_LEAD)
WORLD_XYZ_RECOVERED = NO
STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED
HISTORICAL_INSTANCE_DATA_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO
NOT_CHECKED (explicit) = FUN_006C66D0, FUN_007BF470, FUN_007B5A00, FUN_006C0EC0/ED0/FA0/FB0/F90/10B0, FUN_0050A1E0, FUN_005246E0, FUN_00509670, FUN_0096CDD0, FUN_0048BAC0, FUN_006C3640, FUN_006C8B20/BB0 internals, the resource completion chain, the ExtraData readback, runtime anything, payload/VFS/BNT/NIF contents
HARD_STOP = YES (after package + manifest + bijection verification)
```

## PROPOSED AUDIT_ENTRYPOINT.md newest-first row (NOT applied by this executor)

The persistence phase should add this row at the TOP of AUDIT_ENTRYPOINT.md
(newest-first), adapted to the entrypoint's current column format:

| RUN_ID | PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006 |
|---|---|
| DATE | 2026-10-06 |
| PACKAGE | docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/ |
| BASE_SHA | 24f45e0108b922c26ff584fee9ef7749de0390b6 |
| RESULT | PARENT_FOUND_CHILD_UNRESOLVED — a join site byte-proven on the ArkClientLocalDynamic path: NiNode vtable slot 41 (FUN_007B5810 = NiNode::AttachChild counterpart, STRONGLY_SUPPORTED by the Gb12 oracle fingerprint) called with receiver = the exact examined-path SF+0x30 NiNode and a child derived from the ArkModelManagerMain (FUN_006C66D0 getter, undecoded); child model/resource provenance (A) and visual role (D) UNRESOLVED at the budget boundary (8/8 functions, 6/6 edges, 4/4 candidates, 1/1 oracle); INSTANCE_MODEL_NODE_JOIN = NOT_ESTABLISHED; SAME_INSTANCE_TRANSFORM_RELATION = CONFIRMED_STATIC (separate status) |
| SUPERSESSIONS | none introduced; carries the SF-island/instance-key supersession routing (POST_AUDIT_CORRECTION package) and the R2 anchor-constraint adjudications (HANDOFF_NOTES: FUN_006CB020 = NiControllerSequence — not a visual-child anchor; FUN_006CB3C0 without label priority; 0x00779F80 = StopMorph STRONGLY_SUPPORTED; the 0x00779D60/0x00779E20 "ARK_LOD_STATE_MACHINE" label superseded for ranking) |
| STATUS | PREPARED_NOT_PERSISTED (this executor phase: science + targeted internal QC + package; commit/push = the persistence phase) |

## Key artifact paths

- FINAL_REPORT.md — the science close (authoritative for this phase).
- CANDIDATE_LEDGER.csv — all 4 examined candidates incl. CAND-4 (the join site).
- 01_RAW/FUN_0050A310_DECODE.txt + 01_RAW/FUN_007B5810_ORACLE_BYTE_PROOF.txt — the join site + the operation byte proof.
- 03_SCRIPTS/qualification_results.json + 03_SCRIPTS/qc_reverify_results.json — the machine gate + QC.
- MANIFEST_SHA256.csv — final manifest (generated LAST; without the entrypoint row — see the terminal block).

## HARD STOP

After the package + manifest + bijection verification: HARD STOP. No next RE, no
historical producer search, no ExtraData readback, no 0xA4, no client launch, no
commit/push by this executor. NEXT_EXPERIMENT_AUTHORIZED = NO.
