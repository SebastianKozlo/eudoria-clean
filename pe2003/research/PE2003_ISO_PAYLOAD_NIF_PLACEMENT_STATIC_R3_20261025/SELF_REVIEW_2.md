# SELF_REVIEW_2 — Z01 closing (przegląd 2: promocja WORLD, standing, maszynowa spójność)

RUN_ID: PE2003_ISO_PAYLOAD_NIF_PLACEMENT_STATIC_R3_20261025 | Reviewer: pe-master-auditor (Z01, drugi niezależny przegląd własnych dokumentów) | 2026-10-25
Zakres: (a) zakaz promocji LOCAL→WORLD we wszystkich plikach pakietu; (b) dokładność standing blocku; (c) maszynowa spójność JSON/CSV/JSONL; (d) higiena językowa i statusy słownikowe. Metoda: pełna lektura własnych plików + programowa walidacja parsowania + grep słów kluczowych.

## Sprawdzenia wykonane (wyniki)

1. **Brak promocji LOCAL→WORLD:** wszystkie wartości liczbowe transformów w pakiecie etykietowane jako local/model-local/jednostki modelowe; wystąpienia „world" ograniczone do deklaracji zakresu (NO WORLD PROMOTION, WORLD_XYZ_RECOVERED=NO, NOT_ESTABLISHED) i cytatu kontrmodelu N02 (czułość A/B). Claim C-WLD-01 utrzymuje rozróżnienie status-wyniku vs status-danych. COMPOSED wartości podane wyłącznie jako „jednostki modelowe (AXIS_UNITS_FRAME=UNCALIBRATED)". WERDYKT: brak promocji — OK.
2. **Standing block dokładny:** porównanie znak-w-znak z blokiem podanym przez PE-MASTER (8 pól): PE2003_WORLD_XYZ_RECOVERED=NO; PE2003_HISTORICAL_PLACEMENT=NOT_ESTABLISHED; SOURCE (edycja ISO)=SERVER_DELIVERED_ONLY dla modeli (terrain LOCAL); LOCAL_SOURCE_EXHAUSTED=NO (PE42 reference frontier otwarty; ISO edition: dane modeli poza zasięgiem statycznym); AXIS_UNITS_FRAME=UNCALIBRATED; CANONICAL_GATE_EFFECT=NONE; EXTERNAL_POSTAUDIT=PENDING; ADVISORY — wszystkie obecne, bez roszczeń wykraczających. OK.
3. **Maszynowa spójność:** programowy re-parse: CLAIMS.json OK (45 claims; status_counts zgodne); SOURCE_PROVENANCE/SOURCE_HYPOTHESES/FRONTIER/RESEARCH_BACKLOG/ROLE_LEDGER/NATIVE_TASK_CENSUS/BUDGET_LEDGER/QC_FINDINGS/CORRECTION_DISPOSITION/INPUT_RECHECK/EXTRACTION_BARRIERS — json.load OK (12/12); BODY_ADMISSION_EVENTS.jsonl — 13 linii, każda parsowalna jako samodzielny obiekt JSON (13/13); CSV (ISO_PAYLOAD_INVENTORY 56 wierszy, BUILD_COMPARISON 56, NIF_TRANSFORM_CORRECTION 217, MODEL_INSTANCE_EDGE_MAP 16, STAGE_ACCEPTANCE_GATES 12) — Import-Csv OK.
4. **Statusy słownikowe:** CLAIMS używa wyłącznie 5-wartościowego słownika; werdykty runowe (COMPLETE/PASS/QC_PASS/NOT_PERFORMED) nie są mieszane ze statusem twierdzeń; rozróżnienie status-tezy vs dyspozycja-findingu vs status-runu utrzymane (C-NIF-02: REJECTED teza starej semantyki przy jednoczesnym potwierdzeniu findingu R2-A01).
5. **Higiena granic:** potwierdzone brakiem zapisów Z01 w jobs\ i QC\ (read-only; jedyny zapis w jobs\\I01\\recovered\\... — NIE, re-hash to odczyt); SCIENCE_STOP.json i MANIFEST_SHA256.csv nie istnieją w pakiecie (root je dopisze); zero bajtów payloadu gry (tylko hashe/offsety/VN stringów — sprawdzone w próbkach wszystkich plików tekstowych).

## Znalezione problemy (NAPRAWIONE w tekstach; odnotowane)

- **SR2-F01 (P3, naprawione):** QC_FINDINGS.json summary pierwotnie „resolved_by_c01": 10 — rzeczywiście skorygowanych findings przez C01 jest 8 (P2-QC1-01/02/03 + QC2-F01/F02/F03/F04/F05); pozostałe 2 to NOTE_FOR_NEXT_REVISION. NAPRAWIONE na 8.
- **SR2-F02 (P3, naprawione):** CLAIMS.json C-SRC-03 ograniczenia zawierały zniekształcone słowo „nieproowalny" (oraz nieadekwatną formę) — NAPRAWIONE na „niedowodliwy statycznie w pełni".
- **SR2-F03 (P3, naprawione):** HANDOFF.md pierwotnie „STAGE_ACCEPTANCE_GATES.csv (11/12 PASS…)" — plik zawiera 12 wierszy bramek, wszystkie PASS (2 z notami ERRATA w kolumnie nonpass_class, ale result=PASS). NAPRAWIONE na „12/12 PASS — wszystkie bramki PASS; klasy nie-pass puste".

## Ocena

Po naprawach: pakiet jest maszynowo spójny, standing dokładny, promocja WORLD nieobecna, słowniki statusów zachowane. Werdykt self-review: PASS po 3 naprawkach P3. Zastrzeżenie jakościowe: oba self-reviews wykonane przez tę samą sesję Z01 (niezależność sesji/roli niemożliwa w pojedynczym dziecku) — finalna weryfikacja należy do roota (seal) i ewentualnego EXTERNAL_POSTAUDIT.
