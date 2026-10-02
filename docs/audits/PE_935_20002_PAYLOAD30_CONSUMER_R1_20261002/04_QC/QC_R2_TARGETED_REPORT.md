# QC_R2_TARGETED_REPORT — PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002 (targeted QC round 2: AMEND-R1 verification)

- RUN_ID = PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002
- QC ROUND = 2 (targeted verification of the AMEND-R1 correction round)
- ASSIGNMENT_MODE = INTERNAL_QC (targeted; PE-MASTER direct dispatch; NO_NESTED_TASKS)
- QC worker = pe-master-auditor, FRESH context (not the formalizer; not the executor; not the round-1 QC worker)
- SCOPE = verification of the AMEND-R1 corrections ONLY (claimed changes C1..C8). NO new science.
  NO edits outside 04_QC\. NO git mutations (read-only git only). NO client launch (STATIC_ONLY;
  re-confirmed at close: 0 Entropia / 0 ghidra-analyzeHeadless processes).
- INDEPENDENCE: all QC-R2 tools (`04_QC\qc_tools\q2r1…q2r4`) are this worker's own implementations.
  They share NO code with the executor's `03_SCRIPTS`, with round-1's `qc_tools`, or with JOIN R1's
  `vfs_common.py`. Every load-bearing number below was recomputed from the pinned physical bytes.

## QC_R2_VERDICT = PASS_WITH_FINDINGS

0×P0, 0×P1, 0×P2, 5×P3. Every AMEND-R1 correction C1..C7 is verified applied exactly as ordered
(diff census: exactly 7 mismatches = C1..C7; 356 matches; 0 missing; BEFORE provenance 7/7 against
the delivery manifest; AFTER identity 7/7 against the dispatch-declared hashes; exact-span check
8/8: every OLD span gone, every NEW span verbatim on disk) and factually correct in substance
(extended byte-fact checks 18/18 PASS; VFS census re-derived: u16@payload+0x08 == {0x80: 1366} in
1366/1366 by this worker's own walk). The round-1 QC round-1 findings' substance is confirmed and
NOT contradicted by the corrected wording (duty 7). The five findings are precision/residual items
for the final regeneration; none affects any run verdict, claim status or measurement value.
The one materially important one: **the C8 identity claim (AMEND_LOG_R1.md's SHA256) fails
verification as stated** — the physical file is intact and complete; a one-character transcription
error exists in the delivery-notice/dispatch chain (see P3-R2-1).

---

## 1. Inputs re-verified at session start AND at close (fail-closed identity; dispatch duty 1)

| INPUT | MEASURED (this session, own implementation) | PINNED | RESULT |
|---|---|---|---|
| RUN_CONTRACT.md | 27,270 B / SHA256 `24B3A5599FA16FE1E465BB82462344B35362CA7E1185F712EBC7730065D28657` | same (dispatch + CONTRACT_FREEZE per round-1) | MATCH |
| Entropia.exe (`D:\Eudoria_Reconstruction\pcg_install\Entropia.exe`) | 8,015,872 B / SHA256 `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` | same | MATCH |
| 20002.vfs (`D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\20002.vfs`) | 174,864 B / SHA256 `C3899C3E88D72CE12CEF9B8A4F5E73B26632BB1A3207C950FF2BC40FD9C94AC4` | same | MATCH |
| repo HEAD (eudoria-clean) | `9203b6d1ad5025f4158d5165863594132aaac49f` == origin/master == BASE_SHA | same | MATCH |

Git compliance at close (re-checked after all QC-R2 work): HEAD unchanged; `git status --porcelain`
= exactly the 6 untracked groups (this package + the 5 pre-existing, byte-identical groups);
0 staged; 0 commits. No Entropia.exe or ghidra/analyzeHeadless process alive. QC-R2 wrote ONLY
inside `04_QC\` (9 new files; list in §6).

## 2. Counterchecks executed (own tools; results in 04_QC\)

| # | COUNTERCHECK | TOOL | RESULT |
|---|---|---|---|
| QC-R2-1 | DIFF CENSUS: hashed EVERY file in the package outside 04_QC (365 files) and compared against `06_REPORT\MANIFEST_SHA256.csv` (parsed strictly: header + 363 file rows + 1 NOTE row; 0 malformed) | q2r1_diff_census.py | exactly **7 mismatches = C1..C7** (the AFTER hashes), **356 matches**, **0 missing**; disk-not-in-manifest = exactly {MANIFEST_SHA256.csv (self-excluded by design), AMEND_LOG_R1.md (new C8)}; 365 files outside 04_QC = 363 manifest-covered + 1 manifest + 1 new log (SC6 algebra CONFIRMED). BEFORE provenance: for each C1..C7 the AMEND_LOG BEFORE size+SHA == the delivery-manifest row (7/7; that manifest was itself verified against disk by round-1 QC). AFTER identity: disk size+SHA == the dispatch-declared AFTER values (7/7). 10/10 named load-bearing unchanged files match. C8 disk identity: 16,978 B matches; SHA MISMATCH → finding P3-R2-1 |
| QC-R2-2 | BYTE-FACT SPOT-CHECKS from the pinned EXE (own PE32 parser: image base 0x400000, machine 0x14c; own VA→RVA→file-offset; own re-reads) + extended pins + whole-.text censuses | q2r2_bytefacts.py | 18/18 PASS — see §3 |
| QC-R2-3 | Independent re-walk of 20002.vfs from raw bytes (own grammar derivation: global header "ArkVFS02" + u32 base=0x80; 16-byte record header {u32 id, u32 size, u16 ver, u32 crc, u16 pad}; stride = base×ceil((16+size)/base); EXACT-EOF) | q2r3_vfs_census.py | 1366 records; final_pos == 174,864 == file size (EXACT EOF); all size=56/ver=1/crc=0; **u16@payload+0x08 == {"0x80": 1366} (1366/1366)** — the dispatch duty-5 census, re-derived by this worker's own walk; distinct u16@payload+0x04 == exactly 1..190 (190 values) == the renamed C5 key's "original value set"; u32@payload+0 == 20002 in 1366/1366; u16@+0x2E == 0x11 in 1366/1366; id == composite in 1366/1366; anchors rec0 = 11963 (BB 2E 00 00) @fo 80, rec1014 = 0 @fo 129872, zeros exactly {1014, 1015}; +0x30 field census 142 distinct, min 0, max 16409 (all round-1 figures reproduced). The AMENDED RECORD_FRAMING_SUMMARY.json parses and BOTH its corrected census fields equal this worker's independent aggregates |
| QC-R2-4 | EXACT-SPAN verification of every AMEND_LOG correction record (OLD spans gone from disk, NEW spans verbatim on disk, both recorded in AMEND_LOG) | q2r4_span_check.py | 8/8 PASS (C1 item-6 block; C2 §S8 row; C3 + C4 generator fields; C5 key rename + C5 aggregate insert; C6 line 26; C7 INDEPENDENT_QC cell) |
| — | Script existence (duty 4c): `03_SCRIPTS\s5_consumer_census_pass15.py` EXISTS; the two previously-declared scripts (`s3_ghidra_routing_pass15.py`, `write_relevant_xrefs.py`) do NOT exist anywhere in the package (recursive sweep: 0 + 0) | shell | PASS |
| — | 04_QC round-1 file census by mtime (AMEND-R1 claim SC6/SC4: "04_QC untouched by this round") | shell | all 14 round-1 files written 12:20:55–12:32:27 local (== 19:20–19:32 UTC), all BEFORE the AMEND_LOG close (12:41:32 local == 19:41:32 UTC ≈ AMEND_EXECUTED_UTC 19:40:56Z + 36 s) — CONFIRMED untouched by AMEND-R1 |
| — | `PRIOR_CLAIMS_CONFIRMED` sweep over all *.md in the package | grep | remaining occurrences ONLY in: AMEND_LOG_R1.md (the OLD-TEXT-SPAN historical citations — required), round-1's immutable 04_QC files (historical), RUN_CONTRACT.md §15 (taxonomy definition). **Zero live occurrences** in BLAST_RADIUS.md / EVIDENCE_INDEX.md / REPORT.md / HANDOFF.md / 02_ANALYSIS |

## 3. Byte-fact spot-checks (dispatch duty 5 — PE-MASTER-adjudicated facts + extended verification)

All measured with this worker's own PE32 parser + own re-read of the pinned EXE (identity re-verified in the same run):

- **F1: VA 0x70E4AD == `68 58 68 A8 00`** (PUSH 0xA86858) — PASS. imm32 LE decode == 0xA86858.
- **F2: VA 0x70E4AC == `50`** (PUSH EAX) — PASS. Confirms PE-MASTER's adjudication that round-1's
  probe VA 0x70E4AC was one byte early (the C1 text records this correction accurately).
- **F3: "textures\0" @0xA86858** (.rdata) — PASS (16 bytes read; ASCII + NUL terminator).
- **F4: "EnvironmentZones\0" @0xA9808C** (.rdata) — PASS.
- Extended pins cited by the corrected C1 text — all PASS:
  F6 `68 20 68 A8 00` (PUSH ".vfs" 0xA86820) @0x70C40E; F7 `8B 41 08` (MOV EAX,[ECX+8]) @0x70C3FC;
  F8 `89 86 84 00 00 00` (MOV [ESI+0x84],EAX — reader store; base ESI per the package's own pin,
  disp32 == +0x84 as claimed) @0x70C71E; F9 E8 rel32 @0x70E866 → 0x70E470 (CALL FUN_0070e470);
  F10 E8 @0x70E8B6 → 0x972DF0 (open call); F11 E8 @0x70C742 → 0x972DF0;
  F17 `C7 44 24 18 01 00 00 00` @0x70E839 and F18 `C7 44 24 1C 80 00 00 00` @0x70E841
  (the {1, 0x80, 8} open-params stores; 0x70E841 is the full 8-byte MOV — JOIN R1's 6-byte citation
  was a truncated transcription, as round-1 QC4b already recorded).
- **F12: whole-.text census of E8 calls to FUN_0040e900 (itoa): exactly 5 sites**
  (0x4c50a8, 0x5b374e, 0x70c405, 0x75f3dd, 0x8362e7 — incl. 0x70c405 inside FUN_0070c680, the
  real class-ID builder), **NONE inside [0x70E810, 0x70E928]** — matches the C1 text's
  "exactly 5 call sites … NONE inside FUN_0070E810's window" (verified: DISASM_FUN_0070e810.txt
  ends `RET 0x4` @0x70E928, so the window IS the function body).
- **F15: PUSH `68 58 68 A8 00` occurs at exactly 1 site in the whole .text: 0x70E4AD** —
  the C1 text's "the PUSH imm32 0xA86858 is at 0x70E4AD" is byte-exact and sole.
- **F5a/F5b/F5c/F5d: the EnvironmentZones code ref**: bytes @0x958DCE == `8C 80 A9 00`
  (the imm32 operand), the actual PUSH instruction is at **0x958DCD** (`68 8C 80 A9 00`);
  whole-.text census: PUSH pattern exactly 1 site (0x958DCD), raw imm32 pattern exactly 1 site
  (0x958DCE) — the "sole code ref" substance of the C1 text is TRUE, but its stated VA
  (0x958DCE) is the operand address, one byte after the instruction start → finding P3-R2-2.
- **VFS census (duty 5)**: re-derived by this worker's own walk (QC-R2-3):
  **u16@payload+0x08 == 0x80 in 1366/1366 records** (histogram exactly {"0x80": 1366}), with
  exact-EOF walk (174,864/174,864), 1366 records, all record headers sane, anchors reproduced.

## 4. Content verification of the claimed changes (dispatch duty 4)

| ITEM | REQUIRED VERIFICATION | RESULT |
|---|---|---|
| C1 | BLAST_RADIUS item 6 = PRIOR_CLAIMS_NARROWED, mechanism in FUN_0070c680, FUN_0070E810 contradiction, no historical-attribution-confirmed claim | **PASS** (full 89-line read + mechanical span check; item 6 states exactly that; the two PRIOR_CLAIMS_CONFIRMED bullets are gone; the old verdict stamp survives nowhere live). Two precision defects recorded: P3-R2-2 (0x958DCE VA), P3-R2-3 ("textures" attribution to the DECOMP/DISASM pair) |
| C2 | EVIDENCE_INDEX §S8 row matches | **PASS** (line 77 = the AMEND_LOG NEW TEXT verbatim; span check PASS) |
| C3 | PASS15 generator field == "03_SCRIPTS/s5_consumer_census_pass15.py" AND the script exists AND the two previously-declared scripts do not | **PASS** (field verified; Test-Path True / False / False; recursive sweep 0+0; the script read in full — it IS the pass-15 census Jython generator writing PASS15_GHIDRA_DUMP.json; its result-dict still self-declares the OLD name → P3-R2-5) |
| C4 | RELEVANT_XREFS generator no longer names a non-existent script | **PASS** (now "manual consolidation of 01_RAW/GHIDRA_ROUTING/*_GHIDRA_DUMP.json outputs (executor session)" — true provenance per round-1 P3-2; span check PASS) |
| C5 | RECORD_FRAMING_SUMMARY has BOTH distinct_u16_at_payload_04 (renamed, original value set) AND distinct_u16_at_payload_08 == {"0x80": 1366} | **PASS** (full JSON parse; the array == list 1..190 (190 values) — equal to this worker's own independent u16@+0x04 census; the aggregate == {"0x80": 1366} — equal to this worker's own walk-derived histogram; JSON re-validates after both edits) |
| C6 | HANDOFF states 364 files outside 04_QC / 363 manifest-covered | **PASS** (line 26 exact; measured truth: 363 manifest rows + manifest + new log; a residual sibling of the same defect remains at line 50 → P3-R2-4) |
| C7 | REPORT INDEPENDENT_QC cell == PASS_WITH_FINDINGS with the QC_REPORT/AMEND_LOG/QC_R2 pointers | **PASS** (line 70 exact; the forward reference to this file is now complete — you are reading it) |
| C8 | AMEND_LOG_R1.md records all 8 items with BEFORE/AFTER hashes + the P3-5 DOCUMENTED_NOT_FIXED and P2-2 VERIFIED_REPAIRED_DISCLOSED dispositions | **PASS on content** (full 199-line read: C1..C8 records each with BEFORE size+SHA + old/new spans + reason; both disposition records present and accurately worded; scope-boundary notes accurate — the Retractions section non-edit, the manifest's deliberate staleness for exactly C1..C7 + C8, the forward-pointing PE_MASTER_REVIEW.md). **FAIL on the claimed identity** → P3-R2-1 |

## 5. Consistency with round-1 QC's P2-1 (dispatch duty 7)

The new BLAST_RADIUS item 6 IMPLEMENTS round-1's prescribed correction without fighting it:
mechanism CONFIRMED in FUN_0070c680 (byte-pinned) ✓; JOIN R1 claim 5's function-level attribution
CONTRADICTED ✓; FUN_0070E810 = "textures"+".vfs" opener ✓; verdict PRIOR_CLAIMS_NARROWED ✓;
"the second lead-correction alongside item 2" ✓ (item 2 = the FUN_00959090/EnvironmentZones
lead correction, matching round-1 §5's description of what the run had already corrected).
The added EnvironmentZones "0x58-B array" family paragraph is consistent with round-1 §4.4/§5
(84-byte cursor grammar, size-coincidence with the 0x58-B ArkParameterArmor instances) — all of
which this worker re-verified at byte level (F4/F5a-d; sole code ref confirmed). The round-1
P2-1 SUBSTANCE therefore stands confirmed, and the new wording does not contradict it. Two
inherited/imprecise details are recorded as P3-R2-2/P3-R2-3 (they refine, not reverse, the
finding). Note for the record: round-1's P2-1 revalidation predicate itself contains two
false-as-worded clauses — clause 1 (0x70E4AC, already adjudicated by PE-MASTER) and clause 4
(DECOMP_FUN_0070e810.txt does NOT contain "textures"; the literal lives in
PASS4_DECOMP_FUN_0070e470.txt line 45 + the .rdata string + the byte pins) — so round-1's
"(All four verified true by QC)" was inaccurate on clause 4. The round-1 report is an immutable
historical record; this is recorded here for the audit trail, not as an action item against it.

---

## 6. Findings (all P3; none affects a run verdict, claim status or measurement value)

### **P3-R2-1 — C8 identity claim fails verification: AMEND_LOG_R1.md's declared SHA256 (as transcribed in the AMEND-R1 delivery chain / the QC-R2 dispatch) does not match the physical file**

- SOURCE: the QC-R2 dispatch's C8 claim: 06_REPORT\AMEND_LOG_R1.md = 16,978 B /
  `02A60AE9A562F1C2380023262EBAE9A3B66ACBA7AC0DA7A40934504CBF436943`. AMEND_LOG C8 itself records
  no hash (self-exclusion by design: "Its size/SHA256 at close are reported in the round's
  delivery notice, not herein") — so the erroneous identity lives only in the out-of-package
  delivery-notice → dispatch transcription chain.
- PHYSICAL COUNTER-EVIDENCE (two independent implementations): disk file = 16,978 B / SHA256
  `02A60AE9A562F1C2310023262EBAE9A3B66ACBA7AC0DA7A40934504CBF436943` (Python hashlib AND
  PowerShell Get-FileHash agree; difference from the claim: exactly one character, 0-based
  position 17: disk `1` vs claim `8`). Size matches. LastWriteTime 2026-10-02 12:41:32 local
  (UTC-7) = 19:41:32Z ≈ AMEND_EXECUTED_UTC 19:40:56Z + 36 s → the file has NOT been modified
  since AMEND-R1 close.
- SOURCE_FILE_UNCHANGED vs MANIFEST_IDENTITY_CORRECT (L10): the physical file is intact and its
  CONTENT is fully verified by this worker (all 8 correction records, dispositions, scope notes
  present and accurate). The IDENTITY CLAIM is wrong by one hex character.
- FAILURE MECHANISM: a single-character transcription error somewhere in the chain
  executor delivery notice → PE-MASTER dispatch (the two possible origins cannot be
  distinguished from inside this package; PE-MASTER can check the notice it received).
- AFFECTED: the AMEND-R1 delivery record only. No in-package artifact carries the wrong hash;
  the delivery manifest does not cover the new file; no verdict, claim or measurement is affected.
- CORRECTION (for PE-MASTER's records + the final regeneration): record
  16,978 B / `02A60AE9A562F1C2310023262EBAE9A3B66ACBA7AC0DA7A40934504CBF436943` as the C8
  close identity; any publication citing C8 must use the measured hash.
- REVALIDATION PREDICATE: Get-FileHash(06_REPORT\AMEND_LOG_R1.md) == the value above (exact,
  64-hex, case-insensitive) AND LastWriteTime ≤ AMEND close + no later write.

### **P3-R2-2 — C1 text: "sole code ref @0x958DCE" is the imm32 operand address; the PUSH instruction starts at 0x958DCD (same one-byte-early class PE-MASTER adjudicated for 0x70E4AC)**

- SOURCE: 02_ANALYSIS\BLAST_RADIUS.md item 6 (new text, line 72): "string "EnvironmentZones"
  @0xA9808C, sole code ref @0x958DCE" (inherited from round-1 QC4's report text).
- PHYSICAL COUNTER-EVIDENCE: bytes @0x958DCD == `68 8C 80 A9 00` (PUSH 0xA9808C); bytes @0x958DCE
  == `8C 80 A9 00` (the imm32 operand). Whole-.text census (own scan): PUSH pattern occurs at
  exactly 1 site (0x958DCD); raw imm32 pattern at exactly 1 site (0x958DCE).
- SUBSTANCE UNAFFECTED: the "sole code ref" claim is TRUE (exactly one code reference in the
  whole .text; instruction at 0x958DCD inside FUN_00958d90, matching round-1's census).
- FAILURE MECHANISM: the VA was measured/reported as the operand (imm32) occurrence address
  rather than the instruction start — the identical defect class that the same C1 text
  corrects for the round-1 probe VA (0x70E4AC → 0x70E4AD, PE-MASTER correction).
- AFFECTED: BLAST_RADIUS item 6 wording only (and, historically, round-1's QC4 row — immutable).
- CORRECTION (final regeneration): state the code ref at 0x958DCD (instruction VA), or
  explicitly label 0x958DCE as the operand address of the PUSH at 0x958DCD.
- REVALIDATION PREDICATE: bytes @0x958DCD == `68 8C 80 A9 00` AND whole-.text census of that
  pattern == exactly 1 site.

### **P3-R2-3 — C1 text over-attributes the "textures" literal to DECOMP/DISASM_FUN_0070e810.txt; the literal lives in PASS4_DECOMP_FUN_0070e470.txt + .rdata + the byte pins**

- SOURCE: BLAST_RADIUS item 6 (new text, lines 61–63): "three independent measurements: this
  run's DECOMP/DISASM_FUN_0070e810.txt, the QC byte probes, and PE-MASTER's own countercheck:
  FUN_0070E810 builds a "textures"+".vfs" filename".
- PHYSICAL EVIDENCE (own reads): DECOMP_FUN_0070e810.txt contains NO "textures" literal (it shows
  `FUN_0070e470(local_24, DAT_00b9d8d0 ^ …)`, `&DAT_00a86820` (".vfs"), and the {1,0x80,8} open
  params); DISASM_FUN_0070e810.txt contains no 0xA86858 reference either (the PUSH is inside
  FUN_0070e470, outside FUN_0070E810's window). The literal is in
  PASS4_DECOMP_FUN_0070e470.txt line 45 (`basic_string(param_1,"textures",paVar1)`) + the .rdata
  string @0xA86858 (F3) + the PUSH pin @0x70E4AD (F1/F15, sole). The DECOMP/DISASM pair DOES
  independently establish the rest of the contradiction (FUN_0070e470 call, ".vfs" concat,
  {1,0x80,8}, and NO itoa — F9/F10/F12/F17/F18 all PASS).
- SUBSTANCE UNAFFECTED: every constituent byte fact of "FUN_0070E810 builds a textures+.vfs
  filename" is verified TRUE by this worker; only the file-level attribution of the "textures"
  half is imprecise. Round-1's P2-1 SOURCE text made the same paraphrase (consistency preserved —
  duty 7); its revalidation predicate clause 4 ("DECOMP_FUN_0070e810.txt contains 'textures'",
  "(All four verified true by QC)") is FALSE as worded — recorded in §5 for the historical record.
- CORRECTION (final regeneration): attribute the "textures" literal to the string pin + the
  FUN_0070e470 dump; keep DECOMP/DISASM_FUN_0070e810.txt as evidence of the call/.vfs/{1,0x80,8}/
  no-itoa half.
- REVALIDATION PREDICATE: "textures" ∈ PASS4_DECOMP_FUN_0070e470.txt ∧ "textures" ∉
  DECOMP_FUN_0070e810.txt ∧ PUSH 0xA86858 sole @0x70E4AD ∧ no E8→FUN_0040e900 in
  [0x70E810, 0x70E928].

### **P3-R2-4 — HANDOFF.md line 50 (SELF_CHECK S8) still states "362 rows" — residual off-by-one of the P3-4 class, outside the dispatched line-26 scope; the file is now internally inconsistent**

- SOURCE: 06_REPORT\HANDOFF.md line 50: "manifest census documented (362 rows + self-exclusion)"
  vs the corrected line 26: "363 covered by MANIFEST_SHA256.csv + the manifest itself".
- MEASURED TRUTH (own parse): 363 file rows + 1 NOTE row; 364 delivery files outside 04_QC;
  365 at AMEND close (incl. the new log).
- FAILURE MECHANISM: the AMEND-R1 order fixed only line 26; the executor's S8 self-check line
  kept the delivery-time off-by-one. Order-compliant; defect class not fully closed in the file.
- AFFECTED: HANDOFF.md internal consistency only; the manifest itself is correct and complete.
- CORRECTION (final regeneration): line 50 → "363 rows + self-exclusion".
- REVALIDATION PREDICATE: no occurrence of "362 rows" in HANDOFF.md ∧ manifest row count == 363.

### **P3-R2-5 — script-level residual root causes: the P3-1 and P3-3 generator defects persist inside 03_SCRIPTS (a future re-run would undo the C3/C5 artifact fixes)**

- SOURCE: 03_SCRIPTS\s5_consumer_census_pass15.py line 23: `result = {… "generator":
  "03_SCRIPTS/s3_ghidra_routing_pass15.py"}` — the artifact was corrected (C3) but the script
  still hard-codes the OLD non-existent-script name for its own output. AND
  03_SCRIPTS\s1_framing_census.py line 195 (`u8_vals.add(row["u16_at_payload_04"])`) + line 220
  (emits that set under `"distinct_u16_at_payload_08": sorted(u8_vals)`) — the C5 artifact fix
  (key rename + correct aggregate) is not reflected in the generator; a re-run would re-mislabel
  the key as an array and erase the {"0x80": 1366} aggregate.
- AMEND-R1 COMPLIANCE: this is disclosed/deferred, not a violation — AMEND_LOG C5 states
  "In-place metadata-label fix ONLY: s1_framing_census.py was NOT re-run (per the AMEND-R1
  order)" and C3 fixed only the artifact field; round-1 P3-5's disposition likewise defers the
  s5_tlv_walk_census.py fix to "any future regeneration".
- AFFECTED: nothing now (artifacts on disk are correct; this worker verified their content and
  identity); risk is regeneration-undo.
- CORRECTION (final regeneration): fix both scripts' self-declarations (PASS15 generator name;
  the framing census key + add the true aggregate), or gate any re-run against re-introducing
  the defects.
- REVALIDATION PREDICATE: PASS15_GHIDRA_DUMP.json generator == the script's own hard-coded value;
  s1_framing_census.py emits distinct_u16_at_payload_04 (array) + distinct_u16_at_payload_08
  (histogram).

## 7. Coverage statement (L11: no absolutes without denominators)

- FULL READ (this session): RUN_CONTRACT.md (213/213 lines); 06_REPORT\AMEND_LOG_R1.md (199/199);
  04_QC\QC_REPORT.md round-1 (475/475); 02_ANALYSIS\BLAST_RADIUS.md (89/89);
  06_REPORT\EVIDENCE_INDEX.md (78/78); 06_REPORT\HANDOFF.md (57/57); 06_REPORT\REPORT.md (90/90);
  03_SCRIPTS\s5_consumer_census_pass15.py (67/67); 01_RAW\GHIDRA_ROUTING\DECOMP_FUN_0070e810.txt
  (full), DISASM_FUN_0070e810.txt (full, through RET @0x70E928), PASS4_DECOMP_FUN_0070e470.txt
  (full); 03_SCRIPTS\s1_framing_census.py lines 190–225 (the census-emission region).
- PROGRAMMATIC FULL PARSE + RECOMPUTE (own tools): MANIFEST_SHA256.csv (all 364 rows incl. NOTE);
  ALL 365 package files outside 04_QC hashed (diff census); RECORD_FRAMING_SUMMARY.json (full
  JSON parse + field-by-field comparison vs this worker's own VFS walk); the raw VFS full walk
  (1366/1366 records: u16@+0x08, u16@+0x04, u32@+0, u16@+0x2E, +0x30 field for EVERY record);
  the pinned EXE: whole-.text E8 census + 3 pattern censuses (PUSH 0xA9808C / PUSH 0xA86858 /
  PUSH 0xA86820) + 18 targeted byte probes.
- BOUNDED (region read; whole-file identity otherwise hash-verified): PASS15_GHIDRA_DUMP.json
  and RELEVANT_XREFS.json beyond their generator/header fields (their 202-site / chain content
  was round-1 QC's full-read scope and was independently reproduced there; this round
  byte-verifies the files via the AFTER hashes and verifies the corrected fields + spans).
- NOT_CHECKED (explicit; none load-bearing for the AMEND-R1 verification): content of the 356
  unchanged files beyond identity (all hash-matched to the delivery manifest that round-1 QC
  verified against disk; their content was round-1 QC's full-read scope); content of the 14
  round-1 04_QC files (round-1's own outputs; mtime-verified untouched by AMEND-R1); the
  remaining 03_SCRIPTS / 00_CONTROL transcriptions (S0 identities re-measured directly by this
  worker); no runtime behavior (STATIC_ONLY by contract; nothing launched).
- COVERAGE ALGEBRA: 365 files outside 04_QC = 356 unchanged (hash-verified identical) +
  7 changed C1..C7 (identity + content + span verified) + 1 new C8 (identity + content verified)
  + 1 manifest (fully parsed; self-excluded). 04_QC = 14 round-1 files (untouched) + 9 QC-R2
  files (4 tools + 4 result JSONs + this report). Total package at QC-R2 close: 374 files.
- UNCHECKED LOAD-BEARING COMPONENTS: NONE for this round's question (every dispatched claim was
  traced to physical bytes, exact file content, or exact hash).

## 8. QC-R2 write record (writes confined to 04_QC\; nothing else touched)

- 04_QC\qc_tools\q2r1_diff_census.py; q2r2_bytefacts.py; q2r3_vfs_census.py; q2r4_span_check.py
- 04_QC\QC_R2_DIFF_CENSUS_RESULT.json; QC_R2_BYTEFACTS_RESULT.json; QC_R2_VFS_WALK_RESULT.json;
  QC_R2_SPAN_CHECK_RESULT.json
- 04_QC\QC_R2_TARGETED_REPORT.md (this file)
- Git: read-only only (rev-parse / status); no stage/commit/push; HEAD unchanged at close.
- Round-1 QC artifacts and all executor evidence untouched (no re-runs of any executor script;
  s1_framing_census.py NOT executed — per the AMEND-R1 order — so no artifact could be
  regenerated/altered by this round).

## 9. Verdict justification + NEXT_PARENT_ACTION

The AMEND-R1 round did exactly what it was ordered to do, and every correction is byte-verified:
the diff census matches the expected delta EXACTLY (7/356/0 + the two expected unmanifested
files), all BEFORE states agree with the delivery manifest, all AFTER states agree with the
dispatch's declared identities (except C8's one-character hash defect, P3-R2-1), all spans are
verbatim, the corrected science wording (mechanism in FUN_0070c680; FUN_0070E810 = textures/.vfs
opener; EnvironmentZones family) is byte-confirmed at every cited instruction, and the census
facts (5 itoa sites / none in window; u16@+0x08 == 0x80 in 1366/1366; distinct 1..190) are
independently re-derived. The five P3 findings are precision/residual items for the final
regeneration checklist; none requires reopening any verdict.

QC_R2_VERDICT = **PASS_WITH_FINDINGS** (0×P0, 0×P1, 0×P2, 5×P3).

NEXT_PARENT_ACTION (advisory, for PE-MASTER): (1) record the corrected C8 identity from
P3-R2-1 in PE-MASTER's own records and check the executor's delivery notice to locate the
transcription origin; (2) add P3-R2-2..P3-R2-5 to the final-regeneration checklist (0x958DCD
VA; textures attribution; HANDOFF line 50; both scripts' self-declarations) together with the
already-ordered manifest regeneration; (3) the REPORT.md INDEPENDENT_QC forward reference to
this file is now complete; (4) the package remains under the contract §19 hard stop — no
further science, implementation, client launch or milestone action is implied by this report.
