# FINAL_REPORT — PE_GAMEBRYO_ORACLE_F1_RTTI_CORRECTION_R1_20261003

```text
RUN_ID            = PE_GAMEBRYO_ORACLE_F1_RTTI_CORRECTION_R1_20261003
REPO              = D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean
BASE_SHA          = abc3f8f6f9e35dd8aebbe2cfe525d710e4338acd
RUN_CLASS         = LOAD_BEARING
RUN_TYPE          = DESKTOP_POST_AUDIT_FOCUSED_CORRECTION (F1 only)
EXECUTOR          = pe-reconstruction (PE-MASTER direct dispatch, NO_NESTED_TASKS)
QC_SCOPE          = SELF_CHECK_F1 (no independent reviewer agent available; independence discipline: expectations derived from the pinned source + hand-built fixtures BEFORE the fix, counterexamples re-executed after)
SOURCE_ORACLE     = NiStream.cpp SHA256 E955C36EBBB442029E00BE8A154726741B8454A607F2DC043F1FD542B009DC25 (verified at run start + re-verified at run end; size 38,458 B)
```

## 1. Mission

Fix ONLY Desktop finding F1 (from
`PE_GAMEBRYO_ORACLE_TOOL_DESKTOP_POST_AUDIT_20261003`, report SHA256
`ECE2D452...`): the GB1.2 oracle must validate the ENTIRE RTTI table in
source `NiStream::LoadRTTI` order, including unused entries. The published
adapter validated via object `type_idx` and could skip unregistered/unused
RTTI entries (its counterexample: `[NiNode, NiXyzzyx]` with the only object
using NiNode -> `accepted=true`, `unregistered_types=[]`).

## 2. Independent source derivation (made BEFORE the fix)

`04_ANALYSIS/SOURCE_ORDER_DERIVATION.md` derives the mandatory control flow
from the pinned `NiStream.cpp` L412-449 alone: u16 count -> per entry
LoadRTTIString -> factory check -> next entry; the FIRST unregistered name
aborts with RTTIError -> Load() false BEFORE any later table name, any
object type index (L436-444), the object groups (L470-487) or any body.
Per-fixture expected verdicts were pinned there before the code edit. Two of
the hand-built fixtures came out byte-identical to the Desktop auditor's
independently built fixtures (fx_A == synthetic_valid_node.nif
`48B24BB5...`, fx_B == unused_unregistered_rtti.nif `BEDE862D...`),
cross-validating the derivation twice.

## 3. The fix (change set)

`tools/gamebryo_oracle/gb12core.py` b_new branch (the ONLY functional
change; legacy `< 5.0.0.1` inline-RTTI layout NOT migrated; registry
`adapters/gb12/registry.py` NOT touched — empty diff verified):

- The RTTI table is now scanned in SOURCE ORDER: one name -> factory check
  -> next name. The first unregistered entry fails the factory gate and, in
  ordinary fail-closed mode, the adapter returns IMMEDIATELY (later table
  names, object indices, groups and bodies are never read and never
  reported).
- Unused table entries are validated (they are part of the scan).
- `rtti_table_validation` (new canonical JSON key) separates the table-order
  factory scan (`first_rtti_miss`, `first_miss_table_index`, `names_read`,
  `full_table_read`, `unregistered_table_entries`,
  `source_predicted_verdict`, `extension_observation`) from the OBJECT-side
  artifacts `object_reference_histogram` + `object_reference_census`
  (the per-object u16 indices, LoadRTTI L436-444), which are only produced
  when the index list was actually read. `type_histogram` is kept unchanged
  as the legacy alias consumed by the compare adapter.
- `rtti_gate` is kept as a deprecated compact alias whose content is now
  the TABLE scan (its old object-order semantics were the F1 defect).
- `--full-decode` (OUR extension, never original behavior) continues
  inspection past the miss but KEEPS
  `rtti_table_validation.source_predicted_verdict=REJECTED` and
  `first_rtti_miss` = the first miss in TABLE order, labels every
  continuation (`extension_observation`), and if the extension itself hits
  a parser failure (truncated later table name, corrupt/incomplete object
  indices) it halts with an `EXTENDED_*` warning — the source-predicted
  verdict is never masked.
- Header citation block + `--full-decode` doc + README + schema updated
  (`schemas/oracle_result.schema.json` gains the three new optional keys).
- Permanent regression battery added to `tests/test_gb12.py`
  (`f1_rtti_table_tests`, 8 controls, s18 discipline).

## 4. Mandatory tests (raw records in 02_RAW_TESTS/, each with input
identity, command, stdout, stderr, exit code; QC re-execution in
03_QC_SELF_CHECK/QC_REEXECUTION_COUNTEREXAMPLES.json)

| test | pre-fix (pinned code) | post-fix (final code) | verdict |
|---|---|---|---|
| Counterexample reproduction (B: `[NiNode, NiXyzzyx]`, only object NiNode) | `accepted=true`, `unregistered_types=[]`, exit 0 (BEFORE_FIX_fx_B_counterexample) | `accepted=false`, `RTTIError(NiXyzzyx)`, first miss table index 1, names_read=2 (AFTER_FIX_B_unused_unregistered) | PASS — the exact Desktop bug reproduced then fixed |
| A: registered-only NiNode | accepted=true (Desktop + our fx_A baseline) | accepted=true, roots=[0], census present, exit 0 (AFTER_FIX_A_registered_only) | PASS — baseline preserved |
| B: unused unregistered entry | (as above) | ordinary mode REJECTS on NiXyzzyx; no histogram/census/objects reported past the miss | PASS |
| C: >=2 unregistered entries + object order != table order | `RTTIError(NiQuuxzyx)` — OBJECT-order miss (BEFORE_FIX_C1/C2) | `RTTIError(NiXyzzyx)` @ table index 1 in BOTH ordinary and full-decode (AFTER_FIX_C2_*, QC_REEXEC) | PASS — first miss determined by TABLE order |
| D: B/C with --full-decode | C full-decode: `RTTIError(NiQuuxzyx)` (wrong miss) | SOURCE_PREDICTED_VERDICT=REJECTED, FIRST_RTTI_MISS=NiXyzzyx@1, extension explicitly labeled, bodies inspected (C2: obj0 NiNode decoded 98..186, obj1 NiQuuxzyx boundary-only UNREGISTERED 186..190, obj2 NiNode decoded 190..278, roots=[0]); B full: census shows table index 1 unreferenced by any object yet validated | PASS |
| E: unused first table miss + incomplete later indices | `DECODE_ERROR: CLOSURE_SEARCH_FAILED` (indices misread; BEFORE_FIX_fx_E) | `RTTIError(NiXyzzyx)` — terminates at the factory miss, index list never read (AFTER_FIX_E_incomplete_indices) | PASS |
| F: first table miss + truncated later RTTI name | uncaught `DecodeError` traceback, exit 1, empty stdout (BEFORE_FIX_fx_F) | ordinary: `RTTIError(NiXyzzyx)`, name[2] never read; full-decode: RTTIError preserved + `EXTENDED_TABLE_READ_FAILED` halt warning, partial=true (AFTER_FIX_fx_F*, QC_REEXEC) | PASS — earlier factory miss not masked |
| G: targeted T1/218757 regression (payload 3E8A22C2..., byte-identical to the published pin) | published: inspect_T1_gb12_full.json | 66/66 objects DEEP-IDENTICAL (names, local transforms, byte boundaries, links all equal; histogram, roots [0], 27 edges, controllers/properties/textures/bounds, object_count_check all identical; full-decode stdout deterministic across 2 runs) | PASS — see §6 for the only (justified) metadata deltas |

Whole-corpus run: NOT executed (per contract). T3 completion: NOT executed.

## 5. In-run corrections (honest record)

1. The first fix implementation did not guard the first-miss assignment:
   under `--full-decode` a LATER unregistered entry overwrote
   `first_rtti_miss` (C2 full-decode reported NiQuuxzyx@2 instead of
   NiXyzzyx@1). Mandatory test C caught it; fixed with a first-miss-only
   guard; the ENTIRE after-fix battery was then re-captured with the final
   code (all records in 02_RAW_TESTS/ are from the final code).
2. Fixture F's first builder pass placed the truncated 3rd name outside
   the table; rebuilt (count=3, truncated name inside) BEFORE any
   post-fix run; the pre-fix record was re-captured on the corrected bytes.
3. Fixture C was split into C1 (trailing unknown run — kept as a permanent
   input) and C2 (middle unknown run — the actual test C) after C1's
   full-decode tripped a pre-existing presolver crash under BOTH code
   versions (see §7).

## 6. Test G: the only metadata changed by F1 (all justified, all measured)

T1 full-decode old vs new (deep JSON diff, excluding the new keys):
- ADDED keys: `rtti_table_validation`, `object_reference_histogram`,
  `object_reference_census` (the F1 separation).
- `rtti_gate`: content now the TABLE scan (`scan_basis`,
  `deprecated_alias_of` added; `unregistered_types` identical for T1 — its
  table order happens to coincide with object order here).
- `unknowns` 8 -> 5: the 4 class-level duplicate records (an artifact of
  the old object-order collection) reduce to 1 source-predicted
  first-miss record; the complete table list moved to
  `rtti_table_validation.unregistered_table_entries` (all 4 NiArk classes,
  same list); the 4 per-block records (indices 1, 2, 3, 13) are unchanged
  and still carry all 4 class names, so the compare adapter's unknown-class
  SET is unchanged.
- `decode_continued_after_rtti_gate` warning text extended with
  SOURCE_PREDICTED_VERDICT / FIRST_RTTI_MISS.
T1 ordinary old vs new: verdict and error IDENTICAL
(RTTIError(NiArkAnimationExtraData)); the old build reported a full
66-reference histogram that the original loader never reads (it fails at
table entry 1 of 12 before any index); the fixed build reports names_read=2
and no histogram/census — exactly the contract's "do not report data the
fail-closed mode did not actually read".
The new first table miss `NiArkAnimationExtraData`@1 independently CONFIRMS
the Desktop auditor's own header/RTTI-only read of the corpus (same name,
same order claim). The five historical payloads' recorded misses keep their
independent basis (Desktop §4 F1 note).

## 7. Pre-existing, OUT-OF-SCOPE defects observed (documented, NOT fixed)

- `fx_C1_trailing_unknown_run.nif --full-decode` exits 1 with an IndexError
  in the E3 pre-solver (`assemble` -> `decode_block_at(b, run_end)` with
  run_end == n_obj for a trailing unknown run). Proven PRE-EXISTING by
  running the same input under the pre-fix code (git stash; both exit 1,
  identical traceback shape). This is the Desktop F4 presolver-boundary
  territory ("IndexError w presolverze") and stays untouched per the scope
  guard. Minimal regression case + this run's records are preserved
  (BEFORE_FIX_C1_full_decode_presolver_crash / AFTER_FIX_C1_full_decode_
  presolver_crash_preexisting) for the future F4 fix.
- Two battery controls fail on the T1 NiArk payload in ordinary mode
  (`object_count_mismatch_detected`, `link_failure_detected`): both are
  PRE-EXISTING (identical failure set under the pre-fix code, same payload)
  — the controls can only fire after a body/link phase that an RTTI-failing
  payload never reaches in ordinary mode. F2/F4-adjacent battery limitation;
  not a regression; recorded in 03_QC_SELF_CHECK/FINAL_payload_battery_*.
- All other existing self-tests pass (11 original + 8 new F1 controls,
  0 failures; FINAL_self_and_f1_battery.stdout).

## 8. Scope guard compliance

F2 (acceptance/coverage/link predicate), F3 (compare input identity), F4
(structured exceptions/presolver), F5 (report semantics), F6 (process
ledger), F7 (provenance), T3 solver: NOT touched (diff hunk map confirms
changes only in the two doc blocks + the b_new RTTI region of gb12core.py,
plus schema/tests/README). Registry unchanged. Legacy inline-RTTI layout not
migrated. No PCG client run, no placement RE, no new traces, no corpus-wide
execution. PLACEMENT CONTEXT import: NOT USED (optional per contract; the
R2 placement research context was not needed for F1 and is not transferred
to the HANDOFF).

## 9. Persistence

Path-limited commit + fast-forward push (see HANDOFF.md for SHAs). The
foreign untracked paths (PE_935_* audit dirs, experiments/) were NOT
staged, committed or modified. Repo policy compliance: the six synthetic
fixture .nif files are NOT committed (repo-wide `*.nif` gitignore — zero
NIF files tracked anywhere in the repo, the same convention as the
published run); the committed `build_fixtures.py` regenerates them
deterministically byte-identically (SHA pins in INPUT_IDENTITIES.md), and
physical copies are preserved in the run's external sandbox
(`D:\Eudoria_Reconstruction\99_Audits\
PE_GAMEBRYO_ORACLE_F1_RTTI_CORRECTION_R1_20261003\sandbox\01_FIXTURES\`).
No SDK or proprietary game payload is committed. The output package was
finalized (all records from the final code), then MANIFEST_SHA256.csv was
generated over the committed package content and the bijection physical
files minus manifest <-> manifest rows verified before the commit.

## 10. Terminal fields (exact)

```text
F1_RTTI_TABLE_SOURCE_ORDER = FIXED_AND_VERIFIED
F2_TO_F7 = NOT_ADDRESSED_IN_THIS_RUN
QC_SCOPE = SELF_CHECK_F1
QC_VERDICT = SELF_CHECK_QC_PASS_WITH_FINDINGS
GENERAL_ORACLE_FAIL_CLOSED = NOT_ESTABLISHED
GENERAL_SOURCE_EQUIVALENCE = NOT_ESTABLISHED
T3_COMPLETION_EXECUTED = NO
NEW_PCG_TRACE_EXECUTED = NO
WORLD_PLACEMENT_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
NEXT_RUN_EXECUTED = NO
```

QC_VERDICT rationale: every F1 contract test (counterexample reproduction,
A-G) passes with raw records and a dedicated QC re-execution of the
counterexamples; the one in-scope implementation defect found (first-miss
overwrite under --full-decode) was caught by the mandatory test C itself
and fixed before final capture. "FINDINGS" = the three documented
pre-existing OUT-OF-SCOPE observations in §7 (presolver boundary crash,
two pre-existing battery control failures) — none is an F1 failure, none
was widened into scope, and all are handed to the F2-F7 backlog with their
minimal regression inputs preserved.
