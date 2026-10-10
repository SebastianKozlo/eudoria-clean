# QC_REPORT — PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009

**QC ORIGIN = FRESH INTERNAL QC (pe-master-auditor, fresh session; internal to
PE-MASTER — this is NOT an independent Desktop post-audit).** All findings
below are the result of independent re-measurements executed by this QC session
(read-only against all originals; QC scripts and outputs live under
`00_CONTROL_INTERNAL_QC\`). BASE `f99febeca9498011fc49f3aef932ecfac4244475`
verified UNCHANGED at QC start and end; no staged/tracked changes; the 5 foreign
historical untracked dirs + `experiments/` preserved untouched.

**QC VERDICT: PASS_WITH_FINDINGS** (0 × P0, 0 × P1, 6 × P2, 4 × P3).
Every load-bearing measured claim re-measured by this QC reproduced exactly
(hashes, index derivation, countermodels, native outcomes, SDK/synthetic
controls, census denominators, selection ranking, block ceiling, geometry
fingerprint counts). The findings are mechanical/provenance defects — five SHA
transcription errors and one JSON-syntax defect in the DRAFT evidence index
(plus hygiene items) — none of which changes any scientific claim; exact
corrections and revalidation gates are given below.

---

## 1. Findings (ordered by severity)

### [P2-1] FINAL_REPORT §9 evidence index: cm1 raw-output SHA has 65 characters (a spurious inserted hex char)

- **Location:** `FINAL_REPORT.md`, section 9 index row
  `00_RECORDS_CORRECTION\countermodels\raw\cm1_escaped_local_output.json`
  (recorded SHA `1a609fb164cf3c92f984909ebcdda4139d9328c429f66f9a1c95524b00ba6a099`, 65 chars).
- **Claim contradicted:** the row asserts the file's SHA256 identity; the true
  disk hash (independently re-measured, and correctly recorded in
  `COUNTERMODEL_RESULTS.json`) is
  `1a609fb164cf3c92f984909ebcdda413d9328c429f66f9a1c95524b00ba6a099` (64
  chars) — the index string has an extra `9` inserted after `…a413`.
- **Independent counter-check:** raw-byte comparison `qc11c_sha_transcription_test.py`
  → `q11c_sha_transcription_test.json` (index 65 chars, cmr record 64 chars,
  disk 64 chars; `cmr_matches_disk: true`, `fr_matches_disk: false`).
- **Effect:** MANIFEST_IDENTITY_CORRECT fails for this row even though
  SOURCE_FILE_UNCHANGED holds (the physical file is byte-identical to its
  capture-time state; verified by mtime 2026-10-09 12:59:01 and by
  `COUNTERMODEL_RESULTS.json`'s correct record). A downstream bijection/
  manifest check against the draft index fails on this row.
- **Required correction:** replace the row's SHA with
  `1a609fb164cf3c92f984909ebcdda413d9328c429f66f9a1c95524b00ba6a099`.
- **Revalidation gate:** the persistence-phase manifest generator must re-hash
  every package file from disk (never trust the draft index); the corrected
  row must then match the regenerated manifest byte-for-byte.

### [P2-2] FINAL_REPORT §9 index: cm2 raw-output SHA has one wrong character

- **Location:** `FINAL_REPORT.md` §9 row `cm2_alias_model_output.json`
  (recorded `dfe28dc1e1b686553d0b5b79eaabeead550ffb2c46c5cad7dd67243b2bc1c24e`).
- **Claim contradicted:** true disk hash (and the correct record in
  `COUNTERMODEL_RESULTS.json`) is
  `dfe28dc1e1b686553d0b5a79eaabeead550ffb2c46c5cad7dd67243b2bc1c24e` — position
  21 is `a`, the index has `b`.
- **Independent counter-check:** `q11c_sha_transcription_test.json` (single-char
  diff at position 21; cmr record matches disk).
- **Required correction:** replace with the true hash above.
- **Revalidation gate:** as P2-1 (regenerated manifest bijection).

### [P2-3] FINAL_REPORT §9 index: cm3 raw-output SHA is 63 characters (a dropped hex char)

- **Location:** `FINAL_REPORT.md` §9 row `cm3_dword_float_copy_output.json`
  (recorded `2eb21d4f97c282f399327c5c72188979c1711ff1f7fa2c992eafa1c517004dc`, 63 chars).
- **Claim contradicted:** true disk hash is
  `2eb21d4f97c282f3993270c5c72188979c1711ff1f7fa2c992eafa1c517004dc` (64) — a
  `0` after `…99327` was dropped in the index string.
- **Independent counter-check:** `q11c_sha_transcription_test.json`
  (`fr_len: 63`, `cmr_len: 64`, `cmr_matches_disk: true`).
- **Required correction / revalidation gate:** as P2-1.

### [P2-4] FINAL_REPORT §9 index: cm4 raw-output SHA is 63 characters (a dropped hex char)

- **Location:** `FINAL_REPORT.md` §9 row `cm4_escaped_subject_outslot_output.json`
  (recorded `d1cf897752f256a597ef8ba291f13616f41eed98cbf8fad316898bc44466aa4`, 63 chars).
- **Claim contradicted:** true disk hash is
  `d1cf8977520f256a597ef8ba291f13616f41eed98cbf8fad316898bc44466aa4` (64) — a
  `0` at position 10 was dropped.
- **Independent counter-check:** `q11c_sha_transcription_test.json`.
- **Required correction / revalidation gate:** as P2-1.

### [P2-5] FINAL_REPORT §9 index: gb23 adapter copy SHA is 63 characters (a dropped hex char)

- **Location:** `FINAL_REPORT.md` §9 row `TOOLS\gamebryo_oracle_r1\adapters\gb23\adapter.py`
  (recorded `3bcda25764deaa6d33677e41c1a5242b5006b0410bdbd29b7bb9def11069453`, 63 chars).
- **Claim contradicted:** true hash is
  `3bcda25764deaa6d33677e41c1a5242b5006b0410b5dbd29b7bb9def11069453` (64) — a
  `5` was dropped (`…0410bdbd…` vs true `…0410b5dbd…`).
- **Independent counter-check:** `qc11b_index_char_diff.py` (length 63 vs 64);
  the copy is byte-identical to the canonical
  `tools/gamebryo_oracle/adapters/gb23/adapter.py` (verified 18/18 files
  byte-identical), so the canonical hash equals the true copy hash.
- **Required correction / revalidation gate:** as P2-1.

*(P2-1…P2-5 share one mechanism: SHA transcription defects in the DRAFT index.
The physical files are byte-unchanged and their true identities are correctly
recorded in COUNTERMODEL_RESULTS.json / the copy-identity records — the defect
is confined to FINAL_REPORT §9's hand-transcribed index rows.)*

### [P2-6] COUNTERMODEL_RESULTS.json was not valid JSON (repaired under the one in-run repair round)

- **Location:** `00_RECORDS_CORRECTION\COUNTERMODEL_RESULTS.json`, line 131:
  `"countermodels_supplied": 5 (4 JSON groups from … pre-registered)",` — a
  bare number followed by an unquoted annotation (invalid JSON value).
- **Claim contradicted:** the artifact is a required machine-readable record
  (contract §15); strict parsers fail on the whole file, making even the
  load-bearing countermodel records machine-inaccessible.
- **Independent counter-check:** full-file strict parse failed before repair
  (Python json: "Expecting ',' delimiter", line 131 col 33); all five
  countermodel records themselves were independently re-executed and verified
  (see re-measurements), so the semantic content was correct and the defect
  was purely syntactic.
- **Repair performed (the ONE targeted in-run repair authorized for
  executor-evidence mechanical defects):** value split into
  `"countermodels_supplied": 5,` +
  `"countermodels_supplied_note": "4 JSON groups from … pre-registered",`
  (content preserved verbatim; count remains a number). PRE-REPAIR:
  13,234 B / SHA256 `e687c8f393740ef62271a16fce0fce5d6720bb52f99099d7584fb093be6b690c`
  (= the draft index record — the file was in its draft state). POST-REPAIR:
  13,269 B / SHA256 `2e159900137c14faefcbf910d0025769891cef8cc6f739573a6996fdf3346ed1`;
  strict parse now succeeds; all 5 records + summary intact.
- **Effect:** the FINAL_REPORT §9 recorded hash for this file is superseded
  (documented in AMEND_LOG.md); the persistence-phase manifest must use the
  post-repair hash.
- **Revalidation gate:** strict `json.loads` on the repaired file (executed,
  passes); PE-MASTER must independently audit this change (self-check
  disclosure per the QC contract — this QC authored the change).
- **Disposition:** REPAIRED (QC); capability/phase not affected — the records
  correction (Package A) content was and remains fully valid.

### [P3-1] Raw countermodel outputs carry a UTF-8 BOM

- **Location:** the five files under
  `00_RECORDS_CORRECTION\countermodels\raw\cm*_output.json` each begin with
  `EF BB BF` (PowerShell-capture artifact).
- **Skutek:** strict RFC 8259 parsers (e.g., Python `json.loads`) reject the
  files as-is; content is valid JSON after the BOM and the files are
  SHA-pinned by COUNTERMODEL_RESULTS.json (all five pins verified correct —
  see P2-1…P2-4).
- **Required correction:** document the BOM in the persistence manifest
  (or re-capture BOM-less in a future authorized round). NOT modified by this
  QC: they are executor evidence whose recorded hashes must not be silently
  invalidated.
- **Revalidation gate:** `json.loads(open(p, encoding='utf-8-sig'))` passes
  for all five (verified); manifest rows must keep the existing pinned SHAs.

### [P3-2] LOCAL_ONLY_ROOT README manifest omits the 01_SDK_fixtures section

- **Location:** `99_Audits\PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009\README.md`
  — documents Phase-1 and the 02_PE payloads/work files, but not the
  `01_SDK_fixtures\` files (synthetic + negative-mutation fixtures that exist
  on disk).
- **Skutek:** the private manifest is incomplete for a later local audit
  (fixtures ARE documented repo-side in `SDK_EXECUTION_RESULTS.json`
  mutations_and_negative_fixture_records, with LOCAL_ONLY paths+SHAs).
- **Required correction:** append an 01_SDK_fixtures section to the README
  (persistence phase or a future authorized local-only manifest update).
- **Revalidation gate:** fixture files on disk match the
  SDK_EXECUTION_RESULTS.json recorded SHAs (spot-verified: SYNTH_UNKNOWN_CLASS
  `dae5e636…`, SYNTH_EMPTY_SCENE `86ae58aa…` etc. — my QC re-ran two of them).

### [P3-3] Standalone EVIDENCE_INDEX.md not yet present (assigned to persistence)

- **Location:** package root — no `EVIDENCE_INDEX.md`; the draft index lives
  as FINAL_REPORT §9; `HANDOFF.md` assigns
  EVIDENCE_INDEX/MANIFEST/PE_MASTER_REVIEW to the QC+persistence phases.
- **Skutek:** contract §15 file list is not yet complete — by explicit
  staging, not omission; MUST exist before the final manifest.
- **Required correction:** generate the standalone EVIDENCE_INDEX.md in the
  persistence phase from a fresh full-package re-hash (see P2-1…P2-6 — do not
  copy the draft rows).
- **Revalidation gate:** bijection with the physical package (contract §18:
  no duplicate, missing, extra, size mismatch or SHA mismatch).

### [P3-4] QC-session transient residue (created and removed by THIS QC)

- **Location:** `TOOLS\gamebryo_oracle_r1\adapters\gb12\__pycache__\registry.cpython-312.pyc`
  — created 2026-10-09 23:27:50 by THIS QC session's import of `registry.py`
  (importlib SourceFileLoader bytecode cache, run without `-B`), NOT by the
  executor (the executor ran with `python -B`; their zero-residue claim stands).
- **Skutek:** transient hygiene residue only; removed immediately; package
  residue count at QC end = 0.
- **Required correction:** none (done); future QC scripts must use `python -B`
  for in-package imports (this QC's later scripts did).
- **Revalidation gate:** `__pycache__|*.pyc` scan of the package = 0 (verified
  at QC end).

---

## 2. Per-duty results (all 11 duties executed; details in 00_CONTROL_INTERNAL_QC\)

| # | Duty | Result | Key independent evidence |
|---|---|---|---|
| 1 | Re-adjudicate FC-C1/C2/C3 | PASS | Corrected semantics match contract §4 wording exactly (NOT_ESTABLISHED_WITHIN_BOUND growth path; CONTAINER_VS_P_ALIAS_RELATION=UNRESOLVED; DIRECT_TRANSFORM_OPERATION=NOT_ESTABLISHED + ROLE_IN_PLACEMENT_PIPELINE=UNRESOLVED; arg1–arg5 direct slot usage; retained facts — pins, range begin/end, stride 0x20, indirect call target, fast-path two-DWORD copy — all present in SUPERSESSION §6). OLD wording verified REAL in the frozen f99febe package (ARGUMENT_PROVENANCE.json:20 arg6 row verified byte-exact; FALSIFIER_RESULTS.json:85; FINAL_REPORT:37/171; HANDOFF:82/157; "NEVER dereferenced" absolutes). Historical package files' SHAs match CORRECTED_CLAIM_MATRIX's registry (7/7 re-hashed). **All 5 countermodel scripts read in full and ALL 5 independently re-executed by this QC (exit 0, every expected value reproduced; exceeds the required minimum of 2)**; logical-not-actual-execution labeling present in scripts, results and preregistration. |
| 2 | Recompute hashes + extraction ranges | PASS | 14/14 identities re-measured MATCH (6 Desktop inputs, contract, printer, 2 DLLs, Models.bnt, 218757 pin, gb12_oracle.exe, Entropia.exe). Independent BNT2 index derivation with my OWN reader: dir_offset 395,262,727, 5,596 entries, entry `218757.nif` ordinal 781 @ offset 116,223,520, size 57,316, name byte-offset 395,283,797 — ALL historical cross-checks match; ambiguity sweep: exactly 1 entry with "218757" in name, 1 sharing the declared range, 1 same-size payload with the pin SHA across the whole 5,596-entry archive; fresh extraction byte-identical to the pin → UNIQUE_DERIVATION_OK (`q2_218757_relation.json`). |
| 3 | Rerun native SDK graph controls | PASS | Positive controls re-executed with my own invocation (child-process PATH DLL exposure, same class): WORLD.nif exit 0 (stdout 62,912 B) and OBJECT.NIF exit 0 (6,594 B) — **byte-identical to the executor's raw logs after normalizing only the per-run SDK heap addresses**; printer SHA unchanged before/after. Synthetic transform control TRANSLATED_PARENT re-executed: exit 0, 2 visits, camera World Bound C <101,202,303> = the preregistered expected value; the stdout size difference (988 vs 701 B) is explained by my fuller flag set — the executor's preregistered synthetic invocation used `-trans -bs -mem` (recorded in synthetic_control_details_internal.json), mine used all six flags; the -trans/-bs sections match exactly. |
| 4 | Reproduce PE native outcomes | PASS | 218757 and 423020 re-run by me on the pinned stock printer: both exit 1, stdout empty, stderr byte-exact `Error loading stream.\r\n` (23 B) — identical to the executor's raw logs; all four PE raw stderr files verified byte-identical. |
| 5 | Namespaces and counts | PASS | 62+4/66 ceiling preserved in PARSER_NATIVE_COMPARISON.json and INDEPENDENTLY REPRODUCED: my own NIF 10.1 header census of 218757.nif (layout derived from the pinned NiStream.cpp source: header line → u32 version → u32 user version → u32 numObjects=66 → u16 RTTICount=12 → LoadRTTIString names → u16 type indices) yields exactly 4 NiArk blocks (1× Animation/Importer/Texture/ViewportInfo); parser-output recount: 62 semantically-decoded (47 with transforms/names + 14 NiTriShapeData + 1 NiStringExtraData) + 4 UNREGISTERED_IN_GB12_FACTORY boundary-only = 66. Four namespaces (ORIGINAL_NATIVE_EXECUTION / SOURCE_PREDICTED_ORIGINAL_VERDICT / OUR_PARSER_RESULT / OUR_EXTENSION_CONTINUATION, plus the separately-labeled OBSERVED_NATIVE_ERROR_HELPER) distinct per input for all 4 payloads. Visit-vs-block-vs-unique separation verified: SDK WORLD 131 visits / 396 blocks / 130 unique; PE inputs 0 visits (all rejected; populated-scene rule enforced, populated_scene_inspection=false). 423020 coverage algebra verified (432+5=437; 4 NiArk + 1 registered-but-not-decoded NiTextureEffect). |
| 6 | 10 adversarial checks | PASS | All 10 honestly handled — see section 3 below. |
| 7 | Census audit | PASS | Full CSV parsed (every row, 5,596): version counts 4,838 × 10.1.0.0 / 757 × 4.1.0.12 / **1 × 4.0.0.2 = the "+1 unit": entry 799 `52555.nif`, histogram_status HEADER_UNSUPPORTED, num_blocks EMPTY (NOT_MEASURED, not zero)** → HEADER_UNSUPPORTED 758 = 757+1 ✓. Histogram sums == num_blocks for 4,838/4,838 SCANNED rows (0 mismatches). STOCK-ONLY: 0/4,838 candidates (corpus-proven — all 4,838 files declare NiArkAnimation/Importer/Texture ExtraData; physical verification: ZERO NiArk references in the SDK CoreLibs source; registry 198 names, zero NiArk*). Non-stock class census reproduced 7/7 exactly (NiArkAnimation 4838, NiArkImporter 4838, NiArkTexture 4838, NiArkViewportInfo 4062, NiArkShader 1293, NiArkBillboardNode 12, NiVertexMorphExtraData 118). Compound pool 1,135 reproduced; ranking rule re-implemented independently → top 3 = 496633 (166/163), 512126 (122/129), 423020 (119/102) EXACTLY as selected; 218757 in pool and deduped as mandatory; hard max 5 respected (4 distinct); selection frozen before inspection (PREREGISTRATION_PE_PHASE §3 predates executions; SELECTION_AND_EXTRACTION_PROVENANCE.json `selection_frozen_before_native_or_deep_inspection: true`). |
| 8 | Budget/stop audit | PASS | The closure-search budget is the canonical tool's PRE-EXISTING constant (gb12core.py: MAX_SEARCH_ATTEMPTS=250000, MAX_RUN_SKIP=65536) — the run's oracle copy is byte-identical to the canonical tree (18/18 files verified), so no post-hoc invention. 496633: the tool's internal budget exhausted, measured (exit 0, elapsed 1,011 s under the 2,100 s operational bound; the preceding 300 s runner timeout retained as a measured event in ORACLE_RUN_PROVENANCE.json). 512126: CLOSURE_SEARCH_FAILED — no boundary assignment closes the file. Both failed outcomes RETAINED without candidate replacement (no next-ranked candidate was run — the 4 selected payloads are the only native/parser inputs in the artifacts); no success-chasing. |
| 9 | Helper audit | PASS | Identity pin re-verified (DD7112A4…, 594,944 B). Source oracle.cpp SHA AD1F5DED… re-verified; my own source inspection: the ONLY error-machinery reference is `GetLastErrorMessage` (NiStream public API) — zero NiArk, zero dummy-factory registration, zero guessed loaders; 6 behavior differences disclosed. Controls 3/3 (my own independent re-run of the QC2 control reproduces `QzNode: cannot find create function.` exit 1). The specific error `NiArkAnimationExtraData: cannot find create function.` (lastError 5 = NO_CREATE_FUNCTION) is recorded as HELPER-OBSERVED under CUSTOM_SDK_SOURCE_HELPER_EXECUTION — namespace `ORIGINAL_NATIVE_EXECUTION (OBSERVED VIA THE ONE DISCLOSED HELPER…)` — always separate from stock output and from SOURCE_PREDICTED; my own re-run on 218757 reproduces it exactly. SDK tree unmodified (NiStream.cpp e955c36e… = the cited source identity; all physical pins unchanged at QC end). |
| 10 | FINAL_REPORT draft audit | PASS_WITH_FINDINGS | Labeled FINAL_REPORT_DRAFT_QC_PENDING ✓. Recomputed measured fields: PE_METADATA_CENSUS_COUNT ✓ (all denominators reproduce — duty 7); PE_DEEP_INPUT_COUNT 4/5 with all four payload SHAs ✓ (all four re-verified on disk); MODEL_218757_NATIVE_RESULT ✓ (reproduced by me); MODEL_218757_CUSTOM_PARSE_COVERAGE 62+4/66 ✓ (independently reproduced — duty 5); COMPOUND_SCENE_CANDIDATES_INSPECTED 1/3 + 2/3 ✓; MODEL_GEOMETRY_MATCHES 0 / NO_MATCH_IN_SELECTED_INPUTS ✓ (14 vs 102 — 14 meshes listed EXTRACTED_VALIDATED, matches=[], and my SCENE_STRUCTURE recount finds exactly 116 EXTRACTED_VALIDATED = 14+102). Human-first ordering ✓ (§0 human-decision block); denominators everywhere ✓; honest NOT_CHECKED ✓ (§7); placement-ceiling defaults §5 unmodified ✓ (all five exactly per contract §14). Zero proprietary payloads: full-package extension census — **0 files with nif/bnt/dll/exe/dtx/dgc/dat/bin/ark/vfs/pak extensions** (55 txt / 54 json / 34 py / 10 md / 2 ps1 / 1 csv / 1 .gitignore). Draft package count 132 verified (130 index rows + FINAL_REPORT + HANDOFF). The §9 index carries findings P2-1…P2-5. |
| 11 | Package hygiene | PASS_WITH_FINDINGS | All contract-§15 files for phases A/B/C present and non-vacuous (EVIDENCE_INDEX standalone + MANIFEST explicitly persistence-phase — P3-3; PE_MASTER_REVIEW/QC files are this QC + PE-MASTER's own). JSON validation: after the P2-6 repair, every executor+QC JSON parses strictly as UTF-8, except the 5 BOM-pinned raw captures (P3-1). INTERVENTION_LEDGER covers ALL native executions with classes: 16 SDK (CHILD_PROCESS_PATH_DLL_EXPOSURE) + 4 PE stock (same class) + 7 helper (CUSTOM_SDK_SOURCE_HELPER_EXECUTION) = 27/27. Raw logs referenced in JSONs all exist (139 real paths verified; the 13 regex "missing" are prose citations plus the intentional MISSING_INPUT control file). `__pycache__`/`*.pyc` residue = 0 at QC end (executor zero; my own transient residue P3-4 removed). BASE unchanged at start and end; foreign untracked preserved (5 historical dirs + experiments/); no staged/tracked changes. Oracle copy byte-identity 18/18. |

---

## 3. The 10 required adversarial checks (contract §16; how the package handles each, with my verification)

| # | Adversarial check | Package handling | My verification |
|---|---|---|---|
| 1 | Growth helper may mutate an escaped local without violating the ABI | CM-1 (3 cases; ABI conditions preserved in all three, later_arg6 diverges in the mutation case); SUPERSESSION §1.3.3; NOT_ESTABLISHED_WITHIN_BOUND | Re-executed CM-1 myself: 3/3 cases, expected values exact (305419896/305419896/2271560481) |
| 2 | Distinct provenance sources can alias | CM-2 (distinct chains, same address, disjoint field roles); CONTAINER_VS_P_ALIAS_RELATION = UNRESOLVED in SUPERSESSION §2.2.2 + matrix | Re-executed CM-2 myself: same_address true, disjoint offsets, values exact |
| 3 | DWORD copies can carry float bits without FPU/SSE | CM-3; SUPERSESSION §3.2.3 ("absence of FPU/SSE does not exclude float bit copies") | Re-executed CM-3 myself: 1234.5→0x449a5000→1234.5 and -42.25→0xc2290000→-42.25, bit-identical, 0 float ops |
| 4 | Empty output + exit 0 is not a populated scene | Preregistered populated-scene rule (exit 0 AND ≥1 numbered visit AND nonzero Total Object Count); N6/SYNTH_EMPTY_SCENE honestly classified empty; NATIVE_EXECUTION_RESULTS carries the rule; all 4 PE inputs marked populated_scene_inspection=false | Rule verified present in NATIVE_EXECUTION_RESULTS.json (`populated_scene_rule` field) + PREREGISTRATION_PE_PHASE §4 |
| 5 | Native traversal counts can differ from block counts and unique pointers | TOOL_CAPABILITY_MATRIX C7 (three DISTINCT count namespaces PASS); measured: DT 388 visits/1226 blocks/388 unique; WORLD 131 visits/396 blocks/130 unique; OBJECT 17 visits/60 blocks/16 unique | My own WORLD/OBJECT re-runs reproduce 131 and 17 visit rows; counts recorded in SDK_EXECUTION_RESULTS match |
| 6 | Source-derived predicted rejection is not actual native execution | SOURCE_PREDICTED_ORIGINAL_VERDICT kept as its own namespace ("NEVER an observed native report"); observed native (stock generic + helper-specific) recorded separately with cross_namespace_checks agree=true | Verified per-input in PARSER_NATIVE_COMPARISON.json for all 4 payloads |
| 7 | Opaque blocks are not semantic decodes | 4 NiArk blocks = boundary-only, "NOT promoted to semantic decodes"; coverage INCOMPLETE (not COMPLETE); 423020's registered-but-not-decoded NiTextureEffect kept boundary-only | My own recount reproduces 62 semantic + 4 UNREGISTERED_IN_GB12_FACTORY (boundary-only) = 66 |
| 8 | Bounds center is not a building position | "-bs is a bounding sphere, not a building pivot" (preregistered); bounds recorded as a SEPARATE measurement; extents [2500,3350,1250] recorded with "NO historical location derived"; NiCamera bound-center = world-translation equivalence scoped to NiCamera only | Verified in PREREGISTRATION_SDK_PHASE §1/§3, SCENE_STRUCTURE and FINAL_REPORT §4.6 |
| 9 | Same mesh/asset is not same instance | "Exact shared geometry does NOT establish the same runtime instance or historical building"; PARTIAL vs complete kept separate; no fuzzy threshold/texture-name-only/plausible-coordinate acceptance | Verified in MODEL_218757_RELATION_RESULTS.json fingerprint_method + note (and the run found 0 matches anyway) |
| 10 | An unqualified root cannot confer historical global XYZ | FILE_SCENE_SPACE discipline (no PE axis/unit import); placement ceiling: MODEL_218757_TO_CMO_JOIN / HISTORICAL_WORLD_INSTANCE / PE_WORLD_ROOT_IDENTITY = NOT_ESTABLISHED; PE_AXES_AND_UNITS = UNVERIFIED; WORLD_XYZ_RECOVERED = NO — unmodified in every artifact | Verified in PREREGISTRATION_PE_PHASE §7, PARSER/SCENE/RELATION artifacts and FINAL_REPORT §5 — defaults byte-consistent with contract §14 |

---

## 4. Re-measurements table (my independent recomputations / re-executions)

| What | Method | Result |
|---|---|---|
| 14 pinned identities (6 Desktop inputs, contract, printer, 2 DLLs, Models.bnt, 218757 pin, gb12_oracle.exe, Entropia.exe) | PowerShell Get-FileHash/Get-Item | 14/14 MATCH (`q1_hash_recompute.json`) |
| 218757 index relation | My own BNT2 reader (bounds/dup/EOF-exact/overlap validated; ambiguity sweep) | UNIQUE_DERIVATION_OK — ordinal 781 / offset 116,223,520 / size 57,316 / name-offset 395,283,797; fresh extraction byte-identical to pin; 1-of-1 uniqueness across all 5,596 entries |
| 5 countermodels | Re-execution of all five scripts (python -B) | 5/5 REPRODUCED, exit 0, every expected value exact (outputs in `qc_countermodel_rerun\`) |
| SDK positive controls | My own printer invocation (WORLD.nif, OBJECT.NIF; child PATH DLL exposure) | exit 0 both; byte-identical to executor raw logs modulo per-run heap addresses (62,912 / 6,594 B) |
| Synthetic transform control | My own printer invocation (TRANSLATED_PARENT) | exit 0; camera World Bound C = (101,202,303) = preregistered expectation |
| PE native outcomes | My own printer invocation (218757, 423020) | both exit 1 + `Error loading stream.` (23 B stderr, stdout empty) — byte-identical to executor logs |
| Helper observations | My own gb12_oracle.exe runs (218757 + QC2 control) | `NiArkAnimationExtraData: cannot find create function.` / `QzNode: cannot find create function.` — reproduced exactly (lastError 5) |
| 218757 block census | My own NIF 10.1 header reader (from pinned NiStream.cpp layout) + parser-output recount | 66 blocks / 12 types / exactly 4 NiArk; 62 semantic + 4 boundary-only = 66 ceiling reproduced |
| Census CSV | Full parse of all 5,596 rows + recomputation from columns | 4838/757/1; +1 = entry 799 `52555.nif` (4.0.0.2); 758 HEADER_UNSUPPORTED; 0 sum mismatches; 0/4838 stock-only; 1135 pool; top-3 ranking exact |
| Stock registry NiArk-absence | Grep of SDK CoreLibs source | 0 NiArk references in CoreLibs (2 false positives are binary texture files in Samples) |
| Oracle copy fidelity | Per-file hash vs canonical tools/gamebryo_oracle | 18/18 byte-identical (budget constants pre-existing: MAX_SEARCH_ATTEMPTS=250000, MAX_RUN_SKIP=65536) |
| SDK source identities | NiStream.cpp + oracle.cpp hashes | e955c36e… / ad1f5ded… — match all citations |
| Geometry extraction count | Recount of EXTRACTED_VALIDATED in SCENE_STRUCTURE_RESULTS | 116 = 14 (218757) + 102 (423020) |
| JSON validation | Strict parse of all package .json (UTF-8) | executor: 1 syntax defect (repaired, P2-6) + 5 BOM captures (P3-1); post-repair all pass |
| Package payload census | Full extension census | 0 proprietary-payload files (no nif/bnt/dll/exe/…) |
| EVIDENCE_INDEX bijection | Re-hash of all 130 draft rows | 124 match + 5 SHA transcription defects (P2-1…5) + 1 post-repair supersession (P2-6) |
| Raw-path existence | Existence check of all referenced absolute paths | 139/139 real paths exist (13 regex false-positives = prose citations + the intentional MISSING_INPUT) |
| BASE / repo state | git at QC start and end | HEAD = f99febec… unchanged; 0 staged; 0 tracked mods; foreign untracked preserved |

---

## 5. QC conclusion

The executor's work is **faithful and measured**: every scientific claim I
re-measured reproduced exactly, negative results were retained honestly,
no success-chasing occurred, the placement ceiling is unmodified, no
proprietary payload entered the repo package, and the intervention ledger
covers all native executions. The defects found are confined to the DRAFT
report's hand-transcribed evidence index (5 SHA transcription errors) and one
JSON-syntax defect in a records artifact (repaired in-run, documented) plus
minor hygiene items. All corrections are mechanical with exact values
supplied; the persistence phase MUST regenerate every hash from disk rather
than trusting the draft index rows.

**This QC is INTERNAL to PE-MASTER; it is not the independent Desktop
post-audit (DESKTOP_POST_AUDIT remains PENDING). No qualification of any kind
(CANONICAL_GATE_EFFECT = NONE). This QC performed one targeted executor-side
repair (P2-6) — PE-MASTER must independently audit that change.**

FULL_READ_LOG (files read to EOF by this QC): governing contract (426 lines),
AUTHORIZATION_AND_PREFLIGHT.md, PREREGISTRATION.md, HANDOFF.md,
00_RECORDS_CORRECTION\SUPERSESSION.md, CORRECTED_CLAIM_MATRIX.json,
COUNTERMODEL_RESULTS.json, all 5 countermodel scripts + 2 raw outputs,
01_SDK\PREREGISTRATION_SDK_PHASE.md, SDK_EXECUTION_RESULTS.json (key sections
in full incl. all mutation records), synthetic_control_details_internal.json
(controls 1-3 read; 4-6 same structure), 02_PE\PREREGISTRATION_PE_PHASE.md,
PARSER_NATIVE_COMPARISON.json, CENSUS_SUMMARY.json,
SELECTION_AND_EXTRACTION_PROVENANCE.json, NATIVE_HELPER_RESULTS.json (full),
NATIVE_EXECUTION_RESULTS.json (full structure + all case records),
ORACLE_RUN_PROVENANCE.json (rerun records), MODEL_218757_RELATION_RESULTS.json,
INTERVENTION_LEDGER.md, LOCAL_ONLY README.md, Desktop REPORT.md + countermodel
JSON, selected f99febe records (targeted greps + line reads), FINAL_REPORT.md
(619 lines), NiStream.cpp LoadHeader/LoadRTTI/LoadRTTIString sections,
gb12core.py closure-search sections, my own QC outputs.

NOT_CHECKED (explicit): SceneViewer/SceneDesigner GUI capabilities (SOURCE_ONLY
by contract — not executed, correctly); per-value controller mutation at
Update(0) (no controllers exist in the closure-verified PE inputs; honestly
NOT_MEASURED); the 40-entry compound shortlist ranks 4-40 beyond the selected
top-3 (not re-verified individually beyond ranking-rule spot-equivalence);
the 757 4.1.0.12 headers were not independently re-parsed beyond the CSV
num_blocks field consistency (the executor's nif_parser_v2 layout claim is
taken as preregistered scope, consistent with the historical Rosetta census);
SYNTHETIC_AND_NEGATIVE_CONTROLS.json fields 3-10 (negative mutation cases) were
verified via SDK_EXECUTION_RESULTS's mutation records (same data) rather than
re-run natively by this QC (my native re-runs covered positive + synthetic +
PE + helper classes).

**No P0/P1 findings → no capability or phase ends in this verdict.**
Per-duty PASS with the P2/P3 findings recorded above and their revalidation
gates. QC_VERDICT = **PASS_WITH_FINDINGS**.
