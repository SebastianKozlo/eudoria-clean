# CLASS_HIERARCHY_AND_VTABLE_MAP — GB 1.1.2 and GB 1.2.2.6 (Question A)

Two INDEPENDENT methods were used and they AGREE for every class in both versions:

- **Method 1 — inheritance-aware header reconstruction.** MSVC lays out the primary
  vtable as: slot 0 = vector deleting destructor (`??_E...`; the scalar deleting dtor is
  not a vtable entry on x86), then every NEW virtual in declaration order, base-most
  class first; overrides occupy the base's slot. The declaration order was recovered from
  the pinned headers (including macro-expanded virtuals from `NiDeclareRootRTTI` /
  `NiDeclareRTTI` (GetRTTI), `NiDeclareClone[s]` (CreateClone), `NiDeclare[Abstract]Stream`
  (LoadBinary/LinkObject/RegisterStreamables/SaveBinary/IsEqual), `NiDeclare[Abstract]ViewerStrings`
  (GetViewerStrings)) — see `01_RAW/GB112_SOURCE_LOCATORS.md` and `01_RAW/GB12_SOURCE_LOCATORS.md`
  for line numbers.
- **Method 2 — compiled relocation evidence.** `??_7<Class>@@6B@` vtable symbols were
  extracted from the pinned COFF build products and each slot mapped to its relocated
  MSVC symbol via the section relocation tables (`00_Control/parse_coff_vtable.py`;
  dumps in `03_EVIDENCE/GB112_NIMAIN_LIB_VTABLE_DUMP.json`,
  `03_EVIDENCE/GB12_NINODE_OBJ_VTABLE_DUMP.json`,
  `03_EVIDENCE/GB12_CHAIN_OBJ_VTABLE_DUMP.json`).

No naive header counting was relied on where overrides were in play; the two methods
converge on identical maps.

## Inheritance chain (identical in both versions; also independently confirmed in
Entropia by RTTI walk — `03_EVIDENCE/ENTROPIA_RTTI_CHAIN_PROBE.json`)

`NiRefObject -> NiObject -> NiObjectNET -> NiAVObject -> NiNode`

## GB 1.1.2 vtable map (compiled NiMain.lib VC71 ReleaseLib)

| Slot | NiRefObject | NiObject | NiObjectNET | NiAVObject | NiNode |
|---|---|---|---|---|---|
| 0 | ??_E dtor | ??_E dtor | ??_E dtor | ??_E dtor | ??_E dtor |
| 1 | — | GetRTTI | GetRTTI | GetRTTI | GetRTTI |
| 2 | — | CreateClone | CreateClone(NiObject) | CreateClone(NiObject) | CreateClone |
| 3 | — | LoadBinary | LoadBinary | LoadBinary | LoadBinary |
| 4 | — | LinkObject | LinkObject | LinkObject | LinkObject |
| 5 | — | RegisterStreamables | RegisterStreamables | RegisterStreamables | RegisterStreamables |
| 6 | — | SaveBinary | SaveBinary | SaveBinary | SaveBinary |
| 7 | — | IsEqual | IsEqual | IsEqual | IsEqual |
| 8 | — | GetViewerStrings | GetViewerStrings | GetViewerStrings | GetViewerStrings |
| 9 | — | AddViewerStrings | AddViewerStrings(NiObject) | AddViewerStrings(NiObject) | AddViewerStrings(NiObject) |
| 10 | — | ProcessClone | ProcessClone | ProcessClone | ProcessClone |
| 11 | — | PostLinkObject | PostLinkObject | PostLinkObject(NiObjectNET) | PostLinkObject(NiObjectNET) |
| 12 | — | GetBlockAllocationSize | GetBlockAllocationSize(NiObject) | GetBlockAllocationSize(NiObject) | GetBlockAllocationSize(NiObject) |
| 13 | — | — | — | **UpdateControllers** | UpdateControllers |
| 14 | — | — | — | **UpdateNodeBound** | UpdateNodeBound |
| 15 | — | — | — | **ApplyTransform** | ApplyTransform |
| 16 | — | — | — | **GetObjectByName** | **GetObjectByName** |
| 17 | — | — | — | **SetSelectiveUpdateFlags** | **SetSelectiveUpdateFlags** |
| 18 | — | — | — | UpdateDownwardPass | UpdateDownwardPass |
| 19 | — | — | — | UpdateSelectedDownwardPass | UpdateSelectedDownwardPass |
| 20 | — | — | — | UpdateRigidDownwardPass | UpdateRigidDownwardPass |
| 21 | — | — | — | UpdatePropertiesDownward | UpdatePropertiesDownward |
| 22 | — | — | — | UpdateEffectsDownward | UpdateEffectsDownward |
| 23 | — | — | — | Display | Display |
| 24 | — | — | — | PurgeRendererData | PurgeRendererData |
| 25 | — | — | — | UpdateWorldBound (protected, declared after members) | UpdateWorldBound |
| 26 | — | — | — | UpdateWorldData (protected, declared after members) | UpdateWorldData(NiAVObject) |
| 27 | — | — | — | — | **AttachChild** |
| 28 | — | — | — | — | DetachChild |
| 29 | — | — | — | — | DetachChildAt |
| 30 | — | — | — | — | SetAt |
| 31 | — | — | — | — | UpdateUpwardPass |

Slot counts: NiRefObject 1 (dtor only; compiled `??_7NiRefObject@@6B@` has exactly 1 slot),
NiObject 13, NiObjectNET 13 (no new virtuals), NiAVObject 27, NiNode 32.

**GB 1.1.2 NiNode slot 17 = `NiNode::SetSelectiveUpdateFlags(bool&, bool, bool&)`**
(mangled `?SetSelectiveUpdateFlags@NiNode@@UAEXAA_N_N0@Z` — measured at slot 17 of the
compiled vtable). GetObjectByName is slot **16**; ApplyTransform is slot **15**.

## GB 1.2.2.6 vtable map (compiled gb12_build .obj)

Identical to 1.1.2 up to slot 12, then (exact per-slot symbols from the JSON dumps):

| Slot | NiObject (delta) | NiObjectNET | NiAVObject | NiNode |
|---|---|---|---|---|
| 13 | **GetGroup (NEW virtual in 1.2.2.6)** | GetGroup(NiObject) | UpdateControllers | UpdateControllers |
| 14 | **SetGroup (NEW virtual in 1.2.2.6)** | SetGroup(NiObject) | UpdateNodeBound | UpdateNodeBound |
| 15 | — | — | UpdateControllers | UpdateControllers |
| 16 | — | — | UpdateNodeBound | UpdateNodeBound |
| 17 | — | — | **ApplyTransform** | **ApplyTransform** |
| 18 | — | — | **GetObjectByName** | **GetObjectByName** |
| 19 | — | — | SetSelectiveUpdateFlags | SetSelectiveUpdateFlags |
| 20 | — | — | UpdateDownwardPass | UpdateDownwardPass |
| 21 | — | — | UpdateSelectedDownwardPass | UpdateSelectedDownwardPass |
| 22 | — | — | UpdateRigidDownwardPass | UpdateRigidDownwardPass |
| 23 | — | — | UpdatePropertiesDownward | UpdatePropertiesDownward |
| 24 | — | — | UpdateEffectsDownward | UpdateEffectsDownward |
| 25 | — | — | UpdateWorldData | UpdateWorldData |
| 26 | — | — | UpdateWorldBound | UpdateWorldBound |
| 27 | — | — | Display | Display |
| 28 | — | — | PurgeRendererData | PurgeRendererData |
| 29..33 | — | — | — | AttachChild, DetachChild, DetachChildAt, SetAt, UpdateUpwardPass |

(Note: in 1.2.2.6 `UpdateWorldData`/`UpdateWorldBound` are public-declared (header L161-162)
and occupy 25/26, whereas 1.1.2 declares them protected-after-members in slots 25/26 in the
opposite order — UpdateWorldBound then UpdateWorldData; both orders are directly visible in
the respective JSON dumps. The prose table above is a guide; the JSON dumps are the record.)

Slot counts: NiObject 15, NiObjectNET 15, NiAVObject 29, NiNode 34.

**GB 1.2.2.6 NiNode slot 17 = `NiNode::ApplyTransform(const NiMatrix3&, const NiPoint3&, bool)`**
(mangled `?ApplyTransform@NiNode@@UAEXABVNiMatrix3@@ABVNiPoint3@@_N@Z` — measured at
slot 17 of the compiled vtable). GetObjectByName is slot **18**; ApplyTransform slot **17**.

## The 1.1.2 -> 1.2.2.6 delta (NC2 subject)

The +2 shift for all NiAVObject-introduced ordinals is caused by exactly two virtuals:
`NiObject::GetGroup` and `NiObject::SetGroup`, which are NON-virtual in 1.1.2
(`NiObject.h` L53-54) and VIRTUAL in 1.2.2.6 (`NiObject.h` L59-60). In 1.2.2.6 the group
pointer was REMOVED from NiObject storage (`NiObject.cpp` L53-62: GetGroup returns NULL,
SetGroup is a no-op, "The object group is no longer stored in NiObject"). Therefore:

| Method identity | GB 1.1.2 slot | GB 1.2.2.6 slot |
|---|---|---|
| ApplyTransform | 15 | 17 |
| GetObjectByName | 16 | 18 |
| SetSelectiveUpdateFlags | 17 | 19 |

**Vtable numbering DOES differ between the two pinned oracles.** Any slot-number-based
transfer between versions is therefore invalid (see NEGATIVE_CONTROLS.md NC2).

## NiNode neighborhood (search/lookup/transform/child methods)

- Named lookup virtuals: `GetObjectByName` (both versions; the only name-search virtual
  in the chain). Non-virtual lookups nearby in the headers but NOT vtable entries:
  `NiObjectNET::GetExtraData(const char*)` (binary search by strcmp),
  `NiObjectNET::GetName()`, `NiAVObject::GetProperty(int)`, `NiNode::GetAt(unsigned)`,
  `NiNode::GetChildCount()`, `NiNode::GetArrayCount()`.
- Transform/update virtuals around the target ordinal: UpdateControllers, UpdateNodeBound,
  ApplyTransform, GetObjectByName, SetSelectiveUpdateFlags, UpdateDownwardPass,
  UpdateSelectedDownwardPass, UpdateRigidDownwardPass (both versions; see maps above).
- Child mutation virtuals (NiNode-only): AttachChild, DetachChild, DetachChildAt, SetAt
  (slots 27-30 in 1.1.2; 29-32 in 1.2.2.6); child read access `GetAt` is NON-virtual.

## Entropia side (measured, for contrast)

Entropia NiNode primary vtable (VA 0x00A8CCF4, MSVC RTTI `.?AVNiNode@@`, base chain
identical) has **47 slots (0..46)** — its ABI matches NEITHER pinned oracle (both
smaller: 32 / 34). Slot 17 (+0x44) = 0x007B5390. Full slot list:
`03_EVIDENCE/ENTROPIA_RTTI_CHAIN_PROBE.json`.

**Measured vtable ABI prefix (this run, `03_EVIDENCE/ENTROPIA_SLOT_NEIGHBORS_DISASM.txt`
+ `ENTROPIA_NIRTTI_STATIC_INIT.txt`):** slot 0 = vector deleting dtor (0x0082E420;
dtor body 0x7B60D0, operator delete 0x95D42A, flags&1), slot 1 = scalar deleting dtor
thunk (0x00406D50; `vtable[0](this,1)`), slot 2 = GetRTTI (0x007B60C0 ->
&NiNode::ms_RTTI 0x00BA7218; proven by the static initializer
`NiRTTI(0x00BA7218, "NiNode"@0x00A8CE00, 0x00BA7270 /*NiAVObject*/)` at 0x00A6C200).
Both oracles put GetRTTI at slot 1 with a SINGLE `??_E` dtor slot, so Entropia carries
ONE EXTRA dtor-related slot; under that measured +1 shift, the decoded neighbor slots
16 (transform applier, GB112@15 ApplyTransform-shaped), 17 (recursive named lookup,
GB112@16 GetObjectByName-shaped), 18 (selective-update flags with the GB SELECTIVE_*
masks, GB112@17 SetSelectiveUpdateFlags-shaped) and 27 (UpdateWorldData,
GB112@26, instruction-near-identical incl. collision dispatch +0x3C = 0x38+4) align
with the GB112 map.

The slot-17 identity in Entropia was NOT transferred by number (NC2 proves numbering
is version-specific; NC1 rejects both oracle slot-17 occupants); it was determined
behaviorally from Entropia bytes — 0x007B5390 is near-identical in compiled shape to
the era VC71 `?GetObjectByName@NiNode@@...` (same prologue/loop idiom, name at +0x0C
as in GB112, children array shape as in GB112 with a version-tail offset delta).
See ENTROPIA_SLOT17_FINGERPRINT.md. The engine GENERATION of Entropia's NiNode
(47 slots, children at +0xCC/+0xD4 vs GB112 +0xB8/+0xC0) is not determined by the
two pinned oracles — honest UNKNOWN on generation identity.
