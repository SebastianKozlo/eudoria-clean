# FINAL_REPORT — PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_C1_REPORT_SCOPE_CORRECTION_R1_20261004

RUN_ID: PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_C1_REPORT_SCOPE_CORRECTION_R1_20261004
RUN_CLASS: LOAD_BEARING | RUN_TYPE: DESKTOP_POST_AUDIT_FOCUSED_CORRECTION |
MODE: STATIC-ONLY (the client never ran; every re-verification is a byte read
from the pinned EXE) | Executor: pe-reconstruction (PE-MASTER bounded worker
contract; explicitly human-ordered point correction; commit/push authorized in
its stated scope; NO_NESTED_TASKS).

## MISSION

EXACTLY the point correction of the claims/QC/handoff of
`PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004` (published at commit
25335a28ee61fc2a8c7763f41552df85af45d067) per the independent Desktop
post-audit `PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_DESKTOP_POST_AUDIT_
20261004` (verdict REQUIRE_CORRECTIONS_IN_REPORT_QC_HANDOFF_SCOPE):

1. **GP1_SOURCE_EXCLUSION_AND_CREATION_TIMING** — separate IMMEDIATE STORAGE
   from ULTIMATE SOURCE; scope the creation-timing claim.
2. **GP2_ALTERNATIVE_BRANCH_LOOKUP_BYPASS** — correct the false claim that the
   FUN_00843340 alternative bypasses FUN_0072F880 or directly returns a
   template object.
3. **GP3_STATIC_FALLBACK_LIFETIME_IMMUTABILITY** — replace the lifetime-
   immutability wording for 0x00BA5108/0x00BA9374 with the measured scope.
4. **FUNCTION_BUDGET_OVERRUN wording** — disclose the 28 > 20 overrun as a
   violation, not a contract-conformant stop.

NO new placement RE. NO decode of FUN_0070DC20 / FUN_00843340 / factory+0x84 /
RECORD_A / templates.vfs; no alias-closure search; no model join; no
position/rotation/world-XYZ/network work (scope guard, enforced by
construction — see 01_RAW/QC_CORRECTION_BATTERY.json forbidden_actions, all
NO).

## Inputs (all identities re-verified by this run)

| Input | Identity | Verification |
|---|---|---|
| Desktop post-audit REPORT.md | SHA256 B433828F8DF5C8EFF80A81303BD9A8CA88258E985A4ADB4760B1E6DEE3E670CD | battery A1 PASS |
| PE_MASTER_REVIEW_INPUT.txt | SHA256 61A0DB5CBD4F52C806107A76811C9B13D0A83679F053556F91D2FC9781608AC9 | battery A2 PASS |
| Pinned EXE (D:\Eudoria_Reconstruction\pcg_install\Entropia.exe) | 8,015,872 B / SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 | battery B1/B2 PASS |
| Historical R1 package + AUDIT_ENTRYPOINT.md row | read from the exact BASE_SHA 25335a2 tree (working tree == HEAD; zero tracked modifications; every ledger quote machine-verified as a real substring of its source — 01_RAW/QC_LEDGER_QUOTE_CHECKS.json 23/23 PASS) | quotecheck PASS |

## GP1 — STORAGE != ULTIMATE SOURCE; creation timing NOT closed

**Corrected canonical statements (exact):**

```text
IMMEDIATE_VALUE_STORAGE = PER_RECEIVER_COMPONENT_VALUE_TABLE
ULTIMATE_VALUE_SOURCE = UNKNOWN
FILE_DERIVED_VALUE_EXCLUDED = NO
RECORD_A_RELATION = NOT_ESTABLISHED
DEFAULT_CREATION_PATH_INITIAL_VALUE = 0
NONZERO_VALUE_PRODUCER = UNRESOLVED
NONZERO_VALUE_PRODUCER_TIMING = UNRESOLVED
```

- The audited getter reads the CURRENT u32 at the per-receiver 20006-class
  component's value-table entry 10 ([class_obj+0x40]+10*4) — the IMMEDIATE
  STORAGE is established and preserved. That storage fact does NOT identify
  the value's ultimate producer: a runtime table can be populated from a
  file, a constant, a computation, a cache, or a message, and NO source class
  is excluded without evidence (FILE_DERIVED_VALUE_EXCLUDED = NO; RECORD_A's
  relation to this value is NOT_ESTABLISHED — neither established nor
  excluded; the numeric value 16083 as the actual runtime key is neither
  established nor excluded — the only proven negative is the absence of a
  hardcoded 16083 literal in the audited getter path).
- The DEFAULT creation path (FUN_0070D990 → int-traits vtable 0x00A9C670
  slot 1 = FUN_009777E0 `MOV DWORD [EAX],0`) has byte-confirmed ZERO
  initialization for the audited int value (re-verified: battery E1 —
  vtable slot-1 dword = 0x009777E0; E2 — the MOV DWORD [EAX],0; RET 4 bytes;
  E5/E6 — the writer/reader table-idiom pair @0x0070DA36 / @0x004C5539).
  This does NOT establish that all possible creation/population paths first
  complete with zero and are modified only afterward: the cache-miss creator
  FUN_0070DE10 has an early path (candidate A: FUN_0070DCF0 → record-apply
  FUN_0070DC20 over the factory+0x84 stream) whose population order was
  never decoded. Therefore the nonzero-value producer AND its timing are
  UNRESOLVED. Candidate A / FUN_0070DCF0 → FUN_0070DC20 remains an
  unresolved lead; no physical/file/network/cache provenance is promoted.
- Preserved fact (unchanged): a ZERO key is never consumed — FUN_004C5580
  aborts on TEST EAX,EAX → JE 0x004C5AB6 before the lookup (battery C7/C8).
- Superseded wording: see SUPERSESSION_LEDGER.md rows S-GP1-1..S-GP1-5
  (the external review's source-exclusion wording, the published universal
  creation-timing claim in FINAL_REPORT.md:39-42 and
  PRODUCER_PROVIDER_CHAIN.md:22-25, and the entrypoint row's timing word).

## GP2 — the alternative does NOT bypass the shared FUN_0072F880 lookup

**Byte-verified flow (battery C1-C11, all PASS, pinned EXE):**

```text
CALL FUN_00843340 @0x004C550E   (E8 2D DE 37 00 -> 0x00843340; result in EAX)
ADD ESP,4        @0x004C5513
JMP              @0x004C5516   (EB 38) -> 0x004C5550
MOV ESI,EAX      @0x004C5550   (8B F0)
CALL FUN_00703BC0 @0x004C555E  (cleanup; ESI preserved)
MOV EAX,ESI      @0x004C5563   (8B C6)
return -> the SHARED caller FUN_004C5580 (its call site @0x004C55B5)
FUN_004C5580:
  TEST EAX,EAX   @0x004C55BD   (85 C0)
    result==0 -> JE 0x004C5AB6 @0x004C55C3 (0F 84 ED 04 00 00): abort BEFORE lookup
    result!=0 -> PUSH ESI @0x004C55D0; PUSH EAX @0x004C55D1 (50)
                 -> CALL FUN_0072F880 @0x004C55D9 (the SAME shared lookup)
```

**Corrected canonical statements (exact):**

```text
ALTERNATIVE_TAG6_SEGMENT = BYPASSED
ALTERNATIVE_SHARED_LOOKUP = CONDITIONAL_ON_NONZERO_RESULT
FUN_00843340_RESULT_SEMANTIC = UNKNOWN
FUN_00843340_RESULT_TO_LOOKUP_KEY = CONFIRMED_CONDITIONAL_ON_NONZERO
```

- The alternative's sub-outcome 2 BYPASSES the tag-6 getter and the value
  table (that segment of the historical claim is correct), but its result
  returns to the SAME caller FUN_004C5580, which ABORTS on zero and otherwise
  uses the result as the SAME FUN_0072F880 lookup key. The historical claim
  that this path never consults FUN_0072F880 is FALSE and superseded.
- The direct FUN_00843340 result is NOT called a template object — its
  semantic is UNKNOWN (FUN_00843340 was not decoded and is not decoded by
  this correction; no deeper RE performed).
- Superseded wording: SUPERSESSION_LEDGER.md rows S-GP2-1..S-GP2-4.
- Sub-outcome 1 (FUN_007292F0 TRUE) CONVERGES with the normal branch —
  preserved unchanged.

## GP3 — static INITIAL ZERO != LIFETIME IMMUTABILITY

**Measured scope (re-verified by this run, battery D1-D6):**

- BOTH statics — 0x00BA5108 (the out-of-range default slot) and 0x00BA9374
  (the fallback slot object) — lie in the .data VIRTUAL TAIL (.data
  vsize 0x3D7A4 > rawsize 0x34000; both RVAs beyond the raw data): both read
  as ZEROS AT IMAGE MAPPING (FALLBACK_STATIC_INITIAL_CONTENT =
  ZERO_AT_IMAGE_MAPPING).
- The direct-literal .text census (the SAME measured scope the R1 S5
  instrument performed — re-measured, not widened): 0x00BA9374 → exactly ONE
  .text literal occurrence, the MOV EAX,imm32 LOAD at 0x00977781
  (`B8 74 93 BA 00 C3` = FUN_00977780, battery D2); 0x00BA5108 → TWO
  occurrences, the MOV EAX,imm32 LOAD at 0x0070C1E0 (FUN_0070C180's
  default-slot return, battery D5) and one RAW byte-pattern hit at 0x005246B9
  (a coincidental operand interior, not an instruction using the literal).
  ZERO direct-store forms for BOTH statics.

**Corrected canonical statements (exact):**

```text
FALLBACK_STATIC_INITIAL_CONTENT = ZERO_AT_IMAGE_MAPPING
DIRECT_LITERAL_STORE_FOUND_IN_MEASURED_SCAN = NO
FALLBACK_STATIC_LIFETIME_IMMUTABILITY = NOT_ESTABLISHED
ZERO_RETURN_TO_LOOKUP_ABORT = CONFIRMED_CONDITIONAL
```

- The .text scan looks for LITERAL ADDRESS OCCURRENCES / direct-address
  forms ONLY — it does NOT exclude alias writes, pointer-derived writes,
  caller writes through returned pointers, bulk writes, or other indirect
  mutation. BOTH statics are RETURNED AS POINTERS (FUN_00977780 returns
  0x00BA9374; FUN_0070C180's default returns 0x00BA5108), so a caller can
  read or write through [reg] with no literal address anywhere in .text. No
  claim is made that either static's content must remain zero for the process
  lifetime.
- CONTROL C is NARROWED to: IF the fallback-loaded value is zero THEN
  FUN_004C5580 aborts before FUN_0072F880 (CONFIRMED_CONDITIONAL). The value
  is NOT claimed to remain zero for the process lifetime.
- NO alias-closure search was performed in this correction (scope guard; the
  Desktop's synthetic method counterexample — which proves the census
  insufficient for a lifetime claim — is recorded in the Desktop REPORT.md,
  not reproduced as new science here).
- Superseded wording: SUPERSESSION_LEDGER.md rows S-GP3-1..S-GP3-9 (across
  FINAL_REPORT, GETTER_CHAIN, ALTERNATIVE_BRANCH, CONTROL_CASE, HANDOFF,
  PROVENANCE_CHAIN.csv and the historical entrypoint row).

## FUNCTION BUDGET WORDING

Preserved factual measurement (unchanged):

```text
MAX_NEW_FUNCTIONS_AUTHORIZED = 20
ACTUAL_DETAILED_COUNT = 28
FUNCTION_BUDGET_OVERRUN = BUDGET_OVERRUN_DISCLOSED
```

- The authorized function budget of the R1 run was VIOLATED (28 detailed
  function decodes > 20 authorized; the contract's rule was to stop BEFORE
  the count would exceed 20).
- The later STOP_RE_AND_FINALIZE did NOT retroactively cure the violation.
- Valid byte evidence is preserved; NO scientific result is upgraded because
  of work performed outside the authorized budget.
- Future science contracts require a hard pre-check BEFORE entering function
  N+1 (the counter enforced pre-analysis, not post-analysis).
- THIS correction does NOT retroactively make the original run
  budget-compliant.
- Superseded wording: SUPERSESSION_LEDGER.md rows S-BUDGET-1..S-BUDGET-5
  (the contract-conformant-stop framing in FINAL_REPORT.md:164-165,
  QC_REPORT.md:94-96, HANDOFF.md:19-21 and 61-64, and the entrypoint row).

## Preserved canonical science (do NOT reopen — unchanged)

GETTER_RESULT_TO_LOOKUP_KEY = PRESERVED_CONFIRMED;
CLASS_SELECTOR_20006 = CONFIRMED; PROPERTY_TAG_6 = CONFIRMED; the audited
normal path (property tag 6 → factory slot 6 → descriptor id 10 →
per-receiver value table[10] → current u32 → FUN_0072F880 lookup key);
GETTER_RESULT_PROVENANCE = UNKNOWN; PHYSICAL_TEMPLATE_RECORD_TO_GETTER_
RESULT = NOT_ESTABLISHED; PHYSICAL_SOURCE_RECORD_ID = NOT_ESTABLISHED;
C1 = PRESERVED_CLOSED; C2 = PRESERVED_CLOSED; S1_STATIC_MECHANISM =
PRESERVED_CONFIRMED; WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED;
WORLD_XYZ_RECOVERED = NO. The historical S1-S11 instrument records and raw
JSON were NOT rerun and NOT replaced: the historical S11 PASS verifies pins
and call targets ONLY — it does NOT prove lifetime immutability of the
statics. This run's battery RE-VERIFIED (not re-derived) 27 bounded checks:
input identities (2), EXE identity (2), GP2 alternative-flow pins (11), GP3
statics placement + fallback-addressing + direct-literal census (6), GP1
scoped default-creation pins (6) — 27/27 PASS (01_RAW/
QC_CORRECTION_BATTERY.json).

## Terminal fields (exact)

```text
BASE_SHA = 25335a28ee61fc2a8c7763f41552df85af45d067
HEAD_SHA = (this publication commit; discover: git log -1 -- docs/audits/PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_C1_REPORT_SCOPE_CORRECTION_R1_20261004)
GP1_SOURCE_EXCLUSION_AND_CREATION_TIMING = CORRECTED
GP2_ALTERNATIVE_BRANCH_LOOKUP_BYPASS = CORRECTED
GP3_STATIC_FALLBACK_LIFETIME_IMMUTABILITY = CORRECTED
IMMEDIATE_VALUE_STORAGE = PER_RECEIVER_COMPONENT_VALUE_TABLE
ULTIMATE_VALUE_SOURCE = UNKNOWN
FILE_DERIVED_VALUE_EXCLUDED = NO
RECORD_A_RELATION = NOT_ESTABLISHED
DEFAULT_CREATION_PATH_INITIAL_VALUE = 0
NONZERO_VALUE_PRODUCER = UNRESOLVED
NONZERO_VALUE_PRODUCER_TIMING = UNRESOLVED
ALTERNATIVE_TAG6_SEGMENT = BYPASSED
ALTERNATIVE_SHARED_LOOKUP = CONDITIONAL_ON_NONZERO_RESULT
FUN_00843340_RESULT_SEMANTIC = UNKNOWN
FUN_00843340_RESULT_TO_LOOKUP_KEY = CONFIRMED_CONDITIONAL_ON_NONZERO
FALLBACK_STATIC_INITIAL_CONTENT = ZERO_AT_IMAGE_MAPPING
DIRECT_LITERAL_STORE_FOUND_IN_MEASURED_SCAN = NO
FALLBACK_STATIC_LIFETIME_IMMUTABILITY = NOT_ESTABLISHED
ZERO_RETURN_TO_LOOKUP_ABORT = CONFIRMED_CONDITIONAL
FUNCTION_BUDGET_OVERRUN = BUDGET_OVERRUN_DISCLOSED
MAX_NEW_FUNCTIONS_AUTHORIZED = 20
ACTUAL_DETAILED_COUNT = 28
GETTER_RESULT_TO_LOOKUP_KEY = PRESERVED_CONFIRMED
GETTER_RESULT_PROVENANCE = UNKNOWN
PHYSICAL_TEMPLATE_RECORD_TO_GETTER_RESULT = NOT_ESTABLISHED
PHYSICAL_SOURCE_RECORD_ID = NOT_ESTABLISHED
WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
NEW_PLACEMENT_SCIENCE_EXECUTED = NO
NEXT_EXPERIMENT_EXECUTED = NO
CANONICAL_GATE_EFFECT = NONE
```

## PERSISTENCE

Before the first canonical write: local HEAD == origin/master == actual
remote master == 25335a28ee61fc2a8c7763f41552df85af45d067 (rev-parse +
ls-remote, recorded in INPUT_IDENTITIES.md); the output root was verified
non-existent and created fresh; foreign untracked paths (5x
docs/audits/PE_935_* + experiments/) untouched. Immediately before commit:
actual remote master re-verified == 25335a2 (fetch + ls-remote; any change
would have meant BASE_DIVERGENCE, NO PUSH, HARD STOP). Path-limited staging
of THIS package + exactly one NEW AUDIT_ENTRYPOINT.md row; no `git add .`;
no force push; historical packages unchanged. COMMITTED_PACKAGE_MANIFEST_
SHA256.csv generated LAST (self-excluded; scope = all physical files of this
package + the updated AUDIT_ENTRYPOINT.md); bijection verified (no missing,
no extra, no duplicate, all sizes/SHA256 match). After push: local HEAD ==
origin/master after fetch == actual remote master, all equal.

## Honest boundaries

1. STATIC-ONLY: no runtime observation; nothing in this correction
   establishes what any static or table entry holds at any runtime moment.
2. This is a REPORT/QC/HANDOFF-SCOPE correction: no new placement science,
   no new decode, no source trace, no alias closure, no stream provenance.
3. The corrected UNKNOWNs (ultimate source; nonzero producer + timing;
   FUN_00843340 result semantic; fallback static lifetime) are honest
   terminals of the audited evidence, not deferred work silently promoted.
4. The R1 package's byte evidence, raw records, scripts and manifest are
   READ-ONLY history; the supersession ledger in THIS package is the
   correction record.
