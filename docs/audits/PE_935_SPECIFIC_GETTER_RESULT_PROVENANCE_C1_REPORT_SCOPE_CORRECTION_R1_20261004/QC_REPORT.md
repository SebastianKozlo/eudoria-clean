# QC_REPORT — PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_C1_REPORT_SCOPE_CORRECTION_R1_20261004

QC_SCOPE = SELF_CHECK_GETTER_PROVENANCE_REPORT_SCOPE_CORRECTION (executor
self-check; explicitly NOT an independent PE-MASTER audit; claim status is
kept separate from QC execution). MODE: STATIC-ONLY — the client never ran;
all re-verifications are byte reads from the pinned EXE (identity verified
in-battery: 8,015,872 B / SHA256 E7785430...).

## Targeted correction QC — gate table (Q1-Q8)

| Gate | Predicate (from the dispatch contract) | Result | Evidence |
|---|---|---|---|
| Q1 | GP1 storage/source separation — PASS only if NO file/static source is excluded without evidence | PASS | FINAL_REPORT GP1 block: IMMEDIATE_VALUE_STORAGE = PER_RECEIVER_COMPONENT_VALUE_TABLE; ULTIMATE_VALUE_SOURCE = UNKNOWN; FILE_DERIVED_VALUE_EXCLUDED = NO; RECORD_A_RELATION = NOT_ESTABLISHED; no exclusion claim anywhere in the ACTIVE docs; the historical exclusion wording superseded in ledger rows S-GP1-1/S-GP1-2 (QC_DOC_GATES REQ_FINAL_REPORT + FORBID scans) |
| Q2 | Creation timing — PASS only if default-zero creation is clearly scoped AND universal post-creation timing is NOT claimed | PASS | FINAL_REPORT GP1: DEFAULT_CREATION_PATH_INITIAL_VALUE = 0 explicitly scoped to the audited default path (FUN_0070D990 → FUN_009777E0 `MOV DWORD [EAX],0`, battery E1/E2 re-verified); NONZERO_VALUE_PRODUCER = UNRESOLVED; NONZERO_VALUE_PRODUCER_TIMING = UNRESOLVED; the after-creation universal absent from the ACTIVE docs (FORBID_FINAL_REPORT scan — zero hits); superseded in rows S-GP1-3/S-GP1-4/S-GP1-5 |
| Q3 | GP2 control-flow — PASS only if the FUN_00843340 path is documented as: tag6 bypass → shared caller → nonzero conditional FUN_0072F880 lookup | PASS | FINAL_REPORT GP2: ALTERNATIVE_TAG6_SEGMENT = BYPASSED; ALTERNATIVE_SHARED_LOOKUP = CONDITIONAL_ON_NONZERO_RESULT; byte-verified flow CALL FUN_00843340 @0x004C550E → JMP @0x004C5516 (EB 38) → 0x004C5550 → MOV ESI,EAX (8B F0) → MOV EAX,ESI @0x004C5563 (8B C6) → return to FUN_004C5580 → TEST EAX,EAX @0x004C55BD (85 C0) → zero aborts @0x004C55C3 / nonzero → PUSH EAX @0x004C55D1 (50) → CALL FUN_0072F880 @0x004C55D9 (battery C1-C11 all PASS); superseded in rows S-GP2-1..S-GP2-4 |
| Q4 | GP3 static lifetime scope — PASS only if initial-zero / direct-literal-scan / lifetime-immutability are DISTINCT | PASS | FINAL_REPORT GP3: FALLBACK_STATIC_INITIAL_CONTENT = ZERO_AT_IMAGE_MAPPING (battery D1: both statics in the .data virtual tail, zero-filled at mapping) and DIRECT_LITERAL_STORE_FOUND_IN_MEASURED_SCAN = NO (battery D6: re-measured same-scope census — 1 and 2 literal occurrences respectively, all loads/raw, ZERO store forms) and FALLBACK_STATIC_LIFETIME_IMMUTABILITY = NOT_ESTABLISHED — three separate, distinct statements; the census's exclusions (alias/pointer-derived/caller-through-returned-pointer/bulk/indirect writes NOT excluded) stated explicitly |
| Q5 | Control-C wording — PASS only if zero→abort is CONDITIONAL rather than a lifetime guarantee | PASS | FINAL_REPORT GP3: ZERO_RETURN_TO_LOOKUP_ABORT = CONFIRMED_CONDITIONAL; CONTROL C narrowed to "IF the fallback-loaded value is zero THEN FUN_004C5580 aborts before FUN_0072F880"; no lifetime-zero wording in the ACTIVE docs (FORBID scans zero hits); superseded in rows S-GP3-5/S-GP3-6 |
| Q6 | Budget wording — PASS only if BUDGET_OVERRUN_DISCLOSED appears and "per contract" compliance is NOT claimed | PASS | FINAL_REPORT: FUNCTION_BUDGET_OVERRUN = BUDGET_OVERRUN_DISCLOSED; MAX_NEW_FUNCTIONS_AUTHORIZED = 20; ACTUAL_DETAILED_COUNT = 28; the violation, the non-retroactive cure, the no-upgrade statement, the future hard pre-check and the non-retroactive-compliance statement all present; the stop-wording variants absent from the ACTIVE docs (FORBID scans); superseded in rows S-BUDGET-1..S-BUDGET-5 |
| Q7 | Preserved science — PASS only if GETTER_RESULT_TO_LOOKUP_KEY = PRESERVED_CONFIRMED (in the correction's own claim set), GETTER_RESULT_PROVENANCE = UNKNOWN, PHYSICAL_TEMPLATE_RECORD_TO_GETTER_RESULT = NOT_ESTABLISHED | PASS | All three exact strings present in FINAL_REPORT (QC_DOC_GATES REQ_FINAL_REPORT); the identity chain re-verified at pin level (battery C7-C11, E5, E6) WITHOUT rerunning S1-S11 or replacing their old records; no regression anywhere in the package |
| Q8 | Forbidden new-science census — PASS only if NO new function decode / source trace / alias-closure / stream provenance research occurred | PASS | 01_RAW/QC_CORRECTION_BATTERY.json forbidden_actions: decode_FUN_0070DC20=NO; decode_FUN_00843340_beyond_call_site=NO; trace_factory_plus_0x84_stream=NO; analyze_RECORD_A=NO; open_templates_vfs=NO; alias_closure_or_bulk_write_search=NO; model_join_position_rotation_world_xyz_network=NO; launch_client=NO — enforced by construction (the battery reads ONLY the pinned byte list + the same-scope direct-literal census); FINAL_REPORT: NEW_PLACEMENT_SCIENCE_EXECUTED = NO; NEXT_EXPERIMENT_EXECUTED = NO |

QC_VERDICT = QC_PASS 8/8.

## Machine batteries

| Battery | Scope | Result |
|---|---|---|
| 01_RAW/QC_CORRECTION_BATTERY.json | input identities (A1-A2), EXE identity (B1-B2), GP2 flow pins (C1-C11), GP3 statics + census (D1-D6), GP1 scoped pins (E1-E6), forbidden-actions census | 27/27 PASS, 0 FAIL |
| 01_RAW/QC_LEDGER_QUOTE_CHECKS.json | every SUPERSESSION_LEDGER.md ORIGINAL_EXCERPT is a whitespace-normalized substring of its named SOURCE_FILE | 23/23 PASS, 0 FAIL (no fabricated quote, no quote assigned to a file where it is absent) |
| 01_RAW/QC_DOC_GATES.json | required + forbidden strings over THIS package's ACTIVE docs (FINAL_REPORT.md, HANDOFF.md, SUPERSESSION_LEDGER.md) | PASS (all REQ gates satisfied; all FORBID scans zero hits) |

Key battery details (all from the pinned EXE, PE-mapped, no offset==RVA
assumption):

- GP2: CALL @0x004C550E bytes `e8 2d de 37 00` → 0x00843340; JMP @0x004C5516
  `eb 38` → 0x004C5550; `8b f0` @0x004C5550; cleanup `e8 5d e6 23 00`
  @0x004C555E → 0x00703BC0; `8b c6` @0x004C5563; caller call site
  @0x004C55B5 → 0x004C5480; `85 c0` @0x004C55BD; `0f 84 ed 04 00 00`
  @0x004C55C3 → 0x004C5AB6; `56 50` @0x004C55D0/D1; `e8 a2 a2 26 00`... the
  shared lookup CALL @0x004C55D9 → 0x0072F880; order gate: TEST < JE < PUSH <
  CALL (zero aborts BEFORE the lookup).
- GP3: both statics .data section, NOT file-backed (virtual tail; .data
  vsize 0x3D7A4 > rawsize 0x34000) → ZERO_AT_IMAGE_MAPPING; census: 0x00BA9374
  → 1 hit (MOV EAX,imm32 load @0x00977781, FUN_00977780 `B8 74 93 BA 00 C3`);
  0x00BA5108 → 2 hits (MOV EAX,imm32 load @0x0070C1E0, FUN_0070C180 default
  `B8 08 51 BA 00 C2 04 00`; raw operand-interior hit @0x005246B9); ZERO
  direct-store forms.
- GP1 scoped pins: int-traits vtable 0x00A9C670 slot 1 = 0x009777E0;
  `8b 44 24 04 c7 00 00 00 00 00 c2 04` @0x009777E0 (MOV EAX,[ESP+4]; MOV
  DWORD [EAX],0; RET 4); `89 73 04` @0x0070D9A5 (factory bind); `50 6A 00 6A
  00 6A 01 6A 06` @0x73758D (slot-6 schema args, 9 bytes); `8b 44 19 08`
  @0x0070DA36 / `8b 40 08` @0x004C5539 + `8d 0c 81` @0x004C553F (the
  writer/reader table idioms).

## Anti-success-theater declarations

1. **Keyword-hit ≠ failure:** the SUPERSESSION_LEDGER.md deliberately
   CONTAINS the superseded historical wording inside clearly-identified
   ORIGINAL_EXCERPT blocks (e.g. the historical lifetime-zero and
   never-consults phrases) — that is evidence of what was superseded, not an
   active claim. The FORBID scans therefore cover ONLY the ACTIVE documents
   (FINAL_REPORT.md, HANDOFF.md); the ledger is covered by the positive
   quotecheck instead (23/23 — every quote is a real substring of its named
   source file at BASE_SHA 25335a2).
2. **The historical S1-S11 records were NOT rerun and NOT replaced.** The
   historical S11 PASS (45 call checks + 33 instruction pins) verifies pins
   and call targets ONLY — it does NOT prove lifetime immutability of the
   statics; this correction's battery is a NEW, separate, bounded 27-check
   re-verification scoped to exactly the statements this correction
   re-states.
3. **Non-circularity:** every re-verified pin was set as a pre-registered
   expectation (dispatch contract + published R1 pins) BEFORE execution; the
   battery fails closed on any byte mismatch; the E4 width slip (8-byte
   expectation vs the published 9-byte pin) was caught by the battery itself
   on the first run and fixed BEFORE any document was finalized (recorded in
   INPUT_IDENTITIES.md).
4. **Default-success fallbacks:** none — a missing input, a hash mismatch,
   a byte mismatch, a missing required string, a forbidden-string hit or a
   missing-quote failure each fail the corresponding gate; all gates were
   actually evaluated and all results are recorded in the raw JSON.

## Honest boundaries

1. This QC is a targeted correction QC (SELF_CHECK) — it evaluates the
   CORRECTED claims and the supersession dispositions; it is not a
   re-audit of the R1 science and not an independent QC.
2. STATIC-ONLY: no runtime values of any static or table entry were (or
   could be) observed.
3. The docgates are textual gates over this package's own documents; they
   do not certify the absence of every possible wording variant of the
   superseded claims — the supersession LEDGER is the authoritative
   per-statement record (23 rows, each with SOURCE_FILE, ORIGINAL_EXCERPT,
   FINDING_ID, CORRECTED_CLAIM, STATUS, WHY).
