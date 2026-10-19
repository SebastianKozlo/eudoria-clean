# QC_R1 — INTERNAL_QC pakietów P01–P04 (run PE_935_PAIR_REDUCER_CONSUMER_SAVED_R2_20261019)

RUN_ID_QC = PE_935_PAIR_REDUCER_CONSUMER_SAVED_R2_QC_R1_20261019
AUDITOWANY_RUN = PE_935_PAIR_REDUCER_CONSUMER_SAVED_R2_20261019
TRYB = INTERNAL_QC (niezależny QC wewnętrzny; nie zewnętrzny postaudyt; nie MASTER_ACCEPTED; run pozostaje otwarty, seal należy do rodzica)
REVIEWER = świeży pe-master-auditor (niezależny od executorów; P03/P04 autorstwa rodzica — audytowane ze wzmocnioną rygorystycznością)
KONTRAKT = D:\Eudoria_Reconstruction\99_Audits\PE_935_PAIR_REDUCER_CONSUMER_AUTHORING_R1_20261019\CONTRACT.md (sha256 7494B7146106255B4C710EE0EBF1A87EAECC2C201ADA5A3739521AC86A9FCDA0 — zweryfikowany, zgodny z PREFLIGHT)

## 0. Werdykty per pakiet

| Pakiet | Autor | Werdykt QC | Findings |
|---|---|---|---|
| P01_ADAPTER (006C29D0) | pe-reconstruction | **PASS** | 0 w pakiecie (1×P3 run-root, F-RUN-03) |
| P02_CONSUMER (006C4060) | pe-reconstruction | **PASS_WITH_FINDINGS** | 2×P3 |
| P03_PUMP (0x00823C10) | DIRECT_ANALYST_FALLBACK_BY_PE_MASTER | **PASS_WITH_FINDINGS** | 2×P2, 4×P3 (+P2/P3 run-level) |
| P04_FRONTIER (0085BFA0) | DIRECT_ANALYST_FALLBACK_BY_PE_MASTER | **PASS_WITH_FINDINGS** | 2×P2, 2×P3 (+P2/P3 run-level) |

**QC_VERDICT (całość): QC_PARTIAL** — wszystkie pakiety naukowo trzymają się (żaden finding nie zmienia werdyktu naukowego pakietu; wszystkie claimy load-bearing potwierdzone niezależnie), ale P03/P04 zawierają defekty dokumentacji/statusów (2+2×P2) oraz run-level defekt chronologii (F-RUN-01), które wymagają corrigendum przed sealem. Żadnych P1.

## 1. Obowiązkowe testy niezależne (wyniki)

### 1.1 Re-hash i bijekcja (PASS)
- 4 ekstrakty: sha256 zgodne z przydziałem rodzica, admission events, kontraktami zadań i artifact_index:
  P01_EXTRACT=156C26F6…28AB ✓, P02_EXTRACT=CBFAB828…23AE5 ✓, P03_EXTRACT=675EF8D2…4423F ✓, P04_EXTRACT=5C8F06B2…DA7A23 ✓.
- Source pin GHIDRA_H5_VTABLE2.txt: sha256 642CC29A…D8DB, 50780146 B — zgodny ze wszystkimi 4 admission events ✓ (hash własny QC; zawartość źródła nie była czytana semantycznie).
- CONTRACT.md: 7494B714…FCDA0 = wartość z PREFLIGHT ✓.
- Guard chain: 5/5 zdarzeń previous_sha256 = faktyczny sha256 pliku poprzednika; zegary UTC↔monotonic spójne co do 0.01 s ✓.
- artifact_index: P01 (9 plików) i P02 (9 plików) — wszystkie zadeklarowane sha256 = faktyczne ✓ (wiersze „self-excluded" nie są hash-claimem). P03/P04 indexy nie mają kolumny sha256 (format minimalny; dopuszczalny, ale słabszy — F-RUN-04); pełne wyliczone hashe wszystkich plików P03/P04 w RECHECKS.json.
- **Bijekcja ekstrakt↔źródło: 449/449 wierszy** (P01 67, P02 62, P03 185, P04 135) — każdy wiersz ekstraktu „N|treść" jest werbatim (byte-w-linii) tożsamy z linią N (1-based) przypiętego źródła; numery wierszy ścisłe +1, bez luk ✓. Ekstrakty są więc wiernym, niczym niezmienionym wyborem z przypiętego źródła.
- Seam P02↔prior: WINDOW_006C40E0 ostatni wiersz 650349|006c415e (C7 44 24 50 imm32, 8 B) → P02 pierwszy 650350|006c4166 — delta dokładnie 8 ✓; W1→W2: 006c40df CALL rel32 (5 B) → 006c40e4 ✓; ciągłość wierszy 650268→650411 ✓; 82 wierszy prior ma delta 1–6 (bez anomalii) ✓. claim B01 (144 wiersze/143 delta) potwierdzony (z zastrzeżeniem dwóch jawnych przerw paddingowych po RET, które B02 osobno dokumentuje — to nie jest niezgodność).

### 1.2 Pełny bilans ESP — pump 0x00823C10 (policzony samodzielnie z surowych wierszy; PASS)
Prolog: PUSH −1 → ESP0−4; PUSH handler 0xA236F8 → −8; PUSH FS → −0xC; SUB 0x1C → −0x28; PUSH EBX/EBP/ESI/EDI → −0x38; PUSH cookie → **−0x3C** (baza). Sloty argumentów z bazy: arg1=[ESP+0x40]=ESP0+4 ✓, arg2=[ESP+0x44] ✓, arg3=[ESP+0x48] ✓, arg4=[ESP+0x4C] ✓. EBP=arg1=pair_ptr @00823C3D ✓.
Epilog: FS restore z [ESP+0x30]=ESP0−0xC @00823E44/E48 ✓; POP ECX(cookie)/EDI/ESI/EBP/EBX (5×4=0x14) → ESP0−0x28; ADD ESP,0x28 (lokale 0x1C + trio SEH 0xC) → ESP0; **RET 0x10** → ESP0+0x14 (adres powrotu + 4 argumenty) ✓. 0x14+0x28=0x3C = dokładne lustro prologu; obustronna zgodność z P01 (adapter: LEA [ESP+0x10] @006C2A65 koheruje tylko przy wycofaniu 16 B przez pump) ✓✓.
Dodatkowo odtworzone niezależnie: adapter 006C29D0 (baza E0−0x4C; POP×3+ADD 0x40; RET 0x10 → E0+0x14; caller bez ADD ESP — domknięcie S−0xC) ✓; consumer 006C4060 (B=E1−0x44; POP×5+ADD 0x30; RET → E1+4) ✓; 0085BFA0 (SUB 0xA0+PUSH×2 → 0xA8; POP×2+ADD 0xA0; RET 0x4 → ESP0+8 — wymaga callee-clean wirtualnego (RET 4) i 0096CB20 (RET 0x24): patrz F-P04-02) ; 0085C0F0 i 0085C130 (full trace z lokalnymi buforami; FLD/FSTP na trzech translacjach @0085C140/153/15E koheruje tylko przy głębokości z PUSH ECX @0085C14B) ✓.
Cenzus offsetów [ESP+x] pumpa: wszystkie odwołania rozliczone na podanych głębokościach; **[ESP+0x4C] nie występuje nigdzie** → arg4 dead-in-window ✓ (K12 potwierdzone).

### 1.3 Test low-byte vs DWORD (PASS)
- Adapter @006C2A34: MOV CL,[ESI+0xC] — odczyt TYLKO bajtu 0 ctx[5] (byte ptr); @006C2A3F: MOV [ESP+0x58],CL — zapis TYLKO bajtu 0 własnego slotu arg3; bajty 1–3 slotu zachowują oryginalne bity (S+0x10) → pump arg4 = dokładnie (S+0x10)&~0xFF | (ctx[5]&0xFF) — formula P01 A13/A07 ✓.
- Kontekstowy @006C4125: MOV byte [ESP+0x4C],0x1 (surowy wiersz prior potwierdzony) — zapis bajtowy; @006C412A MOV EBP,[ESP+0x4C] wczytuje CAŁE słowo (górne 24 bity nieustalone) i @006C4133 zapisuje je jako ctx[5] — C3 potwierdzone na poziomie surowym ✓.
- Łańcuch neutralizacji: adapter konsumuje wyłącznie bajt 0 ctx[5] (A13) → pump w ogóle nie czyta arg4 (K12) → nieustalone górne bity NIE wpływają na żadną admitowaną kalkulację ✓. Pakiety utrzymują nieustalone bity poprawnie; P03 zamyka też otwartą w P01 (E9) nieprzejrzystość „co pump robi z tagowanym slotem": w oknie — nic (nie czyta).

### 1.4 Exact pointer holder (PASS)
Surowe wiersze prior P10: @006C36C5 LEA EAX,[ESP+0x20] (=S+0x10) → PUSH EAX (arg3=holder) ✓; @006C36DD MOV [ESP+0x2C],EDI wpisuje aktualny wskaźnik pary do slotu [S+0x10] ✓; @006C36D9 LEA ECX,[ESP+0x38]=S+0x1C=&ctx[2] ✓ (C4). W adapterze: @006C2A37 MOV EDX,[ESP+0x58]=arg3; @006C2A3B MOV EAX,[EDX] — **dokładnie jeden deref poziomu 1** → pair_ptr=M32[S+0x10] ✓; bez redefinicji EAX do PUSH @006C2A52 → pump arg1 ✓. Poziomy śledzone poprawnie (holder→slot→para = 2 poziomy do obiektu); para NIE jest czytana polami w adapterze ✓. Kontynuacja w pumpie: EBP=arg1=pair_ptr; [EBP]=pair[0] @00823C41, [EBP+4]=pair[1] @00823D16 — oba DWORD pary czytane w pumpie ✓ (claim rodzica potwierdzony).

### 1.5 Rozliczenie rezerwacji+debits (PASS, bez refundacji)
Guard events: START(limity 32/6000/200/32/1500) + 4×ADMIT. Sumy z eventów = sumy z pakietów:
bodies 3+4+3+4 = **14/32** ✓; rows 67+62+185+135 = **449/6000** ✓; calls 9+3+20+7 = **39/200** ✓; candidates 3+3+3+3 = **12/32** ✓; document lines 0/1500 ✓.
Obciążenia bez refundacji: P01 3/3 (1 unikalny owner), P02 4/4 (3 widoczne ciała), P03 3/3 (1 owner), P04 4/4 (4 ciała) — pełne rezerwacje obciążone, zero refund, zero INCIDENTALS (katalog pusty) ✓. Suma=unia (bez podwójnego liczenia; wiersze prior konsultowane read-only obciążają swoje runy) ✓. Widoczne ciała ≤ zarezerwowane wszędzie → brak PARTIAL_NONCOMPLIANT ✓. Pozycja PIVOT_RECORD przed pivotem (10/314/32/9) = suma P01–P03 ✓.

### 1.6 Chronologia i zakazane operacje
Guard chain spójny (1.1) ✓; P01 RUN_STARTED 14:29:30→14:34:02Z po ADMIT 000002 (14:21:23Z) ✓; P02 14:45:53Z po ADMIT 000003 (14:38:58Z) ✓. **P03/P04 RUN_STARTED podają „09:55:00Z(approx)"/„10:20:00Z(approx)" — sprzeczne z ADMIT 000004 (15:00:59Z) / 000005 (15:22:14Z)** (analiza nie może wyprzedzać admission w żadnej strefie czasowej) → F-RUN-01 (P2).
Census śladów: w plikach runu brak jakichkolwiek śladów operacji na oryginale/runtime/Ghidra (brak hashy plików gry, brak runtime capture, źródłem wszystkich ekstraktów jest wyłącznie przypięty listing z katalogu docs/audits — projektowy zapis, nie plik gry); forbidden-guard oświadczenia obecne w RUN_STARTED pakietów ✓. QC nie może udowodnić negatywu absolutnie, ale nie istnieje żaden pozytywny ślad przeczący.

## 2. Findings (z wagami)

### F-P03-01 (P2) — P03 REPORT §3 „PATH-NULL-B": błędny opis przepływu sterowania po zerowym wyniku fast-path
- **Źródło**: P03_PUMP\REPORT.md §3 (PATH-NULL-B); ekstrakt: @00823c91 CMP byte [EDI+0x38],BL; @00823c94 **JZ 0x00823cb5**; @00823ca2 **JZ 0x00823cb5**; @00823cae XOR EAX,EAX; 00823cb5 = inicjalizacja PĘTLI.
- **Skutek**: Raport sugeruje, że vtable+0x38==0 kończy się „then XOR EAX,EAX" (zwrot 0). Faktycznie: flag==0 LUB fallback AL==0 → **wejście do pętli** (która może zwrócić wskaźnik obiektu); XOR EAX,EAX osiągalny jest tylko przy (flag!=0 ∧ AL!=0). PATH-LOOP nie podaje warunków wejścia — czytelnik nie może ustalić, kiedy pętla działa.
- **Konkretne poprawki**: corrigendum do §3: PATH-NULL-B dzieli się na (a) flag==0 → LOOP INIT; (b) flag!=0 ∧ 00822970(AL)==0 → LOOP INIT; (c) flag!=0 ∧ AL!=0 → vtable+0x8 → XOR EAX,EAX → RET 0. Dołączyć warunki wejścia PATH-LOOP.
- **Test rewalidacji**: przejście po surowych wierszach 00823c8b→00823cae z rozstrzygnięciem obu JZ; predykat: każdy branch ma jednoznacznie opisany cel.
- Status samych claimów K05/K06/K07 pozostaje prawdziwy (niezależnie zweryfikowane).

### F-P03-02 (P2) — P03 K08/FLOW: zawyżony status „OBJECT POINTER … CONFIRMED" i jednostronna aktualizacja statusu sibling-claim
- **Źródło**: P03_PUMP\CLAIMS.json K08; P03_PUMP\FLOW.md „GLOBAL-ELEMENT-ORIGIN" („upgrades P02's GLOBAL_ELEMENT_KIND:NOT_ESTABLISHED to OBJECT_POINTER_OR_ZERO").
- **Skutek**: Pointer-hood wynika z use-as-ECX-receiver w 00826840/00826760 — ciała **nieotwarte**, ich konwencja (thiscall, RET n) nie jest w dowodzie (premise P2 jest generyczna); to promocja STRUCTURE→SEMANTICS na etykiecie CONFIRMED. Linia FLOW dodatkowo re-graduje claim sibling-pakietu bez adjudykacji rodzica.
- **Konkretne poprawki**: K08 → „mechanizm (EAX→ECX przekazanie) CONFIRMED; kind-by-use OBJECT_POINTER_OR_ZERO **STRONGLY_SUPPORTED** (konwencja 00826760/00826840 nieudowodniona w oknie)"; linię GLOBAL-ELEMENT-ORIGIN oznaczyć jako PROPOZYCJĘ standing-change do rozstrzygnięcia przez rodzica (lub otworzyć ABI jednego z callee w nowym admission, jeśli ma być CONFIRMED).
- **Test rewalidacji**: predykat: każdy status kind-claimu = najniższy status spośród jego przesłanek; przesłanka konwencji callee nieudowodniona ⇒ nie CONFIRMED.

### F-P03-03 (P3) — P03 REPORT §7: lista targetów skoków zawiera nieistniejący „00823df", pomija rzeczywisty 00823dce
- **Źródło**: P03_PUMP\REPORT.md §7; K11 (anchor = ta lista).
- **Skutek**: 00823df nie jest celem żadnego skoku ani początkiem instrukcji (środek kodowania CALL 0x0095db40); 00823dce (cel JZ @00823dc2) w liście brak. Liczba 16 targetów zgadza się przypadkiem. **Containment pozostaje PRAWDZIWE** — niezależny cenzus programowy: 21 instrukcji skoku, 16 różnych celów, wszystkie w [0x00823C10,0x00823E58) ✓.
- **Poprawka**: lista: c69,c6c,cae,cb5,d00,d13,d5c,da2,db3,dbf,dce,dff,e03,e11,e27,e44.
- **Rewalidacja**: programowy cenzus jump-target z ekstraktu (wynik w RECHECKS.json).

### F-P03-04 (P3) — P03 (REPORT §3 PATH-LOOP + FLOW E-RET-LOOP): argumenty wywołania vtable+0x3C opisane błędnie „(&[ESP+0x24], ESI)"
- **Źródło**: @00823d3b MOV EAX,[ESP+0x24] (wartość, nie LEA); @00823d44 PUSH EAX; @00823d45 PUSH ESI; @00823d46 CALL EDX.
- **Skutek**: arg1 (ostatni push) = ESI (obiekt), arg2 = WARTOŚĆ M32[ESP0−0x18] — nie adres; w raporcie kolejność odwrócona i fantomowy „&".
- **Poprawka**: „vtable+0x3C(ESI, M32[ESP+0x24])". **Rewalidacja**: kolejność push z surowych wierszy.

### F-P03-05 (P3) — P03 REPORT §2: kolejność argumentów 004D1430 odwrócona
- **Źródło**: @00823c48 PUSH ECX (&arg1_slot) — push pierwszy; @00823c50 PUSH EDX (&local ESP0−0x24) — push ostatni ⇒ arg1=&local, arg2=&arg1_slot. Raport: „(this=EDI+4, &arg1_slot_addr, &local)".
- **Poprawka**: zamienić kolejność. Zdanie „004D1430 receives a pointer to that slot" pozostaje prawdziwe.

### F-P03-06 (P3) — P03 STACK_MAP.md: błędny VA dla odczytu FS-restore („@00823E31")
- **Źródło**: STACK_MAP linia „FS restore value read from [ESP+0x30] … @00823E31". Faktycznie: MOV ECX,[ESP+0x30] @**00823E44**; 00823E31 to odczyt arg3 dla 00826760.
- **Poprawka**: VA → 00823E44 (MOV FS:[0],ECX @00823E48).

### F-P04-01 (P2) — P04 K05/REPORT §3: trzy zera FST piszą do out-arg wywołującego, NIE „do translacji skopiowanego transformu"; status CONFIRMED zawyżony
- **Źródło**: @0085c10e MOV ESI,[ESP+0x64] (głębokość ESP1−0x60 → **ESP1+4 = własny arg1 0085C0F0, wskaźnik out obiektu wywołującego**); @0085c117/119/11c FST/FST/FSTP [ESI]/[ESI+4]/[ESI+8]; @0085c112 PUSH ESI (arg 0096CD10); @0085c113 LEA ECX,[ESP+0xC]=kopia rotacji (this 0096CD10); @0085c125 MOV EAX,ESI (zwrot out-arg).
- **Skutek**: (a) zera lądują w obiekcie out (offset +0..+0xC), nie w żadnej „kopii transformu" (te są przy ESP1−0x34 i ESP1−0x58); (b) nazwanie +0..+0xC „translacją" zakłada layout, który **sprzeciwia się własnemu K03** (NiTransform: translacja @+0x24); (c) „builds a rotation-only transform" to interpretacja semantiki nieotwartego 0096CD10 — promocja STRUCTURE→SEMANTICS pod etykietą CONFIRMED. Faktycznie udowodnione: out_arg[0..0xC]:=0.0f; 0096CD10(this=&rot9, arg=&out_arg); ret=out_arg.
- **Poprawka**: K05 → „CONFIRMED (mechanizm zapisu zer i wywołania)"; interpretacja rotation-only-transform → PLAUSIBLE; opis celu zapisów → out-arg. **Rewalidacja**: niezależny trace głębokości 0085C0F0 (w RECHECKS.json).

### F-P04-02 (P2) — P04 STACK_MAP: „Callee-clean assumption NOT needed" — fałszywe i wewnętrznie sprzeczne
- **Źródło**: P04_FRONTIER\STACK_MAP.md linia 5; arytmetka: [ESP+0xAC] @0085c06a → ESP0+4 (out-arg) i epilog balansujący na ESP0−0xA8 wymagają, by wywołanie wirtualne @0085bfb5 wycofało swój 1 argument (RET 4) ORAZ 0096CB20 wycofało 0x24 (RET 0x24); w 0085BFA0 nie ma żadnego ADD ESP między prologiem a epilogiem. Tripla koherencja bufora (LEA [ESP+0x78]@−0xCC = LEA [ESP+0x54]@−0xA8 = LEA ESI,[ESP+0x54]@−0xA8 = ESP0−0x54) potwierdza dokładnie ten model.
- **Skutek**: samo „flagged as premise" by wystarczyło; zdanie „NOT needed" jest nieprawdziwe — model głębokości jest od premise callee-clean zależny w sposób load-bearing. (W P02 analogiczne premise P4 dla 006C2C50 udokumentowano ze 3 falsyfikatorami; P04 je odrzuca.)
- **Poprawka**: przeformułować jak P02-P4: „wymagane arytmetycznie; falsyfikowane przez [ESP+0xAC]≠arg i brak balansu epilogu; ciała niewidoczne ⇒ premise, nie fakt".

### F-P04-03 (P3) — P04 REPORT §1: „reorder chain producing a contiguous 12-float block at [ESP..ESP+0x2C]"; „matrix/basis computation from the 12 floats"
- **Źródło**: 9 par FLD/FSTP @0085c011–0085c055 kopiuje PIERWSZE 9 floatów ([EAX],[EAX+4]…[EAX+0x20]) w **zachowaniu kolejności** (gather) do [ESP..ESP+0x20] (obszar argumentu 0096CB20; SUB 0x24=9 DWORD). Translacja ([EAX+0x24..0x2C]) omija 0096CB20 i idzie FLD @0085c066/075/086 wprost do slotów tymczasowych.
- **Poprawka**: „9-float order-preserving gather of the rotation into [ESP..ESP+0x20]; translation bypasses 0096CB20". K02 (zwrot 12 floatów z vtable+0x24) pozostaje prawdziwe.

### F-P04-04 (P3) — P04: niewyliczone przerwy paddingowe między funkcjami
[0085C0B7,0085C0C0)=9 B, [0085C0ED,0085C0F0)=3 B, [0085C12E,0085C130)=2 B — wszystkie po RET, nieosiągalne fall-through (delta_max=12 potwierdza); containment niezagrożony, ale kompletny opis okna powinien je wyliczać (wzór: P02 B02). Obserwacja bez skutku naukowego.

### F-P02-01 (P3) — P02 STACK_MAP §7: adresy slotów argumentów 008D6D90 przesunięte o +4
- **Źródło**: §7 tabela: arg1=[E1−0x78]…arg4=[E1−0x6C], ret=[E1−0x80] — wewnętrznie sprzeczne (arg nie może być 4 B nad adresem powrotu). Poprawnie (z §2 ledger, który jest wiarygodny): arg1 begin=[E1−0x7C], arg2 tail=[E1−0x78], arg3 &out_slot=[E1−0x74], arg4 &wrapper=[E1−0x70], ret=[E1−0x80]. Wartości/kolejność argumentów w §7 poprawne; błędne tylko adresy fizyczne. Żaden claim nie zależy od tych adresów.

### F-P02-02 (P3) — P02 B08: dowodzenie przeregione („no arithmetic on EDX"; „the only memory derefs are cursor positions")
- **Źródło**: EDX w pętli kompakcji: tylko MOV/TEST/MOV-store ✓ — ale w całym oknie EDX podlega SUB/SAR/ADD @006C41C7–D0 (rozmiar dealloc — inna klasa danych); derefy w oknie to też nagłówki (C+0/C+8, global tail), nie tylko „cursor positions".
- **Skutek**: treść claimu (wartości elementów nigdy nie są dereferowane/nie porównywane jako id) PRAWDZIWA i niezależnie potwierdzona; sformułowanie dowodu nadmiarowo szerokie. **Poprawka**: zawęzić do „the loop's element register EDX participates only in MOV/TEST; EDX redefined @006C41C3 for the size computation (C-header data, not element values)".

### F-RUN-01 (P2) — RUN-LEVEL: RUN_STARTED P03/P04 podają czasy „(approx)" sprzeczne z łańcuchem guard
- **Źródło**: P03_PUMP\RUN_STARTED.json „2026-10-19T09:55:00Z(approx)"; P04_FRONTIER\RUN_STARTED.json „10:20:00Z(approx)"; guard: ADMIT P03=15:00:59.500591Z, ADMIT P04=15:22:14.390961Z (zegar spójny UTC↔mono). Żadna strefa czasowa nie zamienia 09:55 w czas późniejszy niż 15:00Z.
- **Skutek**: naruszenie CONTRACT §9 („Zapisuj faktyczne czas UTC"); metadane provenance obu pakietów fallback niedające się pogodzić z autorytatywnym ledgerem; brak też completed_utc/source_pin/verified flag (standard P01/P02).
- **Poprawka**: corrigendum: started_utc := czasy z guard-ledgera (lub wyraźnie „unknown, guard event X jest jedynym źródłem czasu"); nie fabrykować przybliżeń.
- **Rewalidacja**: predykat: każdy timestamp w pakiecie ≥ timestamp admission eventu i zgodny z mono.

### F-RUN-02 (P3) — RUN-LEVEL: brak P04_CONTRACT.json w korzeniu runu
P01–P03 mają pliki kontraktów zadań; P04 (jedyny bez worker dispatchu) nie ma — plan/request istnieją w CONTROL, ale wzorzec dokumentacyjny przerwany (CONTRACT §9: rodzic generuje CONTRACT.json małego zadania). Poprawka: dopisanie przy seale (lub jawnie odnotować, że dla DIRECT_FALLBACK generowano go nie jako plik).

### F-RUN-03 (P3) — RUN-LEVEL: P01_CONTRACT.json pole „extract_dir" nieaktualne
W R2 P01_EXTRACT jest pojedynczym plikiem (w R1 kolidująca próba miała katalog z 6 plikami); pole „extract_dir" to relikt. RUN_STARTED P01 poprawnie traktuje plik. Poprawka kosmetyczna przy seale.

### F-RUN-04 (P3) — RUN-LEVEL: P03/P04 dokumentacja pakietu cieńsza niż standard P01/P02
GATES bez kolumny evidence (P01/P02 mają per-gate evidence); artifact_index bez hashy; brak pełnej tabeli [ESP+x]; premise callee-clean 004D1430 (RET-8, load-bearing dla [ESP+0x18] @00823c5c) i wirtualnych wywołań pętli nie zapisane indywidualnie (u P02 analogiczne premise P3/P4 z falsyfikatorami). Nie narusza kontraktu wprost („artifact_index bez nieaktualnych SHA"), ale obniża audytowalność — część defektów P03/P04 wynika stąd bezpośrednio.

## 3. Weryfikacja kluczowych claims (próba niezależna)
- **P01**: pump call target/receiver/args ✓ (CALL EAX @006C2A63, ECX=ctx[1]+ctx[2], 4 stack args, callee-clean 16B — dwustronnie z P03); return origin jedyna ścieżka ✓ (cenzus: 0 skoków w 67 wierszach, jedyny RET 0x10); zero store'ów do globala w adapterze ✓ (cenzus store'y: stany SEH/FS/1 bajt arg3/push-pop — brak absolutnych zapisów poza FS); dead args ✓ (brak [ESP+0x50]@baza / [ESP+0x5C] w ogóle); containment ✓ (66/66 delta = długości kodowań — wyliczone własnoręcznie).
- **P02**: wektor begin/tail/limit ✓ (range args @006C415C/D; bound @006C418E; append @006C36F6/F8 z guardem [ESI+8] — surowe wiersze prior); pierwsze realne użycie TEST @006C4182 ✓; brak interpretacji wartości poza !=0 ✓ (z zastrzeżeniem F-P02-02); deferred cleanup 0x28/0x38 byte-exact ✓ (0x38=6+4+4; premise 006C2C50 udokumentowana z 3 falsyfikatorami — niezależnie potwierdziłem falsyfikator #2: przy cdecl-2C50 store @006C415E trafiłby w saved EBP [E1−0x38]); epilog=lustro prologu 0x44 ✓; reload tail @006C4192 tylko na ścieżce pętli ✓; store globala wyłącznie @006C41AE ✓; brak cichej promocji (memmove/dealloc = STRONGLY_SUPPORTED/PLAUSIBLE) ✓.
- **P03**: obie ścieżki zwrotu ✓ (fast: vtable+0x38 → EAX=ESI @00823E42; loop: vtable+0x4 @00823D24 → ESI → finish @00823E27 → EAX=ESI); obie pary DWORD czytane ✓ (pair[0] @00823C41, pair[1] @00823D16); „object pointer lub 0" — mechanicznie ✓ (wszystkie normalne ścieżki: ESI albo XOR EAX,EAX @cae/@dff), patrz jednak F-P03-02 (etykieta kind); containment ✓ (niezależny cenzus programowy); ABI ✓ (RET 0x10 = zgodność z P01); TLS flag ✓ (set 1 @00823D74, reset 0 @00823E21; index 0x00BA8E6C, FS:[0x2C]); EH-scope alloc/free ✓ (0095D3BE(0x80)/0095DB40 ze state −1 @00823D7B/@00823DE1); K12 arg4-dead ✓; K15 zgodność z CAND4 w zakresie ✓.
- **P04**: slot+0x24 (transform, 12 floatów) i slot+0x28 (pozycja, 3 floaty) ✓; NiTransform layout STRUCTURAL_ONLY ✓ (0x34 = 9+3+1, scale FLD1→FSTP [EAX+0x30]; brak RTTI/substytucji — K08 ✓); **brak krawędzi do primary thread** ✓ (cenzus okna: zero wątków 0xBA45E8/00823C10/pump; slot-offset similarity nieutożsamione — K09 ✓); live edge 0085C130 zadeklarowany ✓ (K07; ostatni wiersz 0085c15e 4 B wystaje po 0x0085C160 — semantyka row-start admission, wiersz atomowy, legalne); relative-position @0085C144/157 ✓ (niezależny trace głębokości potwierdza trans.x−[ESI+0x54], trans.y−[ESI+0x58]).

## 4. Zgodność z korektami C1–C8 i brak promocji kanonu
C1 (jeden kontener C=B+1C) — używany w P02/P01 bez rozdwojenia ✓ (surowe wiersze prologu: trzy inity C @006C4089/8D/91 ✓). C2 (ESI=arg4=M32[S+10h], literal 0xBA45E8 jako arg4) ✓ surowo (@006C36bf MOV ESI,[ESP+0x1c] przy głębokości S−0xC → S+0x10 ✓; PUSH 0xba45e8 @006C412e ✓). C3 ✓ (1.3). C4 ✓ (1.4). C5 (osie, H1/H2 nierozłączne) — zachowane we wszystkich 4 pakietach ✓ (P02 wprost: reload tail = kształt H2-kompatybilny bez dowodu enqueue). C6 — **rozwiązane przez body proof z jawnym zapisem konfliktu** (A06 correction_note; nie cicho) ✓. C7 (metadane księgowości prior) ✓ tylko metadane. C8 (MEMBER_VIEW conditional) — nieużyte/naruszone ✓.
Promocja kanonu: CORRECTIONS_APPLIED canonic_promotion=false ✓; żaden pakiet nie awansuje kanonu/milestone; jedyne przekroczenie granicy pakietu to linia GLOBAL-ELEMENT-ORIGIN w P03 (F-P03-02) — jawna, ale wymagająca adjudykacji rodzica; WORLD_XYZ/HISTORICAL_PLACEMENT nie claimowane ✓.

## 5. Statusy — kontrola zawyżeń (STRUCTURE→SEMANTICS)
- Wykryte nadmiary: F-P03-02 (kind=OBJECT_POINTER CONFIRMED), F-P04-01 („rotation-only transform" CONFIRMED). Oba to promocje interpretacji ponad dowód okna; oba wymagają obniżenia etykiety (STRONGLY_SUPPORTED/PLAUSIBLE) przy zachowaniu potwierdzonych mechanizmów.
- Zachowane poprawnie: memmove/dealloc (STRONGLY_SUPPORTED/PLAUSIBLE), 008D6D90 find-first-zero (PLAUSIBLE), brak RTTI, brak utożsamienia slot-offsetów (K09), NiTransform STRUCTURAL_ONLY, DATA_DOMAIN NOT_ESTABLISHED wszędzie, opaque UNKNOWN.

## 6. NOT_CHECKED (jawna lista)
1. Ciała wszystkich opaque callee (z definicji nieotwarte; m.in. 004D1430, 00415670, 008D6D90, [0xA753B4], [0xA759FC], 00826760, 00826840, 0096CB20/CF80/CD10, scope tables SEH 0xA04804/0xA04968/0xA236F8).
2. selected_lines_sha256 z eventów ADMIT — nieprzeliczalne bez znajomości normalizacji guard; zamiast tego wykonano mocniejszą bijekcję wiersz-po-wierszu z przypiętym źródłem (449/449).
3. Kod evidence_guard (narzędzie poza zakresem audytowanych pakietów; jego wyjścia zweryfikowano łańcuchem SHA + bijekcją).
4. Zamknięte runy prior w całości (QUALIFICATION_SAVED_R1, DEEP_POSTAUDIT) — czytane wyłącznie na poziomie kotwic użytych przez pakiety (selekcja wierszy potwierdzona verbatim).
5. Semantyka nieprzerwanego 0085C130 poza oknem (zgodnie z K07 — świadomie otwarta krawędź).
6. Dowód absolutny nieobecności operacji na oryginale/runtime (negatyw niedowodliwy w plikach; brak śladów pozytywnych).
7. Kolejność wierszy W1 (006C4057) wewnątrz — delta-check tylko plauzybilność (≤6) + oba seam-y; pełny ręczny decode 82 wierszy prior nie był celem tego QC (one są zamrożonym dowodem prior-runu z własnym audytem).

## 7. Werdykt końcowy QC
- P01: PASS (najwyższa jakość w runie; wzorzec dokumentacji premise/falsyfikator).
- P02: PASS_WITH_FINDINGS (2×P3; claims load-bearing wszystkie potwierdzone).
- P03: PASS_WITH_FINDINGS (nauka trzyma się: obie ścieżki zwrotu, oba DWORD pary, containment, ABI, TLS, arg4-dead — niezależnie potwierdzone; 2×P2 dokumentacyjno-statusowe + 4×P3; autor=rodzic, stąd wzmocniona rygorystyczność — defekty są realne i wymagają corrigendum, ale nie podważają wyniku).
- P04: PASS_WITH_FINDINGS (sloty/STRUCTURAL_ONLY/brak join potwierdzone; 2×P2 + 2×P3; K05/K10 wymagają re-etykietowania; K10 „strongest structural candidate" pozostaje STRONGLY_SUPPORTED — poprawnie).
- RUN-LEVEL: QC_PARTIAL — przed sealem wymagane corrigendum: F-RUN-01 (timestampy), F-P03-01/02, F-P04-01/02 (re-etykietacje i opisy); pozostałe P3 opcjonalnie przy okazji. Budżet/cady/chronologia guard: OK poza F-RUN-01.
- Proponowana NEXT_PARENT_ACTION: (1) wydać corrigendum P03/P04 (re-etykietacja statusów + poprawione opisy ścieżek/celów zapisów) w nowych katalogach bez modyfikacji zamrożonych pakietów; (2) rozstrzygnąć standing-change GLOBAL_ELEMENT_KIND (przyjąć OBJECT_POINTER_OR_ZERO jako STRONGLY_SUPPORTED albo sfinansować admission ABI 00826760/00826840); (3) seal runu z manifestem; (4) publikacja wg §10 kontraktu (bez zmian zakresu).

HARD STOP po review (zgodnie z zleceniem). To internal QC — nie zewnętrzny postaudyt, nie MASTER_ACCEPTED, nie zamknięcie milestone.
