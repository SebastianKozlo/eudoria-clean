# INPUT_IDENTITIES — PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007

Written at preflight, BEFORE any correction work (contract §1/§2). Every SHA256
below was measured by this executor from the physical files. All identities
MATCHED their dispatch-pinned values; none were substituted from memory.

## 1. Contract (the correction instruction set)

| input | size_bytes | SHA256 |
|---|---|---|
| C:\Users\User\Documents\ChatGPT\PE\PE_935_MODEL_CHILD_JOIN_CORRECTION_PROMPT_REVIEW_20261007\OPENCODE_J1_J3_CORRECTION_REVIEWED.md | 15,582 | 8BDE42C762FC49D615731CE1572D50E523C05672D7BC1AFD4E53EFB20B09C94E |

Dispatch-pinned identity: 15,582 B / 8BDE42C7…09C94E — MATCH. Read in full
(490 lines, §0–§12). NOTE: the dispatch text quoted the folder under a longer
alias ("…_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_PROMPT_REVIEW_20261007");
the actual folder on disk is PE_935_MODEL_CHILD_JOIN_CORRECTION_PROMPT_REVIEW_20261007
and the file's size+SHA256 match the pinned identity exactly — recorded to
preclude any substitution concern.

## 2. Authoritative external Desktop post-audit (read in full before work)

| input | size_bytes | SHA256 | role |
|---|---|---|---|
| C:\Users\User\Documents\ChatGPT\PE\PE_935_MODEL_CHILD_SF_JOIN_DESKTOP_POST_AUDIT_064B7F4_20261007\REPORT.md | 12,030 | 9A97EE46B84E81A1ADDB659CEAE8F95F9CBFF0738FAFD5A265B3D50227614C79 | the independent Desktop post-audit of commit 064b7f4 (verdict REQUIRE_CORRECTIONS; findings J1/J2/J3, all P2) |
| C:\Users\User\Documents\ChatGPT\PE\PE_935_MODEL_CHILD_SF_JOIN_DESKTOP_POST_AUDIT_064B7F4_20261007\PRODUCTION_GATE_COUNTEREXAMPLES.json | 23,166 | 6632C6D11F712DBFD61FD3EE13875B4DB90910BE9D0CCE063955BE379F066D16 | the Desktop's counterexample record against the ORIGINAL production gate (M1–M5 PASS = false positives; CTRL-A/B/C FAIL; real CAND-4 FAIL) |

Both MATCH their dispatch-pinned identities (12,030 B / 9A97EE46…; 23,166 B /
6632C6D1…). The counterexample record is an INPUT IDENTITY only: the M1–M5
fixtures in THIS package are RECREATED INDEPENDENTLY from the contract §4 text
(see GATE_COUNTEREXAMPLES.json field "recreation_basis") — the Desktop JSON was
not copied as the fixture source.

## 3. Audited science run (SOURCE_RUN_PACKAGE — READ-ONLY)

| item | identity |
|---|---|
| SOURCE_RUN_PACKAGE | docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/ |
| AUDITED_SHA (BASE of this correction) | 064b7f4aa4f3961f1a44212b2423e298eb51c291 |
| BASE parent / tree (from the Desktop report §1; recorded, not re-derived here) | parent 24f45e0108b922c26ff584fee9ef7749de0390b6 / tree 11952ad784c793f46ab10aca3de5212cb19ee78e |
| File census at BASE | 49 files (git ls-tree -r); 49 physical files present; 49/49 git-blob identity match (blob SHA-1 recomputed from disk bytes; zero mismatches) |
| Package aggregate SHA256 BEFORE work (sorted "path sha256" digest lines) | ab21cbc3991c91b19bd884f851e0fe24f1eba251b48e24643a71f6169be65b5b |
| Original gate script (READ-ONLY reference for J1) | 03_SCRIPTS/qualification_gate.py at BASE; SHA256 EF2D8E1F01D63BD004CC8F4087BDBC8194F51EACC38579DC0B2AC2FCDCC400AD (per the BASE manifest row; unchanged, not executed for any qualification, not edited) |
| Desktop-measured gate identity cross-check | PRODUCTION_GATE_COUNTEREXAMPLES.json "script_sha256" = the same EF2D8E1F… — the Desktop ran exactly this BASE gate |

All source-run materials were read as Git blobs from the exact BASE commit
(physical files verified byte-identical to those blobs BEFORE work). The
historical package (incl. its PE_MASTER_REVIEW.md and MANIFEST_SHA256.csv)
remains immutable; re-hash AFTER work is recorded in QC_REPORT.md (zero diff
required).

## 4. Pinned EXE (for PIN_CHECK re-verification of already-published pins only)

| input | size_bytes | SHA256 |
|---|---|---|
| D:\Eudoria_Reconstruction\pcg_install\Entropia.exe | 8,015,872 | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 |

Re-verified at preflight (measured) and fail-closed inside every tool of this
package. Role: byte source for re-verifying the ALREADY-PUBLISHED pins of the
source run (records-QC only). NO new EXE analysis, no new regions opened, no
new decode beyond what the source run already published.

## 5. Preflight verification record (measured)

- git fetch + git ls-remote origin master, query 2026-10-07T01:32:46-07:00:
  LOCAL_HEAD = origin/master = actual remote master = 064b7f4aa4f3961f1a44212b2423e298eb51c291
  == EXPECTED_BASE_SHA. MATCH. No error.
- Relevant tracked changes: NONE. Foreign untracked roots (6): untouched.
- OUTPUT_ROOT absent before run (collision check PASS).
- No other inputs are used by this correction. No private research reports were
  opened; no payloads were opened; no BNT/VFS/NIF reads.
