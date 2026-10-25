# QC_AND_PROCESS_SUMMARY — PE2003_MODEL_INSTANCE_PLACEMENT_STATIC_R1_20261024

Process: PE-MASTER controller (single writer session); amendment YOLO 8h accepted at 2026-10-24T23:10:45Z (immutable clock, exclusive-create, nonresettable; T0 recorded). 51 native dispatches / 50 delivered / 1 infra-fail (spawn UNKNOWN, retried once within the 2-attempt rule). All roles nask-glm/glm-5-3 default/medium (wire effort UNKNOWN; recorded, not measured). Depth 1, max 2 active, no grandchildren. Budgets: 51/240 attempts (families: V 20/64, L 4/56, T 12/56, D 5/24, Q 9/28, K 1/12; reserve 189 >= 16; rolling QC 6 <= 12). No time-padding; research closed EARLY at 03:30:57Z (branches_exhausted; full backlog review in the private receipt; campaign end unchanged).

QC (all fresh-context pe-master-auditor, procedural — same model family, no model independence):
- QROLL1 (7 material claims): all materially CONFIRMED by independent byte counter-checks; QC_PARTIAL for 3 documentation findings -> fixed by T8, rechecked PASS (QSCI_VM).
- QROLL2 (V14 chain): R1 chain independently byte-verified (FUN_005030c0, 100.0f constant, vtable slots, ntohl import); PASS_WITH_NOTES + 8 P2 doc findings -> fixed by T10, rechecked PASS.
- QROLL3 (final negatives C1-C4): independent full 1936/1936 rescan EXACT-matched V15; fixup bijection reproduced; 1 P2 denominator finding -> fixed by T11.
- QSCI_VM: consistency of the VM chain post-corrections; hop bytes re-verified; T8/T9/T10/T11 rechecks PASS; 5 findings (stale markers) -> fixed by T12, recheck PASS (QACCOUNT 6/6).
- QSCI_INSTANCE: instance-chain consistency, negative scopes, byte counter-checks PASS; 1 P2 stale denominator -> fixed by T12.
- QACCOUNT: census/accounting/schema/chronology PASS_WITH_NOTES; closure blockers (root-owned items) completed at seal.

Admission discipline: 133 ADMIT events; incidents disclosed (retroactive ADMIT: K1, T10; postdated ADMIT timestamps: C1 — DISCLOSED_NO_REPAIR_POSSIBLE; return_by violation: D2b ~60 min). Path-drift layout incidents (C1/C2/L3, D3, V19 — workers writing outside the assigned roots): all caught by root mechanical verification, moved verbatim with SHA preservation, logged CR-PATHDRIFT-*; canonical artifacts verified intact (incl. V19's false "file missing" alarm — canonical SHA matched T10's sealed value).

Seal: closing recheck rehashed 33/33 input pins + 1936/1936 corpus members (0 failures); SCIENCE_STOP recorded; MANIFEST_SHA256.csv generated LAST (60 rows, self-excluded, bijection + independent re-hash PASS). Private evidence immutable; this public package is the sanitized projection.
