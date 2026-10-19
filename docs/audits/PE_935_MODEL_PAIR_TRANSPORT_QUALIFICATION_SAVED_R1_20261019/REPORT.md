# PE_935_MODEL_PAIR_TRANSPORT_QUALIFICATION_SAVED_R1 — REPORT.md

RUN_ID: PE_935_MODEL_PAIR_TRANSPORT_QUALIFICATION_SAVED_R1_20261019
Kontrakt: AUTHORING_ROOT\CONTRACT.md (SHA256 69472F5D1D9766EB126C5E29FFBC82CC26644B12E6E560F378E5CCFEB973EE27), zweryfikowany przed startem.
Preflight: evidence_guard check = PASS (authoring 25 plików / manifest 24 wiersze; external pins 1275); host WINDEV2407EVAL; OUTPUT_ROOT świeży (utworzony przez guard start).
Korekty postaudytu: zapisane w AUDIT_CORRECTIONS_APPLIED.json (9 korekt C1–C9).

## WYKONANIE / ATRIBUTYACJA

- TASK_DISPATCHES: 2 próby pe-reconstruction (P01_EXEC_R1, P01_EXEC_R2). **Obie niekompletne**: każda zapisała tylko RUN_STARTED.json i zwróciła pusty task result (stan completed bez treści). Zgodnie z CONTRACT §10 po dwóch niekompletnych próbach wykonano **DIRECT_ANALYST_FALLBACK** rodzica na tym kontrakcie, z pełnym attribution w każdym pakiecie. Nauka P01–P10 wykonana bezpośrednio przez rodzica. QC_ORIGIN: świeży pe-master-auditor dispatchowany po seal (patrz QC sekcja poniżej).
- Struktura: 10 pakietów naukowych (P01–P10), wszystkie z plan→admit→extract przed jakąkolwiek analizą treści; DENY 000006 (błędny plan path, incydent operacyjny bez wpływu na naukę) zachowany w CONTROL\EVENTS.

## GŁÓWNE PYTANIE — ROZSTRZIĄŚNIĘCIE

**Czy pair/callback kod to synchroniczne zbieranie/projekcja, request transport, czy coś inne — i kto konsumuje wynik?**

**H1 (synchroniczne zbieranie/projekcja do kontenera): CONFIRMED.** Pełny łańcuch instrukcyjny (wszystkie ciała w oknach admission):

1. **006C3640** (P01): synchroniczna pętla map+append — dla każdego elementu zakresu [arg2,arg3) stride 0x20 wywołuje callback arg5 (CALL EBX) i dopisuje parę 2×DWORD (stride 8) z wyniku do kontenera arg4 (tail@+4/limit@+8), grow przez 006C2E00, wynik przez *arg1. Element-stride 0x20, append 8B, pusty zakres → *arg1=arg4.
2. **006C3F50** (P03): rozwiązuje obiekt z id (0043A550→0072F580, opaque), inline dopisuje parę **{0x66, A}** (A=007CE1E0(EDI), opaque), potem CALL 0040B070(EDI) → para DWORD z [EDI+0x14]/[EDI+0x18] = **(begin,end) zakresu** elementów, i 006C3640(&out, begin, end, kontener, **008BD720** [immediate!], A). A (arg6) jest nieczytany w 006C3640.
3. **006C3FE0/006C4020** (P04/P05): pętle po tablicach DWORD (8 i 2 elementów) → 006C3F50(id, kontener) dla każdego id.
4. **006C4060** (P06/P07): **CONTAINER_OWNER** — pełny prolog SEH; trzy stackowe kontenery; trzy wywołania kolekcji ze **statycznych tablic ID** 0xA855F0 (8 id), 0xA858B8 (2 id), 0xA858C0 (2 id); potem konsumpcja: 006C3D40 (sort), 006C2C90 (adjacent-find duplikatów), warunkowe 006C2C50 (opaque), 006C36B0 (projekcja) — ciało NIE w pełni domknięte (open edge za 006C4160, poza budżetem).
5. **006C3D40** (P08): sortowanie zakresu 8B par (introsort-shaped: log-depth → 006C3740 → 006C3330; STRONGLY_SUPPORTED, callees opaque).
6. **006C2C90** (P09): adjacent-find równych sąsiednich par; handler duplikatu 006C24B0 (opaque).
7. **006C36B0** (P10): projekcja każdej pary przez transform **006C29D0** (opaque, dostaje stack-context {0x823C10, EDI, EBX(00415670), 0xA7957B, 0xA7957B, 1}) i **append pojedynczego DWORD do globalnego kontenera 0xBA45E8** (grow 00475A10).

**H2 (request transport/kolejka/scheduler): REJECTED w audytowanym łańcuchu.** Zero: rejestracji wskaźnika funkcji, flag async, osobnego konsumera w tle, zapisów poza kontenerami; callback wywoływany synchronicznie (CALL EBX), wynik konsumowany natychmiast. Cały pipeline collect→sort→dedupe-check→project→global-list wykonuje się w jednym wywołaniu 006C4060.

**H3 (inna projekcja/domena): ograniczone.** Mechanizm = projekcja; domena danych (typy par) pozostaje nieznane z tych okien: 008BD720(element)→{*(e+0x18),*(e+1C)}; {0x66,A} z 007CE1E0. Kształt (statyczne listy id, rozwiązywanie id→obiekt, sort+dedupe, transform→globalna lista wartości) jest spójny z **preprocessingiem listy zależności zasobów** — charakterystyka strukturalna, nie nazwana semantyka.

**Kto naprawdę konsumuje wynik:** 006C4060 (właściciel) konsumuje przez 006C3D40 (sort), 006C2C90 (dup-find), 006C2C50 (opaque), 006C36B0→**global 0xBA45E8** (finalny sink w widocznym łańcuchu; 006C4060 czyta [0xBA45E8]/[0xBA45EC] po powrocie). Dalsza konsumpcja globala — poza zamkniętymi oknami (open edge).

## MEMBER-VIEW I TOŻSAMOŚĆ PAR

- MEMBER_VIEW_MODEL: FUN_0040b070 = return param+0x14 (decompile CONFIRMED); **MEMBER_VIEW_PROVENANCE = SAME-HISTORICAL-AGGREGATE-DECLARED, PROGRAM-IDENTITY-UNVERIFIED** (folder PE_NIGHT_AGGREGATE_20260905_160000; stlp_std; deklaracja skryptu nie weryfikuje program identity bez binarium).
- REGISTRATION_SEMANTICS: REJECTED (utrzymane z postaudytu; ciało gettera = czyste +0x14).
- **PAIR_FRAME_TO_PROJECTED: NOT_ESTABLISHED** — {0x66,A} (inline z 006C3F50) i pary elementów (z 008BD720) są **rodzeństwem w tym samym kontenerze** (nowy fakt), ale most value-flow pozostaje niezamknięty. 296445 NIE przeniesione.

## INSTANCE / TRANSFORM

- **WORLD_INSTANCE_EDGE: NOT_FOUND_IN_AUDITED_CHAIN** — w audytowanym łańcuchu żadne ciało nie tworzy instancji świata, nie robi lookup/acquire→root→attach→scene, nie dostarcza transformu. To jest gałąź preprocessingowa.
- TRANSFORM_SOURCE: UNKNOWN (bez zmian).
- PIVOT_RECORD (§9): fallback SceneFeeder **odrzucony** z powodów zapisanych w PIVOT_RECORD.json (9 callsite'ów 0085BFA0 w 6+ funkcjach — brak jednego rozstrzygalnego wejścia; budżet 3 ciała/2 warianty; slot+24h vtable-indirect nierozstrzygalny statycznie).

## WERDYKTY

- RUN_STATUS: COMPLETED_CONTRACT_SCOPE (główna nitka rozstrzygnięta; open edges zapisane; HARD STOP zgodnie z §13).
- SCIENCE_VERDICT: PASS_WITH_QUALIFICATIONS — mechanizm H1 CONFIRMED instrukcyjnie w audytowanych oknach; semantyka domeny i dalsi konsumerzy globala poza zakresem; decompile-only wyniki oznaczone.
- PROCESS_VERDICT: PARTIAL_NONCOMPLIANT — jawny incydent admission P08 (4 ciała vs 2 zarezerwowane; interpretacja niespodziewanych ciał zatrzymana; obciążenie konserwatywne); 2 niekompletne próby dziecka (DIRECT fallback autoryzowany kontraktem); okno P04 ucięte (domknięte P05); ciało 006C4060 niedomknięte (open edge); DENY 000006 operacyjny.

## BUDŻETY (actual, conservative; sum — brak nakładających się okien)

- Ciała: 21/24 (P01:3, P02:1, P03:2, P04:3, P05:1, P06:2, P07:1, P08:4, P09:2, P10:2). Unikalni function-ownerzy: ~11 + 3 ciała incydentalne (006C3D90/3DB0/3DF0) + 006C2CE0 (notatka strukturalna).
- Wiersze instrukcji: 404/4800 (sum=union; nagłówki ekstraktów wyłączone). Linie body dokumentów: 15/1000 (P02, budżet odrębny). Miejsca CALL: 26/160 (wszystkie targety osobno policzone w pakietach). Warianty: 22/24 (guard: 23 candidates — rozbieżność metod liczenia zanotowana).
- Okna VA: wiersze ekstraktów rozłączne (sum=union=404); na poziomie regionów VA P05 ([006C4050,006C4060)) pokrywa 9 B paddingu z P06 ([006C4057,006C40E0)) — bez wierszy instrukcji w przedziale wspólnym; obciążenia budżetowe konserwatywne.
- Strukturalne censuses (nawigacja, bez treści body): CALL 006C3F50 → 2 sites; CALL 006C3FE0/006C4020 → 3 sites; CALL 0085BFA0 → 9 sites.

## STANDING (bez awansu)

WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CURSOR_SOURCE_MEDIUM=UNKNOWN; CANONICAL_GATE_EFFECT=NONE. Definicja 4508→A296445→296445.nif pozostaje scoped standing.

## QC

- QC_ORIGIN: rodzic dispatchował świeżego pe-master-auditora. Próba QC_R1 (sesja ses_ead396cefffe1tkLMOBRre17Z3) zwróciła pusty wynik i NIE zapisała niczego na dysku — dla tej próby INDEPENDENT_QC=UNAVAILABLE (zgodnie z CONTRACT par. 10; bez fikcyjnego PASS).
- Retry QC_R2 (sesja ses_ead299581ffepZC0kEuOygh48e, skrócony prompt) zmaterializował i wykonał pełne QC: verdict PASS_WITH_FINDINGS (0xP0, 0xP1, 1xP2, 4xP3); 5/5 zleconych kontroli PASS; re-hash wszystkich wierszy manifestów pakietów 50/50 OK; root artifact_index 102/102 OK; 4 ADMIT spot-checki zgodne (selected_lines_sha256 przeliczone niezależnie z treści ekstraktów i źródeł); incydent P08 ujawniony w 6 miejscach, żaden load-bearing claim na niezamierzonych ciałach; budżety w granicach pod każdą interpretacją. Pliki: reviews\QC_R2\ (guard-seal manifest SHA256 53C4193F044CFC0F87547BB35A64DFF5CF8A9CBE4FD7D1DA6EE1901DFF1D162F; zweryfikowany przez rodzica: 6/6 wierszy).
- Findings QC przyjęte przez rodzica: P2-1 ACCEPTED (ta sekcja koryguje referencje QC_R1; INDEPENDENT_QC próby R1 = UNAVAILABLE zapisany jawnie); P3-2 ACCEPTED (poprawiona ścieżka evidence w STAGE_ACCEPTANCE_GATES); P3-3 ACCEPTED (budżet rozdzielony: 404 wiersze instrukcji + 15 linii dokumentowych); P3-4 ACCEPTED (sformułowanie o oknach doprecyzowane w sekcji budżetów); P3-5 ACCEPTED-as-documentation (P01_EXEC_R2\CONTRACT.json to bajtowa kopia kontraktu R1 — wadliwy plumbing archiwalnej próby retry; zamrożone archiwum próby pozostaje bez naprawy, bez wpływu na naukę).
## OPEN EDGES

1. Reszta ciała 006C4060 (za 006C4160) — dalsi konsumerzy globala 0xBA45E8.
2. Opaque: 0043A550, 0072F580, 007CE1E0, 006C2E00, 00475A10, 006C29D0, 006C3740, 006C3330, 006C24B0, 006C2C50, 00415670.
3. Semantyka domeny par (resource/dependency? — kształt mocno sugeruje, nazwa nie dowiedziona).
4. Epilog 006C36B0 (PLAUSIBLE-by-symmetry).