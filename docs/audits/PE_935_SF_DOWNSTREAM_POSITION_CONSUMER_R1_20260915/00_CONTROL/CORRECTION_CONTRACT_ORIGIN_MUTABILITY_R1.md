RUN: PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915
RUN_CLASS: MATERIAL | RUN_TYPE: SCIENCE_CORRECTION_REVALIDATION | MILESTONE: EU935-M1 | TARGET: PCG_9_3_5
Executor: pe-reconstruction. Direct PE-MASTER dispatch. NO_NESTED_TASKS (you cannot launch agents; return to PE-MASTER when done or blocked). STATIC-ONLY — the client is NEVER executed. You are the EXECUTOR of a human-authorized bounded correction of an ALREADY-PUBLISHED canonical package.

=======================================================================
SECTION 0 — WHAT THIS RUN IS AND IS NOT
=======================================================================
Target canonical run being corrected: PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915.
Expected canonical BASE at start: 8a09e459eb5a930054f35b713afe3e28b6fa5abc.
This correction DOES NOT create a new package directory. ALL correction artifacts land INSIDE the existing canonical package:
  docs/audits/PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915/   (repo: D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean)
  - new raw evidence -> 01_RAW/
  - new analysis -> 02_ANALYSIS/
  - evidence/index updates -> 03_EVIDENCE/
  - fresh QC + superseding review -> 06_REPORT/ (QC file is written by a LATER fresh-QC session, NOT by you; the superseding review is written by PE-MASTER, NOT by you)
  - correction scripts -> 00_CONTROL/scripts/
  - amendment history -> APPEND to existing 00_CONTROL/AMEND_LOG_R1.md (continue numbering at AMEND-14; never rewrite AMEND-1..13)
The correction RUN_ID PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915 is provenance metadata in headers/AMEND-14+ entries only.
It MUST NOT create docs/audits/PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915/ or any other new package root.
This run exists ONLY to revalidate and correct: origin singleton S mutability -> origin setter -> output formula status -> affected canonical prose/gates/evidence.
DO NOT START (forbidden): placement-space probe, MODEL_RESOURCE_BRIDGE, another SceneFeeder science seam, ARG2 provenance, terrain, NIF, ArkAnimation, runtime execution, renderer implementation, semantic naming of S (do NOT call S world origin / floating origin / camera origin / region origin / sector origin / cell origin), AUTO LOOP, any next science question.
Do NOT touch: D:\TESTAI\.opencode\skills\... or any external PE-MASTER/WORK-AUDITOR skill/trap-library tree (out of scope; separate human decision).
Do NOT modify AUDIT_ENTRYPOINT.md (that happens only in the LATER PE-MASTER-ordered persistence pass, not in this executor run).
You do NOT commit and do NOT push (persistence happens only after fresh QC + PE-MASTER adjudication, as a separate ordered pass).

=======================================================================
SECTION 1 — LIVE GIT FAIL-CLOSED (BEFORE ANY MUTATION; PERSIST TO A NEW 01_RAW OBSERVATION FILE)
=======================================================================
Repo: D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean
Expected HEAD: 8a09e459eb5a930054f35b713afe3e28b6fa5abc.
Before ANY mutation measure and persist (into a NEW file 01_RAW/CORRECTION_RUN_GIT_OBSERVATION.md): branch, HEAD, origin/master, git ls-remote origin master, git status --short, git worktree list, complete pre-existing untracked inventory.
Historically expected pre-existing untracked set: docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/ and experiments/. LIVE DISK > prompt: if untracked inventory differs, record and adjudicate before mutation. Do NOT clean or sweep pre-existing untracked paths. If HEAD moved: DO NOT reset; inspect all intervening commits and FAIL CLOSED on conflict (stop and return to PE-MASTER).
No work-audit branch/worktree may be read as canonical evidence, modified, merged or cherry-picked (worktrees incl. WORK_AUDIT_REPORTS are forbidden reference).
ZERO git mutations by you: no commit, no push, no branch, no stage. (Only file work inside the package.)

=======================================================================
SECTION 2 — PRIMARY PHYSICAL SOURCE (EVERY SCRIPT FAIL-CLOSED)
=======================================================================
Use: D:\Eudoria_Reconstruction\pcg_install\Entropia.exe
Pinned: SIZE 8015872, SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31, PE32 i386, ImageBase 0x00400000.
Every new measurement script MUST independently fail-closed verify source size, SHA256, PE architecture/layout before decoding. STATIC ONLY — never execute the client.

=======================================================================
SECTION 3 — THE FINDING TO INDEPENDENTLY REPRODUCE (FIRST, BEFORE EDITING ANYTHING)
=======================================================================
External WORK AUDITOR reports (INPUT, NOT TRUTH — reproduce or reject every item from physical bytes):
(a) At direct caller 0x00458E27 -> call FUN_00437F70, additional writes exist:
    0x00458E30  mov [eax],edx / 0x00458E36  mov [eax+4],ecx / 0x00458E3D  mov [eax+8],edx
    where EAX retains the pointer S returned by FUN_00437F70.
(b) The function STARTING at 0x00458D90 contains call site 0x00458E27 and behaves as a setter of S.
The published package states (now challenged): "No caller writes through the returned pointer within 8 instructions (measured over all 99 sites)" and "S == {0,0,0} permanently".
FIRST FALSIFIER (before ANY canonical edit): decode the function starting at 0x00458D90 and the path through 0x00458E27. Prove register state immediately after return from call 0x437F70. Required output field:
    EAX_PROVENANCE_AT_0x458E2C = FUN_00437F70_RETURN / OTHER / UNVERIFIED
Then prove or reject writes through the returned pointer: check [eax], [eax+4], [eax+8] and aliases carrying the same S pointer.
If ONE valid writer through a register proven to contain S exists:
    NO_WRITE_THROUGH_99_CALLERS = REJECTED; ORIGIN_PERMANENT_ZERO = REOPENED; NEGATIVE_CONTROL_4 = FALSIFIED.
One correct counterexample is sufficient. Do not edit canonical science before this falsifier is independently reproduced by YOUR OWN deterministic script.
PE-MASTER has ALREADY independently reproduced the falsifier from physical bytes (AUDITOR_COUNTERCHECK, capstone). Your scripts must reproduce it independently; the following are PE-MASTER cross-check anchors — RE-DERIVE them, do NOT inherit (they are expectations to verify, and your measured values must come from your own decode; report any discrepancy loudly instead of forcing a match):
  - Setter extent 0x00458D90..0x00458E43 (ret @0x00458E43; add esp,0x10 @0x00458E40; int3 padding 0x00458E44..0x00458E4F; next function starts 0x00458E50).
  - Setter shape: sub esp,0x10; read [ecx]/[ecx+4]/[ecx+8] (three int32); neg each; fild+fstp int->float conversion into a local 3xf32 array; a 13-call chain (0x415270 get-or-create singleton [0xba12d4] plain ret; then mov ecx,eax; call 0x6a7b50/0x4147f0/0x44c980/0x401360/0x485050/0x746550/0x524330/0x401360/0x6b22f0/0x7ce1e0/0x8dc540/0x930040); call 0x437F70 @0x458E27; then three writes through EAX: 0x458E30 mov [eax],edx / 0x458E36 mov [eax+4],ecx / 0x458E3D mov [eax+8],edx; add esp,0x10; ret.
  - Stack-discipline OBLIGATION: prove from the setter's own ABI which stack slots the three written values come from. PE-MASTER derived: 4 pushed args must all be consumed by the chain (each arg-popping callee ret 4) so that esp at 0x458E2C..0x458E3D equals the local-frame base, hence the written values are exactly the f32(-int32) triple. VERIFY this: decode the ret convention of every chain member (0x6a7b50, 0x4147f0, 0x44c980, 0x401360, 0x485050, 0x746550, 0x524330, 0x6b22f0, 0x7ce1e0, 0x8dc540, 0x930040, 0x415270) and account for every push (0x458DB8, 0x458DD5, 0x458DE6, 0x458E05) and every pop; document the esp ledger instruction-by-instruction. If your esp ledger contradicts PE-MASTER's derivation, report it loudly — do not paper over.
  - Getter: FUN_00437F70 returns the singleton pointer in EAX (fast path mov eax,[0xba1804]; test; jne 0x437fd7 -> epilogue ret; cold path operator new(12)+ctor 0x82B580, stores [0xba1804], plain ret). Extent 0x437F70..0x437FE7.
=======================================================================
SECTION 4 — REAL WRITE-THROUGH CENSUS (PROVENANCE-AWARE; DO NOT REPRODUCE THE ORIGINAL DEFECT)
=======================================================================
Deterministic census over ALL direct E8 callers of FUN_00437F70. Re-MEASURE the denominator (historically 99 — do not assume).
PRE-REGISTER before measurement: WRITE_THROUGH_WINDOW_N = 16 (primary census) AND a separate historical view N = 8 (because the falsified canonical statement claimed an 8-instruction measurement). Do NOT change N after seeing results. If N=16 does not resolve a site, classify the residual honestly (INSUFFICIENT_PROOF_*); never selectively extend only suspicious rows and present it as one uniform census.
PROVENANCE RULES:
- At every call 0x437F70 the returned value becomes symbolic S_PTR. Track S_PTR across register copies (mov ecx,eax / mov edi,eax / mov esi,ecx etc. preserve provenance; multiple live aliases simultaneously). THIS PATTERN MUST NOT BE MISSED: mov ecx,eax; mov eax,0; mov [ecx],edx (overwriting EAX does not invalidate S_PTR living in ECX). Stop only when S_PTR provenance is fully lost for all known aliases.
- Stack spill/reload: if S_PTR is stored to stack/memory and later provenance cannot be proven within the declared bound -> INSUFFICIENT_PROOF_STACK_ESCAPE (NOT NO_WRITE). If a stack reload is unambiguously tied to the same spill, provenance may continue; record the derivation.
- Pointer escape channel: if S_PTR is pushed as argument / stored to another object / stored to global state / passed through a call / otherwise escapes local registers — record the escape explicitly. For direct bounded callee analysis inspect a deterministic CALLEE-HEAD WINDOW of 0x40..0xA0 bytes; use enough of that fixed head bound to classify: READ_ONLY / WRITE_THROUGH / FORWARDED / NOT_USED_IN_CHECKED_HEAD / INSUFFICIENT_PROOF_HEAD_BOUND. Follow the same disclosure discipline as the historical triple address-taker census (including the 0x4CE5B0 style: "no write found in bounded head; deeper consumer unresolved"). Do NOT turn head-bounded absence into global absence.
- Use DECODED instruction streams (capstone linear decode from function starts for context windows; every census E8 hit must be verified as a real instruction boundary — no raw-byte false positives).
ROW SCHEMA (machine-readable, one row per call site; a site with multiple write events carries them all in per-event fields or sub-rows — document your encoding):
  call_site_va; enclosing_function_start (if proven, with the extent proof rule); WINDOW_N; decoded instruction window; S_PTR provenance transitions; all live aliases; pointer escape events; write address expression; write offset relative to S; write source/value provenance if recoverable; final disposition.
DISPOSITION TAXONOMY (use exactly these classes; you may add documented multi-write encoding, e.g. a site classified WRITE_S_PLUS_0 carrying offsets {0,4,8}):
  NO_WRITE_WITHIN_BOUND; WRITE_S_PLUS_0; WRITE_S_PLUS_4; WRITE_S_PLUS_8; WRITE_S_OTHER_OFFSET; S_PTR_ESCAPED_READ_ONLY; S_PTR_ESCAPED_WRITE; S_PTR_ESCAPED_UNRESOLVED; INSUFFICIENT_PROOF_STACK_ESCAPE; INSUFFICIENT_PROOF_HEAD_BOUND; S_PROVENANCE_LOST; CONTROL_FLOW_ESCAPE; INSUFFICIENT_PROOF.
REQUIRED: denominator/denominator rows classified (every row counted, statuses summed mechanically). Unresolved rows MUST remain unresolved.
OUTPUT: 01_RAW/ORIGIN_SINGLETON_WRITE_THROUGH_CENSUS.csv (rows) + 01_RAW/ORIGIN_SINGLETON_WRITE_THROUGH_RAW.txt (method, windows, ledger, per-site windows, aggregate derivation).
The KNOWN writer site 0x00458E27 must fall out of YOUR census with its three write events (offsets 0/4/8) — if it does not, your instrument is defective: fix the instrument, not the data.

=======================================================================
SECTION 5 — SETTER FUNCTION ANALYSIS (EXACT TARGET 0x00458D90)
=======================================================================
Analyze the function STARTING at 0x00458D90 (the call 0x00458E27 is inside it). Determine (all from your own decode):
- exact function extent (terminal+padding rule; prove the boundary bytes);
- calling convention (PE-MASTER expectation: thiscall-style ECX input, no stack args, plain ret; returns with EAX=S incidentally — verify);
- inputs (PE-MASTER expectation: pointer to a 12-byte triple of three INT32 at [ecx+0/4/8] — verify; the caller FUN_00458E50 produces the triple via three fld+call 0x95da40 f32->int32 conversions (0x95da40 = ftol-style helper — verify its operation class from bytes, bounded head) after fetching floats; the delta-condition at 0x458EE2 (sum of squared int32 deltas == 0 -> skip setter) and the store of the new triple into [esi+0/4/8] at 0x458EE8..0x458EEF precede the call — decode and document FUN_00458E50's flow including what 0x458c40 produces);
- register provenance and control-flow paths;
- the call to 0x437F70 and the exact S writes: all three components, arithmetic before each write (neg + fild int->float), write offsets 0/4/8 relative to S;
- the 13-call chain ABI (esp ledger per Section 3; which callee consumes which pushed arg; identify the chain members' singleton slots e.g. 0x415270 -> [0xba12d4] — bounded head classification only, no deep dive);
- input data types; output/return behavior.
If exact expressions can be recovered, report:
  S.x = ... ; S.y = ... ; S.z = ...   (PE-MASTER expectation: S[i] = f32(-(int32)in[i]) — verify by your own esp ledger).
Separate explicitly: ORIGIN_SETTER_OPERATION / ORIGIN_SETTER_INPUT_TYPE / ORIGIN_SETTER_FINAL_SEMANTIC_ROLE (= UNVERIFIED; do NOT assign a semantic name to S).
OUTPUT: 01_RAW/ORIGIN_SETTER_458D90_DISASM.txt (full decode + ABI + esp ledger + formulas).

=======================================================================
SECTION 6 — STATIC REACHABILITY — BOTH CALLER BRANCHES (RE-DERIVE; DO NOT INHERIT)
=======================================================================
External audit reports Branch A (claimed reachable): 0x458D90 <- 0x458E50 <- 0x416FD0 <- 0x417880 <- 0x514EF0 (virtual method; reported vtable ~0x00A7D764, entry 0x00A7D778, slot 5, COL ~0x00AA1304). And Branch B (claimed dead): 0x458D90 <- 0x417A40 <- 0x4B1B70 with 0x4B1B70 having only a self-recursive E8 edge near 0x4B1F2C and zero external imm32/address-taker channel.
DO NOT inherit these identities. Re-derive with your own decoded censuses (E8/E9 + whole-image imm32 + vtable membership): function boundaries (extent proofs), the call edges, vtable start, slot ordinal, COL, RTTI, class/object identity where possible.
PE-MASTER cross-check anchors (RE-DERIVE, report discrepancies loudly):
  - 0x458D90 sole direct E8 caller: 0x458EF2 (inside FUN_00458E50).
  - 0x458E50 sole direct E8 caller: 0x4171BA — which is inside the function STARTING 0x00417030 (NOT inside FUN_00416FD0: FUN_00416FD0's extent ends at ret 0xc @0x0041702D + int3 0x41702F; the next function starts 0x417030 — the external auditor's chain attribution "0x458E50 <- 0x416FD0" is a MISATTRIBUTION of function boundaries).
  - FUN_00417030 sole direct E8 caller: 0x40296F — inside FUN_00402910 = the MAIN MESSAGE LOOP (prior canon: boot chain RUN 0x4055f0 -> ... -> message loop 0x402910; verify the loop structure from bytes: the loop head, the 0x417030 tick call, the test bl,bl / jne back-edge — the tick's AL return feeds the loop-continue condition). Decode the exact branch conditions guarding the tick call and the guarded sub-path leading to 0x4171BA (PE-MASTER expectation: at 0x4171A5 je 0x417216 skips; the guard is 0x4143f0-singleton -> 0x42bc20(this)->test al,al; the call at 0x4171B3/0x4171B8 chain: 0x414970 -> ecx -> call 0x458e50 — verify).
  - The reported subtree 0x514EF0 (vtable 0x00A7D764 slot 5 @0xA7D778; COL 0x00AA1304 -> TD 0x00B78F74 -> .?AVArkClientPlayerImpl@@) -> E8@0x5159E5 -> 0x417880 -> E8@0x417972 -> 0x416FD0: REAL EDGES, but this subtree NEVER reaches the setter (0x416FD0 is an init/registration helper whose [esi]=0xA7A244 store points to a DATA DESCRIPTOR, not a vtable: 0xA7A240=0x004B3CC0 is a .text address, 0xA7A244={0x00416AD0,0x005B8B80} followed by string data "Parameters\DisplaySettings\Audio..." — verify all of this; the class-name identity of vtable 0xA7D764 is real but IMATERIAL to the setter chain).
  - Branch B: 0x417A40 <- E8@0x4B1EEB (inside FUN_004B1B70); 0x417A40 -> E8@0x417B11 -> 0x417880 (again NOT reaching the setter). 0x4B1B70: verify the self-recursive E8 @0x4B1F2C is a real instruction (decode from 0x4B1B70 start through that address); census its channels (E8/E9/imm32/vtable). PE-MASTER raw-scan expectation: only the self-edge, zero imm32. If evidence supports it: BRANCH_B = STATICALLY_DEAD_WITHIN_MEASURED_CHANNELS — BUT ALSO state explicitly that this subtree does not reach the setter at all, so its deadness is immaterial to origin mutability.
REPORT BOTH BRANCHES even if one is dead; explicitly separate ORIGIN_SETTER_STATIC_REACHABILITY (the TRUE chain: message loop FUN_00402910 -> 0x417030 tick -> guarded -> 0x458E50 -> delta-conditioned -> 0x458D90) from ORIGIN_SETTER_RUNTIME_EXECUTION. Static reachability does NOT prove runtime execution. Without runtime evidence: ORIGIN_SETTER_RUNTIME_EXECUTION = UNVERIFIED.
OUTPUT: 01_RAW/ORIGIN_SETTER_CALLER_CENSUS.csv (edges, extents, channels) + 01_RAW/ORIGIN_SETTER_REACHABILITY_RAW.txt (the two reported branches re-derived + the true chain + all boundary proofs + the external-audit misattribution corrections, each with bytes).

=======================================================================
SECTION 7 — GENERATOR DEFECT REPAIR — REMOVE HARDCODED SCIENCE
=======================================================================
Audit 00_CONTROL/scripts/gen_raw_evidence.py and EVERY touched generator (census_triple_writes.py, gen_manifest.py). The defect is broader than one false sentence. Current generators contain hardcoded scientific conclusions equivalent to: "S == {0,0,0} at ALL times", "never mutated", "No caller writes through ... measured over all 99 sites" (gen_raw_evidence.py line ~277 — a FABRICATED measurement claim: no measurement produced it; the classifier only looked at 2 instructions after the call and keyed on the first instruction's pattern), "global-zero-vector snapshot", unconditional simplified W*0.01f language (e.g. FUN_0082B5A0_DISASM output "With S == {0,0,0} (Phase C)... out[i] = f32(src[i]*0.01f)"), census_triple_writes.py [T.10] "=> THE ORIGIN TRIPLE ... IS NEVER WRITTEN ... => S == {0,0,0} for the whole process lifetime, immutable after construction" (the SECOND arrow is an invalid inference: writes through the returned singleton pointer do not write the triple addresses) and the fabricated coverage "covered for 99 sites by the HELPER437F70 census" (~line 831 — the census never analyzed write-through at all).
RULES:
  GENERATORS MAY EMIT MEASUREMENTS. GENERATORS MUST NOT HARDCODE SCIENCE CONCLUSIONS.
  A conclusion like "writers = 0" may be mechanically aggregated from rows. A conclusion like "therefore runtime origin is permanently zero" belongs in analysis/status, not generator prose.
  Preferred pipeline: physical bytes -> raw measurement -> machine-readable rows -> derived aggregates -> analysis/status.
  Forbidden: generator -> prewritten desired scientific conclusion.
Repair plan (bounded):
  - gen_raw_evidence.py: remove/replace the hardcoded conclusion lines ([C.7]/[C.9](10) "at ALL times"/"entire process lifetime"; [C.10] summary "No caller writes ... => singleton never mutated"; [A.6]/pseudo-C "global-zero-vector snapshot"; any equivalent) with measurement-only text + pointers to the analysis layer; regenerate the affected raw files (FUN_00437F70_DISASM.txt, FUN_0050A050_DOWNSTREAM_DISASM.txt, FUN_0082B5A0_DISASM.txt, HELPER437F70_CALLER_CENSUS.csv, HELPER82B5A0_CALLER_CENSUS.*, SOURCE_VECTOR_LAYOUT_RAW.txt as needed) — the measurement content must come out byte-stable vs the current files except the corrected prose (verify with diffs vs PRE_EDIT_R2 snapshots; a regenerated GENERATED_UTC header changing is acceptable and must be disclosed).
  - census_triple_writes.py: [T.10] must stop at the measurement ("triple never written within the enumerated channels; residuals disclosed") and MUST NOT emit "=> S immutable/whole process lifetime"; remove the fabricated "covered ... by the HELPER437F70 census" residual wording; the [T.1]-[T.9] measurement logic stays untouched. Amend 01_RAW/ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt's [T.10]+residuals accordingly (regeneration or bounded edit — your choice, documented in AMEND; measurement sections byte-stable, verified).
  - gen_manifest.py: update role-map descriptions that carry the stale conclusions ("immutable", "{0,0,0}") to neutral provenance text.
  - The ORIGIN_TRIPLE census measurement ITSELF SURVIVES (the triple 0xBA921C/20/24 write-census remains a valid measurement; PE-MASTER independently recounted 268 = 107+81+80 whole-file imm32 occurrences MATCH) — what dies is only the "=> S permanently zero" inference and the fabricated write-through coverage claim.
Persist two standing lessons IN-REPO (existing standing-rules/correction-ledger mechanism if one exists inside the authorized persistence scope — check the repo for an existing correction-ledger file used by prior runs; if none exists within scope, record them in the package AMEND_LOG as named lessons; do NOT edit external skill trees):
  LESSON 1: CLAIM_OF_MEASUREMENT_REQUIRES_MEASUREMENT_ARTIFACT
  LESSON 2: ROW_INTEGRITY_DOES_NOT_VALIDATE_INFERENCE (a byte-correct CSV does not imply the interpretation of that CSV is correct)

=======================================================================
SECTION 8 — STATUS ALGEBRA (DO NOT OVERCORRECT; PRESERVE CORRECT SCIENCE)
=======================================================================
Independently derive final statuses. Expected shape IF the writer is reproduced (derive, do not copy):
  ORIGIN_INITIAL_ZERO = CONFIRMED        (zero-init .data virtual tail + ctor copies the never-written triple -> S starts {0,0,0}; re-derive from your own bytes + the surviving census)
  ORIGIN_MUTATION_CHANNEL_EXISTS = CONFIRMED  (the setter writes S through the getter's return)
  ORIGIN_MUTATED_AT_RUNTIME = UNVERIFIED (no runtime execution; STATIC-ONLY)
  ORIGIN_PERMANENT_ZERO = REJECTED       (as previously claimed)
  ORIGIN_RUNTIME_VALUE = UNVERIFIED
Do NOT use generic "ORIGIN_MUTABLE" as a substitute for runtime execution.
Byte-level conversion formula revalidated independently (PE-MASTER already re-decoded 0x82B5A0 from bytes: out[i] = f32(f32(W[i]*(double)(float)0.01) - S[i]), K bits 0x3F847AE140000000, ret 8 — re-derive yourself):
  OUTPUT_GENERAL_FORMULA = CONFIRMED: out[i] = f32( f32(W[i] * (double)(float)0.01) - S[i] )
  OUTPUT_ZERO_ORIGIN_SPECIAL_CASE = CONFIRMED CONDITIONALLY: IF S == {0,0,0} THEN out = f32(W * 0.01) (bit-exact; sign-of-zero caveat)
  OUTPUT_ALWAYS_W_TIMES_0_01 = REJECTED (as an unconditional claim)
  PRIMARY_ALWAYS_100X_SMALLER = REJECTED (as an unconditional claim)
  NUMERIC_SCALE_FACTOR = CONFIRMED (if bytes still prove K — they do; re-verify)
  CM_TO_M = PLAUSIBLE (unless independently upgraded — do not upgrade it)
OUTPUT: 02_ANALYSIS/ORIGIN_STATUS_CORRECTION.md (canonical naming equivalent allowed) — the corrected status algebra with per-status measured quantity, evidence pointer, why_non_circular, and failure case.

=======================================================================
SECTION 9 — NEGATIVE CONTROL #4 SUPERSESSION
=======================================================================
Published NEGATIVE_CONTROL_RAW.txt Control 4 effectively states: "dynamic origin rejected because no writer exists" (premise: "all 99 call sites ... measured"). The premise is FALSE (the write-through was never measured; counterexample 0x00458E27).
Mark: NEGATIVE_CONTROL_4 = FALSIFIED_BY_COUNTEREXAMPLE.
Preserve the historical negative-control result — do NOT rewrite it as though it never occurred. In NEGATIVE_CONTROL_RAW.txt APPEND a CONTROL 4 SUPERSESSION block (append-style; original text preserved byte-identical above it) explicitly recording: original premise; original claimed result; counterexample (mandatory failure case: 0x00458E27 plus the exact S-write instructions 0x458E30/0x458E36/0x458E3D); why the original control failed (the "measured" write-through never had a measurement artifact; the census instrument recorded instruction_after_next="mov dword ptr [eax], edx" for this very site but its classifier never interpreted write-through); resulting status correction (ORIGIN_PERMANENT_ZERO REJECTED; ORIGIN_MUTATION_CHANNEL_EXISTS CONFIRMED; ORIGIN_MUTATED_AT_RUNTIME/VALUE UNVERIFIED). Also update FAILURE_CASE_DETECTED bookkeeping in that file so the supersession is visible (do not falsify the historical PASS record — annotate).

=======================================================================
SECTION 10 — GATE RE-EVALUATION (06_REPORT/STAGE_ACCEPTANCE_GATES.csv; AMEND with PRE_EDIT_R2 snapshot)
=======================================================================
Reassess at minimum: G4_HELPER437F70_OPERATION, G5_HELPER82B5A0_OPERATION, G6_END_TO_END_VALUE_FLOW, G10_NEGATIVE_CONTROL, G11_COORDINATE_SPACE, G13_UNIT_SCALE, G14_FINAL_POSITION_ROLE, G16_MASTER_ADJUDICATION.
  - G4 may remain PASS because 0x437F70 = singleton getter still holds. HOWEVER G4's evidence file (FUN_00437F70_DISASM.txt) contained the false S-lifetime prose; after generator repair + regeneration you MUST explicitly recheck G4_EVIDENCE_CONSISTENCY (state the check + result in the gates file/AMEND).
  - G5 may remain PASS if the arithmetic decode is untouched (verify + state).
  - G6 may remain PASS only for "scale(W) - S" — NOT for an unconditional zero-origin simplification; correct its basis text accordingly.
  - G10 must explicitly contain the negative-control supersession (NC-4 FALSIFIED_BY_COUNTEREXAMPLE; controls 1-3 stand).
  - G11: separate the scale-factor claim (K=0.01 byte-proven — stands) from the value-relation claim (out = W*0.01 - S; "always 100x smaller" conditional on S==0 — corrected wording).
  - G13 unchanged if K still proves (verify + state).
  - G14 reworded consistently with the bounded status (position role corroboration unchanged in kind; no unconditional scale relation).
  - G16: the historical MASTER_ACCEPTED stays as the historical adjudication; the gates file row must point to the supersession chain (the NEW superseding review, written later by PE-MASTER, becomes the CURRENT scientific adjudication for the corrected claims — you prepare the pointer, you do NOT write that review).
  - Any PASS depending on "S permanently zero" must be corrected.
Mechanics: AMEND the gates rows with explicit re-evaluation basis; preserve row survival (no row disappears); add correction-run gate rows if you need them (e.g. a CG-block for the correction's own gates) — documented in AMEND_LOG.

=======================================================================
SECTION 11 — COMPLETE STALE-CLAIM SWEEP (SEMANTIC, NOT ONLY EXACT STRINGS)
=======================================================================
Search the ENTIRE existing package (all subdirs incl. 00_CONTROL, and 00_CONTROL/scripts/*) for semantic equivalents of: S permanently zero / origin always zero / immutable origin / never mutated / no caller writes / no setter / global zero vector / unconditional out=W*0.01 / primary output always 100x smaller / dynamic origin rejected. Inspect paraphrases, not only exact strings; do not trust grep alone — read the files.
Minimum explicit inspection list (from the human authorization + PE-MASTER's own grep census — 01_RAW/FUN_00437F70_DISASM.txt (lines ~97/108/115/157), 01_RAW/END_TO_END_VALUE_FLOW_RAW.txt (lines ~27/49/58/113/123/133/136-138/149-155), 01_RAW/ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt (lines ~18/388/398/558/730/935-936/954-955), 01_RAW/NEGATIVE_CONTROL_RAW.txt (Control 4), 01_RAW/FALLBACK_PRIMARY_COMPARISON.txt (lines ~12/16/54), 01_RAW/FUN_0082B5A0_DISASM.txt (~line 94 conditional), 01_RAW/FUN_0050A050_DOWNSTREAM_DISASM.txt (~line 152 "global-zero-vector snapshot"), 02_ANALYSIS/HELPER_OPERATIONS.md (lines ~6-10/21/26/48), 02_ANALYSIS/OUTPUT_VALUE_RELATION.md (lines ~14/16-17/21), 02_ANALYSIS/POSITION_SEMANTICS.md (~line 29 "100:1" — check context), 02_ANALYSIS/SOURCE_VECTOR_LAYOUT.md (check), 02_ANALYSIS/SCIENCE_STATUS_DELTA.csv (rows 5/8/9), 03_EVIDENCE/EVIDENCE_INDEX.csv + 03_EVIDENCE/README.md (descriptions), 06_REPORT/REPORT.md (lines ~14-22/34-41/84-85/92-95), 06_REPORT/HANDOFF.md (lines ~10/24/39-43/55), 06_REPORT/STAGE_ACCEPTANCE_GATES.csv (G6 row), 00_CONTROL/scripts/gen_raw_evidence.py, census_triple_writes.py, gen_manifest.py, 00_CONTROL/SOURCE_IDENTITIES.json (check; likely frozen), 00_CONTROL/RUN_CONTRACT.md (historical — FROZEN), 01_RAW/AT_RUN_START_GIT_OBSERVATION.md (historical — FROZEN)).
EDIT policy: 
  - EDITABLE (with AMEND-14+ entries + PRE_EDIT_R2 snapshots): REPORT.md, HANDOFF.md, SCIENCE_STATUS_DELTA.csv, STAGE_ACCEPTANCE_GATES.csv, the analysis .md files, EVIDENCE_INDEX.csv, README.md (03_EVIDENCE), MANIFEST_SHA256.csv, SCRIPT_SHA256.csv, the generator scripts, the affected raw evidence files (bounded prose corrections; measurement content byte-stable), NEGATIVE_CONTROL_RAW.txt (append supersession block).
  - FROZEN (do NOT edit; their stale phrases are historical record): 06_REPORT/QC_AUDIT.md, 06_REPORT/QC_AUDIT_R2.md, 06_REPORT/PE_MASTER_REVIEW.md (historical adjudication — superseded by a NEW file later, never overwritten), 00_CONTROL/AMEND_LOG_R1.md entries 1-13 (append-only), 00_CONTROL/RUN_CONTRACT.md, 01_RAW/AT_RUN_START_GIT_OBSERVATION.md, 01_RAW/AT_RUN_END_GIT_OBSERVATION.md (historical; the NEW correction git observation is a separate new file), 00_CONTROL/PRE_EDIT/** (load-bearing original evidence — NEVER overwrite), 00_CONTROL/SOURCE_IDENTITIES.json (if it contains only identity metadata, leave; if it carries a stale conclusion, report to PE-MASTER instead of editing).
  - The frozen files' stale phrases must be LISTED in your correction analysis as historical-superseded (the supersession documents name them explicitly), not silently edited away.
In edited prose use the corrected canonical reading (if proven by your measurements):
  GENERAL FORMULA: out = scale(W) - S ; S INITIAL ZERO: CONFIRMED ; S MUTATION CHANNEL: CONFIRMED ; S MUTATED AT RUNTIME: UNVERIFIED ; S RUNTIME VALUE: UNVERIFIED ; S PERMANENT ZERO: RETRACTED ; UNCONDITIONAL W*0.01: RETRACTED ; UNCONDITIONAL 100x SMALLER: RETRACTED.

=======================================================================
SECTION 12 — AMENDMENT / EVIDENCE HISTORY (CRITICAL SNAPSHOT SAFETY)
=======================================================================
Current package contains AMEND-1..AMEND-13. Continue at AMEND-14. Do not reset numbering.
SECOND-ROUND SNAPSHOT SAFETY: existing 00_CONTROL/PRE_EDIT/**/*.pre files are load-bearing original-run/first-correction evidence — NEVER overwrite them. For EVERY AMEND-14+ edited file (whether or not it already has a .pre): create 00_CONTROL/PRE_EDIT_R2/<mirrored relative path>.pre (e.g. 00_CONTROL/PRE_EDIT_R2/06_REPORT/REPORT.md.pre) capturing the pre-edit bytes. This is the PREFERRED mechanism; record SNAPSHOT_MECHANISM = PRE_EDIT_R2 for every entry (an outside-tree immutable snapshot + SHA256 pair + reproducible byte diff is the documented ALTERNATIVE only if PRE_EDIT_R2 is impossible for a specific file — justify it explicitly).
For EVERY AMEND-14+ entry state explicitly: amendment number; finding; exact old claim; corrected claim; OLD SHA256; NEW SHA256; snapshot path/mechanism; reason; blast radius.
Historical QC artifacts remain frozen (QC_AUDIT.md, QC_AUDIT_R2.md untouched). Do not destructively rewrite prior audit history. AMEND_LOG_R1.md gets only APPENDED entries + (if needed) a new section header for the correction pass.

=======================================================================
SECTION 13 — NEW RAW EVIDENCE REQUIRED (INSIDE THE EXISTING PACKAGE)
=======================================================================
01_RAW/: ORIGIN_SINGLETON_WRITE_THROUGH_CENSUS.csv; ORIGIN_SINGLETON_WRITE_THROUGH_RAW.txt; ORIGIN_SETTER_458D90_DISASM.txt; ORIGIN_SETTER_CALLER_CENSUS.csv; ORIGIN_SETTER_REACHABILITY_RAW.txt; CORRECTION_RUN_GIT_OBSERVATION.md.
02_ANALYSIS/: ORIGIN_STATUS_CORRECTION.md (or canonical naming equivalent).
00_CONTROL/scripts/: new deterministic probes (write-through census; reachability census; setter decode; whatever you need) — each fail-closed S0, read-only on the EXE, recorded in SCRIPT_SHA256.csv.
Every load-bearing conclusion must provide: MEASURED_QUANTITY; INDEPENDENT_SOURCE_OF_TRUTH; WHY_NON_CIRCULAR; FAILURE_CASE_DETECTED. Mandatory failure case for the original false claim: 0x00458E27 (+ exact S-write instructions).
For the write-through census: independently measured caller denominator; rows generated from actual instruction decode; aggregates mechanically derived from rows; NO conclusion baked into the generator; unresolved sites disclosed.
Regenerate 00_CONTROL/SCRIPT_SHA256.csv, 03_EVIDENCE/README.md, 03_EVIDENCE/EVIDENCE_INDEX.csv, 06_REPORT/MANIFEST_SHA256.csv in ONE final pass (gen_manifest.py order: SCRIPT_SHA256 -> README -> EVIDENCE_INDEX -> MANIFEST; L12 self-exclusion rules respected; the new files must be covered; QC_AUDIT_R3.md and the superseding review do not exist yet — the manifest regeneration at THIS phase covers what exists on disk at your run end; a later regeneration happens at persistence).
Zero __pycache__, zero .pyc, zero proprietary payload (no EXE bytes beyond short instruction citations; no full copyrighted content).

=======================================================================
SECTION 14 — EXECUTOR PASS/FAIL GATES (pre-registered)
=======================================================================
EG1 FALSIFIER_REPRODUCED: your deterministic scripts reproduce EAX=S at 0x458E2C and >=1 write-through through S with offsets {0,4,8} at 0x458E30/0x458E36/0x458E3D. If your scripts contradict PE-MASTER's anchors: HARD STOP + report (do not force agreement, do not proceed on a contradiction).
EG2 CENSUS_COMPLETE: fresh denominator D re-measured (report D; historical 99 = expectation only); D/D rows classified with taxonomy dispositions; every disposition mechanically summed; unresolved rows disclosed; N=16 primary + N=8 view both emitted; the known writer site present with three write events.
EG3 SETTER_DECODED: extent + ABI + esp ledger + input types + three write formulas + chain ABI all from your own decode; ORIGIN_SETTER_INPUT_TYPE and ORIGIN_SETTER_OPERATION stated; ORIGIN_SETTER_FINAL_SEMANTIC_ROLE = UNVERIFIED.
EG4 REACHABILITY_DERIVED: both reported branches re-derived from your own censuses with boundary proofs; the misattribution corrections (0x4171BA in FUN_00417030; 0xA7A244 data-not-vtable; the ArkClientPlayerImpl subtree not reaching the setter) verified or refuted from your own bytes; ORIGIN_SETTER_RUNTIME_EXECUTION = UNVERIFIED.
EG5_GENERATORS_CLEAN: zero hardcoded science conclusions in the repaired generators' emitted text (grep-verifiable: no "never mutated", no "at ALL times", no "whole process lifetime", no "measured over all 99 sites" style claims emitted by generator literals); measurement sections of regenerated raws byte-stable vs PRE_EDIT_R2 except corrected prose (diffs documented in AMEND).
EG6 SWEEP_COMPLETE: every stale-claim location either corrected or explicitly listed as frozen-historical; the correction analysis names the frozen files.
EG7 SNAPSHOT_SAFE: every AMEND-14+ edited file has a PRE_EDIT_R2 .pre (or justified documented alternative); PRE_EDIT/** byte-identical to before (verify by hash census before and after; state the census).
EG8 PACKAGE_FENCED: no new package root; no AUDIT_ENTRYPOINT.md edit; no skill-tree edit; no runtime execution; no commit/push; zero proprietary payload; zero pycache/pyc; pre-existing untracked paths untouched.
Non-pass classes for each gate: DOCUMENTED_FINDING (bounded, no narrative stretching) or HARD_STOP (return to PE-MASTER). STOP CONDITIONS: SUCCESS A (writer exists, exact mutation operation recovered, status corrected, canonical false permanent-zero claim superseded) / SUCCESS B (external finding independently disproven with stronger physical evidence) / SUCCESS C (writer exists but some static reachability unresolved; general formula and origin status correctly bounded). Any is valid. Do not continue merely to obtain a preferred semantic label.
HARD STOP conditions: BASE SHA mismatch/conflict; EXE pin mismatch; your falsifier contradicting PE-MASTER's byte anchors; inability to classify the census denominator honestly.
=======================================================================
SECTION 15 — DELIVERABLES + MANDATORY RESPONSE HANDOFF BLOCK
=======================================================================
Persist FIRST (before any package edit): 00_CONTROL/CORRECTION_CONTRACT_ORIGIN_MUTABILITY_R1.md containing THIS contract verbatim (the full dispatch text) — so the contract is immutable on disk before mutations. Then execute. Then APPEND the final executor handoff to the contract file or a 00_CONTROL/CORRECTION_EXECUTOR_RETURN.md.
Your FINAL message back to PE-MASTER must end with EXACTLY this handoff block (fill values):
CORRECTION_RUN_RETURN
RUN_ID = PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915
EXECUTOR_STATUS = COMPLETE / DOCUMENTED_FINDINGS / HARD_STOP
BASE_SHA_OBSERVED = <git HEAD at start and at end>
EXE_PIN_VERIFY = PASS/FAIL
EAX_PROVENANCE_AT_0x458E2C = FUN_00437F70_RETURN / OTHER / UNVERIFIED
WRITE_THROUGH_WINDOW_N = <value>
HISTORICAL_WINDOW_N = 8
DIRECT_CALLER_DENOMINATOR = <fresh value>
ORIGIN_WRITE_THROUGH_CENSUS = <rows/dispositions summary + writer sites list>
ORIGIN_WRITER_SITES = <list>
ORIGIN_POINTER_ESCAPE_RESIDUALS = <counts>
ORIGIN_SETTER_OPERATION = <one line>
ORIGIN_SETTER_INPUT_TYPE = <one line>
ORIGIN_SETTER_FINAL_SEMANTIC_ROLE = UNVERIFIED
ORIGIN_SETTER_STATIC_REACHABILITY = <one line: the true chain>
LIVE_CANDIDATE_BRANCH = <branch A disposition incl. misattribution corrections>
DEAD_CANDIDATE_BRANCH = <branch B disposition>
ORIGIN_MUTATED_AT_RUNTIME = UNVERIFIED
ORIGIN_INITIAL_ZERO = <status>
ORIGIN_MUTATION_CHANNEL_EXISTS = <status>
ORIGIN_PERMANENT_ZERO = REJECTED (if reproduced)
ORIGIN_RUNTIME_VALUE = UNVERIFIED
OUTPUT_GENERAL_FORMULA = <status>
OUTPUT_ZERO_ORIGIN_SPECIAL_CASE = <status>
OUTPUT_ALWAYS_W_TIMES_0_01 = REJECTED (as unconditional, if reproduced)
PRIMARY_ALWAYS_100X_SMALLER = REJECTED (as unconditional, if reproduced)
NEGATIVE_CONTROL_4 = FALSIFIED_BY_COUNTEREXAMPLE (if reproduced)
GENERATOR_DEFECT = <one line: which conclusions removed from which generators>
AMEND_RANGE = AMEND-14..AMEND-<n>
SNAPSHOT_MECHANISM = PRE_EDIT_R2
OLD_PRE_EDIT_PRESERVED = YES + <hash census statement>
FILES_CHANGED = <count + list summary>
GATES_CHANGED = <gate ids>
NEW_EVIDENCE = <paths>
INTERVENTION_LEDGER = EMPTY (STATIC-ONLY run; zero runtime interventions)
UNRESOLVED = <honest list>
WORKING_DIR_CLEAN = YES/NO (pycache/pyc)
Remember: NO_NESTED_TASKS; you are the sole executor; fresh QC and the superseding review are NOT yours to write. Return to PE-MASTER with the handoff block.
