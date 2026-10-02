# REPORT — PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002

RUN_ID = PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002
BASE_HEAD = 9203b6d1ad5025f4158d5165863594132aaac49f
STATIC_ONLY = YES
RUNTIME_EXECUTION_PERFORMED = NO
EXE_IDENTITY_MATCH = YES (D:\Eudoria_Reconstruction\pcg_install\Entropia.exe; 8,015,872 B; SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31; FileVersion 9.3.5.6746)
VFS_IDENTITY_MATCH = YES (D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\20002.vfs; 174,864 B; SHA256 C3899C3E88D72CE12CEF9B8A4F5E73B26632BB1A3207C950FF2BC40FD9C94AC4)
SOURCE_SHA256 = EXE E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31; VFS C3899C3E88D72CE12CEF9B8A4F5E73B26632BB1A3207C950FF2BC40FD9C94AC4; both re-measured at execution start (00_CONTROL\PREFLIGHT.md)

## The anchored record (ANCHOR_PRIMARY = record 0; ANCHOR_ZERO in secondary keys; per FORMALIZER_NOTES FN-2)

RECORD_ORDINAL_OR_PHYSICAL_ID = 0 (zero-indexed record 0; header id 0x05B80001)
RECORD_FRAME_START = 16 (0x10)
RECORD_PAYLOAD_START = 32 (0x20)
RECORD_PAYLOAD_LENGTH = 56 (0x38)
FIELD_FILE_OFFSET = 80 (0x50) = RECORD_PAYLOAD_START + 0x30
PAYLOAD_PLUS_30_RAW_BYTES = BB 2E 00 00
PAYLOAD_PLUS_30_DECODED_VALUE = 11963 (4-byte little-endian; width/endianness now RAW_MEASUREMENT from the pinned client read instruction — V2-009 upgrade from the S1 HYPOTHESIS_DERIVED label)
ANCHOR_ZERO_* (secondary, clearly labeled): ANCHOR_ZERO_RECORD_ORDINAL = 1014 (lowest-ordinal zero-valued record; 1015 is the only other); ANCHOR_ZERO_FRAME_START = 129808; ANCHOR_ZERO_PAYLOAD_START = 129824; ANCHOR_ZERO_PAYLOAD_LENGTH = 56; ANCHOR_ZERO_FIELD_FILE_OFFSET = 129872 (0x1FBB0); ANCHOR_ZERO_RAW_BYTES = 00 00 00 00; ANCHOR_ZERO_DECODED_VALUE = 0.

## Routing and client read

20002_VFS_TO_PARSER_ROUTING = CONFIRMED
(byte-pinned chain: class-ID 20002 imm @0x73A441 -> ArkObjectClassImpl<class_ArkParameterArmor,20002> ctor + vtable 0xA86FE0 @0x73A46B -> registry case 0x4E22 returns DAT_00ba5da8 @0x73C8C1 -> FUN_0070c680 builds itoa(classObj->[+8]=20002)+".vfs" (@0x70C3FC, ".vfs" @0xA86820) -> FUN_00972df0 open @0x70C742 -> ArkVFS02 reader stored at classObj+0x84 @0x70C71E -> per-record FUN_00971ad0 (seek @0x971B14; ReadFile; CRC gate skipped because all crc fields are 0 @0x971B4A/0x971B4C) -> FUN_0070dcf0 (advance 8) -> FUN_0070dc20 -> FUN_00726900 generic TLV property parser. Evidence: 01_RAW\CLIENT_READ_BYTES.json 45/45 pins OK; 02_ANALYSIS\VFS_TO_PARSER_TRACE.md. The §B lead's FUN_00959090 family was verified to belong to EnvironmentZones.vfs instead — recorded as a lead correction, not a client-read claim.)

CLIENT_READ_IDENTIFIED = YES
READ_FUNCTION = FUN_00412540 (the type-1 scalar value reader; reached via FUN_00726900 -> FUN_0075f660 @0x726A1B -> FUN_004129c0 @0x4129DF)
READ_INSTRUCTION_VA = 0x00412553
READ_INSTRUCTION_RVA = 0x00012553
READ_INSTRUCTION_FILE_OFFSET = 0x00125553
READ_INSTRUCTION_BYTES = 8B 04 10 (MOV EAX, dword ptr [EAX + EDX*1] — native x86 32-bit little-endian load from cursor.base + cursor.offset; at the tag-0x11 iteration cursor.offset = 0x30 over the record payload buffer)

## Destination

DEST_FIELD_IDENTIFIED = YES
DEST_STRUCTURE = the ArkParameterArmor instance's value array (22 u32 slots; heap array, pointer at instance+0x40; allocated by FUN_0070d990 as descriptor_count(18)+4 slots; instance = 0x58 bytes constructed via the class factory FUN_0073a490 -> FUN_00761540 with ArkParameterArmor::vftable 0xA878BC @0x761556)
DEST_FIELD_OFFSET = slot 21 (value_array + 0x54); slot index = tag + 4 (0x11 + 4 = 0x15; formula pinned @0x70CBF6 ADD ECX,4); STORE_INSTRUCTION_VA = 0x0041255A; STORE_INSTRUCTION_BYTES = 89 02 (MOV dword ptr [EDX], EAX)

## Downstream consumer

DOWNSTREAM_CONSUMER_IDENTIFIED = NO (no specific consumer of the tag-0x11 slot was identified; the read side is runtime-tag-driven generic property machinery)
OBSERVED_OPERATION = pure copy (opaque propagation): 4-byte LE load from the record payload at +0x30, stored into the instance's tag-0x11 property slot; no comparison, arithmetic, branch, or lookup at any traced instruction; the instance is registered in the class instance map keyed by record id (not by this value)

## Census (§10)

STATIC_READ_SEARCH_SCOPE = all 202 direct callers of the descriptor lookup FUN_0070c180 (the generic property machinery: getters/setters/serializers), captured with 0x20 bytes of instruction context each (01_RAW\GHIDRA_ROUTING\PASS15_GHIDRA_DUMP.json); plus the getter family (FUN_00726450/90/26510/26d10/26c00/26d70/27480/275a0/27e90/27f10) and the serialization writer family (FUN_00726560/FUN_00727110)
STATIC_WRITE_SEARCH_SCOPE = the value-read dispatch FUN_0075f660 and its callers (exactly 1: the TLV parse loop FUN_00726900 @0x726A1B), plus the store instructions of the typed readers (FUN_00412540 et al.)
STATIC_WRITE_SITES_FOUND = 1 (the store @0x0041255A — the write path into the destination slot is unique: FUN_0075f660 has exactly one caller)
STATIC_READ_SITES_FOUND = 0 with a static immediate tag 0x11 (2 candidate hits examined and shown to be false positives: the parse loop's own tag register, and a state-variable byte in FUN_008ae600 whose actual lookup tag is 0x2 for class 24017)
UNRESOLVED_ALIASES = the heap value-array pointer (instance+0x40); the class instance map (classObj+0xC); the runtime-initialized class-object singleton DAT_00ba5da8
UNRESOLVED_INDIRECT_CALLS = the instance vtable 0xA878BC methods (incl. the mode-1 nested reader — never exercised: tail u32 == 0 in 1366/1366 records); the classObj+0x80 trait-object virtuals (finalize +0x24 / rollback +0x28); the FUN_00977a50 descriptor-factory object; all runtime-tag-driven getter invocations across the 202-site machinery
UNINSPECTED_PATHS = full downstream data-flow of each of the 202 getter sites (bounded census only); gameplay armor-behavior code; network/save serialization consumers (FUN_00727110 iterates a runtime tag vector); the other 17 descriptor slots of the schema
Exhaustiveness wording (V2-012): ONLY_DIRECT_WRITER_FOUND (write side, evidenced); read-side census BOUNDED (202/202 sites captured; no static tag-0x11 reader); GLOBAL read-side exhaustiveness UNVERIFIED (tag arguments are runtime variables; indirect dispatch paths uninspected)

## Statuses

FIELD_IDENTITY_STATUS = CONFIRMED (structural identity, byte-proven: the value is the tag-0x11 TLV entry's 4-byte scalar value — the 17th descriptor of the ArkParameterArmor/class-20002 property schema — present as the last of six entries in 1366/1366 records at payload+0x30)
FINAL_SEMANTIC_ROLE = bounded wording: "a per-record 4-byte scalar property value (TLV tag 0x11) of the ArkParameterArmor / class-20002 parameter records, copied by the client into the corresponding instance's property slot 21 and exposed to the generic property machinery; its gameplay meaning and its runtime consumers were NOT established in this bounded run"
FINAL_SEMANTIC_STATUS = UNVERIFIED
WORLD_INSTANCE_TO_MODEL_EDGE = NOT_TESTED (no world-instance->model edge was claimed, tested, or demonstrated; the traced operation is a copy into a property slot)
PLACEMENT_XYZ_RECOVERED = NO

## Controls

NEGATIVE_CONTROL_STATUS = PASS (NC-FRAMING: 4/4 mandatory corruption classes detected, +1 documented non-discriminating variant; NC-ANCHOR-ADJ: feasible part AND instruction-level part executed — the +0x2C window is consumed by different instructions into different slots (20/tag-register vs 21); NC-RECORD: all 1366 records including ANCHOR_ZERO share the identical parser path; NC-VALUE: NOT_APPLICABLE_NO_LOOKUP_COMPARISON_CLAIMED — the traced mechanism contains no lookup or comparison of the value, documented per §13's do-not-invent rule; full detail in 02_ANALYSIS\NEGATIVE_CONTROLS.md)

## Governance

INDEPENDENT_QC = PASS_WITH_FINDINGS (QC round 1: 0xP0, 0xP1, 2xP2, 5xP3 — full report 04_QC\QC_REPORT.md; the P2-1 + P3-1..P3-4 corrections applied in AMEND-R1, the P2-2 incident verified repaired, P3-5 documented-not-fixed — see 06_REPORT\AMEND_LOG_R1.md; targeted QC round 2 verification: 04_QC\QC_R2_TARGETED_REPORT.md)
Q1_STATUS_CHANGED = NO
PE_MASTER_QUALIFICATION_CHANGED = NO
GATE_B_CHANGED = NO
M1_CHANGED = NO
M2_CHANGED = NO
M3_CHANGED = NO
COMMIT = NO
PUSH = NO

RUN_STATUS = CONSUMER_REACHED_ROLE_STRONGLY_SUPPORTED
(the consumer — the destination field: the ArkParameterArmor instance's tag-0x11 property slot — was reached with a byte-pinned end-to-end chain: routing CONFIRMED, client read CONFIRMED, store CONFIRMED, mechanism role strongly supported by RTTI + schema + parse evidence; the gameplay semantic role remains UNVERIFIED per the separate FINAL_SEMANTIC_ROLE axis; the three axes are reported separately per §12)

## Summary of the trace (one paragraph)

The value at payload+0x30 of a 20002.vfs record is the tag-0x11 (17th) property value of the record's TLV property block: every record carries six entries (tags 1, 0xC, 0xD, 0xE, 0x10, 0x11) under flags 0x80 and count 6, and the tag-0x11 value sits at payload+0x30 in 1366/1366 records. Class 20002 is the ArkParameterArmor parameter class (RTTI-confirmed); its class object opens its own data file as itoa(20002)+".vfs" and loads records on demand into ArkParameterArmor instances (0x58 bytes, 22-slot value arrays). The generic property parser reads the +0x30 field with a native 4-byte little-endian load (VA 0x00412553) and stores it — a pure copy, no comparison or lookup — into the instance's value-array slot 21 (VA 0x0041255A), from which the generic property machinery can read it by tag at runtime (no statically-coded tag-0x11 reader exists in the 202-site census). What the property means in gameplay and which code reads it at runtime remains open (bounded census documented); no world/model/placement semantics are claimed.

## Package

Evidence index: 06_REPORT\EVIDENCE_INDEX.md. Manifest: 06_REPORT\MANIFEST_SHA256.csv (executor outputs; known-stale until the final regeneration after QC + PE-MASTER verdict; manifest self-exclusion per the L12 precedent: a manifest cannot contain its own hash).
HARD_STOP = YES (per contract §19; no automatic continuation).
