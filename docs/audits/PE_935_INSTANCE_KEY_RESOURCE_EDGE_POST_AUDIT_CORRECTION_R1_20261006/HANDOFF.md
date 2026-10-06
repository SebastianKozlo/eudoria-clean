# HANDOFF — PE_935_INSTANCE_KEY_RESOURCE_EDGE_POST_AUDIT_CORRECTION_R1_20261006

## Run status (this phase = correction + targeted QC + package; PERSISTENCE BY PE-MASTER LATER)

- RUN_STATUS: COMPLETE (records-only correction package written; NO commit /
  NO push / NO AUDIT_ENTRYPOINT edit in this phase — per the dispatch phase
  order, persistence is performed by PE-MASTER after its own audit of this
  package)
- RUN_ID: PE_935_INSTANCE_KEY_RESOURCE_EDGE_POST_AUDIT_CORRECTION_R1_20261006
  · RUN_CLASS: RECORDS_ONLY_POST_AUDIT_CORRECTION · RUN_TYPE:
  INSTANCE_KEY_RESOURCE_EDGE_RECORD_CORRECTION
- BASE_SHA: f129fd5aa8e30f0f19c8903fe0d97899b9fe6510
  (== LOCAL_HEAD == origin/master == actual remote master, verified)
- RESULTING_SHA: NONE (no commit performed in this phase)
- REMOTE_SHA: f129fd5aa8e30f0f19c8903fe0d97899b9fe6510 (unchanged)
- DESKTOP_POST_AUDIT: REQUIRE_CORRECTIONS (REPORT 14,545 B /
  664579B1F0762C9CE6266CDDF75EF9DEDA426E702800FAA0F837EC07EEB19572; target f129fd5...)

## Correction outcome

- CORRECTION_VERDICT: CORRECTED_WITH_PRESERVED_FINDINGS (DPA1 ledgers rebuilt,
  schema PASS; DPA2 fixed as historical FAIL + present adjudication; DPA3
  provenance corrected; P3-1..P3-6 applied; science preserved — see
  FINAL_REPORT.md and the unresolved-findings list below)
- FUNCTION_LEDGER_ROWS: 8 (10 exact columns; schema QC PASS)
- EDGE_LEDGER_ROWS: 22 (11 exact columns; schema QC PASS)
- FUNCTION_LEDGER_SCHEMA_QC: PASS · EDGE_LEDGER_SCHEMA_QC: PASS
- MUT_A_RESULT: CAUSAL_FAIL · MUT_B_RESULT: CAUSAL_FAIL · MUT_C_RESULT: CAUSAL_FAIL
  (temp copies only; exact failed predicates in MUTATION_RESULTS.json)
- DPA1_DISPOSITION: CORRECTED (both ledgers rebuilt; schema PASS; mutations causal)
- DPA2_DISPOSITION: CORRECTED (historical FAIL preserved; HUMAN_ADJUDICATED_NOW
  recorded as present decision only; TECHNICAL_QC separated from
  PROCESS_COMPLIANCE)
- DPA3_DISPOSITION: CORRECTED (PERSISTENCE_PHASE_SPLIT_SOURCE =
  NOT_ESTABLISHED_IN_RECORDED_HUMAN_SOURCE; ORCHESTRATOR_PHASE_SPLIT;
  FINAL_PUBLICATION_AUTHORIZATION = PRESENT)
- P3_DISPOSITIONS: P3-1 CORRECTED (SHA display; no byte-recovery claim);
  P3-2 CORRECTED (store VA 0x00528EA2); P3-3 CORRECTED (129 B inclusive extent);
  P3-4 CORRECTED (CONFIRMED/CONFIRMED/UNRESOLVED wording); P3-5 CORRECTED
  (bounded resource-consumer wording + five-address direct-E8 scoping);
  P3-6 RECORDED (historical QC_GATES.csv G2 width limitation; artifact untouched)
- ORIGINAL_PROCESS_BUDGET_COMPLIANCE = FAIL (historical, unchanged)
- PROCESS_EXCEPTION_AUTHORIZATION = HUMAN_ADJUDICATED_NOW
- RETROACTIVE_PRIOR_AUTHORIZATION = NO
- SCIENTIFIC_CORE_STATUS = PRESERVED_IN_AUDITED_STATIC_SCOPE
- RESOURCE_EDGE_STATUS = NOT_ESTABLISHED_IN_EXAMINED_PATH
- SUPERSESSION_STATUS = ACTIVE (MASTER_ACCEPTED whole-package interpretation
  explicitly superseded by Desktop REQUIRE_CORRECTIONS + this correction;
  historical files not edited)
- WORLD_XYZ_RECOVERED = NO · STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED
  · HISTORICAL_INSTANCE_DATA_RECOVERED = NO · CANONICAL_GATE_EFFECT = NONE
  · NEXT_EXPERIMENT_AUTHORIZED = NO

## Unresolved findings left open (honest; persisted, not hidden)

1. The READ-ONLY source package retains its historical defects by design
   (malformed ledgers, AMENDMENT 1 SHA display, 0x00528EA8 VA, 0x0085620F
   extent, broad §1.3 wording, QC_GATES G2 width) — corrected only in THIS
   package's records.
2. Six OBSERVED_OPERATION values (FUNCTION rows 3–8) and four EDGE cells
   (E-E1-CALL PATH_CONDITIONS; E-GB1 FIELD_REGISTER_VALUE; E-GB2 RECEIVER_PROOF;
   E-XD RECEIVER_PROOF) are reconstructions from existing persisted evidence
   (QC_REPORT RECONSTRUCTION_MAP), not cells preserved by the source
   serialization.
3. RESOURCE_EDGE_STATUS remains NOT_ESTABLISHED_IN_EXAMINED_PATH — unresolved
   by design (records-only run; the candidate science question is
   DESIGNED_NOT_EXECUTED and NOT_AUTHORIZED_BY_THIS_RUN).
4. Historical internal-QC materials and the source HANDOFF retain frozen
   as-measured figures (disclosed limitations; read-only by contract).

## Package census (this phase)

- Changed paths (this run's writes): exactly the files under
  `docs/audits/PE_935_INSTANCE_KEY_RESOURCE_EDGE_POST_AUDIT_CORRECTION_R1_20261006/`.
  AUDIT_ENTRYPOINT.md NOT edited; foreign untracked paths untouched; no
  tracked file outside the package touched; source package byte-identical
  (Q15 = ZERO).
- MANIFEST_ROWS: 12 (CORRECTION_PACKAGE_MANIFEST_SHA256.csv generated LAST;
  scope = every physical file under OUTPUT_ROOT minus the manifest itself;
  in-process bijection re-hash verification: zero missing/extra/duplicate/
  size/SHA mismatches). **AUDIT_ENTRYPOINT.md is NOT in the manifest** (the
  entrypoint file was NOT edited in this phase; per the dispatch phase order
  the persistence phase adds the proposed row below, regenerates the manifest
  INCLUDING the entrypoint row, and repeats the bijection verification).
- PHYSICAL_CORRECTION_PACKAGE_FILE_COUNT: 13 (12 manifest rows + the manifest
  itself).

## p) Persistence instruction for the persistence phase (PE-MASTER)

1. Add the proposed AUDIT_ENTRYPOINT.md row below as the NEWEST-first row of
   the LATEST RUNS table (adapt the commit-discovery string to the actual
   commit; do not edit or delete the historical rows — including the source
   run's row, whose "budget 6 functions / 2 edges respected" cell is now
   superseded by DPA2 and must remain discoverable as history).
2. REGENERATE the manifest LAST with the full scope (every physical file under
   OUTPUT_ROOT minus the manifest + the updated AUDIT_ENTRYPOINT.md).
3. Path-limited commit of ONLY OUTPUT_ROOT/** + AUDIT_ENTRYPOINT.md; inspect
   the staged path census; no source-package file, no foreign untracked path
   staged; exactly one normal correction commit; normal push; verify
   LOCAL_HEAD == origin/master == actual remote master == RESULTING_SHA.
4. Report the exact commit SHA + remote SHA + this package's QC results +
   the unresolved findings above + the manifest census + HARD STOP.

## Proposed AUDIT_ENTRYPOINT.md row (NEW, newest-first; §13 of the contract)

```markdown
| (this commit; discover with `git log -1 -- docs/audits/PE_935_INSTANCE_KEY_RESOURCE_EDGE_POST_AUDIT_CORRECTION_R1_20261006`) | PE_935_INSTANCE_KEY_RESOURCE_EDGE_POST_AUDIT_CORRECTION_R1_20261006 (RUN_CLASS RECORDS_ONLY_POST_AUDIT_CORRECTION; RUN_TYPE INSTANCE_KEY_RESOURCE_EDGE_RECORD_CORRECTION; BASE f129fd5; executor pe-reconstruction, targeted SELF_CHECK QC QC_SCOPE=SELF_CHECK_LEDGER_SCHEMA_CORRECTION — no independent-QC claim in this phase; PE-MASTER direct dispatch, NO_NESTED_TASKS; phase 1 = correction + targeted QC + package (NO commit by the executor), phase 2 = PE-MASTER persistence after its own audit; NO_NEW_SCIENCE — no RE, no EXE reads, no runtime, no payload opening) | `PE_935_INSTANCE_KEY_RESOURCE_EDGE_POST_AUDIT_CORRECTION_R1_20261006/` | the records-only correction of the source run PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006 (commit f129fd5) per the independent Desktop post-audit REQUIRE_CORRECTIONS (REPORT 14,545 B / 664579B1..., audited target = f129fd5) and the 2026-10-06 human adjudication A — SUPERSEDES the source run's MASTER_ACCEPTED whole-package interpretation: (DPA1) both active ledgers REBUILT as FUNCTION_LEDGER_CORRECTED.csv (10 exact cols, 8 rows) + EDGE_LEDGER_CORRECTED.csv (11 exact cols, 22 rows) via csv.DictWriter from existing evidence only (source ledgers were malformed: 7/8 + 5/22 rows); fail-closed 03_SCRIPTS/ledger_schema_qc.py PASS on both (LEDGER_SCHEMA_ORIGINAL=FAIL -> LEDGER_SCHEMA_CORRECTED=PASS) with MUT-A/B/C all CAUSAL_FAIL on temp copies; (DPA2) ORIGINAL_PROCESS_BUDGET_COMPLIANCE = FAIL preserved as historical truth (FUN_0064B1E0 = function #7 full 27-B body observed; the original run's "budget respected"/QC_PASS process framing superseded) with PROCESS_EXCEPTION_AUTHORIZATION = HUMAN_ADJUDICATED_NOW as the PRESENT decision only and RETROACTIVE_PRIOR_AUTHORIZATION = NO; (DPA3) GOVERNANCE_PROVENANCE corrected: PERSISTENCE_PHASE_SPLIT_SOURCE = NOT_ESTABLISHED_IN_RECORDED_HUMAN_SOURCE / ORCHESTRATOR_PHASE_SPLIT (the historical direct-human attribution superseded; FINAL_PUBLICATION_AUTHORIZATION = PRESENT — commit f129fd5 remains authorized); P3-1..P3-6 corrected (State-A SHA display 61->64 chars from GovernanceWriteTime.txt, no byte-recovery claim; vtable store VA 0x00528EA8 -> 0x00528EA2; FUN_00856190 extent 0x00856190..0x00856210 = 129 B inclusive; receiver wording ClientMovableObject CONFIRMED / GameClient CONFIRMED / [EBX] UNRESOLVED; resource wording scoped to "no resource/template/model consumer established in the examined bounded path" + the five-address direct-E8 predicate; historical QC_GATES.csv G2 width limitation recorded); SCIENCE PRESERVED unchanged: SCIENTIFIC_CORE = PRESERVED_IN_AUDITED_STATIC_SCOPE, RESOURCE_EDGE_STATUS = NOT_ESTABLISHED_IN_EXAMINED_PATH, WORLD_XYZ_RECOVERED = NO, STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED, HISTORICAL_INSTANCE_DATA_RECOVERED = NO; no Q1/Gate-B/M1 change, CANONICAL_GATE_EFFECT = NONE, NEXT_EXPERIMENT_AUTHORIZED = NO (the model/resource-derived child -> SceneFeeder+0x30 NiNode question stays DESIGNED_NOT_EXECUTED); unresolved findings persisted honestly (4 reconstructed EDGE/FUNCTION fields carry reconstruction provenance; read-only source package retains its historical defects by design) |
```

(Note: the newest-first LATEST RUNS table of AUDIT_ENTRYPOINT.md has the
columns `| Commit | RUN_ID / ITER | Package path (docs/audits/) | One-line
purpose | PE-MASTER verdict |`. The row above provides the first four cells;
the persistence phase appends the PE-MASTER verdict cell with the actual
advisory verdict for this correction run. The row already contains the
required discovery hook: the previous MASTER_ACCEPTED whole-package
interpretation of the source run is superseded.)

## Honest NOT_CHECKED / UNKNOWN

- Independent internal QC / external Desktop re-audit of THIS correction
  package: NOT_PERFORMED in this phase (PE-MASTER audits before persistence).
- Resource kind/identity for the carried key: UNKNOWN (consumers unexamined).
- FUN_00853d00 / FUN_004A9850 / FUN_007C8780 / FUN_007B6A80 / ExtraData
  consumers semantics: NOT_CHECKED (unchanged from the source run).
- EXE re-verification: NOT_PERFORMED by this run (records-only; identity
  carried from the source package and the Desktop post-audit).
- Historical open P0s (Q1 qualification, canonical Gate-B re-attestation):
  UNCHANGED, not touched by this records-only run.

HARD_STOP = YES (after the package + manifest + bijection verification; no
further work authorized by this dispatch).
