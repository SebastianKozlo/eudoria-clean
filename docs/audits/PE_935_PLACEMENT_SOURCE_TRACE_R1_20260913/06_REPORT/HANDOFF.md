# HANDOFF — PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913

- **AUDIT_OUTPUT_ROOT**: `D:\Eudoria_Reconstruction\99_Audits\PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913\`
  (repo mirror: `docs/audits/PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913/`)
- **FINAL_REPORT_PATH**: `06_REPORT\REPORT.md`
- **PRIMARY_EVIDENCE_PATHS**:
  - `01_RAW\S0_ERA_ASSERTION.json` (fail-closed era)
  - `01_RAW\S14_VA_EVIDENCE.json` (64 VA→raw-bytes)
  - `01_RAW\ghidra_output\ZS1..ZS10_*` (10 tur Ghidry: pseudo/callers/disasm/S5-walidacja)
  - `01_RAW\S5_IMMEDIATE_SCAN.json` + `ZS1_S5_VALIDATION.json` (ID atrybutów 42 kandydatów → instrukcje)
  - `01_RAW\S11B_PORTALS_INDEX.json` + `S12_PRT_CONTENT_CHECK.json` (276 .prt; negatyw ID)
  - `01_RAW\S9_GETTER_STUB_SCAN.json` (getter D: 8B 41 10 C3 @0x0048ADA0)
  - `01_RAW\S13_CWO_HANDLER_TABLE.json` (tabela .rdata z FUN_00514EF0)
  - `03_EVIDENCE\VA_EVIDENCE_REGISTRY.md` + `MANIFEST_SHA256.csv` (350 plików)
- **RUN_STATUS**: PASS_WITH_BOUNDARY (wszystkie bramki ocenione; granice jawne)
- **HARD_STOP_REASON**: brak (żaden HARD STOP nie zadziałał; klient/sieć/mock NIE
  uruchomione; oryginały READ-ONLY; obce runy nietknięte; brak pod-agentów)
- **Bramki**: G1-PRODUCER PASS_WITH_BOUNDARY | G2-CWO PASS | G3-PORTALS PASS |
  G4-D-FIELD PASS_WITH_BOUNDARY | G5-ERA PASS | G6-GENERALITY PASS
- **WERDYKT-ŹRÓDŁO (1 zdanie + status)**: Transformacje rekordów placementu statyków
  są czytane WYŁĄCZNIE z klienckiego drzewa atrybutów (0x6A4/0x6A5/0x6A8/0x6A9), ale
  FIZYCZNY producent danych pozycji statyku nie został statycznie domknięty —
  3 kanały zskanowane (FILE: store "Data\Parameters\" + parsery VFS, ale brak
  pliku-placementów w census; NETWORK: CommunicationSubsystem→executor→case 0xB9
  →builder istnieje, lecz warstwa pakietowa = protokół połączenia, a producent 0xB9
  jest rejestrowany dynamicznie; DERIVED/LOCAL: 53 call-site'y settera w kodzie
  world-object) — **UNKNOWN-with-exact-boundary; H3 nieudowodnione, H1 bez pozytywu,
  H2 udowodniona jako propagacja, H4 nie wykluczone (0xB9 = główny kandydat)**.
- **Kluczowe nowe VA** (tego runu):
  - Z1: FUN_00845F70 (setter atrybutów; 53 callerów), FUN_00413440/50 (locki),
    FUN_008544D0 (resolve klucza→[hit+8]), FUN_008550C0 (ctor managera 0x8c),
    FUN_00413590 (CriticalSection), FUN_00846430 (filtr transformu),
    FUN_0043F4B0 (dispatcher zmian: attach modelu, skala 1.0, attr 0x39/0x42),
    FUN_005146B0 (propagacja), FUN_004387A0 (setter 0x6a5), FUN_00847270
    ({0x6a4/0x6a5→0x619fa; 0x6a8/0x6a9→0x619f9}), FUN_008553D0 (konstruktor-walker),
    FUN_0094DFC0/0094FE00 (store "Data\Parameters\"), FUN_00972DF0 (VFS reader);
  - Z2: FUN_00419DD0 (CommunicationSubsystem ctor, RTTI verbatim; executor@+0x28),
    FUN_004B15F0/004B2950/004B18D0/004B1890 (executor: ctor/Execute/dispatch 0xA2–
    0xC6/enqueue; **case 0xB9**), FUN_005B72C0 (handler 0xB9), FUN_0058DB50,
    FUN_00514EF0 (handler transform — tabela .rdata **0x00A7D764**; xref-DATA
    @0x00A7D778), FUN_0040DE60 (kursor; 703 call-site'y), FUN_00752700/00752640
    (odczyt wpisów kolejki), FUN_0040E0D0 (klon payloadu), tabele 0x00A7D8EC/
    0x00A7DA34 (74/72 handlerów CWO-Logic);
  - Z3: FUN_0084B270 (fabryka slot1: create+parse), FUN_00852A90 (item ctor;
    CellGraph@+0x10), FUN_00852750 (**parser grafu .prt**: u16→sub→u32 count→cells),
    FUN_00852A30 (tag-reader, slot1 komórki), FUN_00852BF0/00852D60 (czytniki pól);
  - Z4: **FUN_0048ADA0 (getter D dword, 8B 41 10 C3)**, **FUN_00861240 (getter D f32,
    D9 41 10 C3)**, FUN_006B22D0 (getter C), FUN_00567B40 (consumer D w push kolejki);
  - Z1-sieć: FUN_00833EA0 (odbiór: ntohl/ramki 0x11–0x13), FUN_008310D0 (ArkStaticPacket
    = protokół POŁĄCZENIA), FUN_00839A50 (chunk 0xFE);
  - RTTI-nowe: vtable'e ArkParameter* (Container 0x00A8784C/create FUN_0073A160,
    Transformation 0x00A877DC/FUN_00739E30), ClassImpl-y create (RealWorldItem
    FUN_0073A9E0, Provider FUN_0073AAF0, Interactive FUN_0073A8D0),
    ArkPortalResourceItemFactory 0x00A91C88, executor vtable 0x00A7C1FC.
- **Commit**: path-limited docs/audits/PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913/
  (350 plików; GHIDRA_LOCAL LOCAL-ONLY pod manifestem) + AUDIT_ENTRYPOINT.md
  (+1 wiersz, 0 usunięć); SHA + push-status: patrz commit `git log -1`.
