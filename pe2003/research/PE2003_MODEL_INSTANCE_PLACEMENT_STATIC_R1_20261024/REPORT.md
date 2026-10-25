# REPORT — PE2003_MODEL_INSTANCE_PLACEMENT_STATIC_R1_20261024
Run date: 2026-10-24/25. Controller: PE-MASTER (ta sesja natywna; writer runu od fali 1). Amendment YOLO 8h przyjęty: T0=2026-10-24T23:10:45Z, research_end=06:10:45Z, campaign_end=07:10:45Z; badania zamknięte wcześnie @03:30:57Z (branches_exhausted, pełne uzasadnienie w RECEIPT_ROOT/EARLY_CLOSE_JUSTIFICATION.md). 100% pliki/statyczny kod 2003; zero klienta/Fridy/free-cam/preview/renderera.

## WERDYKT GŁÓWNY
PE2003_WORLD_XYZ_RECOVERED = **NO**. PE2003_HISTORICAL_PLACEMENT = **NOT_ESTABLISHED**. CANONICAL_GATE_EFFECT = NONE; ADVISORY_PENDING_EXTERNAL_POSTAUDIT.
**Autentyczne położenia świata 296445.nif i 218757.nif NIE istnieją w lokalnych danych instalacji 2003** — negatyw z pełnymi zakresami (poniżej), nie globalny dowód niemożliwości (źródło = tor serwerowy, statycznie niedostępny). Mechanizm instancjonowania i transformacji domknięty bajtowo do granic statyki.

## NOWA NAUKA (łańcuch, obie definicje 4508/4057)
1. **Transport definicji = UDP** (nie plik): pump FUN_005bfe90 (socket AF_INET/SOCK_DGRAM/IPPROTO_UDP @0x5BFEE9; jedyny recvfrom @0x5BF918; datagram <=1472B {8B crypto, ack, seq, flag 0x10=DATA/0x08=ACK}; XOR-LCG crypto). Ścieżka plikowa REFUTED (fopen tylko config/terrain/ark-cache). Korekta kanonu: "message type 0x11" nie istnieje (0x11 = min długość datagramu). [V3/V4/V13; QROLL1 PASS; kontr-bajty QROLL1]
2. **Rejestr definicji data-driven**: loader FUN_005977b0 (rekordy 0x1C {id, payload} z deserializowanego message; writer +0x2C = FUN_005bb321) -> rejestr RB-tree @GCE+0x10064 -> wykonanie FUN_00454300 -> interpreter FUN_00454360. [V2/V4/V5; QROLL1 Q1 PASS]
3. **HOSTCALL = case-id inline; receiver wybiera dispatcher**: pump-site 0x458182-0x458192 ([ECX+0x14]=VM SP; CALL [EDX+0xC]); engine singleton -> 0x441DF0 (definition lookup, nasze operandy 4652/4653); GCE -> dispatch B 0x485260 (379 case -> 378 metod, default tail-jmp do 0x441DF0). [V1/V6/V11; kontr-bajty QROLL3/QSCI_VM PASS]
4. **Konstrukcja modeli (nasze definicje) — domknięta do granicy korpusu**: bytecode 4508/4057: wyłącznie HOSTCALL[0] (lookup 4652/4653 = biblioteka ENVIRONMENT/property-selectors; V7: 4652=strings, 4653=PDAT resource table 6 rekordów) + CALL_abs[0] binder-patched; pętla per-part: 4508 = 26 części mesh (Mesh_B_Eu_Slum_Building_b047_*, ids 126743..126779), 4057 = 18 części; ATTACH -> ext 30298 (def 1796; forwarder: part_id x3 + [SP+56] handle -> ext 33521 klasy 2202 — **bytecode klasy 2202 NIE istnieje w lokalnym korpusie**). Bijekcja fixupów EXTN EXACT (4508: 10 slotow==10 rekordow; 4057: 8==8; QROLL3 C4 PASS). **ZERO stałych pozycyjnych** w całej ścieżce (7134 dwords, 0 f32-triples; negatyw niezależnie potwierdzony przez QROLL3). [V16/V17/V18/V12]
5. **Instancja scenowa**: SceneInstancePair 0x10 {id+8, holder+0xC} z holderem 0x10 (vt 0x5E799C, root-clone z FUN_00521b60 — clone STRUKTURALNY, wartości default; T7 obalł inferencję T3). ScriptInsert (case 15497, dispatch B) = batch ID-only. Add do sceny = slot-append wyłącznie tożsamościowy (transform przy add nigdy nie ustawiany). [L2/T3/T5/V9/V10]
6. **Writery transformów (finalny zbiór po korektach)**: {default reset FUN_004ffbe0; default-init ctors; GCE case 0x10a (SetRelativeSubModelPosition: x,y,z*100 z bytecode VM — sub-model, NIE w naszych definicjach) + 0xdc (orientation); FUN_005030c0 (root writer DLA ENCJI z flagą record[6]: struct 0x48 — tryplet +0x14 = TRANSLACJA (world/100), +0x20 = EULERY w radianach (macierz 3x3 transposed do node+0x2C; NA DRUCIE BRAK KWATERIONU), +0x2C = internal position state; encja klasy 0x118, pending 5s)}. Wartości z sieci, nie z plików lokalnych. [T1/T2/T4/T7/V10/V12/V14/V19; QROLL2 R1 PASS byte-exact; QSCI_INSTANCE PASS]
7. **Lifecycle odroczony**: executor FUN_00454300 ma dokładnie 2 callsite'y — natychmiastowy (loader) i w drainerze FUN_0044a910 (kolejka GCE+0x1001C; drain przez state-machine tick; odroczenie = wyłącznie timing). [V20]
8. **Volume .bvi (296446/218758)**: getter/konsument NIE istnieje w skanowanym zasięgu (region kandydacki odrzucony z dowodem — to funkcje cache-GC); hipoteza dead-registration wymaga runtime. [L3]

## NEGA TYWY (z pełnymi zakresami — nie globalne)
- **Korpus 1936 definicji**: ZERO odwołań do 4508/4057/296445/296446/218757/218758 (poza self); 4508: 1 self + 13 koincydencji nie-semantycznych (EXTN offsets/JMP disp). Niezależny pełny rescan QROLL3: EXACT zgodny. [V15/QROLL3 C2]
- **Cały obraz EXE (writerzy transform)**: census field-level + ślepe plamy LEA/rep/memcpy zamknięte — żaden writer nie dostarcza wartości pozycji dla statyków z danych lokalnych. [T4/T7 + supersedence V10]
- **Instalacja 2003**: 704 pliki — WSZYSTKIE klasy pokryte (D3); data.ini=version metadata; FileList.txt=installer manifest; zero niezbadanej klasy z potencjałem placementu.
- **TDF 50.bnt**: 51921/51921 kanał terrain-only (75/75 reszt = height+material chunk chains, nowy typ 3 = gradient weights; zero struktur id/transform; negatyw na pełnej klasie). [D2/D2b/D4]
- **2234.obj**: 2607/2607 rekordów = tabela recept craftingu (526 id w 284M-382M); zero naszych literałów; CLOSED_NEGATIVE_UNRELATED. [D1]
- **Definicje 4508/4057 bytecode (CODE+EXTN ścieżka)**: zero f32-triples / zero koderów dispatch B — self-positioning FALSYFIKOWANE statycznie z pełnym denominatorem. [V12/V17/V18; QROLL3 C1/C3/C4]

## KOPIA STAREGO DOWODU (reprodukcja) vs NOWE
Reprodukowano (bez zmiany statusów): piny/hashe obu NIF, DLOB decode format (V7-grammar), bazowe getter-y (4508@+F8/+A4, 4057@+68/+14). Nowe: cała fala V2-V20, L2-L3, T1-T12, D1-D4 (wykaz wyżej). Nie odtwarzano: 1936 decode (zakaz), 51921 census (zakaz — użyto pinned), rendererów (zakaz).

## NIEZWERYFIKOWANE / OPEN (dokładne brakujące operandy — RESEARCH_BACKLOG.json)
bytecode klas 2202/768/382 (poza korpusem lokalnym); binder patch values (runtime); receiver runtime identity (GCE vs binder); targets *(owner+0x6C/+0x70); [SP+56] handle; występowanie record[6] dla definicji budynków (dane serwera); TDF height/RLE depth (poza wartością placementową). **Historically: położenia statyków = tor serwerowy (message struct 0x48 potwierdzony dla encji dynamicznych; dla budynków — statycznie nierozstrzygalne w 2003 install).**

## PROCES
51 dispatchy / 50 delivered / 1 infra-fail (D2B a1 spawn UNKNOWN; retry a2 delivered). Modele/role: nask-glm/glm-5-3 default/medium (wire effort UNKNOWN); PE-MASTER controller; pe-reconstruction executor; pe-master-auditor 6x QC (proceduralne — brak niezależności modelowej). QC: QROLL1 (QC_PARTIAL -> T8 fixed), QROLL2 (PASS_WITH_NOTES -> T10 fixed), QROLL3 (PASS_WITH_NOTES -> T11 fixed), QSCI_VM (QC_PARTIAL -> T12 fixed, recheck PASS), QSCI_INSTANCE (PASS_WITH_CORRECTION -> T12), QACCOUNT (QC_PARTIAL: root-owned closure items — wykonane w sealu). Korekty kanonu w-runie: 10 (SELF_REVIEW_1 §3) + 3 path-drift layout + 2 admission incidents — wszystkie addytywne i ujawnione. Budżety amendmentu: 51/240 prób; rodziny daleko pod capami; rezerwa 189>=16; rolling QC 6<=12. Bodies/LOC: per-job raportowane w handoffach; agregaty UNMEASURED poza sumami jawnymi.

## SEAL
SCIENCE_STOP @ 2026-10-25T04:xxZ (kind marker w control/); MANIFEST_SHA256.csv LAST, self-excluded, pełna bijekcja SIZE/SHA256 + read-only rehash. Po sealu: publikacja sanitizowana (receipt w RECEIPT_ROOT/PUBLICATION_RESULT.json; commit/link poniżej po wykonaniu).

## CANON / NEXT
WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; LOCAL_SOURCE_EXHAUSTED=NO (statycznie wyczerpane gałęzie; kanał serwerowy runtime otwarty — drugi nurt człowieka); CANONICAL_GATE_EFFECT=NONE; ADVISORY_PENDING_EXTERNAL_POSTAUDIT. HARD STOP po tej kampanii.
