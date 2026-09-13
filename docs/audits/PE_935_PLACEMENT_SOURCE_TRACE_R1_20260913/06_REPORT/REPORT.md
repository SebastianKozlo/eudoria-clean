# RAPORT — PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913

**KTO i Z JAKICH DANYCH produkuje transformacje rekordów placementu statycznych
obiektów w Entropia.exe EU 9.3.5 — stan na dziś (STATIC-ONLY; klient nieuruchomiony).**
Era: EU 9.3.5 (pcg_install). Binarium SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE613
89689A22F753765D5280F31 (8,015,872 B, image base 0x00400000, brak ASLR — S0 fail-closed).

---

## 1. WERDYKT-ŹRÓDŁO transformacji statyków (co dziś wiemy i z jakim dowodem)

**UNKNOWN-with-exact-boundary** — przy pełnym łańcuchu maszyny placementu
VA-locked i trzech skanowanych kanałach, żaden producent DANYCH pozycji statyku
nie został domknięty instrukcyjnie. Szczegółowo (wszystko STATIC-PROOF z
dekompilacji/disasmu/bajtów; RUNTIME-UNOBSERVED = to, czego bez uruchomienia
rozstrzygnąć się nie da):

1. **Transform wchodzi do rekordu placementu WYŁĄZNIE z drzewa atrybutów encji**
   (FUN_00846840: switch atrybutów 0x6A4/0x6A5/0x6A8/0x6A9; + FUN_00854720
   trójka +0x68/+0x6c/+0x70 — RUN 3 + re-walidacja S5/Ghidra tego runu).
   Typy transformu: pary {0x6A4,0x6A5}/{0x6A8,0x6A9}/{0x23,0x6AC}
   (FUN_00846430 = filtr dokładnie tych 6 ID; FUN_006bd1b0 = resolver par).
2. **Drzewo atrybutów = system kliencki**: manager singleton 0x8c
   (DAT_00ba12e8, 3× CriticalSection + mapa; resolve klucz-u32→[hit+8] przez
   FUN_008544d0); kontenery = obiekty **ArkParameterContainer** (RTTI nowego
   runu: rodzina ArkParameter* z create-metodami ArkObjectClassImpl — dispatch
   wirtualny rejestru klas).
3. **Kanał FILE istnieje** (store "Data\Parameters\" FUN_0094dfc0/FUN_0094fe00
   + parsery VFS z identycznym systemem kursora co kolejki komunikatów), ale:
   brak lokalnego pliku-placementów statyków (Portals.bnt/.prt — patrz pkt 3:
   czysty cell-graph dPVS; census Data\Parameters: 20 plików .vfs parametrów,
   **20006.vfs nie istnieje** mimo 29 użyc ID 20006 w .text; 20xxx.vfs
   nie rozstrzygnięte jako nośnik transformów statyków — szew
   parser→drzewo nie domknięty).
4. **Kanał NETWORK istnieje jako infrastruktura, ale transform-dekod
   NIEUDOWODNiony**: CommunicationSubsystem (RTTI verbatim, FUN_00419dd0)
   → ArkClientPacketExecutor (FUN_004b15f0, 0x34 B, Execute FUN_004b2950,
   ring odroczeń FUN_004b1890) → dispatcher typów FUN_004b18d0
   (0xA2–0xC6) → **case 0xB9 → FUN_005b72c0 → FUN_00567c50 → FUN_00567770
   (builder!)**; warstwa pakietowa (ArkStaticPacket, FUN_008310d0: ntohl,
   chunki 0xFE, acki 0xFF) = **protokół połączenia/kanałów — zero dekodowania
   transformów świata**. Producent payloadu 0xB9 = handler rejestrowany
   dynamicznie (boost::bind) — statycznie nieosiągalny xrefem (granica jawna).
5. **Kanał POCHODNY/LOKALNY (H2) udowodniony jako warstwa propagacji**:
   FUN_00845f70 (setter atrybutu) ma 53 call-site'y — WSZYSTKIE w kodzie
   world-object klienta (0x0043–0x0051), ZERO w rodzinie sieciowej; m.in.
   FUN_00514ef0 pisze {0x2b,0x2c} (para X/Y) i woła builder, FUN_004387a0
   ustawia rodzinę 0x6a5, FUN_005146b0 propaguje, FUN_0043f4b0 po zmianie
   attr 0x39(model-id)/0x42(0x66) ATTACHUJE model ze skALĄ 1.0.

**Granica (co trzeba dynamicznie / w kolejnym runie)**: fizyczny punkt, w którym
dana pozycja STATYKU po raz pierwszy trafia do jego kontenera atrybutów:
(a) trace parser→insert-map dla 20xxx.vfs, (b) runtime-capture komunikatu 0xB9
(zakazany w tym runie), (c) rozbiór wirtualnych rejestracji kanałów.
Hipotezy: H1 — brak pozytywu w censused danych lokalnych; H2 — warstwa
udowodniona, ale propaguje istniejące wartości; **H3 — kanał istnieje, dekod
nieudowodniony; H4 — nie wykluczony (0xB9 = główny otwarty kandydat)**.
Network-first pozostaje odrzucone jako ZAŁOŻENIE (bez zmian ERRATA_R2).

## 2. Łańcuch CWO / ArkObject (pełny diagram: 02_ANALYSIS\Z2_cwo_chain.md)

Rekord placementu (pozycja@+0x08, rotacja@+0x14) buduje **FUN_00567770**
z trzech niezależnych napędów przez wspólny driver FUN_00567c50:
- **droga A**: FUN_00468910 (silnik per-frame update CWO; state machine;
  attr 0x6A4/0x6A8 jako argumenty) → FUN_0058db50 ×3 → FUN_00567c50;
- **droga B**: executor Execute → dispatcher FUN_004b18d0 case 0xB9 →
  FUN_005b72c0 (odczyt bufora zdarzeń kursorami: {u32 klucz,u32 klucz,u8,u8})
  → FUN_00567c50;
- **droga C**: **tabela handlerów .rdata 0x00A7D764** (sąsiedztwo stringów
  "ArkClientWorldObjectLogic::…") → **FUN_00514ef0** (transform-handler:
  pisze X/Y 0x2b/0x2c, woła setter-rodzinę 0x6a5 i builder).
FUN_00567770: odczyt pozycji/obrotu z atrybutów (oba muszą się udać — inaczej
rekord nie powstaje), ctor rekordu FUN_00730700, deriver sub-obiektów
FUN_004c5580 ("Level01_0_BASE"/"volume_0_BASE"/…), settery FUN_00730f90/fb0/fd0,
rejestracja nazwana FUN_004148f0/FUN_00457930, push do kolejki update
FUN_00567b40 (capacity-gated; argument D).
Encje: klasy ArkRealWorldItem/ArkRealWorldProvider/ArkInteractiveWorldObject
(create-y wirtualne przez rejestr ArkObjectClassImpl; most template→encja
bez zmian z RUN 3 — ctor FUN_00726e70, A@+0x28; instancja modelu FUN_006cb6f0,
attach przez attr 0x39/0x42).
Krawędzie NIEUDOWODNIONE (jawnie): (a) producent danych transformu (pkt 1);
(b) rekord-placement→węzeł NIF statyka (bez zmian RUN 3); (c) komplet ciał
wirtualnych rejestru klas (Service/Commander/Manager).

## 3. Portals.bnt / .prt — reader, struktura, rola

**Reader ZNALEZIONY i struktura ZDEKODOWANA z bajtów** (walidowana przeciw
readerowi; pełne: 02_ANALYSIS\Z3_portals.md):
- fabryka ArkPortalResourceItemFactory (vtable 0x00A91C88) slot1 FUN_0084b270
  → item-ctor FUN_00852a90 (CellGraph@+0x10, 0x58 B) → FUN_0084f7a0(payload);
- parser grafu FUN_00852750: u16→[graph+0xac], sub-blok FUN_008539f0
  (boundsy AABB f32 — próbka 382811: -6.001/+6.001, -2.437/+2.4966,
  -0.000388/+3.812), u32 liczba komórek, pętla: u32 id → komórka 0x90 B
  (ArkPortalCell, vtable slot1 FUN_00852A30: bajt-tag → sub-bloki);
- indeks BNT skalibrowany: stopka [int32 index=73218]['BNT2'], wpisy
  {name\n, size, offset, int64} — **276/276 .prt**, 0 naruszeń granic,
  rozmiary 42–1990 B; próbki kontraktowe: 18 wpisów w oknie 505k–510k
  ( enumerated), outliery 382811/422806/592739/592741 — wszystkie istnieją;
  finiteness nagłówków OK.
**Rola: wyłącznie cell-graph dPVS — NIE nośnik placementów.** Dowód strukturalny
negatywny: skan wszystkich 276 payloadów: **0 trafień** template'ów (4508/4752/
2249), ID .nif (296445/126740/278453), .bvi (296446), param-setów (20005/20006/
20007), msgtype 0xB9, atrybutów 0x6A4/0x6A8 (S12; 13 anchorów; round-trip
przed skanem).

## 4. Pole D (PARAM f32; 4508: 124.941) — konsument rozstrzygnięty częściowo

Getterzy stubowy (S9; walidacja Ghidrą): **D(+0x10) dword = FUN_0048ada0
@0x0048ADA0 (8B 41 10 C3)** — 80+ call-site'ów; **D f32 = FUN_00861240
@0x00861240 (D9 41 10 C3)** — 10 call-site'ów; (B=FUN_00746550, A=FUN_007ce1e0,
C=FUN_006b22d0 — bez zmian kanonu). Konsumentów D zaklasyfikowano:
- FUN_008553d0 (konstruktor-walker): D steruje selekcją wariantu (gałąź 0x4e38:
  D=4/5→2, 6→3, 7→4) i trafia do inicjalizacji obiektu;
- FUN_00567c50→FUN_00567b40: D jako argument capacity-push do kolejki update;
- FUN_00861390/0x00529-0x00528x: rodziny distans/LOD (f32-D);
- FUN_00468910 ×5: update world-objectu.
**Semantyka D = parametr multi-konsumenta** (selektor wariantu / wartość
kolejkowa / distans-LOD). Konkretna wartość 124.941 (4508) — promień czy level:
RUNTIME-UNOBSERVED (statycznie nierozstrzygalne); konsumentów — STATIC-PROOF.

## 5. Diagram źródło→instancja→template→transform

Pełny diagram z ogniwami VA-locked: 02_ANALYSIS\Z2_cwo_chain.md §4.
Krawędzie NIEUDOWODNIONE (jawnie, bez zmian + nowe): (a) producent danych
transformu (3 kanały-skanowane — pkt 1); (b) rekord-placement→węzeł NIF;
(c) wirtualne ciała rejestru klas; (d) semantyka liczbowa D=124.941;
(e) producent komunikatu 0xB9 (rejestracja dynamiczna).

## 6. NOT_CHECKED (jawna lista)
1. FUN_0084f7a0 — dekompilacja ciała (struktura .prt wywnioskowana z
   FUN_00852750/FUN_00852A30/FUN_00852bf0 + bajtów — spójna; ciała nie zdekompilowano).
2. TerrainEditZones.bnt (54,156 B) — bez zmian (RUN 3).
3. Komplet ciał ArkObjectService/Commander/ArkClientObjectManagerImpl +
   tabele handlerów 74/72 @0x00A7D8EC/0x00A7DA34 (enumeracja head-ów w S13).
4. Pole aux int64 indeksu BNT (nietypowane pary 0xB2A7C844-style).
5. FUN_00841920 (worker resolvera) — dump jest (ZS10), analiza pól niepełna.
6. Runtime-capture 0xB9 / sieć / mock — ZAKAZANE w tym runie (HARD STOP);
   NIE WYKONANO (dla jasności: ten run jest w 100% statyczny).

## 7. Otwarte kandydaty (posortowane wg wartości)
1. **Domknięcie producenta 0xB9** (największa wartość): statyczna enumeracja
   rejestracji kanałów CommunicationSubsystem (bind-y mf1<ArkChannelID>) +
   runtime-capture w autoryzowanym runie dynamicznym — rozstrzyga H3/H4
   dla statyków.
2. **Trace parser→drzewo atrybutów** dla 20xxx.vfs/24007.vfs (szew
   FUN_0094bd30/FUN_0094f350 → FUN_008544d0-mapa) — rozstrzyga H1.
3. **20006 (0x4E26)**: 29 użyc, brak pliku — skąd dane (sieć? inny plik?
   derivation?) — osobny mikro-run (census czytników + wartości).
4. Tabele handlerów CWO-Logic (0x00A7D8EC/0x00A7DA34) — pełna mapa typów
   komunikatów świata (dopełnia executora 0xA2–0xC6).
5. Semantyka D dynamicznie (124.941 przy 4508) — dopiero z runtime.

---

## Bramki (fail-closed)
- **G1-PRODUCER: PASS_WITH_BOUNDARY** — werdykt UNKNOWN-with-exact-boundary;
  łańcuch VA-locked do granicy: system atrybutów (manager/walker/settery/
  gettery + typy 0x6A4-family), 3 kanały zskanowane (FILE/NETWORK/DERIVED),
  granica = punkt wstawienia danych do kontenera atrybutów statyku
  (wirtualne rejestracje + brak xref — jawne; brak domknięcia = brak
  fałszywego werdyktu FILE/NETWORK/BOTH).
- **G2-CWO: PASS** — creator→setters→attach: 3 napędy (A/B/C) VA-locked;
  diagram z ogniwami; krawędzie nieudowodnione oznaczone jawnie (5 pozycji).
- **G3-PORTALS: PASS** — reader znaleziony (fabryka→ctor→FUN_00852750);
  struktura .prt zdekodowana z bajtów i zwalidowana przeciw readerowi
  (tag-bajt, u16, sub-bloki, u32 count, komórki; boundary 0 naruszeń);
  rola = cell-graph dPVS z dowodem negatywnym (13 anchorów × 276 plików = 0).
- **G4-D-FIELD: PASS_WITH_BOUNDARY** — getterzy D zidentyfikowane bajtowo
  (FUN_0048ada0/FUN_00861240), 90 call-site'ów zaklasyfikowanych do 4 rodzin
  konsumentów; konkretna semantyka liczbowa 124.941 = RUNTIME-UNOBSERVED (jawna).
- **G5-ERA: PASS** — S0 fail-closed (SHA+PE+mapping+spot-checki); zero
  transferu PE2/2003; Gb12 tylko jako oracle (bez zmian RUN 3); wszystkie
  VA z tego binarium (S14 = bajty pod każdym cytowanym VA).
- **G6-GENERALITY: PASS** — drugi przypadek dla każdej ścieżki (tabela w
  Z5 §1: 7 ścieżek); kontrole negatywne: atrybut-nieistniejący→rekord nie
  powstaje (decompile-proof), filtr wrong-ID→0, dystans-gate, 0x66AA-negatyw,
  fałszywe trafienia 0x6a4 z powodami wykluczone.

## SELF_CHECK (własny, jawny — NIE audyt PE-MASTER)
- S0 SHA/ASLR/mapping PASS; BASE_SHA 4d4cde5c zweryfikowane (HEAD==origin/master;
  dirty: wyłącznie obce ?? experiments/ — nietknięte).
- GHIDRA_LOCAL skopiowany do run-dir (379,520,056 B; manifest niezmieniony).
- 10 tur Ghidry (zs1–zs10) — wszystkie DONE; każda z hashem skryptu
  (SCRIPT_SHA256.csv) i logiem analyzeHeadless.
- Censusy callerów z limitem 80 — oznaczone where applicable (FUN_0048ada0
  ma >80 — census ucięty na 80, pełna liczba w JSON).
- Kontrole §11: round-trip przed każdym skanem; finiteness na f32 (próbki .prt);
  STATIC-PROOF vs RUNTIME-UNOBSERVED etykietowane; pułapki (stack-offsety,
  pola klas, koincydencje instrukcji) wykluczone z powodami.
- Brak modyfikacji oryginałów: Portals.bnt/Entropia.exe/Parameters —
  wszystkie skrypty tylko czytają (READ-ONLY).
