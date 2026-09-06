# NC_PROCEDURES.md - negative-control procedures (frozen BEFORE any test execution)

Seed discipline: deterministic (no sampling randomness needed; the wrong starts are pinned). Written to disk before any W1/W2/W3 test execution.

## NC-A (span level, full-269)

- For EVERY span of the 269 population and EVERY grammar (W1, W2, W3): 2 trials at the pinned wrong starts u+2 and u-2 (u = the walk start Wm-2).
- Trial hit = the SAME grammar executed at the wrong start: W1 -> K2.parse_fixed(dp, u2, N, 32) ok and recs>0; W2 -> K2.parse_variable(dp, u2, N, kmax=24) ok and recs>0; W3 -> the W3 window anchored at u2 (offsets u2+d, d in -64..+64 step 4) any-hit.
- Explicit denominator: spans x 2 = 269 x 2 = 538 per grammar. A trial with u2 < 0 is recorded as a NON-hit trial (reason INVALID_START_NONHIT) and stays in the denominator.
- Rate = hits / 538. Compared to the full-269 positive rate (1 trial per span at the true start) as rate-vs-rate ONLY; raw-count cross-population comparisons FORBIDDEN.

## NC-B (held-out side, unit level)

- Unit machinery (RUN A standard): unit = byte-identical dp payload (sha256), dedup within the 269 population; unit side = side of its FIRST member in sorted (file,bi,si) order; split families (a unit whose members land on both sides) are counted once, on the first-member side; held-out side = side B.
- For EVERY held-out-side unit (representative = the unit's first member): 2 trials at u_rep+2 and u_rep-2 with the same grammar semantics as NC-A. Explicit denominator: held-out units x 2.
- Rate = hits / (held-out units x 2), compared to the held-out unit positive rate (1 trial per unit) as rate-vs-rate ONLY.

## Vacuity guard

THE VACUOUS CASE 0 >= 5x0 CANNOT PASS: NC denominator 0 => NC_EMPTY_DENOMINATOR non-pass; zero positives => ZERO_FITS non-pass (checked BEFORE any separation comparison).

Standing sentence: no semantic claims; the +65 H5a/H5c2 status = RETROSPECTIVE_VALIDATED (RUN A); the H7 join-mechanism = UNVALIDATED (RUN A) - this run makes NO H7-based claims; the residual-325 population is OUT OF SCOPE (stays mechanism-unexplained; a diagnostic note only, no new claims). Result classes: BYTE_MATCH / REPEATABILITY / RETROSPECTIVE_VALIDATION / RUNTIME_SEMANTICS (= explicitly NOT_TESTED here, out of scope).

