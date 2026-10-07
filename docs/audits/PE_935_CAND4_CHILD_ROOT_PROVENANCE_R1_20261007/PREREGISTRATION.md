# PREREGISTRATION — PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007

Written BEFORE detailed work (contract §3). This file preregisters the budgets,
the strategy, the adaptive decision rule, the pre-commitments and the honest
negative outcomes of this run. Nothing below may be changed after detailed work
starts; budget consumption is tracked in EDGE_ACCOUNTING_LEDGER.csv (edges),
FIELD_PRODUCER_LEDGER.csv (writers) and the analysis records of 01_RAW/.

## 0. Entry state and supersession compliance (carried, not re-derived)

Entry state (contract §2, from the audited BASE evidence packages):
SCIENCE_OUTCOME = PARENT_FOUND_CHILD_UNRESOLVED ·
PARENT_SCOPE = EXAMINED_ACLD_PLUS_18_SF_INSTANCE ·
EXACT_PARENT = CONFIRMED_EXACT_SCENEFEEDER_PLUS_30 ·
JOIN_OPERATION = STRONGLY_SUPPORTED ·
CHILD_MODEL_PROVENANCE = UNRESOLVED ·
CHILD_VISUAL_ROLE = UNRESOLVED ·
INSTANCE_MODEL_NODE_JOIN = NOT_ESTABLISHED ·
REAL_SCIENCE_AUTO_QUALIFICATION = DISABLED ·
QC_POSITIVE_CHAIN_QUALIFICATION = NOT_ESTABLISHED_AS_GENERAL_AUTHORITY.

J1–J3 supersessions honored (ACTIVE statuses of the corrected lineage): the
historical qualification gate is not used as a positive qualifier anywhere in
this run; the historical source-run edge ledger convention (MINIMUM_ANALYZED_
EDGE_COUNT = 22 distinct pairs for THAT historical run, ACTUAL not reported) is
NOT changed by this run — this run's own edge accounting starts fresh under the
§3 unit definition and is recorded in EDGE_ACCOUNTING_LEDGER.csv; the
SAME_INSTANCE_TRANSFORM_RELATION of the historical run remains
NOT_QUALIFIED_BY_ORIGINAL_SCOPE and no transform semantics are analyzed here.
Load-bearing prior edges are re-pinned only within their already-recorded
interpretation scope (prior file/record cited per row; free re-pin = no new
semantics) — see EDGE_ACCOUNTING_LEDGER.csv rows marked REPIN_PRIOR_SCOPE.

## 1. The one question (contract §2)

Co zwraca FUN_006C66D0 na istniejącej ścieżce CAND-4, skąd pochodzi ten
pointer i czy reprezentuje główny wizualny model/resource tej ścieżki?

Examined path (the ONLY path of this run; byte-proven by the prior run and
re-pinned within its recorded scope at preflight):
FUN_006A3930 (ArkClientLocalDynamic ctor): new(0x130) @0x006A3A48/0x006A3A4D
-> FUN_006C0D50 (ArkModelManagerMain ctor) @0x006A3A77 -> FUN_006C8B20
@0x006A3A8D -> FUN_006C8BB0 @0x006A3A94 -> FUN_0050A310(SF, manager) @0x006A3A9D
-> [SF+0x20]=manager @0x0050A3AC -> child=FUN_006C66D0(manager) @0x0050A3AF
-> return EAX -> EDI @0x0050A3B7 -> push EDI @0x0050A3F6 -> NiNode vtable slot
41 CALL @0x0050A3F7 (receiver = [SF+0x30] of the examined ACLD-path SF instance;
JOIN_OPERATION = STRONGLY_SUPPORTED — the ceiling of this run, not to be raised).

## 2. Hard budgets (contract §3 — preregistered BEFORE detailed work)

MAX_NEW_FUNCTION_BODIES_OPENED = 6
MAX_NEW_INTERPROCEDURAL_EDGES_SEMANTICALLY_ANALYZED = 8
MAX_NEW_MANAGER_FIELD_WRITERS_TRACED = 6
MAX_NEW_WRAPPER_HOPS = 3
MAX_NEW_CHILD_PROVENANCE_CANDIDATES = 3

These limits cover the WHOLE run including producer search, falsifiers,
preservation checking and internal QC. Rules honored exactly:
- Edge unit = a unique semantically analyzed CALLSITE (caller_start_VA,
  callsite_VA) — NOT a (caller,callee) pair. Two callsites of the same pair
  count SEPARATELY. Re-checking the same site costs nothing (re-pin of the
  already-recorded interpretation: prior file/record cited + no new
  semantics). Different established targets of one site = separate variants
  under the same unit. Unresolved/indirect targets do NOT waive the budget.
- A NEW interpretation (receiver / callee identity / argument-result flow /
  path role / semantic role) of a callsite requires an IMMEDIATE
  EDGE_ACCOUNTING_LEDGER.csv row, even if the callee body is not opened.
  Raw un-interpreted decode (target arithmetic only) is recorded separately
  (01_RAW records + ledger RAW_VISIBLE_ONLY rows with explicit
  NOT_COUNTED_REASON) — analysis is never hidden behind a RAW_VISIBLE label
  (lesson J2: list length ≠ performed census).
- Partial body opening / probing of a new function consumes the function
  budget.
- MAX_NEW_WRAPPER_HOPS covers all new typed lineage hops (clone, containment,
  selected subtree, target). Simple SAME_OBJECT load/store/register moves are
  NOT hops, but a new interpretation of their callsites still costs edge
  budget.
- STOP BEFORE exceeding any limit => the affected component gets its honest
  bounded status (BOUND_REACHED) and the run continues with the remaining
  components; zero after-the-fact exceptions; zero retroactive authorization.
- The historical convention of the previous correction run (the SOURCE run's
  minimum-22 census) is NOT changed by this run; this ledger is a fresh
  census under the §3 callsite unit for THIS run's new analysis only.

## 3. Adaptive body-opening plan (priority order; within MAX 6)

1. NEW BODY #1 (mandatory): FUN_006C66D0 — the getter. Complete bounded body
   decode: raw bytes, instructions, entry/extent with provenance of the
   extent claim (terminal RET + padding alignment; CC/RET heuristic alone is
   NOT proof of extent — the extent record must show the bounding bytes), all
   branches, NULL conditions, field reads, return convention. Deliverables:
   GETTER_OPERATION (enum §4) + ARKMODELMANAGER_CHILD_FIELD_OFFSET (measured
   offset | NOT_APPLICABLE | UNRESOLVED).
2. Producer search (bodies #2..#4 as needed): IF the result comes from a
   manager field or bounded producer, trace ONLY the writers/producers of that
   field/result, restricted to the manager-receiver calls executed on the
   examined path variant between the allocation (0x006A3A4D) and the getter
   call (0x0050A3AF): FUN_006C0D50 (ctor — first candidate; field
   initialization), FUN_006C8B20 @0x006A3A8D (candidate 2), FUN_006C8BB0
   @0x006A3A94 (candidate 3), plus any writer of the same field found inside
   an ALREADY-opened body. NO global census of the manager's methods/callers
   (contract §4: coverage = the achieved producers in the declared scope +
   EXPLICIT coverage gaps). Every reached writer, branch, NULL/reset and
   alternative producer is recorded in FIELD_PRODUCER_LEDGER.csv; no
   convenient subset. If several producers stay unresolved, the field is NOT
   promoted to CONFIRMED_MODEL_DERIVED.
3. Preservation check (§7; remaining bodies, in call order):
   FUN_006C0F90 @0x0050A3B9, FUN_006C10B0 @0x0050A3CF, FUN_0050A1E0
   @0x0050A3D8, FUN_005246E0 @0x0050A3E4 — the four intervening calls between
   mov edi,eax @0x0050A3B7 and push edi @0x0050A3F6. Opening a body = one unit;
   the goal is to physically show EDI is not clobbered (ABI is support, not
   proof). Bodies NOT opened due to budget => CHILD_TO_JOIN_IDENTITY is set to
   STRONGLY_SUPPORTED at most (per §7 fallback), with the unopened callees
   listed in NOT_CHECKED.
DECISION RULE (preregistered): the §4 provenance question has priority over
raising §7 to CONFIRMED (the question of THIS run is where the pointer comes
from; §7 has an explicit honest fallback). If bodies #2..#4 turn out
unnecessary (e.g., the getter result does not come from a manager field), the
freed budget goes to §7 preservation bodies, in call order, up to MAX 6 total.

## 4. Planned edge accounting (callsite-unit census for THIS run)

New-edge candidates (semantically analyzed callsites expected under the plan
above; each gets a ledger row the moment its interpretation is new):
- FUN_0050A310 @0x0050A3AF -> FUN_006C66D0 (the child getter; the prior run
  recorded receiver/identity/flow at summary level; THIS run adds the decoded
  callee semantics => new result semantics; counted as a NEW analyzed
  callsite).
- FUN_006A3930 @0x006A3A77 -> FUN_006C0D50, @0x006A3A8D -> FUN_006C8B20,
  @0x006A3A94 -> FUN_006C8BB0 (historically label-level re-pins; THIS run
  gives them semantic roles via the decoded callee bodies => NEW).
- Callsites INSIDE each newly opened body whose interpretation is new (each
  analyzed callsite counted individually; raw-only targets recorded
  RAW_VISIBLE_ONLY with NOT_COUNTED_REASON and NOT analyzed).
- §7 preservation bodies' internal callsites, same rule.
If the 8-edge limit is hit, remaining callsites are recorded RAW_VISIBLE_ONLY
with explicit NOT_COUNTED_REASON and the affected component gets its bounded
status. NOT counted (re-pins of already-recorded interpretations; zero new
semantics; prior file/record cited per row): the 0x0050A3E9..0x0050A3F7 join
window pins (receiver/vtable-slot-41/target — recorded by the source run, QC
S4/S8), the [SF+0x20] store @0x0050A3AC, the three FUN_006C66D0 callsite
targets' rel32 arithmetic (recorded by the source run at raw level), the
manager-allocation chain pins (X06/X07/X08/X31 family of the correction
census).

## 5. Typed pointer lineage (contract §5)

Every hop recorded in POINTER_LINEAGE.csv with SOURCE_OBJECT / DESTINATION_
OBJECT / POINTER_EXPRESSION / RELATION_TYPE (SAME_OBJECT | CLONE_OF |
WRAPPER_CONTAINS | DESCENDANT_OF | CONTROLLER_TARGET | UNRESOLVED) /
OPERATION / PATH_CONDITION / EVIDENCE / STATUS. clone != identity: for
CLONE_OF the operation's concrete input and output and their further flow are
shown; for WRAPPER_CONTAINS the actual containment relation is shown; named
lookup may return receiver / descendant / NULL. MODEL_ROOT_RELATION enum per
contract §5 — descriptive hypotheses until physically grounded. Same-object
moves are not hops; new interpretations of their callsites cost edge budget.

## 6. Separate visual-role proof (contract §6)

CHILD_RESOURCE_PROVENANCE / RTTI / attachment are NOT by themselves a visual
role. Required for CONFIRMED_MAIN_VISUAL_ROOT|WRAPPER: (a) resource-derived
contained model (for wrapper), (b) typed containment/lineage, (c) the exact
wrapper used as the child, (d) a positive PCG proof linking the concrete
result to the choice/installation/storage/consumer of the principal visual
representation of the object on the examined variant. Absence of VFX/
collision/helper findings is NOT the positive proof; achieved fallback/error/
placeholder branches are checked; loading success is not assumed from a
request name. If no proof => CHILD_VISUAL_ROLE = UNRESOLVED. NiControllerSequence
and sequence-control helpers are not automatically scene children; controller
targets need their own proof.

## 7. Getter result -> exact child argument (contract §7)

Re-pin chain: FUN_006C66D0 return EAX -> EDI @0x0050A3B7 -> push EDI
@0x0050A3F6 -> CALL @0x0050A3F7 (slot 41). EVERY intervening call and branch
accounted: call FUN_006C0F90 @0x0050A3B9 (+ test al,al branch -> [SF+0x2C]
bit1 write), call FUN_006C10B0 @0x0050A3CF, call FUN_0050A1E0 @0x0050A3D8
(EDI pushed as argument @0x0050A3D7), call FUN_005246E0 @0x0050A3E4. Generic
ABI is support, not proof; physical behavior of the value or an equivalent
bounded fact required for CONFIRMED. If the budget does not allow all four
intervening bodies: CHILD_TO_JOIN_IDENTITY = STRONGLY_SUPPORTED | UNRESOLVED.
Identity must remain exact: no substitution of a resource pointer, sibling or
wrapper whose relation to the actual result is not proven. Parent/slot-41
re-pins stay within the already-persisted scope; JOIN_OPERATION =
STRONGLY_SUPPORTED remains the ceiling (FUN_007BF470 and any separate
parent/join proof are NOT opened).

## 8. Status algebra (contract §8 — literal)

CHILD_EVIDENCE_COMPLETE = (CHILD_RESOURCE_PROVENANCE == CONFIRMED_MODEL_DERIVED)
  AND (CHILD_VISUAL_ROLE in {CONFIRMED_MAIN_VISUAL_ROOT,
  CONFIRMED_MAIN_VISUAL_WRAPPER}) AND (CHILD_TO_JOIN_IDENTITY == CONFIRMED)
  AND (EXACT_PARENT == CONFIRMED_EXACT_SCENEFEEDER_PLUS_30).
IF CHILD_EVIDENCE_COMPLETE AND JOIN_OPERATION == STRONGLY_SUPPORTED:
  CAND4_CHILD_ROOT_CLOSURE = STRONGLY_SUPPORTED_STATIC_CONDITIONAL.
ELSE: CAND4_CHILD_ROOT_CLOSURE = NOT_ESTABLISHED_WITHIN_BOUND.
Components may be CONFIRMED_STATIC_CONDITIONAL after manual adjudication of
physical evidence; the chain never advances past its weakest required edge;
UNKNOWN != REJECTED != PASS; no automatic science qualification
(REAL_SCIENCE_AUTO_QUALIFICATION stays DISABLED; no tool of this run issues
SCIENCE_PASS).

## 9. Four controls (contract §9) — same-checker clean PASS -> mutated FAIL

1. CTRL_1 animation false positive: the existing pinned NiControllerSequence
   (the prior CH3 canon object — the named 0x110 object of the instance
   creator chain) does NOT qualify as main visual through model-adjacency
   alone on the same visual-role checker.
2. CTRL_2 wrapper relation break: a synthetic fixture breaks the specific
   containment/pointer relation; the relation's positive predicate must not
   survive (same checker, same range, correct cause).
3. CTRL_3 wrong manager field: substituting the field/accessor so that correct
   bytes of a DIFFERENT manager field feed the provenance predicate must FAIL
   that predicate (correct bytes of a foreign field do not qualify as
   provenance of THIS getter).
4. CTRL_4 child identity break: breaking the return->final-child relation in
   a fixture must not leave CHILD_TO_JOIN_IDENTITY = CONFIRMED (same
   preservation/identity checker).
No new real EXE fields/objects are searched for the controls; synthetic
fixtures are marked SYNTHETIC_MACHINERY_TEST_ONLY; a real input rejected ONLY
by disabled policy is recorded POLICY_ONLY (no detection claim); a synthetic
PASS is not PCG science. CTRL notes are not proof of validator completeness.

## 10. Oracles (contract §10) — helpers only

Available: the pinned local Gb12 sources (NiNode.cpp / NiAVObject.cpp —
identities re-measured, INPUT_IDENTITIES.md §5). NOT available on local disk:
the OpenMW commit 0c6a724… sources and the GB2.6 mirror 329cd25… sources —
NOT_USED (file identity unmeasurable). Oracle usage recorded as
ORACLE -> HYPOTHESIS -> PCG BYTE/DATAFLOW PROOF; an oracle supports
MECHANISM_ANALOGY only, never PCG_CONFIRMED; era/build mismatch explicit
(Gb12 != PCG 9.3.5); no blind offset transfer.

## 11. Prohibitions and honest negative pre-commitments (contract §11)

NOT examined: historical XYZ, static-building channel, paging/batching,
network origin, CMO<->ACLD identity, new transform semantics,
ExtraData/readback/FUN_007B68B0, global Ni/model atlas, runtime/client, new
VFS/BNT/NIF payload opening, FUN_007BF470 / any separate parent-join proof.
Pre-committed honest outcomes (recorded precisely + STOP, no continuation for
a positive):
- BOUND_REACHED if a concrete next body/edge/writer/hop would exceed a limit.
- RESOURCE_NEARBY_IDENTITY_UNPROVEN / UNRESOLVED for provenance when
  producers stay unresolved or only nearby model-ID/name/geometry/string/
  request evidence exists.
- CHILD_VISUAL_ROLE = UNRESOLVED when no positive visual-role proof is
  achieved (VFX/helper/NULL/non-scene results are recorded as measured, not
  as evidence of visuality).
- CHILD_TO_JOIN_IDENTITY = STRONGLY_SUPPORTED or UNRESOLVED when preservation
  bodies stay unopened within budget.
- A bounded negative does not prove any other static/paged/network channel.
Maximum positive conclusion (§11 ceiling): on the examined, conditional ACLD
path, component proofs of model/root provenance, role and the pointer fed to
the existing STRONGLY_SUPPORTED join operation — NOT historical world-instance
identity, building data, CMO path, universal mechanism or runtime observation.
