# FINAL_REPORT — PE_935_INSTANCE_KEY_RESOURCE_EDGE_POST_AUDIT_CORRECTION_R1_20261006

RUN_CLASS: RECORDS_ONLY_POST_AUDIT_CORRECTION · Era: PCG 9.3.5 ·
RUN_TYPE: INSTANCE_KEY_RESOURCE_EDGE_RECORD_CORRECTION · Executor:
pe-reconstruction (PE-MASTER direct dispatch, NO_NESTED_TASKS).
BASE f129fd5aa8e30f0f19c8903fe0d97899b9fe6510 (== origin/master == actual
remote master, verified at preflight and unchanged at handoff).
NO_NEW_SCIENCE = YES. NO client runtime, NO network, NO payload opening, NO
EXE byte reads (records-only; EXE identity carried from the source package's
pinned records and the Desktop post-audit).

---

## 1. What this run is

A records-only correction of the published package
`docs/audits/PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006/`
(commit f129fd5...) per the independent Desktop post-audit
REQUIRE_CORRECTIONS verdict (REPORT 14,545 B /
664579B1F0762C9CE6266CDDF75EF9DEDA426E702800FAA0F837EC07EEB19572) and the
present human adjudication A (GOVERNANCE_DECISION.md). The source package is
READ-ONLY historical evidence and remains byte-identical (Q15 = ZERO diff).

## 2. Corrections applied (all measured; details in QC_REPORT.md)

### DPA1 — P2 — the two active ledgers rebuilt (schema PASS)

- `FUNCTION_LEDGER_CORRECTED.csv` — 10 exact columns (contract §6), 8 data
  rows, csv.DictWriter serialization, UTF-8 no BOM, LF. Source defect: 7/8
  data rows malformed (ORD 1: 13 cells from 3 unquoted embedded commas; ORD
  3–8: 9 cells, one field absent). Repair: joins per RECONSTRUCTION_MAP; the
  absent OBSERVED_OPERATION fields reconstructed from FINAL_REPORT §7 status
  algebra (ORD 8 from §6 + the probe windows).
- `EDGE_LEDGER_CORRECTED.csv` — 11 exact columns, 22 data rows. Source defect:
  5/22 rows malformed (E-C1-PUSH 12 cells; E-E1-CALL / E-GB1 / E-GB2 / E-XD 10
  cells). Repair: the E-C1-PUSH embedded-comma join; one reconstructed field
  each for the four 10-cell rows (RECONSTRUCTION_MAP; no silent shifts).
- Fail-closed machine QC (03_SCRIPTS/ledger_schema_qc.py): both tables PASS
  (Q4–Q7); mandatory causal mutations MUT-A/B (per table) and MUT-C (EDGE
  swap) all CAUSAL_FAIL on temp copies with exact failed predicates (Q8–Q10).

### DPA2 — P2 — historical budget breach fixed as record

Historical truth (preserved, not rewritten):
TOTAL_DETAILED_FUNCTIONS_MAX = 6; FUN_0064B1E0 = FUNCTION #7 FULL 27-B BODY
OBSERVED; ORIGINAL_PROCESS_BUDGET_COMPLIANCE = FAIL. The historical labels
DISCLOSED_OVER_BUDGET_PROBE / NON_LOAD_BEARING do not make the original run
compliant. TECHNICAL_QC (byte-level PASS results) is recorded separately from
PROCESS_COMPLIANCE = FAIL (historical). Present decision:
PROCESS_EXCEPTION_AUTHORIZATION = HUMAN_ADJUDICATED_NOW;
RETROACTIVE_PRIOR_AUTHORIZATION = NO; HISTORICAL_BREACH_PRESERVED = YES;
SCIENTIFIC_CORE_EFFECT = NONE. "BUDGET RESPECTED" is never written for the
original run.

### DPA3 — P2 — human-instruction provenance corrected

The historical GOVERNANCE_DECISION.md attributed a persistence-deferral
instruction ("persistence zrobi osobna faza — NIE commituj...") to a direct
human message; the preserved VERBATIM block authorizes manifest LAST ->
commit/push -> remote verification and contains no deferral. Corrected:
PERSISTENCE_PHASE_SPLIT_SOURCE = NOT_ESTABLISHED_IN_RECORDED_HUMAN_SOURCE;
PHASE_SPLIT_BEHAVIOR_CLASSIFICATION = ORCHESTRATOR_PHASE_SPLIT (not
DIRECT_HUMAN_INSTRUCTION); no message fabricated, no chronology back-filled;
FINAL_PUBLICATION_AUTHORIZATION = PRESENT (commit f129fd5... remains
authorized). Historical files not modified.

### P3 precision corrections (records only)

- P3-1 State A SHA display corrected (61 -> the preserved 64-char value from
  01_RAW/GovernanceWriteTime.txt; NO byte-recovery claim).
- P3-2 vtable store VA corrected to 0x00528EA2 (0x00528EA8 = a different
  store, 89 9E A4 00 00 00).
- P3-3 FUN_00856190 extent corrected to the inclusive 0x00856190..0x00856210
  = 129 B (RET 4 = C2 04 00 @0x0085620E..0x00856210); the persisted window's
  0x0085620F end (omitting the final RET byte) disclosed as a limitation.
- P3-4 receiver wording corrected: ClientMovableObject CONFIRMED /
  GameClient CONFIRMED / additional [EBX] receiver form UNRESOLVED; allowed
  conclusion: FUN_00414130 = SHARED +0x74 OFFSET READER — STRONGLY_SUPPORTED
  in examined census scope.
- P3-5 resource-edge wording scoped: "No resource/template/model consumer was
  established in the examined bounded path."; the direct E8 negative strictly
  scoped to the measured five-address direct-E8 predicate
  {FUN_0072F580, FUN_006C9700, FUN_006CB6F0, FUN_006CB020, FUN_0043A550} in
  the decoded insert body.
- P3-6 historical QC_GATES.csv G2 width limitation recorded (8 naive cells vs
  6 declared columns; previous QC did NOT establish generic CSV schema
  validity); artifact not rewritten; its valid physical-byte results remain
  valid within their actual tested scope.

## 3. Preserved science (NO_UNINTENDED_SCIENCE_DIFF = PASS; QC_REPORT Q14)

All ten required-unchanged conclusions are preserved verbatim in the corrected
ledgers and this package: getter bytes; six direct E8 census in stated scope;
selected ClientMovableObject receiver; GameClient different-object result;
map-identity role in examined path; SceneFeeder key pass-through evidence;
resource/model edge NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO;
STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED; HISTORICAL_INSTANCE_DATA_RECOVERED
= NO. Allowed changes only (schema repair, metadata/provenance/address/size/
wording corrections, budget adjudication, supersession routing).

## 4. Status block (authoritative; see SUPERSESSION.md)

SCIENTIFIC_CORE = PRESERVED_IN_AUDITED_STATIC_SCOPE
LEDGER_SCHEMA_ORIGINAL = FAIL (7/8 FUNCTION rows + 5/22 EDGE rows malformed)
LEDGER_SCHEMA_CORRECTED = PASS (measured, fail-closed QC + causal mutations)
ORIGINAL_PROCESS_BUDGET_COMPLIANCE = FAIL (historical, unchanged)
PROCESS_EXCEPTION_AUTHORIZATION = HUMAN_ADJUDICATED_NOW
RETROACTIVE_PRIOR_AUTHORIZATION = NO
GOVERNANCE_PROVENANCE = CORRECTED (DPA3 validation PASS)
RESOURCE_EDGE_STATUS = NOT_ESTABLISHED_IN_EXAMINED_PATH
WORLD_XYZ_RECOVERED = NO
STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED
HISTORICAL_INSTANCE_DATA_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO

The resource result is NOT converted to RESOURCE_EDGE_CONFIRMED nor to
RESOURCE_EDGE_REJECTED_GLOBAL: the bounded conclusion stays
NOT_ESTABLISHED_IN_EXAMINED_PATH.

## 5. Honest unresolved findings (persisted, not hidden)

1. The READ-ONLY source package still contains its historical defects (the
   malformed ledgers, the AMENDMENT 1 SHA display, the 0x00528EA8 VA, the
   0x0085620F extent end, the broad §1.3 wording, the QC_GATES G2 width):
   corrected ONLY in this package's records (the source stays byte-identical
   as historical evidence by design).
2. The 9-cell FUNCTION rows and 10-cell EDGE rows did not persist distinct
   values for their missing fields; the corrected ledgers reconstruct them
   from existing persisted evidence (FINAL_REPORT §7/§6, BYTE_WINDOWS,
   sibling rows) — the mapping is disclosed in QC_REPORT RECONSTRUCTION_MAP,
   and four EDGE cells + six OBSERVED_OPERATION values carry this
   reconstruction provenance rather than a source-row cell.
3. The E-C1-PUSH embedded-comma join position was determined by structural
   analogy with the well-formed sibling rows; all its raw cell texts are
   preserved verbatim inside the corrected row (no text invented).
4. The BYTE_WINDOWS F00856190_mapinsert_full window ends at 0x0085620F and
   omits the final RET byte (disclosed limitation; does not falsify the
   established identity-map operation or the six body E8s).
5. The historical internal-QC materials (00_CONTROL_INTERNAL_QC, read-only)
   retain their as-measured citations (e.g. the pre-round-2 "26 B"/"0x004157B7"
   figures superseded by the source run's own round-2 repair).
6. RESOURCE_EDGE_STATUS remains NOT_ESTABLISHED_IN_EXAMINED_PATH: this
   records-only run did not and could not resolve it; the candidate science
   question (a model/resource-derived child reaching the same
   SceneFeeder+0x30 NiNode) remains DESIGNED_NOT_EXECUTED and is NOT
   authorized by this run.
7. HANDOFF.md of the source run retains the frozen pre-round-2 "26-B body"
   figures (a disclosed frozen historical record, not repaired there).

## 6. Phase and persistence

This phase = correction + targeted QC + package (GOVERNANCE_DECISION,
INPUT_IDENTITIES, the two corrected ledgers, the fail-closed checker + its two
JSON results, QC_REPORT, this FINAL_REPORT, SUPERSESSION, EVIDENCE_INDEX,
HANDOFF with the proposed AUDIT_ENTRYPOINT row, and the manifest generated
LAST covering every physical package file except itself — WITHOUT the
entrypoint row, which is explicitly out of this phase's manifest scope and
will be regenerated by the persistence phase together with the entrypoint
row). NO commit/push and NO AUDIT_ENTRYPOINT.md edit in this phase
(PERSISTENCE_STATUS = PREPARED_NOT_PERSISTED); persistence belongs to
PE-MASTER after its own audit. RESULTING_SHA = NONE in this phase.

## 7. HARD STOP

After the package + manifest + bijection verification: HARD STOP. No
FUN_007B68B0 / FUN_007B6A80 inspection, no AttachChild search, no model
resource tracing, no SceneFeeder consumer inspection, no model->SceneFeeder
join, no XYZ/static-building work, no 0xA4 work, no client launch. The later
candidate science question is DESIGNED_NOT_EXECUTED and
NOT_AUTHORIZED_BY_THIS_RUN.
