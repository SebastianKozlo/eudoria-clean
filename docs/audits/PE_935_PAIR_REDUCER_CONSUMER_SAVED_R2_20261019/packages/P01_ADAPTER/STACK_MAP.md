# STACK_MAP — 006C29D0 (adapter, Etap A, P01)

Source: P01_EXTRACT (67 rows, [006C29D0,006C2AB0), admission A81d30fbf331a, sha256 156C26F6B81F740D2C8DBE8A0F8B45842E48C4591A16CA1C9C559EEBE60C28AB).
Caller map reconstructed from CLOSED prior sources (read-only, cited): P10_SINK_R1 WINDOW_006C36B0.txt (caller body), P06_CONSUMER_R1 WINDOW_006C4057.txt + WINDOW_006C40E0.txt (context construction + outgoing args), STACK_REDERIVATION.json (postaudit), CORRECTIONS_APPLIED.json C2/C3/C4.

Notation:
- `S`  = ESP at entry to caller 006C36B0 (postaudit convention; [S]=return address of 006C36B0).
- `E0` = ESP at entry to callee 006C29D0 (=[S-0x20] at the moment CALL 006C29D0 @006C36E1 pushes its return address).
- All offsets hex. `M32[x]`/`M8[x]` = 4/1-byte memory at x. `ctx[i]` = i-th DWORD of the 6-DWORD context copied by value by 006C4060 (ctx[0] at S+0x14 … ctx[5] at S+0x28).

## 1. Caller side (006C36B0) — S-frame, from closed priors

| Slot | Value | Written at | Note |
|---|---|---|---|
| [S+0x00] | return address of 006C36B0 | — | |
| [S+0x04] | arg1 = &out (LEA ECX,[ESP+0x3C] @006C413C, caller 006C4060) | 006C4140 PUSH ECX | out-slot for container pointer |
| [S+0x08] | arg2 = begin of pair array (M32[T+0x34] @006C4136) | 006C413B PUSH EAX | low byte zeroed @006C36CF before callee-arg1 push |
| [S+0x0C] | arg3 = end of pair array (M32[T+0x38] @006C4121) | 006C413A PUSH EDX | EBP in 006C36B0 (@006C36B1) |
| [S+0x10] | arg4 = **0x00BA45E8** (literal sink global) | 006C412E PUSH | read into ESI @006C36BF (C2); slot REUSED as cursor slot @006C36DD (M32[S+0x10]=EDI=current pair ptr, C4); reused again as result temp @006C36EC |
| [S+0x14] | ctx[0] = **0x00823C10** | 006C410C MOV [EAX],ESI (ESI=0x823C10 @006C40FB) | |
| [S+0x18] | ctx[1] = EDI of 006C4060 = **0** | 006C410E MOV [EAX+4],EDI | EDI=0 since XOR EDI,EDI @006C4087; nonvolatile premise |
| [S+0x1C] | ctx[2] = **EAX of CALL 00415670 @006C4100** | 006C4116 MOV [EAX+8],EBX | opaque producer; **= callee this** (ECX=S+0x1C) |
| [S+0x20] | ctx[3] = **0xA7957B** | 006C411B MOV [EAX+0xC],ECX | |
| [S+0x24] | ctx[4] = **0xA7957B** | 006C411E MOV [EAX+0x10],EDX | same value as ctx[3] |
| [S+0x28] | ctx[5] = M32[B+0x34], low byte = **1** | 006C4125 MOV byte [ESP+4C],1; 006C4133 MOV [EAX+0x14],EBP | C3: upper 24 bits not fixed by admitted stores |

Loop iterations: EDI = begin; while EDI != end: cursor slot [S+0x10] = EDI; CALL 006C29D0; fast-path append of returned EAX to global container {begin@0xBA45E8, tail@0xBA45EC, limit@0xBA45F0}; EDI += 8.

## 2. Call setup at 006C36E1 (caller pushes, last push = lowest address)

| ESP after push | Pushed value | Callee-side role |
|---|---|---|
| S-0x10 | 0x0 (PUSH 0 @006C36C3) | callee arg4 = 0 — **DEAD (never read)** |
| S-0x14 | S+0x10 (LEA EAX,[ESP+0x20] @006C36C5 → PUSH EAX @006C36C9) | callee arg3 = **pointer-holder** = &cursor-slot (C4) |
| S-0x18 | S+0x14 (LEA ECX,[ESP+0x28] @006C36CA → PUSH ECX @006C36CE) | callee arg2 = &ctx[0] |
| S-0x1C | M32[S+8] & 0xFFFFFF00 (M8[S+8]=0 @006C36CF; MOV EDX,[ESP+0x20] @006C36D4; PUSH EDX @006C36D8) | callee arg1 = begin with low byte zeroed — **DEAD (never read)** |

ECX at CALL = S+0x1C (LEA ECX,[ESP+0x38] @006C36D9) = callee this = **&ctx[2]**.

## 3. Callee frame (E0 = S-0x20) — prolog (SEH + nonvolatile + cookie)

| ESP | Instruction | Slot written | Role |
|---|---|---|---|
| E0-0x04 | PUSH -0x1 @006C29D0 | [E0-4] = -1 | SEH state slot (ehstate) |
| E0-0x08 | PUSH 0xA04804 @006C29D2 | [E0-8] = 0x00A04804 | SEH handler |
| E0-0x0C | MOV EAX,FS:[0]; PUSH EAX @006C29DD | [E0-0xC] = previous FS:[0] | SEH next |
| E0-0x40 | SUB ESP,0x34 @006C29DE | [E0-0x40..E0-0xD] = locals (0x34 B) | local objects (see §4) |
| E0-0x44 | PUSH ESI @006C29E1 | [E0-0x44] = caller ESI (0x00BA45E8) | nonvolatile save |
| E0-0x48 | PUSH EDI @006C29E2 | [E0-0x48] = caller EDI (current pair ptr) | nonvolatile save |
| E0-0x4C | MOV EAX,[0x00B9D8D0]; XOR EAX,ESP; PUSH EAX @006C29EA | [E0-0x4C] = cookie^ESP | security cookie; **popped and discarded @006C2AA6; NO validation check visible in window** |

FS:[0] ← E0-0xC (LEA EAX,[ESP+0x40] @006C29EB with ESP=E0-0x4C → E0-0xC; MOV FS:[0],EAX @006C29EF). SEH record = {next@E0-0xC, handler@E0-8, state@E0-4}. Restored @006C2A9B (MOV ECX,[ESP+0x40] → M32[E0-0xC]) + MOV FS:[0],ECX @006C2A9F.

**Base depth of the body: ESP = E0-0x4C** (all [ESP+x] references below are given at the depth valid at that instruction).

## 4. Callee locals (this-pointers of the 4 opaque constructor/destructor calls; base ESP=E0-0x4C)

| Object | Address | Built by | Destroyed by | Passed onward |
|---|---|---|---|---|
| local_A (helper object) | E0-0x3D | CALL [0x00A75A38] @006C29FB, ECX=E0-0x3D, 0 stack args → result_A | CALL [0x00A75A40] @006C2A93, ECX=E0-0x3D | result_A = stack arg2 of ctor-B |
| local_B (wrapper 1) | E0-0x24 | CALL EDI=[0x00A75A44] @006C2A18, ECX=E0-0x24, args (ctx[4]=0xA7957B, result_A) | CALL [0x00A75A5C] @006C2A89, ECX=E0-0x24 | **&local_B = pump arg3** |
| local_C (helper object) | E0-0x3E | CALL [0x00A75A38] @006C2A1E, ECX=E0-0x3E, 0 stack args → result_C | CALL [0x00A75A40] @006C2A7A, ECX=E0-0x3E | result_C = stack arg2 of ctor-D |
| local_D (wrapper 2) | E0-0x3C | CALL EDI=[0x00A75A44] @006C2A32, ECX=E0-0x3C, args (ctx[3]=0xA7957B, result_C) | CALL [0x00A75A5C] @006C2A70, ECX=E0-0x3C | **&local_D = pump arg2** |

## 5. All [ESP+x] references, anchored (callee body)

| VA | ESP depth | Effective addr | Meaning |
|---|---|---|---|
| 006C29EB | E0-0x4C | E0-0xC | LEA EAX,[ESP+0x40] → SEH record node |
| 006C29F7 | E0-0x4C | E0-0x3D | LEA ECX,[ESP+0xF] → local_A |
| 006C2A0C | E0-0x54 | E0-0x24 | LEA ECX,[ESP+0x30] → local_B (this of ctor-B) |
| 006C2A10 | E0-0x54 | **E0-4** | MOV dword [ESP+0x50],0 → SEH state := 0 (before ctor-B) |
| 006C2A1A | E0-0x4C | E0-0x3E | LEA ECX,[ESP+0xE] → local_C |
| 006C2A29 | E0-0x54 | E0-0x3C | LEA ECX,[ESP+0x18] → local_D (this of ctor-D) |
| 006C2A2D | E0-0x54 | **E0-4** | MOV byte [ESP+0x50],2 → SEH state := 2 (before ctor-D) |
| 006C2A37 | E0-0x4C | **E0+0xC** | MOV EDX,[ESP+0x58] → arg3 (pointer-holder S+0x10) |
| 006C2A3F | E0-0x4C | **E0+0xC** (byte) | MOV [ESP+0x58],CL → **low byte of own arg3 slot := ctx[5]&0xFF (=1, C3)**; upper 24 bits of the slot RETAIN arg3's original upper bits (byte store only) |
| 006C2A43 | E0-0x4C | E0+0xC | MOV EDX,[ESP+0x58] → patched arg3 value = (S+0x10)&0xFFFFFF00 \| 1 |
| 006C2A48 | E0-0x50 | E0-0x24 | LEA ECX,[ESP+0x2C] → &local_B (pump arg3) |
| 006C2A4D | E0-0x54 | E0-0x3C | LEA EDX,[ESP+0x18] → &local_D (pump arg2) |
| 006C2A53 | E0-0x5C | **E0+8** | MOV EAX,[ESP+0x64] → arg2 = &ctx[0] |
| 006C2A5E | E0-0x5C | **E0-4** (byte) | MOV byte [ESP+0x58],3 → SEH state := 3 (before pump call) |
| 006C2A65 | E0-0x4C | E0-0x3C | LEA ECX,[ESP+0x10] → local_D (dtor) — **proves pump cleans 16 bytes (RET 0x10-class)** |
| 006C2A6B | E0-0x4C | E0-4 (byte) | MOV byte [ESP+0x48],2 → SEH state := 2 (dtor local_D) |
| 006C2A76 | E0-0x4C | E0-0x3E | LEA ECX,[ESP+0xE] → local_C (dtor) |
| 006C2A80 | E0-0x4C | E0-0x24 | LEA ECX,[ESP+0x28] → local_B (dtor) |
| 006C2A84 | E0-0x4C | E0-4 (byte) | MOV byte [ESP+0x48],0 → SEH state := 0 (dtor local_B) |
| 006C2A8F | E0-0x4C | E0-0x3D | LEA ECX,[ESP+0xF] → local_A (dtor) |
| 006C2A9B | E0-0x4C | E0-0xC | MOV ECX,[ESP+0x40] → saved FS:[0] |

**No [ESP+0x50] or [ESP+0x5C] reference exists at depth E0-0x4C** → callee NEVER reads arg1 ([E0+4]) and NEVER reads arg4 ([E0+0x10]). Exhaustive offset census: refs are 0xF, 0x10, 0x18, 0x28, 0x2C, 0x30, 0x40, 0x48, 0x4C-none, 0x50 (only at depth E0-0x54 → E0-4), 0x58, 0x5E-none, 0x64. All accounted above. Zero unexplained offsets.

## 6. Callee-pump call stack (CALL EAX @006C2A63)

Pushes (order: first push = highest address):
| ESP | Value | Callee-side slot |
|---|---|---|
| E0-0x50 | patched arg3 = (S+0x10)&~0xFF \| 1 | pump arg4 |
| E0-0x54 | E0-0x24 = &local_B | pump arg3 |
| E0-0x58 | E0-0x3C = &local_D | pump arg2 |
| E0-0x5C | **pair_ptr = M32[M32[arg3]] = M32[S+0x10]** (loaded @006C2A3B, pushed @006C2A52) | pump arg1 |
| E0-0x60 | return address (from CALL EAX @006C2A63) | |

Pump target = M32[arg2] = ctx[0] = **0x00823C10** (value from closed prior @006C410C). Pump receiver ECX = M32[arg2+4] + M32[this] = ctx[1] + ctx[2] = **0 + 00415670_result** (@006C2A57, @006C2A3D, ADD ECX,ESI @006C2A5C). Pump convention: ECX-this + 4 stack args, callee cleans 16 (proven by post-call depth arithmetic, §5 @006C2A65).

## 7. Full ESP balance (entry → RET)

| # | Event | ESP |
|---|---|---|
| entry | CALL 006C29D0 pushes return address | E0 |
| +PUSH -1 | 006C29D0 | E0-4 |
| +PUSH handler | 006C29D2 | E0-8 |
| +PUSH FS | 006C29DD | E0-0xC |
| +SUB 0x34 | 006C29DE | E0-0x40 |
| +PUSH ESI | 006C29E1 | E0-0x44 |
| +PUSH EDI | 006C29E2 | E0-0x48 |
| +PUSH cookie | 006C29EA | **E0-0x4C (base)** |
| ctor-B: PUSH,PUSH (006C2A07/0B) → E0-0x54; CALL (retaddr E0-0x58); callee cleans 2 args → | E0-0x4C |
| ctor-D: PUSH,PUSH (006C2A27/28) → E0-0x54; CALL; callee cleans 2 args → | E0-0x4C |
| pump: PUSH×4 (006C2A47/4C/51/52) → E0-0x5C; CALL (retaddr E0-0x60); callee cleans 4 args → | E0-0x4C |
| epilog: POP ECX (cookie) | E0-0x48 |
| POP EDI | E0-0x44 |
| POP ESI | E0-0x40 |
| ADD ESP,0x40 (locals 0x34 + SEH trio 0xC) | E0 |
| RET 0x10: pop return address (+4), add 0x10 | **E0+0x14 = S-0xC** |

Caller cross-check (closed prior P10): no `ADD ESP` after CALL 006C29D0; next loop iteration re-pushes 4 args at S-0x10..S-0x1C — balance closes at S-0xC. ✓

## 8. SEH exceptional path

- Handler 0x00A04804 is DATA (PUSH imm @006C29D2), never CALLed by normal flow.
- Exception in ANY of the 9 indirect callees (or a fault on the loads/stores) → OS walks FS:[0] → record at E0-0xC → handler 0x00A04804 (body OUTSIDE window, opaque scopetable) → unwind destructors per state (0→local_B, 2→local_D, per construction state pairing) → propagate. Caller 006C36B0 shows no catch in its admitted window → unwinds further.
- Exceptional path has NO EAX-return contract to 006C36B0 (no normal RET on that path).
