# CONTROL_CASE — PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004

## The control (naturally available inside the SAME decoded mechanism)

The record-apply loop (FUN_00726900 @0x007269D0..0x00726A35) executes the
SAME instruction sequence for EVERY record entry. The destination of each
write is computed per-entry as:

```text
dest = [class_obj+0x40] + slot->id * 4      (LEA ECX,[EDX+ECX*4] @0x00726A14)
slot = FUN_0070C180(factory, tag)           (CALL @0x00726A03)
slot->id = tag + 4                          (ADD ECX,4 @0x0070CBF6 in SLOT_ADD)
```

Therefore the mechanism maps record tags to table indices as id = tag+4
(schema range tags 0..7 -> ids 4..11):

| record tag | slot | id | destination | traits (canon kinds {4,3,1,4,1,2,1,2}) |
|---|---|---|---|---|
| 2 | 2 | 6 | &table[6] | int (kind 1) |
| 4 | 4 | 8 | &table[8] | int (kind 1) |
| 6 | 6 | 10 | &table[10] | int (kind 1) — THE AUDITED ATTRIBUTE |
| 7 | 7 | 11 | &table[11] | kind 2 |

Machine-verified schema pins:
- slot 6: args `50 6A 00 6A 00 6A 01 6A 06` @0x0073758D (traits,0,0,kind=1,
  tag=6), CALL FUN_0070CBC0 @0x00737598; tag imm `6A 06` @0x00737594.
- slot 7: args `50 6A 00 6A 00 6A 02 6A 07` @0x007375A2 (kind=2, tag=7),
  CALL FUN_0070CBC0 @0x007375AD.
- slot 2: pattern-search of the widened schema window
  (01_RAW/S5 gate Q9, 0x007374F0..0x00737590) found EXACTLY ONE occurrence
  of `50 6A 00 6A 00 6A 01 6A 02` (kind=1, tag=2 — the same int-traits
  family as slot 6), with its SLOT_ADD call at found_VA+11 — unique_found
  PASS (see S5_QC_BATTERY.json Q9).

## What the control demonstrates

1. ATTRIBUTE-IDENTITY DISCRIMINATION: through the identical loop body, a
   record entry carrying tag 2 writes &table[6] and an entry carrying
   tag 6 writes &table[10] — disjoint destinations from the same
   instructions, differing ONLY through the schema descriptor's id
   (tag+4). The mechanism does not collapse all attributes into one sink.
2. SAME-TRAITS DISJOINT-INDEX pair: tag 2 and tag 6 share kind=1 (int) and
   therefore the SAME traits writer FUN_009777F0 and the SAME store
   instruction @0x00977810 — the only difference is the table index.
   This isolates the IDENTITY discrimination (the id) from the VALUE
   machinery (the traits reader/writer).
3. CROSS-VERSION CORROBORATION (cited, not re-derived): the R1 canon
   CONTROL-A established the same discrimination from the schema side
   (tags 2/4 same SLOT_ADD machinery, disjoint value slots 6/8). This
   run's control is derived WRITER-SIDE (the apply loop + SLOT_ADD id
   formula), independently of the getter-side claims.

CONTROL_CASE = PASS
