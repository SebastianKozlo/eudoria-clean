# GOVERNANCE_DECISION — PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006

RUN_ID = PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006
RUN_CLASS = BOUNDED_STATIC_RE
RUN_TYPE = MODEL_RESOURCE_TO_EXACT_SCENEFEEDER_NINODE_JOIN
REPOSITORY = D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean
REMOTE = SebastianKozlo/eudoria-clean
BRANCH = master
BASE_SHA = 24f45e0108b922c26ff584fee9ef7749de0390b6 (EXPECTED == LOCAL_HEAD == origin/master == actual remote, verified at preflight)
MODE = STATIC-ONLY (klient nigdy nie działa; no client launch, no runtime, no network)
EXECUTOR = pe-reconstruction (PE-MASTER direct dispatch, NO_NESTED_TASKS)

## 1. VERBATIM human instruction (the authorization source)

Source: direct human message in the OpenCode PE-MASTER session on 2026-10-06
(after publication of commit 24f45e0), dispatched to this executor as the run
authorization. Preserved verbatim below. This file was written to disk at the
system time recorded in section 3.

---BEGIN VERBATIM HUMAN INSTRUCTION---
Autoryzuję wykonanie jednego micro-runu opisanego w pliku:

C:\Users\User\Documents\ChatGPT\PE\PE_935_MODEL_CHILD_JOIN_PROMPT_REVIEW_20261006\OPENCODE_MODEL_CHILD_JOIN_REVIEWED.md


Uwzględnij jako wiążące ograniczenia wyboru anchorów:


C:\Users\User\Documents\ChatGPT\PE\PE_SCENEFEEDER_MODEL_JOIN_COMPARISON_RESEARCH_R2_20261006\HANDOFF_NOTES.md


Autoryzuję commit i push wyłącznie w granicach allowlisty kontraktu.


Zachowaj pytanie, limity i wymagania dowodowe kontraktu.
Nie uruchamiaj klienta ani dodatkowego eksperymentu.
Po końcowym QC i publikacji zwróć dokładny commit SHA,
wynik micro-runu oraz HARD STOP.
---END VERBATIM HUMAN INSTRUCTION---

## 2. Adjudication of this dispatch's phase boundary (executor-visible)

The contract (OPENCODE_MODEL_CHILD_JOIN_REVIEWED.md §7) orders:
SCIENCE -> FRESH INTERNAL QC -> FINAL REPORT/REVIEW/EVIDENCE_INDEX/HANDOFF ->
AUDIT_ENTRYPOINT newest-first -> FINAL MANIFEST LAST -> FULL BIJECTION ->
COMMIT -> PUSH -> VERIFY REMOTE -> HARD STOP.

The PE-MASTER dispatch message for THIS executor task explicitly states the
current phase assignment:

- "FAZA TEJ DISPATCHY = nauka + targeted QC + pakiet."
- "NIE edytuj AUDIT_ENTRYPOINT.md (proposed newest-first row w HANDOFF.md),
  NIE commituj, NIE pushuj (persistence = PE-MASTER po własnym audycie i
  fresh internal QC)."

Therefore this executor performs: SCIENCE + TARGETED (fresh-context internal)
QC + PACKAGE (including the final MANIFEST_SHA256.csv over the physical
package files, entrypoint row EXCLUDED — the entrypoint is not edited in this
phase), and STOPS. No stage, no commit, no push, no AUDIT_ENTRYPOINT.md edit
by this executor. Classification of this phase split (per the DPA3
methodology of the prior correction run): ORCHESTRATOR_PHASE_SPLIT — it is
recorded here from the dispatch text as received, not reconstructed from
auditor comments.

AUTHORIZATION_FOR_COMMIT_PUSH = GRANTED_IN_VERBATIM_INSTRUCTION (above) with
scope REPO_WRITE_ALLOWLIST = OUTPUT_ROOT/** + final persistence-only
AUDIT_ENTRYPOINT.md; execution of the commit/push belongs to the persistence
phase (PE-MASTER after its own audit and fresh internal QC).

## 3. Write time (system)

GOVERNANCE_DECISION_WRITE_TIME = 2026-10-06T22:54:27-07:00 (system time at the
moment this file was first written to disk, captured from the OS during the
run; local timezone offset as shown).

## 4. Contract identity

CONTRACT_PATH = C:\Users\User\Documents\ChatGPT\PE\PE_935_MODEL_CHILD_JOIN_PROMPT_REVIEW_20261006\OPENCODE_MODEL_CHILD_JOIN_REVIEWED.md
CONTRACT_SIZE_BYTES = 15348
CONTRACT_SHA256 = F929D2C03B1D078BD69BDD206B0CF51DE5F393A0CE6D39618ED87819D043F3C8

ANCHOR_CONSTRAINTS_PATH = C:\Users\User\Documents\ChatGPT\PE\PE_SCENEFEEDER_MODEL_JOIN_COMPARISON_RESEARCH_R2_20261006\HANDOFF_NOTES.md
ANCHOR_CONSTRAINTS_SIZE_BYTES = 1641
ANCHOR_CONSTRAINTS_SHA256 = D531B56AB0C1FD180A31DABC5DACAAE289372CA7B8FD8EC8BAAC565FAB0E4355

Both files were read in full by this executor from disk before any analysis;
their §0–§7 (contract) and all 10 constraint items (handoff notes) are applied
as written. The single science question of the run (contract §0):

"czy na jednej zbadanej ścieżce PCG 9.3.5 wynik o fizycznie ustanowionym
pochodzeniu model/resource zostaje związany jako visual child z dokładnie tym
samym NiNode pointerem, który pochodzi z badanego SceneFeeder+0x30?"

## 5. Hard governance statuses carried into this run (unchanged)

WORLD_XYZ_RECOVERED = NO
HISTORICAL_INSTANCE_DATA_RECOVERED = NO
STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED
CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO
RUNTIME_JOIN_OBSERVED = NO (always, in this static-only run)
No Q1/Gate-B/M1/M2 changes by this run. Publication of this package (by the
persistence phase) is not acceptance; negative results are publishable.
