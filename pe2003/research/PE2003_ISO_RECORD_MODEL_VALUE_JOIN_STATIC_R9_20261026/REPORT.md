# R9 REPORT — PE2003_ISO_RECORD_MODEL_VALUE_JOIN_STATIC_R9_20261026

STATIC_ONLY, era korpusu docelowego: ISO PC Gamer Nov 2003, build 5.1.0.0 (obraz klienta section1.bin, SHA256 D43A23B9..., VA=0x401000+offset). CANONICAL_GATE_EFFECT=NONE.

## Wynik kampanii
Cel posredni (pierwszy sprawdzalny rekord model-instancja-transform) NIE zostal osiagniety dla zadanego korpusu ISO 5.1.0.0: dane modeli/ark tej ery nie istnieja lokalnie (I1, negatyw z dokladnym zakresem). Osiagnieto natomiast: (a) CALY mechanizm deszyfrowania strumienia zasobow klienta potwierdzony bajtowo (kanoniczny Blowfish, klucz 448-bit w obrazie); (b) CALY lancuch maszynerii wiazania rekord->obiekt->node bajtowo domkniety i niezaleznie zweryfikowany (QC3 6/6); (c) pelna struktura referencyjnego templates.vfs z rekordami obu modeli (era UNKNOWN, definicje, skalarne parametry jako CANDIDATE value-source).

## Fale i ustalenia
### A1 (root fallback) — przeplyw bufora okna 0x505C00
- Zrodlo fizyczne dekodow R8 A07 = section1.bin (D43A23B9...), NIE PE2_unpacked_out.exe (561789..., inny plik).
- Dekod R8 0x505C00: wiersz0 = misaligned phantom (call 0xed835ef0 poza obrazem); prawdziwy strumien: 0x505bff mov ebp,eax / jmp / xor ebp,ebp / 0x505c05 lea. Od 0x505c05 wszystkie VA/bajty fizycznie zweryfikowane. raw_reads pre_head: etykieta 0x505bc0 poprawna (QC1; moj wstepny zarzut SHIFTED_PLUS_1 wycofany w AMENDMENT_1).
- Def-use CONFIRMED: alloc 0x1048 B (4168 = 18P+4x256S dword) -> keysetup 0x520620(ctx, key=0x6b6648, 448 bit) -> ebx; petla strumienia 0x505cc0..0x505d61; transform 0x520AD0(ecx=ctx, in/size/out) -> result size; bramka >=0x28; ingest 0x505E60(out,size,extra); string "*.ark" @0x6b0a90.
### A2 + QC2 — identyfikacja algorytmu: CONFIRMED kanoniczny Blowfish
- stale pi: S@0x6b6b10 (1024/1024 dword bajt-dokladne vs wzor Machina), P@0x6b7b10 (18/18); ciaglosc 0x6b6b10..0x6b7b58.
- 0x520620 = thiscall wrapper Initialize -> call 0x520fa0 (poprawka: QC1 podal blednie 0x521000; A2/QC2: 0x520636+0x96c=0x520fa0).
- 0x520fa0 = kanoniczna Blowfish key expansion (laduje P-table 0x6b7b10; P^=BE-slowa klucza div keylen; 9 lancuchowych szyfrowan bloku zerowego; 4x128 par S).
- 0x520AD0 = DECRYPT (QC2, drabina P[17]@+0x44 -> P[1]@+0x04 malejaco) — kierunek rozstrzygniety z surowych bajtow.
### I1 + QC2 — rzeczywista dostepnosc danych ISO
- 50.bnt = jedyny game-data unit ISO (terrain only, 51,921 .tdf, 0 .nif). I01 56/56 pokrywa 100% obszaru danych instalatora (0xC361..0x9653D99). PE_PCG.ark/FullDat_%d.ark = nazwy-nie-dowod, brak fizycznych plikow; Download.data = 12 B verbatim "1 PE_PCG.ark". Brak .ark/.nif/.bvi w czytelnym drzewie ISO9660 (42 wpisy).
- Availability modeli w ISO-corpus: NOT_OBSERVED_IN_BOUNDED_SEARCH (zakres: drzewo + pelny payload + 50.bnt + manifesty). Poza ISO: 296445 wariant 2003 CONFIRMED_AVAILABLE era-oznaczony (4 korpusy, 656795D8...); 218757 wariant 2003 (C13D08...) wylacznie COT Jan 2003; wariant ery 5.1.0.0: UNKNOWN.
### I2 + QC2 — templates.vfs (referencyjny, era UNKNOWN)
- Naglowek ArkVFS02+2xu32 (16 B); 15379 komorek x 36 B; 5255/5255 rekordow, walk EOF-exact; invariant tsize=sections+20 (5255/5255 + 20 spot-check).
- Rekordy 296445/218757: klasy plain (cell id 4508/4057), pary value-id (296445,296446)/(218757,218758), JEDEN skalar f32 param 124.941/21.2574 = CANDIDATE value-source; brak vec3/macierz/placement w calym pliku; kazde z 4 id wystepuje dokladnie raz.
- QC2 korekty agregatow I2 (nierosnace): v3!=0=275 (nie 449); v2==v1+1=1003 (nie 923); plain(nc=0&fc=0)=3065; named+floats=772; transkrypcje hashow.
### M1 (root fallback) + A3/A4/A5 + QC3 — lancuch maszynerii wiazania (CALY CONFIRMED bajtowo)
- Owner chain: A=M32[S+0x78]@0x46f207 -> 0x473c90(B=M32[A+0x34], C=M32[B+8]) -> jmp 0x451200(D=M32[C+0x1C]) -> 0x44f050(owner=M32[D+8]); owner -> call 0x52a130(owner,S,0)@0x46f21e. Konflikt +78/+34 R8 rozwiazany: kolejne hopki na roznych obiektach.
- 0x52a130: call 0x564ab0@0x52a159 = thunk jmp 0x564890 (arg shuffle; E'==E bo 564890 zwraca fetch-result, mov eax,edi@0x564a6f).
- Produkcja X: 564890 fetch E (petla vtable slot +4), store owner(entryECX, [esp+0xc]@0x564a2b) do E+0x14 przez setter 0x451730 ([ecx+0x14]=arg ret4; wywolanie @0x564a32). Odczyt X @0x52a17f mov ecx,[esi+0x14] (odczyt pola +0x14). X=owner.
- 0x417600 = get-or-create w 37-bucket map (global temp [0x6c3a70], vtable temp 0x65b024); X=entryECX; slot +8 -> M (wynik = wartosc funkcji); slot +0x24 wynik DISCARDED. Ogon 0x4176c0: intern/miss, alokacja 12B node.
- M AddRef; alloc 12B; ctor 0x533740: rec[+0]=vtable 0x65e648, rec[+4]=E weak, rec[+8]=M strong (inc [M+4]@0x533754), ret 8. Ogon 52a130: Release E, mov eax,esi@0x52a22a, ret@0x52a238 — rekord(E,M) = wartosc zwrotna 52a130, konsumowany w 46F1A0 (edi=[ebx+8]=M; alloc 0x70; 0x5257c0(new70,ebx,...)).
- Natura M: ref-counted obiekt (protokol jak E), z get-or-create mapy; "model/wezel" NIE udowodnione (vtable M, pola M poza zakresem). 564890 glowica: SEH prolog; owner stack-storage [esp+8]->[esp+0xc] potwierdzone.
### A3 — glowica okna .ark
- 0x505ba0 = CONFIRMED function entry (SEH prolog, handler 0x644387, entryECX->[esp+0x18]@0x505bbb, sub esp,0x2c); [0x65a6ac]=wskaznik funkcji (call esi@0x505bd9, nie vtable). Jedyny caller: 0x45c9b6; w okolicy string "/Scripts/" (0x6b0c54) — sciezka otwarcia skryptow .ark. Producer strumienia: klient otwiera /Scripts/*.ark, deszyfruje Blowfish (klucz statyczny w obrazie), ingeguje przez 0x505E60.

## Proces (uczciwie)
- 5 z 15 natywnych attemtow zwrocilo PUSTY wynik bez artefaktow (A1 a1/a2, M1 a1/a2, QC3 a1/a2 = 6; w tym 3 zadania wykonane jako jawny root fallback A1/M1 z zapisanymi artefaktami i QC; QC3 po 2 porazkach przeszlo w formie minimalnej a3: QC_PASS). Cicha awaria sesji dzieci niedeterministyczna; zadna nie spowodowala utraty danych; wszystkie admisje uczciwie obciazone.
- QC: Q1 QC_PARTIAL (1xP1 wycofany amendmentem), QC2 QC_PASS (1xP2, 4xP3 nierosnace), QC3 QC_PASS 6/6 (po 2 pustych attemptach).
- Budzet: patrz BUDGET_AND_CENSUS.md; actual new_bytes 381,533 B << charged ~12.06 MB.

## Case verdicts (osobno)
- 296445: patrz MODEL_CASE_296445.md — ISO-era join NOT_ESTABLISHED (dane niedostepne, zakres negatywu dokladny); najlepszy punkt zaczepienia = templates.vfs cell 4508 (era UNKNOWN).
- 218757: patrz MODEL_CASE_218757.md — jak wyzej; cell 4057.
- PE2003_WORLD_XYZ_RECOVERED=NO; PE2003_HISTORICAL_PLACEMENT=NOT_ESTABLISHED; LOCAL_SOURCE_EXHAUSTED=NO (dla er referencyjnych; dla ISO-corpus wyczerpany w badanym zakresie); SOURCE_SPECIFIC_ISO_MODELS=NOT_OBSERVED_IN_BOUNDED_SEARCH.