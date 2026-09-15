# AMEND_LOG_R1 — PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915
# Corrections to THIS RUN's own files only (contract rule 14). No pin mismatch was found in this run —
# a pin mismatch would be a FINDING recorded loudly in the reports, never papered over here.

## AMEND-1 (2026-09-15T06:3x local) — EVIDENCE_INDEX self-hash artifact
- WHAT: the first generation of 03_EVIDENCE/EVIDENCE_INDEX.csv included a row for EVIDENCE_INDEX.csv itself
  that captured the file in its in-progress empty state (SHA256 E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855,
  size 0) — a meaningless self-reference, and it also lacked a 06_REPORT/MANIFEST_SHA256.csv row (written later
  in the same pass).
- FIX: gen_manifest.py updated (index self-exclusion + manifest-row exclusion, documented in 03_EVIDENCE/README.md);
  EVIDENCE_INDEX.csv and MANIFEST_SHA256.csv regenerated in one pass; both now carry final, mutually consistent
  hashes (manifest excludes only itself, per L12).
- NATURE: mechanical packaging artifact; NO science content, NO measured value, NO pin affected.

## AMEND-2 (2026-09-15T06:4x local) — raw-file text encoding normalization to UTF-8
- WHAT: the first generation of the gen_raw_evidence.py outputs (FUN_0050A050_DOWNSTREAM_DISASM.txt,
  FUN_00437F70_DISASM.txt, FUN_0082B5A0_DISASM.txt, SOURCE_VECTOR_LAYOUT_RAW.txt, HELPER82B5A0_CALLER_CENSUS.csv/.txt)
  used the Windows default codec (cp1252) for open(...,"w"), which left the em-dash characters in their headers as
  cp1252 bytes that render as mojibake to UTF-8 readers. Content (addresses/bytes/formulas) was never affected.
- FIX: all generator open() calls made explicitly encoding="utf-8" (11 sites across gen_raw_evidence.py and
  gen_manifest.py; one-shot helper patch_utf8.py, kept in 00_CONTROL/scripts/ for the audit trail); raw files
  regenerated deterministically (pin re-verification re-run inside the generator: 37/37 MATCH); SCRIPT_SHA256.csv /
  EVIDENCE_INDEX.csv / MANIFEST_SHA256.csv regenerated in one final pass to match the new hashes.
- NATURE: packaging/encoding correction; NO science content, NO measured value, NO pin affected.

## DISCLOSURE (not an amend — no artifact ever contained the bad value)
The executor's first quick PE-parse during S0 read the ImageBase field from the wrong Optional-Header offset
(e+28, which returns SizeOfCode 0x674000 instead of ImageBase). It was caught and re-measured at the correct
offset (e+24+28 = 0x00400000, PIN MATCH) BEFORE any run artifact was written; the event and its resolution are
disclosed in 01_RAW/AT_RUN_START_GIT_OBSERVATION.md SECTION 2.

---

# CORRECTION PASS (fresh-QC findings P1-1, P1-2, P2-1..P2-4, P3-1..P3-3; bounded batch; STATIC-ONLY; zero git mutations)

Convention for this pass: every amended file has a byte-exact .pre copy under 00_CONTROL/PRE_EDIT/ (mirrored
relative path + ".pre"); entries below list finding ID, file, exact change, why, and the .pre/new SHA256 pair.
No science conclusion changed — the fresh QC independently CONFIRMED every headline claim; these are
proof-documentation, provenance, count and wording corrections. Science re-verified where load-bearing: the
executor's OWN census numbers are in 01_RAW/ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt.

## AMEND-3 (2026-09-15 correction pass) — P1-1: "never written / S immutable" proof re-measured with exhaustive channels
- WHAT: E.3's original 4-channel text enumerated narrower channels than its prose claimed (channel (4) said
  "all decoded" of an "x5" list that was neither 5 nor exhaustive — 24 push sites exist; channel (1) listed only
  5 store encodings; the ECX-consumer list omitted 0x48BAC0 and misclassified 0x437E80/0x82B870 as "[reads]"
  and 0x58E4B0/0x58E520 as "[reads]"; the computed-base channel scanned only [0xba9200,0xba9240]).
- FIX: NEW census script 00_CONTROL/scripts/census_triple_writes.py (NEW, SHA256
  5777F559101CFAC2CAEACC6ADA23291E412F046909D52677E2E751A2E98C734B, 50894 bytes; S0 fail-closed; read-only on
  the EXE) generated NEW raw evidence 01_RAW/ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt (NEW, SHA256
  FEF5DC1C9E4B4C212D4D80E78DAED0574EFA0CD79ACBC22823E7D9D6C401FF87, 77113 bytes) with the executor's OWN
  numbers: whole-image occurrences 0xBA921C=107 / 0xBA9220=81 / 0xBA9224=80 (=268, all .text — MATCHES the QC's
  independent 107/81/80); classification decomposes EXACTLY as 81+81+80 absolute loads (A1/8B mod00 rm101),
  24 push-imm32 address-takers, 2 mov r32,imm32 getters (0x50AA1D, 0x96B960); STORE-CLASS candidates 0 across
  ALL channels (generic operand-access classification covering every x86 store encoding; widened dwords
  0xBA9215..0xBA9227; computed-base hunt [0xBA9000,0xBA92C0) = 34 values/349 occurrences, QC-subwindow
  [0xBA9000,0xBA921C) = 22 values/45 occurrences — MATCHES the QC's independent 22/45); 23/24 push-site
  consumers read-only + 1 disclosed residual (0x488BEA); both getter chains read-only (4 E8 callers of
  0x50AA10; 1 E8 caller + 3 vtable placements of 0x96B960); the 9 ECX-receiving functions read/forward/clobber,
  0 stores to [ECX+0/4/8]; neighborhood writes stop at 0xBA921B; .data virtual-tail zero-init confirmed
  (RVA 0x7A921C/20/24 > raw end 0x7A0000; vsize 0x3D6E4 > rawsize 0x34000). E.3 was rewritten to enumerate
  channels (1)-(6), the decoded set, and the undecoded residuals; the same correction was applied to every
  package location repeating the claim:
  - 01_RAW/END_TO_END_VALUE_FLOW_RAW.txt E.3 (pre 0BBEC584C497C7E474DA1FAA602FF206F5E97410D66102B222B5ADE5FA38EDC6/8293
    -> new A8077F4910BBF96026B6DAAADEB6A381C15A11778EFCB9132A20DF31555904C4/14061): full channel enumeration + census reference.
  - 06_REPORT/REPORT.md (pre 986182BE8837106FB3403336060D177B634EF4FBCD72E5E5FEACCA8D841DC2DE/9935 -> one-line answer
    + executive summary item 3 + negative-control line reworded to cite the census; final new SHA in MANIFEST:
    C17A5691F161111403C5E427B24ABF7B279EB001942CC4528AE6E706DD701043/10897).
  - 02_ANALYSIS/HELPER_OPERATIONS.md (pre 1F3155E464E7F042BAD81B0AE08D780A444D877613186BC41E9CA901B56A1E6C/3863
    -> new BB719FD00B13D1C692A33AC182C78DF0831EAA7834D53A33C6D3AC87ADCFFF83/4118): "NEVER WRITTEN" now cites the census.
  - 01_RAW/FUN_00437F70_DISASM.txt [C.7]/[C.9](10) cross-references (pre
    54AA832AA948B7C4248EBA43C199EF95DF1D91BD837930825F9F4E2EB0FE328E/10244 -> new
    AE041E5A05D2040552ABE21C9BCC780C7B86B9FBE3657F90DE4101E4B7AE7656/11050; also carries the P3-3 wording fix).
  - 06_REPORT/STAGE_ACCEPTANCE_GATES.csv G6 evidence row (pre BF451C544297AD76DACC3F2EB0B86A3DDADF200267C9107328233EF2AF119B5A/4871
    -> new EAECE8B9B64BFBA7A31411BA76B6F698E60CBD0C773C3FCAA0A84F9C02A2ECAA/5275; also carries P2-2/P2-1).
  - 06_REPORT/HANDOFF.md PRIMARY_EVIDENCE_PATHS line for END_TO_END (pre
    817BA82D0F019C825201E244FE309A48A6855E508E4269720673FD0B5E06B34B/5645 -> new
    DE504596F26A46BA7358F1FF343FE07E536C84E4536BAA18FC87B33E76265243/6334; also carries P2-2/P2-3).
  - 00_CONTROL/scripts/gen_raw_evidence.py [C.7]/[C.9] literal texts (pre
    791E92FCB9B8A890333832D2E4804D6E56FB57CA7F4A4F8E8FAEF600F2DA534B/33940 -> new
    389C82C889F32E10C3C3F65E067E8C615BFF669CE3B741F890DEE0E0881E4C7C/36775; also carries P2-1/P2-2/P2-4/P3-3 fixes).
- FINDINGS recorded against the QC annex (measured, in the census file): (a) QC's 10th push-consumer
  "0x8DC5B0->0x92FFE0" is REFUTED by bytes — all 3 E8 callers of 0x8DC5B0 (0x4FC9E7, 0x522F92, 0x5F6D33) push
  stack-frame pointers, never &triple; the 0x5F6D21 push is consumed by the immediately-adjacent call 0x8DC5C0
  (conclusion unaffected — that chain is read-only). (b) QC's cited 0x48BAC0 clobber address 0x48BB19 is a
  secondary redefinition; the FIRST is 0x48BAD6 'lea ecx,[esp+0x10]' (same conclusion either way).
- WHY: QC P1-1 (material, must be corrected before persistence): the load-bearing reduction
  out[i]=f32(W[i]*0.01f) depends on S={0,0,0}; the proof text did not prove what it claimed.
- NATURE: proof-documentation + new evidence artifact. NO measured value changed; the conclusion
  (S={0,0,0}, immutable) is UNCHANGED and now backed by the exhaustive census.

## AMEND-4 (2026-09-15 correction pass) — P1-2: stale EVIDENCE_INDEX row for 03_EVIDENCE/README.md (root cause fixed)
- WHAT: EVIDENCE_INDEX.csv line for 03_EVIDENCE/README.md carried a stale hash+size (D53A02FD.../1251) while
  the disk file was 6EFD30CE58622B39245207B16C44D7210683CC89BCDA3C808A7339C62A464BE4/1255 (executor re-measured
  fresh at correction start — MATCH of QC's measurement; the manifest row was already correct). Root cause:
  gen_manifest.py wrote the index BEFORE rewriting README.md in the same pass, so the index always captured the
  pre-rewrite README.
- FIX: 00_CONTROL/scripts/gen_manifest.py (pre 70CE5EAF91740887402B86A9C1A26945DDE6B4B222130E9228E3771173BA47C4/7866
  -> new A88E730C0C039046AF9D8E820858D24B0494A109CA169111EFC7EF23D1964BD2/9505): generation order changed to
  SCRIPT_SHA256.csv -> README.md -> EVIDENCE_INDEX.csv -> MANIFEST_SHA256.csv so the index's README row captures
  the final file; README text documents the order; role map updated (36/36, census file, amended-file roles).
  EVIDENCE_INDEX.csv is REGENERATED (see AMEND-12; new hash recorded in MANIFEST post-regeneration).
- WHY: QC P1-2 (material, must be corrected before persistence): 03_EVIDENCE provenance integrity + AMEND-1's
  "mutually consistent" claim was falsified by the stale row.
- NATURE: mechanical provenance fix; NO science content.

## AMEND-5 (2026-09-15 correction pass) — P2-1: [A.2] padding miscount (12x int3 / 0x50A0B6 -> 6x 0xCC / 0x50A0B0)
- WHAT/WHY: QC P2-1 — the extent prose miscounted the printed byte string (only the first 6 of the 12 printed
  bytes are 0xCC). Re-measured: 6x 0xCC at 0x50A0AA..0x50A0AF; next function starts 0x50A0B0
  ('56 8b f1' = push esi; mov esi,ecx; cmp byte [esi+0x24],...). Extent verdict 0x50A050..0x50A0AA UNCHANGED.
- FIX: 01_RAW/FUN_0050A050_DOWNSTREAM_DISASM.txt [A.2] (pre AD0E2DD3F3EBD45F4DF30269FEB01068FB320A40411773556D4AA39CB1AA519E/13717
  -> new A27FD8B72B996B59D4C87FCF4CFBA279376140BF0C4C238999942403A7CB2589/14610; carries inline AMEND NOTE; also
  carries the P2-2 fix); 06_REPORT/REPORT.md KEY MEASURED FACTS line (in AMEND-3's file pair);
  06_REPORT/STAGE_ACCEPTANCE_GATES.csv G2 row (in AMEND-3's file pair);
  00_CONTROL/scripts/gen_raw_evidence.py [A.2] literals (in AMEND-3's file pair).
- NATURE: count correction; NO measured extent value changed.

## AMEND-6 (2026-09-15 correction pass) — P2-2: pinned-instruction count 37 -> 36
- WHAT/WHY: QC P2-2 — the contract pin block and the [A.3] PIN table each have 36 instruction lines ("fallback:"
  is a label); the verdict line hardcoded "ALL 37". G2 predicate (every pin MATCH) unchanged — 36/36 MATCH.
- FIX (4 report locations + 2 script literals): 01_RAW/FUN_0050A050_DOWNSTREAM_DISASM.txt [A.3] verdict (file pair
  in AMEND-5); 06_REPORT/REPORT.md (lines 57 + 100; file pair in AMEND-3);
  06_REPORT/STAGE_ACCEPTANCE_GATES.csv G2 row (file pair in AMEND-3); 06_REPORT/HANDOFF.md (lines 6 + 20; file
  pair in AMEND-3); 00_CONTROL/scripts/gen_raw_evidence.py verdict made dynamic len(pins) (file pair in AMEND-3);
  00_CONTROL/scripts/gen_manifest.py role map (file pair in AMEND-4). NOTE: the "37/37" string inside the
  historical AMEND-2 entry above is part of that entry's frozen record of what AMEND-2 did — superseded by this
  correction, not rewritten.
- NATURE: count correction; NO gate status changed.

## AMEND-7 (2026-09-15 correction pass) — P2-3: HANDOFF "No AMEND_LOG_R1.md" contradiction
- WHAT/WHY: QC P2-3 — HANDOFF's Notes for QC claimed "No AMEND_LOG_R1.md — no correction was needed after any
  run artifact was written" while the package contains AMEND_LOG_R1.md with 2 pre-existing entries.
- FIX: 06_REPORT/HANDOFF.md Notes for QC rewritten to state the package DOES contain 00_CONTROL/AMEND_LOG_R1.md
  (2 pre-existing entries + the correction-pass entries added now), with an inline AMEND NOTE (file pair in AMEND-3).
- NATURE: report-integrity correction; NO science content.

## AMEND-8 (2026-09-15 correction pass) — P2-4: fabricated prior_437f70_site cells for the 2 NON-PAIR rows
- WHAT/WHY: QC P2-4 — site-7 was computed under pair geometry for ALL rows; for the 2 NON-PAIR sites
  (0x930030, 0x930056) the cells 0x930029/0x93004F are MID-INSTRUCTION byte positions (inside
  'mov esi,[esp+8]' @0x930027 resp. 'lea ecx,[esp+0xc]' @0x93004E), not 437F70 calls; the .txt prose
  "OR are near-adjacent to a 437F70 call" was false for them.
- FIX: 01_RAW/HELPER82B5A0_CALLER_CENSUS.csv rows 0x930030/0x930056 now carry prior_437f70_site=NOT_APPLICABLE
  and the MEASURED ECX source in context_class_note (ECX = stored origin [this+0x4C]: 0x930023 'mov ecx,[ecx+0x4c]'
  resp. 0x930053 'mov ecx,[esi+0x4c]'; src = [this+0x14]+0x5C; out = [esp+0xc] temp for the 0x930040-family site)
  (pre 2092154C0E72850EBD8A31DCB92603E7646353C6E4BFD462D2222B53029A7AA7/1065 -> new
  A847CA2C8010C84FEE60EDCD87DA5ED2C0477FC10869D5FA4DAFE02D80C1B9EF/1631);
  01_RAW/HELPER82B5A0_CALLER_CENSUS.txt prose line + the two NON-PAIR table rows reworded (pre
  DB81D5D03EF95782553C76630924E03C4F7AA77B411C59BB2ED451DCF898E3D6/3788 -> new
  A533B5364BF58E4F7AF498C1AABF6ADB6A0874FD03C25EF0CEA7F15C9A68C073/4173);
  00_CONTROL/scripts/gen_raw_evidence.py census logic + prose (file pair in AMEND-3). Measured backing:
  ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt [A.1]. The 36-site census count and 34 PAIR classifications are UNCHANGED.
- NATURE: fabricated-cell + prose correction; NO census count changed.

## AMEND-9 (2026-09-15 correction pass) — P3-1: [B.2] excerpt extended to include the cited lea anchor
- WHAT/WHY: QC P3-1 — [B.2] printed only 0x7B4650..0x7B4678 while its Evidence line cited
  'lea edi,[esi+0x5c]' @0x7B468E (outside the printed window). The claim itself is TRUE (re-measured).
- FIX: 01_RAW/SOURCE_VECTOR_LAYOUT_RAW.txt [B.2] excerpt extended to 0x7B4650..0x7B46F0 (linear decode from the
  function start; includes the lea @0x7B468E and its 3-float add/fsub uses 0x7B469E..0x7B46E5), header + inline
  AMEND NOTE (pre 12FF2C63C3F2AA33D307DEC14FBBA97DB30DFA6C757A1ABBB38F50E1620A8D84/10901 -> new
  868E9A867B2FC00B153C80DF130FDBA34E43F9C3C339D8F4C49AB62C1A6EDC1E/13905).
- NATURE: excerpt-completeness correction; NO layout claim changed.

## AMEND-10 (2026-09-15 correction pass) — P3-2: mangled K hex literal in SCIENCE_STATUS_DELTA.csv
- WHAT/WHY: QC P3-2 — the UNIT_SCALE row carried "bit-exact K=0x009999999776482582", a corrupted literal
  (decimal digits 0.009999999776482582 prefixed with 0x00). Correct: K bits = 0x3F847AE140000000 =
  (double)(float)0.01 = 0.009999999776482582 (re-measured BITMATCH in ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt [A.5]).
- FIX: 02_ANALYSIS/SCIENCE_STATUS_DELTA.csv UNIT_SCALE basis cell (pre
  D8551BB8E34E387CB8C51AAA50AC3CD3C92AE7999002EBB74A724786A16FED56/2356 -> new
  243CD870965FD60EEB13D6B32541880E8D48494E623CFDCE037DB3DD79F6F6CF/2531) with inline AMEND NOTE.
- NATURE: one-cell literal correction; NO measured value changed.

## AMEND-11 (2026-09-15 correction pass) — P3-3: [C.5] SEH frame wording
- WHAT/WHY: QC P3-3 — "[C.5] push ecx (exception registration)" mislabeled the pushed-ECX slot; it is a
  local/scratch+alignment slot (stashed with the operator-new result at 0x437FA4 'mov [esp+4],eax'); the
  exception registration node is {prev, handler 0x99C06B} at [esp+8], installed by 'lea eax,[esp+8]; mov fs:[0],eax'.
- FIX: 01_RAW/FUN_00437F70_DISASM.txt [C.5] (file pair in AMEND-3) + 00_CONTROL/scripts/gen_raw_evidence.py
  [C.5] literal (file pair in AMEND-3). Re-measured backing: ORIGIN_TRIPLE_WRITE_CENSUS_RAW.txt [A.6].
- NATURE: wording correction; NO frame-layout claim changed.

## AMEND-12 (2026-09-15 correction pass) — mechanical regeneration + verification (P1-2 closure)
- WHAT: after the content amendments above, the four generated provenance files were regenerated in ONE pass by
  the fixed gen_manifest.py (generation order: SCRIPT_SHA256.csv -> README.md -> EVIDENCE_INDEX.csv ->
  MANIFEST_SHA256.csv): 00_CONTROL/SCRIPT_SHA256.csv (pre 0F2EEB865E9F0802C96C8A4743155E3700E1C6193897BCDC43403D17BA654495/379),
  03_EVIDENCE/README.md (pre 6EFD30CE58622B39245207B16C44D7210683CC89BCDA3C808A7339C62A464BE4/1255),
  03_EVIDENCE/EVIDENCE_INDEX.csv (pre 4E0F94A9C9FBDFBBD6DE65575E968136BF59A340890D913DE204724B798B96BD/4873),
  06_REPORT/MANIFEST_SHA256.csv (pre hash-equivalent of the pre-regeneration content; see .pre copy). The .pre
  copies of all four are under 00_CONTROL/PRE_EDIT/. The NEW hashes of these four files are intentionally NOT
  embedded here (self-referential hash loop: the manifest/index hash this log); they are on disk, were re-verified
  by the post-regeneration re-hash pass (every manifest row re-hashed MATCH; every index row re-hashed MATCH and
  mutually consistent with the manifest), and are reported in the correction return to PE-MASTER.
- WHY: P1-2 requires the index row for 03_EVIDENCE/README.md to reflect the actual file; the whole package's
  provenance must be re-verified after amendments.
- NATURE: mechanical; NO science content, NO measured value, NO pin affected.

## AMEND-13 (2026-09-15 persistence pass, re-QC-authorized) — P3-R1: the AT_RUN_END_GIT_OBSERVATION.md correction-pass appendix lacked its own AMEND_LOG entry
- WHAT: the CORRECTION-PASS GIT OBSERVATION appendix appended to 01_RAW/AT_RUN_END_GIT_OBSERVATION.md during the
  correction batch (fresh-QC findings P1-1..P3-3) was the only correction-pass-amended file without a matching
  entry in this log (re-QC finding P3-R1, 06_REPORT/QC_AUDIT_R2.md Section C). The appendix itself is
  self-declaring (states the correction-pass context, HEAD, untracked census, reflog check, S0 re-verification)
  and every git claim in it was independently re-verified by the re-QC (QC_AUDIT_R2.md A.8: HEAD/status/reflog
  all MATCH).
- FILE: 01_RAW/AT_RUN_END_GIT_OBSERVATION.md — .pre copy 00_CONTROL/PRE_EDIT/01_RAW/AT_RUN_END_GIT_OBSERVATION.md.pre
  (SHA256 B575241382D8882AF426B4FF214EAC985D87851E2A352BC9E56710AB107FA1BC, 2998 bytes) -> current file
  (SHA256 A98153CA89F7DC6BF94FB58BF2806A765C54B6DDDE1A497B24201AE2D97433FC, 4968 bytes) — BOTH re-measured fresh
  at persistence by pe-master-auditor and both MATCH the re-QC's recorded pair and the current manifest rows.
- CHANGE (recorded here; already landed in the correction batch): append-only correction-pass appendix
  (self-declaring; BYTE_PREFIX=True per the re-QC — no pre-correction byte changed; no evidence value affected).
- WHY: AMEND_LOG completeness only — a log-completeness gap, not an evidence defect (the provenance chain was
  intact via the .pre copy + manifest rows; no science content, no evidence damage). Recorded late with re-QC
  authorization (QC_AUDIT_R2.md Section E offered exactly this append-only AMEND-13 alternative; PE-MASTER
  ordered it at G17).
- NATURE: correction-log completeness entry. NO prior entry rewritten; the observed file is NOT modified again
  by this entry (the recorded pair is the already-landed correction-pass change, now logged).

---

# PERSISTENCE PASS RECORD (G17; 2026-09-15; pe-master-auditor; PE-MASTER-ordered path-limited publication)

This section records every G17 persistence-pass change to this package for log completeness (the P3-R1 lesson:
every package change is logged). Append-only; no prior entry above is rewritten. Governance/packaging only —
NO science content, NO measured value, NO pin affected. No .pre copies were created FOR THIS PASS (creating new
ones would overwrite the correction-pass snapshots under 00_CONTROL/PRE_EDIT/, which are load-bearing evidence);
pre-persistence verification was performed against outside-tree snapshots plus post-edit byte diffs, and the
single path-limited commit is the durable record.

- 00_CONTROL/AMEND_LOG_R1.md: AMEND-13 appended (above) + this record section.
- 06_REPORT/STAGE_ACCEPTANCE_GATES.csv: rows G15/G16/G17 flipped PENDING -> PASS with their executed basis
  (G15 fresh QC + correction + targeted re-QC chain; G16 PE-MASTER MASTER_ACCEPTED advisory adjudication;
  G17 the path-limited commit+push mechanism). Rows G0-G14 byte-identical (verified against the outside-tree
  pre-persistence snapshot; only the 3 governance rows changed).
- 06_REPORT/PE_MASTER_REVIEW.md: CREATED — PE-MASTER's G16 verdict persisted VERBATIM on PE-MASTER's direct
  order (byte-identity re-verified before commit).
- 06_REPORT/QC_AUDIT_R2.md (created by the targeted re-QC after the last manifest regeneration, until now
  outside manifest coverage) and 06_REPORT/PE_MASTER_REVIEW.md are ADDED to the regenerated manifest/index
  coverage so ALL package files are covered (QC_AUDIT.md was already covered).
- 00_CONTROL/SCRIPT_SHA256.csv + 03_EVIDENCE/README.md + 03_EVIDENCE/EVIDENCE_INDEX.csv +
  06_REPORT/MANIFEST_SHA256.csv: regenerated in ONE pass by gen_manifest.py (UNCHANGED script; AMEND-12
  generation order; L12 self-exclusion respected — the manifest carries no row for itself; the index carries
  no row for itself or the manifest). SCRIPT_SHA256.csv verified BYTE-IDENTICAL (no script changed). The new
  hashes of these generated files are intentionally NOT embedded here (the AMEND-12 self-reference rule: the
  manifest/index hash this log); they are on disk and reported in the G17 persistence return.
- AUDIT_ENTRYPOINT.md (repo root, OUTSIDE this package): exactly ONE new topmost LATEST RUNS row appended
  (this run); no existing row rewritten (ENTRYPOINT_ROW_SURVIVAL verified: all prior rows intact).
- NOT modified by this pass: 01_RAW/*, 02_ANALYSIS/*, 00_CONTROL/RUN_CONTRACT.md, 00_CONTROL/SOURCE_IDENTITIES.json,
  00_CONTROL/scripts/*, 00_CONTROL/PRE_EDIT/*, 06_REPORT/REPORT.md, 06_REPORT/HANDOFF.md, 06_REPORT/QC_AUDIT.md
  (frozen QC records). The post-push verification record (HEAD == origin/master == ls-remote + the commit SHA)
  lives in the AUDIT_ENTRYPOINT row's discovery command + the G17 persistence return, per the one-commit
  discipline (a package file cannot embed its own commit SHA).
