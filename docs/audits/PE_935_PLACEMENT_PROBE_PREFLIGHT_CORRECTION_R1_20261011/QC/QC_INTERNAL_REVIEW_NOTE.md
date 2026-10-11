# QC_INTERNAL_REVIEW_NOTE — PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011

## Origin statement

This QC package was produced by a **fresh internal QC worker** — a separately-dispatched
**pe-master-auditor** context under PE-MASTER, created specifically for
`PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011` (INTERNAL_QC mode), reading the
preserved PRE, the corrected code and the POST artifacts **from disk** in a fresh context with
no prior session state from the executor's run. It is **internal to this run**: it is NOT an
independent Desktop post-audit, which remains **PENDING** after publication (per contract §10/§11),
and it is not a PE-MASTER verdict, milestone closure or canonical promotion of anything.

## What this QC did

- Verified the contract file against the dispatch SHA256/size (3F443D86...EA3, 25139 B) and read
  it in full.
- Read ALL assigned artifacts to end-of-file: the five PRE records (incl. PRE_MEASUREMENTS.json,
  COUNTERCHECK_BASELINE.json, ORIGINAL_BEHAVIOR.md, ORIGINAL_TEST_RESULTS.json), the corrected
  tools (placement_probe.mjs 469 lines, ids_from_export.mjs, README.md), all four test files,
  fixtures.mjs, both POST harness scripts, POST_MEASUREMENTS.json, POST_TEST_RESULTS.json,
  CORRECTION_MATRIX.csv, FEATURE_COVERAGE_MATRIX.csv, BUDGET_ACCOUNTING.json, AMENDMENT_LOG.md.
- Re-hashed the full input identity chain (contract, original ZIP, original kit files, original
  7 test files, corrected tool files, BASE adapters by git blob and SHA256, worktree HEAD).
- Built a **QC-owned independent mini-implementation** (`qc_recompute.mjs`) from the contract
  text — it does NOT import placement_probe.mjs — and reproduced both §7 cases and the O3
  sample arithmetic from raw fixture bytes; the three fixture SHA256s are byte-identical to
  POST fixtureIdentity.
- Re-executed the corrected tool on every load-bearing POST value (`qc_verify_post_claims.mjs`,
  including an O2 census run on the REAL BASE adapters), re-ran the full 23-test suite fresh
  (23/23), and ran three targeted probes: a 9-input RETAINED_CANDIDATES overshoot probe
  (`qc_retained_gap_probe.mjs`: peak 261 > ceiling 256), a single-input layout-attempt
  measurement (2142 > B3's cap 700), and a full-vs-truncated B6 message comparison.
- Scanned the tool, README, tests, matrices and POST for placement/world-XYZ/218757-join/
  milestone over-claims (none found) and for trivially-true test assertion patterns (none found;
  the one weak `??` assertion was removed by the executor in amendment round 1 and is verifiably
  gone; the remaining `c.fullCensus ?? c.sampleStats` is pinned by the censusStatus assertion).

## Independence limitations (stated honestly)

1. **Same engine family as the executor.** This QC ran on the same AI infrastructure family
   (GLM-class model under OpenCode) as the correction executor. It is an independent CONTEXT
   (fresh, no shared session state, adversarial task framing, QC-owned scripts), not an
   independent implementation platform.
2. **Same physical machine and Node runtime** (v22.22.0, win32) as POST. Identical environment
   reduces the value of "fresh execution" for environment-dependent behavior; however, all
   load-bearing cases here are deterministic byte-arithmetic and were ALSO recomputed by a
   QC-authored independent implementation, not only re-executed through the executor's code.
3. **Fixture definitions were read from the executor's fixtures.mjs** for the re-execution
   harness (the Q2 recomputation itself rebuilt all fixtures from the contract text and matched
   byte-for-byte, which is the non-circular check).
4. **The corrected tool itself was used** to compare POST values against code behavior (Q1b) —
   by design of that subtask; the §7/O3 ground-truth values were established independently
   before any such comparison.
5. **QC did NOT modify any project file.** All QC writes are inside the QC/ directory (the five
   required outputs plus four QC-owned probe scripts, which document exactly how every measured
   claim in this package was obtained).
6. **Not checked:** the publication stage (§11 commit/manifest/push/entrypoint — not yet
   performed at this pipeline stage), byte-level regeneration of POST by re-running the
   executor's harness (would rewrite POST; forbidden), re-execution of the original R1 PRE
   measurements (accepted as preserved record), and the untested additional census code paths
   (recorded as untested, see F10). The full NOT_CHECKED list is in QC_STATUS.json.

## Verdict summary

**QC_STATUS = PASS_WITH_FINDINGS** (0×P0, 1×P1, 3×P2, 6×P3).

- Independently CONFIRMED: the corrected behaviors for §5 (fail-closed config, census
  reconciliation, sample/census separation, f32/u32 diagnostics, single min-distinct-id
  interface), §6 O1..O7, §7 S7a (126/0) and S7b (0.9 legacy vs 0.7 joint, 56/80), POST-vs-code
  identity, PRE preservation, and the standing-science invariants.
- NOT met (findings): the §8 RETAINED_CANDIDATES peak-across-all-structures semantics (F1, P1 —
  measured overshoot 261>256; B5 single-input only), the §8 reservation-before-read ordering
  and its README/POST wording (F2), the B3 cross-input aggregation expectation with the
  SCANNED-for-unanalyzed disposition defect (F3), the self-contradictory CORRECTION_MATRIX
  ORIGINAL_SEVEN_TESTS row (F4), plus six P3 hygiene/provenance items. Per §10, the unmet
  expectations block a blanket CORRECTION_PASS for the affected B-case expectations; the
  executor's stamped all-PASS overstates §8 completeness and should be read as PARTIAL /
  REQUIRE_CORRECTIONS for the F1..F3 budget-semantics items.

This note is part of the run package; the independent Desktop post-audit of the published SHA
remains PENDING and is not substituted by this internal QC.
