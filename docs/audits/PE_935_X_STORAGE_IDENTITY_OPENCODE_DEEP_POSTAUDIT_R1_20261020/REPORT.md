# Niezależny postaudyt X STORAGE IDENTITY / OPENCODE R1

**Werdykt: PARTIAL_PASS_WITH_MATERIAL_CORRECTIONS.** Run przyniósł rzeczywisty postęp: późniejszy wynik CALL z argumentem68 zasila D410, a argument kopiowany w C3B0 prowadzi do bufora stosu callera. Nie przyjmuję jednak bezwarunkowego awansu preservation i X_store=X_entry. Publikacja ma poprawną historię Git i przeszła skan treści nowego diff, lecz brakuje wymaganego manifestu publikacyjnego.

Audyt fizyczny w WinDev2407Eval. Wyłącznie saved text,20 już dopuszczonych ekstraktów, selektywne read-only metadane OpenCode DB i obiekty Git. Zero kontaktu z oryginalnym EXE/runtime gry, zero nowych naukowych okien, zero inferencji, zmian konfiguracji i commit/push. Frozen root niezmieniony. Daty nazw pakietów odnoszą się do dnia użytkownika2026-10-20; zapisy runtime UTC2026-10-21 mieszczą się w tym wieczorze America/Los_Angeles.

## 1. Integralność i rzeczywiste liczniki

| Kontrola | Wynik niezależny |
|---|---|
| Run | 122 wiersze+manifest=123 pliki, bijekcja/hash PASS, zero missing/extra/duplicate |
| Manifest runu | `041E60ACF9BB2E5CE9318199236318335E4208790046241DF97360705EE59238`,12016B |
| Authoring |119+1=120 plików, PASS; SHA `03CF081A2AEDA038EA2762DF6885E1FBCEFCBA9D8F1FC2C42ACB6D6950ABD8C1`|
| INPUT_CATALOG |2018/2018 pełnych pinów PASS |
| Ekstrakty |20/20 odtworzone z przypiętego H5, zgodne selected SHA i bajty materialu |
| Zdarzenia |24: START,20ADMIT,2NAV,STOP; hash-chain PASS; zero zapisanych INCIDENT/DENY |
| Debit |42 body reservations,953rows,59CALL,20candidates; w cap64/10000/400/64 |
| Union |**949rows**,59CALL; cztery wiersze powtórzone w J014/J019 |

REPORT.md i SELF_REVIEW_2 błędnie podają40body; REPORT błędnie podaje union953. BODY_OWNER_LEDGER ma właściwe42/949 i wyjaśnia cztery współdzielone wiersze. Jest to błąd raportowania, nie przekroczenie limitu. Liczba42 oznacza konserwatywne rezerwacje ekspozycji, nie42 odrębne potwierdzone funkcje. Brak późniejszych mtime wspiera LAST, lecz sam czas pliku nie dowodzi pełnej historii zapisów.

## 2. Co zachowujemy

**XSI-01/04/05:** bezpośredni lokalny przepływ EAX z CALL0095D3C4 na85821E, z argumentem68, do ECX przed D410 na858240 jest potwierdzony. Cache w stosie też istnieje, ale receiver bierze bezpośrednio EAX, nie z późniejszego reload cache. Wcześniejszy wynik CALL na857FE3 miał argument80. Są to różne producent-sites i różne definicje wartości. **Nie dowodzą nierówności bitów adresów**; aliasing i świeżość pozostają UNKNOWN bez kwalifikacji callee. Nagłówkowe X_init_in≠A należy zastąpić rozdzieleniem provenance, nie znakiem nierówności wskaźników.

**XSI-06/16:** po normalnym powrocie D410 EAX przechodzi do ESI i ECX przed C3B0. Druga ścieżka zeruje ESI i dochodzi do tego samego bezpośredniego CALL. To obserwacja statyczna ścieżki, nie dowód udanego wykonania C3B0 z this=0. Należy oddzielić istnienie CALL od osiągnięcia normalnego return po możliwym dereference/null fault.

**XSI-07/10/12:** zachowujemy lokalny copy-count13DWORD i sloty źródła/docelowego oraz opaque virtual-return do+2C. Późniejsze sloty+4C/+50 i indeksowane elementy są wartościowym lokalnym ustaleniem. Nie ustanawiają roli world-instance ani tożsamości z R.

**XSI-13:** caller na85A429 przekazuje wskaźnik uzyskany przez LEA do własnej ramki. Niezależny pełny literal CALL census H5 potwierdza **jedno takie bezpośrednie wystąpienie** dla F858. Nie jest to dowód jedynego możliwego callera przez indirect/tailcall ani runtime.

## 3. Preservation — materialna korekta XSI-08/09

Poszerzono pokrycie zapisanego listingu do całego liniowego zakresu C3B0..CD10. To jest wartościowe i znacznie lepsze od dwóch odległych okien poprzednika. Wykazano bezpośredni zapis komórki z entryECX, odczyty oraz lokalną arytmetykę SUB8/ADD8. Nie zamknięto jednak effects callee i wszystkich zapisów pośrednich.

FRAME_PRESERVATION stwierdza, że opaque callees nie mogą adresować komórki bez przekazanego jej wskaźnika, bo ich ramki rosną poniżej ESP. To fałszywa implikacja na x86. Dla F=postprologueESP i calla po SUB8 calleeESP=F-C, więc hypothetical zapis pod calleeESP+40 trafia dokładnie w F+34. Może wrócić ze zbalansowanym ESP. Kontrmodel jest syntetyczny; **nie twierdzę, że rzeczywisty import z A752B4 wykonuje taki zapis**. Jego target/mod-ref nie zostały wykazane w tym dowodzie.

Ponadto CA94 dostaje wskaźnik F+24; komórka F+34 jest od niego oddalona o10. Bez ograniczenia writów callee nie można jej wykluczyć przestrzennie. Ta konkretna gałąź idzie dalej do CD27, więc nie używam jej jako rzekomo wykazanego powrotu do wcześniejszego CD06. Dotyczy bezpieczeństwa późniejszych odczytów ramki. Twierdzenie, że niebadany kod poCD10 nie może wprowadzić writerów przed ewentualną backedge, również nie wynika z pokrycia samego przedziału.

Nie wykazano też pełnego mod/ref dla bezpośrednich CALL przed odczytem. Sam licznik direct syntactic stores nie obejmuje callee writes, REP writes przez alias oraz pamięci osiągalnej pośrednio. Opaque effect to brakująca przesłanka statyczna, nie problem rozwiązywalny wyłącznie runtime.

Zgodnie z kontraktem§6 preservation przy unknown effects powinno pozostać **CONDITIONAL/NOT_ESTABLISHED**, a X_store=X_entry jest równością **pod przesłankami preservation/noalias/normal stack effects**. Nie utrzymuję opisu, że bramka została zamknięta. Ten sufit nie unieważnia niezależnego backward trace argumentu źródłowego kopii.

QC001 nie otrzymał całego zakresu preservation: rzeczywiście dostał49 deklarowanych wierszy z siedmiu pakietów. Jego SUPPORTS dotyczy lokalnych claimów zawartych w promptcie. Nie jest niezależnym potwierdzeniem XSI-08/09. Część innych przejść także była niedostarczona; reviewer prawidłowo je zastrzegł. Parent musiałby odróżnić własną rederywację od zewnętrznego zakresu QC.

## 4. Dokładne adresy i długość bufora

Na85A421 wykonano PUSH, a dopiero potem LEA z bieżącego ESP+64. Definiując **S=ESP tuż przed PUSH naA421**, źródło wynosi **S+60**, nie S+64. Przy odwoływaniu do ESP w chwili LEA zapis +64 jest poprawny, lecz raport/frontier nie definiuje jednoznacznie punktu odniesienia. Następna analiza musi używać jednej bazy i śledzić wszystkie push/pop/call.

Dla13DWORD długość wynosi34hex=52B. Cel C3B0 to **[X+30,X+64)**, ostatni DWORD zaczyna się naX+60. TRANSFORM_INPUT_PROVENANCE opisuje +30..+5F, co obejmuje tylko12DWORD. Analogicznie źródło upstream to **[S+60,S+94)**, ostatni DWORD S+90.

Opis arg2 jako tylko13-float buffer z zakresem frame+2C..67 miesza rozmiary i pola większego lokalnego rekordu. Bezpośrednie stores i późniejsze użycie wskazują więcej pól; nie zamykają typu na13float. Dla arg1 już admitted kod rozdziela9 wartości w układzie3×3 oraz kolejne3 wartości z offsetów24/28/2C; trzynasty DWORD nie otrzymał osobnej semantyki. Hipoteza9+3+1 jest warta sprawdzenia, ale sama liczba13 nie dowodzi NiTransform, skali, osi, jednostek ani world-space.

## 5. Pętla przed A429 pozostaje kandydatem, nie potwierdzonym writerem

J020 pokazuje ogon pętli zapisującej przez ESI, stride z pola obiektu i backedges. Nie zawiera pełnej definicji ESI ani dowodu, że jego adres trafia w [S+60,S+94). Ta pętla może zapisywać inny bufor. FIRST_MISSING_EDGE słusznie przyznaje brak linku; terminalowe określenie „writer bufora = pętla” jest zbyt pewne.

Następny cel: znormalizować ramkę callera i przeprowadzić **backward slice rzeczywistych13 słów źródła**, oddzielając jawne stores, REP/callee writers, niezmienione incoming data i nieznane ścieżki. Pętlę otwierać tylko jako kandydata i wykluczyć, jeśli ESI prowadzi gdzie indziej. Nie inwestować całej analizy w interpretację strided buffer bez identity edge.

## 6. Modele — rzeczywiste sesje potwierdzone, wersja snapshotu błędna

Koordynator, smoke, probe, worker i reviewer istnieją w OpenCode DB, directory=D:/Eudoria_Reconstruction. Role, provider/model IDs, parentIDs, raw answers i deklarowane źródła są fizycznie zgodne. JW001 dostał32 wiersze; QC001 dostał49; oba oryginalne wyniki są byte-identical z assistant text. To realna praca dzieci, nie empty handoff.

**Wszystkie pięć sesji ma session.version=1.18.18.** MODEL_EFFECTIVE_OPTIONS podaje desktop1.19.3, choć bootstrap rozróżnia desktop od CLI i wskazuje faktyczne uruchomienie CLI1.18.18. Ten opis wersji trzeba sprostować addytywnie. Normalizowane dowody/scoped registry pokazują medium dla bazowego ID i aliasu default, a rzeczywiste sesje używają tych ID. Nie znalazłem podstaw do zarzutu high/max, ale same DB IDs nie dowodzą effort. Przyjmuję zgodność klienta jako wspartą scoped-launch provenance, z korektą wersji; nie jako obserwację żądania/API backendu.

REQUEST_EFFORT=NOT_OBSERVED i SERVER_EFFECTIVE_EFFORT=UNKNOWN pozostają właściwe. Nie powtarzano osobnych długich diagnostyk serwera. Następny guard powinien porównywać capture runtime_version z wersją rzeczywistej sesji, zamiast przyjmować nazwę aplikacji bootstrapującej.

## 7. Publikacja f470141

LIVE master w audycie=f470141948c1a3e613feb173bd91dab5e65fc667. Różnica odb8800da to30 ścieżek, entrypoint1/0,8f80190 nie jest ancestorem. Skan30 nowych blobów nie znalazł literalnych wierszy admitted listingu, raw-listing patterns, wyłączonych rozszerzeń binarnych ani sprawdzanych wzorców credentials. Skan nie jest uniwersalnym dowodem braku sekretów; treść trzeba nadal oceniać per-file. Nie stwierdzono tutaj powodu do wycofania publikacji.

**Nie dodano ani nie zmieniono żadnego manifestu publikacyjnego.** Kontrakt§11.6 wymagał odrębnego manifestu dopuszczonych plików z SIZE/SHA/blob-ID i bijekcją. Sam lokalny manifest122+1 obejmujący wyłączone ekstrakty nie zastępuje manifestu publicznego. Publikacja jest zatem formalnie częściowo niezgodna. Opis w receipt o27 publikowanych plikach też trzeba zastąpić dokładnym zakresem Git, nie sumowaniem etykiet katalogów.

W tym audycie przygotowano **PUBLISHED_DIFF_REHASH.csv**: niezależny post-hoc inventory30 zmienionych Git blobów, z przypiętym BASE/HEAD w PUBLICATION_REVALIDATION_SCOPE.json. Nie udaje pierwotnego prepublication manifestu i nie legalizuje historii retroaktywnie. Następny publisher może opublikować ten inventory, sprostowanie i nowy wynik jako addytywny pakiet. Nie zmieniać frozen local run ani historycznego publicznego REPORT.

## 8. Werdykt i dalsza praca

SCIENCE_VERDICT=PARTIAL_PASS_WITH_MATERIAL_CORRECTIONS.
PROCESS_VERDICT=WITHIN_NUMERIC_CAPS_WITH_REPORTING_AND_PUBLICATION_NONCOMPLIANCE.
EVIDENCE_INTEGRITY=PASS.
MODEL_VERDICT=REAL_GLM_SESSIONS_CONFIRMED_CLIENT_MEDIUM_SUPPORTED_VERSION_CORRECTION_REQUIRED.
PUBLICATION_VERDICT=CONTENT_SCAN_AND_ANCESTRY_PASS_REQUIRED_PUBLIC_MANIFEST_MISSING.

Najwyższa krawędź: definicje bufora [S+60,S+94) przed CALL85A429. Nie wymaga ona udawania zamknięcia preservation C3B0 ani wyboru klasy R. Trzymamy odrębne ścieżki: source transform data, conditional entry→store identity, unknown X↔R i model→world-instance join.

WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CURSOR_SOURCE_MEDIUM=UNKNOWN; CANONICAL_GATE_EFFECT=NONE. Nowy eksperyment nie został wykonany. Ten audyt i osobny authoring są nowymi plikami; brak zmian istniejących pakietów i Git. HARD STOP po audycie/przygotowaniu kontynuacji.
