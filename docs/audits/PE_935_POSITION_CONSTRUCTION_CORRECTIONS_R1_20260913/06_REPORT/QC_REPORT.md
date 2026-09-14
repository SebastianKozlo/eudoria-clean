# QC_REPORT — PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913

**Wykonawca:** pe-reconstruction · **Tryb:** STATIC-ONLY · SELF_CHECK (oznaczony jawnie; NIE jest niezależnym audytem PE-MASTER)

## SELF_CHECK — kontrola zgodności z kontraktem

### 1. S0 / G1 (fail-closed)
- SHA256 EXE/templates.vfs + rozmiary: zgodne z §1 kontraktu (mierzone ponownie skryptem `s0_era.py`, exit 0; mismatch = exit 1 bez downstream).
- PE32: machine 0x014C, opt_magic 0x10B, base 0x00400000, ASLR OFF, .text RVA 0x1000/Raw 0x1000 — zgodne.
- 17/17 spot-checków VA→offset z pinami bajtowymi §12.2/§12.3 — **PASS** (w tym FSTP [ESP+0x18] D9 5C 24 18 @0x004C478A — T-26).
- Katalog RUN_ID: istniał jako szkielet formalizacji (00_CONTROL z RUN_CONTRACT.md + puste 01/02/03/06) — brak kolizji treści, brak obcych plików.

### 2. Granice trybu (§8 zakazy)
- Klient/Frida/x32dbg/mock/sieć: **NIEURUCHOMIONE** ✓; porty 8000/9350 bez ingerencji ✓.
- GHIDRA_LOCAL: skopiowany z fazy B po weryfikacji manifestu źródłowego FINAL (10/10 SHA zgodnych); własny manifest AT_COPY == źródłowy FINAL (10/10); analyzeHeadless uruchomiony **wyłącznie na własnej kopii w katalogu runu** (project lock jednego właściciela zachowany); manifest FINAL własnej kopii zapisany po turach (`GHIDRA_LOCAL_MANIFEST_final.csv`).
- Wszystkie dekody z FIZYCZNEGO EXE ✓ (capstone/PE parser własny; Ghidra tylko jako wsparcie dekompilatów censusowych — warstwa jawna w REPORT §7).
- Hexdumpy Desktopu: użyte WYŁĄCZNIE do weryfikacji krzyżowej D-1 (bajt-identyczność potwierdzona, raport §8) — nie jako źródło dekodu ✓.

### 3. Piny AUDITOR_EXPECTATION (§12) — wyprowadzone własnym dekodem, nie kopiowane
- §12.1: zgodność 100% TREŚCI (ABI/maski/arytmetyka/dst+04/EAX-kursor); **rozjazd off-by-one pinów epilogów** (0x0073459C/0x007345B5 mierzone vs 0x0073459B/0x007345B4 Desktop — patrz ERRATA_R5 §2.D-3, surowe bajty w `01_RAW`).
- §12.2: zgodność 100% (wszystkie VA kontraktu potwierdzone bajt po bajcie; FLD [ESP+0x20]=pos.x samodzielnie zweryfikowane arytmetyką stosu).
- §12.3: zgodność 100% (w tym D-2: 0x004C4744-45 = bajty `05 74` — literówka dispatchu potwierdzona).
- §12.4: zgodność struktury szkieletu; **JEDEN rozjazd merytoryczny: wywołania lock/release to FUN_00413440 (EnterCriticalSection-thunk) i FUN_00413450 (LeaveCriticalSection-thunk), NIE FUN_00413340** (adres 0x00413340 nie jest startem funkcji; importy rozstrzygnięte własnym parsowaniem IAT). Raportowane jako rozjazd z dowodem (zgodnie z §12 uwagą metodologiczną).
- §12.5: zgodność z rafinacją (FUN_00765930 konstruuje string w f90rec+0x8C; this singletonu nieczytany — udokumentowane).

### 4. Bramki (SELF)
- G1 PASS; G2 PASS (28/28 + meta PASS; świadectwa SYNTHETIC oznaczone); G3 PASS (tabela = model instrukcji — boundary jawne; mapa EXISTING z nową korektą Z + drop-to-ground); G4 PASS (32/32 targetów; scan: 0 LIVE_ELSEWHERE); G5 PASS (RTTI własne; censusy 104/15/14/14; predykat neutralny); G6 PASS_WITH_BOUNDARY (TRANSFORM_TO_MODEL = NOT_DEMONSTRATED — jawny); G7 PASS (przed==po — patrz §5); G8 BLOCKED_BY_PROCESS (publikacja = osobny krok; wykonawca nie commituje).

### 5. G7 immutability (własny census per-plik)
- BEFORE composite: `A606CF52CC6804702C469777013115A80328539EADC27A9053F4F199877783D0` (1020 plików w 8 pakietach historycznych + 2 oryginały).
- AFTER composite: identyczny (skrypt ten sam, druga tura). Wszystkie SHA per-plik zgodne. **Censusy w `01_RAW/G7_CENSUS_before.json` / `G7_CENSUS_after.json`.**
- git: HEAD == BASE_SHA e30f99f... bez commitów wykonawcy; `?? experiments/` nietknięty (scan czytał read-only); src/game/ nietknięty.

### 6. Determinizm i hashe skryptów
- `00_CONTROL/SCRIPT_SHA256.csv`: każdy skrypt hashowany PO ostatniej edycji PRZED wykonaniem (re-hasze po naprawach opisane inline — wzorzec fazy B).
- Wyniki: bez timestampów w danych wynikowych (JSON-y zawierają wyłącznie mierzalne wartości; świadectwa SYNTHETIC oznaczone polem).

### 7. Znaleziska jakościowe wymagające uwagi PE-MASTER (kandydaci lekcji, nie twierdzenia)
1. **Rozjazd pinu §12.4 (FUN_00413340→FUN_00413440/FUN_00413450):** potwierdzony bajtowo + IAT; prośba o adjudykację pinu.
2. **Rozjazd D-3 (epilogi):** Desktop piny MOV EAX,ESI off-by-one (0x73459B/0x7345B4 to POP EDI) — mierzone 0x73459C/0x7345B5 (surowe bajty w 01_RAW).
3. **NOWE (poza zakresem pinów, w granicach kontraktu §3.2 pkt 6):** EXISTING-path FUN_0085B3E0 stosuje tę samą korektę Z **bez bramki wariantu przed korektą** + drop-to-ground (krok 0.1, ≤100 iteracji, sonda mgr2) + finalny vtable[+4]; guard FUN_0085B750 = wariant ∈ {2..7} (szerszy niż {3..7} w CREATE). To ROZSZERZA model Desktop (Desktop twierdził korektę tylko w CREATE — adjudykacja: **PARTIAL** — CREATE potwierdzone, EXISTING było poza twierdzeniem Desktopu, nie błąd).
4. **T-15 licznik:** ERRATA_R4 „8×f32" — własny pomiar 9×f32 (miscount; disposition PARTIAL w ERRATA_R5).

### 8. Kontrola anti-leak
- W G5/G6 brak predykatów zawierających słowo „terrain" jako warunek PASS (G5 PASS wynika ze struktury: RTTI + łańcuch + konsumenci).
- H-TERRAIN wygrała DOWODEM (RTTI + chain), nie założeniem; heightmapa 50.bnt/field-decode NIE przypisana (zakaz §4 pkt 5).
- Warstwa „wykonanie silnika-klienta" oznaczona jako NIEOBECNA wszędzie (REPORT §7, gates CSV boundary G3).

### 9. Świadectwa
- Suita F1: SYNTHETIC (bufory syntetyczne) — oznaczone w JSON i w skrypcie.
- Tabela x87: MODEL instrukcji (nie pomiar) — oznaczone.
- Wszystkie liczby w REPORT: własne (censusy/dekody) lub wyraźnie oznaczone jako podtrzymane z faz A/B (np. klucz D@4508=124.941 — przeliczone własną arytmetką f32).

**SELF_CHECK verdict: PASS_WITH_BOUNDARY** — komplet bramek w granicach trybu; rozjazdy pinów raportowane uczciwie; publikacja oczekuje na adjudykację PE-MASTER.
