# ORIGIN_STATUS_CORRECTION — corrected origin-singleton status algebra

RUN_ID (correction): PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915
CANONICAL PACKAGE: PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915 (in-place correction; no new package root)
EXECUTOR: pe-reconstruction (PE-MASTER-dispatched bounded correction; STATIC-ONLY; zero runtime interventions)
DATE: 2026-09-15
SCOPE: corrects the origin-singleton S mutability -> origin setter -> output formula status algebra of this
package. All measurements cited below were produced by THIS correction run's deterministic probes
(00_CONTROL/scripts/{probe_origin_setter.py, census_write_through.py, census_setter_reach.py,
probe_output_formula.py}; S0 fail-closed; capstone 5.0.7 decodes of Entropia.exe physical bytes,
SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31).

## 0. WHAT WAS WRONG (the falsified original claims)

The original run claimed (now FALSIFIED by counterexample 0x00458E27):
- "No caller writes through the returned pointer within 8 instructions (measured over all 99 sites)" —
  a FABRICATED measurement claim: the original instrument (classify_pair_membership in
  gen_raw_evidence.py) looked at 2 instructions after each call and keyed on the first instruction's
  pattern; it never measured write-through. Its own census CSV recorded
  instruction_after_next='mov dword ptr [eax], edx' for the very site 0x00458E27 that writes through
  the returned pointer three times.
- "S == {0,0,0} permanently / never mutated post-construction / immutable after construction" — an
  INVALID INFERENCE from a valid measurement: the triple addresses 0xBA921C/20/24 write-census (which
  SURVIVES) never implied S immutability, because the singleton object is a 12-byte heap copy written
  through the getter's returned pointer, not through the triple addresses.

Standing lessons recorded (AMEND_LOG_R1.md, correction-pass entries):
- LESSON 1: CLAIM_OF_MEASUREMENT_REQUIRES_MEASUREMENT_ARTIFACT — a claim of the form "measured over
  all 99 sites" requires a measurement artifact that actually performed that measurement; a
  2-instruction classifier is not an 8-instruction write-through measurement.
- LESSON 2: ROW_INTEGRITY_DOES_NOT_VALIDATE_INFERENCE — a byte-correct CSV does not imply the
  interpretation of that CSV is correct; the original census rows were byte-correct AND the
  write-through conclusion drawn from them was false.

## 1. CORRECTED STATUS ALGEBRA (each status: measured quantity, evidence, why non-circular, failure case)

### ORIGIN_INITIAL_ZERO = CONFIRMED
- MEASURED_QUANTITY: (a) PE section table: .data vaddr=0x76C000 vsize=0x3D6E4 rawsize=0x34000 -> raw
  end RVA 0x7A0000; the triple RVAs 0x7A921C/0x7A9220/0x7A9224 lie BEYOND the raw end (virtual tail;
  loader zero-fill; no static initializer bytes exist in the file); (b) ctor 0x0082B580 decode:
  'mov eax,ecx; mov ecx,[0xba921c]; mov [eax],ecx; mov edx,[0xba9220]; mov [eax+4],edx;
  mov ecx,[0xba9224]; mov [eax+8],ecx; ret' — the singleton is constructed as a copy of the triple;
  (c) independent imm32 recount of the triple: 107/81/80 = 268 occurrences, all in .text (matches the
  surviving census); (d) the SURVIVING triple write-census (01_RAW/ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt,
  unchanged): store-class candidates 0 across all enumerated channels.
- EVIDENCE: 01_RAW/ORIGIN_SETTER_458D90_DISASM.txt [S.8]/[S.9]; 01_RAW/ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt
  (surviving original measurement, channels enumerated).
- WHY_NON_CIRCULAR: the section table, ctor decode and recount are decoded from bytes by this
  correction run's own probes; the surviving census is an independent mechanical scan whose
  aggregate (268 imm32 occurrences) this run re-measured and MATCHED.
- FAILURE_CASE: if a static triple-writer existed, the surviving census' store-class count would be
  nonzero (it is 0); if the ctor did not copy the triple, the [S.9] decode would show different
  source addresses (it shows exactly 0xBA921C/20/24).
- RESULT: the singleton S starts as {0,0,0} (zero-filled triple copied at construction).

### ORIGIN_MUTATION_CHANNEL_EXISTS = CONFIRMED
- MEASURED_QUANTITY: call site 0x00458E27 (E8 rel32 -> 0x437F70, direct-call verified) inside function
  0x00458D90..0x00458E43 (extent: ret @0x00458E43; 12x int3 padding 0x00458E44..0x00458E4F; next
  function 0x00458E50): after the getter returns (EAX proven = FUN_00437F70 return: fast path EAX=
  [0xBA1804]; cold-success path EAX = ctor 0x0082B580 return = the same pointer; alloc-fail corner
  EAX=NULL disclosed), the function executes three stores through EAX:
  mov [eax],edx @0x00458E30; mov [eax+4],ecx @0x00458E36; mov [eax+8],edx @0x00458E3D
  (offsets 0/4/8 — the three f32 components of the 12-byte singleton), with the written values
  proven by the esp ledger + slot dataflow to be f32(f80(-(int32_in[i]))) (neg + fild/fstp chain in
  the local frame).
- EVIDENCE: 01_RAW/ORIGIN_SETTER_458D90_DISASM.txt [S.1]/[S.3]/[S.4]/[S.10];
  01_RAW/ORIGIN_SINGLETON_WRITE_THROUGH_CENSUS.csv row 0x00458E27 (disposition
  WRITE_S_PLUS_0+4+8, three write events) + 01_RAW/ORIGIN_SINGLETON_WRITE_THROUGH_RAW.txt [W.2]/[W.4].
- WHY_NON_CIRCULAR: the falsifier decodes the bytes directly; the census is an independent
  provenance-aware instrument (sprov engine + instrument self-test at the known-negative pair site
  0x0050A075) that MUST reproduce the known writer or declare itself defective ([W.4]: INSTRUMENT OK).
- FAILURE_CASE: the falsified original claim itself — "no caller writes through the returned pointer"
  — with counterexample 0x00458E27 (+ the exact write instructions 0x458E30/0x458E36/0x458E3D).
- RESULT: a write-through mutation channel for S exists in the static bytes.

### ORIGIN_MUTATED_AT_RUNTIME = UNVERIFIED
- MEASURED_QUANTITY: none can exist in a STATIC-ONLY run (the client is never executed).
- EVIDENCE: the full static chain exists (see ORIGIN_SETTER_STATIC_REACHABILITY below), but no
  runtime trace exists in this package.
- WHY_NON_CIRCULAR: the UNVERIFIED label is exactly the absence of runtime evidence; static
  reachability does NOT prove runtime execution and MUST NOT be substituted for it.
- FAILURE_CASE: any attempt to promote this to CONFIRMED on static evidence alone.
- RESULT: whether S is ever actually mutated while the game runs is NOT measured.

### ORIGIN_PERMANENT_ZERO = REJECTED (as previously claimed)
- MEASURED_QUANTITY: the mutation channel exists (above) AND is statically reachable from the main
  message loop (see ORIGIN_SETTER_STATIC_REACHABILITY); the original claim's premise ("all 99 call
  sites measured, no writer exists") is falsified by the write-through census (1 writer site with
  three write events; denominator 99 re-measured, all sites boundary-verified).
- EVIDENCE: 01_RAW/ORIGIN_SINGLETON_WRITE_THROUGH_CENSUS.csv; 01_RAW/ORIGIN_SETTER_REACHABILITY_RAW.txt.
- WHY_NON_CIRCULAR: rejection requires only ONE valid counterexample; the census provides it
  independently (and the falsifier reproduced it before any canonical edit).
- FAILURE_CASE: 0x00458E27 (+ writes 0x458E30/0x458E36/0x458E3D).
- RESULT: "S == {0,0,0} permanently" is RETRACTED. What SURVIVES: S STARTS as {0,0,0}
  (ORIGIN_INITIAL_ZERO) and the triple-address write-census measurement survives as a measurement
  (the triple itself is never written within the enumerated channels); the IMMUTABILITY INFERENCE
  from it does not.

### ORIGIN_RUNTIME_VALUE = UNVERIFIED
- Same reasoning as ORIGIN_MUTATED_AT_RUNTIME. No runtime value of S is measured; no default
  runtime value may be claimed in either direction.

### ORIGIN_SETTER_OPERATION (measured; label, not a semantic name)
- S[0] := f32(f80(-(int32)in[0]))  @ write 0x00458E30 (mov [eax],edx)
  S[1] := f32(f80(-(int32)in[1]))  @ write 0x00458E36 (mov [eax+4],ecx)
  S[2] := f32(f80(-(int32)in[2]))  @ write 0x00458E3D (mov [eax+8],edx)
  where ECX (setter entry) = pointer to a 12-byte triple of three INT32 at [ecx+0/4/8]; each value
  is negated (neg), converted int32->f32 via the fild/fstp chain into a local 3xf32 frame array, and
  stored through the getter-returned singleton pointer. (Contract Section 5's expected shape
  S[i] = f32(-(int32)in[i]) is CONFIRMED by this run's own esp ledger + slot dataflow.)
- EVIDENCE: 01_RAW/ORIGIN_SETTER_458D90_DISASM.txt [S.3]/[S.4]/[S.10].

### ORIGIN_SETTER_INPUT_TYPE (measured)
- thiscall-style: ECX = pointer to a 12-byte triple of three INT32 at [ecx+0/4/8]; no stack args;
  plain ret. The caller FUN_00458E50 builds the triple via three 'fld + call 0x95DA40' f32->int32
  conversions (0x95DA40 = ftol-style helper: measured bounded head uses 'fstp qword [esp]' +
  'cvttsd2si eax, qword [esp]' with an SSE2-availability flag at [0xBA96C8]) after fetching floats,
  applies the delta-condition @0x00458EE2 (sum of squared int32 deltas == 0 -> SKIP the setter),
  stores the new triple into [esi+0/4/8] @0x00458EE8..0x00458EEF and calls the setter @0x00458EF2
  with ECX=ESI. 0x00458C40 (called @0x00458EB2) computes int32 deltas/abs-deltas of the same triple
  pair (bounded head decode recorded).
- EVIDENCE: 01_RAW/ORIGIN_SETTER_458D90_DISASM.txt [S.6]/[S.6.1]/[S.7].

### ORIGIN_SETTER_FINAL_SEMANTIC_ROLE = UNVERIFIED
- No semantic name is assigned to S or to the setter (per contract: no world-origin / floating-origin
  / camera-origin / region-origin / sector-origin / cell-origin naming). What the bytes prove is the
  OPERATION (negate-convert-store through the singleton pointer) and the static call structure; the
  SEMANTIC role would require runtime evidence and independent corroboration outside this run's scope.

### ORIGIN_SETTER_STATIC_REACHABILITY (measured; the TRUE chain)
- FUN_00402910 (message loop; sole E8 caller 0x0040563A — the prior-canon boot chain target)
  --E8@0x0040296F--> FUN_00417030 (tick; the loop's 'mov bl,al' @0x00402974 + 'test bl,bl' +
  'jne 0x402930' back-edge make the tick's AL return feed the loop-continue condition)
- FUN_00417030 --guarded sub-path (call 0x4143f0 -> singleton; mov ecx,eax; call 0x42bc20;
  test al,al; je 0x417216 skips)--> E8@0x004171BA --> FUN_00458E50
  (sole E8 caller of FUN_00458E50; measured inside FUN_00417030's extent 0x00417030..0x004172A0)
- FUN_00458E50 --delta-condition @0x00458EE2--> E8@0x00458EF2 --> FUN_00458D90 (the setter;
  sole E8 caller 0x00458EF2)
- FUN_00458D90 --E8@0x00458E27--> FUN_00437F70 (getter) -> three writes through S
- Channel censuses: every chain member has ZERO E9/imm32/vtable channels (never address-taken,
  never virtual): SETTER(1 E8 caller 0x458EF2), SETTER_CALLER(1: 0x4171BA), TICK_FN(1: 0x40296F),
  MESSAGE_LOOP(1: 0x40563A).
- EVIDENCE: 01_RAW/ORIGIN_SETTER_CALLER_CENSUS.csv; 01_RAW/ORIGIN_SETTER_REACHABILITY_RAW.txt
  [R.1]-[R.4]/[R.7].

### ORIGIN_SETTER_RUNTIME_EXECUTION = UNVERIFIED
- Static reachability does NOT prove runtime execution. STATIC-ONLY run; no runtime evidence.

### LIVE_CANDIDATE_BRANCH (external Branch A, re-derived) — REAL EDGES, DOES NOT REACH THE SETTER
- Measured: 0x00514EF0 is a virtual method (sole channel: .rdata imm32 @0x00A7D778 = vtable
  0x00A7D764 slot 5; RTTI: COL 0x00AA1304 (.rdata), TD 0x00B78F74 (.data), name
  '.?AVArkClientPlayerImpl@@' — the class-name identity is REAL); edge E8@0x005159E5 -> 0x00417880
  (inside FUN_00514EF0's measured extent 0x00514EF0..0x00515F20); FUN_00417880 --E8@0x00417972-->
  0x00416FD0 (E8 callers of 0x417880 measured: {0x00417B11, 0x005159E5}).
- MISATTRIBUTION CORRECTION (measured): the external chain "0x458E50 <- 0x416FD0" is FALSE:
  FUN_00416FD0's own extent ends at its last terminal 'ret 0xc' @0x0041702C (first ret 0xc
  @0x0041701D; single int3 @0x0041702F) and the next function starts 0x00417030; FUN_00416FD0's own
  callees do NOT include 0x00458E50 / 0x00417030 / 0x00458D90. The measured sole E8 caller of
  0x00458E50 (0x004171BA) lies inside FUN_00417030. (PE-MASTER anchor cross-check discrepancy,
  reported loudly: the anchor note said 'ret 0xc @0x0041702D'; measured ret is @0x0041702C — the
  anchor VA is mid-instruction; boundary conclusion unchanged.)
- Also measured: the '[esi]=0xA7A244' store inside FUN_00416FD0 (@0x00417011) points at a DATA
  DESCRIPTOR, not a vtable: [0xA7A240]=0x004B3CC0 (a .text code pointer, not a COL), followed by
  {0x00416AD0, 0x005B8B80}, zeros, a float-looking dword 0x3FE80000 and the string 'Parameters\'
  measured at 0x00A7A258 — consistent with an init/registration helper for a settings descriptor.
- DISPOSITION: Branch A's edges are real, but the subtree NEVER reaches the setter; the
  ArkClientPlayerImpl class-name identity is real and IMMATERIAL to the setter chain.

### BRANCH_B_SUBTREE (external Branch B, re-derived; AMEND-23 corrected disposition) —
  LIVE WITHIN THE MEASURED CHANNELS, AND IMMATERIAL TO ORIGIN MUTABILITY
- [AMEND-23 (QC_R3 findings F1/F4; PE-MASTER adjudicated; fix round
  PE_935_SF_QC_R3_FINDINGS_FIX_R1_20260915): this section originally appeared as
  'DEAD_CANDIDATE_BRANCH (external Branch B, re-derived) — STATICALLY DEAD WITHIN MEASURED
  CHANNELS, AND IMMATERIAL TO THE SETTER' and that reading is RETRACTED (quoted verbatim
  below). Its containment claims contradicted the executor's own raw measurements
  (01_RAW/ORIGIN_SETTER_REACHABILITY_RAW.txt [R.6]: both containment tests printed False).
  Every corrected fact below is measured from bytes; independent probe evidence:
  01_RAW/FIX_ROUND_R4_BYTE_REVERIFICATION_RAW.txt [A]; QC evidence:
  00_CONTROL/QC_R3_RAW/QC_R3_REACHABILITY_RAW.txt.]
- RETRACTED ORIGINAL (verbatim):
  "DEAD_CANDIDATE_BRANCH (external Branch B, re-derived) — STATICALLY DEAD WITHIN MEASURED
   CHANNELS, AND IMMATERIAL TO THE SETTER
   - Measured: E8 callers of 0x00417A40 = {0x004B1EEB} (inside FUN_004B1B70's stream, verified by
     linear decode from 0x4B1B70); 0x004B1EEB calls 0x417A40; FUN_00417A40 --E8@0x00417B11--> 0x00417880
     (the same 0x417880 as Branch A — again NOT reaching the setter).
   - FUN_004B1B70 channels measured: E8 = {0x004B1F2C} (the SELF-RECURSIVE edge only, verified as a
     real instruction boundary by linear decode from 0x4B1B70 through 0x4B1F2C), E9 = none, imm32 =
     none, vtable = none -> STATICALLY DEAD WITHIN THE MEASURED CHANNELS (no external entry channel
     exists for it in this image).
   - BUT: this subtree does not reach the setter at all (0x4B1B70 -> 0x417A40 -> 0x417880 ->
     0x416FD0-path measured above), so its deadness is IMMATERIAL to origin mutability."
  END OF RETRACTED ORIGINAL.
- Measured corrections (all from bytes):
  (a) FUN_004B1B70's extent ends at ret 0x004B1C6E + single int3 0x004B1C6F; the next function
      starts 0x004B1C70 (SEH prologue: push -1; push 0x9acc2a). NEITHER E8@0x004B1EEB (call
      0x417A40) NOR E8@0x004B1F2C (call 0x4B1B70) is inside FUN_004B1B70's stream (both raw
      containment tests: False); BOTH are inside FUN_004B1C70's stream (extent
      0x004B1C70..0x004B1FB0). 0x4B1F2C is therefore a SIBLING call FUN_004B1C70 ->
      FUN_004B1B70, NOT self-recursion.
  (b) FUN_004B1C70 channels measured: E8 = {0x004B2984}, E9 = none, imm32 = none, vtable =
      none. The external caller E8@0x004B2984 is a real instruction inside FUN_004B2950 (the
      prior-canon ArkClientPacketExecutor::Execute; extent 0x004B2950..0x004B29F0), in the
      case-0xB2 dispatch path ('cmp edi, 0xb2' @0x004B2975; jne 0x4B2991 skips; the taken path
      pushes [esp+0x20] and calls 0x4B1C70 @0x004B2984). An external entry channel EXISTS —
      the branch is NOT statically dead within the measured channels.
  (c) The measured branch-B subtree is therefore Execute(FUN_004B2950) --case 0xB2-->
      FUN_004B1C70 -> {0x417A40 -> 0x417880 -> 0x416FD0 (config/init subtree; the same
      0x416FD0 dead-end path measured for Branch A); 0x4B1B70 (queue/ring processing)} —
      STATICALLY REACHABLE within the measured channels.
  (d) Callee-set closure (measured): FUN_004B1B70's callees {0x40E160, 0x4B18D0, 0x40E180,
      0x95DB40}; FUN_004B1C70's 50 callees (including 0x417A40 and 0x4B1B70); FUN_00417A40's
      callees (including 0x417880 @0x00417B11) — every set EXCLUDES all setter-chain members
      {0x458E50, 0x458D90, 0x417030}; the 0x417A40 -> 0x417880 -> 0x416FD0 path dead-ends
      w.r.t. the setter (measured above).
- DISPOSITION (corrected): the branch-B subtree is
  LIVE_WITHIN_MEASURED_CHANNELS_BUT_IMMATERIAL_TO_ORIGIN_MUTABILITY — it has a real external
  entry channel (FUN_004B2950 -> FUN_004B1C70) and STILL NEVER REACHES the origin setter
  (0x458D90's sole static in-tree caller remains the message-loop chain; see
  ORIGIN_SETTER_STATIC_REACHABILITY). The "does not reach the setter" conclusion SURVIVES by
  a different route than the retracted deadness argument; the origin-mutability status algebra
  of this document is UNCHANGED.

## 2. WRITE-THROUGH CENSUS (the measurement the original claim pretended to have)

- DIRECT_CALLER_DENOMINATOR (re-measured): 99. All 99 raw E8 candidates were VERIFIED as real
  instruction boundaries (padding-anchor + linear-decode-landing rule; 0 excluded). The historical
  census' "99 sites" was a raw-candidate count WITHOUT boundary verification; this census discloses
  the verification.
- WINDOW (pre-registered): N=16 primary; separate N=8 historical view (the falsified claim said
  "within 8 instructions"). Callee-head bound 0xA0.
- N=16 dispositions (mechanical sums; D=99): S_PTR_ESCAPED_READ_ONLY 43; NO_WRITE_WITHIN_BOUND 17;
  S_PROVENANCE_LOST 19; WRITE_S_PLUS_0+4+8 1 (site 0x00458E27 — the ONLY writer);
  CONTROL_FLOW_ESCAPE 1; S_PTR_ESCAPED_UNRESOLVED 12; INSUFFICIENT_PROOF 6. Sum check 99 == 99 OK.
- N=8 (historical view): READ_ONLY 41; NO_WRITE 18; PROV_LOST 14; WRITE_S_PLUS_0+4+8 1;
  INSUFFICIENT_PROOF 17; UNRESOLVED 8. (At N=8, 17 sites' provenance fate is not even resolvable
  within the claimed window — the original "measured within 8 instructions" claim was doubly
  false: the instrument never measured write-through, and 8 instructions cannot resolve the
  provenance fate of 17 of the 99 sites.)
- ORIGIN_WRITER_SITES (N=16): exactly one — 0x00458E27 (three write events, offsets 0/4/8).
- ORIGIN_POINTER_ESCAPE_RESIDUALS (N=16): 12 S_PTR_ESCAPED_UNRESOLVED (S_PTR forwarded into deeper
  consumers whose bounded heads forward or ignore it: measured escape targets 0x0082B870, 0x0082B5F0,
  0x0058E520, 0x004B2A50, 0x006C4720 families), 6 INSUFFICIENT_PROOF (window exhausted with live
  register provenance), 1 CONTROL_FLOW_ESCAPE. These residuals REMAIN UNRESOLVED — bounded-head
  absence is NOT turned into global absence (the 0x4CE5B0 disclosure discipline).
- EVIDENCE: 01_RAW/ORIGIN_SINGLETON_WRITE_THROUGH_CENSUS.csv; 01_RAW/ORIGIN_SINGLETON_WRITE_THROUGH_RAW.txt.

## 3. OUTPUT FORMULA REVALIDATION (independent re-derivation)

- OUTPUT_GENERAL_FORMULA = CONFIRMED: out[i] = f32( f32( (f80)W[i] * (f80)K ) - (f80)S[i] ),
  i in {0,4,8}; K = (double)(float)0.01 measured bit-exact (qword @0xA7B360, bits
  0x3F847AE140000000, BITMATCH vs the (double)(float)0.01 reference); FUN_0082B5A0 ret 8 measured.
  The helper READS S (fsub source operands [ecx], [ecx+4], [ecx+8]) and never writes through ECX.
- OUTPUT_ZERO_ORIGIN_SPECIAL_CASE = CONFIRMED CONDITIONALLY: IF S == {0,0,0} (+0.0 in all
  components) THEN out[i] = f32(W[i]*K) bit-exactly (IEEE-754: x - (+0.0) == x for finite x), with
  the sign-of-zero caveat ((+0)-(+0)=+0; (-0)-(+0)=-0) — i.e., the simplification is a CONDITION on
  S, not an unconditional identity.
- OUTPUT_ALWAYS_W_TIMES_0_01 = REJECTED (as an unconditional claim; correct only as the special case
  above).
- PRIMARY_ALWAYS_100X_SMALLER = REJECTED (as an unconditional claim; the value relation is
  out = scale(W) - S; a 100:1 magnitude relation holds only conditionally on S == 0 — and even then
  it is a magnitude statement, not the bit-exact value relation).
- NUMERIC_SCALE_FACTOR = CONFIRMED (K bits re-measured this run: BITMATCH).
- CM_TO_M = PLAUSIBLE (unchanged; not upgraded — no new evidence on unit semantics was sought or
  obtained; the K measurement supports the scale value, not the unit interpretation).
- EVIDENCE: 01_RAW/OUTPUT_FORMULA_REVALIDATION_RAW.txt [F.1]-[F.5].

## 4. NEGATIVE CONTROL #4 SUPERSESSION

- NEGATIVE_CONTROL_4 = FALSIFIED_BY_COUNTEREXAMPLE. Controls 1-3 STAND (they concern other
  promotion inferences and are unaffected). The supersession block appended to
  01_RAW/NEGATIVE_CONTROL_RAW.txt records: original premise ("all 99 call sites ... measured"),
  original result ("dynamic origin rejected; S = permanent zero vector"), the counterexample
  (0x00458E27 + writes 0x458E30/0x458E36/0x458E3D), why the control failed (the "measured"
  write-through never had a measurement artifact; the original census instrument recorded
  instruction_after_next='mov dword ptr [eax], edx' for this very site but never interpreted
  write-through), and the resulting status correction (this document's algebra).

## 5. BOUNDED STATUS SUMMARY (canonical corrected reading)

- GENERAL FORMULA: out = scale(W) - S
- S INITIAL ZERO: CONFIRMED
- S MUTATION CHANNEL: CONFIRMED (setter 0x00458D90; writer site 0x00458E27; offsets 0/4/8;
  operation S[i] := f32(-(int32)in[i]))
- S MUTATED AT RUNTIME: UNVERIFIED
- S RUNTIME VALUE: UNVERIFIED
- S PERMANENT ZERO: RETRACTED
- UNCONDITIONAL W*0.01: RETRACTED (conditional special case stands)
- UNCONDITIONAL 100x SMALLER: RETRACTED (conditional statement stands)
- ORIGIN_SETTER_STATIC_REACHABILITY: message loop FUN_00402910 -> FUN_00417030 tick -> guarded ->
  FUN_00458E50 -> delta-conditioned -> FUN_00458D90 (all edges measured; no virtual channels)
- ORIGIN_SETTER_RUNTIME_EXECUTION: UNVERIFIED
- Frozen historical records whose stale phrases are superseded by this document (NOT edited):
  06_REPORT/QC_AUDIT.md, 06_REPORT/QC_AUDIT_R2.md, 06_REPORT/PE_MASTER_REVIEW.md (historical
  adjudication; superseded by a NEW review to be written by PE-MASTER), 00_CONTROL/RUN_CONTRACT.md,
  01_RAW/AT_RUN_START_GIT_OBSERVATION.md, 01_RAW/AT_RUN_END_GIT_OBSERVATION.md,
  00_CONTROL/PRE_EDIT/** (load-bearing originals), 00_CONTROL/AMEND_LOG_R1.md entries 1-13
  (append-only; their recorded "S immutable/never written" conclusions are superseded by this
  correction's evidence, recorded as AMEND-14+ entries).
