# SOURCE_STATE_AND_FINDINGS — PE_935_CAND4_006C9700_PLUS4_RESIDUAL_POST_AUDIT_CORRECTION_R1_20261008

RUN_CLASS: RECORDS_AND_QC_MACHINERY_CORRECTION (correction-only;
RUN_SCOPE = EXACTLY THREE DESKTOP P2 + ONE REC-W P3).
NEW_SCIENCE_EXECUTED = NO; NEW_PCG_FUNCTION_BODIES = 0;
NEW_PCG_SCIENCE_EDGE_INTERPRETATIONS = 0; QC_REPAIR_ROUNDS_MAX = 1 (the one
runner repair round is disclosed in §6). Executor: pe-reconstruction (bounded
worker phase under direct PE-MASTER dispatch; NO_NESTED_TASKS). Era label for
every physical fact cited in this package: PCG 9.3.5 client image
(Entropia.exe, 8015872 B / SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE6138
96 89A22F753765D5280F31).

## 1. Preflight verdict

PASS. LOCAL_HEAD == origin/master (after fetch) == live ls-remote ==
EXPECTED_BASE_SHA 0b94c487ba11869b811aada188bfabaf8972728a exactly (no fuzzy
comparison). No tracked dirty changes. OUTPUT_ROOT absent at preflight,
created only after PASS. The six foreign untracked paths recorded and left
untouched (INPUT_IDENTITIES.md §1). Contract identity verified (23137 B /
SHA256 2634BA31C4002B636E6AF659D2EB51313C18CB2ED3B7FEB000AA2303042C6969 /
172 lines) and read IN FULL first. Desktop ADVERSARIAL_COUNTERCHECKS.json
verified (16079 B / 62646637C323E0BAEAD371A0AE979D1F92DD2752B60C9D402E70A5A
8FA38837B) and read IN FULL (9 cases; NO REPORT.md exists in that directory —
none was required or invented). EXE verified (8015872 B / E7785430E81DFFE648
CE8F5312414B17BC9FCE61389689A22F753765D5280F31). The SOURCE_RUN 22-file
census verified by physical Git tree comparison AND working-tree hashing
(INPUT_IDENTITIES.md §4); all ten load-bearing pins MATCH; the source
manifest Git blob SHA1 60e8318e90a76e6d0a85365d9080a89f33bdd1bf MATCHES.

## 2. Source state (READ_ONLY)

SOURCE_RUN = PE_935_CAND4_006C9700_PLUS4_POST_AUDIT_CORRECTION_R1_20261008 at
BASE 0b94c487 — 22 physical files, every one byte-identical to its BASE Git
blob; nothing in it was modified, staged or re-run by this residual run
(re-verified after all controls). Its standing records remain: the single
active W record in ACTIVE_CORRECTED_PINS.json (CALLSITE_VA 0x006CB836;
BYTES E8 75 F0 02 00; SIGNED_REL32 +0x2F075; NEXT_VA 0x006CB83B; TARGET_VA
0x006FA8B0); T_EQUALS_FIRST_INITIAL_P = NOT_ESTABLISHED_WITHIN_BOUND;
R_PLUS4_VALUE_PRESERVED_TO_LATER_USE = NOT_ESTABLISHED;
ACTUAL_LATER_OVERWRITE_OBSERVED = NO; P_HEAP_ORIGIN = NOT_ESTABLISHED;
P_ALLOCATION_OR_STORAGE_ORIGIN = NOT_ESTABLISHED_WITHIN_BOUND;
ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL; ORIGINAL_SCOPE_COMPLIANCE = FAIL;
floor 17 / bodies 5 / exact counts UNRESOLVED. The two RECENTRAL retraction
targets found in it (accepted, corrected in §4): its CORRECTED_CLAIM_MATRIX
R_W_SEPARATENESS row claims "R != W AND T != W" as CONFIRMED, and its
SUPERSESSION_LEDGER FD-C2/SL-9 corrected-active text retains "R != T stays".

## 3. The residual findings — accepted, with this run's disposition

### 3.1 P2-A — partial section overlap and PE32 address boundaries — ACCEPTED, CORRECTED (production v2)

The Desktop demonstrated (ADVERSARIAL_COUNTERCHECKS cases 1–4, physically
reproduced here on the EXACT SOURCE scripts with byte parity — 00_PRE/
PRE_20261009T035439Z_MAPPER_P2A_RAW.json): the source successor's
containment-only section matching false-PASSes a read that intersects TWO
sections (VA=0x0040104F,n=4 and VA=0x0040106F,n=4 on geometry A(RVA 0x1000,
vsize/rsize 0x100, roff 0x400) + B(RVA 0x1050, vsize/rsize 0x20, roff 0x600),
ImageBase 0x00400000 — both returned RAW_BACKED bytes 41 41 41 41 on
production AND historical QC), and the missing 32-bit bounds false-PASS
VA=0xFFFFFFFE,n=4 and VA=0x100000000,n=4 (bytes 41 41 41 41). Partially
covered single-section requests were misclassified UNMAPPED (no bytes, wrong
reason).

Disposition: 03_SCRIPTS/checker_plus4_successor_v2.py (the source file NOT
repaired in place): half-open [VA, VA+n) validation BEFORE section matching
(integers-not-bool; 0 <= VA < 2**32; n > 0; VA+n <= 2**32; separate
VA < ImageBase underflow; no negative indexing/wrapping); ANY-INTERSECTION
matching over [VirtualAddress, VirtualAddress+max(VirtualSize,
SizeOfRawData)) — more than one intersecting section => REJECTED_INVALID_
INPUT even if one fully contains the read; a single intersecting section
must cover the WHOLE request; cross-section / partially unmapped intervals
never yield bytes; RAW_BACKED requires the whole range inside ONE section's
SizeOfRawData AND physically inside the file; pure virtual tail =>
VIRTUAL_BSS; crossing raw->BSS => controlled FAIL; no fabricated zeros; the
raw-padding policy preserved verbatim. Mandatory Desktop cases all measured
POST (00_POST/POST_20261009T035844Z_MAPPER_P2A_RAW.json +
MAPPER_BOUNDARY_RESULTS.json, 39/39 case-PASS): overlap START/END rejects;
VA=0xFFFFFFFE,n=4 and VA=0x100000000,n=4 controlled INVALID (no bytes);
POSITIVE boundaries VA=0xFFFFFFFF,n=1 -> byte 41 and VA=0xFFFFFFFE,n=2 ->
41 41 on the raw-backed 4GiB fixture (NOT rejected merely because the
exclusive endpoint equals 2**32); non-overlap + endpoint-touching positives
(the [0x10F8,0x1100) read inside .s1 touching .s2's start is RAW_BACKED);
the crossing [0x10FE,0x1102) rejected; ordinary pin VA=0x006E8FA5,n=3 ->
89 46 04 on the pinned EXE; BSS VAs 0x00BA1100/0x00BA73BC -> VIRTUAL_BSS,
zero bytes fetched; full-section-overlap historical rejection preserved; a
ONE-BYTE intersection (0x106F) rejects (regression detection); the
base+0x7FFFFFFF control retained RELABELED (UNMAPPED far beyond the image —
NOT a PE32 overflow test; real boundary tests are the 4GiB cases).
GENERAL_PE_MAPPER_CORRECTNESS = NOT_ESTABLISHED.

### 3.2 P2-B — truncated/malformed PE optional header — ACCEPTED, CORRECTED (production v2)

The Desktop demonstrated (cases 5–8, reproduced verbatim): on the synthetic
fixture layout (e_lfanew=0x80, COFF @0x84, Magic @0x98, ImageBase @0xB4,
SizeOfOptionalHeader 0xE0), file sizes 0x98/0x99/0xB4/0xB7 let RAW
struct.error escape from BOTH the source production constructor and the
historical QCPE ("unpack_from requires a buffer of at least 154 bytes for
unpacking 2 bytes at offset 152/153"; "184 bytes for unpacking 4 bytes at
offset 180/183").

Disposition: staged constructor checks in v2 — BEFORE EVERY
struct.unpack_from / slice interpretation the physical buffer availability
and the declared limits are verified (e_lfanew; COFF machine/nsec;
SizeOfOptionalHeader; PE32 Magic; ImageBase; section table), each failure
raising ControlledReadError(REJECTED_INVALID_INPUT) with a stage-specific
reason; no catch-all; struct.error/IndexError never escape as a PASS. POST
measured: 0x98/0x99/0xB4/0xB7 each a controlled rejection at the exact stage
(0x98/0x99 at the Magic stage; 0xB4/0xB7 at the ImageBase stage); boundary
probes 0x9A (fails at the ImageBase stage — v1 escaped raw struct.error
there), 0xB8 and 0x190 (fail at the section-table stage — 0xB8 was already
controlled in v1; 0x190 is a POST-only mid-table probe) and 0x1C0
(CONSTRUCTED — headers complete; only raw reads remain); positive intact
control CONSTRUCTED with every measured header field equal to the fixture
(all_match = True: e_lfanew 0x80, PE sig, machine 0x14C, nsec 1, size_opt
0xE0, Magic 0x10B, ImageBase 0x00400000, the .text section values; the
section table starts at 0x178 = 0x84+20+0xE0).

### 3.3 P3 — REC-W coherent wrong-callsite false pass — ACCEPTED, CORRECTED (new production gate)

PRE (unmodified, 00_PRE/PRE_20261009T035439Z_WRONG_CALLSITE_P3_RAW.json):
the Desktop mutant (RECORD_ID W_CTOR_CALL_AT_006CB836 kept; record
teleported to the independently pinned REL_PUMP_CTOR_R callsite
0x006C97D8; BYTES E8 93 F7 01 00; SIGNED_REL32 +0x1F793; NEXT_VA
0x006C97DD; TARGET_VA 0x006E8F70)
replayed through the ORIGINAL production checker's NORMAL loader path
(load_active_corrected_pins(<scratch fixture path>) — physical-file parse +
schema validation, then run_checks + the SAME overall production gate; no
alternate predicate, no prevalidated-dict bypass) FALSE-PASSED **86/86**
(gate PASS) on the REAL pinned EXE — the Desktop's expected PRE result,
reproduced exactly. The separate fixed-address QC comparison (the historical
QC duty-2 style: own QCPE read at the CANONICAL 0x006CB836) DETECTED the
mismatch. RECORD_ID-only mutant (W2): 86/86 false PASS and the fixed-address
QC did NOT catch it (honest negative — nothing compared the ID); generality
mutant (W3, teleport to the pinned REL_HIST_PUMP callsite 0x006CB7CF,
E8 2C DF FF FF, -0x20D4 -> 0x006C9700): 86/86 false PASS, QC detected.

POST (v2): the NEW production check RECW:W_RECORD_IDENTITY binds
W_CTOR_CALL_AT_006CB836 <-> 0x006CB836 from the NON-MUTATABLE module
constant CANONICAL_RECORD_IDENTITY (independent of the fixture JSON and of
the JSON loader). All three mutants FAIL EXACTLY on RECW:W_RECORD_IDENTITY
(86/87 each; the other 80 historical IDs and the existing SIX RECW checks
remain PASS; no SHA mismatch, no missing-file exception, no unrelated pin
failure, no changed EXE rescues the verdict — the mutant replays run on the
REAL pinned EXE). The clean record passes byte pin E8 75 F0 02 00, rel32
+0x2F075, target 0x006FA8B0, all six original RECW checks AND the identity
gate: **87/87** (denominator honestly 87 = 80 + 6 + 1; TARGET_FORMULA stays
a schema-required field, NOT a separate P3 gate, and is never a substitute
for the identity gate). The clean scratch copy through the same loader
path: 87/87.

### 3.4 P2-C — pointer-identity / dependent claim retraction — EXECUTED (records)

Retraction target (a): the SOURCE_RUN CORRECTED_CLAIM_MATRIX
R_W_SEPARATENESS row claimed "R != W and T != W" as CONFIRMED — the
unsupported later-T part is RETRACTED; the R/W construction evidence is
preserved as a SCOPED STRUCTURAL FACT (distinct construction events and
sizes; NOT universal object/class inequality, NOT a lifetime identity
theorem). Retraction target (b): the SOURCE_RUN SUPERSESSION_LEDGER
FD-C2/SL-9 corrected-active text retained "R != T stays" — SUPERSEDED.
The NEW ACTIVE matrix (CORRECTED_CLAIM_MATRIX.csv of THIS package) contains
explicit unknown-status rows for BOTH inequalities: T_NOT_EQUAL_W_AT_
LATER_USE = NOT_ESTABLISHED_WITHIN_BOUND and R_NOT_EQUAL_T_AT_LATER_USE =
NOT_ESTABLISHED_WITHIN_BOUND (NEITHER equality NOR inequality established;
R, P, T, W, addresses of fields, owners and classes are never conflated).
The explicit dependency sweep (not keyword-only grep — every file read and
its standing use traced) covered: CORRECTED_CLAIM_MATRIX.csv, SUPERSESSION_
LEDGER.csv, SOURCE_STATE_AND_FINDINGS.md, FINAL_REPORT.md, EVIDENCE_INDEX.md,
HANDOFF.md, PE_MASTER_REVIEW.md and the AUDIT_ENTRYPOINT standing use —
census in SUPERSESSION_LEDGER.csv row RS-3 (10 dependent locations; the
AUDIT_ENTRYPOINT parent-phase annotation extension for the historical
"R!=T" wording is recorded in RS-2 — this executor phase does NOT edit
AUDIT_ENTRYPOINT.md). All old T==P, heap-origin and WITHIN overclaims remain
superseded (RS-4). Original scope floor 17 and body floor 5 preserved; edge
budget 12 => original scope FAIL; exact counts UNKNOWN; RETROACTIVE_PRIOR_
AUTHORIZATION = NO.

## 4. Regression and preserved controls (measured)

80-ID historical regression: the complete required ID set (EXE_IDENTITY +
57 PIN + 16 REL32 + 3 RTTI + 3 STR; no duplicates) AST-parsed READ-ONLY
from the historical PROVENANCE checker (12749 B / SHA256 F58D2DB3… verified)
and element-identical in v2 to BOTH the historical tables AND the SOURCE_RUN
successor tables (4/4 + 4/4); clean v2 baseline: historical 80/80 PASS, the
six original RECW checks 6/6, the new identity check 1/1 — suite total 87/87,
gate PASS; separate denominators 80/6/1. MC1–MC5 reproduced on v2, each
FAILing exactly its proper anchor (PIN:CTOR_R4_STORE_P; PIN:CTOR_RETURN_
THIS; PIN:PUMP_RETURN_R; REL32:REL_PUMP_CTOR_R; RTTI:RTTI_W_ARKMODELRESOURC
EINSTANCEREF); MC6 (direct physical file offset 0x7A1100 mutation, a .rsrc
raw byte — NOT a read of VA 0x00BA1100) leaves all 87 anchor gates PASS; the
three W-record JSON mutation gates (bytes-only / displacement-only /
target-only) each flip exactly its own gate on v2 while the identity gate
stays PASS (no false triggering); prior RAW/BSS controls preserved (raw-backed
pin, both BSS VAs, raw->BSS crossing with plausible further bytes,
declared-raw-past-EOF no-short-read, structured COL 20 B / TD-name crossing
rejected through the same API, ambiguous overlapping sections rejected).
REGRESSION_RESULTS.json verdict: PASS.

## 5. HISTORICAL_FIRST_QC_PRE = LOST_OR_NOT_AVAILABLE (disclosure)

The SOURCE_RUN QC_RESULTS.json ("qc_tool_self_corrections_disclosed")
admits: "the first execution's raw output was overwritten by the corrected
execution". The ORIGINAL BYTES of that first failed QC raw output are NOT
available anywhere; they are NOT claimed recovered. This is distinct from
THIS run's own fresh PRE evidence (00_PRE/, run-stamped, hashed, never
overwritten), which records the CURRENT session's executions of the exact
source scripts.

## 6. Executor self-corrections disclosed (in-scope, before acceptance)

1. run_residual_controls.py header_field_expectations stated the section
   table at file offset 0x1A0; the correct value is 0x178 (= 0x84+20+0xE0).
   The wrong value was copied into the IMMUTABLE PRE raw as a
   descriptive-only defect (no gate consumed it); corrected for POST with
   an in-file disclosure note.
2. The P2A-PARTIAL-END case carried a wrong expected label in the PRE raw:
   the request [0x11F8,0x1208) lies entirely past the section's membership
   end, so UNMAPPED is the correct classification (v1, v2 and the oracle
   all agree; no bytes were ever returned). The TRUE partially-covered
   demonstration is the POST-run case P2A-PARTIAL-END-2 (VA=0x004010F8,
   n=0x10 -> REJECTED_INVALID_INPUT), disclosed as NOT_IN_PRE.
3. FOUR superseded POST attempts are KEPT as authentic negative evidence:
   20261009T035645Z (runner KeyError at the P2-B probe fixture — a missing
   truncation size; two partial files); 20261009T035712Z (crashed in the
   boundary-assembly code — tuple-index bug; full raws, no final assembly);
   20261009T035717Z (crashed in the boundary-assembly code — missing
   geometry key; full raws, no final assembly); 20261009T035740Z (completed
   but carrying the two case-design defects of items 1–2). The final
   corrected POST stamp is 20261009T035844Z (39/39 boundary case-PASS,
   87/87 clean baseline, regression verdict PASS).

## 7. Phase boundary (what this executor phase did NOT do)

NOT performed by this phase (parent's later phases per contract §7/§8 and
the dispatch): qc_countercheck_v2.py (the fresh-QC worker's own
implementation — the fixed independent QC); 00_CONTROL_INTERNAL_QC/; QC_
RESULTS.json; QC_REPORT.md (QC phase); PE_MASTER_REVIEW.md; FINAL_REPORT.md;
EVIDENCE_INDEX.md; HANDOFF.md; MANIFEST_SHA256.csv (generated LAST by the
parent); the AUDIT_ENTRYPOINT.md new-run row + source-row standing
annotation; the ONE ordinary commit, fast-forward push and remote
re-verification. Nothing was staged; no historical file, no foreign
untracked path and no file outside OUTPUT_ROOT was modified; python -B
everywhere (no __pycache__ residue). The post_qc columns of
MAPPER_BOUNDARY_RESULTS.json honestly say DEFERRED_TO_QC_PHASE.

## 8. Standing ceilings preserved verbatim (unchanged by this correction)

```text
R_PLUS4_FIRST_INITIALIZATION = PRESERVED_CONFIRMED_STATIC_CONDITIONAL
T_EQUALS_FIRST_INITIAL_P = NOT_ESTABLISHED_WITHIN_BOUND
R_PLUS4_VALUE_PRESERVED_TO_LATER_USE = NOT_ESTABLISHED
ACTUAL_LATER_OVERWRITE_OBSERVED = NO (bounded negative only)
T_NOT_EQUAL_W_AT_LATER_USE = NOT_ESTABLISHED_WITHIN_BOUND   (new explicit row)
R_NOT_EQUAL_T_AT_LATER_USE = NOT_ESTABLISHED_WITHIN_BOUND   (new explicit row)
P_HEAP_ORIGIN = NOT_ESTABLISHED
P_ALLOCATION_OR_STORAGE_ORIGIN = NOT_ESTABLISHED_WITHIN_BOUND
LOOKUP_SEMANTIC = UNRESOLVED
MODEL_ROOT_RELATION = UNKNOWN
WORLD_INSTANCE = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
GENERAL_PE_MAPPER_CORRECTNESS = NOT_ESTABLISHED
CANONICAL_GATE_EFFECT = NONE
NEW_DESKTOP_POST_AUDIT = NOT_PERFORMED
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
```

CORRECTION_VERDICT (executor self-assessment, explicitly labelled
SELF_CHECK — the independent QC and MASTER review are separate parent
phases): PASS — all mandated P2-A/P2-B/P2-C/P3 predicates hold on the
measurements above; known UNKNOWN/NOT_ESTABLISHED statuses are NOT errors
of this correction.
