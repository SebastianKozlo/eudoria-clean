# QC_R2 — REPORT.md (niezależny wewnętrzny QC)

RUN_ID: PE_935_MODEL_PAIR_TRANSPORT_QUALIFICATION_SAVED_R1_20261019_QC_R2
ASSIGNMENT_MODE: INTERNAL_QC (pe-master-auditor, świeży dispatch rodzica; bez subagentów)
PARENT_RUN_ID / audytowany run: PE_935_MODEL_PAIR_TRANSPORT_QUALIFICATION_SAVED_R1_20261019
STARTED_UTC: 2026-10-19T06:25:51Z (RUN_STARTED.json w tym katalogu)
QC_VERDICT: **PASS_WITH_FINDINGS** (0×P0, 0×P1, 1×P2, 4×P3)

Niniejszy QC jest pierwszym zmateriaizowanym na dysku niezależnym QC tego runu (patrz finding P2-1: QC_R1 zapowiedziane w REPORT.md runu nie istnieje na dysku). Werdykt QC jest odrębny od SCIENCE_VERDICT i PROCESS_VERDICT runu i nie zamyka milestone'u.

## Metoda

- Pełny odczyt (do EOF) wszystkich 102 plików zindefikowanych przez root `artifact_index.csv`: root REPORT/HANDOFF/STAGE_ACCEPTANCE_GATES/AUDIT_CORRECTIONS_APPLIED/PIVOT_RECORD, wszystkie 12 eventów, 10 planów, 11 requestów, wszystkie 8 pakietów naukowych (REPORT/CLAIMS/HANDOFF/GATES/artifact_index/MANIFEST) + 4 pliki prób dziecka (CONTRACT/RUN_STARTED ×2), wszystkie 11 fizycznych ekstraktów (10 unikatowych okien + 1 duplikat bajtowy zweryfikowany hashem).
- Kontekst: pełny odczyt `CONTRACT.md` authoringu (SHA256 zweryfikowany: 69472F5D1D9766EB126C5E29FFBC82CC26644B12E6E560F378E5CCFEB973EE27) oraz `evidence_guard.py` (rozumienie semantyki plan/admit/extract/seal; seal użyty wyłącznie na końcu, na własnym katalogu QC).
- Wszystkie rehashowania: PowerShell `Get-FileHash` (niezależnie od narzędzi runu).
- Dwustronna weryfikacja ADMIT→ekstrakt→źródło: `selected_lines_sha256` przeliczone niezależnie z treści ekstraktów ORAZ — dla P01/P02 — bezpośrednio z oryginalnych linii źródłowych plików H5/GATE.

## Kontrola 1 — struktura pakietów: PASS

- 8/8 pakietów naukowych (P01_DIRECT_R3, P02_MEMBER_R1, P03_CALLER_R1, P04_CALLER2_R1, P06_CONSUMER_R1, P08_CONSUMER2_R1, P09_CONSUMER3_R1, P10_SINK_R1) posiada komplet 5 wymaganych plików: REPORT.md, HANDOFF.md, STAGE_ACCEPTANCE_GATES.csv, artifact_index.csv, MANIFEST_SHA256.csv (+ CLAIMS.json).
- Re-hash **wszystkich** wierszy każdego manifestu pakietowego (nie tylko 3): 6–7 wierszy/pakiet, 50/50 OK (rozmiar+SHA); bijekcja dysk↔manifest+dokładnie MANIFEST_SHA256.csv dokładna dla 8/8.
- P01_EXEC_R1 i P01_EXEC_R2 (2/10 katalogów) NIE posiadają kwintetu — to udokumentowane archiwa dwóch niekompletnych prób dziecka (CONTRACT.json + RUN_STARTED.json + ekstrakt przygotowany przez rodzica; input extract był pre-staged przez rodzica zgodnie z CONTRACT §10, potwierdzone zawartością CONTRACT.json dziecka). Zgodne z §11 („puste/niekompletne próby zachowaj jako takie"). To zamierzony wyjątek, nie defekt.

## Kontrola 2 — root artifact_index.csv vs dysk: PASS

- 102/102 wierszy: rozmiar i SHA256 zgodne z dyskiem (0 niedopasowań).
- Bijekcja: 103 pliki fizyczne (bez reviews\) = 102 wiersze indeksu + `artifact_index.csv` (self-excluded; dokumentowany precedens). Brak plików poza indeksem; brak wierszy bez pliku.

## Kontrola 3 — spot-check 4 eventów ADMIT vs piny ekstraktów: PASS

Wybrane: 000002_ADMIT (P01), 000005_ADMIT (P04), 000010_ADMIT (P08), 000012_ADMIT (P10).

| Event | selected_lines_sha256 (event) | przeliczone z treści ekstraktu | rows (event=przeliczone) | CALL (event=przeliczone) | admission_id w nagłówku ekstraktu |
|---|---|---|---|---|---|
| 000002 P01 | DABB3B0C…66B386 | DABB3B0C…66B386 ✓ | 47=47 ✓ | 2=2 ✓ | Abe53670b3300 ✓ |
| 000005 P04 | 3F5547AC…53373 | 3F5547AC…53373 ✓ | 46=46 ✓ | 2=2 ✓ | A8562f73a947d ✓ |
| 000010 P08 | 7C1806EE…F17AB7B | 7C1806EE…F17AB7B ✓ | 69=69 ✓ | 5=5 ✓ | A94de71d9876c ✓ |
| 000012 P10 | 12352E27…EF128A5 | 12352E27…EF128A5 ✓ | 42=42 ✓ | 2=2 ✓ | A83b5e96b9c96 ✓ |

- Dodatkowo (najsilniejsza forma): dla P01 przeliczyłem hasz wycinka **oryginalnego źródła** GHIDRA_H5_VTABLE2.txt linii 649385–649431 → DABB3B0C… ✓ równe pinowi ADMIT; dla P02 GHIDRA_GATE_00407270.txt linie 66–80 → CA0CC7CA… ✓ równe pinowi ADMIT. Łańcuch źródło→ADMIT→ekstrakt domknięty fizycznie.
- Piny źródeł rehashowane: GHIDRA_H5_VTABLE2.txt = 50 780 146 B / 642CC29A… ✓; GHIDRA_GATE_00407270.txt = 1269 B / C34D2BD8… ✓ (zgodne ze wszystkimi 10 eventami ADMIT).
- Hash-chain 12/12 eventów poprawny (previous_sha256 każdego = rzeczywisty SHA poprzedniego; START zaczyna od 64×0).
- Ekstrakt P01 istnieje fizycznie w 2 kopiach bajtowo tożsamych (P01_EXEC_R1/R2, SHA 021062EC…), obciążony budżetem raz (1 admission Abe53670b3300) — duplikat to plumbing próby retry, nie podwójna opłata.

## Kontrola 4 — incydent admission P08: PASS (ujawnienie pełne; brak użycia niezamierzonych ciał w claimach nośnych)

- Incydent (4 ciała vs 2 zarezerwowane) jest jawnie ujawniony w CZTERECH miejscach: package REPORT (sekcja „INCYDENT ADMISSION (PARTIAL/NONCOMPLIANT — jawny)"), CLAIMS.json (`process_status` + claim P08-C2 REJECTED-as-worded), package HANDOFF, package gate G_P08_ADMISSION=FAIL oraz root gate G_RUN_P08_ADMISSION=FAIL i root REPORT (PROCESS_VERDICT=PARTIAL_NONCOMPLIANT).
- Fizyczna weryfikacja: okno [006C3D40,006C3E00) zawiera dokładnie 4 wejścia funkcji — 006C3D40 (pełne, RET @006C3D8C), 006C3D90 (pełne, RET 4 @006C3DA5), 006C3DB0 (pełne, RET 4 @006C3DE9), 006C3DF0 (ucięte) — dokładnie jak deklaruje pakiet. Opis strukturalny niezamierzonych ciał (użycie 006C3A50 + FLD/FMUL) zgodny z ekstraktem.
- Brak load-bearing claim z niezamierzonych ciał: claimy P08-C1/C3 kotwiczą wyłącznie w wierszach 006C3D40 (006C3D41–006C3D8C; log-depth 006C3D52–006C3D6F, CALL 006C3740 @006C3D76, CALL 006C3330 @006C3D82 — wszystkie zweryfikowane wiersz po wierszu). Niezamierzone ciała występują wyłącznie jako notatka strukturalna, claim o statusie REJECTED oraz konserwatywna opłata budżetowa (4 ciała, 5 CALL — 3 miejsca CALL z niezamierzonych ciał opłacone konserwatywnie i jawnie wykazane w actuals pakietu).
- Analogicznie P09: drugie ciało 006C2CE0 (2 ciała ≤ 3 zarezerwowane — bez incydentu) ma interpretację zatrzymaną na notatce strukturalnej (claim P09-C2 REJECTED-as-worded) ✓.

## Kontrola 5 — przeliczenie budżetów vs limity 24/4800/160: PASS (z notą P3-3)

Przeliczenia z surowych ekstraktów (każde okno raz; duplikat P01_EXEC_R2 wyłączony):

| Metryka | Limit | Rehash/przeliczenie QC | Zgłoszone przez run | Ocena |
|---|---|---|---|---|
| Wiersze instrukcji | 4800 | **404** (47+54+46+6+41+41+69+58+42; = suma ledgera ADMIT) | „419/4800" | 419 = 404 + 15 linii dokumentowych P02 (konflacja mianników — P3-3; kierunek konserwatywny) |
| Linie body dokumentów | 1000 | 15 (FUN_0040b070, linie 66–81 excl.) | 15/1000 | zgodne ✓ |
| Miejsca CALL | 160 | **26** (2+6+2+0+5+3+5+1+2) — dokładnie | 26/160 | zgodne ✓ (liczone po unikalnym VA) |
| Ciała | 24 | obciążenie 21 (ledger rezerwacji ADMIT: 20; rzeczywiste wejścia fizyczne: 13; P08: 4 rzeczywiste vs 2 zarezerwowane — jawnie obciążone 4) | 21/24 | zgodne, konserwatywne ✓ |
| Warianty | 24 | 22 (suma opłat pakietowych) | 22/24 | zgodne ✓ |

- Żaden limit nie przekroczony pod żadną interpretacją (404 i 419 ≤ 4800; 21 ≤ 24; 26 ≤ 160; 22 ≤ 24; 15 ≤ 1000). Gate G_RUN_BUDGET=PASS zasadny.
- Zgodnie z nauką C3 (AUDIT_CORRECTIONS_APPLIED): incydent P08 jest oznaczony PARTIAL/NONCOMPLIANT procesu mimo zachowania globalnego capa — run uczciwie to utrzymuje (PROCESS_VERDICT=PARTIAL_NONCOMPLIANT).

## FINDINGS

### P2-1. REPORT.md runu wskazuje nieistniejące artefakty QC_R1; status INDEPENDENT_QC nigdzie nie zmateriaizowany
- **Źródło:** root `REPORT.md` linia 63 (sekcja „## QC"): „wynik w QC_QC_R1\ — patrz artifact_index i HANDOFF"; `reviews\` zawiera wyłącznie QC_R2 (ten katalog); root `artifact_index.csv` (102 wiersze) i root `HANDOFF.md` nie zawierają żadnego odwołania do QC_R1/QC_QC_R1.
- **Skutek:** konsument zapisanego runu kierowany jest do nieistniejącej lokalizacji dowodu QC; końcowy status INDEPENDENT_QC (=UNAVAILABLE wg warunkowej reguły §10, którą sam REPORT cytuje) nie został nigdzie zapisany. Łańcuch „rodzic dispatchował świeżego audytora → wynik zmaterializowany" jest w zapisanym runie nieudowodniony.
- **Wpływ na naukę:** brak — claimy naukowe nie zależą od QC_R1; niniejszy QC_R2 dostarcza pierwszego zmaterializowanego niezależnego QC.
- **Poprawka (do decyzji rodzica; pliki runu dla mnie zamrożone):** w przyszłym fresh katalogu corrigendum/notki rodzica zapisać `INDEPENDENT_QC_R1=UNAVAILABLE (no artifacts on disk)` oraz wskazać `reviews\QC_R2` jako pierwsze zmaterializowane QC.
- **Test rewalidacji:** `Test-Path reviews\QC_QC_R1` → oczekiwane wyraźne rozstrzygnięcie (istnieje z artefaktami LUB jawny zapis UNAVAILABLE w notce); referencje REPORT resolvable.

### P3-2. Root STAGE_ACCEPTANCE_GATES.csv: błędna ścieżka evidence dla G_RUN_P08_ADMISSION + 3 komórki evidence ogólnikowe
- **Źródło:** root `STAGE_ACCEPTANCE_GATES.csv` wiersz 6: evidence=`packages/P08_CONSUMER_R1/REPORT.md` — katalog nie istnieje (rzeczywisty pakiet: `packages\P08_CONSUMER2_R1\REPORT.md`, który istnieje i incydent ujawnia). Dodatkowo G_RUN_H1_MECHANISM / G_RUN_H2_QUEUE / G_RUN_INSTANCE_EDGE mają evidence=`packages reports` (bez konkretnych ścieżek), a lista G_RUN_ALL_PACKAGES_SEALED anotuje „P05-in-P04", lecz nie analogicznego „P07-in-P06".
- **Skutek:** traceability wskazanego gate'a wymaga ręcznego mapowania nazwy; substancja gate'a (FAIL incydentu) pozostaje poprawna i udokumentowana w właściwym pakiecie.
- **Poprawka:** corrigendum gates (osobny fresh plik, nie edycja zapięczętowanego zestawu) — poprawić ścieżkę na `packages/P08_CONSUMER2_R1/REPORT.md` i opcjonalnie doprecyzować 3 ogólnikowe komórki.
- **Test rewalidacji:** `Test-Path` wskazanej ścieżki evidence = True.

### P3-3. „Wiersze: 419/4800" konfluje wiersze instrukcji z liniami dokumentowymi
- **Źródło:** root `REPORT.md` linia 54 i HANDOFF linia 12 oraz gate G_RUN_BUDGET; CONTRACT §4 i event START definiują odrębne budżety: 4800 **wierszy instrukcji** i 1000 **linii body dokumentów**; ledger guarda (eventy ADMIT) trzyma je odrębnie (instructions=404, document_lines=15).
- **Skutek:** raportowany licznik 419 = 404 wiersze instrukcji + 15 linii dokumentowych P02; mianownik zmieszany względem własnej definicji limitu. Kierunek konserwatywny (zawyżone zużycie), żaden werdykt/gate się nie zmienia (404 i 419 ≤ 4800); linie 15/1000 raportowane równocześnie poprawnie — czyli 15 liczone podwójnie w dwóch metrykach.
- **Poprawka:** przyszłe raporty: `Wiersze instrukcji: 404/4800` + `Linie body dokumentów: 15/1000` rozdzielnie.
- **Test rewalidacji:** suma `counts.instructions` po eventach ADMIT = raportowana liczba; `document_lines` wyłącznie w metryce 1000.

### P3-4. „Brak nakładających się okien" nieprawdziwe na poziomie regionów VA
- **Źródło:** root `REPORT.md` linia 51 („sum — brak nakładających się okien"); plan P05 region [0x006C4050,0x006C4060) i plan P06 region [0x006C4057,0x006C40E0) — przecięcie [0x006C4057,0x006C4060) = 9 bajtów paddingu.
- **Skutek:** brak jakiegokolwiek wpływu na budżet i claimy: na poziomie wierszy ekstraktów nakładanie NIE występuje (P05 kończy się na 006C4056, P06 zaczyna na 006C4060; sum=union=404 wiersze instrukcji; instrukcja 006C40DF CALL liczone raz, w P06). Guard blokuje nakładania tylko wewnątrz pojedynczego requestu — między requestami przecięcie przeszło.
- **Poprawka:** przyszłe raporty: „brak nakładających się wierszy ekstraktów (sum=union); przecięcie regionów P05∩P06 = 9 B paddingu bez wierszy".
- **Test rewalidacji:** mechaniczne porównanie multizbioru VA wierszy wszystkich ekstraktów (bez duplikatów poza duplikatem plumbingowym P01_EXEC_R2).

### P3-5. Kontrakt retry P01_EXEC_R2 nie przechiszablowany — package_id i ścieżki wskazują P01_EXEC_R1
- **Źródło:** `packages\P01_EXEC_R2\CONTRACT.json` bajtowo identyczny z `packages\P01_EXEC_R1\CONTRACT.json` (SHA 0EBC403DE7161993EF4C3D4FA218E2DA55B3878D5B4CD373E93D5D817C01D48B): `package_id: "P01_EXEC_R1"`, inputs/allowed_outputs pod `packages\P01_EXEC_R1\...`, mimo umieszczenia w katalogu P01_EXEC_R2.
- **Skutek:** próba retry dziecka otrzymała kontrakt odwołujący się do katalogu poprzedniej próby; artefakt wyłącznie archiwalny (próba niekompletna, RUN_STARTED.json dziecka własne package_id ma poprawne). Zero wpływu na naukę i budżety.
- **Poprawka:** przy przyszłych retry — fresh CONTRACT.json z poprawnym package_id/ścieżkami; starych plików nie modyfikować (zamrożone archiwum próby).
- **Test rewalidacji:** `package_id` w CONTRACT.json retry == nazwa katalogu pakietu.

## Weryfikacje dodatkowe (wszystkie PASS)

1. **CONTRACT.md authoringu:** SHA256 = 69472F5D… ✓ równy pinowi w REPORT runu i w CONTRACT.json dziecka.
2. **Preflight numbers:** authoring = 25 plików / manifest 24 wiersze (self-excluded) / katalog external pins = 1275 ✓ zgodne z linią 5 REPORT runu.
3. **DENY 000006:** spójny — `CONTROL\REQUESTS\P04b.json` istnieje, `CONTROL\PLANS\P04b.json` nie istnieje (żądanie odrzucone za brak planu; okno zrealizowane później jako P05 z planem) — zgodny z opisem „incydent operacyjny bez wpływu na naukę".
4. **Claimy naukowe vs ekstrakty (spot):** wszystkie load-bearing claimy CONFIRMED pakietów P01/P03/P04/P06/P08/P09/P10 zweryfikowane wiersz po wierszu (ABI, stride 0x20/8, append {0x66,A} @006C3F8D-8F, immediate 008BD720 @006C3FB0, sort 006C3D40, adjacent-find 006C2CA8-2CB4, projekcja→0xBA45E8 @006C36F6/ADD [ESI+4],4, statyczne tablice ID 0xA855F0/0xA858B8/0xA858C0, odczyt globala [0xBA45E8]/[0xBA45EC] @006C4146/414C) — zgodne.
5. **Odrębność statusów:** run poprawnie separuje SCIENCE_VERDICT (PASS_WITH_QUALIFICATIONS) / PROCESS_VERDICT (PARTIAL_NONCOMPLIANT) / standing (bez awansu); stwierdzenia decompiler-only oznaczone (P02 program-identity UNVERIFIED) ✓; PAIR_FRAME_TO_PROJECTED=NOT_ESTABLISHED nieprzeniesione ✓.

## FULL_READ_LOG

Wszystkie 102 pliki z root artifact_index.csv przeczytane w całości; dodatkowo: CONTRACT.md (authoring, 162 linie), evidence_guard.py (188 linii), 2 pliki źródłowe zweryfikowane haszem (H5 odczytany wycinkowo do weryfikacji slice'ów — pełny odczyt 50 MB zbędny do przypisanych kontroli; GATE odczytany wycinkowo linii 66–80). Pliki QC_R2 (ten katalog) wykluczone z audytu runu.

## NOT_CHECKED

- Pojedyncze 1275 external pins katalogu SAVED_TEXT_CATALOG nie było rehashowane punkt po punkcie (poza zakresem zleconych kontroli; 2 nośne źródła runu rehashowane bezpośrednio z pełną zgodnością).
- Wewnętrzne pliki authoringu (QA_PASS_*, START_PROMPT itd.) nie były audytowane merytorycznie — zweryfikowano jedynie liczby preflight i SHA CONTRACT.md.
- Runtime/EXE nie dotyczy (run saved-only; brak claimów runtime do sprawdzenia).
- Opaque calle (0043A550, 0072F580, 007CE1E0, 006C2E00, 00475A10, 006C29D0, 006C3740, 006C3330, 006C24B0, 006C2C50, 00415670) nieotwarte — zgodnie z zakresem runu; run poprawnie oznacza je opaque/open-edge.

## Werdykt

**QC_VERDICT: PASS_WITH_FINDINGS.**

- Struktura, piny, łańcuch eventów i budżety runu są fizycznie zweryfikowane i spójne; incydent P08 jest uczciwie ujawniony i konserwatywnie rozliczony bez użycia niezamierzonych ciał w claimach nośnych.
- Findings (1×P2, 4×P3) są poziomu dokumentacji/provenance; żadna nie obala claimu nośnego ani nie zmienia SCIENCE_VERDICT/PROCESS_VERDICT runu.
- Rozstrzygnięcie QC_R2 nie jest MASTER_ACCEPTED ani zamknięciem milestone'u; P2-1 wymaga decyzji rodzica (zapis UNAVAILABLE dla QC_R1 i wskazanie QC_R2).
