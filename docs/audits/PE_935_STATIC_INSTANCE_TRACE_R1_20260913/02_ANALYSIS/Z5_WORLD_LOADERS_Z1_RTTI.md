# Z5 — LOADER-Y ŚWIATA (GD-LOADERS) + Z1 MAPA KLAS RTTI

RUN: PE_935_STATIC_INSTANCE_TRACE_R1_20260913 | ERA: EU 9.3.5 (pcg_install)

## 1. Census RTTI (Z1) — pełna lista w 01_RAW/S1_RTTI_CENSUS.{json,csv}

1,970 stringów type-descriptor (`.?AV*/.?AU*`); **483 klasy Ark**, **253 klasy Ni**
(Gamebryo — NiDX9Renderer = era DX9), 592 boost. Kluczowe dla misji:

| grupa | klasy (przykłady z VA name-string) |
|---|---|
| system obiektów | ArkObject @0x00B8CFC4, ArkObjectClass @0x00B8D070, ArkObjectClassInterface @0x00B707A4, ArkObjectService @0x00B730E0, ArkObjectCommander @0x00B73100, ArkClientObjectManagerImpl @0x00B73124 (2 vtable: 0x00A7C028/0x00A7C0A0) |
| template-class | ArkObjectClassImpl<ArkRealWorldItem,$0EOEC> @0x00B8DD18, ArkObjectClassImpl<ArkRealWorldProvider,$0EOEB> @0x00B8DD58, ArkObjectClassImpl<ArkInteractiveWorldObject,$0FNMJ> @0x00B8DCD0, ArkObjectImpl<...> @0x00B8E8D8/@0x00B8EE50/@0x00B8D258 |
| world object | ArkClientWorldObjectManager (bind @0x00B6F928/@0x00B6F9C8: mf0<void> + mf1<uint>), CWOData@ArkClientWorldObjectLogic (bind @0x00B78CC8: free fn(uint, const CWOData&, const function<void()>&)), ArkInstanceProxy (bind @0x00B6FA78), WorldSubsystem @0x00B717A0, ArkClientDynamicWorld (bind @0x00B89AF0), ArkClientDynamicObject @0x00B7F564, ArkClientDynamicMaster/Slave, ArkClientLocalDynamic |
| real world | ArkRealWorldItem @0x00B8E94C, ArkRealWorldProvider @0x00B8EEAC, ArkInteractiveWorldObject @0x00B8D2E8, ArkClientInteractiveWorldObjectImpl @0x00B70F1C |
| portal (spatial cells) | ArkPortalCell @0x00B9743C (vft 0x00A91CF8), ArkPortalCellGraph @0x00B973BC, ArkPortalPortal @0x00B97484, ArkPortalResourceItem(Factory), ArkPortalIdGenerator, ArkPortalCellGraphObserver @0x00B716E0 |
| terrain/veg | ArkTerrainEditZoneFactory @0x00B9D1F4, ArkTerrainEditZoneGroup @0x00B9D51C, ArkTerrainPatchFactory @0x00B9D128, ArkVegetationClimate(Factory) @0x00B970DC/@0x00B970AC, ArkVegetation* (30+ klas), ArkHeightFieldSource @0x00B9D688, ArkHeightFieldInterface @0x00B79A78, ArkHeightTree @0x00B9FDE4, ArkDensityField @0x00B9F9E4 |
| zasoby | ArkModelResourceInstanceRef @0x00B8CACC (vft 0x00A864B8 : ArkRefObject @0x00B8CAB0 vft 0x00A864B0), ArkModelResourceItem(Factory), ArkResourceManager @0x00B958A4, ArkResourceDataStore{Bunt,VFS,File,Audio,FileName} @0x00B959F8/@0x00B95A24/..., ArkFileNameResourceItem |
| sieć (statycznie) | ArkPacket @0x00B96E50, **ArkStaticPacket @0x00B96E98**, ArkPacketDecoder @0x00B96F70, ArkCommunicator @0x00B96EB8 (ctor FUN_00834010) |
| scena | ArkSceneObject @0x00B9D79C (interfejs, 3-slot vft 0x00A98050), ArkSceneObjectFactory @0x00B9D3E0, ArkVegetationSceneObjectSimple @0x00B9D7BC (vft 0x00A9805C), ArkModelSource @0x00B9D428, ArkModelInterface @0x00B9D830 |
| NiAVObject oracle | NiAVObject @0x00B90078 (vft 0x00A8D534), NiNode @0x00B936D0 (vft 0x00A8CCF4), NiCamera @0x00B938E8, NiTriShape @0x00B93E04, NiObjectNET @0x00B6F558 |

**NEGATYW STRUKTURALNY**: klasy "Sector"/"Region"/"Entity" — **0 trafień** w RTTI 9.3.5.
"Cell" istnieje wyłącznie jako ArkPortalCell (portal/dPVS). Pojęcie "sektor" w sensie
klasy klienta NIE ISTNIEJE w 9.3.5 (w przeciwieństwie do era 10.4: Sectors.xbc 129 B).

## 2. Loader-y/rejestry — stringi i funkcje (własny census S2 + xrefy GA1)

| zasób | string (VA) | xref funkcja | interpretacja |
|---|---|---|---|
| templates.vfs | "Parameters\templates.vfs" @0x00A86D30 | FUN_0072fa30 @0x0072FAAC | loader rejestru template'ów (poprzedni run: ArkVFS02) |
| portals | "portals.bnt" @0x00A7A7CC (×2 xref), "portals\" @0x00A7A894 | **FUN_0041dae0** @0x0041EF9B/@0x0041EFF0/@0x0041E95E/@0x0041E9B1 | RM-init: rejestracja magazynu portal (dPVS cell-graph) |
| TEZ | "TerrainEditZones.bnt" @0x00A7A790, "TerrainEditZones\" @0x00A7A86C, ".tez" @0x00A7A71C | FUN_0041dae0 @0x0041F0EF/@0x0041EA57/@0x0041F6BB | rejestracja magazynu stref edycyjnych terenu |
| portal-def w NIF | "m_ContainsPortals" @0x00A86334, "m_ContainsPortalDefinitions" @0x00A86348, "m_ContainsNetImmersePortals" @0x00A86318 | FUN_006f1b90 @0x006F1C25/@0x006F1C64 | check definicji portalów w pliku NIF przy ładowaniu |
| rozbudowa | ".nif"/".bvi"/".amu"/".tdf"/".prt" @0x00A7A774/@0x00A7A734/@0x00A7A744/@0x00A7A73C/@0x00A7A72C | FUN_0041dae0 (@0x0041F1E9/@0x0041F51C/@0x0041F47B/@0x0041F4CE/@0x0041F5C2/@0x0041F615) | magazyny zasobów wg rozszerzeń (.prt = portal resource) |
| scena | "NetImmerseScene::Root" @0x00A972FC, "?NetImmerseScene::Scene" @0x00A972E3 | FUN_00933310 @0x0093338A | dostęp do korzenia sceny po nazwie |
| parametry | "Data\Parameters\" @0x00A97E58 | FUN_0094ba00 @0x0094BA3D, FUN_0094f250 @0x0094F28D | ładowanie parametrów z katalogu |
| dane | "data\" @0x00A797D4 | FUN_00409080 @0x004090BE, FUN_00405150 @0x00405233 | bazowa ścieżka danych |
| CWO | "ArkClientWorldObjectLogic::OnDelayedTextureUpdated" @0x00A7D624 | FUN_0050d480 @0x0050D664 | handler aktualizacji tekstur world-objectów (assert-string = nazwa klasy::metody) |
| vegetacja | (klasy) ArkVegetationClient::GetModel — string w FUN_0094b1d0 | FUN_0094b1d0 | pobranie modelu wegetacji (pump {MODEL,id}) |

## 3. Pliki świata obecne w instalacji 9.3.5 (census katalogów, bez uruchamiania)

```
Data\Parameters\: templates.vfs 560,788 | hierarchy.vfs 169,232 | materials.vfs 80,400 |
  sids.vfs 129,040 | EnvironmentZones.vfs 16,272 | AmbientAudioZones.vfs 144 |
  textures.vfs 1,552 | videos.vfs 3,856 | 20001/20002/20005/20007/20009/20011/20012/
  20014/20015/20016/20017/20030/20033/20034/20037/20039/20040/20043.vfs | 24007.vfs 65,040
Data\Portals\Portals.bnt 80,682 | Data\TerrainEditZones\TerrainEditZones.bnt 54,156 |
Data\VegetationClimates\VegetationClimates.bnt 25,346 | Data\EffectSequences\EffectSequences.bnt 289,984 |
Data\Models\Models.bnt 395,412,868 | Data\Volumes\Volumes.bnt 3,746,375 | Data\Terrain\terrain.bnt 125,064,817
```
**NEGATYW ERA**: w 9.3.5 NIE istnieją Sectors.xbc / Objects.pak / Planets.pak / ResourcePaths.xbc
(to era 10.4 wg E1 z PE_935_EXTERNAL_SOURCES_MATRIX_R1). Przestrzeń "sektorów" 9.3.5 =
ArkPortalCell (portal/dPVS) + TerrainEditZones + EnvironmentZones + parametry 20xxx.vfs.

## 4. GD-LOADERS — werdykt

Loader-y świata zidentyfikowane: (a) RM-init FUN_0041dae0 rejestruje WSZYSTKIE magazyny
świata (nif/bvi/amu/tdf/prt/tez/portals.bnt/TEZ.bnt) — jedno centrum; (b) klasy loaderów
istnieją jako fabryki (ArkPortalResourceItemFactory, ArkTerrainEditZoneFactory,
ArkVegetationClimateFactory, ArkTerrainPatchFactory, ArkEffectSequenceFactory) —
vtable'e wyznaczone metoda COL (S4/GA3); (c) brak klasy "sektor/region/entity" —
9.3.5 nie ma sektorowego modelu świata po stronie klienta; (d) wejścia plikowe istnieją
i są skonsumowane przez RM. NIEROZSTRZYGNIĘTE: zawartość Portals.bnt/TEZ.bnt jako
źródło placementu BUDYNKÓW (kandydat na kolejny run: dekod .prt portal resource).
