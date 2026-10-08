# INPUT_IDENTITIES — PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008

Written at preflight, BEFORE any science work (contract §2; microrun R2 §3).
Every identity below was physically measured by this executor from the disk
files at preflight time (2026-10-08T11:04–11:05Z, UTC timestamps recorded per
query). None were substituted from memory. Any mismatch would have been
BLOCKED_INPUT_IDENTITY + HARD STOP (none occurred).

## 0. Dispatch contract identity (read FIRST, in full, before anything else)

| field | value |
|---|---|
| contract file | C:\Users\User\Documents\ChatGPT\PE\PE_FUN006C9700_PLUS4_MICRORUN_PROMPT_R2_20261008\OPENCODE_FUN006C9700_PLUS4_MICRORUN_R2.md |
| pinned SIZE | 17487 bytes |
| pinned SHA256 | A6ABFE5E155F3FBAECDCC52E9D9A5E2B18D4286E67192C1C6717B3899EA2B20C |
| measured SIZE | 17487 bytes — MATCH |
| measured SHA256 | A6ABFE5E155F3FBAECDCC52E9D9A5E2B18D4286E67192C1C6717B3899EA2B20C — MATCH |
| result | CONTRACT_IDENTITY = PASS (no BLOCKED_INPUT_IDENTITY) |

The contract was read IN FULL (336 lines, §1–§9) from disk before preflight.

## 1. Git identity (STEP 0, fail-closed; measured with UTC timestamps)

| query | UTC | result |
|---|---|---|
| `git rev-parse HEAD` (LOCAL_HEAD) | 2026-10-08T11:04:41Z | 97823c6180b0a35a8f5c43e45c29076d48208bee |
| `git rev-parse origin/master` | 2026-10-08T11:04:41Z | 97823c6180b0a35a8f5c43e45c29076d48208bee |
| `git ls-remote origin master` attempt 1 | 2026-10-08T11:04:41Z | TRANSIENT FAILURE: `fatal: 'origin' does not appear to be a git repository / Could not read from remote repository` (recorded verbatim; NOT accepted as evidence of anything but the failure itself) |
| remote config check `git remote -v` | 2026-10-08T11:04:45Z | origin = https://github.com/SebastianKozlo/eudoria-clean.git (fetch+push) — correctly configured |
| `git ls-remote origin master` retry (GIT_TERMINAL_PROMPT=0) | 2026-10-08T11:04:49Z | `97823c6180b0a35a8f5c43e45c29076d48208bee refs/heads/master`, exit 0, HTTP 200 via 140.82.121.3:443 (GitHub-Babel/3.0; connection trace observed) |
| EXPECTED_BASE_SHA | — | 97823c6180b0a35a8f5c43e45c29076d48208bee |

**GIT_IDENTITY = PASS** — LOCAL_HEAD == origin/master == live remote master ==
EXPECTED_BASE_SHA (all four equal; the first ls-remote failure was transient
and the LIVE retry answered with the pinned SHA — remote AVAILABLE). No
BLOCKED_EXTERNAL. Branch = master. No rebase/adaptation/force-push performed.

## 2. Working-tree / target-path state at preflight

- `git status --porcelain=v1` at 2026-10-08T11:04Z: ZERO tracked changes
  (no M/A/D lines); foreign untracked census (6, left untouched — see
  SOURCE_STATE.md §2): docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/,
  docs/audits/PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003/,
  docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/,
  docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/,
  docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/,
  experiments/.
- OUTPUT_REPO_PATH (docs/audits/PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_
  20261008/) DID NOT EXIST at preflight (Test-Path = False) — collision check
  PASS. Created only AFTER all preflight gates passed.

## 3. Pinned physical inputs (re-verified by this executor; all MATCH)

| input | pinned SIZE / SHA256 | measured SIZE / SHA256 | verdict |
|---|---|---|---|
| NC2_NC3_DESKTOP_REPORT = C:\Users\User\Documents\ChatGPT\PE\PE_935_NC2_NC3_DESKTOP_POST_AUDIT_97823C6_20261008\REPORT.md | 12398 B / 4F852620BBDE4ECA63504ADE56B4B6BC6A74DD761DB94FA57C11F5FA5502487E | 12398 B / 4F852620BBDE4ECA63504ADE56B4B6BC6A74DD761DB94FA57C11F5FA5502487E | MATCH |
| ENGINE_RESEARCH_REPORT = C:\Users\User\Documents\ChatGPT\PE\PE_FUN006C9700_PLUS4_ENGINE_RESEARCH_20261008\REPORT.md | 19290 B / 87375E0669138E410D7B60FEF625822A8A61A401CAED19513BF46FE235E3DEA1 | 19290 B / 87375E0669138E410D7B60FEF625822A8A61A401CAED19513BF46FE235E3DEA1 | MATCH |
| EXE_PATH = D:\Eudoria_Reconstruction\pcg_install\Entropia.exe | 8015872 B / E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 | 8015872 B / E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 | MATCH |

Both reports were READ IN FULL before science (REPORT 1: 138 lines — the
Desktop post-audit of the NC2/NC3 decoder correction, verdict
ACCEPTED_IN_EXAMINED_CORRECTION_SCOPE_WITH_P3_BACKLOG, 3xP3 backlog items
P3-1/P3-2/P3-3 to preserve as backlog, no new EXE proof; REPORT 2: 196 lines —
the independent comparative engine research by Codex Desktop,
COMPARATIVE_RESEARCH=COMPLETED, NEW_EXE_ACCESS=NO, R/T/W roles defined, the
W-later correction, SDK-generation differences, three-name-lookup mechanisms,
OpenMW counterexamples, hypotheses table — research/oracle only, no PCG proof).
Neither was copied into the repo. The three P3 items remain backlog (not fixed
by this run — no correction mandate here).

EXE role: the ONLY byte source for all new decodes of this run; era label:
PCG 9.3.5 client image (Entropia Universe 9.3.5 — the current era contract's
reconstruction corpus). Every new read/decode is tied to this identity; the
fail-closed reader asserts size+SHA256 at import (§5).

## 4. Historical READ_ONLY source packages (contract §2 item 4)

All five packages EXIST at BASE 97823c6. Per-file identity vs BASE: for ALL
263 physical files across the five packages, `git hash-object <physical file>`
== the `git ls-tree BASE <path>` blob SHA-1 (263/263 IDENTICAL, zero mismatch,
measured 2026-10-08T11:04Z). Census (physical file counts): CHILD_ROOT_
PROVENANCE_R1_20261007 = 38; CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007 = 27;
CHILD_ROOT_NC1_SIB_DECODER_POST_AUDIT_CORRECTION_R1_20261007 = 14;
CHILD_ROOT_NC2_NC3_DECODER_CORRECTION_R1_20261008 = 14;
PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z = 170.

Files READ IN FULL by this executor from those packages (record; the full
per-file identity census is §4 above):

- PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007/: INPUT_IDENTITIES.md,
  PREREGISTRATION.md, FINAL_REPORT.md, HANDOFF.md, POINTER_LINEAGE.csv,
  01_RAW/PINS_AND_REL32.txt, 01_RAW/FUN_006C6F60_PRODUCER_DECODE.txt,
  01_RAW/FUN_006C6780_INSTALLER_PARTIAL.txt, 01_RAW/VTABLE_RTTI_STRINGS.txt.
- PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007/: FINAL_REPORT.md,
  HANDOFF.md, SUPERSESSION.md, CORRECTED_LINEAGE_STATUS.md.
- PE_935_CAND4_CHILD_ROOT_NC1_SIB_DECODER_POST_AUDIT_CORRECTION_R1_20261007/:
  FINAL_REPORT.md, HANDOFF.md, SOURCE_STATE.md.
- PE_935_CAND4_CHILD_ROOT_NC2_NC3_DECODER_CORRECTION_R1_20261008/:
  FINAL_REPORT.md, HANDOFF.md, SOURCE_STATE.md, SUPERSESSION.md,
  INPUT_IDENTITIES.md.
- PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z/:
  02_ANALYSIS/TRACE_EDGE_BLOCKS.md (E5 — the FUN_006CB6F0 instance-creator
  record) + the L20_instcreator_006cb6f0 instruction window of
  01_RAW/C9_LISTING_WINDOWS.json (read in full at the cited lines).
- AUDIT_ENTRYPOINT.md (repo root): the five relevant RUN rows read
  (CHILD_ROOT_PROVENANCE, POST_AUDIT_CORRECTION, NC1_SIB, NC2_NC3,
  PLACEMENT_RECORD_BRIDGE).

Not re-read in full (recorded honestly): the remaining HANDOFF/INPUT_IDENTITIES
of the POST_AUDIT and NC1 packages and the bulk QC/matrix JSONs — their
load-bearing content is carried by the FINAL_REPORTs, SUPERSESSION files,
SOURCE_STATE files, the AUDIT_ENTRYPOINT rows and the two pinned reports read
in full above; this run does not depend on any un-read row. The supersession
state (SN-1..SN-3, S-1..S-9) and preserved-science lists were read and are
honored (no status changes by analogy anywhere in this run).

## 5. Decoder identity (the existing mature decoder; measured, not installed)

- Python: 3.12.10 (C:\Users\User\AppData\Local\Programs\Python\Python312),
  CPython; `python -B` used for every script (no __pycache__/.pyc in the
  package — verified at end of run).
- Disassembler: capstone 5.0.7 Python binding — the EXISTING install reused
  from the prior run's scratch
  C:\Users\User\AppData\Local\Temp\opencode\PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007\capstone_lib
  (nothing installed by this run). Measured identity:
  - capstone\__init__.py = 43,729 B / SHA256 0417AE554252BE8E8D03E328054FAD4C3CEC6CF4895DEECEC637078380840F8B
  - capstone\lib\capstone.dll = 7,572,480 B / SHA256 46B7C385EFE50DB4DEF8AA99AA351C44EA28B1F3C2CCBC4CA41DBB2A02340E39
  Both equal the prior provenance run's INPUT_IDENTITIES.md §4 pins (same
  physical install; identity re-measured this run). cs_version() measured at
  use: (5, 0, 1280). Decode mode: CS_ARCH_X86, CS_MODE_32.
- Fail-closed PE reader: pe_reader.py from the same scratch (2,320 B /
  SHA256 BF7B9C1F65B4645549041C46CCF85815B6CCE29E31EB15B1F417D0D5753866D5) —
  asserts the pinned EXE size+SHA256 at import; own PE32 section mapping
  (VA→file offset); all byte reads of this run go through it or through this
  run's own equivalent mapping re-derivation (03_SCRIPTS/checker_plus4.py
  re-implements the mapping independently for the checker — two
  implementations, one physical source).
- Cross-implementation discipline: rel32 targets are recomputed by this run's
  own arithmetic (call_va + 5 + int32(rel32)); capstone's annotation and the
  own arithmetic must agree for every load-bearing pin. Key instructions are
  additionally cross-checked by MANUAL x86 encoding review recorded in
  01_RAW/MANUAL_ENCODING_CROSSCHECK.txt. Disagreement/unsupported form/
  uncertain boundary = UNVERIFIED, no promotion (contract §5).
- The CTRL_4 exact-endpoint checkers (ctrl4_exact_endpoint_nc23fixed.py /
  qc_ind_ctrl_nc23_own.py lineage) are NOT used as a general decoder and NOT
  extended (contract §6): their opcode universe and fail-closed rejection
  discipline hold WITHIN THE TESTED SCOPE only (8-case matrix + 9-case SIB
  battery + 144-form sweep; NOT GENERAL_X86_DECODER_PROVEN).

## 6. Scratch (outside the repo; registered; not published)

SCRATCH_DIR = C:\Users\User\AppData\Local\Temp\opencode\PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008
Contains this run's private analysis helper scripts and intermediate outputs;
inventoried at end of run; not part of the package or manifest. The prior
provenance scratch (§5) is also read for tooling reuse.

## 7. Preflight verdict

| gate | result |
|---|---|
| contract identity (SIZE+SHA256) | PASS |
| LOCAL_HEAD == EXPECTED_BASE_SHA | PASS |
| origin/master == EXPECTED_BASE_SHA | PASS |
| live remote master == EXPECTED_BASE_SHA (available; transient first-attempt failure disclosed; live retry answered pinned SHA) | PASS |
| tracked changes | NONE |
| OUTPUT_REPO_PATH absent before run | PASS |
| foreign untracked census recorded, untouched | PASS (6 paths) |
| NC2_NC3_DESKTOP_REPORT identity | PASS (MATCH) |
| ENGINE_RESEARCH_REPORT identity | PASS (MATCH) |
| EXE identity | PASS (MATCH) |
| historical packages per-file identity vs BASE | PASS (263/263) |

**PREFLIGHT = PASS — OUTPUT_REPO_PATH created only after all gates passed.**
No BLOCKED_INPUT_IDENTITY / BLOCKED_BASE_MISMATCH / BLOCKED_EXTERNAL / collision.
No gate weakened.
