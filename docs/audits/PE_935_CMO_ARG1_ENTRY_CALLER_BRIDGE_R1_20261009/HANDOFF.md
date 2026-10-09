# HANDOFF — PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009

Contract §10 terminal handoff, populated from REAL measurements only. If a
check had not passed, its actual result would be reported here instead of the
expected value.

```text
RUN_ID = PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009
BASE_SHA = ce75b7b3ee0b7b87c1f0a03bc79167169aed71a0
RESULTING_SHA = recorded at the terminal handoff per contract §9 — not embedded in this commit's files
REMOTE_SHA = recorded at the terminal handoff per contract §9 — not embedded in this commit's files
PERSISTENCE_STATUS = PENDING_FINAL_GATES at this file's finalization (this HANDOFF is itself
  inside the persistence scope; the actual commit/push result is recorded at the terminal
  handoff per contract §9: pass -> PUBLISHED with the exact SHA; any gate/push failure ->
  PERSISTENCE_BLOCKED with the honest local/remote state, no replacement commit, no false
  remote success, no guard weakening)

EXE_SIZE = 8015872
EXE_SHA256 = E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
WINDOW_A_SIZE = 66
WINDOW_A_SHA256 = F8735567340CD3BE2F6B64B4BBC2BE292487E97B6184758CA408E6FF1CE78E85
WINDOW_A_DECODE_STATUS = PASS (23 instructions, exact cover of [0x00528E50,0x00528E92))
WINDOW_B_SIZE = 52
WINDOW_B_SHA256 = B59E16DC116F4CE0438A1E92BC6B2CBC33FAB0B19FABC24CB3A29C911C1EFB6A
WINDOW_B_DECODE_STATUS = PASS (16 instructions, exact cover of [0x004C4792,0x004C47C6))

ENTRY_ESP_E = SYMBOLIC (E; derived S = E-0x38)
WINDOW_A_PIVOT_S = S = E-0x38 (ESP at 0x00528E76)
SOURCE_SLOT_RELATIVE_TO_E = [E+4] (≡ [S+0x3C])
ENTRY_SLOT_VALUE_PRESERVATION = ESTABLISHED (write census: 8 stack writes + 1 FS:[0] TIB write,
  zero writes at [E+4] before the load; AS4 stated)
ENTRY_ARGUMENT_IDENTITY_STATUS = CONFIRMED_STATIC_CONDITIONAL

CALLER_REFERENCE_ESP_T = T (ESP at 0x004C47AF; = window-start ESP under AS3)
OPAQUE_RETURN_CONDITION = AS3 (normal ABI-compatible return of 0x95D3C4; body unopened)
TARGET_PATH_CONDITION = EAX≠0 after TEST EAX,EAX (JE taken on EAX==0 exits the window at
  0x004C47C8; flags survive TEST→JE — empty intervening-writer census)
CALLER_LEA_VA = 0x004C47BA
OPERAND = [ESP+0x14]
RESULT_KIND = ADDRESS (opcode 8D; computed, not a read)
RESULT_EXPRESSION = ADDRESS(T+8)
UPSTREAM_CALLSITE = 0x004C47C1
CALL_TARGET = 0x00528E50 (rel32 E8 8A 46 06 00 recomputed == objdump)
ARG1_SLOT = [T-0x10] (≡ [E+4], E = T-0x14)
ARG1_VALUE = ADDRESS(T+8) — the ADDRESS value, NOT MEM(T+8)
RECEIVER_SOURCE = the opaque call's EAX return value (MOV ECX,EAX @0x004C47BF)

CROSS_CALL_IDENTITY_STATUS = POINTER_VALUE_IDENTITY_ESTABLISHED_CONDITIONAL (the SAME pointer
  value ADDRESS(T+8) delivered as arg1 of FUN_00528E50 at CALL 0x004C47C1 and as arg1 of
  FUN_0085B1B0 at CALL 0x00528E8D; AS1–AS5 + the EAX≠0 branch; zero intervening writes to
  the joined slot — the return-address push lands at [T-0x14])
FIRST_UNRESOLVED_DEPENDENCY = the pointee contents/producer at [T+8]
  (POINTEE_CONTENTS_PROVENANCE = UNRESOLVED_UPSTREAM)

SCIENCE_OUTCOME = ENTRY_ARG1_AND_SINGLE_CALLER_BRIDGE_ESTABLISHED (CONDITIONAL)
ORIGINAL_BYTE_FALSIFIERS = none triggered (no unmodified-byte contradiction of any
  preregistered hypothesis; synthetic-mutant rejections = CONTROL_PASS only — correctly
  rejecting a mutated hypothesis is not falsification of the original client)

CONTROL_CASE_COUNT = 12
PRODUCTION_OUTCOMES = 12/12 CONTROL_PASS/QUALIFIED (A_CLEAN; B_CLEAN_NONNULL; B_CLEAN_NULL
  [JE taken, no fabricated delivery]; M1 S=E-0x34/source [E+8]; M2 source [E];
  M3 ADDRESS(T+0xC); M4 arg1 MEM(T+0x4C); M5 arg1+slot UNCHANGED while arg3/arg4 swap
  reported; M6 unconditional exit; M7 arg1 UNCHANGED, receiver ESI/unknown;
  M8 actual target 0x00528E51 recomputed -> bridge_valid=False [real target predicate, not a
  hash failure]; M9 arg1 MEM(T+8) from opcode 0x8B)
QC_OUTCOMES = 12/12 CONTROL_PASS/QUALIFIED (24/24 total, cases ≠ outcomes — 12 cases x
  production + fresh-QC analysis, not 24 independent scientific discoveries)
ARTIFACT_CONTROLS = baseline 21/21 PASS x 2 gates; AC1 (ADDRESS→MEM) REJECTED x 2 gates;
  AC2 ([E+4]→[E+8]) REJECTED x 2 gates -> ARTIFACT_CONSISTENCY_PASS

QC_ORIGIN = pe-master-auditor fresh-context internal QC (internal to PE-MASTER; not a
  Desktop post-audit; same-objdump independence honestly bounded — the same GNU objdump is
  NOT two disassemblers; independence = own bytes/mapping/invocation/symbolic implementation)
QC_VERDICT = QC_PASS (56/56 field agreement on the load-bearing facts)
INTERNAL_ADVISORY_VERDICT = MASTER_ACCEPTED (PE-MASTER; advisory; ADVISORY_PRE_QUALIFICATION;
  CANONICAL_GATE_EFFECT = NONE)
OPEN_FINDINGS = F-QC-1/F-QC-2/F-QC-3 (P3, non-blocking) + the disclosed process items
  (the prior-session executor crash/continuation with mechanical proof; the 7 executor
  pipeline repairs; the 3 QC tooling repairs; the PE-MASTER .text offset-shortcut tooling
  error — disclosed, no package evidence affected)
P3_BACKLOG = DOC-1..DOC-4 (prior) preserved
RETRACTIONS_SUPERSESSIONS = NONE new (standing preserved verbatim; the prior
  ARG1_DIRECT_SOURCE result preserved, not reinterpreted; no J3 restoration; no superseded
  conclusion reopened; this run supersedes no prior package)

ANALYZED_WINDOWS = 2/2
UNIQUE_CODE_BYTES = 118/118 (A 66 + B 52; disjoint; exactly the authorized max)
CALLSITE_CENSUS = 2 target (0x004C47C1→0x00528E50, 0x00528E8D→0x0085B1B0) + 1 incidental
  opaque (0x004C4797→0x95D3C4, body unopened)
SCOPE_COMPLIANCE = WITHIN (0 complete bodies; 0 callee bodies; 0 upstream beyond window B;
  0 other-callsite/xref census; 0 field-semantic promotions; 0 runtime/network/model/
  VFS-BNT-NIF RE; 0 Gamebryo/OpenMW research)

MANIFEST_ROWS = 35 (34 package rows self-excluded + 1 entrypoint row; measured)
PHYSICAL_PACKAGE_FILES = 35 (30 frozen executor/QC [executor 27 + QC 3] +
  PE_MASTER_REVIEW.md + FINAL_REPORT.md + EVIDENCE_INDEX.md + HANDOFF.md + MANIFEST_SHA256.csv)
MANIFEST_BIJECTION = PASS (measured: missing=0, extra=0, duplicate=0, size=0, SHA=0)
CHANGED_PATH_CENSUS = 36 (35 package files + AUDIT_ENTRYPOINT.md; measured at staging)
HISTORICAL_PACKAGES_UNCHANGED = YES

FIELD_SEMANTICS = UNVERIFIED
POINTEE_CONTENTS_PROVENANCE = UNRESOLVED_UPSTREAM
WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED
HISTORICAL_PLACEMENT = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
INDEPENDENT_DESKTOP_POST_AUDIT = NOT_PERFORMED
CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
```

## Value provenance (each terminal value -> its evidence)

- `EXE_*`: contract pin == physical hash re-verified 3x independently (executor retry
  before AND after all work — INPUT_IDENTITIES.md I4; fresh QC — QC_REPORT.md D1;
  PE-MASTER — PE_MASTER_REVIEW.md preflight); unchanged; never committed (local-only).
- `WINDOW_A_*` / `WINDOW_B_*`: physical extraction at the pinned raw offsets (1216080 /
  804754), SHA256s == contract pins (WINDOW_IDENTITIES.json; QC's own extraction —
  QC_REPORT.md D1; PE-MASTER's own re-pin); decode censuses (23 and 16 instructions, exact
  covers, last CALLs ending exactly at the window ends) from the persisted raw objdump
  outputs (01_RAW/WINDOW_{A,B}_OBJDUMP.txt + _RETRY.txt) — the only decoder is GNU objdump
  2.44 (rc 0 recorded).
- `ENTRY_ESP_E` / `WINDOW_A_PIVOT_S` / `SOURCE_SLOT_RELATIVE_TO_E` /
  `ENTRY_SLOT_VALUE_PRESERVATION` / `ENTRY_ARGUMENT_IDENTITY_STATUS`: Phase A derivation —
  ENTRY_FRAME_LEDGER.csv (23 rows, instruction-by-instruction) + BRIDGE_PROVENANCE.json
  phase_a (claims A-1..A-8), independently re-derived by the QC (QC_REPORT.md D2,
  26/26 field agreement) and manually verified by PE-MASTER (the E→S chain and the three
  separate proofs: slot-address equivalence [S+0x3C]==[E+4]; the 8+1 write census with zero
  writes at [E+4]; EDI preservation to PUSH @0x00528E8A). Controls M1/M2 prove the
  predicates discriminate (S and the source slot flip exactly under the frame/slot
  mutations); A_CLEAN = CONTROL_PASS through the REAL analysis.
- `CALLER_REFERENCE_ESP_T` / `OPAQUE_RETURN_CONDITION` / `TARGET_PATH_CONDITION` /
  `CALLER_LEA_VA` / `OPERAND` / `RESULT_KIND` / `RESULT_EXPRESSION` /
  `RECEIVER_SOURCE`: Phase B derivation — CALLER_STACK_LEDGER.csv (NULL + NONNULL paths) +
  BRIDGE_PROVENANCE.json phase_b (claims B-1..B-5), independently re-derived by the QC
  (QC_REPORT.md D3) and byte-pinned by PE-MASTER (LEA 8D 4C 24 14 @0x004C47BA; MOV ECX,EAX
  8B C8 @0x004C47BF; TEST 85 C0; JE 74 19; PUSH ECX 51 — ALL MATCH). KIND = ADDRESS comes
  from the opcode byte 0x8D (LEA computes; M9 proves the 8D→8B kind flip is detected);
  flags survive TEST→JE (empty intervening-writer census; M6 proves the JE→JMP exit flip
  is detected); the EAX==0 null branch shows no fabricated delivery (B_CLEAN_NULL).
- `UPSTREAM_CALLSITE` / `CALL_TARGET` / `ARG1_SLOT` / `ARG1_VALUE`: the nonnull-branch
  arithmetic measured in BRIDGE_PROVENANCE.json phase_b (E = T-0x14; [E+4] = [T-0x10] :=
  ADDRESS(T+8) by PUSH ECX @0x004C47BE) — rel32 recompute E8 8A 46 06 00 → 0x00528E50 ==
  objdump; QC agreement; PE-MASTER hand verification (T-0xC+0x14 = T+8; T-0x10-4 = T-0x14;
  [E+4] = [T-0x10]) — CONSISTENT. M8 proves the checker computes the ACTUAL target from
  bytes (0x00528E51 → bridge_valid=False, not a hash side-failure).
- `CROSS_CALL_IDENTITY_STATUS` / `FIRST_UNRESOLVED_DEPENDENCY`: BRIDGE_PROVENANCE.json
  bridge (claim BR-1: join E=T-0x14; slot-address identity derived both ways; combined
  write census in one coordinate system — zero intervening writes to [T-0x10]; the
  return-address push lands at [T-0x14]); QC's own join (QC_REPORT.md D4) — ALL AGREE;
  PE-MASTER arithmetic check CONSISTENT. Conditions AS1–AS5 + EAX≠0 stated; NOTHING about
  [T+8] contents/type/lifetime/frame-layout/history claimed (BR-2 = NOT_PERFORMED scope
  fence); the pointee/producer is deliberately untraced.
- `SCIENCE_OUTCOME`: FINAL_REPORT.md §14 — one of the contract §8 outcome classes,
  CONDITIONAL as stated; the first upstream delivery boundary of the audited callsite
  qualified; pointee and earlier producer remain untraced.
- `ORIGINAL_BYTE_FALSIFIERS`: no falsifier fired on the unmodified original windows
  (wrong frame delta, slot overwrite/alias, wrong CALL target, LEA/MOV mismatch,
  unreachable delivery — none contradicted the hypotheses); the mutants M1–M9 that DO
  flip these facts were correctly discriminated (CONTROL_PASS), which is control evidence,
  not original falsification.
- `CONTROL_CASE_COUNT` / `PRODUCTION_OUTCOMES` / `QC_OUTCOMES`: CLAIM_MATRIX.csv (12
  PRODUCTION rows 12/12 CONTROL_PASS with structured facts) + CONTROL_RESULTS.json
  (per-case checks) + QC_RESULTS.json / QC_REPORT.md D5 (the QC's own 12/12 through its
  own implementation; production verified field-by-field — 24/24 total; cases ≠ outcomes).
- `ARTIFACT_CONTROLS`: ARTIFACT_CONTROL_RESULTS.json (executor gate: baseline 21/21 PASS,
  AC1/AC2 REJECTED) + QC_RESULTS.json D6 (the QC's own gate: baseline 21/21, AC1/AC2
  REJECTED) → ARTIFACT_CONSISTENCY_PASS; bypasses confined to isolated synthetic copies.
- `QC_ORIGIN` / `QC_VERDICT`: QC_REPORT.md (fresh-context internal QC inside PE-MASTER's
  delegation chain; NOT an independent Desktop post-audit; NOT executor self-review; the
  same-objdump limitation stated honestly; 56/56 field agreement; the crash/continuation
  adjudicated with mechanical proof — the 19151-byte prefix hash F36DE40A…; the 7 executor
  pipeline repairs adjudicated HONEST).
- `INTERNAL_ADVISORY_VERDICT`: PE_MASTER_REVIEW.md (persisted verbatim; advisory
  MASTER_AUDIT; ADVISORY_PRE_QUALIFICATION — PE-MASTER remains
  PROVISIONAL_UNTIL_QUALIFIED; own 9 instruction byte pins + the bridge arithmetic ALL
  MATCH; the disclosed .text offset-shortcut tooling error re-run clean).
- `OPEN_FINDINGS` / `P3_BACKLOG`: F-QC-1 (P3 — the 7 repairs disclosed but not persisted
  as package documents; immaterial), F-QC-2 (P3 — the CALLER_STACK_LEDGER.csv JE-row PATH
  FORK annotation duplicate; cosmetic), F-QC-3 (P3 — the QC's own 3 tooling repairs;
  disclosed, zero executor artifacts touched) — all non-blocking; a correction needs a
  new human decision. DOC-1..DOC-4 (the prior P3 documentary backlog) preserved.
- `RETRACTIONS_SUPERSESSIONS`: SUPERSESSION_AND_STANDING.md — NONE new; the prior
  ARG1_DIRECT_SOURCE result preserved verbatim and re-derived consistently (not
  reinterpreted, not superseded); CMO_C1 / CORE_RECEIVER_VALUE_CHAIN / J3 lines carried
  verbatim; no ACLD↔CMO identity transfer; no J3 restoration.
- `ANALYZED_WINDOWS` / `UNIQUE_CODE_BYTES` / `CALLSITE_CENSUS` / `SCOPE_COMPLIANCE`:
  INPUT_IDENTITIES.md I9 + the QC's raw-VA census (every decoded VA inside A/B; 0 outside)
  + WINDOW_IDENTITIES.json decode censuses — 2/2 windows, 118/118 unique bytes, 2
  target + 1 incidental opaque callsite, all other budgets 0.
- `MANIFEST_ROWS` / `PHYSICAL_PACKAGE_FILES` / `MANIFEST_BIJECTION` /
  `CHANGED_PATH_CENSUS` / `HISTORICAL_PACKAGES_UNCHANGED`: MANIFEST_SHA256.csv generated
  LAST over the final persistence scope (every physical file under this package except
  the manifest itself + the updated AUDIT_ENTRYPOINT.md; repo-relative; self-exclusion
  documented; LF, UTF-8 no BOM, lowercase hex); the measured census — 35 physical package
  files → 34 package rows + 1 entrypoint row = 35 rows; bijection re-verified by the
  persistence phase's independent full re-hash (zero missing/extra/duplicate/size/SHA
  mismatches); staged changed-path census 36; `git diff ce75b7b -- <historical packages>`
  empty (all prior packages byte-identical to BASE); foreign untracked paths
  (5x PE_935_* packages + experiments/) untouched and not staged.

## Persistence facts (this phase)

- Persistence scope: OUTPUT_ROOT
  (`docs/audits/PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009/`) + ONE new
  newest-first LATEST RUNS row in `AUDIT_ENTRYPOINT.md` (existing 5-column format; no
  other row modified).
- Allowlist gates: git status/diff limited to OUTPUT_ROOT/** + AUDIT_ENTRYPOINT.md; no
  proprietary payload (no EXE bytes, no .bin window extracts — the 01_RAW artifacts are
  disassembly text of the two bounded windows only); no residue (`python -B` honored by
  the executor/QC; no __pycache__/.pyc/temp at persistence); executor + QC evidence
  FROZEN (the 30 files untouched by this phase).
- LOCAL_HEAD == origin/master == actual remote master == ce75b7b… re-verified live
  (ls-remote) immediately before commit; ONE normal commit (RUN_ID-prefixed long
  message, repo style); normal fast-forward push; no amend, no rebase, no force, no
  history rewrite; never `git add -A`; explicit path-limited staging.
- Per contract §9: a push/remote-verification failure would be a persistence failure,
  not a scientific PASS — the actual local/remote state would be preserved and the run
  would HARD STOP without a follow-up run and without guard weakening
  (PUSH_NOT_VERIFIED recorded with the local commit SHA preserved; no replacement or
  amended commit; no false remote success).
- No self-referential SHA: RESULTING_SHA/REMOTE_SHA are recorded at the terminal handoff,
  not embedded in any file of this commit.

**A successful pointer delivery does NOT qualify the contents of the stack area
and grants NO historical XYZ claim. WORKS != UNDERSTOOD. NO AUTOMATIC UPSTREAM
CONTINUATION. HARD_STOP = YES.**
