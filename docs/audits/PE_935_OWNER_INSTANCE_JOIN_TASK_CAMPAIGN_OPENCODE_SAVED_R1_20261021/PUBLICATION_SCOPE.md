# PUBLICATION_SCOPE

Do publikacji (repo SebastianKozlo/eudoria-clean, master, docs/audits/PE_935_OWNER_INSTANCE_JOIN_TASK_CAMPAIGN_OPENCODE_SAVED_R1_20261021/):
- REPORT.md (sanitizowany opis nauki — wlasne zestawienia, zero raw instruction rows/disassembly)
- HANDOFF.md
- DERIVED_CLAIMS.json (kopia CLAIMS.json — naglowki/anchory bez tresci instrukcji)
- RESOURCE_INSTANCE_TRANSFORM_MATRIX.csv
- QC_FINDINGS.json
- FIRST_MISSING_EDGE.json
- STAGE_ACCEPTANCE_GATES.csv
- PUBLICATION_SCOPE.md (ten plik)
- manifest publikacji (wygenerowany pub_manifest.py)
- dokladnie jeden nowy wiersz AUDIT_ENTRYPOINT.md (newest-first)

NIE publikuje sie: PACKETS (raw instruction rows), JOBS (raporty dzieci z cytatami instrukcji/adresami w formie raw), SOURCE_ADMISSION_EVENTS (sciezki lokalne), BODY_AND_BUDGET_LEDGER, ROLE_LEDGER (session IDs), IDENTITY_MAP (adresy maszynowe w formie raw rows? — NIE: IDENTITY_MAP zawiera wylacznie wlasne opisy symboliczne; ale dla ostroznosci zostaje local-only), SELF_REVIEW*, INPUT_RECHECK, JOIN_DECISION_R1 (zawiera cytaty adresow w formie zestawien — decyzja: local-only, tresc zmapowana w REPORT), artifact_index.csv (lokalne sciezki).

Sanitizacja: sprawdzono kazdy publikowany plik pod katem: brak raw instruction text/disassembly, brak hex payload, brak promptow/odpowiedzi modeli, brak DB dump, brak config/env/secrets. Adresy funkcji (VA) wystepuja jako symbole analityczne (np. 008544D0) — to sanitizowane opisy pochodne, nie raw listing.
