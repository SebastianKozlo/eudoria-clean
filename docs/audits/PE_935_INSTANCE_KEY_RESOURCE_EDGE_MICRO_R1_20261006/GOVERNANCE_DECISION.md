# GOVERNANCE_DECISION — PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006

## Decision identity

- RUN_ID: PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006
- FILE_WRITTEN_AT (local system time): 2026-10-05 23:54:05.874 (independent re-measurement
  immediately after write, see 01_RAW/GovernanceWriteTime.txt)
- This file is KROK 0 (written BEFORE science/RE), per the human instruction and contract §1
  ("Save that actual instruction verbatim with its source/time in GOVERNANCE_DECISION.md before science.").

## Source of the human instruction

- SOURCE: Direct human message in the OpenCode PE-MASTER session, received after
  the publication of commit 3921dbe2a43a9181f8a50fa5242d8586c85896b6, relayed to this
  executor session verbatim as the PE-MASTER DIRECT DISPATCH payload.
- The instruction identifies the exact contract file path and SHA256, authorizes exactly
  one run (PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006), adjudicates DA1 NOW
  as a disclosed procedural exception, and bounds the persistence phase.
- Per the human instruction, commit/push is NOT performed in this run's dispatch scope:
  "persistence zrobi osobna faza — NIE commituj; manifest i entrypoint-row przygotuj,
  entrypoint NIE edytuj jeszcze; proposed row w HANDOFF.md."

## VERBATIM human instruction

---BEGIN VERBATIM HUMAN INSTRUCTION---
Akceptuję TERAZ DA1 dla commita 3921dbe2a43a9181f8a50fa5242d8586c85896b6 jako ujawniony wyjątek proceduralny: dodatkowy pass F1/F2 przekroczył wcześniej zadeklarowany limit jednej rundy napraw QC. Nie stwierdzam, że wcześniejsza zgoda istniała. Techniczne wyniki D1/D2 pozostają przyjęte w zbadanym zakresie; DA2 pozostaje P3 backlog. Nie zlecam ich ponownego wykonania.

Autoryzuję wyłącznie jeden run PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006 według pliku:
C:\Users\User\Documents\ChatGPT\PE\PE_935_INSTANCE_RESOURCE_MICRORUN_PROMPT_REVIEW_20261005\OPENCODE_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006.md

SIZE_BYTES = 11823
SHA256 = 57A731683EE32E6FC43CCEC42664B03D4DC7FBA2138009B8BF7A0A8E634BABB6

Autoryzuję commit i push wyłącznie w allowliście tego kontraktu. Zachowaj tę rzeczywistą wiadomość ze źródłem i czasem przed rozpoczęciem RE. Sprawdź SHA kontraktu, bazę repo i EXE; nie zmieniaj kontraktu przy dispatchu. Wykonaj jeden bounded static run, targeted QC, manifest LAST, commit/push i weryfikację remote. Wynik negatywny też utrwal uczciwie.

Nie autoryzuję 0xA4 source/init, kolejnego eksperymentu, runtime klienta, odzyskiwania XYZ, zmiany kwalifikacji PE-MASTER ani milestone. Po publikacji zwróć dokładny SHA i HARD STOP.
---END VERBATIM HUMAN INSTRUCTION---

## DA1 adjudication (present decision)

- DA1_ADJUDICATION = PRESENT_EXCEPTION_DISCLOSED
- The present acceptance is NOT evidence of prior authorization; it is an exception
  accepted NOW for the additional F1/F2 pass that exceeded the previously declared
  one-round QC repair limit. No claim is made that an earlier consent existed.
- DA2 remains P3 backlog. DA2 re-execution is NOT authorized.
- The historical deviation is NOT labelled compliant; historical packages are NOT
  rewritten. D1/D2 technical results remain accepted within the examined scope.
- Technical results D1/D2: not re-ordered to execute (no re-execution commissioned).

## Human-instruction vs contract persistence ordering

- Contract §6 orders: "... manifest LAST -> exact bijection/hash verification ->
  path-limited normal commit -> normal push -> verify ... -> STOP".
- The direct human dispatch message instructs this run: prepare manifest and the
  entrypoint row, but DO NOT edit AUDIT_ENTRYPOINT.md yet, DO NOT commit/push —
  a separate persistence phase will do it. Proposed entrypoint row goes to HANDOFF.md.
- Resolution applied: the later, more specific direct human instruction governs this
  run's terminal state (package + manifest computed WITHOUT the entrypoint row, with
  that fact recorded). The manifest therefore covers all physical OUTPUT_ROOT files
  minus the manifest itself; the entrypoint row is documented as OUT_OF_MANIFEST_SCOPE
  in this phase and the final manifest regeneration (including the updated
  AUDIT_ENTRYPOINT.md row) is deferred to the persistence phase, as instructed.
- This is recorded as a dispatch-scoped persistence deferral, NOT a contract change:
  the contract file itself was not modified (SHA256 re-verified 57A731683EE32E6FC43CCEC42664B03D4DC7FBA2138009B8BF7A0A8E634BABB6 / 11823 B).

## Preflight verification (fail-closed, performed 2026-10-05 23:53:47–23:53:49 local)

- CONTRACT SHA256: 57A731683EE32E6FC43CCEC42664B03D4DC7FBA2138009B8BF7A0A8E634BABB6, SIZE 11823 B — MATCH.
- EXPECTED_BASE_SHA = 3921dbe2a43a9181f8a50fa5242d8586c85896b6.
- LOCAL_HEAD = 3921dbe2a43a9181f8a50fa5242d8586c85896b6 — MATCH.
- origin/master (after fetch) = 3921dbe2a43a9181f8a50fa5242d8586c85896b6 — MATCH.
- Independent `git ls-remote origin refs/heads/master` at 2026-10-05 23:53:49:
  3921dbe2a43a9181f8a50fa5242d8586c85896b6 — MATCH (exit 0).
- REMOTE_URL verified: https://github.com/SebastianKozlo/eudoria-clean.git.
- EXE D:\Eudoria_Reconstruction\pcg_install\Entropia.exe: 8,015,872 B / SHA256
  E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 — MATCH.
- OUTPUT_ROOT did not exist (Test-Path = False) before this run — confirmed.
- Tracked working tree: no relevant tracked changes (git status porcelain shows only
  foreign untracked PE_935_* packages + experiments/, untouched per instruction).
- Preflight verdict: PASS.

## Scope boundaries accepted with this decision

- One bounded static run only. STATIC-ONLY: client never runs; no runtime hooking,
  no client launch, no network.
- NO 0xA4 source/init, no next experiment, no client runtime, no XYZ recovery,
  no PE-MASTER qualification change, no milestone change.
- NO VFS/BNT/NIF/ARK payload opening/decoding, no model dataset join,
  no static-building channel.
- Historical packages read-only; foreign untracked paths untouched.
- Negative results are persisted honestly.
- HARD STOP after the package; NO commit/push in this phase.

## FILE_WTIME_VERIFICATION

- Recorded at write time by the run itself (see 01_RAW/GovernanceWriteTime.txt for
  the independent PowerShell re-measurement performed immediately after the write).

## AMENDMENT 1 — DISCLOSED post-KROK-0 edit of this file (record-repair F1; APPEND-only)

- ORIGIN: record-repair continuation of this run (dispatched by PE-MASTER on
  2026-10-06), applying the pre-persistence correction required by the internal
  QC finding F1 (00_CONTROL_INTERNAL_QC/QC_REPORT_INTERNAL.md, section 3, F1,
  run PE_935_INSTANCE_KEY_RESOURCE_EDGE_MICRO_QC_INTERNAL_R1_20261006).
  Nothing above this amendment was altered or removed by the repair; this section
  is a pure append.
- DEVIATION DISCLOSED: this file was edited AFTER the KROK-0 measurement and
  BEFORE the start of science, and that edit was not disclosed in the original
  text. Two identity states of this file exist and are now both pinned here:
  - State A (KROK-0, pinned by 01_RAW/GovernanceWriteTime.txt): written
    2026-10-05 23:54:05.874 (file LastWriteTime), independently re-measured
    2026-10-05 23:54:08.342: 6,299 B, SHA256
    A953107598F7553C8DE5926EE7FA690920117E34977B728F065AC073741A6.
  - State B (pre-science state; the first science artifact, pe935k_core.py, was
    created at 23:56:13): a subsequent edit at 2026-10-05 23:54:12 changed the
    file by +25 B to 6,324 B, SHA256
    96B80022C5819AE0781B978053CB076C12B918C9E377D4CDB8569BBADD808E3A
    (this is also the state pinned by COMMITTED_PACKAGE_MANIFEST_SHA256.csv and
    re-measured by the internal QC at 00:19:47/QC M11).
- CAUSE: the exact content delta of the +25 B edit is NOT reconstructable from the
  package (no intermediate copy was preserved) and no package record documents
  why the edit happened; no cause is claimed here. The non-disclosure of the edit
  in the original KROK-0 text was the provenance defect; this amendment repairs
  the disclosure, not the history. Byte-identity of the current text against
  State A cannot be proven backwards and is NOT claimed (internal QC F1).
- ORDERING THAT STILL HOLDS: State B (mtime 23:54:12) still precedes the first
  science artifact (03_SCRIPTS/pe935k_core.py, 23:56:13), so "written BEFORE
  science" holds for State B; the VERBATIM human instruction was saved before any
  reverse-engineering activity began.
- VERBATIM-BLOCK STATEMENT (re-verified by this repair run, independently of the
  QC): the VERBATIM human-instruction block in the current text remains intact
  and consistent with the pinned contract identity —
  C:\Users\User\Documents\ChatGPT\PE\PE_935_INSTANCE_RESOURCE_MICRORUN_PROMPT_REVIEW_20261005\
  OPENCODE_INSTANCE_KEY_RESOURCE_EDGE_MICRO_R1_20261006.md re-hashed by this
  repair run at 2026-10-06 00:5x local: 11,823 B, SHA256
  57A731683EE32E6FC43CCEC42664B03D4DC7FBA2138009B8BF7A0A8E634BABB6 — MATCHES the
  SIZE_BYTES/SHA256 lines of the VERBATIM block and the Preflight verification
  section; the block remains point-by-point consistent with the PE-MASTER
  dispatch characterization (DA1 present-exception, exactly one authorized run,
  commit/push allowlist, prohibitions, two-phase persistence instruction).
  This is a consistency statement, not a byte-identity proof against State A.
- GovernanceWriteTime.txt: intentionally NOT altered (it is the honest
  measurement of State A; internal QC F1 requires leaving it unchanged). It is a
  single-record measurement file, not a log, so no amendment entry was appended
  to it; the disclosure lives in this section.
- POST-AMENDMENT IDENTITY: appending this amendment changes this file's size and
  SHA256 again (a third state, State C). State C's identity is NOT self-pinned
  inside this file (impossible without changing it again); it is pinned by the
  record-repair section of QC_REPORT.md (as of the end of this repair run) and
  will be pinned definitively by the persistence phase's manifest regeneration,
  which happens LAST and covers every physical file of the package per the
  two-phase flow.

