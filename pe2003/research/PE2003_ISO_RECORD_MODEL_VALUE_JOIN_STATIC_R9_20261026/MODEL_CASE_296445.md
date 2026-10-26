# MODEL CASE 296445 — certyfikat R9
- source/build: ISO PC Gamer Nov 2003 / klient 5.1.0.0 (section1.bin D43A23B9...) jako korpus docelowy; referencje: COT Jan 2003, pcg_install, pcg915, EU2008.
- availability ISO: NOT_OBSERVED_IN_BOUNDED_SEARCH (zakres: czytelne drzewo ISO9660 42 wpisy + pelny 53-plikowy payload instalatora + 50.bnt terrain-only + manifesty; zero .ark/.nif/.bvi). Wariant 2003 byte-identical dostepny poza ISO w 4 korpusach (era-oznaczony, 656795D8...); wariant ery 5.1.0.0: UNKNOWN.
- definition->resource: templates.vfs (REFERENCYJNY, era UNKNOWN): cell 4508, para value-id (296445,296446), zero nazwanych slotow, JEDEN param f32=124.941 (CANDIDATE value-source; bez konsumenta i frame). W ISO-era: brak definicji (dane .ark niedostepne).
- actual open/deserialize: NIE wykonany dla ISO-era (brak pliku); referencyjny: rekord sparsowany (I2/QC2).
- instance identity: NOT_ESTABLISHED w ISO-era. Mechanizm wiazania klienta potwierdzony (owner->E->X->M->record(E,M)), ale bez danych ery nie istnieje instancja do wiazania.
- transform source: mechanizm .ark (Blowfish 448-bit, klucz @0x6b6648, decrypt 0x520AD0) CONFIRMED dla klienta 5.1.0.0; zrodlo wartosci transformacji dla tej instancji: UNAVAILABLE (dane .ark ery nie istnieja lokalnie).
- authentic values: brak. Frame/units: NIE ustalone.
- najlepszy punkt zaczepienia: templates.vfs @offset 96532 (u32 id=4508, v1=296445, v2=296446, f32 124.941) — era UNKNOWN, wartosc kandydacka bez konsumenta; NIE historyczna lokalizacja.