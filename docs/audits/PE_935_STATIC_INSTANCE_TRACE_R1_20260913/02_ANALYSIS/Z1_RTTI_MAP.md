# Z1 — MAPA KLAS RTTI MINDARKA 9.3.5 (CENSUS)

RUN: PE_935_STATIC_INSTANCE_TRACE_R1_20260913 | ERA: EU 9.3.5 (pcg_install)
Pełna lista: 01_RAW/S1_RTTI_CENSUS.json (1,970 type-descriptor strings z VA) +
S1_RTTI_CENSUS.csv. Skan statyczny .rdata/.data (s1_rtti_census.py; wzorce
MSVC RTTI `.?AV<name>@@`/`.?AU<name>@@`).

## Zestawienie
- **1,970** stringów type-descriptor; **483** klasy Ark-prefixed; **253** klas Ni
  (Gamebryo; NiDX9Renderer — era DX9); **592** boost; reszta: STLport/std.
- Filtre keyword (case-insensitive): World=23, Cell=6, Zone=3, Static=2, Instance=3,
  Sector=0, Region=0, Entity=0.

## Kluczowe grupy (mapa modelu obiektowego — podstawa klasyfikacji Z2/Z4/Z5)

### System obiektów (encje)
ArkObject, ArkObjectClass, ArkObjectClassInterface, ArkObjectService,
ArkObjectCommander, ArkClientObjectManagerImpl, ArkClientObjectImpl<T>,
ArkObjectClassImpl<T,CLASSID> — CLASSID w manglingu:
- ArkObjectClassImpl<ArkRealWorldItem,$0EOEC> — RealWorldItem class-id 0xEOEC
- ArkObjectClassImpl<ArkRealWorldProvider,$0EOEB>
- ArkObjectClassImpl<ArkInteractiveWorldObject,$0FNMJ>
- ArkObjectImpl<$0EOEC,ArkRealWorldItem,ArkServerRealWorldItemImpl,ArkClientRealWorldItemImpl>
- ArkObjectImpl<$0FNMJ,ArkInteractiveWorldObject,ArkServerInteractiveWorldObjectImpl,ArkClientInteractiveWorldObjectImpl>
Hierarchia ENCJA: klasa (definicja) → obiekt (instancja) → client/server impl.

### World-object (klient)
ArkClientWorldObjectManager (tylko via boost::bind mf0<void>/mf1<uint>),
CWOData@ArkClientWorldObjectLogic (free fn: void(uint, const CWOData&, const function<void()>&)),
ArkInstanceProxy (free fn: void(ArkInstanceProxy&)), WorldSubsystem,
ArkClientDynamicWorld, ArkClientDynamicObject, ArkClientDynamicMaster/Slave,
ArkClientLocalDynamic, ArkInputListener_World.

### RealWorld / InteractiveWorld
ArkRealWorldItem, ArkRealWorldProvider, ArkInteractiveWorldObject,
ArkClientInteractiveWorldObjectImpl, ArkClientDefaultObjectImpl,
ArkTraverserWorldVertexExtractor.

### Portal (jedyna przestrzeń "cell" w 9.3.5)
ArkPortalCell, ArkPortalCellGraph(+Observer), ArkPortalPortal, ArkPortalResourceItem(Factory),
ArkPortalIdGenerator(+Interface), ArkPortalInterface.

### Teren / wegetacja
ArkTerrainEditZoneFactory, ArkTerrainEditZoneGroup, ArkTerrainPatchFactory,
ArkVegetationClimate(Factory), ArkVegetationClient/Model/Layer/Patch/... (30+),
ArkHeightFieldInterface, ArkHeightFieldSource, ArkVegetationHeightFieldSourceClient,
ArkHeightTree, ArkDensityField, ArkVegetationLODSettings, ArkVegetationSpawner.

### Zasoby (runtime)
ArkResourceManager, ArkResourceDataStore{Bunt,VFS,File,FileName,Audio},
ArkResourceItemString(Factory), ArkResourceItemStoreFixedCount,
ArkModelResourceItem(Factory), **ArkModelResourceInstanceRef**, ArkRefObject,
ArkFileNameResourceItem(Factory), ArkEffectSequenceResourceItem, ArkImageResourceItem*,
ArkPortalResourceItem(Factory), ArkBoundResourceItem(Factory), ArkModelManager(Main).

### Sieć (badana statycznie)
ArkPacket, **ArkStaticPacket**, ArkPacketDecoder, ArkCommunicator, ArkChannelAuth,
ArkPacketExecutorInterface, ArkClientPacketExecutor.

### UI/preview
ArkUIDesktop + ~60 klas UI, ArkUIGfxTemplate*, ArkUI3DViewPort, ArkUIViewPort*.

### Scena (interfejs wrapperów)
ArkSceneObject (interfejs), ArkSceneObjectFactory, ArkVegetationSceneObjectSimple,
ArkModelSource, ArkModelInterface, ArkVegetationModelClient.

### Ni (Gamebryo — oracle strukturalny)
NiObjectNET, **NiAVObject**, NiNode, NiCamera, NiTriShape(+Data), NiSwitchNode,
NiBillboardNode, NiLODNode, NiBSPNode, NiOBBNode, NiCollisionObject/Data,
NiKeyframeController/Data, NiSequence, NiControllerSequence, NiTexturingProperty,
NiMaterialProperty, NiDX9Renderer, NiArkBillboardNode, NiArk*ExtraData,
NiStaticGeometryGroup.

## Negatywy strukturalne
- **BRAK**: ArkSector, ArkRegion, ArkEntity, ArkWorldObject (jako klasa RTTI),
  ArkStaticObject, ArkPlacement*.
- "Static" tylko: ArkStaticPacket (sieć) + NiStaticGeometryGroup (Gamebryo).
- "Instance" tylko: ArkModelResourceInstanceRef, ArkInstanceProxy (bind), NiSkinInstance.
