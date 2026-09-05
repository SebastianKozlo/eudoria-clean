# EXTERNAL_REVIEW — persisted external post-audit + correction direction

Provenance: the FULL external post-audit of PE-NIF-CLAIM-EVIDENCE-LOCK-R2 and
its correction direction are persisted here VERBATIM (byte-exact content
embedded below) with recomputed SHA256 hashes, per the R3 publication contract.
The external post-audit run directory is READ-ONLY and was NOT modified; the
R2 history is NOT rewritten — supersessions are recorded as NEW evidence
(05_ANALYSIS/SUPERSESSION_MAP.csv).

## Hashes (recomputed this run)

| Artifact | Path | SHA256 |
|---|---|---|
| External post-audit final report | PE_NIF_R2_POST_AUDIT_20260905_025627\06_REPORT\00_FINAL_REPORT.md | 8681f754adb0f05f56074b22f7338e7f69a4648cc5241d34a759bfdd66376178 |
| Revalidation prompt (correction direction; executed by this run) | PE_NIF_R2_POST_AUDIT_20260905_025627\00_CONTROL\OPENCODE_REVALIDATION_PROMPT.md | 662d4c522a570d210549618bfee7d27acbc0253f39034c005c2678bde389d35c |
| External verifier (read-only reproducer) | PE_NIF_R2_POST_AUDIT_20260905_025627\00_CONTROL\verify.py | c0fa16fe81717158ffd6c563d7fb58998c136e75af4f7c6c3f55ed264aac1d62 |
| External verification record | PE_NIF_R2_POST_AUDIT_20260905_025627\01_RAW\verification.json | 6617a8f68442664f3d70e96e7bdc330b2e3e3cc09943f9eaaa18ff202f39d41f |

## VERBATIM: external post-audit final report (verdict REVALIDATION_REQUIRED)

The external auditor independently verified its findings before this run; THIS
run additionally re-tested the counterexamples against the actual bytes of the
hash-pinned R2 source (gates R3G3a/R3G3b/R3G6b) rather than accepting them
blindly. All five R2 counterexample values and all five corrected values
reproduced exactly.

`markdown
# Focused external post-audit — NIF claim-lock R2

Date: 2026-09-05. Verdict: **REVALIDATION_REQUIRED**.

This is focused physical revalidation requested by the human, NOT a full EU935-M2 milestone audit and NOT milestone closure. Accept the corrected file counters and byte preservation. Do not approve blanket application of P1R2–P8R2 yet.

```text
SELECTED_AUDIT_TARGET = D:\Eudoria_Reconstruction\99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054
TARGET_CLASS = COMPLETED_RUN
WHY_THIS_TARGET = Explicit handoff; report, raw results, executed sources, gates and published package available.
SKIPPED_NEWER_ARTIFACTS = Later governance commit 5358d969 is not a new NIF experiment; separate Surface/M1 work excluded.
AUDITED_COMMIT = 97ed5e54f685a5a7ed7a47d761d2b6cc42bfd4b7
P0 = HASH_PRIMITIVE_VALUE_IDENTITY_BEFORE_AGGREGATE_ACCEPTANCE
WIKI_APPLICATION = HOLD
MILESTONE_ADVANCEMENT = NOT_AUTHORIZED
```

## 1. What passed independent checks

- Direct BNT parse and byte equality: 5422 shared = 5208 identical + 214 changed; 4 old-only; 174 new-only; d exceptions 524071/524077/524083.nif unchanged.
- Morph ASCII presence: 29 occurrences in 3 changed older-side files: 548296 (13), 548808 (13), 566482 (3). The replacement's presence-only limitation is appropriate.
- Independent Python physical census: all ten **correctly implemented** candidates produce the same final match-count table as R2. Nine zero-match candidates; payload CRC candidate 3435/5596 and 3299/5426. `c==CRC32(payload)` remains 11022/11022.
- All 12 lossless sidecars reconstruct the entire original manifest bytes exactly, including retained BOM/newlines. Accept byte-level losslessness. Do not confuse it with correctness of every interpreted field.
- 53/53 hash-bearing manifest entries match current files. Three documented exclusions are pinned by publication, not mistaken for self-validating hashes.
- 35/35 local run files match Git blobs at 97ed5e54. Commit is confined to the R2 directory. No proprietary payload publication in that bounded package was observed.

Proof: `01_RAW/verification.json`; reproducer: `00_CONTROL/verify.py`, relative to this NEW auditor run. The verifier did NOT execute complete historical drivers or overwrite their outputs. It executed only the two literal pure helper declarations extracted from the hash-pinned R2 source, then compared their returned values with independent references.

## 2. P0: two Node hash primitives are wrong; aggregate agreement conceals it

**F1 — CONFIRMED implementation/validation defect.** R2 `00_CONTROL/control_r2.cjs` definitions `adler32` and `fnv1a` do not implement their declared algorithms correctly.

| Input / function | R2 Node value | Correct reference |
|---|---|---|
| empty bytes / Adler-32 | 00010000 | 00000001 |
| ASCII `a` / Adler-32 | 00620061 | 00620062 |
| ASCII `hello` / Adler-32 | 06280214 | 062c0215 |
| ASCII `hello` / FNV-1a-32 | a82fb4a1 | 4f9f2cab |
| ASCII `548296.nif` / FNV-1a-32 | 200d96de | 4e2b6736 |

Adler's first accumulated sum should start at 1 and the second at 0. The Node helper instead starts the direct byte sum at 0 and its accumulated sum at 1, producing a different function. The reference is Python zlib and the Adler definition in [RFC 1950 §2.2 and sample code](https://www.rfc-editor.org/rfc/rfc1950.html).

FNV uses ordinary JavaScript Number multiplication before `>>>0`. Large intermediate products lose integer precision before the 32-bit reduction. The reference uses exact Python integer multiplication modulo 2^32, following [RFC 9923](https://datatracker.ietf.org/doc/html/rfc9923). A future implementation can use validated exact 32-bit arithmetic; a cast after an already rounded multiplication is not sufficient.

Across the **11022 filename entries**, comparing actual helper return values:

- Adler(name): **11022/11022 mismatches** against zlib.
- FNV-1a(name): **11016/11022 mismatches** against exact integer reference.

Nevertheless, both erroneous functions and the correct reference yield zero equality-to-d matches for those candidate families. Therefore R2G8 passes the 20 candidate-era **aggregate counts**, despite materially different function values. These mismatch counts cover filename inputs; they are not claimed to be a measured per-payload Adler mismatch census.

Important distinction:

```text
Nine exact-zero candidate counts = independently CONFIRMED by correct reference.
Node implements the named algorithms correctly = REJECTED.
20/20 matching aggregate counts proves implementation identity = REJECTED.
```

Blast radius: R2 control source, candidate-method provenance, R2G8's independence assurance, C2-B method evidence, C2-E gate-detection assurance, report/handoff claims of cross-implementation revalidation. Do not revert the actual nine/CRC-subset result or unrelated successful counter/sidecar fixes.

Required repair: new run-local implementation; known-answer tests for empty, one-byte, multi-byte, binary and overflow-sensitive inputs; exact per-input output comparison before match-count aggregation; negative tests must show the literal R2 helpers fail and a replacement that returns wrong values but the same zero match-count cannot pass. Preserve R2 unchanged.

## 3. F2: a new morph proposal overstates the residual population

R2 P1R2-5 says **“334 real-record spans fit no tested grammar.”** This is false as stated.

Independent filtering of R34 `02_results/REAL_SPARSE_GRAMMAR.json`, `per_span`, using its exact classifier `has_real && n_wp_inrange > 0`:

- 334 classifier-real spans have `var_ok == 0`.
- **62 of those 334** have another recorded fit (`g1_ok`, `g2_ok` or nonempty `mscan_ok_m`).
- 272 have no fit in those recorded model fields.

Concrete counterexample: `592572.nif`, bi=65, si=45: `var_ok=0`, `has_real=true`, `n_wp_inrange=2`, `mscan_ok_m=[30]`. Another: `579739.nif`, bi=109, si=138, `mscan_ok_m=[4]`.

These are historical per-span results independently re-summed, not a new physical grammar execution. Correct wording: **334 classifier-real spans do not fit the tested variable-k model**. Other candidate-model fits are not automatically true segmentation or semantic confirmation. Keep 2093/2427 and 3186/6167 scoped exactly.

The broader P2R2-2 paragraph also still uses “every byte-exact grammar reproduced at 100%”. Do not export that as all 21 claims passing at 100%: the cited R35 table includes C-MORPH-1 at 86.2% / 81.0% of classifier-real spans and separately graded claims. Prefer the explicit per-claim table and 19 ERA-STABLE / 2 EVOLVED observations, with sample/denominator limits; no new grammar experiment is requested.

## 4. F3: human-review state is serialized incorrectly; a tally label is stale

R2 `run_gates.py` calls `gate(..., None)` for HR-1..HR-4, but `gate` stores `bool(ok)`, converting None to false. The frozen `TEST_RESULTS.json` contains four `false` values; generated CSV contains four **FAIL** results. The report says they are null by design and await human review.

This is a pending-vs-failed state bug, not evidence that a human reviewed and rejected four gates. Preserve an explicit pending/null state; test pending, pass and fail separately across function, JSON and CSV. OVERALL executable PASS must remain distinct from external acceptance.

R2G13's gate name still says `{CONFIRMED 17, REJECTED 7}` while the check and actual claim table use **16/8**. Correct the generated description from the actual tally. This presentation defect does not invalidate the table itself.

## 5. Sidecar semantic scope and remaining test limitations

Byte reconstruction is accepted. One secondary interpretation discrepancy exists: R39 final row retains a bare CR inside the raw EOF line; R2 maps `computed_by` to `"n/a\r"`, whereas Python CSV treats it as a record terminator and yields `"n/a"`. Both layers preserve the original bytes. Explicitly document whether header mapping follows the custom physical-line contract or standard CSV record semantics; do not change raw bytes or call this byte loss.

R2G10 reconstructs bytes well but checks only that strict-row header mapping is a dict, not that its values independently match the source parse. If semantic normalization is claimed, add a field-level check under the chosen contract. Also distinguish semantic UNRESOLVED from byte-reconstruction success in synthetic fixtures. No new manifest format migration is required for this correction.

The 18 historical executable PASS results were inspected, not rerun in-place: running the full checker would overwrite its completed-run output. Independent probes reproduce physical counts, value mismatches, sidecar reconstruction and Git parity. This audit does not claim that a full fresh R2 suite was executed.

## 6. Publication and concurrency

Initial live remote master was 97ed5e54. During the audit another writer pushed **5358d9699abb81364e5be997f016b91db25fdc02**, adding only `PROJECT_OPERATING_MODEL.md`. R2 remains its verified ancestor; no R2 package change was found. The new governance document was read. It does not turn this focused NIF revalidation into a milestone-wide verdict.

Latest read-only Git status: unrelated untracked `docs/audits/PE_MILESTONE_1_WORLD_SURFACE_R1_GATE/`; no tracked modifications reported. Do not include, remove or halt that work. No Git mutation, wiki update, canonical/loop write, original payload edit or shared-tool change was made by this auditor. This new auditor package is LOCAL_ONLY, not committed/pushed.

## 7. Decision and next bounded direction

**REVALIDATION_REQUIRED**, with accepted sub-results retained. One repair package should fix F1, correct F2/F3 wording/state, rerun only the relevant regressions and publish its evidence. No restart of the entire NIF investigation; no fresh morph-boundary research; no automatic wiki application or milestone progression.

Executor handoff direction: `00_CONTROL/OPENCODE_REVALIDATION_PROMPT.md` in this auditor root. It can be relayed through the browser run auditor and formalized by OpenCode per the adopted operating model. It has not been dispatched or executed by this auditor.

`

## VERBATIM: the executed correction direction (OPENCODE_REVALIDATION_PROMPT.md)

`markdown
# NIF R2 focused revalidation — one bounded repair package

External verdict: REVALIDATION_REQUIRED. Formalize this direction in NEXT_PROMPT.md under the NEW run-local 00_CONTROL, retaining the intent, paths, gates and restrictions. If current authority or locks conflict, return CHARTER_BLOCKED instead of silently changing scope. No milestone closure or new research is authorized.

P0 = HASH_PRIMITIVE_VALUE_IDENTITY_BEFORE_AGGREGATE_ACCEPTANCE

## Read before execution

- D:\Eudoria_Reconstruction\AGENTS.md and its six startup context documents.
- Current operating model and external-audit contract; repository conventions at D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\README.md.
- D:\Eudoria_Reconstruction\99_Audits\PE_NIF_R2_POST_AUDIT_20260905_025627\06_REPORT\00_FINAL_REPORT.md
- D:\Eudoria_Reconstruction\99_Audits\PE_NIF_R2_POST_AUDIT_20260905_025627\01_RAW\verification.json and 00_CONTROL\verify.py (read-only reference; independently verify its findings).
- R2 package: D:\Eudoria_Reconstruction\99_Audits\PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054, pinned published commit 97ed5e54f685a5a7ed7a47d761d2b6cc42bfd4b7.
- Referenced R34 per_span raw results, not merely prose summaries.

The audited remote subsequently advanced to 5358d9699abb81364e5be997f016b91db25fdc02 (governance-only). Capture actual current BASE_SHA; never reset to either reference.

## ====================================================================== REPORT / OUTPUT LOCATION

AUDIT_OUTPUT_ROOT = D:\Eudoria_Reconstruction\99_Audits\PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627
FINAL_REPORT_PATH = D:\Eudoria_Reconstruction\99_Audits\PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627\06_REPORT\00_FINAL_REPORT.md
PRIMARY_EVIDENCE_PATHS =
- D:\Eudoria_Reconstruction\99_Audits\PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627\01_RAW\PRIMITIVE_VALUE_COMPARISON.json
- D:\Eudoria_Reconstruction\99_Audits\PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627\02_LOGS\TEST_RESULTS.json
- D:\Eudoria_Reconstruction\99_Audits\PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627\05_ANALYSIS\CLAIM_MATRIX.csv

Check nonexistence before writing. If it already exists, choose a fresh RUN_ID and resolve ALL paths consistently; never reuse/overwrite an earlier run. Required directories: 00_CONTROL (NEXT_PROMPT + one-time scripts/fixtures), 01_RAW, 02_LOGS, 03_STATIC, 04_RUNTIME (NOT_RUN), 05_ANALYSIS, 06_REPORT. Required files: REPORT.md pointer, HANDOFF.md, STAGE_ACCEPTANCE_GATES.csv, artifact_index.csv; final report at the exact resolved FINAL_REPORT_PATH.

## Work and PASS gates

1. Reproduce the extracted R2 helper defects without executing its whole historical script. Adler(empty) is 0x00010000 instead of 1; Adler(a) is 0x00620061 instead of 0x00620062. FNV-1a(hello) is 0xa82fb4a1 instead of 0x4f9f2cab. Verify against the actual bytes of the hash-pinned source. These are counterexamples to test, not auditor assertions to accept blindly.

2. Implement corrected stage-local primitives with explicit algorithm definitions. Adler uses s1=1, s2=0, modulus 65521; FNV uses exact multiply modulo 2^32 (ordinary floating Number multiplication followed by a cast is insufficient). Primary references: RFC1950, RFC9923. Do not edit shared tools/scripts or R2. No pe-toolsmith authority fiction is needed for one-time 00_CONTROL code.

3. Build executable known-answer tests BEFORE corpus aggregation: empty, single byte, multi-byte, binary including zero/high bytes, overflow-sensitive vectors, repeated/incremental inputs where applicable. Compare actual output words, with explicit input bytes, output width/encoding and oracle provenance. Use independent zlib and exact-integer/reference implementation; verify their known vectors too. A second script sharing the same erroneous primitive is not independent.

4. Compare per-entry function VALUES across both hash-pinned Models.bnt corpora, keyed by era + file + candidate + input identity. At minimum cover every tested candidate input affected by the defects: Adler(name), Adler(payload), FNV(name). Compare the other candidate primitives/assembly used by the ten-formula census proportionately. Match-count tables are derived only AFTER primitive/input identity passes. Record exact values or bounded metadata plus complete mismatch census; do not publish original payload bytes.

5. Negative controls MUST fail: unchanged R2 helpers; a deliberately wrong-value implementation preserving aggregate zero-match counts; pending-as-false serialization. Capture actual failed predicate/exit results, not hand-written FAIL_DETECTED labels. Correct code must pass the same predicates. Internal iterations inside this one bounded run are allowed; significant run boundary remains external gate.

6. Recount the nine-zero/CRC-subset results with corrected primitives. Preserve physical result if unchanged; retract only unsupported method assurances. Record that independent Python already confirmed the aggregate numerical result, whereas Node was not computing the named functions correctly. Supersede R2G8 and affected C2-B/C2-E method claims and report/handoff wording; do not erase historical evidence.

7. Repair two bounded non-research inconsistencies in the new package:
   - P1R2-5: 334 is the classifier-real residual of VARIABLE-K, not all tested grammars. Re-sum R34 per_span: 62 have another recorded fit; 272 have none among the recorded alternatives. Include a concrete counterexample; do not promote alternative fits to true segmentation. Correct replacement wording. Avoid presenting all 21 R35 claims as 100% fits; retain exact claim IDs, denominators and evidence statuses.
   - Preserve human-review pending/null distinctly from fail and pass through the gate function, JSON, CSV and report. R2 bool(None) produced false/FAIL. Test all three states. Derive tally labels from actual rows (R2G13 says 17/7 but actual is 16/8). Executable OVERALL PASS never means human acceptance.

8. Preserve the accepted 12/12 byte-lossless sidecars. If semantic header normalization is restated, document bare-CR policy explicitly (R39 final row maps n/a plus CR under the custom line contract vs n/a under CSV record parsing) and independently compare mapped fields under that policy. This is NOT raw-byte loss and is not permission for a wholesale manifest migration.

9. Produce finding dispositions, claim matrix, supersession map, corrected proposals ONLY, negative/positive test evidence, source hashes and command logs. Each important PASS includes measured quantity, denominator, independent source of truth, why non-circular and detected failure case. Use deterministic assertions with nonzero failure exit. Keep source-inspection, physical recomputation and historical-result re-sums clearly separate.

## Scope / no-write boundaries

READ-ONLY: original game files, all historical run directories, R2, wiki/docs/nif, canonical/vault/index, PE_AUTO_LOOP, shared tools/scripts, runtime code. No game/Ghidra launch, no morph-boundary research, no leaf/XYZ, no MAPRE or milestone promotion, no automatic wiki application. Only new run-local work and its bounded repository publication are permitted. Do not spawn nested agents or stop another writer.

## Remote audit package and handoff

Repository SebastianKozlo/eudoria-clean, master; local clone D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean.
Publish this run only at docs/audits/PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627/ (use collision-resolved RUN_ID if needed). Persist the full external post-audit and its correction direction in the new package as EXTERNAL_REVIEW.md/reference with hashes; do not rewrite R2 history. Respect the current three-tier relay/formalization workflow.

Commit only the new bounded package, report, code, tests, gates, manifest and safe metadata. NEVER publish original Models.bnt, NIF/executable payloads or complete dumps. Original evidence is era/build + canonical local path + size + SHA256 + reproduction method.

Recheck status. Exclude unrelated untracked docs/audits/PE_MILESTONE_1_WORLD_SURFACE_R1_GATE/ and any new concurrent changes. Explicit-path staging, no blanket add, no forced push/reset. Capture BASE_SHA, commit, push, verify remote commit/ancestry and package blob parity; record final publication HEAD_SHA in handoff (do not create self-referential commit hashes). If concurrent movement or permissions block safe publication, report EXTERNAL_AUDIT_INCOMPLETE; never fake CLEAN/READY. No global Git/TLS configuration change.

HARD STOP after this corrected published package and handoff. Wait for independent revalidation before proposals are applied. No next milestone or unbounded loop.

Mandatory final local handoff:
AUDIT_OUTPUT_ROOT = <resolved full path>
FINAL_REPORT_PATH = <resolved full path>
PRIMARY_EVIDENCE_PATHS = <actual full paths>
RUN_STATUS = COMPLETED / PARTIAL / FAILED / BLOCKED / ABORTED
HARD_STOP_REASON = <exact reason>

EXTERNAL AUDIT HANDOFF:
RUN_ID / ITER / MILESTONE (EU935-M2 contribution; no advancement)
REPOSITORY / BRANCH / BASE_SHA / HEAD_SHA
PUSH_STATUS = PUSHED / REMOTE_SYNC_PENDING / EXTERNAL_AUDIT_INCOMPLETE
REPORT_PATH / HANDOFF_PATH / GATES_PATH / EVIDENCE_MANIFEST_PATH (repository-relative)
FILES_CHANGED / PRIMARY_CLAIMS / RETRACTIONS_SUPERSESSIONS / OPEN_UNRESOLVED
TESTS_EXECUTED / LOCAL_ONLY_ORIGINAL_SOURCES (description, era, size, SHA256)
PREEXISTING_UNCOMMITTED_WORK / WORKING_TREE_STATUS = CLEAN or NOT_CLEAN
EXTERNAL_AUDIT_READY = YES or NO (publication completeness, not scientific acceptance)

`

## Note on the external verifier

The external post-audit's own reproducer (verify.py, hashed above) executed only
the two literal pure helper declarations extracted from the hash-pinned R2
source — the same discipline this run follows (00_CONTROL/probe_r2_helpers.cjs).
Its measured values (verification.json, hashed above) are consistent with this
run's independent measurements; R3 extends them with the complete per-payload
adler census (11022/11022), the identified 6 FNV coincidence inputs, the
executed-R2-crc32 positive control, and the wrong-value aggregate-preservation
demonstration.
