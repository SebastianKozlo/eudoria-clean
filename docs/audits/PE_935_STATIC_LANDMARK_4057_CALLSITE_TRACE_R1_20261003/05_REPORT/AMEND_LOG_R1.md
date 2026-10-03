# AMEND LOG — R1 QC REPAIR ROUND — PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003

```text
RUN_ID     = PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003
ROUND      = R1 — the single authorized QC repair round (contract §6
             QC_REPAIR_ROUNDS_MAX = 1)
DATE       = 2026-10-03
EXECUTOR   = pe-reconstruction (author of the original science package)
SCOPE      = DOCUMENTATION / EVIDENCE-CONSISTENCY ONLY
BASE       = QC verdict QC_PASS_WITH_FINDINGS (0×P0, 0×P1, 1×P2, 5×P3;
             04_QC/TARGETED_QC_REPORT.md)
RULES      = NO scientific measurement repeated; NO new science; every measured
             VALUE/status stays exactly as measured; all changes scripted and
             reproducible from 03_SCRIPTS; every modified/created file recorded
             below with BEFORE/AFTER SHA256 (BEFORE hashes computed before each
             edit).
LOG_FILE   = 05_REPORT/AMEND_LOG_R1.md (as required by the dispatch; placed in
             05_REPORT/ — not elsewhere)
```

## 1. Generator scripts added (03_SCRIPTS — authorized as bounded regeneration scripts)

```text
s12_falsifier_reach_check_v2.py  (CREATED in R1)
  - Regenerates 01_RAW/FALSIFIER_REACH_CHECK.json over ALL 18 measured functions
    (g1..g6) from the curated 01_RAW JSON artifacts ONLY (no Ghidra, no scratch,
    no binary access — no new science). Fail-closed row-consistency assertions:
    18 rows; exactly 1 machinery hit {from 0x00823C57, target 0x004D1430} in
    G5_H03_extract_00823c10; 0 registry-edge VAs. Also regenerates
    03_SCRIPTS/SCRIPT_SHA256.csv (no BOM, no blank lines, hashes recomputed
    after all final script edits; 19 rows incl. s12 + s13).
  - Supersedes the s7_curate_g4.py-written 13-function artifact (stage S7; the
    only version that actually shipped in the original package) and the
    never-landed s8_curate_g5.py regeneration.

s13_amend_r1_doc_patch.py  (CREATED in R1)
  - Scripted, reproducible documentation patch: 23 exact-match replacements
    across 9 text files (fail-closed two-phase: every replacement verified
    exactly-once against the pristine files BEFORE any write). Dash/arrow/
    section-sign variant tolerant; line-ending preserving; whitespace-run
    tolerant fallback tier.
  - Pre-verifies the F-P3-4a wording against the committed raw evidence before
    writing it (G1 series-slot check: 0xFD4..0xFD8 => LEA ECX,[ESP+0x2C],
    0xFD9 anchor => LEA ECX,[ESP+0xC8] — PASS, matches QC F-P3-4a).
```

## 2. Per-file amend records (BEFORE hash -> AFTER hash)

All BEFORE hashes were computed before any edit to that file (10 files hashed
in the first pre-edit inspection; NEGATIVE_CONTROLS.md and TRANSFORM_PROVENANCE.md
hashed at the start of the first patch call, before any write).

| file | finding(s) | what changed | BEFORE SHA256 | AFTER SHA256 |
|---|---|---|---|---|
| 00_CONTROL/RUN_BUDGET.md | F-P3-2 | final ledger row NEW_PCG_FUNCTIONS_DETAILED=19/60 -> 18/60 | 2109ae3066833bacd7d045cfd2d8a1ddf19a8359ae4620e830b7266243095ecc | 31b91440f96c1489a13be8de9e6197dfad53e7fc22ea1fd6cd2fb9040892c88a |
| 01_RAW/FALSIFIER_REACH_CHECK.json | F-P2-1 | REGENERATED via s12: 18 per_function rows (g1..g6 census G1:1 G2:5 G3:5 G4:2 G5:4 G6:1), the single generic hit FUN_004D1430 @0x00823C57 inside FUN_00823C10 recorded WITH classification GENERIC_SHARED_MAP_FIND__NOT_A_TEMPLATE_REGISTRY_EDGE + full reason; totals row-consistent: total_functions_checked=18, TOTAL_DIRECT_TEMPLATE_MACHINERY_HITS=1, TOTAL_GENERIC_MACHINERY_HITS=1, TOTAL_TEMPLATE_REGISTRY_EDGES=0; supersedes + amend + QC-cross-check provenance blocks | 95e33cf4c6871012ddb31b135fc11724dc0cb2e25984041238985d85cb1eb275 | 09f5989cb2864bd1c691e75f211be1d7770cf3b0f42b79d9c38f3c8be7abf521 |
| 02_ANALYSIS/RETRACTIONS_SUPERSESSIONS.md | F-P2-1, QC-note-2 | R-2 rewritten (artifact history corrected: s7 13-function version shipped; s8 regeneration never landed; R1 s12 regeneration over 18 functions described); R-1 appended the sids data nuance (first payload entry = empty string, id 2021; layout still closes exactly with 3,887 entries) | 5e6c9da9015c5f783bec877d95d9936b75849d0d5d39ff4f2ac7e781ab97cc39 | c56d6588a9e86f52c1d8af97a56e380cb4bfa41eba8dbe54f0a3d5e15c545a0a |
| 02_ANALYSIS/TEMPLATE_ROLE_TEST.md | F-P2-1, F-P3-4a | §4 heading + intro corrected (artifact regenerated over g1..g6 — R1 amend; 18 functions); G6 census row note corrected (row now regenerated INTO the artifact); TOTAL line added (18 functions checked; 1 generic-machinery hit; 0 template-registry edges; QC Q8 cross-cited); §5 wording fixed: same PUSH -> same callee FUN_008DFCD0 / same arg1 class, but NOT byte-identical call shapes (0xFD4..0xFD8 this = LEA ECX,[ESP+0x2C] vs 0xFD9 anchor this = LEA ECX,[ESP+0xC8] — different this-pointer slots; verified from the g1 listing pre-write) | 6c85476cf97e2674d0751b1483ad4c5e22369b411ba9824a28499cc6ffed1fba | b1c143cd0af2a66b743be909c8848dd15ffa71cdc23dbd1fc9bdff54753f01c3 |
| 02_ANALYSIS/CLAIM_MATRIX.csv | F-P2-1, F-P3-2, F-P3-3 | full rewrite: header gains value_or_result; status column now STRICTLY the §23 five-word taxonomy; value_or_result carries the §29-style precise values verbatim (no information lost; no measured fact changed); C4057-08 method fixed (18 measured functions g1..g6) + independent_countercheck fixed (regenerated artifact totals + QC Q8 cross-cited); C4057-12 claim text 19 -> 18 | 13808099787a612783ebc6ce717a1cfb2841213deba9283aeafc93499d9a1bcb | e793e3887d2c96a78f7bcd95b1ab9025b8de53886f6326794583aae8f40604c8 |
| 02_ANALYSIS/CALLSITE_DATAFLOW.md | F-P3-1, QC-note-1, QC-note-2 | §3 STEP 8 row relabeled: PUSH ECX (51) address 0x00821C27 -> 0x00821C2C (verified from the G3_E02 listing pre-edit: 0x00821C27 = 8D 44 24 20 LEA EAX; 0x00821C2B = 50 PUSH EAX; 0x00821C2C = 51 PUSH ECX; semantics unchanged); §2 appended the R1 RTTI chain-walk QC note (all three facts; behavioral identity NOT upgraded); §4 appended the sids data nuance | 9d01ab6525a7570d7a704d7032b3468b589c11e231c35e1ec4da79b6adfbee34 | 378fe5ab1ef6d418ee29d7b1704efa1d427ba16dbfe8ff95384fc3d8991a2cca |
| 02_ANALYSIS/OBJECT_IDENTITY_TRACE.md | QC-note-1 | O4 bullet appended the R1 RTTI chain-walk QC note (vtable 0x00A7A948 -> COL 0x00A9EDD4 -> TD 0x00B6E084 = .?AVComponent@ArkUI@@; executor + QC agree; behavioral identity not upgraded); §3 appended the caller-side RTTI chain-walk QC note (gate TD 0x00B7DDE8 = .PAVArkRepairUI_Impl@@; unwind vtable 0x00A80704 -> .?AVArkRepairUI@@) | 46950c304fc3c77c346350ff5a5ffb2dc22b3fa3d780b3b9c4f291ecbe998cc4 | c5ae0ad6c5c74654a927345ad680e1a3127e92380105faa253e9f19d0b769b26 |
| 02_ANALYSIS/NOT_CHECKED.md | F-P3-2, QC-note-1 | Budget-relevant counts: NEW_PCG_FUNCTIONS_DETAILED = 19 -> 18 (the enumeration already listed exactly 18 names); N-07 appended the R1 RTTI chain-walk QC note (all three facts confirmed by QC; N-07 remains an honest record of the EXECUTOR's own run scope; behavioral identity not upgraded) | c93adaa85262f094e2d6f4594d10ec1beb7e0e647b60d6b65ed7c50f88d5cce3 | 2ff669c6119ef076124b358001c7903596e28c88043580242b9d5e62d3ac55c0 |
| 02_ANALYSIS/NEGATIVE_CONTROLS.md | F-P3-2, F-P3-4b | CONTROL-1: reach-check "all 19 measured functions" -> 18; CONTROL-2: "62 unique PUSH imm32 values" -> "62 unique PUSH immediate values (NOT an imm32-only census: ... includes imm8/0x6A-form pushes such as the small integers 0..0x16 and 0x3C; QC's independent imm32-only/0x68-form byte census found 49 unique imm32 values — 04_QC F-P3-4b)"; CONTROL-4: "measured 19-function path" -> 18-function | 353860f412a560b127f03abf0bec617d5e851ea81e66ca2f7b5fed6d815f4a3b | 11f8b2b9a8fda99858703320dbb0ea4ba1424a50439b5df75da113a49759ff22 |
| 02_ANALYSIS/TRANSFORM_PROVENANCE.md | F-P3-2 | §3: "anywhere in the 19 measured functions" -> 18 | bd5bb116d13abf74571378cce28a0a1c3f35397b00d601e6de9df421d7d66d2a | 7054ca76121995701ed62f38d1c6558c6f6093cd495692325b3fa0a46772ce9f |
| 03_SCRIPTS/SCRIPT_SHA256.csv | F-P3-5 | REGENERATED via s12: UTF-8 WITHOUT BOM; no blank lines (the original's mid-file blank line is gone); rows now 19 scripts (17 original + s12 + s13 added in R1); every hash recomputed after all final script edits; verified: DictReader yields 19 rows with clean `script` key, 0 hash mismatches vs recomputation; file ends with exactly one LF after the last data row | c391672224dfa508f173dd48299c9fd0ec384d8f3b045d731846206d7a73bee5 | d2543781f597daf1d46afeda479ceaecfcf9a7d9b42659beeba70098f0f8f48a |
| 05_REPORT/DRAFT_FINAL_REPORT.md | F-P3-2, QC-note-1, QC-note-2 | Part A answer 4: reach-check 19 -> 18; answer 5: sids data nuance added; answer 12: 19 -> 18; answer 18: RTTI QC note added; Part B: NEW_PCG_FUNCTIONS_DETAILED 19 -> 18 (H-series double-count phrase removed; the enumeration 1+5+5+2+4+1 = 18); Part C item 10: RTTI QC note added | 20cb593a8fe6e07a8ed4e9023ddd235523a6d673c04af833698fd55ec0136c4a | c4c5696fd75da000f4e848686a1c9aed67301f48561b3cbeed9e2ec2f0d644ef |
| 03_SCRIPTS/s12_falsifier_reach_check_v2.py | F-P2-1, F-P3-5 | CREATED in R1 (generator; see §1) | CREATED (no BEFORE hash) | 15e6a8086299aa160be4f950581297389e7279132433266afca32ee6b30bfcb7 |
| 03_SCRIPTS/s13_amend_r1_doc_patch.py | all text findings | CREATED in R1 (documentation patch; see §1) | CREATED (no BEFORE hash) | d6422bdad38c027b01039fb50ecd0e1628bff9424d64c334d39d2e396ed7efbf |
| 05_REPORT/AMEND_LOG_R1.md | (this log) | CREATED in R1 (this file) | CREATED (no BEFORE hash) | not self-embedded (self-reference; computable post-write) |

## 3. Findings disposition

```text
F-P2-1 (P2)  FIXED. 01_RAW/FALSIFIER_REACH_CHECK.json regenerated by s12 over
             all 18 measured functions; the single machinery hit (shared
             GENERIC mapfind FUN_004D1430 @0x00823C57 inside FUN_00823C10,
             string-table manager map @[mgr+4], singleton DAT_00BA12F4) is
             recorded with classification GENERIC_SHARED_MAP_FIND__NOT_A_
             TEMPLATE_REGISTRY_EDGE + full reason (different singleton than the
             registry's DAT_00BA1824, referenced only in getter FUN_0043A550;
             composite key; string values; FUN_0072F580 not on the path).
             New totals, row-consistent by construction and verified:
             total_functions_checked = 18 = len(per_function);
             TOTAL_DIRECT_TEMPLATE_MACHINERY_HITS = 1;
             TOTAL_GENERIC_MACHINERY_HITS = 1;
             TOTAL_TEMPLATE_REGISTRY_EDGES = 0.
             QC's independent confirmation is cited (same single hit over 18
             windows — 04_QC Q8), but the artifact itself is this run's own
             script's output (reproducible: python 03_SCRIPTS/
             s12_falsifier_reach_check_v2.py). Old-shape texts fixed: R-2
             (RETRACTIONS), §4 (TEMPLATE_ROLE_TEST), C4057-08 method/
             independent_countercheck (CLAIM_MATRIX). Per-verification census:
             G1:1 + G2:5 + G3:5 + G4:2 + G5:4 + G6:1 = 18 rows.
F-P3-1 (P3)  FIXED. CALLSITE_DATAFLOW.md §3 STEP 8 row now reads
             "0x00821C2C  51 / 0x00821C2B 50  PUSH ECX / PUSH EAX" (verified
             from the committed G3_E02 listing BEFORE editing: 0x00821C27 is
             LEA EAX,[ESP+0x20]; PUSH ECX byte 51 is at 0x00821C2C;
             semantics unchanged). Satisfies QC's revalidation predicate
             ("byte table row must read 0x00821C2C 51").
F-P3-2 (P3)  FIXED everywhere stated: 19 -> 18 in 00_CONTROL/RUN_BUDGET.md
             (final ledger), 05_REPORT/DRAFT_FINAL_REPORT.md (Part B budget
             table + answers 4 and 12), 02_ANALYSIS/NOT_CHECKED.md (budget-
             relevant counts), 02_ANALYSIS/NEGATIVE_CONTROLS.md (CONTROL-1,
             CONTROL-4), 02_ANALYSIS/TRANSFORM_PROVENANCE.md §3,
             02_ANALYSIS/TEMPLATE_ROLE_TEST.md §4, 02_ANALYSIS/CLAIM_MATRIX.csv
             (C4057-12). Post-patch package-wide scan for leftover count
             patterns ("19 measured functions", "19-function", "=19/60",
             "NEW_PCG_FUNCTIONS_DETAILED = 19", "All 19 functions",
             "60      19") = ZERO hits.
F-P3-3 (P3)  FIXED. CLAIM_MATRIX.csv: status column now uses ONLY the §23
             taxonomy (CONFIRMED / STRONGLY_SUPPORTED / PLAUSIBLE / UNVERIFIED
             / REJECTED); a new value_or_result column carries the §29-style
             precise values verbatim (PRESENT/NOT_ESTABLISHED/NO/compounds).
             No measured fact changed. Mapping rule documented in §5 below.
F-P3-4 (P3)  FIXED (a + b). (a) TEMPLATE_ROLE_TEST §5 reworded precisely:
             same callee FUN_008DFCD0 + same arg1 class, but NOT byte-identical
             call shapes — 0xFD4..0xFD8 pass this = LEA ECX,[ESP+0x2C] while
             the 0xFD9 anchor passes this = LEA ECX,[ESP+0xC8] (different
             this-pointer slots). The wording was VERIFIED against the
             committed g1 listing pre-write (s13's G1 series-slot check PASS:
             fd4..fd8 -> 2c, fd9 -> c8). (b) NEGATIVE_CONTROLS CONTROL-2
             reworded to "62 unique PUSH immediate values (NOT an imm32-only
             census ...)" citing QC's independently measured 49 unique
             imm32-only values (04_QC F-P3-4b).
F-P3-5 (P3)  FIXED. SCRIPT_SHA256.csv regenerated without BOM and without
             blank lines; hashes recomputed AFTER all final script edits
             (19 rows; 0 mismatches on re-verification; DictReader clean).
```

## 4. QC confirmation notes (additive bookkeeping)

```text
QC-note-1 (RTTI): notes added at every primary labeling site: OBJECT_IDENTITY_
  TRACE.md (O4 bullet + §3), NOT_CHECKED.md N-07, CALLSITE_DATAFLOW.md §2,
  DRAFT_FINAL_REPORT.md (answer 18 + Part C item 10). Content: QC's
  independent chain walks (04_QC Q6) CONFIRM the three chain-walk facts
  (gate TD 0x00B7DDE8 = .PAVArkRepairUI_Impl@@; unwind vtable 0x00A80704 ->
  .?AVArkRepairUI@@; store vtable 0x00A7A948 -> .?AVComponent@ArkUI@@).
  Executor + QC now agree on the chain-walk facts; class BEHAVIORAL identity
  remains exactly as before — NOT upgraded to behavioral semantics anywhere.
QC-note-2 (sids nuance, record-only): added where the sids parse is
  documented — RETRACTIONS R-1, CALLSITE_DATAFLOW §4, DRAFT answer 5. Content:
  the first sids payload entry is an empty string with id 2021; the payload
  still closes exactly under the documented layout with 3,887 entries
  (QC-confirmed, 04_QC).
QC-note-3 (tool-call count): CONFIRMED — the PACKAGE LEDGER value (84/120,
  RUN_BUDGET.md + DRAFT Part B) is authoritative; the "86" in the original
  chat handoff was a paraphrase error (04_QC Q15 confirmed no package-internal
  inconsistency). NO package change was needed or made for this. This R1
  repair round ran under its OWN separate budget (§6) and is NOT added to the
  original run's 84.
```

## 5. CLAIM_MATRIX status mapping rule (F-P3-3)

```text
status (§23 taxonomy) is the epistemic grade of the claim's substance;
value_or_result carries the old §29-style status text VERBATIM (zero
information loss). Mapping applied:
  CONFIRMED (old status)          -> status CONFIRMED
  PRESENT                          -> status CONFIRMED, value PRESENT
  REJECTED_FOR_THIS_CALLSITE
    (test result: falsifier FIRED) -> status REJECTED, value verbatim
  NOT_ESTABLISHED* (09/10/11/12/
  14, incl. compounds)            -> status CONFIRMED, value verbatim
    (rationale: these are MEASURED-ABSENCE / resolved-negative claims whose
    substance QC independently confirmed from bytes — Q8..Q14 all PASS; the
    §29 quantity itself remains NOT_ESTABLISHED and is preserved verbatim in
    value_or_result)
  NO (15)                         -> status CONFIRMED, value "NO"
    (the claim "placement NOT recovered" is a measured negative QC confirmed,
    Q12; the §29 gate value NO is preserved verbatim)
  UNVERIFIED (13)                 -> status UNVERIFIED, value "UNVERIFIED"
  C4057-16 compound               -> status CONFIRMED, value verbatim
If PE-MASTER's §23 semantics grade these differently, no information is lost:
value_or_result preserves every §29 value exactly as measured.
```

## 6. Honest non-promotions and instrument notes

```text
1. F-P3-4b opcode recount NOT promoted: an in-round re-tabulation of PUSH
   encodings from the committed g1 listing produced instruction counts that
   did not exactly reconcile with the committed census object (137 PUSH-
   immediate instructions in the listing vs 136 entries in
   CALLSITE_DATAFLOW_WINDOWS.json immediate_census_function_wide.
   push_imm32_instructions). Per the no-new-science / no-new-inconsistency
   constraint, NO recount numbers were promoted into the package: the fixed
   wording keeps the committed 62-value census and cites QC's independently
   measured 49 unique imm32 values (04_QC F-P3-4b) instead.
2. s13 development history (fail-closed discipline): two development
   attempts aborted WITHOUT writing any target file (a phase-1 exact-match
   assertion on the DRAFT Part C region — a dash/whitespace variant issue —
   and one Python syntax error caught before execution by pre-run ast.parse
   validation). The committed s13 (v3) is the version that ran successfully:
   23/23 replacements, all verified exactly-once before any write. The only
   intermediate file states were the s13 script itself (a NEW R1 file, not a
   target document).
3. SCRIPT_SHA256.csv trailing newline: the regenerated CSV ends with exactly
   one LF after the last data row (standard text-file terminator; the QC
   parse check passes: csv.DictReader yields 19 rows with a clean `script`
   key). The defects QC flagged — UTF-8 BOM and the blank line — are gone.
4. Science statuses explicitly unchanged: IMMEDIATE_4057_IS_TEMPLATE_ID =
   REJECTED_FOR_THIS_CALLSITE; LANDMARK_TRACE_LEVEL = 0;
   MANDATORY_FALSIFIER_RESULT = FAIL_NUMERIC_COINCIDENCE; all data-side
   repins and every measured value unchanged.
```

## 7. Budget (this R1 round only)

```text
PLANNED : 30 tool calls / 60 wall minutes (dispatch hard limit)
USED    : 27 tool calls (self-counted per tool invocation, incl. reads,
          greps, writes, bash) / ~50 wall minutes (self-reported session
          clock; declared-not-machine-measured)
```

## 8. Scope attestation

```text
- Modified files are EXACTLY those enumerated in §2 (12 modified + 3 created,
  incl. this log); all inside the package.
- 04_QC/ (TARGETED_QC_REPORT.md + raw/*) UNTOUCHED.
- NOTHING outside the package was modified; helper scripts were written only
  to the pre-approved temp dir (C:\Users\User\AppData\Local\Temp\opencode).
- NO git state created: no stage, no commit, no push, no config change
  (publication is NOT assigned to this round).
- No scientific measurement repeated; no new science; the only binary/raw
  reads were of already-committed package artifacts (01_RAW JSONs) for
  verification and regeneration.
- Post-patch verification (scripted): FALSIFIER totals row-consistent
  (18/1/0 = True); SCRIPT_SHA256.csv 19 rows, 0 hash mismatches, no BOM;
  leftover bad-pattern scan over 00_CONTROL/02_ANALYSIS/05_REPORT = ZERO
  hits; positive checks (TROLE totals line, slot wording, STEP-8 row) all
  PASS.
```
