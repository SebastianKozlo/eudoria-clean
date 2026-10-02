# NEGATIVE_CONTROLS — PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002

All controls executed STATIC (no client launch). The traced mechanism WAS reached
(the TLV property parse with byte-pinned read/store), so the full §13 control set
applies (NC-VALUE with its lookup/comparison precondition evaluated below).

## NC-FRAMING (mandatory) — EXECUTED, PASS

- Control: in-memory corrupted/truncated record variants must make the executor's
  framing parser FAIL (proves the framing is falsifiable, not a self-confirming walk).
- Executor implementation: 03_SCRIPTS\s1_framing_census.py (in-run; independent of the
  prior tool lineage; the prior tool was used only for the labeled cross-validation).
- Variants and results (01_RAW\RECORD_FRAMING_SUMMARY.json, negative_control_nc_framing):
  | VARIANT | MUTATION | EXPECTED FAILURE | ACTUAL | FAILURE_CASE_DETECTED |
  |---|---|---|---|---|
  | NC1 | record 0 header size field -> 0x00FFFF00 (beyond EOF) | parser must fail | FAILED with "payload beyond EOF at frame 16" | YES |
  | NC2 | whole file shifted by 1 byte | magic check must fail | FAILED with magic mismatch | YES |
  | NC3 | file truncated by 64 bytes | EOF violation | FAILED with "payload beyond EOF at frame 174736" | YES |
  | NC4 | record 0 ver field -> 2 | ver!=1 must fail | FAILED with "ver!=1 at frame 16" | YES |
  | NC5 | global base field -> 64 | stride misalignment | WALK SUCCEEDED - measured NON-DISCRIMINATING for this corpus: with uniform 56-byte payloads, align_up(72,64)=align_up(72,128)=128, so base 64 yields the identical stride. Recorded honestly as a non-discriminating variant (NOT a control failure of the framing; NC1-NC4 carry the falsification). |
- EXPECTED_FAILURE: framing violations are detected. ACTUAL_RESULT: 4/4 mandatory
  corruption classes detected (NC5 non-discriminating, documented).
- FAILURE_CASE_DETECTED: YES (NC-FRAMING verdict PASS).

## NC-ANCHOR-ADJ (mandatory once the client read is claimed) — EXECUTED, PASS (instruction level)

Control: the adjacent displacement field (+0x2C) of the anchored record, extracted by
the same rule, must NOT land in the same destination field as +0x30; verify at the
instruction level: distinct source displacement => distinct destination store/field.

- Feasible part (extraction/decode, per FORMALIZER_NOTES FN-1):
  record 0: +0x2C raw = `00 00 11 00`, LE u32 = 1,114,112 (0x110000) — DIFFERENT bytes
  and value from +0x30 (`BB 2E 00 00` = 11,963) under the identical extraction rule.
  (01_RAW\FIELD_BYTE_ANCHOR.json, nc_anchor_adj_feasible_part.)
- Instruction-level part (now mandatory because the client read IS claimed):
  - The 4 bytes at payload+0x2A..+0x2E are consumed by the tag-0x10 VALUE read:
    cursor offset 0x2A, 4-byte load @0x00412553, store @0x0041255A to descriptor
    field index 0x10+4 = 20 -> **value_array slot 20**.
  - The 2 bytes at payload+0x2E..+0x30 are consumed by the TAG read @0x007269E7
    (u16 load) -> the descriptor lookup for tag 0x11.
  - The 4 bytes at payload+0x30..+0x34 are consumed by the tag-0x11 VALUE read:
    cursor offset 0x30, 4-byte load @0x00412553, store to field index 0x11+4 = 21 ->
    **value_array slot 21**.
  - Therefore the +0x2C window's bytes are consumed by DIFFERENT instructions with
    DIFFERENT destinations (slot 20 / the tag register) than the +0x30 bytes
    (slot 21): **distinct source displacement => distinct destination store** — the
    destination claim survives the adjacent-displacement control.
- EXPECTED_FAILURE: if the parser were offset-insensitive (e.g., a fixed-struct
  misread), +0x2C would land in the same slot. ACTUAL_RESULT: distinct instructions,
  distinct slots (20 vs 21). FAILURE_CASE_DETECTED: YES (control discriminates).

## NC-RECORD (mandatory) — EXECUTED, PASS

Control: a second record (different +0x30 value, e.g. ANCHOR_ZERO = record 1014,
value 0) passes through the SAME parser path — establishes the mechanism is
field-driven, not record-specific.

- Shared evidence: 01_RAW\TLV_WALK_CENSUS.json — all 1,366 records (including 1014 and
  1015, the zero-valued ones) have the identical tag shape {1, 0xC, 0xD, 0xE, 0x10,
  0x11}, count 6, tail 0; tag 0x11's value offset == 0x30 in 1366/1366 records.
- Instruction path: identical (the same 0x00412553 read / 0x0041255A store; the
  parser is descriptor-driven, not record-driven).
- Shared: the whole parse chain. Differing: only the byte VALUES at +0x30
  (record 0: 11963; record 1014: 0).
- EXPECTED_FAILURE: if the parse were record-specific, the zero-valued record would
  take a different path. ACTUAL_RESULT: same path, field-driven. FAILURE_CASE_DETECTED:
  YES (control discriminates).

## NC-VALUE (mandatory IF a lookup/comparison mechanism is claimed) — NOT APPLICABLE, documented

- Precondition check: the traced mechanism contains NO lookup and NO comparison of
  the +0x30 value — the pinned instructions (@0x412553/@0x41255A) perform a pure
  copy (opaque propagation) into the property slot. No branch, no map probe, no
  equality test on the value exists at the traced sites.
- Per §13 ("Do NOT invent an interpretation solely to manufacture a negative
  control"), NC-VALUE is NOT_APPLICABLE_NO_LOOKUP_COMPARISON_CLAIMED.
- Bounded note: the neighboring checks in the parse (descriptor type validity
  @0x726A08; flags bit0 @0x75F687; mode-1 tail size==0 @0x726A87) branch on SCHEMA and
  STRUCTURE values, not on the +0x30 field value; the CRC gate (which WOULD compare a
  record-derived value) is provably skipped for this file (crc fields all 0).

## NEGATIVE_CONTROL_STATUS = PASS

All mandatory controls executed and discriminating; the one not-applicable control
(NC-VALUE) is documented with its measured precondition. SEMANTIC_PASS note: the
controls validate the MECHANISM trace (framing falsifiability, displacement
distinctness, record-independence); the gameplay SEMANTIC of the value remains
unestablished (see 02_ANALYSIS\SEMANTIC_ASSESSMENT.md).
