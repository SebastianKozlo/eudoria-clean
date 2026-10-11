# INTERNAL_REVIEW — PE_935_PLACEMENT_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_20261011

## PART A — EXECUTOR-SELF-QC (preserved from the executor's original review; origin: the executor session that implemented the correction)

This part preserves the substance of the executor's own review record (the original
file content was authored by the executor after matrix batch 3). It is **executor
self-QC, internal to the run**: it is **NOT a fresh-context internal QC** (that was
NOT_PERFORMED_IN_EXECUTOR_SESSION and is performed by PART B below) and **NOT an
external Desktop post-audit** (EXTERNAL_DESKTOP_POST_AUDIT = PENDING).

Executor probes (7/7 PASS, details in QC/FINDINGS.json Part A):

| # | Probe | Kind | Result |
| --- | --- | --- | --- |
| QC-A | Legacy shape independence: archived CLEAN receipt has NO schema field and NO perPin inputMatch; a stripped CLEAN copy still qualifies | independent probe | PASS |
| QC-B | Trusted-pin independence: EXPECTED==MEASURED but both != trusted pins (self-authority) refused | independent probe | PASS |
| QC-C | No CLEAN-hash-listing: re-serialized semantically identical CLEAN (different whole-file SHA256 27eef69b…) still qualifies | independent probe | PASS |
| QC-D | Canonical POST exit path on M1 (replay): exit 4, PA2 FAIL, QUALIFICATION_REFUSED | replay | PASS |
| QC-E | WeakMap observer no-retention: every leaf of TWO_SOURCE_OBSERVER.json scalar; auditObjectsRetained=0 | independent probe | PASS |
| QC-F | Source freeze: only the comment-corrected pa2_identity_gate.test.mjs modified among tracked files vs BASE | independent probe (git) | PASS |
| QC-G | cap32 29+3 replay on final bytes | replay | PASS |

Executor findings: SELF-QC-F1 (batch-1 driver crash — resolved, invalidated batch
retained), SELF-QC-F2 (fresh-context QC not performed in executor session — OPEN,
assigned to the later pe-master-auditor pass), SELF-QC-F3 (frozen verify_inputs.mjs
legacy "spy" wording — superseded by SUPERSESSION.md), SELF-QC-F4 (pre-existing BASE
accounting P3 — preserved). All P3, none P0/P1/P2.

## PART B — FRESH-CONTEXT INTERNAL_QC (this section; origin: a fresh pe-master-auditor session, internal to this run per contract §8 and the governing dispatch; NOT an external Desktop post-audit)

QC_VERDICT: **INTERNAL_QC_PASS_WITH_FINDINGS** (all ten mandated check areas PASS;
findings QC-F1..QC-F7 below are P3/information, none blocking; no P0/P1/P2).

QC_ORIGIN: fresh-context pe-master-auditor session (separate from the executor
session), 2026-10-11. Scope: independent inspection of input identities, receipt
shape, trusted pin source, code identity, the new canonical acceptance/aggregation
path, mutation causality, two-source contributions, observer effect, source freeze
and manifest scope, plus independently crafted adversarial probes. Re-executions of
executor scripts are labeled REPLAY; everything else below is INDEPENDENT (own
scripts/measurements unless noted).

### B.1 Full-read log (load-bearing code and documents read to EOF in this QC session)

- Contract OPENCODE_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_COMPLETE.md (302 lines,
  identity verified first — see B.2).
- tools/placement_probe/qualification/pa2_r1/validate_receipt.mjs — FULL READ (362 lines).
- tools/placement_probe/qualification/pa2_r1/run_post.mjs — FULL READ (581 lines).
- tools/placement_probe/qualification/pa2_r1/run_matrix.mjs — FULL READ (236 lines).
- tools/placement_probe/qualification/pa2_r1/two_source.mjs — FULL READ (100 lines).
- tools/placement_probe/tests/pa2_receipt_qualification.test.mjs — FULL READ (198 lines).
- tools/placement_probe/tests/da2_two_source.test.mjs — FULL READ (99 lines).
- tools/placement_probe/verify_inputs.mjs (BASE blob) — FULL READ (102 lines).
- Package documents read in full: FINAL_REPORT.md, HANDOFF.md, SUPERSESSION.md,
  AMENDMENT_LOG.md, EVIDENCE_INDEX.md, BUDGET_ACCOUNTING.json, PRE/BASELINE_REPRODUCTIONS.json,
  PRE/INPUT_IDENTITIES (run-root preflight copy), PRE/SOURCE_IDENTITIES (run-root preflight
  copy), POST/FULL_POST_RESULTS.json, POST/AGGREGATOR_CONTROLS.json,
  POST/VALIDATOR_PROFILE_CONTROLS.json, POST/TWO_SOURCE_AGGREGATION.json (464 lines),
  POST/LIVE_INPUT_REMEASUREMENT.json, POST/REGRESSION_RESULTS.json,
  POST/RECEIPT_MUTATION_MATRIX.json (summary/ACTUAL fields extracted programmatically),
  POST/RAW/b1/BATCH1_NOTE.json, QC/FINDINGS.json (executor), CONTRACT.md (via run-root
  pin identity).
- Executor QC/INTERNAL_REVIEW.md original content — FULL READ (92 lines, preserved as Part A).
- Not read to EOF (NOT_CHECKED): the 4 private PRE case raw JSON bodies (PRE/RAW/clean,
  m1, m2 POST_TEST_RESULTS.json etc.) were census-listed and their BASELINE_REPRODUCTIONS
  summaries read, but not every raw line; POST/RAW/{m1..m9} raw case bodies were spot-checked
  via POST/FULL_POST_RESULTS.json and RECEIPT_MUTATION_MATRIX.json programmatic extraction
  rather than full-line reads; qc\qc_probes.mjs (executor probe script, 9067 B) was not read
  line-by-line (its outputs QC_PROBE_RESULTS.json were recorded and its probes were
  re-derived independently here). None of these carry a load-bearing claim not otherwise
  verified below by independent measurement.

### B.2 Contract identity (independent)

`C:\Users\User\Documents\ChatGPT\PE\PE_PLACEMENT_PA2_QUALIFICATION_CORRECTION_PROMPT_20261011\OPENCODE_PA2_RECEIPT_QUALIFICATION_CORRECTION_R1_COMPLETE.md`
measured by this QC: SIZE=29207, SHA256=6E4B0B029DBD082451A6F0E432AA66124FCC5E3299260AC3E330A59DED4F4E23 — MATCHES the dispatch pin exactly.

### B.3 The ten mandated check areas — commands, evidence, verdicts

**CHECK 1 — Actual input identities (INDEPENDENT, PASS).**
Own re-hash (PowerShell [System.Security.Cryptography.SHA256], fresh reads) of all
16 pinned evidence files listed in the BASE gate module + the 4 §1 Desktop evidence
files: **20/20 MATCH** (sizes and SHA256 equal to the contract §1 pins and the
gate-module constants; includes PE935_Placement_Probe_Kit_R1.zip 21832 B /
F03D6DA3… and all four PE_PLACEMENT_PROBE_POSTAUDIT_28E91EB_20261011 files).
Own extraction of the 7 §1 BASE blobs via `git cat-file blob 28e91eb…:<path>` and
fresh hashing: **7/7 MATCH** (verify_inputs.mjs 9019/568CE3F2…,
placement_probe.mjs 54156/0D69AAFE…, pa2_identity_gate.test.mjs 8739/5FC89BC0…,
da2_retained.test.mjs 12988/0927352F…, predecessor POST run_post.mjs 48995/3BBDC404…,
predecessor PRE runner 4783/A4733B0D…, CLEAN receipt 8251/837030AB…).
Worktree HEAD = BASE 28e91eb (rev-parse), branch research/pe935-placement-pa2-qualification-correction-r1-20261011.

**CHECK 2 — Receipt shape (INDEPENDENT, PASS).**
Own full read of the CLEAN receipt (package POST/RAW/receipts/CLEAN.json, and the
private matrix\receipts\CLEAN.json copy): 8251 B, SHA256 837030AB901D7E2D… —
byte-identical to the BASE blob (nothing edited CLEAN; three independent copies
measured: BASE git blob, private matrix copy, package copy — all 837030AB…).
Shape confirmed by direct reading: NO top-level `schema` field; NO perPin
`inputMatch` field; perPin entries carry exactly pin/compareResult/EXPECTED{sizeBytes,
sha256}/MEASURED{exists,sizeBytes,sha256}; runId=PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011,
stage=PA2_LIVE_IDENTITY_GATE, mode=REAL_SEQUENCE; moduleIdentity.gateModule.path
uses backslashes (validator normalizes slashes only), SHAs lowercase (hex-case
normalization only); gate total/matched=16, blockedCount=0, blockedPins=[].

**CHECK 3 — Trusted pin source (INDEPENDENT, PASS).**
validate_receipt.mjs read to EOF: `loadTrusted()` verifies TRUSTED_GATE_MODULE and
TRUSTED_RUNNER SHA256 against frozen constants BEFORE importing the gate module,
then freezes pins from `m.EXPECTED_INPUT_PINS` of the SHA-verified module; expected
values are never read from the receipt (profile/consistency code only COMPARES
receipt fields against the trusted pins). The 16 pin values in the BASE gate module
(lines 17–32) were compared with the executor's PRE/INPUT_IDENTITIES — identical.
REPLAY note: LIVE_INPUT_REMEASUREMENT.json (PASS 16/16) is executor output; my own
20/20 re-hash (Check 1) is the independent confirmation.

**CHECK 4 — Code identity checks / §4.2 predicates (INDEPENDENT code read, PASS).**
All four pa2_r1 modules read to EOF. Predicates verified as implemented:
(1) trusted SHA-before-pin-load (Check 3); (2) exactly-16 distinct pin names
(count check + duplicate filter + missing/extra lists), strict types via
Number.isSafeInteger / typeof==='boolean' / HEX64 regex — no string→integer, no
truthy→boolean coercion; SHA hex-case-only normalization (normHex), bytes never ignored;
(3) EXPECTED vs trusted pins; MEASURED.exists===true; measured size/SHA vs the same
pins; derivedCompareResult re-derived independently; claimed compareResult validated
(`compareResultValid`) not trusted; inputMatch never required (optional-consistency
only); (4) recomputed total/matched/blockedCount/blockedPins/verdict/EFFECTIVE_GATE_RESULT
with full consistency checks + the PASS-requires-all-16/zero-blocked/empty-array rule;
(5) exact runId/stage/mode equality; module paths with `replaceAll('\\','/')` slash
normalization only; SHAs vs trusted constants; (6) live verifyAllInputs required
(INPUT_BYTES_REMEASURED.pass true is a conjunct of fourQuantitiesOk), receipt hash
taken before/after and equality asserted (receipt never repaired); (7) fail-closed:
parse failures/missing files/exceptions all return controlled RECEIPT_QUALIFICATION
FAIL with reasons preserved (verified live in my adversarial probes B.4), never an
exception-to-PASS; (8) computeQualification is strict-conjunctive (missing = key
absent; failing = strict !== against frozen EXPECTED_OUTCOMES; only the documented
statuses PASS/CONTROL_PASS count) and drives process.exitCode (0 or 4).
Batch code identity: the frozenCode block in POST/FULL_POST_RESULTS.json equals the
current worktree bytes — my own hashing of all four pa2_r1 files: MATCH 4/4
(run_post 301e081d…, validate_receipt 37e679b3…, two_source bf6ae49d…, run_matrix
f2026073…) and gate module worktree = 568ce3f2… (BASE). freezeOk=true consistent.

**CHECK 5 — Mutation causality (INDEPENDENT deep-diff, PASS).**
Own node deep-diff (no executor script) of matrix\receipts\M{1..9}.json vs CLEAN.json:
- M1: exactly 1 leaf — perPin[0].MEASURED.sha256 → 64 zeroes (all else identical).
- M2: exactly 1 leaf — moduleIdentity.gateModule.sha256 → 64 zeroes.
- M3/M4/M5/M6/M8 also exactly the contract-specified single change (bonus coverage).
- M7: exactly 2 leaves — gate.matched 16→15, gate.blockedCount 0→1.
- M9: exactly 8 leaves — perPin[0].MEASURED.{exists→false,sizeBytes→null,sha256→null},
  perPin[0].compareResult MATCH→MISSING, gate.{matched→15,blockedCount→1}, gate.blockedPins
  []→[1 entry]; gate.verdict/EFFECTIVE_GATE_RESULT UNCHANGED (the contradiction under
  test) — confirmed unchanged by the diff (no leaf reported there).
Refusal semantics (POST/FULL_POST_RESULTS.json, cross-checked against the raw
RECEIPT_MUTATION_MATRIX.json ACTUAL.cases): every M-case refuses with the specific
semantic reason (M1 "MEASURED.sha256 differs from the trusted pin (claimed MATCH)";
M2/M8 module-identity SHA; M4 forged compareResult; M5/M6 count; M7 "gate.matched 15
!= recomputed 16"; M9 "MEASURED.exists is not true … verdict PASS != recomputed
BLOCKED_INPUT_IDENTITY") — none is a whole-file-hash rejection. Non-hash-listing also
independently confirmed: my adversarial receipts below (fresh files, different SHA)
were refused for their own semantic reasons, and the executor's QC-C re-serialization
control passed.

**CHECK 6 — Two-source 29+3 (INDEPENDENT recompute from raw CSV, PASS).**
Own row count over the raw ordinary-run CSV
(matrix\case_CLEAN\runroot\staging\post_fixtures\da2_two_source\un\placement_candidates.csv):
33 lines = header + 32 rows; per-input: raw_0.vfs = 29 rows, raw_1.vfs = 3 rows
(sum 32). Own byte-compare of the four ordinary vs instrumented outputs: 4/4
byte-identical (placement_candidates.csv 16801 B, candidates_top.json 166209 B,
sources.json 1671 B, scan_skips.csv 273 B). Own read of sources.json: both inputs
parseStatus OK (analysisStatus COMPLETED / PARTIAL). Own read of SUMMARY.json:
candidateCount=32, coverage=PARTIAL, peakRetainedCandidates=32. Peaks 29/32/32 and
per-phase observer records read from TWO_SOURCE_AGGREGATION.json (forward phase
provenance per input 29 and 3; serialization allSerializedAreLiveRows=true;
auditObjectsRetained=0 in every phase; WeakMap scalar-id design confirmed in the
two_source.mjs full read — no candidate objects retained as audit roots).
Observer/tool identity: ordinaryToolSha256=0d69aafe… equals the BASE scanner blob I
hashed in Check 1 (unchanged scanner); observedToolSha256=f2568842… (instrumented
copy). cap29 negative control read in the test source: second input NEVER opened
(sources[1].parseStatus === 'NOT_OPENED_BUDGET'), contributions [29,0], and the
two-contributing-sources predicate is asserted false — the control exercises the
actual predicate.

**CHECK 7 — Observer effect / source freeze (INDEPENDENT git + hashes, PASS).**
Own hashes: worktree scanner placement_probe.mjs = 0D69AAFE… = BASE blob (frozen);
verify_inputs.mjs = 568CE3F2… = BASE. Census: `git diff --name-only HEAD -- docs/audits`
filtered to everything outside the new package → EMPTY (0 paths); `git ls-tree -r HEAD
-- docs/audits` → **4761** historical tracked blobs (matches the claimed 4761 census;
HEAD=BASE so tracked-blob equality is exact byte identity); protected files
(placement_probe.mjs, verify_inputs.mjs, ids_from_export.mjs, package.json,
src/pesource adapters) → zero diff, zero untracked; full `git status --porcelain`
census → every changed path is inside the §2 allowlist (tools/placement_probe/qualification/**,
tools/placement_probe/tests/**, the new package, AUDIT_ENTRYPOINT.md). No foreign edits.

**CHECK 8 — Manifest scope (INDEPENDENT full re-hash, PASS — all 165 rows, not a sample).**
Own node script (no executor code) re-hashed **all 165 data rows** of
MANIFEST_SHA256.csv against the worktree files: 0 size mismatches, 0 SHA mismatches,
0 duplicates, 0 path-escapes. Bijection census: changed paths = 2 modified +
164 untracked = 166; minus the self-excluded manifest = 165 = manifest row count;
missing=0, extra=0. Row areas: 4 qualification + 3 tests + 157 package + 1
AUDIT_ENTRYPOINT.md. AUDIT_ENTRYPOINT.md git numstat: **1 insertion / 0 deletions**
(single new table row; all historical bytes preserved). Physical package file count
(measured): 158 — a different unit, as declared. Max package path length measured
255 (<260). Manifest CSV structure: 1 header + 1 #SCOPE# line + 165 data rows.

**CHECK 9 — Aggregator controls (INDEPENDENT code + record read, PASS).**
run_matrix.mjs lines 182–204 read: the three controls import `computeQualification`
and `EXPECTED_OUTCOMES` FROM THE SAME validator module the canonical POST uses, and
apply them to the REAL measured outcomes parsed from the CLEAN case's
POST_TEST_RESULTS.json (not a toy conjunction). POST/AGGREGATOR_CONTROLS.json:
missing → QUALIFICATION_REFUSED/exit4 with missing=[PA2_RECEIPT_QUALIFICATION];
FAIL → failing=[PA2_RECEIPT_QUALIFICATION]/exit4; NOT_PERFORMED → same. The
computeQualification code path matches (missing = `!(id in outcomes)`, failing =
strict `!==`). Additionally my adversarial run B.4 exercised the whole POST
aggregation end-to-end (PA2 FAIL → overall REFUSED/exit 4).

**CHECK 10 — Honest-negative adversarial probes (INDEPENDENT, own inputs, PASS).**
Two adversarial receipts crafted by THIS QC session (fresh CLEAN-based copies,
written only to a PRIVATE runroot under C:\Users\User\AppData\Local\Temp\opencode\qc_pa2\adv_run;
worktree untouched), executed through the actual CANONICAL_POST CLI:
- adv1 `perPin[0].MEASURED.exists = "true"` (truthy STRING instead of strict boolean),
  8253 B / SHA256 e083bd96…: full POST → PA2 FAIL, QUALIFICATION_REFUSED, **exit 4**;
  refusalReason "perPin[0].MEASURED.exists is not a strict boolean"; 10 semantic
  refusal reasons recorded (no-coercion honored; derived consequences all reported).
- adv2 `gate.total = "16"` (STRING instead of safe integer), 8253 B / SHA256
  700b6159…: full POST → PA2 FAIL, QUALIFICATION_REFUSED, **exit 4**; refusalReason
  "gate.total is not a safe integer (no coercion)".
Both refusals are controlled (nonzero exit, diagnostics preserved, other cases still
passing: 13 PASS + 1 CONTROL_PASS in each run). Command shape (executed twice):
`node <worktree>/tools/placement_probe/qualification/pa2_r1/run_post.mjs --worktree <wt>
--runroot <private> --kitdir <stage_kit> --receipt <adv-receipt.json> --out <private-out>`.

### B.4 Conjunction status (contract §9) as evaluated by this QC

preflight/source integrity PASS; preserved historical regression (BASE 53/53 replay
+ kit 7/7) PASS; CLEAN PASS (matrix + identity to BASE blob) PASS; M1..M9 PA2-caused
full-POST refusal 10/10 CONTROL_SUCCESS PASS; 4 profile unit controls (+CLEAN-unchanged
control) PASS; 3 actual aggregator controls PASS; cap32 two-source regression (29+3,
independently recomputed from raw CSV) PASS; required internal QC — performed by this
fresh-context pass (this document; INTERNAL_QC_PASS_WITH_FINDINGS); source freeze
(4761 blobs + protected files + allowlist) PASS; no material unresolved P0/P1/P2 in
this correction scope PASS (all QC findings are P3, listed below).
**The §9 QUALIFICATION_PASS conjunction is now SATISFIED as evaluated by internal QC**
(with the standing limitation that internal QC is NOT an external Desktop post-audit;
EXTERNAL_DESKTOP_POST_AUDIT remains PENDING, and publication is a separate phase).

### B.5 Findings of this fresh-context QC (details in QC/FINDINGS.json Part B)

- QC-F1 (P3): EVIDENCE_INDEX.md and POST/REGRESSION_RESULTS.json describe
  pa2_receipt_qualification.test.mjs as "(11 tests)"; the file has **9** tests
  (independently counted; 11 = 9 PA2-RQ + 2 DA2-COV total new tests; FINAL_REPORT §8
  and HANDOFF state 9+2 correctly). Documentation transcription defect only; suite
  counts 64/64 and the required-prefix probe are unaffected. Disposition: record;
  correct at persistence if PE-MASTER orders it (frozen artifact, outside QC/ scope).
- QC-F2 (P3): repair-round classification. The post-batch-1 edit (validator refactor
  84b08649… → 37e679b3… + defensive driver extraction) meets the literal §8 definition
  of a repair round (edit batch responding to a recorded failed check + revalidation).
  The executor disclosed the dual reading ("0/2 against the tool / 2/2 if counted as
  repair rounds") and the MAX_CORRECTION_ROUNDS=2 cap is not exceeded under either
  reading; no edit after the final batch. Disposition: ACCEPTED_AS_DISCLOSED.
- QC-F3 (P3): executor FINDINGS.json QC-F "untracked" list erroneously repeats the
  modified-file entry as if untracked ("M tools/.../pa2_identity_gate.test.mjs");
  the real untracked census is 164 files + the package. Cosmetic self-QC record defect.
  Disposition: DOCUMENTED (my census is authoritative in B.3 Check 7/8).
- QC-F4 (P3): one PRIVATE PRE evidence path has exactly 260 characters
  (pre\case_m2_gate_module_sha_zeroed\runroot\staging\stage_post\docs\audits\...
  \PRE\verify_inputs_runner.mjs) — at the Windows MAX_PATH boundary. The claim
  "every raw path <260" holds for the published PACKAGE (max 255, measured), not for
  this one private path (=260, not <260). File exists and is readable. Disposition:
  DOCUMENTED; recommendation for future runs: shorter PRE case-dir names.
- QC-F5 (P3): POST/REGRESSION_RESULTS.json declares DENOMINATOR=60 (53 BASE + 7 kit)
  while measuring three sets (the 64-test current suite has no row in that
  denominator). Imprecise unit declaration, not a measurement error. Disposition: DOCUMENTED.
- QC-F6 (P3): BASE_53_REPLAY stages the 10 BASE test files as they stand in the
  worktree — 9/10 byte-identical to BASE; pa2_identity_gate.test.mjs carries the
  §6-authorized comment/assert-message-only corrections (my -U0 diff: 10 insertions/
  3 deletions, all in comments or an assert MESSAGE string; assertion compared values
  and test count unchanged). Honestly disclosed by the executor (HANDOFF Deviation 3,
  REGRESSION_RESULTS note). Disposition: ACCEPTED_AS_DISCLOSED.
- QC-F7 (information): writing this fresh-context QC into QC/INTERNAL_REVIEW.md and
  QC/FINDINGS.json changes those two files' bytes, so the persistence phase MUST
  regenerate MANIFEST_SHA256.csv before staging (per §10 "manifest LAST"); the
  bijection set is unchanged, only two size/SHA cells change. Disposition:
  MANIFEST_REGENERATION_REQUIRED_AT_PERSISTENCE (normal workflow, not a defect).

No P0/P1/P2 findings. No repair round was ordered by this QC (0 QC-ordered rounds;
the two-round cap is untouched; all findings are recordable documentation-level
items outside QC/ write scope or normal-workflow notes).

### B.6 Limitations

- This is internal QC of the run, NOT an external Desktop post-audit
  (EXTERNAL_DESKTOP_POST_AUDIT = PENDING) and NOT a PE-MASTER verdict.
- The canonical POST is the executor's own harness; my adversarial probes and raw-CSV
  recomputations are independent measurements through/over it, not a second
  implementation of the checks.
- The 29+3 cap32 case is synthetic-fixture evidence about the audited cases; it does
  not establish GENERAL_TOOL_CORRECTNESS. No game payload was scanned in this QC.
- Hash consistency is not proof of historical execution, authorship, or a signature.
