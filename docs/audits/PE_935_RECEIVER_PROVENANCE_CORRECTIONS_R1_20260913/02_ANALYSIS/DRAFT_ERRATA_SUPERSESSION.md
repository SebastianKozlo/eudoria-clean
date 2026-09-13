# DRAFT_ERRATA_SUPERSESSION — materiał erraty + kwalifikacje SUPERSESSION

RUN: PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913 | ERA: EU 9.3.5 (pcg_install)
Binarium: Entropia.exe SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
Status dokumentu: **DRAFT dla pe-master-auditor** (formalizacja erraty i publikacja po stronie auditora).
Historicznych plików NIE modyfikowano (GA5: census composite-hash przed/po — identyczny).

Format każdego wpisu: (i) CYTAT zastępowany (verbatim + plik:linia); (ii) NOWA TREŚĆ (kanoniczna);
(iii) podstawa bajtowa NOWEJ treści (własny odczyt tego runu, artefakt).

---

## CZĘŚĆ A — F3: negatywy bajtowe nie wykluczają plikowego placementu

### [SE-1] „pliku-placementów brak" → ANCHORS_ABSENT_SEMANTICS_OPEN

- CYTAT (ROUND_REPORT.md:48, pakiet PE_935_STATIC_PLACEMENT_ROUND1_20260913):
  > „Kanał FILE: infrastruktura istnieje (store "Data\Parameters" FUN_0094dfc0/FUN_0094fe00 + parsery VFS), ale **pliku-placementów brak** (Portals.bnt/.prt = czysty dPVS cell-graph — 276/276, 0 duplikatów, 0 anchorów na WSZYSTKICH offsetach per QC; 20006.vfs nie istnieje mimo dokładnie 29 imm32 0x4E26 w .text)."
- CYTAT (RUN4 REPORT.md:30, pakiet PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913):
  > „brak lokalnego pliku-placementów statyków (Portals.bnt/.prt — patrz pkt 3: czysty cell-graph dPVS; census Data\Parameters: 27 plików .vfs parametrów, **20006.vfs nie istnieje** mimo 29 użyc ID 20006 w .text; 20xxx.vfs nie rozstrzygnięte jako nośnik transformów statyków — szew parser→drzewo nie domknięty)."
- CYTAT (RUN4 QC_REPORT.md:64):
  > „**Brak pliku-placementów udowodniony** na powierzchni censused: Parameters zawiera wyłącznie .vfs parametrów (żaden nie jest plikiem placementów statyków — rozstrzygnięcie H1 pozostaje „bez pozytywu", uczciwie)..."
- NOWA TREŚĆ:
  Negatyw bajtowy ma zakres dokładnie zadeklarowany: w przebadanych nośnikach (276 payloadów .prt;
  27 plików .vfs w Data\Parameters; brak pliku 20006.vfs) **nie znaleziono 13 wskazanych kotwic LE32 na
  żadnym offsecie**. Wynik: **ANCHORS_ABSENT_SEMANTICS_OPEN** — brak kotwic o zadeklarowanym zakresie
  NIE wyklucza: (a) kodowań pochodnych (schemat/indeksy/nazwy/pola innej szerokości/kompresja/wyliczanie),
  (b) pełnej gramatyki żadnego z 27 plików .vfs (20xxx.vfs NIE zdekodowane formatowo — jawne od RUN4),
  (c) łańcucha konsumentów tych plików (szew parser→insert-map nadal otwarty — niniejszy run dodatkowo
  udokumentował, że wartość mapy managera parametrów [hit+8] pozostaje RECEIVER_UNRESOLVED, patrz
  RECEIVER_MATRIX.md §4). **„27 plików" ≠ „27 rodzin formatu"** — count plików nie jest censusem
  gramatyk.
- PODSTAWA: własny walk templates.vfs 5,438/5,438 (F2_T4508_WALK.json); odczyt RUN4 S12 (metoda:
  payload.find po wszystkich offsetach — zweryfikowana w s12_prt_content_check.py:63); RECEIVER_MATRIX.md §4
  (eliminacje + granica insert-map).

### [SE-2] anomalia 20006/0x4E26 — co brak pliku dowodzi, a czego nie

- CYTAT (ROUND_REPORT.md:48, cd.): „20006.vfs nie istnieje mimo dokładnie 29 imm32 0x4E26 w .text".
- NOWA TREŚĆ:
  Brak pliku 20006.vfs **nie dowodzi** (i nie wyklucza): źródła sieciowego param-setu 20006, tożsamości
  „nazwa pliku = ID param-setu", ani tego, że wartości 20006 pochodzą z kanału runtime. Co niniejszy run
  DODAŁ merytorycznie: **0x4E26 (20006) jest numerycznym ID KLASY ArkObjectClassImpl** — rejestracja
  @0x0073B87D (funkcja 0x0073B820) woła ctor ArkObjectClass z imm32 0x4E26 (census 55 rejestracji klas,
  F1_REG_ARGS.json), dokładnie tak samo jak 20035 dla ArkSurgeonObject (RTTI $0EOED@=0x4E43) i 20030
  dla ArkParameterContainer (RTTI $0EODO@=0x4E3E). Rodzina ID 20xxx/24xxx w .text to **identyfikatory
  klas/param-setów rejestrowane w kodzie** — ich pliki VFS są jednym z możliwych nośników zasilania,
  a nie samymi definicjami klas. Granica (kto ZASILA klasę 20006 danymi): pozostaje otwarta.
- PODSTAWA: F1_REG_ARGS.json (pełna lista 55 ID); F1_ABI_BYTES.json (ctor store [class+8]=EBP);
  F1_CTX_WRITER_DAT00BA58CC.txt (wzorzec lazy-init klasy); RTTI decode (F1_RECEIVERS.json, F1_DERIVED.json).

### [SE-3] RUN2 D3 — „w OBU ekosystemach client-side" wymagało pozytywu dla WAR

- CYTAT (ROUND_REPORT.md:99):
  > „DoL/WarEmu create-object (D1/D2a/D3) | **CONFIRMED z kodu** | F_CREATE_STATIC=0x71 (WarEmu, verbatim) i create-family DoL tworzą INTERAKTYWNE encje serwerowe (drzwi/questy/loot; GameObject:Unit z rodzeństwem Door/Item/PQuestObject/...); **w OBU ekosystemach statyczne miasta są CLIENT-SIDE (DAoC: fixtures.csv)**."
- NOWA TREŚĆ:
  Macierz D3 (CLAIMS_MATRIX.md:34, RUN2) mówi z kodu WarEmu: F_CREATE_STATIC tworzy **interaktywne
  obiekty DB-driven** (drzwi/loot/questy) i **„nie pokazuje żadnej ścieżki komponowania/transmitowania
  statycznej geometrii miasta"**. To jest NEGATYW (brak dowodu ścieżki serwerowej) — **nie dodatni dowód
  client-side dla WAR**. Pozytywny dowód client-side istnieje TYLKO dla DAoC (fixtures.csv — wiersze B1–B6).
  Poprawne zdanie: „w DAoC statyczne miasta są client-side (fixtures.csv — CONFIRMED z kodu); dla WAR
  kod WarEmu nie pokazuje serwerowej ścieżki statycznych miast (NEGATYW) — twierdzenie o client-side
  w OBU grach wymagało dodatniego dowodu dla WAR, którego macierz nie dostarcza. Nie przenosić tego
  wniosku na EU935."
- PODSTAWA: odczyt CLAIMS_MATRIX.md D3 (RUN2, verbatim — nie modyfikowano); ROUND_REPORT §3 (cytowane).
  (Ta poprawka jest narracyjna — materiał źródłowy RUN2 jest poprawny; błąd powstał w agregacji ROUND.)

---

## CZĘŚĆ B — F4: 0/38 STATIC_WORLD nie wyklucza użycia funkcji przez budynki

### [SE-4] „statyki NIE przechodzą przez te call-site'y"

- CYTAT (ROUND_REPORT.md:44): „**0/38 STATIC_WORLD** — tylko avatar/UI/maszyna/vegetation (RUN3); **statyki NIE przechodzą przez te call-site'y**."
- CYTAT (RUN3 REPORT.md:46): „Ważny wynik negatywny: **NO_STATIC_CONSUMER_FOUND** na censurowanej powierzchni 25 lookupów + 13 pumpów (pkt 2) — **statyczne budynki NIE przechodzą przez żaden z tych call-site'ów w sposób placement-driven**; redirect na system ArkObject + atrybuty + CWO."
- CYTAT (Z2_CLASSIFICATION_TABLE.md:62, RUN3): „4. Redirect: jeżeli statyki ładują modele, to NIE przez te 38 call-site'ów — kandydatem jest system ArkObject (ctor pobiera A z obiektu template → +0x28) + podsystem wizualny 0x006Cxxxx (FUN_006cd850/cd820/cdd80) + system atrybutów (Z4)."
- NOWA TREŚĆ:
  Prawdziwy zakres negatywu: **na censurowanej powierzchni 25 lookupów + 13 pumpów nie zidentyfikowano
  żadnego call-site'u z DOWIEDZIĄ DEDYKOWANEJ KLASY STATIC_WORLD** (0/38). Klasyfikacja dzieli funkcje
  wg ROLI funkcji (AVATAR_EQUIPMENT / MODEL_MACHINERY / OTHER / UNKNOWN...), **a nie wg dowiedzionej klasy
  obiektów wejściowych** — klasyfikacja MODEL_MACHINERY/OTHER nie jest wykluczeniem, że statyki używają
  tych samych wspólnych funkcji (cross-role-function). W szczególności (zgodnie z tabelą Z2 i RUN4):
  - `FUN_00567170` (Z2 #10: OTHER — rejestracja derived-record z transformem; „mechanizm WYSOKA,
    czy obsługuje statyki — NIEROZSTRZYGNIĘTE"),
  - `FUN_005B5F90` (Z2 #20: OTHER — „WYSOKA (mechanizm), NISKA (rola)"),
  - `FUN_006CB6F0` (pump #4 — MODEL_MACHINERY, **twórca instancji modelu**),
  pozostają **wspólnymi kandydatami przez-role-funkcji vs klasa-danych** — ich użycie przez statyki
  jest nierozstrzygnięte, nie wykluczone. Dodatkowo niniejszy run pokazał, że nawias w Z2:62 „(ctor
  pobiera A z obiektu template → +0x28)" jest błędny (patrz SE-7): ctor kopiuje **[class+8] =
  numeryczne ID klasy**, nie A rekordu.
- PODSTAWA: Z2_CLASSIFICATION_TABLE.md (odczyt); RECEIVER_MATRIX.md wiersz 3 (F1 — poprawka roli +0x28);
  census RUN3 (0/38 potwierdzony przez QC A4 — bez zmian negatywu).

---

## CZĘŚĆ C — F5: „WYŁĄCZNIE z drzewa atrybutów"

### [SE-5] kwantyfikator „WYŁĄCZNIE"

- CYTAT (ROUND_REPORT.md:31-32): „instancja statyczna = rekord placementu z transformami czytanymi **WYŁĄCZNIE z drzewa atrybutów** + instancja modelu przez resource-system + system CWO/ArkObject; templates-lookup NIE jest ścieżką statyków (0/38 — tylko avatar/UI)."
- CYTAT (RUN4 REPORT.md:18-20): „1. **Transform wchodzi do rekordu placementu WYŁĄZNIE z drzewa atrybutów encji** (FUN_00846840: switch atrybutów 0x6A4/0x6A5/0x6A8/0x6A9; + FUN_00854720 trójka +0x68/+0x6c/+0x70...)."
- CYTAT (RUN4 QC_REPORT.md:27, B2): „**„Transformacje czytane WYŁĄCZNIE z drzewa atrybutów"** + alternatywne ścieżki zapisu pól +0x08/+0x14 — PASS (z nuansem NOT_CHECKED, bez kontrprzykładu)".
- NOWA TREŚĆ:
  Test qc_b2_exclusive.py jest **censusem wywołań w przybliżonych ciałach funkcji** (granica = heurystyka
  3×CC), NIE śledzeniem provenance argumentów. Jego wynik uprawnia wyłącznie do zdania: **„we wszystkich
  prześledzonych ścieżkach builder→getter atrybutów→setter (statycznie, w zasięgu testu) transformy
  pochodzą z systemu atrybutów"**. Kwantyfikator „WYŁĄCZNIE" (globalny) wymagałby: (a) rozliczenia
  provenance argumentu dla KAŻDEGO setter-callera z definicją, odbiorcą, gałęzią i upstreamem,
  (b) negatywu pełnego dla ścieżek pozadatawych — żaden z tych dowodów nie istnieje. Skrypt używa
  heurystyki granicy (3 bajty CC), do grupy ATTR wlicza writer FUN_00845F70 — jego wynik jest listą
  wywołań, nie walidatorem wyłączności. Źródło WARTOŚCI w drzewie atrybutów (plik/sieć/mieszane/
  wyliczane) pozostaje UNKNOWN (H1/H2/H3/H4 bez zmian).
- PODSTAWA: odczyt qc_b2_exclusive.py (heurystyka body_of: linia 45-52 — pętla do 3×CC);
  qc_b2_exclusive ATTR_FUNCS zawiera 0x00845F70 (writer); kontrprzykład logiczny Desktop (getter-ignorujący
  ciąg instrukcji) — poprawny wobec PREDYKATU, bez wnioskowania o EU935; census własny F5_SETTER_ACCOUNTING.json.

### [SE-6] rozliczenie 15 setter-callerów („10 bezpośrednich + 4 parametrowe" nie domyka)

- CYTAT (RUN4 QC_REPORT.md:27, B2): „Zbadawszy napędy wszystkich 15 funkcji setter-callers: **10 woła funkcje systemu atrybutów bezpośrednio** (walker FUN_0085b840 / FUN_00843d60 / resolver FUN_008544d0 / check FUN_00844020), a 4 bez bezpośrednich odczytów (FUN_005b5f90, FUN_00459270, FUN_0043a200, FUN_00488920) przyjmuje wartości z parametrów..."
- NOWA TREŚĆ (pełne rozliczenie 15 — census Ghidra + klasyfikacja bajtowa):
  15 call-site'ów settera pozycji FUN_00730f90 w 15 funkcjach (atrybucja Ghidra isCall; GhIDRA_FUNC_ATTR.json):
  FUN_0050bed0, FUN_00457cd0, FUN_00459270, FUN_00442190, FUN_00447630, FUN_004b3a00, FUN_0043a200,
  FUN_004c47f0, FUN_0046e790, FUN_00488920, FUN_0067bc90, FUN_0067ccd0, FUN_00567170, FUN_005b5f90,
  FUN_00567770.
  | grupa | funkcje | status provenance |
  |---|---|---|
  | bezpośrednie odczyty atrybutowe (10) | FUN_0050bed0, FUN_00457cd0, FUN_00442190, FUN_00447630, FUN_004b3a00, FUN_004c47f0, FUN_00567170, FUN_00567770, FUN_0067bc90, FUN_0067ccd0 | atrybutowe (kwalifikacja RUN4 podtrzymana) |
  | parametryczne (4) | FUN_005b5f90, FUN_00459270, FUN_0043a200, FUN_00488920 | wartości z parametrów (RUN4); dalszy ślad śledzony tylko dla FUN_005b5f90 (QC B2) — pozostałe 3: provenance parametrów NIEROZLICZONE |
  | **15. funkcja — NIEROZLICZONA w QC (SE-6)** | **FUN_0046e790** | **NO_DIRECT_ATTR_CALLS** — brak wywołań funkcji atrybutowych w ciele; **woła singleton managera parametrów FUN_004154F0** (mapa DAT_00BA12E8); settery f60/f90/fb0; provenance wartości setterów = NIEROZLICZONA (kandydat: mapa parametrów przez singleton — szew jak w RECEIVER_MATRIX §4) |
- PODSTAWA: GHIDRA_FUNC_ATTR.json (f90 sites = 15, isCall); F5_SETTER_ACCOUNTING.json (klasyfikacja
  attr/singleton/settery per funkcja, starty SEH-anchored dla 4 funkcji, w których heurystyka CC myli
  granice: FUN_00447630, FUN_004c47f0, FUN_0046e790, FUN_00567770).

### [SE-7] (poprzedni most RUN3 — cytaty do zastąpienia razem z F1)

- CYTAT (RUN3 REPORT.md:13-15): „**Encja**: `ArkObject` (ctor `FUN_00726e70` @0x00726E70) przyjmuje **obiekt template'u** i getterem A (`FUN_007ce1e0` = `[ECX+0x08]`, adres-zablokowany w poprzednim runu) zapisuje **A (id pliku .nif) do encji @+0x28**."
- CYTAT (RUN3 REPORT.md:16): „Istnieje 40 call-site'ów ctora — fabryki per klasa (np. ctor `ArkSurgeonObject` `FUN_007351e0` z globalnym template'em `DAT_00ba58cc`)."
- CYTAT (RUN3 REPORT.md:18): „**To jest most template→encja statycznej**: definicja (template) jest osobna od instancji (ArkObject)..."
- NOWA TREŚĆ:
  Ctor ArkObject NIE przyjmuje rekordu template'u. Fabryka (slot1 vtable 0x00A86850 = FUN_0070BF50,
  0 bezpośrednich callerów — wyłącznie dispatch wirtualny) przekazuje jako PIERWSZY argument ctora
  **własny this = instancję ArkObjectClass**; ctor czyta getterem **[class+8]** i zapisuje wynik do
  **encji@+0x28**. **[class+8] = numeryczne ID klasy** (param-set; ustawiane imm32 w 55 funkcjach
  rejestracyjnych: 0x4E20..0x4E4B + rodzina 0x5DCx; store w ctorze `MOV [ESI+8],EBP` @0x0070CFC1),
  NIE pole A rekordu templates.vfs. Weryfikacja podwójna RTTI: mangled names klas kodują te same ID
  (ArkObjectClassImpl<ArkSurgeonObject,$0EOED@> = 0x4E43 = 20035; ArkObjectClassImpl<ArkParameterContainer,
  $0EODO@> = 0x4E3E = 20030). „Globalny template DAT_00ba58cc" = **singleton klasy
  ArkObjectClassImpl<ArkSurgeonObject, 20035>** (writer FUN_0073D810: new(0x118)→ctor→store@0x0073D882→
  rejestracje), nie rekord template'u. **Nie istnieje „most templates.vfs.A → ArkObject+0x28"**;
  istnieje most „class-ID → encja@+0x28" (kopia identyfikatora klasy do instancji). Ilościowo: ctor
  ArkObjectClass ma **55** bezpośrednich call-site'ów (Ghidra isCall; „40" w RUN3 = niedoliczenie),
  ctor ArkObject **55**, fabryka 0 (wirtualna).
- PODSTAWA: F1_ABI_BYTES.json (każde ogniwo z VA+bajtami); F1_CENSUS.json; F1_REG_ARGS.json;
  GHIDRA_REFCOUNTS.json; F1_CTX_WRITER_DAT00BA58CC.txt; F1_DERIVED.json (RTTI);
  RECEIVER_MATRIX.md wiersze 2-3.

### [SE-8] „11/26 callerów ctora bez setterów" — jawna lista NOT_CHECKED

- CYTAT (RUN4 QC_REPORT.md:28, B2): „ctor rekordu FUN_00730700 (init 12 dwordów +0x00..+0x2C, FLDZ→+0x10) ma **26 call-site'ów** (nie tylko builder): 11 z nich nie woła setterów — semantyka tych rekordów (czy to też „placement records" z innym zasilaniem) nie była badana w runie i nie jest rozstrzygnięta w moim QC (pozostaje NOT_CHECKED...)."
- NOWA TREŚĆ (jawnie, atrybucja Ghidra):
  Ctor FUN_00730700 ma **26 call-site'ów w 24 funkcjach** (isCall; dwie funkcje po 2 site'y: FUN_00447630,
  FUN_0050e490). Funkcje wołające settery (5): FUN_00447630, FUN_00459270, FUN_00567770, FUN_0067bc90,
  FUN_0067ccd0. **Funkcje BEZ wywołań setterów (f60/f90/fb0/fd0) = 19 (NOT_CHECKED, lista VA
  call-site'ów ctora)**: FUN_00456770 @0x004567BC, FUN_00457c00 @0x00457C2A, FUN_00457e30 @0x00457E76,
  FUN_0046aa90 @0x0046AAE3, FUN_004b9960 @0x004B9A7D, FUN_004c5bd0 @0x004C5BFB, FUN_004e3b70 @0x004E3C60,
  FUN_004ff620 @0x004FF93C, FUN_0050baf0 @0x0050BB1C, FUN_0050c0c0 @0x0050C147, FUN_0050cc70 @0x0050D1FC,
  FUN_0050d480 @0x0050D730, FUN_0050e490 @0x0050F098+0x0050F5C8, FUN_0050fcf0 @0x0050FD39,
  FUN_005106a0 @0x005106D1, FUN_00511070 @0x005110DA, FUN_006c8000 @0x006C8065, FUN_006c80c0 @0x006C812D,
  FUN_0072fa30 @0x0072FB8E. Liczba „11" z QC nie jest reprodukowalna pod atrybucją Ghidra (była
  zależna od heurystycznych granic ciał); wiążąca jest lista 19 funkcji / 20 site'ów powyżej —
  **semantyka tych rekordów pozostaje NOT_CHECKED** (zgodnie z brzmieniem QC).
- PODSTAWA: GHIDRA_FUNC_ATTR.json (26 sites, atrybucja); F5_SETTER_ACCOUNTING.json
  (setter-usage per funkcja, starty SEH-anchored).

---

## CZĘŚĆ D — F2: twierdzenia „konsument D"

### [SE-9] selektor wariantów w FUN_008553D0 czyta +8 odbiorcy, nie D@+0x10

- CYTAT (Z4_field_d.md:31-32, RUN4): „FUN_008553d0 (konstruktor-walker: `fStack_50 = (float)FUN_0048ada0()`; **w gałęzi 0x4e38 odczyt D steruje mapowaniem local_60: 4/5→2, 6→3, 7→4!**)"
- CYTAT (Z4_field_d.md:47-49): „FUN_008553d0: D steruje **wyborem wariantu konstrukcji** (mapowanie 4/5→2, 6→3, 7→4 w gałęzi param-setu 0x4e38) i trafia do FUN_00415570/FUN_008599a0 jako jeden z argumentów inicjalizacji obiektu."
- CYTAT (RUN4 REPORT.md:123-124): „FUN_008553d0 (konstruktor-walker): D steruje selekcją wariantu (gałąź 0x4e38: D=4/5→2, 6→3, 7→4) i trafia do inicjalizacji obiektu;"
- CYTAT (RUN4 QC_REPORT.md:85, B10): „gałąź param-setu: `CMP EAX,0x4E38` @0x008557DB → selekcja wariantu przez `LEA EAX,[ESI-4]; CMP EAX,3; JMP [EAX*4+0x00855BB4]` (tablica indeksowana D−4; widoczne w bajtach: slot 6→3, 7→4) ✓ — zgodne z claimem „D=4/5→2, 6→3, 7→4"."
- NOWA TREŚĆ:
  ARYTMETYKA mapowania jest prawdziwa (tabela 0x00855BB4: [0]=0x00855834, [1]=0x00855834,
  [2]=0x00855820, [3]=0x0085582A; bloki: [ESP+0x1C]=2 / =2 / =3 / =4), ale **ŹRÓDŁO selektora jest
  błędne**: w gałęzi 0x4E38 (`CMP EAX,0x4E38` @0x008557DD) selektor czyta **wynik CALL FUN_007CE1E0
  (+8)** @0x008557FD, z odbiorcą ECX=[wynik walker-current FUN_0085B860] @0x008557F6 — czyli
  **+8 wartości mapy managera parametrów**, a NIE D@+0x10 template'u (getter D FUN_0048ADA0 @0x008556DF
  leży w INNEJ gałęzi tego samego switcha i czyta +0x10 tego samego typu odbiorcy). Dekompilat
  ZS1_PSEUDO_008553D0.txt (RUN4, linie 203-216) już pokazuje `uVar13 = FUN_007ce1e0(); switch(uVar13)`
  — claim Z4 §2-3 był sprzeczny z własnym artefaktem runu. Odbiorca: wartość [hit+8] mapy mgr+0x10
  (singleton DAT_00BA12E8; resolver FUN_008544D0; layout +0=vtable/+4=nullable lock/+8=small int) —
  **nazwa klasy RECEIVER_UNRESOLVED** (RECEIVER_MATRIX.md §4 z granicą).
- PODSTAWA: F2_CTX_BRANCH_008557C0.txt (pełne bajty gałęzi); F2_SELECTOR.json (tabela skoków);
  F2_CALLMAP.json (mapa wywołań — getterD @0x008556DF to inna gałąź); RECEIVER_MATRIX.md §2 wiersz 4.

### [SE-10] queue-push FUN_00567B40 — pole i odbiorca

- CYTAT (Z4_field_d.md:29-30): „**FUN_00567c50 ×2** (0x005681BD-region: `uVar6 = FUN_0048ada0()` przed FUN_00567b40 — **D przekazywane do capacity-push!**) i FUN_0058db50;"
- CYTAT (Z4_field_d.md:44-46): „FUN_00567c50: `uVar6 = FUN_0048ada0()` (D bieżącego rekordu) → FUN_00567b40 (push do kolejki update z capacity [obj+0x40..0x60] — **D wpływa na priorytet/flagę wpisu kolejki**, bo ten sam obiekt czyta też pola +0x48/+0x50/0x54/0x58/0x5c/0x60)."
- NOWA TREŚĆ:
  Struktura potwierdzona bajtowo: FUN_00567C50 woła getter D ×2 przed pushami (@0x00567D16 → push
  @0x00567D24; @0x00567D46 → push @0x00567D54) i wynik jest 3. argumentem FUN_00567B40. Ale:
  (a) odbiorca getterów D = **[arg1+0x10]**, gdzie arg1 = pierwszy argument stosowy FUN_00567C50
  (`MOV ESI,[ESP+0xEC]` @0x00567C93; `MOV ECX,ESI` przed CALL) — to NIE jest dowiedziony rekord
  templates.vfs (provenance per-caller: FUN_0058db50 → stan world-object; FUN_005b72c0 → bufor
  komunikatu 0xB9; FUN_00514ef0 → argument handlera; **RECEIVER_UNRESOLVED per caller**);
  (b) trzeci call gettera D @0x00567F72 ma odbiorcę **this FUN_00567C50** ([ESP+0x20] = EDI);
  (c) sama funkcja queue-push FUN_00567B40 czyta **[singleton_00BA1260+8] przez getter A**
  (CALL FUN_004143F0 @0x00567B49 → MOV ECX,EAX → CALL FUN_007CE1E0 @0x00567B50) i porównuje z
  FUN_00844130(arg) — flaga równości (iVar2==iVar3 → 5. argument FUN_00567170). Zdanie „D wpływa na
  priorytet/flagę" należy zastąpić: „argument [arg1+0x10] trafia do kolejki update; flaga gate
  pochodzi z porównania [singleton+8] vs FUN_00844130(arg), nie z D template'u".
- PODSTAWA: F2_DCLAIMS.json (struktura call-site'ów); własny hexdump FUN_00567B40/00567C50
  (F2_SELECTOR.json notatki); ZS2_PSEUDO_00567B40.txt (RUN4, odczyt — zgodny: iVar2=FUN_007ce1e0()).

### [SE-11] pola D — klasyfikacja konsumentów (zamiast zbiorczej „semantyka D = parametr multi-konsumenta")

- CYTAT (Z4_field_d.md:51-56, §3): „**Granica (jawna)**: nie znaleziono JEDNEJ jednoznacznej semantyki — D jest parametrem MULTIPLE-consumer: (a) selektor wariantu (FUN_008553d0), (b) argument kolejki update (FUN_00567b40), (c) wartość distans/LOD (FUN_00861390). Dla template'u 4508 (D=124.941 ≈ 125): wielkość/promień/level — nie da się rozstrzygnąć statycznie bez runtime (etykieta: RUNTIME-UNOBSERVED dla konkretnej wartości 124.941; STATIC-PROOF dla konsumentów)."
- CYTAT (ROUND_REPORT.md:261): „| 5 | **Pole D (124.941 przy 4508)** | runtime (semantyka liczbowa: promień/level/selektor wariantu — statycznie nierozstrzygalne, G4 boundary) | gettery VA-locked; semantyka RUNTIME-UNOBSERVED |"
- NOWA TREŚĆ (per konsument, z odbiorcą):
  | claim konsumenta | status po tym runie | odbiorca / poprawka |
  |---|---|---|
  | (a) selektor wariantu 0x4E38 | **REJECTED_AS_ATTRIBUTED** (SE-9) | selektor = +8 wartości mapy parametrów (getter A), nie D@+0x10 |
  | (b) argument kolejki update | **PARTIAL** (SE-10) | [arg1+0x10] przekazywane do pusha — potwierdzone; ale odbiorca ≠ dowiedziony rekord template'u; flaga gate = [singleton+8] vs FUN_00844130 |
  | (c) distans/LOD FUN_00861390 | **CENSUS-CONFIRMED** | 2 site'y gettera D-f32 @0x00861B49/0x00861EEB w kontekście arytmetyki f32 (odbiór z [ESI+0x10]-family); pełny census D-f32: 10 callerów (zgodny z Z4 §2) |
  | FUN_00468910 ×5 | **UNDERCOUNT** | census Ghidra: **12** site'ów gettera D w FUN_00468910 (0x00468D88, 0x00468DA4, 0x004692BC, 0x004692D7, 0x004692F2, 0x0046930D, 0x004694BE, 0x004694D9, 0x004694F0, 0x00469A7D, 0x00469AF0, 0x00469B0D); spot-check 0x00468D88: odbiorca = **lokalny rekord na stosie** ([ESP+0x1C]+0x10) — dla rekordu placementu +0x10 = **trzecia składowa vec3 pozycji (Z)**, nie D template'u |
  | census D-dword 116 | **AUTHORITATIVE 117** | Ghidra isCall = 117 site'ów (raw-E8 = 116; QC B10 cytowała 116) |
  | wartość 124.941 przy 4508 | **ZWERYFIKOWANA, semantyka UNKNOWN** | własny walk: record 4508 @file 96496, size 28, CRC OK, A=296445, B=296446, D@file+0x20 (=payload+0x10) @96528 = bits 0x42F9E1CB = f32 124.94100189208984; E=0, F=0 |
  Zdanie „statycznie nierozstrzygalne" zastąpić: „semantyka liczbowa 124.941 **nie została dotąd
  rozstrzygnięta** (nie ogłaszano nierozstrzygalności z zasady); ANCHORS_ABSENT_SEMANTICS_OPEN".
- PODSTAWA: F2_T4508_WALK.json; F2_DCLAIMS.json (censusy 117/12/10); GHIDRA_REFCOUNTS.json;
  F2_CTX_*/hexdumpy FUN_00468910 (spot-check).

---

## CZĘŚĆ E — drobne korekty (z pinami; wszystkie zweryfikowane własnym odczytem)

| # | STARE | NOWE (pin) | Dowód własny |
|---|---|---|---|
| M-1 | zapis vft ArkModelResourceInstanceRef @0x006FA8BC (+0xC) [RUN3 AMENDMENT P3-2] | **@0x006FA8BD (+0xD)**: `C7 00 B8 64 A8 00` @0x006FA8BD (bajt @0x006FA8BC = ostatni 00 z `C7 40 04 00 00 00 00` MOV [EAX+4],0) | hexdump 0x006FA8B0: `8B C1 8B 4C 24 04 C7 40 04 00 00 00 00` (7B, do 0x006FA8BC) → `C7 00 B8 64 A8 00` @0x006FA8BD → `89 48 08` @0x006FA8C3 → `C2 04 00` |
| M-2 | „296445 LE (5d 85 04 00)" [RUN3 QC A1:22] | **FD 85 04 00** (296445 = 0x000485FD) | własne przeliczenie u32 |
| M-3 | zapis vft ArkObject @0x00726E9F [RUN3 QC A8:69] | **@0x00726EA1**: `C7 06 48 6B A8 00` (poprzedzająca instr. `8D 4E 08` LEA ECX,[ESI+8] @0x00726E9E; bajt @0x00726E9F = 0x4E operand LEA) | F1_HEX_CTOR_ARKOBJECT_00726E70.txt |
| M-4 | store +0x28 @0x006726EBC [RUN3 QC A8:69 — literówka] | **@0x00726EBC**: `89 46 28` | F1_HEX_CTOR_ARKOBJECT_00726E70.txt |
| M-5 | QC B8 przypisuje executorowi skan kotwic „aligned-only" | executor `s12_prt_content_check.py` skanuje 13 kotwic przez `payload.find(pat, off)` (**wszystkie offsety**; L63); caveat „aligned-only" odnosił się do ODRĘBNEGO censusu u32 (L68, L89-90) — powtórka QC nie zwiększyła zakresu skanu kotwic | odczyt s12_prt_content_check.py:63/68/89-90 |
| M-6 | „Execute ma zero znalezionych bezpośrednich CALL" jako granica RE | brak bezpośrednich CALL (0 — potwierdzone) **nie jest** dowodem braku wywołań (wirtualny dispatch przez vtable 0x00A7C1FC istnieje; RUN4 B6) — rozróżnienie „xref-statyczny" vs „osiągalność wirtualna" utrzymać w każdej granicy | GHIDRA_REFCOUNTS (metodologia isCall), RUN4 QC B6 (odczyt) |
| M-7 | łączenie mianowników joinu A | **3618/3618 = 100%** to pokrycie pola A (unikalne niezerowe A mają wpis <A>.nif); **3618/5596 = 64.6533%** to udział tych modeli w korpusie wpisów .nif Models.bnt — dwa różne mianowniki, nie zamienne | definicje z RUN1 Z2 + ROUND §7 (odczyt); 3618/5596 = 0.6465325... |
| M-8 | porządek walidacji manifestów (nakładka) | reguła do erraty: **ostatni poprawny manifest w czasie jest wiążący dla plików, które pokrywa**; closure manifest (49/49) pokrywa 5 nowszych plików; historyczne manifesty RUN3/RUN4 mają 1/4 rozbieżności DOKUMENTACYJNE (nie integralnościowe). Konkret tego runu: manifest GHIDRA_LOCAL pakietu RUN4 (`GHIDRA_LOCAL_MANIFEST_SHA256.csv`, 10 plików) opisuje stan PRZED turami ZS tego runu (listuje `db.52.gbf`/`db.53.gbf`, które w opublikowanym projekcie zostały nadpisane przez `db.63.gbf`/`db.64.gbf`) — manifest był nieaktualny względem własnych, opublikowanych plików projektu; projekt RUN4 nie został jednak zmieniony przez QC/closure (integrity: closure manifest). Kopia projektu w TYM runie ma własny, aktualny manifest (00_CONTROL\GHIDRA_LOCAL_MANIFEST_SHA256.csv) | porównanie manifestów (Compare-Object): 10 vs 10 wpisów, rozbieżność wyłącznie w numerach .gbf; GA5 census composite-hash pakietów przed/po |

---

## ZASADY SUPERSESSION (do ledgera)

1. Niniejszy draft NIE modyfikuje historycznych pakietów (GA5-IMMUTABLE: composite-hash przed/po
   identyczne; patrz GA5_IMMUTABLE_CENSUS_{before,after}.json). Korekty żyją jako errata i w
   RESEARCH_FINDINGS.md tego runu.
2. Kolejność wiążącości: (a) evidence 01_RAW/03_EVIDENCE pakietów runów (nietknięte), (b) amendments
   (QC) dopisane w CLOSURE, (c) niniejsza errata (kwalifikuje narracje ROUND/RUN3/RUN4), (d) raporty
   RUN3/RUN4 w miejscach skonfliktowanych z erratą — czytane przez pryzmat (c).
3. Żadne twierdzenie tego runu nie ogłasza STATIC_INSTANCE_MECHANISM_CONFIRMED ani źródła placementu
   (kontrola kontraktowa); RECEIVER_UNRESOLVED dla wartości mapy parametrów i odbiorców [arg1] w
   FUN_00567C50 pozostaje jawną granicą.
