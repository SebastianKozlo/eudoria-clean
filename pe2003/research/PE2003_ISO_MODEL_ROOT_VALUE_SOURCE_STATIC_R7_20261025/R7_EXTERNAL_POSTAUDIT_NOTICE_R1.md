# R7 external postaudit notice — R8 corrections (additive; historical REPORT.md unmodified)

Run: PE2003_ISO_INPUT_NODE_TRANSFORM_SOURCE_STATIC_R8_20261026 (STATIC_ONLY, ISO PC Gamer Nov 2003 client 5.1.0.0, section1.bin flat image SHA256 D43A23B9EFCFC9BC4092B38FA3C73499DE7DE7B03B20F34478B9E81EE8893631, base 0x401000). This notice is ADDITIVE to the sealed R7 package; the historical R7 REPORT.md is untouched. Corrections confirmed in R8 (dispositions R7-A01..A11; QC Q1/Q2/Q3 PASS):

- Nd (65AB84@40E384; slot4->40EAA0->class-key 6C3940): R7's pixel-data rejection was wrong (integer-only ctor cannot reject); Nd restored to NiPixelData-compatible construction; intern/hash/dictionary roles remain unproven. Confirmed in R8 (disposition R7-A01).
- NAME alias: R7's 51E010->5BA110 consumer was not proven to be the handler ARG_NAME flow (incoming ECX of 51C940 not proven = global ctx); 5BA110 remains quarantined, not an automatic P0 (R7-A02).
- Virtual receiver: 417663 vcall+8 / 41766C vcall+24 receiver = input X (EBX), NOT the temporary collector mapped at 6C3A70; 37 is an array count, not a slot count (R7-A04; R8 C1 CONFIRMED).
- Two lookup arguments: 52A130 arg2 from [stack+24]@46F216 and byte [S+1A]@46F24D->5257C0 are distinct values with distinct roles (R7-A03).
- Unique vs charged: 21 distinct extracts / 3145 summed rows / 2715 unique (VA,bytes) — 5880/6180 were reserved exposures (charged), not actual (R7-A08).
- Provenance label: guarded bytes always used the correct ISO5.1 image (D43A blob); the D43A label error was documentation-only (R7-A11).
- Post-seal immutability violations INC002/003 (log deletion, manifest replacement) stand as documented process violations; R8 froze SCI once (manifest written LAST, self-excluded) and keeps errata/receipts outside the sealed root.
- What R8 confirmed vs still open: X vptr / M class / S==P / R identity / decrypt-site remain OPEN; definition->resource binding VERIFIED for the 2003-family corpus; ISO5.1 build presence NEGATIVE_BOUNDED; consumption machinery EVIDENCED (presence->execution PARTIAL). Canonical effect NONE.

Details: pe2003/research/PE2003_ISO_INPUT_NODE_TRANSFORM_SOURCE_STATIC_R8_20261026/REPORT.md (claims C1-C14, class-identity matrix, QC findings, closure eligibility).
