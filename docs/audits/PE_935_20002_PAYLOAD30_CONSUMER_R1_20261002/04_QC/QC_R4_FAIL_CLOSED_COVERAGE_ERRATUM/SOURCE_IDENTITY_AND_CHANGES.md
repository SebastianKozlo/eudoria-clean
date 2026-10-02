# SOURCE_IDENTITY_AND_CHANGES — QC-R4 fail-closed validator repair

- RUN_ID: PE_935_20002_PAYLOAD30_QC_R4_FAIL_CLOSED_CORRECTION_R1_20261002
- Written by: pe-reconstruction (executor; PE-MASTER direct dispatch; NO_NESTED_TASKS)
- Scope of this record: the source identity of the QC-R4 revision tools vs the immutable
  QC-R3 originals, and the line-referenced list of the ONLY behavioral changes
  (RUN_CONTRACT §2, requirements R1-R12).

## 1. Source identities

| File | Size (B) | Lines | SHA256 | Role |
|---|---|---|---|---|
| OLD validator `04_QC\QC_R3_DESKTOP_CORRECTION\qc_tools\qc3_q1_pinverify.py` | 18,199 | 308 | C354E559B99411DB3AD926577B4C6C8DF5A287B3D19C47B2832BCBC104089F0F | the F1 fail-open defect carrier — IMMUTABLE, byte-unchanged, not executed by this run |
| NEW validator `04_QC\QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM\qc_tools\qc4_q1_pinverify.py` | 30,772 | 548 | 345D69FA6CEC60590F79B97FFE73F29538BEAF6704C5A5B9F7D14192DB8157A8 | the repaired copy (this run's deliverable) |
| OLD helper `04_QC\QC_R3_DESKTOP_CORRECTION\qc_tools\qc3_pe32_x86.py` | 20,432 | 520 | FE0C2F2BEC51504C6A332DCE6C0C54B872A9F32D05D7242D897F5B4E4C819DD6 | the PE32 parser + x86 decoder — IMMUTABLE, byte-unchanged |
| NEW helper `04_QC\QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM\qc_tools\qc4_pe32_x86.py` | 20,432 | 520 | FE0C2F2BEC51504C6A332DCE6C0C54B872A9F32D05D7242D897F5B4E4C819DD6 | **BYTE-IDENTICAL COPY** of qc3_pe32_x86.py (hashes equal; copied with a byte-exact file copy; zero changes) |
| NEW harness `04_QC\QC_R4_FAIL_CLOSED_COVERAGE_ERRATUM\qc_tools\qc4_regression_runner.py` | 27,271 | 536 | E8B01077AE5AD31259FA16CAC27B00A6723F02A99D8EB4C0896E9E531E33DCE5 | new file (no QC-R3 counterpart): fixture build + both regressions + verification + summary |

- The QC-R3 sources are preserved byte-unchanged (re-hashed at executor close; see
  QC_R4_REPORT.md §Hygiene). No QC-R3 output was overwritten (R6/R7: the repaired
  validator's results are NEW artifacts at POSITIVE\ and INVALID_VA\ inside the new revision).

## 2. qc4_pe32_x86.py identity statement

BYTE-IDENTICAL to qc3_pe32_x86.py (SHA256 FE0C2F2BEC51504C6A332DCE6C0C54B872A9F32D05D7242D897F5B4E4C819DD6,
20,432 B, 520 lines). No change was needed, therefore none is justified. R12 (bytecode
disabled) for this helper is operationalized WITHOUT editing it: every qc4 script sets
`sys.dont_write_bytecode = True` as its first statements BEFORE importing the helper, and the
regression runner sets `PYTHONDONTWRITEBYTECODE=1` in every subprocess environment; the
package-wide `__pycache__` absence was verified after all runs (0 directories anywhere under
the package). The helper is only ever imported by qc4_q1_pinverify.py, whose first statements
disable bytecode writing first.

## 3. Line-referenced change list — qc3_q1_pinverify.py -> qc4_q1_pinverify.py

Everything NOT listed here is semantically IDENTICAL to the original (R11): the same
four-artifact pin loading (pins[] with entry_pins fallback, then width_sources.<key>.width_pins[]),
the same verify_pin field semantics and comparisons, the same extra checks (incl. the BSS-tail
factory note), the same 19 semantic windows with identical ranges, the same 51 semantic
assertions with identical predicates and details, the same stdout summary intent.

| Old line(s) | New line(s) | Change | Requirement |
|---|---|---|---|
| L1-L4 (header) | L1-L36 | header replaced: documents the F1 defect and the R1-R12 repair items | documentation |
| — | L37-L38 | `import sys` / `sys.dont_write_bytecode = True` as the FIRST statements | R12 |
| L5 `import json, os, sys, struct` | L40 `import argparse, hashlib, json, os, struct` (+`sys` moved to L37) | argparse + hashlib added for the CLI (R9) and the EXE hash (R10); `struct` retained from the original (unused there too — import identity preserved) | R9, R10 |
| L6 (sys.path.insert) | L41 | unchanged behavior | — |
| L7 `from qc3_pe32_x86 import ...` | L42 `from qc4_pe32_x86 import ...` | import retargeted to the byte-identical helper copy | — |
| L9-L12 (PKG/QC_DIR/RAW_CORR/EXE hard-coded) | L44-L45 (only EXE + new EXPECTED_EXE_SHA256) | the QC-R3 package/output paths are REMOVED (R9: no inherited hard-coded output path); the pinned EXE path stays + its expected SHA256 pin is added | R9, R10 |
| L14 `pe = PE32(EXE)` (unconditional) | L139-L172 | `pe` is now constructed inside main() ONLY after the R10 EXE identity hash check passes; on mismatch/unreadable EXE: run-level error, overall_ok=false, nonzero exit | R10 |
| L15-L16 (res dict) | L143-L147 | res gains `run_id`, `inputs`, `exe_identity`, `run_errors`; `exe_sha_note` (a static note) is REPLACED by the actually-measured `exe_identity` record | R10 |
| — | L52-L58, L60-L69, L71-L88 | new: sha256_file, parse_args (--inputs / --output), resolve_inputs (directory of the four canonical names, or the four explicit file paths; fail-closed on anything else) | R9, R10 |
| L18-L22 (sec_for_fo) | L90-L95 | IDENTICAL | — |
| L24-L45 (verify_pin) | L97-L119 | IDENTICAL verification semantics/fields | — |
| L47-L59 (artifact loading, no error handling) | L121-L137 + L174-L195 | pin enumeration extracted into enumerate_artifact_pins with stable `pin_id` per pin ("<artifact-name>::<array_path>[<index>]" over pins[] / entry_pins[] / width_sources.<key>.width_pins[]); artifact loading is now fail-closed (missing file / unparsable JSON -> run-level error, overall_ok=false, nonzero exit) | R8, R10 |
| — | L196 `original_input_pin_count = len(enumerated)` | ORIGINAL_INPUT_PIN_COUNT captured BEFORE any verification | R1 |
| **L60-L64 (THE FAIL-OPEN DEFECT: per-pin try/except appended to res["errors"] and the pin VANISHED from res["pins"])** | L198-L246 | every enumerated pin now produces exactly one result row: verified rows carry the full verify_pin record (+ pin_id, status); a per-pin exception produces an explicit FAILED row (pin_id + source + original VA string + error string retained) that STAYS in the result set and the denominator | R2, R3 |
| L66 `total = len(res["pins"])` (post-drop denominator) | L248 `denominator = len(rows)` | the denominator now counts EVERY input pin incl. FAILED rows | R2, R3 |
| — | L250-L258 | identity-set bijection input pins <-> result rows (no duplicates, no drops; counters alone insufficient) | R8 |
| L79-L131 (extra checks) | L260-L313 | IDENTICAL extra checks (incl. the BSS-tail factory note); wrapped in `if pe is not None` (skipped only in the already-failing EXE-mismatch branch) | — |
| L133-L147 (dump_window) | L315-L329 | IDENTICAL | — |
| L149-L167 (19 dump_window calls) | L331-L349 | IDENTICAL (same 19 windows, same ranges), wrapped in `if pe is not None` | — |
| L169-L172 (assert_sem) | L351-L357 | IDENTICAL | — |
| L174-L292 (51 assertions) | L359-L474 | IDENTICAL (same 51 assertions, same predicates/details), wrapped in `if pe is not None` | — |
| L293-L297 (semantic census) | L476-L484 | IDENTICAL counting; also exposed per census."semantic_assertions" | — |
| **L298 (overall_ok = ok_count == total AND sem AND extra — errors and the input-pin count IGNORED)** | L487-L496 | overall_ok now requires SIMULTANEOUSLY: exe_identity ok AND no run_errors AND processed_count == ORIGINAL_INPUT_PIN_COUNT AND verified_ok == ORIGINAL_INPUT_PIN_COUNT AND mismatch_count == 0 AND error_count == 0 AND bijection_ok AND all semantic assertions PASS AND all required extra checks PASS | R4 (+R8, R10 folded in) |
| L68-L77 (census claimed/ok/mismatch) | L500-L523 | census now carries the machine fields: input_pin_count, processed_count, verified_ok, failed_count, mismatch_count, error_count, denominator, result_row_count, bijection_ok, mismatch_list, per_artifact (claimed/processed/verified_ok/failed/mismatch/error), semantic_assertions, extra_checks, overall_ok | R1-R4, R8 |
| **L300-L302 (hard-coded output `QC_DIR\QC_R3_PINVERIFY_RESULT.json`)** | L524-L527 | output written to the EXPLICIT --output path (parent dir created if missing) | R9 |
| L303-L308 (print summary; NO exit code logic) | L528-L544 | richer stdout summary + `sys.exit(0 if overall_ok else 1)` | R5 |

## 4. The ONLY behavioral changes (proof of scope)

The change list above touches exactly the R1-R12 items:
R1 (input-pin count captured before verification), R2/R3 (FAILED rows retained in the
denominator), R4 (the overall_ok predicate), R5 (exit codes), R8 (pin identities + bijection),
R9 (explicit --inputs/--output), R10 (EXE identity check + fail-closed artifact/pin handling),
R12 (bytecode disabled). The one-label-per-change mapping is in §3. Everything else —
the loading semantics, verify_pin comparisons, extra checks, the 19 windows, the 51
assertions — is a verbatim transcription from the original (checked side-by-side during
the copy; the fresh internal QC independently full-reads both sources per RUN_CONTRACT §9).

Deviation notes (honest, none weakens a requirement):
- The directory form of --inputs accepts a directory that CONTAINS the four canonical
  artifact names and ignores any other files in it (required by the §3 layout itself:
  FIXTURE_INVALID_VA\ also holds FIXTURE_DIFF.json while being the --inputs of
  Regression B). The four canonical artifacts are always loaded BY NAME; a missing one
  is a fail-closed run error. The four-explicit-paths form requires exactly the four
  canonical basenames.
- overall_ok additionally requires bijection_ok and the absence of run_errors: these are
  the R8/R10 fail-closed conditions folded into the single R4 predicate (strengthening, not
  weakening: counters alone must not permit a dropped or duplicated row).
- The old census key names (claimed_pin_total_in_artifacts / my_verified_ok /
  my_mismatched) are superseded by the §13 census fields; the old names are NOT emitted
  (in qc3 they denoted post-drop values — keeping them would be ambiguous).

## 5. In-run repair history (both regressions re-run from scratch after each fix)

1. First harness execution: both regressions produced all expected values, but the
   harness's own byte-level self-check failed (my harness predicate wrongly required 10
   changed bytes; "0x00977807" -> "0xFFFFFFFF" share the "0x" prefix, so exactly 8 bytes
   change). Harness predicate fixed (qc4_regression_runner.py only; the validator was NOT
   touched), fixture + BOTH regressions + summary regenerated wholesale.
2. Second execution: all green; then a census self-review found the new per-artifact
   `processed` counter was never incremented (showed 0 while claimed/verified_ok/error
   were correct). Validator fixed (qc4_q1_pinverify.py +3 lines); fixture + BOTH
   regressions + summary regenerated wholesale again.
3. Third (final) execution: POSITIVE and INVALID_VA both PASS every §4/§5 expected value;
   harness failures 0; the final identities in §1 are the post-fix ones. The result JSONs
   were regenerated wholesale each time (no partial edits).
