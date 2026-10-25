# MODEL_CASE — 218757 (PE2003 ISO Payload NIF Placement Static R3)

RUN_ID: PE2003_ISO_PAYLOAD_NIF_PLACEMENT_STATIC_R3_20261025 | Autor: Z01 closing (pe-master-auditor) | 2026-10-25
Zakres: synteza istniejących wyników (I01/B01/I02a/I02b/D01/I03/N01/N02/QC1/QC2/C01). Zero nowej nauki.

## 1. ASSET_IDENTITY

| Wymiar | Stan | Źródło |
|---|---|---|
| Definicja PE42 (referencja) | 218757.nif, 56 535 B, SHA256 C13D08736D7E778803E20A3105067448007F32D15290AF168F836CD99248AD98, NIF 4.1.0.12, 62 bloki | 00_CONTROL\CONTRACT.md; jobs\N01\RESULT.md §0; re-hash Z01 MATCH |
| Definicja ISO (wydanie 2003-11) | **NOT_FOUND_IN_RECOVERED_SUBSET** — szukano w 56 nazwach plików, rozszerzeniach, manifestach, nazwach członków BUNT 50.bnt | jobs\B01\data\MODEL_PRESENCE.json; RESULT.md §5 |
| Przyczyna braku w ISO | Modele w wydaniu ISO były w Models.ark wewnątrz download-unitu PE_PCG.ark (serwery FTP MindArk 2003) | jobs\D01\RESULT.md; jobs\I03\RESULT.md §5 |
| Kanał dystrybucji ISO | SERVER_DELIVERED_ONLY (klient 5.1.0.0 ≠ PE42 3.4.3.1 COT; NO VA TRANSFER) | jobs\B01\CLIENT_BUILD_ID.json; I02b Task 7 |
| Uwaga konfuzabl | ISO zawiera 286757.mp3 — zasób dźwiękowy, niezwiązany z modelem 218757 | jobs\B01\RESULT.md §5 |

## 2. DEFINITION_RESOURCE_JOIN (korpus PE42)

- Plik definicji istnieje w korpusie (pochodzenie: Models.ark → 06_Models_and_Materials\PE42_EN_80553A75\218757.nif).
- Mechanizm resource-open: jak w 296445 (std::map 0x51F6E0 / wariant ISO 0x4038E0) — MECHANISM_PRESENT_VARIANT (jobs\I02b Task 5).
- Status krawędzi: **CONFIRMED_PARTIAL** (jw. — pełny log rozwiązywania nazwy niewykazany, jawne).

## 3. MODEL_INSTANCE_JOIN

- **MISSING_EDGE** — resource→instance niewykazane (R2-A04; rodzina ArkBoundingVolumeRenderer nie dowodzi instancji). R3 nie rozszerzał zakresu.
- W wydaniu ISO: konsekwencja braku danych modeli (NOT_PRESENT_IN_RECOVERED_SCOPE).
- Pełna mapa: MODEL_INSTANCE_EDGE_MAP.csv.

## 4. LOCAL_TRANSFORM_STATUS (poprawione liczby; N01/N02; jawne denominatory)

Denominatory jawne: 62 bloki total; 26 FULL_STRUCTURAL (12 NiNode + 14 NiTriShape); 36 TYPE_ONLY_ANCHOR poza transformami.

- Niezerowe lokalne translacje: **7 NiTriShape** (przykład blk 17 sign:0 = (0, −1030, 820)); 12 NiNode = zero/identity; nie-identity rotacje: **0**.
- Scale: 1.0 (26/26; korekta C01 nonunity_scale 0/0). Later triple: (0,0,0) 26/26.
- Root: blok 0 Scene Root lokalnie identity; drzewo 26/26, 10 top-level nodów, 0 cykli/orphanów.
- Stara kolumna translation P01 = later triple (38/38 globalnie) — stara semantyka REJECTED; translation @rotation_off−12 potwierdzona bajtowo.
- Composed root→część (MODEL-LOCAL): **7/26 części z niezerowym offsetem** (bloki 17, 36, 43, 47, 51, 55, 59), max |t| ≈ 1316.55 (blk 17); główna bryła composed (0,0,0); model w całości NIECZUŁY na konwencję A/B (wszystkie NiNode identity).
- Ograniczenie geometryczne: NiTriShapeData niezdekodowane (jak w 296445).

## 5. AUTHENTIC_WORLD_VALUES

**NONE.** AXIS_UNITS_FRAME=UNCALIBRATED; MODEL_LOCAL_SCOPE_ONLY; bez etykiet świata (N5; QC2 check PASS).

## 6. PLACEMENT_VERDICT

- PE2003_WORLD_XYZ_RECOVERED=**NO**; PE2003_HISTORICAL_PLACEMENT=**NOT_ESTABLISHED**.
- SOURCE (edycja ISO)=SERVER_DELIVERED_ONLY; dane modeli poza zasięgiem statycznym R3.
- Ścieżka referencyjna PE42: frontier otwarty (jw. 296445) — LOCAL_SOURCE_EXHAUSTED=NO.
- Status runu: ADVISORY; EXTERNAL_POSTAUDIT=PENDING; bez promocji do kanonu.

Ścieżki dowodowe: jobs\N01\data\NIF_TRANSFORM_CORRECTION.csv; jobs\N02\data\MODEL_LOCAL_COMPOSITE.csv; jobs\B01\data\MODEL_PRESENCE.json; MODEL_INSTANCE_EDGE_MAP.csv; CLAIMS.json (C-NIF-01..09, C-N02-01..05, C-BLD-06, C-SRC-01, C-WLD-01..04).
