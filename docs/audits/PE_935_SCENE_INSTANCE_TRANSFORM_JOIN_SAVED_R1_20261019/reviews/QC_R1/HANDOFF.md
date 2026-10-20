# HANDOFF.md — QC_R1

RUN_ID: PE_935_SCENE_INSTANCE_TRANSFORM_JOIN_SAVED_R1_20261019 | QC package: QC_R1
Author: pe-master-auditor (fresh independent QC) | Parent: PE-MASTER | Verdict: **PASS_WITH_FINDINGS**

ASSIGNMENT_MODE / RUN_ID / PARENT_LOOP_ID / MILESTONE / SCOPE
- INTERNAL_QC, fresh independent recompute; target = 4 packages + 11 extracts + CONTROL chain + root checkpoint files; read-only; no package modified; no MANIFEST created (parent seals).

QC_VERDICT: PASS_WITH_FINDINGS — 2×P1 (QC-F1 P02 L1 OUT-slot off-by-4: +0x24 not +0x20; QC-F2 P03-C13 receiver-attribution conflation: B0A0/B0B0/ACB0 receive ECX=owner, not [owner+0xC]), 7×P2 (QC-F3 roles overstatement, QC-F4 ECX-use wording, QC-F5 P03 premise gaps, QC-F6 P02 FPU-doc gaps, QC-F7 unlabeled field-identity premise, QC-F8 00401360 arg index, QC-F9 007105F0 ECX-clobber premise), plus observations.

Per-item PASS/FAIL (mandatory recomputations):
1. P01 ESP walk/ECX/arg/REP-MOVSD: PASS (5/5).
2. P02: ESP balance PASS; S1=arg2 PASS; L2=v+S1*(u−v) PASS (conditional labeled); push-shift PASS; 0096D7C0 args/return PASS; RET 0x8 PASS; FPU depth 0 at RET PASS (no imbalance found); **L1 OUT-slot mapping FAIL** (+0x20 claimed, +0x24 true) → QC-F1.
3. P03: ECX=[ESI+0xC] at 00528870/00528A18/00528AC2 PASS; S1#1=[E+8] PASS; S1_2=[E0]/[E8] PASS; guard-exit 00528BB4 pops-only-ESI PASS; 29-call census PASS (C10 correct; C13 defective → QC-F2).
4. Saved texts: 0xA7DCB0 PASS; field-init superset PASS (exact list in RECHECKS); 0xA91E4C PASS (from P09 hex; "MovableObject" kept as label only); [this+8]=type-param PASS; [+0xC]=0/[+0x10]=0 PASS; +0x2C-in-subobject-at-+0x14 via 007345C0(+0x18) PASS; 0085B750 {2..7} PASS; +0x2C bit0 on [this+0xC0] PASS (not receiver); 00401360 arg index FAIL (QC-F8).
5. Budgets: sums 34/413/35/34/712 PASS; no incident debits PASS; ADMIT-vs-request PASS (11/11); event chain hashes intact PASS (12/12); ADMIT counts vs extracts PASS (11/11); source pins re-hash PASS (11/11).
6. Negative scope: receiver+0x2C writer NOT_OBSERVED with bounded denominators PASS; [owner+0xC] attach UNKNOWN PASS (base ctor verified as NULL-init only).
7. Premise inventory: 16 labeled premise groups verified correctly labeled (incl. callee-cleanup RET4/RET8, 0096CD10 write-behavior opacity, float-return ST0, decompiler/label provenance, DF-clear, decode provenance); 5 unlabeled gaps → QC-F5/F6/F7/F9.

FINDINGS: 9 total (2 P1, 7 P2) + observations — full evidence, mechanism, correction and revalidation predicate per finding in REPORT.md §2; recompute detail in RECHECKS.json.

FULL_READ_LOG_PATH: QC_R1\REPORT.md §3 (FULL_READ_LOG).
NOT_CHECKED: QC_R1\REPORT.md §4 / RECHECKS.json not_checked (script execution forbidden; unopened callee bodies; selected_lines_sha256; P05–P11 packages absent-by-state; root §12 closure artifacts pending; no git/publication).

FINAL_REPORT_PATH: <PE_ROOT>\99_Audits\PE_935_SCENE_INSTANCE_TRANSFORM_JOIN_SAVED_R1_20261019\QC_R1\REPORT.md
GATES_PATH: QC_R1\STAGE_ACCEPTANCE_GATES.csv
MANIFEST_PATH: NONE (parent seals packages; QC creates no manifest per assignment).
RECHECKS_PATH: QC_R1\RECHECKS.json

INPUT_AND_OUTPUT_HASHES (inputs, recomputed this QC):
- Extracts P01..P11: 7B4DE2F696814521BD6E8A2787C36EE2763384EF351DCC737EC0D03D0CBD01DC / 77D590D2BD80A72317FDF93A688D508E60DA08A01F939998C2B57F1191CE1BB6 / 8BD6B4D087F0E732A02E20857E883EE6F7A9C4395BB0E240A7A509B19C649C1D / F10DB756657B6479918BE3A8AC21654CB451D40197B763F08AD38BC27E98F099 / 53A4E96336586642663F3481BF1FC10AED7D736D77ED7B8471CB111D0BD04693 / 381BEBFF2FBE208B59DB2C119AC194BD815704A5E610E5C3801536314FDFA4E1 / 3F67D465AE00186B32B49BF526F39050AC6C817AF267933AC4ED09ED587232C1 / C9F483B001880854110E28A498DE37494D8DB62E5793114C990DC043BA3979BA / DAE1D7E1D1DD3E006C5B75A330F9A316AD3320E002BD3A1B6E0ABCA8CB27FC7D / 5CA3944EF159852AAC0D42FDE797ABE1343EACA36BDD8EA11BFE5FC8DB5CD865 / 52E28DD812A7D911F4ADE640FAD999C8D6FE8C8E9FEE5BF7C421C10891162702.
- 11 catalog source pins re-verified (H5 642CC29A…01D8DB, 50,780,146 B; the 8 saved-text files per ADMIT source_sha256) — all match.
- Event chain 000001–000012 hashes recorded in RECHECKS.json ITEM5; last: E0CB445E4137986865638FD557744A355B7A748AD4D9DC7D82D618A20731F632.
- Package file hashes (34 files across P01–P04) recorded during this QC and used as read-state baseline; no input changed during QC (packages are read-only targets).
- Output hashes: recorded in artifact_index.csv after file creation (no self-hash of this handoff).

FILES_CHANGED: only QC_R1\* (6 new files: RUN_STARTED.json, RECHECKS.json, REPORT.md, HANDOFF.md, STAGE_ACCEPTANCE_GATES.csv, artifact_index.csv). No existing file touched.

BASE_SHA / HEAD_SHA / PUSH_STATUS: not applicable — this QC assignment performed no git operations (read-only QC; publication not in scope).

UNRELATED_WORK_EXCLUDED: none observed inside the target root; nothing outside the target root was modified.

NEXT_PARENT_ACTION (for PE-MASTER):
1. Apply corrections for QC-F1 (P02 L1 slots +0x24/+0x28/+0x2C, contiguous; remove "non-contiguous/+0x24-skipped") and QC-F2 (P03-C13/finding-7 receiver sets) — packages are UNSEALED, so in-place fix before seal is permitted by contract §10 (otherwise sibling CORRIGENDUM).
2. Optionally fix the P2 items (QC-F3..F9 wording/premise-labeling) in the same pass; upgrade P04-C10's 0085B1B0 RET 0xC premise to CONFIRMED (P09 hex C2 0C 00 @0085B31D).
3. Note for the closure ledger: union of unique CALL-VAs across P01–P03 = 20 (admission sum 35); charged budget 34/413/35/34/712 all under limits; no incident debits.
4. Proceed with the run's remaining stages (P05–P11 have extracts admitted but no analysis packages yet; root §12 closure artifacts not yet present).
5. QC result is internal QC (PASS_WITH_FINDINGS) — not MASTER_ACCEPTED and not milestone closure; a fresh seal-time audit remains the parent's gate.
