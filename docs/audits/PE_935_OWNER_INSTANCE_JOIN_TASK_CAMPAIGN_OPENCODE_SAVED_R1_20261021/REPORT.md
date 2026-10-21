# PE_935_OWNER_INSTANCE_JOIN_TASK_CAMPAIGN_OPENCODE_SAVED_R1_20261021 — REPORT

RUN_STATUS = COMPLETED (nauka bounded; seal lokalny; publikacja sanitizowana)
SCIENCE_VERDICT = STATIC BRIDGE ESTABLISHED; INSTANCE IDENTITY RUNTIME_CONDITIONAL; PLACEMENT NOT ESTABLISHED
CANONICAL_GATE_EFFECT = NONE

## 1. Co NOWEGO rzeczywiscie ustalono

Najwazniejszy wynik kampanii: **pelny statyczny most wartosci miedzy konstruowanym ownerem a czytnikiem transformu**, szczebel po szczeblu, wylacznie na zapisanych dowodach (H5 listing + saved decomp), z def-use na kazdej krawedzi:

```
B_ctor (alokacja 0x128 B @004C47C1, jedyny literalny CALL 00528E50 w H5)
  -> PUSH EAX(B_ctor|NULL) -> 00856190 = BOOL Register(this, obj)
       receiver = wynik 004154F0 (lazy-init singleton, slot globalny 0xBA12E8, ctor 008550C0, footprint 0x8C)
       klucz = 00414130(obj)          [cialo 00414130 POZA saved corpus — OPAQUE]
       insert 00854d90 (SGI-style hashtable @registry+0x10; n=(end-begin)/4-1; selektor=key MOD n)
         -> wezel {next@+0x0, key@+0x4, value@+0x8}
         -> 00854260: node+0x8 = value LITERALNIE (surowa kopia dword) => node.value = B_ctor
       lock/guard @registry+0x44 (00413440/00413450)
lookup-side (deserializacja, funkcja 0048ecc0):
  klucz = dword zdekodowany z bufora bajtow strumienia (def EDI @0048ed23)
  -> 0085B840 (wrapper) -> 008544D0 (lookup: find 00971780 na registry+0x10 pod +0x44)
       find 00971780: IDENTYCZNA arytmetyka jak insert (countercheck mastera: MOD, *4, sentinel, key@+0x4)
     -> EAX = M32[node+0x8]  => wartosc zarejestrowana => (warunkowo) B_ctor
  -> *slot [S+0x74] -> 004123D0 #1/#2 (oba ten sam slot; brak mutacji miedzy odczytami)
  -> ECX = EAX#2 = B_lookup -> 00527AB0 (reader, cialo kompletne)
       R = [B_lookup+0xC] -> 0085bfa0 (provider wrapper, cialo kompletne):
            P=[R+0x2C]; VT=[P]; F=[VT+0x24]; CALL F -> retval = wskaznik na 12-float blob
            bufor 52B = 13 dwords (9 REP + 3 stores + 1.0f@+0x30)
       -> REP MOVSD: 13 dwords do [R+0x30..R+0x63]
```

Ponadto:
- Kontrmodel J01 (klucz ignorowany / node+0x8=next) SFALSYFIKOWANY (J10 + QF1).
- Czytnik 00527AB0: zapisy [EBX+0xE0]=0, [EBX+0xE4]=0 (warunkowo +0xE8 na fall-through) — wzorzec reset/commit akumulatorow.
- 004123D0 = trywialny getter *wrapper (J07); konteksty T01/T02 to inny caller niz sugerowal prior premise.
- Piec LEA: 4x STACK_BASED, 1x OBJECT_FIELD (count/buffer writer bez joinu) — scoped negative dla attach R_load.
- Klucz lookupu pochodzi ze strumienia bajtow (deserializacja), NIE z pola B_ctor — obie strony klucza sa roznych zrodel; zgodnosc wartosci = warunek runtime.
- Kopia 13 dwords do [R+0x30..0x63] ma DOKLADNIE wzorzec docelowy [X+0x30,X+0x64) z prior kanonu trzynastoslowego rekordu — ale zrodlo jest KOMPUTOWANE przez providera (nie [S+0x60,S+0x94)) i to inny callsite niz 0085A429; nie scalono (CL16 UNPROVEN).

## 2. Czego nadal brakuje

- KEY_MATCH: rownosc klucza rejestracji (00414130) i id ze strumienia => B_ctor==B_lookup pozostaje RUNTIME_CONDITIONAL (CL13).
- Receiver identity instance-level (warunki C1: tail 004154F0 poza corpus; C2: brak resetu slotu; C3: fill bucketow w CRT thunkach).
- F_slot24 implementacje (zrodlo danych transformu) — vtable poza zasiegiem static.
- MODEL_RESOURCE -> konkretna instancja: brak krawedzi w tej kampanii.
- WORLD_INSTANCE / historyczne umiejscowienie: brak dowodu.

## 3. Graf krawedzi

Potwierdzone (static, def-use): B_ctor->Register->node{key,value}->lookup->B_lookup->R=[B+0xC]->provider->[R+0x30..0x63].
Warunkowe: node.value==B_lookup (KEY_MATCH, runtime); receiver instance (C1-C3).
Otwarte: provider implementacja; MODEL_RESOURCE; WORLD_INSTANCE; X==R_load (poszlaka wzorca, bez dowodu).

## 4. Proces (skrot)

22 natywne delegacje Task (18 pe-reconstruction, 4 pe-master-auditor), wszystkie parent_id=sesja mastera (census DB: 22/22, zero ukrytych), model dzieci nask-glm/glm-5-3 (medium, variant=default) potwierdzony w DB per sesja. 1 nieudana proba (Q01 finish=length) z naprawczym retry. Swieze QC: Q01R (stage A), QF1+QF2 (QFINAL, 2 obowiazki). Cap-y dotrzymane (rows 1948/10000, bodies ~48/96, calls ~238/400, attempts 22/24). Budzet admission A001..A019 append-only; 4 incydenty udokumentowane (w tym APPEND_LATE A001 i finish=length Q01).

## 5. FIRST_MISSING_EDGE

KEY_MATCH (patrz FIRST_MISSING_EDGE.json): najtanszy test statyczny = eksport 00414100..00414200 + tail 004154F0; test runtime = capture zgodnosci pointerow (zakazany w kampanii). Alternatywy: implementacje F_slot24; sciezka MODEL_RESOURCE.

## 6. Standing

WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CANONICAL_GATE_EFFECT=NONE; zewnetrzny postaudyt PENDING.
