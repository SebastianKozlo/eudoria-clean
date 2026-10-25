# HANDOFF — R4

AUDIT_OUTPUT_ROOT = D:/Eudoria_Reconstruction/99_Audits/PE2003_ISO_ARCHIVE_RESOURCE_INSTANCE_PLACEMENT_STATIC_R4_20261025
WORK_ROOT = D:/Eudoria_Reconstruction/PE2003/10_Campaigns/PE2003_ISO_ARCHIVE_RESOURCE_INSTANCE_PLACEMENT_STATIC_R4_20261025
RECEIPT_ROOT = D:/Eudoria_Reconstruction/99_Audits/PE2003_ISO_ARCHIVE_RESOURCE_INSTANCE_PLACEMENT_STATIC_RECEIPT_R4_20261025
FINAL_REPORT_PATH = AUDIT_OUTPUT_ROOT/REPORT.md
PRIMARY_EVIDENCE_PATHS = jobs/M01/data/ARCHIVE_PRODUCER_CERTIFICATE.json; jobs/L01/data/MODEL_ID_SEARCH.json + EU_REVALIDATION.json + DENOMINATOR.json; jobs/J01/data/MODEL_INSTANCE_EDGE_MAP.json + TRANSFORM_SOURCE_MAP.json; jobs/J02/data/RECORD_TYPE_AND_SOURCE_MAP.json; jobs/N01 (parser v2 + regenerated); QC/QC1 + QC/QC2
RUN_STATUS = SCIENCE_COMPLETE_PENDING_PUBLICATION
HARD_STOP_REASON = none (static campaign goals bounded-exhausted; remaining edges require dynamic trace or external unit acquisition — both outside the static contract)

## Wznów tu (resume instruction)
1. Człowiek decyduje o następnej kampanii: (a) dynamiczna (trace argumentów fabryki 0x4578E0, entry-set, [renderer+0x28]) — wymaga autoryzacji wykonania klienta 5.1.0.0 z udostępnionych plików R3-recovered; (b) pozyskanie PE_PCG.ark/FullDat z zewnętrznych archiwów; (c) starszy build ClientLoadera (konsument Download.data).
2. Obowiązuje: frozen R2/R3/R4 read-only; era-labeling wariantów NIF; PE42/EU935 = referencje, nie substitucje.
