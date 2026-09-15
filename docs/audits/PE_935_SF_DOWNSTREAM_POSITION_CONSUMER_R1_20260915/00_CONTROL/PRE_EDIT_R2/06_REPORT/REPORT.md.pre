# REPORT — PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915
# RUN_CLASS: MATERIAL | RUN_TYPE: STATIC_SEAM_PROBE | MILESTONE: EU935-M1 | TARGET: PCG_9_3_5
# EXECUTOR: pe-reconstruction | STATIC-ONLY (client never executed) | ZERO git mutations by executor
# Environment measured at run time: python 3.12.7 (D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe);
#   capstone 5.0.7 (cs_version (5, 0, 1280)). Source: Entropia.exe size 8015872, SHA256
#   E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31, PE32 i386, ImageBase 0x00400000 — S0 PASS.

## PRIMARY QUESTION
"After SceneFeeder finds the named NiAVObject, what exactly happens to its m_kWorld translation through the chain
NiAVObject+0x90 -> FUN_00437F70 -> FUN_0082B5A0 -> output buffer?"

## ONE-LINE ANSWER (highest status the bytes support)
**CONFIRMED:** FUN_0050A050 itself writes NOTHING on the primary path; FUN_00437F70 is a lazy get-or-create of a
12-byte origin singleton S (always {0,0,0} — its source triple 0xba921c/20/24 is never written: the correction-pass
whole-image write census classifies all 268 imm32 occurrences (loads/pushes/getters only) with 0 store-class
candidates across every store encoding, 0 widened-overlap stores, 0 computed-base stores, all 24 push-site
consumers and both getter chains read-only — 01_RAW/ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt — and it sits
zero-initialized in .data's virtual tail), and FUN_0082B5A0 is the sole writer of the caller's out float3,
computing bit-exactly `out[i] = f32( f32( W[i] * (double)(float)0.01 ) - S[i] )` per component (i = 0/4/8), i.e.
the named NiAVObject's m_kWorld translate converted into a 100:1-scaled internal space (world translate * 0.01,
origin zero, identity axis order) — with an exact algebraic inverse family ((src+S)*100.0, FUN_0082B6A0) anchored
on the same singleton.

## EXECUTIVE SUMMARY (what actually happens, end-to-end)
1. FUN_0050A050 (SF vtable slot 3, class vtable 0xa7d458, thiscall, ret 8) receives (out float3* [esp+4],
   name [esp+8]). It looks up the named object on the SF root node (SF+0x30, a refcounted 0x118-byte
   NiNode-family object) via NiNode vtable slot17 = FUN_007B5390 (recursive named-object lookup — package-B pin,
   re-measured MATCH).
2. On success it forms &obj->m_kWorld.m_Translate (obj+0x90 — Phase B: 13-dword world block at +0x6C, translate at
   blockstart+36; m_kLocal at +0x38 with translate +0x5C is a DIFFERENT field), pushes (out, src) and calls
   FUN_00437F70.
3. FUN_00437F70 IGNORES both stack args (plain 'ret'; it is not a thiscall here), returns the singleton S from
    global slot 0xba1804, constructing it once (operator new(12), ctor FUN_0082B580 copies the global triple
    0xba921c/0xba9220/0xba9224). The triple is proven never written by the correction-pass whole-image write
    census (01_RAW/ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt: 268 imm32 occurrences containment-classified — 81+81+80
    absolute loads, 24 pushes, 2 getter loads; 0 store-class candidates across every store encoding; 0
    widened-overlap stores; 0 computed-base stores in the [0xba9000,0xba92c0) hunt window; all 24 push-site
    consumers and both getter chains read-only; disclosed residuals enumerated in the census [T.10]) => S = zero
    vector forever; S is never mutated after construction (no caller writes through the return within 8
    instructions; the 9 ECX-receiving functions read, forward or clobber ECX before use — none stores to
    [ECX+0/4/8]; the one apparent writer FUN_0082B790 clobbers ECX before use and writes only a fresh array).
4. FUN_0082B5A0 (ECX=S; [esp+4]=out — the leftover pair slot; [esp+8]=src; ret 8) computes per component, with the
   x87 stack traced instruction-by-instruction: multiply src by K=(double)(float)0.01 in extended precision, narrow
   to f32 at the temp store [esp+8], subtract S[i], narrow to f32 at the final store into out — and pops the pair's
   8 leftover bytes. The out buffer is the caller's ARG1; FUN_0050A050 then returns that same out pointer.
5. On the fallback path (name==NULL or lookup==NULL) the function copies 3 raw dwords from SF::slot1() =
   &SF+0x34 (FUN_005090A0 'lea eax,[ecx+0x34]; ret' — measured) into out — NO scale, NO origin subtraction;
   SF+0x34 is the placement-record copy slot (writer FUN_005094C0, prior-canon pin re-measured MATCH) and the SF
   constructor seeds it from the SAME global zero triple that seeds S (one origin system).

## HYPOTHESES OUTCOMES (pre-registered; falsifiers unchanged)
- H1 (NiAVObject+0x90 = contiguous world-translation vector): CONFIRMED.
- H2 (FUN_00437F70 materially transfers/transforms the value): REJECTED — 437F70 is an unrelated operation
  (origin-singleton getter; args untouched). The transfer lives in 0x82B5A0.
- H3 (FUN_0082B5A0 finalizes/mutates the primary-path result): CONFIRMED (stronger: it is the sole primary-path
  writer of out).
- H4 (output = named object's world position after deterministic conversion): CONFIRMED (out = world_translate x
  0.01, identity axis order; conversion is the deterministic part).
- H5 (primary and fallback share structural/coordinate semantics): PARTIAL — structure/interface identical
  (CONFIRMED); coordinate-space coherence STRONGLY_SUPPORTED (shared origin seeding + inverse family + prior
  canon) but the stored fallback value's scale is not byte-provable inside this scope fence.

## KEY MEASURED FACTS (each with instruction-level citation in the raw files)
- FUN_0050A050 extent 0x50A050..0x50A0AA (second terminal ret 8 @ 0x50A0A7, 6x int3 padding 0x50A0AA..0x50A0AF
  after, next function starts 0x50A0B0) — pin MATCH;
  all 36 pinned instructions re-measured MATCH (01_RAW/FUN_0050A050_DOWNSTREAM_DISASM.txt [A.3]).
- Push-order/stack mapping (both helpers) derived, not assumed: lookup callee gets name at [esp+4] (ECX=NiNode,
  ret 4); 0x437F70 sees out at [esp+4] & src at [esp+8] but ignores both (plain ret); 0x82B5A0 sees the SAME out at
  [esp+4] & src at [esp+8] (ret 8 pops them). [esp+8] at 0x50A06A re-derived = ARG1 out buffer.
- The required def-use answer: FUN_0050A050 performs ZERO primary-path XYZ writes itself (mov eax,esi / pop esi /
  ret 8 only).
- K = (double)(float)0.01 = 0.009999999776482582 = 0x3F847AE140000000 (qword 0xa7b360); inverse family constant
  100.0 (qword 0xa7a618); array transformer f32 100.0f (0xa7af68).
- Caller censuses: FUN_00437F70 = 99 E8 / 0 E9 / 0 imm32 / no vtable; FUN_0082B5A0 = 36 E8, of which 34 are the
  'call 437F70; mov ecx,eax; call 82B5A0' pair; FUN_0082B580 = 3 callers.
- SEH: 0x437F70 installs an SEH frame (handler 0x99c06b; handler body NOT decoded — recorded, out of load path).
- Allocator identity: 0x95d3c4 = jmp [0xa75354] = MSVCR80.dll!??2@YAPAXI@Z (operator new) via import-dir walk.

## NEGATIVE CONTROL (MANDATORY) — FAILURE_CASE_DETECTED = YES
4 executed controls (01_RAW/NEGATIVE_CONTROL_RAW.txt): (1) the same pair applied to a non-NiAVObject inline 3-float
field (site 0x523C38) => helper identity = generic engine->scaled-space converter, "world position helper" label
REJECTED; (2) fallback vs primary in-slot => "float3 out" shape does not imply copy semantics; (3) sibling
FUN_0082B6A0 ((src+S)*100.0) => byte-shape similarity is not operation identity; (4) mutability probe => "dynamic
origin (camera-relative)" reading REJECTED (no writer exists — correction-pass census 01_RAW/ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt; S is a permanent
zero vector).

## FINDINGS THAT CONTRADICT / SUPERSEDE STANDING LABELS (loud)
1. FUN_00437F70 is NOT a vector helper of any kind — standing-knowledge caution "do NOT inherit semantics of
   either helper" is vindicated and now replaced by: origin-singleton getter. Any prior (informal) "second helper
   of a copy pair" reading is REJECTED by bytes.
2. FUN_0082B5A0 is NOT a copy: it is a scaled-subtraction coordinate conversion; the SF slot3 primary output is
   numerically 100x smaller than the engine translate (0.01 scale, proven bit-exact).
3. The primary path is NOT "the same output semantics as the fallback": the fallback is unscaled raw copy;
   the primary is a live converted world position. Consumers of SF slot3 output must expect the SCALED space
   (this is a load-bearing reconstruction-relevant fact for any world-position use of SceneFeeder data).
4. FUN_0082B790's apparent "[ecx] writes" are a mid-function displacement loop into a FRESH array — ECX (the
   singleton) is clobbered at 0x82B79B before use. Naive write-scan tooling would misclassify it as a singleton
   setter (recorded for the trap library).
5. Package-B pins (slot17=0x7B5390, slot27=0x7E4820, +0x90=m_kWorld translate) all RE-MEASURED MATCH; no
   contradiction to prior canon found.

## STOP CONDITIONS EVALUATION
SUCCESS A: exact primary-path value relation recovered with component-level proof — MET.
SUCCESS B: deterministic transformation fully recovered (scale + origin, bit-exact, with inverse) — MET.
Not expanded further (SUCCESS C/D not needed): no follow-up science; RUNTIME_COORDINATE_BEHAVIOR = UNVERIFIED
recorded honestly (no runtime test invented).

## GATE SUMMARY (full table: 06_REPORT/STAGE_ACCEPTANCE_GATES.csv)
G0 PASS (S0 fail-closed re-verified at run start). G1 PASS (HEAD==BASE_SHA==origin/master==ls-remote; untracked set
= 2 pre-existing + this run dir; zero mutations). G2 PASS (36/36 pin MATCH; stack mapping derived; def-use answer
NO; pseudo-C after decode). G3 PASS (CONFIRMED layout; world vs local distinguished). G4 PASS (extent/ABI/args
measured; reads/writes/SEH/callee identities/census; 10 questions answered). G5 PASS (bit-exact constants; exact
x87 per-component formulas; 7 questions answered). G6 PASS (per-component dataflow with UNKNOWNs localized). G7
PASS. G8 PASS (five fallback-vs-primary questions answered explicitly). G9 PASS (5 context classes). G10 PASS
(4 executed negative controls; FAILURE_CASE_DETECTED=YES). G11 STRONGLY_SUPPORTED (conversion proven; absolute
space label UNVERIFIED). G12 PASS (identity permutation; labels UNVERIFIED statically). G13 PASS (bit-exact scale;
cm->m reading = PLAUSIBLE interpretation). G14 STRONGLY_SUPPORTED (position role corroborated by 2+ independent
consumer classes; absolute confirmation requires runtime trace — not permitted). G15/G16/G17 PENDING (governance).

## HONEST BOUNDARIES (NOT_CHECKED)
- SEH handler body at 0x99c06b not decoded (out of load path).
- RTTI class NAME of the SF class not recoverable (the pre-vtable pointer 0xaa12b8 region is runtime-relocated;
  structural identity from ctor chain + bone-name data used instead).
- Absolute unit semantics of the scaled space; static consumer census of the slot3 virtual dispatch; the fallback
  stored value's scale — all recorded UNVERIFIED with reasons.
- The 0x437E80/0x82B5F0/0x48BAC0 sibling bodies decoded only far enough to classify their S-read/write behavior.
