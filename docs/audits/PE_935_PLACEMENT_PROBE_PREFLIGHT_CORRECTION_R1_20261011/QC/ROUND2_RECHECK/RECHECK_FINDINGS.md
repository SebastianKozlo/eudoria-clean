# RECHECK_FINDINGS — PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011 (ROUND 2 re-QC)

Fresh re-QC of the ROUND 2 correction delta on the FINAL bytes by a separately-dispatched
pe-master-auditor context. Read-only on the worktree (all writes confined to
`QC/ROUND2_RECHECK/` plus OS temp for harness copies). Every finding below was **measured**
by QC-owned probes (`recheck_probes.mjs`, outputs persisted in `recheck_probes_output.json`)
or by an executed falsifier; none is speculative.

**Statement:** This re-QC is **internal to the run** — it is NOT an independent Desktop
post-audit (that remains PENDING after publication per contract §10/§11), NOT a PE-MASTER
verdict, NOT milestone closure and NOT canonical promotion.

All ten round-1 findings (F1..F10) were re-checked on the final bytes:
**F1, F2, F3, F4, F5, F6, F7, F9, F10 = FIXED_VERIFIED; F8 = FIXED_NOT_VERIFIED
(PUBLICATION_PENDING — FINAL_REPORT.md does not exist at re-QC time).**
Suite re-executed by this re-QC: **27/27 pass, 0 fail, exit 0** (matches POST_TEST_RESULTS.json;
`originalSevenPass` recomputed true from my own TAP). Full POST harness re-executed from a
temp copy of byte-identical code: **47 PASS / 0 FAIL**, value-identical on every compared
case field.

New/residual findings below. Severities: P0 blocks run/persistence; P1 material unmet
contract requirement; P2 real defect requiring a narrow correction; P3 hygiene/documentation/
provenance.

---

## R2-5 (P2) — after a shared-budget exhaustion, the 2nd+ admitted-but-unanalyzed payloads of a MULTI-ENTRY container remain mislabeled SCANNED (residual of the F3 class)

- **File/lines:** `tools/placement_probe/placement_probe.mjs` — the sources loop
  `for (const src of sources)` at lines 404-437: the pre-exhaustion branch (405-414)
  corrects ONLY the current (first unanalyzed) `src` to OVER_BUDGET, pushes one skip row
  and `break`s (line 413). Container entries are ALL admitted and labeled SCANNED in the
  admission loop (lines 369-386) BEFORE any analysis; a container with m admitted entries
  where the budget exhausts during entry k therefore leaves entries k+2..m untouched.
- **Contradicted claim:** AMENDMENT_LOG ROUND 2 item 3 ("an admitted payload that was never
  analyzed ... is corrected to OVER_BUDGET" — as a general rule); contract §5.2 disposition
  truthfulness (a SCANNED disposition asserts analysis work was performed); the round-1 F3
  rationale ("known remaining entries after exhaustion are OVER_BUDGET").
- **Evidence (measured, probe P6):** container `c.bnt` with 4 `records80` entries,
  `--budget-layout-evals 100` (exhaustion during e0's analysis at attempt 101):
  `e0.rec` SCANNED (partially analyzed — honest), `e1.rec` OVER_BUDGET with detail
  "budget exhausted before analysis: LAYOUT_EVALUATIONS" (the fix working), **`e2.rec`
  SCANNED and `e3.rec` SCANNED — never analyzed: zero layout attempts on them, NO skip
  rows for them, no correction**; `censusOk: true` (4 dispositions = 4 declared), so the
  census reconciles numerically while being semantically false for e2/e3.
- **Failure mechanism:** the `break` at line 413 exits the sources loop after correcting a
  single payload; the remaining `sources` iterations never run. Raw inputs and
  1-2-entry containers are covered; ≥3-entry containers under LAYOUT_EVALUATIONS/
  RETAINED_CANDIDATES exhaustion are not. Reachable in normal scanning: the default
  LAYOUT_EVALUATIONS ceiling (100000) is consumed by ~46 records80-class payloads, so any
  larger real container crosses it mid-file.
- **Affected:** §5.2 census truthfulness in SUMMARY exclusionCensus / scan_skips.csv;
  the round-2 AMENDMENT_LOG claim (as worded); no test in the suite covers the ≥3-entry
  post-exhaustion case. No science corruption (tool is CANDIDATE_ONLY on synthetic inputs).
- **Required narrow correction:** in the pre-exhaustion branch, correct ALL remaining
  admitted sources' dispositions to OVER_BUDGET (they were admitted and read but not
  analyzed), pushing one skip row per payload (or one row listing them), instead of
  `break`ing after the first; add a regression test with ≥3 admitted entries and a
  mid-file shared-budget exhaustion.
- **Revalidation predicate:** a 4-entry container with a cap that exhausts at entry 1
  shows dispositions [SCANNED, OVER_BUDGET, OVER_BUDGET, OVER_BUDGET] with a skip row for
  every unanalyzed payload and `censusOk: true`.

## R2-1 (P3) — the claimed "pre-exhaustion skip" reservation refund is NOT implemented (prose/code drift in three locations)

- **File/lines:** `tools/placement_probe/placement_probe.mjs` line 110 (`refundPayload`
  docstring: "reservation released when a reserved payload is never scanned (parse failure /
  pre-exhaustion skip)"); the code calls `refundPayload` ONLY at lines 381 (READER_FAILURE)
  and 383 (PAYLOAD_SIZE_MISMATCH) — the pre-exhaustion skip branch (405-414) does NOT refund.
  Same claim replicated in `BUDGET_ACCOUNTING.json` notes ("refunded when the reserved
  payload is never scanned (read failure, size mismatch, pre-exhaustion skip)") and
  `AMENDMENT_LOG.md` ROUND 2 item 2.
- **Evidence (measured, probe P5):** B3 pre-exhaustion scenario (two raw inputs,
  `--budget-layout-evals 700`): `scannedBytes: 5152`, `syntheticInputs: 2` — both inputs
  charged; a refund would give 2576/1. The charge-standing behavior itself is defensible
  (the payload WAS read into memory; it matches round-1 QC's F3 revalidation gate
  "syntheticInputs: 2, scannedBytes: 5152") — but the documented semantic is false.
- **Required narrow correction:** either implement the refund in the pre-exhaustion branch
  (and adjust round-1-consistent expectations) or, better, correct the three prose
  locations to "refunded on read failure and declared-vs-actual size mismatch; a
  pre-exhaustion-skipped payload keeps its charge because its bytes were read".
- **Revalidation predicate:** probe P5 measured `scannedBytes`/`syntheticInputs` agree with
  the documented semantic (no prose/code divergence).

## R2-2 (P3) — bounded transient candidate-record copies remain outside the tracked peak (strictest "independent copies" reading of §8)

- **File/lines:** `tools/placement_probe/placement_probe.mjs` — rows push loop (419-433):
  each pushed row is a NEW object (`{ ...meta, ...normalizeCandidate(c), ... }`) while the
  original candidate objects stay alive in `rank`/`data.candidates` for the whole loop
  iteration (bounded overlap ≤ `top`, so ≤ cap+top ≈ 356 at default ceilings);
  CSV write-out (line 466, `csvRows = rows.map(x => ({ ...x, ... }))`) materializes a full
  independent copy of all rows while `rows` is alive (≤ 2×cap at serialization).
- **Evidence:** code reading (structures quoted); the TRACKED metric
  (`budgets.used.peakRetainedCandidates`) counts `externalRetained + per-call found` and
  is provably cap-bounded — measured 256/256 on 9- and 20-input probes (round-1: 261), and
  4/10/12 on the lowered-cap adversarial probes. The physical transient overlaps are NOT
  tracked.
- **Skutek:** the round-1 defect class (UNBOUNDED cross-file accumulation) is verifiably
  eliminated; the residual overlap is bounded (≤ top during push loops; ≤ cap at CSV write)
  and small. Whether §8's "niezależnych kopiach" wording obliges counting transient
  write-time copies is a semantic judgment; the honest reading is that the SCAN-loop
  enforcement now complies and the serialization overlap is bounded.
- **Required narrow correction (optional):** either count the write-time copy in a
  one-line note (documenting that CSV serialization transiently doubles the row set), or
  document the boundary explicitly in README §7 / BUDGET_ACCOUNTING notes.
- **Revalidation predicate:** none beyond the existing 9-input probe (this is a disclosure
  item, not a measured overshoot of the tracked metric).

## R2-3 (P3) — the B5 "two-input aggregation" regression test degenerates (input 2 is never opened)

- **File/lines:** `tools/placement_probe/tests/budget.test.mjs` lines 133-138 (B5 r3:
  `['a.vfs','b.vfs']` with `--budget-retained-candidates 4`); main-loop break at
  `placement_probe.mjs` line 462 (`if (rows.length >= budget.limits.retainedCandidates)
  { markExhausted(...); break; }`).
- **Contradicted claim:** the test comment "aggregation across TWO inputs: the GLOBAL peak
  (main rows + per-call lists) stays under the cap" and AMENDMENT_LOG item 1's "B5 extended
  with a two-input aggregation case (peak <= 4 across both inputs)".
- **Evidence (measured, probe P2):** at cap 4, input 1 alone exhausts the cap (found caps
  at 4, 4 rows pushed) and the main-loop break prevents input 2 from being opened AT ALL:
  `syntheticInputs: 1`, `scannedBytes: 2576`, `exclusionCensus.length: 1` (one census
  record; input 2 has no record). The test passes but would also pass WITHOUT the
  externalRetained fix (the per-blob check alone produces the same outcome) — it does not
  exercise cross-structure aggregation. The fix itself is real and proven by the 9/20-input
  default-ceiling probes (the 9th input's found list was capped at 24 by the 232 external
  rows).
- **Required narrow correction:** raise the r3 cap above one input's natural candidate
  count (e.g. 33 with two 29-candidate records80 inputs, so input 2 is analyzed with
  29 external rows bounding its found list) or assert on the 9-input style scenario.
- **Revalidation predicate:** r3 shows `syntheticInputs: 2` / two census records with the
  second input analyzed and its found list bounded by the first input's rows.

## R2-4 (P3) — containerReadBytes is charged for raw inputs that are refused before their read

- **File/lines:** `tools/placement_probe/placement_probe.mjs` line 350
  (`budget.containerReadBytes += size;` runs for every non-INPUT_TOO_LARGE input, BEFORE
  the raw-path admission refusal at line 393-395 which returns before `readFileSync`).
- **Contradicted claim:** README §7 / BUDGET_ACCOUNTING ("container-read bytes and
  control-work bytes are accounted separately from SCANNED_BYTES") — a reader naturally
  interprets containerReadBytes as bytes actually read.
- **Evidence (measured, probe P7):** two raw inputs (2576 B each), cap 2676 → input 1
  admitted+read, input 2 refused BEFORE read: `containerReadBytes: 5152` — the never-read
  second input's size was charged. The charge line predates ROUND 2, but the F2 fix (admission
  now before read) made it charge bytes that are never read. Bounded by maxInputMiB per
  refused input; the budgeted SCANNED_BYTES quantity is unaffected (2576 — correct).
- **Required narrow correction:** move the raw-path `containerReadBytes += size` to after
  successful admission (mirroring the container path, where the whole file IS read), or
  document the counter as "input bytes considered for scanning".
- **Revalidation predicate:** probe P7 measures `containerReadBytes === 2576` for the
  two-input refused case.

## R2-6 (P3) — AMENDMENT_LOG.md internal inconsistencies (stale header, contradictory ROUND 2 sections, guessed re-QC path)

- **File/lines:** `AMENDMENT_LOG.md` line 3 ("Rounds used: 1" — stale; two rounds were
  used); lines 19-20 ("## ROUND 2 — NOT USED / No further correction rounds were started.")
  immediately followed by lines 21-32 ("## ROUND 2 — defects detected by the FRESH INTERNAL
  QC and fixed (final allowed round)") — two contradictory ROUND 2 sections, apparently the
  pre-QC draft left in place when the real ROUND 2 was appended; line 33 predicts the re-QC
  record at "QC/QC_ROUND2_RECHECK" while the actual location per the dispatch instruction is
  `QC/ROUND2_RECHECK/` (this package).
- **Skutek:** provenance hygiene only — a reader of the log could conclude ROUND 2 was
  not used, or look for the re-QC record at a path that does not exist.
- **Required narrow correction:** delete/replace the stale "ROUND 2 — NOT USED" section,
  update "Rounds used" to 2, and point the re-QC reference at `QC/ROUND2_RECHECK/`
  (RECHECK_STATUS.json).
- **Revalidation predicate:** a single coherent ROUND 2 section; header counter matches
  the actual rounds used; the referenced record path exists.

---

## Verified-clean (explicitly checked, no finding)

- F1 enforcement verified by measurement: tracked peak 256 ≤ 256 on the round-1 9-input
  scenario (was 261) and on a 20-input stress; lowered-cap adversarial probes 4/10/12 all
  within cap; the 9th input's found list provably bounded by the 232 externally-held rows.
- F2 ordering verified in code and behavior: raw = statSync size → admitPayload →
  readFileSync; container = declared size → admitPayload → readEntry; refunds measured on
  READER_FAILURE/PAYLOAD_SIZE_MISMATCH (CX4 green, scannedBytes=0, syntheticInputs=0);
  refused raw inputs are never read and never charged SCANNED_BYTES.
- F3 corrected case verified by measurement (first post-exhaustion payload per file →
  OVER_BUDGET + skip row; B3 3001/701/4284 all re-measured; test messages now accurate).
- F4 row consistent (PASS from originalSevenNamesPass predicate; evidence cell matches).
- F5 message complete and byte-identical to the live error (107 bytes, ends ": 100001").
- F6 no dangling reference remains.
- F7 predicates sensitive (executed sabotage → 46 PASS / 1 FAIL); reproducible (47/0/0);
  CONTROL_PASS consciously replaced by in-predicate expected-rejection assertions —
  acceptable resolution, recorded as a disposition note, not a finding.
- F9: B1/B3/B2/B4 genuine two-input aggregation measured; B5 two-input test exists but is
  degenerate (R2-3).
- F10: CX1..CX4 all executed green (suite + POST + CORRECTION_MATRIX consistent).
- Standing science: NO violation introduced by ROUND 2 — only negative-control contexts
  exist; README invariants intact; MODEL_218757_TO_CMO_JOIN=NOT_ESTABLISHED,
  WORLD_XYZ_RECOVERED=NO preserved verbatim.
- POST artifacts were generated against the exact final bytes (code hashes match on-disk);
  original probe/cli-fixture test files byte-identical to the round-1 kit pins; PRE and
  round-1 QC records untouched by ROUND 2 (mtime evidence); HEAD still at BASE 3fbe93e...,
  only the two authorized untracked run paths present.

**Disposition note for the parent:** MAX_FIX_ROUNDS=2 is exhausted per BUDGET_ACCOUNTING
(`fixRoundsUsed: 2`). R2-5 (P2) and the P3 items are either (a) disclosed honestly in the
§11 FINAL_REPORT/INTERNAL_REVIEW as PARTIAL/KNOWN_LIMITATION material (consistent with the
AMENDMENT_LOG's own round-2 preamble), or (b) fixed under a separate parent-authorized
correction assignment. F8 must be re-verified at §11 (FINAL_REPORT.md must exist and contain
the standing-science block the FEATURE_COVERAGE_MATRIX row 14 cites).
