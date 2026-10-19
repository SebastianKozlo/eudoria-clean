# HANDOFF P01_DIRECT_R3

Established (instruction-anchored, window [006C3640,006C36B0)):
- 006C3640 = synchroniczna projekcja zakresu [arg2,arg3) stride 0x20 przez callback arg5 do append-kontenera arg4 (tail@+4, limit@+8, stride zapisu 8 = 2 DWORD), grow przez opaque 006C2E00; wynik przez *arg1.
- H1 STRONGLY_SUPPORTED; H2 REJECTED dla tego ciała; H3 ograniczone do nieznanej domeny pary.
- Brak rejestracji callbacku; brak async/queue/dispatch w oknie.

Open edges (dla T3):
1. Owning caller [006C3F50,006C3FE0) — ustalić: skąd kontener arg4, kto czyta *arg1 (nearest real consumer), skąd zakres arg2/arg3.
2. 006C2E00 grow-helper — opcjonalny osobny admission, niski priorytet (shape wystarcza dla roli mechanizmu).
3. Tożsamość callbacku w realnym callsite (podejrzenie 008BD720 z plumbingu kampanii — wymaga potwierdzenia w callerze).

Premises: P-P1 nie-NULL tail przy niepustym kontenerze; P-P2 możliwa realokacja w 006C2E00 (alias lifetime par — nie sprawdzone).

Actuals pakietu: 1 body-owner, 47 rows, 2 CALL sites, 2 variants (kons. 3/24 bodies reserved).
Attribution: DIRECT_ANALYST_FALLBACK rodzica (2 niekompletne próby dziecka P01_EXEC_R1/R2 — tylko RUN_STARTED.json).