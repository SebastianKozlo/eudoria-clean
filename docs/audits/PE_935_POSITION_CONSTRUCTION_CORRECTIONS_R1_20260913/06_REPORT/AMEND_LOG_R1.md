# AMEND_LOG_R1 — PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913

**Wykonawca nowelizacji:** pe-master-auditor (PUBLICATION task, bezpośredni dispatch PE-MASTER; NO_NESTED_TASKS).
**Zakres:** WYŁĄCZNIE ordered pre-publication amendments A-F PE-MASTER do NIEopublikowanych jeszcze deliverables tego runu (warstwa 06_REPORT + draft 02_ANALYSIS). Zero zmian w 01_RAW (evidence), zero zmian w plikach oryginalnych/historycznych, zero zmian poza pakietem (edycja repo = osobny krok publikacji §5).
**Dowody pre-edit:** kopie byte-identical `.pre` w `00_CONTROL/PRE_EDIT/` (hashe poniżej; porównanie przed/po: tylko linie objęte nowelizacją A-F się różnią — weryfikacja maszynowa diff).
**Kodowanie zachowane:** wszystkie nowelizowane pliki = UTF-8 bez BOM, LF-only (weryfikacja bajtowa po każdej edycji: BOM=False, CR=0).

## Hashe plików (SHA256)

| Plik | PRE (== .pre) | POST (po A-F) |
|---|---|---|
| 06_REPORT/REPORT.md | D1B5E34AF6C5AE8E7F256F92197C02AC26DF1007D3C06E3DE821A174D5364C5B | 9373716D3545F5327CB1D363DE701A3609050A94707BEA6F755864C74DBC60B8 |
| 06_REPORT/ERRATA_R5.md | FB54B4F931F06A179EF46D882D5828D4EA12D76801D2E516DD8A3950F982A24F | E4F85EA8E027CD9B8C9BB1E935F822883D53B6488D6EE08D3E457AAC38014F71 |
| 02_ANALYSIS/ENTRYPOINT_ROW_DRAFT.md | 5E4A24C0493C10AE0A64980986D176E54B9B77BD8062242ABCB8B84C50C76602 | 06AC506E7418CFB14ABB2A413BD7558870DD3E49BD38FEF26A693DF7A14610F0 |

Każdy stary fragment zweryfikowany maszynowo jako DOKŁADNIE RAZ (EXACTLY-ONCE) przed podmianą; każdy nowy fragment DOKŁADNIE RAZ po; zero pozostałości starych fragmentów.

---

## A. REPORT.md §2.B(6) — pin zapisu h w ścieżce EXISTING (linia 102)

- **Sekcja:** §2.B(6), punkt „NOWE ODKRYCIE" (EXISTING-path, FUN_0085B3E0).
- **Stary tekst:** „…identyczny wzorzec FCOM/FNSTSW/FSTP ST(1)/TEST AH,0x41/JNE/FSTP [ESP+0x24] @0x0085B43F — zapis h przy h>z ordered…"
- **Nowy tekst:** „…identyczny wzorzec FCOM/FNSTSW/FSTP ST(1)/TEST AH,0x41/JNE (cel JNE @0x0085B43F = FSTP ST(0), odrzucenie h)/FSTP [ESP+0x24] @0x0085B439 — zapis h przy h>z ordered…"
- **Powód (ground):** surowy dowód `01_RAW/F0085B3E0_SET_POS_EXISTING_FULL.txt` linie 33-36: `jne 0x85b43f` @0x0085B437, `fstp dword ptr [esp + 0x24]` @**0x0085B439** (zapis h), `fstp st(0)` @0x0085B43F (odrzucenie h). Poprzednia treść przypisywała zapis h adresowi celu JNE (odrzucenia) — pin był błędny, surowy dowód był poprawny.
- **Zlecenie:** PE-MASTER dispatch PUBLICATION STEP 1.A („PE-MASTER byte-verified"). Klasa: [P3] pin-precision, nie obciąża twierdzenia nośnego (korekta EXISTING bez bramki + zapis h przy h>z ordered — bez zmiany).

## B. REPORT.md §2.B(6) — bit-exactność kroku drop-to-ground (linia 102)

- **Sekcja:** §2.B(6), pętla drop-to-ground (FUN_0085B3E0).
- **Stary tekst:** „krok = qword [0xA7AF80] = **0.1** (f64)"
- **Nowy tekst:** „krok = qword [0xA7AF80] = **0.100000001490116119384765625** (bits 0x3FB99999A0000000, tzn. f64(double(f32 0.1f)), nie kanoniczne f64 0.1 = 0x3FB999999999999A; wartościowo ≈0.1)"
- **Powód (ground):** stała [0xA7AF80] w EXE ma bity 0x3FB99999A0000000 — nie kanoniczne f64 0.1 (0x3FB999999999999A); wartość = 0.100000001490116119384765625 = f64 uzyskany z f32 0.1f. PE-MASTER byte-verified z fizycznego EXE; własna re-weryfikacja audytora w QC_AUDIT_R1 (odczyt 8 B z .rdata EXE).
- **Zlecenie:** PE-MASTER dispatch PUBLICATION STEP 1.B. Klasa: [P3] precision note; wartościowo ≈0.1 — wnioski liczbowe bez zmian.

## C. REPORT.md §3.2 — piny zapisów vtable w FUN_00538B70 (linia 153)

- **Sekcja:** §3.2 (Provider1… MaTerrainManagerRuntime), writer mgr3+0x18.
- **Stary tekst:** „…a FUN_00538B70: `MOV [ESI],0x00A7F430; MOV [ESI+4],0x00A7F420` @0x00538BA9/B5;"
- **Nowy tekst:** „…a FUN_00538B70: `MOV [ESI],0x00A7F430; MOV [ESI+4],0x00A7F420` @0x00538BA9 i @0x00538BAF (0x00538BB5 = ostatni bajt drugiego zapisu);"
- **Powód (ground):** PE-MASTER byte-verified z EXE: `MOV [ESI],0x00A7F430` @0x00538BA9 (6 B); `MOV [ESI+4],0x00A7F420` @**0x00538BAF** (7 B, kończy się @0x00538BB5). Stary pin „0x00538BA9/B5" mieszał start pierwszego zapisu z końcem drugiego (pin VA = START instrukcji — konwencja ERRATA_R3/4/5 reguła 5).
- **Zlecenie:** PE-MASTER dispatch PUBLICATION STEP 1.C. Klasa: [P3] pin-precision; oba zapisy vtable (0x00A7F430/0x00A7F420 — .?AVMaTerrainManagerRuntime@@) — bez zmiany merytorycznej.

## D. ERRATA_R5.md T-08 — dokładny cytat żywego spanu wiersza 31 (linie 69-72 + wstawka)

- **Sekcja:** §1, T-08 (target AUDIT_ENTRYPOINT.md:31).
- **Stary cytat:** „sub-packet via FUN_007343E0: variant u16 @0x00745435 -> rec+0x34, POSITION vec3 12B via FUN_00412430 @0x0074545A -> rec+0x38"
- **Nowy cytat (dokładna treść żywego wiersza):** „sub-packet via FUN_007343E0: variant u16 @0x00745435 -> rec+0x34, **POSITION vec3 12B via FUN_00412430 @0x0074545A -> rec+0x38" (w tym znacznik `**` przed POSITION; bold zamyka się dalej w wierszu, wokół spanu poprawki QC SE-R4-6).
- **Dodatkowe zmiany w tym samym T-08:** (1) nagłówek targetu: „(fragment @offset ~1679; offset = pozycja znakowa wewnątrz wiersza 31):" — jawna podstawa offsetu; (2) tekst „Poprawka" (replacement) zachowuje `**` na tej samej pozycji przed POSITION; (3) nowa linia: „- [AMENDMENT PE-MASTER audit: pierwotny cytat pomijał znacznik '**' obecny w żywym pliku; cytat skorygowany do dokładnej treści żywego wiersza]".
- **Powód (ground):** publikatorowa weryfikacja maszynowa żywego wiersza 31 AUDIT_ENTRYPOINT.md (UTF-8): stary fragment ZE znacznikiem `**` występuje DOKŁADNIE RAZ na pozycji znakowej 1679; fragment BEZ `**` występuje 0 razy (cytat erraty był NIEDOKŁADNY, nie lustrzany vs żywy plik). Offset ~1679 = pozycja znakowa (code point) wewnątrz wiersza 31 — potwierdzone przez PE-MASTER i ponownie przez audytora.
- **Zlecenie:** PE-MASTER dispatch PUBLICATION STEP 1.D + adjudykacja [P2] PUB-TARGET INEXACTNESS T-08. Klasa: [P2] pub-target exactness; konieczne, żeby edycja wiersza 31 w kroku publikacji trafiła DOKŁADNIE RAZ.

## E. ERRATA_R5.md §0 — literówka wersji capstone (linia 16)

- **Sekcja:** §0 „Zasady pierwszeństwa", linia o narzędziach dekodu.
- **Stary tekst:** „capstone 3.12.2026"
- **Nowy tekst:** „capstone 5.0.7"
- **Powód (ground):** nagłówek REPORT.md tego runu nosi rzeczywistą wersję (capstone 5.0.7); „3.12.2026" = slip wersji w ERRATA_R5 §0 (liczba wyglądająca jak data). PE-MASTER dispatch PUBLICATION STEP 1.E. Klasa: [P3] version slip; żadna klasyfikacja dowodu nie zależy od numeru wersji.
- **Nota:** errata celowo NIE było re-hashowane do SCRIPT_SHA256 (brak zmian skryptów w tej nowelizacji; SCRIPT_SHA256.csv bez zmian).

## F. 02_ANALYSIS/ENTRYPOINT_ROW_DRAFT.md — sekcja 1, wiersz T-08 + nota offsetowa

- **Sekcja:** §1 tabela edycji wiersza 31, wiersz @offset 1679.
- **Stary tekst (wiersz T-08):** old-span bez `**` + replacement bez `**` (oba: „…rec+0x34, POSITION vec3 12B…").
- **Nowy tekst (wiersz T-08):** old-span = DOKŁADNY żywy tekst wiersza 31 włącznie ze `**` przed POSITION (jw. D); replacement zachowuje `**` na tej samej pozycji: „structure 0x28 via FUN_007343E0 @0x00745419 (u16 mask -> rec+0x0C; consumption mask-dependent), then SAME-cursor reads: variant u16 @0x00745435 -> rec+0x34, **POSITION vec3 12B via FUN_00412430 @0x0074545A -> rec+0x38".
- **Dodatkowa nota (nowa):** „**Nota offsetowa (AMENDMENT PE-MASTER):** offsety 1679/3594/3818 = pozycje znakowe (char positions) wewnątrz wiersza 31 — zweryfikowane przez PE-MASTER. Każdy stary fragment musi być przed podmianą maszynowo zweryfikowany jako występujący DOKŁADNIE RAZ (EXACTLY-ONCE) — w tym T-08 z żywym znacznikiem `**` przed POSITION (poprawka tekstu zastępującego zachowuje `**` na tej samej pozycji)."
- **Powód:** draft jest instrukcją edycji dla publikatora — span old MUSI być lustrzany z żywym plikiem (inaczej podmiana by nie trafiła); spójność z D (ERRATA_R5 T-08).
- **Zlecenie:** PE-MASTER dispatch PUBLICATION STEP 1.F.

---

## Wpływ na twierdzenia (status)

- Żadna nowelizacja A-F nie zmienia statusu żadnego twierdzenia nośnego runu: F1 CONFIRMED, F2 CONFIRMED+EXTENDED, PHASE 2 chain CONFIRMED (do seamu), PHASE 3 TRANSFORM_TO_SCENEFEEDER CONFIRMED (value copy, ctor-time) / TRANSFORM_TO_MODEL NOT_DEMONSTRATED, 4508/296445 OPEN — bez zmian.
- Klasa findingów: 1x [P2] (T-08 pub-target exactness) + 4x [P3] (A, B, C, E) + nota dokumentacyjna (F) — zgodnie z werdyktem PE-MASTER (MASTER_ACCEPTED advisory; wszystkie findingi rozwiązane pre-publication przez ordered amendments).

## Uwagi publikacyjne (repo copy — LOCAL-ONLY exclusions)

Kopia repo `docs/audits/PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913/` powstaje z Wyłączeniami LOCAL-ONLY (precedens fazy B): katalog `00_CONTROL/GHIDRA_LOCAL/` (projekt Ghidra — NIE publikowany; w repo zostają tylko `00_CONTROL/GHIDRA_LOCAL_MANIFEST_at_copy.csv` i `00_CONTROL/GHIDRA_LOCAL_MANIFEST_final.csv`) oraz `00_CONTROL/__pycache__/`. Kopia repo niesie: 00_CONTROL (skrypty + manifesty + PRE_EDIT), 01_RAW (JSON evidence + dekody txt + DECOMP_P2), 02_ANALYSIS, 06_REPORT. Bez EXE, bez archiwów, bez projektu Ghidra, bez kodu silnika. Manifest po stronie repo (`06_REPORT/MANIFEST_SHA256.csv` i `artifact_index.csv` w kopii repo) listuje DOKŁADNIE pliki obecne w kopii repo (repo-side manifest, zbudowany niezależnie od manifestu pakietu lokalnego; oba manifesty pozostają bez self-row, ścieżki unikalne).

*AMEND_LOG_R1 zamknięty po stronie nowelizacji; zmiany treści poza A-F wymagają nowego dispatchu PE-MASTER.*
