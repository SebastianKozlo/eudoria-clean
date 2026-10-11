# placement_probe — PE935 placement candidate reconnaissance (correction R1)

Read-only recon tool that scans SYNTHETIC or verified inputs for fixed-stride record
layouts whose columns look like (template ID, X, Y, Z). **Every output is
CANDIDATE_ONLY_NOT_PLACEMENT_PROOF.** The tool never establishes a historical
placement, a world instance, or a model→instance join.

Correction R1 (run `PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011`) changed:

1. **Fail-closed configuration.** Every numeric option is validated (finiteness,
   integrality where required, legal zero for `maxHeader`/`minPosDistinct`/`top`,
   [0,1] for rates, `posLo < posHi` with negatives allowed, value required after
   every flag). Invalid configuration ⇒ `INVALID_CONFIGURATION` + nonzero exit +
   `SCAN_STARTED=NO` (no output directory is created). The exported `analyzeBlob`
   validates the same rules — importing it cannot bypass option checks. Legal
   boundary values (e.g. `--max-header 0`, negative `--pos-lo`) are protected by
   tests against over-rejection.
2. **Exclusion census.** Every declared archive entry receives exactly ONE
   disposition, in fixed order: `FILTERED_REGEX → FILTERED_EXTENSION →
   ENTRY_TOO_LARGE → TOO_SMALL → PARSE_FAILED → OVER_BUDGET → SCANNED`
   (`UNSUPPORTED` = container-level framing failure with NO invented entry count).
   `DECLARED_ENTRIES` must equal the disposition sum (`censusOk` in SUMMARY.json).
   Container / entry / payload / candidate-table counts are separate units.
3. **Layout accounting.** `LAYOUT_ATTEMPTS` counts every visited
   (source, header, stride) BEFORE the divisibility/minRows filters; the legacy
   post-filter `layoutsTested` field is kept (renamed nowhere) and
   `LAYOUTS_ADMITTED` is reported separately. A 10007-byte 0xFF buffer with
   strides 12..512 yields 126 attempts, 0 admitted — R1 reported `layoutsTested=0`,
   which would have charged a layout budget 0 for 126 visits.
4. **Sample vs census.** Candidates carry `TABLE_ROW_COUNT`, `SAMPLED_ROW_COUNT`,
   `SAMPLE_XYZ_FINITE_RATE` (joint complete-finite-triple rate over the sample),
   `FULL_CENSUS_ROW_COUNT`, `FULL_CENSUS_XYZ_FINITE_RATE`, `FULL_CENSUS_ID_RATE`
   and `CENSUS_STATUS` (`FULL_CENSUS` / `PARTIAL_BUDGET_EXHAUSTED` /
   `NOT_PERFORMED` never claimed as sample quality). `XYZ_FINITE_RATE` = rows with
   simultaneously finite X, Y and Z / examined rows; a zero denominator emits
   `null` (NOT_EVALUATED), never 0 or 1. The legacy `xyzRate` (mean of per-axis
   column in posLo..posHi rates) is preserved under its original name and meaning
   and is NOT renamed to the joint rate: in the canonical 80-row fixture the
   column mean is 0.9 while the joint triple rate is 56/80 = 0.7. Per-axis marginal
   rates, column means and posLo/posHi conformance have separate names and
   denominators.
5. **f32/u32 diagnostics.** Each candidate reports per-axis `finiteRate` (with
   explicit denominator), `nanCount`, `infinityCount`, `subnormalCount`, `zeroCount`,
   `magnitudeSummary` and `alternativeU32Interpretation` of the same bytes. u32
   counters read as subnormal f32 stay visible CANDIDATE_ONLY candidates — small or
   zero values are not treated as automatic errors, and no universal
   data-meaning classifier is implemented. Axis statistics and triple statistics
   are separate.
6. **One min-distinct-id interface.** The existing `--min-distinct-id 1` is kept
   (with regression tests) for single-definition tables; there is no second
   equivalent mechanism. The default 2 remains an explicit coverage restriction.
7. **Execution budgets** (per invocation, shared across ALL inputs/entries,
   no reset per payload): `SYNTHETIC_INPUTS ≤ 32` admitted payloads (raw files +
   unpacked entries; the 33rd admission attempt ends work before its scan),
   `SCANNED_BYTES ≤ 67108864` (reserved before payload read using the verified
   size; container-read bytes and control-work bytes are accounted separately),
   `LAYOUT_EVALUATIONS ≤ 100000`, `FULL_CENSUS_ROWS ≤ 50000` (re-examining a row
   for another finalist counts again), `RETAINED_CANDIDATES ≤ 256` (peak across
   all structures, not just the final top). Thresholds may be LOWERED per
   invocation (`--budget-*`), never raised. Exhaustion ⇒ `BUDGET_EXHAUSTED`,
   `COVERAGE=PARTIAL` — never NO_CANDIDATE.

## Limitations (explicit, by design of this correction scope)
- Fixed-stride search only; nested/variable-length records can alias.
- Sampling (`--max-sample-rows`, default 1200) drives discovery; full census is
  performed only for finalists and only within the census budget.
- Heuristic gates (`--min-pos-rate`, `--min-id-rate`, ...) are discovery filters,
  not validity oracles.
- `ids_from_export.mjs` accepts only `.bnt`/`.ark` model archives (a hypothetical
  `.dat` is rejected — a helper limitation, NOT a claim about any real archive)
  and counts only `<numeric>.nif` names toward `S_model`; non-numeric names are
  excluded and explicitly counted (`nonNumericNamesExcluded`).
- NOT implemented / NOT_CHECKED (out of correction scope): variable-stride
  records, quaternion/rotation decoding, georeferencing, any Gamebryo runtime
  research, any original-game payload scanning for placement.

## Standing science invariants (unchanged by this tool)
`MODEL_218757_TO_CMO_JOIN=NOT_ESTABLISHED`, `WORLD_INSTANCE_IDENTITY=NOT_ESTABLISHED`,
`HISTORICAL_PLACEMENT=NOT_ESTABLISHED`, `WORLD_XYZ_RECOVERED=NO`. The 4057→218757
relation stays a definition/resource relation, not a world instance. No candidate
produced by this tool may be cited as a placement, world coordinate, or instance
join. Historical PCG Models.bnt inventory: 5596 `<id>.nif` names incl. `218757.nif`
(earlier measurement; not re-opened by this run).