# NC_PROCEDURES.md — frozen negative-control procedures
(PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500; written BEFORE any test
execution; seeded; NEVER one-per-file; every comparison rate-vs-rate on explicit
denominators; raw-count cross-population comparisons FORBIDDEN.)

Standing sentence: no semantic claims; class -256/field1 MEANING remains
unknown; the -256=>zero-entry association remains ONE-WAY. Result classes:
BYTE_MATCH / REPEATABILITY / RETROSPECTIVE_VALIDATION / ERA_TRANSFER_DIAGNOSTIC
/ RUNTIME_SEMANTICS (= explicitly NOT_TESTED here, out of scope).

## NC-A (H5a and H5c2, retro and era legs)

Per-span trials at the PINNED WRONG STARTS u+2 and u-2 (2 trials per span;
denominator = spans x 2). Positives = 1 trial per span at the true start u.

- The NC hit predicate is K2's `nc2` VERBATIM semantics: for H5c2, execute
  `parse_variable(dp, u2, N, idx_limit=0x8000)`; for H5a, execute
  `parse_variable_trunctail(dp, u2, N)` and take its first four outputs
  `(ok, recs, k_hist, idxs)` exactly as K2's `nc2` does
  (`parse_variable_trunctail(r["dp"], u2, r["N"])[:4]`); a trial HITS iff
  `ok and recs > 0` (K2 `nc2` line: `if out[0] and out[1] > 0`).
- u2 = u+2 and u2 = u-2 are both executed for EVERY span. If u2 < 0 (not
  expected for these populations), the trial is recorded
  outcome=INVALID_START_NONHIT and STILL COUNTS in the denominator (fail-closed).
- NC rate = NC hits / (spans x 2) — an explicit denominator, reported with it.
- Positive rate = fitting spans / spans (1 true-start trial per span).
- The positive and NC executions run on the SAME side of the file-level split
  (the held-out side for the gate; the in-sample side recorded for
  transparency). No other NC structure is used.

## NC-B (H7 adjacency-join, retro and era legs)

Per-span non-adjacent joins sampled PER SPAN (matching the <=2 adjacency trials
per span) — NEVER one-per-file.

- Adjacency trials per span r (population = the residual-unknown spans):
  prev-trial exists iff si > 0 (H7a structure: `spans[si-1][2:] + r.s`);
  next-trial exists iff si+1 < len(spans) (H7b structure: `r.dp + spans[si+1]`).
- NC mirror, per existing adjacency trial: sample ONE non-adjacent partner o
  from the same file's population spans with `abs(si_o - si_r) > 2` (K2 NC3's
  non-adjacency definition), and execute the mirroring join:
  prev-style NC: `greedy_r18(o.dp + r.s, Wm)`; next-style NC:
  `greedy_r18(r.dp + o.s, Wm)`.
- Sampling RNG: `random.Random(20260906)` instantiated at the start of each
  leg's NC-B phase; spans consumed in SORTED (file, bi, si) order;
  `rng.choice(eligible_partners)` per trial. Deterministic given the pinned
  corpus and population.
- If a span has an adjacency trial but no eligible non-adjacent partner in the
  same file, that NC trial is recorded outcome=NC_NO_PARTNER, is a NON-HIT, and
  the span is excluded from the NC denominator (recorded; the positive
  denominator is unaffected; both denominators always reported explicitly).
- NC span-level rate = spans with >=1 NC-trial hit / spans with >=1 NC trial.
- NC trial-level rate = NC hits / NC trials executed (also reported).
- Positive span-level rate = join-explained spans / spans (a span is
  join-explained iff its H7a or H7b adjacency trial walks clean under
  VERBATIM `greedy_r18`).
- The G-RETRO 5x comparison for H7 uses span-level positive rate vs span-level
  NC rate (both "any of <=2 joins succeeds" structures, explicit denominators);
  trial-level rates are reported alongside for transparency.

## Denominator discipline

Every rate is stored next to its numerator and denominator in the outputs
(01_RAW trial records + 05_ANALYSIS JSONs). Any comparison across populations
in raw counts is FORBIDDEN; only rate-vs-rate on explicit, same-structure
denominators is performed. The vacuous case 0 >= 5x0 CANNOT pass (NC
denominator 0 => NC_EMPTY_DENOMINATOR non-pass).
