# HELPER_OPERATIONS — PHASES C+D ANALYSIS (FUN_00437F70, FUN_0082B5A0)
# RUN_ID: PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915 (raw: 01_RAW/FUN_00437F70_DISASM.txt, 01_RAW/FUN_0082B5A0_DISASM.txt)

## FUN_00437F70 (extent 0x437F70..0x437FE7)
- OBSERVED_OPERATION (CONFIRMED): lazy get-or-create of a 12-byte heap singleton S, cached at global slot 0xba1804.
  S = { [0xba921c], [0xba9220], [0xba9224] } at construction — a copy of a global triple that is not written
  within the enumerated channels of the whole-image write census
  (01_RAW/ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt: all 268 imm32 occurrences classified — loads/pushes/getters only,
  0 store-class candidates across every store encoding, 0 widened-overlap and 0 computed-base stores, all
  pointer-consumer channels read-only; .data virtual-tail zero-init) => S's INITIAL value is {0.0, 0.0, 0.0}
  (CONFIRMED). AMEND (origin-mutability correction run PE_935_SF_ORIGIN_MUTABILITY_CORRECTION_R1_20260915):
  the OLD text concluded "=> S == {0.0,0.0,0.0} at ALL times, immutable" — RETRACTED: that inference was invalid
  (the triple-address census does not cover writes through the getter-returned singleton pointer). The correction
  run's write-through census (01_RAW/ORIGIN_SINGLETON_WRITE_THROUGH_CENSUS.csv) measured the getter-return
  consumers: writer site 0x458E27 (three f32 stores through the returned pointer at offsets 0/4/8; setter decode
  01_RAW/ORIGIN_SETTER_458D90_DISASM.txt) => ORIGIN_MUTATION_CHANNEL_EXISTS = CONFIRMED; ORIGIN_MUTATED_AT_RUNTIME
  and ORIGIN_RUNTIME_VALUE = UNVERIFIED (STATIC-ONLY); status algebra:
  02_ANALYSIS/ORIGIN_STATUS_CORRECTION.md.
  Alloc path: `operator new(12)` (thunk 0x95d3c4 = jmp [IAT 0xa75354] = MSVCR80.dll!??2@YAPAXI@Z, import-dir walk
  measured); ctor 0x82B580 copies the triple; alloc-fail NULLs the slot and returns NULL.
  ABI: PLAIN 'ret' at both terminals — consumes ZERO stack args; the caller's 8 leftover bytes (out, src) are
  INVISIBLE to it and remain for the second helper. SEH frame installed (handler 0x99c06b; body NOT decoded —
  outside the load path, recorded NOT_DECODED).
- FUNCTION_IDENTITY: origin/zero-vector singleton getter ("GetWorldOrigin"). NOT a vector copy, NOT a transform.
- FINAL_SEMANTIC_ROLE (context): supplies the additive origin for the coordinate-conversion family (primary pair
  and siblings 0x82B6A0/0x82B5F0/0x437E80).
- CALLER CENSUS: 99 E8 sites (0 E9, 0 imm32, 0 vtable); 34 are the PAIR with 0x82B5A0 (incl. SF slot3 0x50A075);
  other ECX-consumer targets measured (0x82b6a0 x7, 0x437e80 x8, 0x48bac0 x6, 0x82b790 x4, 0x82b870 x2, 0x82b5f0 x2,
  0x58e4b0 x1, 0x58e520 x2; remainder use EAX-adjacent FPU/other patterns). AMEND (origin-mutability correction):
  the OLD text claimed "No caller writes through the return" — RETRACTED: writer site 0x458E27 exists (see above);
  the census instrument had recorded this site's instruction_after_next='mov dword ptr [eax], edx' without
  interpreting write-through.

## FUN_0082B5A0 (extent 0x82B5A0..0x82B5F0)
- OBSERVED_OPERATION (CONFIRMED): per-component scaled subtraction
  out[i] = f32( f32( src[i] * K ) - base[i] ), K = qword [0xa7b360] = (double)(float)0.01 = 0.009999999776482582
  (0x3F847AE140000000), base = ECX = S (S's initial value is measured {0,0,0}; AMEND, origin-mutability
  correction: the unconditional '= {0,0,0}' reading of the base is retracted — the SUBTRACTION is unconditional
  in the bytes; the base's VALUE is a separate status, see 02_ANALYSIS/ORIGIN_STATUS_CORRECTION.md and the
  independent re-derivation 01_RAW/OUTPUT_FORMULA_REVALIDATION_RAW.txt). Two f32 narrowings per component (temp
  store at [esp+8] then the final store); x87 extended-precision inter-stage arithmetic; no clamps, no branches,
  no writes outside out[0..8].
  ABI: ECX + 2 stack args, 'ret 8' (cleans the pair's leftover args at the SF site). ECX = S at ALL 34 pair sites
  (identical 'mov ecx,eax' construction, measured).
- FUNCTION_IDENTITY: forward engine->scaled-space 3-float converter ("ScaledSubWithOrigin"), NOT a plain copy and
  NOT a world-position getter per se (NEGATIVE_CONTROL_RAW.txt Control 1).
- FINAL_SEMANTIC_ROLE (context): in the SF slot3 primary path it converts the named NiAVObject's m_kWorld translate
  into the 0.01-scaled internal space; the inverse exists as 0x82B6A0 = (src + S) * 100.0 using qword [0xa7a618]
  = (double)100.0 — a matched forward/inverse family.

## THE 10 / 7 CONTRACT QUESTIONS
All answered from bytes in the raw files (FUN_00437F70_DISASM.txt [C.9] items 1-10; FUN_0082B5A0_DISASM.txt [D.7]
items 1-7). Highlights: 437F70 ignores both stack args and returns the origin singleton; 82B5A0 is the sole writer of
the primary-path out buffer, transforms coordinate space (scale 0.01 + origin), mutates nothing else, performs no
clamp/validate/cache work.

## H2 / H3 evaluation
- H2 ("FUN_00437F70 materially transfers/transforms the 3-component value from NiAVObject+0x90 toward the output
  buffer"): REJECTED — measured decode proves 437F70 performs an UNRELATED operation (singleton get-or-create;
  both stack args untouched; zero float data movement). The material transfer happens in 0x82B5A0.
- H3 ("FUN_0082B5A0 participates in finalizing or mutating the primary-path position result"): CONFIRMED in the
  stronger form — 0x82B5A0 IS the entire primary-path output computation (the only writer of the out buffer).
  Its specific operation is a deterministic K=0.01 scale conversion with base subtraction; a 100:1 magnitude
  relation holds only IF the base S == {0,0,0} (AMEND, origin-mutability correction: the unconditional
  "(origin == 0)" reading is retracted; the general formula out = f32(f32(W*K) - S) is the measured relation —
  see 02_ANALYSIS/ORIGIN_STATUS_CORRECTION.md).
