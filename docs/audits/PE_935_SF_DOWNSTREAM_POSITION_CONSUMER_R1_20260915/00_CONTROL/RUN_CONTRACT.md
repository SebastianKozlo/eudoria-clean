# RUN_CONTRACT — PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915

## FORMALIZER PROVENANCE HEADER (by pe-master-auditor; part of the released contract)

- Formalized by: pe-master-auditor (FORMALIZE mode; parent = PE-MASTER direct bounded dispatch).
- Dispatch received: 2026-09-15, in-chat Task order from PE-MASTER (the order text is the authoritative source of the requirements below; no separate on-disk parent contract file was supplied).
- Human authorization chain (parent-relayed): exactly ONE bounded science run -> fresh QC -> PE-MASTER adjudication -> bounded correction if needed -> re-QC -> persistence -> HARD STOP. NO AUTO LOOP.
- PARENT_LOOP_ID: PE-MASTER direct dispatch 2026-09-15 (no active loop_id on disk at formalize time; the historical loop 2ed038db-5d2e-4e7e-b679-2d29bf57501a is COMPLETED and is read-only context only).
- NO_NESTED_TASKS: the executor MUST NOT dispatch any nested Task or subagent. All work is performed by the single executor session; the single return goes to PE-MASTER.
- TIMEBOX: one bounded executor session, owned and terminated by PE-MASTER. No numeric timebox was declared by the parent at formalize time; if PE-MASTER declares a deadline at dispatch, the executor stops there; otherwise the executor stops at natural completion of the bounded scope or at its own context boundary (persist an exact RESUME_POINT, return to PE-MASTER, never overrun, never start follow-up science).
- Formalize-time verification (measured 2026-09-15T06:10 local, -07:00; values in 00_CONTROL/SOURCE_IDENTITIES.json and 01_RAW/AT_RUN_START_GIT_OBSERVATION.md SECTION 1): Entropia.exe SIZE 8015872 + SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 — MATCH to the S0 pin; PE32 i386 / ImageBase 0x00400000 / 5 sections — MATCH; repo HEAD == origin/master == ls-remote == 3068f31ad8db7e993a72365dc28cc03066095afd == BASE_SHA below — MATCH; pre-existing untracked inventory == exactly the two declared paths — MATCH; worktrees match the parent's declaration; the output root `docs/audits/PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915/` did NOT exist and was created fresh by this formalization (no output-root collision).
- Executor action on this file: READ-ONLY. Corrections to the contract itself are PE-MASTER-owned (a fresh formalize pass or an explicit correction order); the executor never edits this file and never needs to re-persist it (it already lives at 00_CONTROL/RUN_CONTRACT.md). The SHA256 of this file (post-final-edit) is recorded by the formalizer in 01_RAW/AT_RUN_START_GIT_OBSERVATION.md SECTION 1 and in the formalizer's return to PE-MASTER.

---

## === RUN IDENTITY ===

RUN_ID: PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915
RUN_CLASS: MATERIAL (declared by PE-MASTER per A1.1; may be reclassified UP at adjudication if findings become load-bearing)
RUN_TYPE: STATIC_SEAM_PROBE
MILESTONE: EU935-M1
PRIMARY_TARGET: PCG_9_3_5
EXECUTOR: pe-reconstruction (to be dispatched after this contract is verified by PE-MASTER)
STATIC-ONLY: the client is NEVER executed. No runtime tests.
TIMEBOX: single bounded executor session owned by PE-MASTER (see FORMALIZER PROVENANCE HEADER; stop at the parent-declared deadline / natural completion / context boundary with an exact RESUME_POINT; no follow-up science; NO AUTO LOOP).
NO_NESTED_TASKS: yes (see FORMALIZER PROVENANCE HEADER). The executor creates the run package in the working tree, performs the science, performs ZERO git mutations (no add/commit/push/stash/checkout/reset/branch — persistence is owned by pe-master-auditor at G17, only after PE-MASTER adjudication G16), and returns exactly once to PE-MASTER.

## === PRIMARY QUESTION ===

After SceneFeeder finds the named NiAVObject, what exactly happens to its m_kWorld translation through the chain NiAVObject+0x90 -> FUN_00437F70 -> FUN_0082B5A0 -> output buffer? Goal: recover the real downstream consumer chain. Do NOT stop at naming functions.

## === PHYSICAL SOURCE (fail-closed S0) ===

- Executable: `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe`
- PIN: SIZE 8015872; SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31; PE32 i386; ImageBase 0x00400000; sections (PE-MASTER-measured 2026-09-15; independently re-verified by the formalizer 2026-09-15, see SOURCE_IDENTITIES.json): .text vaddr=0x1000 raw=0x1000 vsize=0x6735E5 (rawsize 0x674000); .rdata vaddr=0x675000 raw=0x675000 (vsize 0xF6569, rawsize 0xF7000); .data vaddr=0x76C000 (vsize 0x3D6E4, raw=0x76C000, rawsize 0x34000); .tls (vaddr=0x7AA000); .rsrc (vaddr=0x7AB000).
- Every generator/probe must fail-closed re-verify size+SHA256+PE layout BEFORE any decode; mismatch = HARD_STOP. (The formalizer's own parse matched all pinned values; the executor still re-measures at run start — measured bytes win over any prose.)

## === GIT FAIL-CLOSED ===

- Repo: `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean`, branch `master`.
- At run start record (timestamped) — APPEND as SECTION 2 of `01_RAW/AT_RUN_START_GIT_OBSERVATION.md` (the formalizer's SECTION 1 is immutable; do not modify it): HEAD, branch, origin/master, `git ls-remote origin master`, `git status --short`, `git worktree list`.
- Expected HEAD at authorization: 3068f31ad8db7e993a72365dc28cc03066095afd (= origin/master = ls-remote at 2026-09-15T06:03 local; re-measured at formalize time 2026-09-15T06:10 local — all three still equal, MATCH). Live disk > prompt: if master moved, do NOT reset; identify each new commit; unknown/conflicting change = FAIL CLOSED = HARD_STOP.
- Record the pre-existing untracked inventory (expected exactly: `docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/` and `experiments/`) and DO NOT touch it. Everything tracked is expected clean.
- ZERO git mutations by the executor (see RUN IDENTITY). At run end record `01_RAW/AT_RUN_END_GIT_OBSERVATION.md` and verify the untracked set is exactly: the two pre-existing entries + your new run dir.
- WORKTREES (context; verified at formalize time): main worktree at 3068f31 [master]; `worktrees/PE_935_NINODE_SLOT17_GB_ORACLE_MINICHECK_R1` at 5290e79 [audit/pe935-ninode-slot17-gb-oracle-minicheck-r1]; `worktrees/WORK_AUDIT_REPORTS` at 1312f89 [audit/work-audit-reports]. The WORK_AUDIT_REPORTS worktree and the branch `audit/work-audit-reports` are FORBIDDEN (WORK AUDITOR separation: do not read its reports as evidence, do not merge, do not modify, do not coordinate with it).

## === BOOT INPUTS (READ-ONLY references) ===

- A: `docs/audits/PE_935_SF_ARG2_PROVENANCE_R1_20260914/` (minimum: 06_REPORT/REPORT.md, 06_REPORT/HANDOFF.md, 06_REPORT/PE_MASTER_REVIEW.md, 01_RAW/FUN_0050A050_DISASM.txt, 01_RAW/B3_PIN_REVERIFICATION.txt (pin verification), 03_EVIDENCE/EVIDENCE_INDEX.csv) — ABI canon for FUN_0050A050 (thiscall, arg2=[esp+8], ret 8 at both sites, extent 0x50A050..0x50A0AA). All minimum files verified present at formalize time (SHA256 identities recorded in 00_CONTROL/SOURCE_IDENTITIES.json).
- B: `docs/audits/PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914/` (minimum: 06_REPORT/REPORT.md, 01_RAW/ENTROPIA_007B5390_DISASM.txt, 02_ANALYSIS/OFFSET90_ORACLE.md, 06_REPORT/PE_MASTER_REVIEW.md) — slot17 = 0x007B5390 recursive named-object lookup (STRONGLY_SUPPORTED identity NiNode::GetObjectByName); +0x90 = m_kWorld.m_Translate.x measured from Entropia bytes (slot 27 UpdateWorldData + slot 16 anchors). Verified present.
- C: `docs/audits/PE_935_SF_ARG2_UPSTREAM_HOLDER_R1_20260915/` — SUPERSEDING CONTEXT ONLY: the ArkAnimation holder route was REJECTED as the SceneFeeder bridge. Do NOT reopen ArkAnimation science. Verified present.
- All three packages are READ-ONLY (immutable completed run directories). Gamebryo oracle headers/SDKs may be used as SECONDARY corroboration only, never as primary proof for this build (QH-012). Oracle rule: Entropia.exe physical bytes are the primary truth.
- Additional bounded citations allowed where the phases name them (PHASE F item 2): `docs/audits/PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914/` and `docs/audits/PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913/` (SF slot census canon incl. FUN_005094C0 and the slot-1 getter; cited as findings, NOT re-derived beyond the named bounded pin check). Verified present.

## === STANDING KNOWLEDGE = INPUT, NOT AUTOMATIC TRUTH (revalidate every load-bearing pin in-run) ===

All expected values below are PINS to freshly re-measure from the pinned EXE bytes in-run; MEASURED bytes win over these pins; a mismatch is a recorded finding, never silent adoption; never inherit a label without remeasurement.

- SF slot3 FUN_0050A050 extent 0x0050A050..0x0050A0AA; observed ABI: this=ECX=SceneFeederObject, arg1=output float3/vector buffer [esp+4] at entry, arg2=name pointer/nullable lookup key [esp+8] at entry, ret 8.
- Primary branch disasm to freshly re-measure:

```
0x0050A050 mov eax,[esp+8]
0x0050A054 test eax,eax
0x0050A056 push esi
0x0050A057 mov esi,ecx
0x0050A059 je 0x50A087
0x0050A05B mov ecx,[esi+0x30]
0x0050A05E mov edx,[ecx]
0x0050A060 push eax
0x0050A061 mov eax,[edx+0x44]
0x0050A064 call eax
0x0050A066 test eax,eax
0x0050A068 je 0x50A087
0x0050A06A mov esi,[esp+8]
0x0050A06E add eax,0x90
0x0050A073 push eax
0x0050A074 push esi
0x0050A075 call 0x437F70
0x0050A07A mov ecx,eax
0x0050A07C call 0x82B5A0
0x0050A081 mov eax,esi
0x0050A083 pop esi
0x0050A084 ret 8
fallback:
0x0050A087 mov edx,[esi]
0x0050A089 mov eax,[edx+4]
0x0050A08C mov ecx,esi
0x0050A08E call eax
0x0050A090 mov edx,[eax]
0x0050A092 mov ecx,[esp+8]
0x0050A096 mov [ecx],edx
0x0050A098 mov edx,[eax+4]
0x0050A09B mov [ecx+4],edx
0x0050A09E mov eax,[eax+8]
0x0050A0A1 mov [ecx+8],eax
0x0050A0A4 mov eax,ecx
0x0050A0A6 pop esi
0x0050A0A7 ret 8
```

- Do NOT inherit semantics of either helper (0x437F70, 0x82B5A0). SF+0x30 receiver = NiNode; NiNode slot17 target = 0x007B5390; returned pointer is NiAVObject-family. Do NOT silently infer +0x90/+0x94/+0x98 are XYZ until revalidated in this run — that is one of the things this experiment explicitly tests.
- Fallback control: when arg2==NULL or lookup returns NULL, FUN_0050A050 falls back to its own slot1 (returns pointer associated with SF+0x34), then three dwords are copied source+0/+4/+8 -> out+0/+4/+8. Do NOT assume primary-path output has identical coordinate meaning. Test it.

## === PRE-REGISTERED HYPOTHESES (declare before science; do NOT change falsifiers after results) ===

- H1: returned NiAVObject+0x90 is the beginning of a contiguous 3-component world-translation vector. Falsifier: structural layout or accesses show different/noncontiguous semantics.
- H2: FUN_00437F70 materially transfers/transforms a 3-component value from the source at NiAVObject+0x90 into or toward the caller-provided output buffer. Falsifier: decode proves unrelated operation or source/destination interpretation.
- H3: FUN_0082B5A0 participates in finalizing or mutating the primary-path position result. Falsifier: it operates on unrelated state, is observationally unrelated to output, or only performs bookkeeping.
- H4: The output of the primary branch represents the named NiAVObject's world-space position, possibly after a deterministic axis/unit/convention conversion. Falsifier: output is local-space, relative-space, unrelated structure, or source values are not the object's world translation.
- H5: Primary-path and fallback-path outputs share the same structural/coordinate semantic expected by callers of SceneFeeder slot3. Falsifier: caller contexts or helper operations demonstrate different spaces/types.
- NOTE FROM PE-MASTER (adjudication-relevant, not a premise): PE-MASTER's own preliminary hand-decode of the helper entries (kept OUT of the executor's evidence chain on purpose) suggests the helper pair may NOT be a plain copy — the executor must derive everything from bytes and is explicitly NOT required to match any PE-MASTER expectation. Independently derived results that contradict PE-MASTER's first-look are scientifically WELCOME and carry no penalty.

## === STATUS ALGEBRA (keep independent; one CONFIRMED does not imply another) ===

- Status dimensions (assign each, keep separate): SOURCE_OBJECT_IDENTITY / SOURCE_FIELD_IDENTITY / SOURCE_VECTOR_LAYOUT / HELPER_437F70_OPERATION / HELPER_82B5A0_OPERATION / OUTPUT_BUFFER_LAYOUT / OUTPUT_VALUE_RELATION / COORDINATE_SPACE / AXIS_MAPPING / UNIT_SCALE / FINAL_POSITION_SEMANTIC_ROLE.
- Values: CONFIRMED / STRONGLY_SUPPORTED / PLAUSIBLE / UNVERIFIED / REJECTED.
- Additionally: OBSERVED_OPERATION vs FUNCTION_IDENTITY vs FINAL_SEMANTIC_ROLE must be separated for 0x437F70 and 0x82B5A0 (example: if a helper reads 3 floats and writes them unchanged, OBSERVED_OPERATION=CONFIRMED 3xfloat copy; FUNCTION_IDENTITY may remain UNKNOWN; FINAL_ROLE may be strongly supported only from surrounding context).

## === PHASES ===

PHASE A — reconfirm FUN_0050A050 downstream window: independently decode 0x0050A050..0x0050A0AA with capstone (full linear decode + boundary derivation with the terminal+padding rule). Focus 0x0050A064..0x0050A084. Measure: returned lookup object register; NULL branch; exact stack state at every instruction (track pushes/ret-N); identity of original arg1 after push esi (derive the [esp+8] mapping at 0x50A06A — do not inherit); add eax,0x90; push order into 0x437F70 (which pushed value lands at callee [esp+4] vs [esp+8]); return value of 0x437F70; handoff into ECX; call to 0x82B5A0 (its stack-arg positions and their identities); writes or lack of direct writes after helper2; function return value. Produce explicit pseudo-C ONLY AFTER byte decode. Required question: does FUN_0050A050 itself write primary-path XYZ? (Likely answer may be NO — but measure.)

PHASE B — source vector layout: prove or reject NiAVObject+0x90=X, +0x94=Y, +0x98=Z using independent target-local evidence (known transform accesses in NiAVObject methods, UpdateWorldData, transform appliers, vector ops, copy loops, arithmetic on contiguous offsets). Do NOT promote from Gamebryo headers alone (oracles = secondary corroboration only). Required output SOURCE_VECTOR_LAYOUT status + X/Y/Z offsets + structure start + structure extent if known + explicitly distinguish m_kWorld.m_Translate from m_kLocal.m_Translate. Revalidate package B's slot27 (0x007E4820) and slot16 (0x007B4650) pins from bytes if you rely on them.

PHASE C — full decode FUN_00437F70 (primary target): exact extent (terminal+padding rule); calling convention; stack arg count and arg order (MEASURE whether it actually consumes stack args — derive, do not assume); return type shape; every memory read; every memory write; constants; FPU/SSE operations; branches; callees (incl. any allocation thunks — identify them via the project's known thunk conventions or your own IAT/RTTI walk); any SEH frame (handler address, what the handler does — decode it too if reachable); any global slots read/written (record addresses). Then census call sites: minimum channels = direct E8 callers, E9 tail calls if present, whole-file imm32 address-takers, vtable membership if relevant. For each strong call site identify argument shapes (what is at [esp+4]/[esp+8] at the call, what ECX is). Answer: (1) is arg1 destination or source? (2) arg2 dest or source? (3) is it a copy? (4) vector constructor? (5) swaps axes? (6) negates components? (7) scales? (8) normalizes? (9) converts engine/world/render coordinates? (10) what does EAX point to on return? Do not label it VectorCopy merely because it resembles one.

PHASE D — full decode FUN_0082B5A0 (second primary target): exact extent; calling convention; meaning of ECX (derive what it is at the SF slot3 call site AND at other call sites); whether ECX is the 0x437F70 return pointer; object/structure identity if possible (RTTI/vtable walk if a vtable exists; else structural); memory writes; mutations; constants (bit-exact values incl. any f64/f32 constants and their bit patterns + decimal values); FPU operation sequence with EXACT per-component formulas (track the x87 register stack precisely: fld/fmul/fsub/fstp/fxch semantics, temp stores to [esp+N], the f32 narrowing at each store, IEEE-754/x87 extended-precision discipline); downstream callees; return behavior. Census direct and structural call contexts sufficient to classify the operation. Answer: (1) does it mutate the vector? (2) modify an owner object? (3) update cache/dirty state? (4) clamp/validate? (5) transform coordinate system? (6) merely return/commit a temporary? (7) operate on something unrelated to position? Do not infer semantic role from address adjacency.

PHASE E — end-to-end value flow: construct the exact dataflow lookup return EAX -> EAX+0x90 -> 437F70 arg? -> reads [source+?] -> writes [destination+?] -> 437F70 return -> ECX -> 82B5A0 -> possible mutation -> caller output arg1. For each output component out[0]/out[1]/out[2] derive the source expression if possible (strongest form: out.x=source.x etc., or with axis swap/negation/scale/offset — whatever bytes prove). If exact relation cannot be established: UNKNOWN stays UNKNOWN.

PHASE F — caller-side semantic control (BOUNDED): determine whether callers treat the slot3 output as position/direction/rotation/scale/generic float3/temporary vector. Look for downstream uses (world placement, distance, translation matrices, camera, sound position, attachment, rendering). Use: (1) the fallback path in-slot (already-decoded bytes — what does the SAME function write when un-transformed); (2) the prior canon SF+0x34 writer FUN_005094C0 context (value copy from the placement record — cite package PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914 / PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913 findings, DO NOT re-derive beyond a pin check); (3) a bounded set (3-6) of OTHER call sites of the 0x437F70/0x82B5A0 helper pair to see what their outputs feed. Do NOT reopen the 218-candidate ARG2 provenance census. No semantic promotion from one suggestive caller; use multiple independent contexts if possible.

NEGATIVE CONTROL (MANDATORY, at least one): e.g. another call to 0x437F70/0x82B5A0 where the source is provably NOT a world translation; or another 0x82B5A0 call context with a different semantic structure; or another float3 helper with similar byte shape but different operation. Purpose: prevent "looks like float3 copy" -> "therefore world position helper". Required: FAILURE_CASE_DETECTED = YES.

FALLBACK VS PRIMARY COMPARISON: fallback (SF slot1 -> &SF+0x34 -> copy 3 dwords -> out) vs primary (named NiAVObject -> +0x90 -> helpers -> out). Determine: same structure? same coordinate space? same axis order? same out pointer returned? does primary add transformation absent in fallback? Structural equivalence != semantic equivalence.

OPTIONAL CONSTANT/AXIS ANALYSIS: only if helpers contain relevant arithmetic — constants 1.0/-1.0/scale factors/degree-radian/world-unit conversions and component permutations; trace independently; no broad constant archaeology outside these functions.

## === STOP CONDITIONS ===

SUCCESS A: exact primary-path value relation recovered with component-level proof.
SUCCESS B: helper chain performs a deterministic transformation and that transformation is fully recovered.
SUCCESS C: one/both helpers shown NOT to be position-transform helpers and actual downstream operation identified.
SUCCESS D: exact uncertainty localized to one helper/field while the rest of the chain is closed.
Do not continue expanding after meaningful closure.
FAILURE/OPEN: stop honestly if helper boundaries uncertain / aliasing prevents output proof / call graph explodes / structure identity cannot be bounded / component relation remains ambiguous. Return strongest boundary (CONFIRMED/STRONGLY_SUPPORTED/UNVERIFIED). A negative result is valid.
If exact runtime coordinate semantics cannot be proven statically: record RUNTIME_COORDINATE_BEHAVIOR = UNVERIFIED and stop. Do not invent a runtime test (separately human-authorized only).

## === EXPLICITLY OUT OF SCOPE (forbidden) ===

ArkAnimation+0x14, Alpha ret-this cleanup, ARG2 producer provenance, 1433 unresolved thunk candidates, MODEL_RESOURCE_BRIDGE, NIF loader, terrain, placement records (beyond the named bounded pin check), LINK30 P2-1 re-attribution, ABI_PREFIX_R2, Gamebryo generation identification, renderer, Three.js implementation, world reconstruction implementation, network/server, wiki. The 218-candidate ARG2 census stays closed.
P2-1 exposure discipline: historical census rows may depend on the old function-attribution layer — that re-attribution is NOT this run; do not silently fix. If attribution-dependent logic becomes load-bearing for a helper boundary or call-site census, record the dependency and use direct byte-level function-boundary proof (terminal+padding rule) locally.
WORK AUDITOR separation: never read unpublished work-audit results, never merge/modify its branch (`audit/work-audit-reports`, worktrees/WORK_AUDIT_REPORTS).
Forbidden paths (never write): all completed run dirs under docs/audits/ (READ-ONLY input/reference), `docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/` (untracked, pre-existing), `experiments/` (untracked, pre-existing), shared tools/scripts (no changes — that would require pe-toolsmith, NOT authorized here; run-local scripts only), the original client payload locations. No original client payloads in any committed artifact. No `__pycache__`/`.pyc` in the package.

## === EVIDENCE QUALITY ===

Every important PASS must contain: MEASURED_QUANTITY, INDEPENDENT_SOURCE_OF_TRUTH, WHY_NON_CIRCULAR, FAILURE_CASE_DETECTED. Example standards: out.x=world.x must be demonstrated by byte-level def-use, not report prose; helper operation claims need actual reads, actual writes, argument mapping, caller control.

## === REQUIRED PACKAGE ===

`docs/audits/PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915/` (project convention):
- `00_CONTROL/`: RUN_CONTRACT.md (this file), SOURCE_IDENTITIES.json, SCRIPT_SHA256.csv, AMEND_LOG_R1.md (only if corrections occur), scripts/ (run-local scripts only; NO changes to shared tools/scripts/ — that would require pe-toolsmith which is NOT authorized here).
- `01_RAW/`: FUN_0050A050_DOWNSTREAM_DISASM.txt, FUN_00437F70_DISASM.txt, FUN_0082B5A0_DISASM.txt, SOURCE_VECTOR_LAYOUT_RAW.txt, HELPER437F70_CALLER_CENSUS.csv, HELPER82B5A0_CALLER_CENSUS.csv, END_TO_END_VALUE_FLOW_RAW.txt, FALLBACK_PRIMARY_COMPARISON.txt, NEGATIVE_CONTROL_RAW.txt, AT_RUN_START_GIT_OBSERVATION.md, AT_RUN_END_GIT_OBSERVATION.md.
- `02_ANALYSIS/`: SOURCE_VECTOR_LAYOUT.md, HELPER_OPERATIONS.md, OUTPUT_VALUE_RELATION.md, POSITION_SEMANTICS.md, SCIENCE_STATUS_DELTA.csv.
- `03_EVIDENCE/`: README.md, EVIDENCE_INDEX.csv.
- `06_REPORT/`: REPORT.md, HANDOFF.md, STAGE_ACCEPTANCE_GATES.csv, MANIFEST_SHA256.csv.

Note: 00_CONTROL/RUN_CONTRACT.md, 00_CONTROL/SOURCE_IDENTITIES.json and 01_RAW/AT_RUN_START_GIT_OBSERVATION.md (SECTION 1) already exist — created by the formalizer; the executor completes the remainder and APPENDS SECTION 2 to AT_RUN_START_GIT_OBSERVATION.md. QC_AUDIT.md will be added later by the fresh QC step; PE_MASTER_REVIEW.md by the persistence step. No filler. No proprietary binary payload. Raw evidence files must carry generator provenance headers (python version measured at run time, capstone version measured, script name+SHA). MANIFEST_SHA256.csv follows the L12 self-exclusion rule (a manifest cannot contain its own hash).

## === REQUIRED GATES ===

(STAGE_ACCEPTANCE_GATES.csv; honest UNVERIFIED/NOT_DEMONSTRATED are valid outcomes; never fake PASS.)

- G0_SOURCE_IDENTITY — S0 fail-closed: size+SHA256+PE layout match.
- G1_BASE_GIT_STATE — HEAD==BASE_SHA==origin/master at run start; untracked inventory unchanged; no reset.
- G2_SF_DOWNSTREAM_WINDOW — full capstone decode 0x50A050..0x50A0AA; every pin above re-measured with pin-MATCH lines; exact stack state at 0x50A064..0x50A084; push-order -> callee arg mapping for BOTH helper calls; the required question answered with instruction-level def-use; pseudo-C AFTER decode.
- G3_SOURCE_VECTOR_LAYOUT — independent Entropia-local evidence; X/Y/Z offsets + structure start/extent; m_kWorld vs m_kLocal distinguished; status.
- G4_HELPER437F70_OPERATION — extent+ABI+args measured; every read/write; constants; SEH; callee identities; caller census with all channels; the 10 questions answered from bytes.
- G5_HELPER82B5A0_OPERATION — extent+ABI+ECX meaning; bit-exact constants incl. f64 values; EXACT per-component x87 formulas with the register-stack trace; the 7 questions answered from bytes.
- G6_END_TO_END_VALUE_FLOW — per-component dataflow with source expressions; UNKNOWN allowed where unprovable.
- G7_OUTPUT_BUFFER_LAYOUT — out[0/+4/+8] layout proven; return value identity.
- G8_FALLBACK_PRIMARY_EQUIVALENCE — structure/space/axis/out-pointer/transformation-presence all explicitly answered.
- G9_CALLER_SEMANTIC_CONTROL — bounded; >=2 independent context classes; no single-caller promotion.
- G10_NEGATIVE_CONTROL — executed; FAILURE_CASE_DETECTED=YES.
- G11_COORDINATE_SPACE — status.
- G12_AXIS_MAPPING — status.
- G13_UNIT_SCALE — status.
- G14_FINAL_POSITION_ROLE — status.
- G15_FRESH_QC — governance; executed by PE-MASTER after delivery.
- G16_MASTER_ADJUDICATION — governance; PE-MASTER.
- G17_PERSISTENCE — governance; pe-master-auditor path-limited commit+push after G16.

NON-PASS CLASSES (valid, must be recorded as such, never faked): UNVERIFIED / NOT_DEMONSTRATED / NOT_APPLICABLE (with reason) / REJECTED (with evidence) / PENDING (governance gates G15-G17). A gate may record PARTIAL with the exact satisfied/unsatisfied sub-predicates. Faking PASS is a contract violation and a QC P0.

## === TOOL/ENV CONVENTIONS ===

Python: `D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe` (3.12.7); capstone 5.0.7 — measure both at run time and print measured versions in every raw file header (the 1a490ee lesson: never hardcode a version label). Read-only on the EXE. Run-local scripts only in 00_CONTROL/scripts/. Old audit folders READ-ONLY. Ghidra not required; capstone + own PE parse is the expected toolchain.

## === HARD STOPS ===

S0 identity fail; git moved (unknown/conflicting); three-identical-failure ladder exhausted on a required decode; any attempt to modify a forbidden path. On hard stop: persist partial raw evidence + exact resume point + HARD_STOP_REASON.

## === FINAL HANDOFF SCHEMA ===

The executor's return to PE-MASTER must contain: AUDIT_OUTPUT_ROOT / FINAL_REPORT_PATH / PRIMARY_EVIDENCE_PATHS / RUN_STATUS (COMPLETE|PARTIAL|HARD_STOP) / HARD_STOP_REASON / measured gate table summary / the one-line answer to the PRIMARY QUESTION at the highest status the bytes support.

## === FORMALIZER VERIFICATION RECORD (appendix; by pe-master-auditor) ===

Measured by the formalizer 2026-09-15T06:10-06:12 local (-07:00); full values in 00_CONTROL/SOURCE_IDENTITIES.json and 01_RAW/AT_RUN_START_GIT_OBSERVATION.md SECTION 1:
- S0 pre-verification: Entropia.exe size 8015872; SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31; own PE parse (Machine 0x14c i386, PE32 magic 0x10b, ImageBase 0x00400000, 5 sections .text/.rdata/.data/.tls/.rsrc) — ALL MATCH the pinned values. The executor still re-verifies fail-closed (G0).
- Git pre-verification: HEAD == origin/master == ls-remote == 3068f31ad8db7e993a72365dc28cc03066095afd == BASE_SHA; untracked set == exactly the two declared pre-existing paths; worktrees == the three declared. MATCH.
- Output root did NOT exist before formalization (no collision); the package was created fresh by the formalizer.
- Environment pre-check: python 3.12.7; capstone 5.0.7 (cs_version (5, 0, 1280)) — measured at formalize time. The executor re-measures at run time and prints measured versions in every raw file header.
- ACTIVE_WRITER.lock observed: heartbeat 2026-09-07 (stale), scope = an unrelated 99_Audits run dir — disjoint from this run's paths; no takeover performed (single-writer ownership resolves by explicit PE-MASTER dispatch per section 20.7; loop control belongs to PE-MASTER).

FORMALIZER NOT_CHECKED (disclosed boundaries of this formalization):
- The formalizer did NOT decode or re-verify any disassembly pin beyond the S0 identity/PE-layout pin verification ordered by the parent; PE-MASTER stated it independently verified the SF slot3 window bytes at BOOT, and the executor re-measures every pin in-run anyway (G2).
- The formalizer verified boot packages A/B/C by existence + SHA256 identities (+ AUDIT_ENTRYPOINT.md consistency of their headline findings), NOT by full-content re-derivation of their science.
- No numeric executor timebox was declared by the parent at formalize time (recorded under TIMEBOX above); PE-MASTER supplies it at dispatch if one is wanted.
