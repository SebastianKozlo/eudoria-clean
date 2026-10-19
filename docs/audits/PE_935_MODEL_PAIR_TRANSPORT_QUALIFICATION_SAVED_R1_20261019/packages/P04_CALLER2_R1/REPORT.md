# P04+P05 — wrappery 006C3FE0/006C4020 (DIRECT_ANALYST_FALLBACK)

Wejścia: extracts\WINDOW_006C3FE0.txt (46 rows, [006C3FE0,006C4050), pin C2099CFD2DE6A90AC5B949CE5F0F9ADBAB55FDCF1E817086A19D16EA66BE6C20) + extracts\WINDOW_006C4050.txt (6 rows, [006C4050,006C4060), pin 5ED47DFDCC328B0417FFAEC3B0A527BD054EF140C5AA4F319EFD0B11A26BACA3; domknięcie uciętego epilogu 006C4020 — osobny admission P05, bez nowych ciał).

## 006C3FE0 (CONFIRMED)
- arg1=ESI ([ESP+0x10] po pushach = entry+4), arg2=EBX ([ESP+0xC]=entry+8) = kontener.
- Podwójna pętla: EBP=2 przejścia; wewn. LEA EDI,[ESI+0x10]; iteracja ESI po DWORD stride 4; dla każdego: EAX=[ESI]; PUSH EBX; PUSH EAX; CALL 006C3F50; ADD ESP,8 (cdecl). Dwa przejścia po 4 DWORD = **8 iteracji po DWORD z tablicy arg1**, każde jako id do 006C3F50(id, kontener).
- Semantycznie: pętla po tablicy 8 DWORD (dwa segmenty po 0x10 B).

## 006C4020 (CONFIRMED)
- Identyczna struktura, LEA EDI,[ESI+4] → 1 DWORD na przejście, EBP=2 → **2 iteracje** po DWORD z tablicy arg1.
- Epilog domknięty w P05: 006C4050 JNZ 006C4031; POP EDI/ESI/EBP/EBX; RET 006C4056.

## Wnioski
1. Oba wrappery to pętle "dla każdego id z tablicy wywołaj 006C3F50(id, kontener)" — rozmiar tablicy 8 (006C3FE0) vs 2 (006C4020) DWORD.
2. Kontener jest **przekazywany z zewnątrz** — wrappery nie tworzą go (CONTAINER_OWNER wyżej).
3. Struktura "tablica id → collect zależności" to klasyczny preprocessing listy zależności.

Actuals (P04): 2 function-owners, 46 rows, 2 CALL sites (006C3FFC, 006C403C), 2 targety; 3 variants kons. (P05): 0 nowych ciał (kontynuacja), 6 rows, 0 CALL, 1 variant kons.

Uwaga procesowa: DENY 000006 (plan P04b nie istniał — literówka id) — poprawnie zalogowany incydent operacyjny, bez wpływu na naukę.