# Audyt faz A/B — EU 9.3.5, 78cd153

RUN_ID: `PE_935_ORIGIN_SEAM_DESKTOP_AUDIT_R1_20260913`

Audytowany zakres: `24d7669 → 5d0edde → 78cd1535e6a35330bde7460c24e98db272acdbd3`.
Data: 2026-09-13. Audytor: Codex/Desktop. Host: WinDev2407Eval.

**Werdykt: faza A — potwierdzone najważniejsze korekty poprzedniego audytu; faza B — PARTIAL_PASS, wymaga korekty opisu formatu i pochodzenia końcowej pozycji. Nie potwierdzam „mechanizmu zamkniętego co do bajtu”.**

Wynik fazy B nie jest bezwartościowy: rozpoznano konkretne klasy wartości mapy, klucz instancji oraz ścieżkę od odczytu pozycji do tworzenia obiektu. Błędne są jednak opis operacji poprzedzającej odczyt pozycji i uproszczenie późniejszego przetwarzania jej trzeciej składowej. Lokalizacja historyczna 296445 nadal nie została odzyskana. Nie rozstrzygnięto, czy budynki używają tego samego kanału.

## 1. Znaleziska wymagające korekty

### F1 — P1: FUN_007343E0 odczytuje strukturę z maską, nie tworzy subkursora

Dotyczy fazy B: `06_REPORT/REPORT.md` §1, S6 i §5c; `ERRATA_R4.md` SE-R4-5/6; `QC_REPORT.md` §1c; `HANDOFF.md` i QC-3 w CSV. Ich zgodność nie stanowi niezależnego potwierdzenia semantyki.

**Własny dowód z oryginalnego EXE:**

- `007343E0`: `PUSH EBX; PUSH ESI; MOV ESI,[ESP+0xC]` — ESI otrzymuje pierwszy argument, kursor wejściowy.
- `00734416`: `MOV EDI,[ESP+0x14]` — drugi argument jest buforem docelowym.
- Caller przy `00745414`: `LEA EDX,[EDI+0xC]; PUSH EDX; PUSH EBP`, potem CALL przy `00745419` — bufor docelowy to **rec+0x0C**.
- Oba wyjścia: `0073459B` i `007345B4` zawierają `POP EDI; MOV EAX,ESI; POP ESI; POP EBX; RET`. Zwracany jest **ten sam kursor wejściowy**, a nie obiekt osadzony w rec+0x0C.
- Pierwszy u16 jest maską sterującą odczytem/podstawianiem floatów. Nie jest dowiedzioną długością podpakietu. Dalszy odczyt wariantu i pozycji kontynuuje ten sam strumień po danych tej struktury.

Układ zapisów pomocnika, offsety względem jego drugiego argumentu:

| Pole | Maska „wpisz 0” | Maska „wpisz 1” | Gdy żadna nie ustawiona |
|---|---:|---:|---|
| +0x00 | 0x002 | 0x004 | odczyt f32 |
| +0x08 | 0x008 | 0x010 | odczyt f32 |
| +0x0C | 0x020 | 0x040 | odczyt f32 |
| +0x10 | 0x080 | 0x100 | odczyt f32 |
| +0x14 | 0x200 | 0x400 | odczyt f32 |
| +0x18 / +0x1C / +0x20 | — | — | trzy odczyty f32 |

Użyty bit jest czyszczony; reszta maski trafia do u16 pod +0x24. Przy obu bitach pary ustawionych pierwszeństwo ma gałąź 0; bit gałęzi 1 zostaje w reszcie. Pole +0x04 nie jest zapisywane przez ten pomocnik. `FUN_007345C0` inicjuje szerszą strukturę zerami, ale to nie jest dowód, że osiem transmitowanych floatów ma semantykę macierzy 3×3.

**Własne kontrprzykłady arytmetyczne wyprowadzone z instrukcji:** maska 0 wymaga 34 bajtów, maski 0x2AA i 0x554 — po 14 bajtów; 0x7FE daje wartości 0 i resztę 0x554. Są to próby syntetyczne, a nie odtworzone pakiety historyczne ani wykonanie klienta.

**Skutek:** zachowuje się dowód odczytu pozycji do rec+0x38 i wariantu do rec+0x34, lecz opis gramatyki komunikatu jest błędny. Implementacja oparta na „subkursorze u16-header” może źle zużyć strumień lub całkiem pominąć strukturę. Nie wolno promować jej do gotowego dekodera.

**Naprawa:** nowa errata z pełnym kontraktem wejście/wyjście/zużycie kursora dla 007343E0, rozdzieleniem offsetów pamięci od offsetów w strumieniu oraz mapą konsumentów rec+0x0C. Nie nazywać pól skalą, prędkością, rotacją ani placementem bez konsumenta.

### F2 — P2: końcowa pozycja nie zawsze jest kopią pozycji komunikatu

Dotyczy fazy B: `REPORT.md` §1, S8/S9, tabela §4 i §5c; skrót PE-MASTER.

`FUN_004C46C0` robi lokalną kopię rekordu, a dla wariantów **3, 4, 5, 6, 7** przed konstruktorem wykonuje:

`h = f32(FUN_00853A80(manager, x, y, 0, 0))`

`z_local = max(z_input, h)` — ta postać równania dotyczy liczb skończonych; zachowanie NaN wymaga uwzględnienia flag x87.

Własne piny: źródłowa trzecia składowa `MOV ECX,[EAX+0x10]` przy `004C4706`; jej kopia `[ESP+0x18]` przy `004C4710`; CALL do 00853A80 przy **004C476E**; porównanie x87 i warunkowy `FSTP [ESP+0x18]` przy **004C4789**; dopiero potem CALL konstruktora przy **004C47C1**. Rekord callera nie jest nadpisywany — zmiana dotyczy kopii podanej konstruktorowi.

Kontrprzykład dla uproszczonego łańcucha: wariant 3, wejściowe z=10, wynik pomocnika=20 → konstruktor otrzymuje z=20; wariant 2 przy tych samych liczbach zachowuje 10. Obliczone w sondzie jako świadki arytmetyczne, bez uruchamiania klienta.

**Atrybucja:** executor już opisał tę gałąź w `02_ANALYSIS/SEAM_FLOW_MAP.md` §3. Znalezisko audytu polega na ujawnieniu pominięcia jej w końcowej syntezie i wniosku o pochodzeniu pozycji, a nie na przypisywaniu sobie pierwszego odkrycia funkcji.

Odczytałem także cały istniejący dekompilat 00853A80 i porównałem go z oryginalnymi bajtami. Funkcja używa testu przy manager+0x58, opcjonalnego obiektu **manager+0x4C** oraz wirtualnego dostawcy przez **manager+0**, slot +4. Nie ustaliłem klas tych dostawców. **To dobry trop korekty względem podłoża/wysokości, lecz „heightmapa” pozostaje hipotezą.**

**Naprawa:** pokazać oddzielnie pozycję odczytaną, przekazaną do f90, skorygowaną w kopii i zapisaną w instancji. Wyśledzić pochodzenie wyniku dostawcy. Dla EXISTING udokumentować osobne warunki aktualizacji; nie przenosić na tę gałąź automatycznie reguły CREATE.

### F3 — P2 w skrócie dla człowieka: nie wykazano wykluczenia statycznych budynków

W przekazanym werdykcie pada: **„Dla statyków (4508/296445): UNKNOWN — ten kanał ich nie obejmuje.”** To drugie zdanie jest mocniejsze od dowodu. Wersja repo w §6.3 jest poprawniej ograniczona: **„statyki (4508/296445) NIE wykazane w tym kanale”**.

Nazwa RTTI `MovableObject` opisuje klasę programu. Nie klasyfikuje automatycznie wszystkich danych, jakie mogą ją zasilić. Brak dowiedzionego połączenia z 4508/296445 nie dowodzi wykluczenia takiego połączenia. Analogicznie raw census E8 bez krawędzi z zakresu 0x0094xxxx nie rozstrzyga pośredniego przepływu danych z pliku.

**Naprawa:** we wszystkich aktualnych skrótach zachować „nie wykazano; użycie przez statyki nierozstrzygnięte”. Tabelę „Źródło insertów = komunikaty” ograniczyć do prześledzonej ścieżki procesora. Sześciu callerów creatora i lokalny generator kluczy nie mają przez samo sąsiedztwo tego samego źródła danych.

## 2. Drobniejsze korekty i granice

- **P3, adres instrukcji:** raport/QC/errata podają 004C4875 jako CALL 0085B3E0. Własny odczyt: CALL pozycji to **004C488A**, warunek przed nim to CALL **004C4878 → 0085B750**, a rotacji **004C4896 → 0085ADB0**. 004C4875 należy do wcześniejszego pośredniego wywołania slotu +0x14.
- **P3, liczebność tabeli:** zakres 0xA2..0xC7 obejmuje **38** indeksów; `CMP ...,0x25` oznacza maksymalny indeks 37, nie 37 wpisów. Tabela skoków ma osobno 22 pozycje.
- **P3, aktualne bramki:** GB4 w CSV zachował stare rec+0x50..0x58/„wariant +0x5C”, podczas gdy dodany QC-3 koryguje je do rec+0x38/+0x34. Istnieje errata, więc nie traktuję historycznych opisów jako nowych odkryć. Jednak §9 finalnego REPORT twierdzący, że „wiersz CSV był poprawny”, wymaga sprostowania. W nowej rundzie opublikować jedną tabelę obowiązujących bramek z mapą supersession, zachowując stary pakiet bez zmian.
- Faza A pozostawia drobne nazewnictwo typu „rb-find” dla 00971780 oraz „transform 296445 (D=124.941)”. Finalna wiedza: hash-map oraz liczba o nieustalonej semantyce. Nie odzyskany transform.

## 3. Co potwierdziłem samodzielnie

| Twierdzenie | Moja kontrola | Wynik |
|---|---|---|
| Właściwa era EXE i templates.vfs | pełne SHA256 obu oryginałów; PE32 i image base | zgodne z raportami |
| 54 rejestracje + 1 korzeń | własny skan E8 do 0070CF80, sprawdzenie PUSH imm32 na 54 podanych miejscach | 55 / 54; bazowe wywołanie zachowane osobno |
| Powiązanie klas z numerami | vtable→COL→TD z oryginału, mechaniczne A..P i porównanie z immediate | 36/36; m.in. Common=20006, Surgeon=20035 |
| Typy mapy i executora | własne odczyty łańcuchów RTTI | MovableObject, ClientMovableObject, ArkClientPacketExecutor |
| Getter +8 i +0x10 | własne raw E8/E9 przez .text | 808+9 oraz 116+1; sama wspólna funkcja nadal nie typuje odbiorcy |
| Cztery ścieżki procesora | własne E8 + odczyt tablic dispatchera | B0/C6/C7 oraz special-case B2; B9 ma inny handler |
| Insert | własny raw census | 1 CALL przy 004C47DA; do creatora 6; producent kluczy 8 |
| Piny T6 | porównanie wszystkich wydrukowanych bajtów z oryginałem | 64/64, 1552 bajty kontekstów, 0 rozbieżności |
| templates.vfs | własny walk i CRC32 każdego payloadu, bez importowania parsera executora | 5438 rekordów, 0 błędów CRC, dokładne EOF 560788 |
| Template 4508 | własny odczyt | A=296445; D=0x42F9E1CB=124.94100189208984, UNKNOWN |
| Manifesty publikacji A/B | ponowne SHA256 i rozmiary | 129/129 oraz 210/210 wierszy plikowych |
| Historyczne 8 pakietów lokalnych | własne listy plików i ponowne SHA256, zgodność saved-before/saved-after/teraz | **1385/1385**, 0 różnic |
| Commit/publikacja | Git lokalny i ls-remote | 5d0edde:132 ścieżki;78cd153:212; każdy entrypoint +1/−0; przed publikacją audytu HEAD=remote=78cd153 |

Oba commity razem: **343 zmienione ścieżki, +81 823 linie**. Poza dwoma nowymi pakietami zmienił się tylko AUDIT_ENTRYPOINT.md. Repo przed audytem: tylko obce `?? experiments/`.

Pełne dane, adresy, hashe i wyniki: `probe.json`; narzędzie: `probe.mjs` + `pe.mjs`; własne hexdumpy: `independent_hexdumps.txt`. Wywołanie: `node probe.mjs` z dostępem do wskazanych oryginałów i audytowanego checkoutu. Sonda celowo wymaga HEAD 78cd153; po publikacji uruchamiać ją na osobnym checkoutcie tego commita albo świadomie dostosować kontrolę snapshotu, bez resetowania aktywnego repo.

## 4. Granice niezależności i wykonania

To audyt aktualnych twierdzeń, kluczowych funkcji i integralności pakietów, **nie deklaracja przeczytania 81 tysięcy linii ani wszystkich 343 plików**. Przeczytałem końcowe raporty A/B, aktualne korekty i bramki nośne, macierze śladu oraz dekompilaty potrzebne do oceny insertu/deserializacji/ctorów i dostawcy 00853A80. Nowe sprawdzenie 007343E0 pochodzi z fizycznego EXE, nie z przejętej nazwy Ghidry.

Nie uruchamiałem Entropia.exe, Ghidry, serwera, mocka ani renderera; nie powtarzałem S8–S11B/WebGL. Nie wykonałem pełnego trace’u sub-obiektu +0xC0 ani producenta bufora. Nie odtwarzałem całej analizy dataflow wszystkich 15 setter-callerów i 19 pozostałych funkcji; poprawa zakresu F5 jest prawidłowa, a ich semantyka nadal wymaga dalszego badania. Liczebności raw E8/E9 nie zastępują niezależnego rozpoznania granic wszystkich instrukcji.

Historyczne hashe dowodzą równości do zachowanych snapshotów, nie wykluczają chwilowych zmian między pomiarami. Daty/counts 194/195 w starym QC odnoszą się do etapu QC; manifest finalny obejmuje późniejsze pliki. Nie traktuję tego samoistnie jako uszkodzenia pakietu.

Self-check audytora: próby przygotowawcze zatrzymały się na kilku ręcznie przepisanych adresach instrukcji przesuniętych o bajt; wszystkie skorygowano odczytem oryginału i rel32, zanim sonda zakończyła się PASS. Poprawiono też pomyloną lokalizację jednego pliku evidence. Nieudane próby nie wygenerowały końcowego raportu PASS.

## 5. Najbardziej użyteczny następny krok

**Najpierw poprawić kontrakt 007343E0 i opisać rzeczywistą konstrukcję pozycji. Następnie rozpoznać dostawcę 00853A80 i jego związek z danymi terenu, zachowując osobne pytanie o model tej samej instancji.** To ma większą wartość dla obecnego celu niż nieograniczone zejście w ogólną obsługę sieci przed ustaleniem, czy badana gałąź obejmuje budynki.

Trzy różne pytania muszą pozostać oddzielne: co kod potrafi utworzyć; skąd dostaje dane; gdzie konkretnie stał budynek w 2008 roku. Ustalenie dwóch pierwszych nie odtwarza automatycznie historycznych współrzędnych.

Gotowy kontrakt dalszej pracy: `PROMPT_OPENCODE.txt`. Obejmuje korekty, bounded trace dostawcy i powiązania instancja→model, testy rozróżniające oraz obowiązkowy commit/push każdego zakończonego pakietu.
