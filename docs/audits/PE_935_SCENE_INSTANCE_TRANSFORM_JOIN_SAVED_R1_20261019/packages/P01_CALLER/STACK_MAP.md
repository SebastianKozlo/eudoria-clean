# P01_CALLER STACK MAP — 00527AA0 (window [0x00527AA0,0x00527B20), 37 rows)

Notation: **E** = value of ESP at function entry (after the CALL into 00527AA0 pushed the return address).
Argument slots of THIS function: **[E] = RETADDR** (return to 00527AA0's caller), **[E+4] = ARG1** (the single stack argument; proven by RET 0x4 callee cleanup, row 180931 @0x00527b1d).

## 1. Full ESP walk (main path)

| row | VA | instruction | ESP after | note |
|---|---|---|---|---|
| — | entry | (CALL pushed RETADDR) | E | [E]=RETADDR, [E+4]=ARG1 |
| 180895 | 0x00527ab0 | SUB ESP,0x34 | E-0x34 | allocates the 0x34-byte local buffer [E-0x34, E) = 13 dwords — the WHOLE frame is the transform out-buffer (P01-C07/C23) |
| 180896 | 0x00527ab3 | PUSH EBX | E-0x38 | [E-0x38]=saved EBX |
| 180897 | 0x00527ab4 | MOV EBX,ECX | E-0x38 | this → EBX (owner register) |
| 180898 | 0x00527ab6 | PUSH EDI | E-0x3C | [E-0x3C]=saved EDI |
| 180899 | 0x00527ab7 | MOV EDI,[EBX+0xC] | E-0x3C | receiver = [this+0xC] (single dereference) |
| 180900 | 0x00527aba | TEST EDI,EDI | E-0x3C | guard 1 |
| 180901 | 0x00527abc | JZ 0x00527b18 | E-0x3C | early exit with ESP=E-0x3C (no ESI push) |
| 180902 | 0x00527abe | CMP [EBX+0x10],0x0 | E-0x3C | guard 2 |
| 180903 | 0x00527ac2 | JZ 0x00527b18 | E-0x3C | early exit with ESP=E-0x3C |
| 180904-180912 | 0x00527ac4-0x00527ae5 | FPU block | E-0x3C | no ESP change (see FPU trace) |
| 180913 | 0x00527aeb | PUSH ESI | E-0x40 | [E-0x40]=saved ESI (join point of the JP branch and fall-through) |
| 180914 | 0x00527aec | FSTP [EBX+0xE4] | E-0x40 | final FPU pop (depth → 0) |
| 180915 | 0x00527af2 | LEA EAX,[ESP+0xC] | E-0x40 | EAX = E-0x40+0xC = **E-0x34** = buffer base = frame base |
| 180916 | 0x00527af6 | PUSH EAX | E-0x44 | [E-0x44] = &buffer → sole stack arg of 0085BFA0 |
| 180917 | 0x00527af7 | MOV ECX,EDI | E-0x44 | receiver → ECX (thiscall) |
| 180918 | 0x00527af9 | CALL 0x0085bfa0 | (inside: E-0x48) | **returns with ESP=E-0x40**: callee RET 0x4 cleans the &buffer arg (P01-C08; prior R2 P04-K01 RET 0x4 @0x0085C0B4) |
| 180919 | 0x00527afe | ADD EDI,0x30 | E-0x40 | copy destination = receiver+0x30 |
| 180920 | 0x00527b01 | MOV ESI,EAX | E-0x40 | copy source = returned pointer = &buffer (prior R2: EAX=out-pointer at RET) |
| 180921 | 0x00527b03 | MOV ECX,0xD | E-0x40 | 13 dwords |
| 180922 | 0x00527b08 | REP MOVSD | E-0x40 | [ESI..ESI+0x33] → [EDI..EDI+0x33] = receiver+0x30..+0x63 (13 dwords = whole buffer) |
| 180923 | 0x00527b0a | MOV ECX,[ESP+0x44] | E-0x40 | = [E-0x40+0x44] = **[E+4] = ARG1** — consistent ONLY with callee cleanup at row 180918 |
| 180924 | 0x00527b0e | PUSH ECX | E-0x44 | [E-0x44] = ARG1 forwarded |
| 180925 | 0x00527b0f | MOV ECX,[EBX+0x10] | E-0x44 | second object → ECX |
| 180926 | 0x00527b12 | CALL 0x00861150 | (inside: E-0x48) | **returns with ESP=E-0x40**: proven by epilogue pairing (P01-C10) |
| 180927 | 0x00527b17 | POP ESI | E-0x3C | restores [E-0x40] ✓ |
| 180928 | 0x00527b18 | POP EDI | E-0x38 | restores [E-0x3C] ✓ (early-exit join lands HERE with ESP=E-0x3C) |
| 180929 | 0x00527b19 | POP EBX | E-0x34 | restores [E-0x38] ✓ |
| 180930 | 0x00527b1a | ADD ESP,0x34 | E | frame released |
| 180931 | 0x00527b1d | RET 0x4 | E+4 | pops RETADDR, callee-cleans ARG1 slot [E+4] |

**ESP balance: entry E → exit E+4. Exact on the main path.**

## 2. Early-exit path (guard 1 or guard 2 fails)

JZ @180901 / @180903 taken with **ESP=E-0x3C** → jump to 0x00527b18:
POP EDI (E-0x38) → POP EBX (E-0x34) → ADD ESP,0x34 (E) → RET 0x4 (E+4).
PUSH ESI @180913 and POP ESI @180927 are correctly NOT on this path (per-path pairing exact). No FPU executed, no calls, no field writes (P01-C25). **Balanced.**

## 3. Callee-cleanup disambiguation (the one subtle point)

After CALL 0085BFA0 (row 180918) there is no ADD ESP. Two arithmetically conceivable readings:
1. **0085BFA0 cleans its 1 arg (RET 0x4)** → ESP=E-0x40 → [ESP+0x44]=[E+4]=ARG1 (forwarded to 00861150). Then 00861150 must also clean 4 bytes for POP ESI @180927 to hit [E-0x40].
2. 0085BFA0 cdecl (RET 0) → ESP=E-0x44 → [ESP+0x44]=[E]=**the saved return address** would be forwarded as the argument — semantically pathological; also contradicted by the frozen prior body (R2 P04-K01: RET 0x4 @0x0085C0B4).

Reading 1 is CONFIRMED (within-package ESP coherence + prior pinned body). Under reading 1 the epilogue pairing is exact; reading 2 is REJECTED (P01-C08).

## 4. x87 FPU depth trace (no-leak proof, both JP directions)

| row | VA | instruction | depth after | st0 |
|---|---|---|---|---|
| 180904 | 0x00527ac4 | FLDZ | 1 | +0.0 |
| 180905 | 0x00527ac6 | FST [EBX+0xE0] | 1 | +0.0 (stored to owner_float_E0, no pop) |
| 180906 | 0x00527acc | FLD [0x00A797C8] | 2 | global_float_A797C8 (st1=+0.0) |
| 180907 | 0x00527ad2 | FCOMP [EBX+0xE4] | 1 | +0.0 (global popped after compare) |
| 180908 | 0x00527ad8 | FNSTSW AX | 1 | +0.0 |
| 180909/180910 | 0x00527ada/0x00527add | TEST AH,0x5 / JP | 1 | +0.0 |
| — JP TAKEN (> , == , unordered) → | 0x00527aeb | **depth 1 at join** | | |
| 180911 | 0x00527adf | FLD [EBX+0xE4] | 2 | owner_float_E4 (st1=+0.0) |
| 180912 | 0x00527ae5 | FSTP [EBX+0xE8] | 1 | +0.0 (owner_float_E4 → owner_float_E8) |
| — fall-through → | 0x00527aeb | **depth 1 at join** | | |
| 180914 | 0x00527aec | FSTP [EBX+0xE4] | 0 | owner_float_E4 := +0.0, popped |

**Both directions of the JP @180910 arrive at the join 0x00527aeb with depth 1 (st0=+0.0); the join FSTP pops to depth 0. Early-exit paths never execute FPU (depth 0). Function returns at FPU depth 0 on all paths — NO LEAK (P01-C06/C22).**

## 5. Conditional-copy semantics of the +0xE4 block (mechanical, working labels)

Let G = float dword at 0x00A797C8 (global; value not in evidence). FCOMP compares **st0=G** against **[EBX+0xE4]**; TEST AH,0x5 masks C0 (bit0) and C2 (bit2); JP is taken iff the masked result has even parity, i.e. iff (C0,C2) ∈ {00, 11}:

| compare result (G vs field_E4) | C3,C2,C0 | AH&5 | parity | JP | copy block (180911-180912) |
|---|---|---|---|---|---|
| G > field | 0,0,0 | 0 | even | taken | skipped |
| G == field | 1,0,0 | 0 | even | taken | skipped |
| G < field | 0,0,1 | 1 | odd | **not taken** | **executed**: field_E8 := field_E4 |
| unordered (NaN) | 1,1,1 | 5 | even | taken | skipped (NaN-safe) |

Net effect (both paths continue to 180913-180914):
- owner_float_E0 := +0.0 — always (FLDZ/FST, rows 180904-180905)
- owner_float_E8 := owner_float_E4 — ONLY when G < field_E4 (rows 180911-180912)
- owner_float_E4 := +0.0 — always (FSTP at join, row 180914)

This is the canonical MSVC `if (G < field_E4) field_E8 = field_E4;` + zeroing idiom. Working labels only: owner_float_E0/E4/E8 are three consecutive dword-stride float fields of the owner at +0xE0/+0xE4/+0xE8. No semantics (metric/timer/position/etc.) invented.
