# QC_REPORT — INTERNAL_QC (niezależny, świeży kontekst, własne próby bajtowe)
## RUN: PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913 | Auditor: pe-master-auditor | FAZA 1

**Werdykt: QC_PASS** (0×P0, 0×P1, 2×P2 + 4×P3 — klasa dokumentacyjna; poprawki
sformalizowane w ERRATA_R4 + finalnym REPORT.md; evidence 01_RAW/02_ANALYSIS
executora NIETYKANE; RESEARCH_FINDINGS.md zachowany verbatim per zlecenie).

**Metoda (własna, niezależna):** własny parser PE (00_CONTROL\qc_probe\qc_pe.py —
nie kopia pe_core), własne censusy E8/E9 po surowych bajtach .text
(qc_census.py), własny dekod switcha dispatcherа (qc_dispatcher.py), własne
dekodowania x86 ogniw łańcucha z hexdumpów, własne łańcuchy RTTI, własny repeat
GB6 (qc_gb6_repeat.py + qc_gb6_perfile.py), hashe evidence przed/po
(qc_hash_evidence.py → QC_HASH_before/after.json). Binarium własny odczyt:
SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 ✓,
base 0x00400000, ASLR OFF, 5 sekcji zgodnie z S0_ERA_ASSERTION.json ✓.
templates.vfs BE57818C...B77 ✓ (S0). Kopia Ghidra executora NIETYKANA (manifesty
AT_COPY/FINAL zgodne; GHIDRA_LOCAL lokalnie). ZERO runtime/sieci/mock/Frida.

---

## 1. Zweryfikowane ogniwa łańcucha (własne bajty; CONFIRMED)

**(a) Dispatcher FUN_004B18D0** — `MOV EAX,[ESP+4]; ADD EAX,-0xA2 (05 5E FF FF
FF); CMP EAX,0x25; JA default; MOVZX EAX,BYTE [EAX+0x004B1B3C]; JMP
[EAX*4+0x004B1AE4]` @0x004B18D0-0x004B18EF. Byte-table 0x004B1B3C: 0xB0→8,
0xB9→0x0C, 0xC6→19, 0xC7→20, **0xB2→21 (=DEFAULT-pusty)**. Jump-table
0x004B1AE4 (22 wpisy) własny odczyt: [8]=0x004B1981 (case 0xB0:
`CALL FUN_004148F0 @0x004B1981; MOV EAX,[ESP+0x10]; PUSH EAX; CALL
FUN_004574F0 @0x004B198B`), [12]=0x004B1A11 (case 0xB9: `MOV EDX,[ESP+0x10];
PUSH EDX; **E8 A5 58 10 00 @0x004B1A16** → FUN_005B72C0 — pin executora
DOKŁADNY), [19]=0x004B1AB3 (0xC6→CALL @0x004B1AC1), [20]=0x004B1ACB
(0xC7→CALL @0x004B1AD9). ✓✓

**(b) Kursor — konwencja adresowania (własny dekod FUN_0040DE60):**
`[kursor+0]=data; [kursor+8]=size; [kursor+0xC]=offset; [kursor+0x11]=flaga`;
odczyt = data+offset; granica: `size < offset+n → flaga=0 + pole=0`
(fail-closed); advance FUN_0040DE60(kursor,n): `offset+=n; size<offset →
flaga=0` ✓. Czytniki FUN_00752700 {u32,u32,u8,u8} / FUN_00752640
{u32,u32,u8} / FUN_007527F0 {u16} — każdy odczyt z bounds-check + advance ✓.

**(c) Deserializator FUN_007453D0 — dokładne VA operacji odczytu (własny dekod):**
- KLUCZ u32: read `MOV EAX,[EAX+EDX]` **@0x007453EF** → `[rec+0]` @0x007453F6;
  advance @0x007453F8 (z TOP-kursora);
- para 2×u32 (FUN_004124B0 @0x0074540F): `[rec+4]`=param-set ID (CMP 0x4E34/
  0x4E38/0x5DC9 @0x004C4989 w processorze) + `[rec+8]` (z TOP-kursora);
- sub-kursor: FUN_007343E0 @0x00745419 (u16-header sub-pakietu → zagnieżdżony
  kursor @rec+0xC);
- WARIANT u16: read `MOV AX,[ECX+EAX]` **@0x00745435** → `[rec+0x34]`
  @0x0074543D (z SUB-kursora);
- POZYCJA vec3 3×dword (FUN_00412430 @0x0074545A, 12 B, advance 12) →
  **`[rec+0x38..0x43]`** — TO pole (nie +0x50..0x58!) zasilu f90 (z SUB-kursora);
- ROTacja vec3 3×dword (FUN_00412430 @0x00745465) → `[rec+0x44..0x4F]` → fb0;
- wektor drugi: X u32 read **@0x0074547C** → `[rec+0x50]`; Y u32 read
  **@0x007454AA** → `[rec+0x54]`; Z **f32** (FLD `D9 04 10` @0x007454D9 / FSTP
  `D9 5F 58` @0x007454E1) → `[rec+0x58]` (z SUB-kursora);
- bajt końcowy u8: read `MOVZX EAX,BYTE [EAX+EDX]` **@0x00745508** →
  `[rec+0x5C]` @0x00745510 (z SUB-kursora).

**(d) Processor FUN_004C47F0 (własny dekod pełnej ramki; record base
[ESP+0x10], placement record = record+0x60 = [ESP+0x70], 0x2C B):** init
FUN_00745360 @0x004C4822; deserialize FUN_007453D0 @0x004C483D; resolver
(klucz=[rec+0]) @0x004C484E-0x004C485F; ścieżka MISS: f60 @0x004C48D8
(LEA ECX,[ESP+0x70]); **FUN_00853A50(placement, KLUCZ) @0x004C48E6 →
`[placement+0]=KLUCZ`** (FUN_00853A50 = `MOV EAX,[ESP+4]; MOV [ECX],EAX; RET 4`);
**f90(placement, &[rec+0x38]) @0x004C48F4** → `[placement+8/+0xC/+0x10]=vec3#1`
(FUN_00730F90 = `[this+8]=p[0]; [this+0xC]=p[1]; [this+0x10]=p[2]` ✓);
fb0(placement, &[rec+0x44]) @0x004C4902; fd0(placement, &[rec+4]) @0x004C4910 →
`[placement+0x20]=param-setID; [+0x24]=field2` (FUN_00730FD0 ✓);
FUN_00797280(placement, X2=[rec+0x50]) @0x004C491E → `[placement+4]=X2`;
FUN_004C4640 @0x004C4930 (ignoruje argumenty — zwraca singleton
`[0x00BA26B8]`, new(0x1C)+FUN_00766480); FUN_00765930 @0*0x004C4937 (na
resztkach stosu str/X2; zwraca wskaźnik stringa); **create
FUN_004C46C0(placement, MOVZX u16=[rec+0x34] @0x004C493C, str, 1) @0x004C4952**;
ścieżka EXISTING: slot5 wartości z f32=[rec+0x58] (`FLD [ESP+0x68]` @0x004C4864,
CALL slot @0x004C4871), FUN_0085B750, **FUN_0085B3E0(istniejąca_wartość,
&[rec+0x38], 1) @0x004C4875** (set-pozycji na istniejącej instancji — ZGODNE z
f90: to samo źródło!), FUN_0085ADB0(&[rec+0x44]). Y2=[rec+0x54] i
bajt=[rec+0x5C]: przeczytane, ale NIE konsumowane przez FUN_004C47F0 (skan
pełnej funkcji: zero odwołań [ESP+0x64]/[ESP+0x6C]).

**(e) Creator FUN_004C46C0 (własny dekod):** kopia rekordu na stos; new(0x128)
`PUSH 0x128 @0x004C4792`; ctor FUN_00528E50(this, kopia, u16-wariant, arg3,
arg4) @0x004C47C1; insert FUN_00856190(mgr, wartość) @0x004C47DA (pin `8B C8
E8 B1 19 39 00` ✓). Uwaga: przy porażce new wypycha NULL → FUN_00856190
dereferowałby [NULL+0x74] (brak null-guard — P3-4, latenty bug klienta, nie
twierdzenie executora).

**(f) Ctor MovableObject FUN_0085B1B0 (własny dekod, kolejność PUSH odwzorowana):**
vtable `[ESI]=0x00A91E4C` (imm32 @0x0085B1C3 ✓); `[ESI+4]=0`;
**`[ESI+8]=arg2=WARIANT`** (`89 46 08` @0x0085B1CB — pin pozycji operandu
0x0085B1CC per konwencja ERRATA_R3 reg.5); +0xC/+0x10=0; transform init
FUN_007345C0(this+0x14); `[ESI+0x3C]=0`; zera f32 +0x44..+0x70;
**KLUCZ: `[ESI+0x74]=FUN_004123D0(record)`** (`8B 01 C3` = deref; call
@0x0085B20A, store @0x0085B211) = `[record+0]` ✓; `[ESI+0x78]=[record+4]`
(FUN_00746550 `8B 41 04 C3`); `[ESI+0x7C..0x84]=0`; **param-set:
`[ESI+0x88]=[record+0x20]; [ESI+0x8C]=[record+0x24]`** (FUN_00746570
`8D 41 20 C3`; call @0x0085B22D; loads @0x0085B234/0x0085B23F) ✓;
`[ESI+0x98]=1.0f` (FLD1+FSTP @0x0085B24D-0x0085B255) ✓; `[ESI+0x50..0x58]=
[0x00BA921C/20/24]` (globals) @0x0085B28E-0x0085B2A6 ✓; 2×vec3 z FUN_0040B070
→ +0x5C..0x70 ✓; bajty +0x9C..+0xA0=0.
Ctor pochodny FUN_00528E50: vtable `[ESI]=0x00A7DCB0` (imm32 @0x00528EA4 —
pin `C7 06 B0 DC A7 00` ✓); base call @0x00528E8D; po bazie: lookup po kluczu
`FUN_00414130([this+0x74])` → FUN_005247C0 → new(0x98)+FUN_00509330 →
`[this+0xC0]` (sub-obiekt — dekod poza szwem; kandydat wiązania modelu).

**(g) RTTI (własne łańcuchy):** vtable 0x00A91E4C → `[vtable-4]=0x00AB33D0`
(COL; sig 0; `[COL+0xC]=0x00B7997C` TD) → TD+8 = **`.?AVMovableObject@@`**
(bytes 2E 3F 41 56 4D 6F 76 61 62 6C 65 4F 62 6A 65 63 74 40 40 ✓). Pochodna:
vtable 0x00A7DCB0 → `[0x00A7DCAC]=0x00AA17CC` COL → TD 0x00B79958 →
**`.?AVClientMovableObject@@`** ✓. Slot-0 unikalność: skan DWORD 0x0085B7F0 po
WSZYSTKICH sekcjach = **1 trafienie: 0x00A91E4C (.rdata)** = sama vtable ✓✓
(brak innych typów ze wspólnym slot-0). imm32 0x00A91E4C w .text = 3 (ctor
@0x0085B1C3 + dtor-base @0x0085B3AB + dtor-deleting @0x0085B7FB ✓✓✓); imm32
0x00A7DCB0 w .text = 2 (ctor @0x00528EA4 + dtor @0x005290AA) ✓.

**(h) Insert FUN_00856190 (własny dekod pełny):** `83 7F 74 00` CMP
[value+0x74],0 → JZ ret0 ✓; EnterCS(mgr+0x44) (FUN_00413440); **klucz =
FUN_00414130(value)`=`[value+0x74]`** (`8B CF; E8 7F DF BB FF; 89 44 24 0C` —
piny executora dokładne ✓); map=mgr+0x10 (`8D 73 10`); rehash FUN_00856090(map,
[mgr+0x24]+1) @0x008561C5; para {klucz@+0xC, wartość@+0x14} (`89 7C 24 14` ✓);
find-or-create FUN_00854D90(map, out{node,flag}, &para) (`E8 B5 EB FF FF` ✓);
node FUN_00854260: **alloc 0xC przez [0x00A75A38-E8 59 A7 00 = __node_alloc]**
(`C7 44 24 04 0C 00 00 00; FF 15 E8 59 A7 00`), **`[node+4]=para[0]=KLUCZ;
[node+8]=para[1]=WARTOŚĆ; [node+0]=0`** (`89 31; 89 51 04; C7 00 00..`) ✓✓;
flag==0 → duplikat: **`MOV EAX,[EDI]; MOV EDX,[EAX]; 6A 01; MOV ECX,EDI; FF
D2`** = slot0(PUSH 1) = deleting dtor zniszczenia duplikatu ✓✓; LeaveCS;
ret.

**(i) Resolver FUN_008544D0 (własny dekod):** EnterCS(mgr+0x44) →
FUN_00971780(map, &klucz, &out) → hit: **`MOV ESI,[EAX+8]` @0x008544F9** ✓ →
LeaveCS → return wartość; miss → 0 ✓. hashfind FUN_00971780: **`DIV` (F7 F7 —
bez znaku!) key % (n_bucketów-1)** (`MOV EDI,[map+0xC]; SUB EDI,[map+8]; SAR
EDI,2; SUB EDI,1; XOR EDX,EDX; DIV EDI`), bucket=[start+hash*4], granica
łańcucha = **wartość następnego bucketa** (`MOV EAX,[EAX+4]` po `MOV ECX,[EAX]`),
pętla `CMP [ECX+4],ESI / MOV ECX,[ECX]` ✓ (node key@+4, next@+0 — STLport ✓).

**(j) TA-SAMOŚĆ klucza (ścieżka dekompilacji z dokładnymi VA):** kursor →
`[rec+0]` @0x007453EF/0x007453F6 → `FUN_00853A50(placement, klucz)`:
`[placement+0]` @0x004C48E6 (z `[ESP+0x10]` @0x004C48DD) → kopia w creatorze →
ctor: `[value+0x74]=[record+0]` @0x0085B20A/0x0085B211 → insert:
`klucz=[value+0x74]` @0x008561AC → `node+4=klucz` @0x00854284. **JEDEN klucz
wiązże komunikat, rekord placementu, węzeł mapy i instancję** ✓✓✓.

**(k) Manager:** singleton `[0x00BA12E8]` getter FUN_004154F0 (lazy `PUSH
0x8C` @0x0041551C ✓); ctor FUN_008550C0: **mapa hash@+0x10** (LEA ECX,[ESI+0x10]
@0x00855104; `PUSH 0x64` @0x00855107 = 100 bucketów; CALL FUN_00854C00
@0x0085510E) ✓; druga struktura +0x2C..+0x40 wyzerowana ✓; CS @+0x44 (new(0x20)
`6A 20` @0x00855138) ✓; 12 floatów +0x58..+0x84 ✓ (FST ×12).

**(l) Napędy i driver (piny własne):** builder FUN_00567770 — 1 caller
@0x0056836C (driver) ✓; driver FUN_00567C50 — 3 callery: **A** 0x0058E0B7 (FUN_0058DB50),
**B** 0x005B7567 (FUN_005B72C0 = handler 0xB9), **C** 0x00515345 (FUN_00514EF0) ✓.
Prolog drivera: EBP=arg1(klucz) @0x00567C8B; ESI=arg3(rekord stanu)
@0x00567C92; EBX=arg2 @0x00567C99; EDI=this @0x00567CA0. **Granica #2 rozstrzygnięta:**
site getterD @0x00567D16 i @0x00567D46: `8B CE` = ECX=ESI=**arg3 (rekord stanu;
czyta [rekord+0x10])**; site @0x00567F72: ECX=`[ESP+0x20]` (`8B 4C 24 20`
@0x00567F56) = **this (kolejka)** ✓. Singleton CMP: FUN_004143F0 (lazy-init
**[0x00BA1260]**, `PUSH 0x4C`) → `8B C8; E8 15 65 26 00` (getterA [singleton+8])
→ **`3B E8` CMP EBP(klucz),EAX** @0x00567CC4-0x00567CCB ✓ (hipoteza
"własny-klucz-awatara" pozostaje HIPOTEZĄ — konsument=CMP, właściciel poza
zakresem).

**(m) Negative bounded (VFS→param-map):** census funnelu insertu: FUN_00856190
←1× FUN_004C46C0 ←6× {FUN_004C47F0, FUN_00456F40, FUN_0050BED0, FUN_00442190,
FUN_00441910, FUN_004B3A00} ←FUN_00457930 8× {…} — **ZERO krawędzi z rodziny
0x0094xxxx**; parsery FUN_0094BD30 (2 callerów: 0x0094E2D6/0x0094E42F),
FUN_0094F350 (2: 0x00950100/0x0095022F) — wszyscy w rodzinie 0x0094xxxx ✓.
FUN_00730C90 ←1× @0x0072FBA5 (FUN_0072FA30 = builder rejestru definicji) ✓.
Granica: census E8-direct (bounded; payload parserów poza zakresem) ✓.

**(n) Censusy (własne, niezależne — zgodność z deklaracjami executora):**
resolver=4 ✓; ctor base=1 ✓; ctor pochodny=1 ✓; insert=1 ✓; creator=6 ✓;
processor=4 ✓; builder=1 ✓; driver=3 ✓; keyproducer=8 ✓; walker=108 ✓;
mgr-getter=104 ✓; getterA=808 E8+9 E9 ✓; getterD=116 E8+1 E9 ✓; attr-writer=53
✓; find-or-create=18 ✓; node-init=2 ✓; rehash=1 ✓; dispatcher=2 ✓
(0x004B1BE6=FUN_004B1B70 ring-pump; 0x004B29A9=FUN_004B2950 Execute);
FUN_005B72C0=1 @0x004B1A16 ✓; FUN_004574F0=1 @0x004B198B ✓; FUN_004B0AB0=1
@0x004B1AC1 ✓; FUN_004B1670=1 @0x004B1AD9 ✓; FUN_00752700=1 @0x005B73B3 ✓;
FUN_00752640=1 @0x005B7338 ✓; FUN_007453D0=1 @0x004C483D ✓; FUN_00745360=1
@0x004C4821 ✓; FUN_005B5F90=3 (wszystkie w FUN_005B6370) ✓; FUN_006CB6F0=2 ✓;
FUN_00567170=1 ✓. **WSZYSTKIE liczebności executora potwierdzone.**

**(o) GB6-IMMUTABLE (własny repeat):** executor before==after (composite
8/8 IDENTICAL) ✓ **+ mój własny pełny repeat per-plikowy: 1385 plików w 8
pakietach — wszystkie zbiory i hashe identyczne z census after**
(QC_GB6_PERFILE.json; verdict GB6_PERFILE_IDENTICAL) ✓✓.

**(p) Determinizm:** SCRIPT_SHA256.csv — 19/19 skryptów (ostatnie-hashe
last-wins z adnotacjami re-hash) = hashe plików na dysku (MATCH) ✓; manifest
195 wierszy pokrywa 194 pliki pakietu ✓; manifesty GHIDRA_LOCAL
AT_COPY==FINAL (1178 B, identyczne rozmiary) ✓.

**(q) Hashe evidence przed/po QC:** QC_HASH_before.json (194 pliki) vs
QC_HASH_after.json — **zero zmian w evidence executora** (jedyny przyrost =
pliki auditora w 00_CONTROL\qc_probe).

---

## 2. FINDINGS

### **[P2-1] Zbiór typów deserializujących kanał pozycji: 0xB9 wykluczone, 0xB2 pominięte**
- **Źródło (executor, raport-layer):** RESEARCH_FINDINGS.md:20 ("kursor
  podkomunikatu (typy 0xB0/0xB9/0xC6/0xC7, dispatcher FUN_004B18D0) jest
  deserializowany (FUN_007453D0: ... pozycja vec3 u32×3@+0x50..0x58, wariant
  bajt@+0x5C...)") + SEAM_FLOW_MAP.md:68 ("FUN_004C47F0 (processor placementu,
  4 callerów = ww. handlery").
- **Przeciw-dowód (własne bajty):** census E8 → FUN_004C47F0 = DOKŁADNIE 4
  call-site'y: 0x00457594 (FUN_004574F0 = handler 0xB0), 0x004B0B47
  (FUN_004B0AB0 = 0xC6), 0x004B171A (FUN_004B1670 = 0xC7), **0x004B1DBC
  (FUN_004B1C70 — NIE handler 0xB9!)**. Handler 0xB9 FUN_005B72C0 NIE woła
  FUN_004C47F0 (dekompilat: brak; census: brak site'u z 0x005B7xxx). FUN_004B1C70
  jest wołana z **FUN_004B2950 (Execute) przy `param_2==0xB2`** (special-case
  PRZED dispatcherem; byte-table[0xB2]=0x15→slot 21=default-pusty — 0xB2
  omija switch), a FUN_004B2950 = wpis vtable **@0x00A7C200** (własny odczyt
  DWORD; RTTI właściciela COL@0x00AA032C→TD@0x00B733A0 =
  **`.?AVArkClientPacketExecutor@@`** — potwierdzenie RTTI tożsamości z rundy-1).
  FUN_004B1C70 czyta u32 z kursora + zapisuje `[mgr+0x224]` (kandydat
  "id własnego obiektu/awatara") i przekazuje TEN SAM kursor do FUN_004C47F0
  (`PUSH ESI; CALL @0x004B1DBC`).
- **Skutek:** kanał pozycji z kursora = {0xB0, 0xC6, 0xC7 (case dispatchera),
  0xB2 (special-case Execute)}; 0xB9 niesie klucze (kanon rundy-1 pozostaje
  prawdziwy DLA 0xB9) i NIE deserializuje pozycji przez FUN_007453D0.
- **Poprawka:** sformalizowana w ERRATA_R4 [SE-R4-1] + finalnym REPORT.md
  (macierz krawędzi M0). Evidence nietknięte.
- **Test rewalidacji:** census E8 FUN_004C47F0 == 4 z powyższymi VA; dekod
  FUN_004B2950: `cmp param_2,0xAC/0xB2`; byte-table[0xB2]==21.

### **[P2-2] Atrybucja pól deserializatu: pozycja→+0x38 (nie +0x50..0x58); wariant→u16@+0x34 (nie bajt@+0x5C)**
- **Źródło (executor, raport-layer):** SEAM_FLOW_MAP.md:78 ("value+0x44..0x4C
  = pozycja z rekordu (setter f90 ← deserializat @+0x50..0x58)") +
  RESEARCH_FINDINGS.md:73/20 ("+0x50/+0x54/+0x58=POZYCJA vec3; +0x5C=WARIANT
  bajt").
- **Przeciw-dowód (własne bajty):** f90 w FUN_004C47F0 ma arg =
  **`LEA ECX,[ESP+0x48]` @0x004C48EB = &[rec+0x38]** — pole wypełniane przez
  **FUN_00412430 @0x0074545A (3×dword, 12 B, advance 12 z SUB-kursora)**;
  trójka @+0x50/+0x54/+0x58 to DRUGI wektor: X2 `[rec+0x50]` →
  FUN_00797280(placement, X2) @0x004C491E → **`[placement+4]=X2`** + string
  nazwy tworzenia (FUN_004C4640/FUN_00765930 → create arg3); Z2 `[rec+0x58]`
  → slot5 f32 → **`[value+0x98]`** (FUN_0085B010 = `MOV [this+0x98],arg` —
  ścieżki EXISTING @0x004C4864-71 i post-create @0x004C49AE-B4); Y2
  `[rec+0x54]` i bajt `[rec+0x5C]` — przeczytane, NIE konsumowane przez
  FUN_004C47F0 (skan pełnej funkcji). **WARIANT do create/ctor = u16@rec+0x34**
  (`MOVZX ECX,WORD [ESP+0x44]` @0x004C493C → create arg2 → ctor arg2 →
  `[value+8]`). Ścieżka EXISTING spójnie używa &[rec+0x38]
  (FUN_0085B3E0 @0x004C4875) — a dekompilat executora sam pokazuje
  `FUN_00730f90(local_78)` gdzie local_78 = rec+0x38 (raport-layer zaprzecza
  własnemu dekompilatowi i własnemu §3c').
- **Skutek:** wynik główny (pozycja z kursora → placement+8..0x10 →
  value+0x44..0x4C → insert) TRWA — ale etykiety pól w raporcie były błędne;
  eksplikacja wektora drugiego (X2=identification-kandydat nazwy tworzenia,
  Z2=slot5/+0x98) to wzbogacenie.
- **Poprawka:** ERRATA_R4 [SE-R4-2] + REPORT.md (macierz pól M1).
- **Test rewalidacji:** dekod FUN_004C47F0: f90-site poprzedzony LEA
  [ESP+0x48]; create-site poprzedzony MOVZX WORD [ESP+0x44]; FUN_00412430 =
  `SUB ESP,0xC; ... 3× MOV/LEA ... [ESP+4]=0xC; JMP FUN_0040DE60`.

### **[P3-1] „IDIV" w KEY_MODEL_MATRIX §0 — faktycznie DIV (bez znaku)**
FUN_00971780 @0x00971798: `F7 F7` = **DIV EDI** (opcode F7 /6; unsigned) —
nie IDIV. Dla kluczy < 0x80000000 bez różnicy; fakt bajtowy inny. Poprawione
w REPORT.md (macierz §0).

### **[P3-2] Piny kontekstowe vs START-opcodu (reguła ERRATA_R3 §5)**
„8D 4E 10 6A 64 @0x008550FE" — opcode LEA @0x00855104 (okno T6 zaczyna się
6 B wcześniej); „EBP=arg1 @0x00567C88" — MOV @0x00567C8B; „8B F9
@0x00567CA8" — MOV EDI,ECX @0x00567CA0; „89 46 08 @0x0085B1CC" — opcode
@0x0085B1CB (pin pozycji operandu — konwencja znana z ERRATA_R3 [M-3/M-4]).
Bajty i semantyka we wszystkich przypadkach poprawne; odnotowane w REPORT.md.

### **[P3-3] Slot5 = FUN_0085B010 = zapis f32 do value+0x98**
Etykieta "slot5 z f32 (pozycja/velocity setter)" jest luźna: bajtowo
`MOV [this+0x98],arg` — jedno-f32 pole (ctor inicjuje +0x98=1.0f; processor
nadpisuje Z2). Odnotowane w REPORT.md (M1).

### **[P3-4] Brak null-guard w FUN_00856190 (obserwacja, nie twierdzenie executora)**
`CMP [EDI+0x74],0` z EDI=NULL (porażka new w FUN_004C46C0 wypycha NULL) →
dereferencja NULL. Latenty bug klienta; poza zakresem szwu (nie blokuje).

---

## 3. Scoping (krytyczne dla uczciwości) — bez przecieku

Executor NIE przenosi wyniku MovableObject na statyki: §7 utrzymuje
"4508/296445 pozycje NIEODZYSKANE", D@4508=ANCHORS_ABSENT_SEMANTICS_OPEN,
"value+0x44 pochodzi z komunikatu, nie z definicji" ✓. Finalny REPORT rozdziela
JAWNIE: (a) CONFIRMED — kanał komunikatowy zasilania pozycji instancji
**MovableObject** (pełny łańcuch VA-locked); (b) OPEN — czy statyki
(4508/296445) przechodzą tym/innym kanałem (kandydaci FUN_00567170/FUN_005B5F90/
FUN_006CB6F0 bez zmian; statyki NIE zostały objęte kanałem movable w tym runie).

## 4. NOT_CHECKED (jawne)

- Ciała wirtualne konsumentów poza szwem: slot3 FUN_0085B6A0 (f32-ptr provider),
  FUN_008599A0 — NIE zdekodowane (osie/jednostki UNRESOLVED — bez zmian);
- Upstream kursora (kto wypełnia ring/bufor: kolejka sieciowa vs lokalna) —
  NIE prześledzony (2 callerów dispatcherа zbadanych; vtable
  0x00A7C200=ArkClientPacketExecutor — callerzy vtable poza zakresem);
- FUN_00509330/FUN_005247C0 (+0xC0 sub-obiekt ctora pochodnego — wiązanie
  modelu movables) — poza szwem; 19 ctor-callers bez setterów z Fazy A —
  NOT_CHECKED (bez zmian);
- Composer FUN_008553D0 wewnątrz (14 instrukcji selektora) — re-użyty z
  PKG_A (F2, tam zweryfikowany 14/14); w tym runie sprawdziłem piny brzegowe
  (getterA/FUN_0085AD50/census E18 22-site'ów nie recountowane per-site);
- Payload plików VFS poza zakresem (GB5 NOT_APPLICABLE ✓ słusznie).

## 5. Pełna lista odczytów (FULL_READ_LOG)

Executor: RESEARCH_FINDINGS.md (139 l.), RUN_CONTRACT.md (42 l.),
SEAM_FLOW_MAP.md (82 l.), KEY_MODEL_MATRIX.md (67 l.),
STAGE_ACCEPTANCE_GATES.csv (8 l.), S0_ERA_ASSERTION.json, SELF_CHECK.json,
T6_BYTE_PINS.json (64 piny — cross-check z własnymi hexdumpami),
SCRIPT_SHA256.csv, GB6_IMMUTABLE_COMPARISON.json, gb6_immutable.py; dekompilaty:
F004B18D0, F005B72C0, F004C47F0, F007453D0, F00752700, F00752640, F0040DE60,
F00730F90, F00730FD0, F004B2950, F004B1C70, F005247C0, F0085B010, F00853A50
(własne bajty obu), MANIFEST_SHA256.csv (struktura); runda-1: PE_MASTER_REVIEW
(RUN4), QC_REPORT (RUN4) §B4-B5, Z1_producer/Z2_cwo_chain (grep-celowane),
ROUND_REPORT §1c-§2/§4, ERRATA_R3 (format, reguły 1-5). Własne: QC_CENSUS.json
(45 funkcji), QC_DISPATCHER.json, QC_GB6_REPEAT.json, QC_GB6_PERFILE.json,
QC_HASH_before.json; hexdump/dekod własny: FUN_004B18D0(+tablice),
FUN_004574F0, FUN_004B0AB0, FUN_004B1670, FUN_004B2950, FUN_004B1B70, FUN_004B1C70
(0x004B1D90-DC5), FUN_007453D0 (pełny), FUN_004124B0/30, FUN_007343E0,
FUN_004C47F0 (0x004C47F0-0x004C4A04 pełny skan modrm), FUN_004C46C0 (pełny),
FUN_00528E50 (head), FUN_0085B1B0 (pełny), FUN_00856190 (pełny), FUN_00854260,
FUN_00853A50, FUN_00797280, FUN_008544D0, FUN_00971780, FUN_008550C0,
FUN_004154F0, FUN_007527F0, FUN_004143F0, FUN_0085B7F0 (T6), RTTI×2 (własne
łańcuchy), 0x00A7C200 vtable+RTTI, driver FUN_00567C50 (0x00567C50-0x00567F80).

**Werdykt końcowy: QC_PASS** — wynik nośny executora (klasa wartości =
MovableObject/ClientMovableObject; insert-seam VA-locked; klucz=uchwyt
instancji z komunikatu; źródło danych insertów = komunikat) POTWIERDZONY
niezależnymi bajtami; 2×P2 + 4×P3 klasy dokumentacyjnej sformalizowane w
ERRATA_R4/REPORT bez zmiany evidence. Publikacja dopuszczona.
