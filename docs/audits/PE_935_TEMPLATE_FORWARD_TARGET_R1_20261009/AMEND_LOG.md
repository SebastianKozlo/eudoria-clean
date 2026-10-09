# AMEND_LOG — PE_935_TEMPLATE_FORWARD_TARGET_R1_20261009

## Records-correction round R1 — 2026-10-09

- **Round class**: BOUNDED RECORDS-ONLY correction (max this one round), dispatched by
  PE-MASTER against this NOT-YET-PUBLISHED package after its fresh internal QC
  (`PE_935_TEMPLATE_FORWARD_TARGET_R1_20261009_QC_R1_20261009`, verdict
  **QC_PASS_WITH_FINDINGS**: zero P0/P1; 1xP2, 5xP3; the findings ledger = this round's
  worklist). Executor: pe-reconstruction. NO_NESTED_TASKS.
- **Scope discipline (mandate respected)**: NO new science, no new binary analysis, no
  Ghidra, no EXE writes. The ONLY machine execution was the P2-1/P3-1 revalidation
  classifier re-run (explicitly authorized by the dispatch): a corrected completeness
  classifier executed from scratch, importing the run's own decoder
  `SCRATCH\x86probe.py` READ-ONLY (unmodified) and reading ONLY the physical EXE
  (read-only; SHA256 re-verified before the run, unchanged) plus
  `SCRATCH\body_end_analysis.json` (read-only) for the body ranges. It wrote NOTHING to
  SCRATCH or to the package; its outputs live in the correction round's temp workspace
  (hashes below) and are embedded as records in
  `CALLEE_FIELD_ACCESS_CENSUS.json.census_completeness_revalidation`.
- **NO science value changed** (verified per file below): no byte pin altered; no
  dataflow classification altered (E1/E2 POINTER_IDENTITY_CONFIRMED and E3
  POINTER_IDENTITY_CONFIRMED_CONDITIONAL verbatim everywhere, E3's
  classification_reason untouched); no gate result altered (G1-G7 all PASS; only
  descriptive class counts inside gate-row text were corrected); no claim limit
  altered (MODEL_218757_TO_CMO_JOIN / WORLD_INSTANCE_IDENTITY / HISTORICAL_PLACEMENT =
  NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO — untouched).
- **Untouched by this round**: QC_RESULTS.json + QC_REPORT.md (QC artifacts, frozen),
  ALL of SCRATCH (incl. selfcheck.py with the original defective classifier rule —
  documented, not modified), AUDIT_ENTRYPOINT.md (not created/touched), PREREGISTRATION.md,
  INPUT_IDENTITIES.json, 01_RAW/OWN_DECODER_WINDOWS.json, 01_RAW/F8_BODY_CROSSCHECK.json,
  01_RAW/PHASE0_INPUT_IDENTITIES_RAW.json, 01_RAW/KEY_REGION_LISTINGS.md,
  01_RAW/SENTINEL_00BA5800_DUMP.json, 01_RAW/GHIDRA_HYPOTHESIS_EXPORT.json (quarantine
  intact), 01_RAW/OBJDUMP_LISTINGS/*. No commit/push (package untracked; tracked tree
  clean; HEAD == BASE == origin/master == cea10e9cfcaa2e814f5cfe4269fd2a6a409d54da).
  No MANIFEST created.

---

## P2-1 revalidation result (the round's one machine execution)

**Predicate** (QC P2-1 + P3-1): re-run the completeness classifier over ALL memory-form
operands (135 incl. the 9 A0-A3 moffs and the 42 LEA forms): expected unclassified=[]
with the 7 formerly mislabeled operands carrying their true base provenance.

**Method**: corrected classifier (rules recorded in
`CALLEE_FIELD_ACCESS_CENSUS.json.machine_classifier_rules_corrected`: the original
SCRATCH rule chain with ONLY the defective W_A `[EAX…` rule split into R10a-R10e, plus
the moffs coverage extension and two census-row-naming subset refinements). Six body
ranges decoded FRESH from the physical EXE by x86probe (imported read-only); body
ranges from SCRATCH\body_end_analysis.json.

**Result: PASS**
- EXE SHA256 before the run: `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` (unchanged; read-only).
- Body instructions reproduced: 339 + 54 + 2 + 2 + 19 + 35 = **451** (all per-window counts match the dual-verified baseline).
- Memory-form operands: **135 total** = 126 modrm-form + 9 A0-A3 moffs (42 LEA forms among the modrm); per-window 102/15/1/1/3/13 (all match the QC's own QC_D2_DECODE census).
- **unclassified = [] (0 of 135)**; zero string-op forms; zero incomplete decodes; all 12 in-run region byte checks match (SUB ESP,0xC / MOV EAX,ESP / MOV ECX,ESP sites and the CALL 0x843DD0 / 0x50CAF0 / 0x50D8C0 / 0x41B3A0 base producers).
- The **7 formerly mislabeled operands** now carry their TRUE provenance —
  `0x005111A5` [EAX] read = CALL 0x00843DD0 result (base produced @0x005111A0);
  `0x005113DC/0x005113DE/0x005113E5` and `0x00511455/0x0051145A/0x0051145D` = EAX=ESP
  stack writes (MOV EAX,ESP @0x005113D5 / @0x00511453 after SUB ESP,0xC) — matching
  the auditor reference `SCRATCH\QC_FRESH\QC_D6_FINAL_PINS.json` my_unclassified
  one-for-one. All 18 W_A `[EAX…` operands are accounted: 11 struct-copy sources
  (5 x 0x50CAF0 range + 6 x 0x50D8C0 range) + 1 0x843DD0-result read + 6 EAX=ESP
  stack writes. **No template-derived access is missing from the direct/forward rows.**
- Classifier script: `C:\Users\User\AppData\Local\Temp\opencode\p21_census_revalidation.py`,
  SHA256 `DA70B5732F1B615691135E12F3D2E5605607D51A9F1E85AF8DB1240682E0CBC4`
  (temp workspace, outside git and the package).
- Full 135-row machine output: `p21_census_revalidation_output.json`,
  SHA256 `3BA2239A7D482B37985997C0F7F4CE7493A4A760961F820AC388B2556D9AF3C2`, 37786 B
  (temp workspace); digest embedded in the census artifact.

---

## Per-file change ledger (every change old -> new, with finding IDs and pre/post SHA256)

### 1. CALLEE_FIELD_ACCESS_CENSUS.json — findings P2-1 (+ P3-1 revalidation record)
- pre SHA256 `CCF4C3A4986FE27B97114FF6472DEC910BA643A280F414992200B79DAFC7243F` (10371 B)
- post SHA256 `2FAA18EB52ADE9DEF32B7D14270C0358F023DFB03CCD85C44D28FCD3442E6877` (24683 B)
- OLD `non_template_memory_rejections` entry 3 (one combined entry): *"W_A: [EAX]/[EAX+0x4]..[EAX+0x10] source reads @0x005112B1-0x005112CF and @0x0051130C-0x00511330 — base = result of CALL 0x0050CAF0 / 0x0050D8C0 …; their DESTINATION stores [ECX]/[ECX+0x4]..[ECX+0x14] @0x005112B8-0x005112CF and @0x00511313-0x00511330 have base ECX = ESP …"* — the single class under which the machine classifier (SCRATCH\selfcheck.py rule `W_A and ea.startswith("[EAX")`) mislabeled 7 non-template operands.
- NEW: that entry is SPLIT into 4 entries with exact machine-extracted operand lists:
  (a) struct-copy SOURCE reads, range 1 (5 dwords, base = CALL 0x50CAF0 result @0x005112AC) and range 2 (6 dwords incl. [EAX+0x14], base = CALL 0x50D8C0 result @0x00511307);
  (b) the [EAX] read @0x005111A5 — base = CALL 0x00843DD0 result @0x005111A0;
  (c) the six [EAX]/[EAX+0x4]/[EAX+0x8] STACK WRITES @0x005113DC/DE/E5 and @0x00511455/5A/5D — base EAX = ESP (MOV EAX,ESP @0x005113D5 / @0x00511453 after SUB ESP,0xC);
  (d) the struct-copy DESTINATION stores (ECX = ESP @0x005112B6 / @0x00511311).
  Rejection-class count 8 -> **11**. Each split entry carries its QC-finding provenance note.
- ADDED section `machine_classifier_rules_corrected` (the corrected rule definitions R1-R11 + R4a/R4b refinements + EXT1 moffs extension; SCRATCH itself unmodified).
- ADDED section `census_completeness_revalidation` (method, coverage 135 = 126 modrm + 9 moffs (42 LEA), per-window counts, unclassified=[], the 7 operands' true provenance rows, the full class_operand_census digest, cross-check vs the auditor's QC_FRESH references, result PASS).
- UNCHANGED: all 4 template_pointer_direct_memory_accesses rows, all 7
  template_derived_value_stores_and_forwards rows, all 5 anchor_registry_memory rows,
  the 7 untouched rejection classes, float_census, scope, naming_discipline.

### 2. 01_RAW/SELF_CHECK.json — findings P3-1 + P3-3
- pre SHA256 `F77563D1BA5D9307D413B2D7F866DAF19B45E495611366B6E3093E06944E8C84` (463 B)
- post SHA256 `41FD98F1355E18B088502659A846A5B687B21686B803F19BC011672D45399710` (2304 B)
- OLD census_completeness: `"memory_operands_in_bodies": 126` (modrm-only denominator, definitional gap).
- NEW: `"memory_operands_in_bodies": 135` (all-forms) with BOTH numbers explicit:
  `memory_operands_in_bodies_modrm_form: 126`, `moffs_a0_a3_forms_enumerated: 9`, and a
  `denominator_definition` naming the 9 moffs forms with their VAs
  (W_A: 64 A1 FS:[0x0] @0x00511077, 64 A3 FS:[0x0] @0x00511097, A1 [0x00B9D8D0] @0x00511088;
  W_E2: 64 A1 @0x0043A557, A1 [0x00B9D8D0] @0x0043A55F, A1 [0x00BA1824] @0x0043A571,
  64 A3 @0x0043A56B, A3 [0x00BA1824] @0x0043A59B, A3 [0x00BA1824] @0x0043A5B2) and
  their census classes. `unclassified: []` and `pass: true` unchanged.
- OLD package_hygiene: `"files": 22` (unexplained vs HANDOFF's 23).
- NEW: `files: 22` KEPT (honest for its moment) + `files_note`: 22 = census at SELF_CHECK
  execution time (mtime 10:52:46), BEFORE EVIDENCE_INDEX.md was written (10:53:29); the
  TRUE final assembled-package census is 23 (HANDOFF correct; EVIDENCE_INDEX.md is the
  23rd file, self-excluded); temporal note per P3-3, including the post-correction
  additions (AMEND_LOG.md + the QC pair). `violations: []` / `pass: true` unchanged;
  byte_rechecks (46/pass) and rel32 (14/pass) untouched.

### 3. POINTER_DATAFLOW.json — finding P3-2
- pre SHA256 `BFA4E063A8E73492C5F3D8BBAC8FAAD601090439A14C0374343A62B9BD158670` (15104 B)
- post SHA256 `6D8D8E517B549C68D1FC9D1E3B1139D8EA48343A410B5BCA60D52DE9A50D1E6D` (15977 B)
- OLD E3.intervening_calls: `direct_path: "NONE (0x006C3F8D -> …)"`, `growth_path: "CALL 0x006C2E00 @0x006C3FA9 … ABI assumption"` — omitted the crossing CALL 0x006C3F74 although the chain anchor 0x006C3F67 precedes it.
- NEW: `crossing_1_CALL_0x006C3F74` (crossed on BOTH paths; verification mode =
  BYTE-PROVEN EDI-SAFE via the callee's open 4-byte body 8B 41 08 C3 which never
  writes EDI) + `crossing_2_CALL_0x006C2E00` (growth path only; verification mode =
  ABI ASSUMPTION; still the ONLY ABI-assumption crossing) + updated direct_path/growth_path
  keys referencing the crossings. `classification` (POINTER_IDENTITY_CONFIRMED_CONDITIONAL)
  and `classification_reason` UNCHANGED (verified verbatim post-edit) — the census
  listing changed, the verdict and its condition did not.

### 4. CALL_EDGE_PROVENANCE.json — finding P3-4
- pre SHA256 `3F8747103D70A61BC6B80D57BDF655562862CD5CC2674E3D3B364E03820CA7BA` (5388 B)
- post SHA256 `0BC4D020BD54B14559E51279876DB383D5FEB48E2BAE5068EB065DDB0773F652` (6465 B)
- OLD: 13 callsite entries (3 subject + 10 anchor) while SELF_CHECK rel32 checked = 14
  (the 14th, 0x00511154 -> 0x41B3A0, existed only in SCRATCH\selfcheck.py call_targets).
- NEW: 14th entry added to `anchor_callsites_in_windows`:
  `A4_FUN_00511070_x_0041B3A0_second_receiver_producer` — callsite 0x511154,
  `E8 47 A2 F0 FF`, rel32 target recomputed 0x41b3a0, instruction_before
  `0x511152 / 74 1D / JE / [0x511171]`, with a provenance note (receiver producer of the
  second FUN_007CE1E0 use @0x51115B; byte-checked in SELF_CHECK (1); recomputed by the
  QC 14/14). All 13 existing entries unchanged; artifact now agrees with SELF_CHECK's
  checked = 14.

### 5. FALSIFIER_RESULTS.json — findings P2-1 + P3-2 (package-wide sweep of the same defects)
- pre SHA256 `762329221E84D809BAC1F1B7373BA752EA8F6D0B1319914A06163E6F2B1BDB4B` (11051 B)
- post SHA256 `CD809AA004C2BEA73C3A0A1780F25BBBF514784A46302BEB5E1160ED0BDF4F4E` (11885 B)
- F1.measured_quantity OLD: *"E3 = 1 writer (MOV ECX,EDI @0x006C3FAE), 0 intervening calls on the direct path, 1 on the growth path (CALL 0x006C2E00 …)"* — NEW: E3 crossings enumerated completely: 1 on BOTH paths (CALL 0x006C3F74 — byte-proven EDI-safe) plus 1 on the growth path (CALL 0x006C2E00 — the ABI-assumption crossing); P3-2 note appended. F1 failure_case_detected + outcome UNCHANGED.
- F3.measured_quantity OLD: *"8 rejection classes enumerated (vector, frame locals, param_3 struct, cookie/SEH, unrelated globals)"* — NEW: *"11 rejection classes enumerated (vector header/slot, frame locals, struct-copy sources 0x50CAF0/0x50D8C0, the 0x843DD0-result read @0x005111A5, the EAX=ESP stack-write regions, struct-copy stack destinations, param_3 struct, cookie/SEH, unrelated globals)"* with the P2-1 old->new note. F3 design / independent_source_of_truth / why_non_circular / failure_case_detected / outcome UNCHANGED.
- F2, F4-F8 records UNCHANGED.

### 6. FINAL_REPORT.md — findings P2-1 + P3-2
- pre SHA256 `CB76F7439A722A8A5DC31E500D799FB3A8AAB0CC356C02A57C82F8E23235580D` (17152 B)
- post SHA256 `B695C2CDA3140C55F390A18F295C4190F7823AF1426E69BE7F3DF5D76601AF29` (18362 B)
- Section 4 E3 table row "Intervening calls" cell OLD: *"fast: none; growth: CALL 0x006C2E00"* — NEW: *"both paths: CALL 0x006C3F74 (byte-proven EDI-safe …); growth additionally: CALL 0x006C2E00 @0x006C3FA9 (the ABI-assumption crossing, body CLOSED)"* with P3-2 note. Classification cell (POINTER_IDENTITY_CONFIRMED_CONDITIONAL + condition) UNCHANGED.
- Section 5 OLD: *"8 rejection classes enumerate every OTHER memory operand …: param_2's vector header, frame locals, the 0x50CAF0/0x50D8C0 result structs (falsifier F3 catch), param_3's struct, the GS cookie/SEH frames, [0x00BA2CE4], the lookup's stack locals."* — NEW: 11-class enumeration with the true provenance split (struct-copy SOURCE reads; the CALL 0x00843DD0-result read @0x005111A5; the EAX=ESP stack-write regions; the struct-copy STACK destinations; …) + the P2-1 correction note citing the 135-operand re-run (unclassified=[]).
- Section 11 G3 gate row OLD: *"…+ 8 rejection classes; …"* — NEW: *"…+ 11 rejection classes (class split per QC finding P2-1 …; corrected classifier re-run over all 135 memory-form operands: unclassified=[]); …"*. **Gate verdict PASS unchanged.**
- All other sections (incl. claim limits section 9, NOT_CHECKED section 10, all other gate rows) UNCHANGED.

### 7. HANDOFF.md — findings P2-1 + P3-2
- pre SHA256 `27F5893DFCE0FEFD85059066A94B0BCCF559BB9B376DD011452CE1FDC8DE5419` (12340 B)
- post SHA256 `F02836C747BDC17F04248DE8BEAF14283AE9EB9E6626E8D8185E1C33181541BD` (12825 B)
- Phase-2 result OLD: *"…+ 8 rejection classes; NO field named…"* — NEW: *"…+ 11 rejection classes (class split per QC finding P2-1 …; corrected classifier re-run over all 135 memory-form operands yields unclassified=[] …)…"*. Phase verdict PASS unchanged.
- E3 classification table row OLD basis: *"direct path byte-confirmed (MOV ECX,EDI @0x006C3FAE, 0 intervening calls); vector-growth path crosses CALL 0x006C2E00 …"* — NEW: *"direct path byte-confirmed (MOV ECX,EDI @0x006C3FAE; both paths cross CALL 0x006C3F74 first — byte-proven EDI-safe …); vector-growth path additionally crosses CALL 0x006C2E00 @0x006C3FA9 (body CLOSED) — EDI survival across THAT call rests on standard callee-saved discipline, recorded as the condition"*. Classification POINTER_IDENTITY_CONFIRMED_CONDITIONAL unchanged.
- MANDATORY HANDOFF BLOCK, RUN_STATUS COMPLETE, all falsifier records, NOT_CHECKED list, claim limits, 12-line summary: UNCHANGED.

### 8. EVIDENCE_INDEX.md — bookkeeping for all findings (index integrity)
- pre SHA256 `42B62ACF2CBA642E2DD0F70C6493A55011130C5BFEA900BD29F9CD4A88D8E515` (9781 B)
- post SHA256 `F241B6E05DA26FD663B198BD529C7A6909FE174BD04E1714E284279018D91F03` (10625 B)
- The 8 rows of the files edited by this round re-hashed to the POST-correction state
  (independently re-verified: all 22 package rows match the physical files post-edit).
- Roles-table row for CALLEE_FIELD_ACCESS_CENSUS.json: "8 rejection classes" -> "11
  rejection classes + corrected machine-classifier rules + 135-operand
  census-completeness revalidation".
- ADDED the AMENDMENT header note: edited-file rows re-hashed; files added after
  assembly (QC_RESULTS.json, QC_REPORT.md, AMEND_LOG.md) intentionally NOT indexed —
  AMEND_LOG because indexing it would create a hash circularity (it records this
  index's post-correction SHA256, stated above).
- SCRATCH sections UNCHANGED (SCRATCH was not modified this round; the SCRATCH
  body_end_analysis.json / selfcheck.json rows keep their original hashes).

### 9. 01_RAW/BODY_END_ANALYSIS.json — finding P3-5 (informational, optional — carried)
- pre SHA256 `947603D7B95A4E43890EF88BB31B505F8199D216BC236A5E1741370C2853C808` (5084 B)
- post SHA256 `A6E9428631F8AC970051C37E0A1FABF82CC38B3DC4FF37FB5C19BF016A1DB68C` (5996 B)
- W_A ret_candidates[0] and body_end_detail: ADDED one `pattern_note` line: "'6A FF 68 …'
  is an MSVC SEH function prologue (PUSH -1; PUSH handler; MOV EAX,FS:[0]);
  is_next_prologue=false is a conservative pattern match, NOT a body-end defect — the
  pre-registered body-end rule is satisfied independently by the 4x CC run, and the
  1212 B / 339-insn body determination is unaffected."
- All measured fields (ret_va, ret_len, after_hex, padding_run, next_bytes,
  is_next_prologue, is_padding_terminated) and ALL other windows UNCHANGED.

### New file created by this round (the only one)
- **AMEND_LOG.md** (this file) — the correction log. Not added to EVIDENCE_INDEX.md
  (hash circularity, see the index amendment note).

---

## Package census after this round

- Physical files: **26** = the 23 assembled package files + QC_RESULTS.json +
  QC_REPORT.md (added by the internal QC after assembly) + AMEND_LOG.md (this file).
- EVIDENCE_INDEX.md covers 22 files (self-excluded; the 3 post-assembly additions are
  explained in its amendment note). Index-vs-file verification post-correction:
  **22/22 rows match** (independently re-executed this round).
- All 9 edited files re-read fully after editing; all 6 edited JSONs parse
  (json.load OK: CALLEE_FIELD_ACCESS_CENSUS.json, CALL_EDGE_PROVENANCE.json,
  FALSIFIER_RESULTS.json, POINTER_DATAFLOW.json, 01_RAW/SELF_CHECK.json,
  01_RAW/BODY_END_ANALYSIS.json). No BOM, no CRLF in any edited file.
- Package-wide sweep for stale defective labels post-correction: "8 rejection
  classes" / `"memory_operands_in_bodies": 126` / "fast: none" / "0 intervening calls
  on the direct path" — **0 occurrences** in executor artifacts (remaining matches are
  only the QC artifacts' findings ledger and the disclosed old->new notes inside the
  amendment annotations, which quote the old values as history).

## Findings disposition

| Finding | Severity | Disposition |
|---|---|---|
| P2-1 census machine-classifier provenance over-breadth (7 mislabeled W_A [EAX] operands) | P2 | **RESOLVED** — class text/rules split in CALLEE_FIELD_ACCESS_CENSUS.json; corrected classifier re-run over all 135 forms: unclassified=[], 7 operands carry true provenance; summary texts in FINAL_REPORT.md/HANDOFF.md/FALSIFIER_RESULTS.json/EVIDENCE_INDEX.md aligned (11 rejection classes) |
| P3-1 SELF_CHECK "126 memory operands" excludes the 9 moffs forms | P3 | **RESOLVED** — SELF_CHECK states both numbers explicitly (135 all-forms / 126 modrm-form) with the 9 moffs enumerated; classifier extended to moffs in the revalidation |
| P3-2 E3 census omits byte-safe crossing CALL 0x006C3F74 | P3 | **RESOLVED** — both crossings listed in POINTER_DATAFLOW.json E3.intervening_calls with verification modes (byte-proven vs ABI-assumption); FINAL_REPORT.md/HANDOFF.md/FALSIFIER_RESULTS.json (F1) aligned; classification and condition unchanged |
| P3-3 SELF_CHECK files:22 vs HANDOFF 23 | P3 | **RESOLVED** — reconciliation note in SELF_CHECK.json (HANDOFF's 23 = true final assembled census; SELF_CHECK's 22 = pre-EVIDENCE_INDEX moment; temporal note; post-correction census 26 recorded here) |
| P3-4 CALL_EDGE_PROVENANCE 13 entries vs SELF_CHECK checked:14 | P3 | **RESOLVED** — 14th entry added (0x00511154 -> 0x41B3A0); artifact now agrees with the 14 recomputations |
| P3-5 informational: 6A FF SEH prologue pattern-miss | P3 | **CARRIED** (optional item, cheap) — one-line pattern_note added to BODY_END_ANALYSIS.json W_A ret_candidates[0] + body_end_detail |

**RUN_STATUS = COMPLETE (records-correction round R1; all 5 mandatory findings resolved,
1 optional finding carried; revalidation PASS; no science value changed).**
