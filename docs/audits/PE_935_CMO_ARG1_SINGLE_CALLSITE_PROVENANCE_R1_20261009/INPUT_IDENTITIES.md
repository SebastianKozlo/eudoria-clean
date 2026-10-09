# INPUT_IDENTITIES — PE_935_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009

All identities below were MEASURED by this executor (pe-reconstruction,
OpenCode session on Windows host `WinDev2407Eval`; STATIC_ONLY — the client
never ran) before any science work. Every hash is a full re-hash of the
physical file. Git blob identity = `git hash-object <physical file>` compared
to `git rev-parse HEAD:<path>`.

## 1. Frozen contract and actual dispatch scope

| Item | Measured value |
|---|---|
| Contract path | `C:\Users\User\Documents\ChatGPT\PE\PE_CMO_ARG1_SINGLE_CALLSITE_PROMPT_20261009\OPENCODE_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009.md` |
| Contract size | 18964 B |
| Contract SHA256 | `9BAF558EA21751B59FA00C41EF532CA20D829AA6082804387DD4BDB71BBF4939` |
| Identity verdict | **MATCH** (contract §0 requirement satisfied; no substitution or edit) |

Actual dispatch instruction scope (the PE-MASTER delegation message that
invoked this run; preserved as the operative scope for THIS phase):

- RUN_ID = `PE_935_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009`;
  RUN_CLASS = `BOUNDED_STATIC_ARGUMENT_PROVENANCE`.
- Executor phase ONLY. This executor writes EXCLUSIVELY under
  `docs/audits/PE_935_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009/`:
  `PREREGISTRATION.md`, `INPUT_IDENTITIES.md`,
  `01_EVIDENCE/WINDOW_IDENTITY.json`, `01_EVIDENCE/CALLSITE_DISASSEMBLY.txt`,
  `STACK_LEDGER.csv`, `ARG1_PROVENANCE.json`, `CONTROLS_RESULTS.json`,
  `03_SCRIPTS/run_stack_controls.py`.
- `QC_RESULTS.json` + `QC_REPORT.md` = the fresh-QC worker's phase;
  `FINAL_REPORT.md`, `EVIDENCE_INDEX.md`, `HANDOFF.md`, `MANIFEST_SHA256.csv`,
  the AUDIT_ENTRYPOINT.md row and any commit/push = later parent phases.
- `NO_NESTED_TASKS`; no AUDIT_ENTRYPOINT.md writes; **no stage/commit/push by
  this executor**; `python -B`; no residue; temporary disassembler inputs in a
  task-owned OS temp directory OUTSIDE Git, identities recorded, outputs
  captured, only own temp files removed, never staged.
- The dispatch quotes the contract's pre-verified window pins
  (BASE_SHA, EXE identity, 28-byte window/offset/SHA, the six control cases,
  the §8 standing) and instructs re-verification of all of them — performed
  below and in the run outputs.

Contract-vs-dispatch consistency check: the frozen contract §7/§9 includes
persistence steps (entrypoint row, manifest, commit, push). The actual dispatch
explicitly reserves those to later parent phases for THIS run. This matches the
established repo phase-split precedent (e.g.
`PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009/SUPERSESSION_AND_STANDING.md`
§6 "Phase boundaries (delegation)"). Recorded as the dispatch instruction
scope — NOT silently bypassed, NOT treated as an authorization to publish.

Process note (honest residue record): during INPUT_IDENTITIES drafting, one
`write` call briefly created a stray placeholder file at
`D:\Eudoria_Reconstruction\12_WebGame\eudocracy-clean\INPUT_IDENTITIES_PLACEHOLDER.md`
(typo'd directory name — a path OUTSIDE the git repo
`D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean`). Detected immediately;
the stray file and the typo'd directory were removed in the same session;
verified `CONFIRMED_GONE`. The git repo worktree was never touched by it;
`git status` remained clean-tracked throughout.

## 2. Repository state (git triple, fail-closed)

| Check | Measured value |
|---|---|
| Local HEAD | `e687eb1360cc0f6f4c4d7c8db7587bb5d357bc6b` |
| `origin/master` | `e687eb1360cc0f6f4c4d7c8db7587bb5d357bc6b` |
| Actual remote `refs/heads/master` (live `git ls-remote origin master`) | `e687eb1360cc0f6f4c4d7c8db7587bb5d357bc6b` |
| EXPECTED_BASE_SHA (contract) | `e687eb1360cc0f6f4c4d7c8db7587bb5d357bc6b` |
| Triple verdict | **MATCH** |
| Tracked tree | CLEAN (`git status --porcelain=v1` shows zero tracked modifications/staged changes) |
| OUTPUT_ROOT before work | ABSENT (verified; created only after preflight PASS) |

Foreign untracked census at preflight (NOT touched, NOT absorbed, left
exactly as found; exact measured census lines):

```text
?? docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/
?? docs/audits/PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003/
?? docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/
?? docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/
?? docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/
?? experiments/
```

## 3. Target binary (read-only; full re-hash)

| Item | Measured value |
|---|---|
| EXE path | `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe` |
| EXE size | 8015872 B (expected 8015872 B) |
| EXE SHA256 (full physical re-hash, BEFORE work) | `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` |
| Expected SHA256 (contract §2) | `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` |
| Verdict | **MATCH** |

The helper `03_SCRIPTS/run_stack_controls.py` re-hashes the full EXE again
inside the run (before its reads and after all work, fail-closed); the
after-work re-hash is recorded in `CONTROLS_RESULTS.json` /
`ARG1_PROVENANCE.json`.

## 4. Required repository inputs at EXPECTED_BASE_SHA (contract §2 table)

Physical size + SHA256 + Git blob identity (HEAD:blob == hash-object(physical)
proves the physical full bytes equal the committed blob):

| Path (repo-relative) | Bytes | SHA256 (physical, measured) | Expected SHA256 | Blob match |
|---|---:|---|---|---|
| `docs/audits/PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009/CONTROL_RESULTS.json` | 18509 | `9545D0D78881C29BC805EA3A05C8AA936D364256671D31A1AE907677A63DE2F8` | `9545D0D7…63DE2F8` | YES (`6645aa4b0bd552173b33d0a8c389af1012ec5224`) |
| `docs/audits/PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009/FINAL_REPORT.md` | 15589 | `FF5FDBD2F54F20E3026B5992F7BCC411B0572ADA249F157BA11CB441E1AC83E0` | `FF5FDBD2…E1AC83E0` | YES (`4c170743ed98eaf752f4e3fc74588686e8dbc570`) |
| `docs/audits/PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009/SUPERSESSION_AND_STANDING.md` | 6848 | `0AB2CDECE09CB2FF1419C48E9A1169832A0A061C618A7F94F290089C75F49921` | `0AB2CDEC…75F49921` | YES (`52f4158500d40acdf839838797e17f2d108df797`) |
| `docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007/SUPERSESSION.md` | 8339 | `DD11137A0E79491511A7688B7C1DE9252DB7BA443FA31892C345CA76CE136845` | `DD11137A…CE136845` | YES (`05de1ce999c351d366aa5ad4d3cded8dd1c8b49b`) |

All four sizes and hashes MATCH the contract pins. All four were READ by this
executor (read-only) for: the prior pinned W3 record (window bytes beginning
two bytes before ours), the callsite pins and rel32 recompute of the prior
package, the callee entry-convention evidence (pinned instruction list of
FUN_0085B1B0: entry `mov eax,[esp+0x8]` = the arg2 slot at entry;
`mov edi,[esp+0x14]` @0x0085B1DA after four pushes = the ARG1 slot), and the
§8 standing / supersession state. No historical file was modified.

## 5. Governance inputs actually read (contract §2 "read current AUDIT_ENTRYPOINT.md and applicable governance")

| Path | Size (B) | SHA256 (measured) | Blob match vs HEAD |
|---|---:|---|---|
| `AUDIT_ENTRYPOINT.md` (repo root) | 271684 | `53528A82695C710FCF68ACD60BAF9B9442CD649B89F4C82E35F81ED86660E5BB` | YES (`aa072c4ea32bc8fa22c08ce7b3c07f5855a66e4d`) |

Applicable governance state read from it: current milestone EU935-M1 OPEN;
PE-MASTER status `PROVISIONAL_UNTIL_QUALIFIED` (advisory verdicts only,
canonical authority blocked pending human-graded Q1); the two immediately
preceding CMO runs (`PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009`,
`PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009`) are the LATEST RUNS
rows. Further applicable governance documents read = the two SUPERSESSION
records in §4 above (CMO-C1 `SUPERSESSION_AND_STANDING.md` — DOC-1..DOC-4
backlog, J3 standing carried verbatim, phase-boundary precedent; J3
`SUPERSESSION.md` — S-1..S-5 supersession set, preserved partial science, the
`ORIGINAL_J3_EDGE_BUDGET_COMPLIANCE = FAIL` standing). No other
PROJECT_STATE/governance file applies: no `PROJECT_STATE.json` is present in
the repo.

Conflict check (contract §2): no governance rule requires an authorization
absent from the actual dispatch. The only divergence — contract §7/§9
persistence (entrypoint/manifest/commit/push) — is explicitly reserved by the
dispatch to the parent phases (see §1 above); recorded as the dispatch
instruction scope. No invention, no bypass.

## 6. Tool identities (measured before science)

| Tool | Version (measured) | Role |
|---|---|---|
| GNU objdump (WSL2 Debian 13, kernel 6.18.33.2-microsoft-standard-WSL2) | `GNU objdump (GNU Binutils for Debian) 2.44` | The ONLY disassembler; bounded raw-binary decode of the 28-byte fixtures (`-D -b binary -m i386 -M intel --adjust-vma=0x528e76`) |
| Python (WSL2) | `Python 3.13.5` | Runs `03_SCRIPTS/run_stack_controls.py` with `-B` (no bytecode residue); pure stdlib |
| Windows host | `WinDev2407Eval` (PowerShell invocations; `wsl -e` bridge) | Executor host |

## 7. Temp directory (task-owned, OUTSIDE Git)

```text
C:\Users\User\AppData\Local\Temp\opencode\PE_935_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009\
  (WSL view: /mnt/c/Users/User/AppData/Local/Temp/opencode/PE_935_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009/)
```

Purpose: the bounded extracted baseline window and the five synthetic mutant
copies (disassembler inputs ONLY). Identities of every temp fixture are
recorded in `CONTROLS_RESULTS.json` (per-fixture size/SHA256 + byte deltas).
All raw tool outputs are captured into this package (baseline ->
`01_EVIDENCE/CALLSITE_DISASSEMBLY.txt`; all six fixtures ->
`CONTROLS_RESULTS.json`). Only files created by this run in that directory are
removed at the end; nothing from the temp directory is ever staged.

## 8. Preflight verdict

**PASS** — contract identity MATCH; git triple MATCH; tracked tree clean;
OUTPUT_ROOT absent (created only after this verdict); all four required repo
inputs MATCH; AUDIT_ENTRYPOINT + governance read and recorded; EXE identity
MATCH; tools available. Science phase (window re-pin, objdump disassembly,
symbolic ledger, six-case controls) authorized to proceed under the §3 budget.
