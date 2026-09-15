# WORK-AUDIT (audytor: Work-Audit, audyt: audyt-935-pub-persist-20260914-0648) — plik audytora, NIE jest częścią pracy wykonawcy
# 01_TWIERDZENIA.md — macierz twierdzen (pastowany PE_MASTER_REVIEW + komunikat commita) -> moja weryfikacja -> status

LEGENDA: POTW = POTWIERDZONE (wlasna egzekucja/odczyt), CZ.POTW = potwierdzone czesciowo, NIEPOTW = niepotwierdzone, NIESPR = niesprawdzone (+powod)

== GIT / PERSISTENCJA ==
1. "commit 6465019 == HEAD == origin == ls-remote" -> git log/rev-parse/ls-remote -> POTW w chwili publikacji; obecnie HEAD=1a490ee (nastepny run, 14.09) — ewolucja po komunikacie, nie sprzecznosc; 6465019 na lini master, ls-remote=1a490ee zgadza sie z lokalnym HEAD -> POTW (z nota ewolucji)
2. "BASE e30f99f -> HEAD 6465019; 1 commit, 180 sciezek" -> git log e30f99f..6465019 = 1; diff --name-only = 180; +29165/-1 -> POTW
3. "pakiet repo 179 plikow" -> 179 sciezek pakietu w commicie -> POTW
4. "manifest 177/177, brak self-row" -> re-hash 177/177 OK; self-row 0; pakiet=179=177+MANIFEST+artifact_index; man==ai zbiory identyczne -> POTW
5. "stare fragmenty 0/0/0, nowe dokladnie-raz (T-08 z **, T-16, undecoded)" -> blob 6465019: sub-packet/NOT covered/undeoded = 0/0/0; structure 0x28.../USE BY.../undecoded = 1/1/1; IDENTYCZNIE na HEAD -> POTW
6. "offsety 1679/3594/3818" -> wlasny odczyt UTF-8 blobu e30f99f: 1679/3594/3818 EXACT (moje wczesniejsze 1687/3628/3830 = moj blad dekodowania CP1252 — korekta wlasna) -> POTW
7. "nowy wiersz LATEST RUNS (+1/-0)" -> diff entrypoint: +1 nowy wiersz runu, -1 wiersz 31 (edit) -> POTW
8. "PE_MASTER_REVIEW opublikowany verbatim" -> committed == lokalna kopia 99_Audits (SHA 3FEDD65A identyczny) -> POTW
9. "wszystkie poprawki A-F wyladowaly" -> diffe .pre: REPORT linie 102(A+B)+153(C); ERRATA 16(E)+69/70/71(D)+nowa@72; DRAFT 10+2 nowe(F); hashe pre/post == AMEND_LOG (6/6) -> POTW
10. "oryginaly EXE/VFS byte-identical" -> SHA E7785430.../BE57818C... == piny kontraktu; zywy odczyt G7 == zapisany composite -> POTW
11. "G8 BLOCKED_BY_PROCESS -> rozwiazane publikacja" -> CSV G8=BLOCKED; commit+push istnieja -> POTW

== LICZBY / CENSUSY ==
12. "G7 composite A606CF52..., 1022 plikow" -> wlasna rekomputacja (wlasna implementacja, preorder DFS + Ordinal): A606CF52CC6804702C469777013115A80328539EADC27A9053F4F199877783D0, 1022 = 2+13+223+143+4+10+220+381+26 -> POTW (EXACT)
13. "G7 before==after byte-identical" -> SHA obu JSON = 9FB8BCE0... -> POTW
14. "censusy 104/15/14" -> wlasny capstone linear sweep (skipdata): 104/15/14/14 EXACT; lista 15 call-site'ow FUN_00853A80 == REPORT VA-po-VA; 9x WAVES w 0x48C05B..0x48C2B7 -> POTW
15. "suita 29 = 28+1" -> JSON: 29 wynikow; 28x model_eq_decoder=True; consumption_arithmetic: 34/14/14/14 + reszta 0x554 -> POTW
16. "x87 21" -> 21 wierszy; moja re-derivacja: flagi FCOM/TEST AH,0x41/zprime-bity/aux = 0 mismatch; bits<->value 42/42; z=-0,h=+0 -> 0x80000000; NaN(h)->z'=z != Math.max -> POTW
17. "SCRIPT_SHA256 last-row 20/20" -> 20 skryptow, 20/20 (ghidra_post_decomp z inline adnotacja = 3EFC41A3 == dysk) -> POTW
18. "LIVE_SCAN 41/18/0 (59)" -> wlasny tally: 17 sond, 59 wpisow, IN_REGISTER 41, HISTORICAL_PACKAGE 18, LIVE_ELSEWHERE 0 -> POTW
19. "GHIDRA_LOCAL FINAL 10/10 vs dysk; at_copy==zrodlo FINAL 10/10" -> re-hash 10/10 (db.73/74 po 189 759 488 B); at_copy vs faza-B FINAL: 10/10 (separatory / vs \ kosmetyka) -> POTW
20. "manifesty 171->177/177" -> obecny 177/177; arytmetyka 171+3(.pre)+3(nowе AMEND/QC_REVIEW/PE_MASTER_REVIEW)=177; snapshot pre-refresh (168+3) nieodtwarzalny (zastapiony refresh) -> CZ.POTW (stan koncowy POTW; snapshot QC-time NIESPR — zastapiony)
21. "AUDYT.md == Desktop REPORT.md (C4C87C2B)" -> oba SHA identyczne -> POTW
22. "D-1 window == independent_hexdumps.txt:69" -> wlasne bajty EXE == linia 69 == plik X004C4770 pakietu (16 B) -> POTW
23. "CLAIM_MATRIX 18 wierszy (16 noSnych + 2 graniczne)" -> REPORT par.6: 18 wierszy; 16 CONFIRMED + 17 NOT_DEMONSTRATED + 18 OPEN -> POTW
24. "kontrakt 776 linii, SHA zweryfikowany" -> 776/776 przeczytane; SHA == BAB59EEC (SOURCE_IDENTITIES) -> POTW
25. "tozsamosci paragraf-14 (12 plikow)" -> 12/12 SHA MATCH na blobach e30f99f (sciezka RESEARCH_FINDINGS: 06_REPORT nie 02_ANALYSIS — patrz finding P3-2) -> POTW (z nota sciezki)
26. "17 spot-checkow S0 PASS" -> S0_ERA_ASSERTION.json: spot_check_count 17, pass 17 -> POTW
27. "RTTI 7/7" -> wlasny chod COL->TD->nazwa 7/7 (MaTerrainManagerRuntime x2, ArkMoveSubsystem, ArkMoverInterface, SceneFeederObject, MovableObject, ClientMovableObject) -> POTW
28. "IAT 0xA75064/0xA7506C" -> wlasny import-walk: KERNEL32.dll Enter/LeaveCriticalSection @0xA75064/0xA7506C -> POTW

== BAJTOWE PINY NAUKOWE ==
29. FSTP [ESP+0x18] @0x004C478A (T-26) -> D9 5C 24 18 -> POTW
30. "EXISTING FSTP [ESP+0x24] @0x0085B439 (JNE cel 0x0085B43F)" -> D9 5C 24 24 @85B439; DD D8 @85B43F -> POTW
31. "EXISTING korekta bez bramki wariantu przed korekta" -> wlasne disassembly okna: korekta 0x85B426-0x85B43F; pierwszy CMP [EDI+8],3 @0x0085B451 PO zapisie z' -> POTW (nowe odkrycie runu potwierdzone bajtowo)
32. "drop-step 0x3FB99999A0000000 = 0.100000001490116119384765625 (f64(double(f32 0.1f)), nie kanoniczne f64 0.1)" -> odczyt .rdata + arytmetka wlasna -> POTW
33. "<=100 iteracji (CMP ESI,0x64)" -> 83 FE 64 @0x85B4E9 -> POTW
34. "guard FUN_0085B750 = wariant {2..7}, kolejnosc CMP 2/3/6/5/4/7" -> capstone: mov eax,[ecx+8]; cmp 2/3/6/5/4/7 + JE 0x85b774 + xor + ret -> POTW
35. "thunki FUN_00413440/FUN_00413450; 0x00413340 nie-start (28 C2 08 00); call @0x853AE8 -> 0x413440" -> wszystkie bajty -> POTW
36. "fallbacki 0.0/0.0/10.0/-1000.0" -> FLDZ @0x853AAD/@0x853B50/@0x934586; 10.0f @0xA7B128; -1000.0f @0xA7B270 -> POTW
37. "stale 14.0/25.0/0.5/-500.0/+/-32767.0f" -> wszystkie -> POTW
38. "cell_id (floor(x/cell)<<16)|(floor(y/cell)&0xFFFF)" -> SHL ESI,0x10 / AND EAX,0xFFFF / OR EAX,ESI w FUN_00936A60 + FCHS w FUN_00936B10 -> POTW
39. "filter AABB 6x FCOMPP, L2=0.0 stala" -> 6x FCOMPP w FUN_00755F90 -> POTW
40. "FUN_005094C0 = kopia wartosci +0x34..0x3C + flag 0x28=1 + RET 4" -> wlasny disassembly -> POTW
41. "vtable-writes @0x00538BA9/0x00538BAF (koniec 0x00538BB5); MOV [ESI],0xA91E4C @0x85B1C1; MOV [EBP],0xA7D458 @0x509366" -> wszystkie bajty -> POTW
42. "jedyny zapis mgr+0x4C = FUN_00855340 @0x85536D (MOV [EBX+0x4C],EAX)" -> 89 43 4C @0x85536D + census5 -> POTW (pelny census zapisow po 2-poziomowym dataflow nieodtwarzalny jednym bajtem — patrz NIESPR)
43. "FUN_00853A50 writer mgr1+0" -> 8B 44 24 04 89 01 C2 04 00 -> POTW
44. "epilogi MOV EAX,ESI @0x73459C/@0x7345B5 (D-3)" -> 66 89 5F 24 5F 8B C6 na obu adresach -> POTW
45. "D-2: 0x4C4744-45 = bajty 05 74 (srodek CMP ESI,5/JE)" -> CMP ESI,5 @0x4C4742 (83 FE 05); JE @0x4C4745 (74) -> POTW
46. "D@4508 = 0x42F9E1CB = f32 124.94100189208984" -> arytmetka wlasna -> POTW (pozycja rekordu 4508 w VFS = przeniesiona z faz A/B, nie re-derivowana w tym audycie)
47. "kanoniczne f64 0.1 = 0x3FB999999999999A != step" -> wlasna arytmetka -> POTW

== DOKUMENTY / DYSKLOSURY ==
48. "ERRATA_R5 T-01..T-32 kompletne" -> 258 linii, wszystkie 32 dispositiony, T-08 cyt. z ** + linia AMENDMENT, capstone 5.0.7 (remnant 3.12.2026 = 0) -> POTW
49. "cytaty verbatim plik:linia" -> spot-check REPORT_52 + AUDYT_55 verbatim -> POTW (probka)
50. "03_EVIDENCE puste" -> lokalnie istnieje, 0 plikow -> POTW
51. "P2_CENSUS2 pusta sonda" -> zawartosc "[]" (2 B); QC cytuje "[[]]" -> CZ.POTW (stan ujawniony slusznie; doslowny cytat QC nieprecyzyjny — patrz P3-3)
52. "PE_CURRENT_CHECKPOINT przestarzaly (2026-09-01)" -> GENERATED 2026-09-01 02:03:33, mtime 09/01 -> POTW
53. "loop-state 89968363 RUNNING_UNATTENDED, stop_reason=null, osierocony, nie tkniety" -> PE_MASTER_LOOP_STATE.json: loop 89968363-..., status RUNNING_UNATTENDED, stop_reason pusty, mtime 06.09 13:24 (przed era runu) -> POTW
54. "brak zywych kopii poza rejestrem (T-18 NOTE)" -> LIVE_SCAN 0 LIVE_ELSEWHERE + wlasne grep-y fragmentow T-08/T-16/D-4 = 0/0/0 na repo -> POTW
55. "historia git T-18 nietykalna" -> commit 78cd153 bez edycji; zywa kopia tylko entrypoint (poprawiona) -> POTW
56. "drzewo czyste poza ?? experiments/" -> git status = ?? experiments/ only (audyt wlasny nie mutowal) -> POTW

== GRANICE (utrzymane uczciwie; weryfikacja granic) ==
57. "SceneFeeder->model NOT_DEMONSTRATED; 4508/296445 OPEN; format komorek terenu za seamem UNDECODED; stan-1 mgr1+0 UNPROVEN; 19 ctor-callers NOT_CHECKED" -> utrzymane w REPORT/REVIEW/HANDOFF; granice sa rozdzialone, bez maskowania -> POTW (co do obecnosci granic)
