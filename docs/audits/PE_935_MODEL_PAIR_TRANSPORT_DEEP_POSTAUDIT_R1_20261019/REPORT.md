# Niezależny głęboki postaudyt — MODEL PAIR TRANSPORT QUALIFICATION R1

AUDIT_TARGET = PE_935_MODEL_PAIR_TRANSPORT_QUALIFICATION_SAVED_R1_20261019
SCIENCE_VERDICT = REQUIRE_CORRECTIONS
PROCESS_VERDICT = PARTIAL_NONCOMPLIANT_WITH_ADMISSION_CONTRACT
EVIDENCE_INTEGRITY = PASS
PUBLICATION_INTEGRITY = PASS
QC_ORIGIN = DESKTOP_INDEPENDENT_POSTAUDIT
CANONICAL_GATE_EFFECT = NONE

Wynik ma wartość: callback jest przypięty, lokalne kopiowanie par i append DWORD są widoczne, doprecyzowano kilku konsumerów. Nie przyjmuję jednak całego MASTER_ACCEPTED jako poprawnego rozstrzygnięcia semantyki. Niezależny bilans stosu obala trzy kontenery; kwalifikacja nieotwartych wywołań jest zbyt mocna. Kryterium integralności plików przechodzi, choć część twierdzeń przechowywanych w tych plikach wymaga korekty.

## 1. Zakres i fizyczna weryfikacja

Przeczytano przedstawiony terminal, kontrakt authoringu, raport nadrzędny, raporty naukowe, fizyczne ekstrakty, istotne CLAIMS/QC/RECHECKS, ledger i receipt publikacyjny. Wszystkie 111 wierszy nadrzędnego manifestu zweryfikowano własnym skryptem przeciw 112 fizycznym plikom. Pełna bijekcja PASS, wszystkie SIZE/SHA zgodne. Zweryfikowano także 9 manifestów zagnieżdżonych, łącznie 10 drzew manifestowych. Brak dowodu utraty lub podmiany wierszy źródłowych.

1275 zamkniętych pinów saved-katalogu przeliczono w całości: zero błędów. Żadnego exists/stat/hash/open oryginalnego EXE ani payloadu gry. Żadnego runtime/Ghidra/new export, zmian konfiguracji lub repo. Kod ze źródeł czytano, nie uruchamiano. Uruchomiono wyłącznie własne skrypty tego nowego audytu.

Każdy numerowany wiersz wszystkich 11 fizycznych ekstraktów porównano z właściwą linią H5/GHIDRA_GATE; kopia P01 R1/R2 jest fizycznie zdublowana, więc sumy wystąpień nie są union. Wynik: 451 fizycznych wystąpień listingowych =404 unikalne VA +47 kopii; 15 linii dekompilatu odrębnie. Union CALL=26. Wszystkie 10 ADMIT ma zgodny selected_lines_sha256 i zakresy. Sprawdzono pełny łańcuch poprzednich hashy 13 zdarzeń. Więcej informacji w INTEGRITY.json, EXTERNAL_RECHECK.json i RAW_AND_CONTROL_RECHECK.json.

Dowód chronologii: event chain i pliki wiążą dokumentowane zdarzenia; same mtime i hash chain nie są niezależnym dowodem, że model przed zdarzeniem nie przeczytał pliku inną drogą. Nie rozszerzam wniosku poza obserwowalny ślad pracy.

## 2. Najważniejsza korekta: jeden kontener, trzy wejścia

Nie są to trzy kontenery C1/C2/C3. Niech B oznacza ESP po PUSH EAX@006C407C. Trzy zapisy zerowe inicjalizują kolejne pola jednego nagłówka:

M32[B+1C]=0; M32[B+20]=0; M32[B+24]=0.

Wywołania kolekcji mają odroczone cdecl cleanup. Audytowane006C3FE0 i006C4020 kończą się RET bez immediate, a wywołujący między nimi nie dodaje ESP:

| Adres LEA | ESP względem B | Operand | Wynik |
|---|---:|---:|---:|
|006C4095|0|+1C|B+1C|
|006C40A8|-8|+24|B+1C|
|006C40B7|-10h|+2C|B+1C|

Każdy kolejny CALL zostawia dwa przekazane DWORD-y na stosie wywołującego. Wszystkie trzy przekazują ten sam adres C=B+1C. Nie jest to utożsamianie obiektów na podstawie podobnego layoutu; to równość wyprowadzonych wyrażeń adresowych, na normalnych powrotach z audytowanym protokołem stosu.

Następnie sort-shaped wrapper dostaje begin z B+1C i end z B+20. Kolejny equality-scan dostaje te same dwa sloty po dalszych PUSH. ADD ESP,28h@006C40E4 usuwa 24 bajty trzech wcześniejszych par argumentów oraz 8+8 bajtów dla dwóch konsumerów. Wynikowy model jest prostszy: trzy sekwencje wejściowe agregują do jednej wspólnej listy, która trafia dalej. Równość zawartości wpisów z różnych źródeł nadal nie wynika z tego wspólnego właściciela.

CONFIRMED oznacza tu statyczną arytmetykę na normalnych, zgodnych z ABI powrotach; nie jest to zapis runtime konkretnej instancji świata. Podstawa: oba kompletne helpery P04/P05, prolog/callsite P06/P07 i STACK_REDERIVATION.json.

## 3. ABI006C36B0 i przekazanie do006C29D0

P10 błędnie nazywa sink arg5. Dla S=ESP na wejściu006C36B0 trzy PUSH zapisujące EBP/EDI/ESI poprzedzają odczyt [ESP+1C]@006C36BF. Stąd ESI=M32[S+10], czyli **arg4**. Callsite literalnie przekazuje0x00BA45E8 jako ten czwarty DWORD. Faktyczny globalny odbiornik nie znika po poprawce numeracji.

Przed czterema PUSH caller rezerwuje i wypełnia blok sześciu DWORD-ów na stosie. Jest on przekazany przez wartość bezpośrednio za czterema argumentami, a nie jako jeden niesprecyzowany argument-pointer. Pierwsze słowo jest0x00823C10; następne pola należy śledzić indywidualnie.

Ważna korekta częściowej definicji: MOV byte ptr [ESP+4C],1@006C4125 ustala tylko niski bajt. Później MOV EBP,[ESP+4C] i MOV [EAX+14],EBP kopiują cały DWORD. W otwartym fragmencie brak wcześniejszego ustalenia pozostałych 24 bitów tego slotu. Przykład0xAABBCC00 po tym store daje0xAABBCC01, zgodny z instrukcjami, a nie1. Dlatego etykieta całego sześciosłowowego kontekstu zakończonego DWORD1 jest nadmierna. Niski bajt1 jest potwierdzony.

Dla callsite006C36E1 dokładny lokalny protokół to:

- ECX=S+1C, adres wewnątrz przekazanego kontekstu;
- stack arg2=S+14, adres początku skopiowanego bloku;
- stack arg3=S+10, adres slotu, do którego006C36DD wpisuje EDI, aktualny adres pary;
- stack arg4=0;
- stack arg1 pochodzi z M32[S+8] po wcześniejszym wyzerowaniu niskiego bajtu; rola semantyczna nieustalona.

Arg3 jest zatem wskaźnikiem na slot zawierający wskaźnik bieżącej pary. Zgubienie tego poziomu pośrednictwa w nowym trace dałoby fałszywy flow. Body006C29D0 nie otwarto w tym audycie; pozostaje konkretną następną krawędzią. To, że w przekazanym bloku jest0x00823C10, jeszcze nie dowodzi, że adapter rzeczywiście wywołuje właśnie to pole.

## 4. Co jest potwierdzone, a czego nie można wykluczyć

CONFIRMED: w006C3640 callback jest wywoływany synchronicznie; jego wynik jest na fast path kopiowany jako dwa DWORD-y, a tail rośnie o8. Znane immediate callbacku008BD720 w konkretnym callsite potwierdzono. W006C36B0 wynik EAX po opaque006C29D0 trafia na fast path jako DWORD do kontenera, z tail+=4. Slow-path helpery pozostają opaque. Nie przypisuję im dowiedzionego działania growth/insert na podstawie samej nazwy lub gałęzi tail==limit.

STRONGLY_SUPPORTED: wrapper006C3D40 przypomina sort/introsort po8-bajtowych elementach; rzeczywiste fazy006C3740/006C3330 są nieotwarte. CONFIRMED są obliczenia, przekazane argumenty i miejsca CALL. Wrapper006C2C90 porównuje dwie części sąsiednich8-bajtowych elementów i po równości woła opaque006C24B0. Samo to nie dowodzi pełnej semantyki usuwania duplikatów.

Należy rozdzielić trzy osie: lokalny mechanizm wykonania, domenę danych i skutki wywołań/dalszych konsumerów. H1 i H2 w dawnym brzmieniu nie muszą być rozłączne. Kontrmodel:006C29D0 synchronicznie dopisuje request do innej struktury, zwraca token, a widoczny kod kopiuje ten token do globala. Wszystkie widoczne instrukcje nadal pasują do H1, a efekt requestowy istnieje. Nie twierdzę, że taki efekt występuje; pokazuję brak podstaw do jego odrzucenia przy opaque callee.

Dlatego REJECTED dla etykiety „to wyłącznie rejestracja callbacku zamiast bezpośredniego wywołania” może być poprawne w widocznej rutynie, lecz „H2 request/queue/scheduler wykluczone dla całego łańcucha” jest zbyt mocne. Bezpieczny status: NO_QUALIFIED_ASYNC_CONSUMER_OBSERVED_IN_ADMITTED_ROWS; OPAQUE_EFFECTS=UNKNOWN. Tak samo brak widocznego instancjowania nie ustanawia braku tego działania we wszystkich wywołanych funkcjach.

Stałe adresy tablic nie ustalają ich pełnej zawartości, historycznego źródła, niezmienności ani domeny identyfikatorów. Pętle8+2+2 są widoczne; rola „compile-time resource dependencies” pozostaje hipotezą. Wartość rzeczywistego296445 nie została związana z aktualnymi tabelami. Tę granicę wykonawca prawidłowo zachował.

Dekomplikat0040B070 dosłownie podaje param+14h. Jest to potwierdzony fakt o zapisanym tekście. Ponieważ zgodność programu/build nadal jest UNVERIFIED, bezwarunkowe przypisanie callerowi pól owner+14/+18 wymaga tej jawnej przesłanki. H5 dowodzi pobrania dwóch DWORD z wartości EAX zwróconej przez CALL; nie dopisuje pochodzenia EAX z nieprzypiętego same-build ciała.

## 5. Proces, budżety, QC i zapisane incydenty

Ledger ma13 zdarzeń: START1, ADMIT10, DENY1 i STOP1. Nie12 ADMIT. Dziesięć logicznych przydziałów zmaterializowano w8 zamkniętych paczkach naukowych; P05 jest częścią P04, P07 częścią P06. Dwa niedokończone podejścia P01 nie są dodatkowymi paczkami naukowymi. Dwie próby wykonawcy, jedna pusta próba QC i jeden skuteczny reviewer to różne mianowniki. Autoryzowany DIRECT_ANALYST_FALLBACK był dopuszczalny.

P08 pozostaje ujawnionym naruszeniem admission:4 ciała przy rezerwacji2. Limit globalny nie anuluje naruszenia lokalnego. Dobrze, że proces nie został nazwany COMPLETE_WITHIN_BOUND. Dalszy opis FLD/FMUL i callsite innego ciała jest już pewną interpretacją; „wyłącznie strukturalne” nie oznacza, że nie otwarto tych ciał. Konserwatywne obciążenie musi je uwzględniać.

Suma rezerwacji wynosi20 ciał oraz23 kandydatów. Kontrakt zabrania refundacji. P08 dodaje dwa ponad rezerwację. Raport21 uzyskano przez odjęcie jednego ciała z P09 (rez3, report2), co nie odpowiada regule. Prawidłowe minimalne obciążenie bez refundacji to **22/24 ciała i23/24 kandydatów**. 404/4800 wierszy instrukcji,26/160 CALL i15/1000 linii body pozostają poprawne. Przestrzeń globalna nadal nie została przekroczona. To korekta accounting, nie wsteczna legalizacja P08.

Pozostałe drobniejsze korekty: HANDOFF i gates nadal mieszają419 z limitem instrukcyjnym, chociaż root REPORT rozdziela404 i15. artifact_index ma jeden stary self-row10899/778D..., a rzeczywisty plik11703/474459...; nadrzędny manifest poprawnie przypina aktualny plik. Receipt ujawnił ten self-reference quirk, więc nie jest to nowo odkryta korupcja. Historycznej paczki nie edytować.

Świeży reviewer QC_R2 sprawdził ważną część integralności i ujawnił5 usterek metadanych, lecz nie wykrył powyższych błędów ABI/dataflow. Przejście mechanicznych testów nie ustanawia poprawności semantycznej. Status internal QC jako wykonanej pracy zachowuję; akceptacja wszystkich load-bearing claims nie przetrwała zewnętrznego audytu.

## 6. Publikacja

LIVE master sprawdzony read-only:45fe1c22c64445127bd68c412e9fa2103425ee0b. Parent2265ec61a1f00a45cdc9e95fdaf588b3708c1ddc. Commit ma91 zmienionych ścieżek, newest-first wpis AUDIT_ENTRYPOINT1/0. Pierwszy receipt opisywał push branch, osobny addendum dopiero FF master; nie utożsamiam tych dwóch etapów.

Dwa publiczne manifesty mają24 i67 wierszy. Po deduplikacji wspólnych AUDIT_NOTICE/ENTRYPOINT otrzymano89 unikalnych ścieżek; wraz z2 self-excluded manifestami obejmują91 ścieżek commita. Wszystkie89 committed blob SIZE/SHA zgodne. Wszystkie81 plików kopiowanych z lokalnych źródeł porównano bajtowo z commit blobs: PASS. Publikacja przeniosła także błędne wnioski źródłowe; byte identity nie oznacza naukowej akceptacji.

Główny lokalny checkout nadal34cf114, bez tracked changes, z tymi samymi6 grupami untracked. Nie wykonano commit/push w tym postaudicie. Korekty należy opublikować addytywnie w nowym katalogu i AUDIT_NOTICE, bez zmiany zamrożonego runu. Potwierdzono wykluczenie ekstraktów z projekcji po porównaniu ścieżek manifestowych; nie publikowano nowego materiału gry przez ten audyt.

## 7. Poprawiony checkpoint i dalsza praca

Poprawny szkielet: trzy sekwencje wejściowe → jeden C → wrapper sort-shaped → adjacent-equality scan/opaque handler →006C36B0 → opaque006C29D0 → DWORD do globala0x00BA45E8 → dalszy consumer poza dotychczasowym oknem.

FIRST_MISSING_EDGE: pełne body006C29D0 i rzeczywiste pochodzenie jego wyniku z zachowaniem pointer-to-pointer callsite; następnie niedomknięta końcówka006C4060 oraz dokładne użycie elementów globala. Pierwszy fragment nie może być promowany do world root/resource handle z podobieństwa do dawnej pompki. Należy zidentyfikować, co wywołuje adapter i czy dane/receiver wynikające z literalnego funktora naprawdę wiążą się z zasobem lub instancją.

Nie rekomenduję kontynuowania wszystkich vtable w ciemno. Po krótkim trace adaptera i pierwszego konsumenta trzeba ocenić związek z MODEL_RESOURCE→WORLD_INSTANCE→TRANSFORM, a nie liczbę nowych funkcji. Jeżeli lista jest wyłącznie zasobami i nie ma kwalifikowalnego mostu, dopiero wtedy odłożyć gałąź i wybrać jeden konkretny saved-only frontier SceneFeeder. Brak guarantee dodatniego wyniku nie jest sam w sobie powodem rezygnacji z dobrze postawionego pytania.

Oddzielnie: ostatnie zlecenie instalacji Hermesa pozostaje innym kontraktem. Ten raport nie jest dowodem jego wykonania. Przy audycie nie znaleziono docelowego runu HERMES_INSTALL_CONFIG_R1. Nie konfiguruję aplikacji ani nie rozpoczynam badań w nowej platformie w ramach postaudytu.

WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CURSOR_SOURCE_MEDIUM=UNKNOWN; CANONICAL_GATE_EFFECT=NONE. Ustalenia o wspólnym kontenerze i ABI są postaudytowymi faktami statycznymi, nie odzyskaniem historycznej lokalizacji budynku.
