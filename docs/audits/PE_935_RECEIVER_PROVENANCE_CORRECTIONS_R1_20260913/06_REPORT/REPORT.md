# REPORT — PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913 (FINAL)

**RUN_CLASS:** LOAD_BEARING. **Executor:** pe-reconstruction. **INTERNAL_QC + formalizacja
+ publikacja:** pe-master-auditor (QC_PASS — 03_EVIDENCE\QC_REPORT.md; poprawki QC-1..QC-7
włączone). **TRYB:** STATIC-ONLY (klient/sieć/mock/Frida/x32dbg NIE uruchomione).
**ERA:** EU 9.3.5 (pcg_install). Binarium Entropia.exe SHA256
E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (8015872 B, image base
0x00400000, ASLR OFF); templates.vfs SHA256 BE57818C7516F8C6C8A68DF427591567DD0E5A421934A-
D A57E8261F65B77 (560788 B). **REPO:** eudoria-clean @ BASE_SHA 24d7669f7a1e5717ed2b5d5338b70ff4d7daabbe
(publikacja: path-limited, patrz HANDOFF.md). **RUN_STATUS: PASS_WITH_BOUNDARY** (granice
RECEIVER_UNRESOLVED jawne — §7). Errata supersession: **06_REPORT\ERRATA_R3.md**.
Raport roboczy executora (warstwa badawcza): 06_REPORT\RESEARCH_FINDINGS.md (ZACHOWANY;
rozbieżności z niniejszą warstwą finalną rozstrzyga ERRATA_R3 §G).

---

## 1. F1–F5 — disposition + własny test + wynik + dowód + poprawione twierdzenie

### F1 — receiver provenance wspólnego gettera FUN_007CE1E0 — CONFIRMED-correction
- **Dispositions Desktop:** przyjęty (most RUN3 wycofany w obu ogniwach).
- **Własny test:** niezależne odtworzenie łańcucha ABI vtable 0x00A86850 → fabryka →
  ctory → getter z bajtów + census rejestracji + korelacja mangling↔imm32 + kontrola
  pozytywna rekordu (parser→lookup→getter→pump).
- **Wynik:** PASS 7/7 ogniw (QC-G2, QC-G3, QC-G4).
- **Dowód (własne bajty):** vtable slot1=0x0070BF50, RTTI `.?AVArkObjectClass@@`
  (COL 0x00AA7F28→TD 0x00B8D068); fabryka: PUSH ECX(arg2)→**PUSH ESI(klasa=arg1)**→
  MOV ECX,EAX(this)→CALL @0x0070BF96; ctor klasy: MOV EBP,[ESP+0x28](arg1, 9 pushów
  SEH)→vft @0x0070CFB6→**MOV [ESI+8],EBP @0x0070CFC1**; ctor ArkObject: MOV EBX,
  [ESP+0x24](arg1, 8 pushów)→vft 0x00A86B48 @0x00726EA1 (RTTI `.?AVArkObject@@`)→
  [obj+4]=EBX→**MOV ECX,EBX+CALL getter @0x00726EB7→MOV [ESI+0x28],EAX @0x00726EBC**;
  getter `8B 41 08 C3`; DAT_00BA58CC=9 trafień, store `A3 CC 58 BA 00` @0x0073D882,
  writer→ctor FUN_0073AB60(Impl Surgeon, PUSH 0x4E43).
- **Poprawione twierdzenie:** **Getter FUN_007CE1E0 nie ma jednej semantyki** — odczytuje
  +8 różnych typów odbiorców: (a) rekord templates.vfs (+8=A=id pliku .nif), (b)
  instancję ArkObjectClass (+8=numeryczne ID klasy 20xxx/24xxx), (c) wartość mapy
  managera parametrów (+8=small int wariantu), (d) pola singletonów systemowych,
  (e) lokalne rekordy placementu (+8=position.X). **ArkObject+0x28 = kopia
  numerycznego ID klasy** (54 rejestracje param-set z imm32 + 1 lazy-init klasy
  bazowej ID 0 [poprawka QC-1]; „40 call-site'ów" RUN3 = niedoliczenie), NIE pole A
  rekordu. **Most „templates.vfs.A → ArkObject+0x28" NIE istnieje** — istnieje most
  „class-ID → encja@+0x28". **DAT_00BA58CC = singleton klasy
  ArkObjectClassImpl<ArkSurgeonObject,20035>**, nie „globalny template" (rejestracje
  po store'u: FUN_0070E2F0, FUN_00734C40, FUN_0070C150, FUN_0070BF10 [poprawka QC-2]).

### F2 — „konsument D" — CONFIRMED-correction (selektor) + PARTIAL (queue-push) + granice
- **Dispositions Desktop:** przyjęty (selektor zasilany +8, nie D@+0x10).
- **Własny test:** niezależny dekod gałęzi 0x4E38 (14 instrukcji), tabela skoków
  0x00855BB4 (4 wpisy) + bloki 2/3/4; odrębność gałęzi gettera D @0x008556DF;
  dataflow walker→[EAX]→+8 (resolver `8B 70 08` @0x008544F9); własny walk
  templates.vfs (5438/0 CRC/EOF) i odczyt D@4508; censusy E8+E9 getterów.
- **Wynik:** PASS (QC-G5, QC-G6).
- **Dowód:** QC_F2_SELECTOR.json; QC_F2_VFS_WALK2.json; QC_CENSUS_GETTERS.json.
- **Poprawione twierdzenie:** selektor gałęzi 0x4E38 czyta **+8 wartości mapy managera
  parametrów** (walker-current→MOV ECX,[EAX]→CALL FUN_007CE1E0), a mapowanie
  4/5→2, 6→3, 7→4 (tabela [2,2,3,4], bloki MOV [ESP+0x1C],2/3/4) jest arytmetyką
  na TYM odczycie; getter D FUN_0048ADA0 @0x008556DF leży w ODRĘBNEJ gałęzi (odczyt
  +0x10 tej samej wartości) — **claim RUN4 „D steruje wyborem wariantu" REJECTED_
  AS_ATTRIBUTED**. „D do capacity-push": PARTIAL — [arg1+0x10] trafia do FUN_00567B40,
  ale odbiorca ≠ dowiedziony rekord template'u (RECEIVER_UNRESOLVED per caller), a
  flaga gate kolejki pochodzi z porównania [singleton_0x00BA1260+8] vs FUN_00844130(arg),
  nie z D. **D@4508 = 0x42F9E1CB = f32 124.94100189208984 @96528; A=296445
  @96516; semantyka liczbowa NIE ROZSTRZYGNIĘTA** (nie ogłaszano statycznej
  nierozstrzygalności). Censusy: D-dword **117** (116 E8 + 1 E9 @0x7CDCCE),
  D-f32 **10**, w FUN_00468910 **12** (nie 5; lista VA identyczna z moim censusem);
  różnice raw/isCall = tail-jumpy E9 (9 dla gettera A @0x7103C6/0x72AC36/0x73EC16/
  0x73EEB6/0x73F256/0x742296/0x742CC6/0x74C156/0x8DC566).

### F3 — negatywy bajtowe — CONFIRMED-correction
- **Dispositions Desktop:** przyjęty (zakres negatywu niesemantyczny).
- **Własny test:** własny walk templates.vfs (reguła stride 36×ceil((16+size)/36),
  kalibracja 67 par, EOF dokładny); odczyt metody s12 (payload.find — wszystkie
  offsety); dekod RTTI klasy 20006.
- **Wynik:** PASS.
- **Poprawione twierdzenie:** **ANCHORS_ABSENT_SEMANTICS_OPEN** — brak 13 kotwic LE32
  (na wszystkich offsetach; .prt 276 payloadów, 27 plików .vfs, brak 20006.vfs) NIE
  wyklucza kodowań pochodnych ani nie domyka gramatyki 20xxx.vfs; „27 plików ≠ 27
  rodzin formatu". **0x4E26 (20006) = ID klasy ArkObjectClassImpl<ArkParameterCommon,
  20006>** (PUSH @0x0073B871/CALL @0x0073B87D, vft 0x00A870C4, mangling `$0EOCG@`)
  — pliki VFS są kandydatem nośnika zasilania, nie definicją klasy. RUN2 D3:
  pozytyw client-side istnieje TYLKO dla DAoC; dla WAR macierz ma negatyw
  (ERRATA_R3 [SE-3]).

### F4 — 0/38 STATIC_WORLD — CONFIRMED-correction
- **Dispositions Desktop:** przyjęty (negatyw ≠ wykluczenie użycia).
- **Własny test:** odczyt klasyfikacji Z2 (RUN3) + własne censusy powiązań
  (settery/ctor) potwierdzające, że klasyfikacja dzieli FUNKCJE wg roli.
- **Wynik:** PASS (re-kwalifikacja; bez nowych pomiarów merytorycznych — zgodnie z
  deklaracją executora).
- **Poprawione twierdzenie:** „na censurowanej powierzchni 25 lookupów + 13 pumpów
  nie zidentyfikowano żadnego call-site'u z **DOWIEDZIĄ DEDYKOWANEJ ROLI
  STATIC_WORLD (0/38)**"; funkcje wspólne (FUN_00567170, FUN_005B5F90, FUN_006CB6F0
  i pozostałe MODEL_MACHINERY/OTHER) pozostają **jawnymi wspólnymi kandydatami**
  (cross-role-function) — użycie przez statyki nierozstrzygnięte, nie wykluczone.
  Nawias Z2:62 „(ctor pobiera A z obiektu template → +0x28)" — błędny (patrz F1).

### F5 — „WYŁĄCZNIE z atrybutów" — CONFIRMED-correction (z poprawką QC-3)
- **Dispositions Desktop:** przyjęty (kwantyfikator wycofany).
- **Własny test:** odczyt predykatu qc_b2_exclusive.py (heurystyka 3×CC linie 45-52;
  writer FUN_00845F70 w ATTR linia 18); własny census 26/24 ctor-FUN_00730700 z
  atrybucją Ghidra i własnymi granicami; własny census attr/singleton dla 15
  setter-callerów z adiustacją 4 spornych startów (prologi SEH) i granicą
  0x00567170/0x00567770 (blob danych bez paddingu).
- **Wynik:** PASS (QC-G6).
- **Poprawione twierdzenie:** „**we wszystkich prześledzonych ścieżkach
  builder→getter atrybutów→setter** (statycznie, w zasięgu testu) transformy pochodzą
  z systemu atrybutów" — kwantyfikator globalny nieuzasadniony (predykat = census
  wywołań w przybliżonych ciałach, nie trace provenance). Rozliczenie 15
  setter-callerów f90: **9 bezpośrednich + 3 czysto parametryczne (FUN_00459270/
  0043A200/00488920) + 3 singleton-readers (FUN_005B5F90, FUN_0046E790,
  FUN_00567170)** [poprawka QC-3 — „10 bezpośrednich" RUN4 QC B2 zawierał artefakt
  zlewu ciał]; **FUN_0046E790: NO_DIRECT_ATTR_CALLS, woła singleton managera
  parametrów FUN_004154F0 @0x46EA1F, settery f60/f90/fb0, provenance NIEROZLICZONA**;
  FUN_00567170: 0 attr-callów w własnym ciele (jedyny — singleton @0x567662),
  provenance NIEROZLICZONA. **26 call-site'ów ctor FUN_00730700 w 24 funkcjach;
  5 z setterami, 19 bez (NOT_CHECKED — pełna lista VA w ERRATA_R3 [SE-8])**.

## 2. Macierz klas/struktur (typy odbiorców gettera — każdy wiersz z dowodem bajtowym)

| # | Typ odbiorcy | Pochodzenie odbiorcy (dowód bajtowy — własny) | Layout +8 | Kto czyta +8 (VA) | Rola |
|---|---|---|---|---|---|
| 1 | **Rekord templates.vfs** | rejestr RB; lookup FUN_0072F580 (rb-find FUN_004D1430 @0x72F590; **hit→`83 C0 14` @0x72F59E**; miss→0x00BA5800); FUN_006C3F50: ECX=EDI po lookup @0x006C3F62 | parser `89 47 08` @0x00730CE6; **+8=A (id pliku .nif)**; B@+4, C@+0xC, D_f32@+0x10 (file: A@record+0x14, D@record+0x20) | FUN_006C3F50 @0x006C3F74; FUN_006B4C50 @0x006B4C82/0x006B4C93; slot-gettery FUN_006C2840/70→tabela 0x00A858B4/B C→FUN_0043A550 | **id modelu NIF** (join A→`<A>.nif` 3618/3618 — RUN1) |
| 2 | **ArkObjectClass** | perklasowe lazy-init singletony (wzorzec: new(0x118)→ctor→store→rejestracje); RTTI: vtable−4→COL 0x00AA7F28→TD 0x00B8D068 `.?AVArkObjectClass@@`; vft-write `C7 06 50 68 A8 00` @0x0070CFB6 | **+8=numeryczne ID klasy** (MOV [ESI+8],EBP @0x0070CFC1; EBP=arg1=imm32 z 54 rejestracji + 1 lazy-init ID 0); bajt low(arg1)@+0xC; CS@+0x24/+0x5C; string@+0xA0 | ctor ArkObject FUN_00726E70 @0x00726EB7 (ECX=arg1=klasa) | **identyfikator klasy/param-setu** (np. 20035 Surgeon; 20030 Container; 20006 ArkParameterCommon) |
| 3 | **ArkObject** (odbiorca końcowy) | fabryka FUN_0070BF50 (slot1 vtable 0x00A86850): PUSH ESI(klasa=arg1)→CALL ctor @0x0070BF96; RTTI `.?AVArkObject@@` (vft 0x00A86B48, COL 0x00AA8008, TD 0x00B8CFBC) | **+8=zagnieżdżona CRITICAL_SECTION** (FUN_004134F0 CS-init @+8) — nie liczba; +4=ptr klasy; **+0x28=[class+8]=class-ID** (`89 46 28` @0x00726EBC); +0x2C=arg2 | getter wołany na KLASIE (nie na encji) | encja świata; +0x28 = **kopia ID klasy** |
| 4 | **Wartość mapy managera parametrów** | walker FUN_0085B840→singleton FUN_004154F0→[0x00BA12E8] (0x8C); resolver FUN_008544D0: mapa mgr+0x10, lock mgr+0x44, rb-find FUN_00971780, **[hit+8]** @0x008544F9; walker-current FUN_0085B860: *out=[walker+0] | **+8=small int (wariant 4..7)**; +0=vtable (potwierdzone @0x00855B2F-3F: MOV EDX,[ECX]; MOV EAX,[EDX+8]; CALL EAX); +4=nullable CS-ptr (FUN_0085B190); +0x10 czytane getterem D w innej gałęzi; +0x44..+0x4C f32 | FUN_008553D0 @0x008557FD (gałąź 0x4E38) | **znacznik wariantu konstruktora**; NAZWA KLASY: **RECEIVER_UNRESOLVED** |
| 5 | **ArkModelResourceInstanceRef** | ctor FUN_006FA8B0: vft `C7 00 B8 64 A8 00` **@0x006FA8BD (+0xD; M-1)**; item `89 48 08` @0x006FA8C3; licznik [EAX+4]=0; RET 4 | **+8=item (ptr na element zasobu)** | bezpośredni getter-call z tym odbiorcą: **NIE WYKAZANY** (kandydaci: podsystem 0x006Fxxxx — poza zakresem) | kontener referencji instancji modelu (layout potwierdzony; rola gettera UNKNOWN) |
| 6 | **Singletony systemowe** | FUN_004143F0→[0x00BA1260] (size 0x4C); FUN_004154F0→[0x00BA12E8] (0x8C); FUN_00415570→[0x00BA12EC] (0xCC) — wzorzec lazy-init (MOV EAX,[global]; TEST; JNZ ret; PUSH size; CALL new) | +8=flaga/identyfikator (w porównaniach gate) | FUN_00567B40 (queue-push) @0x00567B50 (po CALL FUN_004143F0 @0x00567B49) | rola +8: **UNKNOWN** (kandydat: level/typ singletonu); użycie: flaga gate porównania z FUN_00844130(arg) |
| 7 | **Rekord placementu na stosie** | lokalne rekordy w driverach; FUN_00468910: LEA ECX,[ESP+0x1C] @0x00468D84→CALL getter D @0x00468D88 (12 site'ów w tej funkcji); builder FUN_00567770 (rekord z RUN3) | **+8=position.X** (vec3 @+0x08/+0x0C/+0x10); +0x10=position.Z (ten sam offset co D template'u — inna rola); rotacja@+0x14 | getter-D @0x00468D88 i 11 dalszych (FUN_00468910) | **rekord runtime placementu** |

**Kontrola rozróżniająca:** RTTI/vtable odbiorcy + dataflow ECX callera rozróżnia
wiersze 1–4 (wiersz 1: ECX z lookupu, brak vtable; 2: RTTI klasy, imm32; 3: now(0x58)
z vft 0x00A86B48, +8=CS; 4: ECX=[hit+8], vtable@+0). Wiersze 5–7 z jawnymi UNKNOWN.

## 3. Mapa przepływu (ogniwa PROVEN/UNPROVEN)

```
templates.vfs (plik)                                    [PROVEN: własny walk 5438, parser @0x00730CE6]
  └─parser→rekord{A=id NIF}@rejestr-RB                   [PROVEN: lookup +0x14; kontrola pozytywna]
      └─getter A (@0x006C3F74) → para {0x66=MODEL,A}    [PROVEN: ECX=EDI=rekord]
          └─pump/resource-system → instancja modelu     [PROVEN: RUN1/RUN3; granica RUN3 E.3]
              └─...→ NIF otwarty                        [STRONGLY_SUPPORTED (RUN1 D; PARTIAL_TO_RESOURCE)]

ArkObjectClass<T, id-imm32> (54 rejestracje + 1 korzeń) [PROVEN: census 55; imm32 54; RTTI 36/36]
  └─fabryka slot1 (PUSH ESI=klasa jako arg1)            [PROVEN: bajty @0x0070BF92-96]
      └─ctor ArkObject: getter [class+8]→encja@+0x28    [PROVEN: @0x00726EB7/@0x00726EBC]
          └─encja+0x28 = kopia ID klasy                 [PROVEN: wartość = imm32 rejestracji]

mapa managera parametrów (mgr+0x10, [hit+8]=wartość)    [PROVEN: resolver @0x008544F9]
  └─wartość: vtable@+0, small-int@+8 (+0x10=D-field)    [PROVEN: @0x00855B2F-3F; +0x10 w gałęzi @0x008556DF]
      └─selektor wariantu (gałąź 0x4E38) czyta +8       [PROVEN: 14 instrukcji + tabela]
          └─[INSERT do mapy: KTO wstawia wartości]      [UNPROVEN — RECEIVER_UNRESOLVED #1]
          └─[nazwa klasy wartości]                      [UNPROVEN — RECEIVER_UNRESOLVED #1]

drzewo atrybutów encji (FUN_00846840; 0x6A4/0x6A5/0x6A8/0x6A9)
  └─builder FUN_00567770 → FUN_00567C50 → setterzy f60/f90/fb0/fd0 → rekord placementu
                                                        [PROVEN jako ścieżka: RUN3/RUN4 + ten run (§1 F5)]
      └─[źródło WARTOŚCI w drzewie: plik/sieć/mieszane] [UNPROVEN — H1/H2/H3/H4 otwarte]
      └─arg1 FUN_00567C50 (3 callerów)                  [UNPROVEN — RECEIVER_UNRESOLVED #2]
  └─[statyki przez wspólne funkcje?]                     [UNPROVEN — kandydaci jawni (F4)]
```

## 4. Twierdzenie → źródło → pomiar → kontrola → wynik → artefakt

| Twierdzenie | Źródło | Pomiar (własny) | Kontrola | Wynik | Artefakt |
|---|---|---|---|---|---|
| Fabryka przekazuje klasę jako arg1 | bajty 0x0070BF50-96 | dekod 4 bajtów push-run + prolog SEH ctora (9 pushów → [ESP+0x28]=arg1) | kolejność pushów (ostatni=arg1) | CONFIRMED | QC_F1_ABI.json |
| [class+8]=ID klasy | rejestracje | census 55 E8; 54×PUSH imm32; korelacja 36/36 z RTTI | reguła manglingu mechanicznie; 4 pary bajt-co-bajt; negatyw: zapis mid-instr @0x00516F0E wykluczony | CONFIRMED (+QC-1) | QC_F1_CLASSID.json; QC_F1_CLASSID_PAIRS.md |
| encja+0x28=[class+8] | ctor ArkObject | bajty @0x00726EB7/EBC | dataflow ECX=EBX=arg1 | CONFIRMED | QC_F1_ABI.json |
| DAT_00BA58CC=singleton klasy | writer | census imm32=9; store @0x0073D882; ctor→FUN_0073AB60 | read-back/clear/accessor w census | CONFIRMED (+QC-2) | QC_F1_DAT58CC_POSCONTROL.json |
| rekord@hit+0x14 (kontrola pozytywna) | lookup | dekod FUN_0072F580 | miss→0x00BA5800; ECX=EDI przed getterem | CONFIRMED | QC_F1_DAT58CC_POSCONTROL.json |
| selektor czyta +8 mapy (nie D@+0x10) | gałąź 0x4E38 | 14 instrukcji + tabela 4 + bloki | gałąź gettera D @0x008556DF odrębna; dekompilat ZS1 zgodny | CONFIRMED | QC_F2_SELECTOR.json |
| wartość mapy polimorficzna | FUN_008553D0 | skan FF/2 (pełny) — wywołanie [vft+8] @0x00855B2F-3F | brak CALL [reg+0xC] w ciele (QC-4) | CONFIRMED | QC_F2_SELECTOR.json |
| walk 5438/0 CRC/EOF; D@4508 | templates.vfs | własny walk (stride 36×ceil((16+s)/36); 67 par) | CRC32 per payload; EOF exact; negatyw stride (16+size fails @2) | CONFIRMED | QC_F2_VFS_WALK2.json |
| censusy getterów 817/117/10/26/24/15 | .text | E8+E9 po całym .text | zbiory vs Ghidra isCall (∅ rozbieżności; E9=tail-jumpy) | CONFIRMED | QC_CENSUS_GETTERS.json |
| 5/19 setter-usage ctor-callers | 24 funkcje | własny scan ciał (własne granice) | atrybucja Ghidra zgodna; 2×dwo-site ciała | CONFIRMED | QC_F5_SETTERS.json |
| 15 setter-callerów 9/3/3 | f90 | własny scan attr/singleton (pełna lista ATTR) | adiustacja prologów 4 startów; granica 0x567170/0x567770 | CONFIRMED (+QC-3) | QC_F5_SETTERS.json |
| GA5 zero zmian | 7 pakietów + repo | composite SHA256 własny | before/after/now potrójnie | PASS | QC_GA5_IMMUTABLE.json |

## 5. Dokładne liczebności i wyłączenia

| Pomiar | Wartość | Wyłączenia/uwagi |
|---|---|---|
| Call-site'y ctor ArkObjectClass (E8=isCall) | **55** | 54 imm32 param-set + 1 PUSH 0 (lazy-init klasy bazowej; QC-1) |
| Rejestracje z imm32 20xxx/24xxx | **54** (każda wartość 1×) | 0x4E20..0x4E4B (z lukami 0x4E36/37/49/4A) + 0x5DC2..0x5DD1 (brak 0x5DCE) |
| Korelacja mangling↔imm32 | **36/36**, 0 rozbieżności | 18 rejestracji bez vtable-Impl w ciele (rodzina pochodna inna) |
| Fabryka — bezpośredni CALL | **0** | dispatch wyłącznie wirtualny (slot1) |
| getter A: raw E8 / E9 / isCall | **808 / 9 / 817** | E9=tail-jumpy (lista VA §1 F2); zbiory identyczne |
| getter D-dword: raw E8 / E9 / isCall | **116 / 1 / 117** | E9 @0x7CDCCE |
| getter D-f32 | **10** (0 E9) | w tym FUN_00861390 ×2 @0x861B49/0x861EEB |
| getter D w FUN_00468910 | **12** | lista VA = lista executora |
| ctor rekordu FUN_00730700 | **26 site'ów / 24 funkcje** | FUN_00447630 ×2, FUN_0050E490 ×2; 5 z setterami, **19 bez (NOT_CHECKED)** |
| setter pozycji FUN_00730F90 | **15 site'ów / 15 funkcji** | 9 bezpośrednich + 3 parametryczne + 3 singleton-readers (QC-3) |
| imm32 0x00A86850 / 0x00A86B48 / 0x00BA58CC / 0x00BA5D9C | **3 / 2 / 9 / 9** | 0x00A86850: 2 realne + 1 koincydencja @0x00516F0E (wykluczona dumpem) |
| Walk templates.vfs | **5438 rekordów, 0 CRC-fail, EOF=560788** | 73 różne size; id2==id dla size-28 (3435); 0 duplikatów id |
| GA5 | **7 pakietów composite-hash identyczny** (before==after==now) + repo-296445 git-clean | ROUND=4 pliki; RUN1=576; RUN3=220; RUN4=381; RUN2=25; JOIN=26; DESKTOP=10 |
| Evidence executora | **15/15 kluczowych plików hash-przed==hash-po QC** | QC dodał tylko nowe pliki |

## 6. Odpowiedzi (odrębne)

1. **Co identyfikuje model?** Pole **A rekordu templates.vfs** (id pliku .nif; parser
   zapisuje A→rekord+8 @0x00730CE6; join A→`<A>.nif` 3618/3618 — RUN1). Getter
   FUN_007CE1E0 zwraca A **wyłącznie gdy ECX=rekord z lookupu rejestru RB**
   (kontrola pozytywna odtworzona bajtowo). Dla encji ArkObject identyfikatorem jest
   **numeryczne ID klasy @encja+0x28 (kopia [class+8])** — NIE A rekordu.
2. **Jak powstaje instancja?** Fabryka wirtualna ArkObjectClass (slot1 vtable
   0x00A86850 = FUN_0070BF50): new(0x58) → ctor ArkObject FUN_00726E70 z klasą jako
   arg1 → encja z kopią ID klasy @+0x28. Modele NIF: instancja przez resource-system
   (pump {0x66=MODEL,A} → ArkModelResourceInstanceRef → nazwana instancja `<id>__<name>`
   — RUN3 E.3). Klasy rejestrowane statycznie w 54 funkcjach (imm32) + lazy-init
   singletonów per klasa (np. DAT_00BA58CC = Impl<ArkSurgeonObject,20035>).
3. **Skąd jest transform?** W prześledzonych ścieżkach: **z drzewa atrybutów encji**
   (FUN_00846840; builder FUN_00567770→setterzy f60/f90/fb0/fd0; RUN3/RUN4 + ten run
   §1 F5). Źródło WARTOŚCI w drzewie: **UNKNOWN** (H1 plikowy bez pozytywu; H2
   propagacja PROVEN; H3 kanał istnieje, transform-decode UNPROVEN; H4 0xB9 nie
   wykluczony). Selektor wariantów 0x4E38 czyta +8 wartości mapy parametrów
   (RECEIVER_UNRESOLVED), nie D template'u. Kwantityfikator „wyłącznie" — wycofany.
4. **Czy odzyskano autentyczne pozycje 296445? NIE.** Historyczne pozycje placementu
   NIE zostały odzyskane; transform 296445@4508 (D=124.941) istnieje w danych
   (zweryfikowane bajtowo), ale jego semantyka liczbowa i związek z historycznymi
   pozycjami świata pozostają NIE ROZSTRZYGNIĘTE.

## 7. Granice RECEIVER_UNRESOLVED i następny eksperyment

**Granice (NON-PASS, jawne):**
1. Nazwa klasy wartości mapy managera parametrów ([hit+8]) — dataflow/layout
   potwierdzone, nazwa nie; rozstrzygnięcie: (1) punkt INSERT do mapy mgr+0x10
   (kandydaci: FUN_0085B3E0/0085B780/0085B7F0; 71 funkcji z singleton-getterem;
   FUN_009719D0 generyczny operator[]), (2) ctor wartości (vtable+int@+8), (3) runtime
   (zakazany).
2. arg1 FUN_00567C50 przy getterach D (3 callerów: world-object state / bufor 0xB9 /
   handler-arg).
3. 19 funkcji ctor-callers bez setterów — semantyka NOT_CHECKED (lista VA [SE-8]).
4. FUN_00567170/FUN_0046E790 (+FUN_005B5F90/0043A200/00488920) — provenance wartości
   setterów NIEROZLICZONA.
5. Semantyka D=124.941@4508 — ANCHORS_ABSENT_SEMANTICS_OPEN.
6. Cross-role-function: użycie wspólnych funkcji (FUN_00567170/005B5F90/006CB6F0...) przez
   statyki — nierozstrzygnięte (0/38 = brak dowiedzionej DEDYKOWANEJ roli).

**NASTĘPNY EKSPERYMENT (Faza B):** FORMAT-DECODE 20xxx.vfs + szew parser→insert-map:
zdekodować format plików Data\Parameters\20xxx.vfs (za templates.vfs: ArkVFS02,
stride 36×ceil((16+size)/36)), prześledzić reader FUN_00972DF0→...→mapę mgr+0x10
(punkt INSERT — rozstrzyga jednocześnie granicę #1 i kanał zasilania klas 20006/20035
danymi), oraz wyznaczyć ctor wartości mapy (vtable+int@+8). STAT-ONLY; runtime
(human-gated Frida offline-probe) jako alternatywa. Cel pośredni: domknąć szew
parser→attribute-tree z RUN4 §9; cel główny pozostaje: producent transformów statyków.

---
**Skala statusów:** claim-status oddzielony od gate-result, persistence i readiness
(§QC_REPORT). Finalne promocje kanonu/pojedyncze bramki zależą od PE-MASTER/człowieka.
**Nie ogłoszono STATIC_INSTANCE_MECHANISM_CONFIRMED ani źródła placementu.**
GHIDRA_LOCAL (379 520 056 B) pozostaje LOCAL-ONLY (manifest SHA w 00_CONTROL).
