# HANDOFF — PE_935_PARAMETER_RECORD_C1_C1_STORE_IDENTITY_QC_R1_20261004

RUN_ID: PE_935_PARAMETER_RECORD_C1_C1_STORE_IDENTITY_QC_R1_20261004
RUN_CLASS: LOAD_BEARING | STATIC-ONLY (the client never ran) | Executor:
pe-reconstruction (PE-MASTER bounded worker contract; NO_NESTED_TASKS).
QC_SCOPE = SELF_CHECK_C1_C1_STORE_IDENTITY (executor self-check; NOT an
independent PE-MASTER audit). Persistence by the executor under explicit
PE-MASTER publication assignment (path-limited commit; remote re-verified
before the commit).

## What this run did (and only this)

Fixed EXACTLY the remaining C1-C1/P2 of the C1-correction package's
CLIENT_DESTINATION_MAPPING_CHECK: the published verifier proved only "at the
documented VA there is an instruction writing the declared displacement" — it
did NOT bind payload index / field identity → the correct store instruction →
the correct destination.

1. **Reproduced the defect FIRST on the pristine BASE** (private copies only;
   the historical verifier imported READ-ONLY, SHA256 CB4587C1...): Desktop
   mutant C (payload[1](A) row → template+0x04 → MOV [EDI+0x04],EAX
   @0x00730D14; payload[2](B) row → template+0x08 → MOV [EDI+0x08],EAX
   @0x00730CE6 — both REAL stores with MATCHING displacements belonging to the
   OTHER payload field) produced the exact false PASS on BASE:
   PAYLOAD_FIELD_DECODE_CHECK=PASS, CLIENT_DESTINATION_MAPPING_CHECK=PASS,
   FULL_QC=QC_PASS (BASE canonical QC_PASS 10/10 and BASE A/B falsifier
   DETECTED re-measured as controls). 01_RAW/BASE_MUTANT_C_REPRODUCTION.json.
2. **Corrected the gate** (03_SCRIPTS/qc_targeted_c1c1.py TQ2): validates THREE
   identities SIMULTANEOUSLY — PAYLOAD FIELD IDENTITY (idx+name) → STORE
   INSTRUCTION IDENTITY (the exact store VA independently assigned to that
   payload index) → DESTINATION FIELD IDENTITY (the destination of that same
   assigned instruction) — against an INDEPENDENT, HARD-CODED parser-sequence
   oracle byte-backed at runtime from the pinned Entropia.exe (SHA
   E7785430...; six pins: id2 89 07 @0x00730CB6; A 89 47 08 @0x00730CE6; B
   89 47 04 @0x00730D14; C 89 47 0C @0x00730D42; D FLD D9 04 10 @0x00730D69 +
   FSTP D9 5F 10 @0x00730D70; store VAs strictly increasing with payload
   index). The document under test can NEVER supply the mapping
   (anti-circularity: MEASURED_QUANTITY = payload-index→exact-store-VA
   identity; INDEPENDENT_SOURCE_OF_TRUTH = pinned EXE bytes + the
   independently fixed normal parser instruction order; the tested
   PARSER_CHAIN table is never used to generate the expected mapping).
3. **POST-FIX battery** (01_RAW/QC_MUTATION_BATTERY_POST_FIX.json; every case
   a PRIVATE document copy; full QC re-run per case): canonical copy PASSES
   (negative control; byte-identical document 6BA91A1F... — the private-copy
   pipeline is content-neutral); mutants A and B FAIL (historical controls
   preserved); mandatory mutant C FAILS — PAYLOAD_FIELD_DECODE_CHECK=PASS,
   PAYLOAD_INDEX_STORE_IDENTITY_CHECK=FAIL, CLIENT_DESTINATION_MAPPING_CHECK=
   FAIL, FULL_QC=QC_FAIL, per-row oracle-grounded reasons recorded
   (e.g. "documented store VA 0x00730D14 is the store of payload[2] (B) per
   the independent parser-sequence oracle, NOT the store of payload[1] (A)").
   MUTANT_A_DETECTED=YES; MUTANT_B_DETECTED=YES; MUTANT_C_POST_FIX_DETECTED=YES.
4. **Corrected canonical QC**: QC_PASS 10/10 on the canonical document
   (01_RAW/QC_TARGETED.json) — the canonical A→+0x08 / B→+0x04 mapping is
   UNCHANGED and now verified at identity level. Full-QC FAILS whenever TQ2
   fails (proven by the battery).
5. **Supersession recorded** (SUPERSESSION_LEDGER.md): the C1-correction
   package's "The Desktop-counterexample blind spot is closed" detection-scope
   claim and the A/B-falsifier detection-duty wordings are superseded
   (detection scope ONLY — the mapping, all values, and all canonical state are
   preserved). Bounded P3: the blanket "VERBATIM" label of the historical
   ledger is corrected to ORIGINAL_EXCERPT discipline by a ledger row (no
   historical file was edited; the six quotes in THIS ledger are byte-exact
   contiguous substrings, programmatically verified).
6. **AUDIT_ENTRYPOINT.md**: one new LATEST RUNS row.

## TERMINAL FIELDS (exact)

```text
BASE_SHA = 97bdf959cb742490a0e974bddf5a2dd25f93f5f7
HEAD_SHA = (this publication commit; discover: git log -1 -- docs/audits/PE_935_PARAMETER_RECORD_C1_C1_STORE_IDENTITY_QC_R1_20261004)
C2_CLASS_SELECTOR_PROPERTY_TAG = PRESERVED_CLOSED
S1_STATIC_MECHANISM = PRESERVED_CONFIRMED
PAYLOAD_FIELD_DECODE_CHECK = PASS
CLIENT_DESTINATION_MAPPING_CHECK = PASS
PAYLOAD_INDEX_STORE_IDENTITY_CHECK = PASS
MUTANT_A_DETECTED = YES
MUTANT_B_DETECTED = YES
MUTANT_C_BASE_FALSE_PASS_REPRODUCED = YES
MUTANT_C_POST_FIX_DETECTED = YES
C1_C1_PAYLOAD_INDEX_TO_STORE_IDENTITY = FIXED_AND_VERIFIED
C1 = CLOSED_FOR_AUDITED_STATE
PHYSICAL_RECORD_TO_PLACEMENT_ATTRIBUTE = NOT_ESTABLISHED
WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
NEW_PLACEMENT_SCIENCE_EXECUTED = NO
NEXT_EXPERIMENT_EXECUTED = NO
CANONICAL_GATE_EFFECT = NONE
```

## State handed forward (unchanged unless stated)

- C2_CLASS_SELECTOR_PROPERTY_TAG = CLOSED_FOR_AUDITED_STATE (CLASS_SELECTOR
  0x4E26 = 20006 vs PROPERTY_TAG 6) — PRESERVED_CLOSED.
- S1_STATIC_MECHANISM = PRESERVED_CONFIRMED; PARSER_TO_RUNTIME_DEFINITION_SEAM
  = CONFIRMED; RECORD_A {16083, 410620, 0, 0, 0.49950098991394043} and
  RECORD_B {4508, 296445, 296446} values UNCHANGED (TQ1 re-verified).
- PHYSICAL_RECORD_TO_PLACEMENT_ATTRIBUTE = NOT_ESTABLISHED;
  WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO.
- The next placement experiment (SPECIFIC_GETTER_RESULT_PROVENANCE, OPEN
  taxonomy) remains DESIGNED-NOT-EXECUTED; its wording is intact (TQ7).
- NEW_PLACEMENT_SCIENCE_EXECUTED = NO; NEXT_EXPERIMENT_EXECUTED = NO;
  CANONICAL_GATE_EFFECT = NONE. **Terminal HARD STOP: the next placement
  experiment was NOT executed (per contract).**

## Evidence pointers

- Defect reproduction (BASE false PASS): `01_RAW/BASE_MUTANT_C_REPRODUCTION.json`
- Corrected canonical QC: `01_RAW/QC_TARGETED.json`
- POST-FIX battery: `01_RAW/QC_MUTATION_BATTERY_POST_FIX.json`
- Oracle evidence (pins + sequence + bounded EXE windows):
  `01_RAW/ORACLE_EVIDENCE.json`
- The instrument: `03_SCRIPTS/qc_targeted_c1c1.py` (modes: base_repro | normal |
  battery | oracle; READ-ONLY vs all originals and the historical package)
- Supersession + ORIGINAL_EXCERPT discipline: `SUPERSESSION_LEDGER.md`
- Input identities: `INPUT_IDENTITIES.md`
- QC records: `QC_TARGETED_REPORT.md`
- Manifest (generated LAST, self-excluded): `COMMITTED_PACKAGE_MANIFEST_SHA256.csv`
  — scope = every file of THIS package + AUDIT_ENTRYPOINT.md, minus the
  manifest. No proprietary payload beyond the bounded byte windows/pins
  already published in the historical packages; no NEW proprietary payload
  (the byte windows in ORACLE_EVIDENCE.json are the same instruction windows
  already published by the C1-correction package plus three small per-field
  blocks of the same FUN_00730C90 body).
