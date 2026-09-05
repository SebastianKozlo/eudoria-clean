# 06 — Lights, camera, collision, particle systems

## Lights — CONFIRMED (C19)

Chain: NET → AVObject → NiDynamicEffect → NiLight → {Point, Spot, Directional, Ambient}

**NiDynamicEffect layer by version** (the empty middle!):
```
v10 (≥ 0x0A010000): numAffectedNodes u32 + affectedNodes Ref[]
v4.0.0.2 (≤ 0x04000002): numAffectedNodeListPointers u32 + ptrs u32[]
v4.1.0.12: NOTHING (between the two gates)
```

**NiLight**: dimmer f32 + ambient Color3 + diffuse Color3 + specular Color3
**NiPointLight**: + constantAttenuation f32, linearAttenuation f32, quadraticAttenuation f32
**NiSpotLight**: point light + cutoffAngle f32 + exponent f32
(no extra unknownFloat — that needs v ≥ 0x14020007, not PE)

Counts (9.3.5): Point 846, Directional 130, Ambient 76, Spot 47.

## NiTextureEffect — CONFIRMED (C16, 20/20 traces; 167 B v10)

Chain: NET → AVObject → DynamicEffect → TextureEffect
```
[v10 DynamicEffect: numAffectedNodes + affectedNodes]
modelProjectionMatrix Mat33
modelProjectionTransform Vec3
textureFiltering u32, textureClamping u32, textureType u32,
coordinateGenerationType u32
sourceTextureRef i32
clippingPlane u8
unknownVector Vec3, unknownFloat f32
ps2L i16, ps2K i16
[v4 only (≤ 0x0401000C): unknownShort i16]
```
1,694 in 9.3.5. The era's "blink" class = static environment-map effects —
0 of 1,749 effect edges carry controllers (honest negative; no fake blink).

## NiCamera — CONFIRMED (standard Gamebryo layout; parser reads full chain)

## NiCollisionData — CONFIRMED (C22)

```
NiCollisionObject: target Ref
propagationMode u32
[v10: collisionMode u32]
useAbv u8
if 1: collisionType u32 + bounding volume:
  0 Sphere: center Vec3 + radius f32
  1 Box: center Vec3 + axis ×3 Vec3 + extent ×3 f32
  2 Capsule: center Vec3 + origin Vec3 + 2×f32
  5 HalfSpace: normal Vec3 + center Vec3
```
12 instances in 9.3.5.

## Particle systems — CONFIRMED (M1D-07..12, niflib-confirmed)

**NiParticleSystem** = NiGeometry (dataRef+skinRef+hasShader) +
```
[v10]: worldSpace u8 + numModifiers u32 + modifiers Ref[]
```
**NiMeshParticleSystem** = same (pure passthrough).

**NiPSysData** chain: NiGeometryData(v10) → NiParticlesData (hasRadii +
numActive u16 + hasSizes + hasRotations(quats ×4 f32)) → NiRotatingParticles
(v≤0x04020200 only: rotations2 — NOT PE v10) → NiPSysData (particle
descriptions: translation Vec3 + unknownFloats1[3] + 3×f32 + i32 per particle;
then unknownShort1, unknownShort2).

**NiPSysModifier base**: name SizedString + order u32 + target Ref + active u8

Modifiers/emitters in corpus (with own fields):
- AgeDeath (spawnOnDeath u8 + spawnModifier Ref), Spawn (8 fields), Position (none), BoundUpdate (updateSkip u16), ColorModifier (Data Ref), GrowFade (growTime f32, growGen u16, fadeTime f32, fadeGen u16), Gravity (gravityObject Ref + axis Vec3 + decay/strength f32 + forceType u32 + turbulence/turbulenceScale f32), Rotation (initialRotationSpeed f32 + randomInitialAxis u8 + initialAxis Vec3), MeshUpdate (numMeshes + meshes Ref[]), ColliderManager (collider Ref), DragModifier (dragLink + dragAxis + percentage/range/rangeFalloff f32)
- Emitters: Box (width/height/depth), Sphere (radius f32), Mesh (numEmitterMeshes + meshes[] + initialVelocityType u32 + emissionType u32 + emissionAxis Vec3) — all on the emitter base (speed/var, declination/var, planarAngle/var, initialColor Color4, initialRadius, lifeSpan/var) + volume emitter object link (v10)
- **NiPSysCollider base**: bounce f32 + spawnOnCollide u8 + dieOnCollide u8 + spawnModifier Ref + parent Ref + nextCollider Ref + colliderObject Ref; PlanarCollider adds width/height f32 + xAxis/yAxis Vec3

**Controller data**: NiPSysEmitterCtlrData (floatKeys KeyGroup\<f32\> +
numVisibilityKeys u32 + keys time f32 + u8)

Fun corpus fact: of the 33 dangling ArkTexture IDs, 18 are SuperSpray
particle slots (3 missing BNT2 ids × 6) and 15 are individual unshipped BASE
slots (incl. Outpost2_Hospital_dark_0) — texture IDs that do not exist in
Textures.bnt (pre-loop M3-4 R2 canon, refined in
PE_ASSET_CENSUS_R1_20260905_200000; 69/69 flip models + the era's particle
texture convention unchanged).
