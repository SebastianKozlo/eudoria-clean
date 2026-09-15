# QC_AUDIT_R2 — TARGETED RE-QC (post-correction verification) for RUN PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915

- RE_QC_BY: pe-master-auditor (fresh-context; did NOT formalize this run, did NOT execute it, did NOT author the correction batch)
- MODE: TARGETED RE-QC of the CORRECTION BATCH ONLY (AMEND-3..AMEND-12). The science conclusions were already
  independently verified by the original fresh QC (06_REPORT/QC_AUDIT.md, QC_PASS_WITH_FINDINGS) and are NOT re-derived here.
- NO_NESTED_TASKS respected. This re-QC created ONLY this file; NO executor evidence, AMEND_LOG, manifest, index or any
  package file was modified; NO git mutations.
- DATE: 2026-09-15 (local -07:00)
- ENVIRONMENT (measured at re-QC time): python 3.12.7 (D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe);
  capstone 5.0.7 (cs_version (5,0,1280)); PowerShell 5.1. All re-QC probes run OUTSIDE the package
  (C:\Users\User\AppData\Local\Temp\opencode\qc935r2\, probes probe1..probe11) and are READ-ONLY on the EXE.
- SOURCE PIN re-verified at re-QC start: D:\Eudoria_Reconstruction\pcg_install\Entropia.exe = 8015872 bytes,
  SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 — PIN MATCH (measured, not assumed).

## VERDICT: **RE_QC_PASS_WITH_FINDINGS**

0 x P0 / 0 x P1 / 0 x P2 / **1 x P3** (+ 2 minor observations, non-numbered)

The correction batch (AMEND-3..AMEND-12) is verified LANDED and BYTE-CORRECT. All 9 original QC findings
(P1-1, P1-2, P2-1..P2-4, P3-1..P3-3) are fixed as ordered, with every load-bearing corrected fact independently
re-measured from the EXE bytes by fresh probe code (not the executor's tooling). Both correction-vs-QC-annex
discrepancies are adjudicated from bytes: the executor's version is CORRECT in both, and neither affects the
S-immutability conclusion. No gate status, no science-status dimension, no measured value and no predicate was
weakened or altered. Package provenance is fully consistent (manifest 52/52, index 51/51, index<->manifest 51/51).
The single residual finding (P3, this re-QC's own discovery) is a correction-log completeness gap for the
AT_RUN_END_GIT_OBSERVATION.md appendix — mechanical, append-only-fixable, non-blocking.

---

## SECTION A — MANDATED CHECKS (each with method + result)

### A.1 AMEND_LOG_R1.md integrity — PASS
- Entries AMEND-3..AMEND-12 exist, each with finding ID + file + exact change + why + .pre/new SHA256 pair (read in full, 192 lines).
- Append-only proof: the .pre copy (00_CONTROL/PRE_EDIT/00_CONTROL/AMEND_LOG_R1.md.pre, 2623 bytes,
  SHA256 80D3A856D317D9BA012B5E1761D20CF967E205C07375CD0427815F7417AEAF32) is an EXACT BYTE-PREFIX of the current
  file (17233 bytes) — measured: BYTE_PREFIX=True. AMEND-1/AMEND-2/DISCLOSURE are byte-unchanged.
- All 32 distinct 64-hex hash tokens in the log were programmatically extracted and resolved: every recorded
  .pre hash matches the corresponding .pre copy on disk; every recorded new hash matches the corresponding current
  file; the single non-resolving token E3B0C442...9B8255 is the SHA256 of a zero-byte file cited descriptively in
  AMEND-1 (verified: it equals sha256(b"")). No 63-hex (truncated) tokens present.
- Convention cross-check: every file with a .pre copy under 00_CONTROL/PRE_EDIT/ is covered by an AMEND entry
  EXCEPT 01_RAW/AT_RUN_END_GIT_OBSERVATION.md — see residual finding P3-R1 below.

### A.2 .pre integrity — PASS (19/19 verified; mandated minimum was 4)
All 19 .pre copies were hashed and compared:
- 15 via the recorded .pre SHA256 pairs in AMEND-3..AMEND-12: ALL MATCH (END_TO_END 0BBEC584/8293, REPORT
  986182BE/9935, HELPER_OPERATIONS 1F3155E4/3863, FUN_00437F70 54AA832A/10244, GATES BF451C54/4871, HANDOFF
  817BA82D/5645, gen_raw_evidence 791E92FC/33940, gen_manifest 70CE5EAF/7866, FUN_0050A050 AD0E2DD3/13717,
  HELPER82B5A0 csv 2092154C/1065, txt DB81D5D0/3788, SOURCE_VECTOR_LAYOUT 12FF2C63/10901, SCIENCE_STATUS_DELTA
  D8551BB8/2356, SCRIPT_SHA256 0F2EEB86/379, EVIDENCE_INDEX 4E0F94A9/4873, README 6EFD30CE/1255).
- 4 more via manifest rows (AMEND_LOG .pre 80D3A856/2623 — also byte-prefix-proven; AT_RUN_END .pre
  B575241382D8882AF426B4FF214EAC985D87851E2A352BC9E56710AB107FA1BC/2998; MANIFEST .pre 69114E25/3160;
  MANIFEST row set equal to the 52 non-manifest files — see A.7).
- All current files match the recorded new SHA256 + size (incl. REPORT C17A5691/10897, census raw FEF5DC1C/77113,
  census script 5777F559/50894).
- Mtime forensics consistent: .pre copies carry the ORIGINAL files' final write times (copy2-style preserved),
  corroborating them as byte-exact pre-edit snapshots; correction window 07:22:51..07:34:13 (content) ->
  07:39:55 (gen_manifest.py fix) -> 07:40:26 (AMEND_LOG final) -> 07:40:29 single-pass regeneration of
  SCRIPT_SHA256.csv / README.md / EVIDENCE_INDEX.csv / MANIFEST_SHA256.csv — matches AMEND-12's declared order.

### A.3 P1-1 fix (E.3 proof re-measured with exhaustive channels) — PASS, INDEPENDENTLY RE-VERIFIED FROM BYTES
- 01_RAW/ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt EXISTS (77113 bytes; SHA256 FEF5DC1C...01FF87 = manifest row = disk),
  with a complete provenance header (RUN_ID, GENERATED_UTC, GENERATOR_SCRIPT path + SHA256 5777F559...,
  MEASURED ENVIRONMENT at run time, source size+SHA with MATCH line, S0 fail-closed line, SOURCE OF TRUTH,
  PURPOSE) — read in full (1079 lines).
- Headline numbers, independently re-measured by my own whole-image scan + my own opcode-pattern store
  classifier (independent of census_triple_writes.py and of the original QC's probes):
  - Occurrence census: 0xBA921C = 107, 0xBA9220 = 81, 0xBA9224 = 80; total 268; ALL in .text (0 in any other
    section or overlay) — MATCHES census [T.1] and the original QC's 107/81/80.
  - Containment classification: I reconstructed every candidate instruction from all start offsets -14..-1 for
    every occurrence (473 candidate instances) and classified stores with my OWN encoding-pattern detector
    covering A3/66A3, 88/89 mod00rm101, C6/C7 05, 80/81/83 RMW, 00..3F ALU RMW, 8F 05, F6/F7, FE/FF,
    x87 stores (D9/DD/DB/DF fst/fstp/fistp), 0F C7 /1 cmpxchg8b, SSE stores (F3/F2/66 0F 11, F3/F2 0F D6,
    66 0F E7, 0F 2B, 66 0F 7F). STORE-CLASS CANDIDATES = **0** across all three dwords — MATCHES census [T.2].
  - Load decomposition (position-sensitive): 0xBA921C = 42 A1-moffs + 39 8B-mod00rm101 = 81 ABS loads;
    0xBA9220 = 13 + 68 = 81; 0xBA9224 = 20 + 60 = 80 — MATCHES census "81+81+80 absolute loads (A1/8B mod00 rm101)".
  - Push-takers: byte pattern 68 1c 92 ba 00 = exactly **24** sites, VA list EXACTLY equals the census/QC list
    (0x441040..0x949CCC); all push the same value 0xBA921C. MATCHES.
  - mov r32,imm32 takers: B8..BF + imm32 = exactly **2** (0x50AA1D, 0x96B960) — MATCHES census [T.5];
    lea reg,[abs] (8D 05) = 0.
  - Widened scan [T.3] (dwords 0xBA9215..0xBA9227): my own scan finds exactly 1 store-class candidate —
    `or dword [0xba9218],eax` @0x96BB5D (effective range 0xBA9218..0xBA921B, NO overlap with the triple) —
    MATCHES census [T.3] exactly.
  - Computed-base windows [T.6]: my own scan = [0xBA9000,0xBA921C): **22 distinct values / 45 .text occurrences**;
    [0xBA9000,0xBA92C0): **34 distinct values / 349 occurrences** — MATCHES census [T.6] and the original QC's
    independent 22/45.
  - Zero-init tail [T.9]: my own PE header parse (.data vaddr 0x76C000 vsize 0x3D6E4 rawoff 0x76C000 rawsize
    0x34000) — triple RVAs 0x7A921C/0x7A9220/0x7A9224 all BEYOND raw end 0x7A0000; vsize>rawsize; va2off()
    returns None (virtual-only, no file bytes). MATCHES.
- E.3 in END_TO_END_VALUE_FLOW_RAW.txt now ENUMERATES channels (1)-(6) with exact denominators (268 = 107/81/80;
  81+81+80 loads; 24 push sites, 23 resolved + 1 disclosed residual 0x488BEA; 2 getters with 4+1 E8 callers + 3
  vtable placements; 9 ECX-receivers read/forward/clobber with 0 [ECX+0/4/8] stores; computed-base windows
  34/349 and 22/45; neighborhood writes stop at 0xBA921B; zero-init tail), lists the store-encoding coverage as
  GENERIC, and separates DECODED channels from UNDECODED/DISCLOSED residuals. No unbacked "all/never" remains —
  every absolute claim is tied to an enumerated channel or a disclosed residual. The same correction is present
  in REPORT.md (one-line answer + exec summary item 3 + negative-control line), HELPER_OPERATIONS.md,
  FUN_00437F70_DISASM.txt, HANDOFF.md PRIMARY_EVIDENCE_PATHS, the G6 gate row and gen_raw_evidence.py literals.
- Getter/ECX counts re-verified (context): E8 callers of 0x50AA10 = 4 (0x43B584/0x43B78E/0x442886/0x4835CD);
  0x96B960 = 1 (0x4CD66E); 0x82B5A0 = 36; 0x437F70 = 99 — all MATCH the census and the QC-verified originals.

### A.4 P1-2 fix (stale EVIDENCE_INDEX README row; root cause fixed) — PASS
- The current 03_EVIDENCE/EVIDENCE_INDEX.csv row for 03_EVIDENCE/README.md = 7AAD189A591070335D777158428D7F0EC3F
  25FD1D8C8B197CEB2656036C9F43C / 1756 — my own hash of the on-disk file MATCHES; the manifest row is identical
  (mutually consistent). The .pre copy of the index still carries the original stale row (D53A02FD.../1251),
  confirming the defect story and the fix.
- My own full re-hash census: MANIFEST_SHA256.csv = **52 rows, 52/52 MATCH** (every row re-hashed; L12
  self-exclusion respected — no manifest self-row; manifest row set == exactly the 52 non-manifest files on disk).
- EVIDENCE_INDEX.csv = **51 rows, 51/51 MATCH**; index<->manifest consistency on all 51 shared paths: 51/51
  identical hash+size pairs; documented exclusions respected (no self-row, no manifest row; DISK_MINUS_INDEX
  beyond those two = empty).
- Root cause fixed and documented: gen_manifest.py generation order changed to SCRIPT_SHA256.csv -> README.md ->
  EVIDENCE_INDEX.csv -> MANIFEST_SHA256.csv (diff vs .pre verified); README.md documents the order; role map
  updated (census file, amended-file roles, 36/36). AMEND-12's regenerated-file hashes are intentionally not
  embedded in the log (self-referential loop) — they are on disk and verified above; disclosure is adequate.

### A.5 P2-1..P2-4 and P3-1..P3-3 fixes — ALL LANDED, BYTE-VERIFIED
- **P2-1 (padding miscount)**: my own byte read at 0x50A0AA: `cc cc cc cc cc cc 56 8b f1 80 7e 24 00 75 10 e8`
  = exactly **6 x 0xCC at 0x50A0AA..0x50A0AF**; next function starts **0x50A0B0** (`push esi; mov esi,ecx;
  cmp byte [esi+0x24],0`) — MATCHES the corrected [A.2] text, REPORT line 64-65, G2 gate row, and census [A.2].
  Extent verdict 0x50A050..0x50A0AA unchanged (QC-verified). All corrected locations carry inline AMEND NOTEs;
  no live "12x int3"/"0x50A0B6" claim remains (residuals are quotations inside disclosure notes only — see A.6).
- **P2-2 (37 -> 36)**: the [A.3] PIN table has exactly **36 rows** (counted; all MATCH) and the verdict line reads
  "ALL 36 PINNED INSTRUCTIONS MATCH"; "36/36" present in REPORT.md (lines 66, 110), HANDOFF.md (lines 6, 22),
  STAGE_ACCEPTANCE_GATES.csv G2, EVIDENCE_INDEX role map, and the census [A.3]. Independent backing: the contract's
  standing-knowledge block has exactly **36 instruction lines** (counted: lines matching '^0x00550A0xx' = 36)
  plus exactly 1 'fallback:' label line. The G2 predicate is unchanged (all pins MATCH).
- **P2-3 (HANDOFF contradiction)**: HANDOFF.md "Notes for QC" now correctly states AMEND_LOG_R1.md EXISTS with
  the 2 pre-existing entries + correction-pass entries, points at PRE_EDIT, and carries an inline AMEND NOTE
  quoting the original wrong sentence. Verified against the actual package state (AMEND_LOG exists, entries
  verified in A.1). Fixed.
- **P2-4 (fabricated prior_437f70_site cells)**: HELPER82B5A0_CALLER_CENSUS.csv rows 0x930030/0x930056 now carry
  prior_437f70_site=NOT_APPLICABLE with the measured ECX source note; the .txt prose now says 34 PAIR + 2
  STORED-ORIGIN sites with an inline AMEND NOTE. 36 data rows / 34 PAIR (all prior = site-7, geometry-consistent)
  / 2 NON-PAIR — census counts unchanged. BYTE-VERIFIED from my own decode: 0x930023 `mov ecx,[ecx+0x4c]`
  (8b 49 4c) resp. 0x930053 `mov ecx,[esi+0x4c]` (8b 4e 4c) load ECX = [this+0x4C] (stored origin) before
  `call 0x82b5a0` at 0x930030/0x930056; src = [this+0x14]+0x5C in both; the ORIGINAL cells were indeed
  mid-instruction byte positions (0x930029 inside `mov esi,[esp+8]` @0x930027 = 8b 74 24 08; 0x93004F inside
  `lea ecx,[esp+0xc]` @0x93004E = 8d 4c 24 0c) — neither is a call site. Fixed and byte-correct.
- **P3-1 (excerpt vs citation)**: SOURCE_VECTOR_LAYOUT_RAW.txt [B.2] excerpt extended to 0x7B46F0 with an AMEND
  NOTE; the cited anchor `lea edi,[esi+0x5c]` is MEASURED at 0x7B468E (bytes 8d 7e 5c — verified) and the
  3-float add/fsub uses (0x7B469E..0x7B46E5, incl. fsub [edi]/[edi+4]/[edi+8] @0x7B46D0/DA/E5 — verified) are
  now INSIDE the printed window. Fixed.
- **P3-2 (mangled K literal)**: SCIENCE_STATUS_DELTA.csv UNIT_SCALE basis cell now reads "bit-exact
  K=0x3F847AE140000000 (=(double)(float)0.01=0.009999999776482582; AMENDED per QC P3-2 ...)" — verified from
  bytes: qword at 0xA7B360 = 00 00 00 40 e1 7a 84 3f = 0x3F847AE140000000 = 0.009999999776482582; my own
  recomputation of (double)(float)0.01 (f32 0x01 = 0x3C23D70A widened) BITMATCHES. Status CONFIRMED unchanged.
- **P3-3 (SEH wording)**: FUN_00437F70_DISASM.txt [C.5] now describes the pushed-ECX slot as local/scratch
  (stashed with the operator-new result at 0x437FA4 — byte-verified 89 44 24 04 = `mov [esp+4],eax`) and the
  registration NODE as {prev, handler 0x99C06B} at [esp+8] installed by `lea eax,[esp+8]; mov fs:[0],eax`
  (0x437F87-0x437F8B — decoded and verified). Inline AMEND NOTE present; gen_raw_evidence.py literal fixed.
  Fixed.

### A.6 No science change — PASS
- 06_REPORT/STAGE_ACCEPTANCE_GATES.csv (19 lines both): diff vs .pre = exactly 2 changed rows (G2, G6); in BOTH
  the status column is UNCHANGED (PASS -> PASS); only the evidence/provenance text was corrected (P2-1/P2-2 in
  G2; P1-1 census citation in G6). All G0..G17 statuses byte-identical otherwise.
- 02_ANALYSIS/SCIENCE_STATUS_DELTA.csv (12 lines both): diff vs .pre = exactly 1 changed cell (UNIT_SCALE
  basis); status CONFIRMED unchanged; the other 10 dimension rows byte-identical.
- REPORT.md / HANDOFF.md / HELPER_OPERATIONS.md / FUN_* / census files: diffs vs .pre contain ONLY census
  references, count corrections, wording/provenance corrections and inline AMEND NOTEs (verified hunk-by-hunk);
  every measured value, hypothesis disposition (H1 CONFIRMED / H2 REJECTED / H3 CONFIRMED / H4 CONFIRMED /
  H5 PARTIAL) and gate summary is unchanged.
- "37/37" adjudication (task expectation "36/36 everywhere with no residual '37/37' in the package"):
  every LIVE claim now says 36/36. The remaining occurrences of the old string are, exhaustively:
  (a) the FROZEN historical AMEND-2 entry (append-only log; explicitly declared superseded by AMEND-6's NOTE);
  (b) quotations inside correction disclosures (AMEND-6 note, [A.3] census text + census script literal,
  FUN_0050A050 AMEND NOTE, G2 gate row's "the original '37/37' was a count error");
  (c) the original 06_REPORT/QC_AUDIT.md (P2-2 finding text — correctly NOT touched, it describes the defect).
  Rewriting (a) or (c) would violate the append-only/immutability rules; the literal reading of the expectation
  is unsatisfiable BY DESIGN, and the substantive requirement (no live 37/37 claim) is met. Same pattern holds
  for "12x int3", "0x50A0B6", "ALL 37", the mangled K literal and the old SEH wording (all residual hits are
  frozen-history or disclosure quotations; verified hunk-by-hunk, listed with line numbers in my probe log).

### A.7 Package hygiene — PASS
- Zero __pycache__ / .pyc anywhere in the package (file census by walk). Zero NUL-byte (binary) files — all 53
  files are text; extensions {.md 12, .csv 7, .json 1, .pre 19, .py 5, .txt 9}. Largest file = the census raw
  (77113 bytes). NO proprietary payload (no EXE/DLL/archive/image bytes; source era/path/size/SHA + reproduction
  method only, per the evidence rules).
- SCRIPT_SHA256.csv: 5/5 rows re-hashed MATCH and covers EXACTLY the 5 scripts on disk, including the NEW
  00_CONTROL/scripts/census_triple_writes.py (re-hashed: 5777F559101CFAC2CAEACC6ADA23291E412F046909D52677E
  2E751A2E98C734B, 50894 bytes — equals the AMEND-3 recorded value and the manifest row); no script on disk is
  missing from the CSV and no CSV row lacks a disk file.
- Package file census = **53 files = 52 manifest rows + the manifest itself** (verified: manifest row set equals
  the disk set minus MANIFEST_SHA256.csv; DISK_MINUS_MANIFEST = MANIFEST_MINUS_DISK = empty).
- QC_AUDIT.md UNTOUCHED: mtime 06:57:53 (before the 07:22+ correction window), disk hash = manifest row
  (6AFD70DA88977D76086E9B1737FCCEC9D7669AE02FE917C0AF83F73DDF046EF0/37701), no AMEND entry touches it, and its
  content still records the pre-correction QC-time state (correct for a frozen QC record).
- RUN_CONTRACT.md UNTOUCHED: disk hash = EEF4C8982FC49A1B3B2F051557ED7CCECDA4350690A3580809D4E67A410AAC3E /
  28824 = the value the original QC recorded = manifest row. SOURCE_IDENTITIES.json UNTOUCHED (disk = manifest =
  0A66902D.../8945). 01_RAW/AT_RUN_START_GIT_OBSERVATION.md UNTOUCHED (disk = manifest = 3E789A39.../8694;
  mtime 06:20:30; SECTION 1 formalizer block intact — read and verified; SECTION 2 executor append incl. the
  ImageBase-offset disclosure present and consistent with the AMEND_LOG DISCLOSURE note).
- All 53 files decode as strict UTF-8 (AMEND-2 discipline preserved through the correction pass).

### A.8 Git — PASS
Measured by me at re-QC time (repo root D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean):
- HEAD = 3068f31ad8db7e993a72365dc28cc03066095afd (= BASE_SHA = origin/master local ref); branch master.
- `git rev-list --count 3068f31..HEAD` = 0 — ZERO new commits since BASE_SHA.
- `git status --short` = exactly the 2 pre-existing untracked paths (docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_
  R1_20260914/, experiments/) + THIS run dir (docs/audits/PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915/).
- reflog: newest entry is still the pre-existing BASE_SHA commit (HEAD@{0} = 3068f31 formalization-era commit);
  NO entry created by the executor run or the correction batch — ZERO git mutations CONFIRMED.
- Worktrees: the 3 declared (main + 2 audit worktrees) — unchanged.
- (Remote equality note: origin/master here is the local remote-tracking ref; the run's own AT_RUN_START also
  recorded a network ls-remote MATCH at formalize time. No push has occurred; publication remains G17.)

---

## SECTION B — ADJUDICATIONS (correction-vs-QC-annex discrepancies; both from bytes)

### B.1 QC's 10th push-consumer "0x8DC5B0->0x92FFE0" — EXECUTOR CORRECT; QC annex item REFUTED; S-immutability UNAFFECTED
My own bytes:
- 0x8DC5B0 = `mov ecx,[ecx+0x1b8]; jmp 0x92ffe0` (thunk). Its E8 callers = EXACTLY 3: 0x4FC9E7, 0x522F92,
  0x5F6D33 (my own whole-.text E8 scan). Their pushed operands (decoded windows): 0x4FC9E7 <- `lea ecx,[esp+0x20]`
  (0x4FC9D2) then `push ecx`; 0x522F92 <- `lea ecx,[esp+0x3c]` (0x522F71) then `push ecx`; 0x5F6D33 <- `lea
  edx,[esp+0x18]` (0x5F6D2E) then `push edx`. ALL are stack-frame pointers, NEVER &triple — MATCHES the census's
  refutation text exactly.
- The `push 0xba921c` at 0x5F6D21 is consumed by the IMMEDIATELY-ADJACENT `call 0x8DC5C0` at 0x5F6D26 (push;call,
  no intervening instruction) — verified. My independent site->first-call mapping over ALL 24 push sites yields
  10 callees = the census's 9 resolved (0x6C9490 with 13 sites — the 2 beyond my first 0x40-byte window,
  0x50C272/0x50CDB3, confirmed with a wider window; 0x730F90; 0x730FB0; 0x4B66D0; 0x7302E0; 0x4CE5B0; 0x82BC10;
  0x8DC5C0; 0x4AA720) + 0x4123D0 (the first adjacent call at the disclosed-residual site 0x488BEA, which the
  census correctly does NOT count as a resolved consumer). NO push site maps to 0x8DC5B0.
- Effect on the S-immutability conclusion: NONE either way — 0x92FFE0's head passes its [esp+4] arg as the SRC
  of the inverse 0x82B6A0 conversion (read-only; verified), and the QC's own census-level conclusion (0 stores)
  never depended on the 10th-callee attribution. The QC's P1-1 annex enumeration contained one wrong
  attribution; the corrected 9-callee + 1-residual enumeration (census [T.4]/E.3 channel (4)) is byte-correct.

### B.2 0x48BAC0 clobber first-address 0x48BAD6 (correction) vs 0x48BB19 (QC) — EXECUTOR CORRECT; conclusion IDENTICAL either way
My own decode of 0x48BAC0..0x48BB26: first ECX WRITE = 0x48BAD6 `lea ecx,[esp+0x10]` (8d 4c 24 10);
`mov ecx,esi` at 0x48BB19 (8b ce) is a LATER secondary redefinition (the address the QC cited); there is NO
[ECX+0/4/8] read anywhere in the window before either (first [ECX] x87 READ = none). S is unused in 0x48BAC0 —
the corrected text (census [T.8], E.3 channel (6), AMEND-3 findings note) is byte-exact and strictly more
precise than the QC's citation. Neither version affects any store count or the S-immutability conclusion.

---

## SECTION C — RESIDUAL FINDINGS (this re-QC's own)

### **P3-R1. AT_RUN_END_GIT_OBSERVATION.md was amended in the correction pass but has NO AMEND_LOG entry**
- LOCATION: 00_CONTROL/AMEND_LOG_R1.md (no entry covering 01_RAW/AT_RUN_END_GIT_OBSERVATION.md) vs the file's
  .pre copy (00_CONTROL/PRE_EDIT/01_RAW/AT_RUN_END_GIT_OBSERVATION.md.pre, 2998 bytes, B575241382D8882AF426B4FF
  214EAC985D87851E2A352BC9E56710AB107FA1BC) and the current file (4968 bytes, A98153CA89F7DC6BF94FB58BF2806A76
  5C54B6DDDE1A497B24201AE2D97433FC, mtime 07:34:13 — inside the correction window).
- CONTRADICTED CLAIM (as worded): AMEND_LOG's correction-pass convention: "every amended file has a byte-exact
  .pre copy under 00_CONTROL/PRE_EDIT/ (mirrored relative path + '.pre'); entries below list finding ID, file,
  exact change, why, and the .pre/new SHA256 pair" — satisfied for all 18 other amended files, NOT for this one.
- WHAT HAPPENED (measured): a "CORRECTION-PASS GIT OBSERVATION" appendix was appended (append-only:
  BYTE_PREFIX=True; no pre-correction byte changed). The appendix is SELF-DECLARING (states the correction-pass
  context, HEAD, untracked census, reflog check, S0 re-verification) and every git claim in it is independently
  verified by me (A.8: HEAD/status/reflog all MATCH).
- WHY ONLY P3: the provenance chain is intact via the .pre copy + manifest rows; the appendix discloses itself
  inline; no science content; no evidence damage; the gap is correction-LOG completeness only.
- NARROW CORRECTION (optional, append-only, does not block G17): append an AMEND-13 entry recording the
  AT_RUN_END appendix (file, exact change = correction-pass git observation appendix, why = QC-order git
  re-measurement, .pre/new SHA pair B5752413.../2998 -> A98153CA.../4968). Alternatively PE-MASTER may accept
  the appendix's inline self-declaration as sufficient and note the gap in the G17 record.

### Observations (non-numbered; no correction required)
- O-1: the AT_RUN_END appendix prose (line 84) writes "00_Control/scripts/census_triple_writes.py" with a
  lowercase 'c' ("00_Control"); the actual directory is 00_CONTROL (Windows paths are case-insensitive; the
  reference resolves; the manifest/index/AMEND-3 all spell it correctly). Cosmetic.
- O-2: census_triple_writes.py [T.10] channel (9) formats the IMM_TO_MEM count with a hardcoded literal
  ("... %d real ..." % 0) rather than a measured variable. The 0 is CORRECT and fully backed by the [T.2]
  breakdown (no IMM_TO_MEM_POINTER_CANDIDATE row appears among the 268 classified occurrences), so no claim is
  false; the hardcode is a style weakness recorded for the trap library, not a defect requiring correction.

---

## SECTION D — COVERAGE

**Independently re-measured from EXE bytes (my own probe code):** EXE identity (size+SHA, at re-QC start);
PE header/sections; whole-image dword census of the triple (107/81/80=268, per-section); containment
classification of all occurrences with my own store-encoding pattern detector (0 store candidates); load
decomposition (42+39 / 13+68 / 20+60 A1/8B); push-taker census (24 sites, exact VA list, all same imm32);
mov-imm taker census (2: 0x50AA1D, 0x96B960); widened dword scan 0xBA9215..0xBA9227 (1 candidate @0x96BB5D,
0 overlapping); computed-base windows (22/45 and 34/349); zero-init tail (RVA vs raw end; va2off None);
K qword at 0xA7B360 (bitmatch vs recomputed (double)(float)0.01); padding bytes at 0x50A0AA (6x CC) + next
function head 0x50A0B0; 0x930020/0x930040 function families (ECX=[this+0x4C] at 0x930023/0x930053; the two
mid-instruction cell positions); 0x7B468E lea anchor + fsub uses; SEH frame 0x437F70..0x437F8B + 0x437FA4
(89 44 24 04); 0x8DC5B0/0x8DC5C0 thunks + all 3 E8 callers' push operands + 0x5F6D21->0x8DC5C0 adjacency;
0x92FFE0 head (read-only SRC into 0x82B6A0); 0x48BAC0 first/secondary ECX redefinitions; E8 caller counts
(0x50AA10=4, 0x96B960=1, 0x82B5A0=36, 0x437F70=99); push-site -> first-call mapping (all 24; 0x50C272 and
0x50CDB3 confirmed 0x6C9490 with wider windows).

**Hash/consistency censuses (my own):** all 32 AMEND_LOG hash tokens resolved against disk; all 19 .pre
copies hashed; all current files vs recorded new SHA256; MANIFEST 52/52 re-hashed; EVIDENCE_INDEX 51/51
re-hashed; index<->manifest 51/51; SCRIPT_SHA256 5/5; README row vs disk; QC_AUDIT/RUN_CONTRACT/
SOURCE_IDENTITIES/AT_RUN_START untouched checks; AMEND_LOG byte-prefix append-only proof; package census
53 = 52 + 1; UTF-8 validity 53/53; hygiene walk; mtimes.

**Read to EOF:** AMEND_LOG_R1.md; ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt (1079 lines); census_triple_writes.py
(929 lines); decode_lib.py (203 lines); END_TO_END_VALUE_FLOW_RAW.txt; REPORT.md; HANDOFF.md;
STAGE_ACCEPTANCE_GATES.csv; SCIENCE_STATUS_DELTA.csv; EVIDENCE_INDEX.csv; README.md (03_EVIDENCE);
MANIFEST_SHA256.csv; SCRIPT_SHA256.csv; AT_RUN_START_GIT_OBSERVATION.md (114 lines); AT_RUN_END_GIT_
OBSERVATION.md (97 lines); QC_AUDIT.md (the original, 151 lines); HELPER82B5A0_CALLER_CENSUS.csv;
FUN_0050A050_DOWNSTREAM_DISASM.txt ([A.3] pin table region + AMEND NOTEs; 156-line file read in the
correction-relevant parts); every .pre->current diff hunk for all 10 amended files (REPORT, HANDOFF,
HELPER_OPERATIONS, FUN_0050A050, FUN_00437F70, HELPER82B5A0 csv/txt, SOURCE_VECTOR_LAYOUT_RAW,
SCIENCE_STATUS_DELTA, gen_manifest.py, gen_raw_evidence.py).

**NOT_CHECKED / out of re-QC scope (disclosed):**
1. The science conclusions themselves (G3/G5/G9-G14 hypothesis dispositions, layout proofs, fallback
   comparison, negative controls) — already independently verified by the original fresh QC (Section B of
   QC_AUDIT.md) and explicitly OUT OF SCOPE for this targeted re-QC per the parent order.
2. Files NOT amended in the correction batch and not load-bearing for it: FUN_0082B5A0_DISASM.txt,
   POSITION_SEMANTICS.md, OUTPUT_VALUE_RELATION.md, SOURCE_VECTOR_LAYOUT.md, FALLBACK_PRIMARY_COMPARISON.txt,
   NEGATIVE_CONTROL_RAW.txt, HELPER437F70_CALLER_CENSUS.csv (hash-verified vs manifest only).
3. RUN_CONTRACT.md beyond the pin-block count and hash identity (not amended; hash matches the QC-recorded
   value); SOURCE_IDENTITIES.json full content (not amended; hash matches manifest; boot-input package
   identities were the formalizer's measurements).
4. Remote (network) git equality — only the local remote-tracking ref was re-measured (see A.8 note).
5. SEH handler body 0x99C06B (unchanged disclosed residual, out of load path).
6. The executor's caller-census deep reads inside HELPER437F70_CALLER_CENSUS.csv rows beyond the NON-PAIR
   rows (P2-4 scope; the 99-row file was QC-verified in the original pass and hash-verified here).
7. Whether a hypothetical computed base OUTSIDE [0xBA9000,0xBA92C0) with compensating disp32 reaches the
   triple — census [T.10] discloses this channel as not exhaustively hunted (residual, unchanged);
   the original QC's own independent hunt covered [0xBA9000,0xBA921C) only, so the executor's window is
   strictly broader than the QC's.

**Probe trail:** C:\Users\User\AppData\Local\Temp\opencode\qc935r2\ (probe1_amendlog_hashes.py,
probe2_hashpairs.py, probe3_logtokens_atrunend.py, probe4_manifest_index.py, probe4b_index_mtime.py,
probe5_gate_delta_diff.py, probe6_text_diffs.py, probe7_bytes_a.py, probe8_bytes_b.py, probe9_bytes_redo.py,
probe10_residual_bytes.py, probe11_text_scan.py; full package hash table in pkg_hashes.txt).

---

## SECTION E — G17 READINESS (for PE-MASTER)

- The correction batch closes both material findings (P1-1, P1-2) and all count/wording/provenance findings
  (P2-1..P2-4, P3-1..P3-3) with byte-verified backing; the package is INTERNALLY CONSISTENT (manifest/index/
  scripts/AMEND_LOG/.pre chain all re-hash clean).
- The single residual P3-R1 (AMEND_LOG entry missing for the AT_RUN_END appendix) is mechanical, disclosed
  here, and does not undermine any evidence or conclusion. In this re-QC's judgment it does NOT block G17
  persistence; PE-MASTER may either order an append-only AMEND-13 note or accept the appendix's inline
  self-declaration and record the gap in the G17 commit/persistence record.
- THIS file (06_REPORT/QC_AUDIT_R2.md) is the ONLY file created by this re-QC; it is NOT covered by
  MANIFEST_SHA256.csv / EVIDENCE_INDEX.csv / SCRIPT_SHA256.csv (self-hash discipline; written after the
  re-hash censuses above). If PE-MASTER persists the package at G17, the manifest/index regeneration question
  for this file belongs to the persistence assignment.
- This re-QC is an INTERNAL re-verification result. It is NOT MASTER_ACCEPTED, NOT G16 adjudication, NOT
  milestone closure. G16 (PE-MASTER adjudication) and G17 (path-limited persistence by pe-master-auditor)
  remain with the governance chain.

RE_QC_HANDOFF: ASSIGNMENT_MODE=TARGETED_RE_QC (fresh-context post-correction verification) /
RUN_ID=REQC_PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915_R2 / verdict=RE_QC_PASS_WITH_FINDINGS /
P0=0, P1=0, P2=0, P3=1 (+2 observations) / all 9 correction items LANDED and byte-verified / both
discrepancies adjudicated from bytes (executor correct both times; S-immutability unaffected) / package
READY for G16->G17 in this re-QC's judgment, with P3-R1 to be noted (AMEND-13 or G17-record disclosure).
