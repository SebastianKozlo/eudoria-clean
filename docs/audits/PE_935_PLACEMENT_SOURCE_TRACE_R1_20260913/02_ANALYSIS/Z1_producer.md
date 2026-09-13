# Z1 — PRODUCENT ATRYBUTÓW PLACEMENTU (backward slice od FUN_00846840)

RUN: PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913 | ERA: EU 9.3.5 (pcg_install)
Binarium SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31.
Wszystkie twierdzenia poniżej: STATIC-PROOF (dekompilacja/disasm; klient NIE uruchomiony)
chyba że jawnie oznaczone RUNTIME-UNOBSERVED.

## 1. Struktura kontenera atrybutów (a) — VA-locked

System atrybutów = **manager singleton 0x8c B** (DAT_00ba12e8; getter FUN_004154f0
@0x004154F0; ctor FUN_008550c0 @0x008550C0: 3× InitializeCriticalSection przez
FUN_00413590 + wewnętrzna mapa {head@+0x30/0x34/0x38}) + **walkery**:

```
FUN_00843d60(out, key)          @0x00843D60  *out = key; out[1] = FUN_00841920(key)
FUN_0085b840(walker, key)        @0x0085B840  FUN_004154f0() [singleton]
                                             -> FUN_008544d0(key) @0x008544D0:
                                                FUN_00413440 [EnterCriticalSection]
                                                FUN_00971780 [map find] -> [hit+8]
                                                FUN_00413450 [LeaveCriticalSection]
FUN_0085b860(node_out)           @0x0085B860  *out = *walker; FUN_0085b190 [current]
FUN_0085acb0 / FUN_0085b050 / FUN_0085b020 / FUN_0085b0a0 / FUN_0085b0b0  readery wartości
FUN_0085b1a0                     @0x0085B1A0  pop/leave
FUN_00844130(obj)                @0x00844130  if [obj+4]!=0 -> FUN_007479b0(...) [container z encji]
FUN_00845f70(attr_id, val)       @0x00845F70  SETTER (walker-push przez FUN_005275e0)
FUN_008452d0(attr_id)            @0x008452D0  GETTER int (0x4E26-family)
FUN_00845360(attr_id)            @0x00845360  GETTER float
FUN_00844020(attr_id)            @0x00844020  CHECK czy istnieje
```

Rekord atrybutu (odczytany przez FUN_00846840/FUN_008553d0): pozycja 3f @+0x44..+0x4C,
obrót 3 dword @+0x5C/+0x60/+0x64, dodatkowe pola @+0x68/+0x6C/+0x70 (FUN_00854720),
flaga-bajt (FUN_0085b050). **Kontener atrybutów jest rozwiązany KLUCZEM u32**
(FUN_008544d0: map-find po kluczu, wynik [hit+8]) — klucz przychodzi z zewnątrz
(entity/message/lookup), a obiekty kontenerów to instancje klasy **ArkParameterContainer**
(RTTI TD 0x00B8ED0C, vtable 0x00A8784C; create-slot0 FUN_00761230 z zapisem vtable
@0x00761278; ArkObjectClassImpl<ArkParameterContainer> vtable 0x00A86FBC slot1
= FUN_0073a160) oraz rodziny ArkParameter* (Transformation TD 0x00B8EC00,
vtable 0x00A877DC, create FUN_00760FE0; SetObject; ServerGlobal/Local; ...).
Semantyka typów atrybutów transformu: pary {0x6a4,0x6a5} / {0x6a8,0x6a9} / {0x23,0x6ac}
(FUN_006bd1b0 @0x006BD1B0: trzy rozłączne mapowania; FUN_00846430 @0x00846430
= filtr "is-transform" dokładnie {0x6a8,0x6a9,0x6a4,0x6a5,0x6ac,0x23}).

## 2. PRODUCENT (b) — trzy skanaly kandydatów

### (i) READER PLIKU — ISTNIEJE, VA-locked (kanał FILE)
- Magazyn parametrów: FUN_0094dfc0 @0x0094DFC0 (singleton DAT_00ba8df4; operator_new(0xa4)
  → ctor FUN_00972380; otwarcie pliku readerem VFS FUN_00972df0) + FUN_0094fe00 @0x0094FE00
  (drugi store); oba budują ścieżkę "Data\Parameters\" (FUN_0094ba00 @0x0094BA00/FUN_0094f250).
- Parser VFS z kursorem: FUN_00730c90 (RUN 3: templates.vfs) + FUN_0094bd30/FUN_0094f350 —
  rodzina używa **tego samego helpera kursora FUN_0040de60** co czytniki kolejek komunikatów.
- Argumenty param-setów w .text: 0x4E25 (20005; 8 trafień), 0x4E27 (20007; 10), 0x4E22 (20002),
  0x4E21 (20001) — **pliki 20001/20002/20005/20007.vfs istnieją lokalnie**; 0x4E26 (20006)
  — 29 trafień, ale **plik 20006.vfs NIE istnieje** (census Data\Parameters — 20 plików,
  brak 20006). 24007 (0x5DC7) — 32 trafienia, plik 24007.vfs istnieje.
- STRONA ODCZYTU atrybutów plikowych jest dowiedziona; **nie domknięto** szwu
  parser→mapa-walkerów dla atrybutów transformu statyków (wstrzyknięcie zawartości
  pliku do drzewa atrybutów encji — patrz GRANICA niżej).

### (ii) DEKODER PAKIETU SIECIOWEGO — ISTNIEJE, ale warstwa connection (H3 nieudowodniona)
- Odbiór: FUN_00833ea0 @0x00833EA0 — pętla odbioru: FUN_00830830 [recv] → FUN_0082f8d0
  [parse frame] → FUN_00830fa0 [kanał] → FUN_008310d0 @0x008310D0 (tworzy **ArkStaticPacket**
  @FUN_00830030; parse: ntohl @+0x20/@+0x1C, flagi @+0x24, chunki 0xFE przez FUN_00839a50,
  rekordy 0xFF-ack). **ArkStaticPacket = protokół POŁĄCZENIA/kanałów** — w jego parserze
  NIE MA dekodowania transformów świata (struktura: sesja/kanał/chunk — STATIC-PROOF).
- ArkPacketDecoder (vtable 0x00A91A6C): jedyna wirtualka = deleting-dtor (FUN_00835660→
  FUN_00835500) — logika dekodowania NIE jest wirtualna; Runnable-y
  (ArkRunnableT1<ArkPacketDecoder,ArkFrameData/ArkPacketObject>, vtable 0x00A91A54/0x00A91A60)
  mają Run @0x00834EC0 = cienki forwarder `(*[this+0xC])(this+4)`.
- **CommunicationSubsystem** (RTTI verbatim w dekompilacie FUN_00419dd0 @0x00419DD0):
  tworzy **ArkClientPacketExecutor** (operator_new(0x34) → FUN_004b15f0 @0x004B15F0,
  vtable 0x00A7C1FC [dtor FUN_004b1210, Execute FUN_004b2950]) na [comm+0x28];
  executor ma ring odroczonych komunikatów (FUN_004b0df0 init; FUN_004b1890 @0x004B1890
  push {type,x,payload} 12B; drain FUN_004b1b70←FUN_004b1c70 = case 0xb2).
- **FUN_004b2950 @0x004B2950 = Execute(type,payload)**: 0xac→FUN_004b2270, 0xb2→FUN_004b1c70,
  bramka FUN_0042bc20 → bezpośrednio FUN_004b18d0 @0x004B18D0 (**switch ~30 typów
  0xA2–0xC6**; case **0xB9 → FUN_005b72c0** = handler, który Czyta bufor zdarzeń
  kursorami FUN_007527f0/FUN_00752700/FUN_00752640 {u32 klucz-kontenera, u32 klucz-rekordu,
  u8, u8} i woła FUN_00567c50 → FUN_00567770 (builder placementu!).
- **GRANICA (jawna)**: producenta komunikatów 0xB9 NIE udało się VA-lockować —
  Execute jest wirtualne (executor vtable slot1), a bezpośredni caller nie istnieje
  w xrefach (0 call-site'ów). Kanał/handler-y rejestrowane dynamicznie
  (boost::bind CommunicationSubsystem::mf1<ArkChannelID>). STATYCZNIE: sieć dostarcza
  ramki 0x11–0x13 + kanały; **nie znaleziono dekodowania transformu świata z bajtów
  sieci do atrybutów** (H3 dla statyków = NIEUDOWODNIONE, nie wykluczone).

### (iii) MECHANIZM POCHODNY/RPC/EVENT (H2) — ISTNIEJE, VA-locked
- Pisarze atrybutów (FUN_00845f70, 53 call-site'y — WSZYSTKIE w kodzie world-object
  klienta 0x0043–0x0051; ZERO w rodzinie sieciowej 0x0082–0x0084):
  - FUN_00514ef0 (handler z tabeli .rdata 0x00A7D764 — patrz Z2): pisze **0x2b/0x2c
    (para X/Y!)** przez FUN_00845f70 + 0x3f1/0x3f5 → woła FUN_004387a0 (setter 0x6a5)
    → FUN_004641f0 → **FUN_00567c50** (łańcuch builderowy).
  - FUN_004387a0 @0x004387A0: FUN_00845f70(0x3f1,1), FUN_005146b0(param,0x6a5,0),
    FUN_00847270(param,0x6a5), FUN_00845f70(0x271b,0x6ac), FUN_00845f70(0x271c,0x6ac).
  - FUN_005146b0 @0x005146B0: propagacja (0x2720/0x271f/0x3f3 po zmianie {0x6a4,0x6ac,0x6a5}).
  - FUN_0043f4b0 @0x0043F4B0: dispatcher zmiany atrybutu → akcje wizualne
    (attach modelu FUN_006c6040/FUN_006c5c00 ze skALĄ 0x3f800000=1.0; attr 0x39=model-id!,
    0x42=0x66=MODEL-typ); switch {0x23,0x6ac,0x6a4,0x6a5,0x6a8} (wewnątrz także 0x6ac→0x23).
  - FUN_00847270 @0x00847270: dispatch typu atrybutu {0x6a4/0x6a5→obj 0x619fa;
    0x6a8/0x6a9→obj 0x619f9} → FUN_008553d0 (konstruuje obiekty Z drzewa atrybutów;
    param-sety 0x4E34/0x38b0/0x4E38; odczyt +0x44/+0x48/+0x4C pozycji i +0x5C..+0x64 obrotu).
  - FUN_00468910 @0x00468910 (5,3 KB, silnik per-frame update world-objectu; 12 callerów
    z rodzin world; rekurencja z przejściem stanów; w tym: FUN_0058db50 ×3 → FUN_00567c50,
    attr 0x6a4/0x6a8 jako parametry, odczyty D-getterem FUN_0048ada0 ×5).
- FUN_00490010 (hub requesterów; caller FUN_00490310 ← FUN_00415af0) woła
  FUN_0048f930/FUN_0048fcc0/FUN_0048fe60 (requestery atrybutów → settery).

## 3. WERDYKT-ŹRÓDŁO (c)

**UNKNOWN-with-exact-boundary** (uczciwie; nie FILE, nie NETWORK, nie BOTH — żaden
nie domknięty instrukcyjnie do granicy). Co jest dowiedzione STATIC-PROOF:

1. Transformacje rekordów placementu są czytane **wyłącznie z drzewa atrybutów**
   encji (FUN_00846840 switch 0x6A4/0x6A5/0x6A8/0x6A9 + FUN_00854720; RUN 3 + ten run).
2. Drzewo atrybutów jest systemem klienckim: klucze u32 → mapa managera 0x8c;
   kontenery = obiekty klasy ArkParameterContainer (create FUN_0073a160/registry wirtualne).
3. Kanał FILE istnieje (store "Data\Parameters\" + parsery VFS z identycznym kursorem);
   **ale** brak pliku-placementów statyków w census lokalnych danych (Portals.bnt —
   patrz Z3: zero ID template'ów w 276 .prt; brak 20006.vfs; 20xxx.vfs = parametry,
   nie rozstrzygnięte jako nośnik transformów statyków).
4. Kanał NETWORK istnieje jako infrastruktura (CommunicationSubsystem → executor →
   case 0xB9 → builder), ale warstwa pakietowa jest connection-protocol; producent
   payloadu 0xB9 niewirtualnie nieosiągalny statycznie (rejestracja dynamiczna).
5. Kanał POCHODNY/LOKALNY (H2) jest udowodniony jako mechanizm propagacji
   (FUN_00514ef0/004387a0/005146b0/0043f4b0 piszą atrybuty transformu z kodu
   world-object).

**GRANICA (co trzeba dynamicznie, jawne)**:
- kto FIZYCZNIE wypełnia kontener atrybutów STATYKU danymi pozycji (pkt startowy
  danych): (a) load z 20xxx.vfs do drzewa — domknąć trace parser→insert-mapa;
  (b) komunikat 0xB9 z sieci — wymaga runtime capture (zakazane w tym runie);
  (c) ustalić callery wirtualne (executor/channel-handler-y) — rejestrowane
  boost::bind, statycznie tylko deskryptory.
- Z tego wynika: H1 (plik niosący placementy statyków) — brak pozytywu w censused
  danych; H2 (pochodne/propagacja) — dowiedziona jako warstwa, ale to propagacja
  **istniejących już** wartości; H3 (sieć) — kanał istnieje, transform-dekod
  nieudowodniony; H4 — nie wykluczony (0xB9 = główny otwarty kandydat).
