# FIXTURES — PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007

Every fixture of this correction is a BYTE CONSTANT pinned to a published record.
ZERO EXE access of any kind is performed (NEW_PCG_FUNCTION_BODIES_ALLOWED = 0;
NEW_SCIENCE_EDGE_INTERPRETATIONS_ALLOWED = 0). All mutants are SYNTHETIC / IN-MEMORY
ONLY — no mutation is ever written to any file outside this package's own outputs.

## F1. CLEAN_GETTER_FIXTURE (CTRL_3 clean case)

```text
8B 41 68 C3 CC CC CC CC
```

- Semantics: `mov eax, [ecx+0x68]; ret` + int3 padding.
- Provenance (persisted prior pin): SOURCE_PACKAGE 01_RAW/FUN_006C66D0_GETTER_FULL.txt,
  RAW BYTES line — the first 8 bytes of the 96-byte window @0x006C66D0
  ("8B 41 68 C3 CC CC CC CC 56 8B 74 24 08 …").
- Budget status: body #1 of the source run — ALREADY budgeted and opened there; using
  its persisted bytes as an in-memory constant is NOT a new probe.

## F2. FOREIGN_ACCESSOR_FIXTURE (CTRL_3 mutated case)

```text
8B 81 20 01 00 00 C3 CC
```

- Semantics: `mov eax, [ecx+0x120]; ret` + int3.
- Provenance (persisted recorded constant of the HISTORICAL probe): the bytes were read
  from the real EXE at FUN_006C0EE0 (8-byte read) by the source run's CTRL_3 mutated
  case and are recorded in SOURCE_PACKAGE CONTROL_RESULTS.json (CTRL_3 mutated_case
  detail: "accessor 'mov eax, [ecx+0x120]'") and in Desktop CONTROL_COUNTERCHECKS.json
  (foreign_accessor_bytes / foreign_accessor_decode).
- Budget status: the HISTORICAL probe is the proven undeclared 7th real-body opening —
  retroactively ACCOUNTED in FUNCTION_BODY_ACCOUNTING.csv row 7
  (MINIMUM_NEW_FUNCTION_BODIES_OPENED >= 7; ORIGINAL_FUNCTION_BODY_BUDGET_COMPLIANCE =
  FAIL). THIS correction re-reads nothing: the bytes are used only as a recorded
  constant (no new real EXE accessor discovery).

## F3. JOIN_WINDOW_CLEAN_BUFFER (CTRL_4 clean case)

The 0x42 (66) bytes of WINDOW 0x0050A3B7..0x0050A3F8, rebuilt from the per-instruction
byte column of SOURCE_PACKAGE 01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt (a free re-pin of the
prior source run's record; the window record is the byte source — no EXE read here):

```text
8B F8  E8 D2 6B 1B 00  84 C0  74 06  83 4E 2C 02  EB 04
83 66 2C FD  8B 4E 20  E8 DC 6C 1B 00  8B CE  50  57
E8 03 FE FF FF  8B 8E 8C 00 00 00  56  E8 F7 A2 01 00
8B 4E 30  8B 01  8B 90 A4 00 00 00  6A 00  57  FF D2
```

Instruction map (22 instructions; decode boundaries verified contiguously from
0x0050A3B7; total 0x42):

| VA | bytes | instruction |
|---|---|---|
| 0x0050A3B7 | 8B F8 | mov edi, eax (THE HEAD) |
| 0x0050A3B9 | E8 D2 6B 1B 00 | call 0x006C0F90 (intervening #1) |
| 0x0050A3BE | 84 C0 | test al, al |
| 0x0050A3C0 | 74 06 | je 0x0050A3C8 |
| 0x0050A3C2 | 83 4E 2C 02 | or dword ptr [esi+0x2C], 2 |
| 0x0050A3C6 | EB 04 | jmp 0x0050A3CC |
| 0x0050A3C8 | 83 66 2C FD | and dword ptr [esi+0x2C], 0xFFFFFFFD |
| 0x0050A3CC | 8B 4E 20 | mov ecx, dword ptr [esi+0x20] |
| 0x0050A3CF | E8 DC 6C 1B 00 | call 0x006C10B0 (intervening #2) |
| 0x0050A3D4 | 8B CE | mov ecx, esi |
| 0x0050A3D6 | 50 | push eax |
| 0x0050A3D7 | 57 | push edi (EARLIER push — NOT the final site) |
| 0x0050A3D8 | E8 03 FE FF FF | call 0x0050A1E0 (intervening #3) |
| 0x0050A3DD | 8B 8E 8C 00 00 00 | mov ecx, dword ptr [esi+0x8C] |
| 0x0050A3E3 | 56 | push esi |
| 0x0050A3E4 | E8 F7 A2 01 00 | call 0x005246E0 (intervening #4) |
| 0x0050A3E9 | 8B 4E 30 | mov ecx, dword ptr [esi+0x30] |
| 0x0050A3EC | 8B 01 | mov eax, dword ptr [ecx] |
| 0x0050A3EE | 8B 90 A4 00 00 00 | mov edx, dword ptr [eax+0xA4] (NiNode vtable slot 41) |
| 0x0050A3F4 | 6A 00 | push 0 |
| 0x0050A3F6 | 57 | push edi (THE EXACT FINAL JOIN CHILD ARGUMENT) |
| 0x0050A3F7 | FF D2 | call edx (THE EXACT JOIN CALL ENDPOINT) |

Arithmetic re-verification (this correction): call rel32 targets — 0x0050A3BE +
0x001B6BD2 = 0x006C0F90; 0x0050A3D4 + 0x001B6CDC = 0x006C10B0; 0x0050A3DD + (-0x1FD) =
0x0050A1E0; 0x0050A3E9 + 0x0001A2F7 = 0x005246E0; rel8 targets — 0x0050A3C2 + 6 =
0x0050A3C8; 0x0050A3C8 + 4 = 0x0050A3CC; total length 0x0050A3F9 − 0x0050A3B7 = 0x42.

## F4. CTRL_4 mutants (all SYNTHETIC / IN-MEMORY ONLY)

- F4a historical EDI-clobber mutant: offset 0x26 (VA 0x0050A3DD), 6 bytes replaced with
  `8B 3D D0 D8 B9 00` (mov edi, dword ptr [0xB9D8D0]) — same 6-byte length as the original
  `8B 8E 8C 00 00 00`, so all decode boundaries stay intact. This is the historical
  synthetic clobber case of the source run's CTRL_4 (CONTROL_RESULTS.json CTRL_4
  mutated_case).
- F4b final-push-ESI mutant: byte at offset 0x3F (VA 0x0050A3F6) 57 -> 56
  (push edi -> push esi). The earlier push edi @0x0050A3D7 survives — exactly the
  Desktop's wrong_final_push_ESI case.
- F4c final-push-NOP mutant: byte at offset 0x3F (VA 0x0050A3F6) 57 -> 90
  (push edi -> nop). The earlier push edi @0x0050A3D7 survives — exactly the Desktop's
  missing_final_push_NOP case.

None of F4a/F4b/F4c is written anywhere; each exists only as an in-memory bytearray in
03_SCRIPTS/ctrl4_exact_endpoint.py (make_clobber_mutant / make_final_arg_mutant).

## F5. QC fixtures

- The corrected-ledger adjudication inputs are the SOURCE package's records themselves
  (READ-ONLY reads): EDGE_ACCOUNTING_LEDGER.csv, CONTROL_RESULTS.json,
  01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt, the scripts of 03_SCRIPTS/ and
  00_CONTROL_INTERNAL_QC/ (for the probe scan), and the three Desktop post-audit inputs
  (re-hashed, identities pinned in INPUT_IDENTITIES.md §3).
- No other byte source exists in this correction. Scratch work stays outside the repo.
