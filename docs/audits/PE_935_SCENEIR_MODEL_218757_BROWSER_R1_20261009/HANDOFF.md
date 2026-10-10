# HANDOFF — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009

Final handoff of the run (phase PERSISTENCE_PUBLISH). Written BEFORE the
package manifest (MANIFEST_SHA256.csv is generated LAST, self-excluded, after
every other package edit).

```text
AUDIT_OUTPUT_ROOT     = docs/audits/PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009/
                        (on branch codex/pe-sceneir-218757-r1-20261009)
FINAL_REPORT_PATH     = docs/audits/PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009/FINAL_REPORT.md
PRIMARY_EVIDENCE_PATHS = PLAN_AND_PATH_ALLOWLIST.md, INPUT_IDENTITIES.json,
                        SOURCE_IDENTITIES.json, CONTROLS_A.json, CONTROLS_B.json
                        (+ raw/CONTROL_B/), IMPLEMENTATION_NOTES.md,
                        TEST_RESULTS_UNIT.json, TEST_RESULTS_APP.json,
                        APP_AND_SERVER_NOTES.md, SMOKE_CHECKLIST.md, REVIEW.md,
                        QC_RESULTS.json, 00_CONTROL_INTERNAL_QC/ (incl.
                        AMEND_LOG.md), raw/ (HTTP transcripts, headless
                        evidence, sceneir dump, FILE_SCENE_SPACE transforms)
RUN_STATUS            = COMPLETED_WITH_MASTER_ACCEPTED_ADVISORY__INTERACTIVE_SMOKE_OPEN
HARD_STOP_REASON      = NONE (contract scope executed to the runnable slice;
                        interactive browser automation unavailable in this
                        environment; DESKTOP_POST_AUDIT = PENDING;
                        NEXT_EXPERIMENT_AUTHORIZED = NO)
```

## 1. Branch / SHA state (publication)

```text
BASE_SHA                = 3fbe93eec04759395223e6677b5040273d29222a
BRANCH                  = codex/pe-sceneir-218757-r1-20261009
WORKTREE                = D:\Eudoria_Reconstruction\12_WebGame\pe-sceneir-218757-r1
ACTUAL_REMOTE_MASTER    = 3fbe93eec04759395223e6677b5040273d29222a
                          (recorded SEPARATELY; canonical master untouched —
                          measured by git ls-remote before the commit,
                          re-verified after the push)
RESULTING_SHA           = discover with `git log -1` on the branch after the
                          publication commit (a file cannot contain its own
                          commit SHA); the verified value is recorded in the
                          terminal handoff block of this persistence phase.
REMOTE_FEATURE_BRANCH_SHA = verified after push (git ls-remote origin
                          refs/heads/codex/pe-sceneir-218757-r1-20261009);
                          recorded in the terminal handoff block.
Publication form        = ONE normal commit on the feature branch; push -u
                          origin codex/pe-sceneir-218757-r1-20261009; NO
                          force, NO master push, NO history rewrite.
```

## 2. Exact commands (server / tests)

From the worktree root:

```text
npm run serve:sceneir
  -> prints: sceneir server http://127.0.0.1:8140/ pid=<PID>
  -> URL: http://127.0.0.1:8140/   (local only; loopback bind 127.0.0.1 is
     hardcoded/not configurable; busy port = LOUD exit, never replaces
     another process)
  -> STOP: terminate the printed PID (Stop-Process -Id <PID>, or Ctrl+C in the
     owning console); verify the port is freed (rebind probe) — do NOT leave
     the server running.

npm run test:pecompat --models "D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt"
  -> unit suite, 24 tests (24/24 PASS recorded). Without --models: 17 PASS +
     1 loud NOT_PERFORMED (negative control).

npm run test:pecompat:app
  -> app/server suite, 13 tests (13/13 PASS recorded; the harness owns its
     bounded loopback server lifecycle; nothing is left running).
```

Requires the pinned local container
`D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt`
(395,412,868 B / SHA256 c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0)
— READ_ONLY, never committed.

## 3. Changed-path census (the commit's content; manifest scope is SEPARATE)

```text
compat/                                   7 files (app shell, two modes, api client, css, index.html, loopback server)
src/pecompat/                             6 files (PecTransform, PecSceneIR, PecNif10Reader, PecAssetAdapter, PecInstanceBuilder, PecRenderConvert)
tools/pecompat/                           3 files (extract_218757, sceneir_dump, controlB_compare)
tests/pecompat/                          13 files (tests/ contains ONLY tests/pecompat: 9 test files + 2 harnesses + 2 helper modules; the QC REVIEW.md §1 prose count of 14 is a census-side slip — the disk census, QC's own 29-file code pin and the staged census all confirm 13)
.opencode/skills/pe-gamebryo-rosetta/      3 files (SKILL.md + 2 references)
docs/audits/PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009/  68 files (report package: 61 phase-1..QC files + 7 final-phase files incl. the manifest)
package.json                               1 MODIFIED — scripts-only diff (three npm scripts: test:pecompat, test:pecompat:app, serve:sceneir; dependencies untouched; three 0.185.0 RETAINED)
TOTAL committed files                      101
src/pesource/                              ZERO diff (457485 witness untouched — byte-identical to BASE, git blob 7d926fb326339c4983f571cfa839bdefcdd155bb)
```

The report package manifest (MANIFEST_SHA256.csv) hashes ONLY the report
package; the code/skill/test changes above are NOT hashed by the report
manifest — they are enumerated here and in FINAL_REPORT.md §3
(CHANGED_PATH_CENSUS) and verified by the commit census.

## 4. Open items (honest)

- OPEN INTERACTIVE SMOKE GATE: SMOKE_CHECKLIST.md not executed (automation
  daemon unavailable in this environment). ACCEPTED_RUNNABLE_VERIFIED = NO;
  BROWSER_VERIFICATION = REAL_BROWSER_LOAD_VERIFIED__INTERACTIVE_NOT_PERFORMED.
- OPEN P3 findings (F-QC-2, F-QC-3, F-QC-4, F-QC-5) — documented with
  corrections and revalidation gates for the next code touch; none
  load-bearing.
- DESKTOP_POST_AUDIT = PENDING (human gate; nothing in this run claims it).
- NEXT_EXPERIMENT_AUTHORIZED = NO; HARD_STOP = YES.

## 5. Key measured gates (quick reference; full block in FINAL_REPORT.md §3)

unit 24/24 (+17/1 negative control) | app 13/13 | T1 native parity 2/2 tol 1e-4
((96,202,306)/(58,221,363) verbatim) | T5 14/14 associations + 28/28
fingerprints (predecessor-matched; QC third-implementation spot-check 2/2) |
66 = 62+2+2 accounting | 9+5 texture discipline (container NOT_ESTABLISHED) |
denials 22/22 executor + 10/10 QC subset | real-browser loads 3× READY (asset,
asset, scene) | MODEL_218757_INPUT_SHA256 3e8a22c2213202207e374b55cd65b2c3be039ccdd1e8d01a07fcaf44de12cf36.
