# PE_935_TEMPLATE_CONSUMER_TRACE_R1 — FINAL REPORT

**RUN_ID:** PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912
**Executor:** pe-reconstruction (bezpośredni dispatch PE-MASTER; NO_NESTED_TASKS)
**RUN_STATUS:** COMPLETE (główna bramka PARTIAL z pełną dokumentacją residuum; żadna przeszkoda twarda)
**HARD_STOP_REASON:** NONE
**ERA:** EU 9.3.5 (pcg_install). **Binarium:** Entropia.exe SHA256
`E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` (8,015,872 B, brak ASLR, image base 0x00400000).
**Dane:** templates.vfs SHA256 `BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77`.

---

## 0. Odpowiedź na P0 (jedno główne pytanie)

**TAK — klient EU 9.3.5 czyta rekordy template'ów z ArkVFS02/templates.vfs i konsumuje pole A
do załadowania modelu.** Mechanizm jest w pełni zakotwiczony w kodzie (patrz sekcja B):
rekordy czyta generyczny reader VFS (magie "ArkVFS01"/"ArkVFS02", bramka CRC-32, stride
`(floor((size+15)/base)+1)*base`), parser zapisuje A do pola **+0x08** parsed-objektu,
rejestr = std::map&lt;id2, obiekt&gt; (singleton DAT_00ba1824), a konsumenci pobierają A getterem
`FUN_007ce1e0 = [ECX+0x08]` i wołają **`FUN_006c9700(A, …)` = żądanie zasobu typu {0x66 (MODEL), id=A}**
przez singleton **ArkResourceManager** (FUN_00415670) i dispatcher provider-chain (FUN_00823c10),
z dostawą z archiwów BNT2 (Models.bnt), gdzie A **dosłownie nazywa wpis `<A>.nif`**
(byte-proof: "296445.nif" istnieje w Models.bnt @395,268,773).

**Transformacja instancji (pozycja/obrót/skala) NIE została osiągnięta statycznie w tym runie**
(sekcja C): łańcuch urywa się przed wejściem do dekodera strumienia sieciowego; dokładny brak
udokumentowany. Hipoteza PE2 (server-delivered) pozostaje hipotezą — nie założeniem i nie wynikiem.

## 1. Sekcja A — tożsamość definicji (CYTAT + własna weryfikacja)

Patrz `02_ANALYSIS\A_record_definition.md`. Rekord 4508 @96,496 potwierdzony bajtowo własnym
pełnym walkiem (nie tylko cytat): id=4508, size=28, ver=1, crc32=0xAFF5797C (CRC-payload OK),
id2=4508, **A=296445 @96,516**, **B=296446 @96,520**, C=0, PARAM=124.941f.
Pełna struktura (NOWE): stride-rule + payload size-28 = [id2][A][B][C][D_f32][u16 str-count][u16 u32count][F];
rekordy size>28 niosą listy nazw/id (avatar body-part slots). Dwie adnotacje kontraktu rozbieżne
fizycznie: PARAM leży @rec+0x20 (nie +0x24; @+0x24 leży para liczników list) — wartość zgodna;
starty siblingów 97,288/93,976 (kontrakt: +6) — zawartość zgodna. Obie PROMPT_DELTA udokumentowane.

## 2. Sekcja B — kod ładowania modelu (łańcuch VA-locked)

Kompletna tabela 20 ogniw: `03_EVIDENCE\VA_EVIDENCE_REGISTRY.md` + `02_ANALYSIS\B_template_loading_chain.md`.
Szkic:

```
FUN_00452490 → FUN_0072fa30 (loader; "Parameters\templates.vfs" @0x00A86D30)
  → FUN_00972df0 (CreateFileA; magia ArkVFS01/@0x00A9C4F0 / ArkVFS02/@0x00A9C4E4; base=36 → +0x8c)
    → FUN_00972ad0 (index: 16-B {id,size,ver,crc32}; stride FUN_00979d00)
  → per rekord: FUN_00971ad0 (seek [node+0x10]+0x10; read size; CRC32 FUN_004063d0 vs node+0xC)
    → FUN_00730700 (ctor; +0x10 = F32) → FUN_00730c90 (A→+0x08; B→+0x04; C→+0x0C; D→+0x10)
    → FUN_005670a0 (copy) → FUN_0072f8d0 (map insert; klucz=id2; singleton DAT_00ba1824)
KONSUMPCJA:
  FUN_0072f580 (map find → node+0x14; sentinel 0x00BA5800) → FUN_0072fce0 (valid: id2≠0 ∧ (A∨B∨C)≠0)
  → FUN_007ce1e0 (get A = [obj+0x08])
  → FUN_006b4c50: FUN_006c2840/2870 (resolver → TemplateObject) → A → FUN_006c9700(A,…)
     = {typ 0x66=MODEL, id} → FUN_00415670 (ArkResourceManager singleton) + FUN_00823c10
     (provider-chain: node+0x24 → vtable[+4]/[+0x38]) → fabryka (RTTI ArkModelResourceItemFactory)
     → zasób modelu → attach do encji (+0x1b8/+0x1bc)
  Wariant: FUN_00511070 → request {factory=FUN_0043eae0,…,A} → FUN_006c0d50 (new ArkModelManagerMain)
     → fabryka: A → para {0x66, A} (FUN_0043c700) do mapy pending requestera
Store: rozszerzenie ".nif" zarejestrowane w RM-init FUN_0041dae0 (2×; także ".bvi"/".tdf"/".amu"/"models\"/"Cache\");
tester ".nif" FUN_007ee5f0 w tabeli klas @0x00A9026C; cache get-or-create FUN_00799930;
BNT2 reader FUN_00967d00 (magia "BNT2" @0x00A9BF2C).
Data-binding: A ↔ "<A>.nif" w Models.bnt (296445 ✓, 126740 ✓, 278453 ✓; 999999999 ✗).
```

**Residuum (jedyna przerwa):** ciała metod wirtualnych providera (vtable[+4]/[+0x38] na node+0x24)
nie zostały zdekomponowane — klasa ustalona przez RTTI/boost-names, ciąg instrukcji
create→store-read wewnątrz fabryki nie jest VA-locked. To podstaw klasyfikacji
GATE-A-CONSUMER = PARTIAL_TO_RESOURCE (z resztą łańcucha kompletną).

## 3. Sekcja B/C — separacja pól B/C

- **B:** data-level byte-proof: B=296446 ↔ "296446.bvi" w Volumes.bnt (siblingi ✓, negative ✗).
  Volumes.bnt = lokalna biblioteka kolizji (niezależne potwierdzenie erowe w
  PE_STATIC_WORLD_EU_PARSE_R1: 21,835 lokalnych AABB, zero world-coord). Kod: parse → slot +0x04;
  getter rodzinny FUN_00746550=[ECX+4]; indywidualny kodowy konsument B (type-code ścieżki kolizji)
  NIE wyśledzony w tym runie.
- **C:** parse → slot +0x0C; brak konsumenta poza walidacją (FUN_0072fce0) — uczciwie: not found.
- **Separacja od ścieżki modelu:** konsument A (FUN_006b4c50/006c9700/0043eae0) czyta WYŁĄCZNIE
  +0x08 (getter FUN_007ce1e0); żadnej instrukcji czytającej +0x04/+0x0C w tej ścieżce (byte-locked).
  GATE-B-C-SEPARATION = PARTIAL (silne dowody B data-level + rozdzielenie instrukcyjne; brak
  indywidualnych kodowych konsumentów B/C).

## 4. Sekcja C — źródło transformacji instancji

**NIE OSIĄGNIĘTE (dokumentacja granicy):** wejście do dekodera strumienia serwera nie zostało
zidentyfikowane; żaden z 25 call-site'ów lookupu / 13 callerów pumpu modeli nie nosi cech
create-object-handler z rekordami f32 XYZ. Urywa się na: po attach zasobu modelu do encji
(vtable[+0xA4] w FUN_006b4c50) brak dalszego śladu do transform-set. Hipoteza PE2 (server-delivered,
0x1C + transform sub-record + vtable[0x50]) pozostaje NIEPRZENIESIONĄ HIPOTEZĄ. Szczegóły +
plan minimalny dla przyszłego runu: `02_ANALYSIS\C_transform_source_and_D_placement.md`.

## 5. Sekcja D — historyczna lokalizacja

**NIE ZNALEZIONO (uczciwy brak).** Run był misją mechanizmu; brak placementu = poprawny wynik.
Zero mock-spawnów (zakaz kontraktu dotrzymany).

## 6. Bramki

| bramka | werdykt |
|---|---|
| GATE-A-CONSUMER | **PARTIAL_TO_RESOURCE** (łańcuch L1–L7 kompletny VA-locked; residuum: ciała metod wirtualnych providera/fabryki; transform-source sekcji C nieosiągnięty) |
| GATE-B-C-SEPARATION | **PARTIAL** (B data-level byte-proof + separacja instrukcyjna ścieżki modelu; indywidualni kodowi konsumenci B/C nie wyśledzeni) |
| GATE-ERA | **PASS** (asercje SHA fail-closed S1/S3; zero transferu PE2; każdy VA z surowymi bajtami w dumpach) |
| GATE-NC | **PASS** (sibling 4752/2249 w tych samych funkcjach + data-binding; wrong-ID: sentinel bss→walidacja FALSE→ścieżka pominięta + 999999999 nie istnieje; CRC-dyskryminator flip-test) |

Pełne uzasadnienia: `06_REPORT\STAGE_ACCEPTANCE_GATES.csv`.

## 7. SELF_CHECK (własny, oznaczony — nie audit MASTER)

- [x] Full raw census tam gdzie deklarowane: S2 pełny walk 5438/5438 rekordów do EOF, 0 CRC-fail;
      string-census 51 hitów z VA; 20-ogniwo rejestr VA z surowymi bajtami.
- [x] Wszystkie bramki wyliczone fail-closed (PARTIAL nie zamienione na PASS).
- [x] Kontrole negatywne: wrong-ID (sentinel bss + walidacja + brak wpisów), CRC flip-test,
      sibling-genericity, era-asercja.
- [x] Hashe wejść weryfikowane przed użyciem (S1 asercja), generatorów — po edycji przed
      wykonaniem (00_CONTROL\*_SCRIPT_SHA256.txt, 20 skryptów).
- [x] Brak default-success: Ghidra rounds 4/5/6/… każda z EXEC metadata + logiem; fail
      instrumentu findBytes (S4: 0 hitów) ZDIAGNOSZOWANY i naprawiony własnym file-scanem (S4b)
      — nie ukryty.
- [x] Brak modyfikacji oryginałów: binarium/VFS/projects tylko czytane; projekt Ghidra = własna
      kopia (hash-verify 1:1 z night-aggregate); zero zapisów poza katalogiem runu.
- [ ] NIE wykonano: dekompilacja ciał metod wirtualnych providera (residuum GATE-A);
      kodowy konsument B; dekoder strumienia sieci (sekcja C).

## 8. Otwarte pozycje (open items z granicami)

1. Provider-vtable metody fabryki modeli (RTTI ArkModelResourceItemFactory) — zdekompilować
   node+0x24 → vtable → metody; domknie GATE-A do pełnego PASS.
2. Kodowy konsument B (type-code ścieżki .bvi/kolizji) i C.
3. Sekcja C: dekoder strumienia serwera EU 9.3.5 (DYN1-server-stream dla ery EU — status OPEN
   również w PE_STATIC_WORLD_EU_PARSE_R1) → create-object handler → transform-set.
4. PRT/Strings kontenery: NIE dekodowane w tym runie (kontrakt: tylko open items) — tropy:
   string "Data\Parameters\" @0x00A97E48, "parameters\sids.vfs" lowercase @0x00A915FB (0 xref
   w Ghidra — możliwy zapis/edycja vs odczyt), tabela formatów obrazu (".targa"/".rgb"/".rgba"/".sgi")
   przy deskryptorach klas @0x00A902A0+.

## 9. Artefakty

`06_REPORT\artifact_index.csv` (pełny census z SHA256). Kluczowe:
- 01_RAW\S1_ANCHOR_RESULT.json, S2_TRUE_WALK_RESULT.json (+CSV census), S3_PE_HEADER.json, S4B_RAW_HITS.json
- 01_RAW\ghidra_output\S5..S20 (212× DISASM z surowymi bajtami, 224× PSEUDO, 31× JSON xref, 1× CSV = 468 plików łącznie; census POST-QC F4 2026-09-13)
- 02_ANALYSIS\A/B/C (3 dokumenty), 03_EVIDENCE\VA_EVIDENCE_REGISTRY.md
- 06_REPORT\00_FINAL_REPORT.md (ten plik), STAGE_ACCEPTANCE_GATES.csv, HANDOFF.md, artifact_index.csv
