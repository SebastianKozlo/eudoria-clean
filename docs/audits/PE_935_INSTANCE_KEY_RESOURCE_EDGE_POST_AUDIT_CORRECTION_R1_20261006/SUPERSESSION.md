# SUPERSESSION — PE_935_INSTANCE_KEY_RESOURCE_EDGE_POST_AUDIT_CORRECTION_R1_20261006

Explicit new supersession/review record per contract §12. This record
supersedes status ROUTING of the source run's interpretations. It does NOT
erase, alter or rewrite any historical file: the source package
(SOURCE_RUN below) is READ-ONLY and byte-identical; its texts remain the
historical evidence, with the statuses below as the CURRENT routing.

## Status block (authoritative; every value measured or adjudicated in THIS run)

```text
SOURCE_RUN = PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006
SOURCE_SHA = f129fd5aa8e30f0f19c8903fe0d97899b9fe6510
DESKTOP_POST_AUDIT = REQUIRE_CORRECTIONS
DESKTOP_REPORT_SHA256 = 664579B1F0762C9CE6266CDDF75EF9DEDA426E702800FAA0F837EC07EEB19572
SCIENTIFIC_CORE = PRESERVED_IN_AUDITED_STATIC_SCOPE
LEDGER_SCHEMA_ORIGINAL = FAIL
LEDGER_SCHEMA_CORRECTED = PASS
ORIGINAL_PROCESS_BUDGET_COMPLIANCE = FAIL
PROCESS_EXCEPTION_AUTHORIZATION = HUMAN_ADJUDICATED_NOW
RETROACTIVE_PRIOR_AUTHORIZATION = NO
GOVERNANCE_PROVENANCE = CORRECTED
RESOURCE_EDGE_STATUS = NOT_ESTABLISHED_IN_EXAMINED_PATH
WORLD_XYZ_RECOVERED = NO
STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED
HISTORICAL_INSTANCE_DATA_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO
```

Value provenance (why each status is honest, not prefilled):
- LEDGER_SCHEMA_ORIGINAL = FAIL: the source FUNCTION_LEDGER.csv has 7/8
  malformed data rows and EDGE_LEDGER.csv 5/22 (Desktop independent
  reproduction; re-verified this run from the raw bytes: naive cell widths
  13/10/9x6 and 12/10x4).
- LEDGER_SCHEMA_CORRECTED = PASS: measured — the fail-closed
  03_SCRIPTS/ledger_schema_qc.py PASSED both corrected tables (LEDGER_SCHEMA_QC.json)
  and all five causal mutants were REJECTED (MUTATION_RESULTS.json). Not a
  publication-time placeholder.
- GOVERNANCE_PROVENANCE = CORRECTED: measured — the DPA3 validation passed
  (PERSISTENCE_PHASE_SPLIT_SOURCE = NOT_ESTABLISHED_IN_RECORDED_HUMAN_SOURCE;
  PHASE_SPLIT_BEHAVIOR_CLASSIFICATION = ORCHESTRATOR_PHASE_SPLIT;
  FINAL_PUBLICATION_AUTHORIZATION = PRESENT; no fabricated message, no
  rewritten chronology, historical files untouched).
- ORIGINAL_PROCESS_BUDGET_COMPLIANCE = FAIL is the HISTORICAL truth and stays
  FAIL; PROCESS_EXCEPTION_AUTHORIZATION = HUMAN_ADJUDICATED_NOW is the PRESENT
  decision only and never a retroactive authorization.

## Explicit supersessions

1. **MASTER_ACCEPTED (whole-package interpretation) — SUPERSEDED.** The
   original PE_MASTER_REVIEW.md of the source run records
   `RUN_VERDICT = MASTER_ACCEPTED (advisory)`. That whole-package
   interpretation is superseded by the independent Desktop post-audit
   (REQUIRE_CORRECTIONS on the exact commit f129fd5...) plus this correction
   record. The historical review file is NOT edited or erased; its verdict
   becomes historical/superseded routing. A reader of the newest
   AUDIT_ENTRYPOINT row (proposed in HANDOFF.md of this package) must be able
   to discover this supersession — the row states it explicitly.
2. **Machine-readable validity of the two original ledgers — SUPERSEDED.**
   The original FUNCTION_LEDGER.csv / EDGE_LEDGER.csv are not valid claim/
   evidence tables (malformed serialization); their machine-readable validity
   is superseded by FUNCTION_LEDGER_CORRECTED.csv / EDGE_LEDGER_CORRECTED.csv
   (schema PASS). The original CSVs remain valid only as preserved raw
   evidence of their cell texts.
3. **Process-budget compliance framing — SUPERSEDED.** The source run's
   "PASS WITH ONE DISCLOSED DEVIATION" (QC_REPORT Q7) and overall QC_PASS as
   process statements are superseded by the separated algebra:
   TECHNICAL_QC (byte-level PASS results) valid within their actual tested
   scope; PROCESS_COMPLIANCE = FAIL (historical); the present human
   adjudication accepts the disclosed exception NOW without retroactive
   authorization.
4. **Persistence-deferral human attribution — SUPERSEDED.** The historical
   attribution of the two-phase persistence split to a direct human
   instruction is superseded by the DPA3-corrected provenance
   (NOT_ESTABLISHED_IN_RECORDED_HUMAN_SOURCE / ORCHESTRATOR_PHASE_SPLIT);
   the publication authorization itself (FINAL_PUBLICATION_AUTHORIZATION =
   PRESENT) is NOT superseded — commit f129fd5... remains authorized.

## What is NOT superseded (preserved valid)

- All byte-level technical QC results of the source run within their actual
  tested scope (getter pin, 6-site census, receiver chain, map pins, RTTI
  identities, CTRL_A/B/C controls, negative controls) — re-verified by the
  source run's internal QC and the Desktop post-audit.
- The bounded scientific conclusions (SCIENTIFIC_CORE =
  PRESERVED_IN_AUDITED_STATIC_SCOPE): getter bytes; six direct E8 census in
  stated scope; selected ClientMovableObject receiver; GameClient
  different-object result; map-identity role in the examined path; SF key
  pass-through evidence; RESOURCE_EDGE_STATUS = NOT_ESTABLISHED_IN_EXAMINED_PATH.
- The historical artifacts themselves (READ-ONLY; Q15 zero hash diff).

## Discovery chain for auditors

AUDIT_ENTRYPOINT.md (not yet edited in this phase; proposed newest-first row in
HANDOFF.md) -> this package (SUPERSESSION.md, FINAL_REPORT.md, QC_REPORT.md,
LEDGER_SCHEMA_QC.json, MUTATION_RESULTS.json, the two corrected ledgers,
GOVERNANCE_DECISION.md) -> the READ-ONLY source package at commit f129fd5...
-> the Desktop post-audit REPORT.md (SHA256 above).
