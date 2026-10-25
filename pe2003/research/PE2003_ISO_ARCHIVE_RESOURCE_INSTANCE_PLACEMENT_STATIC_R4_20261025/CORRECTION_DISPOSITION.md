# CORRECTION_DISPOSITION — R4 względem R3 postaudytu i QC wewnętrznych

## R3-A01..A12 (postaudyt Desktop, obowiązujące)
- R3-A01 (P1, wyłączność źródła): PRZYJĘTE. capabilityFTP zachowane CONFIRMED jako mechanizm dystrybucji; SERVER_DELIVERED_ONLY nie odtworzone. R4 dodało: PE_PCG.ark bez konsumenta w korpusie (A-04), lokalna ścieżka already-present potwierdzona w ClientLoader — co WZMACNIA kontrmodel "nie kazdy przebieg robi FTP". SOURCE_SPECIFIC_ISO_MODELS=UNKNOWN (zawężone).
- R3-A02 (dataflow Models.ark): PRZYJĘTE i ROZSZERZONE. 0x413B97 = push napisu; 0x41F370 = etap VERIFY (tam kotwice Models\); 0x41D400..0x41E700 = etap EXTRACT. Caly łańcuch jednostki z VA — patrz A-05.
- R3-A03 (56/54 census): PRZYJĘTE. R4 nie miesza zbiorów; mapowanie record->file->source range utrzymane w referencjach I01/B01 (nie było potrzeby re-run).
- R3-A04 (MP3 corpus): PRZYJĘTE bez zmian (dotyczy R3 B01, nie R4).
- R3-A05/A06 (parser): PRZYJĘTE I WYKONANE — N01 v2: 51/51 kontrole, regeneracja end-to-end byte-identical, nonunity_scale=0 z generatora, boundary NiTriShape FAIL-uje, produkcyjne parse_nif/summarize testowane (nie harness-zastępca).
- R3-A07 (CSV/encoding): PRZYJĘTE. Wszystkie CSV R4 strict (csv.writer), JSON strict UTF-8; walidowane własnymi parserami QC1/QC2 i roota.
- R3-A08 (LENGTH/atrybucja): PRZYJĘTE. R4: jawne admission ledgers per job; atrybucja narzędzi per job zachowana; M01 admission ledger uczciwie zrelapowany (7 persisted + PARTIALLY_MEASURED — QC1-F03, poprawione w C01).
- R3-A09 (LOWER_BOUND): PRZYJĘTE. Zero LOWER_BOUND_COMPLIANT w R4; PARTIALLY_MEASURED/UNVERIFIED jawnie (J01/J02).
- R3-A10 (NiTriShapeData 44): PRZYJĘTE. N01 odtworzył 44=30+14 z surowych CSV.
- R3-A11 (hash patterns): PRZYJĘTE. Negatywy R4 eralabel i scoped (PE_PCG.ark negative ma jawny denominator i LOCAL_SOURCE_EXHAUSTED=NO).
- R3-A12 (zakres ISO): PRZYJĘTE. R4 nie wykonywał ponownej ekstrakcji ISO.

## Korekty wewnętrzne R4 (QC1 -> C01 -> QC2)
- QC1-F01 (P1): L01 negatywna kontrola EU była FALSE (EU 2008 Models.bnt ZAWIERA oba modele). POPRAWIONE w C01 (MODEL_ID_SEARCH, LOCAL_ARCHIVE_INVENTORY, RESULT, SELF_CHECK) z obowiązkową rewalidacją (EU_REVALIDATION.json: niezależna ekstrakcja, SHA MATCH obu członków). QC2 potwierdziło poprawność korekcji. Wniosek "wariant 2003 (218757) tylko w COT" pozostaje prawdziwy; dla 296445 liczba korpusów wariantu 2003 wzrosła do CZTERECH.
- QC1-F02/F03/F05/F06/F07/F08: wykonane w C01, zweryfikowane QC2.
- QC2-J01/J02/J03 (P3, dokumentacyjne — przyjęte verbatim do seal zamiast edycji executor artifacts):
  - QC2-J01: w census slot0 (11 trafień) 2 trafienia to false-positives bajtowe (0x46B72D = bezpośredni call 0x51C930; 0x46E5B5 = call [abs 0x65a6ac]); klasyfikacja "ALL destructor loops" nieprecyzyjna; NEGATYWNY WNIOSEK censusu (brak statycznych callsites fabryki) nietknięty.
  - QC2-J02: J02 deklarowane 36 bodies vs 33 wiersze admission bez rekonsyliacji (klasa QC1-F04); traktować jako PARTIALLY_MEASURED.
  - QC2-J03: census callerów 0x457980 = 14 (nie 13); wszyscy w rodzinie writer — substancja POTWIERDZONA.

## Retrakcje/statusy
- Żaden wcześniejszy claim R3 nie został zretraktowany bez zachowania ważnego jądra; era-mixing niedopuszczony (warianty 2003 eralabel vs ISO 5.1.0.0).
- Retraction(A) != Confirmation(not-A): korekta F01 NIE oznacza, że PE_PCG.ark istnieje lokalnie; scoped negatives utrzymane.
