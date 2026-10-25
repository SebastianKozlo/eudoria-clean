# SELF_REVIEW_1 — Z01 closing (przegląd 1: claim-matrix vs proza, denominatorzy, zliczenia)

RUN_ID: PE2003_ISO_PAYLOAD_NIF_PLACEMENT_STATIC_R3_20261025 | Reviewer: pe-master-auditor (Z01, niezależny przegląd własnych dokumentów) | 2026-10-25
Zakres: zgodność CLAIMS.json (macierzy) z prozą REPORT/HANDOFF/MODEL_CASE; denominatorzy; arytmetyka zliczeń; spójność liczb procesowych. Metoda: programowe zliczenia (ConvertFrom-Json/Import-Csv + arytmetyka) + konfrontacja z ROW-ami źródłowymi.

## Sprawdzenia wykonane (wyniki)

1. **Statusy CLAIMS.json zliczone programowo** (ConvertFrom-Json + Group-Object): 45 twierdzeń = 41 CONFIRMED / 1 STRONGLY_SUPPORTED / 1 PLAUSIBLE / 1 UNVERIFIED / 1 REJECTED. Re-parse pliku po scaleniu: OK (45 claims). Wartości w REPORT §0 i HANDOFF zgodne.
2. **Denominatorzy payloadu (C-INS-03)**: programowy Import-Csv RECOVERED_FILES.csv: 56 wierszy; 54 z out_size (2 duplikaty wpisów bez rozmiaru); suma 163 568 016 B (== niezależna suma QC1); 53 wiersze plikowe (bez .bin) = 163 534 578 B; 51 unikalnych nazw plików. Wzór sumy z surowymi intermediatami: 163 568 016 + 11 756 (license_data.bin) + 64 (regdata_64.bin) = 163 579 836 B. Zgodne z zapisem w CLAIMS/QC_FINDINGS.
3. **BUILD_COMPARISON** (C-BLD-03): programowe zliczenie: 56 wierszy = 16 IDENTICAL / 10 DIFFERENT / 30 MISSING — zgodne z B01 i QC2.
4. **Arytmetyka N01/N02** (C-NIF-03..09, C-N02-01..05): 155 = 56 FULL + 99 TYPE_ONLY; 62 = 26 + 36; 82 = 56+26; 217 = 155+62; niezerowe translacje 26 (5+14+7) i nie-identity 11 (4+7) dla 296445; 7 niezerowych TriShape i 12 zero/identity NiNode dla 218757; composed 26/56 i 7/26; czułość A/B 3/82 — wszystkie zgodne z tabelami RESULT i CSV.
5. **QC itemy** (C-PRC-01): QC1 34 (32 TRUE/2 FALSE) + QC2 35 (33 TRUE/2 FALSE) = 69 itemów, 65 TRUE, 4 FALSE; findings 3P2+2P3 i 2P2+3P3 = 5P2+5P3 — zgodne z QC_FINDINGS.json QC1/QC2.
6. **Census natywnych Task**: 15 prób przed Z01 + Z01 = 16; spójność ROLE_LEDGER ↔ NATIVE_TASK_CENSUS ↔ REPORT §0 — OK.
7. **Korekty C01**: ledger zawiera 14 wpisów, z czego 13 in-place + 1 errata-only, errata_files_written = 6 → sformułowanie „13 korekt in-place + 6 ERRATA" (C-PRC-02, QC_FINDINGS, CORRECTION_DISPOSITION) zgodne z ledgerem.
8. **Consistency claim-matrix ↔ proza**: przejrzenie wszystkich 45 tez vs sekcje REPORT §1-2 i MODEL_CASE — brak rozbieżności merytorycznych (numeracja: 26/7 composed, 16/10/30, ISO 42 entries, IP pool, VA-e, sumy unpack). MODELE_CASE zgodne z CLAIMS.

## Znalezione problemy (NAPRAWIONE w tekstach; odnotowane)

- **SR1-F01 (P3, naprawione):** REPORT §2 pierwotnie „67 TRUE / 4 FALSE" — błędna suma (32+33=65). NAPRAWIONE na „69 itemów, 65 TRUE / 4 FALSE".
- **SR1-F02 (P3, naprawione):** BUDGET_LEDGER — pierwotnie suma unique_rows „~10 449" (rzeczywista suma deklaracji 1150+1430+720+138+4900+1831+300 = 10 469) oraz function_bodies „~117" (rzeczywista 107), z garbłą w frazie; data_declared_sum „~3.8 GiB" nie zgadzał się z własnym rozpisaniem składników (suma = ~5.0 GiB). NAPRAWIONE: ~10 469 / ~107 / ~5.0 GiB; zaktualizowana też metoda compliance.

## Ocena

Po naprawach: claim-matrix, proza i zliczenia są spójne; wszystkie liczby kluczowe mają programową weryfikację lub fizyczne źródło. Pozostałe ryzyka: brak (w zakresie tego przeglądu). Werdykt self-review: PASS po 2 naprawach P3.
