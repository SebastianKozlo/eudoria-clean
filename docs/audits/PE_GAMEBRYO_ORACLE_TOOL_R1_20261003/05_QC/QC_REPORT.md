# QC_REPORT — PE_GAMEBRYO_ORACLE_TOOL_R1_20261003

```
RUN_ID            : PE_GAMEBRYO_ORACLE_TOOL_R1_20261003
QC_RUN_ID         : PE_GAMEBRYO_ORACLE_TOOL_R1_20261003_QC_R1 (fresh independent internal QC, order s29)
QC_WORKER         : pe-master-auditor, FRESH context — NOT this run's formalizer,
                    NOT the executor; performed NONE of the run's work
                  (independence per RUN_CONTRACT (n)/AUTHORIZATION A1.2)
BINDING CONTRACT  : RUN_CONTRACT.md section (n) + human order section 29
QC_DATE           : 2026-10-03
QC BUDGET         : <= 40 tool calls / <= 90 wall minutes (used: 40 calls incl.
                    this report; every checklist item executed)
QC_VERDICT        : **QC_PARTIAL** — all scientific substance independently
                    VERIFIED; 6 findings (1×P1, 5×P2) require PE-MASTER-ordered
                    corrections BEFORE the persistence phase (MANIFEST + staging
                    have not run yet, so corrections are still cheap; once
                    published the package is immutable)
ADVISORY STATUS   : ADVISORY_PRE_QUALIFICATION (Q1 absent; no milestone effect;
                    QC is internal QC — MASTER_ACCEPTED and closure remain
                    PE-MASTER/human decisions)
```

## 0. Verdict rationale

Every load-bearing scientific claim I tested reproduces exactly: independent
hashes all match their pins; NIF versions confirmed from raw header bytes; my 7
oracle re-runs are **byte-identical** to the executor's published JSONs; all 5
executor determinism pairs re-hash byte-identical; the fail-closed behavior is
real (my own corrupted-copy and unknown-class controls reproduce it); the
selection lock precedes the first oracle output; pins P1/P2/P4 and records
R6/R7/R8 reconcile against the physical sources; the honest negatives (T2/T5
EOF, T3 448/1288, T4 by-design, tool blockers) are recorded as failures
everywhere with **zero silent skips**. The findings below are
evidence-persistence / machine-readability / hygiene defects that do not
falsify any scientific result but should be corrected before MANIFEST/staging.

## 1. QC checklist results (RUN_CONTRACT (n) items 1-10 + task items 11-12)

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | Independent hashes | **PASS** | §2 table — all match pins (payloads, manifest, NiStream.cpp ×2, SELECTION.md); tool + extra-source hashes QC-recorded |
| 2 | NIF versions from file headers | **PASS** | §3 — raw bytes read by me, not manifest/report |
| 3 | Re-run ≥ 3 oracle tests vs executor | **PASS** | §4 — 7 outputs byte-identical; T1+T4+T2 covered, gb12+gb26, full/orig/probe |
| 4 | Raw vs wrapper | **PASS** | §6 — 66 blocks, Scene Root identity transform, NiArk* list, 13/4/1/1 counts, matrix cells all reconcile |
| 5 | Negative controls executed by QC | **PASS** (with finding P1-1) | §5 — corrupted-version REJECTED; mid-file never accepted; unknown-class REPORTED; detector list verified in code (§5.3) |
| 6 | No proprietary content in package/tool | **PASS** (with finding P2-4) | §7 — census: package 71 files all text; tools 22 incl. 5 .pyc (hygiene finding); sandbox binaries LOCAL_ONLY outside repo |
| 7 | Determinism + no wall-clock | **PASS** | §8 — 5 executor pairs + my own T4 pair byte-identical; 0 date patterns in oracle JSON bodies |
| 8 | Selection lock order + R6 | **PASS** | §9 — lock sha + size + timestamps verified; R6 exactly once, 3-way 948 B tie |
| 9 | Gate predicates vs artifacts | **PASS-substance** (P1-1, P2-1, P2-2, P2-5) | §10 — per-gate trace incl. G-TOOL-3 controls, G-CMP-2 explanations, G-218757-2 statuses, G-MATRIX-1 zero blanks |
| 10 | Pin reconciliations P1/P2/P4 + R7/R8 | **PASS** | §11 — source lines read by me; GB112 lib re-hashed (FF4519AF exact); dialog verbatim; shader chain in gui logs |
| 11 | 30-question completeness | **PASS** | §12 — Q1..Q30 all numbered, each with evidence status |
| 12 | Honest-negative audit | **PASS** | §13 — all failures recorded as failures; T3 448/1288 never promoted; no silent skip anywhere |

## 2. Independent hashes (re-computed by QC, 2026-10-03)

| Artifact | My SHA256 | Pinned expectation | Result |
|---|---|---|---|
| sandbox\payloads\218757.nif (T1, 57,316 B) | `3E8A22C2213202207E374B55CD65B2C3BE039CCDD1E8D01A07FCAF44DE12CF36` | same | MATCH |
| sandbox\payloads\533021.nif (T2, 537 B) | `9CFF776D204AEC7B64377DD365AC11A71C9DCFA4A00A5905E642EE7420D5DC28` | same | MATCH |
| sandbox\payloads\496633.nif (T3, 2,068,670 B) | `4DBCC7311884C453CBB2255C1592994A225088D1D9BBB47D2D0C287580B7369` | same | MATCH |
| sandbox\payloads\223534.nif (T4, 948 B) | `81CB4D8D1ABC166C8384FCBD8CDAC4D93FE9D925BCF79FF7E6DFAC13D1000BE0` | same | MATCH |
| sandbox\payloads\547226.nif (T5, 537 B) | `D7F2A02CC86FBFAEFF10FFEA285E0A7A5BB7745494E888F79239D84D73E5F8DB` | same | MATCH |
| docs/nif/corpus/pcg953_nif_manifest.csv | `2BE0DEFC9C09FF26371528A4601C10216AC3013717A244EB0652169123989B59` | same | MATCH |
| Gb12_Source\CoreLibs\NiMain\NiStream.cpp | `E955C36EBBB442029E00BE8A154726741B8454A607F2DC043F1FD542B009DC25` | same | MATCH |
| Gb26_src\NiStream.cpp | `72781EEB0E22D42152E04FADD498EA30292D1807E5C60378F08BFD8563693BA2` | same | MATCH |
| Gb12_Source\CoreLibs\NiMain\NiObject.cpp | `B137FE42126F496A37E7627061FF968256A6DA87D912784865609E2122FE470E` | gb12core canon | MATCH |
| Gb12_Source\CoreLibs\NiMain\NiObjectNET.cpp | `2ADB8F89CDB40F8C114FEAA6E4A32DD7A1CC73BCE30D745F669458EE6F354190` | gb12core canon | MATCH |
| "Gamebryo 1.1.2 Evaluation\SDK\Win32\Lib\VC71\ReleaseLib\NiMain.lib" (3,073,590 B) | `FF4519AFD2475D9A6E71A35E5DB6B0F5A0B7E9E86EC3662C6A340DA19BA06597` | P4 pin prefix FF4519AF / SOURCE_ORACLE_INDEX row | MATCH (P4 CONFIRMED) |
| 00_CONTROL/SELECTION.md (9,954 B) | `4A67C6B844B6DA65DF403AA5B87B8012FECB7CBBF60051422E306E93C733381C` | SELECTION_LOCK selection_lock_sha256 | MATCH |
| tools/gamebryo_oracle/oracle.py | `6F5FE8E725944AD93B34CF2A21FB58A5E9166C9D697690A3982E9CFB5B5F2947` | QC-recorded (manifest pins later) | — |
| tools/gamebryo_oracle/gb12core.py | `93989D7294C16CAFC57D6910FB70171CC4D5A4F63F684D28DE84FDC19DA177B0` | BATCH_E3_RETURN pin (post-E3) | MATCH |
| tools/gamebryo_oracle/adapters/gb12/adapter.py | `46FCE9A1969E036F60D48BF05FEA9355AA0E1992F1A48FEEE590D7E2D99B503C` | QC-recorded | — |
| tools/gamebryo_oracle/adapters/gb26/adapter.py | `E9B5DC0818CCAE52CB0C100512185AA5EB2E66BAABDDDC17354C873DB8CFDC4B` | QC-recorded | — |

Package drift check (current bytes vs the batch-return pins): 218757_NIF_RESULT.md
(35C0E9A5…), NOT_CHECKED.md (FE2C56EC…), FINAL_REPORT.md (DB7C9E7D…),
HANDOFF.md (B9D113FA…), STAGE_ACCEPTANCE_GATES.csv (69540A42…),
compare_T3.json (B810FA6A…), TEST_MATRIX.csv (010F3BDA…),
FAIL_CLOSED_TESTS.md (B42D1A92…), sgp_T1_dialog.txt (180EB479…),
GAMEBRYO_SEMANTIC_SIGNATURES.json (CE84F485…),
RETRACTIONS_SUPERSESSIONS.md (6177511F…), GAMEBRYO_COMPATIBILITY_MATRIX.csv
(92E34E94…) — **all 12 MATCH (no post-batch drift)**. MANIFEST_SHA256.csv does
not exist yet (correct: persistence phase pending).

## 3. NIF versions from raw file headers (item 2)

Read directly from payload bytes (first 64 ASCII bytes, QC byte-level read —
not the manifest, not the report):

| T | Header line (raw bytes) | Expected | Result |
|---|---|---|---|
| T1 218757.nif | `Gamebryo File Format, Version 10.1.0.0` | same | MATCH |
| T2 533021.nif | `Gamebryo File Format, Version 10.1.0.0` | same | MATCH |
| T3 496633.nif | `Gamebryo File Format, Version 10.1.0.0` | same | MATCH |
| T4 223534.nif | `NetImmerse File Format, Version 4.1.0.12` | same | MATCH |
| T5 547226.nif | `Gamebryo File Format, Version 10.1.0.0` | same | MATCH |

## 4. Oracle re-runs by QC vs executor's published raw JSONs (item 3)

I ran the tool myself from the repo workdir (python 3.x, same sandbox payload
paths as the executor) with outputs to my QC dir, then SHA-compared against
04_EVIDENCE/T_runs (byte identity ⇒ field identity incl. input_identity,
version_gate, load_result, objects, type_histogram):

| My run | Exit | My SHA256 | vs executor file | Result |
|---|---|---|---|---|
| probe-version T1 --adapter gb12 | 0 | `291B673DC7EF5CBD6294879F4B6F451DBC59B74A13BF5A6CB863B57D75501DF7` | probe_T1_gb12.json | **BYTE_IDENTICAL** |
| probe-version T4 --adapter gb12 | 0 | `C1FEECB12CAEFE76B6438198821B6F609DDCC6CBBB1F6C257738C4F808DE6F2D` | probe_T4_gb12.json | **BYTE_IDENTICAL** |
| probe-version T1 --adapter gb26 | 2 | `02A2FDC327C19DF8EAD1EF5DC9F6473490D4ADCDCE2185D41B776CFDCE5B0DF5` | probe_T1_gb26.json | **BYTE_IDENTICAL** |
| inspect T1 gb12 --full-decode | 2 | `E86AAAB65CFF26FC11E07E81DF403C6E0C26922FC72BD001C3BC0FB0ABDF77B9` | inspect_T1_gb12_full.json | **BYTE_IDENTICAL** |
| inspect T1 gb12 (original-verdict mode) | 2 | `1C40972A42415DD119A93C7E7EBE6F45EBFB76F7FF5C7F3895858E3FB312B7CC` | inspect_T1_gb12_orig.json | **BYTE_IDENTICAL** |
| inspect T4 gb12 --full-decode | 2 | `E1ABCB09221349BC80749B313A527691A31D55C4E3D12D256231FB25E48FD384` | inspect_T4_gb12_full.json | **BYTE_IDENTICAL** |
| inspect T2 gb12 --full-decode | 2 | `D9AF7F4D4A354B6628345868E3CD0EE449DDB799F13DA151C3EDFCFB79554C7F` | inspect_T2_gb12_full.json | **BYTE_IDENTICAL** |

Field-level expectations confirmed in MY outputs (== executor's, byte-identical):
- (c) T1 gb12 original-verdict mode: `load_result.accepted=false`,
  `error="RTTIError(NiArkAnimationExtraData): cannot find create function."`,
  `partial=false`, exit 2 — exactly the required original fail-closed verdict.
- (d) T1 vs gb26 adapter: `REJECTED OLDER_VERSION "NIF version is too old."`
  (10.1.0.0 < floor 10.1.0.114), exit 2 — wrong-version behavior correct.
- Extra beyond the minimum: probe-version T2 gb12 → ACCEPTED, exit 0 (no
  executor counterpart file exists; noted, not required by any gate).

## 5. Negative controls EXECUTED BY QC (item 5)

All controls ran on sandbox COPIES mutated only in my QC temp dir
(C:\Users\User\AppData\Local\Temp\opencode\qc_gb_oracle_r1\) — pinned
payloads untouched (re-verified by the §2 hashes after the control runs).

### 5.1 Corrupted-copy control (a): header version field flip on T2 copy
Copy sha256 `0ED12412D0A2E153BC56E0DE2B9639059BCFF64E70A860AED601D8F4EC7E9A2A`
(4 bytes of the version u32 → 0xFF, 2 following bytes flipped; 6 bytes total).
Result: `nif_version=255.255.255.255`, `accepted=false`, `partial=false`,
`error="LATER_VERSION: Unknown NIF version."`, exit 2 — **REJECTED, never
silent success. CONTROL PASS.**

### 5.2 Corrupted-copy control (a2): mid-file flip on T2 copy (falsifier extra)
Bytes 300-303 → 0xFF. Result: `accepted=false`, `partial=true`, original
verdict `RTTIError(NiArkAnimationExtraData)` preserved, 1 warning, exit 2 — the
load NEVER succeeds. Observation (not a defect): the result is outcome-equal
to the clean-T2 fail-closed verdict because the corrupted bytes fall inside a
closure-derived unknown-run region; the predicate "never silent success" holds
either way. **CONTROL PASS.**

### 5.3 Unknown-class control (b): NiNode → NiQCxo in T2 copy's RTTI table
Copy sha256 `CDB7C75F5757281B7545E4A0D41E59FA5FD9ABE10743036B831DC9709DED9CA8`
(first "NiNode" at offset 57 replaced same-length). Result:
- original-verdict mode: `error="RTTIError(NiQCxo): cannot find create
  function."`, `unknowns=[NiQCxo]`, `accepted=false`, `partial=false`, exit 2;
- full-decode: same RTTIError + NiQCxo listed among unknowns,
  `decode_continued_after_rtti_gate=true`, `partial=true`, exit 2.
**unknown_type REPORTED, not skipped. CONTROL PASS.**

### 5.4 Fail-closed detector list (c) — code-level verification (read to EOF)
s17 detector → implementation pointer (I read the full gb12core.py, 2069 lines):
| Detector | Code pointer (gb12core.py unless noted) | Status |
|---|---|---|
| unknown type | RTTI gate L1417-1449 (RTTIError + unknowns list); legacy walk L1897-1926 | IMPLEMENTED |
| missing factory | same RTTIError path ("cannot find create function" = NO_CREATE_FUNCTION, NiStream.cpp L396-400 cited) | IMPLEMENTED |
| unsupported block | NotSupportedByAdapter raises L1497/L1500 + per-class raises; surfaces as boundary-only records or DECODE_ERROR — never silently skipped | IMPLEMENTED |
| link failure | LINK_FAILURE warning per block/field, L2004-2008 | IMPLEMENTED |
| PostLink failure | classified N/A with source proof — **I verified myself**: NiObjectNET.cpp L656-693 PostLinkObject is extra-data migration only (< 5.0.0.11 list→array + NiVertWeightsExtraData removal), zero byte consumption, no load-failure path | N/A JUSTIFIED |
| partial scene | partial=true + decode_continued_after_rtti_gate L1452/L1931; L2036-2037 accepted=false | IMPLEMENTED |
| exception | DecodeError→NOT_NIF_FILE/DECODE_ERROR error JSON (L1346-1358, L1962-1967); oracle.py exit codes 0/2/3 (nonzero on failure) | IMPLEMENTED |
| object-count mismatch | object_count_check + OBJECT_COUNT_MISMATCH L2018-2028; INVALID_TYPE_INDEX L1398-1407 (source assert L440) | IMPLEMENTED |

Note on "exception": arbitrary non-DecodeError exceptions propagate as a
Python traceback with nonzero exit (no error JSON); all decode-logic failure
classes are mapped to explicit error JSON. Acceptable; not a silent-success path.

## 6. Raw vs wrapper (item 4)

Spot-verified from the raw JSONs (all values identical in the wrapper docs):

| Claim | Wrapper location | Raw evidence | Result |
|---|---|---|---|
| T1 block count 66 (66/66) | FINAL_REPORT Q19; 218757_NIF_RESULT | inspect_T1_gb12_full.json: num_blocks_from_header=66, objects=66, object_count_check.match=true | MATCH |
| T1 root NiNode "Scene Root", zero/identity local transform | Q20; 218757_NIF_RESULT L26 | root index 0: name "Scene Root", translate [0,0,0], rotate identity, scale 1.0 | MATCH |
| T1 NiArk* unknown list (4 classes) | Q24; 218757_NIF_RESULT L32 | unknown_block_classes = NiArkAnimationExtraData, NiArkImporterExtraData, NiArkTextureExtraData, NiArkViewportInfoExtraData | MATCH |
| T1 histogram (NiNode 12, NiTriShape 14, …19 properties, 2 lights, 27 edges) | Q20 | type_histogram + edges_len=27 in raw | MATCH |
| T1 comparison 13 MATCH / 4 MISMATCH / 1 NA_IN_OUR / 1 SEMANTICALLY_UNRESOLVED | Q23; 218757_NIF_RESULT L56 | compare_T1.json summary.counts identical; items: names/local_transforms/bounding_volumes MISMATCH with both raw value sets recorded; parse_failures MISMATCH with explicit BY-DESIGN note; world_transforms SEMANTICALLY_UNRESOLVED (KeyError(0) recorded); unknown_blocks NOT_AVAILABLE_IN_OUR_DECODER | MATCH |
| Dimensions GAME_UNITS only, radii 525..1795, translations ~1030 y / 820 z | Q21 (PLAUSIBLE, derived) | raw model_bound radii 525.069/1795.306; serialized translations -1030.0/820.0 | MATCH (correctly not overclaimed) |
| WORLD_PLACEMENT_EVIDENCE = NO_WORLD_PLACEMENT_EVIDENCE_FOUND; root transform never promoted | Q22; 218757_NIF_RESULT G-218757-2 | raw root transform zero; no world bound serialized | MATCH |
| Matrix gb12 row cells | GAMEBRYO_COMPATIBILITY_MATRIX.csv row 2 | my re-runs + T_runs JSONs (gate ACCEPTS + RTTIError; T4 10/10; T1/T2/T5 closure; bit-exact transforms; model spheres only) | CONSISTENT |
| Matrix gb26 row cells | row 7 | probe_T1_gb26 REJECTED OLDER_VERSION (byte-identical to my re-run); NiStream.cpp min 10.1.0.114 (hash-verified) | CONSISTENT |
| Matrix gb112 rows | rows 5-6 | sgp_T1_dialog.txt verbatim timelock (hash == E3 pin); matrix "FAIL (BLOCKED_EVALUATION_TIMELOCK_EXPIRED)" consistent | CONSISTENT |
| Matrix OUR_TOOL row (incl. T3 448/1288 context in NOT_CHECKED) | row 10 | inspect_T3_gb12_full.json: 1288 header, 448 decoded, 840 null, warning "closure search budget exhausted", partial=true | CONSISTENT |
| compare_T4 (our decoder fails T4 by design) | TEST_MATRIX OUR_DECODER_T4 FAIL-BY-DESIGN | our_T4.json: accepted=false "ArkBlockError: not 10.1", blocks empty; compare_T4 block_count MISMATCH(10 vs null) + parse_failures BY-DESIGN note | MATCH (honest) |

The summary never exceeds the raw anywhere I checked. Float policy declared
("serialized fields bit-exact; … no tolerance applied") — no widened tolerance.

## 7. Proprietary-content census (item 6)

- Package (docs/audits/PE_GAMEBRYO_ORACLE_TOOL_R1_20261003): **71 files** —
  6 csv, 35 json, 20 md, 1 ps1, 5 py, 4 txt. Zero binaries, zero Gamebryo
  source bytes, zero NIF/BNT/VFS payload bytes, zero exe/lib/ISO content.
  (Full listing: 05_QC/raw_qc_outputs/package_census.txt)
- Tool tree (tools/gamebryo_oracle): **22 files** — 14 py, 5 **pyc**
  (finding P2-4), 2 json, 1 md. Registry = class-name census only (factual).
- Sandbox (LOCAL_ONLY, outside the repo): holds original tool exes/DLLs
  (SceneGraphPrinter.exe, PhysXNifViewer.exe, VC71/MFC runtimes, GB2.6 SDK
  DLLs), the T payloads, the stock positive-control sample
  (controls\stock_sample_plane.nif) and corrupted control copies — all
  correctly OUTSIDE the repo tree, per contract (j).
- Git state: both run paths UNTRACKED (`??`), HEAD == BASE_SHA
  `f33c7b9c201b02b8e0f8c7010275b6217475b5a4` — no premature staging, no
  executor git operations (consistent with PUSH_STATUS=NO_GIT_OPERATIONS).

## 8. Determinism + wall-clock (item 7)

Executor determinism pairs re-hashed by me (all **byte-identical**):
T1 `E86AAAB6…`, T2 `D9AF7F4D…`, T3 `B4F5A55A7FA9BDC769B24108FCE120CAB0FFCDC75FE00FFD2FB6F2F1F4A281E7`,
T4 `E1ABCB09…`, T5 `BA3D25E1…`. My own T4 double run: byte-identical
(`E1ABCB09…`). Date-pattern grep (`20\d\d-[01]\d-[0-3]\d`) over ALL
04_EVIDENCE/T_runs JSON bodies: **0 hits**. G-TOOL-2 CONFIRMED.
(Observation, not a defect: probe-version outputs have no published pairs —
inspect mode is the used comparison path; probe is a pure function of the
header bytes; TEST_MATRIX documents the determinism rows via inspect pairs.)

## 9. Selection lock order + R6 erratum (item 8)

- SELECTION_LOCK.json `selection_lock_sha256` = `4A67C6B844B6DA65DF403AA5B87B8012FECB7CBBF60051422E306E93C733381C`
  == my independent SHA256 of the current SELECTION.md (9,954 B ==
  locked_file_bytes; LWT 08:48:23 precedes lock write 08:48:29).
- Lock creation/LWT 2026-10-03 08:48:29 (locked_utc 15:48:29Z, consistent
  UTC-7) **precedes** every oracle-output timestamp: earliest T_runs
  LastWriteTime 09:08:14 (probe files); the bulk CreationTime 09:49:56 on 30
  T_runs files is a copy artifact — LastWriteTime (preserved on copy) shows the
  true order. G-SEL-1 lock-before-first-oracle-run VERIFIED (both metrics).
- SELECTION.md T1-T5 rows match my independent payload hashes and my raw
  header reads; T1 num_blocks=66, T2/T5=6, T3=1,288, T4=10 — all confirmed in
  the raw oracle JSONs. Mechanical rules + tie-breaks recorded; R6 erratum
  exists in RETRACTIONS_SUPERSESSIONS.md **EXACTLY ONCE** (1 line with "R6",
  1 line with "948", exactly 1 "Batch E2 additions" block — E3 dedupe
  verified), stating the 3-way 948 B tie
  (223739/223754/223534, all num_blocks 10) with outcome unchanged. RETRACTIONS
  file hash == E3 pin. G-SEL-2 structure verified (EXTRACT_PROVENANCE.json
  carries all 5 payload pins + Models.bnt pin).

## 10. Gate predicates vs artifacts (item 9)

| Gate | Claimed | QC verification | Verdict |
|---|---|---|---|
| G-TOOL-1 | PASS | tool tree + 2 schemas + 5 adapters + tests + README exist; s8-minimum JSON confirmed by my re-runs | PASS |
| G-TOOL-2 | PASS (E2+E3) | §8 — all 5 pairs byte-identical, 0 wall-clock | PASS |
| G-TOOL-3 | PASS | substance CONFIRMED by my own control re-execution + code pointers (§5); BUT 5 mutation controls have no persisted raw output (finding P1-1) | PASS-substance / P1-1 |
| G-TOOL-4 | PASS | every JSON I examined carries ORACLE_MODE (gb12/gb23 = SOURCE_DERIVED, gb112 = ORIGINAL_TOOL_EXECUTION, compare = MIXED), oracle.gamebryo_version, loader_identity, loader_source_identity(file+sha256), tool_version; SOURCE_DERIVED never phrased as original; gb112 records honestly error=NOT_TESTED/ORIGINAL_TOOL_OBSERVATION | PASS |
| G-SEL-1/2 | PASS | §9 | PASS |
| G-CMP-1 | PASS | 19 items per T; decoder identity pinned (FIELD_IDENTITY_V2 lineage + script SHA256s in our_T1.json); float policy declared | PASS |
| G-CMP-2 | PASS | all 4 T1 MISMATCH carry explanations (representation artifacts with both raw value sets; parse_failures BY-DESIGN note); world_transforms SEMANTICALLY_UNRESOLVED with the recorded KeyError; no tolerance widened | PASS |
| G-218757-1 | PASS | full s13 list + s10 classification + 4 explicit questions with statuses (CONFIRMED/REJECTED/UNVERIFIED/STRONGLY_SUPPORTED) | PASS |
| G-218757-2 | PASS | NO_WORLD_PLACEMENT_EVIDENCE_FOUND full value; no promotion; no EXE scan | PASS |
| G-MATRIX-1 | PASS | zero blank cells CONFIRMED (programmatic count); but 2 malformed CSV rows (P2-1), closed-set annotation deviations (P2-2) | PASS-substance / P2-1, P2-2 |
| G-PKG-1 | PARTIAL | honest — MANIFEST + staging correctly pending (MANIFEST absent) | consistent |
| G-VER-2 | PARTIAL | honest per-version executed columns (gb112 timelock; gb26 never reaches load; gb23 NOT_TESTED) | consistent |
| G-SIG-1 | PASS (E3) | 8 signatures, per-version source identity, closed confidence vocabulary; exe_matching = "NONE_PERFORMED"; NOT_AVAILABLE disclosures; hash == E3 pin | PASS |
| G-PAYLOAD-1 | executor-side PASS | my census agrees (§7); staging check remains persistence-phase step 7 | consistent |

## 11. Pin reconciliations (item 10)

- **P1** — I read Gb12 NiStream.cpp L42-46 myself: `ms_uiNifMinVersion =
  GetVersion(3,3,0,11)`, `ms_uiNifMaxVersion = GetVersion(NIF_MAJOR_VERSION,
  NIF_MINOR_VERSION, NIF_PATCH_VERSION, NIF_INTERNAL_VERSION)` (= 10.2.0.0 via
  NiVersion.h macros). The R1 wording supersession (constant DEFINED at
  NiStream.cpp:44-46, not NiVersion.h) reproduces. File hash MATCH.
- **P2** — NiObject.cpp L134-143 read myself: GroupID u32 iff
  `5.0.0.6 <= v < 10.1.0.114` — exactly the gb12core V_GROUPID_LO/HI gate.
  Hash `B137FE42…` MATCH.
- **P4** — GB112 NiMain.lib located at `D:\gamebyroengine\Gamebryo 1.1.2
  Evaluation\SDK\Win32\Lib\VC71\ReleaseLib\NiMain.lib` (top-level corpus dir,
  sibling of extracted\), re-hashed by me:
  `FF4519AFD2475D9A6E71A35E5DB6B0F5A0B7E9E86EC3662C6A340DA19BA06597`,
  3,073,590 B — **exact match** to the SOURCE_ORACLE_INDEX pin and the R4
  non-retraction. CONFIRMED.
- **R6** — exactly once, 3-way 948 B tie stated (§9).
- **R7** — gui_attempts_log.txt (startup, mainTitle='Settings'), log2 (OK
  clicked → "EGB_SHADER_LIBRARY_PATH environment variable not found"), log3
  (env set → "Failed to load shader library!") — the full chain is present and
  consistent with R7/matrix row 8; PhysXNifViewer sha `4543B4B5…` recorded in
  the log header == BATCH_E2 census pin. CONFIRMED (with encoding finding
  P2-3: logs 1/2 are UTF-16LE).
- **R8** — sgp_T1_dialog.txt: plain UTF-8, no BOM, verbatim "The supplied
  Gamebryo timelock (8469DD85B0554A49, Internal) has expired" present, title
  "NetImmerse Evaluation Copy" present, hash == E3 pin. CONFIRMED.
- **PostLink N/A classification** — source-verified by me (§5.4). CONFIRMED.

## 12. 30-question completeness (item 11)

FINAL_REPORT.md answers ALL 30 order questions, numbered Q1..Q30, each with an
explicit evidence status ([CONFIRMED]/[NOT_TESTED — honest]/[PLAUSIBLE
(derived)]/[PARTIAL — see Q24]/[HONEST]) and deliverable pointers consistent
with the RUN_CONTRACT (m) map. No missing answer; no vague answer found. Q4
(build) honestly NOT_TESTED; Q21 correctly scoped as derived/PLAUSIBLE with
GAME_UNITS only. PASS.

## 13. Honest-negative audit (item 12)

Every known negative is recorded AS a negative in every layer I checked:
- Our-decoder failures: T2/T5 EOF error, T3 closure cap, T4 by-design
  10.1-specialist — TEST_MATRIX rows OUR_DECODER_* = FAIL/FAIL-BY-DESIGN;
  compare_T2/T3/T5 = 0 MATCH with 18× NOT_AVAILABLE_IN_OUR_DECODER (no
  manufactured values); FINAL_REPORT Q24(c)/Q25 LOWER proposals; NOT_CHECKED
  E2 item 6.
- T3 oracle honest PARTIAL: 448/1288 decoded, 840 null, warning "closure
  search budget exhausted" — verified in the raw JSON myself (§6);
  FINAL_REPORT Q26 "ADVANCED ... but ... honest PARTIAL"; HANDOFF terminal
  "GB_1_2: PARTIAL-THEN-FAIL ... T3 NOT EOF-exact"; NOT_CHECKED E3 items 1-2.
- Tool blockers: GB 1.1.2 timelock (BLOCKED_EVALUATION_TIMELOCK_EXPIRED), GB
  2.6 shader-library chain (load never reached), GB 1.2 prebuits no observable
  output — all PARTIAL/NOT_DETERMINED, never converted to success.
- No silent skip found anywhere (grep + full reads). Per order s29: **no
  reclassification required; the QC_FAIL trigger does not fire.**

## 14. FINDINGS (for PE-MASTER to order; QC does not modify executor artifacts)

**[P1-1] G-TOOL-3 evidence-pointer gap: the 5 mutation controls have no persisted raw outputs.**
- Exact source: tools/gamebryo_oracle/tests/test_gb12.py (controls executed
  IN-MEMORY: paths `<synthetic>`, `<mutated-unknown-class>`,
  `<corrupted-header-version>`, `<corrupted-midfile>`, `<count-mismatch>`,
  `<link-failure>`); 03_TOOL/FAIL_CLOSED_TESTS.md ("raw outputs: 04_EVIDENCE/
  T_runs + test stdout in this batch's execution log" — no stdout file exists
  in the package or sandbox; my census found none);
  00_CONTROL/STAGE_ACCEPTANCE_GATES.csv row G-TOOL-3 ("04_EVIDENCE/T_runs
  control outputs") vs RUN_CONTRACT (d) G-TOOL-3 ("Raw outputs of all controls
  stored in 04_EVIDENCE").
- Contradicted: the evidence pointer implies all control raw outputs are in
  04_EVIDENCE; T_runs holds the T-corpus-level control outputs (wrong-version
  gb26 probe, positive stock sample, partial-load full-decodes, original-
  verdict RTTIError records) but NOT the 5 mutation-control outputs
  (corrupted-header/midfile, NiXyzzyx, count+5, link 0xFFFFFFFE, synthetic
  wrong-version).
- Effect: the fail-closed SUBSTANCE is not in doubt — my QC re-execution of 3
  of the 5 (corrupted-version → LATER_VERSION REJECTED exit 2; mid-file → never
  accepted; NiQCxo → RTTIError reported) reproduces fail-closed behavior, and
  the control code is committed — but the gate's evidence letter is partially
  unmet and the battery's pass/exit codes are not machine-checkable from the
  package alone.
- Narrow correction (persistence still pending, so cheap): PE-MASTER orders a
  small correction/evidence action: run `python tests/test_gb12.py --self` and
  the payload battery on a sandbox copy, persist stdout + exit codes (and per-
  control result JSONs) into 04_EVIDENCE, update the FAIL_CLOSED_TESTS pointer,
  or record my QC re-execution outputs (now copied to 05_QC/raw_qc_outputs/)
  as the independent raw evidence with pointers.
- Revalidation predicate: every FAIL_CLOSED_TESTS row points to a persisted
  raw output file (package or 05_QC) with tool+input identity + exit code.

**[P2-1] GAMEBRYO_COMPATIBILITY_MATRIX.csv: 2 malformed CSV rows (machine-readability, L10).**
- Exact source: 03_TOOL/GAMEBRYO_COMPATIBILITY_MATRIX.csv rows 5 (GB_1_1_2
  SceneGraphPrinter) and 8 (GB_2_6 PhysXNifViewer): the NOTES cells contain
  `8469DD85B0554A49\, Internal)` — a backslash-escaped comma inside an unquoted
  CSV field is not valid CSV; `csv.reader`/`Import-Csv` parse those rows as 15
  fields (header = 14).
- Effect: machine parsing misaligns rows 5/8 (my programmatic blank-cell check
  had to tolerate the extra cells); the human-readable content is correct.
- Narrow correction: re-emit the file with proper CSV quoting (double-quoted
  fields containing commas) before MANIFEST/staging.
- Revalidation: `csv.reader` yields exactly 14 fields for all 9 data rows.

**[P2-2] Matrix closed-set deviations + gate annotation mismatch.**
- Exact source: row 10 CUSTOM_ARK_BLOCKS = `FAIL-BY-DESIGN` (token outside the
  s16 set {PASS,PARTIAL,FAIL,NOT_TESTED,UNKNOWN}); rows 2/7 BUILDS =
  `NOT_APPLICABLE (reimplementation)` (outside the s16 set; RUN_CONTRACT (f)
  vocabulary has NOT_AVAILABLE, not NOT_APPLICABLE); STAGE_ACCEPTANCE_GATES
  G-MATRIX-1 row says "13 columns per s16" while the file and the s16 example
  have 14 columns.
- Effect: minor contract-letter inconsistencies; semantics are accurate.
- Narrow correction: re-label cells as closed-set tokens with parenthetical
  annotations (e.g. `FAIL (by design ...)` / `NOT_AVAILABLE (pure-python
  reimplementation; no build step)`); fix the column-count annotation to 14.
- Revalidation: programmatic closed-set check = 0 outside tokens.

**[P2-3] gui_attempts_log.txt and gui_attempts_log2.txt are UTF-16LE (published-evidence readability).**
- Exact source: 04_EVIDENCE/gui_attempts_log.txt (18,404 B, UTF-16LE),
  gui_attempts_log2.txt (7,922 B, UTF-16LE); log3 is UTF-8-sig.
- Contradicted context: the E3 batch itself identified and fixed this exact
  defect class for sgp_T1_dialog.txt ("was UTF-16LE+BOM from a PowerShell 5.1
  redirect") but converted only that one file.
- Effect: the R7 chain IS fully present (verified by me with correct decoding)
  but invisible to naive UTF-8 tooling (grep over the evidence dir misses it).
- Narrow correction: convert both files verbatim to plain UTF-8 with the same
  one-line conversion header precedent (content byte-preserved), then re-hash
  and note the change; do BEFORE MANIFEST/staging.
- Revalidation: both files decode as UTF-8; R7 chain greppable; new SHA256
  recorded wherever pinned.

**[P2-4] 5 .pyc files (__pycache__) inside tools/gamebryo_oracle.**
- Exact source: adapters/gb12/__pycache__/*.pyc (3), adapters/compare/__pycache__/*.pyc
  (1), __pycache__/gb12core.cpython-312.pyc (1).
- Effect: derived binary artifacts of OUR code (not proprietary; zero payload
  risk) would enter the G-PAYLOAD-1 committed-path census ("run package +
  tools/gamebryo_oracle + AUDIT_ENTRYPOINT.md ONLY") and contradict the
  expected text-only tree; repo hygiene.
- Narrow correction: delete the __pycache__ directories before staging (and
  exclude from the staged set; the persistence worker's staged-set
  verification covers this).
- Revalidation: staged tree contains zero .pyc files.

**[P2-5] TEST_MATRIX.csv is an E2 snapshot (stale rows vs the E3 state, L14).**
- Exact source: 03_TOOL/TEST_MATRIX.csv row T3_full_decode ("wall-cap 480s
  exceeded (~298 registered-but-not-implemented particle classes ...)") and
  row G_SIG_signatures ("NOT_TESTED, budget exhausted") — both superseded by
  E3 (≈25 classes implemented; 448/1288 with S_B-phase stop; G-SIG-1 produced
  and PASS in the E3 gate rows + GAMEBRYO_SEMANTIC_SIGNATURES.json).
- Effect: a reader taking TEST_MATRIX.csv as the current state gets the E2
  stop reason and the stale G-SIG status; the batch-tagged gates CSV and
  NOT_CHECKED E3 section disambiguate, but the file carries no batch qualifier.
- Narrow correction: add an E3 note/superseding rows (or a header line marking
  it an E2 snapshot with E3 deltas recorded in STAGE_ACCEPTANCE_GATES.csv)
  before MANIFEST/staging.
- Revalidation: no package file states a superseded stop reason as current
  without a batch qualifier.

Non-finding observations (recorded, no action required):
- No probe-version determinism pairs are published (inspect-mode pairs cover
  the used comparison path; probe is a pure header function).
- No probe_T2_gb12.json exists in T_runs (probes published for T1/T4 only; my
  T2 probe is preserved in 05_QC/raw_qc_outputs/).
- The T_runs bulk CreationTime (09:49:56) is a copy artifact; LastWriteTime
  preserves the true oracle-output order (earliest 09:08:14 > lock 08:48:29).
- Mid-file corruption inside a closure-derived unknown-run region yields the
  same fail-closed verdict as the clean file (the predicate "never silent
  success" holds; noting for future control design — corrupt bytes inside
  unknown runs are not independently detectable by boundary closure alone).

## 15. QC NOT_CHECKED (explicit; none load-bearing for the verified verdicts)

1. Models.bnt (395,412,868 B) not re-hashed by QC — the 5 payload hashes match
   the task-pinned expectations (manifest lineage), SELECTION_LOCK records
   pin_match=true, EXTRACT_PROVENANCE carries the pin; MISSING here does not
   affect the verified claims.
2. T3 oracle not re-run by QC (budget; the determinism pair re-hash-verified
   byte-identical and the 448/840/1288 + warning fields verified in the raw
   JSON directly).
3. gb112/gb23/compare adapters not executed by QC (code read + output fields
   verified; gb112 attempt records verified against the dialog evidence).
4. E1 breadth not independently re-audited (G-INV-1..3 census recount,
   TOOLCHAIN_MATRIX 49 rows, VERSION_SUPPORT/NIF_LOAD_PIPELINE/ROSETTA/
   TRANSFORM/BOUNDING docs, PREFLIGHT, RUN_BUDGET, BATCH_E1_RETURN) — treated
   as recorded E1 canon; the load-bearing pins of that canon that this run's
   verdicts rest on (P1/P2/P4, GB112 tree, manifest hash, version gates) were
   verified physically by me.
5. Sandbox binary attempt tree (exes/DLLs) content not forensically analyzed
   (LOCAL_ONLY; identities spot-checked against the recorded census pins).

## 16. FULL_READ_LOG

Read to EOF by QC: RUN_CONTRACT.md; AUTHORIZATION.md; oracle.py; gb12core.py
(2069 L); adapters gb12/gb26 (full), adapters gb112/gb23 (ORACLE_MODE/era
regex-level + gb112 outputs field-level); tests/test_gb12.py;
03_TOOL/FAIL_CLOSED_TESTS.md; 06_REPORT/FINAL_REPORT.md;
02_ANALYSIS/218757_NIF_RESULT.md; RETRACTIONS_SUPERSESSIONS.md; NOT_CHECKED.md;
06_REPORT/HANDOFF.md; 04_EVIDENCE/BATCH_E2_RETURN.md; BATCH_E3_RETURN.md;
00_CONTROL/SELECTION.md; SELECTION_LOCK.json; STAGE_ACCEPTANCE_GATES.csv;
TEST_MATRIX.csv; GAMEBRYO_COMPATIBILITY_MATRIX.csv (parsed programmatically);
T_runs compare_T1..T5.json (summary + targeted items), our_T1/our_T4.json,
inspect_T1/T2/T4/T5_gb12_full.json + inspect_T1_gb12_orig.json (targeted
fields), inspect_T3_gb12_full.json (content fields), probe JSONs,
gb112_exec JSONs (fields); EXTRACT_PROVENANCE.json; GAMEBRYO_SEMANTIC_
SIGNATURES.json (structure + binding fields); sgp_T1_dialog.txt (full head +
verbatim check); gui_attempts_log*.txt (encoding detection + targeted chain
grep); SOURCE_ORACLE_INDEX.csv (P4 rows). Source files read: NiStream.cpp
(L40-48), NiObject.cpp (L130-146), NiObjectNET.cpp (L650-695) + hashes.
NOT fully read: the E1 analysis corpus listed in §15.4, VERSION_SUPPORT.md etc.

## 17. Raw QC output pointers

QC workspace: `C:\Users\User\AppData\Local\Temp\opencode\qc_gb_oracle_r1\`
(copies of the raw QC outputs are persisted INSIDE the package at
`docs/audits/PE_GAMEBRYO_ORACLE_TOOL_R1_20261003/05_QC/raw_qc_outputs/` —
JSON outputs only, identity metadata, zero payload bytes; mutated control
copies stay in the QC temp dir, LOCAL_ONLY):
- probe_T1_gb12_mine.json / probe_T2_gb12_mine.json / probe_T4_gb12_mine.json /
  probe_T1_gb26_mine.json — my independent probe runs
- inspect_T1_gb12_full_mine.json / inspect_T1_gb12_orig_mine.json /
  inspect_T2_gb12_full_mine.json / inspect_T4_gb12_full_mine.json (+_run2) —
  my independent inspect runs (byte-identical to executor's)
- control_corrupt_version.json / control_corrupt_midfile.json /
  control_unknown_class.json / control_unknown_class_orig.json — my negative
  control raw outputs (P1-1 mitigation evidence)
- package_census.txt / tool_census.txt — full path+size censuses
- qc_compare.py + qc_pins*.py — my verification harnesses (reproducible)

## 18. NEXT_PARENT_ACTION (returned to PE-MASTER)

1. Order the 6 corrections (P1-1, P2-1..P2-5) — all are
   evidence-persistence/hygiene level, executable before MANIFEST/staging; no
   scientific re-run required (QC re-verified the science independently).
2. After corrections: persistence phase per RUN_CONTRACT (o) (MANIFEST LAST,
   bijection verify, path-limited staging — staged set must exclude the
   __pycache__/.pyc and any binary; AUDIT_ENTRYPOINT row; one commit; push;
   three-way verify).
3. Decide the R6/R7/R8 proposals and the E3 G-SIG-1 acceptance (all advisory).
4. Optional future authorization (NOT granted by this QC): T3 S_B-phase
   closure work; compare normalization (nifxml compound representation).

```
QC_VERDICT   = QC_PARTIAL
FINDINGS     = 6 (P1: 1, P2: 5) — none falsifies a scientific result
BLOCKERS     = none (no QC_BLOCKED condition; all checklist items executed)
ADVISORY     = ADVISORY_PRE_QUALIFICATION (Q1 absent; no milestone/canonical effect)
```

---

# RE-QC after C1 (2026-10-03)

```
RE-QC RUN_ID : PE_GAMEBRYO_ORACLE_TOOL_R1_20261003_QC_R1B (targeted resume)
SCOPE        : ONLY the six QC_R1 findings + BATCH_C1_RETURN.md residuals 1-8
               (no new sweep, per dispatch); correction round C1 =
               BATCH_C1_RETURN.md (6 fixes, 8 disclosed residuals)
BUDGET       : 6 tool calls of <= 12; ~12 wall minutes of <= 20
WRITES       : this appendix + 05_QC/raw_qc_outputs/reqc_*.{txt,json}
               (+ one disclosed self-inflicted cleanup, see P2-4 note)
BASELINE     : QC_REPORT.md pre-append sha256 F2E8C434ACFDBFC92926BC98
               D0E4551EFD043FFD8240A5D885497FBFCE347CD4 (C1 did not touch 05_QC)
SELECTION.md : sha256 re-verified = 4A67C6B844B6DA65DF403AA5B87B8012FEC
               B7CBBF60051422E306E93C733381C == lock pin — **C1 DID NOT TOUCH
               THE LOCKED SELECTION** (G-SEL-1 integrity preserved)
```

## Per-finding verdicts

| Finding | C1 fix | QC verification (independent) | Verdict |
|---|---|---|---|
| **P1-1** control raw outputs | FIX-1 | 04_EVIDENCE/controls/ has exactly the 5 JSONs; all 5 SHA256 == C1 pins; each parses and carries all 4 s18 labels (MEASURED_QUANTITY / INDEPENDENT_SOURCE_OF_TRUTH / WHY_NON_CIRCULAR / FAILURE_CASE_DETECTED) + per-payload raw runs; test_gb12.py unchanged (323AAA62…) = the declared verbatim source; FAIL_CLOSED_TESTS.md dated addendum (4B9C574C…) + TOOL_IMPLEMENTATION_REPORT.md C1 note (BF6A79A2…) + STAGE_ACCEPTANCE_GATES.csv G-TOOL-3 row now points to 04_EVIDENCE/controls/ raw mutation-control JSONs (single row; 2C40DF1A…). **Re-execution by QC**: corrupted_header_version control on a fresh T2 sandbox copy (mutation v0^0x00400000, code path per test_gb12.py): my run → nif_version=10.65.0.0, error_code=LATER_VERSION, accepted=false, partial=false — their JSON records the same mutation (0x00400000) + same verdict (LATER_VERSION @ 10.65.0.0): **REPRODUCED** (raw output: reqc_reexec_corrupted_header_version_T2.json). Honest non-detections recorded raw (T1 RTTI-gate stops; STOCK artifacts with MIDFILE_STOCK_NOTE / RUN_NOTE) — no smoothing. | **FIXED** |
| **P2-1** matrix CSV | FIX-2 | csv module parse: header 14 fields, 9 data rows, **all rows exactly 14 fields, zero blank cells, all fields properly quoted**; rows 5/8 dialog/P7 commas preserved verbatim inside quotes; sha == C1 pin 02D72F0A… | **FIXED** |
| **P2-2** closed set | FIX-2 + residual | NOT_APPLICABLE: **absent everywhere**; FAIL-BY-DESIGN: **absent everywhere** (OUR_TOOL CUSTOM_ARK = "FAIL (original verdict RTTIError…)"; BUILDS of the 3 reimplementation rows = NOT_TESTED with reason). BUT the G-MATRIX-1 gates row still reads "13 columns per s16" (14 actual) — C1 left it unchanged as RESIDUAL-4 (not in the assigned fix list, disclosed). (Observation, pre-existing in the E2 version already QC'd, not a new finding: SOURCE_AVAILABLE carries descriptive vocabulary FULL/SOURCE/NO per the s16 example column semantics.) | **PARTIALLY_FIXED** (matrix cells FIXED; gates-row wording NOT corrected — RESIDUAL-4) |
| **P2-3** gui log encoding | FIX-3 | both logs now plain UTF-8, **no FF FE BOM**; sha == C1 pins (986B9E77… / 695FF22B…); spot-compare vs my earlier UTF-16 reads: identical wording ("mainTitle='Settings'" + PhysXNifViewer sha 4543B4B5 header in log1; "EGB_SHADER_LIBRARY_PATH environment variable not found" in log2); log3 untouched (UTF-8 with BOM — RESIDUAL-7, valid UTF-8, readable, never part of the finding) | **FIXED** |
| **P2-4** pycache | FIX-4 | C1 end-state verified: .gitignore present with exactly `__pycache__/` + `*.pyc` (862263FA…). **QC disclosure**: my own re-execution (importing gb12core without -B) recreated 3 transient .pyc (gb12core + gb12 registry/__init__); I removed them and re-censused: **0 .pyc / 0 __pycache__** under tools/gamebryo_oracle (18 source files + .gitignore) — the C1 verified state is restored; the .gitignore additionally protects staging even if recreated | **FIXED** (with QC-side transient recreation, cleaned + disclosed) |
| **P2-5** TEST_MATRIX stale | FIX-5 | sha == C1 pin A5D52F05…; T3_full_decode row now states post-E3 facts (all ~25 classes implemented; honest PARTIAL 448/1288 NOT EOF-exact; residuals pointer; determinism pair B4F5A55A…; ORIGINAL RTTIError unchanged); G_SIG_signatures row = produced in E3 per s28, PASS, GAMEBRYO_SEMANTIC_SIGNATURES.json; E2 honest-FAIL rows untouched | **FIXED** |

## BATCH_C1_RETURN.md residuals 1-8 — persistence-blocking assessment

| # | Residual (verified where checkable) | Blocks persistence? | Class |
|---|---|---|---|
| 1 | gb12core.decode called DIRECTLY (tests path) raised uncaught DecodeError on 2 grossly-corrupted STOCK inputs (fail-closed exception, never silent); oracle.py CLI wrapping not re-verified in C1 | **NO** — matches the nuance QC_R1 already recorded (§5.4 note: non-mapped exceptions surface as nonzero-exit failures, never success); raw outputs persist it; robustness improvement for a FUTURE run | P2 (recordable) |
| 2 | STOCK mid-file mutation stayed structurally valid → accepted=true (verified: MIDFILE_STOCK_NOTE + raw entry in corrupted_midfile.json) | **NO** — correct original-loader behavior for a still-valid file; honestly recorded; structural case DETECTED on T2 (QC parity file exists) | P3 (recordable) |
| 3 | T1 mid-file control not run (wall-risk; honest note in JSON) | **NO** — coverage note; T2 case + QC_R1 T2-parity cover the predicate | P3 (recordable) |
| 4 | G-MATRIX-1 gates row still says "13 columns per s16" (14 actual) | **NO** — cosmetic annotation error in an evidence-pointer cell; the artifact itself now satisfies the gate predicates (14 fields, zero blanks, closed set) | P2 (recordable; recommended fix-in-passing at persistence prep) |
| 5 | gb12 row CONTROLLERS cell annotation stale post-E3 (verified verbatim: "T3 has controllers but its full-decode exceeded budget") | **NO** — stale annotation, disambiguated by gates E3 rows + NOT_CHECKED E3 §1 | P2/P3 (recordable; optional fix-in-passing with #4) |
| 6 | FIX-2 interpretation disclosure (OUR_TOOL BUILDS → NOT_TESTED + reason) | **NO** — transparent, within the finding's intent | P3 (informational) |
| 7 | gui_attempts_log3.txt is UTF-8 WITH BOM (EF BB BF) | **NO** — valid UTF-8, fully readable; never part of P2-3 | P3 (informational) |
| 8 | Process disclosures (persistence-order defect fixed by deterministic re-execution 382→388; c1_verify_annotate NameError patched, post-patch sha not re-printed) | **NO** — the affected artifact (link_failure_mutation.json) hash-matches its C1 pin and carries RUN_NOTE | P3 (recordable) |

**Blocking total: 0 × P0, 0 × P1 — no residual blocks the persistence phase.**

## Updated overall verdict

**QC_PASS.** All six QC_R1 findings are dispositioned (4 FIXED, 1 FIXED with
QC-side disclosure, 1 PARTIALLY_FIXED whose only residue is the disclosed
RESIDUAL-4 wording). The two remaining wording items (RESIDUAL-4 "13 columns"
gates-row annotation; RESIDUAL-5 stale CONTROLLERS cell annotation) and
residuals 1-3, 6-8 are recordable advisories for PE-MASTER (fix-in-passing
optional; no gate predicate, no scientific claim, and no payload-discipline
requirement is violated). MANIFEST/staging may proceed per RUN_CONTRACT (o),
with the persistence worker's staged-set verification (G-PAYLOAD-1) applying
the .gitignore protection and the zero-.pyc census. All verdicts remain
ADVISORY_PRE_QUALIFICATION; MASTER_ACCEPTED and milestone closure remain
PE-MASTER/human decisions.

Raw RE-QC outputs: `05_QC/raw_qc_outputs/reqc_verification_log.txt` (full
verification transcript) + `reqc_reexec_corrupted_header_version_T2.json`
(my independent control re-execution result).
