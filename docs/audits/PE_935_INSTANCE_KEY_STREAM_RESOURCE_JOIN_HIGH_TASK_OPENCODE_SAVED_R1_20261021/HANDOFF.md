# HANDOFF — PE_935_INSTANCE_KEY_STREAM_RESOURCE_JOIN_HIGH_TASK_OPENCODE_SAVED_R1_20261021

AUDIT_OUTPUT_ROOT = D:\Eudoria_Reconstruction\99_Audits\PE_935_INSTANCE_KEY_STREAM_RESOURCE_JOIN_HIGH_TASK_OPENCODE_SAVED_R1_20261021
FINAL_REPORT_PATH = AUDIT_OUTPUT_ROOT\REPORT.md
PRIMARY_EVIDENCE_PATHS =
  JOBS\K01_KEY_FIELD_RECON\K01_RESULT.md + RAW\K01_H5_ROWS_0085B1B0_0085B260.txt
  JOBS\K02_STREAM_CALLER\RAW\range_a..d (4 files) + K02_RESULT_RECOVERED.md + DB_RECOVERY_reasoning_both_attempts.md
  JOBS\K03_SCENE_JOIN\K03_RESULT.md + RAW\H5_A1/A2/B1/B2 + GA3_JSON_QUERY_LOG.txt
  JOBS\QCA\QCA_RESULT_RECOVERED.md + QCA_DB_RECOVERY_reasoning.md
  JOBS\B3_RESOURCE_TYPING\B3_RESULT_RECOVERED.md + RAW ranges a/b + B3_DB_RECOVERY_reasoning.md
  JOBS\B4_EMPTY_BUCKET\B4_RESULT_RECOVERED.md + B4_RAW_00851610_00851700.txt + B4_DB_RECOVERY_reasoning.md
  JOBS\B5_FIELD_WRITE\B5_RESULT.md + RAW\B5_006e8f70_rows.txt
  JOBS\B6_CHILD_AND_NODE\B6_RESULT.md + RAW\RAW_range_00854260_00854300.txt
  JOBS\B7_KEY_CONSUMER\B7_RESULT.md + RAW\B7_RAW_H5_ROWS_0048e740_0048e800.txt
  JOBS\B8_REAL_CONSUMER\B8_RESULT.md + RAW\B8_H5_ROWS_005b47c0_005b4860.txt
RUN_STATUS = COMPLETED_WITH_DATA_BARRIERS (see REPORT.md sec.1/3)
HARD_STOP_REASON = none (science closed adaptatively within budget; terminal per contract sec.11-13)

## Co dziedziczy następny run (mapa, nie nauka)
1. FIRST MISSING EDGE: klasa/RTTI obiektu A (join child == A == FUN_007CE1E0([manager+0x70])).
   Bounded cost: (a) census vtable/RTTI w saved materiałach (GA3 ma tylko sloty 0-39; potrzebny
   inwentarz RTTI stringów lub vtable imm); (b) bounded window FUN_007CE1E0 (getterA body).
2. Message upstream producer level 3: callerzy FUN_004B1890 + writer bufora payload (sieć vs lokalna).
3. 0067a9e0 (lookup w 005b47c0) + semantyka vslot+0x8 dispatchu.
4. SF_from_Bctor == SF_at_CAND4_join (identity proof wymagany; symbole w IDENTITY_AND_TIME_MAP.json).
5. Transform konsumenci (Etap C) — dopiero po semantyce A.
6. Bodies 006C0F90/006C10B0 (EDI preservation #1/#2); vtable DATA [NiNode+0xA4]; FUN_00704220.

## Proces następnego runu
- Nie naprawiać starego rootu OIJ; notice addytywny opublikowany w tym runie.
- Budżety: nie kopiować liczb poprzedników jako baseline (kontrakt sec.3).
- Length-failure pattern: children umierają na reason=length przy głębokim reasoningu w jednym
  kroku — zalecane: mniejsze okna + inkrementalny zapis wyniku + krótkie final message (B5/B6/B7/B8
  z tą dyscypliną dostarczyły normalnie).
