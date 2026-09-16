# PROGRESS_STATE — PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915

## FINAL STATE (executor phase COMPLETE — 2026-09-15)

- RUN_STATUS: COMPLETE (G0–G15 PASS; G16–G18 PENDING_LATER_PHASE by design)
- HARD_STOP: YES (executor phase ends; no parser correction, no M2, no
  persistence by executor — no git add/commit/push performed; git status
  verified: only this package untracked + 2 pre-existing roots untouched;
  HEAD == BASE_SHA unchanged)
- Package at executor freeze: 45 physical files including
  00_CONTROL/scripts/__pycache__/ with 5 .pyc build artifacts (scripts
  s01-s06; NOT evidence; excluded from MANIFEST by s10's .pyc filter, but
  physically present — contradicting the earlier "no __pycache__" wording).
  QC AMEND-003 removed __pycache__; post-cleanup package = 40 files
  (MANIFEST 39 rows + MANIFEST_SHA256.csv itself); 0 missing/stale.
  QC_AUDIT.md added later phase (AMEND-004+); PRE_EDIT snapshots under
  00_CONTROL/PRE_EDIT/. See AMEND_LOG_R1.md for all QC amendments.
- All deliverables: 00_CONTROL (contract, registry, findings F-01..F-13,
  amend log, scripts s01-s10, SCRIPT_SHA256), 01_RAW (census, failures=0,
  baseline table, field validation, holdout, negative controls, conflicts
  raw), 02_ANALYSIS (baseline spec, coverage, extension matrix, negative
  set, world slice, Rosetta, parser gap, live doc impact, conflict matrix),
  03_EVIDENCE (README + index), 06_REPORT (REPORT, HANDOFF, gates,
  MANIFEST).
- Local heavy work: D:\Eudoria_Reconstruction\99_Audits\PE_935_NIF_10_1_
  BASELINE_ROSETTA_R1_20260915\02_WORK\ (version JSONs, histograms,
  validation JSON, crosschecks).

## Load-bearing numbers (for QC re-derivation)

- Models.bnt: 395,412,868 B; SHA256 C950A8C2...BEE0 (S0 pin match)
- Census: 5,596 entries; 4,838×10.1.0.0 + 757×4.1.0.12 + 1×4.0.0.2; 0 fail
- Types: 76 observed (v10.1); 364,062 blocks; 425 baseline-applicable;
  349 not-observed
- Closure: 2,363 slice files; TRAIN 1,876/1,890; HOLDOUT 467/473;
  hypothesis_sha 6DB2F1E37E900A2573FEE07B5945B5E25B438066EA0A26AF0841540C96693752
- Parser manifest cross-check: 4,838/4,838 MATCH; NC controls 4+4 executed
- Cross-publisher: EE2 lodtest.nif CLOSURE_OK with frozen layouts

## Stage log (abridged — full details in prior revisions of this file and FINDINGS_LOG)

- S0 PIN: PASS (2026-09-15)
- §1 recount: PASS — exact match 5596/4838/757/1 (s01/s02)
- §3 knowledge base read: COMPLETE (docs/nif/README+01..11)
- §4 oracles pinned: 16 sources (SOURCE_REGISTRY.md); engine-source
  framing discovery (GroupID/TopObjects; F-02/F-03)
- §5 baseline: 10,890 field rows; 425 applicable types (s04)
- §6 census: 4838/4838, 76 types (s03); G2 cross-check 4838/4838 MATCH
- §8/§9: closure decoder s06 (bugs fixed on TRAIN pre-freeze; AMEND-002);
  evidence: F-07..F-10
- §10 holdout: frozen hypothesis; TRAIN 99.3% / HOLDOUT 98.7% (s07)
- §14: EE2 closure PASS (s08)
- §7/§11/§12/§13 matrices: s09
- §15 parser audit: NifModelReader.js REPORT-ONLY (F-13)
- §16/§17: WORLD_VIEWER_MINIMUM_NIF_SLICE.md + NIF_10_1_ROSETTA_BASELINE.md
- Gates: STAGE_ACCEPTANCE_GATES.csv (G0–G15 PASS)
- Provenance: s10 canonical order; rehash clean

## Historical stage note (superseded by FINAL STATE above — kept for the log)

- The section below this line is the mid-run snapshot (§8/§9/§10 phase)
  recorded while the decoder was being developed. It is NOT the current
  state: the executor phase COMPLETED (see FINAL STATE at the top and
  STAGE_ACCEPTANCE_GATES.csv). Retained verbatim for the stage log only.

## Stage snapshot (mid-run, 2026-09-15 — HISTORICAL, superseded)
- STAGE: §8/§9/§10 IN PROGRESS — s06 decoder achieves FULL-FILE CLOSURE on smoke sample (5/5: 505775/505813/508854/508947/505007). Running s07 full validation (2363 candidate files, TRAIN 80% / HOLDOUT 20% by SHA, 505775 forced to TRAIN as discovery file).
- STATUS: healthy. MAJOR physical findings so far (see FINDINGS_LOG.md F-07..F-09 to write): importer tail=41B (schema 13B+7f32 CONFIRMED, wiki 38B WRONG at pad width), ArkTexture count=(field2>>8)&0xFFFFFF CONFIRMED independently, V10_BASE_0B anim = 4 ints + 0B ext.
- Decoder bugs fixed during development (all in TRAIN file 505775): cond/vercond conflation, bool-vs-int eval return, arr2 not stored, name-dedup dropping applicable version-duplicates, dangling cond semantics (absent field → false).
- NEXT ACTION: s07 TRAIN run → freeze → HOLDOUT run → HOLDOUT_RESULTS.csv → §7 classification → matrices (§11-13) → parser audit (§15) → world slice (§16) + Rosetta (§17) → gates/reports.

## s07 invocation
python 00_CONTROL/scripts/s07_full_validation.py train   (then: hold)
Outputs: 99_Audits\PE_935_..._R1_20260915\02_WORK\WORLD_SLICE_VALIDATION.json (merged per-run; runs append subsets — the file is overwritten per invocation; run 'train' first, then 'hold', then merge manually if needed)

## Key facts for resume (do not re-derive)
- BNT2 layout verified: footer DirOffset+BNT2 @EOF-8; NumEntries u32 @DirOffset (=5596); entry = name+0x0A+16B{size,offset,field_c,field_d}; I1 EOF-exact: last entry ends at filesize-8; entry payload bounds [0, DirOffset).
- 10.1.0.0 header (engine-confirmed): line("Gamebryo...10.1.0.0\n") + Version u32 + UserVersion u32 + NumBlocks u32 + u16 NumBlockTypes + NBT×SizedString + u16[type]×NumBlocks + u32 NumGroups + u32[NumGroups] + per-block u32 GroupID + block fields ... + u32 NumTopObjects + u32 LinkID×N at file end.
- 4.x header: line + version u32 + NumBlocks u32 + inline block types (no table, no GroupID).
- External oracles: see 00_CONTROL/FINDINGS_LOG.md F-04. Engine source: D:\gamebyroengine\extracted\Gb12_Source\CoreLibs\NiMain\NiStream.cpp.
- Scripts planned: s01_bnt2_walk.py, s02_nif_version_scan.py, s03_type_census.py (10.1 only), s04 field validators, s05 holdout, s06 negative controls.

## Stage log
- S0 PIN: PASS (2026-09-15). HEAD=f3a3d401f1f254f32cee072260fdc15a6549d378; Models.bnt size=395412868 SHA256=C950A8C2...BEE0 (both match contract pin). Output root clean. Dirty roots pre-existing.
