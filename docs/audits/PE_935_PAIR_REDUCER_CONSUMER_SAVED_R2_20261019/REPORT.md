# PE-935 PAIR REDUCER / GLOBAL CONSUMER - SAVED R2 - FINAL REPORT

RUN_ID = PE_935_PAIR_REDUCER_CONSUMER_SAVED_R2_20261019
MODE = SAVED_ONLY_ADAPTIVE_RESEARCH_WITH_INDEPENDENT_REVIEW_AND_PUBLICATION
BASE_BINDING_NOTE = The contract pinned OUTPUT_ROOT ...SAVED_R1_20261019; guard start collided with an orphaned interrupted attempt of the same mission (no worker science, no STOP). Per CONTRACT section 2 collision clause, this run continues under the new binding ...SAVED_R2_20261019; R1 left untouched (PREFLIGHT_COLLISION_REPORT.md). FINAL_REPORT_PATH for THIS run = ...SAVED_R2_20261019\REPORT.md (this file).
WORLD_XYZ_RECOVERED = NO
HISTORICAL_PLACEMENT = NOT_ESTABLISHED
CURSOR_SOURCE_MEDIUM = UNKNOWN
CANONICAL_GATE_EFFECT = NONE
PENDING STATUS = PENDING_EXTERNAL_POSTAUDIT (no self-promotion to canonical/milestone)

## 1. CORRECTIONS_APPLIED (postaudit assimilation, before new science)

CORRECTIONS_APPLIED.json + CORRECTED_CHECKPOINT.json written before any new science. C1..C8 lemmas preserved throughout; QC_R1 confirmed compliance; no canon promotion; frozen runs untouched.

## 2. SCIENCE RESULTS

### 2.1 Etap A - adapter 006C29D0 (P01, worker pe-reconstruction, QC PASS)
- ADAPTER_ABI: thiscall; ECX = this = &ctx[2] (address inside the caller-copied 6-DWORD context), 4 stack args, callee-clean RET 0x10; incoming arg1 and arg4 DEAD in-window; returns 32-bit EAX.
- Pointer-holder discipline (C4) held: arg3 = S+0x10 points to the slot CONTAINING the current pair pointer; one deref level produces pair_ptr.
- ADAPTER_RETURN_ORIGIN: the ONLY normal EAX path is the CALL EAX @006C2A63 where EAX = M32[arg2] = ctx[0] = 0x00823C10 (direct call, receiver ECX = ctx[1]+ctx[2]) -> ESI @006C2A69 -> EAX @006C2A99. The literal context field IS executed - proven by body, not assumed (C6 resolved).
- Partial-store discipline: the adapter consumes only byte 0 of ctx[5]; upper 24 bits of the context DWORD (C3) are never read in-window.
- No writes to 0x00BA45E8 or the pair/context by the adapter itself; SEH exceptional exits carry no EAX contract.

### 2.2 Etap B - consumer 006C4060 and the first real use of the global (P02, worker, QC PASS_WITH_FINDINGS P3-only)
- 006C4060 is CLOSED at RET @006C41F0 (combined with closed priors; 9 branches in-window; no escape).
- GLOBAL PAIR: 0x00BA45E8/0x00BA45EC/0x00BA45F0 = vector {begin, tail, limit} (reload @006C4192, write @006C41AE, reads @006C4146/414C, loop bound @006C418E).
- FIRST_REAL_CONSUMER (first proven element-VALUE use): TEST != 0 @006C4182 in the forward in-place compaction loop @006C4180-4190 (drop-zero compaction; EAX write cursor, ECX read cursor); followed by block relocation via [0xA753B4] (memmove-like, STRONGLY_SUPPORTED structural) and dealloc-class [0xA759FC]; element values are NEVER interpreted otherwise in-window (never dereferenced).
- GLOBAL_ELEMENT_KIND = OBJECT_POINTER_OR_ZERO @ STRONGLY_SUPPORTED (standing change adjudicated in CORRIGENDUM_R1; kind-by-use premise: pump results are ECX receivers in 00826760/00826840 calls; callee conventions unopened).

### 2.3 Producer level - pump 0x00823C10 (P03, DIRECT_ANALYST_FALLBACK after 2 empty worker attempts, QC PASS_WITH_FINDINGS)
- ABI: thiscall, 4 stack args (arg1 pair_ptr; arg2/arg3 adapter locals; arg4 cursor word NEVER read), RET 0x10, full SEH frame; stack balance independently recomputed by QC (frame 0x3C; epilog POP x5 + ADD 0x28 = exact).
- The pump is an OBJECT RESOLVER consuming BOTH pair DWORDs: pair[0] @00823C41 (into 004D1430 constructor of receiver+4 and sub-object selection), pair[1] @00823D16 (arg to the loop resolver vtable+0x4 call).
- Normal return paths (corrected per CORRIGENDUM_R1): FAST (vtable+0x38 on [EDI+0x24] with pair_ptr) / LOOP (vtable+0x4 on [entry+8] with pair[1]) -> object pointer, acted on via 00826760 before return; NULL-A ([EDI+0x24]==0) / NULL-CAE / NULL-DFF -> 0.
- Return value kind: object pointer or 0 @ STRONGLY_SUPPORTED (kind-by-use); DATA_DOMAIN of the resolver objects NOT_ESTABLISHED (20 callees opaque); WORLD_INSTANCE_RELATION NOT_ESTABLISHED.

### 2.4 Etap C - value graph (source table entry -> ... -> first real use)

| edge | anchor | status |
|---|---|---|
| source table entry -> pair in shared container C | closed prior P04/P05 (C1 lemma scope) | standing |
| pair in C -> pair_ptr holder (arg3=S+0x10) | 006C36DD/006C36E1 | CONFIRMED (C4) |
| holder deref -> adapter this/args | 006C29D0 prolog | CONFIRMED (P01) |
| adapter -> pump CALL (target 0x00823C10, receiver ctx[1]+ctx[2]) | 006C2A53-63 | CONFIRMED (P01) |
| pair[0]/pair[1] -> pump resolver interfaces | 00823C41/00823D16 | CONFIRMED (P03) |
| pump -> returned EAX (object pointer or 0) | 00823C84 / 00823D24 / null paths | CONFIRMED origin; kind STRONGLY_SUPPORTED |
| adapter EAX -> global vector element (tail+=4) | closed prior P06/P07 fast path | standing |
| global element -> first real use (TEST!=0 compaction) | 006C4182 | CONFIRMED (P02) |

H1 SYNCHRONY: the visible chain is synchronous (no async flag observed IN THE ENUMERATED COMPLETE ROW SETS; opaque callee effects remain UNKNOWN - no exclusion, C5).
DATA_DOMAIN: NOT_ESTABLISHED for the resolver objects (opaque).
OPAQUE_EFFECTS: UNKNOWN (pump 20 callees; adapter import-slot callees; consumer 008D6D90/[0xA753B4]/[0xA759FC]; 006C2C50 premise).
MODEL_RESOURCE_INSTANCE_EDGE: NOT_ESTABLISHED. The chain is container/registry maintenance; no identity join to any scene instance; example 4508->296445 remains scoped standing (no obligation to prove, no attribution without an identity edge).
TRANSFORM_ORIGIN: NOT_ESTABLISHED in the primary thread.

### 2.5 Frontier pivot (CONTRACT section 8; P04, DIRECT_ANALYST_FALLBACK, QC PASS_WITH_FINDINGS)

PIVOT_RECORD.json compared: (a) writer SF+30 - ALREADY CLOSED by catalog-pinned PE_935_SCENEFEEDER_LINK30_IDENTITY (NiNode, RTTI-confirmed; TRANSFORM_TO_MODEL NOT_DEMONSTRATED); (b) receiver [this+2Ch] in 0085BFA0 / slot+24h - EXECUTED as the one bounded frontier question (absence of guaranteed success is not rejection).
Result: 0085BFA0 = get-transform: virtual slot+0x24 on the object at [receiver+0x2C] returns a pointer to 12-float transform data; the body converts it to a 0x34-byte output {3x3 rotation, translation, 1.0f} - STRUCTURAL_ONLY match with the Gamebryo NiTransform layout (NO class identity claimed, no RTTI in window). 0085C0C0 = get-position (slot+0x28, 3 floats). Callers: 0085C0F0 (zero 3-vector to own out-arg + 0096CD10, semantics UNKNOWN - corrected per corrigendum) and 0085C130 (partial: FSUB of receiver fields +0x54/+0x58 from the transform translation = relative-position math; live edge beyond 0x0085C160 declared).
NO identity edge between this frontier and the primary thread (slot-offset similarity is coincidence). This is the strongest structural TRANSFORM-candidate edge found in this run; object/receiver classes remain NOT_ESTABLISHED.

## 3. First missing edge (decision-relevant)

FIRST_MISSING_EDGE:
1. Resolver object class identity in the primary thread ([EDI+0x24] provider class; class of returned objects) - requires RTTI or runtime vptr; both out of saved-only scope.
2. Any identity bridge between the pair-transport thread and a scene/world instance.
3. Frontier thread: receiver class of 0085BFA0 and vtable identity of [this+2Ch] objects (needs a receiver-identity census; 0085C130 continuation beyond window is the concrete next admission if pursued).
4. Closed standing seam from LINK30: NiNode vtable slot 17 (0x007B5390) remains the strongest recorded open frontier for TRANSFORM_TO_MODEL.

Honest mission statement: this run improved the understanding of a model-pair transport chain into a resolver-backed registry with compaction maintenance (cache/preprocessing-shaped), and produced a separate structural transform-interface frontier; it did NOT approach building placement. The branch is NOT excluded from instance work (opaque callees; frontier candidate) and is NOT promoted to it (no identity edge).

## 4. PROCESS

- Guard chain: 5 events (START 14:19:01Z, ADMIT P01 14:21:23Z, P02 14:38:58Z, P03 15:00:59Z, P04 15:22:14Z) + STOP (this document precedes it). All extractions followed admissions; bijection 449/449 rows verified verbatim by QC.
- BUDGETS: reserved/charged bodies 14/32, listing rows 449/6000, CALL sites 39/200, candidates 12/32, body document lines 0/1500; INCIDENT_DEBITS 0 (all four windows contained their observed bodies within reservations; containment proven per body; no unexpected-body interpretation). Sum = union (no refund; full reservations charged).
- Delegation: P01/P02 by pe-reconstruction (complete). P03/P04: TWO consecutive empty child returns each (4 empty sessions total; no artifacts created) -> authorized DIRECT_ANALYST_FALLBACK_BY_PE_MASTER with full attribution in each package. This session-emptiness anomaly is recorded as an operational observation; no config changes attempted in-run (per CONTRACT section 9).
- QC: fresh pe-master-auditor QC_R1, complete with all mandatory independent tests (full ESP balance recomputation PASS; low-byte vs DWORD partial-store test PASS; exact pointer-holder argument test PASS; budget reserve+debits reconciliation PASS; re-hash and full bijection PASS). Verdicts: P01 PASS; P02/P03/P04 PASS_WITH_FINDINGS; run-level QC_PARTIAL resolved by CORRIGENDUM_R1 adjudication (13 ACCEPTED, 1 PARTIALLY_ACCEPTED, 0 REJECTED; no P1). AUDIT_OF_AUDITOR: PE-MASTER verified QC hashes, ledger times and re-checked the five P2 findings against raw extracts - all confirmed.
- No original-game operations (no exists/stat/hash of game binaries), no Ghidra/new exports, no runtime, no model/config changes, no Hermes, no nested tasks.

## 5. Publication

Additive publication on LIVE master in an isolated worktree performed after this report: sanitized projections of (1) the deep postaudit PE_935_MODEL_PAIR_TRANSPORT_DEEP_POSTAUDIT_R1_20261019, (2) this run PE_935_PAIR_REDUCER_CONSUMER_SAVED_R2_20261019, (3) AUDIT_NOTICE.md in the published MODEL_PAIR_TRANSPORT_QUALIFICATION directory, (4) one newest-first AUDIT_ENTRYPOINT 1/0 entry. Receipt (commit SHA, remote status) stored OUTSIDE the sealed root (PUBLICATION_RECEIPT_R1 directory). See PUBLICATION section of HANDOFF.md after execution.

## 6. Terminal block (CONTRACT section 11)

RUN_STATUS = COMPLETE_WITHIN_SCOPE_BARRIER_DOCUMENTED
SCIENCE_VERDICT = PRIMARY_CHAIN_QUALIFIED_AS_RESOLVER_REGISTRY_MAINTENANCE; DATA_DOMAIN/WORLD_INSTANCE NOT_ESTABLISHED; FRONTIER_CANDIDATE_EDGE_RECORDED
PROCESS_VERDICT = COMPLIANT_WITH_DOCUMENTED_FALLBACKS_AND_CORRIGENDUM (no P1; QC complete; 4 empty child sessions recorded as operational anomaly)
CORRECTIONS_APPLIED = C1..C8 preserved (CORRECTIONS_APPLIED.json); QC findings adjudicated (CORRIGENDUM_R1)
SHARED_CONTAINER_IDENTITY = one shared 3-DWORD header C=B+1Ch (C1 standing)
ADAPTER_ABI = 006C29D0: thiscall ECX=&ctx[2], 4 stack args, RET 0x10, unique normal return path
ADAPTER_RETURN_ORIGIN = CALL 0x00823C10 (ctx[0]) with receiver ECX=ctx[1]+ctx[2] @006C2A63 -> EAX @006C2A99; value = pump resolver result (object pointer or 0, STRONGLY_SUPPORTED)
CONTEXT_PARTIAL_BITS = ctx[5] low byte = 1 established; upper 24 bits unknown and unconsumed in-window
GLOBAL_ELEMENT_KIND = OBJECT_POINTER_OR_ZERO @ STRONGLY_SUPPORTED (kind-by-use premise)
FIRST_REAL_CONSUMER = element-VALUE test !=0 in the compaction loop @006C4182 of 006C4060 (drop-zeros compaction + relocation + dealloc; values never interpreted otherwise)
OPAQUE_EFFECTS = UNKNOWN (pump 20 callees; adapter/consumer import-slot callees; 008D6D90; 006C2C50 premise)
MODEL_RESOURCE_INSTANCE_EDGE = NOT_ESTABLISHED (no identity join; 4508->296445 remains scoped standing)
TRANSFORM_ORIGIN = NOT_ESTABLISHED in primary thread; separate frontier 0085BFA0 transform-interface candidate recorded (STRUCTURAL_ONLY)
FIRST_MISSING_EDGE = resolver class identity + any primary-thread-to-instance bridge; frontier receiver census + 0085C130 continuation; standing LINK30 slot-17 seam
BUDGETS = bodies 14/32; rows 449/6000; calls 39/200; candidates 12/32; doc-lines 0/1500; incident_debits 0; sum=union
DISPATCH = 4 admissions; 2 successful worker packages; 4 empty child sessions -> 2 DIRECT_ANALYST_FALLBACK packages (attribution recorded); QC_R1 complete (1 successful reviewer attempt)
MANIFEST = root MANIFEST_SHA256.csv built by guard seal AFTER STOP (bijection, nested manifests included, self-excluded)
