# FINAL_REPORT — PE_GAMEBRYO_ORACLE_F1_C1_EXTENSION_HALT_R1_20261003

```text
RUN_ID            = PE_GAMEBRYO_ORACLE_F1_C1_EXTENSION_HALT_R1_20261003
REPO              = D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean
BASE_SHA          = 60a73d9b0cc438b2cf71eed827b28f2806fc03e5
RUN_CLASS         = LOAD_BEARING
RUN_TYPE          = DESKTOP_POST_AUDIT_FOCUSED_CORRECTION (F1-C1 only)
EXECUTOR          = pe-reconstruction (PE-MASTER direct dispatch, NO_NESTED_TASKS)
QC_SCOPE          = SELF_CHECK_F1_C1 (no independent reviewer agent available; independence discipline: expectations derived from the pinned source + the Desktop finding's counterexample description BEFORE the fix; counterexamples reproduced PRE-fix on raw records, re-executed POST-fix through the CLI, battery-verified)
SOURCE_ORACLE     = NiStream.cpp SHA256 E955C36EBBB442029E00BE8A154726741B8454A607F2DC043F1FD542B009DC25 (verified at run start; 38,458 B; L70 MAX_RTTI_LEN=256 + L1150 assert re-read this run)
```

## 1. Mission

Fix ONLY Desktop finding F1-C1/P2 (from
`PE_GAMEBRYO_ORACLE_F1_DESKTOP_POST_AUDIT_20261003`, REPORT.md SHA256
`6BD89E93...`; audited commit 60a73d9; verdict REQUIRE_CORRECTIONS): after
an earlier source-predicted RTTI factory miss, a late RTTI-name DecodeError
under `--full-decode` only appended `EXTENDED_TABLE_READ_FAILED` and broke
the name loop; parsing then continued into the object indices — the
leftover bytes of the unfinished name were interpreted as indices/groups/
bodies although the RTTI table boundary was undetermined. Two failure
shapes: a traceback/lost JSON (IndexError at the histogram loop) and a
spurious object reconstruction out of the unfinished name's bytes.

The contract for the fix: when `first_miss_table_index` is established AND
`--full-decode` is active AND a later RTTI name raises DecodeError —
keep the earlier source-predicted RTTIError (SOURCE_PREDICTED verdict =
REJECTED; a later parser error must NOT replace it), keep FIRST_RTTI_MISS
and names_read, set `full_table_read=false`, record an explicit
distinguishable extension failure/halt marker (STOP_AT_TABLE_FAILURE, NOT
CONTINUE_FROM_UNKNOWN_OFFSET), read NO object indices, create NO
object_reference_histogram/census, read NO object groups, decode NO
bodies, attempt NO scanning/resynchronization, return structured JSON
immediately, CLI exit != 0.

## 2. The fix (change set — minimal, F1-C1 only)

`tools/gamebryo_oracle/gb12core.py` (the ONLY functional change; diff hunk
map: 4 hunks — the header doc block + 3 inside the b_new RTTI region):

- The name-loop DecodeError handler (after an established first miss) now
  records `extension_table_failure = str(e)` (alongside the existing
  `EXTENDED_TABLE_READ_FAILED` warning) before the `break`.
- A new halt block placed AFTER the first-miss verdict block and BEFORE
  the object-index stage: if `extension_table_failure` is set, the
  extension records `rtti_table_validation.extension_halt` (marker
  `STOP_AT_TABLE_FAILURE`, `halted_at_table_index` = names_read,
  `table_boundary_determined: false`, detail, and an explicit
  `continuation: "NONE: ... NOT CONTINUE_FROM_UNKNOWN_OFFSET"` string)
  plus the top-level `extension_halt = "STOP_AT_TABLE_FAILURE"` key and an
  `EXTENSION_HALT: STOP_AT_TABLE_FAILURE` warning, and RETURNS the
  structured JSON IMMEDIATELY. The load_result already carries the
  source-predicted `RTTIError(<first table miss>)`, `accepted=false`,
  `partial=true`, `decode_continued_after_rtti_gate=true` and the
  first-miss unknowns — a later parser error does NOT replace the earlier
  RTTIError. No object index is read, no
  object_reference_histogram/object_reference_census key is produced, no
  object group is read, no body is decoded, no closure scanning is
  attempted. CLI exit = 2 (!= 0).
- The index-stage halt (`EXTENDED_INSPECTION_HALTED`, for a FULLY-read
  table whose indices fail) is untouched and remains a SEPARATE,
  distinguishable halt (fires later, at a PROVEN table boundary).

Non-critical property proven (QC + T1): on non-halt paths the fix adds
ZERO output — the T1 full-decode JSON is byte-identical to the 60a73d9
output (SHA256 of the CRLF-normalized stdout/`--out` text:
`DD19B1C3F036AE7BBB6D53C365F4BC84B0F9B673252BDC139E9B8D8844A5CD45`,
matching the historical AFTER_FIX_G record's stdout).

Also updated: `schemas/oracle_result.schema.json` (one new optional key
`extension_halt`), `tests/test_gb12.py` (permanent F1-C1 battery, 10 new
controls), `README.md` (--full-decode + Tests honesty wording). Registry
UNCHANGED. Legacy `< 5.0.0.1` inline-RTTI layout NOT migrated. F2-F7
untouched (scope guard).

## 3. Mandatory counterexamples (raw records in 02_RAW_TESTS/)

Fixtures built by OUR OWN committed deterministic generator
(`01_FIXTURES/build_fixtures_c1.py`; SIZE+SHA256 pins in
INPUT_IDENTITIES.md; physical files NOT committed per the repo-wide
`*.nif` policy, preserved in the external sandbox). Both fixtures came out
byte-identical to the Desktop auditor's own counterexamples (94 B /
`928A1447...` and 196 B / `719A7EB3...`), constructed from the same
pinned-source description — cross-validated twice against the independent
auditor's bytes.

| test | pre-fix (pinned 60a73d9 code, raw) | post-fix (final code, raw) | verdict |
|---|---|---|---|
| A: TRUNCATED RTTI NAME + INDEX-LIKE REMAINING BYTES (`fx_C1A`, table [NiNode, NiDesktopFirstMissing(miss@1), <3rd name len=127, 2 bytes `02 00`>], n_obj=1) | `--full-decode`: leftover name bytes consumed as the VALID type index 2; `type_names[2]` IndexError at gb12core.py L1561; traceback, EMPTY stdout, exit 1 (PRE_FIX_C1A_full_decode) | accepted=false, error_code=RTTIError, RTTIError(NiDesktopFirstMissing) preserved, first_rtti_miss=NiDesktopFirstMissing@1, names_read=2, full_table_read=false, extension_halt=STOP_AT_TABLE_FAILURE (halted_at_table_index=2), objects=[], NO histogram/census/groups, structured JSON emitted, exit 2 (POST_FIX_C1A_full_decode) | PASS — the traceback/lost-JSON counterexample REJECTED |
| B: TRUNCATED RTTI NAME + FAKE-BODY-LIKE REMAINING BYTES (`fx_C1B`, same table, 104 crafted bytes = index 0 + groups 0 + 90-byte NiNode body + valid footer) | `--full-decode`: SPURIOUS NiNode object (byte_start 98, inside the unfinished-name region), histogram {NiNode:1}, census, groups, roots=[0], count-match=true, accepted=false (the data origin was wrong) (PRE_FIX_C1B_full_decode) | same earlier RTTIError preserved, objects=[], NO histogram/census/groups, NO roots, NO object_count_check, unknowns = the first-miss record only, extension halted at the table failure, structured JSON, exit 2 (POST_FIX_C1B_full_decode) | PASS — the fake-object counterexample REJECTED |
| ordinary mode (both fixtures) | correct RTTIError(NiDesktopFirstMissing) at the first miss, nothing read past it, exit 2 (PRE_FIX_C1*_ordinary) | BYTE-IDENTICAL stdout and exit code pre/post fix (QC check ce_*_ordinary_bytes_identical) | PASS — ordinary semantics UNCHANGED |
| STOP vs CONTINUE distinction | (the pre-fix behaviors WERE the CONTINUE_FROM_UNKNOWN_OFFSET defect) | both classes assert `marker=STOP_AT_TABLE_FAILURE`, `table_boundary_determined=false`, `continuation` starting `NONE:` + containing `NOT CONTINUE_FROM_UNKNOWN_OFFSET`, NO index-stage `EXTENDED_INSPECTION_HALTED` warning, and absence of every continuation artifact (objects/histogram/census/groups/roots/edges) | PASS — distinguishable marker, no continuation |

## 4. Regression: existing F1 controls A–F/C2 + ordinary semantics

- Full battery `tests/test_gb12.py --self` (11 original self-tests + 8 F1
  controls + 10 new F1-C1 controls): **0 failures** (raw:
  `03_QC_SELF_CHECK/FINAL_self_and_f1_and_f1c1_battery.stdout`).
- Fixture F (first table miss + truncated later name, ends exactly at the
  u32 length) STILL PASSES its battery control
  (`f1_full_decode_extension_failure_never_masks_source_verdict`:
  RTTIError(NiXyzzyx) preserved, partial=true,
  EXTENDED_TABLE_READ_FAILED warning present). EXPECTED, F1-C1-justified
  delta on the CLI raw record: F full-decode now halts AT the table
  failure (`extension_halt=STOP_AT_TABLE_FAILURE`, halted_at 2) instead
  of at the object-index stage (`EXTENDED_INSPECTION_HALTED` at EOF) —
  the Desktop report explicitly identified F's shape as the one that
  MASKED the C1 hole (its index-stage read happened to fail at EOF);
  F alone is NOT claimed as F1-C1 closure evidence (the new A/B
  counterexamples are). Raw: PRE_FIX_F_full_decode vs
  POST_FIX_F_full_decode.
- Payload control battery (T1 sandbox copy): 2 failures
  (`object_count_mismatch_detected`, `link_failure_detected`) —
  PRE-EXISTING, proven so by execution this run: the identical failure
  set with identical detail strings was re-produced under the STASHED
  pre-fix code (PRE_FIX_payload_battery_T1_copy.stdout). These controls
  can only fire after a body/count phase that an RTTI-failing payload
  never reaches in ordinary mode (F2-adjacent battery limitation,
  documented by the F1 run §7; NOT widened into scope here).

## 5. T1 regression (identity verified before use: 57,316 B, SHA256
`3E8A22C2213202207E374B55CD65B2C3BE039CCDD1E8D01A07FCAF44DE12CF36`)

- `objects[]` DEEP-IDENTICAL vs the pinned baseline
  (`PE_GAMEBRYO_ORACLE_TOOL_R1_20261003/.../inspect_T1_gb12_full.json`):
  **66/66 records**, every field compared recursively (values,
  names/types/status, local transforms, links, byte_start, byte_end,
  byte_size and all other recorded fields; per-record identical count
  66/66, zero diffs) — raw: `04_REGRESSION/T1_REGRESSION_COMPARISON.json`
  (VERDICT PASS).
- Interpretation label PRESERVED EXACTLY: **62 known semantically decoded
  records + 4 opaque/boundary-only records** (the 4 = indices 1, 2, 3, 13,
  the NiArk* UNREGISTERED boundary-only blocks). The 66/66 record
  identity is NOT promoted to 66 semantic decodes.
- FIRST_RTTI_MISS = `NiArkAnimationExtraData` @ table index 1 (PRESERVED);
  SOURCE_PREDICTED verdict = REJECTED (PRESERVED);
  WORLD_PLACEMENT_RECOVERED = NO (T1 remains MODEL_LOCAL — no placement
  research was executed in this run).
- Determinism: full-decode re-run byte-identical (run1 == run2, SHA256
  `DD19B1C3...`); ordinary mode byte-identical to the 60a73d9 record AND
  verdict-identical to the published pre-F1 ordinary baseline
  (`RTTIError(NiArkAnimationExtraData)`, accepted=false, exit 2).
- Stronger whole-JSON identity: the post-fix T1 full-decode output is
  byte-identical (CRLF-normalized) to the 60a73d9-era CLI stdout — the
  F1-C1 fix adds ZERO output on non-halt paths.

## 6. QC (SELF_CHECK_F1_C1; executor self-check, NOT independent QC)

`03_QC_SELF_CHECK/qc_reexecution.py` re-executes BOTH counterexample
classes through the ORACLE CLI (independent of the in-memory battery) and
checks 21 controls: fixture byte identity (battery bytes == generator
files), all POST-FIX contract requirements per class, the
STOP_AT_TABLE_FAILURE vs CONTINUE_FROM_UNKNOWN_OFFSET distinction,
ordinary-mode byte-identity pre/post, the PRE-FIX raw defect shapes
(C1A traceback + empty stdout + exit 1; C1B spurious object + histogram +
census + groups + roots), and the F-fixture delta. **21/21 PASS,
QC_VERDICT = SELF_CHECK_QC_PASS** (raw:
`03_QC_SELF_CHECK/QC_REEXECUTION_COUNTEREXAMPLES.json`).
Critical non-circular property (restated): after an incomplete RTTI table
read there is NO proven boundary for the start of object indices — the
fix never guesses it from remaining bytes; the extension stops at the
table failure.

## 7. Scope guard compliance

F2 (acceptance/coverage/link predicates): NOT touched. F3 (compare): NOT
touched. F4 (general exception framework; presolver trailing-run
IndexError): NOT touched (the pre-first-miss `raise` behavior is
unchanged; the presolver defect territory is untouched). F5-F7: no
corrections (only the F1-C1 wording supersession recorded here + the
AUDIT_ENTRYPOINT row). No Gamebryo class loaders added. T3: NOT run.
Corpus-wide decode: NOT run. PCG placement RE: NOT run. Registry:
UNCHANGED. Legacy inline-RTTI layout: NOT migrated. The historical F1
package: READ-ONLY (fx_F regenerated in THIS package instead). Foreign
untracked paths (PE_935_* dirs, experiments/): untouched, not staged.

## 8. Supersession record (explicit)

- The historical 60a73d9 F1 verdict = **REQUIRE_CORRECTIONS** (the Desktop
  post-audit of 2026-10-03, finding F1-C1/P2). The historical run's own
  blanket claims ("no material findings", full F1 FIXED_AND_VERIFIED,
  "a later parser failure always halts and never masks the source
  verdict") are superseded FOR THE AUDITED STATE by this finding.
- The ordinary table-order fix of the historical run = **PRESERVED**
  (byte-identical ordinary outputs on the counterexample fixtures and on
  T1; full battery A–F/C2 still passes; fixture F still passes).
- F1-C1 = **the result of THIS run** (FIXED_AND_VERIFIED per the terminal
  fields below; commit is not scientific PASS — the evidence is the raw
  pre/post counterexample records + battery + T1 deep regression).
- F1_RTTI_TABLE_SOURCE_ORDER overall = PARTIAL at 60a73d9 per the
  Desktop verdict; after this run the table-order fix (preserved) AND the
  extension table-failure halt (fixed) stand together.

## 9. Persistence

Path-limited commit + fast-forward push (see HANDOFF.md for SHAs; the
foreign untracked paths were NOT staged; `git add .` NOT used). Repo
policy compliance: the three synthetic fixtures are NOT committed
(repo-wide `*.nif` gitignore, zero NIF files tracked — same convention as
the published runs); the committed generator regenerates them
byte-identically; physical copies preserved in the external sandbox
(`D:\Eudoria_Reconstruction\99_Audits\
PE_GAMEBRYO_ORACLE_F1_C1_EXTENSION_HALT_R1_20261003\sandbox\`). No SDK or
proprietary game payload committed. The output package was finalized
(all records from the final code), then MANIFEST_SHA256.csv was generated
over the committed package content LAST and the bijection physical files
minus manifest <-> manifest rows verified before the commit.

## 10. Terminal fields (exact)

```text
F1_ORDINARY_TABLE_ORDER = PRESERVED
F1_C1_EXTENSION_TABLE_FAILURE_HALT = FIXED_AND_VERIFIED
F1_OVERALL = FIXED_AND_VERIFIED
F2_TO_F7 = NOT_ADDRESSED_IN_THIS_RUN
TRACEBACK_COUNTEREXAMPLE = REJECTED
FAKE_OBJECT_COUNTEREXAMPLE = REJECTED
STRUCTURED_JSON_ON_EXTENSION_TABLE_FAILURE = YES
T1_PHYSICAL_IDENTITY = PASS
T1_66_OBJECT_RECORD_DEEP_REGRESSION = PASS
T1_62_KNOWN_4_OPAQUE = PRESERVED
GENERAL_ORACLE_FAIL_CLOSED = NOT_ESTABLISHED
GENERAL_SOURCE_EQUIVALENCE = NOT_ESTABLISHED
T3_COMPLETION_EXECUTED = NO
NEW_PCG_TRACE_EXECUTED = NO
WORLD_PLACEMENT_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
NEXT_RUN_EXECUTED = NO
```

QC verdict rationale: every F1-C1 contract requirement is verified by raw
pre/post CLI records + a 21-check CLI re-execution + the battery + the T1
deep regression; no in-scope defect remained at capture time. FINDINGS
carried forward honestly: (1) the 2 PRE-EXISTING payload-battery controls
(proven identical pre/post by execution) remain an F2-adjacent battery
limitation; (2) the fixture-F full-decode raw record CHANGED (expected,
F1-C1-justified: the halt now fires at the table failure instead of at
the index stage); (3) QC is executor self-check only — no independent
reviewer was available in this session.
