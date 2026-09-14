# QC_AUDIT_R2.md — PE_935_SCENEFEEDER_LINK30_AMEND_R2_20260914 (INTERNAL_QC, round R2)

RUN_ID: PE_935_SCENEFEEDER_LINK30_AMEND_R2_20260914 · Era: PCG_9_3_5 · STATIC-ONLY
(the client NEVER ran; no process of any game binary was launched by this QC either;
byte-reading scripts only) · INTERNAL_QC round R2 (fresh context, independent of the
execution; the executor was pe-reconstruction — R2 main + completion batch C1 +
micro-batch C2).

- QC_RUN: fresh-context INTERNAL_QC by pe-master-auditor. I did NOT execute any of the
  amendment's scripts (independence rule): 00_CONTROL/f1_globalptr_proof.py,
  amend_r2_manifest.py, census.py, finalize.py were READ to EOF but never imported or
  run. Every binary fact below was re-derived by MY OWN minimal PE parser + MY OWN
  capstone 5.0.7 sweep (capstone from the pinned path
  `C:\Users\User\AppData\Local\Temp\opencode\capstone_lib`; interpreter
  `D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe`, Python 3.12.7,
  every invocation `-B`). My probes live OUTSIDE the package under
  `C:\Users\User\AppData\Local\Temp\opencode\sf30_qc_r2\` (inventory in §14).
- QC date: 2026-09-14. ZERO git mutations by this QC (verified before and after; my
  ONLY write is THIS file — a new untracked path, outside the executor manifest by the
  established QC convention; the 37-row manifest is NOT touched and its self-exclusion
  convention stays intact).
- Skill/context loaded: pe-master-audit (v2, D:\TESTAI\.opencode\skills\pe-master-audit),
  AGENTS.md, AUDIT_ENTRYPOINT.md, 00_PROJECT_CONTEXT/PE_MASTER_ACTIVE_ORDER.md,
  AMEND_LOG_R1.md, PE_MASTER_REVIEW.md, QC_AUDIT_R1.md (full context for the published
  R1 package this amendment modifies).

---

## 1. S0 — identity/base (my own measurements)

| item | result |
|---|---|
| Entropia.exe SHA256 | `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` == pin (my own hash) |
| Entropia.exe size | 8015872 == pin |
| PE facts (own header walk) | machine 0x014C, opt_magic 0x010B, image_base 0x00400000, DLLCHARACTERISTICS 0x0000 (no ASLR); sections .text 0x00401000..0x00A75000 (vsize 0x6735E5, rsize 0x674000), .rdata 0x00A75000..0x00B6C000, .data 0x00B6C000..0x00BA96E4 (rsize 0x34000, file-backed end 0x00BA0000), .tls, .rsrc |
| HEAD == origin/master == ls-remote | `3644e5ac9cbf7b5445861e7f5342fb8642741346` == BASE_SHA pin, all three (ls-remote verified against the actual remote URL; the bare `git ls-remote origin` alias fails on this host — the URL form works and was used) |
| git status (raw porcelain, 13 lines) | exactly 6 worktree-modified ` M` (REPORT.md, QC_AUDIT_R1.md, README.md, SCRIPT_SHA256.csv, HANDOFF.md, MANIFEST_SHA256.csv — all six inside PKG, byte-for-byte the contract's set) + 7 untracked `??` (the two baseline paths `PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/`, `experiments/` + the 5 new package files) |
| staged | **0** — `git diff --cached` empty (verified raw, not via any stripping wrapper) |
| __pycache__ / *.pyc inside PKG | 0 (full recursive walk) |
| NINODE package | 7 files — every size+SHA256 re-hashed fresh, **7/7 == AMEND_LOG_R2 §5 inventory** (incl. the `__pycache__\slot17_core.cpython-312.pyc` hygiene-defect entry); file count 7 before==after; zero interaction by the amendment (read-only) |
| experiments/ | 23 files, name+size census taken read-only (eu1030/ JS suite + demo + test fixtures — foreign untracked, untouched) |

**S0 = PASS.** The tracked-modified set and untracked set are EXACTLY the dispatch's
expected census; zero staged; no pycache; the NINODE/experiments baselines untouched.

Note on my own instrument (L09/L23 discipline, disclosed): my probe's first
`git status` parse produced one spurious "staged entry" because my helper's
`.strip()` ate the leading space of the first porcelain line (" M SCRIPT_SHA256.csv").
I re-measured RAW (no strip) + `git diff --cached` before issuing any finding: the
raw porcelain shows all six as ` M` (worktree-modified), index column clean. The
defective measurement is corrected and nothing below rests on it. (Two further
probe-internal defects — a path case-typo in an expectation list and two
line-wrap-fragment assumptions — are likewise corrected; the corrected results are
what this report records.)

## 2. The F1-P proof — independent re-derivation from the physical EXE (task 2)

My own full-.text linear sweep (0x00401000..0x00A75000, restart-at-next-byte):
**2,266,698 instructions decoded, 64 restarts — identical to the amendment raw's
recorded facts**, and my 64 restart VAs are LIST-IDENTICAL to the raw artifact's list
(64/64, same order). This is a fully independent sweep implementation reproducing the
same stream.

**(a) The candidate window — CONFIRMED.** My boundary-aligned decode:
`0x00405250  8b15d8c3b600  mov edx, dword ptr [0xb6c3d8]`;
`0x00405256  68304c4000  push 0x404c30`;
`0x0040525B  895a30  mov dword ptr [edx + 0x30], ebx` (WRITE [edx+0x30]).
Boundary stream: 0x405250+6==0x405256 and 0x405256+5==0x40525B. All three appear in my
sweep stream as instruction STARTS with the pin bytes. Instructions starting in the
open interval (0x405250, 0x40525B): **exactly 1 — the push — and it does NOT define
edx**. No edx definition exists in the interval. CONFIRMED.

**(b) The [0x00B6C3D8] mem-operand census — CONFIRMED, item-set-identical to the raw.**
My census (mem operands base==0, index==0, disp==0x00B6C3D8 over the full sweep):
**179 total = EXACTLY 1 WRITE @0x00404C9D (`a3d8c3b600`, `mov dword ptr [0xb6c3d8], eax`)
+ 178 READs; RMW 0; unknown-access 0.** Cross-check against
01_RAW/F1_GLOBALPTR_PROOF_RAW.txt §P3: parsed 179 items; **set difference mine−raw:
NONE; raw−mine: NONE; per-item mismatches (VA/access/bytes/mnemonic): 0 of 179.**
The raw's list and my census are the same 179 instructions to the byte.

**Adversarial extra (my own addition, beyond the amendment's scope):** whole-FILE raw
dword census of the value 0x00B6C3D8: **180 occurrences, ALL inside .text**, each
accounted for as a census item's disp bytes (VA+1 of each of the 179 items, e.g. file
offset 0x4C9E == the write's disp at 0x00404C9D+1) plus the push imm @0x00404C90+1.
There is **NO &global taker outside .text** — no .data/.rdata pointer variable holds
the slot's address. This CONFIRMS the "sole address-taker" claim at a level STRONGER
than the amendment's .text IMM-operand census (which I also reproduce below).

**(c) E8/dword census — CONFIRMED.** E8 rel32 calls in .text targeting 0x00409080:
**exactly 1 @0x00404C8B** (`e8f0430000`). Raw dword 0x00409080 occurrences in the
whole file: **0**. (Also re-derived: E8 calls to FUN_00404B60 == {0x00404CA2,
0x005B3C82} — identical to the raw's recorded facts.)

**(d) FUN_00409080 entry→ret — CONFIRMED (chain substance), and the §1 P5-mismatch
documentation is accurate as far as it goes.** My decode: 55 instructions, ZERO bad
bytes; the esi capture `mov esi, ecx` @0x004090A5 (`8bf1`) is the only mov-form esi
definition; **no esi redefinition in (0x4090A5, 0x409142)**; `pop esi` @0x00409150 is
AFTER the eax capture — so the AMEND_LOG_R2 §1 statement "no esi redefinition between
0x004090A5 and the eax capture @0x00409142 (the pop esi is AFTER the capture and does
not affect the return value)" is **byte-verified TRUE**, and its measured detail
"esi definitions in body = 2" (mov @0x4090A5 + pop @0x409150) is exact. Entry ecx is
unmodified to 0x4090A5 (12 instructions, no calls — verified). Last eax definition:
`mov eax, esi` @0x00409142 (`8bc6`) — followed ONLY by the SEH-restore epilogue
(0x409144 mov ecx,[esp+0x14]; 0x409148 mov fs:[0],ecx; 0x40914F pop ecx;
0x409150 pop esi; 0x409151 pop ebx; 0x409152 add esp,0x14) and **`ret 4` @0x00409155
(bytes C2 04 00)**. **ZERO writes to [esi]/[esi+0]** in the body (no vtable store —
non-polymorphic; the HARD-STOP branch could not fire). Everything substantive in the
AMEND_LOG §1 P5 record is confirmed. (The tail sub-predicate's additional literal-pin
failures are P3-1 below; they do not touch the substance.)

**(e) The value chain — CONFIRMED.** `0x00404C86  b9c0feb900  mov ecx, 0xb9fec0`
ends exactly at `0x00404C8B e8f0430000 call 0x409080` (imm == 0x00B9FEC0); between
call-end and the store @0x00404C9D there are exactly `push 0xb6c3d8` @0x00404C90
(`68d8c3b600`) + `mov dword ptr [esp+0x14], 0xffffffff` @0x00404C95
(`c7442414ffffffff`) — **NEITHER defines eax**. The store
`0x00404C9D a3d8c3b600 mov dword ptr [0xb6c3d8], eax` therefore stores
FUN_00409080's return == its `this` == 0x00B9FEC0.

**(f) At-rest data — CONFIRMED.** 0x00B9FEC0 and 0x00B6C3D8 both lie in .data
(va_start 0x00B6C000), inside the file-backed region (raw end 0x00BA0000). My own
VA→offset read: [0x00B9FEC0..0x00B9FF20] = **25 dwords, ALL ZERO**;
[0x00B6C3D8] at rest == **0x00000000**.

**(g) THE BRANCH-DECIDER — CONFIRMED in full.**
- IMM-operand census of 0x00B6C3D8 in .text: **exactly 1** — `push 0xb6c3d8`
  @0x00404C90 (`68d8c3b600`). (Plus my raw-dword strengthening in (b): no other taker
  exists anywhere in the file.)
- Stack arithmetic — MY OWN esp simulation: callee prologue delta before the first
  [esp+0x20] access P = +28 (push -1; push 0x9932e8; push eax; sub esp,8; push esi;
  push eax; push 0x4028f0; push 0xb9febc; add esp,8 ⇒ +28 at the first [esp+0x20]
  access, window index 27); caller-side D = +0 (only the two esp-neutral instructions
  between the &global push and the call); **4 (retaddr) + 0 + 28 == 0x20 ✓**.
- My SUPPLEMENTARY arg-count proof (my own addition, not in the amendment's pins): the
  caller's cleanup right after the call @0x00404CA2 is **`add esp, 4` @0x00404CA7
  (`83c404`)** — FUN_00404B60 took EXACTLY ONE stack argument (the &global push);
  and FUN_00404B60 itself ends with plain `ret` (`c3`) @0x00404C27 (callee cleans
  nothing). All three intermediate callees end their first `ret` with the plain form
  (0x004023C0 `c3` @47 insns; 0x00402880 `c3` @24; 0x00404810 `c3` @32) — **esp-neutral,
  validating the simulation's call assumption**. The arg at [esp+0x20] is &global on
  every ground available.
- The arg load: `mov edx, dword ptr [esp + 0x20]` @0x00404BC5 (`8b542420`) — the only
  arg-slot load (arg regs == {edx}; no first-level copies). Census (a) WRITE
  mem-operands [argreg+0]: **1 — `lock xadd dword ptr [edx], eax` @0x00404C00
  (`f00fc102`)**, and it is a REGISTER-REUSE FALSE POSITIVE exactly as the amendment
  says: `mov ecx, dword ptr [esp + 8]` @0x00404BF5 (`8b4c2408`) then
  **`mov edx, ecx` @0x00404BFE (`8bd1`)** redefine edx immediately before the xadd,
  so edx there holds [esp+8], not the arg. Census (b) stores of the arg register to
  memory: **1 — REAL: `mov dword ptr [ecx], edx` @0x00404BE9 (`89 11`)**. Between the
  arg load @0x00404BC5 and the store @0x00404BE9 there is **NO edx redefinition on ANY
  path in the window** — my path-insensitive scan finds zero edx writers in
  (0x404BC5, 0x404BE9); the intervening instructions write only eax/ecx/esi/flags
  (verified). The expected list-node observations are present:
  read [arg+8] @0x00404BD3 (`3b7208`, `cmp esi, dword ptr [edx + 8]`) and write
  [arg+0xc] @0x00404BE6 (`89420c`). **The &global pointer demonstrably escapes into a
  list link slot @0x00404BE9.** All of P7's facts are independently reproduced.

**(h) SF-always-heap — CONFIRMED.** Sweep census of imm32 0x00A7D458: **exactly 2** —
`0x00509366  c7450058d4a700  mov dword ptr [ebp], 0xa7d458` and
`0x0050A269  c70658d4a700  mov dword ptr [esi], 0xa7d458` (both true-start WRITE
stores); whole-file raw dword 0x00A7D458 == 2 at exactly the imm positions
0x00509369 / 0x0050A26B (file offsets 0x109369 / 0x10A26B). Whole-file raw dword
0x00509330 == **0**. SF ctor E8 callers == exactly **{0x0047D043, 0x0052480F}**.
FUN_005247C0 window (my decode to the CC-pad body end @0x00524858, 49 instructions,
0 restarts): `push 0x98` @0x005247E7 (`6898000000`) — exactly 1;
`call 0x95d3c4` @0x005247EC (`e8d38b4300`) — exactly 1; ctor call
`0x0052480F e81c4bfeff call 0x509330` — exactly 1; order push < new-call < ctor ✓.

**(i) The UNCHANGED CSV/raw recounts — CONFIRMED.** My own parse of
02_ANALYSIS/SF30_WRITER_CENSUS.csv: **3643 data rows; counts
{PROVEN_SF30_WRITER: 2, POSSIBLE_ALIAS: 618, REJECTED_ALIAS: 3023, UNRESOLVED: 0}** —
exact. Row 0x0040525B present, classification **REJECTED_ALIAS** in the historical
artifact, full row
`0x0040525B,0x00405150,"mov dword ptr [edx + 0x30], ebx",ebx,static data address,REJECTED_ALIAS`.
The sidecar's "CSV row 18" quote is **byte-exact verbatim** — the row IS file line 18
(header = line 1; the file-line counting convention), verified against the physical
file. The sidecar's "raw why-line" quote == SF30_WRITER_RAW.txt line 320 byte-exact
(`why: R-IMM-STATIC: base==edx = fixed immediate address (edx, dword ptr [0xb6c3d8] @
00405250); SF proven always-heap ...`). My own fired-reason recount from ALL raw
why-lines: **R-ESP 2765 / R-STACK-PTR 129 / R-CTOR-OTHER 104 / R-ZERO 18 /
R-LEA-STACK 3 / R-EBP-INHERITED 2 / R-IMM-STATIC 1 / R-CONT-FIELD 1 = 3023** —
identical to the census repeated in REPORT/sidecar/AMEND_LOG (R-EBP-FRAME 0).

### 2.1 Branch-(b) adjudication (my explicit verdict)

**VERDICT: the BRANCH (b) decision is SOUND.** Reasoning, from my own bytes:

1. The corrected rejection R-GLOBAL-PTR-NON-SF requires the global slot's VALUE SPACE
   to exclude any heap-only SceneFeederObject pointer. The direct write channel is
   provably closed: the sole direct writer is 0x00404C9D, storing FUN_00409080's
   return == its `this` == 0x00B9FEC0 (a static .data address, at-rest zero,
   non-polymorphic — no vtable store in the body, zero [esi] writes — and entry ecx
   == the static address, never an argument), so the direct channel's value space is
   {0x00000000, 0x00B9FEC0}. SF is always-heap (exactly 2 vtable imm stores; ctor
   callers {0x47D043, 0x52480F}; both creation paths operator new(0x98)→ctor).
   IF that were the whole channel closure, REJECTED would stand.
2. But the ADDRESS-TAKER channel is open: the sole &global taker anywhere in the file
   (push @0x00404C90 — my raw-dword census found NO other taker, so this is not merely
   "the sole in .text" but the sole in the whole file) passes &global as the single
   stack argument to FUN_00404B60 (arg position proven twice: the [esp+0x20]
   arithmetic AND my supplementary add-esp,4 caller-cleanup proof), and FUN_00404B60
   inserts that pointer into a linked list (`mov [ecx], edx` @0x00404BE9 with
   edx==arg, no intervening edx redefinition; node layout +8 key / +0xc next observed
   at 0x404BD3/0x404BE6). A write through a list-derived pointer to the node's +0
   field — the +0 field IS the global slot — is NOT excludable within this amendment's
   static decode bounds (excluding it would require enumerating every consumer of that
   list: interprocedural closure, explicitly out of scope). The path-insensitive
   census (a) hit is a verified register-reuse false positive (edx := ecx := [esp+8]
   @0x404BFE) and does not close anything.
3. The pre-registered rule (AMEND_LOG_R2 T-1) requires BOTH (i) the proven value
   space AND (ii) a CLOSED address-taker channel for R-GLOBAL-PTR-NON-SF; clause (ii)
   fails, so the row's rejection "would rest on the unverified assumption that no
   list-derived write ever reaches the global slot" — exactly the E-2 principle (a
   REJECTED row's reason must be structurally self-contained). The row therefore falls
   to POSSIBLE_ALIAS per the pre-registered branch (b). Canonical counts follow
   arithmetically: 3643 = 2 + 619 + 3022 + 0 (sum verified), exactly one row
   reclassified, historical artifacts byte-identical (hashes verified, §4).

The decision is conservative (it can only widen, never narrow, the alias residue),
the proof record is honest (P7 recorded as MISMATCH with the failures listed, the
false positive analyzed rather than hidden), and every load-bearing fact in it is
independently reproduced by my own decoder.

## 3. The edits — verification from disk (task 3)

**EDIT 4 (QC_AUDIT_R1.md, F3).** Published state (git show HEAD:)
SHA256 `B80DD10B42F9A40EC1E211CF3DD508D4206B35017B3E3F64370AAC338EF6040A` == the §2a
before-pin; current disk `6378165ED945113A9B252F4E5FB650236C220553FCFC2664017076F427FFC632`
== the §2a after-pin. Byte-diff published vs current: **EXACTLY ONE differing byte,
offset 28048, 0x32 '2' → 0x37 '7'**. The published qc4 hash string was
`22E9AC4CF76625026FA7B2D5E8EA200BCC041B8A20FC15B07634A29D49B3D942`; the corrected
string is `22E9AC4CF76625076FA7B2D5E8EA200BCC041B8A20FC15B07634A29D49B3D942` == my
fresh SHA256 of qc_probe/qc4_sample_scope.py == the manifest row. Wrong string occurs
0 times in the current file; correct string exactly once. The differing hex position
is index 15 (0-based) = **the 16th hex character** — my measurement CONFIRMS the
AMEND_LOG's deviation note (the order text said "17th"; the measured position is the
16th; the unambiguous OLD/NEW strings were applied). **EDIT 4 fully CONFIRMED.**

**EDIT 5 (README.md, F4).** The published README's interpreter line read
"Interpreter: Python 3.12.10 (Windows host)..." — at file line 32 of the published
state (I verified the line-shift arithmetic: the 5 appended artifact-map rows sit
above it, so the paragraph is at line 37 today; the §0 F4 citation "line 32" refers to
the pre-edit file — correct). The current line carries the canonical interpreter path
+ "Python 3.12.7 (canonical reproduction interpreter; version re-measured in-run —
the prior \"3.12.10\" was a transcription error, erratum AMEND_LOG_R2 F4)" (the only
remaining "3.12.10" on disk is inside the erratum note itself — correct). I
re-measured `python.exe --version` == Python 3.12.7. All 5 artifact-map rows present
exactly once (AMEND_LOG_R2.md; f1_globalptr_proof.py; F1_GLOBALPTR_PROOF_RAW.txt;
SF30_WRITER_CENSUS_SUPERSESSION_R2.md; amend_r2_manifest.py — casing consistent with
the real path), and the reproduce line
`python -B 00_CONTROL/f1_globalptr_proof.py  # regenerates 01_RAW/F1_GLOBALPTR_PROOF_RAW.txt`
present exactly once. Current README hash == manifest row (187BDCD7...).
**EDIT 5 fully CONFIRMED.**

**EDIT 1 (REPORT.md §3 bound paragraph, branch-(b) form).** All fragments verified
present exactly once: "619 of 3643 candidates are classified **POSSIBLE_ALIAS**
(canonical after AMEND_LOG_R2 F1; historical row count 618)"; "3022 rows are
REJECTED_ALIAS (canonical after AMEND_LOG_R2 F1; historical row count 3023)"; the
fired-reason census relabeled "= 3023 (historical)"; the full branch-(b) supersession
parenthetical (load-from-global @0x00405250 bytes 8B 15 D8 C3 B6 00; the direct
channel proven closed — sole writer 0x00404C9D storing FUN_00409080's return = its
`this` = 0x00B9FEC0, static .data, non-polymorphic, slot at rest 0; the
address-taker channel OPEN — FUN_00404B60 stores &global into a linked list
@0x00404BE9; reclassification REJECTED_ALIAS -> POSSIBLE_ALIAS; canonical counts
3643 = 2/619/3022/0; the historical CSV/RAW byte-identical; pointers to AMEND_LOG_R2
and the sidecar). Every binary claim inside that parenthetical is one I re-derived
independently in §2 above — all TRUE. Published REPORT == E08A5875... (§2c
before-pin, git-verified); the post-EDIT-1 intermediate == 7DF5E064... (verified
against the executor's C1-batch before-copy, hash-identical); current ==
DB89FA3A5E57B036B635EE0792E7600309CE76E5A5C420552C334D8CEC39F794 == the §2j C1..C3
after-pin == the manifest row. **EDIT 1 (with the C1..C3 annotations) fully
CONFIRMED.**

**C1/C2/C3 (REPORT annotations).** The C3 claims-row annotation inside the evidence
cell (anchor "(3643 total). |" — the appended text carries canonical 619/3022 + the
0x0040525B reclassification note) present exactly once; §5 negative-control #5
carries "the 3023 REJECTED rows (historical at this run's publication; canonical
3022 after AMEND_LOG_R2 F1)" + the historical `imm`-rule qualification ("whose single
fired row proved a mislabel and is canonically POSSIBLE_ALIAS per AMEND_LOG_R2
F1/erratum E-2"); §7 carries "The 618 POSSIBLE_ALIAS rows (historical at this run's
publication; 619 canonical after AMEND_LOG_R2 F1)". All verified present.
**CONFIRMED.**

**§4 gates table (adjudication — acceptable as an artifact-scoped mirror).** The §4
table header scopes it: "(06_REPORT/STAGE_ACCEPTANCE_GATES.csv; all recomputed by
finalize.py)"; its G2 row mirrors the gates CSV's raw-evidence text
"raw==CSV==state-json counts (2/618/3023/0)". My adjudication: **acceptable.**
Reasons: (1) the mirrored artifact (STAGE_ACCEPTANCE_GATES.csv, hash 375798E8...) is
byte-identical to publication and its counts are TRUE of the unchanged
CSV/raw/state-json artifacts on disk (I re-parsed all three: they ARE 2/618/3023/0 —
so the mirror asserts no falsehood); (2) REPORT §3, in the same document immediately
above, carries the prominent canonical annotations (619/3022 + reclassification), so
no reader can take 618/3023 as the current canonical state from this file;
(3) the amendment deliberately did not regenerate the gates CSV (finalize.py NOT
re-run; regenerating would have re-executed historical gate machinery), and annotating
the mirror without regenerating would desynchronize mirror and mirrored artifact.
The mirror stays a faithful historical record. Residual note: a reader who reads ONLY
the §4 table could misread — P3-2 records the wording recommendation (annotate the
§4 header "(historical mirror)" in any future regeneration). Verdict: acceptable; not
a defect requiring correction now.

**C4a/C4b (HANDOFF.md).** The residue block (lines 17-20) is **byte-exact identical**
to the AMEND_LOG_R2 §2h "PREPARED replacement" text (compared programmatically,
backtick wrappers stripped — all four lines byte-for-byte). The §2h "current HANDOFF.md
lines 17-18" old-quote matches the PUBLISHED HANDOFF lines 17-18 exactly
(`  (residue: 3023 REJECTED_ALIAS with per-row reasons; 618 POSSIBLE_ALIAS = the` /
`   documented static bound; 0 UNRESOLVED)`). The C4b gates-line annotation is present:
"COUNTER_ARITHMETIC holds: raw file == CSV == state json == 3643 with counts
2/618/3023/0 — historical at this run's publication; canonical 2/619/3022/0 after
AMEND_LOG_R2 F1 branch (b); the gates CSV and the raw/CSV artifacts stay
byte-identical". HANDOFF before==published (71A2B1C1...) and current ==
6555E81E... == the §2h/§2j after-pin == the manifest row. **CONFIRMED.**

**HANDOFF NOT_CHECKED "the 618 POSSIBLE_ALIAS rows" (adjudication).** This is the
short-form NOT_CHECKED list (schema field "NOT_CHECKED (short)") enumerating what the
R1 RUN did not examine — a run-scope statement, historically true of the run's
publication state (then 618). It is contextualized by the same file's residue line
(canonical 619 / historical 618/3023) and gates-line annotation (canonical
2/619/3022/0). The physical row set referenced is the same ±1 reclassified row. My
verdict: **acceptable as a run-scope statement** — it does not assert a canonical
count, and the file's canonical annotations govern; a "(historical)" qualifier in a
future regeneration would make it perfect (P3-2). Not a defect.

**EDIT 2 (sidecar).** SHA256 DE3F5ED7... == manifest row == fresh hash. The
superseded CSV row quote == file line 18 byte-exact (see §2(i)); the superseded raw
why-line == line 320 byte-exact; the canonical supersession statement's every binary
claim re-derived TRUE in §2; canonical/historical counts present and arithmetic-correct
(2/618/3023/0 historical; 2/619/3022/0 canonical); the CSV/RAW pins
(71552E2A... / 64402A73...) == fresh hashes; the REGENERATION PROHIBITION present.
**CONFIRMED.**

**EDIT 3/§0-§8 + §2h APPLIED + §2j + §2k (AMEND_LOG_R2.md).** All section headers
present (§0..§8, 2h with the APPLIED marker + the C1 authorization record, 2i
prepared-not-applied entrypoint text, 2j, 2k); E-1..E-4 present; T-1..T-3 present;
§5 carries the 7-file inventory (all 7 re-hashed fresh, MATCHES), the
missing-deliverables list (all verified absent on disk — the NINODE package contains
only its 7 files: 00_CONTROL×6 + 01_RAW×1, no 02_ANALYSIS/03_EVIDENCE/06_REPORT), the
A/B options, and PENDING HUMAN ADJUDICATION. §7's two fixed hash strings == my fresh
hashes (SF30_RTTI_RAW.txt 399C4CFB...; MANIFEST_NOTE_PUBLICATION.md 6F832230...).
Hex-string census: 79 long hex strings = 6×40-char (git SHAs) + 73×64-char, **ZERO
invalid-length strings**. Both C2-eliminated defective literals occur ZERO times in
the current log (verified directly — for the RTTI 65-hex string by reconstruction
from the §2k signature, for the MANIFEST_NOTE one-char-wrong string by recovery from
the pre-C1 before-copy, see §6). Current AMEND_LOG_R2.md hash
`C6905FE488CE66CCFDA0178742C611FF84716C592F39BBA93D3F2F131EF63928` == the manifest
row (the C2-4 refresh end state is consistent — the log has not changed since the
refresh). **CONFIRMED.**

**EDIT 6/EDIT 7 + C6 (SCRIPT_SHA256.csv + MANIFEST_SHA256.csv).**
SCRIPT_SHA256.csv: CRLF preserved, header + **6 data rows**; every row == my fresh
hash (sf30_core.py CD6BC11F..., census.py 7C4D7055..., finalize.py 4DF58FBF...,
census_state.json D175E791..., f1_globalptr_proof.py E313FAD9...,
amend_r2_manifest.py B2B4D1B0... == my fresh hash of the script == the manifest row;
the §2d-added R2-edition row 5A20758E... was superseded by the C6 refresh to the
post-edit hash, exactly as §2j/§2k document — and 5A20758E... is still correctly cited
3× as the historical R2-edition/pre-C1 value, verified against the executor's
pre-C1 before-copy of the script which hashes to exactly 5A20758E...).
Published SCRIPT_SHA256 == 0C2DE0B2... (§2d before-pin, git-verified); the post-EDIT-6
intermediate == 73F7657F... (verified against the C1-batch before-copy). Current ==
b38d32d9... == the manifest row for it.
MANIFEST_SHA256.csv: CRLF, trailing CRLF, header + **37 data rows**; **EVERY row == my
fresh disk hash — 37/37, zero mismatches**; self-exclusion held (the manifest is not
a row; package census 38 files == 37 rows + manifest); the AMEND_LOG_R2 row ==
current file hash; the row set == the 32 published paths + the 5 new files; the
change set vs publication == exactly the 5 authorized tracked files (the updater's
embedded PUBLISHED_BASELINE is byte-faithful: all 32 rows == git show HEAD:'s manifest,
zero mismatches, zero extra keys — I verified the whole dict). **CONFIRMED.**

## 4. Untouched verification (task 5) — all re-hashed fresh

- AMEND_LOG_R2 §7 list: **27/27 == the listed values** (RUN_CONTRACT.md,
  SOURCE_IDENTITIES.json, census_state.json, census.py, finalize.py, sf30_core.py,
  all 12 qc_probe files, SF30_WRITER_CENSUS.csv 71552E2A..., SF30_WRITER_RAW.txt
  64402A73..., SF30_RTTI_RAW.txt 399C4CFB..., POSITIVE_CONTROL_0050A050.txt
  4BFD3BB1..., SF30_PROVENANCE.md A2F48326..., STAGE_ACCEPTANCE_GATES.csv
  375798E8..., PE_MASTER_REVIEW.md 411E4717..., AMEND_LOG_R1.md 52B19B44...,
  MANIFEST_NOTE_PUBLICATION.md 6F832230...).
- The 3 R2-new files untouched by C1: F1_GLOBALPTR_PROOF_RAW.txt C0ED7A21...,
  f1_globalptr_proof.py E313FAD9..., sidecar DE3F5ED7... — all == fresh. ✓
- QC_AUDIT_R1.md == its post-R2 EDIT-4 state (6378165E...), untouched by C1/C2. ✓
- AUDIT_ENTRYPOINT.md: ZERO touches (not in the modified set; the §2i prepared row is
  correctly NOT applied — it is the persistence worker's job). ✓
- NINODE 7/7 (§1) ✓; experiments/ 23-file census ✓; no __pycache__ ✓.
- Historical publication states (git): REPORT E08A5875..., README FDBE55B8...,
  SCRIPT_SHA256 0C2DE0B2..., QC_AUDIT_R1 B80DD10B..., HANDOFF 71A2B1C1... — all ==
  the AMEND_LOG's before-pins. ✓

## 5. Count-consistency census (task 4)

Whole-package whitespace-normalized scan (all 38 files) for 618/3023/619/3022:
**word-bounded token hits: 618 × 63, 3023 × 59, 619 × 18, 3022 × 19; plus 154
longer-token substring hits (hash/VA/byte-string fragments — e.g. the SOURCE_IDENTITIES
hash `0f6a72...2619bd...` contains "619"; VAs 0x004A0619, 0x0056184F; opcode byte
strings like `894618` in SF30_WRITER_RAW.txt) — all inside hex/byte tokens, none a
count claim.**

Classification of every token hit:
- **Historical artifacts** (byte-identical, immutable): census_state.json, the 12
  qc_probe files (incl. out_qc1_counters.txt lines 24/28/44/55/56 — the E-3 SPURIOUS
  "claim match: FAIL" line intact), SF30_WRITER_RAW.txt (header counts, per-candidate
  blocks), SF30_WRITER_CENSUS.csv (VA substrings only), F1_GLOBALPTR_PROOF_RAW.txt
  P9 (the proof's pin against the historical CSV state — the QUESTION's premise, by
  design), f1_globalptr_proof.py's P9 pins (same class), AMEND_LOG_R1.md,
  PE_MASTER_REVIEW.md (incl. the E-2-superseded sentence, supersession carried by
  AMEND_LOG_R2), QC_AUDIT_R1.md (the historical QC's own record; supersessions carried
  by E-1/E-3 without editing the file — the amendment's disclosed design),
  STAGE_ACCEPTANCE_GATES.csv (the historical gate record).
- **Annotated canonical layer**: REPORT.md lines 82 (C3 row: historical + canonical
  annotation in the same cell), 94-95, 100-101, 105 ("= 3023 (historical)"), 119
  (the canonical supersession counts inside the branch-(b) parenthetical),
  150-151, 174; HANDOFF.md lines 17/20 (residue: canonical + historical), 46-47
  (gates line: historical + canonical); the sidecar lines 86/89/94/95 (Historical/
  CANONICAL/(historical)/"canonically... 3022" labels); AMEND_LOG_R2.md's every
  occurrence (the annotation record itself: F2 quotes, P9/branch statements, EDIT/C
  descriptions, E-3, §6 counts with historical/canonical markers).
- **Hash-substring class**: 154 hits, all inside hash/VA/byte tokens (listed above).
- **UNANNOTATED canonical-layer hits: 2** — REPORT.md:131 (the §4 gates-table G2
  mirror) and HANDOFF.md:40 (the NOT_CHECKED run-scope 618). Both adjudicated
  ACCEPTABLE in §3 (artifact-scoped historical mirror; run-scope statement
  contextualized by the same file's annotations). Neither asserts a wrong canonical
  number: the gates mirror describes the byte-identical artifact's true counts, and
  the NOT_CHECKED line describes the run's own historical coverage. **No hit anywhere
  presents 618/3023 as the live canonical state.** The two hits are recorded as P3-2
  (wording recommendations for any future regeneration), not as count errors.

## 6. The C2-4 method deviation (task 6) — audit + adjudication

**What the §2k documentation says** (verified present and complete): the unchanged
updater's new-row assert requires its OWN row's disk hash to differ from its manifest
row — true for C1 (the script was edited there) but FALSE for C2 (script unchanged,
its manifest row already == disk) — so the literal re-run fails fail-closed
(observed: an AssertionError before any write); the resolution follows the C1 batch's
own recorded method: the INPUT manifest is rolled back ONE ROW (its own row reset to
the pre-C1 value 5A20758E...) and the updater re-runs UNCHANGED with every assert
passing; the deterministic output refreshes every row from disk; the ONLY row whose
hash changes vs the pre-batch manifest is AMEND_LOG_R2.md.

**My audit of the end state and the mechanism**: I read amend_r2_manifest.py to EOF.
The assert chain is exactly as described (step 5: BATCH_EDITED_NEW rows must satisfy
disk != manifest-row; the build() output ignores the input manifest VALUES entirely
and writes fresh disk hashes — so a rolled-back input row can never leak into the
output). I verified the FINAL manifest end state independently: **37/37 rows == disk**
(§3 EDIT 7). I verified against the executor's C1 after_state record (read-only,
corroboration only): the C1-final manifest (on-disk SHA256 8959C695..., recorded) vs
my current manifest parse — **exactly ONE row differs: 06_REPORT/AMEND_LOG_R2.md**
(838784B9... → C6905FE4...), i.e. the §2k claim "the ONLY row whose hash changes is
AMEND_LOG_R2.md" is byte-verified TRUE. The C1-final AMEND_LOG state 838784B9... in
the same record matches §2k's "before" pin.

**Adjudication: acceptable-with-documentation.** The deviation is (a) real and
disclosed non-silently with its full mechanism; (b) confined to a TRANSIENT input
assert state (the rolled-back row exists only between the rollback and the updater's
rebuild, and the rebuild provably writes disk truth for every row); (c) end-state
fully verified by me (37/37 == disk; exactly one row changed vs the C1 manifest);
(d) the alternative — editing the updater to weaken its assert — would have been
worse (violating C2's "unchanged updater" constraint and the guard-strengthening
rule). I record a future-tooling recommendation (P3-3a): parameterize the
expected-change set per batch instead of requiring a per-row diff against the input
manifest, so re-runs never need input rollbacks.

## 7. The executor's disclosed deviations (task 7) — adjudication of each

1. **P5 literal-pin mismatch ("ONLY esi definition" vs the epilogue pop).** The
   AMEND_LOG_R2 §1 documentation is **accurate**: the capture convention
   (definitions up to the capture) HOLDS byte-level (my decode: esi redefined only at
   0x409150, AFTER the eax capture 0x409142; the capture itself is the only mov-def;
   entry ecx unmodified to 0x4090A5 across 12 instructions); the measured mismatch
   (esi definitions in body = 2) is exact; the same-sentence observation ("followed
   ONLY by epilogue" acknowledging the epilogue that contains the pop) is correct.
   The mismatch did not affect the branch outcome (P7 alone routes to branch (b)).
   One documentation-completeness gap is recorded as **P3-1**: the raw's tail
   sub-predicate ALSO evaluated False, for three further literal grounds the log does
   not enumerate (see P3-1). Verdict: **ACCEPTED** (with the P3-1 completeness note).
2. **EDIT-4 "17th vs 16th hex character" wording.** My measurement: the differing hex
   character is at 0-based index 15 = **the 16th character** — the AMEND_LOG's
   correction of the order text's "17th" is exact, and the OLD/NEW hash strings were
   applied verbatim (the one-byte diff at offset 28048 proves it). Verdict:
   **ACCEPTED — the deviation note is itself verified correct.**
3. **C2 exactly-once premise deviation (the defective strings occurred TWICE: listed
   value + discovery-note quote).** I verified independently from the executor's
   pre-C1 before-copy of AMEND_LOG_R2.md (read-only corroboration): the pre-C1 log
   contains the 65-hex RTTI literal EXACTLY ONCE (at the §7 listed value — the
   discovery note did not exist yet), and the one-char-wrong MANIFEST_NOTE literal
   EXACTLY ONCE — I RECOVERED that literal from the before-copy
   (`6F832230769D78ED02A7A6DAF26775E548BDF559E7F8B4CC42C8781A47FD0410`) and it
   differs from the true hash at **exactly one position, hex position 28** — the §2k
   signature ("ONE wrong character, at hex position 28") is byte-verified EXACT. The
   C1 batch then added the discovery-note quotes (→ 2 occurrences each), and C2
   eliminated both (current log: 0 occurrences of each, verified directly; the true
   values occur 3× each and are script-asserted == the manifest rows). The
   "zero-after" end state holds. Verdict: **ACCEPTED — the premise deviation was real,
   is documented non-silently, and the elimination is complete and verified.**

## 8. Findings

**P0: 0 · P1: 0 · P2: 0 · P3: 3** (+ my own QC instrument-error notes, disclosed in
§1 — none of which affects any result in this report).

No finding invalidates any load-bearing claim of the amendment. Every load-bearing
fact (the F1-P binary census, the branch-(b) decision, the canonical counts, every
edit, every hash pair, the manifests) is independently reproduced in §1-§7.

**P3-1. AMEND_LOG_R2 §1 documents only one of P5's failing literal pins (documentation
completeness; the chain substance is unaffected and independently confirmed).**
Location: 06_REPORT/AMEND_LOG_R2.md §1 (the P5 paragraph); the full failure set is
visible in 01_RAW/F1_GLOBALPTR_PROOF_RAW.txt lines 313-340. Claim as worded: "MISMATCH
detail: the pin 'mov esi, ecx @0x004090A5 is the ONLY definition of esi in the body'
is contradicted by the epilogue's pop esi @0x00409150". Counter-evidence (my decode +
the raw): the P5 predicate ALSO failed in its tail sub-predicate, for three further
literal grounds the log does not enumerate: (i) the tail clause demands "no eax/esi
def" in the tail, but the tail legitimately contains `pop esi` @0x00409150 (the same
epilogue fact, so partially the same root); (ii) the mnemonic whitelist
("pop/leave/mov/ret") does not contain `add`, and the epilogue's
`add esp, 0x14` @0x00409152 (`83c414`) fails it; (iii) the tail's op_str pin
`"0x4"` never matches capstone 5.0.7's rendered operand of `ret 4` (`C2 04 00`), which
is `"4"` — I reproduced this rendering myself. The raw line 340 ("tail: no eax/esi
def, ends ret 0x4 @0x00409155 (c20400): False") honestly records the failure, and the
log's substantive statement ("followed ONLY by epilogue and `ret 4` @0x00409155
(C2 04 00)") is byte-TRUE per my own decode. Effect: none on the verdict (P5 was
MISMATCH regardless; branch (b) routes through P7); but a future re-derivation that
tries to "fix" the pin by only re-wording the esi clause would still get a False tail
and might misdiagnose it. Narrow correction (next errata/regeneration note): enumerate
all four literal-pin failures of P5 (esi-def count; tail-no-def clause vs the pop;
whitelist missing `add`; op_str "0x4" vs rendered "4"), or annotate the raw's tail
False line accordingly. Revalidation predicate: decode 0x409142..0x409155 and render
`ret 4` with capstone 5.0.7 — the op_str is "4"; re-evaluate the proof's tail
predicate verbatim and confirm it fails on the three listed grounds.

**P3-2. Two unannotated canonical-layer count hits — both adjudicated ACCEPTABLE
(wording recommendations only).** Locations: 06_REPORT/REPORT.md:131 (the §4
gates-table G2 row, "raw==CSV==state-json counts (2/618/3023/0)") and
06_REPORT/HANDOFF.md:40 ("individual resolution of the 618 POSSIBLE_ALIAS rows" in
NOT_CHECKED (short)). Counter-evidence + adjudication: fully reasoned in §3 — the
§4 table is an explicitly-cited mirror of the byte-identical STAGE_ACCEPTANCE_GATES.csv
whose counts are TRUE of the unchanged historical artifacts (I re-parsed CSV/raw/
state-json: they are 2/618/3023/0 on disk), with the canonical annotations carried
prominently in REPORT §3 of the same file; the HANDOFF line is a run-scope statement
about what the R1 run did not examine, contextualized by the same file's residue and
gates-line annotations. Neither presents 618/3023 as the live canonical state (the
whole-package census in §5 confirms: no hit does). Narrow correction (future
regeneration only — no evidence change warranted now): annotate the §4 table header
"(historical artifact mirror)" and the HANDOFF NOT_CHECKED item "(historical row
count)". Revalidation predicate: re-run the §5 census — the unannotated-canonical
count should be 0 after those annotations.

**P3-3. Updater ONE-SHOT assert design + one cosmetic path-casing inconsistency.**
(a) Location: 00_Control/amend_r2_manifest.py (the BATCH_EDITED_NEW assert, step 5) +
AMEND_LOG_R2 §2k. The design requires a re-run against a prior output to see its own
row as "changed", forcing the documented one-row input rollback (§6). The deviation
is acceptable-with-documentation and the end state is fully verified; the
recommendation: a future updater edition should parameterize the expected-change set
per batch (or assert against the PUBLISHED baseline only, which it already embeds),
eliminating the transient wrong-row input state entirely. Revalidation predicate: a
re-run of the next batch's updater against the current manifest with NO input
modification passes fail-closed. (b) Cosmetic: AMEND_LOG_R2.md §8 line "00_Control/
amend_r2_manifest.py" spells the path with lowercase 'c' (1 occurrence); every
authoritative row (MANIFEST_SHA256.csv, SCRIPT_SHA256.csv) uses the correct
"00_CONTROL/". No functional effect; note for the next log regeneration.

## 9. Claim matrix (amendment claim → my independent measurement → verdict)

| # | amendment claim | my measurement | verdict |
|---|---|---|---|
| 1 | BASE_SHA == HEAD == origin/master == ls-remote == 3644e5ac... | all three re-measured (ls-remote vs the actual remote URL) | CONFIRMED |
| 2 | git census: 6 modified / 0 staged / untracked == 2 baseline + 5 new / 0 pycache | raw porcelain: 6 ` M` (the exact set), diff --cached empty, 7 `??` as claimed, 0 pycache/pyc | CONFIRMED |
| 3 | EXE pins (SHA/size/machine/magic/base/no-ASLR) | own PE walk, all match | CONFIRMED |
| 4 | sweep 2,266,698 decoded / 64 restarts (identical to R1) | own sweep: identical totals + 64/64 restart-VA list identical | CONFIRMED |
| 5 | (a) 0x405250/0x405256/0x40525B pins; 1 interval insn (push); no edx def | own decode, all match | CONFIRMED |
| 6 | (b) 179 = 1 WRITE @0x404C9D + 178 READs; item set == raw §P3 | own census: 179/1/178, item set + per-item bytes/access identical, 0 diffs | CONFIRMED |
| 7 | adversarial: no &global taker outside .text (my addition) | whole-file raw dword 0x00B6C3D8: 180, all .text, all = census disp bytes + push imm | CONFIRMED (strengthens claim 15) |
| 8 | (c) 1 E8 @0x404C8B to 0x409080; raw dword 0x40409080 == 0 | own scans, exact | CONFIRMED |
| 9 | (d) last eax def @0x409142; esi capture @0x4090A5; pop esi AFTER capture; 0 writes [esi]; ret 4 @0x409155 | own body decode, every element confirmed (P5 substance TRUE; see P3-1 for the literal-pin tail) | CONFIRMED |
| 10 | (e) 0x404C86 B9 C0 FE B9 00; no eax def call-end→store | own chain decode, exact | CONFIRMED |
| 11 | (f) 0x00B9FEC0/0x00B6C3D8 .data file-backed; at-rest zeros | own reads: 25 dwords all zero; slot == 0 | CONFIRMED |
| 12 | (g) IMM census == 1 @0x404C90; arg at [esp+0x20] (4+0+28==0x20); edx := arg @0x404BC5; mov [ecx],edx @0x404BE9 89 11, no edx redef in between; xadd = register-reuse FP (mov edx,ecx @0x404BFE) | own esp simulation + window decode: all confirmed; + my supplementary add-esp,4 caller cleanup & callee ret-form checks proving the 1-arg convention and esp-neutrality | CONFIRMED |
| 13 | (h) 2 imm32 0x00A7D458 stores (@0x509366/@0x50A269); 0 dword 0x509330; ctor callers {0x47D043,0x52480F}; push 0x98/new/ctor window | all reproduced exactly | CONFIRMED |
| 14 | (i) CSV 3643 = 2/618/3023/0; row 0x40525B REJECTED_ALIAS; fired-reason census | own parse + own reason recount, all exact; row 18 = file line 18 verbatim | CONFIRMED |
| 15 | F1-P verdict FAIL via P7(b); BRANCH (b); canonical 2/619/3022/0; CSV/RAW byte-identical | decision independently adjudicated SOUND (§2.1); counts arithmetic-verified; hashes byte-identical | CONFIRMED |
| 16 | EDIT 4: exactly one byte @28048 '2'→'7'; corrected string == fresh qc4 hash == manifest row; 16th hex char | all measured exact | CONFIRMED |
| 17 | EDIT 5: interpreter line + 5 map rows + reproduce line | all present once; published line 32 read "3.12.10" (verified from git); 3.12.7 re-measured | CONFIRMED |
| 18 | EDIT 1 + C1..C3: §3 bound paragraph, C3 row, §5#5, §7 annotations | all fragments present once; hash chain published→7DF5E064→DB89FA3A verified (before-copy + disk) | CONFIRMED |
| 19 | §4 gates table = historical mirror | adjudicated ACCEPTABLE (P3-2) | ACCEPTABLE |
| 20 | C4a/C4b: HANDOFF residue == §2h prepared text verbatim; gates-line annotation | byte-exact (4-line block); old quote == published lines 17-18; hash chain verified | CONFIRMED |
| 21 | HANDOFF NOT_CHECKED 618 = run-scope | adjudicated ACCEPTABLE (P3-2) | ACCEPTABLE |
| 22 | EDIT 2 sidecar: verbatim quotes + counts + pins + prohibition | all byte-verified | CONFIRMED |
| 23 | EDIT 3 AMEND_LOG_R2: §0-§8+2h APPLIED+2j+2k; E-1..E-4; T-1..T-3; §5 inventory/A/B/PENDING; §7 hashes fixed; 0 invalid hex; defective literals 0× | all verified (E-3's quoted predicate read from qc1_counters.py:88 verbatim — the dict-Counter bug is real and correctly described; out_qc1_counters.txt line 28 intact byte-identical) | CONFIRMED |
| 24 | EDIT 6: SCRIPT_SHA256 6 rows, all == fresh; row history 5A20758E→B2B4D1B0 | all verified incl. the pre-C1 before-copy == 5A20758E | CONFIRMED |
| 25 | EDIT 7 + C6 + C2-4: manifest 37 rows all == disk; self-exclusion; baseline fidelity; only AMEND_LOG row changed in C2-4 | 37/37 == disk; embedded baseline == git HEAD 32/32; C1-final vs current: exactly 1 row (AMEND_LOG_R2) | CONFIRMED |
| 26 | untouched §7 list (27 files) + 3 R2-new files + NINODE 7/7 + experiments 23 | all re-hashed/censused, all match | CONFIRMED |
| 27 | C2 defective literals: signature exact; zero-after | pre-C1: 1× each (recovered the MANIFEST_NOTE wrong literal — differs at hex position 28 exactly); current: 0× each | CONFIRMED |
| 28 | F5 process note: zero NINODE interaction; missing deliverables absent; PENDING HUMAN ADJUDICATION | 7/7 hashes match; only 7 files exist (no 02_ANALYSIS/03_EVIDENCE/06_REPORT); note present; I performed ZERO NINODE decodes as well | CONFIRMED (adjudication remains HUMAN's) |

## 10. FULL_READ_LOG (this QC round)

Fully read (line-by-line to EOF): AMEND_LOG_R2.md (661) · REPORT.md (201) ·
HANDOFF.md (52) · QC_AUDIT_R1.md (426) · SF30_WRITER_CENSUS_SUPERSESSION_R2.md (95) ·
03_EVIDENCE/README.md (65, + the published state via git show) · AMEND_LOG_R1.md (425)
· PE_MASTER_REVIEW.md (34) · MANIFEST_NOTE_PUBLICATION.md · SCRIPT_SHA256.csv ·
MANIFEST_SHA256.csv · STAGE_ACCEPTANCE_GATES.csv · RUN_CONTRACT.md (128) ·
SOURCE_IDENTITIES.json (44) · census_state.json (142) · SF30_RTTI_RAW.txt (33) ·
F1_GLOBALPTR_PROOF_RAW.txt (542) · f1_globalptr_proof.py (1008 — load-bearing
generator, read to EOF) · amend_r2_manifest.py (209 — load-bearing updater, read to
EOF) · qc1_counters.py (154 — the F2 subject) · out_qc1_counters.txt (60) ·
MANIFEST_NOTE_PUBLICATION.md · AGENTS.md · AUDIT_ENTRYPOINT.md (the LATEST RUNS table)
· 00_PROJECT_CONTEXT/PE_MASTER_ACTIVE_ORDER.md · the pe-master-audit skill (v2).
Programmatic full parses: SF30_WRITER_CENSUS.csv (all 3643 rows);
SF30_WRITER_RAW.txt (why-line reason census over all rows; line 320; header counts;
per-candidate blocks parsed for the reason census); the whole-package count census
(all 38 files, every 618/3023/619/3022 occurrence classified); the §P3 179-item list.
Executor temp-dir records read READ-ONLY as corroboration only (never as primary
evidence): sf30_amend_r2\c1_batch\before\* (5 before-copies — hashed),
c1_batch\after_state.json (the C1 final-state records). My probe scripts + outputs:
see §14.

## 11. NOT_CHECKED (by this QC round)

- No runtime/dynamic verification of anything (STATIC-ONLY; no game binary process
  launched by QC either).
- The other 3642 census rows were NOT instruction-by-instruction re-decoded by THIS
  round (the R1 QC + PE-MASTER already reproduced them; this round re-derived the
  sweep statistics — 2,266,698/64 + the identical 64-restart list — the 179-item
  [0x00B6C3D8] census, the CSV counts, the reason distribution, and all F1-relevant
  windows; the amendment changed no classification row).
- The remaining 606-of-618 POSSIBLE_ALIAS rows were not re-traced (out of scope for
  this amendment; only row 0x0040525B was in play — re-derived fully here).
- The intermediate C2-era AMEND_LOG state (ADCAD755...) is not independently
  verifiable from disk (no C2-era copy exists); I verified the chain ENDPOINTS
  (the C1-final 838784B9 via the C1 after_state record; the current c6905fe4 on disk
  == manifest row) and the pre-C1 defective-literal state (1× each, from the
  before-copy).
- The RTTI walks (SceneFeederObject/NiNode chains) were not re-walked THIS round —
  they were byte-verified by the R1 QC + PE-MASTER, the amendment touched no RTTI
  evidence, and the F1 proof's contingency walker never fired.
- 0x437F70 / 0x82B5A0 / 0x007B5390 bodies were NOT decoded by this QC (the standing
  scope holds; no extent derivation was needed).
- The NINODE package's SCIENCE was not audited (F5 is a process note; the 7 files
  were re-hashed only; the human adjudication is pending). The experiments/ content
  was censused (name+size) only.
- The remote publication state of THIS amendment is pre-publication by design (the
  amendment made zero commits; publication is a separate step). HEAD == origin/master
  == ls-remote holds now.

## 12. QC verdict

- **QC_VERDICT: QC_PASS_WITH_FINDINGS** — the amendment
  PE_935_SCENEFEEDER_LINK30_AMEND_R2_20260914 (R2 main + completion C1 + micro-batch
  C2) is independently reproduced to the byte by this fresh-context round: the F1-P
  binary facts (sweep identity, the 179-item census item-for-item, every window, the
  stack arithmetic, the value chain, the at-rest data, the SF-heap premise), the
  BRANCH (b) decision (adjudicated SOUND), the canonical counts 3643 = 2/619/3022/0,
  the historical-artifact byte-identity, every edit (REPORT/QC_AUDIT_R1/README/
  SCRIPT_SHA256/HANDOFF/AMEND_LOG_R2/sidecar), the 37/37 manifest, the 6/6 script
  table, the 32-row baseline fidelity, the untouched set 27/27 + NINODE 7/7 +
  experiments 23, the count-consistency census (zero live-canonical misstatements),
  and all three disclosed deviations (each verified real, documented non-silently,
  and correctly resolved).
- Findings: **P0: 0 · P1: 0 · P2: 0 · P3: 3** (P3-1 the P5 mismatch documentation
  omits the tail sub-predicate's further literal-pin failures; P3-2 the two
  adjudicated-acceptable unannotated count hits; P3-3 the updater ONE-SHOT design
  note + one cosmetic path casing). None blocks PE-MASTER adjudication or the
  subsequent publication step; each carries a narrow correction and a revalidation
  predicate in §8.
- This verdict is INTERNAL_QC, not MASTER_ACCEPTED and not milestone closure. The F5
  (NINODE) process note remains PENDING HUMAN ADJUDICATION — untouched by this QC
  beyond the 7/7 hash verification, exactly as the amendment left it.
- No executor evidence file was modified by this QC. ZERO git mutations (HEAD ==
  BASE_SHA == origin/master == remote, verified before and after; the tracked-modified
  set is exactly the amendment's six by design — publication is the separate later
  step). My ONLY write is THIS file (a new untracked path
  06_REPORT/QC_AUDIT_R2.md — outside the 37-row executor/amendment manifest by the
  established QC-inventory convention; the manifest was not touched).

## 13. Handoff keys (for PE-MASTER)

- QC_VERDICT: QC_PASS_WITH_FINDINGS (P3-only).
- Canonical state confirmed: 3643 = 2 PROVEN / 619 POSSIBLE / 3022 REJECTED / 0
  UNRESOLVED (branch (b) sound); historical artifacts byte-identical.
- Publication readiness: the on-disk package is internally consistent (37/37 manifest
  == disk; 6/6 script table; all hash pairs verified). The persistence worker's
  remaining external items: the AUDIT_ENTRYPOINT row (§2i prepared text) and the
  path-limited commit/push — per the standing publication protocol.
- NEXT_PARENT_ACTION: PE-MASTER adjudicates this QC verdict; if accepted, the
  persistence/publication step proceeds; the F5 process note stays queued for the
  human's A/B adjudication; the P3 wording/tooling notes enter the next regeneration
  template.

## 14. QC probe inventory (this round; outside the package)

Scripts + outputs under `C:\Users\User\AppData\Local\Temp\opencode\sf30_qc_r2\`
(SHA256 uppercase; own minimal PE parser; capstone 5.0.7 from the pinned path;
interpreter `D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe` 3.12.7;
every run `-B`):

- qc_p1_binary.py B262D38FC799A0A1F053C496033E26338D00FF00364B0FD427BE439E5BF44CFB —
  the binary re-derivation (sweep, censuses, windows, data reads, CSV/raw recounts)
  → qc_p1_out.txt F4BB9E83F56FC4F01E111CF9CB088F0F63E6528B4A369048D2691CDF1EB9ADA5
- qc_p2_files.py 9DA3475BDD29B7E7E01B0A57023687CDB9DF3B56AF873E5DCD45D2DFA8182468 —
  git census (see §1's instrument note: its §1 staged-entry line is the strip
  artifact, corrected in qc_p3_residual.py), NINODE/experiments, EDIT 4 byte-diff,
  untouched re-hashes, manifest/script-table full verify, baseline fidelity, content
  fragments, hex census, count census → qc_p2_out.txt
  C90EDB7CEBA73DB1621EA0EFC7B66E83FA82A05070F3BF89AABE62F03BF155D
- qc_p3_residual.py 3FE24C74C961DA91D12D42FD2F9CCD48193F42BA9ED078F0249CD8B624C08C65 —
  corrected git census (raw), the §2h byte-exact block comparisons, publication-state
  before-pins, restart-VA comparison, normalized fragments → qc_p3_out.txt
  8ED58C7334EB5DF41FE113DE56C976377D69DEDE11CA0A7EFEB828FC9AB489D7
- One-off inline checks (git/README casing/manifest dict-diff/defective-literal
  recovery) — recorded in this file's sections; no package writes.

— pe-master-auditor, INTERNAL_QC round R2 (fresh context), 2026-09-14.
