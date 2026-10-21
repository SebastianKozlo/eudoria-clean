# Niezależny postaudyt SERIALIZER RECEIVER BINDING — R2

Werdykt: **PARTIAL_PASS_REQUIRE_MATERIAL_CORRECTIONS**. Integralność plików i zgodność sześciu ekstraktów z przypiętym listingiem mają PASS. Pełne pochodzenie X, różnica klas X/R, domknięcie ramki oraz deklarowana wyłączność Qwen/Gemma nie mają takiego potwierdzenia. Przygotowanego lokalnego commita **8f80190da8e8b7fd53a0b3b1978291f4a1e26daf nie należy wypychać**.

Audytowany run: `PE_935_SERIALIZER_RECEIVER_BINDING_HERMES_SAVED_R2_20261020`. Audyt wykonany fizycznie na WinDev2407Eval, na zapisanych wytworzonych źródłach i lokalnych obiektach Git. Bez oryginalnego EXE, runtime gry, nowych eksperymentów RE, inferencji, zmian modeli, loginu lub push. Zamrożony run i authoring pozostawiono nietknięte. Niniejszy raport koryguje interpretacje addytywnie.

## 1. Zakres i pomiary niezależne

| Sprawdzenie | Wynik fizyczny |
|---|---|
| Manifest runu | 66 wierszy + manifest = 67 plików; zero missing/extra/mismatch/duplicate |
| Manifest runu SHA256 | `56DB1176EF2258B7E1E56B83ADD63ABE581ADF75163F38F010BEB0335FABD23C`, 6259 B |
| Authoring R2 | 44 wiersze + manifest = 45 plików; zero błędów |
| Manifest authoringu | `EA1F88326A5A716F2E93F8C1FA0E5AF6D4655FAA4BDD0E7910ADDEB34A70B162` |
| INPUT_CATALOG | 1886/1886 pełnych pinów zgodnych |
| Ekstrakty J001–J006 | 6/6 odtworzone wiersz po wierszu z H5; zgodne selected_sha256 |
| Zapisane liczniki | 9 rezerwacji ciał, 300 wierszy, 18 CALL, 8 kandydatów; union wierszy=300, CALL=18 |
| Łańcuch zdarzeń | 12: START, 6 ADMIT, 3 NAV, 1 DENY, STOP; hash-chain zgodny |
| Sesje w izolowanym profilu | 8, a nie 7: smoke, cztery mikropróby, J001, Gemma R1, J007 |
| Manifesty przygotowanej publikacji | 63+1 oraz 56+1 zakresów plików; bijekcja, SHA256 i Git blob-ID PASS |
| LIVE origin/master w czasie audytu | `b8800da030662d4620f6cee437906103cf1a77bb` |

Brak plików o mtime późniejszym niż manifest jest zgodny z LAST, lecz same metadane czasu nie dowodzą nieprzerwanej historii zapisów. Integralność nie jest akceptacją interpretacji ani polityki publikacji. Parser JSON/CSV sprawdza składnię i szerokość, nie prawdziwość twierdzeń.

Źródło H5: `GHIDRA_H5_VTABLE2.txt`, 50 780 146 B, SHA256 `642CC29A01B8AD6F783E82E14DA4A61FA00BA6A3EC6DF98EDFF28AC25CC1D8DB`. Nowa weryfikacja nie otwierała żadnego nowego naukowego regionu poza sześcioma już dopuszczonymi oknami. Szczegóły: INTEGRITY.json, INPUT_RECHECK.json, ADMISSION_RECHECK.json.

## 2. Korekta zasadnicza: B nie jest R

Zachowujemy różne poziomy wskaźników: B to owner w ścieżce 00527AB0, natomiast R to wartość pola M32[B+0xC], przekazana do 0085BFA0 przy 00527AF9. Vtable A7DCB0 i konstruktor 00528E50 należą do ustaleń o **B**. Nie ustalają klasy wartości R przechowywanej w polu B.

SRB-C5 przypisuje A7DCB0 do „R class”, a SRB-C7/FIRST_MISSING_EDGE kierują census do tej klasy. Ten krok należy wycofać. Poprawny stan: **R_CLASS_IDENTITY=NOT_ESTABLISHED**. Nie wolno na tej podstawie odrzucać X=R ani wybierać rodziny 0052xxxx jako dowiedzionego writera R+2C. To powrót błędu wskazanego w poprzednim niezależnym postaudytcie OWNER_ATTACH.

## 3. Brakująca krawędź A → X i wyzerowanie pierwszego DWORD

J006 pokazuje wywołanie o kształcie alokacji 0x80 B, zachowanie jego wyniku w rejestrach oraz zapis A91DB8 do pierwszego DWORD badanego adresu. Nazwijmy ten wynik **A_alloc_shape**. Ciało 0095D3C4 nie zostało otwarte: świeżość, własność i semantyka alokatora pozostają przesłankami wzorca.

J006 kończy się przed 008580A0. J003 rozpoczyna się dopiero przy CALL 0085D410 na 00858240. Luka **[008580A0,00858240)** zawiera niezbadaną definicję ECX przekazywanego do tego wywołania. Nazwijmy ją **X_init_in**. Później wynik D410 przechodzi do ESI, a następnie do ECX przed CALL 0085C3B0 na 0085826D — **X_entry**. Te ostatnie lokalne przepływy są podparte J003; równość wcześniejszego A_alloc_shape z X_init_in nie jest wykazana.

J005 wnosi ważny kontrtest pominięty w syntezie: na 0085D41A inicjalizator zeruje **pierwszy DWORD swojego receivera**, a na 0085D429 jego pole +2C. Zwraca wejściowy adres this. Gdyby X_init_in równał się A_alloc_shape, wcześniejsze A91DB8 zostałoby przez ten zapis wyzerowane. Możliwe są także inny obiekt lub przesunięty subobiekt. Żadnej z tych możliwości nie rozstrzygamy bez luki.

W konsekwencji SRB-C2 wymaga rozbicia. Nie utrzymujemy bezwarunkowego „X_store = fresh heap 0x80 B, vptr A91DB8, zniszczony w F858”. **A_alloc_shape↔X_init_in=UNKNOWN; X_DISPATCH_VPTR=UNKNOWN**. In-place initializer jest dobrym ustaleniem lokalnym; nie jest dowodem, że jego receiver jest obiektem polimorficznym tej samej klasy co wcześniejsza inicjalizacja.

## 4. Ramka C3B0 → CD06: inicjalizacja potwierdzona, preservation otwarte

J002 potwierdza prolog kandydata wejścia 0085C3B0, wyrównanie ESP do 64 B oraz zapis wejściowego ECX do lokalnej komórki stosu na 0085C3C1. Potwierdza też przygotowanie kopii 13 DWORD z arg1 do obszaru this+30 oraz zapis arg4 do this+20. Dla wykonania REP MOVSD istotne są DF, nakładanie adresów i mapowanie argumentów.

J001 potwierdza późniejszy odczyt komórki [ESP+34] przy CD06 i wirtualną dyspozycję przez pole +28, slot +18 (indeks 6), której wynik zapisano do pola +2C na CD17. Ten lokalny opaque-return flow, SRB-C4, pozostaje ważny.

Pomiędzy tymi oknami nie ma pełnej analizy odpowiednich ścieżek, normalizacji ESP i wszystkich możliwości zapisu/aliasowania komórki. Sam COUNTERMODELS.json pozostawia jej przepisanie jako OPEN. Dlatego **„single dominant store” i „Etap A closed” są zbyt mocne**. Prawidłowo: X_store=entry-this **warunkowo**, przy preservation właściwej fizycznej komórki i zgodnym stanie stosu. Nie utożsamiamy układu kilku offsetów z tożsamością instancji R.

## 5. Odrębny caller nie dowodzi nierówności adresów

J004 pokazuje koniec F858 i nowe wejście 00858320. Receiver CALL 0085BFA0 przy 00858361 pochodzi z łańcucha **R68=M32[M32[C85+68]+10]**, gdzie C85 to entry-ECX tego callera, zachowany w EBP. Zachowujemy ten wzór i granicę funkcji.

SRB-C6 nie może jednak stwierdzać „it is not the F858 ESI object”. Inne funkcje, rejestry i offsety nie wykluczają równych bitów wskaźnika. **R68↔X_entry oraz R68↔R pozostają UNKNOWN**, dopóki przepływ wartości, zakres czasu i warunki aliasowania nie domkną relacji.

## 6. Proces: poprawne sumy nie rozwiązują ownership

Dokładne sumy eventów wynoszą 9/300/18/8. REPORT.md błędnie podaje 8 rezerwacji ciał. DENY szerokiego okna i późniejszy split są poprawnym działaniem fail-closed.

J004 rezerwuje tylko jedno ciało, a analiza wykorzystuje epilog F858 i odrębne wejście 00858320. To konkretny defekt lokalnego admission/owner accounting. J005 również zawiera D410 i początek następnego regionu D440 przy rezerwacji jednego ciała; nie dowodzę semantycznego użycia drugiego ciała, ale inventory nie wyjaśnia tej granicy. Nie wymyślam globalnego „11 bodies” i nie twierdzę, że przekroczono cap 64. Nie można kompensować zaniżonej rezerwacji J004 nadmiarem rezerwacji J002/J003 po fakcie.

**PROCESS_VERDICT=NONCOMPLIANT_WITH_LOCAL_OWNER_ADMISSION_AND_PARENT_GATE**. Zapisane zero INCIDENT oznacza zero takich zdarzeń, nie dowód braku wszystkich naruszeń. Helper nie jest sandboxem ani oraklem granic funkcji.

## 7. Faktyczne modele i ograniczenia review

Osiem sesji izolowanego profilu istnieje fizycznie. Qwen J001 dostał wszystkie 10 dosłownych wierszy J001 w promptcie; zerowa liczba tool calls w tej konkretnej odpowiedzi nie unieważnia analizy źródła przekazanego inline. Tool smoke wykonano osobno.

Gemma R1 dostała streszczenie roszczeń długości 1649 znaków, bez dosłownych wierszy listingów i bez wywołań narzędzi. To review spójności narracji, **nie niezależna rederywacja kodu**. J007 miał narzędzie, ale zapisany tool-result nie zawiera dosłownych wierszy żadnego z sześciu ekstraktów. Nie promujemy jego VERIFIED/PARTIAL do niezależnego zamknięcia pełnego trace. „Nothing refuted” nie znaczy „proven”. Nie porównujemy jakości modeli na podstawie różnych pakietów wejściowych.

W MODEL_GATE primary_session_id wskazuje smoke `20261020_073214_21118c`. Faktyczny rodzic desktop `20261020_040227_b6b193` jest oznaczony w Hermes jako **glm-5-2** i ma naukowe wiadomości oraz model_usage dla tej sesji. Run sam przypisuje J002–J006 do PARENT_DIRECT. Deklaracje „mechanical bootstrap only”, „GLM excluded science”, „wyłącznie Qwen/Gemma” są zatem niezgodne z metadanymi i atrybucją. Nie ustalono effort rodzica: nie twierdzę, że był high/max, ani że metadane dowodzą tożsamości zdalnych wag.

**Wada poprzednio przygotowanego przeze mnie guardu:** akceptował prawdziwą sesję smoke jako dowód primary, bez powiązania z rzeczywistym koordynatorem. Sam poprawny smoke nie wystarcza. Nowy kontrakt musi wymagać osobnego ID aktywnego rodzica, markeru kontraktu w jego rzeczywistym promptcie, odczytu DB i odrębnego role ledger. Bootstrap nie może podejmować analizy naukowej, a później konwertować jej na qualified parent przez odpowiedź dziecka.

## 8. Publikacja: integralna, lecz niedopuszczalna treściowo

Commit 8f80190 zmienia 57 ścieżek: 56 nowych plików i jeden wiersz entrypoint (1/0). Oba nowe manifesty zgadzają się z blobami. Jednak nowy blob **JOBS/J001_EXTRACT_INLINE.txt** zawiera 10/10 dosłownych wierszy źródłowego listingu. Łamie to wcześniejsze wyłączenie ekstraktów także poza katalogiem EXTRACTS. Samo rozszerzenie .txt lub nazwa JOBS nie czyni payloadu publikowalnym.

LIVE master pozostał b8800da. **Nie wznawiać push 8f80190 ani jego potomka.** Usunięcie pliku w następnym commicie zachowałoby jego treść w publikowanej historii. Zachować ten commit lokalnie jako evidence. Nową sanitizowaną publikację zbudować z rzeczywistego aktualnego LIVE master, kopiując wyłącznie ocenioną allowlistę, z korektami tego audytu i nowym manifestem publikacyjnym. Bez cherry-pick całego 8f80190, force, reset i ruszania historycznych plików.

Komunikat o braku możliwości odczytu Username potwierdza niedostępność uwierzytelnienia w tej ścieżce, **nie dowodzi wygaśnięcia/usunięcia poświadczeń**. Nie diagnozowano tu logowania ani nie zmieniano sekretów. Brak dopasowania dwóch prostych wzorców sekretów w skanerze nie zastępuje oceny całej allowlisty.

## 9. Następny krok i standing

Priorytet: **dokładny ECX i argument CALL 0085D410 na 00858240, przez brakujący odcinek F858 [008580A0,00858240)**. Następnie arg1 kopii 13 DWORD w C3B0 oraz — jako osobna bramka — preservation lokalnej komórki do CD06. To rozstrzyga ścieżkę danych; census hipotetycznej „klasy R=A7DCB0” należy porzucić.

Każda luka lub opaque CALL ma pozostać jawną barierą. Nie wymuszamy ani A=X, ani A≠X, ani X=R. Jeśli okaże się, że to rekord pomocniczy, wniosek ma tak brzmieć. Nadal nie dowiedziono związku z konkretną instancją budynku i historycznym transformem.

WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; RESOURCE_INSTANCE_JOIN=NOT_ESTABLISHED; CURSOR_SOURCE_MEDIUM=UNKNOWN; CANONICAL_GATE_EFFECT=NONE. Nowy eksperyment nie został wykonany. Brak commit/push w tym audycie. HARD STOP po audycie i przygotowaniu osobnego kontraktu.
