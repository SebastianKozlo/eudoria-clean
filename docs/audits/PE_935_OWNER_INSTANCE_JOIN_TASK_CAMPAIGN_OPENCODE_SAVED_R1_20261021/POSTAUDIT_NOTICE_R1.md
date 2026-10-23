# POSTAUDIT_NOTICE_R1 — addytywny notice do PE_935_OWNER_INSTANCE_JOIN_TASK_CAMPAIGN_OPENCODE_SAVED_R1_20261021

Ten plik jest NOWYM, addytywnym oświadczeniem umieszczonym obok historycznego raportu poprzednika.
Stary REPORT.md i cały stary pakiet NIE zostały zmodyfikowane, naprawione ani ponownie sealowane.
Historyczny status pozostaje: LOCAL_SEAL = FAIL (bijekcja 75 wpisów vs 77 plików, extra
artifact_index; verifier poszerzył SELF_EXCLUDED po FAIL bez autoryzacji kontraktu);
PUBLICATION 4b633db = technicznie poprawna i pozostaje nienaruszona.

Zgodnie z kontraktem PE_935_INSTANCE_KEY_STREAM_RESOURCE_JOIN_HIGH_TASK_AUTHORING_R1_20261021
(sec. 3) niniejszy notice utrwala korekty OIJ-A01..A10 z zewnętrznego postaudytu
PE_935_OWNER_INSTANCE_JOIN_TASK_DEEP_POSTAUDIT_R1_20261021 jako obowiązujące rozumienie:

1. (A01) Dwie potwierdzone LOKALNE ścieżki registration/lookup/provider; ciągły identity join
   B_ctor->B_lookup NIE jest wykazany.
2. (A02) Same-map + same-key nie wystarcza: duplicate-key zachowuje stary payload, rejestracja
   może odrzucić nowy obiekt, a caller (004C47DA) nie sprawdza AL. Identity wymaga: successful
   insert TEGO obiektu, ordering, mapping preservation i lifetime.
3. (A03) Pełne saved EU 9.3.5 gettery 00414130 i 004154F0 istniały już przed tą kampanią;
   "poza saved corpus" i "nowy eksport jako pierwszy krok" były błędne.
4. (A04) Lokalny seal poprzednika jest nieważny (bijekcja FAIL); PASS po poszerzeniu wyłączeń
   nie jest zgodnością. Weryfikator nie może zmieniać predykatu po FAIL.
5. (A05/A06) Rozliczenia 1948 rows / ~48 bodies / ~238 calls wymagały korekty (prawdziwe:
   1990+ unique rows, >=1995 exposures, 39 rezerwacji, 49+ actual); nowy HIGH run nie kopiuje
   ich jako baseline. Brak reprodowalnego final accounting QC.
6. (A07) Fałszywy hash finding QF2 był błędem RAPORTU auditora (65-znakowy przepisany hash),
   nie mastera ani bajtów pakietu.
7. (A08/A09) Rejestracja ustawia tylko AL; empty-bucket helper 00851610 i preinsert 00856090
   były nieotwarte w tamtym runie (nowy run otworzył 00851610 i 00854260: node+4/node+8 są
   pisane wewnątrz FUN_00854260(pair*)).
8. (A10) Etykiety semantyczne (100 bucketów, biblioteka, reset/commit, world-transform,
   "transform 296445@4508") przekraczały zdekodowane dowody; 124.941@4508 pozostaje
   ANCHORS_ABSENT_SEMANTICS_OPEN.
9. Task routing poprzednika był prawdziwy (22 natywne dzieci; historyczny medium niefalsyfikowany
   przez nowy HIGH — HIGH dotyczy wyłącznie nowej kampanii).
10. WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CANONICAL_GATE_EFFECT=NONE.

Odniesienie: nowa kampania
PE_935_INSTANCE_KEY_STREAM_RESOURCE_JOIN_HIGH_TASK_OPENCODE_SAVED_R1_20261021 (HIGH,
saved-only, sealed PASS, 49+1 bijekcja, manifest SHA256
91C0090A79AAE5FFDA1CF74D993D70132ECF3DD10BE85B2EB8EDD17FF4B95E21) rozwinęła ten stan:
resource->scene pointer-flow edge (child == A == FUN_007CE1E0([manager+0x70]); B5 row 696693
[wrapper+4]=A addref), join callee = FUN_007B5810 (nie 007BF470 — helper SetParent wewnętrzny),
strumień 0048ECC0 = message cursor ring {type,data,size}, empty-bucket 00851610 domknięty
strukturalnie (node key/value w FUN_00854260(pair)). Szczegóły: REPORT.md nowego runu.
