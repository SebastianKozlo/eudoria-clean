# REPORT — DERIVED CONSTRUCTION / R ATTACH / RESOURCE INSTANCE (DEFAULT/MEDIUM, SAVED_ONLY)

RUN_ID=PE_935_DERIVED_CTOR_ATTACH_RESOURCE_PROVENANCE_DEFAULT_TASK_OPENCODE_SAVED_R1_20261023
RUN_STATUS=SCIENCE_COMPLETED_QC_COMPLETED_SEALED (patrz MANIFEST_SHA256.csv)
SCIENCE_VERDICT=PARTIAL_PASS_WITH_PPA_COMPLIANT_BOUNDARIES (nowe krawędzie potwierdzone; writer R nieustalony w zapisanym zakresie; QC_PARTIAL rezerwacje utrzymane)
PROCESS_VERDICT=COMPLIANT_WITH_QC_CORRECTIONS_APPLIED (QACC F2/F3/F4; QSCI_3 P2 wording)
ROOT_SESSION=ses_e952375aaffe6rebKJ3oWD4iBo
CLIENT_MEDIUM_ATTESTATION=nask-glm/glm-5-3 process-scoped reasoningEffort=medium (DEFAULT_CONFIG.json, 11 ról; launcher DEFAULT_PREFLIGHT PASS)
TASK_ACTUAL_COUNT = 15
STOP/LENGTH/FAILED/RETRIES/ORPHANS = 15/0/0/0/0 (DB read-only census; parent binding 15/15; 0 grandchildren; max 2 active; depth 1)
QC_SCOPE=3 fresh Q_SCIENCE (construction CFG PASS; writer/provenance PASS; negatives/placement QC_PARTIAL 6xP2) + 1 fresh Q_ACCOUNT (QC_PARTIAL F2/F3/F4 — zastosowane)
ACTUAL_BUDGETS=reservations code 1174/18000, docs 6790/16000, body_ids 15/48, attempts 15/32, rodziny C6/8 W4/8 J1/6 QSCI3/8 QACC1/2; total exposures UNMEASURED_WITH_OBSERVED_LOWER_BOUND (semantyczne wiersze ≥557; census scans count-only raportowane per job; brak exact capPASS z rezerwacji)
INCIDENTS=NONE (mechaniczna korekta podziału pakietu PRZED pierwszą ekspozycją semantyczną — CORRECTION_LEDGER CL-8)
REQUEST_EFFORT=NOT_OBSERVED
SERVER_EFFECTIVE_EFFORT=UNKNOWN
PUBLICATION_STATUS=patrz PUBLICATION_RESULT.json w RECEIPT_ROOT

## Wyniki naukowe (statusy canonical)

- CTOR_CONTROL_COVERAGE=COMPLETE_SAVED_RANGE — saved pokrycie konstruktora pochodnego 00528E50 kompletne dla zapisanego zakresu 00528E50..00529072 (139 wierszy, 4 fragmenty SHA-pinned, nakładki 2 wiersze, zero dziur VA; QSCI_1 weryfikacja per-wiersz). NIE roszczymy pokrycia całej funkcji poza zapisanym zasięgiem.
- NORMAL_EXIT_POSTCONDITIONS=BOTH_MAPPED — dwa normalne wyjścia: epilog (EAX=B, RET 0x10 @00529072; unwinding SEH; rachunek stosu 56=56) i warunkowy wczesny exit (JZ @00528FBF → początek epilogu), który pomija późne inicjalizacje. Postcondition pól +0xC/+0x10 na OBU wyjściach: brak jawnego store w saved pokryciu; wartość wynika z zerowania w bazowym ctorze (store 0085B1CD w 0085B1B0). NIE roszczymy POST_CONSTRUCTION_ONLY ani STILL_NULL_AT_CTOR_EXIT (PPA-A01).
- NONZERO_WRITER=NOT_ESTABLISHED_IN_ADMITTED_SCOPE — census saved H5 (1,743,928 wierszy, VA 0048AEF0..00A745E4, formy MOV/RMW/stack/indexed/float, dedup): jedyny nie-stackowy store [reg+0xC] w oknach 9 funkcji powiązanych z B to zerujący 0085B1CD. Niezależne przeliczenia: W01, W04 (EXACT), QSCI_2 (3 warianty granic — wynik identyczny). Census NIE wyklucza (bounds): adjusted-base, REP MOVS/STOS, out-arg, setter-alias, brak per-region intersection 88 form indeksowanych, regionów poza H5 (004154F0, 00414130), slotów vtable w .rdata. Wynik dotyczy wyłącznie zapisanych wierszy H5.
- ATTACH_PHASE=NOT_ESTABLISHED; R_ARGUMENT_ORIGIN=NOT_ESTABLISHED; R_WRITTEN_TO_R_APPLY_BINDING=NOT_ESTABLISHED_IN_ADMITTED_SCOPE (PPA-A05).
- STATIC_CLASS_VTABLE_BINDING=CONFIRMED_CONSTRUCTION_LEVEL — derived ctor zapisuje vtable A7DCB0 @00528EA2 (drugi store 005290A8 w funkcji 00529080, kandydat dtor; sloty tabeli NIEodzyskiwalne z saved źródeł — .rdata poza H5). Konstrukcyjny store nie dowodzi runtime typu R.
- REGISTER_LOOKUP_JOIN=NOT_ESTABLISHED — brak rejestracji B w oknie creatora; retval 004154F0 to osobna populacja (lookup retval), nie B (QSCI_3 P2-2 reworded).
- RESOURCE_INSTANCE_JOIN=CONTEXT_MENTION_ONLY (bounded: ERRATA_R5.md + ATTRIBUTE_ORIGIN_SEAM REPORT.md + indeks; 11 hit-plików nieczytanych; cytaty vs oryginały NOT_CHECKED poza scope QC) dla 296445.nif/template 4508.
- INSTANCE_ROOT_ROLE=NOT_ESTABLISHED; TRANSFORM_SOURCE=NOT_ESTABLISHED.
- PHYSICAL_SOURCE_MEDIUM=SAVED_DISASSEMBLY_ONLY (pinned H5 + prior packets + własne packety z proweniencją; zero dostępu do EXE/NIF/VFS/runtime; oryginał nie hashowany).
- WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CURSOR_SOURCE_MEDIUM=UNKNOWN; CANONICAL_GATE_EFFECT=NONE.

## Nowe krawędzie tego runu

1. Konstrukcja pochodna 00528E50: entry ECX→ESI (B), SEH prolog, CALL bazowy ctor 0085B1B0 @00528E8D (receiver B), vtable A7DCB0 @00528EA2, 16 unikalnych callsite'ów (MODREF_OBLIGATIONS), kluczowa krawędź: retval 005247C0 → [B+0xC0] @00528FEA (pierwsza inicjalizacja sub-+0xC8), późne cally z receiverem [B+0xC0] i argumentami &B+0x44/&B+0x5C/&B+0x50.
2. Creator 004C46C0 CONFIRMED jako jedyny DIRECT caller (callsite 004C47C1; alokacja 0x128 przez 0095D3C4 @004C4797 z null-check; funkcja RET @004C47EF). Ścieżki pośrednie/wirtualne NIE wykluczone (QSCI_3 P2-1). Poprzednia premise "creator bez call" była artefaktem prefixu (packet kończył się @004C476E) — rozstrzygnięte bez nowego eksportu (PPA-A02 wykonana).
3. Post-ctor: normal path (JMP @004C47C6 pomija XOR EAX,EAX) przekazuje B jako argument wskaźnikowy do 004154F0; null-path przekazuje NULL; retval 004154F0 → receiver 00856190; B pozostaje na stosie podczas 00856190 (args unknown). Brak rejestracji B w oknie.

## FIRST_MISSING_EDGE

Ciało 004154F0 — jedyny bezpośredni odbiorca B po konstrukcji; property: store przez [arg+0xC] (kwalifikowany writer R); time: post-ctor, pre-POP @004C47EA; status: SAVED_TARGET_DATA_BARRIER (004154F0 < min VA saved H5 0048AEF0); measurement: przyszły autoryzowany odczyt/eksport tego ciała (NIE autoryzowany w tym runie). Alternatywne krawędzie: 00414130 (poza H5), sloty A7DCB0/A91E4C (.rdata), 00856190 (stack visibility). Szczegóły: FIRST_MISSING_EDGE.json.

## Zachowane fakty poprzedników (nienaruszone)

B=this 00528380; R_i=M32[B+0xC] w poszczególnych chwilach analizy; P_apply=M32[R_apply+0x2C]; dispatch VT+0x14; permutowany blok 48B; warunkowy cache 52B; B+0x2C vs R+0x2C to różne miejsca; bazowy vtable A91E4C.

## Proces

PPA-A01..A05 przyjęte addytywnie; NEXT_BASELINE.md przeczytany (MASTER_READ M001, prior REPORT DEEP_POSTAUDIT przeczytany). 14 dispatchów TASK + 1 MASTER_READ, wszystkie przez dispatch_admission READY (seq 2..17); START seq 1. Korekty QSCI_3/QACC przyjęte centralnie (CORRECTION_LEDGER CL-1..CL-11); pliki workerów zamrożone; QC_PARTIAL rezerwacje utrzymane w CLAIMS. Sanitizacja: public REPORT to verbatim kopia tego pliku; DERIVED_CLAIMS.json verbatim z CLAIMS.json; EXTERNAL_POSTAUDIT_SUMMARY.md verbatim PUBLIC_SUMMARY niezależnego postaudytu poprzednika; bez game bytes/listingów/SDK/packetów/promptów/DB/config/sekretów.
