# HANDOFF — PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009

The contract §15 terminal handoff fields, with ACTUAL measured values.
(Persistence-phase handoff; the terminal chat handoff to PE-MASTER restates the
SHA facts that cannot be embedded in this commit's own files.)

```text
RUN_ID
  = PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009
  (RUN_CLASS BOUNDED_STATIC_RE; RUN_TYPE CMO_SINGLE_WRITE_RECEIVER_AND_VALUE_SOURCE;
  the one-question bounded micro-run per the human-authorized frozen contract)

CONTRACT_SIZE_BYTES
  = 20158

CONTRACT_SHA256
  = C6599C0CCEB93DA5CD0E6B950DC3EF8AE6826FA962ABE99492F3931C7244CEB5
  (identity verified MATCH before any action)

EXPECTED_BASE_SHA
  = b2feef34122d2118da6ab38fc78f20f337315570

ACTUAL_BASE_SHA
  = b2feef34122d2118da6ab38fc78f20f337315570
  (measured at preflight: LOCAL_HEAD == origin/master == actual remote
  refs/heads/master, live ls-remote, no fuzzy comparison; re-verified
  immediately before commit per contract §14)

RESULTING_SHA / REMOTE_SHA
  = recorded at the terminal handoff per contract §14 — not embedded in this
  commit's files (a commit cannot contain its own SHA). The terminal handoff
  to PE-MASTER states both.

PERSISTENCE_STATUS
  = this handoff is written BEFORE the commit; the gates -> commit -> push
  sequence follows per contract §14. If any persistence gate fails or BASE
  drifts, the honest state would be BLOCKED_UNPUBLISHED per contract §14,
  HARD_STOP, no guard weakening. The recorded technical result (science A,
  QC_PASS, advisory MASTER_ACCEPTED, all persistence-safety gates PASS)
  means the expected terminal state is ONE ordinary commit + fast-forward
  push + actual-remote re-verification == RESULTING_SHA.

PREFLIGHT_STATUS
  = PASS (BASE triple equal live; tracked tree clean; OUTPUT_ROOT fresh;
  contract/EXE/source-pair identities MATCH; foreign untracked census recorded,
  untouched; PROJECT_STATE.json absent recorded N/A; J3 S-5 read before any
  source-A use)

SOURCE_J3_SUPERSESSION_IDENTITY
  = docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007/SUPERSESSION.md
  — 8339 B, SHA256 DD11137A0E79491511A7688B7C1DE9252DB7BA443FA31892C345CA76CE136845
  (+ CORRECTED_STATUS_ALGEBRA.md — 8987 B, SHA256
  00D09B0F72F1F6859C9DAF8A73C592659F251B596588DA304D9BC6912A40FA9F) — MATCH

ACTIVE_J3_TRANSFORM_STANDING = NOT_QUALIFIED_BY_ORIGINAL_SCOPE
  (carried verbatim with PHYSICAL_TRANSFORM_MEASUREMENTS = PRESERVED and
  NEW_TRANSFORM_TRACE = MEASURED_INCIDENTAL_OUTSIDE_PERMITTED_PROMOTION;
  SAME_INSTANCE_TRANSFORM_RELATION = CONFIRMED_STATIC remains superseded —
  no restoration)

ANCHOR_DISCOVERY
  = SUFFICIENT (committed-evidence-only census: 6 qualifying stores +
  10 genuine byte-verified exclusions incl. the FUN_00509510 rep-movsd ->
  SF+0x4C reclassification; pre-registered selection rule applied; the
  lowest-VA tie-break alternative fst @0x0085B1E4 disclosed and rejected
  with rationale)

SELECTED_WRITE_VA
  = 0x0085B281

WRITE_OPCODE_BYTES
  = 89 4E 44

WRITE_PHYSICAL_OFFSET
  = 4567681 (0x45B281)

WRITE_FUNCTION_START_VA
  = 0x0085B1B0 (FUN_0085B1B0; boundary C3 + 3x CC @0x0085B1AC-AF proven)

WRITE_DESTINATION_OPERAND
  = [esi+0x44]

RECEIVER_IDENTITY
  = the MovableObject-under-construction (the FUN_0085B1B0 ctor this; base
  vtable 0x00A91E4C = .?AVMovableObject@@ stamped @0x0085B1C1) which
  FUN_00528E50 stamps 0x00A7DCB0 = .?AVClientMovableObject@@ on the same
  memory after return (C7 06 B0 DC A7 00 @0x00528EA2); temporal nuance
  documented — NOT a finished CMO at store time

RECEIVER_IDENTITY_STATUS
  = CONFIRMED (scoped; temporal nuance QC-adjudicated SUPPORTED)

VALUE_SOURCE_CLASS
  = COPY_FROM_MEMORY

VALUE_PRODUCER_VA
  = 0x0085B27F (mov ecx,[eax] — 8B 08; *(arg1+8) via the pinned 4-byte
  accessor FUN_00746560: lea eax,[ecx+8]; ret — 8D 41 08 C3)

VALUE_PROVENANCE_STATUS
  = CONFIRMED

SCIENCE_OUTCOME
  = A — WRITE_AND_IMMEDIATE_SOURCE_ESTABLISHED

STOP_SCIENCE = YES

FUNCTION_BUDGET_USED
  = 1/1 body (a re-pin of previously fully-decoded committed evidence —
  T1_REGION raw + F0085B1B0.c + Ghidra H5; 0 new body semantics)

EDGE_BUDGET_USED
  = 0/0 (2 prior committed edges re-pinned; zero new)

store budget = 1/1 (sibling stores +0x48/@0x0085B287 and +0x4C/@0x0085B28D
byte-documented, NOT analyzed); callee bodies 0/0 (FUN_00746560 = prior
pin re-read, 4 B); xref expansion 0; semantic promotions 0

total EXE bytes read = 382
  (post-F-QC-1-errata; executor ledger declared 381 — see FINAL_REPORT §6
  errata: RTTI 0x00A7DCB0 chain = 4+20+26 = 50 B, not 49; non-material to
  any predicate or limit)

FALSIFIER_RESULTS
  = NOT_TRIGGERED (F1/F2 evaluated on UNMODIFIED original-client bytes;
  no contradiction found — correct per contract §9; synthetic-mutation
  rejections establish CONTROL_PASS only)

SYNTHETIC_MUTATION_CONTROLS
  = M1-M6 CONTROL_PASS (executor) + QC independent re-runs (M1/M2/M3/M5
  and the SF-conflation control with QC's own mutants — all rejection
  behavior reproduced)

QC_VERDICT
  = QC_PASS (fresh-context internal QC by pe-master-auditor, internal to
  PE-MASTER — NOT an independent Desktop post-audit; 9/9 duties, all
  load-bearing bytes re-measured from scratch: own PE parser, own decoder,
  own RTTI walk, own mutants; W1 232 B byte-identical)

PE_MASTER_ADVISORY_VERDICT
  = MASTER_ACCEPTED (advisory; ADVISORY_PRE_QUALIFICATION;
  CANONICAL_GATE_EFFECT = NONE; PE-MASTER independently re-measured ALL
  load-bearing bytes — ALL MATCH)

MANIFEST_ROWS
  = 20 (measured at generation: 19 package rows [every physical file under
  OUTPUT_ROOT except the manifest itself] + 1 AUDIT_ENTRYPOINT.md row)

MANIFEST_BIJECTION
  = PASS (physical enumeration vs manifest rows: missing = 0, extra = 0,
  duplicate = 0, size mismatch = 0, SHA mismatch = 0; measured by the
  generator at generation time and re-verified at the gates)

CHANGED_PATH_CENSUS
  = 21 (measured at commit: 20 package files incl. the manifest + the
  updated AUDIT_ENTRYPOINT.md; nothing else staged, modified or committed)

SOURCE_PACKAGE_UNCHANGED
  = YES (git diff b2feef34122d2118da6ab38fc78f20f337315570 -- <each source
  package incl. source A, J3, INSTANCE_KEY_RESOURCE_EDGE_MICRO, the PLUS4
  packages> — all empty at the gates)

NEW_FINDINGS
  = F-QC-1..F-QC-4 (all non-material; F-QC-1 = P2 required errata
  381->382 APPLIED in FINAL_REPORT §6 — the frozen executor ledger NOT
  edited in place; F-QC-2 = P2 optional 'fstp'->'fst' documented as an
  errata note; F-QC-3 = P3 optional census C-K source annotation
  documented as an errata note; F-QC-4 = P3 observation: executor token
  gate scanned 10/12 suffixes, QC 12/12 clean)

UNRESOLVED_FINDINGS
  = sibling stores unanalyzed; arg1 upstream UNKNOWN beyond the ctor
  argument; stored-dword representation f32-vs-u32 UNKNOWN; FIELD_SEMANTICS
  UNVERIFIED; world instance / historical placement NOT_ESTABLISHED

RETRACTIONS_SUPERSESSIONS
  = NONE new (J3 active standing carried; no restoration of
  SAME_INSTANCE_TRANSFORM_RELATION = CONFIRMED_STATIC; J3 historical
  ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL 22-vs-6 preserved WITHOUT
  transfer — this run used 0 edges)

GLOBAL_COORDINATE_FRAME = NOT_ESTABLISHED
HISTORICAL_PLACEMENT_RECORD = NOT_ESTABLISHED
INSTANCE_MODEL_JOIN = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
```

WORKS != UNDERSTOOD: one write plus synthetic tests proves nothing about
world XYZ, placement, the instance-model join or any semantic field role.
