# REPORT.md — PE_WORLD_LAUNCHER_R1_20261010 — FINAL REPORT

RUN_ID = PE_WORLD_LAUNCHER_R1_20261010
RESULT_BRANCH = codex/pe-world-launcher-r1-20261010
BASE_SHA = e9bb1f5120444f8bafd7d90c426f9e64d6b9bf2c (see the BASE_DECISION below)
DATE = 2026-10-10
AUTHOR = pe-reconstruction (executor, phases 1–5 + the U-19 correction round) + pe-master-auditor
(fresh internal QC + THIS persistence phase); PE-MASTER review persisted verbatim in
PE_MASTER_REVIEW.md (VERDICT = MASTER_ACCEPTED, advisory; CANONICAL_GATE_EFFECT = NONE)

---

## 0. What you can open RIGHT NOW (human-first)

**Uruchomiony podgląd świata (serwer w tle, działa i czeka):**

- **Launcher (mapa wysokości):** http://127.0.0.1:8162/launcher
  — prawdziwa mapa wysokości z `terrain.bnt` (era PCG_9_3_5, 51 920 kafli, 100% coverage),
  legenda, wybór kafla/siatki, profil roślinności, LAB_SEED, gęstość podglądu,
  przycisk **„Uruchom podgląd świata”**.
- **Świat (bezpośredni link do okna startowego):**
  http://127.0.0.1:8162/world#tile=53,114&profile=0&seed=0&density=50
  — teren z oryginalnych próbek u16 (okno 8×8 = 64 aktywne kafle strumieniowane wokół
  kamery), TEKSTURY TERENU z oryginalnych TGA (naprawiony splat — pat-color 36/36),
  deterministyczna roślinność (oryginalne modele samej ery, seed=0 → ten sam zestaw),
  przełączniki (texture toggle / vegetation toggle / wireframe / tile bounds),
  pozycja w jednostkach adaptera + klucz kafla (bez etykiety „oryginalne XYZ”).

**Serwer (zostawiony działający na życzenie kontraktu §10):**

```text
URL           = http://127.0.0.1:8162/   ( /  przekierowuje na /launcher )
PID           = 24964                    (node compat/server-world.mjs)
WORKDIR       = D:\Eudoria_Reconstruction\12_WebGame\pe-world-launcher-r1
START_COMMAND = npm run serve:world      (z katalogu worktree; PID drukowany przy starcie)
STOP_COMMAND  = Stop-Process -Id 24964   (wyłącznie własny proces)
```

Serwer serwuje **finalny kod** (pliki statyczne z dysku worktree; zweryfikowane
byte-identity: serwowany `compat/world-app.js` == plik na dysku, SHA256
15113B26B1F2AA53997BD5BFDE1D7B56EF53CCAF410426BB8BAB31BED599DB6A — wersja z naprawą U-19).

**Serwery stojące (nieruszane przez cały run, nadal działają):** 8140 (PID 21288 — stary
viewer 218757) i 8161 (PID 9588 — katalog). Wszystkie trzy PID-y potwierdzone żywe na końcu
fazy publikacji.

**Czego NIE ma (uczciwie):** interakcja w przeglądarce NIE została zautomatyzowana
(demon 9222 down przez cały run) → INTERACTION_VERIFIED = NOT_PERFORMED.
**Ty jesteś testem interaktywnym**: launcher → mapa → wybór kafla → „Uruchom podgląd
świata” → spacer (WASD, mysz po świadomym kliknięciu, ESC uwalnia kursor) → przełączniki →
powrót. Wygląd interaktywny (prawdziwy GPU, nie headless ANGLE/WARP) pozostaje UNVERIFIED do
Twojego sprawdzenia.

**INDEPENDENT_DESKTOP_POST_AUDIT = PENDING** — ten raport + QC wewnętrzne + przegląd
PE-MASTER (advisory) NIE zastępują niezależnego audytu Desktop po publikacji.

---

## 1. BASE_DECISION — EXPLICIT DISCLOSURE (never hidden)

Kontrakt oczekiwał `EXPECTED_BASE_SHA = f71eb30ade05d26c4f71f11087a56f4891113680`; zdalny
source branch był na `e9bb1f5120444f8bafd7d90c426f9e64d6b9bf2c`. PE-MASTER zweryfikował i
zdecydował (pełny zapis verbatim: AUTHORIZATION_AND_PREFLIGHT.md §3):

- f71eb30a **JEST** przodkiem e9bb1f5 (`git merge-base --is-ancestor` → 0);
- delta f71eb30a..e9bb1f5 to **DOKŁADNIE JEDEN commit** — CAMERA_UX_FIX
  (compat/catalog-app.js + compat/catalog-preview.js, +169/−14) — autoryzowany przez
  tego samego człowieka w poprzedniej turze („popraw obracanie kamery”);
- klauzula BLOCKED_BASE_CHANGED strzeże przed nieautoryzowanym dryfem obcym; ta delta to
  autoryzowana kontynuacja użytkownika. Budowa od f71eb30a wskrzesiłaby zepsutą kamerę,
  którą użytkownik kazał naprawić.
- **DECISION: RESULT_BRANCH utworzony z e9bb1f5.** Nigdy nie była to cicha adaptacja —
  ujawnienie zapisane w AUTHORIZATION_AND_PREFLIGHT.md, cytowane w
  CAM_C1_C2_C3_DISPOSITION.md §0, tutaj i w PE_MASTER_REVIEW.md.

Publikacja = **jeden zwykły commit** tej gałęzi (patrz §3: RESULTING_SHA/REMOTE_FEATURE_SHA).

---

## 2. Phase summaries (sources: the phase artifacts, all QC-reverified; full read evidence in INTERNAL_REVIEW.md)

### Etap A — trzy błędy katalogu (CAM-C1/C2/C3) — corrected and verified

- **CAM-C1 — RETRACTION EXECUTED** nad standing claim `NO_GLB_PRESENT_FOR_THESE_IDS`.
  Cztery GLB istnieją (piny zweryfikowane 4/4: 192374/193207/193313/193684, SHAs w
  INPUT_IDENTITIES.json). Porównanie po jawnej konwersji `(x,y,z) -> (x,z,-y)`:
  **4/4 EXACT_AGREEMENT** (bit-exact pozycje + unoriented trójkąty; bounds identyczne;
  0 mismatch keys; np. 193313: 5 geoms / 2384 verts / 1192 tris). Metoda/tolerancja/jednostka
  zapisane; **zgodność unoriented triangles NIE potwierdza windingu, materiałów ani lineage
  konwertera**. Nazwa `_textured.glb` nie jest dowodem tekstur — cztery modele pozostają
  **UNTEXTURED_PROXY** (brak UV/bindings; images census 0). Surowe:
  raw/CAM_C1_GLB_COMPARE.json + QC rerun w 00_CONTROL_INTERNAL_QC/raw/CAM/.
- **CAM-C2 — FAILED is not a measurement** (naprawa `tools/pecompat/catalog_data.mjs`):
  obecność `_batch` nie wystarcza do `complexity.unknown=false`. FAILED pozostaje UNKNOWN
  z powodem; wspólny model statusu = jedna definicja dla API/UI/testów.
  **Baseline 1572 zmierzonych complexity (PCG 1568 + CD 4) MATCH przez REAL build** —
  to kontrola baseline, nie hardcode (0 wystąpień 1572 w kodzie produkcyjnym).
  **FAILED rows: 3270/3270 — wszystkie complexity.unknown=true z powodem** (czysta liczba;
  dawny fałszywy wynik 4842 doliczał 3270 FAILED jako „decoded”). Rozdział wpisów:
  21,302 wpisy czterech archiwów; katalog modeli 8,088.
- **CAM-C3 — pełna tożsamość cache w PRODUKCYJNEJ ścieżce**: `(era, containerSHA256,
  entryName, payloadSHA256)` + wersja/schema dekodera, weryfikowane przy KAŻDYM hit
  (tiles / texture edges / pinned batche / modele). Mutanty wrong era / wrong containerSHA /
  wrong texture-edge era / brak envelope → **REFUSED z nazwanym powodem** przez REAL loader
  (M1 ROW_ERA_MISMATCH, M2 ROW_CONTAINER_SHA_MISMATCH, M3 EDGE_ERA_MISMATCH,
  CACHE_IDENTITY_ENVELOPE_MISSING); clean przechodzi ten sam gate (batch 4838, edges 1545,
  0 drops). Kontrola syntetyczna ≠ zarzut skażenia historycznego runu. Focused QC A PASS
  przed użyciem katalogu/cache w launcherze.

### Etap B — Gamebryo research podporządkowany implementacji

Skill `pe-gamebryo-rosetta` istniał od poprzedniego runu; ROZSZERZONY w tym runie o rozdział
terrain/materials/foliage: `references/terrain-foliage-integration.md` (NEW) + status
DELIVERED w SKILL.md (P3-2 fixed at persistence). **GAMEBRYO_MECHANISMS_IMPLEMENTED = 5**:
(1) stream/register/load/link + custom NiArk; (2) local/world transforms + hierarchy;
(3) textures/UV/material bindings; (4) shared geometry + separate instances;
(5) scene load/unload management. Każdy mechanizm: SOURCE+VERSION+SHA → OBSERVED SDK
BEHAVIOR → PE EVIDENCE OR GAP → ADAPTER DECISION → EXECUTED CONTROL
(GAMEBRYO_MECHANISM_MAP.md). Wiedza SDK ≠ wiedza o PE (scope labels wszędzie);
źródła SDK nie opublikowane (piny + omówienia tylko).

### Etap C — launcher z prawdziwą heightmapą (terrain)

- Index census (dwie niezależne enumeracje): **58,451 = 51,920 regular (220×236) +
  6,530 special rows (gridY 0xff5a..0xffff) + 1 sentinel (7ffe7ffe.tdf) + 0 other**.
  Special rows: semantyka UNRESOLVED — wykluczone LOUDLY z adresowania regularnego
  (nigdy nie renderowane, nigdy nie liczone jako NODATA). Sentinel: production decode
  odmawia (nie standardowy 32×32); Range check odmawia współrzędnych (32766,32766).
- **HEIGHTMAP_COVERAGE = 51,920/51,920 = 100%** (production decode każdego regularnego
  kafla, min/max/mean raw u16 + status; async ~1.9 s); **NODATA = 0** (0 missing + 0
  decode-failed). 22,481 kafli all-zero (43.3%) to DANE (status=1), nie NODATA.
  Overview: jawnie downsampled 1px/tile (binarna 363,440 B: mean/min/max/status per tile);
  hover/wybór pokazuje **raw uint16**. Zakres 0..65535; max-mean tile = 00350072.tdf
  (53,114) → domyślny spawn (wybór z danych, nie zgadywanie nazw miast).
- TDF invariant: wysokości od payload offset **64** (negatywna kontrola offset-52
  dyskryminuje: 6/6 kafli testowych, QC 3/3 własnych odczytów bajtów); exact 1024 heights;
  raw u16 BEZ normalizacji/smoothingu/seam-maskingu; hash witness terrain.bnt przed i po
  całej baterii == pin (oryginały READ_ONLY).
- **TERRAIN_RENDER**: okno/patch **8×8 = 64 aktywne kafle** strumieniowane wokół kamery
  (limit 64 aktywnych, kontrolowana pamięć); brak danych zatrzymuje ruch/pokazuje granicę.
  Kalibracja CURRENT_RUNTIME_CALIBRATION (u16/128, 2 m/próbkę, identity min/max) zastosowana
  DOKŁADNIE RAZ, odwracalna (meters×128 == raw u16; A-128). Kolejność ładowania:
  byte-identical region (reverse-order invariance).

### Etap D — oryginalne tekstury terenu

- **6/6 kroków łańcucha proven** (WORLD_DATA_PROVENANCE ETAP_D_MATERIAL_CHAIN): TDF
  entry+record (maska@record+56; negatyw 52 odmawia na RAW 12/12; RLE exact consumption)
  → id@+16 → `<id>.dat` (relacja engine-RE CONFIRMED: M1_TSFS iter015e/f + iter030,
  EU935 census probe05; re-measured per sample; **NIE name-match** — id↔name jest
  MANY-TO-MANY, nazwy to display metadata) → PCG Textures.bnt payload (LAZY bounded, pin
  fail-closed, 8,381/8,381 entries) → decodeTga2 (strict TGA2 24bpp subset; malformed/RLE
  FAIL LOUDLY; ten SAM dekoder serwowany do przeglądarki) → RGBA → GPU DataArrayTexture
  (raw weights bit-exact; slot order = record order) → widoczny materiał.
- **TERRAIN_TEXTURES (final window, browser-observed): resolved 615/615 warstw (0
  unresolved), 28 zdekodowanych tekstur in-window (29 distinct ids across gate samples),
  applied 114,019 slotów.** Liczniki resolved/decoded/applied/browser-observed rozdzielone.
  Unresolved binding = jawny diagnostyczny skip+list, nigdy losowa zielona tekstura
  (999999999 → 404). Wrong era → 403 ERA_REFUSED przez REAL routes.
  **RENDER_RECONSTRUCTION preset** (sequential lerp per layer by RAW mask/255 in RECORD
  ORDER — era-evidenced form z LOD vertex-tint bake; UV repeat 32 m global — analogia,
  brak dowodu PE; sums >255 NIGDY nie normalizowane — raw weights preserved bit-exact).
  Texture toggle realnie zmienia teren (patrz PIXEL_RENDER).

### U-19 — the splat fix (QC P2-1 + drugi, dominujący defekt; oba FIXED + revalidated)

Dwa defekty w SPLAT_FRAG (`compat/world-app.js`, te same ~16 linii shadera):
(a) współrzędna warstwy sampler2DArray używała znormalizowanego bajtu idx zamiast NUMERU
warstwy (root cause P2-1, potwierdzony na poziomie kodu); (b) **blend factor był
podzielony dwukrotnie** (`w0.x / 255.0` na już znormalizowanej wadze → czynnik 1/255×
za mały → kolaps do ~tex×0.004 = DOMINUJĄCA przyczyna near-black; znaleziona w tej rundzie
korekcyjnej, uczciwie ujawniona). Fix: decode `floor(i*255.0+0.5)` → layer k; guard
empty-slot na wartości zdekodowanej; waga = RAW as fetched.

**Dowód (real headless GPU session, ANGLE/WARP): WORLD_U19_PER_COLOR_EXACT — 36/36 próbek
per-color w spanie** (36 distinct cells; mean max-channel delta **0.55/255**, max 1.39/255 —
fp32 bilinear rounding floor; oczekiwane kolory policzone NIEZALEŻNIE w Node z tych samych
payloadów wire + camera pose cross-check z HUD strony). **WORLD_U19_PRE_FIX_BEHAVIOR_REJECTED**
— zachowanie pre-fix NIE pasuje do odczytanych pikseli (34 discriminating, mean delta
65.95) — brama, która dowodnie pada na stanie zepsutym i przechodzi na naprawionym.
Near-black resolution: canvas **370 → 65,240 unikalnych kolorów** (lumaMean 12.2 → 90.67;
uniqueColorsGain 64,870). RAW weights / preset / data paths untouched. Surowe:
raw/WORLD/WORLD_SPLAT_PER_COLOR_U19FIX.json + PIXEL_RENDER_U19FIX.json.

### Etap E — roślinność (deterministic preview z oryginalnych danych)

- **Trzy rozdzielone warstwy** (UI + artifacts): ORIGINAL_CLIMATE_RECORDS (strict .vcl,
  31 DECODED + **25.vcl UNSUPPORTED** — comma tokens („0,2” @ record 9 col 1, token 109,
  potwierdzone z surowych bajtów) — controlled UNSUPPORTED, nigdy nie konwertowane);
  RECOVERED_RNG_ARITHMETIC (PEFoliageCore — byte-identical do HEAD, wyniki odtworzone
  vs niezależna reimplementacja formuł); INSTANCE_DISTRIBUTION = **reconstruction-only**
  (LAB_SEED-keyed wrapper `src/peworld/PEFoliageLabSeed.js` jako stand-in [P-CELLSTREAM]).
- **CLIMATE_PROFILE = 0** — wybór MEASURABLE (nie „historyczny biom”): DECODED, 12 niepustych
  rekordów, 10 distinct modeli, zawiera witness 457485 (importer cross-validowany
  bit-exact vs R61 oracle). **LAB_SEED** wpływa na rzeczywiste rozmieszczenie (inny seed →
  inny hash pozycji); **p3 = 0 pokazane OSOBNO** ([P-RNG-P3] UNVERIFIED; nigdy ≠ LAB_SEED).
- **VEGETATION_MODE = RECONSTRUCTION_PREVIEW.** Determinizm: repeat-seed → identyczny
  instance-set SHA-256; changed-seed → inny hash I inne pozycje; streaming-order invariance
  (16 kafli, dwa porządki → identyczny union); edge ownership bez duplikatów
  (half-open tile box); drop-and-regenerate → ten sam zestaw.
- **VEGETATION_INSTANCES = 2304/2304/0** (zadane/wyrenderowane/ograniczone @ density 50,
  okno 8×8; census line w DOM). Cap case (profile 1 @ 100%): **6144/5000/1144** — twardy
  limit 5000 liczony uczciwie.
- **VEGETATION_MODELS = 8 textured / 2 honest-untextured / 0 parse-unsupported** (profile 0):
  witness **457485** (16v/8t, texture **457490** TGA2 A32) + 436293/436300/436223/457699/
  457579/457523/457532; dwa honest-untextured: 166878, 166897 (texture 166881 to DDS —
  poza strict subsetem, głośna odmowa, neutral gray + diagnostyka — NIGDY fallback tekstura
  ani stock pine pod tym samym ID). Non-visual Bip01/Box shapes liczone, nie renderowane.
  Resource discipline: window A→B→A bez refetch (object identity), profile-change disposals,
  teardown czyści cache.

### Browser evidence + regression (summary; full: BROWSER_SMOKE.md + TEST_RESULTS.json)

- **APP_LOAD = PASS** (T9 fixed 5-conjunct gates, real headless Edge): /launcher 8/8 markerów
  (entry button label exact „Uruchom podgląd świata”; era; mianownik 51 920; coverage;
  VEGETATION_MODE; three-way separation; UNSUPPORTED-25 widoczne) i /world 9/9 (64-tile
  window census; adapter units; raw u16; census żądane/wyrenderowane/ograniczone; p3
  separate; no „oryginalne XYZ”). Suite servers + standing server 8162.
- **PIXEL_RENDER = PASS** (honest label: pixel-content heuristic; PNGs PRIVATE ONLY):
  per-color 36/36; **toggles realnie zmieniają obraz: texture 48.86% pikseli canvas
  różni się (153,375/313,900, meanAbsChannelDelta 62.43), vegetation 6.26%
  (19,646/313,900)** — no-op toggle by FAILował.
- **INTERACTION_VERIFIED = NOT_PERFORMED** — demon automatyzacji (9222) down przez cały
  run; kontraktowa lista kroków interaktywnych pozostaje OPEN GATE (BROWSER_SMOKE.md).
- **REGRESSION = world 44/44 + catalog 41/41 + unit 24/24 + app 22/22** (wszystkie po
  U-19 fix, z raw/ re-runów; 218757 app byte-identical; src/pesource ZERO zmian).

### Fresh internal QC (INTERNAL_REVIEW.md) + korekty

QC = **PASS_WITH_FINDINGS** → wszystkie rozstrzygnięte w rundzie korekcyjnej:
P2-1 (U-19) → FIXED + revalidated (per-color 36/36; oba defekty); P3-1 (transkrypcja
0xff1a→0xff5a w 4 miejscach) → naprawione przez QC + **adjudicated REPAIR_ACCEPTED przez
PE-MASTER z własną weryfikacją hashy POST** (launcher.js 3C58E5A6…, launcher.html
3BFA152…, terrain-foliage-integration.md 0C5C78E0…; jedyna rezydualna 0xff1a to
legitymacyjna historyczna nota w WORLD_DATA_PROVENANCE dokumentująca samą measured
correction); P3-2 → skill status DELIVERED; **P3-3 → TEN raport niesie czystą liczbę
3270/3270** (bez draft relic „3270/3274?”). PE-MASTER review: MASTER_ACCEPTED (advisory),
CANONICAL_GATE_EFFECT = NONE — pełny tekst verbatim: PE_MASTER_REVIEW.md.

---

## 3. The §10 terminal measured block

```text
RUN_ID            = PE_WORLD_LAUNCHER_R1_20261010
RESULT_BRANCH     = codex/pe-world-launcher-r1-20261010
BASE_SHA          = e9bb1f5120444f8bafd7d90c426f9e64d6b9bf2c
                    (BASE_DECISION: contract EXPECTED f71eb30a IS an ancestor; delta =
                    EXACTLY ONE human-authorized commit — CAMERA_UX_FIX; disclosure §1
                    above + AUTHORIZATION_AND_PREFLIGHT.md §3; never a silent adaptation)
RESULTING_SHA     = the single run commit — discover: git rev-parse HEAD in the worktree
                    (self-exclusion precedent: the report cannot embed its own commit's
                    hash; verified == pushed value in the run's terminal handoff)
REMOTE_FEATURE_SHA= after push — git ls-remote origin refs/heads/codex/pe-world-launcher-r1-20261010
                    (must equal RESULTING_SHA; equality verified at push by the
                    persistence phase; the measured value is in the terminal handoff)
SERVER_URL        = http://127.0.0.1:8162/  ( / -> 302 /launcher )
SERVER_PID        = 24964
START_COMMAND     = npm run serve:world   (cwd = D:\Eudoria_Reconstruction\12_WebGame\pe-world-launcher-r1; PID printed at startup)
STOP_COMMAND      = Stop-Process -Id 24964   (own process only)
CAM_C1            = RETRACTION EXECUTED over NO_GLB_PRESENT_FOR_THESE_IDS: 4/4 GLB
                    EXACT_AGREEMENT after explicit (x,z,-y); method/tolerance recorded;
                    unoriented agreement does NOT confirm winding/materials/lineage;
                    the four stay UNTEXTURED_PROXY (0 images)
CAM_C2            = FIXED: FAILED is not a measurement; shared status model; baseline 1572
                    measured (PCG 1568 + CD 4) through the REAL build; FAILED rows
                    3270/3270 all complexity.unknown=true with reason; no hardcode
CAM_C3            = FIXED: full cache identity (era, containerSHA256, entryName,
                    payloadSHA256, decoder/schema version) verified in the PRODUCTION
                    path incl. texture edges + batches + models; 3+ mutants REFUSED by
                    named reason through the REAL loader; clean PASSES the same gate
HEIGHTMAP_COVERAGE= 51,920 / 51,920 = 100% measured (production decode of EVERY regular
                    tile; min/max/mean raw u16 + status); NODATA = 0 (0 missing entries +
                    0 decode failures); 22,481 all-zero tiles are DATA (43.3%) not NODATA;
                    special rows 6,530 (gridY 0xff5a..0xffff) + sentinel 1 (7ffe7ffe.tdf)
                    EXCLUDED LOUDLY from regular addressing (58,451 total index entries);
                    overview downsampled explicitly 1px/tile (363,440 B binary), hover =
                    raw uint16
TERRAIN_RENDER    = 8x8 = 64 active tiles streaming around the camera (patch origin 4x4 ->
                    64 max; controlled memory); heights from original u16 samples at
                    payload offset 64 (52-discriminating negative; exact 1024 heights;
                    raw preserved, no smoothing/normalization/seam masking); calibration
                    CURRENT_RUNTIME_CALIBRATION applied EXACTLY ONCE, reversible;
                    NODATA stops movement/shows the boundary; reverse-order invariance
TERRAIN_TEXTURES = resolved 615/615 layers in-window (0 unresolved; 23 distinct ids in
                    the window probe, 29 across gate samples) / decoded 28 distinct
                    in-window / applied 114,019 slots / browser-observed (DOM census line
                    + U-19 per-color proof 36/36 on the standing-server code); mask@56;
                    id@+16 -> <id>.dat engine-RE-confirmed; strict TGA2 decode; raw
                    weights preserved (sums>255 never normalized); RENDER_RECONSTRUCTION
                    preset; texture toggle changes 48.86% of canvas pixels
CLIMATE_PROFILE   = 0 (MEASURED choice: DECODED, 12 non-empty records, witness 457485 in
                    the model set — never "the historical biome of this place");
                    25.vcl controlled UNSUPPORTED (comma tokens, never converted);
                    indices 0..31 shown with real model ids/scales
LAB_SEED          = documented wrapper (src/peworld/PEFoliageLabSeed.js — the
                    [P-CELLSTREAM] stand-in; PEFoliageCore byte-identical/untouched);
                    determinism proven (repeat-seed identical SHA-256, changed-seed
                    different hash AND positions, streaming-order invariance, edge
                    ownership, cap respected); p3 = 0 shown SEPARATELY (never == LAB_SEED)
VEGETATION_MODE   = RECONSTRUCTION_PREVIEW
VEGETATION_MODELS = 8 textured / 2 honest-untextured (166878+166897: DDS 166881 refused
                    loudly outside the strict subset) / 0 parse-unsupported; witness 457485
                    rendered with its original texture 457490 (bit-exact chain)
VEGETATION_INSTANCES = 2304 requested / 2304 rendered / 0 limited (density 50, window
                    8x8); cap case measured: 6144 / 5000 / 1144 (profile 1 @ 100%)
GAMEBRYO_MECHANISMS_IMPLEMENTED = 5 (stream/register/load/link+NiArk; transforms+hierarchy;
                    textures/UV/materials; shared geometry+separate instances; scene
                    load/unload) — each with SOURCE+SHA -> SDK behavior -> PE evidence/gap
                    -> adapter decision -> executed control
SKILL_UPDATED     = YES (.opencode/skills/pe-gamebryo-rosetta: NEW
                    references/terrain-foliage-integration.md + the world-launcher lineage
                    status DELIVERED + explicit UNKNOWNs)
APP_LOAD          = PASS (T9 fixed 5-conjunct gates on real headless Edge: /launcher 8/8 +
                    /world 9/9 page markers; suite servers + the standing server)
PIXEL_RENDER      = PASS (honest label: pixel-content heuristic; PNGs PRIVATE ONLY):
                    U-19 per-color proof 36/36 (mean max-channel delta 0.55/255) with the
                    pre-fix behavior rejected (65.95); near-black resolved 370 -> 65,240
                    unique colors; texture toggle 48.86% pixels differ; vegetation toggle
                    6.26% pixels differ
INTERACTION_VERIFIED = NOT_PERFORMED (automation daemon down — honest; the contract's
                    interactive step list stays the OPEN GATE; headless per-color proof is
                    NOT interactive verification)
REGRESSION        = world 44/44 + catalog 41/41 + unit 24/24 + app 22/22 (all re-run after
                    the U-19 fix; 218757 app byte-identical; src/pesource ZERO changes)
MANIFEST_BIJECTION = VERIFIED (MANIFEST_SHA256.csv generated LAST over the physical
                    package minus itself; independent bijection verification: no
                    duplicates/missing/extra; every size+SHA256 matches)
OPEN_FINDINGS     = (1) INTERACTION — the interactive browser smoke (launcher -> map ->
                    enter -> toggles -> walk) NOT_PERFORMED: the single standing open gate
                    of this product; (2) interactive/textured-terrain appearance on a
                    real GPU stays UNVERIFIED (the per-color proof is headless
                    ANGLE/Microsoft Basic Render Driver); (3) historical CELL-STREAM SOURCE
                    (U-1), CLIMATE->REGION mapping (U-2) and original p3 (U-12) remain
                    UNKNOWN — INSTANCE_DISTRIBUTION stays reconstruction-only; full list
                    U-1..U-20 with dispositions: CALIBRATION_AND_UNKNOWNS.md
PRODUCT_VERDICT   = PASS_IN_IMPLEMENTED_SCOPE
HISTORICAL_TREE_DISTRIBUTION  = NOT_ESTABLISHED
HISTORICAL_BUILDING_PLACEMENT = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED           = NO
FULL_ORIGINAL_GAME_REIMPLEMENTED = NO
CANONICAL_GATE_EFFECT          = NONE
NEXT_EXPERIMENT_AUTHORIZED    = NO
INDEPENDENT_DESKTOP_POST_AUDIT = PENDING
HARD_STOP                      = YES
```

## 4. Standing flags (frozen) + what stays honest

- Era discipline: **PCG_9_3_5** świat; CD_2003 (CD_JAN_2003 w warstwie źródeł) tylko
  katalog/porównanie; wrong-era refusals CONTROLLED (403 przez real routes).
- Zero twierdzeń historycznych: brak historycznego seedu/liczby drzew/biomu/placementu
  (INSTANCE_DISTRIBUTION = reconstruction-only; three-way separation w UI);
  pozycje w jednostkach adaptera + tile key; surowe u16 bez modyfikacji.
- Historyczne pakiety (f71eb30 docs), AUDIT_ENTRYPOINT, PROJECT_STATE, milestone/gates,
  master (3fbe93e…), obce worktree — NIERUSZANE. CAM-C1 retraction żyje w TYM pakiecie.
- Oryginalne kontenery/NIF/GLB/tekstury/PNG/SDK — PRIVATE ONLY (pat+SHA references);
  repo zawiera kod, testy syntetyczne, omówienia i metadane.
- **HARD_STOP = YES**: kontrakt wykonany do działającego wycinka; serwer podglądu
  zostawiony uruchomiony (§10); żaden nowy experiment nie jest autoryzowany.
