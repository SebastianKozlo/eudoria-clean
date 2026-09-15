WORK-AUDIT PROMPT_LIFECYCLE — audyt-auditor-md-flow-20260914 — TRZECIA (FINALNA) LEKTURA
(Plik audytora, nie czesc pracy wykonawcow. ASCII-only dla gwarancji czystosci kodowania.)

PRZEDMIOT: cykl zycia promptow Desktop->OpenCode widziany w D:\auditor.md — jak byly
ANALIZOWANE, ROZKLADANE, PONOWNIE DEFINIOWANE, SPRAWDZANE NA BLEDY i jak z nich wyprowadzano
NASTEPNE KROKI. Trzecia lektura: weryfikacja verbatim L15989-16128 (patch P10), L17570-17621
(self-check + patch P12), L16252-16306 (drabinka twierdzen A-E), L16128-16330 (ZLECENIE).

=== FAZA 1: ANALIZA WEJSC (zanim powstanie prompt) ===
Kazdy prompt poprzedza faza analizy trzech typow wejsc, kazdy z innym rezerwem zaufania:
(a) RAPORT WYKONAWCY -> sprawdzany przeciwko bajtom: git rev-parse/status/diff, re-hash
    manifestow, claims vs evidence. Wyjscie: ACCEPTED / QUALIFIED / RETRACTED / UNVERIFIED.
(b) MATERIALY ZEWNETRZNE (ChatGPT-web) -> "lista twierdzen do sprawdzenia, nie zrodlo
    prawdy" (L16301). Przed pisaniem promptu wykrywany jest BIAS wejscia — przyklad:
    "Rozmowa z ChatGPT zbyt szybko przechodzi od 'prawdopodobnie serwer' do 'prawdopodobnie
    pliki klienta'" (L15545). Dopiero potem powstaje macierz: CLAIM / SOURCE / OBSERVATION /
    LIMITATION / RELEVANCE_TO_EU935 / STATUS.
(c) HIPOTEZY USERA -> wchlaniane jako hipotezy, nigdy jako prawda. User: "moim zdaniem to
    gdzies musi byc zaszyte" -> prompt przyjmuje: "Dotychczasowe badania nie dowodza, ze
    lokalizacji tam nie ma. Dowodza jedynie, ze nie rozpoznalismy jeszcze zapisu" (L14360).
    User: "budynki na serwerze nie maja sensu" -> odpowiedz: "sam argument o kosztach
    transmisji nie wylacza wariantu serwerowego... 32 kB przy 1000 budynkow" (L17546) —
    hipoteza uszanowana, ale utrzymana jako hipoteza (H1-H4).
Analiza KONCZY SIE jawna dyspozycja przed promptem: "Przeczytalem caly zalacznik. Propozycja
jest wartosciowa, ale wymaga kilku poprawek: [5 ponumerowanych korekt]" (L15991-15997).

=== FAZA 2: ROZKLADANIE (dekompozycja) — osiem narzedzi ===
N1. DRABINKA TWIERDZEN A-E (L16267-16274) — najostrsze narzedzie w pliku:
    A. A jest konsumowane jako id zasobu modelowego.
    B. W sprawdzonych przypadkach A odpowiada wpisowi <A>.nif.
    C. WSZYSTKIE odpowiednie A w korpusie maja takie odwzorowanie.
    D. CALA sciezka wykonania od A do fizycznego odczytu jest rozpisana.
    E. Instancja modelu otrzymuje historyczny world transform.
    REGULA: "Nie awansuj B do C ani A/B do D/E bez nowych dowodow."
N2. PODZIAL NA RUNY: C1 (korekty F1-F3 + trace 00853A80->provider) vs C2 (instancja->model):
    "Kazdy run powinien miec osobny raport, QC, commit i push. Dzieki temu mozna zweryfikowac
    C1 przed rozwijaniem dalszych wnioskow." (L17583)
N3. TAKSONOMIE KLASYFIKACYJNE z obowiazkiem dowodu: konsumenti = STATIC_WORLD /
    AVATAR_EQUIPMENT / PREVIEW_UI / OTHER / UNKNOWN; "Nazwa RTTI ani intuicja nie wystarcza."
N4. POZIOMY POKRYCIA: INVENTORIED / RAW_SCANNED / DECOMPRESSED / STRUCTURALLY_PARSED /
    CONSUMER_TRACED / NOT_INSPECTED. "Zaszyfrowany payload nie jest przeszukany wewnetrznie
    tylko dlatego, ze przeskanowano jego ciphertext." (P10 s.4)
N5. ZBIOR HIPOTEZ BEZ ZWYCIEZCY: H1 LOCAL / H2 LOCAL_DERIVED / H3 NETWORK / H4 HYBRID.
    "Brak lokalnego trafienia nie potwierdza H3. Istnienie world editora nie potwierdza H1."
N6. MECHANIZM vs DANE HISTORYCZNE: "Potwierdzenie A nie oznacza automatycznie odzyskania B.
    Umieszczenie modelu na wybranych wspolrzednych nie jest odzyskaniem placementu." (P11 s.1)
N7. STATYKA vs RUNTIME: "Rozdziel analize statyczna od obserwacji runtime. Nie pisz
    'wykonano', jesli tylko przeczytano kod lub cudzy artefakt." (L16120-16121)
N8. OSIE RAPORTU: "Raportuj osobno: A. wiarygodnosc zrodel zewnetrznych; B. semantyka pola A
    i ladowanie zasobu; C. mechanizm tworzenia instancji i transformacji; D. odzyskanie
    historycznych pozycji." (P10 s.5) — pojedynczy verdict "wszystko zamkniete" zakazany.

=== FAZA 3: PONOWNE DEFINIOWANIE (redefinicja) ===
R1. P6->P7: feedback usera ("przede wszystkim przez ten silnik... a jak dobijemy do tych
    NiArk... kazde dokladnie opisuje... moze w tych plikach jest lokalizacja zapisana")
    -> restruktyryzacja: engine-first, pelny rejestr KAZDEJ instancji NiArk (bez "pierwsze
    30"), priorytet-lokalizacja jako P0, klasyfikacja kandydatow (lokalna/NIF-scena/swiat-
    gry/UV/bind/projekcja/nierozstrzygnieta), "GLOBALNA W SCENIE NIF != GLOBALNA NA MAPIE".
R2. P2->P3: odpowiedz wykonawcy wchlana: "Przyjmuje zamkniecie cyklu... Nie powtarzaj
    kolejnej adjudykacji" + pin SHA256 + "testy maja sprawdzac wersje kanoniczna, nie
    przypadkowa kopie pod zewnetrzna sciezka".
R3. P10 = ROZSTRZYGNIACZ SPORZECZENCI z JAWNĄ PIERWSZENSTWEM: "Ponizsze zasady maja
    pierwszenstwo nad sprzecznymi zapisami obu wczesniejszych promptow." (L16004). Kazdy z
    5 blokow nadpisuje jeden konkretny konflikt: (1) commit+push obowiazkowy vs zakaz
    publikacji; (2) "NIE ZASTĘPUJ network-first zalozeniem client-only"; (3) priorytet:
    instancja budynku przed skanami; (4) skany z okreslonym pokryciem; (5) "BRAMKI NIE MOGA
    WYMUSZAC ODKRYCIA" — "Dobry, odtwarzalny wynik negatywny jest poprawnym wynikiem rundy."
R4. P11 = UNIFIKACJA: jeden prompt deep-think (GLM 5.3), 14 sekcji, wchlania P10 + audyty +
    macierz zrodel zewnetrznych + drabinke A-E + hipotezy H1-H4 + szablony bramek.
R5. P12 = PATCH zakresu po self-review: tylko fazy 1-2 jako RUN C1; "Faze 3 pozostaw jako
    osobny RUN C2, uruchamiany po kontroli wynikow C1."

=== FAZA 4: SPRAWDZANIE BLEDOW SAMYCH PROMPTOW (cztery poziomy) ===
E1. SELF-CHECK NA ZADANIE: user: "czy w tym prompcie byl jakis blad?" -> odpowiedz w 3
    krokach: (1) bezposrednio: "Nie bylo w nim zasadniczego bledu technicznego"; (2) diagnoza:
    "Do ulepszenia jest organizacja zakresu: obejmuje badanie dostawcy i model binding —
    lepiej dwa osobne runy z kontrola pierwszego"; (3) patch + klauzula rollback:
    "Jesli juz uruchomiles stary prompt, nie trzeba kasowac ani zaczynac od nowa — wystarczy
    przekazac to doprecyzowanie." (L17598-17621)
E2. SPRAWDZANIE RECENZENTA (zewnetrznego): "Przyjalbym dwie zmiany organizacyjne" + 3
    zastrzezenia: "38 indeksow dispatchera != 38 komunikatow"; "nazwanie korekty 'wysokoscia
    podloza' nadal jest hipoteza"; "audyt wykryl bledy != poprawki wykonane". (L17577-17591)
E3. SPRAWDZANIE POPONOWANYCH KONTROL (meta-meta): "ID 296445 nie miesci sie w u16; obciecie
    stworzyloby inne ID. Przesuniecie o cztery bajty nadal zachowuje wyrównanie floatow i
    nie musi byc kontrola negatywna." (L15997) — odrzucenie PROPONOWANEJ kontroli negatywnej,
    ktora kontrola negatywna nie byla. W P11 s.11: "Dla kazdej kontroli wyjasnij, jaka
    hipoteze testuje" + "Uzasadnij, dlaczego dana kontrola powinna zniszczy badana relacje,
    a nie tylko zmienic poprawny rekord."
E4. KALIBRACJA POD MODEL DOCELOWY: user: "(bedzie dzialal w deep think w MAX GLM 5.3)" ->
    prompt otwiera anty-wzorzec tego modelu: "Wykorzystaj dostepny czas na rozstrzyganie
    konkretnych pytan, nie na mnozenie planow, etykiet i deklaracji pewnosci." (L16135-16136)
    Plus swiadomosc uszkodzen pipeline'u: "Kopiuj bezposrednio z bloku kodu — sciezki
    powinny zawierac zwykle _, bez dodatkowego \ przed podkresleniami" (L9747).

=== FAZA 5: DYSCYPLINA NASTEPNYCH KROKOW ===
K1. ZAWSZE DOKLADNIE JEDEN eksperyment ("Jeden nastepny eksperyment o najwiekszej wartosci"),
    wyprowadzony z LUKI DOWODOWEJ (nie z zyczenia) — np. RUN C2: dekod slotow vtable
    0x00A7D458 pod katem konsumenta SF+0x34..0x3C i lacza SF+0x30 z systemem modeli.
K2. Eksperyment ma zawsze: WEJSCIA (EXE SHA E7785430..., adresy vtable, funkcje), BRAMKI
    (GA census slotow: kazdy czyta SF+0x34? TAK/NIE; GB dataflow konsumenta; GC KONTROLA
    POZYTYWNA — znana krawedz SF+0x30->FUN_007B6A80), TEST ROZRÓZNIAJACY (slot konsumuje
    SF+0x34 i przekazuje do wezla scenowego -> transform->model domkniety JEDNYM lancuchem;
    nie -> model wylacznie kanalem atrybut-drzewa (pump 0x66) i NOT_DEMONSTRATED zostaje),
    HARD_STOP (mutacja oryginale/historii), i uczciwy wynik negatywny zdefiniowany Z GORY.
K3. Nastepny krot formuluje sie PRZY KAZDEJ rundzie — nigdy backlog 10 eksperymentow;
    kolejny wynika z wyniku poprzedniego (F-luka -> eksperyment -> wynik -> nowa F-luka).

=== SZABLON FINALNY (destylat P10+P11+P12, do ponownego uzycia) ===
1. Tryb: deep-think; anty-dekoracja ("rozwiazywanie pytan, nie plany/etykiety/pewnosc").
2. GO + zakaz zatrzymywania sie na planie.
3. Repo + ostatni zweryfikowany commit + "sprawdz aktualny HEAD; zachowaj cudze zmiany".
4. Materialy do FULL_READ (z READ_LOG: FULL/PARTIAL/EXECUTED/HISTORICAL).
5. Drabinka twierdzen A-E + "nie awansuj bez nowych dowodow".
6. Macierz zrodel zewnetrznych (CLAIM/SOURCE/OBSERVATION/LIMITATION/RELEVANCE/STATUS).
7. Hipotezy H1-H4 bez zwyciezcy + reguly wzajemnego niepotwierdzania.
8. Zadanie P0 z rozdzieleniem MECHANIZM vs DANE + klasyfikacja z dowodem.
9. Dwa zbiezne slady (przod: template->model->wlasciciel; wstecz: transform->producent->zrodlo).
10. Pokrycie skanow (6 poziomow) + "nie wymagaj ID obok transformacji".
11. Wlasne kontrole: round-trip, kontrola dodatnia i negatywna z UZASADNIENIEM co niszczy,
    seed+rozklad, holdout oddzielony od dopasowania, "kilka raportow z tych samych
    artefaktow != niezalezne wykonania".
12. Granice: READ-ONLY oryginale, nie ruszac cudzych, bramki nie wymuszaja odkrycia,
    statyka!=runtime, brak zbiorczego "wszystko zamkniete".
13. Raport: osobne osie A-D, manifesty, skrypty, ograniczenia odtwarzalnosci.
14. Publikacja: commit+push rowniez przy PARTIAL/NOT_FOUND; weryfikacja SHA na origin;
    "nie ogłaszaj publikacji, jesli push nie nastapil".
15. NASTEPNY KROK: jeden eksperyment z bramkami GA/GB/GC + test rozrozniajacym + HARD_STOP.