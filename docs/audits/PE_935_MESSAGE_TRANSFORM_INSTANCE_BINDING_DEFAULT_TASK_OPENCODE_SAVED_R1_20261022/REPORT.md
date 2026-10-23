# REPORT — PE_935 MESSAGE TRANSFORM / INSTANCE BINDING — DEFAULT TASK (SAVED-ONLY)
RUN_ID = PE_935_MESSAGE_TRANSFORM_INSTANCE_BINDING_DEFAULT_TASK_OPENCODE_SAVED_R1_20261022
RUN_STATUS = COMPLETED_WITH_LENGTH_RETRIES (pending seal/publication)
SCIENCE_VERDICT = PARTIAL_PASS_NEW_EDGES_CLOSED_1_DEFECT_CORRECTED
PROCESS_VERDICT = COMPLIANT_WITH_2_LENGTH_ATTEMPTS_AND_2_RESERVATION_INCIDENTS
ERA = PE_EU_9_3_5_SAVED_ONLY (H5 pinned: SHA 642CC29A...D8DB, 50780146 B)
WORLD_XYZ_RECOVERED = NO
HISTORICAL_PLACEMENT = NOT_ESTABLISHED
CURSOR_SOURCE_MEDIUM = UNKNOWN
CANONICAL_GATE_EFFECT = NONE

## 1. Co wykonano (rzeczywista nauka, nie plan)
6 obligacji wykonawczych, 8 prób Task (2 length na pierwszych próbach J01/J02 — zachowane jako LENGTH_LIMITED, artifact=NO; retry z dyscypliną write-early dostarczył). Wszystkie dzieci pe-reconstruction, model nask-glm/glm-5-3 default, parent = ta sesja (DB mode=ro).

## 2. Nowa zamknięta krawędź W1 (record → właściwa instancja → aplikacja pól)
- C05 CONFIRMED: *out_slot := FUN_008544D0(FUN_004154F0(K_query)) w 0085B840 (rows 1170283-1170293, RET 0x4).
- C06 CONFIRMED: konsument 00527AB0 wchodzi z this=*out_slot (deref 004123D0=`MOV EAX,[ECX];RET`) i recordem jako stack-arg (PUSH row 4700 niepoprany; 00527AB0 RET 0x4 row 180931).
- C07 CONFIRMED: w 00527AB0 — 52B (13 dword, REP MOVSD) z próbki 0085BFA0 do [[this+0xc]+0x30] (rows 180915-180922), potem record → CALL 00861150([this+0x10], record) (rows 180923-180926).
- C08 CONFIRMED: 00861150 aplikuje pola rekordu do obiektu [this+0x10]: floats +0x1c/+0x20/+0x24 → +0x8/+0xc/+0x10; triple +0x28/+0x2c/+0x30 → +0x14/+0x18/+0x1c; bajt flag +0x34 bity0-3 → 4 boole +0x28/+0x34/+0x35/+0x36; floats +0x38/+0x3c → +0x38/+0x3c (rows 1176856-1176887); nagłówek rekordu (+0x0/+0x4/+0x8/+0xc) idzie side-channel do 0096cdd0/0085CDE0 (signature-level only).
- C04 CONFIRMED: schema rekordu z parsera 0085BD80 (flagi, sign-flipy 0x20/0x40/0x80, triple warunkowy bit 0x10, defaults).

## 3. Gałąź W2
- C09 CONFIRMED: ciało 007B5810 domknięte do normalnych wyjść (null-child skip; append przez kontener this+0xc8 z inline/grow; dwa sparowane acquire/release [ESI+4] z vcall slot+0x4 przy zejściu do zera; RET 0x8). Slot +0xA4 pozostaje NIEUDOWODNIONY (kandydat ABI-only).
- C10 CONFIRMED: fragmenty 006C0F90-006C112F to accessory/predykat/init-start; sufity PRESERVATION_BY_THIS_HELPER i T_EQUALS_FIRST_INITIAL_P bez zmian.

## 4. Korekta i utrwalone sufity
- Wada J01 (attempt 2, RESULT Answer.1): JZ w row 4690 opisany jako warunek K_query — to jest cursor-flag [ESI+0x11] (CMP w prefix row 4689). Poprawka addytywna w QC_FINDINGS i SELF_REVIEW_1; artefakt workera nietknięty.
- K_in vs P_out: różne definicje, bez mostu (HDA-01). Store ctor_arg2→[wrapper+4] nie ogłoszony ponownie. Preservation/T_EQUALS otwarte. Błąd RAW B7 row4230 poprzednika nie skopiowany — wszystkie pakiety generowane deterministycznie z H5 z parzystością lineNo+VA+instr.

## 5. Budżety (LOWER_BOUND tam gdzie niemierzone)
body reserved/debit 13/80; unique code lines 946/8000; exposures przed QC 1467/24000; próby 8/32; QC 294/320 reserved; CALL units — w final accounting; brak refundacji; J02B init-window zarezerwowany(2) nieotwarty.

## 6. Ograniczenia
Brak semantyki pól docelowych (C11 OPEN); 0085CDE0/0096cdd0/004154F0/008544D0/0085BFA0-internals nieotwarte; static-only (NATURAL, saved listing); brak runtime; slot +0xA4 nieudowodniony; duplikat-klik/failure resolution NOT_OBSERVED_IN_WINDOW.

## 7. Terminal
SCIENCE_STOP po seal; publikacja sanitizowana obowiązkowa (własny raport + 2 addytywne notices HDA + POSTAUDIT_NOTICE R2 sprostowanie).

## 8. Korekty QC (QCA, addytywnie)
- F1 (P2): liczba bezpośrednich store'ów w 00861150 (rows 1176856-1176887) wynosi 12 (3 FLD/FSTP + 3 MOV + 4 bit-unpack + 2 FLD/FSTP), nie "Eleven" jak w RESULT.md J06 (artefakt workera nietknięty).
- F2 (P3): RET 0x4 w row 180931 czyści zewnętrzny push recordu handlera; wewnętrzny PUSH ECX (row 180924) czyści własne RET 0x4 00861150 (row 1176891).
- DEFECT ADJUDICATED (C01): JZ row 4690 testuje cursor-flag [ESI+0x11] (CMP 0048EDFF, row 4689), nie równość K_query (ta była w 0048EDD5/rows 4678-4679). RESULT J01 pozostaje nietknięty; obowiązujący opis warunku = powyższy.
- QC coverage: C02/C03/C04(SAMPLE_ONLY)/C09/C10 NOT_CHECKED przez QCA (poza oknem wejściowym QC); brak podwyższenia statusów bez niezależnej kontroli.

## 9. Rozliczenie finalne (QFINAL)
- CALL-units LOWER_BOUND 64/400 (policzone per-packet przez QFINAL).
- Exposures: JSONL literal 1285 (po RETRO_READ_ADDENDUM); QFINAL reconciled 2140 (ledger basis 2667) / 24000 — LOWER_BOUND, rozbieżność disclosed (F-1).
- Body: ledger 13/13; JSONL literal 11/16 z disclosed reclassyfikacją (F-2). Próby 10/32 (2 length, 2 retry, 0 orphans).
- QC: QCA QC_PARTIAL (F1 P2 liczba 12, F2 P3 RET 0x4, ACCEPTED_DEFECT dla J01); QFINAL QC_PARTIAL (F-1/F-2 rozliczone addytywnie). Brak naruszenia capów; brak delivered inflation.
- SCIENCE_STOP zapisany (admission seq 27). Dalej: seal + obowiązkowa publikacja sanitizowana.
