# EXCLUDED_ARTIFACTS — PE2003_ISO_ARCHIVE_RESOURCE_INSTANCE_PLACEMENT_STATIC_R4_20261025

RUN_ID: PE2003_ISO_ARCHIVE_RESOURCE_INSTANCE_PLACEMENT_STATIC_R4_20261025 | Publikacja (sanitizowana projekcja), JOB_ID PUB1, 2026-10-25.

Plik wylicza artefakty kampanii R4, które celowo NIE są publikowane w
repozytorium publicznym, wraz z uzasadnieniem. Wszystkie pozostają lokalnie
i nigdy nie były staged.

Katalogi lokalne (nigdy nie kandydowały do publikacji):

| Artefakt lokalny | Rozmiar | Powód wykluczenia |
|---|---|---|
| WORK_ROOT `D:\Eudoria_Reconstruction\PE2003\10_Campaigns\PE2003_ISO_ARCHIVE_RESOURCE_INSTANCE_PLACEMENT_STATIC_R4_20261025\jobs\M01` (data/DISASM dumpy disasm, tools, ARCHIVE_PRODUCER_CERTIFICATE.json surowe wejścia) | 582 827 B | Dumpy DISASM i surowe dane wejściowe to pochodne/odwzorowania binarne oryginalnego klienta 5.1.0.0 (game asset data / binary-derived). Publikacja bajtowych pochodnych binariów poza zakresem autoryzacji. |
| WORK_ROOT `jobs\L01` (data: censusy MODEL_ID_SEARCH/DENOMINATOR/EU_REVALIDATION; extracted: iso_members 400 113 B, pcg915 166 192 B, pcg_install 166 192 B, pe42_ark 165 411 B — w tym wyodrębnione membery NIF/SWF) | 1 781 726 B | Wyodrębnione membery archiwów (NIF/SWF i in.) = game asset data (własność MindArk); censusy robocze i narzędzia pośrednie nie są kanonicznym pakietem dowodowym. |
| WORK_ROOT `jobs\J01` (data/DISASM 418 516 B, tools; MODEL_INSTANCE_EDGE_MAP / TRANSFORM_SOURCE_MAP surowe JSON) | 464 959 B | Dumpy disasm klienta 5.1.0.0 = binary-derived content oryginalnego EXE. |
| WORK_ROOT `jobs\J02` (data/DISASM 458 738 B, listingi, ghidra\proj J02proj.rep — projekt Ghidra; data 3 499 419 B łącznie) | 3 545 954 B | Dumpy disasm + projekt Ghidra = binary-derived; surowe tabele caller/dispatch pochodne od oryginalnego obrazu EXE. |
| WORK_ROOT `jobs\N01` (tools/nif_transform_parser_v2.py SHA256 B71C209B..., tests, data/regenerated 83 955 B — regenerowane pochodne NIF) | 161 608 B | Regenerowane pliki pochodne NIF = derived game payload; parser/qualifier suite pozostaje lokalny (receptura i werdykt opisane w REPORT.md). |
| WORK_ROOT `QC\QC1` (work, skrypty robocze, n01_copy) | 179 582 B | Surowe skrypty/workdir QC — niekanoniczne; wyniki QC reprezentowane publicznie przez QC_FINDINGS.md, SELF_REVIEW_1/2.md, STAGE_ACCEPTANCE_GATES.csv. Precedens R2/R3: katalogi robocze jobs\* i QC\ nigdy nie publikowane. |
| WORK_ROOT `QC\QC2` (work 13 417 B) | 40 587 B | Jw. — workdir QC2. |
| AUTHORING package `D:\Eudoria_Reconstruction\99_Audits\PE2003_ISO_ARCHIVE_RESOURCE_INSTANCE_PLACEMENT_STATIC_AUTHORING_R4_20261025` (CONTRACT, CAMPAIGN plan, FINDINGS, INPUT pins, QC_PREFLIGHT, preflight receipt) | katalog | Pakiet autorski/contractowy — wewnętrzna koordynacja, nie kanoniczny dowód naukowy; pozostaje lokalnie per precedens R1-R3. |
| RECEIPT_ROOT `D:\Eudoria_Reconstruction\99_Audits\PE2003_ISO_ARCHIVE_RESOURCE_INSTANCE_PLACEMENT_STATIC_RECEIPT_R4_20261025` (PREFLIGHT_RESULT.json; po publikacji: PUBLICATION_RESULT.json, FINAL_NATIVE_TASK_CENSUS.md, PUBLICATION_CONTENT_REVIEW.md) | katalog | Dowód publikacji po stronie lokalnej; nie jest częścią projekcji naukowej. |
| Zamrożone pakiety R2/R3: `99_Audits\PE2003_NATIVE_BINDING_INSTANCE_PLACEMENT_STATIC_R2_20261025`, `99_Audits\PE2003_ISO_PAYLOAD_NIF_PLACEMENT_STATIC_R3_20261025` (+ ich RECEIPT roots i work roots w PE2003\10_Campaigns) | katalogi | Frozen/immutable historia — read-only, nigdy nie modyfikowane ani publikowane ponownie w tej projekcji (R3 było publikowane własnym commitem 7243918). |

Powyższe nie jest stratą dowodową: 21 kanonicznych plików pakietu seal
(SCIENCE_ROOT = `D:\Eudoria_Reconstruction\99_Audits\PE2003_ISO_ARCHIVE_RESOURCE_INSTANCE_PLACEMENT_STATIC_R4_20261025`,
seal MANIFEST_SHA256.csv self-excluded, SCIENCE_STOP przed manifestem,
bijection+rehash PASS) jest publikowanych byte-identical; surowe wejścia
pozostają weryfikowalne lokalnie przez SHA z SOURCE_PROVENANCE.json i
INPUT_RECHECK.json.
