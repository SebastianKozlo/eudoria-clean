# POSTAUDIT_NOTICE_R1.md — additive notice for the MINCAP run folder

This additive notice accompanies the successor run PE_935_PROVIDER_PROVENANCE_APPLIER_JOIN_HIGH_TASK_OPENCODE_SAVED_R1_20261023 (docs/audits/PE_935_PROVIDER_PROVENANCE_APPLIER_JOIN_HIGH_TASK_OPENCODE_SAVED_R1_20261023/).

The successor run PRESERVES the MSC-A01..A06 baseline corrections (external postaudit of PE_935_OWNER_SLOT1_MINCAP_WRITER_SOURCE_DEFAULT_TASK_DEEP_POSTAUDIT_R1_20261023):
- MSC-A01: exact B/R/P pointer levels kept; [B+0x2C] never conflated with [R+0x2C]; reload-equality NOT claimed across opaque calls; FIRST_MISSING_EDGE formulated as concrete object/field/coverage-gap.
- MSC-A02: CALL 0085CDE0 @005284AC reconciled with input/application/read/cache (applier contract verified; permuted 48-byte block to [[R+0x2C]VT+0x14]; conditional 52-byte raw record-head cache at receiver+0x30); no world/root promotion.
- MSC-A03: enum [R+0x20]==3 documented as gating only the matrix-construction branch (identity vs 0096CCB0); entry guards remain the null checks on [B+0xC]/[B+0x10].
- MSC-A04: STATIC_CLASS_VTABLE_BINDING (construction level) kept separate from REGISTER_LOOKUP_JOIN (NOT_ESTABLISHED); the prior base ctor 0x0085B1B0 / base table 0x00A91E4C referenced and NEW: the successor CONFIRMED the base-table store 0xA91E4C @0085B1C1 at construction level (additive; class identity and runtime dispatch still UNKNOWN).
- MSC-A05: accounting limitations kept honest (failed attempts charged, neighbor fragment F00528600 charged, APPROX/LOWER_BOUND actuals, no COMPLETE_WITHIN_BOUND); fresh QSCI/QACC children had their own ADMITs; the QC caveat (QSCI_3 QC_PARTIAL, admission-scope) is retained in the published REPORT.
- MSC-A06: producer 0085C280 guard/zero-fallback premise kept as premise (not re-read this run; not upgraded to fact).

The successor run made NO new original-EXE access (SAVED_ONLY; zero reads incl. stat/hash; A75378 remains NOT_READ), executed 21 native tasks with pre-dispatch admission, and closed with: SCIENCE_VERDICT = PARTIAL_PASS_WITH_DATA_BARRIERS (R attach POST_CONSTRUCTION_ONLY; P-class qualification barrier; destination opaque), PROCESS_VERDICT = PARTIAL_NONCOMPLIANT_WITH_DISCLOSED_INCIDENTS, 0 material QC findings, ACCOUNTING_PASS.

WORLD_XYZ_RECOVERED = NO; HISTORICAL_PLACEMENT = NOT_ESTABLISHED; CANONICAL_GATE_EFFECT = NONE.
