# QC_AUDIT_R1 — PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913

**Audytor:** pe-master-auditor (fresh INTERNAL_QC, własne narzędzia; NO_NESTED_TASKS) · **Data:** 2026-09-14
**Zakres QC (dispatch PUBLICATION STEP 2):** weryfikacja ordered amendments A-F + census pakietu + G7 + GHIDRA_LOCAL + byte-pins + disclosuree. QC celowe (targeted, LOAD_BEARING), NIE powtórka pełnego audytu PE-MASTER (który wykonał własne weryfikacje bajtowe i censusy — werdykt w PE_MASTER_REVIEW.md).
**Independence statement:** wszystkie pomiary poniżej = własne narzędzia audytora (PowerShell/BCL; PE parser sekcji napisany od zera w tej sesji; hashe Get-FileHash; sortowanie code-point). Żadny skrypt wykonawcy nie był używany do weryfikacji własnych twierdzeń wykonawcy.

---

## 1. Weryfikacja poprawek A-F (ordered amendments)

### Metoda
Każdy stary fragment maszynowo zweryfikowany jako DOKŁADNIE RAZ (EXACTLY-ONCE) przed podmianą; każdy nowy fragment DOKŁADNIE RAZ po podmianie; zero pozostałości starych; porównanie diff vs kopia `.pre` (tylko linie objęte nowelizacją się różnią); kodowanie bajtowe po każdej edycji (UTF-8 bez BOM, LF-only — we wszystkich trzech plikach potwierdzone: BOM=False, CR=0).

### A. REPORT.md §2.B(6) — pin zapisu h (EXISTING-path) — **VERIFIED**
- Old: „…JNE/FSTP [ESP+0x24] @0x0085B43F — zapis h…" (1x) → New: „…JNE (cel JNE @0x0085B43F = FSTP ST(0), odrzucenie h)/FSTP [ESP+0x24] @0x0085B439 — zapis h…" (1x); remnant old = 0.
- **Ground re-read (surowy dowód):** `01_RAW/F0085B3E0_SET_POS_EXISTING_FULL.txt` — linia 33: `0085B437 7506 jne 0x85b43f`; linia 34: `0085B439 d95c2424 fstp dword ptr [esp + 0x24]` (zapis h); linia 36: `0085B43F ddd8 fstp st(0)` (odrzucenie h). Poprawka zgodna z surowym dowodem; poprzedni pin przypisywał zapis h adresowi odrzucenia.

### B. REPORT.md §2.B(6) — bit-exactność kroku drop-to-ground — **VERIFIED**
- Old: „krok = qword [0xA7AF80] = **0.1** (f64)" (1x) → New: „…**0.100000001490116119384765625** (bits 0x3FB99999A0000000, tzn. f64(double(f32 0.1f)), nie kanoniczne f64 0.1 = 0x3FB999999999999A; wartościowo ≈0.1)" (1x).
- **Ground (własny odczyt bajtów EXE):** własny parser PE → sekcja .rdata (RVA 0x676000/Raw 0x676000); VA 0x00A7AF80 → file offset 0x67AF80; 8 bajtów: `00 00 00 A0 99 99 B9 3F` = LE qword **0x3FB99999A0000000** = double **0.100000001490116119384765625** — POTWIERDZONE bit-exact (nie kanoniczne f64 0.1 = 0x3FB999999999999A). Poprawka zgodna z fizycznym EXE.

### C. REPORT.md §3.2 — piny zapisów vtable FUN_00538B70 — **VERIFIED**
- Old: „@0x00538BA9/B5;" (1x) → New: „@0x00538BA9 i @0x00538BAF (0x00538BB5 = ostatni bajt drugiego zapisu);" (1x); remnant = 0.
- **Ground (własny odczyt bajtów EXE):** @0x00538BA9: `C7 06 30 F4 A7 00` = MOV [ESI],0x00A7F430 (6 B); @0x00538BAF: `C7 46 04 20 F4 A7 00` = MOV [ESI+4],0x00A7F420 (7 B — kończy się @0x00538BB5). Oba piny zgodne; konwencja „pin VA = START instrukcji" utrzymana.

### D. ERRATA_R5.md T-08 — dokładny cytat żywego spanu — **VERIFIED**
- Cytat T-08 poprawiony do dokładnej treści żywego wiersza 31 (ze znacznikiem `**` przed POSITION — bold zamyka się dalej w wierszu, wokół spanu poprawki QC SE-R4-6); nagłówek targetu nosi jawne „offset = pozycja znakowa wewnątrz wiersza 31"; dodana linia AMENDMENT z wyjaśnieniem; tekst „Poprawka" (replacement) zachowuje `**` na tej samej pozycji.
- Zmienione linie ERRATA_R5 vs `.pre`: **16, 69, 70, 71 + 1 nowa linia (AMENDMENT)**; wszystkie pozostałe linie byte-identical. Kodowanie zachowane.

### E. ERRATA_R5.md §0 — wersja capstone — **VERIFIED**
- „capstone 3.12.2026" (1x) → „capstone 5.0.7" (1x); remnant „3.12.2026" = 0. Zgodne z nagłówkiem REPORT.md (capstone 5.0.7).

### F. 02_ANALYSIS/ENTRYPOINT_ROW_DRAFT.md — wiersz T-08 + nota — **VERIFIED**
- Old-span wiersza T-08 = dokładny żywy tekst wiersza 31 (z `**`); replacement zachowuje `**` przed POSITION. Dodana „Nota offsetowa (AMENDMENT PE-MASTER)" (offsety 1679/3594/3818 = pozycje znakowe wewnątrz wiersza 31, weryfikacja EXACTLY-ONCE obowiązkowa).
- Zmienione linie vs `.pre`: **10 + 2 nowe linie** (pusta + nota); reszta byte-identical.

### Kopie .pre (dowody pre-edit; byte-identical, SHA256)
| Plik | SHA256 (.pre == pre-edit live) |
|---|---|
| 00_CONTROL/PRE_EDIT/REPORT.md.pre | D1B5E34AF6C5AE8E7F256F92197C02AC26DF1007D3C06E3DE821A174D5364C5B |
| 00_CONTROL/PRE_EDIT/ERRATA_R5.md.pre | FB54B4F931F06A179EF46D882D5828D4EA12D76801D2E516DD8A3950F982A24F |
| 00_CONTROL/PRE_EDIT/ENTRYPOINT_ROW_DRAFT.md.pre | 5E4A24C0493C10AE0A64980986D176E54B9B77BD8062242ABCB8B84C50C76602 |

Każdy hash `.pre` == odpowiedni wiersz (pre-amendment) `MANIFEST_SHA256.csv` — dowód, że pliki nie były zmienione między generacją manifestu a nowelizacją (patrz §2: rozjazdy manifestu = DOKŁADNIE te 3 pliki).

---

## 2. Census pakietu — **VERIFIED**

- **artifact_index.csv:** 171 wierszy; wszystkie ścieżki istnieją na dysku (0 missing); zgodność wiersz-po-wierszu z MANIFEST_SHA256.csv (path+sha) = 171/171; **self-row: 0; zduplikowane ścieżki: 0**.
- **MANIFEST_SHA256.csv (re-hash przed refresh; case-insensitive):** 171/171 wierszy sprawdzonych → **168 dokładnych zgodności + 3 rozjazdy = DOKŁADNIE trzy pliki objęte nowelizacją A-F** (REPORT.md, ERRATA_R5.md, ENTRYPOINT_ROW_DRAFT.md); rozjazd w każdym przypadku: hash manifestu == hash `.pre`, hash dysku == hash post-amendment. Wniosek: manifest był dokładny dla stanu pre-amendment i ŻADEN inny plik pakietu nie zmienił się w trakcie nowelizacji (GA-AMEND hash census PASS). Refresh manifestu w kroku STEP 4 przywraca 100% zgodność.
- **POST-REFRESH (STEP 4, weryfikacja własna):** zbudowane manifesty mają **177 wierszy** (171 poprzednich + 3 kopie `.pre` + 3 nowe pliki: AMEND_LOG_R1.md, PE_MASTER_REVIEW.md, QC_AUDIT_R1.md); niezależny re-hash wszystkich 177 wierszy: **177/177 zgodnych, 0 missing, 0 mismatch; self-row: 0; zduplikowane ścieżki: 0**; artifact_index 177/177 (path+size+sha zgodne z manifestem i dyskiem); pokrycie pełne — każdy plik pakietu poza wykluczeniami (GHIDRA_LOCAL/, __pycache__/, 2 pliki manifestów) ma swój wiersz, i odwrotnie (177 = 175 plików + 2 manifesty GHIDRA_LOCAL_MANIFEST_*.csv; moja pierwsza licznia 175 była efektem zbyt szerokiego filtru nazw — poprawiona).
- **SCRIPT_SHA256.csv (last-row-per-script vs disk):** 20 unikalnych skryptów, **20/20 zgodnych** (0 mismatch). Udokumentowane wielo-wierszowe re-hashe: `ghidra_post_decomp.py` — ostatni wiersz = **3EFC41A3F38644937CE886776C68D039DB630D51A209926ADDF572678C5B879F** (zgodny z dyskiem); `p2_census.py` ostatni = 3CAAE066…; `p2_census2.py` ostatni = F6969F36…; `f1_model_decoder_suite.py` ostatni = 4D00B623… — wszystkie == dysk.

## 3. G7-IMMUTABLE — **VERIFIED (z niezależną re-derivacją composite)**

- `01_RAW/G7_CENSUS_before.json` == `G7_CENSUS_after.json` **byte-identical** (SHA256 obu = 9FB8BCE0B823E3B811D48C74C0BCC09E96D53F877FB162AAFC97D4182DD1767D).
- **Niezależna re-derivacja composite (własna implementacja audytora — PowerShell, sortowanie code-point/ordinal, pre-order DFS, separatory relpath Windows):** 1022 entries (2 oryginały + 1020 plików w 8 pakietach historycznych) → composite = **A606CF52CC6804702C469777013115A80328539EADC27A9053F4F199877783D0** — ZGODNY z zapisanym w G7_CENSUS (i z niezależnym przeliczeniem PE-MASTER).
- **Nota metodologiczna (lesson):** pierwsza próba re-derivacji z kulturowym (case-insensitive) sortowaniem nazw dała INNY composite (05DF7722…) — kolejność sortowania plików/katalogów musi być code-point (Python `sorted()`), nie kulturowa. Composite G7 jest wrażliwy na semantykę sortowania; zreprodukowany poprawnie dopiero z [StringComparer]::Ordinal. Nie jest to defekt pakietu — to wymóg odtwarzalności zapisany tu jako lekcja.

## 4. GHIDRA_LOCAL — **VERIFIED**

- **at_copy manifest vs FINAL manifest źródła (faza B, PE_935_ATTRIBUTE_ORIGIN_SEAM_R1):** 10/10 SHA zgodnych (normalizacja separatorów: at_copy używa `\`, źródło `/` — kosmetyka, SHA identyczne).
- **Własny FINAL manifest vs dysk (10 plików projektu, w tym db.73.gbf/db.74.gbf z tur analyzeHeadless tego runu):** 10/10 zgodnych (re-hash własny, 2 duże pliki 189 759 488 B każdy).

## 5. Byte-pins vs fizyczny EXE (własne narzędzia: własny parser sekcji PE + odczyt bajtów)

Własna tabela sekcji: machine 0x014C, optMagic 0x10B (PE32), imageBase 0x00400000, 5 sekcji (.text RVA 0x1000/Raw 0x1000/VSize 0x676205; .rdata RVA 0x676000/Raw 0x676000; …). Mapowanie VA→file offset własne.

| Pin | VA | Bajty zmierzone (własne) | Oczekiwane | Wynik |
|---|---|---|---|---|
| 1. FSTP [ESP+0x18] (T-26) | 0x004C478A | `D9 5C 24 18` | `D9 5C 24 18` | **MATCH** |
| 2. Thunk EnterCriticalSection | 0x00413440 | `51 FF 15 64 50 A7 00 C3` | `51 FF 15 64 50 A7 00 C3` | **MATCH** |
| 3. CALL FUN_0085B3E0 (set-pos EXISTING) | 0x004C488A | `E8 51 6B 39 00` → target = 0x004C488F + 0x00396B51 = **0x0085B3E0** | E8 51 6B 39 00 → 0x0085B3E0 | **MATCH** (arytmetyka rel32 własna) |
| 4. (extra, ground B) stała drop-step | 0x00A7AF80 | LE `00 00 00 A0 99 99 B9 3F` = 0x3FB99999A0000000 = 0.100000001490116119384765625 | 0x3FB99999A0000000 | **MATCH** |
| 5. (extra, ground C) MOV [ESI],0x00A7F430 | 0x00538BA9 | `C7 06 30 F4 A7 00` (6 B) | C7 06 30 F4 A7 00 | **MATCH** |
| 6. (extra, ground C) MOV [ESI+4],0x00A7F420 | 0x00538BAF | `C7 46 04 20 F4 A7 00` (7 B, koniec 0x00538BB5) | C7 46 04 20 F4 A7 00 | **MATCH** |
| 7. (extra, D-1) okno 0x004C4780-478F | 0x004C4780 | `D1 DF E0 DD D9 F6 C4 41 75 06 D9 5C 24 18 EB 02` | = independent_hexdumps.txt:69 | **MATCH** (byte-identical; re-hash obu stron) |

Do tego **re-hashDesktop AUDYT.md == REPORT.md** (oba SHA256 C4C87C2BC6EE4E7238EAA6FBD79146D1D5D15C7B6B4C2F9E47898ABA84DECAF6 — identyczne, zgodnie z twierdzeniem).

## 6. Wiersz 31 AUDIT_ENTRYPOINT.md — maszynowa weryfikacja EXACTLY-ONCE (przed edycją publikacyjną)

Plik = **UTF-8 bez BOM, LF-only**; pozycje znakowe liczone w punktach kodowych (odczyt z jawnym UTF-8):

| Fragment (żywy) | Pozycja znakowa w wierszu 31 | Liczność w wierszu | Liczność w CAŁYM pliku |
|---|---|---|---|
| T-08: „sub-packet via FUN_007343E0: variant u16 @0x00745435 -> rec+0x34, **POSITION vec3 12B via FUN_00412430 @0x0074545A -> rec+0x38" (ZE znacznikiem `**`) | **1679** | **1** | 1 |
| ten sam fragment BEZ `**` | — | 0 | 0 (konfirmacja niedokładności pierwotnego cytatu ERRATA_R5/DRAFT — naprawionej przez D/F) |
| T-16: „STATICS (4508/296445) NOT covered by the movable channel (OPEN;" | **3594** | **1** | **1** |
| D-4: „undeoded" | **3818** | **1** | **1** |

**Nota metodologiczna (lesson, zapisana):** AUDIT_ENTRYPOINT.md jest UTF-8 bez BOM; domyślny odczyt PowerShell 5.1 (Get-Content bez -Encoding) interpretuje go jako CP1252 — znaki U+201D („”) dekodują się jako 3-znakowy mojibake i pozycje znakowe rosną o +8/+12 (mierzone 1687/3606/3830). Wszystkie offsety tego QC liczone z jawnym UTF-8 — zgodne z deklarowanymi 1679/3594/3818 (PE-MASTER-verified). Publikator MUSI czytać ten plik z jawnym UTF-8.

## 7. LIVE_SCAN — re-tally — **VERIFIED**

`02_ANALYSIS/ERRATA_LIVE_SCAN.json` (17 sond): 59 wpisów = **IN_REGISTER 41 + HISTORICAL_PACKAGE 18 + LIVE_ELSEWHERE 0** — zgodne z re-tally PE-MASTER. Jedyna wymagana edycja poza pakietem = wiersz 31 AUDIT_ENTRYPOINT.md (T-08+T-16+D-4).

## 8. Disclosures (zapisane, zgodnie z dispatchem)

1. **03_EVIDENCE istnieje ale jest PUSTY** (0 plików) — szkielet staged w formalizacji; całość dowodu żyje w 01_RAW/02_ANALYSIS (zgodnie z kontraktem §10 katalogi istnieją; brak plików = jawny stan, nie defekt integralności).
2. **P2_CENSUS2.json = `[[]]`** (2 bajty) — pusty wynik sondy pośredniej; NIE jest nośny (łańcuch census P2 opiera się na P2_CENSUS.json / P2_CENSUS4.json / P2_CENSUS5.json).
3. **ERRATA_R5 T-09 quote = joined-range** cytat REPORT.md:27-34 (faza B) — etykietowany jako zakres („REPORT.md:27-34 (§1)"); linie 27-34 source istnieją (zweryfikowane).
4. **at_copy manifest używa separatorów `\`, źródłowy FINAL `/`** — kosmetyka; SHA identyczne 10/10.
5. **MANIFEST_SHA256.csv (stan bieżący) jest celowo rozjechany dokładnie w 3 wierszach** = pliki nowelizowane A-F (hash manifestu == hash `.pre`) — oczekiwany stan przejściowy; STEP 4 (refresh) przywraca pełną zgodność.

## 9. NOT_CHECKED (jawne, poza celem tego QC)

- Re-run generatorów F1/x87 (suita masek, tabela x87) — warstwa evidence 01_RAW; pełna lektura `f1_model_decoder_suite.py` i własne re-derivacje wykonał PE-MASTER (PE_MASTER_REVIEW.md); to QC nie powielało generatorów (re-run tego samego generatora = powtarzalność, nie niezależność).
- Re-walk wszystkich 7 łańcuchów RTTI — PE-MASTER przeszedł je niezależnie (własne); to QC zweryfikowało groundy poprawek A-F + piny + integralność.
- 67 dekompilatów DECOMP_P2 — warstwa pomocnicza censusów (nie re-odczytane; status zgodnie z granicą runu).
- Pozostałe 13 z 15 call-site'ów FUN_00853A20/00853A80 (2 fizycznie zweryfikowane przez PE-MASTER) — deklarowana granica runu, nie nowa luka.

## 10. Verdict

**QC_PASS.**
- A-F zastosowane i zweryfikowane (EXACTLY-ONCE + diff + kodowanie + groundy bajtowe własne).
- Census 171/171/20/20; G7 byte-identical + composite niezależnie odtworzony (A606CF52…); GHIDRA_LOCAL 10/10+10/10; LIVE_SCAN 41/18/0; byte-pins 7/7 MATCH (własny parser PE).
- Zero defektów technicznych; zero zmian poza przypisanymi plikami (hash census).
- Klasa findingów: bez nowych findingów; jedyna nota metodologiczna = semantyka sortowania composite G7 + wymóg jawnego UTF-8 przy odczycie AUDIT_ENTRYPOINT.md (zapisane jako lekcje, nie defekty).

*QC_AUDIT_R1 zamknięte; publikacja (STEP 3-5) wykonywana po tym QC. Pełny kontekst adjudykacji w PE_MASTER_REVIEW.md (persisted verbatim).*
