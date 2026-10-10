# GAMEBRYO_IMPLEMENTATION_LINKS — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010

Data: 2026-10-10. Kontrakt §7: „Wykorzystaj lokalne źródła… Czytaj tylko
mechanizmy potrzebne aktualnym poprawkom: lifecycle/load-unload,
hierarchy/instance separation i texture/material bindings. Wersje 1.1.2/2.6
traktuj osobno. Dla każdego wykorzystania: source/version/SHA → zaobserwowany
mechanizm → istniejący dowód PE albo GAP → decyzja adaptera → wykonany test.”

## 0. Źródła przeczytane w tym runie (IDENTYTET ZMIERZONY; READ-ONLY)

Wszystkie pliki pochodzą z lokalnego SDK `D:\gamebyroengine\extracted\
Gb12_Source` (Gamebryo 1.2; oznaczenie „Gb12” wg istniejącej konwencji
projektu z tools/gamebryo_oracle). Żaden bajt SDK NIE został skopiowany do
repo. Wersje 1.1.2/2.6 nie były czytane w tym runie (posługują się nimi
wcześniejsze linie projektu — patrz nagłówek tools/pecompat/nif41_deep.mjs
dla 4.1/„1.2” pól layoutu z wcześniejszych faz).

| Plik | B | SHA256 |
|---|---:|---|
| CoreLibs/NiMain/NiStream.cpp | 38 458 | E955C36EBBB442029E00BE8A154726741B8454A607F2DC043F1FD542B009DC25 |
| CoreLibs/NiMain/NiNode.cpp | 33 897 | 38C7A1DE1E166345068D296F70F34B1ADAE27C694E19EAD8FA0FBD8B62E0E016 |
| CoreLibs/NiMain/NiAVObject.inl | 10 672 | 09E1A5A5C88AF503D9566B487941305307CBA5CB1513147FB49E5A4DBDC91C3B |
| CoreLibs/NiMain/NiTexturingProperty.cpp | 32 194 | 2BC36C08E8B9E0AB624569FF098F1CD60B8242B737C0EB7B3E4DD3A6615BA106 |
| CoreLibs/NiMain/NiSourceTexture.cpp | 14 704 | B5D0BB026B812CA4D022E110D7CFE0B98ECA181C06F78C62A999512C0927E70E |
| Samples/ST_Applications/MOUT/TerrainManager.cpp | 7 148 | CDAD77BAB6E448AC36CB88A3DF5867CDA8F9E30A1D8D874D76B4FED34ABAC63E |
| Samples/Demos/BackgroundLoad/BackgroundLoad.cpp | 5 746 | 8287A6AECB058D71978C7C6A1F3DB382447C764B15CFAE082078615D152475B1 |

## 1. Lifecycle / load-unload — Samples/Demos/BackgroundLoad/BackgroundLoad.cpp

- **Zaobserwowany mechanizm** (linie ~91–135, OnIdle): tło ładuje się przez
  `NiStream::BackgroundLoadBegin` + sonda `BackgroundLoadPoll(&kLoadState)`
  z progress read/link; GOTOWY obiekt jest ATTACHOWANY do sceny dopiero przy
  `NiStream::IDLE`; aplikacja śpi (NiSleep) dając wątkowi streamu szansę.
  Oddzielenie „żądanie ładowania → sonda → commit na scenie”.
- **Istniejący dowód PE albo GAP**: brak odzyskanego PE pagingu terenu (GAP —
  nasz streaming nie jest roszczeniem do stock PE). DOWÓD POCHODZĄCY z R1:
  ryzyko utraty najnowszego żądania (WL-1, PRE_COUNTERCHECKS).
- **Decyzja adaptera** (kontrakt §3.1): requestScene/latest-wins — każde
  przebudowanie terenu/tekstur/roślinności niesie id żądania; wynik
  przestarzały ABORTUJE przed apply (z dispose pobranych-a-niezaaplikowanych
  zasobów GPU); najnowsze żądanie w kolejce wyciągane po zakończeniu
  bieżącego; spójność (coherence) żądania pokazywana uczciwie
  („terrain A + trees B” nigdy nie jest READY).
- **Wykonany test**: WORLD_VEG_RESOURCE_DISCIPLINE + R2 świat scenariusz S1
  (scena GOTOWA tylko gdy wszystkie komponenty tego samego żądania) oraz
  POST_COUNTERCHECKS WL-1 (latest-wins naprawione: final origin B=(1,0)).

## 2. Stream lifecycle — CoreLibs/NiMain/NiStream.cpp

- **Zaobserwowany mechanizm**: LoadHeader → LoadRTTI → LoadObjectGroups →
  LoadTopLevelObjects; ResolveLinkID (linie 226+; „read a link id and
  immediately resolve it”) — post-link-owany graf sceny po fazach odczytu.
- **Dowód PE / GAP**: NifModelReader (src/pesource) już modeluje zamknięty
  odczyt v10.1.0.0 z LOUD odmowami (istniejący kwalifikowany importer).
  NiArkTextureExtraData to rozszerzenie MindArk NIEobecne w SDK (GAP w SDK;
  obsłużone przez reader canon, ARK 9-bajtowy ogon pozostaje RAW-ONLY).
- **Decyzja adaptera**: BEZ ZMIAN (brak nowego dekodera formatu; brak
  kopiowania layoutów SDK).
- **Wykonany test**: WORLD_VEG_MODEL_IMPORT_SUPPORT (witness 457485:
  v10.1.0.0, 16 wierzchołków, tekstura 457490) + T6_witness_457485_untouched
  (reader byte-identical z BASE).

## 3. Hierarchy / instance separation — NiNode.cpp + NiAVObject.inl

- **Zaobserwowany mechanizm**: NiNode trzyma listę dzieci
  (AttachChild/DetachChildAt/SetAt, ~linie 34–130); NiAVObject ma parent
  (DetachParent/GetParent, .inl 14–27) — JEDNA geometria może być
  współdzielona przez wiele miejsc w grafie; transformy komponowane po
  hierarchii (update methods, NiNode.cpp ~169).
- **Dowód PE**: kształt→property→data relacje i shape-own TRS już odzyskane
  (iter032; buildShapeRenderables komponuje TRS kształtu przed mostkami osi).
- **Decyzja adaptera**: THREE.InstancedMesh ze WSPÓLNYM geometry+material per
  (model, shape) i RZECZYWISTYMI macierzami per instancja — geometry sharing
  IS NOT instance sharing (niezmienione z R1; §6.8).
- **Wykonany test**: WORLD_VEG_RESOURCE_DISCIPLINE (meshesAreInstanced +
  instanceDistinct: dwie instancje tego samego modelu mają różne macierze) +
  instance_separation.test.mjs.

## 4. Texture/material bindings — NiTexturingProperty.cpp

- **Zaobserwowany mechanizm**: mapa slotów per property (SetMap(uiIndex);
  BUMP_INDEX=5, DECAL_BASE; slot BASE=0 to domyślny kolor bazowy;
  ~linie 38–172). Sloty mają NUMERY i kolejność, nie dowolny zbiór.
- **Dowód PE**: NiArkTextureExtraData 519316 nazywa wpisy
  `bridge_02_*_BASE`/`_DARK`/`_DETAIL` — nazwy slotów pokrywają się ze
  słownikiem slotów SDK (era-evidence, nie dowód ABI).
- **GAP**: który slot 9.3.5 faktycznie wiąże jako albedo pozostaje
  UNRESOLVED — decyzja RENDER_RECONSTRUCTION (pierwszy rozwiązywalny slot w
  KOLEJNOŚCI wpisów, z jawną diagnostyką pominiętych slotów), NIGDY nie
  podawana za historyczny materiał.
- **Wykonany test**: BROWSER_INTERACTION S10 (519316: 3/3 kształty
  teksturowane przez realny łańcuch slotów; „sloty pominięte: 0”) +
  VEGETATION_CENSUS (slotDiagnostics: 0 w oknie domyślnym; pominięte sloty
  liczone jawnie tam, gdzie występują).

## 5. Texture lifetime — NiSourceTexture.cpp

- **Zaobserwowany mechanizm**: Create(pcFilename,…) ustawia nazwę pliku
  (standardyzacja ścieżki, linie 35–50); piksele ładują się LENIWIE
  („m_pcFilename && !m_spSrcPixelData → load”, linie ~117–127) — jedna
  tekstura źródłowa, piksele raz.
- **Dowód PE / GAP**: PE używa NUMERYCZNYCH id tekstur (id@+16 →
  „<id>.dat” w Textures.bnt — potwierdzone silnikowo, M1_TSFS iter015e/
  iter030), NIE filename-lookup z SDK (GAP między mechanizmami — jawnie
  inne API).
- **Decyzja adaptera**: współdzielony cache tekstur per textureId
  (jedno fetch+strict-decode per id, reuse przez wszystkie modele;
  bounded LRU; identity-checked) — duch leniwego źródła SDK w naszym API.
- **Wykonany test**: WORLD_VEG_RESOURCE_DISCIPLINE (texIdentityReused —
  ten SAM obiekt po powrocie okna; brak re-fetch) + R2_DDS_QUALIFIED
  (dyscyplina strict-decode rozszerzona o kwalifikowany DDS DXT1/DXT5).

## 6. Terrain paging pattern — Samples/ST_Applications/MOUT/TerrainManager.cpp

- **Zaobserwowany mechanizm**: menedżer terenu z pick/ground-texture
  (SetReturnTexture(false), Update na terrain graph) — przykład aplikacji
  SDK, NIE dokumentacja terenu PE.
- **Dowód PE / GAP**: brak dowodu, że PE 9.3.5 paginował teren jak MOUT
  (GAP); brak odzyskanego stock pagingu (contract §4: „nie odzyskany stock
  PE paging”).
- **Decyzja adaptera**: WŁASNA polityka LOD near(8×8 RAW)/mid(8×8-decymowane
  RZECZYWISTE próbki)/far(4×4-decymowane, census-gated), z liniami cięcia
  dopasowanymi do tych samych oryginalnych próbek (bez szwów, bez skirtów),
  z jawnymi dziurami na kafle NODATA.
- **Wykonany test**: R2_LOD_ROUTES (bit-exact vs niezależna decymacja
  payloadów; negative 400) + R2_HEIGHT_HALO_BOUNDARY + BROWSER S5
  (teleport daleki i powrót: windowFollowed + sameConfigSameCounts) +
  PIXEL teleportFarVsHome diff 83.5%.

## Status

NIE twierdzimy „100% Gamebryo understood” ani „whole original game
reimplemented”. Każde użycie powyżej jest ograniczone do przeczytanego
mechanizmu i wykonanego testu tego runu. MOUT/SDK nie dowodzą formatu world
data PE, lokalnego placementu ani konkretnego ABI/offsetu PCG.
