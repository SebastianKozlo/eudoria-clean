# REPORT — PE2003 ISO 5.1: ARCHIWA -> ZASÓB -> INSTANCJA -> POŁOŻENIE (kampania statyczna R4)

RUN_ID: PE2003_ISO_ARCHIVE_RESOURCE_INSTANCE_PLACEMENT_STATIC_R4_20261025
Tryb: 100% statyczny i plikowy. Bez wykonania gry/instalatora/loadera/patchera/Fridy/renderera/sieci do serwerów MindArk.

## Werdykt kampanii

SCIENCE_VERDICT = PARTIAL_PASS_MATERIAL_ADVANCE. Łańcuch ISO->archiwum->zasób->instancja->transform jest domknięty strukturalnie na poziomie bezprecedensowym (topologia CONFIRMED z VA na każdym ogniwie); pochodzenie wartości transform (ostatnie ogniwo) pozostaje UNVERIFIED z udokumentowanym poziomem blokady (indirect vtable dispatch). Historyczne położenie obu budynków NIE zostało odzyskane. PE2003_WORLD_XYZ_RECOVERED=NO; PE2003_HISTORICAL_PLACEMENT=NOT_ESTABLISHED.

## Co wykonano (8 natywnych Task, depth1, max2, wszystkie delivered, attempt 1 kazdy)

- M01: faktyczny consumer manifestów (Download.data/Install.data/ClientFiles.txt/UpdateFiles.txt) + pełny łańcuch jednostki danych w ClientLoader 5.1.0.0.
- L01: provenance-aware inwentaryzacja lokalnych archiwów + poszukiwanie obu modeli (z korektą C01 po QC1).
- J01: zasób->instancja->transform w kliencie 5.1.0.0 (lookup .nif, ROOT, fabryka, writer, sinki).
- N01: naprawa parsera NIF end-to-end (kwalifikator skali, boundary NiTriShape, propagacja FAIL).
- J02: źródło wartości transform (mapa typów rekordów, census callerów fabryki, template-record producer, renderer-side sink).
- QC1: rolling QC (10 findings, w tym P1: fałszywa negatywna kontrola EU w L01).
- C01: bounded corrections L01/M01/J01 + obowiązkowa rewalidacja EU.
- QC2: final QC (RUN_ACCEPTED z errata; 4 errata P3 dokumentacyjne przyjęte verbatim do seal).

## Łańcuch A: ISO -> jednostka danych -> archiwum (CONFIRMED topologia)

ClientLoader 5.1.0.0 czyta ClientFiles.txt (6 open sites) i Install.data (binarne 8B rekordy stanu; reader 0x417BB0, rewriter 0x417F20); UpdateFiles.txt pobiera z FTP jako jednostkę type 2. Jednostki danych mają nazwy budowane sprintf: FullDat_%d.ark, Dat%d_%d.ark, Lang_%u.ark, ValidFiles.ark, minipatch; folder Data\. Already-installed to potrójny check (rekordy Install.data + skan lokalnych ark 0x415DD0 + weryfikator 0x41F370 — tam są kotwice R3 Models\/Models.ark: etap VERIFY, nie ekstrakcja). Download po porównaniu wersji (próg 0x2A); walidacja CheckForCorruptFiles + zlib 1.1.4 + ValidFiles.ark; ekstraktor 0x41D400..0x41E700 ze stagingiem tempfile.ark (parser BUNT); dest: Models\Models.ark, Textures\, Volumes\, Scripts\; rename .patch.tmp/*.dlltmp; montaż: HKLM Software\MindArk\Project Entropia + PE.exe montuje fixed-name archiwa (models.ark@0x6B1320->0x45ED7D; client BUNT parser 0x6B8EE4; member-open 0x59E2D0 klucz=lowercased filename).

**Pobór kluczowy:** Download.data ("1 PE_PCG.ark") NIE MA konsumenta w przypiętym korpusie (pełny census ASCII+UTF16LE trzech obrazów; niezależnie potwierdzone przez QC1 i re-run scan_utf16.py). Consumer pozostaje UNVERIFIED (poza korpusem); hipotezy: starsza generacja ClientLoadera / UpdateFiles.txt serwera / komponent nie-wydany. ClientLoader 5.1.0.0 implementuje schemat wersyjny FullDat/Dat, nie PE_PCG.

ARCHIVE_PRODUCER_CERTIFICATE: patrz jobs/M01/data/ARCHIVE_PRODUCER_CERTIFICATE.json (12 claimów z przesłankami/kontrmodelami/granicami).

## Łańcuch B: lokalne archiwa (scoped)

PE_PCG.ark / FullDat*.ark / Dat*.ark / jednostki ClientFiles.txt: NIE istnieją na lokalnym dysku (scoped negative z jawnym denominatorem; LOCAL_SOURCE_EXHAUSTED=NO — nieprzeszukane m.in. D:/Entropia Universe, Program Files/MindArk*, D:/PE_Terrain).

- **296445.nif** (wariant 2003, NIF 4.1.0.12, SHA 656795D8...): byte-identical w CZTERECH korpusach — COT Jan 2003 Models.ark, pcg_install Models.bnt, pcg915 Models.bnt, **EU 2008 Models.bnt** (korekta C01 po wykryciu fałszywego negative przez QC1; rewalidacja niezależną ekstrakcją SHA MATCH).
- **218757.nif**: wariant 2003 (SHA C13D0873...) **wyłącznie w COT ark**; wariant późniejszy (GB 10.1.0.0, 3E8A22C2...) w pcg_install/pcg915/EU2008. Późniejszy wariant nie zastępuje 2003.
- templates.vfs (ArkVFS02, era UNKNOWN) referuje oba ID.

Warianty 2003 są eralabel: to NIE są warianty przypięte do wydania ISO 5.1.0.0 (jego jednostka modelowa PE_PCG.ark jest nieobecna lokalnie).

## Łańcuch C: zasób -> instancja -> transformacja (build 5.1.0.0)

Lookup: klucz = nazwa pliku .nif; loader class 0x42E920 (vtable 0x65BA0C); open-by-name 0x423280 -> ROOT template cached (konsument 0x40F020, out-slot this+0x34). Instancja: fabryka 0x4578E0 (alloc 0x100B, ctor 0x46E870, vtable 0x65C060; natychmiast vtable+0x1C z 6 arg x,y,z,rx,ry,rz). Join root<->instancja: [entity+0x40] idx -> 0x457980 -> [mgr+0x8c] TLO -> [TLO+0x20] SUB -> 0x45DE20(SUB,idx)=record 0x5C -> 0x473E90 -> SFO 0x7B ([sfo+0x78]=record; 'SceneFeeder' RTTI). Writer: 0x46E990 (pos 0x46EB20, rot 0x46EC00); sinki 0x46F0A0 (translate x100; const 0x65B648=0x42C80000=100.0f), 0x46F0C0 (Euler->mat), 0x46F160 (scale). Kontrmodele bbox/debug/physics/camera/model-local odrzucone bajtowo.

**Źródło wartości:** producent template-records (init-set) = LOKALNY KOD (0x45D5F0) — CONFIRMED w scope init-set. Proveniencja 6 argumentów fabryki i entry-set producenta: UNVERIFIED — 0 bezpośrednich xrefów fabryki, jedyna vtable 0x65BE9C slot+0, argumenty przez indirect dispatch; QC2 sprawdził kontrmodel "entry z pliku" (22 writery, 182 strony dispatch) i odrzucił statyczną atrybucję. Renderer-side sink 0x4DD421 (receiver [renderer+0x28], push [rec+0x2c]/[rec+0x14]/[rec+0x30] -> vtable+0x11C) — sink CONFIRMED, receiver identity UNVERIFIED. Rozstrzygnięcie wymaga dynamic trace (poza zakresem kampanii statycznej).

## N01 (narzędzie)

Parser v2 (tools/nif_transform_parser_v2.py, SHA B71C209B...): FIX-1 kwalifikacja floatowa skali (1.0f nigdy nonunity), FIX-2 boundary wszystkich typów w tym NiTriShape, FIX-3 propagacja FAIL/BLOCKED. 51/51 przypadków kontrolnych PASS (anchor +1B -> FAILBOUNDARY); regeneracja end-to-end **byte-identical z R3** na obu NIF bez ręcznych poprawek; nonunity_scale=0 z generatora.

## Korekty R3 (CORRECTION_DISPOSITION: R3-A01..A12 -> patrz CORRECTION_DISPOSITION.md)

Zachowane: payload recovery, 82 transformacje, build identity, census. Skorygowane: SERVER_DELIVERED_ONLY obnizone (A01 — potwierdzone: PE_PCG.ark bez konsumenta w korpusie, ale capabilityFTP nadal nie dowodzi zawartości); 0x413B97 doprecyzowane (A02 — plus rozróżnienie verify 0x41F370 vs extract 0x41D4xx); census 56/54 jawne (A03); MP3->PE42 (A04); parser end-to-end naprawiony (A05/A06 — N01 PASS); CSV/strict (A07); LENGTH/atrybucja (A08); LOWER_BOUND (A09 — brak w R4); NiTriShapeData 44 (A10); hash-pattern scoped (A11); zakres ISO (A12).

## Granice i uczciwość

- Statyka: pochodzenie wartości transform i identity [renderer+0x28] nierozstrzygalne bez dynamic trace (poza zakresem); Ghidra headless w J02: 4 zawieszone próby (udokumentowane, procesy terminowane); wyniki oparte na własnym disasm + weryfikacji bajtowej QC.
- Denominatory jawne (L01 DENOMINATOR.json); brak LOWER_BOUND_COMPLIANT; PARTIALLY_MEASURED/UNVERIFIED jawnie.
- Root wykonał re-hash wejść (ISO 884692A8..., PE.exe 46B687..., section1 D43A23B9..., ClientLoader E24B2377..., NIF-y 656795D8.../C13D0873..., EU Models.bnt 1322ADF2...) — wszystkie MATCH pinów; quiescence potwierdzona (brak java/locków).
- Peer: AUDIT_ENTRYPOINT/manifest LAST na końcu seal; publikacja sanitizowana (patrz PUBLICATION_RESULT w RECEIPT_ROOT).
