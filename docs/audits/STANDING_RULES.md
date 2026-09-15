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

## Entry OMC/L1 — CLAIM_OF_MEASUREMENT_REQUIRES_MEASUREMENT_ARTIFACT

- operation: STANDING-RULE
- applied_by: PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915 (authority: the human authorization of PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915 relayed via PE-MASTER; the bounded in-place correction of docs/audits/PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915)
- claims: the original run's fabricated write-through coverage claim (RETRACTED by the correction); supersession adjudication 06_REPORT/PE_MASTER_REVIEW_SUPERSESSION_R1.md CLAIM_MATRIX (1)
- standing text (verbatim):

A claim that something was “measured” must be backed by a corresponding measurement artifact (script + raw rows + derived aggregate). The SF origin case: “No caller writes through the returned pointer within 8 instructions (measured over all 99 sites)” was a generator-emitted sentence with NO measurement behind it (the classifier looked at two instructions after each call and keyed on the first instruction's pattern); the counterexample (0x00458E27, three writes at 0x458E30/0x458E36/0x458E3D) was sitting in the instrument's own recorded data.

- evidence_pointer: docs/audits/PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915/01_RAW/ORIGIN_SINGLETON_WRITE_THROUGH_CENSUS.csv + NEGATIVE_CONTROL_RAW.txt Control-4 supersession
- lineage_ref: PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915 standing lesson OMC/L1 (00_CONTROL/AMEND_LOG_R1.md STANDING LESSONS + 06_REPORT/PE_MASTER_REVIEW_SUPERSESSION_R1.md CLAIM_MATRIX (10))

---

## Entry OMC/L2 — ROW_INTEGRITY_DOES_NOT_VALIDATE_INFERENCE

- operation: STANDING-RULE
- applied_by: PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915 (authority: the human authorization of PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915 relayed via PE-MASTER; the bounded in-place correction of docs/audits/PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915)
- claims: the original run's origin-immutability inference drawn from the triple-write census (RETRACTED by the correction; the bounded measurement itself preserved); supersession adjudication 06_REPORT/PE_MASTER_REVIEW_SUPERSESSION_R1.md CLAIM_MATRIX (2)/(8)
- standing text (verbatim):

A byte-correct CSV does not imply the interpretation of that CSV is correct. The origin-triple census measured “no writer of the .data triple 0xBA921C/20/24” (valid, 268 imm32 occurrences, 0 store-class) and the analysis layer illegitimately concluded “=> S == {0,0,0} for the whole process lifetime, immutable” — writes through the RETURNED singleton pointer never touch the triple addresses; the measurement and the inference had different subjects.

- evidence_pointer: docs/audits/PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915/01_RAW/ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt [T.10] (corrected) + 02_ANALYSIS/ORIGIN_STATUS_CORRECTION.md
- lineage_ref: PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915 standing lesson OMC/L2 (00_CONTROL/AMEND_LOG_R1.md STANDING LESSONS + 06_REPORT/PE_MASTER_REVIEW_SUPERSESSION_R1.md CLAIM_MATRIX (10))

---

## Entry OMC/L3 — POINTER_RETURN_ANALYSIS_MUST_TRACK_ALIAS_PROVENANCE

- operation: STANDING-RULE
- applied_by: PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915 (authority: the human authorization of PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915 relayed via PE-MASTER; the bounded in-place correction of docs/audits/PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915)
- claims: the provenance-blind write-through census defect (the single writer site 0x00458E27 missed by the ECX-only alias class); supersession adjudication 06_REPORT/PE_MASTER_REVIEW_SUPERSESSION_R1.md CLAIM_MATRIX (1)/(2)
- standing text (verbatim):

For any function returning a pointer, a “does anyone write through it” census must track the pointer's provenance across register copies and aliases (mov ecx,eax; mov edi,eax; ...), keep tracking after the ORIGINAL register is overwritten (mov eax,0 does not invalidate S_PTR living in ECX), handle stack spills/escapes with honest INSUFFICIENT_PROOF_* residuals, and classify escapes with bounded callee-head windows — never converting head-bounded absence into global absence. The SF case: the prior census examined only the ECX alias class (9 pair-site consumers) and never the EAX-retaining sites; the single writer site kept the pointer in EAX.

- evidence_pointer: docs/audits/PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915/01_RAW/ORIGIN_SINGLETON_WRITE_THROUGH_CENSUS.csv (99 rows, N=16 primary + N=8 historical view; 1 writer, 43 read-only escapes, 12 unresolved escapes disclosed)
- lineage_ref: PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915 standing lesson OMC/L3 (00_CONTROL/AMEND_LOG_R1.md STANDING LESSONS + 06_REPORT/PE_MASTER_REVIEW_SUPERSESSION_R1.md CLAIM_MATRIX (10))

---

## Entry OMC/L4 — NEGATIVE_EXISTENCE_CLAIM_REQUIRES_ESCAPE_CHANNEL_ACCOUNTING

- operation: STANDING-RULE
- applied_by: PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915 (authority: the human authorization of PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915 relayed via PE-MASTER; the bounded in-place correction of docs/audits/PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915)
- claims: the branch-B “0x4B1B70 self-recursive, statically dead” attribution (REJECTED_AS_ATTRIBUTED by the correction); supersession adjudication 06_REPORT/PE_MASTER_REVIEW_SUPERSESSION_R1.md CLAIM_MATRIX (7)
- standing text (verbatim):

A negative-existence claim (“no writer exists”, “statically dead”, “never called”) must account for every channel through which the negative could be escaped: direct E8/E9, imm32 address-takers, vtable membership, callee-head forwarding, stack spills, and FUNCTION BOUNDARY ATTRIBUTION (which function actually contains the cited call site — verified by decode from the function start, not by nearest-preceding-prologue). The branch-B case: the “0x4B1B70 self-recursive, statically dead” claim failed boundary attribution — the cited E8s lie inside FUN_004B1C70, which has an external caller in the packet Execute dispatcher.

- evidence_pointer: docs/audits/PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915/01_RAW/ORIGIN_SETTER_REACHABILITY_RAW.txt [R.6] (corrected) + 06_REPORT/QC_AUDIT_R3.md F1 + AMEND-23/28
- lineage_ref: PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915 standing lesson OMC/L4 (00_CONTROL/AMEND_LOG_R1.md STANDING LESSONS + 06_REPORT/PE_MASTER_REVIEW_SUPERSESSION_R1.md CLAIM_MATRIX (10))

---
