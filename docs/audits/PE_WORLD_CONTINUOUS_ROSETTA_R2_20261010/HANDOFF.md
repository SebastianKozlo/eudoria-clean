# HANDOFF — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010

Do PE-MASTER (kompletne wartości zwrotne kontraktu; szczegóły w plikach
pakietu).

```text
RUN_ID                 = PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010
RUN_STATUS             = COMPLETED  (all mandatory features/tests PASS in the examined implemented scope; honest limits listed; no failed gate)
HARD_STOP_REASON       = contract complete (§10): the run ends with a working implementation + honest limits; NEXT_EXPERIMENT_AUTHORIZED=NO

REPOSITORY             = SebastianKozlo/eudoria-clean
BRANCH                 = codex/pe-world-continuous-r2-20261010 (FF from BASE)
ACTUAL BASE            = 44ef254b8ff9ebb05bd104690181c202678c065d (codex/pe-world-launcher-r1-20261010; fresh ls-remote verified pre-start AND pre-commit)
RESULTING_SHA          = git rev-parse HEAD w worktree (single run commit; self-exclusion precedent — ten pakiet nie może zawierać hasha własnego commitu; zmierzona wartość w terminal handoffu tego runu)
REMOTE_SHA            = git ls-remote origin refs/heads/codex/pe-world-continuous-r2-20261010 (must equal RESULTING_SHA; równość zweryfikowana przy pushu; wartość w terminal handoffu)
```

## Weryfikacje discover (wykonane przy publikacji)

- Fresh `git ls-remote origin` przed commitem: ACTUAL_BASE (launcher-r1) nadal
  44ef254b8ff9ebb05bd104690181c202678c065d; RESULT_BRANCH jeszcze nie istniał;
  ACTUAL_MASTER 3fbe93eec04759395223e6677b5040273d29222a bez zmian (nietknięty).
- `git diff --cached --name-only` == census poniżej (no -A nigdzie); po pushu
  `git show --stat --name-only <RESULTING_SHA>` == ten sam zbiór.
- Manifest bijekcja: każdy fizyczny plik pakietu dokładnie raz (MANIFEST_SHA256.csv
  sam się wyklucza — precedent self-exclusion); policzone dwukrotnie.
  [SUPERSEDED w rundzie korekty 2026-10-10: dla ORYGINALNEGO opublikowanego
  stanu twierdzenie było fałszywe (QC P1-1: mismatch wiersza REPORT.md —
  manifest 12408/95650dbc… vs plik 12410/EFCA8566…); manifest zregenerowany
  ze stanu finalnego pakietu korekty i zweryfikowany DWIEMA NIEZALEŻNYMI
  metodami — patrz CORRECTIONS.md P1-1.]

## Bramki (§8 — oddzielne)

```text
DATA_READ_PATH  = PASS
PRODUCT_LOAD    = PASS
PIXEL_RENDER    = PASS
INTERACTION     = PASS   (real browser, real input — 10 scenarios, 0 page errors)
CONTINUOUS_WORLD= PASS   (near+mid+far from REAL samples; measured denominator 51920; 0 missing/failed)
ASSET_LAB       = PASS   (519316 live chain 3/3 textured; 4 CD proxy controls source-untextured; separate eras)
PERFORMANCE     = MEASURED_WITH_LIMITS (budgets pre-registered; all checks PASS; full curve in PERFORMANCE_AND_LIMITS.json)
```

PRODUCT_VERDICT = PASS_IN_EXAMINED_IMPLEMENTED_SCOPE (wszystkie mandatory
features/tests PASS w zbadanym zakresie; otwarte ograniczenia jawnie w
UNRESOLVED_AND_NEXT_SEAMS.md — w tym REFERENCE_INTERACTION_NOT_VERIFIED).

## WL-1..WL-6 disposition (PRE reproduced → POST fixed)

| Finding | PRE (BASE, real functions) | POST (R2) |
|---|---|---|
| WL-1 latest request lost | REPRODUCED (final origin A; busy null) | **FIXED** (queued latest runs; final origin B) |
| WL-2 height mismatch | REPRODUCED (1275/2304 nonzero, max 0.953125; walk↔tri max 15.8203125; 14 y=0 fallback) | **FIXED** (shared triangle query: max diff 0; halo covers 0..512; y=0 fallback GONE from production; 0 deferred in default window) |
| WL-3 walk commits before guard | REPRODUCED ((100,10,100)→(100,10,88)) | **FIXED** (candidate-first; position unchanged + banner) |
| WL-4 fit chases window | REPRODUCED ((53,114)→(68,129)) | **FIXED** (focus-follow streaming; 3× F stable) |
| WL-5 cap slice / recIndex / density | REPRODUCED (11 tiles emptied; 4 coincident groups; 3 IDs @50%) | **FIXED** (fair quota 0 emptied + order-invariant; 0 coincident (recIndex); 5 IDs @50%; density monotone) |
| WL-6 records | LITERAL_ORIGINAL_BASE_GATE_COMPLIANCE=FAIL preserved (parent e9bb1f5 measured fresh); R1 product PASS superseded → PARTIAL/REQUIRE_CORRECTIONS | R1_RECORD_SUPERSESSION.md (no retroactive authorization; no old-package edits) |

PEFoliageCore/PETerrainCore byte-identical (PRE==POST SHA); NifModelReader
byte-identical z BASE (T6).

## Paczka

- AUDIT_OUTPUT_ROOT (repo package):
  `docs/audits/PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010/` (REPORT, INPUT_
  IDENTITIES, R1_RECORD_SUPERSESSION, PRE/POST_COUNTERCHECKS, TEST_RESULTS,
  STREAMING_AND_HEIGHT_QC, WORLD_COVERAGE_AND_LOD, VEGETATION_CENSUS,
  CAMERA_UI_AND_ASSET_LAB, GAMEBRYO_IMPLEMENTATION_LINKS, ROSETTA_RUNTIME_
  PROVENANCE, BROWSER_INTERACTION, PERFORMANCE_AND_LIMITS, INTERNAL_REVIEW,
  PE_MASTER_REVIEW (NOT_PERFORMED placeholder), UNRESOLVED_AND_NEXT_SEAMS,
  RUN_AND_STOP, HANDOFF, MANIFEST_SHA256.csv + raw/*).
- PRIVATE_OUTPUT_ROOT: `D:\Eudoria_Reconstruction\99_Audits\
  PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010\` (screenshots PNG, logi serwera,
  skrypty probe sesji).
- Changed-path census: 25 ścieżek (pełna lista w REPORT §5; allowlist-only:
  compat/, src/peworld/, src/pesource (1 NEW file: DdsDecoder.js — jedyny
  nowy plik w src/pesource; [POPRAWIONE w rundzie korekty: pierwotne pole
  mówiło błędnie „2 NEW files"]), tests/pecompat/, tools/pecompat/,
  skill pe-gamebryo-rosetta, OUTPUT_REPO_PATH; [.gitignore USUNIĘTY z listy
  w rundzie korekty — plik nietknięty, git diff --name-status BASE..HEAD
  daje pusty wynik dla .gitignore]).
  Zero proprietary payloadów w repo (rozszerzenia binarne skanowane).

## Runda korekty (2026-10-10, po INTERNAL_QC) — dodatkowe changed paths

Commit korekty (na wierzchu b4dfae7) zmienia: compat/world-app.js (P1-2
wrapper latest-wins + vegTrace diagnostyka read-only),
tools/pecompat/world_r2_counterchecks.mjs (WL-1 wrapper + --no-canonical),
tools/pecompat/world_r2_correction_counterchecks.mjs (NEW),
tools/pecompat/world_r2_correction_browser.mjs (NEW),
tests/pecompat/world_r2_gates.test.mjs (bramka R2_VEG_WRAPPER_LATEST_WINS),
tests/pecompat/run_world_tests.mjs, run_app_tests.mjs, run_catalog_tests.mjs
(P3a neutral raw-dirs) oraz pliki pakietu (REPORT/HANDOFF/RUN_AND_STOP/
INPUT_IDENTITIES/CORRECTIONS.md NEW/CORRECTION_COUNTERCHECKS.json NEW/
raw/CORRECTION/* NEW/MANIFEST_SHA256.csv regenerated). Pełne rozliczenie:
CORRECTIONS.md.

## Serwer

- RUNNING: `http://127.0.0.1:8163` (launcher /launcher, świat /world,
  Asset Lab /assetlab); node PID 23232 (runda korekty: restart na kodzie
  korekty; [POPRAWIONE w rundzie korekty: pierwotny zapis mówił PID 33876 —
  martwy w momencie QC; pełny łańcuch restartów w RUN_AND_STOP.md]);
  start/stop + served↔published identity: RUN_AND_STOP.md.

## Zachowane frazy (§10 — verbatim)

```text
HISTORICAL_TREE_DISTRIBUTION = NOT_ESTABLISHED
ORIGINAL_REGION_TO_CLIMATE_JOIN = NOT_ESTABLISHED
HISTORICAL_BUILDING_PLACEMENT = NOT_ESTABLISHED
MODEL_218757_TO_WORLD_INSTANCE = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
ALL_NIFS_SUPPORTED = NOT_ESTABLISHED
FULL_ORIGINAL_GAME_REIMPLEMENTED = NO
CANONICAL_GATE_EFFECT = NONE
INDEPENDENT_DESKTOP_POST_AUDIT = PENDING
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
```
