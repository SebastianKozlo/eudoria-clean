# STACK_MAP — 006C4060 (consumer, Etap B, P02)

Source: P02_EXTRACT (62 rows, [006C4166,006C4220), admission Ad4f041c2ce70, sha256 CBFAB828…23AE5) combined with closed priors WINDOW_006C4057 + WINDOW_006C40E0 (P06_CONSUMER_R1, same run family, read-only). Caller-side facts from P01_ADAPTER/STACK_MAP.md (S-frame of 006C36B0) reused read-only.

Notation:
- `E1` = ESP at entry to 006C4060 (= after its CALL pushed the return address; [E1] = return address).
- `B`  = ESP immediately after PUSH EAX (cookie) @006C407C = **E1−0x44** (C1's B).
- `C`  = B+0x1C = **E1−0x28** — the one shared container header (C1): C+0 = begin, C+4 = end (pair array, 8-byte elements), C+8 = limit.
- All offsets hex. `M32[x]` = DWORD at x.

## 1. Prolog (from closed prior WINDOW_006C4057)

| ESP after | Instruction | Slot | Role |
|---|---|---|---|
| E1−0x04 | PUSH −1 @006C4060 | [E1−4] = −1 | SEH state (ehstate) |
| E1−0x08 | PUSH 0xA04968 @006C4062 | [E1−8] = 0x00A04968 | SEH handler (data-pushed) |
| E1−0x0C | MOV EAX,FS:[0]; PUSH EAX @006C4067/6D | [E1−0xC] = prev FS:[0] | SEH next |
| E1−0x30 | SUB ESP,0x24 @006C406E | [E1−0x30, E1−0x0C) | locals (0x24 B) |
| E1−0x34 | PUSH EBX @006C4071 | [E1−0x34] | nonvolatile save |
| E1−0x38 | PUSH EBP @006C4072 | [E1−0x38] | nonvolatile save |
| E1−0x3C | PUSH ESI @006C4073 | [E1−0x3C] | nonvolatile save |
| E1−0x40 | PUSH EDI @006C4074 | [E1−0x40] | nonvolatile save |
| E1−0x44 | MOV EAX,[0x00B9D8D0]; XOR EAX,ESP; PUSH EAX @006C4075/7A/7C | [E1−0x44] = cookie^ESP | security cookie (**popped and discarded @006C41E8; NO validation visible**) |

FS:[0] ← E1−0x0C (LEA EAX,[ESP+0x38] @006C407D with ESP=E1−0x44; MOV FS:[0],EAX @006C4081). SEH record = {next@E1−0xC, handler@E1−8, state@E1−4}. **Base depth of the body: ESP = B = E1−0x44.**

Known locals inside [E1−0x30, E1−0x0C):
| Address | Size | Role |
|---|---|---|
| E1−0x2D | 1 B | wrapper byte (LEA'd @006C40EB → 006C2C50 arg3; LEA'd @006C4152 → 008D6D90 arg4; uninitialized at both uses) |
| [E1−0x2C, E1−0x28) | 4 B | **out-slot**: &out passed as 006C36B0 arg1 (@006C413C/4140); written *out := 0x00BA45E8 by 006C36B0 (prior P10 @006C371B-371F, loop-complete path); **zeroed @006C415E** before 008D6D90; its address passed as 008D6D90 arg3 |
| [E1−0x28, E1−0x1C) | 12 B | **C** = shared container {begin, end, limit} |
| E1−0x10 | 1 B | ctx[5] staging byte (MOV byte [ESP+0x4C],1 @006C4125; MOV EBP,[ESP+0x4C] @006C412A; C3: upper 24 bits not fixed) |

## 2. Segment depths and deferred cleanup ledger (whole body, both paths)

Let PATH-B = the branch where CALL 006C2C50 executes (EAX != end @006C40E7); PATH-A = JZ taken (skip).

| # | Event | ESP |
|---|---|---|
| entry | CALL 006C4060 pushes return address | E1 |
| prolog (§1) | — | **E1−0x44 (B)** |
| collect-1: PUSH EAX(C) @006C4099, PUSH 0xA855F0 @006C409A | 2 args | E1−0x4C |
| CALL 006C3FE0 @006C40A3 (cdecl, args stay) | | E1−0x4C |
| collect-2: PUSH ECX(C) @006C40AC, PUSH 0xA858B8 @006C40AD | 2 args | E1−0x54 |
| CALL 006C4020 @006C40B2 | | E1−0x54 |
| collect-3: PUSH EDX(C) @006C40BB, PUSH 0xA858C0 @006C40BC | 2 args | E1−0x5C |
| CALL 006C4020 @006C40C1 | | E1−0x5C |
| sort: PUSH EAX(end=C+4 val) @006C40CE, PUSH ECX(begin=C+0 val) @006C40CF | 2 args | E1−0x64 |
| CALL 006C3D40 @006C40D0 | | E1−0x64 |
| scan: PUSH ESI(end) @006C40DD, PUSH EDX(begin) @006C40DE | 2 args | E1−0x6C |
| CALL 006C2C90 @006C40DF → EAX | | E1−0x6C |
| **ADD ESP,0x28 @006C40E4** (5 calls × 2 args = 0x28, byte-exact) | | **E1−0x44 (B)** |
| PATH-A: JZ @006C40E9 → 006C40FB | | E1−0x44 |
| PATH-B: PUSH &wrapper @006C40EF, PUSH ESI(end) @006C40F0, PUSH EAX(pos) @006C40F1; LEA ECX,[ESP+0x28]=C (this); CALL 006C2C50 @006C40F6 | 3 args | E1−0x50 during setup; return **E1−0x44 iff callee-clean RET 0xC (premise P4)** |
| CALL 00415670 @006C4100 (0 visible args) → EBX | | E1−0x44 |
| **SUB ESP,0x18 @006C4105** (ctx 6 DWORDs at [E1−0x5C, E1−0x44); ctx[5] = E1−0x48) | | E1−0x5C |
| PUSH 0x00BA45E8 @006C412E (arg4) | | E1−0x60 |
| PUSH EDX(end=C+4) @006C413A (arg3); PUSH EAX(begin=C+0) @006C413B (arg2) | | E1−0x64 → E1−0x68 |
| LEA ECX,[ESP+0x3C] = E1−0x2C (&out); PUSH ECX @006C4140 (arg1) | | E1−0x6C |
| CALL 006C36B0 @006C4141 (S = **E1−0x70**; args at [S+4]=&out, [S+8]=begin, [S+0xC]=end, [S+0x10]=0x00BA45E8 — matches P01 S-map byte-for-byte) | | E1−0x6C (cdecl premise P3) |
| fixup-args: LEA EDX,[ESP+0x3F]=E1−0x2D; PUSH EDX @006C4156 (arg4); LEA EAX,[ESP+0x44]=E1−0x2C; PUSH EAX @006C415B (arg3); PUSH ESI(tail) @006C415C (arg2); PUSH ECX(begin) @006C415D (arg1) | 4 args | E1−0x70 → E1−0x7C |
| MOV [ESP+0x50],0 @006C415E → *out_slot := 0 (E1−0x2C) | | E1−0x7C |
| MOV EDI,ESI @006C4166 (tail snapshot → EDI) | | E1−0x7C |
| CALL 008D6D90 @006C4168 (cdecl premise P3) | | E1−0x7C |
| **ADD ESP,0x38 @006C416D** (ctx 0x18 + 006C36B0 args 0x10 + 008D6D90 args 0x10 = 0x38, byte-exact) | | **E1−0x44 (B)** |
| branch region 006C4170..006C41B2 (no pushes/pops; loop writes elements only) | | E1−0x44 |
| memmove-args: PUSH ESI(count) @006C41A0, PUSH EDI(src) @006C41A1, PUSH EAX(dst) @006C41A2; CALL [0xA753B4] @006C41A3; **ADD ESP,0xC @006C41A9** | net 0 | E1−0x44 |
| dealloc-args: PUSH EDX(size) @006C41D2, PUSH EAX(begin) @006C41D3; CALL [0xA759FC] @006C41D4; **ADD ESP,0x8 @006C41DA** | net 0 | E1−0x44 |
| epilog §3 | | E1 → E1+4 |

## 3. Epilog (P02 extract)

| ESP after | Instruction | Note |
|---|---|---|
| E1−0x44 | MOV ECX,[ESP+0x38] @006C41DD | ECX = M32[E1−0x0C] = saved prev FS:[0] |
| E1−0x44 | MOV FS:[0],ECX @006C41E1 | SEH chain restored |
| E1−0x40 | POP ECX @006C41E8 | cookie → discarded (no /GS check visible) |
| E1−0x3C | POP EDI @006C41E9 | LIFO reversal of prolog |
| E1−0x38 | POP ESI @006C41EA | |
| E1−0x34 | POP EBP @006C41EB | |
| E1−0x30 | POP EBX @006C41EC | |
| E1 | ADD ESP,0x30 @006C41ED | locals 0x24 + SEH trio 0xC |
| E1+4 | RET @006C41F0 | pops return address; frame 0x44 fully reversed (0x14 pops + 0x30 = 0x44 ✓) |

## 4. SEH state slot writes (all resolve to [E1−4] at their local depths)

| VA | Depth | Operand | Effective |
|---|---|---|---|
| 006C4060 | (push) | PUSH −1 | [E1−4] = −1 |
| 006C409F | E1−0x4C | [ESP+0x48] | [E1−4] = 0 (EDI=0 since XOR EDI,EDI @006C4087; no EDI write between) |
| 006C41B9 | E1−0x44 | [ESP+0x40], 0xFFFFFFFF | [E1−4] = −1 (epilog reset; interleaved between TEST @006C41B7 and JZ @006C41C1 — MOV preserves flags) |

Handler = 0x00A04968 (data @006C4062); scopetable opaque; unwind semantics outside window. States visible: −1 → 0 → −1.

## 5. All [ESP+x] references in the P02 window, anchored (body part; neighbors excluded)

| VA | Depth | Effective addr | Meaning |
|---|---|---|---|
| 006C41B3 | E1−0x44 | **E1−0x28 = C+0** | MOV EAX,[ESP+0x1C] → local container begin |
| 006C41B9 | E1−0x44 | **E1−4** | SEH state := −1 |
| 006C41C3 | E1−0x44 | **E1−0x20 = C+8** | MOV EDX,[ESP+0x24] → limit field |
| 006C41DD | E1−0x44 | **E1−0x0C** | MOV ECX,[ESP+0x38] → saved prev FS:[0] |

(Prior-window references reconciled in §1/§2 and by closed priors; e.g. 006C409F [ESP+0x48]@E1−0x4C, 006C4121 [ESP+0x38]@E1−0x5C → C+4, 006C4125 [ESP+0x4C] → E1−0x10 staging byte, 006C4136 [ESP+0x38]@E1−0x60 → C+0, 006C4152 [ESP+0x3F]@E1−0x6C → wrapper E1−0x2D, 006C4157 [ESP+0x44]@E1−0x70 → out-slot E1−0x2C, 006C415E [ESP+0x50]@E1−0x7C → out-slot E1−0x2C.) **Zero unexplained offsets.**

## 6. Independent depth-model confirmations (three fixed-offset writes at three depths, one model)

1. [ESP+0x48] @006C409F (depth E1−0x4C) must hit the state slot [E1−4] — ✓ only at the post-collect-1 depth.
2. [ESP+0x50] @006C415E (depth E1−0x7C) must hit the out-slot E1−0x2C — ✓ only if all 14 deferred DWORDs (ctx 6 + 006C36B0 4 + 008D6D90 4) sit above base; under a cdecl-006C2C50 alternative the depth would be E1−0x88 and the store would hit [E1−0x38] = saved EBP (destructive — falsifier).
3. [ESP+0x40] @006C41B9 (depth E1−0x44) must hit [E1−4] — ✓ only if ADD ESP,0x38 restored base exactly.

## 7. 008D6D90 call frame (at CALL @006C4168, ESP = E1−0x7C)

| Callee slot | Value | Source |
|---|---|---|
| [E1−0x78] (arg1) | begin = M32[0x00BA45E8] | MOV ECX @006C414C; PUSH ECX @006C415D |
| [E1−0x74] (arg2) | tail = M32[0x00BA45EC] (pre-call) | MOV ESI @006C4146; PUSH ESI @006C415C |
| [E1−0x70] (arg3) | &out_slot = E1−0x2C (content 0) | LEA EAX @006C4157; PUSH EAX @006C415B; zeroed @006C415E |
| [E1−0x6C] (arg4) | &wrapper = E1−0x2D (uninitialized) | LEA EDX @006C4152; PUSH EDX @006C4156 |
| [E1−0x80] | return address | CALL @006C4168 |

## 8. Exceptional path

Handler 0x00A04968 is DATA (PUSH imm @006C4062), never CALLed. Any exception in the 11 callees (or fault on loads/stores) → OS walks FS:[0] → record at E1−0xC → handler 0x00A04968 (body outside window, scopetable opaque) → unwind per state (state 0 active from 006C40A3 to 006C41B9 — presumably covering C's heap buffer; inference only) → propagate to caller. No in-window catch; **no EAX-return contract on the exceptional path**.
