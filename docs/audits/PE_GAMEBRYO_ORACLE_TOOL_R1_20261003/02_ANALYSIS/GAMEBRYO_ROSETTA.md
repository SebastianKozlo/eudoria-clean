# GAMEBRYO_ROSETTA — PE_GAMEBRYO_ORACLE_TOOL_R1_20261003 (Batch E1, Phase C)

The byte->loader->runtime map for the steps covered by E1 source reading.
Format: ORIGINAL BYTE(S) -> GAMEBRYO LOADER (version, file, line) -> RUNTIME
FIELD -> RUNTIME OBJECT -> CONSUMER. Every loader cell cites the file whose
SHA256 is pinned in NIF_LOAD_PIPELINE.md section 0 (same lines quoted there).
Where 1.x and 2.x differ, both rows are given — era separation is absolute.

## 1. File header

| Original byte | Gamebryo loader | Runtime field | Runtime object | Consumer |
|---|---|---|---|---|
| header line `"Gamebryo File Format, Version 10.1.0.0\n"` (or `"NetImmerse File Format, Version 4.1.0.12\n"` — T4's actual header) | GB_1_2 NiStream::LoadHeader L309-316 (GetLine 128; requires substring "File Format"); GB_2_6 L380-387 | (text only; version number in the line is informational — the gate uses the u32) | NiStream | error path NOT_NIF_FILE; T-corpus headers recorded in EXTRACT_PROVENANCE.json |
| version u32 (packed maj<<24\|min<<16\|patch<<8\|internal) | GB_1_2 L318 vs ms_uiNifMinVersion 3.3.0.11 / ms_uiNifMaxVersion 10.2.0.0 (L320-332); GB_2_6 L393 vs 10.1.0.114 / 20.6.0.0 (L395-407) | m_uiNifFileVersion | NiStream | every subsequent version conditional; GetFileVersion() consumed by all LoadBinary/LinkObject paths |
| user-defined version u32 (only if file version >= 10.0.1.8) | GB_1_2 L335-338; GB_2_6 L437-440 | m_uiNifFileUserDefinedVersion | NiStream | gate vs ms_uiNifMin/MaxUserDefinedVersion (0.0.0.0/0.0.0.0 both source versions) |
| endianness flag (only if version >= 20.0.0.3; NOT in 10.1.0.0 files) | GB_2_6 L412-415 | m_bSourceIsLittleEndian | NiStream -> m_pkIstr->SetEndianSwap (L464) | NiBinaryStream::DoByteSwap (GB26 NiBinaryStream.cpp L93-131) |
| block count u32 | GB_1_2 L355-357; GB_2_6 L459-461 | m_kObjects.SetSize | NiStream | LoadRTTI allocation loop |

## 2. Block type strings + factory

| Original byte | Gamebryo loader | Runtime field | Runtime object | Consumer |
|---|---|---|---|---|
| usRTTICount u16 | GB_1_2 LoadRTTI L415; GB_2_6 L630 | count | NiStream | create-function table |
| per type: u32 length + raw bytes (LoadRTTIString) | GB_1_2 L1149-1153 / loop L421-434; GB_2_6 LoadRTTIHelper::ParseRTTINameAndArgs L638-646 | RTTI name string | ms_pkLoaders map lookup (GB_1_2 L427; miss -> RTTIError + LOAD FAIL) | ppfnCreate[i] factory; GB_2_6 additionally SKIPPABLE_MASK 0x8000 (NiStream.h L363; L655-677) |
| per block: usRTTI u16 index | GB_1_2 L436-444 (`ppfnCreate[usRTTI]()` -> m_kObjects.Add); GB_2_6 L649-677 (SetAt; skippable -> NULL + Seek by size table) | allocated object | NiObject subclass instance | LoadBinary loop |
| (2.x only, version >= 20.1.0.1) fixed string table: count u32 + max u32 + (len u32 + bytes)* | GB_2_6 LoadFixedStringTable L700-723 | m_kFixedStrings pool | NiFixedString | names by index (NiObjectNET/SourceTexture LoadBinary) |

## 3. Per-block GroupID (where applicable)

| Original byte | Gamebryo loader | Runtime field | Runtime object | Consumer |
|---|---|---|---|---|
| GroupID u32 at block start | GB_1_2 NiObject::LoadBinary L134-143: read iff 5.0.0.6 <= v < 10.1.0.114 (**10.1.0.0: READ**; our v10 parser's "dummy uint32" is this); GB_2_6 NiObject.cpp L150-158: read iff v < 10.1.0.114 | SetGroup(GetGroupFromID(uiID)) | NiObjectGroup (NiStream::LoadObjectGroups L474-487 GB12 / L748-761 GB26, groups present iff v >= 5.0.0.6) | block-allocation grouping (NiGeometryData L523-528 uses group allocator for >= 10.1.0.114 files) |

## 4. Transform triples (SERIALIZED_LOCAL_TRANSFORM)

| Original byte | Gamebryo loader | Runtime field | Runtime object | Consumer |
|---|---|---|---|---|
| flags u16 | GB_1_2 NiAVObject::LoadBinary L551 (+version shifts L554-600); GB_2_6 L533 (+DISABLE_SORTING fixup L543-550) | m_uFlags | NiAVObject | selective-update bits (SetSelectiveUpdateFlags GB12 L216-254 / GB26 L246-285) |
| translate 3x f32 | GB_1_2 L602; GB_2_6 L535 | m_kLocal.m_Translate | NiTransform (NiAVObject) | SetTranslate (inl), UpdateWorldData (NiAVObject_Win32.cpp L22-31) |
| rotate 3x3 f32 | GB_1_2 L603; GB_2_6 L536 | m_kLocal.m_Rotate | NiTransform | SetRotate, UpdateWorldData |
| scale f32 | GB_1_2 L604; GB_2_6 L537 | m_kLocal.m_fScale | NiTransform | SetScale (inl L135-143 both eras: NIASSERT >= 0, NiAbs) |
| (computed, NOT serialized) world transform | NiAVObject::UpdateWorldData (NiAVObject_Win32.cpp L22-31 both) | m_kWorld = parent->m_kWorld * m_kLocal (root: = m_kLocal) | NiTransform | culling, rendering, GetWorldTransform |
| name: u32 length + bytes | GB_1_2 NiObjectNET::LoadBinary L557 (LoadCString L1128-1140); GB_2_6 L575-582 (fixed-string) | m_pcName / m_kName | NiObjectNET | GetObjectByName; scene-graph printers |

## 5. Bounds

| Original byte | Gamebryo loader | Runtime field | Runtime object | Consumer |
|---|---|---|---|---|
| model-space bound: center 3x f32 + radius f32 (in NiGeometryData blocks) | GB_1_2 NiGeometryData::LoadBinary L618 -> NiBound::LoadBinary (NiBound.cpp L163-167); GB_2_6 L279 -> L342-346 | m_kBound | NiBound (NiGeometryData) | NiGeometry::UpdateWorldBound via bound Update(transform) |
| (computed, NOT serialized) world bound | NiNode::UpdateWorldBound GB12 L394-416 / GB26 L311-333; NiAVObject::UpdateWorldBound inline stub | m_kWorldBound | NiBound (NiAVObject) | culling (IsVisualObject = radius != 0), camera |
| ABV (NiBoundingVolume) via collision linkID | NiAVObject::LoadBinary collision ReadLinkID GB12 L675 / GB26 L541 | m_spCollisionObject -> NiCollisionData | NiBoundingVolume::CreateFromStream (GB12 NiBoundingVolume.cpp L143-154; type enum -> ms_apfnLoaders factory; NiBoxBV::LoadBinary L2107-2111, NiSphereBV::LoadBinary L432-436) | collision system |

## 6. Texture name fields

| Original byte | Gamebryo loader | Runtime field | Runtime object | Consumer |
|---|---|---|---|---|
| (NiTexturingProperty map) bHasMap NiBool + Map fields incl. texture linkID | GB_1_2 NiTexturingProperty::LoadBinary L238-317; GB_2_6 L254-348 (+PARALLAX_INDEX) | m_kMaps[i] | Map/BumpMap/ShaderMap | renderer texture binding |
| (NiSourceTexture, v >= 10.0.1.4 — the PCG case) bExternalTexture NiBool + filename (u32 length + bytes) + pixel-data linkID | GB_1_2 NiSourceTexture::LoadBinary L201-207 (`LoadCString(m_pcFilename)`); GB_2_6 L175-193 (fixed-string) | m_pcFilename / m_kFilename | NiSourceTexture | NiImageConverter::ConvertFilenameToPlatformSpecific (GB12 L211-213); search-path + texture palette sharing |

## 7. NOT covered by this map yet (honesty)

- NiGeometryData vertex/normal/color/UV exact stream order beyond the fields
  listed (partially quoted; full function bodies in sandbox evidence packs).
- NiSkinData/NiSkinPartition, NiPixelData image payload, NiControllerSequence /
  NiKeyframeController keyframe payloads — indexed in SOURCE_ORACLE_INDEX.csv
  (functions_present) but not mapped here (E2 candidate extension).
- NiArk* custom MindArk blocks — NOT in any Gamebryo source (Rosetta edge
  terminates at "unregistered RTTI name -> RTTIError").
- Machine-shape -> compiled-signature correlation (s14 optional part) — deferred
  to E2's optional GAMEBRYO_SEMANTIC_SIGNATURES.json.
