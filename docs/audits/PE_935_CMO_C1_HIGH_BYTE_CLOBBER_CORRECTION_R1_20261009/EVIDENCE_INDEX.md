# EVIDENCE_INDEX — PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009

Index of every evidence file of this package with its role. All sizes/SHA256
measured from disk (frozen executor/QC evidence re-hashed by this persistence
phase before the manifest generation; lowercase hex). Repository-relative
paths are rooted at the repository root (BASE `34fc347…`).

## 1. Frozen executor-phase evidence (13 files)

| Path (under `docs/audits/PE_935_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009/`) | Size | SHA256 | Role |
|---|---|---|---|
| `PREREGISTRATION.md` | 19994 | `a0c9fbe9a1ea7ca40b91019664110b1d6f394c6de87147fabefe3b35514d94c0` | Pre-registered correction plan: defect hypothesis with exact source locations, PRE design (AST extraction; verbatim scan transcription; falsifiers F-PRE-1..7 + W1 byte-identity gate), POST control list C1–C6 + AUX-1 with falsifiers, scope boundaries, acceptance gates. Written BEFORE the correction. |
| `INPUT_IDENTITIES.md` | 6771 | `7b2ea846a3915319d8474dee1e31f6a989d61dff8d56497fbdae8583af11f9af` | Fail-closed preflight census: contract identity, repo triple-verification, EXE identity, the 4 mandatory source pins, contextual input identities, historical key evidence values, executed-by list. |
| `ROOT_CAUSE.md` | 9205 | `4a11368b6dac412cc59fd8ae7775da232187f74ddc3b3bd854c78aa4ede4371d` | The defect in one sentence + exact code locations (executor lines 174-175; QC no-op conditional lines 214-215 + missing source parent), the downstream consumer, PRE-measured reproduction table, the PRE-measured historical 8×8 census (blast radius), why the historical run did not catch it, the fix, non-goals. |
| `00_PRE/PRE_COUNTEREXAMPLES.json` | 80885 | `e15225820baefd96a75f06ceeb8c93f1cb03cf64d12c8832f6aa31d3b0d91b64` | The PRE false-pass reproductions (immutable): all six cases (EX/QC × clean/CH/CL) with raw decode records at the mutation site, wrong writes/reads sets, false empty ECX scans, the historical 8×8 census (64 cases × 2 decoders with per-row records), AST-extraction provenance, verbatim-scan transcription verification, input identities, falsifier adjudication. |
| `00_PRE/PRE_SHA256_INDEX.csv` | 1737 | `5d8b96631e2ce87237dad6cd9e941340bc24a0ac380a3d11c1fd26c5659e96bf` | PRE evidence + executed-input provenance index (8 rows incl. the two external inputs: EXE + contract). |
| `03_SCRIPTS/corrected_executor_decoder.py` | 20675 | `c9b553aa90d449871643d27c76f96bcfeb989abdf20b0badd1f8530868fcd2c5` | The CORRECTED EXECUTOR DECODER — successor of the historical `repin_write_provenance.py` decoder (OLD 34043 B / `45120C91AD6A94A79C56E9B06F1C035481FB99D3017688E7F589732BEC6EE931` → NEW, mapping recorded here and in INPUT_IDENTITIES.md): byte-alias parent map for all eight aliases (destination + source, register + memory forms), width/bit-range fields, partial-write distinction, same-lineage successor scan + provenance gate with NO hard-coded mutant expectation. |
| `03_SCRIPTS/run_pre_counterexamples.py` | 38752 | `fa0a5320a165e3e5d7580964f6bb92ad578d04f03d6a52861886a3c1f6c5e684` | PRE runner: AST extraction of both historical decoders, verbatim scan transcription + source-line verification, in-memory mutants, the historical 8×8 census, PRE_COUNTEREXAMPLES.json + PRE_SHA256_INDEX.csv generation (python -B; no residue). |
| `03_SCRIPTS/run_alias_controls.py` | 57096 | `207333f3f1dea39c33707e1d222bf6f65c94b8326b26a2da0a0367029d497be5` | POST runner: C1–C6 + AUX-1 through the corrected executor decoder, the independent REF_BYTE8 reference table (no production helper import), gate decomposition per check, POST_COUNTEREXAMPLES.json + POST_SHA256_INDEX.csv + CONTROL_MATRIX.csv + REGRESSION_RESULTS.json generation. |
| `00_POST/POST_COUNTEREXAMPLES.json` | 151703 | `85b363fad01d259582094537a6c2342edfe6578119b7f5e8095a56be980aa7d8` | The corrected controls: C1–C6 + AUX-1 raw records (expected vs measured, per-check gate decomposition), the 64-case executor alias matrix, the OLD→NEW script mappings, exe_identity_post (unchanged), source_package_unchanged (all true), disclosed repairs, residue scan. |
| `00_POST/POST_SHA256_INDEX.csv` | 2232 | `c8856e3ec52730a6428e74f13abade6d193c560f4a89224b400b6af21687b7c2` | POST evidence + executed-input provenance index (11 rows incl. the two external inputs). |
| `CONTROL_MATRIX.csv` | 2991 | `429f6c629fa5f9908abc90f9c44608cb4db1d9a1c0e1bfcdbe93a8eb4299dbfc` | The C1–C6 + C5.1–C5.4 + AUX-1 case matrix: per-control expected vs measured + verdict (executor phase). |
| `REGRESSION_RESULTS.json` | 3963 | `5ea88bc06b7639493eec6eb7158bef43b790b489af0de1cad6332146120f7032` | C6 historical scientific regression: store/caller/accessor/RTTI records, clean decode (64 insns, end exact 0x0085B290), committed-table anchor, historical field equality, receiver + value chains with the provenance gate PASS, J3 statuses carried verbatim, CORE_RECEIVER_VALUE_CHAIN = PRESERVED_CONFIRMED_STATIC_CONDITIONAL, c6_verdict = PASS. |
| `SUPERSESSION_AND_STANDING.md` | 6848 | `0ab2cdece09cb2ff1419c48e9a1169832a0a061c618a7f94f290089c75f49921` | Documentary supersessions per contract §8: CMO-C1/P2 recorded; DOC-1/P3 + DOC-2/P3 backlog; J3 standing preserved verbatim (source: J3 SUPERSESSION.md 8339 B / `DD11137A…`, identity re-verified); scope confirmation (all zeros); phase boundaries of the record. |

## 2. Frozen QC-phase evidence (4 files)

| Path | Size | SHA256 | Role |
|---|---|---|---|
| `03_SCRIPTS/corrected_qc_decoder.py` | 23454 | `88460076843bda7dfd51bc1182422e1f98ff13eec493f14304bacc92fa7b0919` | The QC worker's OWN independent corrected QC decoder — successor of the historical `qc_remeasure.py` decoder (OLD 31970 B / `4E5426AEAB8FBD9A9364A5FE445ED2EA7C5D9F4B3E2F2E71B3EB5B3F3F8DDE1A` → NEW, mapping recorded): NO production helper import; parent attribution implemented arithmetically from the x86-32 encoding; fail-closed QcDecodeError. |
| `03_SCRIPTS/qc_run_controls.py` | 103975 | `fd84efcb727f53c1562f6ee0715c46f24209d807563c3378b7e9e86417108b75` | QC runner (duties A–J): own AST extraction, own mutants, own reference table (QC_REF_BYTE8 explicit literal), own RTTI walk, own provenance gate (same predicate semantics, no hard-coded mutant expectation), executor-claims verification, supersession token scan (scanner-self exclusion recorded), QC_RESULTS.json generation (python -B). |
| `QC_RESULTS.json` | 188859 | `e1ab3ac87ea995ad874b3b293729a93515cd8044ad49ca7e538b2a71546940c4` | The machine-readable QC record: duties A–J with per-duty measurements (PRE parity field-by-field; corrected clean/CH/CL; the QC's own 64-case matrix → the 128/128 total; 6/6 negatives; regression; AUX; SHA-index verification PRE 8/8 + POST 11/11; supersession scan zero forbidden active standing; J3 verbatim 5/5), acceptance_gates_qc 11/11 true, QC_VERDICT = QC_PASS, pass_records_methodology (MEASURED_QUANTITY / INDEPENDENT_SOURCE_OF_TRUTH / WHY_NON_CIRCULAR / FAILURE_CASE_DETECTED per meaningful PASS), repair_rounds_log (5 own-tooling bring-up steps with intermediate states), QC origin statement. |
| `QC_REPORT.md` | 18833 | `9d88d448bcaf5abd1dee4678e1f806d5a63601ca9e02a715d257ef3bbac28f77` | The QC narrative report: method (independence construction), per-duty results, verdict QC_PASS with the 11-gate table, the repair-rounds disclosure for PE-MASTER adjudication, coverage/NOT_CHECKED (incl. the non-contract 8A branch: implemented, not exercised — no such byte in the window), open findings (none material). |

## 3. Persistence/publication phase (this phase; 5 files)

| Path | Size | SHA256 | Role |
|---|---|---|---|
| `PE_MASTER_REVIEW.md` | 5983 | `81a39a1911aa5c7a4f0f4a895c21c80a8929117acfb8308b23256fef1e205ba9` | PE-MASTER MASTER_AUDIT persisted VERBATIM (advisory; MASTER_ACCEPTED; ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT = NONE; CORRECTION_VERDICT = PASS; own execution counter-checks; the QC repair-rounds adjudication; standing preserved; HARD_STOP = YES). |
| `FINAL_REPORT.md` | measured in MANIFEST_SHA256.csv | measured in MANIFEST_SHA256.csv | The final report: run/contract identity, preflight, root cause (both facets), PRE reproduction + census, OLD→NEW mappings, POST C1–C6 + AUX-1 expected-vs-measured, 128/128 completion, regression, QC + process disclosures + adjudication, supersessions, J3 verbatim, scope zeros, terminal governance. |
| `EVIDENCE_INDEX.md` | (this file) | (self; see manifest) | This index. |
| `HANDOFF.md` | measured in MANIFEST_SHA256.csv | measured in MANIFEST_SHA256.csv | The contract §13 terminal handoff fields with the ACTUAL measured values. |
| `MANIFEST_SHA256.csv` | (self-excluded) | (self-excluded) | The final persistence manifest, generated LAST: every physical file under this package except itself, PLUS the updated AUDIT_ENTRYPOINT.md; repo-relative; bijection self-check (a manifest cannot contain its own SHA256). |

## 4. Source inputs (READ_ONLY; at BASE 34fc347…; identity-verified)

| Path (repo-relative) | Size | SHA256 | Role in this run |
|---|---|---|---|
| `docs/audits/PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009/03_SCRIPTS/repin_write_provenance.py` | 34043 | `45120c91ad6a94a79c56e9b06f1c035481fb99d3017688e7f589732bec6ee931` | Mandatory source input: the historical executor decoder (AST-extracted for PRE; superseded by `corrected_executor_decoder.py`). |
| `docs/audits/PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009/03_SCRIPTS/qc_remeasure.py` | 31970 | `4e5426aeab8fbd9a9364a5fe445ed2ea7c5d9f4b3e2f2e71b3eb5b3f3f8dde1a` | Mandatory source input: the historical QC decoder (AST-extracted for PRE; superseded by `corrected_qc_decoder.py`). |
| `docs/audits/PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009/CONTROL_RESULTS.json` | 18509 | `9545d0d78881c29bc805ea3a05c8aa936d364256671d31a1ae907677a63de2f8` | Mandatory source input: the historical control record (W1 window/offsets, boundary decode, pins, scans — the PRE expectations). |
| `docs/audits/PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009/QC_RESULTS.json` | 31350 | `de7df210fafa465e27d7a7c4410c9d9c44c9bae1492b9fede2b3101f01bf0545` | Mandatory source input: the historical QC record (contextual). |
| `docs/audits/PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009/FINAL_REPORT.md` | 15589 | `ff5fdbd2f54f20e3026b5992f7bcc411b0572ada249f157ba11cb441e1ac83e0` | Contextual input: source final report (read in full). |
| `docs/audits/PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009/CLAIM_MATRIX.csv` | 9721 | `1d32aadeffaaa177dc9b48165b612f0d4882b29b7bfb27d03ad9aa62c425254d` | Contextual input: source claim matrix (read in full). |
| `docs/audits/PE_935_CMO_SINGLE_WRITE_SOURCE_PROVENANCE_R1_20261009/MANIFEST_SHA256.csv` | 5368 | `5f1cae01e98f4c0a317d70f51032debfb3d50cd5c7b38df43042e7ce9e0310b5` | Contextual input: source manifest (format/coverage reference). |
| `docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007/SUPERSESSION.md` | 8339 | `dd11137a0e79491511a7688b7c1de9252db7ba443fa31892c345ca76ce136845` | Contextual input: the J3 SUPERSESSION — the source of the standing carried verbatim (statuses NOT re-derived, NOT reinterpreted). |
| `AUDIT_ENTRYPOINT.md` (repo root) | 269640 (pre-update) | `e707fcb7b52b8bdf27590063e2f5592a8e1925c025d3b1a8bfde355384788644` (pre-update) | Governance input (read) + the ONE new newest-first LATEST RUNS row for this run (no other row modified; post-update identity in MANIFEST_SHA256.csv). |

External inputs (outside the repository; identity-verified): the contract
`C:\Users\User\Documents\ChatGPT\PE\PE_CMO_C1_HIGH_BYTE_CORRECTION_PROMPT_20261008\OPENCODE_CMO_C1_HIGH_BYTE_CLOBBER_CORRECTION_R1_20261009.md`
— 16623 B / SHA256 `61aaa55854942a22085f3767a7d64512248edfae3a7b9bb54a5cbe36f36d3981`;
the target `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe` — 8015872 B /
SHA256 `e7785430e81dffe648ce8f5312414b17bc9fce61389689a22f753765d5280f31`
(unchanged before and after; read-only; reads limited to the approved windows;
NO EXE access in this persistence phase).

**Coverage note**: this index covers all 22 physical package files (17 frozen
executor/QC + 5 persistence-phase incl. this index and the self-excluded
manifest) + the updated AUDIT_ENTRYPOINT.md + the source inputs. Generator
provenance: PRE records generated by `run_pre_counterexamples.py`; POST/CONTROL/
REGRESSION by `run_alias_controls.py`; QC records by `qc_run_controls.py`
(all python -B; residue scans in-record: 0 hits); the persistence-phase
documents written by the pe-master-auditor persistence worker per the contract
§12; the manifest generated LAST with a bijection self-check.
