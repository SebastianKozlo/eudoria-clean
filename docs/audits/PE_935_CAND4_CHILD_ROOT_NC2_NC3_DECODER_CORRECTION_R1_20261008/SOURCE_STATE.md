# SOURCE_STATE — PE_935_CAND4_CHILD_ROOT_NC2_NC3_DECODER_CORRECTION_R1_20261008

RUN_ID: PE_935_CAND4_CHILD_ROOT_NC2_NC3_DECODER_CORRECTION_R1_20261008
RUN_CLASS: RECORDS_AND_QC_MACHINERY_CORRECTION
REPO_ROOT: D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean
EXECUTOR_SCOPE: NC2+NC3 decoder correction (production side) + PRE/POST matrices +
regressions A–D ONLY. Zero new science, zero new RE, zero EXE access, zero new
function bodies opened, zero runtime. No commit / stage / push / manifest / AUDIT_ENTRYPOINT
edit — the parent (PE-MASTER) owns the QC phase and publication.

## 1. Base state (measured, fail-closed)

- LOCAL_HEAD = origin/master = live remote master = 91598a9868037c4954e22e16c535d6a5a671771e
  (= EXPECTED_BASE_SHA; queries with UTC timestamps in INPUT_IDENTITIES.md §1).
- `git fetch origin` exit 0; live `git ls-remote` answered (remote AVAILABLE).
- `git status --porcelain=v1` at preflight (2026-10-08T07:16:43Z): NO tracked changes;
  only foreign untracked paths (census in §3).
- OUTPUT_ROOT did not exist at preflight (Test-Path = False).
- HEAD re-verified at end of run (2026-10-08T07:20:37Z): still 91598a98…; this run
  created NO commit and staged NOTHING.

## 2. What this run created (the ONLY writes; all inside OUTPUT_ROOT)

| file | size (B) | SHA256 |
|---|---|---|
| INPUT_IDENTITIES.md | 8122 | 48B8FBAECD4FAAF2769BA55C553801ABC56F6C3A9F090FACC8B47AB41D1403E3 |
| SOURCE_STATE.md | (this file; hashed after write) | (recorded in handoff) |
| 03_SCRIPTS/ctrl4_exact_endpoint_nc23fixed.py | 21069 | 68BEC1AEFDF6A0F32A3ED12F3AED9B72255F8A89AA2F5BA4EFD11C709C4D9F13 |
| 03_SCRIPTS/run_nc23_matrix.py | 63594 | C3FCDA6C5285AD289EFA908FDD789297EC081286FD5F08F79329B1A0D4A36247 |
| CONTROL_RESULTS_PRE.json | 51477 | 00A90A837E08E1FE7661C0C1E184417200E494587F1FB3A4E098A93B3D7E08B1 |
| CONTROL_RESULTS_POST.json | 71311 | 5E09A5126672F63D2F6C1E19543505597FF80B2C55C13259139DB78C3E12E49D |

Exactly the six delegated files; NO extra files, NO residue (no __pycache__/.pyc under
OUTPUT_ROOT — verified; scripts run with `python -B` AND `sys.dont_write_bytecode = True`;
temporary blob-extraction files lived only in the pre-approved temp area
C:\Users\User\AppData\Local\Temp\opencode and were removed at run end).

## 3. Foreign untracked census (recorded, NEVER touched/staged/cleaned)

Present at preflight and unchanged at the end-of-run census (2026-10-08T07:20:37Z):

    ?? docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/
    ?? docs/audits/PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003/
    ?? docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/
    ?? docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/
    ?? docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/
    ?? experiments/

After this run the census additionally shows `?? docs/audits/
PE_935_CAND4_CHILD_ROOT_NC2_NC3_DECODER_CORRECTION_R1_20261008/` — this run's own
OUTPUT_ROOT (untracked, unstaged — publication is the parent's phase).

## 4. READ-ONLY source packages — untouched (re-verified after the run)

- SOURCE_PACKAGE docs/audits/PE_935_CAND4_CHILD_ROOT_NC1_SIB_DECODER_POST_AUDIT_CORRECTION_R1_20261007/
  — 03_SCRIPTS/ctrl4_exact_endpoint_sibfixed.py re-measured 17740 B /
  44155437F20FA6DA9D6847A236F708C7F2A40F26BABE71424B21C325B4FB4405 (unchanged);
  00_CONTROL_INTERNAL_QC/qc_ind_ctrl_sib_own.py re-measured 51943 B /
  529B61DB312AEC338221425B12F2D94DE2BE351B5C62F68DDBA6BF915B007B25 (unchanged).
- PRIOR_SCIENCE_PACKAGE docs/audits/PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007/
  — 01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt re-measured 4043 B /
  A0DEFAA16D6934FC307BD88210BCCA59B823C58FB57319A2C090F9ED59AD01E3 (unchanged).
- PRIOR_CORRECTION_PACKAGE docs/audits/PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007/
  — 03_SCRIPTS/ctrl4_exact_endpoint.py re-measured 20592 B /
  FDB5F16E6F9A6352030DD2F4D9523E1CAA0AB924F2112DDEC787CC7B3A84A330 (unchanged).
- `git status` shows zero tracked changes anywhere in the repo (both censuses) ⇒ no
  READ-ONLY tracked file differs from its committed blob at 91598a98.
- AUDIT_ENTRYPOINT.md: NOT touched by this run (still unmodified; no tracked changes).
- The historical QC script's top level (which writes QC_RESULTS.json) was NEVER
  executed: PRE used SAFE AST EXTRACTION ONLY (see CONTROL_RESULTS_PRE.json
  METHOD_SAFE_AST_EXTRACTION: whitelisted symbols, static call census, isolated
  namespaces, `top_level_executed: false` for both sources).
- No EXE access. No FUN_006C9700 / FUN_006C8BB0 / transform / placement work. No new
  function bodies opened. All eight matrix buffers are SYNTHETIC / IN-MEMORY.

## 5. Execution facts

- New production module: 03_SCRIPTS/ctrl4_exact_endpoint_nc23fixed.py — successor of the
  READ-ONLY sibfixed production checker (91598a98, SHA256 44155437…); module INERT at
  import; NO file I/O; P1–P4 predicate unchanged; checker catch only
  (ValueError, IndexError); NC1 SIB guard preserved in EVERY memory-ModRM branch;
  NC2 (0x84 all memory TEST forms rejected before any length computation; register TEST
  84 C0 kept), NC3-B (LEA mod=11 rejected explicitly before operand formatting →
  controlled (False, diagnostic), never TypeError); 0xFF branch UNCHANGED (only /2
  mod=11; no FF /6 or extra forms); P3 grp1-imm8 fix kept.
- Executor: 03_SCRIPTS/run_nc23_matrix.py — executed 3 times with `python -B`
  (~2026-10-08T07:17Z–07:19Z): run 1 aborted at the AST static call census guard
  (RuntimeError, no evidence accepted; see §6), run 2 exit 0, run 3 exit 0 (after the
  cosmetic JSON-key typo fix) — runs 2 and 3 measured IDENTICAL results
  (deterministic).
- Production authenticity: the ACTUAL corrected function was executed via importlib
  (not an imitation); production script SHA256 measured at run time
  (68BEC1AEFDF6A0F32A3ED12F3AED9B72255F8A89AA2F5BA4EFD11C709C4D9F13) and recorded in
  CONTROL_RESULTS_POST.json production_checker.script_sha256.
- PRE: REAL HISTORICAL functions (AST-extracted sibfixed production checker +
  qc_ind_ctrl_sib_own QC checker) run on the SAME eight buffers; all 8 cases × both
  checkers reproduced the contract-expected historical behavior; PRE_REPRODUCED = True
  (per-case flags in CONTROL_RESULTS_PRE.json). The historical LEA TypeError was
  captured as {"production": "ERROR:TypeError"} — never recorded as FAIL.
- POST: 8/8 matrix rows match (clean PASS; clobber/esi/nop/NC1 SIB/NC2 TEST/NC3 FF D8/
  NC3 LEA FAIL). Regressions: A clean 22-instruction VA/size map identical to the
  published record (total 0x42, P1/P3/P4 endpoints exact) PASS; B 9-form historical SIB
  battery vs the NEW decode all rejected PASS; C 144-form sweep vs the NEW decode all
  rejected at DECODER level (form set byte-identical to the cited Desktop sweep) PASS;
  D NC2/NC3 mechanisms + instruction-level diagnosis citing the Desktop reference
  decode (capstone 5.0.7, cited; nothing installed) recorded. Register-form support
  (8B/8B-reg/89-reg/84 C0/8D 06 mem LEA/FF D2) verified intact + 4 negative controls
  raise with the expected mechanisms. All 9 executor gates TRUE, OVERALL PASS.

## 6. Honest scope statements

- QC phase (fresh independent internal QC, QC_RESULTS.json, QC_REPORT.md, SUPERSESSION,
  FINAL_REPORT.md, PE_MASTER_REVIEW.md, HANDOFF.md, MANIFEST_SHA256.csv,
  AUDIT_ENTRYPOINT.md line, commit/push, live remote verify): NOT performed by this
  executor — that is the parent's phase per the delegation. QC_REPAIR_ROUNDS_MAX=1
  applies there, not here; this executor needed zero repair rounds.
- NEW_CORRECTION_DESKTOP_POST_AUDIT = NOT_PERFORMED (this run is not and does not
  replace the future Desktop post-audit).
- Strongest permitted claim of this executor phase: the NC2/NC3 production-side defects
  are corrected and revalidated WITHIN THE TEST SCOPE of the eight-case matrix, the
  9-form battery and the 144-form sweep (matrix_verdict PASS). The final
  CORRECTED_AND_REVALIDATED_IN_TEST_SCOPE naming belongs to the positive QC gate
  (parent). NEVER claimed: GENERAL_X86_DECODER_PROVEN.
- Science status untouched: NC1 remains CLOSED_FOR_AUDITED_STATE for 91598a98;
  historical results remain authentic and unchanged; no science created or retracted.
- Deviations from the delegation: none. One in-scope repair during development (the
  AST static call census initially rejected `ValueError(...)` constructor calls in the
  extracted historical raise statements; the allowlist was extended to exception-class
  constructors — inherently non-I/O — before any evidence file was accepted; the census
  guard against open()/exec()/import() etc. remains intact and is recorded in PRE).
