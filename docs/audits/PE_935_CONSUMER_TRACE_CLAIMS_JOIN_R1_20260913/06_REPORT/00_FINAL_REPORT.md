# PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1 — FINAL REPORT

**RUN_ID:** PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913
**Executor:** pe-master-auditor (dispatch bezpośredni PE-MASTER; NO_NESTED_TASKS)
**RUN_CLASS:** MATERIAL (audyt twierdzeń A–E runu R1 + nowy pomiar join + errata; ZERO zmian evidence)
**RUN_STATUS:** COMPLETE (wszystkie bramki G1–G6 PASS; errata opublikowana; żadna przeszkoda twarda)
**HARD_STOP_REASON:** NONE
**ERA:** EU 9.3.5 (pcg_install). **Audytowany pakiet:** PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912
(repo `docs/audits/…` + lokalny `99_Audits\…`) — IMMUTABLE w tym runie (G4: 674 pliki obu kopii
przed/po — identyczne bajtowo).

**Wejścia (własna weryfikacja SHA256 na starcie, fail-closed w skrypcie Z2):**
- templates.vfs `BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77` (560,788 B)
- Models.bnt `C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0` (395,412,868 B)
- Volumes.bnt `6AD8BA3C5AD6F7534F91C1956A0E36485A49BBEF3FFA918CBDDC0C68EDBABC09` (3,746,375 B)
- S2_TEMPLATES_TRUE_WALK.csv runu R1 (pełny walk 5,438 rekordów; użyty do asercji zgodności)
- audyt zewnętrzny (Desktop) — odczytany w całości; PE_MASTER_REVIEW pakietu R1 (literówka + kontekst)

---

## 0. Odpowiedź główna (Z1 + Z2 + Z3 + Z4 w jednym akapicie)

Macierz twierdzeń A–E (Z1) rozdziela to, co run R1 udowodnił, od tego, co tylko sugerował:
**A** (pole A konsumowane jako id zasobu modelowego, łańcuch do żądania {0x66}) = **CONFIRMED**
(przepływ statyczny, VA-locked; kwalifikacja STATIC-ONLY); **B** (mapowanie A na wpis `<A>.nif`
w SPRAWDZONYCH przypadkach) = **CONFIRMED** (byte-proof); **C** (WSZYSTKIE odpowiednie A) =
**CONFIRMED — rozstrzygnięte NOWYM pomiarem Z2: PEŁNE ODWZOROWANIE 3,618/3,618** unikalnych
niezerowych A (per-record 5,438/5,438; 0 rekordów A==0; 0 braków; 0 poza zakresem; bonus B:
1,666/1,666); **D** (cała ścieżka do fizycznego odczytu rozpisana) = **REJECTED as worded** —
łańcuch do ŻĄDANIA zasobu = CONFIRMED (VA-locked), fizyczne otwarcie = STRONGLY_SUPPORTED
(RTTI + rejestracja .nif + BNT2 reader + data-binding), NIE instruction-closed; residuum = ciała
metod wirtualnych providera/fabryki; **E** (world transform instancji) = **UNVERIFIED**. Census
Z3 (32 trafienia): 2 unikalne miejsca overclaim w warstwie głównej + 9 fraz indykatywnych
wymagających kwalifikacji statyczne-vs-runtime (run R1 = STATIC-ONLY); wszystko skodyfikowane
w ERRATA_R2 [E-1..E-6] (Z4). Wynik naukowy runu R1 — NIENARUSZONY i WZMOCNIONY.

## 1. Macierz twierdzeń A–E (Z1)

Pełna wersja z dowodami: `02_ANALYSIS\Z1_CLAIMS_MATRIX.md`.

| twierdzenie | status | istota |
|---|---|---|
| A | **CONFIRMED** (static, VA-locked; kwalifikacja STATIC-ONLY) | parser A→+0x08 @0x00730CE6 → getter FUN_007ce1e0 → konsument FUN_006b4c50 → żądanie {0x66, id=A} FUN_006c9700 → singleton ArkResourceManager + dispatcher; wyrywkowo reodczytane dumpy w tym runie (S6/S11/S20) — zgodne |
| B | **CONFIRMED** (byte-proof; scope: sprawdzone przypadki) | 296445.nif/126740.nif/278453.nif na dokładnych offsetach nazw + negatywy; niezależny byte-scan tego runu 8/8 + 5/5 |
| C | **CONFIRMED — pełne odwzorowanie (Z2)** | 3,618/3,618 unikalnych niezerowych A → wpis `<A>.nif`; per-record 5,438/5,438; A==0: 0 rekordów |
| D | **REJECTED as worded** (warstwy: do żądania = CONFIRMED; fizyczne otwarcie = STRONGLY_SUPPORTED, nie instruction-closed) | ciała metod wirtualnych providera/fabryki niezdekomponowane; ciąg create→store-read nie jest VA-locked; GATE-A-CONSUMER = PARTIAL_TO_RESOURCE pozostaje |
| E | **UNVERIFIED** | sekcja C/D runu R1 nieosiągnięte; hipotezy H_CLIENT/H2/H_SERVER/H4 otwarte; network bez pierwszeństwa jako założenia (erratą E-3) |

Zakazy awansu dotrzymane: jedyny awans (B→C) wyszedz wprost z nowego pomiaru Z2 z pełnym
mianownikiem i kontrolami; A/B nie awansowały do D/E.

## 2. Z2 — pełny JOIN A↔Models.bnt (+BONUS B↔Volumes.bnt): wynik

Generator: `00_CONTROL\z2_join_a_models.py` (SHA pin przed wykonaniem: F47A840A…; re-run
identyczny — powtarzalność; post-run hash == pin). Własny walk templates.vfs 5,438/5,438 do
EOF, 0 CRC-fail; zgodność per-row z S2 CSV runu R1: IDENTYCZNA. Własny parser indeksu BNT2
(trailer [u32 index_start]["BNT2"]; blob: [u32 count][count×{nazwa\0A, u32 packed, u32 offset,
u32 c, u32 d}] + trailer), asercja pełnego skonsumowania do traileru + samozgodność traileru;
**kalibracja**: pozycje nazw-stringów odtworzone EXACT vs byte-scan runu R1 (296445.nif
@395,268,773; 126740.nif @395,268,719; 278453.nif @395,268,746; 296446.bvi @3,701,937;
126741.bvi @3,701,883; 278454.bvi @3,701,910) — parser związany bajtowo z niezależnym pomiarem
R1. Pole `offset` indeksu = lokalizacja payloadu (NOWA miara; R1 nie twierdził o payloadach).

| miara | wartość |
|---|---|
| rekordów template razem | **5,438** |
| unikalne T (id) | **5,438** (0 duplikatów) |
| unikalne niezerowe A | **3,618** |
| rekordy z A==0 | **0** (pole A nie przyjmuje zera w tym korpusie) |
| unikalne B (z zerem / niezerowe) | 1,667 / **1,666**; rekordów z B==0: **3,746** |
| Models.bnt: wpisy / format | **5,596** — wszystkie `<id>.nif` (0 nienumerycznych; **0 duplikatów nazw**) |
| Models.bnt: zakres id .nif | [53 .. 592,853] |
| Volumes.bnt: wpisy / format | **1,865** — wszystkie `<id>.bvi` (0 duplikatów) |
| **JOIN A→`<A>.nif` (unikalne A)** | **3,618 trafień / 0 braków** (100%) |
| JOIN A per-record | **5,438/5,438** |
| wielokrotne w tym kierunku | **niemożliwe** (0 duplikatów nazw w indeksie); po stronie template: 253 A dzielonych przez >1 template |
| A poza zakresem nazw | **0** (max A = 592,853 == max id .nif; min A = 53 == min id .nif; dziedzina A ⊆ dziedzina id .nif) |
| **BONUS: JOIN B→`<B>.bvi` (unikalne niezerowe B)** | **1,666 trafień / 0 braków** (100%); per-record 1,692/1,692 (rekordy z B≠0) |
| kontekst odwrotny | 1,978 wpisów .nif i 199 wpisów .bvi niereferencjonowanych (nadzbiory — spodziewane: inne systemy niż template'y) |

**Kontrole (G1):** podwójna rekomputacja join (membership vs przecięcie zbiorów int-ID) identyczna;
round-trip endianness pack→unpack 0 błędów na wszystkich 3,618 A; kotwica surowa 4508: bajty
@96,516 = `fd 85 04 00` → LE 296445 (BE 4,253,352,960); kontrola dyskryminatywna BE: 1/3,618 —
jedyny „trafiony" A=592128 ma bajty palindromiczne `00 09 09 00` (LE==BE z definicji; czysty
zbieg); negative-control: 20/20 syntetycznych A (realne+1,000,000, seed 20260913) NIEOBECNYCH;
pozytywne piny obecne; negatywne piny (999999999.nif/.bvi, cross-absent 296446.nif, 296445.bvi)
nieobecne. **Niezależny kontr-check (Z2c): surowy byte-scan** (metoda QC R1, bez parsera):
8/8 próbek A + 5/5 B obecnych (każda dokładnie 1×), wszystkie negatywy 0; census surowy
".nif\n" = 5,596 == parser; ".bvi\n" = 1,865 == parser (zgodność pełnokorpusowa obu metod).

**Werdykt twierdzenia C: PEŁNE ODWZOROWANIE (FULL_MAPPING)** z kwalifikatorami: era 9.3.5
pcg_install; mapowanie statyczne danych (nie runtime-load); „odpowiednie A" = wszystkie
niezerowe A (A==0 nie występuje); istnienie wpisów nazwanych, bez dekodowania payloadów.

Uczciwa adnotacja metodyczna: pierwsza wersja kalibracji parsera błędnie traktowała offsety
byte-scan R1 jako offsety payloadów — FAIL-CLOSED zatrzymał pomiar, semantyka skorygowana
(offsety R1 = pozycje nazw-stringów w regionie indeksu); pomiar końcowy przeszedł wszystkie
asercje. To był błąd PINU (audytora), nie parsera; ujawnione świadomie.

## 3. Z3 — census kwantyfikatorów i narracji (finding A Desktop)

Mechaniczny scan (10 wzorców kwantyfikatorów + wzorzec fraz indykatywnych) po 6 plikach
głównych pakietu R1 + warstwa AUX (PE_MASTER_REVIEW). Wynik maszynowy:
`03_EVIDENCE\Z3_QUANTIFIER_CENSUS.csv` (32 wiersze: plik, linia, fraza, ocena, uzasadnienie,
ref erraty) + RAW + 2×JSON.

- **OVERCLAIM (warstwa główna): 2 unikalne miejsca** — FINAL_REPORT §0 L16 (pełne zakotwiczenie
  mechanizmu → [E-1]) i C_transform C.4 L46 („MUSI przechodzić przez menedżer sceny/modeli" → [E-3]);
  warstwa AUX: PE_MASTER_REVIEW L9 (→ [E-6]).
- **NEEDS_QUALIFICATION (statyczne-vs-runtime): 7 + 2 AUX** — frazy indykatywne „czyta/konsumuje/
  pobierają/wołają" w runie STATIC-ONLY → [E-2].
- Pozostałe 22 trafienia: zgodne z bramkami (OK_FACTUAL/OK_SCOPED/OK_STATIC_CODE_DESC/
  OK_FACTUAL_NEGATIVE) — np. „Kompletna tabela 20 ogniw" (fakt), „od pliku do rejestru" (jawny
  scope byte-locked), „NIE wykonano dekompilacji ciał…" (uczciwa negacja).
- Frazy „pełny łańcuch"/„zawsze"/„cał*": **0 trafień** w pakiecie. STAGE_ACCEPTANCE_GATES.csv:
1 trafienie statyczne OK (plus kosmetyczna literówka „scieyka" — adnotacja, pakiet immutable).

## 4. Z4 — ERRATA_R2 (dokumentacyjna; nowy katalog runu; oryginały nietknięte)

`06_REPORT\ERRATA_R2.md` poprawia [E-1..E-6] (każda pozycja: CYTAT zastępowany 1× + źródło +
nowa treść kanoniczna):
- **[E-1]** (a) kwalifikacja frazy otwierającej §0 FINAL_REPORT do warstw PARTIAL_TO_RESOURCE
  (do żądania = CONFIRMED; fizyczne otwarcie = STRONGLY_SUPPORTED; residuum = ciała
  providera/fabryki);
- **[E-2]** (b) statyczne-vs-runtime: klient ZAWIERA i MOŻE WYKONAĆ reader (statycznie wykazany
  przepływ; brak runtime-observation) — kanoniczne brzmienie dla wszystkich fraz indykatywnych;
- **[E-3]** (c) C.4: kolejność network-first zastąpiona hipotezami neutralnymi konkurencyjnymi
  (H_CLIENT priorytet dla statyków jako KIERUNEK BADAWCZY — world-editor MindArk 2002 +
  precedens DAoC fixtures.csv, jawnie nie-dowód; H2 CLIENT_DERIVED; H_SERVER; H4 HYBRID);
  „MUSI" zdegradowane do hipotezy architektonicznej;
- **[E-4]** (d) mapowanie A na nazwę `<A>.nif`: awans do CONFIRMED z pełnym censusem Z2
  (3,618/3,618; kwalifikatory era/statyka/mechanizm/{typ,id}/kontekst odwrotny);
- **[E-5]** (e) literówka w nagłówku PE_MASTER_REVIEW (brak polskich znaków): poprawiona kopia
  w formie cytatu-linii „## GŁÓWNE PYTANIE P0 — ODPOWIEDŹ"; oryginał nietknięty;
- **[E-6]** (audytor, z census Z3) adnotacja do frazy warstwowej PE-MASTER cytowanej wprost przez
  audyt zewnętrzny (Finding A) — warstwowanie jak [E-1]; pakiet immutable.

Oryginalny pakiet R1: **ZERO zmian** (G4); evidence R1: ZERO zmian; wynik naukowy R1: nienaruszony.

## 5. Bramki (fail-closed)

| bramka | werdykt | dowód |
|---|---|---|
| G1-JOIN | **PASS** | rekomputacja z zapisanych artefaktów (detail CSV) zgodna z JSON (3618/0; 5438; 1666; 1692; tożsamości arytmetyczne); round-trip endianness 0 fail; negative-control 20/20; niezależny byte-scan PASS; census surowy == parser (5596/1865); GATE_CHECKS.json |
| G2-CENSUS | **PASS** | 32 wiersze, kolumna verdict pełna (0 UNASSIGNED), zgodność CSV↔JSON co do wartości |
| G3-ERRATA | **PASS** | każda fraza zastępowana obecna dokładnie 1× w ERRATA_R2 (cytaty); poprawki oznaczone [E-1..E-6]; poprawiona kopia nagłówka 1×; frazy nieobecne w poprawionej narracji (ten raport). Ujawnienie: pierwsza iteracja bramki wykryła duplikat frazy w nagłówku [E-4] — naprawione przed finalizacją (FAIL→PASS; ślad w pinach skryptu) |
| G4-IMMUTABLE | **PASS** | pełny re-hash obu kopii pakietu R1 vs baseline przed startem: 674/674 plików identycznych (0 missing / 0 added / 0 changed) |
| G5-GIT | **PASS** | commit path-limited tylko `docs/audits/PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913\` + `AUDIT_ENTRYPOINT.md`; census ścieżek == dozwolone; push OK; HEAD == origin/master (weryfikacja na końcu raportu w HANDOFF) |
| G6-ENTRYPOINT | **PASS** | AUDIT_ENTRYPOINT.md: dokładnie +1 wiersz, 0 usunięć (git diff numstat: 1/0) |

NON_PASS (GATE_FAIL/SCOPE_CREEP/HASH_MISMATCH): **brak**. HARD STOPS: **brak** (evidence/oryginały/
pakiet historyczny nietknięte; experiments/ EU1030 nietknięte; zero pod-agentów).

## 6. SELF_CHECK + NOT_CHECKED

- [x] Własny walk 5,438/5,438 (0 CRC-fail) + zgodność per-row z S2 R1; własny parser BNT2
      z kalibracją do byte-scanów R1; G1 podwójna rekomputacja; re-run skryptu identyczny.
- [x] Niezależny kontr-check (Z2c) metodą surowego byte-scanu (pełnokorpusowa zgodność census).
- [x] Kontrola negatywna 20/20; endianness round-trip + kotwica surowa + kontrola dyskryminatywna BE.
- [x] Census Z3 maszynowy z ocenami semantycznymi audytora; brak „manufactured findings"
      (22 z 32 trafień oceniono OK — zgodne z bramkami).
- [x] Errata [E-1..E-6] z cytatami zastępowanymi 1×; oryginały nietknięte (G4).
- [x] Skrypty hashowane po ostatniej edycji przed wykonaniem (00_CONTROL\Z2_SCRIPT_SHA256.txt;
      historia re-pinów jawna: poprawki składni + trailer-index + semantyka kalibracji + E-6).
- [ ] NIE wykonano (świadome granice): re-forensyka VA runu R1 (zaufanie warstwie: fresh QC R1
      6/6+~40 + wyrywkowe reodczyty dumpów w tym runie); dekompilacja ciał providera/fabryki
      (residuum GATE-A — open item R1); sekcja E/transform (UNVERIFIED); nie badano payloadów
      .nif/.bvi (zakaz ekstrakcji); nie wykonano joinu reverse z dekodowaniem semantyki wpisów
      (tylko kontekst liczbowy); PE_MASTER_REVIEW.md tego runu = PLACEHOLDER PENDING (werdykt
      MASTER_* orzeka PE-MASTER — audytor nie podpisuje werdyktu MASTER).

## 7. Artefakty

`06_REPORT\artifact_index.csv` (pełny census z SHA256). Kluczowe:
- 01_RAW\Z2_JOIN_RESULT.json; Z2_JOIN_A_TO_NIF_DETAIL.csv (3,618); Z2_JOIN_B_TO_BVI_DETAIL.csv
  (1,666); Z2_NEGATIVE_CONTROL_A.csv (20); Z2_MODELS_BNT_INDEX_NAMES.csv (5,596);
  Z2_VOLUMES_BNT_INDEX_NAMES.csv (1,865)
- 02_ANALYSIS\Z1_CLAIMS_MATRIX.md
- 03_EVIDENCE\Z2C_INDEPENDENT_SPOTCHECK.json; Z3_QUANTIFIER_CENSUS.csv; Z3_QUANTIFIER_HITS_RAW.csv;
  Z3_QUANTIFIER_SCAN_SUMMARY.json; Z3_CENSUS_SUMMARY.json
- 06_REPORT\ERRATA_R2.md; 00_FINAL_REPORT.md (ten plik); GATE_CHECKS.json; HANDOFF.md;
  artifact_index.csv; PE_MASTER_REVIEW.md (placeholder PENDING)
- 00_CONTROL\z2_join_a_models.py; z2c_independent_spotcheck.py; z3_quantifier_census.py;
  z3b_merge_verdicts.py; z4_gates.py; Z2_SCRIPT_SHA256.txt
