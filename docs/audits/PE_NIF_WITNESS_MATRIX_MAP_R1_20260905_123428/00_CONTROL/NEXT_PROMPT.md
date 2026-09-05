# NEXT_PROMPT — proposed RUN-D: WITNESS FALSIFICATION EXECUTION (GATED)

> **GATE:** This next run requires EXPLICIT user authorization. The RUN-C MAP ONLY contract
> (no corrupted variant built or parsed) is the standing rule until a GO is given. Nothing in
> RUN-C authorizes execution.

---

You are agent pe-reconstruction executing RUN-D: the WITNESS FALSIFICATION EXECUTION for the NIF
corpus (offline; ZERO renders; no game code; no M2 advancement).

CONTEXT: RUN-C (PE_NIF_WITNESS_MATRIX_MAP_R1_20260905_123428) delivered the WITNESS MATRIX:
5 known-good witnesses + 3 mildly-wrong recipes + 3 severely-scrambled recipes, each with
machine-verified SHA256, exact byte/offset/before/after values, and predictions citing the exact
R61 code paths (05_ANALYSIS\WITNESS_MATRIX.json is the authority). The R61 frozen parser
(99_Audits\PE_R61_FROZEN_BASELINE_20260828\01_source\ — READ-ONLY, verify 10/10 hashes first)
achieves 5,596/5,596 (9.3.5) + 5,426/5,426 (2003) parse closure.

P0 (ONE question): do the 6 corrupted variants behave EXACTLY as the RUN-C matrix predicts —
(MILD-1) PASS via G3E boundary-search recovery with variant flip G3D→G3E; (MILD-2) PASS via
G9_RTTI fallback with variant flip TEXT_CRLF→G9_RTTI; (MILD-3) FAIL_CLOSED "u2=0x00000003 has no
P0-verified parser. FAIL CLOSED."; (SCRAMBLE-1) container ValueError before any parse;
(SCRAMBLE-2) FAIL_ERROR "header parse error: absurd string length 1766719488 at pos=51";
(SCRAMBLE-3) FAIL_CLOSED "non-zero block_preamble_u32=3735928559" at block 0 — with ZERO
divergence from the recorded expected_field_changes?

DELIVERABLE: FALSIFICATION_RESULTS.json + comparison table (predicted vs actual, per variant:
status, fail_reason exact-match, boundary method, variant field) in a NEW run dir.

SAFETY CONTRACT (hard):
- Build the 6 variants in a SANDBOX COPY only (e.g. temp dir): payload copies of 146709/424276/500078
  (single-byte corruptions at the RUN-C-recorded offsets) + a container-level copy for SCRAMBLE-1.
  NEVER modify Models.bnt, the 2003 extraction dir, the originals, or any source tree.
- Re-hash every variant (its SHA256 MUST differ from the raw witness — record both).
- The raw witnesses must still parse PASS before and after (control group).
- Identity metadata only in outputs; no payload redistribution.

GATES: (a) 10/10 R61 hash verification BEFORE any parse; (b) control group 5/5 PASS before and
after; (c) every variant result compared field-by-field against WITNESS_MATRIX.json predictions
with PASS=DIVERGENCE_FREE / FAIL=DIVERGENCE per variant; (d) any divergence is a LOUD finding
(parser or matrix must be corrected — no silent acceptance); (e) MILESTONE_PROGRESS vector.

OUTPUT: same audit structure (00_CONTROL driver + NEXT_PROMPT + SHA256_DRIVER.txt; 01_RAW
variant hashes + parse outputs; 05_ANALYSIS FALSIFICATION_RESULTS.json; 06_REPORT; REPORT.md
pointer; HANDOFF.md; STAGE_ACCEPTANCE_GATES.csv; artifact_index.csv REAL SHA-256). Publish to
docs/audits/<RUN-D id>/ with ONE path-limited commit (staged-index inspected; diff --cached
--stat = exactly your paths; push; remote verify). Standing rules: no payloads, jeden run =
jeden commit, no M2-advancement.
