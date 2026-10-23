# POSTAUDIT_NOTICE_R1 — additive HDA notice (created 2026-10-23 by run PE_935_MESSAGE_TRANSFORM_INSTANCE_BINDING_DEFAULT_TASK_OPENCODE_SAVED_R1_20261022)

This notice is ADDED to this package's directory. Nothing in the original package is modified, retracted or resealed by this file; the local seal (49 manifest rows + manifest, PASS) remains untouched.

Standing corrections that apply when reading this package (from PE_935_INSTANCE_KEY_STREAM_RESOURCE_JOIN_HIGH_TASK_DEEP_POSTAUDIT_R1_20261022 and the subsequent DEFAULT-task run of 2026-10-22):

1. The headline claim getter(0x70) -> value A -> scene is REJECTED_AS_STATED: K_in (result of FUN_007CE1E0 at the input of FUN_006C9700) and P_out (later content of the argument slot after FUN_006C9570) are DIFFERENT definitions; no bit-equality between them was ever proven.
2. The store of ctor_arg2 to [wrapper+4] with conditional retain is real but was already established byte-level on 2026-10-08 (PLUS4_PROVENANCE); it is not a new discovery of this campaign.
3. RAW artifact JOBS/B7_KEY_CONSUMER/RAW/B7_RAW_H5_ROWS_0048e740_0048e800.txt row 4230 (VA 0048E7FE) is a mis-transcription (PUSH ECX recorded; source contains SUB ESP,0x30). That RAW is quarantined as non-canonical; the getter 0048E740 itself is not affected. The 2026-10-22 run generated all excerpts deterministically from the pinned H5 with lineNo+VA+instruction parity and did not reuse this file.
4. Task accounting for this campaign: 12 attempts = 7 stop + 5 length; the four MASTER-derived *_RESULT_RECOVERED documents are master-attributed analysis, not delivered worker verdicts; QCA did not deliver a final QC covering the key hop.
5. PRESERVATION_BY_THIS_HELPER and T_EQUALS_FIRST_INITIAL_P remain NOT_ESTABLISHED; alias/opaque-call countermodels from the 2026-10-16 postaudits remain in force.
6. Additive new knowledge (does not retract anything above): the 2026-10-22 run closed the subtype2 message-update chain structurally: K_query -> instance resolution (*out_slot := FUN_008544D0(FUN_004154F0(K_query)) in FUN_0085B840) -> consumer FUN_00527AB0(this=resolved instance, record as stack argument) -> 52B provider copy to [[this+0xc]+0x30] -> record field application via FUN_00861150 into the [this+0x10] object (12 direct stores incl. 4 bit-unpacked booleans). Field SEMANTICS (position/rotation/etc.) remain NOT established. See the new run package: docs/audits/PE_935_MESSAGE_TRANSFORM_INSTANCE_BINDING_DEFAULT_TASK_OPENCODE_SAVED_R1_20261022/.

WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CANONICAL_GATE_EFFECT=NONE.
