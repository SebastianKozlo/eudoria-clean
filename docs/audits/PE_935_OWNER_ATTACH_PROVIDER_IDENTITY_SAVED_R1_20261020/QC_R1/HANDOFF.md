# HANDOFF — QC_R1 (fresh internal QC, DEFAULT)

ASSIGNMENT_MODE: INTERNAL_QC (fresh, one level)
RUN_ID: PE_935_OWNER_ATTACH_PROVIDER_IDENTITY_QC_R1_20261020
PARENT_LOOP_ID: PE_935_OWNER_ATTACH_PROVIDER_IDENTITY_SAVED_R1_20261020
MILESTONE: OWNER ATTACH / PROVIDER IDENTITY (Etap A/B, EU935 saved corpus)
SCOPE: re-derivation 0085ACE9 + 0085CD17, ESP trace CD06..CD20, budgets, strict JSON/CSV (root+P01+P02)

QC_VERDICT: **REQUIRE_CORRECTIONS**

FINDINGS:
- **P1 F1**: evidence_status poza taksonomią (root R-C5,R-C7; P02-C5/C7 'SUPPORTED'; P02-C6/C9, P05-C2, P06-C3, P08-C2 'UNKNOWN') — blokuje PASS per CONTRACT §10; korekta: serializer, UNKNOWN→UNVERIFIED, SUPPORTED→STRONGLY_SUPPORTED/PLAUSIBLE, z retencją wersji.
- **P1 F2**: P06-C2 source_pin cytuje tylko admission P06 (Af3c179f81dac) dla wierszy P07 (A5742dd0b9845); wzorzec poprawny w root R-C4.
- **P2 F3**: P01/HANDOFF „1 body + 1 candidate" przeczy CONTROL (3/3).
- **P2 F4**: brak STAGE_ACCEPTANCE_GATES.csv w P01/P02 (P03..P08 mają).

NAUKA ZWERYFIKOWANA: P01-C1..C4 VERIFIED (stack local zero-init, out-buffer arg5/6, scoped negative attach); P06-C1 VERIFIED + ABI callee RET4 STRONGLY_SUPPORTED (path-join ESP consistency z oknem P07); P06-C2 treść VERIFIED; budżety 30/48, 652/9000, 50/300, 20/48 zgodne z niezależną sumą eventów; 52 JSON strict-parse bez duplikatów; CSV stałe szerokości.

FULL_READ_LOG_PATH: QC_R1/RUN_STARTED.json (sources_read/not_checked)
NOT_CHECKED: P03/P04/P07/P08 REPORT.md bodies (schema/statusy sprawdzone programowo); MODEL_DEFAULT_GATE.json; stan publikacji.
FINAL_REPORT_PATH: QC_R1/REPORT.md
GATES_PATH: QC_R1/STAGE_ACCEPTANCE_GATES.csv
MANIFEST_PATH: QC_R1/artifact_index.csv
FILES_CHANGED: tylko QC_R1/* (5 nowych plików); żadne źródła sealed nie były modyfikowane.
UNRELATED_WORK_EXCLUDED: brak.
NEXT_PARENT_ACTION: zlecić korekty F1–F4 (serializer, retencja), potem obowiązkowy final recheck zmienionych claimów i konsumentów (świeży QC), potem dalsza nauka: serialize-entry binding [ESP+0x34] (FIRST_MISSING_EDGE).
