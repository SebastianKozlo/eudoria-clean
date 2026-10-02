# AMEND_LOG_R1 — PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002

- RUN_ID = PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002
- AMEND_ROUND = AMEND-R1 (bounded correction round; documentation/metadata ONLY)
- DISPATCHED_BY = PE-MASTER (direct), after internal QC round 1 (04_QC\QC_REPORT.md; QC_VERDICT = PASS_WITH_FINDINGS: 0×P0, 0×P1, 2×P2, 5×P3) and PE-MASTER's adjudication (PE-MASTER's own byte-level counterchecks).
- EXECUTOR = pe-reconstruction (the original executor role, performing the ordered corrections; NO_NESTED_TASKS).
- AMEND_EXECUTED_UTC = 2026-10-02T19:40:56Z
- GIT OPERATIONS = NONE (no commit, no push, no stage; the package dir remains untracked exactly as at delivery).
- CLIENT LAUNCH = NONE (static documentation/metadata edits only; Entropia.exe never launched).
- SCIENCE CHANGES = ZERO; RAW-MEASUREMENT VALUE CHANGES = ZERO (the only 01_RAW edits are the two generator-metadata strings and the census-key label rename + aggregate add of C5, all ordered; every measurement value in every artifact is untouched).

## Scope statement (per the AMEND-R1 dispatch)

"AMEND-R1 scope: documentation/metadata corrections ordered by PE-MASTER after QC round 1 + PE-MASTER adjudication; zero science changes; zero raw-measurement changes except the two generator-metadata fields and the census-key label rename + aggregate add of item 5" — where "item 5" of the dispatch = correction C5 in this log's enumeration. No analysis scripts were re-run; no historical package (incl. JOIN R1 PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928) was modified; 04_QC\* was not touched by this round (all QC references in this log are read-only citations); writes were confined to the package root.

Enumeration of this round (exactly the dispatched items, nothing else):

- C1 (QC P2-1): 02_ANALYSIS\BLAST_RADIUS.md item 6 narrowed (two PRIOR_CLAIMS_CONFIRMED bullets replaced; section heading kept).
- C2 (QC P2-1): 06_REPORT\EVIDENCE_INDEX.md §S8 row "Loader-chain VAs (JOIN R1 claim 5)" result cell changed; artifact pointer kept.
- C3 (QC P3-1): 01_RAW\GHIDRA_ROUTING\PASS15_GHIDRA_DUMP.json field "generator" corrected.
- C4 (QC P3-2): 01_RAW\RELEVANT_XREFS.json field "generator" corrected.
- C5 (QC P3-3): 01_RAW\RECORD_FRAMING_SUMMARY.json census key renamed + correct aggregate added.
- C6 (QC P3-4): 06_REPORT\HANDOFF.md package file count corrected (line 26).
- C7 (post-QC governance fill): 06_REPORT\REPORT.md INDEPENDENT_QC filled (line 70).
- C8: 06_REPORT\AMEND_LOG_R1.md created (this file).

## Correction records (mandatory discipline: file path, BEFORE size + SHA256, exact old text span, exact new text, reason (QC finding ID), AFTER size + SHA256)

### C1 — 02_ANALYSIS\BLAST_RADIUS.md — item 6 narrowed

- REASON (QC finding ID): P2-1 — the prior item-6 text stamped JOIN R1 PE_MASTER_REVIEW claim 5's FUNCTION-LEVEL attribution (FUN_0070E810) PRIOR_CLAIMS_CONFIRMED on mismatched evidence. Corrected record (per QC round 1 + PE-MASTER adjudication): the class-ID→"<classID>.vfs" open mechanism is CONFIRMED but lives in FUN_0070c680; FUN_0070E810 is the "textures"+".vfs" opener with NO itoa call (contradicted by three independent measurements: this run's DECOMP/DISASM_FUN_0070e810.txt, the QC byte probes, PE-MASTER's own countercheck); the FUN_0094BD30/FUN_00959090/FUN_0094D9B0 "0x58-B array" family is the EnvironmentZones.vfs loader, not the 20xxx parameter channel. Verdict: PRIOR_CLAIMS_NARROWED.
- BEFORE: 4678 bytes | SHA256 3190ECA35FB125728650FB80F7D0AD8188827DD9A92B6FE03502BE875DCE7E72
- OLD TEXT SPAN (lines 57–63; the section heading at line 56 was kept):
```
- FUN_0070e810 builds "<classID>.vfs"-style names and opens via FUN_00972df0; the
  ".vfs" string @0xA86820 and the open behavior are re-verified in-run (pins 0x70C40E,
  0x70C742; FUN_00972df0 disasm). PRIOR_CLAIMS_CONFIRMED (independently re-verified
  in this binary, byte-pinned).
- The C5 byte pin cited by the lead ("C7 44 24 1C 80 00 @0x70E841") is consistent with
  this run's FUN_0070e810 disasm (@0x70E841 MOV dword [ESP+0x1C],0x80 — the {1,0x80,8}
  open-params vector). PRIOR_CLAIMS_CONFIRMED.
```
- NEW TEXT (replacing the span above; now lines 57–79):
```
- The class-ID→"<classID>.vfs" open mechanism is CONFIRMED but lives in FUN_0070c680
  (byte-pinned in-run: 0x70C3FC MOV EAX,[ECX+8]; itoa FUN_0040e900; 0x70C40E
  PUSH ".vfs"; 0x70C742 CALL FUN_00972df0; reader stored at classObj+0x84 @0x70C71E).
- JOIN R1 PE_MASTER_REVIEW claim 5's FUNCTION-LEVEL attribution of that mechanism to
  FUN_0070E810 is CONTRADICTED by the physical bytes (three independent measurements:
  this run's DECOMP/DISASM_FUN_0070e810.txt, the QC byte probes, and PE-MASTER's own
  countercheck): FUN_0070E810 builds a "textures"+".vfs" filename (string "textures"
  @0xA86858; the PUSH imm32 0xA86858 is at 0x70E4AD (0x70E4AC holds 50 = PUSH EAX —
  the QC report's probe VA 0x70E4AC was one byte early; PE-MASTER correction); CALL
  FUN_0070e470 @0x70E866; open CALL FUN_00972df0 @0x70E8B6) and contains NO call to
  the itoa function FUN_0040e900 (PE-MASTER whole-.text census: exactly 5 call sites
  of FUN_0040e900 exist, NONE inside FUN_0070E810's window; QC census agrees).
- Additionally the FUN_0094BD30/FUN_00959090/FUN_0094D9B0 "0x58-B array" family cited
  by the same historical claim is the EnvironmentZones.vfs loader (84-byte cursor
  grammar matching EnvironmentZones.vfs's 84-byte payloads — REC0 size field = 84
  measured; string "EnvironmentZones" @0xA9808C, sole code ref @0x958DCE), NOT the
  20xxx parameter channel; the 0x58-byte ArkParameterArmor INSTANCES of this run are
  a different machinery (a size coincidence).
- VERDICT: PRIOR_CLAIMS_NARROWED (mechanism confirmed; JOIN R1 claim 5's function
  attribution corrected in-package; the second lead-correction alongside item 2). No
  historical file is rewritten; the supersession of the historical attribution is
  recorded here and in 06_REPORT\PE_MASTER_REVIEW.md (PE-MASTER verdict) — a future
  amendment of the JOIN R1 package itself requires separate human authorization.
```
- AFTER: 6061 bytes | SHA256 3971527CF395E802FCC4407E65505374A55B8B16085421CD7C20F21E685A53A9

### C2 — 06_REPORT\EVIDENCE_INDEX.md — §S8 row result cell narrowed

- REASON (QC finding ID): P2-1 (same finding; this §S8 row mirrored the BLAST_RADIUS item-6 mis-verification).
- BEFORE: 6429 bytes | SHA256 E7183B9EDE04F788094782BC856CA468E2522D20CC10675F38A858342340AB58
- OLD TEXT SPAN (line 77):
```
| Loader-chain VAs (JOIN R1 claim 5) | 02_ANALYSIS\BLAST_RADIUS.md | PRIOR_CLAIMS_CONFIRMED (re-verified in-run) |
```
- NEW TEXT (artifact pointer kept):
```
| Loader-chain VAs (JOIN R1 claim 5) | 02_ANALYSIS\BLAST_RADIUS.md | PRIOR_CLAIMS_NARROWED (mechanism CONFIRMED in FUN_0070c680; the historical FUN_0070E810 attribution CONTRADICTED by bytes — see 02_ANALYSIS\BLAST_RADIUS.md item 6 + 06_REPORT\AMEND_LOG_R1.md) |
```
- AFTER: 6579 bytes | SHA256 E59CBDD2867332BB038F1C39A428CB5FA32A9DA016EF5F3F289CBA8C750E545B

### C3 — 01_RAW\GHIDRA_ROUTING\PASS15_GHIDRA_DUMP.json — field "generator" corrected

- REASON (QC finding ID): P3-1 — the declared generator script (03_SCRIPTS/s3_ghidra_routing_pass15.py) does not exist in 03_SCRIPTS; the actual pass-15 script is 03_SCRIPTS\s5_consumer_census_pass15.py. Nothing else in the artifact changed; JSON syntax re-validated after the edit.
- BEFORE: 92827 bytes | SHA256 1764D73716ADB73E1990DD37667051E7D82B139F7D195B7FD76610771546EB9D
- OLD TEXT SPAN (line 4; the line's single leading space and trailing ", " were outside the replaced span and are unchanged):
```
"generator": "03_SCRIPTS/s3_ghidra_routing_pass15.py"
```
- NEW TEXT:
```
"generator": "03_SCRIPTS/s5_consumer_census_pass15.py"
```
- AFTER: 92828 bytes | SHA256 B90667D3CAF2DB25E51847C38962451D125C0CC39D70482590CFE9A911C1CFCD

### C4 — 01_RAW\RELEVANT_XREFS.json — field "generator" corrected

- REASON (QC finding ID): P3-2 — the declared generator script (03_SCRIPTS/write_relevant_xrefs.py) does not exist anywhere in the package; the artifact is a manual consolidation of the GHIDRA dump outputs (executor session). Nothing else changed; JSON syntax re-validated after the edit.
- BEFORE: 6127 bytes | SHA256 849DCEE7BFADA5D308FD948B363B294DE31AF5D89566B969BCF311B93405F387
- OLD TEXT SPAN (line 3):
```
"generator": "03_SCRIPTS/write_relevant_xrefs.py"
```
- NEW TEXT:
```
"generator": "manual consolidation of 01_RAW/GHIDRA_ROUTING/*_GHIDRA_DUMP.json outputs (executor session)"
```
- AFTER: 6184 bytes | SHA256 A0028A1933B30EA654DDDBF942138BB01B8FA468B7F2AB71A199FD196767DBF0

### C5 — 01_RAW\RECORD_FRAMING_SUMMARY.json — census-key label rename + correct aggregate added

- REASON (QC finding ID): P3-3 — the aggregate census key "distinct_u16_at_payload_08" was mislabeled: its array value holds the u16@payload+04 values (1..190, the record-id B component). Renamed to "distinct_u16_at_payload_04" (value unchanged) and the correct aggregate "distinct_u16_at_payload_08": {"0x80": 1366} added (independently re-derived by QC round 1 from the raw VFS bytes and by PE-MASTER's own walk: flags u16@+0x08 == 0x80 in 1366/1366 records). In-place metadata-label fix ONLY: s1_framing_census.py was NOT re-run (per the AMEND-R1 order); the per-row 01_RAW\RECORD_FRAMING.jsonl was always correct and was NOT touched. JSON syntax re-validated after both edits.
- BEFORE: 136502 bytes | SHA256 32044BC133A846BA607D00D58E4BF4E4A6FF861338E61EDBA581ADCE0524E976
- OLD TEXT SPAN #1 (line 51; the key of the array whose 190 values 1..190 span lines 52–241):
```
    "distinct_u16_at_payload_08": [
```
- NEW TEXT #1:
```
    "distinct_u16_at_payload_04": [
```
- OLD TEXT SPAN #2 (lines 241–243; array close + next census key):
```
      190
    ],
    "id_equals_payload_composite_check": {
```
- NEW TEXT #2 (the correct aggregate inserted between the array close and the next key):
```
      190
    ],
    "distinct_u16_at_payload_08": {
      "0x80": 1366
    },
    "id_equals_payload_composite_check": {
```
- AFTER: 136567 bytes | SHA256 8088120BA352D3BE632C0A042E51B28BC989A203CFC7FB2D7460708E2EFF52C3

### C6 — 06_REPORT\HANDOFF.md — package file count corrected (line 26)

- REASON (QC finding ID): P3-4 — the delivery count was off by one against the package's own manifest (the manifest carries 363 file rows + itself = 364 files outside 04_QC, plus one NOTE row that is not a file row).
- BEFORE: 8797 bytes | SHA256 3FEFEBDB4B8936265AB3EA9127385A4FFE0ABA7823ACDF4B9681D6AC3D0306E8
- OLD TEXT SPAN (line 26):
```
- Package file count: 363 files (362 covered by MANIFEST_SHA256.csv + the manifest itself, self-excluded per the L12 precedent; 04_QC\ left empty for the fresh QC worker).
```
- NEW TEXT:
```
- Package file count at delivery: 364 files outside 04_QC (363 covered by MANIFEST_SHA256.csv + the manifest itself, self-excluded per the L12 precedent; the manifest additionally carries one NOTE row that is not a file row; 04_QC\ was reserved for the fresh QC worker and is excluded from the executor manifest).
```
- AFTER: 8939 bytes | SHA256 1865DA3295A91CC55DA67AC2E342F8ACC482731B458498E94808B558D573164B

### C7 — 06_REPORT\REPORT.md — INDEPENDENT_QC filled (line 70)

- REASON: post-QC governance fill ordered after QC round 1 (QC_VERDICT = PASS_WITH_FINDINGS, 04_QC\QC_REPORT.md) + PE-MASTER adjudication. The reference to 04_QC\QC_R2_TARGETED_REPORT.md is intentionally forward-pointing: that report does not exist yet and is created by the separate fresh QC worker AFTER this amendment.
- BEFORE: 9944 bytes | SHA256 460AC8ABBE84C113F3C6AC159BAD3EDA4F0DDA0A00ECBE381EF24B2B183AA279
- OLD TEXT SPAN (line 70):
```
INDEPENDENT_QC = QC_PENDING (filled by the fresh internal-QC worker after this run; executor leaves QC_PENDING)
```
- NEW TEXT:
```
INDEPENDENT_QC = PASS_WITH_FINDINGS (QC round 1: 0xP0, 0xP1, 2xP2, 5xP3 — full report 04_QC\QC_REPORT.md; the P2-1 + P3-1..P3-4 corrections applied in AMEND-R1, the P2-2 incident verified repaired, P3-5 documented-not-fixed — see 06_REPORT\AMEND_LOG_R1.md; targeted QC round 2 verification: 04_QC\QC_R2_TARGETED_REPORT.md)
```
- AFTER: 10159 bytes | SHA256 B29BDB8E3E4CC140CD71C856B5B409A9D81252608EC7BD200EE708849CE2DF62

### C8 — 06_REPORT\AMEND_LOG_R1.md — CREATED (this file)

- CREATED by AMEND-R1 (new file; no BEFORE state). Self-hash self-excluded: recording this file's own digest inside itself would alter it (same principle as the manifest self-exclusion, L12 precedent). Its size/SHA256 at close are reported in the round's delivery notice, not herein.

## Disposition records (ordered by the AMEND-R1 dispatch)

### P3-5 — s5_tlv_walk_census.py tautological counter (tag11_value_matches_plus30_count)

- DISPOSITION = DOCUMENTED_NOT_FIXED — the field is non-informative (it compares a value with itself at the offset just verified); it is NOT load-bearing (the real predicate field_30_is_tag11_value_count is correct and was triple-verified: executor walk, QC1 independent walk, PE-MASTER own walk). The artifact (01_RAW\TLV_WALK_CENSUS.json) and script (03_SCRIPTS\s5_tlv_walk_census.py) are left byte-identical to avoid post-hoc raw-evidence modification; any future regeneration must remove the tautological counter or make it a genuine re-read comparison.

### P2-2 — __pycache__ incident (executor process violation, self-repaired in-run; HANDOFF.md process note 1)

- DISPOSITION = VERIFIED_REPAIRED_DISCLOSED — no further action; repair verified by QC round 1 (0 residue, 228 files, 10/10 spot hashes) AND independently by PE-MASTER (0 residue, 228 files, 3/3 own spot hashes vs the JOIN R1 manifest). The violation stays on record.

## Scope-boundary notes (transparency for QC round 2 / PE-MASTER)

- BLAST_RADIUS.md "Retractions/supersessions issued by this run" section (now lines 81–84) was NOT edited: the AMEND-R1 order limited BLAST_RADIUS changes to item 6's bullets (the order's item 9 explicitly excludes all other 02_ANALYSIS content). Its "ONE lead-correction (item 2 above)" wording predates this amendment; the amended item 6 now additionally records the JOIN R1 claim-5 function-attribution narrowing as the second lead-correction. No retraction/supersession edge against the JOIN R1 package itself is issued by this round; per the amended item-6 text, any amendment of the JOIN R1 package requires separate human authorization.
- 04_QC\QC_R2_TARGETED_REPORT.md, referenced by the amended REPORT.md INDEPENDENT_QC line, does not exist at AMEND-R1 close; the separate fresh QC worker creates it AFTER this amendment (intentional forward-pointing reference).
- 06_REPORT\PE_MASTER_REVIEW.md, referenced by the amended BLAST_RADIUS item 6, is likewise forward-pointing: PE-MASTER's verdict record for this package, created by PE-MASTER (not present at AMEND-R1 close; 06_REPORT contains exactly EVIDENCE_INDEX.md, HANDOFF.md, MANIFEST_SHA256.csv, REPORT.md + this log at close).
- 06_REPORT\MANIFEST_SHA256.csv was NOT regenerated (no order to do so): it remains the delivery-time census and is therefore now stale for exactly the seven amended files C1..C7 and silent about the new file C8 — consistent with its own KNOWN-STALE note (final regeneration after QC + PE-MASTER verdict).
- 00_Control\*, 03_SCRIPTS\*, 04_QC\* and every other 01_RAW / 02_ANALYSIS / 06_REPORT file are byte-identical to delivery (verified against MANIFEST_SHA256.csv below).

## SELF_CHECK (executor self-check; explicitly NOT the independent QC-R2 / MASTER audit)

- SC1 (changed-file census, machine-checked vs MANIFEST_SHA256.csv): of the 363 manifest file rows, exactly 7 mismatch — precisely the C1..C7 files — and 356 rows hash identical; 0 missing; 1 NOTE row (not a file row; skipped). No other package file changed.
- SC2 (JSON validity): all three edited JSON artifacts (PASS15_GHIDRA_DUMP.json, RELEVANT_XREFS.json, RECORD_FRAMING_SUMMARY.json) re-parsed successfully after the edits (ConvertFrom-Json PASS).
- SC3 (encoding): all edited files were and remain UTF-8 without BOM; the non-ASCII characters used in the ordered new texts (→ U+2192, — U+2014) were verified to be encodable exactly as in the pre-existing file content (pre-existing em-dashes are UTF-8 sequences; no cp1252 bytes present before or after).
- SC4 (forbidden actions): zero git operations (no commit/push/stage/init); zero analysis-script executions; zero client launches; 04_QC\* never written (read-only); no file outside the package root touched; no historical package touched.
- SC5 (no new measurements): every number inside the corrected texts is a citation of QC round 1's report or PE-MASTER's adjudication text (e.g. the {"0x80": 1366} aggregate was derived by QC and PE-MASTER, not re-derived here; s1_framing_census.py was not re-run).
- SC6 (delta census at AMEND-R1 close): 365 files outside 04_QC = the 364 delivery files (unchanged content except C1..C7) + this new log; 14 files inside 04_QC (untouched by this round).
