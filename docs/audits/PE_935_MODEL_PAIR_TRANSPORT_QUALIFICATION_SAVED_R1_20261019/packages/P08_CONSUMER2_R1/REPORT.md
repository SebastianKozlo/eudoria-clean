# P08 — 006C3D40: sort pary-range + incydent admission (DIRECT_ANALYST_FALLBACK)

Wejście: extracts\WINDOW_006C3D40.txt (69 rows, [006C3D40,006C3E00), pin 33492820A0E01354E566E324F06C6F1F1BD4AFE6CF15709DB7B50AB6A333F530).

## INCYDENT ADMISSION (PARTIAL/NONCOMPLIANT — jawny)

Zarezerwowano 2 ciała (body_reservation=2); okno ujawniło **4 wejścia funkcji** (006C3D40 pełne, RET 006C3D8C; 006C3D90 pełne, RET 4 006C3DA5; 006C3DB0 pełne, RET 4 006C3DE9; 006C3DF0 ucięte). Plan B5 liczył 2 ciała — jego heurystyka nie odzwierciedla granic funkcji (znany postulat postaudytu B3: indeks B5 nie ustanawia funkcji). Zgodnie z CONTRACT §4: zachowuję ekstrakt, NIE dopisuję ADMIT po analizie, oznaczam PARTIAL/NONCOMPLIANT procesu pakietu; **zatrzymuję interpretację ciał 006C3D90/006C3DB0/006C3DF0** (notatka strukturalna tylko: istnieją, używają 006C3A50 i operacji FLD/FMUL na floatach — bez load-bearing claims). Budżet obciążony konserwatywnie 4 ciałami.

## 006C3D40 (CONFIRMED w oknie)

- arg1=ESI=begin, arg2=EDI=end (para DWORD). begin==end → RET.
- EAX=(end-begin)>>3 = liczba elementów 8B; pętla log2 (SAR EAX,1; ADD ECX,1; CMP EAX,1) → ECX=level; ADD ECX,ECX (podwojony limit głębokości).
- 006C3D76 CALL **006C3740**(ESI=begin, EDI=end, 0, 2*level, [ESP+0xC]) — główna faza sortowania (introsort-shaped: quicksort z limitem głębokości; callee opaque).
- 006C3D82 CALL **006C3330**(ESI, EDI, arg) — faza końcowa (wg wzorca std::sort: insertion-sort; callee opaque).
- ADD ESP,0x20; RET. **Semantyka: sortowanie zakresu 8-bajtowych par** — kluczowe potwierdzenie, że zebrane pary trafiają do sortowania, nie do transportu requestów.

Wzorzec (SAR log2 + 2*depth + drugi pass) jest zgodny z MSVC std::sort/_Sort, ale oznaczam to jako **shape-recognition STRONGLY_SUPPORTED**, nie CONFIRMED identyfikacji implementacji.

Actuals: 4 ciała obciążone (3 pełne + 1 ucięte), 69 rows, 5 CALL (006C3D76, 006C3D82, 006C3D9D, 006C3DBF, 006C3DFF), 2 variants.