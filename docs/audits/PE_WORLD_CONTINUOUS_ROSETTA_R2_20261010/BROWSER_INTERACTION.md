# BROWSER_INTERACTION — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010

Kontrakt §8: „Uruchom prawdziwą przeglądarkę i sprawdź DOM/load, piksele
oraz realne wejście użytkownika oddzielnie.”

## Metoda (udokumentowana)

- **Prawdziwa przeglądarka**: Microsoft Edge (headless=new) — suite-owned
  IZOLOWANA instancja: własny `--user-data-dir` (tmp), CDP
  `--remote-debugging-port` na WOLNYM porcie (znaleziony per-run; NIGDY
  9222, nigdy cudza sesja, zero globalnych zmian zabezpieczeń). Sterowanie
  CDP (natywny WebSocket Node 22): Page.navigate, Runtime.evaluate,
  Input.dispatchKeyEvent (rawKeyDown/keyUp — „char” NIE generuje keydown,
  zmierzone), Input.dispatchMouseEvent (mousePressed/mouseMoved/
  mouseReleased = drag-look), Emulation.setDeviceMetricsOverride (resize),
  Page.captureScreenshot (PNG prywatnie: `D:\Eudoria_Reconstruction\
  99_Audits\PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010\browser_png\`).
- Narzędzie: `tools/pecompat/world_r2_browser.mjs` (+ world_r2_pixel_diff.mjs,
  world_r2_performance.mjs). Surowe dane: raw/BROWSER/INTERACTION_SCENARIOS.json,
  PIXEL_DIFFS.json; PERFORMANCE_AND_LIMITS.json.
- Readiness marker = WŁASNY uczciwy marker strony (data-load-status=READY /
  scene-coherence GOTOWA / witness status) — nigdy nie „ty jesteś testem”.

## Wyniki (10 scenariuszy; 0 nieprzechwyconych wyjątków strony)

| # | Scenariusz | Wejście (realne) | Wynik |
|---|---|---|---|
| S1 | /world boot → READY + canvas ≥85%/80% | navigate + wait READY | **PASS** (READY; canvasFrac w JSON) |
| S2 | F ×3 stabilność okna (WL-4) | keydown F ×3 | **PASS** (3× identyczny origin; PRE: dryf do 68,129) |
| S3 | przejścia trybów 1/2/3 bez skoku | keydown 2/3/1 | **PASS** (maxXYJump 0) |
| S4 | spacer realnym W | rawKeyDown W 2 s (wcześniej drag-look mouse up 150 px — fallback po odrzuceniu pointer lock) | **PASS** (ruch XZ ~15 m; Y = 51.7 = sharedQuery 50.0 + oko 1.7 → yOnSharedSurface) |
| S5 | teleport daleko (180,40) i powrót | drawer inputs + tp-go ×2 | **PASS** (windowFollowed 176,36; powrót: requested 2485 = placed 2485 = wyjściowe — sameConfigSameCounts) |
| S6 | drawer nie przechwytuje ruchu | keydown W na POLU (bubbles), blur, keydown W na window | **PASS** (podczas pisania 0 ruchu; po blur ruch) |
| S7 | przełącznik roślinności | change checkbox ×2 | **PASS** (pixel diff 6.06% ≥ 2% w widocznym regionie canvasa; oba capture nontrivial) |
| S8 | przełącznik tekstur terenu | change checkbox ×2 | **PASS** (pixel diff 89.7%) |
| S9 | resize 1280×720→960×600→restore | setDeviceMetricsOverride | **PASS** (kamera bez zmian; drawing buffer podąża) |
| S10 | Asset Lab: 519316 + 4 proxy CD | navigate /assetlab; select ×5 | **PASS** (519316: NIF 10.1.0.0, 3/3 teksturowane, sloty 0 pominiętych; 4 proxy: SOURCE-UNTEXTURED status, eras oddzielne) |

**PIXEL_RENDER**: 11/11 capture nontrivial (uniqueColors/lumaStdDev nad
progami); toggle diffs w widocznym regionie (UI-chrome wyłączone z
mianownika — dyscyplina R1 CANVAS_REGIONS): vegToggle 6.06%, textureToggle
89.7%, teleportFarVsHome 83.5% — wszystkie ≥ progów prerejestrowanych.

**INTERACTION = PASS** (full required interaction performed; nie zastąpione
screenshotem ani „self-testem”). Prawdziwa pętla fly/walk była wykonywana
S4 (raw input, powierzchnia wspólna); odrzucenie pointer lock w headless
obsłużone przez widoczny hint + drag-look (działa — S4 użyło go do
wyprowadzenia patrzenia z pionu).

Uczciwe uwagi: interaktywny „feel” z żywą referencją 9350 nie porównany w
tej sesji (REFERENCE_INTERACTION_NOT_VERIFIED — standing serwer dostępny
tylko HTTP; nie przejmujemy cudzych sesji) — preset cyfrowy przejęty z
faktycznie serwowanego viewer.js (pin LIVE_REFERENCE_CAMERA.json).
