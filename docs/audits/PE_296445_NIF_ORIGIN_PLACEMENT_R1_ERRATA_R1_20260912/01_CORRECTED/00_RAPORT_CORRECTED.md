# 296445.nif — badanie pochodzenia i placementu jednego budynku (WERSJA POPRAWIONA — ERRATA R1)

**RUN:** PE_296445_NIF_ORIGIN_PLACEMENT_R1_ERRATA_R1_20260912 (errata dokumentacyjna + rekomputacja mechaniczna) | **Era:** EU 9.3.5.6746 (pcg_install) + cross-era 2003/intermediate | **Autor:** PE-MASTER (badanie R1); errata: pe-master-auditor na kontrakcie PE-MASTER

> **STATUS ERRATY:** niniejszy dokument jest POPRAWIONĄ wersją raportu `04_REPORT\00_RAPORT.md` runu **PE_296445_NIF_ORIGIN_PLACEMENT_R1_20260912** (R1 pozostaje NIETYKALNY — completed run = immutable). Poprawki wynikają z adjudykacji PE-MASTER (werdykt: MASTER_PARTIAL_PASS z rozszerzoną listą korekt) po audycie zewnętrznym cross-engine (`C:\Users\User\Documents\ChatGPT\PE\audit-296445-placement-r1\AUDYT.md`; 7/7 ustaleń ACCEPTED, każde fizycznie zweryfikowane niezależnie przez PE-MASTER). Każde zmienione miejsce oznaczone jest markerem **[E-…]**; pełna lista korekt z cytatami zastępowanych twierdzeń: `03_REPORT\ERRATA.md`. ZERO nowej forensyki; ZERO nowych twierdzeń poza adjudykowaną listą korekt.

---

## ROZSTRZYGNIĘCIE (skrót)

| # | Ustalenie | Status |
|---|---|---|
| 1 | Pełna mapa pliku: 155/155 bloków, rozliczenie bajtowe dokładne (49+2795+106024+8 = 108,876 B, 0 bajtów nierozliczonych); zero bajtów nierozliczonych = pełne pokrycie ZAKRESÓW bajtowych, nie dowód pełnej semantyki **[E-D3]** | CONFIRMED |
| 2 | Tożsamość próbki: Models.bnt C950A8C2…; payload 296445.nif 656795d8… (108,876 B, offset 57,936,887, RAW); wpis CRC == crc32(payload) | CONFIRMED |
| 3 | Model = budynek slumsów **B_Eu_Slum_Building_b047_01** (pełne nazwy odzyskane); 30 meshy, 2415 wierzchołków, 1030 trójkątów | CONFIRMED |
| 4 | Wewnątrz NIF nie ma placementu świata: korzeń (Scene Root) ma transformację identycznościową; tłumaczenia bloków są lokalne (względem rodziców, A/B); ogon importera == ekstrema SUROWYCH tablic wierzchołków z RÓŻNYCH układów lokalnych (identyczność bitowa faktem, ale NIE jest to bbox sceny po złożeniu); poprawny bbox sceny po złożeniu = ±2500/±2500/[~0, 15620] ≈ 5000×5000×15620 jednostek modelu **[E-B]** | CONFIRMED (bounded) |
| 5 | Łańcuch zewnętrzny DEFINICJI: **template 4508 → A_model=296445, B=296446(.bvi)** — obecny w erze EU 9.3.5 (templates.vfs, rekord w ofs 96496) i w korpusie VFS klienta pośredniego/późniejszego (ArkVFS02; rekord w ofs 0x17914; era ≠ 2003-CD, dokładna era nieustalona — poprzednio błędnie etykietowany „2003" **[E-A2]**); template 4508.obj (Scripts.ark CD-2003, zdekodowany) binduje dokładnie komplet siatek tego modelu | CONFIRMED (byte-exact, dwa źródła + korespondencja zestawów) |
| 6 | Towarzysz kolizyjny: 296446.bvi istnieje w Volumes.bnt (offset 993,420, 760 B, SHA 7fee519b…) i jest byte-identyczny w erze BNT_Models; zawiera LOKALNE wolumeny kolizji (pary ±25/±10/±20 + wysokości), NIE współrzędne świata | CONFIRMED |
| 7 | Rodzina b047 w korpusie 9.3.5: {126740 (T4752), 278453 (T2249), 296445 (T4508)}; model byte-identyczny w Models.ark (CD-2003), BNT_Models (1322adf2) i pcg_install 9.3.5 (zdanie o wariantach slum WYCOFANE — niepodparte artefaktem; cytat zastępowanego twierdzenia w ERRATA.md **[E-F8]**) | CONFIRMED |
| 8 | Hierarchia kategorii: 201→477→**4751**→4508 (tree_paths VFS klienta pośredniego/późniejszego — ArkVFS02 **[E-A2]**); EU hierarchy.vfs zawiera krawędzie 4751→4508 (ofs 46264) i 4751 pod 477; węzeł 4751 = 200 template'ów zawartości miejskiej/slumsów | CONFIRMED (krawędzie byte-verified; pełna ścieżka EU: spójna z korpusem VFS klienta pośredniego) |
| 9 | **Placement instancji świata: NIE ZNALEZIONO W ZBADANYM ZAKRESIE** — statyczne dane klienta przeszukane z podaniem granic (u32LE pełny korpus [run] + u32BE pełny Data [audytor PE-MASTER: 0 trafień BE dla 296445/296446] **[E-F10]** + ASCII + zdekompresowane kafle terenu [LE: run; BE: audytor] + zdekodowany korpus skryptów 2003 + VFS obu er; NIE przeszukiwano WNĘTRZA szyfrowanych payloadów Strings/*.bnt — granice w §6/§8). Kanon RE **PE2/2003** (PE2_unpacked_out.exe, SHA256 56178993692A7409C896398089E482EDDF96177666BACB91A8CC1A638D9A0650; byte-evidenced w kanonie TEMPLATE_READER dla TEGO binarium): sieciowy create-object handler FUN_005977b0 — rekordy 0x1C + sub-rekord transformacji f32 XYZ @+0x2c/+0x30/+0x34, SetPosition przez vtable[0x50] **[E-A1]**. Mechanizm pozycji w EU 9.3.5 (Entropia.exe, SHA E7785430…): **UNVERIFIED — wyłącznie HIPOTEZA TRANSFERU między erami; wymaga trace w Entropia.exe 9.3.5** **[E-A1]** | NOT_FOUND_IN_SEARCHED_SCOPE (negatyw placementu BOUNDED); mechanizm PE2/2003 CONFIRMED w swoim binarium; mechanizm 9.3.5 UNVERIFIED |
| 10 | Konkretna pozycja historyczna budynku: nieosiągalna z istniejącego korpusu (serwery MindArk niedostępne; brak zapisanej sesji — FIRST_PEINST 0/6; brak cache na tej maszynie) | UNKNOWN / NOT_FOUND_IN_SEARCHED_SCOPE |

**Werdykt jednozdaniowy:** model 296445.nif to slum-building b047_01 z pełnym, potwierdzonym łańcuchem definicji (template 4508 w VFS klienta EU 9.3.5 i VFS klienta pośredniego/późniejszego **[E-A2]** → model 296445 → kolizja 296446.bvi → kategoria 4751), ale **nie znaleziono potwierdzonego rekordu historycznej instancji 296445 w opisanym zakresie (NOT_FOUND_IN_SEARCHED_SCOPE)** **[E-D1]** — sieciowa ścieżka dostarczania pozycji jest byte-evidenced w RE klienta PE2/2003, a jej zapisy nie istnieją w korpusie; mechanizm pozycji w EU 9.3.5 pozostaje UNVERIFIED (hipoteza transferu **[E-A1]**); ścieżka sieciowa dowodzi istnienia takiej ścieżki, NIE wyłączności — sceny lokalne/pośrednie ID/sektorowe dane w 9.3.5 pozostają otwarte **[E-D2]**.

---

## 1. Tożsamość próbki

| Pole | Wartość |
|---|---|
| Archiwum źródłowe | D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt |
| SHA256 archiwum | C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0 (zweryfikowany ponownie) |
| Wpis indeksu BNT2 | nazwa „296445.nif”, offset 57,936,887, rozmiar 108,876 B, CRC wpisu = 0xCFAC1D3B = crc32(payload) (zgodne) |
| Payload | RAW (bez kompresji), SHA256 656795d8b3dddf8f9192ee41c4710d592894860f6959b53b2c08036977e7b862 |
| Nagłówek NIF | „NetImmerse File Format, Version 4.1.0.12”, wersja 0x0401000C, num_blocks 155 |
| Klient źródłowy | EU 9.3.5.6746 |
| Ekstrakcja | skrypt 00_CONTROL/extract_296445.py (metoda: parse indeksu BNT2, wyciąg surowych bajtów) |

Cross-era (osobne hashe zapisane):

| Korpus | Era | Wpis | Rozmiar | SHA256 payloadu | Tożsamość |
|---|---|---|---|---|---|
| 01_Original_Files/ARK/Models.ark (f660d055…) | CD-2003 | 296445.nif (stored) | 108,876 | 656795d8b3dddf8f…7e7b862 | **BYTE-IDENTYCZNY** |
| 01_Original_Files/BNT_Models/Models.bnt (1322adf2…, 5426 wpisów) | pośrednia | 296445.nif (ofs 78,809,604) | 108,876 | 656795d8b3dddf8f…7e7b862 | **BYTE-IDENTYCZNY** |
| pcg_install/Data/Models/Models.bnt (c950a8c2…, 5596 wpisów) | EU 9.3.5 | 296445.nif (ofs 57,936,887) | 108,876 | 656795d8b3dddf8f…7e7b862 | referencja |

Wniosek: budynek istniał bez zmian od korpusu 2003 do 9.3.5 — stabilny, długowieczny zasób. BVI 296446: byte-identyczny między BNT_Models a 9.3.5 (7fee519b…).

---

## 2. Pełna mapa pliku (155 bloków, rozliczenie bajtowe)

**Rozliczenie bajtowe (dokładne):** nagłówek 41 B (string) + 8 B (wersja+liczba bloków) = 49; pola typów 155 bloków = 2,795 B; ciała bloków = 106,024 B; stopka [numTopObjects=1][rootID=0] = 8 B. Suma: 49+2795+106024+8 = **108,876 = rozmiar pliku**. Bajtów nierozliczonych: **0** (pełne pokrycie zakresów bajtowych, nie dowód pełnej semantyki **[E-D3]**). Brak pola user-version (Gb12: czytane tylko dla wersji ≥ 10.0.1.8).

**Census typów (155):** NiNode 19, NiTriShape 30, NiTriShapeData 30, NiTexturingProperty 22, NiMaterialProperty 17, NiAlphaProperty 10, NiZBufferProperty 10, NiArkBillboardNode 7, NiStringExtraData 4, NiArkAnimationExtraData 1, NiArkTextureExtraData 1, NiArkImporterExtraData 1, NiTextureEffect 1, NiUVController 1, NiUVData 1. Statystyki przeglądarki potwierdzone niezależnie: 2415 wierzchołków, 1030 trójkątów (Σ po NiTriShapeData).

**Pełna tabela 155 bloków** (indeks, typ, zakres bajtów, nazwa, referencje, pola kluczowe): **02_ANALYSIS/BLOCK_TABLE_FULL.csv** (run R1, bez zmian). Pełny dump JSON: **01_RAW/BLOCKMAP_V2.json** (run R1, bez zmian — wejście rekomputacji erraty). Poniżej bloki istotne merytorycznie.

### 2.1 Łańcuchy extra-data (weryfikacja niestandardowych pól)

NiExtraData w 4.1.0.12 = [next ref 4B][uiSize u32 4B] + pola podklasy (Gb12 NiExtraData.cpp L109: ReadLinkID + uiSize; blob tylko dla dokładnego NiExtraData). To rozstrzyga pozycję „Num Bytes” z nif.xml: pole istnieje i jest czytane dla wszystkich podklas, ale jego wartość NIE jest długością danych podklasy (dla NiStringExtraData: uiSize=111, strlen=107 — uiSize = 4+107, rozmiar chunku; dla bloków Ark: uiSize=0).

| Blok | Typ | next | uiSize | Właściciel łańcucha |
|---|---|---|---|---|
| 1 | NiArkAnimationExtraData | 2 | 0 | Scene Root (0) → 1 → 2 → 3 |
| 2 | NiArkTextureExtraData | 3 | 0 | (j.w.) |
| 3 | NiArkImporterExtraData | -1 | 0 | (j.w., koniec łańcucha) |
| 28 | NiStringExtraData | -1 | 111 | NiNode 27 (Bip01_item) |
| 30 | NiStringExtraData | -1 | 13 | NiNode 29 (GeoTexanim01) |
| 64 | NiStringExtraData | -1 | 13 | NiNode 63 (B_Eu_b047_glowsak) |
| 71 | NiStringExtraData | -1 | 9 | NiNode 70 (B_Eu_b047_Object06) |

### 2.2 Pełne stringi (odzyskane z bajtów, bez obcięć UI)

**NiStringExtraData (4 szt.):**

| Blok | uiSize | długość | Pełna treść |
|---|---|---|---|
| 28 | 111 | 107 | „PredefinedAnimationData:\r\n1\r\n\r\nNodeDataStart\r\nGeoTexanim01\r\n0\r\n0.0\r\n0.0\r\nactiveIdle\r\nControllers\r\nAll\r\nLOOP” |
| 30 | 13 | 9 | „zMode10\r\n” |
| 64 | 13 | 9 | „zMode10\r\n” |
| 71 | 9 | 5 | „decal” |

**NiArkAnimationExtraData (blok 1)** — dekodowanie deterministyczne: next=2, ints (3,27,0), bytes (0,1), u32 strlen=83, tekst (83 B): „\r\n1\r\n\r\nNodeDataStart\r\nGeoTexanim01\r\n0\r\n0.0\r\n0.0\r\nactiveIdle\r\nControllers\r\nAll\r\nLOOP”, ogon 35 B = [u32 0][byte 0][u32 2][i32 -1][5×f32 -1.0][byte 0][byte 0]. Wariant = tekstowy deskryptor animacji (animacja tekstury GeoTexanim01). Pola numeryczne: UNKNOWN (zapisane bajtowo).

**NiArkImporterExtraData (blok 3)**: next=-1, uiSize=0, int=8, importer=„4.1.0.12”, ogon 41 B = [u32 0][u32 0][u32 -1][u8 0xFF] + **7×f32 = [-3447.685, -2500.0, -3543.212, 12593.814, 3743.970, 15620.0, 0.0]**.

### 2.3 Ogon importera == ekstrema SUROWYCH tablic wierzchołków z różnych układów lokalnych **[E-B4]**

| Źródło | min | max |
|---|---|---|
| 7 floatów importera | (-3447.685, -2500.000, -3543.212) | (12593.814, 3743.970, 15620.000) |
| Surowe wierzchołki (wszystkie meshe, bez transformacji) | (-3447.685, -2500.000, -3543.212) | (12593.814, 3743.970, 15620.000) |

Zgodność co do wartości f32 pozostaje FAKTEM. **Poprawiona interpretacja [E-B4]:** ekstrema surowych tablic wierzchołków pochodzą z RÓŻNYCH układów lokalnych (każdy mesh w swoim własnym framie) — ich wspólny min/max **NIE jest bboxem sceny po złożeniu**. Poprawny bbox sceny po złożeniu (konwencja world = parent∘local z własną transformacją mesha — patrz §3B): **min (-2500.0, -2500.0, ~-1.27e-08) do max (2500.0, 2500.0, 15620.0) ≈ 5000×5000×15620 jednostek modelu** (wartość ujemna Z to epsilon numeryczny kompozycji, nie przesunięcie geograficzne). Ogon importera to metadana surowych ekstremów pliku, NIE placement świata. Semantyka siódmego floata (0.0) = **UNKNOWN** (zgodność pierwszych 6 wartości nie dowodzi roli siódmej — zdanie domykające tę semantykę WYCOFANE **[E-B4]**; cytat zastępowanego zdania w ERRATA.md).

### 2.4 NiArkTextureExtraData (blok 2) — 26 wpisów tekstur (pełne nazwy + ID)

Struktura wpisu: [nazwa CString][int3][int4][ref NiTexturingProperty][9 B]. **Pole 9-bajtowe = [u8 0 @0][u32 -1 (0xFFFFFFFF) @1..4][u32 ID @5..8]** — bajt @8 to MSB ID (zawsze 0 dla ID < 2^24 — stąd złudzenie „dodatkowego bajtu”); **brak dziesiątego bajtu** **[E-E]**. int3 = klasa slotu (0=BASE, 3=GLOSS, 4=GLOW, 9=ENVIRONMENT — korelacja z sufiksami nazw), int4 = -1, ID = identyfikator w Textures.bnt.

| Nazwa tekstury | int3 | ref | ID (u32 @5..8) |
|---|---|---|---|
| B\_Eu\_Slum\_Building\_b047\_01\_0\_BASE | 0 | 4 | 126743 |
| B\_Eu\_Slum\_Building\_b047\_01\_1\_BASE | 0 | 5 | 126745 |
| B\_Eu\_Slum\_Building\_b047\_01\_1\_GLOW | 4 | 5 | 126747 |
| B\_Eu\_Slum\_Building\_b047\_01\_2\_BASE | 0 | 6 | 126749 |
| B\_Eu\_Slum\_Building\_b047\_01\_3\_BASE | 0 | 7 | 126751 |
| B\_Eu\_Slum\_Building\_b047\_01\_4\_BASE | 0 | 8 | 126753 |
| B\_Eu\_Slum\_Building\_b047\_01\_5\_BASE | 0 | 9 | 126755 |
| B\_Eu\_Slum\_Building\_b047\_01\_6\_BASE | 0 | 10 | 126745 |
| B\_Eu\_Slum\_Building\_b047\_01\_7\_BASE | 0 | 11 | 126758 |
| B\_Eu\_b047\_gloss\_0\_BASE | 0 | 12 | 126760 |
| B\_Eu\_b047\_gloss\_0\_GLOSS | 3 | 12 | 126762 |
| Nameless0\_ENVIRONMENT | 9 | 13 | 42302 |
| B\_Eu\_b047\_glowsak\_0\_BASE | 0 | 14 | 126765 |
| B\_Eu\_b047\_Object06\_0\_BASE | 0 | 15 | 126767 |
| B\_Eu\_b047\_DoorComputer\_0\_BASE | 0 | 16 | 126769 |
| B\_Eu\_b047\_DoorComputer\_0\_GLOW | 4 | 16 | 126771 |
| B\_Eu\_b047\_Galler\_0\_BASE | 0 | 17 | 126773 |
| B\_Eu\_b047\_Object07\_0\_BASE | 0 | 18 | 126775 |
| GeoTexanim01\_0\_BASE | 0 | 19 | 126777 |
| B\_Eu\_b047\_lens\_1\_01\_0\_BASE | 0 | 20 | 126779 |
| B\_Eu\_b047\_lens\_1\_02\_0\_BASE | 0 | 21 | 126781 |
| B\_Eu\_b047\_lens\_1\_03\_0\_BASE | 0 | 22 | 126779 |
| B\_Eu\_b047\_lens\_1\_04\_0\_BASE | 0 | 23 | 126779 |
| B\_Eu\_b047\_lens\_1\_05\_0\_BASE | 0 | 24 | 126779 |
| B\_Eu\_b047\_lens\_1\_06\_0\_BASE | 0 | 25 | 126779 |
| B\_Eu\_b047\_lens\_1\_07\_0\_BASE | 0 | 26 | 126779 |

Uwaga: wpis „GeoTexanim01_0_BASE” (ID 126777) ma **potwierdzoną UV-animację** (NiUVController, blok 33: 2 klucze kwadratowe, wartość UV 0.0→5.0 w czasie 0→3.3333 s (LOOP), freq=1.0, cel = meshe 32 (GeoTexanim01:0)); **interpretacja flipbook/atlas = HIPOTEZA (wymaga analizy obrazu i kluczy)** **[E-E]**. Sześć wpisów „lens_1_03..07” współdzieli ID 126779 (współdzielenie tekstury, obserwowane).

### 2.5 NiTextureEffect (blok 13) — pełny odczyt (layout z Gb12)

NiDynamicEffect dziedziczy po NiAVObject (Gb12 NiImplementRTTI(NiDynamicEffect,NiAVObject)) — blok zawiera PEŁNE pola NiAVObject + [ModelProjMat 9×f32][ModelProjTrans 3×f32][filter u32=2][clamp u32=0][textureType u32=2 (ENVIRONMENT_MAP)][coordGen u32=2 (SPHERE_MAP)][link -1][planeEnable 0][plane=(1,0,0),0][sL=0][sK=-75][abManual[2]=0,0]. Wartości domyślne zgodne z konstruktorem Gb12 (m_sK=-75, m_kModelPlane(UNIT_X,0)). Ogony „manual” czytane dla wersji pliku < 4.1.0.16 — nasz plik 4.1.0.12 ✓. **Relacje właścicielskie (obie, rozróżnione [E-F4]): rodzic grafu = NiNode 62 „B_Eu_b047_reflex” (blok 13 jest dzieckiem 62 w grafie children); effects-owner = NiNode 59 „B_Eu_b047_gloss” (blok 59 ma effect 13 w tablicy effects)** (efekt env-map dla błyszczących części; tekstura „Nameless0_ENVIRONMENT”, ID 42302).

### 2.6 NiArkBillboardNode (7 szt.)

Wszystkie 7 sparsowane jako czysty NiNode — **ogon = 0 bajtów** (dla tego pliku pytanie „dodatkowe pola za NiNode” rozstrzygnięte negatywnie; granica ustalona invariantem kolejnego bloku). Rodzice: Scene Root. Są to lens-flare'y „B_Eu_b047_lens 1<TAB>0X” (nazwa zawiera znak TAB — dziwactwo eksportera) z materiałami „Flare”/„Flare2”.

### 2.7 Katalog pól nieznanych (UNKNOWN, zapisane bajtowo)

| Blok | Pole/obszar | Wartości | Status semantyki |
|---|---|---|---|
| 1 | ints (3,27,0), bytes (0,1), ogon 35 B | patrz 2.2 | UNKNOWN |
| 2 | int3 (0/3/4/9) | korelacja z sufiksem nazw | INFERENCE (typ slotu) |
| 2 | 9 B: [u8 0 @0][u32 -1 @1..4][u32 ID @5..8; bajt @8 = MSB ID (0 dla ID < 2^24)] **[E-E]** | 00FFFFFFFF + ID LE | UNKNOWN (poza ID) |
| 3 | [u32 0][u32 0][u32 -1][u8 0xFF] przed bboxem | — | UNKNOWN |
| 13 | av_flags_raw=0x0194/0x0084 itd. | flagi NiAVObject (konwersja Gb12 dla <4.1.0.12) | zapisane surowe |
| różne | prop_flags_u16 (współdzielone flagi NiProperty < 10.0.1.2) | semantyka bitów per-property | UNKNOWN (surowe) |

---

## 3. Transformacje i geometria (rozdzielenie A/B/C)

**Drzewo sceny** (z relacji children; pełny wydruk: 01_CORRECTED/TREE_ANALYSIS_CORRECTED.txt [errata]; tabela: 01_CORRECTED/TRANSFORM_TABLE_CORRECTED.csv [errata]; wersje R1: 02_ANALYSIS/TREE_ANALYSIS.txt i TRANSFORM_TABLE.csv — world_T/bbox_world SUPERSUMOWANE, patrz ERRATA). Korzeń = blok 0 „Scene Root”, stopka pliku potwierdza 1 obiekt top-level (blok 0). **50 slotów dzieci korzenia, w tym 27× -1 (23 realne dzieci)** **[E-F1 — korekta liczby pustych slotów; census erraty niezależny z BLOCKMAP_V2.json: 23 realne + 27 pustych]**. Census referencji: **0 bloków sierot**, **0 referencji poza zakresem** — wszystkie 154 bloki osiągalne z korzenia przez children/properties/extra/controller/data/effect/target.

**A. Tłumaczenia lokalne części (względem rodziców):** rdzeń budynku = 8 meshy „B_Eu_Slum_Building_b047_01:0..7” o wspólnym bboxie lokalnym X,Y ∈ ±2500, Z ∈ [0, 15620] (grunt przy Z≈30; mesh _4/_5/_7 to płaskie footprinty w Z=30). Części pomocnicze (tłumaczenia LOKALNE względem rodzica; po złożeniu z własną transformacją — patrz B): gloss (0,0,0), glowsak mesh T=(401,-1611,-368), DoorComputer node (-573.9,-1585.9,520.0), Object07 node (-1894.9,-6.8,65.0) + mesh (-2039.1,0,-65), GeoTexanim01 node (1885.0,-6.8,47.5) + mesh (-513.2,36.7,-1053.4), Object06 mesh (-10591.8,-839.7,1536.8 lokalnie; PO ZŁOŻENIU z własną transformacją i rodzicem bbox = (-2002,-2011,332)..(2002,2002,1396) — wewnątrz obrysu budynku, w owym „daleko od rdzenia” R1 mylał układ lokalny z układem modelu **[E-B]**), 7×lens-flare billboard (±1277,±1274, Z 4394–11146 po złożeniu), 7×dPVS_occ01..07 (okludery DPVS, Z do 7720+4420), Bip01_item (nazwa artefaktowa Character-Studio).

**B. Współrzędne względem korzenia NIF (POPRAWIONE — [E-B], errata B1–B3):** konwencja **world[i] = parent_world ∘ local_i (z WŁASNĄ transformacją mesha), parent korzenia = identity** (poprawka buga R1: analyze_tree.py zapisywał world[i] = transformacja RODZICA, przez co geometria pomijała własną transformację mesha — 14 z 30 meshy miało błędne world_T i bboxy). **Poprawny bbox globalny geometrii = min (-2500.0, -2500.0, ~-1.27e-08) do max (2500.0, 2500.0, 15620.0) ≈ 5000×5000×15620 jednostek modelu** (ujemne Z min = epsilon numeryczny kompozycji, nie przesunięcie). Zmienione world_T: dokładnie 14 meshy (32, 66, 72, 75, 82, 90, 94, 115, 121, 127, 133, 139, 145, 151); pozostałe 16 identycznych (kontrola negatywna bramki G1 erraty). Wszystkie osie w JEDNOSTKACH MODELU (nie metrach gry).

**C. Położenie instancji w świecie gry: BRAK W PLIKU.** Żaden blok nie niesie transformacji instancji świata; korzeń jest tożsamościowy; „world” w grafie NIF = przestrzeń modelu (zgodnie z ostrzeżeniem zadania). Macierz world NIF ≠ placement świata — potwierdzone empirycznie (brak jakiegokolwiek kandydata na współrzędne globalne wewnątrz pliku). Przeliczenie jednostek modelu→metry gry wymaga ODRĘBNEGO źródła (np. RE transformacji pakietu) — nie wyestablishowane w tym runie; PARAM template'u (patrz §5) nie jest parą współrzędnych.

---

## 4. Silnik jako przewodnik (Gb12_Source = oracle formatu; plik/funkcja/linie)

Wszystkie layouti bloków zweryfikowane względem implementacji silnika, który czyta pliki 4.1.0.12 (NDR/NDL Gamebryo, sources D:\gamebyroengine\extracted\Gb12_Source):

| Element | Źródło Gb12 (plik: funkcja: linie) | Ustalenie |
|---|---|---|
| Nagłówek strumienia | NiStream.cpp: LoadHeader: ~L303 | linia „…File Format…”; wersja u32; user-version TYLKO dla ≥ 10.0.1.8 (brak w 4.1.0.12); numObjects u32 |
| Bloki (wersja < 5.0.0.1) | NiStream.cpp: LoadObject: L451, LoadStream: L506 | RTTI inline per blok (długość u32 + nazwa); LoadBinary per obiekt |
| Stopka | NiStream.cpp: LoadTopLevelObjects: L362 **[E-F3 — numer linii skorygowany; poprzednia wartość w ERRATA.md]** | [numTopObjects u32][linkIDy] — w naszym pliku [1][0] |
| NiObjectNET | NiObjectNET.cpp: LoadBinary: L553 | name(CString), extra ref, controller ref |
| NiAVObject | NiAVObject.cpp: LoadBinary: L546+ | flags u16 (+kod konwersji dla <4.1.0.12), T V3, R M33, S f32, Velocity V3, properties (u32+refy), bABV NiBool 1B |
| NiNode | NiNode.cpp: LoadBinary: L861 | children (u32+refy), effects (u32+refy) |
| NiProperty | NiProperty.cpp: LoadBinary: L48 | WSPÓŁDZIELONY u16 flags (< 10.0.1.2) — źródło pól „flags” propercji |
| NiTexturingProperty | NiTexturingProperty.cpp: LoadBinary: L238 + Map::LoadBinary: L838 | apply enum u32, listSize u32, per-slot NiBool + [ref, clamp u32, filter u32, uvset u32, sL i16, sK i16, abManual 2B] |
| NiMaterialProperty | NiMaterialProperty.cpp: LoadBinary: L94 | 4×Color3, shine, alpha |
| NiAlphaProperty / NiZBuffer | NiAlphaProperty.cpp: L60 / NiZBufferProperty.cpp: L52 | threshold u8 / eTest enum u32 (od 4.1.0.5) |
| NiExtraData | NiExtraData.cpp: LoadBinary: L109 | [next ref][uiSize u32] dla < 5.0.0.11; blob TYLKO dla dokładnego NiExtraData |
| NiStringExtraData | NiStringExtraData.cpp: LoadBinary: L81 | LoadCString (i32 długość + znaki, NiStream.cpp: L1123) |
| NiTextureEffect | NiTextureEffect.cpp: LoadBinary: L176–L203 | pełny układ (+ NiAVObject z NiDynamicEffect); sK=-75; abManual[2] dla < 4.1.0.16 |
| NiGeometry/TriShape | NiGeometry.cpp: LoadBinary: L351 | data ref, skin ref (shader gate ≥ 5.0.0.21 — brak) |
| NiGeometryData | NiGeometryData.cpp: LoadBinary: L519+ | numVerts u16, hasVerts NiBool, [verts], hasNormals, [normals], bound (V3+f32), hasColors, [colors RGBA], **numTextureSets i16** (dla < 5.0.0.10 — to jest „Data Flag” z nif.xml), [UV] |
| NiTriShapeData | NiTriShapeData.cpp: LoadBinary: L220 | triListLength u32, trójkąty u16×3×n, sharedNormals u16 + grupy |
| NiTimeController/NiUVController/NiUVData | NiTimeController.cpp: L466 / NiUVController.cpp: L283 / NiUVData.cpp: L264 | kontrolery dziedziczą po NiObject (BRAK pól NET!); 4 grupy kluczy (numKeys u32, typ enum u32, klucze wg typu) |

Granica: NiArk* nie istnieją w Gb12 (bloki MindArk) — ich pola po [next][uiSize] odczytano z bajtów (metoda: invariant granicy bloku + korespondencja treści), a nie z definicji silnika. Wszystkie bramki wersji respektowane (4.1.0.12 < 4.1.0.16, < 5.0.0.x, < 10.0.1.x).

---

## 5. Odwrotne wyszukiwanie odniesień (zakres + wyniki)

**Zakres przeszukany (denominatory jawne):**

| Przestrzeń | Zawartość | Metoda | Wynik dla 296445/rodziny |
|---|---|---|---|
| pcg_install/Data — WSZYSTKIE pliki (1818, 2,384,417,861 B) | Models/Textures/Volumes/Portals/TEZ/ui/ES/MusDef/Strings/VegetationClimates/Sounds/Video/Parameters | skan surowy ASCII + u32LE (korekta wzorca — patrz §7); reprodukcja niezależna w erracie (rawscan.py, bramka G2: 8/8 serii identycznych co do offsetów) **[E-G2]** | ASCII „296445” tylko w indeksie Models.bnt; **u32 296445: wyłącznie Parameters/templates.vfs ofs 96,516** (pole A_model); siblingi analogicznie |
| terrain.bnt po dekompresji | 58,575 markerów/kafli zdekompresowanych (281 MB; indeks BNT2: 58,451 wpisów — 2 liczby NIE są zamienne) **[E-F9 — usunięty mojibake '?']** | zlib + skan | 0 trafień 296445/126740/278453; 3 koincydencje (2×296446, 1×278453) sklasyfikowane jako szum pól wysokości (kontekst = strumień bajtów wysokości 0xFE bez struktury rekordu) |
| Parameters/*.vfs (27 plików, 2.2 MB **[E-F6]**) | ArkVFS02, brak kompresji (test zlib: 0 strumieni) | skan u32LE/u32BE + parse rekordów | rekord template'u 4508: A=296445, B=296446 (ofs 96,496); brak innych odniesień; PARAM=124.941 (semantyka UNKNOWN, kandydat skala/promień) |
| Korpus skryptów 2003 po dekodowaniu (1,936 plików .obj.dec, 5.2 MB) | ArkScript VM | skan ASCII/u32LE (reprodukcja niezależna w erracie **[E-C]**) | **u32 296445/296446 występują WYŁĄCZNIE w 4508.obj.dec (@664/@580, immediates bytecode VM); 126740 w 4752.obj.dec (@520); 278453 w 2249.obj.dec (@664); 0 trafień ASCII; 0 w pozostałych 1,933 skryptach. To WZMOCNIENIE powiązania definicja↔model, NIE placement.** **[E-C — retraction fałszywego negatywu skryptowego R1 (cytat zastępowanego twierdzenia w ERRATA.md); mianownik 1,933 = 1,936−3 pliki z trafieniami, zweryfikowany niezależnym skanem erraty]** |
| Scripts.ark (CD-2003, 5.6 MB surowe) | ark | skan surowy | 0 odniesień |
| Kolejność wzorca | 296445 = 0x000485FD = FD 85 04 00 | asercja konwersji odwrotnej | — (patrz retrakcja §7) |
| Cache klienta | Documents/AppData/Entropia Universe, ClientCache | test istnienia | **nie istnieją** (klient nie był uruchamiany na tym hoście); ClientFiles.txt = manifest patchera; Download.data = 12-bajtowy stan patchera |

**Trafienia zbadane i ODRZUCONE (z uzasadnieniem):**

| Kandydat | Uzasadnienie odrzucenia |
|---|---|
| Transformacje/bbox w NIF (w tym 7 floatów importera, duże tłumaczenia części) | importer-tail = ekstrema surowych tablic wierzchołków (zgodność co do f32 — ale z różnych układów lokalnych; NIE bbox sceny po złożeniu **[E-B4]**); korzeń = identity; brak pola o semantyce instancji |
| 296446.bvi | lokalne wolumeny kolizji (pary ±25/±10/±20, wysokości 0.3/10.3); brak współrzędnych świata (zgodnie z kanonem BVI) |
| Portals.bnt (276×.prt) | definicje portali (**zakres nazw 382,811–592,741; większość w 505k–510k [E-F5]**; payload binarny — w próbkach wartości skali świata (formatu NIE zdekodowano w tym runie); pełny census indeksu: brak .prt o nazwie 296445 i brak ASCII/u32 odniesień do modelu) **[E-F9 — usunięta zduplikowana fraza]** |
| TerrainEditZones.bnt (171×.tez) | binarne strefy edycji terenu; brak odniesień |
| EffectSequences.bnt / ui.bnt / VegetationClimates (TSV) / MusDef (tekst) | brak odniesień; klasy zawartości niespowiązane |
| EnvironmentZones.vfs (126 rekordów stref: 84 kanoniczne + 42 ogonowe, per PE_PLACEMENT_ENCODING_CENSUS_R1; rekord 128 B **[E-F2]**; centra ±30k, promienie wg kanonu r=rec32+26.0) | strefy środowiskowe; census: pary współrzędnych tylko dla kanonicznych osiedli, 0 linków template↔strefa (zweryfikowane — pozostaje) |
| Trafienia u32 w DDS/WAV/BIK | dane skompresowanych nośników; brak struktury rekordu; wartość 0x00048846/0x00048845 (pierwszy skan) = w ogóle zły wzorzec — patrz §7 |
| sids.vfs (3,887 kluczy S_* per R1; dopisek metody: 3,885 unikalnych wg regexu audytora; 170 kluczy S_LOCATION; brak klucza SLUM — istota bez zmian **[E-F7]**) | rejestr nazwanych lokacji (S_BUILDING_*, S_LOCATION_*); klucze = sam tekst, bez pozycji |

**Potwierdzone odniesienia (łańcuch definicji, oba kierunki):**

```
Ścieżka sieciowa PE2/2003 (byte-evidenced w kanonie TEMPLATE_READER dla binarium
PE2_unpacked_out.exe, SHA256 56178993692A7409C896398089E482EDDF96177666BACB91A8CC1A638D9A0650:
network create-object handler FUN_005977b0 — rekordy 0x1C + sub-rekord transformacji
f32 XYZ @+0x2c/+0x30/+0x34, SetPosition vtable[0x50]; zapisy sesji NIEOBECNE w korpusie).
W EU 9.3.5 (Entropia.exe, SHA E7785430…): mechanizm pozycji UNVERIFIED — HIPOTEZA
TRANSFERU między erami; ścieżka sieciowa dowodzi istnienia takiej ścieżki, NIE wyłączności.  [E-A1][E-D2]
    ↓ (definicja — fakty poniżej, byte-exact)
Template 4508  [EU: templates.vfs ofs 96,496: id=4508, hash=0xAFF5797C, A=296445, B=296446, C=0, PARAM=124.941]
    [VFS klienta pośredniego/późniejszego (ArkVFS02; era ≠ 2003-CD, dokładna era nieustalona [E-A2]):
     templates.vfs ofs 0x17914: identyczne wartości A/B (byte-identity rekordu 4508 — FAKT, zweryfikowany bajtowo);
     4508.obj (Scripts.ark CD-2003, zdekodowany) = „Root Model” z 26 bindingami siatek — dopasowanie 1:1 z NiArkTexture modelu]
    ↓ A = model id
 296445.nif (Models.bnt)  +  296446.bvi (Volumes.bnt, lokalna kolizja)
    kategoria: hierarchy 201→477→4751→4508 (tree_paths VFS klienta pośredniego/późniejszego — ArkVFS02 [E-A2];
               EU: krawędzie 4751→4508 @ofs 46,264 i 4751 pod 477)
```

Weryfikacja krzyżowa template↔model (korespondencja zestawów tekstur modeli z bindingami skryptów): 296445 → 26 nazw = 4508.obj ✓ (komplet, w tym b047_01_4, _5, lens_1_07); 126740 → 25 nazw (bez lens_1_07) = 4752.obj ✓; 278453 → 23 nazwy (bez _4, _5, lens_1_07) = 2249.obj ✓. Rozbieżności ZERO.

**Rozstrzygnięcia tropów z audytu (podwójnie zweryfikowane: audyt zewnętrzny [probe.json/terrain-followup.json] + PE-MASTER — cytowane, nie powtarzane po raz trzeci [E-G4]):**
- **4751×301 w skryptach** = 150 plików × [offsety 8, 60] (pola nagłówkowe DLOB: self-ID i parent-ID — nie lokalizacje) + 4751.obj.dec self-ID @4; żadne z tych trafień nie jest lokalizacją instancji.
- **4508×18 w terrain.bnt** = 10 pól dsize z długością rozpakowaną dokładnie 4508 B + 7 pól packedSize w indeksie BNT2 + 1 trafienie przecinające pola crc/nul wpisu 008700ac.tdf; żadne nie jest referencją template'u.

---

## 6. Weryfikacja kandydata na placement — stan łańcucha

Docelowy łańcuch: rekord świata → instancja → model → pozycja/obrót/skala.

| Ogniwo | Stan |
|---|---|
| model → bajty | CONFIRMED (Models.bnt wpis, SHA, CRC) |
| template → model | CONFIRMED (VFS A-pole, 2 ery, 2 niezależne źródła + korespondencja mesh-set) |
| kategoria → template | CONFIRMED (hierarchy 4751→4508, 2 ery) |
| **instancja (template + XYZ) → sektor/teren** | **NOT_FOUND_IN_SEARCHED_SCOPE — nie znaleziono potwierdzonego rekordu historycznej instancji 296445 w opisanym zakresie [E-D1]**; kanon RE PE2/2003: istnieje sieciowa ścieżka dostarczania pozycji (strumień sesji, byte-evidenced w PE2/2003); zapisy sesji nie istnieją w korpusie (FIRST_PEINST 0/6); **ścieżka sieciowa dowodzi istnienia takiej ścieżki, NIE wyłączności — sceny lokalne/pośrednie ID/sektorowe dane w 9.3.5 pozostają OTWARTE [E-D2]** |

Zgodnie z treścią zadania: **„nie znaleziono w zbadanym zakresie”**, a nie „lokalizacji nie ma”. Zakres negatywu: (a) wszystkie pliki pcg_install/Data (2.38 GB surowe: u32LE [run] + u32BE [audytor PE-MASTER: 0 trafień BE dla 296445/296446] **[E-F10]** + 281 MB zdekompresowane: LE [run + audytor] + BE [audytor]), (b) VFS i skrypty 2003 po dekodowaniu, (c) rekordy template'ów obu er na poziomie pól. NIE przeszukiwane zawartościowo (jawny bound): payloady Strings/*.bnt (szyfrowane blob-448, klasa lokalizacyjna; indeksy bez 296445) — dekoder z kanonu istnieje jako trop, nie był użyty w tym runie; wnętrza mediów (BIK/WAV/DDS) tylko po wzorcach; .prt niezdekodowane; pola UNKNOWN.

---

## 7. RETRAKCJA WŁASNA (nauczka — głośno)

W pierwszym pełnym skanie u32 użyłem wzorca „45 88 04 00” z błędnej konwersji heks (296445 ≠ 0x48845; poprawnie **296445 = 0x000485FD → FD 85 04 00**). Wszystkie wnioski pierwszego skanu u32 były na ZŁYM wzorcu (= szukałem liczby 297,029). Błąd wychwycony przez sprzeczność z zewnętrznym rejestrem kanonicznym (vfs_corpus_register.csv zawierał A_model=296445, a mój skan twierdził brak) i potwierdzony bezpośrednim dumpem bajtów rekordu (ofs 0x17914: fd 85 04 00). Skan powtórzony z asercją konwersji odwrotnej (struct.pack→unpack). Artefakty: RAWSCAN_HITS.json (przestarzały, błędny wzorzec — ZASTĄPIONY), RAWSCAN_CORRECT_HITS.json (obowiązujący; reprodukcja niezależna w erracie: rawscan.py — bramka G2 PASS). Wniosek metodologiczny: każdy wzorzec binarny musi być zweryfikowany konwersją odwrotną PRZED użyciem. **[Nauczka zastosowana w erracie: rawscan.py assertuje konwersję odwrotną przed użyciem wzorca; dodatkowo bramka G2 wyłapała (i wymusiła naprawę) błąd scalania słowników wzorców u32/ASCII o tym samym kluczu — pokazuje, że bramki mają zęby.]**

---

## 8. Zakres przeszukany / nieprzeszukany

**Przeszukane w pełni:** pcg_install/Data (wszystkie kontenery + media po wzorcach; Parameters po polach rekordów; endianness: u32LE pełny korpus [run] + u32BE pełny Data [audytor PE-MASTER: 0 trafień BE dla 296445/296446] **[E-F10]**), terrain po dekompresji (LE: run + audytor; BE: audytor **[E-F10]**), korpusy 2003 (Models.ark — wpis i payload; Scripts.ark surowo), zdekodowany korpus .obj.dec, BNT_Models (wpis+payload), VFS klienta pośredniego/późniejszego (ArkVFS02 — rejestr + rekordy; era ≠ 2003-CD, dokładna era nieustalona **[E-A2]**).

**Wsparte kanonem (nie powtórzone):** PE_PLACEMENT_ENCODING_CENSUS_R1 (23 kodowania × 29 kotwic × 5 korpusów = 1,975 plików / 1.90 GB — PASS-NEGATIVE na pary współrzędnych; brak tabeli spawn w skryptach 2,712 pozycji), PE_WORLD_DYN1_VFS_CORPUS_PARSE_R1 (rejestr 3,065 template'ów, B-pole = .bvi, ładowarka .bvi @VA 0x520D88→0x465BD0), PE_WORLD_DYN1_TEMPLATE_READER_GHIDRA_R1 (PLACEMENT_SOURCE=SERVER-DELIVERED, byte-evidenced — **dla binarium PE2_unpacked_out.exe 2003, SHA 561789…; NIE dla Entropia.exe 9.3.5** **[E-A1]**), PE_WORLD_DYN1_SFO_CAPTURE_R1 (runtime: ścieżka świata uśpiona przed loginem).

**Nieprzeszukane (bound):** payloady Strings/*.bnt po dekodowaniu (szyfrowanie blob-448) **[E-F9 — poprawka literówki „.bpt"]**; wnętrza nośników WAV/BIK/DDS (tylko wzorce); .prt niezdekodowane; żadnych zapisów sesji serwera (nie istnieją); RE konsumenta A-pola w Entropia.exe (patrz §9).

---

## 9. Jeden następny eksperyment (P0) — POPRAWIONY [E-V2R007]

**Pytanie P0 (resolver-agnostyczne — poprawka wady V2R-007 oryginalnego sformułowania, które wpisując ścieżkę „%d.nif" zakładało format resolvera z góry):** jaki jest FAKTYCZNY konsument rekordu template'u 4508 w kliencie EU 9.3.5 (Entropia.exe, SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31) — od pola A (rekord @96,496, A=296445 @96516) przez FAKTYCZNY resolver zasobu (ścieżka/ID/tabela — NIE zakładamy formatu) → model → utworzenie instancji → ŹRÓDŁO transformacji → rejestracja sceny?

Projekt (per adjudykacja PE-MASTER; run PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912): statyczny Ghidra-run na Entropia.exe 9.3.5 (bez uruchamiania klienta), z WŁASNĄ weryfikacją SHA binarium / image-base / mapowania VA↔offset PRZED użyciem jakichkolwiek adresów; **zakaz automatycznego transferu adresów PE2** (łańcuch PE2 „.nif" @0x610368 → 0x00520EE0 → FUN_00522010 z kanonu TEMPLATE_READER = WZORZEC WYSZUKIWANIA analogu, nie transfer wartości); A/B/C badane oddzielnie; kontrola negatywna: wrong-ID (sibling 4752/2249). NON-PASS: CHAIN_ABSENT / ARG_FROM_OTHER_FIELD / INDIRECT_ONLY / TOOL_BLOCKED. Wyniki podzielone: A (tożsamość definicji) / B (loader modelu) / C (źródło transformacji instancji) / D (lokalizacja — jeśli odzyskana). **Poszukiwanie placementu pozostaje OTWARTE** (poszukiwanie także pośrednich ID/sektorowych zapisów, nie tylko u32 296445).

---

## 10. Artefakty (SHA256 w manifeście erraty: 02_EVIDENCE/MANIFEST_SHA256.csv)

| Plik | Opis |
|---|---|
| R1 01_RAW/296445.nif | wyodrębniony payload (656795d8…) — bez zmian |
| R1 01_RAW/296446.bvi | wyodrębniony BVI (7fee519b…) — bez zmian |
| R1 01_RAW/EXTRACT_PROVENANCE.json | tożsamość/offset/metoda ekstrakcji — bez zmian |
| R1 01_RAW/BLOCKMAP_V2.json | pełny dump 155 bloków — bez zmian (wejście rekomputacji erraty) |
| R1 02_ANALYSIS/BLOCK_TABLE_FULL.csv | tabela 155 bloków — bez zmian |
| R1 02_ANALYSIS/TRANSFORM_TABLE.csv | tabela transformacji — **world_T/bbox_world SUPERSUMOWANE (patrz ERRATA B1–B3); poprawna wersja: 01_CORRECTED/TRANSFORM_TABLE_CORRECTED.csv** |
| R1 02_ANALYSIS/TREE_ANALYSIS.txt | drzewo sceny + census — **sekcje bbox SUPERSUMOWANE; poprawna wersja: 01_CORRECTED/TREE_ANALYSIS_CORRECTED.txt** |
| R1 02_ANALYSIS/TREE_MESHES.json | statystyki meshy — **world_T/bbox_world SUPERSUMOWANE; poprawna wersja: 01_CORRECTED/TREE_MESHES_CORRECTED.json** |
| R1 03_SEARCH/RAWSCAN_CORRECT_HITS.json | wyniki skanu (poprawny wzorzec) — bez zmian; **reprodukcja niezależna: 02_EVIDENCE/RAWSCAN_REPRO.json (bramka G2 PASS, offset-exact)** |
| R1 03_SEARCH/RAWSCAN_HITS.json | wyniki skanu ZASTARZAŁE (błędny wzorzec — §7) — bez zmian |
| R1 00_CONTROL/*.py | 6 skryptów odtwarzalnych — bez zmian (analyze_tree.py zawiera bug B1; POPRAWIONA KOPIA: errata 00_CONTROL/analyze_tree_v2.py) |
| ERRATA 00_CONTROL/analyze_tree_v2.py | poprawiony instrument (konwencja world = parent∘local; bramka G1 assertowana) |
| ERRATA 00_CONTROL/rawscan.py | niezależny generator reprodukujący RAWSCAN_CORRECT_HITS.json (bramka G2) |
| ERRATA 01_CORRECTED/* | poprawiony raport (ten dokument) + zrekompensowane artefakty transformacyjne |
| ERRATA 02_EVIDENCE/* | manifest SHA256, wyniki bramek G1/G2, reprodukcje skanów |
| ERRATA 03_REPORT/ERRATA.md | pełna lista korekt z cytatami zastępowanych twierdzeń |

Oryginały gry i silnika: READ-ONLY (niezmienione). Run R1: NIETYKALNY (hashy przed/po identyczne — bramka G7 erraty). Parser produkcyjny/viewer/porty: nietknięte. Badanie zawarte w katalogu runu erraty; oryginalne payloady (296445.nif, 296446.bvi) pozostają LOCAL-ONLY z metadanymi w manifeście.

**Statusy użyte:** CONFIRMED (dowód bajtowy/zgodność niezależnych źródeł), SUPPORTED (korelacja mocna, brak pełnego łańcucha), UNKNOWN (semantyka nieustalona), UNVERIFIED (twierdzenie transferu między erami bez dowodu w docelowym binarium **[E-A1]**), NOT_FOUND_IN_SEARCHED_SCOPE (negatyw z zakresem). Żadnego podniesienia statusu ponad dowód.
