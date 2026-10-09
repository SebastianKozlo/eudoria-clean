# PE_MASTER_REVIEW — PE_935_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009

REVIEW_TYPE = PE-MASTER MASTER_AUDIT (internal advisory; NOT an independent Desktop post-audit; NOT executor/QC self-review)
AUTHOR = PE-MASTER
AUDITED_RUN = PE_935_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009
AUDITED_RANGE = uncommitted working tree at BASE e687eb1360cc0f6f4c4d7c8db7587bb5d357bc6b (BOUNDED_STATIC_ARGUMENT_PROVENANCE micro-run; commit pending at persistence)
CONTRACT = C:\Users\User\Documents\ChatGPT\PE\PE_CMO_ARG1_SINGLE_CALLSITE_PROMPT_20261009\OPENCODE_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009.md — 18964 B, SHA256 9BAF558EA21751B59FA00C41EF532CA20D829AA6082804387DD4BDB71BBF4939 — verified MATCH
TARGET_IDENTITY = Entropia.exe 8015872 B / SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (unchanged; reads limited to the authorized 28-byte window + mapping/identity)
VERDICT = MASTER_ACCEPTED (advisory; ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT = NONE)

## Preflight
LOCAL_HEAD == origin/master == actual remote master == e687eb1360cc0f6f4c4d7c8db7587bb5d357bc6b (live ls-remote). OUTPUT_ROOT created fresh. All 4 required repo inputs MATCH (bytes + Git blobs + physical files). EXE identity verified. Governance read (AUDIT_ENTRYPOINT.md 271684 B / 53528A82… == HEAD blob); no governance conflict — the dispatch's phase split recorded in INPUT_IDENTITIES.md.

## Finding (the one question, answered within bound)
- INSTRUCTION identity: window [0x00528E76,0x00528E92), 28 B @ file offset 1216118; bytes 8B F1 89 74 24 10 8B 44 24 44 8B 4C 24 40 8B 7C 24 3C 50 51 57 8B CE E8 1E 23 33 00; window SHA256 64102BC0…923A2 == contract pin; CALL @0x00528E8D rel32 → 0x0085B1B0 — CONFIRMED (fresh physical re-pin by executor, QC and PE-MASTER independently).
- ARG1: the value delivered as the first explicit stack argument of FUN_0085B1B0 at CALL 0x00528E8D = the DWORD loaded into EDI at 0x00528E84 (immediate source operand DWORD [S+0x3C], S = the symbolic unknown ESP at 0x00528E76), delivered by push edi @0x00528E8A into the entry slot [S-0xC] — CONFIRMED (in-window reaching definition established; sole in-window EDI def; no in-window write aliases [S+0x3C]; ESP_BEFORE_CALL = S-0x0C; ESP_AT_CALLEE_ENTRY = S-0x10; the receiver ECX:=ESI is a separate channel from arg1).
- UPSTREAM: the contents/producer/type of [S+0x3C] before the window = UNRESOLVED_UPSTREAM (deliberate boundary; UPSTREAM_PROVIDER_TRACING = 0). Path scope = the examined straight-line path entering 0x00528E76 normally reaching the CALL; no global uniqueness claim. ABI assumptions stated (right-to-left push order ⇒ last push = arg1; thiscall receiver in ECX; callee entry conventions cited from prior-pinned committed evidence — callee body not re-opened; delivery to entry does not claim a later normal return).
- SCIENCE_OUTCOME = ARG1_DIRECT_SOURCE_ESTABLISHED, coexisting with UPSTREAM_PROVENANCE = UNRESOLVED_UPSTREAM (both dimensions reported per the contract).

## Gate predicates
- Controls: 6 cases × 2 implementations = 12 analysis outcomes (cases ≠ outcomes). Executor: BASELINE_QUALIFIED + M1–M5 all CONTROL_PASS — each mutant discriminated on its expected fields through the REAL analysis (GNU objdump 2.44 raw output + symbolic replay; no byte-pin/hash shortcuts; fixtures byte-confined; baseline hash identity-only). QC: own byte read, own objdump invocation (raw outputs byte-identical after path normalization — same disassembler honestly stated as NOT cross-implementation disassembler QC), own replay implementation (no executor-code import), own fixtures (SHA256s byte-identical by independent construction) — 6/6 outcome agreement; negative controls NC1 (unsupported form → controlled FAIL_CLOSED) and NC2 (target falsifier) live.
- QC_VERDICT = QC_PASS — the ledger derivation agrees field-by-field (0 semantic differences); executor claims verified (identities/ledger/controls/ARG1_PROVENANCE completeness; preregistration-before-science consistent — documentary corroboration, not cryptographic proof, disclosed); the executor's in-run repairs R1+R2 adjudicated HONEST (defective intermediate verdicts preserved in CONTROLS_RESULTS.json notes; expectations unchanged vs contract §5).
- Scope: CALLSITES 1/1; every other budget 0 (bodies/callee bodies/edges/upstream tracing/semantic promotions/runtime/network/placement/model RE/Gamebryo-OpenMW); window-only EXE reads; W3's first two bytes not decoded (DOC-1 honored); callee body never re-opened.

## PE-MASTER counter-checks
Independent window re-pin (bytes/SHA/offset/rel32 — ALL MATCH) and full manual ledger verification: instruction sizes 2+4+4+4+4+1+1+1+2+5 = 28 B; ESP deltas 0,0,0,0,0,-4,-4,-4,0,-4; arg1 entry slot [S-0xC] = the last push (EDI); arg1 value = MEM(S+0x3C)@0x00528E84; receiver = ESI via mov ecx,esi — ALL CONSISTENT with the executor and QC derivations.

## Findings
NONE material. Open: F-QC-1 (P3, non-blocking) — the executor's register_definitions emission loses intermediate defs (cosmetic; no verdict/check/claim depends on it; a future correction needs a new human decision); F-QC-2 (P3) — two QC-side cosmetic notes. Disclosed: executor in-run repairs R1+R2 (preserved honestly); one transient stray temp path outside the repo (removed same session, recorded); GENERAL_UNSUPPORTED_FORM_FAIL_CLOSED exercised only on the QC replay (NC1), not the executor path — NOT_ESTABLISHED stands.

## Standing preserved (verbatim, §8)
CMO_C1 = CLOSED_FOR_AUDITED_STATE (e687eb1…); CORE_RECEIVER_VALUE_CHAIN = PRESERVED_CONFIRMED_STATIC_CONDITIONAL; PHYSICAL_TRANSFORM_MEASUREMENTS = PRESERVED; NEW_TRANSFORM_TRACE = MEASURED_INCIDENTAL_OUTSIDE_PERMITTED_PROMOTION; SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN = NOT_QUALIFIED_BY_ORIGINAL_SCOPE; ORIGINAL_J3_EDGE_BUDGET_COMPLIANCE = FAIL; GENERAL_X86_DECODER_CORRECTNESS = NOT_ESTABLISHED; GENERAL_UNSUPPORTED_FORM_FAIL_CLOSED = NOT_ESTABLISHED; FIELD_SEMANTICS = UNVERIFIED; WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED; HISTORICAL_PLACEMENT = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO; CANONICAL_GATE_EFFECT = NONE; NEXT_EXPERIMENT_AUTHORIZED = NO. DOC-1..DOC-4 P3 backlog preserved; no J3 restoration; this argument relation is NOT promoted to any main-model/world-instance/XYZ claim.

## Coverage
Full read: contract (263 lines), executor/QC handoffs, window identity, ledger, provenance JSON, controls results (census-level with load-bearing fields verified). PE-MASTER physical counter-check: window re-pin + manual ledger decomposition — ALL MATCH. NOT_CHECKED: the unmodified upstream producer of [S+0x3C] (deliberately untraced), the callee body (not re-opened), the executor fail-closed path liveness on its own script (verified by full code read + the analogous QC NC1 liveness), runtime (prohibited), the independent Desktop post-audit of the resulting SHA (NOT_PERFORMED, future).

SOURCE_DESKTOP_POST_AUDIT = N/A (this micro-run derives from committed prior evidence, not a Desktop finding)
INDEPENDENT_DESKTOP_POST_AUDIT = NOT_PERFORMED
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
