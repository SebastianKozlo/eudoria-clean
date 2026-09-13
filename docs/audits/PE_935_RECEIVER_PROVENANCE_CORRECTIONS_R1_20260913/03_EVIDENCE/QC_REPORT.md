# QC_REPORT — INTERNAL_QC pe-master-auditor
## RUN: PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913 (executor pe-reconstruction)

**Werdykt QC: QC_PASS** — z 3 findingami P2 i 4 P3 (klasa dokumentacyjna, poprawione
przez auditora w warstwie 02_ANALYSIS/06_REPORT niniejszego pakietu; evidence 01_RAW
executora NIETYKANE — hashe przed/po w §10) + 2 rozstrzygnięciami wyjaśniającymi.
Twierdzenia nośne F1–F5 CONFIRMED własnymi bajtami; brak P0/P1 → dopuszczona publikacja.

- **QC executora:** niezależny, świeży kontekst, WŁASNE narzędzia (00_CONTROL\qc_probe\,
  11 probe + qc_core.py — własne mapowanie PE napisane od zera), własny dekod x86,
  własny walker ArkVFS02, własne censusy E8/E9/imm32, własne hashowanie GA5.
  Evidence executora tylko CZYTANE (patrz FULL_READ_LOG §9) — przed i po QC hashe
  15 kluczowych plików identyczne (§10).
- **ERA:** EU 9.3.5. Binarium SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
  (własny odczyt; 8015872 B; image base 0x00400000; ASLR OFF — własny parse PE).
  templates.vfs SHA256 BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77
  (560788 B; własny odczyt). STATIC-ONLY zachowany (nic nie uruchomiono).

---

## 1. Własna weryfikacja twierdzeń nośnych — wynik

### F1 (most A→+0x28 wycofany; +0x28 = kopia ID klasy) — CONFIRMED własnymi bajtami
- **ABI łańcuch vtable 0x00A86850 → fabryka → ctor klasy → ctor ArkObject → getter:**
  vtable slot0=0x0073F230, slot1=0x0070BF50 (własny odczyt .rdata); RTTI: vtable−4→COL
  0x00AA7F28→TD 0x00B8D068→**`.?AVArkObjectClass@@`** (własny odczyt bajtów TD+8).
  Fabryka FUN_0070BF50: PUSH ESI (=this fabryki = instancja klasy) jako **PIERWSZY** arg
  (bajty `51 56 8B C8` @0x0070BF92-95, CALL @0x0070BF96 → 0x00726E70 — własny dekod).
  Ctor klasy: prolog SEH 9 pushów → `[ESP+0x28]`=arg1 (MOV EBP,[ESP+0x28] @0x0070CFAB);
  vft `C7 06 50 68 A8 00` @0x0070CFB6; **`89 6E 08` MOV [ESI+8],EBP @0x0070CFC1**.
  Ctor ArkObject: 8 pushów → `[ESP+0x24]`=arg1 (MOV EBX,[ESP+0x24] @0x00726E96);
  LEA ECX,[ESI+8] @0x00726E9E; vft 0x00A86B48 @0x00726EA1 (RTTI `.?AVArkObject@@`,
  COL 0x00AA8008, TD 0x00B8CFBC — własny odczyt); [obj+4]=EBX @0x00726EA7;
  **MOV ECX,EBX (arg1=klasa) + CALL FUN_007CE1E0 @0x00726EB7 + `89 46 28` @0x00726EBC**;
  [obj+0x2C]=arg2; RET 8. Getter `8B 41 08 C3`. **Oba ogniwa mostu RUN3 odrzucone
  własnymi bajtami: odbiorca = klasa (nie rekord), wartość = [class+8] (nie A).**
- **ID klasy z imm32:** census E8→0x0070CF80 = **55** site'ów (tożsamo z Ghidra isCall);
  **54** z arg1=PUSH imm32 (rodzina 0x4E20..0x4E4B + 0x5DC2..0x5DD1, każda 1×) — patrz
  jednak QC-1 (P2) poniżej dla 55. site'u. Korelacja mangling↔imm32: **36/36** par
  RTTI `$0`-suffix ↔ imm32, 0 rozbieżności; reguła nibble A=0..P=15; 4 wymagane pary
  bajt-co-bajt: Surgeon `$0EOED@`=0x4E43=20035 (PUSH @0x0073ABB1/CALL @0x0073ABBD),
  Container `$0EODO@`=0x4E3E=20030 (PUSH @0x0073A111/CALL @0x0073A11D),
  RealWorldItem `$0EOEC@`=0x4E42=20034 (PUSH @0x0073A991/CALL @0x0073A99D),
  **20006 = ArkParameterCommon** `$0EOCG@`=0x4E26 (PUSH @0x0073B871/CALL @0x0073B87D,
  vft 0x00A870C4 @0x0073B89B) — pełny dokument: 03_EVIDENCE\QC_F1_CLASSID_PAIRS.md.
- **DAT_00BA58CC:** własny census imm32 w .text = **9** (zgadza się); init-check CMP
  [mem],0 @0x0073D831; writer FUN_0073D810: PUSH 0x118 → new → ctor **FUN_0073AB60**
  (= Impl Surgeon, weryfikacja RTTI własna) → **store `A3 CC 58 BA 00` @0x0073D882** →
  rejestracje; clear @0x0073D8C6. **DAT_00BA58CC = singleton klasy
  ArkObjectClassImpl<ArkSurgeonObject,20035> — potwierdzone; „globalny template" RUN3
  odrzucone.** (Uwaga QC-2: trzy nazwy funkcji „rejestracyjnych" w opisie executora błędne.)
- **Kontrola pozytywna (rekord jako odbiorca):** parser `89 47 08` @0x00730CE6 ✓;
  lookup FUN_0072F580: rb-find FUN_004D1430 @0x72F590, **hit→`83 C0 14` (rekord@hit+0x14)
  @0x72F59E**, miss→0x00BA5800 (własny dekod całości); FUN_006C3F50: CALL lookup
  @0x006C3F62 → EDI → **CALL FUN_007CE1E0 @0x006C3F74 z ECX=EDI(rekord)** ✓; pary {0x66,A}
  (MOV EBX,0x66 @0x006C3F69). Slot-gettery FUN_006C2840/70: `8B 04 85 B4 58 A8 00`
  (tabela 0x00A858B4)/`8B 04 85 BC 58 A8 00` → FUN_0043A550 ✓; body-set FUN_006B4C50:
  getter ×2 @0x006B4C82/0x006B4C93 → FUN_007CE1E0 ✓. **Kontrola rozróżniająca działa:
  ten sam stub odczytuje +8 = A (id NIF) u rekordu (dataflow z lookupu; brak vtable)
  i +8 = ID klasy (imm32; RTTI .?AVArkObjectClass@@) u klasy — RTTI+vft+dataflow
  ROZRÓŻNIA oba typy.**
- **Klasyfikacja callerów vtable 0x00A86850:** census imm32 = **3**: vft-write ctor
  @0x0070CFB6, vft-restore dtor @0x0070D19A, **koincydencja @0x00516F0E** — własny dump:
  `50 68 A8 00 00 00` = PUSH EAX + PUSH 0xA8 (imm32 0x00A86850 przecina granice instrukcji)
  — wykluczona identycznie jak u executora. Fabryka: 0 bezpośrednich CALL (E8+Ghidra=0) —
  granica dispatchu wirtualnego potwierdzona.

### F2 (selektor czyta +8 wartości mapy, nie D@+0x10) — CONFIRMED własnym dekodem
- Gałąź 0x4E38: **14/14 instrukcji bajt-co-bajt** na pinowanych VA (CMP @0x008557DD →
  JNZ → LEA EDX,[ESP+0x38] → PUSH EDX → LEA ECX,[ESP+0x1C] → CALL FUN_0085B860
  @0x008557F1 → **MOV ECX,[EAX] @0x008557F6 → CALL FUN_007CE1E0 @0x008557FD** →
  LEA EAX,[ESI−4] → CMP EAX,3 → JA → **JMP [EAX*4+0x00855BB4]** @0x00855819).
  Tabela 0x00855BB4: [0]=0x00855834, [1]=0x00855834, [2]=0x00855820, [3]=0x0085582A
  (własny odczyt 4 dwordów); bloki: `C7 44 24 1C 02/03/04 00 00 00` — **arytmetyka
  4/5→2, 6→3, 7→4 prawdziwa, ŹRÓDŁO = +8 wartości mapy (getter A), NIE D@+0x10** ✓.
- Walker FUN_0085B860: `*out=[walker+0]; CALL FUN_0085B190(wartość)` (własny dekod;
  lock [v+4]≠0→FUN_00413440). Resolver FUN_008544D0: lock mgr+0x44 (FUN_00413440),
  mapa mgr+0x10, rb-find FUN_00971780, **`8B 70 08` MOV ESI,[EAX+8] @0x008544F9 =
  wartość=[hit+8]** ✓. Odbiorca selektora = wartość mapy managera parametrów ✓.
- **Getter D @0x008556DF → FUN_0048ADA0 to ODRĘBNA gałąź** tego switcha (własny dump
  kontekstu: ten sam wzorzec walker→MOV ECX,[EAX], ale odczyt +0x10 innego pola tej
  samej wartości; CMP EAX,0x4E38 leży dalej w łańcuchu porównań) — **nie zasilą
  selektora** ✓.
- **D@4508:** własny walk templates.vfs (własna reguła stride wyprowadzona z bajtów:
  slot = 36×ceil((16+size)/36), „stride_base 36" z nagłówka; walidacja na 67 parach
  size/stride + EOF): **5438 rekordów, 0 CRC-fail, koniec dokładnie EOF=560788**;
  rekord 4508 @file 96496 (header {id=4508, size=28, ver=1, crc=0xAFF5797C OK}),
  payload @96512: {id2=4508, **A=296445 @96516 (=record+0x14)**, B=296446, C=0,
  **D bits 0x42F9E1CB @96528 = f32 124.94100189208984**, E=0.0, F=0} —
  **ZGODNE CO DO BITU z twierdzeniem executora** (QC_F2_VFS_WALK2.json).
- **Censusy D:** getterD dword: raw E8 = 116, E9 = 1 (@0x7CDCCE), Ghidra isCall = 117
  — **różnica 116/117 = 1 tail-jump E9** (wyjaśniona poniżej §8); D-f32 = 10 (0 E9);
  FUN_00468910: **12 site'ów gettera D** — lista VA executora = moja lista (12/12, 0
  rozbieżności; UNDERCOUNT „×5" potwierdzony); spot-check @0x00468D84: LEA ECX,[ESP+0x1C]
  + CALL getter D @0x00468D88 — odbiorca = **lokalny rekord placementu na stosie**
  (+0x10 = składowa Z vec3 pozycji) ✓; f32-D w FUN_00861390: dokładnie
  {0x00861B49, 0x00861EEB} ✓.
- Queue-push FUN_00567B40: CALL FUN_004143F0 @0x567B49 → MOV ECX,EAX → CALL getter
  @0x567B50 → FUN_00844130 @0x567B5B ✓ (SE-10: bramka czyta [singleton+8] getterem A);
  FUN_00567C50: MOV ESI,[ESP+0xEC] @0x567C93 (arg1), MOV ECX,ESI przed getterami D
  @0x567D16/0x567D46 (odbiór [arg1+0x10]) + pushy @0x567D24/0x567D54 → FUN_00567B40 ✓.

### F3 (negatywy bajtowe; 20006=ID klasy) — CONFIRMED-correction
- Walk templates.vfs 5438/5438 (własny) — zakres negatywu dokładnie zadeklarowany ✓.
- Metoda s12 (odczyt własny RUN4\00_CONTROL\s12_prt_content_check.py:63): kotwice
  skanowane `payload.find(pat, off)` na WSZYSTKICH offsetach; caveat „aligned-only"
  dotyczy ODRĘBNEGO censusu u32 (L69) — opis M-5 zgodny z kodem ✓.
- **20006/0x4E26 = ID KLASY ArkObjectClassImpl<ArkParameterCommon,20006>** (własne
  bajty — patrz F1) — nowa kwalifikacja SE-2 potwierdzona: rodzina 20xxx/24xxx w .text
  to identyfikatory klas/param-setów rejestrowane w kodzie; pliki VFS = kandydat
  nośnika zasilania, nie definicja klasy ✓. ANCHORS_ABSENT_SEMANTICS_OPEN — poprawna
  kwalifikacja zakresu negatywu („27 plików ≠ 27 rodzin formatu").

### F4 (0/38) — CONFIRMED-correction (re-kwalifikacja; zgodna z evidence historycznym)
Klasyfikacja 38 site'ów dzieli FUNKCJE wg roli; 8 MODEL_MACHINERY + 17 OTHER + 1 UNKNOWN
pozostają wspólnymi kandydatami; sformułowanie „0/38 z dowiedzioną DEDYKOWANĄ rolą
STATIC_WORLD" — zgodne z tabelą Z2 (odczytana) i censusami historycznymi (RUN3 QC A4).
Nowy pomiar w tym runie: brak (re-kwalifikacja narracyjna na bazie odczytów) — poprawnie
zadeklarowane w raporcie executora.

### F5 („WYŁĄCZNIE" → „w prześledzonych ścieżkach"; rozliczenie 15/26) — CONFIRMED z poprawką QC-3
- Predykat qc_b2_exclusive.py (odczyt własny): body_of = pętla do 3×CC (linie 45-52) —
  **heurystyka granic ciała, nie trace provenance** ✓; ATTR_FUNCS zawiera writer
  FUN_00845F70 (linia 18) ✓ — opis SE-5 zgodny z kodem RUN4 QC.
- **26 site'ów ctor FUN_00730700 w 24 funkcjach** (mój census E8 = 26 ✓; Ghidra
  attribution: FUN_00447630 ×2, FUN_0050E490 ×2 ✓ — oba dwo-site'owe ciała
  potwierdzone własnym wyznaczeniem końca); **5 funkcji z setterami, 19 bez** —
  mój własny scan ciał (własne granice): with_setters = {0x447630, 0x459270,
  0x567770, 0x67bc90, 0x67ccd0} — **identyczna lista 5 funkcji co SE-8** ✓; 19 bez
  setterów + pełna lista VA = zgodna z moim census ✓ (lista SE-8 = mój wynik).
- **15 setter-callerów f90:** 15 siteów/15 funkcji ✓ (Ghidra + moje granice). Grupy —
  patrz QC-3 (P2): 9 bezpośrednich (nie 10), 3 czysto parametryczne, 3 singleton-readers.
- Adiustacja 4 spornych startów (własne prologi): 0x00447630 ✓ (pełny SEH), 0x004C47F0 ✓,
  0x0046E790 ✓, 0x00567770 ✓; 0x00567170 ✓ (55 8B EC 83 E4 F8 6A FF — z frame pointer,
  stąd „seh_prologue:false" u executora); **granica 0x00567170/0x00567770 = blob danych
  bez paddingu CC (0x0056775C-0x0056776F) — źródło zlewu heurystyki 3×CC, potwierdzone.**

## 2. GA5-IMMUTABLE — PASS (własne hashowanie)
- 7 pakietów executora: **my-now == executor-before == executor-after** (composite
  SHA256, własny census): RUN1 (576 pl.), RUN2 (25), RUN3 (220), RUN4 (381), ROUND (4),
  JOIN+ERRATA_R2 (26), DESKTOP (10) — **0 zmian** ✓ (QC_GA5_IMMUTABLE.json).
- Pakiet „296445-ERRATA" z listy zlecenia = `PE_296445_NIF_ORIGIN_PLACEMENT_R1_ERRATA_R1_20260912`
  — istnieje TYLKO w repo (docs/audits/...; w 99_Audits brak katalogu): **git status
  czysty, HEAD==BASE_SHA → NIETYKALNY w tym runie** (15 pl., 176302 B; ostatni commit
  9fc5d99). Executor w GA5 censusem objął zamiast niego pakiet 99_Audits
  PE_935_CONSUMER_TRACE_CLAIMS_JOIN (zawiera ERRATA_R2.md = erratę 296445-claims) —
  transparentnie opisany w RESEARCH_FINDINGS §6; substancja GA5 (zero zmian pakietów
  historycznych) potwierdzona dla obu zbiorów (nota QC-7, P3).
- GHIDRA_LOCAL: manifesty AT_COPY (db.63/64) i SHA256 (db.67/68) — różnica wyłącznie
  w numerach .gbf, opis cyklu życia zgodny z bajtami obu manifestów (M-8 ✓).

## 3. Findings

### **[P2] QC-1: „55 rejestracji z imm32" — w istocie 54 rejestracje param-set + 1 lazy-init klasy bazowej (arg1=0)**
- **Źródło:** RESEARCH_FINDINGS §2.2 („każda z 55 funkcji woła ctor ... z imm32 jako
  arg1"), §7 („pełna lista + ID każdej rejestracji"); DRAFT_ERRATA [SE-7] („ustawiane
  imm32 w 55 funkcjach rejestracyjnych"); 01_RAW\F1_REG_ARGS.json — wpis dla call-site
  0x007262B7 z imm32=**0x00A7957B** (stała pustego stringa, nie ID klasy!).
- **Przeciw-bajty (własne):** site 0x007262B7 leży w FUN_00726230 (lazy-init singletonu
  DAT_00BA51C4): ostatni PUSH przed CALL = `6A 00` **PUSH 0** @0x007262A7 → **arg1 = 0**
  (prolog SEH ctora: 9 pushów → arg1=[ESP+0x28]). Funkcja tworzy instancję klasy
  bazowej (vtable 0x00A86850 zapisany w ctorze) z ID 0 i zapisuje do DAT_00BA51C4
  (`A3 C4 51 BA 00` @0x007262C4) — to REJESTRATOR-korzeń, nie param-set.
- **Skutek:** liczba „55 rejestracji z imm32" jest o 1 za duża; F1_REG_ARGS.json zawiera
  jeden artefaktowy wpis (imm=0x00A7957B). Twierdzenie nośne F1 (+0x28=kopia ID klasy)
  **niezależne i nietknięte** — 54 imm32 + 36/36 korelacji RTCI wystarcza.
- **Poprawka (wykonana w REPORT.md i ERRATA_R3 [SE-7]):** „55 bezpośrednich call-site'ów
  ctora = 54 rejestracje param-set z imm32 (20xxx/24xxx) + 1 lazy-init singletonu klasy
  bazowej (FUN_00726230, DAT_00BA51C4, ID 0)".

### **[P2] QC-2: trzy błędne nazwy funkcji w opisie writer'a DAT_00BA58CC**
- **Źródło:** RESEARCH_FINDINGS §2.3: „rejestracje FUN_0070E2F0(obj,8,7) @0x0073D888,
  FUN_006B6541, FUN_0072C151, FUN_0072BF11".
- **Przeciw-bajty (własne + dump własny executora F1_CTX_WRITER_DAT00BA58CC.txt
  — identyczne bajty):** cele CALL po store'u @0x0073D882 to
  **FUN_00734C40** @0x0073D892, **FUN_0070C150** @0x0073D8A0, **FUN_0070BF10**
  @0x0073D8AB. Nazw „FUN_006B6541/0072C151/0072BF11" **nie ma w żadnym pliku
  evidence** tego runu (grep po całym pakiecie — tylko RESEARCH_FINDINGS:74).
- **Skutek:** opis cyklu życia klasy w warstwie narracyjnej wskazuje nieistniejące
  w tych miejscach funkcje; twierdzenie o singletonie (writer→ctor FUN_0073AB60→store
  @0x0073D882) **niezależne i potwierdzone**.
- **Poprawka (wykonana w REPORT.md):** lista rejestracji po store'u = FUN_0070E2F0
  (thiscall (obj,8,7)), FUN_00734C40, FUN_0070C150, FUN_0070BF10; przy porażce
  wirtualny dtor slot0 z PUSH 1 + clear @0x0073D8C6.

### **[P2] QC-3: SE-6 — FUN_00567170 NIE jest „bezpośrednim czytnikiem atrybutów" (9/3/3, nie 10/4/1)**
- **Źródło:** DRAFT_ERRATA [SE-6] tabela: „bezpośrednie (10): ..., FUN_00567170, ...";
  01_RAW\F5_SEH_CLASSIFICATION.json (wpis FUN_00567170, size 2498, direct_attr_calls
  [attr-check, attr-pos-fetch, attr-triple, walker-resolve]) i F5_SETTER_ACCOUNTING.json
  (count_funcs=14 przy 15 site'ach — artefakt zlewu).
- **Przeciw-bajty (własne):** ciało FUN_00567170 kończy się @0x00567770 (następna
  funkcja z pełnym prologiem SEH; między funkcjami blob danych bez CC — stąd zlew
  heurystyki 3×CC do 0x00567B32). **W [0x00567170, 0x00567770) zero wywołań funkcji
  atrybutowych** (pełna lista ATTR z qc_b2_exclusive.py: 0x00846840/0x008492C0/
  0x00845360/0x008452D0/0x00854720/0x00843D60/0x0085B840/0x008544D0/0x00844020/
  0x00845F70); jedyne związane wywołanie = **singleton getter FUN_004154F0
  @0x00567662**. Wszystkie 4 attr-calle z wpisu klasyfikacyjnego leżą @0x005677C4+
  (ciało FUN_00567770) — **podwójne policzenie** tych samych 4 wywołań w obu wpisach.
- **Skutek:** „10 bezpośrednich" (powtórzone za RUN4 QC B2, który miał ten sam artefakt
  zlewu) jest o 1 za dużo; FUN_00567170 ma status provenance NIEROZLICZONA (singleton),
  a nie „atrybutowa (kwalifikacja RUN4 podtrzymana)". Poprawny podział 15 setter-callerów:
  **9 bezpośrednich + 3 czysto parametryczne (FUN_00459270/0043A200/00488920; provenance
  3 z 4... uwaga: FUN_005B5F90 przeniesiona) + 3 singleton-readers (FUN_005B5F90
  [provenance śledzona per RUN4 QC B2], FUN_0046E790, FUN_00567170 [provenance
  NIEROZLICZONA])** — 9+3+3=15. (FUN_005B5F90: 0 attr-callów + 1× FUN_004154F0
  @0x005B629D — własny scan.)
- **Poprawka (wykonana w REPORT.md i ERRATA_R3 [SE-6]):** tabela 9/3/3 jak wyżej;
  usunięcie „FUN_00567170 — atrybutowa".

### **[P3] QC-4: RECEIVER_MATRIX rząd 4 / RESEARCH_FINDINGS §3.2 — pin „slot3 CALL [vft+0xC] w gałęzi 0x38B0"**
- **Stan executora:** „+0 = vtable (wywołanie wirtualne slot3 `CALL [vft+0xC]` w gałęzi
  0x38B0 tego samego switcha)".
- **Własne bajty:** gałąź 0x38B0 (CMP EDI,0x38B0 @0x00855791 → JNZ @0x00855797)
  zawiera wyłącznie CALL-e bezpośrednie: FUN_00415570 @0x008557CC i FUN_008599A0
  @0x008557D3. **W całym ciele FUN_008553D0 nie istnieje instrukcja CALL [reg+0xC]**
  (pełny skan form mod8/SIB/disp32/abs). Wirtualne wywołanie NA WARTOŚCI mapy istnieje
  @0x00855B2F-3F: `8B 08` (ECX=[out]=wartość) → `8B 11` (EDX=[wartość]=vtable —
  **+0=vtable potwierdzone**) → `8B 42 08` (EAX=[vtable+8] — slot 0-based nr 2) →
  `FF D0` — w INNEJ gałęzi switcha. Jedyne CALL [vft+0xC] (@0x0085552F-3E, FF D2 po
  `8B 17 8B 52 0C`) dotyczy obiektu EDI — NIE wartości mapy.
- **Skutek:** substancja (wartość polimorficzna, +0=vtable, eliminacja „to nie rekord")
  **poprawna i bajtowo potwierdzona**; szczegół pinu (slot/gałąź) błędny. Poprawka
  wykonana w REPORT.md/ERRATA_R3 [SE-9]: „+0 = vtable — wirtualne wywołanie na wartości
  przez [vft+8] @0x00855B36-3F (inna gałąź switcha); CALL [vft+0xC] @0x0085552F dotyczy
  innego obiektu".

### **[P3] QC-5: konwencja pinów VA — pozycja operandu zamiast startu instrukcji**
- Przykłady (executor → właściwy start instrukcji, własne bajty): Container PUSH
  „@0x0073A114" → `68` **@0x0073A111**; CMP [DAT],0 „@0x0073D832" → `83 3D`
  **@0x0073D831**; CALL FUN_0070E2F0 „@0x0073D888" → `E8` **@0x0073D887**; MOV ECX,[DAT]
  w ctorze SurgeonObject „@0x0073520D" → `8B 0D` **@0x0073520C**; read-back „@0x0073D88D"
  → `A1` **@0x0073D88C**; clear „@0x0073D8C7" → `C7 05` **@0x0073D8C6**.
- Wszystkie PINY KLUCZOWE (vft-write @0x0070CFB6, store+8 @0x0070CFC1, CALL getter
  @0x00726EB7, store+0x28 @0x00726EBC, store singletonu @0x0073D882, CALL fabryki
  @0x0070BF96, CMP 0x4E38 @0x008557DD, CALL @0x008557FD, tabela @0x00855BB4,
  koincydencja @0x00516F0E) — **dokładne**. Poprawka: w REPORT/erratcie pinuję starty
  instrukcji i odnotowuję konwencję.

### **[P3] QC-6: F2_SELECTOR.json „template_4508" — mylący artefakt pierwszego przebiegu**
Podsekcja czyta rekord OD offsetu 96528 (= pozycja pola D) z etykietami pól
(A_u32_at_8=0 itd.); autorytatywne wartości są w F2_T4508_WALK.json i zgadzają się z
moim walkem. Bez wpływu na twierdzenia; odnotowane.

### **[P3] QC-7: GA5 — zbiór pakietów vs zlecenie (nota zakresowa)**
Executor censusem objął 7 pakietów 99_Audits (w tym JOIN+ERRATA_R2 = pakiet erraty
claimów 296445); pakiet „296445-ERRATA" z listy zlecenia istnieje tylko w repo i był
nietykalny per git (HEAD==BASE, status czysty). Zero zmian w obu interpretacjach
(własne pomiary). Odnotowane w REPORT.md.

## 4. Gałęzie RECEIVER_UNRESOLVED (utrzymane — granice Fazy B)
1. **Nazwa klasy wartości mapy managera parametrów** ([hit+8]; dataflow i layout
   potwierdzone własnymi bajtami; insert-do-mapy/ctor wartości/runtime — otwarte).
2. **arg1 FUN_00567C50 per-caller** (getter D @0x00567D16/D46; odbiorca [arg1+0x10]:
   stan world-object / bufor 0xB9 / handler-arg — provenance ogniw, nie typ nazwany).
3. **19 funkcji ctor-callers bez setterów** — semantyka NOT_CHECKED (lista VA = moja
   lista; zgodna z SE-8).
4. **FUN_00567170 i FUN_0046E790: provenance wartości setterów NIEROZLICZONA**
   (singleton-readerzy; kandydat: mapa managera parametrów).
5. Semantyka liczbowa D=124.941 — UNKNOWN (zgodnie z RUN4; nie ogłaszano
   „statycznej nierozstrzygalności").

## 5. NOT_CHECKED (jawne)
- Negatyw 13 kotwic po 276 payloadach .prt — pomiar RUN4 (GA5-protected; QC ROUND
  zweryfikowała); ten run odczytał metodę (s12:63 ✓ własny odczyt skryptu) i walk
  templates.vfs (własny ✓). Nie powtarzałem skanu .prt (brak nowych twierdzeń tego
  runu ponad method-claim).
- FUN_008599A0 w głębi (poza pierwszymi 0x80 B i census wywołań pośrednich — bez
  trafień vtable-slot w pierwszych 0x80 B; nie-nośne dla F1/F2).
- Ciała 36 klas Impl poza linkami ABI (vft-write + PUSH imm32 + RTTI sprawdzone dla
  wszystkich; reszta ciał nie-dekodowana).
- Ghidra nie uruchomiona przez QC (projekt LOCAL-ONLY; isCall porównane z własnym
  census E8/E9 po bajtach — pełna zgodność zbiorów: ghidra_only_not_raw = ∅,
  e8_not_in_ghidra = ∅).

## 6. FULL_READ_LOG (odczytane w całości do EOF)
pe_core.py; s0_era_assertion.py (struktura wyjścia); rc1_ga_attrs.py; rc1_refcounts.py;
ga5_immutable.py; RESEARCH_FINDINGS.md; STAGE_ACCEPTANCE_GATES.csv;
DRAFT_ERRATA_SUPERSESSION.md; RECEIVER_MATRIX.md; S0_ERA_ASSERTION.json; F1_ABI_BYTES.json;
F1_CENSUS.json; F1_REG_ARGS.json (55 wpisów); F2_SELECTOR.json; F2_T4508_WALK.json;
F2_DCLAIMS.json (struktura + klucze); F5_SETTER_ACCOUNTING.json; F5_SEH_CLASSIFICATION.json;
F1_CTX_WRITER_DAT00BA58CC.txt; GHIDRA_REFCOUNTS.json (listy isCall — pełna
konfrontacja); GHIDRA_FUNC_ATTR.json (atrybucje ctor/f90); QC-b2_exclusive.py (RUN4,
odczyt); s12_prt_content_check.py (RUN4, odczyt). Historyczne (READ-ONLY): ERRATA_R2.md
(JOIN, nagłówek+§0), ZS1_PSEUDO_008553D0.txt (RUN4, regiony linii 318-662),
ROUND_REPORT/RUN3/RUN4 cytaty — weryfikowane przez grep + odczyt wskazanych linii.

## 7. Struktura twierdzeń osobno (rozdzielenie statusów)
- Claim-status: F1/F2/F3 CONFIRMED (własne bajty); F4 re-kwalifikacja zgodna;
  F5 CONFIRMED z poprawką QC-3.
- Finding-disposition: Desktop F1–F5 przyjęte z korektami; errata SUPERSESSION
  uzasadniona bajtowo.
- Gate-result: GA1-GA6 executora = PASS/PASS_WITH_BOUNDARY zgodnie z moimi pomiarami;
  bramki QC: patrz §8.
- Persistence/publikacja: Faza 2 (niniejszy dokument + REPORT/ERRATA/HANDOFF +
  commit path-limited).
- Application readiness / milestone closure: POZA zakresem QC (PE-MASTER).

## 8. Bramki QC (fail-closed)
| QC gate | predykat | wynik |
|---|---|---|
| QC-G1-ERA | oba SHA + własny PE parse + mapping | PASS (E778…, BE578…; base 0x00400000; ASLR OFF; 5 sekcji) |
| QC-G2-F1-ABI | 7 ogniw łańcucha bajt-co-bajt + prologi/pushe/args | PASS (7/7) |
| QC-G3-F1-ID | 55 census + 54 imm32 + 36/36 RTTI korelacji + 4 pary | PASS (z QC-1: 54+1) |
| QC-G4-F1-POSITIVE | parser→lookup(+0x14)→getter(ECX=rekord) + rozróżnialność | PASS |
| QC-G5-F2 | 14/14 instrukcji gałęzi + tabela 4 + bloki 2/3/4 + D-branch odrębny + walk 5438/0/EOF + D@4508 bits | PASS |
| QC-G6-CENSUS | E8/E9: 808+9=817, 116+1=117, f32 10, ctor 26/24, setters 5/19, imm32 3/2/9/9 | PASS (z QC-1/QC-3 poprawkami liczników narracyjnych) |
| QC-G7-GA5 | composite-hash 7 pakietów przed/po/teraz + repo-296445 git-clean | PASS (0 zmian) |
| QC-G8-MATRIX | 7 rzędów RECEIVER_MATRIX — każdy owocny dowód bajtowy; UNRESOLVED jawnie | PASS (z QC-4 pin-fix) |
| QC-G9-IMMUTABLE | 15 kluczowych plików evidence: hashe przed==po QC | PASS |

## 9. Wyjaśnienia dodane przez QC (przerwy liczników zamknięte)
- **808 vs 817 (getterA) i 116 vs 117 (getterD):** różnica = **tail-jumpy E9**
  (9 site'ów getterA: 0x7103C6, 0x72AC36, 0x73EC16, 0x73EEB6, 0x73F256, 0x742296,
  0x742CC6, 0x74C156, 0x8DC566; 1 site getterD: 0x7CDCCE) — wszystkie obecne na
  listach isCall Ghidra; zbiory E8=∅-rozbieżne (żadnego site'u tylko-po-jednej
  stronie). Liczby „808 raw" i „817 isCall" obie poprawne; „wiążąca" liczba zależy
  od definicji (CALL bez tail-jump vs CALL+zakończenia ogonowe). Executor odnotował
  rozbieżność bez mechanizmu — mechanizm ustalony przez QC.
- **Stride VFS (nowa, własna):** slot = 36×ceil((16+size)/36) — kalibracja na 67
  parach (size,stride) + dokładny EOF; zgodna z „stride_base 36" z nagłówka.

## 10. Nietykalność evidence executora (hash przed==po)
15 kluczowych plików (RESEARCH_FINDINGS, GATES, DRAFT_ERRATA, RECEIVER_MATRIX,
F1_ABI_BYTES, F1_REG_ARGS, F1_CENSUS, F2_SELECTOR, F2_T4508_WALK, F2_DCLAIMS,
GA5 before/after, S0, F5_SEH_CLASSIFICATION, F5_SETTER_ACCOUNTING):
**14/15 SAME; 1/15 CHANGED-BY-ASSIGNMENT** — 06_REPORT\STAGE_ACCEPTANCE_GATES.csv
otrzymał dopisane bramki QC-G1..QC-G9 (przydział: „GA1–GA6 executora + twoje
bramki QC"); wiersze GA1–GA6 zachowane verbatim (przed-hash = stan executora);
**0 zmian nieprzewidzianych** (pełna lista: 03_EVIDENCE\QC_BEFORE_AFTER_HASHES.txt).
QC dodał wyłącznie nowe pliki (qc_probe\*.py, 03_EVIDENCE\*.json/md) oraz finalne
06_REPORT (REPORT.md, ERRATA_R3.md, HANDOFF.md, artifact_index.csv) i
MANIFEST_SHA256.csv w korzeniu — wszystko w warstwie przydzielonej auditorowi.

## 11. Artefakty QC (03_EVIDENCE + 00_CONTROL\qc_probe)
qc_core.py; qc_f1_abi.py→QC_F1_ABI.json; qc_f1_classid.py→QC_F1_CLASSID.json;
qc_f1_regargs2.py→QC_F1_REGARGS2.json; qc_f1_regargs3.py→QC_F1_REGARGS3.json;
qc_f1_dat58cc_poscontrol.py→QC_F1_DAT58CC_POSCONTROL.json;
qc_f2_selector.py→QC_F2_SELECTOR.json; qc_f2_vfs.py→QC_F2_VFS_WALK.json (+ QC_F2_VFS_WALK2.json);
qc_census_getters.py→QC_CENSUS_GETTERS.json; qc_f5_setters.py→QC_F5_SETTERS.json;
qc_ga5.py→QC_GA5_IMMUTABLE.json; qc_matrix_links.py→QC_MATRIX_LINKS.json;
qc_final_links.py→QC_FINAL_LINKS.json; QC_F1_CLASSID_PAIRS.md; niniejszy QC_REPORT.md.
