# PREFLIGHT OPERATIONAL REPORT - ROOT COLLISION (no overwrite)

RUN_ID_NEW = PE_935_PAIR_REDUCER_CONSUMER_SAVED_R2_20261019
COLLIDING_ROOT = D:\Eudoria_Reconstruction\99_Audits\PE_935_PAIR_REDUCER_CONSUMER_SAVED_R1_20261019
AUTHORING_ROOT = D:\Eudoria_Reconstruction\99_Audits\PE_935_PAIR_REDUCER_CONSUMER_AUTHORING_R1_20261019
CONTRACT_SHA256_VERIFIED = 7494B7146106255B4C710EE0EBF1A87EAECC2C201ADA5A3739521AC86A9FCDA0
GUARD_CHECK = PASS (authoring bijection 21 rows / 22 physical files, manifest self-excluded; external_files=1433)

## Collision facts

guard start --root <SAVED_R1> returned OUTPUT_ROOT_EXISTS. Physical inspection shows an
interrupted prior attempt of the SAME mission, created shortly before this session:
- CONTROL\EVENTS\000001_START.json (START, limits 32/6000/200/32/1500)
- CONTROL\EVENTS\000002_ADMIT.json (P01 adapter, admission A53e359b7f357, selected_lines_sha256 CC491E...)
- CORRECTIONS_APPLIED.json, CORRECTED_CHECKPOINT.json
- P01_EXTRACT (6 listing files), P01_CONTRACT.json
- NO worker science package (no RUN_STARTED, no REPORT/CLAIMS), NO STOP event, NO manifest/seal.

Disposition per CONTRACT.md section 2 (collision clause): the colliding root is left
untouched and unsealed (orphaned interrupted attempt, preserved as-is for provenance);
this run continues under the new consistent binding ..._SAVED_R2_20261019 with fresh
guard START (event 000001, sha 50C440D26C1F1965BDA568F01085EC98D098A4A7B37969EEBD0A970486B23C53).
No file of R1 was modified, re-written, sealed or extended by this session.

## Assimilated postaudit corrections (consumed before new science)

Source: PE_935_MODEL_PAIR_TRANSPORT_DEEP_POSTAUDIT_R1_20261019 (REPORT.md fully read,
CLAIM_DISPOSITION.csv 14 rows fully read, STACK_REDERIVATION.json fully read).
Frozen runs and canon untouched; corrections recorded as closed audit lemmas of stated scope:
1. One shared container C=B+1Ch in 006C4060 (three LEA expressions all equal B+1C).
2. In 006C36B0 ESI is arg4=M32[S+10h]; literal sink 0x00BA45E8 is the fourth argument.
3. Only the LOW BYTE of the sixth context DWORD is established as 1; upper 24 bits unknown.
4. Exact pointer-holder callsite 006C36E1: arg3 = S+10h points to the slot CONTAINING the
   current pair pointer (stored EDI @006C36DD); not the pair pointer itself.
5. Opaque effects of 006C29D0 and other callees are NOT rejected (H1/H2 not disjoint);
   axes LOCAL_MECHANISM / DATA_DOMAIN / OPAQUE_EFFECTS / WORLD_INSTANCE_RELATION kept separate.
6. Literal field 0x00823C10 does not by itself prove it is called; no call assumption before body proof.
7. Prior-run accounting: 13 events (START1+ADMIT10+DENY1+STOP1), correct no-refund charge
   22/24 bodies, 23/24 candidates; P08 local admission breach not legalized by global limit.
8. MEMBER_VIEW 0040B070 remains conditional on same-build provenance.

New science corpus: SAVED_TEXT_CATALOG.json of the current authoring ONLY.
No original EXE/runtime/payload operations; no Ghidra/new export; no model/config changes.
