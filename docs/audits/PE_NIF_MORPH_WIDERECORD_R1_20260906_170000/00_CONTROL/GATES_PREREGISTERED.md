# GATES_PREREGISTERED.md - a-priori gates (CONTRACT.md Section 4 VERBATIM; fixed BEFORE any test execution; NEVER adjusted after seeing results)

## G-PINS

Every input pin verified in-driver before any parse (R61 10/10; Models.bnt; the RUN A artifacts; the K2 artifacts re-hashed from bytes). Mismatch = HARD STOP.

## G-CENSUS

The baseline reproduces EXACTLY (rr 2,427 / var 2,093 / nofit 334 = 62 alt + 272 none; unknown-325 = 325) AND the RUN A removals reproduce (H5a 39 + H5c2 26 FIT keys from the pinned RUN A artifacts) AND 334 - 65 = 269 exact. Mismatch = HARD STOP.

## G-WIDE (evaluated per grammar W1, W2, W3 separately; the PASS predicate is a conjunction - ALL components must hold)

PASS iff (full-269 fits >= 10) AND (full-269 positive rate >= 5x the matched-NC rate) AND (NC denominator > 0) AND (held-out side units >= 30) AND (held-out fits >= 10) AND (held-out rate >= 5x the held-out-side matched-NC rate).
THE VACUOUS CASE 0 >= 5x0 CANNOT PASS (NC denominator 0 => NC_EMPTY_DENOMINATOR). Report the exact binomial 95% CI for every rate (full and held-out, positive and NC).
NON-PASS classes: EMPTY_GROUP / ZERO_FITS / INSUFFICIENT_TRIALS(held-out units < 30) / NC_EMPTY_DENOMINATOR / NC_INSUFFICIENT_SEPARATION(<5x) / HETEROGENEOUS_SPLIT (the full-269 passes its rate test but the held-out side fails - report BOTH numbers).
A-PRIORI JUSTIFICATION (recorded, never adjusted): fits >= 10 so the rate is not a 1-2-span artifact; units >= 30 so the exact binomial CI is not degenerate; 5x = the K2/RUN A pre-registered separation standard; the held-out conjunction prevents full-population masking of file-level heterogeneity.

## Frozen operationalization decisions (fixed here, BEFORE any test execution)

d1. 'full-269' components are MEMBER-level (the 269 spans; 1 positive trial per span at the true start; NC denominator spans x 2 = 538). 'held-out side' components are UNIT-level (dp-sha units, RUN A machinery: dedup, first-member side, split families counted once; held-out = side B; NC denominator units x 2 on unit representatives). The contract text uses 'units' only for the held-out side; the full-269 unit-level numbers are ALSO computed and reported as transparency in WIDE_RESULTS.json (they do not enter the gate).
d2. '(NC denominator > 0)' is enforced for BOTH matched NC denominators (full-269 and held-out side); either being 0 => NC_EMPTY_DENOMINATOR (fail-closed).
d3. Deterministic non-pass classification order (first match wins; every branch is fail-closed): CORRUPTED_RECORD -> DUPLICATE_ACROSS_SIDES -> EMPTY_GROUP -> DENOMINATOR_MISMATCH -> NC_EMPTY_DENOMINATOR -> INSUFFICIENT_TRIALS (held-out units < 30) -> ZERO_FITS (full-269 fits < 10) -> NC_INSUFFICIENT_SEPARATION (full-269 rate < 5x full-269 NC rate) -> HETEROGENEOUS_SPLIT (held-out fits < 10 OR held-out rate < 5x held-out NC rate, with BOTH numbers reported).
d4. Every fit/NC count is a counter increment over an EXECUTED record (per-record validation only; deriving any validation count from a group size is FORBIDDEN).
d5. COVERAGE_DELTA.json: this run's validated additions X = the UNION of spans consumed by grammars whose G-WIDE verdict is PASS (consumed spans of non-pass grammars are recorded but EXCLUDED from X and from every coverage number - the K2 OC-rejection precedent). remaining no-fit = 269 - X.
d6. POST-HOC probes (if any) are labeled POST-HOC NON-COVERAGE and excluded from every number; this run executes NO post-hoc probe.
d7. The 2003-era corpus, H7, and the residual-325 are OUT OF SCOPE (no execution, no claims).

## G-EXEC

Every validation number computed by executing the predicate on a SPECIFIC record; per-record outcomes recorded (span ID, side, grammar, outcome, rejection reason, bytes consumed); deriving any validation count from a group size is FORBIDDEN. The driver must (a) self-audit: grep its own gate code for size-derived assignments and record the audit; (b) unit-test the gate with the EIGHT synthetic fixtures (each must produce an explicit non-pass): (1) zero successes both sides; (2) empty population; (3) only-previously-selected successes; (4) a duplicate present in both groups; (5) unequal denominators; (6) a corrupted record; (7) a malformed manifest row; (8) a missing input file. All eight fail-closed => G-EXEC PASS.

## G-SCOPE

Read-only originals; zero payloads; run-local tooling only in 00_CONTROL; this run's own artifact_index.csv written per MANIFEST_SCHEMA_SPEC.md and its self-validation gate PASSES (dogfooding).

Standing sentence: no semantic claims; the +65 H5a/H5c2 status = RETROSPECTIVE_VALIDATED (RUN A); the H7 join-mechanism = UNVALIDATED (RUN A) - this run makes NO H7-based claims; the residual-325 population is OUT OF SCOPE (stays mechanism-unexplained; a diagnostic note only, no new claims). Result classes: BYTE_MATCH / REPEATABILITY / RETROSPECTIVE_VALIDATION / RUNTIME_SEMANTICS (= explicitly NOT_TESTED here, out of scope).

