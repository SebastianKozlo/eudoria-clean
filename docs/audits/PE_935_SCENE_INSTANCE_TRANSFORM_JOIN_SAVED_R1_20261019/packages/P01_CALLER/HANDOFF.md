# P01_CALLER HANDOFF

RUN_ID: PE_935_SCENE_INSTANCE_TRANSFORM_JOIN_SAVED_R1_20261019 | package P01_CALLER | worker pe-reconstruction
RUN_STATUS: COMPLETE_WITHIN_ASSIGNED_SCOPE (Etap A caller window fully analyzed; identity axes honestly UNKNOWN where unevidenced)

## Established (CONFIRMED, row-anchored)

- 00527AA0: thiscall method, ECX=this→EBX, ARG1=[E+4], RET 0x4; frame = exactly the 13-dword out-buffer; ESP balanced on both paths; FPU depth 0 at exit on all paths (incl. JP branch).
- RECEIVER at CALL 0085BFA0 = [this+0xC], single dereference, loaded @0x00527ab7, null-guarded; ECX set @0x00527af7.
- CALL 0085BFA0 @0x00527AF9: (ECX=[this+0xC], stack=&buffer); callee RET 0x4 (in-package ESP coherence + frozen R2 P04-K01). EAX at return = &buffer (frozen R2 P04 rows 1170983-1171004: last EAX write MOV EAX,[ESP+0xAC], no later clobber).
- Dataflow: 13-dword transform output {9 rot, 3 trans, 1.0f} copied via REP MOVSD to **receiver+0x30** (rows 180919-180922).
- Post-call: ARG1 forwarded as sole stack arg to CALL 00861150 @0x00527B12 with ECX=[this+0x10] (callee cleans 1 arg — proven by epilogue pairing). Mechanical only.
- FPU block: field_E0:=+0.0 always; if float@0x00A797C8 < field_E4 then field_E8:=field_E4; field_E4:=+0.0 always. Working labels only.

## UNKNOWN axes (exact missing information)

- OWNER_IDENTITY: needs caller census/xref of 00527AA0, or saved RTTI/vtable for its this, or ctor/writer of its fields (+0xC/+0x10/+0xE0-E8).
- Writer of [this+0xC] (receiver producer): not in any admitted window.
- FIELD_2C_WRITER: write of [receiver+0x2C] in no admitted window; needs receiver-identity census first, then ctor/store body.
- STORED_OBJECT_CLASS: [receiver+0x2C] object class NOT_ESTABLISHED (prior STRUCTURAL_ONLY stands).
- SLOT24_TARGET identity: slot+0x24 target function/class UNKNOWN (mechanism standing from frozen R2 P04-K02).
- SLOT28_TARGET: not on this path at all.
- 00861150 semantics; ARG1 type/semantics; global float 0x00A797C8 value/meaning: UNKNOWN.

## Next-edge options (parent decides admissions; not requested here)

1. Caller census/xref for 00527AA0 → OWNER_IDENTITY + writer of this+0xC (removes the first unknown on MODEL_RESOURCE→INSTANCE_ROOT→TRANSFORM_SOURCE for this thread).
2. Receiver-identity census: who constructs objects stored at owner+0xC → then the writer of receiver+0x2C.
3. 00861150 body (only if the forwarded ARG1 / owner+0x10 role is decision-relevant).

## Verdict for the run

This package converts the caller side of the 0085BFA0 edge from unopened to fully reconstructed: exact receiver origin, exact arg/out-buffer, exact 13-dword copy destination receiver+0x30, exact stack/FPU discipline. It deliberately does NOT promote any layout match to class identity (countermodels P01-C20..C23 REJECTED).

Evidence base: only P01_EXTRACT (admission A27148d95e802) + frozen R2 read-only context. No new admissions, no game files, no scripts, no runtime, no nested tasks.
