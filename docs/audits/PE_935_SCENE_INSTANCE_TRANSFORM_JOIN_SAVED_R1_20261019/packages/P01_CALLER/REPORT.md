# P01_CALLER REPORT — caller of 0085BFA0 at [0x00527AA0,0x00527B20)

RUN_ID: PE_935_SCENE_INSTANCE_TRANSFORM_JOIN_SAVED_R1_20261019 | package P01_CALLER | worker pe-reconstruction
Evidence: P01_EXTRACT, admission A27148d95e802, source pin 642CC29A01B8AD6F783E82E14DA4A61FA00BA6A3EC6DF98EDFF28AC25CC1D8DB, 37 rows (listing 180895-180931), 2 CALL sites, body complete in-window (RET 0x4 @0x00527B1D).
Read-only prior context (frozen): PE_935_PAIR_REDUCER_CONSUMER_SAVED_R2_20261019 (REPORT.md, P04_FRONTIER/{REPORT.md,CLAIMS.json}, P04_EXTRACT). No new admissions, no game files, no scripts, no runtime.

## 1. Reconstructed body (row-anchored)

00527AA0 is a **thiscall method** (ECX=this, one stack arg ARG1=[E+4], RET 0x4). Prolog: SUB ESP,0x34 (the entire frame is a 13-dword out-buffer — see §3), PUSH EBX, MOV EBX,ECX (owner register), PUSH EDI. **EDI = [this+0xC]** is loaded at entry and null-guarded; **[this+0x10]** is null-guarded next; either null → no-op early exit to the common epilogue.

FPU block (working labels only): owner_float_E0 := +0.0 always; if float@0x00A797C8 < owner_float_E4 (ordered) then owner_float_E8 := owner_float_E4; owner_float_E4 := +0.0 always (TEST AH,0x5/JP = jump-if-not-less idiom; full table in STACK_MAP §5; FPU depth 0 at exit on all paths, STACK_MAP §4).

Then: LEA EAX,[ESP+0xC] (= frame base = the 13-dword buffer), PUSH EAX, MOV ECX,EDI, **CALL 0085BFA0 @0x00527AF9**. Post-return: ADD EDI,0x30; MOV ESI,EAX; MOV ECX,0xD; REP MOVSD → 13 dwords copied to receiver+0x30 (§3). Post-copy: ECX=[ESP+0x44]=ARG1, PUSH ECX; ECX=[this+0x10]; **CALL 00861150 @0x00527B12** — the function forwards its own incoming ARG1 to 00861150 with receiver [this+0x10] (mechanical only; 00861150 unopened → UNKNOWN). Epilogue: POP ESI/POP EDI/POP EBX/ADD ESP,0x34/RET 0x4. ESP exactly balanced on both paths (STACK_MAP §1-2); both callees clean their single arg (STACK_MAP §3).

## 2. Axis answers (statuses)

| axis | answer | status |
|---|---|---|
| **OWNER_IDENTITY** | UNKNOWN. Profile only: object with pointer fields +0xC (transform receiver) and +0x10 (00861150 receiver), both null-guarded; float fields +0xE0/+0xE4/+0xE8. No vptr/RTTI/ctor/xref of 00527AA0 in window; not established as SceneFeeder or any named class. Missing info: caller census of 00527AA0, or saved RTTI/vtable for its this, or ctor/writer of its fields. | UNKNOWN / NOT_ESTABLISHED (P01-C12) |
| **RECEIVER_POINTER_ORIGIN** | ECX at CALL = EDI = **[EBX+0xC]** = M32[this+0xC] — exactly ONE dereference, loaded once @0x00527ab7 (row 180899), guarded non-null, moved unchanged to ECX @0x00527af7. MOV (not LEA) ⇒ receiver is the VALUE stored at owner+0xC, not an embedded object at +0xC. Writer/write-time of [this+0xC]: NOT in any admitted window → UNKNOWN. Whether the pointed-to object is embedded elsewhere in the owner's allocation or separately allocated: UNKNOWN. | origin CONFIRMED (P01-C03); producer UNKNOWN (P01-C13) |
| **ARG at the call** | PUSH EAX where EAX=LEA [ESP+0xC]=E-0x34 = base of the 0x34 SUB allocation ⇒ the arg is a pointer to the 13-dword local stack buffer; the buffer IS the whole frame (no other locals). Post-return EAX→ESI; EDI pre-ADD'ed 0x30; REP MOVSD ×13 dwords ⇒ **the receiver object receives a 13-dword (0x34-byte) copy of the transform output at receiver+0x30** (rows 180919-180922). Per frozen prior R2 P04: output = 9-dword rotation + 3-dword translation + 1.0f; EAX at 0085BFA0's RET = &out-arg (last EAX write = MOV EAX,[ESP+0xAC] @0x0085C06A, no later clobber). Stated as dataflow; no class identity claimed. | CONFIRMED (P01-C07/C09) |
| **FIELD_2C_WRITER** | UNKNOWN. The [receiver+0x2C] read is inside 0085BFA0 @0x0085BFA6 (frozen prior R2 P04-K01); the WRITE of that field is in NO admitted window (neither here nor in R2 P04). Missing info: constructor/store into receiver+0x2C — requires receiver-identity census first. | UNKNOWN (P01-C15) |
| **STORED_OBJECT_CLASS** | UNKNOWN (object at [receiver+0x2C]). Prior frozen R2 P04-K08: NOT_ESTABLISHED; structurally exposes slot+0x24 (12-float data) and slot+0x28 (3 floats); NiTransform-layout match is STRUCTURAL_ONLY. No new identity evidence in this package. | UNKNOWN / NOT_ESTABLISHED (P01-C16) |
| **FIELD_PRESERVATION_AT_CALL** | UNKNOWN for object fields across the CALLs (callee bodies unopened; no evidence 0085BFA0/00861150 write owner/receiver fields). Partial confirmed facts: caller's own frame is path-exact; caller assumes non-volatile EBX (uses [EBX+0x10] after CALL 0085BFA0). Construction-to-read preservation of +0x2C not assessable (no construction event in evidence). | PARTIAL (P01-C17) |
| **SLOT24_TARGET** | Not in this window (dispatch is inside 0085BFA0). Standing frozen prior R2 P04-K02 (CONFIRMED there): slot+0x24 on [[receiver+0x2C]] returns a pointer to 12 floats consumed to build the 0x34 output. Identity of the slot+0x24 target function/class: UNKNOWN. Carried prior context, not re-proven here. | mechanism: standing prior CONFIRMED; identity UNKNOWN (P01-C18) |
| **SLOT28_TARGET** | NOT exercised on this path — zero indirect dispatch in this window. Prior standing (R2 P04-K04): slot+0x28 used by 0085C0C0 (position getter, 3 floats) on a different receiver path. | NOT_ON_THIS_PATH; identity UNKNOWN (P01-C19) |

## 3. Transform dataflow (rows)

1. 180895: SUB ESP,0x34 — frame = 13-dword buffer [E-0x34, E).
2. 180915/180916: EAX = &buffer; PUSH EAX — buffer pointer is the sole stack arg.
3. 180917: ECX = [this+0xC] — receiver.
4. 180918: CALL 0085BFA0 — callee (frozen prior: reads [receiver+0x2C] @0x0085BFA6, virtual slot+0x24 → 12 floats, writes {9 rot, 3 trans, 1.0f} into out-arg, returns EAX=&out-arg, RET 0x4).
5. 180919: EDI = receiver+0x30 (destination pre-adjustment — one ADD level on the receiver pointer; NOT an embedded-class adjustment proof).
6. 180920-180922: ESI=EAX; ECX=0xD; REP MOVSD — buffer → receiver+0x30..+0x63.
7. Net: **receiver region +0x30..+0x63 := the 13-dword transform output**; the local buffer is fully consumed; 00527AA0 then proceeds to the 00861150 call.

Structural note (no unification, P01-C24): frozen prior R2 P04 shows a DIFFERENT caller (0085C130 @0x0085c14c) passing LEA ECX,[its_receiver+0x30] as a this-pointer. Same offset, different receiver provenance, no same-object join — offset equality is not type equality.

## 4. Countermodels / negative controls

- REJECTED: owner = SceneFeeder or any named class (no window evidence; LINK30 SF+0x30 is a different owner/field path) — P01-C20.
- REJECTED: receiver/stored-object = NiNode/NiAVObject via NiTransform-layout similarity (prior STRUCTURAL_ONLY preserved) — P01-C21.
- REJECTED: FPU leak on either JP direction (explicit depth trace) — P01-C22.
- REJECTED: "buffer is only part of the frame" (LEA lands on frame base; copy consumes exactly 0x34 bytes) — P01-C23.
- Examined and rejected: 0085BFA0-as-cdecl reading of [ESP+0x44] (would forward the saved return address as an argument; contradicted by pinned prior RET 0x4) — P01-C08 / STACK_MAP §3.
- Honesty guard: "no evidence" is not used as proof of absence anywhere above; every UNKNOWN lists its exact missing information.

## 5. What this package does NOT establish

Class identities (owner, receiver, stored object), the writer of receiver+0x2C, the writer of [this+0xC], semantics of 00861150 and of ARG1, the value/meaning of global float 0x00A797C8, any world-instance or model-resource join, and any historical placement. WORLD_XYZ_RECOVERED=NO, HISTORICAL_PLACEMENT=NOT_ESTABLISHED (unchanged; no such claim attempted here).

## 6. Process

Deliverables in P01_CALLER\: RUN_STARTED.json (first artifact, real UTC), CLAIMS.json (26 claims P01-C01..C26), STACK_MAP.md, FLOW.md, REPORT.md, HANDOFF.md, STAGE_ACCEPTANCE_GATES.csv, artifact_index.csv, WORKER_BUDGET.md. Budget: only the admitted P01 extract used; no new admissions; see WORKER_BUDGET.md.
