# AUDIT NOTICE - PE_935_MODEL_PAIR_TRANSPORT_QUALIFICATION_SAVED_R1_20261019

An independent deep postaudit (PE_935_MODEL_PAIR_TRANSPORT_DEEP_POSTAUDIT_R1_20261019, published alongside this package) and a follow-up saved-evidence run (PE_935_PAIR_REDUCER_CONSUMER_SAVED_R2_20261019) SUPERSEDE several summary conclusions of THIS package. The frozen source package is preserved byte-identical; this notice points readers to the corrections. Key corrections (all evidenced in the postaudit CLAIM_DISPOSITION.csv F01-F14 and the follow-up run):

1. ONE SHARED CONTAINER, not three: in 006C4060 the three collection callsites pass the SAME header C = B+0x1C (LEA @006C4095/006C40A8/006C40B7 all resolve to B+1C on normal returns). The "three containers" label is superseded.
2. ABI: in 006C36B0 ESI is arg4 = M32[S+0x10]; the caller passes the literal global sink 0x00BA45E8 as the FOURTH argument (not arg5).
3. PARTIAL DWORD: only the LOW BYTE of the sixth context DWORD is established as 1 (MOV byte [ESP+0x4C],1 @006C4125); the upper 24 bits are not fixed by the admitted stores.
4. POINTER HOLDER: at callsite 006C36E1 arg3 = S+0x10 points to the slot CONTAINING the current pair pointer (stored EDI @006C36DD); it is not the pair pointer itself.
5. OPAQUE EFFECTS: REJECTED for the label "H2 request transport excluded for the whole chain" - the opaque callees (006C29D0 and others) retain UNKNOWN effects; synchronous invocation is established, request/domain/async effects are not.
6. ACCOUNTING: the prior-run ledger has 13 events (START1 + ADMIT10 + DENY1 + STOP1), not 12 ADMIT; the correct no-refund charge is 22/24 bodies and 23/24 candidates; the P08 local admission breach (4 bodies vs 2 reserved) is not legalized by the global budget.

The follow-up run PE_935_PAIR_REDUCER_CONSUMER_SAVED_R2_20261019 additionally qualifies: the adapter 006C29D0 return origin (direct CALL 0x00823C10 with receiver ctx[1]+ctx[2] @006C2A63, unique normal path), the pump 0x00823C10 as an object resolver consuming both pair DWORDs, the global as a vector {begin 0x00BA45E8, tail 0x00BA45EC, limit 0x00BA45F0}, and the first proven real consumer of element VALUES (drop-zero compaction TEST @006C4182). GLOBAL_ELEMENT_KIND = OBJECT_POINTER_OR_ZERO @ STRONGLY_SUPPORTED. WORLD_INSTANCE / TRANSFORM relations remain NOT_ESTABLISHED.
