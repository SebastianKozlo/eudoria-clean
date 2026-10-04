# QC_REPORT — PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004

QC_SCOPE = SELF_CHECK_SPECIFIC_GETTER_RESULT_PROVENANCE (executor self-check;
explicitly NOT an independent PE-MASTER audit; claim-status kept separate
from QC execution). MODE: STATIC-ONLY — the client never ran; all identities
are byte reads from the pinned EXE.

## Gate table

| Gate | Check | Result |
|---|---|---|
| Q1 | base/EXE identity | PASS — EXE re-measured 8,015,872 B / SHA256 E7785430... (run start + final battery); BASE_SHA 53c57bfa... re-verified; actual-remote equality re-verified at persistence (FINAL_REPORT PERSISTENCE) |
| Q2 | exact receiver chain | PASS with scope — entity → [entity+4] → FUN_00747970 → resolved receiver → 20006 class_obj → getter receiver = [class_obj+4] = FACTORY: all edges machine-verified; FUN_00747970 surface-only (EXACT_RECEIVER_IDENTITY=STRONGLY_SUPPORTED) |
| Q3 | class selector 20006 | PASS — pair imm32 0x4E26 @0x004C54C2; dispatch CMP 0x4E20 / ADD -0x4E21 / jump-table entry 5 → MOV EAX,[0x00BA590C] @0x0073C8D8; 20006 never called a property tag anywhere in this run's docs |
| Q4 | property tag 6 | PASS — PUSH 6 (6A 06) @0x004C551F; slot 6 in the factory array; SLOT_ADD args byte-pinned @0x73758D |
| Q5 | branch predicate | PASS — PUSH 0xD82 @0x004C54DD → FUN_00844020 → TEST AL,AL → JE 0x004C5518 (normal) |
| Q6 | getter returned-value extraction | PASS — slot+4==1, +0xC bit0 clear, MOV EAX,[EAX+8] @0x004C5539, LEA [table+id*4] @0x004C553F, MOV EAX,[EAX] @0x004C554E |
| Q7 | returned-value → FUN_0072F880 key identity | PASS — identity-preserving u32 dataflow; mapfind key = *(u32*)&p1 @0x004D143E; zero conversions (GETTER_RESULT_DATAFLOW.md) |
| Q8 | producer/provider provenance | PARTIAL (honest) — schema/storage/initial value CONFIRMED; the ACTUAL value writer UNRESOLVED (two bounded candidates: FUN_0070DCF0 record-read path with the factory+0x84 stream; the factory+0x80 delegate bind); GETTER_RESULT_PROVENANCE=UNKNOWN retained |
| Q9 | negative control discrimination | PASS — CONTROL A (tags 2/4 same machinery, disjoint table entries) + CONTROL C (fallback → NULL, no key) byte-pinned in the battery |
| Q10 | forbidden-overclaim census | PASS — see census below |
| Q11/Q12 | physical-record identities | NOT_APPLICABLE — no PHYSICAL_RECORD_DERIVED claim made (bridge stays NOT_ESTABLISHED; templates.vfs never opened) |

## Instrument battery (01_RAW/S11_QC_BATTERY.json)

- Call-target checks: 45 PASS, 0 FAIL, 4 COMPUTED (allocator/thunk targets
  recorded for completeness: 0x0095D3C4, 0x0095D3BE, 0x0070C7B0,
  0x007374C0 — the last is the class_obj ctor target, itself
  machine-resolved and micro-decoded).
- Instruction pins: 33 PASS, 0 FAIL (after the transcription-slip
  corrections documented in INPUT_IDENTITIES.md).
- Control-case JE arithmetic: PASS (JE 0x004C5AB6 target machine-verified).
- EXE identity inside the battery: match=True.

## Anti-success-theater declarations (material positive claims)

1. **Claim: the getter returns the class component's value-table entry 10 and
   that u32 is the FUN_0072F880 key.**
   - MEASURED_QUANTITY: instruction bytes + rel32 targets on the path
     0x004C5518..0x004C55D9 and 0x0072F880..0x004D143E.
   - INDEPENDENT_SOURCE_OF_TRUTH: the pinned EXE bytes (SHA256 E7785430...,
     verified in-battery).
   - WHY_NON_CIRCULAR: no document validates another document; every edge is
     re-read from raw bytes by an independent mapper and machine-verified
     call-target arithmetic; the writer-side/reader-side idiom match
     (0x0070DA36/0x0070DA3E vs 0x004C5539/0x004C553F) is byte-level, not
     numeric-coincidence-based.
   - FAILURE_CASE_DETECTED: the three target-arithmetic slips and five pin-VA
     slips were caught by this battery (recorded in INPUT_IDENTITIES.md);
     the battery fails closed on any byte mismatch.
2. **Claim: the tag-6 slot schema is CONSTANT_INITIALIZATION (kind=1 int,
   id=10, flags=0, int traits).**
   - MEASURED_QUANTITY: the SLOT_ADD argument bytes @0x73758D and the slot
     field writes of FUN_0075F5C0.
   - INDEPENDENT_SOURCE_OF_TRUTH: pinned EXE bytes + the 20002_PAYLOAD30
     canon as CORROBORATION only (independently re-derived: vtable
     0x00A9C670 store @0x00977A68, slot+0 traits layout, tag+4 idiom
     @0x70CBF6).
   - WHY_NON_CIRCULAR: the canon was not used to generate the expectation;
     the bytes were decoded first.
   - FAILURE_CASE_DETECTED: CONTROL A proves the machinery is shared across
     tags — a "generic mechanism" claim would be unfalsifiable, the
     tag-specific chain is not.
3. **Claim: the actual runtime value's producer is UNRESOLVED.**
   - MEASURED_QUANTITY: absence within budget of any decoded writer of
     [class_obj+0x40]+10*4 with a source; presence of two bounded candidate
     mechanisms.
   - INDEPENDENT_SOURCE_OF_TRUTH: FUN_0070DCF0's machine-verified call to
     FUN_00971AD0 (the R1-canon record reader) is a LEAD, not a conclusion —
     the factory+0x84 stream's backing data is unidentified.
   - WHY_NON_CIRCULAR: no physical-record promotion was made from the
     reader-family coincidence (explicitly: seeing FUN_00971AD0 used
     elsewhere over templates.vfs proves nothing about THIS stream).
   - FAILURE_CASE_DETECTED: the whole run refused S2/S3 promotion precisely
     because the control discipline separates mechanism from provenance.

## Forbidden-overclaim census (Q10)

MODEL_JOIN_EXECUTED=NO; POSITION_RECOVERY_GOAL=OUT_OF_SCOPE;
WORLD_XYZ_RECOVERED=NO; STATIC_INSTANCE_CONFIRMED=NOT_ESTABLISHED;
WORLD_INSTANCE_SEMANTIC=NOT_ESTABLISHED; NETWORK_PLACEMENT_PROVEN=NO;
no "placement recovered" wording anywhere; class selector 20006 is never
called a property tag (PROPERTY_TAG on the audited branch = 6); the
class-20006 attribute system is never called a placement system; the
FUN_00971AD0 lead is labeled a LEAD, not a bridge; no ALL-TAGS/ALL-20006
census claims (decode coverage: the audited chain + its immediate machinery
only); templates.vfs untouched.

## Honest boundaries

1. STATIC-ONLY: no runtime observation; which creation path (record-read vs
   delegate bind) is live for the audited receiver is runtime state (the
   manager mode gates it statically, its runtime value is unknown).
2. The budget was EXCEEDED (28 detailed functions > MAX 20) — the run
   stopped RE at the value-writer boundary per contract, honestly recorded
   as FIRST_MISSING_EDGE=FUNCTION_BUDGET_EXHAUSTED.
3. FUN_00747970, FUN_0070DC20, FUN_0070E2F0, FUN_007292F0, FUN_00843340,
   FUN_007374C0's base-ctor FUN_00735E70 and the class_obj vtable
   0x00A86F2C slot enumeration were NOT decoded (surface/identity only) —
   recorded as the designed-not-executed next experiment.
4. slot+8 mutability: no census excludes a later writer of slot+8 (the
   claim is "id 10 at creation", not "id 10 forever").
