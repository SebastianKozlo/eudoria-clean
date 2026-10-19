# FLOW — 006C4060 (consumer, Etap B, P02)

Control flow over the combined windows [006C4060, 006C41F1] (closed priors + P02 extract). Single entry, single normal exit RET @006C41F0. All 9 branches in-window (JZ x7, JMP x1, JNZ x1).

## 1. Control flow (P02 segment; opaque calls marked)

```
... (prolog/collect/sort/scan per closed priors; base depth B=E1-0x44 restored @006C40E4)
006C40E7 CMP EAX,ESI            ; EAX = 006C2C90 ret, ESI = M32[C+4] (end)
006C40E9 JZ 006C40FB            ; no duplicate found -> skip fix-up
006C40EB..F6 [OPAQUE] CALL 006C2C50(this=C, pos, end, &wrapper)     ; dedupe fix-up; callee-clean RET 0xC (premise P4)
006C40FB MOV ESI,0x00823C10
006C4100 [OPAQUE] CALL 00415670 -> EBX                              ; receiver producer (prior)
006C4105 SUB ESP,0x18                                               ; ctx block
006C410A..4133 ctx := {0x00823C10, EDI=0, EBX, 0xA7957B, 0xA7957B, M32[E1-0x10] (lo byte 1, C3)}
006C4121 EDX := M32[C+4] (end); 006C4136 EAX := M32[C] (begin)
006C412E..4141 CALL 006C36B0(&out, begin, end, 0x00BA45E8)          ; projection loop (prior P10 + P01):
        per 8-byte pair: CALL 006C29D0 -> pump 00823C10 -> EAX DWORD
        -> append to global {begin@0xBA45E8, tail@0xBA45EC, limit@0xBA45F0}
        loop-complete path also writes *out := 0x00BA45E8 (prior @006C371B-371F)
006C4146 ESI := M32[0x00BA45EC]                                     ; global tail (pre-consumer)
006C414C ECX := M32[0x00BA45E8]                                     ; global begin
006C4152..415D PUSH (begin, tail, &out_slot, &wrapper)
006C415E *out_slot := 0                                              ; (the slot held 0x00BA45E8 on the loop-complete path)
006C4166 EDI := ESI                                                 ; tail snapshot
006C4168 [OPAQUE] CALL 0x008D6D90(begin, tail, &slot=0, &wrapper)   ; returns EAX = position (contract per B11)
006C416D ADD ESP,0x38                                               ; deferred cleanup (ctx + 2x4 args)
        EAX == tail?  --yes--> 006C4198 (EAX==EDI) --> 006C41B3      [NO-OP case]
        EAX+4 == tail? --yes--> 006C4198: EAX != EDI; SUB ESI,EDI = 0 -> JZ 006C41AE
                                                                      [ERASE-LAST case: tail := EAX = tail-4]
        else:
006C4180-4190 COMPACTION LOOP over [EAX+4, tail_snapshot):
             read cursor ECX, write cursor EAX; drop element iff *ECX == 0;
             element AT EAX dropped unconditionally (never tested)
006C4192 ESI := M32[0x00BA45EC]                                      ; RELOAD current tail (opaque callee may have advanced it)
006C4198 CMP EAX,EDI; JZ 006C41B3                                    ; nothing removed -> skip
006C419C SUB ESI,EDI = growth; JZ 006C41AE                           ; no growth -> tail := compacted end
006C41A0..41A9 [OPAQUE] CALL [0x00A753B4](dst=EAX, src=EDI, count=growth); ADD ESP,0xC
                                                                      ; relocate appended block down (memmove-like, returns dst)
006C41AC EAX += ESI; 006C41AE MOV [0x00BA45EC],EAX                    ; new tail
006C41B3 EAX := M32[C]                                                ; local container begin
006C41B7 TEST EAX,EAX; 006C41B9 SEH state := -1; JZ 006C41DD          ; null -> skip dealloc
006C41C3..41D4 [OPAQUE] CALL [0x00A759FC](begin, (limit-begin)&~7); ADD ESP,0x8
                                                                      ; dealloc-class cleanup of C's buffer
006C41DD..41F0 epilog: FS restore, POP cookie/EDI/ESI/EBP/EBX, ADD ESP,0x30, RET
EXCEPTIONAL: SEH handler 0x00A04968 (outside window) - unwind by state; no EAX contract
```

## 2. Value graph: source table entry → … → first real use of the global

| Edge | From → To | Mechanism / VA | Pointer level | Label |
|---|---|---|---|---|
| V1 | static table entry (0xA855F0/0xA858B8/0xA858C0 DWORD) → 006C3F50(id, C) | collect loops (prior P04/P05) | L0 value | CONFIRMED (closed prior) |
| V2 | id → resolved pair {0x66, A} appended at M32[C+4] (limit C+8, grow 006C2E00) | 006C3F50 body (prior P03 window) | L0→L1 | CONFIRMED (closed prior; resolution chain 0043A550→0072F580→007CE1E0 opaque) |
| V3 | C pair array [M32[C], M32[C+4]) → sort | 006C3D40(begin,end) @006C40D0 | L1 | STRONGLY_SUPPORTED introsort-shaped (prior P08; phases opaque) |
| V4 | C pair array → adjacent-equality scan → EAX = first-dup pos (or end) | 006C2C90 @006C40DF | L1 | CONFIRMED mechanism (prior P09; duplicate handler opaque) |
| V5 | (EAX != end) → 006C2C50(this=C, pos, end, &wrapper) | @006C40F6 | L1 | OPAQUE (unopened; receiver C proven by depth arithmetic) |
| V6 | C [begin,end] → 006C36B0(&out, begin, end, 0x00BA45E8) | reads @006C4121/4136; CALL @006C4141; S=E1−0x70 matches P01 S-map | L1 | CONFIRMED (C2/C4 cross-check) |
| V7 | each 8-byte pair → 006C29D0(pair via pointer-holder) → pump 00823C10 → EAX DWORD | P01 (sibling) | L2 holder → L0 return | CONFIRMED (mechanism; pump semantics opaque; return kind NOT_ESTABLISHED) |
| V8 | EAX → global element: M32[M32[0x00BA45EC]] := EAX; M32[0x00BA45EC] += 4 (limit guard M32[0x00BA45F0]; slow path 00475A10) | prior P10 @006C36E6-370F | L0→L1 | CONFIRMED (closed prior) |
| V9 | 006C36B0 loop-complete → *out := 0x00BA45E8 (out-slot E1−0x2C) | prior P10 @006C371B-371F via its arg1 | L1 | CONFIRMED (prior; empty-case path of 006C36B0 outside its window) |
| V10 | global header (begin,tail) → 008D6D90 range args; *out_slot zeroed first | reads @006C4146/414C; zero @006C415E; pushes @006C4156-415D | L1 header values | CONFIRMED (arg construction); consumer semantics OPAQUE |
| V11 | 008D6D90 EAX → position cursor in global array | CMP/LEA/loop @006C4170-4190 | L1 | CONFIRMED (in-window consumption); production of EAX OPAQUE (premise P6: valid position) |
| V12 | **global ELEMENT VALUES → TEST !=0 → keep/drop → in-place copy [EAX] := [ECX]** | @006C4180-4190 | L1 | **CONFIRMED — first PROVEN element-VALUE consumer of the global in the admitted chain** |
| V13 | tail growth (reload − snapshot) → block relocation [snapshot, current) → [compacted end, …) | SUB ESI,EDI @006C419C; CALL [0xA753B4](EAX,EDI,ESI) @006C41A3 | L1 | CONFIRMED mechanics; callee identity PLAUSIBLE (memmove-class) |
| V14 | EAX+ESI → M32[0x00BA45EC] (new tail) | ADD EAX,ESI @006C41AC; MOV [0x00BA45EC],EAX @006C41AE | L1 | CONFIRMED (bookkeeping, NOT allocation growth) |
| V15 | C buffer (M32[C], (M32[C+8]−M32[C])&~7 bytes) → [0x00A759FC] dealloc-class call | @006C41B3-41DA | L1 + byte size | STRONGLY_SUPPORTED role; identity PLAUSIBLE |
| V16 | global element → ANY id/pointer/handle interpretation | — | — | **NOT_ESTABLISHED (open edge)** — no admitted window interprets an element beyond !=0; candidates: inside 008D6D90 (unopened), inside pump 00823C10 (unopened), or later consumers outside all windows |

## 3. Dead/unused control facts (negative controls)

- The out-slot's prior content (0x00BA45E8, written by V9) is OVERWRITTEN with 0 before the 008D6D90 call (@006C415E) — the callee receives &slot with *slot = 0; the prior value is dead for this call (visible-census within admitted rows).
- The wrapper byte (E1−0x2D) is never initialized in any admitted window before its two address-uses (006C2C50 arg3, 008D6D90 arg4) — mechanism fact; interpretation opaque.
- No instruction in the P02 window dereferences an element VALUE as a pointer (B08) — the only pointer derefs are cursor positions and the global/C header loads.
- begin (0x00BA45E8) and limit (0x00BA45F0) are never written in this window (single global store = tail @006C41AE).

## 4. Axes (per C5)

- LOCAL_MECHANISM: CONFIRMED (this file + STACK_MAP.md balance).
- DATA_DOMAIN: NOT_ESTABLISHED, unchanged standing — "compile-time resource dependencies" hypothesis from static id tables remains a hypothesis; this window adds no domain evidence (V12 is a zero-test only).
- OPAQUE_EFFECTS: UNKNOWN — 008D6D90, [0x00A753B4], [0x00A759FC], 006C2C50, 00415670, 00823C10, plus prior-run opaque set (0043A550, 0072F580, 007CE1E0, 006C2E00, 00475A10, 006C24B0, 006C3740, 006C3330, 006C3640, 0040B070-conditional). The tail reload @006C4192 is an H2-compatible shape (callee may mutate the global) without proving any enqueue.
- WORLD_INSTANCE_RELATION: NONE established in admitted windows (V16 open; no scene/attach/transform instruction anywhere in the chain; pump unopened remains the only bridge candidate).
