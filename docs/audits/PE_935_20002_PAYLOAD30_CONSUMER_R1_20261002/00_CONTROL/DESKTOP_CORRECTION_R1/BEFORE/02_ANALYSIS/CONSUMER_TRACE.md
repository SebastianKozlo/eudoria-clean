# CONSUMER_TRACE — PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002

STATIC_ONLY. The complete answer to the primary question, with the evidence chain.

## PRIMARY QUESTION
"What does the PCG 9.3.5 client do with the value located at payload+0x30 of a concrete record in 20002.vfs?"

## ANSWER (mechanism, instruction-verified)

For record 0 of 20002.vfs (ANCHOR_PRIMARY; and identically for all 1,366 records —
the tag shape is uniform across the whole file, machine-verified):

1. The client opens `Data\Parameters\20002.vfs` **because class 20002 is registered as
   ArkParameterArmor** (RTTI `ArkObjectClassImpl<class_ArkParameterArmor,20002>`): the
   class object builds its data-file name as itoa(20002) + ".vfs" and stores the open
   ArkVFS02 reader on itself (classObj+0x84) via FUN_0070c680 -> FUN_00972df0.
2. Records are loaded on demand by record id: FUN_0070e100 -> FUN_0070de10 ->
   FUN_0070dcf0 -> FUN_00971ad0 (seek to frame_pos+0x10, ReadFile 56 bytes = the
   payload; the per-record CRC comparison is SKIPPED because every crc field in this
   file is 0 — byte-fact, gate instruction pinned).
3. The payload is parsed by the GENERIC class-property TLV parser FUN_00726900:
   flags u16 (0x80), count u16 (6), then six {u16 tag, typed value} entries against the
   class's 18-entry descriptor schema (tags 0x00..0x11; byte-pinned registration).
4. The entry with **tag 0x11** is the LAST of the six; its value starts at
   **payload+0x30** (cursor offset 0x30 at that iteration — machine-verified for
   1366/1366 records).
5. The client reads that value with a native 4-byte little-endian load
   (`MOV EAX, dword [EAX+EDX*1]` @ VA 0x00412553 in FUN_00412540, the type-1 scalar
   reader) and stores it into the freshly created **ArkParameterArmor instance's
   value-array slot 21** (`MOV [EDX], EAX` @ 0x0041255A; slot address =
   instance->[+0x40] + (tag+4)*4 = value_array+0x54).
6. The instance (with the value in its tag-0x11 property slot) is registered in the
   class instance map (record-id -> instance). The property is then available to the
   client's generic property-read machinery (202 descriptor-lookup call sites; all
   captured in the bounded census; NO static immediate-tag-0x11 reader exists — reads
   are tag-variable-driven at runtime).

In one sentence: **the payload+0x30 value of a 20002.vfs record is the tag-0x11 (17th)
property value of an ArkParameterArmor (class 20002) parameter record; the client's
generic TLV property parser copies it — a plain 4-byte little-endian load, no
comparison, no arithmetic — into slot 21 of the corresponding ArkParameterArmor
instance's 22-slot value array, where it is exposed to the generic property machinery.**

## What the value is NOT shown to be (scope honesty)

- No evidence in this bounded run shows the value participating in any lookup,
  comparison, model/resource reference, coordinate, or placement mechanism AT THE
  TRACED INSTRUCTIONS: the traced operation is a pure copy into a property slot.
- No statically-coded reader with an immediate tag 0x11 was found in the 202-site
  census; which runtime code reads the slot (and what it does with it) remains open
  (bounded census documented in 02_ANALYSIS\DESTINATION_CONSUMER_CENSUS.json).
- Per the contract's §2 discipline, NO semantic label (id2/template/resource/model/
  NIF/object/instance/world-placement/network ID/foreign key/pointer/offset/coordinate/
  world-instance->model edge) is applied to the value: none was re-established from
  in-run evidence.

## Evidence chain (SOURCE -> INSTRUCTION -> DESTINATION -> CONSUMER)

| STEP | EVIDENCE |
|---|---|
| Physical bytes at payload+0x30 of record 0: `BB 2E 00 00` (11963) | 01_RAW\RECORD_FRAMING.jsonl row 0; 01_RAW\FIELD_BYTE_ANCHOR.json |
| Record framing + payload bounds (1366 records, exact-EOF walk, NC-FRAMING falsifiable) | 01_RAW\RECORD_FRAMING_SUMMARY.json; 03_SCRIPTS\s1_framing_census.py |
| Cross-implementation boundary agreement (executor vs prior tool) | 01_RAW\CROSSVALIDATION_vfs_common.json (1366/1366) |
| Routing: class 20002 = ArkParameterArmor; open itoa(20002)+".vfs"; reader at classObj+0x84 | 01_RAW\ROUTING_CENSUS_RAW.json; 01_RAW\CLIENT_READ_BYTES.json pins 0x73A441/0x70C3FC/0x70C40E/0x70C742/0x70C71E; 02_ANALYSIS\VFS_TO_PARSER_TRACE.md |
| Per-record seek+read (payload start, 56 bytes, CRC gate skipped) | pins 0x971B14/0x971B4A/0x971B4C |
| TLV parse loop + descriptor schema + destination computation | pins 0x7269E7/0x7269FC/0x726A03/0x726A08/0x726A0E/0x726A11/0x726A14/0x726A1B/0x70C1D3/0x70C1D6/0x761717/0x76171C/0x76171E/0x761722/0x70CBF6 |
| THE READ (payload+0x30) + THE STORE (slot 21) | pins 0x412553 (`8B 04 10`), 0x41255A (`89 02`) |
| Walk coverage: tag 0x11 value at +0x30 in 1366/1366 records; tail 0 in 1366/1366 | 01_RAW\TLV_WALK_CENSUS.json |
| Consumer census (write path unique; read side generic, 0 static imm-0x11 readers) | 01_RAW\GHIDRA_ROUTING\PASS15_GHIDRA_DUMP.json; 02_ANALYSIS\DESTINATION_CONSUMER_CENSUS.json |
