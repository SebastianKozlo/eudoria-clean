# HANDOFF — P01 (Etap A: adapter 006C29D0) → PE-MASTER

RUN_ID: PE_935_PAIR_REDUCER_CONSUMER_SAVED_R2_20261019 | PACKAGE: P01 | MODE: SAVED_ONLY_NO_NESTED_TASKS
RUN_STATUS: COMPLETE_WITHIN_ASSIGNED_SCOPE (no seal by worker; parent checks/seals)

## Deliverables (package root)

- REPORT.md — full analysis, Q1–Q6, axes, budgets, SELF_CHECK
- CLAIMS.json — 17 claims (A01–A17) with labels + VA anchors + assumptions
- STACK_MAP.md — full ESP balance E0→E0+0x14, slot map, SEH frame, caller-side S-map
- FLOW.md — control/data flow, value graph E1–E15, dead-argument controls, axes
- PREMISES.json — P1–P9 (ABI, nonvolatile, closed-lemma reuse, alias census)
- COUNTERS.json — actual budgets + 9-call census + question status
- STAGE_ACCEPTANCE_GATES.csv — 20 gates evaluated
- artifact_index.csv — artifact navigation
- RUN_STARTED.json — run binding (real UTC timestamps; source pin re-verified)

## Per-question status

1. **ABI** CONFIRMED: thiscall (ECX=this, no EDX arg), 4 stack args, callee cleans RET 0x10, 32-bit EAX return.
2. **this reads** CONFIRMED: this = &ctx[2] inside the copied context; fields [this]=ctx[2]→receiver base, [this+4]=ctx[3]→ctor-D arg, [this+8]=ctx[4]→ctor-B arg, [this+0xC] byte=ctx[5] lo→arg3 slot patch. arg3 = pointer-holder, deref level 1 → pair_ptr (level 2 total); arg1/arg4 DEAD.
3. **0x00823C10** mechanism CONFIRMED: `CALL EAX @006C2A63`, target = M32[arg2] = ctx[0] = 0x00823C10 (value STRONGLY_SUPPORTED via closed prior + no-alias census); receiver ECX = ctx[1]+ctx[2] = 0 + 00415670_result; args = (pair_ptr, &local_D, &local_B, (S+0x10) low-byte-tagged 1); pump cleans 16 bytes. C6 resolved by body proof (recorded, not silently promoted).
4. **Return origin** CONFIRMED: pump call → ESI @006C2A69 → EAX @006C2A99 → RET 0x10; SINGLE normal path (zero branches); kind NOT_ESTABLISHED (pump unopened). Exceptional: SEH 0xA04804 unwind only, no EAX contract.
5. **Effects**: visible = SEH states, FS install/restore, one byte into own arg3 slot; NO store to 0xBA45E8/pairs/context. 9 opaque callees preserved UNKNOWN (C5). Partial-store resolved: only byte 0 of ctx[5] consumed → pump arg4 exactly (S+0x10)&~0xFF|1; C3 upper bits never read here.
6. **Containment** CONFIRMED: byte-contiguous (66/66 deltas = encoding lengths), RET ends 006C2AAF < 006C2AB0; zero JMP/Jcc; SEH handler data-referenced only; no branch escapes; **no new in-window admission needed**.

## Boundaries / missing edge (parent decides next admission)

- **PRIMARY NEXT EDGE**: body of **0x00823C10** (the pump) — producer of the returned/appended value. Needed for: return-kind (id/handle/pointer), DATA_DOMAIN, world-instance qualification. Suggested question: "reconstruct ABI + return origin of 0x00823C10 with receiver = 00415670_result and args (pair_ptr, wrapper2, wrapper1, tagged-slot-ptr)"; range from 0x00823C10 to first RET-class boundary; same source (SAVED_TEXT_CATALOG pin 642CC29A…D8DB).
- Secondary: **0x00415670** (receiver producer; no visible register setup at callsite @006C4100 in closed prior window — likely thiscall with leftover ECX or argless); targets of globals **0xA75A38/0xA75A44** (wrapper ctors; would classify wrapper class + role of constant 0xA7957B).
- Etap B per parent plan (consumer 006C4060 continuation) unaffected by P01.

## Budgets consumed (actual, no refund)

bodies 3/3 charged (1 unique owner recognized: 006C29D0); candidates 3/3 charged (0 opened; 4 nominated); rows 67/6000; calls 9/200; document lines 0/1500; INCIDENT_DEBIT 0. Closed priors read-only (P06/P07, P10, STACK_REDERIVATION, postaudit REPORT, CORRECTIONS_APPLIED); no source/config/original-game/Ghidra/runtime/Hermes operations; no nested tasks.

## Honesty statement

Return-value kind, wrapper class identity, pump semantics, DATA_DOMAIN and WORLD_INSTANCE_RELATION are NOT established and are labeled as such; opaque effects remain UNKNOWN per C5. No PASS was written for package structure alone; gates reflect evidence. HARD STOP at assignment boundary — the parent run remains open.
