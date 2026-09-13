# RESEARCH_FINDINGS — PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913

**Rozstrzygnięcie pięciu findingsów audytu Desktop własnymi próbkami bajtowymi + materiał erraty SUPERSESSION.**
RUN_CLASS: LOAD_BEARING. TRYB: STATIC-ONLY (klient/Frida/x32dbg/mock/sieć NIE uruchomione).

- **ERA**: EU 9.3.5 (pcg_install). Binarium `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe`
  SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (8 015 872 B, image base
  0x00400000, ASLR OFF). `templates.vfs` SHA256 BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77
  (560 788 B). **S0 fail-closed PASS** (01_RAW\S0_ERA_ASSERTION.json; asercja OBU SHA własnym skryptem).
- **REPO**: D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean @ BASE_SHA 24d7669f (weryfikacja startowa:
  HEAD = BASE; dirty wyłącznie obce `?? experiments/` — POZA ZAKRESEM, NIETKNIĘTE). Ten run NIE wykonuje
  operacji git (publikacja: pe-master-auditor po QC).
- **AUDIT_OUTPUT_ROOT**: `D:\Eudoria_Reconstruction\99_Audits\PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913\`
  (nieistniał przed runem — brak kolizji). Projekt Ghidra skopiowany z RUN4 (GHIDRA_LOCAL; 10 plików,
  379 520 056 B). **Cykl życia projektu w tym runie (jawny):** stan w chwili kopiowania = po-tury-ZS RUN4
  (db.63/db.64.gbf — manifest 00_CONTROL\GHIDRA_LOCAL_MANIFEST_AT_COPY.csv); dwie tury analyzeHeadless
  tego runu (rc1_ga_attrs.py, rc1_refcounts.py; -noanalysis, -process) wywołały zapis projektu
  ("Save succeeded") → nowe checkpointy db.67/db.68.gbf (dawne nadpisane — standardowy cykl Ghidra);
  **manifest finalny = 00_CONTROL\GHIDRA_LOCAL_MANIFEST_SHA256.csv (db.67/68 — stan wysyłkowy)**.
  Dzięki rozdzieleniu manifestów pakiet NIE powtarza błędu RUN4 (stale manifest — patrz errata M-8).

---

## 1. Odpowiedź na pytanie główne (jedno zdanie + status)

**Getter FUN_007CE1E0 (`8B 41 08 C3`, MOV EAX,[ECX+8]; RET) nie ma jednej semantyki: odczytuje +8
różnych typów odbiorców — (a) rekordu templates.vfs (pole A = id NIF; kontrola pozytywna odtworzona
bajtowo), (b) instancji ArkObjectClass (numeryczne ID klasy 20xxx/24xxx), (c) wartości mapy managera
parametrów (small-int wariantu — selektor 0x4E38), (d) singletonów systemowych i (e) lokalnych rekordów
placementu (+8 = position.X)** — most RUN3 „templates.vfs.A → ArkObject+0x28" jest odrzucony obu
ogniwami (odbiorca = klasa, wartość = ID klasy), a selektor „D=4/5→2,6→3,7→4" czyta +8 odbiorcy
atrybutowego, nie D@+0x10. Status: **CONFIRMED-correction (F1, F2) z jawnymi granicami
RECEIVER_UNRESOLVED** (nazwa klasy wartości mapy parametrów; provenance arg1 w FUN_00567C50).

## 2. F1 — receiver provenance wspólnego gettera: CONFIRMED-correction

### 2.1 ABI odtworzone z bajtów (każde ogniwo VA+bajty; artefakt F1_ABI_BYTES.json)

| Ogniwo | VA | Bajty (własny odczyt) | Znaczenie |
|---|---|---|---|
| vtable ArkObjectClass | 0x00A86850 | slot0=0x0073F230, **slot1=0x0070BF50**; vtable−4 → COL 0x00AA7F28 → +0xC → TD 0x00B8D068 | RTTI **`.?AVArkObjectClass@@`** (TD+8: `2E 3F 41 56 41 72 6B 4F 62 6A 65 63 74 43 6C 61 73 73 40 40`) |
| fabryka (slot1) | 0x0070BF50 | `8B F1` MOV ESI,ECX; `6A 58` PUSH 0x58; `E8..` CALL new@0x0095D3C4; `8B 4C 24 1C` MOV ECX,[ESP+0x1C]; `51` PUSH ctor-arg; `56` **PUSH ESI (this fabryki = ArkObjectClass — PIERWSZY argument)**; `8B C8` MOV ECX,EAX; `E8 D5 AE 01 00` **CALL FUN_00726E70 @0x0070BF96**; RET 4 | fabryka wirtualna: **0 bezpośrednich callerów** (census E8 + Ghidra isCall = 0) |
| ctor ArkObjectClass | 0x0070CF80 | `8B 6C 24 28` MOV EBP,[ESP+0x28] (arg1); **`C7 06 50 68 A8 00` MOV [ESI],0x00A86850 @0x0070CFB6**; **`89 6E 08` MOV [ESI+8],EBP @0x0070CFC1**; (+0xC struktura z bajtem low(EBP); CS @+0x24 i +0x5C; string @+0xA0 z arg2) | **[class+8] = arg1 ctora** |
| ctor ArkObject | 0x00726E70 | `8B 5C 24 24` MOV EBX,[ESP+0x24] (arg1); `8D 4E 08` LEA ECX,[ESI+8]; **`C7 06 48 6B A8 00` MOV [ESI],0x00A86B48 @0x00726EA1**; `89 5E 04` [obj+4]=EBX; CALL FUN_004134F0 (CS-init @+8); `8B CB` MOV ECX,EBX; **`E8 24 73 0A 00` CALL FUN_007CE1E0 @0x00726EB7**; **`89 46 28` MOV [ESI+0x28],EAX @0x00726EBC**; [obj+0x2C]=arg2; RET 8 | **odbiorca gettera = arg1 = ArkObjectClass; encja+0x28 = [class+8]** |
| getter | 0x007CE1E0 | `8B 41 08 C3` | MOV EAX,[ECX+8]; RET |

### 2.2 CO ląduje w ArkObject+0x28 (sedno F1)

**[class+8] = numeryczne ID klasy (param-set family)** — ustalone z dwóch niezależnych ścieżek:

1. **Census 55 rejestracji klas**: każda z 55 funkcji woła ctor ArkObjectClass z imm32 jako arg1
   (PUSH imm32 bezpośrednio przed CALL): 0x4E20(20000), 0x4E21, 0x4E22, 0x4E23, 0x4E24, 0x4E25,
   **0x4E26(20006)**, 0x4E27(20007), 0x4E28..0x4E35, **0x4E38(20024)**, 0x4E39, 0x4E3A, 0x4E3B,
   **0x4E3E(20030)**, 0x3E?→0x4E3D, 0x4E40..0x4E4B + rodzina 0x5DCx/0x5DDx (24004-24017). Pełna lista
   55 (call-site → funkcja → ID): **F1_REG_ARGS.json**. Arg2 = wskaźnik na pusty string 0x00A7957B.
   ⇒ **EBP = imm32 z .text, NIE z rejestru templates.vfs** (odpowiedź kontraktowa na (b)).
2. **Korelacja RTTI**: mangled names klas kodują te same liczby —
   `.?AV?$ArkObjectClassImpl@VArkSurgeonObject@@$0EOED@@@` = **0x4E43 = 20035** (vtable 0x00A87034,
   zapisywany przez ctor FUN_0073AB60 po wywołaniu base-ctor z PUSH 0x4E43);
   `.?AV?$ArkObjectClassImpl@VArkParameterContainer@@$0EODO@@@` = **0x4E3E = 20030** (vtable 0x00A86FBC,
   ctor FUN_0073A0C0, PUSH 0x4E3E @0x0073A114). Mangling MSVC `$0<hex-nibbles-A-P>@` odczytany jako
   nibble-code: E=4,O=14 → 0x4E43 / 0x4E3E — **zgodny co do bajtu z imm32 ctorów**.

⇒ **ArkObject+0x28 = kopia numerycznego ID klasy** (np. 20035 dla instancji SurgeonObject; 20030 dla
ArkParameterContainer), a NIE „A (id pliku .nif)". Most RUN3 §1 (REPORT.md:13-19) — **REJECTED_WITH_EVIDENCE**
(obydwa ogniwa): odbiorca ≠ rekord, wartość ≠ A. RUN3 „40 call-site'ów ctora" = niedoliczenie
(Ghidra isCall: **55** ctor ArkObjectClass + **55** ctor ArkObject; 0 fabryka).

### 2.3 DAT_00BA58CC — writer i rola (GA1-F1 (c))

Writer = **FUN_0073D810** (lazy-init; pełny hexdump: F1_CTX_WRITER_DAT00BA58CC.txt):
`83 3D CC 58 BA 00 00` CMP [0x00BA58CC],0 @0x0073D832 → new(0x118) @0x0073D84D+ → CALL ctor
FUN_0073AB60 @0x0073D86B → **`A3 CC 58 BA 00` MOV [0x00BA58CC],EAX @0x0073D882** → rejestracje
FUN_0070E2F0(obj,8,7) @0x0073D888, FUN_006B6541, FUN_0072C151, FUN_0072BF11; przy porażce wirtualny
dtor (slot0, PUSH 1) + `C7 05 CC 58 BA 00 00 00 00 00` wyzerowanie globalu.
**Census imm32 0x00BA58CC w .text = 9 trafień**, wszystkie w cyklu życiowym klasy: init-check
@0x0073D832/d833, store @0x0073D882, read-back @0x0073D88D, MOV ECX @0x0073D897/8A5/8B4 (rejestracje),
clear @0x0073D8C7, accessor `A1 CC 58 BA 00; C3` @0x0073C970, load w ctorze SurgeonObject @0x0073520D
(`8B 0D CC 58 BA 00`; PUSH ECX jako arg1 base-ctora @0x00735213; CALL FUN_00726E70 @0x00735216).
**DAT_00BA58CC = singleton klasy ArkObjectClassImpl<ArkSurgeonObject, 20035> — deskryptor klasy,
NIE rekord template'u i NIE dane placementu.** RUN3 „globalny template DAT_00ba58cc" — odrzucone.

### 2.4 Census xrefów vtable 0x00A86850 + klasyfikacja callerów (GA1-F1 (b))

- **Census imm32 0x00A86850 w .text = 3**: (1) disp32 w `C7 06 50 68 A8 00` vft-write ctora @0x0070CFB6;
  (2) disp32 w `C7 06 50 68 A8 00` vft-restore w **dtorze** ArkObjectClass @0x0070D19A (funkcja
  0x0070D170: prolog SEH, po nim kasowanie pól i wirtualne wywołania na dzieciach); (3) @0x00516F0E —
  **koincydencja środkowoinstrukcyjna** (PUSH EAX `50` + PUSH 0xA8 `68 A8 00 00 00` — rozkład
  potwierdzony dumpyem F1_CTX3_HIT3_00516F0E.txt) — wykluczona.
- Fabryka FUN_0070BF50: **0 bezpośrednich CALL** (raw-E8 i Ghidra isCall = 0) — wyłącznie dispatch
  wirtualny (slot1). Akcesor singletonu FUN_0073C970 (zwraca [DAT_00BA58CC]): 0 bezpośrednich callerów.
- **Klasyfikacja ≥5 rzeczywistych callerów maszyny fabrykującej (z kontekstem):**
  1. ctor ArkObjectClass **FUN_0070CF80** (vft-write @0x0070CFB6) — bazowy konstruktor klas;
  2. dtor ArkObjectClass **FUN_0070D170** (vft-restore @0x0070D19A) — cykl życia;
  3. **FUN_0073AB60** — ctor klasy pochodnej (base-ctor z 20035 @0x0073ABBD → vft 0x00A87034;
     RTTI ArkObjectClassImpl<ArkSurgeonObject,20035>);
  4. **FUN_0073D810** — lazy-init singletonu klasy (writer DAT_00BA58CC);
  5. **FUN_0073AC00** — per-class fabryka (slot1 vtable 0x00A87034; CALL ctor ArkSurgeonObject
     FUN_007351E0 @0x0073AC45; 0 bezpośrednich callerów — wirtualna);
  6. **FUN_007351E0** — ctor pochodnej instancji (ładuje [DAT_00BA58CC] jako arg1 base-ctora).
  Granica: statyczny graf NIE wskazuje bezpośredniego wywoływania slot1 0x00A86850 — wszystkie drogi
  przechodzą przez wskaźniki klas (rejestr klas + dispatch wirtualny).

### 2.5 Kontrprzykłady odbiorców gettera (F1 (d) — min. 3 typy; kontrola pozytywna)

**Kontrola pozytywna (wzorzec poprawnej proweniencji) odtworzona bajtowo:**
parser → `89 47 08` **MOV [EDI+8],EAX @0x00730CE6** (pole A → rekord+0x08; kursor VFS z bounds-check
`3B 4E 08`/`77 13` i advance `6A 04`+CALL) → rejestr RB-tree (lookup **FUN_0072F580**: rb-find
FUN_004D1430 → **rekord@hit+0x14**, miss → 0x00BA5800) → `FUN_006C3F50`: `MOV ECX,EDI` (rekord)
po CALL lookup @0x006C3F62 → **CALL FUN_007CE1E0 @0x006C3F74** → para {0x66=MODEL, A} → pump.
Slot-gettery FUN_006C2840/006C2870 (C×2 → tabela 0x00A858B4 → FUN_0043A550 → lookup) zasilają
FUN_006B4C50 (getter ×2 @0x006B4C82/0x006B4C93 → pump ×2) — **F1_CTX5_*.txt, F1_BODYSET_CALLMAP.json**.

**Typy odbiorców (macierz GA3 — RECEIVER_MATRIX.md, 7 wierszy):**
1. **Rekord templates.vfs** — identyfikacja: dataflow z lookupu + layout parsera; +8 = A (id NIF);
2. **ArkObjectClass** — identyfikacja: RTTI + vft-write + imm32 rejestracji; +8 = ID klasy;
3. **ArkObject** (odbiorca końcowy) — RTTI `.?AVArkObject@@` (vft 0x00A86B48, COL 0x00AA8008,
   TD 0x00B8CFBC); +8 = zagnieżdżony CRITICAL_SECTION (FUN_004134F0: PUSH ESI → CALL
   [0x00A75068] InitializeCriticalSection-family; magic `C7 46 1C BA 19 E3 1F` @+0x24) — **+8 ArkObject
   nie jest liczbą**, co rozstrzyga, że getter na ArkObject daje wskaźnik DebugInfo, nie dane;
4. **Wartość mapy managera parametrów** (F2) — patrz §3; nazwa klasy RECEIVER_UNRESOLVED;
5. **ArkModelResourceInstanceRef** — layout item@+8 (ctor FUN_006FA8B0: `C7 00 B8 64 A8 00`
   @**0x006FA8BD**, `89 48 08` item @+8); bezpośredni getter-call z tym odbiorcą NIE wykazany;
6. **Singletony** (FUN_004143F0→[0x00BA1260] 0x4C; FUN_004154F0→[0x00BA12E8] 0x8C;
   FUN_00415570→[0x00BA12EC] 0xCC) — +8 czytane w gate'ach (FUN_00567B40);
7. **Lokalny rekord placementu** — +8 = position.X (vec3 @+0x08/+0x0C/+0x10 — RUN3 settery A6),
   +0x10 = position.Z — **ten sam offset, inna rola niż D template'u**.

**Kontrola odróżniająca**: metoda (RTTI/vtable + dataflow ECX callera) ROZRÓŻNIA typy 1–4 (szczegóły
RECEIVER_MATRIX.md §3); dla typu 4 nazwa klasy pozostaje RECEIVER_UNRESOLVED z granicą (§3 poniżej).

## 3. F2 — błędny konsument D: CONFIRMED-correction (selektor) + PARTIAL (queue-push) + granice

### 3.1 Gałąź 0x4E38 odtworzona z bajtów (F2_CTX_BRANCH_008557C0.txt)

```
0x008557DD: 3D 38 4E 00 00        CMP EAX,0x4E38            (param-set 20024)
0x008557E2: 0F 85 8E 00 00 00    JNZ default (0x00855876)
0x008557E8: 8D 54 24 38           LEA EDX,[ESP+0x38]        (out)
0x008557EC: 52                   PUSH EDX
0x008557ED: 8D 4C 24 1C           LEA ECX,[ESP+0x1C]        (walker)
0x008557F1: E8 6A 60 00 00       CALL FUN_0085B860         (walker-current: *out=[walker+0];
                                      CALL FUN_0085B190([walker+0]) — lock [value+4] if ≠0)
0x008557F6: 8B 08                 MOV ECX,[EAX]            ← ECX = wartość mapy = [walker+0]
0x008557FD: E8 DE 89 F7 FF       CALL FUN_007CE1E0         (getter +8 odbiorcy!)
0x00855802: 8B 4C 24 38 / 8B F0   MOV ECX,[ESP+0x38]; MOV ESI,EAX  (ESI = wynik gettera)
0x00855811: 8D 46 FC             LEA EAX,[ESI-4]
0x00855814: 83 F8 03             CMP EAX,3
0x00855817: 77 23                JA default (0x0085583C)
0x00855819: FF 24 85 B4 5B 85 00 JMP [EAX*4+0x00855BB4]
```
Tabela 0x00855BB4 (4 wpisy, zdumpowane + zdekodowane): [0]=**0x00855834**, [1]=**0x00855834**,
[2]=**0x00855820**, [3]=**0x0085582A**; bloki: [ESP+0x1C]=2 (v=4,5), =3 (v=6), =4 (v=7).
Arytmetyka „4/5→2, 6→3, 7→4" — prawdziwa; **źródło = +8 odbiorcy, NIE D@+0x10**.
Getter D FUN_0048ADA0 @**0x008556DF** leży w INNEJ gałęzi tego switcha (odbiorca: ta sama wartość mapy,
odczyt +0x10) — RUN4 Z4 §2-3 i QC B10 przypisały go błędnie do selektora. Dekompilat własny RUN4
(ZS1_PSEUDO_008553D0.txt:203-216: `uVar13 = FUN_007ce1e0(); switch(uVar13)`) potwierdza; claim był
sprzeczny z artefaktem własnym runu.

### 3.2 Tożsamość odbiorcy +8 (GA2-F2)

Dataflow (walker→[EAX]→+8) ustalony dokładnie: **odbiorca = [hit+8] mapy managera parametrów**
(manager = singleton DAT_00BA12E8 rozmiaru 0x8C, getter FUN_004154F0; mapa @mgr+0x10; lock @mgr+0x44;
find = FUN_00971780; resolver FUN_008544D0: `8B 70 08` **MOV ESI,[EAX+8]** @0x008544F9 → return [hit+8];
key = param_1 FUN_008553D0 — builder FUN_00567770 woła FUN_008553D0 @0x005679B8 z ECX=manager,
arg1 = wynik rejestracji FUN_00457930). Layout wartości: **+0 = vtable** (wywołanie wirtualne slot3
`CALL [vft+0xC]` w gałęzi 0x38B0 tego samego switcha), **+4 = nullable CS-ptr** (FUN_0085B190:
`8B 49 04; 85 C9; 74 05; E9 → FUN_00413440`), **+8 = small int (wariant 4..7)**, +0x44..+0x4C f32,
+0x5C..+0x64 dword, +0x10 czytane getterem D w innej gałęzi.

Eliminacje (kontrola odróżniająca): **NIE rekord templates.vfs** (wartość polimorficzna; rekordy bez
vtable; +8 rekordu = A = duże id NIF); **NIE klasa pochodna ArkObject/ArkParameter*** (11 klas rodziny
ArkParameter*: Container/Transformation/SetObject/Common/ServerGlobal/ServerLocal/Creature/Action/
Blueprint/Tool/Makeup — każdy ctor woła base-ctor FUN_00726E70 z globalnym wskaźnikiem klasy ⇒ +4 =
nie-null ptr klasy, +8 = początek CRITICAL_SECTION — sprzeczne z nullable-lock@+4 i small-int@+8);
**NIE ArkObjectClass** (+8 = ID klasy 20000+, nie 4..7).
**Nazwa klasy wartości = RECEIVER_UNRESOLVED**; granica rozstrzygnięcia: (1) punkt INSERT do mapy
mgr+0x10 (kto wstawia wartości pod kluczami param-setów; census kandydatów: 71 funkcji wołających
singleton-getter, rodzina FUN_00854520-008548A0 = akcesory get-or-fail; FUN_009719D0 = generyczny
operator[] z 1 wywołaniem poza celem), (2) ctor wartości (zapis vtable + int@+8), (3) runtime (zakazany).

### 3.3 Pozostałe twierdzenia „konsument D" z RUN4 (receiver per claim)

| Twierdzenie (Z4 §2-3 / QC B10) | Status | Receiver/dataflow |
|---|---|---|
| FUN_008553D0 selektor 0x4E38 = D@+0x10 | **REJECTED_AS_ATTRIBUTED** | selektor = +8 wartości mapy (getter A @0x008557FD) |
| FUN_00567C50→FUN_00567B40 „D do capacity-push" | **PARTIAL** | getter D @0x00567D16/D46 przed pushami @0x00567D24/D54 ✓; ale odbiorca = **[arg1+0x10]** FUN_00567C50 (arg1 = pierwszy arg stosowy — per-caller: world-object state / bufor 0xB9 / handler-arg; RECEIVER_UNRESOLVED per caller); 3. call @0x00567F72 na **this**; sama bramka pusha FUN_00567B40 czyta **[singleton_0x00BA1260+8] getterem A** i porównuje z FUN_00844130(arg) (flaga → 5. arg FUN_00567170) |
| FUN_00861390 ×2 f32-D „distans/LOD" | **CENSUS-CONFIRMED** | 2 site'y @0x00861B49/0x00861EEB (f32-getter 0x00861240), arytmetyka f32; odbiorca = ESI (per-funkcyjny arg); pełny census D-f32 = **10** callerów — dokładnie lista Z4 §2 ✓ |
| FUN_00468910 ×5 „update world-objectu" | **UNDERCOUNT** | Ghidra isCall = **12** site'ów (lista: 0x00468D88, 0x00468DA4, 0x004692BC, 0x004692D7, 0x004692F2, 0x0046930D, 0x004694BE, 0x004694D9, 0x004694F0, 0x00469A7D, 0x00469AF0, 0x00469B0D); spot-check @0x00468D88: odbiorca = **lokalny rekord @ESP+0x1C** (+0x10 = składowa Z vec3 pozycji rekordu placementu) |
| census getter D = 116 (QC B10) | **AUTHORITATIVE 117** | Ghidra isCall = 117 (raw-E8 = 116 — QC cytowała raw) |
| D template'u 4508 = 124.941 | **ZWERYFIKOWANE (semantyka UNKNOWN)** | własny pełny walk templates.vfs: **5438 rekordów, 0 CRC-fail, EOF**; rekord 4508 @file 96496 (size 28, CRC AFF5797C OK), **A=296445**, B=296446, C=0, **D@file+0x20 (=payload+0x10) @offset 96528 = bits 0x42F9E1CB = f32 124.94100189208984**, E=0.0, F=0 |

## 4. F3/F4/F5 — dispositions

- **F3 (negatywy bajtowe): CONFIRMED-correction.** Własna weryfikacja: negatyw 13 kotwic = metoda
  `payload.find` (wszystkie offsety; s12_prt_content_check.py:63 — odczyt własny), walk templates.vfs
  5438/5438 — zakres negatywu dokładnie zadeklarowany. Nowe kwalifikacje: ANCHORS_ABSENT_SEMANTICS_OPEN;
  „27 plików ≠ 27 rodzin formatu"; brak 20006.vfs NIE dowodzi źródła sieciowego ani nazwa=ID —
  **dodatkowo: 0x4E26 (20006) to ID KLASY ArkObjectClassImpl** (rejestracja @0x0073B87D, F1_REG_ARGS)
  — pliki VFS są kandydatem nośnika zasilania, nie definicją klasy. RUN2 D3: poprawka cytatowa
  („w OBU ekosystemach client-side" → pozytyw tylko dla DAoC; dla WAR negatyw) — DRAFT_ERRATA [SE-3].
- **F4 (0/38): CONFIRMED-correction.** Klasyfikacja 38 call-site'ów dzieli FUNKCJE wg roli; 8 MODEL_MACHINERY
  + 17 OTHER + 1 UNKNOWN pozostaje wspólnymi kandydatami (FUN_00567170, FUN_005B5F90 — własne adnotacje
  „NIEROZSTRZYGNIĘTE" w Z2; FUN_006CB6F0 — twórca instancji). Sformułowanie: „0/38 z dowiedzioną
  DEDYKOWANĄ rolą STATIC_WORLD"; usunąć „statyki NIE przechodzą przez te call-site'y" — DRAFT_ERRATA [SE-4].
  (Negatyw 0/38 STATIC_WORLD sam w sobie potwierdzony — bez zmian.)
- **F5 („WYŁĄCZNIE z atrybutów"): CONFIRMED-correction.** Predykat qc_b2_exclusive.py = census wywołań
  w heurystycznych ciałach (3×CC), nie trace provenance; do ATTR wliczony writer FUN_00845F70;
  kontrprzykład logiczny Desktop poprawny wobec predykatu. Kwalifikacja: „we wszystkich prześledzonych
  ścieżkach builder→getter→setter". Rozliczenie 15 setter-callerów: 10 bezpośrednich (potwierdzone) +
  4 parametryczne (provenance 3 z 4 nadal NIEROZLICZONA) + **15. = FUN_0046E790: NO_DIRECT_ATTR_CALLS,
  woła singleton param-manager FUN_004154F0, settery f60/f90/fb0, provenance NIEROZLICZONA** —
  DRAFT_ERRATA [SE-5]/[SE-6]. 26 callerów ctora FUN_00730700: **24 funkcje (2×2 site'y); 19 funkcji
  bez setterów = NOT_CHECKED z pełną listą VA** (nadzbiór QC-owych „11") — DRAFT_ERRATA [SE-8].
- **Drobne korekty (8): wszystkie zweryfikowane własnym odczytem** — M-1 vft AMRIR @**0x006FA8BD**
  (+0xD; bajt @BC = 00 z MOV [EAX+4],0); M-2 LE 296445 = **FD 85 04 00**; M-3 vft ArkObject
  @**0x00726EA1** (bajt @0x00726E9F = operand 0x4E LEA); M-4 store +0x28 @**0x00726EBC**; M-5 QC B8
  attribution błędu (s12 skanował wszystkie offsety; aligned = osobny census u32 — L89-90);
  M-6 „0 bezpośrednich CALL Execute" ≠ brak wywołań (wirtualne przez vtable 0x00A7C1FC);
  M-7 mianowniki 3618/3618 (pokrycie A) vs 3618/5596 = 64.6533% (udział w korpusie NIF);
  M-8 reguła nakładki manifestów (ostatni poprawny manifest w czasie wiążący; RUN4 GHIDRA_LOCAL manifest
  opisuje stan PRZED własnymi turami ZS: db.52/53 → nadpisane przez db.63/64; integrity: closure manifest
  49/49). Pełne cytaty+poprawki: DRAFT_ERRATA_SUPERSESSION.md Część E.

## 5. Granice (NON-PASS jawne)

1. **RECEIVER_UNRESOLVED (nazwa klasy)**: wartość mapy managera parametrów ([hit+8]) — dataflow i
   layout ustalone, nazwa klasy nie; granica: insert-map / ctor wartości / runtime (§3.2).
2. **RECEIVER_UNRESOLVED (per-caller)**: arg1 FUN_00567C50 przy getterach D (3 callerów: stan
   world-object / bufor 0xB9 / handler-arg — provenance ogniw, nie typ nazwany).
3. **NOT_CHECKED**: 19 funkcji ctor-callers bez setterów (pełna lista VA w DRAFT_ERRATA [SE-8]);
   3 z 4 parametrycznych setter-callerów bez śledu provenance (FUN_00459270, FUN_0043a200, FUN_00488920);
   semantyka liczbowa D=124.941 (UNKNOWN — bez zmian; nie ogłaszano „statycznej nierozstrzygalności").
4. **Metodologiczne**: census E8 raw vs Ghidra isCall rozbieżne dla getterA (808 vs **817**) i
   getterD (116 vs **117**) — wiążące liczby to isCall; heurystyka granic ciał 3×CC myli funkcje
   sąsiadujące bez paddingu (FUN_00567170/FUN_00567770) i prologi SEH — dla atrybucji użyto Ghidra
   (GHIDRA_FUNC_ATTR.json) + SEH-anchoring.

## 6. Bramki (fail-closed) — 06_REPORT\STAGE_ACCEPTANCE_GATES.csv

- **GA1-F1: PASS** — ABI fabryki+obu ctorów odtworzone (każde ogniwo VA+bajty, §2.1); rola class+8
  (=ID klasy) i object+0x28 (=kopia ID) ustalona; census callerów vtable 0x00A86850 wykonany
  (3 imm32: 2 realne + 1 koincydencja; fabryka 0 direct — granica jawnie); ≥5 callerów
  sklasyfikowanych z kontekstem (§2.4); writer DAT_00BA58CC prześledzony do źródła (§2.3).
- **GA2-F2: PASS_WITH_BOUNDARY** — selektor 0x4E38 odtworzony; tożsamość odbiorcy ustalona z dataflow
  (walker→[EAX]→+8 = wartość [hit+8] mapy mgr; nazwa klasy RECEIVER_UNRESOLVED z granicą §3.2);
  tabela 0x00855BB4 zdekodowana (4 wpisy); wszystkie twierdzenia „konsument D" rozliczone (§3.3).
- **GA3-MATRIX: PASS** — macierz 7 wierszy (≥ wymaganych 5: rekord, ArkObjectClass, ArkObject,
  wartość atrybutu, instancja modelu + bonus: singletony, rekord lokalny) — RECEIVER_MATRIX.md.
- **GA4-ERRATA-MATERIAL: PASS** — kompletne cytaty (plik:linia) + nowe kwalifikacje dla F3/F4/F5
  i 8 drobnych — 02_ANALYSIS\DRAFT_ERRATA_SUPERSESSION.md [SE-1..SE-11, M-1..M-8].
- **GA5-IMMUTABLE: PASS** — census composite-hash 7 pakietów historycznych (RUN1/RUN2/RUN3/RUN4/
  ROUND/JOIN+ERRATA_R2/Desktop) przed i po — identyczne (GA5_IMMUTABLE_CENSUS_{before,after}.json);
  oryginały READ-ONLY.
- **GA6-ERA: PASS** — S0 fail-closed obu SHA (exe+templates.vfs), PE parse własny, spot-checki.

## 7. SELF_CHECK (własny; NIE audyt PE-MASTER)

- S0: oba SHA zgodne z kontraktem (fail-closed, skrypt własny, wynik w 01_RAW) ✓; AUDIT_OUTPUT_ROOT
  nieistniał → utworzony bez kolizji ✓; BASE_SHA zweryfikowany na starcie (HEAD==24d7669f..., dirty
  wyłącznie obce experiments/) ✓.
- Pełny raw census: callerzy getterA = 817 (isCall) / 808 (raw-E8) — pełna lista VA w JSON ✓;
  getterD = 117/116 ✓; ctor ArkObjectClass = 55 (pełna lista + ID każdej rejestracji) ✓;
  ctor ArkObject = 55 ✓; fabryka = 0 ✓; ctor FUN_00730700 = 26 sites/24 funkcji (Ghidra) ✓;
  f90 = 15 sites/15 funkcji (Ghidra) ✓; imm32 0x00A86850 = 3, 0x00A86B48 = 2, 0x00BA58CC = 9,
  0x00BA5D9C = 9 — pełne listy w F1_CENSUS.json ✓.
- Bramki: wszystkie 6 ocenione fail-closed z mierzalnymi danymi ✓.
- Kontrole negatywne/pozytywne: kontrola pozytywna rekordu (łańcuch bajtowy parser→lookup→getter→pump)
  ✓; kontrola odróżniająca typów odbiorców (RTTI+dataflow rozróżnia 1-4; typ 4 granica jawnie) ✓;
  koincydencja imm32 (0x00516F0E) wykluczona dumpyem ✓; negatywy wykluczeń wartości mapy (3 eliminacje
  z powodami) ✓; round-trip endianness: LE konsekwentnie (FD 85 04 00; nibble-decode manglingu
  skonfrontowany z imm32 ctorów — zgodność 2/2 klas) ✓.
- Determinizm: skrypty hashowane po ostatniej edycji (00_CONTROL\SCRIPT_SHA256.csv); brak timestampów
  w wynikach JSON ✓.
- Granice NON-PASS uczciwe: RECEIVER_UNRESOLVED (2 pozycje), NOT_CHECKED (liste jawne), UNDERCOUNT
  (12 vs 5), AUTHORITATIVE (117 vs 116) ✓.
- Zakres: bez operacji git; bez dotykania experiments/, src/game/, oryginałów i pakietów historycznych
  (GA5); bez sub-agentów; klient/sieć/mock nieuruchomione ✓.
- **Nie ogłoszono STATIC_INSTANCE_MECHANISM_CONFIRMED ani żadnego źródła placementu.**

## 8. Struktura pakietu

```
00_CONTROL\  pe_core.py, s0_era_assertion.py, f1_*.py, f2_*.py, f5_*.py, ga5_immutable.py,
             rc1_*.py (Ghidra), SCRIPT_SHA256.csv, GHIDRA_LOCAL\ (+ manifest), RUN_CONTRACT copy: patrz prompt
01_RAW\      S0_ERA_ASSERTION.json, F1_*.json, F1_HEX_*.txt, F1_CTX*.txt, F2_*.json, F2_CTX*.txt,
             F5_SETTER_ACCOUNTING.json, GHIDRA_FUNC_ATTR.json, GHIDRA_REFCOUNTS.json,
             GA5_IMMUTABLE_CENSUS_{before,after}.json
02_ANALYSIS\ RECEIVER_MATRIX.md, DRAFT_ERRATA_SUPERSESSION.md
06_REPORT\   RESEARCH_FINDINGS.md, STAGE_ACCEPTANCE_GATES.csv
```

Finalny REPORT.md i erratę sformalizuje pe-master-auditor (ten plik = raport roboczy executora).
