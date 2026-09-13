# QC_REPORT — INTERNAL_QC (fresh context, independent)

**RUN_ID (audytowany):** PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912 (executor: pe-reconstruction; klasa LOAD_BEARING; dispatch bezpośredni PE-MASTER)
**RUN_ID (QC):** PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912_QC (audytor: pe-master-auditor, świeży kontekst; NO_NESTED_TASKS)
**ASSIGNMENT_MODE:** INTERNAL_QC
**QC_VERDICT:** **QC_PASS** (0 findingów P0/P1; 1×P2 + 3×P3 do poprawki dokumentacyjnej; wszystkie klasyfikacje bramek executora uzasadnione evidence; address-lock 6/6 + ~40 dodatkowych; census S2 zrekomputowany identyczny; manifest spójny w sobie z 2 lukami higieny)

**Tożsamość wejść (własny pomiar, przed jakąkolwiek analizą):**
- `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe` — SHA256 `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31`, 8,015,872 B → **ZGODNE z claimem runu**.
- `D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs` — SHA256 `BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77`, 560,788 B → **ZGODNE**.
- Models.bnt 395,412,868 B; Volumes.bnt 3,746,375 B (ścieżki wg zadania QC).

**Niezależność:** własny parser PE (od zera: DOS→e_lfanew→COFF→Optional→sekcje; bez pefile, bez ufania S3), własna implementacja CRC-32 (własna tabela 0xEDB88320, self-test `123456789`→`CBF43926`; NIE zlib), własny walk templates.vfs, własne skany bajtowe Models.bnt/Volumes.bnt. Weryfikacja porównawcza dumpów executora vs surowe bajty binarium. Zero modyfikacji evidence executora (dowód nietykalności: sekcja 10); jedyne zapisy = własne skrypty/wyniki w `00_CONTROL\qc_probe\` (dozwolone kontraktem QC) + ten raport.

---

## 1. GATES — czy klasyfikacje są uzasadnione evidence (nie tylko zadeklarowane)

| bramka | claim | werdykt QC | uzasadnienie QC + artefakty |
|---|---|---|---|
| GATE-A-CONSUMER | PARTIAL_TO_RESOURCE | **PASS (klasyfikacja uczciwa, uzasadniona)** | Łańcuch L1–L7 zweryfikowany bajtowo NIEZALEŻNIE (patrz pkt 2): magie ArkVFS01/02 @0x00A9C4F0/E4/D8 (stringi potwierdzone własnym odczytem), CreateFileA+ReadFile(8B)+strcmp×2 w FUN_00972df0 (call-site'y 00972DF0 własny skan), stride FUN_00979d00 (27 bajtów sekwencji identycznych), CRC-gate FUN_004063d0 (prolog+init 0xFFFFFFFF+pętla+finalny NOT), parser A→+0x08 @0x00730CE6 `89 47 08`, insert FUN_0072f8d0 (prolog+CMP klucza), lookup FUN_0072f580 (find+`ADD EAX,0x14`+sentinel), getter A FUN_007ce1e0 `8b 41 08 c3`, pump FUN_006c9700 (MOV [ESP+0x20],0x66 @0x006C973A + CALL 00415670 @0x006C9746 + CALL 00823c10 @0x006C974D), dispatcher vtable[+4]/[+0x38] @0x00823C75/7F, konsument FUN_006b4c50 (getter×2 + pump×2 — własny census calli), data-binding 296445.nif@395,268,773 ✓. RESIDUUM (ciała metod wirtualnych providera/fabryki) jawnie zadeklarowane i rzeczywiście nie domknięte instrukcyjnie — klasyfikacja PARTIAL nie zawyżona. Artefakty: `03_EVIDENCE\VA_EVIDENCE_REGISTRY.md`, `02_ANALYSIS\B_template_loading_chain.md`, `01_RAW\ghidra_output\S5..S20` |
| GATE-B-C-SEPARATION | PARTIAL | **PASS (uczciwa)** | Dowody B data-level zweryfikowane niezależnie: "296446.bvi" @3,701,937 w Volumes.bnt ✓, siblingi 126741.bvi @3,701,883 / 278454.bvi @3,701,910 ✓, negative 999999999.bvi nieobecny ✓. Sloty parse: B→+0x04 `89 47 04` @0x00730D14, C→+0x0C `89 47 0c` @0x00730D42 ✓. Rodzina getterów: FUN_00746550=`8b 41 04 c3`, FUN_006b22d0=`8b 41 0c c3`, FUN_007ce1e0=`8b 41 08 c3` ✓. "Ścieżka modelu czyta WYŁĄCZNIE +0x08": potwierdzone pełnym odczytem pseudokodu konsumenta FUN_006b4c50 (A wyłącznie przez FUN_007ce1e0 ×2). Brak indywidualnych kodowych konsumentów B/C jawnie zadeklarowany → PARTIAL poprawne. Artefakty: `02_ANALYSIS\A_record_definition.md`, `03_EVIDENCE`, `01_RAW\S2_TRUE_WALK_RESULT.json`, `S20_PSEUDO_MRQ_006B4C50.txt` |
| GATE-ERA | PASS | **PASS (uzasadniona)** | Każdy VA zweryfikowany przeze mnie bajtowo w binarium SHA E7785430 (asercja fail-closed potwierdzona w kodzie s1/s2: sys.exit(2) przy niezgodności; piny SHA skryptów 4/4 MATCH). PE-header (image base 0x00400000, 5 sekcji, brak ASLR/DYNAMIC_BASE) odtworzony własnym parserem — zgodny z S3 co do wartości. Sweep era-discipline (pkt 7): wszystkie wystąpienia PE2/2003 są jawnie oznaczone jako hipoteza/kontrast. Artefakty: `01_RAW\S1_ANCHOR_RESULT.json`, `01_RAW\S3_PE_HEADER.json`, `03_EVIDENCE\VA_EVIDENCE_REGISTRY.md` E.5 |
| GATE-NC | PASS | **PASS (uzasadniona; 1 finding P2 w detaalu side-claim — F1)** | (a) Sibling genericity: wszystkie nazwy siblingów istnieją w BNT na claimowanych offsetach (własny skan); **brak jakiejkolwiek stałej 296445/4508/296446/126740/278453 w 29 funkcjach łańcucha** (własny skan imm32, 0 hitów). (b) Wrong-ID: sentinel `b8 00 58 ba 00` @0x0072F5A5 ✓; sentinel 0x00BA5800 leży w .data-bss (własny rachunek: raw_end=0x00BA0000, virt_end=0x00BA96E4) → zerowany ✓; walidacja CMP-family @0x0072FCE0 ✓ (CMP [ECX],0 JZ); 999999999.nif/.bvi nieobecne ✓. (c) CRC-dyskryminator: własny flip-test — AFF5797C→3C32D977, zgadza się z claimem dokładnie ✓. Finding F1 (P2): stałe avatar-hardcode w E.4/B.1/GATE-NC zniekształcone (11705/11706 nie istnieją jako imm32; realnie 11769=0x2DF9 @0x00511245 w FUN_00511070 + rodzina 11655/11656/11657 w FUN_006b28e0) — wniosek bramki (generyczność) NIEZMIENIONY. Artefakty: `S1_ANCHOR_RESULT.json`, `S2_TRUE_WALK_RESULT.json`, `03_EVIDENCE` E.3/E.4 |

---

## 2. ADDRESS-LOCK SPOT (własny skrypt, własny parsing PE) — **6/6 MANDATORY PASS + ~40 dodatkowych PASS**

Narzędzie: `00_CONTROL\qc_probe\qc_A_address_lock.py` + `qc_A2_address_lock.py` + `qc_A3_address_lock.py`; wyniki: `qc_A_address_lock_result.json`, `qc_A2_address_lock_result.json`, `qc_A3_address_lock_result.json`. Własny PE parse: image_base 0x00400000, 5 sekcji (.text/.rdata/.data/.tls/.rsrc), brak ASLR — zgodne z S3.

### Mandatory 6/6 (surowe bajty vs dumpy executora — ZERO rozbieżności):

| ogniwo | VA | bajty zmierzone (własny odczyt) | dump executora | zgodność |
|---|---|---|---|---|
| parser A→+0x08 | 0x00730CE6 | `89 47 08` MOV [EDI+0x08],EAX | S6_DISASM_parse_00730c90.txt L35 | **PASS** |
| getter A | 0x007CE1E0 | `8b 41 08 c3` | S11_DISASM_getter_007ce1e0.txt | **PASS** |
| stride-rule | 0x00979D00 | `8b 41 04 85 c0 74 14 8b 49 14 83 c0 0f 33 d2 f7 f1 83 c0 01 0f af c1 83 c0 f0 c3` (27 B pełnej reguły) | S6_DISASM_stride_00979d00.txt | **PASS** |
| CRC-32 gate | 0x004063D0/0x0040640F/0x00406416/0x00406430 | prolog `81 ec 00 04 00 00…`; init `83 c9 ff`; pętla `0f b6 02 33 c1 25 ff 00 00 00 c1 e9 08 33 4c 84 0c…`; final `f7 d1 … 89 0b` | S6_DISASM_helper_004063d0.txt | **PASS** |
| map insert | 0x0072F8D0 | head `53 8b 5c 24 0c 55 56 8b f1 8b 6e 04 85 ed 57 8b fe`; CMP klucza `3b 45 10` @0x0072F8E7 | S6_DISASM_register_0072f8d0.txt | **PASS** |
| pump {0x66,id} | 0x006C9700 | `c7 44 24 20 66 00 00 00` @0x006C973A; `89 44 24 24` (id) @0x006C9742; CALL 00415670 @0x006C9746 `e8 25 bf d4 ff`; CALL 00823c10 @0x006C974D `e8 be a4 15 00` | S20_DISASM_PUMP_006c9700.txt | **PASS** |

### Dodatkowe ogniwa rejestru zweryfikowane bajtowo (wybór; pełna lista w JSON-ach probe):

- parser B→+0x04 @0x00730D14 `89 47 04`; C→+0x0C @0x00730D42 `89 47 0c`; D_f32 FSTP +0x10 @0x00730D70 `d9 5f 10`; F→+0x2C @0x00730DB6 `89 57 2c` — PASS
- ctor FLDZ/MOV/XOR/FSTP[+0x10] @0x00730700 `d9 ee 8b c1 33 c9 d9 58 10` — PASS
- singleton rejestru: MOV EAX,[0xBA1824] @0x0043A571 `a1 24 18 ba 00` + store @0x0043A59B `a3 24 18 ba 00` + new(0x18) `6a 18` + CALL 0052a260 — PASS
- lookup: head `51 56 8b f1` @0x0072F580; CALL 004d1430 @0x0072F590; `83 c0 14` @0x0072F59E; sentinel `b8 00 58 ba 00` @0x0072F5A5 — PASS
- walidacja CMP-family @0x0072FCE0: `83 39 00`/`83 79 08 00`/`83 79 04 00`/`83 79 0c 00` wszystkie obecne — PASS
- getter B `8b 41 04 c3` @0x00746550; getter C `8b 41 0c c3` @0x006B22D0; klucz insertu `8b 01 c3` @0x004123D0 — PASS
- rekord-offset seek @0x00979D20 `8b 41 10 83 c0 10 c3` — PASS
- konsument FUN_006b4c50: census calli (okno 0x600): CALL 007ce1e0 ×2, CALL 006c9700 ×2 — PASS (zgadza się z claimem "×2")
- wariant avatar FUN_0043eae0: MOV [ESP+0x10],0x66 @0x0043EB9D `c7 44 24 10 66 00 00 00` + CALL 007ce1e0 @0x0043EBA5 `e8 36 f6 38 00` — PASS
- dispatcher: MOV ECX,[EDI+0x24] @0x00823C6C `8b 4f 24`; vtable[+4] `8b 01 8b 50 04 ff d2` @0x00823C75; vtable[+0x38] `8b 01 8b 50 38 55 ff d2` @0x00823C7F — PASS
- ARM singleton: MOV EAX,[0xBA12F4] @0x00415691 `a1 f4 12 ba 00`; PUSH 0x98 (imm32 `68 98 00 00 00`) @0x0041569A — PASS (obiekt 0x98 potwierdzony)
- BNT2 reader: PUSH 0xA9BF2C @0x00967F5C `68 2c bf a9 00`; string "BNT2" @0x00A9BF2C — PASS
- RM-init: PUSH 0xa7a774 (".nif") @0x0041F1E9/@0x0041F23C; PUSH 0xa7a734 (".bvi") @0x0041F51C/@0x0041F56F; PUSH 0xa7a744 (".amu") @0x0041F47B; PUSH 0xa7a73c (".tdf") @0x0041F4CE; PUSH 0xa7a8cc ("models\") @0x0041E5DC/@0x0041E62A; PUSH 0xa7a83c ("Cache\") @0x0041EC46 — PASS (stringi @VA potwierdzone własnym odczytem: "models\\", "Cache\\")
- tablica klas @0x00A90264 = {00AB0EA8, 007EE680, 007EE5F0, 007EE6A0, 007EE780} — tester .nif FUN_007ee5f0 na slot @0x00A9026C — PASS; tester ma PUSH ".nif" w ciele — PASS
- magic-writer FUN_00971680: MOV EDX,[0xA9C4D8] @0x009716D6 (wewnątrz funkcji; pseudo = WriteFile z uStack_14=DAT_00a9c4d8) — PASS
- VFS open FUN_00972df0: pseudo potwierdza CreateFileA→ReadFile(8B)→strcmp("ArkVFS01")→strcmp("ArkVFS02")→ver=2 @+0xa0→base→+0x8c (dla ArkVFS01: ver=1, base=0x80) — PASS (call-site'y strcmp×2 + indexwalk potwierdzone własnym skanem rel32)
- stringi ery: "Parameters\templates.vfs" @0x00A86D30; ".nif" @0x00A7A774; ".bvi" @0x00A7A734; ".tdf" @0x00A7A73C; ".amu" @0x00A7A744; ".vfs" @0x00A86820; "ArkVFS02"×2 @0x00A9C4D8/0x00A9C4E4; "ArkVFS01" @0x00A9C4F0 — PASS
- RTTI/boost fabryk: `counted_impl_p@VArkModelResourceItemFactory@@@detail@boost@@` @0x00B6D851 (start claimowanego zakresu) i `p_counted_impl_p@VArkTerrainEditZoneFactory@@...` @0x00B6D9DF (koniec) — **claim zakresu @0xB6D851..0xB6D9DF POTWIERDZONY co do bajta**; 6 nazw fabryk obecnych; RTTI "ArkModelManagerMain" @0x00B8C1BC — PASS

**Rozbieżności bajtowe z dumpami executora: ZERO.** Cztery chwilowe "FAIL-e" moich probe'ów (prolog insertu, enkodowanie 0x66, prolog singletona, virtual-call pattern dispatchera) były wyłącznie moimi zbyt wąskimi założeniami enkodowania — po odczytaniu dokładnych instrukcji z dumpów executora wszystkie potwierdzone bajtowo w binarium. **Żaden claim executora nie został obalony bajtowo.**

---

## 3. S2 FULL-WALK — rekomputacja z pliku własnym parserem — **PASS (identyczna)**

Narzędzie: `00_CONTROL\qc_probe\qc_B_walk_databinding.py` → `qc_B_walk_databinding_result.json`. Własna reguła stride `ceil((16+size)/base)*base`, base=36 z nagłówka (własny odczyt: magic "ArkVFS02", u32@0x08=36, u32@0x0C=1); własny CRC-32 (self-test PASS). **Nie ufam liczbom w S2_TRUE_WALK_RESULT.json — rekomputuję z surowego pliku.**

| miara | claim S2 | własna rekomputacja | zgodność |
|---|---|---|---|
| liczba rekordów | 5,438 | **5,438** | ✓ |
| stop | EOF | **EOF** | ✓ |
| walk_stop_offset / last_record_end | 560,788 | **560,788** (== rozmiar pliku) | ✓ |
| CRC-fail | 0 | **0** | ✓ |
| bajty nieudokumentowane | 0 | **0** | ✓ |
| size-census (75 wartości) | j.w. | **identyczna co do każdej wartości** (diff = ∅) | ✓ |
| D_f32@+0x20 ≠0 | 5,408 | **5,408** | ✓ |
| E_f32@+0x24 ≠0 | 2,003 | **2,003** | ✓ |
| D∧E ≠0 | 2,003 | **2,003** | ✓ |
| F_u32@+0x28 ≠0 | 1,990 | **1,990** | ✓ |
| id≠id2 | 0 | **0** | ✓ |
| tail_nonzero | 0 | **0** | ✓ |
| negative control CRC | AFF5797C→3C32D977 | **AFF5797C→3C32D977** (własny flip payload[0]^0xFF) | ✓ |

Rekordy docelowe (własny odczyt bajtowy, zgodność z claimami):
- **4508 @96,496** (idx 1340): id=4508, size=28, ver=1, crc=0xAFF5797C OK, id2=4508, **A=296445 @+0x14**, B=296446 @+0x18, C=0, PARAM=124.941f @+0x20 (bajty `cb e1 f9 42`) — **ZGODNE**.
- **4752 @97,288** (idx 1351): id=4752, A=126740, B=126741, crc=0xDFD0B0BA OK, D=111.806f — **ZGODNE**.
- **2249 @93,976** (idx 1305): id=2249, A=278453, B=278454, crc=0xB4B87ABD OK, D=104.863998f — **ZGODNE**.

Census size-census S2 vs QC: `equal=True`, `diffs={}` (pełne porównanie słownikowe w qc_B JSON).

---

## 4. DATA-BINDING — **PASS (6/6 pozytywów na dokładnych offsetach + 2 negatywy nieobecne)**

Własny skan bajtowy pełnych plików (`qc_B_walk_databinding_result.json` → `models_scan`/`volumes_scan`):

| nazwa | plik | claim offset | własny pomiar | werdykt |
|---|---|---|---|---|
| "296445.nif" | Models.bnt | 395,268,773 | **395,268,773** (jedyny hit) | ✓ ISTNIEJE |
| "126740.nif" | Models.bnt | 395,268,719 | **395,268,719** | ✓ |
| "278453.nif" | Models.bnt | 395,268,746 | **395,268,746** | ✓ |
| "296446.bvi" | Volumes.bnt | 3,701,937 | **3,701,937** | ✓ |
| "126741.bvi" | Volumes.bnt | 3,701,883 | **3,701,883** | ✓ |
| "278454.bvi" | Volumes.bnt | 3,701,910 | **3,701,910** | ✓ |
| "999999999.nif" (negative) | Models.bnt | brak | **0 hitów** | ✓ NIE ISTNIEJE |
| "999999999.bvi" (negative) | Volumes.bnt | brak | **0 hitów** | ✓ NIE ISTNIEJE |

Bonus-kontrola separacji: "296446.nif" NIE istnieje w Models.bnt (0 hitów) i "296445.bvi" NIE istnieje w Volumes.bnt — pola A/B nie krzyżują się z cudzymi typami plików. Trzy wpisy .nif siblingów leżą kolejno co 27 B (719→746→773) i trzy .bvi co 27 B — spójne z ciągłą tabelą indeksu BNT2 (E.4).

---

## 5. PROMPT_DELTA — **orzeknięcie: pomiar executora POPRAWNY, kontrakt miał błąd (obie delta potwierdzone)**

**(a) PROMPT_DELTA_1 (PARAM @rec+0x20, nie +0x24):** własny pomiar bajtowy rekordu 4508 @96,496: @+0x20 (96,528) = `cb e1 f9 42` = **124.94100189208984 f32** (zgodna wartość i semantyka z kontraktem); @+0x24 = para u16 liczników list (dla 4508: 0,0 — rekord size=28 bez list). Adnotacja offsetu w prompcie była rozbieżna o 4. **Executor miał rację; kontrakt zawierał błąd adnotacji.** Ppomocniczo: census D≠0 w 5,408 rekordach vs slot@+0x24≠0 w 2,003 → dwie różne populacje pól (rekomputacja własna: identyczna).

**(b) PROMPT_DELTA_2 (starty siblingów 97,288/93,976, nie 97,294/93,982):** własny walk potwierdza: rekord id=4752 fizycznie @**97,288** (id=4752 ✓, A=126740 @+0x14 ✓, B=126741, PARAM f32=111.806 @+0x20 ✓, para liczników @+0x24 = (0,0)); rekord id=2249 @**93,976**. Delta vs kontrakt każdorazowo +6. **Executor miał rację; kontrakt zawierał błędne starty.** Obie PROMPT_DELTA są poprawnie udokumentowane w `02_ANALYSIS\A_record_definition.md` A.2/A.3 i S1 (`offset_delta_vs_parent: 6`).

---

## 6. SEKCJA C (negative-space claim) — censusy istnieją, liczby wyprowadzone z artefaktów; status PLAUSIBLE→STRONGLY_SUPPORTED; pełna niezależna re-weryfikacja per-caller = NOT_CHECKED

Claim: "żaden z 25 call-site'ów lookupu / 13 callerów pumpu modeli nie nosi cech create-object-handler z rekordami f32 XYZ".

- **Census 25 call-site'ów lookupu:** `01_RAW\ghidra_output\S10_LOOKUP_CALLERS.json` — policzyłem: **25 wpisów** (23 funkcje; FUN_006c2bb0 i FUN_006b28e0 po 2 site'y) — **zgodne**. Dumpy każdego caller: 21 plików S10_DISASM_CALLER_* + 2 w S9 (006C2840/006C2870) = 23/23 funkcje.
- **Census 13 call-site'ów pumpu:** `S20_MODEL_REQUEST_CALLERS.json` — **13 wpisów** (11 funkcji; FUN_006b4c50 i FUN_006bc8e0 po 2 site'y) — **zgodne z liczbą "13"** (precyzja językowa: "13 callerów" = 13 call-site'ów w 11 funkcjach — drobna nieścisłość słowna, nie licznościowa). Dumpy: 11/11 S20_DISASM_MRQ_* + PSEUDO.
- **Jawna metodologia:** poszukiwanie opisane w `02_ANALYSIS\C_transform_source_and_D_placement.md` C.1/C.2 (4 zbadane wejścia; granica: "po attach zasobu modelu do encji (vtable[+0xA4]) brak dalszego śladu"). Liczby pochodzą z artefaktów (S10/S20 JSON z polami exec: run_id/started/script), nie z pamięci — zweryfikowane per-site bajty calli dla sample (FUN_006b4c50 pump @0x006B4D3A — mój census wyznaczył dokładnie ten sam site; getter/pump okna).
- **Moja niezależna kontrola losowości:** pełne odczyty FUN_006b4c50, FUN_00511070, FUN_006b28e0, fragmenty FUN_00567170 — konsumenci template→model (attach encji), nie dekodery pakietów; brak cech create-object-handler z f32-XYZ w sample.
- **NOT_CHECKED (moje, jawne):** pełna niezależna re-lektura wszystkich 34 pseudokodów callerów (25+13 site'ów) pod kątem "cech create-object-handler" — wykonałem census + 4-5 pełnych lektur + weryfikację denominators; nie mogę własnym sumieniem podpisać "żaden z 25/13" po pełnej re-lekturze każdego (residuum raportowane, nie obala claimu — artefakty do pełnej weryfikacji istnieją na dysku).
- Claim "nieosiągnięty transform-source" jest spójny z sekcją C raportu i z GATE-A (residuum). Raport NIE zawyża — twierdzenie jest negative-space z udokumentowaną granicą.

---

## 7. ERA-DISCYPLINA — **PASS (zero transferu PE2/2003)**

Sweep (`grep` po *.md runu): wystąpienia PE2: C_transform L21-22 ("odpowiednik PE2 FUN_005977b0 … NIE został zidentyfikowany w tym runie"), L32-34 ("odpowiednik vtable[0x50] set-position z PE2", "TO JEST NIEPRZENIESIONA HIPOTEZA"), FINAL_REPORT L27/L89-90 ("pozostaje NIEPRZENIESIONĄ HIPOTEZĄ"), HANDOFF L36-38 ("mechanizm 9.3.5 ≠ mechanizm PE2 … Transfer PE2→9.3.5: ZERO"), registry E.5 (adresy PE2 "występują wyłącznie jako OPIS wzorca"). **Każde wystąpienie VA-era PE2 (FUN_005977b0, vtable[0x50], 0x1C, FUN_00478950) jest jawnie oznaczone jako hipoteza/kontrast — żadne nie jest użyte jako pomiar/twierdzenie o 9.3.5.** Uwaga: A_record_definition L45 "slot@0x24≠0 w 2003" — liczba rekordów 2003, nie era (poprawny kontekst). E.2 ("w PE2/2003 … ZERO") to era-contrasted fakt cytowany z kanonu PE2 (TEMPLATE_READER_GHIDRA_R1, hash 561789…) — claim O PE2 z podanym źródłem, nie transfer na 9.3.5; strona PE2 nie była re-measzuraowana w tym runie (co jest uczciwe — nie jest to twierdzenie o 9.3.5).

**Odnośniki VA→surowe bajty:** rejestr E.1 ma kolumnę artefaktu dla każdego ogniwa; każdy zweryfikowany przeze mnie link (mandatory 6 + ~40 dodatkowych) ma dump z bajtami zgodnymi z binarium. Nie znalazłem VA w raporcie głównym bez pokrycia w dumpach (wszystkie z sekcji B/szkicu łańcucha zweryfikowane bajtowo powyżej).

---

## 8. ARTIFACT_INDEX — census + re-hash — **PASS z 2 findingami P3 (F2, F3)**

- **Claim "540 artefaktów":** manifest `06_REPORT\artifact_index.csv` = 541 wierszy (nagłówek + **540 wierszy danych**) → **zgodny z claimem**.
- **Census plików vs manifest:** na dysku 541 pliki (poza GHIDRA_LOCAL .rep, który ma osobny manifest `GHIDRA_LOCAL_COPY_MANIFEST.txt` — 11 wierszy z hashami, w tym 2×189,759,488 B db). Rozbieżność dokładnie 1 plik: **`06_REPORT\HANDOFF.md` (4,857 B) istnieje na dysku, a NIE ma wiersza w manifeście** → **finding F3 (P3)**. Wszystkie pozostałe 540 ścieżek manifestu istnieją na dysku; żaden wiersz manifestu nie wskazuje nieistniejącego pliku.
- **Re-hash 10 losowych artefaktów** (seed 20260913): **10/10 MATCH** (rozmiar + SHA256) — `qc_D_nc_manifest.py` → `qc_D_nc_manifest_result.json`.
- **Self-row manifestu:** manifest ZAWIERA wiersz `06_REPORT\artifact_index.csv,64694,B922E31C…` — hash i rozmiar NIEAKTUALNE z definicji (bieżący plik: 65,003 B, SHA256 `00C6DB5073B2E3003FBD021DBA10BFA2B3E8CE9C2C09A4250E6D6E695DE57260`; self-reference niemożliwa do spełnienia) → **finding F2 (P3)** — narusza precedens L12 (manifest nie powinien zawierać własnego hasha; poprawnie: brak self-row i brak hashy QC).
- **Hashy QC w manifeście brak** — poprawnie (QC_REPORT powstaje teraz i nie jest w manifeście — zgodnie z oczekiwaniem).

---

## 9. COVERAGE HONESTY — **PASS (raport nie zawyża)**

Wypunktowanie NOT_CHECKED/nieosiągniętych z raportu executora i moja ocena:
1. **Ciała metod wirtualnych providera/fabryki** (residuum GATE-A) — jawnie w §0/§2 raportu ("jedyna przerwa"), HANDOFF "Granice i residual", §7 SELF_CHECK unchecked, §8 open item 1. → uczciwe.
2. **Kodowy konsument B i C** — §3 raportu + GATE-B-C PARTIAL + §7/§8. → uczciwe.
3. **Dekoder strumienia serwera / transform-source (sekcja C)** — §4 "NIE OSIĄGNIĘTE" + dedykowany dokument C. → uczciwe.
4. **Placement historyczny (sekcja D)** — "NIE ZNALEZIONO (uczciwy brak)"; zero mock-spawnów. → uczciwe.
5. **PRT/Strings kontenery** — §8 open item 4 (NIE dekodowane; tropy zapisane). → uczciwe.
6. Fraza §0 "Mechanizm jest w pełni zakotwiczony w kodzie (patrz sekcja B)" — dotyczy wyspecyfikowanego łańcucha (reader→parser→rejestr→getter→żądanie {0x66,A}→RM→dispatcher), który faktycznie jest w pełni VA-locked (zweryfikowane), a natychmiast w §2 następuje jawne "Residuum (jedyna przerwa)" + klasyfikacja PARTIAL. Brak zawyżenia klasyfikacji; wymaganie powyżej, by nie czytać "w pełni" jako całości mechanizmu fabryki, jest spełnione przez kontekst. → uczciwe (z notką).
7. S1 (naivny fixed-stride census z 3,062 CRC-fail) jest w 01_RAW jako ślad metody; raport główny cytujęje S1 wyłącznie za asercje SHA + negative-control — S2 jest właściwym walidowanym walkiem (rekomputacja własna: 5,438/0). → brak konfliktu.

---

## FINDINGS (pełna lista, wagi, poprawki, testy rewalidacji)

### **F1 (P2) — Zniekształcone stałe avatar-hardcode: "11705/11706" nie istnieją w binarium jako imm32; realna stała FUN_00511070 to 11769 (0x2DF9)**
- **Źródło (3 wystąpienia):** `03_EVIDENCE\VA_EVIDENCE_REGISTRY.md` E.4 ("jedynie hardcode'y id w consumerach to avatar-sloty: 11655/11656/11705/11706 — klasy klasy FUN_006b28e0/FUN_00511070"); `02_ANALYSIS\B_template_loading_chain.md` B.1 link 18 ("lookup(hardcoded id 11705/11706)"); `06_REPORT\STAGE_ACCEPTANCE_GATES.csv` GATE-NC ("jedynie avatar-hardcode 11655/11656/11705/11706 w osobnych consumerach").
- **Przeciw-dowód fizyczny (własny pomiar):** skan całego .text pod imm32: 0x2DB9/0x2DBA (11705/11706) = **0 wystąpień**; 0x2DF9 (11769) = 1 wystąpienie @0x00511246 (`b8 f9 2d 00 00` MOV EAX,0x2df9 — bezpośrednio przed PUSH/CALL 0043a550/0072f580/007ce1e0 w FUN_00511070, zgodnie z dumpem S10_DISASM_CALLER_00511070); FUN_006b28e0: `b8 88 2d 00 00` (11656) @0x006B28F6 + obliczana rodzina {11655|11657} przez `05 87 2d 00 00` ADD EAX,0x2d87 @0x006B2922. Wartości 11705/11706 istnieją wyłącznie w tabeli u32 w .rdata @0x00A85838/0x00A8583C (bez bezpośrednich referencji z .text do tej komórki — skan 0 hitów).
- **Skutek:** błędne stałe w claimie side (kontrola generyczności); **wniosek bramki GATE-NC (brak stałych specyficznych dla template'ów w łańcuchu generycznym; hardcode wyłącznie avatar-slotowy, poza ścieżką) pozostaje NIEZMIENIONY i potwierdzony niezależnie** (własny skan: 0 hitów 296445/4508/296446/126740/278453 w 29 funkcjach łańcucha). Klasyfikacja bramki nie zależy od tych konkretnych liczb.
- **Poprawka (narrow):** w E.4, B.1 link 18 i GATE-NC CSV zamienić "11705/11706" → "11769 (0x2DF9, FUN_00511070 @0x00511245)" + uzupełnić rodzinę FUN_006b28e0 o obliczany wariant {11655|11657} (ADD EAX,0x2d87 po SUB/NEG/SBB/AND 2); opcjonalnie odnotować tablicę .rdata @0x00A85838 zawierającą 11705/11706 (bez bezpośredniego xref z .text).
- **Test rewalidacji:** `Select-String`/skan imm32 0x2DB9/0x2DBA w .text = 0 hitów; imm32 0x2DF9 = dokładnie 1 hit @0x00511246; wystąpienia "11705|11706" w *.md/CSV runu = 0 po poprawce.

### **F2 (P3) — Manifest artifact_index.csv zawiera własny wiersz (self-row) z nieaktualnym hashe/rozmiarem**
- **Źródło:** `06_REPORT\artifact_index.csv` ostatni region wierszy: `06_REPORT\artifact_index.csv,64694,B922E31CD70F6BA4774C5F8C7249EF0AF4B59FD946D05D0EDB4149ADB98EA06A`.
- **Przeciw-dowód:** bieżący plik = 65,003 B, SHA256 `00C6DB5073B2E3003FBD021DBA10BFA2B3E8CE9C2C09A4250E6D6E695DE57260` ≠ claim; self-reference matematycznie niemożliwa do spełnienia (hash pliku nie może zawierać poprawnego hasha samego siebie). Precedens L12 (przekazany w kontrakcie QC): manifest poprawnie NIE zawiera własnego hasha ani hashy QC.
- **Skutek:** higiena manifestu; 1 z 540 wierszy jest nieaktualny z konstrukcji; nie wpływa na żadną bramkę/claim naukowy.
- **Poprawka:** usunąć self-row z manifestu (pozostałe 539 wierszy + ewentualny nowy wiersz HANDOFF — patrz F3) i przehashować manifest bez self-reference.
- **Test rewalidacji:** `Import-Csv artifact_index.csv | Where-Object relative_path -eq '06_REPORT\artifact_index.csv'` → 0 wierszy; 10 losowych re-hash nadal PASS.

### **F3 (P3) — HANDOFF.md nieobecny w census artefaktów (manifest niepełny o 1 plik)**
- **Źródło:** census dysku: 541 plików (poza GHIDRA_LOCAL) vs 540 wierszy manifestu; brakujący wiersz = `06_REPORT\HANDOFF.md` (4,857 B), mimo że FINAL_REPORT §9 wymienia HANDOFF.md jako artefakt kluczowy, a HANDOFF jest formalnym elementem pakietu run (kontrakt: "każdy substantive run ma REPORT/GATES/HANDOFF/manifest").
- **Skutek:** claim "pełny census z SHA256" (§9) jest niepełny o 1 artefakt; hasha HANDOFF.md brak w jakimkolwiek manifestu.
- **Poprawka:** dodać wiersz `06_REPORT\HANDOFF.md,4857,<sha256>` w (poprawionym per F2) manifeście.
- **Test rewalidacji:** census dysku (excl. GHIDRA_LOCAL, excl. qc_probe i QC_REPORT) == liczba wierszy manifestu; re-hash HANDOFF.md zgodny.

### **F4 (P3) — Nieaktualne liczby dumpów w FINAL_REPORT §9 / HANDOFF ("61× DISASM, 48× PSEUDO" vs fizycznie 212/224)**
- **Źródło:** `06_REPORT\00_FINAL_REPORT.md` §9 ("01_RAW\ghidra_output\S5..S20 (61× DISASM z surowymi bajtami, 48× PSEUDO, xref-JSON-y)"); `06_REPORT\HANDOFF.md` ("S5..S20: 61× DISASM z surowymi bajtami, 48× PSEUDO, xref-JSON").
- **Przeciw-dowód (census własny):** ghidra_output = **212** plików DISASM, **224** PSEUDO, 31 JSON, 1 CSV (468 plików łącznie).
- **Skutek:** niedoszacowanie (kierunek bezpieczny — nie zawyża, ale liczba jest fiktywna/nieaktualna). Czysto dokumentacyjne.
- **Poprawka:** zaktualizować liczby do faktycznego census (212/224/31) lub do zakresu, którego claim dotyczył, z definicją zakresu.
- **Test rewalidacji:** census Get-ChildItem/Count zgodny z liczbami w §9 i HANDOFF.

**F5 (wycofany w trakcie QC):** domniemana nieprecyzyjność zakresu RTTI @0xB6D851..0xB6D9DF — obalona jako FALSYWY zarzut: @0x00B6D851 = `counted_impl_p@VArkModelResourceItemFactory@@@detail@boost@@`, @0x00B6D9DF = wnętrze `p_counted_impl_p@VArkTerrainEditZoneFactory@@…` — claim executora POTWIERDZONY co do bajta. (Zostawione jako jawny ślad kontroli.)

---

## 10. Nietykalność evidence executora (dowód)

Przed zapisem QC_REPORT porównałem manifest executora (zapisany przy końcu runu) z własnym świeżym hashowaniem kluczowych plików — **wszystkie UNCHANGED** (pełne hashe w obu porównaniach):

| plik | manifest | własny świeży hash | status |
|---|---|---|---|
| 01_RAW\S2_TRUE_WALK_RESULT.json | B4AC1F2B2425… | B4AC1F2B2425… | UNCHANGED |
| 01_RAW\S1_ANCHOR_RESULT.json | 021A6D3B5F6E… | 021A6D3B5F6E… | UNCHANGED |
| 01_RAW\S3_PE_HEADER.json | 0EEE70545C1D… | 0EEE70545C1D… | UNCHANGED |
| 01_RAW\S2_TEMPLATES_TRUE_WALK.csv | 5385A5F3DED5… | 5385A5F3DED5… | UNCHANGED |
| 06_REPORT\STAGE_ACCEPTANCE_GATES.csv | 21F464F4CF96… | 21F464F4CF96… | UNCHANGED |
| 06_REPORT\00_FINAL_REPORT.md | 726896B0F598… | 726896B0F598… | UNCHANGED |
| 03_EVIDENCE\VA_EVIDENCE_REGISTRY.md | 2C8B95C05BE9… | 2C8B95C05BE9… | UNCHANGED |
| 02_ANALYSIS\A_record_definition.md | 9B856D8B59ED… | 9B856D8B59ED… | UNCHANGED |
| 02_ANALYSIS\B_template_loading_chain.md | E8725D90EC8D… | E8725D90EC8D… | UNCHANGED |
| 02_ANALYSIS\C_transform_source_and_D_placement.md | 4E564FDC1BEB… | 4E564FDC1BEB… | UNCHANGED |
| 01_RAW\S4B_RAW_HITS.json | 1D03B0084436… | 1D03B0084436… | UNCHANGED |

Moje jedyne zapisy w run-dir: `00_CONTROL\qc_probe\` (4 skrypty + 4 JSON-y wyników) + ten plik `06_REPORT\QC_REPORT.md` — oba obszary dozwolone kontraktem QC. Oryginały (Entropia.exe, templates.vfs, Models.bnt, Volumes.bnt, GHIDRA_LOCAL): wyłącznie READ-ONLY.

---

## 11. FULL_READ_LOG (co przeczytałem faktycznie) / NOT_CHECKED (moje, jawne)

**FULL / substantial read:** 00_FINAL_REPORT.md (cały); STAGE_ACCEPTANCE_GATES.csv (cały); HANDOFF.md (cały); VA_EVIDENCE_REGISTRY.md (cały); A/B/C analysis (całe); S2_TRUE_WALK_RESULT.json (cały); S3_PE_HEADER.json (cały); S1_ANCHOR_RESULT.json (struktura + measured/interpreted/errors + target_records; środek = supersededowany naive census — odczytany strukturalnie); s2_true_walk.py (cały — rekonstrukcja logiki narzędzia: brak observer-error klas, negative-control w kopii, asercja SHA fail-closed); dumpy: S6_DISASM_parse_00730c90 (cały), S11_DISASM_getter (cały), S6_DISASM_stride (cały), S6_DISASM_helper_004063d0 (cały), S6_DISASM_register (40/135 linii — prolog+CMP klucza), S9_DISASM_SINGLETON (cały), S20_DISASM_PUMP (60/95), S11_DISASM/PSEUDO_dispatcher (fragmenty 20-70/212 + greps), S10_DISASM_LOOKUP (cały), S10_DISASM_CALLER_006B28E0 (cały), S10_DISASM_CALLER_00511070 (fragmenty wokół lookupu + grep), S10_DISASM_CALLER_0043EAE0 (greps calli), S20_PSEUDO_MRQ_006B4C50 (cały), S10_PSEUDO_CALLER_00511070 (cały), S10_PSEUDO_CALLER_00567170 (head 60), S5_PSEUDO_REF_00972DF0 (fragmenty + greps magii/+0x8c/+0xa0), S5_PSEUDO_REF_00971680 (cały), S13_DISASM_emitter (head), S16_DISASM_objcreate (head), S18_DISASM_loadbyname (head), S18_DISASM_amm_ctor (head), S11_DISASM_singleton2 (head), S18_PSEUDO_BNT2 (grep fprintf "BNT2"), S14_DISASM_rm_init (grepy konkretnych VA pushy), S10_LOOKUP_CALLERS.json (cały), S20_MODEL_REQUEST_CALLERS.json (cały), S19_DISPATCHER_CALLERS.json (census), artifact_index.csv (census 541 wierszy + 10 re-hash), GHIDRA_LOCAL_COPY_MANIFEST.txt (cały); s1_anchor_verify.py (grepy asercji SHA); S*_SCRIPT_SHA256.txt (4 weryfikowane piny).

**NOT_CHECKED (mine, explicit):**
1. Pełna niezależna re-lektura wszystkich pseudokodów 25+13 call-site'ów pod kątem "cech create-object-handler" (sample 4-5 + census + denominators zrobione) — residuum pkt 6.
2. Pełny odczyt wszystkich 212 DISASM / 224 PSEUDO (~45 linków zweryfikowanych bajtowo celowanie; file-census kompletny).
3. Wiersz-po-wierszu porównanie S2_TEMPLATES_TRUE_WALK.csv z moim CSV (zamiast tego: pełna niezależna rekomputacja walka + porównanie aggregate census identyczne + target records identyczne).
4. Re-hash pozostałych ~530 wierszy manifestu (sample 10/10 + 11 kluczowych plików evidence — wszystkie PASS).
5. Zawartość binarna GHIDRA_LOCAL .rep db (2×189,759,488 B; pokryte osobnym manifestem hashy — nie jest to evidence claims).
6. Odczyt pełny skryptów s1/s3/s4/s5–s20 (piny SHA 4/4 zweryfikowane; pełna rekonstrukcja logiki wykonana dla s2 — narzędzia load-bearing rekomputacji).
7. Pełny odczyt środka S1_ANCHOR_RESULT.json (supersededowane wiersze naive census — bez znaczenia dla claims; struktura i pola kluczowe odczytane).
8. Konteksty runtime (klient nigdy nie uruchomiony — STATIC-ONLY, zgodnie z kontraktem runu; nie było czego weryfikować runtimeowo).

**Hierarchy note:** evidence klasy "oryginalne bajty + niezależny pomiar" (moje probe'y A–D na oryginalnych plikach) > dumpy Ghidra executora > raporty. Circular check: moje rekomputacje nie korzystają z generatorów executora.

---

## 12. Artefakty QC (własne, w dozwolonej lokalizacji)

- `00_CONTROL\qc_probe\qc_A_address_lock.py` / `qc_A_address_lock_result.json` (35 checks)
- `00_CONTROL\qc_probe\qc_A2_address_lock.py` / `qc_A2_address_lock_result.json` (22 checks)
- `00_CONTROL\qc_probe\qc_A3_address_lock.py` / `qc_A3_address_lock_result.json` (4 checks)
- `00_CONTROL\qc_probe\qc_B_walk_databinding.py` / `qc_B_walk_databinding_result.json` (walk + census-compare + targets + PROMPT_DELTA + negative control + BNT scans)
- `00_CONTROL\qc_probe\qc_C_registry_links.py` / `qc_C_registry_links_result.json` (18 checks + RTTI + avatar census)
- `00_CONTROL\qc_probe\qc_D_nc_manifest.py` / `qc_D_nc_manifest_result.json` (chain-constants scan + sentinel-bss + manifest re-hash 10)

Skrypty hashowane niżej (dla kompletności; SHA256 obliczone po zapisie):
- patrz `qc_probe\QC_PROBE_SHA256.txt` (wygenerowany przy finalizacji raportu).

---

## 13. FINAL_HANDOFF (compact — dla PE-MASTER)

- **ASSIGNMENT_MODE:** INTERNAL_QC
- **RUN_ID (QC):** PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912_QC (audyt runu PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912)
- **QC_VERDICT:** **QC_PASS** (0×P0, 0×P1; 1×P2 F1 + 3×P3 F2/F3/F4; wszystkie 4 klasyfikacje bramek executora uzasadnione evidence i uczciwe — nie zawyżone; rekomendowana poprawka dokumentacyjna F1–F4 przed persystencją/publish)
- **Punkt 1 GATES:** PASS (GATE-A PARTIAL uzasadniony + residuum jawne; GATE-B-C PARTIAL uzasadniony; GATE-ERA PASS uzasadniony; GATE-NC PASS uzasadniony; F1 nie zmienia klasyfikacji) — dowód: qc_A/A2/A3/B/C/D + dumpy
- **Punkt 2 ADDRESS-LOCK:** PASS 6/6 mandatory (+ ~40 dodatkowych; ZERO rozbieżności bajtowych z dumpami) — dowód: qc_A/A2/A3_*_result.json
- **Punkt 3 S2 FULL-WALK:** PASS (własny walk: **5,438**/5,438 rekordów, EOF, 0 CRC-fail, 0 undocumented, census size identyczny, D/E/DE/F/id≠id2/tail identyczne; targety 4508/4752/2249 zgodne) — dowód: qc_B_walk_databinding_result.json
- **Punkt 4 DATA-BINDING:** PASS 6/6 pozytywów na claimowanych offsetach + 2 negatywy nieobecne (+bonus separacji: 296446.nif/296445.bvi nieobecne) — dowód: qc_B (models_scan/volumes_scan)
- **Punkt 5 PROMPT_DELTA:** PASS — **executor POPRAWNY, kontrakt miał błąd** (PARAM@+0x20 = cb e1 f9 42 = 124.941f; starty 97,288/93,976; delta +6 każdorazowo) — dowód: qc_B (prompt_delta_1/2)
- **Punkt 6 SEKCJA C:** PASS-artifacts (censusy 25/13 wyprowadzone z artefaktów S10/S20 z exec-metadata; dumpy 23/23 + 11/11; metodologia w C.1/C.2 jawna; sample niezależny zgodny; NOT_CHECKED: pełna re-lektura wszystkich 34 pseudokodów) — dowód: S10/S20 JSON + censusy plików + moje lektury
- **Punkt 7 ERA-DISCYPLINA:** PASS (zero transferu; wszystkie PE2-VA jawnie jako hipoteza; każdy VA raportu z bajtami w dumpach — zweryfikowane) — dowód: grep sweep + qc_A/A2/A3
- **Punkt 8 ARTIFACT_INDEX:** PASS z F2+F3 (540/540 claim ✓; 10/10 re-hash ✓; HANDOFF.md poza manifestem; self-row nieaktualny z konstrukcji; GHIDRA_LOCAL pokryty osobnym manifestem) — dowód: census + qc_D
- **Punkt 9 COVERAGE HONESTY:** PASS (5 obszarów NOT_CHECKED jawnych; klasyfikacje nie zawyżone; residuum udokumentowane dokładnie; notka do frazy "w pełni zakotwiczony" — kwalifikowana kontekstem)
- **EVIDENCE NIETYKANE:** potwierdzone (11 kluczowych plików: manifest-hash == świeży hash, wszystkie UNCHANGED; sekcja 10)
- **NEXT_PARENT_ACTION:** adjudykacja PE-MASTER → (a) ewentualna akceptacja werdyktu QC_PASS; (b) CORRECTION_DOCUMENTATION (lub persystencja z errata) dla F1 (P2, stałe avatar 11705/11706→11769/0x2DF9 + rodzina 11655-11657), F2 (usunięcie self-row), F3 (dodanie HANDOFF.md), F4 (liczby DISASM/PSEUDO 212/224); poprawki dotyczą wyłącznie dokumentacji/manifestu — nie generatorów ani evidence; (c) open-item 1 runu (dekompilacja vtable providera/fabryki) pozostaje właściwym kolejnym runem RE.
- **BASE_SHA / HEAD_SHA / PUSH_STATUS:** niedotyczy (INTERNAL_QC bez commitów — persystencja po adjudykacji; zgodnie z kontraktem QC: ZERO commitów).
- **UNRELATED_WORK_EXCLUDED:** brak zapisów poza run-dir; GHIDRA_LOCAL tylko odczytany; oryginały READ-ONLY.

*QC wykonane w pełni na świeżym kontekście, z własnych pomiarów na oryginalnych bajtach; raport zapisany po wykonaniu wszystkich probe'ów (A→D). Wyniki probe'ów w 00_CONTROL\qc_probe\; ten raport: 06_REPORT\QC_REPORT.md.*

---

## 14. POST-QC CORRECTIONS (F1–F4) — wykonane przez pe-master-auditor (append, 2026-09-13)

**RUN_ID:** PE_935_TEMPLATE_CONSUMER_TRACE_R1_20260912_PERSIST (CORRECTION_DOCUMENTATION + PERSIST_PUBLISH; zlecenie PE-MASTER; RUN_CLASS SUPPORTING — czysta mechanika dokumentacyjna). Kolejność wykonania: F1 → F4 → F2/F3 (celowo: wiersze manifestu dla plików zmienionych F1/F4 oraz nowy wiersz HANDOFF.md policzone na stanie końcowym, nie przejściowym). Poprawki wyłącznie dokumentacyjne (dokumentacja/manifest); evidence executora (01_RAW, skrypty S1–S20, dumpy 01_RAW\ghidra_output, wyniki QC qc_*) NIETYKANE — pełny dowód re-hashowy: `persist_gates_result.json` (bramka P4).

### F1 (P2) — stałe avatar-hardcode [DOMKNIĘTE]
- Zmienione pliki (3): `03_EVIDENCE\VA_EVIDENCE_REGISTRY.md` (E.4), `02_ANALYSIS\B_template_loading_chain.md` (B.1 ogniwo 18 + adnotacja POST-QC pod tabelą B.1), `06_REPORT\STAGE_ACCEPTANCE_GATES.csv` (GATE-NC).
- Treść poprawki: "11705/11706" → **11769 (0x2DF9) @0x00511245 (fun. FUN_00511070)** + rodzina **11655/11656 (+obliczany 11657) dla FUN_006b28e0**; w adnotacjach odnotowana tabela .rdata @0x00A85838/0x00A8583C (wartości 11705/11706 istnieją tam jako u32, bez xref z .text).
- Rekalibracja (własny skan .text binarium SHA E7785430…, `persist_p1_recalibration.py` — własny parse PE, asercja SHA fail-closed; wynik: `persist_p1_recalibration_result.json`): imm32 `f9 2d 00 00` (0x2DF9) w .text = **DOKŁADNIE 1 hit** — instrukcja MOV EAX,0x2DF9 @0x00511245 (`b8 f9 2d 00 00`, imm32 @0x00511246, file offset 1,118,533) w FUN_00511070; imm32 0x2DB9 (11705) = **0 hitów w .text**; 0x2DBA (11706) = **0 hitów w .text** (negatywne); potwierdzone w .rdata @0x00A85838/0x00A8583C; rodzina: `b8 88 2d 00 00` (11656) @0x006B28F6 + `05 87 2d 00 00` (ADD EAX,0x2D87 → obliczany {11655|11657}) @0x006B2922. WSZYSTKIE asercje rekalibracji PASS; zgodne 1:1 z pomiarem QC (finding F1, §FINDINGS).
- Wniosek bramki GATE-NC (generyczność ścieżki; 0 hitów 296445/4508/296446/126740/278453 w 29 funkcjach łańcucha) **NIEZMIENIONY** — niezależnie potwierdzony (qc_D chain_constants_scan all_empty=true) + rekalibracja PERSIST (skan informacyjny całego .text: 3 surowe hity wzorca `9c 11 00 00` (4508) @0x0053270C/@0x00532769/@0x0083427E — wszystkie POZA oknami 29 funkcji łańcucha; surowe wzorce bez atrybucji instrukcji nie są stałymi semantycznymi — lekcja V2R-010).
- Census fraz po poprawce (bramka P1): warstwa dokumentacji executora (02_ANALYSIS\*.md, 03_EVIDENCE\*.md, 06_REPORT: 00_FINAL_REPORT.md, STAGE_ACCEPTANCE_GATES.csv, HANDOFF.md, GHIDRA_LOCAL_COPY_MANIFEST.txt) = **0 wystąpień "11705"/"11706"**; "11769" obecny w 3 poprawionych plikach. Wyłączenia jawne (fraza obecna legalnie, poza predykatem): `01_RAW\S1_TEMPLATES_BLOCK_CENSUS.csv` / `01_RAW\S2_TEMPLATES_TRUE_WALK.csv` — fizyczne dane rekordów (id 11705/11706/11769 istnieją jako realne template-id w templates.vfs; evidence nietykane); `06_REPORT\QC_REPORT.md` — warstwa audytu (dokumentacja F1 cytuje stare stałe); `06_REPORT\PE_MASTER_REVIEW.md` — werdykt PE-MASTER dokumentuje korektę "11705/11706→11769". Adnotacje POST-QC wewnątrz poprawionych plików warstwy executora celowo NIE cytują dosłownie starych stałych (predykat P1 wymaga 0 wystąpień w tej warstwie); pełne wartości historyczne dokumentuje wyłącznie warstwa audytu.

### F2 (P3) — self-row manifestu usunięty [DOMKNIĘTE]
- Usunięto wiersz `06_REPORT\artifact_index.csv,64694,B922E31C…` (self-reference niemożliwa do spełnienia z definicji — precedens L12). Manifest NIE zawiera własnego hasha ani hashy warstwy QC/PERSIST (QC_REPORT.md, PE_MASTER_REVIEW.md, qc_probe\*) — zgodnie z L12.
- Ujawnienie (zgodne z klasą defektu F2): przy przebudowie zaktualizowano wiersze 4 plików celowo zmienionych przez F1/F4 (B_template_loading_chain.md 7489→8371 B; VA_EVIDENCE_REGISTRY.md 7865→8443 B; 00_FINAL_REPORT.md 9585→9653 B; STAGE_ACCEPTANCE_GATES.csv 4244→4677 B; hashe nowego stanu w `persist_manifest_rebuild_result.json`; pełne przejście executor→stan pośredni→finalny: `persist_manifest_rebuild_result_run1.json` + `persist_manifest_rebuild_result.json`) — pozostawienie starych hashy odtwarzałoby defekt klasy F2 (nieaktualny wiersz manifestu) dla plików celowo zmienionych.

### F3 (P3) — HANDOFF.md w census [DOMKNIĘTE]
- Dodano wiersz `06_REPORT\HANDOFF.md,4927,E22804CB6A734F5B436C0A116D86F16AB4F3459CC5BD12D3616111FD13455DAE` (hash z dysku, stan PO F4).
- Stan końcowy manifestu: **540 wierszy danych** (539 executora + HANDOFF.md), 64,994 B, SHA256 `1BD74E7B34C3623BEDA3A75DD981DBE3E1B5362311E44312811F140A1E8201FC`; UTF-8 BOM + CRLF zachowane.
- Census dysku == manifest (scope jawny): pliki pakietu minus `00_CONTROL\GHIDRA_LOCAL\` (LOCAL-ONLY; osobny manifest 06_REPORT\GHIDRA_LOCAL_COPY_MANIFEST.txt), minus `00_CONTROL\qc_probe\` (warstwa QC/PERSIST), minus `06_REPORT\QC_REPORT.md` i `06_REPORT\PE_MASTER_REVIEW.md` (warstwa audytu/werdyktu), minus `06_REPORT\GHIDRA_LOCAL_COPY_MANIFEST.txt` (metadane manifestu zasobów LOCAL-ONLY), minus `06_REPORT\artifact_index.csv` (self, L12) → **540 == 540**, zbiór ścieżek identyczny obustronnie (persist_gates_result.json, bramka P2).

### F4 (P3) — liczby dumpów [DOMKNIĘTE]
- Własny census `01_RAW\ghidra_output\` (bramka P3): **212× DISASM, 224× PSEUDO, 31× JSON, 1× CSV = 468 plików łącznie** — zgodne z pomiarem QC (§F4 QC). Nota do formuły kontraktu "212/224/31=468": suma 212+224+31=467; 468. plikiem jest 1× CSV, którego formuła nie uwzględniała — census PERSIST odnotowuje CSV jawnie ("przelicz własnym census z dysku" — wykonane; wynik liczbowo identyczny z QC, rozbicie pełne).
- Zaktualizowano: `06_REPORT\00_FINAL_REPORT.md` §9 + `06_REPORT\HANDOFF.md` (PRIMARY_EVIDENCE_PATHS): "61× DISASM / 48× PSEUDO" → "212× DISASM / 224× PSEUDO / 31× JSON xref / 1× CSV = 468 plików łącznie" + znacznik census POST-QC F4.

### Kontrola całości (dowód nietykalności evidence — bramka P4)
- Pełny re-hash pakietu vs snapshot pre-work (`persist_pre_work_state.json`, 568 plików w chwili startu PERSIST, w tym hashe wszystkich plików evidence): wszystkie pliki evidence executora UNCHANGED poza jawnie zmienioną dokumentacją (F1: 3 pliki; F4: 2 pliki; F2/F3: manifest artifact_index.csv; ten append do QC_REPORT.md) — pełne listy stare→nowy w `persist_gates_result.json`; warstwa qc_probe (12 plików QC) == QC_PROBE_SHA256.txt; GHIDRA_LOCAL == GHIDRA_LOCAL_COPY_MANIFEST.txt.
- Autor poprawek: pe-master-auditor (sesja PERSIST). Zmiany techniczne (kod/generatory/evidence): **ZERO**.
