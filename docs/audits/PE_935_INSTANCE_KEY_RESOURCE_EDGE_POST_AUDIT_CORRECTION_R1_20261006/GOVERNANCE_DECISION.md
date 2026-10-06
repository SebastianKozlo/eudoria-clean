# GOVERNANCE_DECISION — PE_935_INSTANCE_KEY_RESOURCE_EDGE_POST_AUDIT_CORRECTION_R1_20261006

RECORDS-ONLY POST-AUDIT CORRECTION. NO NEW SCIENCE / NO NEW RE.
This file is written BEFORE any correction work, per the dispatch requirement
("zapisz ją z opisem źródła i czasem zapisu przed jakąkolwiek pracą").

## Decision identity

- RUN_ID: PE_935_INSTANCE_KEY_RESOURCE_EDGE_POST_AUDIT_CORRECTION_R1_20261006
- RUN_CLASS: RECORDS_ONLY_POST_AUDIT_CORRECTION
- RUN_TYPE: INSTANCE_KEY_RESOURCE_EDGE_RECORD_CORRECTION
- REPOSITORY: D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean
- REMOTE: SebastianKozlo/eudoria-clean, branch master
- EXPECTED_BASE_SHA: f129fd5aa8e30f0f19c8903fe0d97899b9fe6510
  (verified this run: LOCAL_HEAD == origin/master == actual remote master ==
  EXPECTED_BASE_SHA; fetch exit 0; no tracked changes; 6 foreign untracked
  paths inventoried and preserved untouched)
- CONTRACT (dispatch prompt file):
  C:\Users\User\Documents\ChatGPT\PE\PE_INSTANCE_RECORDS_CORRECTION_PROMPT_REVIEW_20261006\OPENCODE_RECORDS_ONLY_CORRECTION_REVIEWED.md
  — SIZE 24,218 B; SHA256
  EA86AA0897695C100D89BD68438318F6DDC9BD50DE28C7A6EDCC59ACF4ED61ED —
  verified MATCH before any work; contract NOT modified at dispatch.
- SOURCE_PACKAGE_READ_ONLY (historical evidence, MUST remain byte-identical):
  docs/audits/PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006/
- OUTPUT_ROOT: docs/audits/PE_935_INSTANCE_KEY_RESOURCE_EDGE_POST_AUDIT_CORRECTION_R1_20261006/
  (did not exist before this run — Test-Path = False at preflight)
- ALLOWED_WRITE_PATHS (this phase): OUTPUT_ROOT/** only. AUDIT_ENTRYPOINT.md
  is contract-authorized but NOT edited in this phase (dispatch phase order);
  the proposed newest-first row is supplied in HANDOFF.md.
- AUTHORITATIVE EXTERNAL INPUT (Desktop post-audit):
  C:\Users\User\Documents\ChatGPT\PE\PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_DESKTOP_POST_AUDIT_20261006\REPORT.md
  — SIZE 14,545 B; SHA256
  664579B1F0762C9CE6266CDDF75EF9DEDA426E702800FAA0F837EC07EEB19572 —
  verified MATCH before any work. DESKTOP_POST_AUDIT = REQUIRE_CORRECTIONS.
  Audited target commit: f129fd5aa8e30f0f19c8903fe0d97899b9fe6510.

## Source of the human instruction

- SOURCE: direct human message to the PE-MASTER session on 2026-10-06,
  adjudicating the Desktop post-audit REQUIRE_CORRECTIONS outcome of commit
  f129fd5aa8e30f0f19c8903fe0d97899b9fe6510, relayed to this executor session
  verbatim inside the PE-MASTER DIRECT DISPATCH payload (adjudication context
  section, marked ---BEGIN/END VERBATIM HUMAN INSTRUCTION---).
- The instruction identifies the exact contract file path, accepts the
  disclosed historical budget overrun NOW (adjudication A, contract §0),
  authorizes EXACTLY the described records-only correction plus commit/push
  within the allowlist, requires truthful persistence of findings, forbids
  new RE / model join / placement / XYZ, and requires the exact commit SHA,
  remote SHA, QC results, unresolved findings, manifest and HARD STOP at the
  end.
- SAVED (this file written) at local time 2026-10-06 04:27 (before any
  correction work; the file is created as the first artifact of the package).

## VERBATIM human instruction

---BEGIN VERBATIM HUMAN INSTRUCTION---
Wykonaj zlecenie z pliku:

C:\Users\User\Documents\ChatGPT\PE\PE_INSTANCE_RECORDS_CORRECTION_PROMPT_REVIEW_20261006\OPENCODE_RECORDS_ONLY_CORRECTION_REVIEWED.md

Przyjmuję adjudication A z §0: akceptuję TERAZ ujawnione historyczne przekroczenie budżetu, bez retroaktywnej autoryzacji i bez zmiany historycznego FAIL.

Autoryzuję wyłącznie opisany records-only correction oraz commit/push w granicach allowlisty. Utrwal rzeczywisty wynik również wtedy, gdy korekta pozostawi findings.

Nie rozpoczynaj nowego RE, model join, placement ani XYZ.

Na końcu zwróć dokładny commit SHA, remote SHA, wyniki QC, nierozwiązane findings, manifest i HARD STOP.
---END VERBATIM HUMAN INSTRUCTION---

## §0 adjudication A (present human decision — recorded per dispatch)

Akceptuję TERAZ przekroczenie limitu TOTAL_DETAILED_FUNCTIONS_MAX=6 w historycznym
runie PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006 jako ujawniony wyjątek
proceduralny.

Nie stwierdzam ani nie sugeruję, że wcześniejsza zgoda na przekroczenie budżetu
istniała.

Historyczna analiza FUN_0064B1E0 pozostaje DISCLOSED_OVER_BUDGET_PROBE i nie może
zostać przepisana jako zgodna z pierwotnym kontraktem.

Dopuszczam zachowanie jej fizycznych obserwacji jako istniejącego evidence.

Annotations (dispatch-required):
PROCESS_EXCEPTION_AUTHORIZATION = HUMAN_ADJUDICATED_NOW
RETROACTIVE_PRIOR_AUTHORIZATION = NO
ORIGINAL_PROCESS_BUDGET_COMPLIANCE = FAIL (historical, unchanged by this acceptance)
SCIENTIFIC_CORE_EFFECT = NONE

## DPA2 — historical budget breach (contract §9 — the historical truth, FIXED)

- TOTAL_DETAILED_FUNCTIONS_MAX = 6
- FUN_0064B1E0 = FUNCTION #7 FULL 27-BYTE BODY OBSERVED (the 0x30-B head probe
  intended as an identity probe covered the function's ENTIRE 27-byte body;
  0x0064B1E0..0x0064B1FA; disclosed in the source package).
- ORIGINAL_PROCESS_BUDGET_COMPLIANCE = FAIL.
- The historical labels DISCLOSED_OVER_BUDGET_PROBE and NON_LOAD_BEARING do NOT
  retroactively make the original run compliant.
- Historical QC labels ("PASS WITH ONE DISCLOSED DEVIATION" in the source
  QC_REPORT Q7; overall QC_PASS in Q9; internal QC G11; MASTER_ACCEPTED) mixed
  technical QC with process compliance; per DPA2 the two are SEPARATED:
  TECHNICAL_QC (byte-level PASS results) stays valid within its actual tested
  scope; PROCESS_COMPLIANCE = FAIL (historical).
- Present decision recorded separately:
  PROCESS_EXCEPTION_AUTHORIZATION = HUMAN_ADJUDICATED_NOW
  RETROACTIVE_PRIOR_AUTHORIZATION = NO
  HISTORICAL_BREACH_PRESERVED = YES
  SCIENTIFIC_CORE_EFFECT = NONE
- Never written for the original run: "BUDGET RESPECTED". The historical
  sequence is NOT rewritten as if authorization preceded the breach.
- The previous evidence stays preserved (source package READ-ONLY).

## DPA3 — human-instruction provenance correction (contract §10)

The historical GOVERNANCE_DECISION.md (source package, READ-ONLY) attributes an
additional instruction approximately equivalent to
"persistence zrobi osobna faza — NIE commituj..." to a direct human instruction.

The preserved VERBATIM HUMAN INSTRUCTION block (source package) instead
authorizes: manifest LAST -> commit/push -> remote verification.

Corrected provenance (this correction record):
PERSISTENCE_PHASE_SPLIT_SOURCE = NOT_ESTABLISHED_IN_RECORDED_HUMAN_SOURCE
(No exact, already-preserved source with time/identity for the additional
persistence-deferral instruction exists in the authorized evidence set: the
source package, the Desktop post-audit and this adjudication. The Desktop
post-audit verified the preserved verbatim block is consistent with the
prepared dispatch message and contains no deferral instruction, and explicitly
did not claim that an unpreserved message never existed. No such message is
fabricated here; the chronology is not back-filled.)

PHASE_SPLIT_BEHAVIOR_CLASSIFICATION = ORCHESTRATOR_PHASE_SPLIT
(The actually executed two-phase split is, on the recorded evidence, an
orchestration behavior — not a DIRECT_HUMAN_INSTRUCTION.)

FINAL_PUBLICATION_AUTHORIZATION = PRESENT
(The preserved verbatim human instruction DID authorize commit/push; therefore
commit f129fd5aa8e30f0f19c8903fe0d97899b9fe6510 remains authorized. DPA3 does
NOT render that commit unauthorized.)

Historical original files are NOT silently rewritten: the historical
GOVERNANCE_DECISION.md text is preserved unchanged in the read-only source
package; this record + SUPERSESSION.md supersede its persistence-provenance
attribution.

## Required P3 precision corrections (contract §11 — records only)

- P3-1 State A SHA display: the historical AMENDMENT 1 State-A SHA256 string is
  61 chars (`A953107598F7553C8DE5926EE7FA690920117E34977B728F065AC073741A6`,
  missing `239`); the original record 01_RAW/GovernanceWriteTime.txt holds the
  full 64-char SHA
  `A953107598F7553C8DE5926EE7FA690920117E34923977B728F065AC073741A6`
  (re-verified this run: 61 vs 64 chars, common prefix, both strings located).
  The transcription is corrected in THIS correction record. NO claim is made of
  recovery of the missing historical State-A bytes or the unknown +25 B delta.
- P3-2 ClientMovableObject vtable store VA: the authoritative instruction
  `C7 06 B0 DC A7 00` starts at 0x00528EA2, NOT 0x00528EA8 (0x00528EA8 is a
  different store, `89 9E A4 00 00 00`). Corrected in the NEW corrected ledger
  record (FUNCTION_LEDGER_CORRECTED.csv row 2) and this record.
- P3-3 FUN_00856190 extent: RET 4 occupies 0x0085620E..0x00856210; inclusive
  body = 0x00856190..0x00856210 = 129 B (not 128 B to 0x0085620F). Corrected in
  FUNCTION_LEDGER_CORRECTED.csv row 5. The persisted BYTE_WINDOWS window
  F00856190_mapinsert_full ends at 0x0085620F and omits the final RET byte 00 —
  a disclosed window limitation that does not falsify the established
  identity-map operation or the census of the six body E8s (existing evidence;
  no new RE).
- P3-4 shared getter receiver wording: ClientMovableObject — CONFIRMED;
  GameClient — CONFIRMED; additional [EBX] receiver form — UNRESOLVED. The
  claim ">=3 different receiver kinds proven" is corrected; the allowed
  conclusion is `FUN_00414130 = SHARED +0x74 OFFSET READER — STRONGLY_SUPPORTED
  in examined census scope`. Corrected in FUNCTION_LEDGER_CORRECTED.csv row 1.
- P3-5 resource-edge wording: statements equivalent to "No resource edge exists
  anywhere in the examined path" are superseded by "No resource/template/model
  consumer was established in the examined bounded path."; the direct E8
  negative is kept strictly scoped to the measured five-address direct-E8
  predicate ({FUN_0072F580, FUN_006C9700, FUN_006CB6F0, FUN_006CB020,
  FUN_0043A550}) in the decoded insert body. Corrected in the corrected ledger
  records and this correction's reports.
- P3-6 historical QC_GATES.csv limitation: the historical read-only
  00_CONTROL_INTERNAL_QC/QC_GATES.csv contains a malformed G2 row width
  (8 naive cells vs 6 declared columns, caused by unquoted commas inside
  "8,015,872 B"); therefore the previous QC did NOT establish generic CSV
  schema validity. The artifact is NOT rewritten; its valid physical-byte QC
  results (G1, G2 EXE-hash value, NC1-NC3, etc.) remain valid within their
  actual tested scope.

## Phase boundaries (this dispatch phase)

- THIS phase = correction + targeted QC + package. NO commit, NO push, NO
  AUDIT_ENTRYPOINT.md edit (proposed row in HANDOFF.md per contract §13).
  Persistence (entrypoint row + manifest regeneration including the entrypoint
  + path-limited commit/push + remote verification) is performed by PE-MASTER
  after its own audit of this package.
- ABSOLUTE SCOPE (contract §3): NO new PCG RE, no Ghidra/disassembly/xref/
  function-tracing/decoder work, no Gamebryo/OpenMW/NIF research, no oracle
  execution, no SceneFeeder research, no FUN_007B68B0/FUN_007B6A80 analysis,
  no ExtraData consumer research, no resource/model tracing, no AttachChild
  search, no 0xA4 work, no client runtime, no network, no VFS/BNT/NIF/ARK
  payload opening, no historical XYZ recovery, no static-building experiment,
  no PE-MASTER qualification, no milestone change. NO_NEW_SCIENCE = YES.
  No EXE byte reads are performed by this correction run (records-only; the
  EXE identity is carried from the source package and the Desktop post-audit).
- The later candidate science question (model/resource-derived child ->
  the same SceneFeeder+0x30 NiNode) remains DESIGNED_NOT_EXECUTED and
  NOT_AUTHORIZED_BY_THIS_RUN.

## Preflight verification (fail-closed, performed 2026-10-06 04:1x-04:27 local)

- CONTRACT: 24,218 B / SHA256 EA86AA0897695C100D89BD68438318F6DDC9BD50DE28C7A6EDCC59ACF4ED61ED — MATCH.
- DESKTOP REPORT: 14,545 B / SHA256 664579B1F0762C9CE6266CDDF75EF9DEDA426E702800FAA0F837EC07EEB19572 — MATCH.
- LOCAL_HEAD = f129fd5aa8e30f0f19c8903fe0d97899b9fe6510 — MATCH.
- origin/master = f129fd5aa8e30f0f19c8903fe0d97899b9fe6510 — MATCH (fetch exit 0).
- Actual remote master (git ls-remote) = f129fd5aa8e30f0f19c8903fe0d97899b9fe6510 — MATCH.
- SOURCE_PACKAGE exists at the exact expected path; full re-hash baseline census
  taken BEFORE any work (36 files; census persisted in INPUT_IDENTITIES.md).
- OUTPUT_ROOT did not exist (Test-Path = False) — no collision.
- Working tree: zero tracked changes; 6 foreign untracked paths inventoried and
  preserved untouched (see INPUT_IDENTITIES.md).
- Preflight verdict: PASS.
