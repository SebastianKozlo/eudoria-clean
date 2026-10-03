# NOT_CHECKED — PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z

Honest coverage statement. "NOT_CHECKED" = this run did not examine it at all;
"NOT_ESTABLISHED" = examined within the stated scope but the claim is not
proven; "UNVERIFIED" = evidence exists but is not independently confirmed.

## Not checked (out of scope by contract or budget — next discriminators as
proposals only, NOT executed)

1. **NiStream / NIF loading bodies** (provider virtual bodies beyond the
   request pair): the physical open of <A>.nif remains
   STRONGLY_SUPPORTED-inherited; provider-chain internals were not decoded.
   Next discriminating experiment (DESIGNED_NOT_EXECUTED): decompile the
   {0x66,A} request's scheduler callback FUN_008BD720 and the
   ArkResourceManager provider for type 0x66 down to the NiStream load call,
   and byte-pin the NiStream counterpart against the Gb12 NiStream.cpp oracle.
2. **Gamebryo 2.3/2.6/3.2 oracles**: not needed for the three mechanisms used;
   if era-exact AttachChild/NiStream bodies are required (the Entropia engine
   generation is unidentified per NINODE_SLOT17), a later run may pin them.
3. **The slot objects of FUN_00848EA0** (3 x 0x18-stride slots with a vec3
   position): their object class and world semantics were not identified.
4. **FUN_00468910 (P03, 1,336 decompile lines, 9 callers)**: only its role as
   a message-area driver was recorded; not decomposed.
5. **World-instance claim paths beyond the census**: the 23 lookup callers'
   full downstream trees (avatar/UI/equipment/preview areas) were classified
   by decompile of representatives only, not exhaustively (denominator: 23
   callers / 25 sites, all listed in C2 T01).
6. **Templates.vfs list1 string payloads** beyond record 11963's first string
   ("leg_BASE") — the 16-string list was not decoded item-by-item.
7. **The 20002 payload+0x30 consumer**: unchanged from
   20002_PAYLOAD30_CONSUMER (bounded negative; no consumer identified within
   its census) — this run adds the id2-domain cross-check only, and does not
   re-open the consumer census (FAMILY-P not selected).
8. **Portals.bnt / TerrainEditZones.bnt / CWO-Logic handler tables
   0x00A7D8EC/0x00A7DA34 / hierarchy.vfs grammar**: untouched this run.
9. **Runtime behavior of ANY kind**: STATIC_ONLY run — nothing was executed.
10. **The full Models.bnt join**: re-used from JOIN R1 (3,618/3,618) with the
    anchor re-pinned; the full join was not re-run (bounded reuse, recorded).

## Not established (examined, not proven)

- Physical-record -> world-instance identity-preserving edge (the LEVEL-A
  blocker): within the censused construction machinery, no driver reads
  templates.vfs; id2/position inputs come from message/attribute/hardcode.
- World-instance semantic status of the placement records built by
  FUN_00567170/FUN_005B5F90/FUN_00567770 (CONTROL-2 FAIL → UNKNOWN).
- Model -> world-scene insertion beyond the LOD/attach state machine (E7).
- Producer of the attribute containers (H1/H2/H3/H4 boundary — unchanged
  from prior canon; the message-dispatcher evidence supports but does not
  prove H3 for the placement channel).
- Semantic role of D_f32 (124.941 for record 4508) — no consumer identified
  this run (inherited open item; not re-attacked).
- Entropia's engine generation (inherited NINODE_SLOT17 boundary).

## Budget consumption (fixed at 00_CONTROL/RUN_PLAN.md)

- Enumeration + census + trace + controls + oracle: ~41 analytical tool
  invocations total (2 identity/preflight, 1 C1, 9 Ghidra rounds C2-C9+C11,
  4 python instruments C10/C10v2/C12 + array probe, remainder reads of this
  run's own artifacts). Budgets: ENUMERATION ≤30 (used ~14 before selection),
  DEEP_TRACE ≤90 (used ~27), CONTROLS+ORACLE ≤30 (used ~10). No budget
  expansion after results.
- NEW_PCG_FUNCTIONS_DETAILED (instruction/decompile/dataflow analysis,
  including anchors/controls/extra-edge functions): 88 decompiled + probe
  functions < 120 limit. Machine xref census (45 census target lookups with
  caller enumeration) is reported separately above and is not deep trace.
- NEW_PHYSICAL_RECORDS_DETAILED: 3 (templates.vfs record 4508; templates.vfs
  record 11963; 20002.vfs record 0 re-pin) = limit.
