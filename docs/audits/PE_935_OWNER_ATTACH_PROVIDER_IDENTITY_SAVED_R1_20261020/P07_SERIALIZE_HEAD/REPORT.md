# P07_SERIALIZE_HEAD

RUN_ID: PE_935_OWNER_ATTACH_PROVIDER_IDENTITY_SAVED_R1_20261020 (package P07_SERIALIZE_HEAD)
Source: P07_SERIALIZE_HEAD extract, admission A5742dd0b9845. SAVED_TEXT_CATALOG only; no game files, no runtime, no scripts.
Attribution: PARENT_DIRECT (parent on nask-glm/glm-5-3-default).

## Verdict

The containing function is a large serializer: CALL EDI repeatedly converts a float local to double (FSTP qword [ESP]) and writes it, TEST EAX,0x207 error-checking each write (file-writer semantic, class identity not claimed). EBX is an outer object being saved: floats [EBX+0x20/24/28/2C] written, pointer [EBX+0x30], child-pointer array [EBX+0x50]/[EBX+0x54] iterated with per-child virtual slot+0x8 boolean call and byte+0x38 flag tests. The ESI=[ESP+0x34] provider object (+0x20 type int==3, +0x28 factory, +0x2C provider) is read for current state via provider slots +0xAC/+0xB0. Function entry lies before 0085C780 (not reached).

## Claims
See CLAIMS.json (strict JSON, separated statuses).
