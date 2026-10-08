# PREREGISTRATION — PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008

Written BEFORE any science analysis (contract §4). This file preregisters the
hard budgets, the analysis plan, the adaptive decision rule, the pre-commitments
and the honest negative outcomes of this run. Nothing below may be changed
after detailed work starts. Budget consumption is tracked in the SHARED
ledgers: FUNCTION_BODY_ACCOUNTING.csv (bodies), EDGE_ACCOUNTING_LEDGER.csv
(edges), PLUS4_PROVENANCE.csv (writers; with FUNCTION_BODY_ACCOUNTING for the
body charge of the writer sites), POINTER_LINEAGE.csv (hops). Executor,
controls and QC draw from the COMMON budget; QC repetition of the same unit is
free; NEW units consumed by QC draw from the same budget.

## 1. The one question (contract §1)

Na ścieżkach zgodnych z zapisanym callerem CAND-4: skąd pochodzi wynik R z
FUN_006C9700 i kto nadaje wartość odczytywaną później jako [R+4]?
Two required results: RETURN_VALUE_ORIGIN and PLUS4_WRITER_AND_SOURCE. Exact
type/base of R required if physically establishable in bound. T described only
to the ceiling of encountered evidence; no separate downstream trace of T.

## 2. Hard budgets (preregistered BEFORE analysis; contract §4 — verbatim)

```text
MAX_NEW_FUNCTION_BODIES_OPENED = 6
MAX_NEW_INTERPROCEDURAL_EDGES_ANALYZED = 12
MAX_NEW_PLUS4_WRITERS_TRACED = 4
MAX_NEW_WRAPPER_OR_SUBOBJECT_HOPS = 3
```

Unit definitions and rules honored exactly:

- BODY: FUN_006C9700 is body #1 (mandated). Partial opening counts. Re-opening
  a previously unrecorded range of a known function also costs one body unit.
  Each function-start VA is charged ONCE in the shared run ledger; further
  windows of the same already-charged body are recorded in the ledger WITHOUT
  a second body charge. STOP BEFORE EXCEEDING.
- EDGE: edge unit = a unique semantically analyzed (caller_start_VA,
  callsite_VA). Interpretation of a REJECTED candidate / control / ranking /
  RAW content ALSO counts if it contributes new callsite interpretation.
  Data/RTTI reads WITHOUT callsite interpretation are NOT edges. QC
  repetition of the same unit is free; NEW QC units draw from the common
  budget. Check remaining limit BEFORE each new unit. Analysis is never
  hidden inside a RAW label or an exemption.
- WRITER: writer unit = a unique static assignment site + destination-base
  interpretation; runtime iterations are not counted separately.
- HOP: hop = a NEW interpreted transition between the roles/base pointers on
  the trace (R, T, W and any object they physically transition into); not
  every raw dereference in PE/RTTI. SAME_OBJECT register moves are not hops.
- If a bound is insufficient: report PARTIAL / NOT_ESTABLISHED_WITHIN_BOUND
  with the last proven edge; exceeding = disclosed historical FAIL; no
  retroactive authorization; no science continuation. Do not need to spend
  the whole budget.

## 3. Adaptive analysis plan (priority order; within the budgets)

1. BODY #1 (mandatory): FUN_006C9700 @0x006C9700 — bounded full-body decode
   (raw bytes + capstone 5.0.7 disassembly + own rel32 recomputation; window
   initially 0x400 bytes, extendable within the SAME body charge until the
   extent resolves: terminal RET + padding + aligned next entry, or an
   explicit PARTIAL extent record). Deliverables:
   - (A) every return path to RET: the final EAX source (allocation /
     callee-return / field / getter / adjustment / passthrough / other) with
     path predicates; a constructor present in the body is NOT proof of
     return identity.
   - (B) the base pointer R's construction/vptr/RTTI ties ONLY where dataflow
     exists (vtable store into the returned object; RTTI chain of THAT
     vtable); nearby RTTI or the known W cannot replace that edge.
   - (C) all assignment sites inside the opened bodies whose destination can
     be [R+4] (destination-base interpretation recorded per site); first
     initialization and later overwrite reported separately; NO global writer
     census; no closure in bound = UNKNOWN/PARTIAL.
   - (D) T described only to the ceiling of the encountered evidence.
2. Bodies #2..#6 (adaptive; only load-bearing for R, its construction/return
   identity or the R+4 writer/source — contract §4): in expected priority
   order: (a) the direct callee that produces the returned value on the
   dominant return path (e.g. the cache/lookup/provider call whose return is
   moved into EAX); (b) the direct callee that constructs the object whose
   address becomes R (constructor/init); (c) a +4-writer callee reached with a
   proven receiver identity. DECISION RULE: bodies are opened in the order
   the RETURN_VALUE_ORIGIN question demands; the origin question has priority
   over writer closure; STOP BEFORE EXCEEDING 6.
3. Edges: the semantically analyzed callsites inside the opened bodies that
   contribute to (A)/(B)/(C) — each unique (caller_start_VA, callsite_VA)
   counted once; rejected candidates that contribute new callsite
   interpretation counted honestly; raw-visible-only targets recorded in the
   ledger with explicit NOT_COUNTED_REASON without interpretation.
4. Writers: every reachable assignment to [R+4] (or to a base later proven
   equal/unequal to R — destination-base interpretation stated per site),
   first-init vs overwrite separated. Max 4.
5. Hops: the interpreted transitions on the trace R/T/W (max 3 NEW; the
   prior-canon H-1/H-2 record is prior scope — this run's own hops are its own
   units, cited to prior records where identical physical instructions are
   re-pinned).

## 4. Status discipline (contract §5/§7)

- Every load-bearing claim carries: EXE identity (§3 pin), VA/file-offset
  mapping, raw bytes, instruction, source/destination expression, base
  identity, path condition, extent RESOLVED/PARTIAL/UNRESOLVED, status.
- Every used rel32 recomputed separately (own arithmetic; capstone must
  agree). RTTI shown as the raw vptr/COL/TypeDescriptor/name chain with its
  relation to R/T.
- Origin category (allocation/factory/callee/field/adjusted/passthrough/other)
  does NOT replace the exact source expression + path predicate.
- Static possibility is never named an observed execution; branch-dependent
  alternatives shown within bound with their predicates.
- R+4 and T+4 are DIFFERENT addressing expressions; their bases stay separate
  until an alias is physically proven; proven alias is a legal result, not an
  automatic FAIL. No assumption of R==T / R!=T / R==W / R!=W or their class
  equality/difference.
- The pointer-vs-count conflict is CONDITIONAL (same proven base
  pointer/layout required); an unproven condition = CONDITIONAL_UNRESOLVED.
- T types/roles outside encountered evidence = NOT_ADJUDICATED/UNRESOLVED.
- Transform owner and coordinate frame = NOT_ADJUDICATED_BY_THIS_RUN (prior
  status preserved). No promotion of model root / main visual / world
  instance / channel / XYZ in this run.
- REAL_SCIENCE_AUTO_QUALIFICATION = DISABLED; SCHEMA_CHECK != PIN_CHECK !=
  STRUCTURAL_CHECK != SEMANTIC_ADJUDICATION; class/return/source adjudication
  is done explicitly by the author/QC; hash/pin PASS does not approve
  dataflow or semantic role.

## 5. Checker + controls (contract §6 — preregistered)

- A small checker (03_SCRIPTS/checker_plus4.py) uses the PHYSICAL EXE with its
  OWN PE mapping and recomputation (not the report/CSV/JSON): verifies the
  used byte windows, rel32 arithmetic, the return/load/store anchor pins of
  the analysis, and any RTTI pointer chain used. Mechanical controls: a
  documented clean pass + a DELIBERATE CORRUPTION of the proper load-bearing
  anchor with the SAME production gate detecting the corruption (a
  manifest-only/unrelated-check failure is NOT anchor validation).
- Seven controls CTRL_A..CTRL_G (contract §6, verbatim) — they reject
  unauthorized inferences; they are NOT seven new science questions; they may
  use synthetic data or existing pins; NO body opened solely to find an
  intermediate/wrong-object fixture; logical controls labeled
  SYNTHETIC_LOGICAL_CONTROL — never presented as new physical PCG
  measurements:
  - CTRL_A: intermediate/nearby RTTI without final-return dataflow does not
    qualify R;
  - CTRL_B: mixing R+4/T+4, +4/+8 or unproven bases does not qualify field
    identity; a proven alias is a legal result, not an automatic FAIL;
  - CTRL_C: ctor(W,R) and the W name do not qualify class(R) without a
    separate edge;
  - CTRL_D: count-vs-pointer conflict stays conditional until class/base/
    layout are proven; an unproven condition = CONDITIONAL_UNRESOLVED, not
    proof of no conflict; a prior map is not a new layout measurement;
  - CTRL_E: named strings alone do not qualify GetObjectByName/GetExtraData,
    child relation or scene root; synthetic metadata lookup is the
    countermodel;
  - CTRL_F: intrusive release/assign/retain does not qualify a
    NiRefObject/NiNode class or ownership of T by R; retention by the manager
    has a different receiver;
  - CTRL_G: lack of return/writer closure stays UNKNOWN; no R/T result
    promotes main visual, transform, world-instance, channel or XYZ.
- Missing control/evidence = NOT_PERFORMED with a finding.

## 6. Pre-committed honest outcomes (recorded precisely + STOP, no continuation for a positive)

- BOUND_REACHED with the last proven edge if a concrete next body/edge/
  writer/hop would exceed a limit.
- RETURN_VALUE_ORIGIN = PARTIAL/UNKNOWN if the return paths cannot be closed
  in bound; every reachable alternative reported with its predicate.
- PLUS4_WRITER_AND_SOURCE = UNKNOWN/PARTIAL if writer closure is not achieved
  in bound (NO global writer census).
- RETURNED_OBJECT_CLASS_IDENTITY = UNKNOWN if no vptr/RTTI/construction tie
  with dataflow to R is established; nearby RTTI is rejected by CTRL_A.
- No promotion of any standing science status; negative/partial results are
  publishable; publication (parent phase) is not acceptance.

## 7. Prohibitions honored (contract §1/§3)

NOT examined: FUN_006C8BB0, FUN_007B6C30, FUN_007BF900/FUN_007BF630, join
implementation, main visual role, transform owner, coordinate frame, world
instance, historical records, XYZ; no runtime/client launch; no network
science; no VFS/BNT/NIF corpus research; no class atlas; no viewer work; no
general decoder hardening; no automatic follow-up; no extending the CTRL_4
checkers into a universal decoder/semantic verifier. No status changes by
analogy to standing science.
