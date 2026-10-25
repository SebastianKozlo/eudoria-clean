# OBJECT_AND_ID_MAP — PE2003_ISO_MODEL_BINDING_VALUE_ORIGIN_STATIC_R5_20261025

RUN_ID: PE2003_ISO_MODEL_BINDING_VALUE_ORIGIN_STATIC_R5_20261025 | BUILD: ISO2003NOV_PE_5_1_0_0 | DATE: 2026-10-25
PROVENANCE: RUN_CONTROL (dictionary live), jobs/A01,D01,J01-J05 RESULT, QC1/QC2, MODEL_BINDING_CERTIFICATE_J03_CORRECTED.json. Companion strict ledger: ROLE_LEDGER.json.

## 1. Symbole i zmierzone role

**E (entity 0x100B)** — produkt factory 0x4578E0: alloc(0x100) @4ADE7C, ctor 0x46E870(ecx=alloc, stack=this−8=M) → [E]=0x65C060, [E+0x48]=0x65C05C, [E+0xF8]=0 (cache P), [E+0xFC]=M. Fabryka forwarduje a1..a6 verbatim do writera 0x46E990 przez [E_vt+0x1c] @0x457951 (target 0x65C07C=0x46E990 z bajtów). Lifetime: heap; teardown M w 457210/457540 (dtor re-writes base vtables); brak free(M) — T0/immortality nie orzekane.

**I (entity+0x40)** — zapisywane przez a1 (0x555191 `89 46 40`); czytane fresh w lazy-create (getter 0x553220 `mov eax,[ecx+0x40]; ret`); pushowane razem z literalem 0 (osobne sloty argumentów — I i K NIE sklejone). Rola ID-like; nie assetID/templateIndex bez dalszego dowodu.

**K (indeks rekordu)** — w zmierzonym lazy-create: LITERAL 0 (push 0 @0x46E9D0 przed 0x457980). Metoda 0x46ECA0 (re-bind) przyjmuje selektor K z wiadomości (J01 S9) → K≠0 istnieje. Lazy-create K=0 dotyczy pokazanych 16 sites, nie wszystkich metod.

**N (raw ROOT z open-by-name)** — retval 0x423280 (slot+0x3C klasy 0x65B3BC, jedyny ref dword 0x65B3F8): bezpośredni wskaźnik refcounted ROOT (+4=refcount); cache-test [nested_vt+4]([this+8],name); chybienie → stream 0x43C490(name,0,0x2800) (fopen 'rb') → load [nested_vt+8](this+8,&stream,arg2) → retval = ROOT; stream dtor 0x43C510. NIE wskazany jako NiNode bez pointer-level dowodu; w zmierzonym zakresie N nigdy nie dociera do rekordu/SFO jako wspólny pointer.

**T (rekord 0x5C = SUB[K])** — ctor-chain 477FC0(→473430 flag=0)/45D5F0/45DE90; pola: +0x30 ctx, +0x34 SUB(=MGR), +0x38 zasób (provider branch MARTWY in-image → NULL), +0x48/+0x58 sub-obiekty (48A5E0/489CD0, rejestracja 489FD0), lazy default visual 0x4782E0 (placeholder, NIE open-by-name). T0 = rekord odczytany z SUB[0] w konkretnym czasie; niezmienność/lifetime przez cały run niewykazana.

**P (proxy/SFO 0x7C)** — produkt 0x473E90 (push 0x7C byte-proven); P+4=I, P+0x78=T; cache [W+0xF8] (W=E-layout obiekt z 54FD40 lookupu mgr=[0x6C6A44]); E+0xF8=P (writer). Receiver instancjotwórczych 527A00/527BC0 w handlerze 0x47B8A0 = P sam (CORR1/QC2-F01; wcześniejszy label [P+0x10] REJECTED_AS_WORDED). [SFO+0x10] = slot wizualny SFO (produkt 5257C0; J01) — NIE dotknięty na ścieżce tworzenia typu-7.

**R (rzeczywisty scene node/model root)** — tożsamość względem N/T/P pozostaje OTWARTA (UNVERIFIED). Kandydaci surface: post-52A130 flow 0x526CFA+, registry consumers, sekcje poza section1.

**M (manager 0x1D0B)** — ctor 0x456FF0 (PA/R4 pin "4570C0" = mid-body window, D01 correction), global cell 0x6C4C58 (1 write @0x4571CC + dokładnie 3 readery 0x5DDxxx); [M+0x8C]=O (owner, mgr-ctor arg1); interfejs M+0x08 → vt 0x65BE9C (1 slot) = factory 0x4578E0; M+0x80 → live vt 0x65BE44 (3 sloty; D02 korekta base-store vs final-store); M+0x94 holder94 (vt 0x65C050, slot1=468010 switch). Obiekt 462D60 = float-struct (arg2→[rec+0x30]) — wykluczony jako SUB.

## 2. Graf krawędzi kluczowych (zmierzonych, byte-proven)

```
[unreconstructed callsite: 6 pushes, this=M+0x08]  -- BARRIER (C12)
  -> 0x4578E0 factory -> 0x46E990 writer -> 51D730 -> 5531F0 -> 555170 -> 555270
     -> a1..a6 stores (E+0x40/E+0x44/E+0x54/vt+4/vt+8/vt+0x10)
     -> lazy-create: 553220(I) + push 0 -> 457980(M,0,I) -> 451210(O,0) -> 45DE20 -> 473E90 -> [E+0xF8]=P
     -> scratch 46EA02/46EA55 (slot [E+0x18], def=[E+4]) -> 0x46F0A0 (scale [0x65B648])
name side: msg handler 0x47B8A0 -> 4579E0 -> 54FD40([0x6C6A44]) -> W -> 46EC60 -> P
     -> 527A00/527BC0(P, msg-string, flag) -> [per-name obj+0xBC] type-7 instance 0x65B3BC (retval DISCARDED)
     0x4859A0 -> 498B80(inner=[svc_result+0x38], [0x6C4F20] key 0x19A) -> [[inner]vt+0x3C] (potencjalny 423280; retval DISCARDED; inner class=BARRIER)
record side: 47CFB0 -> 45DE90/45D5F0 -> 477FC0(flag=0) -> 473430 -> [rec+0x38]=NULL (provider branch dead)
visual side: 46F1A0 -> 52A130(msg-key) -> 564AB0 -> 564890 -> [entry+8] -> 5257C0 -> [SFO+0x10]
```

## 3. Zakazy merge (KONTRAZ/RUN_CONTROL)

N=T, I=K, T=R, P=world-root — oddzielne pytania, wszystkie NIEROZSTRZYGNIĘTE. Brak sklejania przez podobny offset/vtable/nazwę. Opaque CALL (0x457980/0x473E90 wnętrza poza pinami) = bariera, nie zero. Float-looking wartości nie są world-coordinates bez consumera/ramy (brak etykiet osi w A01 upheld).
