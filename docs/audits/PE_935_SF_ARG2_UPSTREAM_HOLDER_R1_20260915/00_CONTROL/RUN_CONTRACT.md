# RUN_CONTRACT — PE_935_SF_ARG2_UPSTREAM_HOLDER_R1_20260915

## PROVENANCE HEADER (appended by executor, not part of the verbatim contract body)

- Dispatched by: PE-MASTER (direct bounded dispatch, single run; NO_NESTED_TASKS)
- Executor agent: pe-reconstruction
- Contract received / run started: 2026-09-15T05:25:54Z (executor-local 2026-09-14 22:25:54 Pacific Standard Time)
- Repo: D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean (branch master)
- BASE_SHA (contract-pinned, re-measured at run start): 895bbc8baa2d002c562b7e5b43212e38c2abb16f
- ls-remote origin master at run start: 895bbc8baa2d002c562b7e5b43212e38c2abb16f (EXIT 0)
- Run-local instrumentation (all scripts): 00_CONTROL/scripts/ (this directory)
- The contract body below is persisted VERBATIM as received from PE-MASTER.

---

# BOUNDED CONTRACT — EXECUTE AS pe-reconstruction. NO_NESTED_TASKS. STATIC-ONLY.

You are the executor of ONE bounded run, dispatched directly by PE-MASTER. You may NOT launch any subagent. You create the run package in the working tree and perform the science. You perform ZERO git mutations (no add/commit/push/stash/checkout/reset/branch — persistence is owned later by pe-master-auditor). The client binary is NEVER executed.

## 0. FIRST ACTION

Create `docs/audits/PE_935_SF_ARG2_UPSTREAM_HOLDER_R1_20260915/` and persist THIS CONTRACT VERBATIM as `00_CONTROL/RUN_CONTRACT.md` (append a provenance header: dispatched by PE-MASTER, date, BASE_SHA). Then record `01_RAW/AT_RUN_START_GIT_OBSERVATION.md` (HEAD, branch, origin/master, ls-remote, git status, worktree list, timestamp). Then execute the phases.

## 1. IDENTITY — FAIL CLOSED (G0)

- Executable: `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe`
- PINS: SIZE=8015872; SHA256=E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31; PE32 i386; ImageBase 0x00400000.
- EVERY script you write re-measures size+SHA256+PE layout FIRST and aborts on mismatch. MISMATCH = HARD STOP, report, no analysis.
- Environment (record in every raw artifact header): python `D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe` (3.12.7), capstone 5.0.7. Raw artifacts carry: generator script name + SHA256, python/capstone versions, S0 PASS line. Deterministic generators only. SCRIPT_SHA256.csv lists all scripts + hashes.

## 2. GIT STATE (G1)

- Repo: `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean`, branch master.
- BASE_SHA (PE-MASTER measured 2026-09-14, live == origin == ls-remote): `895bbc8baa2d002c562b7e5b43212e38c2abb16f`.
- PRE-EXISTING dirty inventory (DO NOT TOUCH, DO NOT COMMIT): untracked `docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/` and `experiments/`. Everything tracked is clean.
- You: ZERO git mutations. At run end record `01_RAW/AT_RUN_END_GIT_OBSERVATION.md` and verify the untracked set is exactly: the two pre-existing dirs + your new run dir.

## 3. RUN IDENTITY

RUN_ID: PE_935_SF_ARG2_UPSTREAM_HOLDER_R1_20260915
RUN_CLASS: MATERIAL; RUN_TYPE: STATIC_SEAM_PROBE
MILESTONE: EU935-M1; PRIMARY TARGET: PCG_9_3_5
Parent: PE-MASTER direct dispatch (single bounded run; previous loop 2ed038db is terminal; no auto-loop).

## 4. PRIMARY QUESTION

> WHAT EXACTLY IS THE OBJECT HELD AT `[ArkAnimation-family instance + 0x14]` WHEN FUN_006FAB80 DISPATCHES SLOT 3 — and can we PROVE that this object is a SceneFeederObject / ArkSceneFeeder-compatible receiver? Only after answering that may the run proceed upstream toward the source and value of arg2.

Rosetta edge target: ArkAnimation object → [this+0x14] → receiver identity → slot3 target → SceneFeeder::FUN_0050A050 ? → NiNode::GetObjectByName(arg2). Every `?` must be explicitly resolved or remain UNKNOWN. If [this+0x14] is NOT SceneFeeder, that is EQUALLY valuable: falsify the seam and identify the actual class.

## 5. STANDING KNOWLEDGE — INPUT TO REVALIDATE, NOT AUTOMATIC TRUTH

All expected values below are FAIL-CLOSED PINS: you must re-derive each from the pinned EXE bytes in-run; a mismatch is a recorded finding, never silent adoption; never inherit a label without remeasurement.

- PIN-SF1: SceneFeederObject primary vtable 0x00A7D458 (6 slots: 0..5 = 0x50A460/0x5090A0/0x5090B0/0x50A050/0x5090C0/0x509580); slot-3 dword @0x00A7D464 == 0x0050A050; extent ends at the first non-code dword (the `dPVS` data).
- PIN-SF2: FUN_0050A050 extent 0x0050A050..0x0050A0AA; ABI: thiscall this=ECX; arg1=[esp+4] (out float3 buffer pointer); arg2=[esp+8] (name pointer, NULL-tested); ret 8 at both ret sites (0x50A084, 0x50A0A7).
- PIN-THUNK: FUN_006FAB80 B.5 start 0x006FAB80; expected head bytes: `8B 49 14` / `D9 44 24 04` / `8B 54 24 08` / `8B 01` / `8B 40 0C` / `52` / `51` / `D9 1C 24` / `FF D0` / `C2 08 00` (+ CC padding). Derive the extent by the B.5 iterative terminal+padding rule.
- PIN-FIVE: the five expected extent-verified classes sharing FUN_006FAB80 (from the prior accepted run, post-amendment): `.?AVArkAnimationCyclic@@`, `.?AVArkAnimationCyclicLinear@@`, `.?AVArkAnimationCyclicSin@@`, `.?AVArkAnimationDerivatives@@`, `.?AVArkAnimationPredefined@@`. NOTE: in the prior RTTI map `.?AVArkAnimationCyclic@@` had TWO vtable memberships (0x00A86574 — stored by the class deleting-dtor region @0x006FD2E0 — and 0x00AA7958, UNRESOLVED). Phase B must classify every such case (primary vs secondary/derived-class vtable) — never assume.
- PIN-CTOR: shared base ctor 0x006FABA0 writes `[this+0x14] := param` (expected `89 48 14` mov [eax+0x14],ecx) + refcount increment on the HELD param via edx (`BA 01 00 00 00` / `01 51 04` — re-derive; this is a layout constraint: refcount@held+4). Six expected E8 call sites of this ctor: 0x006FAFC7, 0x006FB092, 0x006FB409, 0x006FB5CD, 0x006FE9E8, 0x006FFA87 (prior run bound-exhausted there — THIS run extends the bound, §7(iv-v)).
- PIN-SFCHAIN: SF factory FUN_005247C0 (SF-ctor call site 0x0052480F); SF ctor FUN_00509330 (vtable store `mov [ebp],0xA7D458` @0x00509366; `operator new(0x118)` via thunk 0x95D3C4); container FUN_0044D590 (+0x10 store @0x0044D680 receives FUN_005247C0 result; its +0x24 is an object pointer — LAYOUT CONFLICT vs the ArkAnimation family's +0x24 float, per the prior run: they are probably DIFFERENT classes — do not assume identity).
- PIN-NN: NiNode vtable 0x00A8CCF4; slot-17 dword @0x00A8CCF4+0x44 == 0x007B5390 (value check ONLY, and ONLY if Phase F triggers).
- PIN-NC: negative-control anchors available for re-derivation (prior run's 5 REJECTED_NOT_SF): method 0x007AC2F0 = vtable slot of `.?AVNiD3DHLSLPixelShader@@`/`.?AVNiD3DPixelShader@@`; method 0x007F1D70 = vtable slot 1 of `.?AVNiBoundingVolume@@`.

## 6. STATUS ALGEBRA (keep SEPARATE at all times)

FUNCTION_IDENTITY / OBSERVED_OPERATION / FINAL_SEMANTIC_ROLE — and additionally: FORWARDER_IDENTITY, HELD_OBJECT_IDENTITY, SLOT3_TARGET_IDENTITY, ARG2_ABI, ARG2_PROVENANCE, ARG2_VALUE_CLASS, ARG2_FINAL_SEMANTIC_ROLE. One CONFIRMED never implies another. Statuses: CONFIRMED / STRONGLY_SUPPORTED / PLAUSIBLE / UNVERIFIED / REJECTED.

## 7. PHASES

### PHASE A — RECONFIRM THUNK (G2)
Independently fully decode FUN_006FAB80 (own capstone; B.5 boundary rule — the E8/E9 lattice MIS-ATTRIBUTES vtable-only functions, prior run: 0x006FAB20 false start; use padding-derived starts). Measure: exact function extent; calling convention; stack args; ret immediate; source of [this+0x14]; exact virtual slot displacement (byte evidence `8B 40 0C` = slot 3); forwarding fidelity of arg1 and arg2. CRITICAL DETAIL: arg1 goes through `fld dword [esp+4]` → `fstp dword [esp]` — an x87 ROUNDTRIP, not a register forward. Classify precisely: what bit-pattern classes survive bit-exact (normal values; denormals — x87 does not flush; pointers as dwords), what does not (signaling-NaN quieting), and what this implies: the receiver's arg1 could be a POINTER (out-buffer, bit-preserved) OR a genuine FLOAT VALUE — this ambiguity itself constrains the receiver's slot-3 signature and is a Phase D/E discriminator (a caller passing `lea` = pointer; a caller passing a float constant = value → receiver slot-3 is NOT FUN_0050A050's out-buffer signature). Also measure: any null/refcount logic, mutation/conversion, alternate branches. Output `FORWARDER_OPERATION_STATUS` ∈ {CONFIRMED, STRONGLY_SUPPORTED, REJECTED}. Raw: `01_RAW/FUN_006FAB80_DISASM.txt`. Do NOT inherit "forwarding thunk" from prior prose — your decode is the evidence.

### PHASE B — FIVE CLASS MEMBERSHIPS (G3)
Re-derive the exact MSVC RTTI names (COL→TypeDescriptor walks; this binary's COLs are POINTER-based VA fields, signature 0 — re-derive, don't inherit). For EACH of the five classes measure: primary vtable VA (resolve any double-membership case: which vtable is the class's primary — the one stored by its ctor/dtor on `this` — and what the other is: secondary vtable of a derived class / other; byte evidence required); valid vtable extent (STANDING ANTI-PATTERN: a vtable starts after its COL pointer and ends at the FIRST entry that is not a valid code target under the declared PE-section criterion — first non-.text dword. If an import/thunk/non-.text executable case exists, document it BEFORE applying the rule globally); slot ordinal containing FUN_006FAB80 (same ordinal in all five? record); constructors (entry VAs; `new` sizes → object size where soundly inferable); destructors; base hierarchy where statically derivable (COL base-class descriptor walk; identify the shared base class — its name, vtable, ctor 0x006FABA0's relationship to it). Deliverable: `01_RAW/ARKANIMATION_VTABLE_MAP.csv` + `02_ANALYSIS/FORWARDER_ANALYSIS.md` (Phase A+B).

### PHASE C — [this+0x14] WRITER CENSUS (G4, G5, G6) — THE HIGHEST-VALUE SUBPROBLEM
Declared scope: the ArkAnimation-family instance lifetime (the five classes + their shared base lineage). Method:
(i) FULL-.text write-instruction census with mem-disp == 0x14 (all write forms/widths; esp/ebp bases = stack-frame writes, EXCLUDED but their count recorded; SIB forms enumerated separately, declared). Denominator = all rows. The prior LINK30 run used exactly this census pattern for disp==0x30 (3643 rows) — reuse the methodology.
(ii) Per-row enclosing-function attribution (B.5 starts) + classification: `FAMILY_CONTEXT_PROVEN` (enclosing function is a family vtable slot function, OR the written base's def provably flows from family construction within the declared bound) / `NON_FAMILY_OUT_OF_SCOPE` (reason per row; +0x14 semantics are NOT assumed shared across unrelated classes — offset ≠ semantics) / `UNKNOWN_CONTEXT`.
(iii) Every FAMILY_CONTEXT_PROVEN writer gets: WRITER_VA, CONTAINING_FUNCTION, VALUE_SOURCE, VALUE_PROVENANCE, WRITE_WIDTH, PATH_PRECONDITION, CLASS/LIFETIME_CONTEXT, writer class (constructor-initialization / setter / copy-ctor / assignment-copy / loader-deserializer / callback-registration / resource-binding / unknown).
(iv) ANCHOR CHAIN — the shared ctor 0x006FABA0: full decode (its own vtable store = which base class? its [this+0x14] write; the held-param refcount@+4 increment; any other held-object field writes). Its six call sites (re-derive the list): at EACH site, EXTENDED backward def-slice of the held-pointer argument — DECLARED BOUND: 4 levels, 384-byte backward decode window per level, multi-start, clobber-aware (the prior run's clobber lesson), INSUFFICIENT_PROOF recorded on exhaustion, never guessed.
(v) UPSTREAM CONTINUATION: for each leaf ctor identified in (iv), census ITS callers (E8; imm32; virtual if vtable-relevant) and at each leaf-ctor call site trace the held-pointer argument within the same bound. This is where a SceneFeeder source would surface (SF factory chain PIN-SFCHAIN) — or a different class (equally valuable: SUCCESS B).
Deliverables: `01_RAW/HOLDER14_WRITER_CENSUS.csv` (all rows + classification), `01_RAW/HOLDER14_WRITER_RAW.txt` (per-writer decode evidence), `02_ANALYSIS/HOLDER14_PROVENANCE.md`.

### RECEIVER IDENTITY PROOF LADDER (G5) — per every source value written into [this+0x14]
LEVEL 0: raw pointer source only. LEVEL 1: source object/vtable observed. LEVEL 2: MSVC RTTI/COL identifies class family. LEVEL 3: exact vtable contains slot-3 target. LEVEL 4: exact slot-3 target == 0x0050A050. ONLY LEVEL 4 (or an equally strong independent identity proof, explicitly argued + byte-evidenced) permits `HELD_RECEIVER = SceneFeederObject CONFIRMED`. If the receiver has a different class/vtable but a compatible slot-3: do NOT call it SceneFeeder — record the ACTUAL class.

### STRONG POSITIVE TEST (G6) — for SceneFeeder linkage
A: a writer stores a pointer whose current vtable is PHYSICALLY 0x00A7D458 (vtable-store byte proof on the source object). B: writer/source construction is directly proven SceneFeederObject by MSVC RTTI/ctor chain AND its vtable slot-3 resolves to 0x0050A050. C: a bounded exact call chain proves the held object originates from known SceneFeeder construction and no replacement occurs before FUN_006FAB80. Anything weaker stays STRONGLY_SUPPORTED / PLAUSIBLE / UNVERIFIED.

### NEGATIVE CONTROL (G7) — MANDATORY
Find at least one object/class that has a compatible slot-3 ABI but is provably NOT SceneFeeder; use it to prove the receiver classifier does NOT simply classify every `[ptr] → vtable → +0x0C` dispatch as SceneFeeder. Re-derive at least one anchor from PIN-NC by your own bytes (do not inherit). Required: `FAILURE_CASE_DETECTED = YES`. Raw: `01_RAW/` negative-control raw.

### PHASE D — CALLERS/DISPATCHERS OF THE THUNK (G8) — only after Phase C has a useful result
FUN_006FAB80 may itself be reached virtually. Four SEPARATE channels (0 E8 ≠ no callers):
- DIRECT_E8_CENSUS: E8/E9/EB to 0x006FAB80 across full .text (denominator = E8 byte occurrences scanned);
- IMM32_ADDRESS_CENSUS: whole-file occurrences of 0x006FAB80 (expected: the five vtable slot dwords + whatever else you find — every hit classified);
- VTABLE_MEMBERSHIP_CENSUS: every vtable/slot containing FUN_006FAB80 (extends Phase B; any membership beyond the five = finding);
- VIRTUAL_DISPATCH_PATTERN_CENSUS: candidate invocations of the SPECIFIC slot ordinal(s) occupied by FUN_006FAB80 — the 2-step `mov f,[vt+K*4]; call f` idiom dominates in this binary. KNOWN TRAP: the prior run's follow-check (call/jmp within ≤3 non-control interstitials) MISSED the thunk's own call site (4 interstitials: push/push/fstp). Use a corrected declared threshold (e.g. ≤6 interstitials within a 64-byte window) AND/OR Method-1-style clobber-aware flow accumulation; declare the bound.
Per candidate classify: PROVEN_TARGET / STRONGLY_SUPPORTED_TARGET / INSUFFICIENT_PROOF / REJECTED_TARGET / NOT_A_VTABLE_CALL, with explicit receiver-provenance rules (receiver proven family instance → PROVEN; unproven receiver → INSUFFICIENT_PROOF).
Raw: `01_RAW/THUNK_CALLER_CENSUS.csv`.

### PHASE E — ARG2 PRODUCER (G9, G10) — for PROVEN or strongest-bounded candidate callers ONLY
Trace how the SECOND forwarded argument is constructed. Source classes to TEST (never assume): string literal / pointer-to-object-name / NIF-scenegraph name / animation channel name / bone name / socket-attachment name / marker name / config key / script-event-supplied name / resource-derived name / dynamically generated buffer. Per producer derive: VALUE_SOURCE, ALLOC/STORAGE_CLASS, ENCODING, NULL_TERMINATION evidence, LIFETIME, ORIGINATING_RESOURCE or STRUCTURE, CALLSITE, VALUE_FLOW to thunk. Do not label semantics from spelling alone.
STRING/NAME EVIDENCE RULE: arg2 proven to point to a C string proves `VALUE_CLASS = STRING` — NOT `SEMANTIC_ROLE = BONE_NAME`. Semantic promotion requires consumer/producer context (e.g. producer taken from a structure field explicitly consumed by skeleton/bone lookup may raise the bone-name hypothesis; a literal "Head" alone is insufficient). G11 (semantic role) MAY legitimately end UNVERIFIED while the run is still successful — do NOT fake PASS to close it.
Also: measure arg1's def at the same call sites (lea → out-buffer pointer; float constant → value) — the Phase A discriminator.
Raw: `01_RAW/ARG2_VALUE_FLOW_RAW.txt`; analysis: `02_ANALYSIS/ARG2_UPSTREAM_ANALYSIS.md`.

### PHASE F — OPTIONAL ONE-LEVEL DOWNSTREAM CROSS-CHECK (G12)
ONLY if you prove [ArkAnimation+0x14] receiver → SceneFeeder slot3 → FUN_0050A050: re-confirm exactly ONE downstream edge: arg2 → SF+0x30 NiNode → slot17, by the single value check dword [0x00A8CCF4+0x44] == 0x007B5390. Do NOT reopen full SLOT17 research. If receiver ≠ SceneFeeder: G12 = NOT_APPLICABLE.

## 8. STOP CONDITIONS

SUCCESS (stop science when ONE is achieved; do not expand endlessly):
- SUCCESS A: [ArkAnimation+0x14] = SceneFeederObject CONFIRMED (Ladder LEVEL 4) + at least one bounded upstream arg2 producer identified.
- SUCCESS B: held receiver class proven NOT SceneFeeder → current seam falsified → actual target class identified.
- SUCCESS C: receiver remains polymorphic/unknown BUT all statically reachable +0x14 writer classes are exhaustively bounded and the exact remaining uncertainty is localized.
- SUCCESS D: one concrete arg2 value class established with full provenance even if final semantic role remains UNKNOWN.
FAILURE/OPEN (stop at the strongest evidence boundary, return UNVERIFIED / NOT_DEMONSTRATED + exact blocker): +0x14 writers use computed aliases outside static reach; receiver replacement cannot be bounded; caller set explodes beyond declared denominator; function attribution becomes uncertain; class hierarchy ambiguous. A bounded negative result is VALID SCIENCE.

## 9. PRE-REGISTERED HYPOTHESES (declare at run start in REPORT; do not change criteria after observing results)

- H1: FUN_006FAB80 forwards two args to slot3 of [this+0x14]. Falsifier: decode shows arg2 mutation or a different slot/receiver path. (Note: arg1 fld/fstp roundtrip is already a known qualification — H1 as stated concerns arg2 verbatim + arg1 bit-preserving roundtrip.)
- H2: [this+0x14] may hold a SceneFeederObject. Falsifier: a writer proves the receiver is another unrelated RTTI class.
- H3: at least one writer/source can prove exact receiver identity. Falsifier: all writers are opaque/computed outside bounded static provenance.
- H4: the forwarded arg2 has a traceable upstream source within a bounded caller window. Falsifier: the caller set is unreachable/exhausts the bound with unresolved defs.
- H5: arg2 semantic role can potentially be narrower than generic string/name. Falsifier: only generic strings with no semantic producer context.

## 10. EVIDENCE QUALITY — every material PASS needs: MEASURED_QUANTITY, INDEPENDENT_SOURCE_OF_TRUTH, WHY_NON_CIRCULAR, FAILURE_CASE_DETECTED.
"5 classes contain the thunk" must include actual vtable entries; "receiver is SceneFeeder" must include actual receiver provenance; "arg2 is string" must include actual pointer source/consumer behavior.

## 11. SCOPE DISCIPLINE

OUT OF SCOPE (no exceptions unless a tiny bounded check is strictly necessary to classify the current edge — then disclose it): P2 downstream world-position consumer (0x437F70/0x82B5A0 flow), P2-1 census-wide re-attribution, ABI_PREFIX_R2, general NiNode vtable, broad Gamebryo generation identification, NIF grammar, terrain, biome generation, renderer implementation, Three.js, world placement implementation, server/network, wiki.
P2-1 LINK30 EXPOSURE: up to ~257 historical REJECTED rows may depend on the old function-attribution layer — NOT this run; do not silently fix. If attribution-dependent classification logic contaminates a load-bearing helper: record the dependency and use direct byte-level function-boundary proof locally (B.5 starts).
WORK-AUDITOR SEPARATION: the branch `audit/work-audit-reports` and its worktree are an independent auditor workspace. Do NOT merge, cherry-pick, use as evidence, modify, or coordinate with it. Canonical master + physical evidence only.
ORACLE RULE: Entropia.exe physical bytes are the primary truth. Gamebryo oracles = secondary semantic controls only. NEVER use oracle similarity to prove [ArkAnimation+0x14] = SceneFeeder — the target-local proof must come from Entropia.

## 12. FORBIDDEN PATHS (READ-ONLY or NEVER)

All completed run dirs under docs/audits/ = READ-ONLY input/reference. `docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/` (untracked, pre-existing) = DO NOT TOUCH. `experiments/` = DO NOT TOUCH. `audit/work-audit-reports` = NEVER. Shared tools/scripts = no changes; run-local instrumentation lives ONLY in your new `00_CONTROL/`. No original client payloads in any committed artifact. No `__pycache__`/`.pyc` in the package.

## 13. PACKAGE (project conventions)

`docs/audits/PE_935_SF_ARG2_UPSTREAM_HOLDER_R1_20260915/`:
- `00_CONTROL/`: RUN_CONTRACT.md (this contract verbatim), SOURCE_IDENTITIES.json, SCRIPT_SHA256.csv, AMEND_LOG_R*.md (only if corrections happen)
- `01_RAW/`: FUN_006FAB80_DISASM.txt, ARKANIMATION_VTABLE_MAP.csv, HOLDER14_WRITER_CENSUS.csv, HOLDER14_WRITER_RAW.txt, THUNK_CALLER_CENSUS.csv, ARG2_VALUE_FLOW_RAW.txt, RTTI/COL raw, negative-control raw, AT_RUN_START/END_GIT_OBSERVATION.md, IDENTITY_VERIFICATION.txt (+ any additional raws your phases need)
- `02_ANALYSIS/`: FORWARDER_ANALYSIS.md, HOLDER14_PROVENANCE.md, RECEIVER_IDENTITY.md, ARG2_UPSTREAM_ANALYSIS.md, SCIENCE_STATUS_DELTA.csv
- `03_EVIDENCE/`: README.md, EVIDENCE_INDEX.csv
- `06_REPORT/`: REPORT.md, HANDOFF.md, STAGE_ACCEPTANCE_GATES.csv, MANIFEST_SHA256.csv (L12 self-exclusion rule: a manifest cannot contain its own hash)
QC_AUDIT.md will be added later by the fresh QC session; PE_MASTER_REVIEW.md by the persistence step. No filler artifacts.

## 14. GATES (self-assess in STAGE_ACCEPTANCE_GATES.csv; G13/G14/G15 = PENDING, owned by others)

- G0_SOURCE_IDENTITY: PASS iff own re-measure == pins; fail-closed.
- G1_BASE_GIT_STATE: PASS iff start HEAD==895bbc8==origin==ls-remote + dirty inventory recorded + zero mutations during the run.
- G2_FORWARDER_OPERATION: PASS iff Phase A decode complete with extent+ABI+forwarding semantics measured and FORWARDER_OPERATION_STATUS assigned with raw evidence.
- G3_ARKANIMATION_CLASS_MEMBERSHIP: PASS iff exact RTTI names re-derived (or corrected count with reason), each class: primary vtable VA + valid extent (anti-overrun rule applied + any exception documented) + slot ordinal of FUN_006FAB80 + ctor/dtor + base hierarchy where derivable.
- G4_HOLDER14_WRITER_CENSUS: PASS iff the declared full-.text census denominator is recorded, every row classified, every FAMILY_CONTEXT_PROVEN writer carries the full writer fields, no silent drops.
- G5_RECEIVER_PROVENANCE: PASS iff every writer's value source is dispositioned on the LEVEL 0-4 ladder with explicit level assignment.
- G6_SCENEFEEDER_IDENTITY_TEST: PASS iff the strong-positive test (A/B/C) is executed for every candidate and the outcome recorded; CONFIRMED only on LEVEL 4 or equally strong independent proof.
- G7_NEGATIVE_RECEIVER_CONTROL: PASS iff ≥1 compatible-ABI non-SceneFeeder class demonstrated from own bytes and FAILURE_CASE_DETECTED=YES.
- G8_THUNK_CALLER_CENSUS: PASS iff all four channels censused with denominators + per-candidate classification.
- G9_ARG2_PRODUCER_FLOW: PASS iff every PROVEN/strongest-bounded caller's arg2 traced or honestly recorded INSUFFICIENT_PROOF/bound-exhausted; NOT_APPLICABLE if no such caller exists.
- G10_ARG2_VALUE_CLASS: PASS iff every identified value carries the full producer fields; STRING only on C-string evidence; honest NOT_DEMONSTRATED otherwise.
- G11_ARG2_SEMANTIC_ROLE: PASS iff the assignment follows the string/name evidence rule; outcome UNVERIFIED is a VALID gate outcome.
- G12_DOWNSTREAM_CONTINUITY: NOT_APPLICABLE unless receiver==SceneFeeder proven; if proven: PASS iff the single value check made.
- G13_FRESH_QC / G14_MASTER_ADJUDICATION / G15_PERSISTENCE: PENDING (owned by QC session / PE-MASTER / pe-master-auditor).

## 15. HARD STOPS

EXE identity mismatch; unknown/conflicting commit on master; any need to modify a forbidden path; scope explosion beyond the declared denominators; static-reach failure per §8. On hard stop: record exact state + blocker in REPORT + HANDOFF, set RUN_STATUS accordingly.

## 16. FINAL ANSWER (delivery notice to PE-MASTER)

Return a compact notice: what was executed, phase statuses, the headline outcomes (FORWARDER_OPERATION_STATUS; five-class membership result incl. slot ordinals + any corrected count; writer census denominators + FAMILY_CONTEXT_PROVEN count; HELD_OBJECT_IDENTITY + ladder level; SCENEFEEDER_LINK status; THUNK_CALLERS census outcome; ARG2_PROVENANCE / ARG2_VALUE_CLASS / ARG2_SEMANTIC_ROLE statuses; DOWNSTREAM_CONTINUITY; TOP_NEW_DISCOVERY; TOP_FALSIFIED_HYPOTHESIS; TOP_OPEN_BLOCKER; gates self-assessment; P0-P3 findings), package paths, RUN_STATUS ∈ {PROPOSAL_READY, BOUND_EXHAUSTED, HARD_STOP}, HARD_STOP_REASON. The REPORT.md must contain all raw fields for these headline outcomes with per-claim evidence pointers. UNKNOWN stays UNKNOWN — WORKS != UNDERSTOOD. Do not promote any status without direct byte evidence.
