# STANDING RULES — audit-methodology rules adopted by proposal application

> STANDING CONTRACT (file created by PE_NIF_R3_PROPOSAL_APPLICATION_R1_20260905_121500 on 2026-09-05T12:19:06; authority: the human
> HR-R3-3 GO relayed via PE-MASTER; map: TARGET_MAP.json SHA256 D3F043F2167C1BD0EDBC9C4F7957D5FD31AF37C8296848DEEB9350DDA7699628):
> this file carries STANDING-RULE texts (TARGET_MAP.json operations_legend:
> "new standing text; no superseded file wording") adopted via authorized
> proposal application. Each entry embeds the rule text VERBATIM (the map's
> new_text payload), its evidence pointer and lineage reference.
> APPEND-ONLY: existing rules are never modified or deleted; authorized
> runs append below the last entry. A repo/local byte-identical pair is
> maintained (SYNC hashes recorded per run).

---
## Entry P3R3/c — hash-primitive value identity before aggregate acceptance (the P0)

- operation: STANDING-RULE
- applied_by: PE_NIF_R3_PROPOSAL_APPLICATION_R1_20260905_121500 (authority: HR-R3-3 GO relayed via PE-MASTER; TARGET_MAP.json SHA256 D3F043F2167C1BD0EDBC9C4F7957D5FD31AF37C8296848DEEB9350DDA7699628, edit P3R3/c)
- claims: R3C-01, R3C-02, R3C-03, R3C-04, R3C-05, R3C-06, R3C-07, R3C-08, R3C-09
- standing text (TARGET_MAP.json new_text, verbatim):

Standing rule (the P0): hash-primitive VALUE IDENTITY (known-answer tests + per-entry oracle agreement) must be established BEFORE aggregate acceptance, because aggregate zero-match counts were DEMONSTRATED insensitive to the tested value errors — insensitivity PROVEN for the specific R3 wrong-value controls (adler32_wrong_xor, fnv1a_wrong_basis: KAT exit 1 with identical zero-match census, 02_LOGS/kat_wrong_value_controls.json + R3G7b) and for the two R2 hash defects on the 2003 and 9.3.5 Models.bnt corpora, NOT a general property of arbitrary functions or corpora — which is precisely why value identity cannot be inferred from aggregate agreement and must be established per run.

- evidence_pointer: R3 02_LOGS/kat_wrong_value_controls.json (wrong-value controls; gates R3G7a/R3G7b); P0 demonstration
- lineage_ref: R3 proposal P3R3 standing rule
- new_text_source: 06_REPORT/PROPOSALS_P2P3_FIXED.md (this run) EXTRACT:P3R3-FIXED-3 — R3 P3R3 standing rule (the P0) with the evidence-bounded insensitivity statement (P3 fix); unchanged head verified verbatim against the proposal

---

## Entry P4R3/c — overall executable pass distinct from human acceptance

- operation: STANDING-RULE
- applied_by: PE_NIF_R3_PROPOSAL_APPLICATION_R1_20260905_121500 (authority: HR-R3-3 GO relayed via PE-MASTER; TARGET_MAP.json SHA256 D3F043F2167C1BD0EDBC9C4F7957D5FD31AF37C8296848DEEB9350DDA7699628, edit P4R3/c)
- claims: R3C-12, R3C-13
- standing text (TARGET_MAP.json new_text, verbatim):

OVERALL EXECUTABLE PASS must always be presented as distinct from human acceptance (explicit human_acceptance field: PENDING_HUMAN_REVIEW).

- evidence_pointer: R3 01_RAW/R2_STATE_RESUM.json (HR-1..4 pass=false/CSV=FAIL; actual tally 16/8 vs stale 17/7); claims R3C-12/R3C-13
- lineage_ref: R3 proposal P4R3 third bullet
- new_text_source: PROPOSED_DOC_CORRECTIONS_R3.md P4R3 third bullet (verbatim)

---

