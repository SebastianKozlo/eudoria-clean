# HANDOFF — PE_935_OWNER_INSTANCE_JOIN_TASK_CAMPAIGN_OPENCODE_SAVED_R1_20261021

AUDIT_OUTPUT_ROOT = D:\Eudoria_Reconstruction\99_Audits\PE_935_OWNER_INSTANCE_JOIN_TASK_CAMPAIGN_OPENCODE_SAVED_R1_20261021
FINAL_REPORT_PATH = <root>\REPORT.md
PRIMARY_EVIDENCE_PATHS = PACKETS\J01..J17 (piny w ticketach + SOURCE_ADMISSION_EVENTS.jsonl), JOBS\<id>\ raporty dzieci, JOIN_DECISION_R1.md, IDENTITY_MAP.json, CLAIMS.json
RUN_STATUS = COMPLETED_SCIENCE_SEALED (patrz artifact_index.csv + manifest LAST)
HARD_STOP_REASON = brak blokera; terminal: dozwolone drogi saved-source wyczerpane w ramach cap; KEY_MATCH/F_slot24/MODEL_RESOURCE wymagaja danych poza saved corpus (lista w FIRST_MISSING_EDGE.json)

Dla nastepnej sesji:
- Nie powtarzaj admission zamknietych okien (ledger A001..A019); re-read nie zwieksza union, ale wymaga zdarzenia.
- Nastepne P0: (1) eksport 00414130 + tail 004154F0 (KEY_MATCH), (2) identyfikacja vtable providera (F_slot24), (3) sciezka MODEL_RESOURCE. Kazde wymaga decyzji admission czlowieka o nowych eksportach/limited discovery.
- Prior kanon corrections: provider-chain czyta sie w 0085bfa0 (nie w 00527AB0); T01/T02 to caller 0048ecc0 regionu 0048e9c3-family; piata LEA to count-writer; „keyed" i „wspolny rejestr" maja wording-type corrections (patrz QC_FINDINGS.json).
