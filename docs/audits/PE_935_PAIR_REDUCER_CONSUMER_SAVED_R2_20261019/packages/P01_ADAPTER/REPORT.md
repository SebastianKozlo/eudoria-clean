# P01 — Etap A: adapter 006C29D0 (SAVED-ONLY)

RUN_ID = PE_935_PAIR_REDUCER_CONSUMER_SAVED_R2_20261019 | PACKAGE = P01 | WORKER = pe-reconstruction
Admission: A81d30fbf331a | Extract: P01_EXTRACT, 67 rows, [006C29D0,006C2AB0), sha256 156C26F6B81F740D2C8DBE8A0F8B45842E48C4591A16CA1C9C559EEBE60C28AB (verified)
Source pin (re-verified by worker): GHIDRA_H5_VTABLE2.txt, sha256 642CC29A01B8AD6F783E82E14DA4A61FA00BA6A3EC6DF98EDFF28AC25CC1D8DB, 50780146 B.
Corrections C1..C8 assimilated before analysis (CORRECTIONS_APPLIED.json). Closed priors used read-only: P06/P07 (006C4060), P10 (006C36B0), STACK_REDERIVATION.json, postaudit REPORT.md.

RUN_STATUS = COMPLETE_WITHIN_ASSIGNED_SCOPE (HARD STOP at assignment boundary; parent run not closed)

## 0. Executive result

006C29D0 is a **bound-functor invoker ("pair reducer adapter")**: it builds two opaque wrapper objects from the same constant 0xA7957B, reads the current pair pointer through the arg3 pointer-holder, and calls **ctx[0] (= 0x00823C10, the pump)** on receiver `ctx[1]+ctx[2]` (= 0 + result of 00415670) with four stack arguments `(pair_ptr, &wrapper2, &wrapper1, (S+0x10) with low byte 1)`. **The returned EAX is the pump's return value and nothing else** — there is exactly one normal path (zero branches in the whole body). The C6 caution is now resolved by body proof: the literal 0x00823C10 **is really executed** as the call target (mechanism CONFIRMED in-window; value STRONGLY_SUPPORTED from the closed-prior context construction plus a no-aliasing-writer census). No world-instance or transform edge exists in this window; the appended-value semantics live inside the pump, which remains unopened.

## 1. Q1 — ABI (CONFIRMED)

- **Convention**: ECX-this thiscall. Receiver = ECX (`MOV ESI,ECX` @006C29F5). EDX is **not** an argument register (scratch only; caller's EDX value never read before first overwrite @006C2A37).
- **Stack args**: 4 (`RET 0x10` @006C2AAC ⇒ callee cleans 16 bytes; caller pushes exactly 4 DWORDs @006C36C3/C9/CE/D8 and performs no post-call `ADD ESP` — cross-evidence from closed prior P10).
- **Arg roles at entry** (E0 = entry ESP):
  - arg1 [E0+4] = begin&0xFFFFFF00 (caller zeroed its low byte @006C36CF) — **DEAD, never read**;
  - arg2 [E0+8] = S+0x14 = &ctx[0];
  - arg3 [E0+0xC] = S+0x10 = **pointer-holder** to the cursor slot containing the current pair pointer (C4);
  - arg4 [E0+0x10] = 0 — **DEAD, never read**.
- **Return**: 32-bit EAX; origin = pump call (see §4). No EDX:EAX pair, no secondary return register.

## 2. Q2 — reads of `this` (ECX = S+1Ch) (CONFIRMED)

`this` is not a heap object: it is **&ctx[2]**, i.e. an address inside the caller-copied 6-DWORD context. Exactly four DWORD fields are read through it, all unconditionally executed:

| Field | = | Read at | Used as |
|---|---|---|---|
| [this] | ctx[2] = 00415670_result | 006C2A3D (MOV ESI,[ESI]) | receiver base addend (ADD ECX,ESI @006C2A5C) |
| [this+4] | ctx[3] = 0xA7957B | 006C2A24 (MOV ECX,[ESI+4]) | 1st stack arg of ctor-D (PUSH ECX @006C2A28) |
| [this+8] | ctx[4] = 0xA7957B | 006C2A08 (MOV EAX,[ESI+8]) | 1st stack arg of ctor-B (PUSH EAX @006C2A0B) |
| [this+0xC] low byte | ctx[5]&0xFF = 1 (C3) | 006C2A34 (MOV CL,[ESI+0xC]) | patch byte written into own arg3 slot @006C2A3F |

No other dereferences of `this`. Register chains from load to use verified row-by-row (no redefinitions in between).

**Arg3 pointer levels**: arg3 is dereferenced exactly once at level 1 (`pair_ptr = M32[M32[arg3]]`, @006C2A37/3B) — pair_ptr = M32[S+0x10] = the current pair address (caller EDI, stored @006C36DD). The pair is **not** read field-by-field in this window; only its address is forwarded to the pump.

## 3. Q3 — context words; is 0x00823C10 really called? (mechanism CONFIRMED; value STRONGLY_SUPPORTED)

The callee reads **all six** context words:

| Word | At | Value (closed priors) | Role |
|---|---|---|---|
| ctx[0] [S+0x14] | 006C2A5A (EAX=M32[arg2]) | **0x00823C10** | **CALL TARGET** @006C2A63 |
| ctx[1] [S+0x18] | 006C2A57 (ECX=M32[arg2+4]) | EDI of 006C4060 = 0 (XOR EDI,EDI @006C4087 + nonvolatile premise) | receiver adjustor |
| ctx[2] [S+0x1C] | 006C2A3D (= [this]) | 00415670_result | receiver object |
| ctx[3] [S+0x20] | 006C2A24 | 0xA7957B | ctor-D arg1 |
| ctx[4] [S+0x24] | 006C2A08 | 0xA7957B | ctor-B arg1 |
| ctx[5] [S+0x28] low byte | 006C2A34 | 1 (C3) | low-byte tag for pump arg4 |

**Pinned call** — `CALL EAX @006C2A63`:
- **target** EAX = M32[arg2] = ctx[0] = **0x00823C10**;
- **receiver** ECX = M32[arg2+4] + M32[this] = ctx[1]+ctx[2] = 0 + 00415670_result (ADD ECX,ESI @006C2A5C);
- **args** (push order @006C2A47→52, last push = first arg): `(pair_ptr, &local_D, &local_B, patched_slot)` where `patched_slot = (S+0x10)&0xFFFFFF00 | 1`;
- **callee cleans 16 bytes** (post-call depth arithmetic: `LEA ECX,[ESP+0x10]` @006C2A65 resolves to local_D only if the pump removed its 4 args).

Mechanism is CONFIRMED in-window. The target **value** 0x00823C10 comes from the closed prior (MOV ESI,0x823C10 @006C40FB; store @006C410C) plus a visible-census: no pointer into the context block is handed to any opaque callee, and the window contains no writer to S+0x14 between copy and call. Residual opacity (opaque callees writing through unshared global aliases) cannot be excluded without opening them ⇒ STRONGLY_SUPPORTED, not runtime-CONFIRMED. **This resolves C6 for the mechanism** (no assumption was made before the body proof; the proof now exists). Per contract §5: same target ≠ same object/model — no identity transfer from any historical "pump" analysis; noted only that the historical pump-ABI correction ("four DWORDs, not three") is **numerically consistent** with the four stack args here (PLAUSIBLE echo, no identity claim).

## 4. Q4 — return origin; normal and exceptional paths (CONFIRMED)

- **Producer**: `CALL EAX @006C2A63` → `MOV ESI,EAX @006C2A69` → (4 cleanup calls; ESI untouched) → `MOV EAX,ESI @006C2A99` → `RET 0x10 @006C2AAC`.
- **All normal EAX paths**: exactly **ONE**. The window has **zero** JMP/Jcc (mnemonic census over 67 rows), so no zero-return/alternate/bit-pattern path exists; ctor/dtor return values (except ctor-A/C results feeding ctor-B/D) are discarded. The returned EAX is the pump's EAX, unmodified.
- **Return-value KIND** (id/handle/pointer/bit-pattern): **NOT_ESTABLISHED** — the pump body is unopened (Q-edge in §6). Caller side (closed prior P10) appends it as a raw DWORD to the global container {begin@0xBA45E8, tail@0xBA45EC, limit@0xBA45F0}, which does not constrain its semantics.
- **Exceptional exits**: SEH frame installed @006C29EF (handler **0x00A04804** data-pushed @006C29D2; states −1→0→2→3→2→0). Any exception inside the 9 indirect callees (or a fault on loads/stores) dispatches to 0xA04804 (body outside window; scopetable opaque) → unwind destructors by state → propagate. Caller 006C36B0 shows no handler in its admitted window. **No EAX-return contract exists on the exceptional path.**

## 5. Q5 — visible vs opaque effects; partial-store pattern (CONFIRMED / PRESERVED_UNKNOWN)

**Visible stores (complete census)**: SEH state slot [E0−4] (@006C2A10 dword 0; @006C2A2D/5E/6B/84 bytes 2/3/2/0); FS:[0] install/restore (@006C29EF/@006C2A9F); **one byte store into the own incoming-arg3 slot** @006C2A3F (`M8[E0+0xC] := ctx[5]&0xFF`); push/pop frame writes. **No store to 0xBA45E8, no store to the pair array, no store to the context block.**

**Partial-store pattern resolved inside the adapter**: the callee consumes only **byte 0** of ctx[5] and writes only byte 0 of its arg3 slot; bytes 1–3 of that slot retain the original arg3 value (S+0x10), so pump arg4 is **exactly** `(S+0x10)&0xFFFFFF00 | 1`. The C3 undefined upper 24 bits of ctx[5] are **never read by this body** — the partial DWORD introduces no ambiguity in the adapter's mechanism (its semantics remain unknown: what the pump does with the tagged stack pointer is opaque).

**Opaque (targets unopened, effects UNKNOWN per C5)** — all 9 indirect calls:
| Target | Sites | Role (structural) |
|---|---|---|
| M32[0x00A75A38] | 006C29FB, 006C2A1E | ctor of helper objects local_A (E0−0x3D) / local_C (E0−0x3E), 0 stack args; results feed ctor-B/D as arg2 |
| M32[0x00A75A44] | 006C2A18, 006C2A32 | ctor of wrappers local_B (E0−0x24) / local_D (E0−0x3C), thiscall, args (0xA7957B, helper-result) |
| M32[0x00A75A5C] | 006C2A70, 006C2A89 | dtor of local_D / local_B |
| M32[0x00A75A40] | 006C2A7A, 006C2A93 | dtor of local_C / local_A |
| ctx[0]=0x00823C10 | 006C2A63 | **the pump — value producer** |

The two wrappers are built from the **identical** constant 0xA7957B via structurally identical call pairs; their addresses are passed to the pump as args 2 and 3. Wrapper class identity: **UNKNOWN** (no vptr/runtime proof; per contract §5 no substitution). H1/H2 disjointness not asserted; request/queue effects of the pump remain possible (postaudit countermodel stands).

## 6. Q6 — containment & the next edge (CONFIRMED)

- **Byte-contiguity**: all 66 inter-row deltas equal the x86 encoding lengths of the preceding instructions (dual check: manual encoding derivation + programmatic delta extraction). The 67 rows tile [006C29D0, 006C2AAF] with **zero gaps**; RET 0x10 @006C2AAC ends at 006C2AAF.
- **Window remainder**: the single byte [006C2AAF, 006C2AB0) has no listing row (not an instruction start) and is unreachable by fall-through (RET is a control transfer) ⇒ padding; next function presumably at 006C2AB0 (region end).
- **No escape**: zero JMP/Jcc; all control transfers are the 9 indirect CALLs (opaque targets outside the window — separate bodies, each requiring its own admission) and the final RET. The SEH handler 0xA04804 is **data-referenced**, never executed by normal flow. **Complete executable range of the visible body is inside the window; no in-window continuation admission is needed.**
- **PRECISE NEXT EDGE (parent decides)**: body of **0x00823C10** (the pump) — the producer of the returned/appended value; expected window ~[0x00823C10, next RET-class boundary], same source. Secondary: **0x00415670** (receiver object producer, called @006C4100 with no visible register setup in the closed prior window), and the targets behind globals 0xA75A38/0xA75A44 (wrapper constructors; would identify the wrapper class and the role of 0xA7957B, plausibly a rdata constant).

## 7. Axes (per C5)

- LOCAL_MECHANISM: **CONFIRMED** (functor invocation as reconstructed in §0–§5; STACK_MAP/FLOW give the full ESP balance).
- DATA_DOMAIN: pairs = 8-byte elements of the shared C list (closed prior: collect from static ID arrays → sort → dedupe); "compile-time resource dependencies" remains a hypothesis (postaudit §4). Pump return kind NOT_ESTABLISHED.
- OPAQUE_EFFECTS: **UNKNOWN** (all 9 callees; C5 preserved).
- WORLD_INSTANCE_RELATION: **NONE established** in this window (negative result within scope; the pump is the only candidate bridge).

## 8. Budgets and counters (actual)

| Resource | Reserved | Recognized/used | Charged (no refund) | Cap (run) |
|---|---|---|---|---|
| bodies | 3 (ADMIT) | 1 unique owner (006C29D0); 0 extra bodies in window | 3 | 32 |
| candidates | 3 (ADMIT) | 0 opened; 5 nominated for next admission (pump, 00415670, [0xA75A38], [0xA75A44], dtors low-priority) | 3 | 32 |
| listing rows | — | 67 | 67 | 6000 |
| CALL sites | — | 9 | 9 | 200 |
| body document lines | — | 0 | 0 | 1500 |
| INCIDENT_DEBIT | 0 | — | 0 | — |

No unexpected body; no PARTIAL_NONCOMPLIANT; no refund claimed. Extract sha256 verified; source pin re-verified. Reads outside the extract limited to explicitly authorized closed priors (P06/P07, P10, STACK_REDERIVATION, postaudit REPORT, CORRECTIONS_APPLIED) — read-only, no modifications. No original-game/runtime/Ghidra operations, no nested tasks, no config changes, no Hermes.

## 9. SELF_CHECK (worker-level, not independent MASTER audit)

- [x] Extract SHA256 matches contract (156C26F6…28AB) and admission header; source pin re-verified byte-for-byte (642CC29A…D8DB, 50780146 B).
- [x] Full raw census: 67/67 rows read and individually analyzed; 66/66 VA deltas explained; 9/9 CALL sites classified.
- [x] Every [ESP+x] reference in the window accounted (STACK_MAP §5); zero unexplained offsets; epilog arithmetic balanced E0→E0+0x14 and cross-checked against caller (no ADD ESP @006C36E6).
- [x] Negative controls: dead args proven by exhaustive offset census (A02); single-path return proven by mnemonic census (A09); no-writer alias census for the pump target (A06/P6); no store to the sink global in the callee (A12).
- [x] C1–C8 preserved; C3 resolved within the adapter (byte-0-only consumption, A13); C6 resolved to CONFIRMED-mechanism by body proof, recorded as correction-conflict resolution, not silent promotion.
- [x] No default-success: return-kind and world-relation reported NOT_ESTABLISHED; opaque effects kept UNKNOWN.
- [x] Counters honest: 3/3 bodies charged (no refund despite 1 unique owner); 3/3 candidates charged; 67 rows, 9 calls; INCIDENT_DEBIT=0.
- [x] Scope: no body outside the extract opened; closed priors read-only; HARD STOP at assignment boundary.
