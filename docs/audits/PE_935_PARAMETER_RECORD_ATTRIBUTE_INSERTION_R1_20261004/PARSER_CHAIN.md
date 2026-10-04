# PARSER_CHAIN — PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004 (PHASE D)

## One-line statement

For RECORD_A (templates.vfs, id2=16083, file offset 560,212), the chain
PHYSICAL RECORD BYTES → CLIENT FILE READER → CLIENT PARSER → REAL KEY + REAL VALUE is
byte-pinned end-to-end from the pinned Entropia.exe. RECORD_KEY_VALUE_DECODE = CONFIRMED.

## The chain (every edge byte-pinned this run; established edges cited + re-verified)

```
"Parameters\templates.vfs" @0x00A86D30 (.rdata, 24 chars + NUL — raw bytes verified)
  └─ PUSH 0x00A86D30 @0x0072FAAC (in FUN_0072FA30, the reader/loader)
      └─ path-build/open call FUN_00401E70 @0x0072FAB7
          └─ file-open with 0x80-byte record-buffer config @0x0072FAF1
              ([ESP+0x4C]=1, [ESP+0x50]=0x80, [ESP+0x54]=8)
              └─ record-id list from the FILE'S OWN INDEX:
                  loop head @0x0072FB20: EBP = current id ptr; [ESP+0x3C] = list end;
                  ESI = [EBP] = record id; advance EBP += 4 @0x0072FC3B
                  └─ per record (loop body 0x0072FB7D..0x0072FC3E):
                      FUN_00971AD0 @0x0072FB7D  (per-record read: seek+read into the
                        0x80 buffer; cursor object at [ESP+0xBC])
                      FUN_00730700 @0x0072FB8E (construct/zero the 0x30-byte template
                        object at [ESP+0x4C])
                      FUN_00730C90 @0x0072FBA5 (THE PARSE — cursor+payload → the
                        template object; EXACTLY 1 call site in the whole binary)
                      FUN_004123D0 @0x0072FBB5 (deref [template] → the id2 key; saved
                        as the pair key at [ESP+0x7C])
                      FUN_005670A0 @0x0072FBCA (copy the parsed object into the pair
                        value slot; key+value pair = {[ESP+0x7C], [ESP+0x80]})
                      FUN_0072F8D0 @0x0072FBE5 (RB-tree insert; EXACTLY 1 call site)
```

## The parser's field decode (FUN_00730C90 — this run's own byte decode)

Normal-path pattern per field: flag gate `CMP [ESI+0x11],BL` (reads enabled iff the
cursor flag != 0; EBX=0 from `XOR EBX,EBX` @0x00730C96); bounds check
`[cursor+0xC]+4 <= [cursor+8]`; read u32 `MOV EAX,[EDX+EAX]`; store to the
destination; advance cursor by 4 via FUN_0040DE60 (byte-decoded in the C1 correction:
`ADD [ECX+0xC],EAX`; `CMP EAX,[ECX+8]`; `JBE` skip — on exceed `MOV BYTE [ECX+0x11],0`,
i.e. FUN_0040DE60 ZEROES the cursor flag once the advanced offset passes the limit).
[C1-CORRECTED failure-path description — SUPERSEDES the prior sentence "a flag-checked
slow path (`CMP [ESI+0x11],BL`) handles the other cursor mode and stores the same
value to the SAME destination (both paths verified)", which was FALSE: there is NO
second cursor mode storing the same valid value.] On the flag-cleared or bounds-failed
paths the parser writes ZERO to the SAME destination and does NOT advance the cursor:
`MOV [EDI],EBX` @0x00730CC3 (id2), `MOV [EDI+8],EBX` @0x00730CF0 (A),
`MOV [EDI+4],EBX` @0x00730D1E (B), `MOV [EDI+0xC],EBX` @0x00730D4C (C) — EBX=0;
the D field via `FLDZ` @0x00730D7A + `FSTP [EDI+0x10]` @0x00730D7C. Each failure join
also re-clears the flag (`MOV [ESI+0x11],BL`, e.g. @0x00730CCA). The normal-path
field mapping below is UNCHANGED and remains valid.

Destinations ([C1-corrected verification claim] byte-verified against the pinned-EXE
store instructions by the correction package's CLIENT_DESTINATION_MAPPING_CHECK
(PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_C1_REPORT_QC_CORRECTION_R1_20261004,
including an A/B-swap mutation falsifier). The R1 QC-7 gate verified only the PAYLOAD
FIELD VALUES at fixed file offsets (PAYLOAD_FIELD_DECODE_CHECK) — it did NOT read
these destination instructions; the independent Desktop post-audit proved that a
deliberate A/B destination swap in this table still passes it (QC_COUNTEREXAMPLE_
SUMMARY.json), which retracts the prior claim that QC-7 verified the destinations):

| Payload u32 (file order) | Destination | Instruction |
|---|---|---|
| payload[0] (id2) | template+0x00 | MOV [EDI],EAX @0x00730CB6 |
| payload[1] (A) | template+0x08 | MOV [EDI+0x08],EAX @0x00730CE6 |
| payload[2] (B) | template+0x04 | MOV [EDI+0x04],EAX @0x00730D14 |
| payload[3] (C) | template+0x0C | MOV [EDI+0x0C],EAX @0x00730D42 |
| payload[4] (D_f32) | template+0x10 (FLD/FSTP) | FLD [EDX+EAX] @0x00730D69; FSTP [EDI+0x10] @0x00730D70 |
| u16 count1 → strings | template+0x14 (vector<string>) | LEA EAX,[EDI+0x14] @0x00730D87; CALL FUN_00730B70 @0x00730D8D |
| u16 count2 → u32s | template+0x20 (vector<u32>) | LEA ECX,[EDI+0x20] @0x00730D92; CALL FUN_00730970 @0x00730D97 |
| trailing u32 (f11) | template+0x2C | MOV [EDI+0x2C],EDX @0x00730DB6 |

[C1/P3 instruction-start corrections in the table above — all re-verified from the
pinned EXE bytes: `MOV [EDI+0x04],EAX` starts @0x00730D14 (89 47 04), NOT @0x00730D16
(that was a mid-instruction operand byte); `MOV [EDI+0x0C],EAX` starts @0x00730D42
(89 47 0C), NOT @0x00730D36; `FLD [EDX+EAX]` starts @0x00730D69 (D9 04 10), NOT
@0x00730D6D; the FSTP site @0x00730D70 (D9 5F 10) was already correct. The
A→+0x08 / B→+0x04 destination PAIRING itself is UNCHANGED and remains valid — what is
retracted is only the false claim that QC-7 automatically verified it (see the C1
correction package's mutation falsifier).]

Note on a wording ambiguity resolved this run: the prior E1 text ("reads u32 fields in
order f0, f2, f1, f3, f4 → +0x00, +0x08, +0x04, +0x0C, +0x10") pairs ambiguous names;
this run's byte decode + the established getter anchors (A@[+0x08] via FUN_007CE1E0 with
the 296445 anchor; B@[+0x04] via FUN_00746550; C@[+0x0C] via FUN_006B22D0;
D@[+0x10] via FUN_0048ADA0) settle it: payload[1]=A→+0x08, payload[2]=B→+0x04.

## STRUCTURAL_PARSE vs FIELD_SEMANTIC

- STRUCTURAL_PARSE (this run, byte-pinned): the field reads/stores above.
- FIELD_SEMANTIC (A = model nif id, B = collision bvi id, etc.): inherited from the
  tracked BRIDGE R1 package; NOT re-derived; NOT promoted beyond it.
- UNKNOWN fields: none within the 28-byte payload grammar; the header `crc` field's
  checking semantics were not investigated (its stored value is retained as identity).

## Reachability (why RECORD_A is certainly parsed by this loop)

The loader walks the FILE'S OWN id index (all records); this run's independent walk
reproduces the prior census exactly (5,438 records, EOF-exact; both anchor offsets) —
the loop is the sole parse caller (1 call site) and the sole insert caller (1 call site).
No on-demand/lazy path is involved for this container (contrast: the 20002-class on-demand
loader — different file family, not opened this run).
