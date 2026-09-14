# RUN_CONTRACT — PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913

**Status kontraktu:** sformalizowany (FORMALIZE) 2026-09-13 przez pe-master-auditor na
bezpośrednim dispatchu PE-MASTER. Kontrakt = autorytatywne określenie zakresu, bramek
i celów korekcyjnych runu. Wykonawca (pe-reconstruction) pracuje WYŁĄCZNIE w granicach
tego kontraktu; rozszerzenia zakresu wymagają CORRECTION_REQUEST do PE-MASTER.
**NO_NESTED_TASKS** — wykonawca nie tworzy agentów/podagentów; wynik wraca do PE-MASTER.
**TIMEBOX:** misja czasowa należy do PE-MASTER (właściciel loopa). Wykonawca pracuje do
wykonania zakresu (Faza 1/2/3) lub do udokumentowanej granicy dowodu; CONTEXT_BOUNDARY /
INTERRUPCJA = natychmiastowy zapis RESUME_POINT (stan, następny krok, otwarte rozjazdy)
na dysku + zwrot do PE-MASTER — nie deklarować, że nowa sesja wystartuje sama.

---

## 1. Tożsamość, era, binarium, repo

- **RUN_ID:** `PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913`
- **RUN_CLASS:** LOAD_BEARING
- **TRYB:** **STATIC-ONLY** — klient, Frida, x32dbg, mock-server, sieć, logowanie do
  usług gry: NIEURUCHOMIONE i ZAKAZANE w tym runie. Warstwa „wykonanie silnika-klienta"
  jest NIEOBECNA z definicji trybu — nie maskować jej nieobecności nazwą „oracle".
- **ERA:** EU 9.3.5 (pcg_install). Zakaz transferu semantyki PE2/2003/10.x/Gamebryo 2.3/
  Skyrim na tę erę bez potwierdzenia w JEJ binarium.
- **Binarium:** `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe`
  SHA256 `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31`
  (8 015 872 B; PE32; image base 0x00400000; .text RVA 0x1000 / Raw 0x1000; ASLR OFF).
  **templates.vfs:** `D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs`
  SHA256 `BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77` (560 788 B).
  Obydwa SHA zweryfikowane fizycznie przez PE-MASTER (AUDITOR_COUNTERCHECK) — wykonawca
  MUSI zweryfikować je ponownie własnym S0 fail-closed na starcie (bramka G1).
- **Repo:** `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean`
  **BASE_SHA = `e30f99fdb3c7913c3c4fa6ee1571e505955192d1`** (== origin/master przy
  formalizacji). Status przy formalizacji: czysty POZA obcym `?? experiments/`
  (**NIETYKALNY** — nie stage'ować, nie usuwać, nie absorbować).
- **AUDIT_OUTPUT_ROOT:** `D:\Eudoria_Reconstruction\99_Audits\PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913\`
  (nie istniał przed formalizacją; kolizja sprawdzona przez PE-MASTER i ponownie przez
  formalizera — brak katalogu w `99_Audits\` i w `docs/audits/`).
- **Publikacja (późniejszy krok, po QC i adjudykacji PE-MASTER):**
  `docs/audits/PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913/` — patrz §9.
- **Kontekst nadrzędny (ludzkie zlecenie 2026-09-13, skrót wierny):** kontynuacja badania
  EU 9.3.5 po audycie Desktop faz A/B. GO na OGRANICZONE badanie STATYCZNE + publikację;
  BEZ runtime, mock-servera, modyfikacji klienta. Cel główny: źródło i historyczny
  placement budynku **296445.nif / template 4508**. Trzy fazy: (1) własna adjudykacja
  F1/F2/F3 audytu Desktop z kontrpróbami z oryginalnych bajtów + errata; (2) GŁÓWNY nowy
  eksperyment: kto dostarcza korektę Z (trace FUN_00853A80); (3) powiązanie z celem
  (sub-obiekt +0xC0, rozdzielenie kluczy/ID, tożsamość instancja→model→transform).

## 2. GŁÓWNE PYTANIE (jedno)

**Czy dostawca korekty Z (FUN_00853A80 wywoływany przez managera mapy parametrów
[FUN_004154F0] w ścieżce tworzenia instancji MovableObject) prowadzi do TERENU
(heightfield), i czy TEGO SAMEGO klucza/instancji model łączy TEN SAM transform —
z zachowaniem osobnego pytania o 4508/296445.**

Pytania pomocnicze (F1/F2/F3) służą temu pytaniu; żadne z nich nie zastępuje
rozstrzygnięcia głównego i żadne nie zamyka pytania o statyki bez dodatniego dowodu.

---

## 3. FAZA 1 — własna adjudykacja F1/F2/F3 audytu Desktop + ERRATA_R5

### 3.0 Zasady adjudykacji

- Nie przyjmować audytu Desktop (AUDYT.md / REPORT.md pakietu
  PE_935_ORIGIN_SEAM_DESKTOP_AUDIT_R1_20260913) na autorytet. Powtórzyć decydujące
  próby z ORYGINALNYCH BAJTÓW EXE. Każdemu findingowi Desktopu nadać własny
  disposition: **ACCEPTED / REJECTED / PARTIAL** — z dowodem, nie z liczbą zielonych testów.
- Każdy pin z sekcji 12 (AUDITOR_EXPECTATION) wykonawca MUSI wyprowadzić niezależnie
  własnym dekodem z EXE i raportować ZGODNOŚĆ/ROZJAZD. **Kopiowanie pinów bez własnego
  dekodu = wada metodologiczna (QC_FAIL).** Rozjazd z dowodem jest wynikiem, nie porażką.
- Atrybucja: gałąź korekty Z była już opisana przez wykonawcę fazy B w
  `02_ANALYSIS/SEAM_FLOW_MAP.md` §3. Poprawiany jest BRAK tej gałęzi w końcowej
  syntezie REPORT §1/S8-S9/§5c i w zwięzłych opisach — **nie „nowe odkrycie od zera"**.
  Zachować tę atrybucję w ERRATA_R5 i REPORT.
- Historyczne pakiety (fazy A/B, Desktop, ROUND/RUN*) są NIETYKANE. Poprawiona treść
  żyje w ERRATA_R5 + REPORT tego runu; errata CYTUJE oryginały verbatim (plik:linia) —
  wzorzec pierwszeństwa jak ERRATA_R3/ERRATA_R4 (§3.4).

### 3.1 F1 — GRAMATYKA FUN_007343E0 (deserializacja struktury 0x28 do rec+0x0C)

**Twierdzenie Desktop (do adjudykacji):** FUN_007343E0 odczytuje strukturę z maską u16,
NIE tworzy subkursora; zwraca ten sam kursor wejściowy; pierwszy u16 = maska sterująca
odczytem/podstawianiem floatów, NIE długość podpakietu; dalszy odczyt wariantu i
pozycji kontynuuje ten sam strumień po danych struktury.

Wymagane elementy własnego dowodu:

1. **Pełne ABI z bajtów:** arg1 = kursor (MOV ESI,[ESP+0xC]), arg2 = bufor docelowy
   (MOV EDI,[ESP+0x14] @0x00734416). Caller @0x00745414: `8D 57 0C; 52; 55; E8` →
   destination = **rec+0x0C**. Oba epilogi zakończone `66 89 5F 24; 5F; 8B C6; 5E; 5B; C3`
   (MOV [EDI+0x24],BX; POP EDI; MOV EAX,ESI; POP ESI; POP EBX; RET) — **EAX = TEN SAM
   kursor wejściowy** w obu ścieżkach wyjścia. Zdekodować oba epilogi dokładnie
   (start/koniec każdej instrukcji).
2. **Tabela masek (do wyprowadzenia):** maska u16 @kursor (MOVZX EBX,WORD [EAX+ECX]);
   użyty bit czyszczony (AND EBX,~bit); dla KAŻDEJ pary: bit-0 → FLDZ/FSTP (0.0f),
   bit-1 → FLD1 (1.0f), brak obu → odczyt f32 (FUN_004C32F0); OBA bity pary: gałąź 0
   wygrywa, bit 1 zostaje w reszcie maski:
   - dst+00: 0x002/0x004; dst+08: 0x008/0x010; dst+0C: 0x020/0x040; dst+10: 0x080/0x100;
     dst+14: 0x200/0x400 (ten sam wzorzec);
   - dst+18/+1C/+20: trzy BEZWZGLĘDNE odczyty f32 INLINE (kontrola kursora:
     [ESI+0x11] invalid + bounds [ESI+0xC]+4 vs [ESI+8]; overflow/invalid → FLDZ→0.0f
     zapisane), advance = FUN_0040DE60(4);
   - dst+24 = reszta maski (MOV [EDI+0x24],BX). **dst+04 NIGDY niepisan przez ten
     helper** — rozstrzygnąć, kto (jeśli ktoś) pisze rec+0x10 i kto czyta te pola.
3. **Arytmetyka konsumpcji (do wyprowadzenia):** maska 0 → 34 B (2+8×4); 0x2AA/0x554 →
   po 14 B; 0x7FE → 14 B, reszta 0x554. **NIE utożsamiać maski z długością pakietu ani
   offsetów rec z offsetami strumienia.** Pozycje odczytów wariantu/pozycji w strumieniu
   ZĄLEŻĄ od maski (zmienna konsumpcja struktury).
4. **Census konsumentów:** kto czyta strukturę 0x28 (pola rekordu placementu
   @+0x0C..+0x30, tj. dst+00..dst+24) — census czytelników pól + rozstrzygnięcie dst+04.
   **NIE nazywać pól skalą/prędkością/rotacją/placementem bez konsumenta.**
   FUN_007345C0 = inicjalizacja zerami tej samej szerszej struktury (f90-adjacent;
   8×f32 zero + word@+0x24) — **NIE dowód macierzy 3×3**; etykieta „transform 3×3"
   wymaga konsumenta (patrz T-15).
5. **Pełny FUN_007453D0:** zwrot success, granice bounds/invalid-flag, zachowanie na
   krótkim buforze (fail-closed per pole). NaN/Inf strukturalnie akceptowane —
   **odróżnić: zgodność z historycznym czytnikiem ≠ bezpieczne zasady nowego narzędzia**
   (jeśli wykonawca buduje narzędzie, jego własne walidacje nie muszą powielać
   akceptacji historycznej).
6. **Referencyjny dekoder** — TYLKO run-local (00_CONTROL lub 01_RAW), dopiero PO
   udowodnieniu gramatyki z instrukcji, testowany przeciwko NIEZALEŻNEMU modelowi
   instrukcji (nie przeciwko sobie samemu), **NIE do produkcji** (nie modyfikować
   parsera R61/viewera/prototypu gry).

### 3.2 F2 — KOREKTA Z w FUN_004C46C0 (lokalna kopia rekordu, warianty {3,4,5,6,7})

**Twierdzenie Desktop (do adjudykacji):** FUN_004C46C0 robi lokalną kopię rekordu
([ESP+0x10]=rec+8=pos.x, [ESP+0x14]=rec+0xC=pos.y, [ESP+0x18]=rec+0x10=pos.z, dalej
rotacja/param-sety); dla wariantów {3,4,5,6,7} przed konstruktorem:
`h = f32(FUN_00853A80(manager, pos.x, pos.y, 0, 0))`; korekta trzeciej składowej tylko
przez porównanie x87 (z FSTP ST(1)); rekord callera NIE jest nadpisywany — zmiana
dotyczy kopii podanej konstruktorowi.

Wymagane elementy własnego dowodu:

1. **Łańcuch wariantów:** CMP ESI,3 (flagi)→JE@0x004C473B→0x004C4751; CMP ESI,6
   @0x004C473D; CMP ESI,5; CMP ESI,4; CMP ESI,7 @0x004C474C; JNE@0x004C474F→0x004C4792
   (skip) — korekta TYLKO dla {3,4,5,6,7}.
2. **Korekta (do wyprowadzenia bajtowo):** FLD [ESP+0x14](pos.y)@0x004C4751; PUSH 0;
   PUSH 0; SUB ESP,8; FSTP [ESP+4](pos.y); FLD [ESP+0x20](=pos.x po przesunięciu stosu —
   **zweryfikuj sam z arytmetyki stosu**)@0x004C4760; FSTP [ESP](pos.x);
   CALL FUN_004154F0 (manager)@0x004C4767 (E8 84 0D F5 FF); MOV ECX,EAX@0x004C476C;
   CALL FUN_00853A80 @0x004C476E (E8 0D F3 38 00) — argumenty
   (this=manager, pos.x, pos.y, 0, 0) __thiscall RET 0x10.
3. **Porównanie x87 (do wyprowadzenia bajtowo):** FSTP [ESP+0x44](h)@0x004C4773;
   FLD [ESP+0x18](z_copy)@0x004C4777; FLD [ESP+0x44](h)@0x004C477B;
   FCOM ST(1)@0x004C477F (D8 D1); FSTSW AX@0x004C4781 (DF E0);
   **FSTP ST(1)@0x004C4783 (DD D9)**; TEST AH,0x41@0x004C4785;
   JNE@0x004C4788→0x004C4790 (FSTP ST(0) DD D8 = odrzucenie h; pamięć [ESP+0x18]
   zostaje z); fall-through: FSTP [ESP+0x18]@0x004C478A (zapis h);
   JMP@0x004C478E→0x004C4792; PUSH 0x128 (new)@0x004C4792; ctor CALL
   FUN_00528E50@0x004C47C1 (E8 8A 46 06 00).
4. **PEŁNA tabela x87 (OBOWIĄZKOWA):** każda kombinacja {z, h} × {equal, less, greater,
   unordered, ±Inf po obu operandach, ±0} — każda komórka: flagi C0/C2/C3, wynik
   TEST AH,0x41 (maska C0|C3), gałąź (JNE taken / fall-through), wynikowy z' W BITACH
   (nie tylko wartość — uwaga na equal: z'=z oznacza BITY z, nie h; +0/−0; payload NaN).
   Semantyka oczekiwana (do niezależnego potwierdzenia): z'=h wtw h>z (ordered,
   porównywalne); z=h (equal, C3=1) → z'=z (te same BITY); h<z → z'=z; NaN(h) → z'=z
   (ROŻNIE od Math.max — Math.max(z,NaN)=NaN); NaN(z) → z'=NaN (bity z); ±Inf zgodnie
   z porządkiem total na rozszerzonych wartościach FCOM. **NIE ogłaszać równoważności
   z Math.max dla wszystkich bitów.**
5. **Cztery stany pozycji (świadki, jawnie SYNTHETIC):** raw position (bajty kursora) →
   f90 record (placement +8/+0xC/+0x10) → corrected local copy ([ESP+0x10..0x18] w
   FUN_004C46C0, z' w [ESP+0x18]) → instance +0x44..0x4C (ctor kopiuje z poprawionej
   kopii). Suita: warianty objęte/nieobjęte ({3..7} vs pozostałe), z<h / z=h / z>h,
   helper niedostępny, wartości niefinitywne.
6. **CREATE vs EXISTING — OSOBNE mapy warunków i zapisów:** setter pozycji w EXISTING
   **nie jest bezwarunkowy** — zdekodować ścieżkę warunków FUN_0085B3E0 (wcześniejszy
   pośredni CALL slotu +0x14 = FF D0 — patrz §12.3 i rozjazd D-2) oraz warunki, pod
   którymi pozycja jest aktualizowana.
7. **Helper niedostępny:** sprawdzić, co zwraca FUN_004154F0 przy braku inicjalizacji
   (lazy-init; porażka new?) i czy FILTER (FUN_00755F90) może odrzucić → wtedy h=0.0
   → rozpisać wpływ na z' (wartościowo z'=max(z,0), ale bitowo z zachowuje bity z
   przy braku ścisłej przewagi h — tabela z pkt 4 rozstrzyga każdą komórkę).
8. **Wartości niefinitywne:** osobno zdystryngować zachowanie dla ±Inf/±0/NaN w każdym
   stanie łańcucha (4 stany).

### 3.3 F3 — ZAKRES STATYKÓW + drobne korekty (ERRATA_R5)

Zasady korekty narracji (efekty w ERRATA_R5 — rejestr targetów §3.4):

- **(a) Statyki:** każdy żywy skrót przenoszący „ten kanał ich nie obejmuje" zamienić
  na: **„użycie przez 4508/296445 NIEWYKAZANE w tym kanale, pozostaje OPEN"**. Zachować
  wyróżnienia: nazwa klasy MovableObject ≠ klasyfikacja danych zasilających; brak
  dowiedzionego połączenia ≠ wykluczenie; raw census E8 bez krawędzi 0x0094xxxx NIE
  rozstrzyga przepływu pośredniego z pliku.
- **(b) Źródło insertów:** „Źródło insertów = komunikaty" ograniczyć do WYKAZANEJ
  ścieżki procesora (4 callery FUN_004C47F0 + creator funnel 1+6+8 jako census negatywu
  VFS) — BEZ uogólnienia na 6 callerów creatora i 8 generatorów kluczy jako źródeł
  danych (bez pozytywnego dowodu ich źródła danych pozostają OPEN).
- **(c) Piny P3:** CALL FUN_0085B3E0 @0x004C488A (E8 51 6B 39 00); guard CALL
  FUN_0085B750 @0x004C4878 (E8 D3 6E 39 00); rotation CALL FUN_0085ADB0 @0x004C4896
  (E8 15 65 39 00); wcześniejszy pośredni CALL slotu +0x14: MOV EAX,[EDX+0x14]
  @0x004C4871, FF D0 @0x004C4874 (stąd pochodził stary błędny pin „004C4875");
  dispatcher: byte-table indeksy 0xA2..0xC7 = **38** (CMP EAX,0x25 = maks. indeks 37,
  nie 37 wpisów), jump-table osobno **22** wpisy.
- **(d) GB4/QC-3 (supersession):** opublikować **JEDNĄ obowiązującą tabelę bramek**
  z mapą supersession: stary wiersz GB4 CSV = HISTORYCZNY, poprzedzony przez
  QC-2/QC-3/ERRATA_R4 [SE-R4-5/6] — i sprostować REPORT §9 „wiersz CSV był poprawny"
  oraz [SE-R4-5] „Bramka CSV GB4 … była poprawna" (wiersz niósł stare pola i zbiór
  typów bez 0xB2 — patrz T-27/T-28/T-29).
- **(e) Drobiazgi Fazie A:** „rb-find" dla FUN_00971780 → poprawnie **hash-map find**
  (STLport _Hashtable, DIV key%(n−1)); „transform 296445 (D=124.941)" → **liczba f32 o
  nieustalonej semantyce (ANCHORS_ABSENT_SEMANTICS_OPEN), nie transform**. UWAGA:
  etykieta „rb-find FUN_004D1430" (lookup rejestru definicji VFS) to INNA funkcja —
  NIE jest targetem bez nowego dowodu.
- **Wszystkie liczby po korekcie wyprowadzone WŁASNYM narzędziem** (nie przepisane z
  audytu Desktop ani z raportów fazy A/B).

### 3.4 REJESTR TARGETÓW ERRATA_R5 (autorytatywny; ERRATA_R5.md cytuje każdy verbatim: plik:linia)

Wzorzec: ERRATA_R3/ERRATA_R4 — historyczne pakiety NIETYKANE; errata cytuje STARE
verbatim (plik:linia), poprawiona treść żyje w ERRATA_R5 + REPORT tego runu; kolejność
wiążącości: (a) evidence 01_RAW/02_ANALYSIS (nietknięte), (b) ERRATA_R4, (c) ERRATA_R5
(ten run), (d) raporty historyczne czytane przez pryzmat (b)+(c); piny VA = START
instrukcji (konwencja ERRATA_R3 reguła 5 / ERRATA_R4 reguła 5).

**F1 — framing „sub-kursor/sub-pakiet u16-header" (gramatyka 007343E0):**

- **T-01** `PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/REPORT.md:52` (S6):
  > „sub-kursor (FUN_007343E0 @0x00745419, u16-header); wariant u16 @0x00745435→rec+0x34"
  — poprawnie: FUN_007343E0 czyta strukturę 0x28 z maską do rec+0x0C; brak
  zagnieżdżonego kursora; wariant/pozycja kontynuują TEN SAM strumień po strukturze.
- **T-02** ten sam wiersz S6 — całe grupowanie wariant/pozycja/rotacja/wektor-2/bajt
  jako zawartość „sub-kursora"; poprawnie: kolejne odczyty z tego samego kursora po
  zmiennej konsumpcji struktury (pozycje w strumieniu zależą od maski).
- **T-03** `PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/REPORT.md:30` (§1):
  > „deserializacja FUN_007453D0 z sub-pakietu kursora: vec3 12 B → setter f90 →
  > rekord placementu +8/+0xC/+0x10 → ctor kopiuje do instancji +0x44..0x4C"
  — F1 (framing „sub-pakietu kursora") + F2 (brak korekty z' przed ctor).
- **T-04** `PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/QC_REPORT.md:46-49`
  (§1c): > „sub-kursor: FUN_007343E0 @0x00745419 (u16-header sub-pakietu → zagnieżdżony
  kursor @rec+0xC)" + kwalifikatory „(z SUB-kursora)" przy wariant/pozycja/rotacja/
  wektor-2/bajt (linie 49-57 tej sekcji).
- **T-05** `PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/ERRATA_R4.md:73-77`
  ([SE-R4-1] (ii)): > „sub-pakiet (FUN_007343E0 @0x00745419): **wariant u16** …
  **POZYCJĘ vec3 3×dword** …" — grupowanie pól po FUN_007343E0 jako „sub-pakietu".
- **T-06** `PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/ERRATA_R4.md:97`
  ([SE-R4-1] ŹRÓDŁO): > „FUN_007343E0 (sub-kursor u16-header)".
- **T-07** `PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/STAGE_ACCEPTANCE_GATES.csv:11`
  (QC-3): kwalifikator „z sub-kursora" — poprawnie: z tego samego kursora (kontynuacja
  strumienia). (Atrybucje pól rec+0x38 / u16@rec+0x34 w QC-3 pozostają — są poprawne.)
- **T-08** `AUDIT_ENTRYPOINT.md:31` (wiersz LATEST RUNS, fragment ~offset 1500):
  > „sub-packet via FUN_007343E0: variant u16 @0x00745435 -> rec+0x34, POSITION vec3
  > 12B via FUN_00412430 @0x0074545A -> rec+0x38" — jw.; przy okazji tej samej edycji
  wiersza poprawić literówkę „undeoded" (→ „undecoded"; rozjazd D-4).
- Kontekst cytowany jako STARE (warstwa evidence/robocza, nietykana, już
  sformalizowana w ERRATA_R4): `SEAM_FLOW_MAP.md:68` (pominięcie 007343E0 w §4) oraz
  `RESEARCH_FINDINGS.md:20/73` (stare pola +0x50..0x58).

**F2 — brak gałęzi korekty Z w końcowej syntezie:**

- **T-09** `PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/REPORT.md:27-34` (§1):
  łańcuch „…vec3 12 B → setter f90 → rekord placementu +8/+0xC/+0x10 → ctor kopiuje do
  instancji +0x44..0x4C" pomija korektę z' w lokalnej kopii FUN_004C46C0 dla wariantów
  {3..7} (h z FUN_00853A80; zapis h tylko przy h>z ordered).
- **T-10** `PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/REPORT.md:54` (S8):
  > „create FUN_004C46C0(placement, u16-wariant, string, 1) @0x004C4952 … → new(0x128)
  > @0x004C4792 → ctor FUN_00528E50 @0x004C47C1" — brak kroku korekty między kopią
  rekordu a new (dla {3..7}).
- **T-11** `PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/REPORT.md:55` (S9):
  > „**`[+0x44..0x4C]=[record+8..0x10]`** (FUN_00746560)" — „record" = poprawiona
  kopia lokalna (z'), nie surowy deserializat; kwalifikacja wymagana.
- **T-12** `PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/REPORT.md:97` (§4,
  wiersz „Pozycja z kursora → placement+8..0x10 → instancja+0x44..0x4C"): brak korekty
  + pin „FUN_0085B3E0 @0x004C4875" (poprawnie @0x004C488A — patrz T-21).
- **T-13** `PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/REPORT.md:120-124`
  (§5c): > „(c) Skąd jest TRANSFORM (movable)? — z bajtów KURSORA komunikatu (S6:
  sub-pakiet vec3 12 B → f90)." — niepełne dla wariantów {3..7} (z w instancji = z'
  po korekcie max(z,h), nie surowy bajt kursora; NaN ≠ Math.max).
- **T-14** `PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/HANDOFF.md:18-28`:
  zdanie-odpowiedź bez kroku korekty („setter f90 pisze pozycję do rekordu placementu
  +8/+0xC/+0x10, ctor kopiuje ją do instancji…").
- **T-15** `PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/ERRATA_R4.md:127-128`
  ([SE-R4-2]): > „+0x14..0x3B transform 3×3+flaga word @+0x24 (FUN_007345C0)" —
  „macierz 3×3" = etykieta bez konsumenta; FUN_007345C0 zeruje 8×f32+word (kształt
  zgodny ze strukturą FUN_007343E0), NIE dowód macierzy 3×3. (Analogiczna etykieta w
  `SEAM_FLOW_MAP.md:29` = warstwa evidence — cytowana jako STARE.)
- **Atrybucja do zachowania:** `SEAM_FLOW_MAP.md:46` (§3) już zawiera gałąź
  („jeśli wariant∈{3,4,5,6,7}: FUN_004154F0(mgr) → FUN_00853A80(mgr, 2×f32) →
  max(rekord[4], wynik)") — ERRATA_R5 cytuje jako źródło atrybucji; poprawiana jest
  końcowa synteza, nie odkrycie od zera. (Nota: „max(rekord[4], wynik)" wymaga
  kwalifikacji semantyki x87 — tabela §3.2 pkt 4.)

**F3(a) — statyki (żywe skróty o zbyt mocnym zakresie):**

- **T-16** `AUDIT_ENTRYPOINT.md:31` (wiersz LATEST RUNS, fragment ~offset 3500):
  > „STATICS (4508/296445) NOT covered by the movable channel (OPEN; the 296445
  > positions NOT recovered; D@4508 = 124.941 ANCHORS_ABSENT_SEMANTICS_OPEN unchanged)"
  → „USE BY 4508/296445 NOT DEMONSTRATED in this channel; remains OPEN (the 296445
  positions NOT recovered; D@4508 = 124.941 ANCHORS_ABSENT_SEMANTICS_OPEN unchanged)".
- **T-17** `PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/HANDOFF.md:27-28`:
  > „STATYKI (4508/296445) NIE objęte tym kanałem; pozycje 296445 NIEODZYSKANE."
  → „użycie przez 4508/296445 NIEWYKAZANE w tym kanale, pozostaje OPEN; pozycje
  296445 NIEODZYSKANE."
- **T-18** commit message 78cd153 (historia git, nietykalny; cytowany jako STARE):
  „STATICS (4508/296445) NOT covered by the movable channel (OPEN…)" — żywa kopia tego
  sformułowania = T-16 (entrypoint).
- **Wzorce poprawne (utrzymać, NIE targety):** `REPORT.md:138-140` (§6.3: „statyki
  (4508/296445) NIE wykazane w tym kanale") i `REPORT.md:34` (§1: „NIE zostały objęte
  tym kanałem w tym runie") — zakres-exact; Desktop jawnie pochwalił §6.3.
- Źródło cytatu Desktop (przekazany werdykt): „Dla statyków (4508/296445): UNKNOWN —
  ten kanał ich nie obejmuje." — drugie zdanie mocniejsze od dowodu; korekta jak (a).

**F3(b) — „Źródło insertów = komunikaty" (ograniczenie do wykazanej ścieżki):**

- **T-19** `PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/REPORT.md:99` (§4):
  > „Źródło insertów = komunikaty (VFS=negatyw)" → „źródło danych insertów WYKAZANE
  dla ścieżki procesora FUN_004C47F0 (4 callery: 0xB0/0xC6/0xC7/0xB2); 5 pozostałych
  callerów creatora (FUN_00456F40/FUN_0050BED0/FUN_00442190/FUN_00441910/FUN_004B3A00)
  i 8 generatorów kluczy = źródła danych NIEWYKAZANE (bounded negatyw VFS: census
  funnelu 1+6+8 = 0 krawędzi z 0x0094xxxx)".
- **T-20** `PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/STAGE_ACCEPTANCE_GATES.csv:5`
  (GB4): > „Zrodlo insertu = KOMUNIKATY: dispatcher FUN_004B18D0 switch(typ) case
  0xB9->FUN_005B72C0 @0x004B1A16 (pin E8 A5 58 10 00) case 0xB0/0xC6/0xC7->processory
  placementu" — jw. + case 0xB9 w kontekście źródła insertów wymaga kwalifikacji
  (kanał kluczy/propagacji, nie deserializacji pozycji) + brak 0xB2 (T-27).

**F3(c) — piny P3 (stary pin „004C4875"):**

- **T-21** `PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/QC_REPORT.md:75-77`
  (§1d): > „FUN_0085B3E0(istniejąca_wartość, &[rec+0x38], 1) @0x004C4875" →
  @0x004C488A; guard @0x004C4878→FUN_0085B750; rotation @0x004C4896→FUN_0085ADB0;
  „@0x004C4875" = ostatni bajt 2-bajtowego FF D0 wcześniejszego pośredniego CALL slotu
  +0x14 (MOV EAX,[EDX+0x14] @0x004C4871; FF D0 @0x004C4874 — bajty 0x004C4874-75).
- **T-22** `PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/ERRATA_R4.md:102-104`
  ([SE-R4-1] KONTRTEST (4)): > „FUN_0085B3E0(istniejąca, &[rec+0x38], 1) @0x004C4875" — jw.
- **T-23** `PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/ERRATA_R4.md:225-229`
  ([SE-R4-6] KONTRTEST): > „FUN_0085B3E0(istniejąca, &[rec+0x38], 1) @0x004C4875" — jw.
- **T-24** `PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/REPORT.md:97` (§4):
  pin „FUN_0085B3E0 @0x004C4875" — jw. (ten sam wiersz co T-12).
- **T-25** `PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/REPORT.md:171` (§7):
  > „byte-table dispatchera: 0x25 wpisów (0xA2..0xC7), jump-table: **22** wpisów" →
  „byte-table: 38 INDEKSÓW (0xA2..0xC7; CMP EAX,0x25 = maks. indeks 37), jump-table:
  22 wpisy".
- **T-26** pakiet Desktop `PE_935_ORIGIN_SEAM_DESKTOP_AUDIT_R1_20260913/AUDYT.md:55`
  (== REPORT.md:55 — pliki identyczne; pakiet historyczny: cytować, NIE edytować):
  > „porównanie x87 i warunkowy `FSTP [ESP+0x18]` przy **004C4789**" — off-by-one:
  FSTP [ESP+0x18] = D9 5C 24 18 @**0x004C478A** (0x004C4789 = bajt disp JNE 75 06
  @0x004C4788-89); pełny łańcuch: FCOM@0x004C477F, FSTSW@0x004C4781,
  FSTP ST(1)@0x004C4783, TEST@0x004C4785, JNE@0x004C4788→0x004C4790,
  FSTP[ESP+0x18]@0x004C478A, JMP@0x004C478E→0x004C4792.

**F3(d) — GB4/QC-3 (jedna obowiązująca interpretacja + supersession):**

- **T-27** `PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/STAGE_ACCEPTANCE_GATES.csv:5`
  (GB4): > „deserializat FUN_007453D0 {klucz@+0 pozycja-vec3@+0x50..0x58 wariant@+0x5C}"
  — STARE pola (poprawne: pozycja=rec+0x38 przez FUN_00412430; wariant=u16@rec+0x34;
  trójka +0x50..0x58 = wektor-drugi: X2→placement+4+string, Z2→slot5→value+0x98)
  + zbiór typów bez 0xB2 + „case 0xB9" w kontekście źródła insertów — wiersz =
  HISTORYCZNY, superseded przez QC-2/QC-3/[SE-R4-5/6] w tym samym pliku CSV.
- **T-28** `PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/REPORT.md:191-193`
  (§9): > „GB4-DATA-SOURCE **PASS** (z korektą [SE-R4-5]: zbiór typów
  {0xB0,0xC6,0xC7,0xB2}; wiersz CSV był poprawny)" — „wiersz CSV był poprawny" = FAŁSZ
  na poziomie pól i braku 0xB2 (T-27); sprostowanie + JEDNA obowiązująca tabela bramek
  z mapą supersession.
- **T-29** `PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/ERRATA_R4.md:199-201`
  ([SE-R4-5]): > „Bramka CSV GB4 executora („case 0xB0/0xC6/0xC7→processory
  placementu") była poprawna — błąd tylko w warstwie SEAM_FLOW_MAP/RESEARCH_FINDINGS
  §1." — cytowany fragment poprawny, ale CAŁY wiersz GB4 nie był (T-27);
  kwalifikacja wymagana.

**F3(e) — drobiazgi Fazie A:**

- **T-30** `PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913/06_REPORT/REPORT.md:124`
  (§2, macierz wiersz 4): > „resolver FUN_008544D0: mapa mgr+0x10, lock mgr+0x44,
  rb-find FUN_00971780" → „hash-map find FUN_00971780 (STLport _Hashtable; DIV
  key%(n−1))" — „rb-find" = błędna etykieta dla TEJ funkcji.
- **T-31** `PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913/06_REPORT/ERRATA_R3.md:127-128`
  ([SE-9] ŹRÓDŁO): > „rb-find FUN_00971780" — jw.
- **T-32** `PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913/06_REPORT/REPORT.md:216-219`
  (§6.4): > „transform 296445@4508 (D=124.941) istnieje w danych (zweryfikowane
  bajtowo), ale jego semantyka liczbowa … pozostają NIE ROZSTRZYGNIĘTE" → „liczba f32
  124.94100189208984 (bits 0x42F9E1CB) @4508 o NIEUSTALONEJ semantyce
  (ANCHORS_ABSENT_SEMANTICS_OPEN) — NIE transform; pozycje 296445 NIEODZYSKANE".
- **NIE-target:** „rb-find FUN_004D1430" (REPORT.md:121, ERRATA_R3:70-71, CSV QC-G4)
  — lookup rejestru definicji VFS, INNA funkcja; bez nowego dowodu errata jej nie rusza.
  (Kontekst: HANDOFF.md:53/93 Fazie A już niosą poprawną semantykę D — OK.)

Rejestr jest zamknięty listą T-01..T-32; wykonawca może DODAĆ cel/linie wyłącznie
przez udokumentowane rozszerzenie w ERRATA_R5 z osobnym uzasadnieniem; NIE wolno
pominąć żadnego T-xx bez disposition (cytat verbatim + poprawka + uzasadnienie).

---

## 4. FAZA 2 — GŁÓWNY NOWY EKSPERYMENT: KTO DOSTARCZA KOREKTĘ Z (FUN_00853A80)

Trace FUN_00853A80 — **NIE** ogólny katalog funkcji sieciowych. Zakres:

1. **Receiver managera z FUN_004154F0:** zidentyfikować klasę managera (singleton
   [0x00BA12E8], lazy PUSH 0x8C). RTTI jeśli ma vtable; może NIE mieć vtable — wtedy
   identyfikacja po konstruktorach/writerach (uzasadnić metodę). Pola do rozliczenia:
   +0 (provider1), +0x10 hash_map, +0x2C..+0x40 druga struktura, +0x44 CS,
   +0x4C (provider2), +0x50 (receiver FUN_00413340 — rozszyfrować rolę),
   +0x58..+0x84 12 floatów (pole filtra?).
2. **Writerzy wskaźników manager+0 (provider1) i manager+0x4C (provider2):** census
   zapisów (MOV [reg+0]/[reg+0x4C] z reg z singleton-gettera; init-funkcje;
   rejestracje) → rzeczywiste klasy (RTTI TD→COL→vtable) + ciała vtable **slot +4**
   obu dostawców (dekompilat + bajty). Bez tego trace jest UNPROVEN na krawędzi
   wirtualnej.
3. **Operacje/argumenty/zwrot OBU dostawców:** które wywołanie zasila wynik zwrotny
   FUN_00853A80; skutki uboczne provider2 (co robi z L0/L1 = pos.x/pos.y — modyfikuje?
   zapisuje? zwraca przez lokalne?); kiedy fallback 0.0 (provider1==NULL → JE → FLDZ →
   return 0.0; filter-fail → return 0.0); co dokładnie filtruje FUN_00755F90 (dekod
   pełny + jego własne pola; this=manager+0x58 [LEA ECX,[ESI+0x58]], arg=&L0 — czy
   bounds-check na manager+0x58..0x84?); semantyka FUN_00413340 (this=[ESI+0x50] —
   lock/acquire? release?) — dwie formy wywołania slotu +4 provider1
   (@~0x00853B07 / ~0x00853B3x zależnie od arg3 — rozpisz obie).
4. **KONKURENCYJNE HIPOTEZY (obowiązkowo wszystkie trzy):**
   - **H-TERRAIN** (heightfield/teren), **H-COLLISION** (podłoże/kolizja),
     **H-OTHER** (inny provider: scenka/fizyka/proxy).
   - Dla KAŻDEJ: przewidywania rozstrzygające + falsyfikacja (co dokładnie w bajtach/
     RTTI/łańcuchu danych ją rozstrzygnie). **NAZWY funkcji, liczby wyglądające jak
     współrzędne, x/y jako argumenty NIE WYSTARCZAJĄ.**
5. **Jeśli dostawca prowadzi do terenu:** udowodnić PEŁNY łańcuch
   receiver→konkretny dataset/loader→indeksowanie próbki→interpolacja→wynik.
   Osie/jednostki TYLKO tam, gdzie wynikają z przeliczeń/kontraktu.
   **NIE przypisywać wcześniej odzyskanej heightmapy (50.bnt/field decode) temu
   providerowi NA PODOBIEŃSTWO — potrzebny łańcuch, nie zbieżność liczb.**
6. **Nierozwiązany virtual call:** zakończyć krawędź jako **UNPROVEN** z listą realnych
   kandydatów + testem rozróżniającym. **NIE domykać przez RTTI innej gry/ery.**
7. **Anti-leak:** bramka fazy 2 (G5) NEUTRALNA — predykat nie zawiera wbudowanego
   „terrain"; PASS nie zależy od tego, KTÓRA hipoteza wygra.

## 5. FAZA 3 — POWIĄZANIE Z CELEM (jedna pełna ścieżka; NIE otwierać 19 ctor-callers naraz)

1. **ClientMovableObject sub-obiekt +0xC0:** FUN_005247C0→FUN_00509330 + rzeczywiste
   argumenty tworzenia (create arg3 = pusty string przez singleton [0x00BA26B8] —
   zweryfikować: FUN_004C4640 ignoruje argumenty i zwraca singleton; FUN_00765930
   zwraca wskaźnik stringa). Zdekodować, czym jest sub-obiekt i jaka ścieżka z niego
   prowadzi.
2. **Rozdzielenie kluczy/ID (tabela z osobnymi kolumnami: źródło → konsument → dowód):**
   instance key (+0x74), parent key, class/param-set ID (+0x88), template ID (rekord
   VFS), model resource ID, string — **TEN SAM numer/offset ≠ ta sama rola.**
3. **Tożsamość instancja→model→transform:** ustalić, czy TA konkretna instancja osiąga
   znaną ścieżkę modelu/NiAVObject (RUN3: pump {0x66=MODEL,A} →
   ArkModelResourceInstanceRef → FUN_006cb020 „<id>__<name>" → registration) i czy
   TEN SAM transform (pozycja SKORYGOWANA — z', nie surowa) do niej trafia.
   **WYMAGAĆ tożsamości wskaźnika lub udowodnionego lookupu — NIE sąsiedztwa wywołań.**
4. **4508/296445:** włączyć TYLKO po dodatnim dowodzie, że ich definicja korzysta z
   tej ścieżki. Brak połączenia w badanym zakresie → **OPEN** + wskazać JEDNĄ
   alternatywną ścieżkę wspólnych funkcji z uzasadnieniem (bez ogłaszania „budynki
   są gdzie indziej").
5. **Upstream ArkClientPacketExecutor/ring = backlog**, chyba że trace tej fazy
   wymaga JEDNEJ krawędzi producenta — wtedy dokładnie tę jedną.

---

## 6. WERYFIKACJA (wymogi testowe)

1. **Pełna lektura nośnych źródeł** z wpisem zakresu do FULL_READ_LOG (od wejścia do
   wszystkich wyjść); nagłówki/search-hits NIE są pełną lekturą.
2. **Rozdzielenie warstw (jawne w każdym twierdzeniu):** oryginalne bajty /
   disassembly / dekompilat / hipoteza / model syntetyczny / wykonanie silnika-klienta.
   Ostatnia warstwa = NIEOBECNA (STATIC-ONLY); NIE maskować jej nazwą „oracle".
   Świadki SYNTHETIC oznaczone jawnie; bez historycznych pakietów nie udawać
   corpus evidence.
3. **Suita masek FUN_007343E0:** 0, 0x2AA, 0x554, 0x7FE, KAŻDA para bitów oddzielnie,
   oba bity pary, bity nieużywane (0x800+), krótki bufor przed/po polu, dwa rekordy
   kolejno, końcowy offset kursora, dst+04 przed/po, NaN/Inf — porównywać **STAN
   KURSORA i ZAKRES ZAPISÓW** (nie tylko return success).
4. **Suita pozycji (F2):** warianty objęte/nieobjęte; z<h / z=h / z>h; helper
   niedostępny (manager/filter → h=0.0); wartości niefinitywne; cztery stany łańcucha;
   CREATE i EXISTING osobne mapy warunków i zapisów.
5. **Klucze/model (Faza 3):** kontrola pozytywna; kontrola innego receivera/klucza;
   kontrola braku lookupu; ≥1 realny łańcuch callera.
6. **Publikacja:** manifest plików = istnieją + SHA zgodne na commicie i po push;
   manifest bez self-row (precedens L12); unikalne ścieżki; brak stale rows.
7. **Przed/po:** oryginały i pakiety historyczne byte-identical (wzorzec GB6:
   composite + per-plik before==after); obce `experiments/` i `src/game/` nietknięte;
   porty 8000/9350 bez ingerencji.
8. **Determinizm:** skrypty hashowane po ostatniej edycji PRZED wykonaniem
   (SCRIPT_SHA256.csv); wyniki bez timestampów; manifesty GHIDRA_LOCAL AT_COPY + FINAL
   per MANIFEST_VALIDATION_ORDER (ERRATA_R3 reguła 4).

## 7. BRAMKI (STAGE_ACCEPTANCE_GATES.csv; wzór CSV z fazy B)

Kolumny: `gate_id,status,evidence_count,measured_quantity,independent_source,
why_non_circular,failure_case_detected,boundary`.
Statusy: PASS / FAIL + klasy non-pass: **PARTIAL / UNPROVEN / OPEN / BLOCKED**.

**HARD_STOP (natychmiastowy stop + raport do PE-MASTER, bez pracy downstream):**
(i) SHA/rozmiar mismatch Entropia.exe lub templates.vfs vs §1; (ii) kolizja katalogu
RUN_ID (katalog istnieje); (iii) wykryta mutacja oryginałów/archiwów/pakietów
historycznych; (iv) obca staged ścieżka nakładająca się na cele → raport konfliktu,
NIE odpinać/absorbować.

- **G1-ERA** — S0 fail-closed własnym skryptem: SHA256+rozmiary obu oryginałów == §1;
  PE32 base 0x00400000; ASLR OFF; .text RVA/Raw 0x1000; ≥10 spot-check VA→offset.
  FAIL → HARD_STOP(i). measured_quantity: 2×SHA+rozmiary+spot-checki;
  independent_source: własny odczyt pliku (nie relacja); why_non_circular: odczyt
  pierwotny, mismatch = exit 1 bez downstream; failure_case: jak wyżej; boundary: —.
- **G2-F1-GRAMMAR** — (a) własny dekod bajtowy FUN_007343E0: ABI (arg1=kursor,
  arg2=destination), tabela masek (obie gałęzie każdej pary), 3 odczyty bezwzględne
  inline, residual@dst+24, dst+04 niepisan, oba epilogi EAX==kursor-wejściowy;
  (b) suita masek (§6 pkt 3) wykonana i porównana z NIEZALEŻNYM modelem instrukcji
  (nie własny dekoder sam ze sobą); (c) census czytelników struktury (pola
  rec+0x0C..0x30) + rozstrzygnięcie dst+04; (d) pełny FUN_007453D0 (zwrot success,
  krótki bufor). PASS wymaga (a)-(d) CONFIRMED własnymi bajtami; brak elementu →
  PARTIAL z granicą. measured_quantity: tabela masek + N przypadków suity (kursor
  state + write range); independent_source: EXE vs niezależny model instrukcji;
  failure_case: krótki bufor/oba bity/maska 0x7FE muszą dać mierzalne różnice;
  boundary: semantyka pól bez konsumenta = OPEN.
- **G3-F2-X87** — (a) pełna tabela x87 (każda komórka: C0/C2/C3 + gałąź + wynik
  bitowy); (b) cztery stany pozycji (świadki SYNTHETIC oznaczone); (c) mapa CREATE i
  mapa EXISTING (warunki FUN_0085B3E0 zdekodowane); (d) zbiór wariantów objętych/
  nieobjętych; (e) helper-niedostępny (FUN_004154F0 przy braku init; filter-fail →
  h=0.0 → wpływ na z'); (f) atrybucja SEAM_FLOW_MAP §3 zachowana w ERRATA_R5/REPORT.
  failure_case: NaN(h) musi dawać z'=z (≠Math.max) — mierzalny rozróżnik; boundary:
  brak runtime = tabela jest modelem instrukcji, nie pomiarem procesora.
- **G4-F3-ERRATA** — każdy target T-01..T-32: cytat verbatim (plik:linia) + poprawione
  sformułowanie + disposition; JEDNA obowiązująca tabela bramek z mapą supersession
  (T-27/T-28/T-29); liczby wyprowadzone własnym narzędziem; historyczne pakiety
  byte-identical (zależność z G7). failure_case: brak dowolnego T-xx lub nie-verbatim
  cytat = FAIL.
- **G5-P2-PROVIDER** — manager zidentyfikowany klasowo (RTTI lub
  konstruktorzy/writerzy z uzasadnieniem) ORAZ providerzy (writerzy mgr+0/mgr+0x4C)
  zidentyfikowani klasowo + ciała slot +4 zdekodowane ORAZ fallback (provider1==NULL,
  filter-fail) + FUN_00755F90 + FUN_00413340 zdekodowane — **LUB** krawędź zakończona
  jako UNPROVEN z listą realnych kandydatów + testem rozróżniającym. Hipotezy
  H-TERRAIN/H-COLLISION/H-OTHER rozliczone (przewidywania+falsyfikacje, żadna nie
  „wygrywa" bez dowodu). Predykat NEUTRALNY (bez „terrain" w predykacie).
  measured_quantity: censusy writerów + dekody ciał + disposition hipotez;
  failure_case: wirtualna krawędź bez kandydatów = FAIL (musi być jawny UNPROVEN
  z testem); boundary: runtime zakazany — identyfikacja statyczna tylko.
- **G6-P3-BINDING** — ścieżka +0xC0 zdekodowana (FUN_005247C0→FUN_00509330 +
  argumenty tworzenia); tabela rozdzielenia kluczy/ID; tożsamość transform→model
  UDOWODNIONA (pointer identity / proven lookup) LUB jawny brak (status jawnie:
  TRANSFORM_TO_MODEL_PROVEN / NOT_DEMONSTRATED); status 4508/296445 jawny (domyślnie
  OPEN bez dodatniego dowodu); JEDNA alternatywna ścieżka wskazana, jeśli brak
  połączenia. failure_case: sąsiedztwo wywołań nie może być raportowane jako
  tożsamość; boundary: 19 ctor-callers pozostaje NOT_CHECKED.
- **G7-IMMUTABLE** — composite + per-plik before==after dla: oryginałów, pakietów
  historycznych (min. fazy A/B + Desktop + ROUND/RUN*), evidence własne; obce
  `experiments/`, `src/game/` nietknięte; porty 8000/9350 nietknięte.
- **G8-PUBLICATION** — manifest = pliki istnieją + SHA zgodne na commicie i po push;
  bez self-row; unikalne ścieżki; brak stale rows; path-limited commit
  `docs/audits/PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913/` + DOKŁADNIE
  JEDEN wiersz AUDIT_ENTRYPOINT.md; po push: git show + zgodność manifestu +
  ls-remote; brak push → **PUBLICATION_BLOCKED** (lokalny commit; NIGDY
  „opublikowane").

---

## 8. ZAKAZY

1. Nie zmieniać: oryginalnych archiwów, Entropia.exe, silnika, oracle, parsera R61,
   viewera, prototypu gry, pakietów historycznych.
2. Nie uruchamiać: klienta, Fridy, x32dbg, mock-servera; nie logować się i nie łączyć
   z usługami gry (w tym porty 8000/9350 — bez ingerencji).
3. Nie kopiować proprietary source do publicznego repo.
4. Własny projekt Ghidra TYLKO w kopii runu: skopiować GHIDRA_LOCAL z ostatniego
   pakietu (fazy B), NAJPIERW zweryfikować jego manifest (AT_COPY/FINAL); zapisać
   AT_COPY + FINAL manifesty własnej kopii per MANIFEST_VALIDATION_ORDER (ERRATA_R3
   reguła 4); NIE nadpisywać cudzego locka (jeden właściciel projektu Ghidra naraz).
5. Runtime wymagający GO opisać jako PRZYSZŁY eksperyment (nie wykonany).
6. Nie zamieniać budynku w model roboczy; nie ustawiać zgadywanego XYZ jako
   „odzyskany świat". Pozycje 296445 pozostają NIEODZYSKANE, dopóki nie zostaną
   odzyskane dowodem.
7. Nie przenosić PE2/2003/10.x/Gamebryo 2.3/Skyrim na 9.3.5 bez potwierdzenia w jego
   binarium.
8. Nie ogłaszać STATIC_INSTANCE_MECHANISM_CONFIRMED ani źródła placementu statyków;
   nie wydawać MASTER_ACCEPTED dla całego mechanizmu z samych poprawnych hashy/
   censusów — można zaakceptować integralność i wąski ślad, pozostawiając format/
   provider/źródło danych/placement historyczny otwarte.
9. NIE mutować niczego poza katalogiem runu (wyjątek: kroki publikacji §9 po
   autoryzacji — dokładnie `docs/audits/<RUN_ID>/` + 1 wiersz entrypoint).
10. Referencyjny dekoder F1 — tylko run-local, nigdy do produkcji (§3.1 pkt 6).

## 9. PUBLIKACJA (obowiązkowa, po QC i adjudykacji PE-MASTER)

1. Path-limited commit: `docs/audits/PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913/`
   + **DOKŁADNIE JEDEN** wiersz AUDIT_ENTRYPOINT.md. Bez `git add -A`, bez force-push,
   bez usuwania/absorbowania obcych zmian.
2. Przed commitem: HEAD/remote/staging/diff vs BASE_SHA (e30f99f…). Równoległa
   zmiana → NIE nadpisywać; uzgodnić bazę technicznie lub zgłosić konflikt do
   PE-MASTER.
3. Do repo NIE publikować: EXE, archiwów, projektu Ghidra, dużych fragmentów kodu
   silnika. Publikować: raporty, własne małe sondy, krótkie piny/dane, hashe,
   instrukcję odtworzenia.
4. Po push: `git show` nowego commita + pełna zgodność manifestu + `git ls-remote`;
   podać pełny SHA + linki do REPORT/ERRATA/HANDOFF.
5. Brak dostępu do push = **PUBLICATION_BLOCKED** (lokalny commit; nie deklarować
   „opublikowane").

## 10. OBOWIĄZKOWE PLIKI PAKIETU

`RUN_CONTRACT.md` (ten plik; 00_CONTROL) · `ERRATA_R5.md` (targety verbatim
T-01..T-32 + zasady pierwszeństwa jak ERRATA_R3/4) · `REPORT.md` · `QC_REPORT.md` ·
`HANDOFF.md` · `STAGE_ACCEPTANCE_GATES.csv` · `artifact_index.csv` ·
`MANIFEST_SHA256.csv` · `SOURCE_IDENTITIES.json`. Katalogi: 00_CONTROL, 01_RAW,
02_ANALYSIS, 03_EVIDENCE, 06_REPORT (istnieją od szkieletu formalizacji).

## 11. HANDOFF WYKONAWCY (format zwrotu do PE-MASTER)

1. **RUN_STATUS** (PASS_WITH_BOUNDARY / PARTIAL / BLOCKED / …) + disposition per faza.
2. Wyniki **per bramka** G1-G8 (status + granice + artefakt).
3. Macierz twierdzenie→VA/bajty→receiver→test→wynik→artefakt.
4. Lista artefaktów (ścieżki + SHA) + otwarte kwestie + JEDEN następny eksperyment
   wynikający z nowej wiedzy.
5. Pełny FULL_READ_LOG + NOT_CHECKED (jawne).
6. Stan git (HEAD, commit SHA, push status) — wg §9.
7. Adjudykacja F1/F2/F3 (ACCEPTED/REJECTED/PARTIAL per finding Desktopu) + rozjazdy
   wobec pinów §12 (AUDITOR_EXPECTATION) — każda pozycja: zgodność/rozjazd + dowód.

---

## 12. AUDITOR_EXPECTATION — piny PE-MASTERa (AUDITOR_COUNTERCHECK, fizycznie zweryfikowane z EXE)

> **UWAGA METODOLOGICZNA (kontraktowa):** poniższe wartości są OCZEKIWANYMI wynikami
> niezależnego dekodu. Wykonawca MUSI wyprowadzić każdy niezależnie własnym dekodem z
> EXE i raportować zgodność/rozjazd; **NIE WOLNO kopiować bez własnego dekodu**
> (kopiowanie = wada metodologiczna → QC_FAIL). Rozjazd z dowodem jest wynikiem.

### 12.1 F1 — FUN_007343E0

- ABI: arg1=ESI=kursor (MOV ESI,[ESP+0xC]); arg2=EDI=destination (MOV EDI,[ESP+0x14]
  @0x00734416). Caller @0x00745414: `8D 57 0C; 52; 55; E8` → destination=rec+0x0C.
- Oba epilogi (region 0x00734596 i region ~0x007345AF — patrz rozjazd D-3) kończą:
  `66 89 5F 24; 5F; 8B C6; 5E; 5B; C3` — EAX = ten sam kursor wejściowy.
- Maska u16 @kursor (MOVZX EBX,WORD [EAX+ECX]); tabela: dst+00: bit 0x002→FLDZ/FSTP
  (0.0f), bit 0x004→FLD1 (1.0f), brak→odczyt f32 (FUN_004C32F0); dst+08: 0x008/0x010;
  dst+0C: 0x020/0x040; dst+10: 0x080/0x100; dst+14: 0x200/0x400 (ten sam wzorzec);
  użyty bit czyszczony (AND EBX,~bit); OBA bity pary: gałąź 0 wygrywa, bit 1 zostaje
  w reszcie; dst+18/+1C/+20: trzy BEZWZGŁĘDNE odczyty f32 INLINE (kontrola kursora:
  [ESI+0x11] invalid + bounds [ESI+0xC]+4 vs [ESI+8]; overflow/invalid → FLDZ→0.0f
  zapisane), advance=FUN_0040DE60(4); dst+24=reszta maski (MOV [EDI+0x24],BX);
  **dst+04 NIGDY niepisan przez ten helper**.
- FUN_007345C0 = inicjalizacja zerami szerszej struktury (f90-adjacent), NIE dowód
  macierzy 3×3.
- Arytmetyka: maska 0 → 34 B (2+8×4); 0x2AA/0x554 → po 14 B; 0x7FE → 14 B,
  reszta 0x554.

### 12.2 F2 — FUN_004C46C0

- Lokalna kopia rekordu: [ESP+0x10]=rec+8=pos.x, [ESP+0x14]=rec+0xC=pos.y,
  [ESP+0x18]=rec+0x10=pos.z, dalej rotacja/param-sety.
- Łańcuch wariantów: CMP ESI,3 (flagi)→JE@0x004C473B→0x004C4751; CMP ESI,6@0x004C473D;
  CMP ESI,5; CMP ESI,4; CMP ESI,7@0x004C474C; JNE@0x004C474F→0x004C4792 (skip) —
  korekta TYLKO dla {3,4,5,6,7}.
- Korekta: FLD [ESP+0x14](pos.y)@0x004C4751; PUSH 0; PUSH 0; SUB ESP,8;
  FSTP [ESP+4](pos.y); FLD [ESP+0x20](=pos.x po przesunięciu stosu — zweryfikuj
  sam!)@0x004C4760; FSTP [ESP](pos.x); CALL FUN_004154F0@0x004C4767 (E8 84 0D F5 FF);
  MOV ECX,EAX@0x004C476C; CALL FUN_00853A80@0x004C476E (E8 0D F3 38 00) —
  (this=manager, pos.x, pos.y, 0, 0) __thiscall RET 0x10.
- Po powrocie: FSTP [ESP+0x44](h)@0x004C4773; FLD [ESP+0x18](z_copy)@0x004C4777;
  FLD [ESP+0x44](h)@0x004C477B; FCOM ST(1)@0x004C477F (D8 D1); FSTSW AX@0x004C4781
  (DF E0); **FSTP ST(1)@0x004C4783 (DD D9)**; TEST AH,0x41@0x004C4785;
  JNE@0x004C4788→0x004C4790 (FSTP ST(0) DD D8 = odrzucenie h; pamięć [ESP+0x18]
  zostaje z); fall-through: FSTP [ESP+0x18]@0x004C478A (zapis h);
  JMP@0x004C478E→0x004C4792; PUSH 0x128@0x004C4792; ctor CALL FUN_00528E50@0x004C47C1
  (E8 8A 46 06 00).
- Semantyka z' (do niezależnego potwierdzenia pełną tabelą flag): z'=h wtw h>z
  (ordered); z=h → z'=z (te same BITY); h<z → z'=z; NaN(h) → z'=z (ROŻNIE od
  Math.max); NaN(z) → z'=NaN; ±Inf wg porządku total na wartościach rozszerzonych FCOM.
- TEST AH,0x41 = maska C0|C3 (status word: C0=bit 8 → AH bit 0; C3=bit 14 → AH bit 6);
  JNE taken ⇔ (C0|C3)≠0 ⇔ NIE (h>z ordered).

### 12.3 P3 — piny procesora FUN_004C47F0 (ścieżka EXISTING)

- Wcześniejszy pośredni CALL slotu +0x14 (slot5/f32): MOV EAX,[EDX+0x14] @0x004C4871;
  FF D0 @0x004C4874 (2 B: bajty 0x004C4874-75) — stąd pochodził stary błędny pin
  „004C4875".
- Guard: CALL FUN_0085B750 @0x004C4878 (E8 D3 6E 39 00).
- Set-pozycji EXISTING: CALL FUN_0085B3E0 @0x004C488A (E8 51 6B 39 00).
- Rotacja: CALL FUN_0085ADB0 @0x004C4896 (E8 15 65 39 00).
- Dispatcher: byte-table indeksy 0xA2..0xC7 = 38 (CMP EAX,0x25 = maks. indeks 37);
  jump-table osobno 22 wpisy.

### 12.4 Faza 2 — szkielet FUN_00853A80 (do pełnego dekodu)

- SUB ESP,0xC; lokalne L0=arg1, L1=arg2; MOV ESI,ECX (this=manager z FUN_004154F0);
  L2=0.0.
- CALL FUN_00755F90 (this=manager+0x58 [LEA ECX,[ESI+0x58]], arg=&L0) — AL=filtr;
  fail → return 0.0 (FLDZ, POP ESI, ADD ESP,0xC, RET 0x10).
- CMP [ESI+0x4C],0 (provider2) — ≠0 → provider2->vtable slot+4 (MOV ECX,[ESI+0x4C];
  EDX=[ECX]; EDX=[EDX+4]; CALL EDX) z argumentami z lokalnych (rozpisz dokładnie).
- CMP [ESI],0 (provider1) — ==0 → JE → FLDZ return 0.0 (**FALLBACK 0 gdy
  provider1==NULL**); ≠0 → CALL FUN_00413340(this=[ESI+0x50]) @0x00853AE8;
  provider1->vtable slot+4 (@~0x00853B07/0x00853B3x — dwie formy zależnie od arg3;
  rozpisz obie); ponownie FUN_00413340([ESI+0x50]) (release); wynik f32 → RET 0x10.
- Zbadać: które wywołanie zasila wynik zwrotny; skutki uboczne provider2 (co robi z
  L0/L1); semantyka FUN_00413340 (lock?); FUN_00755F90 (filtr bounds na
  manager+0x58..0x84 = 12 floatów?).

### 12.5 Faza 3 — fakty do weryfikacji

- ClientMovableObject ctor pochodny FUN_00528E50: lookup po kluczu
  FUN_00414130([this+0x74]) → FUN_005247C0 → new(0x98)+FUN_00509330 → [this+0xC0];
  create arg3 = wskaźnik pustego stringa przez singleton [0x00BA26B8]
  (FUN_004C4640 ignoruje argumenty; FUN_00765930 zwraca wskaźnik stringa) —
  zweryfikować.
- Znana ścieżka modelu (RUN3; do powiązania przez TOŻSAMOŚĆ, nie przez sąsiedztwo):
  pump {0x66=MODEL,A} → ArkModelResourceInstanceRef (ctor FUN_006FA8B0) →
  FUN_006cb020 „<id>__<name>" → registration.

---

## 13. FORMALIZER_NOTES — rozjazdy stwierdzone przy formalizacji (do rozliczenia przez wykonawcę)

Formalizator zweryfikował piny dispatchu wobec OPUBLIKOWANYCH artefaktów pakietu
Desktop (independent_hexdumps.txt linie 61-76; probe.json pin window va 0x004C4773,
27 B) — warstwa POCHODNA projektu (nie EXE; EXE pozostaje źródłem autorytatywnym
dla wykonawcy; formalizacja NIE uruchamiała żadnego narzędzia RE i NIE czytała EXE).
Stwierdzono pełną zgodność łańcucha instrukcji §12.2 z opublikowanymi bajtami ORAZ
następujące rozjazdy między twierdzeniami dispatchu a treścią pakietów:

- **D-1 (metatwierdzenie o hexdumpie — NIEPOTWIERDZONE dla pliku opublikowanego):**
  dispatch twierdzi, że w independent_hexdumps.txt „linia @0x004C4780 ma 14 bajtów
  zamiast 16 i całe okno 0x004C4783-0x478F jest u nich przesunięte o 2". Opublikowany
  plik (linia 69: `0x004C4780 d1 df e0 dd d9 f6 c4 41 75 06 d9 5c 24 18 eb 02`) ma
  16 bajtów i ZAWIERA DD D9 @0x004C4783-84; okno probe.json (pin va 0x004C4773,
  hex `d95c2444d9442418d9442444d8d1dfe0ddd9f6c4417506d95c2418` = 27 B) także
  zawiera dd d9. **POTWIERDZONY defekt to off-by-one pin w AUDYT.md:55/REPORT.md:55**
  („FSTP [ESP+0x18] przy 004C4789" — poprawnie 0x004C478A; 0x004C4789 = bajt disp
  JNE 75 06 @0x004C4788-89). Wykonawca: (i) ponownie odczytać okno z EXE; (ii) w
  ERRATA_R5 poprawić pin off-by-one (T-26); (iii) **NIE formułować w erracie
  twierdzenia o „brakujących 2 bajtach w independent_hexdumps.txt" bez ponownego
  fizycznego potwierdzenia — wobec opublikowanego pliku byłoby ono fałszywe.**
  Jeżeli PE-MASTER bazował na innej kopii (lokalna kopia Desktop
  C:\Users\User\Documents\ChatGPT\PE\...), rozjazd zgłosić w raporcie.
- **D-2 (literówka pinu w dispatchu „FF D0 @0x004C4744-45"):** przy 0x004C4744-45
  leżą bajty `05 74` (środek CMP ESI,5 / JE łańcucha wariantów FUN_004C46C0).
  Właściwe odniesienie — zgodnie z własnym nawiasem dispatchu oraz Desktop AUDYT §2 —
  to pośredni CALL slotu +0x14 w FUN_004C47F0: MOV EAX,[EDX+0x14] @0x004C4871,
  FF D0 @0x004C4874 (bajty 0x004C4874-75, stąd stary błędny pin „004C4875").
  Traktować „0x004C4744-45" jako literówkę za „0x004C4874-75"; wykonawca wyprowadza
  z EXE.
- **D-3 (pin epilogu „0x007345A5-region"):** dispatch podaje oba epilogi jako regiony
  0x00734596 i 0x007345A5 z ogonkiem `66 89 5F 24; 5F; 8B C6; 5E; 5B; C3`.
  Desktop pinuje drugie wyjście @0x007345B4 (MOV EAX,ESI). Przy tym ogonku
  start = VA(MOV EAX,ESI) − 5, zatem drugi epilog ≈ 0x007345AF, nie 0x007345A5
  (pierwszy: 0x00734596 → MOV EAX,ESI @0x0073459B = zgodny z Desktop 0x0073459B).
  Prawdopodobna literówka A5→AF; wykonawca dekoduje oba epilogi z EXE i raportuje
  rzeczywiste starty.
- **D-4 (drobne, nienoszące):** entrypoint wiersz 31 zawiera literówkę „undeoded"
  (popr. „undecoded") — do poprawienia w tej samej edycji wiersza co T-16/T-08 (jedna
  edycja, jawnie zdysklosowana). REPORT.md:34 („NIE zostały objęte tym kanałem w tym
  runie") i REPORT.md:138-140 (§6.3) — zakres-exact, NIE są targetami erraty
  (utrzymać jako wzorzec poprawnego sformułowania).

## 14. Tożsamości wejść formalizacji (SHA256; repo @ e30f99fdb3c7913c3c4fa6ee1571e505955192d1)

| Plik (repo) | SHA256 | Zakres lektury formalizatora |
|---|---|---|
| docs/audits/PE_935_ORIGIN_SEAM_DESKTOP_AUDIT_R1_20260913/AUDYT.md | C4C87C2BC6EE4E7238EAA6FBD79146D1D5D15C7B6B4C2F9E47898ABA84DECAF6 | pełna (118 l.) |
| …/PROMPT_OPENCODE.txt | 3DA1EF71FF8090261122A86E40AF212F4DB2B8063DA8643FDD3BCE6903014B31 | pełna (124 l.); historyczna, NIE wiążąca wobec obecnego zlecenia |
| …/independent_hexdumps.txt | 5B73E31384890287DBCD3A5A67623C40E3059B58A4680FF60CB53447EDCCC620 | linie 61-76 (weryfikacja D-1) + struktura pliku |
| …/probe.json | 640272E0C3F7C3EFFA2C47DB9AE2B4A143F5236B6CF64821FCF401771F255E3A | sekcja positionAdjustment (l. ~1930-2050) + grep pól 004C47xx |
| …/REPORT.md | C4C87C2B…CAF6 (identyczny bajtowo z AUDYT.md) | przez tożsamość z AUDYT.md |
| docs/audits/PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/06_REPORT/REPORT.md | 6AC8371200B652E9688D9A2610565C32DB1DCE66FE301B31F2B7E289F15C3BB2 | pełna (199 l.) |
| …/ERRATA_R4.md | 8B28BCC6D5C3AE0EE4DA4A4C986B48C80D7270CC8B1CD1ABCD8B56C0C481578D | pełna (266 l.) |
| …/QC_REPORT.md | CC7779D90843653979AA606DC6EEE5F290D15EF72A4A5887065FD4A01381E0A6 | pełna (331 l.) |
| …/HANDOFF.md | 90F17EFF9CFB6D9184394257DAF91EA75B8C35C1844AC94AED75C76F898676F0 | pełna (100 l.) |
| …/STAGE_ACCEPTANCE_GATES.csv | DA32274A93409AF15B428CE83BBEA076D7782B229EFE86AF751C4C3270C4D334 | pełna (16 wierszy; GB4 i QC-3 własnym odczytem) |
| …/RESEARCH_FINDINGS.md | 9F24A747516379666FF7EB4988BE14B075E3D800B5B935E566F919EDCDC3B503 | pełna (139 l.) |
| …/02_ANALYSIS/SEAM_FLOW_MAP.md | 274F64904DD721F8EAE00E86486BAFB200D392C6E1E56FCC1EB5C401F07EC944 | pełna (82 l.) |
| …/02_ANALYSIS/KEY_MODEL_MATRIX.md | 021F9569B7219F6A9F41AF35E98A08B2DA2902F9FFF37162ECF4FACE055DAB5C | pełna (67 l.) |
| docs/audits/PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913/06_REPORT/REPORT.md | A62FDBDDAB6651189BDA2E07CACA9AABCE76DC2147E4B36D15499A896BA00C41 | pełna (250 l.) |
| …/ERRATA_R3.md | 4D081A367AB334697136B4EC5E2D096339BE6741A052B52926E8FA6716EE3C87 | pełna (410 l.) |
| AUDIT_ENTRYPOINT.md | A2BFC537E25BFCCA30DBD531AF7B0269DDE9F0D6AF871E7372B955066B37CB37 | LATEST RUNS wiersze 30-31 w całości (pełne linie) + nagłówek; reszta tabeli przeskanowana grep-status (STATICS/statyk/4508/296445) |

Kontekst nadrzędny (boot formalizatora, historia — nie wiążące wobec obecnego
zlecenia): 00_PROJECT_CONTEXT/PE_MASTER_ACTIVE_ORDER.md (v4+nagłówek v6/v7),
00_PROJECT_CONTEXT/PE_MASTER_LOOP_STATE.json (loop bd17344b self-audit — historyczny).

**NOT_CHECKED (formalizator):** RUN_CONTRACT.md i RESEARCH_FINDINGS.md Fazie A;
pełna treść wierszy 1-29 i 32+ AUDIT_ENTRYPOINT.md (tylko grep-status); 01_RAW/DECOMP
pakietu fazy B; oryginalne bajty EXE (formalizacja CZYSTO DOKUMENTACYJNA — żadnych
narzędzi RE); manifesty GHIDRA_LOCAL.

---

**Koniec kontraktu.** Ten dokument jest zamknięty po stronie formalizatora; zmiany
treści (nie uzupełnienia wykonawcze zgodne z §3.4/§12) wymagają nowego dispatchu
PE-MASTER.
