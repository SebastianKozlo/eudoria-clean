# INPUT_IDENTITIES — PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007

Written at preflight, BEFORE any science work (contract §1). Every SHA256 below
was measured by this executor from the physical files at preflight time
(2026-10-07T10:54–11:01Z). All identities MATCHED their dispatch-pinned values;
none were substituted from memory; any mismatch would have been BLOCKED + HARD STOP
(none occurred).

## 1. Primary binary (THE pinned static analysis target)

| input | size_bytes | SHA256 |
|---|---|---|
| D:\Eudoria_Reconstruction\pcg_install\Entropia.exe | 8,015,872 | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 |

Re-verified at preflight and fail-closed inside every analysis tool of this run
(the reader module asserts size+SHA256 at import; every decode reads through it).
Role: the ONLY byte source for all new decodes of this run. Era label: PCG 9.3.5
client image (the reconstruction corpus pinned by the current era contract).

## 2. Contract (the instruction set of this run)

| input | size_bytes | SHA256 |
|---|---|---|
| C:\Users\User\Documents\ChatGPT\PE\PE_935_CAND4_CHILD_ROOT_PROMPT_REVIEW_20261007\OPENCODE_CAND4_CHILD_ROOT_REVIEWED.md | 18,159 | 57249511611ADFA68161D9F2363DCB9831BFF36C9C913B59C83251B5D8C17568 |

Dispatch-pinned identity: 18,159 B / 57249511…D8C17568 — MATCH. Read in full
(375 lines, §1–§12) from disk before any work.

## 3. Prior evidence packages (READ-ONLY; read at the exact BASE d65fa12e)

Identity of each item = (BASE_SHA, repo_path); physical copies verified
git-blob-identical to the BASE blobs BEFORE any work (49/49 and 27/27 blob
identity match, zero mismatches — measured at preflight, see
GOVERNANCE_DECISION.md §4).

- docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/
  — 49 files; aggregate SHA256 (sorted "path sha256" digest lines) =
  AB21CBC3991C91B19BD884F851E0FE24F1EBA251B48E24643A71F6169BE65B5B.
  Used records: FINAL_REPORT.md, CLAIM_MATRIX.csv, CANDIDATE_LEDGER.csv (the
  CAND-4 row), FUNCTION_BUDGET.csv, QC_REPORT.md (S2/S3/S4/S8 pin lists),
  PRE_REGISTERED_ANCHORS.md (PA1–PA4/CH1–CH3 prior pins), 01_RAW/
  FUN_0050A310_DECODE.txt (the CAND-4 join window), 01_RAW/
  FUN_006A3930_CHAIN_REPIN.txt (the manager-creation chain), HANDOFF.md
  (NOT_CHECKED list).
- docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007/
  — 27 files; aggregate SHA256 =
  80AB81F5E3F6686D1CA13CDF89EDB119793D8C661B853E741B569EB8AE21A164.
  Used records: FINAL_REPORT.md, SUPERSESSION.md, CORRECTED_STATUS_ALGEBRA.md
  (the ACTIVE corrected statuses incl. the J1/J2/J3 supersessions),
  EDGE_BUDGET_RECONSTRUCTION.csv (the 83-row census; the historical minimum-22
  convention of the SOURCE run), HANDOFF.md, GOVERNANCE_DECISION.md,
  INPUT_IDENTITIES.md.
- Supersession compliance (J1–J3), carried into this run's ACTIVE statuses:
  the historical qualification gate is NOT a positive semantic qualifier
  (REAL_SCIENCE_AUTO_QUALIFICATION = DISABLED; no SCIENCE_PASS); the source
  run's "6/6 edges exhausted" is superseded (source-run MINIMUM_ANALYZED_EDGE_COUNT
  = 22 distinct pairs, ACTUAL not reported — historical value, not changed by
  this run); the source run's transform CONFIRMED_STATIC is
  NOT_QUALIFIED_BY_ORIGINAL_SCOPE (no transform semantics of any kind are used
  by this run). The old gate is NOT used as a positive qualifier anywhere.

## 4. Decoder identity (the x86 disassembler of this run — explicit, contract §4)

- Package: capstone, version 5.0.7 (Python binding; PyPI wheel
  capstone-5.0.7-py3-none-win_amd64.whl), installed by this executor via
  `python -m pip install --target <scratch>\capstone_lib capstone==5.0.7`
  (internet-fetched at 2026-10-07T10:57Z; the empty leftover
  C:\Users\User\AppData\Local\Temp\opencode\capstone_lib directory tree from the
  earlier run contains NO module files and is NOT used — namespace-package
  contamination was detected at preflight and avoided).
- cs_version(): (5, 0, 1280) — measured at use.
- Module path: <scratch>\capstone_lib\capstone\__init__.py,
  SHA256 0417AE554252BE8E8D03E328054FAD4C3CEC6CF4895DEECEC637078380840F8B (43,729 B).
- Native engine: <scratch>\capstone_lib\capstone\lib\capstone.dll,
  7,572,480 B, SHA256 46B7C385EFE50DB4DEF8AA99AA351C44EA28B1F3C2CCBC4CA41DBB2A02340E39.
- Decode mode: CS_ARCH_X86, CS_MODE_32. Rel32 call targets are recomputed by this
  run's own arithmetic (call_va + 5 + int32(rel32)) independently of capstone's
  annotation; the two implementations must agree for every load-bearing pin.
- The prior source run recorded "capstone 5.0.7" in INPUT_IDENTITIES.md §1; this
  run re-measures the identity itself (above) rather than inheriting the label.
- Python: 3.12.10 (C:\Users\User\AppData\Local\Programs\Python\Python312),
  CPython; helper scripts of this run use only the stdlib + capstone.

## 5. Oracle sources (contract §10 — only as mechanism helpers)

| file | size_bytes | SHA256 (re-measured this run) | availability |
|---|---|---|---|
| D:\gamebyroengine\extracted\Gb12_Source\CoreLibs\NiMain\NiNode.cpp | 33,897 | 38C7A1DE1E166345068D296F70F34B1ADAE27C694E19EAD8FA0FBD8B62E0E016 | available |
| D:\gamebyroengine\extracted\Gb12_Source\CoreLibs\NiMain\NiAVObject.cpp | 33,215 | 72E0837149B03CCDA171BDF5E68E1E1F8C2712B2F10E7957AC3EC26344CA5EA7 | available |

Both Gb12 files were re-measured by this executor at preflight (2026-10-07T10:58Z,
re-measured again at 11:02Z after a transcription error was caught in the draft
of this section — the values in the table above are the measured 64-hex strings,
matching the identities pinned by the prior source run's INPUT_IDENTITIES.md §5,
whose oracle-fingerprint role remains: NON_EXACT_PCG_SOURCE_ORACLE, architectural
fingerprint only; Gb12 is NOT the PCG 9.3.5 build).

Availability ruling for the other §10 oracle mechanisms:
- OpenMW commit 0c6a724f33ffd73de6e60322843eead2a0807c7f (animation.cpp
  setObjectRoot/getModelInstance, scenemanager.cpp cloneNode/getInstance): NOT
  PRESENT on the local disk (searched; no openmw tree exists under D:\ or the
  PE research folder). File identity cannot be measured => this oracle is
  NOT_USED by this run (no borrowed mechanism claims from it).
- Gamebryo 2.6 mirror sigmaco/gamebryo-v2.6 @ 329cd25a38d66ca8a55c7564eabd898358c95ff1
  (NiActorManager.inl/.cpp GetNIFRoot/GetActorRoot/ChangeNIFRoot): NOT PRESENT on
  the local disk as the identity-measurable git mirror (searched; the physical
  D:\gamebyroengine listing contains: 'extracted' (directory; incl. the Gb12_Source tree
  of the §5 Gb12 oracle files), 'Gamebryo 1.1.2 Evaluation' (directory),
  'Gamebryo 1.1.2 Evaluation.zip', 'Gamebryo 1.2 Source.rar', 'GameBryo2.6.7z',
  'gamebryo_1.2.7z', 'Gamebryo_Version_1.1.2_Gamebryo_2004.iso' and 'GB_2.3.iso'.
  The Gamebryo 2.6 material exists locally only as the unextracted
  'GameBryo2.6.7z' archive — an archive is not the git mirror tree; no file
  identity against commit 329cd25 can be measured without extraction, which is
  out of scope for this run). NOT_USED by this run.
Any oracle used is recorded with ORACLE → HYPOTHESIS → PCG BYTE/DATAFLOW PROOF in
the analysis records; an oracle can only support MECHANISM_ANALOGY, never
PCG_CONFIRMED; era/build mismatch stays explicit (Gb12 is NOT the PCG 9.3.5 build).

## 6. Private scratch (outside the repo; registered; not published)

SCRATCH_DIR = C:\Users\User\AppData\Local\Temp\opencode\PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007
Contains this run's private analysis tooling (PE reader with fail-closed EXE
pinning, capstone install, decode helpers, QC scripts) and intermediate outputs.
Inventoried at the end of the run; not part of the package or the manifest.

## 7. Preflight verification record (measured)

- git fetch/rev-parse/ls-remote queries 2026-10-07T10:54:00Z and 2026-10-07T10:54:17Z:
  LOCAL_HEAD = origin/master = actual remote master =
  d65fa12e5bae4e9aab291c3cc7815b1822e41cff == EXPECTED_BASE_SHA. MATCH. No error.
- Tracked changes: NONE. Foreign untracked roots (6): inventoried, untouched
  (list in GOVERNANCE_DECISION.md §4).
- OUTPUT_ROOT absent before run (collision check PASS).
- No other inputs are used by this run. No payloads were opened; no VFS/BNT/NIF
  reads; the three prior private research reports of the source run are NOT
  re-opened by this run (their pinned identities remain those of the source
  run's INPUT_IDENTITIES.md §3; this run relies only on the BASE packages of
  §3 above + the EXE).
