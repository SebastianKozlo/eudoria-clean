# SUPERSESSION_LEDGER — PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_C1_REPORT_SCOPE_CORRECTION_R1_20261004

Governance form: **superseded statement → supersession finding → corrected
canonical interpretation.** The superseded statements are from the R1 package
`PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004` (published at commit
25335a28ee61fc2a8c7763f41552df85af45d067), its AUDIT_ENTRYPOINT.md row, and the
external review input it echoed. Historical files were NOT edited (READ-ONLY;
git history preserves every published state; `git status` at this run's start
confirmed zero tracked-file modifications). This ledger IS the supersession
record — nothing was silently rewritten. The corrected readings live in THIS
package's FINAL_REPORT/QC_REPORT/HANDOFF and in the one NEW AUDIT_ENTRYPOINT.md
row added by this run (the historical R1 row is untouched history).

QUOTING DISCIPLINE: every quote below is an **ORIGINAL_EXCERPT** — a faithful
reproduction of historical wording with the original line folds shown. The term
"verbatim" is deliberately NOT used. Each excerpt was machine-verified
(03_SCRIPTS/qc_correction_c1.py `quotecheck`) to be a whitespace-normalized
contiguous substring of its named SOURCE_FILE at BASE_SHA 25335a2 — no quote is
fabricated and none is assigned to a file where it is absent
(01_RAW/QC_LEDGER_QUOTE_CHECKS.json). Historical false wording inside these
clearly-identified ORIGINAL_EXCERPTs is evidence, not an active claim.

Findings source: the independent Desktop post-audit
`PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_DESKTOP_POST_AUDIT_20261004`
(REPORT.md, SHA256 B433828F...) — verdict
REQUIRE_CORRECTIONS_IN_REPORT_QC_HANDOFF_SCOPE, findings GP1/P2, GP2/P2, GP3/P2
and the FUNCTION_BUDGET_OVERRUN process finding — re-verified byte-identical to
the dispatch pins by this run (01_RAW/QC_CORRECTION_BATTERY.json A1/A2).

---

## GP1 — STORAGE != ULTIMATE SOURCE; creation timing not closed

FINDING_ID: **GP1_SOURCE_EXCLUSION_AND_CREATION_TIMING**

### Row S-GP1-1 — the external review's "NOT static data" source-exclusion wording
- SOURCE_FILE: `C:\Users\User\Documents\ChatGPT\PE\PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_DESKTOP_POST_AUDIT_20261004\PE_MASTER_REVIEW_INPUT.txt` (line 105)
- ORIGINAL_EXCERPT (external review, NOT a repo file; Polish):
  ```
  Wartość-klucz lookup FUN_0072F880 używana przez builder FUN_00567770 **pochodzi z per-instance mutable state, NIE ze statycznych danych** — to jest istotny i uczciwy wynik S1.
  ```
- CORRECTED_CLAIM: the IMMEDIATE STORAGE half of that sentence is correct and
  preserved (IMMEDIATE_VALUE_STORAGE = PER_RECEIVER_COMPONENT_VALUE_TABLE);
  the EXCLUSION half ("NIE ze statycznych danych" = "NOT from static data")
  is superseded: ULTIMATE_VALUE_SOURCE = UNKNOWN; FILE_DERIVED_VALUE_EXCLUDED =
  NO. The location where the value is read (the per-receiver component value
  table) does not identify its ultimate producer; a runtime table can be
  populated from a file, a constant, a computation, a cache, or a message, and
  the R1 evidence excludes none of these classes.
- STATUS: SUPERSEDED (the source-exclusion reading only; the storage-identity
  statement preserved).
- WHY: storage != ultimate source; the Desktop GP1 finding (REPORT.md lines
  47-55): "Ustalono miejsce odczytu wartości. Nie ustalono jej ostatecznego
  producenta ani źródła." — no source class may be excluded without evidence.

### Row S-GP1-2 — the external review's "NOT the static 16083 / not RECORD_A" exclusion wording
- SOURCE_FILE: `C:\Users\User\Documents\ChatGPT\PE\PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_DESKTOP_POST_AUDIT_20261004\PE_MASTER_REVIEW_INPUT.txt` (lines 78-81)
- ORIGINAL_EXCERPT (external review, NOT a repo file; Polish):
  ```
  Kluczowa korekta epistemiczna utrwalona: klucz buildera
                     FUN_00567770 to NIE jest statyczne 16083 z templates.vfs — to wartość per-instance
                     mutable state (init 0, realne klucze z nieustalonego writera). To obniża (zgodnie z
                     prawdą) oczekiwanie, że transform placement odbuduje się wprost z RECORD_A.
  ```
- CORRECTED_CLAIM: what remains byte-proven is only the NARROW negative: NO
  hardcoded 16083 literal exists in the audited getter path (R1 decode; not
  re-measured this run). The wider exclusion reading is superseded: the actual
  runtime value is NOT established to be non-16083, NOT established to be
  16083, and NOT proven disjoint from templates.vfs/RECORD_A. Corrected fields:
  ULTIMATE_VALUE_SOURCE = UNKNOWN; FILE_DERIVED_VALUE_EXCLUDED = NO;
  RECORD_A_RELATION = NOT_ESTABLISHED (neither established nor excluded);
  PHYSICAL_SOURCE_RECORD_ID = NOT_ESTABLISHED. The "lowered expectation that
  transform placement rebuilds directly from RECORD_A" stands only as an
  expectation statement, NOT as a proven impossibility.
- STATUS: SUPERSEDED (the exclusion reading; the no-hardcoded-16083-in-the-
  audited-getter-path negative and the init-0/producer-UNRESOLVED statements
  preserved).
- WHY: proven absence of a hardcoded literal != proven absence of a
  file/record-derived or computed origin; the nonzero-value producer and its
  timing are UNRESOLVED (Desktop REPORT.md lines 55, 68).

### Row S-GP1-3 — R1 FINAL_REPORT universal creation-timing claim
- SOURCE_FILE: `docs/audits/PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004/FINAL_REPORT.md` (lines 39-42)
- ORIGINAL_EXCERPT:
  ```
  3. **The actual runtime value = RUNTIME-MUTABLE PER-INSTANCE STATE with
     UNKNOWN producer (UNRESOLVED within budget).** The initial 0 can never
     be a consumed key (FUN_004C5580 aborts on TEST EAX,EAX → JE 0x004C5AB6),
     so any real lookup key was written into table[10] after creation.
  ```
- CORRECTED_CLAIM: the audited DEFAULT creation path (FUN_0070D990 → int
  traits vtable 0x00A9C670 slot 1 = FUN_009777E0 `MOV DWORD [EAX],0`,
  re-verified this run, battery E1/E2) has byte-confirmed ZERO initialization
  for the audited int value — DEFAULT_CREATION_PATH_INITIAL_VALUE = 0 — and
  the zero-abort fact stands (a zero key is never consumed). The universal
  inference "any real lookup key was written into table[10] after creation"
  is superseded: NONZERO_VALUE_PRODUCER = UNRESOLVED;
  NONZERO_VALUE_PRODUCER_TIMING = UNRESOLVED. The default creation path's
  zero init does NOT establish that all possible creation/population paths
  first complete with zero and are modified only afterward — the cache-miss
  creator FUN_0070DE10 has an early path (candidate A: FUN_0070DCF0 →
  record-apply FUN_0070DC20) whose completion/population order was never
  decoded, so no common completion moment is proven.
- STATUS: SUPERSEDED (the universal timing inference; the storage identity,
  the scoped initial-0 fact and the zero-abort fact preserved).
- WHY: the audited initialization path is not a closed list of all
  creation/population paths (Desktop REPORT.md lines 57, 68: the
  FUN_0070DE10 path may return a result of FUN_0070DCF0/undecoded
  FUN_0070DC20 — no common post-creation timing was proven).

### Row S-GP1-4 — R1 PRODUCER_PROVIDER_CHAIN universal creation-timing claim
- SOURCE_FILE: `docs/audits/PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004/PRODUCER_PROVIDER_CHAIN.md` (lines 22-25)
- ORIGINAL_EXCERPT:
  ```
  The initial 0 can never be a consumed key: FUN_004C5580 aborts at
  TEST EAX,EAX / JE 0x004C5AB6 @0x004C55BD/0x004C55C3 when the getter returns 0.
  Therefore any REAL lookup key on the audited path was written into
  table[10] AFTER class_obj creation, by a per-instance value writer.
  ```
- CORRECTED_CLAIM: identical to S-GP1-3, plus: the "by a per-instance value
  writer" identity/timing assertion is superseded — the writer of the nonzero
  value is UNRESOLVED (candidate A: FUN_0070DCF0 → FUN_0070DC20 record-apply
  lead remains an unresolved lead; candidate B: the factory+0x80 delegate
  bind; neither decoded to conclusion, neither promoted).
- STATUS: SUPERSEDED (the "AFTER class_obj creation" universal + the writer
  identity assertion; the zero-abort fact and the table[10] storage identity
  preserved).
- WHY: same as S-GP1-3.

### Row S-GP1-5 — the R1 AUDIT_ENTRYPOINT row's "later per-instance value writer" wording
- SOURCE_FILE: `AUDIT_ENTRYPOINT.md` (LATEST RUNS row of the R1 package — historical row, NOT edited by this run)
- ORIGINAL_EXCERPT:
  ```
  so real keys come from a later per-instance value writer NOT identified within the budget
  ```
- CORRECTED_CLAIM: "later" is superseded as a universal; corrected fields
  NONZERO_VALUE_PRODUCER = UNRESOLVED and NONZERO_VALUE_PRODUCER_TIMING =
  UNRESOLVED; only the DEFAULT-path initial value is established (= 0). The
  corrected reading is carried by THIS package's new AUDIT_ENTRYPOINT row and
  this ledger.
- STATUS: SUPERSEDED (the timing word "later"; the producer-UNRESOLVED
  statement preserved).
- WHY: same as S-GP1-3.

---

## GP2 — the alternative does NOT bypass the shared FUN_0072F880 lookup

FINDING_ID: **GP2_ALTERNATIVE_BRANCH_LOOKUP_BYPASS**

### Row S-GP2-1 — ALTERNATIVE_BRANCH "NEVER consults ... FUN_0072F880"
- SOURCE_FILE: `docs/audits/PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004/ALTERNATIVE_BRANCH.md` (lines 41-46)
- ORIGINAL_EXCERPT:
  ```
  0x004C5516: JMP 0x004C5550        ← SUB-OUTCOME 2: the function RETURNS
                                       FUN_00843340's result (ESI=EAX at the
                                       convergence point 0x004C5550), i.e. a
                                       DIFFERENT template source that NEVER
                                       consults the tag-6 getter, the value
                                       table, or FUN_0072F880.
  ```
- CORRECTED_CLAIM (byte re-verified this run, battery C1-C11): the
  alternative's result flows: CALL FUN_00843340 @0x004C550E (E8 2D DE 37 00 →
  0x00843340, result in EAX) → ADD ESP,4 @0x004C5513 → JMP @0x004C5516
  (EB 38) → 0x004C5550 → MOV ESI,EAX @0x004C5550 (8B F0) → cleanup CALL
  FUN_00703BC0 @0x004C555E → MOV EAX,ESI @0x004C5563 (8B C6) → return to the
  SHARED caller FUN_004C5580 (its call site @0x004C55B5) → TEST EAX,EAX
  @0x004C55BD (85 C0): result==0 → JE 0x004C5AB6 @0x004C55C3 (0F 84 ED 04 00
  00) aborts BEFORE the lookup; result!=0 → PUSH ESI @0x004C55D0, PUSH EAX
  @0x004C55D1 (50) → CALL FUN_0072F880 @0x004C55D9. Corrected semantics:
  ALTERNATIVE_TAG6_SEGMENT = BYPASSED (the tag-6 getter and the value table
  are bypassed on this segment — that part of the historical claim is
  correct); ALTERNATIVE_SHARED_LOOKUP = CONDITIONAL_ON_NONZERO_RESULT (the
  SAME caller conditionally feeds the result to the SAME FUN_0072F880
  lookup); FUN_00843340_RESULT_SEMANTIC = UNKNOWN;
  FUN_00843340_RESULT_TO_LOOKUP_KEY = CONFIRMED_CONDITIONAL_ON_NONZERO.
- STATUS: SUPERSEDED (the "NEVER consults ... FUN_0072F880" claim; the
  tag-6-getter/value-table bypass-segment claim preserved).
- WHY: physical countercheck (Desktop REPORT.md GP2 lines 80-93, re-verified
  by this run's battery): the alternative does NOT bypass FUN_004C5580's
  zero-test and conditional FUN_0072F880 lookup.

### Row S-GP2-2 — ALTERNATIVE_BRANCH "template object" semantic
- SOURCE_FILE: `docs/audits/PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004/ALTERNATIVE_BRANCH.md` (lines 57-58)
- ORIGINAL_EXCERPT:
  ```
     - Sub-outcome 2 (FUN_007292F0 FALSE) bypasses the entire audited chain and
       returns FUN_00843340([entity]) directly as the "template object".
  ```
- CORRECTED_CLAIM: FUN_00843340's result semantic is UNKNOWN — FUN_00843340 was
  NOT decoded (and is NOT decoded by this correction either; scope guard). In
  this path the result is consumed, when nonzero, as the FUN_0072F880 lookup
  key by the shared caller; it is NOT established to be a template object,
  and "bypasses the entire audited chain" is superseded to "bypasses the
  tag-6 getter/value-table segment" (the shared caller's zero-test and
  conditional lookup still run).
- STATUS: SUPERSEDED (the "template object" label + the "entire audited
  chain" reading).
- WHY: no decode supports a template-object semantic; the physical flow shows
  lookup-key consumption (battery C1-C11).

### Row S-GP2-3 — R1 HANDOFF "a different template source entirely"
- SOURCE_FILE: `docs/audits/PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004/HANDOFF.md` (lines 44-46)
- ORIGINAL_EXCERPT:
  ```
  - The 0xD82 alternative CONVERGES with the normal branch when
    FUN_007292F0(resolved) is TRUE (its FALSE sub-path returns
    FUN_00843340([entity]) — a different template source entirely).
  ```
- CORRECTED_CLAIM: the FALSE sub-path returns FUN_00843340([entity]) TO THE
  SHARED CALLER FUN_004C5580, which aborts on zero and otherwise uses the
  result as the SAME FUN_0072F880 lookup key
  (FUN_00843340_RESULT_TO_LOOKUP_KEY = CONFIRMED_CONDITIONAL_ON_NONZERO);
  "a different template source entirely" is superseded
  (FUN_00843340_RESULT_SEMANTIC = UNKNOWN). The sub-outcome-1 CONVERGES
  statement is preserved.
- STATUS: SUPERSEDED (the "different template source" semantic + the implicit
  full-bypass reading; the convergence statement preserved).
- WHY: same as S-GP2-1.

### Row S-GP2-4 — the R1 AUDIT_ENTRYPOINT row's alternative wording
- SOURCE_FILE: `AUDIT_ENTRYPOINT.md` (LATEST RUNS row of the R1 package — historical row, NOT edited by this run)
- ORIGINAL_EXCERPT:
  ```
  the 0xD82 alternative CONVERGES with the normal branch when FUN_007292F0(resolved) is TRUE and returns FUN_00843340([entity]) otherwise
  ```
- CORRECTED_CLAIM: "returns FUN_00843340([entity]) otherwise" is superseded to:
  returns it to the shared caller FUN_004C5580, where a zero result aborts
  before the lookup and a nonzero result is used as the SAME FUN_0072F880 key
  (CONDITIONAL_ON_NONZERO_RESULT). Corrected reading carried by THIS
  package's new AUDIT_ENTRYPOINT row.
- STATUS: SUPERSEDED (the incomplete flow description).
- WHY: same as S-GP2-1.

---

## GP3 — static initial zero != lifetime immutability

FINDING_ID: **GP3_STATIC_FALLBACK_LIFETIME_IMMUTABILITY**

Measured scope re-verified by this run (battery D1-D6): BOTH statics
0x00BA5108 (the out-of-range default slot) and 0x00BA9374 (the fallback slot
object) lie in the .data VIRTUAL TAIL — .data vsize 0x3D7A4 > rawsize 0x34000;
both RVAs are beyond the raw data, so both read as ZEROS AT IMAGE MAPPING.
The SAME direct-literal .text census the R1 S5 instrument performed was
re-measured: 0x00BA9374 has exactly ONE .text literal occurrence — the
MOV EAX,imm32 LOAD at 0x00977781 (B8 74 93 BA 00 C3 = FUN_00977780); 0x00BA5108
has TWO — the MOV EAX,imm32 LOAD at 0x0070C1E0 (FUN_0070C180's default-slot
return) and one RAW byte-pattern hit at 0x005246B9 (a coincidental operand
interior, not an instruction using the literal); ZERO direct-store forms for
both. DIRECT_LITERAL_STORE_FOUND_IN_MEASURED_SCAN = NO.

### Row S-GP3-1 — R1 FINAL_REPORT terminal field "permanently-zero static"
- SOURCE_FILE: `docs/audits/PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004/FINAL_REPORT.md` (line 90)
- ORIGINAL_EXCERPT:
  ```
  FALLBACK_BRANCH_PROVENANCE = STATIC_FALLBACK (permanently-zero static 0x00BA9374 -> NULL getter result -> no key)
  ```
- CORRECTED_CLAIM: FALLBACK_STATIC_INITIAL_CONTENT = ZERO_AT_IMAGE_MAPPING;
  DIRECT_LITERAL_STORE_FOUND_IN_MEASURED_SCAN = NO;
  FALLBACK_STATIC_LIFETIME_IMMUTABILITY = NOT_ESTABLISHED;
  ZERO_RETURN_TO_LOOKUP_ABORT = CONFIRMED_CONDITIONAL (IF the fallback-loaded
  value is zero THEN FUN_004C5580 aborts before FUN_0072F880). The census
  covers literal address occurrences/direct-address forms ONLY — it does NOT
  exclude alias writes, pointer-derived writes, caller writes through
  returned pointers, bulk writes, or other indirect mutation; BOTH statics
  are RETURNED AS POINTERS (FUN_00977780 returns 0x00BA9374; FUN_0070C180's
  default path returns 0x00BA5108), so a caller can read/write through [reg]
  with no literal address anywhere in .text.
- STATUS: SUPERSEDED (the "permanently-zero" lifetime claim; the measured
  initial-zero and census facts preserved).
- WHY: initial zero + absence of direct literal stores != lifetime
  immutability (Desktop REPORT.md GP3 lines 101-109, including the synthetic
  method counterexample proving the census insufficient for a lifetime claim).

### Row S-GP3-2 — R1 GETTER_CHAIN 0x00BA5108 "permanently ZERO — no writers"
- SOURCE_FILE: `docs/audits/PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004/GETTER_CHAIN.md` (lines 58-59)
- ORIGINAL_EXCERPT:
  ```
       │   │      count = ([factory+0x8C]-[factory+0x88])>>4; out-of-range →
       │   │      static default slot 0x00BA5108 (permanently ZERO — no writers)
  ```
- CORRECTED_CLAIM: identical GP3 corrected fields (see S-GP3-1 preamble);
  "permanently ZERO — no writers" is superseded by ZERO_AT_IMAGE_MAPPING +
  DIRECT_LITERAL_STORE_FOUND_IN_MEASURED_SCAN=NO (measured scope) +
  FALLBACK_STATIC_LIFETIME_IMMUTABILITY=NOT_ESTABLISHED.
- STATUS: SUPERSEDED (the lifetime wording; the out-of-range default-slot
  addressing fact preserved).
- WHY: same as S-GP3-1.

### Row S-GP3-3 — R1 GETTER_CHAIN 0x00BA9374 "(no writers, .data virtual tail)"
- SOURCE_FILE: `docs/audits/PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004/GETTER_CHAIN.md` (lines 75-76)
- ORIGINAL_EXCERPT:
  ```
       │   │    (fallback @0x004C5549: CALL FUN_00977780 → MOV EAX,0x00BA9374;RET
       │   │     → [0x00BA9374] = 0 (no writers, .data virtual tail) → returns 0)
  ```
- CORRECTED_CLAIM: "[0x00BA9374] = 0" is superseded to "ZERO_AT_IMAGE_MAPPING"
  (initial content); "no writers" is superseded to the measured-scope statement
  DIRECT_LITERAL_STORE_FOUND_IN_MEASURED_SCAN = NO with
  FALLBACK_STATIC_LIFETIME_IMMUTABILITY = NOT_ESTABLISHED; "→ returns 0" is
  superseded to the CONDITIONAL: returns 0 IF the mapped initial content is
  still zero at read time; ZERO_RETURN_TO_LOOKUP_ABORT = CONFIRMED_CONDITIONAL.
- STATUS: SUPERSEDED (the unqualified "= 0 / no writers / returns 0" runtime
  statements; the fallback addressing/call facts preserved).
- WHY: same as S-GP3-1.

### Row S-GP3-4 — R1 ALTERNATIVE_BRANCH "a permanently-zero static object"
- SOURCE_FILE: `docs/audits/PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004/ALTERNATIVE_BRANCH.md` (lines 62-68)
- ORIGINAL_EXCERPT:
  ```
  3. FALLBACK_BRANCH_PROVENANCE (the descriptor-invalid path @0x004C5549, also
     reached from the normal branch itself): CALL FUN_00977780 → `MOV EAX,
     0x00BA9374; RET` → MOV EAX,[EAX] @0x004C554E reads [0x00BA9374] — the
     .data VIRTUAL TAIL with ZERO direct .text writers (census in
     01_RAW/S5_CREATOR_DECODE.json) → NULL → FUN_004C5580 aborts at
     JE 0x004C5AB6. Classification: STATIC_FALLBACK (a permanently-zero static
     object; produces NO lookup key, only a NULL getter result).
  ```
- CORRECTED_CLAIM: "ZERO direct .text writers (census in 01_RAW/
  S5_CREATOR_DECODE.json)" is preserved AS THE MEASURED CENSUS SCOPE (direct
  literal store forms: none found — re-measured this run, D6). The
  classification parenthetical is superseded: "a permanently-zero static
  object" → ZERO_AT_IMAGE_MAPPING + FALLBACK_STATIC_LIFETIME_IMMUTABILITY =
  NOT_ESTABLISHED; "produces NO lookup key, only a NULL getter result" →
  ZERO_RETURN_TO_LOOKUP_ABORT = CONFIRMED_CONDITIONAL (IF the loaded value is
  zero THEN NULL result and abort before FUN_0072F880).
- STATUS: SUPERSEDED (the lifetime classification wording; the measured
  direct-literal census and the zero→abort conditional preserved).
- WHY: same as S-GP3-1.

### Row S-GP3-5 — R1 CONTROL_CASE 0x00BA5108 "PERMANENTLY ZERO — no writers"
- SOURCE_FILE: `docs/audits/PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004/CONTROL_CASE.md` (lines 40-44)
- ORIGINAL_EXCERPT:
  ```
  **Design.** The fallback path of the getter machinery (descriptor invalid:
  kind==0, kind!=1, or flags bit0 set; also the out-of-range default slot
  0x00BA5108 which is PERMANENTLY ZERO — no writers, .data virtual tail,
  census in 01_RAW/S5_CREATOR_DECODE.json) must NOT be conflated with a
  successful getter result.
  ```
- CORRECTED_CLAIM: CONTROL C's DESIGN is preserved; its wording is NARROWED
  per the correction contract to: IF the fallback-loaded value is zero THEN
  FUN_004C5580 aborts before FUN_0072F880 (ZERO_RETURN_TO_LOOKUP_ABORT =
  CONFIRMED_CONDITIONAL). The static's "PERMANENTLY ZERO" lifetime wording is
  superseded by ZERO_AT_IMAGE_MAPPING + DIRECT_LITERAL_STORE_FOUND_IN_
  MEASURED_SCAN=NO + FALLBACK_STATIC_LIFETIME_IMMUTABILITY=NOT_ESTABLISHED.
  No claim is made that the value must remain zero for the process lifetime.
- STATUS: SUPERSEDED (the lifetime wording; the control's discrimination
  design preserved, narrowed).
- WHY: same as S-GP3-1.

### Row S-GP3-6 — R1 CONTROL_CASE 0x00BA9374 "dword is 0 at runtime" + "never called"
- SOURCE_FILE: `docs/audits/PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004/CONTROL_CASE.md` (lines 49-55)
- ORIGINAL_EXCERPT:
  ```
  - [0x00BA9374] has ZERO .text writers (the only .text reference is the
    MOV EAX above) → the virtual-tail dword is 0 at runtime.
  - Therefore the fallback converges at 0x004C554E with EAX=0x00BA9374,
    reads 0, and FUN_004C5480 returns NULL.
  - `0F 84 ED 04 00 00` @0x004C55C3 — TEST EAX,EAX; JE 0x004C5AB6 (machine
    -verified target): a NULL getter result ABORTS the lookup — FUN_0072F880
    is never called, NO key is produced.
  ```
- CORRECTED_CLAIM: "ZERO .text writers" is preserved as the MEASURED
  direct-literal census scope (the only .text literal occurrence is the MOV
  EAX,imm32 load — re-verified, D6). "the virtual-tail dword is 0 at runtime"
  is superseded: the dword is ZERO_AT_IMAGE_MAPPING;
  FALLBACK_STATIC_LIFETIME_IMMUTABILITY = NOT_ESTABLISHED. "reads 0" and
  "FUN_0072F880 is never called" are superseded to CONDITIONALS: the fallback
  reads 0 IF the static still holds its mapped initial content, and the
  lookup is skipped IF the result is zero (ZERO_RETURN_TO_LOOKUP_ABORT =
  CONFIRMED_CONDITIONAL). The JE target arithmetic (0x004C5AB6) is preserved
  (re-verified, battery C8).
- STATUS: SUPERSEDED (the unconditional runtime-zero/never-called statements;
  the census-scope fact, the JE pin and the control's conditional
  discrimination preserved).
- WHY: same as S-GP3-1.

### Row S-GP3-7 — R1 HANDOFF "permanently-zero static 0x00BA9374"
- SOURCE_FILE: `docs/audits/PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004/HANDOFF.md` (line 43)
- ORIGINAL_EXCERPT:
  ```
  - The fallback branch produces NO key (permanently-zero static 0x00BA9374).
  ```
- CORRECTED_CLAIM: IF the fallback-loaded value is zero THEN no key is
  produced (ZERO_RETURN_TO_LOOKUP_ABORT = CONFIRMED_CONDITIONAL); the static
  is ZERO_AT_IMAGE_MAPPING with FALLBACK_STATIC_LIFETIME_IMMUTABILITY =
  NOT_ESTABLISHED.
- STATUS: SUPERSEDED (the "permanently-zero" parenthetical; the zero→no-key
  conditional preserved).
- WHY: same as S-GP3-1.

### Row S-GP3-8 — R1 PROVENANCE_CHAIN.csv lifetime wording marked CONFIRMED
- SOURCE_FILE: `docs/audits/PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004/PROVENANCE_CHAIN.csv` (rows 31 and 41)
- ORIGINAL_EXCERPT (two rows):
  ```
  31,slot getter FUN_0070C180,0x0070C180,function,&[factory+0x88][tag*16]; 16-byte slots; default 0x00BA5108 (permanently zero),CONFIRMED
  ```
  ```
  41,fallback static object,0x00BA9374,static,returned by FUN_00977780; permanently ZERO (no writers),CONFIRMED
  ```
- CORRECTED_CLAIM: the CONFIRMED evidence status attached to the
  "permanently zero (no writers)" wording is superseded: CONFIRMED attaches
  only to the measured facts (FUN_0070C180's out-of-range default returns the
  slot VA 0x00BA5108 — battery D5; FUN_00977780 returns 0x00BA9374 — battery
  D2; ZERO_AT_IMAGE_MAPPING initial content — battery D1;
  DIRECT_LITERAL_STORE_FOUND_IN_MEASURED_SCAN=NO — battery D6);
  FALLBACK_STATIC_LIFETIME_IMMUTABILITY = NOT_ESTABLISHED.
- STATUS: SUPERSEDED (the lifetime wording and its CONFIRMED status; the
  addressing/existence facts preserved as CONFIRMED).
- WHY: the evidence status exceeded the measured scope (Desktop GP3).

### Row S-GP3-9 — the R1 AUDIT_ENTRYPOINT row's statics wording
- SOURCE_FILE: `AUDIT_ENTRYPOINT.md` (LATEST RUNS row of the R1 package — historical row, NOT edited by this run)
- ORIGINAL_EXCERPT (two fragments of the row):
  ```
  out-of-range default 0x00BA5108 = permanently-zero .data virtual tail
  ```
  ```
  fallback branch = STATIC_FALLBACK (FUN_00977780 → 0x00BA9374, zero writers → NULL → no key)
  ```
- CORRECTED_CLAIM: "permanently-zero" → ZERO_AT_IMAGE_MAPPING +
  FALLBACK_STATIC_LIFETIME_IMMUTABILITY=NOT_ESTABLISHED; "zero writers" →
  DIRECT_LITERAL_STORE_FOUND_IN_MEASURED_SCAN=NO (measured scope);
  "NULL → no key" → CONFIRMED_CONDITIONAL on the loaded value being zero.
  Corrected reading carried by THIS package's new AUDIT_ENTRYPOINT row.
- STATUS: SUPERSEDED (the lifetime wording; the fallback-path structure
  preserved).
- WHY: same as S-GP3-1.

---

## PROCESS_BUDGET — the 28 > 20 overrun is a disclosed violation, not a contract-conformant stop

FINDING_ID: **FUNCTION_BUDGET_OVERRUN** (P2-PROCESS)

Preserved factual measurement (unchanged): MAX_NEW_FUNCTIONS_AUTHORIZED = 20;
ACTUAL_DETAILED_COUNT = 28. The R1 contract's rule was to stop before the
count WOULD exceed 20; the run continued to 28. Corrected canonical wording:
FUNCTION_BUDGET_OVERRUN = BUDGET_OVERRUN_DISCLOSED. The authorized function
budget was VIOLATED; the later STOP_RE_AND_FINALIZE did NOT retroactively
cure the violation; valid byte evidence is preserved and no scientific result
is upgraded because of work performed outside the authorized budget; future
science contracts require a hard pre-check BEFORE entering function N+1; THIS
correction does NOT retroactively make the original run budget-compliant.

### Row S-BUDGET-1 — R1 FINAL_REPORT honest-boundaries item 2
- SOURCE_FILE: `docs/audits/PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004/FINAL_REPORT.md` (lines 164-165)
- ORIGINAL_EXCERPT:
  ```
  2. The budget was exceeded — the run stopped at the value-writer boundary
     per contract; FIRST_MISSING_EDGE honestly = FUNCTION_BUDGET_EXHAUSTED.
  ```
- CORRECTED_CLAIM: FUNCTION_BUDGET_OVERRUN = BUDGET_OVERRUN_DISCLOSED (see
  preamble). "Stopped ... per contract" is superseded: the stop at 28 was NOT
  per contract; the FIRST_MISSING_EDGE record itself is preserved.
- STATUS: SUPERSEDED (the "per contract" stop wording; the 28>20 measurement
  and the FIRST_MISSING_EDGE record preserved).
- WHY: the contract's stop rule was breached at function 21; stopping later
  at 28 does not conform to it (Desktop REPORT.md lines 121-127).

### Row S-BUDGET-2 — R1 QC_REPORT honest-boundaries item 2
- SOURCE_FILE: `docs/audits/PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004/QC_REPORT.md` (lines 94-96)
- ORIGINAL_EXCERPT:
  ```
  2. The budget was EXCEEDED (28 detailed functions > MAX 20) — the run
     stopped RE at the value-writer boundary per contract, honestly recorded
     as FIRST_MISSING_EDGE=FUNCTION_BUDGET_EXHAUSTED.
  ```
- CORRECTED_CLAIM: identical to S-BUDGET-1.
- STATUS: SUPERSEDED (the "per contract" stop wording).
- WHY: same as S-BUDGET-1.

### Row S-BUDGET-3 — R1 HANDOFF deviations wording
- SOURCE_FILE: `docs/audits/PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004/HANDOFF.md` (lines 61-64)
- ORIGINAL_EXCERPT:
  ```
  - The function budget was EXCEEDED (28 detailed functions) — the run stopped
    RE at the value-writer boundary per the contract's STOP_RE_AND_FINALIZE
    rule; FIRST_MISSING_EDGE=FUNCTION_BUDGET_EXHAUSTED is reported honestly
    alongside the underlying science edge.
  ```
- CORRECTED_CLAIM: identical to S-BUDGET-1 (the stop is a DISCLOSED VIOLATION
  of the budget rule, not an execution of it).
- STATUS: SUPERSEDED (the "per the contract's STOP_RE_AND_FINALIZE rule"
  stop wording).
- WHY: same as S-BUDGET-1.

### Row S-BUDGET-4 — R1 HANDOFF "(exceeded at 28; honest stop)"
- SOURCE_FILE: `docs/audits/PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004/HANDOFF.md` (lines 19-21)
- ORIGINAL_EXCERPT:
  ```
  int-traits default 0); the ACTUAL value is runtime-mutable per-instance
  state whose writer was NOT identified within the 20-function budget
  (exceeded at 28; honest stop). Two byte-pinned candidate writer mechanisms
  ```
- CORRECTED_CLAIM: "(exceeded at 28; honest stop)" is superseded by
  FUNCTION_BUDGET_OVERRUN = BUDGET_OVERRUN_DISCLOSED. The storage statement in
  the same sentence is preserved (IMMEDIATE_VALUE_STORAGE =
  PER_RECEIVER_COMPONENT_VALUE_TABLE; producer UNRESOLVED).
- STATUS: SUPERSEDED (the "honest stop" framing; the measurement and the
  storage statement preserved).
- WHY: same as S-BUDGET-1.

### Row S-BUDGET-5 — the R1 AUDIT_ENTRYPOINT row's "honest stop per contract"
- SOURCE_FILE: `AUDIT_ENTRYPOINT.md` (LATEST RUNS row of the R1 package — historical row, NOT edited by this run)
- ORIGINAL_EXCERPT:
  ```
  NEW_FUNCTION_COUNT=28 (budget 20 EXCEEDED — honest stop per contract)
  ```
- CORRECTED_CLAIM: FUNCTION_BUDGET_OVERRUN = BUDGET_OVERRUN_DISCLOSED.
  Corrected reading carried by THIS package's new AUDIT_ENTRYPOINT row.
- STATUS: SUPERSEDED (the "honest stop per contract" framing; the 28>20
  measurement preserved).
- WHY: same as S-BUDGET-1.

---

## What is NOT superseded (explicitly preserved)

- GETTER_RESULT_TO_LOOKUP_KEY = PRESERVED_CONFIRMED (the identity-preserving
  dataflow table[10] → EAX → FUN_0072F880 p1 → *(u32*)&p1; zero conversions;
  zero-key abort) — all pins re-verified by this run's battery (C7-C11, E5,
  E6) without rerunning the S1-S11 instruments.
- CLASS_SELECTOR_20006 = CONFIRMED; PROPERTY_TAG_6 = CONFIRMED; the audited
  normal path: property tag 6 → factory slot 6 → descriptor id 10 →
  per-receiver value table[10] → current u32 → FUN_0072F880 lookup key.
- IMMEDIATE_VALUE_STORAGE = PER_RECEIVER_COMPONENT_VALUE_TABLE (the storage
  identity — GETTER_CHAIN/GETTER_RESULT_DATAFLOW read-location statements
  such as "reads table[10] ... NOT a constant, NOT the slot payload itself"
  are READ-LOCATION identities and make no ultimate-source claim).
- GETTER_RESULT_PROVENANCE = UNKNOWN; PHYSICAL_TEMPLATE_RECORD_TO_
  GETTER_RESULT = NOT_ESTABLISHED; PHYSICAL_SOURCE_RECORD_ID =
  NOT_ESTABLISHED — no source class promoted or excluded.
- The scoped zero-init fact: DEFAULT_CREATION_PATH_INITIAL_VALUE = 0
  (FUN_0070D990 default path, int-traits slot-1 FUN_009777E0
  `MOV DWORD [EAX],0` — re-verified, battery E1/E2/E5).
- The zero-key abort fact (a zero getter result is never consumed as a key).
- Candidate A (FUN_0070DCF0 → record-apply FUN_0070DC20 via the factory+0x84
  stream; reader-family LEAD only) and candidate B (factory+0x80 delegate
  bind) — both remain UNRESOLVED leads; no promotion, no deeper decode.
- The 0xD82 alternative's sub-outcome-1 CONVERGENCE with the normal branch
  (FUN_007292F0 TRUE) — preserved.
- CONTROL A (tags 2/4 same machinery, disjoint value-table entries 6/8 vs the
  audited 10) — preserved; CONTROL C preserved with NARROWED wording (see
  S-GP3-5/S-GP3-6).
- The historical S1-S11 instrument records and raw JSON (01_RAW/S*.json),
  scripts and manifest of the R1 package — READ-ONLY measurement records;
  NOT rerun by this correction; the historical S11 PASS (45 call checks + 33
  instruction pins) verifies pins and call targets ONLY — it does NOT prove
  lifetime immutability of the statics and was never claimed to.
- C1 = PRESERVED_CLOSED; C2 = PRESERVED_CLOSED;
  S1_STATIC_MECHANISM = PRESERVED_CONFIRMED;
  PARSER_TO_RUNTIME_VALUE_SEAM = CONFIRMED; RECORD_A/RECORD_B values;
  PLACEMENT_CONSUMER_EDGE = STRONGLY_SUPPORTED (level unchanged);
  WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO.
- The R1 AUDIT_ENTRYPOINT row itself (historical publication record,
  READ-ONLY) — superseded only by THIS ledger + THIS package's new row.
