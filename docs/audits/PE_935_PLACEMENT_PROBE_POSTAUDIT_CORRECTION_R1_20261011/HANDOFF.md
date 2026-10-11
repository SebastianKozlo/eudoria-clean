# HANDOFF.md — PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011

## What this run did

Bounded correction-only run fixing the three P2 of the external Desktop post-audit of
`938aa946` (DA-1/R2-5 false SCANNED, DA-2/R2-2 distinct-record cap, DA-3 effective
Budget validation) and closing the two earlier observations (PA-1 XYZ 1200/4800
regression coverage gap, PA-2 unconditional-PASS identity gate). Published on the
RESULT branch `research/pe935-placement-probe-census-postaudit-r1-20261011` as one
commit with parent `938aa9462560873126f1e9114dba0319062772f1` (exact SHA in the
terminal report to PE-MASTER and the PRIVATE_EVIDENCE receipts — deliberately not
written into this commit's files).

## Where everything is

- `tools/placement_probe/placement_probe.mjs` — corrected tool (DA-1/DA-2/DA-3;
  exported `censusGate`, `budgetLimitErrors`; `layoutRefusals` counter).
- `tools/placement_probe/verify_inputs.mjs` — PA-2 live identity gate (16 frozen pins).
- `tools/placement_probe/tests/` — 5 new test files (da1/da2/da3/pa1/pa2) + PA-1
  fixtures in `fixtures.mjs`; full suite 53/53.
- `docs/audits/PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011/` — this
  package: PRE/ (BOOT identities, baseline hashes, SOURCE_PACKAGE freeze, BASE test
  results, BASE POST replay 47/0, PRE measurements incl. the Desktop reproducer
  re-runs, branch reservation receipt, PA-2 runner, PRE reproducer), POST/
  (preregistered config, POST test results + measurements, identity-gate receipts +
  counterchecks, object-identity observations, run_post.mjs), QC/ (fresh internal
  review, findings ledger, gate matrix, final gate, fresh probes), CORRECTION_MATRIX,
  FEATURE_COVERAGE_MATRIX, CORRECTED_STATUS_ALGEBRA, BUDGET_ACCOUNTING, AMENDMENT_LOG,
  SUPERSESSION, EVIDENCE_INDEX, MANIFEST_SHA256, FINAL_REPORT (this handoff).

## Verification summary (units separated)

- original 7 kit tests: 7/7; BASE-27 before correction: 27/27; historical POST
  replay on BASE: 47 PASS / 0 FAIL; final suite: 53/53.
- POST named battery: 13 cases — 12 PASS + 1 CONTROL_PASS (the forced-copy mutant
  detection) + 0 FAIL; QUALIFICATION_PASS with an aggregator that refuses PASS
  (exit 4) when any single required result is removed.
- Fresh internal QC: 5/5 own probes (census tail on fresh 6-entry bytes, object
  collections at a different instrument point, effective Budget on a fresh mutated
  instance, live gate on a fresh private mutant, scope/frozen-package git probes).
- Standing science: UNCHANGED. No game payloads, no pilot, no new RE. HARD_STOP=YES.

## What the NEXT session must NOT inherit as established

- `CANDIDATE_ONLY_NOT_PLACEMENT_PROOF` still holds for every candidate.
- `MODEL_218757_TO_WORLD_INSTANCE`, `WORLD_INSTANCE_IDENTITY`, `HISTORICAL_PLACEMENT`
  = NOT_ESTABLISHED; `WORLD_XYZ_RECOVERED` = NO; `CANONICAL_GATE_EFFECT` = NONE.
- The tool is qualified on SYNTHETIC data only. A pilot scan of original game
  payloads remains AWAITING_HUMAN_AUTHORIZATION and requires the external Desktop
  post-audit of this run's published commit first.

## Next step for the controller (PE-MASTER)

1. Commission the external Desktop post-audit of the exact published SHA (same
   discipline as the previous audit: independent refs/manifest/blob verification,
   own reproducers on the census tail, object identities and Budget path).
2. Only after that audit closes without new P0/P1/P2, decide whether to authorize the
   pilot scan contract. Do not reuse this run's internal QC as the external audit.

## Resume instruction (if anything is PARTIAL/blocked)

Nothing is PARTIAL: qualification passed, the reservation is owned, publication
proceeded per contract section J. If the remote push had failed, the state would be
COMMITTED_LOCAL/PUSH_PENDING (work preserved, no second commit) and the resume
instruction would be: `git push origin refs/heads/research/pe935-placement-probe-census-postaudit-r1-20261011`
(fast-forward only) followed by a fresh GET of the exact ref — nothing else.
