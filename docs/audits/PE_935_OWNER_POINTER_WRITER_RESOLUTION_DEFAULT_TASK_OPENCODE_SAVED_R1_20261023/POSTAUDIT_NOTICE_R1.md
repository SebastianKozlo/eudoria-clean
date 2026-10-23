# POSTAUDIT_NOTICE_R1 — OPR-A01..A06 (additive)

This notice acknowledges, additively and without modifying any frozen artifact, the external postaudit verdict for PE_935_OWNER_POINTER_WRITER_RESOLUTION_DEFAULT_TASK_OPENCODE_SAVED_R1_20261023 (PARTIAL_PASS_WITH_MATERIAL_CORRECTIONS / PARTIAL_NONCOMPLIANT_WITH_ADDITIONAL_ARTIFACT_DEFECTS; publication 6c65d15e byte-integrity PASS).

- OPR-A01: accepted — EDI in ctor 00528E50 is ARG1 (caller-stack buffer), not arg3; prologue 0x38, read [ESP+0x3C] = entryESP+4; copy source arg1+0x20/+0x24.
- OPR-A02: accepted — 004154F0 does not consume the pushed B; 00856190 receives B as stack arg; map-like call shape confirmed, insert/key/flag semantics remained conditional on 00856090/00854D90 (opened in the successor run, see OFL claims).
- OPR-A03: accepted — 7 ECX=B callsites are a scoped register census, not full transitive modref; 'none writes' superseded by 'no observed additional nonzero direct store in the examined bodies'; 0085B652 stays closed as stack store.
- OPR-A04: accepted — H5 union 659; primary x86 union 696; 25 pseudocode lines separate; 2356 is a LOWER_BOUND; finish verifiable in message.data.finish; actual task count 12/12.
- OPR-A05: accepted — INPUT_RECHECK.json invalid JSON and STAGE_ACCEPTANCE_GATES.csv inconsistent width (also public at the time); byte-seal did not prove format; superseded versions remain byte-untouched as historical.
- OPR-A06: accepted — QC-derived exact subclaims only; no wholesale QC_FAIL->QC_PASS promotion; no post-hoc argument indices.

Successor run (this publication): PE_935_OWNER_FACTORY_ATTACH_LOOKUP_DEFAULT_TASK_OPENCODE_SAVED_R1_20261023 opened the conditional callees and closed the OPR-A02 flag semantics mechanically (flag byte [P+0x4]: 1=newly inserted, 0=found existing; slot0(B,1) runs on the FOUND case) — see its REPORT and DERIVED_CLAIMS.
No historical file was edited; this notice is a NEW file. WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CANONICAL_GATE_EFFECT=NONE.
