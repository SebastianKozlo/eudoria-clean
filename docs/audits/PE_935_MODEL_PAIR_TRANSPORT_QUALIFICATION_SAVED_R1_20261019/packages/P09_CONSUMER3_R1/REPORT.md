# P09 — 006C2C90: adjacent-find duplikatów (DIRECT_ANALYST_FALLBACK)

Wejście: extracts\WINDOW_006C2C90.txt (58 rows, [006C2C90,006C2D10), pin 6018AA37419B9568196011978C97FE04E5350BA169938E6319C77E083055A48B).

## 006C2C90 (CONFIRMED)

- arg1=ECX=begin ([ESP+4]), arg2=EDX=end ([ESP+8]). begin==end → RET end.
- Pętla po elementach 8B: porównanie kolejnych par DWORD ([ECX]vs[EAX], [ECX+4]vs[EAX+4], EAX=ECX+8) — **adjacent-find równych sąsiednich par**.
- Przy znalezieniu równej pary sąsiedniej (i begin!=end pozostałek): CALL **006C24B0**(ECX, EDX, ECX=first-dup, [ESP+0xC], &[ESP+0x8]) — handler duplikatu (opaque), ADD ESP,0x14; RET.
- Bez duplikatu: RET end.

Semantyka: walidacja/dedupe po sortowaniu — **klasyczny preprocessing listy**, spójny z łańcuchem collect→sort→dup-find. Handler 006C24B0 pozostaje opaque (nie otwarty).

## Okno zawiera też wejście 006C2CE0 (cut)

Druga funkcja w oknie (006C2CE0+, ucięta na 006C2D10): pętla skanująca pary jako klucze 64-bit (CMP hi/lo z JC/JNC) — kształt wyszukiwania w mapie/sortowanych parach. W rezerwacji (2 ciała ≤ 3 zarezerwowane) — brak incydentu; **interpretacja zatrzymana na notatce strukturalnej** (zgodnie z metodą: niespodziewane ciało = stop interpretacji; to ciało poza głównym pytaniem pakietu).

Actuals: 2 ciała (006C2C90 pełne + 006C2CE0 ucięte), 58 rows, 1 CALL (006C2CD6), 2 variants.