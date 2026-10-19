# P04 FRONTIER REPORT - receiver [this+2Ch] in 0085BFA0 / slot+24h (PIVOT per CONTRACT section 8)

ATTRIBUTION: DIRECT_ANALYST_FALLBACK_BY_PE_MASTER (two empty worker attempts; RUN_STARTED.json).
SCOPE: admitted window [0x0085BFA0,0x0085C160), 135 rows, 7 CALL sites, pinned H5 listing. Read-only context: PIVOT_RECORD.json of this run, closed prior LINK30_IDENTITY (SF+30 = NiNode, TRANSFORM_TO_MODEL NOT_DEMONSTRATED). No original/runtime/Ghidra operations.

## 1. Body 0085BFA0 (CONFIRMED, straight-line, no jumps)

Frame: SUB ESP,0xA0; PUSH ESI; PUSH EDI (after two stack arg uses). ABI: thiscall, ECX=this(receiver), ONE stack arg (out-pointer; RET 0x4 @0085C0B4).
Receiver read: MOV ECX,[ECX+0x2C] @0085BFA6 -> this2 = receiver field +0x2C.
Dispatch: MOV EAX,[ECX] (vtable of this2); MOV EAX,[EAX+0x24] (SLOT +0x24); PUSH ESI; PUSH EDI; LEA EDX,[ESP+0x78]; PUSH EDX; CALL EAX @0085BFB5 - virtual call with ECX=this2 and one stack arg (address of a local buffer).
Source data: callee returns EAX pointing to 12 floats ([EAX..EAX+0x2C]) - copied via FLD/FSTP into stack slots @0085BFB7-0085C00D (with an argument-area rebuild SUB ESP,0x24 and a reorder chain @0085C011-0085C055 producing a contiguous 12-float block at [ESP..ESP+0x2C]).
Helpers: CALL 0x0096CB20 @0085C058 (matrix/basis computation from the 12 floats; unopened), CALL 0x0096CF80 with ECX=&[ESP+0x54] @0085C061 (fills a 9-dword block at [ESP+0x54]; unopened).
Output build: MOV EAX,[ESP+0xAC] (the caller out-pointer) @0085C06A; LEA ESI,[ESP+0x54]; MOV EDI,EAX; FLD1 @0085C094 (constant 1.0f); REP MOVSD with ECX=9 @0085C094 - copies the 9-dword matrix into out[0..0x24); then MOV [EAX+0x24],[ESP+0x8] @0085C09C-9F, MOV [EAX+0x28],EDX @0085C0A3, MOV [EAX+0x2C],[ESP+0x10] @0085C0A7, FSTP [EAX+0x30] @0085C0AB (stores 1.0f).
OUTPUT LAYOUT (in-window, structural): 9-dword rotation matrix + 3-dword translation + one 1.0f dword = 0x34 bytes. This byte layout EQUALS the classic Gamebryo NiTransform {rot:3x3, translate:3, scale:1} - STRUCTURAL_ONLY match; no RTTI, no class identity claimed.
SEMANTICS: 0085BFA0 = get-transform(receiver): virtual slot+0x24 on [this+0x2C] returns a pointer to 12-float transform data; the body converts it to a NiTransform-layout 13-dword output with scale pinned to 1.0f.

## 2. Body 0085C0C0 (CONFIRMED, straight-line)

Same receiver read [ECX+0x2C] @0085C0C0, vtable SLOT +0x28 @0085C0C5; local 3-float buffer; CALL EAX (ECX=this2, arg=&buffer); FLD/FSTP copies [EAX..EAX+8] (3 floats) to the caller out-pointer @0085C0D1-0085C0E4; RET 0x4.
SEMANTICS: get-position(receiver): slot+0x28 returns pointer to 3 floats. The [this+2Ch] object thus exposes BOTH a transform interface (slot+0x24) and a position interface (slot+0x28).

## 3. Callers in window (CONFIRMED as far as visible)

0085C0F0: CALL 0x0085BFA0 with out=&[ESP+0x2C] @0085C0FA; FLDZ; copies the 9-dword rotation; then writes THREE ZERO floats (FST/FST/FSTP from FLDZ) into the translation of the copied transform; CALL 0x0096CD10 (unopened; matrix op with this=&[ESP+0xC] and the zero-translation transform); RET 0x4. Pattern = build a rotation-only transform (translation zeroed).
0085C130 (PARTIAL, cut at window end): MOV ESI,ECX (saves receiver); CALL 0x0085BFA0 @0085C13B with out=&[ESP+0x4C]; FLD [ESP+0x70] (out+0x24 = translation.x); FSUB [ESI+0x54] @0085C144; FLD [ESP+0x78] (out+0x28 = translation.y); FSUB [ESI+0x58] @0085C157 - RELATIVE-POSITION math: subtracts the receiver's own float fields +0x54/+0x58 from the transform's translation. LIVE EDGE: body continues beyond 0x0085C160 (cut mid-expression FLD [ESP+0x7C] @0085C15E) - NOT interpreted beyond the window; would require a NEW admission if pursued.

## 4. Frontier verdict (axes separated)

LOCAL_MECHANISM: CONFIRMED - virtual transform/position interface on the object at receiver+0x2C, NiTransform-layout output with unit scale, relative-position subtraction in a caller.
DATA_DOMAIN: receiver class NOT_ESTABLISHED; [this+2Ch] object class NOT_ESTABLISHED (STRUCTURAL_ONLY layout match with NiTransform; slots +0x24/+0x28 identity vs known vtables NOT verified in this window). No RTTI in window. Per CONTRACT: no NiNode/NiAVObject substitution.
OPAQUE_EFFECTS: UNKNOWN for 0096CB20, 0096CF80, 0096CD10 and the virtual callees.
WORLD_INSTANCE_RELATION: NOT_ESTABLISHED as an identity; BUT this is an instruction-level TRANSFORM-PRODUCING chain on a saved frontier - the strongest structural candidate edge found in this run for future instance/transform work (candidate, not confirmed).

## 5. Relation to the primary thread (explicit negative)

NO identity edge exists in the admitted windows between this frontier and the primary thread (pump [EDI+0x24] resolver, global vector 0x00BA45E8/0xBA45EC). The numeric similarity of slot offsets (+0x24) is COINCIDENCE, not identity (different receiver provenance, different dispatch construction). The primary branch stays DATA_DOMAIN NOT_ESTABLISHED; the frontier adds a SECOND, separate thread, not a join.

## 6. Comparison with closed prior results

- Closed PE_935_SCENEFEEDER_LINK30_IDENTITY (catalog): SF+0x30 = refcounted NiNode (RTTI-confirmed); TRANSFORM_TO_MODEL NOT_DEMONSTRATED. This window does not touch SF+0x30 and cannot bridge to it without a receiver-identity census (future work).
- Closed prior PIVOT_RECORD (qualification run): rejected the 0085BFA0 census for ITS budget; this run executed the bounded body question as ordered by CONTRACT section 8.

## 7. Containment and budgets

0085BFA0 and 0085C0C0 and 0085C0F0 are complete straight-line bodies in-window (no jumps at all); 0085C130 is partial with a declared live edge beyond the window end. 4 bodies observed <= 4 reserved (NO incident debit); candidates charged 3/3 (0096CB20, 0096CF80, 0096CD10 nominated; 0 opened); rows 135; calls 7. No original/runtime/Ghidra/nested/Hermes/config operations.

RUN_STATUS = COMPLETE_WITHIN_ASSIGNED_SCOPE (pivot question answered within the window; 0085C130 continuation NOT pursued - not required by the pivot question).
