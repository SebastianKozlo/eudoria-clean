# GOVERNANCE_DECISION — PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007

RUN_ID = PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007
RUN_CLASS = BOUNDED_STATIC_RE
RUN_TYPE = CAND4_CHILD_MODEL_ROOT_PROVENANCE
REPOSITORY = SebastianKozlo/eudoria-clean (D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean)
BRANCH = master
BASE_SHA = d65fa12e5bae4e9aab291c3cc7815b1822e41cff
MODE = STATIC-ONLY (the client is NEVER executed; no runtime, no network, no client
launch; byte-level analysis of the hash-pinned EXE only; no payload/VFS/BNT/NIF
opening — existing persisted metadata/records only)
EXECUTOR = pe-reconstruction (PE-MASTER direct dispatch, NO_NESTED_TASKS)

## 1. VERBATIM human instruction (the authorization source)

Origin: direct human message in the OpenCode PE-MASTER session on 2026-10-07,
relayed to this executor inside the PE-MASTER direct dispatch of this run.
Preserved verbatim below, exactly as received in the dispatch. This file was
first written to disk at the system time recorded in section 3.

---BEGIN VERBATIM HUMAN INSTRUCTION---
Autoryzuję wykonanie dokładnie jednego runu według:
C:\Users\User\Documents\ChatGPT\PE\PE_935_CAND4_CHILD_ROOT_PROMPT_REVIEW_20261007\OPENCODE_CAND4_CHILD_ROOT_REVIEWED.md

RUN_ID:

PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007

EXPECTED_BASE_SHA:

d65fa12e5bae4e9aab291c3cc7815b1822e41cff

Autoryzuję pełny zakres tego jednego bounded static RE oraz przewidziane w kontrakcie internal QC, persistence, commit i push.

Nie autoryzuję żadnego rozszerzenia poza kontrakt, w szczególności historical XYZ, static-building channel, paging/network, nowych transform semantics, CMO↔ACLD identity, ExtraData ani runtime.

Producer/writer coverage należy rozumieć wyłącznie jako producentów osiągniętych w zadeklarowanym bounded scope, z jawnym wskazaniem luk pokrycia. Nie wymagam ani nie autoryzuję globalnego writer census całego EXE.

Jeżeli preflight SHA/EXE/allowlist nie przejdzie, zatrzymaj run jako BLOCKED.

Po wykonaniu i publikacji wykonaj HARD STOP. Nie uruchamiaj automatycznie kolejnego RE, qualification, transform runu ani correction cycle.

NEXT_EXPERIMENT_AUTHORIZED po tym runie pozostaje NO.
---END VERBATIM HUMAN INSTRUCTION---

## 2. Adjudication of this dispatch's phase boundary (executor-visible)

The contract (OPENCODE_CAND4_CHILD_ROOT_REVIEWED.md §12) orders the full terminal
sequence including AUDIT_ENTRYPOINT update, one allowlist-only commit, push, live
remote verification and HARD STOP.

The PE-MASTER dispatch message for THIS executor task explicitly assigns the
current phase of THIS executor:

- "W TEJ FAZIE: NIE edytuj entrypoint, NIE commit/push; proposed newest-first row
  w HANDOFF.md"
- "Manifest LAST: scope = fizyczne pliki OUTPUT_ROOT minus manifest (entrypoint
  wykluczony do-persistence — odnotuj w nagłówku); pełna bijekcja + niezależny
  re-hash zero mismatch."
- "HARD STOP po pakiecie."
- Terminal response must report "RESULTING_SHA=NONE (ta faza)".

Therefore this executor performs: SCIENCE (bounded static RE per §4–§7) + the four
§9 controls + fresh-context internal QC (SELF_CHECK; §9) + PACKAGE (§12), writes
the proposed AUDIT_ENTRYPOINT.md newest-first row in HANDOFF.md ONLY, generates
the final MANIFEST_SHA256.csv LAST over the physical package files (self-excluded;
the AUDIT_ENTRYPOINT.md row EXPLICITLY OUT of this phase's manifest scope —
excluded pending persistence, noted in the manifest header), verifies full
bijection + independent re-hash, and STOPS. No AUDIT_ENTRYPOINT.md edit, no git
stage, no commit, no push by this executor.

AUTHORIZATION_FOR_COMMIT_PUSH = GRANTED_IN_VERBATIM_INSTRUCTION (section 1) with
scope REPO_WRITE_ALLOWLIST = OUTPUT_ROOT/** + persistence-only AUDIT_ENTRYPOINT.md;
EXECUTION of the commit/push belongs to the PE-MASTER persistence phase after its
own audit of this package. RESULTING_SHA = NONE (this phase).

Classification of this phase split: ORCHESTRATOR_PHASE_SPLIT — recorded here from
the dispatch text as received, not reconstructed from auditor comments (the
established methodology).

PE_MASTER_REVIEW.md in this package is a PLACEHOLDER: no PE-MASTER review of THIS
run exists at package time (INDEPENDENT_REVIEW = NOT_PERFORMED — explicitly marked
NOT_PERFORMED-do-persistence); the persistence phase fills it after the PE-MASTER
audit. An internal/advisory review is not an external Desktop post-audit and not
a PE-MASTER qualification.

## 3. Write time (system)

GOVERNANCE_DECISION_WRITE_TIME = 2026-10-07T11:00:55Z (UTC; system time captured
when OUTPUT_ROOT was created immediately before this file was first written to
disk; local system timezone offset UTC-07:00, local wall clock 2026-10-07T04:00:55-07:00).

## 4. Preflight verification record (measured, before any science work)

- git fetch + git rev-parse HEAD / origin/master + git ls-remote origin
  refs/heads/master, queries 2026-10-07T10:54:00Z / 2026-10-07T10:54:17Z (UTC):
  LOCAL_HEAD = d65fa12e5bae4e9aab291c3cc7815b1822e41cff == origin/master ==
  actual remote (git ls-remote refs/heads/master) == EXPECTED_BASE_SHA. MATCH.
  No error returned.
- Relevant tracked changes: NONE (git status --porcelain: no modified/staged
  tracked paths; only untracked).
- Foreign untracked inventoried (6 roots, untouched by this run):
  docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/,
  docs/audits/PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003/,
  docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/,
  docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/,
  docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/,
  experiments/.
- OUTPUT_ROOT absent before this run (collision check PASS; measured
  Test-Path = False at 2026-10-07T10:54:41Z); created by this run at 11:00:55Z.
- EXE identity re-verified at preflight (measured):
  D:\Eudoria_Reconstruction\pcg_install\Entropia.exe = 8,015,872 B / SHA256
  E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 — MATCH;
  fail-closed re-verified inside every analysis tool of this package.
- Contract identity re-verified at preflight (measured):
  C:\Users\User\Documents\ChatGPT\PE\PE_935_CAND4_CHILD_ROOT_PROMPT_REVIEW_20261007\OPENCODE_CAND4_CHILD_ROOT_REVIEWED.md
  = 18,159 B / SHA256
  57249511611ADFA68161D9F2363DCB9831BFF36C9C913B59C83251B5D8C17568 — MATCH the
  dispatch-pinned identity. Read in full (375 lines, §1–§12) from disk before any
  work; applied literally, not modified.
- Prior-evidence package identity at the exact BASE (read-only):
  - docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/ (the
    audited source run): 49 files tracked at BASE; 49 physical files present;
    49/49 git-blob identity match (blob SHA-1 recomputed from disk bytes, zero
    mismatches); package aggregate SHA256 (sorted "path sha256" lines) =
    AB21CBC3991C91B19BD884F851E0FE24F1EBA251B48E24643A71F6169BE65B5B.
  - docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007/
    (the J1–J3 correction of that source run): 27 files tracked at BASE; 27
    physical files present; 27/27 git-blob identity match (zero mismatches);
    package aggregate SHA256 =
    80AB81F5E3F6686D1CA13CDF89EDB119793D8C661B853E741B569EB8AE21A164.
  Both packages are READ-ONLY for this run (historical manifests and records
  immutable); their supersessions J1–J3 are carried into this run's ACTIVE
  statuses (see PREREGISTRATION.md §0 and FINAL_REPORT).

## 5. Contract identity

CONTRACT_PATH = C:\Users\User\Documents\ChatGPT\PE\PE_935_CAND4_CHILD_ROOT_PROMPT_REVIEW_20261007\OPENCODE_CAND4_CHILD_ROOT_REVIEWED.md
CONTRACT_SIZE_BYTES = 18159
CONTRACT_SHA256 = 57249511611ADFA68161D9F2363DCB9831BFF36C9C913B59C83251B5D8C17568

## 6. Hard governance statuses carried into this run (unchanged)

WORLD_XYZ_RECOVERED = NO
HISTORICAL_INSTANCE_DATA_RECOVERED = NO
STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED
CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO
RUNTIME_JOIN_OBSERVED = NO (always; static-only lineage)
REAL_SCIENCE_AUTO_QUALIFICATION = DISABLED (corrected-lineage policy; no tool of
  this run issues a SCIENCE_PASS; component statuses are adjudicated by the
  author's physical proof records, checked — not promoted — by internal QC)
QC_POSITIVE_CHAIN_QUALIFICATION = NOT_ESTABLISHED_AS_GENERAL_AUTHORITY

## 7. Not authorized by this run (contract §11 prohibitions, honored)

No historical XYZ, static-building channel, paging/batching, network origin,
CMO↔ACLD identity work, new transform semantics, ExtraData/readback
(FUN_007B68B0), global Ni/model atlas, runtime or client execution; no new
VFS/BNT/NIF payload opening (existing persisted metadata/records only); no
FUN_007BF470 / separate parent-join proof (JOIN_OPERATION = STRONGLY_SUPPORTED
is the ceiling of this run — not to be raised); no transfer of identity or
transforms from the CMO+0xC0 holder into the ACLD chain; no new real fields or
objects in the EXE created only for the §9 controls.

Publication of this package (by the persistence phase) is not acceptance;
negative/partial results are publishable. This run does not close the
CAND-4 child question if the physical evidence does not support it.
