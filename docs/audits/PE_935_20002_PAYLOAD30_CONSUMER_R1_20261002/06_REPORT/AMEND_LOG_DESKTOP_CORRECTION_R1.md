# AMEND_LOG_DESKTOP_CORRECTION_R1 — PE_935_20002_PAYLOAD30_DESKTOP_CORRECTION_R1_20261002

- RUN_ID = PE_935_20002_PAYLOAD30_DESKTOP_CORRECTION_R1_20261002 (the correction run of the
  package PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002, performed INSIDE that package)
- AMEND_ROUND = DESKTOP_CORRECTION_R1 (one focused correction cycle per
  00_CONTROL\DESKTOP_CORRECTION_R1\CORRECTION_RUN_CONTRACT.md; the normative
  transcription of the human decision PE_935_20002_PAYLOAD30_DESKTOP_CORRECTION_AUTH_R1_20261002)
- DISPATCHED_BY = PE-MASTER (direct), after the independent ChatGPT Desktop post-audit
  verdict DESKTOP_POST_AUDIT_VERDICT = REQUIRE_CORRECTIONS
- EXECUTOR = pe-reconstruction (the original executor role, performing the correction;
  NO_NESTED_TASKS)
- AMEND_EXECUTED_UTC = 2026-10-02 (executor session; correction-contract preflight re-verified
  at start — 01_RAW\DESKTOP_CORRECTION_R1\PREFLIGHT_RERUN.json: HEAD/contract/EXE/VFS/manifest
  all MATCH)
- GIT OPERATIONS = NONE (no commit, no push, no stage; HEAD == BASE_SHA ==
  9203b6d1ad5025f4158d5165863594132aaac49f unchanged; the package dir remains untracked)
- CLIENT LAUNCH = NONE (static analysis only; Entropia.exe never launched; no hooks; no
  original file modified)
- SCIENCE CHANGES = ONE FOCUSED CORRECTION (the branch-selection re-derivation and the
  dependent documentation corrections; NO new science question opened; every
  load-bearing claim re-pinned from the pinned EXE/VFS bytes by this correction's own
  tooling)

## 1. The Desktop finding (why this correction exists)

The independent ChatGPT Desktop post-audit of the package found (Desktop P1): the
value-read dispatch FUN_0075F660 does NOT go straight to the flags-bit0/typed-reader
path. It FIRST tests [descriptor+0]; when that field holds a non-NULL object (the case
for tag ID 17), the dispatch takes a VIRTUAL branch calling
[[descriptor+0].vtable+0x14]. The package's active selected-reader trace
(FUN_00412540 @0x00412553/0x0041255A via FUN_004129c0 case 1) described the FALLBACK
path (requires descriptor+0 == NULL) and was therefore NOT the selected execution path
for the 20002.vfs tag-0x11 parse. Verdict: REQUIRE_CORRECTIONS; one focused correction
cycle authorized.

## 2. The superseded claim

- OLD (superseded): READ_FUNCTION = FUN_00412540 (the type-1 scalar value reader;
  reached via FUN_00726900 -> FUN_0075f660 @0x726A1B -> flags bit0 test @0x75F687 ->
  scalar path -> FUN_004129c0 @0x4129DF); READ_INSTRUCTION_VA = 0x00412553;
  READ_INSTRUCTION_FILE_OFFSET = 0x00125553 (a DIGIT-SHIFT transcription error — the
  correct fallback offset is 0x12553, which the run's own immutable pin JSON always
  recorded); STORE @0x0041255A; RUN_STATUS = CONSUMER_REACHED_ROLE_STRONGLY_SUPPORTED.
- NEW (proven by this correction; 01_RAW\DESKTOP_CORRECTION_R1\BRANCH_SELECTION_TRACE.json,
  96/96 pins, all rel32 targets computed): the tag-ID-17 descriptor's +0 field holds
  the static ArkRTTraitsInt reader object 0x00BA937C (returned by the factory
  FUN_00977a50 on BOTH its lazy-init and already-initialized paths — never NULL; no
  NULL-return path exists in the function), stored into descriptor+0 by the
  registration dataflow (FUN_0070cbc0 arg5 -> FUN_0075f5c0 -> MOV [EAX],ECX
  @0x75F5CA) and preserved into the class descriptor table by FUN_0070c980 ->
  FUN_0070c7b0 (element+0 copied @0x70C7C1/0x70C7C3). Therefore in FUN_0075F660 the
  TEST ECX,ECX @0x75F664 (ECX = [descriptor+0]) does NOT take the JZ @0x75F66E: the
  VIRTUAL BRANCH IS SELECTED. The slot: [0x00BA937C] = vtable 0x00A9C670 (the
  factory's runtime vtable store @0x977A68); [0x00A9C670+0x14] = the dword at
  0x00A9C684 (FO 0x69C684, bytes F0 77 97 00) = 0x009777F0. THE SELECTED READER =
  FUN_009777F0; its RTTI class = .?AUArkRTTraitsInt@@ (ArkRTTraitsInt).
- Corrected §18 chain values: READ_FUNCTION = FUN_009777F0; READ_INSTRUCTION_VA =
  0x00977807; READ_INSTRUCTION_RVA = 0x00577807; READ_INSTRUCTION_FILE_OFFSET =
  0x00577807; READ_INSTRUCTION_BYTES = 8B 04 10; STORE_INSTRUCTION_VA = 0x00977810;
  STORE_INSTRUCTION_BYTES = 89 02; RUN_STATUS = CONSUMER_UNREACHED;
  DOWNSTREAM_CONSUMER_IDENTIFIED = NO; DEST_FIELD_IDENTIFIED = YES;
  FINAL_SEMANTIC_STATUS = UNVERIFIED; WORLD_INSTANCE_TO_MODEL_EDGE = NOT_TESTED;
  PLACEMENT_XYZ_RECOVERED = NO.
- The FALLBACK pins remain BYTE-CORRECT EVIDENCE OF A NON-SELECTED FALLBACK PATH
  (full record: 01_RAW\DESKTOP_CORRECTION_R1\FALLBACK_PATH_RECORD.json, 25/25 pins;
  reachability condition descriptor+0 == NULL; corrected file offsets 0x12553 /
  0x1255A; the old 0x00125553 transcription superseded).

## 3. The branch-selection correction summary (the science, condensed)

1. Registration of tag ID 17 (FUN_00761570 schema ctor): CALL FUN_00977a50 @0x76170F
   -> PUSH EAX (arg5, the reader object) @0x761714; PUSH 0 (arg4) @0x761715; PUSH 0xC0
   (flags) @0x761717; PUSH 1 (type) @0x76171C; PUSH 0x11 (tag) @0x76171E; MOV ECX,ESI
   (this = the class object) @0x761720; CALL FUN_0070cbc0 @0x761722.
2. Factory FUN_00977a50: TEST byte [0xBA9380],1 (lazy-init flag) @0x977A55; on first
   call: flag set, MOV dword [0xBA937C],0xA9C670 (THE VTABLE STORE) @0x977A68, the
   exit-destructor 0x00A744B0 (MOV dword [0xBA937C],0xA799E4 at exit) registered via
   the atexit-style helper 0x95D4DB (PUSH 0xA744B0 @0x977A63; CALL @0x977A72); BOTH
   paths return EAX = 0x00BA937C (non-NULL static .data address) —
   DESCRIPTOR_PLUS_0_VALUE = 0x00BA937C, proof class: byte-decoded registration
   dataflow + factory return (no assumption; control-flow reachability stated).
3. Descriptor-init dataflow: FUN_0070cbc0 pushes arg5 through FUN_0075f5c0
   (descriptor+0 = arg5 @0x75F5CA); field index = tag+4 @0x70CBF6; the local
   descriptor pointer returned in EAX -> FUN_0070c980(this=classObj, &desc) enforces
   tag == count (@0x70C9AE/0x70C9B0) and appends via FUN_0070c7b0: element =
   [classObj+0x88]-vector end (== begin + tag*0x10 given the invariant), all 4 dwords
   copied incl. descriptor+0, end += 0x10 (@0x70C7D8).
4. Lookup FUN_0070c180: descriptor = [classObj+0x88] + tag*0x10 (@0x70C1D3/0x70C1D6).
5. Dispatch FUN_0075F660: MOV ECX,[EAX] @0x75F662; TEST ECX,ECX @0x75F664; JZ ->
   0x75F687 @0x75F66E (fallback) — NOT TAKEN for tag ID 17 (descriptor+0 != NULL);
   virtual branch: MOV EDX,[ESP+0x10] (dest) @0x75F670; MOV EAX,[ECX] (vtable)
   @0x75F674; MOV EAX,[EAX+0x14] (slot) @0x75F676; PUSH EDX; PUSH ESI; CALL EAX
   @0x75F67B (this = the ArkRTTraitsInt object, arg1 = cursor, arg2 = dest).
6. The selected reader FUN_009777F0: cursor flag check @0x9777F4; bounds offset+4 <=
   limit @0x9777FD..0x977803; THE READ MOV EAX,[EDX+EAX*1] @0x00977807 (8B 04 10);
   dest load @0x97780A; THE STORE MOV [EDX],EAX @0x00977810 (89 02); advance 4 via
   FUN_0040de60 @0x977812; RET 8. ERROR PATH (separate, NOT the successful parse
   path): dest = 0 @0x97781E + cursor flag cleared @0x97782A.
7. Cursor provenance (01_RAW\DESKTOP_CORRECTION_R1\CURSOR_PROOF_CORRECTION_R1.json):
   the byte-derived increment table (entry offset 8 via FUN_0070dcf0's advance-8
   @0x70DDA2..0x70DDA8; flags u16 -> count u16 -> per-entry tag u16 + value widths
   per descriptor type: tag 1 = 8 bytes via the type-4 selected reader
   FUN_00409ed0->FUN_004099c0, tag 0xC = 4 via FUN_00977840, tags 0xD/0xE/0x10/0x11 =
   4 via FUN_009777F0) proves the cursor offset == 0x30 at the tag-ID-17 value read
   — re-derived for record 0 (raw BB 2E 00 00 = 11963), record 1014 (ANCHOR_ZERO,
   raw 00 00 00 00 = 0) and 1366/1366 records (own framing walk: 16 + 1366*128 ==
   174,864 exact EOF; full consumption offset == 56 == limit in 1366/1366; success
   path vs error/bounds-failure paths distinguished; 3 negative simulations DETECTED).
8. Destination provenance
   (01_RAW\DESKTOP_CORRECTION_R1\DESTINATION_PROOF_CORRECTION_R1.json, 23/23 pins):
   field index = descriptor+8 = tag+4 = 0x15 = 21 (@0x70CBF6/@0x75F5D7/@0x726A0E);
   value array = instance+0x40 (@0x726A11; allocation arithmetic byte-pinned
   @0x70D9B8/0x70D9BB/0x70D9BF: count(18)+4 = 22 slots); dest = value_array + 21*4 =
   +0x54 (SLOT 21) (@0x726A14); the dest passes through the dispatch's virtual branch
   (@0x75F670/0x75F679) into the reader's arg2 (@0x97780A) and is stored by
   @0x00977810 — width 4.

## 4. Desktop-lead agreement table (measured vs candidate per pin)

| DESKTOP LEAD | MEASURED | VERDICT |
|---|---|---|
| Factory = FUN_00977a50 (static .data singleton, lazy-init flag, runtime vtable store, atexit-style registration, never NULL) | object 0x00BA937C; flag 0x00BA9380; vtable 0x00A9C670; destructor 0x00A744B0; helper 0x95D4DB; return EAX=0x00BA937C on both paths | CONFIRMED |
| Virtual branch selected for tag ID 17 (descriptor+0 non-NULL) | TEST/JZ @0x75F664/0x75F66E not taken; descriptor+0 = 0x00BA937C | CONFIRMED |
| Virtual slot = [object.vtable+0x14] | [0x00A9C670+0x14] = dword @0x00A9C684 = 0x009777F0 | CONFIRMED |
| Selected reader = FUN_009777F0 | vtable slot dword = 0x009777F0; full decode matches the lead shape | CONFIRMED |
| READ VA 0x00977807 / FO 0x00577807 / bytes 8B 04 10 | VA 0x00977807; RVA 0x00577807; FO 0x00577807 (own PE32 section-table computation); bytes 8B 04 10 | CONFIRMED |
| STORE VA 0x00977810 / bytes 89 02 | VA 0x00977810; bytes 89 02 | CONFIRMED |

## 5. BEFORE/AFTER artifact list (every changed file; BEFORE copies byte-verified)

BEFORE values: 00_CONTROL\DESKTOP_CORRECTION_R1\BEFORE\BEFORE_COPIES_INDEX.json (10
copies; each byte-identical to the source at copy time). AFTER values measured at the
correction close:

| FILE | BEFORE size | BEFORE SHA256 | AFTER size | AFTER SHA256 |
|---|---|---|---|---|
| 02_ANALYSIS\FIELD_TO_DESTINATION_TRACE.md | 7306 | 4A19B69394BC1E9B32ABD5D00B998250A49D9DCDEE4A8CFC1949F428DFCD861B | 14730 | 1C69A05C2C0CB5782CC76B7D1234120DA59A9FD258B2FD7BDD1351F37DA74C2A |
| 02_ANALYSIS\CONSUMER_TRACE.md | 5001 | 11B995A93D67D72B3826EBE2F669E6F762AC2DD953154A5E65E37918894207D7 | 7500 | 14F4BA6B702E937F859F689260820CE69B474065644D115ADF30CF0C7CFB99C6 |
| 02_ANALYSIS\SEMANTIC_ASSESSMENT.md | 4395 | 797C5497F5BE76537EC3227ED3CE0E742E9B99995B2F628A3A1405B5C2181F56 | 5934 | C8F257E2D53897F57ADE768FCEB60FCBF39B5BCF98B4052E5657510D7448782F |
| 02_ANALYSIS\NEGATIVE_CONTROLS.md | 5966 | F2E66E3236F60CA06BD1B95B0BBB583E1E43AE4A09A6CAD9B5A863B9F3C6516B | 8400 | 56C2FF71A0C263E2FA383194A62099804113BF60702D1328A73AF4EDE0D7B1DA |
| 02_ANALYSIS\DESTINATION_CONSUMER_CENSUS.json | 5684 | 916CDF8B12640EAEB4402DDFF83388A20A259DA8C1783229F4CEE335994C3AA2 | 8836 | 8CA8248F4712741FCA8C56F10C6985DDBC146151956D20E6CA23C6EAB6454DC7 |
| 02_ANALYSIS\BLAST_RADIUS.md | 6061 | 3971527CF395E802FCC4407E65505374A55B8B16085421CD7C20F21E685A53A9 | 10478 | B698BFED510BE9B9C8A9A4BEF44A421FFAF0338EEBD640A59809634F6F8AA47F |
| 02_ANALYSIS\VFS_TO_PARSER_TRACE.md | 7893 | 77BA036A8083F7B19BB16026E753DEA3603C251F9F05F9BC38EBBA0F355853F1 | 8337 | FFF3386437A92D39C1A7153ABD781F8AB68A4551852A475BAAA5A2D92DB571C1 |
| 06_REPORT\REPORT.md | 10159 | B29BDB8E3E4CC140CD71C856B5B409A9D81252608EC7BD200EE708849CE2DF62 | 18055 | 9B9C3A468EFD7FF5C524B9BA6FE2AAE2FF2F38CC51602C9D3BC5639016611547 |
| 06_REPORT\EVIDENCE_INDEX.md | 6579 | E59CBDD2867332BB038F1C39A428CB5FA32A9DA016EF5F3F289CBA8C750E545B | 14565 | AF2CF382ED27E8E17A0CFDEB63735E8E310F02C4B309F8E78E387FB28E44B705 |
| 06_REPORT\HANDOFF.md | 8939 | 1865DA3295A91CC55DA67AC2E342F8ACC482731B458498E94808B558D573164B | 19197 | C9123409E269F5FE63CC7D5872A2DBABC250D3B3109369BD228E2A27D5FB7B90 |

All BEFORE values above are the authoritative full-length values from
00_CONTROL\DESKTOP_CORRECTION_R1\BEFORE\BEFORE_COPIES_INDEX.json (each copy
byte-identical to its source at copy time). The four BEFORE values for
BLAST_RADIUS.md, REPORT.md, EVIDENCE_INDEX.md and HANDOFF.md match the package's own
AMEND_LOG_R1 C1/C2/C6/C7 AFTER values, closing the chain back to the
manifest-verified pre-correction state.

NEW files created by this correction (no BEFORE state):
- 01_RAW\DESKTOP_CORRECTION_R1\PREFLIGHT_RERUN.json (the C0 re-measurements)
- 01_RAW\DESKTOP_CORRECTION_R1\BRANCH_SELECTION_TRACE.json (96/96 pins)
- 01_RAW\DESKTOP_CORRECTION_R1\FALLBACK_PATH_RECORD.json (25/25 pins)
- 01_RAW\DESKTOP_CORRECTION_R1\CURSOR_PROOF_CORRECTION_R1.json (cursor table + census + negatives)
- 01_RAW\DESKTOP_CORRECTION_R1\DESTINATION_PROOF_CORRECTION_R1.json (23/23 pins)
- 03_SCRIPTS\desktop_correction_r1\ (11 generators: pe_parse.py — this correction's own
  PE32 parser; s1_dump_regions.py; s1b_dump_vtables.py; s1c_dump_helpers2.py;
  s1d_dump_type4.py; s2_branch_pins.py; s3_fallback_path.py; s4_cursor_walk.py;
  s5_destination.py; s6_before_copies.ps1; s7_post_correction_bijection.py — the
  post-correction manifest-bijection verification; each generated artifact states its
  generator + generator SHA256)
- 06_REPORT\AMEND_LOG_DESKTOP_CORRECTION_R1.md (this file; NEW; self-hash self-excluded
  per the L12/C8 precedent — its size/SHA at close are reported in the delivery notice)

## 6. The QC1/QC2 superseded-conclusion record (contract §8; their reports immutable)

- QC round 1 (04_QC\QC_REPORT.md + QC1_*_RESULT.json + qc_tools\) and QC round 2
  (04_QC\QC_R2_TARGETED_REPORT.md + QC_R2_*_RESULT.json) verified the PRE-CORRECTION
  trace's BYTES (45/45 pins; the pure-copy window; the store site) and its delivery
  state. Those byte verifications remain CORRECT and are untouched.
- Their CONCLUSION that the tag-0x11 value read executes at 0x00412553/0x0041255A
  (the selected-reader attribution) is SUPERSEDED by the DESKTOP_CORRECTION_R1
  branch-selection proof: those instructions belong to the NON-SELECTED FALLBACK path
  (requires descriptor+0 == NULL; the tag-ID-17 descriptor+0 = 0x00BA937C). Their
  reports are immutable historical records of the pre-correction state and were NOT
  rewritten; future citations must use the corrected chain
  (01_RAW\DESKTOP_CORRECTION_R1\BRANCH_SELECTION_TRACE.json).
- Root cause recorded for the audit trail: the pre-correction trace verified
  instruction PRESENCE and bytes but did not prove PATH SELECTION (control-flow
  reachability from the proven descriptor state). The lesson (contract §8):
  **"correct instruction bytes != proven selected execution/parser path."**
- The FRESH targeted QC (QC-R3) with the required A/B/C discriminating detector (NULL-descriptor / non-NULL-descriptor / synthetic-slot variants) was subsequently EXECUTED as a separate PE-MASTER dispatch (2026-10-02; verdict PASS_WITH_FINDINGS; report 04_QC\QC_R3_DESKTOP_CORRECTION\QC_R3_REPORT.md; findings dispositioned in section 11 below).

## 7. The contradiction census (contract gate C5; executed AFTER the corrections)

Patterns swept across the whole package (files on disk, 420 files):

| PATTERN | HITS | DISPOSITION |
|---|---|---|
| "0x00412553" as THE client read | 42 lines | Active corrected docs: every hit labeled FALLBACK / non-selected / superseded (REPORT, EVIDENCE_INDEX, FIELD_TO_DESTINATION_TRACE §9a, CONSUMER_TRACE, SEMANTIC_ASSESSMENT, BLAST_RADIUS item 7, HANDOFF correction notice, the new 01_RAW correction artifacts and their generators). Immutable/historical (allowed to retain): 01_RAW\CLIENT_READ_BYTES.json (its role fields describe the fallback-path bytes — re-classified by this correction, byte-unchanged), the QC round-1/2 reports + tools (historical, §8), the historical generator script 03_SCRIPTS\s4_byte_pins.py (historical; NOT re-run — regenerating old artifacts would need the script corrected first, carried from the FUTURE-ADMINISTRATIVE-PASS list), the correction contract itself (quotes the superseded claim as the correction target), PE_MASTER_REVIEW.md (persistence-phase domain; its supersession is written in the persistence phase), the 10 BEFORE copies (preserved pre-correction evidence). |
| "FUN_00412540" as the selected reader | same disposition set | ONE stale LIVE copy found and CORRECTED: 02_ANALYSIS\VFS_TO_PARSER_TRACE.md line 40 listed the fallback chain (FUN_004129c0 + typed readers) as "THE record parser chain" — corrected to state the selected per-type reader objects via the virtual branch with the typed readers as the NON-SELECTED FALLBACK machinery (BEFORE copy made first; the routing conclusion GENERIC_PARSER_IDENTIFIED=YES / 20002_VFS_ROUTED_TO_GENERIC_PARSER=CONFIRMED is unaffected — the parser is the generic FUN_00726900 family either way). |
| "0x00125553" (the digit-shift transcription) | 14 lines | No live copy: the corrected docs cite it only as the SUPERSEDED transcription (with the corrected fallback offsets 0x12553/0x1255A); remaining hits = BEFORE copies, the correction contract (which declares it superseded), and the correction's own generator scripts/artifacts describing the supersession. |
| "CONSUMER_REACHED_ROLE_STRONGLY_SUPPORTED" as the current status | 15 lines | Active corrected docs cite it only as SUPERSEDED. Immutable/historical: PE_MASTER_REVIEW.md (persistence phase), QC round-1 report (historical), 00_CONTROL\RUN_CONTRACT.md (the historical original contract lists it as one value of the §12 taxonomy enum — not a claim), BEFORE copies. |
| "no statically-coded tag-0x11 reader exists" (unbounded) | 3 lines | Only in the explicitly-labeled HISTORICAL original-delivery section of HANDOFF.md ("SUPERSEDED by the corrected paragraph above — preserved as the historical record") and the BEFORE copies. The corrected state uses the bounded wording ("no statically-coded tag-0x11 reader was identified within the 202-site bounded census"). |
| "364 files" as the CURRENT count | 7 lines | Every hit is an explicitly-labeled historical delivery record (HANDOFF historical sections: "Historical delivery counts (preserved as historical records, NOT current)"), the historical AMEND_LOG_R1 entries, the historical QC-R2 report/tool, or a BEFORE copy. The CURRENT count at the correction close (420) is freshly measured in REPORT.md and HANDOFF.md with the physical-file/manifest-row/text-line/NOTE-row distinctions. |
| "17th property"/"17th descriptor" as current wording | 6 lines | Only in the labeled-historical HANDOFF paragraph, the contract's own convention instruction, and BEFORE copies. The corrected state uses "tag ID 17". |

CENSUS VERDICT: no contradictory live copy remains in the active (corrected) set; all
retained old-text occurrences are in immutable historical records, BEFORE copies, the
frozen contract, or explicitly-labeled historical sections, each allowed per contract
§3/§7/§8 and the BEFORE-copy discipline.

## 8. Remaining unknowns (unchanged by this correction; honest)

- Which runtime code reads ArkParameterArmor slot 21 (the downstream consumer) —
  UNVERIFIED (bounded census: 202 sites scanned; tag arguments are runtime variables).
- The gameplay semantic role of the tag-0x11 property — UNVERIFIED (the id2-domain
  membership observation stays CANDIDATE / UNVERIFIED context; numeric-domain overlap
  is not semantic proof).
- Global read-side exhaustiveness and global write-side exhaustiveness — UNVERIFIED
  (the one-caller observation is scoped to the censused parse machinery; W-1).
- WORLD_INSTANCE_TO_MODEL_EDGE = NOT_TESTED; PLACEMENT_XYZ_RECOVERED = NO.
- Whether tag 0x11 appears in the runtime serialization tag vector (FUN_00727110) —
  runtime state, not statically determined.
- The FUN_004123d0 dest-pair helper inside the type-4 reader chain (not further
  decoded; not load-bearing for the cursor/branch proofs — recorded as context).

## 9. The exact affected dependency set (what depended on the old selected-reader trace)

- 06_REPORT\REPORT.md — CORRECTED (the §18 CLIENT_READ chain fields; the statuses
  RUN_STATUS; the census wording; the fallback paragraph; the correction header; the
  counts section).
- 02_ANALYSIS\FIELD_TO_DESTINATION_TRACE.md — CORRECTED (the branch-selection proof
  section; the corrected SELECTED §9 trace; §9a the fallback re-label; the corrected
  field table; the corrected fallback file-offset note).
- 02_ANALYSIS\CONSUMER_TRACE.md — CORRECTED (answer steps 4-5; the bounded consumer
  wording; the evidence-chain table incl. the fallback row).
- 02_ANALYSIS\SEMANTIC_ASSESSMENT.md — CORRECTED (OBSERVED_OPERATION instructions;
  RUN_STATUS -> CONSUMER_UNREACHED; the fallback note).
- 02_ANALYSIS\NEGATIVE_CONTROLS.md — CORRECTED (NC-ANCHOR-ADJ instruction-level part
  re-referenced to the selected reader with an explicit feasibility re-check; NC-RECORD
  instruction reference; NC-VALUE precondition unchanged).
- 02_ANALYSIS\DESTINATION_CONSUMER_CENSUS.json — CORRECTED (the selected store site;
  the fallback store preserved as fallback; the write-scope description; the resolved
  factory object; the bounded wording).
- 02_ANALYSIS\BLAST_RADIUS.md — CORRECTED (item 7 added: the branch-selection
  supersession; item 5's consumer-gap statement corrected to CONSUMER_UNREACHED;
  items 1/2/6 preserved; the JOIN R1 claim-5 advisory supersession already recorded
  stays; no historical JOIN R1 file edited).
- 02_ANALYSIS\VFS_TO_PARSER_TRACE.md — CORRECTED (line 40's parser-chain listing; found
  by the contradiction census; BEFORE copy made).
- 06_REPORT\EVIDENCE_INDEX.md — CORRECTED (the §S4 rows; the new-artifact rows; the
  status labels; the S9 correction-governance rows).
- 06_REPORT\HANDOFF.md — CORRECTED (the correction delivery notice with the corrected
  result paragraph, evidence paths, counts; the original delivery notice preserved as
  explicitly-labeled historical).
- NOT dependent (explicitly dispositioned): 01_RAW\CLIENT_READ_BYTES.json (immutable;
  its pins are byte-correct FALLBACK-path + routing evidence), 02_ANALYSIS\VFS_TO_PARSER_TRACE.md's
  routing sections (unaffected conclusions — only the line-40 chain listing was
  corrected), the QC round-1/2 reports (immutable historical; conclusions superseded
  per §6 above), 06_REPORT\PE_MASTER_REVIEW.md (persistence-phase domain; NOT touched
  by the executor — its supersession is written in the persistence phase),
  06_REPORT\MANIFEST_SHA256.csv (regenerated LAST by the persistence worker;
  byte-unchanged), AUDIT_ENTRYPOINT.md (untouched), the frozen correction control
  files, the historical JOIN R1 package, 00_CONTROL\RUN_CONTRACT.md +
  CONTRACT_FREEZE.json (historical originals).

## 10. Process and verification record (executor; explicitly NOT the independent QC)

- C0 preflight re-measured (01_RAW\DESKTOP_CORRECTION_R1\PREFLIGHT_RERUN.json): HEAD,
  the correction-contract SHA/size, EXE, VFS, the starting manifest — all MATCH; 6
  untracked groups, 0 staged.
- All correction scripts set sys.dont_write_bytecode = True; no __pycache__ anywhere;
  no file outside the authorized paths written (mtime sweep of the 5 pre-existing
  untracked groups: no new writes).
- The four evidence artifacts state their generator + generator SHA256 (verified
  self-consistent at close).
- JSON validity re-verified for every hand-edited JSON (DESTINATION_CONSUMER_CENSUS.json)
  and every generated JSON.
- No runtime execution; no hooks; the original game inputs are read-only physical
  sources; no git operation of any kind; AUDIT_ENTRYPOINT.md untouched.
- Fresh counts measured at the correction close: 420 physical files (389
  pre-correction + 31 new; post-correction bijection: 378/388 manifest rows
  byte-identical, exactly the 10 corrected files differ, 0 missing, 0 ghosts); the
  starting manifest (391 lines = 1 header + 388 file rows + 1 blank + 1 NOTE row;
  389 data rows) is byte-unchanged and stale for the 10 corrected files + 31 new
  files until the persistence-phase regeneration.

## 11. QC-R3 disposition and persistence record (persistence phase; pe-master-auditor under PE-MASTER order)

- QC-R3 verdict: PASS_WITH_FINDINGS (report + machine results in 04_QC\QC_R3_DESKTOP_CORRECTION\).
- P2-1 (two stale file-count clauses: HANDOFF "418", AMEND_LOG §7 "(419)") — FIXED by disposition edits A5/A6 (this section records them; per-file SHA pairs: BEFORE-correction-close -> AFTER-disposition listed below).
- P2-2 (two residual "runtime-tag-driven" clauses: REPORT DOWNSTREAM_CONSUMER_IDENTIFIED parenthetical + HANDOFF result paragraph) — FIXED by disposition edits A1/A4 (the census-scoped wording replaces the unscoped phrases; the remaining census-scoped occurrences in REPORT/CONSUMER_TRACE/BLAST_RADIUS/DESTINATION_CONSUMER_CENSUS were adjudicated by PE-MASTER as already bounded and stand; the historical-labeled sections, the BEFORE copies, the frozen correction contract and the immutable QC reports retain their occurrences as preserved history — post-disposition sweep verified: zero unscoped current-state occurrences remain).
- P3-1 (dead counter tag_sequence_ok=0 in CURSOR_PROOF_CORRECTION_R1.json) — RECORDED, no package edit (notational; the sequence uniformity is independently verified in QC_R3_VFS_WALK_RESULT.json; fix the generator before any future regeneration).
- P3-2 (decorative "match" fields with expected=null) — RECORDED, no package edit (the bytes are physical and independently verified 185/185 by QC-R3; provenance-notation note for future generators).
- P3-3 (PE_MASTER_REVIEW supersession is persistence-phase duty) — DISCHARGED: the review was rewritten in this phase (BEFORE copy per Phase B; the superseded prior verdict is preserved there and its story is recorded in the new review's SUPERSESSION NOTICE).
- PE-MASTER cosmetic note (not a QC finding; recorded here): the BRANCH_SELECTION_TRACE.json chain-narrative string cites "0x70C9AF/0x70C9B1" for the tag==count invariant while the authoritative pin rows record the instruction starts at 0x70C9AE (CMP) / 0x70C9B0 (JNZ) — the pin rows are the authoritative record; the narrative string is superseded by one byte; no edit (regenerating the JSON would orphan its generator pair).
- Persistence sequence executed (this section): the disposition edits A1..A9 (REPORT.md A1-A3; HANDOFF.md A4/A5/A9; AMEND_LOG A6/A7; EVIDENCE_INDEX.md A8; post-edit sweep: zero residual occurrences of every superseded clause; the A-edit SHA pairs are in the table below); the Phase-B BEFORE copies (06_REPORT\PE_MASTER_REVIEW.md 25523 bytes SHA256 811E03E341D7A28F01AF69A47B1643D8E6C71C0F50D047E5B257419A119C248F; 06_REPORT\MANIFEST_SHA256.csv 50698 bytes SHA256 CD938AD7C05C41A62B5847057A92EBF12C0B1890964AEC0ADCDA0F87ECE1E4BF — the copy byte-verified == the starting manifest SHA; both recorded as BEFORE_COPIES_INDEX.json rows 11-12 with phase label PERSISTENCE_PRE_VERDICT); the PE_MASTER_REVIEW.md rewrite (its SHA256 after write: 5EF8B22729F4076D6036A0AB51698239B012C025C0D7AAC0FE1912AFCDD882EB; 20795 bytes; LF-only; verbatim per the PE-MASTER order; the prior review preserved in the BEFORE copy); the AUDIT_ENTRYPOINT.md row addition (one factual LATEST RUNS row at the top; same publication commit; no governance change); the FINAL manifest regeneration (file count 437 physical files; data rows 437 = 436 file rows + 1 NOTE row; 1 header line + 1 blank separator line; manifest size/SHA at the regeneration covering this record's pre-finalization bytes: 61150 bytes / SHA256 45F26A0AB1CB56214D4BD45D4155129C7B42250F17C4323C138B72A4159C0B8C — self-excluded per the L12 precedent; the NOTE-row note field now properly quoted so every data line parses as exactly 5 CSV fields; the committed manifest is the final regeneration covering this section's final bytes — like the commit SHA, its identity is not quotable inside a covered file and is measured fresh and reported in the PE-MASTER terminal delivery); the bijection verification (every manifest file row == disk size+SHA; disk census == manifest file rows + the manifest itself; 0 missing / 0 ghosts / 0 mismatches — re-verified over the committed manifest by an independent re-hash sweep); the staged-path census (the package + AUDIT_ENTRYPOINT.md ONLY; staged file count == 437 + 1; no Entropia.exe / 20002.vfs / *.bnt / *.ark / original *.vfs corpus / installers / credentials / secrets in the staged set — enumerated and verified); the commit (ONE commit; path-limited to the package + the entrypoint); the push (origin/master; normal push; no force); the live remote verification (git ls-remote --exit-code origin refs/heads/master; UTC timestamp; exit status; remote SHA == LOCAL_HEAD — the push/remote evidence is reported in the PE-MASTER terminal delivery per the commit-SHA exclusion class).
- The commit SHA is NOT recorded inside the package (a file cannot carry its own commit's SHA); it is reported in the PE-MASTER terminal delivery and is discoverable via `git log -1 -- docs/audits/PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002`.

### 11a. QC-disposition / persistence SHA pairs (BEFORE -> AFTER)

| FILE | BEFORE (correction executor close) | AFTER (QC disposition / persistence) |
|---|---|---|
| 06_REPORT\REPORT.md | 18055 bytes / 9B9C3A468EFD7FF5C524B9BA6FE2AAE2FF2F38CC51602C9D3BC5639016611547 (§5 AFTER value) | 18835 bytes / 77A3A5BD41EBC5DD5630CD1EB3A0B420421C3CD1DAA0B81EF152637E48E4A5FA (after A1/A2/A3) |
| 06_REPORT\HANDOFF.md | 19197 bytes / C9123409E269F5FE63CC7D5872A2DBABC250D3B3109369BD228E2A27D5FB7B90 (§5 AFTER value) | 19565 bytes / DB1594DC29A94D014B3C30493A839966B4813CE51C8267F52D20AFEF2FC9F32B (after A4/A5/A9; before the FINALIZED STATE append of this same phase) |
| 06_REPORT\AMEND_LOG_DESKTOP_CORRECTION_R1.md | 23490 bytes / 419E45C134C61F300990B6FB8779B69FAC30C8CC1730D58B6868E810FBABD497 (measured fresh; its §5 self-hash is excluded per the L12/C8 precedent) | 23615 bytes / D0E5AB877CF180C79FB15A3ED5B66D4158F832D35F943A8CBD790CCE12DED3C2 (after A6/A7; before this §11 append) |
| 06_REPORT\EVIDENCE_INDEX.md | 14565 bytes / AF2CF382ED27E8E17A0CFDEB63735E8E310F02C4B309F8E78E387FB28E44B705 (§5 AFTER value) | 14852 bytes / 1AFB6EEE8358B08AD78244C566105F650ECF9FE7C1870DF31835B276260B39AB (after A8) |
| 06_REPORT\PE_MASTER_REVIEW.md | 25523 bytes / 811E03E341D7A28F01AF69A47B1643D8E6C71C0F50D047E5B257419A119C248F (Phase-B BEFORE copy SHA) | 20795 bytes / 5EF8B22729F4076D6036A0AB51698239B012C025C0D7AAC0FE1912AFCDD882EB (the new review; C1) |

The AFTER values for AMEND_LOG and HANDOFF are the post-disposition measurements (before the §11 / FINALIZED STATE appends of this same persistence phase); the FINAL committed state of every file is carried by the persisted MANIFEST_SHA256.csv (bijection-verified) and by the publication commit itself.
