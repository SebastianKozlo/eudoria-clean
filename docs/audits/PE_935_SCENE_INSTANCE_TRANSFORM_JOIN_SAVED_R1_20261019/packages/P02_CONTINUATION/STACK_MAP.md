# STACK_MAP.md — 0085C130 (P02_CONTINUATION, author: PE-MASTER_DIRECT_ANALYST_FALLBACK)

E = entry ESP (points at return address). Frame after prolog: SUB ESP,0x7C; PUSH ESI -> ESP0 = E-0x80.

## Entry args (RET 0x8 => 2 callee-cleaned dwords)
- arg1 = [E+0x04] dword pointer -> loaded to ESI @0x0085C243; receiver (ECX) of CALL 0096D7C0; returned as EAX @0x0085C271.
- arg2 = [E+0x08] float, working label S1 (lerp/blend factor) -> read @0x0085C16D as [ESP+0x8C] (ESP=E-0x84) and @0x0085C21A as [ESP+0x88] (ESP=E-0x80).

## Key frame slots (absolute)
- OUT = E-0x34 .. E-0x01: 13-dword 0085BFA0 out-buffer (arg pushed @0x0085C138).
  Slots read here (QC-F1-corrected): +0x24 (E-0x10) @0x0085C140 (FLD BEFORE PUSH ECX, ESP=E-0x80), +0x28 (E-0x0C) @0x0085C153, +0x2C (E-0x08) @0x0085C15E (both AFTER the PUSH, ESP=E-0x84).
- C-O trio: E-0x64/E-0x60/E-0x5C (written @0x0085C14F/0x0085C15A/0x0085C165, ESP=E-0x84).
- S1*(C-O) trio: E-0x58/E-0x54/E-0x50 (@0x0085C17A/0x0085C184/0x0085C18C).
- L1 = O + S1*(C-O): E-0x4C/E-0x48/E-0x44 (@0x0085C197/0x0085C1A2/0x0085C1AD). Read for arg push as LEA EAX,[ESP+0x34] @0x0085C250 (ESP=E-0x80 -> E-0x4C).
- v-trio (zeroed @0x0085C1B3-1BB): E-0x70/E-0x6C/E-0x68; &v pushed @0x0085C14B (value LEA ECX,[ESP+0x10] at ESP=E-0x80 -> E-0x70).
- u-trio (zeroed @0x0085C1C6-1D7): E-0x7C/E-0x78/E-0x74; &u pushed @0x0085C1D2.
- w = u-v: E-0x58/E-0x54/E-0x50 (OVERWRITES the S1*(C-O) trio slots AFTER L1 consumed them; verified write-order: L1 FADDs read E-0x58/E-0x54/E-0x50 @0x0085C193/0x0085C19E/0x0085C1A9 BEFORE w stores @0x0085C1EE/0x0085C200/0x0085C212).
- S1*w trio: E-0x64/E-0x60/E-0x5C (@0x0085C227/0x0085C231/0x0085C235; note [ESP+0x1C] @ESP=E-0x80 -> E-0x64).
- L2 = v + S1*w: E-0x40/E-0x3C/E-0x38 (FSTP @0x0085C24C [ESP+0x40,ESP=E-0x80], @0x0085C25E+PUSH shift -> [ESP+0x4C,ESP=E-0x88] = E-0x3C, @0x0085C268 [ESP+0x50,ESP=E-0x88] = E-0x38).

## Push-shift table [0085C250,0085C268]
| VA | ESP | operand | resolves |
|---|---|---|---|
| 0x0085C250 | E-0x80 | LEA EAX,[ESP+0x34] | E-0x4C = &L1 |
| 0x0085C254 | E-0x80 | PUSH EAX | ESP->E-0x84 |
| 0x0085C255 | E-0x84 | FADD [ESP+0x24] | E-0x60 = S1*w1 |
| 0x0085C259 | E-0x84 | LEA ECX,[ESP+0x44] | E-0x40 = &L2 |
| 0x0085C25D | E-0x84 | PUSH ECX | ESP->E-0x88 |
| 0x0085C25E | E-0x88 | FSTP [ESP+0x4C] | E-0x3C = L2[1] |
| 0x0085C264 | E-0x88 | FADD [ESP+0x2C] | E-0x5C = S1*w2 |
| 0x0085C268 | E-0x88 | FSTP [ESP+0x50] | E-0x38 = L2[2] |
Stack args to 0096D7C0: [ESP]=&L2 (E-0x40), [ESP+4]=&L1 (E-0x4C).

## ESP balance (single path; no branches in window)
SUB 0x7C; PUSH ESI; inner PUSHes: 0x0085C14B, 0x0085C1D2, 0x0085C254, 0x0085C25D (all callee-cleaned: CD10 RET4 x2 premise, D7C0 RET8 premise; no ADD ESP observed); POP ESI; ADD ESP,0x7C; RET 0x8. Balanced.

## FPU depth trace (summary; full step list in REPORT.md)
Depth peaks at 6 @0x0085C21A (S1,w0? see trace) — actual peak 6 (S1,S1,w0S1?,...): exact peaks: 2 @0x0085C174, 3 @0x0085C176, 5 @0x0085C1EA, 4 @0x0085C1FC, 5 @0x0085C216, 6 @0x0085C223, then monotone drain to 0 @0x0085C268. Depth 0 at RET. No leak.

