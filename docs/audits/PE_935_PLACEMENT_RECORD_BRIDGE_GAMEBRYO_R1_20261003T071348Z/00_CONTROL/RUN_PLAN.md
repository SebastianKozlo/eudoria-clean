# RUN_PLAN — PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z

## Enumeration scope (finite, per contract §3)

Concrete existing inventory used as enumeration roots:

1. **Client binary** (Entropia.exe 9.3.5, pinned) — the only code universe for this run.
   Machine census denominators are reported separately per census.
2. **PCG 9.3.5 physical data corpus** (pcg_install\Data):
   - Parameters\*.vfs (27 files, per JOIN R1 census) — parameter/template registry family
   - Models\Models.bnt (BNT2, A→<A>.nif index) — resource side
   - Volumes\Volumes.bnt (B→<B>.bvi) — collision side (not a placement candidate)
   - Portals.bnt / TerrainEditZones.bnt — spatial candidates (NOT decoded in this run
     unless the selected trace requires it; NOT a separate census)
3. **Registration/factory sites** (from prior canon, to be re-pinned where load-bearing):
   - ArkObjectClass registry (class-ID→factory), ArkObject ctor FUN_00726E70,
     factory FUN_0070BF50 (vtable slot 1)
   - templates.vfs registry RB-tree DAT_00BA1824, lookup FUN_0072F580
   - ArkResourceManager stores (.nif/.bvi/.amu/.tdf/.prt/.tez/portals.bnt/TEZ) at RM-init
     FUN_0041DAE0
   - Model request pump FUN_006C9700 ({0x66=MODEL, id=A}), instance creator FUN_006CB6F0,
     named-instance FUN_006CB020, pending-attach FUN_006CB3C0
   - Scene root "NetImmerseScene::Root" (FUN_00933310 area)

Statically observed classes ≠ all client classes; census counts are reported with their
own denominators. Full Ark registry recovery is OUT OF SCOPE.

## Budget (fixed BEFORE analysis; NOT expandable after results)

- ENUMERATION budget (census + shortlist + selection): max 30 tool invocations
- DEEP_TRACE budget (re-pins + new traces + Ghidra rounds): max 90 tool invocations
- CONTROLS + ORACLE budget: max 30 tool invocations
- Hard contract limits respected: SHORTLIST_FAMILIES_MAX=3, DEEP_TRACE_FAMILIES_MAX=1,
  ORACLE_MECHANISMS_MAX=3, NEW_PCG_FUNCTIONS_DETAILED_MAX=120 (detailed =
  instruction/decompile/dataflow analysis, incl. anchor/control functions),
  NEW_PHYSICAL_RECORDS_DETAILED_MAX=3, QC_REPAIR_ROUNDS_MAX=1.
- Estimated wall time: single bounded work session; on limit reached → PARTIAL_COVERAGE /
  STATIC_BOUND recorded with remaining unknowns. No budget expansion after seeing results.

## Shortlist (drafted from call/dataflow evidence in leads; final selection recorded in 02_ANALYSIS/SELECTION.md AFTER census)

1. **FAMILY-T: templates.vfs registry-template family** — physical file registry,
   5,438 records, id2→A→<A>.nif join CONFIRMED by JOIN R1 (3,618/3,618); consumer chain
   byte-pinned (FUN_0072F580 lookup → FUN_007CE1E0 getter A → FUN_006C9700 pump →
   ArkResourceManager → BNT2). Unknowns: which caller drives world statics (0/38 census
   in STATIC_INSTANCE_TRACE), transform producer, template→scene attach edge.
2. **FAMILY-P: 20002.vfs tag-0x11 parameter-slot family** — physical record pinned
   (record 0, payload+0x30, BB 2E 00 00 = 11963), parser→slot CONFIRMED (SELECTED reader
   FUN_009777F0), destination CONFIRMED (value_array[21]); consumer OPEN (202-site
   census negative); id2-domain overlap 1,364/1,366 (JOIN R1 §9) = candidate registry
   reference channel. Unknowns: consumer of slot 21; whether the family leads anywhere
   near world objects (class is ArkParameterArmor — likely avatar-equipment endpoint,
   NOT world-instance-shaped).
3. **FAMILY-A: attribute-tree placement-record family** — runtime placement record
   (position@+0x08, rotation@+0x14, variant u16@+0x34) built by FUN_00567770 from
   attribute tree (FUN_00846840, IDs 0x6A4/0x6A5/0x6A8/0x6A9), setters FUN_00730F90/FB0/FD0
   byte-pinned; instance materialized as ClientMovableObject. Unknowns: upstream producer
   of the attribute container (H1 local file / H3 network / H4 hybrid — unresolved);
   physical record NOT pinned (if producer is network, no physical record exists on disk).

Ranking principle: call/dataflow density + ability to pin a physical source; NOT name-based
(World/Object/Position), NOT numeric-domain overlap, NOT building-promise.

## Deep-trace plan (ONE family; selection finalized after census in SELECTION.md)

Planned trace chain shape (if FAMILY-T selected):
physical record bytes → reader/lookup → template object → consumer (ArkObject ctor /
placement-record builder) → model request → model instance creation → named instance →
pending-attach → scene/transform edge. Gamebryo oracles (max 3 mechanisms) support the
RIGHT side: candidate mechanisms = NiStream LoadBinary (model resource load),
NiNode AttachChild (scene attach), NiAVObject UpdateWorldData (local→world transform).

## What is explicitly NOT studied as separate goals

ArkObjectClass/ArkRTTraits genealogy; all Gamebryo generations; all traits; all numbered
VFS files; schema-wide decoder; automatic placement reconstruction; cosmetic QC-R4
per_artifact.failed repair; closed Gate C audits / QC-R4 re-runs.
