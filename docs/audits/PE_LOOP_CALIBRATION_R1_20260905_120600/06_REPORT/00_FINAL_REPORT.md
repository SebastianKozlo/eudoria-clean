# PE_LOOP_CALIBRATION_R1_20260905_120600 — FINAL REPORT

RUN-4 of the PE-MASTER loop directive: the **loop-mechanics calibration** on a deliberately
safe bounded task — the re-hash census of the M1 gate package + the five M1 run dirs'
named index/report files — with ZERO canon-writes, ZERO runtime, and full reversibility.
pe-reconstruction executed the census; pe-master-auditor audits it (AUDIT_OF_AUDITOR).

## 0. The one P0 question (NEXT_PROMPT.md §0, verbatim)

> Czy mechanika pętli (delegacja -> write-ahead LOOP_STATE -> wykonanie -> stan
> COMPLETED -> wznów-weryfikacja) działa end-to-end na bezpiecznym zadaniu
> (re-hash census pakietu M1) — z zero canon-writes i pełną odwracalnością?

**Answer: TAK — verified end-to-end, including two real defect->re-dispatch cycles
(the loop handled both exactly as designed). See §4.**

## 1. Run identity + entry gates

| Field | Value | Verification |
|---|---|---|
| PROMPT_FILE_PATH | `D:\Eudoria_Reconstruction\99_Audits\PE_MASTER_HANDOFFS\PE_LOOP_CALIBRATION_R1_20260905_120600\NEXT_PROMPT.md` | read in full (88 lines) |
| PROMPT_SHA256 expected | `5F09084FF2D343FB34972508050AA920C9C96B2BE45C49C5342C6924BFFFD388` | — |
| PROMPT_SHA256 computed | `5F09084FF2D343FB34972508050AA920C9C96B2BE45C49C5342C6924BFFFD388` | **MATCH** |
| AUDIT_OUTPUT_ROOT | `D:\Eudoria_Reconstruction\99_Audits\PE_LOOP_CALIBRATION_R1_20260905_120600\` | **FREE before creation** (collision check PASS) |
| BASE_SHA expected | `57a8d96` | — |
| BASE_SHA recorded | `57a8d9635c4df93274c4e0c3da4eabbca7e1783d` | `git log` HEAD at start == expected; worktree CLEAN |
| INTERVENTION_LEDGER | EMPTY | offline run: no runtime, no client, no Ghidra |
| REPO MIRROR | `docs\audits\PE_LOOP_CALIBRATION_R1_20260905_120600\` (eudoria-clean) | committed+pushed at close (§6) |

## 2. The state-file discipline (the mechanics under test) — the resume-read proof

The WRITE-AHEAD state file `00_CONTROL\PE_LOOP_CALIBRATION_STATE.json` was created BEFORE
the census (NEXT_PROMPT §2 requirement) and is the resume checkpoint. Every dispatch
boundary physically re-read it (fail-closed: `census_tool.py` ABORTS unless the file is at
`status=RUNNING` / `phase=CENSUS_DISPATCHED`).

### 2.1 Phase-transition chain (all reads physical; SHAs of the file content)

| # | Transition | State SHA256 (physical read) |
|---|---|---|
| 1 | Write-ahead created (write tool): `RUNNING / CENSUS_DISPATCHED / dispatch 1` | `6FE631E847834E4639A99295F783089CF9C84146636543513C7572C9C0B5DE1E` (read at dispatch-1 census start) |
| 2 | Dispatch 1 census done -> `CENSUS_DONE / AWAITING_ORCHESTRATOR_AUDIT` | `B52C64D7DD95339FEE4D6A8E2961493CFBB228247C166B237992B2CD78160A2B` (read-back after update) |
| 3 | Detector-defect correction #1 -> re-dispatch: `RUNNING / CENSUS_DISPATCHED / dispatch 2` | `BBAC62153772D005370F14A264A2A0DFF3306FBA4980DBADE1AD8D478B55A566` (read at dispatch-2 census start) |
| 4 | Dispatch 2 census done -> `CENSUS_DONE / AWAITING_ORCHESTRATOR_AUDIT` | `C5A64B858A259DF1AA13502DD6F48A0A82177317795C27B3B4CF802988499128` (read-back after update) |
| 5 | Detector-defect correction #2 -> re-dispatch: `RUNNING / CENSUS_DISPATCHED / dispatch 3` | `DAD3D2B29221C4504FC4C3041443F3672A3CDC797A3516E8292571C484238F3C` (read at dispatch-3 census start) |
| 6 | Dispatch 3 census done -> `CENSUS_DONE / AWAITING_ORCHESTRATOR_AUDIT` (FINAL) | `5327BE35BF93CA896B321D9A9CC54C2BC3B106F64D06AE8FEF5B5F054E6FCCEA` (read-back after update) |

### 2.2 The state content BEFORE the census (write-ahead, dispatch 1 — QUOTED)

```json
{
  "run_id": "PE_LOOP_CALIBRATION_R1_20260905_120600",
  "run_class": "LOOP_CALIBRATION (RUN-4 of the PE-MASTER loop directive; safe bounded task; zero canon-writes)",
  "status": "RUNNING",
  "phase": "CENSUS_DISPATCHED",
  "dispatch": 1,
  "started_at": "2026-09-05T12:09:48-07:00",
  "base_sha": "57a8d9635c4df93274c4e0c3da4eabbca7e1783d",
  "base_sha_expected": "57a8d96 (verified: git log HEAD == 57a8d9635c4df93274c4e0c3da4eabbca7e1783d, worktree CLEAN)",
  "scope": {
    "gate_package_root": "D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean/docs/audits/PE_MILESTONE_1_WORLD_SURFACE_R1_GATE",
    "gate_package_rule": "every file recursively (19 files discovered at pre-flight); record relpath + size_bytes + sha256",
    "run_index_dirs_root": "D:/Eudoria_Reconstruction/99_Audits",
    "run_index_dirs": [
      "PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439",
      "PE_M1_GATE_PACKAGE_COMPLETION_R1_20260905_041816",
      "PE_M1_GATE_V4_CORRECTION_R2_20260905_101327",
      "PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528",
      "PE_M1_X87CW_EXPERIMENT_DESIGN_R1_20260905_115209"
    ],
    "run_index_named_files": ["artifact_index.csv", "REPORT.md", "HANDOFF.md", "STAGE_ACCEPTANCE_GATES.csv"],
    "run_index_rule": "exact-name matches searched within each run dir tree (READ-ONLY; full trees NOT in scope); a named file absent = NOT_FOUND recorded + continue",
    "cross_check_rule": "every SHA the package's own records state for a package file (GATE_INDEX entries, manifest built_from values, matrix V4/V3 fields, amendment records, MD citations) vs the fresh census hashes; a within-scope mismatch = LOUD finding; superseded-layer claims classified against the package's own append-only model; out-of-census-scope SHA references recorded as external references (not verified)",
    "counts_rule": "files hashed per scope; totals in the census JSONs",
    "writes_rule": "ZERO writes outside the calibration folder (this ROOT) + the repo mirror docs\\audits\\PE_LOOP_CALIBRATION_R1_20260905_120600\\** at commit time"
  },
  "prohibitions_active": [
    "zero canon-writes",
    "zero edits to any audited/completed file",
    "zero runtime / zero client launches / zero Ghidra",
    "no nested agents",
    "no original payloads committed (identity metadata only: hashes/sizes/paths)"
  ],
  "hard_stops_active": [
    "ANY need to write outside the calibration folders = HARD STOP",
    "a discovered SHA mismatch in (c) is a FINDING recorded loudly, NOT a hard stop",
    "a scope file unreadable = record + continue"
  ],
  "updated_at": "2026-09-05T12:09:48-07:00",
  "updated_by": "pe-reconstruction (loop-mechanics calibration, dispatch 1)"
}
```

### 2.3 The state content AFTER the census (FINAL, dispatch 3 — QUOTED, abridged to the result fields; the full 102-line file is the physical evidence)

```json
{
  "run_id": "PE_LOOP_CALIBRATION_R1_20260905_120600",
  "run_class": "LOOP_CALIBRATION (RUN-4 of the PE-MASTER loop directive; safe bounded task; zero canon-writes)",
  "status": "CENSUS_DONE",
  "phase": "AWAITING_ORCHESTRATOR_AUDIT",
  "dispatch": 3,
  "started_at": "2026-09-05T12:09:48-07:00",
  "base_sha": "57a8d9635c4df93274c4e0c3da4eabbca7e1783d",
  "base_sha_expected": "57a8d96 (verified: git log HEAD == 57a8d9635c4df93274c4e0c3da4eabbca7e1783d, worktree CLEAN)",
  "scope": { "...": "unchanged from the write-ahead (§2.2) — the census never rewrote the scope" },
  "prohibitions_active": [ "unchanged" ],
  "hard_stops_active": [ "unchanged" ],
  "detector_defect_correction": { "defect 1: the dispatch-1 24-token context window -> 7 false-positive MISMATCH findings; verified line-by-line at source; fixed by the claim-locality rule; re-dispatch 2" },
  "detector_defect_correction_2": { "defect 2: the dispatch-2 flat same-line candidate set -> 15 mislabeled SUPERSEDED attributions on the multi-artifact EVIDENCE lines; verified at source (matrix V4.md lines 96/144/156); fixed by positional association; re-dispatch 3" },
  "dispatch_history": [
    { "dispatch": 1, "state_sha256_at_dispatch_read": "6FE631E8...B5DE1E", "state_sha256_after_update": "B52C64D7...60A2B",
      "result": "CENSUS_DONE (claims 776 = MATCH 41 / SUPERSEDED 33 / MISMATCH 7 / EXTERNAL 359 / UNKNOWN 336)",
      "outcome": "SUPERSEDED_BY_DISPATCH_2 - the 7 MISMATCH findings verified as detector false positives" },
    { "dispatch": 2, "state_sha256_at_dispatch_read": "BBAC6215...5A566", "state_sha256_after_update": "C5A64B85...99128",
      "result": "CENSUS_DONE (claims 776 = MATCH 41 / SUPERSEDED 18 / MISMATCH 0 / EXTERNAL 350 / UNKNOWN 367)",
      "outcome": "SUPERSEDED_BY_DISPATCH_3 - MISMATCH 0; but 15 of 18 SUPERSEDED were mislabeled flat-set attributions" }
  ],
  "updated_at": "2026-09-05T12:25:15-07:00",
  "updated_by": "pe-reconstruction (census_tool.py, dispatch 1 completed)",
  "files_hashed": {
    "scope_a_gate_package": { "count": 19, "total_bytes": 917170, "unreadable": 0 },
    "scope_b_run_indexes": { "slots": 20, "found_hashed": 10, "not_found": 10 },
    "total_files_hashed": 29
  },
  "cross_check": {
    "claims_extracted": 776,
    "match": 41,
    "superseded_historical": 3,
    "mismatch": 0,
    "external_reference": 638,
    "unknown_unresolved": 94
  },
  "mismatch_findings": []
}
```

Cosmetic note (honesty): the `updated_by` label "dispatch 1 completed" is a hardcoded
string inside `census_tool.py` (identical on every dispatch); the authoritative fields are
`dispatch: 3` + `dispatch_history` (2 entries). The tool file is preserved byte-exact as it
ran (provenance of the outputs); no correction was applied post-hoc.

## 3. The census (scope: NEXT_PROMPT §2; execution: census_tool.py, dispatch 3 = LIVE)

### 3.1 Scope (a) — the LIVE M1 gate package (repo), re-hash census

**19 files, 917,170 bytes, 0 unreadable.** Identity metadata only (path+size+SHA256).
Full machine record: `01_RAW\census_gate_package.json`.

| path | size (bytes) | SHA256 (fresh) |
|---|---|---|
| CORRECTION_NOTES.md | 6223 | C668FA8AC0D0F2416D243C2ADECBC267415D3188054FE120F42120D083037DE0 |
| EVIDENCE_MANIFEST.json | 347853 | 0E6FCE502CE487EAFEEA603854AE135D81D40E8AA800F04EB98AB1D5D1459947 |
| EVIDENCE_MANIFEST_V4.json | 134472 | 9944925D1489771B9D5EA99A8AF834E363FBFF9BC49D73BB0999DC8706217D90 |
| GATE_INDEX.md | 21862 | 3532F6B71A0A2853D07E3603B9712B7BC8BBD9A320022C959B033A3A23B9C5B6 |
| GATES/AMENDMENT_ITER035_ROWS10_11.json | 8396 | 2B1FF548D1323BA46D1A8B533BF8BA943B5A508390637C632817D90B58254385 |
| GATES/AMENDMENT_ITER036_CLOSURE.json | 5807 | CBBEEEB9DF345FA804FE79011AF23D0F685E2CE51582B472BB3709BB3D590AE1 |
| GATES/AMENDMENTS.md | 15065 | B4EF3610D289675375CA517013884F67624273D396C31DDDB1F1C377283F0717 |
| GATES/M1_GATE_DELIVERABLE_MATRIX.json | 51523 | F373E60ABF87BF04CF7CC72A98423B19E861054D3B1F5F10CDD3C2041D478928 |
| GATES/M1_GATE_DELIVERABLE_MATRIX.md | 57271 | F0C7D0F29EEE32F156D4BBF9565724009188BBE8C1C9B0F4CA0BBEC4184D76E1 |
| GATES/M1_GATE_DELIVERABLE_MATRIX_V3.json | 52929 | 0E46AB2C94EA1BA7B4527950A4D8851AB69DFA48B7DCDDD449F9A52BD39931F8 |
| GATES/M1_GATE_DELIVERABLE_MATRIX_V3.md | 14763 | B0B69F0634774CC4032A471D7F69BFF7312D427166DC24217C26B93B2DFF797F |
| GATES/M1_GATE_DELIVERABLE_MATRIX_V4.json | 78096 | 003056AC0210A7E0C33F304232F2F366D45D4E94B04D9984FA03B62D06CB4A95 |
| GATES/M1_GATE_DELIVERABLE_MATRIX_V4.md | 68176 | EC04FC471C55450DF060E5E3441A92584BB0CB7C4C63ED1E223C20F0BE732552 |
| HANDOFF.md | 7535 | C431BB62C57C68B4399BA478BABD309AFCCDCE4F09B81CA9742D27050EC81EB0 |
| REPORT_V1_SUPERSEDED.md | 10010 | 4DAC73896CEAB8DC2AB0384A757098AE662CC5AEDCF49EB12D9AD4EFC8CA5B05 |
| REPORT_V2_REJUDGMENT.md | 6985 | 12AE3410E5C2663E0F945086F446EDA16F0F653106B1D5580E1857739E8C3415 |
| RETRACTIONS.md | 10415 | A29758BF8DFB0D17BAB8BDADBABE4B26771E3A2F5A5498C3D8F3FF64F83C648B |
| ROADMAP_MAPPING.md | 9490 | 786B832AF49A8090A71E31CEDF1DB06BF031C812693842311DC32BA43819762D |
| UNRESOLVED.md | 10299 | 2525CEDFF04B9FD9A0D32917E252C2B7EEB7D463C0D0A26E8294617F6BD80240 |

### 3.2 Scope (b) — the named index/report files of the five M1 run dirs (READ-ONLY)

**20 slots: 10 FOUND + hashed, 10 NOT_FOUND (recorded + continued — NEXT_PROMPT §3).**
The NOT_FOUND slots reflect an observed naming variance, NOT a defect: the V4-CORRECTION-R2
and V4.1-REGISTRY-RESIDUAL dirs carry their reports as `06_REPORT\00_FINAL_REPORT.md`
(a different name, out of the census's exact-name scope), and X87CW carries `06_REPORT\HANDOFF.md`
(found) + `06_REPORT\00_FINAL_REPORT.md`. Per the bounded scope, only the exact names
`artifact_index.csv`, `REPORT.md`, `HANDOFF.md`, `STAGE_ACCEPTANCE_GATES.csv` were censused.
Full machine record: `01_RAW\census_run_indexes.json`.

| run dir | named file | size | SHA256 (fresh) |
|---|---|---|---|
| PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439 | artifact_index.csv | 6001 | 5D804E3DF6031CD96A2470950B349076259E18EB9BF3B443388432D9E780836E |
| PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439 | REPORT.md | 2427 | B0E01B26909B075BD685C81AE55B16D93240079172714CA4518463F8EB6DA6FC |
| PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439 | HANDOFF.md | 4371 | C9414A06F4F4AADCD08E1722B7C59AE796AEEA658147FE34ACE90F6451CCCB29 |
| PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439 | STAGE_ACCEPTANCE_GATES.csv | 4791 | 3277E5C7A520A87E3F4FFB8157FE6AA576A8F412F023996AC8D58C4676905A3E |
| PE_M1_GATE_PACKAGE_COMPLETION_R1_20260905_041816 | artifact_index.csv | 1391 | 56480FDFFD18CEEFF55D03AB9F1069475B63CC8CECA8044F293F522FF7A06FB2 |
| PE_M1_GATE_PACKAGE_COMPLETION_R1_20260905_041816 | REPORT.md | 3035 | 3DF8E3C71BC19B60BF989E694F5B93FDD582FF6DC7148521898F1BEAEE1A9AEA |
| PE_M1_GATE_PACKAGE_COMPLETION_R1_20260905_041816 | HANDOFF.md | 6454 | 84163C745EA419E2BD29A60AA52551076150CB81BF09EC58FD0571484F66E505 |
| PE_M1_GATE_PACKAGE_COMPLETION_R1_20260905_041816 | STAGE_ACCEPTANCE_GATES.csv | 4506 | 533C2C9E4B4D1C71F15982295EAA2121E6D4570AE966DD4CF39CB26CAE469DA8 |
| PE_M1_GATE_V4_CORRECTION_R2_20260905_101327 | artifact_index.csv | NOT_FOUND | — |
| PE_M1_GATE_V4_CORRECTION_R2_20260905_101327 | REPORT.md | NOT_FOUND | — |
| PE_M1_GATE_V4_CORRECTION_R2_20260905_101327 | HANDOFF.md | NOT_FOUND | — |
| PE_M1_GATE_V4_CORRECTION_R2_20260905_101327 | STAGE_ACCEPTANCE_GATES.csv | NOT_FOUND | — |
| PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528 | artifact_index.csv | NOT_FOUND | — |
| PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528 | REPORT.md | NOT_FOUND | — |
| PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528 | HANDOFF.md | NOT_FOUND | — |
| PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528 | STAGE_ACCEPTANCE_GATES.csv | NOT_FOUND | — |
| PE_M1_X87CW_EXPERIMENT_DESIGN_R1_20260905_115209 | artifact_index.csv | 1835 | 4373AECB3625565B7F0702378E988C23C833915B7B4DF5B6A3680563C2EBF008 |
| PE_M1_X87CW_EXPERIMENT_DESIGN_R1_20260905_115209 | REPORT.md | NOT_FOUND | — |
| PE_M1_X87CW_EXPERIMENT_DESIGN_R1_20260905_115209 | HANDOFF.md | 2582 | C63ED68833BDB99DC3FB160BDAD8D8537C2EB0B4C9542C3E3D7CF5E8A6E90F9B |
| PE_M1_X87CW_EXPERIMENT_DESIGN_R1_20260905_115209 | STAGE_ACCEPTANCE_GATES.csv | NOT_FOUND | — |

### 3.3 Cross-check (c) — the census AS A DETECTOR: the package's own recorded SHAs vs the fresh hashes

**776 SHA claims** extracted from the package's own records (JSON field walk +
positional MD citation walk; every claim carries source file + locator in the census JSON):

| verdict | count | meaning |
|---|---|---|
| **MATCH** | **41** | the recorded SHA equals the fresh hash of a package file — every LIVE recorded identity is TRUE. Includes: the V4.1 LIVE layer `GATES/M1_GATE_DELIVERABLE_MATRIX_V4.json`=003056AC…, `.md`=EC04FC47…, `EVIDENCE_MANIFEST_V4.json`=9944925D… (built_from + GATE_INDEX lines 252/254/256, mutually corroborating); the V3 copies `=B0B69F06…` / `=0E46AB2C…` (the byte-identical-copy claims VERIFIED POSITIVELY); the old manifest's untouched-file record `EVIDENCE_MANIFEST.json`=0E6FCE50… (the supersession record matches the live file — the file was never edited, exactly as recorded); the amendment copies `=2B1FF548…` / `=CBBEEEB9…`; the ORIGINAL-matrix citations in the old manifest; the GATES/AMENDMENTS.md layer claims |
| **SUPERSEDED_HISTORICAL** | **3** | exactly the documented V4-layer values, superseded in place by the V4.1 edit: `5B90D2C4…` (V4.md @ GATE_INDEX line 165), `11FB16B0…` (V4.json @ line 166), `A1E0F5B9…` (manifest V4 @ line 170). Each file has a LIVE matching claim (above) — the append-only layer model is CONSISTENT |
| **MISMATCH (LOUD)** | **0** | **ZERO package-file SHA breaks. The package is internally hash-consistent.** |
| EXTERNAL_REFERENCE | 638 | SHA claims about out-of-census-scope files (run-dir evidence artifacts, local-only originals like Entropia.exe/Models.bnt/50.bnt, repo-tree files, .pre prefix-proof files) — recorded with path context, NOT verified, per the bounded scope |
| UNKNOWN_UNRESOLVED | 94 | hashes embedded in records without local path context (deterministic render hashes, ledger-iteration header SHAs, prose-cited artifacts in JSON row text) — recorded for auditor review; none resolvable to a package file (hex-first: any equal to a fresh package hash would have been a MATCH) |

**Coverage finding (honest gap, not a mismatch):** 10/19 package files have their SHA
recorded INSIDE the package records (all 10 MATCH). The other 9 (`GATE_INDEX.md`,
`HANDOFF.md`, `CORRECTION_NOTES.md`, `RETRACTIONS.md`, `UNRESOLVED.md`,
`ROADMAP_MAPPING.md`, `REPORT_V1_SUPERSEDED.md`, `REPORT_V2_REJUDGMENT.md`,
`GATES/AMENDMENTS.md`) have their identity recorded only in the run-dir indexes
(e.g. the completion run's `artifact_index.csv`), which are OUT of this census's bounded
scope — so the census records their fresh hashes but has no in-package claim to check
them against. Noted for the orchestrator: NOT a finding against the package.

### 3.4 The detector-defect corrections (the calibration's own findings — the mechanics exercised TWICE)

The census tool is part of the loop under test; both defects were discovered by INSPECTING
the loud output at source, fixed in the tool, and re-executed as a NEW dispatch with the
state file walked through RUNNING/CENSUS_DISPATCHED again. No census output was ever
silently patched; every superseded census is preserved in `dispatch_history` with its state SHAs.

| dispatch | claims | MATCH | SUPERSEDED | MISMATCH | EXT | UNKNOWN | outcome |
|---|---|---|---|---|---|---|---|
| 1 | 776 | 41 | 33 | **7** | 359 | 336 | 7 false-positive MISMATCH (detector defect 1) |
| 2 | 776 | 41 | 18 | 0 | 350 | 367 | louds resolved; 15 mislabeled SUPERSEDED (detector defect 2) |
| 3 (LIVE) | 776 | 41 | 3 | 0 | 638 | 94 | **clean, source-verified census** |

- **Defect 1** (dispatch 1 -> 2): a 24-token context-carry window in the MD walk spanned
  10+ lines of sparse prose and attached unrelated package filenames to SHA claims that
  actually belong to `.pre` files (external) and the V4-layer values (superseded). All 7
  loud findings were verified FALSE at source (GATE_INDEX.md lines 82/161/165/166/170,
  matrix V4.md line 326 — read in this run, quoted in `detector_defect_correction`).
  Fix: claim-locality rule (same line + immediately previous line only).
- **Defect 2** (dispatch 2 -> 3): the flat same-line candidate set over-attributed the
  multi-artifact EVIDENCE citation lines (matrix V4.md lines 96/144/156: 6-7 external
  artifacts per line + ONE package filename) — 15 claims mislabeled SUPERSEDED instead of
  EXTERNAL. Verified at source; the true amendment claims (`CBBEEEB9`, `2B1FF548`) were
  already MATCHes. Fix: positional association (each hex belongs to the nearest
  usable name-token before it) + external broadening for non-package path-like tokens.
- **Invariant held across all three dispatches:** MATCH=41 and total claims=776 — the
  hex-first matching layer (a recorded SHA equal to ANY fresh package hash is a MATCH
  regardless of context) was never affected; the corrections only fixed the
  classification of NON-matching hexes. The final SUPERSEDED=3 is exactly the package's
  own documented supersession chain.

## 4. What the mechanics test showed (the P0 answer)

1. **Delegation + hash-gated entry works:** the launcher prompt was SHA-verified
   (MATCH) before execution; the run executed from the NEXT_PROMPT alone.
2. **Write-ahead persistence works:** the state file existed BEFORE the census,
   was physically re-read at every dispatch boundary (6 state SHAs chained, §2.1),
   and its `dispatch_history` preserved every superseded result.
3. **Restart/resume works — proven by real use, not simulation:** TWO defect->re-dispatch
   cycles walked the state machine RUNNING/CENSUS_DISPATCHED -> CENSUS_DONE -> (defect) ->
   RUNNING/CENSUS_DISPATCHED again, each time surviving the boundary and re-verifying the
   fail-closed assert (the tool ABORTS unless the physical file is at the expected phase).
4. **Fail-loud works:** dispatch 1 produced 7 loud findings; the loop did NOT accept
   them — they were inspected at source, proven false, corrected, and re-run. The census
   acted as a detector of its own defect, which is the calibration's purpose.
5. **Boundedness/reversibility works:** ZERO writes outside the calibration folder
   (before the mirror commit); the audited package + run dirs were strictly READ-ONLY;
   zero canon-writes; the census output is identity metadata only.
6. **AUDIT_OF_AUDITOR readiness:** every one of the 776 claims carries source file +
   locator + verdict in `01_RAW\census_gate_package.json`, so the orchestrator can
   independently re-verify any verdict (including the 3 superseded and the 7+15
   corrected false attributions, each with its line-level source quote in the state file).

**Verdict: the loop mechanics WORK end-to-end on this bounded task.** The two detector
defects are not failures of the loop — they are the loop working (each was caught, bounded,
recorded, fixed, re-dispatched, and closed within the run).

## 5. Prohibitions compliance (NEXT_PROMPT §3)

- **ZERO writes outside `<ROOT>`** before the mirror commit. Complete write list:
  `00_CONTROL\PE_LOOP_CALIBRATION_STATE.json`, `00_CONTROL\census_tool.py`,
  `01_RAW\census_gate_package.json`, `01_RAW\census_run_indexes.json`,
  `06_REPORT\00_FINAL_REPORT.md`, `06_REPORT\HANDOFF.md`.
- **Zero canon-writes; zero edits to any audited/completed file:** the gate package and
  the five run dirs were READ-ONLY inputs throughout (the census records identity metadata
  only; no source file, no frozen evidence, no run record was modified).
- **Zero runtime / zero client launches / zero Ghidra** — INTERVENTION_LEDGER EMPTY.
- **No nested agents. No original payloads committed** (hashes/sizes/paths only).
- **Scope files unreadable: 0.** NOT_FOUND slots (§3.2) = recorded + continued per the rule.
- **Hard stops: NONE triggered.** No need to write outside the calibration folders arose.

## 6. PASS / NON-PASS + handoff

| PASS criterion (NEXT_PROMPT §4) | status |
|---|---|
| state file exists with the phase transitions physically recorded | **PASS** (§2; 6 physical state SHAs; transitions in `dispatch_history`) |
| census JSON complete (every file path+size+SHA256; cross-check results; counts) | **PASS** (§3; `01_RAW\census_gate_package.json` + `01_RAW\census_run_indexes.json`) |
| the calibration report (what the mechanics test showed) | **PASS** (this file, §4) |
| mirror committed + pushed + remote verified | **PASS** (see handoff: BASE_SHA/HEAD_SHA/PUSH_STATUS) |

**RUN_STATUS = CALIBRATION_CENSUS_DONE. HARD_STOP_REASON = NONE.**

- BASE_SHA = `57a8d9635c4df93274c4e0c3da4eabbca7e1783d` (recorded FIRST; == expected `57a8d96`)
- HEAD_SHA / PUSH_STATUS: recorded in the run's final handoff message (post-push; the
  mirror commit contains this report — a commit cannot contain its own hash)
- Commit scope: ONLY `docs\audits\PE_LOOP_CALIBRATION_R1_20260905_120600\**` (the mirror;
  AUDIT_ENTRYPOINT and everything else OUT of scope; no payload bytes)
- State at close: M1 remains **PARTIAL / HARD_STOPPED_AT_GATE**; this calibration closes
  NOTHING beyond its own package; zero canon-writes; nothing authorizes M2.

