# REPORT — PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913 (FINAL)
## Szew pochodzenia atrybutów: komunikat → deserializacja → rekord placementu → instancja MovableObject → mapa parametrów

**RUN_CLASS:** LOAD_BEARING. **TRYB:** STATIC-ONLY (klient/Frida/x32dbg/mock/sieć
NIE uruchomione). **ERA:** EU 9.3.5 (pcg_install). **Executor:** pe-reconstruction;
**INTERNAL_QC + formalizacja + publikacja:** pe-master-auditor (QC_PASS;
06_REPORT\QC_REPORT.md; ERRATA_R4 = ledger supresji; poprawki [SE-R4-5..7]
włączone w ten raport; RESEARCH_FINDINGS.md executora zachowany verbatim jako
raport roboczy; evidence 01_RAW/02_ANALYSIS nietknięte).

**Binarium:** Entropia.exe SHA256
E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (8 015 872 B,
base 0x00400000, ASLR OFF; S0 fail-closed PASS). templates.vfs SHA256
BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77 (560 788 B).
**Repo:** eudoria-clean @ BASE_SHA 5d0edde5863795d6eefd8bb11989e8edb7b28546
(weryfikacja auditora: HEAD==origin/master==BASE_SHA przy starcie; obce
`?? experiments/` nietknięte).

**GŁÓWNE PYTANIE (RUN_CONTRACT):** SKĄD trafia konkretna wartość
pozycji/rotacji do właściwego kontenera i jak klucz/kontener wiąże się z TĄ
samą instancją i modelem — na szwie MAPY PARAMETRÓW.

---

## 1. ODPOWIEDŹ JEDNOZDANIOWA (z kwalifikacją scopingową)

**Na kanale instancji RUCHOMYCH: konkretna wartość pozycji przybywa w bajtach
KURSORA KOMUNIKATU (deserializacja FUN_007453D0 z sub-pakietu kursora: vec3
12 B → setter f90 → rekord placementu +8/+0xC/+0x10 → ctor kopiuje do
instancji +0x44..0x4C), klucz u32 z tego samego kursora (rekord[0]) jest
JEDNOCZEŚNIE kluczem węzła mapy jak i kopią w instancji (+0x74), a klasą
wartości mapy jest instancja MovableObject/ClientMovableObject (RTTI) —
upstream bajtów kursora (kolejka sieciowa vs lokalna) pozostaje NIEUDOWODNIONY,
a STATYKI (4508/296445) NIE zostały objęte tym kanałem w tym runie.**

Status: **CONFIRMED (bajtowo, każde ogniwo własny odczyt)** dla kanału movable;
**OPEN** dla statyków (§5d/§6).

## 2. WYNIK SZWU — łańcuch z kwalifikacją każdej krawędzi

Kanał deserializacji (typy komunikatów: **0xB0, 0xC6, 0xC7 — case'y
dispatchera FUN_004B18D0; 0xB2 — special-case w Execute FUN_004B2950 —
korekta QC [SE-R4-5]: 0xB9 NIE jest członkiem tego zbioru**):

| # | Krawędź | VA (własne bajty) | Status |
|---|---|---|---|
| S1 | executor: vtable ArkClientPacketExecutor @0x00A7C200 slot → FUN_004B2950 (Execute); bramy: `param_2==0xAC`→FUN_004B2270, `param_2==0xB2`→FUN_004B1C70, gate→dispatcher, else→ring FUN_004B1890 | DWORD @0x00A7C200=0x004B2950; RTTI własny `.?AVArkClientPacketExecutor@@` (COL@0x00AA032C→TD@0x00B733A0) | **PROVEN** (vtable→funkcja; callerzy vtable = [UNPROVEN] — patrz §6.1) |
| S2 | Execute → dispatcher FUN_004B18D0 @0x004B29A9 (drugi caller: FUN_004B1B70 @0x004B1BE6 — pump ringa, wołany z FUN_004B1C70 @0x004B1F2C) | census E8: 2 | **PROVEN** |
| S3 | dispatcher switch: `ADD EAX,-0xA2; CMP EAX,0x25; MOVZX [0x004B1B3C]; JMP [0x004B1AE4]`; case 0xB0→FUN_004574F0 @0x004B198B; 0xC6→FUN_004B0AB0 @0x004B1AC1; 0xC7→FUN_004B1670 @0x004B1AD9; (case 0xB9→FUN_005B72C0 @0x004B1A16 — osobny kanał, §5c) | 0x004B18D0-0x004B18EF + tablice (22 wpisy) | **PROVEN** |
| S4 | handlery 0xB0/0xC6/0xC7 + ścieżka 0xB2 (FUN_004B1C70) → procesor placementu FUN_004C47F0 z tym samym kursorem | @0x00457594 / @0x004B0B47 / @0x004B171A / @0x004B1DBC (census E8=4) | **PROVEN** |
| S5 | FUN_004C47F0 → FUN_00745360 (init struktury) @0x004C4821; → FUN_007453D0 (deserializacja z kursora) @0x004C483D | census E8=1/1 | **PROVEN** |
| S6 | FUN_007453D0: klucz u32 (TOP-kursor, read @0x007453EF)→rec+0; para param-set 2×u32 (FUN_004124B0 @0x0074540F)→rec+4/+8; sub-kursor (FUN_007343E0 @0x00745419, u16-header); wariant u16 @0x00745435→rec+0x34; POZYCJA vec3 12B (FUN_00412430 @0x0074545A)→**rec+0x38**; ROTACJA vec3 @0x00745465→rec+0x44; wektor-2: u32@0x0074547C→rec+0x50, u32@0x007454AA→rec+0x54, f32(FLD/FSTP)@0x007454D9→rec+0x58; bajt@0x00745508→rec+0x5C (korekta pól [SE-R4-6]) | pełny dekod, konwencja kursora: data@+0/size@+8/offset@+0xC/flaga@+0x11, odczyt=data+offset, fail-closed per pole, advance=FUN_0040DE60 | **PROVEN** |
| S7 | resolver(klucz) @0x004C484E-0x004C485F; MISS → f60 @0x004C48D8; FUN_00853A50(placement, klucz)→`[placement+0]` @0x004C48E6; **f90(placement, &[rec+0x38]) @0x004C48F4 → +8/+0xC/+0x10**; fb0(&[rec+0x44]) @0x004C4902; fd0(&[rec+4]) @0x004C4910 → +0x20/+0x24; FUN_00797280(placement, X2)→`[placement+4]` @0x004C491E | własny dekod pełnej ramki | **PROVEN** |
| S8 | create FUN_004C46C0(placement, u16-wariant, string, 1) @0x004C4952 (MOVZX u16 @0x004C493C) → new(0x128) @0x004C4792 → ctor FUN_00528E50 @0x004C47C1 → base FUN_0085B1B0 @0x00528E8D | korekta wariantu [SE-R4-6]: u16@rec+0x34, NIE bajt@+0x5C | **PROVEN** |
| S9 | ctor: `[+0]=vtable 0x00A91E4C` (imm @0x0085B1C3); `[+8]=wariant`; transform FUN_007345C0; **`[+0x74]=[record+0]`** (FUN_004123D0 @0x0085B20A); `[+0x78]=[record+4]`; **`[+0x44..0x4C]=[record+8..0x10]`** (FUN_00746560); **`[+0x88/+0x8C]=[record+0x20/+0x24]`** (FUN_00746570); `[+0x98]=1.0f`; +0x50..0x58=globalne 0x00BA921C/20/24; pochodny: `[ESI]=0x00A7DCB0` (imm @0x00528EA4) + lookup kluczowy FUN_005247C0→`[+0xC0]` | własny dekod obu ctorów | **PROVEN** (wiązanie modelu: §6.5 OPEN) |
| S10 | insert FUN_00856190(mgr, wartość) @0x004C47DA: `[value+0x74]==0`→ret0; klucz=FUN_00414130=`[value+0x74]` @0x008561AC; rehash FUN_00856090(map, count+1); para{klucz,wartość}; find-or-create FUN_00854D90 → node FUN_00854260: alloc 0xC, **{next=0, klucz@+4, wartość@+8}**; duplikat→slot0(PUSH 1)=deleting-dtor @0x008561E6 | pełny dekod | **PROVEN** |
| S11 | mapa = STLport hash_map @mgr+0x10 (mgr=singleton `[0x00BA12E8]`, getter FUN_004154F0, ctor FUN_008550C0: 100 bucketów; hashfind FUN_00971780: **DIV** key%(n−1), granica=wartość następnego bucketa); resolver FUN_008544D0 `[hit+8]` @0x008544F9; CS @mgr+0x44 | własny dekod [korekta DIV — SE-R4-7a] | **PROVEN** |
| S12 | **TA-SAMOŚĆ klucza:** kursor@0x007453EF → rec+0@0x007453F6 → placement+0@0x004C48E6 → value+0x74@0x0085B20A/0x0085B211 → klucz insertu@0x008561AC → node+4@0x00854284 — **jeden klucz = komunikat, rekord, węzeł, instancja** | łańcuch VA | **PROVEN** |
| S13 | **UPSTREAM bajtów kursora** (kto wypełnia ring/bufor: sieć vs lokalna kolejka) | 2 callerów dispatchera + vtable (rejestracje kanałów poza zakresem) | **UNPROVEN (jawne)** |
| S14 | kanał 0xB9: FUN_005B72C0 (klucze {u32,u32,u8,u8}/{u32,u32,u8}; walkery; distance-gate; FUN_005B6890 0x42/0x39; FUN_005B6370→FUN_005B5F90; **driver(KEY) @0x005B7567** → builder komponuje pozycję Z ATRYBUTÓW → NOWY klucz przez FUN_00457930) — kanał POCHODNY (propagacja), nie deserializacja pozycji | census + dekompilat | **PROVEN** (rola: propagacja; ERRATA_R4 [SE-R4-1]) |
| S15 | VFS → mapa parametrów: **NEGATYW (bounded)**: funnel insertu (FUN_00856190←FUN_004C46C0←6←FUN_00457930 8) — 0 krawędzi z rodziny 0x0094xxxx; parsery FUN_0094BD30/FUN_0094F350 (2+2 callerów, wszyscy w 0x0094xxxx); FUN_00730C90←FUN_0072FA30 = rejestr DEFINICJI (kontrola pozytywna Fazie A odtworzona własnymi bajtami: string "Parameters\templates.vfs"→FUN_00972DF0→parser→FUN_0072F8D0) | census E8 własny | **PROVEN (negative, bounded)** |

## 3. MACIERZ KLUCZY/RECEIVERÓW (E1-E18 executora — zweryfikowana + korekty)

Macierz E1-E18 + napędy A/B/C (02_ANALYSIS\KEY_MODEL_MATRIX.md) —
**zweryfikowana**: wszystkie censusy i piny krawędzi powtórzone własnymi
bajtami (E1-E18: brak zmian poza poniższymi notami). Korekty/kwalifikacje:
- **E1/E3/E3'/E5 (0xB9):** PROVEN jako kanał KLUCZOWY (round-1 zatwierdzone);
  0xB9 **nie** deserializuje pozycji (korekta zbioru typów — [SE-R4-5]);
  subtype reader FUN_007527F0 = u16 (advance 2), przed nim handler robi
  inline skip-4 (nieczytane 4 B).
- **E6/E6' (getterD w driverze):** PROVEN + **receiverzy rozstrzygnięci**
  ([SE-R4-4]): @0x00567D16/@0x00567D46: ECX=ESI=arg3 (rekord stanu, czyta
  [+0x10]); @0x00567F72: ECX=[ESP+0x20]=this (kolejka); pin
  `8B 4C 24 20` @0x00567F56.
- **E8 (singleton CMP):** pin `8B C8 E8 15 65 26 00; 3B E8`
  @0x00567CC4-0x00567CCB potwierdzony; singleton = `[0x00BA1260]` przez
  FUN_004143F0 (lazy, PUSH 0x4C); semantyka „własny klucz awatara" = HIPOTEZA.
- **E10/E11 (builder):** f90-site @0x00567906 ✓ (pin T6 zgodny); builder
  komponuje pozycję z atrybutów klucza (walker) i rejstruje NOWY uchwyt
  (FUN_00457930 → EAX) — klucz budowanego rekordu ≠ klucz komunikatu 0xB9
  (zamknięta dwuznaczność z Fazy A [SE-R4-3]).
- **E18 (composer):** piny brzegowe (FUN_0085AD50=`8D 81 88 00 00 00 C3`;
  getterA census 808+9) potwierdzone; selektor 0x4E38 = re-użycie dekodu PKG_A
  (14/14, jump-table 0x00855BB4) — jawnie NIE re-dekodowany instrukcja-po-
  instrukcji w tym runie (NOT_CHECKED cząstkowe).
- **[P3]:** hasha = **DIV** (nie IDIV) — [SE-R4-7a]; piny kontekstowe —
  [SE-R4-7b].

## 4. TWIERDZENIE → ŹRÓDŁO → POMIAR → KONTROLA → WYNIK → ARTEFAKT

| Twierdzenie | Źródło (własne bajty) | Pomiar | Kontrola (negative/distinguish) | Wynik | Artefakt |
|---|---|---|---|---|---|
| Klasa wartości mapy = MovableObject/ClientMovableObject | RTTI: vtable 0x00A91E4C→COL 0x00AB33D0→TD 0x00B7997C→`.?AVMovableObject@@`; 0x00A7DCB0→`.?AVClientMovableObject@@` | łańcuchy RTTI własne; slot-0 DWORD scan = 1 hit | unikalność slot-0 (1 hit); imm32 3×/2× (ctor+dtory); kontrola odróżniająca getterA+8 (map-value=wariant vs class=ID vs rekord=A) | **CONFIRMED** | QC_REPORT §1g; T1/T6 executora |
| Insert-seam VA-locked | dekod FUN_00856190/00854260/00854D90/00856090/00971780/008544D0 | wszystkie instrukcje kluczowe wylistowane z VA | duplikat→deleting-dtor (6A 01 FF D2); `[+0x74]==0`→brak insertu; DIV-vs-IDIV check | **CONFIRMED** | QC_REPORT §1h/i |
| Klucz = uchwyt instancji z komunikatu | łańcuch VA S12 | 5 ogniw jednego klucza | ID param-setu (0x4E34/0x4E38/0x5DC9/0x38B0) = atrybut +0x88 (CMP w selektorze/processorze), NIE klucz; 0x6A4-rodzina = kolumny drzewa | **CONFIRMED** | QC_REPORT §1j; KEY_MODEL_MATRIX §3 |
| Pozycja z kursora → placement+8..0x10 → instancja+0x44..0x4C | dekod S6-S9 | VA każdej operacji odczytu/kopii | ścieżka EXISTING używa tego samego pola (FUN_0085B3E0 @0x004C4875); Y2/bajt@+0x5C = read-but-unused (skan 0 odwołań) | **CONFIRMED** (z korektą pól [SE-R4-6]) | QC_REPORT §1c/d; ERRATA_R4 |
| Zbiór typów deserializujących = {0xB0,0xC6,0xC7,0xB2} | census E8 FUN_004C47F0=4 + dekod bramek | 4 site'y dokładnie | handler 0xB9 bez call-site'u; byte-table[0xB2]=default→bramka w Execute; RTTI vtable 0x00A7C200=ArkClientPacketExecutor | **CONFIRMED** (korekta [SE-R4-5]) | QC_CENSUS.json; QC_DISPATCHER.json |
| Źródło insertów = komunikaty (VFS=negatyw) | census funnelu + kontrola pozytywna VFS→rejestr definicji | 1+6+8 callerów — 0 z 0x0094xxxx | bounded: E8-direct only; payload parserów poza zakresem (jawne) | **CONFIRMED** (bounded) | QC_REPORT §1m |
| Kanał 0xB9 = klucze/propagacja (round-1) | dekod FUN_005B72C0 + census | pełna konsumpcja {skip4,u16,4,4,1,1} / {skip4,u16,4,4,1} | brak FUN_004C47F0/FUN_007453D0 w handlerze; driver kluczowy | **ZATRZYMANE** (ERRATA_R4 [SE-R4-1]) | QC_REPORT §1a |
| GB6 immutability | repeat własny: composite 8/8 + per-plik 1385/1385 | before==after==now | — | **PASS** | QC_GB6_REPEAT/PERFILE.json |
| Era/determinizm | S0 executora (SHA obie) + własny PE parse; SCRIPT_SHA256 19/19 MATCH | — | mismatch=HARD STOP (nie wystąpił) | **PASS** | QC_REPORT nagłówek |

## 5. OSOBNE ODPOWIEDZI (na pytania człowieka §7)

**(a) Co identyfikuje MODEL (w kanale movable)?** — W tym runie NIE
rozstrzygnięto wiązania instancja↔model dla kanału movable: ctor pochodny
wykonuje lookup PO KLUCZU (`FUN_00414130([+0x74])` → FUN_005247C0 →
new(0x98)+FUN_00509330 → sub-obiekt `[+0xC0]`; create arg3 = wskaźnik pustego
stringa przez singleton [0x00BA26B8]). Dekod sub-obiektu +0xC0 i singletonu
tworzenia = granica (§6.5). Dla STATYKÓW: identyfikacja modelu = stan rund
poprzednich (A→`<A>.nif`, join 3618/3618 CONFIRMED w ROUND) — bez zmian.
**(b) Jak powstaje INSTANCJA (movable)?** — komunikat typu {0xB0/0xC6/0xC7/0xB2}
→ procesor FUN_004C47F0 deserializuje z kursora {klucz, wariant u16, pozycja
vec3, rotacja vec3, wektor-2, para param-set} → buduje rekord placementu 0x2C
(klucz@+0, X2@+4, pozycja@+8..0x10, rotacja@+0x14.., param-set@+0x20/+0x24) →
FUN_004C46C0: new(0x128) → ctor ClientMovableObject(→MovableObject) → insert
{klucz, instancja} do hash-map @mgr+0x10. Istnieje też kanał POCHODNY: 0xB9 →
driver(klucz) → builder komponuje pozycję z ATRYBUTÓW i rejstruje NOWY uchwyt.
**(c) Skąd jest TRANSFORM (movable)?** — z bajtów KURSORA komunikatu (S6:
sub-pakiet vec3 12 B → f90). Upstream kursora = NIEUDOWODNIONY (sieć vs lokalna
kolejka — §6.1); NIE ogłaszamy „z sieci". **Dla STATYKÓW: NADAL UNKNOWN**
(atrybut-drzewo jako warstwa propagacji H2 — bez zmian; kandydaci
FUN_00567170/FUN_005B5F90/FUN_006CB6F0 bez zmian).
**(d) Czy odzyskano autentyczne pozycje 296445?** — **NIE.** Żadna wartość
nie została ogłoszona jako „odzyskana lokalizacja historyczna"; D@4508=124.941
pozostaje ANCHORS_ABSENT_SEMANTICS_OPEN; pozycje 296445 NIEODZYSKANE.

## 6. GRANICE (jawne, wejście do następnej rundy)

1. **Upstream kursora** (S13): NIEUDOWODNIONY — 2 callerów dispatchera
   (FUN_004B1B70 ring-pump; FUN_004B2950=Execute vtable @0x00A7C200,
   RTTI=ArkClientPacketExecutor) + dynamiczne rejestracje kanałów poza
   zakresem. Sieć vs lokalna kolejka — otwarte.
2. **Osie/jednostki value+0x44..0x4C** — UNRESOLVED (konsument=kompozycja
   selektora: slot3[i]+[+0x44]; wymaga dekodu slot3 FUN_0085B6A0 +
   FUN_008599A0).
3. **Statyki vs movable** — kanał z §2 dowiedziony TYLKO dla klasy wartości
   MovableObject/ClientMovableObject; statyki (4508/296445) NIE wykazane w tym
   kanale (0/38 STATIC_WORLD z RUN3 bez zmian; kandydaci bez zmian).
4. **[singleton 0x00BA1260+8] vs klucz** — HIPOTEZA „własny klucz awatara"
   (właściciel singletonu poza zakresem).
5. **Wiązanie modelu movables** (sub-obiekt +0xC0; singleton [0x00BA26B8];
   string tworzenia) — poza szwem.
6. **19 ctor-callers bez setterów (Faza A)** — NOT_CHECKED, bez zmian.
7. **Bounded negatyw VFS** — census E8-direct; payloady parserów 0x0094xxxx
   poza zakresem (jawne).
8. Composer/selektor wewnętrzne — re-użyty dekod PKG_A (nie re-dekodowany).

## 7. DOKŁADNE LICZEBNOŚCI (censusy własne = deklaracje executora)

insert FUN_00856190: **1** (@0x004C47DA) · creator FUN_004C46C0: **6**
(FUN_004C47F0, FUN_00456F40, FUN_0050BED0, FUN_00442190, FUN_00441910,
FUN_004B3A00) · processor FUN_004C47F0: **4** (@0x00457594/0x004B0B47/
0x004B171A/0x004B1DBC) · resolver FUN_008544D0: **4** · ctor MovableObject:
**1** · ctor ClientMovableObject: **1** · builder FUN_00567770: **1** ·
driver FUN_00567C50: **3** (A 0x0058E0B7, B 0x005B7567, C 0x00515345) ·
keyproducer FUN_00457930: **8** · walker FUN_0085B840: **108** · mgr-getter
FUN_004154F0: **104** · getterA FUN_007CE1E0: **808 E8 + 9 E9** · getterD
FUN_0048ADA0: **116 E8 + 1 E9** · attr-writer FUN_00845F70: **53** ·
find-or-create FUN_00854D90: **18** · node-init FUN_00854260: **2** ·
rehash FUN_00856090: **1** · dispatcher FUN_004B18D0: **2** · handler 0xB9
FUN_005B72C0: **1** · handlery 0xB0/0xC6/0xC7: **1/1/1** · read-cursor
FUN_00752700: **1** · FUN_00752640: **1** · FUN_007527F0: **5** (0xB9+4 innych
rodzin) · deserializer FUN_007453D0: **1** · FUN_00745360: **1** ·
FUN_005B5F90: **3** (wszystkie w FUN_005B6370) · FUN_006CB6F0: **2** ·
FUN_00567170: **1** · parsery VFS FUN_0094BD30/FUN_0094F350: **2+2** (0
krawędzi do funnelu) · FUN_00730C90: **1** (FUN_0072FA30) · advance
FUN_0040DE60: **715** · deref FUN_004123D0: **724** · slot-0 0x0085B7F0:
**1 hit** · imm32 0x00A91E4C: **3** · imm32 0x00A7DCB0: **2** · byte-table
dispatcherа: 0x25 wpisów (0xA2..0xC7), jump-table: **22** wpisów · GB6:
8 pakietów / **1385 plików** per-plik identycznych (repeat własny) ·
SCRIPT_SHA256: **19/19 MATCH** · evidence hash przed/po QC: **0 zmian**.

## 8. NASTĘPNY EKSPERYMENT (jeden, STATIC)

**Dekod UPSTREAM kursora:** (1) RTTI właściciela vtable @0x00A7C200 wykonany
w QC (`.?AVArkClientPacketExecutor@@`) — następny krok: **enumeracja callerów
FUN_004B2950 przez vtable** (xrefy danych do 0x00A7C1FC/0x00A7C200 + rejestracje
ArkClientPacketExecutor w CommunicationSubsystem FUN_00419DD0; dekod ringa
FUN_004B1890/FUN_004B1B70: skąd biorą się wpisy {typ,cursor} i kto wypełnia
bufor — rozstrzyga sieć-vs-lokalna kolejka dla kanału movable);
równolegle: **(2) slot3 FUN_0085B6A0 + FUN_008599A0** (osie/jednostki
value+0x44..0x4C — kompozycja selektora), oraz **(3) sub-obiekt +0xC0**
(FUN_005247C0→FUN_00509330 — wiązanie modelu movables). Kolejność: (1) jako
główne (domyka granicę #1), (2)+(3) równolegle.

## 9. Bramki

Executor (06_REPORT\STAGE_ACCEPTANCE_GATES.csv): GB1-VALUE-CLASS **PASS** ·
GB2-INSERT-SEAM **PASS** · GB3-KEY-MODEL **PASS** · GB4-DATA-SOURCE **PASS**
(z korektą [SE-R4-5]: zbiór typów {0xB0,0xC6,0xC7,0xB2}; wiersz CSV był
poprawny) · GB5-PARSER **NOT_APPLICABLE** ✓ (słusznie — ślad insertu nie
prowadzi do Parameters VFS) · GB6-IMMUTABLE **PASS** (repeat auditora
1385/1385) · GB7-ERA **PASS**.
Auditor (dopisane do STAGE_ACCEPTANCE_GATES.csv): QC-1..QC-8 — patrz CSV.

**RUN_STATUS: PASS_WITH_BOUNDARY** (granice §6). NIE ogłoszono
STATIC_INSTANCE_MECHANISM_CONFIRMED; pozycje 296445 NIEODZYSKANE.
