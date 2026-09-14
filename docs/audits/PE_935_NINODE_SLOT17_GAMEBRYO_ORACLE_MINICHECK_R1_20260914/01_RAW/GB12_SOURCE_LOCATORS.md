# GB12_SOURCE_LOCATORS — Gamebryo 1.2.2.6 (semantic source oracle + compiled build products)

All paths physical on this host; all files read-only. SHA256 = full-file SHA256,
measured in this run via Get-FileHash. Two mutually independent evidence classes
exist for 1.2.2.6: the SOURCE tree (`D:\gamebyroengine\extracted\Gb12_Source\`)
and the COMPILED COFF build products
(`D:\gamebyroengine\extracted\gb12_build\build\NiMain\*.obj`).

## Chain headers and sources

| File | SHA256 | Relevant content (line numbers, 1-based) |
|---|---|---|
| `D:\gamebyroengine\extracted\Gb12_Source\CoreLibs\NiMain\NiRefObject.h` | `FE0AFED5FD8EE16D7739F02A264276D04D3F1ED3C8096FD129AD088414BC08C7` | virtual dtor; `m_uiRefCount` (only virtual = dtor; only member = refcount; same shape as 1.1.2) |
| `...\CoreLibs\NiMain\NiObject.h` | `04C39E34A6066689D6DAF09FE2A71E85DC43973BFC0C6D80AE34338D9B57B9D1` | macros L32-35 + inline virtual `AddViewerStrings` L36; virtual dtor L40; `ProcessClone` L47-48; `PostLinkObject` L55; `GetBlockAllocationSize` L58; **`GetGroup` L59 and `SetGroup` L60 are VIRTUAL** — the +2 vtable shift vs 1.1.2; NO `m_pkGroup` member (removed from NiObject) |
| `...\CoreLibs\NiMain\NiObject.cpp` | `B137FE42126F496A37E7627061FF968256A6DA87D912784865609E2122FE470E` | L53-56 `NiObject::GetGroup()` returns NULL; L58-62 `NiObject::SetGroup()` no-op with the explicit comment "The object group is no longer stored in NiObject" — proves the 1.2.2.6 data-layout delta |
| `...\CoreLibs\NiMain\NiObjectNET.h` | `28FC01C19ECAAB27DFC0AC105F3ACEB9858BADA28961ECCAD31882CED3EF10A7` | adds NO new virtuals; members `m_pcName` L139, `m_spControllers` L140, `m_ppkExtra` L143, `m_uiExtraDataSize` L144, `m_uiMaxSize` L145 |
| `...\CoreLibs\NiMain\NiAVObject.h` | `A5B18264157CB1BB68D3DA6021DAEE91581D5E03F157E8536B9FCE5A79A985DD` | `NiDeclareFlags(unsigned short)` L46 (first data member `m_uFlags`); new virtuals in order: `UpdateControllers` L58, `UpdateNodeBound` L62, `ApplyTransform` L78-79, **`GetObjectByName` L100**, `SetSelectiveUpdateFlags` L134-135, `UpdateDownwardPass` L153, `UpdateSelectedDownwardPass` L154, `UpdateRigidDownwardPass` L155, `UpdatePropertiesDownward` L158, `UpdateEffectsDownward` L159, `UpdateWorldData` L161, `UpdateWorldBound` L162, `Display` L174, `ProcessClone` L180, `PurgeRendererData` L187; members `m_pkParent` L196, `m_kWorldBound` L225, `m_kLocal` L231, `m_kWorld` L232, `m_kPropertyList` L236, `m_spCollisionObject` L248 |
| `...\CoreLibs\NiMain\NiAVObject.cpp` | `72E0837149B03CCDA171BDF5E68E1E1F8C2712B2F10E7957AC3EC26344CA5EA7` | ctor L34-53 (member-init order confirms layout); **`NiAVObject::GetObjectByName` L423-432**; `CopyTransforms` L438-442 |
| `...\CoreLibs\NiMain\NiNode.h` | `2F81B261B5BA32FE176B891E800002657646C5927AFEC14F66B516893D9A0F9C` | NiNode new virtuals in order: `AttachChild` L41, `DetachChild` L42, `DetachChildAt` L43, `SetAt` L44, `ApplyTransform`(ovr) L48-49, **`GetObjectByName`(ovr) L58**, `UpdateControllers`(ovr) L63, `UpdateDownwardPass`(ovr) L64, `UpdateSelectedDownwardPass`(ovr) L65, `UpdateUpwardPass`(NEW) L66, `UpdateWorldBound`(ovr) L67, `UpdateRigidDownwardPass`(ovr) L68, `UpdateNodeBound`(ovr) L69, `UpdatePropertiesDownward`(ovr) L75, `UpdateEffectsDownward`(ovr) L76, `Display`(ovr) L79, `SetSelectiveUpdateFlags`(ovr) L90-91, `PurgeRendererData`(ovr) L94, `ProcessClone`(ovr) L96; members `m_kChildren` L105, `m_kEffectList` L108, `m_kBound` L119 |
| `...\CoreLibs\NiMain\NiNode.cpp` | `38C7A1DE1E166345068D296F70F34B1ADAE27C694E19EAD8FA0FBD8B62E0E016` | **`NiNode::GetObjectByName` L749-767** |

## GetObjectByName source bodies (1.2.2.6) — locators for the fingerprint

- `NiAVObject::GetObjectByName(const char* pcName)` — `NiAVObject.cpp` L423-432.
  Compact derived pseudocode (not a source dump):
  `if (pcName == 0 || GetName() == 0) return 0;`
  `if (strcmp(pcName, GetName()) == 0) return this;`
  `return 0;`
- `NiNode::GetObjectByName(const char* pcName)` — `NiNode.cpp` L749-767.
  Compact derived pseudocode:
  `obj = NiAVObject::GetObjectByName(pcName); if (obj) return obj;`
  `for (i = 0; i < m_kChildren.GetSize(); i++) { child = GetAt(i);`
  `  if (child) { obj = child->GetObjectByName(pcName); if (obj) return obj; } }`
  `return 0;`

## Value-type headers

| File | SHA256 | Facts |
|---|---|---|
| `D:\gamebyroengine\extracted\Gb12_Source\SDK\Win32\Include\NiTransform.h` | `EE758C5BA4130B8D8906011DA6BE08827F58B494DA7D23FA4C47F524E86F9B72` | data members L25-27 `NiMatrix3 m_Rotate; NiPoint3 m_Translate; float m_fScale;` — class block BYTE-IDENTICAL to GB112 |
| `...\SDK\Win32\Include\NiMatrix3.h` | `D974E2D03AEC9A0A8C2F27A4489C3D38C90520A71062859D1EE680AD8BC97792` | Win32 `float m_pEntry[3][3]` (36 bytes) |
| `...\SDK\Win32\Include\NiPoint3.h` | `218C2F27860D03C9642769DE0D5F3F6560BF240D11801D3CCD2D19DFFCABDBEF` | `float x, y, z;` (12 bytes) |
| `...\SDK\Win32\Include\NiBound.h` | `D3A1F40A5F14E254924F33D63CBE592D4E002EFB340FA16E936231E62176BEFF` | center+radius (16 bytes) |
| `...\SDK\Win32\Include\NiFlags.h` | `5C87C32DABA3F7408EB8FCB98335CAA325057361C79D5498F741BDA0A38365D7` | same `NiDeclareFlags` macro (one `m_uFlags` member) |

## Compiled build products (COFF .obj, read-only; SHA256 pins in 00_Control/SOURCE_IDENTITIES.json)

| Object | Vtable evidence | Code-behavior evidence |
|---|---|---|
| `build\NiMain\NiNode.obj` | `??_7NiNode@@6B@` 34 slots — `03_EVIDENCE/GB12_NINODE_OBJ_VTABLE_DUMP.json` | `?GetObjectByName@NiNode@@UAEPAVNiAVObject@@PBD@Z` — `03_EVIDENCE/GB12_NINODE_GETOBJECTBYNAME_DISASM.txt` |
| `build\NiMain\NiAVObject.obj` | 29 slots — `03_EVIDENCE/GB12_CHAIN_OBJ_VTABLE_DUMP.json` | `?GetObjectByName@NiAVObject@@UAEPAV1@PBD@Z` — `03_EVIDENCE/GB12_NIAVOBJECT_GETOBJECTBYNAME_DISASM.txt`; ctor `??0NiAVObject@@IAE@XZ` — `03_EVIDENCE/GB12_NIAVOBJECT_CTOR_DISASM.txt` |
| `build\NiMain\NiAVObject_Win32.obj` | — | `?UpdateWorldData@NiAVObject@@UAEXXZ` — `03_EVIDENCE/GB12_NIAVOBJECT_UPDATEWORLDDATA_DISASM.txt` |
| `build\NiMain\NiObject.obj` | 15 slots — `03_EVIDENCE/GB12_CHAIN_OBJ_VTABLE_DUMP.json` | — |
| `build\NiMain\NiObjectNET.obj` | 15 slots — idem | — |
| `build\NiMain\NiRefObject.obj` | `??_7NiRefObject@@6B@` NOT emitted in this obj (root-class dtor-only virtuality established from header + slot-0 `??_E...` presence in all four derived vtables) | — |
