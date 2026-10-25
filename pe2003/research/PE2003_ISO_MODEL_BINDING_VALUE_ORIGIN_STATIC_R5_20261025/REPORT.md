# REPORT — PE2003_ISO_MODEL_BINDING_VALUE_ORIGIN_STATIC_R5_20261025 (draft pakietu SCIENCE, closing child)

RUN_ID: PE2003_ISO_MODEL_BINDING_VALUE_ORIGIN_STATIC_R5_20261025
BUILD: ISO2003NOV_PE_5_1_0_0 (image section1.bin SHA256 D43A23B9EFCFC9BC4092B38FA3C73499DE7DE7B03B20F34478B9E81EE8893631, size 2939409, VA=0x401000+blob_offset; PE.exe 46B68741568D09664D8B0152E19FF765DFD562A8FF4BE32664E867971D55BB32)
DATE: 2026-10-25
AUTHOR: pe-master-auditor (closing child, STATIC_ONLY, NO_NESTED_TASKS, depth 1). DRAFT — root (PE-MASTER) pieczętuje STOP i MANIFEST; ten plik nie zastępuje SCIENCE_STOP ani MANIFEST_SHA256.csv.
PROVENANCE: konsolidacja jobs/A01,A01R,J01,J02,J03,J04,J05,D01,D02,D03,D04 + QC/QC1,QC/QC2 + CORR1 (WORK_ROOT); 00_CONTROL/*, BODY_ADMISSION_EVENTS.jsonl, BUDGET_LEDGER.json (SCIENCE_ROOT); AUTHORING ROOT REV2 (CONTRACT.md, PA_RECONCILIATION.md, FINDINGS_R4.json, EXTRA_PA/*); frozen postaudity wg pinów. Pełna lista użytych wejść z SHA: INPUT_RECHECK.json (osobny plik). Własny READ zakresu closing: pełny odczyt wszystkich RESULT.md/QC_SUMMARY.md/QC_FINDINGS.json + pełny recheck 555/555 pinów wejściowych (patrz INPUT_RECHECK.json).

## RUN_STATUS (propozycja): COMPLETED_WITH_SCOPED_BARRIERS_AND_PROCESS_INCIDENTS

Nauka runu domknięta w zadeklarowanym zakresie statycznym section1.bin; żadna bramka nie została zwolniona; wszystkie BARRIER-y sformalizowane; incydenty budżetowe D01/drobne rozdysponowane jawnie (sekcja 8).STATUS_SEAL_READY (ocena draftu closing child): patrz SELF_REVIEW_2.md — YES warunkowo (warunki QC2 zamknięte; root musi wykonać closing recheck własny, STOP+manifest wg kontraktu §13).

## 1. Werdykt runu (jednopoziomowo, osobno INTEGRITY/SCIENCE/PROCESS/PUBLICATION)

- **INTEGRITY**: PASS. Wszystkie wejścia SHA-pinned; image rekomputowany niezależnie przez QC1 i QC2 (MATCH); closing recheck (ten plik): 555/555 pinów MATCH własnym rehashem; admission ledger 14 eventów, seq monotoniczne 1-14, wszystkie reserved_before_extraction=true; frozen runy nietknięte (CORR1 = addytywne projekcje errata, nie edycje źródeł).
- **SCIENCE**: PASS_WITH_SCOPED_BARRIERS. Rdzeń naukowy niezależnie re-derywowany z bajtów (QC1+QC2); jeden fałszywy sub-claim (J02 zero-refs rel32) wyłapany przez QC1, domknięty errata J03 + CORR1; jeden błędny label receivera (J03 [P+0x10]) wyłapany przez QC2, domknięty CORR1; kontrmodel mostu NIF→entity/SFO pozostaje UNREFUTED z zerem zmierzonych instancji na zamkniętych torach.
- **PROCESS**: PASS_WITH_INCIDENTS. D01 BUDGET_BREACH (~71k decoded rows vs job cap 3500 i run cap 32000) — uczciwie samozgłoszony, zaadjudykowany przez roota (BUDGET_LEDGER.json → adjudication, 2026-10-25, QC2-F03 closed); drobne breache D02 (+3), D03 (+41 attempt-inclusive), J04 (+46) samozgłoszone; centralny ledger zaktualizowany addytywnie; żaden werdykt nie jest niesiony przez przekroczenie; brak wycieku hipotez do predykatów (QC2 grep wszystkich narzędzi).
- **PUBLICATION**: PENDING (root pieczętuje STOP → manifest → sanitizowany commit+FF push wg kontraktu §13; ten draft nie publikuje). Zakazane statusy promocji utrzymane (sekcja 5).

## 2. Mapa obiektów I/K/N/T/E/P/R (skrót; pełne role: OBJECT_AND_ID_MAP.md + ROLE_LEDGER.json)

| Symbol | Definicja (zmierzona) | Status tożsamości |
|---|---|---|
| E | entity 0x100B z factory 0x4578E0; [E]=0x65C060, [E+0x48]=0x65C05C, [E+0xF8]=P cache, [E+0xFC]=M | CONFIRMED_FOR_MEASURED_SCOPE (D01, A01) |
| I | [E+0x40], zapisywane przez a1 (store 0x555191 `89 46 40`), pushowane do lazy-create; rola ID-like | CONFIRMED_FOR_MEASURED_SCOPE; I≠K utrzymane (A01; R4-A01 upheld) |
| K | indeks rekordu; w zmierzonym lazy-create K=0 literal (byte-proven `push 0` @0x46E9D0); 46ECA0 re-bind ma selektor K z komunikatu → K≠0 istnieje | CONFIRMED_FOR_MEASURED_SCOPE (J01 S9) |
| N | retval 0x423280 = bezpośredni wskaźnik refcounted ROOT (+4=refcount); NIGDIE w zmierzonym zakresie nie dociera do record/SFO jako wspólny pointer | S1 CONFIRMED_FOR_MEASURED_SCOPE; N→T/P join: UNVERIFIED (E7) |
| T | rekord 0x5C = SUB[K]; runtime tworzony z komunikatów (45DE90/45D5F0/47CFB0); T0 nie jest globalnym niemutowalnym rekordem | CONFIRMED_FOR_MEASURED_SCOPE (J01 S8/S9) |
| P | proxy/SFO 0x7C (473E90, push 0x7C byte-proven); P+4=I, P+0x78=T, [W+0xF8]=P; E+0xF8=P | CONFIRMED_FOR_MEASURED_SCOPE; receiver 527A00/527BC0 = P sam (CORR1, QC2-F01) |
| R | rzeczywisty scene node/model root — tożsamość względem N/T/P otwarta | UNVERIFIED (brak dowodu) |
| M | manager 0x1D0B (ctor 0x456FF0), global 0x6C4C58, [M+0x08]=interfejs vt 0x65BE9C slot0=factory 0x4578E0 (1-slot vtable; D03 korekta "slot-22 alias"=overrun) | CONFIRMED_FOR_MEASURED_SCOPE (D01/D02/D03) |

**Status ROOT→record/proxy: UNVERIFIED z BARRIER.** Pętla name→ROOT→map→SFO NIE domknięta statycznie w section1.bin (J02 T12 SCOPED_NEGATIVE, upheld J03/J04/J05); lane (a) czytelnicy [obj+0xBC] domknięta negatywnie (J04); lane (c) [SUB+0x18] vt+4 statycznie martwa in-image (flag=0 hardcoded, J05); lane (d) member +0x18 nie wnosi klucza mapy (52A130 args handler-local, J05); pozostają lane (b) residual-14 `call [reg+0x3C]` + wrapper 0x498B80 inner (klasa runtime, key 0x19A), (d-res) post-52A130 flow 0x526CFA+, (e) sekcje poza section1.bin.

## 3. Typed A1..A6 (CONFIRMED_FOR_MEASURED_SCOPE, adresy bajtowe — A01/A01R, re-derywowane przez QC1)

Fabryka 0x4578E0 (thiscall, 6 stack args, ret 0x18) → writer 0x46E990 (przez [vt+0x1c] @0x457951, target z bajtów 0x65C07C) → 0x51D730 → 0x5531F0 → 0x555170 → 0x555270:

| arg | cel | dowód bajtowy |
|---|---|---|
| a1 | [E+0x40] dword (I) | store @0x555191 `89 46 40`; getter 0x553220 |
| a2 | byte [E+0x44] (tylko low byte) | store @0x555194 `88 4e 44` |
| a3 | flags [E+0x54] (NIE forwarded do 0x555170; ret 0x14=5 args; bit0 konsumowany @0x46E9E4) | store @0x553217 `89 56 54` |
| a4 | dispatch [vt+4] → 0x5552C0 → vec3 copy [this+4] | `ff 50 04` @0x55527C; vtable 0x65C064/0x65EC94 = 0x5552C0 |
| a5 | dispatch [vt+8] → 0x5552E0 → vec3 copy [this+0x10] | `ff 52 08` @0x555288; vtable 0x65C068/0x65EC98 |
| a6 | dispatch [vt+0x10] → 0x555320 → vec3 copy [this+0x28] + call 0x524370 | `ff 50 10` @0x5552A0; vtable 0x65C070/0x65ECA0 |

Bonus: vt+0xc→0x555300 i vt+0x14→0x555350 dostają stałą globalną 0x6C6664, nie a1..a6. A4_UNUSED = REJECTED (upheld, bajtowo obalone). **Scratch-slot**: 0x46EA02 (`89 44 24 1c`, ESP=E-0x04) zapisuje [E+4] do wejściowego slotu a6 home [E+0x18]; 0x46EA55 (`d9 44 24 28`, ESP=E-0x10 po `sub esp,0xc` @0x46EA3B) czyta TEN SAM absolutny slot; dominująca definicja = store [E+4]; **"stale A6" REJECTED dla tego callsite** (R4-A04 rozstrzygnięty). First-translation 0x46F0A0 dostaje (scale·f[E+4], scale·f[E+8], scale·f[E+0xC]), scale=[0x65B648] — bez etykiet osi (KONTRAZ).

## 4. Rozdział ról 42E9B0 / 42BA30 / 43C490 / 423350 (J01 + QC1-F02)

- **0x42E9B0** = klasa TEXTUR (NiPalette/NiPixelData/NiExtraData side): reset+source+loaded+type-walk z deskryptorem 0x6C3940 (runtime-init, zerowy w obrazie → BARRIER dla statycznej identyfikacji typu). Etykiety globalne 42E9B0_ONLY_TYPE_WALK / 43C490_STREAM_LOADER: ODRZUCONE per callsite (PA adjudykacja upheld).
- **0x42BA30** = binary stream reader klasy 0x65B3BC, slot **+0xC** (0x65B3C8) — korekta QC1-F02 z błędnego "+0x8" w J01 RESULT prose; semantyka (reader, nie open-by-name) upheld.
- **0x43C490** = konstrukcja strumienia plikowego (fopen 'rb', vt 0x65BAA8, flags 0x2800 na [+8], FILE* [+0x14]) — NIE jest loaderem; load robi nested `[nested_vt+8]`.
- **0x423350** = slot +0x40 klasy 0x65B3BC — compare/merge pól +0x18/+0x1c i smart-ptr +0x28; **NIE wraca jako model placement** (S15; brak nowych dowodów; R4 upheld).

**DrawIndexedPrimitive upheld**: renderer call 0x4DD421 (COM vt+0x11C, 5 args) — zgodność z D3D8 DrawIndexedPrimitive utrzymana; pola record+0x14/+0x2C/+0x30 NIE są tutaj XYZ; interpretacja transform-sink REJECTED (R4-A03, kontrmodel upheld w całym R5).

## 5. Per-model 296445.nif / 218757.nif — osobno, CONDITIONAL_OPEN

Oba modele: **binding_status = CONDITIONAL_OPEN** ( każdy osobno; MODEL_BINDING_CERTIFICATES_FINAL.json). Mechanizm wspólny potwierdzony (open-by-name 0x423280 klasa 0x65B3BC slot+0x3C; per-name tworzenie instancji typu-7 kluczone stringiem komunikatu na receiverze P — J03/CORR1; SFO visual przez message-key→52A130→564AB0→564890→[entry+8]→5257C0→[SFO+0x10]). Per-model: **brak jakiegokolwiek zmierzonego dowodu wiązania** — literały '296445'/'218757' nieobecne (SCOPED_NEGATIVE; name-assembly istnieje: '.nif' 0x6B0304, dword 218757 @0x469CBB incydentalny); oba callery J03 odrzucają retvaly; lane (a)/(c)/(d) domknięte negatywnie; runway = (b)/(d-res)/(e) tylko.

**Zakazy promocji utrzymane (kontrakt §14):**
- PE2003_WORLD_XYZ_RECOVERED = **NO**
- PE2003_HISTORICAL_PLACEMENT = **NOT_ESTABLISHED**
- SOURCE_SPECIFIC_ISO_MODELS = **UNKNOWN** (mechanizm wspólny potwierdzony; per-model otwarty)
- LOCAL_SOURCE_EXHAUSTED = **NO** (negatywy scoped, nie globalne)
- CANONICAL_GATE_EFFECT = **NONE**
- MODEL_INSTANCE_JOIN (ROOT→record/proxy) = **UNVERIFIED** (zakaz CONFIRMED upheld)

## 6. QC — wyniki

- **QC1 (R5-QC1-001)**: PASS_WITH_FINDINGS (P1×1, P2×2, P3×2). Wszystkie 5 findingów domknięte w ERRATA_J01_J02.md (J03, z własną weryfikacją bajtową E1-E5; QC2 ponownie potwierdziło domknięcie; algebra 57 witryn slot+0x3C: 19+24+14=57 DOMKNIĘTE). Korekta QC1-F03 → residual finalny 14 (0x4551C4 wyeliminowana z pełnego okna; 0x56FA46 dodana).
- **QC2 (R5-QC2-001)**: PASS_WITH_FINDINGS (P2×3, P3×3), STATUS_SEAL_READY=NO z warunkami 1-3. Warunki zamknięte: **F01** → CORR1 (MODEL_BINDING_CERTIFICATE_J03_CORRECTED.json, byte-verified, frozen źródło nietknięte); **F02** → D03_EVIDENCE_STRICT.json (re-projekcja strict); **F03** → BUDGET_LEDGER.json adjudication (root, addytywnie) + jawna adjudykacja D01; **F05** → QC_VERIFIED_ITEMS_STRICT.csv (re-projekcja 5-pól). F04/F06: errata/noty wordingowe niewymagane do sealu (opcjonalne).
- **CORR1 (R5-CORR-001, pe-reconstruction)**: wykonane cele QC2-F01/F02/F05 (addytywnie; patrz CORRECTION_DISPOSITION.md).

## 7. Budżet i incydenty

- Native attempts: 13/96 użyte (A01, J01, A01R, J02, QC1, D01, J03, D02, J04, D03, J05, D04, QC2) + CORR1 + closing/pub w rezerwie 8. Bodies 190/256. Doc_lines 21000/100000 (sekcja caps ledgera; closing package liczony osobno, ≤6000 w tym pakiecie).
- **D01 BUDGET_BREACH (incydent procesowy)**: pass2/pass4 ~71k decoded rows vs job cap 3500 i run-level cap 32000; uczciwie samozgłoszony (COMPLETED_WITH_BUDGET_BREACH_FLAG); adjudykacja roota: PROCESS_INCIDENT, evidence static-valid (odczyty read-only), downstream scan-window prohibition egzekwowana od J03 (J04 +46, D03 +41, D02 +3 — drobne, samozgłoszone). Unique-row count nie niezależnie re-derivationowany → status unique UNVERIFIED (upheld R4-A11: brak within-budget z częściowego pomiaru).
- D03 code_rows dual-counting (1241 attempt-inclusive vs 989 retained) — obie liczby podane, interpretacja roota w ledgerze.
- Żaden werdykt naukowy nie jest niesiony przez przekroczenie (nośne: sondy bajtowe + censa z predykatami/denominatorami/kontrolami dodatnimi/testami odmowy).

## 8. Frontier (skrót; pełne: FRONTIER.md + RESEARCH_BACKLOG.json)

1. Residual-14 witryn `call [reg+0x3C]` + inner wrappera 0x498B80 ([svc_result+0x38], serwis [0x6C4F20], key 0x19A) — jedyne pozostałe slot+0x3C lane w section1.
2. Post-52A130 flow 0x526AE0 (0x526CFA+) — najbliższy zmierzony styk lane (d) ze stroną SFO.
3. Registry [0x6C62F4] consumer surface (5077C0/5072C0/468010-tree; nośnik 0x19A z vtable 0x6661E8 — sloty 6/7/9 = czytelnicy M-cell, pozostałe sloty niedekodowane) — niesie ZARÓWNO kontrmodel caller-a fabryki (slot-0 na M+0x08, 6 pushy), jak i proweniencję wartości czytelników.
4. Sekcje PE poza section1.bin (vtable wrappera 0x498B80, RTTI 0x6C3898/0x6C3A0C, import [0x65A1A8], serwis [0x6C4F20]).
5. Factory caller (realny): slot-0 dispatch na receiverze M+0x08 z 6 pushami — nieznaleziony w CAŁYM zmierzonym zakresie (D01-D04 domknęły global→+8→slot0, slot-22 alias, [M+0x8C] subsystem=terminalne leaf-gettery O, 3 czytelników M-cell=producenty stringów). a1..a6 upstream = UNBOUND/UNRESOLVED.
6. EmulationReadiness (46F0A0/46F0C0) = design only — bez autoryzacji wykonania w tym runie.

## 9. Coverage algebra (L11)

TOTAL użytych plików źródłowych closing = 26 (INPUT_RECHECK.json, wszystkie FULL_READ) + 555 pinów (full rehash MATCH). Tryb: FULL_READ dla 10 RESULT, 2 QC_SUMMARY, 2 QC_FINDINGS, 2 certyfikaty finalne, RUN_CONTROL, CLOSING_RECHECK_ROOT, CONTRACT, PA_RECONCILIATION, FINDINGS_R4, INPUT_PINS (hash-recheck), BUDGET_LEDGER, BODY_ADMISSION_EVENTS; BOUNDED_INSPECTION: wybrane data/*.json jobów (D01_EVIDENCE, ABI_FIELD_MAP_R5_A01 odczytany w pełni); NOT_CHECKED: pełne ciała DISASM/*.asm (pokryte przez re-derywacje QC1/QC2), EARLY_RESULT.md jobów, pliki ERRATA_QC2_* czytane fragmentarycznie z potwierdzeniem przez certyfikat CORRECTED. Żaden claim load-bearing tego pakietu nie opiera się wyłącznie na plikach NOT_CHECKED.

## 10. Podsumowanie symboli statusu runu

RUN_STATUS=COMPLETED_WITH_SCOPED_BARRIERS_AND_PROCESS_INCIDENTS; INTEGRITY=PASS; SCIENCE=PASS_WITH_SCOPED_BARRIERS; PROCESS=PASS_WITH_INCIDENTS (D01 zaadjudykowany); PUBLICATION=PENDING (root). Draft: STATUS_SEAL_READY=YES_CONDITIONAL (SELF_REVIEW_2.md) — po wykonaniu przez roota: własny closing recheck, SCIENCE_STOP, MANIFEST (LAST), verify, publikacja.
