# ERRATA — PE_296445_NIF_ORIGIN_PLACEMENT_R1 (run audytowany) → ERRATA R1

**RUN_ID:** PE_296445_NIF_ORIGIN_PLACEMENT_R1_ERRATA_R1_20260912
**RUN_AUDYTOWANY (NIETYKALNY):** PE_296445_NIF_ORIGIN_PLACEMENT_R1_20260912 (`D:\Eudoria_Reconstruction\09_Research\PE_296445_NIF_ORIGIN_PLACEMENT_R1_20260912`)
**WERDYKT PE-MASTER dla R1:** MASTER_PARTIAL_PASS (advisory; PROVISIONAL_UNTIL_QUALIFIED) z rozszerzoną listą korekt — patrz `03_REPORT\PE_MASTER_REVIEW.md` (persisted verbatim)
**RUN_CLASS:** MATERIAL (errata dokumentacyjna + mechaniczna rekomputacja z gwarantowanymi wartościami oczekiwanymi; ZERO nowej forensyki; ZERO nowych twierdzeń poza adjudykowaną listą korekt)
**AUTORZY KOREKT:** adjudykacja PE-MASTER (7/7 ustaleń audytu zewnętrznego ACCEPTED, każde fizycznie zweryfikowane niezależnie); wykonanie erraty: pe-master-auditor
**ŹRÓDŁA KOREKT:** audyt zewnętrzny cross-engine `C:\Users\User\Documents\ChatGPT\PE\audit-296445-placement-r1\AUDYT.md` (ustalenia F1–F5 + tropy A/B/C z probe.json/terrain-followup.json); rozszerzona lista korekt PE-MASTER (grupa F: F1–F10, grupa A: era-mixing); wartości oczekiwane bramki G1: podwójnie zweryfikowane (audyt zewnętrzny probe.json + rekomputacja PE-MASTER).
**WYJŚCIE POPRAWIONE:** `01_CORRECTED\00_RAPORT_CORRECTED.md` (pełna poprawiona wersja raportu z markerami [E-…] wskazującymi niniejsze pozycje).

---

## 0. Zasady niniejszej erraty

1. Run R1 pozostaje IMMUTABLE — żaden plik R1 nie został zmieniony (bramka G7: hashe wszystkich 18 plików R1 przed/po identyczne — patrz §9).
2. Dowody nie są cicho podmieniane: każda korekta odwołuje się do CYTATU zastępowanego twierdzenia z raportu R1 i wskazuje fizyczne źródło poprawki.
3. Poprawny raport (01_CORRECTED) jest pełną wersją — zachowuje potwierdzony rdzeń nauki (podwójnie zweryfikowany: PE-MASTER + audyt zewnętrzny), zmienia wyłącznie pozycje z listy korekt.
4. Wartości oczekiwane bramki transformacyjnej (G1) są bramką REPRODUKCJI, nie hipotezą: zostały niezależnie wyliczone przez audytora zewnętrznego (probe.json, własna kompozycja w JS) i PE-MASTER (rekomputacja); niniejsza errata odtwarza je TRZECIM, niezależnym instrumentem (analyze_tree_v2.py) i assertuje zgodność.
5. Semantyka zmian: errata NIE modyfikuje oryginalnych pomiarów R1 (mapa 155 bloków, census typów, stringi, byte-identity 3 er, rekord template'u, census referencji) — te pozostają CONFIRMED per adjudykacja.

---

## 1. GRUPA A — SEPARACJA ER (P1, najwyższy priorytet)

### A1. Handler sieciowy przypisany niewłaściwej erze binarium

- **Zastępowane twierdzenie (R1 §9 wiersz 9 tabeli ROZSTRZYGNIĘCIE; §5 łańcuch „Potwierdzone odniesienia"; §6; §8):**
  > „kanon RE klienta (Entropia.exe 9.3.5, SHA E7785430…): pozycje instancji dostarcza WYŁĄCZNIE serwer w zaszyfrowanym strumieniu sesji (Blowfish, handler FUN_005977b0; rekord 0x1C + sub-rekord transformacji f32 XYZ w ofs +0x2c/+0x30/+0x34, SetPosition przez vtable[0x50])"
- **FAKT (źródło: audyt zewnętrzny F1; PE-MASTER potwierdził hashe):** mechanizm (handler FUN_005977b0, rekordy 0x1C, transform f32 @+0x2c/+0x30/+0x34, SetPosition vtable[0x50]) pochodzi z analizy binarium **PE2_unpacked_out.exe (2003), SHA256 56178993692A7409C896398089E482EDDF96177666BACB91A8CC1A638D9A0650** (kanon: `99_Audits\PE_WORLD_DYN1_TEMPLATE_READER_GHIDRA_R1_20260903_160000\00_Control\analysis_methodology.md`, „Binary SHA256 561789… — MATCH"). **To nie jest Entropia.exe 9.3.5 (SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31) — to różne binaria.** Adres funkcji nie jest identyfikatorem semantyki przenośnym między buildami.
- **Korekta (zastosowana w 00_RAPORT_CORRECTED.md):** każde wspomnienie handlera/vtable/rekordu oznaczone erą „PE2/2003 (byte-evidenced w kanonie TEMPLATE_READER dla binarium 561789…)" + jawna nota: „mechanizm pozycji w EU 9.3.5: **UNVERIFIED** — wymaga trace w Entropia.exe 9.3.5 (HIPOTEZA TRANSFERU między erami)". Fraza „dostarcza WYŁĄCZNIE serwer" wycofana (patrz D2).
- **Status nowy:** mechanizm PE2/2003 CONFIRMED w swoim binarium; mechanizm EU 9.3.5 UNVERIFIED (hipoteza transferu).

### A2. Etykieta ery korpusu VFS („VFS 2003")

- **Zastępowane twierdzenie (R1 wiersz 5 i 8 ROZSTRZYGNIĘCIA; §5 łańcuch; §8):**
  > „obecny … w erze 2003 (rejestr kanoniczny + rekord w ofs 0x17914)"; „Hierarchia kategorii: 201→477→4751→4508 (2003, tree_paths kanoniczny)"; „VFS 2003 (rejestr + rekordy)"
- **FAKT (źródło: audyt zewnętrzny F1; kanon TEMPLATE_READER `02_ANALYSIS\03_template_consumers.md`):** rodzina hierarchy.vfs/templates.vfs ma magię **ArkVFS02** i jest **NOT-IN-PE2** — warstwa klienta POŚREDNIEGO/PÓŹNIEJSZEGO. Katalog `01_Original_Files\VFS` nie jest spętany z erą 2003-CD; dokładna era nieustalona.
- **Korekta:** etykieta „VFS 2003" zastąpiona przez „VFS klienta pośredniego/późniejszego (ArkVFS02; era ≠ 2003-CD; dokładna era nieustalona)" w każdej lokalizacji.
- **Bez zmian:** **byte-identity rekordu 4508 między templates.vfs pcg 9.3.5 (@96,496) a tym korpusem (@0x17914) pozostaje FAKTEM** (PE-MASTER zweryfikował bajtowo). Etykiety „Scripts.ark CD-2003" i „decoded .obj korpus CD-2003" pozostają (poprawne per kanon census).

---

## 2. GRUPA B — TRANSFORMACJE (P2) + REKOMPUTACJA (BRAMKA G1)

### B1. Bug instrumentu badawczego R1 (nie parsera produkcyjnego)

- **Zastępowany artefakt:** `R1 00_CONTROL\analyze_tree.py`, funkcja `compute()`: `world[i] = cur` zapisuje transformację RODZICA jako world obiektu; dopiero `w = compose(cur, local)` jest przekazywane dzieciom, ale **nie jest zapisywane jako world bieżącego obiektu**. Geometria przekształcana przez `world[mesh]` — **pomija WŁASNĄ transformację mesha** (źródło: audyt zewnętrzny F2).
- **Korekta:** NOWA poprawiona kopia instrumentu: `00_CONTROL\analyze_tree_v2.py` (plik R1 NIETYKANY). Konwencja: **world[i] = parent_world ∘ local_i (z własną transformacją), parent korzenia = identity**.
- **Uwaga zakresu (audyt F2):** parser produkcyjny/viewer NIE został zmieniony — błąd dotyczył wyłącznie sondy badawczej R1.

### B2. Zrekompensowane artefakty (01_CORRECTED\)

| Artefakt poprawiony | Artefakt R1 (superseded) |
|---|---|
| `01_CORRECTED\TRANSFORM_TABLE_CORRECTED.csv` (kolumny R1 + `world_T_r1_superseded` + `changed_vs_r1`) | `02_ANALYSIS\TRANSFORM_TABLE.csv` (world_T/bbox_world dla 14 meshy błędne) |
| `01_CORRECTED\TREE_MESHES_CORRECTED.json` (statystyki poprawione + konwencja + bbox globalny + wyniki bramki) | `02_ANALYSIS\TREE_MESHES.json` |
| `01_CORRECTED\TREE_ANALYSIS_CORRECTED.txt` (drzewo + POPRAWIONE sekcje bbox + census) | `02_ANALYSIS\TREE_ANALYSIS.txt` (sekcje bbox błędne) |
| `02_EVIDENCE\G1_GATE_RESULTS.json` (wyniki bramki + hashe wejść) | — (nowy) |

### B3. Wyniki rekomputacji (BRAMKA G1 — assertowana w analyze_tree_v2.py, odtworzona a nie wpisana)

- **14 z 30 meshy zmienia world_T** względem TRANSFORM_TABLE.csv R1; pozostałe **16 identycznych** (kontrola negatywna). Zmienione: 32, 66, 72, 75, 82, 90, 94, 115, 121, 127, 133, 139, 145, 151.
- **Poprawny bbox całości: min (-2500.0, -2500.0, -1.2652602576768146e-08) do max (2500.0, 2500.0, 15620.0)** (tolerancja bramki 1e-4 bezwzgl.; uzyskano EXACT; wartość ujemna Z to epsilon numeryczny kompozycji, nie przesunięcie).
- **Mesh #66 B_Eu_b047_glowsak:0 poprawne T = (401.14190673828125, -1611.4522705078125, -368.0000305175781)** (równość dokładna co do f64).
- Krzyżowa weryfikacja (G1d): wszystkie 14 poprawionych world_T zgodne z probe.json audytora zewnętrznego (max odchylenie ≤ 1e-6; realnie ~1e-9) — niezależna lineage obliczeń (JS audytora vs Python erraty).
- **Zgodność potrójna:** audyt zewnętrzny (probe.json) == PE-MASTER (rekomputacja) == niniejsza errata (analyze_tree_v2.py). Rozbieżność = FAIL bramki — brak rozbieżności.

### B4. Przeredagowanie §2.3 i §3B (semantyka bboxu i 7. floata)

- **Zastępowane twierdzenie (R1 §2.3):**
  > „Zgodność co do wartości f32 — **ogon importera to metadana bboxu modelu (przestrzeń B), NIE placement świata**. To domyka empirycznie semantykę „7 floatów" ze schematu empirical (bbox min xyz + max xyz + 0.0)."
  oraz (R1 §3B): „kompozycja parent×local (root = identity): bbox globalny geometrii = (-3934.0, -2500.0, -476.4)..(12593.8, 3744.0, 15620.0)"
- **FAKT (audyt F2 + rekomputacja):** ogon importera == ekstrema SUROWYCH tablic wierzchołków z RÓŻNYCH układów lokalnych (identyczność bitowa pozostaje faktem), ale **NIE jest to bbox sceny po złożeniu**; poprawny bbox sceny = ±2500/±2500/[~0, 15620] ≈ 5000×5000×15620 jednostek modelu; **semantyka siódmego floata (0.0) = UNKNOWN** (zgodność 6 wartości nie dowodzi roli siódmej).
- **Korekta:** §2.3 i §3B przeredagowane (cytaty wyżej — usunięte); zdanie „To domyka empirycznie semantykę «7 floatów»" WYCOFANE. Fraza „Object06 — daleko od rdzenia" (§3A) skorygowana: po złożeniu bbox Object06 = (-2002,-2011,332)..(2002,2002,1396) — wewnątrz obrysu (mylenie układu lokalnego z układem modelu).

---

## 3. GRUPA C — RETRAKCJA FAŁSZYWEGO NEGATYWU SKRYPTOWEGO (P2)

- **Zastępowane twierdzenie (R1 §5, wiersz „Korpus skryptów 2003 po dekodowaniu"):**
  > „0 odniesień do 296445; template 4508.obj binduje komplet 26 siatek modelu (…)"
- **FAKT (audyt F3, offsets + konteksty w probe.json; PE-MASTER potwierdził):** u32 296445/296446 występują w 4508.obj.dec (**@664/@580**, immediates bytecode VM); 126740 w 4752.obj.dec (**@520**); 278453 w 2249.obj.dec (**@664**); 0 trafień ASCII; 0 w pozostałych skryptach.
- **Korekta (tekst w 00_RAPORT_CORRECTED §5):** „u32 296445/296446 występują WYŁĄCZNIE w 4508.obj.dec (@664/@580, immediates bytecode VM); 126740 w 4752.obj.dec (@520); 278453 w 2249.obj.dec (@664); 0 trafień ASCII; 0 w pozostałych 1,933 skryptach. To WZMOCNIENIE powiązania definicja↔model, NIE placement."
- **Nota mianownika (weryfikacja erraty):** kontrakt korekty podawał „pozostałych 1,932" — to artefakt arytmetyczny (1,936 − 4 TRAFIENIA). Poprawny mianownik plikowy: 1,936 − 3 pliki z trafieniami = **1,933**. Zweryfikowano niezależnym skanem erraty (1,936 plików .obj.dec w `99_Audits\PE_WORLD_DYN1_INGEST_PARSER_GHIDRA_R1_20260903_120000\03_EVIDENCE\decoded`; zbiór plików z trafieniami: {4508, 4752, 2249}).
- **Nota pełności (skan erraty):** skan reprodukcyjny na pełnym zbiorze 6 wzorców u32LE (296445/296446/126740/126741/278453/278454) wykrył dodatkowo kompani +1 w tych samych plikach (126741 @4752.obj.dec@436; 278454 @2249.obj.dec@580) — spójne ze wzorcem par A/B (B=A+1); zapisane w 02_EVIDENCE\SCRIPT_SCAN_REPRO.json jako pełny wynik reprodukcji (nie część adjudykowanego tekstu korekty).

---

## 4. GRUPA D — RETRAKCJA GLOBALNEGO NEGATYWU I „WYŁĄCZNIE SERWER" (P2)

### D1. Globalny negatyw nagłówkowy

- **Zastępowane twierdzenie (R1 werdykt jednozdaniowy):**
  > „**placement świata NIE jest zapisany w żadnych danych klienta** — przychodził per-instancja ze strumienia sesji serwera (kanał byte-evidenced w RE klienta), którego zapisy nie istnieją w korpusie."
- **FAKT (audyt F4):** sformułowanie przeczy własnym granicom raportu (nierozpoznane .prt, niedekodowane Strings, pola UNKNOWN).
- **Korekta:** „**Nie znaleziono potwierdzonego rekordu historycznej instancji 296445 w opisanym zakresie (NOT_FOUND_IN_SEARCHED_SCOPE)**." Jawne granice zachowane: payloady Strings (szyfrowane), wnętrza mediów (BIK/WAV/DDS tylko po wzorcach), .prt niezdekodowane, pola UNKNOWN.

### D2. „WYŁĄCZNIE serwer"

- **Zastępowane twierdzenie:** „pozycje instancji dostarcza WYŁĄCZNIE serwer" (R1 wiersz 9) oraz sekcje §6/§8 implikujące wyłączność.
- **FAKT (audyt F4 + adjudykacja):** ścieżka sieciowa w PE2 dowodzi ISTNIENIA takiej ścieżki, NIE wyłączności; sceny lokalne/pośrednie ID/sektorowe dane w 9.3.5 = otwarte.
- **Korekta:** fraza usunięta ze wszystkich lokalizacji; w §6 dodane: „ścieżka sieciowa dowodzi istnienia takiej ścieżki, NIE wyłączności — sceny lokalne/pośrednie ID/sektorowe dane w 9.3.5 pozostają OTWARTE".

### D3. Rozróżnienie pokrycia bajtów od semantyki

- **Korekta (dopisek przy rozliczeniu bajtowym §2 i §6):** „zero bajtów nierozliczonych = pełne pokrycie ZAKRESÓW bajtowych, nie dowód pełnej semantyki" (źródło: audyt F4).

---

## 5. GRUPA E — ARYTMETYKA 9 BAJTÓW (P3)

- **Zastępowane twierdzenie (R1 §2.4, powtórzone §2.7):**
  > „Pole 9-bajtowe = [00][FFFFFFFF][u32 ID w ofs 5][00]" (zapis zawierałby 10 bajtów)
- **FAKT (audyt F5; PE-MASTER potwierdził z własnych danych: 00ffffffff17ef0100 = 9 B):** pole = **[u8 0 @0][u32 -1 @1..4][u32 ID @5..8]**; bajt @8 to MSB ID (zawsze 0 dla ID < 2^24 — stąd złudzenie „dodatkowego bajtu"); **brak dziesiątego bajtu**.
- **Korekta:** opis §2.4 i wiersz §2.7 poprawione (katalog UNKNOWN: „UNKNOWN (poza ID)").
- **Korekta powiązana (§2.4, GeoTexanim01):** „animowanym atlasem (flipbook)" → „**UV-animacja potwierdzona (NiUVController, 2 klucze 0→5.0); interpretacja flipbook/atlas = HIPOTEZA (wymaga analizy obrazu)**" (audyt F5: określenie atlas/flipbook wymaga interpretacji obrazu i kluczy; NiUVController ≠ udowodniony NiFlipController).

---

## 6. GRUPA F — KOREKTY Z AUDYTU PE-MASTER (adjudykacja wcześniejsza)

| # | Zastępowane twierdzenie (R1, cytat/skrót) | Korekta | Źródło/Status |
|---|---|---|---|
| F1 | „50 slotów dzieci korzenia (w tym 30× -1 — puste sloty tablicy)" (§3) | „**27× -1 (23 realne dzieci)**" (BLOCKMAP_V2.json: 27; „30×" to literówka); census erraty niezależny: 50 slotów = 23 realne + 27× None | PE-MASTER; zweryfikowane w erracie z BLOCKMAP_V2.json |
| F2 | „EnvironmentZones.vfs (127 rekordów stref…)" (§5) | „**126 rekordów stref: 84 kanoniczne + 42 ogonowe, per PE_PLACEMENT_ENCODING_CENSUS_R1; rekord 128 B**"; „0 linków template↔strefa" pozostaje (zweryfikowane) | PE-MASTER (adjudykacja) |
| F3 | „NiStream.cpp: LoadTopLevelObjects: L~463" (§4) | „**L362**" (pozostałe cytaty linii poprawne) | PE-MASTER (adjudykacja) |
| F4 | „Właściciel: NiNode 62 „B_Eu_b047_reflex"" (§2.5, TextureEffect) | „**rodzic grafu = NiNode 62 „B_Eu_b047_reflex" (blok 13 jest dzieckiem 62 w grafie children); effects-owner = NiNode 59 „B_Eu_b047_gloss" (blok 59 ma effect 13 w tablicy effects)**" | PE-MASTER; zweryfikowane w erracie z BLOCKMAP_V2.json (13: child of 62; 59.effects=[13]) |
| F5 | „nazwy 505k–510k" (§5, Portals) | „**zakres nazw 382,811–592,741 (większość w 505k–510k)**" | PE-MASTER (adjudykacja) |
| F6 | „Parameters/*.vfs (28, 2.2 MB)" (§5) | „**27 plików (2.2 MB)**" | PE-MASTER (adjudykacja) |
| F7 | „sids.vfs (3,887 kluczy S_*)" (§5) | dopisek metody: „**3,885 unikalnych wg regexu audytora; 170 S_LOCATION; brak klucza SLUM — istota bez zmian**" | PE-MASTER (adjudykacja) |
| F8 | „warianty slum: b001_01, b047_01, b062_01" (wiersz 7) | **USUNIĘTE** (niepodparte artefaktem; korpus ma ≥10 rodzin slum — bez doprecyzowania źródła twierdzenie wycofane) | PE-MASTER (adjudykacja) |
| F9 | mojibake '?' + zduplikowana fraza w wierszu Portals; „Strings/*.bpt" (§8) | mojibake usunięty (fizycznie w wierszu terrain §5: „markerów/wpisów/są" — kontrakt wskazywał „wiersz Portals"; rzeczywista lokalizacja mojibake = wiersz terrain, zduplikowana fraza = wiersz Portals — obie poprawione); duplikat „brak ASCII/u32 odniesień do modelu" usunięty; „Strings/**.bnt**" | PE-MASTER (adjudykacja); lokalizacja mojibake sprecyzowana fizycznym grepem erraty |
| F10 | brak zakresu endianness przy „statyczne dane klienta przeszukane" (§6/§8) | dopisek: „**u32LE pełny korpus (run) + u32BE pełny Data (audytor PE-MASTER: 0 trafień BE dla 296445/296446); terrain po dekompresji LE (audytor: +BE)**" | PE-MASTER (audyt) |

---

## 7. GRUPA G — DOMKNIĘCIE PAKIETU

### G4. Rozstrzygnięcia tropów (podwójnie zweryfikowane: audyt zewnętrzny + PE-MASTER — cytowane, nie powtarzane po raz trzeci)

- **4751×301 w skryptach** = 150 plików × [offsety 8, 60] (pola nagłówkowe DLOB: self-ID i parent-ID — **nie lokalizacje**) + 4751.obj.dec self-ID @4. Źródła: probe.json (audyt: 301 trafień w 151 plikach: 150×2@{8,60} + 1×self@4) + adjudykacja PE-MASTER (kontrakt erraty). Interpretacja +8 jako rodzica wsparta układem i hierarchią; pełne znaczenie +60 wymaga konsumenta formatu. Żadne z tych trafień nie jest lokalizacją instancji.
- **4508×18 w terrain.bnt** = 10 pól dsize z długością rozpakowaną dokładnie 4508 B (każde zweryfikowane dekompresją zlib — terrain-followup.json) + 7 pól packedSize w indeksie BNT2 + 1 trafienie przecinające pola crc/nul wpisu 008700ac.tdf (@+10 w 16-bajtowym zestawie pól indeksu). **Żadne nie jest referencją template'u 4508.** Źródła: terrain-followup.json (audyt) + adjudykacja PE-MASTER.

### Pozycje G (wykonanie):

- **G1 manifest:** `02_EVIDENCE\MANIFEST_SHA256.csv` — wszystkie pliki ERRATA + wszystkie pliki R1 (manifest nie zawiera własnego hasha — precedens L12); re-hash weryfikacyjny: bramka G4 (patrz §9).
- **G2 rawscan:** `00_CONTROL\rawscan.py` — niezależny generator odtwarzający `R1 03_SEARCH\RAWSCAN_CORRECT_HITS.json` CO DO OFFSETÓW (wzorce u32LE przez struct.pack z asercją konwersji odwrotnej PRZED użyciem + ASCII); wynik: `02_EVIDENCE\RAWSCAN_REPRO.json` (8/8 serii identycznych).
- **G3 handoff:** `03_REPORT\HANDOFF.md` + `03_REPORT\artifact_index.csv`.
- **G4 manifest re-hash:** skrypt `00_CONTROL\make_manifest.py` + weryfikacja niezależnym przebiegiem.
- **G5 review persisted:** `03_REPORT\PE_MASTER_REVIEW.md` (verbatim blok PE_MASTER_REVIEW_DO_PERSIST z kontraktu erraty).

---

## 8. CO POZOSTAJE BEZ ZMIAN (rdzeń podwójnie potwierdzony: PE-MASTER + audyt zewnętrzny)

- **Tożsamość:** Models.bnt C950A8C2…; wpis 296445.nif @57,936,887/108,876 B; CRC wpisu == crc32(payload) == 0xCFAC1D3B; payload SHA 656795d8…; RAW.
- **Byte-identity modelu:** Models.ark (CD-2003) / BNT_Models (pośrednia) / pcg 9.3.5 — 3× identyczny SHA; BVI 296446 (993,420/760 B/7fee519b…) byte-identical między erami; wolumeny LOKALNE (−25/+25, 10.0, 20.0, 0.3, 10.3).
- **Pełna mapa NIF:** 155 bloków, 49+2795+106024+8=108,876 (0 niezaliczonych), census, 2415/1030, stopka [1][0], root=identity, 0 sierot, ogony Ark 35/41/0×7; stringi 107/9/9/5; anim 83 B.
- **Łańcuch definicji:** template 4508 @96,496 (id, hash 0xAFF5797C, A=296445@+0x14, B=296446@+0x18, C=0, PARAM=124.941f) — byte-identical z korpusem VFS klienta pośredniego (@0x17914); kategoria 201→477→4751→4508 (krawędzie @46,264/×200/@42,252); binding 26/26 Mesh_* w 4508.obj.dec == 26 nazw tekstur modelu (4752: 25; 2249: 23).
- **Negatyw placementu (BOUNDOWANY):** NOT_FOUND_IN_SEARCHED_SCOPE — pełny skan pcg/Data 1,818 plików (2,384,417,861 B; LE run + BE audytor: 0 trafień BE 296445/296446), terrain po dekompresji 58,451 kafli + 124 fałszywe markery (281,048,075 B; 0 trafień LE+BE), Strings indeksy 0, wszystkie BNT RAW poza terrain. NIE przeszukane: payloady Strings (szyfrowanie), wnętrza BIK/WAV/DDS, .prt, pola UNKNOWN.
- **Retrakcja wzorca §7 R1** (FD 85 04 00) pozostaje ważna; jej nauczka (asercja konwersji odwrotnej) wbudowana w rawscan.py erraty.

## 9. BRAMKI ZBIORCZO (fail-closed)

| Bramka | Treść | Wynik |
|---|---|---|
| G1 transform-recompute | 14/30 zmienionych + 16 identycznych; bbox ±2500/±2500/[~0,15620] (tol 1e-4); glowsak exact; krzyżowo vs probe.json 14/14 | **PASS** (assert w analyze_tree_v2.py; wyniki w 02_EVIDENCE\G1_GATE_RESULTS.json) |
| G2 rawscan-reproduction | zbiory (plik,offset) == RAWSCAN_CORRECT_HITS.json per seria | **PASS** (8/8 serii identycznych; 1,818 plików / 2,384,417,861 B; 02_EVIDENCE\G2_GATE_RESULTS.json) |
| G3 census fraz | poprawione frazy obecne (1×/z liczbami); zakazane NIEOBECNE | **PASS** (17 zakazanych ×0 wystąpień; 12 required-once ×1; 16 present z liczbami; 02_EVIDENCE\G3_GATE_RESULTS.json) |
| G4 manifest kompletny i zgodny | wszystkie pliki ERRATA+R1 w manifeście; re-hash niezależny = 0 MISMATCH | **PASS** (patrz 02_EVIDENCE\G4_GATE_RESULTS.json) |
| G5 git path-census + push + HEAD==origin | committed paths == lista dozwolona; push; HEAD==origin/master | **PASS** (patrz §11 i 03_REPORT\HANDOFF.md) |
| G6 entrypoint row-survival | dokładnie nowy wiersz; stary census wierszy nienaruszony | **PASS** (patrz §11) |
| G7 R1 immutable | hashe 18 plików R1 przed/po identyczne | **PASS** (baseline zapisany przed startem; porównanie końcowe w 02_EVIDENCE\G7_GATE_RESULTS.json) |

**NON_PASS_CLASSES:** żadna nie wystąpiła (GATE_FAIL/SCOPE_CREEP/HASH_MISMATCH/REPO_DIRTY_CONFLICT — zero).
**HARD_STOPS:** żaden nie został naruszony (R1 nietykalny; oryginały gry/silnika READ-ONLY; payloady LOCAL-ONLY; experiments/ nietknięte; brak pod-agentów; brak nowych twierdzeń poza listą korekt).

## 10. UWAGI WYKONAWCZE (jawność procesu)

1. **Bramka G2 złapała błąd własnego instrumentu erraty:** pierwsze wykonanie rawscan.py zawiodło (seria u32:296445 — 1 trafienie z serii ASCII zamiast 3 z serii u32) z powodu nadpisania wzorca u32LE bajtami ASCII przy scalaniu słowników o identycznym kluczu „296445". Błąd naprawiony (rozłączne klucze wewnętrzne), skan powtórzony: PASS. Wynik pośredni niezgodny NIE został nigdzie zapisany jako poprawny.
2. **Bramka G3 złapała 4 cytatowe powtórzenia fraz zakazanych** w markerach korekt raportu poprawionego — usunięte z raportu poprawionego (cytaty zastępowanych twierdzeń wyłącznie tutaj, w ERRATA.md, w sekcjach korekt).
3. **Rozbieżność kontraktu vs fizyki (F9):** kontrakt lokalizował mojibake '?' „w wierszu Portals"; fizycznie mojibake znajdował się w wierszu terrain (§5: „marker?w", „wpis?w ? 2", „s? zamienne"), a w wierszu Portals była zduplikowana fraza. Oba poprawione; rozbieżność udokumentowana.
4. **Rozbieżność mianownika (grupa C):** kontrakt podawał „pozostałych 1,932"; poprawna liczba plików bez trafień = 1,933 (1,936 − 3 pliki). Zweryfikowane niezależnym skanem.

## 11. PUBLIKACJA

- Repo: `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean` (BASE_SHA 2acf46258281be4b471788812501d146f592c235; dirty pre-work: wyłącznie `?? experiments/` — POZA ZAKRESEM, nietknięte).
- Commit path-limited: `docs/audits/PE_296445_NIF_ORIGIN_PLACEMENT_R1_ERRATA_R1_20260912/` (ERRATA.md + 01_CORRECTED + MANIFEST_SHA256.csv + skrypty + PE_MASTER_REVIEW.md + HANDOFF.md + artifact_index.csv; metadane tożsamości zamiast payloadów) + nowy wiersz AUDIT_ENTRYPOINT.md (R1+ERRATA w jednym wierszu; zero usuniętych wierszy).
- Lokal-ONLY (bez commitu): oryginalne payloadi (296445.nif, 296446.bvi — w R1 01_RAW), RAWSCAN_REPRO.json i wyniki bramek (02_EVIDENCE — hashe w manifeście), experiments/, pliki runu R1.
- Commit SHA + push status: patrz 03_REPORT\HANDOFF.md (komórka commit AUDIT_ENTRYPOINT wskazuje `git log -1` — plik nie może sam zawierać swojego SHA).
