# REPORT — PE_935_OWNER_POINTER_WRITER_RESOLUTION_DEFAULT_TASK_OPENCODE_SAVED_R1_20261023

RUN_STATUS=COMPLETED (bounded; workers + 3 science QC + accounting QC + seal + publication to terminal)
SCIENCE_VERDICT=PARTIAL_PASS_WITH_NEW_CONFIRMED_HOPS_AND_CLOSED_CENSUS (writer itself NOT observed)
PROCESS_VERDICT=PARTIAL_NONCOMPLIANT (2 disclosed incidents: I038 admission chronology, QC1 exposure overshoot)
INTEGRITY_VERDICT=SEALED (manifest bijection + rehash PASS; sealer proves bytes, not claims)
PUBLICATION_STATUS=see PUBLICATION_RESULT.json in RECEIPT_ROOT
CANONICAL_GATE_EFFECT=NONE
AUTHORITY_STATUS=ADVISORY_PRE_QUALIFICATION
MODEL=DEFAULT nask-glm/glm-5-3, client reasoningEffort=medium; REQUEST_EFFORT=NOT_OBSERVED; SERVER_EFFECTIVE_EFFORT=UNKNOWN

## 1. Pytanie główne i wynik

Cel: rzeczywisty writer [owner+0x0C], jego producent wartości i związek z korzeniem instancji. Wynik:

- WRITER_OBSERVED=NO. W żadnym admitted window nie znaleziono zapisu instalującego [B+0x0C]/[B+0x10]. VALUE_AT_CTOR_RETURN=NOT_ESTABLISHED; WRITER_PHASE=UNKNOWN (konstrukcja NIE została wykluczona — pozostały ścieżki aliasowe (a)-(e)).
- CTOR_DIRECT_B_CENSUS CLOSED: dokładnie 7 callsite'ów z ECX=B w widocznym ciele 00528E50 (0085B1B0, 0085B0A0, 0085AD60, 00401360, 0085B120, 00414130, 0085B750); wszystkie otwarte; żaden nie pisze pól docelowych. 0085B1B0 zero-inituje (prior canon); 00401360 = ECX_UNUSED na poziomie pseudokodu (saved export); pozostałe instruction-level negative.
- KANDYDAT 0085B652 ZAMKNIĘTY NEGATYWNIE: MOV [ESP+0xC],EAX w funkcji 0085B640 — slot ramki stosu, zbieżność offsetowa, nie writer.
- ROZWIĄZANY CALLSITE 004C47C1: to CALL 00528E50 (konstruktor), ECX=alokacja 0x128 z CALL 0095D3C4@004C4797 (IAT thunk, prior canon), 4 argumenty stosowe, RET 0x10 spójne.
- NOWY HOP REJESTRACJI (główny nowy wynik): po konstruktorze creator przekazuje B przez CALL 004154F0 (getter singletonu managera, saved 122B, ignoruje argument stosowy, oba epilogi plain RET — wypchnięty B ZOSTAJE na stosie) do 00856190(ECX=mgr, arg1=B skonsumowany przez RET 0x4): 00856190 czyta [B+0x74] jako guard, blokuje managera, czyta [B+0x74] przez 00414130(B), wstawia B do mapy @mgr+0x10 przez 00856090 z kluczem [mgr+0x24]+1 (B na [ESP+0x14]); przy "już obecny" wykonuje virtual call slot 0 na B (CALL [[B]->vtbl[0]](B,1)); sam nie pisze [B+0x0C]/[B+0x10].
- ROZWIĄZANY ALIAS A1: 00746570 = LEA EAX,[ECX+0x20]; RET z receiverem EDI (arg3 konstruktora — obiekt przychodzący, nie B): 0085AD60 kopiuje [EDI+0x20]->[B+0x88], [EDI+0x24]->[B+0x8C]. Rozłączność EDI<->B nieudowodniona (UNKNOWN-alias).

## 2. Macierz aspektów

Pełna macierz w RESOURCE_INSTANCE_TRANSFORM_MATRIX.csv. Kluczowe: WRITER=NOT_OBSERVED (bounded); CENSUS=CONFIRMED; CALLSITE=RESOLVED; REGISTRATION_EDGE=STRONGLY_SUPPORTED; SLOT0=NOT_RESOLVED; POINTEE_CLASS_P=UNRESOLVED_UPSTREAM; R_VS_X_JOIN=NOT_ESTABLISHED; INSTANCE_ROOT_ROLE=członkostwo w mapie managera (nie tożsamość sceny); TRANSFORM_SOURCE=UNKNOWN; standing: WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CURSOR_SOURCE_MEDIUM=UNKNOWN; CANONICAL_GATE_EFFECT=NONE.

## 3. QC

Trzy świeże sesje pe-master-auditor (depth 1, bez nesting):
- QSCIENCE1: QC_PASS_WITH_FINDINGS — C1-C7 VERIFIED (z notami); kontrmodele M1-M7 HOLD; material P1 (00414130 poza listą ryzyk) rozwiązany otwierciem gettera i korektą census.
- QSCIENCE2: QC_FAIL na tymczasowym sformułowaniu census — material catch: 0085B0A0 pominięty w tekście listy, 00401360 z literal ECX=B (survival przez niemodyfikujące ECX ciało 0085AD60), pośredni [0xA75A5C] jako ryzyko (d).
- QSCIENCE3: QC_FAIL na przedawnionym sformułowaniu (00746570 receiver=EDI nie B; arg 0085AD60 = EDI+0x20 nie B+0x20; 00414130 @00528FD9); finalny census (OWR-C2) i łańcuch (OWR-C3) to TABELE WYPOCHODZONE I ZWERYFIKOWANE PRZEZ QSCIENCE3 — opublikowane verbatim, nie trzecia wersja mastera bez QC. Obligation census_qc spożyło cap 2 prób; science QC na finalnej treści = QC_PASS_WITH_FINDINGS z jawnym QC_PARTIAL dla historii sformułowań.
- QACCOUNT: odrębny świeży auditor (ledger/manifesty/chronologia) — wynik w QC_RESULT i FINAL_ACCOUNTING.

## 4. Proces

12 natywnych Task (8 workerów pe-reconstruction + 3 świeże QC nauki + 1 QACCOUNT, wszystkie completed); wszystkie finish=stop, zero length/failed/retries/orphans, zero grandchildren, 11/11 parent-bound w DB (mode=ro). Capy: exposures lower_bound 2356/24000 (per QACCOUNT F1: 415 worker data rows + 25 pseudo + 47 quotes + 709 master + 1116 QC + 44 QC-admin); unique rows 724/8000; ciała ~30/80; CALL units 65/400 (dekompozycja w FINAL_ACCOUNTING); kandydaci 9/64; discovery 1/8; attempts 12/32; depth 1; max 2 aktywne. Incydenty: OWR-IN1 (chronologia admission I038 — ujawnione, naładowane), OWR-IN2 (overshoot ekspozycji QC1 ~610/320 — ujawniony, kolejne QC zaprojektowane pod cap). Znane naruszenia zobowiązują do PROCESS_PARTIAL_NONCOMPLIANT mimo ujawnienia.

## 5. FIRST_MISSING_EDGE

Writer [B+0x0C] nonzero pozostaje otwarty; ranked edges: (1) indirect CALL [0xA75A5C]@00528FF5 target cell; (2) FUN_004157b0 w 00401360 (pseudocode-level); (3) family setters w przepływie 004C47F0 (0085B3E0, 0085ADB0 — ten czyta [this+0xC], wzorzec konsumencki, 006B22D0) na INNYM this; (4) census setterów po vtable 0xA7DCB0; (5) ciała 00856090/00854D90. Denominatory: direct-B callees 7/7 otwarte; non-B callees ctora 0/9; creator-flow callees 2/15.

## 6. Standing

OWR-A01..A06 przyjęte addytywnie (CORRECTION_LEDGER). Stary run niemodyfikowany. Znane priory (CAND4/P/Q/slot3/loader/12B reader/13|25B header) nietknięte. Publikacja nie jest kanoniczną akceptacją nauki; nowe dowody zgłoszone do external postaudit bez samodzielnego awansu kanonu.

