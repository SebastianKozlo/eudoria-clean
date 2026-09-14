# SEAM FLOW MAP — MAPA PARAMETRÓW (szew insert→odczyt, zad. 1-4)

RUN: PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913 | ERA: EU 9.3.5 | STATIC-ONLY
Wszystkie VA = własne mapowanie (pe_core) + dekompilaty Ghidra (GH1-GH3) + piny bajtowe (T6_BYTE_PINS.json).

## 1. Kontener

**Manager** (singleton `DAT_00BA12E8`, rozmiar 0x8C, getter FUN_004154F0 @0x00415500-16 lazy-init PUSH 0x8C):
- +0x10: **STLport hash_map** (ctor FUN_008550C0 → CALL FUN_00854C00 z PUSH 0x64 = 100 bucketów; pin @0x008550FE: 8D 4E 10 6A 64)
  - map+0x08 = tablica bucketów, map+0x0C = koniec tablicy (mgr+0x18/+0x1C)
  - map+0x14 (mgr+0x24) = licznik elementów, map+0x18 (mgr+0x28) = max load factor (float)
- +0x2C..+0x40: druga wyzerowana struktura (5 dwordów + bajt; rola: NIE zdekodowana w tym runie — NIE jest mapą insertu)
- +0x44: CS-lock (ctor: new(0x20) → [0x00A75A38] InitializeCriticalSection; pin @0x00855164: 68 20 … E8 53 82 10 00; store 89 46 44)
- +0x58..+0x84: 12 floatów 0.0 (pole odczytu FUN_00853A80)
- Węzeł: {+0 next, +4 klucz u32, +8 wartość} (FUN_00971780: CMP [ECX+4],ESI; FUN_00854260: MOV [ECX],ESI / MOV [ECX+4],EDX / MOV [EAX],0; node_alloc::allocate(0xC))
- find = FUN_00971780 (87 isCall; hash: key % (n_bucketów-1), granica łańcucha = wartość następnego bucketa — schemat STLport _Hashtable z _Stl_prime)
- find-or-create = FUN_00854D90 (18 isCall — generyczna dla wszystkich hash-map; flaga out: 1=nowy węzeł, 0=istnieje)
- resolver = FUN_008544D0 (4 isCall: FUN_0085B840, FUN_004C4A10, FUN_004C47F0 ×2): EnterCS(mgr+0x44) → FUN_00971780 → **MOV ESI,[EAX+8]** @0x008544F9 → ExitCS → return wartość; miss → 0. RET 4 (klucz = 1. arg).

## 2. Klasa wartości (GB1)

**MovableObject** — RTTI `.?AVMovableObject@@` (vtable 0x00A91E4C; [vtable-4]=0x00AB33D0=COL; COL+0xC=0x00B7997C=TD; TD+8 = "2E 3F 41 56 4D 6F 76 61 62 6C 65 4F 62 6A 65 63 74 40 40"). 13 slotów vtable (slot0=FUN_0085B7F0 dtor; slot3=FUN_0085B6A0; slot5=FUN_0085B010; slot8=FUN_008E0110 …). Slot-0 unikalny w całym binarium (1 hit DWORD = sama vtable).
**ClientMovableObject** (pochodna) — RTTI `.?AVClientMovableObject@@` (vtable 0x00A7DCB0; zapis w ctorze FUN_00528E50 @0x00528EA3: C7 06 B0 DC A7 00; Ghidra: `*param_1_00 = ClientMovableObject::vftable`).

Ctor MovableObject FUN_0085B1B0(this, arg1=REKORD placementu 0x2C, arg2=WARIANT):
- +0x00 = vtable (pin @0x0085B1C3: C7 06 4C 1E A9 00)
- +0x04 = 0 (nullable lock; helper FUN_0085B190: if [v+4]≠0 → FUN_00413440)
- +0x08 = arg2 = WARIANT (pin @0x0085B1CC: 89 46 08) — small int 0..7; selektor 0x4E38: 4/5→2, 6→3, 7→4
- +0x14..+0x3B = macierz transformu 3×3 f32 + flaga word @+0x24 (FUN_007345C0: 9×FST zerowych + MOV WORD [EAX+0x24],0)
- +0x3C = 0 (dziecko; dtor slot0 zwalnia)
- +0x44/+0x48/+0x4C = **POZYCJA vec3 = [rekord+8/+0xC/+0x10]** (FUN_00746560 = `8D 41 08` LEA EAX,[ECX+8] → kopia 3 dwordów) — pin T6
- +0x50..+0x58 = DAT_00ba921c/20/24 (global vec3)
- +0x5C..+0x64, +0x68..+0x70 = 2× vec3 z FUN_0040B070()
- +0x74 = **[rekord+0] = KLUCZ** (CALL FUN_004123D0 @0x0085B204 z ECX=EDI=arg1; FUN_004123D0 = `MOV EAX,[ECX]; RET` — deref!)
- +0x78 = [rekord+4] (FUN_00746550 = `8B 41 04`)
- +0x88/+0x8C = **[rekord+0x20]/[rekord+0x24] = ID PARAM-SETU + pole2** (FUN_00746570 = `8D 41 20`)
- +0x98 = 1.0f
Ctor ClientMovableObject FUN_00528E50(this, rekord, wariant, arg3, arg4): baza → vtable pochodna → pola +0xA4..+0x124 → warunek: FUN_00414130([x+0x74]) → FUN_005247C0(klucz,…) → this+0xC0 = wynik lookupu → settery flag [+0xC0+0x2C] → inicjalizacje sub-obiektów → [this+0xB4] = [this+0x64].

Callerzy ctorów (census isCall): FUN_0085B1B0 = **1** (FUN_00528E50); FUN_00528E50 = **1** (FUN_004C46C0). Insertowane wartości = ClientMovableObject (jedyna droga do mapy).

## 3. INSERT-SEAM (GB2)

```
FUN_004C46C0(rekord 0x2C, wariant, arg3, arg4)                     [jedyny creator]
  ├─ jeśli wariant∈{3,4,5,6,7}: FUN_004154F0(mgr) → FUN_00853A80(mgr, 2×f32) → max(rekord[4], wynik)
  ├─ operator_new(0x128)                                            @0x004C4792 (pin: 68 28 01 00 00; CALL new)
  ├─ FUN_00528E50(nowy, rekord, wariant, arg3, arg4)               @0x004C47C1
  ├─ FUN_004154F0() → ECX=manager                                   @0x004C47D3
  └─ FUN_00856190(manager, nowa_wartość)                            @0x004C47DA (pin: 8B C8 E8 B1 19 39 00)

FUN_00856190(mgr, wartość)                                          [INSERT — VA-locked]
  ├─ if [wartość+0x74] == 0 → return 0                              (83 7F 74 00)
  ├─ EnterCS(mgr+0x44)
  ├─ klucz = FUN_00414130(wartość) = [wartość+0x74] = rekord[0]     (8B CF E8 7F DF BB FF; 89 44 24 0C)
  ├─ FUN_00856090(mgr+0x10, [mgr+0x24]+1) = rehash-if-needed       (load factor; _Stl_prime::_S_next_size)
  ├─ para na stosie: {slotA=klucz, slotB=wskaźnik wartości}        (89 7C 24 14)
  ├─ FUN_00854D90(map, out{node,flag}, &para) = find-or-create      (E8 B5 EB FF FF)
  │     └─ FUN_00854260(&para): node_alloc(0xC); node+4=para[0]=klucz; node+8=para[1]=WARTOŚĆ; next=0
  ├─ flag != 0 → sukces: LeaveCS → return 1
  └─ flag == 0 (klucz istniał) → value->vtable slot0(PUSH 1) = DELETING DTOR zniszczenia duplikatu → LeaveCS → return 0
```
FUN_00845F70 = **writer-do-istniejącego-kontenera** (lock [this+4]+0x30 → FUN_005275E0(parent,klucz,&out) → LeaveCS; NIE woła FUN_00854D90/FUN_00856190) — NIE creator. 53 isCall (użytkownicy API atrybutów).

## 4. ŹRÓDŁO DANYCH (GB4)

**Komunikaty** (primary): dispatcher FUN_004B18D0(typ, kursor) — case 0xB0→FUN_004574F0(kursor), **case 0xB9→FUN_005B72C0(kursor)** @0x004B1A16 (pin E8 A5 58 10 00), 0xC6→FUN_004B0AB0, 0xC7→FUN_004B1670; case 0xBC→advance+FUN_00458030.
- FUN_004C47F0 (processor placementu, 4 callerów = ww. handlery): FUN_00745360(init struktury) → **FUN_007453D0(rekord, KURSOR) = deserializacja**: rekord+0 = KLUCZ u32; +0x34 u16; +0x50/+0x54/+0x58 = POZYCJA vec3 (3×u32, advance 4); +0x5C = WARIANT bajt (advance 1); każdy odczyt fail-closed (flaga@kursor+0x11) → resolver(klucz) → gdy brak: settery f90(pozycja→rekord+8/+0xC/+0x10), fb0, fd0(param-set→rekord+0x20) → FUN_004C46C0(rekord, wariant) → INSERT → composer.
- FUN_005B72C0 (0xB9): FUN_007527F0(subtyp) → **FUN_00752700(kursor → {KEY,KEY2, 2 bajty})** @0x005B73B3 / typ-2 **FUN_00752640(kursor → {KEY,KEY2, bajt})**; walker(KEY), walker(KEY2); distance-check (FUN_004b2a20 vs FUN_0085aff0×DAT_00a79e28); FUN_005B6890(KEY, 0x42/0x39, payload); FUN_005B6370→FUN_005B5F90 (tworzenie z def-id) — driver(KEY) @0x005B7567.
- Read-cursor ops: FUN_00752700/26 40 — layout kursora {+0 data, +8 size, +0xC offset, +0x11 flag}; advance = FUN_0040DE60(n).

**VFS** (definitions, NIE insert-map): FUN_00452490 → FUN_0072FA30 (string "Parameters\templates.vfs" @dekompilat L81) → FUN_00972DF0 (ArkVFS01/02: CreateFile→ReadFile 8B→magic→[+0xA0]=version) → pętla: FUN_00730C90(kursor→rekord 5×u32: A..E; pin MOV [EDI+8],EAX @0x00730CE6) → FUN_00730700 (ctor węzła rejestru) → FUN_0072F8D0 (insert do RB-REGISTRY). Odbiór definicji: FUN_0043A550/FUN_0072F580 (rb-find FUN_004D1430; rekord@hit+0x14; 25 isCall) — konsumenci: FUN_00567170 (def-id imm32 **0x3BDB**), FUN_005B5F90 (def-id = param_1), FUN_004C47F0-NIE (korzysta z klucza instancji).

**NEGATYW**: FUN_0094BD30/FUN_0094F350 (parsery VFS-cache) — brak krawędzi do lejów insertu (funnel FUN_00856190←FUN_004C46C0; census 6+1 callerów — żaden w regionie 0x0094xxxx). Parsery te NIE zasilają mapy parametrów (bounded census; granica: ich payload = poza zakresem).

## 5. Konsument POZYCJI (odczyt po insercie)

composer FUN_008553D0(klucz): walker → wartość → FUN_0085AD50(wartość)=+0x88 → CMP 0x4E34/0x4E38/0x38B0; getterA → wariant(+8) → switch 4/5/6/7; slot3-wirtualny → f32 ptr; **pozycja_kompozycja = slot3[i] + wartość+0x44/0x48/0x4C** → FUN_00415570/FUN_008599A0 (dispatch render/fizyki; 2 isCall composer2). value+0x44..0x4C = pozycja z rekordu (setter f90 ← deserializat @+0x50..0x58).

## 6. Pełny łańcuch (jedno zdanie)

KOMUNIKAT (typ 0xB0/0xB9/0xC6/0xC7 → kursor) → deserializata {KLUCZ u32 @+0, POZYCJA vec3 @+0x50, WARIANT bajt @+0x5C} → settery (f90: pozycja→rekord+8..0x10; fd0: param-set→rekord+0x20) → FUN_004C46C0 → ctor: KLUCZ=rekord[0]→wartość+0x74, POZYCJA=rekord+8..0x10→wartość+0x44..0x4C, WARIANT→wartość+8 → FUN_00856190: para{KLUCZ, wskaźnik_wartości} → węzeł{next, KLUCZ, wartość} w hash-map@mgr+0x10 → odczyt: resolver(klucz)→[hit+8]=wartość→pola (+8 wariant, +0x44 pozycja, +0x88 param-set) — TEN SAM klucz wiąże komunikat, rekord, węzeł i instancję.
