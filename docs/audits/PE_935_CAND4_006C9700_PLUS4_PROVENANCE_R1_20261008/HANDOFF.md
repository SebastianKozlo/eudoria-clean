# HANDOFF — PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008 (FINAL)

Final handoff of the persistence/publication phase (pe-master-auditor under
direct PE-MASTER dispatch; NO_NESTED_TASKS). This file supersedes the
executor-phase HANDOFF (same path, rewritten at the persistence phase — the
flow the executor-phase handoff itself declared); the executor's MEASURED
content is preserved in the fields below (values identical to the executor's
measurements and to FINAL_REPORT.md / QC_REPORT.md / the ledgers). The only
phase-specific updates are the persistence fields (QC, PE-MASTER review,
census, publication state). RESULTING_SHA and REMOTE_SHA are governed by
contract §8 (exactly one normal commit; the manifest is generated LAST; the
resulting SHA must not be written into any file of the same commit): their
post-push values are recorded at the terminal handoff returned by this worker
to PE-MASTER, NOT embedded in any file of this commit.

## TERMINAL FIELDS BLOCK (contract §9 — actual measured values)

```text
RUN_ID = PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008
BASE_SHA = 97823c6180b0a35a8f5c43e45c29076d48208bee
RESULTING_SHA = recorded at the terminal handoff per contract §8 — not
  embedded in this commit's files
REMOTE_SHA = recorded at the terminal handoff per contract §8 — not
  embedded in this commit's files (post-push predicate: LOCAL_HEAD ==
  origin/master == actual remote master == RESULTING_SHA, measured live by
  ls-remote; recorded at the terminal handoff)
SCIENCE_EXECUTED = YES (bounded static RE; the two required results measured;
  STATIC_ONLY — the client never ran; no runtime, no payloads, no network
  science; no EXE access in the persistence phase)
RUN_STATUS = SCIENCE_AND_QC_COMPLETE__PERSISTENCE_EXECUTING (measured at
  handoff finalization: preflight PASS; preregistration BEFORE analysis;
  bounded science executed with STOP_BEFORE_EXCEED honored; fresh internal QC
  QC_PASS; PE-MASTER MASTER_ACCEPTED advisory persisted verbatim as
  PE_MASTER_REVIEW.md; this persistence phase = review/handoff/entrypoint/
  manifest + gates + one normal commit + fast-forward push per contract §8;
  the post-push state is recorded at the terminal handoff; HARD_STOP = YES)

RETURN_VALUE_ORIGIN (primary result 1) = ALLOCATION + CONSTRUCTION: R
  (non-NULL) = the 0x10-byte heap object allocated inside FUN_006C9700 (size
  push 6A 10 @0x006C97B9; call @0x006C97BB -> 0x0095D3C4 operator new per
  prior canon) and constructed by FUN_006E8F70(this=allocation, arg1=S,
  arg2=P) @0x006C97D8 (rel32 verified), which returns this (mov eax,esi
  8B C6 @0x006E9014); the pump returns it (mov eax,esi 8B C6 @0x006C9808).
  Exact source expression = the ctor's this; origin category =
  ALLOCATION+CONSTRUCTION; path predicate PATH_B: S =
  FUN_00823C10(FUN_00415670(&{0x66,A},arg2,arg3,1)) != NULL AND the
  arg1-slot != 0 after FUN_006C9570 AND new(0x10) != 0; 4 NULL alternatives
  measured with predicates; 5 paths RESOLVED (RETURN_VALUE_TRACE.csv).
  Status: CONFIRMED at the physical-store/path-structure level (byte-measured
  stores; static path structure, NOT an observed execution). Base RESOLVED;
  NO adjustment.
RETURNED_OBJECT_CLASS_IDENTITY = R layout {+0:S, +4:P(refcounted),
  +8:0/conditional, +0xC:0}; NO vptr in the construction dataflow -> class
  NAME UNKNOWN within bound (QC independently confirmed the no-vptr
  negative: the only base-R stores in the ctor are 89 06, 89 46 04, C7 07
  00..., C7 46 0C 00...). R != W (0x10 vs 0xC allocations); the CAND-4 path
  creates no W.

PLUS4_WRITER_AND_SOURCE (primary result 2) = FIRST INIT writer = ctor
  FUN_006E8F70 @0x006E8FA5 (mov [esi+4],eax; 89 46 04) = [R+4] := P, with
  the companion addref add [eax+4],ecx (01 48 04, ecx=1) @0x006E8FAF.
  Source: P = the pump's arg1-slot content, produced by the smart-pointer
  slot-setter FUN_006C9570 (pre-clear C7 06 @0x006C95A0; store 89 3E
  @0x006C9651; addref 01 5F 04 @0x006C9657) = the return of FUN_007B79B0
  (thiscall @0x006C9631, receiver [S+0x10]). Value at first init: a heap
  object address carrying the intrusive refcount protocol (refcount@P+4;
  destroy via vtable slot 1 at zero). LATER OVERWRITE: NOT_ENCOUNTERED_WITHIN_
  BOUND (the other [x+4] writes in the four opened bodies are refcount ops
  on base P; NOT a global census). DEEPER ORIGIN of P (inside FUN_007B79B0):
  NOT_ESTABLISHED_WITHIN_BOUND (body #4 PARTIAL, window cut @0x007B7A0F;
  internal callsites RAW_VISIBLE_ONLY; STOP_BEFORE_EXCEED honored at the edge
  budget 12/12) — honest bounded UNKNOWN. [R+4] RESOLVED_AS_POINTER for the
  CAND-4 chain (same-base dataflow, measured, not assumed); W's count@+4
  map applies to W's base only.

R_TO_T_RELATION_TYPE = R_CONTAINS_POINTER (CONFIRMED)
R_TO_T_ALIAS_STATUS = T == P PROVEN (alias of roles across two recorded
  callers + this run's measured store; NOT one observed execution); R != T
  (different bases)
R_TO_T_OWNERSHIP_STATUS = R holds ONE REFCOUNTED REFERENCE to P (the
  measured addref); release-on-destroy NOT_CHECKED (the neighbor destructor
  is RAW-visible only); the manager's retention is a SEPARATE reference with
  a DIFFERENT receiver

BUDGET (actual vs preregistered) = bodies 4/6 (FUN_006C9700, FUN_006E8F70,
  FUN_006C9570 RESOLVED; FUN_007B79B0 PARTIAL); edges 12/12 AT LIMIT NOT
  EXCEEDED (+9 RAW_VISIBLE_ONLY genuine; QC's own callsite census 8+5+5+3 =
  12 charged; the 13th unit does not exist); writers 2/4 (PW-1, PW-2; PW-3 =
  the honest boundary row); hops 3/3 AT LIMIT NOT EXCEEDED (HP-1 R->P; HP-2
  S->P; HP-3 T==P)
SCOPE_BUDGET_COMPLIANCE = WITHIN (no exceedance; no retroactive
  authorization; no analysis hidden in RAW labels — QC re-adjudicated row
  content, not just sums; QC consumed 0 new budget units; free repetitions
  only)

CONTROLS = CTRL_A..CTRL_G ALL PASS (SYNTHETIC_LOGICAL_CONTROL; each rejects
  its unauthorized inference; the proven T==P alias accepted as a legal
  result; no unauthorized promotion anywhere); mechanical: clean 80/80; MC1
  (own corruption 89 46 04 -> 89 47 04) DETECTED by the SAME production gate
  at PIN:CTOR_R4_STORE_P; MC4 (own rel32 bitflip -> target 0x006E8D70)
  DETECTED at REL32:REL_PUMP_CTOR_R; MC6 x3 specificity PASS (anchor gates
  PASS under unrelated corruption); EXE SHA unchanged after controls (all
  corruptions in-memory; the physical EXE was never modified)

QC_ORIGIN = pe-master-auditor fresh-context internal QC (internal to
  PE-MASTER; under direct PE-MASTER dispatch; NOT a Desktop post-audit; NOT
  independent of PE-MASTER — recorded; QC_RUN_ID =
  PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008_INTERNAL_QC_R1)
QC_VERDICT = QC_PASS (26/26 anchors MATCH by its own PE mapping — QCPE
  distinguishes RAW vs VIRTUAL_BSS, unlike the executor's OwnPE; 19/19
  rel32 + 15/15 rel8 own recomputes; 4/4 body windows byte-identical to the
  physical EXE; RTTI W chain re-walked for W only; strings re-read; clean
  80/80 independently re-run; own MC1/MC4 corruptions detected at the exact
  anchors; MC6 re-verified with direct file-offset corruptions + the
  executor's exact VA replay; 22/22 claims ACCEPT; 12+9 edge ledger rows
  honest and complete; bodies 4/6, writers 2/4, hops 3/3 honest; ceilings
  all held; standing science §7 preserved verbatim; 0 new budget units
  consumed)
PE_MASTER_REVIEW = MASTER_ACCEPTED (advisory; ADVISORY_PRE_QUALIFICATION;
  CANONICAL_GATE_EFFECT=NONE) — PE-MASTER independently re-measured from the
  physical EXE with its own VA->offset mapping: the six load-bearing rel32
  recomputations (0x006C6FFC->0x006C9700; 0x006C97BB->0x0095D3C4;
  0x006C97D8->0x006E8F70; 0x006C9631->0x007B79B0; 0x006CB7CF->0x006C9700;
  0x006CB836->0x006FA8B0) and the load-bearing byte pins (6A 10 @0x006C97B9;
  89 46 04 @0x006E8FA5; 01 48 04 @0x006E8FAF; 8B C6 @0x006E9014 and
  @0x006C9808; 01 5F 04 @0x006C67E7; BB 01 00 00 00 @0x006C67C9; 89 7E 68
  @0x006C67E2; 8B 78 04 @0x006C67BE; 89 46 6C @0x006C7008; slot stores
  @0x006C95A0/0x006C9651/0x006C9657) ALL MATCH; EXE identity E7785430... /
  8015872 B measured — persisted VERBATIM as PE_MASTER_REVIEW.md

OPEN_FINDINGS (PE-MASTER adjudication: NONE material to the load-bearing
  claims; recorded; no correction loop started — the contract ends science at
  material findings and none occurred):
  F-1 (P3) notation residue "8B F0?" in a PINS row @0x006CB811
    (physically 85 F6; the prior record is correct)
  F-2 (P2) checker OwnPE.va_to_off lacks a raw-vs-virtual boundary — ZERO
    effect on this run (all 80 checks on raw-backed VAs; QC independently
    confirmed MC6's specificity conclusion); input for the NEXT checker
    generation, not a correction of this package
  F-3 (P3) rel32 notation residue "-0x2701+...=0x26FF" @0x006C6FFC
    (physically +0x26FF; target correct)
  Disclosed (NOT a finding against the result): one executor transcription
  error (E8 35... -> E8 75 F0 02 00 @0x006CB836) CAUGHT by the production
  gate itself on clean-pass attempt 1 and corrected before any evidence was
  accepted.

PACKAGE_CENSUS = 28 physical package files (26 executor+QC-phase files +
  PE_MASTER_REVIEW.md + MANIFEST_SHA256.csv)
MANIFEST_ROWS = 28 (27 package rows — every physical file under
  OUTPUT_REPO_PATH except the manifest itself — + 1 AUDIT_ENTRYPOINT.md row;
  repo-relative paths)
MANIFEST_BIJECTION = PASS (missing=0, extra=0, duplicate=0, size mismatch=0,
  SHA256 mismatch=0; generator self-check + the persistence phase's
  independent full re-hash of every row)
CHANGED_PATH_CENSUS = exactly 29 paths, all inside the WRITE_ALLOWLIST
  (28 package files + AUDIT_ENTRYPOINT.md); staged census clean — zero
  foreign, zero historical-package files, zero .pyc/__pycache__; the
  pre-existing foreign untracked paths untouched (6: 5x PE_935_* packages +
  experiments/)
SOURCE_PACKAGES_UNCHANGED = YES (the five READ_ONLY historical packages
  unchanged vs BASE blobs: git diff 97823c6 empty per package incl.
  PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z; the QC
  re-measured all load-bearing prior-canon bytes from the physical EXE
  instead of a full 263-file re-hash — all MATCH; the executor's census
  263/263 BASE-blob-identical at preflight and at phase close)

SCIENCE_CEILINGS (NOT raised by this run): deeper origin of P =
  NOT_ESTABLISHED_WITHIN_BOUND; S identity and O identity = NOT_ADJUDICATED;
  R class name = UNKNOWN (no vptr); P/T class names = UNKNOWN;
  release-on-destroy = NOT_CHECKED; T downstream role = NOT_ADJUDICATED;
  transform owner / coordinate frame = NOT_ADJUDICATED_BY_THIS_RUN (prior
  preserved).
STANDING_SCIENCE_PRESERVED_VERBATIM (contract §7): CHILD_RESOURCE_PROVENANCE
  = STRONGLY_SUPPORTED_MODEL_DERIVED; MODEL_ROOT_RELATION = UNKNOWN;
  CHILD_VISUAL_ROLE = UNRESOLVED; CHILD_TO_JOIN_IDENTITY =
  STRONGLY_SUPPORTED; EXACT_PARENT = CONFIRMED_EXACT_SCENEFEEDER_PLUS_30;
  PARENT_SCOPE = EXAMINED_ACLD_PLUS_18_SF_INSTANCE; JOIN_OPERATION =
  STRONGLY_SUPPORTED; CAND4_CHILD_ROOT_CLOSURE =
  NOT_ESTABLISHED_WITHIN_BOUND; WORLD_INSTANCE = NOT_ESTABLISHED;
  WORLD_XYZ_RECOVERED = NO; STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED;
  HISTORICAL_INSTANCE_DATA_RECOVERED = NO. No model root/main visual/world
  instance promotion. REAL_SCIENCE_AUTO_QUALIFICATION = DISABLED; the
  oracle does not raise PCG status.

NEW_DESKTOP_POST_AUDIT = NOT_PERFORMED (the fresh internal QC of this run is
  NOT the future Desktop post-audit of the newly published SHA; the
  published exact SHA is returned for that audit)
CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
```

## Notes

- The two primary results (RETURN_VALUE_ORIGIN; PLUS4_WRITER_AND_SOURCE) are
  THIS run's measured answers to the contract §1 question; they are reported
  without auto-promoting any standing status (the new evidence concerns
  exactly the prior GAP-1 ([instance+4] identity) and the prior lineage H-2
  relation, reported as run-local results for the parent's adjudication).
- Publication is NOT acceptance: the PE-MASTER verdict is advisory
  (ADVISORY_PRE_QUALIFICATION; Q1 absent, PROVISIONAL_UNTIL_QUALIFIED;
  CANONICAL_GATE_EFFECT=NONE); the independent Desktop post-audit of the NEW
  published SHA remains pending.
- Persistence: exactly ONE normal commit at BASE
  97823c6180b0a35a8f5c43e45c29076d48208bee (no amend, no rebase, no force
  push, no history rewrite), normal fast-forward push;
  MANIFEST_SHA256.csv generated LAST; live remote verify after the push;
  any write after the manifest requires regeneration + full re-verification.
