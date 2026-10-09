# QC_REPORT — PE_935_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009

- **QC_VERDICT: QC_PASS**
- **REAL ORIGIN**: pe-master-auditor fresh-context internal QC, executed inside
  PE-MASTER's delegation chain. This is INTERNAL QC — **not** an independent
  Desktop post-audit (which remains NOT_PERFORMED until separately conducted),
  not executor self-review, and not MASTER_ACCEPTED / milestone closure /
  qualification. PE-MASTER remains advisory, PROVISIONAL_UNTIL_QUALIFIED.
- **RUN_ID**: `PE_935_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009`
- **BASE_SHA = HEAD**: `e687eb1360cc0f6f4c4d7c8db7587bb5d357bc6b` (unchanged;
  executor and QC phases made no stage/commit/push/entrypoint write).
- **Machine-readable detail**: `QC_RESULTS.json` (same directory).

## 1. Method

The QC re-derived everything load-bearing from physical bytes with its own
tooling, then compared against the executor's package:

1. **Identity preflight (own measurements)** — frozen contract 18964 B /
   SHA256 `9BAF558E…BBF4939` MATCH; EXE 8015872 B / SHA256 `E7785430…D5280F31`
   MATCH (own full re-hash before AND after all QC work); git HEAD =
   EXPECTED_BASE_SHA = live remote master (read-only `ls-remote`); tracked tree
   clean; all four contract §2 repo inputs + AUDIT_ENTRYPOINT.md re-hashed with
   git blob equality (`hash-object == rev-parse HEAD:<path>`).
2. **Own window re-pin** — own PE header parse (ImageBase 0x400000; exactly one
   covering section `.text`, VirtualAddress 0x1000, PointerToRawData 0x1000;
   computed file offset 1216118 == pin), own seek/read of exactly 28 bytes at
   offset 1216118, own SHA256 `64102BC0…80B923A2` == pin, own pinned-bytes
   equality. W3's first two bytes (offsets 1216116..1216117) were NOT read
   (DOC-1 honored by the QC as well).
3. **Own disassembler provenance** — the QC invoked GNU objdump 2.44 (WSL)
   itself, 8 times (baseline, M1–M5, and two QC negative controls), capturing
   version/command/returncode/stderr/raw output.
4. **Own symbolic replay** — `03_SCRIPTS/qc_stack_replay.py`, written fresh in
   this QC context: own parser (tab-split, plus per-instruction byte-column
   cross-validation against the physical fixture bytes — a check the
   executor's parser does not perform), own replay with register-definition
   snapshot AT PUSH TIME, own fixture construction from the QC's own window
   read (original-byte verification before mutation, diff-offset verification
   after), own expectation encoding translated independently from contract
   §4/§5/§6.
5. **Field-by-field comparison** — programmatic comparison of raw objdump
   outputs (path-normalized), fixture identities, full baseline facts and all
   mutant discriminating fields against `CONTROLS_RESULTS.json`.
6. **Scans** — standing/scope token scans over ALL package files; governance
   citation spot-checks; stray-path disclosure verification.

### Independence dimensions (stated honestly)

- The QC **shares the same mature disassembler** as the executor (GNU objdump
  2.44 via WSL). **Sharing a disassembler is NOT cross-implementation
  disassembler QC** — the decode layer was not independently re-derived.
- Independent dimensions: own byte read, own PE mapping, own objdump
  invocations, own parser (with byte cross-validation), own replay
  implementation, own mutant fixtures (which converged to byte-identical
  fixture SHA256s — construction convergence, not copying), own expectations
  translated from the frozen contract, own negative controls.
- The QC did **not** import, invoke or copy the executor's
  `run_stack_controls.py`, and did not take the executor's ledger or expected
  results as its source of truth.

## 2. Per-duty results

### Duty 1 — window re-pin + objdump provenance: PASS

QC-measured: window `[0x005E76→) [0x00528E76, 0x00528E92)`, 28 B at file
offset 1216118, bytes
`8B F1 89 74 24 10 8B 44 24 44 8B 4C 24 40 8B 7C 24 3C 50 51 57 8B CE E8 1E 23 33 00`,
SHA256 `64102BC06987D31B9610B43602B7F777A73219FF9209F554241EE52080B923A2` ==
contract pin; rel32 `0x0033231E` → target `0x00528E92 + 0x0033231E =
0x0085B1B0` == objdump target. **AGREE with the executor on every field.**
The QC's raw objdump outputs are **byte-identical** to the executor's captured
outputs for all six contract cases after normalizing only the fixture-path
line. Falsifier liveness: NC2 (below) proves the QC's pinned-target check
actually fails when it should.

### Duty 2 — baseline ledger + immediate arg1 source: PASS

The QC's own replay derived, from S = unknown ESP at 0x00528E76:

```text
0x00528E76  mov esi,ecx              ESP=S
0x00528E78  mov [S+0x10],esi         ESP=S      (only in-window memory write)
0x00528E7C  EAX := [S+0x44]          ESP=S
0x00528E80  ECX := [S+0x40]          ESP=S
0x00528E84  EDI := [S+0x3C]          ESP=S      <-- arg1 immediate producer
0x00528E88  push eax  -> [S-0x4]     ESP=S-0x4
0x00528E89  push ecx  -> [S-0x8]     ESP=S-0x8
0x00528E8A  push edi  -> [S-0xC]     ESP=S-0xC  <-- arg1 delivery (last push)
0x00528E8B  ECX := ESI (receiver)    ESP=S-0xC
0x00528E8D  CALL 0x0085B1B0          ESP=S-0x10 (return addr @ [S-0x10])
```

Derived: `ESP_BEFORE_CALL = S-0xC`; `ESP_AT_CALLEE_ENTRY = S-0x10`;
`ARG1_ENTRY_SLOT = [S-0xC]`; `ARG1_VALUE = MEM(S+0x3C)@0x00528E84`;
`ARG1_IMMEDIATE_SOURCE_OPERAND = DWORD [S+0x3C]`;
`REACHING_DEFINITION = IN_WINDOW_REACHING_DEFINITION_ESTABLISHED`
(the only in-window EDI definition, delivered by `push edi` @0x00528E8A);
receiver ECX:=ESI (value `ECX_ENTRY`, separate channel); the only in-window
memory write `[S+0x10]` does not alias the arg1 source slot `[S+0x3C]`; all
loads execute at ESP=S; UPSTREAM = UNRESOLVED_UPSTREAM by budget; PATH_SCOPE =
the examined straight-line path, no global uniqueness claim; ABI assumptions
stated (right-to-left pushes ⇒ last push = arg1; thiscall receiver in ECX;
callee entry conventions reused from prior pinned committed evidence — the QC
verified the citation against the committed W1 decode
(`mov eax,[esp+0x8]` @0x0085B1B0 = arg2; `mov edi,[esp+0x14]` @0x0085B1DA
after four pushes = arg1) — the callee body was NOT re-opened).

**AGREE with the executor field-by-field**: all 10 instructions (VA/bytes/
length/text), every ESP delta, push slots and values, arg1 chain, receiver,
mem write, entry slots, call target. `STACK_LEDGER.csv` machine-parsed and
matches the QC ledger exactly. Zero semantic differences.

### Duty 3 — six QC case outcomes: PASS (6/6)

| Case | QC verdict | QC discriminating result | Executor | Agree |
|---|---|---|---|---|
| BASELINE | BASELINE_QUALIFIED (24/24 checks) | original symbolic arg1 relation + receiver qualified | BASELINE_QUALIFIED | ✓ |
| M1_PUSH_ORDER | CONTROL_PASS | arg1 = push ecx @8A of MEM(S+0x40)@80 (def @0x528E80); arg2 = EDI value from [S+0x3C]; receiver ESI; EDI-source claim NOT retained | CONTROL_PASS | ✓ |
| M2_ESP_BEFORE_READ | CONTROL_PASS | 11 insns (28 B); loads at ESP=S-4 ⇒ EDI source [S+0x38]; ESP before CALL S-0x10; entry S-0x14; arg1 slot [S-0x10]; no mem writes | CONTROL_PASS | ✓ |
| M3_EDI_DEFINITION_REMOVED | CONTROL_PASS | arg1 = push edi with NO in-window def: UNRESOLVED_UPSTREAM, value EDI_ENTRY, in_window_def null; arg2 = ECX value from [S+0x3C] @84; receiver ESI | CONTROL_PASS | ✓ |
| M4_RECEIVER_ONLY | CONTROL_PASS | receiver ESI→EDI @8B; receiver value expression symbolically EQUAL to arg1's (NOT a numeric-inequality claim); arg1 + stack delivery exactly baseline; channels distinct | CONTROL_PASS | ✓ |
| M5_SOURCE_DISPLACEMENT | CONTROL_PASS | arg1 from [S+0x38]; deltas + receiver as baseline | CONTROL_PASS | ✓ |

Fixture identity convergence: all six QC-built fixtures are byte-identical
(SHA256) to the executor's recorded fixtures. Raw objdump outputs identical
(6/6, path-normalized). Full baseline facts comparison: **zero semantic
differences** (7 automated diffs are the QC's own uppercase-vs-lowercase
byte-string emission style). M1–M5 discriminating fields: **zero
differences**. Outcome accounting per contract §5: 6 cases ×
executor/QC = 12 analysis outcomes; cases ≠ outcomes; not 12 independent
implementations (the QC's outcomes are the other 6).

### Duty 4 — PASS records / pinned inputs: PASS

For every meaningful PASS the QC recorded MEASURED_QUANTITY,
SOURCE_OF_TRUTH, WHY_NON_CIRCULAR and FAILURE_CASE_DETECTED (see
`QC_RESULTS.json` §duty_4). Raw baseline and synthetic outputs were kept
separate (QC temp dir vs executor package evidence). No failed check was
encountered by the QC's own tooling; no QC repair rounds were needed. One
QC-side cosmetic disclosure (see F-QC-2).

### Duty 5 — executor-claims verification: PASS

- Window identity, objdump provenance/commands/raw outputs: VERIFIED.
- Baseline ledger (each instruction, each ESP delta, arg slots): VERIFIED.
- Six executor control outcomes (each discriminating field): VERIFIED 6/6.
- `ARG1_PROVENANCE.json` field completeness (executor-phase §10 subset):
  VERIFIED, including `SCIENCE_OUTCOME = ARG1_DIRECT_SOURCE_ESTABLISHED`
  coexisting with `UPSTREAM_PROVENANCE = UNRESOLVED_UPSTREAM`.
- PREREGISTRATION-before-science ordering: **CONSISTENT (documentary)** —
  PREREGISTRATION §7 expectations match the frozen contract §5 table
  verbatim; script expectations match PREREGISTRATION; mtimes corroborate
  (PREREGISTRATION 00:33:31 → INPUT_IDENTITIES 00:34:11 → helper last write
  00:47:31 → outputs 00:47:34). Honest limit: no trusted timestamp exists;
  ordering is corroborated, not cryptographically proven.
- Standing §8: carried verbatim token-by-token in PREREGISTRATION §10 and
  ARG1_PROVENANCE `standing_preserved`.
- **Repairs R1+R2 adjudicated HONEST**: R1 (instruction-length arithmetic)
  — the defect would fail-closed at the contiguity gate for every fixture and
  BLOCK before any output write; the repaired token-count is in the code; the
  note is accurate. R2 (reaching-definition resolution after the whole window)
  — would mis-attribute M1-arg1/M3-arg2 to the receiver `mov ecx,esi`
  @0x00528E8B; repaired to snapshot AT PUSH TIME; sub-repairs (hex-string
  VAs; [0,0,0]→['S','S','S'] form normalization) disclosed; no
  pre-registered expectation changed (they equal contract §5). The defective
  intermediate verdicts are preserved honestly IN THE NOTES (the defective
  output files were regenerated by the repaired third execution — disclosed;
  no failed evidence was edited into success).
- Process-residue disclosure VERIFIED: the typo'd stray placeholder path
  (`…12_WebGame\eudocracy-clean\…`, outside the repo) is confirmed GONE.

### Duty 6 — symbolic-provenance discipline: PASS

Different expressions do NOT prove unequal runtime values — stated in the
contract, PREREGISTRATION §7, and the package methodology, and the controls
test the PROVENANCE CLAIM, not a numeric inequality (M4's symbolic
expression-equality check carries the explicit "NOT a numeric inequality
claim" caveat; the QC reproduced exactly this). No mutant is claimed to
falsify the unmodified client; `falsifiers_triggered = []`;
`HISTORICAL_HYPOTHESIS_REJECTED` appears only in vocabulary/falsifier-semantics
contexts and is never claimed. FALSIFIER semantics per contract §5 preserved.

### Duty 7 — scope compliance: PASS

Only the authorized window read (+PE headers for mapping + whole-file
hashing); W3's first two bytes never read/decoded (DOC-1); no callee body
(callee conventions cited from prior pinned committed evidence, verified);
no upstream tracing (`[S+0x3C]` producer = UNRESOLVED_UPSTREAM); no
xref/RTTI/sibling/runtime work; budget all zeros except the one callsite;
CMO_C1 = CLOSED_FOR_AUDITED_STATE for e687eb1… carried; §8 list verbatim;
P3 backlog DOC-1..DOC-4 preserved; no J3 restoration. Package-wide token
scan: `WORLD_XYZ_RECOVERED=YES` occurrences **0**; transform-promotion
restoration **0**; semantic field promotions of arg1 (coordinate / model /
world / placement / record identity) **0** (all such tokens occur only as
budget zeros, standing lines, case names or explicit not-performed
declarations). Package census: 8 executor files, matching the dispatch.
No entrypoint write, no staging, no commit, no push by executor or QC.

### QC negative controls (QC-internal; NOT part of the 12 outcomes)

The contract's six cases never exercise the fail-closed path (the executor's
own F6 note says "unexercised by design"), so the QC exercised its own:

- **NC1_FAILCLOSED** — `cmpxchg` inside the window ⇒ analysis returned
  controlled FAIL_CLOSED (`unsupported mnemonic 'cmpxchg' @0x00528E7C`), no
  facts, no fabricated source ⇒ **NC_PASS_FAIL_CLOSED_LIVE**.
- **NC2_TARGET_MISMATCH** — one rel32 byte (0x1E→0x2E) ⇒ recomputed target
  0x0085B1C0 ≠ pinned 0x0085B1B0 ⇒ the QC's call-target check **FAILED as
  designed** (23/24 other checks still passed; internal recompute-vs-objdump
  consistency still true) ⇒ **NC_PASS_TARGET_FALSIFIER_LIVE** — the QC's
  predicate is falsifiable, not a rubber stamp.

## 3. Findings

- **F-QC-1 (P3, cosmetic reporting emission; non-load-bearing):** the
  executor's `register_definitions` list loses intermediate register
  definitions — `reg_order` stores register names only and the emission
  re-reads the final dict, so e.g. BASELINE shows ECX@0x00528E8B twice and
  never shows the ECX load @0x00528E80 (M3 mislabels all three ECX entries).
  No verdict, check or claim depends on this field; the load-bearing fields
  (arg records, push-time def snapshots, loads[], mem writes, STACK_LEDGER)
  are all correct. Optional future correction only (needs a new human
  decision). Revalidation predicate: re-run and confirm every definition event
  appears with its own def_va.
- **F-QC-2 (P3, QC-side disclosure only):** (a) the QC's NC1 fixture
  description string says `cmpxchg bl,al` while objdump prints
  `cmpxchg al,bl` (Intel destination-first) — the trigger keys on the
  mnemonic, no impact; (b) the QC emits byte strings uppercase where the
  executor preserves objdump lowercase — pure emission style, recorded so the
  7 automated comparison diffs are not misread as disagreements.

No material findings. No executor artifact was modified by the QC.

## 4. Coverage / NOT_CHECKED

- FULL_READ (to EOF): all 8 package files (PREREGISTRATION 283 L;
  INPUT_IDENTITIES 171 L; WINDOW_IDENTITY 54 L; CALLSITE_DISASSEMBLY 25 L;
  STACK_LEDGER 26 L; ARG1_PROVENANCE 213 L; CONTROLS_RESULTS 4573 L;
  run_stack_controls.py 1332 L) + the frozen contract (263 L).
- Recomputed from raw: window bytes/SHA, PE mapping, instruction stream
  (own decode + byte cross-validation), full symbolic ledger, all six case
  signatures/outcomes, fixture SHAs, EXE identity before/after, all §2 input
  identities (+ git blob equality).
- NOT_CHECKED (honest limits): the executor's fail-closed path was NOT
  re-executed through the executor's script (running it would regenerate the
  frozen package outputs); it was verified by full code read + the executor's
  honest F6 disclosure, with analogous liveness demonstrated on the QC's own
  replay (NC1). PReregistration-before-science ordering is corroborated
  (mtime + content + execution history), not cryptographically proven. The
  executor's defective intermediate executions exist only as honest textual
  disclosures. No cross-implementation disassembler QC (same objdump 2.44).
  AUDIT_ENTRYPOINT.md: identity + two governance lines spot-checked
  (census-level, not full read). Remote publication is not a QC-phase item.

## 5. Verdict

**QC_PASS.** All QC duties hold on the QC's own independent measurements; the
executor's evidence is accurate, honest and scope-compliant; both findings are
P3 and non-material. This verdict is internal QC only — it is not
MASTER_ACCEPTED, not milestone closure, not qualification, and not a
publication action. The independent Desktop post-audit remains NOT_PERFORMED.
SCIENCE_OUTCOME (ARG1_DIRECT_SOURCE_ESTABLISHED, coexisting with
UNRESOLVED_UPSTREAM) and QC_VERDICT remain separate. NEXT_EXPERIMENT_AUTHORIZED
= NO. HARD_STOP = YES for this phase; persistence/report/entrypoint/manifest/
commit/push remain the parent's later phases under the frozen contract §9.
