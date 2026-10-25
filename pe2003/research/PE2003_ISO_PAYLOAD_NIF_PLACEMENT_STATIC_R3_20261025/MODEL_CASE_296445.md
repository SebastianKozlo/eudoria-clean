# MODEL_CASE — 296445 (PE2003 ISO Payload NIF Placement Static R3)

RUN_ID: PE2003_ISO_PAYLOAD_NIF_PLACEMENT_STATIC_R3_20261025 | Autor: Z01 closing (pe-master-auditor) | 2026-10-25
Zakres: synteza istniejących wyników (I01/B01/I02a/I02b/D01/I03/N01/N02/QC1/QC2/C01). Zero nowej nauki.

## 1. ASSET_IDENTITY

| Wymiar | Stan | Źródło |
|---|---|---|
| Definicja PE42 (referencja) | 296445.nif, 108 876 B, SHA256 656795D8B3DDDF8F9192EE41C4710D592894860F6959B53B2C08036977E7B862, NIF 4.1.0.12, 155 bloków | 00_CONTROL\CONTRACT.md; jobs\N01\RESULT.md §0; re-hash Z01 MATCH |
| Definicja ISO (wydanie 2003-11) | **NOT_FOUND_IN_RECOVERED_SUBSET** — szukano w 56 nazwach plików, rozszerzeniach, manifestach, nazwach członków BUNT 50.bnt | jobs\B01\data\MODEL_PRESENCE.json; RESULT.md §5 |
| Przyczyna braku w ISO | Modele w wydaniu ISO były w Models.ark wewnątrz download-unitu PE_PCG.ark (serwery FTP MindArk 2003) | jobs\D01\RESULT.md; jobs\I03\RESULT.md §5 |
| Kanał dystrybucji ISO | SERVER_DELIVERED_ONLY (klient 5.1.0.0 ≠ PE42 3.4.3.1 COT; NO VA TRANSFER) | jobs\B01\CLIENT_BUILD_ID.json; I02b Task 7 |
| Uwaga konfuzabl | ISO zawiera 309445.mp3 — zasób dźwiękowy, niezwiązany z modelem 296445 | jobs\B01\RESULT.md §5 |

## 2. DEFINITION_RESOURCE_JOIN (korpus PE42)

- Plik definicji istnieje w korpusie (pochodzenie: Models.ark → 06_Models_and_Materials\PE42_EN_80553A75\296445.nif).
- Mechanizm resource-open buildu referencyjnego: get-or-create 0x51F6E0 (std::map), dispatch '.nif'; w buildzie ISO odpowiednik wariantowy (hash-bucket 0x4038E0, '.nif' @0x42E990) — MECHANISM_PRESENT_VARIANT (jobs\I02b Task 5).
- Status krawędzi: **CONFIRMED_PARTIAL** — mechanizm obecny i spójny, ale pełny log rozwiązywania nazwa→wolumen→NIF nie był celem R3 (jawne niewykazanie).

## 3. MODEL_INSTANCE_JOIN

- **MISSING_EDGE** — krawędź resource→instance NIE została wykazana ani w R2, ani w R3. R2-A04: graf sieciowy silnie związany z ArkBoundingVolumeRenderer (8 vtx/12 tri, m_ptBoxes) — wspólna rodzina/root NIE dowodzi instancji modelu.
- W wydaniu ISO: konsekwencja braku danych (iso_definition = NOT_PRESENT_IN_RECOVERED_SCOPE) — bez danych modeli brak możliwości dalszych krawędzi.
- Pełna mapa: MODEL_INSTANCE_EDGE_MAP.csv.

## 4. LOCAL_TRANSFORM_STATUS (poprawione liczby; N01/N02; jawne denominatory)

Denominatory jawne: 155 bloków total; 56 FULL_STRUCTURAL (19 NiNode + 7 NiArkBillboardNode + 30 NiTriShape); 99 TYPE_ONLY_ANCHOR poza transformami.

- Niezerowe lokalne translacje: **5 NiNode + 14 NiTriShape + 7 ArkBillboard = 26** (w tym nowo zdekodowane TriShape — dotąd poza zasięgiem P01).
- Nie-identity lokalne rotacje: **4 NiNode + 7 ArkBillboard = 11**.
- Scale≠1: 0 (56/56 = 1.0; liczniki summary skorygowane C01 do 0/0/0 po QC1-P2-QC1-03). Later triple: (0,0,0) 56/56.
- Root: blok 0 Scene Root lokalnie identity; drzewo 56/56, 23 top-level nodów, 0 cykli/orphanów.
- Stara kolumna translation P01 = systematycznie later triple (38/38) — stara semantyka REJECTED (C-NIF-02); translation @rotation_off−12 potwierdzone bajtowo (loader 00416860, 16 pinów).
- Composed root→część (MODEL-LOCAL, konwencja A; czułość konwencji: 3/82 bloków globalnie, tylko ze ścieżkami przez rotacje 90°): **26/56 części z niezerowym composed offsetem**, max |t| ≈ 11291.14 jednostek modelowych (blk 113 B_Eu_b047_lens 1\t01); bryła główna (8 TriShape budynku) composed (0,0,0) — geometria "upieczona" w wierzchołkach.
- Konwencja macierzy: AMBIGUOUS_DUAL_REPORTED (wyniki dla A i B w MODEL_LOCAL_COMPOSITE.csv).
- Ograniczenie geometryczne: wierzchołki NiTriShapeData nie zdekodowane → twierdzenie "drzwi/obiekty w obrębie bryły" UNVERIFIED (brak bounding boxa bryły).

## 5. AUTHENTIC_WORLD_VALUES

**NONE.** AXIS_UNITS_FRAME=UNCALIBRATED; MODEL_LOCAL_SCOPE_ONLY; żadna wartość nie jest etykietowana jako współrzędna/metryka świata (N5; QC2 sprawdził artefakty N02 — N5 compliant).

## 6. PLACEMENT_VERDICT

- PE2003_WORLD_XYZ_RECOVERED=**NO**; PE2003_HISTORICAL_PLACEMENT=**NOT_ESTABLISHED**.
- SOURCE (edycja ISO)=SERVER_DELIVERED_ONLY; dane modeli poza zasięgiem statycznym R3 (PE_PCG.ark, serwery 2003).
- Ścieżka referencyjna PE42: frontier otwarty (registry+0x3C ctor, konsumenci resource-open, geometria NiTriShapeData) — LOCAL_SOURCE_EXHAUSTED=NO.
- Status runu: ADVISORY; EXTERNAL_POSTAUDIT=PENDING; bez promocji do kanonu.

Ścieżki dowodowe: jobs\N01\data\NIF_TRANSFORM_CORRECTION.csv; jobs\N02\data\MODEL_LOCAL_COMPOSITE.csv; jobs\B01\data\MODEL_PRESENCE.json; jobs\I02b\data\ISO_CLIENT_FUNCTION_MAP.json; MODEL_INSTANCE_EDGE_MAP.csv; CLAIMS.json (C-NIF-01..09, C-N02-01..05, C-BLD-06, C-SRC-01, C-WLD-01..04).
