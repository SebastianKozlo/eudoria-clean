QC_COUNTERCHECK_V2 EXECUTION ATTEMPT LOG (authentic negative evidence, per residual contract par. 6)

ATTEMPT 1 (pre-execution identity gate):
  The very first execution of qc_countercheck_v2.py exited with
  "BLOCKED: historical PROVENANCE checker identity mismatch: size 12749
  (expected 12749), sha F58D2DB36106006BA2CBF931DC9CFED872E9C5E22C5484E86462568B985AB7E8
  (expected F58D2DB36106006BA2CBF931DC9CFED872E9C5E2C5484E86462568B985AB7E8)".
  CAUSE: a 63-character transcription typo in THIS QC TOOL's OWN pinned
  constant (one '2' dropped from the historical checker SHA256) — the same
  defect class the historical SOURCE_RUN QC disclosed for its own constant.
  The fail-closed verify_pin caught it BEFORE any execution/evidence write;
  NO raw output was written. The constant was corrected in-place (the
  correction is disclosed in a source comment at the constant).

ATTEMPT 2 (crash after the duties, before the raw dump):
  NameError: name 'v2' is not defined (line ~1284, identity-oracle census)
  — the oracle census used 'v2.count' instead of 'v2_src.count'. All
  duty computations up to the P3 replay had executed, but the raw output
  file QC_COUNTERCHECK_V2_RAW.json had NOT been written (the crash
  preceded the dump); only the deterministic scratch fixtures
  (QC_CLEAN_copy.json, QC_W1_wrong_callsite.json, QC_W2_wrong_record_id.json,
  QC_W3_generality_callsite.json) had been written under
  00_CONTROL_INTERNAL_QC/scratch/ (deterministic content, byte-identical on
  every re-run). Fixed in-place; attempt 3 below is the completed run.

ATTEMPT 3: the COMPLETED run (this is the run whose raw output is
  00_CONTROL_INTERNAL_QC/QC_COUNTERCHECK_V2_RAW.json).

BOTH fixes are QC self-tooling fixes within QC_REPAIR_ROUNDS_MAX=1
(treated as one repair round of THIS QC's own tooling; both were made
BEFORE the first completed evidence-producing execution; neither touched
any executor artifact; both are disclosed in the QC_REPORT.md).
