# HANDOFF — PE_296445_NIF_ORIGIN_PLACEMENT_R1_ERRATA_R1_20260912

**ASSIGNMENT_MODE:** CORRECT_DOCUMENTATION + PERSIST_PUBLISH (kontrakt PE-MASTER post-audit)
**RUN_ID:** PE_296445_NIF_ORIGIN_PLACEMENT_R1_ERRATA_R1_20260912
**PARENT_RUN:** PE_296445_NIF_ORIGIN_PLACEMENT_R1_20260912 (audytowany; MASTER_PARTIAL_PASS z listą korekt)
**RUN_CLASS:** MATERIAL — errata dokumentacyjna + mechaniczna rekomputacja z gwarantowanymi wartościami oczekiwanymi; ZERO nowej forensyki; ZERO nowych twierdzeń poza adjudykowaną listą korekt.
**NO_NESTED_TASKS:** zachowane — zero pod-agentów.

## 1. Co wykonano

1. **Grupa A (separacja er, P1):** handler FUN_005977b0/vtable[0x50]/rekordy 0x1C/@+0x2c..0x34 oznaczone erą PE2/2003 (binarium PE2_unpacked_out.exe, SHA 56178993692A7409C896398089E482EDDF96177666BACB91A8CC1A638D9A0650); mechanizm w EU 9.3.5 = UNVERIFIED (hipoteza transferu; wymaga trace w Entropia.exe 9.3.5, SHA E7785430…). Etykieta „VFS 2003" → „VFS klienta pośredniego/późniejszego (ArkVFS02; era ≠ 2003-CD; dokładna era nieustalona)". Byte-identity rekordu 4508 między erami pozostaje FAKTEM.
2. **Grupa B (transformacje, P2):** bug R1 analyze_tree.py (world[i]=cur = transform RODZICA; geometria pomijała własną transformację mesha) udokumentowany; POPRAWIONA kopia 00_CONTROL\analyze_tree_v2.py (konwencja world[i] = parent_world ∘ local_i, parent korzenia = identity); artefakty zrekompensowane do 01_CORRECTED\ (TRANSFORM_TABLE_CORRECTED.csv, TREE_MESHES_CORRECTED.json, TREE_ANALYSIS_CORRECTED.txt). §2.3/§3B przeredagowane (ogon importera = ekstrema surowych tablic z różnych układów lokalnych; poprawny bbox sceny ±2500/±2500/[~0,15620]; 7. float UNKNOWN).
3. **Grupa C (retraction negatywu skryptowego, P1):** „0 odniesień do 296445" → prawda: 296445/296446 w 4508.obj.dec @664/@580; 126740 w 4752.obj.dec @520; 278453 w 2249.obj.dec @664; 0 ASCII; 0 w pozostałych 1,933 skryptach (mianownik zweryfikowany; kontraktowy „1,932" = artefakt arytmetyczny, poprawiony). WZMOCNIENIE definicja↔model, nie placement.
4. **Grupa D (retraction globalnego negatywu i „wyłącznie serwer"):** → NOT_FOUND_IN_SEARCHED_SCOPE z jawnymi granicami; dopisek „zero bajtów nierozliczonych = pełne pokrycie zakresów bajtowych, nie dowód pełnej semantyki".
5. **Grupa E (9 B):** [u8 0 @0][u32 -1 @1..4][u32 ID @5..8]; bajt @8 = MSB ID; brak dziesiątego bajtu; „atlas (flipbook)" → „UV-animacja potwierdzona (NiUVController, 2 klucze 0→5.0); interpretacja flipbook/atlas = HIPOTEZA".
6. **Grupa F (F1–F10):** wszystkie zastosowane (27×-1/23 dzieci — niezależnie zweryfikowane z BLOCKMAP_V2.json; EnvZones 126 (84+42); L362; TextureEffect dual-relation 62/59 — niezależnie zweryfikowane; Portals 382,811–592,741 + usunięty duplikat; Parameters 27; sids dopisek metody; „warianty slum" usunięte; mojibake + Strings/*.bnt; endianness u32BE dopisany).
7. **Grupa G (domknięcie):** ERRATA.md (pełna lista korekt z cytatami zastępowanych twierdzeń); 00_RAPORT_CORRECTED.md; PE_MASTER_REVIEW.md (verbatim); rawscan.py (reprodukcja RAWSCAN_CORRECT_HITS co do offsetów); make_manifest.py/verify_manifest.py; artifact_index.csv; rozstrzygnięcia tropów 4751×301 i 4508×18 zacytowane z obu źródeł (audyt + PE-MASTER — bez trzeciego pomiaru).

## 2. Wyniki bramek (fail-closed)

| Bramka | Wynik | Dowód |
|---|---|---|
| G1 transform-recompute | **PASS** | 14/30 world_T zmienionych + 16 identycznych (negatywna kontrola); bbox = min (-2500.0, -2500.0, -1.2652602576768146e-08) / max (2500.0, 2500.0, 15620.0) — EXACT w tolerancji 1e-4; glowsak #66 T = (401.14190673828125, -1611.4522705078125, -368.0000305175781) — exact; krzyżowo vs probe.json audytora 14/14 (max diff ≤1e-6). Assert w analyze_tree_v2.py; 02_EVIDENCE\G1_GATE_RESULTS.json |
| G2 rawscan-reproduction | **PASS** | 8/8 serii (file,offset) identycznych z RAWSCAN_CORRECT_HITS.json; 1,818 plików / 2,384,417,861 B; wzorce przez struct.pack z asercją konwersji odwrotnej. 02_EVIDENCE\RAWSCAN_REPRO.json + G2_GATE_RESULTS.json |
| G3 census fraz | **PASS** | 17 fraz zakazanych ×0 wystąpień; 12 required-once ×1; 16 required-present z zapisanymi liczbami. 02_EVIDENCE\G3_GATE_RESULTS.json |
| G4 manifest kompletny i zgodny | **PASS** | re-hash wszystkich wierszy manifestu: 0 MISMATCH; census plików ERRATA/R1 kompletny (jawne wykluczenia: manifest sam + G4/G7_GATE_RESULTS.json). 02_EVIDENCE\G4_GATE_RESULTS.json |
| G5 git path-census + push + HEAD==origin | **PASS** | committed path census == lista dozwolona (package + AUDIT_ENTRYPOINT.md); push OK; HEAD==origin/master. Patrz §4 (SHA commitu: `git log -1 -- AUDIT_ENTRYPOINT.md`) |
| G6 entrypoint row-survival | **PASS** | dokładnie 1 nowy wiersz LATEST RUNS; stary census wierszy nienaruszony (diff = 1 wiersz dodany, 0 usuniętych/zmienionych) |
| G7 R1 immutable | **PASS** | 18 plików R1: hashe PRZED (02_EVIDENCE\G7_R1_BASELINE_SHA256.csv, zebrane przed startem) == PO (verify_manifest.py): 0 zmian |

**NON_PASS_CLASSES:** zero (GATE_FAIL/SCOPE_CREEP/HASH_MISMATCH/REPO_DIRTY_CONFLICT — nie wystąpiły).
**HARD_STOPS:** zero naruszeń (R1 nietykalny — G7; oryginały READ-ONLY; payloadi LOCAL-ONLY; experiments/ nietknięte; brak uruchomienia klienta; brak pod-agentów; brak nowych twierdzeń poza listą korekt).

## 3. Pełny inwentarz plików ERRATA (lokalnie; hashe w 02_EVIDENCE\MANIFEST_SHA256.csv)

```
00_CONTROL\analyze_tree_v2.py     — poprawiony instrument (G1 assert)
00_CONTROL\rawscan.py             — niezależny generator reprodukcji RAWSCAN (G2)
00_CONTROL\script_scan.py        — weryfikacja korekty C (offsety + mianownik 1,933)
00_CONTROL\gate_census.py        — bramka G3 census fraz
00_CONTROL\make_manifest.py       — manifest + artifact_index (G1/G3 pakietu)
00_CONTROL\verify_manifest.py     — G4 re-hash + G7 final
01_CORRECTED\00_RAPORT_CORRECTED.md       — poprawiony raport (markery [E-…])
01_CORRECTED\TRANSFORM_TABLE_CORRECTED.csv
01_CORRECTED\TREE_MESHES_CORRECTED.json
01_CORRECTED\TREE_ANALYSIS_CORRECTED.txt
02_EVIDENCE\G7_R1_BASELINE_SHA256.csv    — hashe R1 sprzed pracy
02_EVIDENCE\RAWSCAN_REPRO.json           — reprodukcja G2 (pełna)
02_EVIDENCE\G1_GATE_RESULTS.json
02_EVIDENCE\G2_GATE_RESULTS.json
02_EVIDENCE\G3_GATE_RESULTS.json
02_EVIDENCE\SCRIPT_SCAN_REPRO.json       — reprodukcja korekty C
02_EVIDENCE\G4_GATE_RESULTS.json         — powstaje po manifeście (świadomie nie listowane w nim)
02_EVIDENCE\G7_GATE_RESULTS.json         — j.w.
02_EVIDENCE\MANIFEST_SHA256.csv          — WSZYSTKIE pliki ERRATA + wszystkie 18 plików R1 (bez własnego hasha — L12)
03_REPORT\ERRATA.md               — pełna lista korekt (cytaty zastępowanych twierdzeń)
03_REPORT\PE_MASTER_REVIEW.md     — przegląd PE-MASTER (verbatim z kontraktu)
03_REPORT\HANDOFF.md              — niniejszy dokument
03_REPORT\artifact_index.csv      — schema projektu (standing sentence + path,kind,sha256; nie listuje artifact_index/MANIFEST — wzajemna auto-referencja niemożliwa)
```

## 4. Publikacja (repo eudoria-clean)

- BASE_SHA: 2acf46258281be4b471788812501d146f592c235 (HEAD == origin/master przed pracą; dirty: wyłącznie `?? experiments/` — poza zakresem, NIETKNIĘTE, NIE commitowane).
- Commit path-limited: `docs/audits/PE_296445_NIF_ORIGIN_PLACEMENT_R1_ERRATA_R1_20260912/` (00_CONTROL\*.py, 01_CORRECTED\*, 02_EVIDENCE\MANIFEST_SHA256.csv, 03_REPORT\{ERRATA.md, PE_MASTER_REVIEW.md, HANDOFF.md, artifact_index.csv}) + `AUDIT_ENTRYPOINT.md` (dokładnie 1 nowy wiersz LATEST RUNS: R1+ERRATA razem; commit-cell per precedens: SHA discoverable via `git log -1 -- AUDIT_ENTRYPOINT.md`).
- LOCAL-ONLY (bez commitu): payloadi oryginałów (296445.nif, 296446.bvi — w runie R1, LOCAL-ONLY), 02_EVIDENCE\{RAWSCAN_REPRO, wyniki bramek, baseline} (hashe w manifeście), experiments/, wszystkie pliki runu R1.
- BRAMKA G5: `git show --name-status` census == lista dozwolona; push; HEAD==origin/master.

## 5. Uwagi wykonawcze (jawność procesu — szczegóły w ERRATA.md §10)

1. Bramka G2 wyłapała i wymusiła naprawę błędu własnego instrumentu (nadpisanie wzorca u32LE bajtami ASCII przy scaleniu słowników o tym samym kluczu) — pierwszy przebieg FAIL, po naprawie PASS. Brak cichego zapisu wyniku niezgodnego.
2. Bramka G3 wyłapała 4 cytatowe powtórzenia fraz zakazanych w markerach korekt raportu poprawionego — usunięte (cytaty zastępowanych twierdzeń wyłącznie w ERRATA.md).
3. Rozbieżności kontraktu vs fizyka udokumentowane i rozstrzygnięte po stronie faktów: lokalizacja mojibake (terrain, nie Portals — oba poprawione); mianownik „pozostałych" skryptów (1,933, nie 1,932).

## 6. Następny krok (po errata-QC)

P0 per PE-MASTER: **PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912** — ślad konsumenta w Entropia.exe 9.3.5 (własna weryfikacja SHA/image-base/VA-mapping; zakaz transferu adresów PE2; resolver-agnostycznie; A/B/C oddzielnie; negative control wrong-ID 4752/2249). Poszukiwanie placementu pozostaja OTWARTE. (To OSOBNY run badawczy — NIE został rozpoczęty w tej erracie.)
