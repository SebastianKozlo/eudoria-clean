# FINAL_REPORT — PE_GAMEBRYO_ORACLE_F2_C1_C2_ACCEPTANCE_GUARDS_R1_20261004

RUN: PE_GAMEBRYO_ORACLE_F2_C1_C2_ACCEPTANCE_GUARDS_R1_20261004
REPO: `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean` (GitHub
`SebastianKozlo/eudoria-clean`, branch `master`)
BASE_SHA (re-verified at run start): `d497b44d85570b8bf94153ba0c08634d0992b302`
= local HEAD = local origin/master = actual remote master (`git ls-remote`).
Executor: pe-reconstruction, PE-MASTER direct dispatch, NO_NESTED_TASKS.
QC_SCOPE = SELF_CHECK_F2_C1_C2 (executor self-check; NO independent
reviewer — no independent QC is claimed). STATIC-ONLY — no client ran.

## Mission (bounded): fix ONLY F2-C1 and F2-C2

Desktop post-audit
`C:\Users\User\Documents\ChatGPT\PE\PE_GAMEBRYO_ORACLE_F2_DESKTOP_POST_AUDIT_20261003\REPORT.md`
found (read in full this run):

- **F2-C1/P2**: a nonzero user-defined version could end
  SOURCE_PREDICTED=ACCEPTED + TOOL_VERDICT=PASS although the pinned source
  rejects it (LoadHeader user-version gate).
- **F2-C2/P2**: an out-of-range LoadTopLevelObjects root ID did not
  participate in link-integrity and could end ADAPTER_INTEGRITY=PASS +
  TOOL_VERDICT=PASS.

The earlier F2 cases (REGISTERED_BUT_NOT_DECODED, invalid body/child link)
were already fixed at BASE and are NOT reinterpreted as oracle completeness.

## Source premises (independently re-verified this run by direct read;
NiStream.cpp SHA256 E955C36EBBB442029E00BE8A154726741B8454A607F2DC043F1FD5
42B009DC25 confirmed)

- L46-50: `ms_uiNifMinUserDefinedVersion = ms_uiNifMaxUserDefinedVersion =
  GetVersion(0,0,0,0) = 0`; `NULL_LINKID = 0xffffffff`.
- L111-112 (constructor): `m_uiNifFileUserDefinedVersion = 0` (era member
  semantics below the 10.0.1.8 read threshold).
- L334-337: user-defined version read iff file version >= 10.0.1.8;
  L340-345 `< min` -> OLDER_VERSION return false; L347-352 `> max` ->
  LATER_VERSION return false — both BEFORE the uiObjects read L355-357.
- L506-509 LoadStream: `!LoadHeader()` -> `return false` — a nonzero
  user-defined version is a SOURCE-PROVEN UNAMBIGUOUS PROPAGATED REJECTION
  -> SOURCE_PREDICTED=REJECTED (not UNRESOLVED).
- L362-385 LoadTopLevelObjects: NULL_LINKID -> NULL (L374-377); else
  DEBUG-only assert (L380) + UNCHECKED GetAt (L381; NiTArray.inl L135-139
  SHA256 C35D866D...: raw `m_pBase[uiIndex]`); the function is VOID and is
  called unconditionally at LoadStream L566; L634 returns true
  unconditionally — an out-of-range top-level root has NO unambiguous
  propagated failure -> SOURCE_PREDICTED=UNRESOLVED (never auto-REJECTED).

## The fixes (tools/gamebryo_oracle/; only C1/C2 correction + tests +
schema + docs; no other behavior touched)

### F2-C1 — user-defined version gate (gb12core.py decode() header stage)

The pinned gate `[0.0.0.0, 0.0.0.0]` is now enforced exactly where the
source enforces it: after the NIF version gate, the field is read iff
version >= 10.0.1.8 and gated (< min -> OLDER_VERSION; > max ->
LATER_VERSION) with a SOURCE-FAITHFUL EARLY REJECTION (the rejection
precedes the uiObjects read L355-357; no object bytes are decoded just to
obtain counts). A nonzero user-defined version now ends, in BOTH ordinary
and --full-decode: SOURCE_PREDICTED_ORIGINAL_VERDICT=REJECTED,
TOOL_VERDICT=FAIL, load_result.accepted=false, inspect exit != 0;
ADAPTER_DECODE_COVERAGE=NOT_MEASURED and ADAPTER_INTEGRITY=NOT_MEASURED
with the 5 object-level counters null + explicit per-counter reasons and
header_num_blocks=null (the uiObjects field was never read). --full-decode
cannot bypass a source-proven LoadHeader rejection (the rejection precedes
every object byte). The measured gate state is reported in a new
`user_version_gate` object (`read_from_stream`,
`measured_user_defined_version`, `verdict` ACCEPTED/REJECTED/
NOT_APPLICABLE_ERA, `reason`); below the 10.0.1.8 read threshold the
source-faithful era semantics is recorded honestly (the original compares
the constructor-initialized member 0 against [0,0] — trivially satisfied).
Central invariant SOURCE_PREDICTED=REJECTED ⇒ TOOL_VERDICT=FAIL flows
through the existing single TOOL_VERDICT derivation site (unchanged law).

### F2-C2 — top-level root link integrity (gb12core.py footer stage)

The parsed top-level root IDs now participate in overall link-integrity.
The RAW representation is preserved for provenance (`scene_graph.roots`,
signed i32 as read — unchanged); VALIDATION normalizes each ID to u32
(`raw & 0xFFFFFFFF`) so a signed -2 == 0xFFFFFFFE cannot bypass; the valid
domain is exactly the pinned source domain: NULL_LINKID 0xFFFFFFFF OR
`< header_num_blocks` (no invented sentinels, no clamping, no rewriting, no
silent dropping). New measured fields inside `adapter_integrity_checks`
(schema-consistent): `top_level_root_link_integrity` (PASS/FAIL),
`top_level_root_failure_count`, `top_level_root_checked_count`,
`top_level_root_raw`, `top_level_root_normalized_u32`. A non-NULL
normalized root outside [0, header_num_blocks) =>
TOP_LEVEL_ROOT_LINK_INTEGRITY=FAIL ⇒ aggregate LINK_INTEGRITY=FAIL ⇒
ADAPTER_INTEGRITY=FAIL ⇒ TOOL_VERDICT=FAIL, accepted=false, exit != 0, in
BOTH modes. SOURCE stays UNRESOLVED for an invalid root (new explicit
UNRESOLVED branch citing L362-385/L380/L381/void — never auto-REJECTED).

### SOURCE REASON CORRECTION (mandatory wording fix, both verdict paths)

The b_new ACCEPTED reason now cites MEASURED fields — "LoadTopLevelObjects
MEASURED in range (top_level_root_checked_count=N,
top_level_root_failure_count=0 ...)" and "every body link and every
top-level root is MEASURED NULL or in range (link_failure_count=0,
top_level_root_failure_count=0)" — and carries the user-defined-version
gate status ("MEASURED: read user_defined_version=..." or the explicit
era-conditional member-0 wording). The legacy (< 5.0.0.1) ACCEPTED reason
now explicitly states the era-conditional gate semantics, that "every raw
BODY link ID ... is MEASURED NULL or in range (raw_out_of_range_link_ids=0)"
and that the legacy adapter path reads NO footer roots so NO
LoadTopLevelObjects claim is made there. It is no longer possible for a
SOURCE=ACCEPTED reason to claim "LoadTopLevelObjects in range" or "every
link is NULL or in range" unless the roots were actually normalized,
measured and passed, nor to claim the complete LoadHeader path content-valid
unless the user-defined version gate was actually checked.

## Measured results (all executed; records in 02_RAW_TESTS/, QC matrix in
03_QC_SELF_CHECK/QC_REEXECUTION_GUARDS.json)

### F2-C1 controls (both ordinary and --full-decode; fixtures differ ONLY
in the user-version DWORD)

| control | PRE-FIX (pristine d497b44d) | POST-FIX |
|---|---|---|
| VALID_USER_VERSION_0 (fx_VALID, 167B/48B24BB5) | ACCEPTED/COMPLETE/PASS/PASS, accepted=true, exit 0 | **UNCHANGED**: ACCEPTED/COMPLETE/PASS/PASS, accepted=true, exit 0 (no over-fail-closed) |
| INVALID_USER_VERSION_1 (fx_C1, 167B/C643F2D2) | ACCEPTED/COMPLETE/PASS/PASS, accepted=true, **exit 0 (the defect, reproduced)** | **REJECTED / coverage NOT_MEASURED / integrity NOT_MEASURED / TOOL=FAIL, accepted=false, exit 2**; user_version_gate.verdict=REJECTED, measured 0.0.0.1; 5 object-level counters null with reasons; header_num_blocks=null; objects=[] |

### F2-C2 controls (both modes; fixtures differ ONLY in the footer/root DWORD)

| control | raw root | normalized u32 | PRE-FIX | POST-FIX |
|---|---|---|---|---|
| VALID_ROOT_0 | [0] | [0] | PASS/exit 0 | PASS/exit 0 (tool PASS, top_root PASS/0) |
| INVALID_ROOT_9999 | [9999] | [9999] | ACCEPTED + INTEGRITY=PASS + TOOL=PASS + accepted=true + exit 0 (**defect reproduced**; scene_graph.roots=[9999]) | **UNRESOLVED source / COMPLETE coverage / top_root=FAIL(1) / link_integrity=FAIL / ADAPTER_INTEGRITY=FAIL / TOOL=FAIL / accepted=false / exit 2**; raw [9999] preserved, no clamping |
| INVALID_ROOT_FFFFFFFE | [-2] | [4294967294] | ACCEPTED + PASS + exit 0 (**signedness bypass reproduced**) | **UNRESOLVED / COMPLETE / top_root=FAIL(1) / integrity=FAIL / TOOL=FAIL / accepted=false / exit 2** — the u32 normalization blocks the -2 bypass |
| NULL_ROOT_FFFFFFFF | [-1] | [4294967295] | ACCEPTED + PASS + exit 0 | **NOT an out-of-range failure** (top_root=PASS, failure_count=0, zero TOP_LEVEL_ROOT_FAILURE warnings; verified by fixture EXECUTION); this fixture is otherwise the valid base, so it also ends SOURCE=ACCEPTED + TOOL=PASS + exit 0 — the NULL permission itself is NOT evidence of acceptance, only that this root value is not an out-of-range failure |

Ordinary and --full-decode AGREE on the guard outcome for every control
(QC `qc_mode_agreement_*`: 11/11 controls).

### Original F2 regression (semantics preserved; both modes)

| case | POST-FIX (identical to the published d497b44 semantics) |
|---|---|
| REGISTERED_BUT_NOT_DECODED (285B/87708915) | SOURCE=UNRESOLVED, coverage INCOMPLETE (2 semantic + 1 boundary; registered_but_not_decoded=1, classes=[NiCamera]), integrity UNRESOLVED, TOOL=UNRESOLVED, accepted=false, exit 2 |
| INVALID_BODY_LINK (171B/36672FA7) | SOURCE=UNRESOLVED, coverage COMPLETE, LINK_INTEGRITY=FAIL (link_failure_count=1), integrity FAIL, TOOL=FAIL, accepted=false, exit 2 |
| VALID NiNode (167B/48B24BB5) | PASS/exit 0 both modes |

### F1 / F1-C1 regression

Full existing battery executed pre (pristine bytes) and post: PRE 42
checks / 0 failures; POST 59 checks / 0 failures — ALL 42 historical check
identities still PASS (0 missing), plus 17 new F2-C1/C2 checks. C1A
(94B/928A1447...) and C1B (196B/719AEB3...) in both modes: exit 2,
RTTIError preserved (first_rtti_miss=NiDesktopFirstMissing@1), full-decode
STOP_AT_TABLE_FAILURE preserved, objects=[], no object-level census, the 5
object-level counters null with reasons. F1/F1-C1 NOT reopened (no new
reproducing counterexample exists).

### T1 targeted regression (218757.nif, identity re-verified 57,316 B /
3E8A22C2213202207E374B55CD65B2C3BE039CCDD1E8D01A07FCAF44DE12CF36)

Complete objects[] 66/66 DEEP-IDENTICAL vs the d497b44 baseline — verified
against TWO independent baselines: (1) this run's PRE-fix pristine-worktree
record, (2) the pinned historical F2-package d497b44 record; 0 recursive
diffs against both (t1_deep_regression.py; 04_REGRESSION/T1_REGRESSION_
FINAL.stdout all PASS). Interpretation remains 62 known semantically
decoded + 4 opaque/boundary-only (NOT promoted to 66 semantic decodes);
FIRST_RTTI_MISS=NiArkAnimationExtraData@1, SOURCE_PREDICTED=REJECTED,
TOOL_VERDICT=FAIL, WORLD_PLACEMENT_RECOVERED=NO. Whole-JSON delta vs BASE
confined exactly to the new F2-C1/C2 metadata: top-level `user_version_gate`
(ADDED), `input_identity.user_defined_version_u32` (ADDED), the 5
`adapter_integrity_checks.top_level_root_*` fields (ADDED) — zero changes
inside objects[].

### Non-inspect CLI (probe-version / compare / capabilities; F3 stays OPEN)

Byte-identical stdout, stderr and identical exit codes PRE (pristine
d497b44d bytes) vs POST on all 5 command pairs: probe-version fx_VALID;
capabilities (all); capabilities --adapter gb12; compare with the pinned
historical `--oracle-result` pair; compare with the internal-inspect pair
(03_QC_SELF_CHECK/noninspect_records/*.json, all `byte_identical` true).
No exit semantics/behavior change.

### Battery pre/post (pristine d497b44 bytes vs corrected bytes)

Payload battery on the T1 sandbox copy: PRE 49 PASS + 2 FAIL; POST 66 PASS
+ 2 FAIL — the 2 failures are the SAME PRE-EXISTING controls
(`object_count_mismatch_detected`, `link_failure_detected` — placeholder
controls that cannot fire on RTTI-failing payloads in ordinary mode;
documented pre-existing at BASE, identical failure set pre/post, NOT fixed
here — out of scope). Self battery: PRE 42/0, POST 59/0.

## SELF_CHECK_F2_C1_C2 (QC; executor self-check, NOT independent QC)

`03_QC_SELF_CHECK/qc_reexecution.py` re-executes every mandatory control in
BOTH modes against the current tool (fresh CLI executions) and verifies the
full predicate matrix — 58/58 PASS, 0 failures
(QC_REEXECUTION_GUARDS.json + qc_reexecution.stdout):
fixture SIZE/SHA256 pins (9) + T1 identity; C1 valid/invalid; C2
root 0/9999/FFFFFFFE/FFFFFFFF; regression preservation (REGNOTDEC,
INVALID_BODY_LINK, C1A, C1B, T1 both modes); T1 first-miss + 62/4
interpretation; ordinary/full guard-outcome agreement (11 controls);
central invariants over all 22 re-executed results (SOURCE=REJECTED ⇒
TOOL=FAIL; integrity=FAIL ⇒ TOOL=FAIL; exit==0 iff TOOL=PASS; accepted ==
(TOOL_VERDICT==PASS)); determinism (run1 == run2); PRE-fix defect
reproduction on the pristine BASE records (6/6: C1 + root9999 +
rootFFFFFFFE all SOURCE=ACCEPTED/TOOL=PASS/accepted=true/exit 0 in both
modes pre-fix); PRE-fix raw root representations ([9999], [-2], [-1]).

QC explicitly verified: unsigned normalization of root IDs (raw -2 ->
u32 4294967294 -> FAIL); -2/0xFFFFFFFE does NOT bypass the range check;
-1/0xFFFFFFFF handled per NULL_LINKID source semantics (no out-of-range
failure, by fixture execution); ordinary and --full-decode AGREE on every
guard outcome; a source rejection cannot become TOOL PASS; adapter
integrity FAIL cannot become TOOL PASS.

## Terminal fields

```text
F1 = PRESERVED
F1_C1 = PRESERVED
F2_REGISTERED_UNDECODED = PRESERVED_FIXED
F2_INVALID_BODY_LINK = PRESERVED_FIXED
F2_C1_USER_VERSION_GATE = FIXED_AND_VERIFIED
F2_C2_TOPLEVEL_ROOT_LINK = FIXED_AND_VERIFIED
NONZERO_USER_VERSION_FALSE_SUCCESS = REJECTED
INVALID_TOPLEVEL_ROOT_9999_FALSE_SUCCESS = REJECTED
INVALID_TOPLEVEL_ROOT_FFFFFFFE_FALSE_SUCCESS = REJECTED
NULL_TOPLEVEL_ROOT_FFFFFFFF = SOURCE_VALID_SENTINEL_PRESERVED
ROOT_UINT32_NORMALIZATION = VERIFIED
ORDINARY_AND_FULL_DECODE_GUARDS = VERIFIED
VALID_USER_VERSION_CONTROL = PASS
VALID_ROOT_CONTROL = PASS
SOURCE_REJECTION_IMPLIES_TOOL_FAIL = YES
TOPLEVEL_ROOT_INTEGRITY_ENFORCED = YES
F2_OVERALL = FIXED_AND_VERIFIED
GENERAL_ORACLE_FAIL_CLOSED = NOT_ESTABLISHED
GENERAL_SOURCE_EQUIVALENCE = NOT_ESTABLISHED
F3_TO_F7 = NOT_ADDRESSED
O1 = NOT_ADDRESSED
T3_COMPLETION_EXECUTED = NO
NEW_PCG_TRACE_EXECUTED = NO
WORLD_PLACEMENT_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
NEXT_RUN_EXECUTED = NO
```

## Scope guard compliance

NO Gamebryo class loaders added (registry unchanged, LOADERS unchanged);
presolver/F4 untouched; compare/F3 untouched (byte-identity verified); no
report/process/provenance F5-F7 work; O1 untouched; T3 not run; no
corpus-wide decode; no PCG client; no placement RE; no milestone change.
Historical packages F1 / F1-C1 / F2 untouched (verified: git status shows
no modification under docs/audits/PE_GAMEBRYO_ORACLE_F*). Foreign
untracked paths (five docs/audits/PE_935_* folders + experiments/) NOT
touched, NOT committed.

## Remaining backlog (unchanged, open)

F3 (compare same-input/comparison validity), F4 (presolver defects —
pre-first-miss DecodeError; trailing-run IndexError), F5-F7 (report
wording/process ledger/HUMAN ORDER verbatim/float bit-exact), O1, T3
completion. The 2 pre-existing payload-battery placeholder controls remain
(as documented).
