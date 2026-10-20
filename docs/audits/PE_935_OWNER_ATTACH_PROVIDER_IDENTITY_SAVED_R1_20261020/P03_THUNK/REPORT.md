# P03_THUNK

RUN_ID: PE_935_OWNER_ATTACH_PROVIDER_IDENTITY_SAVED_R1_20261020 (package P03_THUNK)
Source: P03_THUNK extract, admission A9c13761e27e7. SAVED_TEXT_CATALOG only; no game files, no runtime, no scripts.
Attribution: PARENT_DIRECT (parent on nask-glm/glm-5-3-default).

## Verdict

0085BF00 is a cdecl 2-arg adapter DeserializeThunk(ARG1=reader,[ESP+4]; ARG2=OBJ,[ESP+8]): ECX:=ARG2 becomes this for 0085BD80, ARG1 pushed as its reader arg, returns ARG1 in EAX. 0085BF20 init-writes {ARG1,0,1/ARG1,0,0} to [ECX]; 0085BF50 is a ratio/time accumulator on a POD (int,int,float,float,float); neither writes vptr or object pointers.

## Claims
See CLAIMS.json (strict JSON, separated statuses).
