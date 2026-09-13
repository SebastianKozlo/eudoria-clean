# ERRATA_R3 — SUPERSESSION LEDGER
## RUN: PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913

**RUN_CLASS:** LOAD_BEARING (rozstrzygnięcie 5 findingsów audytu Desktop własnymi
próbkami bajtowymi + errata supersession). **ERA:** EU 9.3.5 (pcg_install).
**Executor:** pe-reconstruction; **INTERNAL_QC + formalizacja + publikacja:**
pe-master-auditor (QC_PASS; 03_EVIDENCE\QC_REPORT.md; poprawki QC-1..QC-7 włączone
poniżej jawne). **TRYB:** STATIC-ONLY.
**Binarium:** Entropia.exe SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
(8015872 B, image base 0x00400000, ASLR OFF). templates.vfs SHA256
BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77 (560788 B).

**ZASADY:**
1. Historyczne pakiety są NIETYKANE (GA5: composite-hash przed/po — identyczne;
   własny census QC 7 pakietów + repo-296445 git-clean). Errata CYTUJE oryginały
   verbatim (plik:linia) — poprawiona treść żyje TUTAJ i w 06_REPORT\REPORT.md.
2. Kolejność wiążącości: (a) evidence 01_RAW/03_EVIDENCE (nietknięte), (b) amendments
   (QC) w ROUND, (c) NINIEJSZA ERRATA_R3 (kwalifikuje narracje ROUND/RUN3/RUN4/RUN2),
   (d) raporty historyczne w miejscach skonfliktowanych — czytane przez pryzmat (c).
3. Żadne twierdzenie nie ogłasza STATIC_INSTANCE_MECHANISM_CONFIRMED ani źródła
   placementu; RECEIVER_UNRESOLVED pozostaje jawną granicą (Faza B).
4. **MANIFEST_VALIDATION_ORDER** (jawna reguła): ostatni poprawny manifest w czasie
   jest WIĄĄCY DLA PLIKÓW, KTÓRE POKRYWA; zamknięcie (closure manifest) jest
   wiążące dla plików, które pokrywa; rozbieżności wcześniejszych manifestów wobec
   plików, których już nie opisują, są klasy DOKUMENTACYJNEJ (nie integralnościowej).
   Konkrety: manifest GHIDRA_LOCAL pakietu RUN4 opisywał stan PRZED turami ZS
   (db.52/53 → nadpisane przez db.63/64 w publikacji RUN4; integrity pakietu RUN4 =
   closure manifest 49/49); kopia GHIDRA_LOCAL w TYM runie przeszła własny cykl
   (db.63/64 → db.67/68 po 2 turach analyzeHeadless; manifest finalny
   00_CONTROL\GHIDRA_LOCAL_MANIFEST_SHA256.csv, manifest stanu- przy-kopiowaniu
   GHIDRA_LOCAL_MANIFEST_AT_COPY.csv) — rozdzielenie manifestów eliminuje błąd
   pojedynczego-stale-manifestu.
5. Piny VA w tej erracie = START instrukcji (opcode); tam gdzie raport historyczny
   pinował pozycję operandu, odnotowano to jawnie (patrz [M-3]/[M-4]/QC-5).

---

## CZĘŚĆ A — F1: receiver provenance wspólnego gettera

### [SE-7] Most „templates.vfs.A → ArkObject+0x28" — REJECTED_WITH_EVIDENCE (oba ogniwa)

- **STARE** (RUN3 REPORT.md:13-15, pakiet PE_935_STATIC_INSTANCE_TRACE_R1_20260913):
  > „**Encja**: `ArkObject` (ctor `FUN_00726e70` @0x00726E70) przyjmuje **obiekt template'u** i getterem A (`FUN_007ce1e0` = `[ECX+0x08]`, adres-zablokowany w poprzednim runu) zapisuje **A (id pliku .nif) do encji @+0x28**."
- **STARE** (RUN3 REPORT.md:16): > „Istnieje 40 call-site'ów ctora — fabryki per klasa (np. ctor `ArkSurgeonObject` `FUN_007351e0` z globalnym template'm `DAT_00ba58cc`)."
- **STARE** (RUN3 REPORT.md:18): > „**To jest most template→encja statycznej**: definicja (template) jest osobna od instancji (ArkObject)..."
- **NOWA KWALIFIKACJA:** Most NIE istnieje w obu ogniwach. (i) Fabryka (vtable
  0x00A86850 slot1 = FUN_0070BF50) przekazuje jako PIERWSZY argument ctora **własny
  this = instancję ArkObjectClass** (PUSH ESI jako ostatni push przed CALL), nie rekord
  template'u. (ii) Ctor czyta **[class+8]** i zapisuje wynik do **encji@+0x28**; a
  **[class+8] = numeryczne ID klasy (param-set)** ustawiane imm32 w rejestracjach, NIE
  pole A rekordu templates.vfs. **ArkObject+0x28 = kopia identyfikatora klasy**
  (np. 20035 Surgeon; 20030 Container), nie „A (id pliku .nif)". Ilościowo: ctor
  ArkObjectClass ma 55 bezpośrednich call-site'ów (Ghidra isCall + raw-E8; „40" =
  niedoliczenie), w tym **54 rejestracje param-set z arg1=PUSH imm32 (rodzina
  0x4E20..0x4E4B + 0x5DC2..0x5DD1, każda wartość dokładnie 1×) oraz 1 lazy-init
  singletonu klasy bazowej (FUN_00726230 → DAT_00BA51C4, arg1 = PUSH 0, ID 0)**
  [poprawka QC-1: „każda z 55 z imm32" było o 1 za dużo]. Fabryka: 0 bezpośrednich
  CALL (wyłącznie dispatch wirtualny). Istnieje most „class-ID → encja@+0x28"
  (kopia identyfikatora klasy do instancji), nie „templates.vfs.A → +0x28".
- **ŹRÓDŁO:** własne bajty: fabryka `51 56 8B C8` @0x0070BF92-95 + CALL @0x0070BF96
  → 0x00726E70; ctor klasy prolog SEH (9 pushów) → MOV EBP,[ESP+0x28] @0x0070CFAB
  (arg1) → vft `C7 06 50 68 A8 00` @0x0070CFB6 → **`89 6E 08` @0x0070CFC1**;
  ctor ArkObject prolog (8 pushów) → MOV EBX,[ESP+0x24] @0x00726E96 (arg1) → vft
  0x00A86B48 @0x00726EA1 (RTTI `.?AVArkObject@@`) → [obj+4]=EBX @0x00726EA7 →
  **MOV ECX,EBX + CALL FUN_007CE1E0 @0x00726EB7 + `89 46 28` @0x00726EBC**;
  census E8→0x0070CF80 = 55 (identyczny Ghidra isCall), 54×PUSH imm32 + 1×PUSH 0
  (F1_REG_ARGS.json + QC_F1_REGARGS2.json); korelacja mangling↔imm32 **36/36**
  (reguła: `$0` + nibble A=0..P=15; QC_F1_CLASSID_PAIRS.md).
- **KONTRTEST:** kontrola pozytywna odtworzona bajtowo — dla rekordu templates.vfs:
  parser `89 47 08` @0x00730CE6 → rejestr RB (lookup FUN_0072F580: rb-find
  FUN_004D1430 @0x72F590; **hit → `83 C0 14` @0x72F59E** = rekord@hit+0x14; miss →
  0x00BA5800) → FUN_006C3F50: lookup @0x006C3F62 → **CALL getter @0x006C3F74 z
  ECX=EDI(rekord)** → para {0x66=MODEL, A}. Ten sam stub `8B 41 08 C3` odczytuje
  +8 = A (id NIF) TYLKO na rekordzie z lookupu (dataflow ECX; brak vtable), a na
  klasie odczytuje +8 = ID klasy (imm32; RTTI `.?AVArkObjectClass@@`) — RTTI+vft+
  dataflow ROZRÓŻNIAją oba typy odbiorców.

### [SE-7a] DAT_00ba58cc — „globalny template" → singleton klasy (poprawka QC-2 w opisie rejestracji)

- **STARE:** (RUN3 REPORT.md:16 — cyt. wyżej; „globalny template'm `DAT_00ba58cc`").
- **NOWA KWALIFIKACJA:** **DAT_00BA58CC = singleton klasy
  ArkObjectClassImpl<ArkSurgeonObject, 20035>** (deskryptor klasy), NIE rekord
  template'u i NIE dane placementu. Writer = FUN_0073D810 (lazy-init): CMP
  [0x00BA58CC],0 @0x0073D831 → new(0x118) → ctor FUN_0073AB60 (Impl Surgeon: PUSH
  0x4E43 + vft 0x00A87034) → **store `A3 CC 58 BA 00` @0x0073D882** → rejestracje
  (thiscall FUN_0070E2F0 z (obj,8,7) @0x0073D887; potem FUN_00734C40 @0x0073D892,
  FUN_0070C150 @0x0073D8A0, FUN_0070BF10 @0x0073D8AB); przy porażce wirtualny dtor
  slot0 (PUSH 1) + clear @0x0073D8C6. Census imm32 0x00BA58CC w .text = 9, wszystkie
  w cyklu życiowym klasy (init-check/store/read-back/3×MOV ECX/clear/accessor
  FUN_0073C970/ load w ctorze ArkSurgeonObject @0x0073520C).
  **[Poprawka QC-2]:** nazwy „FUN_006B6541, FUN_0072C151, FUN_0072BF11" z
  RESEARCH_FINDINGS §2.3 tego runu jako funkcje wołane po store'u są BŁĘDNE (nie
  istnieją w evidence; cele z bajtów: FUN_00734C40/0070C150/0070BF10) — poprawione
  w 06_REPORT\REPORT.md; evidence 01_RAW nietknięte.
- **ŹRÓDŁO:** własny census imm32 (9 trafień; QC_F1_DAT58CC_POSCONTROL.json) + dump
  writer'a (zgodny bajt-co-bajt z F1_CTX_WRITER_DAT00BA58CC.txt executora).
- **KONTRTEST:** accessor FUN_0073C970 = `A1 CC 58 BA 00; C3` (zwraca singleton klasy);
  ctor ArkSurgeonObject FUN_007351E0 ładuje [DAT_00BA58CC] i przekazuje PUSH ECX jako
  arg1 base-ctora (CALL FUN_00726E70 @0x00735216) — klasa jako pierwszy argument, nie
  rekord VFS.

---

## CZĘŚĆ B — F2: „konsument D"

### [SE-9] Selektor wariantów w FUN_008553D0 czyta +8 wartości mapy, nie D@+0x10

- **STARE** (Z4_field_d.md:31-32, pakiet PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913):
  > „FUN_008553d0 (konstruktor-walker: `fStack_50 = (float)FUN_0048ada0()`; **w gałęzi 0x4e38 odczyt D steruje mapowaniem local_60: 4/5→2, 6→3, 7→4!**)"
- **STARE** (Z4_field_d.md:47-49): > „FUN_008553d0: D steruje **wyborem wariantu konstrukcji** (mapowanie 4/5→2, 6→3, 7→4 w gałęzi param-setu 0x4e38) i trafia do FUN_00415570/FUN_008599a0 jako jeden z argumentów inicjalizacji obiektu."
- **STARE** (RUN4 REPORT.md:123-124): > „FUN_008553d0 (konstruktor-walker): D steruje selekcją wariantu (gałąź 0x4e38: D=4/5→2, 6→3, 7→4) i trafia do inicjalizacji obiektu;"
- **STARE** (RUN4 QC_REPORT.md:85, B10): > „gałąź param-setu: `CMP EAX,0x4E38` @0x008557DB → selekcja wariantu przez `LEA EAX,[ESI-4]; CMP EAX,3; JMP [EAX*4+0x00855BB4]` (tablica indeksowana D−4; widoczne w bajtach: slot 6→3, 7→4) ✓ — zgodne z claimem „D=4/5→2, 6→3, 7→4"."
- **NOWA KWALIFIKACJA:** **ARYTMETYKA** mapowania jest prawdziwa, ale **ŹRÓDŁO
  selektora jest błędne** [status: REJECTED_AS_ATTRIBUTED]. W gałęzi 0x4E38
  (`CMP EAX,0x4E38` @0x008557DD; pin „@0x008557DB" w QC B10 był off-by-2):
  CALL walker-current FUN_0085B860 @0x008557F1 → **MOV ECX,[EAX] @0x008557F6
  (ECX = wartość [hit+8] mapy managera parametrów)** → **CALL FUN_007CE1E0
  (+8) @0x008557FD** → LEA EAX,[ESI−4]; CMP EAX,3; JA default; JMP
  [EAX*4+0x00855BB4]. Tabela 0x00855BB4 (4 wpisy): [0]=0x00855834, [1]=0x00855834,
  [2]=0x00855820, [3]=0x0085582A; bloki `MOV [ESP+0x1C],2/3/4` → mapowanie
  v=4,5→2; 6→3; 7→4. **Getter D FUN_0048ADA0 @0x008556DF leży w INNEJ gałęzi tego
  samego switcha** (ten sam wzorzec walker→MOV ECX,[EAX], odczyt +0x10 tego samego
  typu odbiorcy) — NIE zasilą selektora. Dekompilat ZS1 (linie 203-216) już
  pokazywał `uVar13 = FUN_007ce1e0(); switch(uVar13)` — claim Z4 §2-3 był sprzeczny
  z własnym artefaktem RUN4.
- **ŹRÓDŁO:** własny dekod 14/14 instrukcji gałęzi + tabela + bloki
  (QC_F2_SELECTOR.json); resolver FUN_008544D0: lock mgr+0x44, mapa mgr+0x10, rb-find
  FUN_00971780, **`8B 70 08` MOV ESI,[EAX+8] @0x008544F9** = wartość=[hit+8];
  walker FUN_0085B860: *out=[walker+0]; lock FUN_0085B190 gdy [v+4]≠0.
- **KONTRTEST:** wywołanie wirtualne NA WARTOŚCI potwierdza, że wartość jest
  polimorficzna: `8B 08` (ECX=[out]=wartość) → `8B 11` (EDX=[wartość]=**vtable@+0**)
  → `8B 42 08` (EAX=[vtable+8]) → `FF D0` @0x00855B2F-3F — **w INNEJ gałęzi switcha**
  [poprawka QC-4: szczegół „slot3 CALL [vft+0xC] w gałęzi 0x38B0" był błędnym
  pinem — w gałęzi 0x38B0 są wyłącznie CALL-e bezpośrednie (FUN_00415570 @0x008557CC,
  FUN_008599A0 @0x008557D3); jedyne CALL [vft+0xC] w FUN_008553D0 @0x0085552F-3E
  dotyczy innego obiektu (EDI), nie wartości mapy]. Eliminacje wartości: NIE rekord
  VFS (vtable@+0; rekordy bez vtable); NIE klasa pochodna ArkObject/ArkParameter*
  (ctor-y wołają FUN_00726E70 z globalnym wskaźnikiem klasy ⇒ +4=nie-null ptr klasy,
  +8=początek CRITICAL_SECTION — sprzeczne z nullable-lock@+4 i small-int@+8); NIE
  ArkObjectClass (+8=ID 20000+ ≠ 4..7). Nazwa klasy wartości = RECEIVER_UNRESOLVED.

### [SE-10] Queue-push FUN_00567B40 — pole i odbiorca

- **STARE** (Z4_field_d.md:29-30): > „**FUN_00567c50 ×2** (0x005681BD-region: `uVar6 = FUN_0048ada0()` przed FUN_00567b40 — **D przekazywane do capacity-push!**) i FUN_0058db50;"
- **STARE** (Z4_field_d.md:44-46): > „FUN_00567c50: `uVar6 = FUN_0048ada0()` (D bieżącego rekordu) → FUN_00567b40 (push do kolejki update z capacity [obj+0x40..0x60] — **D wpływa na priorytet/flagę wpisu kolejki**, bo ten sam obiekt czyta też pola +0x48/+0x50/0x54/0x58/0x5c/0x60)."
- **NOWA KWALIFIKACJA:** Struktura **PARTIAL**: FUN_00567C50 woła getter D ×2 przed
  pushami (@0x00567D16 → push @0x00567D24; @0x00567D46 → push @0x00567D54; 3. call
  @0x00567F72 na this) i wynik jest argumentem FUN_00567B40 — potwierdzone. ALE:
  (a) odbiorca getterów D = **[arg1+0x10]**, gdzie arg1 = pierwszy argument stosowy
  (`MOV ESI,[ESP+0xEC]` @0x00567C93; `MOV ECX,ESI` przed CALL) — to NIE jest
  dowiedziony rekord templates.vfs (provenance per-caller: FUN_0058DB50 → stan
  world-object; FUN_005B72C0 → bufor komunikatu 0xB9; FUN_00514EF0 → argument
  handlera; **RECEIVER_UNRESOLVED per caller**); (b) sama bramka pusha czyta
  **[singleton_0x00BA1260+8] getterem A** (CALL FUN_004143F0 @0x00567B49 → MOV
  ECX,EAX → CALL FUN_007CE1E0 @0x00567B50) i porównuje z FUN_00844130(arg) —
  flaga równości (→ 5. argument FUN_00567170), nie D template'u. Zdanie „D wpływa
  na priorytet/flagę" zastąpić: „argument [arg1+0x10] trafia do kolejki update;
  flaga gate pochodzi z porównania [singleton+8] vs FUN_00844130(arg)".
- **ŹRÓDŁO:** F2_DCLAIMS.json + własne bajty (wszystkie CALL-e zweryfikowane).
- **KONTRTEST:** różnica gate vs argument — dwie różne wartości z dwóch różnych
  odbiorców (singleton vs arg1) w tej samej funkcji kolejki.

### [SE-11] Pola D — per-konsument zamiast zbiorczej semantyki; censusy

- **STARE** (Z4_field_d.md:51-56, §3): > „**Granica (jawna)**: nie znaleziono JEDNEJ jednoznacznej semantyki — D jest parametrem MULTIPLE-consumer: (a) selektor wariantu (FUN_008553d0), (b) argument kolejki update (FUN_00567b40), (c) wartość distans/LOD (FUN_00861390). Dla template'u 4508 (D=124.941 ≈ 125): wielkość/promień/level — nie da się rozstrzygnąć statycznie bez runtime (etykieta: RUNTIME-UNOBSERVED dla konkretnej wartości 124.941; STATIC-PROOF dla konsumentów)."
- **STARE** (ROUND_REPORT.md:261): > „| 5 | **Pole D (124.941 przy 4508)** | runtime (semantyka liczbowa: promień/level/selektor wariantu — statycznie nierozstrzygalne, G4 boundary) | gettery VA-locked; semantyka RUNTIME-UNOBSERVED |"
- **NOWA KWALIFIKACJA (per konsument, z odbiorcą):**

  | claim konsumenta | status | odbiorca / poprawka |
  |---|---|---|
  | (a) selektor wariantu 0x4E38 | **REJECTED_AS_ATTRIBUTED** ([SE-9]) | selektor = +8 wartości mapy parametrów (getter A), nie D@+0x10 |
  | (b) argument kolejki update | **PARTIAL** ([SE-10]) | [arg1+0x10] przekazywane do pusha ✓; odbiorca ≠ dowiedziony rekord template'u; flaga gate = [singleton+8] vs FUN_00844130 |
  | (c) distans/LOD FUN_00861390 | **CENSUS-CONFIRMED** | 2 site'y gettera D-f32 @0x00861B49/0x00861EEB; pełny census D-f32 = **10** callerów |
  | FUN_00468910 ×5 „update world-objectu" | **UNDERCOUNT** | census: **12** site'ów gettera D w FUN_00468910 (0x00468D88, 0x00468DA4, 0x004692BC, 0x004692D7, 0x004692F2, 0x0046930D, 0x004694BE, 0x004694D9, 0x004694F0, 0x00469A7D, 0x00469AF0, 0x00469B0D); spot-check 0x00468D88: odbiorca = **lokalny rekord @ESP+0x1C** (LEA ECX,[ESP+0x1C] @0x00468D84) — dla rekordu placementu +0x10 = trzecia składowa vec3 pozycji (Z), nie D template'u |
  | census D-dword 116 (QC B10) | **AUTHORITATIVE 117** | Ghidra isCall = 117 (raw-E8 = 116 + 1 tail-jump E9 @0x7CDCCE — mechanizm rozbieżności ustalony przez QC; zbiory zgodne) |
  | wartość 124.941 przy 4508 | **ZWERYFIKOWANA, semantyka UNKNOWN** | własny walk: record 4508 @file 96496 (size 28, CRC 0xAFF5797C OK), **A=296445** @96516 (=record+0x14), B=296446, C=0, **D bits 0x42F9E1CB @96528 = f32 124.94100189208984**, E=0, F=0 |
  Zdanie „statycznie nierozstrzygalne" zastąpić: „semantyka liczbowa 124.941 **nie
  została dotąd rozstrzygnięta** (nie ogłaszano nierozstrzygalności z zasady);
  ANCHORS_ABSENT_SEMANTICS_OPEN".
- **ŹRÓDŁO:** własne censusy (E8/E9: 808+9=817 getterA; 116+1=117 getterD; 10 f32;
  12 w FUN_00468910 — QC_CENSUS_GETTERS.json) + własny walk templates.vfs
  5438/0-CRC/EOF (QC_F2_VFS_WALK2.json; reguła stride: slot=36×ceil((16+size)/36),
  kalibracja 67 par size/stride).
- **KONTRTEST:** lista 12 site'ów = własny census (zgodna z listą executora co do
  VA); rozróżnienie rekord-lokalny vs template w FUN_00468910 przez LEA ECX,[ESP+0x1C]
  (stack) — ten sam offset +0x10, inna rola niż D template'u.

---

## CZĘŚĆ C — F3: negatywy bajtowe i anomalia 20006

### [SE-1] „pliku-placementów brak" → ANCHORS_ABSENT_SEMANTICS_OPEN

- **STARE** (ROUND_REPORT.md:48): > „Kanał FILE: infrastruktura istnieje (store "Data\Parameters" FUN_0094dfc0/FUN_0094fe00 + parsery VFS), ale **pliku-placementów brak** (Portals.bnt/.prt = czysty dPVS cell-graph — 276/276, 0 duplikatów, 0 anchorów na WSZYSTKICH offsetach per QC; 20006.vfs nie istnieje mimo dokładnie 29 imm32 0x4E26 w .text)."
- **STARE** (RUN4 REPORT.md:30): > „brak lokalnego pliku-placementów statyków (Portals.bnt/.prt — patrz pkt 3: czysty cell-graph dPVS; census Data\Parameters: 27 plików .vfs parametrów, **20006.vfs nie istnieje** mimo 29 użyc ID 20006 w .text; 20xxx.vfs nie rozstrzygnięte jako nośnik transformów statyków — szew parser→drzewo nie domknięty)."
- **STARE** (RUN4 QC_REPORT.md:64): > „**Brak pliku-placementów udowodniony** na powierzchni censused: Parameters zawiera wyłącznie .vfs parametrów (żaden nie jest plikiem placementów statyków — rozstrzygnięcie H1 pozostaje „bez pozytywu", uczciwie)..."
- **NOWA KWALIFIKACJA:** Negatyw bajtowy ma zakres dokładnie zadeklarowany: w
  przebadanych nośnikach (276 payloadów .prt; 27 plików .vfs w Data\Parameters; brak
  pliku 20006.vfs) **nie znaleziono 13 wskazanych kotwic LE32 na żadnym offsecie**
  (metoda: `payload.find` po WSZYSTKICH offsetach — s12_prt_content_check.py:63,
  odczytane przez ten run i QC; odrębny census u32 aligned-only @L69). Wynik:
  **ANCHORS_ABSENT_SEMANTICS_OPEN** — brak kotwic o zadeklarowanym zakresie NIE
  wyklucza: (a) kodowań pochodnych (schemat/indeksy/nazwy/pola innej szerokości/
  kompresja/wyliczanie), (b) pełnej gramatyki żadnego z 27 plików .vfs (20xxx.vfs
  NIE zdekodowane formatowo — jawne od RUN4; własny walk templates.vfs 5438/5438
  potwierdza kompletność rekordów, nie semantykę), (c) łańcucha konsumentów (szew
  parser→insert-map otwarty; wartość mapy [hit+8] = RECEIVER_UNRESOLVED).
  **„27 plików" ≠ „27 rodzin formatu"** — count plików nie jest censusem gramatyk.
- **ŹRÓDŁO:** s12 (odczyt metody — potwierdzony przez QC) + własny walk templates.vfs
  (5438 rekordów, 0 CRC-fail, EOF=560788 dokładnie; 73 różne size payloadów).
- **KONTRTEST:** własny walk z własną regułą stride dochodzi DOKŁADNIE do EOF
  (5438) — negatyw „brak pliku 20006.vfs" jest realny, a jego zakres zgodny z
  deklaracją; brak kotwic w .prt (pomiar RUN4, GA5-protected) + brak 20006.vfs nie
  przesądzają kodowań pochodnych (semafor otwarty).

### [SE-2] Anomalia 20006/0x4E26 — co brak pliku dowodzi, a czego nie

- **STARE** (ROUND_REPORT.md:48 — cd. cytatu [SE-1]).
- **NOWA KWALIFIKACJA:** Brak pliku 20006.vfs **nie dowodzi** (i nie wyklucza):
  źródła sieciowego param-setu 20006, tożsamości „nazwa pliku = ID param-setu", ani
  tego, że wartości 20006 pochodzą z kanału runtime. Co ten run DODAŁ merytorycznie:
  **0x4E26 (20006) jest numerycznym ID KLASY ArkObjectClassImpl<ArkParameterCommon,
  20006>** — rejestracja: PUSH 0x4E26 @0x0073B871, CALL ctor @0x0073B87D (funkcja
  0x0073B820), vft 0x00A870C4 @0x0073B89B, RTTI `.?AV?$ArkObjectClassImpl@VArkParameterCommon@@$0EOCG@@@`
  (dekod $0EOCG: E=4,O=14,C=2,G=6 → 0x4E26) — dokładnie tak samo jak 20035 dla
  ArkSurgeonObject i 20030 dla ArkParameterContainer. Rodzina ID 20xxx/24xxx w
  .text to **identyfikatory klas/param-setów rejestrowane w kodzie** — pliki VFS
  są jednym z możliwych nośników zasilania, a nie samymi definicjami klas. Granica
  (kto ZASILA klasę 20006 danymi): pozostaje otwarta.
- **ŹRÓDŁO:** QC_F1_CLASSID_PAIRS.md (reguła manglingu + 4 pary, w tym ArkParameterCommon).
- **KONTRTEST:** korelacja mechaniczna 36/36 (mangling↔imm32, 0 rozbieżności) —
  reguła dekodowania zastosowana uniform na całej rodzinie, nie tylko na 20006.

### [SE-3] RUN2 D3 — „w OBU ekosystemach client-side" wymagało pozytywu dla WAR

- **STARE** (ROUND_REPORT.md:99): > „DoL/WarEmu create-object (D1/D2a/D3) | **CONFIRMED z kodu** | F_CREATE_STATIC=0x71 (WarEmu, verbatim) i create-family DoL tworzą INTERAKTYWNE encje serwerowe (drzwi/questy/loot; GameObject:Unit z rodzeństwem Door/Item/PQuestObject/...); **w OBU ekosystemach statyczne miasta są CLIENT-SIDE (DAoC: fixtures.csv)**."
- **NOWA KWALIFIKACJA:** Macierz D3 (CLAIMS_MATRIX.md:34, RUN2 — odczytana, verbatim)
  mówi z kodu WarEmu: F_CREATE_STATIC tworzy **interaktywne obiekty DB-driven**
  (drzwi/loot/questy) i „nie pokazuje żadnej ścieżki komponowania/transmitowania
  statycznej geometrii miasta". To jest NEGATYW (brak dowodu ścieżki serwerowej) —
  **nie dodatni dowód client-side dla WAR**. Pozytywny dowód client-side istnieje
  TYLKO dla DAoC (fixtures.csv — wiersze B1–B6). Poprawne zdanie: „w DAoC statyczne
  miasta są client-side (fixtures.csv — CONFIRMED z kodu); dla WAR kod WarEmu nie
  pokazuje serwerowej ścieżki statycznych miast (NEGATYW) — twierdzenie o client-side
  w OBU grach wymagało dodatniego dowodu dla WAR, którego macierz nie dostarcza.
  Nie przenosić tego wniosku na EU935."
- **ŹRÓDŁO:** odczyt CLAIMS_MATRIX.md D3 (RUN2, verbatim — pakiet nietyknięty);
  ROUND_REPORT §3 (cytowane).
- **KONTRTEST:** macierz RUN2 (nietknięta) sama nie zawiera pozytywu WAR — zdanie
  ROUND L99 agregowało dwa różne statusy (CONFIRMED DAoC + NEGATYW WAR) do jednego
  „CONFIRMED z kodu" dla obu.

---

## CZĘŚĆ D — F4: 0/38

### [SE-4] „statyki NIE przechodzą przez te call-site'y"

- **STARE** (ROUND_REPORT.md:44): > „**0/38 STATIC_WORLD** — tylko avatar/UI/maszyna/vegetation (RUN3); **statyki NIE przechodzą przez te call-site'y**."
- **STARE** (RUN3 REPORT.md:46): > „Ważny wynik negatywny: **NO_STATIC_CONSUMER_FOUND** na censurowanej powierzchni 25 lookupów + 13 pumpów (pkt 2) — **statyczne budynki NIE przechodzą przez żaden z tych call-site'ów w sposób placement-driven**; redirect na system ArkObject + atrybuty + CWO."
- **STARE** (Z2_CLASSIFICATION_TABLE.md:62, RUN3): > „4. Redirect: jeżeli statyki ładują modele, to NIE przez te 38 call-site'ów — kandydatem jest system ArkObject (ctor pobiera A z obiektu template → +0x28) + podsystem wizualny 0x006Cxxxx (FUN_006cd850/cd820/cdd80) + system atrybutów (Z4)."
- **NOWA KWALIFIKACJA:** Prawdziwy zakres negatywu: **na censurowanej powierzchni
  25 lookupów + 13 pumpów nie zidentyfikowano żadnego call-site'u z DOWIEDZIĄ
  DEDYKOWANEJ KLASY STATIC_WORLD (0/38)**. Klasyfikacja dzieli funkcje wg ROLI
  funkcji (AVATAR_EQUIPMENT / MODEL_MACHINERY / OTHER / UNKNOWN...), **a nie wg
  dowiedzionej klasy obiektów wejściowych** — klasyfikacja MODEL_MACHINERY/OTHER
  nie jest wykluczeniem, że statyki używają tych samych wspólnych funkcji
  (cross-role-function). W szczególności: `FUN_00567170` (rejestracja derived-record;
  „mechanizm WYSOKA, czy obsługuje statyki — NIEROZSTRZYGNIĘTE"), `FUN_005B5F90`
  („WYSOKA (mechanizm), NISKA (rola)"), `FUN_006CB6F0` (MODEL_MACHINERY, **twórca
  instancji modelu**) — pozostają **wspólnymi kandydatami**: ich użycie przez
  statyki jest nierozstrzygnięte, nie wykluczone. Nawias Z2:62 „(ctor pobiera A z
  obiektu template → +0x28)" jest błędny — patrz [SE-7]: ctor kopiuje **[class+8] =
  ID klasy**, nie A rekordu. Negatyw 0/38 STATIC_WORLD sam w sobie potwierdzony
  (RUN3 + QC A4) — bez zmian.
- **ŹRÓDŁO:** Z2_CLASSIFICATION_TABLE.md (odczyt); RECEIVER_MATRIX (ten run);
  QC_F5_SETTERS.json.
- **KONTRTEST:** klasyfikacja per-FUNKCJA nie dowodzi per-KLASA-DANYCH —
  cross-role-function jest jawnym modelem (fun. wspólne); dowiedzioną DEDYKOWANĄ
  rolę STATIC_WORLD miało by call-site przypisany wyłącznie statykom — żaden taki
  nie został zidentyfikowany na censurowanej powierzchni.

---

## CZĘŚĆ E — F5: „WYŁĄCZNIE z drzewa atrybutów"

### [SE-5] Kwantyfikator „WYŁĄCZNIE"

- **STARE** (ROUND_REPORT.md:31-32): > „instancja statyczna = rekord placementu z transformami czytanymi **WYŁĄCZNIE z drzewa atrybutów** + instancja modelu przez resource-system + system CWO/ArkObject; templates-lookup NIE jest ścieżką statyków (0/38 — tylko avatar/UI)."
- **STARE** (RUN4 REPORT.md:18-20): > „1. **Transform wchodzi do rekordu placementu WYŁĄZNIE z drzewa atrybutów encji** (FUN_00846840: switch atrybutów 0x6A4/0x6A5/0x6A8/0x6A9; + FUN_00854720 trójka +0x68/+0x6c/+0x70...)."
- **STARE** (RUN4 QC_REPORT.md:27, B2): > „**„Transformacje czytane WYŁĄCZNIE z drzewa atrybutów"** + alternatywne ścieżki zapisu pól +0x08/+0x14 — PASS (z nuansem NOT_CHECKED, bez kontrprzykładu)".
- **NOWA KWALIFIKACJA:** Test qc_b2_exclusive.py jest **censusem wywołań w
  przybliżonych ciałach funkcji** (granica = heurystyka 3×CC — kod: linie 45-52),
  NIE śledzeniem provenance argumentów; jego ATTR_FUNCS zawiera writer FUN_00845F70
  (linia 18). Jego wynik uprawnia wyłącznie do zdania: **„we wszystkich
  prześledzonych ścieżkach builder→getter atrybutów→setter (statycznie, w zasięgu
  testu) transformy pochodzą z systemu atrybutów"**. Kwantyfikator „WYŁĄCZNIE"
  (globalny) wymagałby: (a) rozliczenia provenance argumentu dla KAŻDEGO
  setter-callera z definicją, odbiorcą, gałęzią i upstreamem, (b) negatywu pełnego
  dla ścieżek pozadatawych — żaden z tych dowodów nie istnieje. Źródło WARTOŚCI w
  drzewie atrybutów (plik/sieć/mieszane/wyliczane) pozostaje UNKNOWN (H1/H2/H3/H4
  bez zmian; sieć-pierwszeństwo odrzucone jako założenie per ERRATA_R2).
- **ŹRÓDŁO:** odczyt qc_b2_exclusive.py (RUN4\00_CONTROL\qc_probe\; linie 45-52,
  18); kontrprzykład logiczny Desktop poprawny wobec PREDYKATU.
- **KONTRTEST:** kontrprzykład: dwa censusy ciał tej samej funkcji o różnych
  granicach heurystyki dają różne przypisanie attr-callei (zlew 0x00567170/
  0x00567770 — patrz [SE-6]) — dowód, że census w ciałach nie jest walidatorem
  wyłączności.

### [SE-6] Rozliczenie 15 setter-callerów — 9/3/3 (poprawka QC-3)

- **STARE** (RUN4 QC_REPORT.md:27, B2): > „Zbadawszy napędy wszystkich 15 funkcji setter-callers: **10 woła funkcje systemu atrybutów bezpośrednio** (walker FUN_0085b840 / FUN_00843d60 / resolver FUN_008544d0 / check FUN_00844020), a 4 bez bezpośrednich odczytów (FUN_005b5f90, FUN_00459270, FUN_0043a200, FUN_00488920) przyjmuje wartości z parametrów..."
- **NOWA KWALIFIKACJA (atrybucja Ghidra + granice szanujące rzeczywiste starty;
  poprawka QC-3 — pełny census własny z pełną listą ATTR):** 15 call-site'ów
  settera pozycji FUN_00730F90 w 15 funkcjach:
  | grupa | funkcje | status provenance |
  |---|---|---|
  | **bezpośrednie odczyty atrybutowe (9)** | FUN_0050BED0, FUN_00457CD0, FUN_00442190, FUN_00447630, FUN_004B3A00, FUN_004C47F0, FUN_00567770, FUN_0067BC90, FUN_0067CCD0 | atrybutowe (kwalifikacja RUN4 podtrzymana; census własny: attr-calle @0x50BF29/0x457D38/0x442334/{0x447726,0x448B8A,0x4498A4,0x44A66E}/{0x4B3A52,0x4B3C02}/{0x4C485A,0x4C4981}/{0x5677C4,0x5677DE,0x5679C2,0x567A48}/0x67BDD2/0x67CE12) |
  | **czysto parametryczne (3)** | FUN_00459270, FUN_0043A200, FUN_00488920 | wartości z parametrów (RUN4); dalszy ślad provenance NIEROZLICZONY |
  | **singleton-readers (3)** | FUN_005B5F90 (provenance parametrów śledzona per RUN4 QC B2), FUN_0046E790, FUN_00567170 | 0 bezpośrednich attr-callów w własnym ciele; wołają singleton managera parametrów FUN_004154F0 (@0x5B629D, @0x46EA1F, @0x567662); provenance wartości setterów NIEROZLICZONA (kandydat: mapa parametrów przez singleton) |
  **Korekty vs RUN4 QC B2 / DRAFT SE-6:** (i) **FUN_00567170 NIE jest „bezpośrednim
  czytnikiem atrybutów"** — jej ciało [0x00567170, 0x00567770) ma ZERO attr-callów;
  cztery attr-calle zliczone w jej wpisie klasyfikacyjnym (F5_SEH_CLASSIFICATION,
  size 2498) leżą w ciele FUN_00567770 (@0x5677C4+) — artefakt zlewu heurystyki 3×CC
  (między funkcjami blob danych bez paddingu); „10 bezpośrednich" (RUN4 QC B2) =
  9 + ten artefakt. (ii) FUN_005B5F90: 0 attr-callów + 1×FUN_004154F0 — przeniesiona
  z grupy „parametryczne" do singleton-readers (z adnotacją śladu RUN4). (iii)
  **15. funkcja = FUN_0046E790: NO_DIRECT_ATTR_CALLS; woła singleton managera
  parametrów FUN_004154F0 @0x46EA1F; settery f60/f90/fb0; provenance NIEROZLICZONA**
  (kandydat: mapa parametrów — szew jak w RECEIVER_MATRIX §4).
- **ŹRÓDŁO:** GHIDRA_FUNC_ATTR.json (atrybucja 15 site'ów/15 funkcji — zgodna z
  własnymi granicami; adiustacja prologów: pełne SEH @0x00447630/0x004C47F0/
  0x0046E790/0x00567770; 0x00567170 = `55 8B EC 83 E4 F8 6A FF...`); własny census
  attr/singleton (QC_F5_SETTERS.json).
- **KONTRTEST:** własny scan z granicami szanującymi starty: 0 attr-callów w
  [0x00567170, 0x00567770) przy 4 attr-callach w [0x00567770, 0x00567C50) — ten sam
  zestaw etykiet w obu wpisach heurystycznych był dublem.

### [SE-8] „11/26 callerów ctora bez setterów" → jawna lista NOT_CHECKED (19 funkcji)

- **STARE** (RUN4 QC_REPORT.md:28, B2): > „ctor rekordu FUN_00730700 (init 12 dwordów +0x00..+0x2C, FLDZ→+0x10) ma **26 call-site'ów** (nie tylko builder): 11 z nich nie woła setterów — semantyka tych rekordów (czy to też „placement records" z innym zasilaniem) nie była badana w runie i nie jest rozstrzygnięta w moim QC (pozostaje NOT_CHECKED...)."
- **NOWA KWALIFIKACJA (atrybucja Ghidra; census własny):** ctor FUN_00730700 ma
  **26 call-site'ów w 24 funkcjach** (dwie funkcje po 2 site'y: FUN_00447630
  @0x0044A19E+0x0044AAA4, FUN_0050E490 @0x0050F098+0x0050F5C8). Funkcje wołające
  settery (5): FUN_00447630, FUN_00459270, FUN_00567770, FUN_0067BC90, FUN_0067CCD0
  (własny scan ciał — identyczna lista). **Funkcje BEZ wywołań setterów
  (f60/f90/fb0/fd0) = 19 (NOT_CHECKED, lista VA call-site'ów):** FUN_00456770
  @0x004567BC, FUN_00457C00 @0x00457C2A, FUN_00457E30 @0x00457E76, FUN_0046AA90
  @0x0046AAE3, FUN_004B9960 @0x004B9A7D, FUN_004C5BD0 @0x004C5BFB, FUN_004E3B70
  @0x004E3C60, FUN_004FF620 @0x004FF93C, FUN_0050BAF0 @0x0050BB1C, FUN_0050C0C0
  @0x0050C147, FUN_0050CC70 @0x0050D1FC, FUN_0050D480 @0x0050D730, FUN_0050E490
  @0x0050F098+0x0050F5C8, FUN_0050FCF0 @0x0050FD39, FUN_005106A0 @0x005106D1,
  FUN_00511070 @0x005110DA, FUN_006C8000 @0x006C8065, FUN_006C80C0 @0x006C812D,
  FUN_0072FA30 @0x0072FB8E (19 funkcji / 20 site'ów). Liczba „11" z QC nie jest
  reprodukowalna pod atrybucją Ghidra (zależna od heurystycznych granic ciał);
  wiążąca jest lista 19/20 — **semantyka tych rekordów pozostaje NOT_CHECKED**.
- **ŹRÓDŁO:** GHIDRA_FUNC_ATTR.json + własny census (26 site'ów E8; oba dwo-site'owe
  ciała potwierdzone własnym wyznaczeniem końca).
- **KONTRTEST:** 5 funkcji z setterami = własny scan niezależny od atrybucji
  (identyczny wynik metodami oboma); lista 19 = dopełnienie 24-5, każda z pełnym VA.

---

## CZĘŚĆ F — drobne korekty (piny; wszystkie zweryfikowane własnym odczytem)

| # | STARE | NOWE (pin — start instrukcji) | Dowód własny |
|---|---|---|---|
| M-1 | zapis vft ArkModelResourceInstanceRef @0x006FA8BC (+0xC) [RUN3 AMENDMENT P3-2] | **@0x006FA8BD (+0xD)**: `C7 00 B8 64 A8 00` @0x006FA8BD (bajt @0x006FA8BC = 00, ostatni operand `C7 40 04 00 00 00 00` MOV [EAX+4],0); item `89 48 08` @0x006FA8C3; RET 4 | QC_MATRIX_LINKS.json |
| M-2 | „296445 LE (5d 85 04 00)" [RUN3 QC A1:22] | **FD 85 04 00** (296445 = 0x000485FD; potwierdzone bajtami rekordu 4508: A=296445 @96516 = fd 85 04 00) | własne przeliczenie + dump |
| M-3 | zapis vft ArkObject @0x00726E9F [RUN3 QC A8:69] | **@0x00726EA1**: `C7 06 48 6B A8 00` (poprzedzająca `8D 4E 08` LEA ECX,[ESI+8] @0x00726E9E; bajt @0x00726E9F = operand LEA) | QC_F1_ABI.json |
| M-4 | store +0x28 @0x006726EBC [RUN3 QC A8:69 — literówka] | **@0x00726EBC**: `89 46 28` | QC_F1_ABI.json |
| M-5 | QC B8 przypisuje executorowi skan kotwic „aligned-only" | executor `s12_prt_content_check.py` skanuje 13 kotwic przez `payload.find(pat, off)` na **wszystkich** offsetach (L63); caveat „aligned-only" dotyczył ODRĘBNEGO censusu u32 (L69; notka L89-90) — powtórka QC nie zwiększyła zakresu skanu kotwic | odczyt skryptu (RUN4, verbatim) |
| M-6 | „Execute ma zero znalezionych bezpośrednich CALL" jako granica RE | brak bezpośrednich CALL (0 — potwierdzone) **nie jest** dowodem braku wywołań — wirtualny dispatch przez vtable 0x00A7C1FC istnieje (RUN4 B6); rozróżnienie „xref-statyczny" vs „osiągalność wirtualna" utrzymać w każdej granicy | GHIDRA_REFCOUNTS (metodologia isCall) + RUN4 QC B6 |
| M-7 | łączenie mianowników joinu A | **3618/3618 = 100%** to pokrycie pola A (unikalne niezerowe A mają wpis `<A>.nif` w Models.bnt); **3618/5596 = 64.6533%** to udział tych modeli w korpusie 5,596 wpisów .nif — dwa różne mianowniki, nie zamienne | definicje RUN1 Z2 + ROUND §7; 3618/5596 = 0.646532… |
| M-8 | porządek walidacji manifestów | **MANIFEST_VALIDATION_ORDER** (reguła jawnie — patrz ZASADY pkt 4 powyżej): ostatni poprawny manifest w czasie wiążący dla plików, które pokrywa; closure manifest wiążący dla pokrytych; rozbieżności historycznych manifestów = documentation-class. Konkrety: RUN4 GHIDRA_LOCAL manifest (db.52/53) nieaktualny wobec własnych opublikowanych plików (db.63/64) — projekt RUN4 niezmieniony przez QC/closure (integrity: closure manifest 49/49); kopia w TYM runie: AT_COPY (db.63/64) + finalny SHA256 (db.67/68) | porównanie manifestów (10 vs 10 wpisów, różnica wyłącznie .gbf) + GA5 census |

---

## CZĘŚĆ G — poprawki QC do warstwy narracyjnej TEGO runu (nie historycznych pakietów)

| # | twierdzenie RESEARCH_FINDINGS/DRAFT | poprawka | dowód |
|---|---|---|---|
| QC-1 (P2) | §2.2/§7: „każda z 55 ... z imm32"; F1_REG_ARGS wpis 0x007262B7 z imm=0x00A7957B | 54 rejestracje param-set z imm32 + 1 lazy-init klasy bazowej (FUN_00726230, DAT_00BA51C4, arg1=PUSH 0, ID 0); wpis 0x00A7957B = artefakt heurystyki (stała pustego stringa, nie ID) | QC_F1_REGARGS2.json |
| QC-2 (P2) | §2.3: „rejestracje ... FUN_006B6541, FUN_0072C151, FUN_0072BF11" | cele z bajtów: FUN_00734C40 @0x0073D892, FUN_0070C150 @0x0073D8A0, FUN_0070BF10 @0x0073D8AB | dump writer'a (własny + executora — identyczne bajty) |
| QC-3 (P2) | DRAFT [SE-6]: „bezpośrednie (10) ... FUN_00567170 ..." | 9/3/3 (patrz [SE-6] powyżej) | QC_F5_SETTERS.json |
| QC-4 (P3) | RECEIVER_MATRIX rząd 4: „slot3 CALL [vft+0xC] w gałęzi 0x38B0" | wartość mapy: +0=vtable potwierdzone @0x00855B2F-3F (wywołanie [vft+8], inna gałąź); CALL [vft+0xC] @0x0085552F dotyczy obiektu EDI; gałąź 0x38B0 = tylko CALL-e bezpośrednie | QC_F2_SELECTOR.json + pełny skan FF/2 |
| QC-5 (P3) | piny operandowe (np. PUSH 0x4E3E „@0x0073A114", CMP „@0x0073D832", CALL FUN_0070E2F0 „@0x0073D888", load „@0x0073520D", read-back „@0x0073D88D", clear „@0x0073D8C7") | starty instrukcji: @0x0073A111, @0x0073D831, @0x0073D887, @0x0073520C, @0x0073D88C, @0x0073D8C6 (konwencja operandowa odnotowana) | QC_F1_REGARGS3.json + QC_F1_DAT58CC_POSCONTROL.json |
| QC-6 (P3) | F2_SELECTOR.json podsekcja „template_4508" (odczyt od pozycji D z zerowymi etykietami) | mylący artefakt pierwszego przebiegu; wartości autorytatywne = F2_T4508_WALK.json (zgodne z własnym walkiem) | QC_F2_VFS_WALK2.json |
| QC-7 (P3) | GA5: zbiór pakietów | executor censusem objął RUN1/RUN2/RUN3/RUN4/ROUND/JOIN+ERRATA_R2/Desktop (7, 99_Audits); pakiet „296445-ERRATA" (repo-only) nietykalny per git (HEAD==BASE, czysty status); zero zmian w obu zbiorach | QC_GA5_IMMUTABLE.json + git |

---

## KONTRAKT NARZĘDZIOWY (dla Fazy B — granice RECEIVER_UNRESOLVED)

1. **Nazwa klasy wartości mapy managera parametrów ([hit+8]):** do rozstrzygnięcia
   przez (1) punkt INSERT do mapy mgr+0x10 (kto wstawia wartości pod kluczami
   param-setów; kandydaci censusu: FUN_0085B3E0/0085B780/0085B7F0 + 71 funkcji
   wołających singleton-getter FUN_004154F0; FUN_009719D0 = generyczny operator[]),
   lub (2) ctor wartości (zapis vtable + int@+8), lub (3) runtime (zakazany w tej
   rundzie).
2. **arg1 FUN_00567C50 przy getterach D (3 callerów):** provenance ogniw
   (world-object state / bufor 0xB9 / handler-arg) — RECEIVER_UNRESOLVED per caller.
3. **19 funkcji ctor-callers bez setterów:** semantyka NOT_CHECKED (lista VA [SE-8]).
4. **FUN_00567170, FUN_0046E790, FUN_0043A200, FUN_00488920 (+FUN_00459270):**
   provenance wartości setterów NIEROZLICZONA (parametry/singleton).
5. **Semantyka liczbowa D (124.941@4508):** nie rozstrzygnięta (ANCHORS_ABSENT_
   SEMANTICS_OPEN; runtime zakazany w tej rundzie).

**Żadne twierdzenie tego runu nie ogłasza STATIC_INSTANCE_MECHANISM_CONFIRMED ani
źródła placementu. Historyczne pozycje 296445 NIE zostały odzyskane.**
