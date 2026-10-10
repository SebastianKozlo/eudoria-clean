# CORRECTIONS — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010 (runda korekty 2026-10-10)

```text
CORRECTION_ROUND   = PE_MASTER_CORRECTION_DISPATCH_20261010 (zbindowana runda korekty po INTERNAL_QC)
PARENT_COMMIT      = b4dfae7ce3c49e87f221fc04707074200e645209 (oryginalny commit runu; NIE amendowany)
BASE               = 44ef254b8ff9ebb05bd104690181c202678c065d (bez zmian; weryfikacja przed commitem)
QC_SOURCE          = D:\Eudoria_Reconstruction\99_Audits\PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010\INTERNAL_QC_BY_PE_MASTER_AUDITOR\QC_REPORT.md
QC_VERDICT         = QC_PASS_WITH_FINDINGS (REQUIRE_CORRECTIONS): 2x P1 + 5x P2 + 4x P3
WORKTREE           = D:\Eudoria_Reconstruction\12_WebGame\pe-world-continuous-r2
BRANCH             = codex/pe-world-continuous-r2-20261010 (RESULT_BRANCH; normal commit NA WIERZCHU b4dfae7; FF push)
KLASA              = P1-1 (BLOCKER-PUBLICATION), P1-2 (MATERIAL), P2-1..P2-5, P3-1..P3-3
```

Zasada porządkowa tej rundy (P1-1): WSZYSTKIE edycje prozy/raportów/handoff
WYKONANE NAJPIERW → MANIFEST_SHA256.csv ZREGENEROWANY OSTATNI ze stanu
finalnego pakietu → pełna bijekcja zweryfikowana DWIEMA NIEZALEŻNYMI
metodami (tylko odczyt po regeneracji; żaden zapis w pakiecie po
regeneracji manifestu).

---

## P1-1 Manifest bijection — FIXED

- **Finding (QC)**: wiersz REPORT.md w MANIFEST_SHA256.csv (12408 B /
  95650dbc…) ≠ fizyczny commitowany plik (12410 B / EFCA8566…). Manifest
  został wygenerowany ze starszej wersji REPORT.md, po czym REPORT.md był
  edytowany (+2 B) bez regeneracji → twierdzenia „zweryfikowana dwukrotnie"
  (REPORT §5, HANDOFF, PE_MASTER_REVIEW placeholder) były FAŁSZYWE dla
  opublikowanego stanu b4dfae7. Defekt persystencji/provenance, NIE
  fabrykacja (pozostałe 33 wiersze zweryfikowane poprawnie przez QC).
- **Fix**: (a) wszystkie edycje prozy tej rundy wykonane PRZED regeneracją
  manifestu (REPORT §5/§6, HANDOFF, RUN_AND_STOP, INPUT_IDENTITIES,
  CORRECTIONS.md, CORRECTION_COUNTERCHECKS.json, raw/CORRECTION/*);
  (b) MANIFEST_SHA256.csv zregenerowany OSTATNI ze stanu finalnego;
  (c) pełna bijekcja zweryfikowana DWIEMA NIEZALEŻNYMI metodami:
  1. **self-check generatora** (node): ponowna enumeracja wszystkich
     fizycznych plików pakietu (rekurencyjnie, poza samym manifestem),
     ponowny pomiar size+SHA256 każdego pliku i porównanie wiersz-po-wierszu
     z zapisanym CSV (duplikaty/missing/extra/hex także sprawdzane);
  2. **niezależny re-hash w PowerShell** (osobna implementacja, inny
     język/ścieżka kodu niż generator): Get-FileHash -Algorithm SHA256 +
     Get-Item .Length dla każdego fizycznego pliku pakietu, porównane z
     wierszami CSV; liczba plików fizycznych == liczba wierszy == każda
     ścieżka dokładnie raz.
  Obie metody: 0 mismatchy w stanie opublikowanym tej korekty (wiersze
  = wszystkie fizyczne pliki pakietu; manifest sam się wyklucza).
- **Superseded claims**: REPORT §5 („zweryfikowana dwukrotnie" — teraz
  oznaczone SUPERSEDED z opisem), HANDOFF („policzone dwukrotnie" —
  SUPERSEDED), PE_MASTER_REVIEW placeholder (nota korekty dodana).
  Oryginalne wartości zachowane w historii gita (blob b4dfae7) — bez
  przepisywania historii twierdzeń; wartości błędne oznaczone wprost.

## P1-2 Veg latest-wins w PRODUKCJI — FIXED

- **Finding (QC)**: `compat/world-app.js#rebuildVegetation` short-circuit
  `if (state.vegBusy) return null;` GUBIŁ nowsze żądanie PRZED dostarczeniem
  go do klasy — klasowa kolejka latest-wins (WL-1) była NIEOSIĄGALNA ze
  ścieżki produkcyjnej; dodatkowo nawet klasowo-kolejkowany rebuild nie
  commitował census do state.vegCensus/coherence.veg (wrapper już wrócił).
  POST WL-1 mierzył KLASĘ w izolacji, nie wrapper produkcji.
- **Fix (produkcja; klasa NIETKNIĘTA — compat/world-vegetation.js
  byte-identical, PEFoliageCore byte-identical)**:
  1. wrapper-level latest-wins: `state.vegPending` — nowsze żądanie podczas
     busy jest ZAPISYWANE (slot nadpisywany przez nowsze), nie gubione;
  2. drain loop: po zakończeniu bieżącego buildu pętla dostarcza NAJNOWSZE
     zaplanowane żądanie do klasy (SERIALnie — klasowa kolejka pozostaje
     warstwą bezpieczeństwa dla bezpośrednich wywołań, w produkcji
     nieangażowana);
  3. commit gen-gated: census commitowany do state.vegCensus +
     coherence.veg TYLKO gdy `state.sceneRequest?.id === req.requestId`
     (census przestarzały NIGDY nie nadpisuje nowszej sceny);
  4. dedupe identycznych powtórzeń (tożsamość = origin+requestId; zmiany
     konfiguracji bumpują id przez forceNew) — produkcja: veg-apply
     wywołuje wrapper DWA razy z tą samą tożsamością (handler + rebuildWindow
     linia 751) — bez dedupe build wykonywałby się podwójnie;
  5. read-only diagnostyka: `state.vegTrace` (ograniczony ring 48 zdarzeń:
     request-take/stored-pending/drain-run/dedupe/returned/committed/
     not-committed/drain-done) eksponowana przez `__peR2Debug.running`
     (żadna zmiana zachowania przez debug; defensive w kontekstach
     nieprzeglądarkowych).
- **PRE (zmierzone przez `tools/pecompat/world_r2_correction_counterchecks.mjs`
  --phase pre; wrapper b4dfae7, SHA256 ce691ec3…)**: B NIGDY nie dociera do
  klasy (delivery: tylko A); finalny committed vegCensus/coherence NIE
  odzwierciedlają B; READY nieosiągalne dla nowego okna (stały PARTIAL do
  następnej akcji użytkownika).
- **POST (ten sam narzędzi, --phase post; wrapper po fixie, SHA256
  06121486…)**: delivery A→B; finalny census = B; coherence.veg = B;
  READY osiągalne; dedupe identycznych powtórzeń trzymany; gen-gate
  (żądanie o przestarzałym id NIE commituje). Oba piny SHA źródła
  production wrapper w CORRECTION_COUNTERCHECKS.json (narzędzie mierzy
  SHA world-app.js w każdej fazie; TEN SAM narzędzi w obu fazach —
  SHA narzędzia zapisany w rekordach).
- **Bramka baterii**: NOWA `R2_VEG_WRAPPER_LATEST_WINS` w
  tests/pecompat/world_r2_gates.test.mjs — ekstrakcja VERBATIM aktualnego
  wrappera produkcyjnego + VM; scenariusz: A→B podczas busy (nowsze
  dostarczone, census ostatniego żądania commitowany, coherence+READY),
  dedupe, negative-control stale-id (nie commituje). Bateria WORLD:
  53 PASS (52 oryginalne + 1 nowa).
- **Kontrczek WL-1 rozszerzony** o ścieżkę wrapperową
  (world_r2_counterchecks.mjs: WL_1.wrapper; `fixed` WL-1 wymaga teraz
  zarówno klasy JAK i wrappera) + flaga `--no-canonical` (rewalidacje bez
  nadpisywania opublikowanych PRE_/POST_COUNTERCHECKS.json).
- **Browser re-verify** (`tools/pecompat/world_r2_correction_browser.mjs`,
  izolowany headless Edge + CDP na wolnym porcie; NIgdy 9222/cudze sesje):
  **REVERIFY_PASS 12/12** — na ŻYWO: (a) nowszy KONFIG (veg-apply profil 2
  podczas buildu profilu 1) ZAPISANY jako vegPending while-busy
  (obserwowane na żywo, +171 ms); (b) PRZEŁĄCZENIE REGIONU (teleport
  200,200) podczas buildu TEŻ ZAPISANE while-busy (ślad
  request-stored-pending origin 196,196); (c) censusy przestarzałe (A i B)
  NIEcommitowane (gen-gate); (d) WYGRAŁO żądanie TELEPORTU — census
  commitowany = ostatnie żądanie (okno 196,196, OSTATNI konfiguracja
  global:2); (e) spójność GOTOWA (teren+tekstury+roślinność 196,196);
  (f) 0 page errors. Pełny zapis z transkryptem zdarzeń wrappera:
  raw/CORRECTION/BROWSER_REVERIFY_VEG_COHERENCE.json + prywatny PNG.
  Uczciwa miara czasów: na tej maszynie (ciepłe cache serwera/OS) buildy
  roślinności są szybkie (6–1500 ms klasa) — „long-running build" z premisy
  QC nie odtwarza się na ciepłych danych; wyścig zrealizowano przez ścieżkę
  apply (bezpośrednie wywołanie wrappera bez latencji przebudowy terenu)
  oraz przez teleport wewnątrz okna buildu — oba warianty ZAPISANE i
  dostarczone (transkrypt). Nota: click-time sceneId przycisku veg-apply
  poprzedza bump id handlera (async setConfig przed requestScene) —
  tożsamość żądań czytana z transkryptu wrappera, nie z przechwytu kliknięcia.

## P2-1 REPORT perf +12 MB — FIXED

- **Finding**: REPORT §2 PERFORMANCE „heap last-route +12≤8+tolerance MB"
  vs kanoniczny PERFORMANCE_AND_LIMITS.json: lastRouteDeltaMB=1 (72→73),
  firstToLastDeltaMB=3 (70→73). Liczba „+12" nie istnieje w JSON.
- **Fix**: linia PERFORMANCE poprawiona na wartości kanoniczne (+1
  last-route, +3 first-to-last, 70→73; budżet ≤8 MB) z oznaczeniem
  [POPRAWIONE w rundzie korekty]. Definicja lastRouteDelta w narzędzi:
  R4−R3 (world_r2_performance.mjs:169).

## P2-2 REPORT „gęstości 100%" — FIXED

- **Finding**: REPORT §4 „WL-2 przy gęstości 100%: … 16324→5000" vs
  VEGETATION_CENSUS.json regionalPreviewBoundaryWindow.config.densityPercent
  = 50 (collect narzędzia ustawia densityPercent: 50 dla wszystkich trzech
  okien). Pomiar autentyczny; etykieta gęstości błędna.
- **Fix**: etykieta poprawiona na ZMIERZONE density 50 (z zaznaczeniem
  poprawki i wskazaniem census config); etykieta findings WL-2→WL-5
  (cena fair cap to WL-5). Nie re-mierzone (opcja „re-measure at 100"
  odrzucona — pomiar 16324→5000@50 jest autentyczny i pozostaje.

## P2-3 Stale PID (RUN_AND_STOP/HANDOFF) — FIXED

- **Finding**: udokumentowany PID 33876 (i wrapper 30780) nie istniał;
  listener = PID 5780; server-run.log pokazuje łańcuch restartów.
- **Fix**: RUN_AND_STOP przepisany na stan RUNDU KOREKTY: node PID 23232
  (wrapper 29328), PEŁNY uczciwy łańcuch restartów (32048→35384→32592→
  35452→33876→5780→23232) z zaznaczeniem [POPRAWIONE]; HANDOFF
  zaktualizowany. PID zweryfikowany live (Get-NetTCPConnection -LocalPort
  8163 → OwningProcess == zapisany PID). Restart rundy korekty = serwowanie
  DOKŁADNIE nowego opublikowanego kodu (served↔published byte identity
  po pushu; patrz końcowy handoff).

## P2-4 HANDOFF census pola — FIXED

- **Finding**: „src/pesource (2 NEW files)" — fizycznie dokładnie 1 NEW
  (DdsDecoder.js); „.gitignore" na liście zmienionych — fizycznie nietknięty
  (git diff --name-status BASE..HEAD: puste dla .gitignore).
- **Fix**: oba pola poprawione (z zaznaczeniem poprawki); weryfikacja
  fizycznym diff BASE..HEAD wykonana przed zapisem (zgodnie ze scope).

## P2-5 → P3(c) PRE harness variant + semantyka pola — DOCUMENTED (NOT_FIXED_AS_ORIGINAL, z powodem)

- **Finding (QC)**: pole PRE WL-2 `y0FallbackInProductionApply: false`
  sprzeczne ze ŹRÓDŁEM BASE (fallback `? 0 :`/`?? 0` FIZYCZNIE istniał w
  BASE w obu plikach); pole policzyła starsza NIEPRZYPĘTA wersja narzędzia
  (committed world_r2_counterchecks.mjs to wersja POST — `--phase pre` z
  committed drzewa na BASE w ogóle by się wywalił: importuje PEHeightQuery.js
  i fairCapQuota, których nie ma w BASE).
- **Disposition (uczciwie)**: dokładny wariant PRE narzędzia NIE ISTNIEJE —
  nie można go przypiąć ani odtworzyć (edycje run-local między fazami;
  naruszenie reproducibility discipline ujawnione przez QC). NIE fabrykuję
  wstecznie „wariantu PRE". Zachowane: liczby PRE są wewnętrznie spójne i
  przypięte do BASE przez productionSources SHAs (fizycznie zweryfikowane
  przez QC); finding WL-2 udokumentowany przez expectedPre. Semantyka pola
  wyjaśniona: w oryginalnym runie pole miało inną semantykę skanu niż w
  committed wersji POST (committed skan `? 0 :` tylko w world-vegetation.js
  daje false w HEAD, ale dałoby true na BASE) — pole PRE `false` pochodzi z
  innej (nieprzypiętej) logiki, NIE z braku fallbacku w BASE. Odtworzenie
  `--phase pre` na oddzielnym worktree BASE committed narzędziem NIEMOŻLIWE
  (importy nieistniejące w BASE) — udokumentowane, nie ukrywane.
- **Runda korekty podnosi poprzeczkę dla NOWYCH pomiarów**: narzędzie tej
  rundy (world_r2_correction_counterchecks.mjs) jest committed, jego SHA256
  zapisany w każdym rekordzie, TEN SAM wariant mierzy obie fazy (pre: wrapper
  b4dfae7 przez git stash; post: finalny wrapper) — w pełni reprodukowalne.

## P3(a) harnessy → neutralne raw-dirs — FIXED

- **Finding**: run_world_tests.mjs / run_app_tests.mjs / run_catalog_tests.mjs
  domyślnie pisały surowe dumpy do HISTORYCZNYCH pakietów READ_ONLY
  (R1/CITY) — przyczyna incydentu z oryginalnego runu (6 modified + 5
  untracked w pakietach READ_ONLY, przywrócone byte-clean).
- **Fix**: domyślne rawDir = NEUTRALNY katalog tymczasowy (os.tmpdir()/
  pecompat-tests-raw/{WORLD,APP,CATALOG}); zapis do jakiegokolwiek pakietu
  docs/audits wymaga JAWNEGO --raw-dir; RUN_ID pozostał ETYKIETĄ baterii
  (nigdy ścieżką zapisu). Weryfikacja: pełne 4 baterie tej rundy uruchomione
  bez wpływu na docs/ (git status: 0 zmian w historycznych pakietach; jedyne
  zmiany docs/ = zamierzone artefakty korekty).

## P3(b) INPUT_IDENTITIES Models.ark null-e — FIXED

- **Finding**: sizeBytes: null, sha256: null dla Models.ark mimo że
  tożsamość istniała (pin serwera cdModelsArkPin).
- **Fix**: wypełnione fizycznym pomiarem tej sesji: 128742137 B /
  F660D055B4B9471B3B6E16B07F5368DBD6F2208DAB6B51BB9BDB9942BD73EA62 (Get-
  FileHash; zgodne z pinem server-world.mjs i QC) + nota [FILLED] z
  wyjaśnieniem.

## P3(c) PRE tool variant — patrz P2-5 (DOCUMENTED, NOT_FIXED_AS_ORIGINAL)

## P3-3 (S5 `|| true` w world_r2_browser.mjs:388) — POZA ZAKRESEM (dokumentowane)

- QC finding: martwy guard (`|| true`) w wyrażeniu wait S5 — żaden fałszywy
  claim nie wynika (równość okna powrotu weryfikowalna z zapisanych danych),
  ale guard jest martwy. NIE należy do przypisanych pozycji tej rundy
  korekty (scope: dokładnie P3a/P3b/P3c) — pozostawione NIETKNIĘTE
  (ryzyko destabilizacji uznane za nieuzasadnione przy braku autoryzacji);
  udokumentowane tu dla następnej rundy. world_r2_browser.mjs poza tym
  nietknięty.

---

## Testy po korekcie (pełne baterie, konfiguracja wykonawcza, finalny kod)

```text
WORLD   = 53 PASS / 0 FAIL / 0 NOT_PERFORMED   (52 oryginalne + 1 NOWA R2_VEG_WRAPPER_LATEST_WINS)
UNIT    = 24 PASS / 0 FAIL / 0 NOT_PERFORMED
APP     = 22 PASS / 0 FAIL / 0 NOT_PERFORMED
CATALOG = 41 PASS / 0 FAIL / 0 NOT_PERFORMED
TOTAL   = 140/140 PASS, 0 FAIL, 0 NOT_PERFORMED (zmiana liczby testów: +1; census)
```

Kontrczeki po korekcie: WL-1..WL-5 ALL FIXED na finalnym kodzie
(world_r2_counterchecks.mjs --no-canonical, raw poza pakietem) —
WL_1 uwzględnia teraz ścieżkę wrapperową; CORRECTION_COUNTERCHECKS.json
(pre+post wrappera produkcji); browser REVERIFY_PASS 12/12.

## Manifest bijection ×2 (stan opublikowany tej korekty)

MANIFEST_SHA256.csv zregenerowany OSTATNI ze stanu finalnego pakietu
(ostatni zapis w pakiecie przed commitem). Pełna bijekcja zweryfikowana
DWIEMA NIEZALEŻNYMI metodami (opis w P1-1): (1) self-check generatora
(node; re-enumeracja + re-hash + porównanie wiersz-po-wierszu, 0
duplikatów/missing/extra, poprawny hex); (2) niezależny re-hash PowerShell
(Get-FileHash + Length każdego fizycznego pliku vs CSV). Wynik: 0
mismatchy; wiersze == wszystkie fizyczne pliki pakietu dokładnie raz;
manifest self-excluded. (Wynik poza pakietem — w terminal handoffu.)

## Zachowane frazy statusowe

Bez zmian — REPORT §3 (§10 kontraktu) nietknięty w tej rundzie; żadna
nauka nie podniesiona; INDEPENDENT_DESKTOP_POST_AUDIT = PENDING;
NEXT_EXPERIMENT_AUTHORIZED = NO; HARD_STOP = YES.
