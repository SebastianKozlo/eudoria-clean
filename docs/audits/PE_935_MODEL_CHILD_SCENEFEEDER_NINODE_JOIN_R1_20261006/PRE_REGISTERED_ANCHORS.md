# PRE_REGISTERED_ANCHORS — PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006

Written BEFORE detailed decoding (contract §3). Every anchor below states its
exact source (prior pin path + status) and the strategy chosen to reach the
join question. Budgets are declared here and tracked in FUNCTION_BUDGET.csv /
EDGE_LEDGER.csv. New semantics of a previously known function counts toward the
budget; re-reads of declared prior pins in their recorded scope do not.

## The one question (contract §0)

Czy na jednej zbadanej ścieżce PCG 9.3.5 wynik o fizycznie ustanowionym
pochodzeniu model/resource zostaje związany jako visual child z dokładnie tym
samym NiNode pointerem, który pochodzi z badanego SceneFeeder+0x30?

Four separate proofs required (contract §4):
A CHILD_PROVENANCE — child value/result from a physically established
  model/resource operation, identity preserved through wrapper/clone;
B EXACT_PARENT — the same examined SF instance, exact access SF+0x30, value
  preserved to the parent argument of the join operation;
C JOIN_OPERATION — on the SAME call/store, parent = B's value and child = A's
  value, with the conditional semantics of the actual parent-child operation;
D VISUAL_ROLE — physical proof of visual/model-derived role of the child.

## Hard budgets (no after-the-fact exceptions)

MAX_NEW_DETAILED_FUNCTIONS = 8
MAX_NEW_INTERPROCEDURAL_EDGES = 6
MAX_JOIN_CANDIDATES_DETAILED = 4
MAX_WRAPPER_LEVELS = 2
ORACLE_MECHANISMS_MAX = 1

## PARENT SIDE — declared prior pins to re-pin from EXE (re-read scope only)

- PA1 — SF ctor FUN_00509330: allocation 0x118 -> CALL FUN_007B6000
  @0x005093B8 -> result stored to [SF+0x30] @0x005093C3 (bytes 89 45 30) ->
  refcount++ [node+4]. The stored object = NiNode (vtable 0x00A8CCF4 stored by
  FUN_007B6000 @0x007B6041; MSVC RTTI .?AVNiNode@@). Source:
  PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006/FINAL_REPORT.md §4 +
  PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914/06_REPORT/REPORT.md C4/C5/C6.
  Status to carry: CONFIRMED (link type identified; SF30_LINK_TYPE_IDENTIFIED).
- PA2 — the same ctor's ExtraData chain: new(0x14) @0x00509485..0x0050948B ->
  FUN_0064B1E0 (SceneFeederObjectExtraData ctor; vtable 0x00A83274; key at
  [obj+0x10]) -> registration @0x00509494..0x005094A2: receiver = [SF+0x30],
  args = literal "ArkSceneFeeder" (0x00A7D444) + ExtraData -> CALL FUN_007B6A80
  (AddExtraData-like front-end, STRONGLY_SUPPORTED; further callee
  0x007B68B0 = final storage, DEFERRED_LEAD). Sources:
  PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006/FINAL_REPORT.md §4/§5 +
  pinned NIRTTI research §4 + pinned ENGINE_COMPARISON research §3.
  Status to carry: CONFIRMED (call chain), STRONGLY_SUPPORTED (helper role),
  STORAGE NOT_CHECKED (deferred lead — see §DEFERRED below).
- PA3 — SF vtable slot 3 FUN_0050A050 (GetPosition(out, name)): [SF+0x30] read
  @0x0050A05B (8B 4E 30) -> NiNode virtual dispatch vtable+0x44 @0x0050A064
  (slot 17 = 0x007B5390, GetObjectByName-like, STRONGLY_SUPPORTED status B);
  result+0x90 (world translate) -> FUN_00437F70 -> FUN_0082B5A0 -> caller's out.
  Sources: PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914 REPORT §3 (slot map),
  PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 C7 (positive control bytes),
  PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914 (slot-17 identity),
  PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915 (downstream semantics).
  Status to carry: CONFIRMED (bytes/ABI), slot-17 identity STRONGLY_SUPPORTED.
- PA4 — CMO ctor FUN_00528E50: [CMO+0x74] key read -> callsite 0x00528FD9 ->
  FUN_005247C0 (SF factory wrapper, RET 8) -> FUN_00509330 (SF ctor, RET 0xC) ->
  result stored to [CMO+0xC0] @0x00528FEA; later SF re-received as
  [esi+0xC0] @0x0052901A -> CALL FUN_005094C0 @0x00529020 (SetPosition-like
  SF method: triple -> SF+0x34/0x38/0x3C, flag SF+0x28=1). Sources:
  PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006/FINAL_REPORT.md §3/§4 +
  PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 C9.
  Status to carry: CONFIRMED (receiver-proven ctor branch).
  NOTE: the CMO ctor is a KNOWN function; any NEW body analysis beyond the
  recorded pin scope (e.g. the un-decoded continuation after 0x00529020) is
  NEW detailed semantics and will be charged to the budget if performed.

## CHILD SIDE — declared prior pins to re-pin from EXE (re-read scope only)

- CH1 — the {0x66=MODEL, A} request pair emission in FUN_006C3F50 (emitter):
  CALL FUN_0043A550 @0x006C3F5B (registry lazy-init) -> MOV ECX,EAX @0x006C3F60
  -> CALL FUN_0072F580 @0x006C3F62 (lookup) -> MOV EDI,EAX @0x006C3F67 ->
  MOV EBX,0x66 @0x006C3F69 -> MOV ECX,EDI @0x006C3F6E -> CALL FUN_007CE1E0
  @0x006C3F74 (getter A = [template+0x08]) -> MOV [ECX],EBX @0x006C3F8D ->
  MOV [ECX+4],EAX @0x006C3F8F -> FUN_006C3640(queue, ..., callback
  FUN_008BD720, A) scheduler entry. Physical source: templates.vfs record
  id2=4508 (file_offset 96,496; payload A=296445 @96,516, bytes fd 85 04 00).
  Source: PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z
  02_ANALYSIS/TRACE_EDGE_BLOCKS.md E1/E2/E3 (byte-verified there 962/962).
  Status to carry: CONFIRMED (request pair + scheduler entry; data join
  A<->296445.nif CONFIRMED at data level; provider completion NOT closed).
- CH2 — FUN_008BD720 = the request's scheduler callback VA (PIN only — pinned,
  never decoded). Source: TRACE_EDGE_BLOCKS E3. Status: PIN_RECORDED,
  UNDECODED. Its body decode = NEW detailed function #1 (charged).
- CH3 — instance creator FUN_006CB6F0 chain (structure CONFIRMED at byte
  level in the bridge run; identity of the named 0x110 object = NiControllerSequence
  per the R2 adjudication): cache lookup FUN_00971780 -> miss -> pump
  FUN_006C9700 @0x006CB7CF -> operator new(0xC) -> FUN_006FA8B0 ctor (vft
  0x00A864B8, refcount@+4, item@+8; inherited prior canon) -> FUN_006CB020
  named-instance builder -> FUN_006F33A0 registration; pending-attach processor
  FUN_006CB3C0 (descriptor type@+0x5C, id@+0x64; attach thunks FUN_0077C0B0/
  0xF0/0x120 -> FUN_00779D60/0xE20 family; per the binding anchor constraints:
  0x00779F80 = STRONGLY_SUPPORTED StopMorph; the 0x00779D60/0x00779E20 family
  label "ARK_LOD_STATE_MACHINE" is SUPERSEDED for ranking — stock Gamebryo
  animation sequence control, mechanism STRONGLY_SUPPORTED; FUN_006CB3C0 has NO
  model-attach priority from its label — it returns to the shortlist ONLY on a
  physical pointer/dataflow edge). Sources: TRACE_EDGE_BLOCKS E5/E7 + the
  pinned R2 HANDOFF_NOTES items 1/2/9/10.
  Status to carry: structure CONFIRMED (byte-level, bridge run); visual-child
  relation of ANY of these = NOT_ESTABLISHED.

## JOIN SEARCH STRATEGY (the examined paths, in priority order)

Strategy summary: start from the resource island's own open edge (the
{0x66,A} completion, CH2) because it is the only physically established
model/resource operation whose RESULT can be given provenance within this
budget; decode the callback and follow the completion dataflow until either
(a) a result object with physically established model provenance exists
(A-candidate), and (b) a parent-argument candidate appears; then test the
parent argument against EXACT_PARENT (B) by tracing its provenance back to
the SAME SF instance's +0x30 access. The SF-side consumers (PA3/PA4) bound
the parent side: no other SF+0x30 reader exists in the SF's own vtable/canon,
so the parent argument must originate outside the SF class — i.e. the join,
if any, is expected to be found where a model-completion consumer receives
or fetches the SF's NiNode.

Declared detailed-analysis targets (budget-charged; STOP before exceeding):

1. NEW function #1 — FUN_008BD720 (scheduler callback body, full decode).
   Purpose: what the {0x66,A} completion does; whether it produces a result
   object (the A-candidate) and hands it anywhere.
2. NEW edges from #1 follow the completion (each callee decode = NEW function
   + NEW edge; STOP at budget).
3. Census (byte-scan only, not detailed): direct E8 callers of FUN_006CB6F0
   and of FUN_005247C0/FUN_00509330 to check for SF/CMO-family provenance
   among model-result consumers. Any caller whose body needs reading to
   establish provenance = NEW detailed function (charged).
4. Join candidates examined (max 4): each candidate = one join site
   (call/store) where parent-argument and child-argument identities are
   tested. All examined candidates — including rejected ones — go to
   CANDIDATE_LEDGER.csv.
5. ORACLE (max 1 mechanism): NiNode::AttachChild / NiAVObject::AttachParent
   fingerprint from the pinned Gb12 source (NiNode.cpp / NiAVObject.cpp),
   identities re-measured at use and compared to the earlier research. Used
   ONLY to (a) predict the fingerprint of the PCG child-array insertion
   operation (children array +0xCC / count +0xD4, per slot-17 canon) and
   (b) verify an identified PCG candidate by independent byte proof, and
   (c) classify any attach-like operation found on the examined path. No
   ABI/offset/semantic transfer; no SDK build; no source copying.

## DEFERRED_LEAD dependency statement (contract §3)

FUN_007B68B0 (final ExtraData storage) and the ExtraData readback are
DEFERRED_LEAD — NOT a target of this run. Dependency declared in advance:
the ExtraData chain (PA2) is NOT the visual-child join (ExtraData is
metadata; not a model-derived visual child), so this run does NOT need
FUN_007B68B0's body to resolve the join question for the paths declared
above. If during a declared candidate the join resolution turns out to
physically require the ExtraData storage body, that dependency will be
recorded BEFORE its analysis and charged to the same budgets; no separate
storage-hardening analysis is performed.

## Negative-outcome pre-commitments (honesty)

- If the completion chain does not produce an established model-derived
  result within the function/edge budget: outcome = BOUND_REACHED (if a
  concrete next callee exists at the stop point) or
  RELATION_NOT_ESTABLISHED_WITHIN_BOUND / CHILD_FOUND_PARENT_UNRESOLVED /
  PARENT_FOUND_CHILD_UNRESOLVED as applicable.
- If no good model-producer anchor exists at all on the declared paths:
  NO_CANDIDATE_WITHIN_BOUND (a valid outcome; header-only candidate ledger).
- A candidate where the parent argument proves to be a different NiNode =
  WRONG_PARENT; a candidate whose child proves non-model (collision/effect/
  audio/UI/metadata) = NON_MODEL_CHILD; a candidate whose child identity is
  lost through wrapper/clone = WRAPPER_IDENTITY_LOST.
- RUNTIME_JOIN_OBSERVED = NO always. No claim that the original client ever
  executed any examined branch.
