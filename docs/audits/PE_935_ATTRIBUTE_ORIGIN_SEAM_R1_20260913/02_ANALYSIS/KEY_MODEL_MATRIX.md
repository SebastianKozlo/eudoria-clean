# KEY MODEL MATRIX — ścieżka transformu (zad. 3, GB3)

RUN: PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913 | ERA: EU 9.3.5 (pcg_install)
Binarium: Entropia.exe SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
Każda krawędź: PROVEN = VA + bajty (T6_BYTE_PINS.json) + dekompilat (01_RAW\DECOMP) + dataflow.
UNPROVEN = jawne. Atrybucja: własne wykonanie (Ghidra headless GH1-GH3 na kopii GHIDRA_LOCAL + pe_core własne bajty).

## 0. Poziomy wskaźników (pointer levels — rozróżnienie jawne)

```
klucz (u32, z komunikatu/deserializatu; = record[0])
  -> hash: klucz % (liczba_bucketów-1)          [FUN_00971780: MOV EDI,[map+0xC]; SUB EDI,[map+8]; SAR EDI,2; SUB EDI,1; IDIV]
  -> bucket -> łańcuch węzłów {+0 next, +4 key, +8 value}   [FUN_00971780: CMP [ECX+4],ESI; MOV ECX,[ECX]]
  -> hit (węzeł)  [FUN_00854D90: *param_1 = node; flag=0 istnieje / 1 nowy]
  -> [hit+8] = wartość = MovableObject/ClientMovableObject*  [FUN_008544D0: MOV ESI,[EAX+8] @0x008544F9]
  -> wartość: +0 vtable, +8 wariant, +0x44..0x4C pozycja f32 vec3, +0x74 = klucz (kopia!), +0x88 ID param-setu, +0xB4 f32
```
Klucz i wartość są związane DWUSTRONNIE: klucz = node+4 = wartość+0x74 (oba = record[0] z tego samego rekordu placementu).

## 1. Krawędzie ścieżki transformu (builder + driver)

| # | Krawędź (caller → callee @site) | Klucz/arg (wartość) | Receiver (ECX/this) | Status |
|---|---|---|---|---|
| E1 | dispatcher FUN_004B18D0 case 0xB9 → FUN_005B72C0 @0x004B1A16 | param_2 = KURSOR komunikatu | brak (statyczna) | PROVEN (E8 A5 58 10 00; dekompilat switch) |
| E2 | FUN_005B72C0 → FUN_007527F0 @subtype | kursor | kursor | PROVEN (dekompilat L93) |
| E3 | FUN_005B72C0 → FUN_00752700 @0x005B73B3 | kursor → out {KEY u32, KEY2 u32, bajt, bajt} | kursor | PROVEN (census 1 caller; dekompilat: 4/4/1/1 advance FUN_0040DE60) |
| E3' | FUN_005B72C0 → FUN_00752640 (typ-2) | kursor → out {KEY u32, KEY2 u32, bajt} | kursor | PROVEN (dekompilat: 4/4/1) |
| E4 | FUN_005B72C0 → FUN_0085B840 @2 site'y (walker-init) | KEY / KEY2 z komunikatu | walker_ctx | PROVEN (dekompilat L117/L121; walker: ctx[0]=resolver(mgr,key)) |
| E5 | FUN_005B72C0 → FUN_00567C50 @0x005B7567 | arg1 = KEY (local_70) | this = obiekt queue (EDI) | PROVEN (raw E8; prolog drivera: EBP=arg1 @0x00567C88) |
| E6 | driver FUN_00567C50 → getterD FUN_0048ADA0 @0x00567D16 / @0x00567D46 | — (odczyt pola) | ECX = ESI = **arg3 = rekord stanu** (czyta [record+0x10]) | PROVEN (pin: 8B CE E8..; prolog ESI=arg3 @0x00567C90) — rozstrzyga granicę #2 PKG_A |
| E6' | driver → getterD @0x00567F72 | — | ECX = [ESP+0x20] = EDI = **this (queue)** | PROVEN (pin 8B 4C 24 20 + E8 29 2E F2 FF) |
| E7 | driver → FUN_00567B40 (queue-push) @0x00567D24/D54 | args: &out, EBX, wartość gettera D | ECX = EDI = this (queue) | PROVEN (pin E8 17 FE FF FF / E8 E7 FD FD FF) |
| E8 | driver → getterA FUN_007CE1E0 (na singletonie 0x00BA1260) + CMP EBP,EAX @0x00567CC9 | porównanie KEY == [singleton+8] | ECX = [0x00BA1260] | PROVEN (pin 8B C8 E8 15 65 26 00; 3B E8) |
| E9 | driver → builder FUN_00567770 @0x0056836C | arg1 = KEY (uVar6 = EBP) | this = queue?? (Ghidra void) | PROVEN (census: JEDYNY caller buildera; dekompilat drivera L543) |
| E10 | builder → FUN_00846840 (key-walker: pozycja wg klucza) @0x005677C4 | param_1 = KEY | walker-ctx | PROVEN (pin E8..; dekompilat: walker-init FUN_0085B840(param_1) + 4× FUN_0085B860 + kompozycja vec3) |
| E11 | builder → settery: FUN_00730F60 @…, FUN_00730F90 @0x00567906, FUN_00730FB0, FUN_00730FD0 | pozycja = skomponowany vec3 (local_c8/c4/c0); fb0 = -Z (local_10c[8]); fd0 = {0.0,0.0} | this = rekord placementu | PROVEN (dekompilat builder L161-171; settery zdekodowane: f90: record+8/+0xC/+0x10 = vec3; fd0: record+0x20/+0x24) |
| E12 | builder → FUN_00853A50 @0x005678DC | zapis pola = **0x1BDC** (imm32) | this = rekord | PROVEN (pin; FUN_00853A50 = *this=param_1) |
| E13 | builder → FUN_00457930 @0x00567985 | rekord 0x2C + 2 + string | — | PROVEN (census/dekompilat; zwraca NOWY KLUCZ w EAX) |
| E14 | builder → FUN_008553D0 (composer) @0x005679B8 | arg1 = NOWY KLUCZ (uVar12) | ECX = manager (z FUN_004154F0 @0x005679B3) | PROVEN (pin E8 13 DA 2E 00) |
| E15 | builder → FUN_0085B840 (walker) @0x005679C2 | TEN SAM NOWY KLUCZ | walker-ctx | PROVEN (pin E8 79 3E 2F 00) |
| E16 | builder → FUN_00567030 (rej. callbacku) | (FUN_00855dc0, manager, NOWY KLUCZ, 0) | — | PROVEN (dekompilat L269) |
| E17 | builder → FUN_00844020(0x1BDE) / FUN_0040bfe0(0xE10,0,2) | imm32 0x1BDE, 0xE10 | — | PROVEN (dekompilat L257/L275) |
| E18 | composer FUN_008553D0(key) → FUN_0085B840/860 (22 site'y) + getterA + slot3 wirtualny + FUN_00415570/FUN_008599A0 | klucz z E14; odczyt wariantu (+8), ID param-setu (value+0x88 przez FUN_0085AD50=LEA +0x88), pozycji (value+0x44..0x4C + slot3) | ECX = value (MovableObject) | PROVEN (dekompilat selektora; FUN_0085AD50 pin: 8D 41 88 C3) |

## 2. Trzy napędy (drive A/B/C → driver)

| Napęd | Funkcja | Krawędź do drivera | Klucz na krawędzi | Status |
|---|---|---|---|---|
| A | FUN_00468910 → FUN_0058DB50 @0x00469299/0x004692AB/0x00469419 (3 site'y) → FUN_00567C50 @0x0058E0B7 | arg1 = uVar4 = FUN_00843D60(local_110) (klucz z rekordu local_110 ← FUN_00715E90) | PROVEN (pins E8..; prolog FUN_0058DB50: param_1 = 6-dword rekord; imm32 0x92E/0xDD0 na krawędziach FUN_007257F0) |
| B | FUN_005B72C0 (handler 0xB9) → FUN_00567C50 @0x005B7567 | arg1 = KEY z KOMUNIKATU (FUN_00752700) | PROVEN (pin; dispatch case 0xB9 @0x004B1A16) |
| C | FUN_00514EF0 (slot5 vtable **.?AVArkClientPlayerImpl@@** @0x00A7D778, vtable baza 0x00A7D764) → FUN_00567C50 @0x00515345 | arg1 = uVar7 = FUN_00726490(puVar9,puVar5,0) | PROVEN (pin; census 1 site; imm32 0x23A→FUN_00414B70, 0x3F1/0x3F5→FUN_00845F70) |

Napęd B to JEDYNA krawędź z dowiedzionym źródłem zewnętrznym (komunikat); A = rekord z subsystemu 0x00468xxx (world-object state), C = klasa playera (obiekt lokalny). Wszystkie trzy zbiegają się w arg1 drivera = KLUCZ instancji.

## 3. Klucze imm32 zaobserwowane na krawędziach (pełny wykaz z dekompilatów)

0x4E34 (20020), 0x4E38 (20024), 0x5DC9 (24009), 0x38B0 (14480) — ID param-setów (CMP w FUN_004C47F0: local_ac[0]≡record+0x20≡value+0x88; selektor: local_38≡*FUN_0085AD50(value)≡value+0x88)
0x1BDC (7132) — pole type-marker rekordu (builder E12) + check FUN_00978A10 w selektorze
0x1BDE (7166), 0xE10 (3600), 0x175 (373), 0x1B2B (6955), 0x3DC8 (15816), 0x92E (2350), 0xDD0 (3536), 0x23A (570), 0x3F1 (1009), 0x3F5 (1013), 0x3BDB (15323 — def-id FUN_00567170), 0x39/0x42 (podtypy FUN_005B6890)
Kluczem MAPY PARAMETRÓW jest ŻADEN z powyższych — klucz mapy = uchwyt instancji z rekordu placementu (record[0], z komunikatu). ID param-setu (0x4E34-rodzina) to ATRYBUT WARTOŚCI (+0x88), nie klucz mapy. (Korekta otwartego założenia Fazie A.)

## 4. Granice (UNPROVEN — jawne)

1. **Skąd bajty do kursora komunikatu**: FUN_004B18D0 ← 2 raw-callery (0x004B1BE6 region 0x004B1xxx; 0x004B29A9 w FUN_004B2950 = wpis vtable @0x00A7C200) — dalszy upstream (kolejka sieciowa vs lokalna) NIE prześledzony w tym runie (bounded). UNPROVEN.
2. **[singleton 0x00BA1260 + 8]**: porównywane z KLUCZEM (E8) — semantyka "własny klucz gracza/awatara" = HIPOTEZA (konsument = CMP; brak nazwy; granica: dekod właściciela singletonu).
3. **Osie/jednostki value+0x44..0x4C**: konsument istnieje (kompozycja w selektorze: *pfVar10 + [value+0x44]; setter f90; FUN_008599A0), ale przestrzeń (client-local/world) i jednostki NIE ustalone (task 7 discipline). HIPOTEZA do czasu dekodu slot3 (FUN_0085B6A0) i FUN_008599A0.
4. **Slot5 vtable C (FUN_00514EF0, 3901 B)**: częściowo rozkój (klucz z FUN_00726490) — pełna semantyka ruchu gracza poza zakresem.
