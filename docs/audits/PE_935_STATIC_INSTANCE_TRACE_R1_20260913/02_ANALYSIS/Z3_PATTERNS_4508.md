# Z3 — TRZY WZORCE 4508 w .text (GB-PATTERNS) — ROZSTRZYGNIĘTE 3/3

RUN: PE_935_STATIC_INSTANCE_TRACE_R1_20260913 | ERA: EU 9.3.5
Round-trip pack→unpack PRZED skanem (S3): 8/8 OK (4508=0x119C LE `9c 11 00 00`;
296445=0x485FD `fd 85 04 00`; 4752/2249/11769/11655/11656/11657 — wszystkie).
Pełny skan .text (S3): **4508 LE = DOKŁADNIE 3 hity** (dane w kontrakcie); 4508 BE = 0;
296445 LE = 0. Wniosek wstępny: stała 4508 nie występuje jako imm32 NIGDZIE.

## Wzorzec 1: 0x0053270C
- **Instrukcja zawierająca**: `LEA ECX,[ESP + 0x119c]` @0x00532709, bajty `8d 8c 24 9c 11 00 00`
  (VA 0x0053270C = adres bajtów disp32 wewnątrz instrukcji, NIE początek instrukcji).
- **Operand**: disp32 = 0x119C = 4508 — **offset w ramce stosu** (adres lokalnego obiektu
  STLport basic_string @ESP+0x119C), dowód: sąsiednie `LEA ECX,[ESP+0x119c]` + `CALL [0x00A75A5C]`
  = dtor ~basic_string (IAT wy-rozstrzygnięty: PTR_~basic_string_00a75a5c); drugi kontekst
  `PUSH ECX` jako argument wywołania metody (CALL 0x0052d420, 5 arg, w tym 0x35).
- **Funkcja**: FUN_0052d6d0 (body 0x0052D6D0-0x005388BE, ~44 KB, ramka stosu >0x2C00;
  buduje stringi znak-po-znaku: `MOV BYTE [ESP+0x2BF0],0x6E/0x6F/0x6C/0x70...`).
- **Jedyny caller**: FUN_005388c0 @0x005389B4.
- **Werdykt**: PRZYPADKOWA STAŁA (stack offset). NIE jest to odwołanie do template'u 4508.

## Wzorzec 2: 0x00532769
- **Instrukcja zawierająca**: `LEA ECX,[ESP + 0x119c]` @0x00532766, bajty `8d 8c 24 9c 11 00 00`.
- **Operand**: disp32 stack (ten sam lokalny obiekt string co wzorzec 1; tu zaraz po nim
  `MOV BYTE [ESP+0x2BE8],0x6C; CALL [0x00A75A5C]` = dtor tego stringu; przed nim
  `LEA ECX,[ESP+0x167]; CALL [0x00A75A40]` (~allocator) i inne LEA+IAT — sprzątanie lokalów).
- **Funkcja**: FUN_0052d6d0 (jak wyżej).
- **Werdykt**: PRZYPADKOWA STAŁA (stack offset), ta sama ramka stosu.

## Wzorzec 3: 0x0083427E
- **Instrukcja zawierająca**: `MOV dword ptr [ESI + 0x119c],EBX` @0x0083427C, bajty
  `89 9e 9c 11 00 00`.
- **Operand**: disp32 = pole obiektu @ESI+0x119C (= offset 0x467 w tablicy dwords).
- **Funkcja**: FUN_00834010 — **KONSTRUKTOR ArkCommunicator** (dowód RTTI: dekompilat
  `*param_1_00 = ArkCommunicator::vftable` + `ArkRunnableT<class_ArkCommunicator>::vftable`;
  obiekt ~4.7 KB; zeroing ciągłe pól [ESI+0x1158..0x11D0], memset([+0x483*4],0,0x800)).
  [ESI+0x119C] = param_1_00[0x467] — zwykłe zerowane pole klasy komunikatora sieciowego.
- **Jedyny caller**: FUN_00419dd0 @0x00419FA1.
- **Werdykt**: PRZYPADKOWA STAŁA (offset pola klasy ArkCommunicator).

## Wniosek GB-PATTERNS
3/3 rozstrzygnięte: **WSZYSTKIE trzy to disp32** (2× stack-frame w jednej funkcji, 1× pole
konstruktora ArkCommunicator). ZERO odwołań do template'u 4508 w .text. Stała 4508 jako
imm32 nie istnieje (skan pełny), więc hardcode template'u-budynku 4508 w kodzie 9.3.5 —
NIE ISTNIEJE. Zgodne z E.4 poprzedniego runu (0 hitów stałych łańcucha w .text).
