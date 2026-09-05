# CORRECTION LEDGER — superseded-wording record for frozen audit artifacts

> STANDING CONTRACT (file created by PE_NIF_R3_PROPOSAL_APPLICATION_R1_20260905_121500 on 2026-09-05T12:19:06; authority: the human
> HR-R3-3 GO relayed via PE-MASTER; map: TARGET_MAP.json SHA256 D3F043F2167C1BD0EDBC9C4F7957D5FD31AF37C8296848DEEB9350DDA7699628):
> historical/frozen audit artifacts are NEVER edited. When a review
> supersedes wording inside such an artifact, the supersession is recorded
> HERE as a new entry: the historical file stays byte-identical (SHA256
> re-hashed before and after the recording run, both trees: the local
> 99_Audits tree and the repo mirror), the entry quotes the superseded
> wording verbatim with its location, and carries the corrected wording
> (verbatim), the evidence pointer and the lineage reference.
> Operation kind: LEDGER-ENTRY (TARGET_MAP.json operations_legend:
> "historical file preserved byte-identical; entry records superseded
> wording"). APPEND-ONLY: existing entries are never modified or deleted;
> authorized application runs append below the last entry. A repo/local
> byte-identical pair is maintained (SYNC hashes recorded per run).

---
## Entry P3R3/a — R2 06_REPORT/00_FINAL_REPORT.md, Area B sentence (R2 Node hash-primitive method provenance)

- operation: LEDGER-ENTRY
- applied_by: PE_NIF_R3_PROPOSAL_APPLICATION_R1_20260905_121500 (authority: HR-R3-3 GO relayed via PE-MASTER; TARGET_MAP.json SHA256 D3F043F2167C1BD0EDBC9C4F7957D5FD31AF37C8296848DEEB9350DDA7699628, edit P3R3/a)
- claims: R3C-01, R3C-02, R3C-03, R3C-04, R3C-05, R3C-06, R3C-07, R3C-08, R3C-09
- historical file (NOT edited; byte-identical before == after this run): 99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054\06_REPORT\00_FINAL_REPORT.md
- repo mirror (NOT edited): docs/audits/PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054/06_REPORT/00_FINAL_REPORT.md
- historical file SHA256 before == after: 2aee83b9858a5dffaef864324ec15d3b027433b12c64bc76390bcf159297effd (repo mirror SHA256 EQUAL: True)
- superseded wording (verbatim; at lines 101-102 of the historical file):

Node hand-rolled CRC32/adler32/
FNV-1a cross-checked against Python zlib

- corrected wording (TARGET_MAP.json new_text, verbatim):

the candidate census was recomputed with stage-local primitives validated by known-answer tests and per-entry oracle identity (R3); the R2 Node adler32 and fnv1a helpers are CONFIRMED defective (value mismatches on 11,022/11,022 name inputs, 11,022/11,022 payload inputs, and 11,016/11,022 name inputs respectively); the R2 crc32 helper and the size/offset candidates were correct; the aggregate counts were never affected because the aggregate zero-match property was DEMONSTRATED insensitive to these specific value errors on these two corpora: the R3 wrong-value controls (adler32_wrong_xor, fnv1a_wrong_basis) failed their known-answer tests (exit 1) while producing the identical zero-match census, and the two R2 defects themselves yielded zero-match aggregates identical to the corrected primitives (02_LOGS/kat_wrong_value_controls.json + R3G7b; R3G10/R3G11). The insensitivity is PROVEN for those controls and those defects on the 2003 and 9.3.5 Models.bnt corpora — NOT asserted as a general property of arbitrary hash functions, candidate sets, or corpora.

- evidence_pointer: R3 01_RAW/PRIMITIVE_VALUE_COMPARISON.json (r2_vs_corrected complete mismatch census); claims R3C-01..R3C-09; R3 02_LOGS/kat_wrong_value_controls.json (wrong-value controls; gates R3G7a/R3G7b); P0 demonstration
- lineage_ref: R3 proposal P3R3 first bullet (R2 report Area B sentence)
- new_text_source: 06_REPORT/PROPOSALS_P2P3_FIXED.md (this run) EXTRACT:P3R3-FIXED-1 — R3 P3R3 entry 1 with the evidence-bounded insensitivity statement (P3 fix); unchanged head verified verbatim against the proposal

---

## Entry P3R3/b1 — R2 00_CONTROL/run_gates.py, R2G8 independence wording (three-computations claim)

- operation: LEDGER-ENTRY
- applied_by: PE_NIF_R3_PROPOSAL_APPLICATION_R1_20260905_121500 (authority: HR-R3-3 GO relayed via PE-MASTER; TARGET_MAP.json SHA256 D3F043F2167C1BD0EDBC9C4F7957D5FD31AF37C8296848DEEB9350DDA7699628, edit P3R3/b1)
- claims: R3C-01, R3C-02, R3C-03, R3C-04, R3C-05, R3C-06, R3C-07, R3C-08, R3C-09
- historical file (NOT edited; byte-identical before == after this run): 99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054\00_CONTROL\run_gates.py
- repo mirror (NOT edited): docs/audits/PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054/00_CONTROL/run_gates.py
- historical file SHA256 before == after: 7688732929b75e926f4fa2a5bf5ca362032d921d24f1d307f883d6e5355bcede (repo mirror SHA256 EQUAL: True)
- superseded wording (verbatim; at lines 249-249 of the historical file):

three independent computations (Node, Python, R36 historical)

- corrected wording (TARGET_MAP.json new_text, verbatim):

corrected primitives == R2 Python (zlib/exact-int) == R36 historical (zlib/exact-int); the R2 Node leg computed different functions whose zero-match aggregates coincidentally agreed

- evidence_pointer: R3 gate R3G11 (corrected == R2 Python == R36 historical, 20/20); claim R3C-08
- lineage_ref: R2G8 independence wording (S-04)
- new_text_source: PROPOSED_DOC_CORRECTIONS_R3.md P3R3 second bullet (verbatim)

---

## Entry P3R3/b2 — R2 02_LOGS/TEST_RESULTS.json, R2G8 why_non_circular wording (three-computations claim)

- operation: LEDGER-ENTRY
- applied_by: PE_NIF_R3_PROPOSAL_APPLICATION_R1_20260905_121500 (authority: HR-R3-3 GO relayed via PE-MASTER; TARGET_MAP.json SHA256 D3F043F2167C1BD0EDBC9C4F7957D5FD31AF37C8296848DEEB9350DDA7699628, edit P3R3/b2)
- claims: R3C-01, R3C-02, R3C-03, R3C-04, R3C-05, R3C-06, R3C-07, R3C-08, R3C-09
- historical file (NOT edited; byte-identical before == after this run): 99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054\02_LOGS\TEST_RESULTS.json
- repo mirror (NOT edited): docs/audits/PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054/02_LOGS/TEST_RESULTS.json
- historical file SHA256 before == after: a0d5c1249bfad39518999e86b713aae6a39fa6859899db28161fefb7cb9d1b53 (repo mirror SHA256 EQUAL: True)
- superseded wording (verbatim; at lines 127-127 of the historical file):

three independent computations (Node, Python, R36 historical)

- corrected wording (TARGET_MAP.json new_text, verbatim):

corrected primitives == R2 Python (zlib/exact-int) == R36 historical (zlib/exact-int); the R2 Node leg computed different functions whose zero-match aggregates coincidentally agreed

- evidence_pointer: R3 gate R3G11 (corrected == R2 Python == R36 historical, 20/20); claim R3C-08
- lineage_ref: R2G8 independence wording (S-04)
- new_text_source: PROPOSED_DOC_CORRECTIONS_R3.md P3R3 second bullet (verbatim)

---

## Entry P3R3/b3 — R2 STAGE_ACCEPTANCE_GATES.csv row R2G8, independence wording (three-computations claim)

- operation: LEDGER-ENTRY
- applied_by: PE_NIF_R3_PROPOSAL_APPLICATION_R1_20260905_121500 (authority: HR-R3-3 GO relayed via PE-MASTER; TARGET_MAP.json SHA256 D3F043F2167C1BD0EDBC9C4F7957D5FD31AF37C8296848DEEB9350DDA7699628, edit P3R3/b3)
- claims: R3C-01, R3C-02, R3C-03, R3C-04, R3C-05, R3C-06, R3C-07, R3C-08, R3C-09
- historical file (NOT edited; byte-identical before == after this run): 99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054\STAGE_ACCEPTANCE_GATES.csv
- repo mirror (NOT edited): docs/audits/PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054/STAGE_ACCEPTANCE_GATES.csv
- historical file SHA256 before == after: b8f8ca6dea55dd1407e84b5718b5fce4b9bcc090f03953707f94334d807c9f2f (repo mirror SHA256 EQUAL: True)
- superseded wording (verbatim; at lines 9-9 of the historical file):

three independent computations (Node, Python, R36 historical)

- corrected wording (TARGET_MAP.json new_text, verbatim):

corrected primitives == R2 Python (zlib/exact-int) == R36 historical (zlib/exact-int); the R2 Node leg computed different functions whose zero-match aggregates coincidentally agreed

- evidence_pointer: R3 gate R3G11 (corrected == R2 Python == R36 historical, 20/20); claim R3C-08
- lineage_ref: R2G8 independence wording (S-04)
- new_text_source: PROPOSED_DOC_CORRECTIONS_R3.md P3R3 second bullet (verbatim)

---

## Entry P3R3/b4 — R2 STAGE_ACCEPTANCE_GATES.csv row R2G8, gate label phrase (Python==Node==R36)

- operation: LEDGER-ENTRY
- applied_by: PE_NIF_R3_PROPOSAL_APPLICATION_R1_20260905_121500 (authority: HR-R3-3 GO relayed via PE-MASTER; TARGET_MAP.json SHA256 D3F043F2167C1BD0EDBC9C4F7957D5FD31AF37C8296848DEEB9350DDA7699628, edit P3R3/b4)
- claims: R3C-01, R3C-02, R3C-03, R3C-04, R3C-05, R3C-06, R3C-07, R3C-08, R3C-09
- historical file (NOT edited; byte-identical before == after this run): 99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054\STAGE_ACCEPTANCE_GATES.csv
- repo mirror (NOT edited): docs/audits/PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054/STAGE_ACCEPTANCE_GATES.csv
- historical file SHA256 before == after: b8f8ca6dea55dd1407e84b5718b5fce4b9bcc090f03953707f94334d807c9f2f (repo mirror SHA256 EQUAL: True)
- superseded wording (verbatim; at lines 9-9 of the historical file):

Python == Node == R36 historical

- corrected wording (TARGET_MAP.json new_text, verbatim):

corrected primitives == R2 Python (zlib/exact-int) == R36 historical (zlib/exact-int); the R2 Node leg computed different functions whose zero-match aggregates coincidentally agreed

- evidence_pointer: R3 gate R3G11 (corrected == R2 Python == R36 historical, 20/20); claim R3C-08
- lineage_ref: R2G8 gate label phrase (S-04)
- new_text_source: PROPOSED_DOC_CORRECTIONS_R3.md P3R3 second bullet (verbatim)

---

## Entry P4R3/a — R2 00_CONTROL/run_gates.py L50 bool coercion (human-review gate state serialization)

- operation: LEDGER-ENTRY
- applied_by: PE_NIF_R3_PROPOSAL_APPLICATION_R1_20260905_121500 (authority: HR-R3-3 GO relayed via PE-MASTER; TARGET_MAP.json SHA256 D3F043F2167C1BD0EDBC9C4F7957D5FD31AF37C8296848DEEB9350DDA7699628, edit P4R3/a)
- claims: R3C-12, R3C-13
- historical file (NOT edited; byte-identical before == after this run): 99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054\00_CONTROL\run_gates.py
- repo mirror (NOT edited): docs/audits/PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054/00_CONTROL/run_gates.py
- historical file SHA256 before == after: 7688732929b75e926f4fa2a5bf5ca362032d921d24f1d307f883d6e5355bcede (repo mirror SHA256 EQUAL: True)
- superseded wording (verbatim; at lines 50-50 of the historical file):

'pass': bool(ok)

- corrected wording (TARGET_MAP.json new_text, verbatim):

Human-review gate state MUST be serialized three-state: PASS / FAIL / PENDING (R2's `'pass': bool(ok)` turned pending into false/FAIL — R2 HR-1..4 were PENDING, not FAIL; reproduced as a negative control with exit code 1).

- evidence_pointer: R3 01_RAW/R2_STATE_RESUM.json (HR-1..4 pass=false/CSV=FAIL; actual tally 16/8 vs stale 17/7); claims R3C-12/R3C-13
- lineage_ref: R2 run_gates.py L50 bool coercion (S-09)
- new_text_source: PROPOSED_DOC_CORRECTIONS_R3.md P4R3 first bullet (verbatim)

---

## Entry P4R3/b1 — R2 00_CONTROL/run_gates.py R2G13 gate label (stale tally wording)

- operation: LEDGER-ENTRY
- applied_by: PE_NIF_R3_PROPOSAL_APPLICATION_R1_20260905_121500 (authority: HR-R3-3 GO relayed via PE-MASTER; TARGET_MAP.json SHA256 D3F043F2167C1BD0EDBC9C4F7957D5FD31AF37C8296848DEEB9350DDA7699628, edit P4R3/b1)
- claims: R3C-12, R3C-13
- historical file (NOT edited; byte-identical before == after this run): 99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054\00_CONTROL\run_gates.py
- repo mirror (NOT edited): docs/audits/PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054/00_CONTROL/run_gates.py
- historical file SHA256 before == after: 7688732929b75e926f4fa2a5bf5ca362032d921d24f1d307f883d6e5355bcede (repo mirror SHA256 EQUAL: True)
- superseded wording (verbatim; at lines 366-366 of the historical file):

tally {CONFIRMED 17, REJECTED 7}

- corrected wording (TARGET_MAP.json new_text, verbatim):

Gate tally labels MUST be derived from the actual emitted rows at emit time (R2G13's "{CONFIRMED 17, REJECTED 7}" label vs the actual 16/8 rows).

- evidence_pointer: R3 01_RAW/R2_STATE_RESUM.json (HR-1..4 pass=false/CSV=FAIL; actual tally 16/8 vs stale 17/7); claims R3C-12/R3C-13
- lineage_ref: R2G13 stale tally label (S-10)
- new_text_source: PROPOSED_DOC_CORRECTIONS_R3.md P4R3 second bullet (verbatim)

---

## Entry P4R3/b2 — R2 02_LOGS/TEST_RESULTS.json R2G13 gate_name (stale tally wording)

- operation: LEDGER-ENTRY
- applied_by: PE_NIF_R3_PROPOSAL_APPLICATION_R1_20260905_121500 (authority: HR-R3-3 GO relayed via PE-MASTER; TARGET_MAP.json SHA256 D3F043F2167C1BD0EDBC9C4F7957D5FD31AF37C8296848DEEB9350DDA7699628, edit P4R3/b2)
- claims: R3C-12, R3C-13
- historical file (NOT edited; byte-identical before == after this run): 99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054\02_LOGS\TEST_RESULTS.json
- repo mirror (NOT edited): docs/audits/PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054/02_LOGS/TEST_RESULTS.json
- historical file SHA256 before == after: a0d5c1249bfad39518999e86b713aae6a39fa6859899db28161fefb7cb9d1b53 (repo mirror SHA256 EQUAL: True)
- superseded wording (verbatim; at lines 207-207 of the historical file):

tally {CONFIRMED 17, REJECTED 7}

- corrected wording (TARGET_MAP.json new_text, verbatim):

Gate tally labels MUST be derived from the actual emitted rows at emit time (R2G13's "{CONFIRMED 17, REJECTED 7}" label vs the actual 16/8 rows).

- evidence_pointer: R3 01_RAW/R2_STATE_RESUM.json (HR-1..4 pass=false/CSV=FAIL; actual tally 16/8 vs stale 17/7); claims R3C-12/R3C-13
- lineage_ref: R2G13 stale tally label (S-10)
- new_text_source: PROPOSED_DOC_CORRECTIONS_R3.md P4R3 second bullet (verbatim)

---

## Entry P4R3/b3 — R2 STAGE_ACCEPTANCE_GATES.csv row R2G13 (stale tally wording)

- operation: LEDGER-ENTRY
- applied_by: PE_NIF_R3_PROPOSAL_APPLICATION_R1_20260905_121500 (authority: HR-R3-3 GO relayed via PE-MASTER; TARGET_MAP.json SHA256 D3F043F2167C1BD0EDBC9C4F7957D5FD31AF37C8296848DEEB9350DDA7699628, edit P4R3/b3)
- claims: R3C-12, R3C-13
- historical file (NOT edited; byte-identical before == after this run): 99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054\STAGE_ACCEPTANCE_GATES.csv
- repo mirror (NOT edited): docs/audits/PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054/STAGE_ACCEPTANCE_GATES.csv
- historical file SHA256 before == after: b8f8ca6dea55dd1407e84b5718b5fce4b9bcc090f03953707f94334d807c9f2f (repo mirror SHA256 EQUAL: True)
- superseded wording (verbatim; at lines 14-14 of the historical file):

tally {CONFIRMED 17, REJECTED 7}

- corrected wording (TARGET_MAP.json new_text, verbatim):

Gate tally labels MUST be derived from the actual emitted rows at emit time (R2G13's "{CONFIRMED 17, REJECTED 7}" label vs the actual 16/8 rows).

- evidence_pointer: R3 01_RAW/R2_STATE_RESUM.json (HR-1..4 pass=false/CSV=FAIL; actual tally 16/8 vs stale 17/7); claims R3C-12/R3C-13
- lineage_ref: R2G13 stale tally label (S-10)
- new_text_source: PROPOSED_DOC_CORRECTIONS_R3.md P4R3 second bullet (verbatim)

---


## LED-ENTRY: WITNESS_MATRIX.json MILD-2 predicted_outcome REFUTED (RUN-E)

- date: 2026-09-05
- issued_by: PE-MASTER (RUN-E review, MASTER_ACCEPTED) — relayed by the human; appended by pe-master-auditor (RUN-E-CORR)
- superseded_claim: WITNESS_MATRIX.json MILD-2 predicted_outcome (RUN-C, pinned @ 8c037c0, blob 408f736d)
- falsified_by: RUN-E execution (PE_NIF_WITNESS_FALSIFICATION_R1_20260905_131214, commit 59b5b63)
- finding: WITNESS_MATRIX.json MILD-2 predicted_outcome (RUN-C, 8c037c0) REFUTED by RUN-E (59b5b63) execution: actual = FAIL_CLOSED @block 3 (loud desync); TEXT_CRLF->G9_RTTI fallback NOT triggered; actual behavior SAFER (no silent corruption absorption). RUN-C final-message claim 'MILD-2 -> PASS via G9_RTTI' corrected. Zero wiki/grammar impact.
- severity: P1, matrix-internal prediction error; no safety regression
- evidence: 01_RAW\FAILURE_DETAILS.json (MILD-2 fail_reason, fail_block_index=3); 05_ANALYSIS\VERDICTS.json (F-1); PE-MASTER physical re-verification (6/6 byte-exact vs originals)

---

## 2026-09-05 (night) â€” PE_M1_X87CW_AUTOMATION_R1 measurement verdict RETRACTED

PE_M1_X87CW_AUTOMATION_R1 measurement verdict OPEN-BREAKPOINT_UNREACHED_WITHIN_BOUNDED_WINDOW (commit f0906b9) RETRACTED as falsified by own artifacts: target_exit_code 3221225781 (0xC0000135, loader-phase DLL death ~20 ms post spawn; mac3r.dll/MSVCR80.dll absent from sandbox wd\ while statically imported). The "300s clean run" was a spin on a dead process. Backend-E qualification 10/10 STANDS. The world-load gating hypothesis remains UNMEASURED pending a live client. Issued by PE-MASTER night audit 2026-09-05.

(Executor's own QC lessons recorded with the retraction: (1) the status code 0xC0000135 was read but NEVER DECODED before the session was interpreted â€” every exit code must be decoded before interpretation; (2) the harness v2 timeout branch OVERWROTE window_closed_by (target_exit -> timeout_no_events) â€” the close marker must never be overwritten; (3) the import-table walk (now done) shows a THIRD missing import: d3dx9_30.dll â€” the repair must close the whole import set, not the two named.)

