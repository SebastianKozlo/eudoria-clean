# STACK_MAP — ESP trace for 0085ACD0 region [0085ACD0,0085AD10)

ESP0 = ESP at function entry (return address of caller at [ESP0], ARG1 at [ESP0+4]).
Locals: L0 = [ESP0-8], L1 = [ESP0-4] (the 8-byte pair reserved by SUB ESP,0x8).

| VA | instruction | ESP after (rel ESP0) | note |
|---|---|---|---|
| 0085ACD0 | SUB ESP,0x8 | -0x8 | reserves L0,L1 |
| 0085ACD3 | LEA EAX,[ECX+0x88] | -0x8 | guard address |
| 0085ACD9 | XOR EDX,EDX | -0x8 | EDX=0 |
| 0085ACDB | CMP [EAX],EDX | -0x8 | tests [ECX+0x88]==0 |
| 0085ACDD | PUSH ESI | -0xC | save ESI |
| 0085ACDE | MOV ESI,[ESP+0x10] | -0xC | [ESP0-0xC+0x10]=[ESP0+4]=ARG1 → ESI |
| 0085ACE2 | JNZ 0085AD12 | -0xC | skip if [ECX+0x88]≠0 (target outside window) |
| 0085ACE4 | PUSH EDX | -0x10 | push 0 (future arg6) |
| 0085ACE5 | MOV [ESP+0x8],EDX | -0x10 | [ESP0-0x10+8]=[ESP0-8]=L0 := 0 |
| 0085ACE9 | MOV [ESP+0xC],EDX | -0x10 | [ESP0-0x10+0xC]=[ESP0-4]=L1 := 0 ← analyzed store |
| 0085ACED | LEA EAX,[ESP+0x8] | -0x10 | EAX=&L0 (8-byte out-buffer) |
| 0085ACF1 | PUSH EAX | -0x14 | arg5 = &L0 |
| 0085ACF5 | LEA EDX,[ECX+0x5C]; PUSH EDX | -0x18 | arg4 = embedded addr ECX+0x5C |
| 0085ACFC | LEA EAX,[ECX+0x44]; PUSH EAX | -0x1C | arg3 = embedded addr ECX+0x44 |
| 0085ACF6 | MOV EDX,[ECX+0x78] | -0x1C | arg2 source |
| 0085AD00 | PUSH EDX | -0x20 | arg2 = [ECX+0x78] |
| 0085ACFD | MOV EAX,[ECX+0x74] | -0x20 | arg1 source |
| 0085AD01 | PUSH EAX | -0x24 | arg1 = [ECX+0x74] |
| 0085AD02 | MOV ECX,ESI | -0x24 | thiscall receiver = ARG1 |
| 0085AD04 | CALL 0x00730F00 | -0x24 at call | callee expected to clean 0x18 (arg1..arg6) → ESP0-0xC |
| 0085AD09 | MOV EAX,ESI | -0xC (assumed) | return ARG1 |
| 0085AD0B | POP ESI | -0x8 | restore |
| 0085AD0C | ADD ESP,0x8 | 0 | drop L0,L1 |
| 0085AD0F | RET 0x4 | 0 | clean ARG1 |

## Key mappings at the analyzed store (0085ACE9)

- ESP = ESP0-0x10 (after SUB ESP,8 + PUSH ESI + PUSH EDX).
- [ESP+0x8]  = ESP0-8 = L0 — written 0 at 0085ACE5.
- [ESP+0xC]  = ESP0-4 = L1 — written 0 at 0085ACE9.
- Return address [ESP0] and saved ESI [ESP0-0xC] are NOT touched by either store.

## Stack layout at CALL 00730F00 (top → down)

| slot | content |
|---|---|
| [ESP0-0x24] | arg1 = [ECX+0x74] |
| [ESP0-0x20] | arg2 = [ECX+0x78] |
| [ESP0-0x1C] | arg3 = ECX+0x44 (embedded address) |
| [ESP0-0x18] | arg4 = ECX+0x5C (embedded address) |
| [ESP0-0x14] | arg5 = &L0 (zeroed 8-byte out-buffer) |
| [ESP0-0x10] | arg6 = 0 |
| [ESP0-0x0C] | saved ESI |
| [ESP0-0x08] | L0 = 0 |
| [ESP0-0x04] | L1 = 0 |
| [ESP0] | return address of 0085ACD0's caller |
| [ESP0+4] | ARG1 of 0085ACD0 (= ESI) |

Callee cleanup of 0x18 bytes is inferred from caller-side balance only (claim P01-C8,
STRONGLY_SUPPORTED); 00730F00 body was not opened.
