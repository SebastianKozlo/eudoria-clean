# REPORT — PE2003_ISO_PAYLOAD_NIF_PLACEMENT_STATIC_R3_20261025

RUN_ID: PE2003_ISO_PAYLOAD_NIF_PLACEMENT_STATIC_R3_20261025 | Autor: Z01 closing (pe-master-auditor) | Data: 2026-10-25
Tryb: AUTONOMICZNA KONTYNUACJA STATYCZNA, natywne Task, GLM default/medium, depth=1, NO_NESTED_TASKS.
Ten raport jest syntezą istniejących wyników (zero nowej nauki). Każde twierdzenie ma fizyczne źródło w jobs\* lub QC\*; pełna macierz: CLAIMS.json (45 twierdzeń, statusy zliczone programowo).

## 0. WERDYKTY (oddzielne)

| Wymiar | Werdykt | Uzasadnienie |
|---|---|---|
| **INTEGRITY** | **PASS** | Wszystkie 15 pinowanych wejść fizycznych re-hashowanych przez Z01: 15/15 MATCH (INPUT_RECHECK.json). Kopie danych do SCIENCE_ROOT weryfikowane hashami (ISO_PAYLOAD_INVENTORY == RECOVERED_FILES SHA 2AD7FD9B…; BUILD_COMPARISON D700B5A9…; EXTRACTION_BARRIERS 62B17D6F…). Wyniki fal 1-5 potwierdzone niezależnie przez QC1/QC2 (re-derivacja z bajtów, nie powtórzenie deklaracji). |
| **SCIENCE** | **QC_PASS / ADVISORY** | 45 twierdzeń: 41 CONFIRMED (bajtowe dowody + niezależne re-derivacje), 1 STRONGLY_SUPPORTED, 1 PLAUSIBLE, 1 UNVERIFIED, 1 REJECTED (stara semantyka kolumny P01). Zero promocji LOCAL→WORLD; standing bez zmian; niedostępność danych serwerowych nie konwertowana na wynik negatywny. 2 findings P2 (fale 2-5) + 3 P2 (fala 1) skorygowane przez C01 addytywnie z ERRATA; żadna treść naukowa nie obalona przez findings. |
| **PROCESS** | **PASS z incydentem udokumentowanym** | 15 natywnych Task przed Z01 (+Z01 = 16; limit 96, rezerwa zachowana). Attempt-cap compliant (I02: 2 dead → split lineage do I02a; I02a: próba 2 ok; QC2: próba 2 ok; zero 3. identycznych retry). INC-R3-01 (zmyślona końcówka SHA w promptach I02/I02a-a1, root self-report) — udokumentowany, żadna nauka nie oparła się na błędnym pinie. Obserwacja C01 o braku plików QC_FINDINGS skorygowana (pliki istnieją; Z01 odczytał oba). Z01-DRIFT-01: suma bajtów w RESULT.md I01 odbiega od własnego CSV (+16 461 B) — defekt prozy raportu, odnotowany (jobs\ read-only), nauka nietknięta. |
| **PUBLICATION** | **NOT_PERFORMED (przypisana rootowi, po sealu)** | Z01 nie pieczętuje: SCIENCE_STOP.json i MANIFEST_SHA256.csv pisze root po powrocie (manifest LAST, wyklucza tylko siebie — R2-A06). Publikacja z izolowanego worktree wg R2-A10 po sealu. |

## 1. ŁAŃCUCH DOWODOWY ISO → INSTALLER → BUILD → MODELS → INSTANCE → PLACEMENT

| Etap | Status | Kluczowe fakty | Źródło |
|---|---|---|---|
| ISO (obraz) | CONFIRMED | Pin 884692A8… (670 306 304 B) re-hash MATCH; spacer ISO9660 42 pozycji (29 plików + 13 katalogów); jedyne PE = ProjectEntropia.zip; PROJEC~1.PCG = FWS menu; 0 arków/nifów/bnt na dysku | C-ISO-01/02; jobs\D01 |
| ISO → installer | CONFIRMED | ZIP (4AB9AD40…) → PE_PCG.exe (F74BE3AC…); genuine NSIS gen-2.0-beta (v20b1/b2/b3), firstheader @0x9800, bez tabeli block_header | C-ISO-03; jobs\I01 |
| installer → payload | COMPLETE | 56/56 FILE_RECOVERED_COMPLETE; 53 bloki zero luk → archive_end−4; blok 0x800F03AC = nagłówek 339567.mp3 (stored-bez-NLEN — anomalia rozstrzygnięta jako kompresja); sumy: 54 wiersze z out_size = 163 568 016 B (== niezależna suma QC1); 53 wiersze plikowe = 163 534 578 B; 51 unikalnych nazw (2 duplikaty wpisów); 315 instrukcji vs 53 pliki wyjaśnione | C-INS-01..03; jobs\I01; QC1 |
| payload → build | CONFIRMED — **DIFFERENT_BUILD** | **ISO2003NOV-PE-5.1.0.0** (MindArk, TDS 2003-07-02, UPX) ≠ PE42 3.4.3.1 COT ≠ EU 9.3.5; NO VA TRANSFER; 16 IDENTICAL / 10 DIFFERENT / 30 MISSING; 50.bnt ISO == pipeline ref-A IDENTICAL_BYTES, ≠ teren instalacji PE42 (era-divergent); ISO PE.exe == PE_EU.exe == MindArk1_Patched (kanał web) | C-BLD-01..05; jobs\B01 |
| build → unpack | CONFIRMED | PE.exe: NRV2D_LE32, c_adler 31C626AA + u_adler 6DCC8194 PASS, obraz 2 939 409 B, OEP RVA 0xADFC2, unfilter 52 637/52 637 (ERRATA: c_len=953 767, u_file_size=2 911 351); ClientLoader (m5) + CLUpdater (m2) unpack PASS | C-UPX-01/02; jobs\I02a/I03 |
| build → mechanizmy NIF/placement | CONFIRMED | Reader NIF PRESENT (0x403940/0x403A80/0x415D40); FIELD_ORDER_SAME (bramki 4.1.0.11/4.1.0.12/4.1.0.0 bajtowo identyczne); writer ×100 PRESENT (0x46EA32, const 0x65B648); **id-hash PE42 NIEOBECNY w 5.1.0.0** (0 hitów, kontrola PE42 10/12/1); resource-open VARIANT (hash-bucket vs std::map); mount ark @startup (0x45ED00, open core 0x5B3E70) | C-MEC-01..06; jobs\I02b/D01 |
| build → models (ISO) | **CONFIRMED — SERVER_DELIVERED_ONLY** | ISO+installer = 0 arków; Download.data = „1 PE_PCG.ark"; ClientLoader = pełny FTP (WSOCK32, USER/PASS/CWD/PASV/RETR; pula 217.212.240.131-134, update .43, login .42); FullDat_%d.ark/Dat%d_%d.ark/Lang_%u.ark → ekstrakcja materializuje Models/Textures/Volumes/Scripts.ark; PE_PCG.ark literal nieobecny we wszystkich 3 binariach (konsument = frontier BLK-R3-01/02); modele 296445/218757 NOT_FOUND_IN_RECOVERED_SUBSET | C-SRC-01..04, C-BLD-06; jobs\D01/I03/B01 |
| models → instance | **MISSING_EDGE** | PE42: krawędź resource→instance niewykazana (R2-A04; rodzina ArkBoundingVolumeRenderer nie dowodzi instancji); ISO: brak danych modeli wcale (konsekwencja SERVER_DELIVERED_ONLY) | MODEL_INSTANCE_EDGE_MAP.csv; R2-A04 |
| instance → transform/world | **NOT_ESTABLISHED** | Transformy N01/N02 są MODEL-LOCAL (composed root→część; 26 części niezerowych w 296445, max |t|≈11 291; 7 w 218757, max ≈1 316); konwencja macierzy AMBIGUOUS_DUAL_REPORTED (czułość 3/82); AXIS_UNITS_FRAME=UNCALIBRATED; AUTHENTIC_WORLD_VALUES=NONE; bez promocji (N5) | C-NIF-*, C-N02-*; jobs\N01/N02 |
| placement | **NOT_ESTABLISHED** | Standing bez zmian (patrz §3) | standing |

## 2. WYNIKI FAL (synteza)

- **Fala 1 (I01, N01):** instalator w pełni zmapowany i rozpakowany (INSTALLER_PAYLOAD_COMPLETE); kolejność pól NIF bajtowo rozstrzygnięta (translation @rotation_off−12, PRZED macierzą — kontrmodel „macierz przed translacją" obalony); parser strukturalny 155/155 + 62/62, 0 boundary mismatch; stara kolumna P01 = later triple (38/38, REJECTED); 24/24 testów syntetycznych; properties-vs-children rozstrzygnięte; TriShape transforms nowo zdekodowane (44 bloki, 21 niezerowych).
- **Fale 2-5 (B01, I02a/I02b, D01, I03, N02):** build rozstrzygnięty (5.1.0.0, DIFFERENT_BUILD, REUSE_CERTIFICATE); unpack klienta i loaderów z pełnymi known-answers; mechanizmy NIF/placement 5.1.0.0 rozstrzygnięte (FIELD_ORDER_SAME; id-hash absent — kluczowa negatywna nowość); kanał danych SERVER_DELIVERED_ONLY (FTP + IP 2003); composed transforms MODEL-LOCAL z dual report.
- **QC (QC1, QC2):** oba QC_PASS; 34+35 = 69 itemów, 65 TRUE / 4 FALSE (wszystkie FALSE = defekty transkrypcji/parsowania artefaktów pochodnych); 5 P2 + 5 P3 findings — wszystkie rozdysponowane (C01: 13 korekt in-place + 6 ERRATA; ledger SHA 7C29F5F5…).
- **C01:** korekty addytywne, każda poprzedzona niezależną weryfikacją fizyczną (falsyfikator adler, byte-scan, recompute z CSV); scope_guards zachowane; obserwacja o braku QC_FINDINGS na dysku skorygowana przez roota (pliki istnieją — potwierdzone odczytem Z01).

## 3. STANDING NAUKOWY (obowiązujący, dokładnie)

```
PE2003_WORLD_XYZ_RECOVERED=NO
PE2003_HISTORICAL_PLACEMENT=NOT_ESTABLISHED
SOURCE (edycja ISO)=SERVER_DELIVERED_ONLY dla modeli (terrain LOCAL)
LOCAL_SOURCE_EXHAUSTED=NO (PE42 reference frontier otwarty; ISO edition: dane modeli poza zasięgiem statycznym)
AXIS_UNITS_FRAME=UNCALIBRATED
CANONICAL_GATE_EFFECT=NONE
EXTERNAL_POSTAUDIT=PENDING
ADVISORY
```

## 4. OGRANICZENIA (jawne)

1. **Niezależność sesji/roli, nie modelowa** — wykonawcy i QC to ta sama rodzina GLM (zastrzeżone w QC1/QC2); wszystkie load-bearing fakty re-derivowane z bajtów własnymi narzędziami.
2. **Statyka tylko** — nic nie wykonano; stringi+disasm = capability, nie obserwowany runtime (L1: brak interwencji runtime — run w 100% statyczny).
3. **ISO edition:** dane modeli nieodzyskiwalne statycznie (PE_PCG.ark, serwery 2003); dostępność serwerów/zarchiwizowanych arkuów = PLAUSIBLE, nie pomierzone (C-WLD-04).
4. **PE42:** 135 bloków TYPE_ONLY_ANCHOR i 62 bloki NiTriShapeData poza dekodowaniem; test „w obrębie bryły" UNVERIFIED (C-N02-05); dispatch list natywnie UNRESOLVED; konwencja macierzy dual.
5. **Raport to mapa, nie prawda** — wszystkie tezy prowadzą do fizycznych źródeł (CLAIMS.json); I01 RESULT suma bajtów drift (+16 461 B, Z01-DRIFT-01, kosmetyka prozy).
6. **Coverage** — pełny census tam gdzie deklarowany (56/56, 155/155+62/62, 42 ISO, 56 BUILD_COMPARISON, 82 composed); BOUNDED_INSPECTION narzędzi poza load-bearing (QC coverage); NOT_CHECKED wykazane w QC1/QC2.

## 5. FIRST_MISSING_EDGE

**ISO_PAYLOAD → model_definition**: dane modeli (Models.ark w PE_PCG.ark) nieobecne lokalnie w wydaniu ISO (SERVER_DELIVERED_ONLY) — bez tej krawędzi łańcuch ISO→placement jest statycznie niewykonalny. Dla ścieżki referencyjnej PE42 pierwszą brakującą krawędzią pozostaje **resource→instance** (R2-A04). Pełna mapa: MODEL_INSTANCE_EDGE_MAP.csv.

## 6. NEXT_BEST_EXPERIMENT

**BLK-R3-03 — PE42: deasemblacja konsumentów resource-open (0x51F6E0 get-or-create) i ctor rejestru (registry+0x3C)** w PE2_unpacked_out.exe: jedyne statyczne źródło mogące zamknąć krawędź resource→instance bez danych serwerowych 2003; falsyfikator: żaden konsument nie tworzy instancji z danymi placementowymi. Runner-up: **BLK-R3-04** — geometria NiTriShapeData vs composed offsets (przekształca UNVERIFIED w testowalny wynik; podstawa przyszłej kalibracji AXIS_UNITS). Pełny frontier: FRONTIER.json; backlog: RESEARCH_BACKLOG.json.

## 7. TERMINAL (wg kontraktu)

RUN_STATUS: **COMPLETE (fale 1-5 + QC + korekty + closing Z01)** | SCIENCE: QC_PASS/ADVISORY | PROCESS: PASS (INC-R3-01 udokumentowany) | PUBLICATION: NOT_PERFORMED (root, po sealu) | per-model standing: 296445 i 218757 — WORLD_XYZ_RECOVERED=NO, HISTORICAL_PLACEMENT=NOT_ESTABLISHED, SOURCE(ISO)=SERVER_DELIVERED_ONLY | ISO identity: ISO2003NOV-PE-5.1.0.0, DIFFERENT_BUILD, NO VA TRANSFER, REUSE_CERTIFICATE (teren ref-A + 16 plików) | reuse scope: patrz REUSE_CERTIFICATE B01 + C-BLD-05 | QC origin: QC1+QC2 (sesje pe-master-auditor; niezależność sesji/roli) | CANONICAL_GATE_EFFECT=NONE | EXTERNAL_POSTAUDIT=PENDING | WORLD_XYZ_RECOVERED=NO | HISTORICAL_PLACEMENT=NOT_ESTABLISHED | HARD STOP — bez auto-next; kolejny krok należy do PE-MASTER (seal, potem ew. dispatch BLK-R3-03/04).

*Manifest (MANIFEST_SHA256.csv) dopisuje root jako OSTATNI po SCIENCE_STOP.json — poza zakresem tego raportu.*
