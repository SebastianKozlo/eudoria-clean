# QC_REPORT — PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004

SELF_CHECK (executor self-check; explicitly NOT the independent PE-MASTER audit).
All automated gates live in `03_SCRIPTS/s5_qc_checks.py`; raw results in
`01_RAW/S5_QC_CHECKS.json`. **QC_VERDICT = QC_PASS (8/8 gates).**

| Gate | Check | Result |
|---|---|---|
| QC-1 | Complete Parameters inventory re-measured from disk: 27 files, all .vfs, 19 numeric basenames, 20006.vfs ABSENT, no subdirectories | PASS |
| QC-2 | Selected-file identity: templates.vfs 560,788 B, SHA256 BE57818C... (== pinned) | PASS |
| QC-3 | Detailed VFS count = 1 (templates.vfs only; no other VFS opened in detail) | PASS |
| QC-4 | Detailed records = 2 (RECORD_A id2=16083, RECORD_B id2=4508; no third record parsed) | PASS |
| QC-5 | NEW_FUNCTION_COUNT = 11 ≤ 20 (list below) | PASS |
| QC-6 | Record-boundary independence: header size-field framing; payload-id2 echo 5,438/5,438; ver==1 invariant 5,438/5,438; next-record framing check (id 16084 @560,284); 28-byte slack all-zero; EOF-exact (5,438 records → 560,788); prior C1 census cross-check (count + both anchor offsets/indices) | PASS |
| QC-7 | PAYLOAD_FIELD_DECODE_CHECK ([C1-corrected name and scope; formerly mislabeled "Parser raw↔decoded roundtrip" — it does NOT read the client's destination instructions]): re-reads the physical payload bytes of RECORD_A {id2=16083, A=410620, B=0, C=0, D_bits=0x3EFFBE98} and RECORD_B {id2=4508, A=296445, B=296446, C=0, D_bits=0x42F9E1CB, crc 0xAFF5797C} at fixed file offsets; RECORD_B reproduces the historical E1/E3 anchors exactly (A=296445 → getter [ECX+8]; D=124.941); consumed==28==header size both records. SCOPE LIMIT (C1): the payload→template-field DESTINATION mapping is NOT verified by this gate — it is verified by the correction package's CLIENT_DESTINATION_MAPPING_CHECK (pinned-EXE store instructions + A/B mutation falsifier) | PASS |
| QC-8 | Receiver/container byte pins: DAT_00BA1824 check @0x0043A571; new(0x18) @0x0043A57A; ctor FUN_0052A260 target; mapfind target FUN_004D1430; ADD EAX,0x14; default 0x00BA5800 (MOV EAX,0x00BA5800 starts @0x0072F5A5 — C1/P3-corrected from @0x0072F5A8); node size 0x44 @0x0072F822 (C1/P3-corrected from @0x0072F825 — the in-run script already pinned the bytes at 0x0072F822; the doc row's address was wrong); pair key store MOV [EAX],EDX @0x0072F782; both canonical copies (FUN_005670A0/FUN_0072F7A0) field-read patterns | PASS |
| QC-9 | Placement-consumer chain pins: PUSH 0x3ED3 @0x005B6597; CALL FUN_005B5F90 @0x005B659C; FUN_0043A550 @0x005B5FE8; FUN_0072F580 @0x005B5FEF; FUN_005670A0 @0x005B5FFC; builder deriver call @0x005678BA; deriver id2 reader @0x004C55B5; class-selector 0x4E26 store @0x004C54C2 (C2-corrected role label: CLASS_SELECTOR constant, not a property id); deriver lookup @0x004C55D9 (→FUN_0072F880); driver→queuepush calls @0x00567D24/@0x00567D54 (→FUN_00567B40); queuepush→constructor @0x00567C3E (→FUN_00567170); FUN_00567170 lookup @0x0056736D (→FUN_0072F580); the 5 static MOV-imm32 key sites | PASS |
| QC-10 | Negative-control disambiguation ([C1/P3-corrected to the measured scan scope; supersedes "→ no static 4508 lookup key"]): all three 0x119C (4508) imm32 hits are ESP/struct displacements (LEA ECX,[ESP+0x119C] ×2; MOV [ESI+0x119C],EBX); PUSH 0x119C sites = 0 in the performed whole-.text PUSH-imm32 scan; computed/indirect/runtime-produced 4508 keys are NOT excluded by this scan class — no absence claim beyond the measured scan is made | PASS |
| QC-11 | Forbidden-overclaim census in FINAL_REPORT (WORLD_XYZ_RECOVERED=NO, MODEL_JOIN_EXECUTED=NO, NETWORK_PLACEMENT_PROVEN=NO, STATIC_INSTANCE_CONFIRMED=NOT_ESTABLISHED, POSITION_RECOVERY_GOAL=OUT_OF_SCOPE, F3/F4/F1F2/RUNTIME all NO) | PASS |

## NEW_FUNCTION_COUNT = 11 (materially analyzed in detail this run)

FUN_005670A0, FUN_0072F7A0, FUN_0072F740, FUN_0072F7F0, FUN_0072F880, FUN_0072FCE0,
FUN_004C5480, FUN_00703B80, FUN_005B6370, FUN_00567B40, FUN_00567170.

Previously-established functions revisited NARROWLY (old claim cited, bytes/call edge
rechecked, no materially new semantics — not counted): FUN_0072FA30 (reader head/loop),
FUN_00971AD0, FUN_00730C90 (parse — confirmed the E1 layout by independent decode),
FUN_0072F8D0, FUN_0043A550, FUN_0072F580, FUN_004D1430 (via windows), FUN_004C5580,
FUN_00567770, FUN_00567C50, FUN_005B5F90, FUN_007CE1E0/FUN_00746550/FUN_006B22D0/
FUN_0048ADA0, FUN_00730F90/FB0, FUN_00730700, FUN_004123D0, FUN_00844020, FUN_00843DD0,
FUN_004148F0/FUN_00457930, FUN_00567030, FUN_00730B70/FUN_00730970 (destinations only).

## ANTI-CIRCULARITY statements (per positive claim)

1. Claim "RECORD_A is parsed into {id2, A, B, C, D_f32, lists, f11}": MEASURED = raw
   payload bytes re-read at fixed file offsets (PAYLOAD_FIELD_DECODE_CHECK); INDEPENDENT SOURCE =
   the pinned EXE instruction windows + the historical anchors for RECORD_B (A=296445
   at +0x08 matches the E3 getter anchor). [C1-corrected FAILURE_CASE — supersedes the
   prior "a wrong destination pairing would have broken the RECORD_B anchor match
   (detected by QC-7 if so)", which was FALSE: the independent Desktop post-audit
   proved that a deliberate A/B destination-documentation swap still passes QC-7
   (QC_COUNTEREXAMPLE_SUMMARY.json), because QC-7 never reads the destination
   instructions.] The payload→destination mapping is now guarded by the correction
   package's CLIENT_DESTINATION_MAPPING_CHECK, whose A/B mutation falsifier FAILS on
   the swapped documentation mapping (both the Desktop-style destination-only swap
   and a fully self-consistent swap) while the raw VFS values stay unchanged.
2. Claim "the record is inserted into the registry at DAT_00BA1824": MEASURED = the
   reader-loop byte window (FUN_004123D0 key read, FUN_005670A0 pair-value copy,
   FUN_0072F8D0 insert — the sole call site); INDEPENDENT = the prior E1 pin + the
   5,438/5,438 walk agreement; FAILURE_CASE = a second insert caller or a different
   root would have shown in the census (none).
3. Claim "RECORD_A's object is read back with static key 0x3ED3": MEASURED = the
   byte-pinned PUSH/CALL chain in FUN_005B6370/FUN_005B5F90; INDEPENDENT = the key
   value equals the record's id2 measured from the FILE, not from the code;
   FAILURE_CASE = if the key did not exist as a record id2, the chain would be
   key-orphaned (the file-side existence check is the discriminator; QC-4/6 cover it).
4. Claim "the named builder reads the same registry with a runtime key": MEASURED =
   the FUN_004C5580→FUN_004C5480→FUN_0072F880 byte chain; INDEPENDENT = the
   class-selector 0x4E26 store instruction + the class-selector-resolve
   (FUN_00703B80 @0x004C54CE) and property-tag-6-getter (PUSH 6 @0x004C551F →
   FUN_0070C180 @0x004C5523) call targets ([C2-corrected layering: CLASS_SELECTOR
   0x4E26=20006 vs PROPERTY_TAG 6 — see PLACEMENT_CONSUMER_EDGE.md]); the KEY VALUE is
   explicitly classified runtime-dependent (NOT statically provable) — the honest
   boundary of this claim.

## Deviations / process notes

1. RESUMED RUN: the previous session's final return arrived empty at PE-MASTER; the
   disk state was partial (Phase A + raw windows only). This session continued from
   that state per the parent's resume order; Phase A was re-verified (not redone).
2. Three s5 QC-check expressions were corrected in-run after first failing due to the
   check's own arithmetic (read-length 22 vs the 24-char string; two check sites at
   wrong sub-offsets). The underlying evidence pins were never wrong; the corrections
   are in the script history of this package.
3. RECORD_A payload hex was machine-measured twice (s4 + QC) after a hand-transcription
   error was caught by the QC-7 gate — the machine-measured values are authoritative.
4. The 0x3ED3/0x3ED2 occurrences at 0x0050F383/0x0050F2F3 are documented
   RAW_OCCURRENCE_ONLY (property-idiom sites; no consumer role claimed without
   parser proof, per the contract's blind-byte-search rule).
5. FUN_0050A690's ECX provenance in FUN_005B5F90's post-registration path is
   stack-state-dependent and left UNRESOLVED (non-load-bearing for Phase F).
6. No original file was modified; all corpus reads were read-only; no runtime
   execution; no client launch; Ghidra not used (raw byte reads + manual decode only).
7. [C1/C2/P3 correction of record, 2026-10-04 — see the supersession ledger in
   PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_C1_REPORT_QC_CORRECTION_R1_20261004]:
   QC-7's declared scope was narrowed to PAYLOAD_FIELD_DECODE_CHECK (the destination
   mapping was never verified by it — Desktop counterexample); the FUN_00730C90
   failure-path description was corrected (ZERO-WRITE on failed flag/bounds reads,
   not a same-value slow path); the FUN_00730C90/FUN_0072F580/FUN_0072F7F0/FUN_004C5480
   instruction starts were corrected (see PARSER_CHAIN.md/RECORD_A.md/
   RECEIVER_INSERTION_CHAIN.md/PLACEMENT_CONSUMER_EDGE.md); the "0x4E26-property" wording
   was replaced by the CLASS_SELECTOR-20006 / PROPERTY_TAG-6 layered identity; the
   4508 negative was reworded to the measured scan scope; the proprietary-byte census
   was reworded (bounded original byte windows/payload excerpts present; no complete
   original files). The R1 raw JSON evidence (01_RAW/S5_QC_CHECKS.json etc.) is the
   historical measurement record and was NOT altered.
