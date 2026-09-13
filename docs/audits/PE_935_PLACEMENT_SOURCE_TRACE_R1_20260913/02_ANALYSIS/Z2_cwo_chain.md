# Z2 — ŁAŃCUCH CWO / ARKOBJECT (jak powstaje statyczny rekord placementu)

RUN: PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913 | ERA: EU 9.3.5 (pcg_install)

## 1. Kto tworzy rekord placementu (+0x08/+0x14) — creator, VA-locked

Rekord placementu (derived; layout RUN 3: ctor FUN_00730700 zeruje 11 dwordów; pozycja
@+0x08 [FUN_00730f90], rotacja @+0x14 [FUN_00730fb0], +0x20/+0x24 [FUN_00730fd0]) jest
budowany w **FUN_00567770 @0x00567770** (RUN 3 potwierdzone; ten run disasm okno
0x00567860–0x00567960: 4× LEA ECX,[ESP+0xB4] + CALL-e seterów — ZS2_DISASM
FUN_00567770_setter_calls). Nowe w tym runie — **trzy niezależne drogi napędu**:

| droga | funkcja | trigger | dowód |
|---|---|---|---|
| A | FUN_0058db50 @0x0058DB50 (← FUN_00468910 ×3 @0x00469299/AB/19) | per-frame update world-objectu | ZS2_PSEUDO_0058DB50: FUN_0072a580-check → getter A → FUN_004641f0 → FUN_00567c50 @0x0058E0B7 |
| B | FUN_005b72c0 @0x005B72C0 | **komunikat executora type 0xB9** | ZS3_PSEUDO_004B18D0 case 0xb9; FUN_007527f0/00 extract {klucz,klucz,u8,u8}; FUN_00567c50 @0x005B7567 |
| C | FUN_00514ef0 @0x00514EF0 | **tabela handlerów .rdata** (DANE @0x00A7D778; run 0x00A7D764: 0x00511A90, 0x0040BB70, 0x00474410, 0x006077C0, 0x0058E280, **0x00514EF0**, 0x00606EC0...) | ZS10_ALL_REFS: jedyny xref FUN_00514EF0 = DATA @0x00A7D778; sąsiadztwo stringów ArkClientWorldObjectLogic @0x00A7D624 |

Wszystkie trzy wołają **FUN_00567c50 @0x00567C50** (3 call-site'y: 0x0058E0B7,
0x005B7567, 0x00515345 — ZS10_ALL_REFS), a ta po bramkach stanu (FUN_009768d0:
0x175/0x1b2b/0x170d/0x1bdc/0x173/0x1fa4/0x2ac5; local_b0 = porównanie encji z getterem A)
woła **FUN_00567770(FUN_004123d0(param_2), param_2)** @0x0056836C (disasm okno
ZS2 DISASM FUN_00567c50_call_00567770: PUSH-y + CALL @0x0056836C).

## 2. Kto wywołuje settery (Z1-warp) — zasilanie z atrybutów

FUN_00567770 czyta pozycję z drzewa atrybutów (FUN_00846840 — switch
0x6A4/0x6A5/0x6A8/0x6A9; mnożniki _DAT_00a7b260-family; macierz przez FUN_0096cdd0)
+ trójkę z FUN_00854720 (+0x68/+0x6c/+0x70) — **oba odczyty muszą się udać**
(`bVar2 = bVar1 & 1 & bVar2`), inaczej rekord NIE powstaje (negatywna kontrola — patrz Z5).
Potem: ctor FUN_00730700 → FUN_004c5580 (deriver sub-obiektów: "Level01_0_BASE",
"volume_0_BASE", "placename_0_BASE", "GeoText_0_BASE", "face_0_BASE/BUMP" — mechanizm
generyczny; wywołania warunkowe po atrybutach 0x657/0xd82/0x2140/0x3d1c) → settery
FUN_00730f60/f90/fb0/fd0 → rejestracja nazwana (FUN_004148f0/FUN_00457930).

Callery setterów f90/fb0 (z RUN 3 + weryfikacja tego runu): 15 funkcji —
FUN_0050bed0, FUN_00457cd0, FUN_00459270, FUN_00442190, FUN_00447630, FUN_004b3a00,
FUN_0043a200, FUN_004c47f0, FUN_0046e790, FUN_00488920, FUN_0067bc90, FUN_0067ccd0,
FUN_00567170, FUN_005b5f90, FUN_00567770. Ich napęd: FUN_00567170 ← FUN_00567b40
(capacity-gated push, czyta D-getterem — patrz Z4); FUN_005b5f90 ← FUN_005b6370
(handler komunikatu w FUN_005b72c0-ścieżce).

## 3. Łączenie z template'em (space ID) i instancją modelu

- Template: rejestr DAT_00ba1824 (RB-tree; lookup FUN_0072f580 — RUN 3). W tym runie:
  deriver FUN_004c5580 woła FUN_004c5480 (arg 0x4E26!) → FUN_0043a550 → **FUN_0072f880**
  (rodzina lookupu 0x0072fxxx) → FUN_008492c0 — TEN SAM rejestr obsługuje obiekty
  template'u; getter A = FUN_007ce1e0 ([ECX+0x08]), B = FUN_00746550 ([+0x04]),
  C = FUN_006b22d0 ([+0x0C]), D = FUN_0048ada0 ([+0x10]).
- Encja: ctor ArkObject FUN_00726e70 (A → encja@+0x28 — RUN 3). Klasy encji świata:
  **ArkRealWorldItem** (TD 0x00B8E944, vtable 0x00A873D8, create-slot FUN_0073a9e0,
  ctor z zapisem vtable @0x0074FFC8), ArkRealWorldProvider, ArkInteractiveWorldObject
  (create FUN_0073a8d0). Create-y rodzin ArkObjectClassImpl (vtable slot1) mają
  0 bezpośrednich callerów = **dispatch przez rejestr klas wirtualnych**
  (ArkObjectClass::create = FUN_0070bf50, RUN 3) — ArkObjectService (vtable 0x00A7BF9C,
  slot0 FUN_004a9810) / ArkObjectCommander (0x00A7BFCC, slot0 FUN_004a9830) /
  ArkClientObjectManagerImpl (2 vtable 0x00A7C028/0x00A7C0A0, slot0 FUN_004a9b90/d0)
  = warstwa rejestru/menedżera.
- Instancja modelu: FUN_006cb6f0 → pump {0x66, A} → ArkModelResourceInstanceRef →
  FUN_006cb020 "<id>__<name>" → kolejka FUN_006cb3c0 (RUN 3 — bez zmian; ten run
  potwierdza spójność przez attr 0x42=0x66 w FUN_0043f4b0 i FUN_005b6890).

## 4. Diagram (krawędzie NIEUDOWODNIONE jawnie: [NIEUDOWODNIONE])

```
[?] producent danych transformu ............................ [NIEUDOWODNIONE — patrz Z1 GRANICA]
   | (a) pliki Data\Parameters\*.vfs (store FUN_0094dfc0; parser FUN_00730c90-family)
   | (b) komunikat 0xB9 executora (payload {k32,k32,u8,u8}; producent = handler kanału
   |     zarejestrowany dynamicznie — brak xref)  [NIEUDOWODNIONE: producent]
   | (c) write-y klienta FUN_00845f70 z FUN_00514ef0/004387a0/005146b0 (H2)
   v
[SYSTEM ATRYBUTÓW: manager 0x8c DAT_00ba12e8; klucz→mapa (FUN_008544d0);
 rekordy ArkParameterContainer (create FUN_0073a160 wirtualnie); typy transformu
 {0x6a4,0x6a5},{0x6a8,0x6a9},{0x23,0x6ac}]
   |
   | 3 napędy: (A) FUN_00468910→FUN_0058db50 (update per-frame)
   |           (B) executor Execute FUN_004b2950→dispatch FUN_004b18d0 case 0xB9
   |               →FUN_005b72c0 (odczyt kursorami FUN_00752700/40)
   |           (C) tabela .rdata 0x00A7D764 → FUN_00514ef0 (write 0x2b/0x2c = X/Y!)
   v
[FUN_00567c50 (bramki stanu 0x170d/0x1bdc/...) @0x0056836C]
   v
[FUN_00567770 — BUILDER REKORDU PLACEMENTU]
   |- odczyt pozycji: FUN_00846840 (switch 0x6A4/0x6A5/0x6A8/0x6A9) + FUN_00854720
   |- ctor rekordu FUN_00730700; deriver FUN_004c5580 (sub-obiekty _BASE/_BUMP)
   |- SETTERY: FUN_00730f90 (pozycja@+0x08), FUN_00730fb0 (rotacja@+0x14),
   |  FUN_00730fd0 (@+0x20 {bits 0x1bdc, 0}); init FUN_00730f60
   |- rejestracja nazwana: FUN_004148f0 (singleton 0x178 DAT_00ba1288) + FUN_00457930
   v
[REKORD PLACEMENTU {poz@+0x08, rot@+0x14, +0x20/+0x24}] + [QUEUE push FUN_00567b40]
   |
   | (attach modelu: dispatcher atrybutów FUN_0043f4b0 → attr 0x39=model-id,
   |  0x42=0x66 → FUN_006c6040/FUN_006c5c00 attach ze skALĄ 1.0;
   |  ścieżka zasobu: FUN_006cb6f0 → "<A>.nif" — RUN 3)   [NIEUDOWODNIONE: krawędź
   |  rekord-placement→węzeł NIF statyka — bez zmian wg RUN 3]
   v
[ENCJA ArkObject (A@+0x28 z template'u; klasy ArkRealWorldItem/...; create przez
 rejestr ArkObjectClass) → instancja modelu → pending-attach FUN_006cb3c0 → scena]
```

## 5. NOT_CHECKED (jawne)
1. Komplet ciał wirtualnych ArkObjectService/Commander/Manager (rejestr klas:
   mapowanie class-id FOURCC (EODN/EODO/EOEC — bajty potwierdzone w manglingu;
   kodowanie MSVC $0+4 znaki) → obiekt klasy).
2. Fun_00474410/FUN_0058E280/FUN_00511A90 (pozostałe wpisy tabeli 0x00A7D764).
3. Tablice handlerów 74/72 @0x00A7D8EC/0x00A7DA34 (pełna enumeracja typów
   komunikatów CWO-Logic; census head-ów w S13_CWO_HANDLER_TABLE.json).
4. FUN_00841920 (worker resolvera FUN_00843d60) — dump istnieje (ZS10), analiza
   pól niepełna (poza budżetem; nie blokuje werdyktów).
