# RAPORT — PE_935_STATIC_INSTANCE_TRACE_R1_20260913

**Jak kod EU 9.3.5 tworzy instancję statycznego obiektu świata i skąd jej transformacja — stan na dziś (STATIC-ONLY).**
Era: EU 9.3.5 (pcg_install). Binarium SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (8,015,872 B, image base 0x00400000, brak ASLR — asercja S0 fail-closed).

---

## 1. Odpowiedź (na dziś)

W 9.3.5 instancja statycznego obiektu świata powstaje w **trzech warstwach** (łańcuch
VA-locked w warstwach 1–2; warstwa 3 częściowo):

1. **Encja**: `ArkObject` (ctor `FUN_00726e70` @0x00726E70) przyjmuje **obiekt template'u**
   i getterem A (`FUN_007ce1e0` = `[ECX+0x08]`, adres-zablokowany w poprzednim runu)
   zapisuje **A (id pliku .nif) do encji @+0x28**. Fabryka: `ArkObjectClass` vtable slot 1
   (`FUN_0070bf50`: `new(0x58)` → ctor ArkObject). Istnieje 40 call-site'ów ctora —
   fabryki per klasa (np. ctor `ArkSurgeonObject` `FUN_007351e0` z globalnym template'em
   `DAT_00ba58cc`). **To jest most template→encja statycznej**: definicja (template) jest
   osobna od instancji (ArkObject), zgodnie z gramatyką record-vs-instance.

2. **Zasób/instancja modelu**: żądanie `{0x66=MODEL, id=A}` pumpem `FUN_006c9700` →
   ArkResourceManager → provider-chain (BNT2/Models.bnt; otwarcie fizyczne =
   STRONGLY_SUPPORTED z poprzedniego runu). **Twórca instancji modelu**:
   `FUN_006cb6f0` @0x006CB6F0 — cache-lookup(A) w mapie [store+0x3C] → pump →
   `new(12)` + **ctor `ArkModelResourceInstanceRef`** (`FUN_006fa8b0`; vft 0x00A864B8,
   licznik@+0x04, item@+0x08; baza ArkRefObject vft 0x00A864B0) → **`FUN_006cb020`**:
   nazwana instancja 0x110 B o nazwie **"<id>__<name>"** (stringstream; check klasy
   "ArkAnimation") → rejestracja (`FUN_006f33a0`). Podsystem wizualny 0x006Cxxxx
   (`FUN_006cb3c0` = procesor kolejki pending-attach {type@+0x5C, A@+0x64}: po załadowaniu
   attach modelu do węzła [cel+8] i czyszczenie deskryptora) domyka asynchroniczne
   ładowanie. Ta maszyna jest **generyczna** (zero hardcode'ów ID budynków w .text).

3. **Transformacja — częściowo**: zlokalizowano **setterzy transformu rekordu placementu**:
   `FUN_00730f90` (pozycja vec3 @+0x08..0x10), `FUN_00730fb0` (rotacja @+0x14..0x1C),
   `FUN_00730fd0` (@+0x20/+0x24), init `FUN_00730f60`. Są zasilane **z systemu
   atrybutów** (`FUN_00846840`: drzewo atrybutów, ID 0x6A4/0x6A5/0x6A8/0x6A9) i
   rejestrowane z nazwami (`FUN_00457930`). Rekordy placementu są POCHODNE (runtime),
   budowane m.in. przez `FUN_00567770`/`FUN_00567170`/`FUN_005b5f90`.
   **GRANICA (jawna)**: nie rozstrzygnięto, czy atrybuty-pozycje dla STATYKÓW pochodzą
   z lokalnych plików Parameters (H1/H2), z sieci (H3), czy hybrydowo (H4). Producer
   kontenera atrybutów nie został VA-locked. Network-first pozostaje odrzucone jako
   ZAŁOŻENIE (bez zmian erraty R2); client-side system atrybutów z transformami jest
   FAKTEM; źródło danych tego systemu = otwarte.

Ważny wynik negatywny: **NO_STATIC_CONSUMER_FOUND** na censurowanej powierzchni
25 lookupów + 13 pumpów (pkt 2) — statyczne budynki NIE przechodzą przez żaden z tych
call-site'ów w sposób placement-driven; redirect na system ArkObject + atrybuty + CWO.

## 2. Tabela klasyfikacji 25+13 (GA-CLASSIFY)

Pełna tabela z dowodami: `02_ANALYSIS/Z2_CLASSIFICATION_TABLE.md`. Skrót:
- **AVATAR_EQUIPMENT**: FUN_00511070 (#1), FUN_0043eae0 (#16), FUN_006b28e0 (#24,25),
  FUN_006b4c50 (pump #7,8), FUN_006bc8e0 (pump #10,11), FUN_006e2610 (#13).
- **PREVIEW_UI**: FUN_0067b800 (#17), FUN_0067c7c0 (#19), FUN_006c2350 (#21, UI table).
- **VEGETATION**: FUN_0094b1d0 (pump #13 — stringi verbatim "ArkVegetationClient::GetModel").
- **MODEL_MACHINERY**: FUN_006c3f50 (#9, emiter pary {0x66,A}), FUN_006cb6f0 (pump #4,
  twórca instancji), FUN_006c6f60/006b73d0/005f5a80/004c83c0/00441200/0094da20 (gettery),
  rodzina 6c (tabelaryczne gettery slotów).
- **OTHER (system atrybutów / ctor-y / rejestracje derived)**: FUN_00733490, FUN_006baa20,
  FUN_00567170, FUN_005b5f90 (setterzy placementu z atrybutów), FUN_00848ea0, FUN_004e68a0,
  FUN_006a3930.
- **UNKNOWN**: FUN_0093be20 (hardcode 0x70D17=460563 — "460563.nif" NIE istnieje lokalnie;
  negatyw udokumentowany).
- **STATIC_WORLD: 0/38.**

## 3. Kwalifikacja FUN_006b4c50 (Z2a) — ROZSTRZYGNIĘTA

FUN_006b4c50 = **konsument AVATAR (body-set)**, NIE ścieżka statyków: dwie pary
slot-table-getter (`FUN_006c2840`/`FUN_006c2870`) → A ×2 (`FUN_007ce1e0`) → pump ×2 →
attach do węzła postaci (detach starego przez vtable+0xA8). Jedyny caller:
`FUN_006b9970` = update postaci — **string "CharacterPosition"** (odczyt węzła pozycji
postaci z modelu, wynik do [obiekt+0x1DC]). Upstream: `FUN_00489810` = setup lokalnego
avatara (łańcuch ResourceManager + płeć: `FUN_006c1f60(2-(stan!=1))`). Stałe
11769/11655/11656/11657 = sloty ciała/wyposażenia avatara. Ścieżka ogólna A→model jest
WSPÓLNA z resztą systemu (generyczna wobec ID — kontrola negatywna: zero stałych
296445/4508 w łańcuchu).

## 4. Trzy wzorce 4508 (GB-PATTERNS) — 3/3 rozstrzygnięte

Wszystkie trzy to **disp32**, nie imm32 i nie odwołania do template'u 4508:
- 0x0053270C → `LEA ECX,[ESP+0x119C]` @0x00532709 (bajty `8d 8c 24 9c 11 00 00`) —
  offset lokalnego obiektu string w ramce stosu funkcji FUN_0052d6d0 (~44 KB).
- 0x00532769 → to samo LEA @0x00532766 (dtor tego stringu: `CALL [0x00A75A5C]` = ~basic_string).
- 0x0083427E → `MOV [ESI+0x119C],EBX` @0x0083427C (bajty `89 9e 9c 11 00 00`) —
  zerowanie pola 0x467 obiektu **ArkCommunicator** (FUN_00834010 = ctor, RTTI
  ArkCommunicator::vftable w dekompilacie).
Dowód pełny: skan .text (round-trip 8/8 przed skanem): 4508 LE = dokładnie 3 hity
(powyższe), BE = 0, 296445 = 0. **Hardcode template'u 4508 w .text nie istnieje.**

## 5. Backward slice (GC-BACKWARD) — wynik z granicą

Dwa VA-locked slice'y (pełne: `02_ANALYSIS/Z4_BACKWARD_SLICE.md`):
- **S-A (transform-setter)**: `FUN_00730f90`/`fb0`/`fd0` (pozycja/rotacja/2-pola rekordu
  placementu @+0x08/+0x14/+0x20) ← `FUN_00567770` (buduje rekord z atrybutów:
  `FUN_00846840`, ID atrybutów 0x6A4/0x6A5/0x6A8/0x6A9) ← `FUN_00567c50`; rejestracja
  `FUN_00457930` (nazwa). **Granica**: producer kontenera atrybutów (plik Parameters vs
  sieć vs encja) — NIEUSTALONY.
- **S-B (instancja modelu)**: `FUN_006cb6f0` → pump → ArkModelResourceInstanceRef →
  instancja nazwana 0x110 B → rejestracja. **Granica**: napęd "placement statyka" nie
  izolowany w podsystemie 0x006Cxxxx (callery: attach "LowerBody"→"Bip01_StartTarget"
  — avatar; FUN_006cd850 = update LOD wizualnego).
Wykluczenia fałszywych trafień (z powodami): (1) ctor ArkSurgeonObject (+0x58..0x60 =
pola klasy, nie NiAVObject); (2) `FUN_006f2af0` = czyszczenie deskryptora pending-attach
(kolizja offsetów z NiAVObject — pułapka udokumentowana); (3) klaster 0x007936-0x00793C =
macierze renderu; (4) klaster 0x00856xx = kwaterniony/macierze lokalne; (5) GetViewerStrings
= czytnik (użyty jako oracle offsetów, nie trafienie).

## 6. Loader-y świata (GD-LOADERS)

- **Jedno centrum rejestracji**: RM-init `FUN_0041dae0` rejestruje magazyny: .nif/.bvi/
  .amu/.tdf/**.prt**(portal-resource)/**.tez** + **portals.bnt** (Portals.bnt 80,682 B)
  + **TerrainEditZones.bnt** (54,156 B) — wszystkie xrefy stringów wskazują na tę funkcję.
- Klasy loaderów (vtable wyznaczone metodą COL): ArkPortalResourceItemFactory,
  ArkTerrainEditZoneFactory/Group, ArkVegetationClimateFactory, ArkTerrainPatchFactory,
  ArkEffectSequenceFactory, ArkResourceDataStore{Bunt,VFS,File,FileName,Audio}.
- Check definicji portalów w NIF: `FUN_006f1b90` ("m_ContainsPortals"/"m_ContainsPortalDefinitions").
- Scena: korzeń "NetImmerseScene::Root" (`FUN_00933310`); parametry: "Data\Parameters\"
  (`FUN_0094ba00`/`FUN_0094f250`).
- **Negatywy**: brak klas ArkSector/ArkRegion/ArkEntity w RTTI 9.3.5 (0 hitów); brak plików
  Sectors.xbc/Objects.pak/Planets.pak (to era 10.4). Przestrzeń cell = wyłącznie
  ArkPortalCell (portal/dPVS). Statyki NIE mają sektorowego modelu klienta w 9.3.5.

## 7. Diagram: źródło danych → instancja → template/model → world transform

```
[templates.vfs (5,438 rekordów)]                    [Parameters\*.vfs 20xxx/24007]     [Portals.bnt/.prt] [TerrainEditZones.bnt/.tez]
        | reader FUN_0072fa30 (ArkVFS02)                    | (loader-y parametrów FUN_0094ba00/0094f250)     | (RM-init FUN_0041dae0)
        v                                              v                                                  v
[REJESTR template'ów (RB-tree, DAT_00ba1824)]   [SYSTEM ATRYBUTÓW/parametrów]              [ArkPortalCell/CellGraph (dPVS)]
        | lookup FUN_0072f580                            | drzewa FUN_0085b8x0; ID 0x6A4/0x6A5/0x6A8/0x6A9
        v                                              v
[obiekt template'u {B,A(id .nif),C,D f32}]--FUN_004c5580-->[REKORD PLACEMENTU {pozycja@+0x08, rotacja@+0x14, +0x20/+0x24}]
        | ctor ArkObject FUN_00726e70: A→encja@+0x28      | setterzy FUN_00730f90/fb0/fd0; rejestracja FUN_00457930
        v                                              v
[ENCJA ArkObject (fabryki ArkObjectClass::create)]   (GRANICA: producer atrybutów = NIEROZSTRZYGNIĘTY: H1/H2 pliki vs H3 sieć vs H4)
        |
        | (ścieżka żądania modelu: PUMP FUN_006c9700 {0x66=MODEL, A} — ktorego konkretnego callera używa statyk: NIEUSTALONE; 0/38 censurowanych = placement-driven)
        v
[ArkResourceManager → provider-chain → Models.bnt (BNT2) → 296445.nif] (otwarcie fizyczne: STRONGLY_SUPPORTED, errata R2)
        |
        v
[FUN_006cb6f0: cache → pump → ArkModelResourceInstanceRef(12B) → FUN_006cb020: instancja nazwana "<id>__<name>" (0x110B) → rejestracja]
        |
        v
[pending-attach FUN_006cb3c0 {type,A} → attach do węzła [cel+8] (FUN_0077c0b0/f0/120)]
        |
        v
[NiNode/NiAVObject (m_kLocal: translate@+0x5C, rotate@+0x38, scale@+0x68; m_kWorld: +0x90/+0x6C/+0x9C)]
   pod sceną "NetImmerseScene::Root"
```
**Krawędzie NIEUDOWODNIONE (jawnie)**: (a) atrybuty→węzeł NIF statyka (brak łącza
rekord-placementu z attach); (b) producer kontenera atrybutów (plik/sieć); (c) konkretny
caller pumpu używany przez statyki; (d) semantyka pola D f32 (124.941 dla 4508) — nie
zidentyfikowano konsumenta; (e) fizyczne otwarcie .nif w provider-bodies (bez zmian —
STRONGLY_SUPPORTED).

## 8. NOT_CHECKED (jawna lista)

1. Dekod zawartości Portals.bnt (ArkPortalResourceItem — .prt) jako potencjalnego nośnika
   placementów — NIE otwarto (statycznie dozwolone, ale poza budżetem tego runu).
2. Zawartość TerrainEditZones.bnt w era 9.3.5 (TEZ 171 plików to era 2003/PCG; tu 54 KB
   jeden plik — nie dekodowano).
3. Provider/factory virtual bodies BEYOND create→store-read (residuum poprzedniego runu)
   — Z6 domknięte tylko dla łańcucha instancji (ArkModelResourceInstanceRef→item).
4. Fun_00567c50 i producenci kontenerów atrybutów (granica S-A).
5. CWOData: definicja struktury i producer (bind @0x00B78CC8 — tylko sygnatura).
6. Network packet handlers (ArkPacketDecoder/ArkClientPacketExecutor) — statyczne badanie
   kodu sieciowego dozwolone, ale nie wykonane w tym runie (priorytet: placement lokalny).
7. Dekompilacja pełna FUN_0052d6d0 (44 KB — nieudana w Ghidra, timeout; nieistotna dla
   wniosku — funkcja buduje stringi, wzorce = stack offsets).
8. Semantyka 0x70D17=460563 (FUN_0093be20) — brak zasobu lokalnego; nie ustalono celu.

## 9. Otwarte kandydaty na kolejny krok

1. **Dekod Portals.bnt/.prt** (ArkPortalResourceItem): czy .prt niosą placementy/macieże
   komórek z transformami — bezpośredni kandydat H1/H2 dla statyków (portal resource =
   kliencki magazyn przestrzenny, jedyna "cell" przestrzeń w 9.3.5).
2. **Producer kontenera atrybutów**: backward od FUN_00846840/FUN_0085b8x0 do źródła
   (plik Parameters vs pakiet sieciowy) — rozstrzyga H1/H2 vs H3.
3. **CWOData + ArkClientWorldObjectManager**: struktura CWOData (bind sygnatura) i jej
   zapisujący — domknięcie "encja świata + pozycja" po stronie klienta.
4. **Konsument pola D f32** (124.941 w template 4508): skan xrefów FUN_0074655x (getter
   rodziny B) / readerów +0x10 — możliwy nośnik wysokości/promienia placementu.
5. Statyczna analiza ArkPacketDecoder/ArkClientPacketExecutor + ArkStaticPacket: czy
   jakikolwiek pakiet create niesie transform statyka (rozstrzygnięcie H3 na kodzie).

---

## Bramki
- **GA-CLASSIFY: PASS** (25+13 sklasyfikowane z dowodem; FUN_006b4c50 rozstrzygnięta; UNKNOWN=1 z powodem).
- **GB-PATTERNS: PASS** (3/3: disp32; zero odwołań do 4508 jako imm32).
- **GC-BACKWARD: PASS** (2 slice'y VA-locked z granicami; 5 wykluczeń fałszywych trafień z powodami).
- **GD-LOADERS: PASS** (census stringów+klas z wynikiem, w tym negatywy strukturalne: brak Sectorów w 9.3.5).
- **GE-ERA: PASS** (S0 fail-closed; zero transferu PE2; Gb12 tylko jako oracle semantyki).

## SELF_CHECK (własny, niezależny audyt PE-MASTER)
- Pełny census 38/38 call-site'ów re-weryfikowany bajtowo (S9: 0 mismatch) ✓
- Round-trip ID przed skanem: 8/8 ✓; skan .text kompletny (3/0/0 hitów) ✓
- Drugi przypadek ogólności: siblingi 4752 (A=126740)/2249 (A=278453) — obecni w skanach
  negatywnych (istnieją w Models.bnt: 395,268,719/395,268,746 = 1 hit każdy) ✓
- Kontrola negatywna klasyfikacji: STATIC_WORLD=0 z dowodem generyczności (zero
  296445/4508-specyfika w .text) ✓
- Oddzielenie transformacji LOKALNEJ od WORLD: oracle offsetów NiAVObject (local +0x38/+0x5C/+0x68
  vs world +0x6C/+0x90/+0x9C) + wykluczenia #1-#5 ✓
- Każdy VA cytowany = surowe bajty w dumpach (GA1-GA8 disasm/pseudo + S3/S9 raw) ✓
- Granice jawne: S-A (producer atrybutów), S-B (napęd statyka), 8×NOT_CHECKED ✓
- Pułapki wyłapane i udokumentowane: kolizja offsetów pending-attach vs NiAVObject (FUN_006f2af0),
  layout rekordu placementu (+0x08 pozycja) vs template rejestru (+0x08 A) — rozdzielone
  dowodem join A→.nif z poprzedniego runu ✓
