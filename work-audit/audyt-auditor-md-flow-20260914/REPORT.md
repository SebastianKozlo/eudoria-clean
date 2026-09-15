WORK-AUDIT REPORT — audyt-auditor-md-flow-20260914
PRZEDMIOT: D:\auditor.md (17849 linii) — eksport rozmowy ChatGPT/Codex Desktop pelniacego role niezalezego
audytora projektu Entropia Universe 9.3.5 (D:\Entropia_935_ThreeJS, pozniej eudoria-clean). Pelna lektura
1..EOF w 15 chunkach. Data audytu: 2026-09-14.

WERDYKT: POTWIERDZONY CZESCIOWO — flow i metodologia audytora sa spojne, skuteczne i samokorygujace;
NIE zweryfikowalem niezaleznie twierdzen technicznych zawartych w pliku (commity/SHA/testy) — przyjete z pliku.

== 1. REKONSTRUKCJA FLOW (petla pracy) ==
Uczestnicy: [Desktop-Codex] = audytor zewnetrzny; [OpenCode/PE-MASTER] = wykonawca+audytor wewnetrzny;
[user] = kurier pomiedzy AI + zrodlo GO; [GitHub] = trwale medium dowodowe (od polowy rozmowy).

Cykl (powtarzalny, ~12 iteracji w pliku):
 1. Wykonawca konczy etap (S1..S11B) -> raport PE_MASTER_REVIEW = MASTER_ACCEPTED.
 2. User wkleja raport do Desktop-audytora + "zrob audyt".
 3. Desktop: czyta raporty + kopiuje projekt (robocopy /XD .git .local) do wlasnego katalogu audytu
    C:\Users\User\Documents\ChatGPT\PE\audit-*; czyta kod + zrodla silnika (Gb12_Source) + oracles.
 4. Desktop: wlasne wykonania — npm test na kopii, parse-all, probe-serwera (tylko odczyt), UI przez
    cua_repl (AX state, playwright.evaluate, dev.logs, screenshoti), wlasne skrypty .mjs, kontrproby
    negatywne (NaN injection, zeroed normals, zepsuty URL %, MIDFETCH, OFF->ON wysscigi).
 5. Desktop znajduje defekty przez wzorzec: "zielone testy nie obejmuja scenariuszy, ktorych testy
    nie obejmuja" + "bramka slabsza niz etykieta" + "raport != kod != git".
 6. Desktop pisze AUDYT.md (wlasny katalog) + krotki raport userowi z linkiem.
 7. User: "napisz prompt" -> Desktop pisze PROMPT_OPENCODE (szczegoly nizej).
 8. User wkleja prompt do OpenCode -> wykonawca naprawia -> nowy raport -> wroc do 1.
 Od ~2026-09-13: kazda ronda = commit+push na GitHub (Desktop publikuje wlasne audyty i prompty;
 wykonal to m.in. commity 24d7669, e30f99f; weryfikuje blob-vs-manifest SHA z gita).

== 2. WYNIKI AUDYTOW DESKTOP (liczby z pliku; przyjete, nie rekomputowane) ==
- 79549d5: 4 defekty mimo MASTER_ACCEPTED "zero defektow" (P1 crash serwera przez URL %, P2 alpha
  0x2 vs 0x0200 w 1744 wlasciwosciach/1194 plikach, P2 kamera bez aspect-ratio 270/1186 wierzch.,
  P3 wireframe state).  Testy 41/41 przechodzily — defekty byly poza pokryciem.
- 15cd631 (S7+S8): 5xP2 (stale bounds po deformie, bramka NaN->PASS, REPLACE color leak, transfer
  reject, panel tnie ERRORY >12 pozycji). Wykonawca ACCEPTED_ALL + errata + lekcje L01-L04.
- 7ce1083 (S9): 5 napraw potwierdzonych + NOWY P2: walidator przepuszcza wyzerowane normalne
  (PASS przy 0/392 porownan kierunku) — wykryty przez wlasna sonde, nie przez suite wykonawcy.
- fa3f88b (S10): 2xP2 (shader DARK+DETAIL redefinition — WebGL VALIDATE_STATUS false na 512829.nif,
  10 meshow/6 plikow; walidator zeroed-normals) + errata liczb.  202/202 zielonych nie obejmuje kombinacji slotow.
- a19e31f (S10c): oba P2 potwierdzone naprawione wlasnymi probami (10/10 bez duplikatow; FAIL exit 5 z 392).
- 989f880 (S11A): naprawy late-slot OK, ale 2xP2 (orientacja Z-up->Y-up pominieta — 20417 px zmiany na
  teksturze kontrolnej; census myli rotacje lokalna ze swiatowa — 45 efektow/42 plikow/71 meshow mimo "0") + P3 NaN.
- 9969a81 (S11B): 2xP2 (kumuluja sie klony tekstur do 602 po 600 klatkach; podwojna rejestracja flipbooka
  OFF->ON mid-fetch) + 2xP3 (granice czasu f32 mismatch z silnikiem; walidacja przepuszcza frequency/phase/cycle).
- NiArk-census (vlastne przeliczenie 5596 NIF): 6 typow NiArk, 23260 blokow; bledy raportu wykonawcy
  (Importer 38 vs 41 bajtow odwrotnie, niflib v4 link!=Name, SHORT 2562!=G3C 308).
- 296445-placement R1: 3 powazne bledy wykonawcy — proweniencja er (fun_005977b0 z PE2/2003 przypisana
  do 9.3.5!), transformacje pomijajace wlasna transformacje mesha (14/30 zmienia wynik), "0 odniesien w
  skryptach" falszywe (296445+296446 w 4508.obj.dec). Desktop utrzymal poszukiwanie OTWARTE.
- static-placement 2a2ba8d: 5 materialnych (ArkObjectClass receiver != template A; "selektor D" czyta +8;
  brak surowych ID nie wyklucza FILE; 0 STATIC_WORLD nie wyklucza generic machinery; call-presence != exclusive provenance).
- origin-seam 78cd153: FUN_007343E0 nie tworzy "subkursora" (maska bitowa + ten sam kursor); pominienta
  korekta Z przed konstruktorem (FUN_00853A80); za mocne wykluczenie budynkow.
- position-construction 6465019: 3 poprawki (pola +0x88/+0x8C nie +0x78; slot vtable +0=0050A460 nie +4;
  wniosek negatywny != "wylacznie atrybuty"). Audyt przerwany usage-limit (punkt pojedynczej awarii).

== 3. ANATOMIA PROMPTOW (powtarzalny szablon Desktop->OpenCode) ==
Kazdy prompt zawiera: (a) GO bez pytania o pozwolenie; (b) repo + ostatni zweryfikowany commit + sciezki
do AUDYT.md i artefaktow; (c) materialy do przeczytania w calosci (FULL_READ_LOG); (d) zadania numerowane
z KONKRETNYMI reprodukcjami (plik:linia, wzor, wynik sledu, liczby); (e) wymagania weryfikacji: wlasne
wykonania pozytywne+negatywne, przed/po, WebGL compile+link+validate (nie tylko defines/draw-calls),
pixel-proof = zmiana obrazu NIE zgodnosc z silnikiem; (f) granice: READ-ONLY oryginale, nie ruszac
cudzych zmian (src/game/, experiments/), nie startowac innych etapow, nie wydawac MASTER_ACCEPTED z
zielonej baterii; (g) format raportu: twierdzenie->zrodlo->wlasny test->wynik->artefakt.
Ewolucja szablonu: od "napraw X" (S10) do pelnych zlecen badawczych z hipotezami H1-H4, bramkami
kategoryzacji konsumentow (STATIC_WORLD/AVATAR_EQUIPMENT/PREVIEW_UI/OTHER/UNKNOWN), rozdzieleniem
MECHANIZM vs DANE HISTORYCZNE, statusami CONFIRMED/SUPPORTED/HYPOTHESIS/UNKNOWN/NOT_FOUND_IN_SEARCHED_SCOPE.

== 4. OSTATNIE 10 PROMPTOW (sedno kazdego) ==
P1. L9348 (S10-naprawy): rozstrzygnij audyt, napraw 2xP2 (shader duplikacje GLSL na 10 podanych
    meshach; walidator jednostronnie zerowych normalnych — wymagane FAIL + coverage-report + negatywne
    testy trwale), errata liczb z artefaktow, zachowaj 5 napraw S9, nie odpalaj S11.
P2. L9473 (S11A-GO): utrwal odtwarzalnosc walidatora (vendoring+SHA256), zdefiniuj i wykonaj S11A —
    ENVIRONMENT: najpierw era-semantyka ze zrodel (nie zakladaj cubemapy!), potem implementacja,
    weryfikacja (kolejnosc pobran, ON->OFF->ON, mid-fetch, NaN), granice, pelny raport.
P3. L9578 (S11A-GO-v2): przyjmuje zamkniecie S10c; zastepuje P2; doprecyzowuje: SHA256 pin
    0FB2DDAC..., testy maja sprawdzac wersje kanoniczna, odtworzenie w izolowanym katalogu,
    good/zeroed/NaN/inverted/short-buffer; "nie opisuj trzech warstw jako trzech niezaleznych
    wykonaen WebGL, jesli tylko executor uruchomil bramke".
P4. L9741 (meta): wklej TYLKO najnowszy; jesli stary poszedl — preambula "zastepuje, zachowaj prace";
    ostrzezenie o escapowanych podkresleniach w sciezkach (skuteczne — user mial \_ w copy-paste).
P5. L12919 (S11B PROMPT_OPENCODE): naprawy P2 (klony stabilne, dedup rejestracji), P3 (f32 granice
    klatek wzgledem zrodel NiFlipController/NiStepFloatKey; walidacja frequency/phase/cycle) +
    kontynuacja: ustal pochodzenie FR441xx.TGA dla 7 nieobslugiwanych kontrolerow.
P6. L12982 (badanie swiata): sesja badawcza heightmapa/ziemia/roslinnosc/oswietlenie; WAŻNE:
    heightmapa JUZ ODZYSKANA — najpierw odnajdz artefakt i zweryfikuj wersje/obszar/skale; nie
    mieszaj wersji klienta; tabela element->plik->format->zrodlo->proba->status; nie zaczynaj renderer-a.
P7. L13113 (badanie v2 NiArk-first): od zrodel Gamebryo do struktur klienta; pelny rejestr KAZDEJ
    instancji NiArk (bez limitu "pierwsze 30"); priorytet: czy w NIF/NiArk zapisano LOKALIZACJE —
    klasyfikacja kandydatow (lokalna/NIF-scena/swiat-gry/UV/bind/projekcja/nierozstrzygnieta);
    "GLOBALNA W SCENIE NIF != GLOBALNA NA MAPIE"; wlasciciel effect-list != rodzic children-list.
P8. L14401 (296445.nif): pelna mapa 155 blokow + rozliczenie bajtowe; transformacje rozdzielone
    A(model)/B(korzen NIF)/C(swiat gry); silnik jako przewodnik (LoadBinary z plikami/liniami);
    odwrotne wyszukiwanie (296445 LE u32, pelne nazwy, templates.vfs); weryfikacja kandydata
    (rekord->instancja->model->XYZ/rot/scale); brak trafien = NOT_FOUND_IN_SEARCHED_SCOPE nie "nie ma".
P9. L14696 (po audycie placement-R1): korekty: era-separacja (fun z PE2 nie przenosi sie na 9.3.5),
    przeliczenie transformacji z wlasna transformacja mesha, skrypty zawieraja ID (0 odniesien =
    falsz), klasyfikacja tropow 4751x301/4508x18; nastepny krok: konsument template 4508 w 9.3.5.
P10. L15799 (NADRZEDNE UZUPELNIENIE): obowiazkowy commit+push kazdej rundy (tez PARTIAL/NOT_FOUND),
    nie zastepuj network-first zalozeniem client-only, priorytet: klasyfikacja konsumentow (25 call-site
    lookupu/13 callerow pumpu) zanim skany, skany z okreslonym pokryciem (INVENTORIED != przeszukany
    wewnatrz), bramki nie moga wymuszac odkrycia (historyczny holdout nie jest wymagany do uznania
    mechanizmu), rozdziel statyke od runtime, nie twierdz "wykonano" gdy przeczytano.
P11. L16132 (duze ZLECENIE): jedno dla sesji deep-think; 14 sekcji: cel (MECHANIZM vs DANE
    HISTORYCZNE), izolacja er (SHA E7785430...), materialy, potwierdzenie lancucha A->MODEL bez
    awansowania B->C/D->E, macierz weryfikacji zewnetrznych zrodel (world editor 2002, DAoC
    fixtures.csv, OpenMW/MWSE, MMO-sieciowe, EU10.4 templates.vfs, historia BNT/NiArk) —
    "odpowiedzi ChatGPT sa lista twierdzen do sprawdzenia, nie zrodlem prawdy", hipotezy H1-H4 bez
    zwyciezcy, P0 instancja budynku, polaczenie dwoch sladow, wlasne kontrole (round-trip, kontrola
    negatywna, holdout), granice, raport osobny per-warstwa, publikacja GitHub z weryfikacja SHA.
P12. L17604 (C1/C2): doprecyzowanie — tylko RUN C1 (korekty F1-F3 + trace 00853A80->provider->zrodlo),
    C2 (instancja->model) po kontroli C1; ERRATA_R5 wskaże zastapione twierdzenia; "nie zakladaj ze
    provider to terrain sampler" (deskryptor-neutralnosc).

== 5. FINDINGS (moje, o flow — nie o kodzie EU935) ==
[F1|P3] Kazdy audyt konczy sie usage-limitem lub przerwaniem w polowie (3x w pliku; audyt 6465019
  urwany). Wplyw: brak domkniecia weryfikacji wyniku dla usera; ryzyko pojedynczego punktu awarii.
  Rekomendacja: czas na domkniecie audytu przed startem, lub checkpoint.
[F2|P3] User jako kurier wkleja czasem zepsute sciezki (escaped underscores), zle pairingi promptow
  (chcial wkleic oba) — AI lapie i koryguje, ale to dodaje noise. Rekomendacja: numerowac wersje
  promptow (v1/v2) wprost w pierwszej linii.
[F3|P3] W pliku wystepuja POZATEMNICZE znaki (dziwny znak "ð" przy "kotwiczenie"?) — minimalne, bez
  wplywu na tresc.
[F4|P2|ZWERYFIKOWANE-Z-PLIKU] AI potrafi samo popelniac blad, ktory polowi: w L13395-13427 Desktop
  przedstawia korekte wlasnego sprzecznego wniosku ("moja poprzednia odpowiedz byla za szeroka")
  i w L14974-14997 prostuje propagande "serwer vs pliki" — to dowod samokorekty, ale tendencje oscylacji
  kierunku badania (server-delivered vs client-only) sterowanego zewnetrznymi opiniami (ChatGPT-web).
  Rekomendacja: trzymac H1-H4 otwarte (co zreszta samo wpisalo do promptow P10/P11).
[F5|P3] Dwa prompty (P2 vs P3, P6 vs P7, P10 vs P11) istnieja jako pary stara/nowa — bez versioning
  user musial pytac "ktory wkleic". AI rozwiazalo to meta-promptem P4; na przyszlosc: od razu
  zastepowac stary, nie dopuszczac do dwoch aktualnych.

== 6. POTWIERDZONE UCZCIWIE (mocne strony tego AI — wg wlasnych wykonan opisanych w pliku) ==
- Kazdy audyt = wlasna egzekucja na kopii (robocopy), nigdy na oryginale; oryginalne repo czyste po
  kazdym audycie (wielokrotnie sprawdzane git status w logu).
- Rozdziela atrybucje wykonan: "232/232 to nadal wyniki OpenCode — pelnego niezaleznego audytu ENV
  jeszcze nie wykonalem" — nie przypisuje sobie cudzych liczb.
- Kontrproba negatywna jako standard: NaN wstrzykniecie, zeroed normals, zepsuty URL, Fetch.failRequest,
  MIDFETCH, krótki bufor, kontrola negatywna do bramek numerycznych.
- Pixel-proof traktowany jako zmiana obrazu, nie zgodnosc z silnikiem; readback deterministyczny.
- Era-separacja bajtowa: zlapano wykonawce na przypisaniu dowodu z PE2/2003 do EU935; wymagania
  GATE-ERA wlasnych promptach.
- Statusy uczciwe: NOT_FOUND_IN_SEARCHED_SCOPE zamiast "nie istnieje"; UNKNOWN jawne; retrakcje
  wlasne publiczne ("przyjmuje korekte mojego raportu").
- Zamyka petle publikacja: wlasne audyty na GitHub (commit e30f99f weryfikowany blob-vs-manifest).

== 7. NIESPRAWDZONE ==
- Wszystkich twierdzen technicznych zawartych w pliku (SHA, liczby testow 41/41..282/282, commity
  d31b184..6465019) NIE rekomputowalem — poza zakresem tego zlecenia (audyt narracji/flow).
- Nie weryfikowalem linkow zewnetrznych (worthplaying, DAoC-repos, fora) — AI samo ich uzywalo
  z ostroznoscia, ja je tylko zanotowalem.
- Nie wchodzilem na zywy serwer 9350/8000 ani do repo EU935 (zlecenie bylo o analize pliku).

== 8. CO CZYTAM ==
- D:\auditor.md — FULL_READ 1..17849 (15 chunkow).
- Nic spoza pliku (poza własnymi notatkami).

== 9. KROKI PO CZLOWIEKU ==
1. Zachowac ten flow — jest skuteczny: kazdy audyt Desktopu znalazl realne defekty po mimo
   MASTER_ACCEPTED; wykonawca je ACCEPTED i implementowal lekcje (L01-L10).
2. Wprowadzic versioning promptow (v1/v2 + data) i zasade "nowy zastepuje stary" od pierwszej linii.
3. Domknac przerwany audyt 6465019 (position-construction) po odnowieniu limitow — nie zakladac
   z wstepnej kontroli, ze reszta sie zgadza.
4. Kontynuowac wg wlasnej rekomendacji tego AI: RUN C1 (dostawca korekty Z -> terra potwierdzony
   przez MaTerrainManagerRuntime wg 6465019) -> C2 (SceneFeeder->model bridge) — to najkrotsza
   sciezka do rozstrzygniecia czy placement jest lokalny czy sieciowy.