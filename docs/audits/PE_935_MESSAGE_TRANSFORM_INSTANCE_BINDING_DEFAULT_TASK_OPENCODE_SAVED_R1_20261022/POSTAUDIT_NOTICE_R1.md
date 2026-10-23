# POSTAUDIT_NOTICE_R1 ? addytywny notice korekt MTB-A01..A07
Source postaudit: PE_935_MESSAGE_TRANSFORM_INSTANCE_BINDING_DEFAULT_TASK_DEEP_POSTAUDIT_R1_20261022 (SCIENCE=PARTIAL_PASS_WITH_TARGETED_CORRECTIONS; PROCESS=PARTIAL_NONCOMPLIANT_WITH_DISCLOSED_LIMITS; PACKAGE/PUBLICATION=PASS).
Niniejszy notice jest DODAWANY obok historycznych raportow; nic nie jest nadpisywane ani wycofywane retroaktywnie.

## Korekty uznane (MTB-A01..A07) i ich status w kampanii RECORD_HEAD_TRANSFORM_ROOT (R1, 2026-10-23)
- MTB-A01 (ABI singletonu): 004154F0 = parameterless lazy singleton getter; O=004154F0(); B=008544D0(this=O,key); *out=B. STATUS: ALREADY_ESTABLISHED ? poprawny zapis uzywany bezponownego odkrywania; pelny getter pozostaje w saved inputs.
- MTB-A02 (role cursor/record; kolejnosc odczytow): STATUS: REVALIDATED_WITH_NEW_EVIDENCE ? nowy pakiet 00864360+A3X potwierdza z instrukcji, ze CALL 00864360 i trzy chained CALL 0085BD20 (ADD ESP,8 miedzy) POPRZEDZAJA odczyt flag byte; 'flags first' pozostaje FALSIFIED; ESI=cursor, EDI=record w 0085BD80.
- MTB-A03 (12 stores): STATUS: REVALIDATED ? 00861150 ma 12 (prior QC F1); siostrana 00861030 ma 11 (nowy B2/QC recount); asymetria 11-vs-12 zgloszona jawnie w macierzy RECORD_HEAD runu.
- MTB-A04 (metryki/J05 cap160; LOWER_BOUND): STATUS: PROCESS_CORRECTION_APPLIED w nowym runie ? cap per-job <=160 (max 132), LOWER_BOUND/UNMEASURED rozdzielone, zero claimow COMPLETE_WITHIN_BOUND dla niemierzonego.
- MTB-A05 (UTC): STATUS: PROCESS_CORRECTION_APPLIED ? wszystkie seq/UTC generowane narzedziowo (append_event.py), zero recznych dat.
- MTB-A06 (observer action/kind): STATUS: ALREADY_ESTABLISHED ? blad adaptera Desktop potwierdzony; stary sealed observer nieedytowany; nowy run uzywa canonical kind schema.
- MTB-A07 (overclaims K_in=P_out/preservation/slot+A4/clone=world-instance): STATUS: OPEN_CEILINGS_PRESERVED ? zadna promocja; nowe runy (RECORD_HEAD R1) raportuja X_provenance/INSTANCE_ROOT_ROLE jako DATA_BARRIER/UNRESOLVED, nie jako ustalone tozsamosci.

Zachowany lokalny przeplyw: handler -> O/key lookup -> 00527AB0 -> 00861150 -> blok52B -> 0085CDE0(X=[D+4]) ? bez promocji do world-instance/building/XYZ.
WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CURSOR_SOURCE_MEDIUM=UNKNOWN; CANONICAL_GATE_EFFECT=NONE.
