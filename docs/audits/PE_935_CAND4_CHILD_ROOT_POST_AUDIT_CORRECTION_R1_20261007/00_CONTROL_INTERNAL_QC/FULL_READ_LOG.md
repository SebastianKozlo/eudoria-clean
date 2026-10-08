# FULL_READ_LOG — PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_INTERNAL_QC_R1_20261007

Independent internal QC by **pe-master-auditor** (fresh session, NOT the executor; the
executor's own QC is the honestly-labeled SELF-REVIEW in the package's QC_REPORT.md).
Read mode legend: FULL_READ = every line to EOF; TARGETED = named sections/rows;
HASHED = byte identity only. All repo reads were done from working-tree copies AFTER
this QC verified their git-blob identity against BASE 790e83735b439e2d76a250868a47a599c2c10184
(38/38 for the SOURCE package; the correction package is untracked and was fully re-hashed
against its own manifest: 18/18 rows zero mismatch).

## 1. Dispatch inputs (FULL_READ)

| file | size | SHA256 (re-measured by this QC) | mode |
|---|---|---|---|
| C:\Users\User\Documents\ChatGPT\PE\PE_935_CAND4_CORRECTION_PROMPT_REVIEW_20261007\OPENCODE_C4_C1_C2_CORRECTION_REVIEWED.md | 11,851 | 364D5C82BBCDD95E44ACF63BB676D026AA482E57950572CE83D71526DD05F348 | FULL_READ (333 lines, §1–§8) |
| Desktop REPORT.md | 12,454 | BDE7B9EB873DF8E80A1E6C6A39B132A3EA1E1545E7A15977571DE7830D63EEEA | FULL_READ (224 lines) |
| Desktop CONTROL_COUNTERCHECKS.json | 2,443 | 32DC3FEEE9881BADDD40AA44A040499E86071C9D7B0E3B3D0F8E772D8C3CCB4C | FULL_READ (85 lines) |
| Desktop EDGE_AND_SCOPE_COUNTERCHECKS.json | 5,042 | E275035BDF9FC8DF6383A8287546AB4009835F8E0DA66254CF5F0EF0B68C22CC | FULL_READ (123 lines) |

All four identities MATCH the dispatch pins. Zero substitution.

## 2. Correction package — ALL 19 files (FULL_READ; the audit target)

| # | file | lines | mode |
|---|---|---|---|
| 1 | FINAL_REPORT.md | 192 | FULL_READ |
| 2 | QC_REPORT.md | 159 | FULL_READ |
| 3 | INPUT_IDENTITIES.md | 162 | FULL_READ |
| 4 | GOVERNANCE_DECISION.md | 195 | FULL_READ |
| 5 | SUPERSESSION.md | 179 | FULL_READ |
| 6 | CORRECTED_LINEAGE_STATUS.md | 85 | FULL_READ |
| 7 | HANDOFF.md | 152 | FULL_READ |
| 8 | PE_MASTER_REVIEW.md | 50 | FULL_READ |
| 9 | CONTROL_RESULTS.json | 104 | FULL_READ |
| 10 | FUNCTION_BODY_ACCOUNTING.csv | 40 (7 counted + C1 + C2 rows) | FULL_READ |
| 11 | CORRECTED_EDGE_ACCOUNTING_LEDGER.csv | 114 (header + 69 rows) | FULL_READ (every row's 13 fields) |
| 12 | MANIFEST_SHA256.csv | 31 (18 rows) | FULL_READ + full re-hash |
| 13 | 03_SCRIPTS/build_corrected_ledger.py | 207 | FULL_READ |
| 14 | 03_SCRIPTS/ctrl3_rebuilt.py | 156 | FULL_READ |
| 15 | 03_SCRIPTS/ctrl4_exact_endpoint.py | 369 | FULL_READ |
| 16 | 03_SCRIPTS/qc_correction.py | 414 | FULL_READ |
| 17 | 03_SCRIPTS/make_manifest.py | 68 | FULL_READ |
| 18 | 03_SCRIPTS/FIXTURES.md | 109 | FULL_READ |
| 19 | 03_SCRIPTS/QC_CORRECTION_RESULTS.json | 93 | FULL_READ |

## 3. SOURCE package (docs/audits/PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007/ —
BASE-blob-verified 38/38 before reading; READ-ONLY)

| file | lines | mode |
|---|---|---|
| EDGE_ACCOUNTING_LEDGER.csv (69 rows) | 104 | FULL_READ (re-adjudication input; verbatim-round-trip basis) |
| 03_SCRIPTS/qc_controls.py (old CTRL_3/CTRL_4) | 216 | FULL_READ (probe + push_edi-anywhere defect verification) |
| CONTROL_RESULTS.json (historical control results) | 106 | FULL_READ |
| 01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt | 53 | FULL_READ (window buffer re-derivation basis) |
| FINAL_REPORT.md | 222 | FULL_READ (S-1/3/5/6/7/8 quote loci) |
| HANDOFF.md | 203 | FULL_READ (S-1/2/3/5/6/7/8 quote loci) |
| PE_MASTER_REVIEW.md | 41 | FULL_READ (S-1/2/4/7/9 quote loci) |
| QC_REPORT.md | 219 | FULL_READ (S-2/S-6 loci; record-repair log) |
| PREREGISTRATION.md | 255 | FULL_READ (literal rule §2; budgets; wrapper-hop rule) |
| POINTER_LINEAGE.csv | 9 (H-1..H-4) | FULL_READ (corrected-lineage basis) |
| 00_CONTROL_INTERNAL_QC/qc_ind_census.py | 206 | FULL_READ (QC-I5/QC-I9/QC-I10 defect loci) |
| CLAIM_MATRIX.csv | 20+ rows | TARGETED (CL-11..CL-16; S-5 locus; S-4 phrase locus CL-14) |
| 01_RAW/FUN_006C66D0_GETTER_FULL.txt | head 25 | TARGETED (RAW BYTES line — the CLEAN_GETTER_FIXTURE provenance) |

## 4. Prior packages at BASE (RP-citation spot-verification; targeted git-blob reads)

- PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/01_RAW/FUN_0050A310_DECODE.txt —
  TARGETED (window instruction lines: the four intervening calls + [SF+0x2C] writes + head/pushes).
- …_JOIN_R1_20261006/EDGE_LEDGER.csv — TARGETED (E5 SF-install row; E6 join-call row).
- …_JOIN_R1_20261006/QC_REPORT.md — TARGETED (S4 join-site receiver preservation).
- PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007/
  EDGE_BUDGET_RECONSTRUCTION.csv — TARGETED (X01/X03/X05/X08/X31 rows).
- git grep -i 6c0ee0 over ALL FOUR prior audit packages — ABSENCE PROOF (exit=1, zero hits).

## 5. Executed by this QC (own engines; records/QC-machinery only)

- qc_ind_reverify.py — 17 checks I1–I16(+finding) — identity/ledger/manifest/quotes/governance/separation/EXE-scan.
- qc_ind_ctrl_own.py — 7 checks C1–C8 — MY OWN decoder + MY OWN exact-endpoint checker; the
  mandatory 4-case matrix; 9 adversarial mutants through BOTH my checker and the executor's
  (imported read-only; ONLY the pure checker functions were called — never run_and_write());
  5 CTRL_3 fixtures through both checkers; window arithmetic.
- qc_ind_finalize.py — executor-file integrity after the QC's executions (zero modified);
  this QC's own file census/hashes/encoding; final verdict assembly.

## 6. NOT_CHECKED (explicit; barriers honored)

- THE EXE: zero access of any kind by this QC (never opened/hashed; identity carried from
  records only). NEW_PCG_FUNCTION_BODIES_ALLOWED = 0 / RECORDS-ONLY scope honored.
- The four §7 intervening callee bodies (FUN_006C0F90/FUN_006C10B0/FUN_0050A1E0/FUN_005246E0);
  FUN_006C9700; FUN_006C8BB0; FUN_007B6C30; FUN_007BF900/FUN_007BF630; FUN_007BF470; all NEIGH
  bodies; the FUN_006C6780 continuation — NOT_CHECKED (forbidden by the correction contract).
- The unrecorded execution history of the audited run (EXACT counts stay UNRESOLVED by design).
- The semantic re-derivation of each of the 24 historical E-row interpretations' underlying bytes
  (verified as PRESENT, recorded, interpretation-shaped; re-proving them would be new RE).
- No re-execution of the executor's qc_correction.py (it writes QC_CORRECTION_RESULTS.json —
  a post-manifest package write; forbidden to this QC). My own engine independently covers its
  load-bearing paths.
- The live REMOTE state (this QC verifies HEAD == BASE locally; remote verification belongs to
  the persistence phase per the contract §8).
- The independent PE-MASTER audit of this package (this QC is its input) and the independent
  Desktop post-audit of the future published SHA (NOT_PERFORMED, pending persistence).
- Capstone cross-decode (not installed/needed for this records-only QC; two independent decoders
  — mine and the rebuilt checker's — plus the published capstone record agree on the window).
