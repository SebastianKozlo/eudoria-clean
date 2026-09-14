# ERRATA_R4 — SUPERSESSION LEDGER
## RUN: PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913

**RUN_CLASS:** LOAD_BEARING (szew pochodzenia atrybutów: łańcuch komunikat →
deserializacja → rekord placementu → instancja MovableObject → insert do mapy
parametrów; własne bajty). **ERA:** EU 9.3.5 (pcg_install). **Executor:**
pe-reconstruction; **INTERNAL_QC + formalizacja + publikacja:** pe-master-auditor
(QC_PASS; 06_REPORT\QC_REPORT.md; poprawki P2/P3 włączone poniżej jawne).
**TRYB:** STATIC-ONLY (klient/Frida/x32dbg/mock/sieć NIE uruchomione).
**Binarium:** Entropia.exe SHA256
E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (8 015 872 B,
image base 0x00400000, ASLR OFF). templates.vfs SHA256
BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77 (560 788 B).

**ZASADY (kontynuacja ERRATA_R3):**
1. Historyczne pakiety NIETYKANE (GB6 executora: composite przed==po IDENTICAL
   8/8 + własny repeat per-plikowy auditora: 1385 plików/8 pakietów — hashe
   identyczne z census „after"; QC_GB6_PERFILE.json). Errata CYTUJE oryginały
   verbatim (plik:linia) — poprawiona treść żyje TUTAJ i w 06_REPORT\REPORT.md.
   Raport roboczy executora (RESEARCH_FINDINGS.md) zachowany VERBATIM.
2. Kolejność wiążącości: (a) evidence 01_RAW/02_ANALYSIS executora (nietknięte),
   (b) NINIEJSZA ERRATA_R4 (kwalifikuje narracje ROUND/RUN4/PKG_A), (c) raporty
   historyczne w miejscach skonfliktowanych — czytane przez pryzmat (b).
3. Żadne twierdzenie nie ogłasza STATIC_INSTANCE_MECHANISM_CONFIRMED ani
   źródła placementu STATYKÓW; pozycje 296445 NIEODZYSKANE (bez zmian).
4. **MANIFEST_VALIDATION_ORDER** (reguła ERRATA_R3): ostatni poprawny manifest
   w czasie jest WIĄŻĄCY DLA PLIKÓW, KTÓRE POKRYWA; manifest zamknięcia
   (closure) jest wiążący dla plików, które pokrywa; rozbieżności wcześniejszych
   manifestów = klasa dokumentacyjna. Manifesty GHIDRA_LOCAL (AT_COPY + FINAL)
   opisują dokładnie stany, które pokrywają (projekt lokalny, .gbf NIE publikowane).
5. Piny VA w tej erracie = START instrukcji (opcode); piny historyczne
   operand-pozycyjne odnotowano jawne (per ERRATA_R3 [M-3]/[M-4]).

---

## CZĘŚĆ A — [SE-R4-1] „komunikat 0xB9 niesie KLUCZE, nie transformy" — supresja precyzyjna

- **STARE** (ROUND_REPORT.md:51-53, pakiet PE_935_STATIC_PLACEMENT_ROUND1_20260913):
  > „łańcuch 0xB9 istnieje i jest rozkodowany bajtowo (CommunicationSubsystem → executor → case 0xB9 → FUN_005b72c0 → FUN_00567c50 → FUN_00567770); komunikat 0xB9 niesie KLUCZE, nie transformy."
- **STARE** (PE_MASTER_REVIEW.md:3, pakiet PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913):
  > „NUANS: ścieżka 0xB9 (FUN_005b6370) też czyta z drzewa — komunikat 0xB9 niesie KLUCZE, nie transformy."
- **STARE** (QC_REPORT.md:27, pakiet PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913):
  > „ścieżka komunikatowa 0xB9 niesie KLUCZE (kursorami FUN_007527xx), a wartości pochodzą z drzewa atrybutów ✓✓. **Kontrprzykładu „transform z sieci/pliku wprost do +0x08/+0x14" nie znaleziono.**"
- **STARE** (ROUND_REPORT.md:158-160): > „kanał NETWORK 0xB9 (łańcuch istnieje; niesie KLUCZE; producent atrybutów NIEUSTALONY — GŁÓWNA NIEWIADOMA)]" oraz (ROUND_REPORT.md:306-307): > „kanały FILE (brak pliku-placementów) i NETWORK (0xB9: łańcuch istnieje, niesie klucze, producent nieustalony) oba otwarte; H2 domknięta jako warstwa".
- **STARE** (Z2_cwo_chain.md:68, pakiet PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913):
  > „(b) komunikat 0xB9 executora (payload {k32,k32,u8,u8}; producent = handler kanału".

- **NOWA KWALIFIKACJA (trzywarstwowa):**
  **(i) DLA TYPU 0xB9 — ZATRZYMANE-JAKO-ZWERYFIKOWANE.** Własne bajty: handler
  FUN_005B72C0 konsumuje z kursora {skip-4 (inline advance, nieczytane),
  u16 subtyp (FUN_007527F0, advance 2), {u32,u32,u8,u8} (subtyp 1, FUN_00752700)
  lub {u32,u32,u8} (subtyp 2, FUN_00752640)} i **NIGDY nie woła procesora
  placementu FUN_004C47F0 ani deserializatora FUN_007453D0** (census E8:
  FUN_004C47F0 ma DOKŁADNIE 4 call-site'y: 0x00457594/0x004B0B47/0x004B171A/
  0x004B1DBC — żadnego z regionu 0x005B7xxx). Odczyt rundy-1 {u32,u32,u8,u8}
  był **PEŁNĄ konsumpcją payloadu subtypu-1 przez handler 0xB9** — NIE
  „niepełnym odczytem kursora". Twierdzenie rundy-1 o 0xB9 pozostaje PRAWDZIWE.
  **(ii) DLA RODZINY KURSORÓW — SUPERSEDED (uogólnienie rundy-1 było
  niepełne).** Twierdzenie „Kontrprzykładu «transform wprost do +0x08/+0x14»
  nie znaleziono" zostaje zastąpione: **kontrprzykład ISTNIEJE na typach
  siostrzanych tego samego executora** — case'y dispatchera **0xB0 → FUN_004574F0**
  (CALL FUN_004C47F0 @0x00457594), **0xC6 → FUN_004B0AB0** (@0x004B0B47),
  **0xC7 → FUN_004B1670** (@0x004B171A) oraz **special-case Execute:
  FUN_004B2950 przy `param_2==0xB2` → FUN_004B1C70 → FUN_004C47F0
  @0x004B1DBC** (0xB2 omija byte-table — własny dekod: byte-table
  0x004B1B3C[0xB2-0xA2]=0x15→slot 21=default-pusty; brama 0xB2 jest w
  FUN_004B2950 = wpis vtable @0x00A7C200, RTTI właściciela własny odczyt:
  `.?AVArkClientPacketExecutor@@`, COL@0x00AA032C → TD@0x00B733A0). Wszyscy
  czterej przekazują TEN SAM kursor komunikatu do FUN_004C47F0, który
  deserializuje (FUN_007453D0 @0x004C483D): **klucz u32 (TOP-kursor, read
  @0x007453EF → rec+0)**, parę param-set 2×u32 (TOP-kursor, FUN_004124B0
  @0x0074540F → rec+4/rec+8; CMP 0x4E34/0x4E38/0x5DC9 @0x004C4989), sub-pakiet
  (FUN_007343E0 @0x00745419): **wariant u16** (read @0x00745435 → rec+0x34),
  **POZYCJĘ vec3 3×dword** (FUN_00412430 @0x0074545A, 12 B → rec+0x38),
  **ROTACJĘ vec3** (@0x00745465 → rec+0x44), wektor-2 (u32@0x0074547C →
  rec+0x50, u32@0x007454AA → rec+0x54, f32 FLD/FSTP @0x007454D9 → rec+0x58),
  bajt końcowy (read @0x00745508 → rec+0x5C). Setter **f90 zapisuje pozycję
  STRAIGHT do rekordu placementu +8/+0xC/+0x10** (@0x004C48F4; FUN_00730F90 =
  `[this+8]=p[0]; [this+0xC]=p[1]; [this+0x10]=p[2]`). Kanał
  kursorowy → rekord placementu → instancja → mapa = **kanał instancji
  RUCHOMYCH (MovableObject/ClientMovableObject — patrz [SE-R4-2])**.
  **(iii) GRANICA (zachowana, jawna):** UPSTREAM bajtów kursora (kto fizycznie
  wypełnia ring odroczeń/bufor executora — kolejka sieciowa vs lokalna)
  **NIEUDOWODNIONY**: dispatcher FUN_004B18D0 ma 2 callerów — FUN_004B1B70
  (pump ringa odroczeń; sam wołany z FUN_004B1C70 @0x004B1F2C) i FUN_004B2950
  (Execute; wpis vtable @0x00A7C200 — callerzy vtable poza zakresem).
  **NIE ogłaszamy „z sieci"** — sieć vs lokalna kolejka pozostaje otwarte.

- **ŹRÓDŁO:** własne bajty (dekod x86 auditora): switch dispatchera
  @0x004B18D0-0x004B18EF (`ADD EAX,-0xA2; CMP EAX,0x25; MOVZX BYTE
  [0x004B1B3C]; JMP [0x004B1AE4]`), byte-table/jump-table pełne (22 wpisy),
  handlery 0xB0/0xC6/0xC7 (`PUSH ESI(kursor); CALL FUN_004C47F0`),
  FUN_004B2950 (`cmp 0xAC/0xB2` + gate FUN_0042bc20 → dispatcher/kolejka
  FUN_004B1890), FUN_004B1C70 head (u32 z kursora + `[mgr+0x224]`), census E8
  FUN_004C47F0/FUN_007453D0/FUN_005B72C0, dekod FUN_007453D0 pełny (VA każdej
  operacji odczytu — wyżej), FUN_004124B0 (2×u32) / FUN_00412430 (3×dword) /
  FUN_007343E0 (sub-kursor u16-header).
- **KONTRTEST:** (1) census E8 FUN_004C47F0 == 4 — dokładnie powyższe VA;
  (2) census E8 FUN_007453D0 == 1 (tylko @0x004C483D — żaden handler nie
  deserializuje sam; robi to processor); (3) dekod FUN_005B72C0: brak call do
  FUN_004C47F0/FUN_007453D0 — 0xB9 nie zasila deserializacji pozycji;
  (4) kontrola odróżniająca: ta sama para setter-arg w ścieżce EXISTING
  (FUN_0085B3E0(istniejąca, &[rec+0x38], 1) @0x004C4875) — spójność pola
  pozycji pomiędzy ścieżkami create/update.

---

## CZĘŚĆ B — domknięcia RECEIVER/KEY z Fazy A (granice ERRATA_R3)

### [SE-R4-2] Klasa wartości mapy parametrów = instancja MovableObject/ClientMovableObject — RECEIVER_UNRESOLVED #1 ZAMKNIĘTE

- **STARE** (ERRATA_R3, ZASADY 3 / boundaries, pakiet
  PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913): > „RECEIVER_UNRESOLVED
  (map-value class name; arg1 FUN_00567C50 per-caller; 19 ctor-callers without
  setters; D=124.941 semantics UNKNOWN) — RECEIVER_UNRESOLVED pozostaje jawna
  granica. (Faza B)." — nazwa klasy wartości mapy była NIEROZSTRZYGNIĘTA.
- **NOWA KWALIFIKACJA:** wartość mapy parametrów (singleton
  `[0x00BA12E8]`, getter FUN_004154F0, resolver FUN_008544D0 `[hit+8]`) to
  instancja **MovableObject** (vtable 0x00A91E4C; `[vtable-4]=0x00AB33D0` COL →
  `[COL+0xC]=0x00B7997C` TD → TD+8 = `.?AVMovableObject@@` — własny łańcuch
  RTTI) lub pochodnej **ClientMovableObject** (vtable 0x00A7DCB0 →
  `.?AVClientMovableObject@@`; ctor pochodny FUN_00528E50 pisze vtable
  `C7 06 B0 DC A7 00`, imm32 @0x00528EA4). Slot-0 (FUN_0085B7F0) unikalny w
  całym binarium (skan DWORD: 1 trafienie = sama vtable 0x00A91E4C); imm32
  0x00A91E4C w .text = 3 (ctor + 2 dtory) — brak innych typów o wspólnym
  slot-0. Layout instancji (ctor FUN_0085B1B0, własny dekod): +0 vtable, +4
  lock, **+8 wariant (u16 z komunikatu)**, +0x14..0x3B transform 3×3+flaga
  (FUN_007345C0), +0x3C dziecko, **+0x44..0x4C POZYCJA = `[placement+8..0x10]`**
  (przez FUN_00746560 `LEA EAX,[ECX+8]`), +0x50..0x58 global vec3
  (0x00BA921C/20/24), +0x5C..0x70 2×vec3 (FUN_0040B070), **+0x74 KLUCZ =
  `[placement+0]`** (FUN_004123D0 `MOV EAX,[ECX];RET` — deref), +0x78 =
  `[placement+4]`, **+0x88/+0x8C = `[placement+0x20/+0x24]` = para param-set**
  (FUN_00746570 `LEA EAX,[ECX+0x20]`; czytane FUN_0085AD50 `8D 81 88 00 00 00
  C3`), +0x98 = 1.0f (nadpisywane slot5). Jedyna droga wartości do mapy:
  FUN_004C46C0 → ctor FUN_00528E50 (census 1/1).
- **ŹRÓDŁO:** własne łańcuchy RTTI + dekod ctorów + censusy imm32/slot-0.
- **KONTRTEST:** kontrola odróżniająca — wspólny getter `8B 41 08 C3`
  (FUN_007CE1E0) czyta +8 różnych odbiorców (map-value = wariant; ArkObjectClass
  = class-ID; rekord VFS = A) — rozróżnienie po RTTI+vtable+dataflow (kontynuacja
  [SE-7] ERRATA_R3); tu: wariant (+8), nie class-ID.

### [SE-R4-3] Klucz mapy parametrów = uchwyt instancji z komunikatu (rekord[0]) — nie class-ID, nie 0x6A4

- **STARE** (założenie otwarte Fazy A, skorygowane przez ten run w warstwie
  raportu): „key = param_1 selektora z rejestracji" (otwarte założenie;
  rejestracja FUN_00457930 rzeczywiście zwraca NOWY uchwyt w EAX — ale to
  uchwyt, nie ID param-setu) + pytanie rundy: „JAKIE klucze" (RUN_CONTRACT
  zad.3).
- **NOWA KWALIFIKACJA:** **klucz węzła mapy = `[wartość+0x74]` = kopia
  `[placement+0]` = KLUCZ u32 z kursora komunikatu (read @0x007453EF)**
  (insert FUN_00856190: klucz = FUN_00414130(value) = `[value+0x74]`; para
  `{klucz, wartość}` → węzeł `{next=0, klucz@+4, wartość@+8}` — FUN_00854260).
  ID param-setu (0x4E34/0x4E38/0x5DC9/0x38B0) = ATRYBUT wartości (+0x88,
  czytany FUN_0085AD50; CMP w selektorze/FUN_004C47F0), NIE klucz mapy.
  Atrybuty 0x6A4-rodziny = identyfikatory KOLUMN drzewa atrybutów (walker
  FUN_00846840), nie klucze mapy parametrów. TA-SAMOŚĆ (jedna ścieżka, VA):
  kursor @0x007453EF → `[rec+0]` @0x007453F6 → `[placement+0]` @0x004C48E6
  (FUN_00853A50) → `[value+0x74]` @0x0085B20A/0x0085B211 → klucz insertu
  @0x008561AC → `node+4` @0x00854284 — **jeden klucz wiąże komunikat, rekord,
  węzeł i instancję**.
- **ŹRÓDŁO:** własny dekod insertu/ctora/FUN_00853A50 + census E8 (insert 1,
  creator 6, keyproducer 8 — identyczne z executorerem).
- **KONTRTEST:** duplikat klucza → flag==0 → deleting-dtor duplikatu
  (`6A 01; FF D2` @0x008561E6-0x008561EA) — klucz jest kluczem TOŻSAMOŚCI
  węzła, nie atrybutem; wartość `+0x74==0` → brak insertu (`83 7F 74 00`).

### [SE-R4-4] Receiver gettera D w driverze (granica #2 Fazy A) — ROZSTRZYGNIĘTY

- **STARE** (ERRATA_R3 boundaries): receiver ECX każdego callu gettera D w
  driverze FUN_00567C50 był nierozstrzygnięty (granica per-caller).
- **NOWA KWALIFIKACJA (własne bajty):** prolog drivera: EBP=arg1=KLUCZ
  @0x00567C8B, ESI=arg3 @0x00567C92, EBX=arg2 @0x00567C99, EDI=this @0x00567CA0.
  Site'y gettera D (FUN_0048ADA0 `MOV EAX,[ECX+0x10];RET`): **@0x00567D16 i
  @0x00567D46: `8B CE` → ECX=ESI=arg3 = rekord stanu** (odczyt `[rekord+0x10]`);
  **@0x00567F72: `8B 4C 24 20` @0x00567F56 → ECX=[ESP+0x20]=EDI=this (kolejka)**.
  Wszystkie trzy rozstrzygnięte per-caller; queue-push (FUN_00567B40) dostaje
  wynik D jako argument.
- **ŹRÓDŁO:** własny dekod drivera 0x00567C50-0x00567F80 + censusy.
- **KONTRTEST:** dwie klasy receiverów na tej samej funkcji-getterze
  (arg3-rekord vs this-kolejka) rozróżnione bajtowo — kontrola odróżniająca
  per-site, nie globalna.

---

## CZĘŚĆ C — rozjazdy raportu run-B znalezione w QC (poprawione w REPORT.md)

### [SE-R4-5] Zbiór typów deserializujących pozycję: 0xB9 NIE jest członkiem; 0xB2 pominięty [P2-1]

- **STARE** (RESEARCH_FINDINGS.md:20, ten pakiet): > „kursor podkomunikatu (typy
  0xB0/0xB9/0xC6/0xC7, dispatcher FUN_004B18D0) jest deserializowany
  (FUN_007453D0: klucz u32@+0, transforma, pozycja vec3 u32×3@+0x50..0x58,
  wariant bajt@+0x5C; read-cursory FUN_00752700/26 40)".
- **STARE** (SEAM_FLOW_MAP.md:68, ten pakiet): > „FUN_004C47F0 (processor
  placementu, 4 callerów = ww. handlery)".
- **NOWA KWALIFIKACJA:** poprawny zbiór karmiący FUN_004C47F0 kursorem:
  **{0xB0, 0xC6, 0xC7 (case'y dispatchera), 0xB2 (special-case Execute
  FUN_004B2950→FUN_004B1C70)}** — census E8 4 site'ów (wyżej); handler 0xB9
  (FUN_005B72C0) NIE woła procesora. „ww. handlery" jest fałszywe dla 4-tego
  callerа (FUN_004B1C70 = handler 0xB2, nie handler 0xB9). Bramka CSV GB4
  executora („case 0xB0/0xC6/0xC7→processory placementu") była poprawna —
  błąd tylko w warstwie SEAM_FLOW_MAP/RESEARCH_FINDINGS §1.
- **ŹRÓDŁO/KONTRTEST:** jak [SE-R4-1] (census + dekod bramki 0xB2).

### [SE-R4-6] Atrybucja pól deserializatu: pozycja = rec+0x38 (FUN_00412430), wariant = u16@+0x34; trójka @+0x50..0x58 = wektor-drugi [P2-2]

- **STARE** (SEAM_FLOW_MAP.md:78, ten pakiet): > „value+0x44..0x4C = pozycja z
  rekordu (setter f90 ← deserializat @+0x50..0x58)".
- **STARE** (RESEARCH_FINDINGS.md:73 i :20, ten pakiet): > „+0x50/+0x54/+0x58 =
  POZYCJA vec3; +0x5C = WARIANT bajt" oraz „wariant bajt@+0x5C".
- **NOWA KWALIFIKACJA (własne bajty):** **POZYCJA** wpisywana do rekordu
  placementu przez f90 pochodzi z pola **rec+0x38** (12 B, czytane FUN_00412430
  z SUB-kursora @0x0074545A; arg f90 = `LEA ECX,[ESP+0x48]` @0x004C48EB);
  **ROTACJA** (fb0) z rec+0x44; **WARIANT** przekazywany do create/ctor (→
  value+8) = **u16@rec+0x34** (`MOVZX ECX,WORD [ESP+0x44]` @0x004C493C).
  Trójka @+0x50/+0x54/+0x58 to **WEKTOR-DRUGI**: X2 → `[placement+4]=X2`
  (FUN_00797280 @0x004C491E; w ctorze → value+0x78) + string tworzenia
  (FUN_004C4640=singleton [0x00BA26B8], ignoruje argumenty; FUN_00765930 →
  create arg3 = wskaźnik stringa); **Z2 (f32) → slot5 → `[value+0x98]`**
  (FUN_0085B010 `MOV [this+0x98],arg`; ścieżki EXISTING @0x004C4864-71 i
  post-create @0x004C49AE-B4); Y2 (@+0x54) i bajt (@+0x5C) — przeczytane, ale
  NIE konsumowane przez FUN_004C47F0 (pełny skan odwołań [ESP+0x64]/[ESP+0x6C]
  = 0). Nota: dekompilat executora (`FUN_00730f90(local_78)`; create z
  `local_7c`) i jego własne §3c' są SPÓJNE z tą korektą — rozjazd był tylko w
  warstwie opisowej SEAM_FLOW_MAP §5 / RESEARCH_FINDINGS §5b.
- **KONTRTEST:** ścieżka EXISTING tej samej funkcji używa tego samego pola
  (FUN_0085B3E0(istniejąca, &[rec+0x38], 1) @0x004C4875) — spójność
  create/update; FUN_00412430 własny dekod (`3× MOV; [ESP+4]=0xC; JMP
  FUN_0040DE60` = vec3-reader 12 B; fail-path FLDZ→0.0f), FUN_004124B0 =
  para 2×u32 (8 B).

### [SE-R4-7] Korekty drobne [P3]

- **(a) „IDIV" → DIV:** FUN_00971780 @0x00971798: `F7 F7` = **DIV EDI**
  (bez znaku) — KEY_MODEL_MATRIX.md:12 mówi „IDIV". Dla kluczy < 0x80000000 bez
  różnicy wyniku; fakt bajtowy inny.
- **(b) Piny kontekstowe vs START-opcodu:** „8D 4E 10 6A 64 @0x008550FE"
  (opcode LEA @0x00855104, okno T6 zaczyna 6 B wcześniej); „EBP=arg1
  @0x00567C88" (MOV @0x00567C8B); „8B F9 @0x00567CA8" (MOV EDI,ECX
  @0x00567CA0); „89 46 08 @0x0085B1CC" (opcode @0x0085B1CB — pin
  operand-pozycyjny, konwencja znana z ERRATA_R3 [M-3]/[M-4]).
- **(c) Slot5 = FUN_0085B010:** bajtowo `MOV [this+0x98],arg` — jedno-f32 pole
  (+0x98; ctor: 1.0f; processor: Z2); etykieta „pozycja/velocity setter"
  niedokładna.
- **(d) Obserwacja (nie twierdzenie executora):** FUN_00856190 nie ma
  null-guard — porażka `new` w FUN_004C46C0 wypycha NULL → `[NULL+0x74]`
  (latentny bug klienta; poza szwem, nieblokujący).

---

## Zestawienie granic PO tej erracie (wejście do REPORT.md §6)

1. **Upstream kursora** (sieć vs lokalna kolejka) — UNPROVEN (2 callerów
   dispatcherа + vtable ArkClientPacketExecutor @0x00A7C200; rejestracje
   kanałów poza zakresem).
2. **[singleton 0x00BA1260+8]** porównywany z KLUCZEM (CMP EBP,EAX
   @0x00567CC4-0x00567CCB) — semantyka „własny klucz awatara" = HIPOTEZA
   (właściciel singletonu poza zakresem).
3. **Osie/jednostki value+0x44..0x4C** — UNRESOLVED (konsument = kompozycja
   selektora slot3[i]+[+0x44]; wymaga dekodu FUN_0085B6A0 + FUN_008599A0).
4. **Statyki (4508/296445)** — NIE objęte kanałem movable w tym runie; kandydaci
   FUN_00567170/FUN_005B5F90/FUN_006CB6F0 bez zmian; pozycje 296445
   NIEODZYSKANE; D@4508=124.941 ANCHORS_ABSENT_SEMANTICS_OPEN bez zmian.
5. **Wiązanie modelu dla movables** — poza szwem (sub-obiekt +0xC0 ctora
   pochodnego: FUN_005247C0 → new(0x98)+FUN_00509330; create arg3 = pusty
   string) — kandydat na następną rundę.
6. **19 ctor-callers bez setterów (Faza A)** — NOT_CHECKED, bez zmian.
