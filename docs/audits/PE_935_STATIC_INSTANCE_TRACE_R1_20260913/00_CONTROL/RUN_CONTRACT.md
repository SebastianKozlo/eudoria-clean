# RUN_CONTRACT — PE_935_STATIC_INSTANCE_TRACE_R1_20260913

## Zlecenie (człowiek §7–§8, §10–§11, przez PE-MASTER)
W Entropia.exe EU 9.3.5 ustalić, JAK kod tworzy instancję statycznego obiektu świata (budynek)
i skąd pochodzi jej transformacja. RUN_CLASS: LOAD_BEARING. STATIC-ONLY:
zakaz uruchamiania klienta/sieci/mock-serwera; statyczne badanie kodu sieciowego dozwolone.
NO_NESTED_TASKS.

## Kanon startowy (zweryfikowany w S0 tego runu)
- Binarium: D:\Eudoria_Reconstruction\pcg_install\Entropia.exe
  SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31, 8,015,872 B,
  image base 0x00400000, brak ASLR.
- Repo: D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean
  BASE_SHA = e8b8ba0fe421f6049a76695031418a35004530dc (HEAD==origin/master — zweryfikowane).
  DIRTY: ?? experiments/ obcej sesji EU1030 — POZA ZAKRESEM, NIETKNIĘTY.
- Poprzedni łańcuch (PE_935_TEMPLATE_CONSUMER_TRACE_R1): templates.vfs reader → parser A→+0x08
  (FUN_00730c90) → registry (FUN_0072f8d0, DAT_00ba1824) → lookup (FUN_0072f580) →
  getter A (FUN_007ce1e0) → żądanie {0x66=MODEL, id=A} (FUN_006c9700) →
  ArkResourceManager (FUN_00415670) + dispatcher (FUN_00823c10).
  Kompletny konsument A→model = FUN_006b4c50 (+ wariant FUN_00511070 z hardcodem 11769 @0x00511245,
  rodzina 11655/11656/11657).
- Census (z 01_RAW poprzedniego runu, re-weryfikowane bajtowo w tym runie):
  25 call-site'ów lookupu (FUN_0072f580) [S10_LOOKUP_CALLERS.json],
  13 call-site'ów pumpu (FUN_006c9700) [S20_MODEL_REQUEST_CALLERS.json].
- DATA: T=5,438 template'ów; A≠0: 3,618 unikalnych; join A→<A>.nif 3,618/3,618.
  Przypadek przewodni: template 4508 → A=296445 (B_Eu_Slum_Building_b047_01).
- ZROZUMIAŁE NIEPEWNOŚCI (errata R2): fizyczne otwarcie zasobu = STRONGLY_SUPPORTED;
  instancja+transform = UNVERIFIED; network-first dla statyków = odrzucony jako ZAŁOŻENIE
  (precedens DAoC/WarEmu: statyczne miasta CLIENT-SIDE; pakiety create = encje dynamiczne).

## Hipotezy (bez zwycięzcy z góry)
H1 LOCAL (dane lokalne zawierają placementy), H2 LOCAL_DERIVED (sektory/komórki/reguły),
H3 NETWORK (transformacje z sieci), H4 HYBRID. Dowód z kodu decyduje.

## Zadania
- Z1: census RTTI klas Ark*/keyword z .rdata (z VA).
- Z2: klasyfikacja 25 lookup + 13 pump call-site'ów (STATIC_WORLD/AVATAR_EQUIPMENT/PREVIEW_UI/OTHER/UNKNOWN)
  z dowodem z dekompilacji callera; kwalifikacja FUN_006b4c50 (a); wniosek o ścieżce STATIC_WORLD (c).
- Z3: 3 wzorce 4508 w .text @0x0053270C, 0x00532769, 0x0083427E (granice instrukcji, operand,
  funkcja, xref, dataflow; template-hardcode czy przypadkowa stała 0x119C).
- Z4: ślad wstecz od world-transform-setterów (separacja: zasób NIF vs manager vs instancja vs
  rodzic przestrzenny; wykluczenia fałszywych trafień z powodem; Gb12_Source = oracle SEMANTYKI setterów).
- Z5: loader-y świata (world/sector/zone/cell/region/environment/portal/edit-zone/vegetation)
  po stringach i klasach z Z1; plik/wejście → co tworzy.
- Z6: ciała provider/factory TYLKO jeśli łączą instancję z zasobem (VA-locked create→store-read).
  Placement ma priorytet.

## Kontrole obowiązkowe
- VA/file-offset/raw-byte agreement (każdy VA = surowe bajty; S0 mapping zapisany).
- Round-trip ID (pack→unpack) przed skanem wzorca.
- Drugi przypadek dla ogólności (siblingi 4752/2249 na klasyfikowanych ścieżkach).
- Kontrola negatywna klasyfikacji (STATIC_WORLD ⇒ generyczność, brak 296445-specyfika).
- Oddzielenie transformacji LOKALNEJ od WORLD.

## Bramki (fail-closed)
- GA-CLASSIFY: 25+13 sklasyfikowanych z dowodem; kwalifikacja FUN_006b4c50 rozstrzygnięta.
- GB-PATTERNS: 3/3 wzorców 4508 rozstrzygnięte.
- GC-BACKWARD: ≥1 backward slice od world-transform-set, VA-locked, z granicą i wykluczeniami.
- GD-LOADERS: loader-y świata zidentyfikowane (census stringów+klas; wynik może być negatywny).
- GE-ERA: SHA + mapping + zero transferu PE2.

## NON-PASS / HARD STOPS
- NO_STATIC_CONSUMER_FOUND (ważny wynik negatywny + redirect), TOOL_BLOCKED, SCOPE_CREEP.
- HARD STOPS: runtime/sieć/mock; modyfikacja oryginałów (exe, VFS, BNT, projekty Ghidra obcych
  runów); pod-agenty; praca poza katalogiem runu.

## Wyjście
D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_INSTANCE_TRACE_R1_20260913\
(00_CONTROL, 01_RAW, 02_ANALYSIS, 03_EVIDENCE, 06_REPORT)
+ commit path-limited docs/audits/... + AUDIT_ENTRYPOINT (+1 wiersz) + push.
RAPORT po polsku (9 punktów wg kontraktu).

## GHIDRA_LOCAL
Skopiowany z PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912\00_CONTROL\GHIDRA_LOCAL
(PE935_DISPLAY_ENUM_R1.rep, 361.9 MB) do 00_CONTROL\GHIDRA_LOCAL tego runu.
Binarium w projekcie: Entropia.exe (ten sam SHA — asercja w skryptach).

## Era
EU 9.3.5 (pcg_install, 2008). Wszystkie twierdzenia era-labelled. Zero transferu PE2/2003.
Gamebryo Gb12_Source (D:\gamebyroengine\extracted\Gb12_Source) = wyłącznie oracle SEMANTYKI
setterów transformacji, NIE opis loaderów MindArka.
