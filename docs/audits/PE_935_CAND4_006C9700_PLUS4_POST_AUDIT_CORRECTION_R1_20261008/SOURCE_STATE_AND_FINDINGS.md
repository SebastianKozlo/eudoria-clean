# SOURCE_STATE_AND_FINDINGS — PE_935_CAND4_006C9700_PLUS4_POST_AUDIT_CORRECTION_R1_20261008

RUN_CLASS: RECORDS_AND_QC_MACHINERY_CORRECTION (NEW_SCIENCE_EXECUTED = NO;
NEW_PCG_FUNCTION_BODIES = 0; NEW_PCG_SCIENCE_EDGE_INTERPRETATIONS = 0;
QC_REPAIR_ROUNDS_MAX = 1). Executor: pe-reconstruction (bounded worker phase
under direct PE-MASTER dispatch; NO_NESTED_TASKS). Era label for every
physical fact cited in this package: PCG 9.3.5 client image (Entropia.exe,
8015872 B / SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31).

## 1. Preflight verdict (queries in INPUT_IDENTITIES.md §1-§2)

PASS. LOCAL_HEAD == origin/master == live ls-remote == EXPECTED_BASE_SHA
fd481c567868b601ffa4be442ab55a7cffaeacd6 (first attempt, no retry needed).
OUTPUT_REPO_PATH absent at preflight; zero tracked changes; the six foreign
untracked paths recorded and untouched. All seven pinned inputs (contract,
three Desktop post-audit files, original microrun contract, engine-research
report, EXE) measured SIZE+SHA256 MATCH. The Desktop post-audit REPORT.md,
SCOPE_REASSESSMENT.csv and COUNTERCHECKS.json were read IN FULL before any
work, as the contract §1 requires.

## 2. Source package state (READ_ONLY)

`docs/audits/PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008/` — 28 files,
each byte-identical to its BASE Git blob (census in INPUT_IDENTITIES.md §4;
28/28 OK, 0 mismatches). Nothing in the package was modified, repaired,
re-run or staged by this run. Its historical QC_PASS
(QC_REPORT.md) and MASTER_ACCEPTED (PE_MASTER_REVIEW.md) remain authentic
historical artifacts; their STANDING USE as acceptance of the alias (T==P),
the scope compliance (WITHIN / 12-12 / "no 13th unit") and the P heap origin
is WITHDRAWN per SUPERSESSION_LEDGER.csv (HISTORICAL_OVERALL_ACCEPTANCE =
SUPERSEDED_IN_AFFECTED_SCOPE; HISTORICAL_MECHANICAL_PIN_RESULTS = PRESERVED).
The AUDIT_ENTRYPOINT.md row of that package (line 31) carries the same
withdrawn standing use; the entrypoint EDIT is the parent's later phase
(ledger row FD-C2/SL-16).

## 3. REC-W — complete occurrence census of the contradictory records

Census method: pattern search for `E8 35 F0 02 00`, `2F035`, `E8 75 F0 02 00`,
`2F075`, `006CB836`, `006FA8B0` over the whole source package + AUDIT_ENTRYPOINT
mentions. Every occurrence is classified as (A) an ACTIVE WRONG claim, (T) a
TRUE description of the earlier mistake (process disclosure — historically
authentic, NOT an active claim), or (C) a CORRECT active record.

### 3.1 The contradictory ACTIVE records (superseded by ACTIVE_CORRECTED_PINS.json)

| # | location | the wrong active record | why wrong |
|---|---|---|---|
| A1 | SOURCE_STATE.md line 112 | `ctor FUN_006FA8B0(W, saved R) @0x006CB836 (E8 35 F0 02 00);` | the physical bytes at 0x006CB836 are E8 75 F0 02 00 (own read, INPUT_IDENTITIES.md §6); E8 35... is the transcription error this same package documents as caught and corrected |
| A2 | 01_RAW/PINS_AND_REL32.txt line 113 | `0x006CB836 -> 0x006FA8B0 (historical W ctor, +0x2F035);` | internally inconsistent: 0x006CB83B + 0x2F035 = 0x006FA870 != 0x006FA8B0; the measured displacement is +0x2F075 |
| A3 | 01_RAW/PINS_AND_REL32.txt lines 136-137 | `... 0x006CB836 E8 35 F0 02 00; the L20 window sequence) == PLACEMENT_RECORD_BRIDGE ... byte-identical after signed-byte conversion` | the prior L20 record agrees with the PHYSICAL EXE (E8 75 F0 02 00; Ghidra signed rendering "-18 75 -10 02 00" where 75 is POSITIVE 0x75); the E8 35 transcription does NOT match the prior record |

### 3.2 TRUE descriptions of the earlier mistake (kept, historically authentic — NOT wrong claims)

| # | location | the description |
|---|---|---|
| T1 | 01_RAW/PINS_AND_REL32.txt lines 92-95 | the CORRECTED record itself: `hist_caller_ctor_call @0x006CB836: E8 75 F0 02 00 (->0x006FA8B0; ctor(W, saved R); PROCESS DISCLOSURE: the run's first draft transcription read E8 35 F0 02 00; the physical-EXE checker caught it (clean-pass attempt 1 FAIL at this pin); corrected to the MEASURED bytes` |
| T2 | 01_RAW/MANUAL_ENCODING_CROSSCHECK.txt lines 69-78 | item 13: `E8 75 F0 02 00 @0x006CB836: rel32 = +0x2F075; 0x006CB83B + 0x2F075 = 0x006FA8B0. MATCH.` + the full PROCESS DISCLOSURE (the E8 35 first transcription; the gate catch `FAIL PIN:HIST_CALLER_CTOR_CALL`; the 80/80 re-run; the prior record never altered) |
| T3 | HANDOFF.md lines 142-145 | `one executor transcription error (E8 35... -> E8 75 F0 02 00 @0x006CB836) CAUGHT by the production gate itself on clean-pass attempt 1 and corrected before any evidence was accepted.` |
| T4 | PE_MASTER_REVIEW.md line 32 | `Disclosed: one executor transcription error (E8 35…→E8 75 F0 02 00 @0x006CB836) caught by the production gate itself ...` |

### 3.3 CORRECT active records (agreement set — cited as prior-record evidence)

| # | location | the correct record |
|---|---|---|
| C1 | 03_SCRIPTS/checker_plus4.py lines 140, 162 | pin `("HIST_CALLER_CTOR_CALL", 0x006CB836, "E8 75 F0 02 00")`; rel32 `("REL_HIST_WCTOR", 0x006CB836, 0x006FA8B0)` |
| C2 | 00_CONTROL_INTERNAL_QC/qc_independent_check.py lines 215-216, 257 | the QC pin `("hist_caller_w_ctor_call", 0x006CB836, "E8 75 F0 02 00", ...)` and rel32 `("prior_hist_wctor", 0x006CB836, 0x006FA8B0)` |
| C3 | 00_CONTROL_INTERNAL_QC/QC_RESULTS.json lines 286-290, 481-486 | expected/measured `E8 75 F0 02 00`; own_target/expected_target `0x006fa8b0` |
| C4 | 00_CONTROL_INTERNAL_QC/QC_PHASE_INPUTS.md line 48 | `corrected bytes E8 75 F0 02 00; verify against the physical EXE` |
| C5 | QC_REPORT.md line 89 | the 26/26 anchor row: `hist. FUN_006FA8B0(W,R) prior record | 0x006CB836 | E8 75 F0 02 00 | E8 75 F0 02 00 | MATCH — the CORRECTED transcription is the physically true one (rel32 +0x2F075 → 0x006FA8B0)` |
| C6 | Desktop COUNTERCHECKS.json | `REL_HIST_WCTOR: va 0x6cb836 ... measured_target 0x6fa8b0` (independent Desktop re-measure) |

### 3.4 Disposition (REC-W)

The single active record is established in **ACTIVE_CORRECTED_PINS.json**
(CALLSITE_VA 0x006CB836; BYTES E8 75 F0 02 00; SIGNED_REL32 +0x2F075;
NEXT_VA 0x006CB83B; TARGET_VA 0x006FA8B0; TARGET_FORMULA = CALLSITE_VA + 5 +
signed_little_endian_int32(BYTES[1:5])) — after THIS run's own physical read
of the 5 bytes (file offset 0x2CB836) and own signed-rel32 recompute, in
agreement with the correct prior record (MANUAL_ENCODING_CROSSCHECK.txt
item 13; exact path, Git blob SHA1 eea2876a460d871a37ea03daee38edd9702323f1,
SHA256 540CA5839C00DE0299EA3DCC1392CDF666ECC00AF4EB827C8E887C1D43F750AF and
quote recorded inside the JSON). The successor gate validates the JSON
against the physical bytes and its own arithmetic (RECW:* gates); the three
mutation controls (byte-hex-only / displacement-only / target-only) each flip
the corresponding production record gate, proving the JSON drives the gate
(MAPPER_RESULTS.json → w_record_mutation_gates). The source package was NOT
edited; the callee FUN_006FA8B0 was NOT opened. No occurrence of the wrong
records exists outside the source package in this run's outputs.

## 4. The Desktop findings — accepted, with this run's disposition

All five findings of the pinned Desktop post-audit
(REQUIRE_CORRECTIONS verdict) are ACCEPTED as findings and dispositioned by
this records-and-QC-machinery run:

- **FD-C1 (P2 — false edge count / false WITHIN)** — DISPOSITIONED:
  HISTORICAL_SCOPE_REASSESSMENT.csv reconstructs the conservative minimum
  from the RECORDED CONTENT (17 floor units: E1..E12 kept + R-3/R-6/R-7/
  R-8/R-9 with exact quotes; R-1/R-2/R-4/R-5 = NOT_ADJUDICATED_FOR_EXACT_
  COUNT, charge 0 ≠ confirmed exclusion); BODY_SCOPE_REASSESSMENT.csv gives
  the 5-body floor (four reported bodies + the described neighbor 0x006C9820
  — NOT read from the EXE, semantics NOT developed). Resulting records:
  MINIMUM_NEW_ANALYZED_CALLSITE_UNITS = 17; EXACT = UNRESOLVED;
  ORIGINAL_MAX_NEW_INTERPROCEDURAL_EDGES = 12; ORIGINAL_EDGE_BUDGET_
  COMPLIANCE = FAIL; MINIMUM_NEW_FUNCTION_BODIES_OPENED = 5; EXACT =
  UNRESOLVED; ORIGINAL_MAX_NEW_FUNCTION_BODIES = 6; BODY_BUDGET_EXCEEDANCE_
  ESTABLISHED = NO; ORIGINAL_SCOPE_COMPLIANCE = FAIL; RETROACTIVE_PRIOR_
  AUTHORIZATION = NO. The old limits are NOT changed; the visible 21-CALL
  census is NOT treated as 21 semantic units.
- **FD-C2 (P2 — first init does not prove T==P at use)** — DISPOSITIONED:
  CORRECTED_CLAIM_MATRIX.csv (R_PLUS4_VALUE_PRESERVED_TO_LATER_USE =
  NOT_ESTABLISHED; T_EQUALS_FIRST_INITIAL_P = NOT_ESTABLISHED_WITHIN_BOUND;
  ACTUAL_LATER_OVERWRITE_OBSERVED = NO) + SUPERSESSION_LEDGER.csv rows
  FD-C2/SL-9..SL-19 (CL-13/HP-3 and the dependents CL-15/CL-20 limited to the
  store level; the report/review/handoff/entrypoint standing uses withdrawn).
  The reachable conditional branch passing &R+8 to the unopened FUN_006B2310
  is recorded as a GAP in the write-effects/frame proof — the helper is NOT
  assumed to preserve R+4 and it is NOT claimed to overwrite; the body was NOT
  opened. The synthetic helper `[this-4]:=Q` countermodel + the
  field-preserving model are built as LOGICAL controls
  (LOGICAL_CONTROL_RESULTS.json; LOGICAL_CONTROLS_SCOPE = SYNTHETIC_ONLY);
  neither resolves how the real FUN_006B2310 works.
- **FD-C3 (P2 — heap origin of P without return provenance)** — DISPOSITIONED:
  CORRECTED_CLAIM_MATRIX.csv (P_HEAP_ORIGIN = NOT_ESTABLISHED;
  P_ALLOCATION_OR_STORAGE_ORIGIN = NOT_ESTABLISHED_WITHIN_BOUND; the
  measured ADD/DEC/vtable dispatch preserved as protocol facts; ownership
  interpretation = intrusive-refcount-like; exact class and storage UNKNOWN)
  + SUPERSESSION_LEDGER.csv rows FD-C3/SL-20..SL-24. No T-use evidence is
  transferred to P without a temporal identity edge; [R+4] is not identified
  with [P+4]/[T+4]; manager+0x68=T is not identified with manager+0x68=P.
- **name-taking wording** — DISPOSITIONED: slot +0x44 / slot 17 and the
  "Geowater:0" argument establish P_NAME_TAKING_VIRTUAL_CALL =
  CONFIRMED_IN_RECORDED_STATIC_SCOPE; LOOKUP_SEMANTIC = UNRESOLVED; it is
  never called proof of GetObjectByName / GetExtraData / child lookup / main
  visual (CORRECTED_CLAIM_MATRIX.csv; E10's note in the scope CSV). The
  research guardrails (D = *(S+0x10); H0; C; C==H0 NOT_ESTABLISHED; the
  slot-3 argument = C or 0 on the allocation-failure path; P = final EAX,
  return source unopened) are recorded as GUARDRAILS ONLY — no new trace was
  performed; Q/H are NOT added as one confirmed identity; NiPointer /
  result-holder / cache / clone remain hypotheses, not PCG class names; a
  load after a callback does not prove a callback writer; 4 B size and a
  zero store do not resolve the smart-pointer class.
- **REC-W** — DISPOSITIONED (see §3).
- **TOOL-MAP** — DISPOSITIONED: the successor checker
  (03_SCRIPTS/checker_plus4_successor.py) with the full range boundary:
  classification RAW_BACKED / VIRTUAL_BSS / UNMAPPED / REJECTED_INVALID_INPUT
  separated from the physical read; whole-range checks (PE32 header with
  measured ImageBase; n>0; no under/overflow; unambiguous section; delta =
  rva - VirtualAddress; delta+n <= SizeOfRawData; PointerToRawData+delta+n
  <= file size; exactly n bytes returned; no zeros fabricated; raw padding
  classified RAW_BACKED per the explicit PHYSICAL_FILE_MAPPER_POLICY — never
  a runtime observation; header VAs UNMAPPED). ALL physical reads — including
  the RTTI COL 20 B and TypeDescriptor/name reads — go through the same API.
  Required mapper/record controls 1-7 executed and PASS (102/102 cases);
  MC1-MC5 reproduced on the successor production gate (each FAILs exactly on
  the proper anchor, in-memory TEST-OVERRIDE copies only); MC6 executed as a
  DIRECT physical file offset 0x7A1100 mutation (a .rsrc raw byte — NOT a
  read of VA 0x00BA1100; VA and file offset are separate units) with all
  86 gates staying PASS; the historical 80-check-ID regression PASS
  (complete ID set from the historical checker itself, parsed read-only via
  AST; successor tables element-identical; 80/80 on the clean physical
  baseline). The historical checker_plus4.py was NOT repaired in place; the
  successor is a bounded checker, NOT a universal PE/x86 framework;
  GENERAL_PE_MAPPER_CORRECTNESS = NOT_ESTABLISHED.

## 5. Preserved backlog (recorded, OPEN — not corrected in this records-only run)

From the source package (its QC F-rows — preserved as recorded backlog):

- **F-1 (P3)**: notation residue `8B F0?` in 01_RAW/PINS_AND_REL32.txt line 90
  (the hist_caller_null_check row; the cited prior record is physically
  85 F6 = TEST ESI,ESI @0x006CB811 — the fragment is a leftover, not a
  measurement). OPEN P3.
- **F-2 (P2)**: the historical checker OwnPE.va_to_off raw-vs-virtual
  boundary defect — dispositioned for THIS run by the TOOL-MAP successor +
  controls; the HISTORICAL file stays unmodified (ledger row TOOL-MAP/SL-28).
  The historical checker is not certified for general reuse.
- **F-3 (P3)**: rel32 notation residue `-0x2701+... = 0x26FF` at
  01_RAW/PINS_AND_REL32.txt line 111 for callsite 0x006C6FFC (physically
  +0x26FF; target correct). OPEN P3.

New P3 extent-metadata notes (Desktop post-audit §6; recorded as OPEN P3
backlog — description-only inconsistencies; the hexes are byte-identical to
the EXE per the Desktop body_windows measurements and this run does NOT
re-measure them):

- **F-4 (P3, new)**: the ctor FUN_006E8F70 record declares extent 184 B
  (0x006E8F70..0x006E9027) but the recorded body hex is 186 B, ending at
  0x006E9029 (the end of the three-byte RET C2 08 00 @0x006E9027 — the
  declared end lands mid-instruction).
- **F-5 (P3, new)**: the getter FUN_007B79B0 record declares window 96 B
  (0x007B79B0..0x007B7A0F) but the recorded hex is 95 B, ending at
  0x007B7A0E.

Both are OPEN P3 descriptions in the READ_ONLY source package; they were
NOT corrected (records-only scope; the source stays unedited).

## 6. Standing ceilings preserved verbatim (unchanged by this correction)

```text
CHILD_RESOURCE_PROVENANCE = STRONGLY_SUPPORTED_MODEL_DERIVED
MODEL_ROOT_RELATION = UNKNOWN
CHILD_VISUAL_ROLE = UNRESOLVED
CHILD_TO_JOIN_IDENTITY = STRONGLY_SUPPORTED
EXACT_PARENT = CONFIRMED_EXACT_SCENEFEEDER_PLUS_30
PARENT_SCOPE = EXAMINED_ACLD_PLUS_18_SF_INSTANCE
JOIN_OPERATION = STRONGLY_SUPPORTED
CAND4_CHILD_ROOT_CLOSURE = NOT_ESTABLISHED_WITHIN_BOUND
WORLD_INSTANCE = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED
HISTORICAL_INSTANCE_DATA_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
NEW_DESKTOP_POST_AUDIT = NOT_PERFORMED
GENERAL_PE_MAPPER_CORRECTNESS = NOT_ESTABLISHED
NEXT_EXPERIMENT_AUTHORIZED = NO
```

HISTORICAL_MECHANICAL_PIN_RESULTS = PRESERVED (the 80/80 clean pass, the
anchor pins, the RTTI/string reads — re-verified by the successor);
HISTORICAL_OVERALL_ACCEPTANCE = SUPERSEDED_IN_AFFECTED_SCOPE; ORIGINAL_SCOPE_
COMPLIANCE = FAIL (now standing); CORRECTION_RECORDS_QC = NOT_PERFORMED_BY_
EXECUTOR (the fresh-context QC of THIS correction run is the parent's
separate phase — no self-review is labeled independent).

## 7. Write scope and phase boundary

This executor phase wrote ONLY under OUTPUT_REPO_PATH
(docs/audits/PE_935_CAND4_006C9700_PLUS4_POST_AUDIT_CORRECTION_R1_20261008/):
AUTHORIZATION_RECORD.md, INPUT_IDENTITIES.md, SOURCE_STATE_AND_FINDINGS.md,
ACTIVE_CORRECTED_PINS.json, HISTORICAL_SCOPE_REASSESSMENT.csv,
BODY_SCOPE_REASSESSMENT.csv, CORRECTED_CLAIM_MATRIX.csv,
SUPERSESSION_LEDGER.csv, MAPPER_RESULTS.json, REGRESSION_RESULTS.json,
LOGICAL_CONTROL_RESULTS.json, 03_SCRIPTS/checker_plus4_successor.py,
03_SCRIPTS/run_correction_controls.py. NOT created by this phase (parent's
later phases): QC_RESULTS.json / QC_REPORT.md / qc_countercheck.py (the fresh
QC worker), PE_MASTER_REVIEW.md, FINAL_REPORT.md, EVIDENCE_INDEX.md,
HANDOFF.md, MANIFEST_SHA256.csv (LAST), the AUDIT_ENTRYPOINT.md correction
row, the commit/push. Nothing was staged; no historical file, no foreign
untracked path and no file outside OUTPUT_REPO_PATH was modified; python -B
everywhere (no __pycache__ residue); scratch work stayed in the temp dir.
