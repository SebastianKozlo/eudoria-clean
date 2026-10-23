# REPORT — PE_935_INSTANCE_KEY_STREAM_RESOURCE_JOIN_HIGH_TASK_OPENCODE_SAVED_R1_20261021

## 1. NOWY RZECZYWISTY PRZYROST (i jego granice)

Największy pojedynczy przyrost tej kampanii: **domknięcie jedynej otwartej przeskoki łańcucha
resource->scene na poziomie przepływu wskaźników (B3+B5)**.

- FUN_006C9700 (creator instancji) tworzy 0x10-bajtowy, NIEpolimorficzny wrapper przez ctor
  FUN_006E8F70(new, ESI, A): [wrapper+0]=ESI (obiekt klucza z lookupu FUN_00415670(&{0x66,A})),
  **[wrapper+4]=A z addref** (ADD [EAX+4],1, row 696693 + 696696), [wrapper+8]=0, [wrapper+C]=0.
- A = wynik gettera FUN_007CE1E0([manager+0x70]) — obiekt refcounted {vtable@0, refcount@+4,
  destroy vtable slot 1} (potwierdzony in-range w 006C9700 i w 007B5810).
- Zatem H-2: [manager+0x68] = [instance+4] = **A**, a join child @0050A3F6/57 to ten sam A.
- Wynik: **resource->scene pointer-flow edge: manager+0x70 -> 007CE1E0 -> A -> [wrapper+4] (addref) -> [manager+0x68] = CONFIRMED**; ostatni hop [manager+0x68] -> EDI -> join child = **STRONGLY_SUPPORTED** (H-3 pomiar EDI CONFIRMED; H-4 preservation przez 4 intervening calls: 2/4 bodies measured, ABI support, calls #1/#2 NOT_CHECKED) — zgodnie z C9/QCA.
- GRANICA (uczciwa): klasa/RTTI A = UNKNOWN. A NIE jest udowodnionym NIF/model rootem;
  MODEL_ROOT=UNKNOWN pozostaje zgodnie z prior. Semantyka A-vtable slot 17 (0x44) wołanego
  po-ctor z arg 0xa85da4 (gated CMP [00728150([wrapper+0])+4],0xb7dc) — nieotwarta.

Drugie istotne domknięcie: **join callee identity (K03+QCA)** — kontrakt wskazywał 007BF470
jako target joinu; ABI rekomputacja (QCA, niezależnie od workera) wykazała: dispatch target =
**FUN_007B5810** (slot 41 = 0xA4 = 41*4, 2-arg consumer), a 007BF470 to wewnętrzny helper
SetParent ([child+0x24]=parent @0x007bf4ac; RET 0x4). Attach-as-graph-child: refcount+1,
SetParent, refcount+1, insert do parent+0xC8 (store końcowy poza oknem => STRONGLY_SUPPORTED).

Trzecie: **strumień (K02)** — site 004B1A43->0048ECC0 to case handler dispatchera
FUN_004B18D0: kursor budowany przez pump FUN_004B1B70 z 12-bajtowego rekordu ringa
{type, data ptr, size} (ring push FUN_004B1890, stride 0xC); 0048ECC0 czyta z kursora
[4B skip][4B query key @0048ED23][1B subtype in {1,2,4}]. SOURCE_CLASS = MESSAGE_CURSOR_ASSOCIATED
(konwencja identyczna z rodziną FUN_007453D0), NIE plik. Upstream producer (poziom 3) UNKNOWN.

Czwarte: **registration lifecycle (B4+B6)** — empty-bucket FUN_00851610 (kompletna:
head-insert + bucket-fill + count++); material negative B4 rozwiązany: node+4(key)/node+8(value)
pisze wewnątrz FUN_00854260(pair*) — canon {next@+0,key@+4,value@+8} potwierdzony bajtowo.
Duplicate-key countermodel (OIJ-A02) niezłamany.

Piąte: **konsument query key (B7+B8)** — 0048E740 = parameterless lazy singleton getter
([0x00BA2040] != manager [0x00BA12E8]); korekta wcześniejszego odczytu: para {value,key}
idzie do CALL 005b47c0 — map lookup po kluczu w kontenerze singletonu + wirtualny dispatch
slot+0x8 na znalezionym obiekcie z kursorem wiadomości; miss = ciche no-op. Lookup internals OPEN.

## 2. GRAF GAŁĘZI (producent i konsument osobno; otwarte krawędzie jawne)

```
[producer/resource side]                    [consumer/scene side]
manager+0x70 (holder)                       [SF_at_CAND4_join+0x30] NiNode (EXACT parent)
  | FUN_007CE1E0 (getterA)                    ^  attach (007B5810 slot41, STRONGLY_SUP)
  v                                           |
A (refcounted, class UNKNOWN)  ===========  join child (EDI @0050A3B7)
  |                                           ^
  | addref, store [wrapper+4]                 | [manager+0x68] (H-2) -> EDI
  v                                           |
[manager+0x6C] wrapper (006C9700/006E8F70) ----+
  (wrapper+0 = ESI key obj z 00415670(&{0x66,A}))

[message stream side]                       [map/registration side]
ring entry {type,data,size} (004B1890)      registration 00856190 -> 00854D90
  | pump 004B1B70 buduje kursor               | empty bucket: 00851610 -> node 00854260(pair)
  v                                           |   {key@+4, value@+8} CONFIRMED
dispatcher 004B18D0 (38 idx / 22 entries)     | duplicate key: stary payload (OIJ-A02 stands)
  | case stub 004B1A43                        |
  v                                           |
0048ECC0: [skip4][key][subtype{1,2,4}]        key field lineage: cursor u32 -> rec+0 -> [+0x74]
  | subtype 4                                 (K01: pins 0085B20A CALL / 0085B211 STORE)
  + pair{value,key} -> 005B47C0 -> lookup
    (singleton 0xBA2040) -> vslot+0x8(cursor)   <-- SEMANTYKA OPEN
```

OTWARTE KRAWĘDZIE (bez fałszywych mostów):
1. klasa/RTTI A (MODEL_ROOT semantics) — patrz FIRST_MISSING_EDGE.json.
2. upstream producenta ringa (poziom 3: callerzy 004B1890, buffer writer, sieć vs lokalna).
3. lookup internals 0067a9e0 + semantyka dispatch slot+0x8 w 005b47c0.
4. SF_from_Bctor == SF_at_CAND4_join? (równość i rootów) — bez zmian OPEN.
5. transform konsumenci konkretnej instancji (Etap C niedostępny w budżecie).
6. bodies FUN_006C0F90/006C10B0 (preservation EDI calls #1/#2) — CHILD_TO_JOIN_IDENTITY
   pozostaje STRONGLY_SUPPORTED, nie CONFIRMED.
7. vtable DATA [NiNode+0xA4] (GA3 ma tylko sloty 0-39) — identity 007B5810 STRONGLY_SUPPORTED.
8. FUN_00704220 (scratch/list-head w 00851610) — OPEN.

## 3. STATUSY TERMINALNE (kontrakt sec.13)

RUN_STATUS = COMPLETED_WITH_DATA_BARRIERS (nauka zamknięta adaptacyjnie; wszystkie dostępne
  dopuszczone krawędzie w budżecie wykorzystane; otwarte pozycje mają dokładne klasy brakującego
  dowodu i bounded cost).
SCIENCE_VERDICT = PARTIAL_PASS_WITH_NEW_POSITIVE_EDGE (nowa potwierdzona krawędź pointer-flow
  resource->scene + 5 domknięć strukturalnych; semantyka A/transform/upstream otwarte).
PROCESS_VERDICT = PASS_WITH_RECORDED_INCIDENTS (11 prób natywnych Task; parent/model
  zweryfikowane w DB ro; 4 length-failures + 1 empty-result odzyskane z DB trybu ro bez model retry,
  znormalizowane przez mastera z pełną atrybucją; 1 incident rezerwacji (RESERVATION_EXCEED_B7);
  retroaktywna admitancja odczytów bazowych zapisana jako RETRO_ADMIT_1).
ROOT_SESSION = ses_e98f24a8effe3VPC0iUNU6UWYA (parent wszystkich 11 dzieci; DB ro potwierdza).
HIGH_CLIENT_ATTESTATION = CONFIRMED_CLIENT_LAYER (HIGH_PREFLIGHT: pe-master/pe-reconstruction/
  pe-master-auditor = nask-glm/glm-5-3-high, reasoningEffort=high, small_model=HIGH, variants={}).
REQUEST_EFFORT = NOT_OBSERVED. SERVER_EFFECTIVE_EFFORT = UNKNOWN.
TASK_ACTUAL_COUNT = 11 (K01, K02x2, K03, QCA, B3, B4, B5, B6, B7, B8).
DELIVERED = 6 normal + 5 recovered-from-DB (4 length + 1 empty-result) (atrybucja w ROLE_LEDGER + plikach *_RECOVERED).
FAILED = 0 (4 length-failures + 1 empty-result odzyskane, nie stracone). RETRIES = 1 (K02 próba 2/2).
ORPHANS = 0. NESTED_TASKS = 0.
KEY_FIELD_LINEAGE = CONFIRMED (reconciliation; store 0085B211 / CALL 0085B20A; [+0x74]=[record+0]).
STREAM_SOURCE_CLASS = MESSAGE_CURSOR_ASSOCIATED (CONFIRMED); UPSTREAM = UNKNOWN.
REGISTRATION_SUCCESS_LIFECYCLE = STRUCTURALLY_CLOSED_WITHIN_WINDOW (empty bucket: node+4/+8
  potwierdzone w 00854260(pair); AL caller-check nadal brak; lifetime poza insert OPEN).
OWNER_ATTACH_WRITER = NIE DOTYCZY TEGO RUNU (B1 attach-writer [B_lookup+C]/[R+2C] nie był
  badany — gałąź B1 nie została wybrana; frontier w matrix).
RESOURCE_TO_SCENE_INSTANCE_JOIN = CONFIRMED_POINTER_FLOW (child == A == getter([manager+0x70]));
  SEMANTICS (model root) = UNKNOWN.
TRANSFORM_SOURCE = NOT_INVESTIGATED (Etap C niedostępny; WORLD_XYZ_RECOVERED=NO).
FIRST_MISSING_EDGE = klasa/RTTI obiektu A (patrz FIRST_MISSING_EDGE.json; bounded cost: census
  vtable/RTTI w saved materiałach + bounded window FUN_007CE1E0).
ACTUAL_BUDGETS = patrz FINAL_ACCOUNTING_DRAFT.json (wszystkie capy w granicach; 21/120 body,
  ~1346 row exposures/12000, 110/600 CALL, 11/32 attempts, 822/12000 doc-lines).
UNMEASURED_METRICS = dokładny instruction-boundary union w regionach decomp (brak nowego decomp;
  notka w FINAL_ACCOUNTING_DRAFT).
LOCAL_SEAL_STATUS / PUBLICATION_STATUS / COMMIT_SHA / REPORT_GITHUB_URL = patrz
  RECEIPT_ROOT\PUBLICATION_RESULT.json (zapis po sealu; raport naukowy wskazuje receipt jako
  miejsce późniejszego statusu publikacji — kontrakt sec.12).

WORLD_XYZ_RECOVERED = NO. HISTORICAL_PLACEMENT = NOT_ESTABLISHED.
CANONICAL_GATE_EFFECT = NONE (do osobnej kwalifikacji).

## 4. KOREKTY OIJ-A01..A10 (addytywne, zgodnie z kontraktem sec.3)
Zapisane w CLAIMS.json C1-C12 i w addytywnym notice do starego raportu (publikacja):
A01/A02 — utrzymane (identity join B_ctor->B_lookup nadal otwarty; duplicate-key niezłamany).
A03 — utrzymane (gettery istnieją; K01 tylko reconciliation, zero "nowego odkrycia").
A05/A06/A07/A08/A09/A10 — utrzymane (A09 empty-bucket domknięty strukturalnie przez B4+B6;
  rozliczenia poprzednika NIE kopiowane jako baseline).
Fałszywy hash finding QF2 — to był błąd raportu auditora poprzednika; nie powielony tutaj.

## 5. Ograniczenia metody (pełna szczerość)
- 4 z 11 prób zakończyło się reason=length (K02#2, QCA, B3, B4) + 1 empty-result (K02#1); odzysk z DB (reasoning parts) jest pełny dla
  pytanych zadań, ale reprezentuje stan analizy w chwili ucięcia (nagrania reasoning są
  literalnie zachowane w *_DB_RECOVERY_reasoning.md).
- QCA był odzyskany tą samą drogą; jego dwa planowane mechaniczne kontrsprawdzenia (hash H5,
  GA3 re-query) wykonał master jako AUDITOR_COUNTERCHECK (odrębnie oznaczone).
- Wszystkie agenty tej samej rodziny modelu (GLM HIGH) — niezależność modelowa nie istnieje;
  niezależność uzyskano przez rekomputację bajtów (QCA) i weryfikację rows przez mastera.

