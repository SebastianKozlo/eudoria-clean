# REPORT — PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913

**RUN_ID:** `PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913` · **RUN_CLASS:** LOAD_BEARING
**Tryb:** STATIC-ONLY — klient/Frida/x32dbg/mock/sieć: NIEURUCHOMIONE. Warstwa „wykonanie silnika-klienta" NIEOBECNA (nie maskowana nazwą „oracle").
**Era:** EU 9.3.5 · **Bin:** `pcg_install\Entropia.exe` SHA256 `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` (8 015 872 B; PE32; base 0x00400000; .text RVA/Raw 0x1000; ASLR OFF — S0 fail-closed PASS 17/17 spot-checków).
**Świadectwo:** wszystkie dekody wykonawcy z FIZYCZNEGO EXE (własny PE parser `pe935_core.py` + capstone 5.0.7 + Ghidra 11.2.1 do censusów na WŁASNEJ kopii GHIDRA_LOCAL). Hexdumpy Desktopu = warstwa POCHODNA, użyta wyłącznie do weryfikacji krzyżowej na końcu (§D-1: bajt-identyczne).

---

## 1. GŁÓWNE PYTANIE (kontrakt §2)

**Czy dostawca korekty Z (FUN_00853A80 wywoływany przez managera mapy parametrów [FUN_004154F0] w ścieżce tworzenia instancji MovableObject) prowadzi do TERENU (heightfield), i czy TEGO SAMEGO klucza/instancji model łączy TEN SAM transform?**

### ODPOWIEDŹ WYKONAWCY (w granicach STATIC-ONLY):

1. **Dostawca korekty Z prowadzi do RUNTIME'U TERENU.** Pełny łańcuch własnych bajtów (§3.2):
   `FUN_004C46C0(+)` → `FUN_004154F0()` (singleton [0x00BA12E8], mgr1) → `FUN_00853A80(mgr1, pos.x, pos.y, 0, 0)` → filtr AABB `FUN_00755F90(mgr1+0x58, {x,y,0})` → provider2 `ArkMoveSubsystem` (mgr1+0x4C, side-query, wynik odrzucany) → **provider1 = mgr1+0 = „aktualny obiekt" — w stanie-2 maszyny stanów FUN_0044CEE0: MaTerrainManagerRuntime ([mgr3+0x18])** → `EnterCriticalSection(mgr1+0x50)` → `MaTerrainManagerRuntime::vtable[+4]` (FUN_00934540) → `[this+8]` (dane terenu) → `FUN_00936C30(x, y)`: indeks komórki `FUN_00936A60` (**cell_id = (floor(x/cell)<<16) | (floor(y/cell)&0xFFFF)**, cell=[data+0x34]) → resolver węzła `FUN_00935870` → **named-resource lookup** `FUN_00934670` (tag 0x6E) → system zasobów (FUN_00415670→FUN_00823C10) → lock `FUN_009347E0` → samplowanie `FUN_00935CB0` + interpolacja `FUN_00936B10` → wynik z **FCHS** (negacją) w ST0. Fallbacki: brak węzła → **10.0f** (_DAT_00a7b128); lock-fail → −1000.0f; provider1==NULL → 0.0; filtr-fail → 0.0.
   - **Dowód RTTI (własny, z EXE):** vtable 0x00A7F430 (mgr3+0x18 ctor FUN_00538B70 `mov [esi],0xa7f430`) → COL 0x00AA1920 → TD 0x00B79A28 → **`.?AVMaTerrainManagerRuntime@@`**; vtable bazowy 0x00A7F420 → ta sama klasa (drugi interfejs).
   - **Status:** TERRAIN-PROVIDER **CONFIRMED** na poziomie łańcucha statycznego receiver→provider→runtime-terenu→indeksowanie→samplowanie→interpolacja→wynik. **Granica jawna:** fizyczny FORMAT i PLIKI komórek terenu (za seamem resource-resolution FUN_00415670/FUN_00823C10) pozostają NIEDEKODOWANE w tym runie — łańcuch domknięty do seamu, nie do bajtów datasetu; NIE przypisuję heightmapy 50.bnt/field-decode temu providerowi (kontrakt §4 pkt 5 — zakaz domykania przez zbieżność liczb).

2. **Tożsamość instancja→model→transform:** pozycja SKORYGOWANA (z') osiąga instancję (+0x44..0x4C) przez ctor z kopii (UDOWODNIONE bajtowo, §3.3); sub-obiekt +0xC0 = **SceneFeederObject** (RTTI `.?AVSceneFeederObject@@`) dostaje pozycję **przez KOPIĘ WARTOŚCI** (FUN_005094C0: [SF+0x34..0x3C]=[instance+0x44..0x4C], flag +0x28=1) — NIE przez pointer identity. Ścieżka dalej do modelu (SceneFeeder→NiAVObject) = **NOT_DEMONSTRATED w tym runie** (§3.4 + jedno alternatywne doświadczenie).

3. **4508/296445: OPEN** (domyślnie, bez dodatniego dowodu użycia tej ścieżki przez ich definicje; pozycje 296445 NIEODZYSKANE; D@4508=124.941 ANCHORS_ABSENT_SEMANTICS_OPEN — podtrzymane własną arytmetką f32 0x42F9E1CB=124.94100189208984).

---

## 2. FAZA 1 — adjudykacja F1/F2/F3 audytu Desktop (własne kontrpróby z bajtów)

### 2.A F1 — gramatyka FUN_007343E0 (deserializacja struktury 0x28 → rec+0x0C)

**Twierdzenie Desktop:** FUN_007343E0 odczytuje strukturę z maską u16, NIE tworzy subkursora, zwraca ten sam kursor, pierwszy u16 = maska, wariant/pozycja kontynuują ten sam strumień.
**Adjudykacja wykonawcy: ACCEPTED** — każdy element potwierdzony własnym dekodem (`01_RAW/F007343E0_STRUCTURE_MASK.txt`, `F007453D0_DESERIALIZER.txt`, `F004C32F0_READ_F32.txt`, `F0040DE60_ADVANCE.txt`):

| Element | Własny dekod (VA/bajty) | Zgodność |
|---|---|---|
| ABI arg1=kursor | `MOV ESI,[ESP+0xC]` @0x007343E2 | ✓ (pin §12.1) |
| ABI arg2=destination | `MOV EDI,[ESP+0x14]` @0x00734416 | ✓ (pin §12.1) |
| caller dst=rec+0x0C | `8D 57 0C; 52; 55; E8` @0x00745414-19 | ✓ (pin §12.1) |
| Maska u16 @kursor | `MOVZX EBX,WORD [EAX+ECX]` @0x007343FB; advance(2) @0x00734403 | ✓ |
| dst+00 pary 0x002/0x004 | `TEST BL,2`/`TEST BL,4` @0x00734413/28; FLDZ @0x0073441C / FLD1 @0x0073442D; czyszczenie bitu AND | ✓ (pin §12.1) |
| dst+08 pary 0x008/0x010 | @0x00734443/55; FLDZ/FLD1 | ✓ |
| dst+0C pary 0x020/0x040 | @0x00734474/86 | ✓ |
| dst+10 pary 0x080/0x100 | @0x007344A5 (TEST BL,BL/JNS = bit7)/0x007344B6 | ✓ |
| dst+14 pary 0x200/0x400 | @0x007344D8/ED | ✓ |
| Oba bity pary: gałąź 0 wygrywa, bit 1 w reszcie | sekwencja AND czyści tylko bit-0; suita: maska 0x006 → residual 0x004 | ✓ (pin §12.1) |
| 3 bezwzględne odczyty dst+18/1C/20 | @0x0073450F/0x00734538/0x00734571; kontrola [ESI+0x11]+bounds [ESI+0xC]+4 vs [ESI+8]; fail → FLDZ→0.0f + flaga:=0; advance=FUN_0040DE60(4) | ✓ |
| dst+24 = reszta maski | `MOV WORD [EDI+0x24],BX` @0x00734597/@0x007345B0 | ✓ |
| **dst+04 NIGDY niepisan** | 0 zapisów dst+04 w FUN_007343E0; suita dst04_sentinel_preserved=True | ✓ (pin §12.1) |
| Oba epilogi EAX=kursor wejściowy | `8B C6` (MOV EAX,ESI) @**0x0073459C** i @**0x007345B5** | ✓ treścią; **rozjazd D-3 na pinach** (Desktop 0x0073459B/0x007345B4 = POP EDI, off-by-one; regiony dispatchu 0x00734596/0x007345A5 = bajty pośrednie CALL/FSTP) |
| Arytmetyka: 0→34B; 2AA/554→14B; 7FE→14B+reszta 0x554 | model+dekoder: 34/14/14/14 + 0x554 (28/28 zgodnych) | ✓ (pin §12.1) |

**Suita masek (kontrakt §6 pkt 3; świadectwo SYNTHETIC, porównanie STAN KURSORA + ZAKRES ZAPISÓW):** 29 przypadków — maski 0/0x2AA/0x554/0x7FE, każda para oddzielnie + oba bity, bity nieużywane 0x800+, krótki bufor przed/po polu (flaga:=0, pola→0.0f), kursor wyczerpany (pos=0, wszystko 0.0f), dwa rekordy kolejno (14+14=28), NaN/Inf akceptowane strukturalnie (odczyt bez walidacji — historyczny czytnik fail-closed na bufor, nie na wartość), dst+04 sentinel preserved. Model (zamknięta forma) == dekoder (przebieg gałęzi) **28/28 + meta-check arytmetyki PASS** (`01_RAW/F1_MASK_SUITE.json`).

**FUN_007453D0 (pełny dekod):** ECX=rekord, arg1=kursor, RET 4; zwrot AL = flaga kursora @+0x11 (≠0 = „sukces/dane dostępne"). Pola: klucz u32→rec+0; para param-set FUN_004124B0→rec+4..0xB; struktura 0x28→rec+0x0C..0x30 (FUN_007343E0); wariant u16→rec+0x34 (read @0x00745435, store @0x0074543D); POZYCJA vec3→rec+0x38 (FUN_00412430 @0x0074545A); ROTACJA vec3→rec+0x44 (@0x00745465); u32→+0x50 (@0x00745483); u32→+0x54 (@0x007454B1); f32→+0x58 (FLD/FSTP @0x007454D9/DF); u8→+0x5C (@0x00745510). Krótki bufor: fail-closed PER POLE (0/NULL; f32→FLDZ 0.0f; flaga:=0 przy bounds-fail).

**Census konsumentów struktury 0x28 (F1 pkt 4, `01_RAW/F1_CONSUMER_CENSUS.json`):**
- FUN_007343E0: **1 call site** (tylko wewnątrz FUN_007453D0 @0x00745419). FUN_007453D0: **1 caller** (FUN_004C47F0 @0x004C483D).
- W kanale FUN_004C47F0 pola f90 rec+0x0C..0x30 są **WRITE-ONLY** (0 odczytów w ścieżce — read: +0, +4, +0x34, +0x38, +0x44, +0x50, +0x58, +0x5C; NIE +0x0C..+0x30).
- W INSTANCJI struktura @+0x14 (zero-init FUN_007345C0): pisarze pól dst+18/1C/20 = ctor FUN_0085B1B0 (z recordu: [FUN_0040B070(rec)]+8/+8/+0 przez FUN_00734220/40/60) oraz FUN_0045AC90 (z recordu +0x70/+0x64/+0x68); **readerów w zbadanym zakresie nie znaleziono** — boundary jawne.
- **dst+04 rozstrzygnięcie:** FUN_007345C0 zeruje **9×f32** (własny dekod: +0x00/+04/+08/+0C/+10/+14/+18/+1C/+20 — 9×FST/FSTP + word@+0x24=0; nota: T-15 ERRATA_R4 mówiło „8×f32" — miscount) — w tym dst+04; żaden inny pisarz dst+04 nie występuje w kanale → **dst+04 = zawsze 0.0f w cyklu życia tej struktury w badanym kanale**; reader dst+04: brak w zbadanym zakresie (boundary: NIE nazywam pola — brak konsumenta).

### 2.B F2 — korekta Z w FUN_004C46C0 (lokalna kopia, warianty {3..7})

**Twierdzenie Desktop:** lokalna kopia rekordu ([ESP+0x10]=rec+8=pos.x, [ESP+0x14]=pos.y, [ESP+0x18]=pos.z); dla {3..7}: h=FUN_00853A80(mgr, pos.x, pos.y, 0, 0); korekta tylko przez porównanie x87; rekord callera nie nadpisywany.
**Adjudykacja wykonawcy: ACCEPTED** — wszystkie piny §12.2 potwierdzone własnym dekodem bajt po bajcie:

| Element | Własny dekod | Zgodność z pinem §12.2 |
|---|---|---|
| Kopia lokalna [ESP+0x10/14/18] = rec+8/0xC/0x10 | kopia 11 dwordów @0x004C46E8-0x004C4737 ([esp+0x10]←[eax+8], [esp+0x14]←[eax+0xC], [esp+0x18]←[eax+0x10]) | ✓ |
| Łańcuch wariantów | `CMP ESI,3` @0x004C46F1 (flagi→`JE` @0x004C473B→0x004C4751); `CMP ESI,6` @0x004C473D; `5` @0x004C4742; `4` @0x004C4747; `7` @0x004C474C; `JNE` @0x004C474F→0x004C4792 | ✓ — korekta TYLKO {3,4,5,6,7} |
| Budowa argumentów | `FLD [ESP+0x14]` @0x004C4751; `PUSH 0`×2 @0x004C4755/57; `SUB ESP,8` @0x004C4759; `FSTP [ESP+4]` @0x004C475C; **`FLD [ESP+0x20]` @0x004C4760 = pos.x po przesunięciu stosu −16 (arytmetyka własna: [ESP+0x20−0x10]=[ESP_pre+0x10]=pos.x)** | ✓ (kontrakt prosił o samodzielne zweryfikowanie — ZWERYFIKOWANE) |
| Wywołania | `CALL FUN_004154F0` @0x004C4767 (`E8 84 0D F5 FF`); `MOV ECX,EAX` @0x004C476C; `CALL FUN_00853A80` @0x004C476E (`E8 0D F3 38 00`) — (this=mgr1, pos.x, pos.y, 0, 0) __thiscall RET 0x10 | ✓ |
| Porównanie x87 | `FSTP [ESP+0x44]`(h) @0x004C4773; `FLD [ESP+0x18]`(z) @0x004C4777; `FLD [ESP+0x44]`(h) @0x004C477B; `FCOM ST(1)` (D8 D1) @0x004C477F; `FNSTSW AX` (DF E0) @0x004C4781; **`FSTP ST(1)` (DD D9) @0x004C4783**; `TEST AH,0x41` (F6 C4 41) @0x004C4785; `JNE` (75 06) @0x004C4788→0x004C4790; fall-through **`FSTP [ESP+0x18]` (D9 5C 24 18) @0x004C478A**; `JMP` (EB 02) @0x004C478E→0x004C4792; odrzucenie h `FSTP ST(0)` (DD D8) @0x004C4790 | ✓ — **T-26 potwierdzony: FSTP @0x004C478A, nie 0x004C4789** |
| new+ctor | `PUSH 0x128` @0x004C4792 (`68 28 01 00 00`); `CALL FUN_00528E50` @0x004C47C1 (`E8 8A 46 06 00`) | ✓ |
| Rekord callera nietknięty | zapis tylko do [ESP+0x18] kopii lokalnej; insert do mapy @0x004C47DA po ctor | ✓ |

**(4) Pełna tabela x87 (kontrakt §3.2 pkt 4; MODEL INSTRUKCJI — STATIC-ONLY, bez pomiaru procesora):** 21 wierszy {z,h}×{equal/less/greater/unordered/±Inf/±0/±bitowe-0} (`01_RAW/F2_X87_TABLE.json`):
- z'=h **wtw** h>z ordered (C0=0,C2=0,C3=0 → TEST AH,0x41=0 → JNE nie wykonany);
- z=h (C3=1) → z'=z **BITY** (−0/+0 rozróżnione bitowo! z=−0,h=+0 → z'=0x80000000);
- h<z (C0=1) → z'=z; **NaN(h) → z'=z (≠ Math.max)**; NaN(z) → z'=NaN(bity z); unordered (C0=C2=C3=1) → JNE wykonany;
- ±Inf zgodnie z porządkiem total FCOM (h=+Inf>z→z'=+Inf; +Inf==+Inf→z'=+Inf bity z; z=+Inf,h=−Inf→z'=+Inf; −Inf==−Inf→z'=−Inf bity z);
- **TEST AH,0x41 = maska C0|C3** (status: C0=bit8→AH0, C3=bit14→AH6); JNE taken ⇔ (C0|C3)≠0 ⇔ NIE(h>z ordered). Potwierdzone 21/21.
- Semantyka oczekiwana §12.2: potwierdzona w każdym punkcie; **NIE ogłaszam równoważności z Math.max** (dywergencje: NaN(h), −0/+0 bitowo).

**(5)/(8) Cztery stany łańcucha pozycji (świadectwo SYNTHETIC — jawne):**
1. **raw position (bajty kursora):** f32 w strumieniu komunikatu (wariant/pozycja po strukturze 0x28 — konsumpcja zależna od maski); NaN/Inf przechodzą bez walidacji (historyczny czytnik akceptuje wartości, waliduje tylko bufor);
2. **f90 record (rec+0x38/+0x3C/+0x40 → placement +8/+0xC/+0x10):** kopia bajtów (FUN_00730F90: kopiowanie 3×f32; własne dekody struktury fazy B podtrzymane);
3. **corrected local copy ([ESP+0x10..0x18] FUN_004C46C0, z'@[ESP+0x18]):** dla {3..7}: z' = max-ordered(z, h) bitowo (tabela x87); dla pozostałych: z' = z;
4. **instance +0x44..0x4C:** ctor FUN_0085B1B0 `mov [esi+0x44],[eax]…[esi+0x4C],[eax+8]` z `FUN_00746560(record)=&record+8` — bajty KOPII POPRAWIONEJ.
   - Wartości niefinitywne w każdym stanie: raw→record: kopia bitowa (bez zmian); record→copy: tylko z' zmienia się przy h>z ordered; copy→instance: kopia bitowa. Zapis h wirtualny = brak modyfikacji L0/L1 w FUN_00853A80 (arg1/arg2 tylko odczytane — L0/L1 to lokalne; provider2 dostaje &L0 — patrz §3.2 granica).

**(6) CREATE vs EXISTING — OSOBNE mapy (kontrakt §3.2 pkt 6 + uwaga S-note 3):**
- **CREATE (FUN_004C46C0):** warunek korekty = wariant ∈ {3,4,5,6,7} (łańcuch CMP/JE — jw.); korekta na kopii; ctor bezwarunkowo po korekty.
- **EXISTING (FUN_004C47F0 @0x004C4840-0x004C489B — pełny dekod warunków):**
  1. `TEST AL,AL/JE` @0x004C4842/48: AL = zwrot FUN_007453D0 (flaga kursora) — fail → koniec;
  2. resolver `FUN_008544D0(mgr, key)` @0x004C485A: EAX = istniejąca wartość; `MOV [ESI],EAX` @0x004C4861 (zapis do wrappera procesora); `TEST EAX,EAX/JE` @0x004C485F/63: **NULL → ścieżka CREATE** (0x004C48D4);
  3. **wirtualny CALL slotu +0x14 (slot5):** `MOV EDX,[EAX]` (vtable wartości) @0x004C4865; `FLD [ESP+0x68]` (f90rec+0x58 = **Z2 f32 wektora-drugiego**) @0x004C4867; `PUSH ECX; MOV ECX,EAX (this=wartość); FSTP [ESP] (arg1=Z2); MOV EAX,[EDX+0x14] (slot5) @0x004C4871; FF D0 @0x004C4874` → **value->slot5(Z2)** — bezwarunkowy po resolverze; slot5=MovableObject::slot5 → value+0x98 (ERRATA_R4 [SE-R4-6] — vtable 0x00A91E4C slot +0x14 = FUN_0085B010, własny odczyt vtable potwierdza);
  4. **guard `FUN_0085B750` @0x004C4878 (`E8 D3 6E 39 00`):** własny dekod FUN_0085B750 = `MOV EAX,[ECX+8]; CMP 2/3/6/5/4/7 → JE OK; XOR EAX,EAX; RET` — **guard = wariant(value+8) ∈ {2,3,4,5,6,7}** (UWAGA: pozwala też wariant 2 — szersze niż {3..7} CREATE); `TEST AL,AL/JE` @0x004C487D/7F → fail = pomiń update pozycji (skok 0x004C489B = FUN_006B22D0(value));
  5. **set-pozycji `FUN_0085B3E0(value, &[f90rec+0x38], 1)` @0x004C488A (`E8 51 6B 39 00`)** — (T-21/T-24: stary pin 0x004C4875 = ostatni bajt FF D0 @0x004C4874-75);
  6. **rotacja `FUN_0085ADB0(value, &[f90rec+0x44])` @0x004C4896 (`E8 15 65 39 00`)**;
  7. `FUN_006B22D0(value)` @0x004C489D = `MOV EAX,[ECX+0xC]; RET` (zwraca value+0xC) — wynik ignorowany w tym miejscu.
  - **NOWE ODKRYCIE (własny dekod FUN_0085B3E0 pełne, `01_RAW/F0085B3E0_SET_POS_EXISTING_FULL.txt`): ścieżka EXISTING stosuje TĘ SAMĄ korektę Z (identyczny wzorzec FCOM/FNSTSW/FSTP ST(1)/TEST AH,0x41/JNE (cel JNE @0x0085B43F = FSTP ST(0), odrzucenie h)/FSTP [ESP+0x24] @0x0085B439 — zapis h przy h>z ordered) — BEZ bramki wariantu PRZED korektą** (jedyny warunek to dostarczenie pozycji: korekta bezwarunkowa w FUN_0085B3E0); następnie **pętla drop-to-ground**: krok = qword [0xA7AF80] = **0.100000001490116119384765625** (bits 0x3FB99999A0000000, tzn. f64(double(f32 0.1f)), nie kanoniczne f64 0.1 = 0x3FB999999999999A; wartościowo ≈0.1), maksymalnie 100 iteracji (CMP ESI,0x64), sonda `FUN_00415570()` (singleton mgr2 [0x00BA12EC]) + `FUN_0085B380`…(poprawka: FUN_00856800) = query na mgr2+0x44 (vtable slot+0x154!) z pozycją krokową; finalnie **value->vtable[+4](&final_pos, flaga)** (FUN_0085B0F0: wariant 3 → [value+0xC]->FUN_0085D240; zawsze [value+0x10]->FUN_00861330).
  - **SETTER W EXISTING NIE JEST BEZWARUNKOWY** (kontrakt §3.2 pkt 6 — potwierdzone): warunki = deserializacja OK + resolver non-NULL + guard wariant ∈ {2..7}; slot5(Z2) bezwarunkowy po resolverze.

**(7) Helper niedostępny:** FUN_004154F0 przy braku inicjalizacji = lazy-init (new(0x8C)+ctor FUN_008550C0; fail new → singleton NULL → zwraca NULL); **filter-fail → FUN_00853A80 zwraca 0.0 (ST0)** (FLDZ @0x00853AAD + RET 0x10); provider1==NULL → 0.0 (FLDZ @0x00853B50). Wpływ na z': h=0.0 → z'=0.0 wtw 0.0>z ordered (z<0), inaczej z'=z bity — tabela x87 rozstrzyga każdą komórkę (§2.B(4)); wartościowo z'=max(z,0), ale BITOWO z zachowuje bity z przy braku ścisłej przewagi h (equal→bity z; NaN(z)→NaN).

### 2.C F3 — zakres statyków + drobne korekty → ERRATA_R5

Zgodnie z kontraktem §3.3: poprawiona narracja żyje w **ERRATA_R5** (T-01..T-32 z cytatami verbatim plik:linia + disposition + uzasadnienie — `06_REPORT/ERRATA_R5.md`). Liczby wyprowadzone własnym narzędziem (28/29 suita; 21 wierszy x87; 104/15/14 censusy; 38 indeksów dispatchera — patrz ERRATA_R5 §1/T-25). Adjudykacja szczegółowa: F1 ACCEPTED, F2 ACCEPTED (+ nowe: EXISTING również koryguje Z bez bramki wariantu + drop-to-ground), F3 — korekty narracyjne ACCEPTED (statyki: NIEWYKAZANE/OPEN; źródło insertów: ograniczone do wykazanej ścieżki; piny P3 poprawione; GB4 supersession jedna tabela; rb-find→hash-map find; transform→liczba f32 o nieustalonej semantyce).

---

## 3. FAZA 2 — GŁÓWNY EKSPERYMENT: KTO DOSTARCZA KOREKTĘ Z (FUN_00853A80)

### 3.1 Pełny dekod FUN_00853A80 (własny, `01_RAW/F00853A80_Z_PROVIDER.txt`; szkielet §12.4 = oczekiwanie — NIE kopiowane; zgodność pozycyjna w §5)

**ABI:** __thiscall, ECX=this=mgr1 (z FUN_004154F0), 4 argumenty stosowe, **RET 0x10** ✓.

**Przebieg (VA/bajty własne):**
1. `SUB ESP,0xC` @0x00853A80; L0(arg1)@E−0xC @0x00853A83-88; `MOV ESI,ECX` @0x00853A8C; L1(arg2)@E−0x8 @0x00853A8E-96; L2=0.0 @E−0x4 @0x00853A9B-A0 — ✓ pin „SUB ESP,0xC; L0/L1/L2=0.0".
2. `LEA ECX,[ESI+0x58]` @0x00853A9D; `CALL FUN_00755F90(this=mgr1+0x58, &L0)` @0x00853AA4; `TEST AL,AL/JNE` — **fail → FLDZ; POP ESI; ADD ESP,0xC; RET 0x10 → zwrot 0.0** @0x00853AAD-B3 ✓.
3. `CMP [ESI+0x4C],0` @0x00853AB6; ≠0 → provider2: `MOV ECX,[ESI+0x4C]` @0x00853AC4; argumenty: FLD [ESP+0x14](arg1)→L0 @0x00853ABC-C7; `MOV EAX,[ESP+0x20]`=**arg4** @0x00853AC0; FLD [ESP+0x18](arg2)→L1 @0x00853ACB-D1; `MOV EDX,[ECX]; MOV EDX,[EDX+4]` (slot+4) @0x00853AD4-36; `LEA EAX,[ESP+8]=&L0; PUSH EAX` @0x00853AD9-DD; `CALL EDX` @0x00853ADE → **provider2->slot4(&L0, arg4)**; **wynik odrzucony** (żaden FSTP po call; przepływ dalej bez odczytu EAX/ST0 jako wyniku — patrz granica §3.5).
4. `CMP [ESI],0` @0x00853AE0; **==0 → JE 0x00853B50 → FLDZ→return 0.0 (FALLBACK 0 gdy provider1==NULL)** ✓.
5. ≠0 → `MOV ECX,[ESI+0x50]; CALL FUN_00413440` @0x00853AE5-E8 = **EnterCriticalSection([mgr1+0x50])** — **ROZJAZD z pinem §12.4: pin mówił FUN_00413340; własny dekod: FUN_00413440 (`51; FF 15 [0xA75064]=KERNEL32!EnterCriticalSection; C3`); FUN_00413340 = adres POŚREDNI (środek instrukcji poprzedniej funkcji — nie jest startem funkcji)**.
6. L0=arg1, L1=arg2 (reload @0x00853AED-B01); `MOV EAX,[ESP+0x1C]`=**arg3** @0x00853AF1; `TEST EAX,EAX/JE` → **dwie formy**:
   - **arg3≠0:** `MOV EDX,[ECX]; MOV EDX,[EDX+4]` @0x00853B07-09; `PUSH EAX`(arg3); `LEA EAX,[ESP+8]=&L0; PUSH EAX`; `CALL EDX` @0x00853B12 → provider1->slot4(&L0, **arg3**); `FSTP [ESP+0x14]`(S) @0x00853B14;
   - **arg3==0 (@0x00853B2B):** `MOV EAX,[ECX]; MOV EAX,[EAX+4]`; `PUSH 0`; `LEA EDX,[ESP+8]=&L0; PUSH EDX`; `CALL EAX` @0x00853B37 → provider1->slot4(&L0, **0**); `FSTP [ESP+0x14]`(S) @0x00853B39;
   - obie: `MOV ECX,[ESI+0x50]; CALL FUN_00413450` = **LeaveCriticalSection** (release) @0x00853B1B/0x00853B40; `FLD [ESP+0x14]`(S); POP ESI; ADD ESP,0xC; **RET 0x10** — **wynik = provider1->slot4 (f32 w ST0)** ✓ (jedno źródło zwrotu; provider2 nie zasila wyniku).
   - **ROZJAZD:** release = FUN_00413450 (`51; FF 15 [0xA7506C]=KERNEL32!LeaveCriticalSection; C3`), nie „FUN_00413340".

### 3.2 Manager (mgr1) i providerzy — identyfikacja klasowa

**mgr1 = singleton [0x00BA12E8]** (getter FUN_004154F0: lazy `PUSH 0x8C` ✓ + ctor FUN_008550C0; **BRAK vtable/RTTI** — identyfikacja metodą dopuszczoną kontraktem: konstruktorzy/writerzy):
- +0x00/+0x04 = para wskaźników (ctor NULL; patrz niżej — „aktualny obiekt" + jego +4);
- +0x10 = hash_map (STLport, `PUSH 0x64`=100 bucketów @0x00855107, ctor FUN_00854C00);
- +0x2C..+0x40 = lista dwukierunkowa (sentinel init @0x00855113-30);
- +0x44/+0x48/+0x50 = **trzy obiekty new(0x20) = wrappery CRITICAL_SECTION** (ctor FUN_00413590 = `call [0xA75068]=InitializeCriticalSection` + magic 0x1FE319BA @+0x1C; nazwa = PUSTY string @0xA7957B; **[mgr1+0x50] = CS używany przez FUN_00853A80**);
- +0x4C = provider2 (ctor NULL);
- +0x54 = new(0x4C) przez FUN_00854E40 (setter FUN_00855340);
- +0x58..+0x8C = 13 floatów (ctor: FLDZ + 13×FST — filter AABB + rezerwa).

**Provider2 (mgr1+0x4C) = ArkMoveSubsystem : ArkMoverInterface** — RTTI z EXE (własny odczyt COL→TD):
- zapis: **FUN_0048EF00** (ctor ArkMoveSubsystem: `mov [esi],0x00A7BA54` @0x0048EF3A) → `FUN_0048EF96`: mgr1=getter; **`FUN_00855340(mgr1, esi, 0xEA60, &13-float-config, …)`** — a **FUN_00855340** @0x0085536D: `MOV [EBX+0x4C],EAX` (provider2=arg) + `REP MOVSD`×13 z configu → mgr1+0x58 (filter AABB!) + [mgr1+8]=arg + [mgr1+0xC]=0 + new(0x4C)→[mgr1+0x54] — **writer census: jedyny zapis mgr1+0x4C w binarium** (census4/5);
- vtable 0x00A7BA54 → COL 0x00A9FB80 → TD 0x00B717E0 = **`.?AVArkMoveSubsystem@@`**; baza 0x00A7BA48 → TD 0x00B717C0 = **`.?AVArkMoverInterface@@`**;
- **slot+4 = FUN_0048E7D0** (`@0x0048E7D0: arg1/arg2 → FUN_004147F0 → FUN_0044C9F0`) — ciało zdekodowane: FUN_004147F0 = **getter mgr3 [0x00BA1280]** (new(0xCC), ctor FUN_0044C950 — wszystkie pola NULL); FUN_0044C9F0(this=mgr3, vec3* L, flag): bounds (qword [0xA7B098]=−500.0 vs x/y), `MOV EDI,[mgr3+8]` (grid; NULL→koniec), wymaga flag≠0; liczy przedziały komórkowe (fist; qword [0xA79A08]=0.5) → **`FUN_0093F710(mgr3+8, &range, 0)`** — query na gridzie; **wynik odrzucony przez FUN_00853A80 (side-effect: powiadomienie/inkrementacja w move-gridzie)**; skutki na L0/L1: brak (L0/L1 tylko odczytane przed wywołaniem; provider2 dostaje &L0 — co robi z nimi wewnątrz = granica patrz §3.5).
- konfiguracja filter: 13 floatów z [0xA7BA38]=−32767.0 / [0xA7BA3C]=+32767.0 → **filter accept-all przy rejestracji** (min=−32767, max=+32767 na osiach x/y; wartości z EXE własne).

**Provider1 (mgr1+0) = „aktualny obiekt" kontekstu — w stanie-2 maszyny FUN_0044CEE0: MaTerrainManagerRuntime:**
- **writerzy (własny census5):** `FUN_00853A50(this, val)` = `MOV EAX,[ESP+4]; MOV [ECX],EAX; RET 4` (zapis +0) oraz `FUN_00797280(this, val)` = zapis **+4** — wołane wyłącznie z **FUN_0044CC60/0044CCA0/0044CD30/0044CD70** (rodzina metod mgr3), wywoływanych z **FUN_0044CEE0** (jedyny caller @0x0048D3C5):
  - stan 2 (`FUN_0044CC60` @0x0044CC63-89): mgr1+0 = **[mgr3+0x18]**, mgr1+4 = [mgr3+0x18]+4 (lub 0 przy NULL);
  - stan 1 (`FUN_0044CD30` @0x0044CD33-5F): mgr1+0 = **[[mgr3+0]]** (dwie dereferencje), mgr1+4 analogicznie+4;
  - `FUN_0044CCA0`/`FUN_0044CD70`: mgr1+0/+4 = NULL (reset).
  - mgr3 = singleton [0x00BA1280] (getter FUN_004147F0 — TEN SAM, który zasila provider2-slot4!). mgr3+0x18: ctor FUN_0044C950=NULL; **writer: FUN_0044D0F0-rodzina @0x0044D210: `MOV [EDI+0x18],EAX` po `new(0x14)+FUN_00538B70`** — a FUN_00538B70: `MOV [ESI],0x00A7F430; MOV [ESI+4],0x00A7F420` @0x00538BA9 i @0x00538BAF (0x00538BB5 = ostatni bajt drugiego zapisu);
- **RTTI (własny):** vtable 0x00A7F430 → COL 0x00AA1920 → TD 0x00B79A28 = **`.?AVMaTerrainManagerRuntime@@`** (drugi vtable 0x00A7F420 → ta sama TD — drugi interfejs tej klasy);
- **slot+4 = FUN_00934540** (własny dekod, `§1` wyżej): `[this+8]`==NULL→FLDZ 0.0; arg2(=arg3 FUN_00853A80)≠0→`FUN_00936D50([this+8], x, y, arg2)`; else→`FUN_00936C30([this+8], x, y)`; RET 8 z wynikiem w ST0;
- **FUN_00936C30 (rdzeń):** `FUN_00936A60(this, [this+0x34], y, x)` → ebx = **cell_id=(floor(x/cell)<<16)|(floor(y/cell)&0xFFFF)** (własny dekod: FILD cell; x/cell; floor; fist; `SHL ESI,0x10`; y/cell; floor; fist; `AND EAX,0xFFFF; OR EAX,ESI`); `FUN_00935870(this, ebx)` → węzeł (NULL→**zwrot _DAT_00a7b128=10.0f**); `FUN_009347E0(node, −1, 0)` lock-check (fail→**−1000.0f** [0xA7B270]); `FUN_00935CB0(this, ebx, x, y, &3×vec3)` samplowanie; `FUN_00936B10(…)` interpolacja; wynik = iloczyn/suma z **FCHS** (negacja) w ST0;
- `FUN_00935870` buduje dwa puste std::string → **`FUN_00934670` → FUN_00415670 (singleton systemu zasobów) → FUN_00823C10`** — **komórki terenu = zasoby NAZYWANE** (tag 0x6E) — łańcuch domknięty do seamu resource-resolution (granica §3.5).

**Fallbacki (kontrakt §4 pkt 3):** filter-fail → 0.0 (FLDZ @0x00853AAD); provider1==NULL → 0.0 (FLDZ @0x00853B50); provider1 slot+4 z [mgr1+0]==NULL inside MaTerrainManagerRuntime → 0.0 (FUN_00934540 FLDZ @0x00934586); brak węzła terenu → 10.0f; lock-fail → −1000.0f. **Filter = FUN_00755F90 (pełny dekod, `01_RAW/F00755F90_FILTER.txt`): AABB 3D — min@(this+0/4/8), max@(this+0xC/0x10/0x14) — akceptuje wtw A≤L<B per oś, (L0,L1,L2)=(arg1, arg2, L2=0.0 STALE!) → kwerenda przechodzi wtw min.z ≤ 0.0 < max.z (region musi obejmować zero na trzeciej osi)**; konfiguracja: rejestracja ArkMoveSubsystem ustawia 13 floatów (domyślnie ±32767) = REGION GATE korekty Z.

**FUN_00413340 (żądane przez kontrakt/dekret):** adres 0x00413340 **nie jest startem funkcji** (bajty `28 C2 08 00…` = środek poprzedniej instrukcji; funkcja kończąca się @0x0041335B (RET 8) zaczyna się przed 0x00413344; kolejna funkcja zaczyna @0x00413360 (SEH prolog, RET 8 @0x00413427)). Rzeczywiste wywołania FUN_00853A80 @0x00853AE8/0x00853B1B/0x00853B40 to **FUN_00413440 = thunk EnterCriticalSection** i **FUN_00413450 = thunk LeaveCriticalSection** (importy rozstrzygnięte własnym parsowaniem IAT: [0xA75064]=KERNEL32!EnterCriticalSection, [0xA7506C]=KERNEL32!LeaveCriticalSection). Semantyka [mgr1+0x50] = **CRITICAL_SECTION** (lock/acquire + release — odpowiedź na pytanie kontraktu).

### 3.3 Konsument FUN_00853A80 (census)

Własny census (E8 aligned, boundary-checked): **15 call sites** (nie tylko FUN_004C46C0!):
- **FUN_004C46C0** @0x004C476E (CREATE — korekta z');
- **FUN_0085B3E0** @0x0085B41D (EXISTING — korekta z'; NOWE);
- **FUN_0048BFF0** @0x0048C05B/0x0048C0A9/0x0048C0FB/0x0048C14D/0x0048C19F/0x0048C1E5/0x0048C22B/0x0048C271/0x0048C2B7 (**9×**): sampling w promieniach qword [0xA7B9F0]=**14.0** i [0xA7AF88]=**25.0** wokół pozycji, porównanie z **10.0f** ([0xA7B128] = fallback „brak terenu") → selekcja dźwięków **WAVES_01/02/03** (FUN_008B6510/008B6550) — detekcja granicy terenu/wody (licznik próbek == fallback);
- 0x0044A925/0x0044A9EF/0x0045BA76/0x0045BF90/0x0085B41D — pojedyncze wywołania w innych funkcjach (konteksty funkcji w DECOMP_P2).
Semantyka zbiorcza: **FUN_00853A80 = zapytanie o wysokość terenu w (x,y) w regionie filtera** — konsument WAVES wzmacnia H-TERRAIN (porównanie do fallbacku 10.0 = „czy poza terenem").

### 3.4 Hipotezy H-TERRAIN / H-COLLISION / H-OTHER (kontrakt §4 pkt 4)

| Hipoteza | Przewidywania rozstrzygające | Wynik |
|---|---|---|
| **H-TERRAIN** | provider1 = klasa z RTTI zawierającym „Terrain"/heightfield; slot+4 prowadzi do samplowania danych wysokościowych po (x,y); konsument porównuje do progu „poziomu wody/braku terenu" | **POTWIERDZONE**: `.?AVMaTerrainManagerRuntime@@`; slot+4→FUN_00936C30(x,y)→cell_index→node→sample/interp→FCHS; WAVES porównuje z 10.0f=fallback. Komórki = NAMED RESOURCES (tag 0x6E) |
| **H-COLLISION** | provider = system kolizji/fizyczny; wynik = wysokość kolizji | **ODRZUCONE jako główne**: główny wynik zasila się z MaTerrainManagerRuntime; przesłanki „collision" istnieją w SĄSIEDZTWIE (mgr2 [0xBA12EC] = query vtable+0x154 = zgoła kolizyjny sondaż drop-to-ground w FUN_0085B3E0; provider2=ArkMoveSubsystem → grid ruchu) — ale one NIE zasiliają zwrotu FUN_00853A80 (provider2 side-effect; mgr2 = osobny singleton poza FUN_00853A80) |
| **H-OTHER** (scenka/fizyka/proxy) | brak powiązania z terenem | **ODRZUCONE**: RTTI + łańcuch samplowania + konsumenci (Z-korekta, WAVES) wiążą wynik z terenem |

**Predykat G5 NEUTRALNY** (bez „terrain" w predykacie) — PASS zależny od struktury, nie od nazwy. **Nie przypisuję heightmapy 50.bnt/field-decode temu providerowi** (zakaz domykania przez podobieństwo — kontrakt §4 pkt 5); format plików komórek = NIEDEKODOWANY w tym runie.

### 3.5 Granice jawne (Faza 2)

1. **Provider2→(L0,L1) side-effects:** FUN_00853A80 przekazuje &L0 providerowi2; wewnątrz FUN_0093F710 (query gridu mgr3+8) możliwe są zapisy węzłów gridu — **dokładny efekt uboczny na L0/L1 (modyfikacja? zapis do gridu?) NIE zdekodowany w tym runie** (FUN_0093F710 = 0x93F710, poza zakresem); po powrocie L0/L1 są **przeładowywane z oryginalnych arg1/arg2** (@0x00853AED-B01), więc wpływ na WYNIK wykluczony bajtowo; wpływ na STAN providerów = UNPROVEN.
2. **Wynik provider2 w ST0:** FUN_00853A80 nie robi FSTP po CALL EDX @0x00853ADE — gdyby provider2 zwracał f32 w ST0, wartość pozostałaby na stosie x87 (ryzyko overflow przy serii). Odczyt ciał (FUN_0048E7D0→FUN_0044C9F0: RET 8 bez FLD zasilającego ST0) wskazuje, że **provider2 zwraca wynik przez EAX/pamień (puste w ST0)** — SEMANTYKA ZWROTU provider2 = UNPROVEN-dokładnie (granica zapisu; niewpływająca na wynik FUN_00853A80).
3. **Format komórek terenu:** za seamem FUN_00415670/FUN_00823C10 (named resources) — NIE dekodowane; osie/jednostki [this+0x34] (cell size) i stałych qword (0.5/−500.0/14.0/25.0/0.1) = wartości liczbowe z EXE; **semantyka osi (x/y/z; konwencja znaku po FCHS) NIE rozstrzygnięta** (zakaz §4 pkt 5: osie TYLKO tam gdzie wynikają z kontraktu/przeliczeń — tu nie wynikają).
4. **mgr1+0 w stanie-1:** [[mgr3+0]] — pisarz mgr3+0 nie był celem tego runu (mgr3+0 = inny obiekt niż mgr3+0x18 — status UNPROVEN dla stanu-1; stan-2 = MaTerrainManagerRuntime CONFIRMED).

---

## 4. FAZA 3 — POWIĄZANIE Z CELEM (ścieżka +0xC0; jedna)

### 4.1 ClientMovableObject sub-obiekt +0xC0 (§12.5 — weryfikacja pozycyjna w §5)

Własny dekod ctor FUN_00528E50 (pełne):
- vtable bazowy `0x00A91E4C` (`.?AVMovableObject@@` — RTTI własny: TD 0x00B7997C) @0x00528E8D→FUN_0085B1B0; vtable pochodny `0x00A7DCB0` (`.?AVClientMovableObject@@` — TD 0x00B79958) @0x00528EA2;
- **base ctor FUN_0085B1B0(this, &kopia_poprawiona, wariant, string):** [+8]=wariant ✓; struktura@+0x14 zero-init (FUN_007345C0 @0x0085B1D3); pozycja 0.0f init @+0x44..0x4C; **[+0x74]=rekord[0] (klucz)** przez FUN_004123D0 (`8B 01 C3` — własny dekod) @0x0085B20A; [+0x78]=rekord[4] przez FUN_00746550; **[+0x44..0x4C]=[FUN_00746560(record)+0..8]=&record+8** @0x0085B27A-2D (FUN_00746560=`8D 41 08 C3` — 4 bajty); [+0x50..0x58]=globalne [0xBA921C/20/24]; rotacja przez FUN_0040B070(record)→[+0x5C..0x70]; FUN_00734220/40/60 piszą strukturę+0x18/1C/20 z recordu.
- **+0xC0 (jedyna pełna ścieżka — kontrakt §5 pkt 1):** FUN_00528E50 @0x00528F9B-0x00528FE6: `FUN_00746570` → push; `FUN_0085AD60(this, …)`; `FUN_00401360()` (mgr4 [0xBA1260]-rodzina) → `FUN_00485050(mgr4, arg4=1)` → **FUN_0048CBB0 → edi**; `FUN_0085B120(this,&local)` → push; `FUN_00414130(this)`=**[this+0x74]=klucz** (4 bajty `8B 41 74 C3`? — własny dekod: funkcja 4-bajtowa zwraca [this+0x74]) → push; `FUN_005247C0(edi, &local, klucz)` → **`[this+0xC0]=EAX`** @0x00528FEA;
- **FUN_005247C0 (własny dekod):** `PUSH 0x98; CALL new` → **FUN_00509330(new_0x98, edi, arg1, arg2)** → esi; `FUN_005094E0(esi, &edi+0xC0)` (back-ptr; gated `[this+0x2C]>>4&1`); `FUN_006A8980(edi+0x24, &l1, &l2)` (rejestracja w liście holdera); zwrot esi;
- **FUN_00509330 (własny dekod):** vtable **0x00A7D458 = `.?AVSceneFeederObject@@`** (RTTI własny: TD 0x00B78834); +0x14=arg1; `new(0x118)`→FUN_007B6000→[+0x30] (obiekt scenowy, refcount @+4); pozycja/rotacja domyślne z [0xBA921C/20/24] (2×); struktury 0x24 z [0xB93C80]; `new(0x14)`→FUN_0064B1E0(new, [+0x14])→push; **`FUN_007B6A80([+0x30], EAX, 0xA7D444)`** (rejestracja z vtable 0xA7D444);
- **argumenty tworzenia (§5 pkt 1 — create arg3):** `FUN_004C4640` = getter singletona **[0x00BA26B8]** (new(0x1C)+FUN_00766480; **ignoruje argumenty, zwraca singleton** ✓ §12.5); `FUN_00765930(this=singleton, &f90rec+0x8C, X2)` — własny dekod: **this NIECZYTANE** (ECX nadpisany @0x00765956 przed użyciem); konstruuje **pusty basic_string("" @0xA7957B) W f90rec+0x8C** i zwraca wskaźnik → **arg3 ctor = pusty string (konstrukcja w rekordzie f90, nie w singletonie)** — §12.5 potwierdzone z rafinacją mechanizmu (singleton wezwany, ale vestigialny w tym call-sitem).
- **guard w ctorze:** `FUN_0085B750(this)` @0x00528FFD (wariant ∈{2..7}) → `[+0xC0]->+0x2C |= 1` (jeśli guard OK) / `&= ~1`;
- **konfiguracja sub-obiektu:** `FUN_005094C0(SF, &[this+0x44])` — **KOPIA WARTOŚCI [SF+0x34..0x3C]=[instance+0x44..0x4C] + flag SF+0x28=1** (własny dekod: 3×MOV + `MOV BYTE [ECX+0x28],1`); `FUN_00509510(SF, &[this+0x5C])` → [SF+0x74..0x7C] + dalsze; `FUN_00509070(SF, &[this+0x50])`; `FUN_00509850(SF, 0, 0.0)`.

### 4.2 Rozdzielenie kluczy/ID (tabela — kontrakt §5 pkt 2)

| Klucz/ID | Przechowanie | Źródło | Konsument | Dowód (VA) | Rola |
|---|---|---|---|---|---|
| klucz instancji (instance key) | **instance+0x74** | rekord[0] (klucz u32 kursora) przez FUN_004123D0 @0x0085B20A | FUN_00414130 (getter [this+0x74]); FUN_00856190 (insert mapy: key=[value+0x74]) | @0x0085B211, 0x00528FD9 | tożsamość w mapie parametrów |
| parent/holder key | holder (FUN_0048CBB0) — NIE w instancji | mgr4 [0xBA1260]-rodzina | FUN_005247C0 rejestruje w holder+0x24 | @0x00528FE1, 0x0052483D | relacja holder↔SceneFeederObject |
| param-set ID (class/param) | **instance+0x78**; f90 rec+4..0xB (para 2×u32) | rekord[4] przez FUN_00746550 | selektor FUN_008553D0 (typy 0x4E34/0x4E38/0x5DC9 — własne porównania @0x004C48AE/0x004C48B9/0x004C48C4 i @0x004C498A-0x004C49A2); zapis do +0x88 (faza B) | @0x0085B21B | klasyfikacja param-setu (≠klucz!) |
| wariant (u16) | **instance+8** | rec+0x34 (u16 kursora) | guard FUN_0085B750 ({2..7}), rate-limiter FUN_0085B780 ({3:5, {4..7}:0x14}), FUN_0085B0F0 (==3→slot na +0xC), korekta Z CREATE ({3..7}) | @0x0085B1CA | tryb obiektu (≠klucz, ≠param-set) |
| template ID (rekord VFS) | VFS record (templates.vfs) | rejestr definicji | lookup FUN_0072F580 (rb-find FUN_004D1430 — INNA funkcja, NIE-target) | R_REPORT:121 (utrzymane) | definicja szablonu |
| model resource ID | resource system (pump 0x66=MODEL,A — RUN3) | atrybut-drzewo | ArkModelResourceInstanceRef→FUN_006cb020 „<id>__<name>" | RUN3 (nie re-derivowane) | zasób modelu |
| string tworzenia | f90rec+0x8C (pusty basic_string) | FUN_00765930("" @0xA7957B) | arg3 ctor FUN_004C46C0/FUN_0085B1B0 | @0x00765974, 0x004C4937 | nazwa (pusta w tym kanale) |

**TEN SAM numer/offset ≠ ta sama rola** — utrzymane (tabela własna, VA z własnych dekodów).

### 4.3 Tożsamość instancja→model→transform (kontrakt §5 pkt 3)

- **Instancja→SceneFeederObject: UDOWODNIONE (pointer identity at creation):** [instance+0xC0] = wynik FUN_005247C0 (ten sam obiekt rejestrowany w holder+0x24 i zwracany — jeden pointer, trzy relacje) ✓;
- **Transform SKORYGOWANY → instancja: UDOWODNIONE bajtowo:** z' w kopii → ctor: [instance+0x44..0x4C]=kopia+8..0x10 (FUN_00746560=&kopia+8) — **z' (nie surowy bajt kursora) osiąga instancję** ✓;
- **Transform → SceneFeederObject: KOPIA WARTOŚCI, nie pointer identity:** FUN_005094C0 kopiuje [instance+0x44..0x4C] do [SF+0x34..0x3C] i ustawia dirty-flag +0x28 — **pojedynczy snapshot w ctorze; późniejsze zmiany instance+0x44 NIE propagują się automatycznie przez ten zapis** (propagacja wymagałaby ponownego wywołania — status: NIE zbadany w tym runie);
- **SceneFeederObject → model (NiAVObject/ArkModelResourceInstanceRef): NOT_DEMONSTRATED w tym runie** — ścieżka RUN3 (pump {0x66=MODEL,A} → ArkModelResourceInstanceRef ctor FUN_006FA8B0 → FUN_006cb020 „<id>__<name>" → registration) = INNY kanał (atrybut-drzewo); połączenie SceneFeeder→model-resource bez dekodu slotów FUN_0050A460/0x5090A0/… pozostaje otwarte. **NIE twierdzę sąsiedztwa wywołań = tożsamość.**
- **Status formalny (kontrakt G6): TRANSFORM_TO_SCENEFEEDER_PROVEN (value copy, ctor-time); TRANSFORM_TO_MODEL = NOT_DEMONSTRATED.**

### 4.4 4508/296445

**OPEN** — bez dodatniego dowodu, że definicje 4508/296445 korzystają z tej ścieżki. Pozycje 296445 **NIEODZYSKANE**. D@4508: f32 0x42F9E1CB = 124.94100189208984 (własna arytmetka f32 — zgodna z fazą A) — semantyka NIEUSTALONA (ANCHORS_ABSENT_SEMANTICS_OPEN); **NIE ogłaszam STATIC_INSTANCE_MECHANISM_CONFIRMED ani źródła placementu statyków.**
**JEDNA alternatywna ścieżka (kontrakt §5 pkt 4):** dekod slotów SceneFeederObject (vtable 0x00A7D458: FUN_0050A460(slot+4), FUN_005090A0/B0, FUN_0050A050, FUN_005090C0, FUN_00509580) — tam gdzie SceneFeeder konsumuje [SF+0x34..0x3C] (pozycję) i swój obiekt 0x118/[+0x30] — wspólna funkcja z kanałem modelu (resource instance ref) byłaby ścieżką łączącą transform z modelem w JEDNYM obiekcie; uzasadnienie: to jedyny znany nośnik poprawionej pozycji poza instancją w tym kanale.

---

## 5. Zgodność z pinami AUDITOR_EXPECTATION (§12) — pozycyjnie

**§12.1 (F1):** ABI ✓; epilogi — treść ✓ (MOV EAX,ESI w obu), **piny VA: ROZJAZD off-by-one** (mierzone 0x0073459C/0x007345B5 vs Desktop 0x0073459B/0x007345B4; patrz ERRATA_R5 §2.D-3); maska+tabela par ✓ (obie gałęzie każdej pary, bit-1 zostaje w reszcie przy obu bitach); 3 odczyty bezwzględne ✓ (kontrola flagi+bounds; fail→FLDZ→0.0f; advance FUN_0040DE60(4) — FUN_0040DE60 = `ADD [ECX+0xC],EAX; CMP; JBE; MOV BYTE [ECX+0x11],0; RET 4` — advance POZA limit ustawia flagę na 0); dst+04 niepisan ✓; FUN_007345C0 = zero-init szerszej struktury — **NIE dowód macierzy 3×3** ✓ (z rafinacją: 9×f32, nie 8×f32 — ERRATA_R5 T-15); arytmetyka 34/14/14/14+0x554 ✓.

**§12.2 (F2):** kopia lokalna ✓; łańcuch wariantów ✓ (wszystkie VA zgodne); budowa argumentów ✓ (FLD [ESP+0x20]=pos.x — samodzielnie zweryfikowana arytmetyką stosu); CALL-e ✓ (bajty E8 zgodne); porównanie x87 ✓ (FCOM D8 D1 / FNSTSW DF E0 / FSTP ST(1) DD D9 / TEST F6 C4 41 / JNE 75 06 → 0x004C4790 / FSTP D9 5C 24 18 @0x004C478A / JMP EB 02; odrzucenie DD D8); PUSH 0x128 + ctor E8 8A 46 06 00 ✓; semantyka z' ✓ (niezależnie potwierdzona tabelą 21-wierszową); TEST AH,0x41=C0|C3 ✓.

**§12.3 (P3):** MOV EAX,[EDX+0x14] @0x004C4871 + FF D0 @0x004C4874 ✓ (D-2: „0x004C4744-45" w dispatchu = literówka — tam leżą `05 74` środka CMP ESI,5/JE); guard FUN_0085B750 @0x004C4878 (E8 D3 6E 39 00) ✓; set-pozycji FUN_0085B3E0 **@0x004C488A** (E8 51 6B 39 00) ✓ (stary pin 0x004C4875 = błąd — T-21/22/23/24); rotacja FUN_0085ADB0 @0x004C4896 (E8 15 65 39 00) ✓; dispatcher byte-table **38 indeksów** (0xA2..0xC7; CMP EAX,0x25) / jump-table 22 ✓ (T-25).

**§12.4 (F2/P2 szkielet):** SUB ESP,0xC ✓; L0/L1/L2 ✓; filter FUN_00755F90(this=+0x58, &L0) z fail→0.0 ✓; CMP [ESI+0x4C] + provider2 slot+4 (ECX=[ESI+0x4C]; EDX=[ECX]; EDX=[EDX+4]; CALL EDX) ✓ z arg (&L0, arg4); CMP [ESI],0 → JE → FLDZ 0.0 ✓; **[ESI+0x50]: EnterCriticalSection/LeaveCriticalSection (FUN_00413440/FUN_00413450) — ROZJAZD: pin §12.4 „FUN_00413340 @0x00853AE8" — rzeczywisty cel wywołania = FUN_00413440; FUN_00413340 nie istnieje jako start funkcji**; slot+4 provider1 @~0x00853B07 (arg3≠0) / @0x00853B2B (arg3==0 — obie formy ✓); ponowny release = FUN_00413450 @0x00853B1B/@0x00853B40 (rozjazd jak wyżej); wynik f32 → RET 0x10 ✓; które wywołanie zasila zwrot: **provider1 (jedyny)** ✓; skutki uboczne provider2 na L0/L1: zdekodowane do poziomu przekazania &L0 (efekt wewnątrz FUN_0093F710 — granica §3.5); FUN_00413340→(poprawione: FUN_00413440/50)=lock acquire/release ✓ semantyką; FUN_00755F90 = bounds-check AABB na manager+0x58..(+0x6C; 13 floatów init — reszta +0x70..+0x8C NIECZYTANA przez filtr) ✓.

**§12.5 (P3):** FUN_00414130([this+0x74]) → FUN_005247C0 → new(0x98)+FUN_00509330 → [this+0xC0] ✓; create arg3: FUN_004C4640 ignoruje argumenty i zwraca singleton [0x00BA26B8] ✓; FUN_00765930 zwraca wskaźnik stringa ✓ **z rafinacją**: string konstruowany w f90rec+0x8C (this=singleton nieużywany w ciele); znana ścieżka modelu (RUN3) — **powiązanie przez TOŻSAMOŚĆ nie wykonane w tym runie (NOT_DEMONSTRATED — §4.3)**.

---

## 6. Macierz twierdzeń → dowód → artefakt

| # | Twierdzenie | VA/bajty (własne) | Receiver/test | Wynik | Artefakt |
|---|---|---|---|---|---|
| 1 | SHA/rozmiar/PE32/ASLR/.text | S0: 17 spot-checków VA→offset | s0_era.py fail-closed | PASS | 01_RAW/S0_ERA_ASSERTION.json |
| 2 | FUN_007343E0 = struktura 0x28 maskowana, EAX=kursor, dst+04 niepisan | 0x007343E0-0x007345BA | model+dekoder, suita 28/28 | CONFIRMED | F007343E0_*.txt, F1_MASK_SUITE.json |
| 3 | Konsumpcja 34/14/14/14+0x554 | arytmetyka | suita consumption | CONFIRMED | F1_MASK_SUITE.json |
| 4 | FUN_007453D0 zwrot=flaga; pola +0/+4/+0xC../+0x34/+0x38/+0x44/+0x50/54/58/+0x5C | 0x007453D0-0x00745537 | dekod | CONFIRMED | F007453D0_*.txt |
| 5 | Korekta Z CREATE warianty {3..7}, zapis h wtw h>z ordered, FSTP @0x004C478A | 0x004C4751-0x004C478E | tabela x87 21 wierszy | CONFIRMED | F004C46C0_*.txt, F2_X87_TABLE.json |
| 6 | EXISTING też koryguje Z (bez bramki przed korektą) + drop-to-ground 0.1×≤100 + vtable[+4] final | 0x0085B3E0-0x0085B5D9 | dekod pełny | CONFIRMED (NOWE) | F0085B3E0_..._FULL.txt |
| 7 | EXISTING warunki: slot5(Z2) bezwarunkowy; guard wariant∈{2..7}; set-pos @0x004C488A; rotacja @0x004C4896 | 0x004C4840-0x004C489B | dekod | CONFIRMED | F004C47F0_*.txt, X004C4840_489B_*.txt |
| 8 | FUN_00853A80 ABI RET 0x10; filtr→0.0; provider2 (side, arg4); provider1 (wynik, arg3/0); CS enter/leave | 0x00853A80-0x00853B61 | dekod + importy | CONFIRMED | F00853A80_*.txt, IMPORT_RESOLUTION.json |
| 9 | Provider2 = ArkMoveSubsystem:ArkMoverInterface (RTTI), writer FUN_0048EF00→FUN_00855340 (mgr1+0x4C + 13F + +0x54) | 0x0048EF00, 0x00855340, RTTI | dekod + census (jedyny zapis +0x4C) | CONFIRMED | P2_CENSUS4/5.json |
| 10 | Provider1 = mgr1+0 = „aktualny obiekt" (FUN_00853A50/797280 z FUN_0044CC60/CD30 — stan2: [mgr3+0x18]) | 0x0044CC60-0x0044CEE0, 0x0044D210 | census5 + dekod | CONFIRMED | P2_CENSUS5.json |
| 11 | mgr3+0x18 = MaTerrainManagerRuntime (RTTI .?AVMaTerrainManagerRuntime@@), slot+4=FUN_00934540 | 0x00538B70, RTTI TD 0x00B79A28 | dekod + RTTI | CONFIRMED | X00853A80_*.txt + §3.2 |
| 12 | Łańcuch wysokości: cell 16:16 → named-resource → sample → interp → FCHS; fallbacki 10.0/−1000.0/0.0 | FUN_00936A60/5870/4670/35CB0/36B10 | dekod | CONFIRMED do seamu | dekody w §3.2 |
| 13 | Filter = AABB 3D; L2=0.0 stała; region gate | FUN_00755F90 | dekod (6×FCOMPP) | CONFIRMED | F00755F90_*.txt |
| 14 | WAVES: 9× sampling w promieniach 14.0/25.0 vs 10.0 | 0x0048C05B-0x0048C2B7 | dekod + stałe | CONFIRMED (H-TERRAIN wzmacniacz) | DECOMP_P2/F0048BFF0.c |
| 15 | Kolejność: [instance+0x44..0x4C]=&kopia+8 (z'); klucz→+0x74; wariant→+8; param-set→+0x78 | FUN_0085B1B0 | dekod | CONFIRMED | §4.1 |
| 16 | +0xC0 = SceneFeederObject (RTTI); new(0x98) FUN_005247C0→FUN_00509330; pozycja KOPIĄ do SF+0x34 | 0x00528E50, 0x005247C0, 0x00509330, 0x005094C0 | dekod + RTTI | CONFIRMED | F00528E50_*.txt, F005247C0_*.txt |
| 17 | Transform→model (SceneFeeder→NiAVObject) | — | brak dekodu slotów SF w tym runie | **NOT_DEMONSTRATED** (granica) | §4.3/4.4 |
| 18 | 4508/296445 | — | brak dodatniego dowodu | **OPEN**; pozycje 296445 NIEODZYSKANE | §4.4 |

## 7. Liczebności własne i granice

- **Censusy własne:** callerzy FUN_004154F0: **104** (aligned 104/104); FUN_00853A80: **15**; FUN_00755F90: **14**; FUN_004147F0 (mgr3): **14**; singleton [0xBA12E8] direct-reads: 1 (getter) + writes: 2 (oba w getterze); writes mgr1+0x4C: **1** (FUN_00855340); writes mgr1+0 (dataflow callerów gettera): **0 bezpośrednich** — przez metody FUN_00853A50/797280 z rodziny FUN_0044CCxx (§3.2); zapisy [mgr+0x4C] w małych funkcjach całego .text: 1 kandydat (FUN_00855340 — jedyny prawdziwy; FUN_0058E2D0 = inna klasa).
- **Suita F1:** 29 przypadków (28 model==decoder + 1 meta-arytmetyka PASS); **tabela x87:** 21 wierszy.
- **RTTI własne:** MaTerrainManagerRuntime (0x00B79A28), ArkMoveSubsystem (0x00B717E0), ArkMoverInterface (0x00B717C0), SceneFeederObject (0x00B78834), ClientMovableObject (0x00B79958), MovableObject (0x00B7997C) — wszystkie odczytane z EXE (COL→TD→name inline).
- **Granice jawne:** (1) format/pliki komórek terenu za seamem resource — NIEDEKODOWANE; osie/jednostki nierozstrzygnięte; (2) provider2 side-effects wewnątrz FUN_0093F710; dokładna semantyka zwrotu provider2; (3) mgr1+0 w stanie-1 ([[mgr3+0]]) — pisarz mgr3+0 poza zakresem; (4) SceneFeeder→model — NOT_DEMONSTRATED; (5) 4508/296445 — OPEN; (6) 19 ctor-callers — NOT_CHECKED (kontrakt G6 boundary); (7) tabela x87 = MODEL instrukcji (STATIC-ONLY — nie pomiar procesora); świadectwa suity = SYNTHETIC (jawne).
- **Warstwy (kontrakt §6 pkt 2):** oryginalne bajty EXE (wszystkie VA/bajty w tym raporcie) / disassembly capstone (01_RAW/*.txt) / dekompilat Ghidra (01_RAW/DECOMP_P2 — warstwa pomocnicza censusów) / hipotezy (§3.4 tabela) / model syntetyczny (suita F1, tabela x87 — SYNTHETIC jawne) / **wykonanie silnika-klienta: NIEOBECNE**.

---

## 8. D-1 weryfikacja rozstrzygnięcia (wymóg dispatchu)

Okno 0x004C4780-0x478F ponownie zrute z FIZYCZNEGO EXE (`01_RAW/X004C4770_479F_D1_WINDOW.txt`): bajty `d1 df e0 dd d9 f6 c4 41 75 06 d9 5c 24 18 eb 02` — **bajt-identyczne z independent_hexdumps.txt:69** pakietu Desktop; `dd d9` @0x004C4783-84 obecne. **Desktop hexdump window 0x004C4780-0x478F re-verified byte-identical with EXE; D-1 closed as PE-MASTER reading error.** W ERRATA_R5 brak twierdzeń o brakujących bajtach; potwierdzonym defektem pozostaje off-by-one T-26.

---

*Raport wykonawcy; INTERNAL_QC w QC_REPORT.md; publikacja po adjudykacji PE-MASTER (osobny krok). Git: brak commitów ze strony wykonawcy.*
