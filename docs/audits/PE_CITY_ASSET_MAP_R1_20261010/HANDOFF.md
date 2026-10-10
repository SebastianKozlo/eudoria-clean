# HANDOFF.md — PE_CITY_ASSET_MAP_R1_20261010 — FINAL HANDOFF (persistence phase)

RUN_ID = PE_CITY_ASSET_MAP_R1_20261010
PHASE = PERSISTENCE_PUBLISH (contract §8; performed by the pe-master-auditor persistence session)
BASE_FEATURE_SHA = 59641caa1b14ade84e1842ca36b395842deb241e
BRANCH = codex/pe-city-asset-map-r1-20261010
WORKTREE = D:\Eudoria_Reconstruction\12_WebGame\pe-city-asset-map-r1
PRIVATE_OUTPUT = D:\Eudoria_Reconstruction\99_Audits\PE_CITY_ASSET_MAP_R1_20261010 (never committed; referenced by path+SHA256)
DATE = 2026-10-10

## 1. Git state (measured at persistence; discover commands included)

- BASE: worktree created FROM 59641caa1b14ade84e1842ca36b395842deb241e on the new branch;
  old SceneIR worktree untouched at 59641ca throughout.
- ACTUAL_MASTER = 3fbe93eec04759395223e6677b5040273d29222a — local == origin == fresh remote
  (git ls-remote), verified at run start, QC end AND persistence start; NEVER touched (no merge,
  no master push).
- Publication = ONE normal commit of the run's paths on THIS branch only, then
  `git push -u origin codex/pe-city-asset-map-r1-20261010` (no force).
- RESULTING_SHA (discover): `git rev-parse HEAD` in the worktree (the single run commit).
- REMOTE_FEATURE_SHA (discover): `git ls-remote origin refs/heads/codex/pe-city-asset-map-r1-20261010`
  — must equal RESULTING_SHA (the persistence phase verified this equality at push time).
- Foreign reference server: port 8140, PID 21288 (node compat/server-sceneir.mjs, the OLD 218757
  viewer) — alive and untouched at start AND end of this phase. The catalog server refuses 8140 by
  construction.

## 2. Changed-path census (the run's full staged set; allowlist conformance verified)

- MODIFIED (4): `.opencode/skills/pe-gamebryo-rosetta/SKILL.md` (chapter pointer append),
  `package.json` (exactly two new scripts: `serve:catalog`, `test:pecompat:catalog`; three stays
  pinned 0.185.0; NO new dependencies), `tests/pecompat/headless_load.test.mjs` (the T9 5-conjunct
  gate fix), `tests/pecompat/run_app_tests.mjs` (safe default raw dir + honest relabel).
- NEW `compat/` (6): `catalog-app.js`, `catalog-preview.js`, `catalog-table.js`, `catalog.css`,
  `catalog.html`, `server-catalog.mjs` — the /catalog mode + bounded loopback server; the 218757
  app files byte-identical (git diff empty).
- NEW `tools/pecompat/` (20): `ark_index`, `bnt_index`, `catalog_census`, `catalog_data`,
  `catalog_pixel_render`, `catalog_rankings`, `catalog_sniff`, `nif41_deep`, `nif_batch_extent`,
  `phase3_collect_rows`, `phase3_extract_primaries`, `phase3_pcg935_name_batch`, `phase3_renders`,
  `phase3_texture_dispositions`, `phase4_collect_test_results`,
  `phase4_texture_dispositions_update`, `png_nontrivial`, `t9_pixel_render`, `texture_chain`,
  `vfs_inspect` (all `.mjs`).
- NEW `tests/pecompat/` (9): `_catalog_server_helpers.mjs`, `catalog_api_denial.test.mjs`,
  `catalog_archive_safety.test.mjs`, `catalog_bounds_countercheck.test.mjs`,
  `catalog_headless_load.test.mjs`, `catalog_preview_math.test.mjs`,
  `catalog_texture_gates.test.mjs`, `catalog_unknown_sort.test.mjs`, `run_catalog_tests.mjs`.
- NEW skill reference (1): `.opencode/skills/pe-gamebryo-rosetta/references/catalog-era-identity.md`
  (contract §6 chapter; P3-2 example fixed at persistence).
- REPORT_PACKAGE `docs/audits/PE_CITY_ASSET_MAP_R1_20261010/` — full package census in
  EVIDENCE_INDEX.md; MANIFEST_SHA256.csv LAST (self-excluded, bijection-verified).
- OUT OF SCOPE and untouched: `src/pesource/**` (NO change), the 218757 app files, master,
  AUDIT_ENTRYPOINT/governance, historical report packages, foreign untracked paths, all original
  containers/inputs (READ_ONLY), the old SceneIR worktree, the VM.

## 3. Commands (what the human/next session can run)

### Staged-diff proprietary review (§8) — persistence-phase result

- Scanned ALL 167 to-be-committed files (fresh independent scan, in addition to QC13's census of
  the 99 phase-1..4 text files): 0 PNG/JPG/GLB/ARK-EOCD payload signatures; 0 long base64/hex
  runs; 0 bulk NIF headers; 0 binary image/archive files staged anywhere.
- 34 heuristic flags resolved to two documented false-positive classes: (a) format-knowledge
  prose — the literal strings "DDS"/"BNT2" inside JSON/CSV/MD/MJS text (e.g. "expected BNT2",
  "sniffDistribution: DDS 2,752"), never binary magics; (b) UTF-16LE+BOM PowerShell-written
  captures (OBS-2 class: 6 raw/T9 + 3 QC console .txt + RERUN_SUMMARY.json) — human-readable
  captures; the authoritative machine records are the UTF-8 JSONs.
- Textual geometry encoding check: report/JSON/CSV files carry only single metadata values
  (bounds, counts, SHAs) — no vertex-sequence dumps.
- RESULT = PROPRIETARY_CLEAN (publishable per contract §8; nothing to strip).


```text
# catalog viewer (START / OPEN / STOP):
npm run serve:catalog                      # in the worktree; default port 8161 (PECATALOG_PORT / PORT override)
# open: http://127.0.0.1:8161/catalog       (deep link: /catalog#model=193313 etc.)
# stop: terminate the printed PID (startup line: catalog server http://127.0.0.1:<PORT>/ pid=<PID>)

# gate suites (all exit nonzero on FAIL):
node tests/pecompat/run_tests.mjs --models D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt
node tests/pecompat/run_app_tests.mjs --models D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt --three-root <three-root>
npm run test:pecompat:catalog

# deep re-read of the four primaries (bounded reader):
node tools/pecompat/nif41_deep.mjs --in <nif> ...
```

- The OLD 218757 viewer stays at http://127.0.0.1:8140/ (READ_ONLY foreign reference; never
  replaced by the catalog server).

## 4. Findings / repairs / standing flags (summary; full detail in REPORT.md §2–§3)

- Fresh internal QC = PASS_WITH_FINDINGS (0 P0 / 0 P1 / 1 P2 / 3 P3); PE-MASTER CONFIRMED and
  adjudicated MASTER_ACCEPTED (advisory; persisted verbatim in PE_MASTER_REVIEW.md).
- All four QC findings FIXED at this persistence phase with PRE/POST hashes and revalidation
  results in 00_CONTROL_INTERNAL_QC/AMEND_LOG.md (P2-1 CSV quoting; P3-1 ledger append-only
  correction; P3-2 skill example; P3-3 private BOM strip).
- Browser: LOAD verified ×2 real Edge + QC fresh; PIXEL_RENDER 5/5 + QC fresh;
  INTERACTIVE NOT_PERFORMED (daemon down) → BROWSER_VERIFIED NOT claimed (the standing open gate).
- HISTORICAL_PLACEMENT = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO;
  CANONICAL_GATE_EFFECT = NONE; NEXT_EXPERIMENT_AUTHORIZED = NO; HARD_STOP = YES.
- DESKTOP_POST_AUDIT = PENDING (human decision; the QC is internal, not a Desktop post-audit).

## 5. Final handoff block (compact)

```text
RUN_ID = PE_CITY_ASSET_MAP_R1_20261010
PHASE = PERSISTENCE_PUBLISH
BASE_FEATURE_SHA = 59641caa1b14ade84e1842ca36b395842deb241e
BRANCH = codex/pe-city-asset-map-r1-20261010
RESULTING_SHA = <git rev-parse HEAD in the worktree — the single run commit>
REMOTE_FEATURE_SHA = <git ls-remote origin refs/heads/codex/pe-city-asset-map-r1-20261010> (== RESULTING_SHA; verified at push)
ACTUAL_MASTER = 3fbe93eec04759395223e6677b5040273d29222a (local == origin == fresh remote; UNTOUCHED)
FIXES_APPLIED = P2-1 + P3-1 + P3-2 + P3-3 (PRE/POST hashes in 00_CONTROL_INTERNAL_QC/AMEND_LOG.md)
RUN_STATUS = COMPLETED_WITH_MASTER_ACCEPTED_ADVISORY__INTERACTIVE_SMOKE_OPEN
DESKTOP_POST_AUDIT = PENDING
HARD_STOP = YES
```
