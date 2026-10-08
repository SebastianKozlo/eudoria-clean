# SOURCE_STATE — PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008

RUN_ID: PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008
RUN_CLASS: BOUNDED_STATIC_RE_SCIENCE · PRIMARY_TARGET: PCG_9_3_5 (Entropia
Universe 9.3.5 client image) · Executor: pe-reconstruction (bounded worker
phase under direct PE-MASTER dispatch; NO_NESTED_TASKS). STATIC-ONLY — the
client never ran; no runtime, no network science, no payloads/VFS/BNT/NIF
opened. The QC phase (QC_REPORT.md etc.), AUDIT_ENTRYPOINT.md,
MANIFEST_SHA256.csv, commit/push and publication belong to LATER parent
phases — this executor does NOT touch AUDIT_ENTRYPOINT.md and does NOT
stage/commit/push (per the delegation; the contract's §8 persistence phase is
the parent's).

## 1. Base state (measured, fail-closed; full query log in INPUT_IDENTITIES.md §1)

- LOCAL_HEAD = origin/master = live remote master = 97823c6180b0a35a8f5c43e45c29076d48208bee
  (= EXPECTED_BASE_SHA; the first live ls-remote attempt failed transiently,
  the live retry at 2026-10-08T11:04:49Z answered the pinned SHA — recorded
  honestly in INPUT_IDENTITIES.md §1).
- `git status --porcelain=v1` at preflight: ZERO tracked changes; foreign
  untracked only (§2).
- OUTPUT_REPO_PATH did not exist at preflight; created only after preflight
  PASS.

## 2. Foreign untracked census (recorded, NEVER touched/staged/cleaned)

    ?? docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/
    ?? docs/audits/PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003/
    ?? docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/
    ?? docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/
    ?? docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/
    ?? experiments/

After this executor phase the census additionally shows this run's own
OUTPUT_REPO_PATH (untracked, unstaged — publication is the parent's phase).

## 3. READ_ONLY source packages — untouched

The five historical packages of contract §2 item 4 (+ the PLACEMENT_RECORD_
BRIDGE package) are byte-identical to their BASE blobs: 263/263 files
(`git hash-object` physical == `git ls-tree BASE` blob; measured at preflight;
re-verified at end of phase — see §7). Their standing records (SUPERSSESSION
SN-1..SN-3, S-1..S-9; preserved-science lists; the corrected lineage status)
are honored: no historical status is changed by analogy anywhere in this run.
Prior records carried over into this run's analysis are cited per claim with
the exact prior record, scope and identity (contract §3).

## 4. Write scope (this executor phase)

All writes confined to OUTPUT_REPO_PATH/** (the delegated allowlist;
AUDIT_ENTRYPOINT.md is NOT touched by this phase). Package contents: the
science records (01_RAW/, RETURN_VALUE_TRACE.csv, PLUS4_PROVENANCE.csv,
POINTER_LINEAGE.csv, FUNCTION_BODY_ACCOUNTING.csv, EDGE_ACCOUNTING_LEDGER.csv,
CLAIM_MATRIX.csv), CONTROL_RESULTS.json (checker + CTRL_A..G), 03_SCRIPTS/,
00_CONTROL_INTERNAL_QC/ (QC-phase inputs only — the fresh QC worker writes
QC_REPORT.md), FINAL_REPORT.md, HANDOFF.md, INPUT_IDENTITIES.md,
PREREGISTRATION.md, SOURCE_STATE.md. QC_REPORT.md, PE_MASTER_REVIEW.md and
MANIFEST_SHA256.csv are LEAVE-FOR-LATER-PHASES (NOT created by this executor).

## 5. Standing science carried into this run (preserved verbatim; no status changes by analogy)

From the prior canon (CHILD_ROOT_PROVENANCE + POST_AUDIT_CORRECTION +
NC1/NC2/NC3 corrections + the pinned Desktop post-audit + the engine
research report):

```text
CHILD_RESOURCE_PROVENANCE = STRONGLY_SUPPORTED_MODEL_DERIVED
MODEL_ROOT_RELATION = UNKNOWN
CHILD_VISUAL_ROLE = UNRESOLVED
CHILD_TO_JOIN_IDENTITY = STRONGLY_SUPPORTED
EXACT_PARENT = CONFIRMED_EXACT_SCENEFEEDER_PLUS_30
PARENT_SCOPE = EXAMINED_ACLD_PLUS_18_SF_INSTANCE
JOIN_OPERATION = STRONGLY_SUPPORTED
CAND4_CHILD_ROOT_CLOSURE = NOT_ESTABLISHED_WITHIN_BOUND
WORLD_INSTANCE = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED
HISTORICAL_INSTANCE_DATA_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
WRAPPER_DEPTH = UNRESOLVED
H-2 RELATION_TYPE = UNRESOLVED  (the exact question THIS run examines)
HISTORICAL_LINEAGE_BUDGET_CHARGE = 2/3 (historical run; this run has its own fresh budget)
MINIMUM_NEW_ANALYZED_EDGE_COUNT >= 32 (EXACT UNRESOLVED) — historical, the source run
MINIMUM_NEW_FUNCTION_BODIES_OPENED >= 7 (EXACT UNRESOLVED) — historical, the source run
ORIGINAL_SCOPE/BUDGET_COMPLIANCE = FAIL (historical, the source run; never becomes PASS)
RETROACTIVE_PRIOR_AUTHORIZATION = NO
NC1 = CLOSED_FOR_AUDITED_STATE; NC2/NC3 = CORRECTED_AND_REVALIDATED_IN_TEST_SCOPE
GENERAL_X86_DECODER_CORRECTNESS = NOT_ESTABLISHED
```

The CAND-4 caller chain (prior canon, re-pinned within recorded scope; this
run re-verifies the load-bearing bytes through its own pinned reads):

```text
caller FUN_006C6F60, callsite 0x006C6FFC → FUN_006C9700 (E8 FF 26 00 00;
  cdecl 4 args: arg1=A, arg2=&local2, arg3=&local1, arg4=0; ECX = [manager+0x70]
  template holder at the getter-A call; +0x70 passed validity FUN_0072FCE0)
return R → store [manager+0x6C] @0x006C7008 (89 46 6C)
installer FUN_006C6780: [manager+0x6C] → R (mov eax,[esi+0x6C] @0x006C67B3);
  [R+4] → T (mov edi,[eax+4] @0x006C67BE, 8B 78 04);
  store T → [manager+0x68] @0x006C67E2 (89 7E 68);
  increment [T+4] @0x006C67E7 (01 5F 04 = ADD [EDI+4], EBX; EBX=1 established
  by BB 01 00 00 00 @0x006C67C9 — NOT an INC opcode)
```

The historical other-caller record (PLACEMENT_RECORD_BRIDGE E5/C9 L20 window;
READ_ONLY; every interpretation carried into this run cites this record):

```text
FUN_006CB6F0: CALL FUN_006C9700 @0x006CB7CF (E8 2C DF FF FF) → saved ESI
  (mov esi,eax @0x006CB7DB); NULL check @0x006CB811; new(0xC) @0x006CB819/
  0x006CB81B → W; ctor FUN_006FA8B0(W, saved R) @0x006CB836 (E8 35 F0 02 00);
  → named-instance builder FUN_006CB020 …
RTTI: vtable 0x00A864B8 → .?AVArkModelResourceInstanceRef@@ concerns the
  KNOWN W; W+4=count / W+8=item is the INHERITED prior-canon field map,
  NOT a new finding for R. No standing proof of R==W or of their class
  equality/difference — roles from two recorded callers, not one execution.
```

Engine guardrails (contract §3) apply verbatim: GetObjectByName self/NULL;
GetExtraData no child traversal; ArkTexture/ArkAnimation names do not identify
callees; SDK 1.1.2/1.2/2.6 differ — no ABI/offset/vtable-slot/name transfer;
resource clone / cached object / fallback root / world instance are separate
roles; loaded root may differ from model wrapper and transform/base node;
runtime field offset is not automatically a serialized NIF field offset.

## 6. What this run examines (bounded scope, contract §1/§5)

ONE question: on paths consistent with the recorded CAND-4 caller — where does
the return value R of FUN_006C9700 come from, and who assigns the value later
read as [R+4]? Deliverables RETURN_VALUE_ORIGIN and PLUS4_WRITER_AND_SOURCE.
Exact type/base of R if physically establishable in bound. T described ONLY
from evidence encountered in the same creation/return chain; no separate
downstream trace of T; no main-visual/transform/world-instance/XYZ search;
FUN_006C8BB0, FUN_007B6C30, FUN_007BF900/FUN_007BF630 and join implementation
NOT opened.

## 7. End-of-phase census

(heads-up: to be re-measured at the end of this executor phase — the actual
values are recorded in §8 below, filled at phase close.)

## 8. End-of-phase state (filled at phase close — actual measured, 2026-10-08T11:27Z)

- HEAD at phase close: 97823c6180b0a35a8f5c43e45c29076d48208bee (UNCHANGED; this
  phase created NO commit and staged NOTHING); origin/master unchanged; zero
  tracked changes repo-wide (all of this run's writes are inside its own untracked
  OUTPUT_REPO_PATH).
- Historical packages: re-verified 263/263 BASE-blob identity at phase close
  (zero mismatches). AUDIT_ENTRYPOINT.md UNCHANGED (no tracked change vs BASE).
- Foreign untracked: the 6 pre-existing paths UNTOUCHED; the census additionally
  shows exactly ONE new untracked path — this run's OUTPUT_REPO_PATH.
- No __pycache__/.pyc under OUTPUT_REPO_PATH (precise re-scan: 0 dirs, 0 files;
  python -B + sys.dont_write_bytecode everywhere).
- Package census at phase close: 22 physical files (INPUT_IDENTITIES.md,
  PREREGISTRATION.md, SOURCE_STATE.md, FINAL_REPORT.md, HANDOFF.md,
  RETURN_VALUE_TRACE.csv, PLUS4_PROVENANCE.csv, POINTER_LINEAGE.csv,
  FUNCTION_BODY_ACCOUNTING.csv, EDGE_ACCOUNTING_LEDGER.csv, CLAIM_MATRIX.csv,
  CONTROL_RESULTS.json, 7x 01_RAW/, 2x 03_SCRIPTS/, 1x 00_CONTROL_INTERNAL_QC/
  QC_PHASE_INPUTS.md). NOT created (left for later phases, per the delegation):
  QC_REPORT.md (the QC worker), PE_MASTER_REVIEW.md (the parent),
  MANIFEST_SHA256.csv (the parent phase — MANIFEST LAST), the AUDIT_ENTRYPOINT.md
  row (the parent phase). No fictional/empty evidence was created.
- No EXE modification (the mechanical-control corruptions were IN-MEMORY copies;
  the physical EXE re-verified pinned before the checker runs); no runtime; no
  payloads; no network science (the only network use: the required live git
  verification).
