# Niezależny postaudyt kampanii BUILDING PLACEMENT 5H

Werdykt naukowy: **PARTIAL_PASS_WITH_MATERIAL_CORRECTIONS**. Werdykt procesu: **NONCOMPLIANT_WITH_ADMISSION_AND_MANIFEST_CONTRACT**. Publikacja została rzeczywiście wykonana, a jej osobny manifest jest zgodny z commitem. Nie ma podstaw do awansu historycznego placement ani do przyjęcia pełnego PASS kampanii.

Audyt dotyczy frozen runu `PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018`. Wykonano go po zakończeniu kampanii, na zapisanych dokumentach i listingach. Nie uruchamiano gry, runtime, debuggera, Ghidry, dawnych writerów ani oryginalnego EXE. Źródłowy run i repo nie były modyfikowane.

## 1. Zakres niezależnej weryfikacji

Fizycznie policzono i przypięto **wszystkie 285 plików** źródłowego drzewa, sprawdzono 260 wierszy parent manifestu i 24 manifesty podrzędne, 16 zdarzeń CONTROL z 15 łączami hash-chain oraz ponownie 967 pinów korpusu. Wszystkie **1254 zapisane wiersze ekstraktów** porównano z fizycznymi liniami H5: 0 rozbieżności. Daje to **1253 unikalne VA instrukcji i 136 unikalnych miejsc CALL**.

Na poziomie semantyki odtworzono kluczowe lokalne przepływy: writer SF, shape producenta macierzy, worklist/pair/callback plumbing, granice P07/P11/P12 oraz byte-compare i stack mapping 745A70/745BF0. Sprawdzono tezy syntezy przeciwko raportom/QC i przeprowadzono kontrmodele. Nie deklaruję osobnego, niezależnego udowodnienia każdego podrzędnego CLAIM ani forensycznego odtworzenia wszystkich sesji modelu. Freshness/attribution sesji pozostają raportowane przez wykonawcę; same nazwy katalogów ich nie dowodzą.

W celu oceny trafności następnego kroku przeczytano także konkretny istniejący `GHIDRA_GATE_00407270.txt` poza starym katalogiem. To **AUDITOR_COUNTERCHECK_AFTER_RUN**, nie kontynuacja zakończonego eksperymentu ani retroaktywne rozszerzenie jego zakresu. Dalsze użycie tego pliku w nowym runie wymaga jawnego nowego katalogu/pina. Zapisany dekompilat nie staje się automatycznie dowodem instrukcji tego samego builda.

## 2. Integralność: zgodne payloady, niepełne manifestowanie

Parent `MANIFEST.json`: 44 542 B, SHA256 `EC012E1BE55A597BA7501C19DEC5423D027AAB00D04568C6E999033439CF04F8`.

- 260/260 wymienionych plików ma zgodne SIZE/SHA. Zero mismatch i missing dla tych wierszy.
- Fizycznie jest **285 plików**, nie 260 ani 261.
- Pominięto **24 manifesty** z `packages/*/MANIFEST.json` i `reviews/*/MANIFEST.json`. Poza listą może pozostawać wyłącznie manifest samego rootu, a nie wszystkie pliki o tej nazwie.
- Pełna bijekcja parent manifest↔dysk ma **FAIL**: 260 wpisów + 24 pominięte manifesty + 1 parent =285.
- Po dostosowaniu checkera do rzeczywistych schematów 24 manifestów: brak hash mismatch w istniejących wierszach hashujących; dwa QC (`P02_QC_R1`, `P03_QC_R1`) zawierają jedynie nazwy/role czterech plików, bez ich SIZE/SHA. To inwentarze, nie samodzielne manifesty integralności. Payloady tych QC są obecnie sprawdzalne poprzez hashujące wiersze parentu.

Wniosek nie brzmi „dowody zostały uszkodzone”. Zgodność wszystkich wymienionych payloadów pozostaje wartościowa. Odrzucam deklarację pełnego parent seal/bijection. Ten postaudyt dodatkowo przypina wszystkie285 plików, w tym brakujące24 manifesty, bez zmiany historii runu.

Parent manifest przyznaje nadpisanie pierwszej wersji, która pominęła CONTROL; zachowano jej SHA, lecz nie bajty. Kontrakt wymagał osobnej korekty/pakietu po błędzie pieczęci. „Przed zewnętrznym użyciem” nie zmienia faktu zapisu po pierwszym manifeście. Nowy run ma używać exclusive create i jednej standardowej manifestacji, a przy błędzie osobnego corrigendum.

Pierwszy ogólny checker tego postaudytu nie rozpoznawał kilku schematów nazw pól. Jego diagnostyka jest zachowana w `CHECKER_DIAGNOSTICS_V1.json`; poprawny adapter i wynik to `recheck_nested.py` / `NESTED_MANIFEST_RECHECK.json`. Błędy schematu checkera nie są przedstawiane jako hash mismatch źródła.

## 3. Rezerwacje i rzeczywiste liczniki

Suma rezerwacji jest zgodna z CONTROL: **32 ciała /1260 wierszy /153 CALL /32 warianty**, w globalnym limicie96/12000/320/48. Globalnych pułapów liczbowych nie wykazano jako przekroczonych. Naruszono jednak konkretne rezerwacje przed odczytem:

| Pakiet | Metryka | Rezerwa | Rzeczywiste | Dyspozycja |
|---|---|---:|---:|---|
| P06 | ciała obecne w ekstrakcie | 2 | 3 | ujawniony incydent, wymagany PARTIAL/NONCOMPLIANT procesu; brak nowych claims na dodatkowym ciele zachowuje wartość nauki |
| P07 | wiersze | 133 | 148 | przekroczenie +15, nawet przy zachowaniu VA window |
| P07 | miejsca CALL | 10 | 13 | QC pomylił10 różnych targetów z13 różnymi miejscami CALL |

**Miejsce wywołania to VA instrukcji CALL.** Dwa różne CALL do tej samej funkcji to dwa miejsca. Potwierdzony sumaryczny wynik kampanii wynosi136 miejsc, a nie133. Trzy brakujące miejsca wynikają dokładnie z błędnej reguły P07. Dlatego wcześniejsze136 w closing dispatch nie powinno być uznane za obalone wyłącznie sumą błędnych COUNTERS. Liczba różnych targetów jest osobną metryką.

P02 jawnie policzył dwa bloki kontynuacji 006B1C80 jako dwa „bodies”; P11 policzył dwa fragmenty tej samej ścieżki jako osobne wejścia. Zgłoszone30 nie jest potwierdzonym licznikiem unikalnych logicznych funkcji. Nie zastępuję go inną zgadywaną liczbą. Nowy ledger ma rozdzielać region, block, function-owner i unikalne ciało; indeks B5 tnący na granicach przepływu nie ustanawia samodzielnych funkcji.

Dodatkowe błędy granic:

- P11 zawiera VA006B6C9D mimo okna `[006B6C1B,006B6C9D)`. To wykluczony endpoint. Wiersz był już autoryzowany w P07, więc nie jest nowym globalnie nieautoryzowanym adresem, ale twierdzenie P11 „wszystko in-window” jest błędne. Ten dublet tłumaczy1254 sumy versus1253 union.
- P04: envelope zdarzenia ADMIT kończy się0067C921, choć kontrakt dziecka prawidłowo wymienia caller006A36F0. Jedna jawnie zlecona podgałąź leży poza envelope. To rozbieżność event↔kontrakt, wymagająca listy dokładnych subregionów zamiast jednego niedokładnego min/max.

Wewnętrzny QC nie ma uprawnienia do retroaktywnego przekształcenia przekroczenia rezerwy w zgodność. Dobre obsłużenie incydentu pozwala zachować wynik i kontynuować niezależny front; nie daje czystego PASS procesu.

## 4. Najważniejsza korekta naukowa: callback, getter i kontener

Zachowuję mocny wynik P06:008BD720 jest dwuwierszowym getterem zwracającym `ECX+18h`, bez dispatch. W P09 widać wywołanie otrzymanego callbacku, odczyt dwóch DWORD z wyniku i zapis do bufora z tail+4, limit+8, przyrostem tail o8. To konkretne fakty instrukcyjne.

Nie wynika z nich automatycznie scheduler, kolejka requestów, rejestracja callbacku ani asynchroniczny dispatcher. **Zwykłe synchroniczne kopiowanie/projekcja do kontenera append** spełnia wszystkie te obserwacje. Układ przypomina kontener vector; również ta nazwa pozostaje kwalifikacją struktury, nie potwierdzoną klasą C++.

Konkretny zapisany dekompilat `FUN_0040b070` w GHIDRA_GATE pokazuje wyłącznie `return param_1+0x14`. Przy poprawnej identyfikacji programu jest to member-view getter, a nie rejestrator. Surowe callsites wspierają ten model: callback trzymany jest w EBX/EDI, a po powrocie0040B070 trafia jako argument do późniejszego0043E5B0/006C3640; z wyniku0040B070 są pobierane dwa DWORD. Nie ma udowodnionego wywołania callbacku przez sam0040B070. Do czasu kwalifikacji provenance utrzymuję **registration semantics NOT_ESTABLISHED, saved decompile counterevidence present**.

Drugi brakujący most: para `{66h,A}` z ramki jest argumentem nieotwartego0043C700; para kopiowana przez callback jest odczytywana z `element+18h/+1Ch`. Kampania nie zamknęła równości tych dwóch źródeł wartości dla rzeczywistego elementu. Kolejność wywołań i zgodny rozmiar8B nie dowodzą tożsamości payloadu. Nie można ogłosić producer-side transportu konkretnego `{66h,296445}` „CONFIRMED end-to-end” poprzez nieotwarte transformacje i niekwalifikowany receiver.

Poprawny rezultat: **zmapowano kandydacki przepływ par i bulk projection/append; jego pełna semantyka resource-request, właściciel, consumer oraz powiązanie z instancją świata pozostają otwarte**. Brak targetów0043E5B0/0043C700 w H5 jest prawdziwą barierą pokrycia tego listingu, nie dowodem braku ich saved dekompilatów gdziekolwiek ani braku sensownych pytań na innych frontach.

## 5. SceneFeeder i property scan — zachowane wyniki oraz sufity

Writer005094C0 ma dokładny dziewięciowierszowy mechanizm: kopiuje3DWORD z argumentu do SF+34/+38/+3C i ustawia dirty+28. Nie niesie ID, parenta ani rotacji w swoim ciele. Nie utożsamiaj automatycznie tych pól z NiAVObject.m_kLocal ani z geograficznym XYZ.

0085BFA0 pobiera dane przez slot+24h obiektu `[this+2Ch]`, wykonuje operacje na floatach/wywołania helperów i formuje wynik matrix-shaped. **Nie znamy jeszcze podstawowego źródła danych receivera.** „COMPUTED” opisuje wrapper/przetwarzanie, nie dowodzi braku serializowanego/network źródła wcześniejszej transformacji. „Droga dominująca” nie ma runtime pomiaru częstości; należy mówić o zbadanych statycznych ścieżkach. 00862850 pozostaje alternatywnym field-copy z+3C..44h; tożsamość jego receivera i frame wymagają dowodu.

745A70 porównuje zero-extended byte z pełnym DWORD argumentu. Wartość20006, jeśli to ona trafi w operand porównania, nie może pasować; high bits nie są po prostu obcinane. To dobry wynik. Nie obala on scenariusza „obiekt klasy20006, osobny tag argumentu=6”. Przyjęta przez QC relacja key[3]→match operand jest slot-exact, ale szerszy FAMILY-P/T merge i semantyka argumentu caller-a nie zostały rozstrzygnięte.

## 6. Negatyw historycznych wartości musi pozostać w swoim zakresie

P08 przeczytał pięć dokumentów/pliki w całości lub we wskazanych sekcjach. Dobrze odróżnił transformy wewnętrzne296445/218757, file-scene-space, kontrolne wartości i zera od placement instancji. To zachowuję.

Nie jest to przeszukanie wszystkich967 źródeł. Werdykt powinien brzmieć **NO_QUALIFIED_HISTORICAL_INSTANCE_TRANSFORM_FOUND_IN_REVIEWED_SOURCES**, z pięcioma źródłami i cytowanymi granicami wcześniejszych poszukiwań. Zdanie „w całym korpusie nie ma wartości” ma większy zakres niż badanie.

Wniosek o server-session source z PE2/2003 pozostaje dowodem dla tamtego binarium. Kampania sama oznacza przeniesienie do9.3.5 jako UNVERIFIED. Nie może jednocześnie twierdzić, że wartości9.3.5 na pewno były server-only i dlatego nie mogą istnieć lokalnie. FIRST_PEINST0/6 nie jest samo w sobie pełnym inwentarzem wszystkich historycznych nośników. WORLD_XYZ_RECOVERED=NO i HISTORICAL_PLACEMENT=NOT_ESTABLISHED są nadal właściwymi statusami braku odzyskania.

## 7. Czas i powód zakończenia

Zegar tym razem jest odtwarzalny: START21:13:23.544925Z → STOP00:03:17.362015Z, około169.9min. Commit publikacyjny ma czas00:10:10Z; receipt00:11:09Z. Całość do receipt to około177.8min, również poniżej300min. Zatrzymanie science nie jest momentem zakończenia publikacji.

Istniał dodatkowy limit **12 pakietów**, który ja wprowadziłem w poprzednim authoringu. Osiągnięcie go jest uzasadnioną granicą kontraktu. Nie wymagam bezczynnego czekania do5h i nie uznaję samego krótszego czasu za naruszenie.

Nie przyjmuję jednak powodu „wszystkie sensowne krawędzie nauki wyczerpane”. Same artefakty zostawiają SF+30 writer/node-role, receiver slots, raw-copy class i inne dostępne krawędzie w H5. Poprawne rozstrzygnięcie to **PACKAGE_CAP_REACHED_WITH_OPEN_FRONTIERS** plus konkretne bariery niektórych gałęzi. Następny zwykły kontrakt nie ma limitu godzin ani arbitralnego capu liczby małych pakietów; pozostaje ograniczony pytaniem i jawnym budżetem naukowym.

TASK_DISPATCHES wymaga doprecyzowania:15 odpowiada opisanej liczbie prób wykonawczych, lecz raport osobno wymienia QC, joint sessions, closing i publikację. Nie certyfikuję15 jako sumy wszystkich Task bez inwentarza sesji. Rola, liczba pakietów, liczba prób i liczba sesji to odrębne liczniki.

## 8. Publikacja GitHub: rzeczywiście istnieje

LIVE master odczytany w czasie audytu: `2265ec61a1f00a45cdc9e95fdaf588b3708c1ddc`; parent commita `1aef60a94ce2ea56382470168e975f5732c02f34`. Sprawdzono bezpośrednio218 zmienionych ścieżek i217 wierszy osobnego PUBLICATION_MANIFEST: **0 mismatch/missing/extra**, self-excluded pozostaje tylko sam publication manifest. AUDIT_ENTRYPOINT ma1 insertion/0 deletions.

Nie opublikowano plików EXE/NIF/VFS/BNT/BIN ani lokalnych EXTRACT/whole-listing plików w tych nowych ścieżkach. Raporty zawierają krótkie analityczne przykłady mnemoników; nie myl tego z publikacją całego korpusu. Mechaniczny scanner zgłosił dwie ścieżki Users, które po odczycie są wyłącznie przykładami w polityce redakcji — false positive, bez podstaw do zgłoszenia wycieku sekretów.

Publikacja technicznie jest PASS. Semantyka opublikowanych raportów wymaga tego corrigendum. Kopie oryginalnych lokalnych manifestów w projekcji są metadanymi źródła, a nie manifestami bijekcji publicznych katalogów; do GitHub stosuje się osobny publication manifest.

## 9. Stan roboczy i następny cel

Zachowane: statyczny writer SF, getter008BD720, instrukcyjne elementy budowania pair/worklist, append-shaped zapis8B, byte-scan z dokładnym argumentem. Odrzucone/zawężone: pełna bijekcja260,133CALL sites, zgodność admission P06/P07, scheduler/registration przez0040B070, bezwarunkowy end-to-end pair identity, corpus-wide historyczne negatywy i wyczerpanie wszystkich frontów.

Najlepszy następny krok to **kwalifikacja przepływu par i ich rzeczywistego konsumenta**: member-view0040B070 w saved dekompilacie → pełne006C3640 z callbackiem008BD720 → właściciel kontenera/caller → najbliższy realny consumer. Hipotezy konkurencyjne: synchroniczne zbieranie zależności zasobów, transport requestów, inna projekcja danych. Najpierw rozstrzygnąć rolę, potem szukać właściwego owner-instance/transform edge. Nie nazywać z góry żadnej gałęzi „queue dispatcher”.

Nowy START ma jawnie dopuścić konkretny saved plik GHIDRA_GATE jako tekst, z pinem i ograniczeniem provenance. To nie wymaga dostępu do EXE/runtime. Nie przenosimy badania CreateMutex/gate z tego samego pliku do celu naukowego. W razie braku pokrycia pierwszej gałęzi pozostaje precyzyjny fallback SceneFeeder receiver/node-role w istniejącym H5.

Standing bez zmian: WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CURSOR_SOURCE_MEDIUM=UNKNOWN; CANONICAL_GATE_EFFECT=NONE. Nowego eksperymentu nie wykonano. Repo i frozen evidence pozostały nietknięte; publikację corrigendum i przyszłego wyniku zleca gotowy następny kontrakt.
