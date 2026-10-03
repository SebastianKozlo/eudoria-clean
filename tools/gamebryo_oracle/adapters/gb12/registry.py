#!/usr/bin/env python3
# registry.py -- GB 1.2 (GB_1_2) NiStream loader factory registry.
#
# GENERATED from the ORIGINAL Gamebryo 1.2.2 source tree (read-only input
# D:\gamebyroengine\extracted\Gb12_Source): every NiRegisterStream(...) and
# NiStream::RegisterLoader("name", ...) call in the per-lib *SDM.cpp static
# data managers across CoreLibs, de-duplicated and sorted. Class-NAME census
# only; no proprietary source bytes are embedded. ZERO NiArk* (MindArk custom)
# classes occur anywhere in the registry -- the RTTIError verdict for NiArk*
# blocks is therefore invariant to which CoreLibs subset a tool links.
#
# SHA256 of the embedded sorted name list (json): 7CD9A5ED038ABB6700213DF67E14D9EF8F1988D8FBE7FBB3BC4B4C5D40365A28
#
# Provenance per SDM file (original files, read-only):
#   NiAnimationSDM.cpp (lib NiAnimation) sha256 752296175F66CB17092D7D2F1221CE622F50914E6653055E75BC111593602EDB : 61 classes
#   NiMilesAudioSDM.cpp (lib Miles) sha256 1C92C72A1870AC05C931030ADE4D50C195BF8C39448821A3E919EB6E786E8631 : 6 classes
#   NiCollisionSDM.cpp (lib NiCollision) sha256 E72BFBEF673604B328C4497C8DA32FDE65DCAEDB261CA9D2367F75F1837B6E72 : 1 classes
#   NiMainSDM.cpp (lib NiMain) sha256 D49B76EDB07B0548006785D4827C528C58684258957DCD7E50BAB344B87E3E08 : 71 classes
#   NiOldParticleSDM.cpp (lib NiOldParticle) sha256 106742312D541B7EDE542A2CA20AA3477891159FD3E3F936A606B97B55591503 : 9 classes
#   NiParticleSDM.cpp (lib NiParticle) sha256 E694F7E1828668E07493C0D71A5E89E30F25AF86EA1D4FE5CDBE130C50140E14 : 45 classes
#   NiPortalSDM.cpp (lib NiPortal) sha256 8F132B265365F38037F5B30EAC30F27F4D623220B84B92F7000DAB5E836F1169 : 4 classes
#   NiPS2RendererSDM.cpp (lib NiPS2Renderer) sha256 7D7CF721576BE9D4CADFDC8E2A8150734F6030CDEE1DCF752126AF4270B32415 : 1 classes
import json as _json

_CLASS_NAMES_JSON = _json.loads(r"""["NiAlphaAccumulator", "NiAlphaController", "NiAlphaProperty", "NiAmbientLight", "NiAudioListener", "NiAudioSource", "NiAudioSystem", "NiAutoNormalParticles", "NiAutoNormalParticlesData", "NiBSPNode", "NiBSplineBasisData", "NiBSplineColorInterpolator", "NiBSplineCompColorInterpolator", "NiBSplineCompFloatInterpolator", "NiBSplineCompPoint3Interpolator", "NiBSplineCompTransformInterpolator", "NiBSplineData", "NiBSplineFloatInterpolator", "NiBSplinePoint3Interpolator", "NiBSplineTransformInterpolator", "NiBillboardNode", "NiBinaryExtraData", "NiBlendAccumTransformInterpolator", "NiBlendBoolInterpolator", "NiBlendColorInterpolator", "NiBlendFloatInterpolator", "NiBlendPoint3Interpolator", "NiBlendQuaternionInterpolator", "NiBlendTransformInterpolator", "NiBltSource", "NiBoneLODController", "NiBoolData", "NiBoolInterpolator", "NiBoolTimelineInterpolator", "NiBooleanExtraData", "NiCamera", "NiClusterAccumulator", "NiCollisionData", "NiCollisionSwitch", "NiColorData", "NiColorExtraData", "NiColorExtraDataController", "NiColorInterpolator", "NiControllerManager", "NiControllerSequence", "NiDefaultAVObjectPalette", "NiDirectionalLight", "NiDitherProperty", "NiExtraData", "NiFlipController", "NiFloatData", "NiFloatExtraData", "NiFloatExtraDataController", "NiFloatInterpolator", "NiFloatsExtraData", "NiFloatsExtraDataController", "NiFogProperty", "NiGeomMorpherController", "NiGravity", "NiIntegerExtraData", "NiIntegersExtraData", "NiKeyframeController", "NiKeyframeData", "NiKeyframeManager", "NiLODNode", "NiLightColorController", "NiLines", "NiLinesData", "NiLookAtController", "NiLookAtInterpolator", "NiMaterialColorController", "NiMaterialProperty", "NiMeshPSysData", "NiMeshParticleSystem", "NiMilesAudioSystem", "NiMilesListener", "NiMilesSource", "NiMorphData", "NiMultiTargetTransformController", "NiNode", "NiPS2GeometryStreamer", "NiPSysAgeDeathModifier", "NiPSysAirFieldAirFrictionCtlr", "NiPSysAirFieldInheritVelocityCtlr", "NiPSysAirFieldModifier", "NiPSysAirFieldSpreadCtlr", "NiPSysBombModifier", "NiPSysBoundUpdateModifier", "NiPSysBoxEmitter", "NiPSysColliderManager", "NiPSysColorModifier", "NiPSysCylinderEmitter", "NiPSysData", "NiPSysDragFieldModifier", "NiPSysDragModifier", "NiPSysEmitterCtlr", "NiPSysEmitterCtlrData", "NiPSysEmitterDeclinationCtlr", "NiPSysEmitterInitialRadiusCtlr", "NiPSysEmitterLifeSpanCtlr", "NiPSysEmitterPlanarAngleCtlr", "NiPSysEmitterSpeedCtlr", "NiPSysFieldAttenuationCtlr", "NiPSysFieldMagnitudeCtlr", "NiPSysFieldMaxDistanceCtlr", "NiPSysGravityFieldModifier", "NiPSysGravityModifier", "NiPSysGravityStrengthCtlr", "NiPSysGrowFadeModifier", "NiPSysMeshEmitter", "NiPSysMeshUpdateModifier", "NiPSysModifierActiveCtlr", "NiPSysPlanarCollider", "NiPSysPositionModifier", "NiPSysRadialFieldModifier", "NiPSysResetOnLoopCtlr", "NiPSysRotationModifier", "NiPSysSpawnModifier", "NiPSysSphereEmitter", "NiPSysSphericalCollider", "NiPSysTurbulenceFieldModifier", "NiPSysUpdateCtlr", "NiPSysVortexFieldModifier", "NiPalette", "NiParticleBomb", "NiParticleColorModifier", "NiParticleGrowFade", "NiParticleMeshModifier", "NiParticleMeshes", "NiParticleMeshesData", "NiParticleRotation", "NiParticleSystem", "NiParticleSystemController", "NiParticles", "NiParticlesData", "NiPathController", "NiPathInterpolator", "NiPixelData", "NiPlanarCollider", "NiPoint3Interpolator", "NiPointLight", "NiPortal", "NiPosData", "NiQuaternionInterpolator", "NiRangeLODData", "NiRendererSpecificProperty", "NiRollController", "NiRoom", "NiRoomGroup", "NiRotData", "NiRotatingParticles", "NiRotatingParticlesData", "NiScreenGeometry", "NiScreenGeometryData", "NiScreenLODData", "NiScreenPolygon", "NiScreenSpaceCamera", "NiScreenTexture", "NiSequence", "NiSequenceStreamHelper", "NiShadeProperty", "NiSkinData", "NiSkinInstance", "NiSkinPartition", "NiSortAdjustNode", "NiSourceCubeMap", "NiSourceTexture", "NiSpecularProperty", "NiSphericalCollider", "NiSpotLight", "NiStencilProperty", "NiStringExtraData", "NiStringPalette", "NiStringsExtraData", "NiSwitchNode", "NiSwitchStringExtraData", "NiTextKeyExtraData", "NiTextureEffect", "NiTextureTransformController", "NiTexturingProperty", "NiTransformController", "NiTransformData", "NiTransformInterpolator", "NiTriShape", "NiTriShapeData", "NiTriShapeDynamicData", "NiTriStrips", "NiTriStripsData", "NiUVController", "NiUVData", "NiVectorExtraData", "NiVertWeightsExtraData", "NiVertexColorProperty", "NiVisController", "NiVisData", "NiWall", "NiWireframeProperty", "NiZBufferProperty"]""")

GB12_REGISTERED_CLASSES = frozenset(_CLASS_NAMES_JSON)

_COUNT = len(GB12_REGISTERED_CLASSES)


def is_registered(name):
    return name in GB12_REGISTERED_CLASSES
