# REPORT — PE_935_SCENE_INSTANCE_TRANSFORM_JOIN_SAVED_R1_20261019

RUN_STATUS=COMPLETED_SCIENCE_PHASE_CLOSED. Autor wykonawczy: pe-reconstruction (P01) + PE-MASTER DIRECT_ANALYST_FALLBACK (P02-P04, po udokumentowanych pustych sesjach workera — patrz DISPATCH_LEDGER D02-D10); świeże QC: pe-master-auditor (QC_R1, PASS_WITH_FINDINGS, 9 findings, 2xP1 skorygowane in-place przed seal).

## RUN_STATUS / SCIENCE_VERDICT / PROCESS_VERDICT
- SCIENCE_VERDICT=PARTIAL_PASS_WITH_STRONG_STRUCTURAL_RESULTS: single-receiver thread CONFIRMED, owner class CONFIRMED (facts)/STRONGLY_SUPPORTED (name), transform mechanism CONFIRMED, transform DATA origin UNKNOWN.
- PROCESS_VERDICT=PARTIAL_NONCOMPLIANT_INHERITED_PATTERN: six empty worker sessions (D02-D09) triggered the contract fallback path; scientific dispatch switched to documented PE-MASTER fallback; QC independence preserved (fresh auditor session, byte-verified packages). No incident debits; budgets within caps.

## INHERITED_DEFECTS
Stary root PAIR_REDUCER_CONSUMER_SAVED_R2 ma 78 plików (76+manifest+CONTROL/EP_ROW.txt) — przypięty jako INHERITED_NONPASS w BASELINE_EXCEPTIONS; guard check potwierdził niezmieniony snapshot. Publiczne manifesty poprzednika mają po 1 hash mismatch i po 2 pominięte metadane — naprawa addytywnymi sidecarami PUBLICATION_REVALIDATION_R1 (poza tym rootem, w projekcji publikacji).

## Wyniki (INSTANCE/TRANSFORM graph)
1. OWNER_IDENTITY: klasa pochodna od MovableObject (base vtable 0xA91E4C, derived vtable 0xA7DCB0; ctor 00528E50, base ctor 0085B1B0 RET 0xC; type id w +0x8; pola +0xA4..+0x124). Nazwa klasy: etykieta dekompilatora z RTTI poprzedniego zamrożonego runu — STRONGLY_SUPPORTED.
2. RECEIVER_POINTER_ORIGIN: ECX@00527AF9 = [owner+0xC] — pole membera, zerowane przy konstrukcji, receiver podłączany później przez nieznanego writera.
3. RECEIVER (mechanika): polimorficzny obiekt o slotach vtable+4 (set-position-like) i +0xC (getter trio 0085B6A0, typowany przez [+0x8]∈{3,4,5,6,7}); przechowuje transform copy w +0x30, floaty +0x54/+0x58/+0x5C, data-address w +0x2C (subobiekt +0x14, slot +0x18).
4. TRANSFORM_SOURCE: 0085BFA0 czyta [receiver+0x2C] (data address, 12 floatów — frozen R2); konsumenci (00527AA0, 0085C130, 00528810)blendują tria z factor S1 (arg2 float lub [owner+0xE0]/[owner+0xE8]); writer data-address NIEUSTALONY — to FIRST_MISSING_EDGE.
5. FIELD_2C_WRITER: w dopuszczonym korpusie tylko (a) bit0-flaga or/and na [owner+0xC0] (ctor 00528E50, bramkowany predykatem typu 0085B750 {2..7}) i (b) zera konstrukcyjne (007345C0). Żaden nie pisze data-addressu receivera.
6. STORED_OBJECT_CLASS([owner+0xC0]): produkt fabryki 00401360->00485050->0048CBB0->005247C0 — klasa UNKNOWN; setup metodami 005094C0/509510/509070/509850 z trio ownera +0x44/+0x50/+0x5C.
7. SLOT17 (Etap C): NIE BADANE w tym runie — główna gałąź nie była data-blocked (kontrakt §8: alternatywa opcjonalna); status pozostaje jak w SCIENCE_CHECKPOINT (prefix starego runu = materiał do rekwalifikacji, nie nowy wynik).
8. HISTORICAL_TRANSFORM: brak odtworzonych XYZ; brak placement. WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CURSOR_SOURCE_MEDIUM=UNKNOWN; CANONICAL_GATE_EFFECT=NONE.

## FIRST_MISSING_EDGE
Writer [receiver+0x2C] (data-address 12 floatów) + writer/attach [owner+0xC]. Premises i denominator w FIRST_MISSING_EDGE.json.

## Budżety
reserved/charged: 34 bodies / 413 rows / 35 CALL / 34 candidates / 712 document lines (union = reserved, brak dubli); 0 incident debits. Budżety globalne: 48/9000/300/48/3000.

## QC_ORIGIN
QC_R1 (pe-master-auditor, świeża sesja): PASS_WITH_FINDINGS; niezależnie przeliczone ESP/FPU/push-shift/budżety/łańcuch eventów/piny; findings F1-F9 (2xP1, 7xP2) — wszystkie ACCEPTED, P1 skorygowane in-place (CORRECTED_PER_QC_F1/F2), P2 skorygowane lub odnotowane w QC_DISPOSITION. To QC wewnętrzne, nie zewnętrzny postaudyt; werdykt runu nie jest MASTER_ACCEPTED.

## MANIFEST
Root manifest zapisany ostatni (po STOP) przez evidence_guard seal; verify po seal. Publikacja wyłącznie poza sealed root.
