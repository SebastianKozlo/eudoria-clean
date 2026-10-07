# EVIDENCE_INDEX — PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006

All evidence was produced this run from the hash-pinned EXE
(E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 / 8,015,872 B)
unless marked as a re-pin of a named prior pin (BASE 24f45e0...). Every raw file
carries its own method header. Line endings LF; UTF-8 no BOM.

## Control / identity files

| file | content |
|---|---|
| GOVERNANCE_DECISION.md | the VERBATIM human authorization, phase-boundary adjudication, write time, contract/constraint identities |
| INPUT_IDENTITIES.md / .json | all input identities (EXE, contract, anchor constraints, 3 private research reports, BASE prior packages, oracle sources, scratch registration, preflight record) — written before any input was used as evidence |
| PRE_REGISTERED_ANCHORS.md | the anchors, statuses, budgets, join strategy, deferred-lead dependency statement — written BEFORE detailed decoding |

## Ledgers (csv.DictWriter; schema-validated; duplicates NONE)

| file | rows |
|---|---|
| FUNCTION_BUDGET.csv | 8 NEW detailed functions (1/8..8/8) with charge basis + prior-scope notes |
| EDGE_LEDGER.csv | 6 NEW interprocedural edges (E1..E6; E6 = the join site) |
| CANDIDATE_LEDGER.csv | 4 join candidates (CAND-1..CAND-4; all examined, incl. rejected) |
| CLAIM_MATRIX.csv | 20 claims CL-01..CL-20 with statuses + WHY_NON_CIRCULAR |

## Raw windows (01_RAW/)

| file | content |
|---|---|
| REPIN_ANCHOR_WINDOWS.txt | PA1–PA4 + CH1/CH3 prior-pin re-pins (bytes + capstone decode + EXPECT checks) |
| FUN_008BD720_DECODE.txt | NEW #1: the "callback" VA is a 4-byte accessor `lea eax,[ecx+0x18]; ret` |
| FUN_00528E50_CONTINUATION.txt | NEW #2: the CMO ctor tail (3 further SF-method calls; ctor extent) |
| FUN_509x_SF_METHODS.txt | NEW #3/#4: FUN_00509510, FUN_00509070 full bodies |
| FUN_00509850_FULL.txt | NEW #5: the SF update (transform application to the SF+0x30 NiNode; model-manager calls; FUN_007BF500 callsite) |
| FUN_007BF500_DECODE.txt | NEW #6: the NiNode update-like operation (no child; no children-array access) + the callsite re-verification |
| SF20_WRITER_CENSUS.txt | the SF-cluster +0x20 store census (2 raw hits) + the FULL NiNode vtable dump (47 slots) |
| SF20_EXTERNAL_WRITER_SCAN.txt | the +0xC0→+0x20 pattern census (ZERO hits — true negative) |
| FUN_006A3930_CHAIN_REPIN.txt | the ACLD construction-chain byte re-pin (prior pin scope: bridge R09) with all E8 callsites + windows |
| FUN_0050A310_DECODE.txt | NEW #7: the SF visual/model-manager install — [SF+0x20] store, the child getter call, THE JOIN SITE @0x0050A3E9..0x0050A3F7, the detach path |
| FUN_007B5810_ORACLE_BYTE_PROOF.txt | NEW #8 + the oracle record: source identities (MATCH), predicted fingerprint, the full AttachChild-counterpart body proof |

## Scripts + machine results (03_SCRIPTS/)

| file | content |
|---|---|
| build_ledgers.py | generates the 4 CSVs (csv.DictWriter) + schema validation -> ledger_build_results.json (all PASS) |
| qualification_gate.py | the structure-reading qualification gate: SYNTHETIC baseline PASS, CTRL-A/B/C proper-predicate rejections, REAL CAND-4 FAIL with byte verification -> qualification_results.json (OVERALL PASS) |
| qc_reverify.py | the fresh-context internal QC: 14 independent checks (EXE identity, 25 pins, 17 rel32 targets, receiver preservation, chains, vtable slots, budgets, schemas, overclaim sweep, repo state, gate results, status algebra) -> qc_reverify_results.json (QC_PASS) |
| ledger_build_results.json | machine-readable schema validation results |
| qualification_results.json | machine-readable gate results |
| qc_reverify_results.json | machine-readable QC results (SELF_CHECK) |

## Reports

| file | content |
|---|---|
| QC_REPORT.md | the targeted/internal QC narrative + the honest QC findings (incl. the 2 round-1 QC-script defects, disclosed) |
| FINAL_REPORT.md | the authoritative science close of this phase (the question, the answer, the proofs, the open edges) |
| PE_MASTER_REVIEW.md | PLACEHOLDER — to be filled by PE-MASTER in the persistence phase (actual author/origin recorded inside; no fabricated review content) |
| HANDOFF.md | the terminal handoff + the proposed AUDIT_ENTRYPOINT newest-first row |
| MANIFEST_SHA256.csv | generated LAST: relative path + size + SHA256 of every physical package file EXCLUDING itself (the AUDIT_ENTRYPOINT.md row is explicitly out of this phase's manifest scope — see FINAL_REPORT §6) |
