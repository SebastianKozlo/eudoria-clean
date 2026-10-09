# ANCHOR_SELECTION — PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009

Anchor discovery per contract §4: search ONLY previously documented
CMO-related forensic evidence and scoped pre-existing disassembly (COMMITTED
tree at BASE b2feef34) for a candidate EXACT memory-store instruction to any
of CMO+0x44 / +0x48 / +0x4C. No broad whole-EXE xref scan, no generic search
across unrelated subsystem functions, no new callee analysis. This document
records the search boundary, the full candidate census (including
rejected/reclassified records), and the selection under the pre-registered
rule (PREREGISTRATION.md §4).

## 1. The leads and their non-status

Leads: CMO+0x44, CMO+0x48, CMO+0x4C. None is a pre-confirmed CMO write, field
identity, vector, coordinate, world XYZ or building placement. "CMO" is a
hypothesis to prove by base-pointer lineage. In the committed evidence the
object family is: new(0x128) -> FUN_00528E50 (derived ctor, stamps vtable
0x00A7DCB0 = .?AVClientMovableObject@@) -> FUN_0085B1B0 (base ctor, stamps
vtable 0x00A91E4C = .?AVMovableObject@@) on the SAME object memory. Stores to
the instance's +0x44/+0x48/+0x4C exist in committed evidence ONLY inside
FUN_0085B1B0 (the base ctor). FUN_00528E50's own body contains NO store to
+0x44/+0x48/+0x4C (its committed hex dump shows stores at +0xA4..+0xCC and
float loads at +0xAC/+0xB4/+0x64->+0xB4 — different offsets; see source A
01_RAW/FUN_00528E50_CONTINUATION.txt and the attribute-seam T2D hex dump).

## 2. Negative search boundary (exact)

Searched (committed documentation only, at BASE b2feef34; untracked foreign
packages excluded — INPUT_IDENTITIES §8):

1. All pinned/required source files (source A 4 files + CLAIM_MATRIX.csv +
   REPIN_ANCHOR_WINDOWS.txt; J3 2 files; MICRO_R1 FINAL_REPORT.md; Source B)
   — read COMPLETELY.
2. CMO-related committed packages (enumerated with tracked-file counts in
   INPUT_IDENTITIES §8), via targeted content search for the lead offsets and
   store forms: patterns `+0x44`, `+0x48`, `+0x4C`, `0x44..0x4C`, store byte
   forms `89 4E 44`, `89 56 48`, `89 46 4C`, `89 4E 48`, `89 56 4C`,
   `89 46 44`, and store-instruction regexes over `mov|fst|fstp|rep movsd`
   with the lead displacements, across docs/audits (git grep over the
   tracked tree).
3. The committed Ghidra full-disassembly corpus
   (PE_NIGHT_AGGREGATE_20260905_160000/GHIDRA_H5_VTABLE2.txt) — the only
   large pre-existing disassembly of the store region.

NOT searched (out of scope by contract §4): whole-EXE byte scans, new xref
enumerations, unrelated subsystem functions, runtime paths, untracked
packages, payload corpora.

## 3. Candidate census (all records; committed evidence only)

### 3.1 Qualifying store family — FUN_0085B1B0 (the base ctor of the CMO-family instance)

Function: FUN_0085B1B0, entry 0x0085B1B0 (padding-proven start: preceded by
`C3` — the terminal ret of the previous thunk — @0x0085B1AC, then exactly 3
bytes `CC` int3 padding @0x0085B1AD..0x0085B1AF in the committed raw region;
measured physically this run). Build: PCG 9.3.5 EXE (SHA E7785430...). Committed sources (all
tracked at BASE):
- PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/01_RAW/T1_REGION_0085B100_0085B900.txt (raw hex rows 0085B1B0..0085B28F)
- PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/01_RAW/DECOMP/F0085B1B0.c (Ghidra decompile: `param_1_00[0x11..0x13] = *puVar2..puVar2[2]` from `puVar2 = FUN_00746560()`)
- PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/REPORT.md S9 + RESEARCH_FINDINGS.md (c) + SEAM_FLOW_MAP.md (summary `[+0x44..0x4C]=[rekord+8..0x10]` via FUN_00746560)
- PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913/06_REPORT/REPORT.md §4.1 item 4 + line 197 (`[+0x44..0x4C]=[FUN_00746560(record)+0..8]=&record+8` @0x0085B27A-2D) + ERRATA_R5.md line 44
- PE_NIGHT_AGGREGATE_20260905_160000/GHIDRA_H5_VTABLE2.txt (instruction-level: 0085b27a CALL 0x00746560; 0085b27f MOV ECX,[EAX]; 0085b281 MOV [ESI+0x44],ECX; 0085b284 MOV EDX,[EAX+0x4]; 0085b287 MOV [ESI+0x48],EDX; 0085b28a MOV EAX,[EAX+0x8]; 0085b28d MOV [ESI+0x4C],EAX)

| ID | Store VA | Bytes (committed) | Instruction | Destination | Notes |
|---|---|---|---|---|---|
| C-A | 0x0085B281 | `89 4E 44` | mov dword ptr [esi+0x44], ecx | [esi+0x44] | record-copy family, +0x44 member |
| C-B | 0x0085B287 | `89 56 48` | mov dword ptr [esi+0x48], edx | [esi+0x48] | record-copy family, +0x48 member |
| C-C | 0x0085B28D | `89 46 4C` | mov dword ptr [esi+0x4C], eax | [esi+0x4C] | record-copy family, +0x4C member |
| C-D | 0x0085B1E4 | `D9 56 44` | fst dword ptr [esi+0x44] | [esi+0x44] | zero-init (0.0f) member of a BULK 12-field float-zero sequence (+0x44..+0x70: 44/48/4C/50/54/58/5C/60/64/68/6C/70) |
| C-E | 0x0085B1E7 | `D9 56 48` | fst dword ptr [esi+0x48] | [esi+0x48] | zero-init, same bulk sequence |
| C-F | 0x0085B1EC | `D9 56 4C` | fst dword ptr [esi+0x4C] | [esi+0x4C] | zero-init, same bulk sequence |

Receiver-lineage assertion for ALL six (committed, and re-pinned physically
this run): `8B F1` mov esi, ecx @0x0085B1B7 — ESI = the ctor entry `this`
(ECX at entry = the object FUN_00528E50 is constructing; committed callsite:
`8B CE` mov ecx, esi + `E8 1E 23 33 00` call 0x0085B1B0 @0x00528E8D in
FUN_00528E50, where FUN_00528E50's own ESI = its entry this via `8B F1`
@0x00528E76; after the base ctor returns, FUN_00528E50 stamps the derived
vtable `C7 06 B0 DC A7 00` @0x00528EA2 = 0x00A7DCB0 = .?AVClientMovableObject@@
on the same object). No instruction in the committed decode between 0x0085B1B7
and 0x0085B28D writes ESI.

### 3.2 Reclassified / rejected records (object-distinction and boundary notes)

| ID | Record | Verdict | Reason |
|---|---|---|---|
| C-G | FUN_00509510 `F3 A5` rep movsd @0x00509557 to SF+0x4C (source A 01_RAW/FUN_509x_SF_METHODS.txt: `lea edi,[ebx+0x4c]`; receiver EBX = the SF passed as ECX=[CMO+0xC0] @0x00529025) | RECLASSIFIED — NOT a CMO store | Receiver is the SF (SceneFeederObject) sub-object, NOT the CMO instance. Contract §3/J3: must not be asserted as a CMO store. `CMO+0x4C` != `SF+0x4C`. |
| C-H | FUN_00528E50 `89 86 C0 00 00 00` mov [esi+0xC0], eax @0x00528FEA | EXCLUDED — real CMO store but offset +0xC0 not in the lead set | Documented (MICRO_R1 E-C1-STORE; source A PA4) as the SF-pointer store; NOT a +0x44/+0x48/+0x4C write. Kept as receiver-context canon. |
| C-I | FUN_00528E50 `D9 9E B4 00 00 00` fstp [esi+0xB4] @0x00529058 | EXCLUDED — CMO store at +0xB4 | Not in the lead set (source A FUN_00528E50_CONTINUATION.txt). |
| C-J | FUN_00745360 (placement-record ctor) `89 46 44`/`89 4E 48`/`89 56 4C` @0x0074539B/A4/AD | RECLASSIFIED — receiver is the placement RECORD object, not the CMO instance | Committed (PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913 01_RAW/F00745360_REC_CTOR.txt); rec+0x44..0x4C is the record's rotation triple per the historical SE-R4-6 correction. A DIFFERENT object from the instance +0x44..0x4C — recorded to prevent conflation. |
| C-K | FUN_008550C0 (manager ctor) `89 46 44` @0x008551CA (+0x48/+0x4C stores @0x00855260 region) | RECLASSIFIED — receiver is the manager singleton object | Committed (attribute seam T2_HEX/mgr_ctor_FUN_008550C0.txt; +0x44 = CS-lock). Not the CMO instance. |
| C-L | FUN_00509330 (SF ctor) `89 45 44`/`89 4D 48` @0x0050944C/55 (fstp [ebp+0x44] @0x005093E9, fst [ebp+0x48] @0x005093F1) | RECLASSIFIED — receiver is the SF (SceneFeederObject, EBP=this) | Committed (PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913 01_RAW/F00509330_SUBC0_B.txt). SF+0x34/0x38/0x3C/0x44/0x48 fields are the SF's own, NOT the CMO instance's. |
| C-M | FUN_008BD720-neighborhood `89 46 44` @0x008bd750 | RECLASSIFIED — receiver class not the CMO; the committed window (source A 01_RAW/FUN_008BD720_DECODE.txt) documents a different function's body with an unestablished CMO relation | No committed receiver-lineage evidence ties its ESI to the CMO instance; not a candidate. |
| C-N | FUN_006C8F80 (CAND-4 child-family base ctor) `89 5E 48`/`89 5E 4C` @0x006c8fbb/be | RECLASSIFIED — receiver is the CAND-4 child-family object | Committed (PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007/01_RAW/FUN_006C8F80_BASECTOR_DECODE.txt). Different class; no CMO relation. |
| C-O | FUN_006C94FF `89 46 44` (ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt) | RECLASSIFIED — request-queue family store; receiver is not the CMO instance in the committed census context | PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915 census of the 0x00BA921C globals triple; unrelated receiver. |
| C-P | STATIC_INSTANCE_TRACE S5_TRANSFORM_WRITES windows `89 46 44/48/4C...` | RECLASSIFIED — bulk zero-inits in OTHER classes' ctors (their own vtables 0x00A814A4/0x00A81544/0x00A815FC/0x00A89DFC families) | Transform-object family, not the CMO instance. |

Summary-level committed claims pointing at the C-A/B/C family (context, not
independent instruction evidence): PE_935_ATTRIBUTE_ORIGIN_SEAM REPORT S9
("[+0x44..0x4C]=[record+8..0x10] (FUN_00746560)"), RESEARCH_FINDINGS (c);
PE_935_POSITION_CONSTRUCTION_CORRECTIONS REPORT.md §4.1 item 4 + line 197 +
ERRATA_R5 line 44; MICRO_R1 INPUT_IDENTITIES.md line 30 ("(+0x44..0x4C
position)" — historical label with the seam's own axes/units-UNRESOLVED
caveats; NOT promoted by this run).

NEGATIVE RESULT within the boundary: NO OTHER committed-evidence store to the
CMO-family instance +0x44/+0x48/+0x4C exists beyond the six records in §3.1.
The derived ctor FUN_00528E50 contains none; the documented CMO-instance
stores are at +0xC0 and +0xB4 (C-H/C-I) plus the base-ctor family §3.1.

## 4. Selection under the pre-registered rule

Rule (PREREGISTRATION §4): prefer physical-byte-supported exact store with
receiver lineage; if genuinely tied, lowest exact verified VA; do not
manufacture a candidate from the label CMO or three adjacent numerical offsets.

1. All six §3.1 records are exact stores with physical byte support and the
   same receiver lineage (same body, same ESI=this chain).
2. The zero-init family (C-D/C-E/C-F) is ranked BELOW the copy family: its
   three members are the first three of a BULK 12-field float-zero sequence
   (+0x44..+0x70) — selecting them would be manufacturing an anchor from
   three adjacent numerical offsets; its immediate value source is a degenerate
   CONSTANT (fldz) with no producer chain; and it is overwritten by the copy
   family later in the SAME straight-line construction sequence (no branch
   between 0x0085B1E4 and 0x0085B281 in the committed decode).
3. The record-copy family (C-A/C-B/C-C) is the value-determining write group
   matching the committed claims and carrying a real in-body producer chain.
   Within it the members are genuinely tied -> lowest exact verified VA.

**SELECTED: C-A — store VA 0x0085B281, bytes `89 4E 44`,
`mov dword ptr [esi+0x44], ecx`, in FUN_0085B1B0 (function start 0x0085B1B0),
destination = [esi+0x44] where ESI = the ctor `this` (the
MovableObject-under-construction that FUN_00528E50 turns into a
ClientMovableObject).**

The strictly-mechanical alternative (zero-init C-D @0x0085B1E4 with a
CONSTANT source) was pre-registered and rejected for the documented reasons
(PREREGISTRATION §4.3); the full census preserves it for independent
re-adjudication.

## 5. Selection status

ANCHOR_DISCOVERY = SUFFICIENT (one defensible candidate with an exact store
VA exists in the permitted committed evidence). Next step per contract §5:
physical re-pin from the pinned EXE through the Source-B range-safe reader +
independent boundary decode (falsifiers F1/F2 active). No EXE-wide writer
discovery was performed or initiated.
