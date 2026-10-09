# AMEND_LOG — PE_935_TEMPLATE_4057_CONSUMER_CHAIN_R1_20261009

- **Round**: records-correction round R1 (2026-10-09), in-place, PRE-PERSISTENCE.
- **Executor**: pe-reconstruction (the run's own executor; NOT an independent audit).
- **Authority**: PE-MASTER bounded records-only correction round (max this one round), worklist = the
  findings ledger of the fresh internal QC (`QC_RESULTS.json` / `QC_REPORT.md` in this package root,
  verdict QC_PASS_WITH_FINDINGS). Mandatory P2: F-QC-1..F-QC-4; recommended P3: F-QC-5..F-QC-10.
- **Scope guard (what this round did NOT do)**: no science values changed, no census counts changed,
  no window classifications changed, no new analysis, no Ghidra, no EXE reads (the only physical
  read outside the package was a read-only SHA256 re-hash of the c2 script for F-QC-1 revalidation).
  QC artifacts (`QC_RESULTS.json`, `QC_REPORT.md`), the SCRATCH and AUDIT_ENTRYPOINT.md untouched.
  No commit, no push. No MANIFEST created (persistence remains the orchestrator's).
- **Findings resolution**: F-QC-1..F-QC-10 ALL RESOLVED this round; none carried.

## 1. Changed files and their hashes

| File (package-relative) | SHA256 pre-edit | SHA256 post-edit |
|---|---|---|
| `EVIDENCE_INDEX.md` | `BA08D16FA813C605D6E61061EE91FEF058F4B9D11284C69FB2F2EBB597E8C35A` | `FCEF38F795EE08805A8973D74F9FF666C767137E5B4A481999A033D8CB815A31` |
| `FINAL_REPORT.md` | `64AD39A0B9B9D16EF5A26C4C4D9027AA86D12A814F5C094947C28131775FBB0C` | `505E793E0F638DB72F45D2DB7DAC0F4D3FAB5AC9986245F17591C0416A8100FD` |
| `HANDOFF.md` | `B5EA08CD6991A683716F1B8A754D2E7AC96333FF6C8EDCFBCF5EF4CE78456E8B` | `E03BB125BC7D296EF5D0FECB5A610C15C311F96A9FC3CE2A3F2B7790D9C99FDF` |
| `CALLER_CENSUS.json` | `86E37C5A6289AFBFFCACB62E2D0D77CC1E98506EDECD61CEA98E79B12DF64FDE` | `82D5A71F487C7F789930DA2FDDD063E7CA0625D762302BB48BDCCDE651011A97` |
| `01_RAW\ID_TABLE_DUMPS.json` | `99F46B9B0123AD209D943031A00E75F540EC20F7AEBFA4B2E6FFDA8A89F1D2A6` | `9698AEB22B610594A89C1005B29CB08A0CEC9FD132C0FDD7A3E0D3BDE30E6710` |

The four pre-edit values above equal the run-final values originally recorded in
`EVIDENCE_INDEX.md` §3 (verified before editing). `AMEND_LOG.md` (this file) is new, created by this
round; its own SHA256 is not self-recorded here (the persistence-phase MANIFEST covers it).

## 2. Every change, old → new, with reason

### EVIDENCE_INDEX.md

1. **§2, row "c2_ghidra_census.py (EXECUTED version)"** — SHA256
   `D073EC73994FA3B2A64898CFA6482CFF4FBB111203893C63D59E009AD16091` (62 hex chars, invalid length)
   → `D073EC73994FA3B2A64898CFA6482CFF4FFBBB111203893C63D59E009AD16091` (64 hex chars).
   **Reason F-QC-1 (P2, mandatory)**: transcription slip ("FFBBB"→"FBB"). The value was
   re-measured this round (read-only SHA256 of
   `99_Audits\PE_935_TEMPLATE_4057_CONSUMER_CHAIN_R1_20261009\SCRATCH\scripts\c2_ghidra_census.py`,
   mtime 09:52:03, predating the run outputs 09:52:20–24, i.e. the executed bytes) — measured value
   equals the QC-recorded actual value; 64-char length asserted.
2. **§5, `.pyc` bullet** — "`.pyc` residue: 0 in run scratch, 0 in package, 0 in historical
   package, 0 in cwd (all `python` invocations used `-B`)." → scoped to residue **created by this
   run** in its own locations (run scratch / package / historical package), plus disclosure that
   the repo tree (cwd) contains pre-existing foreign untracked .pyc/__pycache__ artifacts that
   predate this run (none created by it) and are out of scope of the claim.
   **Reason F-QC-5 (P3)**: the unqualified "anywhere/cwd" wording was over-broad.
3. **§3 hash block** — the SHA256 lines for `01_RAW\ID_TABLE_DUMPS.json`, `CALLER_CENSUS.json`,
   `FINAL_REPORT.md`, `HANDOFF.md` refreshed from the pre-correction values (preserved in the table
   above) to the post-correction values; plus an added "Hash refresh (records-correction round R1)"
   note paragraph after the block.
   **Reason**: consistency follow-through of this round's in-place corrections — the §3 block
   ("computed after final write") would otherwise carry stale hashes for the four amended files
   (same manifest-identity defect class F-QC-1 fixed). All other §3 values unchanged from the run's
   final write.

### FINAL_REPORT.md

4. **§1, FUN_0043A550 row** — "Both paths RET with EAX = the singleton." → "Success and
   already-exists paths RET with EAX = the singleton; the alloc-failure path stores 0 and RETs
   with EAX = 0 (NULL)."
   **Reason F-QC-6 (P3)**: the alloc-fail path (JE @0x0043A592 → `33 C0` @0x0043A5B0 → store 0
   @0x0043A5B2 → RET @0x0043A5C6) returns 0, not the singleton.
5. **§3 table row 6 (FUN_006c2750)** — "dword[0x00A85778 + (A+40B)*4]" →
   "dword[0x00A85778 + (A+10B)*4]".
   **Reason F-QC-2 (P2, mandatory)**: physical bytes `8D 04 80` @0x006C2772 (LEA EAX,[EAX+EAX*4]
   → 5B) then `8D 0C 47` @0x006C2775 (LEA ECX,[EDI+EAX*2] → A + 2·5B = **A + 10B**); the 10-dword
   table dump equals the A-bound (10), corroborating stride 10.
6. **§3 table row 7 (FUN_006c27a0)** — "dword[0x00A857C8 + (A+40B)*4]" →
   "dword[0x00A857C8 + (A+10B)*4]". **Reason F-QC-2** (same, window 06 at 0x006C27C2/C5/C8, +0xE
   field variant).
7. **§3 closing note** — "All callee bodies involved (16 names) stay CLOSED this run — only call
   edges were recorded." → "All in-window callee bodies stayed CLOSED this run — only call edges
   were recorded; the 12 windows contain 92 distinct non-subject call targets and none was opened.
   The classification-relevant callee names (…same 16 names…) are the 16 cited across the
   classifications (14 of them among the 92 in-window targets; FUN_0052a260 and FUN_004d1430 are
   callee edges of the census subjects' own bodies — §1)."
   **Reason F-QC-9 (P3)**: the 16-name enumeration is the classification-relevant subset, not the
   full in-window callee universe. The 92 count was independently re-derived this round from the
   12 window JSONs' `calls_inside_window` target sets (subjects excluded) and matches the QC
   record; the 14/16 vs 2/16 split was derived from the same re-count.
8. **§4(b) answer** — "**NO — within the 12 in-budget windows (STATIC_ONLY).** Zero direct field
   accesses … All consumption is: [pointer STORE …] and [pointer FORWARD …]." → "**NO
   transform-relevant access ESTABLISHED on the returned template object — within the 12
   in-budget windows (STATIC_ONLY); one read pattern on an UNKNOWN-identity derived object
   recorded.**" plus a new bullet recording the byte-pinned in-window reads of the FUN_0040b070
   result: [EAX+0x4] @0x006C3FBE (`8B 50 04`) and [EAX] @0x006C3FC1 (`8B 00`) — object derived
   from the template by method call, identity UNKNOWN while the callee is CLOSED — forwarded as a
   pair into FUN_006c3640 @0x006C3FCD; no float evidence in-window; transform/position relevance
   UNKNOWN. Follow-up sentence extended: FUN_0040b070 added alongside FUN_0072fce0 / the
   FUN_007ce1e0 getter family.
   **Reason F-QC-4 (P2, mandatory)**: the pre-registered (b) asks about objects derived from the
   template; window FUN_006c3f50 reads two fields of a derived result in-window, which the old
   "all consumption is STORE or FORWARD" enumeration did not disclose. (The reads are byte-pinned
   in the existing window artifact `c2_caller_08_006C3F50.json` — no new measurement was made.)
9. **§6 G1** — "PASS (12/12 classes × 2 functions, each with method + result)." → "PASS (10/10
   classes × 2 functions, each with method + result)." NOT_CHECKED sub-class note kept unchanged.
   **Reason F-QC-3 (P2, mandatory)**: the pre-registered class universe is C1..C10 = 10 classes
   (PREREGISTRATION §4, FINAL_REPORT §2 table, CALLER_CENSUS reference_classes = 10 keys); 12 is
   the caller-window budget, not the class count.
10. **§6 G3** — "Zero .pyc residue anywhere (scratch, package, historical package, cwd)." →
    scoped to residue created by this run in its own locations, plus the pre-existing foreign
    untracked .pyc/__pycache__ disclosure (predates the run; out of scope of the claim).
    **Reason F-QC-5 (P3)**.
11. **NEW §8 "FULL_READ_LOG (consolidated read/closed discipline — STATIC_ONLY)"** appended after
    §7. **Reason F-QC-10 (P3)**: consolidates the read/closed discipline that was previously
    distributed across PREREGISTRATION §5.1/5.2, FINAL_REPORT §3 and the census. Content is drawn
    only from existing run records (physical reads = EXE only; decoded = subjects + datum refs +
    12 windows; CLOSED = 92 in-window targets + subject-body edges + 20 not-analyzed callers;
    hash-read-only = landmark package + sandbox EXE; Ghidra project reuse disclosed; client never
    ran). No new measurement.

### HANDOFF.md

12. **Gates, G1 line** — "12/12 reference classes (C1..C10) enumerated for 2/2 functions" →
    "10/10 reference classes (C1..C10) enumerated for 2/2 functions". **Reason F-QC-3 (P2)** (the
    old wording was internally self-contradictory: 12/12 vs C1..C10).
13. **Gates, G3 line** — "0 .pyc residue (4/4 locations checked)" → run-scoped wording (0 residue
    created by this run in its own locations; all invocations used `-B`) plus the pre-existing
    foreign untracked .pyc/__pycache__ disclosure (predates the run; out of scope of the residue
    claim). **Reason F-QC-5 (P3)**.
14. **15-line census summary, item 11** — "(b) NO — zero direct field accesses on the returned
    template in ALL 12 windows; consumption = pointer-store into caller structures or
    pointer-forward." → "(b) NO transform-relevant access ESTABLISHED — zero direct field accesses
    … ; one read pattern on an UNKNOWN-identity derived object recorded (FUN_006c3f50:
    [EAX]/[EAX+4] @0x006C3FBE/C1 of the FUN_0040b070 result, forwarded to FUN_006c3640; transform
    relevance UNKNOWN)."
    **Reason F-QC-4 (P2)**: this summary line repeated the old (b) wording and would have
    contradicted the corrected §4(b)/question_answers records.
15. **15-line census summary, item 15** — follow-up candidates extended with FUN_0040b070 ("its
    result is field-read in-window in FUN_006c3f50"). **Reason F-QC-4 (P2)**: FUN_0040b070 belongs
    on the follow-up list (QC adjudication).
16. **Final section** — "AUDIT_ENTRYPOINT.md untouched (it does not exist yet)." → "no
    docs\audits\AUDIT_ENTRYPOINT.md exists and no entrypoint row was created (persistence
    pending) — the repo-root AUDIT_ENTRYPOINT.md is untouched."
    **Reason F-QC-7 (P3)**: the repo-root AUDIT_ENTRYPOINT.md DOES exist (tracked, byte-unchanged,
    git-verified by the QC); what does not exist is docs/audits/AUDIT_ENTRYPOINT.md.

### CALLER_CENSUS.json

17. **4× classification `id_source_detail.index_inputs` note** (FUN_006C2750 and FUN_006C27A0,
    each in BOTH targets' `analyzed_in_depth` blocks) — `"index = A + 40*B"` →
    `"index = A + 10*B"`. **Reason F-QC-2 (P2, mandatory)** (same physical-byte correction as
    change 5/6; LEA texts and all other index_inputs entries unchanged — they were verified
    correct by the QC).
18. **`question_answers.b_transform_relevant_field_access`** — `answer`:
    "NO (within the 12 in-budget windows; STATIC_ONLY)" → "NO transform-relevant access
    ESTABLISHED on the returned template object (within the 12 in-budget windows; STATIC_ONLY);
    one read pattern on an UNKNOWN-identity derived object recorded"; `detail`: "All consumption
    is: …" → "All template consumption is: …" + appended RECORDED derived-object read pattern
    (same byte-pinned facts as change 8); `closed_callee_note`: extended with "FUN_0040b070
    (whose in-window result is field-read in FUN_006C3F50) belongs on that follow-up list
    alongside FUN_0072fce0 and the FUN_007ce1e0 family".
    **Reason F-QC-4 (P2, mandatory)**.
19. **2× window-8 (FUN_006C3F50) `returned_object_role.note`** (both targets' blocks) — appended:
    "recorded in-window reads [EAX+0x4] @0x006C3FBE ('8B 50 04') and [EAX] @0x006C3FC1 ('8B 00')
    target the FUN_0040b070 RESULT (object derived from the template by method call, identity
    UNKNOWN while the callee is CLOSED), forwarded as a pair into FUN_006c3640 @0x006C3FCD -
    transform relevance UNKNOWN". **Reason F-QC-4 (P2)**: QC correction names the window-8
    classification note. The classification values themselves (`class`, `field_accesses_on_template:
    []`, `transform_relevant_access: false`) are UNCHANGED — no window classification changed.

### 01_RAW\ID_TABLE_DUMPS.json

20. **5 A-family table `note` fields** (ACCESSOR_TABLE_FUN_006c26b0/2700/2750/27a0/27f0) —
    "dwords consumed by the accessor's bounds-checked index range; …" → "row-0 (B=0) dwords of the
    accessor's table, covering the bounds-checked A range (rows B>=1 not dumped; row stride = the
    A bound); values at these positions are pushed directly as the FUN_0072F580 lookup key;
    BYTE_OBSERVATION only". **Reason F-QC-8(i)**: the dumps cover only the B=0 row.
21. **ACCESSOR_TABLE_FUN_006c2700 (va 0x00A855D0) `note`** — additionally discloses: "dwords 0-7
    are NOT ids - 4 code VAs plus a string tail (bytes spelling 'ClickTargetNode') - id-ranged
    values start at dword 8 and cover the rest of the bounds-checked A range".
    **Reason F-QC-8(iii)**: the mixed first row of 0x00A855D0 (the string bytes are the dumped
    dwords 0x63696C43/0x7261546B/0x4E746567/0x0065646F read as ASCII — no new measurement).
22. **2 twin table `note` fields** (ACCESSOR_TABLE_FUN_006c2840/2870, va 0x00A858B4/0x00A858BC) —
    → "B*4-indexed dwords with NO bounds check on B in the accessor window (the bounds-checked
    list covers only the A-family accessors); dwords 0-4 are id-ranged, dwords 5-7 adjoin
    non-table data (code VAs / zeros) which the accessor would read as keys if B reached there -
    so a 'consumed range' beyond the id-ranged positions is an assumption (B's producer
    FUN_006b22d0 is CLOSED, its value range UNKNOWN in-window); …".
    **Reason F-QC-8(ii)**: the 37-B twins have no bounds check on B, so "consumed" is an
    assumption there.
23. **`interpreted.ID_TABLE_CLASSIFICATION`** — "all 7 accessor tables contain id-ranged small
    integers … at the dword positions the accessors bounds-check; … the two 37B twins' tables
    adjoin non-table data (code VAs / zeros) after their consumed range" → corrected statement:
    5 A-family tables with row-0 dump scope (rows B>=1 not dumped), the 0x00A855D0 mixed-first-row
    exception, and the twins' no-bounds-check-on-B assumption. **Reason F-QC-8(iii)**:
    overgeneralization corrected.
24. **UNCHANGED in this file**: all measured `first_n_dwords_hex` / `first_n_dwords_decimal`
    values, `exe_sha256`, `NO_4057_IN_TABLES`, `errors`, table VAs and key names.

### Verified-not-needed (no edit)

- **`01_RAW\C2_CALLER_WINDOWS\c2_caller_05_006C2750.json` / `c2_caller_06_006C27A0.json`** (F-QC-2):
  inspected — they are raw c2 listing/decompile artifacts and contain NO index-formula notes; the
  decompiles already embody the correct stride (`(sVar1 + iVar2 * 10) * 4`). Nothing to correct.
- **`01_RAW\C2_CALLER_WINDOWS\c2_caller_08_006C3F50.json`** (F-QC-4): inspected — it already
  contains the byte-pinned reads (`8B 50 04` @0x006C3FBE, `8B 00` @0x006C3FC1) in its raw listing;
  the disclosure was added to the summary records (changes 8/14/18/19), not to the raw artifact.
- **FINAL_REPORT §3 pointer line** "`01_RAW\ID_TABLE_DUMPS.json` holds the measured table dwords
  (id-ranged small integers, e.g. 11602, 15591, 16104; **no 4057**)" — reviewed and left unchanged:
  the cited values are id-ranged examples and the "no 4057" claim is QC-confirmed; the QC findings
  ledger did not list this line.

## 3. Post-edit verification (executor self-check, NOT an independent audit)

- Every edited file re-read after editing; internal consistency confirmed (cross-references
  between FINAL_REPORT §3/§4(b)/§6/§8, HANDOFF gates + 15-line summary, CALLER_CENSUS
  question_answers/classifications, EVIDENCE_INDEX §2/§3/§5).
- `CALLER_CENSUS.json` and `01_RAW\ID_TABLE_DUMPS.json` parse as valid JSON post-edit.
- `EVIDENCE_INDEX.md` §3 hash census re-run post-amendment: **21/21 MATCH** against the actual
  files (including the four refreshed values).
- The corrected c2 field: 64 hex chars, **equal to the SHA256 of the on-disk executed script**
  (re-measured this round).
- Package-wide defect-string sweep (excluding the QC artifacts, which quote the defects as
  findings): **0 occurrences** of any pre-correction defect string
  ("A + 40*B", "(A+40B)", "12/12 classes", "12/12 reference classes", the 62-char hash,
  "Zero .pyc residue anywhere", "Both paths RET with EAX = the singleton",
  "All callee bodies involved", "it does not exist yet", "dwords consumed by the accessor",
  "0 .pyc residue (4/4").
- The 92-distinct-target count used in the F-QC-9 correction was independently re-derived from the
  12 window JSONs before being written (matches the QC record).
- Git: no commit, no push; HEAD remains `9124e8e` (BASE_SHA); the package remains untracked.
- No science value, census count or window classification changed anywhere in this round.
