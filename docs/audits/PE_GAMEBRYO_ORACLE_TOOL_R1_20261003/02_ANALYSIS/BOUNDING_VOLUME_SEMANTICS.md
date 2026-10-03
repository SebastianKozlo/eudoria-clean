# BOUNDING_VOLUME_SEMANTICS — PE_GAMEBRYO_ORACLE_TOOL_R1_20261003 (Batch E1, order s15)

Answers the s15 questions from source only (no executed loader in E1). Cited
files: GB12 = Gb12_Source CoreLibs; GB26 = Gb26_src; file SHA256s in
NIF_LOAD_PIPELINE.md section 0 unless stated otherwise.

## Q1: Is the bound serialized or recomputed? — BOTH, different bounds (per version)

| Bound | GB_1_2 | GB_2_6 | GB_1_1_2 / GB_2_3 |
|---|---|---|---|
| Model-space sphere bound (NiBound) | **SERIALIZED** inside NiGeometryData blocks: `m_kBound.LoadBinary(kStream)` at NiGeometryData.cpp L618; format = center 3x f32 + radius f32 (NiBound::LoadBinary, NiBound.cpp L163-167; SaveBinary L169-173 mirrors) | **SERIALIZED**, same place/shape: NiGeometryData.cpp L279 -> NiBound::LoadBinary L342-346 | NiBound::LoadBinary/SaveBinary DECLARED in headers (GB112 NiBound.h sha A6ECE63F L68-69; GB23 recovered NiBound.h sha E5ED6E25 L68-69 "Emergent internal use only") — binary impl; serialization implied by 1.x/2.x lineage = UNVERIFIED for these binary SDKs (E2 executed test) |
| World bound (NiAVObject::m_kWorldBound) | **NOT serialized** — NiAVObject::LoadBinary (L546-699) reads NO bound; recomputed at update time | NOT serialized; recomputed | — (binary; header declares `NiBound m_kWorldBound` GB112 NiAVObject.h L229-230) |

## Q2: At which stage is the recomputed bound produced?

- **Update stage, not load stage**: `NiAVObject::UpdateDownwardPass` calls
  `UpdateWorldData()` then `UpdateWorldBound()` (GB12 NiAVObject.cpp L128-132;
  GB26 L178-181). NiNode::UpdateDownwardPass computes the node bound inside its
  children loop (GB12 NiNode.cpp L226-276: `m_kWorldBound.SetRadius(0.0f)` L243,
  first visual child copies, subsequent `Merge` L262-269; GB26 L311-333 same
  merge logic in UpdateWorldBound). Link/PostLink phases contain NO bound
  computation (verified in NiObjectNET/NiNode LinkObject/PostLinkObject bodies
  quoted in NIF_LOAD_PIPELINE.md).
- `NiAVObject::UpdateWorldBound` base is an inline no-op stub (GB12
  NiAVObject.inl L226-230; GB26 L265-269; GB112 L211-215) — only leaves
  (NiGeometry via NiBound::Update(bound, transform), NiBound.h L47) and nodes
  compute bounds.
- `IsVisualObject() == (m_kWorldBound.GetRadius() != 0.0f)` (GB12 inl L232-235;
  GB26 L271-274; GB112 L217-219) — a zero-radius world bound means "not visual"
  and is excluded from the parent merge.

## Q3: In which coordinate system?

- The **serialized** NiBound (NiGeometryData.m_kBound) is in **MODEL space**
  (it travels with the vertex data of the geometry data object; the world
  version is produced by applying the world transform — `NiBound::Update(const
  NiBound& kBound, const NiTransform& kXform)` declared NiBound.h L47, called by
  the geometry's UpdateWorldBound path).
- The **recomputed** m_kWorldBound is in **WORLD space** (computed after
  UpdateWorldData applied parent chain transforms; NiNode merges children's
  WORLD bounds directly — no re-transform, GB12 NiNode.cpp L260-269).
- The collision ABV (NiBoundingVolume tree) has an explicit model/world pair:
  `UpdateWorldData(const NiBoundingVolume& kModelABV, const NiTransform& kWorld)`
  is pure virtual (GB112 NiBoundingVolume.h sha C6172DB2 L96-99; GB26 header
  same contract) — model ABV serialized, world ABV recomputed.

## Q4: Does the root bound represent the whole asset?

- **In the FILE (all source versions): NO.** There is no serialized root bound:
  NiAVObject/NiNode LoadBinary read no bound; only per-NiGeometryData model
  spheres are serialized. (A file's "dimensions" are therefore only derivable
  by combining per-geometry model bounds with the transform hierarchy — the
  E2 218757 probe must do exactly that, in GAME_UNITS.)
- **At RUNTIME (GB_1_2 and GB_2_6, source-proven): YES, after a full
  UpdateDownwardPass from the root** — NiNode::UpdateWorldBound merges every
  visual descendant's world bound (first-copy-then-Merge, GB12 L394-416 / GB26
  L311-333), so the root node's m_kWorldBound covers the whole subtree that was
  updated. Caveat (source text): the merge starts from radius 0 and skips
  non-visual objects; an un-updated graph has radius 0.

## NiBoundingVolume / NiBoxBV / NiSphereBV mechanics (era-separated)

- **Factory + type tag:** `NiBoundingVolume::CreateFromStream(NiStream&)` reads
  an `int` type tag, bounds-checks it against MAXTYPE_BV, and dispatches through
  `ms_apfnLoaders[type]` (GB12 NiBoundingVolume.cpp L143-154, sha
  0DEFE7C93B7F6EEC31D98E97BFB7BE607CA8E1E2E143FF51E831343E1CEAF15D; GB26
  NiBoundingVolume.cpp L157-168, sha BE859A794C8A371D5674C1A7A5C17CE00FA30374CE7F01CBD067007D8BE416DB).
  `NiBoundingVolume::LoadBinary` is EMPTY ("'type' is loaded by CreateFromStream",
  GB12 L156-158); `SaveBinary` writes `Type()` (GB12 L161-165).
- **BoundType enum** (GB112 NiBoundingVolume.h L75-85, sha C6172DB2...; GB23
  recovered header L31-33 macro): SPHERE_BV=0, BOX_BV=1, CAPSULE_BV=2,
  LOZENGE_BV=3, UNION_BV=4, HALFSPACE_BV=5.
- **NiBoxBV::LoadBinary** = base + `m_kBox.LoadBinary` (GB12 NiBoxBV.cpp L2107-
  2111, sha 8A66D75DCEC050DD0D016F41967951545DDA37DE9EE0FD69C0BA270EC65E6C21;
  GB26 L1886-1890, sha 82A6D2AC647EB7E674C6372D2FC6B97DB81A6462797AC37CC63F3A3EBA1CF6A6).
- **NiSphereBV::LoadBinary** = base + `m_kSphere.LoadBinary` (GB12
  NiSphereBV.cpp L432-436, sha CFB89DFD209CD29EF466ED2B44465E8933AB6C0F2F91E2B619DF1499B3EC6104;
  GB26 L420-424, sha F8A94D6BDD3471C8AD1C2D90C0AB9FC1A67E24F06A93062D1B30099A502C8DE8).
- **Library boundary (quote):** "NiMain supports only sphere bounding volumes.
  To use the other bounding volumes, an application needs to link in the
  NiCollision library." (GB112 NiBoundingVolume.h L72-74; the NiCollision
  classes NiBoxBV/NiCapsuleBV/... live in CoreLibs\NiCollision for GB_1_2/GB_2_6.)
- ABVs attach through the serialized collision linkID (NiAVObject::LoadBinary
  GB12 L675 / GB26 L541 -> NiCollisionData), not through the world-bound path.

## Dimension-reporting rule for the E2 218757 probe (binding consequence)

Report dimensions in GAME_UNITS only; they must come from either (a) the
serialized per-geometry model bounds combined with SERIALIZED_LOCAL_TRANSFORM
chains (file-derived, static), or (b) a full runtime UpdateDownwardPass world
bound (GB_1_2/GB_2_6 source semantics). Neither is a meter scale until the
world scale is CONFIRMED (order s15).
