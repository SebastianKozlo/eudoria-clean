# Audyt Desktop: EU935 static placement, 7053654 → 2a2ba8d

Data: 2026-09-13. Audytor: Codex Desktop. Werdykt: **PARTIAL_PASS — REQUIRE_CORRECTIONS**. Jest to ocena raportów i dowodów, bez promocji kamieni milowych.

**Rdzeń pomiarowy przetrwał kontrolę, ale akceptacja całego mechanizmu statycznego placementu jest przedwczesna. Znalazłem pięć materialnych problemów: dwa błędne przypisania semantyki do getterów, dwa nieuprawnione wykluczenia ścieżek oraz niewystarczający dowód wyłącznego pochodzenia transformacji.** Nie są to wyłącznie dwie literówki wymienione w otrzymanym werdykcie.

Audyt dotyczy obu przekazanych podsumowań oraz ich wspólnej podstawy: pakietów JOIN/ERRATA_R2, STATIC_INSTANCE, PLACEMENT_SOURCE i ROUND_REPORT. Lokalne repo: `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean`. Przed publikacją mojego pakietu lokalny HEAD i odczyt `git ls-remote origin refs/heads/master` wskazywały `2a2ba8ddc864d16b0b31e6ef7928e0e2af922633`. Zakres od `7053654` zawiera dokładnie 5 commitów, 637 zmienionych plików, 207501 dodanych linii. Poza `docs/audits/` zmieniono tylko `AUDIT_ENTRYPOINT.md` (+5/-0). Stan roboczy: wyłącznie obce `?? experiments/`.

## F1 — P1: „A → ArkObject+0x28” pomyliło obiekt klasy z rekordem templates.vfs

Miejsca: [RUN3 REPORT, §1](https://github.com/SebastianKozlo/eudoria-clean/blob/2a2ba8d/docs/audits/PE_935_STATIC_INSTANCE_TRACE_R1_20260913/06_REPORT/REPORT.md#L13), RUN3 QC §A8, HANDOFF; powtórzone w ROUND_REPORT §1b i jego diagramie.

Twierdzenie mówi, że `FUN_00726E70` otrzymuje rekord template'u, wywołuje „getter A” i kopiuje identyfikator modelu do encji `+0x28`. Instrukcje potwierdzają odczyt pola, ale przypisano im niewłaściwy typ wejścia.

Moja weryfikacja z oryginalnego EXE, niezależnym mapowaniem PE:

| Element | Wynik |
|---|---|
| Vtable `0x00A86850` → COL `0x00AA7F28` → TypeDescriptor `0x00B8D068` | RTTI `.?AVArkObjectClass@@` |
| Slot 1 tej vtable (`+4`) | `0x0070BF50` |
| Fabryka `FUN_0070BF50` | Zapisuje własne `this` w ESI, alokuje 0x58, przekazuje ESI jako pierwszy argument `FUN_00726E70` |
| Konstruktor `ArkObjectClass`, `0x0070CFB6` | Zapisuje vtable `0x00A86850` |
| `0x0070CFC1`: `89 6E 08` | Zapisuje argument konstruktora klasy do `class+8` |
| Getter `0x007CE1E0`: `8B 41 08 C3` | Wyłącznie odczyt `this+8` |
| Konstruktor `ArkObject`, call `0x00726EB7`, store `0x00726EBC` | Kopiuje pole pierwszego argumentu `+8` do nowego obiektu `+0x28` |

To jest konkretny kontrprzykład dla globalnego utożsamienia `FUN_007CE1E0 = getter model-ID A`: istnieje droga `ArkObjectClass → jego fabryka → ArkObject`. W oryginalnym `.text` naliczyłem 808 kandydatów bezpośrednich wywołań tego stuba. Nie sklasyfikowałem ich wszystkich i nie twierdzę, że wszystkie są scaleniem linkera. Wystarcza wykazana odmienna proweniencja odbiorcy.

**Korekta:** wycofać ten konkretny most `templates.vfs.A → ArkObject+0x28`. Utrzymać fakt kopiowania `class+8 → object+0x28`; dokładną rolę tego pola klasy ustalić oddzielnie. Również `DAT_00BA58CC` z przykładu `ArkSurgeonObject` wymaga śledzenia writera, zanim zostanie nazwany template'em modelu.

Nie obala to wcześniej wykazanego odczytu A z prawidłowo zidentyfikowanego rekordu `templates.vfs` ani joinu A→NIF. Obala przenoszenie tej semantyki na dowolne wywołanie wspólnego gettera.

Artefakt własny: `probe.json → checks.receiverCounterexample`; pomocniczo dostarczone `GA3_CTOR_ArkObjectClass_0070CF80.txt`, `GA4_PSEUDO_0070BF50.txt`, `GA3_CTOR_ArkObject_00726E70.txt`.

## F2 — P2: „D wybiera wariant 4/5→2, 6→3, 7→4” jest błędne

Miejsca: [Z4_field_d.md](https://github.com/SebastianKozlo/eudoria-clean/blob/2a2ba8d/docs/audits/PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913/02_ANALYSIS/Z4_field_d.md#L31), §2–3; [RUN4 QC §B10](https://github.com/SebastianKozlo/eudoria-clean/blob/2a2ba8d/docs/audits/PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913/06_REPORT/QC_REPORT.md#L85).

W `FUN_008553D0`, w gałęzi param-setu `0x4E38`, wartość sterująca tym switchem pochodzi z **CALL `0x008557FD → 0x007CE1E0`**, a więc z odczytu **`+0x08`**, nie `+0x10`. Następnie EAX trafia do ESI i jest używany w selektorze `ESI−4`. Wcześniejsze wywołanie `FUN_0048ADA0` nie jest źródłem tego selektora.

Potwierdziłem to bajtami EXE i porównałem z dostarczonym `ZS1_PSEUDO_008553D0.txt`: sam dekompilat już pokazuje `uVar13 = FUN_007ce1e0(); switch(uVar13)`.

Dodatkowo wyliczenie callerów stubów `+0x10` nie dowodzi, że ich `this` pochodzi z `templates.vfs`. To ten sam problem typowania co F1. Oznaczenia „D-dword”, „D-f32”, „konsument D = LOD/priorytet/selektor” wymagają śladu odbiorcy dla każdego istotnego miejsca.

Wartość D samego template'u 4508 jest rzeczywista: offset pliku **96528**, bity **0x42F9E1CB**, f32 **124.94100189208984** — mój odczyt. **Jej rola pozostaje UNKNOWN.** Nie ma też podstaw, żeby ogłosić jej semantykę z zasady „nierozstrzygalną statycznie”; nie została dotąd rozstrzygnięta.

Artefakt: `checks.fieldDSelector`, `checks.join.template4508D`.

## F3 — P1: negatywy bajtowe nie wykluczają plikowego placementu

Miejsca: [RUN4 QC §B7–B8](https://github.com/SebastianKozlo/eudoria-clean/blob/2a2ba8d/docs/audits/PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913/06_REPORT/QC_REPORT.md#L64), RUN4 REPORT §3, ROUND_REPORT §1c, a szczególnie przyszła bramka G3 w pierwszym załączonym werdykcie.

Potwierdzam: 276 poprawnie wylistowanych `.prt`, 73218 bajtów payloadów, 276/276 CRC, brak 13 wskazanych wzorców LE32 na wszystkich offsetach. Potwierdzam też 27 plików VFS w Parameters. To jednak **nie dowodzi**, że żaden z tych plików nie może zawierać placementu, identyfikatorów pośrednich lub danych używanych do jego wyliczania.

Nie zdekodowano pełnej gramatyki wszystkich badanych nośników ani całego łańcucha ich konsumentów. Sam raport przyznaje brak dekodu 20xxx i brak pełnego `FUN_0084F7A0`. Nawet pełne pokrycie bajtów skanem nie daje pokrycia możliwych kodowań: klucze mogą wynikać ze schematu, indeksów, nazw, pola o innej szerokości, kompresji albo obliczeń. Te możliwości są wyjaśnieniem ograniczenia testu, **nie odkryciami ich występowania w EU935**.

Najbardziej niebezpieczna propozycja brzmi: brak kluczy w 27 plikach → wykluczenie kanału FILE dla statyków. Odrzucam tę regułę. Poprawny wynik takiego skanu to `ANCHORS_ABSENT_SEMANTICS_OPEN`. „27 plików” nie oznacza też „27 rodzin formatów”.

**Korekta:** funkcja portalowa jest pozytywnym tropem dPVS; brak bezpośrednich kotwic placementu jest negatywem o dokładnie tym zakresie. Etykiety „wyłącznie”, „czysty”, „brak pliku-placementów udowodniony” wymagają osobnego dowodu kompletności. Nie podnosić hipotezy sieciowej automatycznie po takim negatywie.

Ten sam rygor dotyczy RUN2: lokalna macierz D3 pisze, że badany kod WarEmu **nie pokazuje** ścieżki statycznego miasta. Streszczenie rundy robi z tego twierdzenie o klienckim przechowywaniu miast w obu grach. Przywołana przesłanka sama tego nie rozstrzyga; potrzebny byłby dodatni dowód właściwej ścieżki WAR. Nie przenosić tego wniosku na EU935.

## F4 — P2: 0/38 etykiet STATIC_WORLD nie wyklucza użycia tych funkcji przez budynki

Miejsca: [Z2_CLASSIFICATION_TABLE.md, wniosek 4](https://github.com/SebastianKozlo/eudoria-clean/blob/2a2ba8d/docs/audits/PE_935_STATIC_INSTANCE_TRACE_R1_20260913/02_ANALYSIS/Z2_CLASSIFICATION_TABLE.md#L62), ROUND_REPORT §1b i §4, PE_MASTER_REVIEW RUN3.

Mój skan potwierdza liczby kandydatów CALL: lookup 25, pump 13. Lecz własna tabela raportu zawiera **8 MODEL_MACHINERY, 17 OTHER i 1 UNKNOWN**. W szczególności:

- `FUN_00567170`: lookup i rekord z transformem; tabela mówi wprost, że użycie przez statyki jest nierozstrzygnięte.
- `FUN_005B5F90`: analogiczny rekord derived; rola oznaczona jako niepewna.
- `FUN_006CB6F0`: ogólny twórca instancji modelu, pump `0x006CB7CF`.

Ogólna funkcja ładowania może obsługiwać budynki, awatary i roślinność. Zakwalifikowanie jej jako „mechanizm” nie jest dowodem wykluczenia jednej z tych klas. Raport wręcz odsyła do twórcy instancji, którego sam policzył w rzekomo wykluczonej powierzchni.

**Korekta:** „nie zidentyfikowano call-site'u dowiedzionego jako dedykowany STATIC_WORLD”. Usunąć „statyki NIE przechodzą przez te call-site'y”. Oddzielić rolę funkcji od dowiedzionej klasy obiektów wejściowych. Wrócić do wskazanych trzech kandydatów, zanim porzuci się powierzchnię lookup/pump.

## F5 — P2: test „WYŁĄCZNIE z atrybutów” nie sprawdza pochodzenia wartości

Miejsca: [qc_b2_exclusive.py](https://github.com/SebastianKozlo/eudoria-clean/blob/2a2ba8d/docs/audits/PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913/00_CONTROL/qc_probe/qc_b2_exclusive.py), RUN4 QC §B2, HANDOFF i PE_MASTER_REVIEW.

Skrypt wyszukuje wywołania funkcji atrybutowych w przybliżonym ciele funkcji. Nie śledzi argumentu settera, nie dowodzi związku danych ani nie sprawdza każdej gałęzi. Do grupy ATTR włącza nawet **writer** `FUN_00845F70`. Kończy ciało na trzech bajtach CC, co jest heurystyką, a nie ogólnym dowodem granicy funkcji. Jego wynik jest listą wywołań, nie samodzielnym walidatorem wyłączności.

Zbudowałem kontrolę logiczną: legalna sekwencja instrukcji wywołuje getter atrybutów, ignoruje jego wynik i podaje setterowi pozycji niezależny wskaźnik `0x2000`. Obecność obu CALL pozostaje prawdziwa. To **kontrprzykład dla predykatu**, nie twierdzenie, że identyczny fragment istnieje w EU935, i nie wynik uruchomienia klienta.

Sam QC pozostawia 11/26 callerów konstruktora bez zbadanej semantyki. Przy czterech ścieżkach przyjmujących wartości z parametrów opisuje dalszy ślad tylko dla `FUN_005B5F90`; zdanie „10 bezpośrednich + 4 parametrowe” nie rozlicza piętnastej funkcji. Nie dowiedziono też wszystkich bezpośrednich store/copy do pól.

**Korekta:** zachować wykazane ścieżki `builder → getter atrybutów → setter`, cofnąć kwantyfikator „wyłącznie”. W nowej tabeli każdy argument settera ma mieć definicję, odbiorcę, gałąź, upstream i granicę. Brak danych = UNKNOWN. Źródło wartości w drzewie nadal może być plikowe, sieciowe, mieszane lub wyliczane.

## Drobne korekty i proweniencja

- Potwierdziłem dwie zgłoszone literówki: zapis vft jest **0x006FA8BD (+0xD)**; 296445 LE to **FD850400**.
- Są kolejne błędne adresy w RUN3 QC §A8: zapis vft ArkObject jest **0x00726EA1**, nie `0x00726E9F`; store do `+0x28` jest **0x00726EBC**, nie `0x006726EBC`. Bajty w moim `receiverCounterexample` pozwalają to odtworzyć.
- QC §B8 przypisuje executorowi skan kotwic „aligned-only”. `s12_prt_content_check.py` używa dla 13 kotwic `payload.find` i przesunięcia o 1, czyli już skanuje wszystkie offsety. Wyrównany był osobny census u32. Powtórka QC nadal jest niezależnym wykonaniem, lecz nie zwiększyła zakresu tego skanu.
- `Execute` ma zero znalezionych bezpośrednich CALL, a istnieje jego vtable. To nie jest dowód statycznej niemożliwości dotarcia przez dispatch pośredni ani wyczerpania RE.
- Pokrycie nazw A wynosi **3618/3618 = 100%**. Udział tych modeli we wszystkich NIF-ach to **3618/5596 = 64.6533%**. Nie łączyć tych mianowników.
- Manifest rundy: **49/49 hashy zgodnych** po uwzględnieniu jego formatu (45 plików + 4 odwołania; 4 komentarze). Stare manifesty RUN3 i RUN4 mają odpowiednio 1 i 4 rozbieżności dokumentacyjne względem HEAD; wszystkie pięć nowszych plików pokrywa manifest zamknięcia. **Nie stwierdzam naruszenia integralności.** Potrzebna jest czytelna reguła nakładania manifestu zamknięcia na historyczne manifesty. Obecny format miesza rekordy 2- i 3-kolumnowe z komentarzami.

## Moje wykonania i ich granice

Skrypt `probe.mjs` korzysta tylko z Node i własnych procedur PE, indeksu BNT2, spaceru VFS, CRC32, SHA256 oraz skanów. Nie importuje parserów executora. CRC32 skalibrowano znanym wektorem `123456789 → CBF43926`. Wynik i dokładny hash wykonanej wersji: `probe.json`; stdout: `probe.log`.

| Sprawdzenie | Własny wynik | Co dokładnie dowodzi |
|---|---|---|
| SHA EXE, templates, Models, Volumes | zgodność z podanymi pinami | Tożsamość wejść |
| templates.vfs | 5438 rekordów, 0 CRC-fail, dokładny EOF | Poprawne przejście tej struktury |
| JOIN A/NIF | 3618/3618, 0 braków; 5596 NIF-ów | Powiązanie nazw w danych, nie instancji świata |
| JOIN B/BVI | 1666/1666; 3746 rekordów B=0 | Powiązanie nazw kolizji |
| 4508 / 4752 / 2249 | A/B zgodne; negatywy typów nieobecne | Kotwice i separacja rozszerzeń |
| Portals | 276 wpisów/CRC, 0×13 wzorców, okno 505k–510k = 19 | Ograniczony negatyw bajtowy |
| S14 | 64/64 offsetów i sekwencji zgodnych | Adresy/bajty, nie automatyczna semantyka |
| Kandydaci CALL | 25/13/53; settery 15/11/7; init 21; ctor 26 | Surowe E8 rel32; nie niezależne dekodowanie wszystkich granic instrukcji |
| Attribute-setter | zbiór 53 VA identyczny z ZS3 | Zgodność wskazanej powierzchni |
| Dispatch 0xB9 | slot12 → 004B1A11 → call005B72C0 | Konkretna krawędź; nie pełna gramatyka komunikatu |
| ArkObjectClass i selektor | F1/F2 odtworzone z EXE | Materialne kontrdowody semantyczne |
| Manifesty | RUN3 192 wpisy, RUN4 351; wyjątki j.w.; closure 49/49 | Kontrola integralności w podanym zakresie |

Pełna lektura objęła przekazane dwa podsumowania, ERRATA_R2, raporty nośne RUN3/RUN4, ROUND_REPORT, tabelę klasyfikacji, Z4 oraz istotne fragmenty QC i skrypty predykatów. Dekompilacje czytałem celowo wokół kwestionowanych krawędzi. Macierz źródeł zewnętrznych oceniałem jako dostarczony materiał i pod kątem przenoszenia wniosków; **nie powtórzyłem w tej rundzie 24 internetowych weryfikacji**. Nie deklaruję przeczytania wszystkich 207501 dodanych linii, ponownego uruchomienia Ghidry ani pełnej kontroli każdego callera. Stare testy viewerów S8–S11 nie były ponawiane: obecny diff jest badawczy i nie zmienia ich kodu.

Kontrola własnych narzędzi: pierwsza ogólna interpretacja manifestu potraktowała komentarze/odwołania jako ścieżki; poprawiona po lekturze całego manifestu, bez przypisania tych pozornych braków projektowi. Jedno wykonanie pomocnicze zatrzymało się na Git ownership przed badaniem bajtów; finalny run użył lokalnego dla komendy `safe.directory`, bez zmiany konfiguracji. Końcowy run zakończył się exit 0. Oryginały i historyczne pakiety były tylko czytane.

## Poprawiony checkpoint i dalsza praca

Mamy potwierdzony katalog modeli i kolizji, kod tworzenia zasobów, konkretne odczyty atrybutów i settery transformacji oraz kilka ścieżek ich uruchamiania. **Nie mamy jeszcze dowiedzionego ciągłego łańcucha instancji statycznego budynku ani jego historycznych XYZ. Nie wykluczono lokalnego zapisu placementu.**

Następna runda powinna najpierw naprawić F1–F5 w oddzielnej erracie i odtworzyć typy odbiorców getterów. Następnie śledzić jeden rzeczywisty szew: pochodzenie kontenera atrybutów oraz ogólną drogę derived-record/model-instance. Dekod jednej uzasadnionej rodziny VFS ma sens po wskazaniu jej czytnika i konsumenta; masowe szukanie czterobajtowych kotwic nie może go zastąpić.

Gotowy kontrakt: `PROMPT_OPENCODE.txt`. Zachowuje oryginały, obce `experiments/`, erę EU935 i wymóg publikacji wyników w GitHub. Nie uruchamia automatycznie klienta, mock-serwera ani nowego etapu renderera.
