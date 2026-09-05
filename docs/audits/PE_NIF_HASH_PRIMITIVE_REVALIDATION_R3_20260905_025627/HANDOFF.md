# HANDOFF — PE-NIF-HASH-PRIMITIVE-REVALIDATION-R3

For: the master auditor / human / independent post-auditor (ChatGPT).
This bounded revalidation run is COMPLETE and HARD-STOPPED. Nothing outside the
run dir and the single authorized publication path was written. The next stage
was NOT auto-continued.

## What exists now (all paths under
## D:\Eudoria_Reconstruction\99_Audits\PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627\)

- 00_CONTROL\ — NEXT_PROMPT.md (formalized direction), EXTERNAL_REVIEW.md (the
  FULL external post-audit + correction direction persisted verbatim with
  recomputed hashes), r3_primitives.py (corrected primitives: RFC1950 adler
  s1=1/s2=0 mod 65521; RFC9923 fnv exact multiply mod 2^32; wrong-value and
  three-state controls), run_kats.py (executable KAT runner, exit-code
  enforced), probe_r2_helpers.cjs (executes ONLY the literal declarations
  extracted from the HASH-PINNED R2 source in a pure vm context; the historical
  R2 script is NOT executed), revalidate_r3.py (main driver: enforced
  KAT-before-aggregation ordering, per-entry identity + value census, census
  recount, historical re-sums, sidecar analysis, three-state gates),
  emit_r3_analysis.py + emit_r3_outputs.py (generators; supersession quotes
  verified present).
- 01_RAW\ — PRIMITIVE_VALUE_COMPARISON.json (identity pass + COMPLETE
  R2-vs-corrected per-entry mismatch census keyed by era+file+candidate),
  CENSUS_RECOUNT_R3.json (nine-zero + CRC subset, 20/20 R2/R36 agreement),
  R2_HELPER_PROBE.json (executed R2 literal values over KATs + full corpus),
  R34_RESUM.json (334/62/272 + 3 counterexamples), R35_CLAIM_TABLE_PRESERVED.json
  (21 claims, 19/2, C-MORPH-1 partial fit), R2_STATE_RESUM.json (actual R2
  tally 16/8; HR-1..4 false/FAIL evidence), SIDECAR_BARE_CR_ANALYSIS.json
  (12/12 + R39 dual-policy), PRIMITIVE_VALUE_CENSUS_FULL.json (LOCAL-ONLY full
  per-entry census — excluded from the published package, SHA256 in the
  manifest).
- 02_LOGS\ — TEST_RESULTS.json (23 executable gates PASS, 4 HR gates PENDING
  with pass=null; OVERALL distinct from human acceptance), kat_*.json (six KAT
  sets with ACTUAL exit codes: corrected/oracle exit 0; R2-literal/wrong-value/
  R2-coercion exit 1), LOGS.md (command log).
- 03_STATIC\SOURCE_QUOTES.md — 16 quote blocks with file+SHA (R2 helper
  declarations, gate serialization, R2G8/R2G13, R36 primitives, R34
  counterexamples, R35 rows, external post-audit, prompt, R39 raw bytes).
- 04_RUNTIME\NOT_RUN.md.
- 05_ANALYSIS\ — CLAIM_MATRIX.csv (15 claims; tally derived from actual rows:
  CONFIRMED 14, REJECTED-as-worded 1), FINDING_DISPOSITIONS.csv (F1, F2, F2b,
  F3, F5, N1, N2), SUPERSESSION_MAP.csv (S-01..S-12, every quote verified
  present in its pinned R2 artifact at emit time).
- 06_REPORT\ — 00_FINAL_REPORT.md (authoritative) + PROPOSED_DOC_CORRECTIONS_R3.md
  (PROPOSALS ONLY: P1R2-5-R3, P2R2-2-R3, P3R3 method-provenance ledger, P4R3
  three-state policy, P5R3 bare-CR policy).
- REPORT.md (pointer), STAGE_ACCEPTANCE_GATES.csv (generated from
  TEST_RESULTS.json; three-state), artifact_index.csv (real SHA256; documented
  exclusions: itself + the final gate output; the local-only full census marked
  LOCAL_ONLY).

## Key revalidation results (short)

1. Defect REPRODUCED from actual executed bytes (not auditor assertion):
   adler32("")=0x00010000 (correct 1); adler32("a")=0x00620061 (correct
   0x00620062); fnv1a("hello")=0xa82fb4a1 (correct 0x4f9f2cab); root causes:
   adler roles/initials misassigned; fnv float64 multiply. R2 crc32 was NOT
   defective (defect census bounded).
2. Per-entry VALUE comparison (11,022 entries, both hash-pinned corpora):
   adler(name) 11,022/11,022 mismatches; adler(payload) 11,022/11,022 (first
   complete per-payload census); fnv(name) 11,016/11,022 (6 coincidences
   identified); all crc32 candidates 0 mismatches. Identity pass first
   (four independent implementations per input class), aggregates only after.
3. P0 demonstrated: deliberately wrong-value primitives FAIL the KATs (exit 1)
   while PRESERVING the aggregate zero-match census on the full corpora —
   aggregate-only acceptance cannot detect value errors.
4. Physical result UNCHANGED (nine exact-zero + crc32(payload) 3,435/5,596 and
   3,299/5,426; c==CRC 11,022/11,022; 20/20 agreement with R2 aggregates and
   R36 historical). Superseded: R2G8/C2-B/C2-E method assurances and
   report/handoff wording (S-03..S-08). History NOT rewritten.
5. R34 re-sum: 334 = VARIABLE-K residual (62 another recorded fit / 272 none);
   counterexamples recorded; no promotion. R35: 19 ERA-STABLE + 2 EVOLVED;
   C-MORPH-1 partial fit (86.2%/81.0%) — no all-21-at-100% claim.
6. Three-state preserved (PENDING ≠ FAIL ≠ PASS through function/JSON/CSV/
   report); R2's bool(None)→false/FAIL detected; actual R2 tally 16/8 vs the
   stale 17/7 label; R3 labels derived from actual rows.
7. 12/12 sidecars byte-lossless re-verified; bare-CR policy explicit (custom
   line contract: "n/a\r" == sidecar mapping, 0 errors; CSV record semantics:
   "n/a" — interpretive difference, NOT byte loss; no migration).

## Publication outcome

The package is published (byte-identical, explicit-path staging only) at
docs/audits/PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627/ in
SebastianKozlo/eudoria-clean (master). BASE_SHA (run start) =
f37ba25468a39d9c89c7b01e106fab3215db7e4c; the package-publication HEAD_SHA and
PUSH_STATUS are reported in the final chat handoff (a commit cannot embed its
own hash). The unrelated untracked
docs/audits/PE_MILESTONE_1_WORLD_SURFACE_R1_GATE/ was NOT added, removed or
changed. No original payload is published; the original corpora are
represented by era/build + local path + size + SHA256 + reproduction method.
If any step had failed safely, the status would be EXTERNAL_AUDIT_INCOMPLETE
with the exact blocker (see the final chat handoff for the actual outcome).

## Next steps (for the human/master auditor to decide — NOT auto-executed)

1. Independent post-audit of THIS package (standing rule before any canon
   update or proposal application).
2. On acceptance: an authorized applier applies the R3 proposals
   (06_REPORT\PROPOSED_DOC_CORRECTIONS_R3.md: P1R2-5-R3, P2R2-2-R3, P3R3,
   P4R3, P5R3) to docs/nif + the correction ledger.
3. Still out of scope until separately authorized: any new morph-boundary
   research, per-payload value investigations beyond this census, wiki edits,
   milestone progression.

## FINAL HANDOFF BLOCK

AUDIT_OUTPUT_ROOT = D:\Eudoria_Reconstruction\99_Audits\PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627
FINAL_REPORT_PATH = D:\Eudoria_Reconstruction\99_Audits\PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627\06_REPORT\00_FINAL_REPORT.md
PRIMARY_EVIDENCE_PATHS = D:\Eudoria_Reconstruction\99_Audits\PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627\01_RAW\PRIMITIVE_VALUE_COMPARISON.json; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627\02_LOGS\TEST_RESULTS.json; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627\05_ANALYSIS\CLAIM_MATRIX.csv
RUN_STATUS = COMPLETED (bounded revalidation package + internal regression + safe publication)
HARD_STOP_REASON = corrected published package + handoff complete; all corrections remain
PROPOSALS pending independent post-audit; no wiki application; no milestone
advancement; no next stage auto-continuation.
