# AUTHORIZATION_RECORD — PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002

Provenance: transcribed by the pe-master-auditor formalizer session on 2026-10-02 from
the human authorization PE_935_20002_PAYLOAD30_CONSUMER_HUMAN_AUTH_R1_20261002 as relayed
verbatim by PE-MASTER direct dispatch. Enumerated lists below are verbatim (no paraphrase).
The human order is the authoritative original; this record is its in-package transcription.

Scope statement (from the authorization, as relayed): the authorization authorizes
exactly ONE bounded STATIC-ONLY reverse-engineering experiment as an explicit exception
to the placement-research block. It does NOT qualify PE-MASTER and does NOT change
Q1/Gate-B/M1.

## Core authorization fields (verbatim)

AUTHORIZATION_ID = PE_935_20002_PAYLOAD30_CONSUMER_HUMAN_AUTH_R1_20261002
RUN_ID = PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002
RUN_CLASS = BOUNDED_RE_EXCEPTION (human namespace); PE-MASTER RUN_CLASS declaration for audit depth: LOAD_BEARING
PRIMARY_TARGET = PCG_9_3_5 / Entropia Universe 9.3.5
CANONICAL_REPO = SebastianKozlo/eudoria-clean
AUTHORIZED_BASE_HEAD = 9203b6d1ad5025f4158d5165863594132aaac49f
PHYSICAL_CORPUS_ROOT = D:\Eudoria_Reconstruction\pcg_install
STATIC_ONLY = YES; RUNTIME_EXECUTION_AUTHORIZED = NO; HUMAN_AUTHORIZATION = YES

## PROHIBITED STARTING ASSUMPTIONS (authorization §2 — all 14 items, verbatim)

1. id2
2. template ID
3. resource ID
4. model ID
5. NIF ID
6. object ID
7. instance ID
8. world-placement ID
9. network ID
10. foreign key
11. pointer
12. offset
13. coordinate
14. world-instance -> model edge

Binding rule carried with the list: these semantic labels may NOT be applied to the
payload+0x30 value unless independently re-established from in-run evidence, with each
such promotion carrying its own byte-level proof.

## EPISTEMIC BASELINE (authorization §3, verbatim)

20002_VFS_PAYLOAD_PLUS_30_FINAL_SEMANTIC_ROLE = UNVERIFIED
WORLD_INSTANCE_TO_MODEL_LINK = NOT_DEMONSTRATED
PLACEMENT_SOURCE = NOT_RECOVERED

## GOVERNANCE UNCHANGED (authorization §4, verbatim)

Q1_ATTEMPT_4_RESULT = NOT_GRADED
PE_MASTER_STATUS = PROVISIONAL_UNTIL_QUALIFIED
PE_MASTER_QUALIFIED = NO
GATE_B_CANONICAL_AUTHORITY_STATUS = BLOCKED
M1_CLOSED = NO

## AUTHORIZED ACTIONS (authorization §5 — compact form of the MAY list)

MAY (all bounded, read-only/static, inside the authorized scope):
- Read and statically analyze the pinned physical Entropia.exe (D:\Eudoria_Reconstruction\pcg_install\Entropia.exe).
- Read and parse the pinned physical 20002.vfs (D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\20002.vfs).
- Bounded reads + identity metadata of other files under D:\Eudoria_Reconstruction\pcg_install\ (e.g. templates.vfs as prior-evidence context).
- Use prior audit packages as READ-ONLY prior-evidence reference (especially the JOIN R1 package docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928\).
- Run Ghidra headless (static) against the pinned EXE.
- Create and run bounded analysis/recomputation scripts inside OUTPUT_ROOT\03_SCRIPTS\ (executor) and OUTPUT_ROOT\04_QC\ (QC worker only).
- Produce local evidence artifacts inside OUTPUT_ROOT (the run package).
- Execute the ONE authorized science question (the static consumer trace of payload+0x30) per RUN_CONTRACT.md §1.

## MAY-NOT LIST (authorization §5 — all 16 items, verbatim)

1. launch the client
2. instrument the running client
3. perform runtime hooks or runtime mutations
4. run a second science question
5. expand into broad placement recovery
6. search all world-instance mechanisms as a new campaign
7. recover building locations generally
8. implement placement in renderer
9. modify original game payloads
10. start M2 or M3
11. close M1
12. qualify PE-MASTER
13. perform Gate-B re-attestation
14. start another Q1 attempt
15. commit
16. push

## Payload + follow-up constraints

"No proprietary original payload goes into Git."

This run is a ONE-RUN EXCEPTION (one bounded RE experiment under the human's direct
order; an explicit exception to the placement-research block).
AUTO_FOLLOWUP_RE = NO
NEXT_EXPERIMENT_AUTHORIZED = NO
INDEPENDENT_CHATGPT_DESKTOP_POST_AUDIT_REQUIRED = YES
