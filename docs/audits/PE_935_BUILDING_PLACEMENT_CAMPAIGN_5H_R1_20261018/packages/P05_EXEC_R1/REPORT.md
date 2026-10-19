# P05 REPORT (DIRECT_ANALYST_FALLBACK by PE-MASTER)
Attribution: parent fallback per CONTRACT section 4 after two incomplete child executions (artifacts of both attempts preserved). No pretending of independent QC; fresh reviewer to follow.
## Scoped result
Dominant producer of the 12 position bytes written by 005094C0 is COMPUTED, not raw: 85BFA0 (affine matrix via virtual slot +0x24 of [this+0x2C] + helpers 96cb20/96cf80), 85C0C0 (virtual slot +0x28 pass-through), 85C0F0 (rotation derived from 85BFA0 + 96cd10), 85C280 (gated virtual slot +0xdc). Alternate 862850 is a RAW FIELD COPY from receiver+0x3C..0x44 (field semantics unknown - could be any 3-float field). 509070 is NOT an SF+30 link-setter (3-DWORD setter to [this+0x80..0x88]); SF+30 node-role edge remains unresolved.
## Per-producer table
| producer | kind | base | writes | calls |
|---|---|---|---|---|
| 0085BFA0 | computed matrix getter | [this+0x2C] virt slot +0x24 | out 3x3 + out+0x24..0x2c trans + 1.0 | 96cb20,96cf80,virt |
| 0085C0C0 | virtual pass-through 3f | [this+0x2C] virt slot +0x28 | out+0/4/8 | virt |
| 0085C0F0 | derived rotation | 85BFA0 result | zeros + 96cd10 out | 85bfa0,96cd10 |
| 0085C280 | gated virtual 3f | [this+0x2C] virt +0x160(0x80)/+0xdc | out+0/4/8 | virt x2 |
| 00862850 | RAW field copy | [this+0x3C..0x44] | out+0/4/8 | 0 |
| 00509070 | field setter (NOT SF+30) | arg1 | [this+0x80..0x88] | 0 |
## Counters
6 bodies / 164 rows / 8 CALL actual (12 reserved, no refund) / 4 candidates.
## Remaining edge
Class identity + vtable of [this+0x2C]; slots +0x24/+0x28/+0xdc targets; 862850 receiver class; SF+30 writer unknown.
Standing: WORLD_XYZ_RECOVERED=NO, HISTORICAL_PLACEMENT=NOT_ESTABLISHED, CURSOR_SOURCE_MEDIUM=UNKNOWN, CANONICAL_GATE_EFFECT=NONE.
