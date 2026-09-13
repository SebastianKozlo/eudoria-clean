# Z4 — POLE D (PARAM f32; przy template 4508: 124.941)

RUN: PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913 | ERA: EU 9.3.5 (pcg_install)

## 1. Getter D — zidentyfikowany (VA-locked, bajty)

Obiekt template'u w pamięci: B@+0x04, A@+0x08, C@+0x0C, **D f32@+0x10** (RUN 3:
parser). Stuby-getterów (skan S9; round-trip + walidacja Ghidrą):

| pole | stub | VA | bajty | potwierdzenie |
|---|---|---|---|---|
| B (+0x04) | `mov eax,[ecx+4]; ret` | **FUN_00746550** @0x00746550 | 8B 41 04 C3 | znany z RUN 3; ten run: 60 callerów |
| A (+0x08) | `mov eax,[ecx+8]; ret` | **FUN_007ce1e0** @0x007CE1E0 | 8B 41 08 C3 | kanon RUN 3 |
| C (+0x0C) | `mov eax,[ecx+0xC]; ret` | **FUN_006b22d0** @0x006B22D0 | 8B 41 0C C3 | 80 callerów (ZS3) |
| **D (+0x10)** | `mov eax,[ecx+0x10]; ret` | **FUN_0048ada0** @0x0048ADA0 | **8B 41 10 C3** | 80+ callerów (ZS3) |
| **D f32 (+0x10)** | `fld dword [ecx+0x10]; ret` | **FUN_00861240** @0x00861240 | **D9 41 10 C3** | 10 callerów (ZS3) |

Skan pełny (S9_GETTER_STUB_SCAN.json): `8B 41 10 C3` występuje DOKŁADNIE w 0x0048ADA0
i 0x0098CFD7 (to drugie = środek innej instrukcji — wykluczone walidacją Ghidry:
function-at check); `D9 41 10 C3` dokładnie w 0x00861240.

## 2. Konsumenci D — census callerów (80+; klasyfikacja głównych)

FUN_0048ada0 (D-dword) — 80 call-site'ów, m.in.:
- **FUN_00468910 ×5** (0x00468D88/0x00468DA4/0x00469A7D/0x00469AF0/0x00469B0D) —
  silnik update world-objectu (droga A łańcucha placementu);
- FUN_00464e30 ×3, FUN_00466a00 ×2, FUN_00466ce0, FUN_00461850, FUN_00460330,
  FUN_00460670, FUN_004610f0 ×2, FUN_00462f50 ×2 (rodzina update CWO);
- **FUN_00567c50 ×2** (0x005681BD-region: `uVar6 = FUN_0048ada0()` przed
  FUN_00567b40 — D przekazywane do capacity-push!) i FUN_0058db50;
- FUN_008553d0 (konstruktor-walker: `fStack_50 = (float)FUN_0048ada0()`;
  w gałęzi 0x4e38 odczyt D steruje mapowaniem local_60: 4/5→2, 6→3, 7→4!);
- FUN_0043f4b0 (dispatcher atrybutów), FUN_0044c120, FUN_0048b6b0 ×2,
  FUN_00511070 ×2, FUN_00523ae0, FUN_0057ae60, FUN_0064b450 ×4, FUN_004b7690,
  FUN_00855dc0 (rejestracja).

FUN_00861240 (D-f32) — 10 call-site'ów: FUN_00456f40 ×2, FUN_0048c700, FUN_0048bff0,
FUN_00529370, FUN_00528810, FUN_00861390 ×2, FUN_009516f0, FUN_00528380 —
czyli licznik LOD/wizualny (0x00861xxx = rodzina distansów) i hierarchy.vfs-rodzina.

## 3. Semantyka D

W łańcuchu placementu D jest czytane jako **parametr skali/typu instancjonowania**:
- FUN_00567c50: `uVar6 = FUN_0048ada0()` (D bieżącego rekordu) → FUN_00567b40
  (push do kolejki update z capacity [obj+0x40..0x60] — **D wpływa na priorytet/
  flagę wpisu kolejki**, bo ten sam obiekt czyta też pola +0x48/+0x50/0x54/0x58/0x5c/0x60).
- FUN_008553d0: D steruje **wyborem wariantu konstrukcji** (mapowanie 4/5→2, 6→3, 7→4
  w gałęzi param-setu 0x4e38) i trafia do FUN_00415570/FUN_008599a0 jako jeden
  z argumentów inicjalizacji obiektu.
- FUN_00861390 (f32-D): rodzina distansów/LOD.
- **Granica (jawna)**: nie znaleziono JEDNEJ jednoznacznej semantyki — D jest
  parametrem MULTIPLE-consumer: (a) selektor wariantu (FUN_008553d0), (b) argument
  kolejki update (FUN_00567b40), (c) wartość distans/LOD (FUN_00861390).
  Dla template'u 4508 (D=124.941 ≈ 125): wielkość/promień/level — nie da się
  rozstrzygnąć statycznie bez runtime (etykieta: RUNTIME-UNOBSERVED dla
  konkretnej wartości 124.941; STATIC-PROOF dla konsumentów).

## 4. Kontrole
- Finiteness: D przy odczycie jako f32 w FUN_008553d0/FUN_00861240 — brak
  założeń o NaN/Inf w ścieżkach (kontrola finiteness wykonana na próbkach .prt
  i wartościach f32 w dumpach; wartość 124.941 = bits 0x42F9E1CB — round-trip OK).
- Drugi przypadek (Z5): FUN_0048ada0 czytany generycznie przez FUN_00468910
  (bez hardcodu 4508) — patrz Z5.
