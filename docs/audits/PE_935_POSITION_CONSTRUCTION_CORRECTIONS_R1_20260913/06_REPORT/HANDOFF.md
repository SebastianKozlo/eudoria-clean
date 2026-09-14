# HANDOFF — PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913

**Do:** PE-MASTER · **Od:** pe-reconstruction (wykonawca) · **Status pakietu:** komplet lokalny, gotowy do QC i adjudykacji; **publikacja = osobny krok** (pe-master-auditor; wykonawca nie commituje).

## RUN_STATUS: PASS_WITH_BOUNDARY

Główne pytanie (kontrakt §2): **dostawca korekty Z prowadzi do RUNTIME'U TERENU (MaTerrainManagerRuntime, RTTI) — łańcuch domknięty do seamu resource-resolution; tożsamość instancja→model NIE została domknięta do modelu (SceneFeeder→NiAVObject = NOT_DEMONSTRATED); 4508/296445 = OPEN.**

## Bramki (STAGE_ACCEPTANCE_GATES.csv — pełne)

| Bramka | Status | Granica |
|---|---|---|
| G1-ERA | PASS | — |
| G2-F1-GRAMMAR | PASS | rozjazd off-by-one pinów epilogów (D-3); semantyka pól struktury bez konsumenta = OPEN |
| G3-F2-X87 | PASS | tabela = model instrukcji (STATIC-ONLY); EXISTING-korekta bez bramki = nowa wiedza |
| G4-F3-ERRATA | PASS | edycja entrypoint wykonuje publikator |
| G5-P2-PROVIDER | PASS | format komórek terenu za seamem; osie/jednostki nierozstrzygnięte; stan-1 mgr1+0 UNPROVEN |
| G6-P3-BINDING | PASS_WITH_BOUNDARY | SceneFeeder→model NOT_DEMONSTRATED; 19 ctor-callers NOT_CHECKED; transform→SF = kopia wartości ctor-time |
| G7-IMMUTABLE | PASS | przed==po (composite A606CF52…); experiments/ nietknięte |
| G8-PUBLICATION | BLOCKED_BY_PROCESS | publikacja po adjudykacji (wykonawca przygotował komplet + draft wiersza entrypoint) |

## Adjudykacja F1/F2/F3 (desktop)

- **F1 ACCEPTED** (gramatyka FUN_007343E0 — potwierdzona bajtowo + suita 28/28; rafinacja dst+04=0.0 zero-init 9×f32).
- **F2 PARTIAL→ACCEPTED+:** CREATE potwierdzone w 100%; **nowe poza twierdzeniem Desktopu: EXISTING-path (FUN_0085B3E0) stosuje tę samą korektę Z bez bramki wariantu przed korektą + drop-to-ground (0.1×≤100, sonda mgr2) + finalny vtable[+4](pozycja, flaga)**; Desktop nie twierdził inaczej (nie błąd — rozszerzenie).
- **F3:** korekty narracyjne ACCEPTED (ERRATA_R5 T-01..T-32, wszystkie disposition); T-15 PARTIAL (8→9×f32); T-29 PARTIAL (fraza OK, całość wiersza GB4 nie); T-18 NOTE (git history immutable).

## Rozjazdy pinów AUDITOR_EXPECTATION (do adjudykacji PE-MASTER)

1. **§12.4: FUN_00413340 → FUN_00413440 (EnterCriticalSection-thunk `51;FF15[0xA75064];C3`) / FUN_00413450 (LeaveCriticalSection `51;FF15[0xA7506C];C3`)**; 0x00413340 nie jest startem funkcji. Importy rozstrzygnięte własnym parserem IAT (IMPORT_RESOLUTION.json).
2. **D-3: epilogi FUN_007343E0** — MOV EAX,ESI @0x0073459C i @0x007345B5 (Desktop: 0x0073459B/0x007345B4 = POP EDI — off-by-one); tail start @0x00734597/@0x007345B0.
3. **D-1 CLOSED (rozstrzygnięcie PE-MASTER potwierdzone):** okno 0x004C4780-0x478F z EXE bajt-identyczne z independent_hexdumps.txt:69 (16 B, dd d9 @0x004C4783-84) — „Desktop hexdump window re-verified byte-identical with EXE; D-1 closed as PE-MASTER reading error" (REPORT §8); ERRATA_R5 bez twierdzeń o brakujących bajtach; potwierdzony defekt = tylko off-by-one T-26.
4. **D-2 CONFIRMED:** „0x004C4744-45" = bajty `05 74` (środek CMP ESI,5/JE); właściwy pośredni CALL = FF D0 @0x004C4874-75.
5. **D-4 READY:** literówka „undeoded" @entrypoint:31 offset 3818 — poprawka w tej samej edycji wiersza co T-08/T-16 (wykona publikator).

## Kluczowe artefakty (ścieżki)

- `00_CONTROL/RUN_CONTRACT.md` (SHA zweryfikowany) + skrypty + `SCRIPT_SHA256.csv`
- `00_CONTROL/GHIDRA_LOCAL/` (własna kopia; AT_COPY==źródłowy FINAL 10/10) + `GHIDRA_LOCAL_MANIFEST_at_copy.csv` / `GHIDRA_LOCAL_MANIFEST_final.csv`
- `01_RAW/` — dekody własne (F*.txt, X*.txt, D1_WINDOW), `S0_ERA_ASSERTION.json`, `F1_MASK_SUITE.json`, `F2_X87_TABLE.json`, `P2_CENSUS*.json`, `F1_CONSUMER_CENSUS.json`, `IMPORT_RESOLUTION.json`, `G7_CENSUS_before/after.json`, `DECOMP_P2/` (67 dekompilatów)
- `02_ANALYSIS/` — `ERRATA_R5_QUOTES.json`, `ERRATA_LIVE_SCAN.json`, `RESEARCH_FINDINGS_WORKING.md` (roboczy, odrębny)
- `06_REPORT/` — `REPORT.md`, `ERRATA_R5.md`, `QC_REPORT.md` (SELF_CHECK), `HANDOFF.md`, `STAGE_ACCEPTANCE_GATES.csv`, `artifact_index.csv`, `MANIFEST_SHA256.csv`, `SOURCE_IDENTITIES.json`
- Odpowiedź na pytanie dispatchu: **repo-wide scan T-01..T-32 — 0 żywych kopii poza rejestrem** (ERRATA_R5 §4; wszystkie trafienia = cele rejestru lub wewnętrzne warstwy pakietów historycznych; jedyna wymagana edycja poza pakietami = AUDIT_ENTRYPOINT.md wiersz 31).

## Otwarte kwestie + JEDEN następny eksperyment

Otwarte: (1) SceneFeeder→model (sloty vtable 0x00A7D458: FUN_0050A460/FUN_005090A0/B0/FUN_0050A050/FUN_005090C0/FUN_00509580) — transform poprawiony osiąga SF+0x34 kopią, ale droga dalej do NiAVObject/model-resource nie zdekodowana; (2) format komórek terenu (named resources, tag 0x6E) za seamem FUN_00415670→FUN_00823C10; (3) 4508/296445 OPEN.

**JEDEN następny eksperyment (STATIC):** zdekodować sloty update **SceneFeederObject** (vtable 0x00A7D458) pod kątem konsumenta [SF+0x34..0x3C] (poprawionej pozycji) i powiązania [SF+0x30] (obiekt 0x118) z systemem modeli — test rozróżniający: jeśli slot konsumuje SF+0x34 i przekazuje do węzła scenowego 0x118, transform→model jest domknięty JEDNYM łańcuchem; jeśli nie — ścieżka modelu biegnie wyłącznie kanałem atrybut-drzewa (pump 0x66), co rozdzieli transform od modelu i utrzyma NOT_DEMONSTRATED.

## Git

HEAD == BASE_SHA `e30f99fdb3c7913c3c4fa6ee1571e505955192d1`; zero commitów wykonawcy; `?? experiments/` (obcy) nietknięty; src/game/ nietknięte.

## NOT_CHECKED (jawne)

- 19 ctor-callers (poza ścieżką +0xC0 — kontrakt G6 boundary).
- Format/pliki komórek terenu (resource format) — za seamem.
- FUN_0093F710 (wewnętrzny side-effect provider2), FUN_0085D240/FUN_00861330 (sub-obiekty value+0xC/+0x10), FUN_0050A0B0/0x50A0D0 (tail-callees FUN_0044CC60/CCA0), pisarz mgr3+0 (stan-1 provider1).
- RTTI Klasy holdera (FUN_0048CBB0-result) i mgr2/mgr4 (identyfikacja strukturalna bez RTTI w tym runie).
- Wykonanie silnika-klienta — NIEOBECNE z definicji trybu (żadna tabela nie jest pomiarem procesora).

## FULL_READ_LOG (komplet)

Pełna lektura (od wejścia do wszystkich wyjść):
1. `RUN_CONTRACT.md` — 776/776 linii (2 tury: start + re-lektura §12 przed raportem).
2. Pakiet Desktop `AUDYT.md`/`REPORT.md` (pełne; zidentyczne bajtowo), `independent_hexdumps.txt` (struktura + linie 61-76), `probe.json` (sekcja positionAdjustment l.~1930-2050), `PROMPT_OPENCODE.txt` (pełne).
3. Faza B: `REPORT.md` (199 l.), `ERRATA_R4.md` (266 l.), `QC_REPORT.md` (331 l.), `HANDOFF.md` (100 l.), `STAGE_ACCEPTANCE_GATES.csv` (16 w.), `RESEARCH_FINDINGS.md` (139 l.), `SEAM_FLOW_MAP.md` (82 l.), `KEY_MODEL_MATRIX.md` (67 l.), `00_CONTROL/*` manifesty (AT_COPY/FINAL GHIDRA_LOCAL), `01_RAW/T6_BYTE_PINS.json`.
4. Faza A: `PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1/06_REPORT/REPORT.md` (250 l.), `ERRATA_R3.md` (410 l.), `RECEIVER_MATRIX.md`, evidence QC.
5. `AUDIT_ENTRYPOINT.md`: wiersz 31 w całości (pełna linia) + nagłówek; reszta tabeli — grep-status (STATICS/statyk/4508/296445/sub-kursor/sub-pakiet/0x004C4875/undeoded).
6. Skill: `pe-reconstruction/SKILL.md` (pełny) + `references/terrain_provider_discovery.md` (kontekst).
7. Własne dekody (capstone): FUN_007343E0/007453D0/007345C0/004C32F0/0040DE60/00412430/004C46C0/004C47F0/004154F0/00853A80/00755F90/00413340-region/00413440/00413450/0085B3E0 (pełne)/0085B750/0085ADB0/00528E50/005247C0/00509330/00414130/004C4640/00765930/008550C0 (pełne)/00855340/0048EF00/00413590/004134F0/0048E7D0/004147F0/0044C9F0/0044C950/00934540/00936A60/00936C30/00935870-region/00934670/0085B1B0 (pełne)/00746560/004123D0-region/0085B0F0/0045AC90-region/0044CC60-0044CEE0/0044D0F0-region/0045B150-region/00538B70/005094C0/005094E0/00509510/006B22D0/00853A50/00853A60/00797280/00856800-region/00853C10 + regiony importów.
8. Ghidra DECOMP_P2: 67 funkcji (census warstwa pomocnicza).

Skanowane (nie pełna lektura, jawne): wyniki censusów (P2_CENSUS*.json), SUITA/RTTI JSON-y, struktury .rdata vtable.

*Powrót do PE-MASTER; adjudykacja pinów §12.4/D-3 oczekuje na decyzję.*
