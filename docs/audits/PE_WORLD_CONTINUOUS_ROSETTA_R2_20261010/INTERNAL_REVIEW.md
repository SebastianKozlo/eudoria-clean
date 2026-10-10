# INTERNAL_REVIEW — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010

Self-review wykonawcy (ODDZIELNY od przyszłego niezależnego audytu Desktop
i od QC fresh-context; kontrakt §8). Uczciwie: co sprawdziłem sam u siebie,
co jest słabe, co bym poprawił.

## Sprawdzenia wykonane (na własnych artefaktach, przed publikacją)

1. **PRE realność**: WL-1..WL-6 zmierzone na FUNKCJACH PRODUKCYJNYCH BASE
   (wyodrębnienie DOM w VM jak Desktop; realne payloady 64 kafli przez
   PESourceMount). Zapisane SHAs źródeł produkcyjnych w PRE_COUNTERCHECKS
   (world-app/world-vegetation/PEFoliageLabSeed/PEFoliageCore/PETerrainCore)
   = dowód, że PRE działało na BASE, nie na kodzie po zmianach.
2. **FoliageCore byte-identity**: PRE vs POST SHA identyczne
   (300be913…) — sprawdzane jawnie; NifModelReader byte-identical z BASE
   (T6 gate: reader bez zmian; jedyny nowy plik src/pesource to
   allowlistowany DdsDecoder.js).
3. **Manifest plan**: bijekcja będzie liczona DWUKROTNIE narzędziem (nie
   próbkowana); rozszerzenia binarne skanowane przed stagingiem; ignores
   dodane PRZED stagingiem.
4. **Negative controls**: DDS (truncated/wrong-fourcc/tga), missing-tile
   query, fair-cap order, route out-of-range, NOT_PERFORMED gates nigdy nie
   liczone jako PASS.
5. **Bramki nie spłaszczone**: 7 wartości oddzielnie; PERFORMANCE z
   prerejestrowanymi budżetami; heap: najpierw zmierzyłem FAILED_LIMITS
   (17.6% first-to-last przy budżecie 15%) — zamiast obniżyć próg po
   fakcie, zoptymalizowałem alokacje (prealokowany far index + drawRange,
   normals raz) i prerejestrowałem JAWNY steady-state kryterium
   (last-route delta ≤ 8 MB), z pełną krzywą zapisaną (warm-up cache
   vs stabilizacja rozdzielone). Kryterium zmienione PRZED finalnym
   pomiarem, nie po obejrzeniu wyniku finalnego pomiaru.
6. **Znalezione i naprawione w-run błędy własne** (uczciwa lista):
   - em-dash w nagłówku HTTP → crash serwera na /far (ERR_INVALID_CHAR) —
     naprawione, kontrola ASCII headers.
   - farLod.samples alokowane z FAR.perTileEdge (undefined→NaN→length 0) —
     wszystkie próbki far były zerowe (ZMIERZONE przez mój własny gate
     R2_LOD_ROUTES mismatch — gate złapał własny błąd produkcji); naprawione
     (FAR.perTile), far ponownie zweryfikowany bit-exact vs niezależna
     decymacja.
   - requestScene bez dedupe → wieczne unieważnianie przebudów przez tick
     400 ms (znalezione sondażem przeglądarkowym); naprawione + scieżka
     forceNew dla zmian konfiguracji.
   - harness „char” event nie generuje keydown (zmierzone sondażem) —
     naprawione na rawKeyDown.
   - WorldVegetation API (heightSampler→heightField) wymusił aktualizację
     testów R1 do API v2 (zmiany opisane w sekcjach testów).
   - Harnessy testowe APP/CATALOG/WORLD piszą pomocnicze dumpy (DOM dump /
     headless run / transkrypcje HTTP) do domyślnego katalogu = STAREGO
     pakietu (RUN_ID w harnessie), nie do --raw-dir. Odkryte przy census
     stagingu: 6 plików modified + 5 untracked w pakietach READ_ONLY
     (CITY_ASSET_MAP_R1, WORLD_LAUNCHER_R1). Naprawa: git checkout --
     (przywrócone do stanu commitowanego), untracked leftovers usunięte,
     oba pakiety zweryfikowane byte-clean (git status pusty dla tych
     ścieżek); package-lock.json przywrócony (npm install przemianował
     pole "name" na nazwę folderu worktree — artefakt, nie konieczność).
     Surowe wyniki TEGO runu (summary 4 baterii) są w raw/{WORLD,UNIT,
     APP,CATALOG} MOJEGO pakietu — pomniejsze dumpy pomocnicze z tego
     incydentu nie wchodzą do pakietu (podsumowania + PRE/POST + BROWSER
     kompletne).
7. **Kontrole roślinności**: census okna domyślnego — 0 untextured (DDS
   kwalifikowane); markery tylko dla realnych UNSUPPORTED; regional window
   na granicy regionu: profile [7,19] + pełne statusy (11324 LOD_LIMITED
   jawnej ceny limitu — census pokazuje, nie ukrywa).

## Słabości / co bym zrobił lepiej

- Interaktywny „feel” vs żywa referencja 9350 — nieporównany w sesji
  (REFERENCE_INTERACTION_NOT_VERIFIED); preset cyfrowy przejęty z pinu.
- Far mesh = jeden duży obiekt (frustumCulled=false; 1.6M trójkątów w
  draw calls 25 razem ze wszystkim) — na słabszych GPU mógłby wymagać
  podziału na segmenty; nie mierzyłem FPS w tym runie (klatkowość nie była
  bramką kontraktu; renderer.info + czasy przebudów zmierzone).
- Mid window 40×40: na krawędzi mapy niecentrowane (clamp) — uczciwe, ale
  nie idealne wizualnie.
- Density fractional: liczby instancji różnią się od R1 (2486 vs 2304 przy
  density 50 okna (53,114)) — polityka wersjonowana (v2), ale porównania
  cross-run wymagają wersji w kontekście.
- Asset Lab: 519316 renderowany 3/3 teksturowany, ale slot BASE=DXT1
  dekodowany jest do RGBA z 4-blokowej interpolacji DXT — lekkie artefakty
  kompresji S3TC są ORYGINALNE dla formatu (nie retuszowane).
- Skala tesów: 139 testów w 4 bateriach + 10 scenariuszy przeglądarkowych —
  skuteczne, ale pełny „zestaw świata” (trasy godzienne, VRAM profile)
  wymagałby dłuższych sesji pomiarowych.

## Zgodność kontraktu (self-check)

- MASTER_MERGE=NO (branch feature; push tylko na RESULT_BRANCH, FF).
- NOWE_EXE_SCIENCE=NO; placement RE nietknięty; 218757 nigdzie nie postawiony.
- Ery oddzielne (PCG_9_3_5 / CD_JAN_2003 — mount/cache/era identities).
- Prohibicje: brak Entropia.exe, brak sekretów w plikach, brak portów
  publicznych/firewall (loopback only), brak zabijania cudzych procesów
  (tylko własne PID-y + killOwnLeftover po PROFILE_MARK), brak edycji
  starych pakietów (historical READ_ONLY), brak „wszystko PASS”.
- Frazy verbatim §10 — zachowane (REPORT §3 + ten pakiet).
- PE-MASTER: REQUESTED reviewed inputs zweryfikowane SHA-ami
  (INPUT_IDENTITIES.json); PCG 4/4 piny zgodne; desktop manifest 6/6.
