# PE_MASTER_REVIEW ADDENDUM R1 — PE_NIF_935_SEMANTIC_CORRELATIONS_R1_20260906_041200 (2d48831)
Issued: 2026-09-06, PE-MASTER loop bd17344b-a054-4cf4-be8d-5f0b250e8509, run PE_NIF_LADDER_CORRECTIONS_R1_20260906_134500 (post-audit PE_NIF_LADDER_POSTAUDIT_R1_20260906; findings F2/F6 adjudicated ACCEPTED).
AUTHORITY_STATUS = ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT = NONE.
This addendum supersedes IN PART the original PE_MASTER_REVIEW.md of this run. The original review file is preserved byte-identical; this is an addition, not a modification.

SUPERSEDED (review-layer claims):
1. BASIS(3) sentence "the probe's 1,796 v10 zero-entry + 33 v4 zero-entry = 1,829 EXACTLY" — the partition is WRONG. Correct partition (PE-MASTER re-derivation from PROBE2_RAW.csv + ARKTEXTURE_ID_TABLE.csv): 1,796 v10 (class -256) + 26 v10 (class 1) + 7 v4 = 1,829 = 5,596 - 3,767. The sum stands; the labels do not.
2. The claim "the classes partition entry-bearing vs zero-entry" — RETRACTED. ONE-WAY implication only: class -256 => zero entries (1,796/1,796); the converse is FALSE (26 class-1 zero-entry files exist — disclosed by the executor report Section 5 and present in PROBE2_CONTINGENCY.json B1_entry_count row0 = [26, 1313, 737, 462, 504]; the descriptives histogram is top-N truncated and omits them).
3. The MASTER_ACCEPTED verdict was graded while the review's own COVERAGE declared the raw event/viewport bytes NOT_CHECKED — improper grading (post-audit F6).

STANDING (unchanged): the run's science at OBSERVED level (all 33 tests with 10,000-label permutation controls; the standing no-semantic-proof sentence); the one-way association class -256 => zero entries; the class MEANING remains unknown (runtime-gated); PROBE-1/3/4 observations. Wiki HOLD stands.
Executor limitation-disclosure is NOT proof that the executor's predicates were correct.
