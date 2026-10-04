# QC_TARGETED_REPORT — PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_C1_REPORT_QC_CORRECTION_R1_20261004

**QC_SCOPE = SELF_CHECK_REPORT_QC_HANDOFF_CORRECTION** (executor self-check of the
corrected report/QC/handoff wording and its byte evidence; explicitly NOT an
independent PE-MASTER audit). Instrument: `03_SCRIPTS/qc_targeted.py` (read-only vs
the pinned EXE/templates.vfs and every canonical repo doc; sys.dont_write_bytecode;
no client launch). Raw records: `01_RAW/QC_TARGETED.json` (normal),
`01_RAW/QC_MUTATION_AB_SWAP.json` (mutation falsifier), `01_RAW/EXE_BYTE_PROOFS.json`
(bounded instruction windows).

**QC_VERDICT = QC_PASS (10/10 checks). AB_MAPPING_MUTATION_FALSIFIER = DETECTED.**

| # | Check (terminal-field mapping) | Result |
|---|---|---|
| TQ0 | Corpus identities re-hashed: Entropia.exe 8,015,872 B SHA E7785430... (== pinned); templates.vfs 560,788 B SHA BE57818C... (== pinned) | PASS |
| TQ1 | PAYLOAD_FIELD_DECODE_CHECK: correct payload values UNCHANGED — RECORD_A {id2=16083, A=410620, B=0, C=0, D_bits=1056947864, list1=0, list2=0, f11=0} payload SHA 9E22B8AF..., window SHA 1987B5C4...; RECORD_B {id2=4508, A=296445, B=296446, C=0, D_bits=1123672523} payload SHA 890A50E5..., window SHA 4345305B...; both == the R1 S4 anchors byte-for-byte | PASS |
| TQ2 | CLIENT_DESTINATION_MAPPING_CHECK: parses the corrected PARSER_CHAIN.md destination table and byte-verifies EVERY documented destination against the pinned-EXE store instruction — payload[0]→+0x00 (89 07 @0x00730CB6); payload[1]→+0x08 (89 47 08 @0x00730CE6); payload[2]→+0x04 (89 47 04 @0x00730D14); payload[3]→+0x0C (89 47 0C @0x00730D42); payload[4]→+0x10 (FLD D9 04 10 @0x00730D69 + FSTP D9 5F 10 @0x00730D70); each row's documented destination == instruction displacement AND the physical bytes match; 4/4 u32 rows + D row parsed | PASS |
| TQ3 | CLASS_SELECTOR_20006 vs PROPERTY_TAG_6 distinct: resolver CALL FUN_00843DD0 starts @0x004C54B2 (E8 19 E9 37 00); CLASS_SELECTOR pair constant MOV [ESP+0x1C],0x4E26 @0x004C54C2 (C7 44 24 1C 26 4E 00 00; 0x4E26==20006); wrapper CALL FUN_00703B80 @0x004C54CE (rel32 → 0x00703B80); exact receiver MOV ECX,[EAX+4] @0x004C551C (8B 48 04); PROPERTY_TAG PUSH 6 @0x004C551F (6A 06); tag-6 getter CALL FUN_0070C180 @0x004C5523 (rel32 → 0x0070C180); 6≠20006, 6≠0x4E26, sites distinct; corrected docs carry the layered wording in all four files | PASS |
| TQ4 | RECEIVER_PROVENANCE: wrapper FUN_00452490 CALL FUN_0043A550 @0x00452490 (rel32 → 0x0043A550); MOV ECX,EAX @0x00452495 (8B C8); tail JMP FUN_0072FA30 @0x00452497 (E9 → 0x0072FA30); loader PRESERVES incoming ECX MOV [ESP+0x38],ECX @0x0072FA6B (89 4C 24 38 — byte-verified; the Desktop's @0x0072FA6C is the ModRM byte); recovers MOV ECX,[ESP+0x3C] @0x0072FBD4 (8B 4C 24 3C); insert CALL FUN_0072F8D0 @0x0072FBE5 (rel32 → 0x0072F8D0); bounded extent scan 0x0072FA30..0x0072FCA0: ZERO FUN_0043A550 call sites inside the loader (the loader does NOT itself call the singleton); corrected wording present, old claim only in retraction quote | PASS |
| TQ5 | PARSER_FAILURE_PATH (ZERO-WRITE) wording + bytes: XOR EBX,EBX @0x00730C96 (EBX=0 source); MOV [EDI],EBX @0x00730CC3 (89 1F); MOV [EDI+8],EBX @0x00730CF0 (89 5F 08); MOV [EDI+4],EBX @0x00730D1E (89 5F 04); MOV [EDI+0xC],EBX @0x00730D4C (89 5F 0C); D zero via FLDZ @0x00730D7A (D9 EE) + FSTP [EDI+0x10] @0x00730D7C (D9 5F 10); FUN_0040DE60: ADD [ECX+0xC],EAX @0x0040DE64 + CMP EAX,[ECX+8] @0x0040DE6A + JBE +4 @0x0040DE6D + MOV BYTE [ECX+0x11],0 @0x0040DE6F (flag zeroed on limit exceed); docs document the zero-write behavior; the retired "stores the same value" claim survives ONLY inside the retraction quote (0 active-claim occurrences) | PASS |
| TQ6 | INSTRUCTION_ADDRESS_CORRECTIONS: positive controls — B store 89 47 04 @0x00730D14, C store 89 47 0C @0x00730D42, FLD D9 04 10 @0x00730D69, FSTP D9 5F 10 @0x00730D70, MOV EAX,0x00BA5800 B8 00 58 BA 00 @0x0072F5A5, node-size C7 45 EC 44 00 00 00 @0x0072F822, resolver E8 19 E9 37 00 @0x004C54B2 — all match; negative controls — the OLD wrong addresses @0x00730D16/@0x00730D36/@0x00730D6D/@0x0072F5A8/@0x0072F825/@0x004C54AD do NOT contain the claimed instruction bytes (operand bytes, never instruction addresses) | PASS |
| TQ7 | NEXT_EXPERIMENT_IDENTITY = SPECIFIC_GETTER_RESULT_PROVENANCE: all three corrected docs (FINAL_REPORT.md, HANDOFF.md, PLACEMENT_CONSUMER_EDGE.md) reference the SPECIFIC RUNTIME VALUE returned by the class-selector-20006 / property-tag-6 getter with the OPEN taxonomy PHYSICAL_RECORD_DERIVED \| CONSTANT_INITIALIZATION \| LOCAL_COMPUTED \| CACHE_PROVIDER \| MESSAGE_DERIVED \| FALLBACK_BRANCH \| UNKNOWN; the overbroad "Decode the WRITERS of the 0x4E26" wording survives only in retraction quotes (0 active claims) | PASS |
| TQ8 | Previously confirmed S1 facts PRESERVED (no regression): PARSER_TO_RUNTIME_VALUE_SEAM = CONFIRMED; CONTAINER_ROLE = DEFINITION_REGISTRY; RECORD_A values; RECORD_B values; Chain-1 static key byte-pinned from the EXE (PUSH 0x3ED3 = 68 D3 3E 00 00 @0x005B6597; CALL → FUN_005B5F90 @0x005B659C; FUN_0043A550 @0x005B5FE8; FUN_0072F580 @0x005B5FEF; FUN_005670A0 @0x005B5FFC); PLACEMENT_CONSUMER_EDGE = STRONGLY_SUPPORTED unchanged | PASS |
| TQ9 | Forbidden overclaims ABSENT / no upgrades: PHYSICAL_RECORD_TO_PLACEMENT_ATTRIBUTE = NOT_ESTABLISHED; WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO; named-builder key still "NOT statically provable"; proprietary census corrected ("no complete original proprietary" FILES; bounded excerpts present); 4508 scan measured-scope wording present; RECORD_A/B values unchanged (== TQ1) | PASS |

## A/B mapping mutation falsifier (negative control; 01_RAW/QC_MUTATION_AB_SWAP.json)

Design: the corrected PARSER_CHAIN.md is copied to a private temp file, the
documented A/B destination mapping is intentionally swapped, and the SAME
CLIENT_DESTINATION_MAPPING_CHECK verifier runs against the UNCHANGED pinned EXE and
UNCHANGED templates.vfs. The check must FAIL for both mutants. This reproduces and
closes the Desktop QC-7 counterexample class (a deliberate A/B documentation swap
passed the published QC-7 with byte-identical PASS output).

| Mutant | Mutation | Raw VFS values | Destination check | Falsifier |
|---|---|---|---|---|
| A — Desktop replica (`qc_counterexample.py` reproduction) | destination cells only: payload[1]→template+0x04, payload[2]→template+0x08 | UNCHANGED (TQ1 PASS) | **FAIL** (rows payload[1] (A), payload[2] (B)) | DETECTED |
| B — fully self-consistent swap | destination cells AND instruction displacement text swapped (internally consistent doc) | UNCHANGED (TQ1 PASS) | **FAIL** (rows payload[1] (A), payload[2] (B) — the physical EXE bytes 89 47 08 @0x00730CE6 / 89 47 04 @0x00730D14 contradict the swapped documentation) | DETECTED |

**AB_MAPPING_MUTATION_FALSIFIER = DETECTED** (both mutants detected; canonical repo
files untouched — mutants lived in a temp copy, removed after the run; the exact
mutated rows are recorded in 01_RAW/QC_MUTATION_AB_SWAP.json).

## Process notes (honest record)

1. Three QC-check EXPRESSIONS were corrected in-run after first failing through the
   check's own arithmetic (the same class as the R1 QC_REPORT deviation note 2):
   (a) TQ5's `all()` included an integer occurrence count that is falsy at 0 — the
   count is now checked explicitly; (b) TQ7's taxonomy string did not match the
   line-wrapped doc text — whitespace is now normalized on both sides; (c) TQ8
   looked for RECORD_B's A/B values in FINAL_REPORT.md where they are canonically
   pinned in RECORD_B.md (FINAL_REPORT pins the id; the physical values are
   re-verified by TQ1). No underlying evidence pin was ever wrong; every byte pin
   passed on the first execution.
2. One retired-claim residue scanner fix: the retired "stores the same value"
   sentence is line-wrapped inside the retraction quote, so the scanner now searches
   the full text with `\s+` between tokens (line attribution preserved).
3. No original file was modified; all corpus reads read-only; no runtime execution;
   no client launch; no Ghidra; no new VFS; no third record; no RECORD_A/B value
   change; no placement science.
