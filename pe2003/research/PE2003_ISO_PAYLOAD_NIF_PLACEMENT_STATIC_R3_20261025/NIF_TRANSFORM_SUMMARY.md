# NIF_TRANSFORM_SUMMARY — PE2003_ISO_PAYLOAD_NIF_PLACEMENT_STATIC_R3_20261025

RUN_ID: PE2003_ISO_PAYLOAD_NIF_PLACEMENT_STATIC_R3_20261025 | Publikacja (sanitizowana projekcja), 2026-10-25.

Zagregowane podsumowanie wyników transformów NIF fal N01/N02. Ten plik jest
PUBLICZNYM zamiennikiem wykluczonego NIF_TRANSFORM_CORRECTION.csv (per-block
pochodne dane NIF — patrz EXCLUDED_ARTIFACTS.md). Zawiera wyłącznie liczby,
denominatory i nazwy bloków; ZERO literalnych bajtów gry, ZERO surowych
per-block wartości. Źródła: REPORT.md §1-2, MODEL_CASE_296445.md,
MODEL_CASE_218757.md (composed z N01/N02); liczby per-type zweryfikowane
publikacyjnym recountem z wykluczonego CSV przed jego wyłączeniem
(zgodność pełna: 296445 — NiNode 19 bloków, TriShape 30, Billboard 7;
218757 — NiNode 12, TriShape 14).

## Poprawka struktury pól (fala N01)

- Kolejność pól transformu NIF 4.1: **translation @ rotation_off − 12**
  (PRZED macierzą 3x3 rotacji) — potwierdzone bajtowo (loader 00416860,
  16 pinów VA w PE2_unpacked_out.exe). Kontrmodel „macierz przed
  translacją" obalony.
- Stara kolumna `translation` P01 (mapy bloków R1) = systematycznie later
  triple (38/38 wierszy) — stara semantyka REJECTED (C-NIF-02).

## 296445.nif (NIF 4.1.0.12, 155 bloków)

Denominatory: 155 bloków total; 56 FULL_STRUCTURAL; 99 TYPE_ONLY_ANCHOR
poza transformami. Root (blok 0) lokalnie identity.

Lokalne transformy per typ (N01):

| Typ | Bloków | Niezerowe translacje | Nie-identity rotacje |
|---|---|---|---|
| NiNode | 19 | 5 | 4 |
| NiTriShape | 30 | 14 | 0 |
| NiArkBillboardNode | 7 | 7 | 7 |

- Scale: 1.0 we wszystkich 56/56 (liczniki skorygowane C01 do 0/0/0).
- Later triple: (0,0,0) 56/56.
- Composed root→część (N02, MODEL-LOCAL, konwencja A): **26/56 części z
  niezerowym composed offsetem**, max |t| ≈ 11291.14 jednostek modelowych
  (blok 113, B_Eu_b047_lens 1\t01). Główna bryła (8 TriShape budynku)
  composed (0,0,0).
- Konwencja macierzy: AMBIGUOUS_DUAL_REPORTED (czułość 3/82 bloków
  globalnie — tylko ścieżki przez rotacje 90°).
- NiTriShapeData (geometria) poza dekodowaniem — twierdzenie „obiekty w
  obrębie bryły" UNVERIFIED.

## 218757.nif (NIF 4.1.0.12, 62 bloki)

Denominatory: 62 bloki total; 26 FULL_STRUCTURAL; 36 TYPE_ONLY_ANCHOR.
Root (blok 0) lokalnie identity.

Lokalne transformy per typ (N01):

| Typ | Bloków | Niezerowe translacje | Nie-identity rotacje |
|---|---|---|---|
| NiNode | 12 | 0 | 0 |
| NiTriShape | 14 | 7 | 0 |

- Scale: 1.0 (26/26). Later triple: (0,0,0) 26/26.
- Composed root→część (N02, MODEL-LOCAL): **7/26 części z niezerowym
  offsetem** (bloki 17, 36, 43, 47, 51, 55, 59), max |t| ≈ 1316.55 (blok 17).
  Główna bryła composed (0,0,0). Model NIECZUŁY na konwencję A/B
  (wszystkie NiNode identity).
- NiTriShapeData niezdekodowane (jak w 296445).

## Standing

Wszystkie transformy są MODEL-LOCAL (composed root→część). AUTHENTIC_WORLD_VALUES
= NONE; AXIS_UNITS_FRAME = UNCALIBRATED; żadna wartość nie jest etykietowana
jako współrzędna świata (N5). PE2003_WORLD_XYZ_RECOVERED=NO;
PE2003_HISTORICAL_PLACEMENT=NOT_ESTABLISHED. Pełne dowody (per-block) pozostają
lokalnie w zapieczętowanym SCIENCE_ROOT; ta projekcja publikuje wyłącznie
agregaty.
