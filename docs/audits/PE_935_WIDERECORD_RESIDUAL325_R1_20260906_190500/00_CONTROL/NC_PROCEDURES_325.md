# NC_PROCEDURES_325.md - negative-control procedures (frozen BEFORE any test execution)

Seed discipline: deterministic (no sampling randomness needed; the wrong starts are pinned). Written to disk before any W1/W3 test execution.

## NC-A (span level, full-325)

- For EVERY span of the 325 population and EVERY grammar (W1, W3): 2 trials at the pinned wrong starts u+2 and u-2 (u = the walk start Wm-2).
- Trial hit = the SAME grammar executed at the wrong start: W1 -> K2.parse_fixed(dp, u2, N, 32) ok and recs>0; W3 -> the W3 window anchored at u2 (offsets u2+d, d in -64..+64 step 4) any-hit.
- Explicit denominator: spans x 2 = 325 x 2 = 650 per grammar. A trial with u2 < 0 is recorded as a NON-hit trial (reason INVALID_START_NONHIT) and stays in the denominator.
- Rate = hits / 650. Compared to the full-325 positive rate (1 trial per span at the true start) as rate-vs-rate ONLY; raw-count cross-population comparisons FORBIDDEN.
- Per-side (A/B) NC rates are computed and reported as TRANSPARENCY + G-CONCENTRATION disclosure inputs only (never gate inputs).

## Vacuity guard

THE VACUOUS CASE 0 >= 5x0 CANNOT PASS: NC denominator 0 => NC_EMPTY_DENOMINATOR non-pass; fewer than 5 fits => ZERO_FITS(<5) non-pass (checked BEFORE any separation comparison).

Standing sentence: no semantic claims; the +65 (RUN A) = RETROSPECTIVE_VALIDATED; the +13 (RUN C) = RETROSPECTIVE_VALIDATED with the family-concentration bounds; the H7 join-mechanism = UNVALIDATED (RUN A) - NO H7-based claims; the residual-325 remains the heterogeneous bucket this run only PROBES. Result classes: BYTE_MATCH / REPEATABILITY / RETROSPECTIVE_VALIDATION / RUNTIME_SEMANTICS (= explicitly NOT_TESTED here, out of scope).

