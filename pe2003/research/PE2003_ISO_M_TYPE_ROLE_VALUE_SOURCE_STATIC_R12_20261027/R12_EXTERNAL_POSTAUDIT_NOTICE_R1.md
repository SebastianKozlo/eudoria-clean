# R12 external postaudit notice R1 (additive; published by R13)

This notice is ADDITIVE: no R12 file, manifest row or ENTRYPOINT line is modified by this change. R12's published history is NOT rewritten; its bytes stand as published. This notice records the R13 static results that dispose of or qualify the R12 external postaudit items, so downstream readers carry them forward correctly. R13 operated on the same pinned image (STATIC_ONLY: section1.bin SHA256 D43A23B9...3631, base 0x401000); the new evidence itself is in the R13 public report (pe2003/research/PE2003_ISO_NODE_IDENTITY_VALUE_PROVENANCE_STATIC_R13_20261028/REPORT.md). No game payloads are contained here.

## Disposition of R12 postaudit items after R13 (static)

1. R12-A01 (UPHELD, with R13 qualification results): the R13 run qualified the saved initializer candidates as real — stubs 0x405410 ("NiNode") and 0x414A00 ("NiAVObject") CALL the shared setter 0x417560; the zero-content observation is bounded-confirmed at token 0x6C3B6C and is correctly kept as TOKEN_ADDRESS != TOKEN_CONTENT (zero content does not force runtime initialization). ACTUAL_M_TYPE remains UNKNOWN and RUNTIME_INIT_REQUIRED remains unproven — exactly the A01 discipline.
2. R12-A02 (UPHELD, instruction-confirmed): EBP is overwritten at 0x53C929 and ESI at 0x53C97A inside 0x53C780; the naming concerns the ARRAY CHILD (M_named = element [owner+0x14]), not the root; 0x5A2840 is a pure [ecx+0x10] getter. No register identity across the body, no equality of repeated opaque getter results.
3. R12-A03 (UNCHANGED): R13 produced no new data on the ".cfg" IO role; the A03 wording stands.
4. R12-A04/A05 (out of R13 scope; maintained): the visitor/FVALUE items were not re-researched in R13; the R13 visitor work falsified the JOIN with the route M (DISJOINT) without reopening those items.
5. R12-A06/A07 (PROCESS, R13 enforced): every R13 native task (22 in the final pre-seal census: 20 research + 2 closing QC) was dispatched with its own prior admission; the closing was an honest budget stop — budget_guard DENY at ledger seq 129 (unique-row research pool negative after the QC phase) — a tool-enforced stop on the protected reserve, NOT a COMPLETED_CONTRACT claim and NOT source exhaustion (SCIENCE_STOP, PARTIAL_PASS_MATERIAL_ADVANCE).
6. R12-A08 (PUBLICATION IO): R13 measured its own publication IO in the receipt package of the publication job (isolated-worktree checkout bytes, projection bytes, Git admin command count, recorded separately; the manifest covers the published blobs).

Advisory; CANONICAL_GATE_EFFECT=NONE. WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; SOURCE_SPECIFIC_ISO_MODELS=NOT_OBSERVED_IN_BOUNDED_SEARCH; LOCAL_SOURCE_EXHAUSTED=NO.
