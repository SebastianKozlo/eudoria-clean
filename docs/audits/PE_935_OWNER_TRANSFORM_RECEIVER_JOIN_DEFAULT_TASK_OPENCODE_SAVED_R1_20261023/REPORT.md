# REPORT — PE_935_OWNER_TRANSFORM_RECEIVER_JOIN_DEFAULT_TASK_OPENCODE_SAVED_R1_20261023

RUN_STATUS=COMPLETED (bounded; science/QC/seal/publish executed to terminal)
SCIENCE_VERDICT=PARTIAL_PASS_WITH_NEW_CONFIRMED_HOPS (receiver identity + ctor scoped negative + wire 12B)
PROCESS_VERDICT=PARTIAL_NONCOMPLIANT (1 admission-chronology incident disclosed, seq3; 2 EMPTY worker finishes charged; accounting corrections applied)
CANONICAL_GATE_EFFECT=NONE
AUTHORITY_STATUS=ADVISORY_PRE_QUALIFICATION

## 1. Pytanie główne i wynik

Cel kampanii: właściwy receiver dwóch pominiętych owner-callsite'ów CALL 0085CDE0 i brakujący writer obiektu receivera. Wynik:

- OWNER_CALL_A (005284AC, funkcja 00528380): receiver = [owner_this+0x0C] (row181598), arg2=1 → warunkowa kopia 13 DWORD do X+0x30 AKTYWNA, 13. dword 1.0f pisany przez caller (FLD1/FSTP 181591-181592); arg1 = lokalny blok 48B (9 REP MOVSD + sumy na +0x24/+0x28/+0x2C). Stack map 12 PUSH/0 POP, ESP przy CALL = E0-0xA0.
- OWNER_CALL_B (00528A00, funkcja 00528810): receiver = [owner_this+0x0C] (row182001), arg2=0 → kopia SKIPPED; arg1 = lokalny blok E1+0x18, część macierzy pisana przez 0085bfa0 (INFERRED z arytmetyki slotów — jedyny kandydat-writer in-span). DEAD PUSH ECX (181967) poprawnie wykluczony z argumentów.
- D_AND_X_WRITER: ani derived ctor 00528E50 (pełne ciało 182360-182498), ani base ctor 0085B1B0 (0085B1B0-0085B31E, RET 0xC) nie pisze this+0x0C/this+0x10 nonzero — oba pola są ZERO-init w konstruktorach. Nonzero writer receivera żyje w ścieżce post-init (frontier: caller flow 004C46C0 po CALL 004C47C1, settery rodzinne).
- Klasa ownera: 00528E50 = ctor wywołujący bazę 0085B1B0(this,arg1..3) i instalujący vtable [this]=0xA7DCB0 (po bazowym 0xA91E4C); RET 0x10 (4 argi). 00528380/00528810 są metodami tej klasy (entry receiver = this).
- WIRE_WIDTH: 00412430 dekoduje vec3 = 12B na dekod (LEA EAX,[EDX+0xc]; CMP EAX,[ECX+0x8]; JA fail; MOV [ESP+4],0xc; JMP 0040de60 tail; 0040de60: ADD [ECX+0xc],EAX). 13B/25B REFUTED. 1.0-default/scale REFUTED dla tych ciał (FLDZ = 0.0f na error path). Globalne 0xBA921C/20/24 są zapisywane do owner this+0x50/54/58 przez ogon base ctora (1169827-33) — rola wartości nadal nieokreślona poza samym zapisem.
- Slot5: NOT_RESOLVED_FROM_ADMITTED_DATA — vtable 0xA91E4C/0xA7DCB0 należy do klasy ownera, nie do pointee P=[R+0x2C]; vptr P nie występuje w admitted writerach.

## 2. Rozdzielczość aspektów (matryca)

- Record schema: 13-DWORD (9+3+1.0f@+0x30) — CONFIRMED (A1 + prior RH-A02).
- Head52 conversion: PARTIAL — 00864360 destination offsets i kolejność PRIOR-CONFIRMED; 00412430/0040DE60 teraz CONFIRMED (12B); gałąź GE 0096CDD0 po 0096CF00 nadal NIEOTWARTA (RH-A01 poprawka przyjęta, nie skonsumowana w nowym jobie — dostępne rows 1500525-1500780).
- Destination: lokalny blok 48B jako arg1 — CONFIRMED na obu site'ach.
- Actual root: 00528380/00528810 = metody klasy ctor-00528E50 (0x128B) — STRONGLY_SUPPORTED (identyczność klasy przez rodzinę ctor, nie runtime).
- Resource-instance join: X==[B+0x0C]==[D+4] UNPROVEN — kandydacka unifikacja z prior provider chain (R=[B+0xC], P=[R+0x2C], VT=[P], F=[VT+0x24]) jest spójna z delegacją [X+0x2C] slot5, ale równość [D+4]==[B+0xC] wymaga def-use, którego nie ma w admitted danych.
- Source medium: CURSOR_SOURCE_MEDIUM=UNKNOWN.
- Historical evidence: WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED.

## 3. QC

QSCIENCE1 (receiver hop, C01-C07): QC_PASS, 252 ekspozycje, wszystkie kontrmodele FAIL-negatywnie (twierdzenia się bronią). QSCIENCE2 (ctor negative + wire, C08-C14): QC_PASS, 243 ekspozycje, samodzielnie przeliczony census store'ów i re-derive wire. QACCOUNT: QC_PARTIAL — D1-D5 administracyjne (call units 48→49, finalizacja draftu, flagi SD ledger, semantyka rezerwacji), zastosowane przez mastera; zero defektów nauki. Promowane wire/conversion claims miały ODDZIELNY fresh QC (kontrakt spełniony).

## 4. Proces

11 natywnych Task (8 workerów pe-reconstruction: 6 delivered, 2 EMPTY finish charged conservatively 130+139 ekspozycji; 2 fresh QC pe-master-auditor PASS; 1 QACCOUNT QC_PARTIAL z korektami). Depth1, max2 aktywne, zero nested. Ekspozycje kodu 1312/24000; unia wierszy 564/8000; ciała 6/80; CALL units 97/400; discovery 4 pliki (SD001-SD004, ciała decoderów odzyskane z saved corpus po metadata planie 0-rows w H5). Incydenty: seq3 (schema peek 3 wierszy przed pierwszym ADMIT — ujawnione, naładowane), seq7/seq13 (puste próby). Rezerwacje były górnymi boundami (seq21: 293 vs faktyczne 243) — bez naruszenia capów.

## 5. FIRST_MISSING_EDGE

Writer this+0x0C nonzero (post-ctor init: 004C46C0 flow po 004C47C1 / settery rodzinne) — domyka tożsamość receivera X i otwiera rozstrzygnięcie slot5 przez ctor/vtable P. Alternatywy w FIRST_MISSING_EDGE.json.

## 6. Standing

WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CURSOR_SOURCE_MEDIUM=UNKNOWN; CANONICAL_GATE_EFFECT=NONE. Statusy bazowe zachowane; priors P/Q/slot3/loader/plus4 nie resetowane. Poprzedni run zamknięty; zero resume/reseal.