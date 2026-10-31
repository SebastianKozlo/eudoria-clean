# MODEL_JOIN — Stage F (PE_WORLD_R2_PLACEMENT_SOURCE_R1_20261031)

Pierwotne źródło indeksu (primary): **własny parser executora** nad
`D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt` (BNT2 trailer;
round-trip do EOF-trailera PASS; **5,596 wpisów, 5,596 unikalnych nazw, 0 duplikatów** —
pomiar własny, zgodny z P5). Cross-check: P5 `Z2_MODELS_BNT_INDEX_NAMES.csv` (nie
użyty do joinu — zgodność liczbową 5,596 odnotowano).

## Join 1 — poziom NAZW plików .bvi (klucz: numeryczna nazwa pliku, szer. dziesiętna 1:1)

Kryterium dokładne: `int(nazwa_bvi)` == `int(nazwa_nif)` (klucz pełny, endianness N/D —
to liczby dziesiętne w nazwach ASCII). Zero duplikatów po obu stronach → każdy wynik
jednoznaczny; brak "first matching value".

| Kryterium | joined / total | odsetek |
|---|---|---|
| **PRIMARY: identyczne id** (`506044.bvi` → `506044.nif`) | **0 / 1865** | 0.0% |
| ALTERNATYWNE (osobny pomiar, nie primary): id − 1 (`506044.bvi` → `506043.nif`) | **1098 / 1865** | 58.9% |
| ALTERNATYWNE: id + 1 | **10 / 1865** | 0.5% |
| not joined (żadne z powyższych) | **757 / 1865** | 40.6% |
| ambiguous | **0** | — |

Interpretacja: wzorzec `bvi_id = nif_id + 1` potwierdzony pomiarowo dla 1098/1865 (58.9%)
— zgodny z kanonem ery 2003 (60% korelacji; skill pe-bnt-tdf). 757 plików .bvi nie ma
sąsiada ±1 w Models.bnt — zgodne z P5 (199 .bvi niereferencjonowanych przez template'y
+ .bvi istniejące dla modeli spoza zakresu id). Mianownik jawny: 1865 nazw .bvi vs 5,596 nazw .nif.

## Join 2 — poziom PÓL zdekodowanych (type0, 3 próbki: 506044, 105624, 506237)

Przetestowane pola id-like: KAŻDE pole f32 z 75 rekordów (675 pól), w dwóch reinterpretacjach.

| Reinterpretacja | Kryterium joinu | testowane | joined | ambiguous/coincidental |
|---|---|---|---|---|
| f32 → u32 LE | u32 == id .nif (exact, 5,596 kluczy, 0 duplikatów) | 675 | **0** | 0 |
| f32 → 2 × u16 LE | u16 == id .nif (exact) | 1350 połówek | 5 trafień (16201.nif ×3, 16645.nif ×2 — wszystkie w 506237.bvi, pola f6/f9) | **5/1350 = 0.37% — sklasyfikowane COINCIDENTAL**: 2 unikalne wartości powtórzone między rekordami (niezgodne z semantyką id, która bywa raz), wartości to połówki bajtowe zwykłych floatów; brak konsumenta |

Denominatory jawne: 675 pól f32 (type0 próbki) — POLA TYPE1 NIE były joinowane
(wierzchołki/indeksy siatki nie są kandydatami id; 2,104 wierzchołków + 2,778 indeksów
584781 = poza testem; zapisane jako not-tested z powodem).

## Wnioski do Stage E

- Nazwa pliku (nie pola payloadu) jest jedynym nośnikiem relacji model↔bvi — dokładny
  join identycznościowy = 0; relacja działa przez przesunięcie −1 (1098/1865, pomiar).
- Wewnątrz payloadów NIE MA joinowalnego id modelu (0/675 u32; u16-trafienia koincydencje)
  — konieczny warunek rekordu placementu (model id) jest NIEOBECNY.

Surowe dane: 01_RAW/MODEL_JOIN.json (generator tools/compare_census_join.py).
