# FINAL_REPORT — PE_935_PARAMETER_RECORD_C1_C1_STORE_IDENTITY_QC_R1_20261004

RUN_ID: PE_935_PARAMETER_RECORD_C1_C1_STORE_IDENTITY_QC_R1_20261004
RUN_CLASS: LOAD_BEARING | MODE: STATIC-ONLY (client never launched; raw byte
reads + independent x86 byte verification only) | Executor: pe-reconstruction
(PE-MASTER bounded worker contract; NO_NESTED_TASKS; QC_SCOPE =
SELF_CHECK_C1_C1_STORE_IDENTITY — executor self-check, explicitly NOT an
independent PE-MASTER audit) | Dispatch: PE-MASTER direct, 2026-10-04.

## MISSION AND RESULT

Fix EXACTLY the remaining C1-C1/P2: the CLIENT_DESTINATION_MAPPING_CHECK
published by the C1-correction package
(PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_C1_REPORT_QC_CORRECTION_R1_20261004,
BASE 97bdf95) confirms only that at the documented VA there exists an
instruction writing the declared displacement — it does NOT prove payload
index / field identity → the correct store instruction → the correct
destination. NO new placement RE.

**COMPLETE. The defect was reproduced FIRST on the pristine BASE historical
verifier (private copy only): the exact Desktop mutant C false PASS
(PAYLOAD_FIELD_DECODE_CHECK=PASS, CLIENT_DESTINATION_MAPPING_CHECK=PASS,
FULL_QC=QC_PASS) reproduced as expected. The corrected gate validates THREE
identities simultaneously (payload field identity → store instruction identity
→ destination field identity) against an INDEPENDENT, HARD-CODED
parser-sequence oracle byte-backed from the pinned EXE; the canonical table
remains PASS (corrected full QC 10/10 QC_PASS), the POST-FIX battery detects
mutants A, B and the mandatory mutant C (each FAIL with FULL_QC=QC_FAIL), and
the canonical-copy negative control passes. C1_C1_PAYLOAD_INDEX_TO_STORE_IDENTITY
= FIXED_AND_VERIFIED; C1 = CLOSED_FOR_AUDITED_STATE.**

## 1. The defect, reproduced first (BASE, private copies only)

`01_RAW/BASE_MUTANT_C_REPRODUCTION.json` (historical verifier imported
READ-ONLY, SHA256 CB4587C19ACBD4B7B9DE798A598251D63D97C0DE0CDB5BF80CC09BAA98E734E8;
`sys.dont_write_bytecode` guaranteed no `__pycache__` in the historical package —
verified):

| Step | Result |
|---|---|
| BASE canonical QC (pristine state re-measured) | **QC_PASS 10/10** (TQ1 PASS, TQ2 PASS) |
| BASE A/B mutation falsifier | **DETECTED** (mutant A and mutant B, published behavior reproduced) |
| BASE mutant C (private document copy, SHA256 7C0809CD...; EXE unchanged, VFS unchanged, canonical docs unchanged) | **PAYLOAD_FIELD_DECODE_CHECK=PASS, CLIENT_DESTINATION_MAPPING_CHECK=PASS (the FALSE PASS), FULL_QC=QC_PASS (the FALSE PASS)** |

Mutant C swaps ONLY the destination documentation:
payload[1](A) → template+0x04 → `MOV [EDI+0x04],EAX @0x00730D14` AND
payload[2](B) → template+0x08 → `MOV [EDI+0x08],EAX @0x00730CE6`. Both VAs are
REAL stores with MATCHING displacements — but they belong to the OTHER payload
field. The historical verifier's per-row verdicts on the mutant (recorded in
full in 01_RAW): every row `dest_eq_disp=True`, `bytes_match=True`, `pass=True`.
**BASE_MUTANT_C_FALSE_PASS_REPRODUCED = YES.**

## 2. Root cause (per Desktop; confirmed by reading the historical verifier)

`verify_destination_table` parses idx/name/dest/disp/va but row validity checks
only `dest == instruction-displacement` AND `bytes at VA match the opcode
implied by dest`. idx/name do not constrain which store instruction belongs to
which payload field — a document row can point at ANY real MOV with the right
displacement. Mutant C is exactly that class: both rows are real, byte-correct,
displacement-consistent stores — of the wrong payload fields.

## 3. The fix — three simultaneous identities against an independent oracle

The corrected gate (`03_SCRIPTS/qc_targeted_c1c1.py` TQ2) judges every
documented row against a HARD-CODED parser-sequence oracle, never against the
document's own rows:

- **ORACLE (hard-coded, in the script, before the document is read):**
  payload[0]/id2 → store VA 0x00730CB6 → template+0x00 → bytes 89 07;
  payload[1]/A → store VA 0x00730CE6 → template+0x08 → bytes 89 47 08;
  payload[2]/B → store VA 0x00730D14 → template+0x04 → bytes 89 47 04;
  payload[3]/C → store VA 0x00730D42 → template+0x0C → bytes 89 47 0C;
  payload[4]/D_f32 → FLD VA 0x00730D69 → FSTP VA 0x00730D70 → template+0x10
  (D9 04 10 / D9 5F 10). The oracle is byte-backed at runtime
  (`verify_oracle`): pinned-EXE SHA must match AND the exact instruction bytes
  must be present at these VAs AND the store VAs must strictly increase with
  payload index (normal parser instruction order); any mismatch fails closed.
- **Per row the corrected gate requires ALL of:**
  1. PAYLOAD FIELD IDENTITY — documented payload index == expected payload
     index AND documented semantic name == expected audited field identity;
  2. STORE INSTRUCTION IDENTITY — documented store VA == the store VA the
     oracle independently assigns to that payload index;
  3. DESTINATION FIELD IDENTITY — documented destination == the destination
     of that same independently assigned instruction (and documented
     instruction displacement == that destination);
  plus actual EXE bytes at the oracle VA == expected instruction bytes, and
  table completeness (exactly one row per expected payload index, no unexpected
  payload rows, the D row present).
- A row pointing at "a real MOV to the right displacement somewhere else" can
  never substitute for the correct store of that payload index: the owner of
  the documented VA is looked up in the ORACLE, and the failure reason names
  the true owner (e.g. "documented store VA 0x00730D14 is the store of
  payload[2] (B) per the independent parser-sequence oracle, NOT the store of
  payload[1] (A)").

**ANTI-CIRCULARITY (explicit):**
- MEASURED_QUANTITY = payload-index to exact-store-VA identity.
- INDEPENDENT_SOURCE_OF_TRUTH = pinned Entropia.exe bytes (SHA256 E7785430...
  byte-verified at runtime) + the independently fixed normal parser
  instruction order of FUN_00730C90 (payload fields are read in payload order,
  each store follows its read; the six store/FLD/FSTP VAs strictly increase
  with payload index; per-field read→store→zero adjacency recorded in
  01_RAW/ORACLE_EVIDENCE.json).
- WHY_NON_CIRCULAR = the document row under test cannot choose an arbitrary
  correct MOV and thereby change the payload-index identity: the expected
  payload-index → store-VA → destination mapping is fixed BEFORE and
  INDEPENDENT of the tested document and byte-backed from the pinned EXE. The
  tested PARSER_CHAIN table is NEVER used to generate the expected mapping.
- FAILURE_CASE_DETECTED = Desktop mutant C (BASE false PASS:
  01_RAW/BASE_MUTANT_C_REPRODUCTION.json; POST-FIX detection:
  01_RAW/QC_MUTATION_BATTERY_POST_FIX.json).

## 4. POST-FIX mutation battery (01_RAW/QC_MUTATION_BATTERY_POST_FIX.json)

All cases run the CORRECTED full QC against a PRIVATE copy of the 8 tested
documents with only PARSER_CHAIN.md mutated; the full QC is re-run per case
and FAILS whenever TQ2 (the mapping check) fails. Raw VFS values unchanged in
every case (TQ1 PASS everywhere proves it).

| Case | Document SHA256 | PAYLOAD_FIELD_DECODE | PAYLOAD_INDEX_STORE_IDENTITY | CLIENT_DESTINATION_MAPPING | FULL_QC | Detected |
|---|---|---|---|---|---|---|
| canonical copy (negative control) | 6BA91A1F... (byte-identical to the canonical disk file — the private-copy pipeline is content-neutral) | PASS | PASS | PASS | QC_PASS | n/a (must PASS — it does) |
| mutant A (destination-cell-only swap) | 0AEC1DB4... | PASS | **FAIL** | **FAIL** | **QC_FAIL** | **YES** |
| mutant B (destination+displacement swap, old VAs) | 2901BD57... | PASS | **FAIL** | **FAIL** | **QC_FAIL** | **YES** |
| mutant C (destination+displacement+MATCHING REAL STORE VA swap) | 7C0809CD... (byte-identical to the BASE-reproduction mutant document) | PASS | **FAIL** | **FAIL** | **QC_FAIL** | **YES** |

MUTANT_A_DETECTED = YES; MUTANT_B_DETECTED = YES; MUTANT_C_POST_FIX_DETECTED =
YES. The per-row oracle-grounded reasons for mutant C are recorded verbatim in
the battery JSON (STORE INSTRUCTION IDENTITY FAIL + DESTINATION FIELD IDENTITY
FAIL + displacement mismatch per mutated row).

## 5. Corrected canonical QC (01_RAW/QC_TARGETED.json)

Corrected full QC on the canonical document: **QC_PASS 10/10** (TQ0 identities,
TQ1 PAYLOAD_FIELD_DECODE_CHECK, corrected TQ2 with
PAYLOAD_INDEX_STORE_IDENTITY_CHECK=PASS and CLIENT_DESTINATION_MAPPING_CHECK=PASS,
TQ3 CLASS_SELECTOR 0x4E26=20006 vs PROPERTY_TAG 6, TQ4 receiver provenance,
TQ5 failure-path zero-write, TQ6 instruction-start negative/positive byte
controls, TQ7 next-experiment wording, TQ8 S1 facts preserved, TQ9 forbidden
overclaims absent). TERMINAL canonical gate values:
PAYLOAD_FIELD_DECODE_CHECK = PASS; CLIENT_DESTINATION_MAPPING_CHECK = PASS;
PAYLOAD_INDEX_STORE_IDENTITY_CHECK = PASS.

## 6. Oracle evidence (01_RAW/ORACLE_EVIDENCE.json)

Six pins byte-verified against the pinned EXE (independently re-verified with
this run's own PE section-table mapper; PE-MASTER byte-verified the same six
pins at dispatch): id2 store 89 07 @0x00730CB6; A store 89 47 08 @0x00730CE6;
B store 89 47 04 @0x00730D14; C store 89 47 0C @0x00730D42; D FLD D9 04 10
@0x00730D69; D FSTP D9 5F 10 @0x00730D70. Per-field normal read/store/zero
sequence recorded (reads @0x00730CAB / 0x00730CDF / 0x00730D0D / 0x00730D3B /
FLD @0x00730D69; store VA order strictly increasing with payload index). 
Additional closed class recorded (oracle property, NOT a battery case):
`FSTP [EDI+0x10]` (D9 5F 10) has a byte-identical twin at the zero-path site
0x00730D7C — a document row pointing the D store at 0x00730D7C would ALSO have
passed the BASE verifier (same bytes); only the VA identity of the corrected
oracle rejects it.

## 7. Supersession (see SUPERSESSION_LEDGER.md)

Superseded (detection-scope claims ONLY — the payload mapping itself is
unchanged): the C1-correction package's "The Desktop-counterexample blind spot
is closed" and equivalent detection-scope wordings that credited the A/B
falsifier with full mapping validation. Preserved unchanged: the canonical
mapping (A→+0x08, B→+0x04 pairing — now verified at identity level), all
published byte evidence, the narrowed QC-7 scope, the zero-write failure-path
description, the instruction starts, the CLASS_SELECTOR/PROPERTY_TAG layered
identity. Bounded P3: the ORIGINAL_EXCERPT correction is recorded in this
package's ledger (no historical file was edited).

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

(Canonical-state gate values: the corrected CLIENT_DESTINATION_MAPPING_CHECK
and PAYLOAD_INDEX_STORE_IDENTITY_CHECK PASS on the canonical table; the mutant
C INPUT FAILS them — see section 4. C1 = CLOSED_FOR_AUDITED_STATE is scoped to
the audited state — the pinned EXE + the canonical destination table + the
A/B/C mutation battery — and claims nothing beyond it.)

## Not-superseded canonical state (explicitly preserved, no upgrades)

C2_CLASS_SELECTOR_PROPERTY_TAG = CLOSED_FOR_AUDITED_STATE (CLASS_SELECTOR
0x4E26 = 20006, PROPERTY_TAG 6); S1_STATIC_MECHANISM = PRESERVED_CONFIRMED;
PARSER_TO_RUNTIME_DEFINITION_SEAM = CONFIRMED; RECORD_A {id2=16083, A=410620,
B=0, C=0, D_f32=0.49950098991394043}; RECORD_B {id2=4508, A=296445, B=296446};
PLACEMENT_CONSUMER_EDGE = STRONGLY_SUPPORTED (level unchanged);
PHYSICAL_RECORD_TO_PLACEMENT_ATTRIBUTE = NOT_ESTABLISHED;
WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO. The
A→+0x08 / B→+0x04 destination pairing is UNCHANGED and remains valid — it is
now guarded at identity level instead of only at displacement level.

## Evidence index (this package)

- `01_RAW/BASE_MUTANT_C_REPRODUCTION.json` — the defect reproduced on the
  pristine BASE historical verifier (BASE canonical QC_PASS 10/10 + BASE A/B
  falsifier DETECTED + BASE mutant C false PASS with per-row historical
  verdicts).
- `01_RAW/QC_TARGETED.json` — corrected full QC, canonical, QC_PASS 10/10,
  with the corrected TQ2 (three identities + oracle byte-backing + per-row
  expected-vs-documented records).
- `01_RAW/QC_MUTATION_BATTERY_POST_FIX.json` — POST-FIX battery: canonical
  negative control PASS; mutants A/B/C FAIL with per-row oracle-grounded
  reasons, document SHAs, mutation rows, full-QC FAIL propagation.
- `01_RAW/ORACLE_EVIDENCE.json` — the six byte-verified pins, the per-field
  normal read/store/zero sequence, the strictly-increasing store VA order, the
  FSTP byte-identical-twin note, and 6 bounded EXE byte windows.
- `03_SCRIPTS/qc_targeted_c1c1.py` — the bounded instrument (modes:
  base_repro | normal | battery | oracle; read-only vs all originals and the
  historical package; private mutation copies only, temp-root cleanup).
- `03_SCRIPTS/make_manifest.py` + `COMMITTED_PACKAGE_MANIFEST_SHA256.csv` —
  manifest generated LAST, self-excluded.
- `SUPERSESSION_LEDGER.md` — the supersession update (detection-scope claims)
  + the bounded ORIGINAL_EXCERPT P3 correction record.
- `INPUT_IDENTITIES.md` — all input identities (EXE/VFS/document/instrument
  SHAs, BASE/remote verification).
- `QC_TARGETED_REPORT.md` — the targeted QC records (gate table + battery
  table + BASE reproduction table).

## COMMITTED PACKAGE MANIFEST SCOPE (declared explicitly)

`COMMITTED_PACKAGE_MANIFEST_SHA256.csv` covers EXACTLY the files committed by
this run minus the manifest itself:

- every file of THIS package (docs/audits/PE_935_PARAMETER_RECORD_C1_C1_STORE_
  IDENTITY_QC_R1_20261004/) except the manifest;
- `AUDIT_ENTRYPOINT.md` (one new LATEST RUNS row).

NO historical package file was edited (the R1 package, the C1-correction
package, and all other historical packages are byte-identical to BASE 97bdf95;
`git status` confirms no tracked-file modification). The historical C1
correction script was imported READ-ONLY for the BASE reproduction.

## Honest boundaries

1. SELF_CHECK only (QC_SCOPE = SELF_CHECK_C1_C1_STORE_IDENTITY) — no
   independent-QC claim; the PE-MASTER review of this package is pending.
2. STATIC-ONLY: no client launch, no runtime observation, no Ghidra, no
   network; all instruction identities are byte reads from the pinned
   Entropia.exe with this run's own PE mapper (section-table-driven; no
   offset==RVA assumption).
3. C1 = CLOSED_FOR_AUDITED_STATE is scoped: the corrected gate proves the
   payload-index → store-VA identity for the audited five payload fields of
   FUN_00730C90 against the pinned EXE; it does not claim anything about
   other parsers, other fields, or runtime behavior.
4. In-run process note (honest record): the first private-copy executions
   wrote the mutated documents with CRLF newline normalization (Windows text
   mode), so their document SHAs were not directly comparable to the LF-ending
   canonical file. The instrument was corrected to preserve LF (`newline="\n"`)
   and ALL modes were re-run; the published records are the corrected ones
   (canonical private copy byte-identical to the canonical disk file
   6BA91A1F...; the BASE-reproduction and battery mutant C documents are
   byte-identical 7C0809CD...). No verifier logic changed between the runs;
   all verdicts were identical in both executions.
5. The corrected checker lives as a NEW bounded script in THIS package
   (03_SCRIPTS/qc_targeted_c1c1.py). The historical C1-correction script is
   preserved byte-identical (READ-ONLY); its published QC record is a
   historical measurement record and remains untouched — the supersession is
   recorded in THIS package's ledger, not by rewriting history.
6. Next placement experiment NOT executed (terminal HARD STOP per contract):
   the SPECIFIC_GETTER_RESULT_PROVENANCE experiment remains designed-not-
   executed exactly as worded in the R1/C1-correction docs (TQ7 re-verifies the
   wording is intact).
