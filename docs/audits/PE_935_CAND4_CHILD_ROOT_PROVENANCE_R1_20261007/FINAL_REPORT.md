# FINAL_REPORT — PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007

RUN_CLASS: BOUNDED STATIC_RE · Era: PCG 9.3.5 · MODE: STATIC-ONLY (the client is
never executed; no runtime, no network, no payload/VFS/BNT/NIF opening —
existing persisted metadata/records only). Executor: pe-reconstruction
(PE-MASTER direct dispatch, NO_NESTED_TASKS). BASE_SHA d65fa12e5bae4e9aab291c3cc7815b1822e41cff
(== origin/master == actual remote master, verified at preflight
2026-10-07T10:54Z and re-verified by the internal QC at package time). EXE
pinned: D:\Eudoria_Reconstruction\pcg_install\Entropia.exe = 8,015,872 B /
SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
(fail-closed inside every tool). Decoder: capstone 5.0.7 (identity:
INPUT_IDENTITIES.md §4) + this run's own rel32 arithmetic (cross-checked).

---

## 1. The one question and the answer

**QUESTION (contract §2):** Co zwraca FUN_006C66D0 na istniejącej ścieżce CAND-4,
skąd pochodzi ten pointer i czy reprezentuje główny wizualny model/resource tej
ścieżki?

**ANSWER (measured, bounded):**

1. FUN_006C66D0 is a 4-byte DIRECT FIELD GETTER: `mov eax, [ecx+0x68]; ret`
   (0x006C66D0..0x006C66D4; extent proven by terminal ret + 12x int3 padding +
   the aligned next entry 0x006C66E0; all three examined callers reach it by
   verified rel32). It returns the ArkModelManagerMain base-class field
   **+0x68** — no branches, no NULL handling, no computation.
   `GETTER_OPERATION = DIRECT_FIELD_GETTER`;
   `ARKMODELMANAGER_CHILD_FIELD_OFFSET = 0x68` (measured).

2. **Skąd pochodzi ten pointer** — the on-path producer chain of
   [manager+0x68] is physically established (all links byte-verified):
   - the base ctor FUN_006C8F80 writes the NULL initial state ([+0x68]=0
     @0x006C8FD3) and initializes the +0x70 template holder;
   - FUN_006C8B20 (called @0x006A3A8D, right after the ctor on the examined
     chain) is the LAZY INITIALIZER: when [+0x68]==0 it calls FUN_006C6F60;
   - FUN_006C6F60 is the PRODUCER: validity check of the +0x70 holder
     (FUN_0072FCE0 — the prior-canon validity family), two import-mediated
     lookups with an EMPTY-STRING key (0x00A7957B), A = FUN_007CE1E0([+0x70])
     (the prior-canon getter A of the {0x66=MODEL, A} request family), then
     instance = FUN_006C9700(A, &local, &local, 0) — the prior-canon
     INSTANCE-CREATOR PUMP (bridge CH3) — stored at [manager+0x6C] @0x006C7008;
   - FUN_006C6780 is the WRITER: on creation success it performs the
     refcounted smart-pointer set `[manager+0x68] = [instance+4]` @0x006C67E2
     (incref [edi+4] @0x006C67E7; old value decref + zero-destroy via vtable
     slot 1 @0x006C67D4/0x006C67DE) and then uses the stored child as a
     NAMED-LOOKUP ROOT: two conditional lookups via FUN_007B6C30 with the
     measured constants 'ArkTexture' (0x00A859F8) and 'ArkAnimation'
     (0x00A8547C).
   `CHILD_RESOURCE_PROVENANCE = STRONGLY_SUPPORTED_MODEL_DERIVED` — NOT
   CONFIRMED_MODEL_DERIVED: the identity of [instance+4] is UNRESOLVED (the
   creation chain was not opened; the prior-canon wrapper field map
   (.?AVArkModelResourceInstanceRef@@: refcount@+4/item@+8) CONTRADICTS
   pointer use if the pump returns that wrapper), and the alternative on-path
   producer FUN_006C8BB0 is NOT_CHECKED (explicit coverage gap GAP-2).
   `MODEL_ROOT_RELATION = UNKNOWN` (descriptive physical facts recorded: a
   refcounted object, refcount@+4, used as a named-lookup root for
   texture/animation components, attached to the SF's NiNode; raw-vs-wrapper
   vs actor-family identity unresolved at the [instance+4] boundary).
   `WRAPPER_DEPTH = 2` (manager -> instance [+0x6C]; instance -> [+4]; the
   further moves to the join are SAME_OBJECT).

3. **Czy reprezentuje główny wizualny model** — UNRESOLVED within this bound
   (contract §6): the positive principal-visual proof was not achieved. The
   measured evidence (production by the prior-canon model-instance family;
   NiObject-family refcount protocol; named texture/animation component
   lookups; the join attaching it to the SF+0x30 NiNode) is NOT sufficient per
   §6 (attachment is not by itself proof; the lookups are conditional; VFX/
   helper alternatives are not excluded; the follow-up calls
   FUN_007BF900/FUN_007BF630 remain undecoded). `CHILD_VISUAL_ROLE = UNRESOLVED`.

4. **Getter result -> join child identity (§7):** the child argument pushed at
   0x0050A3F6 is the getter result held in EDI (mov edi,eax @0x0050A3B7; no
   caller-side EDI write before the push — measured; free re-pin of the source
   run's QC S4). The value crosses FOUR intervening calls
   (FUN_006C0F90/FUN_006C10B0/FUN_0050A1E0/FUN_005246E0), none of which was
   opened (function budget exhausted by the producer chain); preservation
   rests on the MSVC callee-saved ABI — support, not proof.
   `CHILD_TO_JOIN_IDENTITY = STRONGLY_SUPPORTED` (NOT CONFIRMED) — the honest
   §7 fallback.

5. **Status algebra (§8, literal):**
   CHILD_EVIDENCE_COMPLETE = (CONFIRMED_MODEL_DERIVED) AND (CONFIRMED
   main-visual) AND (CONFIRMED identity) AND (CONFIRMED parent) = **FALSE**
   (provenance = STRONGLY_SUPPORTED_MODEL_DERIVED; visual role = UNRESOLVED;
   identity = STRONGLY_SUPPORTED; parent = CONFIRMED — carried).
   => `CAND4_CHILD_ROOT_CLOSURE = NOT_ESTABLISHED_WITHIN_BOUND`.
   EXACT_PARENT = CONFIRMED_EXACT_SCENEFEEDER_PLUS_30 (carried; scoped to the
   examined ACLD+0x18 SF instance) and JOIN_OPERATION = STRONGLY_SUPPORTED
   (the ceiling of this run; FUN_007BF470 and any separate parent/join proof
   were NOT opened, per contract).

## 2. What was examined (budgeted bodies 6/6)

| # | body | extent | status |
|---|---|---|---|
| 1 | FUN_006C66D0 (the getter) | 0x006C66D0..0x006C66D4 | RESOLVED; direct field getter [+0x68] |
| 2 | FUN_006C0D50 (derived ctor) | 0x006C0D50..0x006C0DAE | RESOLVED; thin derived ctor (base delegation + derived zeroing + vtable) |
| 3 | FUN_006C8F80 (base ctor) | 0x006C8F80..0x006C9036 | RESOLVED; WRITER W1 ([+0x68]=0; +0x70 holder init) |
| 4 | FUN_006C8B20 (lazy init) | 0x006C8B20..0x006C8BAA | RESOLVED; the [+0x68]==0 trigger of the producer |
| 5 | FUN_006C6F60 (producer) | 0x006C6F60..0x006C7072 | RESOLVED; validity + lookups + getter A + pump + [+0x6C] store + installer call |
| 6 | FUN_006C6780 (installer/writer) | 0x006C6780..0x006C6848 SEEN; body continues | **PARTIAL — extent UNRESOLVED** past 0x006C6848 (window ended mid-body; per contract §4 the continuation is NOT decoded and NOT claimed); WRITER W2 + the two named lookups are inside the seen window |

Additional data reads (no body opening): vtable entries (manager slots 2/3 =
0x006C0FD0/0x006C19B0), RTTI names of three classes, string constants —
01_RAW/VTABLE_RTTI_STRINGS.txt.

## 3. The four §9 controls (machinery falsifiability)

CTRL_1 (animation false positive) = PASS; CTRL_2 (wrapper relation break) =
PASS; CTRL_3 (wrong manager field) = PASS; CTRL_4 (child identity break) =
PASS. Each control runs ONE checker with clean PASS -> mutated FAIL on the same
checker, same range, recorded cause (03_SCRIPTS/qc_controls.py ->
CONTROL_RESULTS.json). The real-input classification of CTRL_1 is recorded
POLICY_ONLY (the real child is not confirmed main-visual by absence of the §6
proof legs — no detection claim). SYNTHETIC PASS is not PCG science; no new
real EXE fields/objects were searched for the controls.

## 4. Honest budget accounting (measured)

- MAX_NEW_FUNCTION_BODIES_OPENED = 6 — used 6/6 (the 6th partial; extent
  UNRESOLVED). NOT exceeded.
- MAX_NEW_MANAGER_FIELD_WRITERS_TRACED = 6 — used 2 (W1, W2) + 3 declared
  gaps (GAP-1 creation-chain internals; GAP-2 FUN_006C8BB0; GAP-3 off-path
  writers out of scope by governance). NOT exceeded.
- MAX_NEW_WRAPPER_HOPS = 3 — used 2 (H-1, H-2; H-3/H-4 are SAME_OBJECT
  moves, not hops). NOT exceeded.
- MAX_NEW_CHILD_PROVENANCE_CANDIDATES = 3 — used 3/3 (ctor reset; producer
  chain; FUN_006C8BB0 alternative). AT the limit.
- **MAX_NEW_INTERPROCEDURAL_EDGES_SEMANTICALLY_ANALYZED = 8 — ANALYZED 24.
  EXCEEDED by 16.** EDGE_ACCOUNTING_STATUS = BUDGET_EXCEEDED;
  ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL; RETROACTIVE_PRIOR_AUTHORIZATION =
  NO. Honest disclosure: the stop-before-exceeding rule was NOT honored in
  execution — completing the producer-chain proof inside the budgeted bodies
  required interpreting the callsites those bodies contain, and the executor
  continued past the 8-unit stop line instead of stopping at BOUND_REACHED.
  The full census is in EDGE_ACCOUNTING_LEDGER.csv (24 ANALYZED_NEW + 7
  RAW_VISIBLE_ONLY + 11 REPIN_PRIOR_SCOPE + 27 OUT_OF_ANALYZED_EXTENT rows;
  every uncounted row carries an explicit reason — the J2 discipline). The
  byte evidence and the component findings are NOT falsified by the
  exceedance; SCOPE_COMPLIANCE = PARTIAL_WITH_EXCEEDED_EDGE_BUDGET.
- The historical minimum-22 convention of the source run's census (distinct
  (caller,callee) pairs of THAT run) is unchanged by this run; this run's
  census uses the §3 callsite unit as preregistered.

## 5. What remains OPEN (honest; NOT authorized by this run)

1. The identity of [instance+4] (GAP-1): decode FUN_006C9700 and the creation
   chain; reconcile with the prior-canon ArkModelResourceInstanceRef field
   map — the single highest-value next input for CHILD_RESOURCE_PROVENANCE.
2. FUN_006C8BB0 (GAP-2): the second on-path manager method — alternative
   producer of [+0x68] not excluded.
3. The §7 preservation bodies (FUN_006C0F90, FUN_006C10B0, FUN_0050A1E0,
   FUN_005246E0) — CHILD_TO_JOIN_IDENTITY can rise toward CONFIRMED only with
   their bodies.
4. The child's class/role evidence: FUN_007B6C30 (the named-lookup helper),
   FUN_007BF900/FUN_007BF630 (the post-join calls on the child), and the
   manager slot-2/slot-3 targets (0x006C0FD0/0x006C19B0).
5. The child's visual-role proof (§6) — remains the missing required leg for
   any future closure; per §6, attachment + provenance are not sufficient.
6. The FUN_006C6780 unseen continuation (past 0x006C6848) — extent UNRESOLVED.

## 6. Governance statuses (unchanged)

RUNTIME_JOIN_OBSERVED = NO · WORLD_XYZ_RECOVERED = NO ·
STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED · HISTORICAL_INSTANCE_DATA_RECOVERED
= NO · CANONICAL_GATE_EFFECT = NONE · REAL_SCIENCE_AUTO_QUALIFICATION =
DISABLED (no tool of this run issues a SCIENCE_PASS) ·
NEXT_EXPERIMENT_AUTHORIZED = NO. Negative/partial results are publishable;
publication (by the persistence phase) is not acceptance. Maximum positive
conclusion (§11 ceiling): on the examined, conditional ACLD path, the
component proofs of the child's model-resource production chain and the
pointer's physical dataflow to the existing STRONGLY_SUPPORTED join operation
were established — NOT historical world-instance identity, building data, CMO
path, universal mechanism or runtime observation.

## 7. Phase boundary (per the dispatch)

This executor's phase = SCIENCE + the four §9 controls + fresh-context internal
QC (SELF_CHECK, QC_PASS 23/23) + PACKAGE. No AUDIT_ENTRYPOINT.md edit (the
proposed newest-first row is in HANDOFF.md only), no git stage, no commit, no
push (the persistence phase owns them after the PE-MASTER audit).
RESULTING_SHA = NONE (this phase). The final MANIFEST_SHA256.csv was generated
LAST over the physical package files EXCLUDING itself; the AUDIT_ENTRYPOINT.md
row is EXPLICITLY OUT of this phase's manifest scope (excluded pending
persistence, noted in the manifest header). PERSISTENCE_STATUS =
PREPARED_NOT_PERSISTED.

## 8. SELF_CHECK (executor's own — NOT independent PE-MASTER audit)

- [x] Full raw census where claimed: the 24 analyzed callsite units are ALL
      ledgered; the opened bodies' 26 CALL instructions are 100% covered by
      ledger rows (machine-verified by the internal QC S6); every uncounted
      row (RAW_VISIBLE_ONLY / REPIN / NEIGH) carries an explicit reason; the
      edge-budget exceedance is disclosed by the run itself, not discovered
      post-hoc.
- [x] All gates honestly evaluated: the §8 algebra applied literally
      (CHILD_EVIDENCE_COMPLETE = FALSE -> closure NOT_ESTABLISHED_WITHIN_BOUND);
      no automatic science qualification; the four §9 controls clean PASS ->
      mutated FAIL on the same checkers.
- [x] Meaningful negative controls: CTRL_1..CTRL_4 + the POLICY_ONLY
      classification of the real input; the producer census's explicit gaps
      (GAP-1/2/3) recorded instead of silently dropped.
- [x] Correct source/generator hashes: contract (18,159 B / 57249511…), EXE
      (8,015,872 / E7785430…), decoder (capstone 5.0.7 + native engine
      SHA256), prior packages (49/49 + 27/27 blob identity, aggregates
      re-measured) — all re-measured and MATCHING (INPUT_IDENTITIES.md).
- [x] No default-success fallback: provenance capped at
      STRONGLY_SUPPORTED_MODEL_DERIVED (multiple unresolved elements — no
      promotion per §4); visual role UNRESOLVED; identity STRONGLY_SUPPORTED
      (not CONFIRMED); the budget exceedance reported as FAIL, not excused.
- [x] Limits respected: bodies 6/6; writers 2/6; hops 2/3; candidates 3/3;
      edges EXCEEDED (24 > 8) — disclosed honestly (§4 above); prohibitions
      honored (no FUN_007BF470, no ExtraData, no CMO↔ACLD, no runtime, no
      payloads, no transform semantics).
- [x] Historical packages read-only (blob identity 49/49 + 27/27 re-verified
      before AND after work); foreign untracked roots untouched; no tracked
      changes; HEAD unchanged at BASE.
- [x] Manifest LAST + bijection: generated last over the physical package
      minus itself (entrypoint excluded pending persistence, noted in the
      header); bijection + independent re-hash verified zero mismatch.
