# QC_REPORT — PE_935_ROUND_QC_STATIC_PLACEMENT_R1_20260913 (RUN B: PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913)

- **ASSIGNMENT_MODE**: INTERNAL_QC (niezależny audytor wewnętrzny, świeży kontekst; nie executor, nie formalizator)
- **AUDITOWANY RUN**: PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913 (commit 6ab6290)
- **QC_RUN_ID**: PE_935_ROUND_QC_STATIC_PLACEMENT_R1_20260913
- **Data**: 2026-09-13
- **Metoda**: własny parser PE (00_CONTROL\qc_probe\qc_pe.py — kopia narzędzia QC), własne censusy CALL rel32 po całym .text, własny dekod switcha dispatchera (byte-table + jump-table), własny parse indeksu Portals.bnt i skan payloadów .prt na wszystkich offsetach, własne censusy plików instalacji (Parameters/20006), własne skany RTTI/stringów.
- **Binarium (asercja własna)**: D:\Eudoria_Reconstruction\pcg_install\Entropia.exe, SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (Get-FileHash — ZGODNE z kontraktem QC i S0), 8,015,872 B, image base 0x00400000, ASLR OFF.

---

## WERDYKT QC RUN B: **QC_PASS** (0×P0, 0×P1; 2×P2 + 3×P3 — wymagane poprawki dokumentacyjne przed ewentualną promocją; żaden z nich nie odwraca werdyktów bramek G1–G6)

Kluczowe twierdzenia runu (werdykt-źródło UNKNOWN-with-exact-boundary; łańcuch maszyny placementu; negatywy Portals/20006; granica 0xB9) zweryfikowane pozytywnie NIEZALEŻNIE, w większości mocniej niż wymagano (B1: 64/64 VA zamiast 5 losowych; B8: skan .prt na wszystkich offsetach, domykający własny caveat executora „aligned-only").

---

## Punkty QC (B1–B12)

### B1. S0/S14 — asercje ery + 64 cytowane VA — **PASS**
- S0 odtworzone własnym parserem co do bajtu (rozmiar, baza, sekcje, ASLR, entry offset 5,626,385, spot-checki).
- **S14_VA_EVIDENCE.json: wszystkie 64 wpisy zweryfikowane** (nie 5 losowych): dla każdego wpisu własne mapowanie VA→file-offset (offset zgodny 64/64) + surowe bajty zgodne 64/64 (qc_addr_lock_runB.json). Zawiera komplet 64 VA cytowanych w HANDOFF.
- Ścieżka: 01_RAW\S0_ERA_ASSERTION.json; 01_RAW\S14_VA_EVIDENCE.json; 00_CONTROL\qc_probe\qc_addr_lock_runB.json.

### B2. „Transformacje czytane WYŁĄCZNIE z drzewa atrybutów" + alternatywne ścieżki zapisu pól +0x08/+0x14 — **PASS** (z nuansem NOT_CHECKED, bez kontrprzykładu)
- **Odczyt w builderze**: FUN_00567770 woła FUN_00846840 (attr-pos-fetch) @0x005677C4 + FUN_00854720 (trójka) — census własny: callerzy FUN_00846840 = 7, w tym 0x005677C4 w builderze ✓. FUN_00846430 (filtr „is-transform") = `3d a8/a9/a4/a5/ac 06 00 00` + 0x23 — bajtowo dokładnie {0x6a8,0x6a9,0x6a4,0x6a5,0x6ac,0x23} ✓ (3 call-site'y: 0x004C5389/0x004C53A8/0x0051450B — ostatni w FUN_00514ef0 ✓ spójny z Z2).
- **Alternatywne ścieżki zapisu +0x08/+0x14 (test adversarialny)**: census setterów — FUN_00730f90: 15 call-site'ów w 15 funkcjach (zgodne z listą Z2 §2, 15/15 nazw po atrybucji Ghidry — site 0x0044AAFD należy do FUN_00447630, potwierdzone prologiem SEH @0x00447630 i atrybucją w ZS1/ZS3/ZS7_CALLERS.json); FUN_00730fb0: 11 site'ów; FUN_00730fd0: 7; FUN_00730f60: 21. Zbadawszy napędy wszystkich 15 funkcji setter-callers: **10 woła funkcje systemu atrybutów bezpośrednio** (walker FUN_0085b840 / FUN_00843d60 / resolver FUN_008544d0 / check FUN_00844020), a 4 bez bezpośrednich odczytów (FUN_005b5f90, FUN_00459270, FUN_0043a200, FUN_00488920) przyjmuje wartości z parametrów — dla load-bearing FUN_005b5f90 prześledzone: jej callerzy (3 site'y) leżą w FUN_005b6370, który **czyta z drzewa atrybutów** (2× FUN_0085b840 walker, 16× FUN_00844020 check, 15× FUN_004123d0 fetch) i przekazuje wartości dalej — tj. ścieżka komunikatowa 0xB9 niesie KLUCZE (kursorami FUN_007527xx), a wartości pochodzą z drzewa atrybutów ✓✓. **Kontrprzykładu „transform z sieci/pliku wprost do +0x08/+0x14" nie znaleziono.**
- **Nuans (NOT_CHECKED, jawny)**: ctor rekordu FUN_00730700 (init 12 dwordów +0x00..+0x2C, FLDZ→+0x10) ma **26 call-site'ów** (nie tylko builder): 11 z nich nie woła setterów — semantyka tych rekordów (czy to też „placement records" z innym zasilaniem) nie była badana w runie i nie jest rozstrzygnięta w moim QC (pozostaje NOT_CHECKED; dla definicji rekordu placementu = ctor+settery+rejestracja — wszystkie prześledzone ścieżki są atrybutowe).
- Drobna nieścisłość Z2 §1: „ctor FUN_00730700 zeruje 11 dwordów" — faktycznie 12 (do +0x2C włącznie); RUN A dla FUN_00730f60 podaje „11 dwordów" poprawnie (+0x00..+0x28). Layout claims (+0x08/+0x14/+0x20/+0x24) — niezaaffected.
- Ścieżka: 02_ANALYSIS\Z2_cwo_chain.md §2; 01_RAW\ghidra_output\ZS3_CALLERS.json; qc_probe\qc_setter_census.py, qc_b2_exclusive.py, qc_b2_b12.py.

### B3. FUN_00845f70 — 53 call-site'y, klasyfikacja — **PASS (census dokładny; zob. finding P2-1 dla sformułowania zakresu)**
- **Census własny = census executora**: dokładnie **53** bezpośrednie CALL rel32 → FUN_00845f70; **zbiór VA identyczny co do adresu** z ZS3_CALLERS.json (53/53) ✓.
- Sample klasyfikacji (5, wymagane 5): FUN_00514ef0 (PUSH 0x2B/0x2C → FUN_00845f70 + 0x3F1/0x3F5 → builder ✓ bajtowo), FUN_004387a0 (PUSH 0x6A5 ×2 ✓), FUN_005b72c0/FUN_005b6370 (walker+checki atrybutowe ✓), FUN_0043f4b0 (łańcuch CMP 0x6a4/0x6a5/0x6a8 + attach-family ✓), FUN_00447630 (walker + ctor + settery + rejestracja ✓) — wszystkie klasyfikacje „world-object/attr-writer" uzasadnione bajtowo.
- „ZERO w rodzinie sieciowej": na poziomie FUNKCJI potwierdzone — żaden z 53 callerów nie jest executor/communicator/packet-subsystem (FUN_004b15f0/18d0/1890/2950, FUN_0083xxxx, FUN_00419dd0 — zero trafień); na poziomie ZAKRESU ADRESOWEGO zdanie z raportu jest fałszywe (finding P2-1).
- Ścieżka: 01_RAW\ghidra_output\ZS3_CALLERS.json (FUN_00845f70_attr_setter: 53 wpisy); qc_probe\qc_setter_census.py, qc_b3_sample.py, qc_b2_exclusive.py.

### B4. Handler transform FUN_00514EF0 — **PASS** (pełne domknięcie bajtowe)
- **„Jedyny xref = DATA @0x00A7D778"**: imm32 0x00514EF0 w .text = **0 trafień** (brak callerów kodowych); w .rdata = **dokładnie 1 trafienie @0x00A7D778** ✓✓ — claim potwierdzony w całości.
- **Tabela @0x00A7D764**: 16 wpisów wskaźników kodowych (dump własny): [0x00511A90, 0x0040BB70, 0x00474410, 0x006077C0, 0x0058E280, **0x00514EF0**, 0x00606EC0, 0x00606EC0, 0x0040BB70, 0x00606E50, 0x00511AB0, 0x009154A0, 0x00606E50, 0x00984610, 0x008E0110, 0x008E0110] — wpis nr 5 (0-based) = 0x00514EF0 @0x00A7D778 ✓; identyczna z S13_CWO_HANDLER_TABLE.json (len=16) ✓; sąsiedztwo stringów ArkClientWorldObjectLogic::… @0x00A7D624 ✓ (S14).
- **Pisanie attr X/Y 0x2B/0x2C**: w body FUN_00514ef0 (0x00514EF0-0x00515EB4): `6a 2b` PUSH 0x2B @0x00515B36 → CALL FUN_00845f70 @0x00515B44; `6a 2c` PUSH 0x2C @0x00515B4E → CALL @0x00515B54; plus PUSH 0x3F1 @0x00515CD6 → CALL @0x00515CE0 i PUSH 0x3F5 @0x00515D12 → CALL @0x00515D18 ✓✓ — dokładnie zgodne z Z1 §2(iii).
- Woła builder: CALL FUN_00567c50 @0x00515345 ✓ (jedna z 3 dróg).
- Ścieżka: 02_ANALYSIS\Z2_cwo_chain.md §1 (droga C); 01_RAW\ghidra_output\ZS2_PSEUDO_00514EF0.txt; 01_RAW\S13_CWO_HANDLER_TABLE.json; qc_probe\qc_final_bytes.py, qc_b2_b12.py.

### B5. Kanał sieciowy (łańcuch executora + case 0xB9) — **PASS** (każde ogniwo bajtowo, łącznie z mechanizmem switcha)
- **FUN_00419DD0 (CommunicationSubsystem ctor)**: `6a 34` PUSH 0x34 @0x00419E9B (operator_new(0x34)) → CALL FUN_004b15f0 @0x00419EC5 → **`89 46 28` MOV [ESI+0x28],EAX @0x00419ED8** — executor @ [comm+0x28] ✓✓.
- **FUN_004b2950 (Execute)**: `81 ff ac 00 00 00` CMP EDI,0xAC → CALL 0x004B2270 ✓ (case 0xac); CMP EDI,0xB2 → deferred; bramka → **CALL FUN_004b18d0 @0x004B29A9** ✓; ścieżka odroczona → CALL FUN_004b1890 @0x004B29D7 ✓.
- **FUN_004b1890 (enqueue)**: body = ring push 12 B {x,payload,type} z head@+0x10/tail@+0x18 (`8b 51 18 8b 41 10 83 ea 0c 3b c2…`) ✓ — zgodne z „ring odroczeń push {type,x,payload} 12B".
- **FUN_004b18d0 (dispatch) — skąd 0xB9 (własny dekod)**: `MOV EAX,[ESP+4]; ADD EAX,-0xA2 (05 5e ff ff ff); CMP EAX,0x25 (83 f8 25); JA default; MOVZX EAX,BYTE [EAX+0x004B1B3C]` (byte-table mapująca case→slot) `; JMP [EAX*4+0x004B1AE4]` (adresowanie absolutne). **Case 0xB9 → indeks 0x17 → byte-table[0x17]=0x0C → slot 12 jump-table @0x004B1AE4 → 0x004B1A11 → blok `MOV ECX,[ESP+0x10]; PUSH ECX; CALL 0x005B72C0 @0x004B1A16`** ✓✓✓ — „case 0xB9 → FUN_005b72c0" potwierdzone przez faktyczną tabelę skoków (dekompilat ZS3_PSEUDO_004B18D0 zgodny: `case 0xb9: FUN_005b72c0(param_2)`).
- **FUN_005b72c0 → FUN_00567c50 @0x005B7567** ✓ (jedyne 2 call-site'y FUN_00567c50 poza tym: 0x0058E0B7 w FUN_0058db50, 0x00515345 w FUN_00514ef0 = drogi A/C ✓); **FUN_00567c50 → FUN_00567770 @0x0056836C** (jedyny call-site buildera ✓); FUN_00567770: settery f60 @0x005678F5→(LEA @0x005678FF)/f90 @0x00567906/fb0 @0x00567917/fd0 @0x00567934 + fetch atrybutów FUN_00846840 @0x005677C4 ✓.
- Droga A: **FUN_00468910 → FUN_0058db50 ×3** (0x00469299/0x004692AB/0x00469419 ✓ — „×3" odnosi się do tych call-site'ów, potwierdzone); site 0x0058E0B7 ∈ FUN_0058db50 (granica funkcji zweryfikowana — wewn. 0xCC przy 0x0058DE34 to bajt displacement LEA [ESP+0xCC], nie padding).
- Ścieżka: 02_ANALYSIS\Z1_producer.md §2(ii), Z2 §1; 01_RAW\ghidra_output\ZS3_PSEUDO_004B18D0.txt, ZS6_PSEUDO_00419DD0.txt, ZS6_DISASM_FUN_004b2950_full.txt, ZS3_DISASM_FUN_0058db50_call_00567c50.txt; qc_probe\qc_final_bytes.py, qc_bounds2.py, qc_b6_bound.py.

### B6. Granica producenta 0xB9 — **PASS** (granica uczciwa; jeden klauzul z evideną PLAUSIBLE — finding P3-3)
- **Statyczna nieosiągalność xrefem — potwierdzona bajtowo**: Execute FUN_004b2950 = **0 bezpośrednich callerów** (tylko wirtualnie przez vtable 0x00A7C1FC [dtor 0x004b1210, Execute 0x004b2950] ✓); enqueue FUN_004b1890 = **1 caller** (sam Execute — ścieżka odroczona); dispatch FUN_004b18d0 = **2 callerów** (0x004B29A9 w Execute i 0x004B1BE6 w drain-ring FUN_004b1c70 — oba wewnątrz rodziny executora). Producer przez statyczny graf wywołań **nie istnieje** ✓.
- **Test adversarialny 0xB9**: wszystkie 71 wystąpień imm-bytów `b9 00 00 00` w .text sklasyfikowane: prawie wszystkie to końcówki displacements JZ/JNZ (+0xB9), kodowania SIB (`c7 04 b9…`), MOV ECX,imm (opcode B9) i offsety stosu (LEA [ESP+0xB9]); realne stałe 0xB9 (PUSH/MOV): 0x004F1325→CALL 0x008EBD90, 0x005CEA81/0x005CEB24→(funkcje 0x005CExxx), 0x005D0EE4/0x005EC9B2→CALL **FUN_007ce1e0** (getter A — argument dla późniejszego wywołania, nie executor), 0x008FB37D→CALL 0x00719F70, tablica stałych [ESP+0x6C]=0xB9,0xBA,0xBB… — **żadne nie zasilą executora typu komunikatu** ✓.
- **boost::bind**: RTTI verbatim potwierdzone własnym skanem — TD `?$mf1@XVCommunicationSubsystem@@ABVArkChannelID@@@_mfi@boost@@…` @0x00B6D271/0x00B6D292 + mf0/mf3 CommunicationSubsystem ✓; ZS2_BIND_HUNT.json dokumentuje pusty wynik szukania construction sites (0) — granica była BADANA, nie pominięta.
- **Nuans (finding P3-3)**: „producent = handler rejestrowany dynamicznie (boost::bind)" — rejestracja dynamiczna to wniosek z obecności RTTI bindów + braku statycznych xrefów (evidence: PLAUSIBLE→STRONGLY_SUPPORTED), nie prześledzony fakt; „statycznie nieosiągalny xrefem" — CONFIRMED (jak wyżej).
- Ścieżka: 02_ANALYSIS\Z1_producer.md §2(ii) GRANICA; 01_RAW\ghidra_output\ZS2_BIND_HUNT.json; qc_probe\qc_b6_bound.py.

### B7. Kanał FILE (store "Data\Parameters" + parsery VFS) — **PASS** (z finding P3-2 — liczba plików)
- Store-y: FUN_0094dfc0/FUN_0094fe00 (S14: bajty potwierdzone ✓ — singleton + store 0xa4); ścieżka "Data\Parameters\" budowana przez FUN_0094ba00/FUN_0094f250 (S14 ✓ — bajty @0x0094ba00 = PUSH 0x00a47f89 = "Data\Parameters\\"); reader VFS FUN_00972df0 (S14 ✓) — **to ta funkcja otwiera pliki VFS parametrów** (składowa store-init FUN_0094dfc0: new(0xa4) → ctor → VFS reader), parser kursorowy FUN_00730c90 (rodzina z RUN 3; S14 ✓).
- **Censusy imm potwierdzone dokładnie**: 20005 (0x4E25) = 8 ✓ (claim „8 trafień"), 20007 (0x4E27) = 10 ✓, 24007 (0x5DC7) = 32 ✓; 20001 = 2, 20002 = 3, 20040 (0x4E48) = 5 — pliki 20001/20002/20005/20007/24007.vfs istnieją w pcg_install\Data\Parameters ✓ (własne listowanie).
- **Brak pliku-placementów udowodniony** na powierzchni censused: Parameters zawiera wyłącznie .vfs parametrów (żaden nie jest plikiem placementów statyków — rozstrzygnięcie H1 pozostaje „bez pozytywu", uczciwie), Portals.bnt/.prt = czysty dPVS (B8), **20006.vfs nie istnieje** (B9).
- Finding P3-2: liczba „20 plików .vfs parametrów" w raporcie nie odpowiada rzeczywistemu stanowi (27 .vfs: 18× 20xxx + 24007 + 8 nazwanych; naturalne liczenia dają 19/21/27, nie 20) — drobna, nie-nośna.
- Ścieżka: 02_ANALYSIS\Z1_producer.md §2(i); 01_RAW\S5_IMMEDIATE_SCAN.json, ZS1_S5_VALIDATION.json (klucze potwierdzone); qc_probe\qc_a10_b9.py (censusy imm), własne listowanie katalogu.

### B8. Portals.bnt/.prt — NEGATYW — **PASS** (pełna reprodukcja niezależna + wzmocnienie)
- **Własny parse indeksu** (D:\Eudoria_Reconstruction\pcg_install\Data\Portals\Portals.bnt, 80,682 B; stopka [73218]['BNT2'] ✓): indeks = **[u32 liczba wpisów = 276 @73218][276 wpisów {nazwa\n, size, offset, aux}]**; **276 wpisów, wszystkie .prt (276/276, 0 non-.prt)** ✓; boundary-invariants: **0 naruszeń** (każdy offset+size ≤ 73218) ✓; rozmiary min=42 / mediana=212 / max=1990 ✓ (dokładnie jak Z3); id-range 382811..592741 ✓; total .prt bytes = 73,218 ✓.
- **Próbki kontraktowe**: okno 505000–510000 = **19 wpisów** (poprawny parse z nagłówkiem licznika): 505009, 505033, 505076, 505211, 505227, 505593, 505753, 505777, 505815, 505948, 506371, **507165**, 507204, 507224, 508495, 508588, 508949, 509990, 509991 — lista Z3 zawiera 18 z nich, **pomijając 507165** (zob. finding P2-2: parse executora pominął 4-bajtowy nagłówek licznika, wchłaniając go w nazwę pierwszego wpisu `\x14\x01\x00\x00507165.prt`); outliery 382811/422806/592739/592741 — wszystkie istnieją ✓ (poprawne w obu parse'ach).
- **Skan 13 anchorów (ten sam zestaw co executor: 4508/4752/2249, 296445/126740/278453, 296446, 20005/20006/20007, 0xB9, 0x6A4/0x6A8)**: **0 trafień × 13** w moim skanie surowym po **WSZYSTKICH offsetach** (executor skanował aligned-only i sam zaznaczał caveat „misaligned possible" — mój skan domyka ten caveat: 0 także na offsetach niealigned) ✓✓ — werdykt strukturalny „.prt nie niosą ID/transformów placementów" WZMOCNIONY.
- Census u32: unikalnych aligned u32 = **10,413** (identycznie jak S12) ✓; wartości w zakresie 100k–460k występują (moje 627 wystąpień aligned ≈ ich 148 unikalnych — metryki zliczają inaczej: wystąpienia vs unikalne; zgodne ze sobą).
- Struktura payloadu: **u16@0 = 0x0101 (257) we WSZYSTKICH 276 próbkach** (census: {257: 276}) ✓ — zgodne z Z3; AABB-f32 obecne (sample 382811: −6.00499/+6.00499, +2.497787, +3.811898 — patrz finding P3-1: transkrypcja liczb w Z3 nieprecyzyjna); reader-chain (fabryka 0x00A91C88 [slot0 0x0041B870, slot1 0x0084B270] ✓ S14; item-ctor 0x00852A90 ✓; parser FUN_00852750 ✓ S14) — bajty potwierdzone.
- **Pokrycie skanu negatywnego**: mimo błędu parse'owania nagłówka (P2-2), pola size/offset pierwszego wpisu parsowały się poprawnie w obu wariantach — zakresy payloadów w skanie 13-anchorów są identyczne w moim i executora parse'u → negatyw 0×13 zostaje kompletny w obu.
- Ścieżka: 02_ANALYSIS\Z3_portals.md; 01_RAW\S11B_PORTALS_INDEX.json; 01_RAW\S12_PRT_CONTENT_CHECK.json; qc_probe\qc_b8_portals.py (pełny niezależny parse).

### B9. Anomalia 20006/0x4E26 — **PASS** (census dokładny)
- **29 użyc**: własny census imm32 0x4E26 w .text = **dokładnie 29** ✓ (dominują wzorzec `MOV DWORD [ESP+xx],0x4E26` przed wywołaniami systemu atrybutów — param-set 20006 przekazywany do walkerów; 3× bezpośredni PUSH).
- **Plik nie istnieje**: 20006.vfs nieobecny w pcg_install\Data\Parameters (własne listowanie — 27 .vfs, brak 20006) ani nigdzie w pcg_install (rekurencyjne szukanie *20006* → 0 wyników) ✓✓. Anomalia potwierdzona dokładnie jak raportowana.
- Ścieżka: 02_ANALYSIS\Z1_producer.md §2(i); 01_RAW\S5_IMMEDIATE_SCAN.json; qc_probe\qc_a10_b9.py.

### B10. Pole D: getterzy + G4 „PASS_WITH_BOUNDARY" — **PASS**
- **Bajty**: 0x0048ADA0 = `8b 41 10 c3` (MOV EAX,[ECX+0x10]; RET — getter D dword) ✓; 0x00861240 = `d9 41 10 c3` (FLD [ECX+0x10]; RET — getter D f32) ✓ (S14 + własny odczyt).
- **Censusy**: FUN_0048ada0 = **116** bezpośrednich callerów (claim „80+" — konserwatywnie prawdziwe ✓; census ucięty na 80 w S9_GETTER_STUB_SCAN z pełną liczbą w JSON — zgodne z SELF_CHECK); FUN_00861240 = **10** ✓ dokładnie.
- Konsument FUN_008553d0 (konstruktor-walker): CALL getter-D @0x008556DF ✓; gałąź param-setu: `CMP EAX,0x4E38` @0x008557DB → selekcja wariantu przez `LEA EAX,[ESI-4]; CMP EAX,3; JMP [EAX*4+0x00855BB4]` (tablica indeksowana D−4; widoczne w bajtach: slot 6→3, 7→4) ✓ — zgodne z claimem „D=4/5→2, 6→3, 7→4".
- **G4 „PASS_WITH_BOUNDARY" — granica jawna i uczciwa**: nie domknięte = konkretna semantyka liczbowa wartości 124.941 przy 4508 (RUNTIME-UNOBSERVED, statycznie nierozstrzygalne) — wyrażone wprost w raporcie §4 i bramce; konsumentów podano jako STATIC-PROOF. Brak maskowania FAIL-i.
- Ścieżka: 02_ANALYSIS\Z4_field_d.md; 01_RAW\S9_GETTER_STUB_SCAN.json; qc_probe\qc_final_bytes.py + własny dump gałęzi 0x008557D0-0x00855830.

### B11. Bramki G1–G6 — **PASS** (klasyfikacje zgodne z evidence; PASS_WITH_BOUNDARY uzasadnione)
- **G1-PRODUCER PASS_WITH_BOUNDARY — UZASADNIONE**: łańcuch VA-locked do granicy (manager/walker/settery/gettery/typy 0x6A4-family — wszystko bajtowo potwierdzone); 3 kanały zskanowane (FILE: censusy imm + pliki ✓; NETWORK: łańcuch executora do buildera ✓ + brak statycznego producenta ✓; DERIVED: 53-site census ✓ z korektą P2-1); granica = punkt wstawienia danych do kontenera atrybutów — jawna; brak fałszywego werdyktu FILE/NETWORK/BOTH ✓ (werdykt UNKNOWN-with-exact-boundary — poprawny fail-closed).
- **G2-CWO PASS — POTWIERDZONE**: 3 napędy (A: FUN_00468910→FUN_0058db50 ×3 ✓ bajtowo; B: executor→case 0xB9→FUN_005b72c0 ✓ przez jump-table; C: tabela .rdata→FUN_00514ef0 ✓ jedyny-xref-DATA) → FUN_00567c50 (3 call-site'y ✓) → FUN_00567770 (1 caller ✓) → settery+rejestracja ✓; krawędzie nieudowodnione oznaczone jawnie (5 pozycji) ✓.
- **G3-PORTALS PASS — POTWIERDZONE** (B8: pełna niezależna reprodukcja + wzmocnienie negatywu).
- **G4-D-FIELD PASS_WITH_BOUNDARY — UZASADNIONE** (B10).
- **G5-ERA PASS — POTWIERDZONE** (B1: S0 + 64/64 S14; zero transferu PE2 — Gb12 wyłącznie oracle).
- **G6-GENERALITY PASS — POTWIERDZONE**: drugi przypadek (siblingi 4752/2249/296446/20007 w negatywie .prt ✓); kontrole negatywne: filtr wrong-ID→0 (FUN_00846430 — bajtowo), atrybut-nieistniejący→rekord nie powstaje (podwójny odczyt gated w FUN_00567770 — dekompilat GA8 + struktura zgodna z B2), dystans-gate/capacity-push ✓ (FUN_00567b40 — 3 call-site'y, w tym 2 w FUN_00567c50 ✓).
- Ścieżka: 06_REPORT\REPORT.md (sekcja Bramki); 02_ANALYSIS\*; weryfikacje jak wyżej.

### B12. Tabele CWO @0x00A7D764/0x00A7D778 + 0x00A7D8EC/0x00A7DA34 — **PASS**
- **0x00A7D764**: 16 wpisów = wskaźniki kodowe (format: płaska tablica dword; koniec wyznaczony przez wpisy zerowe @+0x40) ✓; **0x00A7D778 = wpis [5] = 0x00514EF0** ✓ (B4).
- **0x00A7D8EC**: **74 wpisy** (entry[73]=0x00585180 — kod; entry[74]=0x00AA14E8 — poza .text, koniec runu) ✓ — dokładnie „74" jak Z2/HANDOFF; head: [0x00520940, 0x00775CA0×3, 0x004926E0, …] — powtarzalny handler-domyślny 0x00775CA0 + właściwe handlery ✓.
- **0x00A7DA34**: **72 wpisy** (entry[71]=0x008E1840 — kod; entry[72]=0x00AA15D4 — koniec) ✓ — dokładnie „72"; head: [0x00521C80, 0x00775CA0×3, 0x004926E0, …] ✓.
- S13_CWO_HANDLER_TABLE.json: census runów zdefiniowany dla regionu 0x00A7D400-0x00A7E400 — runy 74/72 i 16 obecne, zgodne z moimi dumpami ✓.
- Ścieżka: 01_RAW\S13_CWO_HANDLER_TABLE.json; 02_ANALYSIS\Z2_cwo_chain.md NOT_CHECKED #3; qc_probe\qc_b2_b12.py.

---

## FINDINGS (RUN B)

### **P2-1: fałszywe zdanie o zasięgu censusu FUN_00845f70 (drift raportu od własnego artefaktu)**
- **Źródło (2 miejsca)**: 06_REPORT\REPORT.md §1 pkt 5: „FUN_00845f70 (setter atrybutu) ma 53 call-site'y — **WSZYSTKIE w kodzie world-object klienta (0x0043–0x0051), ZERO w rodzinie sieciowej**…"; 02_ANALYSIS\Z1_producer.md §2(iii): „…53 call-site'y — WSZYSTKIE w kodzie world-object 0x0043–0x0051; **ZERO w rodzinie sieciowej 0x0082–0x0084**".
- **Przeciwieństwo fizyczne**: własny census i census runu (ZS3_CALLERS.json, entry FUN_00845f70_attr_setter — **zbiory 53/53 identyczne**) pokazują **5/53 site'ów POZA 0x0043–0x0051**: 0x0056984B (FUN_005697f0), 0x005B6F95 (FUN_005b6890), **0x005B7376 (FUN_005b72c0 — handler komunikatu 0xB9)**, 0x0084738C + 0x0084739F (FUN_00847270 — dispatch typu atrybutu). Dwa z nich (0x008473xx) leżą w zakresie 0x0082–0x0084, który Z1 sam etykietuje „rodziną sieciową" — ale funkcjonalnie FUN_00847270 to maszyneria atrybutów, nie sieć.
- **Skutek**: zdanie jako opis censusu jest fałszywe; czytelnik bazujący na nim pominie fakt, że **rodzina handlera 0xB9 (FUN_005b72c0/FUN_005b6890) sama pisze atrybuty przez FUN_00845f70** — co istotnie WZBOGACA obraz H4 (0xB9 = główny otwarty kandydat; handler nie tylko czyta katalogi, ale i propaguje atrybuty). Liczba 53 — dokładna; semantyczny wniosek „zero writerów z podsystemu sieci (executor/communicator/packets)" — prawdziwy na poziomie funkcji (0 z 53 callerów nie należy do FUN_004b15f0/18d0/1890/2950, 0x0083xxxx, 0x00419dd0); werdykt UNKNOWN-with-exact-boundary **nie ulega zmianie**.
- **Poprawka (dokumentacyjna, w nowym amendment-correct run)**: w REPORT §1 pkt 5 i Z1 §2(iii) zastąpić zdanie zasięgowe atrybucją per-funkcja: „53 call-site'y w 53 lokalizacjach; 48 w kodzie world-object (0x0043–0x0051 region + FUN_00569xxx/FUN_005b6890/FUN_005b72c0 z rodziny CWO-Logic), 2 w FUN_00847270 (dispatch typu atrybutu), 0 w podsystemie sieci (executor/communicator/packets)". Jawnie odnotować, że handler 0xB9 pisze atrybuty (wzmocnienie kandydatury H4).
- **Test rewalidacji**: porównanie zbioru 53 VA (mój census vs ZS3_CALLERS.json) — 53/53 identyczne; klasyfikacja per-funkcja wg func_entry z artefaktu.

### **P2-2: parse indeksu Portals.bnt pominął 4-bajtowy nagłówek licznika → dwa fałszywe detale censusu w Z3 §2 (fantomowy „duplikat"; okno 18 zamiast 19)**
- **Źródło**: 02_ANALYSIS\Z3_portals.md §2: „wpisy {nazwa\n(0x0A), int32 size, int32 offset, int64 aux} ×276 — 276/276 wpisów .prt … **275 unikalnych id + 1 duplikat** (count 276 vs 275 — zduplikowane id w indeksie…)"; oraz: „**Próbki kontraktowe**: w oknie 505000–510000 istnieje **dokładnie 18 wpisów** (…)".
- **Dowód fizyczny (własny parse z nagłówkiem)**: @73218 stoi **u32 = 276 (0x114)** — nagłówek liczby wpisów; wpisy zaczynają się @73222. Parse executora (S11b/Z3) startował 4 bajty wcześniej, wchłaniając licznik w nazwę pierwszego wpisu (`\x14\x01\x00\x00507165.prt` — stąd „1 duplikat" i „275 unikalnych"). Po korekcie: **276 wpisów .prt, 276 unikalnych numerycznych id, 0 duplikatów**; okno 505000–510000 = **19 wpisów** (na liście Z3 brakuje **507165**).
- **Skutek**: dwa fałszywe szczegóły strukturalne (kwestionują „zduplikowane id" i kompletność próbki kontraktowej okna); twierdzenia NOŚNE nietknięte — 276/276 .prt ✓ (prawdziwe w obu parse'ach), 0 naruszeń granic ✓, min/mediana/max 42/212/1990 ✓, outliery ✓, **negatyw 13×0 anchorów kompletny** (pola size/offset pierwszego wpisu parsują się poprawnie w obu wariantach, więc pokrycie payloadów identyczne), werdykt G3 (rola .prt = czysty cell-graph dPVS) — bez zmian.
- **Poprawka**: w amendment-run poprawić S11b/Z3: format indeksu = [u32 count][count × {name\n, size, offset, aux}]; usunąć claim o duplikacie; lista okna = 19 wpisów (z 507165).
- **Test rewalidacji**: qc_b8_portals.py + własny parse z nagłówkiem (wyniki w tym raporcie); porównanie nazwy pierwszego wpisu w obu wariantach.

### **P3-1: nieprecyzyjna transkrypcja AABB próbki 382811.prt w Z3 §2**
- **Źródło**: 02_ANALYSIS\Z3_portals.md §2: „np. 382811: f32-pary **-6.001/+6.001, -2.437/+2.4966, -0.000388/+3.812** = AABB min/max".
- **Pomiar niezależny (payload 140 B)**: wartości obecne to −6.00499/+6.00499 (±6.005), +2.497787, +3.811898, −2.374126 (i −2.638733 w sąsiedztwie); „−2.437" ani „−0.000388" nie odtwarzają się w progu 0.01 (najbliższe −2.374/−0.00499). Struktura (f32-pary AABB-like w sub-bloku grafu) — prawdziwa; u16 nagłówka = 0x0101 (257) we wszystkich 276 próbkach — potwierdzone ✓; negatyw 13×0 anchorów — potwierdzony (B8).
- **Skutek**: kosmetyczne zafałszowanie liczb w opisie próbki; żaden werdykt nie zależy od tych konkretnych liczb.
- **Poprawka**: w amendment-run poprawić transkrypcję na wartości zmierzone (−6.005/+6.005, −2.374/+2.498, −0.005/+3.812) lub podać offsety bajtów, z których f32 czytano.
- **Rewalidacja**: qc_b8_portals.py (f32-skan próbki po wszystkich offsetach).

### **P3-2: liczba „20 plików .vfs parametrów" nie odpowiada stanowi katalogu**
- **Źródło**: 06_REPORT\REPORT.md §1 pkt 3: „census Data\Parameters: **20 plików .vfs** parametrów, 20006.vfs nie istnieje…"; Z1 §3 pkt 3 analogicznie.
- **Pomiar niezależny**: Data\Parameters zawiera **27** plików .vfs: 18× 20xxx (20001, 20002, 20005, 20007, 20009, 20011, 20012, 20014, 20015, 20016, 20017, 20030, 20033, 20034, 20037, 20039, 20040, 20043) + 24007 + 8 nazwanych (AmbientAudioZones, EnvironmentZones, hierarchy, materials, sids, templates, textures, videos). Żadna naturalna metodologia nie daje 20 (kandydaci: 19 numerycznych / 21 / 27).
- **Skutek**: drobna niespójność liczbowna w nie-nośnym elemencie (kluczowe twierdzenia: brak 20006.vfs ✓, istnienie 20001/20002/20005/20007/24007 ✓ — potwierdzone dokładnie).
- **Poprawka**: podać rzeczywistą liczbę i metodologię zliczania w amendment-run.
- **Rewalidacja**: własne listowanie katalogu ( wynik w handoff QC).

### **P3-3: „producent 0xB9 = handler rejestrowany dynamicznie (boost::bind)" — siła dowodu nieoznaczona**
- **Źródło**: 06_REPORT\REPORT.md §1 pkt 4 (ostatnie zdanie); HANDOFF werdykt-źródło.
- **Pomiar niezależny**: statyczna nieosiągalność xrefem — CONFIRMED (B6: Execute 0 callerów, enqueue 1, dispatch 2 wewn., zero stałych 0xB9 zasilających executor); obecność RTTI bind/mf1<CommunicationSubsystem, ArkChannelID&> — CONFIRMED (@0x00B6D271); construction sites bindów — **0 znalezionych** (ZS2_BIND_HUNT.json puste). Samo „rejestrowany dynamicznie" to wniosek (RTTI + brak xref), nie prześledzony fakt — w raporcie brak etykiety siły dowodu dla tej klauzuli (RESZTA granicy jest uczciwie jawna).
- **Skutek**: czytelnik może wziąć mechanizm rejestracji za prześledzony fakt; werdykt UNKNOWN-with-exact-boundary nie ulega zmianie (bo granica i tak leży PRZED producentem).
- **Poprawka**: w amendment-run dodać etykietę: „rejestracja dynamiczna: PLAUSIBLE→STRONGLY_SUPPORTED (RTTI verbatim; brak statycznych construction sites — ZS2_BIND_HUNT); nieosiągalność xrefem: CONFIRMED".
- **Rewalidacja**: qc_b6_bound.py + ZS2_BIND_HUNT.json.

---

## Mikro-rozjazdy odnotowane (bez findingu)
- Z2 §1: „ctor FUN_00730700 zeruje 11 dwordów" — faktycznie 12 (+0x00..+0x2C); bez wpływu na layout claims.

## NOT_CHECKED (w moim QC — jawna lista)
1. 11 z 26 callerów ctora FUN_00730700 bez setterów — czy budują rekordy-placement innymi ścieżkami (patrz B2; brak kontrprzykładu dla ścieżek prześledzonych).
2. Pełna dekompilacja FUN_0084f7a0 (wejście parsowania .prt) — zgodnie z NOT_CHECKED runu; struktura .prt potwierdzona niezależnie na poziomie bajtów (B8).
3. Pole aux int64 indeksu BNT — bez zmian (NOT_CHECKED runu).
4. TerrainEditZones.bnt — bez zmian (NOT_CHECKED RUN 3).
5. Komplet wirtualnych ciał rejestru klas (Service/Commander/Manager) + pełna mapa typów tabel 74/72 — nagłówki, liczby wpisów i wybrane wpisy zweryfikowane; pełna semantyka każdego wpisu poza zakresem (zgodnie z NOT_CHECKED #3 runu).
6. FUN_00841920 (worker resolvera) — bez zmian (NOT_CHECKED #5 runu).
7. Wszystkie 10 tur Ghidry (ZS1-ZS10) — weryfikowałem artefakty selektywnie wg kluczowych claims (S14 w całości 64/64; S12 w całości; ZS3_CALLERS klucz-w-całości; ZS2_BIND_HUNT w całości; ZS3_PSEUDO_004B18D0 w całości); pełna lektura każdego dumpa pseudo nie wykonana.
8. Runtime-capture 0xB9 — zakazane (STATIC-ONLY); nie wykonano (spójnie z runem).
9. Pole D — semantyka liczbowa 124.941 — RUNTIME-UNOBSERVED (nie rozstrzygalne statycznie; zgodnie z G4 boundary).

## Integralność evidence executora
Sole zapisy QC w katalogu runu: 06_REPORT\QC_REPORT.md (ten plik) + 00_CONTROL\qc_probe\* (narzędzia własne + qc_addr_lock_runB.json). Pliki executora nietknięte — hashe kluczowych plików pobrane PO zakończeniu weryfikacji (odczyt-only przez cały QC): REPORT.md = 4B05C1DBEE8A13E265788A3165CD690D7F56BD5D1F797A9792E8BD630A311B60; S14_VA_EVIDENCE.json = 4A0FD1F6069926BD0FE2141FF80F844211837A2E1BDB7F28F7E83438A58EBFD5; S12_PRT_CONTENT_CHECK.json = 9C626E112D5C54E45A4F5E781498091A0AE722FFCD4C582BD84961392963424A; VA_EVIDENCE_REGISTRY.md = 2231F6FF3EBD666F1ED1BE446881BB6E09D2135BDD20E5A83E34E246F64B12AC (pełny wykaz w handoff QC).

**QC_VERDICT_RUN_B: QC_PASS** — 0×P0, 0×P1, 2×P2 (P2-1: fałszywe zdanie o zasięgu censusu 53-site'ów FUN_00845f70; P2-2: parse indeksu Portals.bnt bez nagłówka licznika → fantomowy „1 duplikat" i niekompletne okno 18/19 z pominiętym 507165 — oba wymagają amendmentu dokumentacyjnego; semantyczne wnioski i wszystkie werdykty bramek nietknięte), 3×P3 (transkrypcja AABB, liczba plików .vfs, etykieta siły dowodu „dynamic boost::bind"). Wszystkie twierdzenia nośne potwierdzone niezależnie bajtowo.
