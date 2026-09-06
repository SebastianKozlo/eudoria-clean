# QC1_CORRECTION_LOG — RUN C PE_NIF_MORPH_WIDERECORD_R1_20260906_170000 (documentation-only correction)

- CORRECTION RUN: 2026-09-06, correction class REPORT_AMENDMENT + MANIFEST_REFRESH. NO re-execution of any driver; NO generator touched; NO raw evidence touched.
- Basis: 00_CONTROL/INTERNAL_QC_R1.md (QC_VERDICT = QC_FAIL; discrepancies D1-D4 P1 disclosures, D5-D6 P2 label conventions). The numbers of RUN C are unchanged in every artifact; every quantitative claim remains the QC-verified original.
- Untouched-proof: the manifest re-validation below re-hashed ALL 22 ordinary rows including the driver 00_CONTROL/widerecord_driver_r1.py (sha256 b4fa818a7f7b42de565eb73837b1c10e368f021c3ab54f54146eb84cb499a714) and the raw evidence (01_RAW/WIDE_SPAN_OUTCOMES.jsonl bf1afbd2..., 01_RAW/WIDE_NC_TRIALS.jsonl ed4ae539..., 01_RAW/NEGATIVE_FIXTURES_GEXEC.json 7ceb64e8..., 01_RAW/MANIFEST_NEGATIVE_TESTS.json edddfeac..., 01_RAW/SELF_AUDIT.txt 6ae4dacc...) — all physical hashes equal the run-manifest pins; zero bytes of driver or raw evidence were modified.
- Standing sentence: no semantic claims; the +65 H5a/H5c2 status = RETROSPECTIVE_VALIDATED (RUN A); the H7 join-mechanism = UNVALIDATED (RUN A) - this run makes NO H7-based claims; the residual-325 population is OUT OF SCOPE (stays mechanism-unexplained; a diagnostic note only, no new claims). Result classes: BYTE_MATCH / REPEATABILITY / RETROSPECTIVE_VALIDATION / RUNTIME_SEMANTICS (= explicitly NOT_TESTED here, out of scope).

## 1. Pre-edit backup of the report

- 00_CONTROL/PRE_EDIT_QC1/00_FINAL_REPORT.md.pre — byte-exact copy of 06_REPORT/00_FINAL_REPORT.md made BEFORE the amendment; sha256 82f5ee8ec763937f93fc0f3362b908c6b34215d7cd9e625ed632ab247534b617 (equals the original manifest row; copy verified byte-identical to the source at copy time).
- RUN A PRE_EDIT precedent.

## 2. Report amendment (06_REPORT/00_FINAL_REPORT.md)

- One section APPENDED at the end. The original 82 lines are preserved byte-identical: the .pre file is a byte-prefix of the amended file (verified), and Compare-Object shows only the appended section.
- Appended section title (exact): "## QC1 AMENDMENT (2026-09-06 — disclosures added per INTERNAL_QC_R1 findings D1-D6; the numbers unchanged — QC-verified independently)"
- Four disclosures appended, verbatim as specified by the correction order (each a labeled prose paragraph inside that section):
  1. PRIOR EXECUTION ATTEMPT (D1): first execution attempt HARD-STOPPED in-driver on a 63-character transcription error of the RUN A driver pin constant inside this run's own driver; the constant was fixed, the stale partial evidence (an overwritten 06_REPORT draft from that attempt, the 19-vs-18 manifest-row discrepancy at pre-validation time) was removed, and a clean full re-run produced every artifact reported here; the pin itself always matched the physical file; no K2/RUN A input was ever mis-read.
  2. ZERO-HIT NC STRUCTURAL CAVEAT (D2): the W1/W3 negative controls recorded 0 hits (NC 0/538 full; 0/314 held-out; denominators > 0, so not the vacuous case); the fixed 132-byte stride of the W1 unit layout makes the u+/-2 wrong-start NC partly STRUCTURALLY trivial for this grammar family; the separation (full rate 0.0446 vs the NC CI upper bound 0.0068 = 6.5x) is an upper-bound-based bound, not a behaviorally-strong separation; a stronger NC (stride-aligned wrong-block starts) remains future work.
  3. FAMILY CONCENTRATION (D3): 12 of the 13 consumed spans lie in ONE file and block (548296.nif block 75 — 12 of that block's 15 population spans); the 13th (548808.nif block 164 si=129) arrives via the W3 window at offset +4; the wide-record class is CONFIRMED at the record level in this one block, CROSS-FILE generality NOT established by this run.
  4. SIDE A = 0 FITS (D4): all 13 fits are on split side B (side B 13/157); side A recorded 0 fits (0/108, exact binomial CI [0.0, 0.0336]); the frozen G-WIDE conjunction gated the held-out side and the full population and passed as written; the side asymmetry is disclosed as a homogeneity caveat of the +13 claim.
- Amended report sha256: ae1b8a818ac48cf2eb14e8051ccdc7987f73f4ae181c0d2f8deca5da366657cb

## 3. Artifact class notes (01_RAW/ARTIFACT_CLASS_NOTES.md — NEW file)

- Content: the D5/D6 standing note — WIDE_NC_TRIALS.jsonl rows are per-record NEGATIVE-CONTROL evidence (result-class: BYTE_MATCH-class trials; they carry hit/reason/denominator fields and no corpus result_class by design — the note supplies the standing sentence for the file); NEGATIVE_FIXTURES_GEXEC.json is a TOOLING artifact (the G-EXEC gate's eight synthetic fixtures) whose result_class value "G-EXEC" denotes tooling, not one of the four corpus result classes; the aux control files in 01_RAW share this tooling status.
- sha256: eaf0753d004d13f66662533bd8346e3f153c3c965a8396332003a6ba56b39d67

## 4. Manifest refresh + re-validation

- artifact_index.csv refresh: ordinary row "01_RAW/ARTIFACT_CLASS_NOTES.md,package artifact,eaf0753d004d13f66662533bd8346e3f153c3c965a8396332003a6ba56b39d67" added (sorted position in the 01_RAW block); the 06_REPORT/00_FINAL_REPORT.md row hash replaced 82f5ee8ec763937f93fc0f3362b908c6b34215d7cd9e625ed632ab247534b617 -> ae1b8a818ac48cf2eb14e8051ccdc7987f73f4ae181c0d2f8deca5da366657cb. No other rows touched.
- New manifest sha256: 95b3ce98259b68eb465036a30de0b4d68dfe08a9986de57e067c40b09834505f
- Re-validation (independent standard-CSV validator, Python csv module, NOT the run driver; script C:\Users\User\AppData\Local\Temp\opencode\qc1_manifest_revalidation.py): 22/22 ordinary rows OK (exactly 3 fields; 64-hex sha; relative forward-slash path with no drive/absolute/.. shapes; file exists; physical hash equals the row; 0 duplicates); 12/12 external rows OK (kind=external_source; era PCG_9_3_5; 64-hex; physical path exists; physical hash equals). gate_pass = true; findings = [].
- Negative tests a-f re-executed on this validator: 6/6 fail the gate as required (a MALFORMED_MANIFEST_ROW, b MALFORMED_MANIFEST_ROW, c MISSING_FILE, d MALFORMED_HASH, e UNSUPPORTED_PATH_SHAPE, f HASH_MISMATCH + DUPLICATE_ROW); all_six_fail_the_gate = true.
- Coverage census at validation time: 26 files on disk = 22 manifested ordinary + 4 documented non-manifested (artifact_index.csv self-hash impossible; 05_ANALYSIS/MANIFEST_VALIDATION.json circular; 00_CONTROL/INTERNAL_QC_R1.md the QC's own record file; 00_CONTROL/PRE_EDIT_QC1/00_FINAL_REPORT.md.pre this backup). This log (written after that snapshot) brings the package to 27 files on disk and is likewise a documented non-manifested control-plane file.
- Dated additional entry recorded in 05_ANALYSIS/MANIFEST_VALIDATION.json: key "qc1_correction_revalidation_20260906" (gate_pass true; ordinary_rows 22; external_rows 12; findings []; negative tests rerun 6/6; census; manifest_sha256_at_this_validation 95b3ce98...; manifest_gate_verdict_after_qc1 PASS). 05_ANALYSIS/MANIFEST_VALIDATION.json sha256 after the entry: 102fe80bb8bddb1b0f63256dafb8190d11883ae50b78d5e41b029c3f944f3584 (excluded from the manifest as circular, documented).

## 5. D1-D6 resolution map

- D1 resolved: disclosure (1) appended in the QC1 AMENDMENT section — the prior execution attempt (pin-constant typo, stale overwritten 06_REPORT draft, clean re-run) is now disclosed in the report; the .pre backup preserves the pre-amendment report for provenance.
- D2 resolved: disclosure (2) appended — the 0-hit NC structural caveat (partly trivial separation for W1/W3) is now stated.
- D3 resolved: disclosure (3) appended — the 12-of-13 one-file-one-block family concentration and the missing cross-file generality are now stated.
- D4 resolved: disclosure (4) appended — the side A 0-fits asymmetry (0/108, CI [0.0, 0.0336]) is now stated.
- D5 resolved: 01_RAW/ARTIFACT_CLASS_NOTES.md supplies the standing sentence for WIDE_NC_TRIALS.jsonl and documents its per-record NEGATIVE-CONTROL result-class convention (BYTE_MATCH-class trials, no corpus result_class by design).
- D6 resolved: the same notes file documents NEGATIVE_FIXTURES_GEXEC.json "G-EXEC" as a tooling class (not one of the four corpus result classes) and the shared tooling status of the aux control files in 01_RAW.
- No QC finding required a re-run; no gate was waived; no raw evidence or driver byte was modified; RUN_STATUS remains COMPLETED with the corrected, disclosure-complete report.
