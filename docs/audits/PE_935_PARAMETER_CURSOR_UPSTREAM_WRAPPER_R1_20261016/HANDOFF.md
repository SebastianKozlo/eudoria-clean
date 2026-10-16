# HANDOFF — PE_935_PARAMETER_CURSOR_UPSTREAM_WRAPPER_R1_20261016

generated_utc = 2026-10-16T14:30:50.085131+00:00
time_provenance = measured by the t00_write_doc.py serializer at the moment of writing this prepared content

## Terminals (separate layers)

- RUN_STATUS = **PARTIAL** (process: error-correction rounds 2/2 exhausted -> controls needed both rounds; OPEN finding F1 CRLF write translation; science content unaffected)
- SCIENCE_RESULT = **WRAPPER_CURSOR_RELAY_CONFIRMED_CONDITIONAL_ON_DECLARED_MODELS**
- EVIDENCE_STATUS = **CONFIRMED** (scoped to the 82-B window, conditional on the declared entry + ABI models; unconditional byte facts listed in EVIDENCE.json)
- QC_ORIGIN = **SELF_REVIEW_WITH_LIMITATIONS**; QC verdict QC_PARTIAL; EXTERNAL_POSTAUDIT_OF_THIS_RUN = PENDING

## One-line science answer

FUN_00852A30 RELAYS its incoming cursor C (the single stack argument at [entryESP+4], ESI @0x00852A32) and its own entry receiver O (entry ECX -> EDI @0x00852A3E) to FUN_00852750 by a direct CALL rel32 @0x00852A77 -> 0x00852750 (PUSH ESI @0x00852A74; MOV ECX,EDI @0x00852A75), admitted by the exact local byte gate **B == 1** (MOVZX/SUB 1/JE @0x00852A64..0x00852A6A) after a u8 read from [C.data + C.offset] under valid/size guards and one opaque helper CALL 0x0040DE60 (receiver C, arg 1; actual advance effects NOT_ESTABLISHED). Both value identities cross that ONE opaque CALL -> CONDITIONAL_ON_ABI_MODEL; no in-window construction/fill of the cursor (only [C+0x11]:=0 on the size-fail path, which never reaches the transfer).

## Evidence pointers

- Final report: REPORT.md (full analysis, budgets, findings, standing)
- Roster: decode/INSTRUCTION_ROSTER.json (37 rows, A/B full agreement 37/37 + 7/7 targets)
- Provenance: EVIDENCE.json (8 rows, symbols separately typed, models, variants)
- Controls: controls/v3/CONTROL_SUMMARY.json (4/4 CONTROL_PASS; v1/v2 preserved with their failure records)
- Records: records/pe32_mapping.json, records/SOURCE_UNCHANGED.json, records/JSON_VALIDATION.json, records/STANDING_CHECK.json
- Budgets: BUDGET_USED.json (original EXE bytes exactly at the 16036004 maximum; rounds 2/2 binding)
- Ledger: ATTEMPT_LOG.jsonl (append-only; every line carries its pre-append prefix size+sha)

## Process honesty (must be carried forward)

1. F1 (P2, OPEN): Windows CRT text-mode write defect in run_common.atomic_write_bytes (os.open without O_BINARY) — CRLF translation on disk for every artifact written through it; the PE header buffer is 4099 B on disk (3 inserted bytes) with PROVEN recoverable logical content (replace \r\n with \n -> 4096 B, SHA256 636B01A25A9DE410781805D67AE1149FA64DF3D26C5C4FDE7D2D9EBCABC5A5C0 == the identity recorded at write time); window buffers unaffected; manifest = binding disk identity layer, ledger outputs = logical identity layer.
2. F2 (P2, OPEN): repair rounds 2/2 exhausted (round 1 = t08 v1 child-argv; round 2 = v2 claims-wrapper); both defective versions + outputs preserved; v3 passes; no false PASS ever occurred.
3. The predecessor (PARAMETER_RECORD_INGRESS_R1) terminal PARTIAL and its findings are history — not repaired, not PASS.

## FIRST_MISSING_EDGE (proposal, NOT executed)

Who supplies C to FUN_00852A30 (the wrapper's caller) and where that cursor buffer is constructed/filled — the next upstream edge; requires a separately authorized bounded run (caller census is currently prohibited). NEXT_EXPERIMENT_AUTHORIZED = NO. NEXT_MILESTONE_AUTHORIZED = NO.

## Manifest note

MANIFEST_SHA256.csv is written after this handoff as the ABSOLUTE LAST package file; its SIZE/SHA and the read-only bijection verification are reported in the terminal message only. HARD_STOP = YES.
