# P05_TRANSFORMWRITE

RUN_ID: PE_935_OWNER_ATTACH_PROVIDER_IDENTITY_SAVED_R1_20261020 (package P05_TRANSFORMWRITE)
Source: P05_TRANSFORMWRITE extract, admission A2aba7bef7da0. SAVED_TEXT_CATALOG only; no game files, no runtime, no scripts.
Attribution: PARENT_DIRECT (parent on nask-glm/glm-5-3-default).

## Verdict

The window is the tail of a function writing a full 13-dword transform at [EAX..EAX+0x30]: 9 dwords copied via REP MOVSD (ECX=9) from a local built by CALL 0096CF80, three floats from locals ([EAX+0x24],[EAX+0x28],[EAX+0x2C]), and FLD1 stored at [EAX+0x30]. EAX=[ESP+0xAC] (caller-frame slot). The store+2C here is a FLOAT slot of a 13-dword transform layout, not a provider pointer; EAX==R not established (R stores its transform at R+0x30 per frozen priors).

## Claims
See CLAIMS.json (strict JSON, separated statuses).
