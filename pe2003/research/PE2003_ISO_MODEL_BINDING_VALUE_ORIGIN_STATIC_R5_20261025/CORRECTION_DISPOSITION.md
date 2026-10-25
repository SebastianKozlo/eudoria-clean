# CORRECTION_DISPOSITION — PE2003_ISO_MODEL_BINDING_VALUE_ORIGIN_STATIC_R5_20261025

RUN_ID: PE2003_ISO_MODEL_BINDING_VALUE_ORIGIN_STATIC_R5_20261025 | BUILD: ISO2003NOV_PE_5_1_0_0 | DATE: 2026-10-25
PROVENANCE: FINDINGS_R4.json (AUTHORING ROOT REV2), PA_RECONCILIATION.md, QC/QC1/QC_FINDINGS.json, QC/QC2/QC_FINDINGS.json, jobs/J03/data/ERRATA_J01_J02.md, jobs/J03/data/MODEL_BINDING_CERTIFICATE_J03_CORRECTED.json (CORR1), jobs/D03/data/D03_EVIDENCE_STRICT.json, QC/QC1/QC_VERIFIED_ITEMS_STRICT.csv, BUDGET_LEDGER.json. All dispositions ADDITIVE (frozen sources untouched); every correction projection re-derives from image bytes with its own provenance block.

## 1. R4 findings A01..A12 — zastosowanie addytywne w R5

| ID | Zastosowanie w R5 | Status |
|---|---|---|
| R4-A01 | A01/A01R: I=[E+0x40] zapisywane przez a1 (89 46 40), push do lazy-create z literalem K=0 (push 0 @0x46E9D0); 46ECA0 ma jawny selektor K z komunikatu (J01 S9, K≠0 istnieje); ID→SFO+4, record→SFO+0x78 upheld | APPLIED |
| R4-A02 | CONFIRMED ROOT→instance NIE odziedziczone: J01-J05 utrzymały luki; certyfikaty per-model = CONDITIONAL_OPEN; join UNVERIFIED (CLAIMS C07) | APPLIED |
| R4-A03 | DrawIndexedPrimitive upheld; record+0x14/2C/30 nie XYZ; transform-sink REJECTED; R5 nie rehabilitował renderera (CLAIMS C15) | APPLIED (utrzymany) |
| R4-A04 | Rozstrzygnięty przez A01: scratch-slot [E+0x18] — dominująca definicja = store [E+4] @0x46EA02; "stale A6" REJECTED per callsite; ×100 scale w callerze, 0x46F0A0 kopiuje; brak etykiet osi | APPLIED + RESOLVED |
| R4-A05 | Literal-absence = scoped negative tylko; name-assembly '.nif'/'.dds'/'.tga' potwierdzone; brak globalnego consumer-absence (J01 S14, J02 T1; CLAIMS C16) | APPLIED |
| R4-A06 | Holder/vtable/getter/ABI analysis wykonana (D01-D04) zamiast deklaracji runtime-niezbedności; właściwy status UNRESOLVED_IN_BOUNDED_STATIC_PASS stosowany w BARRIER-ach | APPLIED |
| R4-A07 | Kontrmodele ról (kamera/lokalny węzeł/fizyka) nie odrzucone; brak roli world-root zadeklarowanej; WORLD_XYZ_RECOVERED=NO | APPLIED |
| R4-A08 | Anomalia 417BE7→414C9E/414C9F NIE naprawiona heurystycznie; gałąź T niewykonana w R5 (brak uzasadnienia) | APPLIED (no-op: edge untouched) |
| R4-A09 | Wszystkie finalne JSON/CSV R5 pisane serializatorem strict/csv.writer; błędne artefakty D03/QC1 naprawione NOWĄ projekcją (D03_EVIDENCE_STRICT.json, QC_VERIFIED_ITEMS_STRICT.csv), nie edycją | APPLIED |
| R4-A10 | R5 prowadzi prawdziwy append-only ledger (BODY_ADMISSION_EVENTS.jsonl, 14 eventów, seq 1-14, reserved_before_extraction=true, przed ekstrakcją) | APPLIED |
| R4-A11 | PARTIALLY_MEASURED≠within-budget: D01 breach nie zaextentowany na "within"; unique-row status UNVERIFIED; D03 dual-counting rozstrzygnięty przez podanie obu liczb + interpretację roota w ledgerze | APPLIED |
| R4-A12 | Stare locki: closing lock-scan (CLOSING_RECHECK_ROOT.md) = 5 plików PYC cache, brak aktywnych locków, LOCK_SCAN_DONE; brak wniosku o aktywnym writerze | APPLIED |

## 2. Adjudication PA (PA_RECONCILIATION.md) — rozstrzygnięcia

| Teza PA | Rozstrzygnięcie R5 | Status |
|---|---|---|
| Stale-A6 (CONFLICT) | REJECTED w callsite (writer 0x46E990): dominująca definicja slotu [E+0x18] = store [E+4] @0x46EA02; scratch read @0x46EA55 czyta ten sam absolutny slot | RESOLVED (A01/A01R, QC1 upheld) |
| A4_UNUSED | REJECTED (utzymane z PA-QC): a4 żywy — dispatch [vt+4]→0x5552C0 vec3-copy | RESOLVED |
| A1..A6 mapa | CONFIRMED_FOR_MEASURED_SCOPE bajtowo z podwójną weryfikacją (A01 + QC1); precyzje: a2 low-byte only, a3 dead-arg dla 555170 (zapisuje sam 5531F0) | RESOLVED |
| 42E9B0 vs 43C490 etykiety | Rozdzielone per callsite: 42E9B0=klasa tekstur, 43C490=konstrukcja strumienia, load=nested vt+8; etykiety globalne odrzucone | RESOLVED (J01 S5) |
| E7 model-instance join | UNVERIFIED upheld; luka zwężona do lane (b)/(d-res)/(e); 90-caller negative utrzymany SCOPED | UPHELD (open) |
| CLDLLPatcher UNVERIFIABLE_STATICALLY | REJECTED jako wniosek o niemożliwości — upheld; wnętrze nieprzeanalizowane w R5 (brak potrzeby); brak uruchomienia patchera | UPHELD |
| 46F0A0 readiness | EMULATION_DESIGN_ONLY upheld; brak emulacji w R5; LOCAL mechanism accepted (×100 w callerze, kopiowanie w 46F0A0) | UPHELD |
| Renderer 4DD421 applier XYZ | REJECTED upheld (DrawIndexedPrimitive kontrmodel stoi) | UPHELD |
| R4 budget promotion (PA-C) | Upheld: brak within-budget z częściowego pomiaru; D01 adjudykacja jawna | UPHELD |

## 3. QC1 — findings + dispositions (wszystkie ACCEPTED, zamknięte errata J03)

| ID | Sev | Finding | Disposition | Status |
|---|---|---|---|---|
| QC1-F01 | P1 | J02 "zero rel32 refs" dla 0x527A00/0x527BC0/0x498B80 — FAŁSZ (real call sites 0x47B8EF/0x47B8FD/0x485A02) | T10 zero-refs sub-claim REJECTED_AS_WORDED; bodies-construct CONFIRMED; redirected edge J03 (caller analysis) | CLOSED — ERRATA_J01_J02.md E2; J03 census (refusal+positive control); QC2 re-verified |
| QC1-F02 | P2 | J01 slot+0x8=42BA30 — błąd: slot+0x8=0x42B940, slot+0xC=0x42BA30 | Erratum slot index; semantic verdict (42BA30=reader) upheld | CLOSED — E1; REPORT sekcja 4 poprawiona wąsko |
| QC1-F03 | P2 | Algebra 57 witryn slot+0x3C się nie domyka (55 sklasyfikowane; brak 0x4551C4/0x56FA46) | Domknięcie klasyfikacji w J03: 0x4551C4 wyeliminowana (pełne okno, 1 push, ret 4≠ret 8); 0x56FA46 dodana do residual; finalna algebra 19+24+14=57 DOMKNIĘTA | CLOSED — E3; SLOT3C_CLASSIFICATION_J03.json; QC2 potwierdziło pustą różnicę symetryczną |
| QC1-F04 | P3 | Licznik plików J01 data/ 30 vs 34 | Nota; korekta licznika | CLOSED — E4; QC2 live count 34 |
| QC1-F05 | P3 | '.dds' 0x6B12C4 drugi konsument @0x4B61E4 pominięty | Erratum; claim nie twierdził ekskluzywności (incompleteness, nie fałsz); '.nif' only = TRUE upheld | CLOSED — E5; QC2 imm32 census = dokładnie 2 hity |

## 4. QC2 — findings + dispositions (wszystkie ACCEPTED)

| ID | Sev | Finding | Disposition | Status |
|---|---|---|---|---|
| QC2-F01 | P2 | J03 receiver = P (0x7C proxy), NIE [P+0x10]; brak loadu +0x10 w callerze A | Erratum projection przed sealem: CORR1 wydaje MODEL_BINDING_CERTIFICATE_J03_CORRECTED.json (byte-verified pins 0x47B8CB..0x527BD6, negative scan [reg+0x10]=0 w oknie caller-a); '[P+0x10]' sub-claim REJECTED_AS_WORDED; wnioski J3/J4 STRENGTHENED (visual slot nietknięty); J04 §0 inherited wording — nota (ERRATA_QC2_RECEIVER) | CLOSED — CORR1 (R5-CORR-001) |
| QC2-F02 | P2 | D03_EVIDENCE.json nieparsuje strict (proza bez cudzysłowów) | Nowa projekcja strict: D03_EVIDENCE_STRICT.json + ERRATA_QC2_COUNTS.md; frozen źródło nietknięte; treść naukowa niezależnie zweryfikowana | CLOSED — CORR1 |
| QC2-F03 | P2 | BUDGET_LEDGER nieaktualizowany; D01 ~71k rows > run cap 32000 bez adjudykacji | Root (PE-MASTER): addytywna korekta ledgera (rekonstruowane liczniki 13 admissions, caps block) + jawna ADJUDICATION D01: PROCESS_INCIDENT, evidence static-valid, scan-window prohibition od J03, unique-status UNVERIFIED | CLOSED — root adjudication 2026-10-25 (BUDGET_LEDGER.json) |
| QC2-F04 | P3 | D03/D04 prose 56/160 vs listy 54/154 | Erratum liczników w ERRATA_QC2_COUNTS.md (44F080=54, 44F050=154 E8; lub 55/158 E8+E9 z predykatem); werdykty leaf-getter nieobciążone | CLOSED (nota; nie blokował sealu) |
| QC2-F05 | P3 | QC1 QC_VERIFIED_ITEMS.csv fieldcount 5-9 + U+FFFD | Re-projekcja: QC_VERIFIED_ITEMS_STRICT.csv (5 pól, quoted, UTF-8) — wydana, bo CSV jest konsumowane przez closing/manifest tooling | CLOSED — CORR1 |
| QC2-F06 | P3 | "112−18 esp" niedreprodukowalne instrukcyjnie (0 realnych esp-readers; finalne 94 PRAWDA) | Wording note: rozdzielenie raw-byte-candidate counting od instruction-level counting w przyszłych projekcjach | RECORDED (nota; nie blokował sealu) |

## 5. CORR1 (R5-CORR-001, pe-reconstruction) — cele i wynik

Wykonane cele: (1) erratum receivera J03 (QC2-F01) — certyfikat CORRECTED z pełnym blokiem byte_verification_CORR1 i revalidation_predicate SATISFIED; (2) re-projekcja D03_EVIDENCE strict (QC2-F02); (3) re-projekcja QC1 CSV (QC2-F05). Zapisy wyłącznie addytywne; frozen RESULT/certyfikaty J03/D03/QC1 NIETKNIĘTE. Role CORR1: EXECUTOR (pe-reconstruction), korekcja pre-seal wg dyspozycji QC2 — odnotowana w NATIVE_TASK_CENSUS.json.

## 6. Rekalibracja statusów po korektach

Żadna korekta nie zmieniła kierunku werdyktu szczytowego: SCOPED_NEGATIVE non-closure mostu (C07) stoi i zostało WZMOCNIONE (receiver P zamiast [P+0x10] oznacza, że ścieżka nie dotyka nawet slotu wizualnego); żaden claim REJECTED nie został zrehabilitowany; żadna teza CONFIRMED nie została podniesiona z UNVERIFIED.
