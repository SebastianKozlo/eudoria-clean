# PE_MASTER_REVIEW — PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009

REVIEW_TYPE = PE-MASTER MASTER_AUDIT (internal advisory; NOT an independent Desktop post-audit; NOT executor/QC self-review)
AUTHOR = PE-MASTER
AUDITED_RUN = PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009
AUDITED_RANGE = uncommitted working tree at BASE ce75b7b3ee0b7b87c1f0a03bc79167169aed71a0 (BOUNDED_STATIC_ARGUMENT_PROVENANCE micro-run; commit pending at persistence)
CONTRACT = C:\Users\User\Documents\ChatGPT\PE\PE_CMO_ENTRY_CALLER_BRIDGE_PROMPT_REVIEW_20261009\OPENCODE_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_REVISED_20261009.md — 23187 B, SHA256 773C1310A2CB02B365068EE2D9C684A97765E4D416E30B415B8672D8CC09FF07 — verified MATCH
TARGET_IDENTITY = Entropia.exe 8015872 B / E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (unchanged; reads limited to the two authorized windows + mapping/identity)
VERDICT = MASTER_ACCEPTED (advisory; ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT = NONE)

## Preflight
LOCAL_HEAD == origin/master == actual remote master == ce75b7b3ee0b7b87c1f0a03bc79167169aed71a0 (live ls-remote). OUTPUT_ROOT created fresh. All 8 required repo inputs MATCH (bytes + Git blobs incl. the historical listing blobs 3648e1b8…/dc61d1b4…). EXE identity verified. Governance read; no conflict — the dispatch's bounded exception recorded.

## Finding (the one bounded question, answered within bound)
- PHASE A (ENTRY_FRAME_VALUE_IDENTITY = PASS): E = symbolic ESP at entry 0x00528E50; S = E-0x38 (ESP at 0x00528E76; SEH prologue + SUB 0x1C + register/cookie pushes, all derived from the physical A window); source-slot address [S+0x3C] == entry arg1 slot [E+4]; write census: 8 stack writes + 1 FS:[0] TIB write, ZERO at [E+4] (AS4 stated); EDI preserved to PUSH @0x00528E8A; delivery at CALL 0x00528E8D: ESP_before = S-0xC, callee entry = S-0x10, arg1 slot [S-0xC], target 0x0085B1B0, receiver via ESI separate channel — CONFIRMED (conditional static; straight-line examined path only).
- PHASE B (CALLER_PATH_AND_VALUE = PASS, performed only after clean A): T = ESP at 0x004C47AF (window-start ESP under AS3); opaque call 0x004C4797→0x95D3C4 treated opaquely (AS3 normal ABI-compatible return; body never opened); flags survive TEST→JE (empty intervening-writer census); JE target outside B not opened; on the qualified EAX≠0 branch: LEA ECX,[ESP+0x14] = ADDRESS(T+8) (opcode 8D, kind ADDRESS — computed, not a read); PUSH ECX → [T-0x10] := ADDRESS(T+8); receiver = opaque EAX return; CALL 0x004C47C1 → 0x00528E50; E = T-0x14; entry arg1 slot [E+4] = [T-0x10] containing ADDRESS(T+8) — CONFIRMED. Null branch: JE taken, no delivery.
- BRIDGE (CROSS_CALL_IDENTITY = POINTER_VALUE_IDENTITY_ESTABLISHED_CONDITIONAL): join E=T-0x14; slot-address identity [E+4] ≡ [T-0x10] derived both ways; combined write census zero intervening writes to that slot (the return-address push lands at [T-0x14]); the SAME pointer value ADDRESS(T+8) is delivered as arg1 of FUN_00528E50 at CALL 0x004C47C1 and as arg1 of FUN_0085B1B0 at CALL 0x00528E8D — CONFIRMED (CONDITIONAL: AS1/AS2/AS3/AS4/AS5 + EAX≠0 branch; nothing about [T+8] contents/type/lifetime/frame-layout/history claimed; POINTEE_CONTENTS_PROVENANCE = UNRESOLVED_UPSTREAM).
- SCIENCE_OUTCOME = ENTRY_ARG1_AND_SINGLE_CALLER_BRIDGE_ESTABLISHED (conditional; the first upstream delivery boundary of the audited callsite qualified; pointee and earlier producer remain untraced).

## Gate predicates
- 12 cases × production + fresh-QC = 24 matrix outcomes, ALL CONTROL_PASS/QUALIFIED (A_CLEAN; B_CLEAN_NONNULL; B_CLEAN_NULL no fabricated delivery; M1–M9 each discriminated on its contract §7 fields through the REAL analysis — M5/M7 retained unchanged arg1 facts while reporting the altered channel [non-blanket proof]; M8 reached the actual-target predicate 0x00528E51 → bridge_valid=False; M9 kind STACK_READ from opcode 0x8B).
- Artifact controls: baseline 21/21 PASS on both the executor gate and the QC's independently implemented gate; AC1 (ADDRESS→MEM) REJECTED by both; AC2 ([E+4]→[E+8]) REJECTED by both → ARTIFACT_CONSISTENCY_PASS. Hash/manifest bypass confined to isolated synthetic copies; no historical file mutated.
- Separate gates used: ORIGINAL_IDENTITY / DECODE_COVERAGE / ENTRY_FRAME_VALUE_IDENTITY / CALLER_PATH_AND_VALUE / CROSS_CALL_IDENTITY / REQUIRED_CONTROLS / ARTIFACT_CONSISTENCY. No generic SCIENCE_PASS.
- Fresh internal QC: QC_VERDICT = QC_PASS — 56/56 field agreement on the load-bearing facts; its own 12 matrix outcomes; artifact controls through its own gate; the crash/continuation adjudicated WITH MECHANICAL PROOF (the first 19151 B of PREREGISTRATION.md hash to F36DE40A… — pure P10 append, P1–P9 byte-identical pre-science); the executor's 7 pipeline repairs adjudicated HONEST (fail-closed; EXPECTED used only as the contract comparison table; defective intermediates preserved). Independence honestly bounded: the same GNU objdump is NOT two disassemblers; independence = own bytes/mapping/invocation/symbolic implementation.

## PE-MASTER counter-checks
Window A/B identities re-pinned physically (pre-preflight). 9 instruction byte pins from the physical EXE with a full PE-section parser: LEA 8D 4C 24 14 @0x004C47BA; MOV ECX,EAX 8B C8 @0x004C47BF; CALL E8 8A 46 06 00 @0x004C47C1 → target 0x00528E50; SUB 83 EC 1C @0x00528E5E; MOV EDI 8B 7C 24 3C @0x00528E84; TEST 85 C0 @0x004C47A3; JE 74 19 @0x004C47AD; PUSH ECX 51 @0x004C47BE — ALL MATCH. The bridge arithmetic verified by hand: E-0x38+0x3C = E+4; T-0xC+0x14 = T+8; T-0x10-4 = T-0x14; [E+4] = [T-0x10] — CONSISTENT. Operational disclosure: one PE-MASTER counter-check script initially used a wrong simplified .text offset shortcut producing apparent mismatches; re-run with the full section table — ALL MATCH (a PE-MASTER tooling error, disclosed; no package evidence affected).

## Findings
NONE material. Open (P3, non-blocking): F-QC-1 (the executor's 7 pipeline repairs disclosed to the parent but not persisted as package documents — immaterial, final artifacts re-derive exactly); F-QC-2 (CALLER_STACK_LEDGER.csv JE-row PATH-FORK annotation — cosmetic); F-QC-3 (the QC's own 3 tooling repairs — disclosed, zero executor artifacts touched). Disclosed process: the prior-session executor crash (empty handoff; 3 files verified-kept with mechanical proof; retry outputs added; model-origin change glm-5-2→glm-5-3 recorded).

## Standing preserved (verbatim)
S = ESP at 0x00528E76; ARG1_DIRECT_SOURCE = CONFIRMED_STATIC_CONDITIONAL (prior result preserved); CMO_C1 = CLOSED_FOR_AUDITED_STATE; CORE_RECEIVER_VALUE_CHAIN = PRESERVED_CONFIRMED_STATIC_CONDITIONAL; PHYSICAL_TRANSFORM_MEASUREMENTS = PRESERVED; NEW_TRANSFORM_TRACE = MEASURED_INCIDENTAL_OUTSIDE_PERMITTED_PROMOTION; SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN = NOT_QUALIFIED_BY_ORIGINAL_SCOPE; J3 preserved; no ACLD↔CMO identity transfer. POINTEE_CONTENTS_PROVENANCE = UNRESOLVED_UPSTREAM; FIELD_SEMANTICS = UNVERIFIED; WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED; HISTORICAL_PLACEMENT = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO. The bridge is a POINTER-VALUE delivery qualification — NOT a type, semantic, coordinate or placement claim.

## Coverage
Full read: contract (305 lines), executor/QC handoffs, window identities, both ledgers, BRIDGE_PROVENANCE.json, CONTROL_RESULTS/ARTIFACT_CONTROL_RESULTS (census-level with load-bearing fields verified). PE-MASTER physical counter-checks: window pins + 9 instruction pins + the bridge arithmetic — ALL MATCH. NOT_CHECKED: the unmodified pointee contents/producer at [T+8] (deliberately untraced; POINTEE UNRESOLVED_UPSTREAM), the EAX==0 out-of-window branch, the opaque callee body (never opened), the ESI-at-T producer, AS3/AS4 runtime realizability (assumptions; bridge CONDITIONAL), runtime (prohibited), cross-disassembler QC (same objdump — honestly bounded), the independent Desktop post-audit of the resulting SHA (NOT_PERFORMED, future).

SOURCE_DESKTOP_POST_AUDIT = N/A (this micro-run derives from committed prior evidence)
INDEPENDENT_DESKTOP_POST_AUDIT = NOT_PERFORMED
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
