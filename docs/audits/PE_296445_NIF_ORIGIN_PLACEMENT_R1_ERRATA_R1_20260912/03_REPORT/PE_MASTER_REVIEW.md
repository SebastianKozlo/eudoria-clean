# PE_MASTER_REVIEW — PE_296445_NIF_ORIGIN_PLACEMENT_R1_20260912 (REWIZJA po audycie zewnętrznym)
VERDICT: MASTER_PARTIAL_PASS (advisory; PROVISIONAL_UNTIL_QUALIFIED; CANONICAL_GATE_EFFECT=NONE)
DATA: 2026-09-12. Auditor: PE-MASTER. Adjudykacja zewnętrznego audytu cross-engine (C:\Users\User\Documents\ChatGPT\PE\audit-296445-placement-r1\AUDYT.md): 7/7 ustaleń ACCEPTED (0 odrzuconych), każde zweryfikowane niezależnie przez PE-MASTER z fizycznych bajtów.

## POTWIERDZONE BEZ ZMIAN (podwójnie: PE-MASTER + audyt zewnętrzny)
- Tożsamość: Models.bnt C950A8C2…; wpis 296445.nif @57,936,887/108,876 B; CRC wpisu == crc32(payload) == 0xCFAC1D3B; payload SHA 656795d8…; RAW.
- Byte-identity modelu: Models.ark (CD-2003) / BNT_Models (pośrednia) / pcg 9.3.5 — 3× identyczny SHA. BVI 296446 (993,420/760 B/7fee519b…) byte-identical między erami; wolumeny LOKALNE (−25/+25, 10.0, 20.0, 0.3, 10.3).
- Pełna mapa NIF: 155 bloków, 49+2795+106024+8=108,876 (0 niezaliczonych), census, 2415/1030, stopka [1][0], root=identity, 0 sierot, ogony Ark 35/41/0×7; stringi 107/9/9/5; anim 83 B.
- Łańcuch definicji: template 4508 @96,496 (id, hash 0xAFF5797C, A=296445@+0x14, B=296446@+0x18, C=0, PARAM=124.941f) — byte-identical z korpusem VFS klienta pośredniego (@0x17914); kategoria 201→477→4751→4508 (krawędzie @46,264/×200/@42,252); binding 26/26 Mesh_* w 4508.obj.dec == 26 nazw tekstur modelu (4752: 25; 2249: 23).
- Negatyw placementu (BOUNDOWANY): NOT_FOUND_IN_SEARCHED_SCOPE — pełny skan pcg/Data 1,818 plików (2,384,417,861 B; LE przez run + BE przez audytora: 0 trafień BE 296445/296446), terrain po dekompresji 58,451 kafli + 124 fałszywe markery (281,048,075 B; 0 trafień 296445/126740 LE+BE), skrypty 1,936 (wyłącznie własne ID w 4508/4752/2249.obj.dec), Strings indeksy 0, wszystkie BNT RAW poza terrain (kompletność zmierzona). NIE przeszukane: payloady Strings (szyfrowanie), wnętrza BIK/WAV/DDS, .prt, pola UNKNOWN.

## SKORYGOWANE (errata R1 wykonuje)
1. [P1] ERA-MIXING: FUN_005977b0/vtable[0x50]/0x1C/@+0x2c..0x34 = PE2_unpacked_out.exe (2003; SHA 56178993692A7409…) — raport przypisał je EU 9.3.5 (E7785430…). Mechanizm pozycji w 9.3.5: UNVERIFIED (hipoteza transferu). Etykieta „VFS 2003" → VFS klienta pośredniego (ArkVFS02 = NOT-IN-PE2 per kanon TEMPLATE_READER).
2. [P2] TRANSFORMACJE: analyze_tree.py pomija własną transformację mesha (world[i]=cur). Poprawne: 14/30 meshy zmienionych; bbox sceny = (-2500,-2500,~-1.27e-08)..(2500,2500,15620) ≈ 5000×5000×15620 j.m. (podwójnie: rekomputacja PE-MASTER == probe.json audytu, identyczna epsilon). Ogon importera == surowe ekstrema z różnych układów lokalnych, NIE bbox sceny; 7. float UNKNOWN.
3. [P1] „0 odniesień do 296445 w skryptach" FAŁSZYWY: 4508.obj.dec 296445@664, 296446@580; 4752 126740@520; 2249 278453@664 (wzmocnienie definicji, nie placement).
4. [P2] GLOBALNY NEGATYW nagłówka + „wyłącznie serwer" WYCOFANE na NOT_FOUND_IN_SEARCHED_SCOPE; ścieżka sieciowa PE2 ≠ wyłączność w 9.3.5.
5. [P3] Arytmetyka 9 B: [u8@0][u32 -1 @1..4][u32 ID @5..8] (bajt @8 = MSB ID); „atlas/flipbook" = hipoteza; 27×-1 dzieci korzenia; EnvZones 126 (84+42); LoadTopLevelObjects L362; Portals zakres 382,811–592,741; Parameters 27; TextureEffect dual-relation (62 rodzic grafu / 59 effects-owner); „warianty slum" usunięte.
6. Tropy rozstrzygnięte (podwójnie): 4751×301 = pola nagłówkowe (150×[8,60] + self@4); 4508×18 terrain = 10 dsize-declen-4508 + 7 packedSize + 1 crc/nul-crossing (008700ac.tdf) — żadne nie jest referencją template'u.

## SAMO-KOREKTY PE-MASTER (głośno)
- Moje C3 „world-bbox EXACT" było fałszywym potwierdzeniem przez wspólny bug konwencji (niezależny kod, wspólna lineage założeń — QH-009).
- Moje C8 zweryfikowało zgodność cytatu z kanonem, ale nie erę binarium kanonu; odziedziczyłem „VFS 2003".
- Mój pierwotny NEXT_EXPERIMENT miał wadę V2R-007 (ścieżka „%d.nif" wpisana w bramkę) — poprawiony na resolver-agnostyczny.

## NASTĘPNY P0 (osobny run po errata-QC)
PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912: ślad konsumenta w Entropia.exe 9.3.5 (SHA E7785430…; własna weryfikacja SHA/image-base/VA-mapping PRZED użyciem adresów; zakaz transferu adresów PE2): rekord 4508 (A@+0x14) → FAKTYCZNY resolver zasobu (ścieżka/ID/tabela — nie zakładaj formatu) → model → utworzenie instancji → ŹRÓDŁO transformacji → rejestracja sceny; A/B/C oddzielnie; negative control: wrong-ID (sibling 4752/2249); NON-PASS: CHAIN_ABSENT/ARG_FROM_OTHER_FIELD/INDIRECT_ONLY/TOOL_BLOCKED; wyniki podzielone A(tożsamość)/B(loader)/C(źródło transformacji)/D(lokalizacja — jeśli odzyskana). PE2-chain (".nif" @0x610368→0x00520EE0→FUN_00522010 per kanon TEMPLATE_READER) = WZORZEC WYSZUKIWANIA dla analogu, nie transfer. Poszukiwanie placementu pozostaje OTWARTE.
