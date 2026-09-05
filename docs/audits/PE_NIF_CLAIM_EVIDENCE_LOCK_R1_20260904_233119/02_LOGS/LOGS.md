# 02_LOGS — commands, tool versions, errors and disposition
# PE-NIF-CLAIM-EVIDENCE-LOCK-R1 (all commands executed on the VM project tree)

## Tool versions
- Node.js v22.22.0 (all control scripts .cjs; no external dependencies)
- Windows PowerShell 5.1 (filesystem operations, hashing via Get-FileHash)
- git (repo D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean; read-only:
  rev-parse / show / diff --numstat / log / status only — NO checkout, NO
  reset, NO commit, NO push)
- Python: NOT used this round (no historical driver was executed)

## Prompt integrity
- NEXT_OPENCODE_PROMPT.md SHA256 verified BEFORE execution:
  BFDB1D23E42904FB29CBDB5995D072B8C793AB5D4E241E28BF7F3EFA8EEBA562 (match)
- AUDIT_OUTPUT_ROOT did not exist at check time (Test-Path = False); created
  fresh with the required structure.

## Control instrumentation (one-time, 00_CONTROL only)
- control_r1.cjs — execution history (hash-after-last-edit rule):
  - exec 1: SHA256 6A296CC778861FB6F9F684DBCCBD7CE0ACA938599E2BA300AFE327E4A36922BC
    (recorded in SHA256_CONTROL.txt BEFORE execution). COMPLETE, but the
    strict-CSV validation counted a trailing blank line in
    PE_NIF_CROSS_ERA_R35 artifact_index.csv as a 12th bad row (my split()
    vs the auditor's .trim() standard). DISPOSITION: parser artifact,
    not a data finding.
  - exec 2 (FIX: trim trailing blank lines — probe.cjs-compatible standard):
    SHA256 5AD889D34D7A1507F74FC7BF6005C5738F609093FFBCE02035C517BE9FC7A9A6
    (recorded in SHA256_CONTROL.txt BEFORE execution). COMPLETE; 11 strict
    errors in exactly the 8 manifests the auditor named. ALL OTHER RESULTS
    IDENTICAL to exec 1 (f1 985/142/30; denominators 6167/2427/3186/2093;
    574845 k=1; era join 5208/214/4/174; c==CRC32 11022/11022 0 mismatches;
    d==c 3435/5596 + 3299/5426; 3 d-exceptions; witnesses 214/9/214/29/214;
    R40 apply sim==actual; +236 combined).
- generate_claim_matrix.cjs — emits 05_ANALYSIS/CLAIM_MATRIX.csv (43 rows,
  all fields quoted). Iterated 3 times for column/status hygiene: the first
  hand-written CSV had 26 unquoted-comma rows (REPLACED by generator output);
  two intermediate generator versions carried mixed knowledge statuses
  (violating the one-status-per-atomic-claim gate) — FIXED by splitting
  compound rows (C-R38-02 -> 02/02B; C-R38-03 -> 03A..03D) and assigning
  exactly one of the 5 taxonomy values per row. Final CSV validated: 43 rows,
  0 bad rows, statuses {CONFIRMED 24, REJECTED 9, STRONGLY_SUPPORTED 7,
  UNVERIFIED 2, PLAUSIBLE 1}.
- generate_gates.cjs — emits STAGE_ACCEPTANCE_GATES.csv. The first hand-
  written gates CSV had 8 unquoted-comma rows (the same defect class this
  round audits in the historical manifests — caught by my own validator);
  REPLACED by generator output (17 rows, 0 bad).
- generate_artifact_index.cjs — emits artifact_index.csv (55 file entries +
  1 self-exclusion row, all strict-quoted). Regenerated after each artifact
  change; FINAL full verification: all 31 non-manifest run files listed with
  correct SHA256 (0 mismatches), 0 bad rows.
- csv_validate.cjs — strict CSV validator (written to the approved temp dir
  C:\Users\User\AppData\Local\Temp\opencode — OUTSIDE the protected trees;
  identical logic embedded in control_r1.cjs). Validated: CLAIM_MATRIX.csv,
  ALLEGATION_DISPOSITIONS.csv and all 12 normalized sidecars: 0 bad rows.

## Read-only source operations (no writes to any protected path)
- Both Models.bnt containers: opened read-only (fs.readFileSync), direct
  BNT2 index parse, payload CRC32 re-computation, era join, family scan.
- 12 run dirs: REPORT.md, STAGE_ACCEPTANCE_GATES.csv, artifact_index.csv,
  02_results JSONs, 01_source driver (R34) — READ ONLY.
- git repository eudoria-clean: rev-parse HEAD = 8cd0bc3f81bb131413574d6f9d64fb90b3114c39
  (matches the audit-time HEAD; docs/nif clean vs HEAD; diff 077b8a4..HEAD on
  docs/nif = empty). git show 077b8a4^ / 077b8a4 for the wiki pre/post states;
  git diff --numstat for the +236 verification. NO write operation issued.
- PE_AUTO_LOOP.json, PE_* context files: READ ONLY (loop state not modified;
  last_completed = ITER-40 unchanged).

## ACTIVE_WRITER.lock consideration
- ACTIVE_WRITER.lock v2 (heartbeat 2026-09-04T10:25:00) scopes the WRITER to
  PE_AUTO_LOOP.json, PE_MILESTONE_1_WORLD_SURFACE_R1, eudoria-web, canonical
  working state files. This round writes ONLY to the new run dir
  PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119 and reads all writer-scope
  paths read-only -> NO conflict; no dependent work stopped. The lock
  heartbeat is stale (>60 min) but this round does NOT take over the lock
  (no need — no writer-scope path is written).

## Errors encountered and disposition
1. exec-1 trailing-blank-line false error (R35) — fixed with trim; documented.
2. PowerShell inline node -e with embedded quotes failed (parser error) —
   replaced by script files; no data impact.
3. First [regex] PowerShell edit attempt had a syntax typo — abandoned in
   favor of the edit tool; no file corruption (target file regenerated).
4. No other errors. All JSON/CSV outputs pass syntax validation (gate).

## Runtime / game execution
- NOT RUN (see 04_RUNTIME/NOT_RUN.md). No PE.exe, no game, no emulator, no
  Ghidra, no historical driver executed.
