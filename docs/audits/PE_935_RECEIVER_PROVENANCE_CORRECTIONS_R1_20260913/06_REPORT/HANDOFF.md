# HANDOFF — PE_935_RECEIVER_PROVENANCE_CORRECTIONS_R1_20260913

**RUN_CLASS:** LOAD_BEARING | **EXECUTOR:** pe-reconstruction | **INTERNAL_QC +
formalizacja + publikacja:** pe-master-auditor (QC_PASS) | **TRYB:** STATIC-ONLY.
**ERA:** EU 9.3.5 (pcg_install): Entropia.exe SHA256
E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31;
templates.vfs SHA256 BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77.
**RUN_STATUS (finalny): PASS_WITH_BOUNDARY** (executor) + **QC_PASS** (auditor) —
granice RECEIVER_UNRESOLVED jawne (REPORT.md §7). Nie ogłoszono
STATIC_INSTANCE_MECHANISM_CONFIRMED ani źródła placementu; pozycje 296445 NIE odzyskane.

## Odpowiedź główna (1 zdanie)
Getter FUN_007CE1E0 (`8B 41 08 C3`) nie ma jednej semantyki — odczytuje +8 różnych
typów odbiorców (rekord VFS: A=id NIF; ArkObjectClass: ID klasy; wartość mapy
parametrów: wariant; singletony: flagi; rekord placementu: position.X); most RUN3
„templates.vfs.A → ArkObject+0x28" REJECTED w obu ogniwach (odbiorca=klasa,
wartość=numeryczne ID klasy z imm32), a selektor „D=4/5→2, 6→3, 7→4" czyta +8
wartości mapy parametrów, nie D@+0x10.

## Struktura pakietu (warstwy)
- **00_CONTROL\** — narzędzia executora (pe_core.py, f1_*/f2_*/f5_*, ga5_immutable.py,
  rc1_*.py, s0; SCRIPT_SHA256.csv; manifesty GHIDRA_LOCAL: AT_COPY db.63/64 + finalny
  SHA256 db.67/68 — projekt 379 520 056 B LOCAL-ONLY) + **00_CONTROL\qc_probe\**
  (narzędzia QC auditora — 12 plików, własne mapowanie PE od zera).
- **01_RAW\** — evidence executora (F1_ABI_BYTES, F1_REG_ARGS, F1_CENSUS, F1_CTX_*,
  F2_*, F5_*, GA5_IMMUTABLE_{before,after}, GHIDRA_FUNC_ATTR, GHIDRA_REFCOUNTS,
  S0_ERA_ASSERTION) — **NIETYKANE przez QC** (15/15 kluczowych hash przed==po).
- **02_ANALYSIS\** — RECEIVER_MATRIX.md (macierz 7 typów odbiorców), 
  DRAFT_ERRATA_SUPERSESSION.md (materiał erraty — roboczy).
- **03_EVIDENCE\** — pomiary QC auditora: QC_F1_ABI.json, QC_F1_CLASSID.json,
  QC_F1_REGARGS2.json, QC_F1_REGARGS3.json, QC_F1_DAT58CC_POSCONTROL.json,
  QC_F2_SELECTOR.json, QC_F2_VFS_WALK.json, QC_F2_VFS_WALK2.json,
  QC_CENSUS_GETTERS.json, QC_F5_SETTERS.json, QC_GA5_IMMUTABLE.json,
  QC_MATRIX_LINKS.json, QC_FINAL_LINKS.json, QC_F1_CLASSID_PAIRS.md (reguła
  manglingu + 4 pary), **QC_REPORT.md** (pełny raport QC z findings QC-1..QC-7).
- **06_REPORT\** — RESEARCH_FINDINGS.md (raport roboczy executora — ZACHOWANY),
  **REPORT.md** (raport finalny — 7 sekcji per zlecenie), **ERRATA_R3.md**
  (sformalizowany ledger SUPERSESSION z sekcją MANIFEST_VALIDATION_ORDER),
  STAGE_ACCEPTANCE_GATES.csv (GA1–GA6 executora + QC-G1..QC-G9 auditora),
  artifact_index.csv, HANDOFF.md (ten plik). MANIFEST_SHA256.csv w korzeniu pakietu.

## Kluczowe wyniki (F1–F5)
- **F1 CONFIRMED-correction:** łańcuch ABI vtable 0x00A86850→fabryka(PUSH ESI=klasa
  jako arg1 @0x70BF92-96)→ctor klasy([class+8]=arg1 @0x70CFC1)→ctor ArkObject(getter
  [class+8] @0x726EB7 → encja+0x28 @0x726EBC); 55 call-site'ów ctora = **54
  rejestracje param-set z imm32 + 1 lazy-init klasy bazowej (ID 0)**; korelacja
  mangling↔imm32 **36/36** (reguła: `$0`+nibble A=0..P=15); DAT_00BA58CC = singleton
  klasy ArkObjectClassImpl<ArkSurgeonObject,20035> (store @0x73D882); 20006 =
  **ArkParameterCommon** ($0EOCG@; rejestracja @0x73B87D).
- **F2 CONFIRMED-correction:** selektor 0x4E38 czyta **+8 wartości mapy managera
  parametrów** (14/14 instrukcji; tabela 0x00855BB4=[2,2,3,4]; bloki MOV [ESP+0x1C],
  2/3/4); getter D @0x8556DF = odrębna gałąź; walk templates.vfs **5438/0-CRC/EOF**
  (własna reguła stride 36×ceil((16+size)/36)); **D@4508 = 0x42F9E1CB = 124.94100189208984
  @96528, A=296445 @96516**; censusy: D-dword 117 (116 E8+1 E9), D-f32 10,
  FUN_00468910=12; różnice raw/isCall = E9 tail-jumpy (9+1, wszystkie na listach
  Ghidra — mechanizm wyjaśniony przez QC).
- **F3 CONFIRMED-correction:** ANCHORS_ABSENT_SEMANTICS_OPEN; „27 plików ≠ 27 rodzin
  formatu"; 20006=ID KLASY — pliki VFS kandydatem nośnika zasilania; RUN2 D3: pozytyw
  client-side tylko DAoC (dla WAR negatyw).
- **F4 CONFIRMED-correction:** „0/38 = brak dowiedzionej DEDYKOWANEJ roli
  STATIC_WORLD"; FUN_00567170/005B5F90/006CB6F0 = jawni wspólni kandydaci.
- **F5 CONFIRMED-correction:** „WYŁĄCZNIE" → „we wszystkich prześledzonych
  ścieżkach" (predykat = census w ciałach 3×CC); 15 setter-callerów = **9 bezpośrednich
  + 3 parametryczne + 3 singleton-readers** (QC-3); FUN_0046E790 i FUN_00567170 =
  NO_DIRECT_ATTR_CALLS z singletonem FUN_004154F0, provenance NIEROZLICZONA;
  26/24 ctor-callerów: 5 z setterami, **19 bez (NOT_CHECKED, lista VA w ERRATA_R3
  [SE-8])**.

## Findings QC (pe-master-auditor; pełny opis: 03_EVIDENCE\QC_REPORT.md)
- **P2 QC-1:** „55 rejestracji z imm32" → 54 imm32 + 1 lazy-init (arg1=PUSH 0);
  wpis F1_REG_ARGS 0x7262B7 z imm=0xA7957B = artefakt (stała stringa).
- **P2 QC-2:** trzy nazwy funkcji „rejestracyjnych" w RESEARCH_FINDINGS §2.3 błędne
  (realne: FUN_00734C40/0070C150/0070BF10) — poprawione w REPORT/ERRATA_R3.
- **P2 QC-3:** SE-6 „10 bezpośrednich" → 9/3/3 (FUN_00567170 bez attr-callow we
  własnym ciele — zlew ciał 3×CC na granicy 0x567170/0x567770).
- **P3 QC-4:** pin „slot3 CALL [vft+0xC] w gałęzi 0x38B0" → wywołanie na wartości =
  [vft+8] @0x00855B2F-3F (inna gałąź); substancja (+0=vtable) potwierdzona.
- **P3 QC-5:** konwencja pinów operandowych (6 przykładów) — errata pinnie starty
  instrukcji.
- **P3 QC-6:** F2_SELECTOR.json „template_4508" = mylący artefakt pierwszego
  przebiegu (autorytet: F2_T4508_WALK.json).
- **P3 QC-7:** GA5 — nota zakresowa (zbiór executora vs „296445-ERRATA" repo-only;
  zero zmian w obu).
Wszystkie P2/P3 klasy dokumentacyjnej — poprawione w warstwie 02_ANALYSIS/06_REPORT
(REPORT.md, ERRATA_R3.md, STAGE_ACCEPTANCE_GATES.csv); evidence 01_RAW nietykane.

## Gałęzie RECEIVER_UNRESOLVED (do Fazy B)
1. Nazwa klasy wartości mapy managera parametrów ([hit+8]).
2. arg1 FUN_00567C50 per-caller (getter D @0x567D16/D46).
3. 19 ctor-callers bez setterów — semantyka NOT_CHECKED.
4. Provenance wartości setterów: FUN_00567170, FUN_0046E790, FUN_005B5F90,
   FUN_0043A200, FUN_00488920, FUN_00459270 — NIEROZLICZONA.
5. Semantyka D=124.941@4508 — ANCHORS_ABSENT_SEMANTICS_OPEN.
**NASTĘPNY EKSPERYMENT:** FORMAT-DECODE 20xxx.vfs + szew parser→insert-map
(rozstrzyga granicę #1 + kanał zasilania klas 20006/20035; STAT-ONLY).

## Provenance i reprodukcja
- Binarium: `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe` (SHA wyżej);
  własne mapowanie PE: image base 0x00400000, ASLR OFF, sekcje .text/.rdata/.data/
  .tls/.rsrc (S0_ERA_ASSERTION.json + QC_F1_ABI.json.pe).
- Generatorzy evidence: 00_CONTROL\*.py (executor; SCRIPT_SHA256.csv po ostatniej
  edycji) + 00_CONTROL\qc_probe\*.py (auditor; census w artifact_index.csv).
- Komendy: python <skrypt>.py (każdy zapisuje JSON/txt do 01_RAW executora lub
  03_EVIDENCE QC); Ghidra: analyzeHeadless -process na kopii GHIDRA_LOCAL
  (-noanalysis; 2 tury: rc1_ga_attrs, rc1_refcounts; manifesty AT_COPY/finalny).
- Niezależne źródła prawdy QC: własny parser PE (qc_core.py — napisany od zera,
  niezależnie od pe_core.py), własny dekod x86 (w probe'ach), własny walker VFS,
  własne censusy E8/E9/imm32, atrybucja Ghidra executora skonfrontowana z własnymi
  granicami funkcji.

## Publikacja (git; path-limited)
- Zmienione/nowe ścieżki (dokładnie): `docs/audits/PE_935_RECEIVER_PROVENANCE_
  CORRECTIONS_R1_20260913/**` (kopia pakietu BEZ GHIDRA_LOCAL — projekt LOCAL-ONLY,
  w repo jego manifesty SHA — i BEZ __pycache__) + `AUDIT_ENTRYPOINT.md` (+1 wiersz
  LATEST RUNS, 0 usunięć). BASE_SHA 24d7669f7a1e5717ed2b5d5338b70ff4d7daabbe;
  obce `?? experiments/` NIETYKANE. Commit SHA/push status: patrz metadane poniżej
  (uzupełniane po push przez auditora).
- HEAD/push: dokumentowane w metadanych końcowych niniejszego handoffu.

## Metadane końcowe (uzupełnione po publikacji)
- COMMIT_SHA: (uzupełnione po commicie — patrz AUDIT_ENTRYPOINT / git log)
- REMOTE: origin/master — status push: patrz AUDIT_ENTRYPOINT.
- UNRELATED_WORK_EXCLUDED: `?? experiments/` (obce, nietknięte).
