# P01 — pełne 006C3640: rola mechanizmu (DIRECT_ANALYST_FALLBACK)

Attribution: analiza wykonana bezpośrednio przez PE-MASTER (rodzic) zgodnie z CONTRACT.md §10 po dwóch niekompletnych próbach dziecka (P01_EXEC_R1/P01_EXEC_R2 — każda tylko RUN_STARTED.json, pusty zwrot taska). Świeży QC sprawdzi ten wynik niezależnie.

Wejście: packages\P01_EXEC_R1\extracts\WINDOW_006C3640.txt (47 wierszy, region [0x006C3640,0x006C36B0) H5, SHA256 021062EC41487E0ABA8E70EDE0C7EEBC0F85847BA1B28F0AFA61C31935516BF7 — zweryfikowany).

## 1. Rekonstrukcja ABI (dowód instrukcyjny)

Stos na wejściu: [ESP]=ret, +4=arg1, +8=arg2, +C=arg3, +10=arg4, +14=arg5.

- 006C3640 PUSH EBP; 006C3641 MOV EBP,[ESP+0x10] → po 1 pushie [ESP+0x10]=entry+0xC → **EBP = arg3**.
- 006C3645 PUSH EDI; 006C3646 MOV EDI,[ESP+0x10] → po 2 pushach [ESP+0x10]=entry+0x8 → **EDI = arg2** (początek zakresu).
- 006C364A CMP EDI,EBP; 006C364C JZ 006C369C → **pusta pętla gdy arg2==arg3**.
- 006C364E PUSH EBX; 006C364F MOV EBX,[ESP+0x20] → entry+0x14 → **EBX = arg5 = callback**.
- 006C3653 PUSH ESI; 006C3654 MOV ESI,[ESP+0x20] → entry+0x10 → **ESI = arg4 = wskaźnik kontenera**.

Podsumowanie argumentów: arg1 = out-slot (pointer-to-pointer), arg2 = zakres begin, arg3 = zakres end (end-exclusive, porównywany przed iteracją), arg4 = kontener (jednocześnie wartość domyślna out), arg5 = callback (wywoływany, nie rejestrowany).

## 2. Pełna pętla rzutująca (CONFIRMED)

Loop head 006C3658–006C368F:
- 006C3658 MOV ECX,EDI — ECX = bieżący element zakresu.
- 006C365A CALL EBX — synchroniczne wywołanie callbacku z ECX=element; wynik w EAX (dla znanego callbacku 008BD720: EAX = element+18h — fakt kampanii S1, CONFIRMED).
- 006C365C MOV ECX,[ESI+4] — tail kontenera; 006C365F CMP ECX,[ESI+8] — tail vs limit; 006C3662 JZ 006C3678 — **pełny kontener → slow-path (grow)**.
- 006C3664 TEST ECX,ECX; 006C3666 JZ 006C3672 — gałąź NULL-tail pomija kopiowanie, ale 006C3672 nadal wykonuje ADD [ESI+4],8. To jest potencjalna niespójność przy NULL; przyjmuję premise niezerowego tail dla niepustego kontenera (alias/lifetime premise P-P1, nie dowód runtime).
- Fast path 006C3668–006C366F: MOV EDX,[EAX]; MOV [ECX],EDX; MOV EAX,[EAX+4]; MOV [ECX+4],EAX — **kopia dokładnie 2 DWORD (8 bajtów) z wyniku callbacku do tail**.
- 006C3672 ADD [ESI+4],8 — **stride zapisu = 8**.
- Slow path 006C3678–006C3685: PUSH 1; PUSH 1; LEA EDX,[ESP+0x1C]; PUSH EDX; PUSH EAX; PUSH ECX; MOV ECX,ESI; CALL 006C2E00 — helper rozbudowy z this=ESI, tail, wynik callbacku, wskaźnikiem lokalnym i dwoma jednostkami. 006C2E00 pozostaje **opaque shape** (poza oknem; nieotwarty). Etykieta "grow/append helper" wynika z kontekstu wywołania (pełny tail==limit), nie z jego body.
- 006C368A ADD EDI,0x20 — **stride elementu zakresu = 0x20 (32 bajty)**.
- 006C368D CMP EDI,EBP; 006C368F JNZ 006C3658 — warunek wyjścia: iterator == end.

## 3. Epilog i out-parametr (CONFIRMED)

- Sukces: 006C3691 MOV EAX,[ESP+0x14] → entry+4 = **arg1**; 006C3695 MOV [EAX],ESI → **\*arg1 = kontener**.
- Pusty zakres: 006C369C MOV EAX,[ESP+0xC] → arg1; 006C36A0 MOV ECX,[ESP+0x18] → **arg4**; 006C36A5 MOV [EAX],ECX → **\*arg1 = arg4** (arg4 jest zarówno domyślnym wynikiem, jak i kontenerem — spójne: pusta pętla zwraca kontener bez zmian).
- RET: 006C369B i 006C36A8 — oba należą do tej samej funkcji; B5-splits na 006C3678 (blok slow-path) i 006C369C (blok empty-path) są **wewnętrznymi blokami tej samej funkcji**, nie osobnymi ciałami (postaudyt B3).

## 4. Mechanizm: H1/H2/H3

**H1 (synchroniczna projekcja/zbieranie do kontenera): STRONGLY_SUPPORTED.** Cała rutyna to synchroniczna pętla map+append: dla każdego elementu zakresu (stride 0x20) wywołuje callback (arg5) i Dokleja (append) zwróconą parę 2×DWORD (stride 8) do kontenera [arg4; tail@+4, limit@+8], rosnąc przez 006C2E00 przy pełnym buforze, po czym zwraca kontener przez \*arg1.

**H2 (transport requestów / kolejka / scheduler): REJECTED w obrębie tego ciała.** W oknie nie istnieje: zapis wskaźnika funkcji, struktura requestu, wątek/clock/flaga async, wywołanie zwrotne konsumujące kolejkę, storage poza kontenerem. Wywołanie CALL EBX jest bezpośrednie i synchroniczne (wynik konsumowany natychmiast w 006C365C+). Zewnętrzni konsumerzy wyniku (jeśli istnieją) czytają \*arg1 — to jest do ustalenia u callera, nie tu.

**H3 (inna projekcja/rejestracja danych): PLAUSIBLE tylko co do DOMENY danych (pary mogł,_dependency vs co innego), nie co do MECHANIZMU.** Mechaniczna pętla jest projekcją; semantyka pary pozostaje nieznana z tego okna.

Callback nie jest rejestrowany: żyje w EBX tylko na czas pętli (kontrargument do starej tezy "registration"; spójne z postaudytem S2).

## 5. Co NIE zostało potwierdzone

- Tożsamość callbacku w konkretnym callsite (okno pokazuje CALL EBX=arg5; przypięcie do 008BD720 pochodzi z plumbingu kampanii, nie z tego okna).
- Rzeczywisty rozkład pól elementu zakresu (stride 0x20 potwierdzony; offset 0x18 wynika z zewnętrznego gettera).
- Semantyka grow-helpera 006C2E00 (opaque; możliwa realokacja — alias premise P-P2: przy realokacji stare adresy par mogą się unieważnić; nie sprawdzone).
- Żaden związek z instancją świata/transformem — ten etap tego nie rozstrzygał.

## 6. Liczniki actuals (paket)

- Region: [0x006C3640,0x006C36B0), 47 wierszy, end-exclusive, 1 okno.
- Ciała: 1 function-owner (006C3640); B5-splits 006C3678/006C369C = bloki. 006C2E00 = kandydat opaque, NIEOTWARTY (0 nowych body poza rezerwą 3, konserwatywnie obciążone 3/24).
- Miejsca CALL: 2 (006C365A CALL EBX — indirect; 006C3685 CALL 006C2E00), 2 różne targety.
- Wiersze: 47/4800. Warianty: 2/24 użyte konserwatywnie.
- Document body: 0/1000 (listing only).

## 7. Krawędzie do następnego etapu (T3)

- Owning caller kandydata [006C3F50,006C3FE0) należy otworzyć plan/admit (kampania znała tylko tail 006C3F98+): oczekiwać ustalenia arg4 (kontener — skąd pochodzi, kto go tworzy) i arg1 (kto czyta \*arg1 po powrocie) oraz arg2/arg3 (skąd zakres elementów 0x20).
- Przy callsite z kampanii: callback w EBX/EDI przed CALL 006C3640; ECX podczas CALL EBX = element zakresu, NIE receiver ownera.