# EVIDENCE_INDEX — PE_935_INSTANCE_KEY_RESOURCE_EDGE_POST_AUDIT_CORRECTION_R1_20261006

RECORDS-ONLY correction package. No proprietary game payload is included; no
EXE copy or byte read was performed by this run. Every artifact below lives
under OUTPUT_ROOT
(docs/audits/PE_935_INSTANCE_KEY_RESOURCE_EDGE_POST_AUDIT_CORRECTION_R1_20261006/).

## Package artifacts (this run's writes)

| Artifact | Content | Role |
|---|---|---|
| GOVERNANCE_DECISION.md | decision identity; the VERBATIM human adjudication instruction of 2026-10-06 with source and save time; §0 adjudication A block + annotations; DPA2 historical-budget-breach record; DPA3 provenance correction; P3-1..P3-6 record; phase boundaries; preflight | KROK 0-style governance record, written FIRST, before any correction work |
| INPUT_IDENTITIES.md | pinned input identities (contract, Desktop report, repo/base, EXE carried identity); foreign untracked inventory; the full 36-file SOURCE_PACKAGE baseline re-hash census; evidence-bearing source records used | identity + Q3/Q15 baseline evidence |
| FUNCTION_LEDGER_CORRECTED.csv | the corrected FUNCTION ledger: exactly the 10 contract §6 columns, 8 data rows, csv.DictWriter serialization | DPA1 authoritative replacement for the malformed FUNCTION_LEDGER.csv |
| EDGE_LEDGER_CORRECTED.csv | the corrected EDGE ledger: exactly the 11 contract §6 columns, 22 data rows | DPA1 authoritative replacement for the malformed EDGE_LEDGER.csv |
| 03_SCRIPTS/ledger_schema_qc.py | fail-closed machine schema QC: separate FUNCTION/EDGE schemas; header/width/uniqueness/DictReader/CITED-artifact-existence checks; EDGE STATUS vocabulary + swap detection; FUNCTION no-STATUS-column assertion; mutation mode (MUT-A/B per table, MUT-C EDGE swap) on temp copies | Q4–Q10 production validator (never consults manifest/Git) |
| LEDGER_SCHEMA_QC.json | machine results of `check` mode (both tables PASS; per-check outcomes) | Q4–Q7 measurement |
| MUTATION_RESULTS.json | machine results of `mutate` mode: 5 mutants, clean baselines, mutated verdicts, exact failed predicates, CAUSAL_FAIL verdicts | Q8–Q10 measurement |
| QC_REPORT.md | Q1–Q16 measured; RECONSTRUCTION_MAP (per-field derivations for both corrected ledgers); residual honesty notes | targeted QC report |
| FINAL_REPORT.md | what was corrected (DPA1/2/3, P3-1..6), preserved science, status block, honest unresolved findings, phase/persistence state | correction report |
| SUPERSESSION.md | the §12 status block with value provenance; explicit supersessions (MASTER_ACCEPTED, ledger machine-validity, process-compliance framing, persistence attribution); preserved-valid list; discovery chain | supersession record |
| EVIDENCE_INDEX.md | this file | evidence index |
| HANDOFF.md | terminal status (§19, this phase) + proposed AUDIT_ENTRYPOINT.md newest-first row (§13) + persistence instructions | handoff |
| CORRECTION_PACKAGE_MANIFEST_SHA256.csv | manifest generated LAST: every physical file under OUTPUT_ROOT minus the manifest itself (rel path, byte size, SHA256); header comment documents the entrypoint-row exclusion and the persistence-phase regeneration | final package manifest |

## Evidence used (READ-ONLY; existing persisted records only)

Source package docs/audits/PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006/
(full 36-file census in INPUT_IDENTITIES.md; byte-identical before/after — Q15):

- FUNCTION_LEDGER.csv / EDGE_LEDGER.csv — the raw malformed cell texts
  (preserved evidence per row; the basis of every corrected field).
- FINAL_REPORT.md — §4 branch trace; §6 budget accounting; §7 status algebra
  table (the authoritative per-field OBSERVED_OPERATION / FINAL_SEMANTIC_ROLE
  / HISTORICAL_INPUT_AVAILABILITY assignments used for reconstruction); §1.3
  (the superseded broad wording, per P3-5).
- QC_REPORT.md — Q1–Q9 + the two record-repair rounds (F1–F6, R2-1/R2-2).
- PE_MASTER_REVIEW.md — the historical MASTER_ACCEPTED (superseded by
  SUPERSESSION.md; file not edited).
- GOVERNANCE_DECISION.md — AMENDMENT 1 (State A/B identity pins; the 61-char
  SHA display corrected per P3-1; the superseded persistence attribution
  corrected per DPA3).
- 01_RAW/BYTE_WINDOWS.txt — the 10 persisted byte windows (F00401360,
  F005247C0, F00509330 + SF_ctor_tail, F00856190 (ends 0x0085620F — P3-3
  limitation), ctor prologue (C7 06 B0 DC A7 00 @0x00528EA2 — P3-2), base-ctor
  keystore, W00459fd0, F0064B1E0, F004157B0).
- 01_RAW/E8_CENSUS.json — the six direct E8 hits + zero-counts.
- 01_RAW/GETTER_PIN.txt / GETTER_PIN.json / GHIDRA_VERIFY.json /
  GHIDRA_DISASM_WINDOWS.txt / GHIDRA_DECOMPILES.txt — the getter pin, the
  6/6 PROVEN_EXACT instruction starts, the disassembly windows and the
  decompiles used for row-internal cross-references.
- 01_RAW/RTTI_PROBES.json — the 3 calibration walks + the GameClient /
  ExtraData probes + the honest NOT-A-CLASS-VTABLE negative.
- 01_RAW/QC_CONTROLS.json — CTRL_A/B/C control results (the direct-E8
  predicate basis for the P3-5 scoping).
- 01_RAW/GovernanceWriteTime.txt — the preserved 64-char State-A SHA (P3-1).
- CALLSITE_SHORTLIST.csv, COMMITTED_PACKAGE_MANIFEST_SHA256.csv,
  00_CONTROL_INTERNAL_QC/* (QC_GATES.csv with the malformed G2 width — P3-6;
  QC_MEASUREMENTS.txt; QC_REPORT_INTERNAL.md; MANIFEST_REHASH.csv;
  FULL_READ_LOG.txt; QC_PACKAGE_MANIFEST_SHA256.csv; qc_negative_controls.ps1).

External authoritative input (read-only):

- Desktop post-audit REPORT.md
  (C:\Users\User\Documents\ChatGPT\PE\PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_DESKTOP_POST_AUDIT_20261006\REPORT.md,
  14,545 B / 664579B1F0762C9CE6266CDDF75EF9DEDA426E702800FAA0F837EC07EEB19572)
  — REQUIRE_CORRECTIONS; findings DPA1/DPA2/DPA3 + P3-1..P3-6.
- The present human adjudication instruction (2026-10-06) — saved VERBATIM in
  GOVERNANCE_DECISION.md before any correction work.
- Contract OPENCODE_RECORDS_ONLY_CORRECTION_REVIEWED.md (24,218 B /
  EA86AA0897695C100D89BD68438318F6DDC9BD50DE28C7A6EDCC59ACF4ED61ED) — the
  dispatch/authorization document, not modified.

## NOT_CHECKED (explicit)

- No independent/fresh-context QC of THIS correction package in this phase
  (PE-MASTER audits it before persistence; no independent-QC claim is made).
- No new RE verification of any byte claim (records-only; all technical
  content is carried from the source package's verified records and the
  Desktop post-audit).
- Runtime behavior, payload contents, consumers of ExtraData+0x10,
  FUN_007B6A80/FUN_007B6A80-class analyses, indirect/inlined readers: not
  examined, not claimed.
- The future persistence phase's entrypoint adaptation and its manifest
  regeneration (including the entrypoint row) — prepared here only as a
  proposed row in HANDOFF.md.
