# METODA_DESKTOP_PE — procedura pracy przejeta z sesji Desktop (ChatGPT/Codex, projekt PE)
# WORK-AUDIT (audytor: Work-Audit) — dokument wiedzy miedzy sesyjnej; NIE jest czescia pracy wykonawcow.
# Przeznaczenie: kazda NOWA sesja Work-Audit zaczyna od TEGO pliku, zanim zacznie audytowac.

## SKAD TO SIĘ WZIĘŁO
Zrodlo wiedzy: transkrypt D:\Untitled.txt (7266 linii — pelny cykl audytow Desktop nad EU935,
od audit-eu935-79549d5 [11.09] po przerwany audyt runu 6465019 [14.09]) + moje wlasne sondy
treningowe w audyt-eu935-position-construction-6465019/. Przeczytane od poczatku do konca.

## PROCEDURA (8 krokow — stosowac bez wyjatkow)

KROK 0 — STAN GRUNT (nigdy nie zakladaj):
- git rev-parse HEAD; git status --short; git ls-remote origin refs/heads/master
- Get-FileHash EXE/archiwow vs piny z raportu (np. Entropia.exe 9.3.5 = E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31)
- nazwa pliku/katalogu/ZIP-a NIE jest wersja klienta (przypadek: DVD "2008" = klient 9.1.5.0, nie 9.3.5)
- sprawdz czy wskazany commit to nadal HEAD (zdarzylo sie: HEAD poszedl dalej o 2 runy)

KROK 1 — PELNA LEKTURA wszystkiego o co jest spor:
- REPORT/QC_REPORT/ERRATA/HANDOFF/STAGE_ACCEPTANCE_GATES wykonawcy + wcześniejsze pakiety audytow
- z raportu wyciagnij KAZDE twierdzenie nosne (liczby, VA, "wylacznie", "zero", "nigdy") do macierzy
- grep sluzy do LOKOWANIA, nie do dowodzenia nieobecnosci

KROK 2 — IZOLACJA:
- wlasny katalog: D:/TESTAI/audits/work-audit/audyt-<temat>-<hash>/
- oryginaly (exe, archiwa, repo produkcyjne, src/game/, experiments/) READ-ONLY
- kopie robocze robocopy do wlasnego katalogu; kazdy wlasny plik z naglowkiem WORK-AUDIT

KROK 3 — WLASNE NARZEDZIE + WLASNE BAJTY:
- wzorzec: pe.mjs (~14 linii) — parser PE: sekcje, off(va), dump() heksdump, u32(), cstring(),
  calls(target) census E8, target(va); spacer RTTI: vtable-4 -> COL -> [COL+12]=TD -> TD+8 nazwa
- kopiuj wzorzec z: C:\Users\User\Documents\ChatGPT\PE\audit-eu935-origin-seam-78cd153\pe.mjs
- NIGDY nie cytuj cudzego dekodu jako dowodu — kazdy pin wlasnym heksdumpem z fizycznego EXE
- capstone niedostepny w srodowisku -> dekoduj recznie wzorce opcodow (jest wykonalne; przyklad:
  FUN_00746550=8B 41 04 C3, FUN_00746560=8D 41 08 C3, FUN_00746570=8D 41 20 C3)

KROK 4 — WERYFIKUJ SILNIEJ NIZ DEKLARACJA:
- rekomputacja: censusy (calls/E8 aligned), manifesty (hash per plik!), liczby z raportu
- kontrproba negatywna: zepsute wejscie MUSI failowac (mutant NaN, uszkodzony dekoder)
- kontrola dodatnia: znana krawedz MUSI przejsc
- rozrozniaj: statyczny dekod != runtime; mechanizm != dane historyczne; transform lokalny != world;
  model/manager/instancja/wlasciciel instancji = 4 rozne rzeczy

KROK 5 — ADJUDYKACJA PER TWIERDZENIE:
- statusy: ACCEPTED / CONFIRMED-own / QUALIFIED / REJECTED-as-worded / NOT_DEMONSTRATED / OPEN / UNVERIFIED
- kazdy z lokalizacja plik:linia + wlasnym dowodem
- NEGATYW = "nie znaleziono w zbadanym zakresie" — NIGDY "nie istnieje" / "kanal wykluczony"
  (brak wzorca bajtowego nie wyklucza innego kodowania; "nie wykazane" != "wykluczone")

KROK 6 — SAMOKOREKTA JAWNA (znak rozpoznawczy metody):
- zlapan wlasny blad = zapisz go w raporcie z korekta (przypadki wzorcowe z transkryptu:
  kompozycja przez effect-list zamiast children-list; endian 296445=FD 85 04 00 nie 45 88 04 00;
  pin 0x004C4789->0x004C478A; moj wlasny dzisiejszy: manifest CSV ma 2 kolumny path,sha256 —
  moj skrypt czytal trzecia i dal falszywe 177/177 MISMATCH; po poprawie 177/177 PASS)
- zero-trust dotyczy TEZ wlasnych sond

KROK 7 — ZAPIS + PUBLIKACJA ODTWARZALNA:
- AUDYT.md/REPORT.md: twierdzenie -> lokalizacja -> dowod -> kontrproba -> wplyw -> naprawa (NIE poprawiam sam!)
- PROMPT_OPENCODE.txt (kontynuacja), manifest SHA256 wszystkich artefaktow
- publikacja: commit+push -> weryfikacja z committed blobow (git show commit:path + re-hash), nie z dysku
- skrot dla usera: potwierdzone / odrzucone / nieznane / JEDEN nastepny krok

KROK 8 — GRANICE JAWNIE NA KONCU:
- kazde NIEsprawdzone z nazwy; negatywny odtwarzalny wynik = poprawny wynik rundy
- "wszystkie warstwy zamkniete" wolno napisac tylko wtedy, gdy zaden wiersz nie zostal otwarty

## STAN PROJEKTU (na 2026-09-14 — sprawdzic od nowa w KROK 0)
- Repo: D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean (GitHub: SebastianKozlo/eudoria-clean, master)
- Lanuch commitow: 989f880 -> 3e2ccd9 -> ccd9fab -> 9969a81 -> ... -> 7053654 -> 2a2ba8d -> 24d7669
  -> 78cd153 -> e30f99f -> 6465019 -> 1a490ee -> 3644e5a (HEAD na dzien zapisu)
- Po 6465019 wykonano juz: 1a490ee (SceneFeeder slot census: sloty 0..5 = 50A460/5090A0/5090B0/50A050/5090C0/509580;
  slot3 czyta SF+0x30 link -> vtable[+0x44] slot17; vtable konczy sie na danych "dPVS")
  i 3644e5a (SF+0x30 link identity: RTTI .?AVNiNode@@, vtable 0x00A8CCF4, 2 writerow; TRANSFORM_TO_MODEL nadal NOT_DEMONSTRATED)
- Potwierdzone kodowo: templates.vfs -> pole A -> MODEL -> <A>.nif (4508->296445);
  dostawca korekty Z = teren (MaTerrainManagerRuntime, cell_id 16:16, named-resource tag 0x6E, FCHS);
  pozycja -> SceneFeederObject+0x34..0x3C kopia wartosci (FUN_005094C0); +0x74=klucz, +0x78=rekord[4],
  +0x88/+0x8C=rekord[0x20]/[0x24] (pola mask-struktury — NIE para param-setu)
- OTWARTE: SceneFeeder->model NOT_DEMONSTRATED; 4508/296445 OPEN; pozycje historyczne 296445 NIEODZYSKANE;
  format komorek terenu za seamem resource; D@4508=124.941 semantyka OPEN
- PRZERWANY audyt Desktop runu 6465019 (usage limit): wstepne 3 zarzuty sesji przerwanej to:
  (a) +0x78 vs +0x88/+0x8C param-set — MOJE sondy: +0x78=rekord[4] OK, +0x88/+0x8C=rekord[0x20]/[0x24],
      zarzut przerwanego Desktopu czesciowo bledny, ale fraza "zapis do +0x88 (faza B)" w REPORT 4.2 mylna;
  (b) slot vtable: FUN_0050A460 jest pod +0 nie +4 — POTWIERDZONE moja sonda (REPORT 4.4 mial zla numeracje);
  (c) "wylacznie kanal atrybut-drzewa" w HANDOFF po negatywie — nadmierny wniosek (P3 narracyjny)
- Nastepny planowany run: PE_935_SCIENCEFEEDER_MODEL_BRIDGE_R1 (czeka na GO czlowieka) — moze byc juz czesciowo
  wykonany przez runy 1a490ee/3644e5a — SPRAWDZ stan przed rozpoczeciem

## KLUCZOWE SCIEZKI
- Pakiety audytow Desktop: C:\Users\User\Documents\ChatGPT\PE\ (14 pakietow + niark-census-935.json)
- Transkrypt zrodlowy: D:\Untitled.txt
- EXE: D:\Eudoria_Reconstruction\pcg_install\Entropia.exe
- Pakiety runow: D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\
  + D:\Eudoria_Reconstruction\99_Audits\
- Zrodla Gamebryo: D:\gamebyroengine\extracted\Gb12_Source
- Skill audytowy PE-MASTER: D:\TESTAI\.opencode\skills\pe-master-audit\SKILL.md (metodologia zywaca — czytac przy okazji)

## PRZYKLADY PRAWDZIWYCH PULATEK (zlapanych ta metoda — pamietac wzorce)
1. licznik mierzyl rotacje LOKALNA zamiast swiatowej -> raport mowil "zero", bylo 45/42 plikow
2. walidator przepuszczal numSources=1.5 -> wyjatek w runtime
3. bramka oracle: NaN daje maxAbs=0 -> falszywy PASS (predykat musi wymagac isFinite)
4. dowod z PE2/2003 przypisano 9.3.5 (era-mixing)
5. endian-bug: 45 88 04 00 = 297029, a 296445 = FD 85 04 00 (round-trip asercja ratuje)
6. "subkursor" = w rzeczywistosci odczyt floatow sterowanych maska bitowa, ten sam kursor
7. "selektor pola D" czytal +0x08, nie +0x10
8. GUI crash jednym GET-em (URIError z callbacku HTTP)
9. literowka pinu: FSTP jest @0x004C478A (bajt za JNE), nie 0x004C4789
10. wiersz param-set w tabeli raportu wskazywal +0x88 jako "zapis pary", a +0x88/+0x8C
    dostaje pola mask-struktury (moje wlasne sondy, probe2)

# KONIEC — nowa sesja: zaczynamy od KROK 0.
