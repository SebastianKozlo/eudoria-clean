# FINAL_REPORT — PE_935_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009

RUN_CLASS = BOUNDED_STATIC_ARGUMENT_PROVENANCE (one-question micro-run)
SCIENCE_OUTCOME = ARG1_DIRECT_SOURCE_ESTABLISHED (coexisting with UPSTREAM_PROVENANCE = UNRESOLVED_UPSTREAM)
QC_VERDICT = QC_PASS | RUN_VERDICT = PE-MASTER MASTER_ACCEPTED (advisory; ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT = NONE)

This report formalizes an ALREADY VISIBLE LOCAL ARGUMENT-DELIVERY RELATION inside
one authorized 28-byte window. It is NOT recovery of world data, NOT a field-semantics
result, NOT a world-instance/placement/XYZ claim, and it authorizes NO automatic
upstream continuation (the producer of the caller source slot [S+0x3C] before the
window stays UNRESOLVED_UPSTREAM by budget).

## 1. Run and contract identity (measured)

| Item | Value |
|---|---|
| RUN_ID | `PE_935_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009` |
| Contract | `C:\Users\User\Documents\ChatGPT\PE\PE_CMO_ARG1_SINGLE_CALLSITE_PROMPT_20261009\OPENCODE_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009.md` — 18964 B / SHA256 `9BAF558EA21751B59FA00C41EF532CA20D829AA6082804387DD4BDB71BBF4939` — verified MATCH (executor preflight, fresh QC, PE-MASTER master audit; re-verified at persistence) |
| Repository / branch | `SebastianKozlo/eudoria-clean`, `master` |
| BASE_SHA | `e687eb1360cc0f6f4c4d7c8db7587bb5d357bc6b` (LOCAL_HEAD == origin/master == actual remote master, live ls-remote; re-verified at persistence immediately before commit) |
| Target binary | `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe` — 8015872 B / SHA256 `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` — unchanged (rehashed before and after by executor and QC; reads limited to the authorized window + PE headers for mapping/identity; no EXE access in the persistence phase) |
| Executor | pe-reconstruction (OpenCode executor phase; preregistration written before science) |
| Fresh internal QC | pe-master-auditor fresh-context internal QC (internal to PE-MASTER; NOT an independent Desktop post-audit; NOT executor self-review) |
| PE-MASTER master audit | internal advisory MASTER_AUDIT (see `PE_MASTER_REVIEW.md`, persisted verbatim) |

## 2. Preflight (executor-measured; independently re-verified by QC and PE-MASTER)

- Git triple MATCH (local HEAD == origin/master == live remote master == EXPECTED_BASE_SHA `e687eb1…`); tracked tree CLEAN; OUTPUT_ROOT absent before the executor phase (created only after preflight PASS).
- Foreign untracked census (untouched throughout, left exactly as found): 5× `PE_935_*` packages + `experiments/`.
- All four contract §2 required repository inputs MATCH (physical bytes + SHA256 + Git blob equality at HEAD):
  - `docs/audits/PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009/CONTROL_RESULTS.json` — 18509 B / `9545D0D78881C29BC805EA3A05C8AA936D364256671D31A1AE907677A63DE2F8` (blob `6645aa4b…`)
  - `docs/audits/PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009/FINAL_REPORT.md` — 15589 B / `FF5FDBD2F54F20E3026B5992F7BCC411B0572ADA249F157BA11CB441E1AC83E0` (blob `4c170743…`)
  - `docs/audits/PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009/SUPERSESSION_AND_STANDING.md` — 6848 B / `0AB2CDECE09CB2FF1419C48E9A1169832A0A061C618A7F94F290089C75F49921` (blob `52f41585…`)
  - `docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007/SUPERSESSION.md` — 8339 B / `DD11137A0E79491511A7688B7C1DE9252DB7BA443FA31892C345CA76CE136845` (blob `05de1ce9…`)
- Governance read: `AUDIT_ENTRYPOINT.md` 271684 B / SHA256 `53528A82695C710FCF68ACD60BAF9B9442CD649B89F4C82E35F81ED86660E5BB` == HEAD blob; no governance conflict — the dispatch's phase split (executor / QC / persistence) recorded in `INPUT_IDENTITIES.md`.

## 3. Window identity (measured; fresh physical re-pin, triple-verified: executor, QC, PE-MASTER)

```text
AUTHORIZED_ORIGINAL_CODE_WINDOW = [0x00528E76, 0x00528E92)
SIZE = 28 B; file offset 1216118 (0x128E76); RVA 0x128E76; ImageBase 0x400000; section .text
BYTES = 8B F1 89 74 24 10 8B 44 24 44 8B 4C 24 40 8B 7C 24 3C 50 51 57 8B CE E8 1E 23 33 00
WINDOW_SHA256 = 64102BC06987D31B9610B43602B7F777A73219FF9209F554241EE52080B923A2  (== contract pin)
CALL @0x00528E8D: bytes E8 1E 23 33 00; rel32 0x0033231E; next VA 0x00528E92;
  recomputed target 0x00528E92 + 0x0033231E = 0x0085B1B0 == objdump target == CALLEE_TARGET
```

The window begins TWO BYTES into the previously recorded W3 (0x00528E74, len 52, raw
offset 1216116). W3's first two bytes (offsets 1216116..1216117) were NOT read and NOT
decoded — DOC-1 honored by executor, QC and PE-MASTER. Original code was read ONLY
within this window; PE headers/section metadata and whole-file hashing are mapping /
identity only.

## 4. Tool provenance

- Disassembler (the ONLY decoder; none built, extended or qualified): **GNU objdump
  (GNU Binutils for Debian) 2.44** via WSL2 Debian 13 (kernel
  6.18.33.2-microsoft-standard-WSL2); Python 3.13.5 (`python -B`, no bytecode residue).
- Command (baseline; per-case command recorded in `CONTROLS_RESULTS.json`, all six
  invocations returncode 0, stderr empty):
  `objdump -D -b binary -m i386 -M intel --adjust-vma=0x528e76 <fixture>`
- Raw output reference: baseline verbatim in `01_EVIDENCE/CALLSITE_DISASSEMBLY.txt`;
  all six fixture outputs (baseline + M1–M5) in `CONTROLS_RESULTS.json`
  (`objdump_raw_output_by_case`), plus per-case fixture identities (size/SHA256/byte
  deltas) and the temp-cleanup record (fixtures removed after capture, identities at
  removal recorded, nothing staged).
- Symbolic replay (bounded helper, fail-closed): executor `03_SCRIPTS/run_stack_controls.py`
  (replays ONLY objdump-decoded instructions; unsupported forms → controlled
  UNRESOLVED/FAIL); QC `03_SCRIPTS/qc_stack_replay.py` (own implementation, no
  executor-code import).

## 5. Baseline stack ledger (S = the UNKNOWN ESP at 0x00528E76; executor derivation, QC agrees field-by-field, PE-MASTER manual verification consistent)

| VA | Bytes | Instruction | ESP delta | ESP after | Register / memory effects |
|---|---|---|---:|---|---|
| 0x00528E76 | 8B F1 | mov esi,ecx | 0 | S | ESI := ECX0 (entry ECX, symbolic) |
| 0x00528E78 | 89 74 24 10 | mov [esp+0x10],esi | 0 | S | the ONLY in-window memory write: [S+0x10] := ECX0 (not an alias of any read slot) |
| 0x00528E7C | 8B 44 24 44 | mov eax,[esp+0x44] | 0 | S | EAX := DWORD [S+0x44] |
| 0x00528E80 | 8B 4C 24 40 | mov ecx,[esp+0x40] | 0 | S | ECX := DWORD [S+0x40] |
| 0x00528E84 | 8B 7C 24 3C | mov edi,[esp+0x3C] | 0 | S | EDI := DWORD [S+0x3C] — the sole in-window EDI definition (arg1 immediate producer) |
| 0x00528E88 | 50 | push eax | -4 | S-0x4 | [S-0x4] := MEM(S+0x44)@0x00528E7C (arg3 delivery) |
| 0x00528E89 | 51 | push ecx | -4 | S-0x8 | [S-0x8] := MEM(S+0x40)@0x00528E80 (arg2 delivery) |
| 0x00528E8A | 57 | push edi | -4 | S-0xC | [S-0xC] := MEM(S+0x3C)@0x00528E84 (arg1 delivery — the LAST push) |
| 0x00528E8B | 8B CE | mov ecx,esi | 0 | S-0xC | receiver ECX := ESI := ECX0 (thiscall `this` channel, SEPARATE from arg1) |
| 0x00528E8D | E8 1E 23 33 00 | call 0x0085B1B0 | -4 | S-0x10 | return address 0x00528E92 pushed to [S-0x10] |

ESP delta sequence: 0,0,0,0,0,-4,-4,-4,0,-4 (instruction sizes 2+4+4+4+4+1+1+1+2+5 = 28 B;
10 instructions, straight line, decode ends exactly at 0x00528E92). Machine-readable
ledger: `STACK_LEDGER.csv` (rows 1..10 + summary; machine-parsed by QC, exact match).

## 6. The arg1 determination (all fields agree with ARG1_PROVENANCE.json field-by-field)

```text
ARG1 (first explicit stack argument of FUN_0085B1B0 at CALL 0x00528E8D)
  = the DWORD loaded into EDI at 0x00528E84
  immediate source operand = DWORD [S+0x3C]        (caller stack slot; ESP = S at the load)
  delivered by push edi @0x00528E8A into the entry slot [S-0xC]
  ESP_BEFORE_CALL = S-0x0C; ESP_AT_CALLEE_ENTRY = S-0x10
  ARG1_ENTRY_SLOT = [ESP_AT_CALLEE_ENTRY+4] = [S-0xC]   (last push = arg1 under the stated ABI)
  ARG1_IMMEDIATE_PRODUCER_VA = 0x00528E84
  REACHING_DEFINITION_STATUS = IN_WINDOW_REACHING_DEFINITION_ESTABLISHED
    (sole in-window EDI def; no intervening redefinition; no in-window write aliases [S+0x3C];
     all three loads execute at ESP = S, before any push)
  RECEIVER = ECX := ESI @0x00528E8B (thiscall receiver; separate channel from arg1)
  arg2 = [S-0x8] = MEM(S+0x40)@0x00528E80; arg3 = [S-0x4] = MEM(S+0x44)@0x00528E7C
    (recorded for explicitness; NO complete signature and NO arg2/arg3 semantics declared)
  UPSTREAM_BOUNDARY = UNRESOLVED_UPSTREAM  (contents/producer/type of [S+0x3C] before the
    window NOT traced; UPSTREAM_PROVIDER_TRACING = 0)
  PATH_SCOPE = the examined straight-line path entering 0x00528E76 normally reaching the CALL;
    no global uniqueness claim across unexamined entries or paths
  ABI_ASSUMPTIONS = 32-bit push/call semantics; right-to-left push order ⇒ last push = arg1;
    thiscall receiver in ECX; callee entry conventions cited from prior pinned committed
    evidence (arg1 read by callee: mov edi,[esp+0x14] @0x0085B1DA after four pushes =
    [entry+4]; arg2: entry mov eax,[esp+0x8]) — callee body NOT re-opened; delivery to
    entry does NOT claim a later normal return.
```

The source-slot ADDRESS [S+0x3C] is recorded separately from the VALUE loaded from it and
from the ARGUMENT SLOT [S-0xC] the value is copied into (three distinct ledger notions).

## 7. The six control cases (expected discriminating results vs measured; same actual analysis predicate)

| Case | Exact synthetic change (28-byte copy) | Pre-registered expected discriminating result | Executor measured | QC measured |
|---|---|---|---|---|
| BASELINE | none | original symbolic arg1 relation + receiver qualified (or honest bounded failure) | BASELINE_QUALIFIED (all expectation checks match) | BASELINE_QUALIFIED (24/24 checks) |
| M1_PUSH_ORDER | @0x00528E89..8A: `51 57` → `57 51` | last push now supplies the ECX value from [S+0x40]; receiver still ESI; EDI-source claim NOT retained | CONTROL_PASS (arg1 = push ecx @8A of MEM(S+0x40)@80; arg2 = EDI value) | CONTROL_PASS (same) |
| M2_ESP_BEFORE_READ | @0x00528E78..7B: `89 74 24 10` → `83 EC 04 90` | loads at ESP=S-4 ⇒ EDI source [S+0x38]; ESP before CALL S-0x10; entry S-0x14; 11 instructions (28 B kept) | CONTROL_PASS (11 insns; arg1 slot [S-0x10]; no mem writes) | CONTROL_PASS (same) |
| M3_EDI_DEFINITION_REMOVED | @0x00528E84..87: `8B 7C 24 3C` → `8B 4C 24 3C` | the load defines ECX not EDI; final push reads EDI with NO in-window def ⇒ UNRESOLVED_UPSTREAM, not the memory-derived claim | CONTROL_PASS (arg1 UNRESOLVED_UPSTREAM, value EDI_ENTRY) | CONTROL_PASS (same) |
| M4_RECEIVER_ONLY | @0x00528E8B..8C: `8B CE` → `8B CF` | receiver source ESI → EDI; arg1 source + stack delivery exactly baseline; channels distinct (symbolic expression equality is NOT a numeric inequality claim) | CONTROL_PASS (receiver ESI→EDI; arg1 unchanged) | CONTROL_PASS (same) |
| M5_SOURCE_DISPLACEMENT | @0x00528E84..87: `8B 7C 24 3C` → `8B 7C 24 38` | EDI/arg1 now derive from [S+0x38]; deltas + receiver as baseline | CONTROL_PASS (arg1 from [S+0x38]) | CONTROL_PASS (same) |

12-outcome accounting (contract §5): **6 cases × 2 implementations = 12 analysis
outcomes** (cases ≠ outcomes; NOT 12 independent implementations). Executor:
BASELINE_QUALIFIED + 5× CONTROL_PASS (6 outcomes). QC: BASELINE_QUALIFIED + 5×
CONTROL_PASS (the other 6 outcomes) — 6/6 verdict agreement, 0 semantic differences.
Each mutant reached the REAL analysis (objdump raw output + symbolic replay; the
original-byte hash is an identity check on baseline ONLY; no byte-pin/hash shortcut
rejected any mutant; mutant fixtures byte-confined to the declared offsets). QC fixture
SHA256s are byte-identical to the executor's by independent construction (convergence,
not copying); QC raw objdump outputs byte-identical after fixture-path normalization.
Symbolic-provenance discipline held: different expressions do not prove unequal runtime
values; a synthetic mutant never falsifies the unmodified client; falsifiers_triggered = [].

## 8. Fresh internal QC results

- QC_ORIGIN = pe-master-auditor fresh-context internal QC, inside PE-MASTER's
  delegation chain (INTERNAL to PE-MASTER; NOT an independent Desktop post-audit, NOT
  executor self-review). QC_VERDICT = **QC_PASS** (machine detail: `QC_RESULTS.json`;
  narrative: `QC_REPORT.md`).
- QC independence dimensions, stated honestly: own byte read of the window, own PE
  mapping, own objdump invocations (8: baseline + M1–M5 + NC1 + NC2, raw outputs
  captured), own parser with per-instruction byte-column cross-validation against the
  physical fixture bytes, own symbolic replay implementation (no executor-code import),
  own fixtures (SHA convergence), own expectations independently re-translated from the
  frozen contract §4/§5/§6, own negative controls. **Same disassembler as the executor
  (GNU objdump 2.44) — sharing a disassembler is NOT cross-implementation disassembler
  QC** (decode-layer independence was NOT provided).
- QC negative controls (QC-internal, NOT part of the 12 outcomes): NC1 — a `cmpxchg`
  inside the window ⇒ controlled FAIL_CLOSED (`unsupported mnemonic`), no facts, no
  fabricated source (NC_PASS_FAIL_CLOSED_LIVE); NC2 — one rel32 byte mutated
  (0x1E→0x2E) ⇒ recomputed target 0x0085B1C0 ≠ pinned 0x0085B1B0 ⇒ the pinned-target
  check FAILED as designed (NC_PASS_TARGET_FALSIFIER_LIVE).
- QC findings: **F-QC-1 (P3, cosmetic, non-blocking)** — the executor's
  `register_definitions` emission loses intermediate defs (e.g. the ECX load
  @0x00528E80 invisible in BASELINE; no verdict/check/claim depends on it; a future
  correction needs a new human decision; revalidation predicate: re-run and confirm
  every definition event appears with its own def_va). **F-QC-2 (P3)** — two QC-side
  cosmetic notes (NC1 description operand order; QC uppercase byte-string emission
  style). No material findings; 0 semantic disagreements with the executor.
- QC verified: all input identities (contract/EXE/git/4 repo inputs/entrypoint blob),
  the ledger field-by-field, all six control outcomes, ARG1_PROVENANCE.json
  completeness (incl. SCIENCE_OUTCOME coexisting with UPSTREAM_PROVENANCE), the §8
  standing carried verbatim, the budget, preregistration-before-science CONSISTENT
  (mtime + content corroboration — documentary, NOT cryptographically proven;
  disclosed), and the process-residue disclosure (stray temp path confirmed GONE).

## 9. Disclosed process items (no fabricated success)

- **Executor in-run repairs R1 + R2, adjudicated HONEST by QC and PE-MASTER**: R1 —
  instruction-length arithmetic defect (`len(hex)//2` counting separators); the
  contiguity gate fail-closed on the anomaly for EVERY fixture (honest BASELINE
  failure + 5× CONTROL_FAIL) and main() BLOCKED before writing any package output;
  repaired to a byte-pair token count. R2 — reaching-definition capture resolved a
  pushed register's definition AFTER the whole window, mis-attributing M1-arg1/M3-arg2
  to the receiver `mov ecx,esi` @0x00528E8B; repaired to snapshot the definition AT
  PUSH TIME; sub-repairs disclosed (hex-string VAs; `[0,0,0]`→`['S','S','S']` form
  normalization). The defective intermediate verdicts are preserved honestly in the
  `executor_implementation_notes` of `CONTROLS_RESULTS.json`; the defective output
  files were regenerated by the repaired third execution (disclosed); no pre-registered
  expectation changed (they equal contract §5); no failed evidence was edited into
  success.
- **One transient stray temp path** outside the repo (typo'd
  `…12_WebGame\eudocracy-clean\INPUT_IDENTITIES_PLACEHOLDER.md`) — created by a write
  slip during executor drafting, removed in the same session, recorded in
  `INPUT_IDENTITIES.md`, confirmed GONE by the QC; the git worktree was never touched.
- **GENERAL_UNSUPPORTED_FORM_FAIL_CLOSED = NOT_ESTABLISHED stands**: the contract's six
  cases never exercise the fail-closed path (executor's own F6 note: unexercised by
  design); liveness was demonstrated only on the QC replay (NC1) plus full code read of
  the executor's fail-closed structure — honestly disclosed, not promoted.

## 10. Scope compliance (all budgets)

```text
CALLSITES_ANALYZED = 1/1 (CALL 0x00528E8D)
NEW_FUNCTION_BODIES = 0 | NEW_CALLEE_BODIES = 0 (FUN_0085B1B0 body NOT re-opened)
NEW_CALL_EDGES = 0 (the 0x00528E8D->0x0085B1B0 edge is PRIOR pinned evidence, re-pinned)
UPSTREAM_PROVIDER_TRACING = 0 | FIELD_SEMANTIC_PROMOTIONS = 0 | RUNTIME_WORK = 0
NETWORK_RE = 0 | PLACEMENT_RE = 0 | MODEL_RE = 0 | GAMEBRYO_OPENMW_RESEARCH = 0
```

Window-only EXE reads (+PE headers for mapping + whole-file identity hashing); W3's
first two bytes never read/decoded (DOC-1); callee entry conventions REUSED from prior
pinned committed evidence (verified as a committed blob by the QC); no xref/callgraph
census, no upstream stack-frame reconstruction, no sibling stores, no RTTI expansion,
no later scene/model analysis; the client never ran.

## 11. Standing preserved (contract §8, verbatim — carried, not re-derived)

```text
CMO_C1 = CLOSED_FOR_AUDITED_STATE
CMO_C1_AUDITED_STATE = e687eb1360cc0f6f4c4d7c8db7587bb5d357bc6b
CORE_RECEIVER_VALUE_CHAIN = PRESERVED_CONFIRMED_STATIC_CONDITIONAL
PHYSICAL_TRANSFORM_MEASUREMENTS = PRESERVED
NEW_TRANSFORM_TRACE = MEASURED_INCIDENTAL_OUTSIDE_PERMITTED_PROMOTION
SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN = NOT_QUALIFIED_BY_ORIGINAL_SCOPE
ORIGINAL_J3_EDGE_BUDGET_COMPLIANCE = FAIL
GENERAL_X86_DECODER_CORRECTNESS = NOT_ESTABLISHED
GENERAL_UNSUPPORTED_FORM_FAIL_CLOSED = NOT_ESTABLISHED
FIELD_SEMANTICS = UNVERIFIED
WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED
HISTORICAL_PLACEMENT = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO
```

P3 backlog DOC-1..DOC-4 preserved; no J3 restoration; this argument relation is NOT
promoted to any main-model/world-instance/XYZ claim.

## 12. PE-MASTER master audit (advisory)

PE-MASTER independently re-pinned the window (bytes/SHA/offset/rel32 — ALL MATCH) and
manually verified the full ledger decomposition (instruction sizes 2+4+4+4+4+1+1+1+2+5
= 28; ESP deltas 0,0,0,0,0,-4,-4,-4,0,-4; the arg1 slot/value/receiver separation) —
ALL CONSISTENT with the executor and QC derivations. VERDICT = **MASTER_ACCEPTED**
(advisory; ADVISORY_PRE_QUALIFICATION — PE-MASTER remains PROVISIONAL_UNTIL_QUALIFIED;
CANONICAL_GATE_EFFECT = NONE). Persisted verbatim as `PE_MASTER_REVIEW.md` (internal
advisory review; NOT an independent Desktop post-audit).

## 13. Terminal governance

```text
SCIENCE_OUTCOME = ARG1_DIRECT_SOURCE_ESTABLISHED  (coexisting with UPSTREAM_PROVENANCE = UNRESOLVED_UPSTREAM)
QC_VERDICT = QC_PASS (internal QC; separate from the science outcome)
RUN_VERDICT = MASTER_ACCEPTED (advisory; ADVISORY_PRE_QUALIFICATION)
INDEPENDENT_DESKTOP_POST_AUDIT = NOT_PERFORMED  (until separately conducted)
FIELD_SEMANTICS = UNVERIFIED
WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED
HISTORICAL_PLACEMENT = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
```

Publication never means scientific acceptance. RESULTING_SHA / REMOTE_SHA are recorded
at the terminal handoff per contract §9 (a commit SHA cannot be embedded in its own
commit's files). No automatic upstream continuation.

**WORKS != UNDERSTOOD. STOP BEFORE SCOPE EXCEED.**
