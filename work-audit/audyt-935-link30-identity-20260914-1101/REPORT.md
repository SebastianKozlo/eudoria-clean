# WORK-AUDIT REPORT - audyt-935-link30-identity-20260914-1101
# WORK-AUDIT (audytor: Work-Audit, audyt: audyt-935-link30-identity-20260914-1101) - plik audytora, NIE jest czescia pracy wykonawcy

PRZEDMIOT: run PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 (BASE 1a490ee -> HEAD 3644e5a, 34 sciezki,
STATIC-ONLY, era PCG_9_3_5) + komunikat domkniecia wklejony przez usera (obejmujacy takze cross-run:
SLOT_CENSUS 6465019->1a490ee i self-audit runu POSITION_CONSTRUCTION konczacego sie w 6465019) +
stan dysku/gita PO publikacji. Audyt 2026-09-14 11:01-12:10, wlasna egzekucja, pelna izolacja
(zero mutacji na plikach wykonawcy; wlasne skrypty w 02_SKRYPTY/, wyniki w 03_WYNIKI/).

WERDYKT: **POTWIERDZONY CZESCIOWO**.
Nauka runu LINK30 (wszystkie twierdzenia nosne: writerzy, provenance, RTTI .?AVNiNode@@, census,
gates, publikacja) - POTWIERDZONA CALKOWICIE wlasna egzekucja co do bajtu i instrukcji (pelny
sweep odtworzony identycznie: 2 266 698 / 64 / 3643; wszystkie 3643 instrukcje CSV == moj dekod;
wszystkie piny bajtowe, 3 lancuchy RTTI, manifesty, hashe - zgodne). Ale: (1) twierdzenie
procesowe "slota 17 nie otwierano / nastepny run autoryzowany osobno PO Desktop post-audycie"
 jest ODRZUCONE przez stan dysku - run SLOT17 zostal juz wykonany (10:54-10:59) PRZED tym
post-audytem; (2) jeden wiersz censusu (R-IMM-STATIC 0x40525B) spoczywa na regule szerszej niz
 jej opis - klasyfikacja REJECTED nieudowodniona, wg wlasnej taksonomii runu powinna byc
POSSIBLE_ALIAS; (3) cztery defekty P3 (hash-typo w inwentarzu QC, falszywa linia FAIL w probe QC,
wersja interpretera w README, higiena pakietu SLOT17).

=====================================================================
MACIERZ TWIERDZEN (skondensowana; pelne dowody w 02_SKRYPTY/verify_link30_part1..10.py)
=====================================================================

GIT/PERSISTENCJA:
- HEAD==origin/master==ls-remote==3644e5ac -> POTW (wlasny git rev-parse + ls-remote)
- zakres 1a490ee..3644e5a = 1 commit, 34 sciezki = 33 pakiet + AUDIT_ENTRYPOINT.md -> POTW
- entrypoint +1/-0 (numstat 1/0), wiersz LINK30 wstawiony na czole tabeli, wiersz SLOT_CENSUS
  nietkniety (diff) -> POTW
- 6465019 = 180 sciezek; 1a490ee = 28 sciezek -> POTW (liczby z komunikatow cross-run)
- MANIFEST_SHA256.csv = 32 wiersze (33 pliki minus self); re-hash 32/32 OK -> POTW
- PE_MASTER_REVIEW SHA256 == 411e471701161013CE0F7B3067CD8D099248745107C17126E01C1FDA5892B7F0 -> POTW
- AMEND_LOG_R1 SHA256 == 52b19b44... (wiersz manifestu) -> POTW
- STAGE_ACCEPTANCE_GATES.csv == 375798e8... -> POTW; SF30_WRITER_CENSUS.csv == 71552e2a... -> POTW
- SCRIPT_SHA256 4/4 -> POTW; referencje prior-run 3/3 -> POTW
- skill pe-master-audit SKILL.md SHA256 == 8500E59A972993ED... (pin z komunikatu) + L22/L23
  obecne, dobrze uformowane -> POTW
- qc_probe 12/12 == QC s9 -> ODRZUCONE dla 1 pliku: qc4_sample_scope.py - QC s9 zapisuje
  ...F7662502 6FA... a plik/manifest maja ...F7662507 6FA... (blad transkrypcji 1 bajtu w
  wlasnym inwentarzu QC; PE_MASTER_REVIEW "all 12 byte-equal to QC section 9's hashes" niesluszne
  dla tego pliku) -> FINDING P3

EXE + BAJTY (wlasny parser PE + capstone 5.0.7, wlasne skrypty):
- EXE SHA E7785430...F31, 8015872 B, i386/PE32/0x400000/no-ASLR -> POTW
- 78 pinow bajtowych (writery 89 45 30 @0x5093C3 / 89 5E 30 @0x50A2D1, hop-tabele P1/P2,
  vtable stores 0x509366/0x50A269, block ctor 0x7B6023/29/37/41/47/5E/9F, positive control
  0x50A057..0x50A07C, magazyny slotow 7x, thunki 0x95D3C4/0x95D42A, creation chains
  0x5247E7..0x524814 / 0x47CFC6..0x47D04A, load/call split 4x, push-eax gaps 3x) -> POTW
- cele call rel32 10/10 -> POTW; IAT: 0xA75354=??2@YAPAXI@Z, 0xA7535C=??3@YAXPAX@Z -> POTW
- ECX-clobber window (3 insns, brak def ECX) -> POTW; ebp/esi single-definition -> POTW
- rep movsd: dokladnie 2 (0x50945D/0x50946E); edi = [esp+0x18] @0x5093E0 / [ebp+0x4C] @0x509462;
  ecx=9; zrodlo statyczne 0xb93c80 -> POTW (bulk-init nie pokrywa +0x30)
- combined-disp {0x34,0x3C,0x40,0x44,0x48,0xF0} przez esi w 5 ciaach kontenerow = 0 ->
  POTW (moja wczesniejsza "komplikacja" to stackowe [esp+...] poza cialami - artefakt mojego
  nadzbioru; skorygowany test = replika dokladna executora)

RTTI (wlasny walker, niezalezny):
- kalibracja: [0xA7D454]=0x00AA12B8 -> COL(sig0,off0,ptd 0xB78834,pchd 0xAA12CC) -> TD vfptr
  0xA98110 spare 0 -> ".?AVSceneFeederObject@@" -> POTW
- link: [0xA8CCF0]=0x00AAEEC8 -> ptd 0x00B936C8 -> name hex 2e3f41564e694e6f64654040 =
  ".?AVNiNode@@" -> POTW
- secondary: [0xA8CCDC]=0x00AAEE78 -> ptd 0x00B93694 -> ".?AV?$NiTPointerList@PAVNiDynamicEffect@@@@"
  -> POTW
- TD+0x0C = "NiNode@@" (nazwa bez prefiksu) - dowod defektu etykiety P2-2 -> POTW
- SF vtable 6 slotow == 0x50A460/0x5090A0/0x5090B0/0x50A050/0x5090C0/0x509580; granica
  0xA7D470 = 0x53565064 ("dPVS") -> POTW
- NiNode vtable: 47 wpisow code-pointer; 0x7B6000 NIE jest wpisem -> POTW
- slot17: [0xA8CD38] = 0x007B5390 -> POTW

SKANY:
- imm32 0xA7D458 w .text == dokladnie 2 (@0x509369, @0x50A26B) -> POTW
- absolute dword 0x509330 w calym pliku == 0 -> POTW
- E8 -> 0x509330 == {0x47D043, 0x52480F} -> POTW
- E8 -> 0x5247C0 == 7 callsites {0x44D625,0x44D677,0x44D6C8,0x528FE1,0x67B8A4,0x67C864,0x6A39ED}
  -> POTW; E8 -> 0x5094C0 == 15 -> POTW; 0x52482B/0x50A298/0x50A2A9 obcene -> POTW
- fam42c 5 trafien, fam444 4 trafienia -> POTW

CENSUS (najmocniejsza czesc - pelna niezalezna reprodukcja):
- sweep: 2 266 698 zdekodowanych / 64 restarty / 3643 kandydatow -> POTW (identyczne!)
- dystrybucja baz: eax=80, ebp=25, ebx=24, ecx=30, edi=76, edx=6, esi=637, esp=2765 -> POTW
- CSV: 3643 wierszy; klasy 2/618/3023/0; unikalne VA; kolejnosc == moj sweep; wszystkie 3643
  instrukcje == moj wlasny dekod -> POTW
- PROVEN = 0x005093C3 (89 45 30, fn 0x509330) i 0x0050A2D1 (89 5E 30, fn 0x50A240) -> POTW
- 2461 roznych function_va; 15 UNATTRIBUTED -> POTW
- wewnatrz 19 F_SF: 2 PROVEN + 7 REJECTED (6x esp + 1x cont-field 0x44D5F0), 0 POSSIBLE -> POTW
- POSSIBLE 618 wierszy w 562 roznych funkcjach -> POTW
- rozklad reasons: R-ESP 2765 / R-STACK-PTR 129 / R-CTOR-OTHER 104 / R-ZERO 18 / R-LEA-STACK 3 /
  R-EBP-INHERITED 2 / R-IMM-STATIC 1 / R-CONT-FIELD 1 = 3023; R-EBP-FRAME = 0 -> POTW
- RAW: 35086 linii; 3643 blokow (unikalne); klasy blokow == CSV w kolejnosci; linie 19-21/62/
  83-87/150 == AMEND_LOG 4b (format poprawiony) -> POTW
- deep-checks klasyfikatora: R-CTOR-OTHER 4/4 (RTTI nazwy wlasnie: .?AVArkReleaseClientApplication@@,
  .?AVNiPSysMeshUpdateModifier@@, .?AVArkIconBookUI@@, .?AVArkVegetationModel@@; vtable store
  przed kandydatem; pojedyncza def mov reg,ecx) -> POTW; R-ZERO 0x7A929C (xor eax,eax @0x7A9296)
  -> POTW; probki POSSIBLE 0x6E1A57/0x7894B6 (mov esi,ecx thiscall w klasach nieprovenowanych)
  -> POTW

SCOPE:
- census etykiet zakazanych na CA LYM pakiecie (33 pliki, moje narzedzie + reczna adjudykacja):
  52 wystapienia MODEL_BRIDGE_CONFIRMED/TRANSFORM_TO_MODEL, wszystkie = machineria (predykaty
  bramek, regexy probe QC, zdania negacyjne); zero roszsled wynikow -> POTW (zgodne z QC C7 i
  PE-MASTER; moj automat dal 5 "bez markera" - wszystkie recznie adjudykowane jako machineria:
  finalize.py:203 rozciecie stringu predykatu przez newline, qc4*/qc4b* definicje regexow/labeli,
  QC_AUDIT_R1.md:234 opis defektu detektora)
- UTF-8 4 zregenerowanych plikow valid -> POTW; REPORT/HANDOFF bez BOM (zgodne z opisem)

PROCES (odrzucone/niepotwierdzone):
- "slota 17 nie otwierano" + "nastepny run autoryzowany osobno przez czlowieka PO Desktop
  post-audycie" -> ODRZUCONE jako opis stanu obecnego: na dysku istnieje wykonany (nieopublikowany)
  run PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914 (pliki 10:54-10:59, po commicie 10:12:52 -0700,
  PRZED rozpoczeciem tego post-audytu 11:01): body slotu-17 zdekodowane do 1. calla
  (0x7B5399 -> target 0x7BF220), okno prologu targetu zdekodowane, RECEIVER_CHAIN udokumentowany.
  Tresc bajtowo PRAWdziwa (moj wlasny dekod potwierdza 6 instrukcji body + cel + okno), ALE
  run zostal rozpoczety przed bramka autoryzacji -> FINDING P1-proces (do adjudykacji czlowieka;
  nie wykluczam autoryzacji pozapasmowej, ale komunikat usera jej nie wskazuje).
- "status czysty poza experiments/" (koniec runu LINK30) - prawdziwe w chwili publikacji;
  obecnie NIEAKTUALNE (?? SLOT17 + __pycache__ w srodku pakietu SLOT17).
- R-IMM-STATIC 0x40525B: baza edx = mov edx, dword ptr [0xb6c3d8] - LADOWANIE Z GLOBALA
  (jedyny writer: 0x404C9D mov [0xb6c3d8],eax <- call 0x409080; global 0 w spoczynku), NIE
  "fixed immediate address". Odrzucenie REJECTED opiera sie na zalozeniu, ze global nigdy nie
  trzyma wskaznika SF - zalozenie miedzyproceduralne, ktorego run nie zweryfikowal (i ktore
  wlasnie objasnienia dyskutuje jako residue 618). Wg wlasnej taksonomii runu wiersz powinien
  byc POSSIBLE_ALIAS (618->619, REJECTED 3023->3022), chyba ze udowodni sie klase obiektu
  globala. Falsyfikuje tez zdanie PE_MASTER_REVIEW "the residue falls to POSSIBLE, never to
  false REJECTED" w brzmieniu uniwersalnym -> FINDING P2. (Uczciwie: QC samplowal ten wiersz
  i potwierdzil FORME defnicji - nie zweryfikowal trafnosci reguly dla tej formy.)
- Python: 03_EVIDENCE/README.md:32 "Interpreter: Python 3.12.10" vs AMEND_LOG s0/s3
  (interpreter regeneracji = 10_Scripts/python_env = 3.12.7 - moje pomiary) -> FINDING P3 (drobna
  niespojnosc dokumentacji odtwarzalnosci).
- qc1_counters.py:88 - bug porownania dict(Counter) == CLAIM (brak klucza UNRESOLVED==0) drukuje
  "claim match ... FAIL" do opublikowanego out_qc1_counters.txt:28 mimo ze liczby sa poprawne;
  QC_AUDIT_R1.md nie dyspozycjonuje tego artefaktu -> FINDING P3.
- Higiena SLOT17: __pycache__/slot17_core.cpython-312.pyc wewnatrz pakietu runu (lamanie wlasnej
  konwencji -B z LINK30 AMEND_LOG 8.4); pakiet niekompletny wg wlasnego kontraktu (brak
  REPORT/HANDOFF/STAGE_ACCEPTANCE_GATES/MANIFEST/SCRIPT_SHA256/02_ANALYSIS/03_EVIDENCE) -> P3.

=====================================================================
FINDINGS (posortowane wg wagi)
=====================================================================

[P1-proces] SLOT17 uruchomiony przed bramka autoryzacji.
  Twierdzenie: komunikat LINK30 "slota 17 nie otwierano; nastepny run (SLOT17) autoryzowany
  odrębnie przez człowieka po Desktop post-audycie" + PE_MASTER_REVIEW "NEXT_EXPERIMENT =
  DESIGNED, NOT DISPATCHED".
  Fakty: docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/ - nieśledzony, 7 plikow,
  czasy 10:54-10:59 (commit LINK30: 10:12:52 -0700; start tego post-audytu: 11:01). RUN_CONTRACT
  SLOT17 istnieje (BASE 3644e5a), run_state.json zawiera zakonczone Taski A/B/C (body 6 insns,
  first call 0x7B5399 -> 0x7BF220, prolog targetu, receiver chain).
  Moja kontrproba: dekod wlasny potwierdza bajty SLOT17 (53/8b5c2408/57/53/8bf9/e8829e0000;
  cel 0x7BF220; okno 0x7BF220 = strcmp-like) - tresc poprawna, proces przedwczesny.
  Wplyw: nie podwaza nauki LINK30; podwaza proces (HARD STOP/bastion autoryzacji) i
  aktualnosc komunikatu; wymaga decyzji czlowieka (retro-autoryzacja lub parkowanie).
  Do poprawy (NIE przezemnie): adjudykacja; jesli retro-autoryzacja - dokończyc run wg kontraktu
  (REPORT/HANDOFF/gates/manifest, -B, usunac pyc); jesli parkowanie - zapisac stan i czekac.

[P2] Census: wiersz 0x40525B (R-IMM-STATIC) - regula szersza niz opis; klasyfikacja
  nieudowodniona; wg wlasnej taksonomii = POSSIBLE_ALIAS.
  Twierdzenie: "R-IMM-STATIC: base defined by mov reg,imm32/lea reg,[imm] -> fixed data-section
  address" (polityka w census.py) + why-line "fixed immediate address (edx, dword ptr
  [0xb6c3d8] @00405250)"; PE_MASTER_REVIEW: "the residue falls to POSSIBLE, never to false
  REJECTED".
  Fakty: implementacja trace_reg_in_fn klasyfikuje take "dword ptr [0x...]" (ladowanie z adresu
  absolutnego) jako IMM; jedyny taki wiersz: 0x40525B. Receiver = wartosc globala 0xb6c3d8
  (1 writer w .text: 0x404C9D <- call 0x409080; 0 w spoczynku) - obiekt wskazywany przez global,
  nie "statyczny adres". Zalozenie "global nigdy nie trzyma SF" nie zostalo wykonane zadnym
  skanem (run skanowal zapisy DO [X+0x30], nie zapisy wskaznikow SF DO globalow) i jest tego
  samego typu co residue 618, ktore run uczciwie zostawia jako POSSIBLE.
  Moja kontrproba: wlasny dekod 0x405250/0x40525B + skan writerow/readersow globala.
  Wplyw: na twierdzenia nosne ZERO (2 PROVEN, mianownik 3643, RTTI - nietkniete); dotyka
  "3023 REJECTED z trafnymi per-row reasons" (3023->3022) i zdania "never to false REJECTED".
  Do poprawy: AMEND_LOG_R2 - rekalsyfikacja 0x40525B do POSSIBLE_ALIAS (albo dowod klasy obiektu
  globala 0xb6c3d8 - wtedy REJECTED zostaje z poprawionym uzasadnieniem); aktualizacja liczb w
  REPORT s3/HANDOFF/entrypoint row + erratum zdania "never to false REJECTED" w review;
  CSV pozostaje artefaktem historycznym z adnotacja supersession (albo regeneracja z determinism
  proof - decyzja PE-MASTER). Template: liczby censusow zawsze z podaniem standu po ktorej
  wersji.

[P3-1] QC_AUDIT_R1.md s9: blad transkrypcji hasha qc4_sample_scope.py (bajt 16: '2' zamiast '7').
  Manifest publikacyjny ma poprawny hash (re-hash 32/32 OK); plik nietkniety. PE_MASTER_REVIEW
  zdanie "all 12 qc_probe files ... byte-equal to QC section 9's pre-amendment hashes" -
  niedokladne dla tego pliku (pliki byte-equal, ale s9 RECORD zly). Poprawka: erratum 1 linia.

[P3-2] out_qc1_counters.txt:28 "claim match (2/618/3023/0, total 3643): FAIL" - falszywy wynik
  buga porownania w qc1_counters.py:88 (dict(Counter) nie ma klucza UNRESOLVED przy 0); liczby
  poprawne (wlasnorcznie potwierdzone). QC_AUDIT_R1 nie dyspozycjonuje artefaktu. Poprawka:
  erratum/notka; fix predykatu w template probe.

[P3-3] 03_EVIDENCE/README.md:32 "Python 3.12.10" vs faktyczna wersja interpretera regeneracji
  (3.12.7 - pomiary wlasne + AMEND_LOG s0). Poprawka: jednoznaczne podanie sciezki+wersji
  interpretera kanonicznego dla reprodukcji.

[P3-4] SLOT17: __pycache__/*.pyc wewnatrz pakietu (lamie wlasna konwencje -B) + pakiet
  niekompletny wg wlasnego kontraktu. Poprawka przy okazji P1.

=====================================================================
POTWIERDZONE UCZCIWIE (wykonawca zaslużyl - najmocniejsze, ze sposobem weryfikacji)
=====================================================================
- "Exactly TWO proven static writers" 0x5093C3/0x50A2D1: bajtowo, pojedyncza-definicja receiverow,
  pelne hop-tabele P1/P2 - wlasny dekod (78 pinow, 10 celow call, ECX-clobber, ebp/esi single-def).
- RTTI .?AVNiNode@@: wlasny walker (kalibracja -> link -> secondary), name-hex exaktnie;
  47 wpisow; 0x7B6000 nie-virtual; slot17 [0xA8CD38]=0x7B5390.
- Enumeration-completeness censusu: MOJA wlasna reimplementacja sweep odtworzyla 2 266 698
  instrukcji / 64 restarty / 3643 kandydatow CO DO INSTRUKCJI (identyczna kolejnosc, dystrybucja
  baz exaktna, wszystkie 3643 stringi instrukcji CSV == moj dekod). To najmocniejszy mozliwy
  dowod twierdzenia "complete writer census".
- Klasy 2/618/3023/0 + rozklad reasons (3023) + struktura F_SF (2+7+0) + 15 UNATTRIBUTED +
  2461 funkcji - wszystko rekomputowane wlasnymi skryptami z CSV/RAW.
- Coverage (i)-(iv): combined-disp przez esi w 5 ciaach = 0 (replika); rep movsd 2x z celami
  [esp+0x18]/[ebp+0x4C] (bulk nie pokrywa +0x30).
- E8/pattern censusy: {0x47D043,0x52480F}, 7 create-callsites, 15 callerow 0x5094C0, 2x imm32
  0xA7D458, 0x absolutnych 0x509330, fam42c/fam444 - wszystkie exaktnie.
- Publikacja: 34 sciezki, entrypoint +1/-0 z przetrwalym wierszem poprzednim, manifest 32/32,
  PE_MASTER_REVIEW 411e4717..., gates 375798E8..., CSV byte-identical 71552E2a...,
  skill pin 8500E59A... - wszystko re-hashowane wlasnie.
- Amendment R1: wszystkie 5 poprawek REPORT widoczne na dysku (5a-5e), raw lines 19-21/62/83-87/
  150 w formacie pos-amend, census_state line 72 poprawiona - weryfikacja diff-regions.
- QC probe'y = niezalezne implementacje (naglowki + wyjscia potwierdzaja wlasne parsery;
  zgodnosc z moja weryfikacja 100% na przemiarkach).
- Scope: zero roszsled wynikow w calym pakiecie (52 wystapienia etykiet = machineria/negacje).
- SLOT17 tresc (poza procesem): body/cel/okno targetu bajtowo poprawne (moj dekod).

=====================================================================
NIESPRAWDZONE (uczciwie)
=====================================================================
- PE_MASTER_LOOP_STATE (loop 89968363, deadline 2026-09-07): plik stanu wlasnosci pluginu nie
  znalazl sie w moich sciezkkach; twierdzenie "stale/martwy/nietkniety" niepodweryfikowane
  (brak kontradyktora na dysku; wplyw zero na nosne twierdzenia).
- 606/618 wierszy POSSIBLE poza 2 moimi + 12 probek QC: granica klasowa przyjeta jawna
  (zweryfikowalem programowo strukture calej klasy: 618/562, zero w F_SF, formy why).
- 96/104 R-CTOR-OTHER poza 8 deep-checkami (4 QC + 4 moje).
- 64 punkty restartow sweep: odtworzone numerycznie (64 == 64), nie inspekcjonowane pojedynczo.
- Ciala zakazanych funkcji (0x437F70/0x82B5A0) i slot-17 poza 6-instrukcyjnym oknem SLOT17 -
  zgodnie z zakresem (nie dekoduje poza nim).
- "44/44 byte checks" wewnetrzne QC - nie liczone; substancja odtworzona niezaleznie w calosci.
- Before-copies amendmentu (temp poza pakietem): hashe pre nieodtwarzalne z dysku; determinizm
  posredni - aktualne hashe == wszystkie piny AMEND_LOG (potwierdzone).
- Czy czlowiek autoryzowal SLOT17 pozapasmowo - nie weryfikowalne z dysku (stąd P1-proces z
  wnioskiem do adjudykacji, nie z orzekaniem winy).

=====================================================================
CO CZYTAM (FULL_READ_LOG)
=====================================================================
PELNA LEKTURA: REPORT.md (179), HANDOFF.md (48), PE_MASTER_REVIEW.md (34), QC_AUDIT_R1.md (426),
AMEND_LOG_R1.md (425), RUN_CONTRACT.md (128), SOURCE_IDENTITIES.json (44), census_state.json
(142), SCRIPT_SHA256.csv (5), MANIFEST_SHA256.csv (33), MANIFEST_NOTE_PUBLICATION.md (1),
STAGE_ACCEPTANCE_GATES.csv (7), SF30_PROVENANCE.md (72), SF30_RTTI_RAW.txt (33),
POSITIVE_CONTROL_0050A050.txt (39), 03_EVIDENCE/README.md (59), sf30_core.py (346),
census.py (1099), finalize.py (302), qc1_counters.py (154), out_qc1/2/3/5.txt (60/173/47/68),
out_qc4_sample_scope.txt (195), out_qc4b_scope_bytes.txt (149), git-show/diff/numstat
(entrypoint + commity 3644e5a/1a490ee/6465019), SKILL.md L22/L23 region, SLOT17 RUN_CONTRACT.md
(103), SLOT17 run_state.json (341), SLOT17_BODY_RAW.txt (95).
PROGRAMOWO W PELNI SPARSED (wlasne skrypty, silniejsze niz lektura wzrokiem):
SF30_WRITER_RAW.txt (wszystkie 35086 linii - bloki/why/rozklad), SF30_WRITER_CENSUS.csv (3643
wiersze - kazdy instruction vs wlasny dekod), qc2/qc3/qc4/qc4b/qc5 .py (naglowki+predykaty -
przegrepowane jako niezalezne; pelna lektura qc1).
NIESPRAWDZONE: patrz sekcja wyzej + ciala zakazanych + runtime (STATIC-ONLY).

=====================================================================
KROKI PO CZLOWIEKA
=====================================================================
1. ADJUDYKACJA SLOT17 (P1-proces): potwierdz lub odrzuc autoryzacje. Rozwiazanie A (retro-
   autoryzacja): wykonawca dokancza run wg kontraktu (REPORT/HANDOFF/gates/manifest, -B,
   bez pycache) - tresc dotychczasowa jest bajtowo weryfikowana przeze mnie. Rozwiazanie B
   (parkowanie): run zostaje nieopublikowany do formalnej autoryzacji, stan zapisany.
2. AMENDMENT R2 (P2): reklasyfikacja 0x40525B -> POSSIBLE_ALIAS (lub dowod klasy obiektu
   globala 0xb6c3d8 -> utrzymanie REJECTED z poprawionym uzasadnieniem) + erratum liczb
   (618->619 / 3023->3022) w REPORT/HANDOFF/entrypoint + korekta zdania "never to false
   REJECTED" w przyszlych review; fix template: regula R-IMM-STATIC rozdzielic na forme
   imm32 (sound) vs load-from-absolute (traktowac jak POSSIBLE).
3. ERRATA P3: QC s9 hash-typo (1 linia), dyspozycja linii FAIL w out_qc1 (1 linia + fix
   template probe), README interpreter 3.12.10 -> kanoniczna sciezka 3.12.7.
4. Kontynuacja: nauka LINK30 potwierdzona w calosci - most SceneFeeder->model mozna prowadzic
   dalej po decyzji z pkt 1 (SLOT17 albo jego re-run) z uwzglednieniem pkt 2.
