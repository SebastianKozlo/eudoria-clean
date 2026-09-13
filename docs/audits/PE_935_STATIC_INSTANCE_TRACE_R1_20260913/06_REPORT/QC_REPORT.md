# QC_REPORT — PE_935_ROUND_QC_STATIC_PLACEMENT_R1_20260913 (RUN A: PE_935_STATIC_INSTANCE_TRACE_R1_20260913)

- **ASSIGNMENT_MODE**: INTERNAL_QC (niezależny audytor wewnętrzny, świeży kontekst; nie executor, nie formalizator)
- **AUDITOWANY RUN**: PE_935_STATIC_INSTANCE_TRACE_R1_20260913 (commit 4d4cde5)
- **QC_RUN_ID**: PE_935_ROUND_QC_STATIC_PLACEMENT_R1_20260913
- **Data**: 2026-09-13
- **Metoda**: własny parser PE (00_CONTROL\qc_probe\qc_pe.py — pełny parse nagłówków/sekcji, własne mapowanie VA→offset), własne censusy CALL rel32 po całym .text, własne skany surowych bajtów, własny parse Models.bnt i plików instalacji. NIE oparto się na narzędziach executora do żadnej weryfikacji bajtowej; dumpy executora (GA*) czytano wyłącznie jako dekompilacje do porównania narracji.
- **Binarium (asercja własna na starcie)**: D:\Eudoria_Reconstruction\pcg_install\Entropia.exe, SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (Get-FileHash — ZGODNE z kontraktem QC i z S0 runu), 8,015,872 B, image base 0x00400000, 5 sekcji, ASLR OFF (dll_chars 0x0000), entry VA 0x0095DA11→offset 5,626,385 (własny parse = wartości S0 co do bajtu).

---

## WERDYKT QC RUN A: **QC_PASS** (0×P0, 0×P1; 3×P3 — wymagają poprawy dokumentacyjnej, nie podważają żadnego twierdzenia nośnego)

Wszystkie kluczowe twierdzenia runu zweryfikowane pozytywnie NIEZALEŻNIE (własne bajty + własne censusy), w tym pełny census 25+13 call-site'ów — mój zbiór VA identyczny co do adresu z tabelą klasyfikacji runu (25/25 lookup + 13/13 pump).

---

## Punkty QC (A1–A10)

### A1. S0/S3 — asercje ery — **PASS**
- Własny parse PE (qc_pe.py): rozmiar 8,015,872 B ✓; image base 0x00400000 ✓; 5 sekcji (.text/.rdata/.data/.tls/.rsrc) z identycznymi VA-raw ptr/size jak S0_ERA_ASSERTION.json ✓; dll_characteristics 0x0000 (ASLR OFF) ✓; entry RVA 0x55DA11 → VA 0x0095DA11, file offset 5,626,385 = dokładnie wartość spot-check S0 ✓; 0x00A86D30→.rdata (offset 6,843,696 = wartość S0) ✓; mapping rule S0 odtworzona i potwierdzona.
- S3 (round-trip/skan .text): 4508 LE (9c 11 00 00) = **dokładnie 3 trafienia** w .text: 0x0053270C, 0x00532769, 0x0083427E (identyczne VA jak S3/GA1) ✓; 4508 BE (00 00 11 9c) = 0 ✓; 296445 LE (5d 85 04 00) = 0 ✓.
- Ścieżka: 01_RAW\S0_ERA_ASSERTION.json; 01_RAW\S3_ROUNDTRIP_4508.json; qc_probe\qc_pe.py, qc_probe\qc_scan_text.py.

### A2. Kwalifikacja FUN_006b4c50 = AVATAR body-set — **PASS**
- String "CharacterPosition" istnieje w binarium: **VA 0x00A8548C** (jedyna lokalizacja). Xrefy (PUSH imm32): 0x006B9B27 i 0x006B9BE1 — **oba wewnątrz FUN_006b9970**; kontekst bajtowy: `MOV ECX,[ESI+0x18]; MOV EDX,[ECX]; MOV EAX,[EDX+0x44]; PUSH 0x00A8548C; CALL EAX` = wirtualny odczyt węzła przez slot +0x44 z argumentem "CharacterPosition" — dokładnie wzorzec cytowany w rejestrze ✓. Wynik do [obiekt+0x1DC]: `FSTP DWORD [ESI+0x1DC]` @0x006B9B36 ✓ (dalej FLD/FADD [ESI+0x1DC] @0x006B9BCC).
- FUN_006b4c50: **dokładnie 1 caller** — CALL rel32 @0x006B99C5 → 0x006B4C50, wewnątrz FUN_006b9970 ✓; przy tym **0 odwołań imm32 do 0x006B4C50 w .text/.rdata/.data** (nie jest instalowany jako callback) — "jedyny caller" potwierdzone w pełni.
- Upstream FUN_00489810 istnieje (chain zgodny z GA6). Stała 11769 (0x2DF9): `B8 F9 2D 00 00` @0x00511245 ✓ tuż przed lookup call-site 0x00511252.
- Ścieżka: 03_EVIDENCE\VA_EVIDENCE_REGISTRY.md E.4; 01_RAW\ghidra_output\GA5_PSEUDO_006B9970.txt; qc_probe\qc_xref.py, qc_final_bytes.py.

### A3. Klasyfikacja 25 lookup + 13 pump — **PASS** (weryfikacja pełna, nie tylko 3 losowe)
- **Pełny niezależny census**: CALL rel32 → FUN_0072f580 = **dokładnie 25** site'ów, CALL rel32 → FUN_006c9700 = **dokładnie 13**; zbiory VA **identyczne co do adresu** z 02_ANALYSIS\Z2_CLASSIFICATION_TABLE.md (25/25 + 13/13). S9_BYTE_VERIFY.json (38 wierszy, mismatches: 0) — spójny z moim census.
- Sample klasyfikacji (5, wymagane 3) — dowody bajtowe własne:
  1. **#1 FUN_00511070 (AVATAR_EQUIPMENT)**: hardcode 11769 @0x00511245 ✓ → lookup @0x00511252 ✓ — dowód zgodny z bajtami.
  2. **#13 FUN_006e2610 (AVATAR_EQUIPMENT adjacent)**: 10× CALL FUN_004926e0 (avatar-id) + 6× CALL FUN_00977780 w body, potem lookup @0x006E28E4 → FUN_005670a0 @0x006E28EE ✓ — "czyta avatar-id → rejestracja template'u avatara" potwierdzone bajtowo.
  3. **pump #13 FUN_0094b1d0 (VEGETATION)**: PUSH 'ArkVegetationModelClient::~ArkVegetationModelClient' @0x0094B220 + PUSH 'ArkVegetationClient::GetModel' @0x0094B23C — stringi verbatim obecne w body, dokładnie jak w tabeli ✓.
  4. **#10 FUN_00567170 (OTHER — rekord derived z transformem)**: f60 @0x0056738E, f90 @0x0056739B, fb0 @0x005673BA — komplet call-site'ów setterów placementu w body ✓ (moje censusy), rejestracja FUN_004148f0 @0x00567413 + FUN_00457930 @0x0056741A ✓.
  5. **#20 FUN_005b5f90 (OTHER — j.w.)**: f60 @0x005B6010, f90 @0x005B601A, fb0 @0x005B6032 ✓ (dokładnie adresy z tabeli); rejestracja @0x005B6088/0x005B608F ✓.
- Ścieżka: 02_ANALYSIS\Z2_CLASSIFICATION_TABLE.md; 01_RAW\S9_BYTE_VERIFY.json; qc_probe\qc_xref.py, qc_b3_sample.py, qc_setter_census.py.

### A4. „0/38 STATIC_WORLD" + UNKNOWN z powodami — **PASS**
- Tabela Z2-A: 25 wierszy lookup (w tym 2 wiersze multi-site 4-8, 11-12, 22-23, 24-25 = 25 call-site'ów łącznie) + 13 wierszy pump — **kompletna (38 call-site'ów = mój census)**; klasyfikacje: AVATAR_EQUIPMENT / PREVIEW_UI / VEGETATION / MODEL_MACHINERY / OTHER / UNKNOWN-1 — **zero STATIC_WORLD** ✓ (przeliczone z tabeli: 0 wierszy z tą klasą).
- UNKNOWN=1 (pump #5 FUN_0093be20): powód udokumentowany (hardcode 0x70D17=460563, "460563.nif NIE istnieje lokalnie; negatyw udokumentowany"); bajtowo: `17 0d 07 00` @0x0093BEB0 + pump CALL @0x0093BEBC ✓.
- Kontrola negatywna generyczności: zero stałych 296445/4508 w .text (A1) ✓ — "ścieżki generyczne wobec ID" potwierdzone.
- Ścieżka: 02_ANALYSIS\Z2_CLASSIFICATION_TABLE.md §C; 03_EVIDENCE\VA_EVIDENCE_REGISTRY.md E.7.

### A5. Trzy wzorce 4508 — **PASS** (rozstrzygnięcie „disp32" potwierdzone własnym dekodowaniem)
- **0x0053270C**: instrukcja `8d 8c 24 9c 11 00 00` = LEA ECX,[ESP+0x119C] **@0x00532709**; VA 0x0053270C = pozycja disp32 (9c 11 00 00) wewnątrz instrukcji — dokładnie „disp32, nie imm32" ✓.
- **0x00532769**: identyczna LEA @0x00532766, disp32 @0x00532769 ✓; dalej `CALL [0x00A75A5C]` (~basic_string — dtor stringu) zgodnie z narracją ✓.
- **0x0083427E**: `89 9e 9c 11 00 00` = MOV [ESI+0x119C],EBX @0x0083427C, disp32 @0x0083427E ✓ — zapis pola 0x467 obiektu (wielkość ramki ctora ArkCommunicator — zgodne z narracją; RTTI ArkCommunicator obecne — patrz A10).
- Granice instrukcji własnoręcznie odtworzone; pełny skan .text (A1) = 3/0/0 — nie istnieją inne wystąpienia 4508/296445 → „hardcode template'u 4508 w .text NIE istnieje" potwierdzone niezależnie.
- Ścieżka: 01_RAW\S3_ROUNDTRIP_4508.json; 01_RAW\ghidra_output\GA1_PATTERNS.json, GA1_PATTERN_WINDOWS.txt; 02_ANALYSIS\Z3_PATTERNS_4508.md; qc_probe\qc_region_dump.py, qc_scan_text.py.

### A6. Settery placementu + zasilanie z systemu atrybutów — **PASS**
- FUN_00730f90 @0x00730F90: `MOV [ECX+0x08/0x0C/0x10],p[0..2]` — pozycja vec3 @+0x08 ✓; FUN_00730fb0 @0x00730FB0: `MOV [ECX+0x14/0x18/0x1C]` — rotacja @+0x14 ✓; FUN_00730fd0 @0x00730FD0: `MOV [ECX+0x20/0x24]` ✓; FUN_00730f60: init 11 dwordów (+0x00..+0x28, pola vec przez FLDZ/FSTP) ✓ (całość z surowych bajtów).
- FUN_00846840 (reader atrybutów): body 0x00846840-0x00846B8A; switch po attr-ID zaimplementowany jako `LEA EAX,[EDI-0x6A4]` @0x00846A0C + `CMP EAX,5` + tabela skoków — case 0x6A4/0x6A5/0x6A8/0x6A9 potwierdzone bajtowo (immediate występuje jako −0x6A4 w LEA; dekompilat GA8_PSEUDO_00846840 zgodny) ✓. Mnożniki _DAT_00a7b260-family w case'ach zgodne z dekompilatem (w tym _DAT_00a79a08 = 0.5 f64 — kanon N-4).
- **Immediates 0x6A4/0x6A5/0x6A8/0x6A9 jako imm w call-site'ach — potwierdzone**: PUSH 0x6A4 @0x00469557 + PUSH 0x6A8 @0x00469568 (FUN_00468910, update world-object); PUSH 0x6A5 @0x00438890/0x0043889B (FUN_004387a0); PUSH 0x6A4 @0x005B70C3/0x00627B1F; łańcuchy CMP: FUN_00846430 `3d a8/a9/a4/a5/ac 06 00 00` (filtr transformu), FUN_00847270, FUN_005146b0, FUN_0043f4b0, FUN_006bd1b0-region.
- Pułapki offsetowe odnotowane i sprawdzone: istnieją mylące wystąpienia 0x6A4 jako offsety stosu (LEA ECX,[ESP+0x6A4] @0x00436153 i in.) i pola klasy (FSTP [ESI+0x6A4] @0x00770D4D) — slice runu ich NIE używa (brak w cytowanych call-site'ach) ✓.
- Ścieżka: 03_EVIDENCE\VA_EVIDENCE_REGISTRY.md E.2; 01_RAW\ghidra_output\GA8_PSEUDO_00846840.txt, GA8_PSEUDO_00730F90.txt, GA8_PSEUDO_00730FB0.txt, GA8_PSEUDO_00730FD0.txt, GA8_PSEUDO_00730F60.txt; qc_probe\qc_a6_switch.py, qc_region_dump.py, qc_xref.py.

### A7. Kreator instancji modelu (FUN_006cb6f0 → FUN_006cb020 → FUN_006cb3c0) — **PASS**
- FUN_006cb6f0 @0x006CB6F0: cache w mapie [store+0x3C] — `LEA ESI,[EBX+0x3C]` @0x006CB729 + CALL FUN_00971780 ✓; check FUN_006cb370 (5 call-site'ów census); pump CALL @0x006CB7CF (`e8 2c df ff ff`) ✓; `PUSH 0xC` @0x006CB819 + CALL operator_new @0x006CB81B → **0x0095D3C4** ✓ (adres dokładnie jak w E.3); ctor ArkModelResourceInstanceRef @0x006FA8B0: `MOV [EAX+4],0` (licznik@+0x04=0), `MOV [EAX],0xA864B8` (vft), `MOV [EAX+8],ECX` (item@+0x08), `RET 4` — wszystkie cytowane instrukcje obecne (offset w body +0x0C) ✓; dtor @0x006FA8D0 z zapisem vft 0xA864B8 w body (0x006FA8FA) — baza 0x00A864B0 dalej w body (E.3 podaje 0x006FA8D0→0x006FA952 — spójne z body).
- FUN_006cb020 @0x006CB020 (536 B body): **PUSH 'ArkAnimation' @0x006CB08D + CALL FUN_007b6c30 @0x006CB092** (check klasy po nazwie) ✓; **PUSH '__' @0x006CB0F7** — separator formatu "<id>__<name>" ✓.
- FUN_006cb3c0 @0x006CB3C0 (250 B): `MOV EAX,[ESI+0x5C]` @0x006CB3C6 (type@+0x5C) ✓, `MOV EAX,[ESI+0x64]` @0x006CB3DE (A@+0x64) ✓; CALL FUN_006f2af0 (reset deskryptora) ×3 @0x006CB445/0x006CB45E/0x006CB4AE ✓; attach przez rodzinę FUN_0077c0f0/0x0077c0b0/0x0077c120 (CALL-e w GA5 disasm, potwierdzone) ✓.
- Rejestracja FUN_006f33a0: dokładnie 1 call-site @0x006CB85E (w FUN_006cb6f0) ✓. FUN_006cb020: dokładnie 1 call-site @0x006CB84F ✓. Narracja spójna bajtowo.
- Ścieżka: 03_EVIDENCE\VA_EVIDENCE_REGISTRY.md E.3; 01_RAW\ghidra_output\GA5_DISASM_006CB6F0.txt, GA5_DISASM_006CB3C0.txt, GA6_PSEUDO_006CB020.txt, GA3_CTOR_ArkModelResourceInstanceRef_006FA8B0.txt; qc_probe\qc_region_dump.py, qc_setter_census.py.

### A8. Most ArkObject (ctor → getter A → encja@+0x28) — **PASS**
- FUN_00726e70 @0x00726E70: `C7 06 48 6B A8 00` = MOV [ESI],0x00A86B48 (vft ArkObject) @0x00726E9F ✓ (vft = 0x00A86B48 zgodne z S4); sekwencja zasilania: `MOV ECX,EBX` (EBX=param_1=obiekt template'u) → **CALL FUN_007ce1e0 @0x00726EB7** → **`MOV [ESI+0x28],EAX` @0x006726EBC** — most A→encja@+0x28 potwierdzony bajt-po-bajcie, dokładnie jak w E.6/raporcie §1.
- Fabryka: FUN_0070bf50 — `PUSH 0x58` @0x0070BF74 (operator_new(0x58)) → CALL FUN_00726e70 @0x0070BF96 ✓; ArkObjectClass vtable @0x00A86850 zawiera slot1=0x0070BF50 ✓ (dump vtable: [0x0073F230, 0x0070BF50]).
- Per-class factory: FUN_007351e0 (ctor ArkSurgeonObject) — istnieje, DAT_00ba58cc cytowane w GA3 dump ✓ (registry E.6).
- Ścieżka: 03_EVIDENCE\VA_EVIDENCE_REGISTRY.md E.6; 01_RAW\ghidra_output\GA3_CTOR_ArkObject_00726E70.txt; qc_probe\qc_region_dump.py, qc_final_bytes.py.

### A9. Oracle NiAVObject (FUN_007c04f0 vs Gb12) — **PASS**
- Kolejność viewer-strings w binarium (własne bajty): m_bAppCulled (read @0x007C053A `8a 45 20`, PUSH 0xa8d8ac @0x007C0544) → m_localTranslate (PUSH @0x007C057C, `LEA ECX,[EBP+0x5C]` @0x007C0580) → m_localRotate (PUSH @0x007C05B0, `LEA ECX,[EBP+0x38]` @0x007C05B3) → m_worldTranslate (PUSH @0x007C061C, `LEA ECX,[EBP+0x90]` @0x007C0620) → m_worldRotate (PUSH @0x007C0654, `LEA ECX,[EBP+0x6C]` @0x007C0658) → m_kWorldBound (PUSH @0x007C06C1, `LEA ECX,[EBP+0x28]` @0x007C06C6).
- **Porównanie z Gb12_Source\CoreLibs\NiMain\NiAVObject.cpp:842-856 (GetViewerStrings)**: kolejność 1:1 (m_bAppCulled → m_localTranslate → m_localRotate → [m_fLocalScale] → m_worldTranslate → m_worldRotate → m_kWorldBound) ✓✓.
- Spot-check offsetów vs Gb12 layout (NiBound@+0x28=16B → NiTransform m_kLocal@+0x38 {rotate@+0x38, translate@+0x38+0x24=+0x5C, scale@+0x68} → m_kWorld@+0x6C {rotate@+0x6C, translate@+0x90, scale@+0x9C}): binarium +0x20(culled)/+0x28(bound)/+0x38/+0x5C/+0x68/+0x6C/+0x90 — **pełna zgodność strukturalna** ✓ („local +0x38/+0x5C/+0x68, world +0x6C/+0x90/+0x9C" z raportu potwierdzone).
- Ścieżka: 03_EVIDENCE\VA_EVIDENCE_REGISTRY.md E.1; 01_RAW\ghidra_output\GA2_DISASM_FUN_007c04f0.txt; D:\gamebyroengine\extracted\Gb12_Source\CoreLibs\NiMain\NiAVObject.cpp (linie 842-856); qc_probe\qc_region_dump.py.

### A10. „9.3.5 nie ma Sector/Region/Entity" — **PASS** (negatyw potwierdzony surowym skanem całego pliku)
- Własny skan **całego pliku** (wszystkie sekcje, surowe substringy bez wymogu terminatora — poprawka metododyczna względem skanu z terminatorem NUL, który nie widzi nazw RTTI `.?AVName@@`): **Sector = 0, Region = 0, Entity = 0** trafień (również 0 w type-descriptorach `.?AV*`) ✓✓; **Sectors.xbc = 0, Objects.pak = 0, Planets.pak = 0** w binarium oraz w pcg_install (rekurencyjne szukanie plików: 0 wyników) ✓.
- **ArkPortalCell OBECNY**: 3 wystąpienia surowego stringu w .data (TD @0x00B716E4, 0x00B973C0, 0x00B97440 — region type-descriptorów RTTI) ✓; dodatkowo TD '?AVArkPortalPortal@@' — przestrzeń portalowa istnieje, sektorowa nie.
- Ścieżka: 02_ANALYSIS\Z5_WORLD_LOADERS_Z1_RTTI.md; 01_RAW\S1_RTTI_CENSUS.json (census executora — kluczowe pozycje potwierdzone własnymi skanami); qc_probe\qc_scan_text.py, qc_a10_b9.py.

---

## FINDINGS (RUN A)

### **P3-1: niespójny blok pomocniczy w S9_BYTE_VERIFY.json (models_bnt_name_check)**
- **Źródło**: 01_RAW\S9_BYTE_VERIFY.json → sekcja `models_bnt_name_check`: "296445.nif": count 0 / first_offset -1 (analogicznie 460563/460564).
- **Skutek**: artefakt S9 wewnętrznie przeczy kalibracji z 03_EVIDENCE\VA_EVIDENCE_REGISTRY.md E.7 („296445.nif@395,268,773 = 1 hit … 126740.nif@395,268,719 = 1, 278453.nif@395,268,746 = 1"). Czytelnik bazujący na samym S9 uznałby kalibrację za nieudaną.
- **Dowód niezależny (mój skan Models.bnt, 395,412,868 B)**: 296445.nif = 1 hit @395,268,773 ✓; 126740.nif = 1 @395,268,719 ✓; 278453.nif = 1 @395,268,746 ✓ (z terminatorem LF i bez terminatora); **460563.nif = 0 hitów** (bez term./LF/NUL) ✓. Rejestr E.7 ma rację; blok S9 to nieudany skan z błędnym terminatorem (prawdopodobnie NUL), zamieszczony bez etykiety metody.
- **Poprawka**: dopisać do S9_BYTE_VERIFY.json adnotację, że `models_bnt_name_check` jest skanem z błędnym terminatorem (wyniki void), a wiążącym skanem nazw jest skan z terminatorem 0x0A udokumentowany w E.7; albo usunąć blok. NIE modyfikować wyników (append-annotation).
- **Rewalidacja**: powtórzenie mojego skanu (LF) — 3/3 offsety zgodne z E.7, 460563=0.

### **P3-2: rejestr VA — 2 wiersze cytują bajty „przy VA" zamiast „w VA"**
- **Źródło**: 03_EVIDENCE\VA_EVIDENCE_REGISTRY.md:
  - wiersz E.3 „ctor ArkModelResourceInstanceRef | 0x006FA8B0 | `c7 00 b8 64 a8 00`…" — bajty przy entry 0x006FA8B0 to `8b c1 8b 4c 24 04`; cytowana instrukcja `c7 00 b8 64 a8 00` (MOV [EAX],0xa864b8) znajduje się @0x006FA8BC (+0x0C w body). Substancja (vft 0x00A864B8, item@+0x08, RET 4) — potwierdzona bajtowo.
  - wiersz E.2 „wywołanie w FUN_00567770 (ECX=lokal @ESP+0xB4) | 0x00567906 | `8d 8c 24 b4 00 00 00`" — LEA ECX,[ESP+0xB4] stoi @0x005678FF; @0x00567906 jest `e8 85 96 1c 00` = CALL FUN_00730f90 (setter pozycji). Substancja (rekord lokalny @ESP+0xB4 → setter pozycji) — potwierdzona bajtowo.
- **Skutek**: rejestr sugeruje, że cytowane bajty leżą pod podanym VA; reproducibility obniżona, twierdzenia fałszywe NIE są.
- **Poprawka**: w obu wierszach podać dokładne VA instrukcji (0x006FA8BC; 0x005678FF + zaznaczenie CALL @0x00567906→FUN_00730f90).
- **Rewalidacja**: moje dumpy regionów (qc_region_dump.py) — bajty zgodne z powyższym.

### **P3-3: rejestr VA cytuje nieistniejący artefakt**
- **Źródło**: 03_EVIDENCE\VA_EVIDENCE_REGISTRY.md, wiersz E.2 „wywołanie w FUN_00567770 … | S9-read + GA8_PSEUDO_00567770.txt (GA5)".
- **Skutek**: plik `GA8_PSEUDO_00567770.txt` **nie istnieje** w 01_RAW\ghidra_output (Glob: 0 trafień) — odwołanie do artefaktu wskazuje w próżnię; twierdzenie (LEA/calle w FUN_00567770) jest jednak prawdziwe i potwierdzone: moim dumpem regionu 0x005678E0-0x00567940 (wiele LEA ECX,[ESP+0xB4] + CALL-e, w tym do f60/f90/fb0/fd0) oraz disasmami runu B (ZS2_DISASM_FUN_00567770_setter_calls.txt / _attr_reads.txt).
- **Poprawka**: podmienić wskazanie artefaktu na istniejące (S9 + własny disasm okna z E.2, albo ZS2 runu B z zaznaczeniem cross-run) lub dodać brakujący dump jako uzupełnienie (append-only).
- **Rewalidacja**: Glob `**/GA8_PSEUDO_00567770*` w 99_Audits → 0 plików; mój region-dump potwierdza treść twierdzenia.

---

## Bramki runu (weryfikacja niezależna)
- **GA-CLASSIFY: PASS — potwierdzone** (census 25+13 identyczny bajtowo z moim; klasyfikacje sample'owane 5/5 z dowodem bajtowym; STATIC_WORLD=0; UNKNOWN=1 z powodem).
- **GB-PATTERNS: PASS — potwierdzone** (3/3 = disp32; instrukcje i granice odtworzone; pełny skan 3/0/0).
- **GC-BACKWARD: PASS — potwierdzone** (slice S-A: settery+f60 + FUN_00567770 + FUN_00846840 (switch LEA −0x6A4) + rejestracja FUN_00457930 — wszystkie ogniwa bajtowo; slice S-B: FUN_006cb6f0→pump→ref→FUN_006cb020→FUN_006f33a0 — wszystkie ogniwa bajtowo; wykluczenia #1-#5 zgodne z bajtami/dumpami; granice jawne).
- **GD-LOADERS: PASS — potwierdzone** (negatywy Sector/Region/Entity/Sectors.xbc/Objects.pak/Planets.pak = 0 w binarium i instalacji; ArkPortalCell obecny; "portals.bnt"/"TerrainEditZones.bnt"/"NetImmerseScene::Root"/"m_ContainsPortals" stringi obecne na cytowanych VA).
- **GE-ERA: PASS — potwierdzone** (S0 odtworzone własnym parserem co do bajtu; wszystkie VA z tego binarium; Gb12 użyty wyłącznie jako oracle — porównanie A9 wykonałem niezależnie i potwierdziłem zgodność).

## NOT_CHECKED (w moim QC — jawna lista)
1. Pełna dekompilacja FUN_0052d6d0 (44 KB; Ghidra executora timeout) — zgodnie z runem: nieistotna dla wniosku (wzorce = offsety stosu); nie dekodowałem jej funkcji dalej.
2. S1_RTTI_CENSUS.json (1,970 TD) — pełny recount nie wykonany (560 KB); kluczowe pozycje (Sector/Region/Entity=0; ArkPortalCell=3; Ark*) potwierdzone własnymi skanami surowymi.
3. S4_RTTI_VTABLES.json (41 klas) — pełna enumeracja nie powtórzona; head-y kluczowych vtable (ArkObject 0x00A86B48, ArkObjectClass 0x00A86850, ArkPortalCell 0x00A91CF8, ArkModelResourceInstanceRef 0x00A864B8, NiAVObject, NiNode, ArkSceneObject) zweryfikowane własnymi dumpami.
4. Zawartość TerrainEditZones.bnt (bez zmian — NOT_CHECKED runu) i pole aux int64 indeksu BNT (bez zmian — NOT_CHECKED runu B).
5. Wirtualne ciała providerów poza create→store-read (residuum RUN 3 — bez zmian).
6. Wszystkie 38 wierszy klasyfikacji czytane; dowody bajtowe wykonane dla 5 sample'ów (wymagane 3) + pełny census VA — pozostałe 33 wiersze weryfikowane spójnością censusu i tabelą (dowody z dekompilatów GA4-GA8 istnieją w run-dir, nie czytałem każdego w całości).
7. Runtime (klient/sieć/mock) — zakazane; nie dotyczy.

## Integralność evidence executora
Sole zapisy QC w katalogu runu: 06_REPORT\QC_REPORT.md (ten plik) + 00_CONTROL\qc_probe\* (narzędzia własne). Pliki executora nietknięte — hashe kluczowych plików pobrane PO zakończeniu weryfikacji (odczyt-only przez cały QC): REPORT.md = 837332C04D49CBF1592EBE53BBD562E3889A63A7B94B672E756D9CB086CF53BD; S9_BYTE_VERIFY.json = 47939E082EA7725A2F8D340B44E8DD8142490876ECF2B77A002B2F63B45D0046; Z2_CLASSIFICATION_TABLE.md = D5864C6F7B966E640E5403A1EE91504A4B4C19D17C4FF40085BC660BD46B2761; VA_EVIDENCE_REGISTRY.md = 604DDB62724AE9658C09F12C729C98111583986376F282CF786FA3173F4FECC1 (pełny wykaz przed/po w handoff QC).

**QC_VERDICT_RUN_A: QC_PASS** — 0×P0, 0×P1, 3×P3 (korekty dokumentacyjne: adnotacja do bloku S9, 2 wiersze rejestru VA, wskazanie nieistniejącego artefaktu). Wszystkie twierdzenia nośne runu potwierdzone niezależnie bajtowo.
