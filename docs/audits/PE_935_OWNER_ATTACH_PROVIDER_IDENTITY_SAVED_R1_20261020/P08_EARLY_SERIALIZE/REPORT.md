# P08_EARLY_SERIALIZE

RUN_ID: PE_935_OWNER_ATTACH_PROVIDER_IDENTITY_SAVED_R1_20261020 (package P08_EARLY_SERIALIZE)
Source: P08_EARLY_SERIALIZE extract, admission A59633431247e. SAVED_TEXT_CATALOG only; no game files, no runtime, no scripts.
Attribution: PARENT_DIRECT (parent on nask-glm/glm-5-3-default).

## Verdict

At 0085C796..0085C814 an EARLIER ESI binding (not [ESP+0x34]) has float fields +0x20/+0x24/+0x28/+0x2C written to the stream; at 0085C81E onward EBX floats [EBX], [EBX+4] etc. are written. The [ESP+0x34]-ESI of the provider store is a RE-binding (MOV ESI,[ESP+0x34] at 0085CA3F/0085CD06); the earlier ESI is a different object. Function entry still before 0085C780. The join edge remains open.

## Claims
See CLAIMS.json (strict JSON, separated statuses).
