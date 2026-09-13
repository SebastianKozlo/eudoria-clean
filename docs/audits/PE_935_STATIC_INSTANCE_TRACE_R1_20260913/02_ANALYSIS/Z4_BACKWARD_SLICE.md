# Z4 — ŚLAD WSTECZ OD TRANSFORM-SETTERÓW (GC-BACKWARD)

RUN: PE_935_STATIC_INSTANCE_TRACE_R1_20260913 | ERA: EU 9.3.5
Oracle semantyki setterów: Gb12_Source (D:\gamebyroengine\extracted\Gb12_Source) —
Wyłącznie semantyka (NiAVObject::SetTranslate/SetRotate/UpdateWorldData, NiTransform
{m_Rotate 9f, m_Translate 3f, m_fScale}); NIE opis loaderów MindArka.
Ground-truth offsetów NiAVObject w 9.3.5 (VA-locked, własny dump): **FUN_007c04f0 =
NiAVObject::GetViewerStrings** (kolejność stringów 1:1 z Gb12 NiAVObject.cpp: m_bAppCulled,
m_localTranslate, m_localRotate, m_fLocalScale, m_worldTranslate, m_worldRotate,
m_worldScale, m_kWorldBound + mindarkowy prefiks dpvs). Wyzkane offsety:
- m_bAppCulled @+0x20 (byte)
- m_kLocal.m_Translate @+0x5C (3f), m_kLocal.m_Rotate @+0x38 (9f), m_kLocal.m_fScale @+0x68
- m_kWorld.m_Rotate @+0x6C (9f), m_kWorld.m_Translate @+0x90 (3f), m_kWorld.m_fScale @+0x9C
- m_kWorldBound @+0x28; dpvs pola @+0xB4/+0xB8/+0xBC/+0xC4

## SLICE S-A: setterzy transformu rekordu placementu (VA-locked)

```
FUN_00846840(param_1=kontener atrybutów, out=3 floaty)      @0x00846840
  └─ FUN_0085b840/0085b860/0085acb0/0085b1a0/0085b050 (walker-y drzewa atrybutów)
  └─ switch po ID atrybutu: 0x6A4 (1700) / 0x6A5 (1701) / 0x6A8 (1704) / 0x6A9 (1705)
     → semantyka: pozycja/rotacja z REKORDU ATRYBUTÓW (system parametrów)
FUN_00567770(param_1, param_2)                              @0x00567770  [anchor slice]
  ├─ czyta pozycję (3f) + drugą trójkę floatów z atrybutów (FUN_00846840 + FUN_00854720 + FUN_004154f0)
  ├─ buduje rekord POCHODNY (ctor FUN_00730700; wypełnienie przez FUN_004c5580 = CWO-deriver)
  ├─ *** SETTERY TRANSFORMU (cel Z4) ***
  │    FUN_00730f60: zeruje 11 dwordów (+0x00..+0x2C)      @0x00730F60
  │    FUN_00730f90: [obj+0x08]=x,[+0x0C]=y,[+0x10]=z  POZYCJA  @0x00730F90 (`MOV [ECX+8],EAX...`)
  │    FUN_00730fb0: [obj+0x14..0x1C]               ROTACJA  @0x00730FB0
  │    FUN_00730fd0: [obj+0x20],[+0x24]            2 pola (skala/param?) @0x00730FD0
  │    (ECX = obiekt lokalny @ESP+0xB4 — weryfikacja disasmem @0x005678F0-0x0056790C:
  │     `LEA ECX,[ESP+0xB4]; CALL ...` — NIE jest to obiekt rejestru template'ów!)
  └─ rejestracja z NAZWĄ: FUN_004148f0(...,2,str,1,1) + FUN_00457930 (map-insert z basic_string)
FUN_00567770 ← FUN_00567c50 @0x00567C50 (jedyne wywołanie @0x0056836C)
Inni użytkownicy setterów f90/fb0 (11-15 call-site'ów): FUN_00567170 (@0x0056739B/@0x005673BA),
FUN_005b5f90 (@0x005B601A/@0x005B6032), FUN_0050bed0, FUN_00457cd0, FUN_00442190,
FUN_00447630, FUN_004b3a00, FUN_0043a200, FUN_004c47f0, FUN_0046e790, FUN_00488920,
FUN_0067bc90, FUN_0067ccd0.
```

**GRANICA SLICE S-A (jawna)**: rekord atrybutów (param_1) jest czytany z systemu
atrybutów/parametrów (drzewo FUN_0085b840...; ID atrybutów 0x6A4/0x6A5/0x6A8/0x6A9;
konstelacja param-setów 0x4E26=20006-class). PRODUCENT kontenera atrybutów NIE został
VA-locked w tym runie — kandydaci: (a) pliki Parameters\*.vfs (klienckie, H1/H2),
(b) pakiet sieciowy (H3), (c) rekord pochodny innej encji (H4). Brak rozstrzygnięcia =
rodzina hipotez otwarta; brak defaultu.

**Uwaga separacyjna (§7)**: rekord placementu (klasa "derived-record": pozycja@+0x08,
rotacja@+0x14) ma INNY layout niż obiekt template'u rejestru (B@+0x04, A@+0x08=id .nif,
C@+0x0C, D f32@+0x10 — join A→<A>.nif 3618/3618 z poprzedniego runu wyklucza inne
czytanie pola +0x08). Fakt, że OBA używają ctor-a FUN_00730700, jest spójny (ctor zeruje
tylko +0x10, co pasuje do obu layoutów) i udokumentowany jako potencjalna pułapka.

## SLICE S-B: instancja modelu (VA-locked)

```
FUN_006cb6f0(this=ModelManager-side, A, store)              @0x006CB6F0  [twórca instancji]
  ├─ FUN_00971780: lookup A w mapie [store+0x3C] → hit: return [hit+8]+8 (cache)
  ├─ FUN_006cb370(A): check (thiscall)
  ├─ pump FUN_006c9700 {0x66=MODEL, A} @0x006CB7CF → ESI = item zasobu (async load)
  ├─ operator_new(0xC) @0x006CB819 (CALL 0x0095d3c4) → ctor FUN_006fa8b0 @0x006CB836
  │    = ArkModelResourceInstanceRef {vft 0x00A864B8, licznik@+0x04, item@+0x08}
  │      (dtor @0x006FA8D0 ustawia bazowy vft ArkRefObject 0x00A864B0)
  ├─ FUN_006cb020 @0x006CB020: tworzy instancję 0x110 B z NAZWĄ "<id>__<name>"
  │    (stringstream: `<< [rec+4]` + "__" + string@+4; check klasy "ArkAnimation" FUN_007b6c30)
  └─ FUN_006f33a0: rejestracja instancji (this=store)
Callers: FUN_006cd820 @0x006CD820 (→ FUN_006cd4e0(name,1): nazwa→id; caller:
  FUN_006bf2e0 @0x006BF2E0 = attach "LowerBody" do kości "Bip01_StartTarget" — ŚCIEŻKA AVATAR),
  FUN_006cd850 @0x006CD850 (7 arg float: update LOD/placement wizualnego; caller ×2:
  FUN_006cdd80 @0x006CDD80 — rodzina body-part/"LowerBody"/"ArkAnimation").
```

**GRANICA SLICE S-B**: podsystem wizualny 0x006Cxxxx obsługuje przypięcia modeli
(sloty, body-part, animacje). NIE zidentyfikowano w nim napędu typu "wczytaj placement
statycznego budynku z pliku X" — napęd statyków (jeśli przez ten podsystem przechodzi)
leży WYŻEJ niż FUN_006cdd80 i nie został izolowany w tym runie.

## FAŁSZYWIE TRAFIENIA — WYKLUCZONE (z powodami)

1. **FUN_007351e0 @0x00735226 / FUN_00736700 @0x00736746** (skan S5: `89 46 58 89 46 5c
   89 46 60`): ctor **ArkSurgeonObject** (`*param_1_00 = ArkSurgeonObject::vftable`,
   globalny template DAT_00ba58cc) — zeruje POLA KLASY [+0x58..+0x70] (fields 0x16-0x1C),
   NIE transform (offsety niezgodne z oracle NiAVObject: translate byłby +0x5C tylko
   w NiAVObject; tu +0x58/+0x5C/+0x60 to trzy osobne pola dword). Powód wykluczenia:
   zły typ obiektu (RTTI potwierdza klasę).
2. **FUN_006f2af0 @0x006F2AF0** (zapis +0x5C/+0x60/+0x64=0, +0x68=1.0, +0x6C=1.0): wygląda
   jak reset transformu NiAVObject, ALE caller FUN_006cb3c0 @0x006CB3C0 czyta z TEGO
   SAMEGO obiektu type@+0x5C (1/2/3) i A-id@+0x64 — więc to **deskryptor pending-attach**
   (czyszczenie kolejki po attach: type→0, A→0, priorytet→1.0). Kolizja offsetów z
   NiAVObject jest przypadkowa — pułapka udokumentowana (wykluczone po analizie dataflow
   callera, nie po wzorcu bajtów!).
3. **Klaster FUN_00793690-0x00793C80** (6 funkcji, zapisy +0x20..+0x5C): kopiowanie
   macierzy renderu (rzędy stride 0x10: `MOV [p+0x20],[0]; MOV [p+0x30],[1]; ...`) +
   FUN_007a75f0(0x18,2,0) render-state — macierze renderera, NIE placement świata.
4. **Klaster FUN_00856240-0x0085DA30** (FSTP/MOV @+0x40..+0x6C): konwersje
   kwaternion/macierz (NiMatrix3::FromQuaternion-style) — matematyka lokalna, nie encja.
5. **FUN_007c04f0 (GetViewerStrings)**: czyta world transform do debug-printu — nie setter;
   użyty jako ORACLE offsetów, nie jako trafienie.

## Rozdzielenie §7 (zasób NIF ≠ manager ≠ lokalna hierarchia ≠ instancja ≠ rodzic)
- Zasób NIF: Models.bnt (BNT2, name index z poprzedniego runu — join 3618/3618).
- Manager: ArkModelManagerMain/ArkModelManager (RTTI @0x00B8C1B8/@0x00B8C1DC); RM
  singleton DAT_00ba12f4 (FUN_00415670).
- Instancja: ArkModelResourceInstanceRef (12 B) + nazwana instancja 0x110 B
  ("<id>__<name>") — DWA poziomy instancji zasobu.
- Obiekt świata: ArkObject (+A@0x28 z template'u) — ENCYJA; jej model dowiązany
  podsystemem 0x006Cxxxx (attach do węzła [this+8]).
- Rodzic przestrzenny: scena "NetImmerseScene::Root" (nazwa @0x00A972FC, funkcja
  FUN_00933310); kości ("Bip01_StartTarget") — LOKALNE hierarchie modelu, wykluczone
  jako world transform.

## JAWNA GRANICA CAŁOŚCI Z4
Nie znaleziono (w zakresie tego runu) instrukcji-celu "SetWorldTranslate(vec3) na węźle
statycznego budynku z danymi z pliku sieci/pakietu". Znaleziono natomiast: (a) pełną
maszynę tworzenia instancji modelu (S-B), (b) setterzy transformu rekordów placementu
(S-A) zasilane z systemu atrybutów. Czego brakuje do domknięcia: powiązanie
(atrybuty-z-pozycją → węzeł NIF instancji) oraz identyfikacja pliku/pakietu, który
zapełnia kontener atrybutów dla statyków. To są otwarte kandydaty na następny run.
