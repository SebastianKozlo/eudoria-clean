# HANDOFF — PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912

- **AUDIT_OUTPUT_ROOT** = `D:\Eudoria_Reconstruction\99_Audits\PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912\`
- **FINAL_REPORT_PATH** = `06_REPORT\00_FINAL_REPORT.md`
- **PRIMARY_EVIDENCE_PATHS** =
  - `06_REPORT\STAGE_ACCEPTANCE_GATES.csv` (4 bramki z uzasadnieniami)
  - `03_EVIDENCE\VA_EVIDENCE_REGISTRY.md` (rejestr 20 ogniw: VA → instrukcja → artefakt)
  - `02_ANALYSIS\B_template_loading_chain.md` (łańcuch A→model, tabela ogniw + residuum)
  - `02_ANALYSIS\A_record_definition.md` (definicja: cytat + własny pełny walk 5438/5438; PROMPT_DELTA×2)
  - `02_ANALYSIS\C_transform_source_and_D_placement.md` (granica transform-source + plan)
  - `01_RAW\S2_TRUE_WALK_RESULT.json` + `01_RAW\S2_TEMPLATES_TRUE_WALK.csv` (pełny walk pliku, 0 CRC-fail)
  - `01_RAW\S1_ANCHOR_RESULT.json` (asercje SHA + negative-control CRC)
  - `01_RAW\S3_PE_HEADER.json` (image base/sekcje/mapping; brak ASLR)
  - `01_RAW\ghidra_output\` (S5..S20: 212× DISASM z surowymi bajtami, 224× PSEUDO, 31× JSON xref, 1× CSV = 468 plików łącznie; census POST-QC F4 2026-09-13)
  - `01_RAW\ghidra_output\S20_PSEUDO_MRQ_006B4C50.txt` (konsument kompletny: get A → {0x66,A})
- **RUN_STATUS** = COMPLETE (główna bramka PARTIAL z pełną dokumentacją residuum; zero hard-stopów)
- **HARD_STOP_REASON** = NONE

## Kluczowe wyniki (dla PE-MASTER)

1. **P0 ROZSTRZYGNIĘTE:** EU 9.3.5 czyta rekordy templates.vfs generycznym readerem ArkVFS02
   (magie "ArkVFS01"×1/"ArkVFS02"×2 @0x00A9C4D8/E4/F0; bramka CRC-32; stride
   `(floor((size+15)/base)+1)*base`, base=36 z nagłówka pliku — reguła bajt-tozsama z własnym
   pełnym walkiem pliku 5438/5438 do EOF, 0 CRC-fail) i **konsumuje A do załadowania modelu**:
   A → parsed-objekt +0x08 → getter FUN_007ce1e0 (`MOV EAX,[ECX+8]`) → **FUN_006c9700 = żądanie
   zasobu {typ 0x66 (MODEL), id=A}** → singleton ArkResourceManager (FUN_00415670, DAT_00ba12f4)
   + dispatcher provider-chain (FUN_00823c10) → fabryka (RTTI ArkModelResourceItemFactory,
   boost::shared_ptr) → BNT2 store (Models.bnt; reader FUN_00967d00, magia "BNT2" @0x00A9BF2C;
   cache get-or-create FUN_00799930). Wiązanie danych byte-proof: **A=296445 ↔ wpis "296445.nif"
   istnieje w Models.bnt** (siblingi 126740/278453 ✓; negative 999999999 ✗).
2. **Transformer instancji NIEosiągnięty** (sekcja C): łańcuch urywa się przed dekoderem strumienia
   serwera; hipoteza PE2 pozostaje hipotezą. Dokładna granica + plan w 02_ANALYSIS\C_*.md.
3. **B (kolizja) data-level:** B=296446 ↔ "296446.bvi" w Volumes.bnt (lokalna biblioteka kolizji);
   ścieżka modelu czyta WYŁĄCZNIE +0x08 (separacja instrukcyjna); indywidualni kodowi konsumenci
   B/C nie wyśledzeni (PARTIAL).
4. **Kanon-podobieństwo vs różnica ery:** mechanizm 9.3.5 ≠ mechanizm PE2 (PE2: mount+sprintf
   "%d"+ext w resource-manager; 9.3.5: generyczne żądanie {type,id} przez ArkResourceManager,
   rozszerzenia rejestrowane globalnie w RM-init FUN_0041dae0). Transfer PE2→9.3.5: ZERO.

## Najważniejsze VA (wszystkie własne, z binarium E7785430…)

- Loader: FUN_0072fa30 (string "Parameters\templates.vfs" @0x00A86D30; caller FUN_00452490)
- VFS open: FUN_00972df0; index walk: FUN_00972ad0; stride: FUN_00979d00; record read+CRC:
  FUN_00971ad0 (+ FUN_004063d0 CRC-32); parser: FUN_00730c90 (A→+0x08 @0x00730CE6);
  ctor: FUN_00730700 (+0x10=F32); registry: FUN_0072f8d0/FUN_0043a550 (DAT_00ba1824);
  lookup: FUN_0072f580 (sentinel 0x00BA5800); walidacja: FUN_0072fce0; **getter A: FUN_007ce1e0**;
  **pump modeli: FUN_006c9700 (type 0x66)**; dispatcher: FUN_00823c10; konsument kompletny:
  FUN_006b4c50; fabryka avatar: FUN_0043eae0 + para-insert FUN_0043c700; ArkModelManagerMain:
  FUN_006c0d50/006c8f80; cache: FUN_00799930; BNT2: FUN_00967d00 ("BNT2" @0x00A9BF2C);
  RM-init: FUN_0041dae0 (".nif"/".bvi"/".tdf"/".amu"; "models\"; "Cache\"); tester ".nif":
  FUN_007ee5f0 (tabela klas @0x00A9026C).

## Granice i residual (dokładnie)

- GATE-A PARTIAL: ciała metod wirtualnych providera (FUN_00823c10 → node+0x24 → vtable[+4]/[+0x38])
  nie zdekomponowane; identyczność klasy przez RTTI/boost-names (ArkModelResourceItemFactory).
  Domknięcie = 1 ograniczony Ghidra-round (vtable → metody fabryki → FUN_00799930/FUN_00967d00).
- GATE-B-C PARTIAL: kodowy konsument B (type-code .bvi) i C — nie wyśledzeni.
- Sekcja C: dekoder strumienia serwera EU (DYN1-server-stream ery EU = OPEN od dawna) —
  wymagany dedykowany run.

## Skope-guards

- Oryginały nietknięte: Entropia.exe / templates.vfs / night-aggregate projekt = READ-ONLY;
  projekt Ghidra = run-localna kopia (hash-verify 1:1, manifest w 06_REPORT\GHIDRA_LOCAL_COPY_MANIFEST.txt).
- Zero zapisów poza run-dir; zero pod-agentów; klient NIGDY nie uruchomiony (STATIC-ONLY);
  skrypty hashowane po edycji przed wykonaniem (20×, 00_CONTROL\S*_SCRIPT_SHA256.txt).
