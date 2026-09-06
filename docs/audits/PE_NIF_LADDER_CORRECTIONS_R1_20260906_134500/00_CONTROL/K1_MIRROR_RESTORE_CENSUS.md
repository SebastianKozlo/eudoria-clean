# K1_MIRROR_RESTORE_CENSUS.md — TM-6 (post-audit F3) K1 mirror restoration census
Run: PE_NIF_LADDER_CORRECTIONS_R1_20260906_134500 (RUN B, BATCH B2, TM-6). Executor: pe-master-auditor, 2026-09-06. NO commit in this batch.
Source (repo, read-only): D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021\ — 22 files.
Mirror (restored): D:\Eudoria_Reconstruction\99_Audits\PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021\.
Copy window (UTC): 2026-09-06T14:26:36.7321112Z .. 2026-09-06T14:26:36.8144376Z.
Files copied in this action: 21 (all package files except PE_MASTER_REVIEW.md); subdirectories 00_CONTROL, 01_RAW, 05_ANALYSIS, 06_REPORT created as needed.
Pre-existing in the mirror before this action: PE_MASTER_REVIEW.md ONLY (not re-copied; its SHA256 equals the repo source — row below, match=OK).

## Per-file census (mirror side; match = SHA256 equals the repo source)
relative_path | bytes | sha256 | match
00_CONTROL/binding_chain_revalidation_r1.py | 48921 | 8f20229025e31a449e9401ecb73249ad5406cd24d108babbc6952de266d253b4 | OK
00_CONTROL/SHA256_DRIVER.txt | 64 | 8edd46c544602e334d9bcc3c908877389cdcf4a045a9e6ebde973fb3ef1147b2 | OK
01_RAW/ARKTEXTURE_ID_TABLE.csv | 2027570 | 34f64fc8c4dc2ffe84dde52efa588a8cfa843197250b8efd57224729c7c1bbf9 | OK
01_RAW/CENSUS_RECONCILIATION.json | 2409 | ee8f046577c9a1e87c9ee51f3389cf867c983fde79da46e0831e5e6f611d7098 | OK
01_RAW/CONTROLLER_EDGES.csv | 4576 | 89bc749efb82dc6dbafcc7110f647f68825e6b46b041c76519e0c9ca1834bc3a | OK
01_RAW/DANGLING_CLASSIFICATION.json | 3209 | 5d92d14e5507c23a7889702e4b8825afd2daeb7c2ce8af18e67a146b956d3dde | OK
01_RAW/DANGLING_LIST.csv | 4211 | 9f5941f3c20ad08620f33eda51e2c20b840e8b235c7f06fbd2824a69a9dd8fe6 | OK
01_RAW/EDGE_COUNTS.json | 1028 | 958e49f500e8cc07b249b1ca691510d6b2457913884895f32d28fd147a30f082 | OK
01_RAW/EFFECT_EDGES.csv | 59330 | 0f524a4a7f9aca1e0971180944c4efb06418986d1104a62f0ccdd985908a1534 | OK
01_RAW/INDEX_VALIDATION.json | 839 | b149d7f912ff583968b3d6ce75d1f4041cad01ab1ba2bd665de1ab3b9910f143 | OK
01_RAW/NEGATIVE_CONTROLS.json | 927 | e90dfe0455c5b1949755290d20bbb54b7f30d04fa20ced2e36c609940f58d4c8 | OK
01_RAW/STATIC_EDGES.csv | 481751 | cab6d94e3db26d98c576aafecf2abdb3b5ad95bdb01b1f9c1c72e7a79fe632a7 | OK
01_RAW/SUMMARY.json | 2719 | 81c1ab421abdb9f73b7e1df0fd7ee22eca661cd241114dcd73b0f1d09dfdbdca | OK
05_ANALYSIS/CONTROLLER_ATTACHMENT_ANALYSIS.json | 2406 | c16921fcb59a466336f56825b571d5a78dbddaa70d16da1fb4bfb5d4fb9f64ea | OK
05_ANALYSIS/controller_attachment_analysis.py | 4089 | d420e710b5a15a2ab1032739d075fdecb6a8fd7622f4756c2c66b0f3e85c1ac8 | OK
05_ANALYSIS/CONTROLLER_CHAIN_COUNTS.json | 716 | f48560a833b45c4ce8c4e299581b835877a0735268ca85cb6aafd1354cb97281 | OK
05_ANALYSIS/controller_chain_counts.py | 4006 | e8ee388f22628de4f8035f6f5094abdc1b308b4c1d1dfef0f5a0fa28c81fc537 | OK
06_REPORT/00_FINAL_REPORT.md | 10429 | 5c408e5e70e5c78ec4f54994d5e17939198fb4cc50f1d8c5e9562f491e3a11d3 | OK
06_REPORT/HANDOFF.md | 4452 | 74cd62af01d705374b9161494a1d10904127eff88bd19837c180397ca37a0c28 | OK
artifact_index.csv | 2080 | 6f4b21609b6aa81d2adfc51e1d2053b0ae7533a944e838d56d1e7102fbac3d5e | OK
PE_MASTER_REVIEW.md | 3817 | 0893982d999995a73e466305e3a14c7590977e0dc66b83dafbd677a707556d4a | OK
STAGE_ACCEPTANCE_GATES.csv | 5394 | 50731b6d8b624367c5419e741bac60b4837a064ba433ec9e3922d2ff95f15764 | OK

## Total
22/22 files present in the mirror (incl. the pre-existing PE_MASTER_REVIEW.md), every SHA256 equals its repo source: MATCH_OK_TOTAL=22, MIRROR_TOTAL=22, REPO_TOTAL=22, zero MISSING_IN_MIRROR, zero MISMATCH. Gate G3 (MIRROR_CENSUS) satisfied for K1.

## Note (verbatim)
FORWARD FIX ONLY: this restoration (post-audit F3) makes the mirror complete from 2026-09-06; NO historical claim is made whether a mirror existed or was removed before this action; the b4dda2e '21/21 package files byte-identical' sentence remains ambiguous (repo-side reading stays true).
