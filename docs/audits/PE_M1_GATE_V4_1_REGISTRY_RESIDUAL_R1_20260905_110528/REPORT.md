# 00_FINAL_REPORT — PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528

- RUN_ID: PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528
- EXECUTOR: pe-reconstruction (bounded residual fix; offline; INTERVENTION_LEDGER = EMPTY)
- MANDATE: the PE-MASTER post-audit of the V4 correction (verdict MASTER_PARTIAL_PASS,
  commit 58ab627) - the ORDERED_WORK items 2-4: (W1) compose the registry fields for BOTH
  entries (P-RNG-DIV, P-POS-SCALE) per the byte-locks, in the V4 md AND json, then rebuild
  the manifest echo (built_from SHAs updated); (W2) the EXTENDED semantic gate (the
  full-document walk + the NEW forbidden phrases + the NEW negative fixture N6) re-executed
  in full; (W3) the consistency check re-run with a payload scan over 100% of the FINAL
  commit set; (W4) the bounded commit+push; (W5) M1_PARTIAL + M2_HARD_STOP unchanged.
- PROMPT SHA256: 909256DED9CCEE615B31679FA2DE9570BC9F512B898327E84E6D28431A28828F (computed
  by the launcher BEFORE any work; MATCH).
- BASE_SHA recorded FIRST: 58ab627 (== the expected 58ab627; git log verified at run start;
  the worktree was CLEAN - zero PREEXISTING_UNCOMMITTED_WORK).

## 0. THE ONE P0 QUESTION - ANSWERED

Czy residualny stale-carrier w rejestrze V4 da się usunąć z warstwy LIVE wyłącznie
kompozycją z istniejących zapisów - tak, żeby rozszerzona bramka semantyczna przeszła
fail-closed? **TAK - WYKONANE:** both registry entries composed from the existing records
(the iter035 byte locks + the historical open-item record), the extended gate passes the
clean edited V4.1 (0 hits / 0 problems in the FULL-document walk) and FAILS all six negative
fixtures N1-N6 (N6 = the OLD missing/why restored - caught in every scanned document),
and the final 100%-of-commit-set payload scan is clean. ZERO new forensics, ZERO runtime,
ZERO frozen-file edits.

## 1. PRE_RUN_LOCKS (fail-closed; 01_RAW\pre_run_locks_verification.json)

- 24/24 pins re-hashed MATCH: the launcher NEXT_PROMPT (1) + the 5 CURRENT-LIVE editable
  pins SHA-locked BEFORE the edit (V4 md 5B90D2C4... / V4 json 11FB16B0... / manifest
  A1E0F5B9... / GATE_INDEX pre-append FD68060A... / AMENDMENTS pre-append C8FF0ABE...) +
  the FULL frozen list (the R2 mandate's 18-pin list, exact 64-hex values from the R2
  NEXT_PROMPT section 2, incl. the old EVIDENCE_MANIFEST.json 0E6FCE50... and the
  identity-only Entropia.exe E7785430...).
- Verdict: PRE_RUN_LOCKS_ALL_MATCH (match=24, mismatch=0, missing=0).

## 2. W1 - THE REGISTRY COMPOSITION (per the byte-locks; both formats + the manifest echo)

- THE RESIDUAL (the post-audit's F-1): the LIVE missing/why of P-RNG-DIV/P-POS-SCALE carried
  the verbatim-inherited pre-iter035 hypothesis "reads 0.0 statically (runtime-initialized)"
  - factually false vs the byte-locked operands (0x00A7D7A8 = 32767.0 f64, bytes
  00 00 00 00 C0 FF DF 40; 0x00A8C758 = 65535.0 f64, bytes 00 00 00 00 E0 FF EF 40 - iter035,
  CONSTANT_ADDRESS_LOCK, re-read by PE-MASTER at the R2 post-audit) and internally
  contradictory with the entries' own SUPERSEDED-LOCKED v4_status.
- THE COMPOSITION (each field labeled "composed in V4.1"; the sources = the byte-locks +
  the historical open-item record, kept as TYPED historical context, NOT live status):
  - missing (P-RNG-DIV): "composed in V4.1: NONE for the divisor (byte-locked 32767.0 f64
    @0x00A7D7A8, iter035; the historical open-item record follows)";
  - missing (P-POS-SCALE): "composed in V4.1: NONE for the divisor (byte-locked 65535.0 f64
    @0x00A8C758, iter035; the historical open-item record follows)";
  - why (both): the TYPED SUPERSESSION record carrying the mandated disproof statement
    verbatim ("composed in V4.1: the pre-iter035 hypothesis 'reads 0.0 statically
    (runtime-initialized)' was DISPROVEN by the byte lock - the slot is file-backed .rdata
    (bytes 00 00 00 00 C0 FF DF 40 [32767.0 f64]; 65535.0: 00 00 00 00 E0 FF EF 40)") +
    the supersedes pointer (the retired why) + the sources (the iter035 byte locks +
    the PE-MASTER R2 post-audit re-read). WHY TYPED: the mandated statement quotes the
    retired hypothesis verbatim - a phrase the V4.1 gate permits ONLY in typed
    retraction/supersession records (W2(b)); the why field therefore IS that typed record.
  - resume_path (both): "composed in V4.1: NONE for the divisor; runtime tracing remains
    relevant only to the actual-CW question";
  - the historical open-item record (the OLD missing/why/resume, verbatim): kept as the
    TYPED RETRACTION record inside each entry ("the historical open-item record follows").
- THE MD LAYER: the two registry lines re-rendered with the composed fields WITHOUT the
  retired wording (the R2-established architecture: retired wordings live ONLY in typed JSON
  records; the live MD layer stays clean) + the explicit typed-record pointers.
- BOUNDED DIFF (proven): the JSON - the other 17 entries + every other top-level key
  verified IDENTICAL; the MD - exactly 2 lines differ, the line count unchanged;
  the manifest - the echo rebuilt FROM the V4.1 fields (mechanically re-derived from the
  edited matrix) + the built_from SHAs updated; every other manifest key verified IDENTICAL.
- NEW SHAs: V4 json 003056AC0210A7E0C33F304232F2F366D45D4E94B04D9984FA03B62D06CB4A95 /
  V4 md EC04FC471C55450DF060E5E3441A92584BB0CB7C4C63ED1E223C20F0BE732552 /
  EVIDENCE_MANIFEST_V4.json 9944925D1489771B9D5EA99A8AF834E363FBFF9BC49D73BB0999DC8706217D90.
- Records: 01_RAW\composition_record_v4_1.json + 01_RAW\manifest_rebuild_record_v4_1.json.

## 3. W2 - THE EXTENDED SEMANTIC GATE (01_RAW\semantic_gate_report_v4_1.json)

- (a) FULL-DOCUMENT WALK: ALL top-level keys of the V4.1 JSON (incl. consolidation_basis,
  supersession, this_run_evidence, honest_limits_binding, charter_five_labels,
  nine_fields_per_row, taxonomy) + the full manifest walk + the full MD text; the
  typed-exempt rule UNCHANGED (records explicitly typed as retraction/supersession are the
  ONLY permitted carriers).
- (b) NEW forbidden phrases in live fields: "reads 0.0 statically" + "missing: the exact
  RNG normalization divisor" + "missing: the u16->world position divisor" (+ the R2's seven,
  all case-insensitive) + the NEW MD-parity rule (each live registry missing/why also
  scanned as its MD rendering - the rendered form IS the phrase).
- (c)+(d) RE-EXECUTION OF THE WHOLE GATE:
  - clean edited V4.1: **PASS (0 hits / 0 problems)**;
  - N1 (the V3 carried fields for rows 8/10/11): **FAIL** (4 hits: u16/k, rand*2.0,
    32768.0 divisor, divisor candidate);
  - N2 (one section-13 field removed): **FAIL** (1 problem);
  - N3 (the stale era_statement fixture): **FAIL** (3 hits);
  - N4 (a required phrase removed): **FAIL** (1 problem);
  - N5 (the clean copy): **PASS**;
  - N6 (NEW - the OLD missing/why restored, the FULL pre-V4.1 registry state across the
    matrix + the manifest echo + the MD lines): **FAIL** (16 hits + 28 problems - hits in
    EVERY scanned document: the matrix live fields, the MD-parity renderings, the MD text,
    the manifest echo; plus the structural absence of the V4.1 composition).
- Verdict: **PASS** (fail-closed proven: clean PASS + N1-N6 ALL FAIL).
- Required phrases: the R2 rules unchanged + the V4.1 composition requirements (the label,
  NONE-for-the-divisor, the byte-locked constant + address, the typed SUPERSESSION why with
  the disproof statement + both byte patterns, the typed RETRACTION historical record with
  the exact old triple, the actual-CW resume).

## 4. W3 - THE CONSISTENCY CHECK (01_RAW\consistency_report_v4_1.json + payload_scan_final_v4_1.json)

- Pass 1 (the content checks): 35/35 PASS - the 18 frozen pins UNCHANGED (incl. Entropia.exe
  identity + the frozen CSV + the repair evidence); the R2/R1 completed-run dirs preserved
  (read-only); the .pre copies == the pre-append pins AND byte-prefixes of the appended
  files (append-only proven); the V4.1 structure verified independently (19x9 non-vacuous
  in both formats; the five section-13 labels; BOTH entries composed + labeled + typed);
  72/72 cited evidence SHAs re-hashed MATCH from the physical files (+ 1 honest null-SHA
  disposition, ROW_19/iter034 - the noted frozen-matrix pointer); 5/5 local-only originals
  identity re-hash MATCH; the counter split consistent (443,141 + 20,000 = 463,141);
  the manifest echo == the V4.1 matrix registry (mechanical equality); the built_from SHAs
  == the actual files; the PC24 record consistent with the R2 raw artifact (SHA-pinned,
  103,073/1,245,184 CONFIRMED - triple-confirmed per the post-audit); the GATE_INDEX
  append SHA records == the actual files; the semantic gate report SHA agreement.
- The FINAL 100%-of-commit-set payload scan (01_RAW\payload_scan_final_v4_1.json): every
  file of the FINAL commit set byte-scanned (the 5 gate-package repo files + the ENTIRE
  mirror tree + the run-local originals; identity metadata only, zero proprietary payloads);
  the self-referential exclusions documented (the scan report itself + the artifact_index's
  own row set - the established a-file-cannot-hash/scan-itself convention).

## 5. W4 - THE APPEND-ONLY MARKS + THE COMMIT

- GATE_INDEX.md + GATES\AMENDMENTS.md: the V4.1 record appended (byte-extension; the .pre
  prefix proofs FD68060A.../C8FF0ABE... verified; the new SHAs recorded inside the append:
  3532F6B71A0A2853D07E3603B9712B7BC8BBD9A320022C959B033A3A23B9C5B6 /
  B4EF3610D289675375CA517013884F67624273D396C31DDDB1F1C377283F0717).
- COMMIT SCOPE (exactly as granted): ONLY docs\audits\PE_MILESTONE_1_WORLD_SURFACE_R1_GATE\**
  (the edited V4 md/json + the rebuilt EVIDENCE_MANIFEST_V4.json + the appended
  GATE_INDEX/AMENDMENTS - exactly 5 modified files, no others) +
  docs\audits\PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528\** (the mirror).
  AUDIT_ENTRYPOINT.md OUT of scope (never staged). git status at run start: CLEAN.
- The repo mirror: 00_CONTROL (the run's control scripts) + 01_RAW (the raw outputs incl.
  the .pre proofs) + REPORT.md + HANDOFF.md + STAGE_ACCEPTANCE_GATES.csv + artifact_index.csv.

## 6. W5 - FINAL STATUS UNCHANGED

M1 remains PARTIAL / HARD_STOPPED_AT_GATE; M2 remains HARD-STOPPED. This run closes NOTHING
except its own residual. The package now awaits the PE-MASTER re-audit; only after its
ACCEPTED verdict does the package return to the external auditor (the human's relay
decision alone).

## FINAL HANDOFF BLOCK

```text
AUDIT_OUTPUT_ROOT      = D:\Eudoria_Reconstruction\99_Audits\PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528
FINAL_REPORT_PATH      = D:\Eudoria_Reconstruction\99_Audits\PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528\06_REPORT\00_FINAL_REPORT.md
PRIMARY_EVIDENCE_PATHS = 01_RAW\semantic_gate_report_v4_1.json + 01_RAW\consistency_report_v4_1.json
                          + 01_RAW\payload_scan_final_v4_1.json + 01_RAW\pre_run_locks_verification.json
                          + 01_RAW\GATE_INDEX.md.pre + 01_RAW\AMENDMENTS.md.pre
                          + 01_RAW\composition_record_v4_1.json + 01_RAW\manifest_rebuild_record_v4_1.json
                          + the repo V4 md/json (new SHAs 003056AC0210... / EC04FC471C55...)
                          + EVIDENCE_MANIFEST_V4.json (new SHA 9944925D1489...)
BASE_SHA / HEAD_SHA    = 58ab627 / recorded RUN-LOCALLY after the push
                          (a commit cannot embed its own hash - see 99_Audits\PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528\06_REPORT\00_FINAL_REPORT.md)
PUSH_STATUS            = recorded RUN-LOCALLY after the push
RUN_STATUS             = V4_1_REGISTRY_RESIDUAL_COMPLETE
HARD_STOP_REASON       = NONE
INTERVENTION_LEDGER    = EMPTY (run offline)
```

5-LINE SUMMARY:
1. The P0 answered YES-EXECUTED: the residual stale carrier (the registry missing/why of
   P-RNG-DIV/P-POS-SCALE carrying the disproven "reads 0.0 statically" verbatim) removed
   from the LIVE layer by pure composition from the existing records - the byte-locked
   missing, the typed-SUPERSESSION why (the mandated disproof statement verbatim, the only
   permitted carrier), the actual-CW-bounded resume, and the historical open-item record
   kept as the typed RETRACTION context.
2. The extended semantic gate (full-document walk + the 3 new forbidden phrases + the
   MD-parity rule + N6) passes the clean edited V4.1 (0 hits / 0 problems) and FAILS all
   six fixtures N1-N6 - N6 (the old missing/why restored) caught in every scanned document.
3. The manifest rebuilt FROM the V4.1 fields (the echo mechanically re-derived; the
   built_from SHAs updated); the append-only marks byte-prefix-proven; the 18 frozen pins +
   the R2/R1 run dirs untouched; the bounded diffs proven (17 entries + all other keys
   identical; exactly 2 MD lines).
4. The consistency check 35/35 PASS (72/72 cited SHAs re-hashed + 1 honest null-SHA
   disposition; 5/5 local-only originals; the counter split + PC24 records consistent);
   the FINAL payload scan = 100% of the commit set, zero proprietary payloads.
5. M1_PARTIAL + M2_HARD_STOP unchanged; the package awaits the PE-MASTER re-audit, then
   the external re-judgment (the human's relay decision).
