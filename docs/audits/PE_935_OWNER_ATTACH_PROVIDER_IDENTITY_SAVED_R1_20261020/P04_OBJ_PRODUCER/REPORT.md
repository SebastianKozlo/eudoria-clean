# P04_OBJ_PRODUCER

RUN_ID: PE_935_OWNER_ATTACH_PROVIDER_IDENTITY_SAVED_R1_20261020 (package P04_OBJ_PRODUCER)
Source: P04_OBJ_PRODUCER extract, admission A07454ff97918. SAVED_TEXT_CATALOG only; no game files, no runtime, no scripts.
Attribution: PARENT_DIRECT (parent on nask-glm/glm-5-3-default).

## Verdict

OBJ deserialized via the thunk is a STACK-LOCAL temporary at [ESP+0x18] of the 0048EDxx stream-load function, constructed in place by CALL 0085BBE0 at 0048EDDF, then deserialized (thunk) and further consumed by 0085B840/004123D0. OBJ is not a heap object, not a field of an owner, not R; the 0085BD80 store+2C thread is definitively not the R+0x2C provider writer for this chain.

## Claims
See CLAIMS.json (strict JSON, separated statuses).
