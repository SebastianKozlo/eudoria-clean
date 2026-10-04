# QC_TARGETED_REPORT — PE_935_PARAMETER_RECORD_C1_C1_STORE_IDENTITY_QC_R1_20261004

SELF_CHECK (executor self-check; explicitly NOT the independent PE-MASTER
audit). QC_SCOPE = SELF_CHECK_C1_C1_STORE_IDENTITY. Instrument:
`03_SCRIPTS/qc_targeted_c1c1.py` (modes base_repro | normal | battery | oracle);
raw records in `01_RAW/`. All reads STATIC-ONLY (no client launch, no runtime
execution, no network, no Ghidra). READ-ONLY vs Entropia.exe, templates.vfs,
every canonical repo file, and the historical C1-correction package (whose
verifier was imported read-only for the BASE reproduction).

## Corrected full QC on the canonical document — QC_VERDICT = QC_PASS (10/10)

| Gate | Check | Result |
|---|---|---|
| TQ0 | Corpus identities: EXE SHA E7785430... (8,015,872 B), templates.vfs SHA BE57818C... (560,788 B) — both == pins | PASS |
| TQ1 | PAYLOAD_FIELD_DECODE_CHECK: RECORD_A {id2=16083, A=410620, B=0, C=0, D_bits=0x3EFFBE98} + RECORD_B {id2=4508, A=296445, B=296446, C=0, D_bits=0x42F9E1CB} at fixed file offsets; payload + window SHA256s == pins; values UNCHANGED | PASS |
| TQ2 | CLIENT_DESTINATION_MAPPING_CHECK — CORRECTED: three simultaneous identities (payload field identity → store instruction identity → destination field identity) per row against the HARD-CODED, byte-backed parser-sequence oracle; completeness (exactly one row per expected payload index, no unexpected payload rows, D row present); PAYLOAD_INDEX_STORE_IDENTITY_CHECK sub-gate | PASS (identity PASS; mapping PASS) |
| TQ3 | CLASS_SELECTOR 0x4E26=20006 (pair constant store @0x004C54C2; resolver CALL FUN_00843DD0 @0x004C54B2; wrapper CALL FUN_00703B80 @0x004C54CE) vs PROPERTY_TAG 6 (receiver MOV ECX,[EAX+4] @0x004C551C; PUSH 6 @0x004C551F; CALL FUN_0070C180 @0x004C5523); docs layered wording | PASS |
| TQ4 | Receiver provenance: FUN_00452490 wrapper (CALL FUN_0043A550 @0x00452490; MOV ECX,EAX @0x00452495; tail JMP FUN_0072FA30 @0x00452497); loader ECX preserve @0x0072FA6B / recover @0x0072FBD4; insert CALL FUN_0072F8D0 @0x0072FBE5; 0 singleton call sites in the loader extent | PASS |
| TQ5 | FUN_00730C90 failure-path ZERO-WRITE pins (XOR EBX,EBX @0x00730C96; zero stores @0x00730CC3/CF0/D1E/D4C; FLDZ @0x00730D7A + FSTP @0x00730D7C) + FUN_0040DE60 advance/flag-zero; PARSER_CHAIN retraction-quote discipline | PASS |
| TQ6 | Instruction-start corrections: negative controls (old addresses @0x00730D16/@0x00730D36/@0x00730D6D/@0x0072F5A8/@0x0072F825/@0x004C54AD must NOT hold the claimed bytes) + positive controls (@0x00730D14/@0x00730D42/@0x00730D69/@0x00730D70/@0x0072F5A5/@0x0072F822/@0x004C54B2) | PASS |
| TQ7 | Next-experiment wording (SPECIFIC RUNTIME VALUE; class-selector-20006/property-tag-6; OPEN taxonomy; no active overbroad writers claims) intact in FINAL_REPORT/HANDOFF/PLACEMENT_CONSUMER_EDGE | PASS |
| TQ8 | S1 canonical facts preserved (PARSER_TO_RUNTIME_VALUE_SEAM=CONFIRMED; CONTAINER_ROLE=DEFINITION_REGISTRY; RECORD_A/B values; PUSH 0x3ED3 @0x005B6597 + the four call targets; PLACEMENT_CONSUMER_EDGE=STRONGLY_SUPPORTED) | PASS |
| TQ9 | Forbidden overclaims absent (PHYSICAL_RECORD_TO_PLACEMENT_ATTRIBUTE / WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED=NO; proprietary + 4508 scan wordings) | PASS |

Full-QC verdict algebra: QC_VERDICT = QC_PASS iff ALL TQ gates pass — the
FULL_QC FAILS whenever TQ2 (the mapping check) fails (demonstrated per case in
the battery below).

## BASE defect reproduction (01_RAW/BASE_MUTANT_C_REPRODUCTION.json)

Historical verifier imported READ-ONLY (SHA256 CB4587C1...). Private document
copies only; EXE/VFS/canonical docs unchanged.

| Step | Result |
|---|---|
| BASE canonical QC (pristine state) | QC_PASS 10/10 (TQ1 PASS; TQ2 PASS) |
| BASE A/B mutation falsifier | AB_MAPPING_MUTATION_FALSIFIER = DETECTED (A: detected; B: detected) |
| BASE mutant C (document SHA 7C0809CD...) | PAYLOAD_FIELD_DECODE_CHECK=PASS; CLIENT_DESTINATION_MAPPING_CHECK=**PASS (the FALSE PASS)**; FULL_QC=**QC_PASS (the FALSE PASS)**; all 5 historical row verdicts `dest_eq_disp=True`, `bytes_match=True`, `pass=True` |

BASE_MUTANT_C_FALSE_PASS_REPRODUCED = **YES** (the C1-C1/P2 defect exists in
the published verifier exactly as described by Desktop).

## POST-FIX mutation battery (01_RAW/QC_MUTATION_BATTERY_POST_FIX.json)

Every case: PRIVATE copy of the 8 tested documents with only PARSER_CHAIN.md
mutated; corrected FULL QC re-run per case; raw VFS values unchanged
(PAYLOAD_FIELD_DECODE_CHECK=PASS in every case).

| Case | Document SHA256 | PAYLOAD_FIELD_DECODE | PAYLOAD_INDEX_STORE_IDENTITY | CLIENT_DESTINATION_MAPPING | FULL_QC | Detected | Expected |
|---|---|---|---|---|---|---|---|
| canonical copy (negative control — a correct field-index/name/VA/destination tuple must pass) | 6BA91A1F... (byte-identical to canonical) | PASS | PASS | PASS | QC_PASS | n/a | PASS ✓ |
| mutant A (destination-cell-only swap — Desktop replica) | 0AEC1DB4... | PASS | **FAIL** | **FAIL** | **QC_FAIL** | **YES** | FAIL ✓ |
| mutant B (destination+displacement swap, old VAs) | 2901BD57... | PASS | **FAIL** | **FAIL** | **QC_FAIL** | **YES** | FAIL ✓ |
| mutant C (destination+displacement+MATCHING REAL STORE VA swap — each row at the OTHER field's real store) | 7C0809CD... | PASS | **FAIL** | **FAIL** | **QC_FAIL** | **YES** | FAIL ✓ |

Per-row reasons recorded (oracle-grounded), e.g. mutant C payload[1]:
"STORE INSTRUCTION IDENTITY FAIL: documented store VA 0x00730D14 is the store
of payload[2] (B) per the independent parser-sequence oracle, NOT the store of
payload[1] (A) (oracle assigns payload[1] (A) store VA 0x00730CE6, bytes
89 47 08)"; plus destination-identity and displacement reasons (full list in
the battery JSON).

MUTANT_A_DETECTED = YES; MUTANT_B_DETECTED = YES; MUTANT_C_POST_FIX_DETECTED =
YES; canonical negative control PASS; battery_pass = true.

## ANTI-CIRCULARITY (per positive claim — the corrected TQ2)

1. Claim "the documented destination table binds payload field identity → the
   exact store instruction → the destination": MEASURED = the parsed document
   rows (idx/name/dest/disp/VA) compared against the ORACLE; INDEPENDENT SOURCE
   = the pinned Entropia.exe bytes (SHA-pinned, byte-verified at runtime) + the
   independently fixed normal parser instruction order of FUN_00730C90
   (hard-coded in the instrument BEFORE the document is read; store VAs
   strictly increase with payload index; per-field read→store adjacency
   byte-pinned); FAILURE_CASE = Desktop mutant C — the document row pointed at
   the OTHER field's real store with matching displacement: the BASE verifier
   PASSED it (reproduced), the corrected gate FAILS it (battery). The document
   under test cannot supply the mapping.
2. Claim "the BASE verifier has the C1-C1 defect": MEASURED = the pristine
   historical verifier imported read-only (SHA CB4587C1...) run against a
   private mutant C document copy; INDEPENDENT = the BASE canonical QC_PASS
   10/10 + BASE A/B falsifier DETECTED controls measured in the same session
   prove the verifier was the unmodified published one; FAILURE_CASE = a false
   PASS would have shown as TQ2 FAIL on BASE (it did not — the false PASS is
   the defect, recorded verbatim).
3. Claim "the corrected gate detects the A/B/C classes while passing the
   canonical table": MEASURED = the four-case battery with byte-identical
   document control (canonical copy SHA == canonical disk SHA proves the
   private-copy pipeline is content-neutral); FAILURE_CASE = any battery case
   with the wrong verdict (none; every case matched its expected verdict).

## Deviations / process notes

1. Honest instrument iteration BEFORE the final records: the first
   private-copy executions wrote mutated documents with CRLF normalization
   (Windows text mode), making document SHAs not directly comparable to the
   LF-ending canonical file. The instrument was corrected to preserve LF
   (`newline="\n"`) and ALL modes were re-run; the published records are the
   corrected executions (canonical private copy now byte-identical:
   6BA91A1F...; the BASE-reproduction and battery mutant C documents are
   byte-identical: 7C0809CD...). No verifier logic changed between the
   executions; all verdicts were identical in both.
2. No original file was modified; all corpus reads were read-only; no runtime
   execution; no client launch; no Ghidra; no network. The historical
   C1-correction package was imported read-only for the BASE reproduction and
   left byte-identical (verified: no `__pycache__`, `git status` clean of
   tracked modifications).
3. Additional closed class recorded as an oracle property (NOT a battery case,
   per the bounded contract): the D-store FSTP [EDI+0x10] (D9 5F 10) has a
   byte-identical twin at the zero-path site 0x00730D7C — a document row
   pointing the D store at 0x00730D7C would also have passed the BASE
   verifier; only the VA identity of the corrected oracle rejects it.
