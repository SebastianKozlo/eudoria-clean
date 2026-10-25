# INSTANCE TRANSFORM FLOW — R2 synthesis (static, byte-verified chain edges)

RUN_ID: PE2003_NATIVE_BINDING_INSTANCE_PLACEMENT_STATIC_R2_20261025 | Authoring: 2026-10-25T11:18:13Z
Sources: B02a_CHAIN_DECODE.json, J01a_WRITER_CENSUS.json, J01b_RECEIVER_FLOW.json + J01b_EXECUTOR_SEMANTICS.md, P01/P02, J03/J04. All VAs in the pinned EXE (imagebase 0x400000). LOCAL vs WORLD distinction maintained at every step.

## 1. VM-side construction (COMMON plumbing; per-model data injected per part)

4508/4057 per-part loop (26/18 parts; per-part mesh name + part ext id injected into part-object properties via bind-pass-patched selectors ext 122915/122889 owner 4653) → CALL_abs ext 30298 (slot patched; EXTN bijection 10/10 + 8/8) → 1796 CODE@1016 forwarder → CALL_IND_Aoff @1116 (slot 1120 patched to ext 33521 owner 2202 hash 2DB10D07) → [comp+8] slot 0 → 2202 CODE@532..804. The chain carries only runtime handles; **no literal model ids** (B02a). Part objects are VM objects — DISJOINT from the C++ node family (J03 CM2).

## 2. Native object chain (J01b → P01 → J04; reader sites byte-verified)

SceneInstancePair (vt 0x5E7534, +8 id) —[pair+0xC]→ P instance (vt 0x5E799C) → FUN_004918b0 → **X** (0x28 B, vt 0x5EBC1C, ctor FUN_005b5110) → owner = [X+0x14] (class 0x78, vt 0x5EBBEC; constructed by FUN_005b5380, store @0x5b5433); [X+8] = NIF parse root = NiNode block-0, vt 0x5E2A3C (install @0x407896; loader registry 0x619E78; J03), with dual provenance in the FUN_00521b60 else-branch (0x61A0C8 transient registry, FUN_004186a0). Alternative resolve-root: owner+0x1C (writer = owner vt slot+0x10 FUN_005b3cf0 @0x5b3d09, value = FUN_00403e80(arg); dispatched as [manager_vt+0x50] = FUN_00407440-family recursive name resolver; NOT the GCE hash registry; exact class OPEN — J04).

## 3. Transform field sources (P01 CONFIRMED / P02 CONFIRMED-STRONGLY_SUPPORTED)

- **owner+0x6C/+0x70 (and +0x50..+0x68, +0x74 gate): NIF_FILE_LOCAL** — NIF block reader (owner vt slot 3, FUN_005b38c0 region, version-gated stream reads; LEA instructions at 0x5b3ca9/0x5b3cb9 — erratum R2-E01) overwrites ctor defaults (−1.0f @0x5b2cf4/f7) from the <id>.nif file stream. Definition data; LOCAL only.
- **node+0x2C (3x3 rotation matrix, +0x2C..+0x4F) and node+0x50/+0x54/+0x58 (translation)**: written by FUN_005030c0 (network-reachable via FUN_005bbbd0 wire triplets → record[6] 0x48 struct → FUN_005977b0 pass-2 → entity 0x118 vt 0x5E4628 vslots; also called at GCE registry-add FUN_00502e80) on 0x130 B vt-0x5E2A3C objects; translation scaled ×100.0f (@0x50310a/0x50311e/0x503129; FMUL _DAT_005e412c); matrix copy REP MOVSD @0x5031b0-0x5031c1 (P02/J04).
- **NIF local transforms: identity (31/31 NiNode transforms across both pinned models)** — the NIF files carry NO local placement data.

## 4. Consumer / record emission (J01b CONFIRMED)

FUN_005068f0 (sole caller FUN_00506780): owner+0x74 gate → FLD owner+0x6C @0x506aab / +0x70 @0x506af0 (d9 40 6c / d9 40 70) → record[0] targets of fresh 0x14/0x18 record arrays; payload x,y,z from node+0x50/54/58; quaternion from node+0x2C via FUN_00545030 (matrix→quat). Executors: **DAT_A = FUN_005c27a0 (no-op)**; **DAT_B = FUN_00561ee0 → FUN_005541e0** quaternion normalizer (adjacent-pair dot<0 → −q flip; clamp to [−1,1]). Writers of the callback table: 15 lazy-init installers into 20 slots (beyond-raw BSS). Consumer side: FUN_00555470/FUN_005553f0 submit into the 0xFC transform-stream channel object → FUN_00556d70/FUN_00556ea0 register/store → FUN_00506e10 finalize. **Downstream drain beyond FUN_00506e10 remains OPEN (inherited R1 T3-d2).**

## 5. What the flow does NOT establish

No step connects a concrete 296445/218757 instance to concrete world coordinates: the VM chain has no model ids; the NIF files have identity transforms; the network-written nodes are family-joined but their object-identity link to our models is STILL_AMBIGUOUS (decisive edge: registry+0x3C root identity — FRONTIER BLK-R2-01). WORLD_XYZ_RECOVERED=NO; all NIF-derived values are LOCAL_PART_TRANSFORM at most; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; SOURCE_UNKNOWN.
