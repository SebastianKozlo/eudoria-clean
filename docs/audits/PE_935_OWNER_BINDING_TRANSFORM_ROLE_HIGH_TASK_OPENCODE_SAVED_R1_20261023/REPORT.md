# REPORT.md
@'

# REPORT — OWNER BINDING / TRANSFORM ROLE / WORLD-INSTANCE RELEVANCE (R1)

RUN_ID = PE_935_OWNER_BINDING_TRANSFORM_ROLE_HIGH_TASK_OPENCODE_SAVED_R1_20261023
ROOT_SESSION = ses_e96065615ffe8p6hDCJJBEade2
ERA = PE_EU_9_3_5_SAVED_ONLY (saved static representations; NO original EXE/assets, NO runtime, NO new Ghidra exports)
CLIENT_HIGH_ATTESTATION = HIGH_CONFIG_CHECK.json: 11/11 ról reasoningEffort=high, registry glm-5-3 high, brak variantów w registry; REQUEST_EFFORT = NOT_OBSERVED; SERVER_EFFECTIVE_EFFORT = UNKNOWN
TASK_ACTUAL_COUNT = 14
INTRUN interventions = NONE (statyczna analiza saved packetów)

## SCIENCE_VERDICT = PARTIAL_PASS_WITH_MATERIAL_CORRECTIONS
## PROCESS_VERDICT = PARTIAL_NONCOMPLIANT (doc_lines breach + reservation overshoots, oba ujawnione)
## BYTE/INPUT INTEGRITY = PASS (authoring 44 files; 610 pinów; snapshot 39; H5/pakiety/discovery re-hash PASS — INPUT_RECHECK.json)
## NATIVE TASKS = 14 (11 workers: 8 DONE + 3 failed-length; 3 auditors DONE; bijection 14/14; zero grandchildren)
## CANONICAL_GATE_EFFECT = NONE

## WYNIKI GŁÓWNE (wszystkie packet-bounded, era PE_EU_9_3_5_SAVED_ONLY)

1. RECEIVER_JOIN (I01; QC: QSCI CONFIRMED): receiver wywołania 0085B3E0@004C488A = zapisany wcześniej pointer pary z lookupu 008544D0 (klucz = dword lokalny, jedyny stack-arg; manager z singletonu 004154F0 per prior VSB-A05). B_at_call = B_lookup wartościowo (store bezwarunkowy 004C4861). B jest polimorficzne (vptr w B+0, metoda slot5 wołana wirtualnie). Gałąź pusta (EAX==0) pomija pracę na parze (JZ@row031→row064; polarność rozstrzygnięta przez QC: carry I01A był CARRY_ERRONEOUS — OBTR-A09).
2. CALLER→QUERY KONTRAKT (R01; QC: QSCR): oba callsites 0085B4D5/0085B56E wołają 00856800 identycznie: R=[EDI+0xC], trio vec3 z lokalów+stałych globalnych, const float (0x00A80594/0x00A7AF9C — wartości NIEZNANE), selector=2, przez 00415570 (klasa RETn0; EFEKT EAX 00415570 = UNVERIFIED — OBTR-A08: ciało nieobecne w H5 ani w katalogu 610 pinów). 00856800 = KOMPLETNY thiscall bool-query wrapper (RET 0x10): wirtualne zapytanie na this->[0x44] vt[0x154] z block32{2,zero,trio,float}; zwraca bool.
3. ROLA R (R01+R02; QC: QSCR, QC_PARTIAL): R = holder/agregator kolekcji polimorficznych elementów (holder @ R+0x2C: vt[0x4C]=licznik, vt[0x50]=tablica; elementy elem->vt[0x8](flaga INWERTOWANA: PRE→1, POST→0) przez 0085C360 = czysty fan-out forwarder, RET 0x4, ciało kompletne, zero zapisów na R). Semantyka booleana elementów = UNKNOWN; domena = NONE_OF_THE_ABOVE. B≡EDI = PLAUSIBLE (def poza oknami).
4. SLOT1/VT+4 (S01+S01B+S02A; QC: QSCI): entries[1] zakotwiczonych tabel A91E4C/A7DCB0 = DATA_BARRIER — 12 saved źródeł wyczerpanych (case (a) wszędzie, pełne denominator: 159 struktur/95 vtable/154 entries/851664B/28296 linii/98 skanów regex; konwencja offset+4 potwierdzona w korpusie tylko dla OBCYCH rodzin; near-miss A91A4C odkonfluowany). Jednocześnie S02A CONFIRMUJE, że wirtualny dispatch PRZEZ VT+4 istnieje w ciele 0085B3E0-family (0085B5CE, this=EDI, args &local + [ESP+0x54], callee czyści 8B) — mechanizm bez targetu.
5. H5 = CZĘŚCIOWY eksport: region 004154xx-004155xx nieobecny (0 wierszy także dla 004154F0); tożsamość this_00856800 pozostaje UNKNOWN.

## STATUSY KONTRAKTOWE
WRITER_OBSERVED = NO (żaden zapis transformu niezaobserwowany w oknach; zapisy tylko przez niewidoczne ciała CALL) | WRITER_SITE = N/A | WRITER_PHASE = N/A
VALUE_PRODUCER = NOT_ESTABLISHED | CTOR_RETURN_VALUE_STATUS = N/A (I02 nie było potrzebne dla receiver proof)
RECEIVER_JOIN = ESTABLISHED (B_lookup=B_at_call, packet-bounded CONFIRMED, QSCI)
REGISTER_LOOKUP_JOIN = ESTABLISHED (key→manager lookup→pair; pochodzenie wartości klucza UNVERIFIED)
MAP_KEY_AND_FLAG_CONTRACT = key=dword lokalny jako jedyny stack-arg lookupu; flagi/typ K_manager vs instance ID nierozróżnialne w pakietach
X_PROVENANCE = X (this_00856800 z 00415570) = UNKNOWN
INSTANCE_ROOT_ROLE = UNVERIFIED | RESOURCE_INSTANCE_JOIN = NOT_ESTABLISHED
TRANSFORM_SOURCE = UNKNOWN | PHYSICAL_SOURCE_MEDIUM = UNKNOWN
FIRST_MISSING_EDGE = wartość entries[1] (VT+4, komórka A91E50/A7DCB4) — cel dispatchu 0085B5CE
WORLD_INSTANCE_RELEVANCE = UNVERIFIED | MODEL_RESOURCE_BINDING = UNVERIFIED | BUILDING_ROLE = UNKNOWN | HISTORICAL_TRANSFORM_PROVENANCE = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO | HISTORICAL_PLACEMENT = NOT_ESTABLISHED | CURSOR_SOURCE_MEDIUM = UNKNOWN

## KOREKTY (CORRECTION_LEDGER OBTR-A01..A12)
Materialne: OBTR-A08 (C-R02 narrowed: RETn0-contract-only, EAX 00415570 UNVERIFIED); OBTR-A10 (C-I06 konsumpcja poszerzona); OBTR-A11 (etykiety slotów stack ±4 — UNVERIFIED detail, joins nietknięte); OBTR-A09 (carry erroneous, rozstrzygnięte przez QC). Procesowe: OBTR-A01 (3x finish=length → protokół iteracyjny + dekompozycja; potem 7/7 zadań DONE); doc_lines breach (INCIDENT seq11: ~32k vs cap 12k — S01B czytał pełne pliki zamiast targeted; werdykt procesowy PARTIAL_NONCOMPLIANT); QSCR overshoot +48 (seq12); QACCOUNT overshoot doc lines (ujawnione). Lower bounds NIE dowodzą cap PASS.

## RELEVANCE / PRIORYTET DALEJ
Fala I/R ustaliła tożsamość receivera i rolę strukturalną R; brak jakiejkolwiek krawędzi placement/instance/resource → branch relevance obniżona dla dalszego rozwoju R-chain bez nowej kotwicy. Pierwsza brakująca krawędź = entries[1] (VT+4). Propozycja minimalnego przyszłego capture (NIE wykonana): saved dumpy LE pokrywające [A91E44..A91E88) i [A7DCA8..A7DCEC) — klasa DWORD_ROSTER-style; ewentualny odczyt fizyczny wymaga osobnej autoryzacji (poza tym kontraktem).

## QC
QSCI = QC_PASS_WITH_FINDINGS (79 rows; 1xP1 stack-labels, 4xP2; carry resolved; barrier spot-check 3/3 zgodny).
QSCR = QC_PARTIAL (228 rows; 1xP1 C-R02 overclaim → corrected; 1xP2; 4xP3; korekty zastosowane w CLAIMS).
QACCOUNT = PASS_WITH_FINDINGS (algebra domknięta; reklasyfikacje zastosowane; UNMEASURED nie awansowane; call_units adjudication: +6 ACCEPTED, +7 REJECTED — R01B unread).

## NIE WYKONANO / NIE SPRAWDZONO
Oryginalny EXE/assets (stat/hash/runtime) — zakazane kontraktem; SDK source — 0 ekspozycji (brak claimu propagation do kontrpróby; G01 NOT_EXERCISED, polityka ENGINEERING_REFERENCE_ONLY); pakiet R01B (00856900..008569FE, 89 rows) — wycięty i przypięty, NIE czytany (poza ciałem 00856800; brak pytania wymagającego); luki ciała 0085B3E0 (85B3E0..85B48D, 85B4DA..85B522, 85B570..85B5BC) — nieanalizowane; wartości stałych float (0xA7B508/0xA7B2D0/0xA79818/0x00A80594/0x00A7AF9C) — NIEZNANE (brak odczytu danych oryginału); runtime-effort dzieci — UNMEASURED.

RAPORT STATUS = REPORTED_PENDING_EXTERNAL_POSTAUDIT; bez samodzielnego awansu kanonu.
