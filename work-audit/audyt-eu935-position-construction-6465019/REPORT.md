# WORK-AUDIT REPORT — audyt-eu935-position-construction-6465019
# (audytor: Work-Audit — plik audytora, NIE jest czescia pracy wykonawcy)

PRZEDMIOT: dokonczenie przerwanego audytu runu PE_935_POSITION_CONSTRUCTION_CORRECTIONS_R1_20260913
(commit 6465019, repo eudoria-clean; poprzednia sesja Desktop przerwana na usage limit).
Zakres: ukierunkowana weryfikacja bajtowa twierdzen nosnych + adjudykacja 3 wstepnych
zarzutow przerwanej sesji. Audyt CELOWANIANY (targeted), nie pelna re-egzekucja wszystkich
bramek — granice podane nizej.
DATA: 2026-09-14. EXE: E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (Get-FileHash wlasny).

WERDYKT: POTWIERDZONY CZESCIOWO — rdzen runu (dostawca korekty Z = teren, MaTerrainManagerRuntime,
lacuch do seamu resource, korekta CREATE/EXISTING, kopia wartosci do SceneFeederObject) potwierdzony
wlasnymi bajtami; znaleziono 2 materialne defekty klasy P3 w warstwie dokumentacji (tabela 4.2 i HANDOFF)
oraz ODRZUCONO zarzut przerwanego Desktopu o +0x88/+0x8C (jego korekta byla bledna w obu polowach).
Publikacja/integralnosc: PASS.

## MACIERZ TWIERDZEN (skondensowana; dowody: probe1.log/probe2.log/probe3 stdout w tym katalogu)

| Twierdzenie runu | Moja weryfikacja | Status |
|---|---|---|
| RTTI: MaTerrainManagerRuntime (vt A7F430/A7F420 -> TD B79A28), ArkMoveSubsystem (B717E0), ArkMoverInterface (B717C0), SceneFeederObject (B78834), MovableObject (B7997C), ClientMovableObject (B79958) | wlasny spacer vtable-4->COL->TD->name, 7/7 identycznie | POTWIERDZONE |
| T-26: FSTP [ESP+0x18] @0x004C478A (nie ...89) | heksdump 0x004C4770-0x479F: D8 D1/DF E0/DD D9/F6 C4 41/75 06/D9 5C 24 18 @...8A/EB 02/DD D8/68 28 01 00 00 | POTWIERDZONE |
| EXISTING FUN_0085B3E0 ta sama korekta Z bez bramki + drop-to-ground; FSTP [ESP+0x24] @0x0085B439; JNE @0x0085B43F = DD D8 | heksdump wlasny + step qword @0xA7AF80 = 0x3FB99999A0000000 | POTWIERDZONE |
| D-3: epilogi MOV EAX,ESI @0x0073459C/@0x007345B5 (Desktop piny ...9B/B4 = POP EDI, off-by-one) | heksdump: 66 89 5F 24 @...97, 5F, 8B C6 @0x0073459C; analogicznie @0x007345B5 | POTWIERDZONE (korekta runu sluszna) |
| 0x00413340 nie jest startem funkcji; wlasciwe thunke = FUN_00413440/413450 (Enter/LeaveCriticalSection) | 0x00413340 = srodek ADD ESP,0x28 (83 C4 28 @...3E); thunke 51/FF15/...A75064|A7506C/C3 — wlasne bajty | POTWIERDZONE |
| cell_id = (floor(x/cell)<<16)|(floor(y/cell)&0xFFFF) | FUN_00936A60: C1 E6 10 / 25 FF FF 00 00 / 0B C6 — wlasne bajty | POTWIERDZONE |
| vtable-writes 0x00A7F430/0x00A7F420 @0x00538BA9/0x00538BAF, koniec 0x00538BB5 | heksdump zgodny | POTWIERDZONE |
| FUN_005094C0 = kopia wartosci [SF+0x34..0x3C] + flag +0x28=1 | 8B 44 24 04/8B 10/89 51 34/.../89 41 3C/C6 41 28 01/C2 04 00 | POTWIERDZONE |
| FUN_00853A80: 15 call-site; RET 0x10; fallbacki 0.0/10.0f(0xA7B128)/-1000.0f(0xA7B270) | census E8 wlasny: 15 adresow identycznych jak w raporcie; C2 10 00; const wlasne | POTWIERDZONE |
| MovableObject slot+0x14 = FUN_0085B010 (slot5) | u32(0x00A91E4C+0x14) = 0x0085B010 | POTWIERDZONE |
| FUN_00855340 = jedyny zapis mgr1+0x4C + REP MOVSD x13 -> mgr1+0x58 | 89 43 4C @0x0085536D + 8D 7B 58 + B9 0D + F3 A5 — wlasne bajty | POTWIERDIONE |
| singleton getter FUN_004154F0 lazy new(0x8C) | 68 8C 00 00 00 @0x00415524 | POTWIERDZONE |
| Manifest pakietu 177/177 | re-hash per plik (po korekcie MOJEGO bledu skryptu — CSV ma kolumny path,sha256) | POTWIERDZONE |
| Publikacja: 6465019 na origin (nastepnik commitow 1a490ee, 3644e5a) | git log + ls-remote master=3644e5a zawiera 6465019 w historii | POTWIERDZONE |
| REPORT 4.2: instance+0x78 = rekord[4] przez FUN_00746550 | FUN_00746550 = 8B 41 04 C3 (MOV EAX,[ECX+4]; RET) | POTWIERDZONE |
| REPORT 4.2 (wiersz param-set): fraza "zapis do +0x88 (faza B)" | FUN_00746570 = 8D 41 20 C3 -> +0x88/+0x8C = rekord[0x20]/[0x24] = pola mask-struktury 0x28, NIE para param-setu; drugi u32 pary (rec+8) w ctorze nigdzie nie zapisany | ODRZUCONE (mylaca fraza) |

## FINDINGS

F-1 [P3] REPORT 4.2 — mylne skojarzenie +0x88 z para param-setu.
  Fakty (moje bajty): +0x74=[rec], +0x78=[rec+4] (para czesc 1), +0x88/+0x8C=[rec+0x20]/[rec+0x24]
  (pola struktury maski). "Zapis do +0x88 (faza B)" w wierszu param-setu jest bledne; los drugiego
  u32 pary w instancji = nierozstrzygniety. Wplyw: zaden na lacuch Z; ale przyszly trace selectorow
  czytajacy +0x88 jako param-set poprowadzi w zla strone. Naprawa: errata wiersza tabeli.

F-2 [P3] REPORT 4.4/HANDOFF — zla numeracja slotow vtable SceneFeederObject.
  Fakty (moje bajty): slot+0=0x50A460, +4=0x5090A0, +8=0x5090B0, +C=0x50A050, +10=0x5090C0, +14=0x509580;
  vtable konczy sie na danych "dPVS" @+0x18. Run nazywal FUN_0050A460 "slot+4". Naprawa: juz wykonana
  przez run nastepny PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914 (slots 0..5) — nie powtarzac; tylko
  errata wewnatrz pakietu 6465019 jesli konwencja jej wymaga.

F-3 [P3] HANDOFF 49 — "sciezka modelu biegnie WYLACZNIE kanalem atrybut-drewa" jako konsekwencja
  negatywnego wyniku testu slotow. Negatyw w sprawdzonym zakresie nie dowodzi "wylacznie".
  (Nie dokucam: run utrzymal NOT_DEMONSTRATED uczciwie; to tylko przyklad nadmiernego jezyka
  w testie rozrozniajacym.) Naprawa: errata frazy.

F-4 [KOREKTA ZARZUTU PRZERWANEJ SESJI DESKTOP] — zarzut "para param-setu trafia do +0x88/+0x8C,
  pole +0x78 z innego pola" jest FALSZYWY w obu polowach (moje bajty: para[0]->+0x78=[rec+4];
  +0x88/+0x8C to pola mask-struktury). Przerwana sesja poprawnie zwachowala ze cos jest nie tak
  z "+0x88", ale zaproponowala bledna korekte. Do wpisania do erraty jako wycofanie zarzutu.

F-5 [SELF-KOREKTA AUDYTORA, jawna] — moj pierwszy re-hash manifestu dal "177/177 MISMATCH",
  bo moj skrypt czytal kolumne $cols[2] nieistniejaca w CSV (path,sha256). Po poprawce 177/177 PASS.
  Lekka: czytaj naglowek CSV przed uzyciem indeksow kolumn.

## POTWIERDZONE UCZCIWIE
Rdzen naukowy runu (Z=teren, lacuch, korekty x87, kopia do SF, granice STATIC-ONLY) — wlasnymi
bajtami (sondy probe1/probe2, ~40 pinow VA). Manifest 177/177. Publikacja w historii origin.

## NIESPRAWDZONE (jawne)
- pelna re-egzekucja suity F1 (28/28), tabeli x87 (21 wierszy), censusow P2 (104/15/14) — czytane,
  nie odpalane (brak capstone w moim srodowisku; suita to model wlasny wykonawcy);
- skrypty 00_CONTROL nie re-uruchamiane (hash manifestu potwierdza integralnosc);
- statyczne twierdzenia faz A/B (78cd153) poza celami sondy — dziedziczone jako kontekst, nie dowod;
- G7 composite nie re-derivowany (spokoile: manifest 177/177 + brak zmian mtime nie byl mierzony).

## CO CZYTALEM
PELNA lektura: REPORT.md (287 l.), HANDOFF.md (77 l.), QC_REPORT.md (54 l.) runu 6465019;
REPORT.md runu 3644e5a (link-identity; 120+ l.); MESSAGE transkryptu D:\Untitled.txt (wczesniej).
Przegrepowane: manifesty, dekody 01_RAW (F00528E50 w calosci). Niesprawdzone: ERRATA_R5 w calosci
(32 targety — czytalem wzmianki i QC podsumowanie), PE_MASTER_REVIEW runu 6465099 w calosci,
RUN_CONTRACT.md (776 l.).

## KROKI PO CZLOWIEKU
1. Przyjac: rdzen runu POTWIERDZONY; 3 defekty P3 do erraty (F-1, F-3; F-2 juz naprawione przez
   run nastepny) + wycofanie zarzutu przerwanego Desktopu (F-4).
2. Kontynuacja (PROMPT_OPENCODE.txt obok): dekod NiNode-vtable slot 17 (FUN_007B5390) — ostatni
   znany seam przed TRANSFORM_TO_MODEL.
