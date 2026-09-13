# 02_ANALYSIS — Z1. Macierz twierdzeń A–E (audyt semantyczny twierdzeń runu PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912)

RUN_ID: PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913 | AUDYTOR: pe-master-auditor (dispatch PE-MASTER)
ERA: EU 9.3.5 (pcg_install). Binarium: Entropia.exe SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31.
Dane: templates.vfs BE57818C…, Models.bnt C950A8C2…, Volumes.bnt 6AD8BA3C… (wszystkie zweryfikowane na starcie tego runu).

ZAKRES MACIERZY: rozdzielenie i ocena KAŻDEGO twierdzenia kontraktu runu R1 osobno, wg słownika
statusów CONFIRMED / STRONGLY_SUPPORTED / PLAUSIBLE / UNVERIFIED / REJECTED. Bez powtarzania
forensyki runu R1 (odpowiedniki byte-level były niezależnie rewalidowane przez fresh QC runu R1:
address-lock 6/6 + ~40 ogniw, zero rozbieżności bajtowych); niniejszy run dodaje: (1) semantyczny
audyt twierdzeń na tle klasyfikacji bramek, (2) NOWY pomiar join (Z2) dla twierdzenia C,
(3) census narracji (Z3). Zakaz awansu B→C (narracyjnie) oraz A/B→D/E — dotrzymany: jedyny awans
w tej macierzy (B→C) następuje WYŁĄCZNIE przez nowy pomiar Z2 z pełnym mianownikiem, nie przez
reklamę narracji.

RUN R1 BYŁ STATYCZNY (STATIC-ONLY): klient nigdy nie został uruchomiony; wszystkie statusy
poniżej opisują STATYCZNY przepływ w kodzie i STATYCZNE mapowanie danych, chyba że jawnie
zaznaczono inaczej. Fraza „klient wykonuje X" oznacza w praktyce: „klient zawiera i może
wykonać X (statycznie wykazany przepływ; brak runtime-observation)" — patrz errata [E-2].

---

## Twierdzenie A — „Pole A jest konsumowane jako identyfikator zasobu modelowego (łańcuch code-level do żądania {0x66})"

**Status: CONFIRMED (przepływ statyczny, VA-locked; kwalifikacja STATIC-ONLY).**

Łańcuch dowodowy (każde ogniwo z surowymi bajtami w dumpach; rewalidowane niezależnie przez QC
runu R1; wyrywkowo reodczytane w tym runie — patrz FULL_READ_LOG):

1. Parser zapisuje A do +0x08 parsed-objektu: `MOV [EDI+0x08],EAX` @0x00730CE6
   (01_RAW\ghidra_output\S6_DISASM_parse_00730c90.txt L35 — potwierdzone w tym runie odczytem dumpu).
2. Getter A: `MOV EAX,[ECX+0x8]; RET` (8b 41 08 c3) @0x007CE1E0
   (S11_DISASM_getter_007ce1e0.txt — potwierdzone w tym runie odczytem dumpu).
3. Konsument kompletny FUN_006b4c50: `iVar2 = FUN_007ce1e0()` → `FUN_006c9700(iVar2,…)`
   (S20_PSEUDO_MRQ_006B4C50.txt L53/L103 — potwierdzone w tym runie odczytem pełnego pseudokodu).
4. Pump żądań FUN_006c9700: `MOV [ESP+0x20],0x66` @0x006C973A (kod typu MODEL) → CALL 00415670
   (singleton ArkResourceManager) @0x006C9746 → CALL 00823c10 (dispatcher provider-chain)
   @0x006C974D (S20_DISASM_PUMP_006c9700.txt — potwierdzone w tym runie odczytem dumpu).

Wzmocnienie z Z2 (nowe): wszystkie 5,438 rekordów ma A≠0 i KAŻDY unikalny A (3,618) jest
prawidłowym id modelu w indeksie Models.bnt (FULL_MAPPING) — semantyka „identyfikator zasobu
modelowego" jest spójna z całym korpusem, nie tylko z 3 przykładami.

Granice statusu: (i) STATIC-ONLY — brak runtime-observation (errata [E-2]); (ii) łańcuch jest
kompletny DO ŻĄDANIA zasobu — nie do fizycznego otwarcia (patrz twierdzenie D). Audyt zewnętrzny
(Desktop): „To nie jest już korelacja nazw plików, tylko dataflow w kodzie klienta" — zgodność.

## Twierdzenie B — „W SPRAWDZONYCH przypadkach A odpowiada wpisowi <A>.nif w Models.bnt"

**Status: CONFIRMED (mapowanie statyczne, byte-proof na dokładnych offsetach nazw w regionie
indeksu; scope: sprawdzone przypadki).**

Sprawdzone przypadki runu R1: 296445.nif @395,268,773; 126740.nif @395,268,719;
278453.nif @395,268,746 (trzy kolejne wpisy co 27 B — ciągła tabela indeksu BNT2).
Negatywy: 999999999.nif nieobecny; cross-absent 296446.nif nieobecny w Models.bnt.
QC runu R1 niezależnie potwierdził 6/6 offsetów + 2 negatywy (qc_B §4).

Niezależna weryfikacja w tym runie (Z2c): surowy byte-scan całych archiwów potwierdza
wystąpienia nazw (8/8 próbek A, 5/5 B — każda dokładnie 1 wystąpienie) i 0 wystąpień negatywów;
census surowy „.nif\n" = 5,596 == liczba wpisów parsera (zgodność pełnokorpusowa metod).

Uwaga semantyczna: „A odpowiada wpisowi <A>.nif" to mapowanie WARTOŚCI A (u32 LE) na NAZWĘ wpisu
indeksu (format dziesiętny). Mechanizm runtime NIE buduje ścieżki w consumerze — konsumer
przekazuje {typ 0x66, id} (B.2 runu R1); rozszerzenie .nif rejestrowane globalnie w RM-init
FUN_0041dae0. „Odpowiada" = korespondencja danych, nie udowodniona instrukcja formatująca
(„%d" → ".nif" istnieje w warstwie fabryk: FUN_00799bf0 — ogniwo zapamiętane w Z2 jako kontekst,
bez instruction-lock ciała fabryki).

## Twierdzenie C — „WSZYSTKIE odpowiednie A w korpusie mają takie odwzorowanie"

**Status: CONFIRMED — rozstrzygnięte NOWYM pomiarem Z2 (pełny join z dokładnymi mianownikami);
przed Z2 status globalny był niewykazany (audyt zewnętrzny: „globalność <A>.nif nie została mi
wykazana pełnym denominatorowym joinem").**

Wynik Z2 (01_RAW\Z2_JOIN_RESULT.json; skrypty zhashowane przed wykonaniem; G1 podwójna
rekomputacja identyczna):

- rekordów template razem: **5,438** (własny walk 5,438/5,438 do EOF, 0 CRC-fail; zgodność
  per-row z S2_TEMPLATES_TRUE_WALK.csv runu R1: IDENTYCZNA);
- unikalne T (id): **5,438** (zero duplikatów id);
- unikalne niezerowe A: **3,618**; rekordów z A==0: **0** (sentinel zero w polu A nie występuje
  w korpusie — walidacja (A∨B∨C)≠0 spoczyna tu na B/C);
- Models.bnt: indeks **5,596** wpisów, WSZYSTKIE <id>.nif (0 nienumerycznych, 0 duplikatów
  nazw), id z zakresu [53 .. 592,853];
- **JOIN A→<A>.nif: 3,618/3,618 trafień (100%), 0 braków**; per-record: 5,438/5,438;
- rozkład A poza zakresem nazw: **0** (max A = 592,853 == max id .nif; min A = 53 == min id .nif;
  dziedzina A ⊆ dziedzina id .nif);
- wielokrotne: **niemożliwe w tym kierunku** (0 duplikatów nazw w indeksie → każde A mapuje co
  najwyżej na 1 wpis); mnożność po stronie template: 253 wartości A dzielonych przez >1 template;
- BONUS (odrębny mianownik): **JOIN B→<B>.bvi: 1,666/1,666 trafień (100%), 0 braków** (unikalne
  niezerowe B; Volumes.bnt 1,865 wpisów <id>.bvi; per-record 1,692/1,692 rekordów z B≠0;
  3,746 rekordów z B==0);
- kontrola negatywna: 20/20 syntetycznych A (realne+1,000,000) NIEOBECNYCH w Models.bnt;
  pozytywne piny obecne; negatywne piny (999999999.nif/.bvi; cross-absent 296446.nif,
  296445.bvi) nieobecne;
- endianness: round-trip pack("<I")→unpack("<I") 0 błędów; kotwica surowa rekordu 4508
  (A@96,516: fd 85 04 00 → LE 296445; BE 4,253,352,960); kontrola dyskryminatywna BE: join pod
  interpretacją BE = 1/3,618 (jedyny „trafiony" A=592128 ma bajty palindromiczne 00 09 09 00 —
  LE==BE z definicji; czysty zbieg, nie dowód BE);
- niezależny kontr-check (Z2c): surowy byte-scan 8/8 pozytywów A + 5/5 B + wszystkie negatywy 0;
  census „.nif\n" w całym Models.bnt = 5,596 == census parsera; „.bvi\n" = 1,865 == parser.

Werdykt twierdzenia C: **PEŁNE ODWZOROWANIE** (FULL_MAPPING) — z jawnymi kwalifikatorami:
(i) era EU 9.3.5 pcg_install (nie transfer na inne ery); (ii) mapowanie STATYCZNE nazw/danych,
nie runtime-load; (iii) „odpowiednie A" = wszystkie niezerowe A (A==0 nie występuje — klauzula
 bezobjektowa); (iv) kontekst odwrotny: 1,978 wpisów .nif nie jest referencjonowanych przez
żadne A (Models.bnt jest nadzbiorem dziedziny A — spodziewane: modele referencjonowane także
z innych systemów niż template'y); (v) join dotyczy ISTNIENIA wpisów nazwanych — nie dekoduje
payloadów .nif/.bvi (zakaz ekstrakcji dotrzymany).

## Twierdzenie D — „Cała ścieżka wykonania od A do fizycznego odczytu wpisu jest rozpisana"

**Status: REJECTED as worded (odrzucone w brzmieniu) — z zachowaniem ważnych warstw;
GATE-A-CONSUMER = PARTIAL_TO_RESOURCE pozostaje uczciwą klasyfikacją.**

Rozstrzygnięcie uczciwe (zgodne z taskiem i z Finding A audytu zewnętrznego):

- Ciała metod wirtualnych providera/fabryki (FUN_00823c10 → node+0x24 → vtable[+4]/[+0x38])
  NIE są zdekomponowane; ciąg instrukcji create→store-read wewnątrz fabryki NIE jest VA-locked.
  Tożsamość klasy = RTTI/boost-names (ArkModelResourceItemFactory), nie dekompilacja ciała.
- „Fizyczne otwarcie" wpisu <A>.nif = **STRONGLY_SUPPORTED** (nie instruction-closed):
  (1) RTTI fabryki modeli; (2) rejestracja rozszerzenia ".nif" w RM-init FUN_0041dae0
  (+ tester FUN_007ee5f0 w tabeli klas); (3) BNT2 reader FUN_00967d00 (magia "BNT2"
  @0x00A9BF2C) + cache get-or-create FUN_00799930; (4) data-binding: pełny join Z2
  (3,618/3,618 <A>.nif istnieje w Models.bnt). Silne kumulatywne domknięcie dowodowe —
  brakujące ogniwo instrukcyjne = jedyna luka.
- Łańcuch do ŻĄDANIA zasobu {0x66, id=A} = CONFIRMED (VA-locked; twierdzenie A).

Poprawne brzmienie zamiast odrzuconego: „łańcuch do ŻĄDANIA zasobu = w pełni rozpisany
(VA-locked); fizyczne otwarcie = STRONGLY_SUPPORTED (RTTI + rejestracja + BNT2 reader +
data-binding), NIE instruction-closed; residuum = ciała metod wirtualnych providera/fabryki".
Zgodność: GATE-A-CONSUMER = PARTIAL_TO_RESOURCE (bramka runu R1); audyt zewnętrzny Finding A;
errata [E-1]/[E-6].

## Twierdzenie E — „Instancja modelu otrzymuje historyczny world transform"

**Status: UNVERIFIED (nie wykazane; brak dowodu w którąkolwiek stronę — UNVERIFIED, nie REJECTED).**

- Run R1: sekcja C NIE OSIĄGNIĘTA — wejście do dekodera strumienia sieciowego niezidentyfikowane;
  census 25 call-site'ów lookupu / 13 callerów pumpu bez cech create-object-handler z f32 XYZ;
  łańcuch urywa się na attach zasobu do encji (vtable[+0xA4] w FUN_006b4c50) bez dalszego śladu
  do transform-set. Potwierdzone w tym runie odczytem S20_PSEUDO_MRQ_006B4C50.txt: po attach
  brak jakiejkolwiek operacji transformacyjnej w tej funkcji.
- Sekcja D (placement historyczny): NIE ZNALEZIONO; zero mock-spawnów (zgodnie z kontraktem).
- Hipoteza PE2 (server-delivered: 0x1C + transform sub-record + vtable[0x50]) pozostaje
  NIEPRZENIESIONĄ HIPOTEZĄ — bez statusu dowodowego dla EU 9.3.5.
- Nowszy kontekst badawczy (erratą [E-3], jako KIERUNEK badawczy — nie dowód): historyczny
  world-editor MindArk (2002) + precedens fixture-record NetImmerse (DAoC: nifs.csv/fixtures.csv
  {NIF ID, XYZ, angle, scale}) podnoszą priorytet poszukiwania LOKALNEGO authored-placementu
  statyków (H_CLIENT) nad network-first; network pozostaje konkurencyjną hipotezą (H_SERVER).
  „Brak dowodu placementu w przeszukanych miejscach nie jest dowodem server-delivered" (audyt
  zewnętrzny §7).

## Podsumowanie macierzy

| twierdzenie | treść (skrót) | status | rola Z2 |
|---|---|---|---|
| A | A konsumowane jako id zasobu modelowego (do żądania {0x66}) | **CONFIRMED** (static, VA-locked; kwalifikacja STATIC-ONLY) | wzmocnienie: 3,618/3,618 unikalnych A to prawidłowe id modeli |
| B | w SPRAWDZANYCH przypadkach A ↔ <A>.nif | **CONFIRMED** (byte-proof; scope: sprawdzone) | niezależny kontr-check byte-scan 8/8 |
| C | WSZYSTKIE odpowiednie A ↔ <A>.nif | **CONFIRMED** — pełne odwzorowanie (3,618/3,618; per-record 5,438/5,438) | ROZSTRZYGNIĘTE przez Z2 (nowy pomiar) |
| D | cała ścieżka do fizycznego odczytu rozpisana | **REJECTED as worded**; warstwy: do żądania = CONFIRMED; fizyczne otwarcie = STRONGLY_SUPPORTED (nie instruction-closed); residuum = ciała providera/fabryki | data-binding join = 4. filar STRONGLY_SUPPORTED |
| E | instancja otrzymuje historyczny world transform | **UNVERIFIED** (sekcja C/D nieosiągnięte; hipotezy konkurencyjne otwarte) | bez wpływu (poza zakresem Z2) |

Zakazy kontraktu dotrzymane: awans B→C nastąpił wyłącznie przez pomiar Z2 (pełny mianownik,
kontrole negatywne, podwójna rekomputacja, niezależny byte-scan); awans A/B→D/E nie nastąpił
(D odrzucone w brzmieniu; E pozostaje UNVERIFIED).
