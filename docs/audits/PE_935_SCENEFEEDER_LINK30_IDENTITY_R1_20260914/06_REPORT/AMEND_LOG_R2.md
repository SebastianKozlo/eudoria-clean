# AMEND_LOG_R2.md — PE_935_SCENEFEEDER_LINK30_AMEND_R2_20260914 (post-audit amendment)

- **Amendment order**: PE_935_SCENEFEEDER_LINK30_AMEND_R2_20260914 (RUN_CLASS MATERIAL,
  post-audit amendment of the published package
  PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914): the human's AMENDMENT ORDER of
  2026-09-14 "PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 (post-audit Desktop R2,
  AMEND_LOG_R2)", delivered to PE-MASTER; PE-MASTER adjudicated the Desktop findings
  (F1-F4 ACCEPTED; F5 accepted-as-process-fact / HOLD, human adjudication pending).
  Executor: pe-reconstruction (direct PE-MASTER dispatch). NO NESTED TASKS. NO HUMAN
  PROMPTS. STATIC-ONLY; originals fail-closed; zero runtime; ZERO git mutations by
  this amendment (no add/commit/push/stage; publication remains a separate later step
  by pe-master-auditor after PE-MASTER adjudication).
- **BASE_SHA re-verified before any change (fail-closed)**: HEAD == origin/master ==
  `git ls-remote origin master` == 3644e5ac9cbf7b5445861e7f5342fb8642741346 (the LINK30
  publication commit); pre-run `git status --short` showed exactly the two baseline
  untracked paths (`?? docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/`,
  `?? experiments/`) and NOTHING else; `git diff HEAD` and `git diff --cached` empty.
- **EXE pin re-verified in-run (fail-closed asserts at the top of the proof script)**:
  Entropia.exe SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31,
  size 8015872, machine 0x014C, opt_magic 0x010B, image_base 0x00400000, no ASLR
  (DLLCHARACTERISTICS 0x0000) — all re-derived by the amendment's own PE walk (raw
  artifact §P1).
- **NO `.pre` files** (the R1 convention; this log's SHA pairs replace byte-prefix
  copies). Transient scripts and before-copies live OUTSIDE the package under
  `C:\Users\User\AppData\Local\Temp\opencode\sf30_amend_r2\` (never inside it).
- **Interpreter**: `D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe` —
  Python 3.12.7 (measured `--version` in-run; the canonical interpreter; every script
  run with `-B`).

## 0. Pre-edit verification (the adjudicated defect facts re-measured BEFORE editing)

- **F1 (the 0x405250/0x40525B bytes)** — re-measured by the proof script (P2,
  fail-closed): 0x00405250 == 8B 15 D8 C3 B6 00 (`mov edx, dword ptr [0xb6c3d8]`),
  0x00405256 == 68 30 4C 40 00 (`push 0x404c30`), 0x0040525B == 89 5A 30
  (`mov dword ptr [edx + 0x30], ebx`); the historical raw why-line
  (01_RAW/SF30_WRITER_RAW.txt line 320) reads "R-IMM-STATIC: base==edx = fixed
  immediate address" and the historical CSV row 18 reads "static data address" —
  both quoted verbatim in the sidecar. The mislabel re-measured: the base register is
  LOADED from the global pointer slot 0x00B6C3D8 (P2 PASS).
- **F3 (the qc4_sample_scope.py hash vs QC §9 line vs manifest row)** — fresh SHA256
  of 00_CONTROL\qc_probe\qc4_sample_scope.py ==
  22E9AC4CF76625076FA7B2D5E8EA200BCC041B8A20FC15B07634A29D49B3D942 == the
  MANIFEST_SHA256.csv row (both verified equal); 06_REPORT/QC_AUDIT_R1.md line 395
  carried ...22E9AC4CF7662502**2**6FA7... (one wrong hex character, a transcription
  of the same file's hash). Fixed by EDIT 4 below (exactly ONE byte).
- **F2 (the qc1_counters.py:88 predicate)** — the predicate read verbatim:
  `log("claim match (2/618/3023/0, total 3643): %s" % ("PASS" if dict(cc) == CLAIM and len(rows) == 3643 else "FAIL"))`
  — `dict(cc) == CLAIM` compares a live Counter dict (which never carries the
  UNRESOLVED key when its count is 0) against a fixed 4-key dict, so the clause is
  ALWAYS False; the artifact line 01_RAW/../out_qc1_counters.txt line 28 therefore
  reads "claim match (2/618/3023/0, total 3643): FAIL" while its own lines 24 and 27
  show the counts DO match (REJECTED 3023 / POSSIBLE 618 / PROVEN 2; UNRESOLVED rows:
  0). The probe files stay byte-identical (erratum E-3).
- **F4 (the interpreter version)** — measured in-run: `python.exe --version` ==
  "Python 3.12.7"; 03_EVIDENCE/README.md line 32 previously read "Python 3.12.10"
  (transcription error; corrected by EDIT 5).

## 1. The F1-P proof record (00_CONTROL/f1_globalptr_proof.py ->
01_RAW/F1_GLOBALPTR_PROOF_RAW.txt; the QUESTION: is the census row 0x0040525B's
receiver PROVABLY never a SceneFeederObject pointer — via the global pointer slot
0x00B6C3D8 — so that REJECTED_ALIAS stands with the corrected justification
R-GLOBAL-PTR-NON-SF?)

Method: own minimal PE parser (written for this proof; the historical sf30_core.py /
census.py NOT imported, NOT modified), capstone 5.0.7 from the pinned path, full
.text linear sweep 0x00401000..0x00A75000 with the bad-byte restart rule (restart at
cursor+1; recorded facts: **2,266,698 instructions decoded, 64 restarts — identical
to the accepted run's sweep statistics**), every pin re-derived from physical bytes.
Per-predicate results (full census listings in the raw artifact):

- **P1 PASS** — identity/base as above (raw §P1).
- **P2 PASS** — 0x00405250/0x00405256/0x0040525B boundary-aligned decode == pins; the
  sweep stream contains all three as instruction starts; EXACTLY ONE instruction
  starts in the open interval (0x405250, 0x40525B) — the push — and it does NOT
  define edx.
- **P3 PASS** — full-.text census of absolute [0x00B6C3D8] mem operands: **179
  occurrences total = EXACTLY ONE WRITE @0x00404C9D (A3 D8 C3 B6 00, `mov dword ptr
  [0xb6c3d8], eax`) + 178 READs** (all 179 recorded VA+access+bytes+rendered in the
  raw artifact; all plain mov forms — no lea, no RMW, no unknown-access operands).
- **P4 PASS** — EXACTLY ONE E8 rel32 call targeting 0x00409080 in .text:
  @0x00404C8B (E8 F0 43 00 00); raw dword 0x00409080 occurrences in the WHOLE FILE ==
  0 (no function-pointer channel).
- **P5 MISMATCH (literal pin; chain substance PROVEN)** — the pinned chain decodes
  byte-exactly (0x00404C86 `mov ecx, 0xb9fec0` (B9 C0 FE B9 00) immediately before the
  call; between call-end and store exactly `push 0xb6c3d8` @0x404C90 + `mov dword ptr
  [esp + 0x14], 0xffffffff` @0x404C95 — neither defines eax; the last eax definition
  in FUN_00409080 is `mov eax, esi` @0x00409142 (8B C6) followed ONLY by epilogue and
  `ret 4` @0x00409155 (C2 04 00); ZERO bad bytes in the body; ZERO writes to
  [esi]/[esi+0] — **no vtable store, non-polymorphic; the vtable-store HARD-STOP branch
  did NOT fire**). MISMATCH detail: the pin "mov esi, ecx @0x004090A5 is the ONLY
  definition of esi in the body" is contradicted by the epilogue's `pop esi`
  @0x00409150 (a second esi definition — measured: esi definitions in body = 2). The
  chain-relevant convention (definitions UP TO the capture, the accepted run's QC-C2
  convention) HOLDS: no esi redefinition between 0x004090A5 and the eax capture
  @0x00409142 (the pop esi is AFTER the capture and does not affect the return value);
  entry ecx is unmodified to 0x004090A5 (12 instructions, no calls). The pin's wording
  is a contract-label defect of the same class as R1's "TD+0x0C" (the same sentence
  pins "followed ONLY by epilogue", acknowledging the very epilogue that contains the
  pop). The chain substance — return value == `this` == 0x00B9FEC0 — is byte-proven;
  this mismatch does not change the branch outcome (P7 alone routes to branch (b)).
- **P6 PASS** — 0x00B9FEC0 lies in .data (measured section 0x00B6C000..0x00BA96E4,
  file-backed to 0x00BA0000; va_start == 0x00B6C000); at-rest dwords
  [0x00B9FEC0..0x00B9FF20] == ALL ZERO (25 dwords recorded); [0x00B6C3D8] at rest ==
  0x00000000.
- **P7 MISMATCH — ALIAS_CHANNEL_OPEN (the branch-deciding predicate)** —
  IMM-operand census of 0x00B6C3D8 in .text == EXACTLY 1 (`push 0xb6c3d8` @0x00404C90,
  68 D8 C3 B6 00); its consumer is FUN_00404B60 (E8 call site @0x00404CA2; the arg
  verified at [esp+0x20] by the measured stack arithmetic: 4 (retaddr) + 0 (caller
  delta) + 28 (callee prologue delta) == 0x20); the arg is loaded into edx
  (`mov edx, dword ptr [esp + 0x20]` @0x00404BC5, 8B 54 24 20). Census over the FULL
  decoded window (58 instructions, body-end by the documented CC-padding rule,
  path-insensitive per the contract):
  - (a) WRITE mem-operands [argreg+0]: **1 — NOT expected ZERO**: `lock xadd dword
    ptr [edx], eax` @0x00404C00. Path analysis (from the same window decode): edx is
    redefined at 0x00404BFE (`mov edx, ecx`, 8B D1) — immediately
    before the xadd (ecx = [esp+8] from `mov ecx, dword ptr [esp + 8]` @0x00404BF5),
    so on the actual dataflow edx at 0x00404C00 does NOT hold the arg: a
    register-reuse FALSE POSITIVE of the pre-registered path-insensitive census.
  - (b) stores of the arg register to memory: **1 — REAL**: `mov dword ptr [ecx],
    edx` @0x00404BE9 (89 11) — no edx redefinition between the arg load @0x00404BC5
    and the store on ANY path in the window (the intervening instructions write only
    esi/ecx/eax/flags). FUN_00404B60 inserts the arg — &global — into a linked list
    (node layout +8 key, +0xc next: it reads [arg+8] @0x404BD3 `cmp esi, dword ptr
    [edx + 8]`, writes [arg+0xc] @0x404BE6 `mov dword ptr [edx + 0xc], eax` — both
    the expected observations — and links the predecessor/head slot to the arg
    @0x404BE9).
  - => the &global POINTER escapes into a list structure; a write through that
    list-derived pointer (some other code writing the node's +0 field — the +0 field
    IS the global slot) is NOT excludable within this amendment's static decode
    bounds. The value space {0x00000000, 0x00B9FEC0} is therefore proven ONLY for the
    DIRECT write channel; the indirect channel remains unbounded.
- **P8 PASS** — exactly TWO imm32 0x00A7D458 stores in .text (@0x00509366
  C7 45 00 58 D4 A7 00 and @0x0050A269 C7 06 58 D4 A7 00; whole-file dword
  occurrences == 2, both at the imm positions 0x00509369/0x0050A26B, both true-start
  WRITE stores); ZERO absolute dword refs of 0x00509330 in the whole file; SF ctor E8
  callers == exactly {0x0047D043, 0x0052480F}; in the FUN_005247C0 window the SF-block
  allocation is `push 0x98` @0x005247E7 (68 98 00 00 00) + the operator-new thunk
  call @0x005247EC (E8 D3 8B 43 00, call 0x95d3c4 — the MSVCR80.dll operator-new
  thunk per the accepted run's IAT walk, not re-decoded here) before the ctor call
  @0x0052480F — both creation paths operator new -> heap.
- **P9 PASS** — counts recomputed by parsing the UNCHANGED CSV: 3643 rows ==
  2 PROVEN_SF30_WRITER / 618 POSSIBLE_ALIAS / 3023 REJECTED_ALIAS / 0 UNRESOLVED
  (UNRESOLVED via .get(k, 0)); row 0x0040525B present with classification
  REJECTED_ALIAS (CSV row quoted verbatim in the sidecar).

**F1-P VERDICT: FAIL (P7 (b) NONZERO — ALIAS_CHANNEL_OPEN; P5 literal-pin mismatch
with the chain substance proven). BRANCH DECISION: (b)** per the amendment contract's
pre-registered branches: the row 0x0040525B is reclassified
REJECTED_ALIAS -> POSSIBLE_ALIAS in this canonical record; canonical counts
3643 = 2 PROVEN / **619 POSSIBLE** / **3022 REJECTED** / 0 UNRESOLVED; the historical
CSV/RAW artifacts stay byte-identical (NOT regenerated; the supersession sidecar
02_ANALYSIS/SF30_WRITER_CENSUS_SUPERSESSION_R2.md carries the canonical state). The
R-GLOBAL-PTR-NON-SF label does NOT stand: the rejection would rest on the unverified
assumption that no list-derived write ever reaches the global slot — a rejection must
be structurally self-contained (erratum E-2).

## 2. The edits (before/after SHA256; exactly-once anchors verified before and after)

**2a. EDIT 4 — 06_REPORT/QC_AUDIT_R1.md (the F3 one-character fix).**
B80DD10B42F9A40EC1E211CF3DD508D4206B35017B3E3F64370AAC338EF6040A ->
6378165ED945113A9B252F4E5FB650236C220553FCFC2664017076F427FFC632.
EXACTLY ONE BYTE changed (offset 28048): the qc4_sample_scope.py hash's wrong hex
character '2' -> '7' (the contract's order text calls it "the 17th hex character"; the
measured differing position is the 16th — the explicit OLD/NEW hash strings in the
order are unambiguous and were applied verbatim). Pre-assert held: fresh SHA256 of
qc4_sample_scope.py == 22E9AC4CF76625076FA7B2D5E8EA200BCC041B8A20FC15B07634A29D49B3D942
== the MANIFEST row; the FILE qc4_sample_scope.py itself NEVER touched (hash
before==after, section 7). Post-assert: the wrong string occurs 0 times, the correct
string exactly once.

**2b. EDIT 5 — 03_EVIDENCE/README.md (the F4 interpreter fix + artifact map + reproduce
line).** FDBE55B810583EC33833B16A8DA48553BDB207A4A14474D087445004F64BC360 ->
187BDCD7B99348222A2FB1556E192E1433295D2A99C3BF7EBBC57BED2339BBDF.
Three anchored edits: (i) line 32 "Interpreter: Python 3.12.10 (Windows host)..." ->
the canonical interpreter path + "Python 3.12.7 (canonical reproduction interpreter;
version re-measured in-run — the prior \"3.12.10\" was a transcription error, erratum
AMEND_LOG_R2 F4)" (rest of the paragraph unchanged); (ii) five artifact-map rows
appended for the new files (06_REPORT/AMEND_LOG_R2.md; 00_CONTROL/f1_globalptr_proof.py;
01_RAW/F1_GLOBALPTR_PROOF_RAW.txt;
02_ANALYSIS/SF30_WRITER_CENSUS_SUPERSESSION_R2.md; 00_CONTROL/amend_r2_manifest.py);
(iii) one reproduce-block line appended: `python -B 00_CONTROL/f1_globalptr_proof.py
# regenerates 01_RAW/F1_GLOBALPTR_PROOF_RAW.txt`.

**2c. EDIT 1 (BRANCH (b) form) — 06_REPORT/REPORT.md, §3 bound paragraph.**
E08A5875790F5A3FDCA539C5A3BE4C717515D08ABBE5937F73CD33CEECE5436D ->
7DF5E0648B7E632F621E71F3172BE33E9D182EBF37106AAB35A4E03549F7081E.
Count updates 618 -> 619 (POSSIBLE_ALIAS, annotated "canonical after AMEND_LOG_R2 F1;
historical row count 618") and 3023 -> 3022 (REJECTED_ALIAS, same annotation); the
fired-reason census relabeled "= 3023 (historical)" (it describes the unchanged raw
artifact); the BRANCH-(b) supersession parenthetical appended (verbatim in the
REPORT §3 text now on disk): the R-IMM-STATIC label superseded (load-from-global
@0x00405250 proven); the direct-write channel PROVEN closed (sole writer 0x00404C9D
storing FUN_00409080's return = its `this` = 0x00B9FEC0, static .data,
non-polymorphic; slot at rest 0); the address-taker channel OPEN
(FUN_00404B60 stores &global into a linked list @0x00404BE9 — write-through-pointer
NOT excluded); row reclassified REJECTED_ALIAS -> POSSIBLE_ALIAS; canonical counts
2/619/3022/0; CSV/RAW byte-identical; pointers to AMEND_LOG_R2 and the sidecar.

**2d. EDIT 6 — 00_CONTROL/SCRIPT_SHA256.csv (two new script rows, CRLF csv format
preserved).** 0C2DE0B2C7DB5FDDE7D71D883351A8FE540A49C8B7AA9D809312561BE2228B61 ->
73F7657F798235E2C07C5E4C9D6F022FF944D32FA9B4A604440B5DCC9277B7A9.
Appended: f1_globalptr_proof.py (SHA256
E313FAD9D78A9ABDA6919D365801996932C175D0496B0CCA077F1BFE325341D5) and
amend_r2_manifest.py (SHA256
5A20758EC65BA6E37E185E7E759DF7297B9F134C4AEFDB34B83488A2A61CE8D4); the existing four
rows byte-identical.

**2e. EDIT 2 — NEW 02_ANALYSIS/SF30_WRITER_CENSUS_SUPERSESSION_R2.md (the supersession
sidecar).** SHA256
DE3F5ED710B9A37F62FDEB7865D50262F78BC036CB2DF30CAD6A9E538FB72921.
Contains: RUN/era/mode header; the superseded CSV row 18 quoted verbatim from the
file; the superseded raw why-line quoted verbatim from 01_RAW/SF30_WRITER_RAW.txt
line 320; the canonical BRANCH-(b) supersession statement (the proof summary with the
key VAs — what PROVED and what failed); the historical-artifact status with the
re-hashed pins (CSV 71552E2A4BFC120DA0BE1A7E108A41A03C873ADDD238637DD7C18F3C968824D0,
RAW 64402A73013B52943E10AE17BB115F466A0D3BEF98AA3835915CF3C1CD572248 — re-hashed and
asserted BEFORE the sidecar was written); the regeneration prohibition; the counts
(historical 2/618/3023/0; canonical 2/619/3022/0).

**2f. EDIT 3 — NEW 06_REPORT/AMEND_LOG_R2.md (this log).** Its own final SHA256 is not
self-recordable (the same regress as the manifest's L12 self-exclusion); it is carried
by the updated MANIFEST_SHA256.csv row (written after this log's final wording by
00_CONTROL/amend_r2_manifest.py) and reported in the executor's delivery notice.

**2g. EDIT 7 — 06_REPORT/MANIFEST_SHA256.csv via the NEW bounded updater
00_CONTROL/amend_r2_manifest.py (run LAST, after this log's final wording).**
Finalize.py was NOT re-run. The updater verified every row against disk (fail-closed),
found the change set == EXACTLY {06_REPORT/REPORT.md, 06_REPORT/QC_AUDIT_R1.md,
03_EVIDENCE/README.md, 00_CONTROL/SCRIPT_SHA256.csv}, added the five new rows, kept
all other rows byte-identical, held self-exclusion, and wrote the 37-data-row
manifest deterministically (rows 32 -> 37). The manifest's own on-disk SHA256 is
reported in the executor's delivery notice.

**2h. APPLIED BY THE COMPLETION BATCH (C1) — the HANDOFF.md residue line (BRANCH (b) count update).**
The amendment contract's BRANCH-(b) text says "apply the count updates in ... HANDOFF
residue line (3023->3022, 618->619)", but the same contract's Forbidden section
prohibits ANY modification of 06_REPORT/HANDOFF.md (and EDIT 7's expected-change set
does not include it; section 7 lists it as untouched). Adjudication (recorded here,
non-silent): the prohibition controls — HANDOFF.md is NOT modified by this
amendment; the canonical state is carried by THIS LOG, the REPORT §3 edit and the
sidecar. The PREPARED text for the persistence worker (verbatim; the current
HANDOFF.md lines 17-18 read):
`  (residue: 3023 REJECTED_ALIAS with per-row reasons; 618 POSSIBLE_ALIAS = the`
`   documented static bound; 0 UNRESOLVED)`
PREPARED replacement:
`  (residue: 3022 REJECTED_ALIAS with per-row reasons; 619 POSSIBLE_ALIAS = the`
`   documented static bound, canonical after AMEND_LOG_R2 F1 branch (b) — census row`
`   0x0040525B reclassified REJECTED_ALIAS -> POSSIBLE_ALIAS; historical row counts`
`   3023/618; 0 UNRESOLVED)`

APPLIED by the completion batch C1 (contract
PE_935_SCENEFEEDER_LINK30_AMEND_R2 completion batch C1, 2026-09-14; PE-MASTER's
audit of this R2 amendment authorized the HANDOFF.md completion): the C4a edit
applied the PREPARED replacement above VERBATIM (the HANDOFF.md residue lines;
cross-checked byte-exact against this prepared block by script before writing),
and the C4b edit applied the gates-line historical/canonical annotation (the
COUNTER_ARITHMETIC sentence; described in section 2j). 06_REPORT/HANDOFF.md SHA256
before -> after: 71A2B1C127ECF4F7191BB9D8E3B3B769B2E41EAAF38137C8D6CA45610E943BC8 ->
6555E81E0252E0A1186BD6ED02A7AF39E5A6ED5B97C5A1A13AF229E63B089B67. The file is REMOVED from section 7's byte-identical
untouched list and is now in the authorized expected-change set (cross-reference
2j).

**2i. PREPARED, NOT APPLIED — the AUDIT_ENTRYPOINT.md row text (for the persistence
worker to adapt to the entrypoint table's conventions; this amendment made ZERO
touches of AUDIT_ENTRYPOINT.md):**
`| (this commit; discover with git log -1 -- docs/audits/PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914) | PE_935_SCENEFEEDER_LINK30_AMEND_R2_20260914 (RUN_CLASS MATERIAL; post-audit amendment of the LINK30 package: Desktop findings F1-F4 applied; the F1-P static proof executed — BRANCH (b): census row 0x0040525B reclassified REJECTED_ALIAS -> POSSIBLE_ALIAS, canonical counts 3643 = 2 PROVEN / 619 POSSIBLE / 3022 REJECTED / 0 UNRESOLVED; the historical CSV/RAW stay byte-identical; supersession carried by 02_ANALYSIS/SF30_WRITER_CENSUS_SUPERSESSION_R2.md + 06_REPORT/AMEND_LOG_R2.md; executor pe-reconstruction, direct PE-MASTER dispatch; NO_NESTED_TASKS; STATIC-ONLY — the client never ran; publication by pe-master-auditor after PE-MASTER adjudication) | PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914/ (amendment — same package) | Post-audit R2 amendment: F1 the R-IMM-STATIC label superseded (load-from-global proven; the direct channel proven closed; the address-taker channel OPEN -> the row falls to POSSIBLE_ALIAS); F2 the qc1 claim-match predicate bug; F3 the QC §9 qc4 hash typo; F4 the interpreter version erratum; F5 (the NINODE package) documented as a process note, PENDING HUMAN ADJUDICATION. | (pending PE-MASTER adjudication) |`

**2j. Completion batch C1 (PE-MASTER audit findings — the four
documentation-completion gaps).** PE-MASTER's audit of this R2 amendment found four
documentation-completion gaps (canonical-layer count claims not yet carrying the
historical/canonical annotation); the completion batch C1 (contract
PE_935_SCENEFEEDER_LINK30_AMEND_R2 completion batch C1, 2026-09-14; executor
pe-reconstruction, direct PE-MASTER dispatch; NO NESTED TASKS; STATIC-ONLY — the
client never ran; zero git mutations; BASE_SHA
3644e5ac9cbf7b5445861e7f5342fb8642741346 re-verified == HEAD == origin/master ==
ls-remote before and after) applies exactly the six ordered edits and nothing
else. The human's branch-(b) order line ("zaktualizuj liczby w REPORT §3, HANDOFF,
AUDIT_ENTRYPOINT row") is completed by these edits; the AUDIT_ENTRYPOINT row itself
remains the persistence worker's job (NOT this batch's — zero touches of
AUDIT_ENTRYPOINT.md).

- **C1 — 06_REPORT/REPORT.md §3 claims-table row C3, evidence cell (line 82).** The
  historical/canonical annotation appended INSIDE the evidence cell after
  "(3643 total)" (anchor "UNRESOLVED=0 (3643 total). |" verified exactly-once by
  script before and after; the appended text carries the canonical 619 POSSIBLE /
  3022 REJECTED counts and the 0x0040525B reclassification note).
- **C2 — 06_REPORT/REPORT.md §5 negative control 5.** The classifier-discipline item
  relabeled: the 3023 REJECTED rows "historical at this run's publication; canonical
  3022 after AMEND_LOG_R2 F1", and the structural-rule list annotated with the
  historical `imm` rule (its single fired row = the mislabel; canonically
  POSSIBLE_ALIAS per F1/erratum E-2). OLD fragment verified exactly-once
  (whitespace-normalized) before; NEW exactly-once after.
- **C3 — 06_REPORT/REPORT.md §7 NOT_CHECKED bullet.** The 618 POSSIBLE_ALIAS bullet
  annotated "historical at this run's publication; 619 canonical after
  AMEND_LOG_R2 F1". OLD fragment verified exactly-once (whitespace-normalized; the
  file's continuation indent is 2 spaces while the contract fragment prints 3 — the
  applied NEW is the contract's verbatim text) before; NEW exactly-once after.
- **REPORT.md SHA256 before -> after (the whole C1+C2+C3 transition — a SECOND
  pair for REPORT.md; the section-2c pair above stays intact as the first
  transition):** 7DF5E0648B7E632F621E71F3172BE33E9D182EBF37106AAB35A4E03549F7081E ->
  DB89FA3A5E57B036B635EE0792E7600309CE76E5A5C420552C334D8CEC39F794.
- **C4a/C4b — 06_REPORT/HANDOFF.md.** C4a applied the section-2h prepared residue
  text VERBATIM; C4b applied the gates-line annotation (the counts 2/618/3023/0
  marked "historical at this run's publication", the canonical 2/619/3022/0 after
  AMEND_LOG_R2 F1 branch (b), and the note that the gates CSV and the raw/CSV
  artifacts stay byte-identical). 06_REPORT/HANDOFF.md SHA256 before -> after:
  71A2B1C127ECF4F7191BB9D8E3B3B769B2E41EAAF38137C8D6CA45610E943BC8 ->
  6555E81E0252E0A1186BD6ED02A7AF39E5A6ED5B97C5A1A13AF229E63B089B67 (also recorded in section 2h). The file moves from section 7's
  untouched list to the authorized expected-change set.
- **C6 — manifest + SCRIPT_SHA256 refresh (executed LAST, after this log's final
  wording; sequence: content edits -> this log's C5 wording -> the updater edit ->
  the SCRIPT_SHA256 refresh -> the manifest re-run).** 00_CONTROL/
  amend_r2_manifest.py edited (expected-change set extended with
  06_REPORT/HANDOFF.md; the published 32-row manifest embedded as the read-only
  comparison baseline so the amendment-total change set stays verifiable against
  the publication commit 3644e5ac9cbf7b5445861e7f5342fb8642741346 — the on-disk
  manifest already carries the R2 hashes and would mask it; final output 37 rows)
  and re-run (ONE-SHOT semantics: the DELIVERED manifest is the FINAL run's
  output; an initial run was superseded when the section-7 C1 re-assertion
  surfaced two pre-existing R2 listed-value transcription defects — recorded
  in section 7 — requiring an accuracy correction to this log's own
  section-7 C1 entry: the intermediate manifest was rolled back to the
  pre-batch state and the updater re-ran against it): every row verified
  fail-closed against disk; the
  change set vs the published package == EXACTLY {06_REPORT/REPORT.md,
  06_REPORT/QC_AUDIT_R1.md, 03_EVIDENCE/README.md, 00_CONTROL/SCRIPT_SHA256.csv,
  06_REPORT/HANDOFF.md} plus the five new-file rows already present; all other
  rows byte-identical; self-exclusion held; the final 37-data-row manifest written
  deterministically with FRESH disk hashes for every row (so this log's own
  manifest row carries its FINAL hash and the updater's row carries its post-edit
  hash). 00_CONTROL/SCRIPT_SHA256.csv: the amend_r2_manifest.py row carries the
  script's post-edit hash (the only field changed in that row; the other five rows
  byte-identical, CRLF format preserved). The final manifest's own on-disk SHA256
  is not self-recordable (the L12 regress — the same class as section 2f for this
  log itself; recording it here would change this log AFTER the manifest recorded
  its FINAL hash) — it is reported in the executor's completion-batch delivery
  notice. Final manifest rows count: **37 data rows**.

## 3. ERRATA (recorded; the historical probe/output files stay byte-identical)

- **(E-1)** 06_REPORT/QC_AUDIT_R1.md §4 C8 line 139's sampled description
  "R-IMM-STATIC 0x0040525B base=edx from fixed immediate" is SUPERSEDED — the QC
  file itself is NOT edited for this (the QC's own record stays verbatim; only the
  F3 one-character hash typo was fixed per the order's EDIT 4). The historical
  description repeated the same misreading as the executor's raw why-line. The
  canonical description (per this amendment's proof): the base register of row
  0x0040525B holds the VALUE loaded from the global pointer slot 0x00B6C3D8
  (`mov edx, dword ptr [0xb6c3d8]` @0x00405250); the direct-write channel of that
  slot is proven closed (sole writer 0x00404C9D storing the static .data address
  0x00B9FEC0); the address-taker channel is OPEN (the sole consumer stores &global
  into a linked list @0x00404BE9), and the row is canonically POSSIBLE_ALIAS
  (BRANCH (b)).
- **(E-2)** the sentence "the residue falls to POSSIBLE, never to false REJECTED"
  (06_REPORT/PE_MASTER_REVIEW.md CLAIM_MATRIX 1, line 12 — the review file stays
  verbatim) is superseded for ALL FUTURE reviews: a REJECTED row's reason must be
  STRUCTURALLY self-contained (a proven value-space/non-alias fact), never an
  unverified interprocedural assumption; a rejection resting on an unverified
  assumption belongs to POSSIBLE_ALIAS. The 0x0040525B case is the demonstrated
  instance TWICE OVER: the historical label (R-IMM-STATIC) pretended to be structural
  while the justification ("base = fixed immediate address") was factually wrong AND
  the corrected rejection (R-GLOBAL-PTR-NON-SF), attempted by this amendment, could
  not close the address-taker channel — the row's rejection WAS resting on an
  unverified assumption and NOW IS POSSIBLE_ALIAS (canonical, branch (b)).
- **(E-3)** 00_CONTROL/qc_probe/out_qc1_counters.txt line 28 "claim match
  (2/618/3023/0, total 3643): FAIL" is a SPURIOUS artifact of the qc1_counters.py:88
  predicate bug (dict(Counter) never carries the UNRESOLVED key when its count is 0,
  so `dict(cc) == CLAIM` is always False — F2, quoted verbatim in section 0). The
  counts DO match (2/618/3023/0 with 0 UNRESOLVED rows — verified by the QC's own
  recount lines 24/27 and re-verified by this amendment's P9 from the CSV). The
  historical probe files stay byte-identical.
- **(E-4)** 03_EVIDENCE/README.md's "Python 3.12.10" was a transcription error;
  canonical = `D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe`, Python
  3.12.7 (measured). Fixed by EDIT 5.

## 4. TEMPLATE FIXES for future runs/probes

- **(T-1)** the R-IMM-STATIC rule SPLIT: the sound form is base==imm32/lea[imm] (a
  fixed immediate ADDRESS in the register). A LOAD-from-absolute form
  (`mov reg, [global]`) is NOT R-IMM-STATIC — it routes to R-GLOBAL-PTR-NON-SF only
  with BOTH (i) a proven non-SF value space (sole-direct-writer census + return
  chain + SF-heap-only) AND (ii) a CLOSED address-taker channel (the sole &global
  taker's consumer neither writes [arg+0] NOR stores the arg pointer anywhere that
  could create new writers), else POSSIBLE_ALIAS. This amendment's P7(b) is the
  demonstrated necessity of clause (ii): a sole direct writer + a proven value chain
  are NOT sufficient when the pointer escapes into a data structure.
- **(T-2)** the probe claim-match predicate compares KEY-BY-KEY with .get(k, 0) —
  never dict equality against a fixed 4-key dict (E-3/F2's root cause).
- **(T-3)** the reproduction interpreter is ALWAYS cited as canonical path + measured
  version (E-4/F4's root cause).

## 5. F5 PROCESS NOTE (state-at-moment, read-only; PENDING HUMAN ADJUDICATION)

- **Inventory of docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/ (7 files,
  hashes recorded before == after, section 7; this amendment performed ZERO decodes
  of the NINODE subject matter and made ZERO changes in that package):**
  - 00_CONTROL\RUN_CONTRACT.md — 12443 bytes — SHA256
    9E0006030D078E71F4D9609371F6BA27CDEB936BA63ABD8D5EE5F9DAAEEC8882
  - 00_CONTROL\run_state.json — 7125 bytes — SHA256
    D7F7428827B459256F23A4CFEDC77D5CB8DD5B40061D4F6D52C6A1C5F7A14F65
  - 00_CONTROL\slot17_core.py — 10615 bytes — SHA256
    02D58F8B642E1952AA4E3A5A538998C1FDFEDCB17A7B798AB481ADE9AF6CAF4D
  - 00_CONTROL\slot17_run.py — 26646 bytes — SHA256
    C4802B2A1B7E1FBFF8258A993B2CB36D0707025F345B4460106D7EDA444CB2C3
  - 00_CONTROL\SOURCE_IDENTITIES.json — 2037 bytes — SHA256
    088A4EE4766B37C6B80B55643A2610F9FBA1C44C29E707A2B137DCA881F8DBB2
  - 00_CONTROL\__pycache__\slot17_core.cpython-312.pyc — 12520 bytes — SHA256
    FF8344BFC9BDA545AA466DD0A45DCFA67D377CEBDE8C8146EA79F147792D3FE9
    (the __pycache__ presence itself is a hygiene defect of that run)
  - 01_RAW\SLOT17_BODY_RAW.txt — 5577 bytes — SHA256
    2EABC45F81738039DA6C876C411301EFCE0CD0744BB6CF0077C740A455A9C2F1
- **Missing contract deliverables (verified absent on disk)**:
  02_ANALYSIS/SLOT17_FIRSTCALL_ANALYSIS.md; 03_EVIDENCE/README.md;
  06_REPORT/REPORT.md; HANDOFF.md (06_REPORT/HANDOFF.md);
  STAGE_ACCEPTANCE_GATES.csv (06_REPORT/STAGE_ACCEPTANCE_GATES.csv);
  MANIFEST_SHA256.csv (06_REPORT/MANIFEST_SHA256.csv);
  SCRIPT_SHA256.csv (00_CONTROL/SCRIPT_SHA256.csv).
- **The run_state.json technical summary (<=6 lines, per the amendment order)**:
  calibration .?AVSceneFeederObject@@ ok; NiNode walk ok; slot17=0x007B5390 ok;
  body decoded 6 insns to first call @0x007B5399 -> E8 target 0x007BF220;
  task_b prologue window decoded; rtti=null.
- **Process violation statement**: the NINODE run was dispatched+executed 2026-09-14
  ~10:54-10:59 local, BEFORE the Desktop post-audit authorization gate — the LINK30
  PE_MASTER_REVIEW said the next run is authorized by the human AFTER the Desktop
  post-audit.
- **The A/B options (quoted per the order)**: (A) retro-authorization -> complete per
  contract incl. __pycache__ removal, -B; (B) parking -> zero further decodes until
  formal GO.
- **PENDING HUMAN ADJUDICATION** — this amendment performed ZERO decodes of the
  NINODE subject matter and made ZERO changes in that package (7/7 file hashes
  before==after, recorded above and in section 7).

## 6. Determinism + counts asserts (script-measured, not hand-checked)

- 02_ANALYSIS/SF30_WRITER_CENSUS.csv: **BYTE-IDENTICAL** — SHA256
  71552E2A4BFC120DA0BE1A7E108A41A03C873ADDD238637DD7C18F3C968824D0 (before == after,
  re-hashed twice by this amendment: before the sidecar was written and after all
  edits).
- 01_RAW/SF30_WRITER_RAW.txt: **BYTE-IDENTICAL** — SHA256
  64402A73013B52943E10AE17BB115F466A0D3BEF98AA3835915CF3C1CD572248 (before == after).
- 01_RAW/SF30_RTTI_RAW.txt, 01_RAW/POSITIVE_CONTROL_0050A050.txt,
  02_ANALYSIS/SF30_PROVENANCE.md: **BYTE-IDENTICAL** (section 7 hashes).
- Counts: **historical 3643 = 2 PROVEN / 618 POSSIBLE / 3023 REJECTED / 0 UNRESOLVED**
  recomputed from the UNCHANGED CSV by the proof script (P9 PASS, UNRESOLVED via
  .get(k,0)); **canonical (after this amendment, BRANCH (b)): 3643 = 2 PROVEN /
  619 POSSIBLE / 3022 REJECTED / 0 UNRESOLVED** — exactly one row reclassified.
- 06_REPORT/STAGE_ACCEPTANCE_GATES.csv: **BYTE-IDENTICAL** — SHA256
  375798E82C80E7ED4EC388DB486A22856C9409A5A397FF10582E1D0188121968 (before == after;
  NOT regenerated; the amendment did not re-run finalize.py).
- The proof raw artifact (01_RAW/F1_GLOBALPTR_PROOF_RAW.txt) is fully generated by
  00_CONTROL/f1_globalptr_proof.py (deterministic from the physical EXE + the
  recorded git state); its reproduction line is in 03_EVIDENCE/README.md.

## 7. Untouched verification (before == after SHA256, measured after all edits except
EDIT 7 which touches only MANIFEST_SHA256.csv)

- 00_CONTROL/RUN_CONTRACT.md 7416A3C9642D4E088ABBFB5548242E1511E966C63468E12839842270810D6609
- 00_CONTROL/SOURCE_IDENTITIES.json 0F6A72721168222619BDA4BC3913D7F71E9AAC151919986E831D0015E57BB1FF
- 00_CONTROL/census_state.json D175E7919C8FA662B089E1E4EE5569EA4A606F6D315BB101AF0F7E568ADD87A3
- 00_CONTROL/census.py 7C4D705575238DDC4A27D01DCC1EA92BADE8FA0EE42D400EB2697F1D75B4723F
- 00_CONTROL/finalize.py 4DF58FBF8132168976554189EF4B758A4554D29698F72F32F5BC1CFE46C0B868
- 00_CONTROL/sf30_core.py CD6BC11F2AF482FD587BF24D6291242CAF652FB0189CEBB83B7A18A2EE42907E
- 00_CONTROL/qc_probe/ all 12 files —
  qc1_counters.py BB7FF3AD8B19A635A79C843797A3E20781AE9F3A9D5D37397BFFF5EC9338AA65,
  qc2_bytes.py DCE9091AB93877B78E39309E7B2AFD244C630BA7D31F32E5FB591C7EC6E6C98B,
  qc3_sweep.py 9AF5B188D3A21FB7A6BDAB4E2D2FD21ACFA69548FD14A8BEEC8F96F6B8601E8D,
  qc4_sample_scope.py 22E9AC4CF76625076FA7B2D5E8EA200BCC041B8A20FC15B07634A29D49B3D942,
  qc4b_scope_bytes.py 430B80CE6AB7B52D2B4F456B15B86552FD0C7D11B3FAEDE5BBB4C16270DD8959,
  qc5_final.py 2DDAD0CB40384D3D040F568E0039BE04B5752FF19AD141B56957DF5FFA56E1B0,
  out_qc1_counters.txt DFE4B37D71CDBAADDC28DBD0C422207F359C1FA1881ECFE2B0BEADAE4001E0B4,
  out_qc2_bytes.txt DB3BC4CF5C79181A4EAC01DA5FBFF5FF57598F96A9A33300A14796A3FA5D0BBE,
  out_qc3_sweep.txt 05509B777DBB9CCCE3C945B816951C487C0FC7E8D3A1E343A8E18035F3DAAA46,
  out_qc4_sample_scope.txt 6786160F8597510EAE019B930372865980ECAC40A857AA54B37A0AC612A2F466,
  out_qc4b_scope_bytes.txt 741CFF6084A5D7A8BC52AFA9B2AEC3663C96F34D9CC8CD4E0542E909F020B5A3,
  out_qc5_final.txt 71B99BC7403497FA9F7F63544FD4F8F99EFC8ED5905320481EAFB2C6A0128AC0
  (all == QC_AUDIT_R1.md §9's inventory — qc4_sample_scope.py hash now the CORRECTED
  one that §9 line 395 now displays).
- 02_ANALYSIS/SF30_WRITER_CENSUS.csv 71552E2A4BFC120DA0BE1A7E108A41A03C873ADDD238637DD7C18F3C968824D0
- 01_RAW/SF30_WRITER_RAW.txt 64402A73013B52943E10AE17BB115F466A0D3BEF98AA3835915CF3C1CD572248
- 01_RAW/SF30_RTTI_RAW.txt 399C4CFB5A83728B019D51DE805BFF2FDC2F5D753E87C909F8E0A43E8326AEE5
- 01_RAW/POSITIVE_CONTROL_0050A050.txt 4BFD3BB14BC815BD8B2B1B4D150430A40DF4E848C54EC1214C3898342CFA8D18
- 02_ANALYSIS/SF30_PROVENANCE.md A2F48326CE7B795B8B4067C6E719CBDBF0A082627A1C2B660C36D980A296452C
- 06_REPORT/STAGE_ACCEPTANCE_GATES.csv 375798E82C80E7ED4EC388DB486A22856C9409A5A397FF10582E1D0188121968
- 06_REPORT/HANDOFF.md — REMOVED from this byte-identical list by the completion
  batch C1: the section-2h prepared text (C4a) and the gates-line annotation (C4b)
  are APPLIED (PE-MASTER audit of the R2 amendment); the file is now in the
  authorized expected-change set — before->after SHA256 pair in sections 2h/2j
  (historical R2 state: 71A2B1C127ECF4F7191BB9D8E3B3B769B2E41EAAF38137C8D6CA45610E943BC8, not modified by
  the R2 amendment per the section-2h adjudication; cross-reference 2j)
- 06_REPORT/PE_MASTER_REVIEW.md 411E471701161013CE0F7B3067CD8D099248745107C17126E01C1FDA5892B7F0
- 06_REPORT/AMEND_LOG_R1.md 52B19B44C50EB924A2E7B6967EC9B26D4224959ADE02019581ACBC41D3D2AD2D
- 06_REPORT/MANIFEST_NOTE_PUBLICATION.md 6F832230769D78ED02A7A6DAF26875E548BDF559E7F8B4CC42C8781A47FD0410
- AUDIT_ENTRYPOINT.md: ZERO touches (the persistence worker applies the row edit; the
  prepared text is in section 2i).
- The NINODE package: 7/7 file hashes before==after (section 5 inventory); zero
  files created/removed (file count 7 before == after).
- experiments/: census (name + size, 23 files) before==after — foreign untracked,
  untouched.
- Repo state: HEAD == origin/master == ls-remote == BASE_SHA
  3644e5ac9cbf7b5445861e7f5342fb8642741346 at every phase (before the proof, after
  all edits); ZERO git mutations (no add/commit/push/stage; `git diff --cached` empty;
  the four on-disk modified tracked files are exactly the contract's EXPECTED-CHANGE
  set, by design — publication is a separate later step); the untracked set at the
  end = the two baseline paths + this amendment's five new package files.

- Completion batch C1 re-assertion (2026-09-14): every remaining entry above
  re-measured on disk and verified byte-identical to the PUBLICATION baseline
  (== the MANIFEST_SHA256.csv rows) for all 32 published paths (RUN_CONTRACT.md,
  SOURCE_IDENTITIES.json, census_state.json, census.py, finalize.py, sf30_core.py,
  the 12 qc_probe files, SF30_WRITER_CENSUS.csv, SF30_WRITER_RAW.txt,
  SF30_RTTI_RAW.txt, POSITIVE_CONTROL_0050A050.txt, SF30_PROVENANCE.md,
  STAGE_ACCEPTANCE_GATES.csv, PE_MASTER_REVIEW.md, AMEND_LOG_R1.md,
  MANIFEST_NOTE_PUBLICATION.md — plus AUDIT_ENTRYPOINT.md zero touches, the
  NINODE package 7/7, the experiments/ census (23 files), and the three R2-new
  files untouched by C1: 01_RAW/F1_GLOBALPTR_PROOF_RAW.txt,
  00_CONTROL/f1_globalptr_proof.py, 02_ANALYSIS/SF30_WRITER_CENSUS_SUPERSESSION_R2.md);
  06_REPORT/QC_AUDIT_R1.md and 03_EVIDENCE/README.md stay at their post-R2
  (EDIT 4 / EDIT 5) states — untouched by the C1 batch; no __pycache__ inside
  the package. RE-ASSERTION DISCOVERY (pre-existing R2 transcription defects,
  NOT file changes): TWO of the LISTED VALUES above are wrong while the FILES
  are byte-identical to publication —
  (i) 01_RAW/SF30_RTTI_RAW.txt: the listed value was an INVALID 65-hex-char
  string (the TRUE hash with one extra 'B' inserted — the defective substring
  E80B5BFF2 where the true value reads E805BFF2; script-verified: len 65 and
  != the file's true hash); TRUE hash (disk == publication baseline == manifest
  row): 399C4CFB5A83728B019D51DE805BFF2FDC2F5D753E87C909F8E0A43E8326AEE5;
  (ii) 06_REPORT/MANIFEST_NOTE_PUBLICATION.md: the listed value was the TRUE
  hash with ONE wrong character (script-verified: exactly one differing
  character, at hex position 28); TRUE hash (disk == publication baseline
  == manifest row): 6F832230769D78ED02A7A6DAF26875E548BDF559E7F8B4CC42C8781A47FD0410.
  ADJUDICATED by PE-MASTER (ACCEPTED — the F2 defect class inside this log
  itself); FIXED by micro-batch C2 (2026-09-14) with script-computed values
  asserted == the manifest rows — the two invalid literals (the 65-hex string
  and the one-char-wrong string) are REMOVED from this log: at the section-7
  listed values (C2-1) and from these discovery-note quotes (C2-2); they now
  occur ZERO times in this file (script-verified); the correction is recorded
  in section 2k. The C1 end state: the tracked-modified set == exactly
  {06_REPORT/REPORT.md, 06_REPORT/QC_AUDIT_R1.md, 03_EVIDENCE/README.md,
  00_CONTROL/SCRIPT_SHA256.csv, 06_REPORT/HANDOFF.md, 06_REPORT/MANIFEST_SHA256.csv};
  the untracked set unchanged (the two baseline paths + the five new package
  files); HEAD == origin/master == ls-remote == BASE_SHA
  3644e5ac9cbf7b5445861e7f5342fb8642741346 at every phase; ZERO git mutations;
  zero staged.

## 8. Tooling inventory

- Package content (with SCRIPT_SHA256.csv rows + manifest rows):
  00_CONTROL/f1_globalptr_proof.py (E313FAD9D78A9ABDA6919D365801996932C175D0496B0CCA077F1BFE325341D5)
  — the F1-P bounded static proof script; 00_Control/amend_r2_manifest.py
  (5A20758EC65BA6E37E185E7E759DF7297B9F134C4AEFDB34B83488A2A61CE8D4) — the bounded
  manifest updater; 01_RAW/F1_GLOBALPTR_PROOF_RAW.txt
  (C0ED7A21235305FC59F56B15C55B4DF2A2480A274F00CF33FD94C72D13254D78) — the proof raw
  evidence; 02_ANALYSIS/SF30_WRITER_CENSUS_SUPERSESSION_R2.md
  (DE3F5ED710B9A37F62FDEB7865D50262F78BC036CB2DF30CAD6A9E538FB72921) — the
  supersession sidecar; 06_REPORT/AMEND_LOG_R2.md (this log — not self-recordable).
- Temp scripts OUTSIDE the package
  (C:\Users\User\AppData\Local\Temp\opencode\sf30_amend_r2\, not package content):
  before_state.py (pre-edit state measurement: git/EXE/package/NINODE/experiments +
  F2/F3/F4 defect facts), after_state.py (post-edit verification: untouched asserts,
  NINODE 7/7, experiments census, git state, __pycache__ absence), the proof script's
  four assembly parts (proof_part1.py, proof_part2.py, proof_part2b.py, proof_part3.py,
  proof_part4.py — assembled into the package script before freezing), the
  before_state.json / after_state.json measurement records, and the two AMEND_LOG
  assembly parts (amend_part1.md, amend_part2.md — assembled into the package file).
- Hygiene: every interpreter invocation used `-B`; no `__pycache__` inside the
  package (verified absent after all runs); the proof script imported capstone 5.0.7
  only from the pinned temp path
  (C:\Users\User\AppData\Local\Temp\opencode\capstone_lib); nothing was installed.

— pe-reconstruction, amendment executor, 2026-09-14. RUN_STATUS: COMPLETE (BRANCH (b)).

## 2k. Micro-batch C2 (the two §7 hash-typo fixes)

Micro-batch C2 (contract PE_935_SCENEFEEDER_LINK30_AMEND_R2_20260914 batch C2
RETRY, 2026-09-14; executor pe-reconstruction, direct PE-MASTER dispatch;
NO_NESTED_TASKS; STATIC-ONLY — the client never ran; ZERO git mutations;
BASE_SHA 3644e5ac9cbf7b5445861e7f5342fb8642741346 re-verified == HEAD ==
origin/master == ls-remote before and after) fixes the two section-7
listed-value transcription defects recorded by the C1 RE-ASSERTION
DISCOVERY, as adjudicated by PE-MASTER (ACCEPTED — the F2 defect class
inside this log itself). This batch touches EXACTLY ONE content file
(this log) plus the manifest; every other file in the package is
byte-identical to its C1 final state (re-asserted after the batch).

- **C2-1 — the two section-7 listed values FIXED (script-computed, never
  hand-typed).**
  (i) 01_RAW/SF30_RTTI_RAW.txt: the DEFECTIVE listed value (an INVALID
  65-hex-char string: the true hash with one extra 'B' inserted — the
  substring E80B5BFF2 where the true value reads E805BFF2; script-verified
  len==65 and != the file's true hash) REPLACED BY the script-computed
  TRUE hash 399C4CFB5A83728B019D51DE805BFF2FDC2F5D753E87C909F8E0A43E8326AEE5 (64 chars;
  computed from the physical file; asserted == the MANIFEST_SHA256.csv row
  for that file).
  (ii) 06_REPORT/MANIFEST_NOTE_PUBLICATION.md: the DEFECTIVE listed value
  (the true hash with ONE wrong character — at hex position 28;
  script-verified != the file's true hash) REPLACED BY the script-computed
  TRUE hash 6F832230769D78ED02A7A6DAF26875E548BDF559E7F8B4CC42C8781A47FD0410 (computed
  from the physical file; asserted == the MANIFEST_SHA256.csv row for that
  file). The invalid literals are NOT reproduced in this record (the
  zero-occurrence end state required by the batch; the signatures above
  re-derive them exactly).
- **EXACTLY-ONCE anchor deviation (script-measured, recorded non-silent).**
  The C2 contract asserted each defective string occurs EXACTLY ONCE in
  this file before the fix; script measurement found each occurring TWICE
  — at the section-7 listed value AND inside the section-7 C1 re-assertion
  discovery-note quotes of those values. Both occurrences of each string
  were eliminated (C2-1 at the listed values; the C2-2 note rewrite at the
  quotes): after this batch each defective string occurs ZERO times in
  this file (script-verified). No other line of this log changed
  (line-diff verified; the count-consistency strings untouched).
- **C2-2 — the discovery note updated.** The note's conclusion (the
  defective strings "stay VERBATIM above ... flagged for PE-MASTER
  adjudication") is replaced by the adjudicated state: ADJUDICATED by
  PE-MASTER (ACCEPTED — the F2 defect class inside this log itself); FIXED
  by micro-batch C2 with script-computed values asserted == the manifest
  rows. The note's (i)/(ii) clauses are rewritten to describe the defects
  WITHOUT reproducing the invalid literals (the discovery record's
  substance — the file names, the defect signatures, the true hashes — is
  preserved; only the invalid literals are gone).
- **This log's SHA256 across this batch (before -> after the two section-7
  content fixes): 838784B95ADA3EE861FFA25CD9167267AA96BA8B4CD5625A857DF942D7E4933A ->
  ADCAD75580680FAD7620F829408F13E3DB3ACAC2B9653BA1E1BE2904DAEAA1F2** (before == the verified
  post-C1 disk state this batch started from; after == the state produced
  by the C2-1/C2-2 content fixes, i.e. the state to which this section 2k
  appends). This log's FINAL hash (including this section) is not
  self-recordable here (the fixpoint regress — the same class as section
  2f / the updater's L12); it is carried by the refreshed
  MANIFEST_SHA256.csv row for 06_REPORT/AMEND_LOG_R2.md (C2-4) and reported
  in the executor's handoff.
- **Script-computed-value rule.** Every hash string C2 wrote into this log
  was computed by script from the physical file (never hand-typed) and
  asserted == the corresponding MANIFEST_SHA256.csv row before writing;
  the same rule binds every future value-carrying edit of this package.
- **C2-4 manifest refresh note (executed LAST, after this log's final
  wording).** 00_CONTROL/amend_r2_manifest.py re-runs UNCHANGED (not
  edited; its SCRIPT_SHA256.csv row stays
  b2b4d1b09b7a2a0b5650fffd4a55af1c737fc1e67448269b49f2a09a8a103754). The pre-batch
  manifest (on-disk SHA256 8959c6952e5b59f4b66629ef0307dbc2340c797992f744bbd90a6aa404f46948) is the
  input. ONE-SHOT DISCOVERY (script-measured, non-silent): the unchanged
  updater's new-row assert requires its OWN row's disk hash to differ
  from its manifest row — TRUE for the C1 batch (the script was edited
  there) but FALSE for C2 (the script is unchanged and its manifest row
  already equals its disk hash), so the literal re-run against the
  pre-batch manifest fails fail-closed by design (observed: an
  AssertionError before any write). Resolution by the C1 batch's own
  recorded method (section 2j C6: "the intermediate manifest was rolled
  back to the pre-batch state and the updater re-ran against it"): the
  INPUT manifest is rolled back ONE ROW — its own row reset to the
  pre-C1 value (the R2-edition script hash
  5A20758EC65BA6E37E185E7E759DF7297B9F134C4AEFDB34B83488A2A61CE8D4, recorded in section 8 and in
  the updater's own header comment) — and the updater re-runs UNCHANGED
  with every assert passing; the deterministic output then refreshes
  every row from disk: the ONLY row whose hash changes is
  06_REPORT/AMEND_LOG_R2.md (its post-C2 hash); the other 36 rows
  byte-identical to the pre-batch manifest; self-exclusion held; still 37
  data rows. The final manifest's own on-disk SHA256 is not recorded
  here (the self-recording regress) — it is reported in the executor's
  handoff.

— pe-reconstruction, micro-batch C2 executor, 2026-09-14. C2 RUN_STATUS:
reported in the C2 handoff (this section was finalized before the C2-4
manifest refresh ran; the refresh evidence is in the handoff).
