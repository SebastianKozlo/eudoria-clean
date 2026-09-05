# PE_NIF_R3_PROPOSAL_APPLICATION_R1 — RUN-B (executed prompt, formalized)

TASKING: agent pe-reconstruction executes RUN-B: the bounded wording-only
application of the R3 proposals P1–P5 to docs/nif per TARGET_MAP.json
(HR-R3-3 = GO issued by the human via PE-MASTER).

AUTHORITATIVE INPUTS (SHA256 verified before execution):
- TARGET_MAP.json: 99_Audits\PE_NIF_R3_PERSISTENCE_AND_TARGETMAP_R1_20260905_101203\05_ANALYSIS\TARGET_MAP.json
  (SHA256 D3F043F2167C1BD0EDBC9C4F7957D5FD31AF37C8296848DEEB9350DDA7699628)
- Fixed texts: 06_REPORT\PROPOSALS_P2P3_FIXED.md (same run dir, SHA256
  65DC552806C2C2A1E27A7ABDB227B4CCF09A8C2A473BC6A9628655298A88DE27); original
  proposals at 99_Audits\PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627\06_REPORT\PROPOSED_DOC_CORRECTIONS_R3.md
  (SHA256 84B3D05DB719AB09A6CEECE8300BBEE059655B5443F6B5CFC1090B4C8B7EC8E6)
- Repo: 12_WebGame\eudoria-clean (HEAD 642bc12 at orchestrator check; actual
  BASE_SHA captured by this run itself; working tree clean; staged index EMPTY)

THE 16 OPERATIONS (exactly per the map; breakdown 3 REPLACE / 9 LEDGER-ENTRY /
2 STANDING-RULE / 2 STANDING-POLICY):
- 3 REPLACE in docs/nif: P1R2-5-R3/a+b (09-semantics.md — the "position
  deltas" + related fragments) and P2R2-2-R3-FIXED/main (10-containers-corpus.md
  — the cross-era conclusion block). Map old/new texts used verbatim;
  whitespace-normalized matching per the census method; the map's
  machine_verification fields are the checklist.
- 13 annotation operations (P3R3/P4R3/P5R3) per the operations_legend:
  LEDGER-ENTRY = "historical file preserved byte-identical; entry records
  superseded wording"; STANDING-RULE = "new standing text; no superseded file
  wording"; STANDING-POLICY = "acceptance/policy guard; anchor fragment
  verifies the referenced historical wording". The referenced historical files
  (the R2 package, both local 99_Audits tree and repo copy) stay
  BYTE-IDENTICAL (re-hashed before/after, both recorded); the ledger/standing
  entries carry the map's verbatim new_text payloads + evidence_pointer +
  lineage_ref. Anchor fragments verified read-only. .pre byte-prefix proofs
  saved for appended annotations; pre-edit copies saved for the 3 REPLACE
  targets (before/after SHA registry).
- SYNC: every repo-created file byte-identical in the local 99_Audits tree.

GATES (PASS = all; fail-closed; each gate = executable check with recorded raw
result): G1 pre — re-verify ALL 13 old fragments EXACTLY-ONCE before editing
(abort if any missing/duplicated). G2 post — new texts present VERBATIM
(whitespace-normalized) in the 2 docs/nif targets; old fragments ABSENT.
G3 post — forbidden-clause scan over docs/nif = 0 hits (the forbidden phrases
from PROPOSALS_P2P3_FIXED.md, machine-checked). G4 post — ALL docs/nif files
OUTSIDE the 2 targets hash-identical before/after (13-file registry).
G5 — annotations APPEND-ONLY (+ .pre byte-prefix proofs); historical files
byte-identical. G6 — ONE path-limited commit: inspect staged index BEFORE add
(must be empty; report it), add ONLY the explicit run paths (the 2 docs/nif
files + ledger/standing annotation files + the run package dir
docs/audits/PE_NIF_R3_PROPOSAL_APPLICATION_R1_<ts>/), VERIFY git diff --cached
--stat lists EXACTLY those paths, commit (message: RUN + subsystem + result),
push origin/master (no force), verify remote SHA == local HEAD. If the remote
moved mid-run: re-evaluate safely (rebase-free; re-add paths on new HEAD),
never reset.

NON-PASS modes (recorded): EXACTLY_ONCE_FAIL / POST_EDIT_TEXT_MISMATCH /
FORBIDDEN_PHRASE_PRESENT / COLLATERAL_EDIT / ANNOTATION_APPEND_FAIL.
HARD STOP: fragment missing/duplicated | hash-drift of a non-target | ANY
proprietary payload in the commit.

OUTPUT RUN PACKAGE: 99_Audits\PE_NIF_R3_PROPOSAL_APPLICATION_R1_<ts>\
(00_CONTROL with NEXT_PROMPT + driver + SHA256_DRIVER.txt; 01_RAW gate
results + fragment verifications; 05_ANALYSIS before/after SHA registry +
edit log; 06_REPORT\00_FINAL_REPORT.md; REPORT.md pointer; HANDOFF.md;
STAGE_ACCEPTANCE_GATES.csv; artifact_index.csv with REAL SHA-256,
self-exclusion documented). The package is also published to
docs/audits/PE_NIF_R3_PROPOSAL_APPLICATION_R1_<ts>/ in the commit (G6).

MILESTONE_PROGRESS vector (mandatory in the report): edits_applied 16/16;
fragments_reverified 13/13; forbidden_hits 0/<n files scanned>;
collateral_edits 0/<13 registry files>; ledger_entries 9/9; standing_rules 2/2;
standing_policies 2/2 (anchor verifications); commit_files <n>; what
counts/what excluded stated explicitly.

STANDING RULES: no M2-advancement claims; no payloads; jeden run = jeden
commit; re-hash every cited SHA personally; wording-only (any evidence-status
change = FAIL per the PE-MASTER design — a status-word change inside the
replaced text counts as FAIL only if it changes the claim's evidential status,
not if the proposal text itself carries the corrected statuses verbatim — the
map's new_texts are the authority).
