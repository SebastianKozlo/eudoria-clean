# BATCH_C1_RETURN — PE_GAMEBRYO_ORACLE_TOOL_R1_20261003 (correction round C1)

- ASSIGNMENT_MODE: PE-MASTER direct dispatch (C1 redispatch after the empty
  child L25 event; PE-MASTER verified ZERO disk changes before redispatch).
  NO_NESTED_TASKS respected; no agent launched; no loop state touched; NO
  git operations.
- PARENT_LOOP_ID: 8f0ef23a-964b-4767-ac59-1ec593a1b118
- SCOPE: the six mechanical QC_PARTIAL fixes only. No scientific re-run:
  no verdict was altered; FIX-1 re-executed control code paths for OUTPUT
  CAPTURE, and every honest per-payload result (including non-detections)
  is recorded raw.
- BUDGET_USED: 25/25 tool calls (at cap, disclosed); ~40 wall minutes of
  <= 45. All spawned python processes completed and exited (PIDs bounded by
  the tool timeouts; no background writer remains). Sandbox copies stay
  LOCAL_ONLY in C:\Users\User\AppData\Local\Temp\opencode\
  c1_gb_oracle_controls\ (outside the repo).

## PER-FINDING DISPOSITION

### FIX-1 (controls/ persistence) — DONE
New dir docs/audits/PE_GAMEBRYO_ORACLE_TOOL_R1_20261003/04_EVIDENCE/controls/
with the five mutation-control raw outputs as JSON (mutation + check logic
copied verbatim from tools/gamebryo_oracle/tests/test_gb12.py, sha256
323AAA6245605A191EF335A32397418F579A580C1DA86D686699D97C25F2289B; runners
04_EVIDENCE/scripts/c1_control_persist.py + c1_followup.py +
c1_complete.py + c1_verify_annotate.py). Each JSON carries
MEASURED_QUANTITY / INDEPENDENT_SOURCE_OF_TRUTH / WHY_NON_CIRCULAR /
FAILURE_CASE_DETECTED + per-payload runs with raw decode outputs. All runs
on SANDBOX COPIES only; pins verified before use (T1
3E8A22C2213202207E374B55CD65B2C3BE039CCDD1E8D01A07FCAF44DE12CF36, T2
9CFF776D204AEC7B64377DD365AC11A71C9DCFA4A00A5905E642EE7420D5DC28, STOCK
F26FB84346E32BE94AFD9FD3C62DA18FB49308480D7EC38476A216520F6DAC8F;
SDK:2310 sha recorded inside its run entry).

| control JSON | sha256 | DETECTED on | honest non-detections |
|---|---|---|---|
| corrupted_header_version.json | 4D7E9C1A99B814EE7D7E6B4ED44DF72C79AF2A211EF55E630ADE0405C2911C1A | T2, T1, STOCK | none |
| corrupted_midfile.json | 32EB2DF29205AFAE735CE5198324C31A19B8DB9F0192403C58C513BEDF791F2C | T2 | STOCK = verified data-region artifact (see RESIDUAL-1/2); T1 not run (wall-risk note) |
| unknown_class_mutation.json | 84B59AD2ED59E8D19B8D81BF187B6AA34DF91B98AC7E4FFC038ADE7262E7D2A7 | T2, T1, STOCK | none |
| link_failure_mutation.json | 033219DDFAFA484B1997B086EC9D7362F2550F5386337373C0CA28EF0DC0F0CC | SDK:2310 HN (Plane).nif | T1 = RTTI-gate stop before link phase (fail-closed); STOCK = verbatim find() footer num-top collision -> DecodeError (fail-closed exception); T2 not applicable (no NiNode w/ children) |
| object_count_mutation.json | 325AADC8738C0A7B0796D8F4535C0B8D2A807C8512F88209E001A9DE39AE847E | T2, STOCK | T1 = RTTI-gate stop |

Measured link evidence (SDK:2310): warning "LINK_FAILURE: block 0 (NiNode)
field children link 4294967294 out of range (num_blocks=13)". All five
controls have a DETECTED case; no silent success occurred (the STOCK
mid-file accepted=true is verified as a structurally-valid file case,
not a violation — see RESIDUAL-1).
Also updated: G-TOOL-3 evidence-pointer row in 00_CONTROL/
STAGE_ACCEPTANCE_GATES.csv (sha256
2C40DF1A5AF3622377B534CD73DAF1A1B0EB758B349704CF1C93717D0229AB21, 4691 B
— controls/ path + "(C1 persistence)" appended); dated addendum appended
to 03_TOOL/FAIL_CLOSED_TESTS.md (sha256
4B9C574C98491099A2EF17D81A1F6DD752F65E30B8DC829E5C275945FC860E3B,
original text unchanged); dated C1 note appended to
03_TOOL/TOOL_IMPLEMENTATION_REPORT.md (sha256
BF6A79A2EE14EA4CC26872D096B831796BFDEF2BFA0F12FE7F7A2DB03E3A002B) stating
that E2 executed the controls in-memory (disclosed) and C1 persisted them.

### FIX-2 (compatibility matrix rewrite) — DONE
03_TOOL/GAMEBRYO_COMPATIBILITY_MATRIX.csv rewritten (sha256
02D72F0AAA48E04AD00108AE1C0FDC370DE04BB0507C23438E07BC4D386E8A7A, 4920 B).
Programmatically verified with the csv module: 1 header + 9 data rows,
exactly 14 fields per data row, ALL fields quoted, zero blank cells, every
verdict-column token in {PASS, PARTIAL, FAIL, NOT_TESTED, UNKNOWN}. The
malformed rows 5/8 (dialog/P7 backslash-comma) are now properly quoted with
the real comma preserved verbatim; row 10 (OUR_TOOL) has its NOTES cell.
BUILDS of the 3 reimplementation rows = NOT_TESTED with "reimplementation --
no build step" reason in NOTES; FAIL-BY-DESIGN -> FAIL with the design
reason in NOTES. Information content otherwise unchanged.

### FIX-3 (gui log encoding) — DONE
04_EVIDENCE/gui_attempts_log.txt: UTF-16LE (FF FE BOM, 18404 B, old sha256
A0818EBB0EE0A98E01249A4DF1BCD3E66236C2B6AC3B797DEB34089B660539AF) ->
plain UTF-8, 9413 B, new sha256
986B9E77C5D782CE198F98231D07666801C0AE80ECB47A405C400DA2F1E83A0F.
04_EVIDENCE/gui_attempts_log2.txt: UTF-16LE (7922 B, old sha256
BE395C7F20A7C8931C93D994B45A96B59584463216F3D18A0E8FFA1C306FACA6) ->
plain UTF-8, 4172 B, new sha256
695FF22BFAB6796185F15C775D81BA1179C1209EFB45E293D540EB52269341CB.
Both: UTF-16LE round-trip re-encode verified byte-identical before write;
one-line conversion header in the E3 sgp_T1_dialog.txt pattern; log wording
byte-preserved.

### FIX-4 (pycache + .gitignore) — DONE
Deleted exactly the six transient .pyc build artifacts (tools/gamebryo_oracle/
__pycache__/gb12core.cpython-312.pyc; adapters/compare/__pycache__/
adapter.cpython-312.pyc; adapters/gb12/__pycache__/{__init__,adapter,
registry}.cpython-312.pyc; adapters/gb26/__pycache__/adapter.cpython-312.pyc)
and the 4 emptied __pycache__ dirs. Created tools/gamebryo_oracle/
.gitignore (sha256 862263FA1F46C20F0D1E4DAC5FFCC75ABD55C08211B2C3864C5F8764B9D87793)
with exactly two lines: __pycache__/ and *.pyc. All C1 python executions
used -B; post-run census: 0 .pyc / 0 __pycache__ remaining.

### FIX-5 (TEST_MATRIX refresh) — DONE
03_TOOL/TEST_MATRIX.csv refreshed (sha256
A5D52F05960F38A5FEA6C7312D192C32540C8F8F3B07EE70725256B212CF3DA8, 4019 B;
31 rows x 4 fields verified). T3_full_decode row now states the post-E3
facts: all ~25 T3 RTTI classes implemented (E3); honest PARTIAL decode
448/1288 blocks -- NOT EOF-exact (closure budget; residuals in
inspect_T3_gb12_full.json); full-decode determinism pair byte-identical
(sha B4F5A55A7FA9BDC769B24108FCE120CAB0FFCDC75FE00FFD2FB6F2F1F4A281E7);
ORIGINAL RTTIError(NiArkAnimationExtraData) verdict unchanged.
G_SIG_signatures row now: produced in E3 per order s28, PASS,
02_ANALYSIS/GAMEBRYO_SEMANTIC_SIGNATURES.json. All still-true E2 rows
byte-unchanged (incl. OUR_DECODER_* honest FAILs).

### FIX-6 (report scan) — DONE (zero corrections required)
Scanned 06_REPORT/FINAL_REPORT.md and 06_REPORT/HANDOFF.md in full plus a
pattern scan (columns / NOT_APPLICABLE / FAIL-BY-DESIGN / in-memory /
stdout / persist / controls): NO statement contradicted by the C1 fixes
exists in either file — both were already E3-updated inline (Q17/Q26/Q27
E3 notes; HANDOFF terminal block E3 state), there is no "13 columns"
claim, no stale T3/G-SIG status, and no control-persistence claim in
06_REPORT (the E2 in-memory disclosure lived in 03_TOOL, now covered by
the addendum). HANDOFF terminal block CONFIRMED TRUTHFUL post-C1:
RUN_STATUS=PARTIAL (E3 description still accurate; C1 is a mechanical
QC_PARTIAL correction), HARD_STOP=NO, G-SIG-1 produced, T3 closure open —
all still true; Q29 (payloads/corrupted copies LOCAL_ONLY) remains true
(only decode-verdict JSONs entered the package, no payload bytes). Zero
"(C1 correction, 2026-10-03)" marks were added because zero corrections
were needed — this scan result is itself the FIX-6 deliverable.

## RESIDUALS (for PE-MASTER; none block the package)

1. gb12core.decode, called directly (as tests/test_gb12.py does), RAISED an
   uncaught DecodeError on two grossly-corrupted STOCK inputs (link
   pattern-collision feeding 0xFFFFFFFE into num-top; observed fail-closed:
   exception, never silent) instead of returning the error-JSON path of the
   s17 "exception" detector row. The oracle.py CLI wrapping of decode
   exceptions was NOT verified in C1. Recorded raw in the control JSONs.
2. STOCK mid-file control: the flipped byte (844 of 1689) lands deep inside
   a NiTriStripsData block (offset-in-block 260) — verified from the
   persisted raw output — so the mutated file remained structurally valid
   and loads (accepted=true, no error). Recorded with a MIDFILE_STOCK_NOTE
   in corrupted_midfile.json + the addendum; consistent with original
   loader semantics, NOT a fail-closed violation; the structural case is
   DETECTED on T2 (QC parity 05_QC/raw_qc_outputs/control_corrupt_midfile.json).
3. T1 mid-file corruption control not re-executed in C1 (unbounded
   closure-search wall risk on a corrupted 66-block NiArk body; E3 measured
   the S_B candidate-phase cost class on T3); honest not-run note in the
   JSON; control covered by T2 + QC parity.
4. G-MATRIX-1 gates row still reads "13 columns per s16" while the matrix
   header has 14 columns (incl. NOTES) and FIX-2 mandates 14 fields per data
   row. Not in the assigned fix list — left unchanged, flagged here.
5. gb12-adapter CONTROLLERS cell annotation ("T3 has controllers but its
   full-decode exceeded budget") is stale post-E3 (classes implemented; T3
   now decodes 448/1288 incl. controllers). Kept unchanged per FIX-2's
   "information content otherwise unchanged"; flagged here.
6. FIX-2 interpretation: only 2 NOT_APPLICABLE cells existed (gb12/gb26
   BUILDS). OUR_TOOL's BUILDS was "PASS (pure python; no build)" -> set to
   "NOT_TESTED (reimplementation -- pure python; no build step)" with the
   reason in NOTES, per the instruction's 3-reimplementation-rows intent.
7. gui_attempts_log3.txt is UTF-8 WITH BOM (EF BB BF) — not in the FIX-3
   list; left untouched.
8. Process disclosure: c1_followup.py's in-memory append of the SDK link
   run was initially lost to a persistence-order defect (final recompute
   reloaded from disk before the dump); disclosed in
   link_failure_mutation.json RUN_NOTE and fixed by the c1_complete.py
   re-execution (identical target=6/pos=382 -> pos=388 both runs, i.e.
   deterministic). c1_verify_annotate.py had one trivial NameError
   (FILE_LEN/FILES_LEN) patched before its successful run; its post-patch
   sha256 was not re-printed (only the three files it changed are hashed
   above).

## SELF_CHECK (executor's own, labelled — NOT independent MASTER audit)

- Scope: only the six assigned fixes + their direct evidence; no completed
  run modified other than the assigned paths; zero writes to pinned
  payloads, gb12core.py, foreign paths, or any completed package outside
  the listed files.
- FIX-1 outputs re-executed (not copied from memory): test-file control code
  paths copied verbatim, run on sha-pinned sandbox copies; every JSON
  parses (json.load verified) and carries the 4 required labels.
- Negative controls meaningful: the honest non-detections (T1 RTTI-gate
  stops; STOCK artifacts) are recorded as raw outputs with verified
  explanations, not smoothed over; no default-success fallback anywhere.
- CSV claims verified by execution (csv module field counts, blank-cell
  scan, closed-set token scan), not by assertion.
- Gates-row replacement asserted exactly-once before writing; FAIL_CLOSED
  original text preserved (append-only + two wording refinements, anchors
  asserted once).
- FIX-4 verified post-run: 0 .pyc / 0 __pycache__ under
  tools/gamebryo_oracle (python -B used for every execution).
- Budget: 25/25 tool calls (at cap), ~40/45 wall minutes; no HARD_STOP
  condition fired; no git operations; no vault writes.

RUN_STATUS = COMPLETED (all six fixes dispositioned; FIX-6 resolved as a
zero-change scan with its truthfulness confirmation)
FINAL_REPORT_PATH = docs/audits/PE_GAMEBRYO_ORACLE_TOOL_R1_20261003/
06_REPORT/FINAL_REPORT.md (unchanged in C1; still accurate)
PRIMARY_EVIDENCE_PATHS =
  docs/audits/PE_GAMEBRYO_ORACLE_TOOL_R1_20261003/04_EVIDENCE/controls/
    {corrupted_header_version,corrupted_midfile,unknown_class_mutation,
    link_failure_mutation,object_count_mutation}.json
  docs/audits/PE_GAMEBRYO_ORACLE_TOOL_R1_20261003/04_EVIDENCE/scripts/
    c1_{control_persist,followup,complete,verify_annotate}.py
  docs/audits/PE_GAMEBRYO_ORACLE_TOOL_R1_20261003/03_TOOL/
    GAMEBRYO_COMPATIBILITY_MATRIX.csv + TEST_MATRIX.csv +
    FAIL_CLOSED_TESTS.md (addendum) + TOOL_IMPLEMENTATION_REPORT.md (note)
  docs/audits/PE_GAMEBRYO_ORACLE_TOOL_R1_20261003/00_CONTROL/
    STAGE_ACCEPTANCE_GATES.csv (G-TOOL-3 row)
  docs/audits/PE_GAMEBRYO_ORACLE_TOOL_R1_20261003/04_EVIDENCE/
    gui_attempts_log.txt + gui_attempts_log2.txt (UTF-8 conversions)
  tools/gamebryo_oracle/.gitignore
HARD_STOP_REASON = NONE
