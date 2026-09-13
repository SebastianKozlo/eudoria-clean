# ERRATA_R2 — PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912 (claims + narrative + next-step)

**RUN_ID:** PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913
**RUN_CLASS:** MATERIAL (audyt twierdzeń + nowy pomiar join + errata dokumentacyjna; ZERO zmian evidence)
**AUDYTOR:** pe-master-auditor (dispatch PE-MASTER; NO_NESTED_TASKS)
**AUDYTOWANY PAKIET:** `99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912\` (+ publikacja repo
`docs/audits/PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912\`) — **IMMUTABLE**: ten run nie zmienia
w nim żadnego bajtu (bramka G4: pełny re-hash pakietu przed/po — identyczny; baseline 674 plików
obu kopii zapisany przed startem pracy). Errata CYTUJE oryginały; poprawiona treść żyje tutaj
i w 06_REPORT\00_FINAL_REPORT.md tego runu.
**ŹRÓDŁA ZLECENIA:** EU935 §4 (człowiek, przez PE-MASTER); audyt zewnętrzny (Desktop)
`C:\Users\User\.codex\attachments\514c9eb5-c0b4-474a-96b2-9395d8c4e88b\pasted-text.txt` (rozdz.
twierdzeń A–E + findings A/B — odczytany w całości); poprzedni PE_MASTER_REVIEW pakietu.
**ERA:** EU 9.3.5 (pcg_install). Wszystkie liczby z nowych pomiarów tego runu (Z2/Z2c/Z3);
twierdzenia forensyczne runu R1 nie są tu powtarzane — tylko kwalifikowane semantycznie.

---

## 0. Kontekst i wynik rozstrzygający

Run R1 ustalił łańcuch VA-locked: parser A→+0x08 (@0x00730CE6) → getter FUN_007ce1e0 →
konsument FUN_006b4c50 → żądanie zasobu {typ 0x66=MODEL, id=A} (FUN_006c9700 → singleton
ArkResourceManager + dispatcher FUN_00823c10) i data-binding na 3 przykładach
(296445.nif/126740.nif/278453.nif) z negatywami. Audyt zewnętrzny (Desktop) dał całemu runowi
PARTIAL_PASS z dwoma findingami narracyjnymi (A: „łańcuch kompletny do otworzenia zasobu" o pół
kroku za mocny; B: C.4 network-first zbyt wąski) i jednym brakiem dowodowym: globalność mapowania
A→<A>.nif bez pełnego joinu. Ten run: (Z1) rozdziela i ocenia twierdzenia A–E; (Z2) wykonuje
PEŁNY JOIN A↔Models.bnt (+BONUS B↔Volumes.bnt) — **wynik: FULL_MAPPING 3,618/3,618 unikalnych
niezerowych A ma wpis <A>.nif (per-record 5,438/5,438; 0 rekordów A==0; 0 braków; 0 poza
zakresem; indeks bez duplikatów nazw)**; (Z3) census kwantyfikatorów (32 trafienia; 3 unikalne
miejsca overclaim; 9 fraz wymagających kwalifikacji statyczne-vs-runtime); (Z4) niniejsza errata.

Pełne mianowniki i kontrole: 06_REPORT\00_FINAL_REPORT.md §2 + 01_RAW\Z2_JOIN_RESULT.json.

---

## 1. Poprawki erraty [E-1..E-6]

Format każdej poprawki: (i) CYTAT zastępowanego twierdzenia (verbum + źródło: plik/linia);
(ii) nowa treść; (iii) status/uzasadnienie. Cytowane frazy zastępowane występują w tym dokumencie
DOKŁADNIE 1× (bramka G3) i nie występują w narracji poprawionej.

### [E-1] — kwalifikacja „w pełni zakotwiczony" do PARTIAL_TO_RESOURCE (finding A, poz. (a))

**CYTAT zastępowany (1×):**
> „Mechanizm jest w pełni zakotwiczony w kodzie (patrz sekcja B)"

Źródło: FINAL_REPORT §0 (06_REPORT\00_FINAL_REPORT.md L16 pakietu R1). Nota: QC runu R1 §9.6
oceniło frazę „uczciwie z notką" (czytanie przez pryzmat §2 z jawnym residuum); audyt zewnętrzny
Finding A orzek overclaim narracyjny („o pół kroku za mocny"); kwalifikacja erraty przyjmuje
ostrożniejszą wersję audytu zewnętrznego.

**Nowa treść (kanoniczna, do użycia zamiast cytatu):**
Łańcuch do ŻĄDANIA zasobu jest w pełni zakotwiczony w kodzie (VA-locked, CONFIRMED): reader
ArkVFS02 → parser A→+0x08 → rejestr → getter → konsument → żądanie {typ 0x66=MODEL, id=A}.
Fizyczne otwarcie wpisu <A>.nif jest STRONGLY_SUPPORTED (RTTI ArkModelResourceItemFactory +
rejestracja rozszerzenia „.nif" w RM-init FUN_0041dae0 + BNT2 reader FUN_00967d00 + data-binding
[od Z2: pełny join 3,618/3,618]) — NIE instruction-closed. Residuum (dokumentowane jawnie od
runu R1 §2): ciała metod wirtualnych providera/fabryki (node+0x24 → vtable[+4]/[+0x38])
niezdekomponowane; ciąg create→store-read w fabryce nie jest VA-locked. Klasyfikacja
GATE-A-CONSUMER = PARTIAL_TO_RESOURCE pozostaje obowiązująca.

### [E-2] — rozróżnienie statyczne-vs-runtime (poz. (b))

**CYTAT zastępowany (1×; fraza-klasa):**
> „klient posiada i wykonuje reader"

Źródło: audyt zewnętrzny §4 (własne podsumowanie CONFIRMED audytu; fraza-klasa odpowiada
indykatywnym sformułowaniom pakietu R1: FINAL_REPORT §0 „klient … czyta rekordy … i konsumuje
pole A", „konsumenci pobierają A getterem … i wołają FUN_006c9700(A,…)", „rekordy czyta
generyczny reader VFS"; HANDOFF „EU 9.3.5 czyta rekordy templates.vfs … i konsumuje A do
załadowania modelu"; pełna lista w 03_EVIDENCE\Z3_QUANTIFIER_CENSUS.csv, wiersze
NEEDS_QUALIFICATION — 9 trafień: 7 w warstwie głównej + 2 w warstwie PE-MASTER).

**Nowa treść (kanoniczna):**
Run R1 był STATIC-ONLY (klient NIGDY nie uruchomiony). Poprawne brzmienie wszystkich tych
twierdzeń: **klient ZAWIERA i MOŻE WYKONAĆ reader oraz łańcuch konsumpcji A (przepływ wykazany
statycznie — VA-locked na instrukcjach; brak runtime-observation)**. Czasowniki wykonaniowe
(„czyta/konsumuje/pobierają/wołają") w dokumentacji runu R1 opisują statyczny przepływ w kodzie,
nie zaobserwowany przebieg. Wynik runu R1 nie jest osłabiony: statyczny dowód przepływu jest
kompletny w swoim zakresie; chodzi wyłącznie o precyzję słownictwa (statyczny przepływ vs
runtime-observation). Nie dotyczy opisów rozkazów byte-locked („ścieżka modelu czyta WYŁĄCZNIE
+0x08" = opis statycznych instrukcji — poprawne użycie).

### [E-3] — sekcja C.4: network-first → hipotezy neutralne z priorytetem śladu statycznego (finding B, poz. (c))

**CYTAT zastępowany (1×):**
> „Kolejność pracy dla przyszłego runu: (1) zdekodować warstwę sieci (login/stream), (2) znaleźć
> create-object handler, (3) śledzić transformację do vtable set-position."

Źródło: 02_ANALYSIS\C_transform_source_and_D_placement.md C.4 (ostatni punkt). Kontekst cytatu:
to samo zdanie wiersz wyżej zawiera dodatkowo nieudowodnioną konieczność modalną (census Z3,
OVERCLAIM, ref [E-3]): „Transformacja modelu per-instancja MUSI przechodzić przez menedżer
sceny/modeli" — kwalifikowana do: hipoteza architektoniczna (PLAUSIBLE), nie wykazana konieczność.

**Cytat uzasadniający z audytu zewnętrznego (Desktop, §6):**
> „Po naszym dzisiejszym researchu **nie ma podstaw, aby dla statycznych budynków przyjąć
> network-first**." oraz: „To **nie dowodzi**, że EU935 ma `fixtures.csv`-like format. Ale
> wystarcza, by odrzucić network-first jako założenie."

**Nowa treść (kanoniczna):**
Kolejność pracy dla przyszłego runu placementu = hipotezy KONKURENCYJNE, neutralne, bez
network-first jako założenia:
- **H_CLIENT** (priorytet dla statyków — jako KIERUNEK BADAWCZY, nie dowód): authored placement
  statycznych budynków istnieje w LOKALNYM korpusie klienta EU 9.3.5 (kandydaci: fixture-like
  rekordy {model/id, XYZ, rotacja, skala}; struktury per-sector/cell/terrain; PRT/Strings/200xx.vfs).
- **H2 CLIENT_DERIVED**: placement zakodowany pośrednio w strukturach sector/cell/terrain/world.
- **H_SERVER**: placement dostarczany runtime z serwera (dekoder strumienia sieci).
- **H4 HYBRID**: szkielet definicji lokalnie, aktywacja/uzupełnienie z serwera.
Ślad network (create-object → transform-set) uruchamiać dopiero, gdy (a) census client-side
wyczerpany i negatywny, LUB (b) code trace prowadzi wprost do obiektu sesji/sieci.
Uzasadnienie priorytetu H_CLIENT — JAKO KIERUNEK BADAWCZY, NIE DOWÓD: (1) historyczny
world-editor MindArk (2002, Worthplaying: rozmieszczanie miast/mieśc w edytorze świata);
(2) CGW 2003 (osobni artyści „static objects and environments"); (3) precedens NetImmerse w
innych MMO tej ery (DAoC: katalog modeli nifs.csv + fixtures.csv {NIF ID, XYZ, angle, scale} —
podział catalogue/fixtures bez potrzeby sieci dla świata statycznego). ŻADEN z tych trzech
argumentów nie jest dowodem o EU 9.3.5 (zakaz transferu formatu DAoC); podnosi jedynie
racjonalność kolejności przeszukiwań. Zakaz wnioskowania: „brak dowodu placementu w
przeszukanych miejscach NIE jest dowodem server-delivered" (audyt zewnętrzny §7). Hipoteza PE2
(server-delivered: 0x1C + transform sub-record + vtable[0x50]) pozostaje NIEPRZENIESIONĄ
HIPOTEZĄ, bez pierwszeństwa.

### [E-4] — mapowanie A na nazwę wpisu `<A>.nif`: awans do CONFIRMED z pełnym censusem Z2 (poz. (d))

**CYTAT zastępowany (1×):**
> „A dosłownie nazywa wpis `<A>.nif`"

Źródło: FINAL_REPORT §0 (w zdaniu „…z dostawą z archiwów BNT2 (Models.bnt), gdzie A [cytat]");
odpowiednik w PE_MASTER_REVIEW L6 (to samo twierdzenie z doprecyzowaniem „w Models.bnt").
Kwalifikacja audytu zewnętrznego §5: zdanie „powinno być albo ograniczone do zweryfikowanych
przypadków, albo poparte pełnym joinem całego population A↔Models.bnt" — wykonano join.

**Nowa treść (kanoniczna):**
Mapowanie wartości A na nazwę wpisu `<A>.nif` w Models.bnt jest **CONFIRMED z pełnym censusem**
(pełne odwzorowanie; run Z2, era EU 9.3.5): 3,618/3,618 unikalnych niezerowych A ma wpis
`<A>.nif` (per-record 5,438/5,438; 0 rekordów z A==0; 0 braków; 0 wartości poza zakresem nazw;
indeks Models.bnt 5,596 wpisów <id>.nif, zero duplikatów nazw → wielokrotne trafienia w tym
kierunku niemożliwe). Kwalifikatory: (i) era 9.3.5 pcg_install; (ii) mapowanie STATYCZNE
danych (nazwa wpisu indeksu), nie runtime-load; (iii) mechanizm żądania = {typ 0x66, id} —
konsument nie buduje ścieżki; rozszerzenie .nif rejestrowane globalnie (RM-init); (iv) kontekst
odwrotny: 1,978 wpisów .nif nie jest referencjonowanych przez pole A template'ów (Models.bnt
= nadzbiór — spodziewane, modele referencjonowane także z innych systemów). BONUS (odrębny
mianownik): B→`<B>.bvi` w Volumes.bnt: 1,666/1,666 unikalnych niezerowych B (per-record
1,692/1,692; 3,746 rekordów z B==0; 199 wpisów .bvi niereferencjonowanych). Kontrole: 20/20
negatywów syntetycznych (A+1,000,000) nieobecnych; round-trip endianness 0 błędów; kotwica
surowa 4508 (fd 85 04 00 → LE 296445); kontrola BE: 1/3,618 (palindrom bajtów A=592128 —
zbieg, nie interpretacja); niezależny surowy byte-scan 8/8 + 5/5 pozytywów, wszystkie negatywy 0,
census „.nif\n" 5,596 == parser.

### [E-5] — literówka w historycznym PE_MASTER_REVIEW.md (poz. (e))

**CYTAT zastępowany (1×):**
> „## GWNE PYTANIE P0 — ODPOWIEDŹ"

Źródło: 06_REPORT\PE_MASTER_REVIEW.md L5 pakietu R1 (autorstwo: PE-MASTER; nagłówek sekcji).
Błąd typu brak polskich znaków („GWNE" zamiast poprawnego słowa).

**Poprawiona kopia w formie cytatu-linii (bez modyfikacji oryginału — pakiet immutable):**
> ## GŁÓWNE PYTANIE P0 — ODPOWIEDŹ

Adnotacja: oryginał pozostaje nietknięty (bramka G4); powyższa linia jest JEDYNIE poprawioną
kopią nagłówka do celów cytowania w przyszłych dokumentach. Żadna treść merytoryczna
PE_MASTER_REVIEW nie jest przez to zmieniona (literówka kosmetyczna, bez wpływu na werdykt
MASTER_ACCEPTED advisory).

### [E-6] — (audytor, z census Z3) adnotacja do frazy w warstwie PE-MASTER

**CYTAT zastępowany (1×):**
> „Łańcuch kompletny do otworzenia zasobu modelu; residuum jawne: …"

Źródło: 06_REPORT\PE_MASTER_REVIEW.md L9 pakietu R1 (autorstwo: PE-MASTER — warstwa advisory;
fraza cytowana wprost przez audyt zewnętrzny Finding A jako przykład overclaimu narracyjnego
„o pół kroku za mocny"). Pakiet immutable; adnotacja erraty (bez modyfikacji oryginału):
poprawne warstwowanie jak w [E-1] — do ŻĄDANIA zasobu = CONFIRMED (VA-locked); fizyczne
OTWARCIE = STRONGLY_SUPPORTED (RTTI + rejestracja .nif + BNT2 reader + data-binding [Z2:
3,618/3,618]), nie instruction-closed. Uczciwość oryginalnego zdania ratuje natychmiastowe
„residuum jawne" w tej samej linii; errata precyzuje warstwy, nie obala werdyktu.

---

## 2. Census narracji (Z3) — wynik maszynowy

Pełny zapis: 03_EVIDENCE\Z3_QUANTIFIER_CENSUS.csv (32 wierszy: plik, linia, fraza, ocena,
uzasadnienie, ref erraty) + 03_EVIDENCE\Z3_QUANTIFIER_HITS_RAW.csv (scan mechaniczny) +
03_EVIDENCE\Z3_QUANTIFIER_SCAN_SUMMARY.json + 03_EVIDENCE\Z3_CENSUS_SUMMARY.json.

| ocena | liczba (warstwa główna / AUX PE-MASTER) | ref erraty |
|---|---|---|
| OVERCLAIM_AS_WORDED | 3 (2 unikalne miejsca) / 1 | [E-1], [E-3], [E-6] |
| NEEDS_QUALIFICATION (statyczne-vs-runtime) | 7 / 2 | [E-2] |
| OK_FACTUAL / OK_SCOPED / OK_STATIC_CODE_DESC / OK_FACTUAL_NEGATIVE | 6 / 7 / 3 / 2 oraz 0 / 0 / 1 / 0 | — (zgodne z bramkami) |

Unikalne miejsca overclaim (warstwa główna): FINAL_REPORT §0 L16 (→ [E-1]);
C_transform_source_and_D_placement.md C.4 L46 (→ [E-3]). Warstwa AUX: PE_MASTER_REVIEW.md L9
(→ [E-6]). Fraza „pełny łańcuch": 0 wystąpień w pakiecie; „zawsze": 0; „cały/cał*": 0
(census również tych fraz — brak trafień). STAGE_ACCEPTANCE_GATES.csv: 1 trafienie (opis
statyczny byte-locked — OK). Uwaga: STAGE_ACCEPTANCE_GATES.csv zawiera też literówkę
„scieyka modelu" (GATE-B-C) — kosmetyczna, bez wpływu na treść; adnotacja bez poprawki
(pakiet immutable).

## 3. Zakres erraty i NIETYKALNOŚĆ

- ZERO zmian w opublikowanym pakiecie PE_935_TEMPLATE_CONSUMER_TRACE_R1 (bramka G4: hashe
  wszystkich plików obu kopii przed/po identyczne; baseline w 00_CONTROL pakietu tego runu).
- ZERO zmian evidence (01_RAW, dumpy, skrypty S1–S20, qc_probe) i generatorów runu R1.
- Poprawki dotyczą WYŁĄCZNIE narracji/kwalifikacji twierdzeń na warstwie dokumentacyjnej
  (kanoniczna poprawiona treść = ten plik + 06_REPORT\00_FINAL_REPORT.md tego runu).
- Wyniki naukowe runu R1 (łańcuch VA-locked, data-binding, bramki, klasyfikacja PARTIAL) —
  NIENARUSZONE i wzmocnione (Z2: full mapping).
- Pliki oryginalne (Entropia.exe, templates.vfs, Models.bnt, Volumes.bnt): READ-ONLY;
  brak ekstrakcji payloadów .nif/.bvi (dozwolone metadane: nazwy/offsety indeksów, CSV z ID).
