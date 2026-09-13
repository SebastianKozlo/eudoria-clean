# RECEIVER MATRIX — typy odbiorców wspólnego gettera FUN_007CE1E0 (MOV EAX,[ECX+8]; RET)

RUN: PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913 | ERA: EU 9.3.5 (pcg_install)
Binarium: Entropia.exe SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
Wszystkie VA → własne mapowanie (pe_core.PE, sekcje z S0_ERA_ASSERTION.json); każdy bajt cytowany odczytany z pliku.

## 1. Dlaczego getter ma wiele typów odbiorców

`FUN_007CE1E0` @0x007CE1E0 = 4 bajty `8B 41 08 C3` (MOV EAX,[ECX+8]; RET) — odczytuje pole
**+8 dowolnego obiektu podanego w ECX**. Własny census bezpośrednich CALL rel32 → 0x007CE1E0:
**808 site'ów** (raw E8-scan; niezależnie zgodny z liczbą „kandydatów" audytu Desktop).
Census nie jest dowodem jednorodności odbiorców — provenance ECX decyduje o typie.
Poniższa macierz rozróżnia typy metodą RTTI/vtable + dataflow callera (kontrola odróżniająca).

## 2. Macierz (GA3)

| # | Typ odbiorcy | Pochodzenie odbiorcy (dowód bajtowy) | Layout +8 | Inne pola | Kto czyta +8 (getter, VA) | Rzeczywista rola | Artefakty |
|---|---|---|---|---|---|---|---|
| 1 | **Rekord templates.vfs** (kontrola pozytywna) | rejestr RB-tree (DAT_00BA1824-family); lookup `FUN_0072F580` (rb-find `FUN_004D1430`; **rekord@hit+0x14**, miss→0x00BA5800); bezpośrednio: `FUN_006C3F50`: `MOV ECX,EDI(rekord)` po CALL lookup @0x006C3F62; slot-gettery `FUN_006C2840/70` (C×2 → tabela 0x00A858B4 → FUN_0043A550 → lookup) | **+8 = A (u32, id pliku .nif)** — parser zapis: `89 47 08` MOV [EDI+8],EAX @0x00730CE6 | B@+4, C@+0xC, D_f32@+0x10 (payload@+0x10 = file+0x20) | FUN_006C3F50@0x006C3F74; FUN_006B4C50@0x006B4C82/0x006B4C93 | **id modelu NIF** (join A→`<A>.nif` 3618/3618 — RUN1, re-walidacja ROUND) | F1_CTX5_*.txt; F1_POSCONTROL.json; F1_BODYSET_CALLMAP.json |
| 2 | **ArkObjectClass** (F1) | perklasowe lazy-init singletony: `DAT_00BA58CC` = ArkObjectClassImpl<ArkSurgeonObject,**20035**> (writer FUN_0073D810: new(0x118)→ctor FUN_0073AB60→store @0x0073D882); `DAT_00BA5D9C` = ArkObjectClassImpl<ArkParameterContainer,**20030**> (writer FUN_0073CF50); fabryka ArkObjectClass vtable **0x00A86850** slot0=dtor 0x0073F230, **slot1=fabryka 0x0070BF50**; RTTI: vtable−4→COL 0x00AA7F28→TD 0x00B8D068 `.?AVArkObjectClass@@`; vft-write `C7 06 50 68 A8 00` @0x0070CFB6 | **+8 = numeryczne ID klasy (param-set)** — ctor `MOV [ESI+8],EBP` @0x0070CFC1 (EBP = arg1); 55 rejestracji woła ctor z imm32: 0x4E20..0x4E4B, 0x5DCx-family (pełna lista w F1_REG_ARGS.json) | +0xC struktura (bajt@+0xC = low byte arg1), CS@+0x24, CS@+0x5C, string@+0xA0 | **ctor ArkObject `FUN_00726E70` @0x00726EB7** (ECX = arg1 = klasa) | **identyfikator klasy** (np. 20035 Surgeon; 20030 Container; 20006 — klasa istnieje mimo braku pliku 20006.vfs) | F1_ABI_BYTES.json; F1_CENSUS.json; F1_REG_ARGS.json; F1_CTX_WRITER_DAT00BA58CC.txt |
| 3 | **ArkObject** (F1 — obiekt docelowy) | fabryka `FUN_0070BF50` (slot1 vtable 0x00A86850): MOV ESI,ECX; PUSH 0x58; CALL new @0x0095D3C4; **PUSH ctor-arg; PUSH ESI (klasa = PIERWSZY arg)**; MOV ECX,EAX; CALL ctor @0x0070BF96; RTTI vft 0x00A86B48 = `.?AVArkObject@@` (COL 0x00AA8008, TD 0x00B8CFBC) | **+8 = zagnieżdżona struktura (InitializeCriticalSection @+8** przez FUN_004134F0: PUSH ESI→CALL [0x00A75068]; magic 0x1FE319BA @+0x24) — NIE dane liczbowe | +4 = ptr klasy, **+0x28 = [class+8] = class-ID** (store `89 46 28` @0x00726EBC, wartość z gettera @0x00726EB7), +0x2C = arg2 fabryki, +0x30..+0x54 = 0 | getter NIE jest wołany na ArkObject w ctorze (na klasie) — macierzowa rola: **odbiorca końcowy wartości** | encja świata; jej +0x28 = **kopia numerycznego ID klasy** (nie „A rekordu") | F1_HEX_CTOR_ARKOBJECT_00726E70.txt; F1_HEX_FACTORY_0070BF50.txt |
| 4 | **Wartość mapy managera parametrów** (F2 — odbiorca węzła atrybutu) | walker `FUN_0085B840`(walker, key): singleton `FUN_004154F0`→[0x00BA12E8] (0x8C); `[walker+0] = FUN_008544D0(mgr,key)` = **[hit+8] mapy mgr+0x10** (rb-find FUN_00971780, lock mgr+0x44); `FUN_0085B860`: *out=[walker+0]; gałąź 0x4E38: LEA EDX,[ESP+0x38]; PUSH EDX; LEA ECX,[ESP+0x1C]; CALL @0x008557F1; **MOV ECX,[EAX] @0x008557F6**; CALL getter @0x008557FD | **+8 = small int (typ/wariant; selektor mapuje 4/5→2, 6→3, 7→4)** | +0 = vtable (wywołanie wirtualne slot3 w gałęzi 0x38B0: `CALL [vft+0xC]`), +4 = nullable CS-ptr (FUN_0085B190: if [v+4]≠0→FUN_00413440), +0x44..+0x4C f32, +0x5C..+0x64 dword, +0x10 czytane getterem D w INNEJ gałęzi @0x008556DF | FUN_008553D0 @0x008557FD | **znacznik wariantu konstruktora** („konstruktor-walker"); NAZWA KLASY: **RECEIVER_UNRESOLVED** — patrz §4 | F2_CTX_BRANCH_008557C0.txt; F2_CTX_WALKER_*.txt; F2_SELECTOR.json; F2_CALLMAP.json |
| 5 | **ArkModelResourceInstanceRef** (instancja modelu) | ctor `FUN_006FA8B0`: `MOV [EAX],0x00A864B8` (vft; w body @+0xC wg poprawki P3-2 RUN3), `MOV [EAX+4],0` (licznik), `MOV [EAX+8],ECX` (**item@+8**), RET 4 (RUN3 E.3; re-odczyt tej samej ery potwierdza bajty przy VA) | **+8 = item (ptr na element zasobu)** | licznik refcount@+4, vft 0x00A864B8 (baza 0x00A864B0) | bezpośredni getter-call z tym odbiorcą: **NIE WYKAZANY w tym runie** (kandydaci: podsystem 0x006Fxxxx — poza zakresem) | kontener referencji instancji modelu | layout z RUN3 re-zweryfikowany; brak nowego dowodu użycia gettera |
| 6 | **Singletony systemowe** (uzupełniający) | `FUN_004143F0`→[0x00BA1260] (0x4C); `FUN_004154F0`→[0x00BA12E8] (0x8C); `FUN_00415570`→[0x00BA12EC] (0xCC) — lazy-init singleton-gettery (wzorzec: MOV EAX,[global]; TEST; JNZ ret; PUSH size; CALL new...) | +8 = pole flagi/identyfikatora (używane w porównaniach gate) | rozmiary 0x4C/0x8C/0xCC; mapa mgr+0x10, CS mgr+0x44 | **FUN_00567B40 (queue-push) @getter po CALL FUN_004143F0 @0x00567B50** (MOV ECX,EAX; CALL getter @0x00567B50-55) | porównanie [singleton+8] vs FUN_00844130(arg) → flaga 5. argumentu FUN_00567170 (decompile ZS2_PSEUDO_00567B40: iVar2=FUN_007ce1e0(); SETE) | rola +8: **UNKNOWN** (kandydat: level/typ singletonu) | F2_DCLAIMS.json; ZS2_PSEUDO_00567B40.txt (RUN4, odczyt) |
| 7 | **Rekord placementu na stosie** (uzupełniający; kontrast D) | lokalne rekordy w funkcjach drivera, np. FUN_00468910: `LEA ECX,[ESP+0x1C]` @0x00468D84 → CALL getter-D @0x00468D88; builder FUN_00567770: rekord @ESP+0xB4 (E.2 RUN3) | **+8 = position.X (f32, vec3 @+0x08/+0x0C/+0x10)** — settery FUN_00730f90/fb0/fd0 (RUN3 QC A6) | rotacja @+0x14..+0x1C, +0x20/+0x24; init f60 (12 dwordów, FLDZ→+0x10) | getter-D (+0x10 = position.Z!) @0x00468D88 i 11 dalszych w FUN_00468910 | **rekord runtime placementu** — odczyty +0x10 na tym typie to Z-koordynata, nie D template'u | F2_DCLAIMS.json |

## 3. Kontrola odróżniająca (rozróżnialność metodą)

Metoda (RTTI/vtable odbiorcy + dataflow ECX callera) ROZRÓŻNIA wiersze 1–4:
- wiersz 1: ECX z lookupu rejestru (hit+0x14); brak vtable (layout 28-B rekordu, parser @0x00730CE6);
- wiersz 2: ECX = obiekt z RTTI `.?AVArkObjectClass@@` (vtable-4→COL→TD), arg1 ctorów per-klasa = imm32 param-set;
- wiersz 3: obiekt now(0x58) z vft 0x00A86B48 (RTTI `.?AVArkObject@@`), +8 zainicjowane CS-init (nie liczba);
- wiersz 4: ECX = [hit+8] mapy managera (vtable@+0 — wywołania wirtualne; +4 nullable lock; +8 small int).
Kontrola pozytywna (wiersz 1) odtworzona własnym dekodem: parser→rejestr→lookup→getter→pump
(F1_CTX5_PARSER_A_READ_00730CE6.txt: `89 47 08` @0x00730CE6; FUN_006C3F50 lookup @0x006C3F62 → getter @0x006C3F74).

## 4. Granice RECEIVER_UNRESOLVED

**Wiersz 4 (wartość mapy managera):** dataflow dokładny (key = param_1 FUN_008553D0; wartość = [hit+8]
mapy mgr+0x10; odczyt +8 przez wspólny getter), ale NAZWA KLASY wartości nierozstrzygnięta statycznie
w tym runie: eliminacje — (a) to NIE rekord templates.vfs (wartość jest polimorficzna — wywołanie
wirtualne przez [vft+0xC]; rekordy nie mają vtable); (b) to NIE klasa pochodna ArkObject/ArkParameter*
(rodzina ArkParameter*: Container 0x00A8784C, Transformation 0x00A877DC, SetObject 0x00A87260, Common
0x00A86F2C, ServerGlobal/Local, Creature, Action, Blueprint, Tool, Makeup — wszystkie ctor-y wołają
base-ctor FUN_00726E70 z globalnym wskaźnikiem klasy, co daje +4 = ptr klasy (nie-null) i
+8 = początek zagnieżdżonego CRITICAL_SECTION — sprzeczne z użyciem +4 jako nullable-lock i +8 jako
small-int); (c) to NIE ArkObjectClass (+8 = 20000-family ID ≠ 4..7).
**Co trzeba, żeby rozstrzygnąć:** (1) znaleźć punkt INSERT do mapy mgr+0x10 (kto wstawia wartości pod
kluczami param-setów — szew „parser→insert-map", otwarty kandydat nr 2 z RUN4 §9; kandydaci censusu:
FUN_0085B3E0/0085B780/0085B7F0 i 71 funkcji wywołujących singleton-getter), lub (2) ctor wartości
(zapis vtable + +8 = small int), lub (3) runtime (zakazane w tej rundzie).

## 5. Wnioski dla twierdzeń nośnych

1. **Getter FUN_007CE1E0 nie ma jednej semantyki** — odczyt +8 różnorodnych odbiorców: id modelu (rekord),
   ID klasy (ArkObjectClass), wariant konstruktora (wartość mapy parametrów), flaga (singletony),
   X-pozycja (rekord placementu ma +8 = position.X — ten sam offset, inna rola).
2. Most RUN3 „templates.vfs.A → ArkObject+0x28" jest **BŁĘDNY w obu ogniwach**: odbiorca gettera w ctorze
   ArkObject to ArkObjectClass (nie rekord), a wartość to numeryczne ID klasy (nie A=NIF-id).
3. Selektor wariantów w gałęzi 0x4E38 czyta **+8 wartości mapy parametrów**, nie D@+0x10 template'u
   (RUN4 Z4 §2–3 — patrz DRAFT_ERRATA_SUPERSESSION.md, F2).
