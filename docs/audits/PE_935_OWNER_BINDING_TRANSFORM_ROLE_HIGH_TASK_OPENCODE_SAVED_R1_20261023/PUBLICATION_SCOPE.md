# PUBLICATION_SCOPE — PE_935_OWNER_BINDING_TRANSFORM_ROLE_HIGH_TASK_OPENCODE_SAVED_R1_20261023

## Co jest publikowane (sciezki tego commita)
- docs/audits/PE_935_OWNER_BINDING_TRANSFORM_ROLE_HIGH_TASK_OPENCODE_SAVED_R1_20261023/: REPORT.md, HANDOFF.md, DERIVED_CLAIMS.json, RESOURCE_INSTANCE_TRANSFORM_MATRIX.csv, QC_FINDINGS.json, FIRST_MISSING_EDGE.json, STAGE_ACCEPTANCE_GATES.csv, PUBLICATION_SCOPE.md, EXTERNAL_POSTAUDIT_SUMMARY.md, PUBLICATION_MANIFEST.csv (strict per-file manifest, self-excluded; 11 rows / 12 pathow lacznie z manifestem).
- docs/audits/PE_935_OWNER_VIRTUAL_SETTER_SCENE_BRIDGE_DEFAULT_TASK_OPENCODE_SAVED_R1_20261023/POSTAUDIT_NOTICE_R1.md — NOWY plik addytywny (brak konfliktu z istniejacymi notice w BASE; zaden dawny notice nie jest modyfikowany).
- AUDIT_ENTRYPOINT.md — dokladnie jeden nowy wiersz newest-first w tabeli LATEST RUNS (1 insertion / 0 deletions; zadna historyczna komorka niezmieniona).

## Sanitizacja
- Publikowane sa wlasne wnioski, klasyfikacje, referencje wierszy (VA+H5line) i piny/provenance.
- NIE publikuje sie: RAW packetow, listingow instrukcji zrodlowych, SDK source, payloadow, promptow, odpowiedzi/reasoning modeli, tresci DB, sekretow, konfiguracji.
- Publiczne projekcje zapisane jako UTF-8 (bez BOM); odpowiadajace artefakty lokalne w sealed package moga nosic BOM — opisana transformacja kodowania, nie deklaracja falszywej byte parity. Referencja integralnosci jest lokalny sealed package: MANIFEST_SHA256.csv (86 rows + manifest = 87 plikow, pin C2E9EABA48439EB03081D24A372617874EE1B686DF595F0BD6C2110B824A4072). Em-dash w publicznych projekcjach przywrcony tam, gdzie zapis lokalny mial znak zutraciony; tresc merytoryczna bez zmian.
- EXTERNAL_POSTAUDIT_SUMMARY.md = kopia przypietego PUBLIC_SUMMARY niezaleznego postaudytu VSB (I0576, 4602 B, SHA256 636149648F54790ACCF2C96BA4C5BD599E5FB382FB1444DE01A0DBCF08BD54CB).

## Status
- Publikacja nie jest kanoniczna akceptacja nauki. SCIENCE_VERDICT = PARTIAL_PASS_WITH_MATERIAL_CORRECTIONS; PROCESS_VERDICT = PARTIAL_NONCOMPLIANT (ujawnione incydenty: doc_lines ~32k/12k; QSCR reservation overshoot +48; QACCOUNT doc lines 774/600).
- WORLD_XYZ_RECOVERED = NO; HISTORICAL_PLACEMENT = NOT_ESTABLISHED; CURSOR_SOURCE_MEDIUM = UNKNOWN; CANONICAL_GATE_EFFECT = NONE; DESKTOP_POST_AUDIT = PENDING.
- Era: PE_EU_9_3_5_SAVED_ONLY. Bez oryginalnych EXE/assets, bez runtime, bez nowych eksportow Ghidry, bez wykonywania SDK.
