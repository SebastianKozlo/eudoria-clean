# Głęboki niezależny postaudyt — SCENE INSTANCE TRANSFORM JOIN R1

**Werdykt: REQUIRE_CORRECTIONS.** Utrzymuję potwierdzony przepływ ECX z pola owner+0xC, kopiowanie13DWORD oraz mechanikę blendowania. Odrzucam główną rekwalifikację pola receiver+0x2C jako bezpośredniego adresu12floatów oraz wywiedzioną z niej barierę danych. Konstruktor ownera został zastosowany do innego, wskazywanego obiektu bez dowodu ich tożsamości. W dwóch zamkniętych plikach CLAIMS.json są ponadto rzeczywiste błędy składni JSON.

AUDIT_TARGET=PE_935_SCENE_INSTANCE_TRANSFORM_JOIN_SAVED_R1_20261019. SCIENCE_VERDICT=PARTIAL_PASS_WITH_MATERIAL_IDENTITY_CORRECTIONS; PROCESS_VERDICT=REQUIRE_CORRECTIONS; LOCAL_HASH_AND_BIJECTION=PASS; OUTPUT_SCHEMA=FAIL; PUBLICATION=MASTER_PRESENT_WITH_NEW_MANIFEST_SCHEMA_DEFECT; CANONICAL_GATE_EFFECT=NONE.

## 1. Niezależne pomiary fizyczne

Root107 wierszy+manifest=108 plików: pełne SIZE/SHA i bijekcja PASS, manifest SHA2562FC752440E7C932107C11C2B707FD274E64C461D3822F5982EF5DDBDA0AF1551. Pięć child manifests sprawdzono niezależnie; zawarte w parent. Authoring27+1 PASS. Wszystkie1560 pinów katalogu zgodne. Piny nie są tożsame z semantyczną lekturą każdego pliku.

Łańcuch13 zdarzeń START+11ADMIT+STOP poprawny.11/11 ekstraktów zgodnych dokładnie z przypiętymi źródłami;11 selected_lines_sha256 przeliczone niezależnie. Liczniki narzędzia:34body reservations,413listing rows,35listing CALL,34candidate reservations,712document lines,0incident debit. Zero debits nie jest równe34 reservations; właściwe charged=reserved+0. Nie ma dowodu przekroczenia globalnych capów.

Jednocześnie odczytane dokumenty z dekodowanymi instrukcjami zawierają26 dalszych unikalnych CALL VA; razem z listingiem daje to **co najmniej61 widocznych CALL-sites**. To dolna granica: nie interpretowano wszystkich hexdumpów/dekompilatów jako kompletnego zbioru instrukcji.35 jest poprawnym wynikiem starej funkcji liczącej listing-only, ale nie pełnym kosztem semantycznej lektury.712document lines to source-line union, nie liczba unikalnych instrukcji czy funkcji. Rezerwacje34 nie dowodzą poprawności lokalnego P09: cztery body przypisano szerokiemu regionowi z wieloma funkcjami bez rozpisania, które interpretowano. Local bound PASS jest NOT_DEMONSTRATED; nie wymyślam dokładnej nadwyżki.

## 2. Najważniejsza korekta: provider i dane transformu to różne poziomy

Wprowadzam jawne symbole:

- B — wejściowy ECX ownera w callerze00527AB0;
- R=M32[B+0xC] — receiver0085BFA0;
- P=M32[R+0x2C] — dalszy receiver/provider;
- VT=M32[P], F=M32[VT+0x24];
- T=retval CALL F — dopiero z T czytane są floaty.

Dowód z zamrożonego P04_EXTRACT poprzedniego R2:
0085BFA6 ładuje ECX=[ECX+2C];0085BFA9 EAX=[ECX];0085BFAB EAX=[EAX+24];0085BFB5 CALL EAX;0085BFB7 FLD[EAX]. CALL jest wykonywany **przed** odczytem floatów i nadpisuje EAX wynikiem. Nie istnieje tu dowód P=T. Nowy raport pominął dyspozycję i potraktował P jako T. To zmienia badane pytanie: najpierw trzeba kwalifikować provider P i target jego slotu24h, a następnie pochodzenie T. Sam writer R+2C może prowadzić do obiektu z metodami, nie do alokacji12-floatowego bloku.

Syntetyczny kontrmodel z oddzielnymi B/R/P/VT/T spełnia wszystkie jawne odczyty, a P!=T. To przykład dopuszczalnego modelu, nie dowód rzeczywistej nierówności pointerów klienta. Zachowujemy oba dopuszczalne przypadki; nie wolno zakładać ani równości, ani nierówności bez provenance.

## 3. Konstruktor B nie jest konstruktorem R

P04/P05/P09 wspierają ścieżkę konstruktora00528E50→0085B1B0 dla obiektu B, z vtableA7DCB0 i bazowąA91E4C. P09 bytes wskazują LEA EBP,[ESI+14], ECX=EBP przed CALL007345C0. P10 zeruje pola tego subobiektu, w tym+18. Efektywny adres to **B+14+18=B+2C**.

R natomiast pochodzi z **wartości M32[B+C]**, nie z LEA B+C ani z wejściowego B. Brakuje dowodu B=R. Nawet ten sam typ obu obiektów nie dowodzi tożsamości instancji. Dlatego brak podstaw do zdań: „R+2C leży w tym osadzonym subobiekcie”, „konstruktor wyzerował R+2C” oraz „provider/data-address na pewno podłączono po tej konstrukcji”. Fakty zerowania ownera pozostają ważne dla B. Zerowanie B+C pokazuje jedynie stan tego pola na opisanej ścieżce konstruktora; połączenie tej ścieżki z faktycznym B callsite jest nadal strukturalnie wspierane, nie pomiarem runtime.

Podobny błąd dotyczy przypisania receiverowi R metod0085B3E0/0085B6A0 i slotów1/3. Te zapisane ciała dotyczą rodziny ownera; ich udział w vtable R nie został wykazany. Nie wystarcza podobny zakres adresów ani wspólna nazwa „receiver”. Nazwa MovableObject pochodzi z etykiety dekompilatora; jej samodzielny byte-backed RTTI walk nie został w tym runie wykonany. Status nazwy STRONGLY_SUPPORTED jest właściwszy od CONFIRMED.

## 4. Co z mechaniką transformu pozostaje ważne

P01 rzeczywiście ładuje R z B+C, strzeże go i memberaB+10 przed NULL, wywołuje0085BFA0 oraz kopiuje13DWORD z EAX do R+30. Pierwszy wiersz H5 to **00527AB0**.00527AA0 jest dolną granicą nawigacyjnego requestu, nie wykazanym entry.

W0085C130 zachowane są: ten sam wejściowy R przy CALL0085BFA0; po poprawnym rebase stosu ciągłe slotsT_out+24/+28/+2C; L1=O+S*(C−O); dwa wywołania0096CD10; końcowe przekazanie wskaźników do0096D7C0; zwrot arg1. C nie jest dowodem XYZ budynku. Własny interpreter99 admitowanych wierszy, oparty na zwykłej semantyce x87, potwierdził dla S=0,1,1/4 oba endpointy i pełny push-shift, peak6 i depth0. Nie wykonuje instrukcji gry ani runtime; używa skończonych wartości wymiernych i jawnie zadanych wyników opaque helpers.

Dla usunięcia niejednoznaczności symboli definiuję A=out pierwszego0096CD10(this=R+30), Bfresh=out drugiego0096CD10(this=&freshTransform). Wtedy **L2=A+S*(Bfresh−A)**. To zgadza się z pakietowym v+S*(u−v), jeśli v oznacza pierwszy/stored, a u drugi/fresh. Nie twierdzę, że stary wzór ma odwrócone końce; wymaga jawnego związania symboli. Jego treść i FPU balance nadal zależą od cleanup/FPU-neutrality/out-write behavior nieotwartych helpers. Semantykę FSUBP odniesiono do [Intel SDM vol.2](https://cdrdv2-public.intel.com/774492/325383-sdm-vol-2abcd.pdf). Zaokrąglenia/NaN/FP control/runtime wartości nie były weryfikowane.

## 5. Korekty QC nie zostały domknięte maszynowo

Wszystkie JSON rootu/pakietów sprawdzono parserem, niezależnie od ich hashy. Dwa pliki nie są JSON:

- P02_CONTINUATION/CLAIMS.json, linia7/kolumna28: po `text:` wstawiono niezacytowany marker CORRECTED_PER_QC_F1;
- P03_DISPATCHER/CLAIMS.json, linia7/kolumna253: nieucieczone wewnętrzne cudzysłowy przy „identical roles”.

To błędy finalnych zamkniętych bajtów, a nie wyłącznie styl raportu. Sam prawidłowy manifest gwarantuje odtworzenie tych błędnych bajtów. P02 REPORT nadal ma pierwotne+20 i „non-contiguous” obok poprawnego parenthetical markera; sekcja odpowiedzi zachowuje stary błędny opis. F1 został poprawnie zdiagnozowany przez QC, lecz oznaczenie CORRECTED nie wystarczyło do usunięcia sprzeczności i walidacji finalnej struktury.

Nie kwestionuję niezależności świeżego recenzenta tylko dlatego, że rodzic zastosował później korekty. Odróżniam stan recenzowany, stan po poprawce i stan finalnie zapieczętowany: brakuje domykającego parse/schema/affected-claim recheck. Kolejny run musi stosować structured serializer i validator na finalnych bytes po ostatniej korekcie, przed każdym seal.

Sześć pustych prób workerów jest anomalią operacyjną. Jeden retry i direct fallback były dozwolone w kontrakcie; sama pustka nie jest podstawą PARTIAL_NONCOMPLIANT. Rzeczywiste odstępstwa są opisane osobno. Nie odtworzono tu sesyjnej telemetrii serwera — ledger jest przypiętą deklaracją wykonawcy.

## 6. Bariera danych jest przedwczesna

Denominator11admissions opisuje zbadane wycinki, nie całą dostępność1560 zapisanych plików ani całego H5. W bazowym źródle nadal są nieotwarte body i istnieje dozwolony mechanizm adaptive admission. Ocena niskiego prawdopodobieństwa sukcesu nie dowodzi braku saved evidence.

Wykonałem ograniczoną **nawigację strukturalną**, bez nowej analizy semantycznej tych ciał: w lokalnym przedziale85AC00..85B120 literalny MOV-store z displacement+C występuje przy**0085ACE9**; w85B900..85BFA0 displacement+2C przy**0085BE70**. To kandydaci, nie zakwalifikowani writerzy B/R. Zamknięte okna do ich zbadania są małe: [85ACD0,85AD10)26rows/1CALL oraz[85BD80,85BEE0)125rows/8CALL. Trzeba ustalić receiver, zapisywaną wartość i drogę do callsite. Nie ogłaszam odkrycia writera ani nie otwieram tych ciał semantycznie w tym postaudytowym kontrakcie.

Stwierdzenie „główna gałąź nie była data-blocked” jako powód pominięcia slot17 i równoczesne zamknięcie źródła transformu jako corpus-blocked jest niejasne. Alternatywa była opcjonalna; samo pominięcie nie dowodzi naruszenia. Wymagana jest jednak nowa ocena frontier po usunięciu błędu B/R/P/T. Najlepszy następny krok to te konkretne store-site qualification, następnie provider vtable i return-storage. Nie wracamy do globalnego szukania floatów.

## 7. Publikacja — co naprawdę poprawiono

LIVE master=f38349322ee32932583d73d43c7605d31f991fd7. Publikacja wykonana na master; rodzicbb42709, poprawne ancestry,66 nowych ścieżek, entrypoint1/0. Odczytano wszystkie66 committed blobs. Poprzednie manifestyV2 mają niezależne PASS65+1 i23+1; wcześniejsze błędy hash/omissions poprawiono addytywnie. To realnie wykonana część kontraktu.

Nowa projekcja59wierszy+manifest=60plików ma pełne membership i zgodne Git blob identities **po niezależnym odtworzeniu znaczenia trzech wierszy**. Sam CSV ma jednak5-kolumnowy header i3 metadata rows o4 kolumnach. Dotyczy EXCLUDED_ARTIFACTS.csv,PUBLICATION_ALLOWLIST.csv,REDACTION_MAP.md. Standardowy DictReader przesuwa pola: rozmiar wpada do src_sha256, SHA1 do blob_size, końcowe pole staje się NULL. To schema FAIL, mimo poprawnych blobów. Nie naprawiono tego w źródłach; następny prompt przewiduje addytywny V2 ze structured csv writer i ścisłą walidacją width/header/hash. Oba wadliwe CLAIMS.json zostały również opublikowane jako byte-identical projekcja i wymagają jawnego corrigendum, bez wymazywania historii.

## 8. GLM/default — fizyczny stan i następny kontrakt

Nie zmieniałem konfiguracji podczas audytu. Odczytano z maskowaniem sekretów tylko dozwolone metadane: główny nask-glm/glm-5-3 ma reasoningEffort=max; nask-glm/glm-5-3-high ma high; **nask-glm/glm-5-3-default ma medium**. Trzy projektowe profile pe-master/pe-reconstruction/pe-master-auditor jawnie wskazują pierwszy alias. Sama etykieta „default” w display name modelu MAX nie oznacza żądanego standardowego profilu.

Nowa autoryzacja użytkownika wymaga tylko standardowego GLM dla nauki i agentów. Następny kontrakt ma oddzielny mały etap ustawienia dokładnego istniejącego aliasu DEFAULT/medium, sprawdzenia effective agent/model options i pierwszego rzeczywistego child-session metadata przed badaniem. Nie wystarczy zmienić tekst promptu. Nie zakładamy honorowania reasoning_effort przez NASK na podstawie UI/HTTP200; client default i server behavior to różne twierdzenia. Obsługa cache odbywa się przez świeżą właściwą instancję lub kontrolowany wspierany reload bez przerywania cudzych zadań; brak cichego powrotu do max/high. W tym audycie zmiany nie wykonano.

## 9. Zakres i następna decyzja

Potwierdzone: mechanika member-receiver i statyczne rachunki, część konstrukcji B, warunkowy blend. Niepotwierdzone: dokładna klasa faktycznego B/R/P, attach/lifetime B→R, provider slot24/28 target, źródło T i rola instancji świata. Historyczne XYZ nieodzyskane. WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CURSOR_SOURCE_MEDIUM=UNKNOWN; CANONICAL_GATE_EFFECT=NONE.

Wytworzono nowy niezależny raport i pakiet następnego promptu; nie wykonywano następnego eksperymentu ani push. Zero odczytów/stat/hash oryginalnej gry, zero runtime, zero zmian frozen/source/config/repo. Dwa przerywane przebiegi własnego checkera zachowano pod versions: pierwszy nie obsługiwał nowego formatu Git-blob manifestu, drugi zatrzymał się przed nieznanym blob_size schema; po rozpoznaniu rzeczywistego błędu CSV końcowy checker raportuje go jawnie, nie naprawia. HARD STOP po authoringu i dostarczeniu promptu.
