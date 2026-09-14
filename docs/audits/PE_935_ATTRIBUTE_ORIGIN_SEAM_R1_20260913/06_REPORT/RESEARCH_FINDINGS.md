# RESEARCH_FINDINGS — PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913

**RUN_CLASS: LOAD_BEARING. TRYB: STATIC-ONLY** (klient/Frida/x32dbg/mock/sieć NIE uruchomione; zero procesów poza Ghidra headless + Python).

- **ERA**: EU 9.3.5 (pcg_install). Binarium `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe`
  SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (8 015 872 B, base 0x00400000, ASLR OFF);
  templates.vfs SHA256 BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77. **S0 fail-closed PASS** (01_RAW\S0_ERA_ASSERTION.json).
- **REPO**: eudoria-clean @ BASE_SHA 5d0edde5863795d6eefd8bb11989e8edb7b28546 (deklaracja PE-MASTER; ten run NIE wykonuje operacji git).
- **AUDIT_OUTPUT_ROOT**: nieistniał przed runem (brak kolizji). Projekt Ghidra skopiowany z pakietu A
  (GHIDRA_LOCAL, 10 plików; manifest AT_COPY = db.67/68, zgodny bajtowo z manifestem finalnym pakietu A).
- **Atrybucja (3 poziomy, jawne)**: własne wykonanie = Ghidra headless GH1-GH3 na WŁASNEJ kopii projektu (65+39+22 funkcji zdekompilowane, censusy isCall, piny T6 z pe_core);
  odczyt cudzego artefaktu = dekompilaty/rejestr wyników pakietu A (01_RAW\F2_CTX*, RECEIVER_MATRIX.md) użyte jako PUNKT STARTOWY (każde twierdzenie pakietu A re-weryfikowane własnymi bajtami);
  cudza deklaracja = BASE_SHA repo (PE-MASTER), statusy QC Fazy A (cytowane z atrybucją).
- **Determinizm**: skrypty hashowane po ostatniej edycji przed wykonaniem (00_CONTROL\SCRIPT_SHA256.csv); wyniki bez timestampów; GHIDRA_LOCAL manifesty AT_COPY + FINAL (każdy manifest opisuje dokładnie stan, który pokrywa).

---

## 1. Odpowiedź na pytanie główne (jedno zdanie + status)

**Konkretna wartość pozycji/rotacji trafia do kontenera z KOMUNIKATU: kursor podkomunikatu (typy 0xB0/0xB9/0xC6/0xC7, dispatcher FUN_004B18D0) jest deserializowany (FUN_007453D0: klucz u32@+0, transforma, pozycja vec3 u32×3@+0x50..0x58, wariant bajt@+0x5C; read-cursory FUN_00752700/26 40), settery zapisują pozycję do rekordu placementu (FUN_00730F90: rekord+8/+0xC/+0x10 = XYZ), ctor klasy wartości kopiuje rekord do pól instancji (KLUCZ=rekord[0]→+0x74, POZYCJA=rekord+8..0x10→+0x44..0x4C, WARIANT→+8, ID-param-setu=rekord+0x20→+0x88), a INSERT (FUN_00856190) wstawia parę {klucz=rekord[0], wskaźnik instancji} do STLport hash_map@mgr+0x10 (węzeł {next, klucz@+4, wartość@+8}) — TEN SAM klucz (rekord[0]) jest więc kluczem węzła ORAZ kopią w polu instancji+0x74, co wiąże komunikat, rekord, węzeł i instancję; klasą wartości jest MovableObject/ClientMovableObject (RTTI), a NIE klasa parametrów.**

Status: **CONFIRMED (GB1-GB4, bajtowo)** z granicami §8 (upstream kursora, osie/jednostki pozycji, semantyka D@4508).

## 2. Zadanie 1 — KLASA WARTOŚCI MAPY: CONFIRMED (zamyka RECEIVER_UNRESOLVED #1 Fazie A)

(a) **Rzeczywiste wywołania resolvera FUN_008544D0 zwracające [hit+8] do kodu czytającego [value+0]** — census isCall = **dokładnie 4**:
- FUN_0085B840 (walker-init; 108 isCall — najszerszy konsumer): ctx[0] = wartość; czytelnicy [value+0]: selektor FUN_008553D0 (`(**(code **)(*(int *)*puVar7 + 0xc))` = slot3; `(**(code **)(*(int *)*puVar8 + 8))` = slot2; FUN_0085B860 lock [value+4]);
- FUN_004C47F0 ×2: `(**(code **)(*piVar4 + 0x14))` = **slot5 z f32** (pozycja/velocity setter);
- FUN_004C4A10: bez wirtualnego czytania [value+0] (przekazuje wartość do FUN_00792B20/FUN_0085AD50=LEA+0x88 → FUN_00719E30).
[+0]-vtable z żywego przykładu (statycznego — runtime zakazany): zapisy vtable w ctorach = 0x00A91E4C (MovableObject, pin C7 06 4C 1E A9 00 @0x0085B1C3) i 0x00A7DCB0 (ClientMovableObject, pin C7 06 B0 DC A7 00 @0x00528EA3); dwie pozostałe wartości imm32 0x00A91E4C w .text = destruktory (FUN_0085B3A0-base @0x0085B3AB, FUN_0085B7F0-deleting @0x0085B7FB — slot0).

(b) **Klasa wartości przez vtable→COL→RTTI (metoda TD Fazie A)**: vtable−4 = 0x00AB33D0 (COL) → COL+0xC = 0x00B7997C (TD) → TD+8 = `.?AVMovableObject@@` (bajty 2E 3F 41 56 4D 6F 76 61 62 6C 65 4F 62 6A 65 63 74 40 40). Pochodna: `.?AVClientMovableObject@@` (COL/TD zapisane w T2B). Ghidra niezależnie: `*param_1_00 = MovableObject::vftable` / `ClientMovableObject::vftable`.

(c) **Ctor i pola (FUN_0085B1B0, thiscall(this, rekord, wariant))**: +0 vtable; +4 nullable-lock(0); **+8 = wariant** (89 46 08); +0x14..0x3B transform 3×3+flaga (FUN_007345C0); +0x3C dziecko(0); **+0x44..0x4C = POZYCJA = [rekord+8/+0xC/+0x10]** (FUN_00746560=LEA EAX,[ECX+8]); +0x50..0x58 global vec3; +0x5C..0x70 = 2×vec3 z FUN_0040B070; **+0x74 = KLUCZ = [rekord+0]** (CALL FUN_004123D0=`MOV EAX,[ECX]; RET` z ECX=rekord); +0x78 = [rekord+4]; **+0x88/+0x8C = ID PARAM-SETU/pole2 = [rekord+0x20/+0x24]** (FUN_00746570=LEA+0x20; czytane przez FUN_0085AD50=`LEA EAX,[ECX+0x88]`); +0x98=1.0f; rozmiar ≥0xA0 (pochodna 0x128).
**Census callerów**: ctor MovableObject = 1 (FUN_00528E50); ctor ClientMovableObject = 1 (FUN_004C46C0) — jedyna droga wartości do mapy.

(d) **Unikalność vtable**: slot-0 (FUN_0085B7F0) — skan DWORD w WSZYSTKICH sekcjach: 1 trafienie = sama 0x00A91E4C (RTCI-chain walidowany); **vtable unikalna dla wartości** — brak innych typów ze wspólnym slot-0. Vtable pochodnej: 2 zapisy imm32 (ctor + dtor własny) — bez funkcji pośrednich.

## 3. Zadanie 2 — INSERT-SEAM: VA-locked (GB2)

(a) **Struktura managera (ctor FUN_008550C0, 0x8C B)**: hash_map @+0x10 (ctor FUN_00854C00 z **PUSH 0x64 = 100 bucketów** — pin 8D 4E 10 6A 64 @0x008550FE; **STLport hash_map, NIE rb-tree/hash-custom**: find=key%(n−1), _Stl_prime::_S_next_size w FUN_00856090, __node_alloc::allocate(0xC)); druga struktura wyzerowana +0x2C..+0x40 (rola niezdekodowana — NIE jest mapą insertu); **lock CS @+0x44** (new(0x20)+[0x00A75A38] InitializeCriticalSection; store 89 46 44); 12 floatów +0x58..+0x84. Kontraktowy hint „head@+0x30/+0x34/+0x38" = pola DRUGIEJ struktury (wyzerowane w ctorze), NIE header mapy (mapa@+0x10: buckets@mgr+0x18, end@mgr+0x1C, count@mgr+0x24, load-factor@mgr+0x28 — potwierdzone dekompilatami FUN_00856090/FUN_00854D90).
**INSERT**: nie jest wirtualny; funkcja find-or-create = FUN_00854D90 (generyczna, **18 isCall** — służy wielu mapom; kontrola odróżniająca: ten sam node-op używany przez FUN_00946AE0/FUN_005538F0 na INNYCH instancjach map), specyficzny wrapper mapy parametrów = **FUN_00856190** (1 isCall).

(b) **Jedyny realny writer mapy parametrów = FUN_004C46C0 → FUN_00856190**: 
```
FUN_00856190(mgr=this, wartość):
  [wartość+0x74]==0 → return 0                                  (83 7F 74 00)
  EnterCS(mgr+0x44)
  klucz = FUN_00414130(wartość) = [wartość+0x74] = rekord[0]      (8B CF; E8 7F DF BB FF; 89 44 24 0C)
  FUN_00856090(map, [mgr+0x24]+1) — rehash-if-needed             (load factor map+0x18)
  para{slotA=klucz, slotB=wskaźnik_wartości} na stosie           (89 7C 24 14)
  FUN_00854D90(map, out{node,flag}, &para)                        (E8 B5 EB FF FF)
    └─ FUN_00854260(&para): __node_alloc::allocate(0xC); node+4=para[0](klucz); node+8=para[1](WARTOŚĆ); next=0
  flag≠0 → sukces (return 1); flag==0 → klucz istniał: wartość->slot0(PUSH 1) = deleting dtor ZWOLNIENIA DUPLIKATU → return 0
```
(c) **Rozdzielenie pierwotne/propagacja**: insert pierwotny = FUN_004C46C0 (new+ctor+FUN_00856190); kopia/update istniejącej instancji = FUN_004C47F0 ścieżka „istnieje" (setery wirtualne FUN_0085B3E0/FUN_0085ADB0 na wartości). **FUN_00845F70 = writer-do-istniejącego-kontenera** (lock [this+4]+0x30 → FUN_005275E0(parent, klucz, &out) → unlock; **NIE woła insertu** — jego cel operuje na 0x0052xxxx rodzinie atrybutów). Wszystkie realne writery rozliczone: funnel insertu = FUN_00856190 (1 caller) ← FUN_004C46C0 (6 callerów: FUN_004C47F0, FUN_00456F40←FUN_00457930(8 callerów: builder FUN_00567770, FUN_00567170, FUN_005B5F90, FUN_00459270, FUN_00447630, FUN_00457C00, FUN_0067BC90, FUN_0067CCD0), FUN_0050BED0, FUN_00442190, FUN_00441910, FUN_004B3A00).
(d) Insert NIE jest wirtualny (E8 bezpośrednie) — brak slotu do rozstrzygania.
(c') **Reklasyfikacja kandydatów insertu Fazie A** (FUN_0085B3E0/FUN_0085B780/FUN_0085B7F0 — żaden nie jest insertem): FUN_0085B3E0 = metoda wartości (set-pozycji na ISTNIEJĄCEJ instancji — ścieżka update FUN_004C47F0); FUN_0085B780 = stepper licznika wariantu (@wartość+0xA0, limity 5/20, gated [mgr+8]==1; 1 caller @0x0048EAE9); FUN_0085B7F0 = deleting destructor (vtable slot-0).

## 4. Zadanie 3 — MODEL KLUCZY: per krawędź (GB3)

Pełna macierz: **02_ANALYSIS\KEY_MODEL_MATRIX.md** (E1-E18 + napędy A/B/C; każda krawędź PROVEN z VA+pinem). Kluczowe ustalenia:
1. **Klucz mapy = uchwyt instancji z komunikatu (rekord[0])**, NIE ID param-setu. ID param-setu (0x4E34/0x4E38/0x5DC9/0x38B0) = **ATRYBUT wartości** (+0x88, czytany FUN_0085AD50=LEA+0x88; CMP w selektorze/FUN_004C47F0). Korekta otwartego założenia Fazie A (tam: „key = param_1 selektora z rejestracji" — rejestracja FUN_00457930 rzeczywiście ZWRACA nowy klucz w EAX, ale jest to uchwyt, nie ID param-setu).
2. **Builder FUN_00567770 ma dokładnie 1 callera = driver FUN_00567C50; driver ma dokładnie 3 = napędy A/B/C** (FUN_0058DB50@0x0058E0B7, FUN_005B72C0@0x005B7567, FUN_00514EF0@0x00515345) — potwierdzenie struktur A/B/C z Fazie A bajtowo.
3. **Receiver gettera D w driverze (granica #2 Fazie A) ROZSTRZYGNIĘTA**: site'y @0x00567D16/0x00567D46: ECX = ESI = **arg3 drivera (rekord stanu; czyta [rekord+0x10])**; site @0x00567F72: ECX = [ESP+0x20] = EDI = **this (obiekt queue)**. Prolog drivera: EBP=arg1=KLUCZ (@0x00567C88), ESI=arg3, EBX=arg2, EDI=this (@0x00567CA8: 8B F9).
4. **Klucz vs [singleton 0x00BA1260+8]**: driver CMP EBP,EAX po getterA na [0x00BA1260] (pin @0x00567CC4: 8B C8 E8 15 65 26 00; 3B E8) — klucz porównywany z flagą/ID singletonu (hipoteza: własny klucz awatara — granica §8).
5. imm32 na krawędziach (wykaz w macierzy §3): 0x4E34/0x4E38/0x5DC9/0x38B0 (param-sety), 0x1BDC (pole rekordu buildera), 0x1BDE, 0xE10, 0x175, 0x1B2B, 0x3DC8, 0x92E, 0xDD0, 0x23A, 0x3F1, 0x3F5, 0x3BDB, 0x39/0x42.
6. Poziomy wskaźników rozdzielone (macierz §0): klucz→bucket→węzeł(hit)→[hit+8]=wartość→pola.

## 5. Zadanie 4 — ŹRÓDŁO DANYCH INSERTÓW: KOMUNIKATY (GB4)

(a) **NEGATYW dla ścieżki VFS→mapa-parametrów**: parsery VFS NIE zasilają mapy parametrów. Funnel insertu (FUN_00856190←FUN_004C46C0←6 callerów) — żaden caller w rodzinach parserów (FUN_00730C90 ma 1 callera = FUN_0072FA30 = builder rejestru definicji; FUN_0094BD30/FUN_0094F350 — 2+2 callerów w rodzinie 0x0094xxxx, bez krawędzi do funnelu). VFS→rejestr definicji = KONTROLA POZYTYWNA Fazie A, re-weryfikowana (patrz (c)).
(b) **POZYTYW: komunikaty**. Dispatcher **FUN_004B18D0(typ_komunikatu, kursor)** — case 0xB9 → FUN_005B72C0 @0x004B1A16 (pin E8 A5 58 10 00), case 0xB0 → FUN_004574F0, 0xC6 → FUN_004B0AB0, 0xC7 → FUN_004B1670, 0xBC → advance(4)+FUN_00458030. Read-cursor ops (z kontraktu „FUN_00752700/40/26 40"): **FUN_00752700(kursor→u32,u32,u8,u8)** i **FUN_00752640(kursor→u32,u32,u8)** — każdy odczyt: bounds-check ([kursor+8]<[kursor+0xC]+n), zapis z flagą fail-closed @kursor+0x11, advance FUN_0040DE60(n). Handler 0xB9: subtyp (FUN_007527F0) → read-cursor → {KEY,KEY2,bajty} → walker(KEY/KEY2) → distance-gate (FUN_004b2a20 vs FUN_0085aff0×[0x00A79E28]) → FUN_005B6890(KEY, 0x42/0x39, payload) / FUN_005B6370→FUN_005B5F90 → **driver(KEY)**. Processor placementu FUN_004C47F0: **FUN_007453D0(rekord, kursor)** — deserializata: **rekord+0=KLUCZ u32; +0x34=u16; +0x50/+0x54/+0x58=POZYCJA vec3; +0x5C=WARIANT bajt** (+sub-struktury transformu) — klucz i pozycja przybywają RAZEM w jednym rekordzie z kursora.
(c) **Rozdzielenie pierwotne/propagacja**: pierwotne źródło danych INSTANCJI (klucz+pozycja+wariant) = komunikat; DEFINICJE (A=NIF id itd.) = pliki VFS przez rejestr (FUN_00452490→FUN_0072FA30: string **"Parameters\templates.vfs"** → FUN_00972DF0 ArkVFS01/02 (CreateFile/ReadFile/magic, wersja@+0xA0) → pętla: FUN_00730C90(kursor→5×u32; pin 89 47 08 @0x00730CE6=rekord+8=A) → FUN_00730700(ctor) → FUN_0072F8D0(insert do RB-rejestru); odczyt definicji = FUN_0043A550/FUN_0072F580 (rb-find, rekord@hit+0x14; konsumenci: FUN_00567170 def-id **0x3BDB**, FUN_005B5F90 def-id=param_1). Krawędź komunikat→insert = PROVEN; krawędź VFS→rejestr→def-id→rekord placementu = PROVEN; granica: upstream bajtów kursora (kolejka sieciowa vs lokalna) NIE prześledzony (§8).

## 6. Zadanie 5 — PARSER VFS: NOT_APPLICABLE (decyzja po dowodzie z zad. 4)

Ślad insertu prowadzi do KOMUNIKATÓW (dowód czytnika §5b), NIE do Parameters VFS — warunek zadania 5 („jeśli ślad wskazuje Parameters VFS") **NIE spełniony**. GB5 = NOT_APPLICABLE. Weryfikacja pozytywna szwu VFS wykonana w ramach zad. 4c (kontrola Fazie A odtworzona: string→reader→record→registry), BEZ dekodowania nowej rodziny plików. Skan kluczy 0x6A4-rodziny w payloadach niewykonany (brak spustu semantycznego; klucze mapy ustalone z kodu, nie z plików).

## 7. Zadanie 6 — KANDYDACI RUNDA-1 (F4)

| Kandydat | Def-id → rekord → instancja | Wiązanie tym samym kluczem? | Status |
|---|---|---|---|
| **FUN_00567170** | def-id = imm32 **0x3BDB** → FUN_0043A550 → FUN_0072F580 (RB-rejestr, rekord@hit+0x14) → FUN_005670a0 → settery: f60; **f90(param_3) = pozycja z ARGUMENTU**; fb0(FUN_0096C630(&x, param_4)) → rekord → **FUN_00457930** → nowy klucz (EAX) → FUN_0050a690(klucz) | NIE — klucz definicji (0x3BDB, rejestr VFS) ≠ klucz instancji (nowy, z rekordu) | PROVEN (def→rekord→instancja przez jawne transfery pól; bez sąsiedztwa adresów) |
| **FUN_005B5F90** | def-id = **param_1 (argument)** → FUN_0043A550 → FUN_0072F580 → settery (**f90(param_4) = pozycja z argumentu**) → FUN_00457930 → nowy klucz → FUN_00567030(cb, uVar2, klucz, 0); 3 isCall — wszystkie w FUN_005B6370 (wywoływanym z handlera 0xB9, gałąź 0x39) | NIE — j.w. | PROVEN |
| **FUN_006CB6F0** | (param_1=klucz) → **FUN_00971780** (hash-find po kluczu w INNEJ mapie — this z kontekstu) → FUN_006CB370 → FUN_006C9700 → **FUN_006FA8B0** (ctor ArkModelResourceInstanceRef — macierz Fazie A wiersz 5) → FUN_006CB020/FUN_006F33A0 | Częściowo — klucz param_1 szuka w mapie model-instancji; wartość=rekord→AMRIR(item@+8) | PROVEN do granicy: tożsamość mapy (this) i dalsze pola NIE zdekodowane (poza szwem param-map; FAMILY_UNRESOLVED z granicą) |

Wniosek F4: kandydatom BRAK wspólnego klucza def↔instancja — wiązanie zachodzi przez **jawny transfer pól rekordu** (0x2C) z definicji do rekordu placementu (FUN_004148F0/FUN_00730FD0) i dopiero potem powstaje nowy klucz instancji. Pozycje 4508/296445 pozostają NIEODZYSKANE (żadna z tych ścieżek nie odczytuje D@+0x10 template'u jako pozycji — D@4508=124.941 pozostaje ANCHORS_ABSENT_SEMANTICS_OPEN, a value+0x44 pochodzi z komunikatu, nie z definicji).

## 8. Zadanie 7 — TRANSFORM SEMANTICS DISCIPLINE

Rozdział przestrzeni: **value+0x44..0x4C = f32 vec3 = POZYCJA** — konsument i kompozycja potwierdzone (selektor: `slot3_result[i] + wartość+0x44/0x48/0x4C`; setter f90; dispatch FUN_00415570/FUN_008599A0), ale **przestrzeń (model-local/parent-local/world) i jednostki NIEUSTALONE** — wymaga dekodu slot3 (FUN_0085B6A0) i FUN_008599A0. Rotacja: transform 3×3 @+0x14 (+flaga word @+0x24) — NIE zdekodowana osiowo. **Dla 4508/296445 nie utworzono żadnego przykładowego XYZ** — żadna wartość w tym runie nie została ogłoszona jako „odzyskana lokalizacja historyczna". Wszystkie wektorowe wartości = hipotezy do czasu konsumenta+reguły kompozycji (konsument pozycji jest, reguła kompozycji częściowa — granica jawna).

## 9. Kontrole (obowiązkowe)

- **Kontrola pozytywna** (wzorzec Fazie A): łańcuch rekordu templates.vfs odtworzony: FUN_0072FA30 ("Parameters\templates.vfs" → FUN_00972DF0 @0x0072FAF1 → FUN_00730C90 @0x0072FBA5 z pinem `89 47 08` @0x00730CE6 → FUN_0072F8D0 insert; odbiór FUN_0072F580→FUN_006C3F50 getter @0x006C3F74) — RE-WERYFIKACJA WŁASNA (dekompilaty GH1/GH3 + piny T6).
- **Kontrola odróżniająca**: (1) ten sam node-op FUN_00854D90 (find-or-create) używany przez 18 różnych call-site'ów na RÓŻNYCH mapach (param-map przez FUN_00856190 vs FUN_00946AE0/FUN_005538F0 na własnych this) — generyczność vs specyficzność rozróżniona; (2) getter +8 (FUN_007CE1E0) na 2 typach odbiorców w tym runie: wartość mapy (wariant) vs singleton 0x00BA1260 (flaga porównana z kluczem) — ten sam offset, różne role (macierz Fazie A rozszerzona o wiersz „wartość mapy=MovableObject" z RTTI).
- **Drugi rzeczywisty przypadek**: (a) read-cursor ops — FUN_00752700 i FUN_00752640 (oba fail-closed per pole); (b) zapis vtable — 2 ctory (MovableObject/ClientMovableObject); (c) setter f90 — builder FUN_00567770 i processor FUN_004C47F0 (różne źródła pozycji, ten sam zapis rekord+8..0x10); (d) dispatch komunikatów — 0xB9 (klucz z read-cursor) i 0xB0/0xC6/0xC7 (kursor → processor placementu).
- **Censusy z pełnymi listami VA**: 01_RAW\GH1/GH2/GH3_DECOMP_CENSUS.json (isCall, autoritative Ghidra) + T2/T2B/T2C/T4 (raw E8/E9 — rozbieżności E9-tail-jump wyjaśnione jak w Fazie A), T1_VALUE_CLASS.json (slot-0 census), T4_HANDLER_DISPATCH.json (imm32 handlerów).
- **Granice ciał**: heurystyka 3×CC zlała FUN_004C46C0/FUN_004C47F0 (brak paddingu @0x004C47E9) — wychwycone i skorygowane Ghidra-atribucją (funkcje: 0x004C46C0-0x004C47E8 C3 / 0x004C47F0-0x004C4A04 RET 4).

## 10. Bramki (fail-closed) — 06_REPORT\STAGE_ACCEPTANCE_GATES.csv

- **GB1-VALUE-CLASS: PASS** — RTTI+vtable+ctor+caller census (§2).
- **GB2-INSERT-SEAM: PASS** — FUN_00856190 VA-locked (klucz=[wartość+0x74]=rekord[0], wartość=nowy obiekt; para→węzeł; deleting-dtor przy duplikacie); FUN_00845F70=writer-nie-creator; funnel 1+6 callerów rozliczony (§3).
- **GB3-KEY-MODEL: PASS** — E1-E18 + napędy A/B/C per krawędź PROVEN (macierz; §4).
- **GB4-DATA-SOURCE: PASS** — krawędź komunikat→insert prześledzona bajtowo (dispatcher+read-cursor+deserializat); VFS=negatyw dla mapy (bounded census); rozdział pierwotne/propagacja (§5).
- **GB5-PARSER: NOT_APPLICABLE** — warunek (ślad→Parameters VFS) nie spełniony po dowodzie zad. 4 (§6).
- **GB6-IMMUTABLE: PASS** — census 8 pakietów historycznych przed/po identyczne (01_RAW\GB6_IMMUTABLE_CENSUS_{before,after}.json; porównanie w 03_EVIDENCE poniżej — w tym pakiet A).
- **GB7-ERA: PASS** — S0 fail-closed obu SHA.

## 11. SELF_CHECK (własny; NIE audyt PE-MASTER)

- S0: oba SHA zgodne (skrypt własny, fail-closed, 01_RAW) ✓; AUDIT_OUTPUT_ROOT nieistniał ✓; kopia GHIDRA_LOCAL zgodna bajtowo z manifestem finalnym pakietu A (AT_COPY manifest) ✓.
- Pełne raw censusy: resolver=4 isCall (Ghidra) vs 4 raw E8 ✓; ctor wartości 1/1; ctor pochodnej 1/1; insert 1/1; builder 1 isCall vs 1 raw; driver 3/3; walker-init 108 isCall vs 108 raw ✓; getter mgr 104 isCall vs 104 raw ✓ (Fazie A: „71 funkcji" = funkcje, nie site'y — census site'ów 104).
- Bramki: wszystkie ocenione fail-closed z MEASURED_QUANTITY + INDEPENDENT_SOURCE + WHY_NON_CIRCULAR + FAILURE_CASE_DETECTED (CSV) ✓.
- Negatywy: VFS→param-map (bounded census funnelu — 0 krawędzi) ✓; koincydencje imm32 odrzucone przez kontekst pinów ✓; raw-E8 vs isCall rozbieżności wyjaśnione (E9 tail-jumpy) ✓.
- Determinizm: SCRIPT_SHA256.csv (hash po ostatniej edycji, przed uruchomieniem; weryfikacja końcowa poniżej); brak timestampów w JSON ✓; manifesty GHIDRA_LOCAL AT_COPY + FINAL rozdzielone (nie powtórzono błędu stale-manifest) ✓.
- Zakres: bez operacji git; bez dotykania experiments/, src/game/, oryginałów, pakietów historycznych (GB6 przed/po); bez sub-agentów; STATIC-ONLY ✓; każdy proces Ghidra headless zakończony („Save succeeded", EXIT=0, brak zostawionych procesów) ✓.
- **NIE ogłoszono STATIC_INSTANCE_MECHANISM_CONFIRMED ani źródła placementu historycznego; pozycje 296445 NIEODZYSKANE.**

## 12. Struktura pakietu

```
00_CONTROL\  pe_core.py (kopia z PKG_A), s0_era_assertion.py, gb6_immutable.py, ghidra_manifest.py,
             t1_value_class.py, t2_insert_seam.py (+t2_extract), t2b_derived_insert_hunt.py (+t2b_extract),
             t2c_insert_helper.py (+t2c_extract), t2d_node_alloc.py, t4_handler_dispatch.py,
             t4b_dispatcher_context.py, t6_pinbytes.py, gh1/gh2/gh3_decomp.py (Ghidra postScripts),
             SCRIPT_SHA256.csv, GHIDRA_LOCAL\ (+ manifesty AT_COPY/FINAL)
01_RAW\      S0_ERA_ASSERTION.json, T1_VALUE_CLASS.json, T1_REGION_*.txt, T2_INSERT_SEAM.json,
             T2_HEX\*, T2B_*, T2C_*, T2D_*, T3_DRIVER_DSITES_RAW.txt, T4_HANDLER_DISPATCH.json,
             T4B_DISPATCHER_CONTEXT.json, T6_BYTE_PINS.json, DECOMP\F*.c (112 plików unikalnych),
             GH1/GH2/GH3_DECOMP_CENSUS.json, GB6_IMMUTABLE_CENSUS_{before,after}.json,
             GB6_IMMUTABLE_COMPARISON.json, SELF_CHECK.json
02_ANALYSIS\ SEAM_FLOW_MAP.md, KEY_MODEL_MATRIX.md
06_REPORT\   RESEARCH_FINDINGS.md (ten plik), STAGE_ACCEPTANCE_GATES.csv
```

Finalny REPORT/HANDOFF sformalizuje pe-master-auditor (ten plik = raport roboczy executora).
