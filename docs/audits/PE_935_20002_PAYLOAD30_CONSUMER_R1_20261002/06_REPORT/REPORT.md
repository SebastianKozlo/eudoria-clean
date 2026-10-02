# REPORT — PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002

RUN_ID = PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002
BASE_HEAD = 9203b6d1ad5025f4158d5165863594132aaac49f
STATIC_ONLY = YES
RUNTIME_EXECUTION_PERFORMED = NO
EXE_IDENTITY_MATCH = YES (D:\Eudoria_Reconstruction\pcg_install\Entropia.exe; 8,015,872 B; SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31; FileVersion 9.3.5.6746)
VFS_IDENTITY_MATCH = YES (D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\20002.vfs; 174,864 B; SHA256 C3899C3E88D72CE12CEF9B8A4F5E73B26632BB1A3207C950FF2BC40FD9C94AC4)
SOURCE_SHA256 = EXE E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31; VFS C3899C3E88D72CE12CEF9B8A4F5E73B26632BB1A3207C950FF2BC40FD9C94AC4; both re-measured at execution start (00_CONTROL\PREFLIGHT.md) and re-verified at the DESKTOP_CORRECTION_R1 preflight (01_RAW\DESKTOP_CORRECTION_R1\PREFLIGHT_RERUN.json)

> **CORRECTION STATE: DESKTOP_CORRECTION_R1 (amended state).** This REPORT was amended
> by the focused correction run PE_935_20002_PAYLOAD30_DESKTOP_CORRECTION_R1_20261002
> (human decision PE_935_20002_PAYLOAD30_DESKTOP_CORRECTION_AUTH_R1_20261002, after the
> independent ChatGPT Desktop post-audit verdict REQUIRE_CORRECTIONS). The amendment
> corrects the SELECTED-READER branch of the client-read chain (the value read for tag
> ID 17 flows through the proven VIRTUAL branch to FUN_009777F0, not the fallback
> FUN_00412540) and the statuses derived from it. Full correction record incl. the
> BEFORE/AFTER artifact list and the contradiction census:
> 06_REPORT\AMEND_LOG_DESKTOP_CORRECTION_R1.md. BEFORE copies of every changed file:
> 00_CONTROL\DESKTOP_CORRECTION_R1\BEFORE\. Historical evidence (01_RAW\CLIENT_READ_BYTES.json,
> QC rounds 1/2, the historical JOIN R1 package) is byte-unchanged.

## The anchored record (ANCHOR_PRIMARY = record 0; ANCHOR_ZERO in secondary keys; per FORMALIZER_NOTES FN-2)

RECORD_ORDINAL_OR_PHYSICAL_ID = 0 (zero-indexed record 0; header id 0x05B80001)
RECORD_FRAME_START = 16 (0x10)
RECORD_PAYLOAD_START = 32 (0x20)
RECORD_PAYLOAD_LENGTH = 56 (0x38)
FIELD_FILE_OFFSET = 80 (0x50) = RECORD_PAYLOAD_START + 0x30
PAYLOAD_PLUS_30_RAW_BYTES = BB 2E 00 00
PAYLOAD_PLUS_30_DECODED_VALUE = 11963 (4-byte little-endian; width/endianness RAW_MEASUREMENT from the pinned SELECTED client read instruction — V2-009 upgrade from the S1 HYPOTHESIS_DERIVED label)
ANCHOR_ZERO_* (secondary, clearly labeled): ANCHOR_ZERO_RECORD_ORDINAL = 1014 (lowest-ordinal zero-valued record; 1015 is the only other); ANCHOR_ZERO_FRAME_START = 129808; ANCHOR_ZERO_PAYLOAD_START = 129824; ANCHOR_ZERO_PAYLOAD_LENGTH = 56; ANCHOR_ZERO_FIELD_FILE_OFFSET = 129872 (0x1FBB0); ANCHOR_ZERO_RAW_BYTES = 00 00 00 00; ANCHOR_ZERO_DECODED_VALUE = 0. (Re-derived for the SELECTED reader in 01_RAW\DESKTOP_CORRECTION_R1\CURSOR_PROOF_CORRECTION_R1.json: zero-valued records exactly [1014, 1015].)

## Routing and client read

20002_VFS_TO_PARSER_ROUTING = CONFIRMED
(byte-pinned chain: class-ID 20002 imm @0x73A441 -> ArkObjectClassImpl<class_ArkParameterArmor,20002> ctor + vtable 0xA86FE0 @0x73A46B -> registry case 0x4E22 returns DAT_00ba5da8 @0x73C8C1 -> FUN_0070c680 builds itoa(classObj->[+8]=20002)+".vfs" (@0x70C3FC, ".vfs" @0xA86820) -> FUN_00972df0 open @0x70C742 -> ArkVFS02 reader stored at classObj+0x84 @0x70C71E -> per-record FUN_00971ad0 (seek @0x971B14; ReadFile; CRC gate skipped because all crc fields are 0 @0x971B4A/0x971B4C) -> FUN_0070dcf0 (advance 8 @0x70DDA8) -> FUN_0070dc20 -> FUN_00726900 generic TLV property parser. Evidence: 01_RAW\CLIENT_READ_BYTES.json 45/45 pins OK (byte-correct; its reader-role fields describe the fallback-path evidence — see the correction); 02_ANALYSIS\VFS_TO_PARSER_TRACE.md. The §B lead's FUN_00959090 family was verified to belong to EnvironmentZones.vfs instead — recorded as a lead correction, not a client-read claim.)

CLIENT_READ_IDENTIFIED = YES
READ_FUNCTION = FUN_009777F0 (the SELECTED type-1 scalar value reader — the ArkRTTraitsInt virtual at [reader-object.vtable+0x14]; reached via FUN_00726900 -> FUN_0075f660 @0x726A1B -> the VIRTUAL branch, selected because [descriptor+0] != NULL for tag ID 17; the full branch-selection proof incl. the registration site, the factory FUN_00977a50 (returns the static ArkRTTraitsInt object 0x00BA937C, never NULL), the descriptor-init dataflow and the RTTI walk: 01_RAW\DESKTOP_CORRECTION_R1\BRANCH_SELECTION_TRACE.json, 96/96 pins)
READ_INSTRUCTION_VA = 0x00977807
READ_INSTRUCTION_RVA = 0x00577807
READ_INSTRUCTION_FILE_OFFSET = 0x00577807
READ_INSTRUCTION_BYTES = 8B 04 10 (MOV EAX, dword ptr [EDX + EAX*1] — native x86 32-bit little-endian load from cursor.base + cursor.offset; at the tag-ID-17 iteration cursor.offset = 0x30 over the record payload — re-derived for record 0, record 1014 and 1366/1366 records in 01_RAW\DESKTOP_CORRECTION_R1\CURSOR_PROOF_CORRECTION_R1.json)

FALLBACK (non-selected; recorded as evidence, superseded as the §18 read chain): the
typed-reader path FUN_004129c0 -> FUN_00412540 with READ @ VA 0x00412553 (file offset
0x12553; bytes 8B 04 10) / STORE @ VA 0x0041255A (file offset 0x1255A; bytes 89 02) is
BYTE-CORRECT EVIDENCE OF A NON-SELECTED FALLBACK PATH: it is reachable only when
[descriptor+0] == NULL (the JZ @0x75F66E target), which is NOT the tag-ID-17 state.
Full record: 01_RAW\DESKTOP_CORRECTION_R1\FALLBACK_PATH_RECORD.json (25/25 pins). The
prior transcription "READ_INSTRUCTION_FILE_OFFSET = 0x00125553" was a digit-shift
error and is superseded (the correct fallback offset is 0x12553; the run's own pin
JSON always recorded it correctly).

## Destination

DEST_FIELD_IDENTIFIED = YES
DEST_STRUCTURE = the ArkParameterArmor instance's value array (22 u32 slots; heap array, pointer at instance+0x40; allocated by FUN_0070d990 as descriptor_count(18)+4 slots — the count+4 arithmetic and the instance+0x40 slot byte-pinned @0x70D9B8/0x70D9BB/0x70D9BF; instance = 0x58 bytes constructed via the class factory FUN_0073a490 -> FUN_00761540 with ArkParameterArmor::vftable 0xA878BC @0x761556)
DEST_FIELD_OFFSET = slot 21 (value_array + 0x54); slot index = tag + 4 (0x11 + 4 = 0x15; formula pinned @0x70CBF6 ADD ECX,4; loaded from descriptor+8 @0x726A0E; the LEA chain @0x726A11/0x726A14 byte-pinned)
STORE_INSTRUCTION_VA = 0x00977810
STORE_INSTRUCTION_BYTES = 89 02 (MOV dword ptr [EDX], EAX — the SELECTED reader's store into the destination slot; width 4; the dest argument chain: value_array=[instance+0x40] @0x726A11 -> LEA dest=value_array+field_index*4 @0x726A14 -> FUN_0075f660 arg2 -> the virtual branch passes it as the reader's arg2 @0x75F670/0x75F679 -> loaded by the reader @0x97780A; proof: 01_RAW\DESKTOP_CORRECTION_R1\DESTINATION_PROOF_CORRECTION_R1.json, 23/23 pins)

## Downstream consumer

DOWNSTREAM_CONSUMER_IDENTIFIED = NO (no specific consumer of the tag-0x11 slot was identified within the inspected machinery). Bounded wording: "Within the inspected 202 direct descriptor-lookup sites and the documented limited context window, no tag-ID-17 downstream reader was identified. Full downstream static data-flow, aliases, indirect calls and global writer/read completeness remain UNVERIFIED. Further static resolvability is NOT_ESTABLISHED."
OBSERVED_OPERATION = pure copy (opaque propagation): 4-byte LE load from the record payload at +0x30, stored into the instance's tag-0x11 property slot; no comparison, arithmetic, branch, or lookup at any traced instruction; the instance is registered in the class instance map keyed by record id (not by this value)

## Census (§10)

STATIC_READ_SEARCH_SCOPE = all 202 direct callers of the descriptor lookup FUN_0070c180 (the generic property machinery: getters/setters/serializers), captured with 0x20 bytes of instruction context each (01_RAW\GHIDRA_ROUTING\PASS15_GHIDRA_DUMP.json); plus the getter family (FUN_00726450/90/26510/26d10/26c00/26d70/27480/275a0/27e90/27f10) and the serialization writer family (FUN_00726560/FUN_00727110)
STATIC_WRITE_SEARCH_SCOPE = the value-read dispatch FUN_0075f660 and its callers (exactly 1: the TLV parse loop FUN_00726900 @0x726A1B), plus the store instructions of the value readers — for tags with a non-NULL descriptor+0 object (all tags present in 20002.vfs records) the store happens in the SELECTED per-type reader reached via [reader-object.vtable+0x14] (the type-1 store @0x00977810; the fallback typed readers FUN_00412540 et al. are the non-selected machinery, reachable only when descriptor+0 == NULL)
STATIC_WRITE_SITES_FOUND = 1 (the selected-reader store @0x00977810 — the write path into the destination slot within the censused machinery: FUN_0075f660 has exactly one caller; ONE_DIRECT_CALLER_FOUND within the censused machinery — NOT global proof that slot 21 has exactly one writer across the client; runtime-tag-driven SETTER writes via the 202-site property machinery are the write-side counterpart of the disclosed read-side limitation, W-1)
STATIC_READ_SITES_FOUND = 0 with a static immediate tag 0x11 (2 candidate hits examined and shown to be false positives: the parse loop's own tag register, and a state-variable byte in FUN_008ae600 whose actual lookup tag is 0x2 for class 24017)
UNRESOLVED_ALIASES = the heap value-array pointer (instance+0x40); the class instance map (classObj+0xC); the runtime-initialized class-object singleton DAT_00ba5da8
UNRESOLVED_INDIRECT_CALLS = the instance vtable 0xA878BC methods (incl. the mode-1 nested reader — never exercised: tail u32 == 0 in 1366/1366 records); the classObj+0x80 trait-object virtuals (finalize +0x24 / rollback +0x28); all runtime-tag-driven getter invocations across the 202-site machinery. (The FUN_00977a50 descriptor-factory object behavior was RESOLVED by DESKTOP_CORRECTION_R1: the factory returns the static ArkRTTraitsInt object 0x00BA937C — see 01_RAW\DESKTOP_CORRECTION_R1\BRANCH_SELECTION_TRACE.json.)
UNINSPECTED_PATHS = full downstream data-flow of each of the 202 getter sites (bounded census only); gameplay armor-behavior code; network/save serialization consumers (FUN_00727110 iterates a runtime tag vector); the other 17 descriptor slots of the schema
Exhaustiveness wording (V2-012, corrected): ONLY_DIRECT_WRITER_FOUND (write side, evidenced within the censused machinery); read-side census BOUNDED (202/202 sites captured; no static tag-0x11 reader identified within the census); GLOBAL read-side exhaustiveness UNVERIFIED (tag arguments are runtime variables; indirect dispatch paths uninspected)

## Statuses

FIELD_IDENTITY_STATUS = CONFIRMED (structural identity, byte-proven: the value is the tag-0x11 (tag ID 17) TLV entry's 4-byte scalar value of the ArkParameterArmor/class-20002 property schema — present as the last of six entries in 1366/1366 records at payload+0x30)
FINAL_SEMANTIC_ROLE = bounded wording: "a per-record 4-byte scalar property value (TLV tag 0x11, i.e. tag ID 17) of the ArkParameterArmor / class-20002 parameter records, copied by the client into the corresponding instance's property slot 21 and exposed to the generic property machinery; its gameplay meaning and its runtime consumers were NOT established in this bounded run"
FINAL_SEMANTIC_STATUS = UNVERIFIED
WORLD_INSTANCE_TO_MODEL_EDGE = NOT_TESTED (no world-instance->model edge was claimed, tested, or demonstrated; the traced operation is a copy into a property slot)
PLACEMENT_XYZ_RECOVERED = NO

## Controls

NEGATIVE_CONTROL_STATUS = PASS (NC-FRAMING: 4/4 mandatory corruption classes detected, +1 documented non-discriminating variant; NC-ANCHOR-ADJ: feasible part AND instruction-level part executed with the SELECTED reader's instructions after the DESKTOP_CORRECTION_R1 correction — the +0x2C window is consumed by different instructions into different slots (20/tag-register vs 21); NC-RECORD: all 1366 records including ANCHOR_ZERO share the identical parser path (the selected-reader walk re-derived for record 0 and record 1014); NC-VALUE: NOT_APPLICABLE_NO_LOOKUP_COMPARISON_CLAIMED — the traced mechanism contains no lookup or comparison of the value, documented per §13's do-not-invent rule; full detail in 02_ANALYSIS\NEGATIVE_CONTROLS.md)

## Governance

INDEPENDENT_QC = QC rounds 1/2 (historical; PASS_WITH_FINDINGS for the run as delivered; their selected-reader conclusion is SUPERSEDED by the DESKTOP_CORRECTION_R1 branch-selection correction — their reports are immutable historical records; see 06_REPORT\AMEND_LOG_DESKTOP_CORRECTION_R1.md). The FRESH targeted QC round for this correction (QC-R3) has been executed: PASS_WITH_FINDINGS (04_QC\QC_R3_DESKTOP_CORRECTION\QC_R3_REPORT.md; 185/185 pins independently re-verified with its own PE32/x86/VFS toolchain; the A/B/C branch-selection discriminating detector PASS; P2-1/P2-2 fixed in the QC disposition, P3-1/P3-2 recorded as notational future-regeneration notes, P3-3 discharged by the persistence phase; see 06_REPORT\AMEND_LOG_DESKTOP_CORRECTION_R1.md section 11).
Q1_STATUS_CHANGED = NO
PE_MASTER_QUALIFICATION_CHANGED = NO
GATE_B_CHANGED = NO
M1_CHANGED = NO
M2_CHANGED = NO
M3_CHANGED = NO
COMMIT = NO
PUSH = NO

RUN_STATUS = CONSUMER_UNREACHED
(the destination field — the ArkParameterArmor instance's tag-0x11 (tag ID 17) property slot 21 — was reached with a byte-pinned end-to-end chain: routing CONFIRMED, the SELECTED client read CONFIRMED via the proven virtual branch (descriptor+0 != NULL -> [ArkRTTraitsInt.vtable+0x14] -> FUN_009777F0), the store CONFIRMED; but NO downstream consumer of the slot was identified: within the inspected 202 direct descriptor-lookup sites and the documented limited context window, no tag-ID-17 downstream reader was identified; full downstream static data-flow, aliases, indirect calls and global writer/read completeness remain UNVERIFIED; further static resolvability is NOT_ESTABLISHED. The gameplay semantic role remains UNVERIFIED per the separate FINAL_SEMANTIC_ROLE axis; the three axes are reported separately per §12. The pre-correction RUN_STATUS = CONSUMER_REACHED_ROLE_STRONGLY_SUPPORTED is superseded — it rested on the non-selected fallback-path trace and treated the destination slot as "the consumer".)

## Summary of the trace (one paragraph)

The value at payload+0x30 of a 20002.vfs record is the tag-0x11 (tag ID 17) property value of the record's TLV property block: every record carries six entries (tags 1, 0xC, 0xD, 0xE, 0x10, 0x11) under flags 0x80 and count 6, and the tag-0x11 value sits at payload+0x30 in 1366/1366 records. Class 20002 is the ArkParameterArmor parameter class (RTTI-confirmed); its class object opens its own data file as itoa(20002)+".vfs" and loads records on demand into ArkParameterArmor instances (0x58 bytes, 22-slot value arrays). The generic property parser dispatches the value read through FUN_0075f660, which selects the VIRTUAL branch for tag ID 17 because the tag's descriptor holds a non-NULL reader object (the static ArkRTTraitsInt singleton returned by the factory FUN_00977a50): the selected reader FUN_009777F0 reads the +0x30 field with a native 4-byte little-endian load (VA 0x00977807) and stores it — a pure copy, no comparison or lookup — into the instance's value-array slot 21 (VA 0x00977810), from which the generic property machinery can read it by tag at runtime (no statically-coded tag-0x11 reader was identified within the 202-site census). What the property means in gameplay and which code reads it at runtime remains open (bounded census documented; DOWNSTREAM_CONSUMER_IDENTIFIED = NO); no world/model/placement semantics are claimed.

## Package counts (freshly measured at the DESKTOP_CORRECTION_R1 executor close; no conflation)

- CURRENT PHYSICAL FILE COUNT (whole package on disk, incl. 00_CONTROL\DESKTOP_CORRECTION_R1\ with its BEFORE\ copies, 01_RAW\DESKTOP_CORRECTION_R1\, 03_SCRIPTS\desktop_correction_r1\, 04_QC\ and 06_REPORT\AMEND_LOG_DESKTOP_CORRECTION_R1.md): 420 files (measured 2026-10-02 at the correction close; composition: the 389 pre-correction physical files (388 manifest-covered + MANIFEST_SHA256.csv itself, self-excluded from its own rows per the L12 precedent) + 31 new correction-phase files (14 in 00_CONTROL\DESKTOP_CORRECTION_R1\ = 3 frozen formalizer files + BEFORE_COPIES_INDEX.json + 10 BEFORE copies; 5 in 01_RAW\DESKTOP_CORRECTION_R1\ = PREFLIGHT_RERUN.json + BRANCH_SELECTION_TRACE.json + FALLBACK_PATH_RECORD.json + CURSOR_PROOF_CORRECTION_R1.json + DESTINATION_PROOF_CORRECTION_R1.json; 11 in 03_SCRIPTS\desktop_correction_r1\ (incl. the post-correction manifest-bijection verification script); 1 = 06_REPORT\AMEND_LOG_DESKTOP_CORRECTION_R1.md)). Post-correction bijection verification (03_SCRIPTS\desktop_correction_r1\s7_post_correction_bijection.py): of the starting manifest's 388 file rows, 378 remain byte-identical, exactly the 10 corrected files differ, 0 missing, 0 ghosts.
- STARTING MANIFEST (06_REPORT\MANIFEST_SHA256.csv, byte-unchanged by this correction; its SHA256 CD938AD7C05C41A62B5847057A92EBF12C0B1890964AEC0ADCDA0F87ECE1E4BF re-verified at the correction preflight): 391 raw text lines = 1 header line + 388 file data rows + 1 blank separator line + 1 NOTE row; 389 total data rows (388 file rows + 1 NOTE row that is NOT a file row).
- MANIFEST STALENESS: the starting manifest is the historical census of the pre-correction state; it is stale for exactly the 10 corrected files (their post-correction bytes differ) and silent about the 31 new files. It is regenerated LAST by the persistence worker (self-excluded; bijection verified there); until then it stays byte-unchanged as historical evidence.
- POST-CLOSE GROWTH (persistence-phase state): the QC-R3 round added its 15 artifacts under 04_QC\QC_R3_DESKTOP_CORRECTION\ and the persistence phase (QC disposition + verdict persistence + manifest regeneration) edited package files; the FINAL census is the persisted MANIFEST_SHA256.csv with its verification record in 06_REPORT\AMEND_LOG_DESKTOP_CORRECTION_R1.md section 11 (the 420 figure above is the executor-close measurement, preserved as dated).

## Package

Evidence index: 06_REPORT\EVIDENCE_INDEX.md (corrected). Amendment/correction log: 06_REPORT\AMEND_LOG_DESKTOP_CORRECTION_R1.md (the DESKTOP_CORRECTION_R1 record incl. BEFORE/AFTER artifact pairs and the contradiction census). Manifest: 06_REPORT\MANIFEST_SHA256.csv (the starting historical census; known-stale until the final regeneration by the persistence worker after the fresh QC + PE-MASTER verdict; manifest self-exclusion per the L12 precedent: a manifest cannot contain its own hash).
HARD_STOP = YES (per contract §19; no automatic continuation). Correction-executor part ends at the amendment log; fresh QC, QC disposition, final report finalization, PE_MASTER_REVIEW supersession, manifest regeneration and persistence are separate PE-MASTER dispatches (NO_NESTED_TASKS).
