# PRIOR_CANON_PLACEMENT_VERDICTS — Stage A (PE_WORLD_R2_PLACEMENT_SOURCE_R1_20261031)

Wszystkie werdykty wyekstrahowane Z PLIKÓW P1–P5 (read-first; re-hash PASS przed startem,
patrz REPORT §Startup). Żaden werdykt nie pochodzi z pamięci. Era: PCG_9_3_5.

## P1 — PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913 (primary: 06_REPORT/REPORT.md)
| Werdykt (cytat/istota) | Plik dowodowy | Status |
|---|---|---|
| Producent transformacji statyków = UNKNOWN-with-exact-boundary; transform wchodzi do rekordu placementu wyłącznie z drzewa atrybutów encji (FUN_00846840/00854720) | 06_REPORT/REPORT.md §1; 02_ANALYSIS/Z1_producer.md; Z2_cwo_chain.md | STANDING |
| .prt (Portals.bnt) = wyłącznie cell-graph dPVS, NIE nośnik placementów; 0 trafień 13 kotwic × 276 plików | 02_ANALYSIS/Z3_portals.md; 01_RAW/…S12_PRT_CONTENT_CHECK.json (pakietu P1) | STANDING |
| Hipotezy H1–H4 otwarte; network-first odrzucone jako ZAŁOŻENIE (ERRATA_R2) | REPORT §1; P5 06_REPORT/ERRATA_R2.md [E-3] | STANDING |

## P2 — PE_935_STATIC_PLACEMENT_DESKTOP_AUDIT_R1_20260913 (primary: REPORT.md)
| Werdykt | Plik dowodowy | Status |
|---|---|---|
| Brak lokalnego zapisu placementu NIE został wykazany; negatyw bajtowy = ANCHORS_ABSENT_SEMANTICS_OPEN (F3); "Nie wykluczono lokalnego zapisu placementu" | REPORT.md §F3, §"Poprawiony checkpoint" | STANDING (ograniczenie zakresu negatywu) |
| F1: most templates.vfs.A→ArkObject+0x28 wycofany (kontrprzykład proweniencji odbiorcy gettera A) | REPORT.md §F1; probe.json checks.receiverCounterexample | STANDING |

## P3 — PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z (primary: 06_REPORT/FINAL_REPORT.md)
| Werdykt | Plik dowodowy | Status |
|---|---|---|
| Autorytatywny raport naukowy = 06_REPORT/DRAFT_FINAL_REPORT.md (publikacja bez nowej nauki); NiNode transform copy-chain slot-27 STRONGLY_SUPPORTED | 06_REPORT/DRAFT_FINAL_REPORT.md; 01_RAW/C10V2_BYTE_CROSSCHECK.json | STANDING |
| Brak dekodu payloadów .bvi w tym pakiecie (run dotyczył binarium/NiNode) | FINAL_REPORT.md CHANGED_PATH_CENSUS (brak artefaktów bvi) | STANDING |

## P4 — PE_935_PARAMETER_RECORD_ATTRIBUTE_INSERTION_R1_20261004 (primary: FINAL_REPORT.md)
| Werdykt | Plik dowodowy | Status |
|---|---|---|
| PARSER_TO_RUNTIME_VALUE_SEAM = CONFIRMED (templates.vfs id2=16083 → klucz+wartość → insert do rejestru RB-tree DAT_00BA1824) | FINAL_REPORT.md §"THE ONE QUESTION"; 01_RAW/S4_RECORD_ANCHOR_AND_SCANS.json | STANDING |
| PLACEMENT_CONSUMER_EDGE = STRONGLY_SUPPORTED; PHYSICAL_RECORD_TO_PLACEMENT_ATTRIBUTE = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO; MODEL_JOIN_EXECUTED = NO | FINAL_REPORT.md TERMINAL FIELDS | STANDING |
| FIRST_MISSING_EDGE = INSERTED_VALUE_TO_PLACEMENT_CONSUMER (provenance runtime value class-selector-20006/property-tag-6) | FINAL_REPORT.md §FIRST_MISSING_EDGE | STANDING |

## P5 — PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913 (primary: 06_REPORT/00_FINAL_REPORT.md)
| Werdykt | Plik dowodowy | Status |
|---|---|---|
| JOIN A→`<A>.nif` = 3,618/3,618 (100%), per-record 5,438/5,438; Models.bnt = 5,596 wpisów .nif, 0 duplikatów | 01_RAW/Z2_JOIN_RESULT.json; Z2_JOIN_A_TO_NIF_DETAIL.csv | STANDING |
| BONUS JOIN B→`<B>.bvi` = 1,666/1,666 unikalnych niezerowych B; per-record 1,692/1,692; Volumes.bnt = 1,865 wpisów .bvi (0 duplikatów) | 01_RAW/Z2_JOIN_RESULT.json; Z2_JOIN_B_TO_BVI_DETAIL.csv; Z2_VOLUMES_BNT_INDEX_NAMES.csv | STANDING |
| **Payloady .nif/.bvi NIE badane w P5** ("nie badano payloadów .nif/.bvi (zakaz ekstrakcji)") — join tylko na poziomie NAZW | 00_FINAL_REPORT.md §6 SELF_CHECK/NOT_CHECKED | STANDING (otwiera payloadowe pytanie tego runu) |
| E (world transform instancji) = UNVERIFIED; D = REJECTED as worded | 02_ANALYSIS/Z1_CLAIMS_MATRIX.md | STANDING |

## Kanon poza P1–P5, era 2003 (etykieta ery! — NIE bindujący dla PCG_9_3_5)
- BVI (Volumes.bnt, era 2003, 2,571,628 B / 1,807 wpisów) = LOKALNE MESH-e kolizyjne, NIE world placement;
  BVI ID = NIF ID + 1 (60% korelacji); "DO NOT scan BVI for model IDs as world placement".
  Źródło: skill pe-bnt-tdf (verified 2026-07-30, era 2003 PE_Terrain). Status: STANDING dla ERY 2003;
  dla PCG_9_3_5 — HIPOTEZA wstępna wymagająca niezależnej weryfikacji (dokonanej w tym runie).

## Wniosek Stage A
Żaden pakiet P1–P5 nie rozstrzygnął ani nie odrzucił pytania payloadowego .bvi dla PCG_9_3_5
(P5 jawnie nie dekodował payloadów). **Brak podstaw do HARD STOP PRIOR_CANON_ALREADY_RESOLVED.**
Pytanie tego runu (dual-independent decode payloadów .bvi + struktura) jest legalnie otwarte.
Re-derivacja uniknięta: nie powtarzano joinu nazw (P5 STANDING), censusu .prt (P1), seam parser→rejestr (P4).
