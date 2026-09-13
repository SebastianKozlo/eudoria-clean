# Z3 — PORTALS.BNT / .PRT: reader, struktura, rola

RUN: PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913 | ERA: EU 9.3.5 (pcg_install)
Portals.bnt: 80,682 B; READ-ONLY (nigdy nie modyfikowany; skrypty tylko czytają).

## 1. Reader — ZNALEZIONY (VA-locked)

Łańcuch (RM-init FUN_0041dae0 rejestruje magazyn ".prt"/portals.bnt — RUN 3;
konsumenci w tym runie):

```
ArkPortalResourceItemFactory (vtable 0x00A91C88; slot0 FUN_0041b870 @0x0041B870
  [dtor-family], slot1 FUN_0084b270 @0x0084B270)
  └─ slot1: operator_new(0x14) → FUN_00852a90 @0x00852A90 = ctor ArkPortalResourceItem:
       *item = vtable 0x00A91D04; operator_new(0x58) → FUN_0084ce20 = ctor
       ArkPortalCellGraph (vtable 0x00A91CB4) → [item+0x10]
     → FUN_0084f7a0(payload) = PARSOWANIE danych .prt do grafu
       (fail → destroy + return null)
```

**Parser grafu** FUN_00852750 @0x00852750 (disasm pełny: ZS9_DISASM_FUN_00852750_full):
1. czytaj u16 → [graph+0xac] (nagłówek);
2. FUN_008539f0(graph+0x2c, buf) — sub-blok grafu (bounds/portale — czyta bajty,
   u16, u32 — rodzina kursorowa FUN_0040de60);
3. czytaj u32 = **liczba komórek** (local_94);
4. pętla ×count: czytaj u32 (id/kod komórki) → operator_new(0x90) →
   FUN_0084fe50 (ctor bazy) → FUN_00852dc0(id,…) — **komórka ArkPortalCell**
   (vtable 0x00A91CF8 [FUN_00850C50, FUN_00852A30]) → **wirtualny slot1 =
   FUN_00852A30 @0x00852A30**: czytaj bajt-tag; jeśli ==1 → sub-bloki
   (FUN_00852750 na obiektach zagnieżdżonych — portale/boundsy) → FUN_008526d0
   (insert do grafu).

Czytniki terminalne: FUN_00852bf0 (u16@+0x8c, u32@+0x0c — pola portalu),
FUN_00852d60 (bajty) — rodzina kursorowa (S8 cursor census: 0x00852A30 PUSH 0x1,
0x00852BF0 PUSH 0x2/0x4, 0x00852D60 PUSH 0x1).

## 2. Struktura .prt z BAJTÓW — zdekodowana i zwalidowana przeciw readerowi

Format indeksu BNT (skalibrowany z bajtów; S11b): stopka `[int32 index_start=73218]
['BNT2']` @EOF; wpisy `{nazwa\n(0x0A), int32 size, int32 offset, int64 aux}` ×276 —
**276/276 wpisów .prt** (zero non-.prt), boundary-invariants 0 naruszeń
(każdy offset+size ≤ index_start; S11B_PORTALS_INDEX.json). ID-range: 382811..592741,
275 unikalnych id + 1 duplikat (count 276 vs 275 — zduplikowane id w indeksie,
zgodne z kontraktem "outliery"). Rozmiary: min 42, mediana 212, max 1990 B.

**Próbki kontraktowe**: w oknie 505000–510000 istnieje dokładnie 18 wpisów
(505009, 505033, 505076, 505211, 505227, 505593, 505753, 505777, 505815, 505948,
506371, 507204, 507224, 508495, 508588, 508949, 509990, 509991 — brak ciągłości;
pozostałe 983 id okna NIE istnieją). Outliery 382811/422806/592739/592741 —
WSZYSTKIE istnieją (S11B). Finiteness: wszystkie f32-interpretacje nagłówków próbek
finite (S11B/S11 finiteness PASS; NaN/Inf odrzucone).

Struktura payloadu .prt (zgodna z readerem bajt-po-bajcie):
```
[01] tag bajt (wchodzimy w sub-blok — wg FUN_00852A30: tag==1 → czytaj dalej)
[01 01] u16 → nagłówek grafu [graph+0xac] = 0x0101 (257) we wszystkich próbkach
[00 00 00 01 ...] sub-blok FUN_008539f0 (bounds/portale grafu)
  — np. 382811: f32-pary -6.001/+6.001, -2.437/+2.4966, -0.000388/+3.812
    = AABB min/max (symetryczne boundsy komórki) + 0x2000/0x2000/0x100 (rozmiary
   /sektory siatki)
[xx xx xx xx] u32 = liczba komórek
{ [u32 id/kod] [tag-bajt...] [dane komórki: boundsy f32, portale] } × count
```

## 3. Czy .prt niesie ID obiektów świata + transformy? — NIE (dowód strukturalny)

Skan WSZYSTKICH 276 payloadów (S12_PRT_CONTENT_CHECK.json; round-trip LE przed skanem;
10413 unikalnych u32 aligned):
- **0 trafień**: template 4508, 4752, 2249; nif A 296445, 126740, 278453;
  bvi B 296446; param-sety 20005/20007/20006; msgtype 0xB9; atrybuty 0x6A4/0x6A8.
- 148 wartości u32 w zakresie 100k–460k (aligned) — przypadkowe (interpretacja
  jako f32 daje typowe boundsy; brak jakiegokolwiek odzwierciedlenia przestrzeni
  ID Models.bnt — z zastrzeżeniem: aligned-grid tylko, nie wyczerpuje skrajnych
  interpretacji).

**Werdykt G3: Portals.bnt/.prt = wyłącznie cell-graph dPVS** (ArkPortalCellGraph:
AABB grafu, komórki 0x90 B z boundsami, portale) — **NIE jest nośnikiem placementów**
ani ID obiektów świata. Zawartość = geometria renderowania (widoczność), nie dane
placementu. STATIC-PROOF (reader + bajty + negatywny skan ID); RUNTIME-UNOBSERVED:
aktualne użycie w sesji gry (zakazane w tym runie).

## 4. NOT_CHECKED
1. Pełna dekompilacja FUN_0084f7a0 (wejście parsowania .prt; struktura wywnioskowana
   z FUN_00852750/FUN_00852A30/FUN_00852bf0 + bajtów — spójna, ale ciała FUN_0084f7a0
   nie zdekompilowano w tym runie).
2. Pole aux int64 w indeksie BNT (0xB2A7C844-style pary — wygląda na sumę kontrolną
   lub znacznik czasu; niezidentyfikowane).
3. TerrainEditZones.bnt (54,156 B) — poza zakresem (NOT_CHECKED RUN 3, bez zmian).
