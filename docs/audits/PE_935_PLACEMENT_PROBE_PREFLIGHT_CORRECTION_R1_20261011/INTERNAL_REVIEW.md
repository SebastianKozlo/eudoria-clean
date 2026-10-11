# INTERNAL_REVIEW — PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011

## Authorship / origin (honest provenance)
- Executor: the PE-MASTER session of 2026-10-11 (OpenCode, GLM), executing the human-authorized contract OPENCODE_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R2_COMPLETE.md (25139 B / SHA256 3F44D8680130BD24854F02232D29D8BD6EE6CA54B5BC9C3312087F617888EA3, identity verified PASS).
- PRE measurement harness, POST harness, matrices generator, fixtures, corrected tool, tests, README, this package: authored in this run; every file's SHA256/size is in MANIFEST_SHA256.csv.
- The two fresh internal QC passes (round 1 + round-2 re-QC) were performed by a separately-dispatched pe-master-auditor agent context reading PRE, code and POST from disk, writing only QC/** records. QC/QC_STATUS.json (PASS_WITH_FINDINGS, F1..F10) and QC/ROUND2_RECHECK/RECHECK_STATUS.json (PASS_WITH_FINDINGS, R2-1..R2-6, F1-F7/F9/F10 FIXED_VERIFIED, F8 publication-pending) are verbatim worker outputs.

## Independence limitations (stated honestly)
- The internal QC contexts run on the same model family as the executor (same-engine risk); the independent recomputations (126 layout attempts; 56/80 triples; per-axis 72/80; sample 1.0 vs full 0.25; adversarial peak probes) were re-derived from raw fixture bytes by separate mini-implementations, which mitigates — but does not replace — a cross-engine audit. The external Desktop post-audit remains PENDING.
- The "two modes of one checker" trap was avoided: QC recomputations do not import placement_probe.mjs; the correction tool itself is one implementation (its suite is regression, not an independent oracle). PRE vs POST comparisons use the SAME synthetic fixtures (byte identity recorded in PRE/INPUT_IDENTITIES.json and POST fixtureIdentity), so PRE→POST differences are attributable to the tool change, not fixture drift.
- The original kit tests (probe.test.mjs, cli-fixture.test.mjs) are byte-identical copies of the ZIP originals (SHA256 5459C1EB... / 5E643FD8... — see PRE/BASELINE_FILE_HASHES.csv); the shim adapters used in mechanics tests are the kit's own placeholders and are NOT utożsamiane with the actual-project-adapter test (O6 uses the BASE adapters, git blobs 1fb8629.../a9c9f04...).

## What the run does NOT claim
- No historical placement, world XYZ, instance identity or model→instance join — CANDIDATE_ONLY everywhere (grep-verified by QC Q5 across tool, tests, README, matrices, PRE and POST).
- No canonical gate effect; no milestone advancement; standing-science statuses frozen (see FINAL_REPORT.md).
- The corrected tool is qualified ONLY on synthetic inputs; no original PCG payload was scanned for placement in this run.

## Residual defect disclosure (beyond FINAL_REPORT summaries)
R2-5 (P2) and R2-1..R2-4 (P3) are described in FINAL_REPORT.md with revalidation gates. R2-6 documentation inconsistencies were corrected before publication (this is record-keeping for publication integrity, not a third code-fix round). MAX_FIX_ROUNDS = 2 is exhausted; CORRECTION_STATUS = PARTIAL is the honest terminal state, persisted per contract §11 (PASS, PARTIAL and REQUIRE_CORRECTIONS MUST be persisted when integrity gates hold).