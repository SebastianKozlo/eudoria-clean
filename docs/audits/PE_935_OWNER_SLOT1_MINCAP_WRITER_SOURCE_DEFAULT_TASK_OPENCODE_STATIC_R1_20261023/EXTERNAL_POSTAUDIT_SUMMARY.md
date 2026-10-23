# EXTERNAL_POSTAUDIT_SUMMARY — PE_935_OWNER_SLOT1_MINCAP_WRITER_SOURCE_DEFAULT_TASK_OPENCODE_STATIC_R1_20261023

One-line: the long-missing VT+4 values of the two candidate vtables were recovered by a single authorized minimal static capture (4 DWORD cells + header window + two full hashes), and the derived-table slot proved to be a writer method statically bound to the creator(0x004C46C0)->ctor(0x00528E50) class; the chain terminates honestly at a runtime-vptr barrier; no world placement claimed.

Key results for external review:
1. STATIC capture PASS at pinned identity (hash pin E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31); cells: BASE VT+4=0x0095D4FA, DERIVED VT+4=0x00528380; both slot-3 controls matched prior saved targets (0x0085B6A0 / 0x005278A0).
2. BASE VT+4 is an import-style forwarding thunk (indirect jump through .rdata cell 0x00A75378; content not read). HBR-A03 resolved: even address; prior rejection unjustified; the same target appears in three other saved vtable contexts (S4B).
3. DERIVED VT+4 (0x00528380) writes two float triples + three floats + five tail fields into its own object; values come from two producer methods that forward through an opaque virtual dispatch on sub-object [this+0x2c] — ultimate provenance UNKNOWN (runtime-vptr barrier; saved-only scope).
4. Decisive join: ctor 0x00528E50 stores EXACTLY 0x00A7DCB0 = captured derived-table base => STATIC class-vtable binding for the creator->ctor class; runtime dispatch remains NOT_OBSERVED; RECEIVER_JOIN stays NOT_ESTABLISHED (HBR-A01).
5. Honest negatives: no world/scene/model/resource evidence in any read chunk; base-table class UNKNOWN.

Fresh QC: QSCI QC_PARTIAL (two wording corrections applied pre-seal); QACCOUNT PASS (three administrative updates applied). Fresh-auditor caveat: hashes are recorded claims (no re-hash of the forbidden original); verification at saved-disassembly level; creator->ctor chain is prior canon.

Invariants: WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CURSOR_SOURCE_MEDIUM=UNKNOWN; CANONICAL_GATE_EFFECT=NONE.
Next best edge: the [this+0x2c] runtime-vptr dispatch (or a new explicitly authorized minimal static read for the sub-object class vtable); secondary: the 0x00A75378 forwarding cell.
