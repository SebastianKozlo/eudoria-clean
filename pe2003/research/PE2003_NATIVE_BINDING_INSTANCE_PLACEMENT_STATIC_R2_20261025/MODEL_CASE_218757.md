# MODEL CASE — 218757 (def 4057)

RUN_ID: PE2003_NATIVE_BINDING_INSTANCE_PLACEMENT_STATIC_R2_20261025 | Authoring: 2026-10-25T11:18:13Z | Evidence: B01_*, B02a_*, J01a_*, J01b_*, J02_*, P01_*, P02_*, J03_*, J04_* (+ QC verification items)

## Identity

- Model resource id **218757**; NIF 218757.nif (56535 B, SHA256 C13D08736D7E778803E20A3105067448007F32D15290AF168F836CD99248AD98, NetImmerse 4.1.0.12, **62 blocks**: 14 NiTriShape, 14 NiTriShapeData, 12 NiNode, 9 NiTexturingProperty, 8 NiMaterialProperty, + properties/extras).
- VM definition **4057** (4057.obj.dec 2688 B, SHA256 EA93FCA93C5F46D133D272D61012963DB7F5F338F9558421994B73BD644945D3; header A=477 forwarder, B=218782; **18-part construction def**).

## Model-id channel (J02, CONFIRMED)

- 4057 NYD DYN recs: ctor {218787, 162187, 0xA5222B37, @188}; **getter → 218757** = DYN rec {218784, f1=1617, 0x585DAF8C, @104} with literal STOREI_SPoff@128 [20, 218757] (bytes `de fe 00 77 14 00 00 00 85 56 03 00`; instruction starts at file offset 0x1C4, id operand at 0x1C8 — erratum R2-E03); sibling getter {218783, f1=1611, 0x9FA86861, @20} → 218758. Header-B sibling 218782 (= PFIX#0 resource).
- Value flow identical to 4508: literal → [SP+20] → C → RET across DYN dispatch; **no in-file consumer** → class **(e) MISSING_EDGE**; same 1936-file corpus + EXE bounded negative (0 foreign hits; 218785/218786 ABSENT from all four chain files under tested representation classes).

## Chain & transform (B02a, J01b, P01, P02, J03, J04)

- Attach chain byte-identical to 4508's (COMMON plumbing; bijection 8/8; 18 parts; ext 30298 → 1796@1016 → dispatch slot @1120 → ext 33521 → 2202@532; zero literal model ids in the chain).
- Same native chain and same transform sources as MODEL_CASE_296445.md (pair → X → owner; [X+8] NiNode root vt 0x5E2A3C; owner+0x6C/+0x70 NIF_FILE_LOCAL; node rotation/translation written by FUN_005030c0 on GCE-registry vt-0x5E2A3C nodes). **218757.nif local transforms all identity (12 NiNode transforms — no local placement data in the file; 31/31 across both models).**

## Verdict (carried exactly, not strengthened)

- WORLD placement: **NOT_RECOVERED** (WORLD_XYZ_RECOVERED=NO; no LOCAL→WORLD promotion).
- Instance join to the network-written nodes: **STILL_AMBIGUOUS** — family-level join ESTABLISHED; no per-model identity anchor exists statically (0 foreign literal hits); decisive missing edges identical to the 296445 case (registry+0x3C root identity; owner+0x1C class; HOSTCALL case ids 4652/4653; ctx+0x50 append).
- Candidate record: HISTORICAL_INSTANCE_CANDIDATES.csv row 218757 (join_status STILL_AMBIGUOUS).
