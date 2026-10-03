# TEMPLATE ROLE TEST — MANDATORY FALSIFIER — PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003

Executor: pe-reconstruction. STATIC_ONLY.

## 1. THE FALSIFIER (contract §4, verbatim meaning)

If immediate 4057 at/around 0x0059AB12 does NOT reach FUN_0072F580 or another
independently proven template-id consumer, then IMMEDIATE_4057_IS_TEMPLATE_ID =
REJECTED_FOR_THIS_CALLSITE, HARDCODED_TEMPLATE_REFERENCE_4057 = NOT_ESTABLISHED,
NUMERIC_MATCH_4057 = COINCIDENCE_OR_UNRESOLVED, and the run MUST NOT continue
pretending 0x0059AB12 constructs template 4057.

## 2. WHAT THE PROVEN TEMPLATE-ID CONSUMER ABI IS (canon, context only)

Registry lookup FUN_0072F580: thiscall, ECX = registry_this (singleton getter
FUN_0043A550, registry tree DAT_00BA1824), id2 = stack argument, RET 4; used by
the {0x66=MODEL, A} emitter FUN_006C3F50 with A-read getter FUN_007CE1E0
([this+8]) (record-bridge E2/E3 + desktop-correction F-D2 ABI). Any honest PASS
would require this ABI (or an independently proven alternative consumer) on the
4057 path.

## 3. EXECUTION — the measured 4057 path (details: CALLSITE_DATAFLOW.md §3)

```text
4057 -> this->FUN_008DFCD0 (stack arg, this = ArkRepairUI stack-local object)
     -> 0x1C string-table singleton (FUN_00414170, @DAT_00BA124C — NOT the
        registry singleton DAT_00BA1824; different global, different getter)
     -> singleton->FUN_00821BB0(&out_str, 4057, &struct)
     -> FUN_00821760(0, 4057, &out)
     -> 0x98-manager singleton (FUN_00415670, @DAT_00BA12F4)
     -> mgr->FUN_00823C10(key{section_object, 4057})
        -> GENERIC STL RB-tree mapfind FUN_004D1430 (mgr's own map @[this+4])
        -> string from [entry chain] -> out
     -> this->FUN_008DFB70(&str) (ArkUI::Component-family store)
```

## 4. REACH-CHECK ARTIFACT (01_RAW/FALSIFIER_REACH_CHECK.json, regenerated over g1..g6 — R1 amend)

All 18 functions measured this run (full listings + callee sets) tested for
direct calls to the fixed canon machinery VA set
{FUN_0072F580, FUN_0043A550, FUN_0072FA30, FUN_00730C90, FUN_007CE1E0,
FUN_004D1430, FUN_0072F8D0, FUN_006C3F50, FUN_008BD720, FUN_0072FE30}:

```text
G1_FUN_00599d30 (177 call sites)      : 0 hits
G2_FUN_008dfcd0 / 008f0780 / 008e7b80
    / 008df3f0 / 008df310             : 0 hits
G3_FUN_00414170 / 00821bb0 / 008dfb70
    / 008f01c0 / 0059be70             : 0 hits
G4_FUN_00821760 / 008221c0            : 0 hits
G5_FUN_00826a50 / 00415670 / 00823c10
    / 00821fb0                        : 1 x FUN_004D1430 (see below)
G6_FUN_00821e70                       : 0 hits (row regenerated into the
                                          artifact by the R1 script — the
                                          original artifact shipped without
                                          G5/G6 rows; see RETRACTIONS R-2)

TOTAL: 18 functions checked; 1 generic-machinery hit; 0 template-registry
edges (row-consistent with the regenerated artifact; QC independently
measured the same single hit over 18 windows — 04_QC Q8).
```

**The single machinery-adjacent hit is FUN_004D1430 called by FUN_00823C10
@0x00823C57.** FUN_004D1430 is the GENERIC STL RB-tree mapfind primitive
shared by many maps (the template registry lookup FUN_0072F580 also calls it —
record-bridge E2). It is NOT a template-id consumer:

```text
- different object: the tree walked is the 0x98-manager's own map @[mgr+4],
  not the registry tree rooted at DAT_00BA1824;
- different singleton path: FUN_00415670/DAT_00BA12F4, not
  FUN_0043A550/DAT_00BA1824;
- different key: composite {section_object, 4057}, not a bare id2;
- different value type: string-table entries, not 12-u32 template objects
  {id2,B,A,C,D,list1,list2,f11};
- FUN_0072F580 itself (the only independently proven template-id consumer) is
  called by NOTHING on the 4057 path.
```

## 5. STRUCTURAL COINCIDENCE TEST (data side; CONTROL-1/CONTROL-2 material)

templates.vfs record id2=4057 physically exists (Phase 1: record @88,792,
A=218757, B=218758 — CONFIRMED). But the anchored immediate is one of a
CONSECUTIVE SERIES consumed identically by the same function, and the series is
NOT a run of templates id2 (01_RAW/SIDS_REPINS.json templates_series_census +
SIDS_ENTRY_PARSE.json):

```text
value   as sids.vfs string id (measured)      as templates.vfs id2 (measured)
0xFD4   S_REPAIR_UI_ADD_EQUIPPED_TOOLTIP      ABSENT
0xFD5   S_REPAIR_UI_ADD_WEAPONS_TOOLTIP       ABSENT
0xFD6   S_REPAIR_UI_ADD_ARMOR_TOOLTIP         PRESENT (id2=4054)
0xFD7   S_REPAIR_UI_ADD_TOOLS_TOOLTIP         ABSENT
0xFD8   S_REPAIR_UI_ADD_ALL_TOOLTIP           ABSENT
0xFD9   S_REPAIR_UI_CLEAR_TOOLTIP             PRESENT (id2=4057)  <- the anchor
0x376   S_GENERIC_CLEAR                       ABSENT
```

The code treats all six series members as the same value class (same PUSH ->
same callee FUN_008DFCD0, same arg1 class — but NOT byte-identical call
shapes: 0xFD4..0xFD8 pass this = LEA ECX,[ESP+0x2C] while the 0xFD9 anchor
passes this = LEA ECX,[ESP+0xC8] — same callee/argument shape, different
this-pointer slots; s4 windows). Four of the six are
NOT templates id2 at all; the two overlaps (4054, 4057) are numeric coincidence
between two independent id spaces (sids string ids vs. templates id2). The
sibling series shows the same effect: 0xFAE..0xFB2 are BOTH repair-UI label sids
AND templates id2 values — cross-file numeric overlap is common and carries no
identity.

## 6. VERDICT

```text
IMMEDIATE_4057_IS_TEMPLATE_ID = REJECTED_FOR_THIS_CALLSITE
HARDCODED_TEMPLATE_REFERENCE_4057 = NOT_ESTABLISHED
NUMERIC_MATCH_4057 = COINCIDENCE_OR_UNRESOLVED
MANDATORY_FALSIFIER_RESULT = FAIL_NUMERIC_COINCIDENCE
STOP CONDITION S2 FIRED (contract §24): 4057 does not reach a proven
template-id consumer; the landmark construction path is NOT continued.
```

Per contract §31 this is a FULL-VALUE negative result. The measured positive
identification at this call-site: 4057 = sids.vfs string-table entry id
`S_REPAIR_UI_CLEAR_TOOLTIP` (data side CONFIRMED by exact-closure parse of the
physical sids.vfs payload under the code-measured layout), consumed by the
ArkRepairUI construction path.

The physical templates.vfs record 4057 (A=218757, B=218758) remains a valid
DATA-side fact (Phase 1 CONFIRMED) — but it is NOT connected to VA 0x0059AB12 by
any code path measured this run. Per contract §31 the run does NOT search for
another 4057 call-site (that would be a separate future experiment).
