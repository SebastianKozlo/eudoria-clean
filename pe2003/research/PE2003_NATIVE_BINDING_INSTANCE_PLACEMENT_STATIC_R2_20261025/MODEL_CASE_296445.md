# MODEL CASE — 296445 (def 4508)

RUN_ID: PE2003_NATIVE_BINDING_INSTANCE_PLACEMENT_STATIC_R2_20261025 | Authoring: 2026-10-25T11:18:13Z | Evidence: B01_*, B02a_*, J01a_*, J01b_*, J02_*, P01_*, P02_*, J03_*, J04_* (+ QC verification items)

## Identity

- Model resource id **296445**; NIF 296445.nif (108876 B, SHA256 656795D8B3DDDF8F9192EE41C4710D592894860F6959B53B2C08036977E7B862, NetImmerse 4.1.0.12, **155 blocks**: 30 NiTriShape, 30 NiTriShapeData, 22 NiTexturingProperty, 19 NiNode, 17 NiMaterialProperty, 10 NiZBufferProperty, 10 NiAlphaProperty, 7 NiArkBillboardNode, + extras).
- VM definition **4508** (4508.obj.dec 3640 B, SHA256 B6C96E9CCB2763C18644BC8BA5268B1FA63BCC28A738544225E276F4D3FFC9F3; header A=4751 forwarder, B=296473; **26-part construction def**).

## Model-id channel (J02, CONFIRMED)

- 4508 NYD DYN recs: ctor {296479, 162187, 0xA5222B37, @332}; **getter → 296445** = DYN rec {296478, f1=1617, 0x585DAF8C, @248} with literal STOREI_SPoff@272 [20, 296445] (bytes `de fe 00 77 14 00 00 00 fd 85 04 00`; instruction starts at file offset 0x294, id operand at 0x298 — erratum R2-E03); sibling getter {296477, f1=1611, 0x9FA86861, @164} → 296446; name-getter {296476, 7769, @20}. (J02's dyn_tables_raw_bytes is the corrected source; B02a's f1/f2 transposition for these recs is a visible frozen defect — CORRECTION_LEDGER R2-CLR-04.)
- Value flow: literal → [SP+20] → C → RET across the DYN dispatch boundary; **no in-file consumer** (0 EXTN bindings, 0 CALL_IND, 0 in-file callers) → class **(e) MISSING_EDGE**. Bounded negative: 0 foreign raw LE32 hits for 13 target ids across the 1936-file corpus + EXE (residual: computed/non-literal encodings untestable statically).

## Chain & transform (B02a, J01b, P01, P02, J03, J04)

- Attach chain (COMMON plumbing, byte-decoded, bijection 10/10): per-part loop (26 parts; mesh names + part ext ids injected into part-object properties via patched selectors ext 122915/122889 owner 4653) → CALL_abs ext 30298 → 1796@1016 forwarder → dispatch slot @1120 → [comp+8] slot 0 → ext 33521 → 2202@532. No model-resource id literal anywhere in the chain.
- Native chain: pair+0xC → FUN_004918b0 → X (0x28 B, vt 0x5EBC1C) → owner=[X+0x14] (class 0x78, vt 0x5EBBEC; writer FUN_005b5380 @0x5b5433) ; [X+8] = NIF parse root = NiNode block-0 "Scene Root", vt 0x5E2A3C (install @0x407896).
- Transform sources: owner+0x6C/+0x70 = **NIF_FILE_LOCAL** (block reader overwrites ctor defaults −1.0f; consumed as record[0] targets by FUN_005068f0); node+0x2C rotation matrix + node+0x50..0x58 translation written by network-reachable FUN_005030c0 (×100.0f) on vt-0x5E2A3C-class GCE-registry nodes; **296445.nif local transforms all identity (19 NiNode transforms — no local placement data in the file)**.

## Verdict (carried exactly, not strengthened)

- WORLD placement: **NOT_RECOVERED** (WORLD_XYZ_RECOVERED=NO; no LOCAL→WORLD promotion).
- Instance join to the network-written nodes: **STILL_AMBIGUOUS** — family-level join ESTABLISHED (byte-identical installs 0x407896/0x405bdf; resolver FUN_00407440 at slot+0x50 of 13 family vtables); decisive missing edge = registry+0x3C root identity (+ owner+0x1C class; HOSTCALL case ids 4652/4653; ctx+0x50 append — see CLAIMS R2-C31, FRONTIER BLK-R2-01/02/03).
- Candidate record: HISTORICAL_INSTANCE_CANDIDATES.csv row 296445 (join_status STILL_AMBIGUOUS).
