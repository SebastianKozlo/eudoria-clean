# REPORT — OWNER FACTORY / ATTACH / LOOKUP — DEFAULT/MEDIUM, NATIVE TASK

RUN_ID = PE_935_OWNER_FACTORY_ATTACH_LOOKUP_DEFAULT_TASK_OPENCODE_SAVED_R1_20261023
RUN_STATUS = COMPLETED_SCIENCE_QC_SEALED (see HANDOFF for publication)
SCIENCE_VERDICT = PARTIAL_PASS_WITH_MATERIAL_NEW_RESULTS
PROCESS_VERDICT = PARTIAL_NONCOMPLIANT (retroactive peek disclosure V1 + late-logged worker READ events QA-1 + A3 length failure; all disclosed, corrected where possible)
CANONICAL_GATE_EFFECT = NONE
WORLD_XYZ_RECOVERED = NO
HISTORICAL_PLACEMENT = NOT_ESTABLISHED
CURSOR_SOURCE_MEDIUM = UNKNOWN

## 1. Cel i wykonanie

Cel: ścieżka od zarejestrowanego ownera B do instalacji obiektu sceny; writer/producer R=[B+0x0C]/D=[B+0x10]. Wykonano 8 natywnych workerów pe-reconstruction + 3 natywne QC pe-master-auditor (QSCIENCE, QACCOUNT x2), wszystkie parent-bound do jednej sesji root (DB mode=ro weryfikacja), max 2 aktywne, depth 1, bez nested.

## 2. Główne nowe wyniki naukowe

R1 (CONFIRMED, QC-literally re-derived): REGISTRATION PAYLOAD CHAIN — wrapper 00856190 wstawia do mapy mgr+0x10 wpis: klucz = [B+0x74] (przez getter 00414130), payload node+0x8 = B (zarejestrowany obiekt). Arytmetyka stosu E-relative: key slot E-0x10, B slot E-0xC, Q=E-0x10, Q+0x4=E-0xC=B-slot; fabryka 00854260 kopiuje [Q]->node+0x4, [Q+0x4]->node+0x8. QSCIENCE: C1-C5 CONFIRMED, C6 CONFIRMED_IN_PACKET.

R2 (CONFIRMED): mechanika mapy — open hashing: [this+0x8]/[this+0xC] bucket array, index = key % (N-1), node+0x0=next, node+0x4=key, node+0x8=payload; 008544D0/00971780 lookup zwraca [node+0x8] lub 0; 00854D90 find-or-insert; 00856090 reserve-only; flag byte [P+0x4]: 1=nowo wstawiony, 0=znaleziony istniejący.

R3 (STRONGLY_SUPPORTED): LOOKUP-TO-SAME-OWNER BRIDGE — lookup 008544D0 po kluczu [B+0x74] zwraca TEN SAM B (mapa via singleton mgr premise; namespace-key equality POSSIBLE_ONLY — nie zamknięte).

R4 (CONFIRMED): 0085B3E0 (cel A1) NIE jest setterem — zero własnych store'ów na receiverze; konsumuje [B+0x0C] (0085b48d/0085b522), dwa wywołania wirtualne vt+0xC/vt+0x4 (interiors UNKNOWN); stepped-movement.

R5 (CONFIRMED): drugi instalator vptr 0xA7DCB0 @005290A8 = 00529080, destructor/close-style (frees [B+0xC4] vector, call 0085B3A0 frees [B+0x3C]/[B+0x40], reinstall vptr); NIE writer. Census vptr: dokładnie 2 instalatory w całym H5.

R6 (PLAUSIBLE_NEGATIVE_BOUNDED): NONZERO WRITER B+0x0C/B+0x10 — NOT_OBSERVED_IN_BOUNDED_SEARCH (prior: pełny ctor + 7 helperów + creator; this run: pełny łańcuch mapy, 0085B3E0, 00529080, 0085B3A0; censuses: 11442 pattern-stores/133 family/2 vptr/~1800 allocator). Jedyne udowodnione zapisy: zero-init 0085B1B0 (value 0). NOT_TESTED_CLASSES jawne (indirect/alias stores, inne szerokości, interior vt+0xC/vt+0x4 — vtable DATA nieobecne w H5, slot targets NOT_RECOVERABLE_FROM_SAVED; runtime forbidden).

## 3. OPEN / FIRST_MISSING_EDGE

FIRST_MISSING_EDGE = rzeczywiste funkcje vt+0xC / vt+0x4 vtable 0xA7DCB0 (potencjalna warstwa writer/producer R) — NOT_RECOVERABLE_FROM_SAVED (brak sekcji danych vtable w H5 listing). Druga krawędź: equality klucza insert-vs-lookup namespace. Następny testowalny hop z saved: pakiet 00854E11 (empty-bucket path) + caller-side [found+0x8] read w 008544D0 w celu domknięcia R3 do CONFIRMED.

## 4. Proces

START seq1, exclusive-create SCIENCE/RECEIPT, preflight PASS (authoring 33/34, postaudit 25/26), OPR-A01..A06 przyjęte addytywnie. 10 prób Task (32 cap): 8 stop + 1 length (A3 — retry split A3R+A5 per ladder, oznaczone INTERPRETIVE) + QACCOUNT2. Ekspozycje 1109+ (24000 cap), unique rows ~596 (8000), bodies 11 (80), CALL units 46 (400), kandydaci 2 (64). QSCIENCE: QC_PASS_WITH_FINDINGS. QACCOUNT: attempt1 FAIL (pin mutation by design, F1-F5) -> fix -> attempt2 QACCOUNT_PASS_WITH_FINDINGS (defekty wyłącznie dokumentacyjne, naprawione). Znane niekompliance (disclosed): 78 master peek rows przed per-range ADMIT (INCIDENT seq22, V1 P3); 4 late-logged READ events (QA-1, closed pre-STOP); UNMEASURED: REQUEST_EFFORT=NOT_OBSERVED, SERVER_EFFECTIVE_EFFORT=UNKNOWN (client medium only).

## 5. Granice

Saved-only (H5 + prior canon); bez runtime/EXE/assets/nowych eksportów. Wszystkie frozen pakiety nietknięte. Historyczne placement/XYZ nieodzyskane; wyniki zgłoszone do external postaudit bez samodzielnego awansu kanonu.
