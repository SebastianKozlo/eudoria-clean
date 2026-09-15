# WORK-AUDIT REPORT - audyt-pe935-slot17-oracle-minicheck-20260914-1515
# WORK-AUDIT (audytor: Work-Audit) - plik audytora, NIE jest czescia pracy wykonawcy.
# Uwaga edytorska: raport zapisany ASCII (kana? transmisji manglinguje diakrytyki) - polskie
# znaki bez ogonkow; to ograniczenie zapisu, nie tresci.

PRZEDMIOT: (1) run PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914, zakres gita
3644e5ac..5290e79 (branch audit/pe935-ninode-slot17-gb-oracle-minicheck-r1, worktree
D:\Eudoria_Reconstruction\worktrees\PE_935_NINODE_SLOT17_GB_ORACLE_MINICHECK_R1, pakiet 35 plikow
docs/audits/PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914/);
(2) werdykt PE_MASTER_REVIEW (MASTER_ACCEPTED, advisory) przeklejony przez usera - audytowany
zero-trust jako zbior twierdzen. Audyt: 2026-09-14, start 15:15, zakonczenie ~15:4x lokalne (-0700).
WSZYSTKIE 35 plikow pakietu przeczytane w calosci (FULL_READ_LOG nizej).

WERDYKT: POTWIERDZONY CZESCIOWO.
Warstwa merytoryczna runu (vtable mapy obu oracli, fingerprint 0x007B5390, +0x90 po trzech
stronach, kontrole negatywne, bramki, izolacja gita, publikacja) - POTWIERDZONA w calosci moja
niezalezna egzekucja, miejscami glebiej niz sam werdykt PE-MASTER (re-derwacja slotow z FIZYCZNYCH
NiMain.lib/.obj wlasnym parserem COFF, a nie z dumpow JSON; wlasny disasm cial oracli; rizin jako
drugi, odrebny toolchain). Odrzucenia dotycza wylacznie dokumentacji/opisow: 1xP2 (nieprawdziwe
w momencie publikacji zdjecie "no drift" local master w HANDOFF) + 6xP3, w tym dwa findinigi
przeciwko samemu werdyktowi (nieprawdziwe uzasadnienie "ta sama zawartosc" dla P3#2; nieaktualne/
nieweryfikowalne "origin/master=3644e5ac (brak dryfu)" przy FINAL). Zaden finding nie podwaza
zadnego wyniku naukowego runu ani statusu B; MASTER_ACCEPTED pozostaje w mocy.

------------------------------------------------------------------------------------------
MACIERZ TWIERDZEN (twierdzenie -> dowod -> moja weryfikacja -> status)

--- A. TWIERDZENIA WERDYKTU PE_MASTER_REVIEW ---
A1. AUDITED_RUN=PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914; zakres 3644e5ac..5290e79;
    branch audit/pe935-ninode-slot17-gb-oracle-minicheck-r1.
    -> git log/diff-tree: dokladnie 1 commit 5290e79 na bazie 3644e5a, branch istnieje.
    -> POTWIERDZONE.
A2. FINAL: worktree HEAD=5290e79, remote=5290e79 (ls-remote), worktree clean, commit path-limited
    35/35 plikow, AUDIT_ENTRYPOINT/PROJECT_STATE/master nietykane, brak commitow mieszanych.
    -> git rev-parse=5290e79e0dc4...; ls-remote origin=5290e79e0dc4...; status --short pusty;
       diff-tree: 35 sciezek, wszystkie w docs/audits/PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914/;
       AUDIT_ENTRYPOINT.md nie ma wiersza SLOT17 (Select-String: tylko LINK30).
    -> POTWIERDZONE.
A3. AUDIT_START: origin/master=3644e5ac=BASE_SHA; glowny tree brudny (sesja LINK30, nietykany).
    -> reflog master: master@{1}=3644e5a do 14:40:54; obecnie glowny tree ma tylko untracked
       (FIRSTCALL pkg + experiments/); brudne sciezki LINK30 zostaly scommitowane przez TE sesje.
    -> POTWIERDZONE.
A4. FINAL: origin/master=3644e5ac (brak dryfu); "brak commitow posrednich na master".
    -> OBECNIE origin/master=a7a6c75 (LINK30_AMEND_R2). Reflog: LOKALNY master scommitowany
       14:40:54 (a7a6c75), czyli W OKNIE runu 14:31-15:11 (sesja rownolegla, nie audytowany run).
       Czas pusha a7a6c75 na origin nieodkladutowywalny z mojej pozycji; werdykt mogl byc prawdziwy
       w chwili pomiaru (jesli push nastapil po ls-remote PE-MASTERA ~15:12) albo falszywy (jesli
       przed). Nie da sie ani potwierdzic, ani odrzucic.
    -> NIEPOTWIERDZONE (stan zmienny w czasie; patrz F1/F6).
A5. STATUS_ALGEBRA: slot17 vtable Entropii=0x7B5390 (CONFIRMED, wlasny odczyt bajtow, file_off
    0x68CD38); 0x7B5390=rekurencyjny named-lookup (CONFIRMED, disasm w calosci); GB112 slot17=
    SetSelectiveUpdateFlags (CONFIRMED); GB12 slot17=ApplyTransform (CONFIRMED, lineage VS2022
    z SHA-identycznej kopii src); Entropia +0x90=m_kWorld.m_Translate.x (CONFIRMED-structural,
    0x6C+0x24=0x90, slot 27 osobiscie odczytany); TRANSFORM_TO_MODEL=NOT_DEMONSTRATED; "SF+0x30
    NiNode=root/container (PLAUSIBLE)" zgodne z mode-bridge guard.
    -> moj skrypt 77/77: [vtable+0x44]=0x7B5390 @ file 0x68CD38 (=0x68CCF4+0x44) TAK; caly
       fingerprint bajtowo (prolog, call 0x7BF220, dzieci +0xCC/+0xD4, rekursja [edx+0x44],
       ret 4, padding); rizin: listing identyczny, zero instrukcji FP; moj parser COFF na
       fizycznych plikach: GB112 NiNode 32 sloty (15=ApplyTransform, 16=GetObjectByName,
       17=SetSelectiveUpdateFlags), GB12 NiNode 34 (13=GetGroup, 14=SetGroup, 17=ApplyTransform,
       18=GetObjectByName); moj disasm oracli potwierdza wszystkie offsety skladowe; +0x90:
       GB112 0x6C+0x24=0x90 (x), GB12 0x68+0x28=0x90 (y), Entropia slot 27 lea [ebx+0x6C] +
       rep movsd 0xD + slot 16 kotwice +0x5C/+0x68 (x); src-copy NiNode.h/NiAVObject.h
       SHA-identyczna z Gb12_Source (przeliczone).
    -> POTWIERDZONE (wszystkie pozycje).
A6. EXECUTABLE_GATE: 10/10 PASS; G5/G7 z pelnymi 4 polami; NC2 realny; NC3: 4 falsyfikatory.
    -> STAGE_ACCEPTANCE_GATES.csv: 10 bramek, wszystkie PASS, kazda z MEASURED_QUANTITY/
       INDEPENDENT_SOURCE/WHY_NON_CIRCULAR/FAILURE_CASE; NC2 liczby odtworzone przeze mnie
       z fizycznych plikow (32->34, +2 przez GetGroup/SetGroup, potwierdzone zrodlowo
       NiObject.h 53-54 vs 59-60 + NiObject.cpp 53-62); NC3 falsyfikatory bajtowo obecne
       (name-compare, child traversal, thiscall/1arg/ret4/pointer, same-slot +0x44).
    -> POTWIERDZONE.
A7. MILESTONE/CANON/CHECKPOINT: bez zmian; AUDIT_ENTRYPOINT wg kontraktu niemodyfikowany; brak
    wymagalnych retrakcji; promocja UNKNOWN->CONFIRMED dla +0x90 legalna.
    -> brak wiersza SLOT17 w AUDIT_ENTRYPOINT; commit 35 sciezek bez ENTRYPOINT; tresc pakietu
       zgodna z kontraktem HARD STOP.
    -> POTWIERDZONE.
A8. "manifest re-hash 35/35" (COVERAGE).
    -> MANIFEST_SHA256.csv ma 34 wiersze danych (nie zawiera samego siebie - slusznie, nie moze);
       moje re-hash: 34/34 OK; 35. plik commitu = manifest sam (SHA przeliczone); na dysku 35
       plikow pakietu. Fraza "35/35" czytelna jako "wszystkie 35 plikow commitu" - poprawna,
       acz nieprecyzyjna (34 wiersze manifestu + manifest).
    -> POTWIERDZONE (z precision-note).
A9. EVIDENCE_FINDINGS (P3): (1) dwa przerwane sesje "odzyskane uczciwie, wszystko zregenerowane,
    manifest 35/35 zgodny"; (2) sciezka dumpu GB112 "ta sama zawartosc (SHA re-measured)".
    -> (1) nota o uczciwosci jest w RUN_CONTRACT i jest technicznie zgodna z enumerate, ALE mtime
       plikow: 4 skrypty 00_CONTROL (14:11:34/14:12:14/14:18:25/14:24:07) i 01_RAW/GB12_SOURCE_
       LOCATORS.md (14:26:37) pochodza z sesji przerwanych - 5 plikow PRZEJETYCH, nie zregenerowanych;
       nota wylicza jako regenerowane tylko 02_ANALYSIS/*, 03_EVIDENCE/* i 01_RAW/ENTROPIA_007B5390_
       DISASM.txt (i to sie zgadza: mtimes 14:31-15:11), ale nie ujawnia jawnie przejecia locators
       GB12; "wszystko zregenerowane" w werdykcie jest naciagniete. Tresc locators zweryfikowalem
       sam (24/24 piny) - materialnie zero wplywu.
       (2) FALSZ w uzasadnieniu werdyktu: extracted\Gb112_eval zawiera WYLACZNIE Documentation
       (0 plikow .lib); NiMain.lib istnieje tylko w installed sciezce "Gamebryo 1.1.2 Evaluation\
       SDK\Win32\Lib\VC71\ReleaseLib\" (SHA zgodna z pinem - przeliczone). Pakiet opisuje to
       poprawnie (SOURCE_IDENTITIES: "Gb112_eval contains only Documentation; not required for
       any gate"). Konkluzja werdyktu (etykieta kosmetyczna, brak defektu) sie utrzymuje, ale
       uzasadnienie "ta sama zawartosc" jest nieprawdziwe.
    -> (1) POTWIERDZONE CZESCIOWO (nota technicznie zgodna; gloss werdyktu nadmierny);
       (2) ODRZUCONE (uzasadnienie werdyktu; patrz F5).
A10. CANON_CONFLICTS NONE (zgodne z 1a490ee i 3644e5a: vtable 0x00A8CCF4, slot17 0x7B5390).
    -> moje bajty: vtable 0x00A8CCF4, [vtable+0x44]=0x007B5390 identycznie jak w publikacjach
       LINK30/SLOT_CENSUS.
    -> POTWIERDZONE.
A11. NOT_CHECKED przez PE-MASTERA: pelne locators, skrypty 00_CONTROL, oryginalne naglowki GB,
    NiRTTI bajty, CROSS_VERSION pelny.
    -> ja: czytlem WSZYSTKIE 35 plikow w calosci, wszystkie 4 skrypty, 24 naglowki/rodzla GB
       (piny + wybrane linie), CROSS_VERSION pelny (18 wymiarow), NiRTTI static-init bajtowo.
       Skrypty poprawne; w docstring entropia_rtti_probe.py jest jeden falszywy opis (F4).
    -> przezemnie SPRAWDZONE (rozszerzenie pokrycia wzgledem werdyktu).

--- B. TWIERDZENIA PAKIETU (wykonawcy) - no?ne ---
B1. GB112 (era VC71 NiMain.lib): NiRefObject 1 slot; NiObject 13; NiObjectNET 13; NiAVObject 27
    (GetObjectByName@16); NiNode 32 (slot15 ApplyTransform, slot16 GetObjectByName, slot17
    SetSelectiveUpdateFlags); GetGroup/SetGroup NIE-wirtualne w 1.1.2.
    -> wlasny parser AR/COFF na fizycznym NiMain.lib (SHA FF4519AF... zweryfikowany):
       identyczne mapy; NiRefObject=1 slot w kazdym z 12 memberow; zrodla NiObject.h L53-54
       potwierdzone odczytem.
    -> POTWIERDZONE.
B2. GB12 (VS2022 .obj): NiObject 15 (GetGroup@13, SetGroup@14); NiObjectNET 15; NiAVObject 29;
    NiNode 34 (slot17 ApplyTransform, slot18 GetObjectByName); NiRefObject vtable nieemitowany;
    src kopii byte-identical.
    -> wlasny parser COFF na 6 fizycznych .obj (SHA zgodne): identyczne mapy; NiRefObject.obj
       bez ??_7NiRefObject; NiNode.h/NiAVObject.h w gb12_build\src\CoreLibs\NiMain\ SHA-identyczne
       z Gb12_Source (2F81B261.../A5B18264...).
    -> POTWIERDZONE.
B3. Entropia: vtable VA 0x00A8CCF4 (MSVC RTTI .?AVNiNode@@, lancuch baz pelny), 47 slotow (slot 47
    non-code 0x65666665), slot17=0x7B5390; prefiks ABI slot0=vector dtor 0x82E420, slot1=scalar
    thunk 0x406D50, slot2=GetRTTI 0x7B60C0 -> 0xBA7218 (NiRTTI static-init NiRTTI(0xBA7218,
    "NiNode"@0xA8CE00, 0xBA7270) @0xA6C200, .data virtual-only tail).
    -> 77/77 moich sprawdzen bajtowych (wlasciwym PE parse, wlasnym RTTI walk od zera).
    -> POTWIERDZONE.
B4. 0x7B5390: extent 0x7B5390..0x7B53E0 (ret 4 + 0xCC), thiscall 1 arg, self-check przez
    0x7BF220 (name@+0x0C, inlined byte-pair strcmp, this-or-NULL, ret 4, extent ..0x7BF270),
    dzieci count@+0xD4/array@+0xCC, NULL-skip, rekurencja wirtualna [edx+0x44] z tym samym
    argumentem, first-match-or-NULL.
    -> bajty + rizin (odrebny toolchain) - listing identyczny co do instrukcji.
    -> POTWIERDZONE.
B5. Sasiedzi: slot16=0x7B4650 transform applier (m_kLocal@+0x38, translate@+0x5C, scale@+0x68,
    dzieci +0xCC/+0xD4, rekursja wlasny slot +0x40); slot18=0x7B5160 selective-update flags
    (maski 2/4/8/0x10 na +0x20, rekursja [edx+0x48]); slot27=0x7E4820 UpdateWorldData (parent
    +0x24, local +0x38, parent world +0x6C, own world write +0x6C rep movsd x13, collision
    +0xB0 -> dispatch [eax+0x3C]).
    -> bajty (wszystkie podane wzorce); SELECTIVE_* maski potwierdzone w naglowku GB112
       (0x0002/0x0004/0x0008/0x0010).
    -> POTWIERDZONE.
B6. +0x90: GB112=m_kWorld.m_Translate.x (m_kWorld@+0x6C), GB12=m_kWorld.m_Translate.y
    (m_kWorld@+0x68; UWD addss +0x8C/+0x90/+0x94), Entropia=m_kWorld.m_Translate.x PROVEN
    in-binary (slot27 + slot16) - nie transfer z oracla.
    -> moj wlasny disasm cial oracli z fizycznych plikow: GB112 ctor lea [esi+0x38]/[esi+0x6C],
       UWD mov ecx,0xD + rep movsd (B9 0D 00 00 00 F3 A5 potwierdzone bajtem) -> [ebx+0x6C];
       GB12 ctor lea [esi+0x34]/[esi+0x68], UWD addss [esi+0x8C]/[0x90]/[0x94], scale [esi+0x98],
       write [edi+0x68]; NiTransform.h L25-27 (m_Rotate/m_Translate/m_fScale, komentarz L23-24)
       identyczny w obu wersjach; arytmetyka 0x6C+0x24=0x90 (x) / 0x68+0x28=0x90 (y) poprawna.
    -> POTWIERDZONE.
B7. Fingerprint kompilacyjny oracli: GB112 NiNode::GetObjectByName (dzieci +0xB8/+0xC0,
    call [edx+0x40], inc esi, ret 4; name +0x0C w bazie) vs GB12 (+0xB4/+0xBC, call [eax+0x48],
    name +0x08); GB112 brak .cpp dla NiMain (disasm=material dowodowy).
    -> moj disasm obu cial: wszystkie wzorce obecne.
    -> POTWIERDZONE.
B8. Bramki G0..G9 PASS (10/10), w tym G0 piny fail-closed, G1 izolacja worktree (14 brudnych
    sciezek sesji LINK30 nietknietych), G8 scope held, G9 copyright hygiene (tylko fakty
    pochodne).
    -> lektura CSV + moja weryfikacja tresci kazdej bramki no?nej (piny, git, pliki);
       pre-commit census G9 zgodny z moja lektura 35 plikow (zero payloadow zrodlowych/binarnych).
    -> POTWIERDZONE.
B9. HANDOFF: FILES_CHANGED "35 files incl. this manifest: 00_CONTROL 6, 01_RAW 3, 02_ANALYSIS 6,
    03_EVIDENCE 15, 06_REPORT 5".
    -> FAKT: 03_EVIDENCE ma 16 plikow, 06_REPORT ma 4 (suma 35 OK).
    -> ODRZUCONE (census per-katalog; patrz F2).
B10. HANDOFF: "OBSERVED_MASTER_SHA ... local master and live remote master observed equal to
    BASE_SHA; no drift"; REPORT: "BASE_SHA ... (= origin/master = live remote master = isolated
    worktree HEAD, re-verified)".
    -> reflog: local master = a7a6c75 od 14:40:54 (commit sesji LINK30), HANDOFF pisany 15:11:05,
       wiec zdjecie "local master ... no drift" bylo FALSZYWE w chwili publikacji (obserwacja
       boot-time 14:31-14:40 przeniesiona bez znacznika czasu); origin/master w 15:09-15:11
       nieweryfikowalne (push a7a6c75 nastapil w jakims momencie przed 15:15:24 - moj pomiar).
    -> ODRZUCONE dla local master (F1); NIEPOTWIERDZONE dla origin/master przy FINAL (F6).
B11. RUN_CONTRACT: "did NOT adopt any prior file on trust: every analysis document rewritten;
    every evidence file and raw listing REGENERATED; every oracle hash pin re-measured".
    -> enumeracja zgodna z mtimes (02_ANALYSIS 15:04-15:07, 03_EVIDENCE 14:39-15:09, 01_RAW
       disasm 14:57), piny re-measured (24/24 przeliczone) - ALE 5 plikow przejeto z sesji
       przerwanych bez regeneracji (4 skrypty + GB12_SOURCE_LOCATORS.md 14:26:37); nota nie
       twierdzi inaczej, ale nie ujawnia jawnie locators GB12.
    -> POTWIERDZONE CZESCIOWO (patrz F3).
B12. SOURCE_IDENTITIES: gb112_eval "contains only Documentation; not required for any gate";
    lib pinned w installed sciezce; Gb26 out-of-scope; capstone 5.0.7 via PYTHONPATH (label
    dist-info 5.0.9 - known inconsistency); python 3.12.10.
    -> zawartosc Gb112_eval sprawdzona (sama Documentation, 0 .lib); capstone self-report=5.0.7
       (dist-info 5.0.9); python 3.12.10; Gb26 na dysku, nieuzywany w pakiecie (zero wzmianek
       materialnych).
    -> POTWIERDZONE.

------------------------------------------------------------------------------------------
FINDINGS (sortowane wg wagi; NIE poprawiam sam)

F1 [P2] HANDOFF.md: nieprawdziwe w chwili publikacji zdjecie stanu gita "local master ...
    no drift".
    TWIERDZENIE: HANDOFF linia "OBSERVED_MASTER_SHA: 3644e5ac... (local master and live remote
    master observed equal to BASE_SHA; no drift)".
    FAKTY: git reflog master: a7a6c75 zcommitowany 2026-09-14 14:40:54 -0700 (rownolegla sesja
    LINK30_AMEND_R2), czyli w trakcie completing session runu (14:31-15:11); HANDOFF mtime
    15:11:05. Lokalny master w chwili pisania HANDOFF = a7a6c75, nie 3644e5a.
    KONTRPROBA: reflog + mtime (oba z dysku); SOURCE_IDENTITIES jawnie nazywa swoj pomiar
    "observed_master_sha_at_start" - poprawnie; HANDOFF nie ma znacznika czasu.
    WPLYW: brak wplywu na wyniki runu (parent commitu audytu to nadal 3644e5a; run nie tknal
    mastera - 35 sciezek pakietu). Wplyw na wiarygodnosc opisu provenance: czytelnik
    rekonstruujacy stan z HANDOFF dostanie falszywa odpowiedz.
    DO POPRAWY (wykonawca, przy okazji nastepnego runu pakietu lub erratum): dodac znaczniki
    czasu do obserwacji git-state ("at run start 14:31: local master=3644e5a; at publication
    15:11: local master=a7a6c75 - concurrent LINK30 AMEND_R2, not this run") albo przeredagowac
    na "observed at run start".

F2 [P3] HANDOFF.md: zly census per-katalog ("03_EVIDENCE 15, 06_REPORT 5").
    FAKTY: 03_EVIDENCE=16 plikow, 06_REPORT=4 (diff-tree + ls). Suma 35 sie zgadza; manifest
    obejmuje 34 pliki + sam siebie.
    DO POPRAWY: poprawic liczby w HANDOFF na 16/4 (erratum przy okazji).

F3 [P3] Nota o uczciwosci (RUN_CONTRACT/SOURCE_IDENTITIES): 5 plikow przejetych z sesji
    przerwanych bez regeneracji - nieujawnione jawnie dla GB12_SOURCE_LOCATORS.md.
    FAKTY: mtimes: entropia_rtti_probe.py 14:11:34, parse_coff_vtable.py 14:12:14,
    entropia_disasm_7b5390.py 14:18:25, coff_disasm_symbol.py 14:24:07 (sesja #1/#2),
    GB12_SOURCE_LOCATORS.md 14:26:37 (sesja #2); completing session 14:31+. Nota wylicza
    regeneracje 02_ANALYSIS/03_EVIDENCE/01_RAW-disasm (zgadza sie), ale nie rozroznia skryptow
    i locators GB12 jako "adopted, pins re-measured". Werdyktowa fraza "wszystko zregenerowane"
    jest naciagniete (5 plikow nie).
    KONTRPROBA: tresc GB12 locators zweryfikowalem w calosci sam (24/24 piny, linie zrodel) -
    materialnie poprawne; skrypty: czytane + wyjscia odtworzone z fizycznych plikow - poprawne.
    WPLYW: zerowy materialnie; higiena dokumentacji procesu.
    DO POPRAWY: w przyszlych runach jawnie wypisac plik po pliku co przejeto (z mtime) a co
    zregenerowano.

F4 [P3] 00_CONTROL/entropia_rtti_probe.py docstring: falszywy opis naglowka PE ("+4 shifted
    relative to the winnt.h layout"; modbase.py "+28 convention").
    FAKTY: moj wlasny PE parse: ImageBase=0x400000 odczytywany na STANDARDOWYM offset 0x1C
    (=+28 dziesietnie) wg winnt.h - zadne "+4 shift"; DllCharacteristics@0x46=0; magic 0x10B.
    WPLYW: zerowy (skrypt hardcoduje 0x400000 i waliduje empirycznie; ja potwierdzilem baze
    tresciowo), ale opis w docstring jest nieprawdziwy i moze wyprowadzac w blad przyszlych
    czytelnikow (kto moglby "naprawiac" poprawny offset).
    DO POPRAWY: erratum w docstring przy okazji (opcjonalnie - skrypt jest w published pakiecie,
    wiec formalnie przez amendment run).

F5 [P3] (przeciwko WERDYKTOWI PE-MASTER) uzasadnienie EVIDENCE_FINDING #2 "to ta sama zawartosc
    (SHA re-measured)" jest falszywe.
    FAKTY: D:\gamebyroengine\extracted\Gb112_eval zawiera wylacznie Documentation (0 plikow
    .lib); NiMain.lib istnieje tylko w installed sciezce SDK, ktora pakiet pinuje konsekwentnie
    (RUN_CONTRACT + SOURCE_IDENTITIES opisuja to poprawnie; SHA FF4519AF... przeliczona przez
    mnie). Nie ma zadnej "tej samej zawartosci" miedzy tymi korzeniami - Gb112_eval to podzbior
    (dokumentacja) tego samego pakietu instalacyjnego.
    WPLYW: konkluzja werdyktu (etykieta sciezkowa kosmetyczna, brak defektu runu) pozostaje
    sluszna; uzasadnienie do poprawy w przyszlych review.
    DO POPRAWY: w przyszlych PE_MASTER_REVIEW nie formolowac "same content" bez sprawdzenia
    zawartosci katalogow.

F6 [P3] (przeciwko WERDYKTOWI) "FINAL: origin/master=3644e5ac (brak dryfu)" - stan nieaktualny
    w chwili mojego audytu i czasowo nierozstrzygalny; "Brak commitow posrednich na master" -
    nieprawda dla LOKALNEGO mastera w oknie runu.
    FAKTY: teraz origin/master=a7a6c75; lokalny commit a7a6c75 nastapil 14:40:54 (wewnatrz okna
    runu 14:31-15:11; autorstwa rownoleglej sesji LINK30, nie audytowanego runu). Czas pusha
    nieznany (moj pomiar ls-remote 15:15:24 juz pokazuje a7a6c75). Nie moge udowodnic, ze
    ls-remote PE-MASTERA widzial 3644e5ac.
    WPLYW: na wyniki runu - zerowy; na precyzje werdyktu - obserwacje czasu-zywane powinny byc
    znacznikowane.
    DO POPRAWY: przy final-check zapisywac znacznik czasu pomiaru ls-remote.

F7 [P3] REPORT.md linia 5-6: "(= origin/master = live remote master = isolated worktree HEAD,
    re-verified)" - ta sama niewaznosc czasowa co F1 (dotyczy origin/master; isolated worktree
    HEAD potwierdzone, bo do 15:11:43 HEAD byl 3644e5a).
    DO POPRAWY: erratum zbiorczy z F1 przy okazji.

UWAGA do F1/F6/F7: rownolegla sesja LINK30 legalnie opublikowala swoj AMEND_R2 (a7a6c75) -
to nie jest defekt zadnej z sesji; defektem jest wylacznie brak znacznikow czasu przy
zdjeciach stanu gita w dokumentach koncowych i w werdykcie.

------------------------------------------------------------------------------------------
POTWIERDZONE UCZCIWIE (wykonawca zaslu?yl na potwierdzenie; wszystko nizej przeszlo MOJA
niezalezna egzekucja, nie lektura raportow):

1. GIT/PUBLIKACJA: 1 commit 5290e79 na bazie 3644e5a; 35/35 sciezek tylko w katalogu pakietu;
   remote SHA == HEAD (ls-remote zywotny); worktree clean; AUDIT_ENTRYPOINT bez wiersza SLOT17;
   master nie tkniety przez run; brak commitow mieszanych. (git diff-tree/rev-parse/ls-remote/status/reflog)
2. MANIFEST: 34/34 wiersze re-hash OK + manifest sam; 35 plikow na dysku = 35 sciezek commitu.
3. PINY FIZYCZNE (33 przeliczone recznie): Entropia.exe (SHA E7785430.../8015872B), NiMain.lib
   (FF4519AF.../3073590B), gb12_oracle.exe (DD7112A4.../594944B + banner EU935_GB12_ORACLE_BUILD_R1
   obecny), 6x gb12 .obj (SHA+size), 24x naglowki/zrodla GB112+GB12 (wlacznie z NiObject.cpp,
   NiAVObject.cpp, NiNode.cpp); kopie src gb12_build SHA-identyczne z Gb12_Source.
4. ENTROPIA.EXE 77/77: PE (e_lfanew 0x120, i386, 5 sekcji, IB 0x400000 standardowym offsetem,
   brak ASLR, raw==RVA dla .text/.rdata, .data RawSize 0x34000 vs VSize 0x3D6E4 - virtual tail,
   0xBA7218 w tail); vtable 0x00A8CCF4 47 slotow (slot47=0x65666665 non-code); sloty 0/1/2/16/17/18/27
   wartosci bajtowo; wlasny RTTI walk COL->TD .?AVNiNode@@->CHD 5 baz (4/3/2/1/0); 0x7B5390
   (prolog, call->0x7BF220, +0xCC/+0xD4, [edx+0x44], ret 4, 0xCC od 0x7B53E1, zero FP);
   0x7BF220 (name@+0x0C, byte-pair strcmp, idiom this-or-NULL, ret 4, int3); slot16/18/27 wzorce
   (maski 2/4/8/0x10, [edx+0x48], [eax+0x3C], rep movsd 0xD, +0x5C/+0x68); NiRTTI static-init
   bajtowo doslownie (68 70 72 BA 00 / 68 00 CE A8 00 / B9 18 72 BA 00 / E8 CC D7 CA FF / C3,
   call->0x7199E0, "NiNode\0"@0xA8CE00, 0xCC przed inicjalizatorem).
5. RIZIN (odrebny toolchain od capstone wykonawcy): listing 0x7B5390/0x7BF220 identyczny
   instrukcja-po-instrukcji z 01_RAW wykonawcy; brak instrukcji FP (podstawa NC1).
6. WLASNA RE-DERWACJA COFF (inna implementacja niz parse_coff_vtable.py): GB112 NiNode 32
   (15/16/17), NiAVObject 27 (16), NiObject 13, NiObjectNET 13, NiRefObject 1-slot w 12
   memberach; GB12 15/15/29/34 (GetGroup@13/SetGroup@14, ApplyTransform@17, GetObjectByName@18),
   NiRefObject nieemitowany. Liczby NC2 odtworzone 1:1.
7. WLASNY DISASM CIAL ORACLI z fizycznych plikow: GB112 ctor (+0x38/+0x6C/+0x20/+0x24/+0x28/
   +0xA0/+0xB0), GB112 UWD (parent +0x24, local +0x38, parent world +0x6C, own +0x6C,
   B9 0D 00 00 00 F3 A5 bajtowo, collision +0xB0, [eax+0x38]); GB112 NiNode::GetObjectByName
   (+0xB8/+0xC0, [edx+0x40], inc esi, ret 4); GB112 NiAVObject::GetObjectByName (name +0x0C);
   GB12 ctor (+0x34/+0x68/+0x1C/+0x20/+0x24/+0x9C/+0xAC); GB12 UWD (+0x20, +0x34, addss
   +0x8C/+0x90/+0x94, scale +0x98, write +0x68, collision +0xAC, [eax+0x40]); GB12 pary
   GetObjectByName (+0xB4/+0xBC, [eax+0x48]; name +0x08). => +0x90 (x/y/x) potwierdzone po
   trzech stronach z wlasnych bajtow.
8. ZRODLA na wskazanych liniach: GB112 NiObject.h L53-54 (nievirtualne GetGroup/SetGroup) +
   m_pkGroup L61; GB12 NiObject.h L59-60 (virtualne); NiObject.cpp L53-62 (NULL/no-op +
   komentarz doslowny); NiAVObject.cpp L423-432 i NiNode.cpp L749-767 (ciala zgodne z
   pseudokodem); NiTransform.h L23-27 identyczny w obu wersjach (rotate/translate/scale);
   maski SELECTIVE_* 0x0002/0x0004/0x0008/0x0010.
9. BRAMKI: 10/10 PASS, po 4 pola kazda (G5/G7 kompletne); tresci no?ne zweryfikowane;
   NC2 "proven not assumed" - potwierdzone moja re-derwacja; NC3 4 falsyfikatory bajtowo
   obecne; NC1 oba kandydatow 3-arg (mangled ABVNiMatrix3&+ABVNiPoint3&+bool / bool&+bool+bool&
   => ret 0xC) vs zmierzone ret 4.
10. HIGIENA: pakiet zawiera wylacznie fakty pochodne (moja lektura 35 plikow); main tree =
    tylko untracked WIP (FIRSTCALL + experiments/), zgodnie z kontraktem; CROSS_VERSION ma 18
    wymiarow (claim "14+" konserwatywny); EVIDENCE_INDEX 14 wierszy = 14 plikow dowodowych
    (index i README poza zestawem - spojne); capstone self-report 5.0.7 przy etykiecie dist-info
    5.0.9 (znana niespojnosc etykiet - opisana uczciwie).

------------------------------------------------------------------------------------------
NIESPRAWDZONE (uczciwie):
- Zawartosc Gb112_docs_html (CHM "Gamebryo_1_1.chm") i gb112_tools_setup - deklarowane
  non-load-bearing; nie otwieralem (uzasadnienie "member-documentation presence" przyjete
  jako niewiezcace).
- Media roots (Gamebryo_Version_1.1.2 iso, Evaluation.zip) - nie sprawdzane.
- Zawartosc niecommitowanego pakietu WIP FIRSTCALL_R1 - celowo nie czytany (kontrakt wykonawcy
  tez zakaz; nie da sie udowodnic "nie czytano" z dysku; zweryfikowalem ze jest untracked i
  poza commit 5290e79).
- Czasy pushy na origin (brak dostepu do remote reflog) - st?d NIEPOTWIERDZONE dla A4/F6.
- Stan plikow sesji przerwanych sprzed nadpisania - nieodzyskiwalny; nota o uczciwosci jest
  jedynym swiadkiem (spojna z mtimes i trescia - patrz F3).
- Oryginalne naglowki GB112: zweryfikowalem 11 plikow pinami + wybrane linie 3 plikow;
  nie czytalem calych plikow naglowkowych linia po linii (piny SHA gwarantuja zgodnosc z
  odczytami wykonawcy).

------------------------------------------------------------------------------------------
CO CZYTLEM (FULL_READ_LOG):
- W CALOSCI (35/35 plikow pakietu): 00_CONTROL/{RUN_CONTRACT.md, SOURCE_IDENTITIES.json,
  coff_disasm_symbol.py, entropia_disasm_7b5390.py, entropia_rtti_probe.py, parse_coff_vtable.py};
  01_RAW/{ENTROPIA_007B5390_DISASM.txt, GB112_SOURCE_LOCATORS.md, GB12_SOURCE_LOCATORS.md};
  02_ANALYSIS/{6 plikow}; 03_EVIDENCE/{16 plikow}; 06_REPORT/{4 pliky}.
- AUDIT_ENTRYPOINT.md: przegrepowany (SLOT17/LINK30/ORACLE); nie czytany w calosci.
- Zrodlowo: GB112 NiObject.h (L50-62), GB12 NiObject.h (L56-63), NiObject.cpp (L50-63),
  NiAVObject.cpp (L421-433), NiNode.cpp (L747-768), NiTransform.h (L20-28 obie wersje),
  NiAVObject.h (L131-138, L213-224) - fragmenty wskazane w twierdzeniach.
- NIE czytalem: CHM dokumentacji, ISO/zip media, FIRSTCALL WIP, pliki sesji LINK30 (poza
  commit-messageami w git log).

------------------------------------------------------------------------------------------
KROKI PO CZ?OWIEKA (rekomendacje - do zlecenia wykonawcy; JA nie poprawiam):
1. Przy okazji najblizszego amendment-run tego pakietu: erratum do HANDOFF (F1: znaczniki
   czasu obserwacji git; F2: census 16/4), opcjonalnie F4 (docstring probe).
2. Trwale utrwalenie werdyktu SLOT17 w repo (PE_MASTER_REVIEW.md w pakiecie + ewentualny wiersz
   LATEST RUNS w AUDIT_ENTRYPOINT) - osobny bounded persistence run, zgodnie z sugestia samego
   werdyktu (APPLICATION_READY/ORDERED_WORK). Werdykt MA tera findinigi (F5/F6), ktore warto
   uwzglednic w tresci utrwalanego wpisu.
3. Kontynuacja badawcza (nastepny bounded run; patrz PROMPT_KONTYNUACJA.md w tym katalogu):
   dekod slotow 3-15 (i opcjonalnie 28-46) vtable NiNode Entropii -> test modelu +1-shift
   na pelnym prefiksie; ewentualna promocja B->A wymaga pelnej zgodnosci ABI, a jej porazka
   bedzie rowniez wynikiem (falsyfikacja modelu).
4. Opcjonalnie: identyfikacja generacji silnika Entropii (Gb26 na dysku - celowo poza pinem
   tego runu; wymaga osobnej decyzji o dodaniu oracla do pinu).

Koniec raportu.
