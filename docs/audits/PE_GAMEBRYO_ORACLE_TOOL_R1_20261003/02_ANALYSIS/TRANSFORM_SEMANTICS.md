# TRANSFORM_SEMANTICS — PE_GAMEBRYO_ORACLE_TOOL_R1_20261003 (Batch E1, order s14)

Source-derived contracts only. NO Entropia.exe matching was performed (s14
binding); the optional machine-shape signature file is E2 scope. "Offsets"
column: only offsets DETERMINABLE FROM SOURCE (field order comments) are given —
no binary measurements were made in E1.

## NiAVObject::SetTranslate

| | GB_1_1_2 | GB_1_2 | GB_2_6 |
|---|---|---|---|
| Source file | SDK\Win32\Include\NiAVObject.inl (sha D45FDDE07BF70C986EECA82087929B0081923F3D7EDEAA2C417690539C7971D5) | CoreLibs\NiMain\NiAVObject.inl (sha 09E1A5A5C88AF503D9566B487941305307CBA5CB1513147FB49E5A4DBDC91C3B) | Gb26_src\NiAVObject.inl (sha 44694841C4F993049BC7035727CCC4D46EDC4305219A9BBF1925D35A5938AB55) |
| Line | 77-80 (and 82-85 float x,y,z overload) | 82-85 (87-90 overload) | 92-95 (97-100 overload) |
| Contract | `m_kLocal.m_Translate = kTrn` (or NiPoint3(x,y,z)) — pure local-transform write | identical | identical |
| Input | const NiPoint3& / 3 floats | idem | idem |
| Output | void | idem | idem |
| State mutated | m_kLocal.m_Translate only | idem | idem |
| Calling shape | inline, no parent notification — world transform goes stale until Update | idem | idem |

## NiAVObject::SetRotate

| | GB_1_1_2 | GB_1_2 | GB_2_6 |
|---|---|---|---|
| Line (inl) | 92-95 (matrix), 102-105 (angle/axis), 118-121 (quat) | 97-100, 107-110, 123-126 | 107-110, 117-120, 133-136 |
| Contract | `m_kLocal.m_Rotate = kRot` / MakeRotation(angle,x,y,z) / kQuat.ToRotation(m_kLocal.m_Rotate) | identical | identical |
| State mutated | m_kLocal.m_Rotate only | idem | idem |

## NiAVObject::SetScale

| | GB_1_1_2 | GB_1_2 | GB_2_6 |
|---|---|---|---|
| Line (inl) | 130-138 | 135-143 | 145-153 |
| Contract | `assert(fScale >= 0.0f); m_kLocal.m_fScale = NiAbs(fScale);` — negative scale is NOT supported; sign is silently corrected (comment: negative scale "screws up bounding spheres") | identical | identical (NIASSERT) |
| State mutated | m_kLocal.m_fScale | idem | idem |
| Extra (2.x only) | — | — | SetLocalTransform (inl L205-215) + SetLocalFromWorldTransform (L217-232: parent world inverse * world) exist only in GB_2_6 |

## NiAVObject::UpdateWorldData

| | GB_1_2 | GB_2_6 |
|---|---|---|
| Source file | CoreLibs\NiMain\Win32\NiAVObject_Win32.cpp (platform implementation; whole file 31 lines + header block) | Gb26_src\NiAVObject_Win32.cpp (same structure) |
| Line | 22-31 | 22-31 |
| Contract (verbatim, identical both) | `if (m_pkParent) m_kWorld = m_pkParent->m_kWorld * m_kLocal; else m_kWorld = m_kLocal; if (m_spCollisionObject) m_spCollisionObject->UpdateWorldData();` |
| Input | none (uses m_pkParent, m_kLocal) | idem |
| Output | void | idem |
| State mutated | m_kWorld; collision object's world data | idem |
| Calling shape | virtual; called from UpdateDownwardPass AFTER controller update and BEFORE UpdateWorldBound (NiAVObject.cpp GB12 L118-136 esp. L128-132; GB26 L174-182) — downward pass order: controllers -> UpdateWorldData -> UpdateWorldBound | idem (GB26 L180-181) |
| GB_1_1_2 | declaration only (binary SDK): NiAVObject.h line 245 `virtual void UpdateWorldData();` (sha 3FC6C7101EC816EE27E116D495CF5A1E292F4AE261A0E9BFE58DBB6BCA99E6B6) |
| Field-order note (GB112/GB12 NiAVObject.h L232-239) | "Variable declarations whose order effects assembly language code begin here": CopyTransforms, NiTransform m_kLocal; NiTransform m_kWorld — source-comment evidence that m_kLocal precedes m_kWorld in the object layout (exact offsets NOT measured — E2 optional) |

## NiNode::AttachChild

| | GB_1_2 | GB_2_6 |
|---|---|---|
| Source file | CoreLibs\NiMain\NiNode.cpp (sha 38C7A1DE...) | Gb26_src\NiNode.cpp (sha C0414C8F...) |
| Line | 52-72 | 54-74 |
| Contract (identical logic) | `assert(pkChild); if (!pkChild) return; pkChild->IncRefCount(); pkChild->AttachParent(this); bFirstAvail ? m_kChildren.AddFirstEmpty(pkChild) : m_kChildren.Add(pkChild); assert(refcount >= 2); pkChild->DecRefCount();` |
| Input | NiAVObject* child, bool bFirstAvail=false | idem |
| Output | void | idem |
| State mutated | child->m_pkParent; m_kChildren array; transient refcount | idem |
| Calling shape | NOT called during NIF load (children link via NiNode::LinkObject -> SetAt, NiNode.cpp GB12 L886-888) — runtime scene assembly | idem |
| GB_1_1_2 / GB_2_3 | declarations only: GB112 NiNode.h (installed, NiNode.inl sha 0C1E5765... companion) / GB23 recovered NiNode.h L40 `virtual void AttachChild(NiAVObject* pkChild, bool bFirstAvail = false);` (sha 8C4D29D6...) |

## NiNode::DetachChild / DetachChildAt

| | GB_1_2 | GB_2_6 |
|---|---|---|
| Line | DetachChildAt 74-90; DetachChild 92-106 | 76-92; 94-108 |
| Contract | linear scan for the child; on match: child->DetachParent(); m_kChildren.RemoveAt(i); returns NiAVObjectPtr (null if absent) | identical |
| State mutated | child->m_pkParent = 0 (DetachParent inl GB112 L17-20); m_kChildren | idem |

## NiNode::SetAt

| | GB_1_2 | GB_2_6 |
|---|---|---|
| Line | 108-130 | 110-132 |
| Contract | if i beyond size: grow + AttachParent; else detach former child, attach new, `m_kChildren.SetAt(i, pkChild)`; returns former child (NiAVObjectPtr) | identical |
| Load-time role | THIS is how loaded children are attached: NiNode::LinkObject resolves ReadMultipleLinkIDs entries via GetObjectFromLinkID then SetAt (GB12 L886-888) | GB26 identical link flow (GetObjectToLinkID null-safety added in the stream loop, not in SetAt) |

## NiStream load / link / postlink (per-block orchestration)

| Aspect | GB_1_2 (NiStream.cpp sha E955C36E) | GB_2_6 (sha 72781EEB) |
|---|---|---|
| Load entry | L637-660 (file) / L662-670 (memory) / L672-689 (stream) -> LoadStream L521-635 | same spine L795-950 |
| header | LoadHeader L303-360; gate [3.3.0.11, 10.2.0.0] | L374-467; gate [10.1.0.114, 20.6.0.0] + endian |
| object create | LoadRTTI L415-449 (unknown class -> RTTIError -> FAIL) | L630-683 (skippable unknowns for >= 20.2.0.5, SKIPPABLE_MASK 0x8000) |
| LoadBinary loop | L538-564: `pkObject->LoadBinary(*this)` per object, in block order, single pass | L823-877 (+ size-table Seek for skipped NULLs L855-867) |
| link phase | L568-578: `pkObject->LinkObject(*this)` per object, in block order | L881-889 (GetObjectToLink null-safe) |
| postlink phase | L580-590: `pkObject->PostLinkObject(*this)` per object | L893-904 |
| post process + old-version fixup | L602-622 (registered PostProcessFunctions); L630 + L821-841 SetSelectiveUpdateFlagsForOldVersions ONLY for v < 4.1.0.12 (TTTF recursive on roots) | present in 2.6 source at same conceptual place (2.x constants; for 10.1.0.0-relevant flow see NIF_LOAD_PIPELINE) |

## Claim discipline notes (s26/s27)

- FUNCTION_IDENTITY: all functions above are identified by source (class::name +
  file + line + file SHA256). OBSERVED_OPERATION: the quoted bodies. FINAL_
  SEMANTIC_ROLE: transform/attachment contracts as stated.
- No claim here says Entropia/PCG uses any of these implementations — the
  source-exists != engine-uses-it anti-overclaim applies until build
  correspondence is established (E2+).
- SERIALIZED_LOCAL_TRANSFORM (m_kLocal, from file bytes) vs COMPUTED_WORLD_
  TRANSFORM (m_kWorld, from UpdateWorldData) are kept distinct throughout; a
  computed world transform is NEVER a Eudoria world position.
