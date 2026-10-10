# STREAMING_AND_HEIGHT_QC — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010

Kontrakt §3–§4. Wszystkie pomiary na funkcjach produkcyjnych; PRE zachowane
w PRE_COUNTERCHECKS.json, POST w POST_COUNTERCHECKS.json; pełne surowe
wartości w raw/POST/.

## 1. Jedno wspólne zapytanie wysokości (§3.2)

**Implementacja**: `src/peworld/PEHeightQuery.js` (PEHeightField).
Odtwarza DOKŁADNIE płaszczyzny renderowanych trójkątów warstwy bliskiej:
ten sam podział quada co `PETerrainRegion.buildGeometry` ((a,c,b),(b,c,d);
anty-diagonala fx+fz=1). Surowe u16 zachowane; `worldHeightMeters` (u16/128,
CURRENT_RUNTIME_CALIBRATION) zastosowane DOKŁADNIE RAZ; zero wygładzania.

**Pomiar POST (okno (53,114)+halo, profil 0, seed 0, density 50)**:
- instancje 2486 (wrapper v2: recIndex w hashu + gęstość frakcyjna — liczba
  różni się od R1 2304 zgodnie z wersjonowaną zmianą polityki);
- max |sharedQuery − niezależne barycentryczne przeliczenie z SUROWYCH
  payloadów| = **0** (300 losowych + 6 brzegowych/diagonalnych sond;
  R2_HEIGHT_TRIANGLE_EXACT PASS);
- pozycji bez realnej powierzchni: **0** (halo pokrywa 0..512 generatora);
- fallback y=0 w produkcji: **BRAK** (AST check + R2_HEIGHT_HALO_BOUNDARY);
- kafel NODATA → quad null (4/4 sondy w dziurze null; sąsiad działa;
  R2_HEIGHT_MISSING_TILE_NULL PASS — kontrola negatywna).

**Granica 256/0..510 vs 0..512**: rozwiązana halo 1 kafla RZECZYWISTYCH
sąsiednich próbek (pole 10×10 dla okna 8×8; sampling do 638 m rel). Fallback
y=0 usunięty; instancje bez powierzchni mają status DEFERRED_NO_SURFACE i nie
są renderowane.

**Ruch (WL-3)**: kandydat obliczany PIERWSZY; commit tylko po sprawdzeniu
powierzchni. Pomiar: produkcja `updateFlyWalk` W dt=1 null-ground → pozycja
(100,10,100) BEZ ZMIANY + banner (POST; PRE: (100,10,88)). Banner rozróżnia
LOADING od CORPUS_EDGE. Blur/utrata locka/zmiana trymu czyszczą klawisze.
Pointer lock rejection → komunikat + działający drag-look (S4 użyło
prawdziwych mouse events; ruch działa: 15 m XZ, Y=50.0+1.7 na WSPÓLNEJ
powierzchni — S4 yOnSharedSurface=true).

## 2. Latest-request / własność zasobów (§3.1)

- Tożsamość żądania: `{id, origin, era, containers, profileMode, profile,
  labSeed, density, calibration, versions}` — bump przy ZMIANIE celu lub
  forceNew (zmiana konfiguracji); dedupe przy powtórzeniu tego samego originu
  (bez dedupe ~400ms tick unieważnia w locie przebudowę — zmierzone).
- Przestarzały wynik: abort PRZED apply + dispose (tekstury: materiał/
  arrayTexture/idx/wTex zbudowane-a-niezaaplikowane zwalniane; census nie
  ustawiany dla stale).
- Najnowsze żądanie: kolejka latest-wins (teren pendingOrigin; wegetacja
  pendingRequest w klasie). POST WL-1: żądanie B podczas busy → finalny
  origin B=(1,0) (PRE: A).
- Spójność: `scene #id: żądane okno | teren | tekstury | roślinność` +
  status GOTOWA tylko gdy wszystkie komponenty tego samego żądania (S1);
  przy przebudowie poprzednia spójna scena pozostaje widoczna (PARTIAL).
- Błąd komponentu: nazwany reason + census (banner + panel; żaden trwały
  busy; timeouty 20 s na indeksy tekstur/modeli).

## 3. Ciągły świat (§4)

- **near**: okno 8×8 RAW (PETerrainRegion) — jak R1, plus halo.
- **mid**: ring 40×40 kafli poza near (hole cięty dokładnie po ostatnich
  próbkach near — te same oryginalne próbki na linii cięcia: bez szwu);
  8×8-decymowane RZECZYWISTE próbki/kafel; bloki 8×8 kafli (8 256 B) z
  /api/world/lod8/<bx>/<by>; LRU 96 bloków klient / 128 serwer.
- **far**: cały świat 4×4-decymowane (1 713 368 B binary: header u16×4 +
  51 920 status + 830 720 u16 próbek); zbierane przez census (503 + progress
  aż READY — zero placeholdera); mesh ~831K wierzchołków, indeks
  prealokowany + drawRange (hole za mid), normals RAZ.
- **Orientacja/przyrost**: linie cięcia near|mid i mid|far to TE SAME
  próbki oryginalne (mid line 135/k=7 = near sample 255; far line =
  mid edge) → brak szczelin i nakładania z definicji; skirt niepotrzebny
  (żaden nie użyty).
- **Brak danych**: status per kafel w payloadach mid/far; quad dotykający
  kafla spoza MEASURED → dziura jawna (nigdy zero-powierzchnia; w tym
  korpusie 0 missing + 0 failed kafli — denominator 51 920 z indeksu).
- **Kalibracja RAZ na obu poziomach** (worldHeightMeters; pozycje = własne
  pozycje próbek — decymacja bez uśredniania).
- **Streaming za fokusem** (§5/WL-4): orbit→controls.target, fly/walk→
  camera; okno centrowane; teleport zapewnia dane celu przed osadzeniem
  kamery (brak ground ≠ y=0).
- **Budżety/scenariusz**: perf (run 4 teleporty): przebudowy ~0.9–1.4 s;
  kafle cache 288≤512; tekstury 23≤64; modele 9≤16; heap krzywa
  47→68→69→79→80 MB (ostatnia trasa +1 MB — steady state; pełne dane
  PERFORMANCE_AND_LIMITS.json). Powrót A odtwarza te same liczby
  (requested 2485/placed 2485 przy powrocie — sameConfigSameCounts w S5)
  i te same wysokości źródłowe (ten sam payload hash — WL-2 tile hashes
  PRE==POST).

## 4. Pokrycie (§4 rozdział jawny)

Pełne liczby: WORLD_COVERAGE_AND_LOD.json. Skrót:
indexed regular 51 920 (z indeksu) + 6 530 special + 1 sentinel;
valid raw samples: 51 920/51 920 measured (0 missing, 0 failed);
coarse-LOD represented: far 51 920 (gated), mid 25 bloków okna;
near-resident: 64 kafle okna (+36 halo dla wysokości);
pending: census 0 przy zbiorze (far gotowy); actual missing: 0.
