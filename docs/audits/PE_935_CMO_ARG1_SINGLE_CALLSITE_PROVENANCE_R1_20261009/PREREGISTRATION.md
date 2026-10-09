# PREREGISTRATION — PE_935_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009

Written BEFORE any disassembly, byte-window extraction or analysis. This file
pre-registers the question, the window identity pins, the budget, the analysis
boundary, the symbolic-stack plan, the expected control results and the
falsifiers. All numeric expectations below are PRE-REGISTERED EXPECTATIONS from
the frozen human-authorized contract and prior committed evidence; every one of
them is to be independently MEASURED in this run before any result is claimed.

- RUN_ID = `PE_935_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009`
- RUN_CLASS = `BOUNDED_STATIC_ARGUMENT_PROVENANCE`
- Contract = `C:\Users\User\Documents\ChatGPT\PE\PE_CMO_ARG1_SINGLE_CALLSITE_PROMPT_20261009\OPENCODE_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009.md`
  (18964 B / SHA256 `9BAF558EA21751B59FA00C41EF532CA20D829AA6082804387DD4BDB71BBF4939`,
  identity verified MATCH before work).
- Repo = `SebastianKozlo/eudoria-clean`, branch `master`,
  EXPECTED_BASE_SHA = `e687eb1360cc0f6f4c4d7c8db7587bb5d357bc6b` (git triple
  re-verified by this executor: local HEAD == origin/master == live remote
  master).
- STATIC_ONLY — the client never runs. Read-only binary analysis.

## 1. The one question (contract §1)

What value is delivered as the FIRST EXPLICIT STACK ARGUMENT (`arg1`) of
FUN_0085B1B0 at CALL `0x00528E8D`, and what is its immediate source operand?

Scope discipline (pre-registered): the value is NOT assumed to be a caller
function argument, a historical record, a pointer with known object identity,
a model, or a coordinate. `arg1` here means the first explicit stack argument
slot `[ESP_at_callee_entry + 4]`; the ECX receiver channel (thiscall `this`) is
SEPARATE and is not counted as arg1. This run formalizes an already visible
local relation inside one 28-byte window; it is not presented as recovery of
world data.

## 2. Window identity pins (pre-registered, TO BE MEASURED)

```text
AUTHORIZED_ORIGINAL_CODE_WINDOW = [0x00528E76, 0x00528E92)
AUTHORIZED_ORIGINAL_CODE_BYTES = 28
PHYSICAL_FILE_OFFSET = 1216118 (0x128E76)
WINDOW_SHA256 (expected) = 64102BC06987D31B9610B43602B7F777A73219FF9209F554241EE52080B923A2
```

Expected original bytes (hypothesis/identity pin, TO BE MEASURED — taken from
the frozen contract and cross-checkable against the committed prior W3 record
of `PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009/CONTROL_RESULTS.json`
(W3 va 0x00528E74, len 52, raw_offset 1216116), of which this window is the
sub-range beginning TWO BYTES in):

```text
8B F1 89 74 24 10 8B 44 24 44 8B 4C 24 40 8B 7C 24 3C 50 51 57 8B CE E8 1E 23 33 00
```

Window-boundary rule (contract §3): 0x00528E76 is an instruction start by the
PRIOR PINNED evidence only (prior package pin_00528e76 = `8B F1`); the first
two W3 bytes (`00 00` at 0x00528E74..75, the tail of the preceding instruction)
are NOT decoded and NOT trusted as an independently proven function start
(P3 backlog DOC-1: padding alone is not a trusted function start). Original
code is read ONLY within [0x00528E76, 0x00528E92). PE headers/section metadata
and the whole-file identity hash are permitted for mapping/identity only.

## 3. Budget (contract §3 — all zeros except the one callsite)

```text
CALLSITES_ANALYZED_MAX = 1        (used: 1 — CALL 0x00528E8D)
NEW_FUNCTION_BODIES = 0
NEW_CALLEE_BODIES = 0             (FUN_0085B1B0 body NOT re-opened)
NEW_CALL_EDGES = 0                (the 0x00528E8D->0x0085B1B0 edge is PRIOR
                                   committed pinned evidence, re-pinned, not new)
UPSTREAM_PROVIDER_TRACING = 0
FIELD_SEMANTIC_PROMOTIONS = 0
RUNTIME_WORK = 0
NETWORK_RE = 0
PLACEMENT_RE = 0
MODEL_RE = 0
GAMEBRYO_OPENMW_RESEARCH = 0
```

Decomposing the argument delivery into load/register/push/stack steps is part
of the single question. If the source precedes the window, record the boundary
and STOP tracing. No xref/callgraph census, no upstream stack-frame
reconstruction, no sibling-store analysis outside the window, no RTTI
expansion, no later scene/model analysis.

## 4. Evidence method plan (contract §4)

- Mature disassembler: GNU objdump via WSL (measured availability: GNU objdump
  (GNU Binutils for Debian) 2.44; WSL2 Debian, kernel 6.18.33.2-microsoft-
  standard-WSL2). Bounded raw-binary disassembly of the extracted 28 bytes:
  `objdump -D -b binary -m i386 -M intel --adjust-vma=0x528e76 <fixture>`.
  Tool name, version, command and ACTUAL raw output are captured into
  `01_EVIDENCE/CALLSITE_DISASSEMBLY.txt`.
- NO new x86 decoder is built, extended or qualified. The CMO-C1 closure does
  NOT qualify the QC 0x8A branch or general unsupported forms.
- Helper `03_SCRIPTS/run_stack_controls.py` (pure stdlib, run with `python -B`)
  may symbolically replay ONLY instructions that objdump actually decoded from
  the fixture bytes; its decoder input is always the objdump output / raw bytes,
  never a hand-authored instruction list. Any instruction the symbolic layer
  cannot handle returns a controlled UNRESOLVED/FAIL — never a fabricated
  source. The helper itself invokes objdump (same version) for the baseline and
  each synthetic fixture, captures the raw outputs, and derives everything from
  them.
- Temporary disassembler inputs (baseline window + 5 synthetic mutant copies)
  live ONLY in a task-owned OS temp directory OUTSIDE Git
  (`C:\Users\User\AppData\Local\Temp\opencode\PE_935_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009\`),
  with recorded identities; all raw outputs are captured into this package
  before removal of the temp files; never staged.

## 5. Symbolic-stack plan (contract §4)

- `S` = the UNKNOWN ESP at 0x00528E76. NOT an invented runtime address, NOT
  the caller function-entry ESP.
- Initially-unknown registers and all memory reads stay symbolic:
  the entry value of ECX is `ECX0` (unknown), entry ESI/EDI/EAX/EBX likewise
  unknown-and-untrusted.
- Instruction-by-instruction ledger (`STACK_LEDGER.csv`): VA, bytes, decoded
  text, ESP delta, register definitions, memory source operands (the source
  SLOT ADDRESS expression is distinguished from the VALUE read from it, and
  both are distinguished from the ARGUMENT SLOT the value is copied into),
  pushes, and the return-address push by CALL.
- Top prepared stack slots are captured as needed to establish arg1 (arg1
  delivery slot and its content; arg2/arg3 slots recorded for explicitness),
  WITHOUT declaring the complete function signature or the semantics of other
  arguments.
- Callee entry conventions are REUSED from pinned prior committed evidence
  (contract §3): FUN_0085B1B0's own pinned instruction list shows its entry
  instruction `8B 44 24 08` (mov eax,[esp+0x8]) reading the arg2 slot at
  entry, and `8B 7C 24 14` @0x0085B1DA (mov edi,[esp+0x14], after FOUR
  pushes ebx/ebp/esi/edi = entry+4) reading the ARG1 slot — i.e. the callee's
  arg1 = `[ESP_at_entry + 4]` = the LAST value pushed by the caller before
  CALL. The callee body is NOT re-opened.

## 6. Hypothesis to qualify independently on the unmodified client

Pre-registered expected decode of the 28 bytes (10 instructions, straight
line, no branches):

```text
0x00528E76: 8B F1            mov esi,ecx            (ESI := ECX0)
0x00528E78: 89 74 24 10      mov [esp+0x10],esi     (write [S+0x10]; ESP unchanged)
0x00528E7C: 8B 44 24 44      mov eax,[esp+0x44]     (EAX := DWORD [S+0x44])
0x00528E80: 8B 4C 24 40      mov ecx,[esp+0x40]     (ECX := DWORD [S+0x40])
0x00528E84: 8B 7C 24 3C      mov edi,[esp+0x3C]     (EDI := DWORD [S+0x3C])
0x00528E88: 50               push eax               (ESP = S-4; [S-4] := [S+0x44] value)
0x00528E89: 51               push ecx               (ESP = S-8; [S-8] := [S+0x40] value)
0x00528E8A: 57               push edi               (ESP = S-0xC; [S-0xC] := [S+0x3C] value)
0x00528E8B: 8B CE            mov ecx,esi            (receiver ECX := ESI := ECX0)
0x00528E8D: E8 1E 23 33 00   call 0x0085B1B0        (rel32 0x0033231E; next=0x00528E92;
                                                     0x00528E92+0x0033231E = 0x0085B1B0)

ESP_BEFORE_CALL       = S-0x0C
ESP_AT_CALLEE_ENTRY   = S-0x10   (CALL pushes the return address 0x00528E92)
ARG1_SLOT_AT_ENTRY    = [ESP_AT_CALLEE_ENTRY+4] = [S-0x0C]
ARG1_VALUE            = the value loaded into EDI from DWORD [S+0x3C] at 0x00528E84
ARG1_IMMEDIATE_PRODUCER_VA   = 0x00528E84 (the only in-window EDI definition)
ARG1_IMMEDIATE_SOURCE_OPERAND = DWORD [S+0x3C]  (caller source slot; contents
                                                 before the window = UNRESOLVED_UPSTREAM)
RECEIVER              = ESI (via mov ecx,esi @0x00528E8B; ESI := ECX0 @0x00528E76,
                            prior pinned caller evidence: FUN_00528E50's `this`)
```

Aliasing/ESP assumptions to be verified explicitly in the measurement (contract
§4): the only in-window memory write before the pushes is [S+0x10] (not an
alias of [S+0x3C]); all three loads execute with ESP = S (before any push);
the pushes write only [S-4], [S-8], [S-0xC] (below S); the arg1 source slot
[S+0x3C] is read BEFORE any push executes.

## 7. Expected controls and boundary (contract §5 — pre-registered)

The ordinary analysis result is defined as structured facts independent of
the expected answer: receiver source; arg1 register producer and its in-window
definition VA or unresolved boundary; source-memory expression; per-instruction
ESP deltas; ESP before CALL and at callee entry; arg1 entry slot. The SAME
predicate runs on the baseline and on five synthetic copies of the 28 bytes.
The original-byte hash is an identity check ONLY on baseline — it is NOT the
reason a synthetic control is rejected; every mutant must reach the REAL
analysis (objdump + symbolic replay), not merely fail a byte pin or file hash.

| Case | Exact synthetic change (on the 28-byte copy) | Pre-registered expected discriminating result |
|---|---|---|
| BASELINE | none | 10 instructions as in §6; ARG1 = push EDI @0x00528E8A of the value loaded from [S+0x3C] @0x00528E84; ESP_BEFORE_CALL=S-0x0C; ESP_AT_ENTRY=S-0x10; arg1 entry slot [S-0x0C]; receiver ESI. (Or honest bounded failure.) |
| M1_PUSH_ORDER | @0x00528E89..8A: `51 57` -> `57 51` | Last push (now @0x00528E8A) supplies the value loaded into ECX @0x00528E80 from [S+0x40]; arg1 source = MEM(S+0x40); receiver still ESI; the original EDI-source claim is NOT retained (arg2 becomes the EDI value). |
| M2_ESP_BEFORE_READ | @0x00528E78..7B: `89 74 24 10` -> `83 EC 04 90` (sub esp,4; nop) | At the subsequent EDI load ESP=S-4 so its source is [S+0x38]; ESP before CALL = S-0x10; at entry S-0x14; fixture stays 28 bytes with a DIFFERENT instruction count (11). |
| M3_EDI_DEFINITION_REMOVED | @0x00528E84..87: `8B 7C 24 3C` -> `8B 4C 24 3C` | The load defines ECX, not EDI; the final push still reads EDI whose definition is now OUTSIDE the window: ARG1 source = UNRESOLVED_UPSTREAM (register EDI, no in-window reaching definition), not the original memory-derived EDI claim. |
| M4_RECEIVER_ONLY | @0x00528E8B..8C: `8B CE` -> `8B CF` | Receiver source changes from ESI to EDI; arg1 source and its stack delivery remain EXACTLY as baseline; receiver (ECX channel) and arg1 (stack slot channel) remain separate — same symbolic value expression on both channels is NOT a numeric inequality claim. |
| M5_SOURCE_DISPLACEMENT | @0x00528E84..87: `8B 7C 24 3C` -> `8B 7C 24 38` | EDI/arg1 now derive from [S+0x38]; stack deltas and receiver as baseline. |

Symbolic-provenance discipline: different expressions do NOT prove unequal
runtime values (e.g. [S+0x40] could coincidentally hold the same DWORD as
[S+0x3C]). The controls test whether the PROVENANCE CLAIM is justified, not a
fabricated numeric inequality. Correctly recognizing a mutant = CONTROL_PASS
even if its answer changes or becomes unresolved. A synthetic mutant never
falsifies the unmodified historical client; only contradictory evidence from
the unmodified client may justify HISTORICAL_HYPOTHESIS_REJECTED.

## 8. Falsifiers (pre-registered)

- F1 (identity): measured window bytes/size/SHA256 differ from §2 pins ->
  BLOCKED identity failure (not a science result).
- F2 (boundaries): objdump's actual decode of the window disagrees with the
  §6 instruction boundaries (e.g. CALL not at 0x00528E8D, window not ending
  exactly at 0x00528E92, unexpected branches/control flow) -> the straight-line
  and boundary assumptions fail; outcome degrades honestly
  (ARG1_REACHING_DEFINITION_AMBIGUOUS / UNRESOLVED_WITHIN_BOUND).
- F3 (target): rel32 recomputed from the measured CALL bytes != 0x0085B1B0 ->
  callee-target mismatch; investigate within bound or finalize UNRESOLVED.
- F4 (reaching definition): an in-window write aliasing [S+0x3C] (or an
  intervening redefinition of EDI between 0x00528E84 and the push, or an
  unexpected ESP change before the loads) -> the arg1 reaching definition is
  NOT established as hypothesized; degrade the outcome honestly.
- F5 (control liveness): a mutant whose measured discriminating field equals
  the baseline result (mutant not recognized by the analysis predicate) ->
  CONTROL_FAIL for that case; the predicate is insufficient, never silently
  repaired post hoc.
- F6 (fabrication guard): any instruction the symbolic replay cannot handle ->
  controlled UNRESOLVED/FAIL for that fixture; never a fabricated source.

## 9. Path scope and ABI assumptions (pre-registered)

- PATH_SCOPE: the examined straight-line path entering 0x00528E76 and
  normally reaching the CALL. The local reaching-definition proof applies ONLY
  to that path; NO global uniqueness claim across unexamined entries or
  execution paths.
- UPSTREAM_BOUNDARY: the contents of the caller source slot [S+0x3C] before
  the window — its producer, its type, any caller-function-argument identity —
  are UNRESOLVED_UPSTREAM and will NOT be traced in this run.
- ABI_ASSUMPTIONS (stated, reused from pinned prior evidence): 32-bit x86
  push/call stack semantics; caller pushes arguments right-to-left so the LAST
  push before CALL occupies [ESP_at_entry+4] = arg1; the thiscall receiver
  travels in ECX and is separate from arg1; the callee's own pinned entry
  conventions (arg1 read @0x0085B1DA from [esp+0x14] after four pushes =
  [entry+4]; arg2 read by the entry instruction `mov eax,[esp+0x8]`) are
  consistent with this ordering. Delivery to callee entry does NOT require
  claiming a later normal return.
- The measured caller source slot is recorded separately from the argument
  slot and from any hypotheses about its type.

## 10. Standing preserved (contract §8 — carried verbatim, not re-derived)

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

P3 backlog preserved: DOC-1 (padding alone is not a trusted function start),
DOC-2 (historical M1–M6 are not six semantic byte mutations), DOC-3
(additional QC 0x8A support is not qualified by CMO-C1), DOC-4 (the internal
11/11 aggregate includes a literal-True documentation gate and deferred
manifest obligations). No reopening of CMO-C1; no restoration of the J3
transform promotion; this argument relation is NOT turned into a
main-model/world-instance/XYZ claim.

## 11. Phase boundary of this executor (dispatch scope)

This executor writes ONLY: `PREREGISTRATION.md`, `INPUT_IDENTITIES.md`,
`01_EVIDENCE/WINDOW_IDENTITY.json`, `01_EVIDENCE/CALLSITE_DISASSEMBLY.txt`,
`STACK_LEDGER.csv`, `ARG1_PROVENANCE.json`, `CONTROLS_RESULTS.json`,
`03_SCRIPTS/run_stack_controls.py`. `QC_RESULTS.json` + `QC_REPORT.md` are the
fresh-QC worker's phase; `FINAL_REPORT.md`/`EVIDENCE_INDEX.md`/`HANDOFF.md`/
`MANIFEST_SHA256.csv`/the AUDIT_ENTRYPOINT.md row are later parent phases.
NO_NESTED_TASKS. No AUDIT_ENTRYPOINT.md write, no stage, no commit, no push in
this phase. Fresh internal QC is NOT performed by this executor.

## 12. Science outcome vocabulary (contract §6)

Exactly one of:
`ARG1_DIRECT_SOURCE_ESTABLISHED` / `ARG1_STACK_SLOT_ESTABLISHED_UPSTREAM_UNRESOLVED`
/ `ARG1_REACHING_DEFINITION_AMBIGUOUS` / `HISTORICAL_HYPOTHESIS_REJECTED` /
`UNRESOLVED_WITHIN_BOUND`. A confirmed direct source MAY coexist with
unresolved upstream provenance — both dimensions are reported. Critical
preflight failure is BLOCKED, not a science result.
