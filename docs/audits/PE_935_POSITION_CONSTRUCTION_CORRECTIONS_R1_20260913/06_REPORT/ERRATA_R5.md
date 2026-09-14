# ERRATA_R5 — PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913

**RUN_ID:** `PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913`
**RUN_CLASS:** LOAD_BEARING · **TRYB:** STATIC-ONLY (klient nigdy nie uruchomiony)
**Era:** EU 9.3.5 (`pcg_install\Entropia.exe`, SHA256 `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31`, 8 015 872 B — zweryfikowany własnym S0 fail-closed)
**Autor:** pe-reconstruction (wykonawca), dispatch bezpośredni PE-MASTER. Publikacja: osobny krok po QC i adjudykacji (pe-master-auditor).

---

## 0. Zasady pierwszeństwa (wzorzec ERRATA_R3/ERRATA_R4)

Kolejność wiążącości warstw:
(a) evidence `01_RAW`/`02_ANALYSIS` (nietknięte), (b) ERRATA_R4, (c) **ERRATA_R5 (ten dokument)**, (d) raporty historyczne czytane przez pryzmat (b)+(c).
Historyczne pakiety są **NIETYKANE** — errata cytuje STARE treści verbatim (plik:linia); poprawiona treść żyje tutaj i w REPORT tego runu.
Piny VA = START instrukcji (konwencja ERRATA_R3 reguła 5 / ERRATA_R4 reguła 5).
Wszystkie dekody wykonawcy pochodzą z FIZYCZNEGO EXE (capstone 5.0.7, własny PE parser `pe935_core.py`); warstwa hexdumpów Desktopu NIE była źródłem dekodu (weryfikacja krzyżowa na końcu — §2.D).

**Rozstrzygnięcie D-1 (PE-MASTER, nadpisuje §13 w kwestii metatwierdzenia):** okno 0x004C4780-0x478F zostało ponownie zrzute z EXE w tym runu (`01_RAW/X004C4770_479F_D1_WINDOW.txt`) i jest **bajt-identyczne** z linią 69 `independent_hexdumps.txt` pakietu Desktop (16 bajtów, `dd d9` @0x004C4783-84). D-1 zamknięte jako błąd odczytu PE-MASTERa (L09). **W niniejszej erracie NIE formułuje się ŻADNEGO twierdzenia o „brakujących bajtach"** — potwierdzonym defektem pinów pozostaje wyłącznie off-by-one T-26.

---

## 1. Register targetów — T-01..T-32 (kolejność kontraktu §3.4)

### F1 — framing „sub-kursor/sub-pakiet u16-header" (gramatyka FUN_007343E0)

**T-01** — `PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/REPORT.md:52` (S6):
> „sub-kursor (FUN_007343E0 @0x00745419, u16-header); wariant u16 @0x00745435→rec+0x34"

- **Poprawka:** FUN_007343E0 czyta **strukturę 0x28 do rec+0x0C sterowaną maską u16** — brak zagnieżdżonego kursora; wariant/pozycja/rotacja kontynuują **ten sam strumień** po strukturze (konsumpcja struktury zależy od maski).
- **Uzasadnienie (własny dekod):** caller @0x00745414 `8D 57 0C; 52; 55; E8` → dst=rec+0x0C; FUN_007343E0: `MOVZX EBX,WORD [EAX+ECX]` @0x007343FB (maska), pary bitów dst+00/08/0C/10/14, trzy odczyty bezwzględne dst+18/1C/20, reszta→dst+24; **oba epilogi zwracają EAX=WSKAŹNIK WEJŚCIOWY** (MOV EAX,ESI @0x0073459C/0x007345B5). Arytmetyka konsumpcji: maska 0→34 B; 0x2AA/0x554→14 B; 0x7FE→14 B + reszta 0x554 (potwierdzone model + dekoder, 28/28 przypadków zgodnych, `01_RAW/F1_MASK_SUITE.json`).
- **Disposition:** ACCEPTED_AS_ERROR — sformułowanie „sub-kursor (u16-header)" jest błędne; poprawna treść żyje w REPORT §F1 tego runu.

**T-02** — ten sam wiersz S6 — całe grupowanie wariant/pozycja/rotacja/wektor-2/bajt jako zawartość „sub-kursora":
- **Poprawka:** wszystkie te pola to kolejne odczyty z **tego samego kursora** (FUN_007453D0 czyta: key u32→rec+0, FUN_00412B0→rec+4, struktura→rec+0x0C, wariant u16→rec+0x34, vec3 FUN_00412430→rec+0x38, rotacja→rec+0x44, u32→+0x50, u32→+0x54, f32→+0x58, u8→+0x5C; zwrot AL = flaga kursora @+0x11).
- **Uzasadnienie:** pełny własny dekod FUN_007453D0 (`01_RAW/F007453D0_DESERIALIZER.txt`); pozycje w strumieniu zależą od maski struktury (zmienna konsumpcja).
- **Disposition:** ACCEPTED_AS_ERROR — grupowanie „wewnątrz sub-kursora" jest błędne; to kontynuacja tego samego strumienia.

**T-03** — `REPORT.md:30` (§1, pełny fragment l.27-34):
> „deserializacja FUN_007453D0 z sub-pakietu kursora: vec3 12 B → setter f90 → rekord placementu +8/+0xC/+0x10 → ctor kopiuje do instancji +0x44..0x4C"

- **Poprawka (dwie części):**
  1. **F1:** „z sub-pakietu kursora" → „z KURSORA komunikatu, kontynuacja tego samego strumienia po strukturze 0x28 (maskowej) w rec+0x0C".
  2. **F2:** między kopią rekordu a ctorem brakuje kroku korekty: dla wariantów {3..7} FUN_004C46C0 pobiera h=FUN_00853A80(mgr, pos.x, pos.y, 0, 0) i warunkowo zapisuje z'=h do kopii (FSTP [ESP+0x18] @0x004C478A) — ctor dostaje **poprawioną kopię**.
- **Uzasadnienie:** dekod FUN_004C46C0 (warianty: CMP ESI,3→JE 0x004C473B…; korekta 0x004C4751-0x004C478E; ctor @0x004C47C1). Fun. 0085B1B0: `[+0x44..0x4C]=[FUN_00746560(record)+0..8]` = `&record+8` (`8D 41 08 C3`), czyli bajty skorygowane.
- **Disposition:** ACCEPTED_AS_ERROR (obie części).

**T-04** — `QC_REPORT.md:46-49` (§1c):
> „sub-kursor: FUN_007343E0 @0x00745419 (u16-header sub-pakietu → zagnieżdżony kursor @rec+0xC)" + kwalifikatory „(z SUB-kursora)" (linie 49-57 tej sekcji).
- **Poprawka:** „FUN_007343E0 @0x00745419 — struktura 0x28 maskowana do rec+0x0C; dalsze pola z TEGO SAMEGO kursora" — kwalifikator „(z SUB-kursora)" w l.49/51/55/57 do czytania jako „(z tego samego kursora)".
- **Uzasadnienie:** jw. T-01/T-02 (pary masek i odczyty w tym samym strumieniu; EAX=kursor w obu epilogach — funkcja nie może „wracać" innym kursorem).
- **Disposition:** ACCEPTED_AS_ERROR — framing błędny; atrybucje PÓL (rec+0x38 pozycja, +0x34 wariant, wektor-drugi) pozostają poprawne.

**T-05** — `ERRATA_R4.md:73-77` ([SE-R4-1] (ii)):
> „sub-pakiet (FUN_007343E0 @0x00745419): **wariant u16** … **POZYCJĘ vec3 3×dword** …"
- **Poprawka:** grupowanie po „sub-pakiecie" błędne — to odczyty z tego samego kursora; struktura 0x28 (rec+0x0C) to ODRĘBNY element, wyprzedzający wariant/pozycję.
- **Uzasadnienie:** kolejność odczytów FUN_007453D0 (dekod własny): key→param-set→**struktura**→wariant→pozycja→rotacja→wektor-2→bajt.
- **Disposition:** ACCEPTED_AS_ERROR (framing); treści pól OK.

**T-06** — `ERRATA_R4.md:97` ([SE-R4-1] ŹRÓDŁO):
> „FUN_007343E0 (sub-kursor u16-header)".
- **Poprawka:** „FUN_007343E0 (struktura 0x28 maskowana u16 → rec+0x0C; EAX=kursor wejściowy)".
- **Disposition:** ACCEPTED_AS_ERROR.

**T-07** — `STAGE_ACCEPTANCE_GATES.csv:11` (QC-3): kwalifikator „z sub-kursora".
- **Poprawka:** „z tego samego kursora (kontynuacja strumienia po strukturze 0x28 w rec+0x0C)".
- **Nota (z rejestru):** atrybucje pól rec+0x38 i u16@rec+0x34 w QC-3 pozostają — są poprawne.
- **Disposition:** ACCEPTED_AS_ERROR (sam kwalifikator).

**T-08** — `AUDIT_ENTRYPOINT.md:31` (fragment @offset ~1679; offset = pozycja znakowa wewnątrz wiersza 31):
> „sub-packet via FUN_007343E0: variant u16 @0x00745435 -> rec+0x34, **POSITION vec3 12B via FUN_00412430 @0x0074545A -> rec+0x38"
- **Poprawka:** „structure 0x28 via FUN_007343E0 @0x00745419 (u16 mask -> rec+0x0C; consumption mask-dependent), then SAME-cursor reads: variant u16 @0x00745435 -> rec+0x34, **POSITION vec3 12B via FUN_00412430 @0x0074545A -> rec+0x38".
- [AMENDMENT PE-MASTER audit: pierwotny cytat pomijał znacznik '**' obecny w żywym pliku; cytat skorygowany do dokładnej treści żywego wiersza]
- **D-4 (ta sama edycja wiersza):** literówka „undeoded" (@offset 3818) → „undecoded" — wspólna edycja z T-16, jawnie zdysklosowana.
- **Disposition:** ACCEPTED_AS_ERROR (+ literówka D-4 w tej samej edycji wiersza, która wykona publikator).

*Kontekst cytowany jako STARE (warstwa evidence/robocza, nietykana, już sformalizowana w ERRATA_R4):* `SEAM_FLOW_MAP.md:68` (pominięcie FUN_007343E0 w §4) oraz `RESEARCH_FINDINGS.md:20/73` (stare pola +0x50..0x58). Te pliki pozostają bez zmian (pakiety historyczne nietykalne).

### F2 — brak gałęzi korekty Z w końcowej syntezie

**T-09** — `REPORT.md:27-34` (§1): łańcuch „…vec3 12 B → setter f90 → rekord placementu +8/+0xC/+0x10 → ctor kopiuje do instancji +0x44..0x4C" pomija korektę z' w lokalnej kopii FUN_004C46C0 dla wariantów {3..7}.
- **Poprawka:** po seterach f90 i przed ctor: „dla wariantów {3,4,5,6,7}: h=FUN_00853A80(mgr, pos.x, pos.y, 0, 0); z' = h wtw h>z ordered (x87 FCOM/FSTSW/TEST AH,0x41/JNE — zapis h tylko przy h>z ordered; NaN→z'=z bity; equal→z'=z bity)". **Rekord callera NIE jest nadpisywany** — korekta dotyczy lokalnej kopii podanej ctorowi.
- **Uzasadnienie:** własny dekod 0x004C4751-0x004C478E + tabela x87 (21 wierszy, `01_RAW/F2_X87_TABLE.json`).
- **Disposition:** ACCEPTED_AS_OMISSION (synteza niepełna).

**T-10** — `REPORT.md:54` (S8):
> „create FUN_004C46C0(placement, u16-wariant, string, 1) @0x004C4952 … → new(0x128) @0x004C4792 → ctor FUN_00528E50 @0x004C47C1" — brak kroku korekty między kopią rekordu a new (dla {3..7}).
- **Poprawka:** „…create FUN_004C46C0(placement, wariant, string, 1) @0x004C4952 → lokalna kopia rekordu (@[ESP+8..0x33]) → dla {3..7}: korekta z' (FUN_00853A80 + x87 max-ordered) → new(0x128) @0x004C4792 → ctor FUN_00528E50 @0x004C47C1(&kopia_poprawiona, wariant, string, 1)".
- **Disposition:** ACCEPTED_AS_OMISSION.

**T-11** — `REPORT.md:55` (S9):
> „**`[+0x44..0x4C]=[record+8..0x10]`** (FUN_00746560)" — „record" = poprawiona kopia lokalna (z'), nie surowy deserializat.
- **Poprawka:** „`[+0x44..0x4C]=[FUN_00746560(record)+0..8]` gdzie FUN_00746560=`LEA EAX,[ECX+8]; RET` i record = LOKALNA KOPIA w FUN_004C46C0 ze skorygowaną z' (dla {3..7})".
- **Uzasadnienie:** dekod FUN_00746560 (4 bajty: `8D 41 08 C3`) + przebieg arg1 ctor: `lea ecx,[esp+0x14]`=kopia lokalna (@0x004C47BA po 3 push).
- **Disposition:** ACCEPTED_AS_UNQUALIFIED (kwalifikacja wymagana).

**T-12** — `REPORT.md:97` (§4, wiersz „Pozycja z kursora → placement+8..0x10 → instancja+0x44..0x4C"): brak korekty + pin „FUN_0085B3E0 @0x004C4875".
- **Poprawka (dwie części):** (1) dodać korektę z' dla {3..7} przed ctor; (2) pin **FUN_0085B3E0 @0x004C488A** (`E8 51 6B 39 00`) — patrz T-21.
- **Disposition:** ACCEPTED_AS_OMISSION + ACCEPTED_AS_ERROR (pin — patrz T-21/T-24).

**T-13** — `REPORT.md:120-124` (§5c):
> „(c) Skąd jest TRANSFORM (movable)? — z bajtów KURSORA komunikatu (S6: sub-pakiet vec3 12 B → f90)."
- **Poprawka:** niepełne dla {3..7}: z w instancji = **z' po korekcie max-ordered(z, h)** gdzie h z FUN_00853A80 — nie surowy bajt kursora; NaN ≠ Math.max; equal/-0/+0 na poziomie BITÓW. Dla pozostałych wariantów z = bajt kursora bez korekty. Framing „sub-pakiet" jw. T-01.
- **Uzasadnienie:** tabela x87 (z=-0,h=+0 → z'=-0 bity — dywergencja od Math.max; NaN(h)→z'=z ≠ Math.max(z,NaN)=NaN).
- **Disposition:** ACCEPTED_AS_UNQUALIFIED.

**T-14** — `HANDOFF.md:18-28`: zdanie-odpowiedź bez kroku korekty („setter f90 pisze pozycję do rekordu placementu +8/+0xC/+0x10, ctor kopiuje ją do instancji…").
- **Poprawka:** pomiędzy f90 a ctor: „dla wariantów {3..7} korekta z'=max-ordered(z, FUN_00853A80(mgr,pos.x,pos.y,0,0)) NA KOPII; ctor dostaje kopię poprawioną".
- **Disposition:** ACCEPTED_AS_OMISSION.

**T-15** — `ERRATA_R4.md:127-128` ([SE-R4-2]):
> „+0x14..0x3B transform 3×3+flaga word @+0x24 (FUN_007345C0)" — „macierz 3×3" = etykieta bez konsumenta; FUN_007345C0 zeruje 8×f32+word.
- **Poprawka (liczba zmierzona własnym dekodem):** FUN_007345C0 zeruje **9×f32** (+0x00/+0x04/+0x08/+0x0C/+0x10/+0x14/+0x18/+0x1C/+0x20 — 9× FST/FSTP) + word @+0x24 = 0 (`01_RAW/F007345C0_ZERO_INIT.txt`). Kształt 9+word pasuje do 3×3+flaga, ale etykieta „transform 3×3" pozostaje **BEZ KONSUMENTA**: census konsumentów (F1 pkt 4) wykazał, że w kanale FUN_004C47F0 struktura f90 (rec+0x0C..0x30) jest **write-only** (0 odczytów pól), a w instancji (struktura @+0x14) pisarze to ctor (rotacja→+0x18/+0x1C/+0x20 przez FUN_00734220/40/60) i FUN_0045AC90 (z recordu +0x64/+0x68/+0x70) — **readerów nie znaleziono w zbadanym zakresie** (boundary jawne).
- **Disposition:** PARTIAL — ERRATA_R4 miała rację co do braku konsumenta („etykieta bez konsumenta" — UTRZYMANE), ale liczba 8×f32 jest błędna (własny pomiar: 9×f32).

*Atrybucja do zachowania:* `SEAM_FLOW_MAP.md:46` (§3) już zawiera gałąź („jeśli wariant∈{3,4,5,6,7}: FUN_004154F0(mgr) → FUN_00853A80(mgr, 2×f32) → max(rekord[4], wynik)") — ERRATA_R5 cytuje ją jako źródło atrybucji; poprawiana jest końcowa synteza, nie odkrycie od zera. **Nota:** zapis „max(rekord[4], wynik)" wymaga kwalifikacji semantyki x87 — z'=h wtw h>z ordered (tab. §F2 REPORT), nie dwuargumentowy max w sensie Math.max.

### F3(a) — statyki (żywe skróty o zbyt mocnym zakresie)

**T-16** — `AUDIT_ENTRYPOINT.md:31` (fragment @offset ~3594):
> „STATICS (4508/296445) NOT covered by the movable channel (OPEN; the 296445 positions NOT recovered; D@4508 = 124.941 ANCHORS_ABSENT_SEMANTICS_OPEN unchanged)"
- **Poprawka:** „USE BY 4508/296445 NOT DEMONSTRATED in this channel; remains OPEN (the 296445 positions NOT recovered; D@4508 = 124.941 ANCHORS_ABSENT_SEMANTICS_OPEN unchanged)".
- **Uzasadnienie:** nazwa klasy MovableObject ≠ klasyfikacja danych zasilających; brak dowiedzionego połączenia ≠ wykluczenie; raw census E8 bez krawędzi 0x0094xxxx nie rozstrzyga przepływu pośredniego z pliku.
- **Disposition:** ACCEPTED_AS_OVERREACH (edycja wiersza w kroku publikacji; ta sama edycja co T-08/D-4).

**T-17** — `HANDOFF.md:27-28`:
> „STATYKI (4508/296445) NIE objęte tym kanałem; pozycje 296445 NIEODZYSKANE."
- **Poprawka:** „użycie przez 4508/296445 NIEWYKAZANE w tym kanale, pozostaje OPEN; pozycje 296445 NIEODZYSKANE."
- **Disposition:** ACCEPTED_AS_OVERREACH.

**T-18** — commit message 78cd153 (historia git, nietykalny; cytowany jako STARE): „STATICS (4508/296445) NOT covered by the movable channel (OPEN…)" — żywa kopia tego sformułowania = T-16 (entrypoint). Commit-history bez zmian.
- **Disposition:** NOTED (no edit — git history immutable; żywa kopia tylko T-16).

*Wzorce poprawne (utrzymać, NIE targety):* `REPORT.md:138-140` (§6.3: „statyki (4508/296445) NIE wykazane w tym kanale") i `REPORT.md:34` (§1: „NIE zostały objęte tym kanałem w tym runie") — zakres-exact; Desktop jawnie pochwalił §6.3.
*Źródło cytatu Desktop (przekazany werdykt):* „Dla statyków (4508/296445): UNKNOWN — ten kanał ich nie obejmuje." — drugie zdanie mocniejsze od dowodu; korekta jak T-16/T-17.

### F3(b) — „Źródło insertów = komunikaty"

**T-19** — `REPORT.md:99` (§4):
> „Źródło insertów = komunikaty (VFS=negatyw)"
- **Poprawka:** „źródło danych insertów WYKAZANE dla ścieżki procesora FUN_004C47F0 (4 callery: 0xB0/0xC6/0xC7/0xB2); 5 pozostałych callerów creatora (FUN_00456F40/FUN_0050BED0/FUN_00442190/FUN_00441910/FUN_004B3A00) i 8 generatorów kluczy = źródła danych NIEWYKAZANE (bounded negatyw VFS: census funnelu 1+6+8 = 0 krawędzi z 0x0094xxxx)".
- **Disposition:** ACCEPTED_AS_OVERGENERALIZATION (ograniczenie do wykazanej ścieżki).

**T-20** — `STAGE_ACCEPTANCE_GATES.csv:5` (GB4):
> „Zrodlo insertu = KOMUNIKATY: dispatcher FUN_004B18D0 switch(typ) case 0xB9->FUN_005B72C0 @0x004B1A16 (pin E8 A5 58 10 00) case 0xB0/0xC6/0xC7->processory placementu"
- **Poprawka:** jw. (T-19) + case 0xB9 w kontekście źródła insertów wymaga kwalifikacji (kanał kluczy/propagacji, nie deserializacji pozycji) + zbiór typów bez 0xB2 (patrz T-27).
- **Disposition:** ACCEPTED_AS_ERROR — wiersz GB4 = HISTORYCZNY, superseded przez QC-2/QC-3/[SE-R4-5/6] (patrz T-27/T-28/T-29 i §3 poniżej — JEDNA obowiązująca tabela bramek).

### F3(c) — piny P3 (stary pin „004C4875")

**T-21** — `QC_REPORT.md:75-77` (§1d):
> „FUN_0085B3E0(istniejąca_wartość, &[rec+0x38], 1) @0x004C4875"
- **Poprawka:** **@0x004C488A** (`E8 51 6B 39 00` — własny dekod); guard FUN_0085B750 @0x004C4878 (`E8 D3 6E 39 00`); rotation FUN_0085ADB0 @0x004C4896 (`E8 15 65 39 00`). „@0x004C4875" = ostatni bajt (disp 06) 2-bajtowego `FF D0` wcześniejszego pośredniego CALL slotu +0x14 (`MOV EAX,[EDX+0x14]` @0x004C4871, `FF D0` @0x004C4874 — bajty 0x004C4874-75).
- **Disposition:** ACCEPTED_AS_ERROR (pin off-by-one; stary pin = adres NIE-STARTU instrukcji).

**T-22** — `ERRATA_R4.md:102-104` ([SE-R4-1] KONTRTEST (4)):
> „FUN_0085B3E0(istniejąca, &[rec+0x38], 1) @0x004C4875" — jw. → @0x004C488A.
- **Disposition:** ACCEPTED_AS_ERROR (ten sam błąd pinu w warstwie ERRATA_R4 — supersedowane przez ten errata).

**T-23** — `ERRATA_R4.md:225-229` ([SE-R4-6] KONTRTEST):
> „FUN_0085B3E0(istniejąca, &[rec+0x38], 1) @0x004C4875" — jw. → @0x004C488A.
- **Disposition:** ACCEPTED_AS_ERROR (jw.).

**T-24** — `REPORT.md:97` (§4): pin „FUN_0085B3E0 @0x004C4875" — jw. (ten sam wiersz co T-12).
- **Poprawka:** @0x004C488A + korekta z' (część T-12).
- **Disposition:** ACCEPTED_AS_ERROR.

**T-25** — `REPORT.md:171` (§7):
> „dispatcherа: 0x25 wpisów (0xA2..0xC7), jump-table: **22** wpisów"
- **Poprawka:** „byte-table: **38 INDEKSÓW** (0xA2..0xC7; `CMP EAX,0x25` @własnym dekodzie = maks. indeks 37, nie 37 wpisów), jump-table: **22** wpisy".
- **Uzasadnienie (własny dekod):** `CMP EAX,0x25` porównuje indeks (0x25=37 = maks. dozwolony indeks) → zakres indeksów 0x00-0x25 = 38 wartości (0xA2..0xC7 po przesunięciu -0xA2 = 0..0x25 = 38); jump-table 22 wpisów (`01_RAW` QC dispatchera fazy B + własna kontrola `ADD EAX,-0xA2` @0x004B1B3C regionu).
- **Disposition:** ACCEPTED_AS_ERROR („0x25 wpisów" → „38 indeksów").

**T-26** — pakiet Desktop `PE_935_ORIGIN_SEAM_DESKTOP_AUDIT_R1_20260913/AUDYT.md:55` (== REPORT.md:55; pakiet historyczny — cytować, NIE edytować):
> „porównanie x87 i warunkowy `FSTP [ESP+0x18]` przy **004C4789**"
- **Poprawka:** off-by-one — `FSTP [ESP+0x18]` = `D9 5C 24 18` @**0x004C478A** (0x004C4789 = bajt disp `06` JNE `75 06` @0x004C4788-89). Pełny łańcuch (własny dekod): `FLD [ESP+0x44]`(h) @0x004C477B → `FCOM ST(1)` (D8 D1) @0x004C477F → `FNSTSW AX` (DF E0) @0x004C4781 → `FSTP ST(1)` (DD D9) @0x004C4783 → `TEST AH,0x41` (F6 C4 41) @0x004C4785 → `JNE` (75 06) @0x004C4788→0x004C4790 → `FSTP [ESP+0x18]` @0x004C478A → `JMP` (EB 02) @0x004C478E→0x004C4792.
- **Nota D-1:** okno 0x004C4780-0x478F w EXE jest bajt-identyczne z independent_hexdumps.txt:69 — potwierdzony defekt to wyłącznie off-by-one pinu T-26 (D-1 closed as PE-MASTER reading error; w erracie brak twierdzeń o brakujących bajtach).
- **Disposition:** ACCEPTED_AS_ERROR (pin off-by-one).

### F3(d) — GB4/QC-3 (jedna obowiązująca interpretacja + supersession)

**T-27** — `STAGE_ACCEPTANCE_GATES.csv:5` (GB4):
> „deserializat FUN_007453D0 {klucz@+0 pozycja-vec3@+0x50..0x58 wariant@+0x5C}"
- **Poprawka pola (własny dekod):** **pozycja = rec+0x38** (przez FUN_00412430 @0x0074545A); **wariant = u16 @rec+0x34**; trójka +0x50..0x58 = **wektor-drugi** (X2→placement+4 + string tworzenia; Z2 f32→slot5→value+0x98); zbiór typów {0xB0,0xC6,0xC7,**0xB2**} (nie bez 0xB2); „case 0xB9" w kontekście źródła insertów = kanał kluczy/propagacji (kwalifikacja).
- **Disposition:** ACCEPTED_AS_ERROR — **wiersz GB4 = HISTORYCZNY**, superseded przez QC-2/QC-3/[SE-R4-5/6] w tym samym pliku CSV.

**T-28** — `REPORT.md:191-193` (§9):
> „GB4-DATA-SOURCE **PASS** (z korektą [SE-R4-5]: zbiór typów {0xB0,0xC6,0xC7,0xB2}; wiersz CSV był poprawny)"
- **Poprawka:** „wiersz CSV był poprawny" = FAŁSZ na poziomie pól (stare pola +0x50..0x58/0x5C — T-27) i braku 0xB2; sprostowanie: „wiersz CSV GB4 był HISTORYCZNY (stare pola, zbiór bez 0xB2); obowiązująca tabela bramek = QC-2/QC-3 + [SE-R4-5/6] + ERRATA_R5 (mapa supersession — §3 tego dokumentu)".
- **Disposition:** ACCEPTED_AS_ERROR.

**T-29** — `ERRATA_R4.md:199-201` ([SE-R4-5]):
> „Bramka CSV GB4 executora („case 0xB0/0xC6/0xC7→processory placementu") była poprawna — błąd tylko w warstwie SEAM_FLOW_MAP/RESEARCH_FINDINGS §1."
- **Poprawka:** cytany fragment (case→processory) poprawny, ale **CAŁY wiersz GB4 nie był poprawny** (T-27: stare pola + brak 0xB2); kwalifikacja: „poprawna była fraza o case'ach, nie cały wiersz".
- **Disposition:** PARTIAL (fraza OK, wniosek o całości wiersza błędny).

### F3(e) — drobiazgi Fazie A

**T-30** — `PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913/06_REPORT/REPORT.md:124` (§2, macierz wiersz 4):
> „resolver FUN_008544D0: mapa mgr+0x10, lock mgr+0x44, rb-find FUN_00971780"
- **Poprawka:** „hash-map find FUN_00971780 (STLport _Hashtable; `DIV key%(n-1)`)" — „rb-find" = błędna etykieta dla TEJ funkcji.
- **Uzasadnienie:** własny dekod FUN_00971780 (faza B T2_HEX/region 0x971600-0x971D00: `DIV` modulo-haszowanie bucketów, nie drzewo czerwono-czarne).
- **Disposition:** ACCEPTED_AS_ERROR.

**T-31** — `ERRATA_R3.md:127-128` ([SE-9] ŹRÓDŁO):
> „resolver FUN_008544D0: lock mgr+0x44, mapa mgr+0x10, rb-find FUN_00971780" — jw. → hash-map find.
- **Disposition:** ACCEPTED_AS_ERROR (ta sama etykieta w warstwie ERRATA_R3 — superseded).

**T-32** — `REPORT.md:216-219` (§6.4):
> „transform 296445@4508 (D=124.941) istnieje w danych (zweryfikowane bajtowo), ale jego semantyka liczbowa … pozostają NIE ROZSTRZYGNIĘTE"
- **Poprawka:** „liczba f32 124.94100189208984 (bits 0x42F9E1CB) @4508 o NIEUSTALONEJ semantyce (ANCHORS_ABSENT_SEMANTICS_OPEN) — **NIE transform**; pozycje 296445 NIEODZYSKANE".
- **Uzasadnienie:** bez kotwic semantycznych liczba nie może być etykietowana „transform"; pozycje 296445 nadal nieodzyskane dowodem.
- **Disposition:** ACCEPTED_AS_OVERREACH (etykieta „transform").

*NIE-target (utrzymać):* „rb-find FUN_004D1430" (REPORT.md:121, ERRATA_R3:70-71, CSV QC-G4) — lookup rejestru definicji VFS, INNA funkcja; bez nowego dowodu errata jej nie rusza. (Kontekst: HANDOFF.md:53/93 Fazie A już niosą poprawną semantykę D — OK.)

---

## 2. Weryfikacje rozstrzygnięć D-1..D-4 (kontrakt §13)

**D-1** — (zamknięte przez rozstrzygnięcie PE-MASTER przed startem runu): własny re-dump okna 0x004C4770-0x004C479F z FIZYCZNEGO EXE (`01_RAW/X004C4770_479F_D1_WINDOW.txt`) — 16 bajtów @0x004C4780: `d1 df e0 dd d9 f6 c4 41 75 06 d9 5c 24 18 eb 02` — **bajt-identyczne** z independent_hexdumps.txt:69 pakietu Desktop; `dd d9` @0x004C4783-84 potwierdzone. D-1 = błąd odczytu PE-MASTERa (L09); w erracie brak twierdzeń o brakujących bajtach (jw. §0). Status: CLOSED.

**D-2** — „FF D0 @0x004C4744-45" w dispatchu = literówka za **0x004C4874-75**: przy 0x004C4744-45 leżą bajty `05 74` (środek `CMP ESI,5`/`JE` łańcucha wariantów FUN_004C46C0 — własny dekod: `83 FE 05` @0x004C4742-44, `74 0A` @0x004C4745). Właściwy pośredni CALL slotu +0x14 w FUN_004C47F0: `MOV EAX,[EDX+0x14]` @0x004C4871, `FF D0` @0x004C4874 (bajty 0x004C4874-75, stąd stary błędny pin „004C4875"). Status: CONFIRMED_AS_TYPO (dispatch→0x004C4874-75).

**D-3** — piny epilogów FUN_007343E0: własny dekod surowych bajtów (0x00734588-0x007345BA):
- epilog 1: `66 89 5F 24` (MOV WORD [EDI+0x24],BX) @**0x00734597**, `5F` (POP EDI) @0x0073459B, `8B C6` (MOV EAX,ESI) @**0x0073459C**, `5E`/`5B`/`C3` @0x0073459E/9F/A0;
- epilog 2: `66 89 5F 24` @**0x007345B0**, `5F` @0x007345B4, `8B C6` (MOV EAX,ESI) @**0x007345B5**, `5E`/`5B`/`C3` @0x007345B7/B8/B9.
Ogonki `66 89 5F 24; 5F; 8B C6; 5E; 5B; C3` potwierdzone w OBU wyjściach (byte-exact). Desktop pinuje „drugie wyjście @0x007345B4 (MOV EAX,ESI)" — **rozjazd off-by-one: MOV EAX,ESI @0x007345B5** (0x007345B4 = POP EDI); region dispatchu „0x00734596"/„0x007345A5" wskazują bajty POŚREDNIE (ostatni bajt `E8` CALL @0x00734592-96 / ostatni bajt disp `20` FSTP @0x007345A3-A5). Szacunek formalizatora „≈0x007345AF" też off-by-one (mierzone: tail start @0x007345B0). Status: CONFIRMED_TAIL / ROZJAZD na pinach startów (§RAPORT).

**D-4** — literówka „undeoded" @AUDIT_ENTRYPOINT.md:31 offset 3818 → „undecoded"; poprawka w TEJ SAMEJ edycji wiersza co T-08/T-16 (jedna edycja, jawna dysklosura). REPORT.md:34 i §6.3 = zakres-exact, NIE targety (utrzymać). Status: READY (edycja wykonuje publikator).

---

## 3. JEDNA obowiązująca tabela bramek — mapa supersession (F3(d))

Zgodnie z kontraktowym wymaganiem jednej obowiązującej interpretacji dla GB4/QC-3:

| Brameka (istota) | Wiersz HISTORYCZNY (superseded) | Obowiązująca treść |
|---|---|---|
| **GB4-DATA-SOURCE** (źródło danych insertów) | `STAGE_ACCEPTANCE_GATES.csv:5` (GB4): stare pola {klucz@+0, pozycja@+0x50..0x58, wariant@+0x5C}, zbiór typów bez 0xB2, „case 0xB9" bez kwalifikacji | Źródło danych WYKAZANE dla ścieżki procesora FUN_004C47F0 (typy {0xB0,0xC6,0xC7,0xB2}); pozycja=rec+0x38 (FUN_00412430), wariant=u16@rec+0x34; 0xB9 = kanał kluczy/propagacji (kwalifikacja); 5 pozostałych callerów creatora + 8 generatorów kluczy = NIEWYKAZANE (bounded negatyw VFS 1+6+8=0 krawędzi 0x0094xxxx) |
| **QC-3-FIELD-ATTRIBUTION** | `STAGE_ACCEPTANCE_GATES.csv:11` kwalifikator „z sub-kursora" | te same odczyty, ale „z tego samego kursora" (kontynuacja strumienia po strukturze 0x28 w rec+0x0C); atrybucje pól rec+0x38/+0x34 pozostają |

Supersession: stary wiersz GB4 CSV → poprzedzony przez QC-2/QC-3/ERRATA_R4 [SE-R4-5/6] → **ERRATA_R5 (ten dokument) ostatecznie**. Sprostowania: REPORT §9 „wiersz CSV był poprawny" = FAŁSZ (T-28); [SE-R4-5] „Bramka CSV GB4 … była poprawna" = PARTIAL (fraza o case'ach OK, cały wiersz NIE — T-29).

---

## 4. Census żywych kopii (repo-wide scan)

Scan repo `eudoria-clean` (wszystkie pliki tekstowe, w tym obcy `experiments/` — read-only) po fragmenty charakterystyczne T-01..T-32 (`02_ANALYSIS/ERRATA_LIVE_SCAN.json`):
- **LIVE_ELSEWHERE: 0 trafień.**
- Wszystkie trafienia: cele rejestru (IN_REGISTER — dokładne pliki:linie z §1) lub wewnętrzne warstwy pakietów historycznych (HISTORICAL_PACKAGE: probe.json, probe.stdout.txt, PROMPT_OPENCODE.txt, SEAM_FLOW_MAP, RESEARCH_FINDINGS, KEY_MODEL_MATRIX, qc_probe/*.py, RECEIVER_MATRIX, evidence QC — wszystkie wewnątrz zamrożonych pakietów, cytowane/nieżywe).
- Zbiór typów {0xB0,0xC6,0xC7} bez 0xB2 pojawia się wyłącznie w wierszu GB4 (T-27) i cytatach Desktop.
- „0x25 wpisów" pojawia się dodatkowo w `qc_probe/qc_dispatcher.py` (narzędzie QC fazy B — stała zapisu raportu, HISTORICAL_PACKAGE).

**Wniosek:** poprawki ERRATA_R5 wymagają edycji dokładnie JEDNEGO pliku poza pakietami historycznymi: `AUDIT_ENTRYPOINT.md` wiersz 31 (jedna edycja: T-08 + T-16 + literówka D-4). Żadnych innych żywych kopii nie znaleziono.

---

*ERRATA_R5 zamknięte: wszystkie targety T-01..T-32 mają disposition; rejestr zamknięty listą kontraktu; rozszerzenia wyłącznie przez udokumentowane pozycje z osobnym uzasadnieniem (brak w tym runie).*
