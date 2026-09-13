# HANDOFF — PE_935_STATIC_INSTANCE_TRACE_R1_20260913

- **AUDIT_OUTPUT_ROOT**: `D:\Eudoria_Reconstruction\99_Audits\PE_935_STATIC_INSTANCE_TRACE_R1_20260913\`
  (kopia publikowana: `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\docs\audits\PE_935_STATIC_INSTANCE_TRACE_R1_20260913\`)
- **FINAL_REPORT_PATH**: `06_REPORT\REPORT.md`
- **PRIMARY_EVIDENCE_PATHS**:
  - `01_RAW\S0_ERA_ASSERTION.json` (SHA/PE/ASLR/mapping, fail-closed)
  - `01_RAW\S1_RTTI_CENSUS.json` + `.csv` (1,970 TD-stringów; 483 Ark; 253 Ni)
  - `01_RAW\S2_STRING_CENSUS.json` + `S2_STRING_CENSUS_ALL.txt` (66,298 stringów)
  - `01_RAW\S3_ROUNDTRIP_4508.json` (round-trip 8/8; skan .text 3/0/0)
  - `01_RAW\S4_RTTI_VTABLES.json` (41 klas TD→COL→vtable)
  - `01_RAW\S5_TRANSFORM_WRITES.json` (skan setterów transformu)
  - `01_RAW\S9_BYTE_VERIFY.json` (25+13 call-site'ów: 38/38 bajtowo, 0 mismatch; negatyw 460563)
  - `01_RAW\ghidra_output\GA1_PATTERNS.json` + `GA1_PATTERN_WINDOWS.txt` (Z3, surowe bajty)
  - `01_RAW\ghidra_output\GA1_STRING_XREFS.json` (Z5: xrefy loaderów)
  - `01_RAW\ghidra_output\GA1_IAT.json` (rozstrzygnięcie IAT wzorców)
  - `01_RAW\ghidra_output\GA2_DISASM_FUN_007c04f0.txt` (oracle offsetów NiAVObject)
  - `01_RAW\ghidra_output\GA3_CTOR_INDEX.json` + `GA3_CTOR_*.txt` (konstruktory klas)
  - `01_RAW\ghidra_output\GA3_VTABLE_ENTRIES.json`
  - `01_RAW\ghidra_output\GA4-GA8_*.txt/json` (slice'e S-A/S-B, klaster CWO, upload-chain)
  - `02_ANALYSIS\Z2_CLASSIFICATION_TABLE.md` (38 wierszy z dowodami)
  - `02_ANALYSIS\Z4_BACKWARD_SLICE.md` (2 slice'e + 5 wykluczeń + granice)
  - `03_EVIDENCE\VA_EVIDENCE_REGISTRY.md` (rejestr VA→bajty→artefakt)
- **GHIDRA_LOCAL** (projekt Ghidra PE935_DISPLAY_ENUM_R1.rep, 361.9 MB): LOCAL-ONLY
  (skopiowany z poprzedniego runu do `00_CONTROL\GHIDRA_LOCAL` tego runu; NIE commitowany —
  pokryty manifestem SHA w `00_CONTROL\GHIDRA_LOCAL_MANIFEST_SHA256.csv`).
- **RUN_STATUS**: **PASS_WITH_NEGATIVE** — bramki GA–GE PASS; ważny wynik negatywny
  NO_STATIC_CONSUMER_FOUND na censurowanej powierzchni 25 lookupu + 13 pumpu (0/38
  STATIC_WORLD) z redirectem (system ArkObject + atrybuty + CWO + Portals.bnt/.prt);
  odpowiedź misji CZĘŚCIOWA — warstwy encja+zasób VA-locked, transform: setterzy i źródło
  (atrybuty) zlokalizowane, ale producer kontenera atrybutów i łącze
  atrybuty→węzeł-NIF-statyka NIEROZSTRZYGNIĘTE (granice jawne w raporcie §5, §8).
- **HARD_STOP_REASON**: brak (żaden HARD STOP nie zadziałał; STATIC-ONLY dotrzymany —
  klient/sieć/mock nieuruchomione; oryginały niemodyfikowane; GHIDRA_LOCAL to kopia
  lokalna, projekty obcych runów nietknięte).
- **Wyniki bramek**: GA-CLASSIFY **PASS** (25+13 z dowodem; FUN_006b4c50 = AVATAR,
  rozstrzygnięta; UNKNOWN=1 z powodem) | GB-PATTERNS **PASS** (3/3 = disp32, zero
  imm32-odwołań do 4508) | GC-BACKWARD **PASS** (slice S-A: transform-settery
  FUN_00730f90/fb0/fd0 ← FUN_00567770 ← atrybuty FUN_00846840; slice S-B:
  FUN_006cb6f0→pump→ArkModelResourceInstanceRef→instancja nazwana; 5 wykluczeń
  fałszywych trafień z powodami; granice jawne) | GD-LOADERS **PASS** (census stringów
  + klas z wynikiem, w tym NEGATYW: brak ArkSector/Region/Entity w 9.3.5, brak
  Sectors.xbc/Objects.pak/Planets.pak) | GE-ERA **PASS** (S0 fail-closed; zero transferu
  PE2; Gb12 wyłącznie oracle semantyki).

## Kluczowe rozstrzygnięcia (po 1 zdaniu)
1. ArkObject ctor (FUN_00726e70) pobiera A z obiektu template'u do encji@+0x28 — most
   template→encja statycznej (definicja≠instancja potwierdzone w 9.3.5).
2. Twórca instancji modelu = FUN_006cb6f0: pump {0x66,A} → ArkModelResourceInstanceRef
   (12 B) → FUN_006cb020: nazwana instancja 0x110 B "<id>__<name>" → rejestracja;
   pending-attach domyka asynchroniczne ładowanie.
3. FUN_006b4c50 = konsument AVATAR (body-set; caller FUN_006b9970 z węzłem
   "CharacterPosition") — NIE ścieżka statyków.
4. Wzorce 4508 = 3×disp32 (2× stack LEA w FUN_0052d6d0; 1× pole ctora ArkCommunicator
   FUN_00834010) — hardcode template'u 4508 w .text NIE ISTNIEJE.
5. Transform: setterzy rekordu placementu (FUN_00730f90 pozycja@+0x08, FUN_00730fb0
   rotacja@+0x14, FUN_00730fd0 @+0x20) zasilane z systemu atrybutów (FUN_00846840; ID
   0x6A4/0x6A5/0x6A8/0x6A9); producer atrybutów = granica otwarta (H1/H2 vs H3 vs H4).
6. NiAVObject oracle offsetów VA-locked (FUN_007c04f0 = GetViewerStrings; local
   +0x38/+0x5C/+0x68, world +0x6C/+0x90/+0x9C — zgodność 1:1 z Gb12).
7. 9.3.5 NIE MA klas Sector/Region/Entity ani plików Sectors.xbc/Objects.pak — przestrzeń
   cell = ArkPortalCell (portal/dPVS) + TEZ + parametry 20xxx.vfs; RM-init FUN_0041dae0
   rejestruje wszystkie magazyny świata (.nif/.bvi/.amu/.tdf/.prt/.tez/portals.bnt/TEZ.bnt).

## NOWE VA (lista — własne tego runu)
0x00730F60, 0x00730F90, 0x00730FB0, 0x00730FD0 (setterzy placementu);
0x00567770, 0x00567170, 0x005B5F90 (builder-y rekordów placementu); 0x00567C50;
0x00846840 (reader atrybutów, switch 0x6A4/0x6A5/0x6A8/0x6A9); 0x00457930 (rejestracja
z nazwą); 0x006CB6F0 (twórca instancji), 0x006FA8B0/0x006FA8D0 (ctor/dtor
ArkModelResourceInstanceRef; vft 0x00A864B8/0x00A864B0), 0x006CB020 (instancja nazwana
0x110 B "<id>__<name>"), 0x006F33A0 (rejestracja instancji), 0x006CB3C0/0x006CB4C0
(pending-attach), 0x006F2AF0 (reset deskryptora pending), 0x006CB370, 0x006CB880,
0x006CD820/0x006CD850/0x006CDD80/0x006CD580/0x006CD4E0 (podsystem wizualny);
0x00726E70 (ctor ArkObject; A→+0x28), 0x0070BF50 (ArkObjectClass::create), 0x007351E0
(ctor ArkSurgeonObject); 0x006B9970 (update postaci, "CharacterPosition"), 0x00489810
(setup avatara); 0x0077C0B0/0x0077C0F0/0x0077C120 (attach węzłów); 0x007C04F0
(NiAVObject::GetViewerStrings — oracle); 0x00834010 (ctor ArkCommunicator);
0x006F1B90 (check portal-def w NIF); 0x00933310 ("NetImmerseScene::Root");
0x0094BA00/0x0094F250 ("Data\Parameters\"); 0x0094B1D0 (ArkVegetationClient::GetModel);
0x0093BE20 (hardcode 0x70D17, negatyw 460563.nif); 0x007B6C30 (lookup klasy po nazwie);
vtable: 0x00A864B8/0x00A864B0/0x00A86B48/0x00A86850/0x00A98050/0x00A9805C/0x00A91CF8/
0x00A7C028/0x00A7C0A0/0x00A7BA0C/0x00A7BF9C/0x00A7BFCC/0x00A8D534/0x00A8CCF4;
stringi: 0x00A8D7D0-0x00A8D8BC (viewer/dpvs), 0x00A86334/0x00A86348 (m_ContainsPortals).

## Commit
path-limited: `docs/audits/PE_935_STATIC_INSTANCE_TRACE_R1_20260913/` (191 plików) +
`AUDIT_ENTRYPOINT.md` (+1 wiersz LATEST RUNS). Commit SHA i push: patrz END-of-run
komunikat w repo (SebastianKozlo/eudoria-clean, master).
