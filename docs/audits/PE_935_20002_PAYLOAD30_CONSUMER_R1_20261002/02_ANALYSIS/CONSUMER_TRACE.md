# CONSUMER_TRACE — PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002

STATIC_ONLY. The complete answer to the primary question, with the evidence chain.
Correction state: DESKTOP_CORRECTION_R1 — the value-read chain below uses the
SELECTED reader (the virtual branch -> FUN_009777F0) proven in
01_RAW\DESKTOP_CORRECTION_R1\BRANCH_SELECTION_TRACE.json; the pre-correction text
attributing the read to the fallback reader FUN_00412540 is superseded (recorded in
06_REPORT\AMEND_LOG_DESKTOP_CORRECTION_R1.md; BEFORE copy preserved in
00_CONTROL\DESKTOP_CORRECTION_R1\BEFORE\02_ANALYSIS\CONSUMER_TRACE.md).

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
   FUN_0070dcf0 -> FUN_00971ad0 (seek to frame_pos+0x10, read 56 bytes = the payload
   into a cursor; the per-record CRC comparison is SKIPPED because every crc field in
   this file is 0 — byte-fact, gate instruction pinned).
3. The payload is parsed by the GENERIC class-property TLV parser FUN_00726900:
   flags u16 (0x80), count u16 (6), then six {u16 tag, typed value} entries against the
   class's 18-entry descriptor schema (tags 0x00..0x11; byte-pinned registration).
4. The entry with **tag 0x11 (tag ID 17)** is the LAST of the six; its value starts at
   **payload+0x30** (cursor offset 0x30 at that iteration — machine-verified for
   1366/1366 records; cursor provenance re-derived for the selected reader in
   01_RAW\DESKTOP_CORRECTION_R1\CURSOR_PROOF_CORRECTION_R1.json).
5. The client dispatches the value read through FUN_0075f660, which **tests
   [descriptor+0] first**: for tag ID 17 the descriptor's +0 field holds the
   **ArkRTTraitsInt** reader object (a static .data singleton 0x00BA937C returned by
   the descriptor factory FUN_00977a50 — never NULL), so the **VIRTUAL BRANCH is
   SELECTED**: the call goes through the object's vtable slot +0x14 (the dword
   0x009777F0 read from the pinned .rdata at 0x00A9C684) to the **selected type-1
   reader FUN_009777F0**, which reads the value with a native 4-byte little-endian
   load (`MOV EAX, dword [EDX+EAX*1]` @ VA 0x00977807, bytes 8B 04 10) and stores it
   into the freshly created **ArkParameterArmor instance's value-array slot 21**
   (`MOV [EDX], EAX` @ 0x00977810, bytes 89 02; slot address =
   instance->[+0x40] + (tag+4)*4 = value_array+0x54), then advances the cursor by 4.
   (The old attribution of this read to the fallback reader FUN_00412540 is superseded:
   that path requires descriptor+0 == NULL, which is not the tag-ID-17 state — see
   01_RAW\DESKTOP_CORRECTION_R1\FALLBACK_PATH_RECORD.json.)
6. The instance (with the value in its tag-0x11 property slot) is registered in the
   class instance map (record-id -> instance). The property is then available to the
   client's generic property-read machinery (202 descriptor-lookup call sites; all
   captured in the bounded census; NO static immediate-tag-0x11 reader was identified
   within the censused machinery — reads are tag-variable-driven at runtime).

In one sentence: **the payload+0x30 value of a 20002.vfs record is the tag-0x11 (tag
ID 17) property value of an ArkParameterArmor (class 20002) parameter record; the
client's generic TLV property parser dispatches it through the proven virtual branch
to the ArkRTTraitsInt type-1 reader, which copies it — a plain 4-byte little-endian
load, no comparison, no arithmetic — into slot 21 of the corresponding
ArkParameterArmor instance's 22-slot value array, where it is exposed to the generic
property machinery.**

## What the value is NOT shown to be (scope honesty)

- No evidence in this bounded run shows the value participating in any lookup,
  comparison, model/resource reference, coordinate, or placement mechanism AT THE
  TRACED INSTRUCTIONS: the traced operation is a pure copy into a property slot.
- No statically-coded reader with an immediate tag 0x11 was found in the 202-site
  census; which runtime code reads the slot (and what it does with it) remains open.
  Within the inspected 202 direct descriptor-lookup sites and the documented limited
  context window, no tag-ID-17 downstream reader was identified. Full downstream
  static data-flow, aliases, indirect calls and global writer/read completeness
  remain UNVERIFIED. Further static resolvability is NOT_ESTABLISHED.
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
| BRANCH SELECTION (registration -> factory -> descriptor+0 -> TEST/JZ -> virtual slot -> selected reader; RTTI ArkRTTraitsInt) | 01_RAW\DESKTOP_CORRECTION_R1\BRANCH_SELECTION_TRACE.json (96/96 pins; slot dword @0xA9C684 = 0x009777F0) |
| THE SELECTED READ (payload+0x30) + THE SELECTED STORE (slot 21) | pins 0x977807 (`8B 04 10`), 0x977810 (`89 02`); 01_RAW\DESKTOP_CORRECTION_R1\DESTINATION_PROOF_CORRECTION_R1.json (23/23) |
| THE FALLBACK READ/STORE (non-selected; descriptor+0==NULL required) | 01_RAW\DESKTOP_CORRECTION_R1\FALLBACK_PATH_RECORD.json (25/25; read @0x00412553 / FO 0x12553; store @0x0041255A / FO 0x1255A) |
| Cursor provenance for the selected reader (record 0 + record 1014 + 1366 census; error paths distinguished) | 01_RAW\DESKTOP_CORRECTION_R1\CURSOR_PROOF_CORRECTION_R1.json |
| Walk coverage: tag 0x11 value at +0x30 in 1366/1366 records; tail 0 in 1366/1366 | 01_RAW\TLV_WALK_CENSUS.json (+ the correction re-derivation) |
| Consumer census (write path unique within the censused machinery; read side generic, 0 static imm-0x11 readers in the census) | 01_RAW\GHIDRA_ROUTING\PASS15_GHIDRA_DUMP.json; 02_ANALYSIS\DESTINATION_CONSUMER_CENSUS.json |
