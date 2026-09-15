WORK-AUDIT PLAYBOOK — audyt-auditor-md-flow-20260914 — DRUGA GLEBOKA LEKTURA D:\auditor.md
(Plik audytora, nie czesc pracy wykonawcow. ASCII-only dla czystosci kodowania.)

CEL: operacyjna destylacja METODY ChatGPT-Desktop-audytora (EU935), do ponownego uzycia
przez mnie (Work-Audit) i jako wzorzec dla promptow usera do opencode.
Druga lektura: celowane ponowne czytanie sekcji nosnych L4940-5060, L7205-7305, L11798-11827,
L12904-12924, L13495-13518, L14670-14714, L15500-15620, L17542-17620, L17659-17801.

== A. SEKWENCJA AUDYTU (zaobserwowana, powtarzalna w ~12 iteracjach) ==
A1. Przeczytaj raport w calosci; wyciagnij kazde twierdzenie (liczby, "all", "zero", "never").
A2. git status / log / diff — zakres deklarowany vs rzeczywisty (zlapano: importer/nif/ vs importer/).
A3. Kopiuj projekt do wlasnego katalogu (robocopy /XD .git .local) — NIGDY na oryginale.
A4. FULL_READ kodu nosnego (loguj: plik, linie, PEŁNA/czesciowa).
A5. Re-execucja: npm test, parse-all NA KOPII; logi do wlasnego katalogu.
A6. Wlasne sondy .mjs: corpus-check, shader-probe, renderer-check, late-slot-probe, probe.mjs.
A7. Serwer wykonawcy TYLKO odczytem (GET 200, API total); nigdy restart/mutacja.
A8. UI przez cua_repl: AX state, playwright.evaluate (geometria DOM, liczniki), dev.logs
    (bledy konsoli WebGL!), screenshot, viewport 1500x950 + reset, scroll do 5596/5596.
A9. KONTRPROBY NEGATYWNE (serce metody):
    - NaN injection (0x7fc00000) -> bramka musi FAIL (exit 5), nie PASS z bledem 0
    - wyzerowane normalne -> musi FAIL z coverage-raportem (0/392 porownan = PASS = defekt)
    - zepsuty URL (/eu935/%) -> serwer ma zyc (P1: crash + exit 1)
    - Fetch.failRequest / serwer odcinajacy body -> resolves-with-error, 0 unhandled rejections
    - MIDFETCH: zmiana modelu przy 144/185 pending -> model B czysty, 0 bledow konsoli
    - ON->OFF->ON -> state-diff przed/po musi byc 0 roznic
    - wywolania po clearModel -> 0 mutacji osieroconych materialow (55->0)
    - kontrola negatywna ID (999999999 nie istnieje) przy joinach
A10. Cross-check z era-source: Gb12_Source .cpp/.inl z plikami/liniami przy kazdym twierdzeniu
     o semantyce (NiAlphaProperty.h bity, NiSkinInstance_Win32.cpp Deform, NiTextureTransform
     MAX_TRANSFORM, NiFlipController fAccumTime, NiNode::AttachChild refcount-pattern).
A11. AUDYT.md: finding -> lokalizacja -> reprodukcja -> wplyw -> co dokladnie poprawic
     (NIE poprawiam sam) + link dla usera.
A12. Dopiero potem PROMPT dla wykonawcy.

== B. TAKSONOMIA DEFEKTOW, KTORYCH SZUKA (10 klas, z instancjami) ==
D1. Bramka slabsza niz etykieta: bit 0x2 vs 0x0200 (1744 wlasciwosci/1194 plikow);
    NaN>x=false -> maxima 0 -> PASS; 0/392 porownan -> PASS; numSources=1.5 przechodzi.
D2. Zielone testy nie obejmuja scenariusza: DARK+DETAIL (redefinition GLSL, 10 meshow/6 plikow
    przy 202/202); OFF->ON mid-fetch; kombinacje slotow.
D3. Raport != kod != git: "0 odniesien w skryptach" falsz (296445+296446 w 4508.obj.dec);
    "diff = 0 linii importer/" prawda tylko dla importer/nif/.
D4. Pomieszanie er: dowod FUN_005977b0 z PE2/2003 przypisany EU 9.3.5; DVD 2008 = klient
    9.1.5.0 (inne hashe archiwow) — era identyfikowana po SHA, nie po nazwie/data.
D5. Wykrywanie wyciekow stanu: klony tekstur 602 po 600 klatkach; stale bounds po deformie;
    wireframe state vs materialy; 55/57 osieroconych materialow mutowanych po clearModel.
D6. Zmiana pikselowa != wiernosc silnikowi: pixel-proof = zmiana obrazu; wlasny GPU-probe
    z diagnostyczna tekstura UV (20417/147456 px) dowodzi bledu orientacji mimo zielonych bramek.
D7. Census misclassification: rotacja lokalna vs swiata (45/42/71 mimo "0"); wlasciciel
    effect-list != rodzic children-list; SHORT 2562 != G3C 308; pole D "selektor" czyta +8 nie +0x10.
D8. Proweniencja receivera: ArkObjectClass przekazuje samego siebie — odczyt +0x08 nie jest
    polem A z templates.vfs; transformacja drzewa atrybutow != jedyny kanal.
D9. Za mocne wnioski negatywne: "FILE wykluczony" z braku surowych wzorow (identyfikatory moze
    dodaje kod); "0 STATIC_WORLD" nie wyklucza generic machinery; brak 20006.vfs nie jest
    anomalia bez dowodu konstruowania takiej nazwy.
D10. Framing negatywow: NOT_FOUND_IN_SEARCHED_SCOPE zamiast "nie istnieje"; UNKNOWN jawne;
     "nie ustalono w opisanym zakresie" + wskazanie gdzie urywa sie przeplyw danych.

== C. SZABLlon PROMPTU (dokladne frazy, ktore dzialaja) ==
C1. GO: "Masz moje GO na ... Nie zatrzymuj sie na planie ani prosbie o kolejne potwierdzenie."
C2. Kotwice: repo + "Ostatni zweryfikowany commit: X" + sciezki do AUDYT.md + "Przeczytaj w calosci"
    + "Sprawdz aktualny HEAD; nie zakladaj, ze nadal jest taki sam; zachowaj cudze zmiany."
C3. Findings z reprodukcja: plik:linia, wzor, liczba, wynik sondy, lista dotknietych plikow.
C4. Wymogi weryfikacji: "Odtworz probe przed naprawa" / "wlasne wykonania pozytywne i negatywne"
    / "rzeczywista kompilacja i linkowanie WebGL; same defines nie wystarczaja"
    / "pixel-proof to dowod zmiany obrazu, nie wiernosci silnikowi"
    / "roznica miedzy analiza statyczna a obserwowanym wykonaniem".
C5. Granice: READ-ONLY oryginale; nie ruszac src/game/ ani experiments/; nie startowac innych
    etapow; nie zmieniac oracle dla PASS; nie restartowac portow 8000/9350.
C6. Anty-rubber-stamp: "Nie wydawaj MASTER_ACCEPTED wylacznie na podstawie zielonej baterii.
    Werdykt musi odpowiadac faktycznie sprawdzonemu zakresu." / "Dobry, odtwarzalny wynik
    negatywny jest poprawnym wynikiem rundy."
C7. Atrybucja: "Rozniaj wykonania executora, audytora i Desktop. Nie opisuj ich jako trzech
    niezaleznych wykonan WebGL, jesli tylko executor uruchomil bramke."
C8. Publikacja: commit+push kazdej rundy (tez PARTIAL/NOT_FOUND); weryfikacja SHA na origin;
    manifesty; nie publikowac archiwow gry/exe.
C9. Supersession: "Ten prompt zastepuje poprzednie zlecenie. Zachowaj wykonana prace."
C10. Hipotezy bez zwyciezcy: H1 LOCAL / H2 LOCAL_DERIVED / H3 NETWORK / H4 HYBRID —
    "o kierunku decyduja bajty, przeplyw danych i odtwarzalne obserwacje".

== D. KULTURA SAMOKOREKTY (wystapienia z pliku) ==
- "moja poprzednia odpowiedz byla za szeroka" (heightmap kontekst)
- przyjecie korekty wlasnego raportu: 004C478A nie 004C4789
- zamiana "urywa sie przed dekoderem strumienia sieciowego" -> "nie ustalono producenta
  danych instancji; pochodzenie lokalne/sieciowe/mieszane nierozstrzygniete"
- executor: wlasna retrakcja endian-pattern (45 88 04 00 -> FD 85 04 00) zlapana przez
  sprzecznosc z rejestrem kanonicznym — i dopiero WTADY template 4508 znaleziony
- lekcje executora L1-L4 + L10 (same-engine blind spot) po adjudykacjach audytora

== E. STAN GRANICY BADANIA (na koniec pliku) — fakty, nie narracja ==
- CONFIRMED: templates.vfs (5438 rekordow/0 CRC-fail) -> A -> obj+0x08 -> getter -> request
  {typ 0x66=MODEL, id=A} -> "<A>.nif" (296445; negatyw 999999999; B=296446.bvi dwukierunkowo czysto)
- CONFIRMED: dostawca korekty Z = MaTerrainManagerRuntime (wlasne RTTI, vtable 0x00A7F430/420;
  cell_id 16:16 -> tag 0x6E -> sample/interpolacja -> FCHS; fallbacki 0.0/0.0/10.0/-1000.0;
  z'=max-ordered(z,h) w CREATE {3..7} i EXISTING bez bramki; drop-to-ground <=100x0.1)
- CONFIRMED: pozycja poprawiona -> instance +0x44..0x4C -> VALUE-COPY (FUN_005094C0) ->
  SceneFeederObject +0xC0
- NOT_DEMONSTRATED: SceneFeederObject -> wezel sceny -> model (brakujace ogniwo)
- OPEN: czy kanal obsluguje budynek 4508/296445; D@4508=124.941; format komorek terenu
- NIEODZYSKANE: historyczne wspolrzedne budynkow
- NEXT_EXPERIMENT (RUN C2): dekod slotow vtable 0x00A7D458 (0050A460/005090A0/B0/0050A050/
  005090C0/00509580) pod katem konsumenta SF+0x34..0x3C i lacza SF+0x30 (obiekt 0x118) z
  systemem modeli; bramki: GA census slotow, GB dataflow, GC kontrola pozytywna
  (znana krawedz SF+0x30->FUN_007B6A80); test rozrozniajacy: slot konsumuje SF+0x34 i
  przekazuje do wezla -> transform->model domkniety JEDNYM lancuchem; nie -> model
  wylacznie kanalem atrybut-drzewa (pump 0x66) i NOT_DEMONSTRATED zostaje.

== F. BLEDY MOJE (audytora-audytora) Z PIERWSZEGO PRZEJSCIA, SKORYGOWANE ==
- brak korekty; druga lektura potwierdzila wszystkie liczby. Dodano precyzje: mechanika
  fallbackow terenu, bramka rozrozniajaca C2, rozwiazania tropow (4751x301 = 150x2+self;
  4508x18 = 10 dlugosci+7 rozmiarow+1 przypadek), DVD=9.1.5.0.