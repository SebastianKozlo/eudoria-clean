# QC_REPORT — PE_935_CAND4_006C9700_PLUS4_RESIDUAL_POST_AUDIT_CORRECTION_R1_20261008

QC_RUN_ID = PE_935_CAND4_006C9700_PLUS4_RESIDUAL_POST_AUDIT_CORRECTION_R1_20261008_INTERNAL_QC_R1

## 0. REAL origin

**pe-master-auditor fresh-context internal QC, internal to PE-MASTER — NOT an
independent Desktop post-audit, NOT executor self-review.** This QC is the
contract §7(b) fresh-QC parent phase of the residual correction run. It is
NOT a substitute for the external ChatGPT Desktop post-audit of the resulting
SHA (NEW_DESKTOP_POST_AUDIT = NOT_PERFORMED), NOT a PE-MASTER advisory review
(separate parent phase), NOT milestone closure and NOT canonical promotion
(CANONICAL_GATE_EFFECT = NONE; ADVISORY_PRE_QUALIFICATION standing
unchanged).

QC_VERDICT: **PASS** (internal QC of this run's machinery and records; scope
statement in §8).

## 1. Method

Independent counter-measurements, never a replay of the executor's evidence:

- **Own implementation.** This QC wrote its own fixed independent QC mapper
  `03_SCRIPTS/qc_countercheck_v2.py` (89938 B / SHA256
  F57988BC7DB255E70C0EEE7E6B3A7BD4C3F2045078233C90FD81F499B5AF4402,
  1778 lines) — class `QCPEv2`, own synthetic builder `build_minipe2`
  (Desktop layout e_lfanew=0x80, COFF @0x84, Magic @0x98, ImageBase @0xB4),
  own oracle arithmetic (`qc_oracle_expectation`,
  `qc_oracle_constructor_stage`), own observation helpers. It is NOT a
  re-export of the production `RangeSafePE`/`RangeSafePEv2` classifier; the
  code lineage continues this QC family's historical `qc_countercheck.py`
  QCPE style with the residual P2-A/P2-B defects FIXED. Executed:
  `python -B 03_SCRIPTS/qc_countercheck_v2.py`; raw machine-readable
  evidence: `00_CONTROL_INTERNAL_QC/QC_COUNTERCHECK_V2_RAW.json`.
- **PRE discipline.** The historical QCPE was **AST-EXTRACTED** from the
  READ_ONLY SOURCE_RUN `qc_countercheck.py` (verified 40309 B /
  11957F40…; only the listed definition nodes compiled and executed in a
  fresh namespace — QC_RAW/QC_BSS/QC_UNMAPPED/QC_REJECT, QCReadError, QCPE,
  make_minipe, sha256_bytes, sha256_file, parse_hex, _try_read; **main() and
  every other top-level statement never executed**). The SOURCE_RUN
  production checker was imported via importlib only after a FULL inertness
  read (620 lines; definitions only, main() under `__main__`).
- **POST discipline.** The PACKAGE production v2
  (`checker_plus4_successor_v2.py`, 776 lines, read IN FULL for inertness;
  measured SHA256 80EBEE27883AA61173737590FB822B3503B4658CDA511B4B690F8E75B
  6B64E62, identical before and after this QC) was imported and re-executed
  — clearly labeled PRODUCTION replay, never presented as independence.
- **Non-circular oracles.** Every expected classification is computed by
  this runner's OWN interval arithmetic; replay of production is never an
  independence source. Every essential PASS records MEASURED_QUANTITY,
  INDEPENDENT_SOURCE_OF_TRUTH, WHY_NON_CIRCULAR and
  FAILURE_CASE_DETECTED in the raw output.
- **Identities fail-closed.** Contract (23137 B / 2634BA31…C6969), Desktop
  ADVERSARIAL_COUNTERCHECKS.json (16079 B / 62646637…), EXE (8015872 B /
  E7785430…), SOURCE_RUN pins, historical checker (12749 B / F58D2DB3…),
  entrypoint (263460 B / 87FF3314…) — all verified by this QC's own
  measurements; full EXE re-hash before all reads AND after all controls
  (unchanged).

## 2. Duty results

### D1 — Desktop P2-A mapper cases (contract §2 list 1–5) — PASS (18/18)

All four Desktop false-passes reproduce on the historical QCPE (PRE) with
**byte parity with the Desktop corpus and the executor's 00_PRE**: reads
RETURNED `41 41 41 41` classified `QC_RAW_BACKED` for
VA=0x0040104F/n=4 and VA=0x0040106F/n=4 on the overlapping A/B geometry, and
for VA=0xFFFFFFFE/n=4 and VA=0x100000000/n=4 on the near-4GiB fixtures (the
Desktop corpus records these as `READ_SUCCESS`/`41414141`; the
RETURNED↔READ_SUCCESS difference is vocabulary, not measurement — mapping
documented in QC_RESULTS.json). On this QC's own QCPEv2 (POST) and on
production v2 every one is a controlled REJECT: the overlap cases fail as
"ambiguous: 2 sections INTERSECT", the 4GiB cases are rejected by address
arithmetic BEFORE section matching.

Positive boundaries measured, not assumed: VA=0xFFFFFFFF,n=1 → RAW byte
`41`; VA=0xFFFFFFFE,n=2 → `41 41` (exclusive endpoint == 2**32 is VALID);
VA=0xFFFFFFFE,n=4 and VA=0x100000000,n=4 → INVALID (no bytes). Positive
non-overlap/endpoint-touching read inside .s1 touching .s2's start →
RAW_BACKED; crossing/touching range → REJECT; historical full-overlap
rejection preserved; a ONE-BYTE intersection case (each section intersected
in exactly one byte) rejects — the historical containment-only matcher would
classify it UNMAPPED (regression detection). QC extra falsifiers: B's raw
bytes set to 0x42 on the same geometry (a containment-only false pass would
provably return the WRONG section's bytes); raw→BSS crossing from the last
raw byte → controlled VIRTUAL_BSS-classified read FAIL, never fabricated
bytes. The base+0x7FFFFFFF control is retained RELABELED (UNMAPPED far
beyond the image — not a PE32 overflow test; the real boundary tests are the
4GiB cases). Ordinary pin VA=0x006E8FA5,n=3 → `89 46 04` on the physical EXE;
BSS VAs 0x00BA1100/0x00BA73BC → VIRTUAL_BSS, zero bytes fetched (this QC's
own reads). GENERAL_PE_MAPPER_CORRECTNESS stays NOT_ESTABLISHED.

### D2 — P2-B truncated optional header (contract §3) — PASS (9/9)

On the exact Desktop fixture layout, sizes 0x98/0x99 let a raw
`struct.error` escape from the historical QCPE and production v1
("unpack_from requires a buffer of at least 154 bytes for unpacking 2 bytes
at offset 152 (actual buffer size is 152/153)") and 0xB4/0xB7 escape at the
ImageBase field ("…184 bytes for unpacking 4 bytes at offset 180…") —
**byte-identical to the Desktop messages and the executor's PRE raws**
(parity confirmed). On QCPEv2 (and production v2) every truncation is a
controlled rejection at the exact stage: 0x98/0x99 at the Magic stage,
0xB4/0xB7 at the ImageBase stage. Probes measured: 0x9A — PRE escaped a raw
struct.error at the ImageBase field; POST controlled at the ImageBase stage.
0xB8 — already controlled in the historical QCPE (incomplete section table)
and controlled at the section-table stage on v2. 0x190 — mid-section-table
probe, controlled at the section-table stage. 0x1C0 — CONSTRUCTED on all
four implementations (headers complete). Positive intact control:
CONSTRUCTED with EVERY measured fixture header field equal to the intended
value (e_lfanew 0x80, PE signature, machine 0x14C, nsec 1, size_opt 0xE0,
Magic 0x10B, ImageBase 0x00400000, section table @0x178) — this QC's own
field measurements, all_match = true.

### D3 — P3 wrong-callsite identity gate (contract §5) — PASS

This QC built its OWN isolated scratch fixtures under
`00_CONTROL_INTERNAL_QC/scratch/` (CLEAN copy, W1 teleport to 0x006C97D8,
W2 RECORD_ID-only, W3 generality 0x006CB7CF; the SOURCE pins JSON and the
physical EXE never mutated) and replayed them through the checkers' NORMAL
loader paths.

- PRE parity (original production checker): W1/W2/W3/CLEAN all FALSE-PASS
  **86/86** — the Desktop's expected PRE result, reproduced exactly by this
  QC's own replay. The fixed-address QC comparison detects W1/W3
  (MISMATCH_DETECTED) but NOT W2 (MATCH_NO_MISMATCH — honest negative:
  nothing compared the RECORD_ID; only the identity gate catches it).
- POST (production v2, re-executed by this QC): CLEAN scratch copy through
  the normal loader path **87/87** (and 87/87 via the default pinned SOURCE
  path); W1, W2 and W3 each FAIL **exactly** on `RECW:W_RECORD_IDENTITY`
  (86/87) with the historical 80 and the SIX original RECW checks all PASS —
  no SHA mismatch, missing-file exception or unrelated pin failure rescues
  the verdict (the replays ran on the REAL pinned EXE). Denominators honest:
  80 + 6 + 1 = 87.
- Identity oracle non-mutatability (independently verified): structural
  census over the full v2 source — exactly ONE module-level
  `CANONICAL_RECORD_IDENTITY = {"W_CTOR_CALL_AT_006CB836": 0x006CB836}`,
  zero later assignments, zero JSON-driven writes; behavioral: W1 proves the
  JSON cannot rebind the canonical id, W2 proves an unknown id fails closed,
  W3 proves the binding is callsite-exact. CONFIRMED non-mutatable
  module-internal oracle independent of the fixture JSON.
- The clean W callsite passes byte pin `E8 75 F0 02 00`, rel32 `+0x2F075`
  and target `0x006FA8B0` (see D4).

### D4 — W byte pin own read — PASS

This QC's own QCPEv2 read at VA 0x006CB836: bytes `E8 75 F0 02 00`, own
signed-rel32 recompute `+0x2f075`, next VA 0x006CB83B, target
`0x006FA8B0`; physical file offset 0x2CB836 with an independent direct
file-slice crosscheck at that offset returning the identical 5 bytes; the
SOURCE record fields match this QC's own measurement field-by-field.

### D5 — 80-ID regression own re-execution — PASS

The 80 required IDs (EXE_IDENTITY + 57 PIN + 16 REL32 + 3 RTTI + 3 STR;
no duplicates) AST-parsed READ_ONLY from the historical PROVENANCE checker
(pinned SHA verified) and re-executed by THIS QC's own reads and arithmetic:
**80/80 PASS**. Tables element-identical: v2 vs historical 4/4, v2 vs the
SOURCE_RUN successor 4/4. The executor's REGRESSION_RESULTS.json required-ID
list is identical to this QC's own; its verdict PASS agrees with this QC's
independent re-execution.

### D6 — P2-C records content re-adjudication — PASS

- CORRECTED_CLAIM_MATRIX.csv: 21 data rows (22 physical rows with the
  header). Retraction (a) executed: R_W_SEPARATENESS is now a SCOPED
  STRUCTURAL FACT (CORRECTED) — the R/W construction evidence (6A 10 vs 6A
  0C pushes, separate construction sites and callers, the CAND-4 path
  creates no W) preserved IN FULL, the unsupported later-T part "T != W"
  REMOVED from the active claim, explicitly not a universal
  object/class inequality nor a lifetime identity theorem. Retraction (b)
  executed: R_NOT_EQUAL_T_AT_LATER_USE = NOT_ESTABLISHED_WITHIN_BOUND — the
  historical ACTIVE "R != T stays" (SOURCE ledger FD-C2/SL-9 corrected-active
  text) is superseded; NEITHER equality NOR inequality established; R, P, T,
  W, field addresses, owners and classes never conflated. Explicit
  unknown-status rows present for BOTH inequalities
  (T_NOT_EQUAL_W_AT_LATER_USE and R_NOT_EQUAL_T_AT_LATER_USE =
  NOT_ESTABLISHED_WITHIN_BOUND). Preserved statuses verified:
  T_EQUALS_FIRST_INITIAL_P = NOT_ESTABLISHED_WITHIN_BOUND;
  R_PLUS4_VALUE_PRESERVED_TO_LATER_USE = NOT_ESTABLISHED; P_HEAP_ORIGIN =
  NOT_ESTABLISHED; P_ALLOCATION_OR_STORAGE_ORIGIN =
  NOT_ESTABLISHED_WITHIN_BOUND; R_PLUS4_FIRST_INITIALIZATION =
  PRESERVED_CONFIRMED_STATIC_CONDITIONAL. SCOPE_BUDGET_RECORDS row: floor
  17, bodies 5, edge budget 12 → original scope FAIL preserved; exact counts
  UNRESOLVED; RETROACTIVE_PRIOR_AUTHORIZATION = NO.
- SUPERSESSION_LEDGER.csv: 8 data rows (9 with the header), RS-1..RS-8;
  RS-1 retraction (a), RS-2 supersession of the R!=T active assertion,
  RS-3 explicit 10-location census, RS-4 prior-supersession confirmation,
  RS-8 discloses HISTORICAL_FIRST_QC_PRE = LOST_OR_NOT_AVAILABLE (the
  SOURCE_RUN QC_RESULTS.json's overwritten first raw output NOT claimed
  recovered — distinct from THIS run's fresh PRE evidence, which this QC
  verified immutable).
- Active-overclaim sweep of the PACKAGE (this QC's own regex census):
  ZERO active T==P / heap-origin / WITHIN / SCIENCE_PASS standing — all hits
  are HISTORICAL/SUPERSEDED/RETRACTION-tagged records (two "scope WITHIN"
  hits fell outside this script's short tagging-context window, but the full
  row reads — SUPERSEDED_OVERCLAIMS_STANDING and RS-4 — are explicitly
  supersession-statement rows; verified by this QC's manual row read).
  GENERAL_PE_MAPPER_CORRECTNESS: 4 occurrences in the package, all
  NOT_ESTABLISHED. SCIENCE_PASS: zero occurrences — schema/pin PASS is not
  SCIENCE_PASS anywhere.

### D7 — Dependent-location census + entrypoint (for the parent phase)

All 10 RS-3 census locations independently verified by this QC (regex +
full-line reads + SOURCE_RUN file reads):
(1) SOURCE_RUN matrix line 18 ACTIVE→retracted by RS-1; (2) SOURCE_RUN
ledger FD-C2/SL-9 ACTIVE→superseded by RS-2; (3) SOURCE_RUN FINAL_REPORT
L228 ("R != W, T != W, 0x10 vs 0xC") + L248 ("R_W_SEPARATENESS =
PRESERVED (CONFIRMED)") dependent → HISTORICAL/SUPERSEDED; (4) SOURCE_RUN
QC_RESULTS.json duty6 line dependent → HISTORICAL/SUPERSEDED; (5) SOURCE_RUN
PE_MASTER_REVIEW L28 generic "R/W separateness" citation (no literal
inequality token) → limited to the scoped structural fact; (6) SOURCE_RUN
HANDOFF — NO occurrence (confirmed); (7) SOURCE_RUN EVIDENCE_INDEX — NO
inequality restatement (confirmed); (8) SOURCE_RUN SOURCE_STATE — NO
direct occurrence (confirmed); (9) AUDIT_ENTRYPOINT.md line 31 (SOURCE_RUN
row) — ZERO inequality tokens (confirmed by this QC's own 4546-char line
read); (10) AUDIT_ENTRYPOINT.md line 32 (older provenance row) — carries
"R!=W 0x10 vs 0xC" and "R!=T" in its ORIGINAL historical text.

**Remaining pending for the parent phase:** AUDIT_ENTRYPOINT.md line 32 —
the existing bracketed HISTORICAL_REFERENCE annotation (span offsets
4707..5175 of the 5352-char line) withdraws the T==P PROVEN alias and the
WITHIN/12-12 scope standing uses but does NOT name "R!=T". The parent phase
must extend that withdrawal annotation to ALSO cover the "R!=T" standing use
per RS-2. (The "R!=W 0x10 vs 0xC" token in the same line is the SCOPED
STRUCTURAL FACT and is permitted.) Precision note: RS-2/RS-3 phrase this as
"R!=T … inside the bracketed HISTORICAL_REFERENCE annotation"; physically
both R!=T tokens sit in the ORIGINAL row text BEFORE the appended
annotation (measured: tokens at offsets 2234 and 2438, annotation starting at
4707). The intended meaning is unchanged — the R!=T standing use is not
withdrawn by the current annotation and remains pending.

Additional historical occurrences OUTSIDE the RS-3 census scope (for
completeness, no action needed): the older PROVENANCE_R1 package (READ_ONLY
history) contains further "R!=T/R!=W" tokens (its QC_REPORT L113, FINAL_REPORT
L154, CLAIM_MATRIX CL-13/CL-14, HANDOFF L56/L78, PE_MASTER_REVIEW L21,
00_CONTROL_INTERNAL_QC/QC_RESULTS.json L840); those files' standing alias
claims were already superseded at the claim level by the SOURCE_RUN FD-C2
supersessions; the contract §4 sweep list covers the 8 SOURCE_RUN files +
the entrypoint, so these are recorded here only as census completeness.

### D8 — MAPPER_BOUNDARY_RESULTS.json spot verification — CONFIRMED

Pairwise comparison of this QC's own production-v2 re-observations against
every mapped case: 16 synthetic cases + 3 EXE cases + 8 input-type cases —
**zero disagreements** (classification vocabulary map QC_RAW_BACKED↔RAW_BACKED
etc. documented; a namespace difference, not a measurement difference). The
historical-QCPE PRE observations also agree with the executor's 00_PRE for
all mapped cases.

### D9 — REGRESSION_RESULTS.json spot verification — CONFIRMED

Executor: historical 80/80, RECW-old 6/6, identity 1/1, total 87/87, gate
PASS, denominators 80/6/1=87, regression verdict PASS. This QC's own
re-execution: clean 87/87 (default pinned loader AND normal scratch loader
path), own 80/80 by its own reads, each mutant 86/87 failing exactly on
RECW:W_RECORD_IDENTITY — agrees on every measured value.

### D10 — PRE immutability + superseded POST stamps — PASS

All 10 PRE files match their SHA256 index exactly; the only file outside the
index is the index itself (self-exclusion by design). None of the 00_PRE/
files was overwritten. The 4 superseded POST stamps
(035645Z partial-crash, 035712Z, 035717Z assembly-crash, 035740Z
completed-but-superseded) are preserved as authentic negative evidence
(035740Z's own 33-file index verified with zero mismatches); the final
corrected POST stamp is 20261009T035844Z.

## 3. QC self-tooling fixes (disclosed; repair round 1 of 1 used)

1. The first write of `qc_countercheck_v2.py` had a 63-character
   transcription of the historical checker SHA pin (one "2" dropped). The
   fail-closed verify_pin caught it BEFORE any execution — no raw output
   was written. Corrected in place with a comment at the constant. (The
   same defect class the historical SOURCE_RUN QC disclosed for its own
   constant.)
2. An identity-oracle census line used `v2.count` instead of `v2_src.count`
   (NameError after the duties, before the raw dump; that attempt wrote no
   raw output — only the deterministic scratch fixtures). Fixed in place.

Both are fixes to THIS QC's OWN tooling, made before the first
completed evidence-producing run (attempt 3); no executor artifact was
modified. Authentic attempts log kept:
`00_CONTROL_INTERNAL_QC/QC_ATTEMPTS_LOG.md`.

## 4. Final identity re-verification (after ALL QC controls)

- EXE: 8015872 B / E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765
  D5280F31 — unchanged (this QC's own re-hash; the QC's read classes stayed
  within the contract policy: headers, pinned byte/rel32/COL/TypeDescriptor/
  name/string ranges, the 5 W-ctor bytes; in-memory TEST-OVERRIDE copies only
  for mutants).
- SOURCE_RUN pins re-hashed unchanged (checker 30167/F50DDC40…, qc_countercheck
  40309/11957F40…, ACTIVE_CORRECTED_PINS.json 4835/64C64DA9…).
- AUDIT_ENTRYPOINT.md unchanged (263460 / 87FF3314…) — this QC performed NO
  entrypoint write, NO stage, NO commit, NO push.
- checker_plus4_successor_v2.py SHA identical before and after this QC
  (80EBEE27…).
- No __pycache__/.pyc residue (python -B everywhere; directory scan).

## 5. Coverage / NOT_CHECKED

Full read: the frozen contract (172 lines), the Desktop corpus (649 lines),
checker_plus4_successor_v2.py (776 lines), run_residual_controls.py (1794
lines), SOURCE_RUN qc_countercheck.py (892 lines) and
checker_plus4_successor.py (620 lines), PACKAGE INPUT_IDENTITIES /
AUTHORIZATION_RECORD / SOURCE_STATE_AND_FINDINGS, both CSV ledgers (all rows),
SOURCE_RUN PE_MASTER_REVIEW.md, REGRESSION_RESULTS.json (917 lines), and a
full programmatic parse of all 39 MAPPER_BOUNDARY cases with every case
object individually compared to this QC's own measurements.

NOT_CHECKED (explicit): no new RE/disassembly of any kind (zero new bodies,
zero new xrefs); FUN_007B79B0 / FUN_007B7930 / FUN_006B2310 bodies NOT
opened (the &R+8 write-effects GAP stays a GAP); the EXE never executed
(STATIC_ONLY); executor PRE/POST raws were hash-verified and their
load-bearing rows re-executed, but not every JSON field of every raw was
individually re-executed by this QC; the external Desktop post-audit of the
resulting SHA remains NOT_PERFORMED.

## 6. Open findings

- **F-QC-1 (pending parent action, not a defect of this package):**
  AUDIT_ENTRYPOINT.md line 32 still carries the "R!=T" standing use in its
  original historical text; the existing HISTORICAL_REFERENCE annotation
  withdraws T==P/WITHIN but not R!=T — the parent phase must extend the
  annotation per RS-2 (the executor correctly recorded this as pending and
  did not edit the entrypoint).

No other new material findings. The two executor-disclosed runner
case-design defects (section_table_file_offset 0x1A0→0x178 descriptive-only
PRE note; P2A-PARTIAL-END expected-label corrected by the POST-run
P2A-PARTIAL-END-2 case) are already disclosed in the package
(SOURCE_STATE_AND_FINDINGS.md §6 / RS-8) and this QC verified the corrected
POST state and the preserved immutable PRE raws.

## 7. Standing statuses confirmed unchanged

ORIGINAL_SCOPE_COMPLIANCE = FAIL; ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL;
RETROACTIVE_PRIOR_AUTHORIZATION = NO; exact counts UNRESOLVED;
T_EQUALS_FIRST_INITIAL_P = NOT_ESTABLISHED_WITHIN_BOUND;
T_NOT_EQUAL_W_AT_LATER_USE = NOT_ESTABLISHED_WITHIN_BOUND;
R_NOT_EQUAL_T_AT_LATER_USE = NOT_ESTABLISHED_WITHIN_BOUND;
P_HEAP_ORIGIN = NOT_ESTABLISHED; GENERAL_PE_MAPPER_CORRECTNESS =
NOT_ESTABLISHED; MODEL_ROOT_RELATION = UNKNOWN; WORLD_XYZ_RECOVERED = NO;
HISTORICAL_FIRST_QC_PRE = LOST_OR_NOT_AVAILABLE;
NEW_DESKTOP_POST_AUDIT = NOT_PERFORMED; NEXT_EXPERIMENT_AUTHORIZED = NO;
HARD_STOP = YES.

## 8. Verdict

**QC_VERDICT = PASS** — every mandated duty holds on this QC's independent
measurements (own QCPEv2 implementation, own AST extraction of the
historical QCPE, own EXE reads and arithmetic, production-gate
re-executions through the normal loader paths, records content
re-adjudication, RS-3 census re-verification, PRE immutability). Scope: an
internal QC verdict about THIS correction run's machinery and records —
NOT MASTER_ACCEPTED, NOT a milestone closure, NOT canonical qualification.
The parent phases (PE-MASTER review, final reports, entrypoint row +
RS-2 annotation extension, manifest LAST, one ordinary commit/push) remain
ahead per contract §7.
