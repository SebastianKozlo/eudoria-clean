# HANDOFF — PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002

Executor: pe-reconstruction (STATIC-ONLY executor session).
Original dispatch: PE-MASTER direct, under human authorization
PE_935_20002_PAYLOAD30_CONSUMER_HUMAN_AUTH_R1_20261002.
This is the DESKTOP_CORRECTION_R1 amended handoff: the delivery notice of the focused
correction run PE_935_20002_PAYLOAD30_DESKTOP_CORRECTION_R1_20261002 (human decision
PE_935_20002_PAYLOAD30_DESKTOP_CORRECTION_AUTH_R1_20261002, after the independent
ChatGPT Desktop post-audit verdict REQUIRE_CORRECTIONS). The ORIGINAL delivery notice
below the correction notice is preserved as the historical delivery record.

## CORRECTION DELIVERY NOTICE (DESKTOP_CORRECTION_R1; compact)

- CORRECTION_RUN_ID = PE_935_20002_PAYLOAD30_DESKTOP_CORRECTION_R1_20261002
- RUN_STATUS = CONSUMER_UNREACHED (corrected; supersedes the delivery-time
  CONSUMER_REACHED_ROLE_STRONGLY_SUPPORTED, which rested on the non-selected
  fallback-path trace)
- HARD_STOP_REASON = CORRECTION_EXECUTION_COMPLETE (the executor's part of contract
  §10 steps 1-4 is complete: CORRECTION + BEFORE copies + document corrections +
  amendment log; fresh QC, QC disposition, final report finalization, manifest
  regeneration and persistence are separate PE-MASTER dispatches — NO_NESTED_TASKS)
- AUDIT_OUTPUT_ROOT = D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002\
- FINAL_REPORT_PATH = <root>\06_REPORT\REPORT.md (the DESKTOP_CORRECTION_R1 amended
  state; correction record: <root>\06_REPORT\AMEND_LOG_DESKTOP_CORRECTION_R1.md)
- PRIMARY_EVIDENCE_PATHS (the correction's primary evidence, new):
  1. <root>\01_RAW\DESKTOP_CORRECTION_R1\BRANCH_SELECTION_TRACE.json — the full
     pinned branch-selection chain: registration site (incl. the factory call + arg
     pushes), the factory FUN_00977a50, the descriptor-init dataflow
     (FUN_0070cbc0/FUN_0075f5c0/FUN_0070c980/FUN_0070c7b0), the lookup, the
     FUN_0075F660 TEST/JZ/virtual slot/call, the vtable dword @0xA9C684 = 0x009777F0,
     the selected reader's full instruction window (read/store/advance + error path),
     the RTTI walk (.?AUArkRTTraitsInt@@) — 96/96 pins, all 9 rel32 call targets
     computed
  2. <root>\01_RAW\DESKTOP_CORRECTION_R1\FALLBACK_PATH_RECORD.json — the old path
     (FUN_00412540 read @0x00412553 / FO 0x12553, store @0x0041255A / FO 0x1255A)
     recorded as BYTE-CORRECT EVIDENCE OF A NON-SELECTED FALLBACK PATH with its
     reachability condition (descriptor+0 == NULL) and the superseded 0x00125553
     transcription note — 25/25 pins
  3. <root>\01_RAW\DESKTOP_CORRECTION_R1\CURSOR_PROOF_CORRECTION_R1.json — the
     cursor increment table per tag, the +0x30 derivation, record-0 and record-1014
     walk states, the 1366-record census (exact-EOF re-derivation; full consumption
     1366/1366; zero records [1014, 1015]), the success-vs-error path distinction
     (3 negative simulations DETECTED), the width sources (type-1/-2/-4 reader
     advance pins) — 41 pins
  4. <root>\01_RAW\DESKTOP_CORRECTION_R1\DESTINATION_PROOF_CORRECTION_R1.json — the
     slot-21 chain pins (field index = tag+4, value_array = instance+0x40, LEA dest,
     the dest pass-through into the reader's arg2, the selected store 0x00977810,
     the 22-slot allocation arithmetic) — 23/23 pins
  5. <root>\01_RAW\DESKTOP_CORRECTION_R1\PREFLIGHT_RERUN.json — the C0 correction
     preflight re-measurements (HEAD, contract SHA, EXE, VFS, starting manifest —
     all MATCH)
  6. <root>\03_SCRIPTS\desktop_correction_r1\ — the correction's generators
     (pe_parse.py = the run's own PE32 parser; s1* context dumps; s2_branch_pins.py;
     s3_fallback_path.py; s4_cursor_walk.py; s5_destination.py;
     s6_before_copies.ps1; s7_post_correction_bijection.py = the post-correction
     manifest-bijection verification; each artifact states its generator + generator
     SHA256)
  7. <root>\00_CONTROL\DESKTOP_CORRECTION_R1\BEFORE\ — the 10 BEFORE copies
     (byte-for-byte; BEFORE_COPIES_INDEX.json with size + SHA256 per copy; the 10th
     copy, 02_ANALYSIS\VFS_TO_PARSER_TRACE.md, was added when the contradiction census
     found a stale live copy there)
  8. <root>\06_REPORT\AMEND_LOG_DESKTOP_CORRECTION_R1.md — the amendment/correction
     log (Desktop finding, superseded claims, BEFORE/AFTER artifact pairs, the
     contradiction census, the affected dependency set, remaining unknowns, the §8
     lesson, the QC1/QC2 superseded-conclusion record)
- HEAD unchanged: 9203b6d1ad5025f4158d5165863594132aaac49f (== BASE_SHA; re-verified
  at the correction preflight; ZERO commits / staging / push by the executor;
  AUDIT_ENTRYPOINT.md untouched; the historical QC dirs and the JOIN R1 package
  untouched)
- NO-COMMIT / NO-PUSH / NO-RUNTIME: CONFIRMED (Entropia.exe never launched; all
  correction evidence is static; no hooks; no original file modified)
- Corrected package counts (freshly measured 2026-10-02 at the correction close;
  physical files vs manifest rows vs text lines distinguished, no conflation):
  - CURRENT PHYSICAL FILE COUNT: 420 files on disk (whole package incl. 04_QC and
    00_CONTROL\DESKTOP_CORRECTION_R1\ with the BEFORE\ copies) = the 389
    pre-correction physical files + 31 new correction-phase files (14 control/BEFORE
    + 5 01_RAW correction artifacts + 11 scripts incl. the post-correction
    manifest-bijection verification + 1 amendment log). Post-correction bijection
    verification: of the starting manifest's 388 file rows, 378 byte-identical,
    exactly the 10 corrected files differ, 0 missing, 0 ghosts.
  - STARTING MANIFEST (byte-unchanged historical census): 391 raw text lines = 1
    header + 388 file rows + 1 blank separator + 1 NOTE row (389 data rows; the NOTE
    row is not a file row). The manifest is stale for the 10 corrected files and
    silent about the 31 new files; it is regenerated LAST by the persistence worker.
- Historical delivery counts (preserved as historical records, NOT current):
  the ORIGINAL delivery census was 364 files outside 04_QC (363 manifest-covered +
  the manifest itself + one NOTE row that is not a file row); the QC-era census was
  389 physical files (388 manifest rows + the manifest itself). Those numbers
  accurately described those earlier package states and are not corrected here; the CURRENT count at the correction executor close is the 420 above (the QC-R3 round then added its artifacts under 04_QC\QC_R3_DESKTOP_CORRECTION\; the FINAL package count is measured at the persistence-phase manifest regeneration — see the FINALIZED STATE section below).

## Result in one paragraph (CORRECTED)

The value at payload+0x30 of a 20002.vfs record is the tag-0x11 (tag ID 17) property
value of the record's TLV property block: every record carries six entries (tags 1,
0xC, 0xD, 0xE, 0x10, 0x11) under flags 0x80 / count 6, and the tag-0x11 value sits at
payload+0x30 in 1366/1366 records. Class 20002 is ArkParameterArmor
(RTTI-confirmed); its class object opens its own data file as itoa(20002)+".vfs" and
loads records on demand into ArkParameterArmor instances (0x58 bytes, 22-slot value
arrays). The generic property parser dispatches the value read through FUN_0075f660,
which — per the DESKTOP_CORRECTION_R1 branch-selection proof — selects the VIRTUAL
branch for tag ID 17 because the tag's descriptor holds a non-NULL reader object (the
static ArkRTTraitsInt singleton 0x00BA937C returned by the factory FUN_00977a50, never
NULL): the selected reader FUN_009777F0 reads the +0x30 field with a native 4-byte
little-endian load (VA 0x00977807; bytes 8B 04 10) and stores it — a pure copy, no
comparison/lookup — into the instance's value-array slot 21 (VA 0x00977810; bytes 89
02; dest = value_array + (tag+4)*4 = +0x54), exposed thereafter to the client's
generic property-read machinery (no statically-coded tag-0x11 reader was identified within the 202-site bounded census; within that census the reads take the tag as a runtime variable). The FALLBACK path
(FUN_00412540 @0x00412553/0x0041255A) is byte-correct but NON-SELECTED for tag ID 17
(it requires descriptor+0 == NULL). The gameplay semantics of the property remain
UNVERIFIED; no downstream consumer was identified (RUN_STATUS = CONSUMER_UNREACHED);
no world/model/placement edge is claimed or demonstrated.

## Process notes (correction; full disclosure)

1. Scope discipline: the correction was performed exactly per the correction
   contract (§1-§5, §7-§9; §10 steps 1-4); no new science question was opened; the
   historical QC reports (rounds 1/2), the historical JOIN R1 package, the frozen
   formalizer files, PE_MASTER_REVIEW.md (its supersession is written in the
   persistence phase), AUDIT_ENTRYPOINT.md and MANIFEST_SHA256.csv (regenerated LAST
   by the persistence worker) were NOT touched.
2. Every load-bearing instruction of the corrected chain was re-derived from the
   pinned EXE bytes with this correction's own PE32 parser (pe_parse.py — no
   offset==RVA assumption: the section table is read; .tls/.rsrc demonstrably differ
   from the .text/.rdata/.data identity). All 9 rel32 call targets in the chain were
   computed programmatically; the RTTI walk was performed from the pinned bytes.
3. The contradiction census (contract gate C5) was executed after the corrections:
   the whole package was swept for stale live copies of the superseded claims; every
   hit is either corrected or explicitly labeled historical/fallback/BEFORE-copy.
   The census (patterns, hits, dispositions) is recorded in
   06_REPORT\AMEND_LOG_DESKTOP_CORRECTION_R1.md.
4. Tooling hygiene: all correction scripts set sys.dont_write_bytecode = True (the
   prior __pycache__ incident class); no bytecode was created anywhere; no file
   outside the authorized package paths was written (verified by mtime sweep of the
   pre-existing untracked groups).

## SELF_CHECK (executor self-check; explicitly NOT the independent QC-R3/MASTER audit)

- C0: HEAD/contract/EXE/VFS/starting-manifest re-measured, all MATCH
  (01_RAW\DESKTOP_CORRECTION_R1\PREFLIGHT_RERUN.json). Gate PASS.
- C1 (branch proven): each of the 8 contract §1(a) items byte-pinned (96/96
  BRANCH_SELECTION_TRACE pins; the descriptor+0 value for tag ID 17 proven NON-NULL
  from the registration dataflow + factory return bytes; the selected slot/target
  identified statically from the pinned .rdata dword; control-flow reachability
  stated). Gate PASS.
- C2 (reader pins): the selected reader's READ/STORE byte-pinned with independently
  recomputed VA/RVA/FO (READ VA 0x00977807 / RVA 0x00577807 / FO 0x00577807 / 8B 04
  10; STORE VA 0x00977810 / 89 02) — the Desktop candidates CONFIRMED by measurement.
  Gate PASS.
- C3 (cursor proven): the selected-reader cursor at the tag-ID-17 iteration ==
  payload+0x30 (record 0 + ANCHOR_ZERO record 1014 + the 1366-record denominator
  re-derived from the pinned VFS by this correction's own walk; error paths
  distinguished + 3 negative simulations DETECTED). Gate PASS.
- C4 (destination proven): the selected store targets value_array + (tag+4)*4 = slot
  21 (+0x54), width 4 — the LEA chain 0x726A11/0x726A14 + the dest pass-through
  (0x75F670-0x75F679) + the reader's dest load @0x97780A + the store @0x977810,
  all byte-pinned (23/23). Gate PASS.
- C5 (dependencies corrected): every active-dependency artifact updated or explicitly
  dispositioned; the contradiction census recorded in the amendment log; the fallback
  pins preserved labeled; BEFORE copies verified. Gate PASS (see the census).
- Wording: §5 bounded consumer wording applied verbatim; "tag ID 17" convention
  applied; the one-caller observation scoped; RUN_STATUS = CONSUMER_UNREACHED;
  DOWNSTREAM_CONSUMER_IDENTIFIED = NO; DEST_FIELD_IDENTIFIED = YES;
  FINAL_SEMANTIC_STATUS = UNVERIFIED; WORLD_INSTANCE_TO_MODEL_EDGE = NOT_TESTED;
  PLACEMENT_XYZ_RECOVERED = NO. Gate PASS.
- Forbidden actions: zero git operations; zero runtime execution; zero historical
  file edits; zero writes outside the package; the 5 pre-existing untracked groups
  byte-identical. Gate PASS.

## Next steps (per the correction contract §10 — NOT for the executor to perform)

- FRESH TARGETED QC (EXECUTED: QC-R3 verdict PASS_WITH_FINDINGS; 04_QC\QC_R3_DESKTOP_CORRECTION\QC_R3_REPORT.md; the A/B/C discriminating branch detector per contract §6 PASS; P2-1/P2-2 fixed + P3s dispositioned per the PE-MASTER QC-disposition order — AMEND_LOG_DESKTOP_CORRECTION_R1.md section 11).
- QC disposition -> final report finalization -> final evidence index -> PE-MASTER
  review supersession (persistence phase) -> final handoff -> entrypoint pointer (if
  applicable) -> manifest regenerated LAST -> bijection verification -> staged-path
  verification -> commit -> push -> live remote verification -> HARD STOP
  (NEXT_EXPERIMENT_AUTHORIZED = NO; NEXT_ACTION = FOCUSED_CHATGPT_DESKTOP_POST_AUDIT).

---

# ORIGINAL DELIVERY NOTICE (historical; preserved as the delivery-time record of the original run; superseded where the correction notice above differs)

Executor: pe-reconstruction (STATIC-ONLY executor session).
Dispatch: PE-MASTER direct, under human authorization PE_935_20002_PAYLOAD30_CONSUMER_HUMAN_AUTH_R1_20261002.

## Delivery notice (compact)

- RUN_STATUS = CONSUMER_REACHED_ROLE_STRONGLY_SUPPORTED (SUPERSEDED by the correction above)
- HARD_STOP_REASON = Contract §19 terminal hard stop after completion of the single authorized science question; no further experiment authorized (NEXT_EXPERIMENT_AUTHORIZED = NO).
- AUDIT_OUTPUT_ROOT = D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002\
- FINAL_REPORT_PATH = <root>\06_REPORT\REPORT.md
- PRIMARY_EVIDENCE_PATHS (top):
  1. <root>\01_RAW\CLIENT_READ_BYTES.json — 45/45 byte-pins of the routing + client-read + store chain
  2. <root>\01_RAW\RECORD_FRAMING.jsonl + RECORD_FRAMING_SUMMARY.json — full-file framing census (1,366 records, exact EOF, NC-FRAMING)
  3. <root>\01_RAW\FIELD_BYTE_ANCHOR.json — anchored records with machine-checked bounds assertions
  4. <root>\01_RAW\TLV_WALK_CENSUS.json — client-semantics walk over all 1,366 records (tag 0x11 value at +0x30 in 1366/1366; tail 0 in 1366/1366)
  5. <root>\01_RAW\ROUTING_CENSUS_RAW.json — imm32 0x4E22 / mangling / string census
  6. <root>\01_RAW\GHIDRA_ROUTING\PASS15_GHIDRA_DUMP.json — the 202-site consumer census
  7. <root>\01_RAW\RELEVANT_XREFS.json — consolidated reference censuses
  8. <root>\02_ANALYSIS\VFS_TO_PARSER_TRACE.md — the byte-pinned routing chain (§8)
  9. <root>\02_ANALYSIS\FIELD_TO_DESTINATION_TRACE.md — the §9 read/store chain
  10. <root>\02_ANALYSIS\NEGATIVE_CONTROLS.md — NC-FRAMING / NC-ANCHOR-ADJ / NC-RECORD / NC-VALUE
- ACTUAL_HEAD_end = 9203b6d1ad5025f4158d5165863594132aaac49f (== BASE_SHA; unchanged)
- Git-status-delta: ONLY the new package dir `docs/audits/PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002/` added (untracked); the 5 pre-existing untracked groups byte-identical (see process note below); 0 staged entries; 0 commits.
- NO-COMMIT / NO-PUSH / NO-RUNTIME: CONFIRMED (no git commit/push/stage performed; the client Entropia.exe was never launched — all evidence is static; no runtime hooks).
- Package file count at delivery: 364 files outside 04_QC (363 covered by MANIFEST_SHA256.csv + the manifest itself, self-excluded per the L12 precedent; the manifest additionally carries one NOTE row that is not a file row; 04_QC\ was reserved for the fresh QC worker and is excluded from the executor manifest). (HISTORICAL record of the delivery-time state; the CURRENT count is in the correction notice above.)
- REPORT.md SHA256: recorded in MANIFEST_SHA256.csv (the manifest is the authoritative in-package hash census; it is KNOWN-STALE until the final regeneration after the QC round and the PE-MASTER verdict).

## Result in one paragraph (delivery-time; SUPERSEDED by the corrected paragraph above — preserved as the historical record)

The value at payload+0x30 of a 20002.vfs record is the tag-0x11 (17th) property value of the record's TLV property block: every record carries six entries (tags 1, 0xC, 0xD, 0xE, 0x10, 0x11) under flags 0x80 / count 6, and the tag-0x11 value sits at payload+0x30 in 1366/1366 records. Class 20002 is ArkParameterArmor (RTTI-confirmed); its class object opens its own data file as itoa(20002)+".vfs" and loads records on demand into ArkParameterArmor instances (0x58 bytes, 22-slot value arrays). The generic property parser reads the +0x30 field with a native 4-byte little-endian load (VA 0x00412553) and stores it — a pure copy, no comparison/lookup — into the instance's value-array slot 21 (VA 0x0041255A), exposed thereafter to the client's generic property-read machinery (no statically-coded tag-0x11 reader exists; reads are runtime-tag-driven). The gameplay semantics of the property remain UNVERIFIED; no world/model/placement edge is claimed or demonstrated.

## Process notes (full disclosure — original run)

1. EXECUTOR INCIDENT (found and repaired in-run): the first execution of the cross-validation script (03_SCRIPTS\s3_crossval_vfs_common.py) imported the prior tool without suppressing CPython bytecode, causing CPython to create `docs\audits\PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928\04_TOOLS\__pycache__\vfs_common.cpython-312.pyc` — a write outside OUTPUT_ROOT into a pre-existing untracked group. REPAIR: the artifact was deleted; the group was re-verified byte-identical to its pre-run state (228 files; latest write 2026-09-30, before this run); the script was patched with `sys.dont_write_bytecode = True` and re-run (cross-validation re-confirmed FULL_BOUNDARY_AGREEMENT 1366/1366) without recreating the artifact. No other pre-existing group was touched (all latest writes 2026-09-11..09-30).
2. Ghidra usage: headless analyzeHeadless against a project in the pre-approved temp dir (C:\Users\User\AppData\Local\Temp\opencode\pe935_20002_ghidra); the analyzed program was imported from the pinned physical Entropia.exe; every load-bearing claim is byte-pinned by re-reading the pinned EXE directly (01_RAW\CLIENT_READ_BYTES.json) — Ghidra output is analysis context, never the sole basis of a load-bearing claim. All java processes exited before this handoff (verified; no untracked writer remains). The temp Ghidra project persists in the temp dir (bounded tooling state; safe to delete).
3. Ghidra postScript execution quirks (documented for QC): pass 1 postScript initially failed on Jython-2 os.makedirs(exist_ok) and was fixed + re-run via -process on the already-analyzed program; an early crash on mem.getBytes was fixed with a jarray buffer. These were tooling fixes inside OUTPUT_ROOT, not science changes.
4. The 202-site consumer census (PASS15) scanned the instruction context before each FUN_0070c180 call for a static immediate tag 0x11; the 2 candidate hits were examined and shown to be false positives (the parse loop's own register tag; a state-variable byte with actual tag 0x2 for class 24017). The conclusion "no static tag-0x11 reader" is therefore evidence-based, not an absence of search.

## Next steps (per contract §19 — NOT for the executor to perform; original-run wording)

- Fresh internal-QC worker (04_QC\; §C requirements; share no code with the executor implementations).
- INDEPENDENT_CHATGPT_DESKTOP_POST_AUDIT_REQUIRED = YES (human-side).
- AUTO_FOLLOWUP_RE = NO; NEXT_EXPERIMENT_AUTHORIZED = NO; HARD_STOP = YES.

## FINALIZED STATE (persistence phase)

- QC-R3: PASS_WITH_FINDINGS; dispositions applied (AMEND_LOG section 11).
- PE-MASTER verdict: MASTER_ACCEPTED (advisory; ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT=NONE) for the correction cycle — persisted verbatim in 06_REPORT\PE_MASTER_REVIEW.md.
- FINAL PACKAGE CENSUS (measured at the manifest regeneration): 437 physical files = 437 manifest data rows (436 file rows + 1 NOTE row) + 1 header line + 1 blank separator line; the manifest regenerated LAST, self-excluded; bijection verified 436/436 file rows size+SHA, 0 missing/0 ghosts/0 mismatches; the manifest's own size/SHA at the regeneration covering this section's pre-finalization bytes: 61150 bytes / SHA256 45F26A0AB1CB56214D4BD45D4155129C7B42250F17C4323C138B72A4159C0B8C (the committed manifest is the final regeneration covering this section's final bytes — like the commit SHA, its identity is not quotable inside a covered file and is measured fresh and reported in the PE-MASTER terminal delivery; same self-reference exclusion class).
- AUDIT_ENTRYPOINT.md: factual row added for this package + correction (in the SAME publication commit; no governance promotion; no Desktop-PASS claim).
- GIT: ONE commit of the package + AUDIT_ENTRYPOINT.md only; push verified live (git ls-remote --exit-code origin refs/heads/master; remote master SHA == LOCAL_HEAD; the UTC timestamp, exit status and SHA equality are reported in the PE-MASTER terminal delivery per the commit-SHA exclusion class).
- HARD_STOP = YES; NEXT_EXPERIMENT_AUTHORIZED = NO; NEXT_ACTION = FOCUSED_CHATGPT_DESKTOP_POST_AUDIT of the pushed commit SHA.
