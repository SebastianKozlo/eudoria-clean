# OBJECT IDENTITY TRACE — PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003

Executor: pe-reconstruction. STATIC_ONLY.

## 1. Contract phase discipline

Contract Phase 8 (object identity) executes ONLY if the template→model bridge
passes (Phase 6/7). The mandatory falsifier fired at Phase 5 (see
TEMPLATE_ROLE_TEST.md): there is NO template/model/landmark construction path at
0x0059AB12. Therefore NO world-instance object identity is claimed and NONE was
traced further. This file records ONLY the object facts measured on the
falsifier path itself (all needed to classify the immediate's role), not a
landmark instance chain.

## 2. Measured objects on the 4057 consumption path

```text
O1  FUN_00599D30 stack-local object @ [ESP+0xC8]-class frame slot
    - base pointer: stack address (LEA ECX,[ESP+0xC8] @0x0059AB17, post-push base)
    - class: NOT independently identified (no vtable store of its own measured;
      it is the owner/container on which FUN_008DFCD0/FUN_008E7B80/FUN_008F0780
      operate). Bounded working context: it belongs to the ArkRepairUI
      construction path (caller RTTI gate: ArkRepairUI_Impl type check before
      FUN_00599d30 is invoked — 01_RAW/G3_DECOMPILE_E05_caller_0059be70_0059BE70.c).
    - role of O1 at the anchor: `this` of this->FUN_008DFCD0(4057).

O2  0x1C string-table singleton @ DAT_00BA124C
    - created by FUN_00414170 (lazy get-or-create: operator new(0x1C) via thunk
      0x0095D3C4, ctor FUN_008221C0 @0x004141B6, store @0x004141BB); NOT the
      template registry singleton (DAT_00BA1824 via FUN_0043A550).
    - FUN_008221C0 (g4): plain struct init (zero fields + self-linked list/tree
      at +4..+0x14) + CALL FUN_00821FB0; no vtable -> non-polymorphic.
    - FUN_00821FB0 (g5): opens "parameters\\sids.vfs", reads the record
      (FUN_00971ad0 family), calls FUN_00821E70 to parse entries into the map.
    - role of O2 in the chain: `this` of singleton->FUN_00821BB0(&str, 4057, &s).

O3  0x98 manager singleton @ DAT_00BA12F4
    - created by FUN_00415670 (lazy get-or-create: operator new(0x98), ctor
      FUN_00824C70 @0x004156B9, store @0x004156BE); the ctor FUN_00824C70 was
      NOT measured (NOT_CHECKED).
    - role of O3: `this` of mgr->FUN_00823C10(key{section, 4057}) — walks its
      own RB-tree map @[this+4] via the GENERIC mapfind FUN_004D1430
      @0x00823C57; node value slot at node+0x14; entry chain through
      [entry+0x24] virtual dispatch; result string at +0x10.

O4  ArkUI::Component-family temp object in FUN_008DFB70
    - vtable store: MOV dword ptr [ESP+0x3C], 0x00A7A948 @0x008DFBD0
      (raw bytes C7 44 24 3C 48 A9 A7 00); Ghidra RTTI analyzer labels
      0x00A7A948 as ArkUI::Component::vftable (binary RTTI symbol).
    - role of O4: the sub-component that receives the resolved string
      ("add component with text" style store). The class LABEL is
      Ghidra-RTTI-derived (STRONGLY_SUPPORTED); an independent vtable-4 ->
      COL -> TD chain walk was NOT performed this run (NOT_CHECKED). R1 AMEND
      NOTE: QC's independent chain walk CONFIRMS the chain-walk fact — vtable
      0x00A7A948 -> COL 0x00A9EDD4 -> TD 0x00B6E084 = '.?AVComponent@ArkUI@@'
      (04_QC/TARGETED_QC_REPORT.md Q6). Executor + QC agree on the chain-walk
      fact; class BEHAVIORAL identity remains exactly as before (not upgraded
      to behavioral semantics).
```

## 3. Caller-path identity (context for the containing function)

```text
FUN_0059BE70 (sole caller of FUN_00599D30, call site 0x0059BF11):
  - stores ArkRepairUI::vftable in its unwind local (Ghidra RTTI label);
  - compares the object's RTTI Type Descriptor against
    ArkRepairUI_Impl::RTTI_Type_Descriptor (binary RTTI symbol);
  - on match calls FUN_00599d30() (and siblings FUN_0059ba40, FUN_004d9dc0,
    FUN_004143f0, FUN_0042bc30).
  => FUN_00599D30 executes inside the RTTI-gated ArkRepairUI initialization.
```

R1 AMEND NOTE: QC's independent RTTI chain walks (04_QC/TARGETED_QC_REPORT.md
Q6) CONFIRM the caller-side chain-walk facts: gate Type Descriptor 0x00B7DDE8
= '.PAVArkRepairUI_Impl@@' (pointer-form TypeDescriptor of ArkRepairUI_Impl);
unwind-store vtable 0x00A80704 -> COL 0x00AA276C -> TD 0x00B7DED8 =
'.?AVArkRepairUI@@'. Executor + QC agree on the chain-walk facts; class
BEHAVIORAL identity remains exactly as before (labels stay RTTI-symbol
readings; not upgraded to behavioral semantics).

## 4. Required statuses

```text
SAME_RUNTIME_OBJECT_IDENTITY (construction->transform, landmark instance) =
NOT_ESTABLISHED — and NOT PURSUED: there is no construction->transform path on
this call-site; the measured objects are UI-side and no world instance exists
on the path.
CONCRETE_RUNTIME_INSTANCE = NOT_ESTABLISHED (no landmark instance; the UI
objects above are identified only as measured, not as world placements).
STATIC_BUILDING_INSTANCE = REJECTED_FOR_THIS_CALLSITE (the 0x0059AB12 chain
builds ArkRepairUI string labels, not a static building; the human's
HUMAN_HISTORICAL_RECOLLECTION about model 218757 was a probe-selection
criterion only and is untouched by this result).
```
