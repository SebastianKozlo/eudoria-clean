# STACK_MAP.md — 00528810 OwnerFn (P03_DISPATCHER)

E = entry ESP. Deep-path frame: SUB ESP,0x78 -> PUSH ESI -> PUSH EDI@00528842 => ESP = E-0x80. Guard-exit path (JZ 00528BB4 taken before PUSH EDI) has ESP = E-0x7C at its POP ESI.

## Entry args (RET 0x8)
- arg1 = [E+0x04] float (FADD source @00528A60 reads it via [ESP+0x84] at ESP=E-0x80)
- arg2 = [E+0x08] float (S1 of 0085C130 call#1 via [ESP+0x88] @00528A05)

## Key slots (ESP=E-0x80 base unless noted)
- [ESP+0x18] = E-0x68: 0085BFA0 out-buffer (13 dwords, E-0x68..E-0x35). Slots referenced: +0x24= [ESP+0x3C], +0x28=[ESP+0x40], +0x2C=[ESP+0x44].
- [ESP+0xC]/[ESP+0x10]/[ESP+0x14] = copies of this{+0xD4,+0xD8,+0xDC}.
- [ESP+0x8] = temp float (e.g., [ESI+0xE0]+arg1).
- arg1 local of 0085C130 calls = LEA [ESP+0x50] at call#1 (ESP=E-0x84 => E-0x34) and LEA [ESP+0x50] at call#2 (ESP=E-0x84 => E-0x34): SAME local E-0x34. Post-call read at [EAX+0x24..+0x2C] = E-0x10/E-0x0C/E-0x08.
- S1 slots: call#1 PUSH ECX reserve + FSTP [ESP] at ESP=E-0x84 => E-0x84. call#2 PUSH ECX reserve@00528AA8 + FSTP [ESP]@00528ABB at ESP=E-0x84 => E-0x84.
- 0085CDE0 args: PUSH 0; LEA ECX,[ESP+0x1C]; PUSH ECX (callee-cleanup RET8 premise).
- 0085C280 arg: LEA EAX,[ESP+0xC]; PUSH EAX (RET4 premise).
- Manual float-arg blocks: SUB ESP,8 (args for 004B2A20) + SUB ESP,0xC (args for cdecl 0041C740) cleaned by ADD ESP,0x14@0052897E.

## ESP balance
Deep path: POP EDI@00528BB3; POP ESI; ADD 0x78; RET 0x8. Guard path: POP ESI@00528BB4; ADD 0x78; RET 0x8. All inner pushes callee-cleaned (premises labeled per callee). Balanced.

## FPU depth
Full trace performed (CLAIMS C12): peaks depth 5 (block 005289AC..005289F3 leaves depth-3 reuse), drained to 0 at RET on all paths. Float-return premise for 004B2A20/00861220/00734210/00861240 (FSTP after each CALL).
