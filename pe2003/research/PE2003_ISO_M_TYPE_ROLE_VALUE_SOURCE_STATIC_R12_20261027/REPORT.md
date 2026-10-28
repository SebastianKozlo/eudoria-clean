# PE2003_ISO_M_TYPE_ROLE_VALUE_SOURCE_STATIC_R12_20261027 — public sanitized report (advisory)

Era/build: ISO2003NOV_PE_5_1_0_0 (client 5.1.0.0). Image: section1.bin, SHA256 D43A23B9EFCFC9BC4092B38FA3C73499DE7DE7B03B20F34478B9E81EE8893631, flat mapping base 0x401000. 100% STATIC_ONLY: zero runtime, zero game execution, zero original-code emulation. Models under investigation: 296445.nif, 218757.nif. Placement result: WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CANONICAL_GATE_EFFECT=NONE. This publication is a sanitized projection of the sealed local science package; it carries conclusions, VAs, statuses and provenance only (no raw instruction encodings, no payload bytes).

## Results (static, QC-verified)

1. The F-type gates 0x6C3A50 and 0x6C3898 are 16 bytes of static zeros each; the comparisons at 0x447B55/0x447BCA are address-identity tests of chain nodes returned by the virtual M+4 dispatch. TYPE_TAG_NAME=UNKNOWN; FILTER_BRANCH=CONFIRMED (mechanics); ACTUAL_M_TYPE=UNKNOWN.
2. Full-image census: 121 static references to both node constants (89 + 32) and ZERO static writers — the nodes are runtime-initialized class-identity nodes; their writer is not statically observable in section1. Two absolute reads (0x407664, 0x416401) feed their results into calls — candidate identity consumers, open.
3. Function 0x447B20 is CLOSED as a structural VISITOR: early-out via H+18; loop A over the intrusive list at M+BC via callback H+14 (head-restart when the callback returns true — the list may mutate); class gates versus both node constants; children phase H+8 begin / H+4 depth counter / H+10 accept filter over the array at M+EC (count M+F4) / refcounted fetch at M+D4 plus release / H+C end; the function result is AL of H+4(M). VISITOR=CONFIRMED structural (callback semantics unqualified); SCENE_GRAPH/RESOURCE role=PLAUSIBLE; the earlier "query/detach-only" reading is REJECTED as a whole-function reading (the releases are refcount cleanup of temporaries).
4. Exactly 3 direct callers: 0x53BE60, 0x53BF30 (a twin init pair), 0x53C780 (an in-run mis-attribution to 0x53C890 was RETRACTED).
5. 0x53C780 is virtual slot +0x18 of a full 7-slot primary vtable 0x65E6F4 (no RTTI at -4; deleting dtor 0x53BCD0; shared base slots in the 0x447xxx range — "derived-from" needs a base decode = open). Its loop names children "ParticleMeshModifier_Index" via helper 0x440350 -> M::SetName 0x41AFB0 (owned name copy at M+8). M is a named-node object graph: vtable / +4 refcount / +8 name / +0xC link / +0x10 back-link (bidirectional refcounted attach at 0x41B000). MODEL_PIPELINE_CONNECTION=PLAUSIBLE (Gamebryo particle-mesh-modifier vocabulary; no direct NIF/model-file proof; CLASS_IDENTITY=UNKNOWN).
6. R11 falsifications resolved: 0x402650 is a 4-byte getter returning &S+0x1C (plain ret) — NOT the ".cfg" consumer; the real consumer is 0x401260, a cdecl 3-argument builder of the string `<content of member S+0x1C>+".cfg"` (range-copy/range-append string API; SEH; caller cleans). CONFIG_VS_INSTANCE of the S population at callsite 0x401140 = CONFIRMED (CONFIG); E_builder = CONFIRMED INSTANCE DATA (static "." copied into this+0x54 per instance); population S/E_builder pushed away from placement; E_fetch 0x564890 and class E remain open. The SGAP (0x4011EB..0x401F0) is NOT_EXECUTED_MOOT (config population; the bridge is not needed for placement; the gap remains scientifically open, deprioritized).
7. The F-branch is closed: 0x52F290 returns its receiver (vtable 0x65E62C; +4 refcount=0; +8 is a 0x3C subobject built by 0x52C610 with the [F+1C] value and the F+24 address — the ONLY F-derived content; +0xC is a subobject from 0x5409A0 with constants -1.0f/0/0/0/-1.0f — a transform-like default, ABI-presumption; the R11 residual "retval = same fresh 0x3C block" is RESOLVED NEGATIVELY). 0x52C610 is a thiscall constructor of the 0x3C subobject copying the [F+1C] dword verbatim with a low-byte tag broadcast; F_FIELD_SEMANTICS=PLAUSIBLE (dword; FP-vs-int unresolved); VALUE_SOURCE_CONNECTION=PLAUSIBLE (a value-join/copy, not a transform).

## Model case status

- 296445.nif: all six case-cert fields remain OPEN (no source-specific asset observation, no definition join, no instance identity, no transform source, no authentic values, no frame). COMMON mechanism knowledge advanced only.
- 218757.nif: same status. A common mechanism never closes the join for a specific model.

## Best missing edges (for the next run)

L1: decode 0x5409A0 (the default transform subobject constructor). L2: instantiation census of the true constructor (tail 0x53BCC0) -> RUNTIME vs TOOL_EXPORT. L3: base vtable family decode (derived-from). L4: decode the surroundings of the node absolute reads 0x407664/0x416401.

## Process (advisory)

22 native dispatches vs 19 reserved science TASK admissions (PROCESS_DEFECT_P1_ACCOUNTING disclosed — 3 dispatches without their own reservations; limits untouched; ledger 48 events incl. the 768 MiB PUB_IO reservation; closing reserve intact). QC waves QROLE1 QC_PASS, QSCI1 QC_PASS (2 errata written additively), QACCOUNT QC_PASS. 3 empty child final messages with work verified from disk; 1 mis-anchored VOID attempt (PMM1) isolated; per-op exposures measured=UNKNOWN (charges only). Sealed package: 161 files, exclusive manifest verified; the seal receipt lives outside the science tree.

WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; SOURCE_SPECIFIC_ISO_MODELS=NOT_OBSERVED_IN_BOUNDED_SEARCH; LOCAL_SOURCE_EXHAUSTED=NO; CANONICAL_GATE_EFFECT=NONE; EXTERNAL_POSTAUDIT=PENDING; EU935 milestones untouched.
