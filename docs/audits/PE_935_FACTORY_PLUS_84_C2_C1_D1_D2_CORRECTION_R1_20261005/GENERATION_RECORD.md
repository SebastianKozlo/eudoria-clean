# GENERATION RECORD — PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005

Every generated artifact of this package, the exact generation command, the
instrument identity and the measured result. Nothing here is copied from a
prior run and relabelled: every generator was re-executed this run against
the pinned EXE (REGRESSION_DIFF.json measures the outcome against the exact
BASE package; byte-identity is reported per artifact, never assumed).

Environment: Python 3.12.10 (Windows), all invocations `python -B ...`
(bytecode writes disabled everywhere). Working directory: the repo root or
script dir as noted; all output paths under OUTPUT_ROOT.

## Instrument identities (03_SCRIPTS; lineage: committed BASE scripts + this run's corrections)

| Script | Role this run | Changes vs the committed BASE script |
|---|---|---|
| `x86dec.py` | production decoder | D1: per-opcode legal-reg tables for 0F 71/72/73 (`_D1_LEGAL_REG_NO66/_66`); `0F 73 /4` REJECTED with and without 66; 0F BA behaviour, mod=3 requirement, memory-form rejection, F2/F3 rejection and ALL carried fixes preserved verbatim |
| `pebnd.py` | loader + boundary machinery | CARRIED UNCHANGED from BASE (run label + header note only); the D1 decoder change is measured THROUGH it |
| `c1_pin_ledger.py` | pin JSON+CSV generator | run label + D2 note only; PINS carried VERBATIM (never edited) |
| `c2_census.py` | census generator | run label + header note only |
| `c3_object_scope.py` | C3 generator | run label + header note only |
| `cqc_battery.py` | QC battery | D2: gate_q2 roster/multiset/totals/role/EA-spec binding; gate_q3 roster membership + EXE-derived operand_kind; D1 unit vectors + the D1 falsifier case with in-run BASE reproduction; run_d2_mutations harness (8 cases); Q1/Q14 BASE_SHA 9d31a82 + updated required/forbidden strings + required-files battery; outputs D1/D2 records |
| `capture_independent_evidence.py` | oracle capture | +9 D1 fixtures (expectations locked BEFORE decoder evaluation); outputs renamed D1_INDEPENDENT_ORACLE_RECORDS.json + BASE_COMMIT_MESSAGE_VERBATIM.txt (BASE_SHA 9d31a82) |
| `pin_roster.py` | NEW: D2 expected-roster extraction | ast literal evaluation of PINS from the BASE Git blob; in-process cache; identity recording |
| `extract_expected_pins.py` | NEW: EXPECTED_PIN_REGISTRY.json generator | — |
| `diff_vs_base.py` | NEW: regression vs the exact BASE package | byte-identity + declared-metadata-excluded comparison |
| `make_manifest.py` | manifest generator (LAST) | run path updated; entrypoint covered at its CURRENT BASE state (this run does not edit AUDIT_ENTRYPOINT.md) |

## Generation sequence (actual commands, in execution order)

1. Preflight (fail-closed, BEFORE any write): `git rev-parse HEAD` /
   `git rev-parse origin/master` / `git ls-remote origin master` (all ==
   9d31a82b6589f46e9ca6c75c6e323b433c1ebf92); `git status --porcelain=v1`
   (tracked clean; the six foreign untracked paths recorded, untouched);
   EXE / Desktop-report / source-manifest size+SHA256 re-verified; source
   manifest bijection 33/33 vs physical files AND vs exact Git blobs at
   BASE (script: verify_base_package.ps1 in the task temp tree OUTSIDE the
   repo; measured PASS - see INPUT_IDENTITIES.md).
2. `python -B capture_independent_evidence.py`
   -> `01_RAW/D1_INDEPENDENT_ORACLE_RECORDS.json` (80 fixtures; measured
   oracle verdicts: `0F 73 E0 02` -> (bad); `66 0F 73 E0 02` ->
   data16 (bad); all six D1 legal controls legal at the expected lengths)
   + `01_RAW/BASE_COMMIT_MESSAGE_VERBATIM.txt` (4,918 B; machine-checked
   == `git log -1 --format=%B 9d31a82...` by gate Q14).
3. `python -B extract_expected_pins.py`
   -> `EXPECTED_PIN_REGISTRY.json` (133 claims; role tally bytes=38,
   mem=46, imm32=14, call=29, imm8=4, declassified=2; ea_required=46;
   source: BASE Git blob 5a7b642f..., file SHA256 757225FE...).
4. `python -B c1_pin_ledger.py`
   -> `01_RAW/C1_PIN_EVIDENCE.json` + `CORRECTED_PIN_LEDGER.csv`.
   Measured: pins=133 fail=0 exe_ok=True statuses={VALIDATED: 120,
   DECLASSIFIED_NOT_A_CALL: 2, CORRECTED_VALIDATED: 4,
   VALIDATED_BYTES_BOUNDARY_UNRESOLVED: 5, NOT_VERIFIED: 2} - identical
   status distribution to BASE.
5. `python -B c2_census.py`
   -> `CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv` + `01_RAW/C2_CENSUS.json`
   + `AF3_PROVENANCE_LEDGER.csv`.
   Measured: raw=2612 pos=2227 negctl=385 bndpos=10 refuted=0 known=2
   unres=2218 wcand=832 wrongobj=1 read=6 midrej=0 provunres=832
   decreject=0 af3rows=5 - every quantity identical to BASE (the D1 decoder
   repair changed no census row; the falsifier's .text census measured ZERO
   occurrences of the `0F 73` mod=3 reg=4 pattern, so no anchor decode
   stream can have been affected).
6. `python -B c3_object_scope.py`
   -> `01_RAW/C3_OBJECT_SCOPE.json`. Measured: decode=RET_REACHED insns=93
   offset0=3 seg=2 thisbase=0 vptr=NOT_OBSERVED callsites=3/3 ctorE8=2/10 -
   identical values to BASE.
7. `python -B cqc_battery.py --mode data`
   -> `01_RAW/CQC_MUTATION_RESULTS.json` (7 retained controls),
   `01_RAW/D2_MUTATION_RESULTS.json` (8 new D2 controls),
   `01_RAW/D1_BOUNDARY_FALSIFIER.json`, `01_RAW/CQC_DECODER_UNIT_TESTS.json`
   (72 entries), `01_RAW/CQC_BOUNDARY_COUNTEREXAMPLES.json` (14 cases),
   `01_RAW/CQC_FINAL.json` (data-mode record), `AF1_MUTATION_MATRIX.csv`
   (15 rows), `AF2_BOUNDARY_TEST_MATRIX.csv` (14 rows).
   Measured: gates Q1-Q13 all PASS; mutations 15/15 CAUSAL_PASS
   (7/7 retained + 8/8 D2). Console line of the FINAL full run is recorded
   in QC_REPORT.md.
8. `python -B diff_vs_base.py`
   -> `REGRESSION_DIFF.json` (measured: 3 artifacts byte-identical, 3
   metadata-only (run label), 6 expected content changes - all new/extended
   D1/D2 artifacts; census 0/2612 changed rows; pins 0/133 changed fields;
   AF3 0/5; measured quantities identical).
9. `python -B cqc_battery.py --mode docs` (FINAL full run; executed AFTER all
   documents were written; the committed CQC_FINAL.json is THIS run)
   -> re-executes Q1-Q13 + both mutation harnesses fresh + Q14 docs gates;
   measured verdict recorded in QC_REPORT.md. Sequence: the first docs-mode
   execution failed Q14 on two instrument/report-alignment findings (the
   required-string list still carried the BASE-form core status; one
   forbidden-phrase hit in the ledger's S-AUD-01 summary line) - fixed
   within the ONE authorized targeted QC repair round (see QC_REPORT.md);
   the subsequent docs-mode run is the committed record (14/14 PASS).
10. `python -B make_manifest.py`
    -> `COMMITTED_PACKAGE_MANIFEST_SHA256.csv` (generated LAST; bijection
    verified: missing=0, extra=0, duplicates=0, size mismatches=0, SHA256
    mismatches=0; HANDOFF-declared MANIFEST_ROW_COUNT cross-checked).

## In-run construction fixes (disclosed honestly; all BEFORE the first full
battery pass; none is a post-QC repair round)

1. `run_d2_mutations` input-path construction crashed with a TypeError on
   the first data-mode invocation (a format-string argument misplacement in
   the temp-tree input census); fixed to direct relative-path construction
   and re-run. The committed battery is the fixed version; the crash
   produced NO artifact (the run aborted before any output write).
2. The Q14 supersession record-header regex was updated from the BASE
   `S-P2-*` prefix to this ledger's `S-D1-*/S-D2-*/S-CM-*/S-AUD-*` prefixes
   before the docs-mode run.
3. Cosmetic: the final console line's mutation denominator corrected to the
   total (15) - stdout only, no artifact content.

ONE targeted QC repair round within D1/D2 was AUTHORIZED and USED (the
docs-mode Q14 findings above; both instrument/report alignment items inside
the correction scope; the repair round is now exhausted by design): the
first full data-mode battery run after the construction fixes passed 13/13
gates + 15/15 mutations; the first docs-mode run failed only Q14 (2
findings); after the repair the final docs-mode run passed 14/14 + 15/15.
No material defect remains.

## Unchanged code/definition reuse (permitted)

Reusing unchanged code or definitions is allowed; copying old generated
outputs and labelling them freshly generated is NOT. This run re-executed
every generator (steps 2-9) and measured the outcomes: the census CSV, pin
CSV and AF3 ledger are BYTE-IDENTICAL to the committed BASE files by
fresh regeneration (REGRESSION_DIFF.json), and the C1/C2/C3 JSONs differ
only in the declared `run` label.

## Record-repair after internal QC (2026-10-05; record hygiene ONLY — no new science)

Origin: the internal QC run PE_935_QC_INTERNAL_20261005 (00_CONTROL_INTERNAL_QC/,
read-only for this executor) independently reproduced the D1/D2 results and
returned verdict QC_PASS_WITH_FINDINGS with two P2 record/provenance findings
(F1, F2) plus observation O1 (the nondeterministic mkdtemp temp-path fields in
the mutation records — the root cause of F2). This repair pass is RECORD
HYGIENE ONLY: no D1/D2 measured result, PIN, CORE status, or supersession-ledger
record was touched (the 9 existing ledger records are unedited; the
repair-round statement above still describes the ORIGINAL generation
sequence, steps 1-10 — this section documents the separate, PE-MASTER-authorized
record-repair dispatch that followed the internal QC).

- F1 fix: `03_SCRIPTS/cqc_battery.py` line 2745 — the `final` dict's
  `qc_scope` literal still carried the BASE value
  `SELF_CHECK_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION` while the sibling
  `run` literal had been updated to this run id; corrected to
  `SELF_CHECK_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION` (the exact value
  QC_REPORT.md, FINAL_REPORT.md and INPUT_IDENTITIES.md already declare).
  Instrument SHA256 after the fix:
  5A8B5F9D82A514D7688E3D3DA80F4A05864349452762770B8D6DF56F62A68EB5
  (the one-literal change only).
- F2 fix: `diff_vs_base.py` re-executed AFTER the final battery re-run
  (step 13 below), so every REGRESSION_DIFF.json `sha256_new` again re-hashes
  true against the FINAL artifacts. The stale intermediate identity was the
  data-mode battery's CQC_MUTATION_RESULTS.json (hash taken by the original
  step 8 before the original step 9 docs run overwrote the file — observation
  O1's mkdtemp fields make the two runs differ bit-wise while semantically
  identical).

Re-execution sequence (new runs; commands verbatim, `python -B` as before):

11. `python -B cqc_battery.py --mode data`
    -> refreshed `01_RAW/CQC_MUTATION_RESULTS.json`,
    `01_RAW/D2_MUTATION_RESULTS.json`, `01_RAW/D1_BOUNDARY_FALSIFIER.json`,
    `01_RAW/CQC_DECODER_UNIT_TESTS.json`,
    `01_RAW/CQC_BOUNDARY_COUNTEREXAMPLES.json`, `AF1_MUTATION_MATRIX.csv`,
    `AF2_BOUNDARY_TEST_MATRIX.csv` + the data-mode CQC_FINAL.json (overwritten
    again by step 12).
    Measured: gates Q1-Q13 all PASS; mutations 15/15 CAUSAL_PASS (7/7 + 8/8).
    Console: `CQC done (data). gates: {"Q1": "PASS", ..., "Q13": "PASS"} mutations_causal=15/15 verdict=QC_PASS`
12. `python -B cqc_battery.py --mode docs` (the FINAL full run of this package;
    the committed `01_RAW/CQC_FINAL.json` is THIS run)
    -> re-executes Q1-Q13 + both mutation harnesses fresh + Q14 docs gates.
    Measured: gates Q1-Q14 all PASS (14/14); mutations 15/15 CAUSAL_PASS
    (7/7 retained + 8/8 D2); QC_VERDICT = QC_PASS; `qc_scope` =
    SELF_CHECK_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION; mode = docs.
    Console: `CQC done (docs). gates: {"Q1": "PASS", ..., "Q14": "PASS"} mutations_causal=15/15 verdict=QC_PASS`
13. `python -B diff_vs_base.py` (executed AFTER step 12, per the F2 fix)
    -> `REGRESSION_DIFF.json` regenerated over the final artifacts.
    Measured: content_changes=6 metadata_only=3 byte_identical=3/9 (identical
    summary values to the original step 8); all 9 `sha256_new` + 9
    `sha256_base` declarations re-hash true against the physical files (my
    own re-validation outside the package; see the repaired-file census
    below).
    Console: `REGRESSION_DIFF: content_changes=6 metadata_only=3 byte_identical=3/9`

Repaired-artifact census (the ONLY package files whose content changed in
this record-repair pass; every change is the F1/F2 fix itself or the
observation-O1 temp-path fields — no semantic battery value changed):

| File | New SHA256 | Nature of change |
|---|---|---|
| `03_SCRIPTS/cqc_battery.py` | 5A8B5F9D82A514D7688E3D3DA80F4A05864349452762770B8D6DF56F62A68EB5 | F1 literal fix (qc_scope) |
| `01_RAW/CQC_FINAL.json` | 7798C10855F76591F41EF2F376B86DE462EB33F28F64D7BDD9E5A8BB1E95E924 | fresh final docs run; qc_scope corrected; 14/14 + 15/15 unchanged |
| `01_RAW/CQC_MUTATION_RESULTS.json` | 0981403799355FC32E555C045D19C38B84165B2BDCD32563874FAB79D8B77E30 | fresh run; mkdtemp AFTER temp-path fields only (O1); ids/causality/failing-predicate counts identical (7/7 CAUSAL_PASS) |
| `01_RAW/D2_MUTATION_RESULTS.json` | 614681416F8CF5393357C4D0679E95E38A7A24F8CE10057132F7F94E237EF175 | fresh run; mkdtemp TEMP_TREE fields only (O1); 8/8 CAUSAL_PASS unchanged |
| `AF1_MUTATION_MATRIX.csv` | 815683FB9CDE3A5D431CF9E36733D1B09C8484DD5421E391A49E944F11AE8E1F | fresh run; temp-path columns only (O1); all 15 rows CAUSAL_PASS with identical semantic columns |
| `REGRESSION_DIFF.json` | 6D69CD9DE604DFA25E5818B5ED72E2CF68D84B492B53A4F010E2587D682B1606 | F2 fix: sha256_new now matches the final artifacts (9/9 re-verified) |

Scope discipline of this pass: `COMMITTED_PACKAGE_MANIFEST_SHA256.csv` was
intentionally NOT regenerated (the persistence phase owns manifest LAST per
the contract scope — it must also cover `00_CONTROL_INTERNAL_QC/` and the
future `PE_MASTER_REVIEW.md` and the updated `AUDIT_ENTRYPOINT.md`); its rows
for the six repaired files (and this GENERATION_RECORD/QC_REPORT note) are
stale by design until that phase. `00_CONTROL_INTERNAL_QC/`,
`AUDIT_ENTRYPOINT.md`, `SUPERSESSION_LEDGER.md`, `PE_MASTER_REVIEW.md`,
`FINAL_REPORT.md`, `HANDOFF.md`, `INPUT_IDENTITIES.md`, `EVIDENCE_INDEX.md`,
the foreign untracked paths and all D1/D2 measured results are untouched.
