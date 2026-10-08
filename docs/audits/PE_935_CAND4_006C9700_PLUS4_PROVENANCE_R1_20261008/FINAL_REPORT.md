# FINAL_REPORT — PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008

RUN_CLASS: BOUNDED STATIC_RE_SCIENCE · Era: PCG 9.3.5 client image (Entropia
Universe 9.3.5; Entropia.exe 8,015,872 B / SHA256 E7785430E81DFFE648CE8F5312414B17
BC9FCE61389689A22F753765D5280F31 — the ONLY byte source, fail-closed in every
tool). Executor: pe-reconstruction (bounded worker phase under direct PE-MASTER
dispatch; NO_NESTED_TASKS). BASE_SHA 97823c6180b0a35a8f5c43e45c29076d48208bee
(== LOCAL_HEAD == origin/master == live remote master at preflight; the first
ls-remote attempt failed transiently and is disclosed in INPUT_IDENTITIES.md §1).
STATIC-ONLY — the client never ran; no runtime, no payloads, no network science.
Decoder: capstone 5.0.7 (existing install re-measured, identity INPUT_IDENTITIES.md
§5) + this run's own rel32 arithmetic + manual encoding cross-checks
(01_RAW/MANUAL_ENCODING_CROSSCHECK.txt). QC phase: SEPARATE (fresh QC worker —
QC_REPORT.md is NOT written by this executor; QC_ORIGIN for this executor phase =
NOT_PERFORMED_BY_EXECUTOR). Persistence (entrypoint/manifest/commit/push) = the
parent's later phase.

---

## 1. THE ONE QUESTION AND THE ANSWER

**QUESTION (contract §1):** Na ścieżkach zgodnych z zapisanym callerem CAND-4:
skąd pochodzi wynik R z FUN_006C9700 i kto nadaje wartość odczytywaną później
jako [R+4]?

**ANSWER (measured, bounded — see §2–§5 for the exact expressions and §8 for
the status ladder):**

1. **RETURN_VALUE_ORIGIN**: R (the non-NULL return) is the **0x10-byte heap
   object allocated inside FUN_006C9700 at 0x006C97BB (operator new per prior
   canon; size 0x10 pushed @0x006C97B9) and constructed in place by
   FUN_006E8F70(this = the allocation, arg1 = S, arg2 = P) @0x006C97D8, which
   RETURNS `this`** (mov eax,esi @0x006E9014) — the pump returns that result
   (mov eax,esi @0x006C9808). ORIGIN CATEGORY = **ALLOCATION + CONSTRUCTION**
   (the exact source expression: the ctor's this; path predicate = PATH_B:
   S != NULL AND the arg1-slot != 0 after FUN_006C9570 AND new(0x10) != 0 —
   RETURN_VALUE_TRACE.csv). All NULL alternatives are measured with predicates
   (§2).
2. **R's measured structure**: 16 bytes; [R+0] = S (the FUN_00823C10 result —
   an object POINTER, NOT a vptr); [R+4] = P (a refcounted object pointer,
   addref'd [P+4]+=1 at the store); [R+8] = 0 (conditionally populated); [R+0xC]
   = 0. **NO vptr is stored by the construction** → R's class NAME is not
   RTTI-derivable in bound (CTRL_A guards this).
3. **PLUS4_WRITER_AND_SOURCE**: the value later read as [R+4] is assigned —
   **FIRST INITIALIZATION — by the ctor FUN_006E8F70 @0x006E8FA5
   (mov [esi+4],eax; 89 46 04)** with the companion addref [P+4]+=1 @0x006E8FAF;
   the VALUE is P = the content of the pump's arg1 slot, produced by
   **FUN_006C9570 @0x006C9651 (mov [esi],edi)** — a smart-pointer slot-set of
   the **return value of FUN_007B79B0 (receiver = [S+0x10])**, addref'd
   [P+4]+=1 @0x006C9657 (the slot is pre-cleared @0x006C95A0, discarding the
   original A id). The DEEPER origin of P (inside FUN_007B79B0) is
   **NOT_ESTABLISHED_WITHIN_BOUND** (body #4 extent PARTIAL; the edge budget
   exhausted at the preregistered 12/12 — STOP_BEFORE_EXCEED honored; its
   internal callsites are RAW_VISIBLE_ONLY). LATER OVERWRITE of [R+4]:
   NOT encountered within the opened chain (NOT a global census — outside the
   chain = NOT_CHECKED).

## 2. RETURN_VALUE_ORIGIN (paths, predicates, extent)

See RETURN_VALUE_TRACE.csv (five RESOLVED paths) and 01_RAW/FUN_006C9700_PUMP_FULL.txt.
The pump (cdecl 4 args; extent RESOLVED 0x006C9700..0x006C981B):
- builds the 8-byte request pair {type=0x66 (MODEL), id=A} (@0x006C973A/@0x006C9742
  — the prior-canon request family, cited);
- O = FUN_00415670(&pair, arg2, arg3, 1) (@0x006C9746; callee cleans 0x10 —
  dataflow-verified);
- S = FUN_00823C10(thiscall O) (@0x006C974D);
- if S == NULL → return 0 (PATH_A);
- FUN_006C9570(S, &arg1-slot, arg4) (@0x006C9764) sets the slot;
- if slot == 0 → FUN_008268A0(S, arg3) (@0x006C977B; body NOT opened) →
  return 0 (PATH_C / PATH_C_RELEASE);
- else R = new(0x10) (@0x006C97BB) → FUN_006E8F70(new, S, slot-P)
  (@0x006C97D8) → release the caller-side P (dec [P+4] @0x006C97F3 +
  vtable-slot-1 destroy @0x006C9806) → **return the ctor result** (PATH_B).
On the CAND-4 caller conditions (arg4 = 0; the SAME arg4=0 as the recorded
historical caller — 6A 00 @0x006CB7BD), PATH_B is the only R-producing path.
A static path is NOT an observed execution.

## 3. RETURNED_POINTER_BASE_AND_ADJUSTMENT

The returned value is the ctor's `this` = the allocation base (ECX of the ctor =
EAX of new @0x006C97BB; ESI == that base; returned unmodified @0x006C9808). **NO
pointer adjustment** — RESOLVED. (This rules out an adjusted/subobject return on
PATH_B within bound.)

## 4. RETURNED_OBJECT_CLASS_IDENTITY

R = the 16-byte handle object {+0: S, +4: P (refcounted), +8: sub-object, +0xC:
0} constructed by FUN_006E8F70. The construction writes NO vptr (89 06 stores
the S pointer at +0) → **class NAME = UNKNOWN within bound** (no COL/TypeDescriptor
chain exists for R; nearby RTTI does NOT qualify it — CTRL_A). R is NOT the 0xC
ArkModelResourceInstanceRef wrapper (W): W is allocated by the OTHER recorded
caller (new(0xC) @0x006CB819, ctor FUN_006FA8B0(W, R) @0x006CB836 — cited prior
record); different size, different construction, different caller; the CAND-4
path creates NO W. Naming R "ArkModelResourceInstance" from W's name alone is
REJECTED (CTRL_C) — that inference is not made by this run.

## 5. PLUS4_WRITERS_WITHIN_BOUND / PLUS4_WRITER_AND_SOURCE

Writers census within the opened creation/return chain (PLUS4_PROVENANCE.csv):
- **PW-1 (THE [R+4] writer, first init)**: FUN_006E8F70 @0x006E8FA5
  (89 46 04) — value P; addref [P+4] @0x006E8FAF (01 48 04; ecx=1).
- **PW-2 (the upstream producer of the value)**: FUN_006C9570 @0x006C9651
  (89 3E) — slot = FUN_007B79B0([S+0x10]) return; addref @0x006C9657 (01 5F 04);
  slot pre-cleared @0x006C95A0 (C7 06 00 00 00 00).
- PW-3 (the deeper origin inside FUN_007B79B0): NOT_ESTABLISHED_WITHIN_BOUND —
  the visible head allocates a 4-byte object (0x0095D3C4(4) — RAW arith only,
  identity NOT adjudicated at this site), initializes it (0x007B7930 — RAW),
  and dispatches a receiver vtable-slot-3 call (RAW); the return path past the
  window cut @0x007B7A0F is NOT decoded. Interpreting those result flows would
  be NEW edge units (13+) — the preregistered MAX 12 was reached; STOP honored.
- Value at FIRST INIT: P = a heap object address carrying the intrusive
  refcount protocol (refcount at [P+4]: ADD forms 01 48 04/01 5F 04; DEC
  83 40 04 FF; destroy via P's vtable slot 1 at zero count — the pump's release
  blocks @0x006C9790..A3/@0x006C97F3..06). P's class identity: UNKNOWN in bound.
- LATER OVERWRITE: NOT_ENCOUNTERED_WITHIN_BOUND (the only [x+4] writes in the
  four opened bodies besides PW-1 have destination base P — the refcount ops).

## 6. PLUS4_TARGET_CLASS_AND_LIFETIME (T — only to the encountered-evidence ceiling)

**T == P (alias PROVEN by dataflow — POINTER_LINEAGE HP-3)**: the installer's
read [R+4] (@0x006C67BE, 8B 78 04 — prior-canon pin, re-pinned) reads the very
value PW-1 stored; T is then stored to [manager+0x68] (@0x006C67E2) and
addref'd [T+4] (@0x006C67E7 — prior-canon pins). T's protocol (measured, this
run + prior re-pins): intrusive refcount at +4 (ADD/DEC; EBX=1 established by
BB 01 00 00 00 @0x006C67C9 — MOV, not an INC opcode), destroy via vtable slot
1 at zero count; T is usable as a NAMED-LOOKUP RECEIVER (this run: the ctor's
conditional branch calls P→vtable slot 17 (+0x44) with the measured name
"Geowater:0" @0x006E8FE6/EB — E10; prior canon: the installer's 'ArkTexture'/
'ArkAnimation' lookups via FUN_007B6C30 — cited). T's CLASS NAME: NOT established
in bound (P's vtable is runtime data; the deeper origin NOT adjudicated). T's
lifetime model: intrusive-refcounted object shared by reference (the pump,
the ctor's R, and the manager each hold/addref references). T's downstream role
(visual/scene/model root): NOT_ADJUDICATED (no downstream trace of T was
performed, per contract).

## 7. ARKMODELRESOURCEINSTANCEREF_RELATION (conditional — conflict not forced)

The prior pointer-vs-count conflict (the W-class prior map count@+4/item@+8
"CONTRADICTS pointer use IF the pump returns that wrapper") is now physically
resolved FOR THE CAND-4 CHAIN: the pump does NOT return the 0xC wrapper; it
returns the 0x10 handle R, and **[R+4] is an object POINTER** (P — stored,
addref'd, released, and read back as a pointer by the installer on the same
base R). The count field of the W map lives at W's base (a different object of
a different caller; W+8 = R per the inherited prior-canon map — cited, not
re-measured). **Status: RESOLVED_AS_POINTER for the CAND-4 chain** (same-base
dataflow, measured — not assumed); W's own map unchanged (prior canon). No MI/
subobject alternatives were investigated beyond the encountered evidence (no
forced conflict either way — CTRL_D's discipline).

## 8. R_TO_T_RELATION_TYPE / R_TO_T_ALIAS_STATUS / R_TO_T_OWNERSHIP_STATUS

- **R_TO_T_RELATION_TYPE = R_CONTAINS_POINTER**: R (the 16-byte handle) contains
  the pointer P at +4 (the ctor store PW-1 + the addref). CONFIRMED at byte level.
- **R_TO_T_ALIAS_STATUS = T == P PROVEN (alias of roles); R != T**: R is the
  handle; T is the contained object. The alias is established across the two
  RECORDED callers + this run's measured store (NOT one observed execution).
- **R_OWNS_REFERENCE = R holds ONE REFCOUNTED REFERENCE to P/T** (the ctor's
  addref [P+4]+=1 @0x006E8FAF). The symmetric release inside R's own destruction
  is NOT opened (the RAW-visible deleting-destructor-shaped neighbor
  @0x006C9820 — role NOT adjudicated) → ownership status: ONE_REFERENCE_HELD
  (measured addref) / release-on-destroy NOT_CHECKED. The manager's retention of
  T ([manager+0x68]=T + [T+4]+=1) is a SEPARATE reference with a DIFFERENT
  receiver (CTRL_F).
- R == W / class(R) == class(W): NOT proven, and NOT assumed either way; the
  measured difference (0x10 vs 0xC allocation; construction site; caller) is
  recorded (CL-14).

## 9. TRACE_COVERAGE / NOT_CHECKED

COVERED (this run): FUN_006C9700 (full), FUN_006E8F70 (full), FUN_006C9570
(full), FUN_007B79B0 (head, PARTIAL); the request-pair build; the CAND-4-path
flag branch; the P refcount/release protocol; the ctor's conditional [R+8]
branch head (E9/E10 + RAW tail); the RTTI re-pins; the string constants.
NOT_CHECKED (explicit; with reasons — FUNCTION_BODY_ACCOUNTING.csv):
FUN_00415670, FUN_00823C10 (S/O identity — not required for the two required
results); FUN_008268A0 (the slot==0 path — returns 0); FUN_007B7660 (off-CAND-4
variant; callsite-level interpretation only); FUN_00728150, FUN_00769510,
FUN_006E8A90, FUN_006B2310 (the [R+8] conditional tail — RAW_VISIBLE_ONLY);
FUN_007B7930 (RAW); FUN_006C9670 + the 0x006C9820 neighbor (RAW display only);
FUN_006C8BB0, FUN_007B6C30, FUN_007BF900, FUN_007BF630, FUN_007BF470, the join
implementation (contract §1 prohibitions — never touched); runtime anything;
payloads; the downstream role of T.

## 10. UNRESOLVED_EDGES

1. The deeper origin of P inside FUN_007B79B0 (its return path; whether the
   4-byte object / the slot-3 virtual participate) — NOT_ESTABLISHED_WITHIN_BOUND
   (edge budget 12/12; body #4 PARTIAL). This is the single open edge of the
   PLUS4 source chain.
2. S's and O's identity (FUN_00823C10 / FUN_00415670 bodies unopened) — R's +0
   content is measured as a pointer; its class is NOT adjudicated.
3. P's/T's class identity (runtime vtable; construction site unopened).
4. R's release path (the neighbor destructor's ownership) — NOT adjudicated.
5. The [R+8] conditional population (RAW tail) — not load-bearing here.

## 11. CTRL_A..CTRL_G (contract §6 — dispositions)

All seven performed and PASS (CONTROL_RESULTS.json; the mechanical gates run on
the PHYSICAL EXE via the production checker; corruptions are IN-MEMORY copies —
the file is never modified):
- CTRL_A = PASS (nearby W RTTI does not qualify R; R has no vptr edge).
- CTRL_B = PASS (unproven base mixing rejected; the PROVEN alias T==P accepted
  as a legal result — not an automatic FAIL).
- CTRL_C = PASS (ctor(W,R) + the W name do not qualify class(R); no separate
  edge exists for R).
- CTRL_D = PASS (unproven condition stays CONDITIONAL_UNRESOLVED; the prior W
  map is not a new layout measurement; the proven base resolves the conflict
  as POINTER — measured, not assumed).
- CTRL_E = PASS (name constants alone qualify no lookup/child/scene-root claim;
  the callee bodies are unopened).
- CTRL_F = PASS (the refcount protocol qualifies NO class and NO absolute
  ownership; the manager's retention has a different receiver).
- CTRL_G = PASS (the missing deeper-origin closure stays UNKNOWN; NO
  main-visual/transform/world-instance/channel/XYZ promotion anywhere).
Mechanical anchor validation: clean pass 80/80; MC1 (+4 writer pin corruption →
detected), MC2 (ctor return-this → detected), MC3 (pump return-R → detected),
MC4 (ctor call rel32 → detected), MC5 (W RTTI chain name → detected) — each by
the SAME production gate with the correct cause; MC6 (unrelated-byte corruption
→ anchor gates remain PASS — specificity). The whole-file SHA gate is NOT used
as the corruption detector (documented — a manifest-level failure is not anchor
validation).

## 12. QC (separated from the science result)

FRESH internal QC = the PARENT'S separate phase (a fresh QC worker;
00_CONTROL_INTERNAL_QC/QC_PHASE_INPUTS.md lists the inputs it must independently
check). By this executor: NOT_PERFORMED (QC_REPORT.md intentionally absent;
no self-review is labeled independent). REAL_SCIENCE_AUTO_QUALIFICATION =
DISABLED; SCHEMA_CHECK != PIN_CHECK != STRUCTURAL_CHECK != SEMANTIC_ADJUDICATION;
the class/return/source adjudications above are the AUTHOR's explicit
adjudication from the byte evidence — the checker/controls validate only the
physical anchors and the unauthorized-inference rejections.

## 13. Budget disposition (actual vs preregistered maxima)

| budget | preregistered MAX | used | status |
|---|---|---|---|
| MAX_NEW_FUNCTION_BODIES_OPENED | 6 | 4 (B-1 RESOLVED; B-2 RESOLVED; B-3 RESOLVED; B-4 PARTIAL) | WITHIN |
| MAX_NEW_INTERPROCEDURAL_EDGES_ANALYZED | 12 | 12 (E1..E12) | AT LIMIT — NOT exceeded (STOP_BEFORE_EXCEED honored at the FUN_007B79B0 boundary; 9 RAW_VISIBLE_ONLY rows with explicit reasons) |
| MAX_NEW_PLUS4_WRITERS_TRACED | 4 | 2 (PW-1, PW-2; PW-3 = the honest boundary row) | WITHIN |
| MAX_NEW_WRAPPER_OR_SUBOBJECT_HOPS | 3 | 3 (HP-1 R→P; HP-2 S→P; HP-3 T==P) | AT LIMIT — NOT exceeded |

SCOPE/BUDGET_COMPLIANCE = WITHIN (no exceedance; no retroactive authorization
needed). Process disclosures: the transient first ls-remote failure (INPUT_
IDENTITIES.md §1); the historical-caller pin transcription error caught by the
production gate on the clean-pass attempt 1 and corrected to the measured bytes
(01_RAW/MANUAL_ENCODING_CROSSCHECK.txt item 13).

## 14. Standing science (preserved verbatim; contract §7)

CHILD_RESOURCE_PROVENANCE = STRONGLY_SUPPORTED_MODEL_DERIVED · MODEL_ROOT_RELATION
= UNKNOWN · CHILD_VISUAL_ROLE = UNRESOLVED · CHILD_TO_JOIN_IDENTITY =
STRONGLY_SUPPORTED · EXACT_PARENT = CONFIRMED_EXACT_SCENEFEEDER_PLUS_30 ·
PARENT_SCOPE = EXAMINED_ACLD_PLUS_18_SF_INSTANCE · JOIN_OPERATION =
STRONGLY_SUPPORTED · CAND4_CHILD_ROOT_CLOSURE = NOT_ESTABLISHED_WITHIN_BOUND ·
WORLD_INSTANCE = NOT_ESTABLISHED · WORLD_XYZ_RECOVERED = NO ·
STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED · HISTORICAL_INSTANCE_DATA_RECOVERED =
NO · CANONICAL_GATE_EFFECT = NONE.

No promotion is performed by this run. This run's new evidence concerns EXACTLY
the prior GAP-1 ([instance+4] identity) and the prior lineage H-2 relation: as
THIS run's measured results — [R+4] = P (a contained refcounted object pointer;
NOT a count) and H-2's relation = the measured handle→contained-object store —
they are reported here and in the ledgers for the parent's adjudication; the
top-level standings above are NOT auto-promoted (publication != acceptance).

## 15. Governance statuses

RUNTIME_JOIN_OBSERVED = NO (STATIC-ONLY) · NEXT_EXPERIMENT_AUTHORIZED = NO ·
HARD_STOP = YES (after the package; the entrypoint/manifest/commit/push belong
to the parent phases) · NEW_DESKTOP_POST_AUDIT = NOT_PERFORMED ·
TRANSFORM_OWNER / COORDINATE_FRAME = NOT_ADJUDICATED_BY_THIS_RUN (prior status
preserved) · T types/roles outside the encountered evidence =
NOT_ADJUDICATED/UNRESOLVED.
