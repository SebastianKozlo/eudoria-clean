# P10 — 006C36B0: projekcja par do globalnego kontenera 0xBA45E8 (DIRECT_ANALYST_FALLBACK)

Wejście: extracts\WINDOW_006C36B0.txt (42 rows, [006C36B0,006C3720), pin 91923409E53A88C5F42E9E6CCD6D6ED08790B7A7FB65A5BA8921BCD125D48F55).

## Rekonstrukcja (CONFIRMED w oknie)

Siostrzana pętla projekcyjna względem 006C3640 (ten sam szkielet):
- arg3=EBP, arg2=EDI (begin); empty→skip (JZ 006C3725 poza oknem — epilog odcięty, ale wzorzec identyczny jak 006C369C; oznaczam epilog jako PLAUSIBLE-by-symmetry, widoczny początek empty-path).
- ESI = arg5 = **0xBA45E8 (kontener globalny)** (callsite 006C412E-006C4141: PUSH 0xBA45E8; PUSH EDX; PUSH EAX; LEA ECX,[ESP+0x3C]; PUSH ECX).
- Pętla po parach stride **0x8**: dla każdej pary CALL **006C29D0**(EDX=[ESP+0x20], LEA ECX,[ESP+0x38], LEA EAX,[ESP+0x20], PUSH 0, byte[ESP+0x20]=0, [ESP+0x2C]=EDI) — transform pary → EAX (opaque; dostaje wskaźniki na stack-context 006C4060, czyli 6-DWORD struct {0x823C10, EDI, EBX, 0xA7957B, 0xA7957B, 1}).
- **Append pojedynczego DWORD EAX** do globalnego kontenera 0xBA45E8 (tail@ESI+4, limit@ESI+8, stride 4; grow helper **00475A10** przy pełnym — inny helper niż 006C2E00, bo element 4B).
- Epilog sukcesu widoczny: MOV EAX,[ESP+0x10]; MOV [EAX],ESI (out-slot = globalny kontener); dalej ucięte (POP/RET za 006C3720).

## Wnioski

- **Finalny sink w widocznym łańcuchu: globalny kontener DWORD @0xBA45E8** — pary są redukowane transformem 006C29D0 do pojedynczych wartości (id/handle?) i kolekcjonowane globalnie.
- Po powrocie 006C4060 czyta [0x00BA45E8]/[0x00BA45EC] (begin/tail globala) i kontynuuje (poza budżet).
- To domyka obraz mechanizmu: **collect (3 listy) → sort → dup-check → transform → globalna lista wartości** — kompletny preprocessing synchroniczny; żadnej ścieżki do instancji świata/transformu w tym łańcuchu.

Actuals: 1 body-owner (006C36B0; empty-path block B5 nie jest osobną funkcją; epilog ucięty), 42 rows, 2 CALL (006C36E1=006C29D0, 006C370F=00475A10), 2 variants. Epilog poza oknem: open edge (zapisany, low-risk).