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

Format indeksu BNT (skalibrowany z bajtów; S11b; korekta nagłówka per QC P2-2 [RUN B]):
stopka `[int32 index_start=73218]['BNT2']` @EOF; **nagłówek licznika [u32 276
@73218]**, wpisy `{nazwa\n(0x0A), int32 size, int32 offset, int64 aux}` ×276 —
**276/276 wpisów .prt** (zero non-.prt), boundary-invariants 0 naruszeń
(każdy offset+size ≤ index_start; S11B_PORTALS_INDEX.json). ID-range: 382811..592741,
**276 unikalnych id, 0 duplikatów** (pierwotny parse S11b pominął 4-bajtowy nagłówek
licznika, wchłaniając go w nazwę pierwszego wpisu — stąd fantomowy "duplikat"; patrz
AMENDMENT (QC) na końcu pliku). Rozmiary: min 42, mediana 212, max 1990 B.

**Próbki kontraktowe**: w oknie 505000–510000 istnieje dokładnie **19 wpisów**
(505009, 505033, 505076, 505211, 505227, 505593, 505753, 505777, 505815, 505948,
506371, **507165**, 507204, 507224, 508495, 508588, 508949, 509990, 509991 — brak
ciągłości; pozostałe 982 id okna NIE istnieją [arytmetyka po korekcie: pierwotna
przestrzeń id 18+983=1001 minus odzyskany wpis 507165 — korekta QC P2-2 [RUN B]]).
Outliery 382811/422806/592739/592741 — WSZYSTKIE istnieją (S11B). Finiteness:
wszystkie f32-interpretacje nagłówków próbek finite (S11B/S11 finiteness PASS;
NaN/Inf odrzucone).

Struktura payloadu .prt (zgodna z readerem bajt-po-bajcie):
```
[01] tag bajt (wchodzimy w sub-blok — wg FUN_00852A30: tag==1 → czytaj dalej)
[01 01] u16 → nagłówek grafu [graph+0xac] = 0x0101 (257) we wszystkich próbkach
[00 00 00 01 ...] sub-blok FUN_008539f0 (bounds/portale grafu)
  — np. 382811: f32 zmierzone przez QC (korekta transkrypcji per QC P3-1 [RUN B]):
    -6.005/+6.005, -2.374/+2.498, +3.812 (pary AABB-like w sub-bloku grafu; patrz
    AMENDMENT (QC)) + 0x2000/0x2000/0x100 (rozmiary
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

---

## AMENDMENT (QC) — PE_935_ROUND_QC_STATIC_PLACEMENT_R1_20260913 (dopisek CLOSURE 2026-09-13)

Korekty §2 wykonane per INTERNAL_QC (QC_PASS, RUN B; pełne cytaty i odsyłacze:
06_REPORT\REPORT.md sekcja AMENDMENT (QC) tego runu + QC_REPORT.md):
- P2-2 [RUN B]: indeks MA 4-bajtowy nagłówek licznika (u32 276 @73218; wpisy od
  @73222) — "275 unikalnych + 1 duplikat" → **276 unikalnych, 0 duplikatów**;
  okno 505000–510000 = **19 wpisów** (dopisany 507165). Twierdzenia nośne
  (276/276 .prt, 0 naruszeń granic, rozmiary min 42 / mediana 212 / max 1990,
  outliery, negatyw 13×0 anchorów po WSZYSTKICH offsetach — QC domknął caveat
  "aligned-only" executora) — bez zmian; werdykt G3 bez zmian.
- P3-1 [RUN B]: transkrypcja AABB 382811 → wartości zmierzone: **-6.005/+6.005,
  -2.374/+2.498, +3.812** (struktura f32-par AABB-like — prawdziwa; żadna bramka
  nie zależy od tych liczb).
Evidence runu NIETYKANE (S11B_PORTALS_INDEX.json, S12_PRT_CONTENT_CHECK.json,
VA_EVIDENCE_REGISTRY.md bez zmian — hashe przed/po w MANIFEST_SHA256.csv rundy
closure).
