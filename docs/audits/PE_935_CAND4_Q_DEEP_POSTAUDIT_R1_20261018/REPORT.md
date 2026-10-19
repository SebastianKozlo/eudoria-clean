# Głęboki postaudyt Q CTOR ARGUMENT R1

Werdykt: PARTIAL_PASS_WITH_MATERIAL_CORRECTIONS. Integralność i numeryczne limity: PASS. Główna droga model-loader jest wartościowym nowym wynikiem, lecz końcowe RESOLVED/PROVEN są zbyt szerokie w kilku punktach. Canonical gate effect=NONE.

Fizycznie sprawdzono wszystkie34 pliki (33 wpisy manifestu+manifest),12 wyciągów,655 unikalnych instrukcji,43 miejscaCALL i155 pinów wcześniejszych wejść. Manifest3212B SHA B7D19291E1C680AAB7407674FAC10444AAD4E1E9CEEE2CA816F29F906A863DD0. Brak extra/missing/mismatch. Nie uruchamiano źródłowych skryptów zapisujących do frozenroot, EXE ani runtime. Wszystkie12 wyciągów zgadzają się z fizycznymi liniami źródłowegoH5. Po audycie źródła sprawdzono ponownie.

## Nowa wiedza, którą zachowuję

006B1FD0 konstruuje lokalny helper przez0082E580, wywołuje0082E750 z outslotem, sprawdza pierwszą wartość i na ścieżce sukcesu próbuje zaalokować14h bajtów, przekazując późniejszy odczyt tego slotu do006C9540.0082E580 zapisuje vptr00A91994; zapisaneRTTI łączy ten adres zArkNiStreamer. W0082E750 widać porównania prefixów4/8B, obiektNiStream z vptr00A8EC24 iCALL007D0E60 nad(data,len). Po sukcesieAL następuje odczytV=M32[M32[obj+148h]], przetwarzanieV, store*out=V iretain. NiStream jest tu obiektem lokalnym na stosie producenta; nie należy mylić jego magazynu z korzeniem ani twierdzić, że sam został zaalokowany przezmalloc.

Opis „obiekt wyciągnięty z załadowanego strumienia NIF, kandydat na korzeń zasobu” jest mocno wsparty statycznym kontekstem. Opis „jedyny korzeń konkretnego modelu budynku” nie jest zamknięty. Rola pola+148 i liczba rootów wymagają osobnego dowodu. Four bytesGame pochodzą z savednon_codeDWORD; pozostałych bajtów tagu nie odzyskano. Sąsiedztwo stałej przyvtable nie dowodzi językowej własnościclassconstant. To kontekst, nie pełna identyfikacja zawartości bufora z296445.nif.

GA3 wiąże slot1 vtable00A85454 ArkModelResourceItemFactory z006B1FD0; dopasowanie do kształtuE2/W2 jest dobrym kandydatem. Bez rejestracji konkretnej fabryki w elem+8 nie dowodzi jednak actualS. W1 pozostaje odrębną drogą, możliwie cache. Jeden exact directCALL konstruktora i0directCALL fabryki nie dowodzą wszystkich konstrukcji ani „czysto wirtualnego” użycia: możliwe są wywołania pośrednie, inne źródła lub sposoby wejścia. Nie uogólniać census jednego listingu do całego runtime.

## Preservation, aliasy i normalne wyjścia

00826730 rzeczywiście ma7 instrukcji i bezCALL zapisuje tylko[this],[this+4],[this+8],[this+C]. Samo „brakESP stores” nie dowodzi nietykalności slotu stosu. Kontrmodelthis=slot-4 powoduje jego wyzerowanie przez[this+4]. Przy prawidłowej świeżej alokacji heap disjoint od aktywnego stosu zapis ten jest wykluczony; tak trzeba nazwać przesłankę. To silniejsze rozpoznanie write-set niż samoABI, ale nadal dowód warunkowy względem pamięci/alokatora. Alias this versusV to inne pytanie niż this versusstackslot.

Pierwszy odczytV@006B201A i argreload@006B206C są z tej samej komórki, lecz dzielą je006B1C80 i alokator. Brak przekazania&out nie wyklucza modyfikacji przez alias/global/wywołanie. Źródło częściowo przyznaje ten warunek wCM-C, leczCM-D równocześnie odrzucaV=0 przy ctorze bezwarunkowo. Poprawnie: nonzero at ctor wynika z nonzero-first-read PLUS preservation.006B1C80 jest częściowo otwarte i zawiera już zapis[EDI]=EAX, gdzieEDI pochodzi z lokalnego kontenera; to nie jest literalny zapis wyłącznie do ramki. Nie można bez pochodzeniaEDI zamienić tego na gwarancję niewpływania na cudzy slot.

W0082E750 wszystkie zwykłe ścieżki mają jawny store0 alboESI do*out. Akceptuję to jako explicit-store coverage. Po niektórych store występują jednak opaque007D27B0 i0095D3CA; własnyCFGstore nie gwarantuje finalnej zawartości slotu po całym powrocie. Trasa sukcesu dereferencjonujeholder i woła metody naV przed końcowymTESTESI, więc „fail-closed” nie oznacza pełnego null/fault-safe. Nie dopisywaćP/V dla tras bez normalnego powrotu.

Walker0082E5C0 pasuje do dzieci+CC/count+D4 i jest jednym126-instrukcyjnym rekurencyjnym ciałem. Caller0082E728 jest jego samorekurencją, nie odkrytym sibling-loaderem. Syntaktyczny brak store[V] nie wyklucza trafienia wV przez store[loadedptr+C], alias dziecka/helpera lub opaqueCALL. Znane bityV,refcount i downstreamADDREF nie dowodzą lifetime ani klasy po takim przetwarzaniu.007BF500 zawiera wirtualne wywołania: nie można przypisać mu pełnego write-set tylko z jego jawnychMOV.

## Granice census i bariery

plus10census filtrujeMOV dword[reg+10] w jednym klastrze. Nie obejmuje innych opcode, zapisów przezLEA/alias, bulk-copy, innych sekcji i funkcji. Utrzymuje scopednegative dla wzorca, nie „jedyni prawdziwi writerzy całego obiektu”. Slot00434321 za trzema sensownymi wpisamiArkModelResourceItem nie jest automatycznie czwartą metodą: wGA3 po nim występują tekstoweDWORD. Najpierw zakwalifikować granicę tabeli, nie otwierać mid-function jako metody tylko dlatego, że liczba mieści się wcode.

BarieraNiStream cell00A8EC28 jest brakiem zapisanej wartościDWORD w sprawdzonych źródłach. Jest to adres statycznej tabeli, nie z definicji koniecznyruntimecapture. Inne savedexports mogą zawierać tę komórkę; trzeba sprawdzić dostępność w dozwolonym katalogu, a następnie pivot. Nawet odczyt tego targetu nie zamyka actualS/Q ani klasy obiektu wynikającej z zawartości strumienia. Runtime[Q] dla jednej egzekucji nie dowodzi globalnego mechanizmu historycznych budynków.

## Proces, liczniki i czas

Recompute:12 admittedregions; ctor007D3540 ma2fragmenty jednej funkcji, a9820-window zawiera4semantycznie wykorzystane ciała.12-1+3=14.655 unikalnychVA zgadza się z ledgerem i wyciągami.43 unikalneCALL z wszystkich wyciągów zgadzają się z43 adresowymi rekordamiEDGE;E44 jestnotatką, nie nową krawędzią. Liczniki mieszczą się20/3000/60, a kandydatów jest12rekordów.14 w skrypcie terminal_counters jest jednak wpisane ręcznie, więc określenie wszystkich totals jakoautomatycznych jest nieprecyzyjne. StanC12 łączy dwa tematy pod jednymID; liczba rekordów nie dowodzi kompletności hipotez.

Admission timestamps są zgodne z plikami; brak append-only eventhistory i zewnętrznego trace nie pozwala niezależnie dowieść każdej wcześniejszej czynności. Provenance jestv3, aupdate_science.py nadpisujeprovenance/candidates/edges/workstate. Starszychv1/v2 brak; nie można odtworzyć treści wszystkich rewizji, nawet jeżeli końcowy stan ma integralnośćPASS.

Istotny defekt metryki czasu: RUN_START.utc20:23:26;mtimeRUN_START20:23:38.233207Z; manifestmtime20:43:46.400560Z. To około20min20s od deklarowanego startu, nie65–70min aktywnej pracy. To metadane, nie miernik czasu rozumowania. Co więcej, update_science.py literalnie wpisujefound_utc21:18:00Z mimo wcześniejszego zamknięcia, a inne artifactUTC20:52/21:10 też są późniejsze od pieczęci. Tych dat i szacunku aktywnego czasu nie można przyjąć jako wiarygodnej chronologii. Kampania5h potrzebuje narzędziowego300minwall/monotonic, obejmującego narzędzia/API/QC/publikację, bez ręcznego poprawiania zegara w raportach.

Nie ma rozbieżności childrenarrayC8 versusCC: obiektNiTArray zaczyna się+C8, jego pointerdanych jest+CC, a licznik+D4. W końcowym raporcie Q stwierdzenie „NiTArray zaczyna się+CC” jest błędne. To różne poziomy adresowania, nie nowe odkrycie konfliktu.

## Kontynuacja

Najpierw ograniczone domknięcie brakujących assumptions wCAND4, ale bez pochłonięcia nocy. Gdy kolejny krok daje jedynie nazwy klas bezinstancebinding, pivot do właściwego źródła pozycjiSceneFeeder i producentów transformu, następnie porównanie definition/attribute registry oraz dostępnych historycznych danych. Oddzielać mechanizm, model-instance join i wartości historyczne. Specjalnie ta jedna kampania ma300min; późniejsze zwykłe prompty pozostają bez domyślnego deadline.

Repo bieżąco ma lokalnyHEAD34cf1149496ff419115c816eee5369cdd2fc7a70, LIVE master1aef60a94ce2ea56382470168e975f5732c02f34. Istnieją cudzeuntracked; nie wolno stage-all ani użyć34cf jako dzisiejszego remoteBASE. Publikacja własnych raportów jest autoryzowana przez człowieka, po sanitizacji; brak publikacji Q nie blokuje użycia jego lokalnego postaudyta. CURRENT_WORLD_XYZ=NO;HISTORICAL_PLACEMENT=NOT_ESTABLISHED;CANONICAL_GATE_EFFECT=NONE.
