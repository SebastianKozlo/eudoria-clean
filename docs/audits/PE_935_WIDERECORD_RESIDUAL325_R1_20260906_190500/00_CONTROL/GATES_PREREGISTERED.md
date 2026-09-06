# GATES_PREREGISTERED.md - a-priori gates (CONTRACT.md Section 4 VERBATIM; fixed BEFORE any test execution; NEVER adjusted after seeing results)

## G-PINS

All pins in-driver; mismatch = HARD STOP.

## G-CENSUS

The K2 baseline reproduces (rr 2,427 / var 2,093 / nofit 334; unknown-325 = 325 across 56 files; 551564.nif x84); mismatch = HARD STOP.

## G-WIDE325 (per grammar W1, W3 separately)

PASS iff (full-325 fits >= 5) AND (full-325 rate >= 5x the matched-NC rate) AND (NC denominator > 0). A-PRIORI JUSTIFICATION (recorded): fits >= 5 (not 10) because this is a LOW-PREVALECE probe of a heterogeneous fragment bucket - 5+ fits with >= 5x separation and exact CIs establish the class's existence; fewer than 5 = the class ABSENT/RARE (a valid bound, not a failure). Report the exact binomial CI for every rate. THE VACUOUS CASE 0 >= 5x0 CANNOT PASS.
NON-PASS classes: EMPTY_GROUP / ZERO_FITS(<5) / NC_EMPTY_DENOMINATOR / NC_INSUFFICIENT_SEPARATION(<5x).

## G-CONCENTRATION (the RUN C lesson)

The per-side/per-family fit distribution is ALWAYS reported; if ALL fits land on one split side or one file+block, the label CONCENTRATED is MANDATORY in every output (a disclosure class, not a gate failure by itself; the PASS stands only with the separation intact + the concentration disclosed).

## G-EXEC

Per-record outcomes only; zero size-derived validation numbers (the driver self-audit); the EIGHT negative fixtures fail-closed (the standard list): (1) zero successes both sides; (2) empty population; (3) only-previously-selected successes; (4) a duplicate present in both groups; (5) unequal denominators; (6) a corrupted record; (7) a malformed manifest row; (8) a missing input file.

## G-SCOPE

Read-only originals; zero payloads; run-local tooling only; the artifact_index per the spec + self-validation PASS.

## Frozen operationalization decisions (fixed here, BEFORE any test execution)

d1. 'full-325' components are MEMBER-level (the 325 spans; 1 positive trial per span at the true start; NC denominator spans x 2 = 650 per grammar). Per-side (A/B) fit/NC rates and per-(file,bi) fit distributions are TRANSPARENCY + G-CONCENTRATION disclosure inputs, never G-WIDE325 gate inputs (this contract has NO held-out conjunction).
d2. '(NC denominator > 0)' is enforced on the per-span matched-NC denominator (650); 0 => NC_EMPTY_DENOMINATOR (fail-closed). With fits >= 5 > 0 and NC hits 0 over a positive denominator, the >= 5x separation test is satisfied (5x0 = 0 <= rate); this is NOT the vacuous case (the vacuous case is fits 0 AND NC 0, which cannot pass - ZERO_FITS is checked first).
d3. Deterministic non-pass classification order (first match wins; every branch fail-closed): CORRUPTED_RECORD -> DUPLICATE_KEYS -> EMPTY_GROUP -> DENOMINATOR_MISMATCH -> NC_EMPTY_DENOMINATOR -> ZERO_FITS(<5) -> NC_INSUFFICIENT_SEPARATION(<5x).
d4. Every fit/NC count is a counter increment over an EXECUTED record (per-record validation only; deriving any validation count from a group size is FORBIDDEN).
d5. COVERAGE_DELTA.json: the 2,171/2,427 = 89.45% state stands (canon 2,093 + RUN A +65 RETROSPECTIVE_VALIDATED + RUN C +13 RETROSPECTIVE_VALIDATED with the family-concentration bounds); this run's additions X = the UNION of 325-spans consumed by grammars whose G-WIDE325 verdict is PASS, each labeled RETROSPECTIVE_VALIDATED (+ CONCENTRATED when d8 applies); the 325 -> 325 - X. Consumed spans of non-pass grammars are recorded but EXCLUDED from every coverage number (the K2 OC-rejection precedent).
d6. POST-HOC probes (if any) are labeled POST-HOC NON-COVERAGE and excluded from every number; this run executes NO post-hoc probe. ZERO_FITS is a VALID honest outcome - if the wide-record class is absent/rare in the 325 residual, that bound is reported plainly.
d7. W2 (RUN C), H7 mechanisms, the 2003-era corpus and the R61 parser internals are OUT OF SCOPE (no execution, no claims; H7 = UNVALIDATED, NO H7-based claims).
d8. G-CONCENTRATION: the per-side and per-(file,bi) fit distributions are ALWAYS reported; CONCENTRATED_SIDE (all fits on one split side) and CONCENTRATED_FAMILY (all fits on one file+block) labels are MANDATORY in every output when they hold; they are disclosure classes - a G-WIDE325 PASS stands only with the separation intact AND the concentration disclosed. Fixture 3's ONLY_PREVIOUSLY_SELECTED integrity guard: if every fitting member is flagged previously_selected=True the gate fails-closed (the real 325 members all carry previously_selected=False by population definition, so the guard is inert on real data).

Standing sentence: no semantic claims; the +65 (RUN A) = RETROSPECTIVE_VALIDATED; the +13 (RUN C) = RETROSPECTIVE_VALIDATED with the family-concentration bounds; the H7 join-mechanism = UNVALIDATED (RUN A) - NO H7-based claims; the residual-325 remains the heterogeneous bucket this run only PROBES. Result classes: BYTE_MATCH / REPEATABILITY / RETROSPECTIVE_VALIDATION / RUNTIME_SEMANTICS (= explicitly NOT_TESTED here, out of scope).

