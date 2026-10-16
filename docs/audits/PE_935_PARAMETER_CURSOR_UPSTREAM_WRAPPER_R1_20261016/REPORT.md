# PE_935_PARAMETER_CURSOR_UPSTREAM_WRAPPER_R1_20261016 — FINAL REPORT

RUN_ID = PE_935_PARAMETER_CURSOR_UPSTREAM_WRAPPER_R1_20261016
RUN_CLASS = BOUNDED_STATIC_CURSOR_RELAY_MICRORUN
ERA = PCG_9_3_5
EVIDENCE_COMMIT = 3fbe93eec04759395223e6677b5040273d29222a
BASE_SHA = NOT_APPLICABLE_PRIVATE_RUN_NO_GIT_WRITE
generated_utc = 2026-10-16T14:30:41.494199+00:00
time_provenance = measured by the t00_write_doc.py serializer at the moment of writing this prepared content (no agent-authored time field in this document)

## 1. RUN_STATUS / SCIENCE_RESULT / EVIDENCE_STATUS (kept separate)

- **RUN_STATUS = PARTIAL** (process terminal). Two binding reasons, both disclosed in QC.json: (a) the shared error-correction budget is exhausted — the controls qualifier needed rounds 1 (v1 child-argv defect) and 2 (v2 claims-wrapper defect) before executing correctly; both defective versions and outputs are preserved byte-untouched and the v3 controls pass 4/4; per contract section 9 a PARTIAL terminal is disclosed after 2/2 rounds. (b) OPEN material finding F1: a Windows CRT text-mode write defect (run_common.atomic_write_bytes without O_BINARY) CRLF-expanded every artifact written through that path; the saved PE header buffer is 4099 B on disk instead of 4096 B (byte-faithful content PROVEN recoverable: replace \r\n with \n yields exactly 4096 B / SHA256 636B01A25A9DE410781805D67AE1149FA64DF3D26C5C4FDE7D2D9EBCABC5A5C0, equal to the logical identity recorded at write time); no repair round remained when detected and no correction was performed. Science content is NOT affected by either process finding.
- **SCIENCE_RESULT = WRAPPER_CURSOR_RELAY_CONFIRMED_CONDITIONAL_ON_DECLARED_MODELS.**
- **EVIDENCE_STATUS = CONFIRMED** for the scoped claim below, with separate flags: scope = the 82-B window [0x00852A30,0x00852A82) of the pinned Entropia.exe decoded from the preregistered start by both pinned decoders with full agreement; model = CONDITIONAL_ON_ENTRY_MODEL + CONDITIONAL_ON_ABI_MODEL (without the ABI model the value identities crossing the opaque helper CALL remain NOT_ESTABLISHED).

## 2. Answer to the question (all from bytes; roster decode/INSTRUCTION_ROSTER.json, 37 rows)

**Is the value passed to FUN_00852750 the same cursor C the wrapper received at entry?** YES — as a RELAY, not a construction: C_wrapper_entry is the wrapper's single incoming stack argument at **[entryESP+4]**, loaded into ESI @0x00852A32 (`8b 74 24 0c`, MOV ESI,[ESP+0xC]; after PUSH EBX/PUSH ESI, [ESP+0xC]=[entryESP+4]); the SAME register value is PUSHed as the parser's stack argument @0x00852A74 (`56`, PUSH ESI). Between the load and the push there is exactly ONE opaque CALL (the helper 0x0040DE60 @0x00852A56), so the value identity at the push is CONDITIONAL_ON_ABI_MODEL (ESI callee-saved); without the model it is NOT_ESTABLISHED. Within the window there is NO cursor construction, no allocation, no field/global load and no opaque return feeding the transferred value; the only in-window cursor write is the valid-flag clear [C+0x11]:=0 on the size-fail path (a mutation of one field, not a construction — and on that path B stays 0 so the transfer is never reached).

**Which receiver O is passed?** O_wrapper_entry = the wrapper's entry ECX, saved into EDI @0x00852A3E (`8b f9`, MOV EDI,ECX; note: the PUSH EDI @0x00852A3D saves the CALLER's pre-entry EDI, not O; O has no stack anchor in this window — its only carrier is the register EDI). At the transfer, MOV ECX,EDI @0x00852A75 (`8b cf`) sets the parser's receiver — i.e. the wrapper RELAYS its own entry receiver; CONDITIONAL_ON_ABI_MODEL (EDI preserved across the same one opaque helper CALL). Class identity UNKNOWN.

**Which exact local gate of the read byte allows the transfer?** **B == 1, exactly**: B_read is the u8 read @0x00852A4F (`8a 1c 01`, MOV BL,[ECX+EAX*1]) from [C.data + C.offset] under the guards [C+0x11]!=0 (CMP AL,BL @0x00852A3B; JE @0x00852A40) and offset+1 <= size unsigned (LEA EDX,[ECX+1] @0x00852A45; CMP EDX,[ESI+8] @0x00852A48; JA @0x00852A4B; 32-bit modulo 2^32 arithmetic, no separate no-wrap proof). The gate: MOVZX EAX,BL @0x00852A64; SUB EAX,1 @0x00852A67 (32-bit modulo; B=0 gives 0xFFFFFFFF); JE @0x00852A6A -> transfer at 0x00852A74. B lives in BL (low byte of EBX) across the opaque helper CALL, so B at the gate is CONDITIONAL_ON_ABI_MODEL. On gate failure the bypass returns AL:=0 (XOR AL,AL @0x00852A6E) — the historical pseudo's "return (bVar2-1)&0xffffff00" is decompiler noise, superseded by the bytes.

**Transfer form/target**: direct CALL rel32 @0x00852A77 (`e8 d4 fc ff ff`) to **0x00852750** (arithmetic: 0x00852A7C + s32(0xFFFFFCD4) = 0x00852750; agrees with the PATH_A printed operand). Form CALL (not JMP/tail): the return address 0x00852A7C is pushed, so the parser receives the pushed ESI at [parser_entryESP+4] and the EDI value in ECX. The wrapper's own RET 0x4 on both exits proves cleanup4; the parser's return value passes through unchanged (EAX not modified between CALL and epilogue). The wrapper's cursor also reaches the opaque helper as its RECEIVER (MOV ECX,ESI @0x00852A54) with stack argument 1 (PUSH 0x1 @0x00852A52) — the "advance(1)" shape; the helper's ACTUAL offset/memory effects remain NOT_ESTABLISHED (body closed).

## 3. The three separate guard paths (recorded per the governing ingress interpretation)

- valid-fail: JE @0x00852A40 -> gate with B=0; nothing zeroed, valid NOT cleared, no byte read.
- size-fail (valid!=0, offset+1 > size unsigned): JA @0x00852A4B -> 0x00852A5D -> [C+0x11]:=0 (valid clear @0x00852A61); B stays 0 (the byte was never set); transfer never reached on this path.
- read-success: B:=byte[data+offset]; helper CALL; JMP to the gate.
The redundant re-test CMP AL,BL @0x00852A5D / JE @0x00852A5F is byte-real; on the described size-fail path valid!=0 so that JE is not taken there; no dead-code claim is made. AL is never read after the helper CALL (no volatile-AL-across-CALL misuse in this window).

## 4. Decoder coverage

- PATH_A: GNU objdump 2.44 (/usr/bin/objdump, binary SHA256 96AFB8521834982D0E711B5D6E9785252BF82129FB0106B93A6BD54D83FAE11F), 1 full sweep (1/2), exit 0, over the SAVED buffer via /mnt/d passthrough (no copy into WSL /tmp or home), 37 heads, 0 continuation lines.
- PATH_B: x86dec_pinned.py (27188 B / C8E8470EFD762F66FF20369B2F656694C635131261F4D611DCA9C504E2B90B95), imported read-only by explicit path (no main, no .pyc), sequential sweep from offset 0, 37 decode applications (37/192), no barrier, reached the window end exactly; never fed PATH_A heads.
- Comparison (decode/ab_comparison.json): **37/37 head+length+raw agreement; 7/7 target agreement (5 in-window branches + 2 direct CALLs); 0 disagreements**. Every target recomputed from the recorded raw bytes (TARGET_SOURCE=ARITHMETIC_FROM_RECORDED_RAW) and compared against the PATH_A printed operand — this is not two independent full operand-semantics verifications. Known PATH_B limitations (0x3C/0x3D, 0x9A/0xEA) were NOT exercised by this window (the CMP encodings used are 0x3A/0x3B ModRM forms, both in the pinned table).
- Both decoders swept the full window from the preregistered start; agreement does not prove all entries of 0x00852A30, a complete CFG, or any caller's reachability. All 5 branch targets are inside the window; the 2 CALL targets (0x0040DE60, 0x00852750) are OPEN_EDGE callees — not read.

## 5. Controls (4/4 CONTROL_PASS; two repair rounds disclosed)

Base case ACCEPTED (exit 0). C1 (transfer-site moved to the interior byte 0x00852A78): REFUSED NOT_INSTRUCTION_HEAD. C2 (C and O/receiver carriers swapped): REFUSED ROLE_OR_SLOT_MISMATCH. C3 (preservation across the opaque helper promoted to unconditional CONFIRMED): REFUSED UNJUSTIFIED_OPAQUE_PRESERVATION. C4 (FILE as established cursor source medium and XYZ as recovered): REFUSED UNSUPPORTED_SOURCE_OR_WORLD_PROMOTION. Each refusal is a real nonzero child-process exit with the proper reason, on a COPY of the claims record, through the same bounded predicate as the base case (controls/v3/CONTROL_SUMMARY.json; full results in controls/v3/). CONTROL_PASS = the required refusal for that specific mutation only — not a falsification proof, not a universal validator. The two failed tool versions (t08_controls.py, t08_controls_v2.py) and all their outputs are preserved byte-untouched (controls/, controls/v2/); both failures were fail-closed before any predicate evaluated — no false PASS ever occurred. 5 qualifier executions, 0 retries.

## 6. Budgets (actual/limit; binding source BUDGET_USED.json)

| Budget | Actual | Limit |
|---|---|---|
| window reads / bytes | 2/2 | 164/164 B |
| header reads / bytes | 1/1 | 4096/4096 B |
| full EXE hash passes | 2/2 | 2 |
| PATH_A sweeps | 1/2 | 2 |
| PATH_B decode applications | 37/192 | 192 |
| unique instruction starts | 37/96 | 96 |
| callsite units (VA,role) | 2/6 | 6 |
| symbolic states | 8/8 | 8 |
| provenance rows | 8/12 | 12 |
| new function bodies / callee bodies | 1/0 | 1/0 |
| additional saved inputs | 0/0 | 0 |
| synthetic decode applications | 0/0 | 0 |
| **error correction rounds (BINDING)** | **2/2** | 2 |
| own files (predicted final; binding = manifest census) | 125 | 128 |

Total original EXE bytes read: 16,036,004 = 2x8,015,872 + 4096 + 2x82 — exactly the contract maximum (within_budget at full budgets; SOURCE_READS.json + records/SOURCE_UNCHANGED.json).

## 7. QC chain and process findings

QC.json: **QC_ORIGIN = SELF_REVIEW_WITH_LIMITATIONS** (no fresh reviewer context was available in this session; two algorithms of one author are not two audits); verdict QC_PARTIAL. Checks QC-01..QC-14 all PASS on the science content (pins, prereg-before-read, decoder independence, A/B agreement, buffer integrity, C/O/B encodings, ABI typing, controls, standing machine-check 22/22, strict JSON 50/50, ledger discipline, timestamp honesty, SOURCE_UNCHANGED). Material OPEN findings: **F1** (CRLF write-translation defect: full inventory + PROVEN reversibility of the header buffer + science-impact NONE + auditor verification predicate in QC.json) and **F2** (repair budget 2/2 exhausted -> PARTIAL terminal). EXTERNAL_POSTAUDIT_OF_THIS_RUN = PENDING (PE-MASTER may assign a separate records-only QC).

## 8. SOURCE_UNCHANGED

YES, in the measured scope: hash pass 2 == pass 1 == pinned SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (8015872 B, streaming, both passes); all 12 input copies + INPUT_PINS + the contract re-hashed 14/14 matching pins at close (records/SOURCE_UNCHANGED.json). No whole-EXE copy was ever written; the only original bytes in the package are the permitted header buffer (CRLF-affected on disk — F1, recoverable, logical identity recorded) and the two 82-B window buffers (byte-faithful, SHA256 43134E71A4C84F7F06972F9EDC3C6BDC8A29A5FCBCF27E6D95252FE5B2D30B5C, byte-identical reads).

## 9. Typed standing (contract section 11 block, machine-checked 22/22 — records/STANDING_CHECK.json)

```ini
FIELD_SEMANTICS = UNVERIFIED_EXCEPT_SCOPED_WIDTH_AND_ADDRESS_FACTS
CURSOR_SOURCE_MEDIUM = UNKNOWN
CURSOR_CONSTRUCTION_OR_FILL_UPSTREAM = NOT_ESTABLISHED
ACTUAL_ADVANCE_HELPER_EFFECTS = NOT_ESTABLISHED
ACTUAL_VIRTUAL_CALLEE_TARGET = NOT_ESTABLISHED_UNLESS_DIRECTLY_EVIDENCED_IN_SCOPE
ACTUAL_VIRTUAL_CALLEE_EFFECTS = NOT_ESTABLISHED
ALLOCATION_RETURN_EQUALS_INITIALIZATION_RETURN = NOT_ESTABLISHED
STATIC_BUILDING_ROLE = NOT_ESTABLISHED
MODEL_218757_TO_THIS_PARSER_INSTANCE = NOT_ESTABLISHED
MODEL_218757_TO_CMO_JOIN = NOT_ESTABLISHED
WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED
HISTORICAL_PLACEMENT = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
PREDECESSOR_PROCESS_TERMINAL = PARTIAL
RETROACTIVE_AUTHORIZATION = NO
CANONICAL_GATE_EFFECT = NONE
REPOSITORY_MODIFIED = NO
COMMIT_PUSH = NOT_PERFORMED
EXTERNAL_POSTAUDIT_OF_THIS_RUN = PENDING
NEXT_EXPERIMENT_AUTHORIZED = NO
NEXT_MILESTONE_AUTHORIZED = NO
HARD_STOP = YES
```

The predecessor's PARTIAL terminal and its open findings (P2-1, DISCLOSURE-M1, PRI-PA-01/02/03) are preserved as history; this run does not repair them and does not treat the predecessor as PASS.

## 10. Artifacts and manifest note

Required artifacts are materialized under OUTPUT_ROOT (PREFLIGHT.json, RUN_CONFIG.json, PREREGISTRATION.json, SOURCE_READS.json, buffers/, decode/ (PATH_A_SWEEP.txt, PATH_B_SWEEP.json, ab_comparison.json, INSTRUCTION_ROSTER.json), EVIDENCE.json, controls/ (v1/v2 preserved + binding v3), QC.json, BUDGET_USED.json, ATTEMPT_LOG.jsonl (append-only, 19 planned lines with prefix-hash chain), records/ (pe32_mapping.json, SOURCE_UNCHANGED.json, JSON_VALIDATION.json, STANDING_CHECK.json), this REPORT.md, HANDOFF.md, STAGE_ACCEPTANCE_GATES.csv, artifact_index.csv). **MANIFEST_SHA256.csv is written by t10_manifest.py AFTER this report as the ABSOLUTE LAST package file** (dynamic census of every physical file except itself; zero exclusions; the ledger physically closes before the manifest census). The manifest's SIZE/SHA and the read-only bijection re-verification result are reported in the TERMINAL MESSAGE ONLY, outside this package. Note (F1): the manifest is the binding DISK identity layer; the ledger outputs are the logical (pre-CRLF-translation) identity layer.

## 11. FIRST_MISSING_EDGE (proposal only, NOT executed)

After a confirmed relay, the first missing edge is: **who supplies C to FUN_00852A30 (the caller of the wrapper) and where that caller's cursor buffer is constructed/filled** — an upstream caller-census question outside this window; the parser (FUN_00852750) and the helper (0x0040DE60) bodies remain closed. This is a proposal for a separate decision; NEXT_EXPERIMENT_AUTHORIZED = NO.

HARD_STOP = YES — no next experiment or milestone is authorized by this report.
