# HANDOFF — P02 (Etap B: consumer 006C4060 continuation) → PE-MASTER

RUN_ID: PE_935_PAIR_REDUCER_CONSUMER_SAVED_R2_20261019 | PACKAGE: P02 | MODE: SAVED_ONLY_NO_NESTED_TASKS
RUN_STATUS: COMPLETE_WITHIN_ASSIGNED_SCOPE (no seal by worker; parent checks/seals)

## Deliverables (package root)

- REPORT.md — full analysis Q1-Q7, axes, budgets, SELF_CHECK
- CLAIMS.json — 23 claims (B01-B23) with labels + VA anchors + assumptions
- STACK_MAP.md — full ESP balance E1→E1+4 of 006C4060: prolog/epilog mirror, deferred-cleanup ledger, all [ESP+x] anchored, SEH states, call frames
- FLOW.md — control flow + value graph V1-V16 (source table entry → pair in C → adapter → EAX → global element → first real use V12) + negative controls
- PREMISES.json — P1-P10 (listing contract, nonvolatile ABI, cdecl premises, 006C2C50 callee-clean premise with 3 falsifiers, opaque-callee contract premises P6/P7, C5/C6 compliance)
- COUNTERS.json — actual budgets + 3-call census + deferred ledger + question status
- STAGE_ACCEPTANCE_GATES.csv — 22 gates evaluated
- artifact_index.csv — artifact navigation
- RUN_STARTED.json — run binding (real UTC; extract sha256 verified)

## Per-question status

1. **Full normal path & closure** CONFIRMED: prolog→collect(×3)→ADD ESP,0x28→sort→dedupe-scan→cond. 006C2C50→ctx build→006C36B0 projection (per-pair adapter→pump→DWORD append to global)→global read→008D6D90→ADD ESP,0x38→fix-up (3 cases)→C dealloc→epilog→**RET @006C41F0**. Body CLOSED; all 8 branches in-window; byte-contiguous (144 rows, 143 deltas = encodings; seams 5 and 8 verified). No exit escapes. Callee bodies separate; 006C36B0's own epilogue still a prior-run open edge.
2. **Global pair** CONFIRMED vector semantics: header in .data {begin@0x00BA45E8, tail@0x00BA45EC, limit@0xBA45F0}, DWORD elements: range-pair args to 008D6D90 @006C415C/415D; one-past-end bound @006C418E; append tail+=4 (prior @006C36F8); **reload @006C4192** (loop path only — tail is shared mutable state, opaque callee may advance it); **write @006C41AE**. GLOBAL_ELEMENT_KIND: 32-bit; only zero-vs-nonzero interpreted in-window; pointer/handle/id kind **NOT_ESTABLISHED**; zero = removable/empty (mechanism level).
3. **Loop @006C4180-4190** CONFIRMED: forward in-place compaction of [ret+4, tail_snapshot) into positions from ret; ECX read cursor (+4 always), EAX write cursor (+4 only on copy); drop iff value==0; **element at returned position dropped unconditionally**; NOT established: any other value interpretation (never deref'd as pointer/compared as id — census B08), meaning of zero, no bounds guard (premise P6), zeros before the returned position are NOT removed.
4. **CALL [0xA753B4]**: 3-arg cdecl (dst=EAX, src=EDI, count=ESI) block-copy fix-up relocating the 008D6D90-appended block down; memmove-class structural match **STRONGLY_SUPPORTED** (incl. return-dst dependence: ADD EAX,ESI then tail store only coher if callee returns dst); memmove identity **PLAUSIBLE** (target unopened). **[0x00BA45EC]=EAX is NOT allocation growth**: tail bookkeeping after compaction+relocation; begin/limit untouched; no allocation in-window.
5. **008D6D90** OPAQUE (in-window contract CONFIRMED: args (begin, tail, &slot=0, &wrapper); return consumed as array position; may append — reload exists); best-fit hypothesis find-first-zero **PLAUSIBLE only**. **[0x00A759FC](M32[C], (M32[C+8]−M32[C])&~7)**: dealloc-class role **STRONGLY_SUPPORTED** (C+8=limit proven cross-window from P03 append; allocated-size argument; skip-if-null guard; single epilog-time call); identity (sized delete / custom free) **PLAUSIBLE**. **[ESP+0x40]=−1**: SEH state slot reset (E1−0x04) — MSVC epilog idiom, NOT a data flag.
6. **Neighbors**: 006C4200 (complete: returns ([ECX]!=0); identity NOT_ESTABLISHED) and 006C4210 (partial: this+0x88:=arg1, [arg1], [+0x44]; cut at 006C4220) — **marked, not interpreted**.
7. **Deferred cleanup** fully accounted: ADD ESP,0x28 = 5×2 args (byte-exact); ADD ESP,0x38 = ctx+4+4 args (byte-exact, both paths **iff 006C2C50 callee-clean RET 0xC** — premise P4 with 3 independent falsifiers: the 0x38 sum, the [ESP+0x38] reads @006C4121/4136, the [ESP+0x50] store @006C415E); immediate ADD ESP,0xC/0x8; epilog POP ECX/EDI/ESI/EBP/EBX + ADD ESP,0x30 = exact prolog mirror (0x14+0x30=0x44); RET @006C41F0. Cookie popped into ECX, discarded — NO /GS check visible.

## Boundaries / missing edges (parent decides next admission)

- **PRIMARY**: **0x008D6D90** body — what it computes over the global range; whether it derefs element VALUES (the only place DATA_DOMAIN could advance from these windows); its append behavior (resolves the reload/relocation purpose); falsifies/confirms find-first-zero.
- [0x00A753B4] / [0x00A759FC] targets (memmove / sized-free identity).
- 006C2C50 body (closes premise P4 into fact).
- 006C36B0 epilogue [006C3720,006C3740) (closes its normal-exit/empty-case; also premise P3 for that callee).
- 0x00823C10 pump (P01's primary nomination — producer of element values; still the only bridge candidate toward any domain/instance semantics).

## Mission-relevant summary

Etap B closes the 006C4060 body and the "first real use" question: after the projection fills the global DWORD list, the visible continuation is **container maintenance** (opaque range query → erase returned position + drop zeros → relocate any callee-appended block → tail update → local buffer dealloc). **No element is interpreted as an id/pointer/handle in any admitted window** — DATA_DOMAIN not advanced; no world/transform edge. The chain remains: static id tables → pairs in C → sort/dedupe → pump projection → global DWORD list → maintenance. The MODEL_RESOURCE→WORLD_INSTANCE bridge would have to live inside the pump 00823C10 or beyond — both unopened.

## Budgets consumed (actual, no refund)

bodies 4/4 charged (3 visible: 006C4060 continuation + 006C4200 + 006C4210-partial; 3 ≤ 4 reserved, no incident); candidates 3/3 charged, 0 opened, 6 nominated; rows 62/6000 (new; 82 prior rows + 67 P01 rows consulted read-only, charged to their runs); CALL sites 3/200; document lines 0/1500; INCIDENT_DEBIT 0. Closed priors read-only; no source/config/original-game/Ghidra/runtime/Hermes operations; no nested tasks.

## Honesty statement

GLOBAL_ELEMENT_KIND, DATA_DOMAIN, meaning of zero, 008D6D90 semantics, [0xA753B4]/[0xA759FC] identities, and any world-instance relation are NOT established and are labelled as such. The 006C2C50 callee-clean conclusion is a labelled premise (STRONGLY_SUPPORTED, 3 falsifiers), not a body-read fact. Opaque effects remain UNKNOWN per C5; the tail reload is reported as an H2-compatible shape without claiming any enqueue occurs. No PASS was written for package structure; gates reflect evidence. HARD STOP at assignment boundary — the parent run remains open.
