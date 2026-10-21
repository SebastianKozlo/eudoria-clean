# REPORT - PE_935_X_STORAGE_IDENTITY_OPENCODE_SAVED_R1_20261020

RUN: X STORAGE IDENTITY AND TRANSFORM INPUT / OPENCODE GLM MEDIUM R1, on saved sources only.
Verdict: SCIENCE_VERDICT=PARTIAL_RESOLVED_STRUCTURALLY (priority questions of stages A and B answered; C conditional part answered; X<->R remains unjoined). PROCESS_VERDICT=COMPLIANT (all operand reads under REQUEST->PLAN->ADMIT->EXTRACT; budgets respected; QC performed; no incidents).

## Resolved questions

1. X_init_in (last live ECX at CALL 0085D410, 00858240): result of a SECOND, later allocation CALL 0095D3C4 with request 0x68 at 0085821e, cached at [ESP+0x18] and moved to ECX at 0085823e. This is NOT the earlier 0x80 allocation: the two are different call sites with different request sizes. Value equality remains UNKNOWN (allocator body not opened).
2. A_alloc_shape (0x80 result at 00857fe3) is linked by MOV ESI,EAX (0085800a) to the field-init blocks, receives 0x00a91db8 in its first DWORD at 00858059, and is pushed BY POINTER into a vector at 00858206. Prior SRB-C2 chain (X = fresh heap 0x80, vptr A91DB8) is thereby CORRECTED: the D410/C3B0 object is the 0x68 result; D410 zeroing does not threaten A91DB8 unless the allocator aliases the two results (unknown).
3. D410 ABI: thiscall-like; this = 0x68 result; single stack arg = dword [this_F858+0x44], where this_F858 = F858 entry ECX stored at [ESP+0x14] in the prologue (00857fba).
4. X_entry = X_init_out: EAX after D410 -> ESI (00858245) -> ECX (00858260) -> CALL 0085C3B0 (0085826d). On the 0x68-allocation-failure path ESI=0 and C3B0 is dispatched with this=0 (XSI-16).
5. C3B0 argument map: this=entry ECX; arg1=[EBP+8] (last pushed) is the 13-DWORD source copied by REP MOVSD to this+0x30; arg2 = LEA [ESP+0x34] (F858 local 13-float buffer, filled by FST/FSTP stores 00858108-0085816c); arg3 = 1.0f; arg4 = 1 -> this+0x20.
6. Transform input provenance: C3B0 arg1 = F858 incoming stack arg1 = LEA [callerESP+0x64] pushed at the SOLE direct caller CALL 0085a429 (complete literal CALL census of the pinned H5 listing) - i.e. a stack buffer inside the caller frame. The writer of that buffer (caller loop region 0085a331..0085a3fe) is NOT yet admitted: FIRST_MISSING_EDGE.
7. Frame gate: C3B0 prologue PUSH EBP/MOV EBP,ESP/AND ESP,~0x3F/SUB 0xF4/3 pushes; frame cell [ESP+0x34]=entry ECX stored 0085C3C1; read back 0085CA3F and 0085CD06. Full linear coverage [0085C3B0,0085CD10): single writer; only balanced SUB/ADD ESP,8 pairs; the only LEA passed to a call is [ESP+0x24]; all in-range branch targets covered; single forward exit 0085CD27. Preservation STRONGLY_SUPPORTED (static); X_store==X_entry STRONGLY_SUPPORTED (upgrades prior CONDITIONAL).
8. U28/V18 chain re-derived fresh: U28=[X_store+0x28] (0085cd0a), vptr slot +0x18 called (0085cd13), result V18 -> [X_store+0x2c] (0085cd17). NEW beyond prior runs: consumer P=[X_store+0x2c] (0085cd27) with vtable slots +0x4c/+0x50 called, then array iteration [EBX+ESI*4] with element vtable slot +0x84 (structural observation only).
9. X_store <-> R (R=M32[B+0xC] of the 00527AB0 path): NOT_ESTABLISHED; no admitted data relates them. R_CLASS_IDENTITY remains NOT_ESTABLISHED. No speculative census opened.

## Standing limitations
- All analysis is STATIC on the pinned saved listing; no runtime, no original EXE, no game data.
- Allocator 0095D3C4 semantics (freshness/aliasing) not opened.
- DF=0 and live aliasing are static assumptions (XSI-08 ceiling: STRONGLY_SUPPORTED).
- 0x80/0x68 are allocator requests; size semantics not proven.
- Internal QC ran on the same GLM-5.3 family (fresh context, not model-independent). External Desktop post-audit PENDING.

## Corrections applied from the deep postaudit
See CORRECTIONS_APPLIED.json (SRB-C1..C9 all applied; R=A7DCB0 census abandoned; priority redirected to the F858 gap).

## Budgets
rows 953/10000 (union 953), calls 59/400, body reservations 40/64, candidates 20/64, incidents 0, denials 0.

## Model
Coordinator ses_ea2f8ce67ffeM0nfb7KgqtcHXG (pe-master, glm-5-3, medium client options); smoke, worker, reviewer sessions recorded in MODEL_ATTESTATION.json and ROLE_LEDGER.json. REQUEST_EFFORT=NOT_OBSERVED, SERVER_EFFECTIVE_EFFORT=UNKNOWN.

WORLD_XYZ_RECOVERED=NO
HISTORICAL_PLACEMENT=NOT_ESTABLISHED
CURSOR_SOURCE_MEDIUM=UNKNOWN
CANONICAL_GATE_EFFECT=NONE
