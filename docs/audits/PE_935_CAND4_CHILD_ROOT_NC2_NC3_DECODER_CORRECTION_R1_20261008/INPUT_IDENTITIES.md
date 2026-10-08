# INPUT_IDENTITIES — PE_935_CAND4_CHILD_ROOT_NC2_NC3_DECODER_CORRECTION_R1_20261008

RUN_ID: PE_935_CAND4_CHILD_ROOT_NC2_NC3_DECODER_CORRECTION_R1_20261008
RUN_CLASS: RECORDS_AND_QC_MACHINERY_CORRECTION
Executor: pe-reconstruction (bounded worker phase under direct PE-MASTER dispatch;
the QC phase, publication/manifest and commit/push belong to the parent, NOT this run).
All queries below were measured independently by this executor (never trusted from chat text).
Verdict language: MATCH = physically measured bytes equal the pinned identity.

---

## 0. Dispatch contract identity (read FIRST, in full, before anything else)

| field | value |
|---|---|
| contract file | C:\Users\User\Documents\ChatGPT\PE\PE_935_NC2_NC3_CORRECTION_PROMPT_20261008\OPENCODE_NC2_NC3_CORRECTION.md |
| pinned SIZE | 14069 bytes |
| pinned SHA256 | 3E0BDB58A0CDC1488DE9477A855CEC04D712D492E147CC92CDB3C021B5143B8F |
| measured SIZE | 14069 bytes — MATCH |
| measured SHA256 | 3E0BDB58A0CDC1488DE9477A855CEC04D712D492E147CC92CDB3C021B5143B8F — MATCH |
| result | CONTRACT_IDENTITY = PASS (no BLOCKED_INPUT_IDENTITY) |

The contract was read in FULL (321 lines) before preflight. Delegation-scope note: the
dispatch narrows this worker's write scope to exactly six files inside OUTPUT_ROOT
(INPUT_IDENTITIES.md, SOURCE_STATE.md, 03_SCRIPTS/ctrl4_exact_endpoint_nc23fixed.py,
03_SCRIPTS/run_nc23_matrix.py, CONTROL_RESULTS_PRE.json, CONTROL_RESULTS_POST.json);
the contract §5 full package (QC script, QC_RESULTS, QC_REPORT, SUPERSESSION,
FINAL_REPORT, PE_MASTER_REVIEW, HANDOFF, MANIFEST, AUDIT_ENTRYPOINT line, commit/push)
is the parent's phase and was NOT created/touched here.

## 1. Git identity (STEP 0, fail-closed; measured with UTC timestamps)

| query | UTC | result |
|---|---|---|
| `git rev-parse HEAD` (LOCAL_HEAD) | 2026-10-08T07:16:42Z | 91598a9868037c4954e22e16c535d6a5a671771e |
| `git fetch origin` | before 07:16:42Z | exit 0 (no transport error) |
| `git rev-parse origin/master` | 2026-10-08T07:16:43Z | 91598a9868037c4954e22e16c535d6a5a671771e |
| `git ls-remote origin refs/heads/master` (LIVE remote) | 2026-10-08T07:16:43Z | 91598a9868037c4954e22e16c535d6a5a671771e refs/heads/master |
| EXPECTED_BASE_SHA | — | 91598a9868037c4954e22e16c535d6a5a671771e |

**GIT_IDENTITY = PASS** — LOCAL_HEAD == origin/master == live remote master ==
EXPECTED_BASE_SHA (all three equal). Remote was AVAILABLE and answered live; no
BLOCKED_EXTERNAL. Re-confirmed at end of run: HEAD still 91598a98… (2026-10-08T07:20:37Z);
no commit/stage/push performed by this run.

## 2. Desktop inputs (C:\Users\User\Documents\ChatGPT\PE\PE_935_NC1_DESKTOP_POST_AUDIT_91598A98_20261007\)

| file | pinned SIZE / SHA256 | measured SIZE / SHA256 | verdict |
|---|---|---|---|
| REPORT.md | 11570 B / 125C47CA195C5D2F782EA1DBCEA0BA1CA65B973CBABEBABDD4F78963C43E83B4 | 11570 B / 125C47CA195C5D2F782EA1DBCEA0BA1CA65B973CBABEBABDD4F78963C43E83B4 | MATCH |
| CONTROL_COUNTERCHECKS.json | 132471 B / AD8DC2052F714439497A277512944EF729F53BDC94B436CB20EE09FEE6BCC28D | 132471 B / AD8DC2052F714439497A277512944EF729F53BDC94B436CB20EE09FEE6BCC28D | MATCH |
| AUDIT_CHECKS.json | 46417 B / 593B03C3AB87FD274BE8C02E7196D60A961975C95631278C97A8271E528862B7 | 46417 B / 593B03C3AB87FD274BE8C02E7196D60A961975C95631278C97A8271E528862B7 | MATCH |

Measured at ~2026-10-08T07:15Z (Get-FileHash SHA256, independent PowerShell measurement).
**DESKTOP_INPUTS = PASS (3/3).** All Desktop files were opened READ-ONLY.
CONTROL_COUNTERCHECKS.json is the SOURCE_DESKTOP_MEASUREMENT citation source
(residual_tests: NON_SIB_TEST_HIDDEN_EDI, INVALID_FF_FAR_CALL_REGISTER,
INVALID_LEA_REGISTER — transcribed VERBATIM into CONTROL_RESULTS_PRE.json with this
cited path+size+SHA256; equality with the source JSON verified programmatically 3/3).

## 3. Repo inputs — disk AND committed-blob equality at EXPECTED_BASE_SHA

Method (recorded per dispatch STEP 0): HEAD == EXPECTED_BASE_SHA and `git status
--porcelain=v1` shows NO tracked changes for these paths (working tree clean ⇒ worktree
== index == HEAD content), PLUS the physical disk SHA256 equals the pin, PLUS the
committed blob itself was extracted byte-exact (no transcoding: `cmd /c "git cat-file
blob <blob-sha1> > tempfile"`, then SHA256 of the extracted file) into the approved
temp area and its SHA256 equals the pin. Git blob SHA-1s additionally recorded.

| repo input (repo-relative) | pinned SIZE / SHA256 | disk measurement | committed blob | verdict |
|---|---|---|---|---|
| SOURCE_PACKAGE 03_SCRIPTS/ctrl4_exact_endpoint_sibfixed.py (under docs/audits/PE_935_CAND4_CHILD_ROOT_NC1_SIB_DECODER_POST_AUDIT_CORRECTION_R1_20261007/) | 17740 B / 44155437F20FA6DA9D6847A236F708C7F2A40F26BABE71424B21C325B4FB4405 | 17740 B / 44155437F20FA6DA9D6847A236F708C7F2A40F26BABE71424B21C325B4FB4405 — MATCH | blob 48485dca0b90bc75cdbbd01621fca269462f6ef7; extracted SHA256 = pin — MATCH | PASS |
| SOURCE_PACKAGE 00_CONTROL_INTERNAL_QC/qc_ind_ctrl_sib_own.py (same package) | 51943 B / 529B61DB312AEC338221425B12F2D94DE2BE351B5C62F68DDBA6BF915B007B25 | 51943 B / 529B61DB312AEC338221425B12F2D94DE2BE351B5C62F68DDBA6BF915B007B25 — MATCH | blob 6fd3d14673f72214916c245ee7575e50aa026d78; extracted SHA256 = pin — MATCH | PASS |
| PRIOR_SCIENCE_PACKAGE 01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt (under docs/audits/PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007/) | 4043 B / A0DEFAA16D6934FC307BD88210BCCA59B823C58FB57319A2C090F9ED59AD01E3 | 4043 B / A0DEFAA16D6934FC307BD88210BCCA59B823C58FB57319A2C090F9ED59AD01E3 — MATCH | blob 6836b8935e442f4f864a3d843a8bab47602fa75f; extracted SHA256 = pin — MATCH | PASS |

**REPO_INPUTS = PASS (3/3, disk + committed-blob equality).**

Re-verification AFTER the run (source packages untouched): all three files re-measured
2026-10-08T07:20Z with byte-identical SIZE/SHA256 to the pins (see SOURCE_STATE.md §4).
Additionally verified the PRIOR_CORRECTION_PACKAGE input
docs/audits/PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007/03_SCRIPTS/
ctrl4_exact_endpoint.py (20592 B / FDB5F16E6F9A6352030DD2F4D9523E1CAA0AB924F2112DDEC787CC7B3A84A330)
— unchanged (it is the grandparent checker, cited in the new module's docstring lineage).

## 4. In-run re-measurement (self-contained evidence)

03_SCRIPTS/run_nc23_matrix.py re-measures ALL seven pinned identities (contract + 3
Desktop + 3 repo) at execution time and fails closed on any mismatch; the per-input
measurements are persisted in BOTH CONTROL_RESULTS_PRE.json and
CONTROL_RESULTS_POST.json under `input_identities_remeasured_at_run_time` —
result: ALL MATCH.

## 5. Preflight verdict

| gate | result |
|---|---|
| contract identity (SIZE+SHA256) | PASS |
| LOCAL_HEAD == EXPECTED_BASE_SHA | PASS |
| origin/master == EXPECTED_BASE_SHA | PASS |
| live remote master == EXPECTED_BASE_SHA (available, measured live) | PASS |
| Desktop inputs 3/3 | PASS |
| repo inputs disk 3/3 + committed-blob 3/3 | PASS |
| OUTPUT_ROOT did not exist (Test-Path False, 2026-10-08T07:16Z) | PASS |
| git status: no tracked changes | PASS |
| foreign untracked census recorded WITHOUT touching | PASS (see SOURCE_STATE.md §3) |

**PREFLIGHT = PASS — OUTPUT_ROOT created only after all gates passed.**
No BLOCKED_INPUT_IDENTITY / BLOCKED_EXTERNAL / collision. No gate weakened.

## 6. Opcode universe of the corrected production decoder (successor documentation)

Unchanged from sibfixed plus the two new rejections: 8B/89/8D (mov reg,r/m | mov r/m,reg |
lea) with NC1 SIB guard + NC3-B LEA mod=11 rejection; 84 (test r/m8, r8) with NC1 guard +
NC2 all-memory-form rejection (register form only); 74/EB (je/jmp rel8); 83 (grp1 imm8,
mod=01/11 only, P3 imm@opcode+3 fix kept); 6A (push imm8); 50-57 (push r32); 58-5F
(pop r32); BF (mov edi, imm32); E8 (call rel32); FF (grp5, ONLY /2 mod=11 call r/m32 —
FF D2 endpoint; everything else raises); 90 (nop); every other opcode raises
ValueError. Fail-closed: bytes never skipped, decode never continues past a rejected
form; checker catches ONLY (ValueError, IndexError) — unexpected exceptions propagate
(recorded as ERROR, never as an expected FAIL).
