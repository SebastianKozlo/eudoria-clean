# INPUT_IDENTITIES — PE_935_CAND4_006C9700_PLUS4_POST_AUDIT_CORRECTION_R1_20261008

All queries below were executed by this executor phase (fail-closed) before
any package write. Tools: git (repo at
D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean), PowerShell 5.1,
Python 3.12.10 (MSC v.1943 64 bit; `python -B` everywhere; no bytecode).

## §1. Base state (fresh queries; command | UTC timestamp | exit | returned SHA)

```text
git rev-parse HEAD            | 2026-10-08T13:30:28Z | exit 0 | fd481c567868b601ffa4be442ab55a7cffaeacd6
git rev-parse origin/master   | 2026-10-08T13:30:28Z | exit 0 | fd481c567868b601ffa4be442ab55a7cffaeacd6
git ls-remote origin master   | 2026-10-08T13:30:46Z | exit 0 | fd481c567868b601ffa4be442ab55a7cffaeacd6  (refs/heads/master)
EXPECTED_BASE_SHA = fd481c567868b601ffa4be442ab55a7cffaeacd6
LOCAL_HEAD_EQ_ORIGIN_EQ_ACTUAL_REMOTE = YES   (triple check PASS; no retry needed)
```

Working tree at preflight: ZERO tracked changes (`git status --porcelain=v1`,
exit 0). OUTPUT_ROOT
(docs/audits/PE_935_CAND4_006C9700_PLUS4_POST_AUDIT_CORRECTION_R1_20261008)
did NOT exist at preflight (Test-Path = False); created only after preflight
PASS.

Foreign untracked census at preflight (recorded, NEVER touched/staged/cleaned):

```text
?? docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/
?? docs/audits/PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003/
?? docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/
?? docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/
?? docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/
?? experiments/
```

## §2. Pinned inputs (SIZE + SHA256, all measured MATCH; any mismatch/missing would have been BLOCKED_INPUT_IDENTITY)

| input | path | pinned size / SHA256 | measured size / SHA256 | verdict |
|---|---|---|---|---|
| CONTRACT | C:\Users\User\Documents\ChatGPT\PE\PE_PLUS4_CORRECTION_PROMPT_REVIEW_20261008\OPENCODE_PLUS4_RECORDS_QC_CORRECTION_R2.md | 23704 / 37248BDBD47ACBAB96CA4D02E0738123444412842B227E2E7C9A38EAF6132251 | 23704 / 37248BDBD47ACBAB96CA4D02E0738123444412842B227E2E7C9A38EAF6132251 | MATCH (read IN FULL, 510 lines) |
| DESKTOP_POST_AUDIT | C:\Users\User\Documents\ChatGPT\PE\PE_935_FUN006C9700_PLUS4_DESKTOP_POST_AUDIT_FD481C5_20261008\REPORT.md | 15346 / BF9C8C7903F984B0F3579B48A7EA5B9479BF4E9BE697F98EF0A6EFFAE6D2505B | 15346 / BF9C8C7903F984B0F3579B48A7EA5B9479BF4E9BE697F98EF0A6EFFAE6D2505B | MATCH (read IN FULL before any work) |
| DESKTOP_SCOPE_REASSESSMENT | ...\PE_935_FUN006C9700_PLUS4_DESKTOP_POST_AUDIT_FD481C5_20261008\SCOPE_REASSESSMENT.csv | 7668 / C21DA7BA52F935D56FEE1864A283DC0DB8836A3AF58414C93C80CEA9EC78EF6B | 7668 / C21DA7BA52F935D56FEE1864A283DC0DB8836A3AF58414C93C80CEA9EC78EF6B | MATCH (read in full) |
| DESKTOP_COUNTERCHECKS | ...\PE_935_FUN006C9700_PLUS4_DESKTOP_POST_AUDIT_FD481C5_20261008\COUNTERCHECKS.json | 38977 / A1F6A943E5A67C51F990126727C8A35CD0579CA9F70E5A7960911774210823AC | 38977 / A1F6A943E5A67C51F990126727C8A35CD0579CA9F70E5A7960911774210823AC | MATCH (read in full) |
| ORIGINAL_MICRORUN_CONTRACT | C:\Users\User\Documents\ChatGPT\PE\PE_FUN006C9700_PLUS4_MICRORUN_PROMPT_R2_20261008\OPENCODE_FUN006C9700_PLUS4_MICRORUN_R2.md | 17487 / A6ABFE5E155F3FBAECDCC52E9D9A5E2B18D4286E67192C1C6717B3899EA2B20C | 17487 / A6ABFE5E155F3FBAECDCC52E9D9A5E2B18D4286E67192C1C6717B3899EA2B20C | MATCH (read IN FULL; source of the original budgets) |
| DESKTOP_ENGINE_RESEARCH (guardrails ONLY) | C:\Users\User\Documents\ChatGPT\PE\PE_H4_P_GETTER_ENGINE_RESEARCH_20261008\REPORT.md | 17960 / D1B6B4A0F66D0BEAF65FBE7F9A97CC55BA7474A69DC51761E1B9DF500852E316 | 17960 / D1B6B4A0F66D0BEAF65FBE7F9A97CC55BA7474A69DC51761E1B9DF500852E316 | MATCH (read in full; interpretive guardrails, NOT PCG byte proof) |
| EXE | D:\Eudoria_Reconstruction\pcg_install\Entropia.exe | 8015872 / E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 | 8015872 / E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 | MATCH (re-measured again inside the controls run, before AND after all controls — unchanged) |

## §3. Physical EXE access census (contract §2 — the ONLY reads performed)

| class | what | used VA / range | result |
|---|---|---|---|
| full re-hash | whole file identity | whole file (8015872 B) | E7785430...F31 (pinned, MATCH); re-verified unchanged after all controls |
| PE header parse | MZ/PE, machine 0x014C, PE32 magic 0x010B, measured ImageBase | file offsets 0x00..0x148 (e_lfanew 0x120; 5 sections) | ImageBase 0x00400000 (== pin); sections measured (see §6) |
| existing-pin reads (b) | the historical checker's BYTE_PINS/REL32_PINS/RTTI_PINS/STRING_PINS, re-executed by the successor gate on the clean baseline | the 57 pin VAs, 16 rel32 VAs, 3 RTTI chain ranges (vtable[-1] 4 B; COL 20 B; TD name len+1), 3 string VAs — every range raw-backed | 80/80 PASS (REGRESSION_RESULTS.json) |
| existing-pin reads (c) | the COL/TypeDescriptor/name ranges pointed to by the RTTI pins (no new classes/vtables) | 0x00A864B4, 0x00AA7770(+20 B), 0x00B8CAC4+8(+name); 0x00A855CC, 0x00AA6C58, 0x00B8C1B0+8; 0x00A85A04, 0x00AA6CD8, 0x00B8C1D4+8; strings 0x00A85DA4/0x00A859F8/0x00A8547C | all raw-backed, all MATCH (RTTI/STR gates PASS) |
| W-ctor 5-byte re-read (d) | the 5 bytes @0x006CB836 | VA 0x006CB836..0x006CB83A (physical offset 0x2CB836, .text raw) | E8 75 F0 02 00 (see §6; the callee FUN_006FA8B0 NOT opened) |
| BSS VA classification (e) | the two named BSS VAs from headers, NO physical bytes fetched | VA 0x00BA1100, VA 0x00BA73BC | both VIRTUAL_BSS (.data zero-init tail; delta past raw range); physical read = controlled FAIL |
| in-memory mutations | MC1..MC6 + the W-record JSON mutation gates | in-memory TEST-OVERRIDE copies only | physical file NEVER modified (SHA unchanged before/after) |

NOT accessed: the rest of FUN_007B79B0; the bodies FUN_007B7930 /
FUN_006B2310 / any other PCG function; any new xref/callgraph; any writer
search; runtime/client; VFS/BNT/NIF; transform/XYZ; any new
class-atlas/vtable; any new Gamebryo/OpenMW research; any new oracle source.

## §4. READ_ONLY source package census (path + Git blob identity vs BASE fd481c5)

`docs/audits/PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008/` — 28 files;
every physical file compared to its BASE Git blob (`git hash-object` physical
== `git rev-parse HEAD:<path>`); **28/28 identical, 0 mismatches**. The
package was NOT modified; its write-phase scripts were NOT executed.

```text
OK 00_CONTROL_INTERNAL_QC/QC_PHASE_INPUTS.md          blob c2f89420af2ec8a92824183b2b87c500a4b3c601
OK 00_CONTROL_INTERNAL_QC/QC_RESULTS.json            blob 2f2349459c9a67d3573f4c70684c4dc9cfc8881a
OK 00_CONTROL_INTERNAL_QC/qc_adjudication_append.py  blob 1fbc2ee84f17f83c0ab5a153c4e4b67e31603a9a
OK 00_CONTROL_INTERNAL_QC/qc_independent_check.py    blob ad0a0b476351fb05e3fb86c38f61d33e23e96770
OK 01_RAW/FUN_006C9570_SLOT_SETTER.txt               blob 5e1cd407658363f3c1803a9349c93cfd89851960
OK 01_RAW/FUN_006C9700_PUMP_FULL.txt                 blob dffafa0112709a6b9f0a5901c4592bda6a1e91dc
OK 01_RAW/FUN_006E8F70_CTOR_R.txt                    blob 727e56143727055cd1c34a9701bd05022cdf73a1
OK 01_RAW/FUN_007B79B0_P_GETTER_PARTIAL.txt          blob 0d22e657c5dc2f9dd817e3ed20c9603a9bcb9718
OK 01_RAW/MANUAL_ENCODING_CROSSCHECK.txt             blob eea2876a460d871a37ea03daee38edd9702323f1
OK 01_RAW/PINS_AND_REL32.txt                          blob 7696829d5860fc69ed570f91a4a790a5ee857db2
OK 01_RAW/RTTI_AND_STRINGS.txt                        blob be2d81390c07d6a5f640923f750b3913f836a549
OK 03_SCRIPTS/checker_plus4.py                        blob 29014f9f76cacce21177e925be2dc4b970815494
OK 03_SCRIPTS/run_controls.py                         blob 246ee79a5e63f86a6b65ba78c681e27a90356987
OK CLAIM_MATRIX.csv                                   blob e516551b2154d7da6c582e0ea8611d65d03f6849
OK CONTROL_RESULTS.json                               blob b5d379e221f8a409312ba71e02021b73ad944278
OK EDGE_ACCOUNTING_LEDGER.csv                        blob e5c48409f4bd8f66086b9a24f806b6e41457dd05
OK FINAL_REPORT.md                                   blob 6354cf49710f08321b4c3a3031d508546e14c1d1
OK FUNCTION_BODY_ACCOUNTING.csv                      blob ffadbe803c079f7b5a2cb1a44907d20440564c46
OK HANDOFF.md                                        blob 3a17707cbc79d0e911568f839069e1d9f08cc49a
OK INPUT_IDENTITIES.md                               blob 638372cba21ce9cf023c364f8f5294453596d367
OK MANIFEST_SHA256.csv                               blob 663f2ed26118a6abd771a7fff0d13660ed2579c
OK PE_MASTER_REVIEW.md                                blob 0f4a4dfd0d085c83c5542f06af62d43812c50a49
OK PLUS4_PROVENANCE.csv                              blob 19dd120a461745c671b28fd29d70f2033f581177
OK POINTER_LINEAGE.csv                               blob abac163a3f54814943fc008bf3b1abe1921a17c7
OK PREREGISTRATION.md                                blob e881150978138e8d872b2a72951452fd1490eeca
OK QC_REPORT.md                                      blob 894111d106d4d962f22ca09c6220866bb92962e9a
OK RETURN_VALUE_TRACE.csv                            blob 8102fc44d87a3e929a8e3138a35f72a08031e9de
OK SOURCE_STATE.md                                   blob d30f00b5ea00e7f21587d420a4a7d76cd477879f
```

Load-bearing quoted records re-verified against the blobs during the
corrections: 01_RAW/MANUAL_ENCODING_CROSSCHECK.txt (SHA256
540CA5839C00DE0299EA3DCC1392CDF666ECC00AF4EB827C8E887C1D43F750AF — the
correct prior W-ctor record, item 13) and
03_SCRIPTS/checker_plus4.py (SHA256
F58D2DB36106006BA2CBF931DC9CFED872E9C5E22C5484E86462568B985AB7E8 — the
required-ID source of the 80-check regression; parsed READ-ONLY via AST,
never executed).

## §5. Toolchain / decoder lineage

- Python 3.12.10; `python -B` + `sys.dont_write_bytecode` everywhere (no
  `__pycache__`/`.pyc` created under OUTPUT_REPO_PATH).
- NO disassembler was invoked by this run (no capstone); the successor gate
  works from raw byte equality, own rel32 arithmetic and RTTI chain walks
  only. The historical decodes are re-verified as BYTE PINS, not re-decoded.
- No runtime; no network beyond the required `git ls-remote` (§1); scratch
  work in C:\Users\User\AppData\Local\Temp\opencode only (no repo residue).

## §6. REC-W own physical measurement (the authoritative re-read)

Measured 2026-10-08 from the pinned EXE (identity verified first):

```text
E_LFANEW=0x120  MACHINE=0x014C  NSEC=5  SIZE_OF_OPTIONAL_HEADER=0xE0
OPTIONAL_MAGIC=0x010B (PE32)  IMAGE_BASE=0x00400000 (== pin)
.text  VirtualAddress=0x1000    VirtualSize=0x6735E5  SizeOfRawData=0x674000  PointerToRawData=0x1000
.rdata VirtualAddress=0x675000  VirtualSize=0xF6569   SizeOfRawData=0xF7000  PointerToRawData=0x675000
.data  VirtualAddress=0x76C000  VirtualSize=0x3D6E4   SizeOfRawData=0x34000  PointerToRawData=0x76C000
.tls   VirtualAddress=0x7AA000  VirtualSize=0xA        SizeOfRawData=0x1000   PointerToRawData=0x7A0000
.rsrc  VirtualAddress=0x7AB000  VirtualSize=0x3C54    SizeOfRawData=0x4000   PointerToRawData=0x7A1000

CALLSITE_VA = 0x006CB836   RVA=0x2CB836   .text delta=0x2CA836
PHYSICAL_OFFSET = 0x2CB836 (2930742)
BYTES = E8 75 F0 02 00
SIGNED_REL32 = +0x2F075 (192629; signed little-endian int32 of BYTES[1:5])
NEXT_VA = 0x006CB83B
TARGET_VA = 0x006CB836 + 5 + 0x2F075 = 0x006FA8B0
```

The wrong readings for contrast: bytes E8 35 F0 02 00 would give rel32
+0x2F035 and target 0x006FA870 (neither matches the physical EXE nor the
prior record); the displacement +0x2F035 with target 0x006FA8B0 is internally
inconsistent (0x006CB83B + 0x2F035 = 0x006FA870). The full occurrence census
is in SOURCE_STATE_AND_FINDINGS.md §3; the single active record is
ACTIVE_CORRECTED_PINS.json.
