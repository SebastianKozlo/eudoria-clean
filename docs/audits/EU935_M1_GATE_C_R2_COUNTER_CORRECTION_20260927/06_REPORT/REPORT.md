# R2 COUNTER CORRECTION — FINAL REPORT

RUN_ID: EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927
MILESTONE: EU935-M1 (World Surface Fidelity); TARGET ERA: PCG_9_3_5
RUN_CLASS: LOAD_BEARING; RUN_TYPE: GATE_C_R2_BOUNDED_COUNTER_CORRECTION
EXECUTOR: pe-reconstruction (PE-MASTER-dispatched; NO_NESTED_TASKS; STATIC-ONLY
— the client never ran; no GPU; no new corpus; no new RE beyond the bounded
reproductions defined in the contract)
DATE: 2026-09-27. Report contract: PROJECT_OPERATING_MODEL.md section 15
(20 points), applied to this bounded correction run.

## 1. HUMAN DECISION BLOCK (what needs the human NOW)

- NOTHING for this bounded run itself: all three Desktop R2 findings were
  independently reproduced, and all three authorized corrections were applied
  byte-safely with full before-image preservation. No correction was forced;
  no evidence contradicted a Desktop finding.
- The persistence of this package + the predecessor R1 package is a LATER,
  separate phase (another worker) — the human-authorized Commit 1. This run
  performed NO git add/commit/push; HEAD remains cc747df.
- Human-gated items unchanged: Q1 (PE-MASTER qualification) NOT executed;
  Gate C remains REQUIRES_INDEPENDENT_DESKTOP_REAUDIT; M1 = OPEN; M2 = NOT
  AUTHORIZED; Viewer = NOT AUTHORIZED. This run claims NO Gate C PASS and NO
  MILESTONE_POST_AUDIT_PASS.

## 2. STATE DELTA (before -> after)

- BEFORE: F03:102 carried the wrong sample total ("1,664,000 samples");
  EVIDENCE_INDEX line 10 mislabeled the PEFoliageCore diff "comment-only";
  the R1 manifest carried the pre-edit hashes; the entrypoint had 1 uncommitted
  row (R1); the bad review equation lived only in a chat relay.
- AFTER: F03:102 states 53,166,080 u16 SAMPLE SLOTS across the 51,920 regular
  32x32 tile blocks (both arithmetic paths + the explicit NOT-list +
  attribution; BRIDGE_STATUS = UNKNOWN preserved); EVIDENCE_INDEX line 10
  states the true patch class (comments + ONE metadata string); the R1
  manifest rows for the two edited files carry the fresh post-edit hashes;
  the entrypoint has 2 uncommitted rows (R2 on top, R1 beneath — all
  historical rows byte-preserved); the review-equation erratum is documented
  in this package (no repo file ever contained it — 0/2,594 tracked files).
- GIT: HEAD cc747df before AND after (no commits); tracked modified = the
  same 3 files (numstat AUDIT_ENTRYPOINT.md 2/0, VegetationClimateDecoder.js
  30/6, PEFoliageCore.js 20/5); staged = NONE; untracked roots = R1 package
  (49 files) + THIS R2 package + the two DO-NOT-TOUCH roots.

## 3. METHOD (what this run did)

1. S0 fail-closed state pin: contract SHA re-verified (MATCH); HEAD =
   origin/master = cc747df; worktree shape exactly as pinned; ALL 8 hash
   pins re-verified MATCH; the two frozen sources verified byte-identical to
   BASE+patch (raw live git diff buffers hash 27DEE198.../5978FF6B...).
   Deviation recorded: the live github.com fetch failed (no connectivity);
   the local tracking ref matched the pin; no fetch/push/pull was attempted.
2. Phase 1 independent reproduction (before any edit; scripts write only into
   this package): R2-F01 fresh READ-ONLY BNT2 census of terrain.bnt;
   R2-F02 machine recomputation + per-file re-derivation + repo search;
   R2-P3 patch-class verification + mislabel confirmation + 41-hit bounded
   scan. ALL THREE FINDINGS REPRODUCED.
3. Phase 2 before-image preservation: byte-exact binary copies of all three
   EDIT TARGETS (BYTE_IDENTITY = YES x 3, hash + size + full byte-compare).
4. Phase 3 the three authorized predecessor edits: EDIT A (F03 line 102, 1
   removed + 11 added, everything else byte-preserved), EDIT B (EVIDENCE_INDEX
   line 10 description field, 1/1, one line 5 fields), EDIT C (manifest rows
   of the two edited files, 2/2, order/header/self-exclusion preserved).
   Exact unified diffs: 03_EVIDENCE/EDIT_{A,B,C}_*.diff; structural span
   checks ALL pass.
5. Phase 4 the entrypoint row: ONE row inserted at the top of the LATEST
   RUNS table; numstat 2/0; the vs-HEAD diff contains ONLY the 2 added rows;
   zero deletions; all historical rows byte-preserved.
6. Phase 5 this package (control/raw/analysis/evidence/report) with the
   verbatim contract, source index, baseline pin, findings/edges CSVs, the
   four analyses (F01/F02/P3 + blast radius + self-adversarial pass), the
   evidence JSONs/diffs/scripts, and this report.

## 4. PER-FINDING RESULTS (full records: 01_RAW/FINDINGS.csv; analyses: 02_ANALYSIS/)

- R2-F01 (F03:102 sample counter): REPRODUCED. Census from the pinned
  terrain.bnt (95841761...): 58,451 total / 51,920 regular (x: 220 contiguous
  0..219; y: 236 contiguous 0..235) / 6,530 special / 1 sentinel / 0
  duplicates; index consumed exactly. Both arithmetic paths machine-executed:
  51,920 x 1,024 = 53,166,080 and (220x32) x (236x32) = 7,040 x 7,552 =
  53,166,080. Falsifier: 51,920 x 32 = 1,661,440 != 1,664,000 (the old total
  underivable). EDIT A applied; SAFE SEMANTIC = SAMPLE SLOTS with the
  explicit NOT-list; BRIDGE_STATUS = UNKNOWN preserved byte-identical.
- R2-F02 (VCL review-arithmetic erratum): REPRODUCED. Bad LHS 491x12 + 24 +
  252 = 6,168 != 5,916. Correct relations both machine-verified:
  (491+1+1)x12 = 5,916 (group-level: 491 numeric lines + 1 continuation extra
  group + 1 comma group = 493 groups) and 472x12+252 = 5,916 (file-level);
  493-21 = 472. Double-count decomposition exact: 240 (25.vcl's 20 numeric
  lines x 12, already inside 491x12) + 12 (the continuation line's FIRST
  group, already inside 491x12) = 252 = 6,168 - 5,916. Raw census
  492/5,916/493/472 UNCHANGED and valid (re-summed from per_file rows; the
  totals block not trusted; log cross-check 472). Repo search: 0 hits over
  all 2,594 tracked files — the defect existed only in the human-pasted chat
  relay. Search timing: Phase 1 (pre-edit worktree, 133,463,531 bytes; the
  R2 entrypoint row and this package's own records did not yet exist);
  post-run, the equation string appears only in this run's own
  quoted-as-false correction records — this package's own records and the
  new AUDIT_ENTRYPOINT.md R2 row — no repo file asserts it. NO repo edit was
  required for this edge (erratum record only).
- R2-P3 (evidence label): REPRODUCED. Patch class verified from the frozen
  bytes + the fresh live diff (byte-identical, 27DEE198...): 4+19 comment
  lines + exactly ONE documentation-metadata string
  (FOLIAGE_OPERAND_LOCK.exactness); no arithmetic/parser/control-flow/
  placement change; zero runtime consumers of the operandLock metadata in
  src/. EVIDENCE_INDEX line 10 was the ONLY live UNDISCLOSED mislabel; EDIT B
  applied. Bounded scan (49 R1 files, 41 hits): 1 mislabel (fixed), 1
  imprecise residue OUTSIDE the authorized edit set
  (F05_EXACTNESS_ORIGIN_PRECISION.md:87 — recorded as open residue, NOT
  edited), the rest VCD-scoped-accurate / already-precise / AMEND_LOG
  historical fix records.

## 5. GATES (stage acceptance; full CSV: 06_REPORT/STAGE_ACCEPTANCE_GATES.csv)

| stage_gate_id | result |
|---|---|
| R2_F01_COUNTER | PASS |
| R2_F02_VCL_ERRATUM | PASS |
| R2_P3_LABEL | PASS |
| BEFORE_IMAGES | PASS (BYTE_IDENTITY YES x 3) |
| PREDECESSOR_MANIFEST | PASS (48 rows re-hashed: 0 stale / 0 missing; self-excluded) |
| R2_MANIFEST | PASS (computed last; re-hash 0 stale / 0 missing on the final file set) |
| CSV_SCHEMAS | PASS (all written/edited CSVs strict RFC4180; field counts verified) |
| SOURCE_FREEZE | PASS (frozen sources byte-identical to BASE+patch; numstat 30/6 + 20/5 at handoff) |
| PATCH_IDENTITY | PASS (both patch files byte-identical to the fresh live git diffs; not regenerated) |
| ENTRYPOINT_ROW_SURVIVAL | PASS (numstat 2/0; +2/-0 vs HEAD; all historical rows byte-preserved) |
| UNAUTHORIZED_CHANGED_PATHS | PASS (0; git status shape unchanged except the new R2 untracked root; no staging) |
| OPEN_P0P1P2 | PASS |
| INTERNAL_QC | QC_PASS_WITH_FINDINGS |
| PE_MASTER_VERDICT | MASTER_ACCEPTED |
| FINAL_REVIEW_INVENTORY | PASS |
| MILESTONE_STATE_ASSERTIONS | PASS (Gate A = PASS per the independent Desktop R2 audit; Gate C = REQUIRES_INDEPENDENT_DESKTOP_REAUDIT; Q1 NOT executed; Gate B canonical authority BLOCKED; M1 OPEN; M2 NOT AUTHORIZED; Viewer NOT AUTHORIZED) |

## 6. THE ONE P0 QUESTION + ANSWER

P0: Are Desktop R2's three bounded package-quality findings independently
reproducible, and can the three bounded predecessor corrections be applied
byte-safely with full before-image preservation, inside the authorized path
set? ANSWER: PASS — all three findings reproduced from primary sources
(terrain.bnt index bytes; the census per-file rows; the frozen patch bytes);
all three edits applied with BYTE_IDENTITY = YES before-images, exact-span
unified diffs, and 0 unauthorized changed paths.

## 7. NEGATIVE CONTROLS / FALSIFIERS (executed)

- The old counter falsifier: 51,920 x 32 = 1,661,440 != 1,664,000 (the old
  total is not any valid product over these denominators).
- The two-path independence: 51,920 x 1,024 and (220x32) x (236x32) computed
  separately and compared — both 53,166,080.
- The bad-equation repo search: 2,594 tracked files / 133,463,531 bytes, 3
  literal variants + a flexible regex — 0 hits (a hit would have flagged an
  unlisted affected file). Search timing: Phase 1 (pre-edit worktree,
  133,463,531 bytes; the R2 entrypoint row and this package's own records did
  not yet exist); post-run, the equation string appears only in this run's
  own quoted-as-false correction records — this package's own records and
  the new AUDIT_ENTRYPOINT.md R2 row — no repo file asserts it.
- The old-counter dependent search: the ONLY occurrences of "1,664,000" in
  the tracked repo are the correction descriptions themselves (0 live
  dependents).
- The patch-class negative control: any non-comment changed line beyond the
  exactness pair would have failed the classification; the classification
  found exactly 4+19 comments + 1 metadata-string pair.
- The before-image control: BYTE_IDENTITY (hash + size + full byte-compare)
  required YES for all three before any edit.
- The entrypoint control: numstat must be 2/0 with zero deletions; verified
  +2/-0 vs HEAD.
- The mislabel scan control: the 41-hit scan would have surfaced other live
  mislabels; one additional imprecise phrasing (F05:87) was found and is
  recorded honestly as open residue (outside the authorized edit set).

## 8. NOT_CHECKED (coverage honesty)

- The client NEVER ran; no GPU; no runtime experiment of any kind (STATIC-ONLY).
- No new RE beyond the bounded reproductions; the x87 CW question, Q1,
  P-CELLSTREAM/P-CLIMATE and every other M1 queue item remain where they were.
- The original-client comma/locale/tokenization semantics remain UNVERIFIED
  (unchanged statuses; no inference was made).
- The remote github.com state could not be live-fetched in this environment
  (no connectivity); the local origin/master tracking ref matched the pin;
  remote verification belongs to the persistence phase.
- The QC_PHASE / PERSIST_PHASE gates are PENDING (later workers).
- The F05:87 label residue was NOT edited (outside the authorized edit set).

## 9. CORRECTION CHAIN (chain of custody)

BASE_SHA = HEAD = cc747dfbf75d3c89c80bd8cccd33d6546fbfa36d (before AND after
this run; no commits made). Predecessor files edited: F03_TERRAIN_TEXTURE_
SCOPE.md 5704D1C8.../9,807 -> 72e1e221.../10,534 (EDIT A); EVIDENCE_INDEX.csv
02E03B7D.../7,536 -> 67bfee8c.../7,710 (EDIT B); MANIFEST_SHA256.csv
3A91F3A3.../8,520 -> a57aa321.../8,521 (EDIT C). Entrypoint:
8EEC84E6.../113,685 -> A0F21829.../115,846 (one row added). Full chain:
01_RAW/MODIFIED_PATHS.csv; exact diffs: 03_EVIDENCE/EDIT_*.diff.

## 10. PUSH DISCIPLINE

No push (this run performs NO git add/commit/push; persistence is the LATER
human-authorized Commit 1 by another worker). BASE_SHA = HEAD_SHA = cc747df.
Remote verification: NOT_PERFORMED_THIS_RUN (environment has no outbound
connectivity; recorded as the S0 deviation; the persistence worker must
verify the remote after Commit 1).

## 11. OPEN ITEMS / RESIDUE (loud, not buried)

- F05_EXACTNESS_ORIGIN_PRECISION.md:87 — an additional imprecise
  "(comment-only; zero arithmetic change)" phrasing of the PEFoliageCore
  correction, OUTSIDE this run's authorized edit set. Recorded as open
  residue in 01_RAW/FINDINGS.csv (R2-P3 open_residue) and
  02_ANALYSIS/R2_P3_EVIDENCE_LABEL.md section 4. NOT edited (the contract
  forbids editing any historical package span other than the three
  authorized). Its factual content ("zero arithmetic change") is true.
- PENDING_QC_PHASE: OPEN_P0P1P2 + INTERNAL_QC (later worker).
- PENDING_PERSIST_PHASE: PE_MASTER_VERDICT + FINAL_REVIEW_INVENTORY
  (later worker).
- P3 dispositions (persistence phase): OPEN_P0=0 OPEN_P1=0 OPEN_P2=0
  (both fresh QC contexts); P3-QC-1/2/3 FIXED+verified; P3-QC-4 (F05:87
  residue) and P3-QC-5 (RUN_CONTRACT final CRLF)
  EXPLICITLY_ACCEPTED_NONBLOCKING with written reasons; P3-RE-1
  (self-falsified 'no 9,916 anywhere' sentence)
  EXPLICITLY_ACCEPTED_NONBLOCKING with written reason
  (PE_MASTER_REVIEW.md section FINDINGS).

## 12. PAYLOAD DISCIPLINE

Zero proprietary payloads entered the repo: only identity metadata (names,
sizes, SHA256 values) and text records. The before-images are copies of
ALREADY-IN-REPO audit files. terrain.bnt was READ-ONLY (never copied); its
census output records names/counts only. VegetationClimates.bnt was only
hash-pinned this run.

## 13. DERIVED-NUMBER PROVENANCE

Every machine-readable artifact states its generator: the three JSON evidence
outputs name their probe scripts (03_EVIDENCE/scripts/r2_*.mjs, node v22.22.0);
the unified diffs name git diff --no-index (before-image vs post-edit); the
manifest is computed by this run's final hash walk (06_REPORT/
MANIFEST_SHA256.csv, self-excluded). Script hashes are in the manifest.

## 14. SELF-ADVERSARIAL PASS

02_ANALYSIS/SELF_ADVERSARIAL_PASS.md — 18 rows (claim / falsifier / test /
independent source / result / impact), ALL PASS. Labelled SELF_CHECK: it is
the executor's own pass, NOT an independent PE-MASTER audit. Process note:
during Phase 5 documentation, the executor's own verification pass caught a
transcribed-wrong manifest after-hash tail + after-size in three draft
package files (the actual manifest is 8,521 B, +1 byte from the "9807"->
"10534" digit growth); the error was corrected from fresh measurements
before finalization and is recorded here for chain honesty.

## 15. HANDOFF BLOCK (copyable)

AUDIT_OUTPUT_ROOT: docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/
FINAL_REPORT_PATH: docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/06_REPORT/REPORT.md
PRIMARY_EVIDENCE_PATHS:
- docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/03_EVIDENCE/R2_F01_TERRAIN_COUNTER.json
- docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/03_EVIDENCE/R2_F02_VCL_ARITHMETIC.json
- docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/03_EVIDENCE/R2_P3_PATCH_CLASS.json
- docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/03_EVIDENCE/EDIT_A_F03.diff
- docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/03_EVIDENCE/EDIT_B_EVIDENCE_INDEX.diff
- docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/03_EVIDENCE/EDIT_C_MANIFEST.diff
- docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/03_EVIDENCE/BEFORE_IMAGES/ (byte-exact x 3 + metadata CSV)
RUN_STATUS: COMPLETE (all three findings reproduced; all authorized edits applied byte-safely; gates as recorded)
HARD_STOP_REASON: NONE (no hard stop fired)
