# EVIDENCE_INDEX — PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002

Claim -> artifact -> status. All VAs byte-pinned from the pinned physical EXE
(01_RAW\CLIENT_READ_BYTES.json, 45/45 pins OK).

## S0 identity
| CLAIM | ARTIFACT | STATUS |
|---|---|---|
| HEAD == 9203b6d1ad5025f4158d5165863594132aaac49f | 00_CONTROL\PREFLIGHT.md | CONFIRMED (measured) |
| EXE identity (8,015,872 B; E7785430...) | 00_CONTROL\PREFLIGHT.md; 00_CONTROL\SOURCE_IDENTITY.md | CONFIRMED (measured) |
| VFS identity (174,864 B; C3899C3E...) | 00_CONTROL\PREFLIGHT.md | CONFIRMED (measured) |

## S1 framing
| CLAIM | ARTIFACT | STATUS |
|---|---|---|
| 20002.vfs = ArkVFS02, base=0x80, 16-byte global header | 01_RAW\RECORD_FRAMING_SUMMARY.json | CONFIRMED (in-run walk) |
| 1,366 records, stride 128, exact-EOF consumption | 01_RAW\RECORD_FRAMING_SUMMARY.json; 01_RAW\RECORD_FRAMING.jsonl (1366 rows) | CONFIRMED (in-run implementation) |
| Record header {u32 id, u32 size=56, u32 ver=1, u32 crc=0} (all 1366) | 01_RAW\RECORD_FRAMING.jsonl | CONFIRMED (byte census) |
| Boundary agreement with the prior tool lineage | 01_RAW\CROSSVALIDATION_vfs_common.json (1366/1366) | CONFIRMED (cross-validation, labeled) |
| NC-FRAMING falsifiability | 01_RAW\RECORD_FRAMING_SUMMARY.json (nc_framing); 02_ANALYSIS\NEGATIVE_CONTROLS.md | PASS (4/4 mandatory classes detected; NC5 non-discriminating documented) |

## S2 field anchor
| CLAIM | ARTIFACT | STATUS |
|---|---|---|
| ANCHOR_PRIMARY = record 0; +0x30 raw BB 2E 00 00 = 11963 | 01_RAW\FIELD_BYTE_ANCHOR.json; 01_RAW\RECORD_FRAMING.jsonl row 0 | CONFIRMED (byte-level; bounds assertions machine-checked) |
| ANCHOR_ZERO = record 1014 (and 1015) value 0 | 01_RAW\FIELD_BYTE_ANCHOR.json; 01_RAW\RECORD_FRAMING_SUMMARY.json | CONFIRMED (re-derived in-run) |
| All 1366 records: u32@payload+0 = 20002; u16@+0x2E = 0x11 | 01_RAW\RECORD_FRAMING_SUMMARY.json (census) | CONFIRMED (byte census) |
| Width 4 / LE | 01_RAW\CLIENT_READ_BYTES.json (pin 0x412553, native dword load) | RAW_MEASUREMENT (upgraded from HYPOTHESIS_DERIVED per V2-009) |

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

## S4 client read
| CLAIM | ARTIFACT | STATUS |
|---|---|---|
| THE READ @0x00412553 (8B 04 10): 4-byte LE load at cursor offset 0x30 = payload+0x30 | 01_RAW\CLIENT_READ_BYTES.json; 01_RAW\GHIDRA_ROUTING\PASS13_DISASM_FUN_00412540.txt | CONFIRMED (byte-pinned) |
| THE STORE @0x0041255A (89 02) into value_array + (tag+4)*4 | same + PASS13_DISASM_FUN_0070cbc0.txt (ADD ECX,4) | CONFIRMED (byte-pinned) |
| TLV loop + schema (tag 0x11 = {type 1, flags 0xC0, field 21}) | 01_RAW\CLIENT_READ_BYTES.json (pins 0x761717/0x76171C/0x76171E/0x761722/0x70CBF6/0x70C1D3/0x70C1D6) | CONFIRMED (byte-pinned) |
| Instance = ArkParameterArmor (vtable 0xA878BC @0x761556; factory new(0x58)) | 01_RAW\CLIENT_READ_BYTES.json (pins 0x761547/0x761556) | CONFIRMED (byte-pinned) |
| Walk coverage: tag-0x11 value at +0x30 in 1366/1366; tail 0 in 1366/1366 | 01_RAW\TLV_WALK_CENSUS.json | CONFIRMED (machine walk) |

## S5 consumer census
| CLAIM | ARTIFACT | STATUS |
|---|---|---|
| Write path unique (FUN_0075f660 has exactly 1 caller) | 01_RAW\RELEVANT_XREFS.json; 01_RAW\GHIDRA_ROUTING\PASS11_GHIDRA_DUMP.json | CONFIRMED (xref census) |
| 202 descriptor-lookup sites; 0 static tag-0x11 readers (2 false positives examined) | 01_RAW\GHIDRA_ROUTING\PASS15_GHIDRA_DUMP.json; 02_ANALYSIS\DESTINATION_CONSUMER_CENSUS.json | CONFIRMED (bounded census; global exhaustiveness UNVERIFIED) |

## S6 semantics
| CLAIM | ARTIFACT | STATUS |
|---|---|---|
| OBSERVED_OPERATION = pure copy (no lookup/comparison/branch on the value) | 02_ANALYSIS\SEMANTIC_ASSESSMENT.md; pins 0x412553/0x41255A | CONFIRMED |
| FIELD_IDENTITY (structural: tag-0x11 property of ArkParameterArmor records) | 02_ANALYSIS\SEMANTIC_ASSESSMENT.md | CONFIRMED (structural) |
| FINAL_SEMANTIC_ROLE (gameplay meaning) | 02_ANALYSIS\SEMANTIC_ASSESSMENT.md | UNVERIFIED (baseline not lifted) |

## S7 negative controls
| CONTROL | ARTIFACT | RESULT |
|---|---|---|
| NC-FRAMING | 01_RAW\RECORD_FRAMING_SUMMARY.json; 02_ANALYSIS\NEGATIVE_CONTROLS.md | PASS |
| NC-ANCHOR-ADJ (feasible + instruction level) | 02_ANALYSIS\NEGATIVE_CONTROLS.md; 01_RAW\FIELD_BYTE_ANCHOR.json | PASS |
| NC-RECORD | 01_RAW\TLV_WALK_CENSUS.json (1366/1366 same shape) | PASS |
| NC-VALUE | 02_ANALYSIS\NEGATIVE_CONTROLS.md | NOT_APPLICABLE_NO_LOOKUP_COMPARISON_CLAIMED (documented) |

## S8 blast radius
| ITEM | ARTIFACT | RESULT |
|---|---|---|
| id2-domain membership observation (AMEND_R2) | 02_ANALYSIS\BLAST_RADIUS.md | PRIOR_CLAIMS_UNCHANGED (context only; raw basis re-derived and agrees) |
| FUN_00959090 lead | 02_ANALYSIS\BLAST_RADIUS.md; 02_ANALYSIS\VFS_TO_PARSER_TRACE.md §6 | PRIOR_CLAIMS_NARROWED (lead corrected in-package; lead was marked LEADS_TO_REVERIFY) |
| Loader-chain VAs (JOIN R1 claim 5) | 02_ANALYSIS\BLAST_RADIUS.md | PRIOR_CLAIMS_NARROWED (mechanism CONFIRMED in FUN_0070c680; the historical FUN_0070E810 attribution CONTRADICTED by bytes — see 02_ANALYSIS\BLAST_RADIUS.md item 6 + 06_REPORT\AMEND_LOG_R1.md) |
| WORLD_INSTANCE_TO_MODEL_LINK / PLACEMENT_SOURCE | 02_ANALYSIS\BLAST_RADIUS.md | UNCHANGED (NOT_DEMONSTRATED / NOT_RECOVERED) |
