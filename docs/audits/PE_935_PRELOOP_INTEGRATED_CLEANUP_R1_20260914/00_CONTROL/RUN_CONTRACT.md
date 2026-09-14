# RUN CONTRACT — PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914

Executor: **pe-reconstruction** (direct PE-MASTER dispatch; NO_NESTED_TASKS).
You see ONLY this contract plus the two sibling control files in this package
(`00_CONTROL/SOURCE_IDENTITIES.json`, `00_CONTROL/GIT_OBSERVATIONS_AT_FORMALIZE.md`).
Every expected value cited here is a FAIL-CLOSED pin: you RE-DERIVE it from the physical
sources in-run (L22 discipline) and assert pin == re-derived. A pin mismatch is a
HARD_STOP, never a silent pass.

---

## A. IDENTITY

- RUN_ID: `PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914`
- RUN_CLASS: MATERIAL (canonical closed namespace)
- RUN_TYPE: PROCESS / PERSISTENCE / REVALIDATION
- MILESTONE: EU935-M1
- ERA: PCG_9_3_5
- MODE: **STATIC-ONLY** — the client binary is NEVER executed; no game/oracle binary is
  ever executed. All analysis is own byte-read + own disassembly of the pinned EXE file.
- EXECUTOR: pe-reconstruction, direct PE-MASTER dispatch, NO_NESTED_TASKS.
- PARENT LOOP: `2ed038db-5d2e-4e7e-b679-2d29bf57501a` (4h auto loop, human-authorized
  2026-09-14). Phase 1 = THIS cleanup run. Phase 2 (science RE) starts only AFTER this
  cleanup is ACCEPTED. No milestone closure, no next milestone in this run.
- PUBLICATION: a SEPARATE LATER STEP performed by pe-master-auditor AFTER PE-MASTER
  adjudication. The executor performs **ZERO git mutations** (no add/commit/push/stage/
  branch/checkout/config). All executor outputs are new untracked files under this
  package directory only.
- PURPOSE / CONTEXT: the human authorized a canonical cleanup that (a) revalidates the
  two LINK30 census rows rejected under the unsound R-EBP-INHERITED rule, (b) verifies
  and dispositions the seven SLOT17 audit findings plus the GB12 prose-table erratum and
  the NiRTTI precision disposition, (c) records the F5 HOLD, and (d) reconciles the writer
  census counts with TOTAL=3643 — so that the historical SLOT17 package
  (branch `audit/pe935-ninode-slot17-gb-oracle-minicheck-r1`, tip
  `5290e79e0dc469c70605f35c125d7b727f9f7a6b`) can be integrated verbatim via a future
  cherry-pick of 5290e79 onto current master (performed by the persistence worker AFTER
  PE-MASTER adjudication — NOT in this run).

---

## B. PINNED IDENTITIES (FAIL-CLOSED)

All pins below were verified by the formalizer from disk/git at AT_FORMALIZE
(2026-09-14 15:49-15:51 -07:00); the recorded measurements live in
`00_CONTROL/SOURCE_IDENTITIES.json` and `00_CONTROL/GIT_OBSERVATIONS_AT_FORMALIZE.md`.
The executor re-verifies ALL of them at run start (G0/G1/G2).

1. **Primary binary — Entropia.exe**
   - Path: `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe`
   - Expected SIZE: 8015872 bytes; expected SHA256:
     `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31`
   - Format PE32 i386, ImageBase 0x00400000.
   - EVERY probe of this binary fails closed on SHA256+SIZE BEFORE any byte is read.
   - The binary is NEVER executed.

2. **Repo / BASE_SHA**
   - Repo: `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean`, branch `master`.
   - BASE_SHA (pin): `a7a6c756bc35a5b28220236e9ac649131206aeb3`.
   - At executor start, assert HEAD == BASE_SHA. If HEAD differs: G0 FAIL, HARD_STOP
     (do not proceed; report the observed HEAD).
   - Expected untracked set AT_CLEANUP_START (exactly three entries, nothing else,
     0 modified, 0 staged):
     1. `docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/`
     2. `experiments/`
     3. `docs/audits/PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914/` (this package)
   - Local `origin/master` ref and live `git ls-remote origin master` are both expected
     == BASE_SHA (AT_FORMALIZE both matched). Record your own observation at
     AT_CLEANUP_START; a live-remote mismatch is a finding to report, not silently passed.

3. **SLOT17 branch (HISTORICAL COMPLETED RUN — never force-push, never rewrite, never
   delete)**
   - Ref: `audit/pe935-ninode-slot17-gb-oracle-minicheck-r1`
   - Pinned tip: `5290e79e0dc469c70605f35c125d7b727f9f7a6b` — verify with
     `git rev-parse audit/pe935-ninode-slot17-gb-oracle-minicheck-r1` AND
     `git ls-remote origin audit/pe935-ninode-slot17-gb-oracle-minicheck-r1`
     (AT_FORMALIZE both returned the pinned tip).
   - Pinned parent: `3644e5ac9cbf7b5445861e7f5342fb8642741346` — verify with
     `git rev-parse 5290e79e0dc469c70605f35c125d7b727f9f7a6b^`.
   - Worktree: `D:\Eudoria_Reconstruction\worktrees\PE_935_NINODE_SLOT17_GB_ORACLE_MINICHECK_R1`
     (expected clean; HEAD == tip).
   - Package (READ-ONLY for you):
     `docs/audits/PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914/` inside
     that worktree — 35 files (00_CONTROL 6, 01_RAW 3, 02_ANALYSIS 6, 03_EVIDENCE 16,
     06_REPORT 4; formalizer disk census == this pin).

4. **LINK30 historical artifacts (READ-ONLY)**
   - `docs/audits/PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914/02_ANALYSIS/SF30_WRITER_CENSUS.csv`
     — expected SHA256 `71552E2A4BFC120DA0BE1A7E108A41A03C873ADDD238637DD7C18F3C968824D0`,
     352206 bytes (AT_FORMALIZE: match).
   - `docs/audits/PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914/01_RAW/SF30_WRITER_RAW.txt`
     — expected SHA256 `64402A73013B52943E10AE17BB115F466A0D3BEF98AA3835915CF3C1CD572248`,
     2492537 bytes (AT_FORMALIZE: match).
   - Byte-identical before == after is asserted (G9/G11). NEVER regenerate them.

5. **GB112 oracle**
   - NiMain.lib pin:
     `D:\gamebyroengine\Gamebryo 1.1.2 Evaluation\SDK\Win32\Lib\VC71\ReleaseLib\NiMain.lib`,
     expected size 3073590, SHA256
     `FF4519AFD2475D9A6E71A35E5DB6B0F5A0B7E9E86EC3662C6A340DA19BA06597`
     (AT_FORMALIZE: match). Never executed; static COFF parsing only if needed.
   - `D:\gamebyroengine\extracted\Gb112_eval\` exists; one-level census (AT_FORMALIZE):
     `Documentation` directory ONLY (documentation-installer material inside — see
     SOURCE_IDENTITIES.json for the 5-entry Documentation census). NOT the full SDK,
     NOT the source of NiMain.lib.

6. **FIRSTCALL unauthorized package (READ + HASH ONLY)**
   - `docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/` — process status
     PARKED_UNAUTHORIZED_ATTEMPT (human OPTION C; see W7).
   - Formalizer census (AUTHORITATIVE for your unchanged-assertion): **7 files total**
     (6 content files + 1 `.pyc`) plus 3 EMPTY directories (02_ANALYSIS, 03_EVIDENCE,
     06_REPORT). NOTE: the parent's phrasing "7 content files + the .pyc" does not match
     disk — disk truth is 6 content + 1 pyc = 7; the 7 hashes recorded in
     SOURCE_IDENTITIES.json are the pins. You re-hash all 7 and assert unchanged (G10).
   - Never staged/committed/deleted/modified. NOT an evidence source.

7. **Canonical census layer (baseline for W4)**
   - 3643 = 2 PROVEN / 619 POSSIBLE / 3022 REJECTED / 0 UNRESOLVED
     (LINK30 AMEND_R2, commit a7a6c756). TOTAL == 3643 is a hard invariant.

8. **Toolchain**
   - Interpreter: `D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe`
     (Python 3.12.7 measured). All scripts run with `-B`; no `__pycache__` anywhere in
     this package.
   - Capstone: available BOTH in the interpreter's own site-packages AND in
     `C:\Users\User\AppData\Local\Temp\opencode\capstone_lib`; BOTH copies measure
     `capstone.__version__ == 5.0.7` (AT_FORMALIZE). The capstone_lib dist-info label
     `capstone-5.0.9.dist-info` is a KNOWN FALSE LABEL — cite the MEASURED version,
     never the label. EMPIRICAL PROVENANCE NOTE (formalizer probe): setting
     `PYTHONPATH=...\capstone_lib` before invoking this interpreter did NOT add it to
     sys.path; `import capstone` resolved to the interpreter's own site-packages copy.
     If you need the capstone_lib copy specifically, use
     `sys.path.insert(0, r'C:\Users\User\AppData\Local\Temp\opencode\capstone_lib')`
     explicitly. In EVERY script header record the dynamically measured
     `capstone.__version__` AND `capstone.__file__` — never a hand-typed provenance.

---

## C. THE ONE PRIMARY QUESTION

Is the canonical state correctly reconciled —

(a) the two LINK30 census rows rejected under the unsound R-EBP-INHERITED rule (E1/E2)
    revalidated under the corrected rule (W1/W2/W3/W4),
(b) the SLOT17 audit findings AUD-F1..AUD-F7 plus the GB12 prose-table erratum plus the
    NiRTTI precision disposition each verified and dispositioned with the executor's OWN
    evidence (W5/W6),
(c) the F5 HOLD recorded (W7),
(d) the writer census counts reconciled with TOTAL=3643 (W4),

— so the SLOT17 package can be integrated verbatim and the cleanup published?

This is ONE question. The executor does NOT answer it by assertion; every sub-part needs
own from-disk/bytes evidence per W1-W9.

---

## D. WORK ITEMS (execute ALL, in this order)

All output paths below are RELATIVE TO THIS PACKAGE ROOT
(`docs/audits/PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914/`). You create the
subdirectories you need (01_RAW, 02_ANALYSIS, 03_EVIDENCE, 06_REPORT) inside this
package only.

### W1. EBP REVALIDATION E1

Target: LINK30 census row **0x007EB1B3** (function 0x007EAC00, insn
`mov dword ptr [ebp+0x30], esi`, bytes `89 75 30`, historical class REJECTED_ALIAS,
historical reason R-EBP-INHERITED: "fn never redefines ebp (FPO, ebp untouched);
ebp = ancestor frame pointer = stack address").

THE HISTORICAL RULE IS UNSOUND: EBP is callee-saved and may carry arbitrary caller
state. REJECTED_ALIAS may stand ONLY IF proven by one of:

- (A) explicit current-function frame construction (`push ebp; mov ebp,esp`) before the
  writer on every writer-reaching path;
- (B) explicit derivation of EBP from ESP/stack before the writer on every
  writer-reaching path;
- (C) bounded entry/caller provenance proving the incoming EBP is non-SF on every entry
  path (e.g., every reachable caller holds a live standard frame pointer at its call
  site, so incoming EBP is a stack address). NOTE: SF (SceneFeederObject) is always-heap
  per the accepted census — a stack/frame address can never alias SF+0x30.

METHOD: own disassembly from the physical EXE (own PE parse + capstone; fail-closed
SHA256+SIZE pin FIRST). Disassemble FUN_007EAC00 from entry; determine whether EBP is
defined at all (push ebp / mov ebp,esp / lea ebp) anywhere before the writer; locate the
writer VA 0x007EB1B3 and verify the instruction bytes `89 75 30`.

Caller provenance with SEPARATE closures, each with a declared bound:

- DIRECT_CALLER_CLOSURE: full-.text E8 rel32 census of calls targeting 0x007EAC00.
  For each direct caller: does it construct a frame (`push ebp; mov ebp,esp`) and is EBP
  unmodified from prologue to the call site? If yes for ALL direct callers, incoming
  EBP = frame pointer = stack address on all direct paths.
- ADDRESS_TAKEN_CLOSURE: whole-file imm32 0x007EAC00 occurrence census. If ZERO, there
  is no function-pointer/vtable/jump-table channel.
- INDIRECT_ENTRY_CLOSURE: if address-taken > 0, enumerate the takers and bound their
  reachability; declare an explicit bound (e.g., two levels). If the bound is exhausted
  without closure -> UNKNOWN provenance.

RULES: a direct E8 census alone is NOT sufficient if the function can be reached
indirectly. If entry provenance remains open -> the row classification is
**POSSIBLE_ALIAS** (this does NOT mean it IS SF; it means REJECTED is not proven).
Record per-case: which of A/B/C was proven, with VA+bytes for every load-bearing step,
or **NONE_PROVEN**.

Raw output -> `01_RAW/` (e.g., `01_RAW/E1_FUN_007EAC00_DISASM.txt`,
`01_RAW/E1_CALLER_PROVENANCE_CENSUS.txt`).

### W2. EBP REVALIDATION E2

Target: LINK30 census row **0x0082DB61** (function 0x0082DAC0, insn
`mov word ptr [ebp+0x30], cx`, bytes `66 89 4D 30`, historical class REJECTED_ALIAS,
same unsound R-EBP-INHERITED reason). Same method as W1.

NOTE the operand width: a 16-bit write can alias the LOW HALF of a 32-bit pointer field —
the alias analysis is identical (the base register is what matters).

Raw output -> `01_RAW/` (e.g., `01_RAW/E2_FUN_0082DAC0_DISASM.txt`,
`01_RAW/E2_CALLER_PROVENANCE_CENSUS.txt`).

### W3. CLASSIFIER RULE V2 + MANDATORY NEGATIVE TEST

1. Write `02_ANALYSIS/EBP_CLASSIFIER_RULE_V2.md` — the corrected rule for all future
   censuses: "UNKNOWN LIVE-IN EBP -> NEVER structural REJECTED solely because
   untouched; default POSSIBLE_ALIAS unless A/B/C proven" (cases A/B/C exactly as in W1).

2. Implement the rule as a small deterministic checker script under `00_CONTROL/`
   (suggested name `00_CONTROL/ebp_alias_classifier.py`; deterministic, runs with `-B`,
   no pycache output anywhere in this package).

3. EXECUTE the mandatory synthetic negative test. FIXTURE (never claimed to be Entropia
   bytes; clearly labelled **SYNTHETIC_FIXTURE** in the fixture definition, the script
   output, and the evidence record): incoming EBP unknown; function does not redefine
   EBP; a write `[ebp+0x30], reg`.
   EXPECTED classifier output: **POSSIBLE_ALIAS**.
   If the classifier returns REJECTED_ALIAS -> the cleanup FAILS (G8 fails).

4. Also run the POSITIVE CONTROL: a fixture with
   `push ebp; mov ebp,esp; mov [ebp+0x30], eax` -> must classify **REJECTED_ALIAS**
   (sound case A). If it does not, the checker is broken (G8 fails).

5. Record BOTH outputs raw -> `01_RAW/EBP_CLASSIFIER_TEST_OUTPUTS.txt` (both the
   negative and the positive control, verbatim program output).

### W4. CENSUS RECOMPUTATION LAYER

The historical CSV/RAW are READ-ONLY: verify byte-identity against the
SOURCE_IDENTITIES.json pins BEFORE your work and AFTER it; NEVER regenerate them.

Derive the corrected canonical counts from the E1/E2 adjudication:
- START from the canonical layer 3643 = 2 PROVEN / 619 POSSIBLE / 3022 REJECTED /
  0 UNRESOLVED.
- Possible outcomes: 2/619/3022/0 (both rejections stand sound under A/B/C) or
  2/620/3021/0 (one falls to POSSIBLE) or 2/621/3020/0 (both fall).
- **DO NOT HARD-CODE the outcome** — derive it from the W1/W2 evidence.
- The derived counts MUST satisfy TOTAL == 3643 (assert in G9).

Record per changed row: OLD_CLASS, NEW_CLASS, PROOF (the A/B/C case + VAs), STATUS
(e.g. REJECTED_STANDS_SOUND / REJECTED_SUPERSEDED_TO_POSSIBLE), reason superseded.
Rows that do not change are listed as unchanged with their standing class.

Output -> `02_ANALYSIS/CANONICAL_STATE_RECONCILIATION.md`. If the counts change, ALSO
draft — INSIDE that same file, NOT into the LINK30 package — the exact content for a
future append-only sidecar `02_ANALYSIS/SF30_WRITER_CENSUS_SUPERSESSION_R3.md` in the
LINK30 package (the persistence worker will apply it after adjudication; you draft the
text only).

### W5. SLOT17 AUDIT FINDINGS VERIFICATION

Verify each finding YOURSELF from disk/bytes — never assume the finding is right. Each
gets a disposition ACCEPTED / PARTIALLY_ACCEPTED / REJECTED_WITH_EVIDENCE with YOUR OWN
evidence. Output -> `02_ANALYSIS/SLOT17_AUDIT_FINDINGS_DISPOSITION.md`.

- **AUD-F1 (P2)**: the SLOT17 HANDOFF.md claims "OBSERVED_MASTER_SHA: 3644e5ac... (local
  master and live remote master observed equal to BASE_SHA; no drift)". Verify the
  chronology from git evidence: master commit a7a6c756 (LINK30 AMEND_R2 publication) has
  timestamp 2026-09-14 14:40:54 -0700; the SLOT17 branch commit 5290e79 timestamp
  15:11:43 -0700; the SLOT17 completing session started 14:31 local. Determine what was
  provable: RUN_START_OBSERVATION (master==3644e5ac at 14:31 — TRUE) vs
  PUBLICATION_OBSERVATION (at the 15:11 branch commit, local master was ALREADY
  a7a6c756 — drift existed at publication). Use `git log --format` with author+commit
  dates, `git reflog` (if the reflog retains the evidence — AT_FORMALIZE it does; see
  GIT_OBSERVATIONS_AT_FORMALIZE.md section 7), `git ls-remote` for the branch. If exact
  remote-head chronology cannot be proven: set REMOTE_HEAD_CHRONOLOGY = UNRESOLVED. The
  science branch validity does NOT depend on it (the branch was isolated at pinned
  parent 3644e5ac — verify the parent yourself with
  `git rev-parse 5290e79e0dc469c70605f35c125d7b727f9f7a6b^`). Disposition expected: the
  HANDOFF wording is imprecise/unscoped (a temporal-scope erratum, not a science defect).

- **AUD-F2 (P3)**: the SLOT17 HANDOFF says FILES_CHANGED census "03_EVIDENCE 15,
  06_REPORT 5". Recount the commit tree PHYSICALLY:
  `git ls-tree -r 5290e79e0dc469c70605f35c125d7b727f9f7a6b --name-only` and count
  per-directory. Expected (PE-MASTER disk census, confirmed by the formalizer):
  03_EVIDENCE = 16, 06_REPORT = 4, TOTAL = 35 (00_CONTROL 6, 01_RAW 3, 02_ANALYSIS 6).
  Persist the erratum with the true census; the TOTAL 35 stands.

- **AUD-F3 (P3)**: the SLOT17 REPORT says "All evidence was regenerated by the
  completing session" while the SLOT17 RUN_CONTRACT honesty note is narrower
  (02_ANALYSIS rewritten, 03_EVIDENCE + 01_RAW disasm regenerated). Verify the
  carry-over: the completing session started 14:31 local; measure the LastWriteTime of
  EVERY file in the SLOT17 worktree package. Expected (PE-MASTER's measurement —
  re-derive; treat as a pin): `00_CONTROL\entropia_rtti_probe.py` 14:11,
  `parse_coff_vtable.py` 14:12, `entropia_disasm_7b5390.py` 14:18,
  `coff_disasm_symbol.py` 14:24, `01_RAW\GB12_SOURCE_LOCATORS.md` 14:26 (all BEFORE
  14:31 = carried from the interrupted sessions); all other files 14:39 or later
  (regenerated/rewritten). Distinguish explicitly in the erratum: REGENERATED = the
  analysis/evidence/raw classes actually recreated; CARRIED = exactly those 5
  control/source-locator files. Do NOT downgrade the science if the carried files'
  content is correct (the completing session re-measured every oracle hash pin — note
  this in the erratum; the mtime is corroboration, NOT the sole proof — the content
  correctness stands on the completing session's re-measurements recorded in the
  SLOT17 package 00_CONTROL/SOURCE_IDENTITIES.json).

- **AUD-F4 (P3)**: the SLOT17 `entropia_rtti_probe.py` docstring claims the binary's
  optional header reads "+4 shifted" for ImageBase. VERIFY from the physical EXE (own
  byte read; fail-closed SHA+SIZE first): e_lfanew at file offset 0x3C; PE signature;
  optional header start = derive yourself (e_lfanew + 0x18). Expected pins (PE-MASTER's
  measurement — re-derive): e_lfanew=0x120, opt header start 0x138, magic 0x10B,
  dword@opt+0x1C (standard ImageBase) = 0x00400000, dword@opt+0x20 (SectionAlignment)
  = 0x00001000, DllCharacteristics@opt+0x46 = 0x0000. Persist the docstring erratum
  (the "+4 shifted" claim is factually wrong; the standard IMAGE_OPTIONAL_HEADER32
  layout holds — ImageBase is at OptionalHeader+0x1C). The historical commit 5290e79 is
  NEVER rewritten; the erratum lives in THIS cleanup package. Every future adapted
  script must use the standard wording. Raw evidence ->
  `01_RAW/ENTROPIA_PE_OPTIONAL_HEADER_DUMP.txt`.

- **AUD-F5 (P3)**: a historical (chat-only, not on disk) PE-MASTER review of SLOT17
  claimed the installed GB112 SDK path = "extracted\Gb112_eval" with "full same
  content". VERIFY: the NiMain.lib ACTUALLY used by the SLOT17 run (per the SLOT17
  package's own 00_CONTROL/SOURCE_IDENTITIES.json) is
  `D:\gamebyroengine\Gamebryo 1.1.2 Evaluation\SDK\Win32\Lib\VC71\ReleaseLib\NiMain.lib`
  (verify existence/size/SHA256 against THIS contract's SOURCE_IDENTITIES.json pin).
  Census `D:\gamebyroengine\extracted\Gb112_eval\` (expected: Documentation only — see
  SOURCE_IDENTITIES.json for the AT_FORMALIZE census). Erratum: oracle identity is
  ALWAYS physical path + size + SHA256; the "Gb112_eval = full same content" claim is
  REJECTED_WITH_EVIDENCE (Gb112_eval = Documentation only; the lib used = the installed
  Evaluation SDK path).

- **AUD-F6 (P3)**: the historical (chat-only) PE-MASTER verdict contained
  "FINAL origin/master=3644..., no drift". Since the review text is not on disk, the
  disposition document records the superseded wording + the corrected temporal statement
  (at SLOT17 publication time local master was a7a6c756; the "no drift" statement was
  true at run start, stale at publication). The FUTURE persisted PE_MASTER_REVIEW.md
  (written by the persistence worker per the human's §22 decision) carries the corrected
  temporal scoping; no verbatim chat text is reconstructed.

- **AUD-F7 (P3)**: the SLOT17 REPORT line "BASE_SHA 3644e5ac... (= origin/master = live
  remote master = isolated worktree HEAD, re-verified)" lacks temporal scope. Erratum:
  distinguish AT_RUN_START vs AT_PUBLICATION explicitly (same evidence as AUD-F1).

### W6. GB12 VTABLE TABLE ERRATUM (G4) + NiRTTI PRECISION (G5)

Output -> `02_ANALYSIS/SLOT17_ERRATA.md`.

1. The raw relocation JSON `03_EVIDENCE/GB12_NINODE_OBJ_VTABLE_DUMP.json` (and
   `GB12_CHAIN_OBJ_VTABLE_DUMP.json`) in the SLOT17 package is the source of truth.
   Verify the GB12 NiNode vtable sequence from the raw JSON YOURSELF. Expected slots:
   13=GetGroup, 14=SetGroup, 15=UpdateControllers, 16=UpdateNodeBound,
   17=ApplyTransform, 18=GetObjectByName, 19=SetSelectiveUpdateFlags.
2. The prose table in `02_ANALYSIS/CLASS_HIERARCHY_AND_VTABLE_MAP.md` rows for slots 13-16
   in the NiAVObject/NiNode columns are WRONG (they duplicate UpdateControllers at 13
   AND 15 and UpdateNodeBound at 14 AND 16, misplacing the inherited GetGroup/SetGroup).
   The headline results (GB12 slot17=ApplyTransform, GetObjectByName@18,
   SetSelectiveUpdateFlags@19) are CORRECT and unchanged. RAW JSON untouched;
   append-only erratum.
3. The erratum also covers the NiRTTI precision statement (G5), in exactly three parts:
   - 0x00BA7218 = NiNode NiRTTI — CONFIRMED (static-initializer call-site proof,
     ENTROPIA_NIRTTI_STATIC_INIT.txt);
   - the base pointer VALUE 0x00BA7270 — CONFIRMED (the pushed immediate);
   - 0x00BA7270 semantic identity = NiAVObject NiRTTI — STRONGLY_SUPPORTED (via the
     independent MSVC RTTI chain .?AVNiNode@@ -> .?AVNiAVObject@@ + the NiImplementRTTI
     pattern), NOT CONFIRMED absent a direct NiAVObject static-initializer proof.
4. OPTIONAL BOUNDED PROBE (allowed, only if trivially bounded): scan .text for the byte
   pattern `B9 70 72 BA 00` (mov ecx, 0x00BA7270) — if found, decode the surrounding
   static initializer; if it provably constructs NiRTTI at 0x00BA7270 with a "NiAVObject"
   name literal, record the direct proof (upgrading the semantic identity toward
   CONFIRMED, with the evidence class stated). If the probe starts expanding the seam
   (anything beyond this one pattern + its immediate context): STOP, keep
   STRONGLY_SUPPORTED, record NOT_PROBED or the bounded result.

### W7. F5 DISPOSITION (G10)

Output -> `02_ANALYSIS/F5_DISPOSITION.md`.

1. Record the human's OPTION C decision verbatim-faithful:
   **F5_PROCESS_STATUS = PARKED_UNAUTHORIZED_ATTEMPT** (the FIRSTCALL run started
   before the authorization gate; the violation history stands; the package is never
   completed, never retro-authorized, never deleted, its science never adopted, never
   published; it stays untracked on disk untouched).
2. Re-verify the FIRSTCALL package census against THIS cleanup's
   00_CONTROL/SOURCE_IDENTITIES.json (7 files — 6 content + 1 .pyc, hashes recorded by
   the formalizer; re-hash NOW, assert unchanged; the 3 empty directories are named
   there too).
3. THEN the supersession comparison (this is a QC comparison, NOT adoption of FIRSTCALL
   as an evidence source): compare FIRSTCALL `01_RAW/SLOT17_BODY_RAW.txt` (its measured
   facts: calibration .?AVSceneFeederObject@@ PASS; NiNode RTTI walk PASS; slot17 dword
   = 0x007B5390; the 6 dispatch pins byte-exact; body decode 0x007B5390 first call
   @0x007B5399 E8 target 0x007BF220; target prologue NULL-guards + byte-pair strcmp +
   ret 4) against the SLOT17 package's INDEPENDENT re-measurements
   (01_RAW/ENTROPIA_007B5390_DISASM.txt + 02_ANALYSIS fingerprints): assert consistency
   AND strict subsumption (every FIRSTCALL measured fact is re-measured independently
   and consistently in SLOT17, which additionally decoded the full extent, neighbors,
   vtable prefix and NiRTTI). Build the per-fact consistency table.
4. If confirmed: F5_SCIENCE_STATUS = SUPERSEDED_SCIENTIFICALLY_BY
   PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914 (commit
   5290e79e0dc469c70605f35c125d7b727f9f7a6b). Any inconsistency: record it and set
   F5_SCIENCE_STATUS = NOT_SUPERSEDED (do not force).

### W8. SCIENCE STATUS MATRIX

Output -> `02_ANALYSIS/SCIENCE_STATUS_MATRIX.csv` with columns:
era, item, status_before, status_after, evidence_pointer.

Preserve ALL standing statuses (do not invent changes):
- SF+0x30 identity NiNode — CONFIRMED
- [vtable+0x44]=0x7B5390 — CONFIRMED
- 0x7B5390 observed recursive named lookup — CONFIRMED
- 0x7B5390 = NiNode::GetObjectByName — STRONGLY_SUPPORTED (NOT to be raised without a
  separately authorized era/generation-qualified oracle experiment — the locked B->A
  criterion)
- Entropia +0x90 = m_kWorld.m_Translate.x — CONFIRMED STRUCTURAL
- SF+0x30 graph root/container — PLAUSIBLE
- arg2 ABI — partially observed, revalidate-pending
- arg2 provenance — UNVERIFIED
- arg2 semantic role — UNVERIFIED
- downstream consumer — UNVERIFIED/partially observed
- MODEL_ASSET_TO_SCENEGRAPH_ROOT — NOT_DEMONSTRATED
- PLACEMENT_TO_SCENEGRAPH_TRANSFORM — partially known
- TRANSFORM_TO_MODEL — NOT_DEMONSTRATED
- MODEL_BRIDGE — NOT_DEMONSTRATED
- engine generation identity — UNVERIFIED

Update ONLY what W1-W7 changed (the E1/E2 rows' status in the census layer; the NiRTTI
semantic identity if W6's probe upgraded it). Every row cites its evidence pointer.

### W9. PACKAGE COMPLETION

- Write `03_EVIDENCE/README.md` + `03_EVIDENCE/EVIDENCE_INDEX.csv` — index EVERY
  evidence/raw/analysis artifact with its role + generator.
- `01_RAW/` receives: the E1/E2 disassembly raw listings; the caller-provenance raw
  censuses; the classifier test raw outputs; the timestamped git observation
  AT_CLEANUP_START (suggested name `01_RAW/GIT_OBSERVATIONS_AT_CLEANUP_START.md`:
  timestamp, HEAD, branch, origin/master, ls-remote, status --short, worktree list);
  the Entropia PE optional-header byte dump (AUD-F4 evidence).
- All scripts deterministic, run with `-B`, no `__pycache__` in the package, NO
  proprietary payloads (hashes/addresses/derived facts only — no binary dumps), the
  interpreter cited as canonical path + measured version (and capstone measured
  `__version__` + `__file__`, see B.8).
- `06_REPORT/REPORT.md` + `06_REPORT/HANDOFF.md` +
  `06_REPORT/STAGE_ACCEPTANCE_GATES.csv` are written AFTER the evidence (the fresh QC
  and PE-MASTER audit come between). You DRAFT them with honest placeholders for the
  QC/verdict fields marked PENDING (G14/G15 remain PENDING — closed by others).

---

## E. FORBIDDEN (HARD)

- NO execution of Entropia.exe or ANY game/oracle binary. STATIC-ONLY.
- NO modification of the FIRSTCALL package (read + hash census only).
- NO modification of `experiments/`.
- NO force-push / rewrite / delete of the SLOT17 branch or commit 5290e79.
- NO modification of the SLOT17 worktree package files (READ-ONLY).
- NO modification of the LINK30 historical artifacts
  (`02_ANALYSIS/SF30_WRITER_CENSUS.csv`, `01_RAW/SF30_WRITER_RAW.txt` must be
  byte-identical before == after — assert).
- NO `AUDIT_ENTRYPOINT.md` edits (the persistence worker's job).
- NO wiki / canonical-state changes; NO milestone actions.
- ZERO git mutations (no add/commit/push/stage/branch/checkout).
- NO proprietary payloads in any output (hashes/addresses/derived facts only).
- NO `__pycache__` anywhere in the package.

---

## F. STAGE ACCEPTANCE GATES G0-G15

The executor SELF-ASSESSES G0-G12; the fresh QC verifies; PE-MASTER adjudicates. Write
each gate into `06_REPORT/STAGE_ACCEPTANCE_GATES.csv` with columns:
`GATE / MEASURED_QUANTITY / INDEPENDENT_SOURCE_OF_TRUTH / WHY_NON_CIRCULAR /
FAILURE_CASE_DETECTED / STATUS`. Never mark a self-assessed gate PASS without the
measured quantity and the independent source of truth.

- **G0_SOURCE_IDENTITY**: Entropia SHA+SIZE == pins; HEAD == BASE_SHA; SLOT17 branch
  tip == 5290e79; untracked set == expected (the three entries of B.2).
- **G1_GIT_STATE_TIMESTAMPS**: timestamped git observations recorded
  (AT_CLEANUP_START) with HEAD / branch / origin/master / ls-remote / status --short /
  worktree list.
- **G2_SLOT17_BRANCH_INTEGRITY**: branch tip unchanged; parent == 3644e5ac; worktree
  clean; package file count 35 (recount per-directory: 16/4 erratum verified via
  git ls-tree).
- **G3_AUD_F1_F7_DISPOSITIONS**: all seven findings dispositioned with OWN evidence
  (not assumed).
- **G4_GB12_TABLE_ERRATUM**: raw JSON re-verified (slots 13-19 sequence); prose table
  erratum recorded.
- **G5_NIRTTI_PRECISION**: the three-part statement recorded (0xBA7218 CONFIRMED /
  pointer value 0xBA7270 CONFIRMED / semantic identity STRONGLY_SUPPORTED unless the
  bounded probe proved it directly).
- **G6_EBP_E1_PROVENANCE**: E1 dispositioned with case A/B/C or NONE_PROVEN, with
  VA+bytes.
- **G7_EBP_E2_PROVENANCE**: same for E2.
- **G8_CLASSIFIER_NEGATIVE_TEST**: the synthetic fixture returns POSSIBLE_ALIAS (if
  REJECTED -> cleanup FAIL); the positive control returns REJECTED_ALIAS.
- **G9_CENSUS_RECOMPUTATION**: derived counts recorded; TOTAL == 3643 asserted;
  per-row OLD/NEW/PROOF/STATUS for every changed row; historical CSV/RAW
  byte-identical (hash asserts before == after).
- **G10_F5_HOLD_DISPOSITION**: F5_PROCESS_STATUS recorded; FIRSTCALL 7 hashes
  unchanged; supersession comparison recorded with the per-fact consistency table.
- **G11_HISTORICAL_ARTIFACT_IMMUTABILITY**: FIRSTCALL untouched; experiments/ untouched;
  SLOT17 worktree package untouched; LINK30 CSV/RAW byte-identical; SLOT17 commit/branch
  untouched.
- **G12_SLOT17_SCIENCE_STABILITY**: the standing SLOT17 statuses (observed operation
  CONFIRMED, identity STRONGLY_SUPPORTED, +0x90 CONFIRMED STRUCTURAL) re-affirmed from
  the package evidence (no downgrade, no upgrade beyond W6's bounded result).
- **G13_CANONICAL_INTEGRATION**: the cleanup package contents are internally consistent
  (counts, errata, matrix) and the drafted R3 sidecar text (if counts changed) is
  consistent with the evidence. NOTE: the ACTUAL cherry-pick + commits + push happen
  AFTER PE-MASTER adjudication (G15 is closed by the persistence worker).
- **G14_FRESH_QC**: placeholder PENDING (the fresh-context QC closes it).
- **G15_PERSISTENCE**: placeholder PENDING (the persistence worker closes it).

---

## G. NON-PASS CLASSES

For each gate: **PASS / FAIL / NOT_APPLICABLE (with reason) / PENDING (G14/G15 only)**.

Cleanup-level outcome (exactly one of):
- `PRELOOP_CLEANUP_PROPOSAL_READY` — all self-assessed gates G0-G12 PASS (or
  NOT_APPLICABLE with reason) and evidence consistent;
- `PRELOOP_CLEANUP_DEFECTS_FOUND` — list the defects honestly (defects do NOT fail the
  loop; they go back to PE-MASTER for adjudication).

An incomplete work item is reported INCOMPLETE — never PASS (see H).

---

## H. TIMEBOX

The executor's soft timebox is **40 minutes of work**. If a work item exceeds its
bounded scope: STOP that item, record the bound reached, and continue with the rest.
The run reports honestly; an incomplete item is INCOMPLETE, not PASS. Three similar
blockers are a return to PE-MASTER, not a declaration that the night is finished.

---

## I. FINAL_HANDOFF_SCHEMA (your return message to PE-MASTER)

- RUN_ID
- BASE_SHA
- OBSERVED_HEAD_SHA
- git mutations (expected NONE)
- per-work-item status (W1-W9)
- E1_FINAL_CLASS + which case proven (A/B/C/NONE_PROVEN)
- E2_FINAL_CLASS + which case proven
- DERIVED_CENSUS_COUNTS (must sum 3643)
- CLASSIFIER_TEST_RESULTS (negative + positive)
- F5_SCIENCE_STATUS
- NiRTTI semantic identity status
- AUD-F1..F7 one-line dispositions each
- gates G0-G12 self-assessed states
- P0/P1/P2 findings (if any)
- REPORT_PATH
- HANDOFF_PATH
- EVIDENCE_PATHS
- RUN_STATUS
- HARD_STOP_REASON (expected NONE)

---

## J. MANDATORY PROCESS RULES

1. **L22 discipline**: re-derive every expected value from the physical sources in-run.
   The contract states them only as fail-closed pins. The SLOT_CENSUS and all quantities
   are NEVER taken from prose.
2. Every hash you write is script-computed, never hand-typed.
3. All scripts run with `-B`; no `__pycache__` in the package.
4. Interpreter = `D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe` (Python
   3.12.7 — the canonical interpreter). Capstone per B.8 (measured provenance recorded
   dynamically; known false 5.0.9 dist-info label; explicit sys.path.insert if the
   capstone_lib copy is required).
5. Every raw evidence file records its generator (script path + SHA256), the executed
   command, and the input identities (SHA pins).
6. Historical runs are immutable: SLOT17 (commit 5290e79, branch, worktree package),
   LINK30 artifacts, the FIRSTCALL package, `experiments/` — read-only, byte-identity
   asserted where pinned.
7. ZERO git mutations by the executor. Publication (cherry-pick of 5290e79 onto current
   master, commits, push, AUDIT_ENTRYPOINT update, PE_MASTER_REVIEW persistence) is the
   persistence worker's separate, later, adjudication-gated step.
8. Do not manufacture findings. If evidence is UNAVAILABLE or NOT_OBSERVED_IN_CAPTURE,
   say so; UNAVAILABLE is not NO.
9. Save a precise RESUME_POINT on disk (in this package, 00_CONTROL/ or 02_ANALYSIS/)
   if interrupted mid-run; a child deadline is a return to the parent, never a silent
   truncation of evidence.

## K. READ-ONLY INPUT INVENTORY (paths you may read; NEVER modify)

- `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe` (fail-closed SHA+SIZE first;
  never execute)
- SLOT17 worktree package (all 35 files), notably:
  - `06_REPORT/HANDOFF.md` (AUD-F1/F2 claims), `06_REPORT/REPORT.md` (AUD-F3/F7)
  - `00_CONTROL/RUN_CONTRACT.md` (AUD-F3 honesty note),
    `00_CONTROL/entropia_rtti_probe.py` (AUD-F4 docstring),
    `00_CONTROL/SOURCE_IDENTITIES.json` (AUD-F5 NiMain.lib identity)
  - `03_EVIDENCE/GB12_NINODE_OBJ_VTABLE_DUMP.json`, `GB12_CHAIN_OBJ_VTABLE_DUMP.json`,
    `ENTROPIA_NIRTTI_STATIC_INIT.txt` (W6)
  - `02_ANALYSIS/CLASS_HIERARCHY_AND_VTABLE_MAP.md` (W6 prose defect),
    `02_ANALYSIS/ENTROPIA_SLOT17_FINGERPRINT.md`,
    `02_ANALYSIS/GETOBJECTBYNAME_FINGERPRINT.md` (W7)
  - `01_RAW/ENTROPIA_007B5390_DISASM.txt` (W7)
- LINK30 package: `02_ANALYSIS/SF30_WRITER_CENSUS.csv`, `01_RAW/SF30_WRITER_RAW.txt`
  (+ their SHA pins in this package's SOURCE_IDENTITIES.json)
- FIRSTCALL package: all 7 files (census + W7 comparison ONLY)
- `D:\gamebyroengine\Gamebryo 1.1.2 Evaluation\SDK\Win32\Lib\VC71\ReleaseLib\NiMain.lib`
  and `D:\gamebyroengine\extracted\Gb112_eval\` (AUD-F5)
- This package's `00_CONTROL/` (RUN_CONTRACT.md, SOURCE_IDENTITIES.json,
  GIT_OBSERVATIONS_AT_FORMALIZE.md)

END OF CONTRACT.
