# ROUND_REPORT — PE_935_STATIC_PLACEMENT_ROUND1 (runda statycznego placementu EU 9.3.5)

- **RUN_ID**: PE_935_STATIC_PLACEMENT_ROUND1_CLOSURE_20260913 (RUN_CLASS: MATERIAL; domknięcie rundy)
- **Data**: 2026-09-13. **Era**: EU 9.3.5 (pcg_install). Binarium Entropia.exe SHA256
  E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (8,015,872 B,
  image base 0x00400000, brak ASLR — asercja S0 fail-closed wszystkich runów).
- **Raport integracyjny rundy**: konsumuje raporty runów 1–4 + QC rundy + kanon;
  NIE re-deriwuje pomiarów (numeracja i dowody w pakietach runów, patrz §8).
- **Runy rundy** (wszystkie opublikowane, path-limited):
  1. PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913 (commit d1a036d) — macierz A–E + PEŁNY JOIN A↔`<A>.nif` + ERRATA_R2 [E-1..E-6]; INTERNAL_QC/PE-MASTER: MASTER_ACCEPTED (advisory).
  2. PE_935_EXTERNAL_SOURCES_MATRIX_R1_20260913 (commit e8b8ba0) — macierz 24 wierszy źródeł zewnętrznych (23 claimy kontraktowe); MASTER_ACCEPTED (advisory).
  3. PE_935_STATIC_INSTANCE_TRACE_R1_20260913 (commit 4d4cde5) — jak kod tworzy instancję statycznego obiektu świata; QC_PASS (3×P3 → amendments CLOSURE); MASTER_ACCEPTED (advisory).
  4. PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913 (commit 6ab6290) — KTO i Z JAKICH DANYCH produkuje transformy rekordów placementu statyków; QC_PASS (2×P2 + 3×P3 → amendments CLOSURE); MASTER_ACCEPTED (advisory).
- **QC rundy**: PE_935_ROUND_QC_STATIC_PLACEMENT_R1_20260913 — QC_PASS dla obu runów
  nośnych (RUN A: 0×P0/P1, 3×P3; RUN B: 0×P0/P1, 2×P2 + 3×P3); wszystkie twierdzenia
  nośne potwierdzone niezależnie bajtowo (własny parser PE, censusy, dumpy regionów);
  amendments dokumentacyjne wykonane w CLOSURE (sekcje AMENDMENT (QC) w plikach
  raportów runów 3/4; evidence NIETYKANE — hashe przed/po w MANIFEST_SHA256.csv rundy).

---

## 1. KRÓTKA ODPOWIEDŹ

**(a) Definicja→model = CODE-CONFIRMED (join 3,618/3,618).** Rekord template'u
(Parameters\templates.vfs; parser A→+0x08 @0x00730CE6) konsumuje pole A jako id
modelu: żądanie {0x66=MODEL, id=A} przez ArkResourceManager (RUN R1) oraz pełne
odwzorowanie A→`<A>.nif` w Models.bnt: **3,618/3,618 unikalnych niezerowych A,
0 braków** (per-record 5,438/5,438; bonus B→`<B>.bvi` 1,666/1,666) — RUN1, niezależnie
potwierdzone przez PE-MASTER (własny parser BNT2) i kontr-check surowym byte-scanem.

**(b) MECHANIZM: instancja statyczna = rekord placementu z transformami czytanymi
WYŁĄCZNIE z drzewa atrybutów + instancja modelu przez resource-system + system
CWO/ArkObject; templates-lookup NIE jest ścieżką statyków (0/38 — tylko avatar/UI).**
Pełny łańcuch maszyny placementu jest VA-locked: transform wchodzi do rekordu
placementu (pozycja@+0x08 FUN_00730f90, rotacja@+0x14 FUN_00730fb0, FUN_00730fd0
@+0x20/+0x24) wyłącznie z klienckiego drzewa atrybutów (FUN_00846840; ID
0x6A4/0x6A5/0x6A8/0x6A9; pary wg FUN_00846430; test adversarialny QC: 15
setter-callerów — ZERO kontrprzykładów); builder FUN_00567770 (3 napędy przez
FUN_00567c50), ctor rekordu FUN_00730700, most template→encja ArkObject
FUN_00726e70 (A→encja@+0x28), kreator instancji modelu FUN_006cb6f0 →
ArkModelResourceInstanceRef → instancja nazwana "<id>__<name>" (FUN_006cb020) →
kolejka pending-attach FUN_006cb3c0. Powierzchnia templates-lookup/pump (25+13
call-site'ów, klasyfikacja 38/38 bajtowo): **0/38 STATIC_WORLD** — tylko
avatar/UI/maszyna/vegetation (RUN3); statyki NIE przechodzą przez te call-site'y.

**(c) DANE HISTORYCZNE: producent transformacji = UNKNOWN-WITH-EXACT-BOUNDARY.**
Kanał FILE: infrastruktura istnieje (store "Data\Parameters" FUN_0094dfc0/FUN_0094fe00
+ parsery VFS), ale **pliku-placementów brak** (Portals.bnt/.prt = czysty dPVS
cell-graph — 276/276, 0 duplikatów, 0 anchorów na WSZYSTKICH offsetach per QC;
20006.vfs nie istnieje mimo dokładnie 29 imm32 0x4E26 w .text). Kanał NETWORK:
łańcuch 0xB9 istnieje i jest rozkodowany bajtowo (CommunicationSubsystem → executor
→ case 0xB9 → FUN_005b72c0 → FUN_00567c50 → FUN_00567770); komunikat 0xB9 niesie
KLUCZE, nie transformy. Hipotezy: **H2 = warstwa propagacji (udowodniona), H1 bez
pozytywu, H3 nieudowodniona, H4 nie wykluczona** (0xB9 = główny otwarty kandydat).
**Historyczny placement 296445 nadal NIEODZYSKANY** — pozycja konkretnego budynku
(296445) pozostaje nieznana; producent atrybutów = główna niewiadoma.

---

## 2. AUDYT WCZEŚNIEJSZYCH TWIERDZEŃ (macierz A–E + erraty + rozstrzygnięcia QC)

| twierdzenie (z pakietu R1) | adjudykacja rundy | podstawa |
|---|---|---|
| A — pole A konsumowane jako id modelu | **ACCEPTED (STATIC-QUALIFIED)**: CONFIRMED, kwalifikacja STATIC-ONLY | RUN1 Z1; RUN3 re-walidacja (parser, getter FUN_007ce1e0, pump) |
| B — A→`<A>.nif` w sprawdzonych przypadkach | **ACCEPTED**: CONFIRMED (byte-proof) | RUN1 Z1/Z2c; RUN3 (Models.bnt skany nazw, E.7) |
| C — pełne odwzorowanie wszystkich A | **ACCEPTED-UPGRADED (JOIN)**: CONFIRMED pełnym mianownikiem 3,618/3,618 | RUN1 Z2 (nowy pomiar; kontr-check PE-MASTER 25/25 + negatywy 25/25) |
| D — pełny łańcuch do fizycznego odczytu | **REJECTED-as-worded**; warstwy: do żądania zasobu = CONFIRMED; fizyczne otwarcie = STRONGLY_SUPPORTED (nie instruction-closed); PARTIAL_TO_RESOURCE stoi | RUN1 Z1; residuum: ciała wirtualne providera/fabryki |
| E — world transform instancji | **UNVERIFIED** (runda 3/4 częściowo domyka: settery rekordu + drzewo atrybutów VA-locked; łącze rekord↔węzeł NIF statyka nadal nieudowodnione) | RUN3 §5; RUN4 §1 |

- **Network-first RETRACTED jako ZAŁOŻENIE** (ERRATA_R2 [E-3] RUN1): zastąpiony
  hipotezami neutralnymi (H_CLIENT/H2/H_SERVER/H4) z H_CLIENT jako kierunkiem
  badawczym (wspartym wzorcem zewnętrznym, NIE dowodem).
- **„FUN_006b4c50 avatar" — CONFIRMED** (RUN3 Z2a: jedyny caller FUN_006b9970 czyta
  węzeł "CharacterPosition"; QC A2: bajtowo, 1 caller, 0 imm32-xrefów).
- **Trzy wzorce 4508 = disp32 — trop ZAMKNIĘTY** (RUN3 Z3: 2× LEA ECX,[ESP+0x119C]
  w FUN_0052d6d0 + wyzerowanie pola w ctorze ArkCommunicator; pełny skan .text:
  4508 LE = dokładnie 3, BE = 0, 296445 = 0 → hardcode template'u w .text NIE ISTNIEJE).
- **Poprawki P2 QC (wykonane jako AMENDMENT (QC) w CLOSURE)**: (P2-1) census 53
  call-site'ów FUN_00845f70 — 48 w rodzinie world-object (0x0043–0x0051), 5 poza
  (w tym handler 0xB9 — WZBOGACA H4); (P2-2) indeks Portals.bnt ma 4-bajtowy
  nagłówek licznika (u32 276 @73218) — **276 unikalnych, 0 duplikatów**; okno
  505k–510k = **19 wpisów** (z 507165). P3 (AABB 382811 = −6.005/+6.005/−2.374/
  +2.498/+3.812; 27 plików .vfs; etykiety siły dowodu dla „dynamic boost::bind";
  adnotacja S9 models_bnt_name_check; doprecyzowanie VA wierszy rejestru) — j.w.

---

## 3. MACIERZ ŹRÓDEŁ ZEWNĘTRZNYCH (RUN2)

Pełna macierz: `99_Audits\PE_935_EXTERNAL_SOURCES_MATRIX_R1_20260913\02_ANALYSIS\CLAIMS_MATRIX.md`
(+ claims_matrix.csv/json; 24 wiersze / 23 claimy kontraktowe: 21 CONFIRMED,
1 STRONGLY_SUPPORTED, 2 UNVERIFIED z udokumentowanymi próbami). Streszczenie 5 wierszy:

| # | źródło | status | istota |
|---|---|---|---|
| 1 | MindArk world editor 2002 (A1/A2) | **CONFIRMED** | Kajsa Högberg "World Creator" (newsletter 2002 przez Worthplaying) autoruje heightfield/tekstury/wegetację „including the cities" w edytorze świata; CGW 2003: osobni artyści statyków. Limit: dowodzi PROCESU autorowania, NIE lokalizacji storage wyniku (klient/serwer/oba). |
| 2 | DAoC fixtures (B1/B3/B4/B6; B5 fork) | **CONFIRMED w 3 niezależnych liniach** | klienckie nifs.csv (ID→NIF) + fixtures.csv (id/nif/name/XYZ/angle/scale/...) parsowane verbatim w kodzie (MapCreator 073a594, daoctocrysis 3e98846, DaocNavMesh 206c328; OpenDAoC-BuildNav = deklarowany fork Uthgard). Wzorzec poszukiwawczy, ZERO transferu formatu. |
| 3 | OpenMW/MWSE separacja (C1–C3) | **CONFIRMED (wzorzec, nie obowiązek)** | base-record bez lokacji vs instancja z position/rotation/scale (0/1/N na base) — dokumentacja jednej rodziny silników, NIE obowiązkowy standard ery Gamebryo. |
| 4 | DoL/WarEmu create-object (D1/D2a/D3) | **CONFIRMED z kodu** | F_CREATE_STATIC=0x71 (WarEmu, verbatim) i create-family DoL tworzą INTERAKTYWNE encje serwerowe (drzwi/questy/loot; GameObject:Unit z rodzeństwem Door/Item/PQuestObject/...); w OBU ekosystemach statyczne miasta są CLIENT-SIDE (DAoC: fixtures.csv). RoR post (D2b) UNVERIFIED (7 udokumentowanych prób). |
| 5 | EU 10.4 (E1) + historia BNT/NiArk (F1/F2/F4/F5) | **CONFIRMED / ograniczone** | post EU10.4 = GRACZ „Wody" (nie MindArk); Sectors.xbc 129 B — za małe na tabelę placementów, ciągłość nazwy ≠ ciągłość formatu; historia BNT/NiArk (PerlMonks 2005, xennex 2007, sinkillerj 2020, PyFFI) CONFIRMED — praca społeczna nigdy publicznie nie doszła do semantyki placementów; PEBNTView (F3) UNVERIFIED (8 udokumentowanych prób). |

Notka F6 (pierwszeństwo) zapisana: z braku wyników NIE wykonuje się twierdzeń o
pierwszeństwie odkrycia; UNVERIFIED = zdania o DOSTĘPNOŚCI z tego środowiska (2026-09-13).

---

## 4. KLASYFIKACJA KONSUMENTÓW (RUN3: tabela 25 lookup + 13 pump = 38 call-site'ów)

Pełna tabela z dowodami: `99_Audits\PE_935_STATIC_INSTANCE_TRACE_R1_20260913\02_ANALYSIS\Z2_CLASSIFICATION_TABLE.md`
(census 38/38 bajtowo, 0 mismatch; QC A3/A4: pełny niezależny census identyczny co do adresu).

| klasa | call-site'y (z 38) | uwagi |
|---|---|---|
| **STATIC_WORLD** | **0** | wynik negatywny rundy: NO_STATIC_CONSUMER_FOUND na powierzchni templates-lookup + pump |
| AVATAR_EQUIPMENT | 9 (6 funkcji: FUN_00511070, FUN_0043eae0, FUN_006b28e0, FUN_006b4c50, FUN_006bc8e0, FUN_006e2610) | w tym body-set FUN_006b4c50 (pump #7-8) — ROZSTRZYGNIĘTA = avatar |
| MODEL_MACHINERY | 8 | emiter pary {0x66,A}, twórca instancji FUN_006cb6f0 (pump #4), gettery modelu |
| OTHER (system atrybutów / ctor-y / gettery tabelaryczne / derived) | 17 | w tym rekordy derived z transformem (FUN_00567170, FUN_005b5f90), gettery slotów body-set, resolver referencji template'owych |
| PREVIEW_UI | 2 | obiekty UI z template'em (FUN_0067b800, FUN_0067c7c0) |
| VEGETATION | 1 | FUN_0094b1d0 (stringi verbatim ArkVegetationClient) |
| UNKNOWN | 1 | pump #5 FUN_0093be20 (hardcode 0x70D17=460563; „460563.nif" NIE istnieje lokalnie — negatyw udokumentowany) |

**FUN_006b4c50 = AVATAR body-set** (jedyny caller FUN_006b9970 = update postaci czyta
węzeł „CharacterPosition"; upstream FUN_00489810 = setup lokalnego avatara). Kontrola
negatywna generyczności: zero stałych 296445/4508 w .text. Redirect rundy: statyki
ładowałyby modele przez system ArkObject + atrybuty + CWO, NIE przez te 38 call-site'ów.

---

## 5. REJESTR NOWYCH ADRESÓW

- **RUN3: ~50 VA własnych tego runu** — pełna lista: `06_REPORT\HANDOFF.md`
  (sekcja NOWE VA) + rejestr dowodowy `03_EVIDENCE\VA_EVIDENCE_REGISTRY.md`
  (każde twierdzenie → era/hash → VA/instrukcja → artefakt; E.1–E.8).
- **RUN4: ~30 VA własnych tego runu** — pełna lista: `06_REPORT\HANDOFF.md`
  (Kluczowe nowe VA per Z1–Z4) + `03_EVIDENCE\VA_EVIDENCE_REGISTRY.md`;
  **S14_VA_EVIDENCE.json = 64 cytowanych VA, 64/64 zweryfikowanych bajtowo przez
  QC (B1: własne mapowanie VA→file-offset + surowe bajty zgodne 64/64,
  qc_addr_lock_runB.json)** — kompletny zestaw VA cytowanych w HANDOFF RUN4.
- Kluczowe rejestry runu (punkt wejścia audytora): RUN3 — ctor ArkObject
  FUN_00726e70 @0x00726E70 (A→encja@+0x28), twórca instancji FUN_006cb6f0
  @0x006CB6F0, settery placementu FUN_00730f90/fb0/fd0/f60, reader atrybutów
  FUN_00846840 @0x00846840 (switch 0x6A4-family), NiAVObject::GetViewerStrings
  FUN_007c04f0 (oracle offsetów); RUN4 — setter atrybutów FUN_00845f70
  @0x00845F70 (53 call-site'y), builder FUN_00567770/FUN_00567c50, handler 0xB9
  FUN_005b72c0, executor FUN_004b15f0/Execute FUN_004b2950/dispatch FUN_004b18d0
  (0xA2–0xC6; case 0xB9 rozkodowany bajtowo), tabela handlerów CWO-Logic
  @0x00A7D764 (16 wpisów; wpis [5] = FUN_00514EF0 @0x00A7D778 — jedyny DATA-ref),
  tabele 0x00A7D8EC/0x00A7DA34 (74/72), parsery VFS FUN_00972df0/FUN_00730c90,
  store "Data\Parameters" FUN_0094dfc0/FUN_0094fe00.

---

## 6. DIAGRAM: źródło danych → instancja → model → world transform

(Krawędzie NIEUDOWODNIONE oznaczone JAWNYM prefixem [NIEUDOWODNIONA];

```
[ŹRÓDŁO: NIEZNANE — kanał FILE (brak pliku-placementów w przebadanym zakresie)
 | kanał NETWORK 0xB9 (łańcuch istnieje; niesie KLUCZE; producent atrybutów
  NIEUSTALONY — GŁÓWNA NIEWIADOMA)]
   → drzewo atrybutów (FUN_00845f70 setter; FUN_00846840 getter; ID 0x6A4/0x6A5/0x6A8/0x6A9 pozycja/rotacja)
   → rekord placementu (settery FUN_00730f90/@+0x08, FUN_00730fb0/@+0x14)
   → system CWO/ArkObject (ArkClientWorldObjectManager; instancja świata)
   → [KRAWĘDŹ NIEUDOWODNIONA: łącze rekord↔model dla statyków]
   → instancja modelu przez resource-system (FUN_006cb6f0 → <id>__<name> → attach)
   → template 4508 → A=296445 → 296445.nif
     [to działa TYLKO dla ścieżek avatar/UI na powierzchni lookupu;
      dla statyków ścieżka ID = otwarta]
```

Diagram łączy wyniki RUN3 §7 (łańcuch instancji) i RUN4 §5 (kanały producenta);
krawędzie (a)–(e) NIEUDOWODNIONE w RUN3/RUN4 pozostają otwarte: łącze
rekord-placementu z węzłem NIF statyka, producent kontenera atrybutów, konkretne
callery wirtualne, semantyka liczbowa D=124.941, fizyczne otwarcie .nif
(STRONGLY_SUPPORTED — errata R2).

---

## 7. MANIFEST PRZESZUKANEGO ZAKRESU I WYŁĄCZEŃ

**Korpus danych (pcg_install EU 9.3.5):**
- templates.vfs — pełny walk 5,438/5,438 rekordów do EOF, 0 CRC-fail (RUN1; QC R1
  rekomputacja); join do Models.bnt 3,618/3,618.
- Models.bnt (395,412,868 B; 5,596 wpisów .nif) + Volumes.bnt (1,865 .bvi) — indeksy
  BNT2 parsowane własnym parserem (RUN1); skany nazw z terminatorem 0x0A (RUN3 E.7;
  uwaga QC P3-1 [RUN A]: blok models_bnt_name_check w S9_BYTE_VERIFY.json = skan
  z błędnym terminatorem, wyniki void — wiążący jest skan E.7).
- **Wszystkie pcg/Data LE+BE** (errata R1-errata: censusy w obu endianness) —
  terrain rozłożony (TDF/TEZ poza zakresem tej rundy); **Portals.bnt 276/276 z
  DEKODOWANYM indeksem** (nagłówek licznika u32 276 @73218 — korekta QC P2-2;
  boundary 0 naruszeń; rozmiary 42–1990 B) = **czysty dPVS cell-graph** (negatyw
  13 anchorów × 276 payloadów = 0 trafień, skan po WSZYSTKICH offsetach per QC —
  domknięty caveat „aligned-only"); Strings payloady NIE przeszukane — szyfrowane;
  .prt payload struktura: sample dumpy (parser grafu FUN_00852750; u16@0=0x0101
  we wszystkich 276 próbkach; AABB f32 w sub-bloku grafu); **20006.vfs nie
  istnieje** (27 plików .vfs w Data\Parameters: 18× 20xxx + 24007 + 8 nazwanych —
  korekta QC P3-2 [RUN B]); **20xxx.vfs NIE zdekodowane formatowo** (kandydat
  eksperymentu nr 1 — patrz §10); TerrainEditZones.bnt (54,156 B) NOT_CHECKED
  (bez zmian RUN3).

**Kod (binarium Entropia.exe 8,015,872 B):**
- RTTI census 1,970 type-descriptorów (483 Ark + 253 Ni + 592 boost) — **9.3.5 NIE
  MA Sector/Region/Entity** (0 trafień; census + surowy grep QC); cell space =
  wyłącznie ArkPortalCell (dPVS); 41 klas TD→COL→vtable.
- Censusy imm: 20005=8, 20007=10, 24007=32, **20006 (0x4E26)=29** (anomalia:
  plik nie istnieje), 0xB9=71 sklasyfikowane (0 zasilających executora — QC),
  0x6A4/0x6A5/0x6A8/0x6A9 (atrybuty transformu) + pułapki offsetowe wykluczone.
- Klasyfikacja 38 call-site'ów (lookup/pump; 0 STATIC_WORLD); 53 call-site'y
  FUN_00845f70 (48 world-object + 5 poza — korekta QC P2-1); censusy setterów
  (FUN_00730f90: 15, FUN_00730fb0: 11, FUN_00730fd0: 7, FUN_00730f60: 21);
  gettery D: FUN_0048ada0 116, FUN_00861240 10 (censusy QC).
- Backward slice'y: S-A (transform-setter ← builder ← atrybuty) i S-B (kreator
  instancji) VA-locked z granicami; 3 napędy buildera (A/B/C per RUN4); dispatch
  0xB9 rozkodowany bajtowo (ADD EAX,−0xA2; byte-table@0x004B1B3C[0x17]=0x0C;
  jump-table@0x004B1AE4[12] → CALL @0x004B1A16 — dekod QC).
- **Granice NOT_CHECKED (jawne, z QC)**: 11/26 callerów ctora FUN_00730700 bez
  setterów (semantyka nieznana); pełna dekompilacja FUN_0084f7a0; pole aux int64
  indeksu BNT; komplet ciał wirtualnych rejestru klas; pełna mapa tabel
  CWO-Logic 0x00A7D8EC/0x00A7DA34 (74/72 — nagłówki i liczby zweryfikowane,
  semantyka każdego wpisu poza zakresem); FUN_0052d6d0 (44 KB, timeout Ghidry);
  runtime (klient/sieć/mock) — ZAKAZANY w tej rundzie (STATIC-ONLY).

---

## 8. SKRYPTY/LOGI (odsyłacze per run)

- **RUN1** `99_Audits\PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913\00_CONTROL\`
  (z2_join_a_models.py, z2c_independent_spotcheck.py, z3_quantifier_census.py,
  z3b_merge_verdicts.py, z4_gates.py, z5_manifest.py + piny Z2/Z3_SCRIPT_SHA256.txt —
  hash skryptu pinowany po ostatniej edycji PRZED wykonaniem, post-run hash == pin);
  wyniki: 01_RAW (JOIN detail CSV 3,618/1,666; negative control 20), 03_EVIDENCE
  (censusy Z3, spotcheck Z2c).
- **RUN2** `...\PE_935_EXTERNAL_SOURCES_MATRIX_R1_20260913\00_CONTROL\`
  (z1_matrix_consistency.ps1 + VERIFY_PROCEDURES.md); materiał źródłowy 01_RAW
  (10 plików cytatów/kodu z commitami); macierz 02_ANALYSIS (CSV+JSON+MD; G4:
  24==24); manifest 03_EVIDENCE\MANIFEST_SHA256.csv.
- **RUN3** `...\PE_935_STATIC_INSTANCE_TRACE_R1_20260913\00_CONTROL\` (s0–s9, ga1–ga8;
  SCRIPT piny w GHIDRA_LOCAL_MANIFEST_SHA256.csv + logi Ghidry w 01_RAW\ghidra_output);
  **qc_probe** (narzędzia własne QC RUN A: qc_pe.py, qc_scan_text.py, qc_xref.py,
  qc_region_dump.py, qc_setter_census.py, qc_b3_sample.py, qc_b6_bound.py,
  qc_final_bytes.py, qc_a6_switch.py, qc_a10_b9.py, qc_bounds2.py, qc_addr_lock.py
  [+ qc_addr_lock_runA.json]) — publikowane z CLOSURE.
- **RUN4** `...\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913\00_CONTROL\` (s0, s4b–s14,
  zs1–zs10, build_manifest.py; SCRIPT_SHA256.csv — każdy skrypt z hashem; 10 tur
  Ghidry z logami analyzeHeadless w 01_RAW\ghidra_output); **qc_probe** (RUN B:
  jw. + qc_b2_exclusive.py, qc_b2_b12.py, qc_b8_portals.py + qc_addr_lock_runB.json
  [64/64]) — publikowane z CLOSURE.
- **QC rundy**: QC_REPORT.md w 06_REPORT obu runów nośnych (RUN A + RUN B; pełne
  punkty A1–A10/B1–B12, FINDINGS z P0/P1/P2/P3, NOT_CHECKED, hashe evidence).

---

## 9. OTWARCI KANDYDACI (ranking wg wartości; z dowodem, którego każdy wymaga)

| # | kandydat | dowód potrzebny | status |
|---|---|---|---|
| 1 | **Producent atrybutów 0xB9** (kto FIZYCZNIE wypełnia kontener atrybutów statyku danymi pozycji) | runtime (offline-probe drzewa atrybutów; human-gated) LUB domknięcie statyczne przez enumerację rejestracji kanałów (wyczerpana statycznie — patrz QC B6: Execute 0 callerów, enqueue 1, dispatch 2 wewn., 71 imm 0xB9 sklasyfikowane, 0 zasilających; bind-hunt 0) | H4 nie wykluczona — 0xB9 = główny otwarty kandydat |
| 2 | **Formaty 20xxx.vfs/24007.vfs** (32 imm 24007; 18 plików 20xxx; szew parser→drzewo atrybutów) | CZYSTO STATYCZNE: dekod formatowy + trace parser→insert-map (najwyższa wartość bez runtime — patrz §10) | H1/H2-closure możliwe bez uruchamiania klienta |
| 3 | **Anomalia 20006/0x4E26** (29 użyc imm32; plik NIE istnieje) | co robi kod przy braku pliku? (census czytników + wartości; mikro-run) | zagadka otwarta |
| 4 | **Pełna mapa tabel CWO-Logic 0x00A7D8EC/0x00A7DA34** (74/72 wpisów) | dekompilacja handlerów + typy komunikatów świata (dopełnia executora 0xA2–0xC6) | nagłówki/rozmiary zweryfikowane; semantyka wpisów otwarta |
| 5 | **Pole D (124.941 przy 4508)** | runtime (semantyka liczbowa: promień/level/selektor wariantu — statycznie nierozstrzygalne, G4 boundary) | gettery VA-locked; semantyka RUNTIME-UNOBSERVED |
| 6 | **11/26 callerów ctora FUN_00730700 bez setterów** (QC NOT_CHECKED) | klasyfikacja semantyczna (czy budują rekordy-placement innymi ścieżkami) | brak kontrprzykładu dla ścieżek prześledzonych |

---

## 10. JEDEN NASTĘPNY EKSPERYMENT (STATYCZNY, bez runtime)

**„FORMAT-DECODE 20xxx.vfs + SEAM parser→drzewo atrybutów"**

1. Zdekodować rodziny 200xx/24007.vfs (format ArkVFS02; store "Data\Parameters";
   parsery: FUN_00972df0+ reader VFS, parser kursorowy FUN_00730c90 — rodzina
   używająca helpera FUN_0040de60 wspólnego z kolejkami komunikatów).
2. Ustalić, które parsery zasilają drzewo atrybutów (szew: writerzy FUN_00845f70
   vs kontenery ArkParameterContainer; klucze u32 → mapa managera FUN_008544d0).
3. Sprawdzić, czy atrybuty transformu 0x6A4/0x6A5/0x6A8/0x6A9 są PERSYSTOWANE
   w którejkolwiek z 27 rodzin Parameters (kandydat H1/H2-closure bez
   uruchamiania klienta).
4. Kontrola negatywna: round-trip endianness przed każdym skanem; kalibracja
   parsera przeciw znanym kotwicom (jak RUN1/RUN4); granice NOT_CHECKED jawne.

**Alternatywa (human-gated)**: runtime offline-probe (Frida na FUN_00845f70 /
FUN_00846840 / handler 0xB9 przy starcie klienta BEZ sieci) — rozstrzyga H3/H4
dla ścieżki dynamicznej; wymaga autoryzacji człowieka (zakaz runtime w tej rundzie).

---

## OCENY OSOBNO (zlecenie §13, koniec — cztery oceny oddzielone od twierdzeń)

1. **Jakość weryfikacji źródeł zewnętrznych: WYSOKA** — klony repozytoriów z SHA
   (commit + plik + linie dla każdego cytatu), verbatim quotes/kod, 21/24
   CONFIRMED z dowodem, 2 UNVERIFIED z udokumentowanymi próbami dostępu
   (RoR post 7 prób; PEBNTView 8 prób) — uczciwe, bez konfabulacji; notka F6
   (pierwszeństwo) zapisana.
2. **Łańcuch ładowania modelu: CONFIRMED do żądania zasobu** (rekord template →
   pole A → żądanie {0x66, A} → provider-chain — VA-locked, join 3,618/3,618);
   **STRONGLY_SUPPORTED do fizycznego otwarcia** (RTTI + rejestracja .nif +
   reader BNT2 + data-binding; residuum: ciała wirtualne providera/fabryki —
   PARTIAL_TO_RESOURCE).
3. **Mechanizm instancjonowania: CONFIRMED** (rekord placementu + drzewo
   atrybutów + resource-system: settery/ctor/buildery/twórca instancji/kolejka
   attach — wszystko VA-locked i niezależnie potwierdzone przez QC);
   **NIEZNANE: łącze rekord↔model dla statyków** (0/38 STATIC_WORLD na powierzchni
   lookupu; krawędź jawna) oraz producent atrybutów (GŁÓWNA NIEWIADOMA).
4. **Odzyskanie historycznych placementów: NIE** — pozycja 296445 nadal
   NIEODZYSKANA; producent danych transformu UNKNOWN-with-exact-boundary;
   kanały FILE (brak pliku-placementów) i NETWORK (0xB9: łańcuch istnieje,
   niesie klucze, producent nieustalony) oba otwarte; H2 domknięta jako warstwa
   propagacji istniejących wartości.

---

## NOTA KOŃCOWA (granice raportu rundy)

- Raport integruje; pełne dowody w pakietach runów 1–4 + QC. Każde twierdzenie
  nośne ma w pakiecie źródłowym surowe bajty (dump/census/JSON) i asercję ery.
- Status PE-MASTER: PROVISIONAL_UNTIL_QUALIFIED — werdykty MASTER_ACCEPTED tej
  rundy są advisory (CANONICAL_GATE_EFFECT=NONE); promocja kanoniczna i domknięcie
  milestone pozostają pod bramką ludzką/external-review.
- Evidence wszystkich runów NIETYKANE w CLOSURE (patrz MANIFEST_SHA256.csv:
  hashe przed/po; jedyna para zmieniona = pliki amendmentsów dokumentacyjnych).
