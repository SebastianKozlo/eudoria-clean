# STANDING POLICIES — acceptance/policy guards adopted by proposal application

> STANDING CONTRACT (file created by PE_NIF_R3_PROPOSAL_APPLICATION_R1_20260905_121500 on 2026-09-05T12:19:06; authority: the human
> HR-R3-3 GO relayed via PE-MASTER; map: TARGET_MAP.json SHA256 D3F043F2167C1BD0EDBC9C4F7957D5FD31AF37C8296848DEEB9350DDA7699628):
> this file carries STANDING-POLICY texts (TARGET_MAP.json
> operations_legend: "acceptance/policy guard; anchor fragment verifies
> the referenced historical wording"). Where an entry references historical
> wording, the anchor fragment is verified READ-ONLY (present exactly-once
> at the recorded location in the hash-stable historical file). Each entry
> embeds the policy text VERBATIM (the map's new_text payload), its
> evidence pointer and lineage reference. APPEND-ONLY: existing policies
> are never modified or deleted; authorized runs append below the last
> entry. A repo/local byte-identical pair is maintained (SYNC hashes
> recorded per run).

---
## Entry P5R3/a — R2 Area C sidecar acceptance preserved; no manifest migration

- operation: STANDING-POLICY
- applied_by: PE_NIF_R3_PROPOSAL_APPLICATION_R1_20260905_121500 (authority: HR-R3-3 GO relayed via PE-MASTER; TARGET_MAP.json SHA256 D3F043F2167C1BD0EDBC9C4F7957D5FD31AF37C8296848DEEB9350DDA7699628, edit P5R3/a)
- claims: R3C-14
- historical file (NOT edited; byte-identical before == after this run): 99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054\06_REPORT\00_FINAL_REPORT.md
- repo mirror (NOT edited): docs/audits/PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054/06_REPORT/00_FINAL_REPORT.md
- historical file SHA256 before == after: 2aee83b9858a5dffaef864324ec15d3b027433b12c64bc76390bcf159297effd (repo mirror SHA256 EQUAL: True)
- referenced historical wording (anchor; verified read-only at lines 129-132 of the historical file):

VERIFIED LOSSLESS by full-file byte reconstruction: the
reassembly of all rows (decode + terminators, in order) equals the original file
byte-for-byte — 12/12 SHA256 equality (R2G10, verified by BOTH the Node builder and
the independent Python checker using the strict csv module).

- standing policy text (TARGET_MAP.json new_text, verbatim):

The accepted 12/12 byte-lossless sidecars (R2 Area C) are PRESERVED; no manifest migration is requested or authorized.

- evidence_pointer: R3 01_RAW/SIDECAR_BARE_CR_ANALYSIS.json (R3G14: 12/12 SHA-equal + 0 field-mapping errors, R39 row 10); claim R3C-14
- lineage_ref: R2 Area C acceptance anchor (12/12 lossless; R2G10)
- new_text_source: PROPOSED_DOC_CORRECTIONS_R3.md P5R3 first bullet (verbatim)
- anchor verification (this run): the anchor fragment above was verified READ-ONLY — present EXACTLY-ONCE at the recorded location in the historical file whose SHA256 was re-hashed before and after this run (2aee83b9858a5dffaef864324ec15d3b027433b12c64bc76390bcf159297effd == 2aee83b9858a5dffaef864324ec15d3b027433b12c64bc76390bcf159297effd; both trees EQUAL: True)

---

## Entry P5R3/b — sidecar bare-CR semantic mapping policy (future-restatement guard)

- operation: STANDING-POLICY
- applied_by: PE_NIF_R3_PROPOSAL_APPLICATION_R1_20260905_121500 (authority: HR-R3-3 GO relayed via PE-MASTER; TARGET_MAP.json SHA256 D3F043F2167C1BD0EDBC9C4F7957D5FD31AF37C8296848DEEB9350DDA7699628, edit P5R3/b)
- claims: R3C-14
- standing policy text (TARGET_MAP.json new_text, verbatim):

Where semantic header normalization is restated, the policy line is explicit: semantic mapping follows the CUSTOM PHYSICAL-LINE CONTRACT (a bare CR inside a physical row is DATA; the R2 builder csvParse semantics). Under standard CSV record semantics exactly one row (R39 row 10) parses differently (computed_by "n/a\r" vs "n/a") — an INTERPRETIVE difference, NOT raw-byte loss; both layers reconstruct the original bytes exactly (R3G14: 12/12 SHA-equal reconstruction + 0 field-mapping errors under the custom contract, R39 row 10 included).

- evidence_pointer: R3 01_RAW/SIDECAR_BARE_CR_ANALYSIS.json (R3G14: 12/12 SHA-equal + 0 field-mapping errors, R39 row 10); claim R3C-14
- lineage_ref: R3 proposal P5R3 second bullet (future-restatement guard)
- new_text_source: PROPOSED_DOC_CORRECTIONS_R3.md P5R3 second bullet (verbatim); no current restatement exists in docs/nif (absence-checked by the census)
- absence re-verification (this run): no restatement of the semantic-header-normalization trigger family exists in docs/nif (read-only whitespace-normalized scan of the 15 docs/nif files for 4 patterns: 0 hits)

---

