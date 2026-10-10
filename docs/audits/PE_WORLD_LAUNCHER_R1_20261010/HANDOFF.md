# HANDOFF.md — PE_WORLD_LAUNCHER_R1_20261010 — FINAL HANDOFF (persistence phase)

RUN_ID = PE_WORLD_LAUNCHER_R1_20261010
PHASE = PERSISTENCE_PUBLISH (contract §10; performed by the pe-master-auditor persistence
        session; the report package + ONE branch commit + push; NO new science)
BASE_SHA = e9bb1f5120444f8bafd7d90c426f9e64d6b9bf2c (BASE_DECISION disclosure: REPORT.md
        §1 + AUTHORIZATION_AND_PREFLIGHT.md §3; contract EXPECTED f71eb30a is an ancestor)
BRANCH = codex/pe-world-launcher-r1-20261010
WORKTREE = D:\Eudoria_Reconstruction\12_WebGame\pe-world-launcher-r1
PRIVATE_OUTPUT = D:\Eudoria_Reconstruction\99_Audits\PE_WORLD_LAUNCHER_R1_20261010
        (never committed; referenced by path+SHA256 only)
DATE = 2026-10-10

## 1. Git state (measured at persistence; discover commands included)

- BASE: worktree created FROM e9bb1f5120444f8bafd7d90c426f9e64d6b9bf2c on the new branch
  (§1.8 of AUTHORIZATION_AND_PREFLIGHT.md); the other worktrees untouched throughout
  (pe-sceneir-218757-r1 @ 59641ca READ_ONLY; pe-city-asset-map-r1 @ e9bb1f5 clean — its
  earlier local modifications ARE the committed CAMERA_UX_FIX).
- ACTUAL_MASTER = 3fbe93eec04759395223e6677b5040273d29222a — local == origin == fresh
  remote (`git ls-remote origin`), verified at run start, QC end AND persistence start
  AND (re-measured) after push; NEVER touched (no merge, no master push, no master write).
- Publication = ONE normal commit of the run's paths on THIS branch only, then
  `git push -u origin codex/pe-world-launcher-r1-20261010` (no force, no amend, no PR).
- RESULTING_SHA (discover): `git rev-parse HEAD` in the worktree (the single run commit;
  self-exclusion precedent — this package cannot embed its own commit's hash; the measured
  value is in the run's terminal handoff).
- REMOTE_FEATURE_SHA (discover): `git ls-remote origin
  refs/heads/codex/pe-world-launcher-r1-20261010` — must equal RESULTING_SHA (the equality
  was verified at push time by this persistence phase; measured value in the terminal
  handoff).
- COMMITTED_PATH_SET verification command: `git show --stat --name-only <RESULTING_SHA>`
  — the staged census below must equal the committed set exactly (verified pre-commit by
  `git diff --cached --name-only` against this list; no -A anywhere).

## 2. Changed-path census (the run's full set; §9 allowlist conformance verified)

34 git entries = 10 MODIFIED + 24 NEW (code/tools/tests/skill/package) + the report
package (untracked dir → committed). Group census:

- MODIFIED (10):
  - `.opencode/skills/pe-gamebryo-rosetta/SKILL.md` (world-launcher lineage status
    DELIVERED — the P3-2 fix; era/UNKNOWN discipline preserved)
  - `compat/server-catalog.mjs` (the era gate lifted to before data access + shared
    allowlist/statics pattern reuse; +16/−6)
  - `package.json` (EXACTLY 2 new scripts: `serve:world`, `test:pecompat:world`;
    three stays pinned 0.185.0; NO dependency changes)
  - `tools/pecompat/catalog_data.mjs` (CAM-C2: FAILED-not-a-measurement; shared status
    model)
  - `tools/pecompat/png_nontrivial.mjs` (canvas-region census option — the U-19 evidence
    tool support)
  - `tests/pecompat/catalog_archive_safety.test.mjs`, `catalog_bounds_countercheck.test.mjs`,
    `catalog_preview_math.test.mjs`, `catalog_unknown_sort.test.mjs`, `run_catalog_tests.mjs`
    (the CAM-C3 cache-envelope declaration + world-battery awareness in the shared runner;
    +3/−1 each envelope edit)
- NEW `compat/` (9): `launcher.css`, `launcher.html`, `launcher.js`, `server-world.mjs`,
  `world-app.js`, `world-splat.js`, `world-vegetation.js`, `world.css`, `world.html` —
  the /launcher + /world apps + the bounded loopback world server (U-19 fix inside
  world-app.js SPLAT_FRAG; launcher.js/launcher.html carry the P3-1-repaired 0xff5a text).
- NEW `src/peworld/` (1): `PEFoliageLabSeed.js` — the DOCUMENTED LAB_SEED wrapper
  ([P-CELLSTREAM] stand-in; PEFoliageCore byte-identical — WORLD_VEG_CORE_UNTOUCHED).
- NEW `tools/pecompat/` (4): `cam_c1_glb_compare.mjs` (CAM-C1 retraction evidence),
  `world_collect_test_results.mjs`, `world_pixel_render.mjs` (CDP capture),
  `world_splat_per_color.mjs` (the U-19 per-color gate tool).
- NEW `tests/pecompat/` (8): `_world_server_helpers.mjs`, `catalog_cam_fixes.test.mjs`,
  `run_world_tests.mjs`, `world_headless_load.test.mjs`, `world_materials.test.mjs`,
  `world_server.test.mjs`, `world_terrain.test.mjs`, `world_vegetation.test.mjs`.
- NEW skill reference (1): `.opencode/skills/pe-gamebryo-rosetta/references/
  terrain-foliage-integration.md` (terrain/materials/foliage integration index + checked
  sources + executed controls + explicit UNKNOWNs; P3-1-repaired 0xff5a).
- REPORT_PACKAGE `docs/audits/PE_WORLD_LAUNCHER_R1_20261010/` — full file census in
  EVIDENCE_INDEX.md; MANIFEST_SHA256.csv LAST (self-excluded, bijection-verified).
- **src/pesource: ZERO changes** (verified: `git status` 0 entries under src/pesource;
  `git diff HEAD -- src/pesource` empty; all 12 pesource modules byte-identical to HEAD
  — the QC hash-object sweep + the battery's WORLD_VEG_CORE_UNTOUCHED witness gates).
  src/pecompat: ZERO changes.
- OUT OF SCOPE and untouched: master, AUDIT_ENTRYPOINT/governance, PROJECT_STATE,
  milestone/gates, historical docs/audits packages (incl. the f71eb30 package — READ_ONLY),
  the old viewer (218757 app files byte-identical), foreign untracked paths, all original
  containers/inputs (READ_ONLY), the other worktrees, the VM.

## 3. Commands (what the human/next session can run)

```powershell
# the standing world preview server (RUNNING now):
Set-Location D:\Eudoria_Reconstruction\12_WebGame\pe-world-launcher-r1
npm run serve:world                      # START (PID printed at startup; default 8162)
Stop-Process -Id 24964                   # STOP (own process only)
Invoke-RestMethod http://127.0.0.1:8162/api/world/status   # verify

# the batteries (all green: 44/41/24/22):
npm run test:pecompat:world    # 44 gates (terrain/server/materials/vegetation/headless-load)
npm run test:pecompat:catalog  # 41 gates (incl. the CAM-C1/C2/C3 focused QC A suite)
npm run test:pecompat:app     # 22 gates (the 218757 app regression battery)
npm run test:pecompat         # 24 gates (the unit battery incl. the witness guard)

# the SHA state (post-publication verification):
git rev-parse HEAD                                        # RESULTING_SHA
git ls-remote origin refs/heads/codex/pe-world-launcher-r1-20261010   # == RESULTING_SHA
git rev-parse master origin/master                        # 3fbe93e… (untouched)
```

## 4. Staged-diff proprietary review (§10) — persistence-phase result

Scanned ALL to-be-committed text files (the 10 modified + the 23 new code/tool/test/skill
files + EVERY report-package file incl. all raw/ HTML dumps and JSONs): 0 PNG/JPG/DDS/TGA
payload signatures; 0 bulk "NetImmerse File Format" headers; 0 long base64 runs (≥4000
chars); 0 bulk f32 vertex sequences (>300); 0 binary image/archive files staged. The mask
base64 inside the materials TEST evidence is bounded per-record 256-B material masks
(legitimate decoded-data evidence, not payload redistribution). Textual geometry encoding
checked explicitly (the CAM-C1 comparison JSONs carry derived position/triangle MULTISETS —
aggregated numeric arrays, not redistributable asset payloads; sizes bounded). All PNGs/
screenshots verified PRIVATE-ONLY (5 private PNGs spot-checked path+size+SHA by QC + the
2 U-19 captures + QC's own launcher capture — none committed). RESULT: SAFE TO COMMIT.

## 5. Manifest (§10) — generated LAST

MANIFEST_SHA256.csv (LF, UTF-8 no BOM, lowercase hex) covers EVERY report-package file
except itself; generated after all final writes; bijection `physical package files minus
manifest <-> rows` verified by an INDEPENDENT verification path (no duplicates, no
missing, no extra; every size + SHA256 matches). Any later package write invalidates it.

## 6. The standing world server (left RUNNING per contract §10)

- http://127.0.0.1:8162/ PID 24964 (started from this worktree; serves the final code
  from disk — byte-identity verified at persistence: served compat/world-app.js == disk,
  SHA256 15113B26B1F2AA53997BD5BFDE1D7B56EF53CCAF410426BB8BAB31BED599DB6A).
- Foreign standing servers 8140 (PID 21288) + 8161 (PID 9588): alive, untouched.
- No test server left running; suite servers stopped with port-freed proof (ledger).

## 7. Terminal handoff block (this phase's return to PE-MASTER)

```text
RUN_ID                     = PE_WORLD_LAUNCHER_R1_20261010
PHASE                      = PERSISTENCE_PUBLISH
BRANCH                     = codex/pe-world-launcher-r1-20261010
RESULTING_SHA              = (measured post-commit; git rev-parse HEAD; terminal message)
REMOTE_FEATURE_SHA         = (measured post-push; == RESULTING_SHA; terminal message)
REMOTE_VERIFIED            = local == origin == fresh remote (verified at push)
ACTUAL_MASTER              = 3fbe93eec04759395223e6677b5040273d29222a (local+origin+remote, untouched)
COMMIT_PATH_CENSUS         = 34 git entries staged: 10 M + 24 new (+ report package files);
                             per-group in §2; §9 allowlist conformance verified;
                             src/pesource absent (0 files)
MANIFEST_ROWS              = (count; == physical package files minus the manifest)
MANIFEST_BIJECTION         = VERIFIED (independent path; no dup/missing/extra; sizes+SHAs match)
STAGED_PROPRIETARY_REVIEW  = SAFE (§4 above; 0 payload findings)
FINAL_REPORT_FIELDS_FILLED = ALL §10 fields (REPORT.md §3; clean 3270/3270 per P3-3)
PE_MASTER_REVIEW_PERSISTED = VERBATIM (PE_MASTER_REVIEW.md; between the dispatch markers,
                             no markers in the file)
SERVERS_FINAL              = 8162 world PID 24964 (serving the FINAL committed code) +
                             8140 PID 21288 + 8161 PID 9588 (alive, untouched)
ORPHAN_PROCESSES           = NONE (all suite/dev servers stopped with port-freed proof;
                             the orphan debug-server case PID 14820 was cleaned in-run,
                             ledger-recorded)
BLOCKERS                   = NONE
```
