# P01_CALLER WORKER BUDGET

This package used **only the admitted P01 extract** — no new admissions.

- Admissions consumed by this package: 1 (parent-issued before worker start)
  - P01_EXTRACT, admission A27148d95e802, region [0x00527AA0,0x00527B20), 37 listing rows (180895-180931), 2 CALL sites, source pin 642CC29A01B8AD6F783E82E14DA4A61FA00BA6A3EC6DF98EDFF28AC25CC1D8DB.
- New admissions requested/created by this worker: **0**.
- Bodies semantically interpreted: 1 (00527AA0 — complete in-window; entry @0x00527AA0, RET 0x4 @0x00527B1D, contained in the admitted region). Both CALL targets (0085BFA0, 00861150) were NOT opened in this package: 0085BFA0 facts are cited from the frozen prior R2 P04 package (read-only), 00861150 left UNKNOWN.
- CALL accounting: sum of admissions = 2 CALL sites; union of unique CALL-VA = 2 (0085BFA0, 00861150); no re-reservation, no refund.
- Prior evidence READ (frozen, read-only, never executed):
  - PE_935_PAIR_REDUCER_CONSUMER_SAVED_R2_20261019\REPORT.md
  - PE_935_PAIR_REDUCER_CONSUMER_SAVED_R2_20261019\P04_FRONTIER\REPORT.md
  - PE_935_PAIR_REDUCER_CONSUMER_SAVED_R2_20261019\P04_FRONTIER\CLAIMS.json
  - PE_935_PAIR_REDUCER_CONSUMER_SAVED_R2_20261019\P04_EXTRACT
- Constraints honored: no game/original files touched or stat'ed; no scripts executed (science or historical); no new listing regions opened; no Ghidra; no runtime/debugger; no Git; no PE-Vault writes; no nested tasks; no config changes.
- Operational note: the only terminal commands used were directory creation and UTC timestamp retrieval for RUN_STARTED.json, and file-size listing for artifact_index.csv. No evidence-processing script was run.

Prepared by pe-reconstruction for RUN_ID PE_935_SCENE_INSTANCE_TRANSFORM_JOIN_SAVED_R1_20261019.
