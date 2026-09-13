# Z5 — RÓŻNORODNOŚĆ ŚCIEŻEK (generality + kontrole negatywne)

RUN: PE_935_PLACEMENT_SOURCE_TRACE_R1_20260913 | ERA: EU 9.3.5 (pcg_install)

## 1. Drugi przypadek ogólności — każda kluczowa ścieżka

| ścieżka | przypadek pierwotny | drugi przypadek | dowód |
|---|---|---|---|
| builder rekordu placementu | FUN_00567770 (statek 4508-ścieżki) | FUN_00567170 (caller: FUN_00567b40 ×3 — 0x00567D24/54 + FUN_00521770) i FUN_005b5f90 (caller FUN_005b6370 ×3) — TEN SAME setterzy f90/fb0 (RUN 3 GA8_CALLERS) | ZS2/ZS4 census + RUN 3 |
| napęd FUN_00567c50 | droga A (FUN_0058db50) | drogi B (komunikat 0xB9 → FUN_005b72c0) i C (tabela .rdata → FUN_00514ef0) — 3 call-site'y: 0x0058E0B7/0x005B7567/0x00515345 | ZS10_ALL_REFS |
| odczyt pozycji z atrybutów | FUN_00846840 (0x6A4/0x6A5/0x6A8/0x6A9) | inni callerzy: FUN_0045ba30, FUN_00460580, FUN_00846bb0, FUN_00565ab0, FUN_00438450 ×2 (7 call-site'ów) | ZS1_CALLERS |
| deriver sub-obiektów | FUN_004c5580 | inni callerzy: FUN_004c5bd0, FUN_00511070, FUN_0050baf0, FUN_004ff620, FUN_004e3b70, FUN_0050c0c0, FUN_0050d480, FUN_0050fcf0, FUN_005106a0 (10 call-site'ów) | ZS1_CALLERS |
| getter D (+0x10) | FUN_0048ada0 przy FUN_00567c50 | FUN_00468910 ×5, FUN_008553d0, FUN_0064b450 ×4, ... (80 call-site'ów) | ZS3_CALLERS |
| portale .prt | próbka 505009 (967 B) | 382811 (140 B, out-of-band mały), 592741 (333 B, ostatni w indeksie) — identyczny header-tag 01 + u16 0x0101; struktura readera zgodna dla wszystkich | S11B/S12 |
| atrybuty-writers | FUN_004387a0 (0x6a5) | FUN_00514ef0 (0x2b/0x2c = X/Y!), FUN_005146b0 (0x2720/0x271f/0x3f3), FUN_005b6890 (0x271c) | ZS2/ZS4 pseudo |

Sibling templates (4752→A=126740, 2249→A=278453) istnieją w rejestrze (RUN 3 S2:
starty 97,288/93,976, crc OK) i przechodzą przez TEN SAM generyczny łańcuch —
zero hardcodów 4508/296445 w .text (RUN 3 GB-PATTERNS PASS; ten run: kontrola
0x1BDC/0x1BDE = rekord-ids w FUN_00567770/00567c50/0067bc90/0067ccd0/008553d0/0072a580
— generyczne, nie-ID-specyficzne).

## 2. Kontrole negatywne (wykonane, z wynikami)

1. **Atrybut nieistniejący → ścieżka pominięta** (STATIC-PROOF z dekompilacji):
   FUN_00567770: `bVar2 = bVar1 & 1 & bVar2` — gdy FUN_00846840 (fetch pozycji)
   NIE znajdzie atrybutu (zwróci 0) LUB FUN_00854720 (fetch trójki) zwróci 0 —
   **rekord placementu nie jest budowany** (cały blok `if (bVar2 != 0)` pominięty;
   return CONCAT31(...,bVar2) = 0). Identycznie FUN_00846840: `iVar6 == 0 → return 0`
   (walker pusty).
2. **Wrong-ID** (STATYCZNE): FUN_00846430 @0x00846430 = filtr — atrybuty
   {0x6a8,0x6a9,0x6a4,0x6a5,0x6ac,0x23} zwracają 1, **każdy inny ID → 0**
   (ścieżka transformu nie aktywuje się); analogicznie FUN_006bd1b0 mapuje
   pary; FUN_0043f4b0 switch ma domyślne pominięcie dla nieznanych typów.
3. **Dystans-gate** (droga B): FUN_005b72c0: bVar1 = porównanie
   FUN_004b2a20 (kamera?) z FUN_0085aff0 × _DAT_00a79e28 — poza progiem
   handler robi tylko FUN_005b6890(…,0x42,…) (request modelu), NIE pełny
   placement-update (LAB_005b758c early-return).
4. **Surowe trafienia dyskryminowane** (S5): LE-dword 0x66AA (negatywna kontrola)
   — 1 trafienie w .text @0x008DC1B2 = bajty środka CALL 0x008e2860 (koincydencja
   instrukcji — wykluczone walidacją Ghidry); 0x6a4: 18 kandydatów → po walidacji
   instrukcyjnej: prawdziwe użycia ID (CMP/PUSH/MOV) vs fałszywe
   (LEA [ESP+0x6a4] stack-offsety @0x00436156/0x00530345/0x005B2F4E;
   FSTP [ESI+0x6a4] pole klasy @0x00770D4D; JNZ/JZ-koincydencje @0x0073FEF5/
   0x00960177/0x00983182; CALL-koincydencja @0x00747793) — każdy z powodem.
5. **Portals.bnt**: 0 trafień ID template'ów/nif/bvi w 276 .prt (S12) —
   negatyw strukturalny roli .prt.
6. **Round-trip**: wszystkie skanowane wartości pack→unpack przed skanem
   (S5 rt_ok, S9, S10, S12 assert) ✓.

## 3. Pułapki transformacyjne wykluczone (z powodami)
- LEA ECX,[ESP+0x6a4/0x6a8] (FUN_00435ca0/0052d6d0/005b1c90) = offsety ramki,
  NIE ID atrybutów.
- FSTP dword [ESI+0x6a4/0x6a8] (FUN_00770ce0) = pola klasy (offset >0x600),
  nie NiAVObject transform (oracle RUN 3: +0x38/+0x5C/+0x68/+0x6C/+0x90).
- 0x007936-0x00793C (macierze renderu), 0x00856xx (kwaterniony) — bez zmian
  wg RUN 3.
- "CharacterPosition"/Bip01* (FUN_006b9970, stringi Bip01 @0x00A7D484+) = avatar,
  nie statyki.
- TABELE .rdata 0x00A7D8EC/0x00A7DA34 (74/72 wpisów) zawierają 0x00775CA0
  (purecall) — puste sloty handlerów, nie kandydaci transformu.
