# SUPERSESSION — PE_935_CAND4_CHILD_ROOT_NC2_NC3_DECODER_CORRECTION_R1_20261008

Explicit supersessions issued by this NC2/NC3 correction package (frozen contract §5/§6).
Superseded basis: the independent Desktop post-audit of the published NC1 state
(PE_935_NC1_DESKTOP_POST_AUDIT_91598A98_20261007 — REPORT.md 11570 B /
125C47CA195C5D2F782EA1DBCEA0BA1CA65B973CBABEBABDD4F78963C43E83B4;
CONTROL_COUNTERCHECKS.json 132471 B / AD8DC2052F714439497A277512944EF729F53BDC94B436CB20EE09FEE6BCC28D;
AUDIT_CHECKS.json 46417 B / 593B03C3AB87FD274BE8C02E7196D60A961975C95631278C97A8271E528862B7 —
all re-verified byte-identical by the executor, the fresh internal QC and PE-MASTER) which
recorded POST_AUDIT_VERDICT = REQUIRE_CORRECTIONS_FOR_RESIDUAL_MACHINERY with
RESIDUAL_NC2_PRODUCTION_NON_SIB_BOUNDARY = CONFIRMED_P2 and
RESIDUAL_NC3_QC_INVALID_FORMS = CONFIRMED_P2 at AUDITED_SHA
91598a9868037c4954e22e16c535d6a5a671771e.

This supersession is NARROW: it reaches exactly the two residual CTRL_4 machinery defect
states and one over-general sentence of the NC1-era report. Nothing else of the audited
91598a98 state is reopened. The superseded historical packages remain READ-ONLY and their
records are NOT edited — this file + the corrected successors of THIS package
(03_SCRIPTS/ctrl4_exact_endpoint_nc23fixed.py + 00_CONTROL_INTERNAL_QC/qc_ind_ctrl_nc23_own.py)
are the supersession authority. Supersession takes effect only because the positive
executable QC gate (G1..G6 all PASS, QC_VERDICT = PASS, 00_CONTROL_INTERNAL_QC/QC_RESULTS.json)
and the PE-MASTER MASTER_ACCEPTED review (advisory; ADVISORY_PRE_QUALIFICATION) were issued;
the corrected status naming below is CORRECTED_AND_REVALIDATED_IN_TEST_SCOPE, where the test
scope is exactly the 8-case matrix + the 9-case SIB battery + the 144-form sweep. NOT
GENERAL_X86_DECODER_PROVEN.

## SN-1. RESIDUAL_NC2_PRODUCTION_NON_SIB_BOUNDARY = CONFIRMED_P2 — SUPERSEDED (status transition to CORRECTED_AND_REVALIDATED_IN_TEST_SCOPE)

Where (superseded state, at 91598a98): the Desktop post-audit finding NC2/P2 — the published
production decoder 03_SCRIPTS/ctrl4_exact_endpoint_sibfixed.py, `decode()`, opcode 0x84 branch,
line 236 `size = 2 if mod == 0b11 else (3 if mod == 0b01 else 6)` assigns a 6-byte length to the
2-byte memory TEST form `84 06` (mod=00, rm=6; no SIB, so the NC1 guard does not block it),
swallows `84 06 BF AA BB CC` as one TEST, decodes the MOV-EDI immediate as a CALL, and FALSE-PASSES
the synthetic buffer `84 06 BF AA BB CC E8 90 90 90 90 90` @0x0050A3DD..0x0050A3E8 — the EDI write
`mov edi,0xE8CCBBAA` @0x0050A3DF inside the prohibited P2 interval (0x0050A3B7, 0x0050A3F6) is
never decoded (Desktop measurement: EXPECTED=FAIL, ACTUAL_PRODUCTION=PASS,
ACTUAL_INTERNAL_QC=FAIL, REFERENCE_EDI_WRITE=0x0050A3DF; Desktop capstone 5.0.7 reference decode
cited; PRE reproduced on the REAL AST-extracted historical functions by this run's
EXECUTOR_REPRODUCTION in CONTROL_RESULTS_PRE.json: production PASS / QC FAIL).

Superseded by: the corrected production successor 03_SCRIPTS/ctrl4_exact_endpoint_nc23fixed.py
(SHA256 68BEC1AEFDF6A0F32A3ED12F3AED9B72255F8A89AA2F5BA4EFD11C709C4D9F13) — the sibfixed 0x84
memory length table is REMOVED BY DESIGN; EVERY memory TEST form (mod != 11) is rejected
fail-closed with `ValueError: unsupported memory TEST form (mod=00) — FAIL CLOSED` BEFORE any
length computation (raise @line 289 precedes `size = 2` @line 291), while the clean register TEST
84 C0 stays supported. Revalidated in test scope: the POST 8-case matrix on the ACTUAL corrected
function (clean PASS; NC2_NON_SIB_TEST_HIDDEN_EDI FAIL on both checkers), the 9-form SIB battery
(9/9 rejected by BOTH decoders) and the 144-form sweep (144/144 rejected by BOTH decoders at the
DECODER level; 288 decoder calls); the fresh independent QC executed the actual function via
importlib (8/8 POST row equality) and PE-MASTER independently re-executed it (8/8 match).

New status:

```text
NC2_PRODUCTION_NON_SIB_BOUNDARY_FALSE_PASS = CORRECTED_AND_REVALIDATED_IN_TEST_SCOPE
(test scope = 8-case matrix + 9 SIB cases + 144-form sweep; NOT GENERAL_X86_DECODER_PROVEN)
```

## SN-2. RESIDUAL_NC3_QC_INVALID_FORMS = CONFIRMED_P2 — SUPERSEDED (status transition to CORRECTED_AND_REVALIDATED_IN_TEST_SCOPE)

Where (superseded state, at 91598a98): the Desktop post-audit finding NC3/P2 — the published
independent internal-QC engine 00_CONTROL_INTERNAL_QC/qc_ind_ctrl_sib_own.py, `my_decode()`:

- (A) the FF branch `reg == 0b011` described FF /3 as PUSH and, for `FF D8` (mod=11), fabricated
  a harmless 2-byte `push eax` — FF /3 is far CALL with a memory-only operand; the register form
  FF D8 is an INVALID x86 encoding. Desktop measurement: PRODUCTION=FAIL, INTERNAL_QC=PASS
  (the false PASS); PRE reproduced (production FAIL / QC PASS).
- (B) the LEA branch treated `8D C0` (mod=11) as a valid `lea eax, eax` and FALSE-PASSED — LEA
  requires a memory operand. Desktop measurement: INTERNAL_QC=PASS, PRODUCTION=TypeError
  (formatting memoff=None), i.e. the historical production crashed with an uncontrolled TypeError
  instead of a verdict. PRE reproduced (production ERROR:TypeError captured as ERROR / QC PASS).

Superseded by: the fresh independent QC successor 00_CONTROL_INTERNAL_QC/qc_ind_ctrl_nc23_own.py
(own implementation lineage from the historical internal-QC engine; only stdlib imports) —
NC3-A: the erroneous FF /3 acceptance REMOVED; only FF /2 mod=11 remains accepted (incl. the
required FF D2 endpoint); FF D8 rejected fail-closed (`ValueError: uncovered FF /3 mod=11`);
FF /6 NOT added (verified: FF F0 raises on both engines). NC3-B: LEA mod=11 rejected explicitly
BEFORE operand formatting in BOTH decoders (`ValueError: unsupported LEA register form
(mod=11) — FAIL CLOSED`; production raise @line 247 precedes the LEA formatting @line 282) → the
checker returns the controlled (False, diagnostic) verdict — the historical production TypeError
defect is eliminated (zero TypeError in any POST row; checker catch only (ValueError, IndexError)
@line 353). Revalidated in test scope: POST 8-case matrix (NC3_INVALID_FF_FAR_CALL_REGISTER and
NC3_INVALID_LEA_REGISTER both FAIL on both checkers), register-form support battery (84 C0,
8D 06, FF D2 decode; FF F7, FF F0, 8D C0 raise) and the 144-form sweep; QC re-execution of the
actual production equals POST 8/8; PE-MASTER counter-check 8/8.

New status:

```text
NC3_QC_INVALID_FORMS_ACCEPTANCE (FF /3 register + LEA mod=11) = CORRECTED_AND_REVALIDATED_IN_TEST_SCOPE
NC3_LEA_HISTORICAL_TYPEERROR = ELIMINATED (controlled (False, diagnostic) rejection in both decoders)
(test scope = 8-case matrix + 9 SIB cases + 144-form sweep; NOT GENERAL_X86_DECODER_PROVEN)
```

## SN-3. NC1-era report overclaim "reject everything else fail-closed" — SUPERSEDED (bounded to the tested scope)

Where (superseded sentence, NC1-era report at 91598a98): PE_935_CAND4_CHILD_ROOT_NC1_SIB_
DECODER_POST_AUDIT_CORRECTION_R1_20261007/FINAL_REPORT.md §11 — "both engines cover only the
recorded clean window's opcode universe and reject everything else fail-closed" — and the same
sentence in that package's QC_REPORT.md §10 (NOT CLAIMED clause). The Desktop post-audit of
91598a98 ruled this sentence TOO STRONG ("Zdanie z raportu, że wszystkie pozostałe formy są
odrzucane fail-closed, jest zbyt silne"): two concrete non-SIB unsupported forms were NOT
rejected fail-closed by the then-current implementations (the NC2 production memory TEST form
false-pass; the NC3 QC FF /3-register and LEA mod=11 false-passes) and one produced an
uncontrolled TypeError.

Superseded by: this package's corrected, now-authoritative bounded wording — the fail-closed
rejection discipline of the corrected successors (03_SCRIPTS/ctrl4_exact_endpoint_nc23fixed.py +
00_CONTROL_INTERNAL_QC/qc_ind_ctrl_nc23_own.py) is established EXACTLY WITHIN THE TESTED SCOPE of
the 8-case matrix + the 9-case SIB battery + the 144-form sweep (6 opcode branches 8B/89/8D/84/
83/FF × 3 memory mod 00/01/10 × 8 reg, always rm=4, 144 forms, 288 decoder calls, all rejected at
the DECODER level by BOTH decoders, never presented as an accidental whole-checker P1 FAIL).
Every claim of "everything else fails closed" outside that tested scope is RETRACTED as an
unsupported generalization; no universal x86-decoder correctness is claimed (NOT
GENERAL_X86_DECODER_PROVEN), and no historical finding depends on the superseded sentence.

```text
"ALL OTHER UNSUPPORTED FORMS ALREADY REJECTED FAIL-CLOSED" (unbounded, NC1-era) — RETRACTED
CTRL4_REJECTION_DISCIPLINE = ESTABLISHED_WITHIN_TESTED_SCOPE_8CASE_9SIB_144SWEEP
```

## Explicitly NOT superseded (all preserved verbatim; historical results remain authentic and unchanged)

```text
NC1 = CLOSED_FOR_AUDITED_STATE for 91598a98 (unchanged historical status; the NC1 SIB guards
      are preserved in every memory-ModRM branch of both successors — @245/287/299/328 in the
      production successor, before any displacement/length computation)
All historical results of the three prior packages (SOURCE / PRIOR_SCIENCE / PRIOR_CORRECTION
      packages — authentic, byte-unchanged, READ-ONLY)
C4_C1_RECORDS = ACCEPTED_IN_EXAMINED_RECORDS_SCOPE
MINIMUM_NEW_ANALYZED_EDGE_COUNT >= 32; EXACT = UNRESOLVED
MINIMUM_NEW_FUNCTION_BODIES_OPENED >= 7; EXACT = UNRESOLVED
ORIGINAL_SCOPE/BUDGET_COMPLIANCE = FAIL
RETROACTIVE_PRIOR_AUTHORIZATION = NO
WRAPPER_DEPTH = UNRESOLVED
HISTORICAL_LINEAGE_BUDGET_CHARGE = 2/3
The real clean recorded bytes (the published 0x42 window: 22 instructions, P1 8B F8 @0x0050A3B7,
      P3 57 @0x0050A3F6, P4 FF D2 @0x0050A3F7 — boundary regression identical, total 0x42)
The getter/store byte evidence (FUN_006C66D0 mov eax,[ArkModelManagerMain+0x68] 8B 41 68 C3;
      writer FUN_006C6780 store [mgr+0x68]=[instance+4] @0x006C67E2)
CHILD_RESOURCE_PROVENANCE = STRONGLY_SUPPORTED_MODEL_DERIVED
MODEL_ROOT_RELATION = UNKNOWN
CHILD_VISUAL_ROLE = UNRESOLVED
CHILD_TO_JOIN_IDENTITY = STRONGLY_SUPPORTED
EXACT_PARENT = CONFIRMED_EXACT_SCENEFEEDER_PLUS_30 (scoped to examined ACLD+0x18 SF instance)
JOIN_OPERATION = STRONGLY_SUPPORTED
CAND4_CHILD_ROOT_CLOSURE = NOT_ESTABLISHED_WITHIN_BOUND
WORLD_INSTANCE = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
```

## Scope statement

The NC2/NC3 changes touch VALIDATION MACHINERY ONLY: the two CTRL_4 exact-endpoint checkers and
their QC gates. This package creates NO historical placement data and retracts NO historical
placement data; no science status of the prior runs changes; no new function bodies were opened
and no EXE was accessed. The historical PRE behavior is preserved read-only as the honest
record of the defect (CONTROL_RESULTS_PRE.json); the POST behavior is the corrected successor's
own measured state (CONTROL_RESULTS_POST.json). Publication is not acceptance: the PE-MASTER
verdict is advisory (ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT = NONE) and the future
Desktop post-audit of the newly published correction SHA remains pending
(NEW_CORRECTION_DESKTOP_POST_AUDIT = NOT_PERFORMED).
