# POSTAUDIT_NOTICE — PE_935_PAIR_REDUCER_CONSUMER_SAVED_R2_20261019

This run was subsequently subjected to an independent deep postaudit:
PE_935_PAIR_REDUCER_CONSUMER_DEEP_POSTAUDIT_R1_20261019 (published in this repository),
verdict REQUIRE_CORRECTIONS / science PARTIAL_PASS_WITH_MATERIAL_CORRECTIONS.
Its 16 QC-level findings (15 ACCEPTED_FINDING + 1 PARTIALLY_ACCEPTED) and the two
publication-manifest defects are recorded additively in PUBLICATION_REVALIDATION_R1.md
in this directory and in the postaudit's own projection. The qualified run's scientific
core (adapter/return-origin/visible compaction, bounded to its admissions) is preserved;
the following standing corrections apply when citing this run:
- 006C2A63 is CALL EAX (statically resolved 00823C10 on the documented caller path), not E8.
- Consumer erases the opaque-selected position and zeroes strictly after it; whole-range
  remove-zero and first-chronological-use are NOT proven.
- 004D1430 is not proven a constructor; opaque effects remain UNKNOWN.
- 14 body reservations are not 14 distinct functions; budgets 449 rows/39 CALL/12 candidates confirmed.
- LINK30 proves a construction path, not universal field preservation (R3: 620 POSSIBLE aliases).
- No world-instance join, no historical placement: WORLD_XYZ_RECOVERED=NO,
  HISTORICAL_PLACEMENT=NOT_ESTABLISHED, CURSOR_SOURCE_MEDIUM=UNKNOWN.