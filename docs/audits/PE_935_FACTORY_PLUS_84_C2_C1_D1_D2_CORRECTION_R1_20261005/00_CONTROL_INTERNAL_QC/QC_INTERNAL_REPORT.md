# QC INTERNAL REPORT — PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005 / 00_CONTROL_INTERNAL_QC

RUN_ID = PE_935_QC_INTERNAL_20261005
ASSIGNMENT_MODE = INTERNAL_QC (independent, fresh-context, STATIC-ONLY)
QC_SCOPE = INDEPENDENT_INTERNAL_QC_FACTORY_PLUS_84_C2_C1_D1_D2 (LOAD_BEARING depth)
PARENT_LOOP_ID = PE-MASTER direct dispatch of 2026-10-05 (internal QC of the
D1/D2 correction package; NO_NESTED_TASKS)
EXECUTED_BY = pe-master-auditor worker session (fresh context)
AUDITED_PACKAGE = docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005
BASE_SHA = 9d31a82b6589f46e9ca6c75c6e323b433c1ebf92 (verified: HEAD == BASE; nothing committed; package untracked)
RUN_CONTRACT = OPENCODE_F84_C2_C1_D1_D2_CORRECTION_COMPLETE_20261005.md
(read in full from disk; 15,036 B; SHA256 CFB2B43BC760D4ED337ED0EEB79E480993B2396EDBEFB0D573C017CF5446D2BD)

QC_VERDICT = QC_PASS_WITH_FINDINGS
(2 findings P2 — record/provenance defects, no scientific-result defect found;
all load-bearing D1/D2 claims INDEPENDENTLY REPRODUCED or RE-VERIFIED;
a CORRECTION_REQUEST for the two record defects is returned to PE-MASTER)

## 1. Findings

### FINDING F1 (P2) — CQC_FINAL.json `qc_scope` field carries the BASE (THREE-P2) QC-scope name; drift vs all four declaring documents

- EXACT LOCATION: `01_RAW/CQC_FINAL.json` top-level field `qc_scope` =
  `"SELF_CHECK_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION"` (the committed LAST
  full battery run record). Producing code:
  `03_SCRIPTS/cqc_battery.py` line 2745 — in the `final` dict the sibling
  field `"run"` (line 2744) was updated to the D1_D2 run id but the
  `"qc_scope"` literal was not.
- CONTRADICTED CLAIMS: QC_REPORT.md line 3, FINAL_REPORT.md line 301 and
  INPUT_IDENTITIES.md line 116 all declare
  `QC_SCOPE = SELF_CHECK_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION`; EVIDENCE_INDEX
  and the audit trail describe the committed CQC_FINAL.json as the record of
  that QC_SCOPE. The machine record disagrees with the documents.
- FAILURE MECHANISM: single-line oversight in the run-id rename (the diff of
  cqc_battery.py BASE→NEW shows the `run` literal changed while `qc_scope`
  stayed at the BASE value; no gate checks the record's own qc_scope field,
  so Q14 could not catch it).
- EFFECT: provenance/labeling defect only. The gate predicates, mutation
  harness and measured values in CQC_FINAL.json are unaffected (verified
  independently below); but the committed record self-identifies under the
  WRONG QC scope name — a record-vs-report drift inside the package.
- NARROW CORRECTION: update `03_SCRIPTS/cqc_battery.py:2745` to
  `"SELF_CHECK_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION"` and re-run the battery
  `--mode data` + `--mode docs` (this refreshes CQC_FINAL.json,
  CQC_MUTATION_RESULTS.json and the other battery outputs), then regenerate
  the manifest (already required by the persistence phase for the entrypoint
  row). The re-run must re-verify 14/14 + 15/15 as before.
- REVALIDATION PREDICATE: `json.load(01_RAW/CQC_FINAL.json)["qc_scope"] ==
  "SELF_CHECK_FACTORY_PLUS_84_C2_C1_D2_CORRECTION"` AND the string occurs in
  none of the documents with the THREE_P2 name; manifest bijection re-verified.

### FINDING F2 (P2) — REGRESSION_DIFF.json `sha256_new` for 01_RAW/CQC_MUTATION_RESULTS.json does not match the committed file (stale intermediate identity)

- EXACT LOCATION: `REGRESSION_DIFF.json` →
  `reports["01_RAW/CQC_MUTATION_RESULTS.json"].sha256_new` =
  `A83B0B714C8EC4D1E2995FE734C39EFED9A7E6630F90B25BE215E5CC71C65533`;
  actual on-disk SHA256 of the committed `01_RAW/CQC_MUTATION_RESULTS.json` =
  `EB2707AF1A0645EA9AC8784D363087F6A1A259995E38C5DBBCF5C90F46C24BA6`
  (my independent re-hash; every OTHER sha256_new and ALL sha256_base fields
  in REGRESSION_DIFF.json re-hash correctly — 15/16 SHA declarations verified
  true).
- FAILURE MECHANISM (verified from GENERATION_RECORD sequence + code):
  step 8 (diff_vs_base.py) ran after the data-mode battery (step 7) and
  hashed that run's CQC_MUTATION_RESULTS.json; the FINAL docs-mode battery
  (step 9) re-executed all 7 retained mutations and OVERWROTE the file; the
  mutation records embed the random `mkdtemp` temp-tree path in each
  `AFTER` field (7 fields; e.g. `p2fix_mut_gy65mp13_out\M1`), so the two
  runs differ bit-wise while being semantically identical (ids M1..M6 +
  AF3/Q8, 7/7 CAUSAL_PASS in BOTH — the ids/causality declarations in
  REGRESSION_DIFF remain TRUE for the committed file). REGRESSION_DIFF was
  not regenerated after the final battery run.
- CONTRADICTED CLAIM: REGRESSION_DIFF.json is declared as "the complete
  regression measurement vs the exact BASE package" and FINAL_REPORT/HANDOFF
  rely on its byte-identity/content-identity statements; one recorded
  artifact identity is false as committed (L10: MANIFEST_IDENTITY_CORRECT is
  FALSE for this entry even though the physical file is a legitimate battery
  output; the package manifest itself is correct — 38/38 rows re-hash true).
- EFFECT: any consumer verifying REGRESSION_DIFF's recorded identity against
  the committed artifact gets a mismatch; downstream blast radius limited to
  this one JSON field (no gate, count or verdict depends on it).
- NARROW CORRECTION: re-run `03_SCRIPTS/diff_vs_base.py` AFTER the final
  battery run (so `sha256_new` reflects the committed file) and regenerate
  the manifest (already required). Longer-term: make the mutation-record
  `AFTER` field deterministic (strip the mkdtemp suffix) so re-runs are
  byte-stable — see OBSERVATION O1.
- REVALIDATION PREDICATE: sha256(01_RAW/CQC_MUTATION_RESULTS.json on disk)
  == REGRESSION_DIFF.reports[that key].sha256_new; manifest bijection
  re-verified; 15/15 + 14/14 unchanged.

### OBSERVATION O1 (P3, root cause of F2) — nondeterministic temp-path fields in mutation records

`CQC_MUTATION_RESULTS.json` (7 `AFTER` fields) and `D2_MUTATION_RESULTS.json`
(8 `TEMP_TREE` fields) embed random `mkdtemp` suffixes, so battery outputs
are not byte-repeatable between runs. Causality/semantics are unaffected
(each record's failing predicates are measured in-run), but any post-hoc
re-execution of the battery invalidates previously recorded SHAs of these
two artifacts (exactly what F2 shows). Recommend deterministic identifiers
(e.g. constant per-run temp prefix recorded once) in a future authorized
instrument pass. Not a standalone defect this run; recorded as the mechanism
behind F2.

### OBSERVATION O2 (P3, naming) — REGRESSION_DIFF `changed_vectors` semantics

diff_vs_base.py keys the unit battery by vector string; the two carried
`0F 73 /2` and `/6` vectors, each now present twice (H2 entry + the disclosed
byte-identical D1 duplicate entry with a D1 note), surface as
`changed_vectors` rather than `new_vectors`. FINAL_REPORT discloses the
duplicates honestly; the field name is mildly misleading but the content is
accurate (64+6 new+2 duplicated = 72 entries, verified). No correction
required; noted for future diff readability.

## 2. Independent verification results (my own measurements)

All numbers below were re-measured by me from the physical artifacts (raw
JSON/CSV parse + own scripts), NOT copied from the executor's reports.

| # | Claim / declared value | My independent measurement | Verdict |
|---|---|---|---|
| 1 | PINS roster 133 claims; role tally bytes 38 / mem 46 / imm32 14 / call 29 / imm8 4 / declassified 2 | AST-extracted PINS from BASE Git blob 5a7b642f... (file SHA256 757225FE... == declared): 133; tally identical | CONFIRMED |
| 2 | EXPECTED_PIN_REGISTRY.json == BASE PINS | Full field compare (claim_id/va/role/expect_bytes/expect_ea/expect_imm) over all 133: 0 mismatches; 0 duplicate claim_ids; on-disk NEW c1_pin_ledger PINS == BASE PINS (PINS never edited) | CONFIRMED |
| 3 | JSON pins 133 / CSV rows 133 / roster 133; EA objects 46 | 133 / 133 / 133; 46 EA objects; CQC_FINAL Q2 d2_pin_universe agrees (dups/missing/extra all empty) | CONFIRMED |
| 4 | Pin status tally VALIDATED 120 / DECLASSIFIED 2 / CORRECTED_VALIDATED 4 / VALIDATED_BYTES_BOUNDARY_UNRESOLVED 5 / NOT_VERIFIED 2 | CSV recount identical (120/2/4/5/2); declared pin_totals tally == CSV-recomputed | CONFIRMED |
| 5 | Census 2612 rows; positive 2227; negative-disp8 385; boundary-confirmed positive 10; census unresolved 2218; write candidates 832; wrongobj 1; read 6; midrej 0; prov-unresolved 832 | Recount from CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv: 2612 rows; signed_disp +132: 2227; −124: 385; boundary_status CONFIRMED: 10 (2 KNOWN + 6 READ + 1 WRONGOBJ + 1 UNRESOLVED row 0x004B0A3A); classification UNRESOLVED: 2218 (cross-tab 2217 boundary-UNRESOLVED + the 1 CONFIRMED-boundary UNRESOLVED row — both definitions coexist consistently); Q9-rule write candidates 830 write + 2 lea-linked = 832; wrongobj 1; read 6; midrej 0 | CONFIRMED |
| 6 | AF3 ledger 5 rows (4 UNRESOLVED + 1 PROVEN manager) | 5 rows; 0x00707EC0 PROVEN, 0x006D4F88/0x007196AA/0x0074955A/0x0075138F UNRESOLVED | CONFIRMED |
| 7 | Mutations: 7 retained + 8 D2 = 15/15 CAUSAL_PASS, each UNMUTATED=PASS→MUTATED=FAIL through its own production gate | AF1_MUTATION_MATRIX 15 rows all PASS→FAIL; CQC_MUTATION_RESULTS 7/7 (M1:Q2, M2:Q3, M3:Q8, M4:Q6, AF3/Q8:Q7, M5:Q2, M6:Q2); D2_MUTATION_RESULTS 8/8 with exact FAILING_PREDICATES taken from gate_q2's OWN mismatch list (verified per case: D2-M1/M3 = role mismatch + required-EA missing (2), D2-M2/M4 = missing claim (1), D2-M5 = multiplicity (1), D2-M6/M7 = extra claim (M7 also status_tally (2)), D2-M8 = JSON missing + CSV missing + totals vs roster (3)); per-case INPUT_HASH_CENSUS proves unrelated inputs byte-identical (M1..M7: 5/6 identical, only the declared target changed; M8: 4/6, the two declared targets changed) — no manifest/Git-baseline/other-gate failure substitutes | CONFIRMED (predicate inspection + code read) |
| 8 | D1 negatives REJECT (2/2), six legal controls at true lengths, /4 stays legal for 0F 71/72, 66 0F 73 /3,/7 legal, 0F BA/memory/F2/F3 unchanged | MY OWN EXECUTION of the on-disk corrected decoder in-memory (no artifact writes): `0F 73 E0 02`→None, `66 0F 73 E0 02`→None; 0F 71 E0 02→4, 0F 72 E0 02→4, 0F 73 D0 02→4, 0F 73 F0 02→4, 66 0F 73 D8 02→5, 66 0F 73 F8 02→5; exhaustive (op2,reg)×(66) sweep == contract tables EXACTLY (71:{2,4,6}/{2,4,6}, 72:same, 73:{2,6}/{2,3,6,7}); 0F BA reg 0..3 REJECT, 4..7 legal mod=0/1/2/3 (mod=2 len 8 with full disp32+imm8 vector); memory forms REJECT; F2/F3 REJECT | CONFIRMED (independent counter-execution) |
| 9 | D1 downstream falsifier: corrected = UNRESOLVED/NOT_VERIFIED/no promotion; BASE defect = CONFIRMED/PASS/0x00A0000E | MY OWN in-memory execution through BOTH module pairs: corrected x86dec+pebnd → UNRESOLVED/None source/NOT_VERIFIED/target None; committed BASE (THREE-P2) modules READ-ONLY import → CONFIRMED/KNOWN_FUNCTION_ENTRY/PASS/0x00A0000E; base module SHA identities re-verified (925963BD.../0ACA015B... match the record) | CONFIRMED (independent counter-execution) |
| 10 | .text census: ZERO occurrences of `0F 73` mod=3 reg=4 (both forms) | MY OWN full .text scan of the pinned EXE (own PE parser, .text 6,766,592 B @ 0x401000): 0 and 0 → the D1 repair could change no real stream (consistent with the byte-identical census/pins regression) | CONFIRMED (independent counter-measurement) |
| 11 | 3 CSV artifacts BYTE-IDENTICAL to BASE | Direct byte-compare of on-disk files vs `git show 9d31a82:...`: CORRECTED_PIN_LEDGER.csv, CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv, AF3_PROVENANCE_LEDGER.csv all identical (43A39A9A.../56A59917.../BF0968E3... both sides) | CONFIRMED (fresh regeneration, not copied) |
| 12 | C1/C2/C3 JSONs identical after excluding the declared `run` label; unit battery 64→72 (+6 new, 2 disclosed duplicates); boundary cases 13→14 (+D1 falsifier); NEW_G change = oracle-record filename only; oracle fixtures 71→80 (+9 D1) | Actual SHA re-hash of all 6 vs REGRESSION_DIFF sha256_new: 5/6 match, CQC_MUTATION_RESULTS MISMATCH (= finding F2); unit battery 72 entries, ok=false count 0, D1 vectors present incl. the 2 byte-duplicates; case set 14, only NEW_G changed and ONLY in field INDEPENDENT_ORACLE (old ORACLE_INDEPENDENT_RECORDS.json → new D1_INDEPENDENT_ORACLE_RECORDS.json — field-level diff vs BASE blob); fixtures 80 with all 9 D1 fixtures carrying full objdump command lines + raw stdout (`(bad)`/`data16 (bad)` verbatim for the two negatives, legal disassembly for the six controls) | CONFIRMED except F2 |
| 13 | Supersession ledger 9 records, quotecheck-verified | My own parser: 9 record headers (S-D1-01..03, S-D2-01..04, S-CM-01, S-AUD-01); 20 ORIGINAL_EXCERPT lines; ALL 20 excerpts verbatim substrings of their named READ-ONLY sources (0 failures) — including S-AUD-01 quotes against the Desktop report and S-CM-01 against 01_RAW/BASE_COMMIT_MESSAGE_VERBATIM.txt; declared count == measured | CONFIRMED |
| 14 | Manifest 38 rows, bijection, size+SHA256 all correct | 38 rows; 0 missing/extra/duplicate; 38/38 size and SHA256 re-hash true (incl. AUDIT_ENTRYPOINT.md at its BASE state, blob 6f28c045...); manifest self-excluded; = 37 package files + entrypoint == HANDOFF MANIFEST_ROW_COUNT | CONFIRMED |
| 15 | Identity pins: EXE / Desktop report / source manifest | EXE 8,015,872 B + E7785430... ✓; Desktop REPORT.md 15,535 B + 31AA87BC... ✓; source manifest 5,613 B + A407694E... ✓; BASE blob of c1_pin_ledger.py content-SHA 757225FE... ✓ | CONFIRMED |
| 16 | Baseline: HEAD == origin/master == actual remote == BASE_SHA; AUDIT_ENTRYPOINT untouched; foreign untracked paths untouched | rev-parse HEAD = 9d31a82; origin/master = 9d31a82; `git ls-remote origin master` = 9d31a82 (measured by me); `git diff 9d31a82 -- AUDIT_ENTRYPOINT.md` empty; git status shows only the 7 untracked paths (this package + the six foreign ones) — nothing staged, nothing modified | CONFIRMED |
| 17 | Gates Q1–Q14 PASS (committed CQC_FINAL.json, mode=docs) | gates dict: Q1..Q14 all "PASS"; QC_VERDICT=QC_PASS; Q14 detail: quotecheck 20 excerpts/0 failures, records 9==9 declared, commit-message fidelity true, required files missing [], P3_C ok, forbidden-extensions/http none | CONFIRMED (record + my predicate/code read) |
| 18 | Forbidden/overclaim phrase sweep clean | My own independent sweep (incl. the ledger ORIGINAL_EXCERPT exception rule): 0 real hits on FINAL_REPORT/HANDOFF/INPUT_IDENTITIES/SUPERSESSION_LEDGER/QC_REPORT | CONFIRMED |
| 19 | Core status algebra not promoted | All non-claims present verbatim: ASSIGNED_OBJECT_VTABLE=UNVERIFIED, OBJECT_POLYMORPHISM=NOT_ESTABLISHED, ULTIMATE_VALUE_SOURCE=UNKNOWN, WORLD_XYZ_RECOVERED=NO, PHYSICAL_RECORD_TO_WORLD_INSTANCE=NOT_ESTABLISHED, SPECIFIC_RUNTIME_GETTER_VALUE_PRODUCER=UNVERIFIED, 3×NOT_ESTABLISHED lifetime/preservation/closure invariants; no UNVERIFIED/UNKNOWN/NOT_ESTABLISHED/NO promoted anywhere in the package | CONFIRMED |
| 20 | Scope restrictions: no 0xA4 source/init, no placement, no templates.vfs/RECORD_A/Model 194013 execution, no client execution | Nonclaim strings present in FINAL_REPORT; Q14 forbidden-input census (instrument open-literal scan) clean; my own scan of all 11 instruments: the only `.vfs/.ark/.bnt/.nif` literals are the census's own forbidden-extension CHECK list (endswith tuple), no such file is opened; no http literals; temp trees under the authorized temp base | CONFIRMED |
| 21 | BASE module identities recorded in D1_BOUNDARY_FALSIFIER.json (base_x86dec_sha256 925963BD..., base_pebnd_sha256 0ACA015B...) | My own `git show` extractions of the SAME BASE blobs hash to EXACTLY 925963BD... / 0ACA015B... (see ARTIFACT_INDEX.csv script_diffs/BASE2_*): the executor's recorded BASE-module identities are true; the in-run BASE reproduction used the committed bytes | CONFIRMED |

Coverage algebra (L11): audited package files 38/38 read (16 root + 11 raw +
11 scripts; every load-bearing file read in full — FINAL_REPORT 366 l.,
QC_REPORT 137 l., HANDOFF 202 l., SUPERSESSION_LEDGER 198 l.,
INPUT_IDENTITIES 133 l., GENERATION_RECORD 126 l., EVIDENCE_INDEX 71 l.,
PE_MASTER_REVIEW 38 l., REGRESSION_DIFF 368 l., EXPECTED_PIN_REGISTRY 1320 l.
(structure + full field-compare via code), x86dec.py 671 l., cqc_battery.py
2787 l., pebnd/c1/c2/c3/capture/make_manifest via full unified diffs vs BASE
blobs + targeted sections, pin_roster 105 l., extract_expected_pins 71 l.,
diff_vs_base 400 l., raw JSONs via full parse + targeted field reads).
My QC working files (3 scripts + diff corpus) live only under
00_CONTROL_INTERNAL_QC/ and are NOT part of the executor manifest.

## 3. NOT_CHECKED (explicit)

1. The production battery `cqc_battery.py --mode data/docs` was NOT re-run by
   me: executing it would OVERWRITE the executor's committed artifacts in
   01_RAW (forbidden: evidence read-only for the QC worker). Instead I
   independently re-measured the same predicates via in-memory execution of
   the decoder/boundary functions (items 8-10 above) and full artifact parses.
2. GNU objdump was NOT re-executed: the 80 oracle records were verified for
   internal consistency (full command lines, verbatim stdout with `(bad)`
   verdicts, return codes, tool version string) and for set-composition
   (71+9), but the oracle binary itself was not re-invoked by me.
3. The mutation temp trees were NOT re-created (deleted after use by design);
   their effect is verified from the persisted per-case hashes/predicates and
   the harness code.
4. Process-order claims (oracle-first timing, the two disclosed repair rounds)
   are accepted from GENERATION_RECORD/QC_REPORT as consistent process
   disclosures; they cannot be re-derived statically. Their CONSISTENCY with
   the artifacts was checked (CQC_FINAL is the LAST run; QC_REPORT console
   line matches the record).
5. mtime-based execution ordering was not used as evidence anywhere.
6. The Desktop post-audit REPORT.md was hash-verified (identity pin) but not
   content-audited by me (the D1/D2 requirements were taken from the
   OpenCode dispatch contract, which I read in full).

## 4. Corrections returned (for PE-MASTER routing)

CORRECTION_REQUEST (single item, two sub-fixes, all within D1/D2 record
hygiene — NO new science):
- Fix F1: cqc_battery.py:2745 qc_scope literal + battery re-run
  (data+docs) — executor (pe-reconstruction) task.
- Fix F2: diff_vs_base.py re-run AFTER the final battery + manifest
  regeneration — executor task; manifest regeneration is already mandatory
  for the persistence phase (entrypoint row).
Both must be followed by the manifest bijection re-verification and a
check that 14/14 gates + 15/15 mutations are unchanged. If PE-MASTER instead
chooses to publish with the findings disclosed in the PE-MASTER review, the
two defects must be recorded as open P2 record defects in the package
handoff (they do not invalidate the D1/D2 scientific results, which I
independently reproduced).

## 5. Verdict

QC_PASS_WITH_FINDINGS. The D1 per-opcode repair, the D2 roster-bound gate,
all 15 causal mutations, the regression identities, the retractions, the
manifest and the identity pins are INDEPENDENTLY VERIFIED from physical
evidence (including my own in-memory counter-executions of the decoder and
boundary machinery on both the corrected and the committed BASE modules).
The two P2 findings are record/provenance defects (a stale QC-scope label in
the committed battery record; a stale intermediate SHA in REGRESSION_DIFF)
that do not change any measured result, but are real, must not be silently
absorbed, and are cheap to fix inside the already-planned persistence phase.
