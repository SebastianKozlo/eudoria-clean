# P06_PROVIDER_FACTORY

RUN_ID: PE_935_OWNER_ATTACH_PROVIDER_IDENTITY_SAVED_R1_20261020 (package P06_PROVIDER_FACTORY)
Source: P06_PROVIDER_FACTORY extract, admission Af3c179f81dac. SAVED_TEXT_CATALOG only; no game files, no runtime, no scripts.
Attribution: PARENT_DIRECT (parent on nask-glm/glm-5-3-default).

## Verdict

STRONG POSITIVE CANDIDATE (first genuine object-pointer provider field writer found): at 0085CD06-0085CD17, ESI=[ESP+0x34]; ECX=[ESI+0x28]; EDX=[ECX] (vtable); EAX=[EDX+0x18] (slot +0x18); PUSH EBX; CALL EAX with ECX=[ESI+0x28] as receiver; TEST EAX,EAX; MOV [ESI+0x2C],EAX. The stored value is the return product of a virtual factory call on the object at [ESI+0x28]. Later in the same body [ESI+0x2C] is null-checked and used as receiver with vtable slots +0x4C and +0x50 (0085CD27..0085CD45). Join ESI==R: NOT established (binding of [ESP+0x34] at function entry unknown; function starts before 0085C780).

## Claims
See CLAIMS.json (strict JSON, separated statuses).
