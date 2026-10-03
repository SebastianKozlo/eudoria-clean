# DRAFT FINAL REPORT — PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z

> DRAFT: this report is the executor's science-close draft. Fresh-context QC,
> advisory PE_MASTER review, entrypoint row, final manifest and publication
> happen AFTER this task returns (dispatch boundary: no commit/push/stage).

```text
HARD_STOP = YES (end of the executor's bounded task; publication is a separate phase)
RUN_ID = PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z
BASE_SHA = 743f9fac2dd5c9e94eaba074b46903b4d3686b46
INPUT_BUILD_SHA256 = E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
  (physical source pins used: Entropia.exe (above); templates.vfs
  BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77 (560,788 B);
  20002.vfs C3899C3E88D72CE12CEF9B8A4F5E73B26632BB1A3207C950FF2BC40FD9C94AC4
  (174,864 B); Models.bnt C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0
  (395,412,868 B, index metadata only); NiMain.lib FF4519AFD2475D9A6E71A35E5DB6B0F5A0B7E9E86EC3662C6A340DA19BA06597
  (3,073,590 B); Gb12 source tree (per-file locators in 05_ORACLE).)
PRIMARY_QUESTION = For ONE selected PCG 9.3.5 data family, can a chain be
  statically demonstrated from a concrete PHYSICAL RECORD, through the
  original client, to a world-object instance and its resource/model or
  transform?
ENUMERATION_SCOPE = finite: the pinned 9.3.5 client binary + the templates.vfs
  registry family + the 20002.vfs cross-family candidate + Models.bnt index;
  registration sites/factories: RB-tree registry DAT_00BA1824 (lazy singleton
  FUN_0043A550), ArkObject factory FUN_0070BF50/new(0x58)/ctor FUN_00726E70,
  RM-init store registrations (inherited), model request pump FUN_006C9700,
  instance creator FUN_006CB6F0, named-instance FUN_006CB020, pending-attach
  FUN_006CB3C0, scene root FUN_00933310. Full Ark registry recovery OUT of scope.
COVERAGE = own machine census: 45 = 19+10+4+8+4 census-target caller
  enumerations (C2=19, C4=10, C5=4, C6=8, C8=4; denominators reported per
  target in the C2/C4/C5/C6/C8 JSONs);
  88 functions decompiled (detailed) of the client's ~13.5k functions — the
  deep trace is FAMILY-local, not client-global; 962/962 listing instructions
  byte-verified against the raw EXE; 113/113 call/imm targets recomputed from
  raw bytes.
NOT_CHECKED = see 02_ANALYSIS/NOT_CHECKED.md (10 items, incl. NiStream bodies,
  slot-object classes, provider chain, 2.3/2.6/3.2 oracles, full Models.bnt
  join re-run, CWO tables, runtime anything).
SHORTLIST = FAMILY-T (templates.vfs registry-template family; SELECTED),
  FAMILY-P (20002.vfs tag-0x11 parameter slot family; NOT selected —
  endpoint evidence points to avatar body-part models, not world objects),
  FAMILY-A (attribute-tree world-construction family; NOT selected — no
  physical on-disk record pinned; producer boundary H1/H3/H4 unresolved).
SELECTED_FAMILY = FAMILY-T (templates.vfs).
SELECTION_REASON = the only family with BOTH ends already pinned by this
  run's own measurements (physical record bytes 4508@96,496 incl. A bytes
  fd 85 04 00 @96,516; byte-proven consumer chain on the code side) and the
  highest dataflow density with clean denominators (25/23 lookup, 55 ctor,
  13/11 pump callsites — own census), making the open edges statically
  measurable; Gamebryo oracles had a defined role on its right side.
FUNCTIONS_DETAILED_COUNT = 88 (limit 120; anchors/controls/extra-edge
  functions included in the count; machine xref census reported separately)
RECORDS_DETAILED_COUNT = 3 (templates 4508; templates 11963; 20002 record 0
  re-pin) (limit 3)
BUDGET_SET = ENUM ≤30 / TRACE ≤90 / CONTROLS+ORACLE ≤30 tool invocations
BUDGET_REACHED = NO (used ~14/~27/~10; no budget expansion after results)
ORACLES_AND_MECHANISMS_USED = Gb12 source (NiNode.cpp:34 ctor, :52 AttachChild;
  NiObjectNET.cpp:112 SetName) + NiMain.lib 1.1.2 (identity-pinned; prior
  NINODE_SLOT17 vtable canon reused as labeled historical control). 3
  mechanisms: (1) NiObjectNET::SetName / NiNode ctor (scene-root naming)
  STRONGLY_SUPPORTED; (2) NiNode::AttachChild as NEGATIVE matcher for the
  pending-attach thunks (REJECTED as AttachChild; confirmed Ark LOD state
  machine) — CONTROL-3; (3) UpdateWorldData-shaped slot 27 (transform
  target semantics) STRONGLY_SUPPORTED with a disclosed probe-window
  discrepancy vs the historical rep-movsd description.
PHYSICAL_RECORD_IDENTITY = CONFIRMED: templates.vfs record id2=4508,
  file_offset 96,496, header {id=4508,size=28,ver=1,crc=AFF5797C}, payload
  28 B {id2=4508, A=296445, B=296446, C=0, D_f32=124.94100189208984,
  list1_count=0, list2_count=0, f11=0} (own bytes, own walk).
RESULT_LEVEL = B (PARTIAL RESOURCE/SCENE CHAIN)
FUNCTION_IDENTITY = reader FUN_0072FA30 CONFIRMED; lookup FUN_0072F580
  CONFIRMED; getter FUN_007CE1E0 ([ECX+0x08]) CONFIRMED-as-instruction (A-read
  provenance = ECX is the lookup result); FUN_007B67E0 = NiObjectNET::SetName
  counterpart STRONGLY_SUPPORTED; FUN_007B6000 = NiNode ctor counterpart
  STRONGLY_SUPPORTED; 0x007B5390 GetObjectByName-like (historical B, re-pinned);
  FUN_00779D60/E20 family = Ark LOD/attachment state machine (NOT AttachChild).
OBSERVED_OPERATION = physical record -> parse -> registry (RB-tree, key id2)
  -> keyed lookup -> A-read -> model request pair {0x66=MODEL, A} -> scheduler
  queue; placement records are built at runtime from message/attribute/
  hardcoded drivers with position/rotation setters into record fields
  (+0x08/+0x14/+0x20/+0x24) and by-name registration.
FINAL_SEMANTIC_ROLE (bounded) = templates.vfs is the static template registry
  {id2 -> A (model nif id), B (collision bvi id), C, D_f32, name-list1, u32-list2};
  within the censused machinery it is consumed as a DEFINITION source; its
  records were NOT shown to carry world-instance identity or instance
  transforms.
MODEL_RESOURCE_EDGE = CONFIRMED for record 4508: A=296445 -> "296445.nif" in
  the Models.bnt index (anchor @395,268,773 re-pinned; full join 3,618/3,618
  inherited from JOIN R1 as bounded reuse). Runtime physical open of the .nif
  remains STRONGLY_SUPPORTED (provider bodies not decoded this run).
INSTANCE_IDENTITY = model-side named instance = NiControllerSequence
  "<A>__<name>" (0x110 B; identity CORRECTED this run — R-1); world-instance
  identity from a physical record NOT ESTABLISHED (CONTROL-2 FAIL -> UNKNOWN).
TRANSFORM_EDGE = placement-record setters CONFIRMED as runtime transport
  (record is not a NiAVObject: +0x08/+0x14 vs m_kLocal@+0x38/m_kWorld@+0x6C);
  template payload list2 (3 x vec3) -> runtime slot-position lerp CONFIRMED as
  payload-derived transform data (slot object class UNKNOWN); physical-record
  -> world-instance transform NOT ESTABLISHED.
SCENE_GRAPH_EDGE = scene root NiNode ctor + SetName("NetImmerseScene::Root")
  CONFIRMED; model -> world-scene insertion NOT traced past the LOD/attach
  state machine (E7 negative).
PERSISTENT_PLACEMENT_EDGE = NOT ESTABLISHED (construction drivers are
  message-dispatched (types 0xA2..0xC7), attribute-sourced (class-20006
  property tag 6), or hardcoded (PUSH 0x3ED3 etc.) — none reads templates.vfs;
  the only file reader is the registry loader, census 1 caller).
MODEL_ID_RECOVERED = YES — A=296445 ("296445.nif") for record 4508; (and
  A=551661 "551661.nif" @395,323,507 for the cross-record id2=11963).
PLACEMENT_XYZ_RECOVERED = NO — no placement XYZ recovered for any world
  instance from a physical record; record 4508's list2 is empty; the only
  payload-derived vec3 feeds a slot-position computation of unknown class.
CONTROLS_EXECUTED = CONTROL-1 false-candidate (PASS), CONTROL-2
  template-vs-instance (FAIL for the world-instance claim -> UNKNOWN, kept
  honest), CONTROL-3 oracle-transfer negative matcher (PASS), CONTROL-4
  listing-vs-raw byte cross-check (PASS, 962/962 + 113/113), CONTROL-5
  payload/record identity (PASS).
CONTROLS_NOT_ESTABLISHED = slot-object class semantics (FUN_00848EA0 slots);
  no runtime controls (STATIC_ONLY).
INDEPENDENT_CROSSCHECKS = own census caller enumerations (45 target
  enumerations with denominators = 19+10+4+8+4) vs the decompile chains; C1 file walk (own
  container decoder) vs the binary-side parse order; historical anchor
  re-pins (3/3 consistent + 1 partial with disclosed discrepancy).
WHY_NON_CIRCULAR = the A value (296445) is measured from the physical
  templates.vfs file (C1), not from the binary; the parse-order claim is
  byte-pinned in the binary and independently confirmed by the file-side
  structure (payload 28 B = 5 u32 fields + 2 u16 zero counts + f11 = 0 — the
  walk reproduces the record exactly); the Ghidra line and the raw-byte line
  are separate implementations, and the raw-byte line's targets (113/113) and
  bytes (962/962) were recomputed without Ghidra.
INTERNAL_QC_VERDICT = PENDING (fresh-context QC is a separate later phase per
  the dispatch boundary; this executor's own SELF_CHECK is below)
OPEN_P0_P1_P2_P3 = P0: none blocking the science close. P1: (a) the
  NiControllerSequence identity correction R-1 should be propagated as a
  precision note to any future consumer of the "named instance" phrase;
  (b) the E12d probe-window discrepancy (rep movsd) is adjudication-optional
  low priority. P2: the id2-domain candidate channel (X1/X2) remains
  CANDIDATE/UNVERIFIED; a dedicated consumer-decode run is the next
  discriminator. P3: cosmetic QC-R4 per_artifact.failed intentionally untouched.
RETRACTIONS = R-1 (this run's own early "named model instance" wording;
  corrected to NiControllerSequence before finalization).
SUPERSESSIONS = S-1..S-4 (re-pins and reproductions; no historical claim
  retracted; see 02_ANALYSIS/RETRACTIONS_SUPERSESSIONS.md).
BLAST RADIUS = none material against historical claims; R-1 adds precision
  only (no published historical claim asserted the class identity).
PACKAGE_PATH = docs/audits/PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z/
ARTIFACT_INDEX_PATH = docs/audits/PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z/06_REPORT/artifact_index.csv
DRAFT_FINAL_REPORT_PATH = docs/audits/PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z/06_REPORT/DRAFT_FINAL_REPORT.md
MANIFEST_SHA256 / MANIFEST_ROWS / PHYSICAL_FILE_COUNT = TO BE REGENERATED in
  the publication phase (this executor ships artifact_index.csv covering its
  own files; the final manifest is regenerated LAST by the publishing worker).
CHANGED_PATH_CENSUS / COMMIT_SHA / LIVE_REMOTE_HEAD / PUSH_VERIFIED = N/A in
  this task (NO commit/push/stage by executor; publication is a later phase).
PUBLICATION_STATUS = NOT_STARTED_BY_THIS_TASK (by design)
PUBLICATION_BLOCKER = NONE (science close reached; package complete for QC)
```

## What was CONFIRMED / STRONGLY_SUPPORTED / REJECTED / UNKNOWN

- CONFIRMED: the full left-hand chain for record 4508 — physical record bytes
  -> reader/parse (field order f0,f2,f1,f3,f4 = id2,A,B,C,D_f32; lists;
  f11) -> RB-tree registry (key id2@node+0x10, value@node+0x14) -> keyed
  lookup -> A-read ([template+0x08] with pinned ECX provenance) -> request
  pair {0x66=MODEL, A=296445} -> queue+scheduler entry; the data join
  A=296445 -> "296445.nif" (anchor re-pinned; full join inherited);
  placement-record field offsets re-pinned at instruction level; scene root
  naming; the historical anchors (20002 rec0; 296445.nif offset; slot 17
  = 0x007B5390); template payload list2 -> slot-position lerp.
- STRONGLY_SUPPORTED: model instance path structure (with the corrected
  NiControllerSequence identity); FUN_007B67E0 = SetName counterpart;
  FUN_007B6000 = NiNode ctor counterpart; slot 27 UpdateWorldData-shaped.
- REJECTED (as worded): "the pending-attach thunks are Gamebryo AttachChild"
  (they are an Ark LOD/attachment state machine — CONTROL-3).
- UNRESOLVED / UNKNOWN (the honest core of the Level-B outcome): the
  physical-record -> WORLD-INSTANCE identity edge. Within the censused
  construction machinery the placement drivers' inputs (id2, position,
  rotation) come from the message channel, runtime attributes, or hardcoded
  immediates — templates.vfs is consumed as a DEFINITION registry only, and
  no censused driver reads it for instance data. Placement XYZ from a
  physical record: not recovered.

## The missing edge and the next discriminating experiment (proposal only —
DESIGNED_NOT_EXECUTED, not run)

The missing edge is: (message/attribute/hardcoded id2) + (runtime transform)
  -> WORLD INSTANCE whose provenance is a file record. The single most
  discriminating next static experiment: decode the scheduler callback
  FUN_008BD720 (pinned this run as the {0x66,A} request's callback) and the
  type-0x66 provider chain down to the NIF load, then determine whether any
  placement-construction driver feeds its placement record's identity/
  transform into a NiAVObject under "NetImmerseScene::Root" (which would close
  record->registry->model->scene for definition-data, while the
  instance-data edge remains wherever the transform is born — message vs
  file). Complementary: decode the class-20006 property-tag-6 writers (who
  sets the id2 property that FUN_00848EA0 consumes) — if that property is
  ever fed from a VFS record, FAMILY-P/T merge into a real
  physical-record->placement channel.

## Governance block (unchanged, per contract §10)

```text
PE_MASTER_STATUS = PROVISIONAL_UNTIL_QUALIFIED
Q1_STATUS = UNCHANGED
GATE_B_CANONICAL_AUTHORITY = BLOCKED
GATE_C_R3_HISTORICAL_STATUS = MILESTONE_POST_AUDIT_PASS_FOR_AUDITED_SHA
GATE_C_HISTORICAL_AUDITED_SHA = 666a822e1109b3aa68be96fece932def3236424b
M1_CLOSED = NO
M2_M3_AUTHORIZED = NO
CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO
NEXT_ACTION = (this task) return to PE-MASTER with this package; then fresh QC
  and the publication phase per the dispatch boundary.
```

## SELF_CHECK (executor's own — NOT independent PE-MASTER audit)

- [x] Full raw census where claimed: 5,438/5,438 registry records walked to
      exact EOF with own decoder; 1,366/1,366 parameter records; 962/962
      byte cross-check; 113/113 target recomputation; all census denominators
      recorded per target.
- [x] All gates honestly evaluated; no UNVERIFIED promoted; CONTROL-2
      explicitly FAILED (kept UNKNOWN) rather than passed.
- [x] Meaningful negative controls: CONTROL-1 (displacement false positives
      demonstrated with the 817-site getter and the node-left-pointer case),
      CONTROL-3 (oracle negative matcher).
- [x] Correct source/generator hashes: every newly opened source hashed
      (PREFLIGHT.md); EXE identity asserted before every byte instrument.
- [x] No default-success fallback: the c10 v1 transcription artifact was
      caught by the automated cross-check (CONTROL-4) and fixed by
      automation, not by assertion.
- [x] Limits respected: 88/120 functions, 3/3 records, 3/3 oracle mechanisms,
      1 deep-trace family, budget not expanded after results.
- [x] No original file modified; no payload committed into the repo (only
      derived evidence, scripts, hashes, small decoded structures); Ghidra
      work on a run-local project copy outside the repo.
- [x] Foreign untracked groups untouched; no git staging; AUDIT_ENTRYPOINT.md
      NOT modified (publication phase owns the entrypoint row).
- [x] One in-run retraction (R-1) disclosed with blast radius; no historical
      claim retracted.
```
