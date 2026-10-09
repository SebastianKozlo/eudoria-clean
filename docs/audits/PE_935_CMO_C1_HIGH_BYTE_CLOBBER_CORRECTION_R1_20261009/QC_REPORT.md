# QC_REPORT.md — PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009

**FRESH-CONTEXT INTERNAL QC** of the machinery/control correction run
`PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009` (executor phase:
pe-reconstruction).

**REAL ORIGIN**: pe-master-auditor fresh-context internal QC, internal to
PE-MASTER — **NOT** an independent Desktop post-audit, **NOT** executor
self-review.

- QC_RUN_ID = `PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009_INTERNAL_QC_R1`
- Contract = `C:\Users\User\Documents\ChatGPT\PE\PE_CMO_C1_HIGH_BYTE_CORRECTION_PROMPT_20261008\OPENCODE_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009.md`
  — 16623 B / SHA256 `61AAA55854942A22085F3767A7D64512248EDFAE3A7B9BB54A5CBE36F36D3981`
  — identity verified MATCH before any QC work.
- Machine-readable record: `QC_RESULTS.json` (this package; generator
  `03_SCRIPTS/qc_run_controls.py`, python -B; decoder
  `03_SCRIPTS/corrected_qc_decoder.py`).
- QC_VERDICT = **QC_PASS** (all 11 acceptance gates of contract section 11
  hold with this QC's own independent measurements; see below).

---

## 1. Method

The QC implemented its own corrected QC decoder
(`03_SCRIPTS/corrected_qc_decoder.py`, 23454 B / SHA256
`88460076843BDA7DFD51BC1182422E1F98FF13EEC493F14304BACC92FA7B0919`) as the
successor of the historical QC decoder (`qc_remeasure.py` my_decode lineage:
GPR/GPR8/GPR16 tables, my_modrm/_mem_str/my_decode/linear_decode over a PE
image object, QcDecodeError fail-closed). Independence from the production
`corrected_executor_decoder.py`:

- the production mapping helper (`BYTE8_PARENT` / `BYTE8_BIT_RANGE` dict
  literals) was **NOT** imported, copied or transcribed;
- the parent attribution is implemented **arithmetically** from the x86-32
  byte-register encoding (`byte_parent(idx) = GPR[idx & 3]`;
  `byte_bits(idx) = [8,16) iff idx >= 4` — no REX in this window);
- the alias matrix reference (`QC_REF_BYTE8`) is an **explicit literal table**
  defined inside the runner — a different construction than the decoder's
  arithmetic helper, so a bug in either would be caught by the other;
- the QC provenance gate (`qc_value_provenance_gate`) is the QC's own
  implementation of the SAME production predicate semantics (byte pins at
  0x0085B1DA / 0x0085B24B / 0x0085B27A / 0x0085B27F / 0x0085B281, rel32
  recomputation to 0x00746560, accessor bytes, EDI and ECX
  reaching-definition scans), with NO hard-coded mutant expectation — the
  identical checks run for the clean window and for every mutant.

Historical reproduction method: both historical decoders were **AST-extracted
by the QC itself** (never executed at top level, never imported as modules;
free-name sets verified; the executor scan comprehension at source lines
444-446 and the QC scan call at source line 509 verified **byte-for-byte**
against the source text and executed verbatim). All mutants are in-memory
copies (window copies for the executor-lineage decoder, full-EXE copies for
the QC-lineage decoder); the physical EXE was never modified and was
re-hashed unchanged after all work (`E7785430E81DFFE648CE8F5312414B17`
`BC9FCE61389689A22F753765D5280F31`, 8015872 B, before AND after).

Per-duty PASS records with MEASURED_QUANTITY / INDEPENDENT_SOURCE_OF_TRUTH /
WHY_NON_CIRCULAR / FAILURE_CASE_DETECTED are in `QC_RESULTS.json`
(`pass_records_methodology`).

## 2. Per-duty results

### DUTY A — historical PRE false PASS reproduced by the QC (own runs)

QC's own AST-extracted historical decoders, own mutants, own verbatim-scan
executions:

| Case | Implementation | Measured | QC reproduced |
|---|---|---|---|
| CH mutant 88 DD | historical executor | dst `ch`, src `bl`, **writes ["ebp"]**, reads ["ebx"] (BL parent — low-alias coincidence), verbatim ECX scan **[] (FALSE EMPTY)** | YES |
| CH mutant 88 DD | historical QC | dst `ch`, src `bl`, **writes ["ebp"]**, **reads []** (source parent missing), verbatim QC scan **[] (FALSE EMPTY)** | YES |
| clean | both | 64 insns, end exact 0x0085B290, `D9 E8` `fld1` @0x0085B24D, scans [] (TRUE no-clobber) | YES |
| CL mutant 88 D9 | both | writes ["ecx"] (low-alias coincidence), scans DETECTED @0x0085B24D | YES |
| length preservation | all six | 64 insns each, end exact 0x0085B290 | YES |

Historical 8x8 census (64 cases x 2 decoders, QC's own enumeration):
executor writes-parent correct 32/64 (dest 0-3 only), reads-parent correct
32/64, both correct exactly 16/64; QC writes-parent correct 32/64, register-
form source parent recorded 0/64 (missing in all 64).

**Executor's `00_PRE/PRE_COUNTEREXAMPLES.json` compared field-by-field against
these own measurements: ALL 6 cases match (writes/reads/dst/src/scan/decode),
and all census aggregates + all 64 per-row historical decode records match.**
PRE_EXECUTOR_FALSE_PASS_REPRODUCED_BY_QC = YES;
PRE_QC_FALSE_PASS_REPRODUCED_BY_QC = YES.

### DUTY B — corrected clean PASS through the QC's own decoder

Physical window: 64 instructions, 224 bytes, end exact 0x0085B290;
mutation site `D9 E8` `fld1`; ECX scan [] (no false positive); QC
provenance gate PASS; CORE_VALUE_SOURCE = [arg1+8]. **PASS.**

### DUTY C — corrected CH (88 DD) detection + provenance gate FAIL

QC's own decoder: dst `ch`, writes {ecx}, reads {ebx} (BL parent recorded —
the historical QC's missing-reads facet fixed), dst bits [8,16), width 8,
partial_gpr_write=True, length 2. ECX scan **DETECTED @0x0085B24D**. QC gate
**FAIL with failure_reasons exactly ["ECX_REACHING_DEF_BROKEN"]** — every
other check measured true on the mutant (pin 0x0085B1DA, pin 0x0085B24B, call
pin + rel32 recompute to 0x00746560, accessor bytes 8D 41 08 C3, pin
0x0085B27F, pin 0x0085B281, EDI reaching definition intact). The CH mutant
reached the SAME QC provenance predicate used for the clean analysis (no
hard-coded mutant assertion); the failure is causally the broken ECX
reaching definition alone. **PASS.**

### DUTY D — corrected CL (88 D9) detection + provenance gate FAIL

Same through the QC's decoder: dst `cl`, writes {ecx}, bits [0,8), scan
DETECTED @0x0085B24D, gate FAIL via ECX_REACHING_DEF_BROKEN alone. **PASS.**

### DUTY E — the complete 64-case 8x8 matrix through the QC's own decoder

All eight destinations x all eight sources (AH/CH/DH/BH on both sides), 64
distinct 2-byte cases (`88 C0|src<<3|dst`), each verified against the QC's
own explicit reference table on: exact destination/source operand, parent,
writes-set == {parent}, reads-set == {source parent}, width 8, length 2,
bit ranges low [0,8) / high [8,16), partial-vs-full-32-bit distinction.
**64/64 PASS; destination coverage 8/8; source coverage 8/8.** With the
executor's 64/64 (verified present and consistent), the contract's
**128 decoder outcomes across the two implementations are COMPLETE: 128/128.**

### DUTY F — unrelated-parent negatives

The executor's four negatives re-run by the QC through its own decoder —
88 DF `mov bh,bl` -> EBX; 88 DC `mov ah,bl` -> EAX; 88 CE `mov dh,cl` -> EDX
(reads {ecx} — a byte READ never triggers the WRITER-based scan); 88 FF
`mov bh,bh` -> EBX — plus the QC's own additional negatives: 88 D4
`mov ah,dl` -> EAX and 88 FB `mov bl,bh` -> EBX (not EDI/ECX/ESP/EBP/ESI).
All six: correct parent, ECX scan [], gate PASS. **6/6 PASS.**

### DUTY G — historical scientific regression (own measurements)

- 23/23 byte pins within the approved windows match (incl. store
  `89 4E 44` @0x0085B281, boundary C3 + CC CC CC, entry, vtable stamps,
  zero-init triple, chain pins, copy48/copy4C byte-pinned ONLY — no
  analysis, per contract section 9).
- rel32 recomputations: call @0x0085B27A -> **0x00746560** and call
  @0x00528E8D -> **0x0085B1B0** (signed rel32 -1133855 / +3351326).
- Accessor 0x00746560 re-read: **8D 41 08 C3** (`lea eax,[ecx+8]; ret`).
- Own RTTI walks: vtable 0x00A91E4C -> COL 0x00AB33D0 (sig 0) -> TD
  0x00B7997C -> `.?AVMovableObject@@` (null-terminated); vtable 0x00A7DCB0
  -> COL 0x00AA17CC -> TD 0x00B79958 -> `.?AVClientMovableObject@@`.
- Clean decode through the QC's own decoder: 64 instructions, 224 bytes,
  end exact **0x0085B290**; committed-table anchor (va/len/bytes,
  lineage-independent) 64/64 MATCH.
- Field-level comparison vs the re-executed HISTORICAL QC decoder
  (facet-scoped, measured): va/length/bytes/text/writes/dst/src/width/
  mnemonic equal on **ALL 64** rows; reads equal except **exactly the four
  memory-form `88 9E` instructions** @0x0085B25B/0x0085B261/0x0085B267/
  0x0085B26D (`mov [esi+0x9c..0x9f], bl`), where the corrected decoder gains
  exactly {ebx} (the BL source parent) and loses nothing — the CMO-C1
  facet-2 fix on real instructions, disclosed by the executor's
  ROOT_CAUSE.md section 5. Zero unexpected differences. (The executor's own
  C6 field-equality — corrected-executor vs historical-executor, same
  lineage — holds 64/64 on all fields including reads; the QC verified that
  lineage pair differently: the QC-lineage pair shows exactly these four
  documented facet-2 reads differences and nothing else.)
- Value-source chain (own decode + scans): arg1 = [esp+0x14] (4 pushes
  before 0x0085B1DA, entry [esp+4] + 0x10 — own push enumeration), EDI :=
  [esp+0x14] @0x0085B1DA, ECX := EDI @0x0085B24B, call 0x00746560 (accessor
  returns arg1+8), ECX := [eax] @0x0085B27F, store [esi+0x44] @0x0085B281;
  EDI-writer scan (0x0085B1DA,0x0085B24B] = [], ECX-writer scans
  (0x0085B24B,0x0085B27A) = [] and (0x0085B27F,0x0085B281) = [];
  ESI receiver: ESI := this @0x0085B1B7, base vtable stamp @0x0085B1C1,
  ESI-writer scan (0x0085B1B7,0x0085B281] = [], derived stamp after return
  @0x00528EA2, both RTTI identities.
- **CORE_RECEIVER_VALUE_CHAIN = PRESERVED_CONFIRMED_STATIC_CONDITIONAL**
  (QC's own independent measurement; no promotion beyond the original
  static scope).

### DUTY H — executor claims verification

- PRE_SHA256_INDEX.csv: **8/8 rows match the physical files** (QC's own
  re-hash); POST_SHA256_INDEX.csv: **11/11 rows match**.
- All four mandatory source inputs + contextual inputs (FINAL_REPORT,
  CLAIM_MATRIX, MANIFEST, J3 SUPERSESSION, AUDIT_ENTRYPOINT) identity-
  verified by the QC's own hashes; `git diff HEAD` over the source package
  EMPTY — **SOURCE_PACKAGE_UNCHANGED confirmed**.
- POST semantic comparison against the QC's own re-runs: C1/C2/C3/C5 site
  values (writes/reads/bits/scan) all MATCH; C2/C3 gate decomposition
  matches exactly (FAIL via ECX_REACHING_DEF_BROKEN alone); C4 64/64;
  C6 all sub-claims match (pins/rel32/RTTI/decode/chain); AUX-1
  UNSUPPORTED_FAIL_CLOSED (DecodeError) confirmed; exe_identity_post
  unchanged; residue 0.
- **Three disclosed process repairs adjudicated by the QC:**
  1. **C5.4 test-data repair (0xF7 -> 0xFF)**: CONFIRMED HONEST — the QC's
     own independent decoder agrees 88 F7 is `mov bh, dh` (writes ebx /
     reads edx) and 88 FF is `mov bh, bh` (writes ebx / reads ebx); the
     corrected decoder catching the wrong TEST DATA demonstrates the alias
     fix; only test data changed, no decoder or measured value.
  2. **PRE regeneration (per-case records + file-offset formula fix)**:
     CONFIRMED HONEST — the QC re-measured all six PRE cases independently
     (duty A): every decode/scan value matches the executor's PRE records
     field-by-field; the present PRE_COUNTEREXAMPLES.json contains the
     per-case records, and the QC's own offset computation confirms the
     corrected consistency formula (committed W1 raw_offset 4567464 + 165
     = 4567629, consistent).
  3. **CONTROL_MATRIX.csv expected-column repair**: CONFIRMED HONEST —
     present CSV rows carry the correct expected parents; measured values
     match the QC's own re-runs; presentation-only.
- No measured value was silently altered anywhere (SHA indexes + POST
  records re-verified by the QC's own re-hash/re-run).

### DUTY I — AUX unsupported-opcode fail-closed (QC's own decoder)

In-memory mutant `0F B0` @0x0085B24D through the QC's decoder:
**UNSUPPORTED_FAIL_CLOSED** (controlled `QcDecodeError: unsupported opcode
0x0f @0x85b24d`) — never a silent acceptance. PASS.

### DUTY J — documentary supersession / standing scan

All package files present at scan time scanned (16: 13 executor-phase files
+ the QC's 2 tooling files; QC_RESULTS.json written after the scan contains
only carried-verbatim statuses; QC_REPORT.md — this file — carries the same
verbatim statuses). **Forbidden active standing: 0 hits.** Unmarked
mentions of the historical transform-relation standing (the
`... = CONFIRMED_STATIC` form — the SUPERSEDED historical J3 status):
**0** — the single occurrence in SUPERSESSION_AND_STANDING.md line 95 is
explicitly supersession-marked ("remains SUPERSEDED"). The five J3
statuses are carried
**verbatim** in SUPERSESSION_AND_STANDING.md (equals form, 5/5 found) and in
REGRESSION_RESULTS.json (JSON `j3_statuses_carried_verbatim` fields,
semantically verified 5/5):

```
PHYSICAL_TRANSFORM_MEASUREMENTS = PRESERVED
NEW_TRANSFORM_TRACE =
  MEASURED_INCIDENTAL_OUTSIDE_PERMITTED_PROMOTION
SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN =
  NOT_QUALIFIED_BY_ORIGINAL_SCOPE

ORIGINAL_J3_EDGE_BUDGET_COMPLIANCE = FAIL
WORLD_XYZ_RECOVERED = NO
```

No restoration anywhere in the package. Scanner-self exclusion: the scanner
file (03_SCRIPTS/qc_run_controls.py) is excluded from the forbidden-pattern
regex portion (its own regex definitions would be self-referential false
positives — the same self-exclusion the historical qc_remeasure.py applied
to its own qc_* scripts); the exclusion scope is recorded in QC_RESULTS.json.

## 3. Verdict

**QC_VERDICT = QC_PASS** — all 11 acceptance gates (contract section 11)
hold with this QC's own independent measurements:

| Gate | Result |
|---|---|
| 1 PRE false PASS reproduced in BOTH old decoders | TRUE |
| 2 CH -> ECX in BOTH new decoders (executor 64-case record + QC own decode) | TRUE |
| 3 actual clobber/provenance predicate reached (per-check decomposition) | TRUE |
| 4 clean retains no CH-related false positive | TRUE |
| 5 CL + complete alias matrix pass (128/128 outcomes total) | TRUE |
| 6 unrelated-parent negatives pass (6/6 incl. 2 QC-own) | TRUE |
| 7 original client bytes + chain unchanged (EXE rehash; PRESERVED chain) | TRUE |
| 8 no new science interpretation | TRUE |
| 9 QC independently reproduces the decisive failure case | TRUE |
| 10 documentation does not overclaim | TRUE |
| 11 manifest/indexes/historical immutability pass | TRUE |

This QC verdict is INTERNAL QC, not MASTER_ACCEPTED and not milestone
closure. CORRECTION_VERDICT / persistence / publication remain PE-MASTER's
phase per the delegation.

## 4. Repair rounds (own tooling; full disclosure)

`QC_REPAIR_ROUNDS_MAX = 1` per the QC dispatch. During the initial bring-up
of the QC runner, **five distinct own-tooling fix steps** were needed, ALL
disclosed in `QC_RESULTS.json` (`repair_rounds_log`, with failed intermediate
states preserved): (1) a mistyped constant name (NameError on the first
run); (2) the duty-G field-equality premise was wrong for the QC lineage
(the historical QC decoder never recorded the register byte-source parent in
reads — CMO-C1 facet 2 — so reads equality on ALL 64 rows was an impossible
premise; re-scoped per facet with exactly the four documented exceptions);
(3) the duty-J token scan flagged its own regex definitions (self-reference;
scanner-self exclusion applied per the historical qc_remeasure.py
precedent); (4) the duty-J record was computed but not persisted into the
results dict (one missing assignment — regenerated); (5) a duty-J
equals-form-regex boolean was misleading for the colon-form JSON in
REGRESSION_RESULTS.json (replaced by the authoritative semantic field
check). **No executor artifact, no measured value and no expectation of the
run under audit was touched by any fix.** Whether these five steps count as
one bring-up session or as five repair rounds against the MAX=1 budget is
DISCLOSED for PE-MASTER's adjudication; this QC does not hide it. No tooling
edit touched any measurement logic; the runner is deterministic over
identical inputs.

## 5. Coverage and NOT_CHECKED

FULL_READ_LOG (read to EOF in this QC): the contract (529 lines);
corrected_executor_decoder.py (488); run_pre_counterexamples.py (785);
run_alias_controls.py (1113); qc_remeasure.py (715, source);
repin_write_provenance.py (729, source); ROOT_CAUSE.md; PREREGISTRATION.md;
INPUT_IDENTITIES.md; SUPERSESSION_AND_STANDING.md; CONTROL_MATRIX.csv;
REGRESSION_RESULTS.json; PRE_SHA256_INDEX.csv; POST_SHA256_INDEX.csv;
QC_RESULTS.json (QC-generated, parsed in full); PRE_COUNTEREXAMPLES.json and
POST_COUNTEREXAMPLES.json (parsed programmatically; every load-bearing
record extracted and compared; not every nested JSON row printed in this
report — the machine record in QC_RESULTS.json carries the per-row data).

NOT_CHECKED / out of scope (by contract, not by omission):
- the source package's 01_RAW evidence files, token_gates.py internals, the
  J3 package contents, the PLUS4/FD packages, AUDIT_ENTRYPOINT.md content
  beyond identity — outside this correction's audit target (contextual
  identities verified by hash);
- exclusion-census pins outside the approved windows — NOT re-read (scope);
- sibling stores +0x48/+0x4C — byte-pinned only, no analysis (section 9);
- the upstream arg1 chain — not followed (section 9);
- GENERAL_X86_DECODER_CORRECTNESS / GENERAL_UNSUPPORTED_FORM_FAIL_CLOSED —
  NOT established by this correction (bounded window decoder; AUX-1
  demonstrates a controlled failure for one unsupported opcode only);
- the 8A (mov r8, r/m8) symmetric branch in the QC decoder is implemented
  but not exercised by any contract control (no such byte exists in the
  window); the 128-outcome matrix covers opcode 0x88 as contracted.
- Cosmetic note (no impact on any measurement): within QC_RESULTS.json the
  duty-B record names its scan field `ecx_scan_(...)` while duties C/D/F use
  `ecx_clobber_scan_(...)` for the same scan — a key-naming inconsistency in
  the QC's own evidence JSON, disclosed here.

## 6. Open findings

- **None material against the executor's correction.** All executor claims
  verified against the QC's own independent measurements; the three
  disclosed process repairs are honest; no measured value was silently
  altered; historical package, EXE and tracked tree unchanged.
- Process disclosure for PE-MASTER: the five own-tooling bring-up fix steps
  (section 4) versus `QC_REPAIR_ROUNDS_MAX = 1`.
- This QC adds no new P0/P1/P2. Unresolved project-level ceilings remain as
  carried verbatim: FIELD_SEMANTICS = UNVERIFIED; WORLD_INSTANCE_IDENTITY =
  NOT_ESTABLISHED; HISTORICAL_PLACEMENT = NOT_ESTABLISHED;
  WORLD_XYZ_RECOVERED = NO; DOC-1/DOC-2 remain documented P3 backlog.

**WORKS != UNDERSTOOD. STOP BEFORE SCOPE EXCEED.**
