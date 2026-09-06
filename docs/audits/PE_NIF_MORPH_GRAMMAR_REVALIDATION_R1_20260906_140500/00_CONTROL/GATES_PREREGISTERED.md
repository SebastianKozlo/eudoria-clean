# GATES_PREREGISTERED.md — a-priori gates (contract Section 5, VERBATIM) +
# executor interpretation decisions (recorded BEFORE any test execution;
# NEVER adjusted after seeing results)

Source contract: 00_CONTROL/CONTRACT.md (SHA256
02F32099AD7D9A528A6BC08C46E6C4F55C8218A06FBB482B5BE529E76DC34F95), Section 5.

Standing sentence: no semantic claims; class -256/field1 MEANING remains
unknown; the -256=>zero-entry association remains ONE-WAY. Result classes:
BYTE_MATCH / REPEATABILITY / RETROSPECTIVE_VALIDATION / ERA_TRANSFER_DIAGNOSTIC
/ RUNTIME_SEMANTICS (= explicitly NOT_TESTED here, out of scope).

## The gates, VERBATIM from the contract

- G-PINS: every input pin verified in-driver before any parse (R61 10/10; K2
  artifacts re-hashed from bytes; the 2003 corpus SHA recorded). PASS = all
  match. Mismatch = HARD STOP.
- G-CENSUS: the baseline census reproduces K2 EXACTLY (rr 2,427 / var 2,093 /
  nofit 334 = 62 alt + 272 none; unknown-325 = 325 across 56 files; 551564.nif
  x84). Mismatch = HARD STOP.
- G-RETRO (the 9.3.5 retrospective leg; evaluated per grammar H5a, H5c2, and
  the H7 join model separately): PASS iff (held-out independent trial units
  after family grouping >= 30) AND (held-out fits >= 10) AND (held-out positive
  rate >= 5x the matched-NC rate) AND (NC denominator > 0). A-PRIORI
  JUSTIFICATION (recorded with the contract, never adjusted): >=30 units so
  the exact binomial 95% CI of the held-out rate is not degenerate; >=10 fits
  so the rate is not a 1-2-span artifact; 5x = K2's own pre-registered
  separation standard. Report the exact binomial 95% CI for every rate. THE
  VACUOUS CASE 0 >= 5x0 CANNOT PASS (NC denominator 0 => NC_EMPTY_DENOMINATOR
  non-pass). NON-PASS classes: EMPTY_GROUP / ZERO_FITS / INSUFFICIENT_TRIALS
  (<30 units) / NC_EMPTY_DENOMINATOR / NC_INSUFFICIENT_SEPARATION (<5x).
- G-ERA (the 2003 leg): DIAGNOSTIC ONLY, no PASS/FAIL; outputs: fit counts,
  rates with exact binomial CIs, the prior-use verdict, the duplicate/family
  census; near-zero transfer = the finding CORPUS_SPECIFIC_935 (a valid
  outcome, not a failure). Explicitly NOT a substitute for 9.3.5-target
  correctness.
- G-EXEC: every validation/validation_exact number computed by executing the
  predicate on a SPECIFIC record; per-record outcomes recorded (span ID,
  side, grammar, outcome, rejection reason, bytes consumed); deriving any
  validation count from a group size is FORBIDDEN. The driver must (a)
  self-audit: grep its own gate code for size-derived assignments (patterns
  like "// 2" applied to a population count, len()-derived validation counts)
  and record the audit result; (b) unit-test the gate with EIGHT synthetic
  fixtures, EACH producing an explicit non-pass outcome: (1) zero successes
  both sides; (2) empty population; (3) only-previously-selected successes;
  (4) a duplicate present in both groups; (5) unequal denominators; (6) a
  corrupted record; (7) a malformed manifest row; (8) a missing input file.
  All eight fail-closed => G-EXEC PASS.
- G-SCOPE: read-only originals; zero payloads; run-local tooling only in
  00_CONTROL; this run's own artifact_index.csv written per RUN B's
  MANIFEST_SCHEMA_SPEC.md and its self-validation gate PASSES (dogfooding).

## A-PRIORI INTERPRETATION DECISIONS (executor, fixed before any test)

These decisions resolve ambiguities in the gate text. They are frozen HERE,
before the census-derived populations or any grammar result is known to the
executor, and are NEVER adjusted after seeing results.

1. UNIT (G-RETRO "independent trial units after family grouping"): the unit
   is the eligible span, with byte-identical dp payloads (sha256 of the span's
   dp bytes) collapsed to ONE unit within the population. "Family grouping"
   for units = this byte-identical payload dedup (the contract's family rule
   "byte-identical payloads = one family", Section 4, applied as dedup).
   Rationale: the matched NC is per-span ("NEVER one-per-file"), so the
   rate comparison is only coherent with span-level units; the binomial CI
   is over these units. The same-file family relation is additionally
   REPORTED (distinct-file counts) for transparency, and family integrity of
   the split is enforced (decision 3).
2. HELD-OUT SIDE: side B = the second half of the seeded file shuffle
   (decision 4). Both sides are evaluated; the gate evaluates side B.
3. SPLIT (contract Section 3, frozen): the split is ONE JOINT file-level
   50/50 over the sorted union of the files carrying the eligible
   populations (P1 = the 334 no-fit spans for H5a/H5c2; P2 = the 325 residual
   spans for H7). files = sorted(unique file names of P1 ∪ P2);
   rng = random.Random(20260906); shuffled = files.copy(); rng.shuffle(
   shuffled); side_A = shuffled[:n//2]; side_B = shuffled[n//2:]; FAMILY
   INTEGRITY: every span of a file lands on the side of its file. One joint
   split (not per-population splits) keeps family integrity global.
4. H5a/H5c2 NC rate = NC hits / (spans x 2) per NC_PROCEDURES.md NC-A;
   H7 NC rate = span-level (NC_PROCEDURES.md NC-B). The 5x comparison is
   rate-vs-rate on these explicit denominators.
5. Exact binomial 95% CI = the Clopper-Pearson exact interval (two-sided,
   alpha=0.05), computed by exact binomial tail inversion (pure Python,
   no scipy dependency); reported for every rate.
6. G-RETRO is evaluated per grammar (H5a, H5c2, H7) SEPARATELY, each on its
   own population's held-out units; the three verdicts are independent.
7. REPEATABILITY evidence (not a gate): the union of side A + side B
   per-record outcomes on the full populations must reproduce K2's pinned
   fit lists EXACTLY (H5a 39 fits; H5c2 26 fits; H7 join-explained of the
   325 = 74) because the grammars are deterministic and the populations are
   pinned; any mismatch is reported as a repeatability defect (and for the
   334-side populations also fails G-CENSUS's population identity).
8. The 2003 leg's independence unit for REPORTING (Section 4 FAMILY
   GROUPING) is the family: same file = one family; byte-identical payloads
   (cross-era AND within-era) = one family. The 2003 rates are reported
   per-span (deduped as in decision 1) AND per-family; the family count is
   reported as the independence unit. DIAGNOSTIC ONLY.
9. The canonical 2003 Models container resolution (input to G-PINS):
   01_Original_Files\BNT_Models\Models.bnt (5,426 entries, 5,426 unique .nif
   names — the contract's "5,426-name class" EXACTLY; full SHA256 recorded
   in-driver; matches PE-MASTER ground-truth pin 1322ADF2...). The
   contract's "~5,441 NIF" is the physical-LINE count of the pinned R12
   manifest CSV (5,442 lines incl. header) whose true CSV RECORD count is
   5,426 (verified with a standard CSV parser); the binding canon class is
   the 5,426-name class, which matches EXACTLY. The driver additionally
   byte-verifies all 5,426 container payloads against the prior-run
   extraction (M1B3 02_extraction\nif) to tie the container to the R12/R61/
   R35/era-drift prior evidence.
10. G-SCOPE "zero payloads": this run writes NO payload bytes and NO hex
    dumps; outputs carry only identifiers, outcomes, reasons and byte
    COUNTS (the K2 hex-cap dumps are re-hashed as pinned inputs but never
    copied or extended).
