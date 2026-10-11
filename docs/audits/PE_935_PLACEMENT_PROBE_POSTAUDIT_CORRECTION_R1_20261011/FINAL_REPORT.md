# FINAL_REPORT.md — PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011

**RUN_ID:** `PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011`
**MODE:** `BOUNDED_CORRECTION_ONLY` (fix the three post-audit P2 + resolve PA-1/PA-2; no
new science, no pilot, no RE)
**REPOSITORY:** `SebastianKozlo/eudoria-clean`
**DATE:** 2026-10-11

## 1. Contract and input identity (fail-closed BOOT)

```ini
CONTRACT = OPENCODE_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_COMPLETE.md
CONTRACT_SIZE_BYTES = 23496        (expected)  -> MEASURED 23496        = PASS
CONTRACT_SHA256 = 38205CE52733E3F1AEC707B9921BF7DABFDD5DC80F9A4F15B0DFAF3A43F67F5C
INPUT_PINS_SIZE_BYTES = 4550       (expected)  -> MEASURED 4550        = PASS
INPUT_PINS_SHA256 = F39541326226531F9C0F0806B30CE029BB5DD54403B50C82691AEABFEB043711
PINNED_INPUTS_16 = 16/16 MATCH
GIT_BLOBS_4 = 4/4 MATCH (placement_probe.mjs, gen_pre_identity.mjs, Bnt2Archive.js, ArkArchive.js)
ZIP_PE935_PLACEMENT_PROBE_KIT_R1 = size/SHA PIN PASS; 7 FILE_HASHES.json members 7/7 MATCH
BOOT_VERDICT = BOOT_PASS (independent PowerShell Get-Item/Get-FileHash bootstrap with
                explicit if-conditions in the invoking session, re-verified by
                PRE/gen_pre.mjs with node:crypto; expected values are frozen constants,
                never regenerated from measured files)
```

## 2. Baseline and refs

```ini
EXPECTED_BASE_SHA = 938aa9462560873126f1e9114dba0319062772f1
SOURCE_REF_SHA (refs/heads/research/pe935-placement-probe-correction-r1-20261011) = 938aa946... (local + remote)
MASTER = 3fbe93eec04759395223e6677b5040273d29222a (separate branch, NOT the base; unchanged)
RESULT_REF = refs/heads/research/pe935-placement-probe-census-postaudit-r1-20261011
BRANCH_RESERVATION = RESERVED (GitHub REST Create a reference: HTTP 201, ref/sha match,
                     follow-up GET 200; receipt PRE/BRANCH_RESERVATION.json, no tokens;
                     create-only — NO Update-a-reference, NO force; transport note: gh CLI
                     unauthenticated in this session, the contract REST operation was
                     executed directly via .NET HTTP with the credential-manager token
                     used in-memory only)
WORKTREE = detached HEAD at BASE under the run's own LOCAL_RUN_ROOT; main checkout untouched
SOURCE_PACKAGE_938aa946 = READ_ONLY, 37/37 Git blobs unchanged (PRE/SOURCE_PACKAGE_FREEZE.json)
```

## 3. The three P2 corrections (measured PRE → POST)

| Defect | PRE (unchanged BASE, this run's own reproduction) | POST (corrected, independently measured) | Verdict |
|---|---|---|---|
| **DA-1 / R2-5** false SCANNED | 4-entry BNT2 @ layout limit 100: e0 SCANNED, e1 OVER_BUDGET, **e2/e3 SCANNED though never analyzed**; scannedPayloadCount=**4**; censusOk=true (sum-only) | e0 **SCANNED/PARTIAL** (analysis started), e1–e3 **OVER_BUDGET/NOT_ANALYZED** (analysisStarted=false); scannedPayloadCount=**1**; whole tail accounted; censusOk computed by the exported `censusGate()` which **REFUSES** a mutant flipping an entry to SCANNED while keeping the sum; unopened files → **NOT_OPENED_BUDGET + UNKNOWN_ENTRY_COUNT**; duplicate names keyed by stable entryIndex | **CLOSED** |
| **DA-2 / R2-2** distinct-record cap | cap4/2 inputs: tracker 4, **8 distinct** at forward and serialization; cap256/9 inputs: tracker 256, **280 forward / 512 CSV**; outputs byte-identical between runs | per-phase independently measured peaks: cap4 **4/4/4**, cap256 **256/256/256** (creation/forward/serialization); serialized identities ARE the live rows; aliasing counts once; **forced-copy mutant detected (8 > 4)**; instrumented == ordinary (byte-identical outputs, identical budgets); small fixture still emits candidates; honest PARTIAL kept | **CLOSED** |
| **DA-3** effective Budget | `new Budget({layoutEvaluations:100001})`, `NaN`, `retainedCandidates:512` passed to exported analyzeBlob were **ACCEPTED** (NaN → null limit) | Budget constructor validates all five limits; effective tracker re-validated at use time (post-construction mutation refused); contradictory `budgetThresholds` refused fail-closed; masquerading non-instance supplies nothing; all refusals `INVALID_CONFIGURATION` **before any analysis** (layoutAttempts=0 after refusal); CLI exit!=0 + SCAN_STARTED=NO; no null-limit leak | **CLOSED** |

## 4. PA-1 / PA-2 (earlier post-audit observations)

- **PA-1 (regression coverage gap): CLOSED.** Byte-pinned fixtures PA1-A/B/C
  (153616 B; SHA256 `9AB2D32A…`, `2E8520FF…`, `20258A0C…` — all byte-exact) with
  harness-computed ground truth; production equals truth in all three:
  A = sample 1.0 / full XYZ 0.25 / full ID **0.25**; B = 1.0 / 0.25 / **1.0**;
  C = 1.0 / **1.0** / **1.0**; FULL_CENSUS 4800 under the legal budget 4800; the full
  result changes ONLY after changing unsampled bytes; the harness gate REJECTS a
  mutant FULL_XYZ=1.0 for A/B while keeping sample 1.0; without budget the target
  stays honestly PARTIAL_BUDGET_EXHAUSTED. The algorithm was NOT rewritten — the
  unchanged BASE already computed the right rates (a coverage gap, not a computation bug).
- **PA-2 (unconditional PASS gate): CLOSED.** `verify_inputs.mjs` (16 frozen expected
  pins, separate measured, conditional verdict) + `PRE/verify_inputs_runner.mjs`
  actually invoked in the REAL sequence **before POST/qualification**:
  PASS 16/16, exit 0. Mutants on PRIVATE copies (unchanged expected pins):
  same-size-wrong-SHA → BLOCKED; wrong-size → BLOCKED; missing → BLOCKED; each exit 3
  with **downstreamCalls all zero** (spy-proven) and **no real GitHub write**. The
  historical literal-PASS generator is superseded (SUPERSESSION.md); the historical
  extra manual check stays **UNVERIFIED**.

## 5. Test counts (units separated)

```ini
ORIGINAL_SEVEN (pinned ZIP kit, isolated stage) = 7 tests / 7 pass / 0 fail, exit 0
BASE_SUITE_BEFORE_CORRECTION (unchanged BASE 938aa946) = 27 tests / 27 pass / 0 fail
HISTORICAL_POST_REPLAY (frozen 938aa946 POST battery on BASE) = 47 outcomes PASS / 0 FAIL
FINAL_SUITE (corrected tools, isolated stage, 10 files) = 53 tests / 53 pass / 0 fail
POST_NAMED_CASES = 13 cases: 12 PASS + 1 CONTROL_PASS (DA2_MUTANT_COPY) + 0 FAIL + 0 ERROR + 0 NOT_PERFORMED
AGGREGATOR = QUALIFICATION_PASS (exit 0); refuses PASS with exit 4 when any single
             required result is removed (12/12 removals refused)
FRESH_INTERNAL_QC = INTERNAL_QC_PASS (5/5 fresh probes; distinct phase; author/origin
                    and measured-vs-read disclosed in QC/INTERNAL_REVIEW.md)
```
Tests, outcomes, files, findings and candidates are separate units; the battery count
is dynamic (13 named cases here, not a fixed 47).

## 6. Unique peak per phase/cap (DA-2)

| Case | creation | forward | serialization | PRE (forward/serialization) |
|---|---|---|---|---|
| cap 4 (2 inputs) | 4 | 4 | 4 | 8 / 8 |
| cap 256 (9 inputs) | 256 | 256 | 256 | 280 / 512 |
| forced-copy mutant (cap 4) | — | **8 (DETECTED > 4)** | 4 | — |

## 7. Tail dispositions (DA-1 canonical reproducer, 4 entries @ limit 100)

`SCANNED/PARTIAL` ×1, `OVER_BUDGET/NOT_ANALYZED` ×3; `scannedPayloadCount=1`;
`censusOk=true`; whole tail; state vectors `{admitted, payloadRead, analysisStarted,
analysisStatus}` on every entry. Fresh QC probe with SIX fresh entries at limit 50:
same semantics (1 started + 5 not-analyzed).

## 8. Scope and publication state

- Changed paths: all inside the allowlist (`tools/placement_probe/**`,
  `docs/audits/PE_935_PLACEMENT_PROBE_POSTAUDIT_CORRECTION_R1_20261011/**`,
  `AUDIT_ENTRYPOINT.md` with exactly one appended index line). Zero paths outside.
- `SOURCE_PACKAGE_UNCHANGED = YES` (37/37 blobs).
- No `.pyc`/foreign paths; no ZIP/SDK/game files published; all evidence bytes are
  synthetic or run-local.
- Exactly ONE commit with parent == 938aa9462560873126f1e9114dba0319062772f1 on the
  RESULT branch; fast-forward push of ONLY that ref; no master change, no amend, no
  force. `COMMIT_PARENT_SHA = 938aa9462560873126f1e9114dba0319062772f1`;
  `RESULTING_SHA`/`LOCAL_HEAD_SHA`/`REMOTE_TRACKING_SHA`/`ACTUAL_REMOTE_SHA`:
  NOT_CREATED at the time this report is frozen (manifest closure precedes the commit);
  the actual values are recorded in the post-publication receipts
  (PRIVATE_EVIDENCE + the terminal report to PE-MASTER) and are deliberately NOT
  written into this commit's files (AUDIT_ENTRYPOINT contains no self-SHA).
- Fix rounds used: **0 post-first-green-suite rounds against the tool** (of max 2);
  bring-up iterations and harness bugs are disclosed in AMENDMENT_LOG.md.

## 9. Open findings

`P0 = 0`, `P1 = 0`, `P2 = 0` open in scope; `P3 = 4` disclosed (QC/FINDINGS.json):
historical SHA-typo record (unwritable history), the preserved 61-request counter
semantics (now honestly described), the superseded historical branch-reservation
record, and the pre-existing containerReadBytes-before-RAW-refusal accounting
limitation (R2-4, disclosed).

## 10. Standing science freeze (absolute)

```ini
MODEL_218757_TO_CMO_JOIN = NOT_ESTABLISHED
MODEL_218757_TO_WORLD_INSTANCE = NOT_ESTABLISHED
WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED
HISTORICAL_PLACEMENT = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
PLACEMENT_DISCOVERY = NOT_EXECUTED
STANDING_SCIENCE_STATUS_CHANGES = NONE
CANONICAL_GATE_EFFECT = NONE
EXTERNAL_DESKTOP_POST_AUDIT = PENDING
PILOT_SCAN = AWAITING_HUMAN_AUTHORIZATION
NEXT_EXPERIMENT_AUTHORIZED = NO
NEXT_MILESTONE_AUTHORIZED = NO
HARD_STOP = YES
```

This run qualifies the tool **on synthetic data only** and publishes the exact state
for the external Desktop post-audit of the new commit. It does not authorize a pilot,
the gb112 adapter, or any new RE.
