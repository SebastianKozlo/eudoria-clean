# EXCLUDED_ARTIFACTS — PE2003_ISO_PAYLOAD_NIF_PLACEMENT_STATIC_R3_20261025

RUN_ID: PE2003_ISO_PAYLOAD_NIF_PLACEMENT_STATIC_R3_20261025 | Publikacja (sanitizowana projekcja), 2026-10-25.

Plik wylicza artefakty zapieczętowanego pakietu R3, które celowo NIE są
publikowane w repozytorium publicznym, wraz z uzasadnieniem i precedensem.
Wszystkie pozostałe pozostają lokalnie w SCIENCE_ROOT
(D:\Eudoria_Reconstruction\99_Audits\PE2003_ISO_PAYLOAD_NIF_PLACEMENT_STATIC_R3_20261025)
i są objęte seal MANIFEST_SHA256.csv (SHA256 pliku manifestu:
F7AC06585D540B327F2819D36D0358C61A97CE7040149660518F4271CC49EBF4).

| Artefakt | Powód wykluczenia | Precedens / zamiennik publiczny |
|---|---|---|
| NIF_TRANSFORM_CORRECTION.csv | Per-block pochodne dane NIF (pełne kolumny per blok 155+62 wierszy: offsets, triple, macierze 3x3, refy). Publikacja per-block danych pochodnych korpusu NIF byłaby payloadem pochodnym gry poza zakresem autoryzacji. | Precedens R2: P01_NIF_BLOCK_MAP.csv wykluczony z publikacji R2 tą samą regułą. Zamiennik publiczny: NIF_TRANSFORM_SUMMARY.md (tylko zagregowane liczby i nazwy bloków — zero literalnych bajtów gry). |
| QC\ (katalog roboczy QC1/QC2) | Workdir narzędzi QC: skrypty pośrednie, scan'y robocze, pliki tymczasowe. Nie jest częścią zapieczętowanego kanonu dowodowego dystrybuowanego publicznie; wyniki QC są reprezentowane publicznie przez QC_FINDINGS.json, SELF_REVIEW_1/2.md, INPUT_RECHECK.json i STAGE_ACCEPTANCE_GATES.csv. | Precedens R2: katalogi robocze jobs\* nie były publikowane; publikowane są tylko pliki kanoniczne run dir. |

Uwaga: jobs\* (katalogi fal I01/B01/N01/N02/I02a/I02b/D01/I03/QC1/QC2/C01)
oraz 00_CONTROL\ nigdy nie były kandydatami publikacji w projekcji R3 —
projekcja zawiera wyłącznie 26 kanonicznych plików pakietu + 2 nowe pliki
addytywne (NIF_TRANSFORM_SUMMARY.md, DESKTOP_PRIOR_AUDIT_CORRECTION_2202_768_382.md)
+ EXCLUDED_ARTIFACTS.md (ten plik).
