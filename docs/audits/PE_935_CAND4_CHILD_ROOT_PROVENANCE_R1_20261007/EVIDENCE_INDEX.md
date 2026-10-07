# EVIDENCE_INDEX — PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007

Index of every evidence artifact of the package, with its role. All EXE-derived
records are fresh reads through the fail-closed pinned reader (EXE identity:
INPUT_IDENTITIES.md §1); the decoder identity is INPUT_IDENTITIES.md §4
(capstone 5.0.7 + own rel32 arithmetic, cross-checked).

## Governance / identity records

| path | role |
|---|---|
| GOVERNANCE_DECISION.md | the verbatim human authorization, the phase-boundary adjudication (NO entrypoint edit, NO commit/push this phase), preflight record, contract identity |
| INPUT_IDENTITIES.md | all input identities (EXE, contract, prior packages + aggregate hashes, decoder identity, oracle availability ruling, scratch) |
| PREREGISTRATION.md | preregistered budgets, adaptive plan, pre-commitments (written BEFORE detailed work) |

## Analysis records (01_RAW/)

| path | role |
|---|---|
| 01_RAW/FUN_006C66D0_GETTER_FULL.txt | the complete bounded getter body (mov eax,[ecx+0x68]; ret) + extent provenance (ret + 12x CC padding + aligned next entry) |
| 01_RAW/FUN_006C0D50_CTOR_DECODE.txt | derived ctor (base-ctor delegation; derived-field zeroing; vtable 0xA855D0) |
| 01_RAW/FUN_006C8F80_BASECTOR_DECODE.txt | base ctor — WRITER W1 ([+0x68]=0 @0x006C8FD3; +0x70 template-holder init; flag reset) |
| 01_RAW/FUN_006C8B20_LAZYINIT_DECODE.txt | the on-path lazy initializer (the [+0x68]==0 trigger of the producer; registrations; slot-3 dispatch) |
| 01_RAW/FUN_006C6F60_PRODUCER_DECODE.txt | the producer (validity check; empty-string-key lookups; getter A; the instance-creator pump; [+0x6C] store; installer call) |
| 01_RAW/FUN_006C6780_INSTALLER_PARTIAL.txt | WRITER W2 ([+0x68]=[instance+4] @0x006C67E2 with refcount swap; 'ArkTexture'/'ArkAnimation' named lookups) — PARTIAL window, extent UNRESOLVED past 0x006C6848 |
| 01_RAW/PINS_AND_REL32.txt | 56 byte pins + 23 rel32 recomputes + cross-checks vs prior records |
| 01_RAW/VTABLE_RTTI_STRINGS.txt | vtable slot data, RTTI class names (.?AVArkModelManagerMain@@ / .?AVArkModelManager@@ / .?AVArkModelResourceInstanceRef@@), string constants ('ArkTexture', 'ArkAnimation', the empty-string key) |
| 01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt | the §7 chain re-pin (getter result -> EDI -> push EDI -> slot-41 join; four intervening calls recorded NOT_CHECKED; CHILD_TO_JOIN_IDENTITY = STRONGLY_SUPPORTED with the honest basis) |

## Ledgers

| path | role |
|---|---|
| FIELD_PRODUCER_LEDGER.csv | the writer census of manager+0x68 within the declared scope (W1 NULL reset; W2 value producer) + 3 explicit gaps (GAP-1 creation-chain internals; GAP-2 FUN_006C8BB0; GAP-3 off-path writers out of scope by governance) |
| POINTER_LINEAGE.csv | the typed lineage hops (H-1 manager-contains-instance; H-2 instance-> [+4] relation UNRESOLVED; H-3/H-4 SAME_OBJECT moves) |
| EDGE_ACCOUNTING_LEDGER.csv | the callsite census over the ledger's per-row-defined classes (LEDGER_CLASSES in the ledger header; every callsite touched by this run's records has a row with a class and reason — NOT a global EXE-wide callsite census): 24 ANALYZED_NEW units (the honest exceedance vs MAX 8, disclosed), 7 RAW_VISIBLE_ONLY, 11 REPIN_PRIOR_SCOPE (incl. the 4 prior-scope §7 intervening-call rows added by the F-QC-E record-repair), 27 OUT_OF_ANALYZED_EXTENT neighbor rows — every uncounted row with an explicit reason |
| CLAIM_MATRIX.csv | every load-bearing claim with status/evidence/non-circularity (CL-01..CL-17) |

## Control + QC machinery (03_SCRIPTS/, root)

| path | role |
|---|---|
| 03_SCRIPTS/qc_controls.py | the four §9 mechanical checkers (visual-role classifier; containment predicate; field-provenance predicate; §7 preservation predicate) — each clean PASS -> mutated FAIL on the same checker |
| CONTROL_RESULTS.json | the four control results (all PASS; the real-input POLICY_ONLY classification recorded) |
| 03_SCRIPTS/qc_internal.py | the fresh-context internal QC (SELF_CHECK): pins re-read, rel32 recomputed, getter/writer bytes re-verified, RTTI re-derived, edge count reconstructed, callsite completeness re-enumerated over the 6 analyzed extents, status algebra re-checked, overclaim sweep, encoding, prior-package immutability, repo state |
| QC_INTERNAL_RESULTS.json | the machine record of the internal QC (OVERALL = QC_PASS, 23 checks) |
| QC_REPORT.md | the QC report (incl. the two QC-tooling defect rounds fixed in the QC scripts only) |

## Reports

| path | role |
|---|---|
| FINAL_REPORT.md | the run's answer, statuses, budget accounting, honest open items |
| PE_MASTER_REVIEW.md | PLACEHOLDER — NOT_PERFORMED-do-persistence (filled by the persistence phase after the PE-MASTER audit) |
| HANDOFF.md | the terminal block + the proposed AUDIT_ENTRYPOINT.md newest-first row (NOT applied by this executor) |
| MANIFEST_SHA256.csv | generated LAST over the physical package files minus itself; entrypoint EXCLUDED pending persistence (noted in the header) |
