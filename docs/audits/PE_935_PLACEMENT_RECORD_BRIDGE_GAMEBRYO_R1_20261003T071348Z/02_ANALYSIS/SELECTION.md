# SELECTION — PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z

Shortlist (SHORTLIST_FAMILIES_MAX=3) ranked by call/dataflow density and ability to pin
a physical source (NOT by names, numeric-domain overlap, or building promise).
Own measurements: 01_RAW/C1_CENSUS.json (physical), 01_RAW/C2_CALLER_CENSUS.json (code).

## FAMILY-T: templates.vfs registry-template family

- Source relation: templates.vfs — physical file pinned this run (560,788 B, SHA256
  BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77, ArkVFS02, base=36,
  5,438 records walked to exact EOF, 0 CRC fail — C1). Record id2=4508 pinned at byte
  level: file_offset 96,496, payload 28 B, A=296445 @file 96,516 bytes `fd 85 04 00`,
  B=296446, C=0, D_f32=124.94100189208984.
- Registration/factory: RB-tree registry (DAT_00BA1824 root, per prior canon); lookup
  FUN_0072F580 = map-find idiom returning node+0x14 (template object), default
  DAT_00BA5800 on miss (decompiled D01 this run). ArkObject factory FUN_0070BF50
  (vtable slot 1) = new(0x58) -> ArkObject ctor FUN_00726E70 (decompiled D03/D04 this
  run): template object -> this+0x04; A = getter FUN_007CE1E0 ([template+0x08]) ->
  entity+0x28; param_2 -> this+0x2C; zeros +0x30..+0x54.
- Parser lead: reader FUN_0072FA30 (1 caller — T02); CONFIRMED at record level by
  C1 walk (5,438/5,438 EOF-exact) + JOIN R1 prior.
- Consumer lead (own C2 census): lookup 25 callsites/23 callers; ArkObject ctor
  55 callsites; model pump FUN_006C9700 13 callsites/11 callers; instance creator
  FUN_006CB6F0 2; named-instance FUN_006CB020 1; pending-attach FUN_006CB3C0 2.
- Unknowns: which caller creates a WORLD instance from a registry template (prior
  bounded census: 0/38 placement-driven); scene attach target; instance transform
  producer; relation of D_f32 (124.941 for 4508) to any placement quantity.

## FAMILY-P: 20002.vfs tag-0x11 parameter-slot family

- Source relation: 20002.vfs (pinned: 174,864 B, SHA256 C3899C3E..., 1,366 records,
  base=128, EOF-exact — C1) -> ArkParameterArmor instances (class 20002; per
  20002_PAYLOAD30_CONSUMER: SELECTED reader FUN_009777F0 read VA 0x00977807
  `8B 04 10`, store VA 0x00977810 `89 02` -> value_array slot 21 = [instance+0x40]+0x54).
- Physical record pinned: record 0 header_id 0x05B80001, payload 56 B (C1 own bytes),
  tag-0x11 value at payload+0x30 = `bb 2e 00 00` = 11963 (re-pinned this run).
- Cross-family observation (C1 own measurement): payload+0x30 column of all 1,366
  records: 1,364 values ∈ templates.vfs id2 set, 2 misses = [0,0] (the two zero
  records). id2=11963 EXISTS in templates.vfs (file_offset 315,916, size 382, A=551661,
  payload contains string "leg_BASE"; 551661.nif EXISTS in Models.bnt index
  @name_file_offset 395,323,507).
- Consumer lead: generic property machinery (getter family FUN_00726450/90/26510/...;
  202 descriptor-lookup sites censused by 20002_PAYLOAD30_CONSUMER; NO tag-0x11 reader
  identified within that bounded census).
- Unknowns: consumer of value_array slot 21; semantic role. Evidence shape (leg_BASE
  string in the referenced template payload) points to avatar/body-part models, NOT
  world objects.

## FAMILY-A: attribute-tree world-construction family

- Source relation: attribute tree FUN_00846840 (attribute IDs 0x6A4/0x6A5/0x6A8/0x6A9)
  -> placement builder FUN_00567770 (which BOTH calls registry lookup FUN_0072F580
  @0x0056736D AND the BASE-object builder FUN_004C5580 @0x005678BA — own C2 census)
  -> placement-record setters FUN_00730F90/FB0/FD0.
- FUN_004C5580 (decompiled D02 this run): builds named objects "Level01_0_BASE",
  "volume_0_BASE", "placename_0_BASE", "GeoText_0_BASE", "face_0_BASE" via
  FUN_00730e50 (name->object) + FUN_00730b30 (register), gated by attribute flags
  0x657/0xd82/0x2140/0x3d1c. 10 callers (C2).
- Consumer lead: setters byte-pinned (prior); placement record {position@+0x08,
  rotation@+0x14, pair@+0x20/+0x24, variant u16@+0x34}.
- Unknowns: producer of the attribute container (H1 local file / H3 network / H4 —
  unresolved; prior census found no placement table in the 27-file Parameters corpus);
  NO physical record on disk is currently pinned for this family; whether FUN_004C5580's
  BASE objects are world instances or template/asset-local constructs is UNDETERMINED.

## DECISION (before deep trace; no substitution after unfavorable results)

**SELECTED_FAMILY = FAMILY-T (templates.vfs registry-template family).**

Selection reason:
1. It is the only family where BOTH ends are already pinned by this run's own
   measurements: a physical record byte-pinned in a corpus file (4508 @96,496; A bytes
   `fd 85 04 00` @96,516) AND a byte-proven consumer chain exists on the code side
   (lookup -> getter -> pump -> ResourceManager -> BNT2 per JOIN R1, re-pinned this run
   at the census level).
2. Highest dataflow density with clean denominators (25/23 lookup, 55 ctor, 13/11 pump
   callsites — own C2), making the open edges statically measurable rather than
   speculative.
3. The open edges are narrow and concrete: (a) which caller(s) turn a registry template
   into a runtime entity/instance; (b) whether the entity's model request and attach are
   identity-preserving from the record; (c) any transform edge. These map directly to
   the contract's edge-block format.
4. Gamebryo oracles have a defined role on the right side of THIS family's chain
   (NiStream LoadBinary for model load, NiNode AttachChild for attach,
   UpdateWorldData/m_kLocal for transform) — max 3 mechanisms.

FAMILY-P is NOT selected: its endpoint evidence (leg_BASE body-part template; armor
parameter class) points away from world-instance semantics; even a full success would
not answer the PRIMARY_QUESTION about world objects. The C1 cross-family observation
(1,364/1,366 id2-domain membership) is recorded as a CANDIDATE observation only.

FAMILY-A is NOT selected: no physical on-disk record is pinned for it; its producer
boundary (H1/H3/H4) is unresolved, so a deep trace risks ending with no physical-record
edge at all. Its FUN_004C5580 finding (named BASE objects) is recorded here as a lead
for future runs.

DEEP_TRACE_FAMILIES = 1 (FAMILY-T). No candidate substitution after unfavorable
results; no second deep trace.

## Budget reminder (from 00_CONTROL/RUN_PLAN.md; unchanged)

ENUMERATION ≤30 invocations; DEEP_TRACE ≤90; CONTROLS+ORACLE ≤30.
Census consumption so far: ~14 tool invocations (preflight+pins+census+2 Ghidra rounds
of which 1 was C2). Deep-trace budget: 90 invocations from here.
