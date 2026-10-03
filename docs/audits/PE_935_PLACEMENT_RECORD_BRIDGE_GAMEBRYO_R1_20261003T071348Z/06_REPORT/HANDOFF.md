# HANDOFF — PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z

Executor: pe-reconstruction (bounded worker contract from PE-MASTER, no
nested dispatch). This document is the return-to-parent handoff.

## Science result (one paragraph)

For the SELECTED family (templates.vfs registry-template family), the run
statically demonstrates — byte-pinned at every load-bearing step, with two
check methods per edge (Ghidra listing + raw-EXE readers) — the chain:
physical record id2=4508 (file_offset 96,496; payload bytes incl.
A=296445 @96,516 `fd 85 04 00`) -> reader/parse (field order id2,A,B,C,D_f32
+ string-list1 + u32-list2 + f11) -> RB-tree registry (DAT_00BA1824, key
id2@node+0x10, value@node+0x14) -> lookup FUN_0072F580 -> A-read via
FUN_007CE1E0 with pinned ECX provenance -> request pair {0x66=MODEL, A} ->
scheduler queue (callback 0x008BD720) -> (data join) "296445.nif" in
Models.bnt (anchor re-pinned @395,268,773). The placement-construction
machinery that turns templates into positioned runtime records (FUN_00567170
/ FUN_005B5F90 / FUN_00567770; setters +0x08/+0x14/+0x20/+0x24 byte-pinned)
is driven by message dispatch (FUN_004B18D0, types 0xA2..0xC7), runtime
attributes (class-20006 property tag 6), or hardcoded id2 immediates (PUSH
0x3ED3) — NONE of the censused drivers reads templates.vfs, so the
physical-record -> WORLD-INSTANCE identity edge is NOT ESTABLISHED:
RESULT_LEVEL = B (partial resource/scene chain), with MODEL_ID_RECOVERED =
YES (A=296445) and PLACEMENT_XYZ_RECOVERED = NO. The pending-attach
operations were behaviorally REJECTED as Gamebryo AttachChild (they are an
Ark LOD/attachment state machine) — CONTROL-3; the scene root
("NetImmerseScene::Root") naming was pinned against the Gb12 oracle
(STRONGLY_SUPPORTED), and the historical NiNode slot-17 anchor re-pinned
MATCH. One in-run identity correction: the 0x110 "named instance" is
NiControllerSequence (RTTI), not a model instance class.

## Status block

```text
RUN_ID = PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z
BASE_SHA = 743f9fac2dd5c9e94eaba074b46903b4d3686b46
HEAD = BASE (no commits/staging by this executor)
REMOTE_STATE_AT_START = live master = BASE_SHA (ls-remote at preflight;
  no change observed during the run)
RUN_STATUS = COMPLETE (science close; Level B; budgets not exhausted)
HARD_STOP_REASON = end of bounded executor task (publication intentionally
  NOT started: fresh QC -> advisory PE_MASTER review -> entrypoint row ->
  final manifest -> commit/push are the later phase per the dispatch)
CANONICAL_GATE_EFFECT = NONE; M1_CLOSED = NO; Q1_STATUS = UNCHANGED;
NEXT_EXPERIMENT_AUTHORIZED = NO
```

## Package contents (this run's files; the publishing phase will regenerate
the final MANIFEST and add the entrypoint row)

- 00_CONTROL: AUTHORIZATION.md (verbatim human message + provenance),
  PREFLIGHT.md (all pins/exit codes), RUN_PLAN.md (fixed budgets)
- 01_RAW: C1_CENSUS.json, C2_CALLER_CENSUS.json, C3_DECOMP.json,
  C4_CONSTRUCTION_TRACE.json, C5_LAYOUT_AND_DRIVERS.json, C6_DRIVER_SOURCES.json,
  C7_LISTS_AND_ATTACH.json, C8_TOP_SOURCES.json, C9_LISTING_WINDOWS.json,
  C10_BYTE_PINS.json, C10V2_BYTE_CROSSCHECK.json, C11_ORACLE_COUNTERPARTS.json,
  C12_NINODE_VTABLE_REPIN.json
- 02_ANALYSIS: SELECTION.md, TRACE_EDGE_BLOCKS.md, CLAIM_MATRIX.csv,
  NOT_CHECKED.md, RETRACTIONS_SUPERSESSIONS.md
- 03_SCRIPTS: c1..c12 instruments (13 scripts, all read-only vs originals)
- 04_CONTROLS: CONTROLS.md
- 05_ORACLE: ORACLE_RECORDS.md
- 06_REPORT: DRAFT_FINAL_REPORT.md, HANDOFF.md, artifact_index.csv

## For the fresh-context QC (suggested falsification targets)

1. E1 parse order: re-derive the payload->object field mapping from raw
   bytes alone (the 28-B record is fully determined: 5 u32 + 2 zero u16
   counts + zero f11).
2. E3 ECX provenance: re-check 0x006C3F60-0x006C3F74 bytes (MOV ECX,EAX /
   MOV ECX,EDI) and try to find an alternative path where the getter is
   called with a different ECX in the same function.
3. CONTROL-2: attempt to rescue the world-instance claim by finding any
   construction driver that reads a file (the census denominators are in
   C2 T02: the templates reader has exactly 1 caller).
4. R-1 (NiControllerSequence): confirm the RTTI symbol in O03 is not a
   decompiler hallucination (the symbol comes from the binary's RTTI).

## Next experiments (proposals ONLY — not authorized, not designed in detail)

1. Decode FUN_008BD720 + the type-0x66 provider chain to the NIF load
   (closes the model-load body; NiStream oracle comparison).
2. Decode the class-20006 property-tag-6 WRITERS (who sets the id2 that
   FUN_00848EA0 consumes) — if ever file-fed, the P/T families merge into a
   physical-record->placement channel.
3. The two missed items from the shortlist (FAMILY-P consumer decode;
   FAMILY-A attribute producer H1/H3/H4 backward slice) remain open as
   before, with this run's census adding the message-dispatch evidence.

## Boundaries honored

- STATIC_ONLY; no client launch; no dynamic instrumentation; no engine/SDK
  execution; no production parser changes; no repository creation; no
  stage/commit/push; AUDIT_ENTRYPOINT.md untouched; foreign untracked groups
  untouched; original game files read-only (0 modifications); Ghidra project
  worked on a run-local copy outside the repo; oracle payloads kept out of
  the repo (locators + hashes + short derived descriptions only).
