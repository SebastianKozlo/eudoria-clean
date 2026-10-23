# REPORT — PE_935_PROVIDER_PROVENANCE_APPLIER_JOIN_HIGH_TASK_OPENCODE_SAVED_R1_20261023

RUN_ID = PE_935_PROVIDER_PROVENANCE_APPLIER_JOIN_HIGH_TASK_OPENCODE_SAVED_R1_20261023
RUN_STATUS = COMPLETED_SCIENCE_QC_SEALED_PUBLISHED (publication receipt: RECEIPT_ROOT/PUBLICATION_RESULT.json)
TASK_ACTUAL_COUNT = 21
ROOT_SESSION = ses_e956f43f1ffekOtseu0Zy9KGe4 (single visible TUI pe-master, launched once, PID 5084)
CLIENT_HIGH_ATTESTATION = HIGH_PREFLIGHT: nask-glm/glm-5-3 for root, small_model and all 11 registered roles, client reasoningEffort=high, thinking=enabled, process-only config (HIGH_CONFIG.json), global config untouched, MAX not selected
REQUEST_EFFORT = NOT_OBSERVED
SERVER_EFFECTIVE_EFFORT = UNKNOWN
STOP/LENGTH/FAILED/RETRIES/ORPHANS = 1 STOP_JOB (S01, 2x length) / 8 length-finish attempts / 5 failed-first-then-retried-OK / 0 orphans; all children quiesced, zero grandchildren
QC_SCOPE = fresh QSCI_1a (caller windows pointer/time; QC_PASS 10/10), fresh QSCI_1b (base-ctor+census replay byte-identical+cache-tail; QC_PASS), fresh QSCI_2 (applier contract; QC_PASS 7/7), fresh QSCI_3 (MSC/negatives/categories; QC_PARTIAL — admission-scope caveat retained, 0 material), fresh QACC (accounting; ACCOUNTING_PASS, 0 material / 4 hygiene all fixed pre-seal)
INCIDENTS = INC-1 (master DB-diagnostic exposure of P_S01/P_S02 packet rows before master-read admission; disclosed, charged, forward admissions taken); INC-2 (S01 attempt-2 length failure -> STOP_JOB per ladder; family S_BASELINE exhausted 4/4; entry/cache-tail windows mapped MASTER_DERIVED under admitted master reads and independently QC-verified)
CANONICAL_GATE_EFFECT = NONE

## 1. Nauka — co ustalono (saved-only; wszystkie VA = zapisany H5, bajty nie rewalidowane vs oryginał)

B/R/P TIME BINDING (CONFIRMED):
- B = 00528380 dispatching object (ECX->EBP @00528387; SUB ESP,0x88; RET 0x8 na obu wyjściach); wejściowe straże null [B+0xC] @00528389 i [B+0x10] @00528393 -> ścieżka 005285E3 (dispatch slot+0x24, RET 0x8).
- Cztery osobne odczyty tego samego pola [B+0xC]: R_gate @005283EB, R_apply @005284A1 (this CALL 0085CDE0 @005284AC), R_read1 @005284B6 (this 0085C0C0 @005284B9), R_read2 @005284D2 (this 0085C280 @005284E0). RÓWNOŚĆ POLA-ŹRÓDŁA = FAKT; równość wartości pomiędzy odczytami NIEDOWODLIWA statycznie (pomiędzy odczytami interwenią nieprzezroczyste CALL-e).
- Enum [R+0x20]==3 @005283F0 wybiera gałąź macierzy identity (9 dword @0052840E..00528430, sloty ESP+0x28..0x48); nierówność -> CALL 0096CCB0 (this=&matrix_local, arg=[B+0x64]) @00528407; obie gałęzie łączą się @00528434. Enum3 bramkuje WYBÓR MACIERZY, nie całego writera.
- Rekord 13 dword @ X+0x64: 9 dword macierzy (REP MOVSD @00528478) + 3 sumy FADD ([ret_wirtualnego+0/4/8]+[EBX+0/4/8]; EBX=M32[X+0x9C] @00528448, writer poza oknem) + końcowe 1.0 @00528480. Applier CALL 0085CDE0 @005284AC, this=R_apply, args (record_ptr, 0x1).
- Cache B: [B+0x110/114/118] <- trójka 0085C0C0; [B+0x11C/120/124] <- trójka 0085C280 (dokończenie @005284ED/005284F9/005284FF); [B+0x104/108/10C] <- 00861220/00734210/00861240 na [B+0x10]; cztery konsumpcje na vtable B (slot+0x24 warunkowo @0052853C; slot+0x28 @00528547 z arg=&[B+0x11C]; slot+0x30 @00528570; slot+0x2C @00528593) — cele slotów NIEZNANE (komórki tabeli 0xA7DCB0 poza 4 przechwyconymi); tail: [B+0xD2]=0, [B+0x9E] warunkowo, [B+0xD4/D8/DC] <- globalnie.
- Brak dostępu poziomu P w ciele writera ([R+0x2C] i głębiej: CONFIRMED_ABSENT w 00528380..0052860A).

PROVIDER_ORIGIN (częściowo CONFIRMED, ostatecznie UNKNOWN):
- R=[B+0xC]: KOMPLETNY ctor bazowy 0085B1B0 (head 0085B1B0..0085B25B + tail ..00528...0085B31E, RET 0xC) czyści [+0xC] i [+0x10] do NULL (@0085B1CD/@0085B1D0, EBX=0); widoczna głowa ctora pochodnego 00528E50 nie dotyka tych pól; ATTACH R = POST_CONSTRUCTION_ONLY; writer NIEZNANY (tail ctora pochodnego 00528F07+ poza zapisanymi pakietami = SAVED_COVERAGE_BARRIER). NOWY FAKT: ctor bazowy przechowuje vtable 0x00A91E4C @0085B1C1 (bazowa tabela klasy — addytywnie potwierdza prior kandydata; runtime dispatch nadal NOT_OBSERVED).
- P=[R+0x2C]: census count-only całego zapisanego H5 (1,743,928 wierszy): 598 MOV + 0 LEA + 144 other = 742 kandydatów zapisu [GPR+0x2C]; strefa klasy pochodnej (00528380..00528E60) = 0 zapisów; strefa rodziny (0085B000..0085C400) = 3 (0x0085BBF8, 0x0085BE70, 0x0085C0A7); kwalifikacja BARIERA: brak literalnej proweniencji receivera dla tych 3 (klastrowanie layoutowe niewystarczające); 2 z 6 dopuszczonych okien kwalifikacyjnych użyte (oba okna ctora bazowego, uzasadnione przesłanką P01); pozostałych okien nie otwierano (brak łączącej przesłanki — zakaz losowego sweep).
- Prior inventory: ŻADEN przypięty prior nie ustanawia pozytywnego writera/ctora dla R ani P; HBR-R vs nasze R: CANNOT_DETERMINE.

APPLIER_INPUT / APPLIER_DESTINATION (CONFIRMED, destynacja nieprzezroczysta):
- 0085CDE0: P_apply = M32[this+0x2C] @0085CEC5; dispatch wirtualny [P_apply VT + bajt 0x14] @0085CED4; pojedynczy argument = wskaźnik na lokalnie permutowany blok 48 bajtów (transpozycja 3x3 + trójka z rekordu arg1; dword 1.0 NIE wchodzi do bloku; LEA @0085CE17, PUSH @0085CE1E) — QC zweryfikowało niezależnie; warunkowy (arg2) cache 52 bajtów SUROWEJ głowicy rekordu do this+0x30 (@0085CED6/JZ @0085CEDE, REP MOVSD 13 dword @0085CEE0-0085CEEA).
- DESTINATION = OPAQUE virtual receiver; tożsamość metody slotu +0x14 nieznana w zapisanych danych; jedyna konkretna destynacja w ciele = cache this+0x30. Brak jakiegokolwiek claim scene/root/world/model.
- SDK 1.2.2.6 (reference only, nie ABI): rekord 13 dword = PARTIAL_MATCH layoutu NiTransform (m_Rotate 3x3 -> m_Translate -> m_fScale; NiTransform.h L25-27); blok 48B = NONE_OF_THE_ABOVE w SDK; semantyka settera destynacji NOT_ESTABLISHED.

VT_IDENTITY / TARGETS / STATUS: runtime vptr żadnego obiektu NOT_OBSERVED; B-table: dwa statyczne bindingi konstrukcyjne (0xA7DCB0 pochodna @00528E50, 0xA91E4C bazowa @0085B1C1); sloty konsumpcyjne +0x24/+0x28/+0x2C/+0x30 i slot destynacyjny P +0x14: cele UNKNOWN (komórki .rdata poza zapisanym capture; A75378 NOT_READ poza zakresem).

DIRECT_STORES = zachowana mechanika prior (14 store'ów self-cache/flags/globals; spójna z zapisanymi wierszami).
VALUE_PRODUCER = 0085C0C0/0085C280 (forward przez [this+0x2C] sloty +0x28/+0xDC; guards + zero-fallback przesłanka prior zachowana).
SOURCE_vs_CACHE = rozdzielone: SOURCE_VALUES / SERIALIZED_RECORD / REQUESTED_STATE / APPLIED_STATE(UNKNOWN za opaque call) / CURRENT_STATE_CACHE(B-side) / RAW_HEAD_CACHE(this+0x30).
RECEIVER_JOIN = NOT_ESTABLISHED (opaque CALL między odczytami; brak przesłanki no-interfering-write/lifetime).
REGISTER_LOOKUP_JOIN = NOT_ESTABLISHED (nie testowane; bez promocji STATIC_CLASS_VTABLE_BINDING).
STATIC_CLASS_VTABLE_BINDING = ESTABLISHED_AT_SAVED_CONSTRUCTION_LEVEL (poziom konstrukcji; runtime NOT_OBSERVED) — dwie tabele, dwie fazy konstrukcji jednego obiektu.
INSTANCE_ROOT_ROLE = UNKNOWN; RESOURCE_INSTANCE_JOIN = UNKNOWN; HISTORICAL_TRANSFORM_PROVENANCE = NOT_ESTABLISHED; TRANSFORM_SOURCE = UNKNOWN; PHYSICAL_SOURCE_MEDIUM = UNKNOWN.
WORLD_INSTANCE_RELEVANCE = UNKNOWN (relevance gate po każdej fali; negatywy z denominatorami: census 742/3/0, prior-inventory NONE_FOUND, destynacja opaque).

FIRST_MISSING_EDGE = writer/attach R=[B+0xC] post-construction: typ = SAVED_COVERAGE_GAP (tail ctora pochodnego 00528F07+ bez pokrycia; brak autoryzowanego census zapisów +0xC w tym runie) + brak receiver-qualified kandydatów; wtórne: tożsamość klasy P + jej tabela (sloty +0x14/+0x28/+0xDC/+0x160), cel [P VT+0x14], cele slotów konsumpcyjnych B. Dyskryminujący następny eksperyment: pokrycie H5 taila ctora pochodnego + kwalifikacja zapisów [reg+0xC] przez literalną proweniencję receivera (klasa 0xA7DCB0/0xA91E4C lub łańcuch creatora 0x004C46C0).

WORLD_XYZ_RECOVERED = NO
HISTORICAL_PLACEMENT = NOT_ESTABLISHED
CURSOR_SOURCE_MEDIUM = UNKNOWN

## 2. Proces

SCIENCE_VERDICT = PARTIAL_PASS_WITH_DATA_BARRIERS (bariary dokładnie zlokalizowane; zero findinfów materialnych QC)
PROCESS_VERDICT = PARTIAL_NONCOMPLIANT_WITH_DISCLOSED_INCIDENTS (INC-1: ekspozycja mastera przed admission — ujawniona, obciążona, forward admissions; INC-2: STOP_JOB S01 + wyczerpanie rodziny S — ujawnione; wszystkie capy globalne i rodzinne dochowane; brak refundacji)
ACTUAL_BUDGETS = próby 21/28 (S 4/4, P 7/8, A 3/8, Q_SCIENCE 6/6, Q_ACCOUNT 1/2); ciała 5/48 (w tym F00528600 = 3 wiersze-sąsiad); rezerwacje code 2203/18000, doc 10750/16000 (pełny zakres po korekcie H1); unikalne wiersze H5 ~432/5000; ekspozycje ~800-870/18000 APPROX/LOWER_BOUND; SDK 284/300 primary lines (A02); nowe pliki saved 0/8; reference queries 0/32
UNMEASURED_METRICS = dokładne liczby bajtów tool-output; dokładne liczby cytatów w RESULTach pracowników (APPROX); REQUEST_EFFORT/SERVER_EFFECTIVE_EFFORT
QACC = ACCOUNTING_PASS (READY<->DB 21/21, chronologia, saved-only, jednostki)
SEAL/PIN = package_tools --seal + --verify-tree (manifest LAST; receipt poza rootem)
PUBLICATION_STATUS = RECEIPT_ROOT/PUBLICATION_RESULT.json (canonical)
COMMIT_SHA / REPORT_GITHUB_URL = zapisane w canonical receipt (powstają po sealu)

## 3. Zastrzeżenia (obowiązujące)

(1) Wszystkie VA/instrukcje = poziom ZAPISANEGO H5 (parzystość literalna 190/190 wierszy paczek run-local); bajty kodu nie rewalidowane vs oryginał (zakaz ponownego otwarcia). (2) Mapy okien S01/S03 są MASTER_DERIVED (job wykonawczy S01 przerwany po 2 identycznych awariach length; rodzina S wyczerpana) — zostały niezależnie zweryfikowane przez świeży QSCI_1a/QSCI_1b co do wiersza. (3) QSCI_3 = QC_PARTIAL: weryfikacja dokumentowa MSC-A05 na poziomie CORRECTION_LEDGER nie była w dopuszczonych wejściach audytora (rodzina Q_SCIENCE 6/6); poziom ledgerów zweryfikował świeży QACC (PASS). Zastrzeżenie pozostaje. (4) Statyczne bindingi vtable != runtime vptr; brak jakiejkolwiek obserwacji runtime. (5) Porównanie SDK = reference-only; sloty/ABI nie transferują się do PE. (6) Publikacja nie jest kanoniczną akceptacją nauki; nowy dowód zgłoszony do external postaudit; CANONICAL_GATE_EFFECT=NONE.
