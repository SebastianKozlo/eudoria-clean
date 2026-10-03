# NIF_LOAD_PIPELINE — PE_GAMEBRYO_ORACLE_TOOL_R1_20261003 (Batch E1, Phase C)

MODE: STATIC / source-derived. No loader executed in E1. Line numbers are the
cited file's own physical lines. Cited-file SHA256s are given once per file.

## 0. Cited source identities

| File (version) | Path | SHA256 |
|---|---|---|
| GB12 NiStream.cpp | Gb12_Source\CoreLibs\NiMain\NiStream.cpp | E955C36EBBB442029E00BE8A154726741B8454A607F2DC043F1FD542B009DC25 |
| GB26 NiStream.cpp | Gb26_src\NiStream.cpp | 72781EEB0E22D42152E04FADD498EA30292D1807E5C60378F08BFD8563693BA2 |
| GB12 NiObject.cpp | Gb12_Source\CoreLibs\NiMain\NiObject.cpp | B137FE42126F496A37E7627061FF968256A6DA87D912784865609E2122FE470E |
| GB26 NiObject.cpp | Gb26_src\NiObject.cpp | F25499D8C91281B49A3BFF61AEB801B7A09948DA63DA5D2292D5701077AFDA5E |
| GB12 NiObjectNET.cpp | Gb12_Source\CoreLibs\NiMain\NiObjectNET.cpp | 2ADB8F89CDB40F8C114FEAA6E4A32DD7A1CC73BCE30D745F669458EE6F354190 |
| GB26 NiObjectNET.cpp | Gb26_src\NiObjectNET.cpp | 5F63AF1B92C803A76E4E4C35D8A690165D0BBD3B0D82AB1A8000D306D69726E6 |
| GB12 NiAVObject.cpp | Gb12_Source\CoreLibs\NiMain\NiAVObject.cpp | 72E0837149B03CCDA171BDF5E68E1E1F8C2712B2F10E7957AC3EC26344CA5EA7 |
| GB26 NiAVObject.cpp | Gb26_src\NiAVObject.cpp | 091C7ABCE2C1576063245594A761377BE310EFB1DFF8C313BC444BCAEA63E2B9 |
| GB12/GB26 NiAVObject_Win32.cpp | CoreLibs\NiMain\Win32\ / Gb26_src\ | (platform impl of UpdateWorldData; both start line 22) |
| GB12 NiNode.cpp | Gb12_Source\CoreLibs\NiMain\NiNode.cpp | 38C7A1DE1E166345068D296F70F34B1ADAE27C694E19EAD8FA0FBD8B62E0E016 |
| GB26 NiNode.cpp | Gb26_src\NiNode.cpp | C0414C8F85768BF52F741BD51030DB5F73943BD64CA8871D8714DD471084B984 |
| GB12 NiGeometryData.cpp | Gb12_Source\CoreLibs\NiMain\NiGeometryData.cpp | 7E7C09014E87027F32C07B304C58939A561C30DA076B64B4E5D4BA88712D7A8A |
| GB26 NiGeometryData.cpp | Gb26_src\NiGeometryData.cpp | 5C55D2CC64E3FBFFBD60814F6865F70D59BC2E1BF88F92A5F4FA7F24A7725228 |
| GB12 NiBound.cpp | Gb12_Source\CoreLibs\NiMain\NiBound.cpp | F34BB0B9D7BAD147EF3F0FD4E622541A53BD5AAE2F4FCD1077AF863E2FA663A1 |
| GB26 NiBound.cpp | Gb26_src\NiBound.cpp | 14A882078D1C9297C5D81A1D710D98E6B20697C8AE10869548E27B5D62A6FC9C |
| GB12 NiTexturingProperty.cpp | Gb12_Source\CoreLibs\NiMain\NiTexturingProperty.cpp | 2BC36C08E8B9E0AB624569FF098F1CD60B8242B737C0EB7B3E4DD3A6615BA106 |
| GB26 NiTexturingProperty.cpp | Gb26_src\NiTexturingProperty.cpp | ECC6852E882C9915082A9065D541F2DDE353D828B46C7CFFF33665D7DCA752B9 |
| GB12 NiSourceTexture.cpp | Gb12_Source\CoreLibs\NiMain\NiSourceTexture.cpp | B5D0BB026B812CA4D022E110D7CFE0B98ECA181C06F78C62A999512C0927E70E |
| GB26 NiSourceTexture.cpp | Gb26_src\NiSourceTexture.cpp | 2F78C862B902C543A3F2298087FBB341A6547D4BFFCB20A2E641936AD6F7CE74 |

## 1. GB_1_2 (1.x family) — bytes -> runtime

| Step | Class::function | File + lines | Notes (all versions conditional) |
|---|---|---|---|
| 1 entry (file) | NiStream::Load(const char*) | GB12 NiStream.cpp L637-660 | NiFile::GetFile(READ_ONLY); failure -> FILE_NOT_LOADED "Cannot open file." (L650-653) |
| 1 entry (memory) | NiStream::Load(char*, int) / Load(NiBinaryStream*) | L662-670 / L672-689 | both funnel into LoadStream() (L684) |
| 2 header/version | NiStream::LoadHeader | L303-360 | GetLine(128); needs "File Format" in line (L311); version u32 vs [3.3.0.11, 10.2.0.0] (L318-332); user-defined u32 if >= 10.0.1.8 (L335-338); uiObjects u32 (L355-357). FULL QUOTE in 02_ANALYSIS/VERSION_SUPPORT.md |
| 3 type strings | NiStream::LoadRTTI / LoadRTTIString | L415-449 / L1149-1153 | usRTTICount u16; per type: u32 length + raw bytes (LoadRTTIString); lookup in ms_pkLoaders; miss -> RTTIError + return false (L427-433) |
| 4 factory | NiStream::RegisterLoader / ms_pkLoaders | L755-766 / L57, L692 | NiTStringPointerMap<CreateFunction> keyed by RTTI name; registered by each class module |
| 5 object allocation | LoadRTTI second loop | L436-444 | per object: usRTTI u16 index -> ppfnCreate[usRTTI]() -> m_kObjects.Add — ALL objects allocated BEFORE any LoadBinary (bNew path, file >= 5.0.0.1; legacy LoadObject path L466-468 for older files) |
| 6 LoadBinary loop | NiStream::LoadStream | L521-635 | bNew = ver >= 5.0.0.1 (L521); LoadObjectGroups if >= 5.0.0.6 (L529-532); per-object `pkObject->LoadBinary(*this)` (L551-553); CheckConsistency L563 |
| 7 top-level | NiStream::LoadTopLevelObjects | L367-385 | u32 count + linkIDs -> m_kTopObjects (L566) |
| 8 link phase | LoadStream link loop | L568-578 | `pkObject->LinkObject(*this)` for every object (L576) |
| 9 PostLink phase | LoadStream post-link loop | L580-590 | `pkObject->PostLinkObject(*this)` for every object (L588) |
| 10 post-process | ms_pkPostProcessFunctions | L602-622 | registered PostProcessFunction per top object |
| 11 old-version fixup | NiStream::SetSelectiveUpdateFlagsForOldVersions | L821-841, called L630 | ONLY if file version < 4.1.0.12: SetSelectiveUpdateFlagsTTTFRecursive on roots (L824-840). For 10.1.0.0 and 4.1.0.12 files this is a NO-OP |
| 12 finish | FreeLoadData; return true | L632-635 | failure anywhere -> FreeLoadData + return false |

### Per-block LoadBinary chain (GB_1_2; the PCG-relevant 10.1.0.0 column)

- `NiObject::LoadBinary` (NiObject.cpp L134-143): GroupID u32 iff 5.0.0.6 <= v < 10.1.0.114 → **for NIF 10.1.0.0 the per-block GroupID u32 IS read** (this is the "dummy uint32" our v10 parser observed). For NIF 4.1.0.12 the lower bound is NOT met (4.1.0.12 < 5.0.0.6 packed) — the GroupID is NOT read (T4 decode: zero group_id fields, EOF-exact). (C2 correction 2026-10-03; PE-MASTER audit finding.)
- `NiObjectNET::LoadBinary` (NiObjectNET.cpp L553-571): `kStream.LoadCString(m_pcName)` (L557 — u32 length + bytes); ExtraData: single linkID if v < 5.0.0.11, else ReadMultipleLinkIDs (L559-568); controller linkID (L570).
- `NiAVObject::LoadBinary` (NiAVObject.cpp L546-699): flags u16 (L551) + conversion shifts for v < 4.1.0.11 / < 4.1.0.12 / < 5.0.0.1 (L554-600); **local transform: `m_kLocal.m_Translate.LoadBinary` (L602, 3x f32), `m_kLocal.m_Rotate.LoadBinary` (L603, 3x3 f32), scale f32 (L604)**; v >= 5.0.0.19: property ReadMultipleLinkIDs (L674) + collision ReadLinkID (L675); v < 5.0.0.19 legacy path with velocity + ABV (L606-670).
- `NiNode::LoadBinary` (NiNode.cpp L861-870): children ReadMultipleLinkIDs (L866) + effects ReadMultipleLinkIDs (L869).
- `NiGeometryData::LoadBinary` (NiGeometryData.cpp L519-648): GroupID iff v >= 10.1.0.114 (L523 — NOT read for 10.1.0.0); vertices u16 (L530); keep/compress flags iff v >= 10.0.1.16 (L532); bHasVertex NiBool (L547); data flags iff v >= 10.0.0.2 (L574); **bound: `m_kBound.LoadBinary(kStream)` (L618 — model-space center 3x f32 + radius f32)**; colors (L620-630).
- `NiBound::LoadBinary` (NiBound.cpp L163-167): center + radius.
- `NiTexturingProperty::LoadBinary` (NiTexturingProperty.cpp L238-349): apply enum (L242); map list u32 + per-map NiBool bHasMap + inline Map/BumpMap/ShaderMap::LoadBinary (L243-317); shader maps iff v >= 5.0.0.17 (L319-346).
- `NiSourceTexture::LoadBinary` (NiSourceTexture.cpp L162-221): v >= 10.0.1.4 (PCG case): bExternalTexture NiBool + **`kStream.LoadCString(m_pcFilename)`** (L204) + pixel-data linkID (L205-206); v < 10.0.1.4: bSaveName legacy layout (L172-200).

### Link + PostLink (GB_1_2)

- `NiObjectNET::LinkObject` (NiObjectNET.cpp L573-598): ExtraData resolution (L577-595), `m_spControllers = GetObjectFromLinkID()` (L597).
- `NiNode::LinkObject` (NiNode.cpp L886-918): children via SetAt (L886-888); effect list, reverse order for v < 4.1.0.8 (L891-916).
- `NiObjectNET::PostLinkObject` (NiObjectNET.cpp L656-693): old-style ExtraData linked-list migration (L660-679); deprecated NiVertWeightsExtraData removal (L681-692).
- `NiObject::LinkObject`/`PostLinkObject` are empty bases (NiObject.cpp L145-151).

## 2. GB_2_6 (2.x family) — and the 1.x vs 2.x differences

Same spine (entry -> LoadHeader -> LoadRTTI -> LoadBinary loop -> top-level ->
link -> post-link), with these **explicit differences** (all GB26 NiStream.cpp):

1. **Version gate:** min 10.1.0.114 (L48-49) — 10.1.0.0 files are rejected here.
2. **Endianness:** header read forced little-endian (L389-391); serialized
   endianness flag when v >= 20.0.0.3 (L412-415); ENDIAN_MISMATCH error path
   (L417-425); `NiBinaryStream::DoByteSwap` (GB26 NiBinaryStream.cpp L93-131).
3. **Object size table:** `LoadObjectSizeTable` when v >= 20.2.0.5 (L802-806,
   impl L691-695) — enables skipping unknown objects by Seek (L855-867).
4. **Fixed string table:** `LoadFixedStringTable` when v >= 20.1.0.1 (L808-812,
   impl L700-723): u32 count + u32 max size + (u32 length + bytes)* -> NiFixedString
   pool; names then load by **index** (`NiObjectNET::LoadBinary` GB26 L571-589:
   LoadCStringAsFixedString if v < 20.1.0.1, else LoadFixedString; NiSourceTexture
   GB26 L177-184 same pattern).
5. **Skippable unknown classes:** `LoadRTTI` uses LoadRTTIHelper +
   ParseRTTINameAndArgs (constructor-arg RTTI syntax, L630-683) with
   `SKIPPABLE_MASK = 0x8000` (NiStream.h L363) when v >= 20.2.0.5 (L655-677);
   GB 1.2 instead FAILS the whole load on any unknown class (fail-closed).
6. **Link loop null-safety:** `m_kObjects.GetAt(m_uiLink).GetObjectToLink()`
   (L888) — NULL (skipped) objects tolerated; GB 1.2 assumes all objects exist.
7. **Per-block GroupID:** GB26 NiObject.cpp L150-158 — read when
   v < 10.1.0.114 (no 5.0.0.6 lower bound, unlike GB12 L136-137).
8. **NiAVObject::LoadBinary simplified** (GB26 L528-551): no < 4.1.0.11/< 4.1.0.12/
   < 5.0.0.1/< 5.0.0.19 legacy branches (min-version floor makes them dead);
   keeps one 2.x fixup: DISABLE_SORTING clear when v < 20.0.0.4 (L543-550).
9. **NiNode::LoadBinary** adds `SetNodeBit()` (GB26 NiNode.cpp L829).
10. **NiGeometryData::LoadBinary** (GB26 L216-325): same field order; bound at
    L279; additional-geometry linkID when v >= 10.3.0.7 (L321-324).

## 3. GB_1_1_2 and GB_2_3 (binary SDKs) — pipeline shape from headers

- GB_1_1_2 `NiStream.h` (SHA256 DF8057C6...) declares the full 1.x spine:
  Load/Save (L49-58), LoadHeader/SaveHeader (L161-162), LoadStream/SaveStream
  (L163-164), LoadTopLevelObjects (L166), LoadObject (L168),
  SetSelectiveUpdateFlagsForOldVersions + TTTF recursive (L174-175),
  LoadRTTIString/LoadRTTI/SaveRTTI/RTTIError (L178-181), LoadObjectGroups
  (L184), RegisterLoader/CreateFunction (L144-146),
  CreateObjectByRTTI (L155). Implementation = NiMain.lib (binary).
- GB_2_3 recovered `NiStream.h` (SHA256 532FEE68...) declares the 2.x spine:
  LoadHeader (L210), LoadStream (L212), LoadObject (L217),
  PreSaveObjectSizeTable/SaveObjectSizeTable/**LoadObjectSizeTable** (L218-220),
  SaveFixedStringTable/**LoadFixedStringTable** (L237-238), LoadRTTIString/
  LoadRTTI (L230-231), LoadObjectGroups (L241), SetSelectiveUpdateFlagsForOldVersions
  (L226), m_uiNifFileVersion/m_uiNifFileUserDefinedVersion members (L247-248),
  ms_uiNifMin/MaxVersion statics (L314-317). Implementation = binary libs.

## 4. Runtime handoff (both source versions)

After PostLink + post-process, the app takes `m_kTopObjects` roots; per-object
`SERIALIZED_LOCAL_TRANSFORM` (m_kLocal: translate L602/535, rotate L603/536,
scale L604/537) is distinct from `COMPUTED_WORLD_TRANSFORM` (m_kWorld, computed
later by `NiAVObject::UpdateWorldData` — NiAVObject_Win32.cpp L22-31 both
versions: `m_kWorld = m_pkParent->m_kWorld * m_kLocal`, else `m_kWorld = m_kLocal`).
World bounds are NOT serialized; they are recomputed by UpdateWorldBound
(NiNode.cpp GB12 L394-416 / GB26 L311-333: merge of visual children bounds).

## 5. What this pipeline does NOT yet cover (honesty)

- Executed-loader behavior (return codes, message boxes in tools) — E2.
- NiArk* (MindArk custom) classes: NOT present in any Gamebryo loader registry —
  see VERSION_SUPPORT.md section 5 (source-derived prediction, E2 must test).
- KF/KFM animation container format, NiControllerSequence LinkObject internals —
  indexed (SOURCE_ORACLE_INDEX.csv) but not quoted in this file.
