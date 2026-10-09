# FINAL_REPORT — PE_935_CAND4_006C9700_PLUS4_RESIDUAL_POST_AUDIT_CORRECTION_R1_20261008

RUN_CLASS = RECORDS_AND_QC_MACHINERY_CORRECTION (correction-only; RUN_SCOPE =
EXACTLY THREE DESKTOP P2 + ONE REC-W P3). This is the terminal report of the
run; it does not authorize any further work (NEXT_EXPERIMENT_AUTHORIZED = NO;
HARD_STOP = YES).

## 1. Run and contract identity

```text
RUN_ID          = PE_935_CAND4_006C9700_PLUS4_RESIDUAL_POST_AUDIT_CORRECTION_R1_20261008
CONTRACT        = C:\Users\User\Downloads\OPENCODE_PLUS4_RESIDUAL_CORRECTION_R1_20261008.md
                  23137 B / SHA256 2634BA31C4002B636E6AF659D2EB51313C18CB2ED3B7FEB000AA2303042C6969
                  172 lines, read IN FULL by executor, QC and PE-MASTER; identity MATCH
BASE_SHA        = 0b94c487ba11869b811aada188bfabaf8972728a
SOURCE_RUN      = docs/audits/PE_935_CAND4_006C9700_PLUS4_POST_AUDIT_CORRECTION_R1_20261008/
                  (22 physical files, 22/22 byte-identical at BASE; manifest Git blob
                  60e8318e90a76e6d0a85365d9080a89f33bdd1bf verified)
DESKTOP CORPUS  = C:\Users\User\Documents\ChatGPT\PE\PE_PLUS4_CORRECTION_DESKTOP_POST_AUDIT_0B94C48_20261008\
                  \ADVERSARIAL_COUNTERCHECKS.json — 16079 B / SHA256
                  62646637C323E0BAEAD371A0AE979D1F92DD2752B60C9D402E70A5A8FA38837B
                  (read IN FULL, 9 cases; NO REPORT.md exists in that directory —
                  none was required, invented or synthesized)
TARGET EXE      = D:\Eudoria_Reconstruction\pcg_install\Entropia.exe — 8015872 B / SHA256
                  E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
                  (rehashed before all reads and after all controls by executor AND QC;
                  unchanged; reads limited to pins/rel32/RTTI/strings/COL/TD/name ranges
                  + the 5 W-ctor bytes; NO new RE, NO new bodies, NO runtime)
PACKAGE         = docs/audits/PE_935_CAND4_006C9700_PLUS4_RESIDUAL_POST_AUDIT_CORRECTION_R1_20261008/
                  (75 files before this persistence phase: executor 66 + QC 9)
```

## 2. Preflight (fail-closed; all PASS)

LOCAL_HEAD == origin/master (after fetch) == live `git ls-remote` actual remote
master == EXPECTED_BASE_SHA 0b94c487ba11869b811aada188bfabaf8972728a exactly (no
fuzzy comparison). No tracked dirty changes at start. OUTPUT_ROOT absent at
preflight, created only after PASS. Six foreign untracked paths recorded and
left untouched (INPUT_IDENTITIES.md §1). All ten load-bearing SOURCE_RUN pins
verified SIZE+SHA256 MATCH; source manifest blob SHA1 60e8318e… MATCH; the
historical PROVENANCE checker pin (12749 B / F58D2DB3…) MATCH. Nothing was
reset/amended/rebased/force-pushed at any point of this run.

## 3. Finding dispositions (measured evidence)

### 3.1 P2-A — partial section overlap and PE32 address boundaries — CORRECTED

- PRE (immutable 00_PRE/, stamp 20261009T035439Z): the Desktop's four mapper
  false-passes were physically reproduced on BOTH historical implementations
  (the EXACT SOURCE production checker imported via importlib and the
  AST-extracted historical QCPE) with byte parity with the Desktop corpus —
  VA=0x0040104F,n=4 and VA=0x0040106F,n=4 returned RAW_BACKED `41 41 41 41`
  on the overlapping A/B geometry, and VA=0xFFFFFFFE,n=4 /
  VA=0x100000000,n=4 returned bytes as well (containment-only matching; no
  32-bit bounds).
- POST (production v2 `03_SCRIPTS/checker_plus4_successor_v2.py`; independent
  QC v2 `03_SCRIPTS/qc_countercheck_v2.py`): half-open [VA, VA+n) intervals
  with whole pre-validation (integers-not-bool; 0 <= VA < 2**32; n > 0;
  VA+n <= 2**32; separate VA < ImageBase underflow rejection; no negative
  indexing/wrapping); per-section membership interval [VirtualAddress,
  VirtualAddress+max(VirtualSize,SizeOfRawData)) with an ANY-INTERSECTION rule
  — more than one intersecting section => REJECTED_INVALID_INPUT/QC_REJECT
  even if one fully contains the read; a single intersecting section must
  cover the WHOLE request; RAW_BACKED requires the whole range inside ONE
  section's SizeOfRawData AND physically inside the file; pure virtual tail
  => VIRTUAL_BSS; raw→BSS crossing => controlled FAIL; no fabricated zeros.
- Measured POST evidence (MAPPER_BOUNDARY_RESULTS.json — all 39 cases
  verdict PASS; executor 39/39; QC's own 18/18 Desktop-case suite + extras):
  Desktop overlap geometry A(RVA 0x1000,v/r 0x100,roff 0x400) +
  B(RVA 0x1050,v/r 0x20,roff 0x600), ImageBase 0x00400000 —
  VA=0x0040104F,n=4 and VA=0x0040106F,n=4 => controlled reject; valid
  boundaries VA=0xFFFFFFFF,n=1 => byte `41` read correctly and
  VA=0xFFFFFFFE,n=2 => `41 41` read correctly (NOT over-rejected; the
  exclusive endpoint may equal 2**32); VA=0xFFFFFFFE,n=4 and
  VA=0x100000000,n=4 => INVALID, no bytes; one-byte-intersection case
  rejects (regression detection); historical full-section-overlap rejection
  preserved; real-EXE pin 0x006E8FA5,n=3 => `89 46 04`; BSS VAs
  0x00BA1100/0x00BA73BC => VIRTUAL_BSS with zero bytes fetched;
  base+0x7FFFFFFF retained RELABELED UNMAPPED (NOT a PE32 overflow test).
  GENERAL_PE_MAPPER_CORRECTNESS = NOT_ESTABLISHED (restricted corpus).

### 3.2 P2-B — truncated/malformed PE optional header — CORRECTED

- PRE: on the Desktop's synthetic fixture layout (e_lfanew=0x80, COFF @0x84,
  Magic @0x98, ImageBase @0xB4), truncations 0x98/0x99/0xB4/0xB7 let RAW
  `struct.error` escape from both historical implementations — messages
  byte-identical with the Desktop ("unpack_from requires a buffer of at
  least 154 bytes for unpacking 2 bytes at offset 152/153"; "…184 bytes for
  unpacking 4 bytes at offset 180/183").
- POST: staged constructor boundary checks BEFORE every unpack_from/slice
  (e_lfanew, COFF machine/nsec, SizeOfOptionalHeader, PE32 Magic, ImageBase,
  section table); every truncation a controlled
  ControlledReadError(REJECTED_INVALID_INPUT)/QCReadError(QC_REJECT) at the
  exact stage — 0x98/0x99 at the Magic stage, 0xB4/0xB7 at the ImageBase
  stage; no catch-all; struct.error/IndexError can never escape as a PASS.
- Probes measured: 0x9A (controlled at the ImageBase stage; PRE escaped a raw
  struct.error there), 0xB8 and 0x190 (section-table stage), 0x1C0
  (CONSTRUCTED — headers complete). Positive intact control: CONSTRUCTED with
  every measured fixture field matching (e_lfanew 0x80, PE signature, machine
  0x14C, nsec 1, SizeOfOptionalHeader 0xE0, Magic 0x10B, ImageBase 0x00400000,
  section table at file offset 0x178 = 0x84+20+0xE0).

### 3.3 P3 — REC-W coherent wrong-callsite false pass — CORRECTED

- PRE (immutable): the Desktop mutant (RECORD_ID `W_CTOR_CALL_AT_006CB836`
  kept; the record teleported to the pinned REL_PUMP_CTOR_R callsite
  0x006C97D8; BYTES E8 93 F7 01 00; SIGNED_REL32 +0x1F793; NEXT_VA 0x006C97DD;
  TARGET_VA 0x006E8F70) replayed through the ORIGINAL checker's NORMAL loader
  path (load_active_corrected_pins(scratch) → run_checks → gate; physical-file
  parse + schema validation; no prevalidated-dict bypass) FALSE-PASSED 86/86
  on the REAL pinned EXE — the Desktop expectation, reproduced exactly.
  W2 (RECORD_ID-only): 86/86 false pass and the fixed-address QC comparison
  did NOT catch it (honest negative — nothing compared the ID). W3
  (generality teleport to 0x006CB7CF, E8 2C DF FF FF, -0x20D4 → 0x006C9700):
  86/86 false pass.
- POST: NEW production gate `RECW:W_RECORD_IDENTITY` binds
  W_CTOR_CALL_AT_006CB836 ↔ 0x006CB836 from the NON-MUTATABLE module-internal
  constant CANONICAL_RECORD_IDENTITY (structurally: exactly 1 module-level
  definition, 0 later assignments, 0 JSON-driven writes; behaviorally: W1
  proves the JSON cannot rebind the canonical id, W2 proves an unknown id
  fails closed, W3 proves the binding is callsite-exact). W1/W2/W3 each FAIL
  EXACTLY on the identity gate (86/87; the 80 historical IDs and the six
  original RECW checks PASS; no SHA-mismatch/missing-file/unrelated-pin
  failure rescues the verdict — replays ran on the REAL pinned EXE). Clean
  record: 87/87 (byte pin E8 75 F0 02 00, rel32 +0x2F075, target 0x006FA8B0,
  six RECW + identity). Denominator honestly 87 = 80 + 6 + 1
  (TARGET_FORMULA stays a schema-required field, NOT a separate gate, never a
  substitute for the identity gate). Clean scratch copy through the same
  loader path: 87/87.
- PE-MASTER's own counter-check reproduced all of this through the normal
  loader path (W1 → exactly 1 FAIL on the identity gate; W2 → exactly 1 FAIL
  on the identity gate; clean scratch → 87/87 PASS).

### 3.4 P2-C — pointer-identity / dependent claim retraction — CORRECTED (records)

- Retraction (a): the SOURCE_RUN matrix's R_W_SEPARATENESS claimed
  "R != W and T != W" as CONFIRMED — the unsupported later-T part RETRACTED;
  the R/W construction evidence preserved as a SCOPED STRUCTURAL FACT
  (distinct construction events and sizes, 6A 10 vs 6A 0C; NOT universal
  object/class inequality; NOT a lifetime-wide identity theorem).
- Retraction (b): the SOURCE_RUN ledger FD-C2/SL-9 corrected-active text
  "R != T stays" SUPERSEDED (RS-2).
- NEW ACTIVE records (CORRECTED_CLAIM_MATRIX.csv, 22 physical rows incl.
  header; SUPERSESSION_LEDGER.csv RS-1..RS-8, 9 physical rows incl. header):
  explicit unknown-status rows T_NOT_EQUAL_W_AT_LATER_USE =
  NOT_ESTABLISHED_WITHIN_BOUND and R_NOT_EQUAL_T_AT_LATER_USE =
  NOT_ESTABLISHED_WITHIN_BOUND — NEITHER equality NOR inequality established;
  R, P, T, W, field addresses, owners and classes never conflated.
- All old T==P, heap-origin and WITHIN overclaims remain SUPERSEDED with zero
  active standing (RS-4; QC's own package-wide sweep: 0 untagged active
  overclaims; SCIENCE_PASS token count 0; GENERAL_PE_MAPPER_CORRECTNESS —
  all 4 occurrences say NOT_ESTABLISHED).
- RS-3 dependency census: 10 dependent locations traced semantically (not
  keyword-only grep); the ONLY remaining pending location was
  AUDIT_ENTRYPOINT.md line 32 — closed by THIS persistence phase (see §7).
- Scope records preserved: floor 17 callsite units / 5 bodies / edge budget
  12 => ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL and
  ORIGINAL_SCOPE_COMPLIANCE = FAIL; exact counts UNRESOLVED;
  RETROACTIVE_PRIOR_AUTHORIZATION = NO.
- HISTORICAL_FIRST_QC_PRE = LOST_OR_NOT_AVAILABLE disclosed (RS-8): the
  SOURCE_RUN QC's first failed raw output was overwritten historically and
  the original bytes are NOT available anywhere; NOT claimed recovered —
  distinct from THIS run's fresh PRE (run-stamped, hashed, immutable).

## 4. PRE/POST evidence summary

```text
00_PRE/  (11 files, IMMUTABLE, run stamp 20261009T035439Z)
  PRE_..._RUN_HEADER.json, PRE_..._SHA256_INDEX.json,
  PRE_..._BASELINE_CLEAN.json, PRE_..._CONTROLS_RAW.json,
  PRE_..._HEADER_P2B_RAW.json, PRE_..._MAPPER_P2A_RAW.json,
  PRE_..._WRONG_CALLSITE_P3_RAW.json + scratch/ (CLEAN copy, W1, W2, W3).
  Every file matches its SHA256 index (QC re-verified: 10/10 files, 0
  mismatches; the index excludes itself by design). The PRE executions ran
  the EXACT SOURCE scripts (production via importlib import only after a
  full inertness read; historical QCPE via AST-EXTRACTION of executed
  definitions only — main() and every other top-level statement never
  executed). Never overwritten by POST.

00_POST/ (46 files: final stamp 20261009T035844Z + FOUR superseded stamps
  KEPT as authentic negative evidence)
  20261009T035645Z — runner KeyError at the P2-B probe fixture (two partial
                     files kept); superseded.
  20261009T035712Z — tuple-index runner bug in the boundary assembly (full
                     raws, no final assembly); superseded.
  20261009T035717Z — missing-geometry runner bug in the boundary assembly
                     (full raws, no final assembly); superseded.
  20261009T035740Z — completed but carried the two disclosed case-design
                     defects; superseded (its own 33-file index verified,
                     zero mismatches).
  20261009T035844Z — the FINAL corrected POST: 39/39 boundary case-PASS,
                     87/87 clean baseline, regression verdict PASS (+ its
                     RUN_HEADER and SHA256_INDEX).
  The wrong-callsite mutants replay on the REAL pinned EXE in every POST
  stamp; scratch fixtures isolated under 00_POST/scratch/ (CLEAN/W1/W2/W3).
```

Executor self-corrections disclosed (SOURCE_STATE_AND_FINDINGS.md §6,
RS-8): (1) header_field_expectations section_table_file_offset stated 0x1A0
in the PRE raw — correct value 0x178 (descriptive-only defect; corrected for
POST; no gate consumed it); (2) the P2A-PARTIAL-END PRE case carried a wrong
expected label (the true partial-end demonstration is the POST-run
P2A-PARTIAL-END-2 case, disclosed NOT_IN_PRE).

## 5. Regression table (measured)

```text
Historical 80-ID regression : 80/80 PASS (EXE_IDENTITY + 57 PIN + 16 REL32
                               + 3 RTTI + 3 STR; no duplicates; complete
                               required ID set AST-parsed READ_ONLY from the
                               pinned historical PROVENANCE checker)
Table identity v2 vs hist.  : 4/4 element-identical (BYTE/REL32/RTTI/STRING)
Table identity v2 vs SOURCE : 4/4 element-identical
RECW original six checks    : 6/6 PASS (RECORD_SCHEMA, W_RECORD_BYTES,
                               W_RECORD_REL32, W_RECORD_NEXT_VA,
                               W_RECORD_TARGET, W_RECORD_INTERNAL_CONSISTENCY)
NEW identity check          : 1/1 PASS (RECW:W_RECORD_IDENTITY)
Clean v2 suite total        : 87/87, gate PASS (80 + 6 + 1; separate
                               denominators honest)
MC1–MC5                     : each FAILs exactly its proper anchor
                               (PIN:CTOR_R4_STORE_P; PIN:CTOR_RETURN_THIS;
                               PIN:PUMP_RETURN_R; REL32:REL_PUMP_CTOR_R;
                               RTTI:RTTI_W_ARKMODELRESOURCEINSTANCEREF)
MC6 (offset-0x7A1100 direct physical file mutation, a .rsrc raw byte — NOT
     a VA read of 0x00BA1100): all 87 anchor gates PASS (specificity held)
W-record JSON mutation gates: bytes-only/displacement-only/target-only each
                               flip exactly its own gate; identity gate
                               stays PASS (no false triggering)
Prior RAW/BSS controls       : preserved (raw-backed pin, both BSS VAs,
                               raw→BSS crossing, declared-raw-past-EOF,
                               COL 20 B / TD-name crossing rejected through
                               the same API, ambiguous overlapping sections)
REGRESSION verdict           : PASS
```

## 6. QC (fresh-context internal QC)

QC_ORIGIN = pe-master-auditor fresh-context internal QC, internal to
PE-MASTER — NOT an independent Desktop post-audit, NOT executor self-review
(contract §7(b) parent phase). QC_VERDICT = **PASS** — 9/9 duties on the QC's
own measurements: own independent QCPEv2 implementation
(`03_SCRIPTS/qc_countercheck_v2.py`, 89938 B / SHA256 F57988BC…B4402, 1778
lines — NOT a re-export of the production classifier) 18/18 Desktop P2-A
cases + Desktop PRE parity byte-identical + own POST cases; own P2-B
truncation re-measurements (9/9); own scratch fixtures + production-gate
mutant re-executions through the normal loader paths (W1/W2/W3 each exactly
1 FAIL = RECW:W_RECORD_IDENTITY; clean scratch 87/87 via both loader paths);
own W byte pin read (E8 75 F0 02 00 / +0x2F075 / 0x006FA8B0; direct
file-slice crosscheck at offset 0x2CB836); own 80-ID re-execution 80/80 with
element-identical tables; P2-C records content re-adjudication incl. the
RS-3 10-location census and the entrypoint dependent-locations
re-verification; MAPPER/REGRESSION spot verification (0 disagreements);
PRE immutability (0 mismatches) + superseded POST stamps preserved.
QC repair round 1/1 used ONLY on the QC's own tooling (2 disclosed fixes:
a dropped character in a SHA pin constant caught by fail-closed verify_pin
before any execution; a NameError census line fixed before the raw dump);
attempts preserved as authentic negative evidence
(00_CONTROL_INTERNAL_QC/QC_ATTEMPTS_LOG.md); ZERO executor artifacts
modified. Every essential PASS records MEASURED_QUANTITY,
INDEPENDENT_SOURCE_OF_TRUTH, WHY_NON_CIRCULAR and FAILURE_CASE_DETECTED in
the raw output.

## 7. PE-MASTER MASTER_AUDIT and the entrypoint amendment (F-QC-1)

PE-MASTER MASTER_AUDIT = **MASTER_ACCEPTED_ADVISORY** (internal advisory;
CORRECTION_VERDICT = PASS per contract §8; ADVISORY_PRE_QUALIFICATION;
CANONICAL_GATE_EFFECT = NONE). PE-MASTER independently: verified the
75-file census; full-read-verified the identity-gate source region; executed
the production v2 gate itself (clean 87/87, all rows enumerated); executed
its own W1/W2 mutant scratch fixtures through the normal loader path
(exactly 1 FAIL on RECW:W_RECORD_IDENTITY each; clean scratch 87/87);
verified SOURCE_RUN immutability and the desktop corpus identity. Full
detail: PE_MASTER_REVIEW.md in this package.

**F-QC-1 EXECUTED in THIS persistence phase:** the AUDIT_ENTRYPOINT.md
line-32 historical PROVENANCE row's HISTORICAL_REFERENCE annotation has been
EXTENDED so that the active "R!=T" standing use of that row's original
historical text is ALSO WITHDRAWN per RS-2 of this package
(R_NOT_EQUAL_T_AT_LATER_USE = NOT_ESTABLISHED_WITHIN_BOUND; neither equality
NOR inequality established), in addition to the already-withdrawn T==P and
WITHIN standing uses. The row's historical content was NOT rewritten; the
extension is a short bracketed addition inside the existing annotation. This
was the only remaining dependent location from the RS-3 census of 10; the
census is now fully closed. A new newest-first LATEST RUNS row for this run
was also added (AUDIT_ENTRYPOINT.md; no other row touched — the immediately
preceding correction row was independently re-swept by this phase and
contains no other un-annotated active R!=T/T!=W standing).

## 8. Open findings (unchanged unless stated)

- F-1..F-5 (source backlog, unchanged, kept OPEN by the SOURCE_RUN and not
  material to the corrections; P3 notation/extent-metadata description-only
  residues + the F-2 P2 historical mapper dispositioned via the successor
  machinery of this run).
- Executor-disclosed process items: the two runner case-design defects
  (§4) and the four superseded POST stamps kept as authentic negative
  evidence. QC-disclosed process items: the two self-tooling fixes (§6).
- HISTORICAL_FIRST_QC_PRE = LOST_OR_NOT_AVAILABLE (§3.4; honest
  unavailability of a historical artifact, distinct from this run's fresh
  PRE).
- NO new material findings beyond the corrected five
  (PE_MASTER_REVIEW.md "Findings" section).

## 9. Terminal governance

```text
ORIGINAL_SCOPE_COMPLIANCE      = FAIL (preserved; floor 17 / bodies 5 /
                                 edge budget 12; exact counts UNRESOLVED —
                                 no exact counts are established by this run)
ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL (preserved)
RETROACTIVE_PRIOR_AUTHORIZATION = NO
NEW_PCG_FUNCTION_BODIES        = 0
NEW_PCG_SCIENCE_EDGE_INTERPRETATIONS = 0
GENERAL_PE_MAPPER_CORRECTNESS  = NOT_ESTABLISHED (restricted PE32 corpus)
MODEL_ROOT_RELATION            = UNKNOWN
WORLD_INSTANCE                 = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED            = NO
LOOKUP_SEMANTIC                = UNRESOLVED
the &R+8→FUN_006B2310 write-effects GAP preserved (body never opened)
SCIENCE_NEW                    = 0
CANONICAL_GATE_EFFECT          = NONE
NEW_DESKTOP_POST_AUDIT         = NOT_PERFORMED (external post-audit of the
                                 resulting SHA is a later human-authorized
                                 action; NOT self-declared here)
NEXT_EXPERIMENT_AUTHORIZED     = NO
HARD_STOP                      = YES
```

THIS CORRECTION AUTHORIZES NOTHING FURTHER. The one-run boundary stands; any
next action requires a fresh explicit human authorization.
