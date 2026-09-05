# PE_MASTER_STANDING_RETRACTIONS — annotations ordered by the PE-MASTER V4.1 re-audit
# (ORDERED_WORK item 3 of the MASTER_ACCEPTED verdict, 2026-09-05)
# Written by pe-master-auditor in the V4.1 run mirror. The prior review files are NOT
# edited (no history rewrite) — this file is the annotation carrier.

## Standing self-retractions of record (PE-MASTER, originally recorded @ faf215b)

1. **The repair-run review claim "the divisor-candidate line disappeared from the live
   matrix" (PE_MASTER_REVIEW.md of PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439,
   lines 83-84 + 135) — RETRACTED.** The claim was true ONLY for the V3 MARKDOWN format
   (the MD generator never printed the carried fields); the live V3 JSON carried the
   stale content (lines 328/376/721 + the manifest flow at 2157/3519). The verification
   miss: no forbidden-phrase census was run over the carried fields of the live JSON.
2. **The completion-run pre-check claim 9 ("RETRACTIONS complete, nothing retracted
   resurrected — CONFIRMED") — RETRACTED-as-verified.** The needle census covered only
   NUMERIC retractions (4,912,912; the old sweep hashes) — a set structurally incapable
   of detecting SEMANTIC retractions (32768.0 / u16/K / rand*2.0 / queued).
   REMOTE_AUDIT_READINESS:TAK is limited to the mechanical/SHA layer.
   Canonical record: docs/audits/PE_M1_GATE_PACKAGE_COMPLETION_R1_20260905_041816/
   PE_MASTER_FINDING_VERIFICATION.md (commit faf215b).

## Canon lesson (standing discipline)

A retraction-completeness claim REQUIRES a forbidden-phrase census over ALL live fields
of the artifact (including registry/metadata fields and both formats), never an
inherited prior from a previous audit layer. The semantic gate with negative fixtures
(the instrument missing from both the executor's check and PE-MASTER's own pre-check)
is now a permanent part of the gate-package discipline (V4: N1-N5; V4.1: N1-N6 + the
full-document walk + the PE-MASTER counter-check poisoning method).

## Advisory wording notes (from the V4.1 re-audit; recorded, no re-run ordered)

- payload_scan_final_v4_1.json self_reference_exclusion: "the ONLY unscanned bytes" is
  strictly imprecise — the artifact_index.csv PENDING->real row delta (~89 B) is also
  unscanned; both exclusions ARE disclosed in the same field and in REPORT.md.
- The commit message 2653662 conflates the scan universe (41 files = the commit set +
  run-local originals) with the commit set (25 files); the authoritative records
  (REPORT.md + commit_set_coverage) describe the composition exactly.
