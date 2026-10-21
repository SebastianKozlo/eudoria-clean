# ADDITIVE ERRATUM RELATION - PE_935_DISPATCH_ARGUMENT_IDENTITY_OPENCODE_SAVED_R1_20261021

This publication is ADDITIVE. It does not edit any frozen/published history of the predecessor run PE_935_CALLER_TRANSFORM_BUFFER_PRODUCER_OPENCODE_SAVED_R1_20261020 or its published correction packages.

Incorporated corrections (from the external deep postaudit PE_935_CALLER_BUFFER_DEEP_POSTAUDIT_R1_20261021, verdict PARTIAL_PASS_WITH_MATERIAL_CORRECTIONS; published here as context, not as new evidence):
- CB-C2: zero literal direct CALLs to 0x0085A1B0 is NOT treated as proof of virtual dispatch. This run instead measured the full in-corpus census (direct_callers=0, direct_jumps=0, address_mentions=0 in the pinned textual listing, format-validated) plus a structural GA3 scan (0 slot/address matches in the single pinned saved dataset, census_complete=true), and left DISPATCH_IDENTITY explicitly UNRESOLVED with a preserved candidate set (computed pointer / dispatch table outside corpus / no representation).
- CB-C1/CB-C3: the prior 13-word frame results are not re-derived or broadened; the i9/i10 x87 FLD/FSTP round-trip framing is retained wherever the prior is cited.
- CB-C4: helper 7C3BB0 addresses remain 007C3Bxx in this run; no 85A3B prefixes were introduced.
- CB-C5/CB-C6/CB-C7: prior FPU-tail, P1-branch and opaque-modref caveats remain premises; this run lists its own unqualified callees explicitly (OPEN_TARGETS in the local sealed package).
- CB-C9: this run uses a distinct clean authoring root (guard check bijection PASS, no inherited bytecode cache); the historical contaminated-root incident is NOT repaired here and remains disclosed in the postaudit.
- CB-C10: publication is executed only after seal; the sealed science root MANIFEST_SHA256.csv is D280880DA4A4453E1CCF89967DDC6EB87BE037C101358CFE76AD004F78DDD1C8, 59 rows + manifest = 60 files, guard verify PASS.

New results of THIS run (see REPORT.md): entry/caller of 0x0085A1B0 has no representation in the admitted saved sources (DATA_BARRIER); arg2 in-body semantics established (float quad, loop seeds from scaled axis differences); PATH_ROLE = procedural region/grid buffer computation (STRONGLY_SUPPORTED), no placement bridge; placement priority of this path LOWERED. WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CURSOR_SOURCE_MEDIUM=UNKNOWN; CANONICAL_GATE_EFFECT=NONE. PENDING_EXTERNAL_POSTAUDIT.
