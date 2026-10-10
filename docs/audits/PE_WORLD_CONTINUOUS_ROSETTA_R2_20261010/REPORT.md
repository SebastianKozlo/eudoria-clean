# REPORT — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010

Data: 2026-10-10. Repo `SebastianKozlo/eudoria-clean`, branch
`codex/pe-world-continuous-r2-20261010`, BASE = EXACT `44ef254b8ff9ebb05bd104690181c202678c065d`
(`codex/pe-world-launcher-r1-20261010`, świeży ls-remote zgodny przed startem
i przed commitem). Worktree `12_WebGame/pe-world-continuous-r2`. Serwer live:
`http://127.0.0.1:8163` (launcher `/launcher`, świat `/world`, Asset Lab
`/assetlab`).

**Werdykt wykonawczy: COMPLETED w zbadanym zakresie implementacji, z
uczciwymi ograniczeniami wymienionymi w tym raporcie (żadnych FAILED bramek
wymaganych; bramki oddzielne poniżej — nie „wszystko PASS”).**

## 1. Co wykonano (kontrakt §0–§7)

1. **PRE (§2)**: wszystkie sześć findings WL-1..WL-6 odtworzone NA
   RZECZYWISTYCH funkcjach produkcyjnych BASE (`PRE_COUNTERCHECKS.json`;
   narzędzie `tools/pecompat/world_r2_counterchecks.mjs`):
   WL-1 latest-request LOST; WL-2 (2304 instancje, 14 poza siatką, 1275
   niezerowych różnic, max 0.953125, walk↔triangle max 15.8203125); WL-3
   (100,10,100)→(100,10,88); WL-4 dryf okna (53,114)→(68,129); WL-5
   (11 kafli opróżnionych, 4 grupy nakładające się 166878, 3 ID przy 50%);
   WL-6 (parent e9bb1f5 pomierzony świeżo; LITERAL_ORIGINAL_BASE_GATE_
   COMPLIANCE=FAIL zachowane). `R1_RECORD_SUPERSESSION.md` zapisuje cofnięcie
   szerokiego product PASS R1 do PARTIAL/REQUIRE_CORRECTIONS (bez
   retroaktywnej autoryzacji, bez edycji starego pakietu).
2. **§3.1 latest-request**: jedna tożsamość żądanej sceny (era+kontenery+
    focus+profil/seed/gęstość+wersje); gen-id w terenie/teksturach/roślinności;
    abort-before-apply + dispose wyników przestarzałych; kolejka latest-wins
    (pendingOrigin w terenie; [SUPERSEDED w rundzie korekty 2026-10-10: w
    roślinności produkcja używa teraz kolejki latest-wins NA POZIOMIE
    WRAPPERA world-app.js#rebuildVegetation — pierwotne twierdzenie
    „WorldVegetation wewnętrznie" było nieosiągalne z ścieżki produkcyjnej
    (P1-2 QC); klasa nietknięta, jej kolejka pozostaje warstwą
    bezpieczeństwa; patrz CORRECTIONS.md P1-2]); dedupe dla
    powtórzonych identycznych żądań (bez niego ~400 ms tick wiecznie
    unieważniałby przebudowę — zmierzone w sesji). Spójność pokazana uczciwie
    („teren A + drzewa B” nigdy READY).
3. **§3.2 jedna wysokość**: `src/peworld/PEHeightQuery.js` — PEHeightField:
   DOKŁADNIE renderowane trójkąty warstwy bliskiej (ten sam podział quada co
   PETerrainRegion.buildGeometry), surowe u16, kalibracja RAZ, bez
   wygładzania. Halo 1 kafla RZECZYWISTYCH sąsiednich próbek (10×10 dla okna
   8×8) rozwiązuje granicę 256-próbek/0..510 vs generator 0..512: wszystkie
   instancje mają realną powierzchnię (POST: 0 DEFERRED w oknie domyślnym),
   fallback y=0 USUNIĘTY z produkcji (POST: brak `? 0 :` w apply). Statusy
   instancji: PLACED/DEFERRED_NO_SURFACE/UNSUPPORTED_MODEL/LOD_LIMITED.
   Ruch: kandydat → sprawdzenie powierzchni → commit; brak danych = stop na
   ostatniej bezpiecznej pozycji + odróżnienie LOADING od CORPUS_EDGE;
   blur/utrata locka/zmiana trybu czyszczą klawisze; odrzucenie pointer
   locka ma widoczny komunikat + działający drag-look (CDS raw-key + drag
   mouse: S4).
4. **§4 ciągły świat**: near 8×8 RAW + mid ring 40×40 (8×8-decymowane
   RZECZYWISTE próbki/kafel, bloki /api/world/lod8) + far cały świat
   (4×4-decymowane, census-gated /api/world/far, zbierane PRZEZ census
   serwera). Linie cięcia poziomów = TE SAME oryginalne próbki (bez szwów,
   bez skirtów, potwierdzone geometrycznie). Brakujące kafle = jawne dziury
   (status byte, nigdy zero-powierzchnia). Mianownik ZMIERZONY z indeksu
   (51 920 zwykłych; pojemność siatki 220×236 oddzielnie). Skoki =
   teleport w UI (najpierw dane celu). Budżety: prealokowane bufory far
   index + drawRange; far normals liczone RAZ (pozycje statyczne).
5. **§5 kamera/UI**: preset referencji 9350: FOV 45, damping 0.08,
   minDistance 10, maxDistance 50000, far 200000 (near 0.5 +
   logarithmicDepthBuffer — uzasadniony wybór skali świata; nie twierdzenie
   historyczne). Streaming podąża za FOCUSEM (orbit: controls.target) —
   F/Reset stabilne ×3 (zmierzone: 3× identyczny origin). Przejścia
   1/2/3 bez skoku miejsca (max XY jump 0). Layout: canvas ≥85%×80%
   (zmierzone w S1), zwijany drawer „Szczegóły” (domyślnie zwinięty,
   zapamiętywany w localStorage), bez stałego sidebara 480px, bez
   nakładających się pasków; pola drawer NIE przechwytują klawiszy ruchu
   (S6 PASS); resize bez resetu kamery, drawing buffer podąża (S9 PASS).
6. **§6 roślinność**: PEFoliageCore BYTE-IDENTICAL (PRE vs POST SHA
   300be913…, zweryfikowane). recIndex w hashu pozycji (0 grup
   nakładających — POST). Gęstość frakcyjna floor+stable-hash (klucz
   tile/cell/record/model, BEZ labSeed — seed przesuwa pozycje, gęstość
   steruje liczbą; 5 ID przy 50% zamiast 3; monotoniczność d0≤d25≤d50≤d100
   i inkluzywność ID zmierzone). Fair cap: largest remainder + ≥1 dla
   każdego niepustego kafla (0 opróżnionych; order-invariant; suma DOKŁADNIE
   5000). Regional RECONSTRUCTION_PREVIEW: NASZA deterministyczna mapa
   (region=tile>>5; profile 0/2/7/19 — wszystkie DECODED; okno na granicy
   regionu używa 2 profili [7,19], zmierzone). Census per model/kafl +
   statusy + slot diagnostics. **Dwa nieobsłużone formaty tekstur
   zbadane na rzeczywistych wejściach**: DDS DXT1 (518860/518862/516807 —
   sloty BASE witnessa 519316) i DDS DXT5 (166881 — tekstura modeli
   166878/166897, wcześniej jedyne „untextured” profile 0): SKWALIFIKOWANE
   strict-subset dekoderem `src/pesource/DdsDecoder.js` (gates: magic/size/
   fourcc/top-mip-only; kontrole negatywne: truncated/wrong-fourcc/tga-refused
   — WORLD R2_DDS_QUALIFIED PASS). Profil domyślny jest teraz w pełni
   teksturowany (0 untextured w census). Cztery proxy CD
   192374/193207/193313/193684 pozostają SOURCE-UNTEXTURED (kontrola;
   bez wymyślonych bindingów).
7. **§7 wykonywalna Rosetta + Gamebryo**: czytniki/mount/adapter bez
   przepisania; WorldAssembler-lite (world-lod.js) nad nimi. Punkt debug
   (klik teren/model): era+containerSHA+wpis/payloadSHA→dekoder→obiekt
   sceny→polityka (drawer). Źródła Gb12 przeczytane selektywnie
   (NiStream/NiNode/NiAVObject.inl/NiTexturingProperty/NiSourceTexture/
   BackgroundLoad/MOUT TerrainManager — SHA w GAMEBRYO_IMPLEMENTATION_
   LINKS.md); każde użycie: źródło→mechanizm→dowód PE/GAP→decyzja
   adaptera→wykonany test. ZERO bajtów SDK w repo; brak „100% Gamebryo
   understood”. Asset Lab: witness PCG 519316 NA ŻYWO (parseWitnessModel →
   3 kształty, 3/3 TEKSTUROWANE przez łańcuch slotów; sześć nazw tekstur
   rozwiązywanych do RZECZYWISTYCH wpisów tej samej ery: 518860/518862/
   516807 DXT1 + 519227 TGA A32) + 4 proxy CD jako KONTROLA (bounded nif41
   reader SERVER-side — importuje node:fs — przeglądarka renderuje wire;
   SOURCE-UNTEXTURED, era CD_JAN_2003 ODRĘBNA od PCG_9_3_5).
8. **§8 QC**: 4 baterie istniejące + nowa bramka R2: **139 PASS / 0 FAIL /
   0 NOT_PERFORMED** (world 52, unit 24, app 22, catalog 41 — wszystkie
   z pełnymi kontenerami; liczby wykonane, nie hardcode). Prawdziwa
   przeglądarka (izolowana instancja Edge headless + CDP na wolnym porcie;
   NIGDY demon 9222 ani cudze sesje): DOM/load, PIKSELE, i REALNE
   wejście (rawKeyDown/mouse events). 10 scenariuszy S1–S10 — wszystkie
   PASS, 0 nieprzechwyconych wyjątków stron.

## 2. Bramki (kontrakt §8 — oddzielne, uczciwe)

```text
DATA_READ_PATH      = PASS     (PRE/POST counterchecks na production readerach; archiwa 4/4 pin; R2_LOD_ROUTES bit-exact; niezależna decymacja)
PRODUCT_LOAD        = PASS     (T9 5-koniunkcyjne bramki /launcher + /world; S1 READY + coherence)
PIXEL_RENDER        = PASS     (11/11 capture nontrivial; vegToggle 6.06% ≥2%; textureToggle 89.7%; teleport diff 83.5% — wszystko w raw/BROWSER/)
INTERACTION         = PASS     (S1..S10 real input: fit×3 stable, mode no-jump, walk raw-W moved+Y-on-shared-surface, teleport+return same counts, drawer key guard, resize)
CONTINUOUS_WORLD    = PASS     (near+mid+far z RZECZYWISTYCH próbek; granice dopasowane; denominator measured 51920; 0 missing/failed kafli; coverage w WORLD_COVERAGE_AND_LOD.json)
ASSET_LAB           = PASS     (519316 live chain 3/3 textured + 4 CD proxy controls source-untextured z honest status; eras separate)
PERFORMANCE         = MEASURED_WITH_LIMITS (budżety prerejestrowane; wszystkie checki PASS: cache 288≤512 kafli, 23≤64 tekstur, 9≤16 modeli, heap last-route +1 MB (R4−R3: 72→73), first-to-last +3 MB (70→73; budżet last-route ≤8 MB) — pełna krzywa w PERFORMANCE_AND_LIMITS.json; NIE twierdzimy VRAM z liczników JS) [POPRAWIONE w rundzie korekty 2026-10-10: pierwotna proza „+12 MB" nie istnieje w kanonicznym PERFORMANCE_AND_LIMITS.json (lastRouteDeltaMB=1, firstToLastDeltaMB=3) — patrz CORRECTIONS.md P2-1]
```

PRODUCT_VERDICT = PASS_IN_EXAMINED_IMPLEMENTED_SCOPE (wszystkie obowiązkowe
funkcje/testy PASS w tym zakresie; otwarte limity — §5). QC_PASS nie podnosi
science: poniższe frazy pozostają.

## 3. Zachowane frazy (verbatim)

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

## 4. Ograniczenia i uczciwe luki (skrót; pełna lista w UNRESOLVED_AND_NEXT_SEAMS.md)

- Daleki LOD gotowy dopiero po census serwera (~10–120 s po starcie;
  klient pokazuje PENDING; 503 bez placeholdera zer).
- Slot tekstury modelu: PIERWSZY rozwiązywalny w kolejności wpisów =
  RENDER_RECONSTRUCTION (który slot 9.3.5 wiązał — UNRESOLVED).
- DDS: tylko top-level mip (łańcuch mipów pozostaje nieczytany,
  udokumentowane); mipsDeclared=9 dla 166881.
- Regional preview = NASZA mapa (NIE historyczny biom); profil 25.vcl
  pozostaje UNSUPPORTED (bez konwersji przecinków); modele bez łańcucha
  texprop→Ark pozostają NIE-wizualne (liczone, nie renderowane); markery
  UNSUPPORTED_MODEL to diagnostyka, nie oryginalny model.
- Asset Lab: witness 519316 to pojedynczy kontrolny PCG (nie „wszystkie
  NIF-y”; ALL_NIFS_SUPPORTED = NOT_ESTABLISHED); 225492.nif (NiTexture-
  TransformController) poza zakresem tego runu — bez nowych rodzin loaderów.
- Okno mid 40×40 kafli: dalej „brak danych” poza halo 10×10 (ruch stopuje
  uczciwie dopóki okno nie podąży); fullscreen far nie zastępuje bliskiego
  detalu.
- WL-5 przy gęstości 50% (ZMIERZONEJ — census config densityPercent=50;
  [POPRAWIONE w rundzie korekty: pierwotna etykieta „100%" była błędna —
  pomiar 16324→5000 wykonano przy density 50, collect narzędzia ustawia
  densityPercent: 50 dla wszystkich trzech okien]): fair cap LOD_LIMITED
  liczone jawnie (16324→5000 w oknie regionalnym — census pokazuje cenę
  limitu per kafl/model).

## 5. Paczka i persystencja

Zmienione ścieżki (census przed commitem; 25 wpisów git = 12 MODIFIED +
13 NEW): MODIFIED — compat/launcher.html, compat/server-world.mjs,
compat/world-app.js, compat/world-vegetation.js, compat/world.html,
compat/world.css, src/peworld/PEFoliageLabSeed.js,
tests/pecompat/run_world_tests.mjs,
tests/pecompat/witness_457485_regression.test.mjs,
tests/pecompat/world_headless_load.test.mjs,
tests/pecompat/world_vegetation.test.mjs,
.opencode/skills/pe-gamebryo-rosetta/SKILL.md; NEW — compat/world-lod.js,
compat/assetlab.html, compat/assetlab.js,
src/peworld/PEHeightQuery.js, src/pesource/DdsDecoder.js,
tests/pecompat/world_r2_gates.test.mjs,
tools/pecompat/world_r2_counterchecks.mjs,
tools/pecompat/world_r2_browser.mjs,
tools/pecompat/world_r2_pixel_diff.mjs,
tools/pecompat/world_r2_performance.mjs,
tools/pecompat/world_r2_census_collect.mjs,
tools/pecompat/world_r2_collect_test_results.mjs,
docs/audits/PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010/ (pakiet 35 plików =
34 + MANIFEST_SHA256.csv). .gitignore BEZ zmian (istniejące ignores
(*.png/*.log/*.bnt/*.ark/*.tdf/…) już pokrywają wszystkie wykluczenia —
żaden nowy typ binarny nie wchodzi do repo). PEFoliageCore / PETerrainCore /
NifModelReader / stary katalog 218757 — nietknięte (T6 gate: reader
byte-identical z BASE; jedyny nowy plik w src/pesource to allowlistowany
DdsDecoder.js). Zero payloadów proprietary w repo (manifest sprawdzony
na rozszerzenia binarne). Historyczne pakiety (CITY_ASSET_MAP_R1,
WORLD_LAUNCHER_R1) zweryfikowane byte-clean przy stagingu (przywrócone
pomocnicze dumpy z domyślnych katalogów harnessów; patrz INTERNAL_REVIEW).

MANIFEST_SHA256.csv: pełna bijekcja (wszystkie fizyczne pliki pakietu poza
manifestem, dokładnie raz, size+SHA). [SUPERSEDED w rundzie korekty
2026-10-10: twierdzenie „zweryfikowana dwukrotnie" było FAŁSZYWE dla
opublikowanego stanu — QC znalazło mismatch wiersza REPORT.md (manifest
12408/95650dbc… vs plik 12410/EFCA8566…; P1-1); manifest został
ZREGENEROWANY ze stanu finalnego pakietu korekty i zweryfikowany dwiema
NIEZALEŻNYMI metodami w commicie korekty — patrz CORRECTIONS.md P1-1.]

## 6. Runda korekty (2026-10-10, po INTERNAL_QC_PE_MASTER_AUDITOR)

Po publikacji b4dfae7 fresh-context internal QC (QC_PASS_WITH_FINDINGS,
REQUIRE_CORRECTIONS) wykazał 2×P1 + 5×P2 + 4×P3. Zbindowana runda korekty
(nowy commit NA WIERZCHU b4dfae7, bez amend/force; kontrakt §9) naprawiła:

- **P1-1 manifest bijection** — manifest zregenerowany ze stanu finalnego;
  pełna bijekcja zweryfikowana DWIEMA niezależnymi metodami (self-check
  generatora + osobny re-hash w PowerShell; patrz CORRECTIONS.md).
- **P1-2 veg latest-wins w PRODUKCJI** — wrapper `rebuildVegetation` przenosi
  kolejkę latest-wins na poziom produkcji: nowsze żądanie podczas busy jest
  ZAPISYWANE (vegPending), dostarczane po zakończeniu bieżącego buildu;
  wygrywający census commitowany gen-gated vs requestId (coherence.veg);
  dedupe identycznych powtórzeń; klasa WorldVegetation/PEFoliageCore
  NIETKNIĘTE (byte-identical). PRE (b4dfae7, SHA ce691ec3…) i POST (fix)
  zmierzone narzędziem `world_r2_correction_counterchecks.mjs` (ten sam
  narzędzi w obu fazach): PRE — B ginie przed klasą, census/coherence nie
  odzwierciedlają B, READY nieosiągalne; POST — B dostarczone
  (delivery A→B), census B commitowany, coherence.veg=B, READY osiągalne,
  dedupe i gen-gate trzymane (CORRECTION_COUNTERCHECKS.json). Nowa bramka
  baterii R2_VEG_WRAPPER_LATEST_WINS (ścieżka PRODUKCYJNA, ekstrakcja
  verbatim + VM) + rozszerzenie kontrczeka WL-1 o ścieżkę wrapperową.
- **P2** — REPORT perf +12→kanoniczne +1/+3 MB; etykieta gęstości 100%→50;
  PID serwera (RUN_AND_STOP/HANDOFF) odświeżony z łańcuchem restartów;
  pola census HANDOFF (src/pesource = 1 NEW plik DdsDecoder.js; .gitignore
  bez zmian — puste diff); notka o semantyce pola PRE
  y0FallbackInProductionApply i nieprzypiętym wariancie narzędzia PRE
  (CORRECTIONS.md P2-5/P3c — uczciwie: dokładny wariant PRE nie istnieje,
  oryginalne pola PRE są spójne wewnętrznie i przypięte SHAs źródeł).
- **P3** — (a) harnessy testowe: domyślne raw-dirs do NEUTRALNEGO katalogu
  tymczasowego (przypadkowe wywołanie nie może brudzić historycznych
  pakietów READ_ONLY; weryfikacja: baterie bez flag = 0 zmian w docs/);
  (b) INPUT_IDENTITIES: Models.ark null-e wypełnione pomiarem
  (128742137 B / F660D055…); (c) patrz P2-5 wyżej. P3-3 (S5 `|| true` w
  world_r2_browser.mjs) POZA zakresem zlecenia korekty — udokumentowane,
  nietknięte (dead guard, bez fałszywych twierdzeń; patrz CORRECTIONS.md).

Testy po korekcie: **140/140 PASS / 0 FAIL / 0 NOT_PERFORMED** (world 53
[+1 R2_VEG_WRAPPER_LATEST_WINS], unit 24, app 22, catalog 41 — pełne
kontenery, konfiguracja wykonawcza). Browser re-verify (narzędzie
`world_r2_correction_browser.mjs`, izolowany headless Edge + CDP):
REVERIFY_PASS 12/12 — nowszy config ZAPISANY while-busy (vegPending
obserwowane na żywo), przełączenie regionu while-busy też ZAPISANE,
censusy przestarzałe niecommitowane, WYGRAŁO żądanie teleportu
(okno 196,196, ostatni konfig global:2), spójność GOTOWA, 0 page errors
(raw/CORRECTION/BROWSER_REVERIFY_VEG_COHERENCE.json + prywatny PNG).
Pełny zapis: CORRECTIONS.md + CORRECTION_COUNTERCHECKS.json +
raw/CORRECTION/*. Serwer restartowany na kodzie korekty (PID w
RUN_AND_STOP.md).

Serwer pozostaje URUCHOMIONY na 8163 serwując dokładnie opublikowany kod
(start/stop + served↔published identity: RUN_AND_STOP.md).
