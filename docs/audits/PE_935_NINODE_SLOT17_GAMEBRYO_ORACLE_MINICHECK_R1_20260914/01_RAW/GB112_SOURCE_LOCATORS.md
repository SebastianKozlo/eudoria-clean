# GB112_SOURCE_LOCATORS — Gamebryo 1.1.2 Evaluation (era-nearest oracle)

All paths physical on this host; all files read-only. SHA256 = full-file SHA256.
The 1.1.2 Evaluation SDK ships HEADERS + COMPILED LIBS only (no .cpp for NiMain);
behavioral fingerprints therefore come from headers (signatures, member order)
plus compiled-code evidence in `SDK\Win32\Lib\VC71\ReleaseLib\NiMain.lib`
(SHA256 `FF4519AFD2475D9A6E71A35E5DB6B0F5A0B7E9E86EC3662C6A340DA19BA06597`).

## Chain headers (class/virtual map inputs)

| File | SHA256 | Relevant content (line numbers are 1-based, reproducible locators) |
|---|---|---|
| `D:\gamebyroengine\Gamebryo 1.1.2 Evaluation\SDK\Win32\Include\NiRefObject.h` | `BA093BD36019F0D4DA9C27AD790B6D7CE257560D28E1C417C7695EE8791EC4E6` | virtual dtor L27; `m_uiRefCount` L34 (only virtual = dtor; only member = refcount) |
| `...\Include\NiObject.h` | `D35499ED65FA8755799F12D9D96C3CF5917A52E475EE9AEEB87CFEE81C40365C` | macros L31-34 (root RTTI/clone/stream/viewerstrings) + inline virtual `AddViewerStrings` L35; virtual dtor L39; `ProcessClone` L43-44; `PostLinkObject` L49; `GetBlockAllocationSize` L52; **GetGroup/SetGroup L53-54 are NON-VIRTUAL**; member `m_pkGroup` L61 |
| `...\Include\NiObjectNET.h` | `C092517D47B69368364F2FF00D49556CF2D792D8CA6739E766B64EDA98FB806F` | adds NO new virtuals; members `m_pcName` L139, `m_spControllers` L140, `m_ppkExtra` L143, `m_uiExtraDataSize` L144, `m_uiMaxSize` L145 |
| `...\Include\NiAVObject.h` | `3FC6C7101EC816EE27E116D495CF5A1E292F4AE261A0E9BFE58DBB6BCA99E6B6` | `NiDeclareFlags(unsigned short)` L50 (first data member `m_uFlags` u16); new virtuals in declaration order: `UpdateControllers` L61, `UpdateNodeBound` L65, `ApplyTransform` L81-82, **`GetObjectByName` L102**, `SetSelectiveUpdateFlags` L140-141, `UpdateDownwardPass` L158, `UpdateSelectedDownwardPass` L159, `UpdateRigidDownwardPass` L160, `UpdatePropertiesDownward` L163, `UpdateEffectsDownward` L164, `Display` L176, `PurgeRendererData` L190, protected-after-members `UpdateWorldBound` L244, `UpdateWorldData` L245; members `m_pkParent` L199, `m_kWorldBound` L230, `m_kLocal` L236, `m_kWorld` L237, `m_kPropertyList` L241, `m_spCollisionObject` L255 |
| `...\Include\NiNode.h` | `40F77EE947B64C2969C050A2E06EE063DC65E46949F5DFEEC1D511B4220FE2E6` | NiNode new virtuals in declaration order: `AttachChild` L41, `DetachChild` L42, `DetachChildAt` L43, `SetAt` L44, `ApplyTransform`(override) L48-49, **`GetObjectByName`(override) L58**, `UpdateControllers`(ovr) L63, `UpdateDownwardPass`(ovr) L64, `UpdateSelectedDownwardPass`(ovr) L65, `UpdateUpwardPass`(NEW) L66, `UpdateWorldBound`(ovr) L67, `UpdateRigidDownwardPass`(ovr) L68, `UpdateNodeBound`(ovr) L69, `UpdatePropertiesDownward`(ovr) L75, `UpdateEffectsDownward`(ovr) L76, `Display`(ovr) L79, `SetSelectiveUpdateFlags`(ovr) L90-91, `PurgeRendererData`(ovr) L94, `ProcessClone`(ovr) L100-101; members `m_kChildren` L106, `m_kEffectList` L109, `m_kBound` L120 |

## Value-type headers (member-offset math inputs)

| File | SHA256 | Facts |
|---|---|---|
| `...\Include\NiTransform.h` | `CD5C20B13B1060E50126C753A4B5AC915F43518A41FBB1BFE777FFE7E4769BC9` | class block L20-42; data members L25-27 `NiMatrix3 m_Rotate; NiPoint3 m_Translate; float m_fScale;` with "declaration order effects assembly" comment L23-24; class block BYTE-IDENTICAL to GB 1.2.2.6 version |
| `...\Include\NiMatrix3.h` | `620F646B97B64FDF4C364D67E90F232AC32E591599718542D79FA80E5FBB85D6` | Win32 member `float m_pEntry[3][3]` (= 9 floats = 36 bytes), after `#if defined(PS2)||defined(_XBOX)` block near class end |
| `...\Include\NiPoint3.h` | `8682E6DD2CB1C54B1264DDD3071F34810BF37CC06765B711FD93D4EBD64728A1` | `float x, y, z;` L23 (12 bytes) |
| `...\Include\NiBound.h` | `A6ECE63FF6C357E61AE21F37BF97D1EF15CD64E8E93F81BF25FCDF992E43A322` | members `m_kCenter` L76, `m_fRadius` L77 (16 bytes); note `NI_DATA_ALIGMENT(16)` at L83 |
| `...\Include\NiFlags.h` | `2EAF9D03907F9C67086C97DC0F123A1853092D7F9900343AD84F98EE4EE2E75C` | `NiDeclareFlags(type)` macro inserts exactly ONE data member `m_uFlags` (+ inline bit helpers) |
| `...\Include\NiRTLib.h` | `A04D93A6C58336B2614035F3740A822B2E4A82DAA217257F55578BBF1F09A292` | **`#define NI_DATA_ALIGMENT(size)` is EMPTY on Win32 (L37)** — NiBound carries no 16-byte alignment on x86 |

## Compiled-code locators (NiMain.lib, VC71 ReleaseLib)

Member names in this archive resolve through the long-name table; the defining members
found by symbol scan (see `00_Control/coff_disasm_symbol.py`, deterministic):

| Symbol (MSVC-decorated) | Defined in lib member | Evidence file |
|---|---|---|
| `??_7NiRefObject@@6B@` | e.g. `/1031`, `/1466`, `/1499`, `/1532`, `/1635`, `/2224`, `/2608`, `/2796`, `/2822`, `/3104`, `/3227`, `/3517`, `/4165` (vtable symbol present in many members; slot set identical, 1 slot) | `03_EVIDENCE/GB112_NIMAIN_LIB_VTABLE_DUMP.json` |
| `??_7NiObject@@6B@` | `/2796` (13 slots) | idem |
| `??_7NiObjectNET@@6B@` | `/2736` (13 slots) | idem |
| `??_7NiAVObject@@6B@` | `/4165` (27 slots) | idem |
| `??_7NiNode@@6B@` | `/2822` (32 slots) | idem |
| `?GetObjectByName@NiNode@@UAEPAVNiAVObject@@PBD@Z` | `.\releaselib\NiNode.obj` | `03_EVIDENCE/GB112_NINODE_GETOBJECTBYNAME_DISASM.txt` |
| `?GetObjectByName@NiAVObject@@UAEPAV1@PBD@Z` | `.\releaselib\NiAVObject.obj` | `03_EVIDENCE/GB112_NIAVOBJECT_GETOBJECTBYNAME_DISASM.txt` |
| `??0NiAVObject@@IAE@XZ` (protected ctor) | `.\releaselib\NiAVObject.obj` (scan-located) | `03_EVIDENCE/GB112_NIAVOBJECT_CTOR_DISASM.txt` |
| `?UpdateWorldData@NiAVObject@@MAEXXZ` | `.\releaselib\NiAVObject_Win32.obj` member (scan-located; note MAE = protected virtual in 1.1.2) | `03_EVIDENCE/GB112_NIAVOBJECT_UPDATEWORLDDATA_DISASM.txt` |

GB 1.1.2 has NO .cpp for NiMain in the Evaluation SDK — the 1.1.2 GetObjectByName body
is therefore only recoverable as compiled code; the disassembly evidence above IS the
1.1.2 body, and its shape is identical to the 1.2.2.6 source body quoted in
`01_RAW/GB12_SOURCE_LOCATORS.md` (same base-call-first + child-loop structure).
