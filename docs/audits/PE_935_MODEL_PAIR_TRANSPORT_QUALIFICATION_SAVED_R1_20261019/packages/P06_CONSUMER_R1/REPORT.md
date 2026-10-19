# P06+P07 — właściciel kontenerów 006C4060 i początek konsumpcji (DIRECT_ANALYST_FALLBACK)

Wejścia: extracts\WINDOW_006C4057.txt (41 rows, [006C4057,006C40E0), pin 77430020B54C00DA2B8CB02CADB0333781693F4E200A369A43480B8D583CE043; admission P06) + extracts\WINDOW_006C40E0.txt (41 rows, [006C40E0,006C4160), pin 6FD34BDFBAFFB4F43593811A57769491E1471D46B0902C4E032E233B6D53C57B; admission P07, kontynuacja tego samego ciała).

## Rekonstrukcja (CONFIRMED w oknach)

**Kontener owner = 006C4060** — pełny prolog SEH (PUSH -1; PUSH 0xA04968; FS:[0]; SUB ESP,0x24; stack canary 0x00B9D8D0).
- Trzy stackowe kontenery (pola {?,tail@+4,limit@+8}; trzy inicjalizacje zerami @006C4089-91).
- **Trzy wywołania kolekcji ze statycznych tablic ID**:
  - 006C40A3 CALL 006C3FE0(ids@**0xA855F0**, C1=&[ESP+0x1C])
  - 006C40B2 CALL 006C4020(ids@**0xA858B8**, C2=&[ESP+0x24])
  - 006C40C1 CALL 006C4020(ids@**0xA858C0**, C3=&[ESP+0x2C])
- **Statyczne tablice ID = zależności zdefiniowane w czasie kompilacji** — mocny sygnał preprocessing-u list zależności zasobów.

## Łańcuch konsumpcji (CONFIRMED callsites, ciele callee opaque)

1. 006C40D0 CALL **006C3D40**(ECX=[ESP+0x34], EAX=[ESP+0x38]) — sortowanie (P08).
2. 006C40DF CALL **006C2C90**(EDX=[ESP+0x3C], ESI=[ESP+0x40]) — adjacent-find duplikatów (P09).
3. 006C40F6 CALL **006C2C50**(EAX,ESI,ECX=&[ESP+0x17]) — pod warunkiem CMP EAX,ESI (opaque).
4. 006C4100 CALL **00415670** (po MOV ESI,0x823C10) — opaque.
5. SUB ESP,0x18; budowa 6-DWORD structu na stosie {0x823C10, EDI, EAX(00415670), 0xA7957B, 0xA7957B, 1}.
6. 006C4141 CALL **006C36B0**(&out, begin, end, ?, **0xBA45E8**) — projekcja do globalnego kontenera (P10).
7. Dalej: MOV ESI,[0x00BA45EC]; MOV ECX,[0x00BA45E8] — odczyt globala po powrocie; LEA/PUSH... — okno P07 kończy się mid-body (006C4160, MOV [ESP+0x50],0x0 ostatni wiersz). **Ciało 006C4060 nie zostało w pełni domknięte** — dalsza konsumpcja istnieje, ale poza budżetem tego runu; zapisuję jako open edge, nie jako barierę dowodową.

## Wnioski

- NEAREST_REAL_CONSUMER (kolejność): 006C3D40 (sort) → 006C2C90 (dup-find) → 006C2C50 (opaque, warunkowe) → 006C36B0 (projekcja do globala 0xBA45E8).
- Pipeline: **collect → sort → dedupe-check → project do globalnego kontenera** — wszystko synchroniczne w jednym wywołaniu 006C4060.
- Slot-mapping dwoch DWORDów przekazywanych do 006C3D40/006C2C90 na konkretne pola C1/C2/C3 jest inference stack-layout (nie byte-proven; premise P6-P1).
- 0xBA45E8/0xBA45EC: global {begin, tail} — docelowo kontener wynikowy.

Actuals: P06: 2 bodies (B5), 41 rows, 5 CALL (006C40A3/B2/C1/D0/DF — 5 z 6 widocznych w pierwszym oknie; 006C40DF na ostatnim wierszu), 3 variants. P07: 1 body (kontynuacja 006C4060), 41 rows, 3 CALL (006C40F6/006C4100/006C4141), 2 variants.