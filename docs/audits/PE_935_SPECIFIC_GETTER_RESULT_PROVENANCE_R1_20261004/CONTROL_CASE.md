# CONTROL_CASE — PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004

CONTROL_CASE = PASS. Two static negative controls executed within limits
(order-A and order-C of the contract's preference list), both byte-pinned in
the pinned EXE by the QC battery (01_RAW/S11_QC_BATTERY.json).

## CONTROL A — same getter/provider mechanism, PROPERTY_TAG ≠ 6

**Design.** The audited getter mechanism (FUN_0070C180 slot addressing +
value-table indexing) is shared by all 8 factory slots. Tags 2 and 4 are
ALSO kind-1 (int) slots with the SAME int-traits object (FUN_00977A50) and
the SAME SLOT_ADD machinery — if the analysis were "generic mechanism =
provenance", tags 2/4/6 would be indistinguishable. They are not: each tag's
slot carries its own ATTRIBUTE ID (tag+4) and therefore reads a DIFFERENT
value-table entry.

**Byte-pinned evidence (FUN_007374F0 slot-add argument sequences).**

| tag | args bytes (verified) | kind | SELECTED_VALUE (attr id) | key slot |
|---|---|---|---|---|
| 2 | `50 6A 00 6A 00 6A 01 6A 02` @0x737539 | 1 (int) | 6 | table[6] |
| 4 | `50 6A 00 6A 00 6A 01 6A 04` @0x737563 | 1 (int) | 8 | table[8] |
| 6 (AUDITED) | `50 6A 00 6A 00 6A 01 6A 06` @0x73758D | 1 (int) | 10 | table[10] |

All three use identical machinery (SLOT_ADD @0x0070CBC0 — machine-verified
call sites 0x00737544 / 0x0073756E / 0x00737598) and identical int traits
(FUN_00977A50 — machine-verified call sites 0x00737534 / 0x0073755E /
0x00737588), yet the audited path's key comes from table[10] — a slot
DISJOINT from tag 2's table[6] and tag 4's table[8].

**Discrimination demonstrated:** the generic getter/slot mechanism does NOT
identify the value source of the audited tag-6 result; only the tag-6
specific chain (slot 6 → id 10 → table[10]) does. A hypothetical claim "the
value comes from the class component's value table" is true for ALL THREE
tags, but the SPECIFIC provenance question (which entry, whose writer)
requires the tag-6 chain this run pinned.

## CONTROL C — the alternative/fallback branch produces NO lookup key

**Design.** The fallback path of the getter machinery (descriptor invalid:
kind==0, kind!=1, or flags bit0 set; also the out-of-range default slot
0x00BA5108 which is PERMANENTLY ZERO — no writers, .data virtual tail,
census in 01_RAW/S5_CREATOR_DECODE.json) must NOT be conflated with a
successful getter result.

**Byte-pinned evidence.**
- `B8 74 93 BA 00 C3` @0x00977780 — FUN_00977780 returns the static VA
  0x00BA9374.
- [0x00BA9374] has ZERO .text writers (the only .text reference is the
  MOV EAX above) → the virtual-tail dword is 0 at runtime.
- Therefore the fallback converges at 0x004C554E with EAX=0x00BA9374,
  reads 0, and FUN_004C5480 returns NULL.
- `0F 84 ED 04 00 00` @0x004C55C3 — TEST EAX,EAX; JE 0x004C5AB6 (machine
  -verified target): a NULL getter result ABORTS the lookup — FUN_0072F880
  is never called, NO key is produced.

**Discrimination demonstrated:** the same machinery (property-slot getter +
FUN_004C5480 shape) can produce a NON-result (NULL) — so the existence of
the mechanism alone proves nothing about the provenance of any actual key;
only the valid-descriptor normal branch (kind==1, flags bit0 clear, nonzero
table entry) yields the FUN_0072F880 lookup this run's CONFIRMED data-flow
verdict covers.

## Acceptance-rule conformity

- Neither control is a same-numeric-value coincidence (rule 1).
- CONTROL A is NOT "same property tag on a different receiver" (rule 2) — it
  is the same mechanism at DIFFERENT tags on the SAME factory.
- CONTROL C is the contract's order-C alternative/fallback branch.
- No synthetic misattribution case was needed; both controls are real code
  paths in the pinned EXE, and neither establishes actual provenance — they
  only test the evidence rules, as required.
