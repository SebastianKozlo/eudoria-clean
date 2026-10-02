# EVIDENCE_INDEX — PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002

Claim -> artifact -> status. All VAs byte-pinned from the pinned physical EXE.
Correction state: DESKTOP_CORRECTION_R1 — the §S4 rows and statuses below reflect the
SELECTED-reader chain (the virtual branch -> FUN_009777F0); the pre-correction
selected-reader rows are superseded (correction record:
06_REPORT\AMEND_LOG_DESKTOP_CORRECTION_R1.md; BEFORE copy of this index:
00_CONTROL\DESKTOP_CORRECTION_R1\BEFORE\06_REPORT\EVIDENCE_INDEX.md).

## S0 identity
| CLAIM | ARTIFACT | STATUS |
|---|---|---|
| HEAD == 9203b6d1ad5025f4158d5165863594132aaac49f | 00_CONTROL\PREFLIGHT.md; 01_RAW\DESKTOP_CORRECTION_R1\PREFLIGHT_RERUN.json (correction-preflight re-measurement) | CONFIRMED (measured at run start and at correction start) |
| EXE identity (8,015,872 B; E7785430...) | 00_CONTROL\PREFLIGHT.md; 00_CONTROL\SOURCE_IDENTITY.md; 01_RAW\DESKTOP_CORRECTION_R1\PREFLIGHT_RERUN.json | CONFIRMED (measured) |
| VFS identity (174,864 B; C3899C3E...) | 00_CONTROL\PREFLIGHT.md; 01_RAW\DESKTOP_CORRECTION_R1\PREFLIGHT_RERUN.json | CONFIRMED (measured) |
| Correction-contract identity (21,076 B; 1E592EBC...) + starting-manifest identity (50,698 B; CD938AD7...) | 01_RAW\DESKTOP_CORRECTION_R1\PREFLIGHT_RERUN.json | CONFIRMED (measured at correction preflight) |

## S1 framing
| CLAIM | ARTIFACT | STATUS |
|---|---|---|
| 20002.vfs = ArkVFS02, base=0x80, 16-byte global header | 01_RAW\RECORD_FRAMING_SUMMARY.json | CONFIRMED (in-run walk) |
| 1,366 records, stride 128, exact-EOF consumption | 01_RAW\RECORD_FRAMING_SUMMARY.json; 01_RAW\RECORD_FRAMING.jsonl (1366 rows); 01_RAW\DESKTOP_CORRECTION_R1\CURSOR_PROOF_CORRECTION_R1.json (independent re-derivation: 16 + 1366*128 == 174,864) | CONFIRMED (in-run implementation + correction re-derivation) |
| Record header {u32 id, u32 size=56, u32 ver=1, u32 crc=0} (all 1366) | 01_RAW\RECORD_FRAMING.jsonl; 01_RAW\DESKTOP_CORRECTION_R1\CURSOR_PROOF_CORRECTION_R1.json (census: sizes_56/ver_1/crc_0 = 1366/1366) | CONFIRMED (byte census) |
| Boundary agreement with the prior tool lineage | 01_RAW\CROSSVALIDATION_vfs_common.json (1366/1366) | CONFIRMED (cross-validation, labeled) |
| NC-FRAMING falsifiability | 01_RAW\RECORD_FRAMING_SUMMARY.json (nc_framing); 02_ANALYSIS\NEGATIVE_CONTROLS.md | PASS (4/4 mandatory classes detected; NC5 non-discriminating documented) |

## S2 field anchor
| CLAIM | ARTIFACT | STATUS |
|---|---|---|
| ANCHOR_PRIMARY = record 0; +0x30 raw BB 2E 00 00 = 11963 | 01_RAW\FIELD_BYTE_ANCHOR.json; 01_RAW\RECORD_FRAMING.jsonl row 0; 01_RAW\DESKTOP_CORRECTION_R1\CURSOR_PROOF_CORRECTION_R1.json (record_0_walk: raw BB2E0000, LE 11963) | CONFIRMED (byte-level; bounds assertions machine-checked) |
| ANCHOR_ZERO = record 1014 (and 1015) value 0 | 01_RAW\FIELD_BYTE_ANCHOR.json; 01_RAW\RECORD_FRAMING_SUMMARY.json; 01_RAW\DESKTOP_CORRECTION_R1\CURSOR_PROOF_CORRECTION_R1.json (record_1014_walk: raw 00000000; zero_records [1014, 1015]) | CONFIRMED (re-derived in-run, twice) |
| All 1366 records: u32@payload+0 = 20002; u16@+0x2E = 0x11 | 01_RAW\RECORD_FRAMING_SUMMARY.json (census) | CONFIRMED (byte census) |
| Width 4 / LE | 01_RAW\DESKTOP_CORRECTION_R1\BRANCH_SELECTION_TRACE.json (the SELECTED read pin 0x00977807, 8B 04 10, native dword load); 01_RAW\CLIENT_READ_BYTES.json (the fallback read pin 0x00412553 — same width/endianness, byte-correct fallback evidence) | RAW_MEASUREMENT (upgraded from HYPOTHESIS_DERIVED per V2-009) |

## S3 routing
| CLAIM | ARTIFACT | STATUS |
|---|---|---|
| Class 20002 = ArkParameterArmor (RTTI; $0EOCC@ mangling, calibrated vs $0EOCG@=20006) | 01_RAW\ROUTING_CENSUS_RAW.json; 01_RAW\CLIENT_READ_BYTES.json (string pins) | CONFIRMED (string/RTTI level) |
| 3 imm32 0x4E22 sites; the registration ctor FUN_0073a3f0 | 01_RAW\ROUTING_CENSUS_RAW.json; 01_RAW\RELEVANT_XREFS.json | CONFIRMED (byte census) |
| Registry: FUN_0073c870 case 0x4E22 -> DAT_00ba5da8 | 01_RAW\CLIENT_READ_BYTES.json (pin 0x73C8C1) | CONFIRMED (byte-pinned) |
| Open chain: itoa(classID)+".vfs" -> FUN_00972df0; reader at classObj+0x84 | 01_RAW\CLIENT_READ_BYTES.json (pins 0x70C3FC/0x70C40E/0x70C742/0x70C71E) | CONFIRMED (byte-pinned) |
| Index builder stride rule ((size+0xF)/base+1)*base-0x10 | 01_RAW\GHIDRA_ROUTING\DISASM_FUN_00972ad0.txt; PASS2_DISASM_FUN_00979d00.txt | CONFIRMED (instruction level) |
| CRC gate skipped (all crc fields 0) | 01_RAW\CLIENT_READ_BYTES.json (pins 0x971B4A/0x971B4C); 01_RAW\RECORD_FRAMING.jsonl (crc=0 census) | CONFIRMED (byte+instruction) |
| GENERIC_PARSER_IDENTIFIED=YES; 20002_VFS_ROUTED_TO_GENERIC_PARSER=CONFIRMED | 02_ANALYSIS\VFS_TO_PARSER_TRACE.md | CONFIRMED (chain byte-pinned) |
| FUN_00959090 family = EnvironmentZones.vfs (lead correction) | 01_RAW\GHIDRA_ROUTING\PASS3_DECOMP_FUN_00958d90.txt ("EnvironmentZones" string); 02_ANALYSIS\VFS_TO_PARSER_TRACE.md §6 | CONFIRMED (string byte-proven) |

## S4 client read (CORRECTED — the SELECTED reader chain)
| CLAIM | ARTIFACT | STATUS |
|---|---|---|
| Tag-ID-17 registration: factory call FUN_00977a50 @0x76170F; PUSH EAX (arg5) @0x761714; PUSH 0 (arg4) @0x761715; PUSH 0xC0 (flags) @0x761717; PUSH 1 (type) @0x76171C; PUSH 0x11 (tag) @0x76171E; MOV ECX,ESI @0x761720; CALL FUN_0070cbc0 @0x761722 | 01_RAW\DESKTOP_CORRECTION_R1\BRANCH_SELECTION_TRACE.json (pins; all 96/96 match) | CONFIRMED (byte-pinned) |
| Factory FUN_00977a50 return behavior: lazy-init flag byte 0xBA9380; vtable store [0xBA937C]=0xA9C670 @0x977A68; atexit-style registration (destructor 0xA744B0 -> helper 0x95D4DB) @0x977A63/0x977A72; BOTH paths return EAX=0x00BA937C (non-NULL static .data address; no NULL-return path) | 01_RAW\DESKTOP_CORRECTION_R1\BRANCH_SELECTION_TRACE.json (factory pins + the destructor context pin) | CONFIRMED (byte-pinned) |
| Descriptor+0 dataflow: FUN_0070cbc0 arg5 -> FUN_0075f5c0 -> descriptor+0 store @0x75F5CA; field index = tag+4 @0x70CBF6; the insert FUN_0070c980 (tag==count invariant @0x70C9AE/0x70C9B0) -> vector append FUN_0070c7b0 (element+0 = the object pointer @0x70C7C1/0x70C7C3; end += 0x10 @0x70C7D8); lookup = [classObj+0x88] + tag*0x10 @0x70C1D3/0x70C1D6 | 01_RAW\DESKTOP_CORRECTION_R1\BRANCH_SELECTION_TRACE.json (dataflow pins) | CONFIRMED (byte-pinned) |
| THE BRANCH SELECTION: FUN_0075f660 loads [descriptor+0] @0x75F662; TEST @0x75F664; JZ -> fallback @0x75F66E — NOT TAKEN for tag ID 17 (descriptor+0 = 0x00BA937C != NULL) => THE VIRTUAL BRANCH IS SELECTED (control-flow reachability from the proven descriptor state) | 01_RAW\DESKTOP_CORRECTION_R1\BRANCH_SELECTION_TRACE.json (dispatch pins + the branch_selection_chain) | CONFIRMED (byte-pinned + reachability-stated) |
| THE SELECTED SLOT: vtable 0xA9C670 (from the factory store) + 0x14 -> the dword at 0x00A9C684 (FO 0x69C684, bytes F0 77 97 00) = 0x009777F0 | 01_RAW\DESKTOP_CORRECTION_R1\BRANCH_SELECTION_TRACE.json (the slot-dword pin) | CONFIRMED (byte-pinned; static .rdata read) |
| THE SELECTED READ @0x00977807 (8B 04 10; RVA 0x00577807; FO 0x00577807): 4-byte LE load at cursor.base+offset == payload+0x30 at the tag-ID-17 iteration | 01_RAW\DESKTOP_CORRECTION_R1\BRANCH_SELECTION_TRACE.json (reader pins); 01_RAW\DESKTOP_CORRECTION_R1\CURSOR_PROOF_CORRECTION_R1.json (the +0x30 derivation: record 0 + record 1014 + 1366/1366) | CONFIRMED (byte-pinned + cursor re-derived) |
| THE SELECTED STORE @0x00977810 (89 02) into value_array + (tag+4)*4 = slot 21 (+0x54), width 4 | 01_RAW\DESKTOP_CORRECTION_R1\DESTINATION_PROOF_CORRECTION_R1.json (23/23 pins: the LEA chain 0x726A11/0x726A14 + dest pass-through + the reader's dest load @0x97780A) | CONFIRMED (byte-pinned) |
| RTTI identity of the reader object: [vtable-4]=0xAB8360 (COL) -> TypeDescriptor 0xB9F10C -> name .?AUArkRTTraitsInt@@ (the ArkRTTraitsInt class) | 01_RAW\DESKTOP_CORRECTION_R1\BRANCH_SELECTION_TRACE.json (RTTI walk pins) | CONFIRMED (byte-pinned) |
| THE FALLBACK (non-selected): FUN_00412540 with READ @0x00412553 / FO 0x12553 / STORE @0x0041255A / FO 0x1255A; reachable only when descriptor+0 == NULL (the JZ @0x75F66E target); the old REPORT transcription 0x00125553 superseded (digit-shift) | 01_RAW\DESKTOP_CORRECTION_R1\FALLBACK_PATH_RECORD.json (25/25 pins incl. the flags-bit0 gate, the type switch, the jump table, the reader window, the error path) | CONFIRMED AS BYTE-CORRECT EVIDENCE OF A NON-SELECTED FALLBACK PATH |
| TLV loop + schema (tag 0x11 = {type 1, flags 0xC0, field 21}) | 01_RAW\CLIENT_READ_BYTES.json (pins 0x761717/0x76171C/0x76171E/0x761722/0x70CBF6/0x70C1D3/0x70C1D6; byte-correct, reader-role fields describe the fallback evidence) + BRANCH_SELECTION_TRACE.json | CONFIRMED (byte-pinned) |
| Instance = ArkParameterArmor (vtable 0xA878BC @0x761556; factory new(0x58)); value array = 22 slots at instance+0x40 (count+4 @0x70D9B8/0x70D9BB; instance+0x40 @0x70D9BF) | 01_RAW\CLIENT_READ_BYTES.json (pins 0x761547/0x761556); 01_RAW\DESKTOP_CORRECTION_R1\DESTINATION_PROOF_CORRECTION_R1.json (allocation pins) | CONFIRMED (byte-pinned) |
| Walk coverage: tag-0x11 value at +0x30 in 1366/1366; tail 0 in 1366/1366; full consumption (final offset == 56) in 1366/1366 | 01_RAW\TLV_WALK_CENSUS.json; 01_RAW\DESKTOP_CORRECTION_R1\CURSOR_PROOF_CORRECTION_R1.json (independent re-derivation + the success-vs-error path distinction + 3 negative simulations DETECTED) | CONFIRMED (machine walk, twice) |

## S5 consumer census
| CLAIM | ARTIFACT | STATUS |
|---|---|---|
| Write path unique within the censused machinery (FUN_0075f660 has exactly 1 caller; the selected type-1 store @0x00977810; ONE_DIRECT_CALLER_FOUND scoped to the censused machinery — NOT global slot-21-writer proof) | 01_RAW\RELEVANT_XREFS.json; 01_RAW\GHIDRA_ROUTING\PASS11_GHIDRA_DUMP.json; 02_ANALYSIS\DESTINATION_CONSUMER_CENSUS.json (corrected) | CONFIRMED (bounded census; global write-side exhaustiveness UNVERIFIED, W-1) |
| 202 descriptor-lookup sites; 0 static tag-0x11 readers identified (2 false positives examined); DOWNSTREAM_CONSUMER_IDENTIFIED = NO | 01_RAW\GHIDRA_ROUTING\PASS15_GHIDRA_DUMP.json; 02_ANALYSIS\DESTINATION_CONSUMER_CENSUS.json (corrected bounded wording) | CONFIRMED (bounded census; global exhaustiveness UNVERIFIED; further static resolvability NOT_ESTABLISHED) |

## S6 semantics
| CLAIM | ARTIFACT | STATUS |
|---|---|---|
| OBSERVED_OPERATION = pure copy (no lookup/comparison/branch on the value; the selected reader's conditionals test cursor state only) | 02_ANALYSIS\SEMANTIC_ASSESSMENT.md (corrected); pins 0x977807/0x977810 | CONFIRMED |
| FIELD_IDENTITY (structural: the tag-ID-17 property of ArkParameterArmor records) | 02_ANALYSIS\SEMANTIC_ASSESSMENT.md | CONFIRMED (structural) |
| FINAL_SEMANTIC_ROLE (gameplay meaning) | 02_ANALYSIS\SEMANTIC_ASSESSMENT.md | UNVERIFIED (baseline not lifted; id2-domain correlation CANDIDATE/UNVERIFIED — numeric-domain overlap is not semantic proof) |
| RUN_STATUS = CONSUMER_UNREACHED (the destination slot is not a downstream consumer; the downstream-consumer axis is honestly NO) | 02_ANALYSIS\SEMANTIC_ASSESSMENT.md; 06_REPORT\REPORT.md | CONFIRMED (corrected; supersedes CONSUMER_REACHED_ROLE_STRONGLY_SUPPORTED) |

## S7 negative controls
| CONTROL | ARTIFACT | RESULT |
|---|---|---|
| NC-FRAMING | 01_RAW\RECORD_FRAMING_SUMMARY.json; 02_ANALYSIS\NEGATIVE_CONTROLS.md | PASS |
| NC-ANCHOR-ADJ (feasible + instruction level with the SELECTED reader's instructions) | 02_ANALYSIS\NEGATIVE_CONTROLS.md; 01_RAW\FIELD_BYTE_ANCHOR.json | PASS |
| NC-RECORD | 01_RAW\TLV_WALK_CENSUS.json (1366/1366 same shape); 01_RAW\DESKTOP_CORRECTION_R1\CURSOR_PROOF_CORRECTION_R1.json (record 0 + record 1014 identical walk states) | PASS |
| NC-VALUE | 02_ANALYSIS\NEGATIVE_CONTROLS.md | NOT_APPLICABLE_NO_LOOKUP_COMPARISON_CLAIMED (documented) |
| NC (correction-specific): the cursor-walk error paths (truncated payload / flag-clear entry / corrupted count) are DETECTED by the byte-derived simulation (3/3) | 01_RAW\DESKTOP_CORRECTION_R1\CURSOR_PROOF_CORRECTION_R1.json (negative_simulations_on_record_0) | PASS (the success path vs the reader's error/failure paths are distinguished) |

## S8 blast radius
| ITEM | ARTIFACT | RESULT |
|---|---|---|
| id2-domain membership observation (AMEND_R2) | 02_ANALYSIS\BLAST_RADIUS.md | PRIOR_CLAIMS_UNCHANGED (context only; raw basis re-derived and agrees twice) |
| FUN_00959090 lead | 02_ANALYSIS\BLAST_RADIUS.md; 02_ANALYSIS\VFS_TO_PARSER_TRACE.md §6 | PRIOR_CLAIMS_NARROWED (lead corrected in-package; lead was marked LEADS_TO_REVERIFY) |
| Loader-chain VAs (JOIN R1 claim 5) | 02_ANALYSIS\BLAST_RADIUS.md | PRIOR_CLAIMS_NARROWED (mechanism CONFIRMED in FUN_0070c680; the historical FUN_0070E810 attribution CONTRADICTED by bytes — see 02_ANALYSIS\BLAST_RADIUS.md item 6 + 06_REPORT\AMEND_LOG_R1.md; the historical JOIN R1 file untouched) |
| DESKTOP P1: the branch selection (added by DESKTOP_CORRECTION_R1) | 02_ANALYSIS\BLAST_RADIUS.md item 7; 06_REPORT\AMEND_LOG_DESKTOP_CORRECTION_R1.md | SELF-CORRECTION ISSUED (the active selected-reader trace FUN_00412540 @0x00412553/0x0041255A superseded by the proven virtual-branch selection to FUN_009777F0; the QC rounds 1/2 selected-reader conclusion superseded — their reports immutable; lesson: "correct instruction bytes != proven selected execution/parser path") |
| WORLD_INSTANCE_TO_MODEL_LINK / PLACEMENT_SOURCE | 02_ANALYSIS\BLAST_RADIUS.md | UNCHANGED (NOT_DEMONSTRATED / NOT_RECOVERED) |

## S9 correction governance (new; DESKTOP_CORRECTION_R1)
| ITEM | ARTIFACT | STATUS |
|---|---|---|
| Correction contract identity + C0 preflight re-measurements | 00_CONTROL\DESKTOP_CORRECTION_R1\CORRECTION_RUN_CONTRACT.md (frozen); 01_RAW\DESKTOP_CORRECTION_R1\PREFLIGHT_RERUN.json | CONFIRMED (all identities re-measured MATCH) |
| BEFORE-copy discipline (10 changed files, byte-for-byte + size + SHA256; the 10th was added when the contradiction census found a stale live copy in VFS_TO_PARSER_TRACE.md) | 00_CONTROL\DESKTOP_CORRECTION_R1\BEFORE\BEFORE_COPIES_INDEX.json + the 10 mirrored copies | CONFIRMED (verified byte-identical at copy time) |
| The amendment/correction log (superseded claims, BEFORE/AFTER pairs, the contradiction census, the affected dependency set, remaining unknowns, the §8 lesson, the QC1/QC2 superseded-conclusion record) | 06_REPORT\AMEND_LOG_DESKTOP_CORRECTION_R1.md | THE correction record (this index points to it) |
| Fresh QC for this correction (QC-R3, EXECUTED) | 04_QC\QC_R3_DESKTOP_CORRECTION\QC_R3_REPORT.md + QC_R3_PINVERIFY_RESULT.json + QC_R3_BRANCH_MODEL_RESULT.json + QC_R3_VFS_WALK_RESULT.json + QC_R3_BEFORE_COPIES_RESULT.json + QC_R3_WORDING_SWEEP_RESULT.json | PASS_WITH_FINDINGS (0xP0/P1; 2xP2 fixed in the QC disposition per PE-MASTER order; 3xP3 recorded; 185/185 own pins verified; the A/B/C discriminating detector PASS with all 3 mutant models DETECTED; every QC gate predicate of contract §6 PASS) |
