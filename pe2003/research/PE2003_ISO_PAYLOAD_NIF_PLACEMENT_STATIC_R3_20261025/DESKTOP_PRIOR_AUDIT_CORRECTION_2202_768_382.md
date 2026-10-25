# DESKTOP_PRIOR_AUDIT_CORRECTION_2202_768_382 — PE2003_ISO_PAYLOAD_NIF_PLACEMENT_STATIC_R3_20261025

RUN_ID: PE2003_ISO_PAYLOAD_NIF_PLACEMENT_STATIC_R3_20261025 | Publikacja
(sanitizowana projekcja), 2026-10-25. Plik addytywny pakietu R3.

## Korekta wcześniejszego audytu Desktop (klasy 2202 / 768 / 382)

Wcześniejszy raport audytu Desktop (kategoria provenance ISO) błędnie
zapisał, że w przypiętym zbiorze brak nagłówków ID 2202/768/382, mimo że
własny artefakt tego samego audytu (INDEPENDENT_DEFINITION_STRUCTURE.json)
zawiera `missing_header_ids = false` dla wszystkich trzech klas — czyli
dane audytu same wskazywały obecność tych nagłówków.

Poprawne rozstrzygnięcie (utrzymane w R2/R3): klasy 2202/768/382 są
**FILE_CLASS_PRESENT** — surowe człony udowodnione byte-identical w
Scripts.ark (header offsets 1032200 / 4990079 / 2602823). Błąd był błędem
namespace/raportowania, nie nieobecności danych.

Pełna treść korekty, jej zakres dowodowy i lineage znajdują się w
katalogu postaudytu (lokalnie, poza repo):
99_Audits\PE2003_R2_ISO_PROVENANCE_DESKTOP_POSTAUDIT_R1_20261025\
PRIOR_DESKTOP_AUDIT_ADDITIVE_CORRECTION.md
(seal MANIFEST_SHA256 SHA256
700215C8DE11F8E165FB0656740F25E35AA1E611BB1665B228865758ED0FD27A).
Treść tamtego dokumentu NIE jest kopiowana do tej projekcji.
