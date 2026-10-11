# QC/INTERNAL_REVIEW.md — fresh-context internal QC

**RUN_ID:** `PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011`
**Phase:** FRESH INTERNAL QC on the FINAL BYTES (after CORRECTION and POST, before publication)
**Author/origin:** the executor session of this run, as a DISTINCT PHASE re-reading the
final code and re-measuring with fresh probes (`QC/qc_fresh_probes.mjs`, output
`QC/QC_FRESH_PROBE_OUTPUT.json`). This is INTERNAL QC — it is NOT the external Desktop
post-audit, and a replay of this or any harness is NOT a second implementation of the
checks. The external Desktop post-audit of THIS run's commit remains PENDING.

## What this QC phase PERSONALLY MEASURED (own probes, not inherited counters)

| # | Probe | Method (fresh) | Result |
|---|---|---|---|
| 1 | Census tail on NEW bytes | fresh 6-entry BNT2 (not the POST 4-entry fixture), fresh CLI invocation, fresh `--budget-layout-evals 50`, disposition list read directly from SUMMARY.json | `QC_PASS` — 1×SCANNED/PARTIAL + 5×OVER_BUDGET/NOT_ANALYZED, scannedPayloadCount=1, censusOk=true, whole tail accounted |
| 2 | Object collections | identity observer injected at a DIFFERENT program point than the POST observer (the `selected = found.slice(...)` line + the forward push), 3 raw inputs, retained cap 6; aliasing re-derived from the published CSV/top.json directly | `QC_PASS` — candidateCount == CSV rows == top.json rows, peak ≤ 6, rows carry entry/payloadSha256 (aliased live records, no copy population) |
| 3 | Effective Budget | fresh `Budget` instance with `limits` replaced post-construction (`retainedCandidates: 4096`) → refused at use time with `INVALID_CONFIGURATION`, `layoutAttempts=0` after the refusal; PLUS fresh structural source-text check of all four validation call sites | `QC_PASS` — refused before analysis start; constructor-validates/use-time-validates/masquerade-instanceof/contradictory-policy all present in the final source text |
| 4 | Live identity gate | fresh private mutant of pin #11 (byte 0 flipped → same size, different SHA) via the gate module directly; live receipt re-read | `QC_PASS` — mutant `SHA_MISMATCH` + `inputMatch=false`, clean path `MATCH`, live receipt PASS 16/16 REAL_SEQUENCE |
| 5 | Scope + frozen package | direct git probes: HEAD==BASE, 37 blobs of `PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011` unchanged vs BASE, allowlist census of every changed path | `QC_PASS` — HEAD 938aa946, SOURCE_PACKAGE unchanged (37/37 blobs), zero changed paths outside the allowlist |

Probe 5 initially FAILED its own allowlist filter: `stdout.trim()` on the porcelain
output eats the leading space of the FIRST line (`' M path'` → `'M path'`), corrupting
`slice(3)`. The probe was fixed (per-line cleanup) — a harness bug caught by the QC
phase itself, recorded in AMENDMENT_LOG.md; no tool code was involved.

## What this phase READ (did not re-measure) and accepts on its recorded evidence

- PRESERVED PRE (`PRE/PRE_MEASUREMENTS.json`, `PRE/BASE_TEST_RESULTS.json`,
  `PRE/BASE_POST_REPLAY.json`, `PRE/BOOT_INPUT_IDENTITIES.json`) — measured earlier in
  this same run; identities cross-checked at BOOT with an independent PowerShell
  Get-Item/Get-FileHash bootstrap in the invoking session.
- The pinned external Desktop post-audit package (REPORT/ADVERSARIAL_RESULTS/…), whose
  PRE values (tracker 4 vs distinct 8; 256 vs 280/512; R2-5 census; DA-3 bypass) this
  run reproduced on unchanged BASE during PRESERVED PRE and then corrected.
- POST battery outcomes (`POST/POST_TEST_RESULTS.json`) — measured by this run's own
  preregistered harness; the fresh probes above re-verified the census tail, object
  collections, effective Budget and identity gate WITHOUT reusing POST's case objects.

## Independence honesty

- The fresh probes used DIFFERENT fixtures (6 entries), DIFFERENT instrument points
  (selection slice vs POST's creation hook), DIFFERENT pins (pin #11 vs the tests' pin
  usage), and direct file reads.
- What could NOT be made independent here: the QC phase shares the executor's code
  base under test (it re-runs the same corrected tool), so an undetected shared
  defect in the tool itself would fool both. This is exactly why
  EXTERNAL_DESKTOP_POST_AUDIT stays PENDING and qualification of the tool is not a
  pilot authorization.

## Counter semantics statement (section E obligation)

At a lowered layout limit of 60 the corrected tool reports `layoutAttempts=61`
(requests), `layoutRefusals=1`, executed layout evaluations = 60, `layoutsAdmitted`
reported separately. 61 is therefore NOT a claim of 61 performed layout evaluations —
the refusal record itself names "executed evaluations: 60". Verified by suite test
`DA3: positive controls` and POST case `DA3_POSITIVES`.

## Verdict

`INTERNAL_QC_PASS` — all five fresh probes green; no P0/P1/P2 findings open in scope;
P3 ledger in QC/FINDINGS.json. Fresh context: YES (distinct phase, own probes).
